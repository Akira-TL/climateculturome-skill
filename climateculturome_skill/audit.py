from __future__ import annotations

def determine_status(
    preflight_errors: list[str],
    has_summary: bool,
    has_sample_level_matrix: bool,
    human_reviewed: bool = False,
) -> str:
    if preflight_errors:
        return "BLOCKED_BY_INPUTS"
    if human_reviewed:
        return "VALIDATED_WITH_LIMITATIONS"
    if has_sample_level_matrix:
        return "READY_FOR_STATISTICAL_VALIDATION"
    if has_summary:
        return "DESCRIPTIVE_ONLY"
    return "BLOCKED_BY_INPUTS"

def audit_flags() -> dict:
    return {
        "forbidden_claims_guarded": True,
        "fake_coordinates_forbidden": True,
        "shared_occurrence_not_transfer": True,
        "space_not_time": True,
        "summary_not_sample_level_inference": True,
    }
