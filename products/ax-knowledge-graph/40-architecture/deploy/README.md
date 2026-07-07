# Deploy

AX Knowledge Graph의 배포 설정은 Next.js Web, FastAPI API, PostgreSQL, bind-mounted knowledge workspace, open-kknaks를 분리해서 다룬다. Redis는 필요할 때만 queue/cache/lock 용도로 붙인다.

## Services

| Service | Required | Notes |
|---|---|---|
| `web` | yes | Next.js app. Talks to FastAPI only. |
| `api` | yes | FastAPI app. Owns workflow state and file writes through Apply Executor. |
| `postgres` | yes | Operational DB and graph cache. |
| `open-kknaks` | yes | AI task runner/provider bridge. Can be external service. |
| `redis` | optional | Background task queue, locks, progress pub/sub, short-lived cache. |

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

## Environment

| Env | Required | Example |
|---|---|---|
| `AXKG_DATABASE_URL` | yes | `postgresql+psycopg://axkg:axkg@postgres:5432/axkg` |
| `AXKG_REDIS_URL` | no | `redis://redis:6379/0` |
| `AXKG_WORKSPACE_ROOT` | yes | `/workspace` |
| `AXKG_MARKDOWN_WRITE_ALLOWLIST` | yes | `permanent/**,products/ax-knowledge-graph/00-baseline/**` |
| `AXKG_OPEN_KKNAKS_BASE_URL` | yes | `http://open-kknaks:8080` |
| `AXKG_DEFAULT_PROVIDER` | no | `claude` |
| `AXKG_AUTH_TOKEN_TTL_DAYS` | no | `30` |
| `AXKG_SLACK_SIGNING_SECRET` | Slack intake 사용 시 yes | Slack app signing secret |
| `AXKG_SLACK_BOT_TOKEN` | no | `xoxb-...` (수신 완료 응답용, 선택) |
| `NEXT_PUBLIC_AXKG_API_BASE_URL` | yes | `http://localhost:8000` |

## Slack Intake

- Slack Events API가 `api` 서비스의 `POST /integrations/slack/sources`로 직접 이벤트를 보낸다(별도 브릿지 서비스 없음).
- 이 엔드포인트는 토큰 로그인(AXKG-SPEC-008) 대상이 아니라 Slack signing secret 서명 검증으로 보호한다.
- Slack event 원문은 장기 보존하지 않고 URL/channel/user/timestamp/text snippet/metadata만 저장한다(AXKG-DEC-004).
- `api`가 외부에서 도달 가능해야 하므로(홈서버 NPM 뒤), Events API request URL은 공개 HTTPS 경로로 등록한다.

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
- Provider credentials must stay in API/open-kknaks runtime, never in Next.js.

## Open Items

- docker compose 초안 작성.
- PostgreSQL volume/backup 정책 확정.
- Redis 도입 시점 결정.
