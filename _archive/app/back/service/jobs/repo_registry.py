"""레포 레지스트리 — 조회와 1회 시드 (KDEV-WORK-017 P5 / KDEV-WORK-018 P2).

시드는 **한 번만** 돈다. 그 뒤로는 레지스트리가 SoT 이고 showcase 는 공개 표시용으로
돌아간다 — 둘을 계속 동기화하면 "보여줄 레포와 긁을 레포를 분리한다" 는 목적이
무의미해진다.

**시드 원천이 showcase 스캔에서 명시 목록으로 바뀌었다** (KDEV-WORK-018 P2). 이유가
둘이고 둘 다 P1 의 결과다.

- **회사 레포는 카드가 없어졌다.** KDEV-DEC-017 D9 로 `products/{회사}/showcase.md`
  5개를 지웠다 — 회사 레포는 문서 트리도 공개 카드도 갖지 않고 레지스트리에만 산다.
  스캔할 원천 자체가 사라졌으므로 `COMPANY_REPOS` 가 그 자리를 대신한다.
- **카드 없이 추적할 레포가 생겼다.** D12 의 4개(`ax-graph`·`gcs_demo`·`lunch_game`·
  `mac-remote`)는 제품 문서만 있고 공개 카드가 없다. 실측으로 **최근 30일 본인 커밋
  57건**이 이것들 때문에 잔디에서 빠지고 있었다.

`product_slug` 도 스캔으로 유도할 수 없다. `kknaks/kknaks_profile` 이 어느 제품인지는
문자열로 정해지지 않는다(`kknaks-profile` 이었다가 D2 로 `kknaks-dev` 가 됐다).

`detail`(career 귀속)은 여전히 사람이 준다. `--company-detail` 로 받은 값을 적기만 한다.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

import frontmatter
from sqlalchemy.ext.asyncio import AsyncSession

import repository.tracked_repos as tracked_repos_repo
from service.products.dto import RepoCreate, RepoPatch, TrackedRepoDTO

logger = logging.getLogger("kknaks-back.repo-registry")

#: `github.com/owner/name` · `https://github.com/owner/name` 어느 쪽이든 받는다.
_SLUG_RE = re.compile(r"(?:https?://)?(?:www\.)?github\.com/([^/\s]+/[^/\s#?]+)")

#: 개인 계정 둘 — 어느 쪽이든 personal 토큰으로 클론한다.
PERSONAL_OWNERS = ("kknaks", "kknaksss")

#: 레포 → `products/` 디렉토리명 (KDEV-DEC-017 D1).
#:
#: **문자열로 유도할 수 없어서 표로 둔다.** `kknaks/kknaks_profile` 은 `kknaks-profile`
#: 이었다가 D2 통합으로 `kknaks-dev` 가 됐고, `kknaksss/mykakao` 처럼 소유자와 제품명이
#: 다른 경우도 있다. 규칙을 지어내면 조용히 틀린 곳에 붙는다.
PRODUCT_BY_SLUG: dict[str, str] = {
    # studio — 공개 카드 있음
    "kknaks/kknaks_profile": "kknaks-dev",
    "kknaks/language_diary": "language-diary",
    "kknaks/open_kknaks": "open-kknaks",
    "kknaks/persona_counselor": "persona-counselor",
    "kknaks/study_timelapse": "study-timelapse",
    "kknaks/summer_star_company": "summer-star-company",
    "kknaks/wine_log": "wine-log",
    "kknaksss/mykakao": "mykakao",
    # studio — 카드 없음 (D12)
    "kknaks/ax-graph": "ax-knowledge-graph",
    "kknaks/lunch_game": "mini-game",
    "kknaks/mac-remote": "mac-remote",
    "kknaksss/gcs_demo": "cloud-file-organizer",
    # company — 제품 문서가 없다. 조인할 곳이 없어 비운다.
}

#: 공개 카드가 없어 showcase 스캔에 안 잡히는 studio 레포 (KDEV-DEC-017 D12).
CARDLESS_REPOS: tuple[str, ...] = (
    "kknaks/ax-graph",
    "kknaks/lunch_game",
    "kknaks/mac-remote",
    "kknaksss/gcs_demo",
)

#: 회사 레포. D9 로 카드가 사라져 스캔 원천이 없다 — 여기가 유일한 목록이다.
COMPANY_REPOS: tuple[str, ...] = (
    "MediSolveAIDev/CENTURION-CHARTY",
    "MediSolveAIDev/Linky",
    "MediSolveAIDev/NEXUS",
    "MediSolveAIDev/centurion_mso",
    "MediSolveAIDev/mediness",
)


@dataclass(frozen=True)
class SeedEntry:
    slug: str
    type: str
    account: str


def parse_slug(raw: str) -> str | None:
    """`links.repo` → `owner/name`. 못 읽으면 `None`.

    showcase 는 `github.com/owner/name` 으로 적는데 레지스트리는 `owner/name` 을
    쓴다. 접두를 안 떼면 클론 URL 이 `github.com/github.com/...` 이 된다.
    """
    match = _SLUG_RE.search(raw or "")
    if match:
        return match.group(1).removesuffix(".git")
    cleaned = (raw or "").strip().strip("/")
    return cleaned if cleaned.count("/") == 1 and " " not in cleaned else None


def account_for(slug: str) -> str:
    """소유자 → 토큰 종류. 개인 계정이 둘이라 목록으로 본다."""
    owner = slug.split("/", 1)[0]
    return "personal" if owner in PERSONAL_OWNERS else "company"


def scan_showcase(repo_root: Path) -> list[SeedEntry]:
    """`products/*/showcase.md` 를 훑어 시드 후보를 만든다.

    `visible` 은 보지 않는다 — 사이트 표시 여부와 추적 여부는 다른 축이고, 그 둘을
    가르려고 레지스트리를 만드는 것이다.
    """
    entries: list[SeedEntry] = []
    seen: set[str] = set()
    for path in sorted((repo_root / "products").glob("*/showcase.md")):
        try:
            meta = frontmatter.load(path).metadata
        except Exception:  # noqa: BLE001
            logger.warning("showcase 를 읽지 못했다 — %s", path)
            continue
        raw = str((meta.get("links") or {}).get("repo") or "")
        slug = parse_slug(raw)
        if not slug or slug in seen:
            continue
        seen.add(slug)
        kind = "company" if str(meta.get("org") or "") == "company" else "studio"
        entries.append(SeedEntry(slug=slug, type=kind, account=account_for(slug)))
    return entries


async def seed_from_showcase(db: AsyncSession, repo_root: Path) -> dict[str, int]:
    """시드를 **한 번** 적용한다. 이미 있는 slug 는 건드리지 않는다.

    덮어쓰지 않는 이유는 `detail`·`enabled`·`path_rules` 가 사람이 손본 값이기
    때문이다. 다시 돌려도 새 레포만 들어온다.

    `company` 는 `detail` 이 필수인데 시드가 그 값을 지어낼 수 없다. 그래서 **`studio` 만
    넣고 `company` 는 `seed_company()` 에 맡긴다** — 사람이 채워야 할 것이 몇 건인지
    `needs_detail` 로 돌려준다.

    **카드가 없는 studio 레포(`CARDLESS_REPOS`)를 함께 넣는다** (KDEV-DEC-017 D12).
    showcase 스캔만 쓰면 제품 문서만 있는 레포가 영원히 안 잡히고, 실측으로 그것이
    최근 30일 57건이었다.
    """
    existing = await tracked_repos_repo.existing_slugs(db)
    scanned = scan_showcase(repo_root)
    skipped_company = sum(1 for e in scanned if e.type == "company")

    candidates = [e.slug for e in scanned if e.type != "company"]
    candidates += [slug for slug in CARDLESS_REPOS if slug not in candidates]

    added = 0
    for slug in candidates:
        if slug in existing:
            continue
        await tracked_repos_repo.create(
            db,
            RepoCreate(
                slug=slug,
                type="studio",
                product_slug=PRODUCT_BY_SLUG.get(slug),
                account=account_for(slug),
            ),
        )
        added += 1
    await db.flush()
    return {"added": added, "needs_detail": skipped_company, "existing": len(existing)}


class UnknownCareerError(ValueError):
    """`detail` 이 실재하지 않는 career stem 을 가리킨다."""


async def seed_company_from_showcase(
    db: AsyncSession, repo_root: Path, *, detail: str
) -> dict[str, int]:
    """회사 레포를 `detail`(career 귀속)을 붙여 넣는다.

    시드가 company 를 건너뛰는 것은 옳은 판단이지만, 그러면 **넣을 방법이 아무데도
    없다.** 그 자리를 여기서 메운다 — 어느 career 로 갈지는 여전히 사람이 정하고,
    이 함수는 그 값을 받아 적기만 한다.

    **목록은 `COMPANY_REPOS` 다.** KDEV-DEC-017 D9 로 회사 제품의 `showcase.md` 가
    사라져 스캔할 원천이 없다 — 회사 레포는 문서 트리도 카드도 없이 레지스트리에만
    산다.

    `detail` 을 하나만 받는 이유는 지금 재직 중인 회사가 하나이기 때문이다
    (`is_current: true` 는 `medisolve-ai` 뿐). 회사가 늘면 slug 별로 받게 바꾼다 —
    지금 그 일반화를 하면 쓰지 않을 인자를 설계하는 것이 된다.

    **실재하는 career 문서인지 먼저 본다.** 오타가 나면 DB CHECK 는 통과하고
    (`detail IS NOT NULL` 만 본다) 조사도 정상으로 돌지만, 발행 단계에서 없는 문서에
    쓰려다 그날 career 가 통째로 사라진다. 그 실패는 승인 화면까지 가서야 보인다.

    Raises:
        UnknownCareerError: `persona/career/{detail}.md` 가 없을 때.
    """
    career_path = repo_root / "persona" / "career" / f"{detail}.md"
    if not career_path.exists():
        raise UnknownCareerError(
            f"career 문서가 없다 — {career_path}. `detail` 은 실재하는 stem 이어야 한다"
        )

    existing = await tracked_repos_repo.existing_slugs(db)
    added = 0
    for slug in COMPANY_REPOS:
        if slug in existing:
            continue
        await tracked_repos_repo.create(
            db,
            RepoCreate(
                slug=slug,
                type="company",
                detail=detail,
                product_slug=PRODUCT_BY_SLUG.get(slug),
                account=account_for(slug),
            ),
        )
        added += 1
    await db.flush()
    return {"added": added, "detail": detail}


async def enabled_repos(db: AsyncSession) -> list[TrackedRepoDTO]:
    """조사 대상. `enabled` 가 꺼진 것은 클론을 남긴 채 fetch 만 멈춘다.

    쿼리는 `repository/tracked_repos.py` 가 갖는다 — 이 모듈은 시드라는 도메인 규칙을
    맡고 DB 접근은 계층에 넘긴다(KDEV-WORK-018 P2).
    """
    return await tracked_repos_repo.list_enabled(db)


async def backfill_product_slug(db: AsyncSession) -> dict[str, int]:
    """이미 있는 행에 `product_slug` 를 채운다 (KDEV-WORK-018 P2).

    `0009` 로 컬럼이 새로 생겨 **기존 행은 전부 `NULL`** 이다. 그래서 이 채우기는
    "사람이 손본 값을 덮어쓰지 않는다" 는 시드 규율과 충돌하지 않는다 — 비어 있는
    자리에만 쓴다.

    **이미 값이 있으면 건드리지 않는다.** 화면에서 연결을 바꿨을 수 있고, 그때는
    사람 쪽이 옳다.
    """
    filled = skipped = unknown = 0
    for row in await tracked_repos_repo.list_all(db):
        if row.product_slug:
            skipped += 1
            continue
        mapped = PRODUCT_BY_SLUG.get(row.slug)
        if not mapped:
            # company 레포는 제품 문서가 없어 정상적으로 비어 있다.
            unknown += 1
            continue
        await tracked_repos_repo.patch(
            db, row.id, RepoPatch(product_slug=mapped)
        )
        filled += 1
    return {"filled": filled, "kept": skipped, "no_product": unknown}

