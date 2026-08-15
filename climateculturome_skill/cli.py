from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

from .governance import load_table, preflight
from .audit import determine_status, audit_flags
from .hypotheses import template_hypotheses
from .provenance import write_json

def load_request(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def cmd_preflight(args):
    req = load_request(args.request)
    meta = None
    summary = None
    if req.get("sample_metadata"):
        p = Path(req["sample_metadata"])
        if p.exists():
            meta = load_table(p)
    if req.get("microbiome_summary"):
        p = Path(req["microbiome_summary"])
        if p.exists():
            summary = load_table(p)
    result = preflight(
        metadata=meta,
        summary=summary,
        has_sample_level_matrix=bool(req.get("sample_level_feature_matrix")),
    )
    print(json.dumps({
        "errors": result.errors,
        "warnings": result.warnings,
        "capabilities": result.capabilities,
    }, ensure_ascii=False, indent=2))

def cmd_run(args):
    req = load_request(args.request)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    meta = None
    summary = None
    if req.get("sample_metadata") and Path(req["sample_metadata"]).exists():
        meta = load_table(req["sample_metadata"])
    if req.get("microbiome_summary") and Path(req["microbiome_summary"]).exists():
        summary = load_table(req["microbiome_summary"])

    pf = preflight(
        metadata=meta,
        summary=summary,
        has_sample_level_matrix=bool(req.get("sample_level_feature_matrix")),
    )
    status = determine_status(
        pf.errors,
        has_summary=summary is not None,
        has_sample_level_matrix=bool(req.get("sample_level_feature_matrix")),
    )

    write_json({
        "status": status,
        "errors": pf.errors,
        "warnings": pf.warnings,
        "capabilities": pf.capabilities,
        **audit_flags(),
    }, out/"audit.json")
    write_json({"hypotheses": template_hypotheses()}, out/"hypotheses.json")
    print(status)

def cmd_audit(args):
    p = Path(args.output)/"audit.json"
    if not p.exists():
        raise SystemExit("audit.json not found")
    print(p.read_text(encoding="utf-8"))

def main():
    ap = argparse.ArgumentParser(prog="climateculturome")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("preflight")
    p.add_argument("--request", required=True)
    p.set_defaults(func=cmd_preflight)

    p = sub.add_parser("run")
    p.add_argument("--request", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("audit")
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_audit)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
