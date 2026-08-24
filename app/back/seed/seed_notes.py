"""note 시드 — para/resources/note/ 의 md 전부를 공개 등록한다 (visible=true).

원장 144건이 옛 사이트에서 전부 공개였으므로 그대로 올린다. 숨길 것은
어드민에서 visible 을 끈다. 파일 스캔·frontmatter 파싱은 note_service 의
등록 후보 로직을 그대로 재사용한다 — 파서를 두 번 만들지 않는다.

멱등: 이미 등록된 detail_path 는 후보에서 빠지므로 재실행 시 남은 것만 넣는다.

실행:  uv run python -m seed.seed_notes
"""

from __future__ import annotations

import asyncio

from sqlalchemy import select

from core.db import SessionLocal
from models import Note, Profile
from service.note_service import note_service


async def seed() -> None:
    async with SessionLocal() as session:
        profile = (
            await session.execute(select(Profile).order_by(Profile.id).limit(1))
        ).scalar_one_or_none()
        if profile is None:
            raise SystemExit("profile 이 없다 — seed_profile 을 먼저 돌린다")

        candidates = await note_service.list_file_candidates(session)
        taken = set(
            (await session.execute(select(Note.slug))).scalars().all()
        )

        created = 0
        for c in candidates:
            slug = c.stem
            if slug in taken:
                # 폴더가 달라 stem 이 겹치면 부모 폴더명을 앞에 붙여 가른다.
                folder = c.path.split("/")[-2]
                slug = f"{folder}-{c.stem}"
            if slug in taken:
                print(f"건너뜀 — slug 충돌 해소 실패: {c.path}")
                continue
            taken.add(slug)

            session.add(
                Note(
                    profile_id=profile.id,
                    slug=slug,
                    title=c.title or c.stem,
                    summary=c.summary,
                    detail_path=c.path,
                    tags=c.tags,
                    published_on=c.date,
                    visible=True,
                )
            )
            created += 1

        await session.commit()
        print(f"note 생성 {created}건 (후보 {len(candidates)}건)")


if __name__ == "__main__":
    asyncio.run(seed())
