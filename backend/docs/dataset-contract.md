# Dataset Contract (v1)

Source dataset: `ManikaSaini/zomato-restaurant-recommendation`

This contract defines the internal canonical fields Phase 1 should produce, independent of source naming differences.

## Canonical `Restaurant` Fields
- `id: str` - stable record identifier generated during ingestion
- `name: str` - restaurant name
- `location: str` - city/locality normalized string
- `cuisines: list[str]` - normalized cuisine tokens
- `cost_for_two: float | None` - normalized estimated cost
- `rating: float | None` - normalized rating on 0-5 scale

## Mapping Notes
- Source columns can vary; ingestion must map them into canonical fields.
- Missing/invalid numeric values should become `None` and be handled downstream.
- Raw source fields may be retained separately for debugging, but core logic should rely on canonical fields only.

## Validation Expectations
- `name` and `location` are required for a valid record.
- `rating`, if present, must be in `[0, 5]` after normalization.
- `cuisines` should be split and trimmed into individual strings.
