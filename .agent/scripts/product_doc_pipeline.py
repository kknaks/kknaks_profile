#!/usr/bin/env python3
"""Product document pipeline checker/updater.

Implemented:
- validate required/optional stage READMEs
- validate 60-release / 70-runbook frontmatter and required sections
- validate Obsidian wikilinks in frontmatter links fields
  (target exists · label == target frontmatter `id`)
- validate SPEC -> WORK single direction (`spec.works` must stay empty — the
  spec-centric view is derived from work `links.specs`, see rules §정합성)
- warn on specs with no covering work (status implemented/released)
- validate decision 근거 개념 검토 흔적 (`up:` key + 「근거 개념」 section)
- release gate (--release-gate)

Not implemented yet:
- detect changed product docs
- validate optional SPEC -> Architecture -> WORK mappings
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


LINK_BUCKETS = ("baselines", "decisions", "specs", "works", "releases", "related")
WIKILINK_ITEM_RE = re.compile(r'^    - "?\[\[([^\]|]+)(?:\|([^\]]+))?\]\]"?\s*$')
# 「구현됐다」고 선언한 spec 만 커버리지를 요구한다.
# `stable` 은 제외한다 — rules 의 spec status 열거(draft/ready/in_dev/implemented/
# deprecated)에 없는 값이고, 실제로 ax-knowledge-graph 는 「계약 확정」의 뜻으로 쓴다
# (SPEC-001 이 stable 인데 Spec Coverage 는 in-progress). 구현 여부와 무관하다.
COVERED_SPEC_STATUS = {"implemented", "released"}


def read_links(path: Path) -> dict[str, list[tuple[str, str]]]:
    """frontmatter `links:` 버킷 → {버킷: [(대상 stem, 표시 라벨), ...]}.

    `links` 는 중첩 dict 라 read_frontmatter() 가 못 읽는다(들여쓴 줄을 건너뛴다).
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}

    out: dict[str, list[tuple[str, str]]] = {}
    bucket: str | None = None
    for line in text[4:end].splitlines():
        header = re.fullmatch(r"  (\w+):\s*(\[\])?", line)
        if header:
            bucket = header.group(1) if header.group(1) in LINK_BUCKETS else None
            if bucket:
                out.setdefault(bucket, [])
            continue
        if not line.startswith("    "):
            if not line.startswith(" "):
                bucket = None
            continue
        item = WIKILINK_ITEM_RE.match(line)
        if bucket and item:
            out[bucket].append((item.group(1).strip(), (item.group(2) or "").strip()))
    return out


def validate_links(
    product_dirs: list[Path], errors: list[str], warnings: list[str]
) -> None:
    """frontmatter `links` 검증 — 대상 실존 · id 일치 · SPEC→WORK 단방향 · spec coverage.

    rules/product-doc-pipeline.md:
      - "관계 필드에는 ID 문자열이 아니라 Obsidian wikilink를 둔다"
      - "pipeline은 wikilink 대상 파일의 frontmatter `id`를 읽어 관계를 검증한다"
      - "SPEC → WORK 추적은 ... work frontmatter `links.specs` 와 Spec Coverage 에서
         **단방향으로** 관리한다" → `spec.works` 는 derived view 를 원본에 복사한 것이라
         금지한다(「한 곳 원칙」).
    """
    # 링크 대상은 제품 문서가 기본이고, `related` 는 지식노트로도 나간다.
    index: dict[str, tuple[Path, str]] = {}
    for md in ROOT.glob("products/**/*.md"):
        if "_archive" in md.parts:
            continue
        index[md.stem] = (md, read_frontmatter(md).get("id", ""))
    for layer in ("source", "concept", "synthesis"):
        for md in ROOT.glob(f"resources/{layer}/*.md"):
            index.setdefault(md.stem, (md, read_frontmatter(md).get("id", "")))

    covered_specs: set[str] = set()
    specs: list[tuple[Path, str, str]] = []  # (path, id, status)

    for product_dir in product_dirs:
        for md in sorted(product_dir.glob("**/*.md")):
            if "_archive" in md.parts or md.name == "README.md":
                continue
            meta = read_frontmatter(md)
            doc_type = meta.get("type", "")
            if not doc_type:
                continue
            rel = md.relative_to(ROOT)
            links = read_links(md)

            if doc_type == "spec":
                specs.append((md, meta.get("id", md.stem), meta.get("status", "")))
            # 스펙을 구현으로 내리는 문서는 `work` 만이 아니다 — `30-work/` 의
            # `bugfix` 도 links.specs 로 스펙을 가리킨다. 타입을 좁게 잡으면
            # 실제로는 커버된 스펙이 미커버로 잡힌다.
            if doc_type in ("work", "bugfix"):
                covered_specs.update(stem for stem, _ in links.get("specs", []))

            # decision 은 근거 개념 검토 흔적을 남긴다 — `up:` 키 + 「근거 개념」 절.
            # 결론이 「없음」이어도 통과한다(`up: []` + 사유 한 줄). 요구하는 것은
            # 개념을 반드시 잇는 것이 아니라 **검토했다는 사실이 문서에 남는 것**이다.
            # rules/knowledge-note-pipeline.md 「결정을 쓰다 새 개념이 나오면」 참조.
            if doc_type == "decision":
                text = md.read_text(encoding="utf-8")
                fm_end = text.find("\n---\n", 4)
                fm_text = text[4:fm_end] if fm_end != -1 else ""
                if not re.search(r"^up:", fm_text, re.M):
                    errors.append(
                        f"decision missing `up:` (근거 개념 미검토 — 없으면 `up: []`): {rel}"
                    )
                if "## 근거 개념" not in text:
                    errors.append(
                        f"decision missing 「근거 개념」 절 (없으면 '없음 — 사유' 한 줄): {rel}"
                    )

            if doc_type == "spec" and links.get("works"):
                errors.append(
                    f"spec must not link works (SPEC→WORK is single-direction, "
                    f"rules/product-doc-pipeline.md): {rel}"
                )

            for bucket, items in links.items():
                for stem, label in items:
                    target = index.get(stem)
                    if target is None:
                        errors.append(f"dead wikilink: {rel} links.{bucket} -> [[{stem}]]")
                        continue
                    target_id = target[1]
                    if label and target_id and label != target_id:
                        errors.append(
                            f"wikilink label != target id: {rel} links.{bucket} "
                            f"-> [[{stem}|{label}]] (id={target_id})"
                        )

    for path, spec_id, status in specs:
        if status in COVERED_SPEC_STATUS and path.stem not in covered_specs:
            warnings.append(
                f"spec has no covering work: {path.relative_to(ROOT)} "
                f"({spec_id}, status={status})"
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

        validate_links(product_dirs, errors, warnings)

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
