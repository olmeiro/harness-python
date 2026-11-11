# harness-python

Plantilla de harness para proyectos Python trabajados con agentes (Claude Code):

- **Gate determinista** (`scripts/gate.py`): ruff, formato, mypy y pytest. Corre en local (hook `Stop`) y en CI (`.github/workflows/gate.yml`).
- **Hooks de Claude Code** (`.claude/`): bloquean comandos destructivos y el acceso a `.env*`, formatean cada edición y no dejan terminar con el gate en rojo.
- **Revisor independiente**: subagente `revisor` en local y `.github/workflows/revisor.yml` en cada PR. En CI, un filtro determinista bloquea los intentos de manipular la revisión; la Decisions API de Azure OpenAI responde preguntas de sí o no sobre cada `CA-N` de la spec y sobre riesgos fijos, y el código decide. Si algo falla, otro modelo explica por qué.
- **Specs SDD** (`specs/`): método, plantillas y la skill `/specs` para llenarlas.

## Empezar un proyecto

1. **Use this template** → crea el repo y clónalo fuera de carpetas sincronizadas (OneDrive, Dropbox): bloquean `.git`.
2. Entorno local:
   ```
   uv venv && .venv\Scripts\activate
   uv pip install -r requirements-dev.txt
   python scripts/gate.py
   ```
3. GitHub → **Settings → Secrets and variables → Actions**:
   - Secrets: `AZURE_OPENAI_EVALUATOR_ENDPOINT` (termina en `/openai/v1`) y `AZURE_OPENAI_EVALUATOR_API_KEY`.
   - Variables: `AZURE_OPENAI_EVALUATOR_DEPLOYMENT` (`gpt-6-luna`: el único modelo de la Decisions API) y, opcional, `AZURE_OPENAI_EVALUATOR_EXPLAINER_DEPLOYMENT` (p. ej. `gpt-5.2`) para explicar los fallos. Los dos deployments deben estar en el recurso del endpoint.
4. GitHub → **Settings → Rules → New branch ruleset** sobre la rama por defecto: *Restrict deletions*, *Block force pushes*, *Require a pull request* (0 aprobaciones si trabajas solo) y *Require status checks*: `gate` y `revisor`. Los checks aparecen en el buscador después de su primera ejecución: abre un PR de prueba y añádelos luego.
5. Rama `init/constitucion` → en Claude Code, `/specs init`. Completa también las secciones marcadas de `AGENTS.md`.
6. Cada feature: `/specs feature NN-nombre` → implementar → `/specs cerrar NN-nombre` → PR.

## Adaptar

- Qué revisa el gate: `pyproject.toml` (rutas de mypy y pytest, reglas de ruff). Al crear `src/`, añádelo a `[tool.mypy] files`.
- `scripts/`, `.claude/` y `.github/workflows/` son iguales en todos los proyectos: las mejoras se hacen aquí y se copian.
- Otro lenguaje: cambia la lista `CHECKS` de `scripts/gate.py`.

## Flujo de trabajo con Claude Code

El detalle está en `specs/orden_spec.md` §7. Las ramas las creas tú; la skill no hace commit ni push, propone el mensaje.

### Una vez por proyecto: Constitución

```
git checkout -b init/constitucion
```
```
/specs init
```
Responde los `PENDIENTE:` que deje en `mission`, `tech-stack`, `alcance-inicial` y `roadmap`, haz commit (`docs(specs): define la constitución`) y abre el PR.

### Cada feature

| Paso | Dónde | Comando |
|---|---|---|
| 1. Rama | terminal | `git checkout -b feature/NN-nombre` |
| 2. Spec | Claude | `/specs feature NN-nombre` → responde los `PENDIENTE:` → commit `docs(specs): define la spec de NN-nombre` |
| 3. Implementar | Claude | `Implementa specs/features/NN-nombre/ siguiendo plan.md` |
| 4. Gate | automático | el hook `Stop` lo ejecuta si hubo ediciones; a mano: `python scripts/gate.py` |
| 5. Revisión rápida (opcional) | Claude | `@agent-revisor valida specs/features/NN-nombre/` |
| 6. Cierre | Claude | `/specs cerrar NN-nombre`: gate, evidencia en `review.md`, revisor, roadmap, changelog y progress |
| 7. PR | terminal | `git push -u origin feature/NN-nombre` y abre el PR con una descripción |
| 8. CI | GitHub | `gate` y `revisor` (obligatorios). Con `revise`: corrige, haz push y se relanzan |
| 9. Merge | GitHub | con los dos checks en verde |

Revisor desde otra terminal, con contexto limpio: `claude -p --agent revisor "Valida specs/features/NN-nombre/"`.

### Veredictos

- `accept`: se cierra y se mergea.
- `revise`: se corrige y se vuelve a revisar; máximo 2 vueltas.
- `block`, o una tercera vuelta: para y decide la persona (falta información o un cambio de alcance).

### Entre features

- Cambios al roadmap o la Constitución: rama `replanning/tema` y copia `specs/replanning/_plantilla.md`.
- Al empezar cada sesión, Claude lee `specs/progress.md`, mira `git log` y ejecuta el gate antes de tocar nada (`AGENTS.md`).
