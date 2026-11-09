# 리뷰 리포트 — day-data-architecture / code · Delivery #226 KOS 연동 (2026-11-06)

검수 대상: 워크트리 `CENTURION_DAY/day-data-architecture` · 브랜치 `kknaksss/day-data-architecture` · #224 · #225 커밋 위 미커밋 변경(#226) + AGENTS.md 「테스트」 절(2026-11-06 · 코디 추가분).
읽기 전용으로 봤다. 파일 수정 · 커밋 없음. KOS 호출 없음.

## 판정: WARN

계약 A1 ~ A7 은 코드 · 테스트로 확인된다. 「하지 않는 것」 침범도 없다. KOS 쓰기는 0이고, 비밀값 누출도 없다(로그에 테넌트 id 끝 4자리가 남는 것만 예외 — W5).
머지를 막을 FAIL 은 없다. 다만 **W1(기준 정보 매핑 실패 = 사라짐 처리)** 과 **W2(outbox 상태 전이가 DB 테스트에만 있음 — 2026-11-06 규칙 · A7 「단위 테스트」)** 는 머지 전에 고치기를 권한다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| compose `up -d --wait postgres redis`(11042 · 11043) | healthy → 끝나고 `down` 함 |
| `scripts/test.sh -q` (DAY_REQUIRE_INFRA=1) | **203 passed / 16.3s** — 구현 리포트 203 과 같음 |
| `uv run pytest -q -m "not infra"` | **131 passed · 72 deselected / 1.6s** |
| `uv run ruff check backend scripts` | All checks passed |
| 이번 테스트 파일별 (전체 / DB 없이) | `test_kos_mapper` 14/14 · `test_kos_client` 9/9 · `test_emr_vendor_boundary` 2/2 · `test_redis` 3/2 · **`test_outbox` 8/0 · `test_sync` 7/0 · `test_emr_sync_service` 7/0** |
| 비밀값 대조(`deploy/local.env` 값 ↔ 추적 · 미추적 파일 전부 + 구현 리포트) | open_api_key · tenant_id · system_email · system_password **0건**. 브랜드 · 병원 이름(「KOS 데모」 · 「KOS 데모 지점」)은 일반어라 무관. `deploy/local.env` gitignore(`*.env`) 확인 |
| models · migrations diff | 0줄(건드리지 않음 — 브리프대로) |

## 계약 대조 (A1 ~ A7)

| | 판정 | 근거 |
|---|---|---|
| A1 | 같음 | `sync.py:131-175` `Refs.link` — 외부 id 는 `external_ref` 에만 쓴다. DAY 칸은 `lookup` 한 DAY id(`sync.py:787-847`)다. 실물 건수는 워커가 1회 확인했다(리포트 표 · 2회차도 건수 그대로). `test_두_번_반영해도_행이_늘지_않는다` |
| A2 | 같음 | `tasks/emr.py:61-82` interval 10 · 3600 · 10(`test_주기는_10초_3600초`). `common/redis.py:62-79` `SET NX EX` + 토큰 비교 Lua 해제(`test_앞_회차가_…건너뛴다` · `test_잠금은_병원마다_일마다_따로다` · 남의 잠금 유지). TTL 은 W3 참고 |
| A3 | 같음(주의 W1) | `sync.py:177-207` `mark_absent` — `is_present_in_source=false` + `deleted_at`. 되살림은 `link`(true) + upsert `deleted_at=None`. 방문은 「오늘 범위」(`sync.py:884-895`)로 판단하고, mapper 가 뺀 일정은 제외한다(`held_back`) |
| A4 | 같음(작은 지적 W6) | `test_kos_mapper.py` 14개. fixture 값은 가짜다(`*.example.invalid` · `C-0001` · `zone-a` · `+00`/`0000`). 빈 문자열 · 없는 칸은 None, 모르는 enum 은 None 또는 제외 |
| A5 | 같음 | `client.py:144-154` · `test_내부_API_요청에는_브라우저_헤더가_실린다` · `test_공개_API_에는_브라우저_헤더를_싣지_않는다`(sign-in · get-user-account · tenants/… 전부) |
| A6 | 같음 | `crm_connections.py:21-29` `app_env != "prod"` → `is_demo` 만. 병원별 태스크가 `_run`(`emr_sync.py:96-98`)에서 한 번 더 거른다. `test_dev_에서_실제_병원_연결은_한_회차도_돌지_않는다`(어댑터 호출 0) |
| A7 | 동작은 같음 · **테스트 종류가 다름(W2)** | `test_outbox.py` 8개가 전이를 다 덮는다. 다만 모듈 전체가 `pytest.mark.infra` 라 「단위 테스트」가 아니다 |

