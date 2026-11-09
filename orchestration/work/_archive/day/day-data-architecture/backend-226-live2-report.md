# Delivery #226 fix1 뒤 실물 확인 (live2) — KOS 데모 지점 · 조회만

## 상태: done — `needs_master` 경로가 실물에서 한 번 돌았다. 코드 · 테스트 변경 없음.

## 순서 (2026-11-06 · UTC)

1. compose `up -d --wait postgres redis`(11042 · 11043).
2. shell 에서 `DB_SCHEMA=day_livecheck` 를 넣어 compose 값(`day_dev`)을 덮고 이미지 빌드 → `migrate` 를 빈 스키마에
   실행(0001_baseline → 0002_data_model). dev 가드: `APP_ENV=dev` + `day_prod` 아님 — 통과.
3. `--profile app up -d --wait`(api 11040 · worker · scheduler) — **연결 시드 전에** 띄웠다. scheduler 시작 때의 기준 정보
   주기 회차는 병원 0곳을 보고 끝난다 → 첫 일정 회차가 기준 정보 없는 병원을 만나게.
4. 01:16:46 `scripts/seed_demo_connection.py`(env 값만 · 데모 지점 키) → 병원 · 브랜드 · `crm_connection(is_demo=true)`.
5. 약 35초 로그 · 건수 확인 → api · worker · scheduler 정지 → `DROP SCHEMA day_livecheck CASCADE` → `down`.
   남은 스키마는 `day_dev` 하나(그 안 데이터는 건드리지 않음 — 방문 10건 그대로).

## 로그 (값 없이 · 병원 id 는 `<hid>`)

```text
01:16:51.154 emr outbox hospital=<hid> done {'sent': 0, 'retry': 0, 'failed': 0, 'conflict': 0}
01:16:51.210 KOS open token issued hospital=<hid>
01:16:51.458 KOS internal token issued hospital=<hid>
01:16:51.523 emr schedules hospital=<hid> done {upserted: {}, absent: {}, skipped: {}, outbox: {…0}, 'needs_master': True}
01:16:51.524 taskiq Executing task day.emr.sync_master_hospital
01:16:51.976 emr master hospital=<hid> done {upserted: {zone 2, room 41, reservation_group 13,
             reservation_group_capacity 14, reservation_group_timetable 91, job_role 15, staff 80,
             customer_category 7, funnel 14}, absent: {}, skipped: {}}
01:17:01.326 emr schedules hospital=<hid> done {…, 'needs_master': False}
01:17:11.150 emr schedules hospital=<hid> done {…, 'needs_master': False}
01:17:21.173 emr schedules hospital=<hid> done {…, 'needs_master': False}
```

- 첫 일정 회차 `needs_master: True` → 같은 ms 대에 태스크가 `day.emr.sync_master_hospital` 발행 → 0.45초 뒤 기준 정보 `done`
  → 다음 10초 회차부터 `needs_master: False`. 일정 회차는 5번 모두 `done`.
- 로그 집계: `needs_master: True` 1 · 기준 정보 `done` 1 · 일정 `done` 5 · **잠금 skip 0** · timeout 0 · error/traceback/exception 0.
- 로그 누출 확인(W5): 테넌트 id 전체 문자열 0건 · `tenant=` 0건 · httpx 줄 0건(URL 이 찍히지 않음).

## 테이블별 건수 (`day_livecheck`, DROP 전)

| 테이블 | 건수 |
|---|---|
| brand · hospital · crm_connection | 1 · 1 · 1 |
| zone · room | 2 · 41 |
| reservation_group · capacity · timetable | 13 · 14 · 91 |
| job_role · staff | 15 · 80 (`deleted_at` 있는 직원 0) |
| customer_category · funnel_category · funnel | 7 · 0 · 14 |
| customer_type · customer · visit · visit_flow_log · visit_occupied_resource | 0 (오늘 일정 0건) |
| external_outbox · event_log | 0 · 0 |

`external_ref`(전체 · `is_present_in_source=true`): zone 2/2 · room 41/41 · reservation_group 13/13 · job_role 15/15 ·
staff 80/80 · customer_category 7/7 · funnel 14/14.

## 이상 · 참고

- **데모 지점 오늘(KST 2026-11-06) 일정은 또 0건** — 일정 · 고객 행은 이번에도 0. 일정 반영 경로는 #226 1차 실물(시계 이동)과
  테스트로만 확인돼 있다.
- 유입 채널이 1차 실물 13 → 이번 14 — 데모 지점 쪽 코드가 하나 늘어난 것으로 보인다(DAY 쪽 문제 아님).
- 첫 일정 회차의 `needs_master` 는 「연결을 scheduler 시작 뒤에 넣은」 경우에만 보인다. 평소(연결이 먼저 있음)는 scheduler 시작
  때의 기준 정보 주기 회차가 먼저 돈다 — 그때 일정 회차와 겹치면 일정 쪽은 `needs_master: True` 로 기준 정보를 한 번 더 발행할 수
  있고, 그 발행은 기준 정보 잠금에 걸려 skip 된다(이번엔 겹치지 않아 skip 0). 해 없음.
- 코드 · 테스트 변경 없음. KOS 쓰기 0(outbox 0건 · `SUPPORTED_WRITES` 비어 있음).
