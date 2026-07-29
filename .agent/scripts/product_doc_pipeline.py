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
import re
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
    "70-runbook/README.md",
)
RELEASE_REQUIRED_SECTIONS = (
    "## 요약",
    "## 상세 수정 사항",
)
RELEASE_WORK_REQUIRED_SECTIONS = (
    "## 심사 체크리스트",
    "## 제출 기록",
    "## 심사 결과",
)
RUNBOOK_REQUIRED_SECTIONS = (
    "## 목적",
    "## 절차",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate product document pipeline.")
    parser.add_argument(
        "--product",
        help="Validate one product slug under products/.",
    )
    parser.add_argument(
        "--release-gate",
        action="store_true",
        help="Require the selected product to be cut-ready: specs implemented/stable and works done.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when validation errors are found.",
    )
    return parser.parse_args()


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith((" ", "-")):
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta


def table_rows(source: str, header: str) -> list[list[str]]:
    lines = source.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            start = i
            break
    if start is None:
        return []

    rows: list[list[str]] = []
    seen_table = False
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        if not line.lstrip().startswith("|"):
            if seen_table:
                continue
            continue
        seen_table = True
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r"[-: ]+", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows[1:] if rows else []


def validate_release_gate(product_dir: Path, errors: list[str]) -> None:
    product = product_dir.name
    spec_dir = product_dir / "20-spec"
    work_dir = product_dir / "30-work"

    spec_files = sorted(spec_dir.glob("spec-*.md")) if spec_dir.exists() else []
    if not spec_files:
        errors.append(f"release gate failed: {product} has no spec files")
    for spec in spec_files:
        meta = read_frontmatter(spec)
        status = meta.get("status", "")
        if status not in {"implemented", "released", "stable"}:
            errors.append(
                f"release gate failed: spec not implemented/stable: {spec.relative_to(ROOT)} status={status or '-'}"
            )

    work_files = sorted(work_dir.glob("work-*.md")) if work_dir.exists() else []
    if not work_files:
        errors.append(f"release gate failed: {product} has no work files")
    for work in work_files:
        meta = read_frontmatter(work)
        status = meta.get("status", "")
        progress = meta.get("progress", "")
        if status != "done":
            errors.append(
                f"release gate failed: work not done: {work.relative_to(ROOT)} status={status or '-'}"
            )
        if progress and progress != "100":
            errors.append(
                f"release gate failed: work progress not 100: {work.relative_to(ROOT)} progress={progress}"
            )

    work_index = work_dir / "README.md"
    if work_index.exists():
        source = work_index.read_text(encoding="utf-8")
        for row in table_rows(source, "## Work 목록"):
            if len(row) >= 5:
                status = row[3].strip("`")
                progress = row[4].strip("`")
                if status and status != "done":
                    errors.append(
                        f"release gate failed: work index row not done: {product}/30-work/README.md {row[0]} status={status}"
                    )
                if progress and progress != "100":
                    errors.append(
                        f"release gate failed: work index row progress not 100: {product}/30-work/README.md {row[0]} progress={progress}"
                    )

        for row in table_rows(source, "## Spec Coverage"):
            if len(row) >= 3:
                coverage = row[2].strip("`").lower()
                if coverage not in {"full", "done", "implemented"}:
                    errors.append(
                        f"release gate failed: spec coverage incomplete: {product}/30-work/README.md {row[0]} coverage={row[2]}"
                    )


def main() -> int:
    args = parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    if not PRODUCTS_DIR.exists():
        errors.append(f"missing products directory: {PRODUCTS_DIR}")
    else:
        stage_dir_names = tuple(rel.split("/")[0] for rel in REQUIRED_STAGE_READMES)
        product_dirs = sorted(p for p in PRODUCTS_DIR.iterdir() if p.is_dir())
        if args.product:
            product_dirs = [p for p in product_dirs if p.name == args.product]
            if not product_dirs:
                errors.append(f"product not found: products/{args.product}")

        for product_dir in product_dirs:
            # showcase-only 제품(S1: 회사/일부 개인) — stage 디렉토리 없이 showcase.md 만.
            # 구조로 추론(KDEV-SPEC-001 §5): showcase.md 가 있고 stage 디렉토리가 하나도
            # 없으면 stage README 면제. (showcase 도 stage 도 없는 빈 dir 은 여전히 에러)
            is_showcase_only = (product_dir / "showcase.md").exists() and not any(
                (product_dir / s).is_dir() for s in stage_dir_names
            )
            if not is_showcase_only:
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

            work_dir = product_dir / "30-work"
            if work_dir.exists():
                for work_note in sorted(work_dir.glob("work-*.md")):
                    source = work_note.read_text(encoding="utf-8")
                    if "work_type: release" not in source:
                        continue
                    rel_note = work_note.relative_to(ROOT)
                    for section in RELEASE_WORK_REQUIRED_SECTIONS:
                        if section not in source:
                            errors.append(
                                f"release work missing required section {section!r}: {rel_note}"
                            )
                    if "work-type/release" not in source:
                        warnings.append(
                            f"release work missing 'work-type/release' tag: {rel_note}"
                        )

            runbook_dir = product_dir / "70-runbook"
            if runbook_dir.exists():
                for runbook in sorted(runbook_dir.glob("runbook-*.md")):
                    source = runbook.read_text(encoding="utf-8")
                    rel_note = runbook.relative_to(ROOT)
                    if "type: runbook" not in source:
                        errors.append(f"runbook missing type frontmatter: {rel_note}")
                    for section in RUNBOOK_REQUIRED_SECTIONS:
                        if section not in source:
                            errors.append(
                                f"runbook missing required section {section!r}: {rel_note}"
                            )

            if args.release_gate and not is_showcase_only:
                validate_release_gate(product_dir, errors)

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
