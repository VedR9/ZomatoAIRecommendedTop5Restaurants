import argparse
import json
from dataclasses import asdict

from milestone1.ingestion.loader import load_restaurants_from_huggingface


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase 1 ingest smoke command")
    parser.add_argument("--limit", type=int, default=5, help="How many rows to load")
    parser.add_argument("--split", type=str, default="train", help="Dataset split")
    parser.add_argument("--revision", type=str, default=None, help="Optional dataset revision")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    restaurants = load_restaurants_from_huggingface(
        split=args.split,
        limit=args.limit,
        revision=args.revision,
    )
    payload = {
        "loaded_count": len(restaurants),
        "sample": [asdict(restaurant) for restaurant in restaurants[:3]],
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
