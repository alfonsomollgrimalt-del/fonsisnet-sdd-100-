# FONSISNET SDD-100 — T11 preparación del repositorio independiente

Sistema **local, offline y sin dependencias externas** para preparar materiales de
vídeo/publicidad FONSISNET bajo Spec-Driven Development (SDD).

> **Entrega v0.3.0 / T11 — preparada para revisión, no desplegada.**
> Repo de destino verificado el 21-11-2026:
> `alfonsomollgrimalt-del/fonsisnet-sdd-100-` (**público**).
> Esta entrega no se ha subido automáticamente a GitHub.

## Ejecutar pruebas (Python 3.11+)

```bash
python scripts/validate_sdd.py
python -m unittest discover -s tests -v
python scripts/fonsisnet.py brief examples/brief.json
python scripts/fonsisnet.py script examples/script.json
python scripts/fonsisnet.py claims examples/script.json
```

## Qué hace realmente
- Valida briefs y guiones temporizados; identifica ciertas afirmaciones de riesgo.
- Exige origen, licencia, permiso y coste 0 explícito para activos.
- Verifica metadatos de voz/música/subtítulos y checklist de revisión humana.
- Genera paquetes ZIP marcados **no aprobados para publicación**.
- Documenta 100 agentes **lógicos**, no 100 procesos ni 100 modelos activos.

**No** genera vídeos automáticamente, no certifica cumplimiento tributario,
no comprueba derechos de materiales externos y no publica anuncios.

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

**T11 NO se marca completada** hasta verificar commit, PR y CI reales. **T12** sigue
bloqueada mientras no exista un Preview independiente autorizado.
