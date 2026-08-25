# 개요

유저가 영향 받은 것들 (책 / 인물 / 철학 / 경험) 을 입력해 나만의 AI 상담사 페르소나를 만들고, 실시간 대화로 고민을 상담하는 모바일 앱. LangGraph 로 페르소나 추출·대화 워크플로우를 구성하고, pgvector 로 영향 요소 임베딩을 관리한다. 모바일 (Expo) + 관리자 웹 (Next.js) + 백엔드 (FastAPI) + AI (LangGraph) 풀스택 모노레포. 약 한 달간 300 커밋의 빠른 사이클.

# 기술스택

**모바일 (`frontend/`)**
- React Native + **Expo (SDK 54)** — iOS/Android
- expo-router — 파일 기반 라우팅
- expo-audio + @siteed/expo-audio-studio — 음성
- 소셜 로그인 — Google / Apple / Kakao
- Firebase Analytics — 사용자 추적

**관리자 웹 (`frontend_admin/`)**
- Next.js 16 (App Router) + React 19
- TanStack Query, Tailwind CSS, Radix UI, Recharts
- @ducanh2912/next-pwa — PWA 지원

**백엔드 (`backend/`)**
- FastAPI + WebSocket
- SQLAlchemy (async) + asyncpg + Alembic
- python-jose + passlib — 인증
- Redis + **Taskiq (taskiq-redis)** — 비동기 작업 큐
- google-analytics-admin / data — GA 통계 수집

**AI**
- **LangGraph + LangChain (OpenAI)** — chat / onboarding 워크플로우
- **pgvector** — 영향 요소 임베딩 저장
- **kiwipiepy** — 한국어 형태소 분석
- tiktoken — 토큰 카운트 / 비용 관리

**인프라**
- PostgreSQL + Redis + Docker Compose
- GitHub Actions

# 주요기능

**모바일** — 단일 페이지 + tabs:

- **온보딩** — 영향 요소 입력 → AI 가 페르소나 추출 (LangGraph workflow)
- **(tabs)/index** · **history** · **mypage** — 메인 3탭
- **(auth)/login**
- **chat** — AI 페르소나와 실시간 대화 (메인 기능)
- **add-influence** — 영향 받은 책/인물/경험 추가
- **persona-settings** + edit-* (이름·아바타·음성·언어)
- **personality-report** — 추출된 성격 리포트
- **subscription-plan** — 구독
- **history-detail** — 대화 회상

**관리자 웹** (`(dashboard)/`):
- **costs / costs/sessions** — AI 비용 모니터링 (세션별)
- **errors / errors/[id]** — 에러 추적
- **stats/overview / chat / retention / subscription / onboarding** — 5종 통계 (GA + 자체)
- **plans / ideas / legal** — 구독 plan / 아이디어 백로그 / 약관 관리

**백엔드 API** (`/api/v1/`):
- **사용자** — auth, users, onboarding, persona, personality, conversation, chat, subscription, webhook, home, seed
- **관리자** — admin/legal, admin/tasks, admin/ideas, admin/plans

# 아키텍처

```
persona_counselor/
├─ frontend/         ← React Native (Expo) — 모바일 메인
├─ frontend_admin/   ← Next.js — 관리자 웹 (PWA)
├─ backend/          ← FastAPI
│  └─ app/api/v1/
│     ├─ chat.py · conversation.py · persona.py · personality.py
│     ├─ onboarding.py · subscription.py · webhook.py
│     ├─ users.py · auth.py · home.py · seed.py
│     └─ admin/     ← legal, tasks, ideas, plans
├─ docs/             ← API_DESIGN, ERD, ERROR_DESIGN, GA4_DESIGN, I18N,
│                       CHAT_LANGGRAPH, ONBOARDING_LANGGRAPH, EXTRACT_PERSONALITY 등
├─ plan/             ← 17개 plan 문서 + plans/
├─ sprint/           ← sprint 진행 추적
└─ docker-compose
```

**데이터 흐름**:

