# research-2 — E3 · E4 방 카드 오더 메모 위 「담당 상담사」 원천 조사 (read-only)

- 코드: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-web` 작업 트리(dev `c5045a99` + fix-web 미커밋 변경 — 읽기만). 줄 번호는 **작업 트리 기준**(fix-web 워커 변경 포함).
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-web-spec/products/day/20-spec/`(HEAD `de59fe3f` + 미커밋 변경 — spec-002 · spec-003 은 수정 중). 줄 번호 = 작업 트리 기준.
- HAR: `~/Downloads/상담사 조회 .har`(88 entries). 값은 출력하지 않고 키 · 건수 · 같은지 여부만 봤다. 스크립트는 scratchpad 에서 `python3 -I` 로 돌림.
- 로컬 DB: `day-local-postgres-1` · DB `day` · 스키마 `day_dev` — `SELECT count(*)` 만(쓰기 0). HAR id 는 셸 변수로만 넘기고 출력하지 않음.
- 실명 · id · 키는 적지 않는다(「HAR 의 상담사」 · 「HAR 의 일정」).

---

## 0. 요약

- **E3 「KOS 에서 상담사 누가 했는지 불러오나」 → 불러와 있다.** DAY 는 10초 일정 동기화로 `consultations[].counselors[]` 를 `consultation.counselor_id` 에 이미 저장한다. 로컬 DB 에서 HAR 의 상담 · 그 상담사가 `consultation` 행에 그대로 들어와 있고, 그 방문은 지금 판 카드다(§2 SQL). **새 KOS 호출은 필요 없다.** 판 조회 · 스냅샷 · 템플릿에 싣기만 하면 된다.
- **「여러 명 다」는 지금 구조로 안 된다.** 매퍼 `single()` 이 상담사가 **둘 이상이면 아무도 저장하지 않고 비운다**(`mapper.py:521-524`). 칸도 `consultation.counselor_id` 한 칸이고, spec-000 이 「한 상담에 한 명(사용자 2026-11-03)」으로 정해 두었다(`spec-000:431 · :500`). 여러 명을 담으려면 **migration + spec-000 변경**이 필요하다.
- **오더 메모와 상담은 다른 행이다.** 오더 메모 = 일정(방문) 단위 `orderMemo` → `visit.procedure_order_note`. 상담 = `consultation` 행(방문 1 : N). KOS 일정 응답에는 오더 메모를 **누가 썼는지 알려 주는 칸이 없다**(HAR entry 38 · 24 일정 키 목록). 그래서 「그 메모를 쓴 상담의 상담사」로 정확히 묶을 수는 없고, 「그 방문 상담들의 상담사」로 묶는 것이 최선이다.
- 앱은 `cards[]` 의 아는 키만 읽는다 → 새 칸을 더해도 깔린 앱은 무영향(§5).

---

## 1. DAY 가 지금 저장하는 상담사 값 전부

| 테이블 · 칸 | 원천(KOS 응답 · 필드) | 매핑 · 저장 | 주기 | 로컬 DB(day_dev) |
|---|---|---|---|---|
| `consultation.counselor_id`(FK staff · `models/visit.py:101`) | 일정 `schedule/v2/queries/get-schedules-grouped-by-zone` 의 `schedules[].consultations[].counselors[]`(`{id, name}` 배열) | `emr/kos/mapper.py:527-537 consultation()` → `counselor_external_id=single(row.get("counselors"))`(`:535`) → `emr/sync.py:1631-1688 _apply_consultations` → `staff` external_ref 로 id 바꿈(`:1643-1654`) · upsert(`:1666-1677`) · 이번 응답에 없는 상담은 absent 표시(`:1679-1688`) | 일정 동기화 **10초**(`tasks/emr.py:3,36,66` · `config.py:114` `SYNC_SCHEDULE_INTERVAL_SECONDS`) | 상담 6행 · counselor 있음 6 · 삭제 0 |
| `visit.requested_counselor_id`(`models/visit.py:54`) | 같은 일정 응답 `reservation.counselor{id,name}`(희망 상담사 · 예약 때 지정) | `mapper.py:600` `ref_id(reservation.get("counselor"))` → `sync.py:855,941` | 10초 | 방문 74 · 있음 4 |
| `customer.assigned_counselor_id`(`models/customer.py:65`) | (KOS 고객 `counselor{id,name}` 지정 상담사 — `spec-000:380`) | **매핑 없음**(`emr/` grep 0) — 칸만 있음 | — | 고객 61 · 있음 0 |
| `consultation.doctor_id` | `consultations[].consultationDoctors[]` | `mapper.py:536` `single(...)` | 10초 | (이번 범위 밖) |

