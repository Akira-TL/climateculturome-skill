from __future__ import annotations
from pathlib import Path
import hashlib, json, datetime as dt

def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def build_manifest(paths: list[str | Path]) -> dict:
    files = []
    for p0 in paths:
        p = Path(p0)
        files.append({
            "path": str(p),
            "sha256": sha256_file(p),
            "size_bytes": p.stat().st_size,
        })
    return {
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "files": files,
    }

def write_json(obj: dict, path: str | Path) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
