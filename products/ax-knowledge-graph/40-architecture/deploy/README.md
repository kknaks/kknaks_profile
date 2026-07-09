# Deploy

AX Knowledge Graph의 배포 설정은 Next.js Web, FastAPI API, PostgreSQL, bind-mounted knowledge workspace, open-kknaks를 분리해서 다룬다. Redis는 필요할 때만 queue/cache/lock 용도로 붙인다.

## Services

| Service | Required | Notes |
|---|---|---|
| `web` | yes | Next.js app. Talks to FastAPI only. |
| `api` | yes | FastAPI app. Owns workflow state and file writes through Apply Executor. |
| `postgres` | yes | Operational DB and graph cache. |
| `open-kknaks` | yes | AI task runner/provider bridge. `ClaudeWorker` consumer가 Redis(`namespace=axkg`, `queue=default`)를 구독해 claude를 실행한다. **스테이지 방법 지침 프로젝트 컨텍스트를 이미지에 내장**하고 `WORK_DIR`을 그 경로로 둔다(아래 Worker Project Context). provider credential(`CLAUDE_CODE_OAUTH_TOKEN`)은 이 worker에만 둔다. Can be external service. |
| `redis` | required for AI 실행 | open-kknaks 실행 broker(api producer ↔ worker consumer). 그 외 queue/lock/pub-sub·cache는 필요 시. |

## Local Development Topology

```text
Next.js dev server  ->  FastAPI dev server  ->  PostgreSQL
                                      |      ->  Workspace root: /workspace bind mount
                                      |      ->  open-kknaks
                                      `---->  Redis (optional)
