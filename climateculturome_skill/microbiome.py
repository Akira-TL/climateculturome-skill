from __future__ import annotations
import pandas as pd

DEFAULT_EXCLUDE_TAXA = {"Other", "Unclassified", "Incertae_Sedis", "Unknown"}

def top_taxa(
    summary: pd.DataFrame,
    sample_type: str | None = None,
    rank: str = "genus",
    n: int = 20,
    exclude_taxa: set[str] | None = None,
) -> pd.DataFrame:
    exclude_taxa = exclude_taxa or DEFAULT_EXCLUDE_TAXA
    x = summary.copy()
    if sample_type is not None:
        x = x[x["sample_type"] == sample_type]
    x = x[(x["rank"] == rank) & (~x["taxon"].isin(exclude_taxa))]
    if x.empty:
        return pd.DataFrame(columns=["taxon", "mean_abundance", "mean_prevalence"])
    out = (
        x.groupby("taxon", as_index=False)
        .agg(
            mean_abundance=("mean_abundance", "mean"),
            mean_prevalence=("prevalence", "mean"),
        )
        .sort_values("mean_abundance", ascending=False)
        .head(n)
    )
    return out

def shared_taxa_candidates(
    summary: pd.DataFrame,
    min_niches: int = 2,
    rank: str = "genus",
    exclude_taxa: set[str] | None = None,
) -> pd.DataFrame:
    exclude_taxa = exclude_taxa or DEFAULT_EXCLUDE_TAXA
    x = summary[
        (summary["rank"] == rank) & (~summary["taxon"].isin(exclude_taxa))
    ].copy()
    if x.empty:
        return pd.DataFrame(
            columns=["taxon", "n_niches", "mean_prevalence", "evidence_level", "interpretation"]
        )
    grp = (
        x.groupby("taxon")
        .agg(
            n_niches=("sample_type", "nunique"),
            mean_prevalence=("prevalence", "mean"),
        )
        .reset_index()
    )
    grp = grp[grp["n_niches"] >= min_niches].copy()
    grp["evidence_level"] = "C"
    grp["interpretation"] = (
        "shared occurrence candidate only; not evidence of transfer or source contribution"
    )
    return grp.sort_values(["n_niches", "mean_prevalence"], ascending=False)

def descriptive_gradient_candidates(
    summary: pd.DataFrame,
    site_metadata: pd.DataFrame,
    gradient_column: str,
    group_column: str = "site_code",
    min_groups: int = 4,
    min_abs_rho: float = 0.7,
) -> pd.DataFrame:
    """
    Group-level Spearman ordering for hypothesis generation only.
    Never returns p-values or significance labels.
    """
    if group_column not in summary.columns:
        return pd.DataFrame()
    needed = {group_column, gradient_column}
    if not needed.issubset(site_metadata.columns):
        return pd.DataFrame()

    meta = site_metadata[[group_column, gradient_column]].dropna().drop_duplicates()
    x = summary.merge(meta, on=group_column, how="inner")
    rows = []
    for keys, g in x.groupby(["sample_type", "rank", "taxon"]):
        if g[group_column].nunique() < min_groups:
            continue
        rho = g[gradient_column].corr(g["mean_abundance"], method="spearman")
        if pd.notna(rho) and abs(rho) >= min_abs_rho:
            rows.append({
                "sample_type": keys[0],
                "rank": keys[1],
                "taxon": keys[2],
                "n_groups": int(g[group_column].nunique()),
                "spearman_rho_descriptive": float(rho),
                "evidence_level": "C",
                "warning": "descriptive group-level ordering only; no significance or causality",
            })
    return pd.DataFrame(rows)
