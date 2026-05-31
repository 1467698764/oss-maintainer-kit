import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def test_pyproject_declares_tomli_runtime_dependency_for_python_310() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8-sig"))

    dependencies = pyproject["project"].get("dependencies", [])

    assert 'tomli>=1.1.0; python_version < "3.11"' in dependencies
