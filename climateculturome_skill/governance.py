from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd

SUMMARY_REQUIRED = {
    "sample_type", "rank", "taxon", "mean_abundance", "prevalence"
}

SAMPLE_METADATA_MIN = {
    "sample_id", "dataset_id", "sample_type", "sampling_date"
}

INFERENTIAL_METHODS_REQUIRING_SAMPLE_LEVEL = {
    "alpha_diversity",
    "beta_diversity",
    "permanova",
    "permdisp",
    "ancom_bc",
    "lefse",
    "feast",
    "sourcetracker",
    "cooccurrence_network",
    "rda",
    "db_rda",
    "cca",
    "variance_partitioning",
    "mixed_model",
    "sem",
}

@dataclass
class PreflightResult:
    errors: list[str]
    warnings: list[str]
    capabilities: dict[str, bool]

def load_table(path: str | Path, sep: str | None = None) -> pd.DataFrame:
    p = Path(path)
    if sep is None:
        sep = "\t" if p.suffix.lower() in {".tsv", ".txt"} else ","
    return pd.read_csv(p, sep=sep)

def validate_summary(df: pd.DataFrame) -> list[str]:
    missing = SUMMARY_REQUIRED - set(df.columns)
    return [] if not missing else [
        f"summary missing columns: {sorted(missing)}"
    ]

def validate_sample_metadata(df: pd.DataFrame) -> list[str]:
    missing = SAMPLE_METADATA_MIN - set(df.columns)
    return [] if not missing else [
        f"sample metadata missing columns: {sorted(missing)}"
    ]

def detect_cross_design_collisions(metadata: pd.DataFrame) -> list[str]:
    """
    Detect same site_code appearing in multiple dataset_id values with
    different sampling dates. This is a generic anti-auto-merge guard.
    """
    required = {"dataset_id", "site_code", "sampling_date"}
    if not required.issubset(metadata.columns):
        return []
    warnings: list[str] = []
    x = metadata[list(required)].dropna().astype(str)
    for site, g in x.groupby("site_code"):
        if g["dataset_id"].nunique() > 1 and g["sampling_date"].nunique() > 1:
            warnings.append(
                f"site_code={site} appears across multiple designs/dates; "
                "do not auto-merge without an explicit linkage key"
            )
    return warnings

def real_coordinates_available(metadata: pd.DataFrame) -> bool:
    required = {"latitude", "longitude"}
    if not required.issubset(metadata.columns):
        return False
    coords = metadata[list(required)].apply(pd.to_numeric, errors="coerce")
    return bool(coords.notna().all(axis=1).any())

def inferential_allowed(has_sample_level_matrix: bool) -> bool:
    return bool(has_sample_level_matrix)

def preflight(
    metadata: pd.DataFrame | None = None,
    summary: pd.DataFrame | None = None,
    has_sample_level_matrix: bool = False,
) -> PreflightResult:
    errors: list[str] = []
    warnings: list[str] = []

    if metadata is not None:
        errors.extend(validate_sample_metadata(metadata))
        warnings.extend(detect_cross_design_collisions(metadata))

    if summary is not None:
        errors.extend(validate_summary(summary))

    coords = real_coordinates_available(metadata) if metadata is not None else False
    if metadata is not None and not coords:
        warnings.append(
            "no verified real coordinates available; point-level Earth-system "
            "matching must remain disabled"
        )

    return PreflightResult(
        errors=errors,
        warnings=warnings,
        capabilities={
            "point_environment_matching": coords,
            "sample_level_inference": bool(has_sample_level_matrix),
            "summary_descriptive_analysis": summary is not None and not validate_summary(summary),
        },
    )
