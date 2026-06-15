---
type: work
id: WORK-002
title: "AI 요약 기능 구현 (BE 엔드포인트 2 + FE 2뷰 + 워커 기동)"
status: todo
product: mykakao
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: profile-fe
  be: profile-be
  qa: kknaks
  ops: profile-be
progress: 0
created_at: 2026-06-15
updated_at: 2026-06-15
tags:
  - product/mykakao
  - doc/work
  - status/todo
links:
  baselines: []
  decisions:
    - "[[decision-002-ai-summary-approach]]"
  specs:
    - "[[spec-002-ai-conversation-summary]]"
  works: []
  releases: []
  related: []
---

# AI 요약 기능 구현 (BE 엔드포인트 2 + FE 2뷰 + 워커 기동)

SPEC-002 계약(방·날짜 선택 + 사용자 프롬프트 → codex 요약 → SSE 스트리밍, 2뷰)을 mykakao 코드로 내리는 작업 지시서.

> spec의 조합을 실제 구현 단위로 내리는 작업 지시서다.
> 제품 결정·기능 계약은 [[decision-002-ai-summary-approach]] / [[spec-002-ai-conversation-summary]]에 둔다. 여기엔 작업·acceptance·테스트만.

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | todo |
| Progress | 0% |
| Branch/PR | `toy_pr2/mykakao` (코드 레포, 미구현) |
| Blocker | 없음 (인프라 = docker compose; 사전조건 호스트 `~/.codex` 인증 준비 = 충족) |
| Next | W-1/W-2 병렬 착수 → W-3 docker(redis+codex worker) 기동 통합 E2E |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위·acceptance 판정 | todo |
| FE | profile-fe | `index.html` 진입 + `summary.html` 2뷰/스트리밍 렌더 | todo |
| BE | profile-be | `/api/summarize` + `/api/summarize/stream` + 조립/cap + open_kknaks 연동 (호스트 스크립트) | todo |
| QA | kknaks | E2E 라이브 검증 | todo |
| Ops | profile-be | `docker-compose`(redis + codex worker) 작성·기동 + `.codex-tools`/`.codex-home` 준비 | todo |

## Scope

- Covers: [[spec-002-ai-conversation-summary]] — 2뷰 데모, 단일 방×단일 날짜 요약, open_kknaks(codex) 호출, SSE 스트리밍.
- Out of scope: 멀티데이/방 전체 요약, 일정 파싱·캘린더 출력, 프롬프트 프리셋, 인증/멀티유저, 배포.
- **결과 저장(DB) 명시적 제외**: 요약 결과는 SSE로 휘발한다. 결과 영속화/히스토리(postgres 등)는 이번 범위에서 다루지 않으며 후속 과제다. → 인프라에서 결과 저장용 DB는 띄우지 않는다(W-3).

## Target Surface

- 코드 레포: `/Users/kknaks/git/toy_pr2/mykakao`
  - `backend/main.py` — `/api/summarize`(POST), `/api/summarize/stream`(GET SSE) 추가. 기존 `/api/stream` SSE 패턴(`main.py:167-211`) 재사용. **backend는 호스트 스크립트 유지**(컨테이너화 X — 사유 아래).
  - `backend/` — 메시지 조회(그 방·그날 `sentAt` epoch 범위) + OQ-2 조립기 + OQ-3 cap. 조회는 기존 ro 연결(`db.py`) 재사용.
  - `backend/models.py` — 기존 `ChatMessage`(logId/chatId/authorId/type/message/sentAt) / `ChatRoom` 재사용(스키마 변경 없음).
  - `requirements.txt` — `open_kknaks` 의존 추가.
  - open_kknaks client 초기화 — `REDIS_URL` env로 broker 연결(호스트 → `redis://localhost:6379`, docker redis 노출 포트).
  - `frontend/index.html` — 날짜 선택 + 요약 진입 CTA 추가.
  - `frontend/summary.html` — 신규 요약 화면(바닐라 JS).
  - `docker-compose.yml` (신규) — **redis + codex worker 2 서비스**. open-kknaks `examples/docker-compose.yml` 패턴 미러. (examples엔 `app` 서비스도 있으나 mykakao는 backend 호스트라 **app 서비스 생략**.)
  - `Dockerfile.worker` (신규) — `pip install open-kknaks` + `worker/run.py` 기동. examples `Dockerfile.worker` 미러(레퍼런스 핀 `open-kknaks==2.0.2`).
  - `setup.sh` 류 (신규) — Linux용 codex CLI를 `.codex-tools/`에 설치 + 호스트 `~/.codex` 인증/config를 `.codex-home/`으로 복사 + `.env` 생성 + `docker compose up`. examples `setup.sh` 미러.
