# Python Environment Management

Always use pixi for Python package management:
- Add packages: `pixi add <package>` (not pip install)
- Run commands: `pixi run <command>`
- Execute Python: `pixi run python <file.py>`
- Never use pip, conda, venv, or virtualenv directly

All dependencies must go through pixi to maintain pyproject.toml and pixi.lock.
