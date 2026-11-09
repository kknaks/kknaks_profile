# DAY v2 시스템 아키텍처

2026-11-03 사용자와 정함. 데이터 설계는 [../erd/README.md](../erd/README.md).

## 이미 정한 것 (앞 논의에서)

- 레포 `MediSolveAIDev/CENTURION_DAY` `v2-dev` — centurion 모양(`backend/day/` + `runtime/`), 구조는 레포 `AGENTS.md`.
- 웹 = Jinja2 + HTMX(centurion admin 방식) · 앱 = Flutter(iOS · 축소판).
- DB = PostgreSQL(`day` 스키마) · SQLAlchemy 2 async · alembic.
- KOS 연동: 폴링(일정 10초 · 기준 정보 1시간) · 쓰기 큐(`external_outbox`) · 로그인 = KOS sign-in.
- 배포 = DAY 전용 Azure 서버(나중) · `APP_ENV` 로 dev / prod.

## 정한 것 (2026-11-03)

| # | 주제 | 결정 | 근거 |
|---|---|---|---|
| 1 | 프로세스 | **`api`(DAY 내부 동작 — 화면 · JSON API · SSE · 버튼 처리) 와 `worker`(KOS 동기화 — 폴링 · 쓰기 큐 발송/확인 · 푸시) 를 나눈다.** `api` 는 KOS 를 부르지 않는다(로그인 · 잔여 시술권 같은 바로 조회만 예외) | KOS 가 느리거나 멈춰도 시술실 화면 · 버튼이 돈다. cc 는 한 프로세스(`lifespan` 의 asyncio 태스크)라 서로 영향을 줬다 |
| 2 | 백그라운드 도구 | **taskiq**(사용자 2026-11-03) — centurion Linky 와 같은 도구. `worker`(taskiq worker) + 주기 작업은 `scheduler`(taskiq scheduler · `LabelScheduleSource`) | centurion 통합 · 선례 |
| 3 | Redis | **둔다**(정식) — taskiq 브로커 · 결과 저장 · 프로세스 사이 화면 알림(SSE 갱신 신호) · 잠금 | 사용자 2026-11-03 |
| 4 | taskiq 브로커 | **Redis**(`taskiq-redis`) — RabbitMQ 를 두지 않는다(centurion Linky 와 다름). VM 메모리를 아낀다 | 사용자 2026-11-03 |
| 5 | 10초 폴링 | **taskiq scheduler 의 `interval` 스케줄** — `schedule=[{"interval": 10}]`(초 단위 · 정수 · 1초 이상). 기준 정보는 `interval: 3600`. taskiq 0.12.6(centurion 고정 버전)에서 지원 확인 | taskiq `scheduler/scheduled_task/v2.py` · 2026-11-03 확인 |
| 7 | DB · 환경 분리 | **관리형 PostgreSQL 1대 · DB 1개(새 DB 권한 없음) → 스키마로 env 분리** — `DB_SCHEMA=day_dev` / `day_prod`. 코드는 같고 env 만 다르다: 모델 `MetaData(schema=…)` · alembic `version_table_schema` · 접속 `search_path` 를 이 값으로. DB 계정도 스키마별로 둘(dev 계정은 `day_prod` 권한 없음). migration 은 dev 에 먼저 → prod 에 같은 것 | 사용자 2026-11-05 |
| 8 | 지금 범위 | **개발(dev)만 먼저** — 로컬 compose PostgreSQL 도 같은 방식(`DB_SCHEMA`). prod 는 배포 때 env 만 바꿔 같은 migration 적용 | 사용자 2026-11-05 |
| 6 | 중복 실행 막기 | 병원별 Redis 잠금 — 같은 병원을 두 번 폴링 · 같은 쓰기를 두 번 보내지 않는다(이전 폴링이 10초를 넘기면 다음 회차는 건너뜀) | 코디 기본값 |

버튼 하나의 흐름(예: 시술 완료): `api` 가 DB 에 쓰고 쓰기 큐에 넣고 「반영 중」으로 바로 응답 → `worker` 가 KOS 에 보내고 다음 조회로 확인 →
확인되면 「반영 중」이 풀리고 Redis 로 `api` 에 알림 → SSE 로 화면 갱신.

## 위험 — KOS 내부 API 차단 (2026-11-04 확인)

