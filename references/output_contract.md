# 输出契约

## audit.json

至少包含：

- status
- errors
- warnings
- enabled capabilities
- forbidden claim guards

## claim_ledger.csv

建议字段：

- claim_id
- claim
- evidence_level
- supporting_inputs
- status
- boundary
- alternative_explanations
- next_validation

## hypotheses.json

必须包含：

- hypothesis
- why_generated
- current_evidence
- evidence_level
- alternative_explanations
- falsifiable_prediction
- next_validation
- stop_condition