`single(...)` 규칙(`mapper.py:521-524`):

```text
ids = staff_ids(value); return ids[0] if len(ids) == 1 else None
```

→ **0명 · 2명 이상이면 None.** 여러 명 중 하나를 고르는 게 아니라 **전부 버린다**. 주석 근거 = SPEC-002 OQ-13(`spec-002:932` 「한 상담에 상담사 · 의사가 둘 이상 오는 경우 — 지금 HAR 엔 값 있는 배열 없음」) · `normalized.py:232` docstring 「한 명일 때만(둘 이상이면 비운다)」. 테스트 `tests/day/emr/test_kos_board_contract.py:102-109` `test_상담_한_명일_때만_사람을_넣는다`(상담 의사 둘 → None 단언).

그 밖: `sync.py:1640` docstring 「상담 사본 — 이 화면에서 쓰지 않는다」. 지금 판 조회(`queries/board.py`)는 `consultation` 테이블을 **읽지 않는다**(grep `consultation` queries/board.py = 0).

## 2. 판 카드의 「담당 상담사」 후보 — HAR 대조 · 로컬 DB

### HAR 에서 본 것(entry 번호)
- entry 41(상담 생성 전) `get-consultations-by-visitor-id` → `data` 비어 있음(11 bytes).
- entry 78 `consultation/v1/commands/create-consultation` 요청 키 = `consultationId · consultationStartedDateTimeUtc · content{text} · counselorIds(배열 · 1개) · scheduleId · visitorId` → **KOS 는 상담 하나에 상담사를 배열로 받는다.**
- entry 80(생성 뒤) `get-consultations-by-visitor-id` → 상담 1건, 키 = `consultationDoctors · consultationProcedures · consultationStartedDateTimeUtc · content · counselors · createdDateTimeUtc · id · scheduleId · updatedDateTimeUtc · visitor`. `counselors` = 1명(`{id, name}`). `scheduleId` = entry 38 일정 id 와 **같음**.
- entry 24 `get-schedules-for-reservation`(일정 24건) · entry 38 `get-schedule-detail`(그 일정) — 둘 다 **상담 생성 전** 응답이라 `consultations[]` = 전부 0건. 일정 단수 칸 `consultation{consultationMemo, counselor, doctor}` 는 24건 모두 id · name 이 **빈 글자**. `reservation.counselor` 는 24건 중 2건만 값 있음 · 대상 일정은 빈 값.
- 코디 메모 「entry 24 `tasks[].doctors[]` 에도 같은 이름」 → **확인함: 대상 일정이 아니다.** HAR 의 상담사 id 는 **다른 일정 2건의 작업 6개**(ETCETERA 1 · PROCEDURE 5)의 `doctors[]` 에 있다. 대상 일정의 작업에는 없다. 그 계정의 KOS 직무 이름 = 「관리자」(entry 12 `get-accounts` 의 `roleName`). 즉 이 계정이 데모에서 다른 고객의 시술 담당으로도 쓰인 것이고, 「상담 작업의 담당자」는 아니다.
- DAY 동기화 원천(`get-schedules-grouped-by-zone`)은 이 HAR 에 없다. 대신 저장소 고정본 `tests/day/emr/fixtures/kos_schedules.json` 에 `schedules[].consultations[].counselors[]`(`{id, name}`) 모양이 있다 — `get-schedule-detail` 고정본 `kos_schedule_detail.json` 도 같은 모양.

### 후보별