「하지 않는 것」: 화면 0 · 시술 현황 동작 0 · 알림 0 · prod/DNS 0 · **KOS 쓰기 0** · Vegas 어댑터 0(`factory.py:49` `UnsupportedVendorError` 뿐) · 소켓 0 · 명동점 0(`seed_demo_connection.py` docstring 의 금지 문구뿐). allowed_paths 이탈 없음.

### KOS 쓰기 0 — grep 전수

- `SUPPORTED_WRITES = frozenset()` — `emr/kos/__init__.py:48`.
- 저장소 안 `commands` 문자열: `client.py:31-32`(exchange-token · sign-in = 토큰 받기)뿐이고, 나머지는 테스트(`test_kos_client.py:258` · `test_outbox.py:31` 가짜 경로)다.
- 업체 호출 지점은 `kos/__init__.py:68 · 137 · 173` 셋뿐이다. 173(`send`)은 `supports_write` 가 막는다. `outbox.enqueue` 를 부르는 업무 코드는 0이다(테스트만).
- `test_쓰기는_열려_있지_않다_요청이_나가지_않는다` — 요청 0건을 단언한다.

## FAIL

없음.

## WARN

### W1. 기준 정보에서 매핑 실패로 뺀 행을 「외부에서 사라짐」으로 지운다 — `emr/sync.py:273-295 · 302-326 · 429-497 · 555-572`, `emr/kos/__init__.py:79-131`
- 근거: `fetch_master` 는 필수 칸이 없는 항목을 `keep()` 에서 빼고 수만 `skipped` 에 센다. `apply_master` 는 매핑된 행만 `link` 하고, `mark_absent(seen=link 된 것)` 로 나머지를 전부 `is_present_in_source=false` + `deleted_at` 처리한다. 일정 쪽은 `held_back` 으로 막아 두었는데(`sync.py:873-883`) 기준 정보 쪽에는 이 장치가 없다. 「방 — 구역을 모르면 뺀다」(`sync.py:302`)도 같은 길로 사라짐이 된다.
- 실물: KOS 가 직원 한 명의 `activate` 를 빼거나, 예약 그룹 시간표의 한 요일 `enabled` 를 빼거나, 칸 이름을 바꾸면 그 직원 · 예약 그룹 · 방이 DAY 에서 지워진 것으로 바뀐다. 모든 행이 매핑에 실패하면 `seen` 이 비어 그 종류 **전부**가 지워진다(`mark_absent` 는 `seen` 이 비면 `notin_` 조건을 빼기 때문). 그래도 `external_ref.deleted_at` 은 그대로라 방문은 여전히 그 직원 · 방을 가리킨다 → **지워진 행을 가리키는 방문**이 생긴다.
- 고칠 방향: `NMasterData` 에 종류별 「응답에 있었던 외부 id」(매핑 실패 포함)를 싣고 `seen` 에 합친다. 일정의 `skipped_external_ids` 와 같은 방식이다. 최소한 `skipped[kind] > 0` 인 종류는 그 회차에 사라짐 표시를 하지 않는다. 테스트는 DB 없이 「skipped 가 있는 종류는 absent 후보에서 빠진다」로 쓰고, infra 로 1건 확인한다.

