from pathlib import Path

FORBIDDEN_DIRS = {"evidence", "real_project", "example_output", "private_data", "raw_project_data"}
FORBIDDEN_EXTENSIONS = {".pdf", ".xlsx", ".xls"}

def test_no_real_project_artifact_directories():
    root = Path(__file__).resolve().parents[1]
    dirs = {p.name for p in root.rglob("*") if p.is_dir()}
    assert not (FORBIDDEN_DIRS & dirs)

def test_no_embedded_report_or_spreadsheet_files():
    root = Path(__file__).resolve().parents[1]
    embedded = [
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in FORBIDDEN_EXTENSIONS
    ]
    assert embedded == []