| 후보 | HAR 의 상담사와 같은가 | 로컬 DB 로 판 카드에 붙나 |
|---|---|---|
| (a) 그 방문의 `consultation.counselor_id` | **같음** — HAR 상담 id 의 `external_ref(consultation)` 1행 · 그 행 `counselor_id` 의 `external_ref(staff)` = HAR 상담사 id(1건 일치) | **붙음.** 그 방문(HAR 일정 id 의 visit)은 지금 판 대상(`procedure_waiting`/`procedure` · 방 있음) 1건 · 오더 메모 있음 1건. 판 대상 방문 23 중 상담사 있는 상담이 붙은 방문 3 |
| (b) `visit.requested_counselor_id` | **다름** — 대상 일정 `reservation.counselor` 는 빈 값(entry 38). 예약 때 지정한 「희망 상담사」라 실제 상담한 사람과 다를 수 있음 | 판 대상 23 중 0건. 상담 counselor 와 같은 행 0건(둘 다 값 있는 행 0) |
| (c) 상담 작업(task)의 담당자 | **아님** — 위 「다른 일정」 참고. 대상 일정 작업에 그 사람 없음 | DAY 는 작업 담당을 `visit_task_staff` 로 저장하지만 상담 전용 작업 구분이 없다(확인 안 됨 — 이번 범위에서 더 보지 않음) |
| (d) 일정 단수 칸 `consultation.counselor` | HAR 24건 모두 빈 값 — 이 칸은 쓰이지 않는 것으로 보인다 | DAY 매핑 없음(`mapper.py` grep `consultationMemo` = 0) |
| (d) `customer.assigned_counselor_id`(고객 지정 상담사) | 이 HAR 에 고객 응답(entry 34 `get-visitor`) 있음 — 대조 안 함(확인 안 됨) | 매핑 없음 · 로컬 0 |

로컬 SQL 결과(건수만):

```text
consultation: 전체 6 · counselor 있음 6 · 삭제 0 · 상담사 빈 행 0
visit: 전체 74 · requested_counselor 있음 4 · 오더 메모 있음 33
customer: 전체 61 · assigned_counselor 있음 0
판 대상 방문(procedure_waiting/procedure · 방 있음): 23 · 상담사 있는 상담 붙음 3 · requested_counselor 있음 0
상담 2건 이상인 방문: 0
HAR 상담 id → external_ref(consultation) 1 · HAR 일정 id → external_ref(visit) 1 · HAR 상담사 id → external_ref(staff) 1
HAR 상담 행의 counselor = HAR 상담사: 1
HAR 일정 방문: 판 대상 1 · 오더 메모 있음 1
```

판 조회가 이미 그 병원 직원 전부(`queries/board.py:298-309` — 지운 직원만 뺌 · 비활성 · 시스템 계정도 이름은 실음)를 `world.staff` 에 싣는다 → 상담사 이름을 얻으려고 직원 쿼리를 더할 필요는 없다.

## 3. 여러 명 — 담을 칸이 있나

- **없다.** `consultation.counselor_id` 한 칸(`models/visit.py:101` · migration `20261105_0002…py:1182,1199`) · `NConsultation.counselor_external_id: str | None`(`normalized.py:238`) · 매퍼 `single()`.
- KOS 는 배열이다: 응답 `counselors[]`(entry 80 · 고정본) · 쓰기 `counselorIds[]`(entry 78). 로컬 데이터는 6건 모두 한 명(상담사 빈 행 0)이라 **2명 이상이 실제로 버려진 행은 지금 로컬에 없다**(다만 2명이면 `counselor_id` 가 null 로 들어가므로 「빈 행 0」 = 버려진 것 0).
- 바꿀 후보:

| 후보 | 모양 | migration | 데이터 규칙 · 스펙 |
|---|---|---|---|
| ① 연결 테이블 `consultation_counselor` | `(id, consultation_id FK, staff_id FK, created_at, updated_at, deleted_at)` · 순서가 필요하면 `sort_order` | 필요(새 테이블 + 기존 `counselor_id` 를 옮기거나 둠) | data_rules 0(소프트 딜리트 · `deleted_at`) · 13(DAY 테이블엔 생성 · 수정 · 삭제 시각만) · 1(외부 id 는 external_ref 만 — 연결 행엔 staff FK 만)에 맞음. spec-000 `consultation` 의 `procedures → consultation_procedure` 와 같은 1:N 꼴(`spec-000:503,514`) |
| ② `consultation.counselor_ids uuid[]` | 배열 칸 | 필요 | FK 를 걸 수 없음(spec-000 「직원류 칸은 staff FK」 `:130` 과 어긋남) · 소프트 딜리트 단위가 행이 아님 |
| ③ 지금 칸 유지 + `single()` 을 「첫 명」으로 | 한 명만 | 불필요 | 사용자 결정 「여러 명 다」와 어긋남 |

