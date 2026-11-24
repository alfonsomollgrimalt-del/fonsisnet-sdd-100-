# G1 — Plan de implementación

## Arquitectura
Pipeline modular y agnóstico del proveedor:
1. Intake/Brief
2. Strategy & Script
3. Fact/Legal Review
4. Storyboard
5. Asset Sourcing/Generation
6. Voice & Audio
7. Edit & Captions
8. Brand/Accessibility QA
9. Final Review & Release Package

Cada módulo recibe un contrato de entrada/salida documentado. Los agentes son unidades lógicas coordinadas; se activan bajo demanda y no representan procesos/modelos simultáneos.

## Fases SDD
- G0 Spec: especificación y límites.
- G1 Plan: arquitectura, riesgos y estrategia de pruebas.
- G2 Tasks: tareas trazables y dependencias.
- G3 Implementación: construir módulos y conectores gratuitos.
- G4 Validación: pruebas funcionales, legales, visuales y de coste.
- G5 Release: paquete aprobado; Preview solo tras disponer de repositorio y autorización de entorno. Producción requiere autorización independiente.

## Plan por incrementos
- I0: scaffold, contratos, manifiesto de agentes y validadores.
- I1: brief, guion, storyboard y control de afirmaciones.
- I2: gestión de activos, licencias, voz, música y subtítulos.
- I3: ensamblado/exportación y QA audiovisual.
- I4: interfaz de revisión, evidencias y empaquetado.
- I5: integración Git/Preview, pruebas de aceptación y documentación operativa.

## Estrategia de pruebas
- Unitarias: esquemas, validadores y políticas.
- Integración: contratos entre etapas.
- Regresión: guion/activos/subtítulos/exportación.
- Seguridad/privacidad: detección de datos personales y secretos.
- Coste: bloquear cualquier operación de pago por defecto.
- Revisión humana: checklist obligatoria antes de release.

## Riesgos
- Disponibilidad regional/cambios en planes gratuitos.
- Restricciones de licencia o marcas de agua.
- Errores en afirmaciones fiscales o legales.
- Desincronización de audio/subtítulos.
- Filtración de datos personales.
- GitHub accesible; el repositorio independiente público aún no contiene el código de esta entrega.

## Fuera de alcance operativo actual
No crear proyecto Vercel, no desplegar Preview y no tocar producción sin una autorización posterior específica. El repositorio independiente existe, pero T11 aún requiere carga del código, revisión y CI.
