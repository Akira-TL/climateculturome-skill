#!/usr/bin/env bash
set -euo pipefail

uv run python scripts/validate_skill.py
uv run pytest -q