- **backend 컨테이너화 불가 사유**: 카카오 DB가 macOS 호스트 경로 + `extract.py`가 `ioreg`/plist(호스트 전용 API) 의존 → 컨테이너 내부에서 접근 불가. 따라서 backend는 호스트 네이티브 유지하고 docker redis(노출 포트)에만 연결.
- 라이브러리(런타임 의존): `open_kknaks` (`ClaudeClient`/codex client + `client.submit`/`client.stream`).
- grounding 레퍼런스: `/Users/kknaks/git/library/claude_code_pty/open_kknaks/examples/` (`docker-compose.yml`, `Dockerfile.worker`, `setup.sh`, `.env.example`).

## Implementation Plan

| Step | Task | Owner | Status | Notes |
|---|---|---|---|---|
| W-1.1 | `POST /api/summarize` — 그 방·그날(`sentAt` epoch [00:00,24:00)) 메시지 조회 | profile-be | todo | 기존 ro 연결 재사용 |
| W-1.2 | OQ-2 조립 템플릿(`{프롬프트}\n\n---\n[{방}/{date}]\n{HH:MM} {발신자}: {본문}`) + 비텍스트 placeholder | profile-be | todo | SPEC-002 §Data Contract |
| W-1.3 | OQ-3 cap — 상한 초과 시 오래된 것부터 truncate + `…(일부 생략됨, 총 N개 중 M개 표시)` 메타 | profile-be | todo | 상한값 = 이 work에서 고정(tunable param) |
| W-1.4 | `client.submit(assembled, model="gpt-5.5")` → `{task_id}` 반환 | profile-be | todo | codex provider |
| W-1.5 | `GET /api/summarize/stream?task_id=` — `client.stream(task_id, event_types={"text"})` 릴레이 + terminal 합성 | profile-be | todo | done/error는 TaskStatus 파생(아래 Notes) |
| W-1.6 | `requirements.txt` open_kknaks 추가 + client 초기화(호스트, `REDIS_URL`로 broker 연결) | profile-be | todo | 호스트 backend → docker redis 노출 포트 |
| W-2.1 | `index.html` 날짜 선택 수단 + `summary.html?chat_id=&date=` 진입 | profile-fe | todo | 기존 목록 유지 |
| W-2.2 | `summary.html` — 헤더/프롬프트 textarea/실행 버튼/결과 스트리밍 영역/고지·에러 | profile-fe | todo | 바닐라 JS, 프레임워크 금지 |
| W-2.3 | `POST /api/summarize`→task_id→`EventSource(stream)` 구독·렌더 + State Machine UI | profile-fe | todo | idle→submitting→streaming→done/error+취소/재실행 |
| W-3.1 | `docker-compose.yml` 작성 — `redis`(`redis:7-alpine`, `6379:6379` 노출, `redis-cli ping` healthcheck) + `worker`(codex) 2 서비스 | profile-be | todo | examples 미러. app 서비스 생략(backend 호스트). 결과 DB 미포함 |
| W-3.2 | `Dockerfile.worker` 작성 — `pip install open-kknaks` + `worker/run.py`. **node 런타임 멀티스테이지 복사**(codex bin이 node 런처) + run.py에서 `os.chdir(WORK_DIR=/project)` | profile-be | todo | Data Notes 메커니즘 1·2. node 없으면 exit 127 |
| W-3.3 | worker 서비스 마운트/env — `..:/project:ro`, `./.codex-tools:/codex-tools:ro`, `./.codex-home:/codex-home`, `CODEX_HOME=/codex-home`, `PATH=/codex-tools/node_modules/.bin:...` | profile-be | todo | codex 인증 = 바인드 마운트 |
| W-3.4 | `setup.sh` 류 — Linux codex CLI를 `.codex-tools/`에 설치 + 호스트 `~/.codex`→`.codex-home/` 복사 + **`.codex-home/config.toml`에 `/project` trust 등록** + `.env` 생성 | profile-be | todo | 메커니즘 3(trust). 사전조건: 호스트 codex 로그인(`~/.codex`). codex bin: `/opt/homebrew/bin/codex` 확인됨 |
| W-3.5 | `docker compose up` 기동 검증 — redis + codex worker up, 호스트 backend가 redis 큐로 submit → 워커 codex 실행 → 스트림 반환 | profile-be | todo | NAMESPACE/QUEUES가 submit↔worker 일치해야 픽업됨 |

> 의존: W-1(BE 계약)과 W-2(FE)는 SPEC 계약 기준 병렬 가능. W-3은 W-1 통합 검증 단계에서 필요.

## Data / API Notes

