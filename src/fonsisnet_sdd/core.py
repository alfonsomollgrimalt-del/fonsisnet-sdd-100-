"""Local, offline checks for the FONSISNET SDD-100 video review workflow.

No network requests, credential handling, paid APIs, publication or deployment.
Passing these checks does NOT authorize use of unverified assets or legal claims.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import math
import re
import zipfile
from datetime import date, datetime, timezone
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
    # No empty lead-in, interior gaps or uncovered ending; tiny float drift tolerated.
    tolerance = 1e-6
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
            if start < prev_end - tolerance:
                errors.append(f"Escena {index}: solapamiento o desorden")
            elif start > prev_end + tolerance:
                errors.append(f"Escena {index}: hueco sin cubrir en la línea de tiempo")
            if end > duration + tolerance:
                errors.append(f"Escena {index}: excede duración total")
            prev_end = end
        claims = scene.get("claims")
        if not isinstance(claims, list) or not all(_text(c) for c in claims):
            errors.append(f"Escena {index}: claims debe ser una lista de texto")
    if scenes and not math.isclose(prev_end, duration, abs_tol=tolerance):
        errors.append("El guion no cubre el final de la duración declarada")
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


def _validate_rights_evidence(asset: dict, evidence_root: str | Path | None) -> list[str]:
    """Verify presence/integrity of a LOCAL rights document, not legal sufficiency.

    A caller-supplied approval is an attestation, not independent proof. Never
    auto-approve a missing document; evidence belongs outside this public repo.
    """
    evidence = asset.get("rights_evidence")
    if not isinstance(evidence, dict):
        return ["Derechos: falta rights_evidence con prueba documental y revisión humana"]
    errors: list[str] = []
    for field in ("file", "sha256", "rights_holder", "reviewed_by", "reviewed_at"):
        if not _text(evidence.get(field)) or evidence.get(field) == PENDING:
            errors.append(f"Derechos: falta {field}")
    if evidence.get("human_approved") is not True:
        errors.append("Derechos: falta aprobación humana explícita")
    reviewed_at = evidence.get("reviewed_at")
    if _text(reviewed_at) and reviewed_at != PENDING:
        try:
            when = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
            if when.tzinfo is None or when.utcoffset() is None:
                raise ValueError("zona horaria ausente")
            if when > datetime.now(timezone.utc).astimezone(when.tzinfo):
                raise ValueError("fecha futura")
        except (ValueError, TypeError, OverflowError):
            errors.append("Derechos: reviewed_at debe ser fecha ISO-8601 con zona horaria, no futura")
    valid_until = evidence.get("valid_until")
    if valid_until is not None:
        try:
            if not isinstance(valid_until, str) or date.fromisoformat(valid_until) < datetime.now(timezone.utc).date():
                raise ValueError("caducado")
        except (ValueError, TypeError):
            errors.append("Derechos: permiso caducado o valid_until inválido")
    if evidence_root is None:
        errors.append("Derechos: indicar directorio local de evidencias; no se verifican declaraciones sin archivo")
        return errors
    rel = evidence.get("file")
    if not _text(rel) or rel == PENDING:
        return errors
    if "\\" in rel or PurePosixPath(rel).is_absolute() or any(seg in ("", ".", "..") for seg in rel.split("/")):
        errors.append("Derechos: ruta documental inválida o insegura")
        return errors
    try:
        root = Path(evidence_root).resolve(strict=True)
        candidate = root.joinpath(*rel.split("/"))
        resolved = candidate.resolve(strict=True)
        if not root.is_dir() or not resolved.is_relative_to(root) or not candidate.is_file():
            raise ValueError("evidencia fuera del directorio permitido")
        # No links anywhere between the evidence root and the file.
        cursor = root
        for segment in rel.split("/"):
            cursor = cursor / segment
            if cursor.is_symlink():
                raise ValueError("evidencia mediante enlace simbólico")
        if resolved.stat().st_size == 0 or resolved.stat().st_size > 10 * 1024 * 1024:
            raise ValueError("evidencia vacía o demasiado grande")
        expected = evidence.get("sha256")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
            raise ValueError("SHA-256 documental inválido")
        digest = hashlib.sha256()
        total = 0
        with candidate.open("rb") as src:
            for chunk in iter(lambda: src.read(65536), b""):
                total += len(chunk)
                if total > 10 * 1024 * 1024:
                    raise ValueError("evidencia demasiado grande")
                digest.update(chunk)
        if not hmac.compare_digest(digest.hexdigest(), expected.lower()):
            raise ValueError("SHA-256 documental distinto del archivo")
    except (OSError, ValueError, RuntimeError) as exc:
        errors.append(f"Derechos: evidencia documental no válida ({exc})")
    return errors


def register_asset(asset: dict, evidence_root: str | Path | None = None) -> list[str]:
    if not isinstance(asset, dict):
        return ["Activo: se esperaba un objeto JSON"]
    errors: list[str] = []
    for key in ("asset_id", "kind", "source", "license", "permission_status"):
        if not _text(asset.get(key)) or asset.get(key) == PENDING:
            errors.append(f"Activo: falta {key}")
    if not isinstance(asset.get("permission_status"), str) or asset.get("permission_status") not in RIGHTS:
        errors.append("Activo bloqueado: permiso no confirmado")
    if isinstance(asset.get("license"), str) and asset["license"].strip().casefold() in (
        "unknown", "claimed by user", "unverified", "pending", "desconocida"
    ):
        errors.append("Activo bloqueado: licencia no acreditada")
    if not _finite_number(asset.get("cost_eur")) or asset.get("cost_eur") != 0:
        errors.append("Activo bloqueado: coste cero explícito obligatorio")
    errors.extend(_validate_rights_evidence(asset, evidence_root))
    return errors


def validate_audio_package(audio: dict, evidence_root: str | Path | None = None) -> list[str]:
    if not isinstance(audio, dict):
        return ["Audio: se esperaba un objeto JSON"]
    errors: list[str] = []
    for key in ("voice", "music"):
        item = audio.get(key)
        if not isinstance(item, dict):
            errors.append(f"{key}: se esperaba un activo con derechos y coste cero")
            continue
        errors.extend(f"{key}: {problem}" for problem in register_asset(item, evidence_root))
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
    """Create a review-only ZIP *inside* project, never replace an existing file.

    The destination directory must already exist. Opening with ``xb`` is
    exclusive: symlinks/existing files cannot be overwritten accidentally.
    """
    root = Path(project_dir).resolve(strict=True)
    output_path = Path(output_zip).absolute()
    out = output_path.resolve(strict=False)
    if not root.is_dir() or not isinstance(files, list) or not files:
        raise ValueError("Carpeta de proyecto o lista de archivos inválida")
    if (out == root or not out.is_relative_to(root) or
            not output_path.parent.is_dir() or not output_path.name.endswith(".zip")):
        raise ValueError("El ZIP debe generarse en una carpeta existente dentro del proyecto")
    if output_path.is_symlink():
        raise ValueError("No se permite ZIP de salida mediante enlace simbólico")
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
    created = False
    try:
        with output_path.open("xb") as destination:
            created = True
            with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for rel, path in checked:
                    data = path.read_bytes()
                    archive.writestr(rel, data)
                    manifest.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
                archive.writestr("REVIEW_MANIFEST.json", json.dumps({
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "files": manifest, "approval": "NOT_APPROVED_FOR_PUBLICATION",
                }, indent=2, ensure_ascii=False))
    except Exception:
        if created:
            output_path.unlink(missing_ok=True)
        raise
    return {"output": str(out), "files": len(manifest), "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}
