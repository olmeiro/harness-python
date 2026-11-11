# harness-python

Harness mínimo para proyectos Python con agentes.

## Componentes
- **Gate**: `python gate.py`
- **Hooks de Claude Code**: `.claude/hooks/pre-task.sh` y `.claude/hooks/post-task.sh`
- **Revisor independiente en CI**: job `independent-reviewer` en `.github/workflows/ci.yml`
- **Specs SDD**: `specs/001-harness-python-sdd/spec.md`

## Uso rápido
```bash
python gate.py
```

Para validar solo estructura (sin tests):
```bash
python gate.py --skip-tests
```
