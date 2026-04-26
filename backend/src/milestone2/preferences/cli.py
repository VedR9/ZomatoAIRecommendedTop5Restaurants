import argparse
import json
import sys
from dataclasses import asdict

from milestone2.preferences.models import (
    ValidationError,
    preference_schema_hint,
    preferences_from_mapping,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase 2 preference parsing command")
    parser.add_argument("--location", required=True)
    parser.add_argument("--budget-band", required=True)
    parser.add_argument("--cuisines", required=True, help="Comma-separated cuisines")
    parser.add_argument("--minimum-rating", required=True, type=float)
    parser.add_argument("--additional-preferences", default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    payload = {
        "location": args.location,
        "budget_band": args.budget_band,
        "cuisines": args.cuisines,
        "minimum_rating": args.minimum_rating,
        "additional_preferences": args.additional_preferences,
    }
    try:
        preferences = preferences_from_mapping(payload)
    except ValidationError as exc:
        output = {"error": str(exc), "schema_hint": preference_schema_hint()}
        print(json.dumps(output, indent=2), file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(asdict(preferences), indent=2))


if __name__ == "__main__":
    main()
