---
id: spec-05
type: spec
title: 모노레포 디렉토리 구조 — repo root + back/frontend/scripts/persona/medi_docs
status: draft
created: 2026-05-01
updated: 2026-05-01
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[spec-01-persona-md-format]]"
tags: [spec, monorepo, layout, structure]
---

# 모노레포 디렉토리 구조

## Summary

`kknaks_profile` 모노레포의 통합 디렉토리 구조 SoT. 6개 최상위 디렉토리(`persona/`, `back/`, `frontend/`, `scripts/`, `medi_docs/`, `claude_design/`) + `.claude/` + `.gitignore` 룰. 페르소나 내부는 spec-01 §1, 백엔드 잡은 spec-03, _map 빌드는 spec-04 참조 (DRY). 본 spec이 디렉토리 위치의 SoT — 향후 변경 시 본 spec 갱신 → 다른 spec의 디렉토리 언급 동기화.

---

## 1. Repo root 트리

```
kknaks_profile/                       ← repo root (git)
├─ persona/                           ← md SoT + 옵시디언 vault root (spec-01 §1)
├─ back/                              ← FastAPI 백엔드 (§3)
├─ frontend/                          ← Next.js 프론트 (§4)
├─ scripts/                           ← 공통 스크립트 (§5)
├─ medi_docs/                         ← 본 설계 문서 (harness plugin 관리)
├─ claude_design/                     ← 디자인 v0.5 동결본
├─ .claude/                           ← Claude Code 설정 (skills/hooks/scripts)
├─ docker-compose.yml                 ← back + redis 컨테이너 정의 (§7)
├─ CLAUDE.md                          ← 프로젝트 메모 (harness plugin 자동 augment)
├─ .gitignore                         ← §6
└─ README.md                          ← (선택)

## 포트 컨벤션 (사용자 컨벤션 — 4-prefix)

| 서비스 | 포트 |
|---|---|
| back (FastAPI) | **48000** (default 8000 → 4 prefix) |
| redis | **46379** (default 6379 → 4 prefix) |
| frontend dev | 3000 (Next.js default — local dev only) |
```

**원칙**:
- 6개 최상위 디렉토리 외엔 root에 안 박음 (혼란 회피)
- `.git/`, `.DS_Store` 등 시스템 디렉토리는 git이 관리 / gitignore
- 빌드 산출물(`back/__pycache__/`, `frontend/.next/`, `frontend/node_modules/`)은 gitignore (§6)

---

## 2. `persona/` — 페르소나 콘텐츠 (md SoT)

디테일은 **spec-01 §1** 참조. 요약:

```
persona/
├─ profile.md
├─ career/*.md
├─ projects/*.md
├─ notes/*.md                         ← 위키링크 [[id]]
├─ contents/*.md
├─ daily/YYYY-MM-DD.md
├─ assets/<category>/...              ← 정적 자산 (spec-01 §2.5 — 백엔드가 /assets/* 로 서빙)
├─ activity.yaml                      ← 잡 산출물 (백엔드 write — ADR-03 §2.2)
├─ _meta.yaml                         ← enum 정의 (사람 작성)
├─ _map.md                            ← 자동 인덱스 (백엔드 + pre-commit write — spec-04)
└─ .obsidian/                         ← 옵시디언 사용자 설정 (gitignore)
```

→ 옵시디언이 이 폴더만 vault로 인식. `back/`, `frontend/` 무관.

---

## 3. `back/` — FastAPI 백엔드 (4 layer: api / service / core / utils)

### 3.1 디렉토리 트리

