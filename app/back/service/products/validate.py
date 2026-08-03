"""등록 사전 검증 (KDEV-WORK-018 P3 / KDEV-SPEC-014 §4 Validation).

**파일을 쓰기 전에 전부 판정한다.** 하나라도 걸리면 아무것도 만들어지지 않는다 —
`service/apply/plan.py` 가 발행 전에 검증하는 것과 같은 규율이다. 커밋 후 부팅에서
잡으면 이미 사이트가 멈춰 있다.

여기서 보지 **않는** 것이 하나 있다. `product_slug` 가 실재하는 디렉토리인지는 거부
사유가 아니다(KDEV-DEC-017 D7) — 저장하고 조회 응답이 경고를 싣는다. 막지 않고 알린다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from service.products.errors import ProductError
from utils.slug import is_valid_product_slug, parse_repo_slug, product_dir

#: 카드가 반드시 가져야 하는 값. 하나라도 없으면 로더가 `PersonaError` 를 던지고
#: **persona 로드 전체**가 실패한다 — 파일 하나가 거부되는 것으로 끝나지 않는다.
REQUIRED_CARD_FIELDS = ("title", "summary", "category", "status", "stack")

#: 사이트에서 쓰는 진행 상태.
CARD_STATUSES = ("wip", "live")


def load_categories(repo_root: Path) -> list[str]:
    """허용 분류. **이 코드가 아니라 `persona/_meta.yaml` 이 소유한다.**

    목록을 코드에 박으면 SoT 가 둘이 되고, 사이트가 아는 분류와 화면이 주는 분류가
    갈리는 날 등록이 통과한 뒤 로드가 죽는다.
    """
    meta_path = repo_root / "persona" / "_meta.yaml"
    try:
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    except Exception:  # noqa: BLE001 — 읽을 수 없으면 고를 것이 없는 상태다
        return []
    return [
        str(c.get("id"))
        for c in (meta.get("projects") or {}).get("categories") or []
        if c.get("id")
    ]


def normalize_repo_slug(raw: str) -> str:
    slug = parse_repo_slug(raw)
    if not slug:
        raise ProductError(
            "INVALID_SLUG",
            "레포는 `owner/name` 또는 GitHub 주소여야 한다",
            field="repo",
        )
    return slug


def check_slug_available(slug: str, existing: set[str]) -> None:
    if slug in existing:
        raise ProductError(
            "SLUG_TAKEN", f"이미 등록된 레포다 — {slug}", field="repo"
        )


def check_product_slug_shape(slug: str) -> None:
    if not is_valid_product_slug(slug):
        raise ProductError(
            "INVALID_PRODUCT_SLUG",
            "제품 slug 는 소문자·숫자·하이픈만 쓴다 (예: `mac-remote`)",
            field="product_slug",
        )


def check_product_dir_free(slug: str, repo_root: Path) -> None:
    """이미 있는 디렉토리에 스캐폴드하지 않는다.

    덮어쓰면 사람이 쌓아 둔 baseline·decision 이 사라진다. **이미 있는 제품에 레포를
    잇는 것은 등록이 아니라 수정이다** — 그쪽은 `PATCH` 로 간다.
    """
    if (repo_root / product_dir(slug)).exists():
        raise ProductError(
            "PRODUCT_EXISTS",
            f"제품 디렉토리가 이미 있다 — {product_dir(slug)}. 연결만 하려면 목록에서 수정한다",
            field="product_slug",
        )


def check_career(detail: str | None, repo_root: Path) -> None:
    """`company` 의 career 귀속.

    오타는 DB CHECK 를 통과한다(`detail IS NOT NULL` 만 본다). 막지 않으면 조사까지
    정상으로 돌다가 **발행 단계에서** 없는 문서에 쓰려다 그날 career 가 사라진다 —
    승인 화면까지 가서야 보이는 실패다.
    """
    if not detail:
        raise ProductError(
            "CAREER_REQUIRED",
            "회사 레포는 어느 career 에 귀속할지 정해야 한다",
            field="detail",
        )
    if not (repo_root / "persona" / "career" / f"{detail}.md").exists():
        raise ProductError(
            "CAREER_NOT_FOUND",
            f"career 문서가 없다 — persona/career/{detail}.md",
            field="detail",
        )


def check_card(card: dict[str, Any], repo_root: Path) -> None:
    """공개 카드 입력. **`category` 가 특히 중요하다.**

    허용 목록 밖의 값이 파일에 들어가면 `validate_persona` 가 `PersonaError` 를 던져
    persona 로드 **전체**가 실패하고, `reload_data` 가 기존 데이터를 유지해 사이트는
    옛 데이터를 계속 서빙한다. 발행 뒤에야 알게 된다.
    """
    for field in REQUIRED_CARD_FIELDS:
        value = card.get(field)
        if value is None or value == "" or value == [] or value == {}:
            raise ProductError(
                "CARD_FIELD_MISSING", f"카드 필수 값이 비어 있다 — {field}", field=field
            )

    categories = load_categories(repo_root)
    if categories and card.get("category") not in categories:
        raise ProductError(
            "CATEGORY_INVALID",
            f"분류는 {', '.join(categories)} 중 하나여야 한다",
            field="category",
        )

    if card.get("status") not in CARD_STATUSES:
        raise ProductError(
            "CARD_FIELD_MISSING",
            f"상태는 {', '.join(CARD_STATUSES)} 중 하나여야 한다",
            field="status",
        )

    for lang_field in ("title", "summary"):
        value = card.get(lang_field)
        if not isinstance(value, dict) or not value.get("ko") or not value.get("en"):
            raise ProductError(
                "CARD_FIELD_MISSING",
                f"{lang_field} 은 ko·en 을 모두 채운다",
                field=lang_field,
            )
