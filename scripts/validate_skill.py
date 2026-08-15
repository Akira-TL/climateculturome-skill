from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "skill.json",
    "LICENSE",
    "pyproject.toml",
    ".gitignore",
    "workflows/01_data_intake_and_governance.md",
    "references/evidence_grading.md",
]
FORBIDDEN_DIRS = {
    "evidence",
    "real_project",
    "example_output",
    "private_data",
    "raw_project_data",
}
FORBIDDEN_EXTENSIONS = {
    ".pdf",
    ".xlsx",
    ".xls",
    ".qza",
    ".qzv",
    ".biom",
    ".parquet",
    ".sqlite",
    ".db",
}
EXCLUDED_SCAN_DIRS = {
    ".git",
    ".venv",
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
}


def source_paths():
    for path in ROOT.rglob("*"):
        relative_parts = path.relative_to(ROOT).parts
        if any(part in EXCLUDED_SCAN_DIRS or part.endswith(".egg-info") for part in relative_parts):
            continue
        yield path


for rel in REQUIRED_FILES:
    assert (ROOT / rel).is_file(), f"missing required file: {rel}"

present_forbidden_dirs = {
    p.name for p in source_paths() if p.is_dir() and p.name in FORBIDDEN_DIRS
}
assert not present_forbidden_dirs, (
    f"forbidden project-data directories exist: {sorted(present_forbidden_dirs)}"
)

embedded_artifacts = [
    p.relative_to(ROOT).as_posix()
    for p in source_paths()
    if p.is_file() and p.suffix.lower() in FORBIDDEN_EXTENSIONS
]
assert not embedded_artifacts, f"forbidden embedded artifacts: {embedded_artifacts}"

skill_meta = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
request_schema = json.loads(
    (ROOT / "data_templates/request.schema.json").read_text(encoding="utf-8")
)
assert skill_meta["entrypoint"] == "SKILL.md"
assert skill_meta["data_policy"]["embedded_project_data"] is False
assert manifest["contains_real_project_data"] is False
assert manifest["contains_personal_information"] is False
assert request_schema["type"] == "object"

for case_path in sorted((ROOT / "examples").rglob("case.json")):
    case = json.loads(case_path.read_text(encoding="utf-8"))
    assert case.get("synthetic") is True, (
        f"example must be explicitly synthetic: {case_path.relative_to(ROOT)}"
    )

license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
assert "Permission is hereby granted" in license_text, "LICENSE is not a complete MIT license"

print("PURE_SKILL_VALIDATION_OK")
