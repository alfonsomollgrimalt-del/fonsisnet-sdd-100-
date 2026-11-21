# G3 — Implementación T02–T10

Implementación local, modular y sin dependencias de terceros. Los contratos JSON viven en `schemas/`; la lógica reusable está en `src/fonsisnet_sdd/core.py`; el CLI en `scripts/fonsisnet.py`.

| Tarea | Entrega | Criterio verificable |
|---|---|---|
| T02 | `schemas/brief.schema.json`, `schemas/script.schema.json` | Contratos versionables y campos cerrados |
| T03 | `validate_brief` + `examples/brief.json` | Campos obligatorios, duración, formato y contacto confirmado |
| T04 | `validate_script` + `examples/script.json` | Escenas ordenadas, temporizadas y dentro de duración |
| T05 | `check_claims` | Afirmaciones con estado pendiente/bloqueado, fuente y fecha; no aprueba automáticamente |
| T06 | `register_asset` | Origen, licencia, permiso y coste cero obligatorios |
| T07 | `validate_audio_package` | Voz/música con derechos y subtítulos con idioma/contraste |
| T08 | `qa_checklist` | QA audiovisual, marca, accesibilidad, privacidad y aprobación humana |
| T09 | `build_review_package` | ZIP de revisión con SHA-256 por archivo y aprobación no concedida |
| T10 | `tests/test_pipeline.py` | Pruebas de integración y seguridad de rutas/afirmaciones/licencias |

## Limitaciones deliberadas
No se genera audio ni vídeo real, no se conecta a proveedores, no se suben archivos a servicios externos y no se publica. Esta entrega implementa y valida el flujo de preparación y control de calidad. La generación/edición audiovisual requiere un proveedor gratuito disponible y una revisión de sus términos antes de utilizarlo.
