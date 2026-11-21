# T11 — Entrega revisable para repositorio independiente

**Fecha:** 21-11-2026. **Estado:** PREPARADA LOCALMENTE; SIN COMMIT REMOTO; SIN CI REMOTA VERIFICADA.

## Destino confirmado en GitHub (solo lectura)
- `https://github.com/alfonsomollgrimalt-del/fonsisnet-sdd-100-`
- Rama predeterminada actual: `main`.
- Rama de revisión observada: `reportaje/t11-t12-review` (no confundir con `feature/t11-t12-review`).
- Visibilidad observada: **público**. No subir secretos, datos personales ni material propietario.
- En la auditoría del 21-11-2026 solo se verificó `README.md` en `main` y rama de revisión.

## Contenido preparado
- `src/`: comprobaciones locales de brief, guion, afirmaciones, activos, audio y QA.
- `config/`: 100 agentes lógicos; presupuesto 0 €, ejecución real y publicación bloqueadas.
- `schemas/`: contratos JSON documentados.
- `tests/`: suite local y nuevas pruebas negativas de seguridad.
- `.github/workflows/t11-ci.yml`: CI de solo lectura, en PR o inicio manual; el job se omite si el repositorio es privado.
- `.github/pull_request_template.md`: checklist para revisión humana.
- `docs/`: SPEC, PLAN, TASKS, puertas de calidad, decisiones y evidencias.
- `scripts/`: comandos offline; no crean proyectos remotos.

## Antes de incorporar
1. Confirmar que se ha elegido **este** repositorio independiente y que su visibilidad pública es adecuada.
2. Crear una rama nueva desde `main`, por ejemplo `feature/t11-import-v0.3.0`.
3. Copiar los archivos al árbol de esa rama; no fusionar sin revisión.
4. Ejecutar localmente `python scripts/validate_sdd.py` y `python -m unittest discover -s tests -v`.
5. Crear una PR a `main` y comprobar el resultado real de la CI, el diff, los permisos y la ausencia de secretos.
6. Marcar T11 completada solo después de un commit remoto verificable y CI real aprobada.

## No incluido / límites
- Sin renderizado audiovisual, sin herramientas de pago, sin publicación, sin despliegue Vercel.
- La validación por patrones no sustituye revisión fiscal/jurídica de **todo** el texto.
- T12 requiere proyecto Preview **nuevo** e independiente y autorización específica; no reutilizar `inversion-market-radar`.
- No se garantiza una ejecución gratuita si se cambian los ajustes de GitHub, visibilidad o plan; verificar el uso antes de correr CI remota.
