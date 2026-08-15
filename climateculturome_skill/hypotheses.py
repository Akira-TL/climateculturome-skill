from __future__ import annotations
from typing import Iterable

def build_hypothesis(
    statement: str,
    why_generated: str,
    current_evidence: str,
    evidence_level: str = "D",
    alternative_explanations: Iterable[str] = (),
    falsifiable_prediction: str = "",
    next_validation: Iterable[str] = (),
    stop_condition: str = "",
) -> dict:
    return {
        "hypothesis": statement,
        "why_generated": why_generated,
        "current_evidence": current_evidence,
        "evidence_level": evidence_level,
        "alternative_explanations": list(alternative_explanations),
        "falsifiable_prediction": falsifiable_prediction,
        "next_validation": list(next_validation),
        "stop_condition": stop_condition,
    }

def template_hypotheses() -> list[dict]:
    """
    Generic templates only. They intentionally contain no real taxa,
    sites, coordinates, dates, or project findings.
    """
    return [
        build_hypothesis(
            statement="A composite environmental axis may explain microbiome reorganization better than a single geographic proxy.",
            why_generated="Geographic proxies often bundle temperature, pressure, moisture and radiation.",
            current_evidence="Requires a site-level environmental matrix and microbiome response data.",
            evidence_level="D",
            alternative_explanations=["spatial structure", "site management", "host composition", "sampling batch"],
            falsifiable_prediction="Composite-axis models outperform single-proxy models under sensitivity analyses.",
            next_validation=["environmental PCA", "variance partitioning", "hierarchical model"],
            stop_condition="Reject if the composite axis adds no stable explanatory value.",
        ),
        build_hypothesis(
            statement="Cross-niche shared taxa may contain candidates for later source-tracking validation.",
            why_generated="Repeated detection across niches can prioritize candidates without implying transfer.",
            current_evidence="Shared occurrence alone is descriptive.",
            evidence_level="D",
            alternative_explanations=["background ubiquity", "taxonomy granularity", "contamination"],
            falsifiable_prediction="Source-tracking estimates reproducible non-zero contributions above negative-control expectations.",
            next_validation=["sample-level feature matrix", "source tracking", "negative controls"],
            stop_condition="Reject transfer interpretation if source contributions are not reproducible.",
        ),
    ]
