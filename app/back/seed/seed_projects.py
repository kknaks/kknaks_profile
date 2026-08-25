"""project 시드 — 2026-08-25 실 DB 상태를 값으로 박는다.

원래는 showcase.md frontmatter 를 파싱했지만, 같은 날 frontmatter 를 9건 전부
제거했다(메타 SoT 는 DB — templates/projects/showcase.md 참조). 그래서 이제
원료가 md 가 아니라 **어드민이 관리하는 DB 그 자체**이고, 시드는 그 시점 상태의
스냅샷이다. showcase.md 는 본문(# 개요 …)만 갖고 detail_path 로 가리킨다.

- title·summary 는 한국어 하나(database.md 서두).
- links 는 표시 전용 — 잔디가 긁는 레포는 repo 표(seed_repos)가 소유한다.
- visible 은 어드민에서 정한 실값 그대로.
- profile_id 는 첫 profile 행 — 1인 사이트다.

멱등 upsert(slug 기준): 없으면 넣고, 있으면 시드 값으로 덮어쓴다.
재실행이 값을 안 되돌린다 — 시드 값이 곧 현 DB 값이라서다.

실행:  uv run python -m seed.seed_projects
"""

from __future__ import annotations

import asyncio
from datetime import date

from sqlalchemy import select

from core.db import SessionLocal
from models import Profile, Project

_DETAIL = "para/projects/summer-star/{slug}/showcase.md"
_COVER = "para/projects/summer-star/{slug}/assets/cover.png"

