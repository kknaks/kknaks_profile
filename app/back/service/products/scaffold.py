"""제품 문서 골격과 공개 카드 생성 (KDEV-WORK-018 P3 / KDEV-DEC-017 D3·D5·D6).

**결정적이다 — LLM 을 부르지 않는다.** 복사·치환·조립뿐이라 워커도 예산도 비동기
수확도 필요 없다.

가장 조용한 실패 모드가 여기 있다. `templates/product/` 를 통째로 복사하면 예시
문서 8개(`baseline.md` = `id: BASE-001` 등)가 `products/` 아래로 들어가고, 그것들이
frontmatter `type` 을 갖고 있어 **지식 그래프 노드가 된다.** 제품을 둘 만들면 stem
`baseline` 이 둘이 되어 L2 중복 ERROR 가 나고, WORK-007 이 enforce 를 켜 뒀으므로
`load_persona` 가 raise 해 **백엔드가 부팅되지 않는다.**

그래서 복사 목록을 화이트리스트로 두고 테스트가 고정한다.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

import frontmatter

from service.products.errors import ScaffoldError
from utils.slug import next_card_id, product_dir

logger = logging.getLogger("kknaks-back.products.scaffold")

#: 복사할 파일 — `templates/product/` 기준 상대 경로. **이 목록이 계약이다.**
#:
#: `product_doc_pipeline.py:33 REQUIRED_STAGE_READMES` 가 요구하는 4개 + 제품 README +
#: `log.md`. `40-architecture`·`60-release`·`70-runbook` 은 optional 이라 만들지 않는다 —
#: 안 쓰는 제품에 빈 트리를 남기지 않기 위해서다.
SCAFFOLD_FILES: tuple[str, ...] = (
    "README.md",
    "log.md",
    "00-baseline/README.md",
    "10-decision/README.md",
    "20-spec/README.md",
    "30-work/README.md",
)

#: 복사하면 **안 되는** 것. 테스트가 이 목록과 `SCAFFOLD_FILES` 가 겹치지 않는지 본다.
#: 목록으로 남기는 이유는 "왜 빠졌는지" 가 코드에 있어야 하기 때문이다.
NEVER_COPY: tuple[str, ...] = (
    "00-baseline/baseline.md",
    "10-decision/decision.md",
    "20-spec/spec.md",
    "30-work/work.md",
    "30-work/work-release.md",
    "60-release/release.md",
    "70-runbook/runbook.md",
    "40-architecture/database/domains/domain.md",
    # 카드 양식은 형식 SoT 문서지 복사 대상이 아니다 — 아래 `render_card` 가 조립한다.
    "showcase.md",
)


def _templates_dir(repo_root: Path) -> Path:
    return repo_root / "templates" / "product"


def scaffold_paths(slug: str) -> list[str]:
    """만들어질 파일들의 레포 상대 경로. 커밋 대상이자 롤백 단위다."""
    base = product_dir(slug)
    return [f"{base}/{rel}" for rel in SCAFFOLD_FILES]


def write_scaffold(slug: str, repo_root: Path) -> list[str]:
    """골격 6 파일을 만든다. 만든 경로를 돌려준다.

    제목 치환은 하지 않는다 — 템플릿의 `# Product Map` 머리말은 사람이 첫 baseline 을
    쓰면서 같이 손보는 자리이고, 여기서 지어낸 문장을 넣으면 그것이 방치된다.
    """
    templates = _templates_dir(repo_root)
    target_root = repo_root / product_dir(slug)
    written: list[str] = []

    for rel in SCAFFOLD_FILES:
        source = templates / rel
        if not source.exists():
            raise ScaffoldError(
                "TEMPLATE_MISSING", f"템플릿이 없다 — templates/product/{rel}"
            )
        target = target_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        written.append(f"{product_dir(slug)}/{rel}")

    logger.info("제품 골격 생성 — %s (%d 파일)", slug, len(written))
    return written


def existing_card_ids(repo_root: Path) -> list[str]:
    """이미 쓰인 `P-NN`. 채번의 입력이다."""
    ids: list[str] = []
    for path in sorted((repo_root / "products").glob("*/showcase.md")):
        try:
            meta = frontmatter.load(path).metadata
        except Exception:  # noqa: BLE001
            continue
        if meta.get("id"):
            ids.append(str(meta["id"]))
    return ids


def render_card(
    *, slug: str, card: dict[str, Any], repo_root: Path, org: str = "studio"
) -> tuple[str, str]:
    """공개 카드 전문을 조립한다. `(레포 상대 경로, 내용)`.

    **frontmatter 를 시스템이 조립한다.** `type`·`id`·`org` 는 사람이 정하는 값이
    아니고, 특히 `id` 는 자산 경로에 쓰이므로 입력으로 받으면 중복이 난다
    (KDEV-DEC-017 D6).

    **PDF 케이스 스터디 블록을 넣지 않는다.** 케이스 스터디는 제품이 어느 정도
    진행된 뒤에 쓰는 것이고, 빈 필드를 미리 깔면 "채워야 할 것" 과 "안 쓰기로 한 것" 이
    구분되지 않는다(`templates/product/showcase.md`).
    """
    card_id = next_card_id(existing_card_ids(repo_root))
    meta: dict[str, Any] = {
        "type": "project",
        "id": card_id,
        "org": org,
        "title": card["title"],
        "summary": card["summary"],
        "category": card["category"],
        "status": card["status"],
        "stack": card["stack"],
        # 기본은 **감춤**이다. 본문이 비어 있는 채로 사이트에 올라가지 않게 한다.
        "visible": False,
    }
    if card.get("date"):
        meta["date"] = card["date"]
    if card.get("thumbnail"):
        meta["thumbnail"] = card["thumbnail"]
    if card.get("links"):
        meta["links"] = card["links"]

    body = "\n".join(
        [
            "# 개요",
            "",
            "# 기술스택",
            "",
            "# 주요기능",
            "",
        ]
    )
    content = frontmatter.dumps(frontmatter.Post(body, **meta)) + "\n"
    return f"{product_dir(slug)}/showcase.md", content


def append_product_index(slug: str, repo_root: Path) -> str | None:
    """`products/README.md` 제품 목록에 행을 더한다 (KDEV-DEC-017 D15).

    **표를 재생성하지 않고 행만 넣는다** — `Context` 열에 사람이 적은 메모가 있다.
    이미 있으면 건드리지 않는다.
    """
    index = repo_root / "products" / "README.md"
    if not index.exists():
        return None
    text = index.read_text(encoding="utf-8")
    row = f"| {slug} | `products/{slug}/` |"
    if f"| {slug} |" in text:
        return None

    lines = text.splitlines()
    last_row = max(
        (i for i, line in enumerate(lines) if line.startswith("| ") and "|" in line[2:]),
        default=None,
    )
    if last_row is None:
        return None
    lines.insert(last_row + 1, row)
    index.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "products/README.md"


#: frontmatter 안의 `visible:` 한 줄. **블록 안에서만 찾는다** — 본문에 같은 문자열이
#: 있어도 건드리지 않기 위해서다.
_VISIBLE_LINE = re.compile(r"^(\s*visible\s*:\s*)(true|false)\s*$", re.IGNORECASE)


def set_card_visible(slug: str, value: bool, repo_root: Path) -> str:
    """카드의 `visible` **한 줄만** 바꾼다. 레포 상대 경로를 돌려준다.

    **`frontmatter.loads()` → `dumps()` 왕복을 쓰지 않는다.** 값은 보존되지만 주석이
    사라지고 키가 알파벳순으로 재정렬된다 — WORK-017 결함 ⑩ 에서 한 줄을 바꾸려던
    발행이 42 insertions / 38 deletions 를 냈고 `# 이력서 PDF — 비면 PDF 미표시` 주석이
    없어졌다. 사람이 적어 둔 주석과 순서도 그 사람의 것이다.

    `visible` 키가 없으면 **추가한다.** 로더 기본값이 `true` 라(`projects.py:18`)
    없는 상태에서 끄려면 줄이 생겨야 한다.
    """
    path = repo_root / product_dir(slug) / "showcase.md"
    if not path.exists():
        raise ScaffoldError("CARD_MISSING", f"공개 카드가 없다 — {product_dir(slug)}/showcase.md")

    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ScaffoldError("CARD_MALFORMED", "카드에 frontmatter 가 없다")

    close = next(
        (i for i in range(1, len(lines)) if lines[i].strip() == "---"), None
    )
    if close is None:
        raise ScaffoldError("CARD_MALFORMED", "frontmatter 가 닫히지 않았다")

    literal = "true" if value else "false"
    for i in range(1, close):
        match = _VISIBLE_LINE.match(lines[i].rstrip("\n"))
        if match:
            lines[i] = f"{match.group(1)}{literal}\n"
            break
    else:
        # 키가 없다 — 닫는 `---` 바로 앞에 넣는다. 순서를 흩지 않는 자리다.
        lines.insert(close, f"visible: {literal}\n")

    path.write_text("".join(lines), encoding="utf-8")
    return f"{product_dir(slug)}/showcase.md"
