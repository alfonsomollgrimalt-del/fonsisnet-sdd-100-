#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def require(path):
    if not (ROOT / path).is_file():
        errors.append(f"Falta archivo: {path}")

for p in ["README.md", "docs/SPEC.md", "docs/PLAN.md", "docs/TASKS.md",
          "docs/QUALITY_GATES.md", "docs/DECISIONS.md", "config/policy.json",
          "config/agents.json"]:
    require(p)

try:
    policy = json.loads((ROOT / "config/policy.json").read_text(encoding="utf-8"))
    if policy.get("default_budget_eur") != 0: errors.append("El presupuesto por defecto debe ser 0.")
    if policy.get("production_deploy_allowed") is not False: errors.append("Producción debe permanecer bloqueada.")
    if policy.get("human_approval_required") is not True: errors.append("Debe exigirse aprobación humana.")
except Exception as e:
    errors.append(f"policy.json inválido: {e}")

try:
    agents = json.loads((ROOT / "config/agents.json").read_text(encoding="utf-8"))
    rows = agents["agents"]
    if len(rows) != 100: errors.append(f"Se esperaban 100 agentes lógicos; encontrados {len(rows)}.")
    ids = [a["id"] for a in rows]
    if len(set(ids)) != 100: errors.append("IDs de agentes duplicados.")
    if sum(a["role"] == "director" for a in rows) != 1: errors.append("Debe existir 1 director.")
    if sum(a["role"] == "coordinator" for a in rows) != 9: errors.append("Deben existir 9 coordinadores.")
    if sum(a["role"] == "specialist" for a in rows) != 90: errors.append("Deben existir 90 especialistas.")
except Exception as e:
    errors.append(f"agents.json inválido: {e}")

if errors:
    print("VALIDACIÓN FALLIDA")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)

print("VALIDACIÓN SDD CORRECTA")
print("- Estructura documental presente")
print("- Política de coste cero y producción bloqueada")
print("- 100 agentes lógicos: 1 director + 9 coordinadores + 90 especialistas")
