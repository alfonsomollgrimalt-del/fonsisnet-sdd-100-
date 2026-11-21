# FONSISNET SDD-100 — T11 preparación del repositorio independiente

Sistema **local, offline y sin dependencias externas** para preparar materiales de
vídeo/publicidad FONSISNET bajo Spec-Driven Development (SDD).

> **Entrega v0.3.1 / T11 — correcciones de seguridad, no desplegada.**
> Repo de destino verificado el 21-11-2026:
> `alfonsomollgrimalt-del/fonsisnet-sdd-100-` (**público**).
> La v0.3.0 se subió a `feature/t11-import-v0.3.0`. La v0.3.1 es una revisión de seguridad sobre esa rama; `main` no se fusiona.

## Ejecutar pruebas (Python 3.11+)

```bash
python scripts/validate_sdd.py
python -m unittest discover -s tests -v
python scripts/fonsisnet.py brief examples/brief.json
python scripts/fonsisnet.py script examples/script.json
python scripts/fonsisnet.py claims examples/script.json
# Para validar activos/audio, conservar las pruebas de derechos FUERA del repositorio público:
# python scripts/fonsisnet.py asset /ruta/activo.json --evidence-dir /ruta/privada/derechos
```

## Qué hace realmente
- Valida briefs y guiones temporizados; identifica ciertas afirmaciones de riesgo.
- Exige origen, licencia, permiso, coste 0 y comprobación de hash de evidencia documental local con aprobación humana para activos y audio. La revisión legal real sigue siendo humana.
- Verifica metadatos de voz/música/subtítulos y checklist de revisión humana.
- Genera paquetes ZIP marcados **no aprobados para publicación**: solo dentro del proyecto y sin sobrescribir destinos existentes.
- Documenta 100 agentes **lógicos**, no 100 procesos ni 100 modelos activos.

**No** genera vídeos automáticamente, no certifica cumplimiento tributario,
no determina la suficiencia jurídica de los documentos de derechos y no publica anuncios.

## Políticas
- Presupuesto máximo predeterminado: **0 €**; servicios de pago deshabilitados.
- Sin despliegue a producción; publicación y acceso a clientes requieren autorización humana.
- No inventar contacto, datos comerciales, ahorros fiscales, testimonios ni garantías.
- Ningún dato personal, credencial o secreto en repositorio, sobre todo por ser público.
- No tocar FONSISNET Network ni `inversion-market-radar`.

## Documentación
- `docs/SPEC.md`: especificación y exclusiones.
- `docs/PLAN.md`: arquitectura y secuencia SDD.
- `docs/TASKS.md`: tareas y dependencias.
- `docs/T11_HANDOFF.md`: instrucciones para incorporar el código a GitHub.
- `docs/QUALITY_GATES.md`: controles pendientes antes de una publicación.
- `.github/workflows/t11-ci.yml`: CI sin despliegues, solo PR o ejecución manual.

**T11: código en rama independiente; PR, CI remota y revisión humana pendientes.** **T12** sigue
bloqueada mientras no exista un Preview independiente autorizado.