### W2. outbox 상태 전이 · 동기화 규칙이 DB 테스트에만 있다 — `tests/day/emr/test_outbox.py:28` · `test_sync.py:43` · `test_emr_sync_service.py:31` (AGENTS.md 「테스트」 2026-11-06 · A7 「단위 테스트」)
- 근거: AGENTS.md 는 「outbox 상태」 · 「mapper 변환」 · 「설정 검사」를 **DB 없이** 도는 단위 테스트로 쓰라고 이름까지 들어 정했다. 지금 outbox 8개는 모두 `infra` 다. 전이 판단(`_fail_or_retry` 의 attempts/MAX · `confirm` 의 waiting/resend/superseded)이 SQL `UPDATE` 와 엉켜 있어 DB 없이는 시험할 수 없는 구조다. 그 밖에 DB 가 필요 없는 `test_오늘은_병원_현지_자정부터` · `test_주기는_10초_3600초` 도 모듈 단위 `pytestmark` 때문에 `infra` 로 묶였다(`-m "not infra"` 에서 빠짐).
- `test_outbox.py` · `test_emr_sync_service.py` 는 commit 하는 세션(`tests/day/emr/conftest.py`)을 쓴다. 「테스트 하나는 rollback 으로 끝낸다」와 다르다. 바깥 호출이 transaction 밖이라 commit 이 필요하다는 이유는 맞다. 다만 그렇다면 그 테스트는 「DB 가 보장하는 것」(조건부 UPDATE 경합 · advisory lock)만 남겨야 한다.
- 고칠 방향: `outbox` 에 순수 함수를 둔다. 예: `decide_after_send(row, ok|error) -> Transition`, `decide_on_poll(row, same_visit, received) -> Transition`. DB 없는 테스트 8개는 이 함수로 옮기고, infra 는 「조건부 UPDATE 경합 1개 · seq 동시 적재 1개(W4) · 막힘 UPDATE 1개」만 남긴다. `today_window` · 주기 테스트는 infra 아닌 파일로 옮긴다.

### W3. 잠금 TTL(300초)과 회차 실행 시간 사이에 상한이 없다 · worker 가 죽으면 일정 폴링이 최대 5분 멈춘다 — `services/emr_sync.py:88-107`, `common/config.py` `sync_lock_ttl_seconds=300`
- 근거: config 주석은 「한 회차가 이보다 길면 안 된다」고 하지만 회차 본문에 `asyncio.timeout` 이 없다. 기준 정보 1회차는 HTTP 10여 번이고, 호출마다 15초 · 401 이면 재시도한다. 최악이면 300초를 넘길 수 있다. 그러면 잠금이 풀린 채 다음 회차가 겹친다. upsert 가 멱등이라 행 수는 깨지지 않지만 `mark_absent` 가 서로 엇갈릴 수 있다. 반대로 worker 가 회차 도중 죽으면 그 병원의 일정 잠금이 300초 남는다. 10초 폴링이 최대 5분 건너뛰어진다.
- 고칠 방향: 일(job)마다 TTL 을 따로 둔다(일정 ≈ 60초, 기준 정보 ≈ 300초). 본문을 `asyncio.timeout(ttl - 여유)` 로 감싸 TTL 안에서 끝나게 한다(AGENTS 「timeout · 취소 · 동시성 상한을 명시」). 잠금 연장(watchdog)은 지금 필요 없다.

### W4. outbox `seq` — advisory lock 판정과 빠진 테스트 — `emr/outbox.py:101-123`
- 판정: 방법 자체는 맞다. `pg_advisory_xact_lock(hashtextextended('outbox:'||visit_id))` → `max(seq)+1` 은 READ COMMITTED 에서도 앞 보유자가 commit 한 뒤에 읽으므로 겹치지 않는다. 해시 충돌은 서로 다른 방문을 직렬화할 뿐이라 정확성에 문제가 없다. 다만 DB 가 지켜 주지는 않는다. `enqueue` 를 거치지 않는 INSERT 는 막지 못한다.
- 조용히 통과: `test_적재는_방문별_순서를_매긴다` 는 두 번을 **차례로** 넣는다. advisory lock 을 지워도 통과한다. 이 경로에서 DB 가 보장하는 것은 동시 적재뿐이니, 이것이야말로 infra 로 시험할 대상이다.
- 고칠 방향: (지금) 두 세션의 동시 `enqueue` → seq {1,2} infra 테스트 1개. (첫 실제 쓰기 Delivery) migration 으로 `live_unique("external_outbox", "visit_id", "seq")` 를 더한다. 그 전까지는 「코디가 확인할 것 4」 대로 미뤄도 된다.

