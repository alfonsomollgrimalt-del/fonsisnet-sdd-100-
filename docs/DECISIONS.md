# Registro de decisiones

| ID | Decisión | Motivo | Estado |
|---|---|---|---|
| ADR-001 | Proyecto independiente | Evitar interferencia con otros proyectos | Aprobada |
| ADR-002 | 100 agentes lógicos: 1 director + 9 coordinadores + 90 especialistas | Coordinación modular y escalable | Aprobada |
| ADR-003 | Ejecución bajo demanda, no 100 modelos simultáneos | Control de costes y realismo operativo | Aprobada |
| ADR-004 | Presupuesto cero por defecto | No incurrir en gastos sin autorización | Aprobada |
| ADR-005 | Sin despliegue de producción | Requiere autorización separada | Aprobada |
| ADR-006 | Repositorio independiente público confirmado | Existe `alfonsomollgrimalt-del/fonsisnet-sdd-100-`; no se ha subido código en esta entrega | Verificado 21-11-2026 |


## 2026-11-11 — Implementación T02–T10
- Se elige Python estándar sin dependencias externas para mantener coste cero y portabilidad.
- Los módulos de vídeo/audio se limitan a validación y trazabilidad; no simulan generación ni exportación audiovisual.
- Los datos de contacto no confirmados y afirmaciones fiscales de riesgo bloquean la aprobación.
- El ZIP de revisión se marca siempre como no aprobado para publicación.

## 2026-11-21 — Preparación T11
- Se aprovecha el scaffold v0.2.0 y se prepara la entrega local v0.3.0.
- CI de solo lectura; nunca desplegar ni publicar desde el workflow.
- El repositorio GitHub confirmado es público; no publicar secretos, datos personales ni licencias no revisadas.
- No se crea commit remoto, PR o Preview automáticamente durante la preparación.
