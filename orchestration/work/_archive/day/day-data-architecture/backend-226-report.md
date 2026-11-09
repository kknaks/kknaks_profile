# Delivery #226 KOS 연동(폴링 · external_ref · outbox 기반) 결과 보고

## 상태: done (커밋 안 함 · 브리프대로)

워크트리 `CENTURION_DAY/day-data-architecture` · 브랜치 `kknaksss/day-data-architecture` · #224 · #225 위.
모델 · migration 은 건드리지 않았다.

## 수행 — 파일 · 모듈

| 경로 | 내용 |
|---|---|
| `backend/day/emr/base.py` | 업체 공통 인터페이스 `EmrAdapter`(fetch_master · fetch_schedules · supports_write · send) · `EmrError` · `WriteNotSupportedError` · `OutboxCommand` |
| `backend/day/emr/normalized.py` | 우리 형식 dataclass(NZone · NRoom · NReservationGroup · NJobRole · NStaff · NCode · NCustomer · NVisit · NOccupiedResource · NRequestedProcedure …) · `MappingError` |
| `backend/day/emr/factory.py` | `ConnectionConfig` → 업체 어댑터. worker 프로세스 안에서 병원별 어댑터(토큰) 재사용, 설정 지문이 바뀌면 새로 |
| `backend/day/emr/sync.py` | 반영 — `external_ref` upsert(`ON CONFLICT … WHERE deleted_at IS NULL`) · DAY 행 upsert(동기화가 아는 칸만) · 사라짐 표시 · 되살리기 |
| `backend/day/emr/outbox.py` | 적재(advisory lock 으로 방문별 seq) · 발송(transaction 밖) · 확인 · 재전송 · 실패/막힘 + `event_log outbox.failed` · 조건부 UPDATE(원자적 전이) |
| `backend/day/emr/kos/client.py` | KOS HTTP — 공개 토큰 · 내부 sign-in + get-user-account · **내부 요청에 KOS 웹 헤더** · 401 재시도 1회 · 토큰은 메모리만 |
| `backend/day/emr/kos/mapper.py` | KOS 응답 ↔ 우리 형식(SPEC 표의 KOS 칸) |
| `backend/day/emr/kos/__init__.py` | `KosAdapter` — 경로 · 토큰 선택. **`SUPPORTED_WRITES` 비어 있음(쓰기 0개)** |
| `backend/day/services/crm_connections.py` | 동기화할 연결(dev = is_demo 만) · 데모 연결 시드 · 기준 정보 유무 |
| `backend/day/services/emr_sync.py` | 한 회차 — 병원별 Redis 잠금 · 연결 재확인 · 받기(밖) → 반영 · commit. 첫 일정 회차에 기준 정보가 없으면 먼저 받음 |
| `backend/day/tasks/emr.py` · `tasks/__init__.py` | taskiq 태스크 6개(주기 3 + 병원별 3) — `day.tasks` CLI 모듈 인자로 등록(#224 W3) |
| `backend/day/public.py` | `seed_demo_kos_connection(...)` 만 내보냄 |
| `backend/common/config.py` | `REDIS_SOCKET_*_TIMEOUT_SECONDS`(W5) · `SYNC_*_INTERVAL_SECONDS` · `OUTBOX_SEND_INTERVAL_SECONDS` · `SYNC_LOCK_TTL_SECONDS` · `EMR_HTTP_TIMEOUT_SECONDS` · `HOSPITAL_TIMEZONE` |
| `backend/common/redis.py` | 클라이언트 timeout 을 헬스체크와 분리(W5) · `try_lock`(SET NX EX · 가진 쪽만 푸는 Lua) |
| `scripts/seed_demo_connection.py` | 로컬 시드 — 값은 env(`DAY_SEED_*`)만 |
| `deploy/compose.local.yaml` | worker · scheduler `depends_on migrate: service_completed_successfully`(W9) · `KOS_*_BASE` env 전달 |
| `deploy/local.env.example` | KOS 공개 호스트(비밀값 아님) · `DAY_SEED_*` 자리표시자 |
| `pyproject.toml` · `uv.lock` | `httpx` 를 dev → 런타임 의존성으로 |
| `AGENTS.md` | 실행 명령에 시드 한 줄 |
| `backend/tests/day/emr/` | fixtures(값 가짜) · mapper contract · client/adapter · sync · outbox · 서비스(잠금 · is_demo · 주기) |
| `backend/tests/common/test_redis.py` · `tests/architecture/test_emr_vendor_boundary.py` | W5 · 잠금 · 업체 패키지는 `emr/factory.py` 만 import |

## 검증

- `scripts/test.sh -q` → **203 passed**(로컬 compose PostgreSQL · Redis, `DAY_REQUIRE_INFRA=1`). 이번에 더한 테스트 50개.
- `uv run ruff check backend` → All checks passed.
- 비밀값 검사: 바뀐 · 새 파일 전부에서 데모 키 · 테넌트 id · 계정 · 비밀번호 문자열 0건. `deploy/local.env` 는 gitignore 확인.

### 실물 1회 (KOS 데모 지점 · 조회만)

순서: compose `migrate` → `scripts/seed_demo_connection.py`(두 번 — 같은 hospital id, 행 안 늘어남) →
`--profile app up`(api · worker · scheduler) → 로그 확인 → `down`. 포트 11040 · 11042 · 11043 만.

- scheduler 가 뜨자마자 `sync_master` · `sync_schedules` · `send_outbox` 발행, worker 가 병원별 태스크 실행.
  10초마다 일정 회차 6번 `done`, 오류 · traceback 0건.
- **잠금이 실제로 동작**: 시작 직후 주기 `sync_master` 와 첫 일정 회차의 「기준 정보 먼저」가 겹쳐
  `emr master … skipped: previous run still holds the lock` 1건.
- **데모 지점의 오늘(2026-11-06 KST) 일정은 0건**이라 10초 폴링은 0행을 반영했다(예외 아님). 그래서 같은
  서비스 경로(`emr_sync.run_schedules`)를 **시계만 4일 앞으로 옮겨** 한 번 더 돌렸다(스크래치 스크립트 ·
  커밋 안 함 · 조회만). 그 결과가 아래 일정 건수다.

테이블별 건수(`day_dev`):

| 테이블 | 1회차 후 | 2회차 후 |
|---|---|---|
| zone | 2 | 2 |
| room | 41 | 41 |
| reservation_group | 13 | 13 |
| reservation_group_capacity | 14 | 14 |
| reservation_group_timetable | 91 | 91 |
| job_role | 15 | 15 |
| staff | 80 | 80 |
| customer_category | 7 | 7 |
| funnel_category | 0(데모가 비어 있음) | 0 |
| funnel | 13 | 13 |
| customer_type | 1 | 1 |
| customer | 8 | 8 |
| customer_category_link | 1 | 1 |
| visit | 10 | 10 |
| visit_flow_log | 10 | 10(단계 그대로라 안 늘어남) |
| visit_occupied_resource | 10 | 10 |
| visit_requested_procedure · visit_occupied_resource_doctor | 0(그날 응답에 없음) | 0 |
| external_outbox · event_log | 0 | 0 |

`external_ref` entity_type 별(전체 · `is_present_in_source=true`) — 2회차 뒤에도 같다:
zone 2/2 · room 41/41 · reservation_group 13/13 · job_role 15/15 · staff 80/80 · customer_category 7/7 ·
funnel 13/13 · customer_type 1/1 · customer 8/8 · visit 10/10 · visit_occupied_resource 10/10.

그 밖: `crm_connection.is_demo = true`, `config` 의 `open_api_key` · `system_email` · `system_password` 는
`enc:` 암호문(`tenant_id` 는 #225 대로 평문). `staff.is_system_account = true` 1명(sign-in 계정).

## 완료 조건 대조

| | 증거 |
|---|---|
| A1 | 실물 1회(위 표). 외부 id 는 `external_ref` 에만 — DAY 칸은 DAY id(테스트 `test_오늘_일정과_그_고객` 이 `visit.room_id == external_ref(room-2).entity_id` 확인). 차트번호는 SPEC 대로 `customer.chart_number` + `external_ref.external_number` |
| A2 | 주기 라벨 `sync_schedules {interval:10}` · `sync_master {interval:3600}` · `send_outbox {interval:10}`(`test_주기는_10초_3600초`). 느린 앞 회차가 잠금을 쥔 동안 다음 회차 `skipped_locked`, 끝나면 다시 `done`(`test_앞_회차가_안_끝났으면_다음_회차는_건너뛴다`). 잠금은 병원 · 일마다 따로, 남의 잠금은 안 푼다. 실물 로그 1건 |
| A3 | 사라진 구역 · 방문 → `deleted_at = 그 회차 시각` + `is_present_in_source = false`, 다시 나타나면 되살림(`test_외부에서_사라진_행은_deleted_at_과_is_present_in_source`). 줄어든 희망 시술 · 정원 · 분류 연결 · 지정 의사도 `deleted_at`. mapper 가 뺀 일정은 사라짐으로 표시하지 않는다 |
| A4 | `tests/day/emr/fixtures/`(모양만 데모 응답, 값은 가짜) + `test_kos_mapper.py` 14개 — 빈 문자열 · 없는 칸 = None, 모르는 enum · 필수 칸 없음 = 그 항목 제외, 성별 미지정 · 채널 미지정 = None, 자정이 아닌 생년월일 = None, 30분 · false 같은 기본값을 지어내지 않음 |
| A5 | `test_내부_API_요청에는_브라우저_헤더가_실린다`(sign-in · get-user-account · tenants/… 에 User-Agent · Origin · kos-client-uri) · `test_공개_API_에는_브라우저_헤더를_싣지_않는다` |
| A6 | `test_dev_는_데모_연결만_동기화한다`(dev = 데모만, prod = 데모 + 실제. 끊긴 연결 · 꺼진 병원 제외) · `test_dev_에서_실제_병원_연결은_한_회차도_돌지_않는다`(어댑터 호출 0) |
| A7 | `test_outbox.py` 8개 — 적재 seq · pending→sent→confirmed · 조회 2번 안 맞음 → 재전송 · 오류 3번 → failed + 뒤 쓰기 막힘 + event_log · 거절 뒤 이미 맞으면 confirmed · 한 번도 안 보낸 건 확인 안 함 · 뒤 쓰기가 같은 칸을 바꾸면 앞 쓰기 confirmed · 지원 안 하는 쓰기 → failed(조용히 안 넘김). 가짜 어댑터로만 |

#224 W3(태스크 CLI 등록) · W5(Redis timeout 분리 — `test_공용_클라이언트_timeout_은_헬스체크와_따로다`) · W9(compose) 반영.

## 호출마다 API · 토큰

cc-prototype(`origin/main:procedure/back/app/kos/`)과 같은 방식. 「내부」는 전부 KOS 웹 헤더(User-Agent · Origin ·
kos-client-uri) + `Authorization: Bearer <sign-in 토큰>`, 「공개」는 `Authorization: <exchange-token 토큰>`(Bearer 없음 ·
웹 헤더 없음).

| 무엇 | 주기 | API | 토큰 | 경로 · 요청 | cc 와 |
|---|---|---|---|---|---|
| 공개 토큰 받기 | 필요할 때 · 401 | 공개 | `open_api_key` | `open/authorization/commands/exchange-token {key}` | 같음 |
| 내부 로그인 | 필요할 때 · 만료 10분 전 · 401 | 내부(테넌트 없음) | 시스템 계정 email/password | `common/v1/user/commands/sign-in` | 같음(만료 시각이 없으면 cc 는 12시간 가정 — DAY 는 가정하지 않고 401 때 다시) |
| 시스템 계정 id | sign-in 직후 | 내부 | Bearer | `tenants/{t}/v1/account/queries/get-user-account {}` | 같음 |
| 구역 | 1시간(+ 일정 회차에 구역 id 가 없을 때) | 공개 | 공개 토큰 | `schedule/open/zone/v1/queries/get-zones {}` | 같음 |
| 방 | 1시간 · 구역마다 | 내부 | Bearer | `tenants/{t}/schedule/zone/room/v1/queries/get-rooms {zoneId}` | 같음(cc 는 기본 구역 + 나머지 구역) |
| 예약 그룹 | 1시간 | 내부 | Bearer | `tenants/{t}/schedule/group/v1/queries/get-reservation-groups {deleted:false, zoneIds}` | 같음 |
| 직무 | 1시간 | 내부 | Bearer | `tenants/{t}/role/v2/queries/get-roles {}` | cc 없음(로그인 때 받는 값 — SPEC 04) |
| 직원 | 1시간 | 내부 | Bearer | `tenants/{t}/account/v2/queries/get-accounts {}` | **다름** — cc 는 공개 `account/open/v1/queries/get-accounts`. SPEC 04 `staff` 칸(realName · licenseNumber · roleId)이 내부 응답에만 있다 |
| 코드 | 1시간 | 내부 | Bearer | `tenants/{t}/meta/codes/v1/queries/get-codes {category}` × `VISITOR_CATEGORY` · `FUNNEL_CATEGORY` · `FUNNEL` | cc 는 FUNNEL 만 |
| 오늘 일정 + 고객 | 10초 | 내부 | Bearer | `tenants/{t}/schedule/v2/queries/get-schedules-grouped-by-zone {zoneIds, startDateTimeUtc, endDateTimeUtc}` | 같음(cc 는 한 구역 · DAY 는 병원 전 구역) |
| 쓰기(commands) | — | — | — | **하나도 열지 않음**(`SUPPORTED_WRITES = ∅`) — 실제로 보낸 쓰기 0건 | 코디 결정 1 |

직무 태그: 내부 API 는 `roleTags` 가 정수(1~7). 정수 ↔ 이름은 **데모 직원 80명 전원**의 공개(문자열) · 내부(정수)
응답 대조로 확인(80/80 일치) — 추정 아님.

## 공개 API 로 옮길 수 있는 호출 (후보만 · 이번엔 안 옮김)

| 지금(내부) | 공개 후보 | 막히는 것 |
|---|---|---|
| 직원 `account/v2/get-accounts` | `account/open/v1/queries/get-accounts`(cc 가 쓰던 것) | realName · licenseNumber · roleId 없음 → `staff.real_name` · `license_number` · `job_role_id` 를 못 채움 |
| 예약 그룹 `schedule/group/v1/get-reservation-groups` | `schedule/open/v1/queries/get-reservation-groups` | 응답 칸 비교 안 함(조회 안 해 봄) |
| 오늘 일정 `get-schedules-grouped-by-zone` | `schedule/open/v1/queries/get-schedules-by-flow-step` · `get-schedule-detail` · `get-schedules-summarized-by-tasks` | 응답 칸 비교 안 함. 방 배정(`roomAssignedDateTimeUtc`) · occupiedResources 가 공개에 있는지 확인 필요 |
| 고객 상세(아직 안 부름) | `visitor/open/v1/queries/get-visitor` | 데모에서 `{visitorId}` 본문은 400 — 요청 칸 이름 확인 필요. 내부 v2 보다 칸이 적다(SPEC 02) |
| 방 · 직무 · 코드 | 공개에 같은 작업 없음(KOS 개발자 문서 목록 기준) | 옮길 곳 없음 |
| 로그인(sign-in) | 없음 | 공개 API 로 직원 로그인 불가 |

## OQ-02-2 확인 (결정하지 않음 · 칸 이름 · 타입만)

- 내부 `visitor/v2/queries/get-visitor {id}` 응답 `data.updatedDateTimeUtc`: **있음 · string**(`createdDateTimeUtc` 도 string).
- 일정(`get-schedules-grouped-by-zone`) 각 건 `updatedDateTimeUtc`: 있음 · string — 일정 안 `visitor` 에는 **없음**.
- 내부 `account/v2/get-accounts` 각 건 `updatedDateTimeUtc`: 있음 · string.
- 바뀐 고객만 골라 주는 조회 조건(`updatedDateTimeUtc` 필터)이 있는지는 보지 않았다 — 요청 칸은 HAR 로 확인할 일.

## 응답에 없어 비워 둔 칸 · 추정하지 않은 것

| 칸 | 왜 비었나 |
|---|---|
| `staff.default_zone_id` | 내부 `account/v2` 응답에 `defaultWorkingZoneId` 없음(80/80 null) |
| `staff.real_name` · `license_number` | 응답에 값이 없는 직원(16/80 · 77/80) — 표시 이름으로 채우지 않음 |
| `staff.account_id` | 로그인 Delivery 가 잇는다 — 동기화는 이 칸을 고치지 않는다 |
| `customer` — `registered_at` · 여권 칸 · 주민/외국인 등록번호 · `passport_expiry_date` · 추가 전화 · email · 주소 · 지정 의사/상담사 · 유입 · 추천인 · 동의 3개 | 10초 폴링은 **일정 안 `visitor`** 만 읽는다(cc 방식). 이 칸들은 내부 `get-visitor` 에만 있다 — 고객 상세 조회는 남은 것(OQ-02-2 와 같이) |
| `customer.gender` | KOS `MALE`/`FEMALE` → `male`/`female`, `GENDER_UNSPECIFIED` → null (값 목록은 OQ-02-1) |
| `visit.connected_channel` | KOS `Channel_UNSPEICIFED` → null |
| `visit.funnel_id` 등 참조 | 기준 정보에 없는 id 면 null(실물 10건 중 9건은 그날 예약에 유입이 없음) |
| `visit_requested_procedure.product_option_id` | 1차 비움(SPEC) — KOS 옵션 id 를 DAY 칸에 넣지 않음. 시술권은 `option_type` · 가격 없음 |
| `funnel.category_id` · `funnel_category` | 데모 응답에 카테고리 칸 · 목록이 없음 |
| `reservation_group_timetable` 시각 | KOS 가 UTC 날짜시각으로 준다 → `HOSPITAL_TIMEZONE`(기본 Asia/Seoul) 시계 시간(cc 와 같음). 빈 문자열 = null |
| `visit_flow_log.changed_at` | `flowStepUpdatedDateTimeUtc` 가 없으면 DAY 가 그 단계를 처음 본 시각(필수 칸) |

필수 bool 을 채운 근거:
- `staff.is_system_account` — sign-in 한 시스템 계정(get-user-account id)만 true, 나머지 false. KOS 응답에 「시스템 계정」 칸은
  없다 — cc `KOS_EXCLUDE_ACCOUNT_IDS` 의 시스템 계정 부분만 옮김. 공용 계정 등 다른 「사람 아님」 표시는 정할 것(코디 확인).
- `staff.is_active` = `activate` · `zone.is_default` = `isDefault` · `timetable.is_enabled` = `enabled` ·
  `visit.consultation_required` / `sedation_required` = 응답값. 없으면 그 항목을 뺀다(기본값 없음).

## 이슈 · 코디가 확인할 것

1. **데모 지점 오늘 일정 0건** — 실물 일정 건수는 같은 경로를 시계만 4일 앞으로 옮겨 얻었다. 그 10건 방문은 로컬 `day_dev` 에
   남아 있다(오늘 범위 밖이라 10초 폴링이 건드리지 않음). 지우려면 로컬 볼륨을 비우면 된다.
2. **다른 날로 옮긴 예약** — 오늘 범위에서 빠지면 `deleted_at` · `is_present_in_source=false` 가 되고, 그날 다시 보이면
   되살아난다(A3 를 「오늘 범위 안에서 사라짐」으로 읽음). 고객은 일정으로만 보므로 사라짐 표시를 하지 않는다.
3. **고객 차트번호 충돌**(KOS 가 지운 고객의 번호를 다른 고객이 쓰는데 DAY 는 지운 줄 모를 때) — 그 고객 · 그 방문만
   savepoint 로 빼고 나머지는 들어간다(`skipped.customer`). 고객 삭제를 알 길(상세 조회)이 생기면 풀린다.
4. `external_outbox (visit_id, seq)` 에 유일 제약이 없다(#225 모델) — 적재는 방문별 advisory lock 으로 seq 를 매긴다.
   제약을 원하면 migration 이 필요(이번엔 안 함).
5. 직원을 내부 `account/v2` 로 받는다(cc 와 다른 한 곳) — 내부 API 의존이 하나 늘었다.
6. 일정 · 기준 정보는 잠금이 따로라 동시에 돌 수 있다(같은 어댑터 · 토큰은 asyncio 잠금으로 겹쳐 받지 않음).

## 남은 것

- 상담(`consultation` · `consultation_procedure`) · 작업(`visit_task` …) 동기화 — 시술 현황 Delivery.
- 고객 상세(내부 `get-visitor`) — OQ-02-2 결정 뒤(바뀐 고객만 받을지).
- 첫 실제 쓰기 — `SUPPORTED_WRITES` 에 경로를 열고 `expect` 를 정한다(시술 현황 Delivery).
- 공개 API 이전 — 위 후보 표.
- 이 Delivery 의 커밋 · PR #228 은 코디 · 사용자 몫(브리프: 커밋 금지).
