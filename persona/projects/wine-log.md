---
type: project
id: P-03
title:
  ko: "Wine Log"
  en: "Wine Log"
summary:
  ko: "와인 기록·관리 모바일 앱 + 관리자 웹 + AI 라벨 분석 서버"
  en: "Wine logging mobile app with admin web & AI label-analysis server"
category: mobile
status: live
date: "2026.02"
stack:
  - FastAPI
  - React Native
  - Expo
  - Next.js
  - Postgres
  - pgvector
  - LangGraph
  - Dramatiq
  - Redis
  - Docker
visible: true
thumbnail: /assets/projects/P-03/cover.png
links:
  repo: "github.com/kknaks/wine_log"
# 포트폴리오 PDF 케이스 스터디 (planning-02 §3.3) — 비면 PDF 에 미표시.
problem:
  ko: ""
  en: ""
approach:
  ko: []
  en: []
impact:
  ko: []
  en: []
learnings:
  ko: []
  en: []
troubles: []
---

# 개요

와인을 기록·관리하는 모바일 앱. 사용자는 와인 라벨을 카메라로 촬영해 데이터베이스에 등록하고, 시음 다이어리 (바디·타닌·산도·당도·알콜 + 아로마/맛/피니쉬 태그) 를 남긴다. 백엔드는 FastAPI + Postgres (pgvector) 로 사용자 취향과 와인 임베딩을 저장하고, AI 서버 (LangGraph MCP) 가 라벨 OCR + 와인 정보 enrich + 추천을 비동기 처리한다. 관리자 웹 (Next.js) 으로 와인/배너/문의/통계를 운영한다.

# 기술스택

**모바일 (`frontend/`)**
- React Native + **Expo (SDK 54)** — iOS/Android 단일 코드베이스, OTA 업데이트
- expo-router — 파일 기반 라우팅 + tabs 네비게이션
- expo-camera + expo-image-picker — 라벨 촬영 / 갤러리 업로드
- 소셜 로그인 — Google / Apple / Kakao (`@react-native-google-signin`, `expo-apple-authentication`, `@react-native-seoul/kakao-login`)
- Firebase Analytics — 앱 사용 추적

**관리자 웹 (`frontend_admin/`)**
- Next.js 16 (App Router) + React 19
- TanStack Query — 서버 상태
- Zustand — 클라이언트 상태
- TipTap — rich text editor (배너 / 약관)
- Tailwind CSS + Radix UI
- Recharts — 통계 차트

**백엔드 (`backend/`)**
- FastAPI + SQLAlchemy (async) + asyncpg + Alembic
- Pydantic v2 — 검증 / 설정
- python-jose + bcrypt + pyjwt — 인증
- Dramatiq + Redis — 비동기 작업 큐 (이미지 업로드 후처리, 크롤링)
- BeautifulSoup + lxml + requests — 와인 정보 크롤링
- Pillow + opencv-python-headless — 이미지 처리
- pgvector — 벡터 검색
- google-analytics-data — GA 통계 fetch

**AI (`ai/`)**
- LangGraph + LangChain (OpenAI / Google GenAI) — agent workflow
- MCP (Model Context Protocol) — 와인 라벨 분석 server
- LangSmith — 관측 / 디버깅
- Dramatiq + Redis — backend 와 동일 큐 공유 (비동기 enrich)

**DB / 인프라**
- PostgreSQL 16 + pgvector (`pgvector/pgvector:pg16`)
- Redis 7
- Docker Compose — 로컬 dev + prod 분리 (`docker-compose.yml` / `docker-compose.prod.yml`)
- GitHub Actions — CI/CD

# 주요기능

**모바일 (Expo)** — `(tabs)` 5탭 + 상세

- **홈** (`(tabs)/index`) — 추천 와인 + 최근 다이어리 피드
- **발견** (`(tabs)/discover`) — 와인 검색·둘러보기
- **추가** (`(tabs)/add`) — 카메라로 와인 라벨 촬영 → AI 분석 트리거
- **다이어리** (`(tabs)/diary`) — 본인 시음 기록 list
- **마이페이지** (`(tabs)/my`) — 프로필 / 설정
- **와인 상세** (`/wine/[id]`) — 와인 정보 + 관련 다이어리
- **다이어리 상세 / 작성 / 수정** (`/diary/[id]`, `/diary/new`, `/diary/edit`)
- **공지사항** (`/notices/`) · **1:1 문의** (`/inquiry/`)
- **설정** (`/settings/nickname`) · **로그인** (`/login`)

**관리자 웹 (Next.js)** — `(dashboard)` 그룹

- **다이어리 관리** (`/diaries`) — 사용자 다이어리 모니터
- **와인 관리** (`/wines`) + 크롤러 (`/wines/crawler`) — Vivino 등 외부 사이트 크롤링
- **문의 응답** (`/inquiries/answer`)
- **배너 관리** (`/banners`, `/banners/new`)
- **사용자 관리** (`/users`)
- **약관 관리** (`/legal`)
- **통계** (`/stats/diaries`, `/stats/wines`, `/stats/recommendation`) — GA + 자체 메트릭

**백엔드 API** (`/api/v1/`) — auth, users, wines, diaries, banners, home, recommendations, feed, inquiries, legal + 관리자 admin_*

