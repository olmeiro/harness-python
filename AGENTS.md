# AGENTS.md

<!-- IA: una o dos frases: qué es el proyecto y dónde vive el código. Sácalo de specs/mission.md y de la estructura del repo. -->

## Ejecutar

<!-- IA: comandos exactos para crear el entorno, instalar dependencias y ejecutar el proyecto. Solo lo verificado. -->

```
uv venv && .venv\Scripts\activate
uv pip install -r requirements-dev.txt   # incluye requirements.txt
python scripts/gate.py
```

## Arquitectura

<!-- IA: lo que un agente no deduce leyendo un solo archivo: capas, convenciones, decisiones transversales. Enlaza specs/decisions.md en lugar de repetirlo. -->

## Variables de entorno

`.env` está en `.gitignore`; `.env.template` sí se versiona. Los agentes no pueden leer ni editar ningún `.env*`, tampoco el template: al introducir una variable nueva, pide a la persona que la añada a `.env.template`.

## Definición de terminado

1. `python scripts/gate.py` en verde (lint, formato, tipos y tests). Si falla, corrige y repite.
2. Revisión independiente (otro agente o una persona) contra la spec de la feature (`specs/features/NN-nombre/`) o, si no hay feature, contra lo pedido, con el diff y la salida del gate. Responde `accept`, `revise` o `block`. Solo `accept` cierra la tarea; `revise` admite 2 vueltas; con `block` o a la tercera vuelta, para y pregunta.
3. Reporta las comprobaciones ejecutadas y su resultado.

## Specs y continuidad

- Método SDD en `specs/orden_spec.md`; cada feature vive en `specs/features/NN-nombre/`, copiada de `_plantilla/`.
- Al empezar una sesión: lee `specs/progress.md`, mira `git log --oneline -10` y ejecuta el gate antes de tocar nada. Al terminar, actualiza `specs/progress.md`.
- Lo terminado lo registra git. Un error que se repite se convierte en una línea de este archivo, en una skill o, si puede costar datos, dinero o seguridad, en un hook o una regla del gate (`specs/orden_spec.md` §8).

## Harness

- Qué revisa el gate (rutas, reglas, umbrales) está en `pyproject.toml`. `scripts/`, `.claude/` y `.github/workflows/` se copian igual a otros proyectos.
- Dependencias: `requirements.txt` para ejecutar y `requirements-dev.txt` (la incluye) para el gate.
- `tests/test_harness.py` prueba que los hooks bloquean lo que prometen.
- Commits y push los hace la persona. No los ejecutes si no te lo pidió para ese cambio: prepara los archivos y propón el mensaje. Si lo intentas, las reglas `ask` de `settings.json` le piden confirmación también en modo auto ([permisos de Claude Code](https://code.claude.com/docs/en/permissions); comprobado en la práctica el 2026-11-11), y `validar_comando.py` cubre las variantes que esas reglas no ven.
- En cada PR, `.github/workflows/revisor.yml` ejecuta `scripts/revisor_ci.py`. Primero un filtro determinista rechaza el título, la descripción o los `CA-N` que intentan dirigir la revisión (órdenes al revisor, comentarios HTML, caracteres invisibles). Después la Decisions API de Azure OpenAI (deployment `gpt-6-luna`) responde preguntas de sí o no: una por cada `CA-N` de la spec más si respeta el «No tocar» de `plan.md` y si `review.md` tiene la evidencia de `validation.md` (o una sobre lo pedido, si no hay feature), y una por cada riesgo fijo. La feature se detecta por los archivos de `specs/features/` que toca el PR o por su rama `feature/NN-nombre`. El código decide con un umbral, así que los detalles de estilo no tumban un PR. Si algo falla y está definida `AZURE_OPENAI_EVALUATOR_EXPLAINER_DEPLOYMENT` (p. ej. `gpt-5.2`), ese modelo explica en el Summary por qué falló cada pregunta, sin cambiar la decisión. Variables: `AZURE_OPENAI_EVALUATOR_*` (endpoint y clave como *secrets*, deployments como *variables* del repo). Corre con `pull_request_target`, así que workflow y revisor salen siempre de `main`; por eso nunca debe ejecutar código del PR, solo leerlo con git. Solo es obligatorio si `gate` y `revisor` son *required checks* de `main` (Settings → Rules).