### W5. 로그에 테넌트 id 끝 4자리가 남는다 — `emr/kos/client.py:197 · 231`
- 근거: 브리프는 「키 · 토큰 · **테넌트 id** 를 … 로그에 쓰지 마라」고 했다. 부분 값이라 위험은 낮지만 규칙과 어긋나고, 식별에는 이미 `hospital_id` 가 있다.
- 고칠 방향: `tenant=%s` → 부르는 쪽 `hospital_id`, 또는 아예 빼기.

### W6. mapper 가 확인되지 않은 다른 칸 이름으로 대체한다 — `emr/kos/mapper.py:284 · 309 · 339`
- 근거: `roleId or role.id` · `categoryId or funnelCategoryId` · `phone or phoneNumber`. 앞의 것(`roleId`/`role.id`)은 fixture(`kos_accounts.json`)에서 두 칸이 같은 값으로 오는 것이 보이므로 받아들일 만하다. `categoryId`/`funnelCategoryId` 는 리포트에도 「데모 응답에 없다」고 적혀 있다. 응답에서 본 적 없는 칸 이름을 미리 지어 둔 것이다. `phoneNumber` 객체도 fixture 에 없다. 값을 추정해 채우지는 않으니 A4 위반은 아니다. 다만 「응답 모양 확인 기준」에서는 벗어난다.
- 고칠 방향: 데모 응답에서 확인한 칸만 남긴다. 확인 안 된 대체 칸은 지우거나, 출처(HAR 등) 주석을 단다.

### W7. outbox 남은 구멍 — 첫 실제 쓰기 Delivery 전에 닫을 것 (지금은 `SUPPORTED_WRITES=∅` 라 실해 없음) — `emr/outbox.py`
- (a) **중복 발송**: `send_pending` 은 행을 읽고 세션을 닫은 뒤 보낸다(`:208-236`). 그 사이 일정 회차의 `confirm` 이 같은 행(재시도 대기 PENDING · attempts>0)을 CONFIRMED 로 옮기면 이미 반영된 쓰기를 한 번 더 보낸다. 그 뒤 `_move` 는 `conflict` 다. 보내고 commit 하기 전에 worker 가 죽어도 다시 보낸다. 일정 잠금과 쓰기 큐 잠금이 따로라서 생기는 일이다. → 쓰기마다 KOS 에서 멱등인지(같은 단계 재요청은 400 → 확인으로, cc 방식) 정하거나, 보내기 직전 조건부 UPDATE 로 `sending` 을 표시한다.
- (b) **SENT 영구 정체**: `confirm` 은 이번 조회(오늘 범위)에 있던 방문만 본다(`:291-299`). 쓰기 뒤 방문이 다른 날로 옮겨지면 그 행은 SENT 에서 영원히 안 움직인다. → 일정 시간이 지나도록 확인 안 된 SENT 는 `failed`(+ event_log)로 바꾼다.
- (c) `expect` 가 비면 `expect_met` 가 늘 False 라 3번 재전송한 뒤 failed 가 된다(`:256`). → `enqueue` 에서 빈 `expect` 를 거부한다.
- 실패 뒤 새로 들어온 쓰기는 평소대로 보낸다. 이것은 cc `ops.py:9-10` 과 같은 의도된 동작이라 지적하지 않는다.

