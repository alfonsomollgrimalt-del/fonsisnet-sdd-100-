"""Local, offline checks for the FONSISNET SDD-100 video review workflow.

No network requests, credential handling, paid APIs, publication or deployment.
Passing these checks does NOT authorize use of unverified assets or legal claims.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

PENDING = "[PENDIENTE DE COMPROBAR]"
RISKY_CLAIM_PATTERNS = (
    r"\bgarantiz\w*\b",
    r"\bahorr\w*\s+(?:hasta\s+)?\d+\s*%",
    r"\bpaga\s+menos\s+impuestos\b",
    r"\bresultados?\s+garantizados?\b",
)
RIGHTS = {"confirmed", "public_domain", "not_required"}


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _finite_number(value: object) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_brief(brief: dict) -> list[str]:
    if not isinstance(brief, dict):
        return ["Brief: se esperaba un objeto JSON"]
    errors: list[str] = []
    for key in ("project", "objective", "audience", "language", "cta"):
        if not _text(brief.get(key)):
            errors.append(f"Falta campo de texto obligatorio: {key}")
    duration = brief.get("duration_seconds")
    if type(duration) is not int or not 5 <= duration <= 60:
        errors.append("duration_seconds debe ser entero entre 5 y 60")
    if brief.get("aspect_ratio") not in ("9:16", "16:9", "1:1"):
        errors.append("aspect_ratio no permitido")
    if "claims" in brief and (not isinstance(brief["claims"], list) or
                               not all(_text(x) for x in brief["claims"])):
        errors.append("claims debe ser una lista de afirmaciones de texto")
    contact = brief.get("contact_details", "")
    if not isinstance(contact, str):
        errors.append("contact_details debe ser texto")
    elif contact.strip() and PENDING not in contact and brief.get("contact_details_confirmed") is not True:
        errors.append("Datos de contacto requieren confirmación expresa")
    return errors


def validate_script(script: dict) -> list[str]:
    if not isinstance(script, dict):
        return ["Guion: se esperaba un objeto JSON"]
    errors: list[str] = []
    duration = script.get("duration_seconds")
    if type(duration) is not int or not 5 <= duration <= 60:
        errors.append("duration_seconds debe ser entero entre 5 y 60")
        duration = 0
    if not _text(script.get("project")):
        errors.append("Falta project")
    scenes = script.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        errors.append("El guion debe contener una lista de escenas")
        scenes = []
    prev_end = 0.0
    seen: set[str] = set()
    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            errors.append(f"Escena {index}: objeto inválido")
            continue
        scene_id = scene.get("id")
        if not _text(scene_id):
            errors.append(f"Escena {index}: id ausente")
        elif scene_id in seen:
            errors.append(f"Escena {index}: id duplicado")
        else:
            seen.add(scene_id)
        for key in ("visual", "voiceover", "on_screen_text"):
            if not _text(scene.get(key)):
                errors.append(f"Escena {index}: falta {key}")
        start, end = scene.get("start"), scene.get("end")
        if not _finite_number(start) or not _finite_number(end):
            errors.append(f"Escena {index}: tiempos inválidos")
        else:
            if start < 0 or end <= start:
                errors.append(f"Escena {index}: intervalo inválido")
            if start < prev_end:
                errors.append(f"Escena {index}: solapamiento o desorden")
            if end > duration:
                errors.append(f"Escena {index}: excede duración total")
            prev_end = end
        claims = scene.get("claims")
        if not isinstance(claims, list) or not all(_text(c) for c in claims):
            errors.append(f"Escena {index}: claims debe ser una lista de texto")
    if script.get("human_review") is not True:
        errors.append("La revisión humana debe estar activada")
    return errors


def check_claims(script: dict) -> list[dict]:
    """Triage only. Human review must cover ALL copy, not just tagged claims."""
    findings: list[dict] = []
    for scene in script.get("scenes", []):
        if not isinstance(scene, dict):
            continue
        declared = scene.get("claims") if isinstance(scene.get("claims"), list) else []
        for claim in declared:
            if not isinstance(claim, str):
                continue
            risky = any(re.search(p, claim, re.I) for p in RISKY_CLAIM_PATTERNS)
            findings.append({
                "scene_id": scene.get("id"), "claim": claim,
                "status": "BLOCKED_REVIEW_REQUIRED" if risky else "PENDING_SOURCE_AND_REVIEW",
                "source": PENDING, "checked_at": datetime.now(timezone.utc).isoformat(),
                "human_approved": False,
            })
        # Detect a subset of high-risk, undeclared statements too.
        for field in ("voiceover", "on_screen_text"):
            copy = scene.get(field)
            if isinstance(copy, str) and any(re.search(p, copy, re.I) for p in RISKY_CLAIM_PATTERNS):
                if copy not in declared:
                    findings.append({
                        "scene_id": scene.get("id"), "claim": copy, "field": field,
                        "status": "BLOCKED_REVIEW_REQUIRED", "source": PENDING,
                        "checked_at": datetime.now(timezone.utc).isoformat(),
                        "human_approved": False,
                    })
    return findings


def register_asset(asset: dict) -> list[str]:
    if not isinstance(asset, dict):
        return ["Activo: se esperaba un objeto JSON"]
    errors: list[str] = []
    for key in ("asset_id", "kind", "source", "license", "permission_status"):
        if not _text(asset.get(key)):
            errors.append(f"Activo: falta {key}")
    if asset.get("permission_status") not in RIGHTS:
        errors.append("Activo bloqueado: permiso no confirmado")
    if asset.get("license") in ("unknown", "", None, PENDING):
        errors.append("Activo bloqueado: licencia desconocida")
    if not _finite_number(asset.get("cost_eur")) or asset.get("cost_eur") != 0:
        errors.append("Activo bloqueado: coste cero explícito obligatorio")
    return errors


def validate_audio_package(audio: dict) -> list[str]:
    if not isinstance(audio, dict):
        return ["Audio: se esperaba un objeto JSON"]
    errors: list[str] = []
    for key in ("voice", "music"):
        item = audio.get(key)
        if not isinstance(item, dict) or not _text(item.get("license")) or item.get("license") in ("unknown", PENDING) or item.get("permission_status") not in RIGHTS:
            errors.append(f"{key}: derechos/licencia no verificados")
    captions = audio.get("captions")
    if not isinstance(captions, dict) or not _text(captions.get("language")):
        errors.append("Subtítulos: idioma no indicado")
    if not isinstance(captions, dict) or captions.get("contrast_checked") is not True:
        errors.append("Subtítulos: contraste sin revisar")
    return errors


def qa_checklist(video: dict) -> dict:
    if not isinstance(video, dict):
        video = {}
    fields = {
        "duration_within_brief": "duration_ok",
        "aspect_ratio_matches": "aspect_ratio_ok",
        "brand_identity_checked": "brand_checked",
        "audio_levels_checked": "audio_checked",
        "captions_legible_and_synced": "captions_checked",
        "assets_rights_verified": "rights_checked",
        "claims_reviewed_by_human": "claims_human_approved",
        "privacy_reviewed": "privacy_checked",
        "human_final_approval": "final_human_approval",
    }
    checks = {label: video.get(field) is True for label, field in fields.items()}
    return {"checks": checks, "passed": all(checks.values()), "blocked": [k for k, v in checks.items() if not v]}


def build_review_package(project_dir: str | Path, output_zip: str | Path, files: list[str]) -> dict:
    """Make a review-only ZIP. Reject absolute/traversal, links and reserved names."""
    root = Path(project_dir).resolve()
    out = Path(output_zip).resolve()
    if not root.is_dir() or not isinstance(files, list) or not files:
        raise ValueError("Carpeta de proyecto o lista de archivos inválida")
    manifest = []
    checked = []
    seen: set[str] = set()
    for rel in files:
        if not isinstance(rel, str) or not rel or "\\" in rel:
            raise ValueError(f"Ruta inválida: {rel!r}")
        segments = rel.split("/")
        entry = PurePosixPath(rel)
        if entry.is_absolute() or any(s in ("", ".", "..") for s in segments):
            raise ValueError(f"Ruta no normalizada: {rel!r}")
        if rel == "REVIEW_MANIFEST.json" or rel in seen:
            raise ValueError(f"Nombre reservado o duplicado: {rel}")
        path = root.joinpath(*segments)
        if path.is_symlink() or not path.is_file() or root not in path.resolve().parents or path.resolve() == out:
            raise ValueError(f"Ruta fuera de proyecto, vínculo o archivo inexistente: {rel}")
        seen.add(rel)
        checked.append((rel, path))
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for rel, path in checked:
            data = path.read_bytes()
            archive.writestr(rel, data)
            manifest.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
        archive.writestr("REVIEW_MANIFEST.json", json.dumps({
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": manifest, "approval": "NOT_APPROVED_FOR_PUBLICATION",
        }, indent=2, ensure_ascii=False))
    return {"output": str(out), "files": len(manifest), "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}
