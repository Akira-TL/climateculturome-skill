from __future__ import annotations
from dataclasses import dataclass, asdict

VALID_LEVELS = {"A", "B", "C", "D"}

@dataclass
class Claim:
    claim: str
    evidence_level: str
    supporting_inputs: list[str]
    status: str
    boundary: str
    alternative_explanations: list[str]
    next_validation: list[str]

    def validate(self) -> None:
        if self.evidence_level not in VALID_LEVELS:
            raise ValueError(f"invalid evidence level: {self.evidence_level}")
        if self.evidence_level in {"C", "D"} and not self.next_validation:
            raise ValueError("C/D claims must include next_validation")
        if self.evidence_level in {"C", "D"} and not self.alternative_explanations:
            raise ValueError("C/D claims must include alternative_explanations")

    def to_dict(self) -> dict:
        self.validate()
        return asdict(self)

FORBIDDEN_PHRASES_WITHOUT_EVIDENCE = [
    "proved migration",
    "proven transfer",
    "caused by altitude",
    "climate change caused",
    "significantly enriched",
]

def audit_claim_text(text: str) -> list[str]:
    lower = text.lower()
    return [p for p in FORBIDDEN_PHRASES_WITHOUT_EVIDENCE if p in lower]
