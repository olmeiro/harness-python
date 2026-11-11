import tempfile
import unittest
from pathlib import Path

import gate


class GateTests(unittest.TestCase):
    def _write(self, root: Path, relative: str, content: str = "ok") -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_validate_structure_success(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            self._write(root, ".claude/hooks/pre-task.sh")
            self._write(root, ".claude/hooks/post-task.sh")
            self._write(root, ".github/workflows/ci.yml")
            self._write(root, "specs/001-harness-python-sdd/spec.md")

            self.assertEqual(gate.validate_structure(root), [])

    def test_validate_structure_missing_spec(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            self._write(root, ".claude/hooks/pre-task.sh")
            self._write(root, ".claude/hooks/post-task.sh")
            self._write(root, ".github/workflows/ci.yml")

            errors = gate.validate_structure(root)
            self.assertIn(
                "Missing SDD spec: expected at least one specs/**/spec.md file",
                errors,
            )

    def test_run_skip_tests_success(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            self._write(root, ".claude/hooks/pre-task.sh")
            self._write(root, ".claude/hooks/post-task.sh")
            self._write(root, ".github/workflows/ci.yml")
            self._write(root, "specs/001-harness-python-sdd/spec.md")

            exit_code = gate.run(["--skip-tests", "--repo-root", str(root)])
            self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
