# Spec: Harness Python con agentes

## Objetivo
Definir un harness mínimo para proyectos Python con agentes que incluya gate, hooks de Claude Code, revisor independiente en CI y especificaciones SDD.

## Requisitos
1. Existirá un comando `python gate.py` que valide la estructura del harness y ejecute pruebas unitarias.
2. Existirán hooks de Claude Code pre y post tarea que ejecuten el gate.
3. Existirá un workflow de CI con un job de gate y un job de revisor independiente para pull requests.
4. Existirá al menos una spec SDD en `specs/**/spec.md`.

## Criterios de aceptación
- `python gate.py --skip-tests` pasa cuando los archivos obligatorios existen.
- `python -m unittest discover -s tests -p "test_*.py"` valida el comportamiento mínimo del gate.
- En pull requests, CI ejecuta tanto `gate` como `independent-reviewer`.
