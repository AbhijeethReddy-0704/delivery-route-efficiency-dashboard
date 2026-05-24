# Validation Rules

Validation script: `scripts/validate_data.py`
Summary output: `data/processed/validation_summary.csv`

## Checks
- Minimum row count (>= 100,000)
- Minimum unique routes (>= 25)
- Duplicate delivery ID check
- Required columns present
- Non-negative delivery cost
- Positive delivery distance
- Valid binary SLA/on-time flags
- Valid date parsing
- Business rule: failed deliveries must have `sla_met_flag = 0`
- Synthetic SLA improvement range check (9% to 15%)

## Summary Schema
- `check_name`
- `result`
- `expected_value`
- `actual_value`
- `status`
- `notes`
