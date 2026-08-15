import pandas as pd
from climateculturome_skill.microbiome import shared_taxa_candidates

def test_shared_taxa_is_candidate_not_transfer():
    df = pd.DataFrame([
        {"sample_type":"F","rank":"genus","taxon":"Taxon-X","mean_abundance":0.1,"prevalence":0.8},
        {"sample_type":"S","rank":"genus","taxon":"Taxon-X","mean_abundance":0.2,"prevalence":0.7},
    ])
    out = shared_taxa_candidates(df, min_niches=2)
    assert len(out) == 1
    assert "not evidence of transfer" in out.iloc[0]["interpretation"]
