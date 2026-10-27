---
type: work
id: WORK-007
title: "전체현황판 「현황 › 예약 현황」 — 스케줄 표 · 등록 · 상세(접수 묶음 · 실장 호출 · 귀가 정산) · WP-KOS 먼저"
status: todo
product: cc-prototype
feature: procedure
work_type: new-feature
owner: kknaks
progress: 0
created_at: 2026-10-26
updated_at: 2026-10-27
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-009-reservation-board|BASE-009]]"
  decisions:
    - "[[decision-006-reservation-board|DEC-006]]"
  specs:
    - "[[spec-005-reservation-board|SPEC-005]]"
    - "[[spec-003-procedure-board|SPEC-003]]"
    - "[[spec-004-procedure-app|SPEC-004]]"
  works:
    - "[[work-006-overall-board-undo|WORK-006]]"
  releases: []
  related: []
sources:
  - "orchestration/work/overall-board/_RESUME.md §2 (2026-10-26 줄)"
  - "reference/2026-10-26-cc-reservation/workflow-v3.md"
  - "orchestration/work/overall-board/reservation-*-report.md (15건)"
  - "cc-prototype overall-board procedure/ (d05cd88 — 읽기만)"
  - "orchestration/work/overall-board/reservation-review-doc-r1.md (r1)"
  - "orchestration/work/overall-board/reservation-kos-probe-report.md (WP-KOS)"
  - "orchestration/work/overall-board/reservation-e2e-feedback.md (E2E batch 1 · 2026-10-27)"
  - "orchestration/work/overall-board/reservation-e2e-batch1-brief.md (batch 1 BE · FE 몫)"
---

# 전체현황판 「현황 › 예약 현황」 — 빌드 계획

계약은 **SPEC-005 0.3.0**(r3 — 사용자 로컬 E2E batch 1 · 23건 · DEC-006 D-51 ~ D-57 · 부록 F. 0.2.0 = r1 처분 · U1 ~ U7 · WP-KOS) — 이 문서는 빌드 계획만 적고 계약을 다시 쓰지 않는다. 사용자 지시 「코드까지 다 작성해서 알려줘 — e2e 로컬 해보게」(`_RESUME 10-26 #49`)의 순서: 문서 → reviewer_doc → **WP-KOS** → BE ∥ FE → reviewer → 코디 검증 → 사용자 로컬 E2E.

## Meta

