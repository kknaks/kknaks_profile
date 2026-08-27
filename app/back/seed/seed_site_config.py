"""site_config 시드 — 사이트에 뜨는 문구 전부. 키 목록은 erd.md §site_config 가 정본.

원료는 _archive/persona/profile.md + _meta.yaml (ko 값만).

멱등 upsert: 키가 없으면 넣고, 있으면 시드 값으로 덮어쓴다.
2026-08-25 실 DB 상태로 동기 — 어드민에서 고친 about.cards 를 반영했다.
재실행이 값을 안 되돌린다.

실행:  uv run python -m seed.seed_site_config
"""

from __future__ import annotations

import asyncio
from typing import Any

from core.db import SessionLocal
from models import SiteConfig

# (key, value, note)
SEED: list[tuple[str, Any, str]] = [
    (
        "home.hero_headline",
        [
            {"text": "안녕하세요!", "tone": "muted"},
            {"text": "새로운 아이디어로", "tone": "default"},
            {"text": "도전하며 제품을 만드는", "tone": "default"},
            {"text": "백엔드 개발자입니다.", "tone": "accent"},
        ],
        "home 히어로 — [{text, tone}]",
    ),
    (
        "home.hero_subline",
        "풀스택 엔지니어. 백엔드부터 인프라까지 직접 손대는 게 즐겁습니다.",
        "home 히어로 아래 한 줄",
    ),
    (
        "home.hero_terminal",
        [
            {"prompt": "whoami", "output": ["kknaks · backend engineer · seoul, kr"]},
            {
                "prompt": "cat stack.txt",
                "output": [
                    "frontend → Next.js · TypeScript",
                    "mobile   → React Native · Expo",
                    "backend  → FastAPI · Python · Postgres",
                    "ai       → LangGraph · OpenAI · pgvector",
                    "infra    → Docker · Linux · nginx",
                ],
            },
            {
                "prompt": "wc -l ~/career/**/*.md",
                "output": [
                    "메디솔브 AI · 백엔드 개발자",
                    "퀀터스 · 백엔드 개발자",
                    "도화 엔지니어링 · 토목 설계",
                ],
            },
            {
                "prompt": "ls ~/product/now",
                "output": [
                    "kknaks.dev          · This Site",
                    "Wine.Log            · iOS/Android App",
                    "Persona.Counselor   · iOS/Android App",
                    "open-kknaks         · CLI · MCP",
                ],
            },
        ],
        "home 터미널 연출 — [{prompt, output[]}]",
    ),
    (
        "about.tagline",
        "호기심으로 시작해서, 도전으로 만들고, 개발로 풀어냅니다.",
        "/about 한 줄 소개",
    ),
    (
        "about.intro",
        "저는 새로운 것을 도전하고 직접 만들어 보는 걸 좋아합니다. "
        "CS를 늦게 시작했지만, 매일의 학습을 코드와 노트로 남기며 배운 것을 "
        "조금씩 넓혀가고 있습니다.",
        "/about 소개 1문단",
    ),
    (
        "about.intro2",
        "지금은 AI 회사에서 피부과 전용 CRM·MSO 의 백엔드와 사내 하네스 "
        "엔지니어링을 맡고 있습니다. 제품을 만들면서 동시에 AI 가 규칙 안에서 "
        "일하도록 도구까지 함께 만들 수 있어 매일이 새롭습니다.",
        "/about 소개 2문단 — 지금 하는 일",
    ),
    (
        # 어드민에서 고친 실값(2026-08-25) — 시드는 그 상태를 재현한다
        "about.cards",
        [
            {
                "title": "지금 일하는 곳",
                "body": "AI 회사에서 피부과 AI서비스 구축과 AX리더로 사내 및 고객사 AX전환 사업을 맡고 있습니다.",
            },
            {
                "title": "만들고 있는 것",
                "body": "홈서버에서 직접 호스팅하는 작은 포트폴리오 사이트. AI를 활용한 툴, 제품",
            },
            {
                "title": "관심 있는 기술",
                "body": "LLM·RAG·벡터 DB 같은 AI 인프라. Loop Engineering 같은 LLM 기반 자동화 구조",
            },
            {
                "title": "일하는 방식",
                "body": "문서로 기획, 스펙을 작성하고 코드로 풀어냅니다.",
            },
        ],
        "/about 카드 4개 — [{title, body}]",
    ),
    (
        "footer.tagline",
        "홈서버에서 직접 호스팅하는 작은 포트폴리오.",
        "footer 한 줄",
    ),
]


async def seed() -> None:
    async with SessionLocal() as session:
        for key, value, note in SEED:
            row = await session.get(SiteConfig, key)
            if row is None:
                session.add(SiteConfig(key=key, value=value, note=note))
                print(f"생성 — {key}")
            else:
                row.value = value
                row.note = note
                print(f"갱신 — {key}")
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
