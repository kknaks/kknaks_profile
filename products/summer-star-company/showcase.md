---
type: project
id: P-11
org: studio
title:
  ko: "Summer Star — 사무실 NFC 출퇴근"
  en: "Summer Star — Office NFC Attendance"
summary:
  ko: "NFC 카드로 사무실 출퇴근 자동 트래킹. Next.js 어드민 + FastAPI + Pi NFC 에이전트 4 컴포넌트."
  en: "Auto attendance tracking via NFC cards. Next.js admin + FastAPI + Pi NFC agent (4 components)."
category: web
status: wip
date: "2026.04"
stack:
  - Next.js
  - React
  - TypeScript
  - Tailwind CSS
  - FastAPI
  - Python
  - SQLAlchemy
  - Alembic
  - Postgres
  - pyscard
  - Docker
  - Raspberry Pi
visible: false
thumbnail:
links:
  repo: "github.com/kknaks/summer_star_company"
  live: ""
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

NFC 카드 기반 사무실 출퇴근 트래킹 시스템. **개인 사무실용** (admin 1명 + 직원 소수, 리더기 1대) — 멀티테넌트/SaaS 아님, RBAC·조직 모델·OTA 배포 같은 기업용 패턴은 명시적으로 도입 금지.

ACR122U USB 리더기를 라즈베리파이 (Orange Pi Zero 3) 에 꽂아 NFC 카드를 감시하는 Python 에이전트 + FastAPI 백엔드 (Postgres) + Next.js 관리자 웹의 4 컴포넌트 구조.

# 기술스택

**Frontend (admin)**
- Next.js 16 + React 19 + TypeScript 5
- Tailwind CSS v4 + Radix UI Slot + class-variance-authority + lucide-react
- axios — 백엔드 호출
- Vercel 배포 가정 (port 43000 — 사내 한정)

**Agent (Pi)**
- Python 3.12 + uv
- `pyscard` — PC/SC 인터페이스 (ACR122U 리더기)
- `httpx` — 백엔드 push
- `pydantic-settings` — config
- systemd 서비스 등록 (`agent/systemd/`)