- 충돌하는 결정: `spec-000:431` 「상담사 · 상담 의사는 한 상담에 한 명」 · `:500` 「상담사 — 한 상담에 한 명(사용자 2026-11-03)」 · `spec-002:747`(동기화 표 · OQ-13) · `spec-002:932` OQ-13. 사용자 새 결정(「여러 명 다」 · 2026-11-12)으로 **spec-000 · spec-002 OQ-13 을 고쳐야 한다**.
- `config/projects/day.json` data_rules 에 배열 · 연결 테이블을 막는 규칙은 없다(0 ~ 16 전부 읽음). 규칙 7(「외부가 가진 정보를 처음부터 전부 DAY 칸으로」)은 오히려 여러 명을 다 받는 쪽을 민다.
- 상담 의사(`consultationDoctors` · `doctor_id`)도 같은 `single()` 이다 — 같이 바꿀지는 범위 밖(정할 것).

## 4. 오더 메모의 원천과 상담의 연결

- 오더 메모 = 일정 단위 `orderMemo` 글 → `mapper.py:620` `procedure_order_note=text(row.get("orderMemo"))` → `sync.py:955` → `visit.procedure_order_note` → `queries/board.py:120` → `board_rules.py:814` 스냅샷 `cards[].orderMemo` → `board_parts.html:170` `ui.memo(...)`. 테스트 `tests/day/emr/test_kos_mapper.py:210-232` 「오더 메모는 일정의 orderMemo 만」. 스펙 `spec-002:183`(카드 메모 = 오더 메모만 · 일정 단위) · `spec-000:432`.
- 상담 메모는 다른 칸 `consultation.consultation_note`(`content.text`) — 카드에 안 보임(`spec-002:183` · 사용자 2026-11-06 F8).
- **같은 행이 아니다**: 오더 메모는 `visit` 칸, 상담사는 `consultation` 행(방문 1 : N · `spec-000:493-500`). KOS 일정 응답에도 오더 메모의 작성자 · 작성 시각 · 상담 id 같은 칸이 없다(HAR entry 24 · 38 일정 키: `consultation · consultations · createdDateTimeUtc · … · orderMemo · …` — `orderMemo` 는 글 하나).
- 묶는 길(후보 — 결정 아님):
  - (가) 「그 방문의 상담 전부의 상담사」(삭제 안 된 상담 · 상담사 겹치면 한 번) — 방문 = 오더 메모 단위이므로 가장 가까움. 로컬은 방문당 상담 최대 1건(2건 이상 0).
  - (나) 「그 방문의 가장 최근 상담(`started_at`)의 상담사들」 — 상담이 여럿일 때만 (가)와 다름.
  - 「그 메모를 쓴 상담의 상담사」로 정확히 묶기는 **KOS 가 작성자를 주지 않아 불가**(확인한 응답 범위에서).

## 5. 스냅샷에 싣는 자리 · 앱 영향

