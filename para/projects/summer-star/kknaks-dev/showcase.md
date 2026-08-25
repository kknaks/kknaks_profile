# 개요

본 포트폴리오 사이트. 모든 콘텐츠 (about / career / projects / notes / contents / daily) 는 `persona/**/*.md` 가 SoT — DB 없음, 백엔드는 부팅 시 md 를 메모리 dict 로 로드 (`ADR-01`). 잡 인프라는 본인 OSS `open-kknaks` 를 dogfooding — 잔디 (daily activity) + contents enrich 두 잡 모두 Anthropic SDK 직접 import 없이 PTY 로 Claude Code CLI 를 큐 처리한다 (`ADR-04`). 1년차 셀프호스팅 + declarative 사고를 한 사이트에 박은 작품.

# 기술스택

**프론트엔드 (`app/front/`)**
- **Next.js 15 (App Router) + React 19** — Server Component 기본, 인터랙션만 Client
- TypeScript
- **react-force-graph-2d + d3-force** — 노트 그래프 시각화 (force-directed)
- react-markdown — 노트/콘텐츠 본문 렌더

**백엔드 (`app/back/`)**
- **FastAPI** + uvicorn — async, in-memory persona server
- python-frontmatter + pyyaml — md SoT 파싱
- httpx — 외부 API 호출
- **open-kknaks** — LLM 호출 (Anthropic SDK 직접 import 금지 — `ADR-04`)
- **Redis** — open-kknaks broker
- **APScheduler** — 잔디 잡 매일 23:55 KST 실행 (`spec-03`)
- yt-dlp + youtube-transcript-api — content enrich 잡 (`spec-06`)

**선택 이유**
- DB 없음 — 1년차 셀프호스팅 + 데이터 양이 적어 부담 회피 (`ADR-01`)
- i18n A안 — 슬롯 단일키 + frontmatter `{ko, en}` (`ADR-02`)
- LLM 어댑터 — open-kknaks 로 통일해 모델 교체 / 비용 / 재시도 / 큐를 한곳에서 관리 (`ADR-04`)

**인프라**
- Docker Compose — back + redis + worker (open-kknaks ClaudeWorker)
- 홈서버 셀프호스팅
- Vercel (프론트) + 홈서버 docker + NPM (백) 분리

# 주요기능

**5 섹션 + 페이지** (`app/front/app/`)
- **랜딩** (`/`) — Hero (터미널 애니메이션) + 5섹션 미리보기
- **About** (`/about`) — 자기소개 + 잔디 + Career timeline + Skills
- **Career** (`/career`) — 경력 timeline (5개 — 도화 / 비트캠프 / 멋사 / 퀀터스 / 메디솔브)
- **Projects** (`/projects`) — 프로젝트 카드 그리드 + 카테고리 필터 + visible: false 제외
- **Notes** (`/notes`) — 노트 그래프 (force-directed) + 클러스터별 색상 + 위키링크 백링크
- **Contents** (`/contents`) — 매일 업로드 스터디 영상 + 교안

**잡 인프라** (`app/back/service/scheduler.py` + `app/back/service/jobs/`)
- **잔디 잡** — 매일 23:55 KST. `daily/YYYY-MM-DD.md` + git log + GitHub Events 수집 → LLM 종합 → `activity.yaml` rolling 365 + `git push`
- **Content enrich 잡** — `contents/*.md` 의 `status: pending` 감지 → YouTube 메타 + 자막 추출 → LLM 으로 8 H2 섹션 본문 자동 생성 → `status: published` commit
- **Reload trigger** — `POST /admin/reload` 또는 GitHub webhook → 메모리 dict 재로드

**문서 시스템 (`medi_docs/`)** — harness plugin 으로 9 카테고리 (planning / plan / spec / adr / runbook / test / release-notes / retrospective) 정형화. 본인 작업 흐름 자체를 declarative SoT 로 박음.

# 아키텍처

```
kknaks_profile/
├─ persona/             ← md SoT (사람 작성 + 잡 산출물)
│  ├─ profile.md · career/ · projects/ · notes/ · contents/ · daily/
│  ├─ assets/<category>/ · activity.yaml · _meta.yaml · _map.md
├─ app/
│  ├─ back/             ← FastAPI (4 layer: api/service/core/utils)
│  │  ├─ main.py — lifespan: load_all() + APScheduler 시작
│  │  ├─ api/routers/   ← 12 엔드포인트 + /assets static mount
│  │  ├─ service/       ← persona_loader, scheduler, jobs/
│  │  └─ core/          ← i18n, wikilinks (외부 의존 0)
│  ├─ front/            ← Next.js
│  ├─ worker/           ← open-kknaks ClaudeWorker (별도 컨테이너)
│  └─ scripts/          ← build_persona_map.py, install_hooks.sh
├─ medi_docs/           ← 본 설계 문서 (harness plugin)
├─ claude_design/       ← 디자인 v0.5 동결본
├─ workspace/           ← import-project skill 의 외부 레포 자리 (gitignored)
└─ docker-compose.yml
```

**데이터 흐름**:

1. **부팅** — `lifespan` → `_check_single_worker()` (APScheduler 다중 발동 차단) → `load_all()` (persona 검증 + 메모리 dict) → 스케쥴러 start.
2. **요청** — frontend → `/api/<resource>?lang=ko|en` → `/assets/...` (static) → 라우터가 메모리 dict + i18n helper → JSON.
3. **잡** (매일 23:55 KST) — APScheduler → `extract_inputs` (daily.md + git + GitHub) → open-kknaks `submit` → ClaudeWorker (PTY 로 `claude -p`) → 결과 → `upsert_activity` → `git_push` (fetch-rebase-push 3회 retry) → `POST /admin/reload`.
4. **content enrich** (별도 cadence) — `contents/*.md` 에서 `status: pending` 감지 → yt-dlp + 자막 → open-kknaks → 8 H2 섹션 본문 → `status: published` commit.

**의존 방향** (단방향): `api → service → core → utils`. core 는 외부 의존 0 (단위 테스트 격리).

# 핵심 구현

**페르소나 로더** (`app/back/service/persona_loader.py`)
- `persona/**/*.md` 전체 스캔 → 카테고리별 dict + frontmatter 검증 (필수 필드 / enum / 위키링크 dead link 등 — `spec-01 §6`)
- 검증 fail-fast — frontmatter 위반 시 부팅 abort

**i18n 헬퍼** (`app/back/core/i18n.py`) — `{ko, en}` 객체 → `?lang=` 분기 단일 helper

**위키링크 그래프** (`app/back/core/wikilinks.py`) — `notes/*.md` 본문의 `[[id]]` 추출 → 그래프 edge + 백링크 자동 계산

**APScheduler 잡 등록** (`app/back/service/scheduler.py`) — `spec-03 §1.1`. multi-worker 차단으로 분산 lock 회피.

**open-kknaks dogfooding** (`app/back/service/jobs/llm.py`)
- `RedisBroker` + `ClaudeClient` 로 큐 발행
- ClaudeWorker (`app/worker/` 컨테이너) 가 PTY 로 `claude -p ...` 실행
- LoggingMiddleware + RetriesMiddleware + CostMiddleware 체인
- Anthropic SDK import 0 — `ADR-04` 강제

**자산 정적 서빙** — `app.mount("/assets", StaticFiles(directory=PERSONA_DIR / "assets"))` (`spec-01 §2.5`, `spec-02 §2`)

**Agent 시스템** (`.agent/skills/`, `.codex/`) — YouTube content stub 생성과 Codex 세션 hook 등 본 사이트 작업 흐름을 repo 안에 박아 dogfooding.

# 마주친 문제

(spec / ADR 결정 기록 — 자동 추론보다 사실 기반)

- **DB 도입 vs 미도입** — 1년차 + 데이터 양 + 셀프호스팅 부담 vs 검색 / 그래프 quality. **결론: DB-less + in-memory dict** (`ADR-01`). 트리거 발동 시 sqlite 도입 검토.
- **i18n 표현 — 슬롯 단일키 vs 키 분기** — 백엔드 응답 분기 vs frontend slot 분기. **결론: A안 슬롯 단일키 + frontmatter `{ko, en}`** (`ADR-02`).
- **잔디 잡 attribution — kind 분류 + summary 길이** — 단순 commit count vs 의미 있는 narrative. **결론: 5종 kind (commit/note/study/null) + LLM 종합 summary** (`ADR-03`).
- **LLM SDK 선택 — Anthropic 직접 import vs 어댑터** — 비용 / 재시도 / 모델 교체 / 큐 처리 한곳에서 관리. **결론: open-kknaks 통일** (`ADR-04`). 본인 OSS 를 production dogfooding.
- **Content enrich — 동기 처리 vs pending → published** — 사용자 push 직후 즉시 enrich 시 latency / 실패 처리. **결론: pending stub 박고 잡이 비동기 enrich → published** (`ADR-05`, `spec-06`).

> 자동 추론은 git log 4 커밋만으로는 어려움 — 본 프로젝트는 ADR 5개 / spec 6개 / planning 1개의 의사결정 기록이 풍부해 그 자체가 마주친 문제 list 역할.

# 회고

> 일부 자동 추론 — 사용자 검토 권장.

- **declarative SoT 의 미니멀함** — 모든 콘텐츠가 `persona/**/*.md` 에 있고, 백엔드는 부팅 시 한 번 로드 + reload 트리거. md 를 옵시디언으로 작성, AI 컨텍스트로도 그대로 활용. 한 SoT 가 작성 도구 / 사이트 / AI / 옵시디언 vault 4 군데에 동시 활용되는 구조.
- **(자동 추론)** 4 ADR + 6 spec — 1년차 치고 의사결정 추적 수준이 높음. 빠른 시도 vs 사전 설계의 균형에서 사전 설계 쪽으로 기울었는데, 1인 작업이라 *합의* 보다는 *미래 자기*를 위한 기록.
- **(자동 추론)** open-kknaks dogfooding — 본인 OSS 를 production 에 박은 결정. 라이브러리 quality 검증 + 본 사이트 quality 가 동시에 발전.
- **(자동 추론)** 다음 sprint — 배포 (트리거 미결정 — Actions / cron / webhook 중). 본 sprint 까지 잡 + contents + webhook 가 끝났고 (memory), 다음은 운영 단계.
- **(자동 추론)** 다시 한다면 — medi_docs harness plugin 도입을 더 일찍. 9 카테고리 정형화가 의사결정 추적성에 큰 영향.