- **open_kknaks 호출 패턴**: 본진 `app/back/service/jobs/llm.py:175 task_id = await client.submit(...)`와 동일 흐름. mykakao는 provider=codex, `model="gpt-5.5"`(pass-through tunable; `codex exec --json --model gpt-5.5`, `codex_adapter.py:100-109`).
- **스트림 이벤트 매핑(중요, 코드 확인 결과)**: `client.stream`은 `StreamEvent`(`task.py:45`)를 yield한다. `type ∈ {text, cost, retry, tool_use, tool_result, thinking, init, progress}`, 텍스트 토큰은 `type=="text"`의 `.text` 필드. **종료/에러 전용 stream 이벤트는 없다** — 완료/실패는 `TaskStatus`(`done`/`failed`/`cancelled`, `task.py:14-21`)와 `Task.error`로 파생. → BE가 스트림 종료 후 task 상태를 조회해 **terminal SSE 이벤트(완료/에러)를 합성**해 FE에 보낸다. SSE 이벤트 JSON 키는 이 매핑(`type`/`text` + 합성 done/error)으로 고정.
- **메시지 조회**: `chat_id` + `sentAt`(unix epoch 초)이 그 날짜 로컬 `[00:00,24:00)`. 기존 ro 연결(WORK-001 `mode=ro`) 재사용.
- **직렬화**: `chatId`/`logId`는 18자리(>2^53) → 문자열 직렬화 유지(SPEC-001 / WORK-001 규약).
- **표시명 해석**: 방 이름/발신자는 SPEC-001 `NTChatRoom.chatName`(1:1 빈값 → 멤버명) 규약 재사용. 오픈채팅 등 미해석은 WORK-001과 동일 한계(`(이름 없음)`) 수용.
- **Redis broker = docker** (`redis:7-alpine`, `6379:6379` 노출). brew 미사용. 연결 주소가 둘로 갈린다(grounding):
  - **codex worker**(compose 네트워크 내부) → `redis://redis:6379` (worker `.env`).
  - **호스트 backend**(노출 포트) → `redis://localhost:6379` (`REDIS_URL`). 같은 redis를 가리킨다.
- **NAMESPACE/QUEUES 일치 필수**: 호스트 backend의 `client.submit`과 docker worker가 같은 namespace/queue를 공유해야 작업이 픽업된다. 불일치 시 submit은 성공하나 워커가 영원히 집지 않는다.
- **codex worker provider_options**: 초기 grounding은 기본값 `{"sandbox":"workspace-write","color":"never","skip_git_repo_check":true}`로 적었으나, T-006 E2E(commit `c5d4b97`) 실측 결과 **이건 submit-side 옵션이며 현재 미사용**이다. adapter(`codex_adapter.execute()`)가 worker config를 무시하고, T-005 최소 submit(`client.submit(prompt, model)`)은 이 옵션을 보내지 않는다. 실제 codex 동작은 아래 3개 메커니즘으로 성립한다. `sandbox`는 adapter 기본 `workspace-write`, `color`는 미지정으로도 동작. `skip_git_repo_check`는 trust 방식(아래 3)으로 우회되어 불필요.
- **docker codex 실측 메커니즘 3개 (T-006 grounding, 정본)**:
  1. **codex bin = node 런처** — `@openai/codex` 의 `.bin/codex`는 `#!/usr/bin/env node` shebang이라 컨테이너에 node 런타임이 필요하다(없으면 `env: 'node': No such file`, exit 127). → `Dockerfile.worker`에서 `node:22.16.0-slim` 멀티스테이지로 node 바이너리를 복사(self-contained). examples는 `.claude-tools/node` 마운트 방식이나 self-contained가 깔끔.
  2. **codex가 워커 프로세스 cwd를 상속** — `codex_adapter.execute()`가 `ClaudeConfig.work_dir`를 무시하고 **워커 프로세스의 cwd**를 codex exec cwd로 쓴다. Dockerfile `WORKDIR /app`(비-git, 미신뢰)에서 그대로 돌면 실패. → `run.py`에서 `os.chdir(WORK_DIR)`(=`/project`)로 codex가 trusted git repo에서 돌게 한다.
  3. **codex trust는 config.toml로** — git repo여도 trust 등록이 별도 필요(codex 0.139, "Not inside a trusted directory…"). submit-side `skip_git_repo_check`는 위 1번 사유로 미적용. → `.codex-home/config.toml`에 `[projects."/project"] trust_level = "trusted"`를 등록(`setup.sh`가 자동 추가)하여 우회. 결과: T-005 최소 submit이 무수정 동작.