1. **온보딩** (LangGraph workflow — `docs/ONBOARDING_LANGGRAPH.md`)
   - 유저 입력 (책/인물/철학/경험) → `extract_personality` agent → 페르소나 프롬프트 + 임베딩 (pgvector) 저장

2. **대화** (LangGraph workflow — `docs/CHAT_LANGGRAPH.md`)
   - 모바일 → backend (`/api/v1/chat`) → LangGraph agent (페르소나 + 사용자 발언 + 영향 retrieval) → OpenAI → 응답 stream → 모바일

3. **비동기 작업** (Taskiq + Redis)
   - personality 추출 / 통계 집계 / GA 데이터 fetch 등 background

**외부 의존**:
- OpenAI (chat + embedding)
- Google Analytics 4 (관리자 통계)
- Firebase Analytics (모바일)

# 핵심 구현

**LangGraph workflow 2개** (`docs/CHAT_LANGGRAPH.md`, `docs/ONBOARDING_LANGGRAPH.md`):
- **onboarding** — 영향 요소 multi-input → 성격 추출 (`docs/EXTRACT_PERSONALITY.md`) → 페르소나 프롬프트 합성
- **chat** — 사용자 발언 + 페르소나 컨텍스트 + 영향 요소 retrieval (pgvector) → 응답

**비용 관리** — 관리자 `costs` 페이지 + tiktoken 으로 세션별 토큰 / USD 추적. `docs/` 에 비용 설계 문서 별도.

**i18n** — `docs/I18N.md`. 한국어/영어 다국어. expo-localization + 백엔드 응답 분기.

**GA4 통합** — `docs/GA4_DESIGN.md`. Firebase Analytics (모바일) + google-analytics-data (관리자) — 두 입력을 stats 대시보드에 통합.

**한국어 형태소 (kiwipiepy)** — 사용자 입력 분석에 활용 (정확한 사용처는 코드 확인 필요).

# 마주친 문제

> 자동 추론 결과 — 사용자 검토 필수.

- **(자동 추론)** **LangGraph workflow 설계** — `CHAT_LANGGRAPH.md` / `ONBOARDING_LANGGRAPH.md` / `EXTRACT_PERSONALITY.md` 3개 문서로 분리해 다룬 흔적. 페르소나 추출 + 유지 + retrieval 의 3축이 핵심 challenge.
- **(자동 추론)** **에러 추적 인프라** — `docs/ERROR_DESIGN.md` 별도 + 관리자 `errors` 페이지 + `errors/[id]` 상세. 에러 디버깅 인프라를 일찍 박은 결정.
- **(자동 추론)** **AI 비용 관리** — `costs/sessions` 페이지 + tiktoken — 세션별 USD 추적 인프라를 직접 만든 흔적. OpenAI 비용이 quality 에 영향 큰 도메인.
- **(자동 추론)** **GA4 + Firebase Analytics 통합** — 모바일 / 관리자 두 입력을 통합 대시보드로 — `docs/GA4_DESIGN.md` 별도.
- **(자동 추론)** **300 커밋 / 1 개월** — 빠른 반복.

# 회고

> 자동 추론 결과 — 사용자 검토·교체 필수.

- **(자동 추론)** **plan/ + sprint/ + docs/** 세 트랙 분리 — 사전 계획 (plan), 진행 추적 (sprint), 설계 문서 (docs) 의 역할 분리가 명확. 17 + 개의 plan 문서.
- **(자동 추론)** wine-log 와 같은 풀스택 4 컴포넌트 (mobile / admin / backend / ai) 구조 + Taskiq 큐는 본인 표준 패턴으로 굳어지는 중.
- **(자동 추론)** LangGraph workflow 를 설계 문서로 따로 박은 결정 — agent 흐름이 코드만으로는 추적이 어려움을 인지하고 의사결정 트레일을 별도 보존.
- **(자동 추론)** 다음에 시도한다면 — workflow visualization (LangSmith trace 활용), 페르소나 quality 정량 평가 (eval suite).
