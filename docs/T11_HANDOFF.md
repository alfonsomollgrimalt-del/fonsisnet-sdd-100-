# T11 — Entrega revisable para repositorio independiente

**Fecha:** 21-11-2026. **Estado:** v0.3.0 subida a rama independiente; v0.3.1 refuerzo de seguridad; SIN MERGE A MAIN; SIN CI REMOTA VERIFICADA.

## Destino confirmado en GitHub
- `https://github.com/alfonsomollgrimalt-del/fonsisnet-sdd-100-`
- Rama predeterminada actual: `main`.
- Rama de revisión observada: `reportaje/t11-t12-review` (no confundir con `feature/t11-t12-review`).
- Visibilidad observada: **público**. No subir secretos, datos personales ni material propietario.
- El código T11 v0.3.0 quedó en `feature/t11-import-v0.3.0` (commit `5bda4ca63055c5e529aef393d6de824137332340`). No existe aprobación para fusionar `main`.

## Contenido preparado
- `src/`: comprobaciones locales de brief, guion, afirmaciones, activos, audio y QA.
- `config/`: 100 agentes lógicos; presupuesto 0 €, ejecución real y publicación bloqueadas.
- `schemas/`: contratos JSON documentados.
- `tests/`: suite local y nuevas pruebas negativas de seguridad.
- `.github/workflows/t11-ci.yml`: CI de solo lectura, en PR o inicio manual; el job se omite si el repositorio es privado.
- `.github/pull_request_template.md`: checklist para revisión humana.
- `docs/`: SPEC, PLAN, TASKS, puertas de calidad, decisiones y evidencias.
- `scripts/`: comandos offline; no crean proyectos remotos.

## Para concluir T11
1. Confirmar el commit de seguridad en `feature/t11-import-v0.3.0`; no tocar `main`.
2. Ejecutar localmente `python scripts/validate_sdd.py` y `python -m unittest discover -s tests -v`.
3. Registrar hashes y revisión de seguridad. No ejecutar GitHub Actions sin verificar previamente cuotas y costes.
4. Si se autoriza posteriormente, revisar PR y CI real; T11 no se cierra sin evidencia remota y humana.

## No incluido / límites
- Sin renderizado audiovisual, sin herramientas de pago, sin publicación, sin despliegue Vercel.
- La validación por patrones no sustituye revisión fiscal/jurídica de **todo** el texto.
- T12 requiere proyecto Preview **nuevo** e independiente y autorización específica; no reutilizar `inversion-market-radar`.
- No se garantiza una ejecución gratuita si se cambian los ajustes de GitHub, visibilidad o plan; verificar el uso antes de correr CI remota.

## Endurecimiento v0.3.1
- El gasto 0 € se exige también a voz y música; no admite ausencias, booleanos ni valores no finitos.
- Cada activo y audio exige evidencia local accesible, huella SHA-256, titular, revisor, fecha y consentimiento humano explícito. Un documento comprobado por hash **no garantiza validez jurídica**. Guardar esos documentos fuera del repo público.
- El ZIP de revisión requiere directorio existente dentro del proyecto y apertura exclusiva (`xb`); nunca sobrescribe.
- Guiones con inicio posterior a 0, huecos o final antes de duración quedan rechazados.
- CI con acciones fijadas a commits verificados, solo permisos de lectura y sin ejecución remota iniciada.
