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
- validate optional 60-release structure when present
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

REQUIRED_STAGE_READMES = (
    "00-baseline/README.md",
    "10-decision/README.md",
    "20-spec/README.md",
    "30-work/README.md",
)
OPTIONAL_STAGE_READMES = (
    "40-architecture/README.md",
    "60-release/README.md",
)
RELEASE_REQUIRED_SECTIONS = (
    "## 요약",
    "## 상세 수정 사항",
)


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
    else:
        for product_dir in sorted(p for p in PRODUCTS_DIR.iterdir() if p.is_dir()):
            for rel_path in REQUIRED_STAGE_READMES:
                if not (product_dir / rel_path).exists():
                    errors.append(f"missing required stage README: {product_dir.name}/{rel_path}")

            for rel_path in OPTIONAL_STAGE_READMES:
                stage_dir = product_dir / rel_path.split("/")[0]
                readme = product_dir / rel_path
                if stage_dir.exists() and not readme.exists():
                    errors.append(f"missing optional stage README: {product_dir.name}/{rel_path}")

            release_dir = product_dir / "60-release"
            if release_dir.exists():
                for release_note in sorted(release_dir.glob("release-*.md")):
                    source = release_note.read_text(encoding="utf-8")
                    rel_note = release_note.relative_to(ROOT)
                    if "type: release" not in source:
                        errors.append(f"release missing type frontmatter: {rel_note}")
                    if "version:" not in source:
                        errors.append(f"release missing version frontmatter: {rel_note}")
                    if "released_at:" not in source:
                        errors.append(f"release missing released_at frontmatter: {rel_note}")
                    if "summary:" not in source:
                        errors.append(f"release missing summary frontmatter: {rel_note}")
                    if "details:" not in source:
                        errors.append(f"release missing details frontmatter: {rel_note}")
                    for section in RELEASE_REQUIRED_SECTIONS:
                        if section not in source:
                            errors.append(f"release missing required section {section!r}: {rel_note}")

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
