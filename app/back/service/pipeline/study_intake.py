"""공부 노트 접수 — `inbox/` 를 비우는 일 (KDEV-DEC-021 / KDEV-BL-007 케이스 5).

`inbox/` 는 **입구 하나**다. 사람이 노트를 넣고 push 하면 서버가 그것을 큐로 옮기고
파일을 지운다. 그래서 **파일이 남아 있다는 것은 곧 미처리**다 — 디렉토리를 보고
「이게 처리됐나」를 묻지 않아도 된다.

수집이 없다. URL 을 받아 본문을 긁어 오는 유튜브·블로그와 달리 **본문이 이미 손에
있다**. 그래서 파일 내용이 그대로 `note` 로 들어가고, `submit_preparation` 이
`source_url` 이 없을 때 메모를 원문 대신 쓰는 기존 분기를 그대로 탄다 —
`STUDY_NOTE` 정의에 `collect` 가 없는 것과 짝이다.

멱등의 자연키는 **파일명(slug)** 이다. 접수 때 파일이 사라지므로 같은 경로가 다시
나타났다는 것은 「같은 노트를 다시 넣었다」는 뜻이다. 내용 해시를 쓸 이유가 없고,
그 편이 오탈자를 고쳐 다시 넣은 경우까지 같은 항목으로 잡는다.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ITEM_PENDING_STATUSES, QueueItem

from .intake import intake

logger = logging.getLogger("kknaks-back.pipeline.study-intake")

#: 합성 키 접두. 잔디의 `daily:{날짜}` 와 같은 자리다 — URL 이 없는 입력의 중복 축.
KEY_PREFIX = "study:"

INBOX_DIRNAME = "inbox"

#: 입구를 설명하는 문서지 노트가 아니다. 함께 사는 파일이라 이름으로 가른다.
RESERVED_NAMES = {"README.md"}

#: 파일명이 곧 멱등키라 **키로 쓸 수 있는 모양**이어야 한다. 공백·따옴표가 든 이름은
#: 접수는 되겠지만 나중에 그 항목을 사람이 지목할 때 키가 애매해진다.
SLUG_RE = re.compile(r"[A-Za-z0-9가-힣][A-Za-z0-9가-힣._-]*")


@dataclass(frozen=True)
class InboxItem:
    """접수 시도 하나의 결과."""

    slug: str
    outcome: str  # created · already_queued · duplicate_published · skipped
    item_id: int | None = None
    reason: str | None = None

    @property
    def consumed(self) -> bool:
        """파일을 지웠는가.

        지운다 = 「이건 큐가 갖고 있다」. 안 지운다 = 「아직 아무도 안 받았다」.
        입구가 비어 있는지로 미처리를 판별하므로 이 둘이 어긋나면 안 된다.
        """
        return self.outcome in ("created", "already_queued")


@dataclass
class ScanResult:
    items: list[InboxItem] = field(default_factory=list)

    @property
    def created_ids(self) -> list[int]:
        return [i.item_id for i in self.items if i.outcome == "created" and i.item_id]

    def summary(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.items:
            counts[item.outcome] = counts.get(item.outcome, 0) + 1
        return counts


def synthetic_key(slug: str) -> str:
    return f"{KEY_PREFIX}{slug}"


def inbox_files(repo_root: Path) -> list[Path]:
    """입구의 노트들. **최상위 `*.md` 만** 본다.

    하위 디렉토리를 훑지 않는 것은 `inbox/_restored/` 같은 작업용 더미가 통째로
    접수되는 사고를 막기 위해서다. 입구에 넣는다는 것은 **파일을 거기 놓는다**는
    뜻이지 폴더를 통째로 던진다는 뜻이 아니다.
    """
    inbox = repo_root / INBOX_DIRNAME
    if not inbox.is_dir():
        return []
    return sorted(
        p for p in inbox.glob("*.md") if p.is_file() and p.name not in RESERVED_NAMES
    )


def read_note(path: Path) -> tuple[str, str | None]:
    """본문과 제목. frontmatter 는 벗겨 낸다.

    입구의 파일은 `type: idea` 를 갖는다(DEC-021 D3). 그 키들은 **그래프용 값**이라
    요약 프롬프트에 들어가면 잡음이다. 다만 `title` 은 사람이 붙인 주제라 살린다 —
    본문이 제목 없이 시작하는 노트가 흔하다.
    """
    try:
        post = frontmatter.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 — 못 읽는 파일은 건너뛴다
        logger.warning("inbox/%s 를 파싱하지 못했다 — %s", path.name, exc)
        return "", None

    title = str(post.metadata.get("title") or "").strip() or None
    body = post.content.strip()
    if title and not body.startswith("#"):
        body = f"# {title}\n\n{body}"
    return body, title


async def _pending_item(db: AsyncSession, key: str) -> QueueItem | None:
    return await db.scalar(
        select(QueueItem)
        .where(
            QueueItem.normalized_url == key,
            QueueItem.deleted_at.is_(None),
            QueueItem.status.in_(ITEM_PENDING_STATUSES),
        )
        .limit(1)
    )


async def intake_inbox(
    db: AsyncSession,
    *,
    repo_root: Path,
    channel: str = "inbox",
    submitted_by: str | None = None,
    delete: bool = True,
) -> ScanResult:
    """입구를 훑어 접수하고 비운다. 커밋은 호출자가 한다.

    결과가 넷이고 **파일을 지우는가**가 둘로 갈린다.

        created             새 항목. 지운다
        already_queued      큐가 이미 갖고 있다. 지운다 — 두 번 접수하지 않는다
        duplicate_published 이미 발행된 slug. **안 지운다**
        skipped             빈 파일·이상한 이름. **안 지운다**

    `already_queued` 를 `intake()` 의 합류에 맡기지 않고 먼저 조회해 끊는 이유는
    합류가 **메모를 덧붙이기** 때문이다. 노트 본문이 통째로 메모라 덧붙이면 같은
    글이 두 번 들어간 입력이 요약으로 간다. 이 경로에서는 「이미 있으면 손대지
    않는다」가 맞다.

    지우지 않는 둘은 **사람이 봐야 하는 상태**다. 입구에 남아 있는 것 자체가 그
    신호다 — 조용히 지우면 발행된 노트를 다시 정리하려던 의도가 사라진다.
    """
    result = ScanResult()

    for path in inbox_files(repo_root):
        slug = path.stem
        if not SLUG_RE.fullmatch(slug):
            logger.warning("inbox/%s — 파일명이 키로 쓸 수 없는 모양이다", path.name)
            result.items.append(
                InboxItem(slug=slug, outcome="skipped", reason="INVALID_SLUG")
            )
            continue

        body, _title = read_note(path)
        if not body:
            # 본문이 없으면 요약할 것이 없다. 항목을 만들어 `NO_SOURCE_MATERIAL` 로
            # 실패시키느니 입구에 둔 채 알린다 — 실패 항목은 사람이 지워야 한다.
            logger.warning("inbox/%s — 본문이 비어 접수하지 않는다", path.name)
            result.items.append(
                InboxItem(slug=slug, outcome="skipped", reason="EMPTY_NOTE")
            )
            continue

        key = synthetic_key(slug)
        pending = await _pending_item(db, key)
        if pending is not None:
            logger.info("inbox/%s — item=%s 로 이미 큐에 있다", path.name, pending.id)
            result.items.append(
                InboxItem(slug=slug, outcome="already_queued", item_id=pending.id)
            )
            if delete:
                path.unlink()
            continue

        outcome = await intake(
            db,
            note=body,
            channel=channel,
            submitted_by=submitted_by,
            source_kind="study_note",
            normalized_key=key,
        )
        if outcome.outcome == "duplicate_published":
            logger.warning(
                "inbox/%s — 같은 slug 가 item=%s 로 이미 발행됐다. 입구에 남긴다",
                path.name,
                outcome.existing_item_id,
            )
            result.items.append(
                InboxItem(
                    slug=slug,
                    outcome="duplicate_published",
                    item_id=outcome.existing_item_id,
                    reason="ALREADY_PUBLISHED",
                )
            )
            continue

        result.items.append(
            InboxItem(slug=slug, outcome="created", item_id=outcome.item_id)
        )
        if delete:
            path.unlink()

    return result


async def run_inbox_scan() -> dict:
    """부팅 시 한 번 도는 접수 (DEC-021 D1).

    스케줄이 아니라 **시작 프로세스**인 이유는 트리거가 push 이기 때문이다. 노트를
    넣고 push 하면 배포가 돌고 서버가 다시 뜬다 — 그 시점이 곧 「새 노트가 왔다」다.

    예외를 밖으로 내보내지 않는다. 입구가 비어 있는 것이 보통이고, 여기서 터지면
    **콘텐츠 API 와 무관한 이유로 부팅이 막힌다** — `seed_admin` 이 DB 미가용에
    로그만 남기는 것과 같은 판단이다.
    """
    import config
    from core.db import new_session

    from .runtime import follow

    try:
        async with new_session() as db:
            result = await intake_inbox(db, repo_root=config.repo_root())
            await db.commit()
    except Exception as exc:  # noqa: BLE001
        logger.warning("inbox 스캔 실패 — %s: %s", type(exc).__name__, exc)
        return {"error": f"{type(exc).__name__}"}

    if result.items:
        logger.info("inbox 스캔 — %s", result.summary())

    # 커밋 **뒤**에 민다. 드라이버가 다른 세션으로 이 항목들을 읽는다.
    for item_id in result.created_ids:
        try:
            await follow(item_id)
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "inbox 접수 후 드라이버 기동 실패 item=%s — %s: %s",
                item_id,
                type(exc).__name__,
                exc,
            )
    return result.summary()