```
back/
├─ main.py                            ← FastAPI 앱 + lifespan (config + persona_loader + scheduler)
├─ config.py                          ← env 기반 설정 (PERSONA_DIR, REDIS_URL, RUN_SCHEDULER, ...)
│
├─ api/                               ← HTTP 핸들러만. 비즈니스 로직 X
│  ├─ __init__.py
│  ├─ routers/                        ← 12 엔드포인트 (spec-02 §2)
│  │  ├─ __init__.py
│  │  ├─ site.py · me.py · activity.py · career.py · projects.py · notes.py · contents.py
│  └─ admin/
│     ├─ __init__.py
│     └─ reload.py                    ← POST /admin/reload (ADR-03 §4.2)
│
├─ service/                           ← 비즈니스 흐름 — 부팅 로딩, 검색, 잡 orchestration
│  ├─ __init__.py
│  ├─ persona_loader.py               ← yaml/md → dict + spec-01 §6 검증 fail-fast
│  ├─ search.py                       ← 메모리 inverted index (spec-02 §3.9)
│  ├─ scheduler.py                    ← APScheduler 등록 (spec-03 §1.1)
│  └─ jobs/                           ← 잡 흐름 (spec-03)
│     ├─ __init__.py
│     ├─ inputs.py                    ← daily.md / git log / GitHub Events 수집
│     ├─ llm.py                       ← open-kknaks 호출 (ADR-04)
│     ├─ upsert.py                    ← activity.yaml rolling 365 + idempotent
│     ├─ git_push.py                  ← fetch+rebase+push 3회 retry (spec-03 §5)
│     └─ main_job.py                  ← orchestrator (입력 → LLM → upsert → push → reload)
│
├─ core/                              ← 페르소나 도메인 본질. 외부 의존 0 (fastapi/redis 등 X)
│  ├─ __init__.py
│  ├─ i18n.py                         ← {ko,en} 객체 → str 변환 규칙 (ADR-02)
│  └─ wikilinks.py                    ← [[id]] 파싱 + 그래프/백링크 빌더
│
├─ utils/                             ← 도메인-agnostic 가공 helper
│  ├─ __init__.py
│  └─ meta_helpers.py                 ← _meta.yaml + items 자동 집계 (categories.count)
│
├─ tests/                             ← pytest
│  ├─ test_i18n.py · test_wikilinks.py · test_loader.py · test_main.py · test_routers.py · test_jobs.py
│
├─ Dockerfile                         ← back 컨테이너 빌드 (§7)
├─ .dockerignore
├─ pyproject.toml                     ← uv. 의존성: fastapi, uvicorn, open-kknaks, redis, apscheduler, httpx, pyyaml, python-frontmatter
└─ .env                               ← (gitignore — 개발용 GH_TOKEN, REDIS_URL)
```

### 3.2 의존 방향 (단방향)

```
api      ──→ service · core · utils
service  ──→ core · utils
core     ──→ utils 만 (외부 패키지 의존 X — 순수 도메인)
utils    ──→ 의존 X (pure functions)
```

**이유**: core가 외부 의존 0이면 (1) 단위 테스트 빠름·격리됨, (2) 도메인 규칙 재사용 쉬움 (예: 다른 프로젝트에서 i18n helper 통째로), (3) layer 위반 시 import만 봐도 즉시 발견.

### 3.3 핵심 책임

- `main.py` — 앱 부팅 시 `_check_single_worker()` → `load_all()` (lifespan) → `scheduler.start()` 순서
- `service/persona_loader.py` — 페르소나 검증 fail-fast (spec-01 §6.1)
- `api/routers/*` — 핸들러는 dict comprehension + i18n 적용만. 로직은 service에
- `service/jobs/main_job.py` — spec-03 전체 흐름 (입력 → LLM → upsert → push → reload)

---

## 4. `frontend/` — Next.js (App Router)

```
frontend/
├─ app/                               ← App Router (Next.js 14+)
│  ├─ layout.tsx                      ← 루트 레이아웃 (TopNav, lang 상태)
│  ├─ page.tsx                        ← 랜딩 (5섹션 미리보기)
│  ├─ about/
│  │  └─ page.tsx
│  ├─ career/
│  │  └─ page.tsx
│  ├─ projects/
│  │  └─ page.tsx
│  ├─ notes/
│  │  ├─ page.tsx                     ← 그래프 메인
│  │  └─ [id]/page.tsx                ← 노트 상세 (위키링크 jump)
│  └─ contents/
│     ├─ page.tsx
│     └─ [id]/page.tsx
├─ components/
│  ├─ TopNav.tsx
│  ├─ Footer.tsx
│  ├─ TerminalHero.tsx                ← 랜딩 A안 터미널
│  ├─ NotesGraph.tsx                  ← force-directed (react-force-graph 등)
│  ├─ ActivityHeatmap.tsx             ← 잔디 격자 변환 (spec-02 §4.3)
│  └─ ContentCard.tsx
├─ lib/
│  ├─ api.ts                          ← fetcher (?lang= + 응답 타입)
│  ├─ i18n.ts                         ← lang 상태 hook (URL state 또는 context)
│  └─ types.ts                        ← API 응답 TypeScript 타입 (spec-02 §3 기반)
├─ public/                            ← 정적 자산 (favicon 등)
├─ styles/                            ← global.css 등
├─ package.json
├─ tsconfig.json
├─ next.config.ts
└─ .env.local                         ← (gitignore — NEXT_PUBLIC_API_BASE 등)
```

**핵심 책임**:
- `app/*` — 페이지별 데이터 fetch + 렌더. Server Component 기본, 인터랙션 부분만 Client Component (Notes 그래프 등)
- `lib/api.ts` — `fetch(API_BASE + path + ?lang=)` 단일 entry point
- `lib/i18n.ts` — lang 토글 시 URL state 갱신 → 페이지 refetch
- `components/*` — 디자인 v0.5 시안 이식 (`claude_design/js/proto-*.jsx` → `.tsx`)

---

## 5. `scripts/` — 공통 스크립트

