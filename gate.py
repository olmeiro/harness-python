from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REQUIRED_PATHS = (
    Path(".claude/hooks/pre-task.sh"),
    Path(".claude/hooks/post-task.sh"),
    Path(".github/workflows/ci.yml"),
)


def validate_structure(repo_root: Path) -> list[str]:
    errors: list[str] = []

    for relative_path in REQUIRED_PATHS:
        if not (repo_root / relative_path).exists():
            errors.append(f"Missing required file: {relative_path}")

    spec_files = sorted(repo_root.glob("specs/**/spec.md"))
    if not spec_files:
        errors.append("Missing SDD spec: expected at least one specs/**/spec.md file")

    return errors


def run_tests(repo_root: Path) -> bool:
    tests_dir = repo_root / "tests"
    if not tests_dir.exists():
        print("No tests directory found; skipping tests.")
        return True

    command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]
    completed = subprocess.run(command, cwd=repo_root, check=False)
    return completed.returncode == 0


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Harness gate for Python projects with agents")
    parser.add_argument("--skip-tests", action="store_true", help="Skip unit tests")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parent),
        help="Repository root path",
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    errors = validate_structure(repo_root)

    if errors:
        for error in errors:
            print(error)
        return 1

    if not args.skip_tests and not run_tests(repo_root):
        return 1

    print("Gate checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
