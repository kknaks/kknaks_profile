#!/usr/bin/env python3
"""synthesis(판단층) 후보 탐지 — 같은 개념이 여러 제품의 결정 근거로 반복되는 자리를 찾는다.

`dec1 -> up -> concept1` 과 `dec2 -> up -> concept1` 은 **위반이 아니다.** 개념 하나가
여러 결정의 근거인 것은 정상이고, 그것이 곧 판단층을 만들 이유도 아니다.

판단층을 만드는 조건은 「공통」이 아니라 **같은 판단의 반복**이다. 그 판정은 결정 본문을
읽어야 하므로 기계가 못 한다. 이 스크립트는 **① 후보를 뽑는 데까지만** 한다.

    ① 기계  — 서로 다른 제품 decision N곳 이상의 근거인 개념 (이 스크립트)
    ② 사람  — 그 결정들이 같은 말을 하는지 본문 대조 → 같으면 synthesis, 다르면 그대로

가른 실제 사례:
  - `unique-key` 4제품 — 멱등 upsert · transaction_id 중복 차단 · 하루 1회 제출.
    같은 개념의 **다른 적용**이라 올리지 않았다(올리면 「유일 제약을 쓴다」는 공허한 노트).
  - `human-in-the-loop` 3제품 — 셋 다 「AI 제안 ≠ 확정」을 말해 같은 판단이었다.
    → resources/synthesis/ai-proposes-human-approves.md 로 올렸다.

규칙: rules/knowledge-note-pipeline.md 「concept 직접이냐 synthesis 경유냐」
양식: templates/knowledge/permanent.md 「언제 만드나」

pre-commit 은 이것을 **막지 않는다.** 위반이 아니기 때문이다.
`product_doc_pipeline.py` 가 products 변경 시 후보 개수 한 줄만 알린다.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MIN_PRODUCTS = 3

UP_BLOCK_RE = re.compile(r"^up:\s*(\[\])?\s*$\n((?:  - .*\n)*)", re.M)
BULLET_RE = r"- \[\[{}\]\] — (.*)"


def frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    return text[4:end] if end != -1 else ""


def up_targets(fm: str) -> list[str]:
    m = UP_BLOCK_RE.search(fm + "\n")
    return re.findall(r"^  - (\S+)", m.group(2), re.M) if m else []


def field(fm: str, key: str) -> str:
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
    return m.group(1).strip().strip('"') if m else ""


def owning_synthesis() -> dict[str, list[str]]:
    """개념 → 그 개념을 `up:` 한 synthesis stem 들.

    **후보에서 빼지 않는다.** 판단 노트가 있다고 그 개념의 모든 쓰임이 덮이는 것은
    아니다 — `ai-agent` 는 승인 게이트 판단이 소유하지만, 「요약 호출을 라이브러리에
    맡긴다」처럼 **다른 판단**으로 그 개념에 기대는 결정이 따로 있다. 숨기면 그 두 번째
    판단을 영영 못 본다. 그래서 표시만 한다.
    """
    owning: dict[str, list[str]] = defaultdict(list)
    for path in (ROOT / "resources" / "synthesis").glob("*.md"):
        for concept in up_targets(frontmatter(path)):
            owning[concept].append(path.stem)
    return owning


def find_candidates(min_products: int = DEFAULT_MIN_PRODUCTS) -> dict[str, dict[str, list]]:
    """개념 → {제품: [(decision stem, title, 근거 한 줄)]}. 후보만 남긴다."""
    concepts = {p.stem for p in (ROOT / "resources" / "concept").glob("*.md")}

    hits: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for path in sorted(ROOT.glob("products/*/10-decision/decision-*.md")):
        if "_archive" in path.parts:
            continue
        product = path.parts[path.parts.index("products") + 1]
        fm = frontmatter(path)
        body = path.read_text(encoding="utf-8")
        title = field(fm, "title")
        for target in up_targets(fm):
            if target not in concepts:
                continue  # synthesis 를 가리키는 것은 이미 판단을 경유하고 있다
            m = re.search(BULLET_RE.format(re.escape(target)), body)
            hits[target][product].append((path.stem, title, m.group(1).strip() if m else ""))

    return {c: prods for c, prods in hits.items() if len(prods) >= min_products}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--min", type=int, default=DEFAULT_MIN_PRODUCTS,
                    help=f"후보로 볼 최소 제품 수 (기본 {DEFAULT_MIN_PRODUCTS})")
    ap.add_argument("--count-only", action="store_true", help="후보 개수만 한 줄로 출력")
    args = ap.parse_args()

    candidates = find_candidates(args.min)

    if args.count_only:
        print(f"synthesis 후보: {len(candidates)}건 (제품 {args.min}곳 이상에서 근거)")
        return 0

    print(f"# synthesis 후보 — 서로 다른 제품 {args.min}곳 이상의 결정 근거인 개념\n")
    if not candidates:
        print("없음.")
    owning = owning_synthesis()
    for concept, prods in sorted(candidates.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        mark = f"  ← 이미 판단 노트 있음: {', '.join(owning[concept])}" if concept in owning else ""
        print(f"## {concept}  ({len(prods)}개 제품){mark}")
        for product, rows in sorted(prods.items()):
            for stem, title, why in rows:
                print(f"  [{product}] {title or stem}")
                if why:
                    print(f"      └ {why[:150]}")
        print()

    if candidates:
        print("---")
        print("이 목록은 **위반이 아니라 후보**다. 다음은 사람이 판정한다:")
        print("  같은 판단을 반복하고 있나 → templates/knowledge/permanent.md 로 synthesis 작성")
        print("  같은 개념의 다른 적용인가 → 그대로 둔다 (`unique-key` 가 그 사례)")

    if owning:
        print("\n판단 노트가 이미 있는 개념도 목록에 남긴다 — 그 판단이 아닌 **다른 측면**으로")
        print("기대는 결정이 있을 수 있고, 숨기면 두 번째 판단을 못 보기 때문이다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