2026-11-03 18:23 KST 부터 KOS 내부 API 가 브라우저 UA 가 아닌 요청을 403 `Unsupported client.` 로 막는다. cc-prototype 이 KOS 웹 헤더
(User-Agent · Origin · kos-client-uri)를 실어 풀었다(#20 · `77173cf`). DAY 의 로그인 · 일정 · 쓰기가 전부 내부 API 라 **같은 헤더가 필요**하고,
KOS 가 더 막으면 멈출 수 있다 — 공식 API(공개 API · KOS 요청)로 옮길 수 있는 것은 옮길 후보로 둔다.

## 서버

Azure VM 2코어 / 4GB(예정) 기준 예상 메모리: caddy ~50MB · api 768MB · worker 384MB · scheduler 384MB · redis 256MB ≈ 1.9GB — 여유 있음(RabbitMQ 없음).
조건: PostgreSQL 은 VM 밖(Azure 관리형) · 파일은 Azure Blob. centurion 은 prod `Standard_B2ms`(2/8) · stg `Standard_B2s`(2/4) · DB 는 VM 밖 PostgreSQL.

요청할 것: **VM 2코어/4GB + Azure 관리형 PostgreSQL(1대 · DB 1개 — 확정 2026-11-05) + Azure Blob**.

## 배포 결정 (사용자 2026-11-08 ~)

| 주제 | 결정 |
|---|---|
| 서버 · DB 개수 | **dev 와 prod 는 VM 한 대에 같이**(Azure VM 2코어/4GB · 한 대) · **관리형 PostgreSQL 도 한 대**(DB 1개 · 스키마 `day_dev` / `day_prod` 로 나눔) |
| 배포 시작(브랜치) | **브랜치 `dev` · `prod` 로 관리** — `v2-dev` 가 `dev` 가 되고 `prod` 는 새로(사용자 2026-11-08 · 추천) — `dev` 에 들어가면 dev 배포 · `prod` 에 들어가면 prod 배포(사용자 2026-11-08). prod 는 dev 에서 확인한 같은 이미지(조사 D5) |
| 도메인 · DNS | dev = **`day-dev.medisolveai.com`** · prod = **`day.medisolveai.com`** · DNS 는 사용자가 관리 |
| HTTPS | Caddy 자동 발급(ACME) |
| 백업 | **기본값만**(관리형 PostgreSQL 자동 백업) — 스키마 단위 백업 등은 나중 |
| 배포 시간 | 제한 없음 — 배포는 사용자 혼자 관리 |
| Azure 권한 | VM · Azure 권한은 사용자에게 있다 — VM · 네트워크 · Key Vault · ACR 권한 · 배포 계정(OIDC) 준비는 사용자가 |
| 그 밖 | 조사(`work/day-data-architecture/researcher-deploy-report.md` §3) 추천대로: compose project 셋(`day-edge` Caddy 하나 · `day-dev` · `day-prod`) · redis 환경마다 · dev 메모리 상한 낮춤(첫 배포 뒤 실측 · 모자라면 VM 2/8) · 회사 공용 ACR · migration dev 자동 / prod 따로 승인 · 비밀값 Key Vault · JSON 로그(구현 필요) · 롤백 = 이전 이미지 · prod 첫 배포는 `KOS_TRIAL_WRITES_ON_LIVE=false` |
| 받은 서버 · DB(인프라 담당 2026-11-09) | **VM `vm-centurion-day-prod`** — 공인 IP `52.231.77.47` · B2s(2코어/4GB) · Ubuntu 24.04 · 디스크 64GB · 22/80/443 열림 · 사용자 `azureuser`(sudo) · 키 `azure_crmproject` · 처음엔 docker 없음 · 로컬 별칭 `ssh day-vm`<br>**DB `pg-centurion-day-prod.postgres.database.azure.com`** — PostgreSQL 16 · DB 이름 `day` · 외부 공개 꺼짐(VM 경유 SSH 터널만 · `ssh -N day-db` → 로컬 15432) · TLS verify-full · 관리 계정 `dayadmin`(초기 설정용 — 앱은 별도 계정) · 11-09 기준 스키마 `public` 만(`day_dev` · `day_prod` 미생성) · dayadmin CREATE 권한 있음<br>VM · DB 삭제 방지 잠금. **비밀번호는 레포에 두지 않는다** — 사용자 로컬 `~/.pgpass` 에만 |
| 앞단(리버스 프록시) | **Caddy** — VM 안 맨 앞 · HTTPS 인증서 자동 발급 · 갱신 · 외부엔 80/443 만 · api 로 전달(SSE 포함). centurion 과 같은 방식(`deploy/Caddyfile` · `compose.caddy.yaml`) |

## 기본값 (코디 추천 — 바꿀 때만 말하기)

| 주제 | 기본값 |
|---|---|
| 화면 실시간 갱신 | SSE(cc 와 같음) — HTMX 는 SSE 확장, 앱은 cc 방식. `worker` 가 바꾼 것은 Redis pub/sub 로 `api` 에 알린다 |
| 병원이 늘 때 폴링 | 병원마다 폴링 태스크 1개 + 병원별 Redis 잠금(위 6) |
| 파일 저장 | Azure Blob(로컬은 디스크) — 신분증 사진 · 채팅 첨부 |
| 푸시 | APNs 직접(cc 방식) — 키는 서버 비밀값 |
| 비밀값 · 설정 | 서버 env → 나중에 Azure Key Vault(centurion 환경변수 가이드) |
| 로그 · 감시 | 구조화 JSON 로그(centurion 형식) |