- **고정값 동기화 주의**: codex cwd/trust 경로가 한 쌍이다 — `WORK_DIR=/project`(run.py chdir) ↔ `.codex-home/config.toml`의 `[projects."/project"]` trust. **WORK_DIR을 바꾸면 trust 경로도 같이 바꿔야** codex가 동작한다. (`/project`는 `.:/project:ro` 마운트 — 요약은 텍스트라 쓰기 불요; 워크스페이스 쓰기 작업으로 확장 시 rw 재검토.)
- **컨테이너 codex 인증**: 호스트 `~/.codex`를 `.codex-home`으로 복사한 바인드 마운트(`CODEX_HOME=/codex-home`). auth.json 전체가 복사되므로 로컬 데모 전제(`.gitignore` 처리).

## Acceptance Criteria

연결된 SPEC-002 계약을 완료 판단 기준으로 번역한다.

- [ ] **W-1 BE**: `POST /api/summarize {chat_id,date,prompt}`가 그 방·그날 메시지를 OQ-2 템플릿으로 조립(+cap 시 고지 메타)하고 `client.submit(...,model="gpt-5.5")` 후 `{task_id}`를 반환한다.
- [ ] **W-1 BE**: `GET /api/summarize/stream?task_id=`가 `client.stream` text 이벤트를 `text/event-stream`으로 릴레이하고, 종료 시 TaskStatus 기반 terminal(완료/에러) 이벤트를 합성해 보낸다.
- [ ] **W-1 BE**: Validation/Case Matrix 준수 — 빈 프롬프트 400, 잘못된 chat_id/date 400, 그날 0건 안내, cap 초과 시 truncation+고지(에러 아님), 워커/codex 오류 시 에러 이벤트.
- [ ] **W-2 FE**: `index.html`에서 방+날짜 선택 후 `summary.html`로 진입한다.
- [ ] **W-2 FE**: `summary.html`이 POST→task_id→EventSource 분리 구조로 결과를 스트리밍 렌더하고, State Machine(idle→submitting→streaming→done/error+취소/재실행)을 UI에 반영한다. 바닐라 JS 유지.
- [ ] **W-3 인프라**: `docker compose up`으로 redis(`redis:7-alpine`) + codex worker가 기동되고, 호스트 backend(`run.sh`/uvicorn)가 `redis://localhost:6379` 큐로 submit → 워커가 codex 실행 → 스트림 반환까지 방·날짜·프롬프트 → 스트리밍 결과 **E2E 1회 라이브 동작**. (`.codex-tools`/`.codex-home` 준비 완료 상태에서.)

## Test Plan

| Case | Owner | Status | Notes |
|---|---|---|---|
| `POST /api/summarize` 정상 → task_id | kknaks | todo | curl, 실제 방·날짜 |
| 조립 템플릿/시각/placeholder 형식 | kknaks | todo | OQ-2 형식 일치 |
| cap 초과 truncation + 고지 | kknaks | todo | 메시지 많은 날 선택 |
| `GET /stream` text 릴레이 + terminal 합성 | kknaks | todo | done/error 분기 |
| 빈 프롬프트/잘못된 chat_id·date/0건 | kknaks | todo | Case Matrix |
| FE 2뷰 + State Machine 렌더 | kknaks | todo | 브라우저 |
| E2E 1회(방→날짜→프롬프트→스트리밍) | kknaks | todo | `docker compose up`(redis+worker) 후, 호스트 backend submit |

## Done Criteria

- [ ] role별 완료 상태 갱신.
- [ ] SPEC-002 Work Handoff와 계약 섹션(UX/FE/BE/State/Data/Case)을 Acceptance에 반영.
- [ ] cap 상한 구체값·SSE 이벤트 키를 코드에 고정(spec가 work로 이월한 파라미터).
- [ ] E2E 라이브 검증 완료.
- [ ] `log.md` / `30-work/README.md`(+spec coverage) 갱신.

## Open Issues

- cap 상한 구체값 미정 — 토큰 예산 측정 후 W-1.3에서 고정.
- 오픈채팅 발신자명/방이름 해석 한계(WORK-001과 동일) — 필요 시 별도 메타 처리.
- 코드 레포 커밋은 별도 BE/FE 워커 + 사용자 승인 소관(이 work order는 문서만).
- 기동 방식 = **docker(redis+codex worker) + 호스트 스크립트(backend)** 하이브리드. T-006 E2E(`c5d4b97`)로 메커니즘이 굳었으니 **`40-architecture/`(system) 승격 후보** — codex node 런처/cwd 상속/config.toml trust 3개 메커니즘이 여러 work에 재사용될 장기 구조면 승격. (사용자 승인 전까지 40 문서 미생성. DEC-002/SPEC-002 기능 계약은 불변 — 이번 정정은 work 레벨 한정.)
- 결과 영속화(DB)는 이번 범위 제외(SSE 휘발). 히스토리/재조회가 필요해지면 별도 baseline→decision으로 올린다.
