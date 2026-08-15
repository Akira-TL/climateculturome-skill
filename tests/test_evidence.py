import pytest
from climateculturome_skill.evidence import Claim

def test_c_claim_requires_alternatives_and_validation():
    c = Claim(
        claim="Synthetic candidate",
        evidence_level="C",
        supporting_inputs=["synthetic-summary"],
        status="candidate",
        boundary="descriptive only",
        alternative_explanations=["site effect"],
        next_validation=["sample-level model"],
    )
    c.validate()

def test_invalid_level():
    with pytest.raises(ValueError):
        Claim(
            claim="x", evidence_level="Z", supporting_inputs=[],
            status="x", boundary="x", alternative_explanations=[],
            next_validation=[]
        ).validate()