- 자리 후보: `board_rules.py:814` `"orderMemo": v.order_memo` 옆 — 예 `"counselors": [{"staffId", "name"}]`(여러 명 · 순서 = 정할 것). 값은 `BVisit`(`dtos/board.py:59-69` 근처 · `order_memo` `:64`)에 칸을 더해 `queries/board.py` 가 채움. 스펙 모양 `spec-002:603`(`cards[] … orderMemo`).
- 판 조회 쿼리: 상담을 방문 id 묶음으로 한 번 더 읽어야 함 → `tests/day/board/test_board_queries.py:155-166` 의 `assert one == 15`(쿼리 수 고정)이 16 이 된다(방문 수와 무관하게 같은 수면 `one == ten` 은 그대로). 기존 쿼리에 join 하면 수는 그대로일 수 있음 — 구현 선택.
- **앱 무영향**: `app/lib/model/board.dart:210-224 BoardCard.parse` 는 이름 붙은 키만 읽는다(`m['orderMemo']` `:217` 등). 모르는 키를 검사하거나 실패하지 않음 → 새 칸을 더해도 깔린 앱(TestFlight · 심사본)은 그대로. 참고: 앱 방 상세는 이미 오더 메모 제목 줄 「오더 메모」 + 파란 「접기 / 크게 보기」를 그린다(`app/lib/ui/room_screen.dart:336-360`) — E4 웹 모양과 비슷하다. 앱에 상담사 배지를 넣는 건 이번 범위 밖(정할 것).

## 6. 손댈 파일 목록(grep 전수)

grep: `counselor|consultation|orderMemo|order_memo|day-memo|ui.memo|memo-toggle|오더 메모|접기|크게 보기`(backend · app/lib · tests)

### 백엔드 — 동기화(「여러 명」을 받을 때만)
- `backend/day/emr/kos/mapper.py:521-537`(`single` · `consultation()`)
- `backend/day/emr/normalized.py:232-240`(`NConsultation.counselor_external_id`)
- `backend/day/emr/sync.py:1631-1688`(`_apply_consultations` — 연결 테이블 upsert · absent 처리)
- `backend/day/models/visit.py:95-103`(`Consultation`) + 새 모델(연결 테이블이면) · `models/__init__.py`
- `backend/migrations/versions/` 새 파일
- 테스트: `tests/day/emr/test_kos_board_contract.py:102-109` · `tests/day/emr/test_sync.py:379-406`(`cons.counselor_id is not None`) · `tests/day/test_column_snapshot.py:112-120`(consultation 칸 목록) · 고정본 `tests/day/emr/fixtures/kos_schedules.json` · `kos_schedule_detail.json`(여러 명 사례를 더하려면)

### 백엔드 — 판 표시(한 명이든 여러 명이든)
- `backend/day/queries/board.py:95-123`(방문 → `BVisit`) + 상담 조회 추가 · `:298-309`(직원 이름은 이미 있음)
- `backend/day/dtos/board.py:59-69`(`BVisit` 에 상담사 칸)
- `backend/day/services/board_rules.py:814`(스냅샷 `cards[]`)
- `backend/day/routers/kit_board.py:111,123`(dev 견본 world 의 `order_memo` 옆에 상담사 값)
- 테스트: `tests/day/board/test_board_queries.py:155-166`(`one == 15`) · `tests/day/board/test_board_rules.py`(스냅샷 모양 단언이 있으면 — 확인 안 됨) · `tests/day/web/test_board_page.py`(메모 단언 — 지금 `day-memo` 단언 0, 새로 더할 자리)

### 템플릿 · JS · CSS(E1 · E2 · E4)
- `backend/day/templates/ui.html:226-236`(`memo()` 매크로 — 제목 줄 「오더 메모」 · 상담사 배지 · 오른쪽 끝 파란 「접기 / 펼치기」 · 구분선 없음). 호출처: `templates/partials/board_parts.html:170`(판 카드) · `templates/partials/kit_page.html:217,285-287,512,525`(dev 견본)
- `backend/day/static/day.js:15,434,459-462,804-810`(펼침 토글 · `aria-label` 「메모 접기 / 메모 크게 보기」 글자를 바꾸는 곳 `:810`)
- `backend/day/styles/app.css:161`(`--day-memo-max-h` — 지금 fix-web 이 80px · 12px 기준. E2 14px 이면 다시 계산) · `:447-451`(`.day-memo` · `__box` · `__more` 아이콘 자리 — 아이콘을 글자 버튼으로) → `scripts/build-css.sh` 로 `static/day.css` 재빌드
- 배지 모양: 기존 `ui.sq_badge`(`ui.html` — 마취 칩 · 「수납 필요」가 씀) 재사용 후보
- 화면 문구 표 `tests/architecture/test_screen_copy.py:120-124`(「메모」 · 「메모 접기」 · 「메모 크게 보기」 · 「접기」 · 「크게 보기」 있음) — **「오더 메모」 · 「펼치기」 는 표에 없음** → 근거와 함께 더해야 함(`:156-159` 표에 없는 글자는 실패)

