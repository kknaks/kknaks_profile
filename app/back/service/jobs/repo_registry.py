"""레포 레지스트리 — 조회와 1회 시드 (KDEV-WORK-017 P5 / KDEV-SPEC-011).

시드는 `products/*/showcase.md` 에서 **한 번만** 긁어 온다. 그 뒤로는 레지스트리가
SoT 이고 showcase 는 공개 표시용으로 돌아간다 — 둘을 계속 동기화하면 "보여줄 레포와
긁을 레포를 분리한다" 는 목적이 무의미해진다.

`detail`(career 귀속)은 시드가 채우지 않는다. showcase 에 그 정보가 없고, 어느 career
문서로 갈지는 사람이 정할 일이라 자동으로 지어내면 조용히 틀린다. `company` 레포는
시드 후 손으로 채운다.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

import frontmatter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import TrackedRepo

logger = logging.getLogger("kknaks-back.repo-registry")

#: `github.com/owner/name` · `https://github.com/owner/name` 어느 쪽이든 받는다.
_SLUG_RE = re.compile(r"(?:https?://)?(?:www\.)?github\.com/([^/\s]+/[^/\s#?]+)")

#: 개인 계정 둘 — 어느 쪽이든 personal 토큰으로 클론한다.
PERSONAL_OWNERS = ("kknaks", "kknaksss")


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

    `company` 는 `detail` 이 필수인데 showcase 에 그 정보가 없다. DB 제약이 막으므로
    **`studio` 만 넣고 `company` 는 건너뛴 뒤 수를 돌려준다** — 사람이 채워야 할 것이
    몇 건인지 알아야 한다.
    """
    existing = set(
        (await db.scalars(select(TrackedRepo.slug))).all()
    )
    added = skipped_company = 0
    for entry in scan_showcase(repo_root):
        if entry.slug in existing:
            continue
        if entry.type == "company":
            # detail 을 지어내지 않는다 — 어느 career 로 갈지는 사람이 정한다.
            skipped_company += 1
            logger.info("company 레포는 detail 이 필요해 건너뛴다 — %s", entry.slug)
            continue
        db.add(
            TrackedRepo(
                slug=entry.slug, type=entry.type, account=entry.account, enabled=True
            )
        )
        added += 1
    await db.flush()
    return {"added": added, "needs_detail": skipped_company, "existing": len(existing)}


async def enabled_repos(db: AsyncSession) -> list[TrackedRepo]:
    """조사 대상. `enabled` 가 꺼진 것은 클론을 남긴 채 fetch 만 멈춘다."""
    return list(
        (
            await db.scalars(
                select(TrackedRepo)
                .where(TrackedRepo.enabled.is_(True))
                .order_by(TrackedRepo.slug)
            )
        ).all()
    )