**Backend**
- FastAPI 0.115 (standard) + SQLAlchemy 2 (asyncio) + asyncpg
- Alembic 마이그레이션
- `bcrypt` (passlib) + PyJWT — 관리자 인증 (JWT 30일 + localStorage, sessions 테이블 없음 = stateless)
- `pyscard` — 등록 리더(#2) PC/SC 인터페이스 (백엔드도 카드 등록 시점에 직접 읽음)
- 4 계층 (api/services/repos/models)

**인증 / 보안**
- 관리자 웹: 비밀번호 → JWT 30일 (stateless)
- 에이전트 → 백엔드: 정적 API 키 (`X-Agent-Key` 헤더)
- OAuth/세션쿠키 사용 안 함

**인프라 / 배포**
- Postgres (집 서버 자호스팅, Docker)
- `docker-compose.yml` + `docker-compose.prod.yml`
- Pi 에 systemd 로 agent 데몬 등록

# 주요기능

- **카드 등록** (`/users` + `cards` API) — 등록 리더(#2) 로 카드 UID 읽음 → 사용자 1:1 매핑. UID 직접 입력도 지원 (최근 commit `34fe129`)
- **출입 감시** — Pi 의 NFC agent 가 카드 태그 감시 → 백엔드 `/access` 로 push
- **출퇴근 해석** — KST 04:00 컷오프 기준 출/퇴근 (`domain/access-log`)
- **로그 뷰** (`/logs`) — 출입 이벤트 시계열
- **통계 대시보드** (`/stats`) — 출퇴근 집계
- **관리자 로그인** (`/login`) — 비밀번호 → JWT

# 아키텍처

```
[ACR122U] ─USB─ [Pi: Python Agent] ─HTTP─> [FastAPI Backend] ─SQL─> [Postgres]
                                                  ↑
                                          [Next.js 관리자 웹]
```

```
summer_star_company/
├─ backend/                      ← FastAPI (4계층)
│  ├─ app/
│  │  ├─ api/                    ← access · auth · cards · logs · stats · users
│  │  ├─ services/               ← *_service.py (auth/access/card/log/stats/user) + card_reader
│  │  ├─ repos/                  ← DB 접근
│  │  ├─ db/                     ← models, base
│  │  ├─ schemas/                ← Pydantic
│  │  └─ dtos/                   ← API DTO
│  ├─ alembic/                   ← 마이그레이션
│  └─ Dockerfile
├─ admin/                        ← Next.js 어드민 (Vercel)
│  ├─ app/
│  │  ├─ login/                  ← 비밀번호 → JWT
│  │  └─ (authed)/               ← logs · stats · users
│  ├─ components/  lib/
│  └─ package.json (next 16, react 19, tailwind v4)
├─ agent/                        ← Pi NFC 에이전트
│  ├─ nfc_agent/                 ← reader · client · feedback · main
│  ├─ systemd/                   ← Pi 서비스 유닛
│  └─ Dockerfile
├─ docs/                         ← MAP.md 진입점, architecture/domain/spec/plan/conventions
└─ docker-compose.yml + .prod.yml
```

**도메인 모델**: `User` (admin/직원) — `Card` (UID 정규화, 1:1 사용자) — `AccessLog` (이벤트 시계열, KST 04:00 컷오프 출/퇴근 해석).

**SSOT 룰** (CLAUDE.md):
- 도메인 결정 → `docs/domain/*`
- 컴포넌트 구현 → `docs/spec/*`
- 크로스컷팅 (인증/보안/네트워크) → `docs/architecture/*`

# 핵심 구현

**Backend API** (`backend/app/api/`):
- `auth.py` — 비밀번호 → JWT 30일
- `users.py` — 직원 등록/조회
- `cards.py` — NFC 카드 등록 (등록 리더로 UID 캡처) + UID 직접 입력
- `access.py` — agent → 백엔드 카드 태그 push (`X-Agent-Key` 헤더 인증)
- `logs.py` — 출입 이벤트 조회
- `stats.py` — 출퇴근 집계

**Agent** (`agent/nfc_agent/`):
- `reader.py` — pyscard PC/SC 폴링
- `client.py` — httpx 로 백엔드 push
- `feedback.py` — 리더기 LED/Beep 등 사용자 피드백
- `main.py` — 데몬 entrypoint
- systemd 유닛으로 Pi 부팅 시 자동 기동

**Admin** (`admin/app/`):
- `login/` — 비밀번호 → JWT → localStorage
- `(authed)/` — JWT 검증된 라우트 그룹 (logs · stats · users)
- axios 인터셉터로 토큰 헤더 부착

# 마주친 문제

> (자동 추론 — 검토 필요. commit log 패턴 기반)

- **prod 배포 단독화**: prod compose 와 ssh 한 번에 raw 다운로드되도록 정리 (`4f03103`)
- **NPM 컨테이너 도달**: backend 포트 58000 + 0.0.0.0 바인딩으로 NPM (Nginx Proxy Manager) 컨테이너에서 도달 가능하게 (`7c373f8`)
- **카드 UID 직접 입력**: 등록 리더가 없어도 운영자가 UID 입력으로 카드 등록 가능하게 (`34fe129`) — 운영/포트 보정 함께
- **Orange Pi Zero 3 배포 진행**: `architecture/deployment-pi` 가 진행 중 — Pi 셋업 + systemd 등록 작업

# 회고

> (자동 추론 — 검토 필요)

- **스코프 경계의 명시적 차단**: CLAUDE.md 의 "기업용 패턴 도입 금지" (RBAC·조직·OTA·SaaS) 가 처음부터 박혀있음. 1명 admin + 직원 소수 + 리더기 1대 전제가 모든 결정을 단순화시킴 — 멀티테넌트 모델, sessions 테이블, OAuth 등 다 빠짐.
- **stateless JWT 채택**: 30일 JWT + localStorage 만으로 어드민 인증. 사용자 1명 시나리오라 가능한 단순화.
- **에이전트-백엔드 정적 API 키**: 리더기 1대 전제로 mTLS·rotation 등 복잡도 안 박음. `X-Agent-Key` 한 개.
- **SSOT 문서 룰**: docs/MAP.md + 위키링크 그래프 (옵시디언 호환) 로 결정 owner 문서 명시. 결정 바뀔 때 owner 만 수정 → 다른 문서는 자동 추종.
- **다음 단계**: Orange Pi Zero 3 배포 마무리 + 운영 안정화. 통계 대시보드는 출퇴근 데이터 누적되는 대로 다듬는 방향.