# 아키텍처

```
wine_log/
├─ frontend/         ← React Native (Expo) — iOS/Android 모바일 앱
├─ frontend_admin/   ← Next.js — 관리자 웹
├─ backend/          ← FastAPI — REST API + 인증 + 비동기 작업 발행
│  ├─ app/api/v1/    ← 라우터 20+개 (사용자 + 관리자)
│  ├─ app/models/    ← SQLAlchemy 모델 (users, wines, diaries, tags, vectors)
│  ├─ app/services/  ← 비즈니스 로직
│  └─ alembic/       ← DB migration
├─ ai/               ← LangGraph MCP server — 와인 라벨 OCR + enrich + 추천
├─ docs/             ← 설계 문서 (PROJECT_PLAN, DIARY_FLOW, SOCIAL_LOGIN_PLAN 등)
├─ scripts/          ← 운영 스크립트
├─ docker-compose.yml          ← dev (db, redis, backend, ai-worker)
└─ docker-compose.prod.yml     ← prod
```

**데이터 흐름**:

1. 모바일 → 라벨 촬영 → 이미지 업로드 (`POST /api/v1/wines`)
2. 백엔드 → 이미지 저장 + Dramatiq 작업 발행 (Redis enqueue)
3. AI worker → 큐 consume → LangGraph agent (OCR → 와인 정보 검색 → embedding 생성)
4. AI worker → DB 직접 write (와인 정보 + `wine_vectors`)
5. 모바일 → polling 또는 push 알림으로 enrich 완료 확인
6. 추천 — 사용자 `user_vectors` ↔ `wine_vectors` 코사인 유사도 (pgvector)

**DB 스키마 (CLAUDE.md §Database Schema)**:
- `users` 1:N `diaries` · 1:1 `user_vectors`
- `wines` 1:N `diaries` · 1:1 `wine_vectors`
- `wines` N:M `tags` (via `wine_tags`)
- `diaries` N:M `tags` (via `diary_tags`)
- 모든 테이블에 `id (BIGINT PK)` + `created_at` + `updated_at` (BaseModel)

**외부 의존**:
- OpenAI / Google GenAI (LangChain)
- Google Analytics (관리자 통계)
- Firebase Analytics (모바일)
- 외부 와인 사이트 (Vivino 등) — 크롤러

# 핵심 구현

**백엔드 API 라우터 (`backend/app/api/v1/`)** — 20+ 엔드포인트, 사용자 + 관리자 분리:

```
auth.py             ← 소셜 로그인 (Google/Apple/Kakao) — 6 endpoints
users.py            ← 프로필 CRUD, 탈퇴
wines.py            ← 와인 등록 (이미지) + 조회 + 검색
diaries.py          ← 다이어리 CRUD + 태그 연결
recommendations.py  ← pgvector 기반 추천
feed.py · home.py   ← 메인 피드
banners.py          ← 사용자용 배너 / 공지
inquiries.py        ← 1:1 문의
legal.py            ← 약관

admin_*.py          ← 관리자 — banner / legal / crawler / ga / inquiry / stats / upload
```

응답은 `SuccessResponse[T]` 통일 형식.

**AI MCP server (`ai/`)** — LangGraph workflow:
- 와인 라벨 OCR → Vivino 등 외부 검색 → 정보 enrich → embedding 생성 → DB write
- Dramatiq actor 가 backend 의 작업 큐를 consume
- LangSmith 로 trace

**모바일 인증** (`frontend/`):
- expo-secure-store 에 token 저장
- (tabs) 진입 전 `_layout.tsx` 가 로그인 체크 후 `/login` 리다이렉트

# 마주친 문제

> 자동 추론 결과 — 사용자 검토 필수.

- **(자동 추론)** 카메라 포커스 — `git log` 에 "카메라 포커스 개선 및 Android 설정" 커밋. iOS/Android 카메라 동작 차이 + 라벨 인식 정확도 튜닝.
- **(자동 추론)** 관리자 패키지 API 정합 — `fix/admin package api` 커밋. 관리자 라우트 분리 시 발생한 path/스키마 mismatch.
- **(자동 추론)** 비동기 작업 큐 운영 — backend 와 ai 컨테이너가 같은 Redis 를 공유. 작업 멱등성 + 실패 재시도 처리가 핵심 challenge 였을 가능성.
- **(자동 추론)** pgvector 인덱스 튜닝 — 사용자 취향 ↔ 와인 임베딩 검색 성능. (확인 필요)

# 회고

> 자동 추론 결과 — 사용자 검토·교체 필수.

- **(자동 추론)** 4개 컴포넌트 (mobile / admin / backend / ai) 를 모노레포로 묶은 결정 — 작업량은 크지만 데이터 모델 / 환경 변수 / Docker compose 공유로 운영 부담은 줄음.
- **(자동 추론)** AI 컴포넌트를 LangGraph + MCP 로 분리한 것 — 백엔드와 큐로 디커플링되어 모델 교체 / 워크플로우 변경 부담이 적음.
- **(자동 추론)** 다음에 시도한다면 — embedding 모델 선택 vs 벡터 DB 별도 분리 (Qdrant / Weaviate) 비교, 추천 알고리즘 A/B 테스트 인프라.
