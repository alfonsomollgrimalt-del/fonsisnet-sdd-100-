# Puertas de calidad

- G0 Spec: alcance, requisitos, exclusiones y riesgos completos.
- G1 Plan: arquitectura, dependencias y estrategia de pruebas.
- G2 Tasks: tareas con criterios de salida y estados trazables.
- G3 Implementación: código/configuración revisados y reproducibles.
- G4 Validación:
  - [x] pruebas automáticas locales aprobadas (consultar informe T11 para cifra de esta entrega)
  - [ ] afirmaciones fiscales/jurídicas verificadas
  - [ ] activos y licencias comprobados
  - [ ] subtítulos, audio, duración y formato revisados
  - [ ] coste total = 0 € o gasto expresamente autorizado
  - [ ] datos personales y secretos ausentes
  - [ ] aprobación humana registrada
- G5 Release:
  - [ ] paquete final versionado
  - [ ] Preview validado si existe infraestructura
  - [ ] publicación aprobada expresamente
  - [ ] producción sigue bloqueada salvo autorización separada

Cualquier fallo crítico bloquea la fase siguiente.

## Evidencia de G3/G4 (11-11-2026)
- T02: dos esquemas JSON Draft 2020-12.
- T03–T09: funciones locales documentadas en `docs/IMPLEMENTATION.md`.
- T10: `tests/test_pipeline.py`, incluidas pruebas de bloqueo de afirmaciones, contacto sin confirmar, derechos, coste, QA y traversal de rutas.
- Los controles no sustituyen revisión jurídica, revisión de marca ni prueba audiovisual real.
- Publicación y producción permanecen bloqueadas.

## Estado de puerta G4

La suite de software está aprobada. La puerta G4 global sigue **abierta/bloqueada** hasta disponer de activos audiovisuales concretos, verificar sus licencias, revisar audio/subtítulos, comprobar afirmaciones y registrar aprobación humana.

## T11 — Revisión de importación
- [x] Commit fuente incorporado al repositorio independiente (rama de T11, no `main`).
- [ ] Revisión de PR y diferencia con `main`.
- [ ] CI del commit remoto aprobada, sin despliegue ni gastos (no ejecutada).
- [ ] Material del repositorio público revisado para ausencia de datos sensibles.

## Requisitos de la versión v0.3.1
- [x] Control explícito de coste de activos, voz y música (tests locales).
- [x] Documentación verificable por archivo+SHA-256 y atestación humana (sin certificar licencias de terceros).
- [x] Creación de ZIP sin sobrescritura y dentro del proyecto (tests locales).
- [x] Cobertura continua de escenas (tests locales).
- [x] Actions de CI fijadas a SHAs inmutables (refs oficiales verificadas el 21-11-2026).
- [ ] Revisión humana real del expediente de cada material concreto.
- [ ] CI remota aprobada cuando el presupuesto 0 € pueda garantizarse.
