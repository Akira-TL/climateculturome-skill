import pandas as pd
from climateculturome_skill.governance import (
    detect_cross_design_collisions,
    preflight,
)

def test_cross_design_collision():
    df = pd.DataFrame([
        {"dataset_id":"A","site_code":"S01","sample_id":"a1","sample_type":"F","sampling_date":"2024-01-01"},
        {"dataset_id":"B","site_code":"S01","sample_id":"b1","sample_type":"F","sampling_date":"2025-01-01"},
    ])
    warnings = detect_cross_design_collisions(df)
    assert warnings

def test_no_fake_coordinate_capability():
    df = pd.DataFrame([
        {"dataset_id":"A","site_code":"S01","sample_id":"a1","sample_type":"F","sampling_date":"2024-01-01"},
    ])
    result = preflight(metadata=df)
    assert result.capabilities["point_environment_matching"] is False
