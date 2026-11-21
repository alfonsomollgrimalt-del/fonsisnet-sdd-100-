# G2 — Backlog trazable

| ID | Tarea | Dependencia | Criterio de salida | Estado |
|---|---|---|---|---|
| T01 | Crear scaffold independiente | — | estructura y README | Hecho |
| T02 | Definir contratos JSON de brief y guion | T01 | esquemas versionados | Hecho — schemas/ |
| T03 | Implementar intake/brief | T02 | validación de campos | Hecho — core.py + ejemplo |
| T04 | Implementar guion/storyboard | T02 | escenas temporizadas | Hecho — core.py + ejemplo |
| T05 | Implementar verificador de afirmaciones | T04 | fuente/fecha o bloqueo | Hecho — sin aprobación automática |
| T06 | Registro de activos y licencias | T01 | activo trazable | Hecho — validación de licencia/permisos/coste |
| T07 | Pipeline de voz, música y subtítulos | T06 | derechos y sincronía | Hecho — controles de derechos/metadatos; render y sincronía real pendientes |
| T08 | QA audiovisual y de marca | T04,T07 | checklist aprobada | Hecho — checklist implementada; revisión audiovisual real pendiente |
| T09 | Empaquetado de revisión | T08 | evidencias y versión | Hecho — ZIP + SHA-256 + no aprobado |
| T10 | Pruebas de integración y seguridad | T02-T09 | suite aprobada | Hecho — pruebas locales |
| T11 | Incorporar código al repositorio independiente | T10 | commit de código + PR + CI verificables | Preparado localmente; repositorio accesible, pendiente incorporar y validar CI remota |
| T12 | Preview de validación | T11 | URL y build verificables | Bloqueado: requiere T11 aprobado y Preview independiente autorizado |
| T13 | Aprobación de publicación | T12 | aprobación humana expresa | No autorizado |

## Regla de estado
Una tarea solo pasa a «Hecho» cuando existe evidencia verificable (archivo, prueba, resultado o aprobación). No inferir completitud por planificación.