### W8. `is_system_account` 는 sign-in 계정 하나만 — SPEC 은 「시스템 · 공용」 — `emr/kos/mapper.py:286-287`
- 근거: SPEC-000 `staff.is_system_account` = 「사람이 아닌 계정(시스템 · 공용) — 원장 목록 등에서 뺀다 (cc KOS_EXCLUDE_ACCOUNT_IDS)」. 구현은 `get-user-account` 의 id 와 같을 때만 true 다. KOS 응답에는 「공용」을 알려 주는 칸이 없으니, 다른 칸으로 추정하지 않은 것은 **맞다**. 대신 공용 계정은 사람으로 들어간다.
- 고칠 방향: 코드는 그대로 둔다. 공용 계정을 어디서 표시할지(DAY 관리 화면에서 사람이 고르는 칸 · 연결 설정의 제외 목록 등) 코디 · 사용자가 정한다. 정할 때까지 원장 목록 화면이 공용 계정을 보여 줄 수 있다(아래 「직원이 실물에서 만날 자리」).

## 조용히 통과하는 자리

| 자리 | 왜 초록인데 계약은 안 지켜지나 |
|---|---|
| `test_outbox.py::test_적재는_방문별_순서를_매긴다` | 차례대로 두 번 넣는다. advisory lock 을 지워도 통과한다(W4) |
| 기준 정보 「매핑 실패 = 사라짐」 | 기준 정보에서 뺀 행이 사라짐으로 가는지 보는 테스트가 없다. `test_기준_정보는_cc_와_같은_API_토큰으로_받는다` 는 `skipped == {"reservation_group": 1}` 까지만 보고, 그 행이 DB 에서 어떻게 되는지는 보지 않는다(W1) |
| 병원 경계 | 코드는 전부 `hospital_id` 로 범위를 거는 것을 확인했다(`Refs._scope` · `in_window` · 자식은 이 병원 부모 id 로만). 그런데 「병원 A 반영이 병원 B 행을 건드리지 않는다」 테스트가 없다. 두 병원에 같은 외부 id(`zone-a`)를 넣고 A 에서 사라짐 처리 → B 는 그대로인지 보는 infra 1개를 권한다 |
| `today_window` · 주기 테스트 | DB 가 필요 없는데 `infra` 라 `-m "not infra"` 에서 빠진다(W2) |
| 잠금 TTL 만료 | `test_잠금은_하나만_잡고_가진_쪽만_푼다` 는 해제만 본다. TTL 이 지나 남이 잡은 잠금을 내가 나올 때 안 지우는지는 Lua 로 보장되지만 테스트가 없다(낮음) |

동기화 정확성 — 확인되어 지적 없음:
- `external_ref` upsert 는 `index_where=deleted_at IS NULL` 을 매번 준다(`sync.py:162-172`). 나머지 upsert 대상(`reservation_group_capacity` · `_timetable` · `customer_category_link` · `visit_occupied_resource_doctor`)은 복합 PK 라 `index_where` 가 필요 없다(`models/customer.py:149-150` 등). `customer.chart_number` 의 live_unique 충돌은 savepoint 로 그 고객만 뺀다(`sync.py:671-693`).
- 같은 회차를 두 번 돌려도 행은 그대로다. 단계 이력은 단계가 바뀔 때만 쌓인다(`sync.py:850`).
- transaction 안에서 KOS 를 기다리지 않는다. `run_master` · `run_schedules` 는 받기를 세션 밖에서 하고(`emr_sync.py:115 · 137`), 쓰기 큐 `send` 도 세션 밖에서 한다(`outbox.py:236`). `has_master_data` 세션도 받기 전에 닫힌다.
- 남의 잠금을 풀지 않고(토큰 Lua), 해제가 실패해도 원래 예외를 가리지 않는다. worker 가 죽으면 TTL 뒤 풀린다(W3).

## 「코디가 확인할 것」 1 ~ 6 판정

