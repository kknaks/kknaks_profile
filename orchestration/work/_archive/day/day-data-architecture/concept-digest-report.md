# 개념 소화 리포트 — day-data-architecture 회고 §2

회고: `para/projects/company/day/log/2026-11-09-day-data-architecture.md` §2(8항목)
규약: `para/areas/area.md` §3.3 — aliases grep 으로 먼저 찾고, 있으면 보강(up: · 출처 · 본문 녹이기 · aliases), 없을 때만 새로 + §3.4 맵 한 줄.
결과: **보강 7 · 새로 5** · 회고 §2 8항목 끝에 역링크 · 커밋 안 함.

## 항목 → 개념

| # | 회고 §2 항목 | 처리 | stem | 녹인 것 |
|---|---|---|---|---|
| 1 | 외부 CRM 폴링 + outbox 쓰기(KOS) | 보강 | `back/external-write-queue` | 보내기 전 claim · 오래 멈춘 SENT → 실패 · 쓰기 토큰 = 누른 직원 · 즉시 kick 상한 1초 · 아웃박스 경계에 「화면 상태와 outbox 행 한 트랜잭션」 |
| 1 | 〃 | 보강 | `cs/polling` | 새 절 「웹훅 없는 외부 원천을 따라 읽기」(10초 회차 = 동기화 방식) · webhook · external-write-queue 링크 |
| 2 | KOS 내부 API 브라우저 헤더 | 보강 | `back/public-vs-internal-api` | 정의 8 — UA · Origin · 단계별 `kos-client-uri` 없으면 403 · HAR 은 경로 · 값 모양만 · 확인 안 된 쓰기는 데모에서만(`KOS_TRIAL_WRITES_ON_LIVE`) |
| 3 | 부분 유일 인덱스(soft delete) | 보강 | `db/unique-key` | 경계 — `WHERE deleted_at IS NULL` 부분 유일 인덱스 · upsert `ON CONFLICT` 에 같은 `WHERE` 반복 |
| 4 | 서버 렌더 웹(Jinja2 + HTMX + SSE) | **새로** | `front/server-rendered-fragments` | 화면 라우트 = HTML 조각 · JSON 은 앱 전용 · SSE · CSRF. 상태 전이 노트(`server-authoritative-transition`)는 결이 달라 링크만 |
| 5 | router → service → repository + DB 없는 단위 테스트 | 보강 | `cs/layered-architecture` | DAY 백엔드 사례 · DB 없는 기본 테스트가 계층의 값 |
| 5 | 〃 | **새로** | `qa/test-tiering` | 기본 `-m "not infra"` · 인프라 표식은 전체 실행에서만 · 표식 누락 구멍 |
| 6 | 한 VM 두 환경 배포(OIDC · ACR · run-command · Key Vault) | 보강 | `infra/ci-cd` | 새 절 「한 번 빌드해서 승격」 — prod fast-forward 로 같은 digest · run-command · concurrency group 취소 → 워크플로별 + VM flock · 실패 복구 = 배포 직전 스냅샷 |
| 6 · 8 | 〃 · Azure managed identity | **새로** | `infra/workload-identity` | OIDC 연합(바깥) · 관리 ID(안쪽) · 역할 배정은 별개 단계 · 연합 조건 좁히기 |
| 7 | asyncpg TLS verify-full | **새로** | `back/database-tls-verification` | libpq `sslmode` ≠ asyncpg `ssl` · `PGSSLROOTCERT` · 기동 검사 · `require` 로 낮추기 금지 |
| 7 | 〃 | 보강 | `infra/dev-prod-parity` | 사용 예시 — 터널로 실제 DB 에 앱 코드 경로 그대로 1회 |
| 8 | Azure managed identity · Key Vault 방화벽 | **새로** | `infra/secret-store` | VM 신원으로 읽기 · 서브넷만 허용 · 비밀 넣을 때 로컬 IP 잠깐 열고 닫기 · 외부 시스템 주소도 레포 밖(§3 사고) · 로컬 비밀 파일 → `~/.pgpass`(§3) |

코디 1차 후보 중 `back/webhook` · `infra/reverse-proxy` · `infra/web-application-deployment` 는 보강하지 않았다. 웹훅은 「없어서 폴링」 이라 polling 쪽에 링크만 걸었고, 회고 §2 에 Caddy · war 배치 내용이 없다.

## 맵 추가 줄(`para/areas/area.md` §3.4)

```text
| 514 | `front` | `server-rendered-fragments` | 웹은 서버가 HTML 조각을 그려 갈아 끼우고(HTMX) JSON 은 앱 전용. 상태 · 권한 표시가 서버 한 곳 · 쿠키 세션이라 CSRF |  |
| 515 | `qa` | `test-tiering` | 기본 실행은 DB 없이 수 초, 실제 인프라 시험은 표식으로 전체 실행에서만. 계층 구조가 빠른 층을 만든다 |  |
| 516 | `infra` | `workload-identity` | 장기 키 대신 실행체 자신의 신원(OIDC 연합 · 관리 ID)으로 단기 토큰. 신원과 역할 배정은 다른 단계 |  |
| 517 | `infra` | `secret-store` | 비밀은 레포 밖 보관소, 서버는 자기 신원으로 읽는다. 외부 시스템 주소도 비밀 · 방화벽은 열면 바로 닫기 |  |
| 518 | `back` | `database-tls-verification` | libpq 의 sslmode=verify-full 은 asyncpg 에서 안 먹는다. ssl 인자 + 루트 CA 경로 + 기동 검사 · 실제 DB 로 1회 |  |
```

## 회고 역링크

§2 각 항목 첫 줄 끝에 `[[stem]]`. 1 → external-write-queue · polling / 2 → public-vs-internal-api / 3 → unique-key / 4 → server-rendered-fragments / 5 → layered-architecture · test-tiering / 6 → ci-cd · workload-identity / 7 → database-tls-verification · dev-prod-parity / 8 → workload-identity · secret-store.

## 검증

- 바뀐 · 새 파일 13개의 `[[]]` 전부 레포 stem 으로 풀림(끊김 0)
- 사내 정보: 사람 · 지점 이름 · IP · 계정 ID · KOS 주소 · 키 0. 회고의 「centurion admin」 은 새 노트에서 「사내 기존 관리자 앱」 으로 씀(회고 본문은 안 고침)
- 건드린 파일: `para/areas/area.md` · 개념 12(보강 7 · 새로 5) · 회고 1 · 이 리포트. 커밋 안 함
