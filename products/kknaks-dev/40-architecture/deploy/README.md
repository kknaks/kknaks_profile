# Deploy Architecture

규칙: `rules/product-doc-pipeline.md`

> 제품의 배포 환경과 타겟을 관리한다. 실행 절차(명령·단계)는 여기 두지 않는다.

## Environments

| Environment | URL/Target | Purpose | Notes |
|---|---|---|---|
| local | `docker-compose.local.yml` | 개발 | `JOB_GIT_PUSH_DRY_RUN=1` 기본 — 커밋/푸시가 실제로 나가지 않는다 |
| production (back) | 홈서버 docker + NPM(reverse proxy) | 백엔드 운영 | `profile-api.kknaks.cloud` |
| production (front) | Vercel | 프론트 운영 | `profile.kknaks.cloud` |

staging 환경은 없다. 프론트·백이 같은 site(`kknaks.cloud`)라 세션 쿠키가 `SameSite=Lax`로 전송된다([[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]] D3).

## Services

| Service | Image | 호스트 포트 | 비고 |
|---|---|---|---|
| `back` | `Dockerfile.back` | 48000 | 단일 워커. **repo 쓰기 마운트 필요** — Executor가 md를 쓰고 push한다 |
| `postgres` | `postgres:16-alpine` | 45433 → 5432 | 호스트 포트는 4-prefix 컨벤션 |
| `redis` | `redis:7-alpine` | 46379 → 6379 | |
| `worker` | `Dockerfile.worker` | — | repo `:ro` 마운트 |
| ~~`slack-bridge`~~ | ~~`Dockerfile.back`~~ | ~~—~~ | **제거 예정** — back에 흡수([[decision-013-slack-bridge-into-backend|KDEV-DEC-013]]) |

## Deploy Map

| Area | Index |
|---|---|
| Backend | `back/README.md` |
| Frontend | `front/README.md` |

## Release Flow

1. `main`에 push
2. GitHub webhook → `POST /admin/reload` → `git fetch` + `reset --hard origin/main` + 메모리 reload
3. 그래프 검증(L1~L6)에서 ERROR면 **503 + 구 데이터 유지** — 부팅 fail-fast가 배포 게이트 역할을 한다(WORK-007)
4. 컨테이너 이미지가 바뀐 경우에만 홈서버에서 `docker compose up -d --build`

코드 변경 없이 md만 바뀌면 2~3단계로 끝난다. 발행 파이프라인이 push에 의존하는 이유다.

## Open

- `slack-bridge` 서비스 제거와 `SLACK_*`·`CAPTURE_*` env의 `back` 이관 시점 — 흡수 work.
- CI PR merge-gate는 PR 플로가 없어 보류 중이다([[spec-004-graph-validation|KDEV-SPEC-004]] §7).