PROJECTS: list[dict] = [
    {
        "slug": "kknaks-dev",
        "title": "kknaks.dev",
        "summary": (
            "본 포트폴리오 사이트 — 페르소나 시스템 (md SoT) + "
            "자동 enrich 잡 (open-kknaks dogfooding)"
        ),
        "category": "web",
        "status": "wip",
        "started_on": date(2026, 5, 1),
        "stack": [
            "Next.js", "React", "FastAPI", "Python",
            "open-kknaks", "Redis", "APScheduler", "Docker",
        ],
        "thumbnail": _COVER.format(slug="kknaks-dev"),
        "links": {"repo": "github.com/kknaks/kknaks_profile"},
        "visible": False,
    },
    {
        "slug": "language-diary",
        "title": "Language Diary",
        "summary": "AI 와 음성 대화로 일기를 만들고 영어 학습 포인트를 제공하는 모바일 앱",
        "category": "mobile",
        "status": "wip",
        "started_on": date(2026, 2, 1),
        "stack": [
            "FastAPI", "React Native", "Expo", "Postgres", "Redis",
            "WebSocket", "OpenAI", "ElevenLabs", "Docker",
        ],
        "thumbnail": _COVER.format(slug="language-diary"),
        "links": {"repo": "github.com/kknaks/language_diary"},
        "visible": False,
    },
    {
        "slug": "mac-remote",
        "title": "DeskDeck",
        "summary": "iPhone을 Mac 리모컨으로 쓰는 앱",
        "category": "mobile",
        "status": "live",
        "started_on": None,
        "stack": ["Swift", "SwiftUI"],
        "thumbnail": None,
        "links": None,
        "visible": True,
    },
    {
        "slug": "mykakao",
        "title": "mykakao",
        "summary": (
            "카카오톡 대화를 내보내기 없이 로컬에서 자동 추출(SQLCipher DB 복호화). "
            "추출 확인용 웹 데모(실시간 SSE) 완성. 향후 일정 파싱 → 캘린더 출력 단계 예정."
        ),
        "category": "backend",
        "status": "wip",
        "started_on": date(2026, 6, 1),
        "stack": None,
        "thumbnail": None,
        "links": {"repo": "github.com/kknaksss/mykakao"},
        "visible": True,
    },
    {
        "slug": "open-kknaks",
        "title": "open-kknaks",
        "summary": "PTY 기반 Claude Code CLI 태스크 큐 라이브러리 + MCP 서버",
        "category": "cli",
        "status": "live",
        "started_on": date(2026, 3, 1),
        "stack": ["Python", "Redis", "MCP", "Pydantic", "Typer", "structlog"],
        "thumbnail": _COVER.format(slug="open-kknaks"),
        "links": {"repo": "github.com/kknaks/open_kknaks"},
        "visible": True,
    },
    {
        "slug": "persona-counselor",
        "title": "Persona Counselor",
        "summary": "영향 받은 책·인물·철학으로 AI 상담사 페르소나를 만들고 실시간 대화하는 앱",
        "category": "mobile",
        "status": "wip",
        "started_on": date(2026, 3, 1),
        "stack": [
            "FastAPI", "React Native", "Expo", "Next.js", "Postgres", "pgvector",
            "Redis", "LangGraph", "LangChain", "OpenAI", "Taskiq", "Docker",
        ],
        "thumbnail": _COVER.format(slug="persona-counselor"),
        "links": {"repo": "github.com/kknaks/persona_counselor"},
        "visible": False,
    },
    {
        "slug": "study-timelapse",
        "title": "Study Timelapse",
        "summary": (
            "공부하는 모습을 카메라로 녹화 → 자동 타임랩스 영상 생성. "
            "iOS 앱 (Expo + native AVFoundation) + FastAPI 백엔드."
        ),
        "category": "mobile",
        "status": "wip",
        "started_on": date(2026, 2, 1),
        "stack": [
            "React Native", "Expo", "TypeScript", "FastAPI", "Python",
            "Postgres", "FFmpeg", "AVFoundation",
        ],
        "thumbnail": _COVER.format(slug="study-timelapse"),
        "links": {"repo": "github.com/kknaks/study_timelapse"},
        "visible": False,
    },
    {
        "slug": "summer-star-company",
        "title": "Summer Star — 사무실 NFC 출퇴근",
        "summary": (
            "NFC 카드로 사무실 출퇴근 자동 트래킹. "
            "Next.js 어드민 + FastAPI + Pi NFC 에이전트 4 컴포넌트."
        ),
        "category": "web",
        "status": "wip",
        "started_on": date(2026, 4, 1),
        "stack": [
            "Next.js", "React", "TypeScript", "Tailwind CSS", "FastAPI", "Python",
            "SQLAlchemy", "Alembic", "Postgres", "pyscard", "Docker", "Raspberry Pi",
        ],
        "thumbnail": None,
        "links": {"repo": "github.com/kknaks/summer_star_company"},
        "visible": True,
    },
    {
        "slug": "wine-log",
        "title": "Wine Log",
        "summary": "와인 기록·관리 모바일 앱 + 관리자 웹 + AI 라벨 분석 서버",
        "category": "mobile",
        "status": "live",
        "started_on": date(2026, 2, 1),
        "stack": [
            "FastAPI", "React Native", "Expo", "Next.js", "Postgres",
            "pgvector", "LangGraph", "Dramatiq", "Redis", "Docker",
        ],
        "thumbnail": _COVER.format(slug="wine-log"),
        "links": {"repo": "github.com/kknaks/wine_log"},
        "visible": True,
    },
]


async def seed() -> None:
    async with SessionLocal() as session:
        profile = (
            await session.execute(select(Profile).order_by(Profile.id).limit(1))
        ).scalar_one_or_none()
        if profile is None:
            raise SystemExit("profile 이 없다 — seed_profile 을 먼저 돌린다")

        for fields in PROJECTS:
            fields = {
                **fields,
                "detail_path": _DETAIL.format(slug=fields["slug"]),
                "profile_id": profile.id,
            }
            row = (
                await session.execute(
                    select(Project).where(Project.slug == fields["slug"])
                )
            ).scalar_one_or_none()
            if row is None:
                session.add(Project(**fields))
                print(f"project 생성 — {fields['slug']} (visible={fields['visible']})")
            else:
                for key, value in fields.items():
                    setattr(row, key, value)
                print(f"project 갱신 — {fields['slug']} (visible={fields['visible']})")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
