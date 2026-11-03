# DAY v2 시스템 아키텍처

2026-11-03 사용자와 정하는 중. 데이터 설계는 [../erd/README.md](../erd/README.md).

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
| 3 | Redis | **둔다**(정식) — taskiq 결과 저장 · 프로세스 사이 화면 알림(SSE 갱신 신호) · 잠금 | 사용자 2026-11-03 |

버튼 하나의 흐름(예: 시술 완료): `api` 가 DB 에 쓰고 쓰기 큐에 넣고 「반영 중」으로 바로 응답 → `worker` 가 KOS 에 보내고 다음 조회로 확인 →
확인되면 「반영 중」이 풀리고 Redis 로 `api` 에 알림 → SSE 로 화면 갱신.

## 확인할 것 (taskiq)

1. **브로커** — centurion Linky 는 RabbitMQ 브로커 + Redis 결과 저장이다. DAY 는 Redis 를 이미 두므로 **Redis 브로커(taskiq-redis)** 로 RabbitMQ 를 빼는 안 —
   VM 2코어/4GB 에서 RabbitMQ(512MB)를 아낀다. 정할 것.
2. **10초 폴링을 taskiq 로 어떻게 돌리나** — centurion 의 주기 작업은 전부 `cron`(분 단위)이다. 10초 주기는 cron 으로 안 된다.
   후보: taskiq 의 초 단위 스케줄 지원 여부 확인 / 폴링 태스크가 끝나면 10초 뒤 자기 자신을 다시 넣는 방식 / worker 안 asyncio 루프(cc 방식) 병행. 정할 것.
3. **중복 실행 막기** — 같은 병원을 두 번 폴링 · 같은 쓰기를 두 번 보내지 않게 병원별 잠금(Redis).

## 서버 (논의 중)

Azure VM 2코어 / 4GB(예정) 기준 예상 메모리: caddy ~50MB · api 768MB · worker 384MB · scheduler 384MB · redis 256MB ≈ 1.9GB — 여유 있음.
조건: PostgreSQL 은 VM 밖(Azure 관리형) · 파일은 Azure Blob. centurion 은 prod `Standard_B2ms`(2/8) · stg `Standard_B2s`(2/4) · DB 는 VM 밖 PostgreSQL.

## 아직 안 본 것

화면 실시간 갱신(SSE 세부) · 병원이 늘 때 폴링 · 파일 저장 · 푸시(APNs) · 비밀값(Key Vault) · 로그/감시.
