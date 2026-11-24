# G0 — Especificación del producto

## Objetivo
Diseñar un flujo repetible y auditable para producir vídeos cortos y piezas publicitarias de FONSISNET, empezando por anuncios de asesoramiento fiscal/tributario para empresarios y pymes.

## Usuario y resultado
- Audiencia inicial: empresarios y responsables de pymes en España, con foco en Illes Balears.
- Resultado: guion, storyboard, recursos audiovisuales autorizados, montaje, subtítulos, controles de calidad y paquete listo para revisión.
- CTA inicial: «Contacta con FONSISNET».
- No se incorporarán teléfono, correo, dirección, web, tarifas ni promesas comerciales sin confirmación expresa.

## Alcance v0.1
Incluye:
- Brief y guion para anuncios de 15–30 segundos.
- Storyboard y lista de planos.
- Generación/selección de recursos audiovisuales mediante herramientas gratuitas disponibles.
- Voz, música y subtítulos con licencias verificables.
- Lista de comprobación legal, de marca, accesibilidad y calidad.
- Exportación de un paquete de revisión y registro de evidencias.

No incluye:
- Asesoramiento fiscal individual automatizado.
- Presentar declaraciones ni actuar ante organismos.
- Publicar anuncios, enviar mensajes o contactar clientes automáticamente.
- Comprar créditos, contratar planes o usar servicios de pago.
- Despliegue en producción sin autorización específica.

## Requisitos funcionales
- RF-01: capturar objetivo, audiencia, duración, formato y CTA.
- RF-02: generar guion con escenas temporizadas y locución.
- RF-03: marcar cada afirmación fiscal/legal con fuente y fecha o bloquearla como pendiente.
- RF-04: generar storyboard y lista de activos por escena.
- RF-05: registrar origen, licencia y permiso de cada activo.
- RF-06: producir subtítulos sincronizados y revisar legibilidad.
- RF-07: validar duración, relación de aspecto, audio y consistencia de marca.
- RF-08: entregar versión de revisión con checklist y evidencias.
- RF-09: exigir aprobación humana antes de publicar/exportar como final.
- RF-10: registrar fallos, decisiones, versiones y responsables.

## Requisitos no funcionales
- RNF-01: coste cero por defecto.
- RNF-02: trazabilidad de entradas, salidas y fuentes.
- RNF-03: privacidad: no subir datos personales de clientes a herramientas externas.
- RNF-04: accesibilidad: subtítulos legibles y contraste suficiente.
- RNF-05: portabilidad; el proyecto no dependerá de un proveedor concreto.
- RNF-06: separación estricta de otros repositorios/proyectos.

## Controles y bloqueos
- No inventar ahorros fiscales, porcentajes, resultados, testimonios o garantías.
- No afirmar «paga menos impuestos» como promesa garantizada; usar formulaciones prudentes y revisables.
- No usar logotipos, fotografías, música, voces o clips sin derechos/permiso comprobados.
- Si falta información, etiquetar `[PENDIENTE DE COMPROBAR]`.
- Si una herramienta exige pago o no muestra licencia clara, detener ese paso y proponer alternativa gratuita.
- Aprobación humana obligatoria de guion, afirmaciones, activos y pieza final.

## Criterios de aceptación G0
- Alcance y exclusiones documentados.
- Todos los requisitos tienen identificador.
- Riesgos y bloqueos explícitos.
- No se inventan datos de contacto ni datos comerciales.
