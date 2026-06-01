#!/usr/bin/env python3
"""Product document pipeline checker/updater.

This script is intentionally a scaffold for now.

Expected responsibilities:
- detect changed product docs
- validate frontmatter and IDs
- validate BASE -> DEC -> SPEC -> WORK mappings
- validate optional SPEC -> Architecture -> WORK mappings
- validate Obsidian wikilinks in frontmatter links fields
- validate optional 40-architecture structure when present
- validate product/doc/status tag patterns
- sync stage README indexes
- sync product README maps
- append product log entries

Rules source: rules/product-doc-pipeline.md
Hook contract: .agent/hooks/product-doc-pipeline.md
"""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRODUCTS_DIR = ROOT / "products"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate product document pipeline.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when validation errors are found.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    if not PRODUCTS_DIR.exists():
        errors.append(f"missing products directory: {PRODUCTS_DIR}")

    print("Product Doc Pipeline")
    print(f"- checked: {PRODUCTS_DIR}")
    print("- updated: none (scaffold)")
    print(f"- warnings: {len(warnings)}")
    for warning in warnings:
        print(f"  - {warning}")
    print(f"- errors: {len(errors)}")
    for error in errors:
        print(f"  - {error}")
    print("- needs_user_decision: none")

    if args.strict and errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