```
scripts/
├─ build_persona_map.py               ← spec-04 — 페르소나 _map.md 빌드
├─ install_hooks.sh                   ← spec-04 §5 — .git/hooks/pre-commit 설치
├─ backfill_activity.py               ← spec-03 §7 — 365일 백필 (1회 수동 실행)
└─ validate_persona.py                ← (선택) spec-01 §6 검증을 CLI로 — pre-commit 또는 CI에서 활용
```

**원칙**: Python 스크립트는 백엔드 의존성 공유 (`back/pyproject.toml`). bash 스크립트는 standalone.

---

## 6. `.gitignore` 룰

```gitignore
# secret
.env
.env.local
.env.*.local

# Claude Code 로컬 설정 (절대 경로 + 머신별)
.claude/settings.local.json

# 옵시디언 사용자 설정 (사용자 PC vs 홈서버 분리)
.obsidian/

# Python 빌드 산출물
back/__pycache__/
back/**/__pycache__/
back/.pytest_cache/
back/.venv/
back/dist/
back/*.egg-info/

# Next.js 빌드 산출물
frontend/node_modules/
frontend/.next/
frontend/out/
frontend/dist/

# 시스템
.DS_Store
*.swp
*.swo

# log
*.log
back/logs/
```

**원칙**:
- secret(`.env*`) — 절대 commit X
- 머신별 설정(`.claude/settings.local.json`, `.obsidian/`) — 분리
- 빌드 산출물 — 재현 가능한 것만 ignore (소스는 commit)

---

## 7. 다른 spec과의 관계

본 spec이 디렉토리 위치의 **SoT**. 다른 spec/adr이 디렉토리 경로 언급할 때 본 spec과 일치해야 함:

| 다른 문서 | 언급된 경로 | 본 spec 정합 |
|---|---|---|
| spec-01 §1 | `persona/**/*.md`, `_meta.yaml`, `activity.yaml`, `_map.md` | ✅ §2 |
| spec-02 §4.1-4.4 | `back/loader.py`, `back/i18n.py` 등 (의사 코드) | ✅ §3 |
| spec-03 전반 | `back/scheduler.py`, `back/.env`, `persona/activity.yaml` | ✅ §3, §6 |
| spec-04 §3.2, §5 | `scripts/build_persona_map.py`, `.git/hooks/pre-commit` | ✅ §5 |
| ADR-03 §2.2 | `persona/activity.yaml`, `persona/_map.md` (write 화이트리스트) | ✅ §2 |
| plan-01 §M0 | `.gitignore`, EnvironmentFile 위치 | ✅ §6 |

**변경 룰**: 디렉토리 추가/이동/이름변경은 본 spec(spec-05) 먼저 갱신 → 다른 spec의 경로 언급 동기화 → 코드 반영. 역순으로 진행하면 SoT 깨짐.

---

## 7. docker-compose (back + redis + worker)

```yaml
# docker-compose.yml (repo root)
services:
  back:
    build: ./back
    ports:
      - "48000:48000"
    environment:
      REDIS_URL: redis://redis:6379            # 컨테이너 내부 통신은 redis 기본 포트
      PERSONA_DIR: /persona
    volumes:
      - ./persona:/persona                      # md SoT mount (잡이 activity.yaml + contents/*.md write — ADR-03, ADR-05)
    depends_on: [redis]
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "46379:6379"                            # 호스트 포트 4-prefix
    restart: unless-stopped
    volumes:
      - redis-data:/data

  worker:                                        # ADR-04 §2.2 — open-kknaks ClaudeWorker
    build:
      context: .
      dockerfile: Dockerfile.worker
    depends_on:
      redis:
        condition: service_healthy
    environment:
      REDIS_URL: redis://redis:6379
      CLAUDE_CODE_OAUTH_TOKEN: ${CLAUDE_CODE_OAUTH_TOKEN}
      PATH: /claude-tools/node/bin:/claude-tools/node_modules/.bin:/usr/local/bin:/usr/bin:/bin
    volumes:
      - ./.claude-tools:/claude-tools:ro        # Linux Node.js + claude CLI 바이너리 (setup.sh 로 사전 박음)
    restart: unless-stopped

volumes:
  redis-data:
```

**참고 — ClaudeWorker 는 worker 컨테이너** (ADR-04 §2.2). 호스트의 `.claude-tools/` (Linux Node.js + Claude Code CLI 바이너리) 를 read-only 바인드 마운트하고, `CLAUDE_CODE_OAUTH_TOKEN` env 로 인증해 컨테이너 안에서 `claude` CLI 실행. 호스트에 별도 systemd unit 없음.

## 8. 향후 확장 여지

- `back/cli/` — 운영 CLI (수동 reload, 백필 trigger 등) 추가 시
- `frontend/api/` — Next.js Route Handler 도입 시 (서버 컴포넌트만으로 부족할 때)
- `db/` — sqlite 도입 시 (ADR-01 §4.3 트리거 발동 시)
- `infra/` — Docker Compose, systemd unit, nginx config 등 IaC 박을 때
