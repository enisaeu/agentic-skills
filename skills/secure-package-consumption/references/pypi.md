---
name: secure-package-consumption-pypi
description: Routing reference for Python package-manager-specific files.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [pip, poetry, pipenv, uv]
  ecosystems: [python, pypi]
---

# PyPI and Python Packaging

Use an exact manager reference instead of this router when possible:

- `pip.md` for requirements files, constraints, direct pip use, or setup metadata without a higher-level manager.
- `poetry.md` for `pyproject.toml` plus `poetry.lock`.
- `pipenv.md` for `Pipfile` plus `Pipfile.lock`.
- `uv.md` for `uv.lock`, uv project commands, or uv pip workflows.

If multiple managers are present, treat that as a control issue. Load the exact reference for the manager that owns the lockfile, preserve the existing workflow, and avoid switching managers unless the user requested it.