- Covers spec: SPEC-005 0.3.0 전부(§1 ~ §10 · 부록 A ~ F) · SPEC-003 §7.4 경로 수(19 → 34 · SPEC-005 §7.6) · SPEC-004 §3.1 · §3.4(역할 `coordinator` 더함 · SPEC-005 §3.4)
- 코드 레포: `kknaksss/cc-prototype` — 범위 `procedure/back/**` · `procedure/front/**` · `procedure/.env.example` · `procedure/README.md`. **`procedure/app/`(앱) · infra 는 건드리지 않는다**(D-02 · SPEC-005 §1.2)
- base: 같은 코드 브랜치 **`kknaksss/overall-board`**(PR #6 에 이어서 · `d05cd88` 위) — `_RESUME 10-26 #49`
- 워커: backend(WP-KOS · WP-BE0 ~ BE4) · frontend(WP-FE1 ~ FE3) · reviewer · 코디(E2E)
- 순서 원칙: **WP-KOS(데모 실호출 확인)를 맞물리는 BE 앞에** — **2026-10-26 끝남 · 게이트 통과**(「안 받음」 0 · 모양 다름 5 는 SPEC-005 0.2.0 부록 E 로 반영). 남은 실물 확인(정원 초과 동시 조작 · 접수 뒤 [실장 호출] · 딥링크 2)은 WP-E2E
- 검증은 WP 마다 그 범위만(시험 · 빌드). 전체 검증(compose · 데모 지점 E2E)은 WP-E2E 에서 한 번
- 배포: 이번 문서 범위 밖 — 사용자 E2E 통과 뒤 코디가 정한다

## 계약 고정점 — BE ↔ FE 병렬의 기준

| 고정점 | 값 | SPEC-005 |
|---|---|---|
| 화면 경로 | `/reservations/live`(+ `/reservations` → live) · 헤더 드롭다운 「시술 현황」 · 「예약 현황」 순 · 「현황」 글자 · 첫 화면 = 시술 현황(D-49) | §6.1 |
| 조회 API | `GET /api/reservations/board?date=` · `GET /api/reservations/{id}` · `GET /api/reservations/form` · `GET /api/customers/search` — 응답 모양 = §7.2 · §7.3 · §7.4(0.2.0: `zones` · `capacities` · `zoneId` · `rows` · `identity.fields` · `receiveMode` · `roomLocked`) | §7.2 ~ §7.4 |
| 조작 API | §7.5 표 11개(경로 · 요청 · 성공 · 409 코드 — `identity_incomplete` · `room_locked` 포함) · 공통 400 · 404 · 502 `kos_unavailable` · 409 `kos_rejected` · 오류 본문 `{error:{code,message,step?,candidate?,fields?}}` | §7.5 · §4.4 |
| 상태 문자열 | `state.main` ∈ `reserved · reception · consultation · procedure · home · canceled · noshow` · `state.sub` ∈ `waiting · doing · done · null` | §5.1 |
| 규칙 값 | `full` · `plusAllowed` · `draggable` · `paymentRequiredCount` · `can.*` · `receiveMode` · `roomLocked` · `identity.complete` · `busy` · `busyRoom` · `needsCheck` 는 back 이 계산 — front 는 다시 계산하지 않는다 | §5 머리 · §5.14 |
| 역할 | `coordinator` 더함 · 예약 API 는 네 역할 모두 | §3.4 · §7.1 |
| 가짜 응답 | `PROC_FAKE_BOARD=1` 이면 GET 넷 = `service/fake_reservations.py` 지어낸 값 · 조작 403 `fake_board` | §7.1 |
| 갱신 | front 10초 폴링 · 조작 성공 직후 + 2초 뒤 다시 부름 · SSE 안 씀 | §6.7 |

**가짜 응답은 WP-BE0 가 먼저 낸다** — `schemas/reservations.py`(응답 모델) + `api/reservations.py`(경로 15개) + `service/fake_reservations.py`(지어낸 값 — 시안 실명 치환 규칙 · 칸 13개(+ 「그룹 없음」 1) · 구역 2(켜진 구역 둘인 칸 1) · 상태 7종 · 카드 수납 필요 1건 · 귀가 대기 1건 · 공지 1줄 · 원내 현황 3명(두 구역) · 상세 1건씩 상태별 + 부도 · 이어 하기(방 고정) · 신분 칸 빔 1건)를 **첫 커밋**으로. FE 는 그 위에서 그린다. 실제 경로(가짜 아님)는 BE1 ~ BE4 가 채우기 전까지 501 `not_ready` 를 돌려도 된다(그 사이 FE 는 가짜만 쓴다).

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-KOS** | **데모 지점 실호출 확인 — 맞물리는 BE 앞**. 데모 테넌트 확인(SPEC-003 WP-KOS 와 같은 `assert`) 뒤 **1회씩** 보내고 1 ~ 3초 뒤 다시 읽어 전후를 적는다. K1 읽기 모양 — `get-schedules-for-reservation{baseDateUtc, reservationGroupIds, zoneIds:[4층]}` · `get-reservation-groups` · `getReservationSlotsByGroupsV2` · `get-notices`(그 날짜) · `get-codes{FUNNEL}` · `get-etcetera-tasks` · `get-visitors`(이름 하나) · `get-visitor` · `getVisitorQuestionnaire` `pages[]` 키 · `getQuestionnaireSubmit`(제출본 있는 고객) · `getSchedulesByVisitor` · `get-schedule-detail` 의 키가 SPEC-005 §3.3 · §4.2 와 같은지 / K2 **신규 고객** `find-duplicated-visitor` → `create-visitor`(동의 플래그 없이 — OQ-753) → `reserve`(**전 칸**: `doctors` · `counselor` · `funnel`(KOS 웹 JS 에서 요청 모양을 먼저 읽는다 — OQ-754) · `reservationMemo` · `sedationRequired` · `consultationRequired` · `desiredDischargeDateTimeUtc`) — 일정 상세에 각 칸이 보이나 / K3 내부 `update-reservation` 이동(`items` 에 `doctors` 그대로) — 지정 의사 · 메모 · 유입 남나 / K4 `update-reservation{consultationRequired}` 단독 · K5 `update-reservation{counselor}` 단독 — 다른 칸 남나(OQ-755) / K6 공개 `change-reservation-memo` / K7 `get-visitor` → `update-visitor-personal-information`(여권 성 · 여권번호 · 국적 · 생년월일 꼴 — OQ-739) — 고치지 않은 칸 남나 / K8 접수 묶음 끝 단계 `PROCEDURE_WAITING`(바로 시술 — OQ-756) / K9 **귀가** — K8 일정을 KOS 에서 시술 진행 → 작업 완료 → `PROCEDURE_DONE`(공개 change-flow-step · 「방 배정」 취소)으로 만든 뒤 공개 `changeFlowStep(COMPLETED)` — 그리고 수납 필요 작업이 남은 일정에서 KOS 가 거절하는지(OQ-728) / K10 정리 — 만든 예약 · 고객을 목록으로 남기고(지우지 않음 — 지울지는 사용자) 리포트에 적는다. 호출은 **일회성 스크립트**(back `KosClient` import 가능 · 레포에 남기지 않음) · 사용자 스택(3700 · 8700) 건드리지 않음 · env 값 출력 금지 | §8 「미확인」 줄 · §10 OQ-728 · OQ-739 · OQ-753 ~ OQ-756 | backend | 코드 변경 없음 · 리포트 `orchestration/work/overall-board/reservation-kos-probe-report.md` | K1 ~ K10 표(경로 · 본문 키 · HTTP · 거절 이름 · 전후 값 모양) · **판정 한 줄씩**: 신규 생성 · 전 칸 예약 · 내부 이동 · 진행 경로 · 상담사 · 메모 · 고객 수정 · 바로 시술 · 귀가 · 귀가 거절 = 「받음 / 안 받음 / 모양 다름(무엇)」 · `funnel` 요청 모양 확정 · 남긴 데모 데이터 목록. **public — KOS id · 키 · 토큰 · 실명 · 고객 값 0** | `grep -nE '[0-9a-f]{8}-[0-9a-f]{4}-\|[0-9a-f]{24}\|@[A-Za-z0-9.-]+\.[a-z]{2,}\|Bearer \|eyJ' orchestration/work/overall-board/reservation-kos-probe-report.md \| wc -l` = **0**(표 안이라 `\|` — 실행 때는 역슬래시 없이) | **완료(2026-10-26)** — 리포트 `reservation-kos-probe-report.md` · 「안 받음」 0 · 모양 다름 5 · 쓰기 20(데모 · 운영 키 0) · 남긴 데모 데이터 = 고객 1 · 일정 2 |
| (게이트) | 코디가 WP-KOS 판정을 읽는다. 모두 「받음」 → 고정점 그대로 BE3 · BE4. 「안 받음 · 모양 다름」이 하나라도 있으면 SPEC-005 해당 줄(§8 · §5)을 planner 가 고친 뒤 BE3 · BE4(사용자 결정이 필요한 것은 옵션 + 권장으로 올린다 — 예: 내부 이동이 지정 의사를 지우면 공개로 바꿀지). **BE0 · BE1 · BE2 · FE 는 게이트를 기다리지 않는다**(읽기 · 화면 계약은 K1 결과로만 고칠 수 있다 — K1 이 다르면 BE1 이 그 키를 따른다) | §10 | 코디 | — | 판정 기록 · (필요하면) SPEC 개정 | — | **통과(2026-10-26)** — 모두 「받음」. 모양 다름 5(문진 제출본 최상위 · 없음 = 400 + `errorProperties` · `room:{id:""}` · `change-tasks-room` 약 1초 · 시각 밀리초 없음)는 planner r2 가 SPEC-005 0.2.0 §3.3 · §4.2 · §4.4 · §5.6 · §5.11 · §8 에 반영(부록 E). BE3 · BE4 막힘 없음 |
| **WP-BE0** | **계약 뼈대 + 가짜 응답(첫 커밋)** — `schemas/reservations.py`(§7.2 ~ §7.5 모델 · 상태 Literal · 오류 코드) · `api/reservations.py`(경로 15 · `require_real_board` 는 조작만) · `service/fake_reservations.py`(지어낸 값 — 위 「가짜 응답」) · `main.py` router 등록 · `tests/test_order.py` 경로 수 34(**`test_route_count_19` → `test_route_count_34` · 34 = HTTP 33(router 32 + health) + WS 1** — SPEC-005 §7.6) · `tests/test_contract.py` 응답 모양 | §7 · §7.1 · §7.6 | backend | `procedure/back/app/{schemas/reservations.py, api/reservations.py, service/fake_reservations.py, main.py}` · `tests/test_order.py` · `tests/test_contract.py` · `tests/test_resv_contract.py`(새) | 가짜 모드 GET 넷이 §7 모양(0.2.0 키 포함) · 조작 403 `fake_board` · 경로 34 · 기존 시험 전부 통과 | `cd procedure/back && uv run ruff check . && uv run pytest -q tests/test_order.py tests/test_contract.py tests/test_resv_contract.py` | 대기 |
| **WP-BE1** | **사본 · 조회 · 스케줄 표 · 코디 역할** — ① `repository/db.py` 새 표 7(`zone` · `reservation_group`(`capacities` 구역별) · `reservation` · `reservation_slot` · `notice` · `funnel_code` · `etc_task_def`) + ccc 표 2(`identity_check` · `questionnaire_history`) · `customer.gender` MIGRATIONS ② `kos/reservation_sync.py` — 1시간 목록(구역 · 그룹(`zoneIds` 전 구역) · 유입 · 기타 작업 · **다른 구역 방**(`get-rooms` 4층 밖 구역마다 → 같은 `room` 사본), 서버 시작 1회 포함 · `KosRuntime.master_once` 에 이어 붙임) · 날짜별 조회 4종(§4.2 · `zoneIds` 전 구역 · 10초 캐시 · 날짜 잠금 · 실패 = `sync.lastError` · 「오늘 사본 갱신」 함수 — §4.2 W7) · `room.id` 빈 값 = 방 없음 · 시각 파싱 비교 ② ′ `kos/client.py` — `KosError.errorProperties`(`[{key, reason}]` · 값 없음 · 메시지 문자열 그대로) ③ `domain/reservation_rules.py` — 2계층(§5.1) · 축 · 칸(「그룹 없음」 · 칸 머리 정원 구역별) · 카드(묶음당 · `zoneId`) · 건수 · `full` 구역별 · `plusAllowed` · `draggable` · 「방 배정」 판정 = `domain/rules.py` `is_room_task` 와 같은 식 + **잇는 키**(`reservation.kos_id` ↔ `visit.kos_id` · `sequence` ↔ `kos_sequence` · visit 없음 = 호출 0 — §5.9) · 수납 필요(카드 · 원내 · 정산 같은 값) ④ `service/reservations.py` board 조립(§7.2 · 원내 현황 두 구역 · 금액) ⑤ 코디 역할 — `config.py` `CCC_COORD_*` · `service/accounts.py` `_fixed`/`_passwords` · `schemas` `Role` · **`service/actions.py` `accept()` 의 `admin` 분기에 `coordinator`(SPEC-005 §3.4 · r1 F2)** · `.env.example` · README env 표 ⑥ env `KOS_WEB_BASE` · `KOS_ROOM_TASK_ID` · `KOS_RESV_CACHE_SEC` | §2.3 · §3 · §4.1 ~ §4.3 · §5.1 ~ §5.4 · §5.7 · §5.9 · §7.2 · §3.4 | backend | `procedure/back/app/{config.py, repository/db.py, repository/repo.py, kos/client.py, kos/reservation_sync.py, kos/runtime.py, domain/reservation_rules.py, service/reservations.py, service/accounts.py, service/actions.py, schemas/actions.py}` · `procedure/.env.example` · `procedure/README.md` · `tests/fake_kos.py`(예약 조회 응답 더함 — **모양 = WP-KOS K1 실제**: 제출본 최상위 · 없음 400 + `errorProperties` · `room:{id:""}` · 밀리초 없는 시각 · 구역 2) · `tests/test_resv_board.py`(새) · `tests/test_auth_roles.py` | SPEC-005 §9 끝 「back 단위 시험」 중 §5.1 ~ §5.4 · §5.7 · §5.9 · 구역별 정원 · 칸 머리 · 「그룹 없음」 · 「방 배정」 잇는 키 · 오늘 사본 갱신 · `errorProperties` · 캐시 · 조회 실패 · 코디 계정 · 역할 · **코디 수락 = 됨 · `doctorId` 없으면 400**(`test_auth_roles.py` 한 줄) · 옛 DB 파일로 시작해도 새 표 · 열이 생기고 기존 행 남음 · 시술 현황 시험 전부 통과(다른 구역 방 행이 늘어도) | `cd procedure/back && uv run ruff check . && uv run pytest -q tests/test_resv_board.py tests/test_auth_roles.py tests/test_kos_sync.py` | 대기 |
| **WP-BE2** | **상세 · 검색 · 등록 칸 · 신분 확인 · 문진 이력** — `GET /api/reservations/{id}`(§7.3 — 고객 · **KOS 신분 칸 `identity.fields` · `complete`**(§5.12 ①) · 문진 양식 · 제출본(최상위 · 400 + `errorProperties visitorId NotFound` = 없음) · 이전 방문(오늘 뺌) · 수납 · 딥링크 · 그 구역 방 목록 사용 중 · 상담사 상태(두 구역) · `receiveMode` · `roomLocked` · `can.*` · 오늘 사본 갱신 먼저) · `GET /api/reservations/form`(구역 `available` · `defaultZoneId`) · `GET /api/customers/search`(결과 upsert) · `PUT /api/customers/{id}/identity`(표시만) · 확인 필요(§5.11) · 문진 이력 쌓기(같은 제출본 한 번) | §4.2 상세 · §5.7 · §5.8 · §5.11 ~ §5.14 · §7.3 · §7.4 · §7.5 identity | backend | `procedure/back/app/{service/reservations.py, domain/reservation_rules.py, repository/repo.py, api/reservations.py}` · `tests/test_resv_detail.py`(새) | 단위 시험 중 §5.8 · §5.11 ~ §5.14(신분 칸 외국인 · 내국인 · 국적 빈 값 · 영문명 하나 · 갈래 new/resume · 붙은 방 고정) · 상세 KOS 읽기 하나 실패해도 응답(`get-visitor` 실패 = 새 접수 꺼짐) · 딥링크(`KOS_WEB_BASE` 비면 null) | `cd procedure/back && uv run ruff check . && uv run pytest -q tests/test_resv_detail.py` | 대기 |
| **WP-BE3** | **쓰기 — 등록 · 이동 · 취소 · 메모 · 경로 · 고객 정보 · 특이사항**(게이트 뒤) — §8 순서 · 본문(**WP-KOS K2 ~ K7 판정 모양 그대로** — `funnel{funnel:<코드 행 전체>, funnelDetail}` · 이동 `items` 에 `doctors` · `zoneId` 그대로 · 고객 저장은 없던 키 안 보냄) · §4.4 동기 · 409/502 매핑(`errorProperties` 먼저 — §4.4 표) · `event_log` · 날짜 캐시 비움 · 신규 구분 규칙 · 중복 409 + candidate · 정원 409(고른 구역) · 등록 구역 기본 · 이동 = 길이 · 구역 유지 · 간격 경계 · 고객 저장 = 저장 직전 다시 읽은 묶음 + 바꾼 칸 · 특이사항 = 관리 묶음 + memo | §4.4 · §5.4 · §5.5 · §5.13 · §5.14 · §7.5 · §8 | backend | `procedure/back/app/{service/reservations.py, domain/reservation_rules.py, kos/reservation_sync.py, api/reservations.py}` · `tests/test_resv_write.py`(새) | 단위 시험 중 §5.4 · §5.5 · §5.13 · 409 · 502 · `event_log` · **WP-KOS 판정과 같은 본문**(K2 ~ K7) · 게이트 통과(기다리지 않음) | `cd procedure/back && uv run ruff check . && uv run pytest -q tests/test_resv_write.py` | 대기 |
| **WP-BE4** | **접수 묶음 · 실장 호출 · 귀가 완료**(게이트 뒤) — `service/reception.py`(§5.6 **두 갈래**(새 접수 = 예약 · 부도 + 신분 칸 / 이어 하기 = `RECEPTION` · 방 유무 무관 · 신분 조건 없음) · 0단계 KOS 단계로 갈래 다시 정함 · 끝 단계 이후 = 보내지 않고 ok · `identity_incomplete` · 붙은 방 고정 `room_locked` · 순서 · 건너뛰기 · 다시 읽기(2 · 4 · 5) 1초 × 5 · `room.id` 빈 값 판정 · 멈춤 + `step` · `kos_slow`) · `counselor-call` · `discharge`(수납 필요 막기 · KOS 400 → `kos_rejected`) · 성공 뒤 시술 현황 일정 조회 1회(`KosRuntime.tick()`) | §5.6 · §5.8 · §5.10 · §4.4 · §8 | backend | `procedure/back/app/{service/reception.py, service/reservations.py, api/reservations.py, kos/runtime.py}` · `tests/test_resv_reception.py`(새) | 단위 시험 중 §5.6(갈래 2 · 부도 접수 · 신분 칸 409 · 이어 하기 (a) 접수만 (b) 방 붙음 · 끝 단계 이후 ok · 순서 · 건너뛰기 4종 · 실패 단계 · 지연) · §5.8 · §5.10 · 바로 시술이면 시술 현황 스냅샷에 카드(가짜 KOS) · **K8 · K9 판정과 같은 본문** · 게이트 통과(기다리지 않음) · 기존 시험 전부(지금 178 + 새) | `cd procedure/back && uv run ruff check . && uv run pytest -q` | 대기 |
| **WP-FE1** | **헤더 · 경로 · 스케줄 표** — `AppHeader` 드롭다운 항목 하나 더함(시술 현황 뒤 · 「현황」 글자 그대로 · 부모 활성 = `/procedures/*` · `/reservations/*` — §6.1 · D-49) · `app/(main)/reservations/{page,live/page}.tsx` · 제목 줄(날짜 · [오늘] · 총 · 범례 7 · 동기화 글자) · 표(칸 · 축 · 회색 · 줄 간격 · 1시간 높이 · 지금 줄 · 자동 스크롤) · 카드(§6.3 · `flag-icons` · title = 국가 이름 · 부상태 칩 · 취소 흐림 · **「수납 필요」 Badge warning sm** — D-50) · 칸 머리 정원(구역별) · 「그룹 없음」 칸 · [+](`rows[].plusAllowed`) · 드래그(카드 구역 슬롯으로 미리 막기 · 낙관 표시 · 실패 원위치 + 토스트) · 10초 폴링 · 토스트 · `lib/types.ts` · `lib/api.ts` · `lib/session.ts`(`coordinator`) | §5.2 ~ §5.4 · §5.9(카드) · §6.1 ~ §6.3 · §6.7 · §6.8 #1 ~ #4 · #18 · #20 · #21 · #23 ~ #25 · #27 · #28 | frontend | `procedure/front/{components/common/AppHeader.tsx, app/(main)/reservations/**, components/reservations/**, lib/api.ts, lib/types.ts, lib/session.ts, package.json}` | 가짜 응답(`PROC_FAKE_BOARD=1`) 스크린샷: 표 전체 · 15/30/60 칸 · 구역 둘인 칸 머리 · 「그룹 없음」 칸 · 취소/부도 카드 · 수납 필요 카드 · 범례 · 드래그 중 금지 칸 · 드래그 403 토스트 · 헤더 드롭다운(「현황」 = 시술 현황). 시술 현황 화면 회귀 없음(스크린샷 1장) · `cc/` import 0 | `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build` | 대기 |
| **WP-FE2** | **오른쪽 패널 · 등록 모달** — 탭 둘(공지 목록 · 요청 빈 자리 / 원내 현황 필터 · **구역별 묶음** · 카드 · 금액 3칸) · 등록 모달(§6.5 — 구역 칸 · 검색 · 결과 표 · 페이지 · 이름 경고 · 신규/기존 · 칸 표 · 신규 구분 규칙 버튼 끄기 · `duplicated_visitor` 처리 · 등록 중 · 실패 줄) | §5.5 · §6.4 · §6.5 · §6.8 #5 ~ #9 · #26 · #29 | frontend | `procedure/front/components/reservations/**` · `lib/api.ts` · `lib/types.ts` | 가짜 응답 스크린샷: 공지 · 요청 빈 상태 · 원내 현황 필터 5 · 구역 묶음 둘 · 수납 필요 카드 · 등록 모달(구역 select)(검색 결과 · 이름 경고 · 신규 구분 꺼짐/켜짐 · 중복 안내) | 같음 | 대기 |
| **WP-FE3** | **예약 상세 모달** — §6.6 전부(기본 정보 · 「n / N 입력」 · 여권 영문 칸 · 저장 · 신분 확인(KOS 신분 칸 줄 + ccc 표시) · 유입 읽기 · 예약 메모 · 건강 · 특이사항 · 이전 방문 · 내원 현황 · 상담 카드 · 상담사 팝오버 · 단계 카드 · 정산 상자 · 딥링크 새 탭 · 바닥 줄 · [예약 취소] 고르기 · 시술실 팝오버(그 구역 · `roomLocked` 고정) · [접수 완료] 꺼짐 이유(신분 칸 · 방) · 단계 오류 표시) · 버튼은 `can.*` · `receiveMode` 로만 · 상세 다시 부르기 규칙(§6.7) | §5.6 ~ §5.14 · §6.6 · §6.7 · §6.8 #10 ~ #17 · #19 · #22 · #28 | frontend | `procedure/front/components/reservations/**` · `lib/api.ts` · `lib/types.ts` | 가짜 응답 스크린샷: 상태별 상세(예약 · 상담 대기 · 시술 진행 · 귀가 대기 수납 필요 · 귀가 완료 · 취소 · **부도(접수 가능)** · **이어 하기(방 고정)** · **신분 칸 빔(꺼짐 이유)**) · 시술실 팝오버(사용 중) · 상담사 팝오버 · 건강 확인 필요 · 이전 방문 펼침 · 조작 403 토스트 | 같음 · `grep -rn "can\.\(receive\|discharge\|cancel\)" procedure/front/components/reservations` ≥ 3 | 대기 |
| **WP-FIX1** | **E2E batch 1 수정**(2026-10-27 · 사용자 지적 23건 · 코드 `3c3c6ad` 위) — SPEC-005 0.3.0 부록 F 의 # 1 ~ 23 「SPEC-005 0.3.0」 칸 전부. back: 고객 검색 빈 조건 · 시간축 06–22 · `closedDay` · 등록 본문 셋 뺌(422) · `form.doctors` 뺌 · `snsTypes` · 접수 신분 조건 · `identity_incomplete` 없앰 · `route` 받음 · `PUT …/route` 없앰 · `POST …/consultation-add`(+ **데모 1회 시험** `changeFlowStep(CONSULTATION_WAITING)`) · 접수 단계별 측정(#14) · 상세 캐시 없음. front: DS 컨트롤 · 달력 · 칸 폭 · 카드 2줄 · 줄 경계 · 칸 머리 한 꼴 · 공지 높이 · 시각 뺌 · 자동 스크롤 · 이름 경고 뺌 · 진행 경로 라디오 · [+ 상담 추가] · 귀가 문구 뺌 · 성공 닫기 · 상세 5초 폴링 · 접수 낙관 표시 · 타이포 | §5.2 · §5.5 · §5.6 · §5.8 · §5.10 · §5.12 · §5.14 · §6 · §7.2 ~ §7.6 · §8 · 부록 F · D-51 ~ D-57 | backend ∥ frontend | `procedure/back/**` · `procedure/front/**`(batch 1 브리프 §2 몫) | 부록 F 23줄 처리 여부 줄마다(각자 몫) · #14 측정 수치 · #15 KOS 시험 결과(받음/안 받음 · 바뀐 값) · 경로 34(`PUT route` 없음 · `consultation-add` 있음) · 기존 시험 전부 · planner 가 SPEC 과 다른 곳을 보고로 고침 | `cd procedure/back && uv run ruff check . && uv run pytest -q` · `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build` | 진행 중(2026-10-27) |
| **WP-E2E** | **리뷰 + 코디 E2E(데모 지점)** — reviewer: SPEC-005 §1 ~ §8 ↔ 코드(부록 A 의 절 전부) · 기본값(§10 「planner 기본값」 줄)이 코드에 그대로인지 · KOS 본문 = WP-KOS 판정 · 시술 현황 회귀 · public 누출. FAIL 은 모아서 한 번에 수정 발주. 코디: 백엔드 커밋 뒤 **compose 다시 올리고** 데모 지점 → SPEC-005 §9 **#1 ~ #35**(브라우저 2개 · 시술 현황 탭) + SPEC-003 §9 회귀 #1 · #9 · #12 · #14 → 사용자 E2E(사용자 표면 · 피드백은 모아서 한 batch) | §9 | reviewer · 코디 · backend · frontend(수정) | `procedure/back/**` · `procedure/front/**` | 리뷰 PASS · 코디 §9 #1 ~ #41 통과(0.3.0 — #36 ~ #41 더함)(KOS 쪽 확인 칸 포함 — #13 · #17 「다른 칸 그대로」 · #21 KOS 웹 눈 확인 · #23 두 갈래 · #30 `COMPLETED` · #33 부도 접수 · #35 다른 구역) · #12 관찰 갈래 · #25 접수 뒤 상담사 지정 기록(OQ-760) · 남긴 데모 데이터 목록 사용자 통보 · 사용자 E2E 통과 | `cd procedure/back && uv run ruff check . && uv run pytest -q` · `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build` · `cd procedure && docker compose up --build` | 대기 |

## SPEC-005 절 → WP (빠진 절 0)

| SPEC-005 | WP |
|---|---|
| §1 범위 · §1.2 Out | 전부 · 「하지 않는 것」 |
| §0 0.2.0 변경 | 전부(각 WP 의 0.2.0 줄) |
| §2.1 폴더 · §2.2 실행 · §2.3 env | BE0 · BE1 · FE1(`flag-icons`) |
| §3.1 · §3.2 · §3.3 데이터 모델 | BE1(표 · 열) · BE2(`identity_check` · `questionnaire_history` 쓰기) |
| §3.4 코디 역할 · 수락 분기 | BE1(`service/actions.py`) · FE1(`session.ts`) |
| §4.1 ~ §4.3 조회 · 덮어쓰기 | BE1(목록 · 날짜별) · BE2(상세) · WP-KOS K1 |
| §4.4 쓰기 방식 · 오류 표 · `errorProperties` | BE1(`kos/client.py`) · BE3 · BE4 |
| §5.1 ~ §5.4 상태 · 칸 · 건수 · 정원 · 드래그 | BE1 · FE1 |
| §5.5 등록 규칙 | BE3 · FE2 · WP-KOS K2 |
| §5.6 접수 묶음 | BE4 · FE3 · WP-KOS K8 |
| §5.7 방 사용 중 | BE1 · BE2 · FE3 |
| §5.8 상담 카드 · 상담사 | BE2 · BE4 · FE3 · WP-KOS K5 |
| §5.9 수납 필요 · 금액 | BE1 · FE2 · FE3 |
| §5.10 귀가 완료 | BE4 · FE3 · WP-KOS K9 |
| §5.11 ~ §5.13 건강 · 신분 · 이전 방문 · 고객 정보 · 특이사항 | BE2 · BE3 · FE3 · WP-KOS K7 |
| §5.14 버튼 켜짐 | BE2 · FE3 |
| §6.1 ~ §6.3 경로 · 헤더 · 표 | FE1 |
| §6.4 · §6.5 패널 · 등록 모달 | FE2 |
| §6.6 상세 모달 | FE3 |
| §6.7 갱신 · 토스트 · §6.8 시안 차이 | FE1 ~ FE3 |
| §7 API · §7.6 경로 수 | BE0(모양) · BE1 ~ BE4(실제) |
| §8 KOS 반영 표 | WP-KOS · BE3 · BE4 |
| §9 E2E · 단위 시험 | WP-E2E · 각 BE 완료 조건 |
| §0 0.3.0 변경 · 부록 F(E2E batch 1) | WP-FIX1 |
| §10 열린 것 | 「열린 것」 |
| 부록 C · D · E(r1 처분 · U 반영 · WP-KOS 반영) | 리뷰(WP-E2E) 대조 기준 |

## 병렬

```text
WP-KOS(데모 실호출 · 리포트) ✓ ─────────── (게이트 통과 2026-10-26 · SPEC-005 0.2.0 반영)
WP-BE0(뼈대 · 가짜 · 첫 커밋) ─┬─ WP-BE1 ─ WP-BE2 ─────────────┬─ WP-BE3 ─ WP-BE4 ─┐
                                └─ WP-FE1 ─ WP-FE2 ─ WP-FE3 ──────────────────────────┴─ WP-E2E
```

- **WP-BE0 를 맨 먼저 커밋** — FE 는 그 가짜 응답으로 그린다(back 을 기다리지 않음). 응답 모양을 바꿔야 하면 SPEC-005 §7 을 먼저 고친다(코디 → planner) — 고정점
- **WP-BE3 · WP-BE4 는 게이트 뒤** — 게이트 통과(2026-10-26). 쓰기 본문은 WP-KOS 판정 모양을 따른다
- backend 한 워커가 BE0 → BE1 → BE2 → (게이트) → BE3 → BE4 를 차례로 · frontend 한 워커가 FE1 → FE2 → FE3. 두 워커가 같은 파일을 만지지 않는다(front 는 `procedure/back/**` 를 고치지 않는다 — 가짜 값이 모자라면 backend 에 요청)
- 숨은 의존: FE1 의 드래그 실패 토스트 · FE3 의 단계 오류는 가짜 모드 403 으로만 본다. 성공 경로 · 409 · `kos_slow` 는 WP-E2E 에서

## 하지 않는 것

- 앱(`procedure/app/`) · infra · 배포 — SPEC-005 §1.2 · D-02
- 시술 현황 규칙 · 화면 · 스냅샷 · SSE 바꾸기 — 헤더 항목 한 줄 · 공통 타입 · 경로 수 · 역할 추가 말고는 SPEC-003 그대로. 시술 현황판 2계층(OQ-743)도 안 함
- 본사 예약 요청 동작 · 취소 되돌리기 버튼 · KOS 소켓 · 공지 쓰기 · 휴무 칠하기 · 문진 제출 · 신분증 이미지 · 상담사 푸시 — SPEC-005 §1.2 · §10 「이번 판 밖」
- `kos_op` 대기열에 예약 조작을 넣기 — 동기(SPEC-005 §4.4 · OQ-705)
- 시안 파일 수정 · 시안 실명을 코드 · 가짜 값 · 스크린샷에 옮기기 — SPEC-005 머리말 「시안 실명 치환 규칙」

## 주의

- public 레포(코드 · 문서 · 시험 · 리포트 · 커밋 · 스크린샷) — KOS 키 · 토큰 · 비밀번호 · 계정 이메일 · 실명 · 연락처 · KOS id 값 · 실제 금액을 넣지 않는다. 가짜 값은 지어낸 것만
- **데모 지점에서만 쓴다**(D-06) — 운영 명동점 키 금지. WP-KOS · WP-E2E 가 만든 예약 · 고객은 지우지 않고 목록으로 남겨 사용자에게 알린다
- 워커는 사용자 포트(3600 · 8600 · 3700 · 8700)에 떠 있는 사용자 프로세스를 죽이지 않는다
- 백엔드 커밋 뒤 compose 를 다시 올리고 E2E(옛 코드가 떠 있는 채로 확인 금지)
- 외부 서비스 경로(KOS)는 **실물 호출이 완료 조건** — 가짜 KOS 시험만으로 done 하지 않는다(WP-KOS · WP-E2E)
- 같은 코드 브랜치에 시술 현황 되돌리기(WORK-006 · PR #6)가 E2E 중이다 — 그 코드 · 시험을 깨지 않는다(기존 시험 전부 통과가 매 BE WP 완료 조건)

## 열린 것 (2026-10-27 · r3)

SPEC-005 §10 이 정본(OQ-701 ~ OQ-760). WP-KOS 게이트 줄(OQ-728 · OQ-739 · OQ-753 ~ OQ-756)은 **닫혔다**. 이 문서가 기다리는 것만:

| 무엇 | 지금(기본값) | 근거 |
|---|---|---|
| 내부 API 정원 초과 거절 · 접수 뒤 단계 [실장 호출] | WP-E2E #12(관찰) · #25 에서 기록 | SPEC-005 OQ-760 · §8 |
| planner 기본값 줄 전부(OQ-701 나머지 · OQ-702 · OQ-704 ~ OQ-715 · OQ-717 · OQ-720 ~ OQ-727 · OQ-729 · OQ-731 ~ OQ-742 · OQ-752 · **OQ-757 작은 기본값 묶음 · OQ-758 구역 세부 · OQ-759 신분 칸 세부**) | 사용자 확인 대기 — 바뀌면 SPEC-005 개정 뒤 해당 WP | SPEC-005 §10 |
| batch 1 이 기다리는 것 — [+ 상담 추가] KOS 동작 · 고객 검색 빈 조건 · DS 컴포넌트 유무 · 접수 측정 수치 | WP-FIX1 보고 | SPEC-005 OQ-761 · OQ-762 · OQ-764 · OQ-767 |
| WP-KOS 가 남긴 데모 데이터(고객 1 · 일정 2 — 하나는 귀가 대기 + 수납 필요로 남음) 지울지 | 지우지 않음 · E2E #28 · #34 에 씀 · 사용자 판단 | `reservation-kos-probe-report.md` §5 · OQ-751 |
