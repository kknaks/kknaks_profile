# 리뷰 리포트 — day-cc-mig #264 테이블 보충 / code (2026-11-20)

## 판정: WARN — FAIL 0 · WARN 8

- 대상: 워크트리 `CENTURION_DAY/day-cc-mig` 미커밋 변경(고친 파일 36 · 새 파일 16) · base `origin/dev` `844eace4`(HEAD 와 같음)
- 기준: DAY-SPEC-000 §4A · §6 OQ-4A-1 ~ 15(mediness #954) · Delivery #264 D-1 ~ D-5 · A1 ~ A7 · `_RESUME.md` §2(2026-11-20) · `be-fix-1-instructions.md` · 레포 `AGENTS.md` · data_rules

| 2절 항목 | 결과 | 요약 |
|---|---|---|
| 1. prod 무중단 · 더하기만 | **PASS** | 0012 upgrade 는 create_table 12 · add_column(전부 `nullable=True` · 기본값 없음) · create_index(부분 유일 5) · FK 만 있다. drop · alter_column · `op.execute` · 데이터 이동 0. enum 9개는 `CREATE TYPE`(값 포함)이고 `ALTER TYPE … ADD VALUE` 0 → 트랜잭션 안 사용 문제 없음. downgrade 는 새 칸 · 새 표 · 새 타입만 역순으로 지운다(`weekday` · `option_type` 는 `create_type=False` · NEW_TYPES 밖). `down_revision = 0011_visit_reserved_index`. `MIGRATION_LOCK_TIMEOUT_MS` 기본 5초(`common/config.py:102`)라 운영 잠금을 오래 기다리지 않는다 |
| 2. SPEC 대조 | **PASS** | 새 표 12 · 지금 표 23(prod 9 · dev 14)의 칸을 §4A 표와 한 칸씩 맞췄다. 빠진 칸 0 · 지어낸 칸 0(아래 「대조」). enum 값 · 매핑은 §4A + 고침 1 과 같다 |
| 3. 기존 회차 격리 | **PASS(WARN 3)** | 묶음 만들기(`safe_kos_keys`) · 반영(`apply_isolated` · 다른 tx · 30초 · 자기 잠금 · 모든 예외 로그) · 새 단계(`_isolated("kos_keys")`) 모두 지금 회차의 commit · 신호 · 발행 **뒤**. 반환 · status · 「동기화 멈춤」 스냅샷 · 10초/1시간 회차의 KOS 호출 수 그대로. `Refs.link` coalesce 는 의도대로 동작 — 다만 다른 호출자에도 뜻이 퍼진다(W5). 지연 · 쿼리 수 · 겹침은 W1 |
| 4. 목록 밖 값 규칙 | **PASS(WARN 1)** | `Extra.enum` → 칸 None + `「칸=KOS 원래 값」` 경고 · 행 유지. CARD → `card`. `payment_type`(NOT NULL) 의 모르는 수단 = 그 거래 제외 — SPEC OQ-4A-1 「그 전엔 표 밖 값 처리(그 행을 뺀다)가 그대로」 · §4A 공통 「이 절의 새 enum 칸에 적용」과 같다. 경고 반복은 W2 |
| 5. data_rules | **PASS(WARN 1)** | KOS id 칸 0(참조는 전부 `external_ref` → DAY FK) · 동기화 칸은 `external_ref` 에만(`treatment_item_revised_at` · `payment_updated_at` 는 SPEC 이 정한 스냅샷 값) · 시각 `timestamptz`(운영 시간만 현지 `time` — S0 06 예외) · 여권 · 주민 · 외국인등록은 기존 `EncryptedText` 칸 · 새 표 전부 `deleted_at` · 물리 DELETE 0 · jsonb 는 SPEC 이 「통째」로 정한 칸뿐. `created_at` 덮기는 W8 |
| 6. 업데이트 경로 | **PASS(WARN 1)** | `--dry-run`: `_apply` · `settings()` 가 쓰기 전에 돌아가고 `save_progress` 도 dry-run 이면 Redis 를 안 쓴다. KOS 1초 1회는 `PacedTransport`(모든 요청 · sign-in 포함) — 새 경로(`outside_tenant` 포함)도 같은 `_http` 를 지난다. 자기 세션만 해제(`release_own_sessions(started-30s)` · 표시 `backfill`). 멱등(바뀐 칸만) · resume(부분 · 달 · 장 · 순번). 진행 키 공유 · 동시 실행은 W7 |
| 7. 조용히 통과하는 자리 | **WARN 2** | W3(살아 있는 회차의 실패 · 「못 찾음」이 로그 밖으로 안 나옴 · 태스크 배선 테스트 0) · W4(`visit.reservation_status_at` 채우는 경로 0) |
| 8. 직접 실행 | **PASS** | 아래 수치 |

### 직접 실행(각 1회 · `./scripts/test.sh` 격리 인프라 · 사용자 포트 · 프로세스 안 건드림)

| 명령 | 결과 |
|---|---|
| `./scripts/test.sh -q` — `test_kos_keys_{mapper,sync,isolation,backfill}` · `tests/migrations/`(0012 왕복 · `alembic check`) · `test_enum_labels` · `test_column_snapshot` · `test_constraints` · `test_models` · `test_kos_sale_mapper` · `test_sale_sync_rules` · `test_sync` · `test_sale_sync` · `test_backfill` · `test_emr_sync_service` · `test_kos_board_contract` | **355 passed**(39s) |
| `./scripts/test.sh --pure -q backend/tests/architecture` | **309 passed** |
| `ruff check` · `ruff format --check`(바꾼 · 새 .py 52개) | 통과 · 52 files already formatted |
| `mypy`(레포 설정 · 루트) | **Success: no issues found in 439 source files** |

## FAIL

없음.

## WARN

**W1 — 10초 회차에 행마다 쿼리(N+1) · 회차 시간 연장 · 같은 행 동시 쓰기 가능성(query-count 테스트 0)** — 레포 `AGENTS.md` 「백엔드 안전 기준」(N+1 위험 경로는 query-count 테스트로 막는다)
- `backend/day/emr/sync_kos_keys.py:316-318` 배열 표마다 **부모 행마다 SELECT**(방문마다 희망 시술 · 기타 업무, 희망 시술마다 구성, 기타 업무마다 담당) · `:459-466` 약품 · 기기 참조 **소유 행마다 SELECT**(작업 · 희망 시술 · 구성마다) · `:281-299` 외부 수정 시각 **행마다 UPDATE 문**(값이 같아도 문은 나간다). DEMO 하루(방문 12 · 작업 42)로 회차당 대략 100문 · 운영 병원 하루 방문 100 · 작업 300 이면 10초마다 수백 문이 늘어난다(쓰기는 0 이어도).
- `backend/day/services/emr_kos_keys.py:36` `APPLY_TIMEOUT_SECONDS = 30.0` > 10초 주기 · `backend/day/tasks/emr.py:108` 같은 태스크가 반영을 기다린다. 반영이 10초를 넘기면 다음 일정 회차(`schedules` 잠금)와 이 반영(`kos_keys_apply:schedules` 잠금 — 서로 다른 잠금)이 **같은 visit · visit_task 행을 동시에** 쓴다 → 행 잠금 대기 · 순서가 다르면 deadlock. `_run` 은 `EmrError · ValueError · OSError` 만 잡아(`emr_sync.py:171`) DB 오류는 일정 태스크까지 올라간다(지금도 같은 길이지만 동시 쓰는 쪽이 새로 생겼다).
- 고칠 방향(제안): 부모 id 묶음으로 한 번에 SELECT(`parent_col.in_(…)` · `owner_id.in_(…)`) · `external_updated` 를 한 문으로 · 반영 상한을 주기보다 짧게 또는 `schedules` 잠금 안/같은 잠금 이름으로 · query-count 테스트 1개.

**W2 — 목록 밖 값 경고가 매 회차 반복(로그 폭주)** — 2절 7 · A4 「경고 1줄」
- `sync_kos_keys.py:213`(`self._warned` 가 `Applier` 하나 = 회차 하나에만 산다) · `:245-252`. 같은 값이 오늘 일정에 있으면 **10초마다 한 줄** — 값 하나 · 병원 하나에 하루 8,640줄. 고침 1 로 지금 관찰 값은 다 매핑돼 0줄이지만, KOS 새 값(예: 다른 긴급도) 하나가 오면 바로 난다. `safe_kos_keys` 실패(`mapper_kos_keys.py:501`) · `apply_isolated` 실패(`emr_kos_keys.py:64-68`)도 회차마다 같은 줄.
- 제안: 프로세스 단위(또는 Redis `set_once` · TTL 하루) 한 번 · 이후는 셈만.

**W3 — 살아 있는 회차에서 「못 찾음 · 못 함」이 보이지 않는다 · 태스크 배선 테스트 0** — 2절 7
- `emr_kos_keys.py:69-70` 결과 로그는 `total_written or warnings` 일 때만 — `missing`(DAY 에 행 없음) · `unresolved`(참조 못 찾음)만 있는 회차는 **아무 줄도 남지 않는다**. entity_type 철자 · 매핑 실수로 모든 행이 `missing` 이 돼도 운영에선 조용하다(DEMO 숫자가 지금은 맞다는 것만 보장).
- `emr_kos_keys.py:57-58` 잠금을 못 얻으면 로그 없이 None.
- 실패는 전부 WARNING 로그(오류 이름)뿐 — 회차 스냅샷 · 화면 · 셈에 남지 않아 「계속 실패 중」을 알 길이 로그 검색밖에 없다(의도된 격리지만 감시 수단이 없음).
- 테스트: `test_kos_keys_isolation.py` 는 `apply_isolated` 함수 · 매핑만 본다. `tasks/emr.py` 의 `_kos_keys` 배선(일정 · 기준 정보 · 구매 태스크가 반영 실패 · 지연에도 같은 status 를 돌려주는지 · `run_hospital` 이 던져도 `sync_master_hospital` 이 master status 를 돌려주는지)을 확인하는 테스트가 없다(`test_emr_rules.py:175-205` 는 `run_schedules` 만 바꿔 끼우고 `kos_keys` 는 빈 묶음이라 반영을 안 탄다). 코드 읽기로는 맞다 — 고정하는 테스트가 없다.

**W4 — `visit.reservation_status_at` 를 채우는 경로가 없다(늘 null · 리포트에 안 적힘)** — SPEC §4A.3 「P07 에 없는 `statusUpdatedDateTimeUtc` 는 P08 · P33 에서만 온다」 · D-2
- 매퍼는 `mapper_kos_keys.py:283` 에 있지만 `kos_keys` 를 만드는 곳은 `fetch_schedules`(P07) · `fetch_master` · 메뉴 · 구매 · 시술권 · 카드 · 고객 목록뿐. P08 을 읽는 `fetch_visit_tasks`(`emr/kos/__init__.py` · 이벤트 연쇄)는 묶음을 만들지 않고, 업데이트 경로도 P07 이다. `test_kos_keys_mapper.py:144-153` 주석 「상세가 채운 값을 지우지 않게」의 「상세」가 코드에 없다.
- D-2 가 회차를 「일정 10초 · 기준 정보 · 판매 · 메뉴」로 적어 계약 위반은 아니지만, 칸이 영원히 비는 것을 리포트가 밝히지 않았다. P08 묶음을 붙이거나(이벤트 때만 · 호출 수 그대로) 2단계(미래 일정 요청 때 P33)로 넘긴다고 적어야 한다.

**W5 — `Refs.link` coalesce 는 직원 · 상담 · 고객뿐 아니라 모든 호출자의 뜻을 바꾼다** — 2절 3 · 고침 1 항목 2
- `backend/day/emr/sync_references.py:274-276`. 전에는 「None = 비움」, 지금은 「None = 지금 값 유지」. 값을 넘기는 호출자 — 구매(`sync_purchases.py:119,124`) · 카드(`sync_tickets.py:180,206`) · 메뉴(`sync_menu.py:122,213`) · 방문(`sync_schedules.py:271`) — 는 저장된 값으로 「바뀜」을 판단한다. KOS 가 수정 시각을 한 번이라도 빈 값으로 주면 ① 저장 값이 남아 `known[1] != None` → **매 회차 「바뀐 고객」** → 고객마다 시술권 · 카드 KOS 호출이 회차마다 더 나가고 ② 그 뒤 같은 시각이 다시 오면 바뀜을 놓친다. 실제로 빈 수정 시각이 오는지는 관찰 없음(가능성 낮음) · 이 경우의 테스트 없음. 코디가 허용한 한 줄이라 FAIL 은 아니고, PR 본문에 「None = 유지」로 계약이 바뀐 것을 적을 것.

**W6 — 예약 규칙 이력(쌓기만)의 중복 판정 열쇠가 바뀔 수 있는 값을 포함** — §4A.1 `reservation_rule_event` 「쌓기만」 · OQ-4A-9
- `sync_kos_keys.py:136-142` 열쇠 = `(occurred_at, event_type, staff_id, payload)`. `event_type` 은 enum 매핑 결과 · `staff_id` 는 참조 해석 결과다. OQ-4A-9 방식대로 **enum 값을 나중에 더하면**(그 전엔 null 로 들어간 행) 다음 회차에 같은 이력이 값 있는 행으로 **한 번 더** 쌓이고, 쌓기만이라 null 행은 지워지지 않는다. 직원이 나중에 잡혀도 같다. 표에 유일 제약이 없어 아래 W7 의 동시 실행에서도 중복이 난다.
- 제안: 열쇠를 KOS 원래 값(이력 종류 문자열 · 직원 KOS id)으로 두거나, 매핑 전 값이 같으면 갱신 허용.

**W7 — 업데이트 경로: 진행 키 공유 · 운영 새 단계와 잠금 공유 없음**
- `backend/day/services/emr_backfill.py:229-238` 진행 위치는 병원마다 키 하나(JSON 통째). `--resume` 없이 `--stage kos_keys` 를 실제로 돌리면 `self.progress` 가 빈 dict 에서 시작해 **지난 백필의 이어 받기 위치를 덮어 지운다**(반대도 같다). 다시 돌려도 멱등이라 데이터 손상은 없고 시간만 든다 — dev 서버 순서 안내에 적을 것.
- `emr_kos_keys_backfill.py:97-120` ① 병원 설정 부분은 운영 1시간 새 단계(`run_hospital` · 잠금 `kos_keys`)와 같은 잠금을 쓰지 않는다 → 둘이 겹치면 규칙 · 휴무 연결은 `external_ref` 유일로 한쪽이 IntegrityError(백필 종료 2 · 운영은 로그), 규칙 이력은 중복 가능(W6). ② 고객 부분도 1시간 고객 장과 같은 고객을 동시에 쓴다(행 잠금 대기만).
- 드라이런의 「받은 행」(5,064)은 「쓸 행」(6,126)의 예고가 아니다 — 리포트 수치 해석에 주의(정상 · 설명만 필요).

**W8 — 열린 결정(OQ-4A-11)을 코드가 「덮는다」로 정함 · 지금 prod 행이 바뀐다** — §4A 공통 「생성 시각」 · §6 OQ-4A-11 · be-1 리포트 §7-2
- `mapper_kos_keys.py:361`(상담) · `:418-419`(직원) · `:458-462`(고객 `created_at` · `registered_at`) · 구매 · 거래 · 티켓 · 카드 · 규칙 — 배포 뒤 첫 1시간 회차 · 업데이트가 **이미 있는 prod 행의 `created_at` 을 KOS 생성 시각으로 덮는다**. SPEC 은 「지난 prod 행을 언제 고칠지는 OQ-4A-11」로 열어 뒀다. 브리프 D-2 문구대로이고 리포트가 확인을 요청했으므로 FAIL 은 아니나, **prod 배포 전에 사용자 결정**이 필요하다.
- 같은 결: `mapper_kos_keys.py:463-464` KOS `deleted:true` 고객 → `customer.deleted_at`(SPEC 「동기화로 채움」대로). 지금 화면 · 조회 중 `Customer.deleted_at` 으로 거르는 곳은 0(`grep` 0)이라 판에서 사라지는 일은 없다. 되살린 고객(`deleted:false`)의 `deleted_at` 은 비우지 않는다.

## 대조 — §4A 칸 ↔ 모델 · 0012(직접 한 칸씩)

| 표 | SPEC | 코드 | 비고 |
|---|---|---|---|
| hospital | 19 | 19 | `languages[]` 보류(OQ-4A-4) |
| crm_connection | 1 | 1 | `tenant_info` jsonb |
| reservation_group | 3 | 3 | |
| customer | 새 8 · 채움 23키 | 8 · 매퍼 23키(+ `created_at` · `deleted_at`) | 지금 고객 upsert 칸(`sync_tables.py:288-305`)과 겹치는 칸 0 |
| visit | 6 | 6 | `reservation_status_at` 경로는 W4 |
| visit_requested_procedure | 2 + TI 17 | 19 | |
| staff | 2(+ 채움 4) | 2 | 지금 직원 upsert 는 `email` 만 겹칠 수 있는데 보충은 `email` 을 안 씀 |
| job_role | 1 | 1 | `feature_list` 의 `featureId` 는 SPEC 이 「통째」로 정함 |
| visit_task | 15 | 15 | |
| product_option · composition · price · etc_task_type · prepaid_card_product · etcetera_product | 3 · 5 · 8 · 1 · 3 · 2 | 같음 | `product` 는 칸 없이 `medicine_machine_ref` 행만 — Delivery 「dev 15표」는 product 를 센 수 |
| purchase · purchase_item · purchase_transaction | 1 · 40 · 10 | 같음 | |
| ticket_bundle · ticket_set · ticket | 5 · 17 · 2 | 같음 | `ticket_set.treatment_item_id` 는 지금 칸 그대로(mixin 밖) |
| prepaid_card · ledger | 8 · 1 | 같음 | |
| 새 표 12 | 10 · 7 · 7 · 13 · 9 · 9 · 9 · 23 · 10 · 5 · 35 · 12 | 같음 | 필수 칸 NOT NULL(`owner_type` · `owner_id` · `kind` · `name` · `sort_order` · `is_enabled` · 부모 FK) · 부분 유일 5 |

enum: `task_urgency_level{unspecified, urgent}` · `etc_work_status{waiting, completed, canceled}` · `price_reason{general}` · `reservation_occupancy_policy{all_matched_sequential}` · `reservation_zone_occupancy_policy{single_zone_only}` · `requested_procedure_repetition{once_per_reservation}` · `reservation_rule_event_type{created, activated, deactivated, rule_set_changed, default_rule_set}`(KOS `protos.schedule.*Event` 문자열은 `mapper_kos_keys.py:62-69` 매핑에만) · `medicine_machine_owner_type`(SPEC 9값) · `medicine_machine_kind{medicine, machine}` — 고침 1 지시와 같다. TI 묶음의 상태 · 단위 · 급여 · 과세는 원본 `treatment_item` 과 같은 열린 문자열(`models/menu.py:205-210` 관례).

## 직원이 실물에서 만날 자리

- 화면 변경 0 — 이 작업의 칸 · 표를 읽는 화면이 없다(A6).
- 간접: 배포 직후 1시간 회차부터 기준 정보 태스크의 KOS 호출이 병원마다 시간당 약 「10 + 예약 그룹 수 + 규칙 수 + 고객 1 ~ 5장」 늘고, 일정 태스크 한 번이 칸 보충(최대 30초)까지 기다린다(W1). 판 갱신 신호는 반영 전에 나가므로 화면 지연은 없다.
- 고객 `created_at` · `registered_at` 이 KOS 값으로 바뀐다(W8) — 이 칸으로 정렬 · 표시하는 화면이 생기면 순서가 달라 보인다.

## 참고(기존 부채 · 이번 범위 밖)

- 백필 시술권 이어 받기는 정렬된 고객 목록의 순번으로 이어 간다(`emr_backfill.py:351-370` · 새 `kos_keys_tickets` 도 같은 방식) — 그 사이 운영 회차가 구매 고객을 더하면 순번이 밀려 한 고객을 건너뛸 수 있다. 지난 백필과 같은 패턴.
- 같은 병원에 백필 두 개를 동시에 돌리면 `release_own_sessions` 가 서로의 `backfill` 로그인을 해제한다(지난 백필과 같음 — 하나씩만 돌릴 것).
- OQ-4A-9 다음 값 추가 때는 `ALTER TYPE … ADD VALUE` 가 필요하다 — 같은 transaction 안에서 그 값을 쓰지 않게 마이그레이션을 나눌 것(이번 0012 는 `CREATE TYPE` 이라 해당 없음).
- 0012 는 한 transaction 에서 지금 표 23개에 칸 · FK 를 더해 그 표들의 강한 잠금을 commit 까지 잡는다. lock_timeout 5초라 막히면 실패하고 다시 돌리면 되는 구조 — 배포 시각을 한가한 때로.

## 재검수 2 (2026-11-20 · 고침 2 W1 ~ W7)

### 판정: PASS — FAIL 0 · 새 WARN 0 · W1 ~ W7 닫힘 · W8 은 사용자 결정 대기(지시대로 안 봄)

| | 결과 | 근거(같은 워크트리 미커밋 diff) |
|---|---|---|
| W1 N+1 · 겹침 | **닫힘** | `sync_kos_keys.py` `_live`(부모 id 묶음 `parent_col.in_(…)` · CHUNK) · `children()` 가 표마다 한 번 읽고 부모마다 맞춤 · 기타 업무 연결 한 문. query-count 테스트 `test_보충_반영_문_수는_방문_수와_무관하다`(실제 PG · 방문 1 vs 7 재회차 SQL 문 수 같음). 잠금: `emr_kos_keys.apply_isolated` 가 그 회차와 **같은 잠금**(`lock_key(job)` · `APPLY_JOBS`) 안에서 반영 · 일정 상한 8초(< 10초 주기) · 나머지는 `run_budget` — 같은 visit · visit_task 행을 두 쪽이 동시에 쓰는 길이 구조적으로 없다 |
| W2 경고 반복 | **닫힘** | `warn_once`(`sync_kos_keys.py:207-213` · 프로세스 단위 · 상한 1만) — 목록 밖 값 · 반영 실패 · 묶음 실패 모두. 테스트 `test_목록_밖_값_경고는_병원_줄마다_한_번`(두 회차 · 줄 1 · 셈 1+1) |
| W3 조용한 자리 · 배선 | **닫힘** | `_log_result` 가 `missing` · `unresolved` 포함 · 셈이 바뀔 때만 한 줄 · 잠금 못 얻음 = 셈 + 처음/360번마다 한 줄. `tasks/emr.py` `_kos_keys` 도 예외를 잡는다. 배선 테스트 `test_보충이_실패하거나_늦어도_태스크_status_는_그대로`(일정 · 기준 정보 · 구매 status `done` · `run_hospital` 이 던져도 master status 그대로) |
| W4 `reservation_status_at` | **닫힘** | 매퍼 줄 제거 + 이유 주석(2단계 P08 · P33) · 키가 와도 안 싣는 테스트. 칸은 0012 에 그대로(SPEC 대로) — PR 본문에 「늘 null · 2단계」 적을 것 |
| W5 `Refs.link` 뜻 | **닫힘** | `sync_references.py` 기본은 원래 뜻(`excluded` 그대로 = None 이면 비움) · `keep_updated_at=True` 는 직원(`sync_master.py`) · 상담(`sync_tasks.py`) · 고객(`sync_schedules.py`) 세 곳뿐 — 구매 · 카드 · 메뉴 · 방문의 「바뀜」 판정은 고침 1 전과 같다. 테스트 `test_연결은_수정_시각을_주지_않으면_기본은_비우고_보충_호출만_유지한다` |
| W6 이력 열쇠 | **닫힘** | 열쇠 = `(occurred_at, payload)` + 느슨한 칸 `(event_type, staff_id)` — 같거나 **빈** 행에 맞추고 빈 칸만 채움(`_pick` · `updates` 는 None 아닌 값만). enum 값 추가 · 직원 해석 뒤 중복 0 — 테스트 `test_규칙_이력은_종류가_나중에_잡혀도_두_번_쌓이지_않는다`. SPEC 밖 칸 추가 0 |
| W7 진행 키 · 잠금 | **닫힘** | `progress_key(…, stages)` — `kos_keys` 단독이면 `day:emr:backfill:kos_keys:<병원>` 로 분리. 병원 설정 · 고객 부분은 운영 새 단계와 같은 잠금 `lock_key("kos_keys")`(TTL 1시간 · 10초 × 60번 기다린 뒤 종료 2 → `--resume`). 운영 쪽은 `skipped_locked` |
| 새로 깬 것 | **없음** | 0012 upgrade 에 drop · alter_column · `op.execute` · ADD VALUE 0(변경 없음) · 기존 회차 반환 · status 그대로 · 테스트 아래 |

직접 실행(각 1회 · `./scripts/test.sh` 격리 인프라)

| 명령 | 결과 |
|---|---|
| `./scripts/test.sh -q backend/tests/day/emr backend/tests/migrations` + `test_enum_labels` · `test_column_snapshot` · `test_constraints` · `test_models` | **492 passed** |
| `./scripts/test.sh --pure -q backend/tests/architecture` | **309 passed** |
| `ruff check` · `ruff format --check`(바꾼 · 새 .py 55개) | 통과 · 55 files already formatted |
| `mypy`(레포 설정) | **no issues found in 439 source files** |

참고(판정에 안 넣음 · PR 본문 · 운영 안내 몫)
- 같은 잠금 방식의 대가: 일정 회차 + 보충이 10초를 넘으면 **다음 일정 회차 하나가 `skipped_locked`** 로 건너뛴다(보충 상한 8초라 최대 한 주기 늦음 · DEMO 회차 4 ~ 6초). 판이 한 주기 늦게 갱신될 수 있다는 뜻 — 의도된 교환.
- `--stage kos_keys --dry-run` 도 고객 부분 동안 `kos_keys` 잠금을 잡아 그 시간 운영 1시간 병원 단계를 건너뛰게 한다(데이터 영향 없음 · dev 실행 안내에 한 줄).
- W6 느슨한 맞춤의 남은 틈: 저장된 이력에 직원이 있는데 새 응답에서 그 직원을 못 찾으면(None) 같은 이력이 새 행으로 하나 더 쌓인다(직원이 DAY 에서 사라지는 경우뿐 · 관찰 없음).
- W8(`created_at` 덮기 · OQ-4A-11)은 그대로 — prod 배포 전 사용자 결정.