| # | 구현 리포트 항목 | 판정 | 근거 · 권고 |
|---|---|---|---|
| 1 | 데모 지점 오늘 일정 0건 — 시계를 4일 앞으로 옮겨 실물 건수를 얻음, 10건이 로컬 `day_dev` 에 남음 | **받아들임** | 같은 서비스 경로(`run_schedules`)이고 조회만 했다. 스크래치 스크립트는 커밋되지 않았다(미추적 목록에 없음). 남은 10건은 로컬 볼륨이라 저장소 · 공유 DB 와 무관하다. 다음 실물 확인은 데모에 오늘 일정이 있는 날 10초 경로 그대로 1회를 권한다 |
| 2 | 다른 날로 옮긴 예약 = 오늘 범위에서 사라짐 → 그날 되살림 · 고객은 사라짐 없음 | **받아들임** | A3 를 「조회 범위 안에서 사라짐」으로 읽는 것이 맞다(`sync.py:884-895` · 범위는 DAY 에 저장된 `reserved_start_at`). 고객은 일정 안에서만 보이므로 사라짐을 판단할 근거가 없다 — 추정하지 않은 것이 맞다. 다만 W7(b)(옮긴 방문의 SENT 정체)와 같이 기억할 것 |
| 3 | 차트번호 충돌 → 그 고객 · 그 방문만 savepoint 로 빼기 | **받아들임** | `sync.py:671-693` · 뺀 방문은 `held_back` 으로 사라짐 처리에서도 빠진다(`:873-883`). 로그는 예외 클래스 이름만 남겨 차트번호가 새지 않는다. 실물에서는 그 환자가 현황판에서 안 보이고 `skipped.customer` 에만 남는다. 로그 경보 기준은 화면 Delivery 에서 정한다 |
| 4 | `external_outbox (visit_id, seq)` 유일 제약 없음 — advisory lock | **조건부 받아들임** | 방법은 맞다(W4). 지금은 적재하는 업무 코드가 0이다. ① 동시 적재 infra 테스트를 지금 더하고 ② 첫 실제 쓰기 Delivery 에서 `live_unique` migration 을 단다(백엔드 안전 기준: 사전 조회만으로 불변식을 지키지 않는다) |
| 5 | 직원을 내부 `account/v2` 로 받음(cc 는 공개) | **받아들임 · 위험 기록** | SPEC-000 04 `staff.real_name` · `license_number` · `job_role_id` 의 출처가 내부 응답에만 있고, 공개 응답에는 없다(리포트 「공개 API 후보」 표). 공개로 받으면 SPEC 칸을 못 채우니 내부가 맞다. 대가: 내부 API(브라우저 헤더 우회)에 대한 의존이 하나 늘어, KOS 가 더 막으면 직원 동기화가 멈춘다. 다만 `fetch_master` 가 전부 받거나 전부 실패하는 구조라, 멈춰도 기존 직원이 「사라짐」 처리되지는 않는다. Issue 「검토할 부분」의 공식 API 이전 목록에 올려 둘 것 |
| 6 | 일정 · 기준 정보 잠금이 따로라 동시에 돌 수 있음 | **받아들임(주의)** | 두 일이 쓰는 테이블은 겹치지 않는다(일정은 기준 정보를 `lookup` 만 한다). 토큰은 `asyncio.Lock` 으로 한 번만 받는다(`client.py:133`). 같은 방식이 일정 ↔ 쓰기 큐 사이에서는 W7(a) 중복 발송의 원인이 된다 — 첫 실제 쓰기 Delivery 에서 다룰 것 |

## 「추정 금지」 대조 — 리포트 「비워 둔 칸」 표 ↔ 코드