```

Recommended local ports:

| Service | Port |
|---|---|
| Next.js | `3000` |
| FastAPI | `8000` |
| PostgreSQL | `5432` |
| Redis | `6379` |
| open-kknaks | configured by `AXKG_OPEN_KKNAKS_BASE_URL` |

## Workspace / Document Mount

- 최종 문서는 Markdown file이 SoT다.
- 결과물 Markdown은 컨테이너 내부 임시 디렉터리에 쓰지 않는다.
- API 컨테이너는 host의 knowledge workspace를 bind mount로 받는다.
- 앱/컨테이너 내부에서는 고정된 workspace root config를 사용한다.
- Apply Executor는 workspace root 아래의 allowlist 경로에만 쓴다.
- DB의 `documents.path`에는 workspace root 기준 상대 경로만 저장한다.

예시:

```text
host: /Users/kknaks/git/toy_pr2/kknaks_profile
app:  /workspace
```

MVP write allowlist:

```text
/workspace/permanent/**
/workspace/products/ax-knowledge-graph/00-baseline/**
```

Read-only context roots:

```text
/workspace/context/**
/workspace/reference/**
/workspace/templates/**
/workspace/rules/**
/workspace/products/ax-knowledge-graph/20-spec/**
/workspace/products/ax-knowledge-graph/40-architecture/**
```

로컬 개발도 같은 bind mount 구조를 사용한다. `data/documents`는 컨테이너 내부 결과물 저장소가 아니라, 필요할 때만 별도 실험용 document root로 둔다.

> `/workspace/context/**`의 AI 방법·배경 지침은 **api가 마운트로 읽어 조립하지 않는다**. 이 지침은 worker 이미지에 내장된 프로젝트 컨텍스트로 옮겨졌고 claude가 직접 읽는다(아래 Worker Project Context, AXKG-SPEC-011). api의 이 마운트는 Apply Executor 쓰기와 그래프 인덱싱용이다.

## Worker Project Context

- open-kknaks worker(`ClaudeWorker`)는 스테이지 방법·배경 지침(요약/분류/연결/chat)을 담은 프로젝트 컨텍스트를 **worker 이미지에 내장한다** — 배포 시 마운트(git pull 런타임 의존)가 아니라 **빌드 시점 고정**이다.
- worker는 실행 작업 디렉토리(`WORK_DIR`)를 그 내장 경로로 두고, claude가 진입 `CLAUDE.md → agent.md → context/`를 스스로 읽는다.
- api submit 표면은 **DB 프롬프트(작업 지시) + output_schema (+③ 활성 템플릿) + 런타임 원문/후보**뿐이다. 요약 방법 지침(`source-summary-guide.md` 등)은 프로젝트 컨텍스트가 담당하고 api는 로드하지 않는다.
- 요약 작업용 프로젝트 컨텍스트 원본은 코드레포 `apps/worker/workspace/`에 둔다(worker 이미지 빌드 소스, profile-be 소관).
- 이 프로젝트 컨텍스트는 최종 Markdown document root(위 Workspace / Document Mount)와 별개다 — worker는 문서 root를 마운트하지 않는다(요약은 파일을 쓰지 않고, 쓰기는 api Apply Executor 전속).
- 원문(`SourceMaterial`)이 claude에 닿는 방식(프롬프트 인라인 vs `WORK_DIR` 파일 드롭)은 구현 시 결정(AXKG-SPEC-011 OQ).

## Environment

| Env | Required | Example |
|---|---|---|
| `AXKG_DATABASE_URL` | yes | `postgresql+psycopg://axkg:axkg@postgres:5432/axkg` |
| `AXKG_REDIS_URL` | AI 실행 시 yes | `redis://redis:6379/0` — open-kknaks broker(`namespace=axkg`) 겸 optional queue/cache. 미설정 시 요약 자동 트리거 생략 |
| `CLAUDE_CODE_OAUTH_TOKEN` | open-kknaks worker only | claude provider 실행 credential. **worker(consumer)에만** — api/web에 두지 않는다(AXKG-SPEC-007) |
| `AXKG_WORKSPACE_ROOT` | yes | `/workspace` |
| `AXKG_MARKDOWN_WRITE_ALLOWLIST` | yes | `permanent/**,products/ax-knowledge-graph/00-baseline/**` |
| `AXKG_OPEN_KKNAKS_BASE_URL` | yes | `http://open-kknaks:8080` |
| `AXKG_DEFAULT_PROVIDER` | no | `claude` |
| `AXKG_AUTH_TOKEN_TTL_DAYS` | no | `30` |
| `AXKG_SLACK_SIGNING_SECRET` | Slack intake 사용 시 yes | Slack 슬래시 커맨드 서명 검증 |
| `AXKG_SLACK_BOT_TOKEN` | Slack intake 사용 시 yes | `xoxb-...` — 앵커 메시지 post·스레드 요약 회신용 |
| `NEXT_PUBLIC_AXKG_API_BASE_URL` | yes | `http://localhost:8000` |

## Slack Intake

- Slack 슬래시 커맨드가 `api` 서비스의 `POST /api/v1/slack/commands`로 커맨드 payload를 보낸다(Events API 채널 구독 아님, 별도 브릿지 서비스 없음).
- 이 경로는 Slack 앱에 등록된 Request URL(`https://ax-api.kknaks.cloud/api/v1/slack/commands`)과 문자 그대로 일치시킨다 — 다른 라우트의 무prefix 관례에 대한 예외로, rewrite 없이 그대로 서빙한다.
- 이 엔드포인트는 토큰 로그인(AXKG-SPEC-008) 대상이 아니라 Slack signing secret 서명 검증으로 보호한다.
- Slack payload 원문은 장기 보존하지 않고 URL/channel/user/timestamp/text snippet/metadata만 저장한다(AXKG-DEC-004).
- `api`가 외부에서 도달 가능해야 하므로(홈서버 NPM 뒤), 백엔드 공개 주소 `ax-api.kknaks.cloud`로 Request URL을 등록한다. Slack 앱 등록·NPM 노출 자체는 스펙 밖(배포는 후속).
- 슬래시 커맨드는 채널 메시지를 남기지 않으므로, 봇이 앵커 메시지를 post하고(`AXKG_SLACK_BOT_TOKEN`) 그 스레드에 `summarized`/`collection_failed` 결과를 회신한다.

## Persistence

| Data | Persistence |
|---|---|
| PostgreSQL | volume + regular backups |
| Markdown workspace | host bind mount; this is document body SoT |
| Redis | disposable unless queue durability is explicitly required later |
| open-kknaks logs | follow open-kknaks deployment policy |

## Deployment Rule

- API containers must mount the workspace root.
- Web containers must not mount the workspace root.
- DB stores workspace-relative `documents.path` only.
- Apply Executor rejects file actions outside `AXKG_WORKSPACE_ROOT`.
- Apply Executor rejects writes outside `AXKG_MARKDOWN_WRITE_ALLOWLIST`.
- Provider credentials(`CLAUDE_CODE_OAUTH_TOKEN`)는 open-kknaks worker(consumer) 런타임에만 둔다 — AXKG api/web에 두지 않는다(AXKG-SPEC-007: credential은 서버까지, 실행은 worker).

## Open Items

- ~~docker compose 초안 작성~~ → 코드 레포 루트 `docker-compose.yml`로 작성 완료(postgres 45432 + redis 46380 + api 48100 + open-kknaks worker, web은 profile). 기존 kknaks 스택(48000/46379)과 포트 충돌 없음.
- PostgreSQL volume/backup 정책 확정.
- ~~Redis 도입 시점 결정~~ → open-kknaks broker가 Redis 기반이라 compose에 포함. AXKG 자체 queue/lock 용도 사용은 여전히 필요 시점에 결정.
