$ErrorActionPreference = "Stop"
uv run python scripts/validate_skill.py
uv run pytest -q