| 칸 | 코드 | 판정 |
|---|---|---|
| `staff.default_zone_id` | upsert 칸 목록에 없다(`sync.py:482-492`) | 같음 |
| `staff.real_name` · `license_number` | `text(realName)` · `text(licenseNumber)`, 없으면 None. `name` 으로 채우지 않는다 | 같음 |
| `staff.account_id` | upsert 칸에 없다(로그인이 채운다) | 같음 |
| `customer` 상세 칸들 | `CUSTOMER_COLUMNS`(`sync.py:578-591`)에 없다 → 넣지도 덮지도 않는다 | 같음 |
| `gender` | `GENDERS.get` — UNSPECIFIED → None | 같음 |
| `connected_channel` | `Channel_UNSPEICIFED` 는 표에 없어 None | 같음 |
| 참조 id 를 모를 때 | `ref()` → None(선택 칸) · 필수 칸은 그 행을 뺀다 | 같음 |
| `product_option_id` | 정규형에 칸이 없다 | 같음 |
| `funnel.category_id` | 응답이 줄 때만 — 다만 확인 안 된 칸 이름(W6) | 대체로 같음 |
| 시간표 시각 | `HOSPITAL_TIMEZONE`(전역 1개) 시계 시간 | 같음 — 병원마다 시간대가 다르면 연결 설정으로 옮길 일(참고) |
| `visit_flow_log.changed_at` | `flow_step_at or now` | 받아들임 — 필수 칸이고 리포트에 밝혔다 |
| 필수 bool | `activate` · `isDefault` · `enabled` · `consultationRequired` · `sedationRequired` 가 없으면 그 항목을 뺀다(기본값 없음) | 같음 — 대신 뺀 기준 정보 행은 W1 로 사라짐이 된다 |
| `birth_date` | 자정이 아니면 None | 같음 — KOS 가 KST 자정을 UTC 15:00 으로 주는 고객이 있으면 전부 None 이 된다. 실물 8명 중 몇 명이 채워졌는지 다음 실물 확인 때 세어 볼 것(참고) |
| `ROLE_TAGS` 정수 ↔ 이름 | 데모 80/80 대조로 확인했다는 리포트 근거 | 받아들임 |

## 직원이 실물에서 만날 자리

- **KOS 가 응답 모양을 조금 바꾸면 방 · 직원 · 예약 그룹이 현황판에서 통째로 사라질 수 있다**(W1). 다음 정상 응답이 오면 되살아나지만 최대 1시간(기준 정보 주기)이 걸린다.
- **worker 가 재시작되면 그 병원 현황판이 최대 5분 멈춰 보일 수 있다** — 일정 잠금 TTL 300초(W3).
- 공용 계정이 원장 · 직원 목록에 사람처럼 나온다(W8 — 정책 결정 대기).
- 차트번호가 충돌한 환자는 그날 현황판에 안 보인다(확인할 것 3). 로그 · 건수(`skipped.customer`)에만 남는다.
- KOS 가 내부 API 를 더 막으면(브라우저 헤더 우회 실패) 일정 · 방 · 직원 동기화가 함께 멈춘다. 구역만 공개 API 라 계속 들어온다. 오류는 `emr … failed: HTTP 403 …` 로그로만 보인다.

## 참고 (기존 부채 · 이번 범위 밖)

- `deploy/local.env.example` 에 KOS 공개 호스트 3개가 실제 값으로 들어 있다. 코드에는 기본값이 없고(`KosEndpoints` 기본 `""` + `require()`), 비밀값도 아니며, 가짜 도메인도 아니다. AGENTS 「부재값은 env 로」와 맞다.
- worker 가 오래 내려가 있으면 scheduler 가 10초마다 넣은 디스패치 메시지가 Redis 큐에 쌓인다. 재시작 때 한꺼번에 처리되지만 잠금 · 멱등 덕분에 해는 없다. 메시지 만료(taskiq 라벨)는 운영 Delivery 에서 정할 일이다.
- `_run` 은 `EmrError · ValueError · OSError` 만 잡는다. SQLAlchemy 오류는 taskiq traceback 으로 나간다. PostgreSQL `DETAIL` 에 키 값이 실릴 수 있으니(차트번호 유일 위반은 이미 잡아 이름만 남김), 다른 제약 위반에도 같은 처리가 필요한지 운영 로그 기준과 같이 볼 것.
- 계층 규칙: router 변경 0. `services/` 가 세션을 직접 쓴다(repository 없음). `day.public` 은 `seed_demo_kos_connection` 이 UUID 만 돌려준다. 업체 패키지는 `emr/factory.py` 만 import 한다(`test_emr_vendor_boundary`). 지적 없음.
- 출처 표기: cc-prototype 본을 docstring 에 적었다(`client.py:3` · `outbox.py:3` · `kos/__init__.py:16` · `mapper.py:416-417`). `stg` 에서 통째로 복사한 곳은 없다.