### 스펙
- `spec-000-data-model.md:431`(한 상담에 한 명) · `:493-503`(`consultation` 표 · `counselor_id`) · `:130`(직원류 FK 목록 — 새 칸이면)
- `spec-002-procedure-board.md:182-183`(U-1 카드 안 · 카드 메모 = 오더 메모만 — 제목 줄 · 상담사 배지 추가) · `:166`(E39) · `:603`(스냅샷 `cards[]`) · `:747`(동기화 표 consultation 행) · `:932`(OQ-13)
- (앱도 바꾸면) spec-003 방 상세 오더 메모

## 확인 안 됨

- DAY 동기화 원천 `get-schedules-grouped-by-zone` 응답에서 **상담 생성 직후** `consultations[].counselors[]` 가 실린 실물 — 이 HAR 엔 그 호출이 없다. 다만 로컬 DB 에 HAR 상담 · 상담사가 들어와 있으므로 동기화 경로로 받은 것은 확인됨(어느 응답에서 받았는지는 코드상 그 하나뿐).
- KOS 가 상담사를 **2명 이상** 준 실물(HAR · 로컬 모두 1명). `counselorIds` 가 배열이라 가능은 함.
- (c) 상담 작업 구분 · (d) 고객 지정 상담사(entry 34) 대조.
- `test_board_rules.py` 에 스냅샷 `cards[]` 키 전체를 단언하는 곳이 있는지.

## 고칠 방향 후보(결정 아님)

1. **표시만 먼저(migration 없음)**: 판 조회에서 방문별 상담(`consultation` · 삭제 안 됨 · `counselor_id` 있음)의 상담사 이름을 모아 `cards[].counselors[]` 로 싣고 E4 제목 줄 배지로 그림. 지금 저장 구조라 상담당 1명까지만(2명 이상은 동기화 단계에서 이미 비어 있음). 방문에 상담이 여럿이면 여러 명이 됨.
2. **여러 명까지(migration)**: 연결 테이블 `consultation_counselor` 추가 · `single()` 대신 전부 · `_apply_consultations` 가 연결 행 upsert · 소프트 딜리트 → 1번 표시가 그 테이블을 읽음. spec-000 · OQ-13 갱신.
3. 2를 하면서 `consultation.counselor_id` 를 남길지(첫 명 · 호환) 없앨지.

## 정할 것

1. 「여러 명 다」의 범위: (가) **한 상담의 여러 상담사**(KOS `counselors[]` 2명 이상 — 지금 버려짐 · migration 필요)까지인가, (나) **한 방문의 여러 상담**(상담마다 1명 — 지금 구조로 됨)까지인가.
2. (가)라면 담을 모양: 연결 테이블(후보 ①) vs 배열 칸(②) — 그리고 spec-000 「한 상담에 한 명(사용자 2026-11-03)」 결정을 바꾸는 것 확인.
3. 상담 의사(`consultationDoctors` · 같은 `single()`)도 같이 여러 명으로 바꾸나.
4. 「담당 상담사」 = 그 방문의 상담 **전부**의 상담사인가, **가장 최근** 상담만인가. 순서(상담 시작 순 · 이름 순).
5. 희망 상담사(`visit.requested_counselor_id` — 예약 때 지정)는 상담 기록이 없을 때 대신 보여주나, 안 보여주나(로컬 판 카드엔 0건).
6. 상담사가 없을 때 제목 줄: 「오더 메모」만 두나. 오더 메모가 없고 상담사만 있으면 제목 줄을 그리나(지금은 메모 없으면 칸 자체를 안 그림 `board_parts.html:170`).
7. 앱 방 상세(오더 메모 제목 줄이 이미 있음)에도 상담사 배지를 넣나 — 넣지 않으면 앱 변경 0.
8. 퇴사 · 비활성 직원(`is_active` false)인 상담사도 이름을 보여주나(판 조회는 지운 직원만 뺌).
