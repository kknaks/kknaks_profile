# research-1 — F-3 시작 규칙 · F-7 수락 흐름 · F-6 차트 아이콘 표면 (read-only)

- 조사일: 2026-11-17 · 워커: day `researcher`
- 코드: `CENTURION_DAY` **`origin/dev` `4f8316a7`**(#253) — 아래 `dev:` 는 이 ref. `git show` / `git grep` 으로만 읽었다
- 스펙: mediness **`origin/main` `c3639503`** — `SPEC-002` = `products/day/20-spec/spec-002-procedure-board.md`, `SPEC-003` = `spec-003-mobile-app.md`, `기획 시술현황` = `products/day/00-baseline/planning/데이(CC)-기획안-·-시술-현황.md`, `기획 원내현황` = 같은 폴더 `…-원내-현황.md`
- KOS 앞 조사: `orchestration/work/_archive/day/day-procedure-board-2/research-har-room-chart-report.md`(이하 `HAR 리포트`)
- 결정하지 않는다. 마지막에 「정할 것」으로 모은다.

## 한눈에

| # | 핵심 사실 |
|---|---|
| F-3 | **호출 없이 [시작] 하는 길은 이미 있다** — 단, 그 시술의 KOS 집도의(`doctors[]`)에 원장 목록 사람이 있을 때만. 없으면 `no_doctor` 409. 호출된(수락 전) 줄은 `call_not_accepted` 409. **일괄 시작 엔드포인트는 없다**(단건만). [시작] 은 KOS 에 집도의를 쓰지 않는다(첫 시작의 `change-flow-step` + 시술 전 의사차트 글만). 「원장 호출이 필요 없는 시술」을 가를 칸은 **데이터에 없다** |
| F-3 | 스펙(SPEC-002 U-7 :252)은 「원장 없이 시작하는 길 없음(사용자 2026-11-09)」, 기획안(4-1 흐름 1 · 정책 1)은 「대기 줄 바로 시작 · 담당 원장 비어 있음」 — **스펙이 기획안보다 좁다**. 현장 요청은 기획안 쪽이다 |
| F-7 | **앱은 이미 F-7 그대로다**(원장 = 창 없이 본인 수락 · 그 밖 = 원장 골라 대리 수락 · iOS 알림 [수락]도 본인). **웹만 다르다** — 원장 계정도 늘 원장 고르기 팝오버를 거친다(기본 선택 = 지정 호출이면 지정 원장, 아니면 본인) |
| F-6 | 웹에서 아이콘이 그려지는 곳은 매크로 **`ui.chart_icons` 한 곳**(`dev:backend/day/templates/ui.html:258-260`)이고, 실제 화면 호출처는 **둘** — 판 카드의 **완료 줄**(`ui.html:280`)과 「시술 완료」 탭 카드(`board_parts.html:241`). **판 카드의 미완료 줄에는 아이콘이 없다**. **앱(Flutter)에는 차트 아이콘이 없다**. 아이콘은 버튼이 아니고 줄 전체가 차트를 연다 → 아이콘을 안 그려도 **작성 진입로는 사라지지 않는다** |

---

## F-3 시작 규칙

### Q1. 「시작」이 되려면 무엇이 먼저인가 · 거절 사유 전부 · 호출 없이 시작하는 경로

**판정 한 곳** = `BoardRules.start_block` (`dev:backend/day/services/board_rules.py:280-292`). 웹 · 앱이 같은 서비스(`board.start`, `dev:backend/day/services/board.py:807-815`)를 부르고 그 안에서 `_check(rules.start_block(v, t))` 한다.

| 순서 | 조건 | 409 코드 | 근거 |
|---|---|---|---|
| 1 | 귀가 대기 방문 | `visit_home` | `board_rules.py:285-286` |
| 2 | 줄이 진행중 · 완료 | `task_not_waiting` | `:287-289` |
| 3 | 유효 호출이 있는데 그 호출에서 이 줄이 수락 안 됨(= 「호출」 상태) | `call_not_accepted` | `:290-291` |
| 4 | 유효 호출이 없고 **KOS 집도의 중 원장 목록 사람(`kos_doctor`)이 없음** | `no_doctor` | `:292` · `kos_doctor` `:142-144` · `is_listed_doctor` `:138-140` |

- 그 앞에 서비스 공통 거절: 시술 없음 404(`board.py:810-812`), 권한 `board` edit 없음 403(라우터).
- 「원장 목록」 = 직무 태그 `doctor` + `is_active` + `is_system_account=false` (`dev:backend/day/queries/board.py:337-341`).
- 즉 **전제는 「원장 호출 → 수락」이 아니라 「담당의(원장)가 정해져 있음」**이다. 호출이 있으면 수락이 담당의를, 호출이 없으면 KOS 집도의가 담당의를 준다.

**웹 · 앱 엔드포인트**

| 쪽 | 경로 | 권한 | 근거 |
|---|---|---|---|
| 웹 | `POST /board/tasks/{task_id}/start` (`TASK_ACTIONS` 디스패치) | `board` edit | `dev:backend/day/routers/board.py:654-666` |
| 앱 | `POST /api/tasks/{task_id}/{action}` | `board` edit | `dev:backend/day/routers/api/board.py:278` |

**호출 없이 시작하는 경로 — 있다(단건)**

- 웹 줄 버튼: `t.state in ("ready_wait","accepted") and t.canStart` 일 때만 [시작](`dev:backend/day/templates/partials/board_parts.html:96-97`). `canStart` = `start_block(...) is None` (`board_rules.py:753`). 준비중 + KOS 집도의 있음이면 [시작] 이 보인다 = SPEC-002 S-4 「호출 없이 담당의가 바로 시작」(:391-393).
- 앱: 진행중 · 완료가 아니면 [시작] 을 늘 그리고 `!t.canStart` 면 눌리지 않게(`dev:app/lib/ui/room_screen.dart:504-511`).
- 서비스: 호출 없는 시작이면 시술 전 의사차트를 [시작] 때 보낸다(`board.py:829-834` · 실제 원장 = `kos_doctor`).
- **여러 건(일괄) 시작 — 없다.** 웹 · 앱 라우터에 시작은 단건 `task_id` 경로뿐이다(위 표). 판 액션바의 일괄 조작은 「의사 호출」 하나다(Q4).

### Q2. 호출 · 수락 · 시작이 KOS 로 보내는 것 · 집도의 필수 여부

KOS 쓰기 표 = `dev:backend/day/emr/kos/writes.py:10-29`(경로 상수 `:46-55`). 보내는 토큰 = 누른 사람(`board.py:284` `sender_staff_id` · SPEC-002 규칙 24 :860).

| 조작 | KOS 경로(끝 이름) | 본문 | 확인 조건 | 근거 |
|---|---|---|---|---|
| 호출 ① | `change-tasks-room` | `scheduleId · sequences · roomId` — 줄 방이 카드 방과 다를 때만 | 작업 방 = 그 방 | `board.py:543-555` · `writes.py:112-118` |
| 호출 ② | `change-tasks-assignees` | `assigneeIds = [병원 시스템 계정]` | 담당자에 시스템 계정 | `board.py:556-557` · `writes.py:119-127` |
| 호출 ③ | `call-tasks-doctors` | `scheduleId · sequences` (대상 원장 id 없음) | 작업 `status = waiting`(다시 호출은 `waiting`/`ready`) | `board.py:558-563` · `writes.py:128-144` |
| 수락 | `change-tasks-doctors` | `doctorIds = [수락한 원장 KOS id]` | `doctors_contain` + **`status = ready`** | `board.py:736-750` · `writes.py:145-153` |
| 수락(시술 전 의사차트 있으면) | `change-flow-tasks-doctor-memo` | 글 전체 | — | `board.py:730-735 · 792-801` |
| [시작] — 그 고객 첫 시작만 | `change-flow-step` | `{id, step: PROCEDURE}` (방문 단위) | 일정 `flowStep = PROCEDURE` | `board.py:835-851` · `writes.py:164-169` |
| [시작] — 호출 없는 시작 + 시술 전 의사차트 있으면 | `change-flow-tasks-doctor-memo` | 글 전체 | — | `board.py:829-848` |
| [시작] — 첫 시작 아님 | **없음**(DAY 만 · `started_at`) | — | — | SPEC-002 KOS 쓰기 표 :774 |

- **[시작] 은 KOS 에 시술(작업) 단위 「시작」도, 집도의도 보내지 않는다.** KOS 에 「작업 시작」 명령 자체가 없다(KOS 작업 상태 = `not_started · waiting · ready · done · canceled`, `dev:backend/day/enums/task.py:9-14`; 시작 시각은 「KOS 에 없음」 — HAR 리포트 :87).
- **KOS 쪽에서 집도의가 [시작] 의 필수인가 — 코드상으로는 아니다.** DAY 가 보내는 [시작] 쓰기(`change-flow-step`)는 일정 단위이고 집도의 칸이 없다. `no_doctor` 거절은 **DAY 자체 규칙**(cc D-30 계승 · SPEC-002 U-7 :244 · 규칙 10 :837)이다.
- **확인 안 됨**: ⓐ 집도의가 빈 작업이 있는 일정에 `change-flow-step(PROCEDURE)` 를 보내면 KOS 가 받는지(실호출 기록 없음 — HAR 은 집도의가 있는 흐름 `의사호출_2.har` 뿐) ⓑ 집도의 없이 진행 · `change-tasks-complete` 된 작업을 KOS 화면 · 정산이 어떻게 다루는지 ⓒ 호출 ③ 없이(KOS `status` 가 `not_started` 인 채) [종료] `change-tasks-complete` 를 보내면 받는지 — 지금은 호출 없는 시작도 KOS 집도의가 이미 있는 줄만이라 이 조합을 실물로 본 기록이 없다.
- 참고(HAR 리포트 :104 · :117): 차트 메모는 담당자 · 집도의 없이도 200 이었으나 「빈 작업」 기준은 확인 안 됨.

### Q3. 「원장 호출이 필요 없는 시술」을 가를 근거가 데이터에 있나 — **없음**

- 작업 칸(`dev:backend/day/models/task.py:57-95`): `kind`(`procedure`/`etc`) · `title` · `option_title` · `medical_service_title` · 단위 · 회차 · `medicines` · `payment_required` · `anesthesia_type` · 메모 3종 · 방 · 시각들. **호출 필요/불필요 칸 없음.**
- KOS 매핑(`dev:backend/day/emr/kos/mapper.py:470-517`): `procedureConfiguration`(옵션 · 진료항목 · 단위 · 회차 · 약물) · `paymentRequired` · `anesthesiaType` · `doctors` · `calledDoctors` 등 — **그런 플래그를 읽지 않는다.** KOS 원본에 그런 키가 있는지는 **확인 안 됨**(우리 매퍼가 안 읽는 키는 이번에 보지 않았다).
- 카탈로그 테이블 없음(`dev:backend/day/models/` = customer · hospital · misc · room · staff · task · visit). 연결 설정(`crm_connection.config`)에 시술별 설정 키 없음(grep `no_call|call_required|skip_call|direct_start|…` 0건).
- **간접 근거 하나**: KOS 작업 `doctors[]` 가 이미 차 있으면 지금도 호출 없이 [시작] 이 켜진다(Q1-4). 이 값을 누가 · 언제 채우는지(예약 · 상담 · 오더 단계)는 **확인 안 됨**.

### Q4. 액션바 「의사 호출 · N건」 · 일괄 호출 경로 · 섞일 때

| 층 | 무엇 | 근거 |
|---|---|---|
| 템플릿 | 카드마다 액션바 1개 · 버튼 하나 「의사 호출 · `<span data-day-count>`건」 → 호출 팝오버(`call-{visitId}`) | `board_parts.html:175-180` |
| 템플릿 | 전체 선택 체크 = `ui.check_all(visitId, disabled=not (card.canCall and EDIT))` | `board_parts.html:171` · `ui.html:156-158` |
| 템플릿 | 줄 체크 = 상태 `wait`·`called` 이고 `pickable` 일 때만 켜짐, `form="call-{visitId}-form"` 으로 호출 창 form 에 딸림 | `board_parts.html:72` · `ui.html:286-288` |
| 서버 값 | `pickable` = 귀가 대기 아님 + 상태 `ready_wait`·`called` | `board_rules.py:185-191` · `canCall` = 하나라도 pickable `:836` |
| JS | **N = 그 카드 그룹에서 체크된 켜진 체크박스 수**(꺼진 것 제외) · 0 이면 바 내려감 | `dev:backend/day/static/day.js:192-207` |
| 호출 창 | `ui.doctor_call_modal(mode="call")` — 받는 칸 `taskIds,target,doctorStaffId` | `board_parts.html:39-47` · `board_regions.html:51` |
| 라우터 | 웹 `POST /board/visits/{id}/calls` · 앱 `POST /api/visits/{id}/calls` — 둘 다 `board` edit | `routers/board.py:474-485` · `routers/api/board.py:183-193` |
| 서비스 | `board.call` — 고른 줄 전부가 `pickable` 이어야(아니면 `task_not_pickable`) · 호출 1건 + 줄 N개 · KOS 3단계 | `board.py:581-636` · `board_rules.py:222-227` |

- **일괄 시작 엔드포인트: 없음.** (Q1)
- **선택에 호출 필요/불필요가 섞이면**: 지금은 그런 구분이 없어(Q3) 고른 줄 **전부가 같은 호출 하나**로 간다. 기획안은 「원장 없이 할 시술이 섞였으면 원장마다 줄을 골라 따로 부른다」(`기획 시술현황` 3-1 흐름 2 :395)로 사람이 나눠 고르는 전제.
- 「바로 시작 · N건」을 같은 N 으로 붙이면: 지금 체크 대상에는 **「호출」(수락 전) 줄도 들어 있다** — 그 줄은 `call_not_accepted` 로 막힌다. 준비중 줄도 KOS 집도의가 없으면 `no_doctor`. 즉 **지금 규칙 그대로면 N 건 중 일부만 시작될 수 있다.**
- 앱에는 판 카드 체크 · 액션바가 없다(룸 상세 [의사 호출] 시트 — `room_screen.dart:427-446`). 앱에 「바로 시작 · N건」을 둘지는 범위 밖(정할 것).

### Q5. 스펙 · 기획안의 시작 · 호출 · 수락 순서 — 그리고 어긋난 곳

| 문서 | 자리 | 내용 |
|---|---|---|
| SPEC-002 | U-7 :244 | [시작] — 호출한 시술은 유효 호출 수락 뒤, 호출 안 한 시술은 **담당의가 있으면 호출 없이**(U1 · cc D-30) |
| SPEC-002 | U-7 :252 | **「[시작]은 지금 조건 그대로(수락 → [시작] · 원장 없이 시작하는 길 없음 · 사용자 2026-11-09)」** |
| SPEC-002 | U-3 :207 · :208 | 줄 버튼: 준비중 · 담당의 있음 → [시작] / 호출 → 버튼 없음 · 「원장 없이 시작하는 길은 없다 U-7」 |
| SPEC-002 | 규칙 10 :837 · 규칙 11 :838 | [시작] 켜짐 조건 · 시작 때 쓰기 |
| SPEC-002 | 케이스 매트릭스 :678-680 · 검사 순서 :694 · 글자 :718-719 | `task_not_waiting` · `call_not_accepted` · `no_doctor` |
| SPEC-002 | S-4 :391-393 | 호출 없이 담당의가 바로 시작(KOS `doctors[]` 있는 준비중) |
| SPEC-002 | 「기획안에서 안 하는 것」 표 :113 | 기획 3-1 흐름 5 · 4-1 흐름 2b · 2c(호출 중 줄 수락 없이 시작 · 전체 호출이면 원장 고름) = **안 함** |
| SPEC-002 | 용어 :454 | 담당의 = KOS 작업 집도의(`visit_task_staff.role = doctor`) 중 원장 목록 직원 |
| 기획 시술현황 | 4-1 흐름 1 :507 | **「대기 줄 「시작」을 누르면 확인 창이나 원장 목록 없이 그 줄이 진행 중이 된다」** |
| 기획 시술현황 | 4-1 :516 · 정책 1 :561 | 「1은 **원장 호출 없이 시작하는 갈래**」 · 「대기 줄을 바로 시작하면 [담당 원장은] **비어 있다**」 |
| 기획 시술현황 | 4-1 흐름 2a~2c :508-510 · 3-2 흐름 4 :452 | 수락 줄 / 지정 호출 중 줄(부른 원장으로) / 전체 호출 중 줄(원장 목록에서 고름) 시작 |
| 기획 원내현황 | :137 | 「원장 없이 시작한 줄은 시술 이름만 보인다」 |

**어긋난 곳**

1. **기획 4-1 흐름 1 · 정책 1(원장 없이 바로 시작)** ↔ **SPEC-002 U-7 :252 · 코드 `no_doctor`**. 스펙의 「기획안에서 안 하는 것」 표(:113)는 2b · 2c 만 적었고 **흐름 1(원장 없이 대기 줄 시작)을 뺀 기록은 표에 없다** — 대신 U-7 :252 에 「사용자 2026-11-09」로 남아 있다. F-3 현장 요청은 기획 흐름 1 쪽이다.
2. 스펙 · 코드는 서로 맞다(검사 순서 :694 = `board_rules.py:280-292`).

---

## F-7 수락 흐름

### Q6. 「수락」 뒤 집도의가 정해지는 경로

**서버(웹 · 앱 공통)** — `board.accept(call_id, doctor_staff_id)` (`dev:backend/day/services/board.py:694-751`)

- 집도의 = **요청 본문 `doctorStaffId`**(필수) — 누른 계정도, 호출 대상도 아니다. 서버는 `doctorStaffId` 가 원장 목록에 있는지만 본다(`:707-708` `doctor_not_listed`). **지정 호출 대상과 같은지는 보지 않는다**(SPEC-003 :336 에 사실로 적힘).
- 기록: `doctor_call_accept.doctor_staff_id = doctorStaffId`(`:710-715`) · `event_log.actor = doctorStaffId`(`:716-728` — 「누른 사람은 남기지 않는다」 규칙 9).
- 판정: `accept_block` = `visit_home` → `call_closed` → `call_already_accepted` → `nothing_to_accept` (`board_rules.py:258-272`).

**웹** — 인박스 「수락 대기」 탭 카드 [수락](`board_parts.html:216-230`, `ACCEPT` 일 때만 :226-228) → **원장 고르기 팝오버**(`ui.doctor_call_modal` mode `accept`, 머리 「수락할 원장」 · 「모든 의사」 줄 없음 — `ui.html:378 · 437 · 456`) → 원장 하나 고르고 [수락] → `POST /board/calls/{id}/accept doctorStaffId=…`(`routers/board.py:501-512`).

- 팝오버 기본 선택(`board_regions.html:55-60`): **지정 호출이면 지정 원장 · 아니면 로그인 계정이 원장 목록에 있으면 본인 · 그 밖 없음**. → 원장 계정도 **늘 팝오버를 거치고**, 다른 원장 지정 호출이면 기본값이 **그 지정 원장**이다(본인 아님).
- 판 카드 시술 줄에는 [수락] 이 없다(`board_parts.html:91-93` · SPEC-002 U-3 :207).

**앱** — `dev:app/lib/ui/accept.dart:13-54` (목록 카드 `board_screen.dart:501-508` · 룸 상세 `room_screen.dart:255-277` 공통)

- `snap.isDoctor(me.staffId)`(스냅샷 `doctors[]` 에 로그인 staff 가 있음 — `dev:app/lib/model/board.dart:349`)면 버튼 「수락 · N건」 → **창 없이 `doctorStaffId = 로그인 staff.id`**(`accept.dart:34-37`). 다른 원장 지정 호출이어도 본인으로(주석 OQ-A28).
- 아니면 「원장 골라 수락 · N건」 → 원장 고르기 드로어(기본 = 지정 호출이면 지정 원장) → 고른 원장(`:39-53`).
- iOS 알림 [수락](카테고리 `CALL` · 액션 `ACCEPT`) = 네이티브가 `POST /api/calls/{id}/accept {doctorStaffId: 세션 staff_id}`(`dev:app/ios/Runner/AppDelegate.swift:18-21 · 36-38 · 139`). 카테고리는 `board.accept` edit 가진 직원 기기에만(`dev:backend/day/services/notifications.py:413-437 · 468-493`).
- 스펙: SPEC-003 U-6 :325-336 이 이 분기를 계약으로 둔다(사용자 2026-11-10 「원장을 다시 고르게 하지 않는다」). SPEC-002 U-6 :236-240 은 웹을 「원장 고르기 창 · 기본 선택 = 지정 원장 / 본인」으로 둔다.

→ **F-7 은 앱엔 이미 있고 웹에만 없다.** 웹을 앱(SPEC-003 U-6)과 같게 맞추는 일이다.

### Q7. 로그인 계정이 원장인지 가르는 기준 — 있다

- 서버: `BStaff.is_doctor` = 직무 태그 `doctor` ∈ `JobRole.tags` **그리고** `is_active` **그리고** `not is_system_account`(`dev:backend/day/queries/board.py:337-341`). 스냅샷 `doctors[]` 는 이 사람들(`board_rules.py:175-182`). 알림 쪽 같은 판정 `notifications.py:206-213`.
- 로그인 계정 ↔ 직원: 세션이 `CurrentSession.staff_id` 를 들고 있다(웹 템플릿 `session.staff_id` — `board_regions.html:56`, 앱 `/me` 의 `staffId`). 즉 **계정 = 직원 1행**이고 따로 「계정 ↔ 원장」 연결 테이블은 없다 — 그 직원이 원장 목록(`doctors[]`)에 있으면 원장이다.
- 웹에서도 이미 `me_listed = snapshot.doctors|selectattr("staffId","equalto",me)` 로 본인 원장 여부를 계산한다(`board_regions.html:57`) → **「로그인 계정 = 집도의」를 웹 템플릿 · 서버 값만으로 바로 정할 수 있다**(새 칸 불필요).
- 주의: 원장 목록은 1차에 KOS 「마취용」 · 공용 계정도 태그 `doctor` 면 들어간다(SPEC-002 규칙 19 :855). 그런 공용 계정으로 로그인한 웹 PC(의국 공용 PC 등)라면 「본인 즉시 수락」이 그 공용 계정을 집도의로 남긴다 — **실제 병원에 그런 계정이 있는지는 확인 안 됨**.

### Q8. 수락이 KOS 로 보내는 값 · 대리 / 본인 구분

- `change-tasks-doctors {scheduleId, sequences, doctorIds: [수락한 원장 KOS id]}` + 시술 전 의사차트 글(Q2 표). 원장 KOS id 를 못 찾으면 `Skipped("accept_doctor")`(`board.py:737-749`).
- 토큰 = **누른 사람**(`sender_staff_id = current.staff_id` `board.py:284` · SPEC-002 규칙 9 :836 · 규칙 24 :860). 원장 본인이면 원장 토큰, 간호사 대리면 간호사 토큰.
- **KOS 에서 대리 / 본인이 구분되는가**: 요청 본문은 같다(`doctorIds` 만). 다른 것은 보내는 토큰뿐. KOS 가 토큰 주인을 이력 등에 남겨 구분하는지는 **확인 안 됨**. KOS 는 대리 수락을 받는다(cc D-27 실호출 「관리자 계정이 원장 대신 수락 200」 — SPEC-002 :836 인용).
- DAY 에서도 구분되지 않는다 — 수락 행 · event 에 누른 사람이 없다(규칙 9). 남는 흔적은 `external_outbox.sender_staff_id` 뿐(토큰 고르기 전용).

### Q9. 권한 — `board.accept` edit 를 누가 갖나 · 원장이 지금 누를 수 있나

- 기본 권한(`dev:backend/day/services/default_permissions.py:36-63`): 직무 이름 표 → 태그 `nurse` · `skincare` · **`doctor`** · `admin` 중 하나 → `board` edit + `board.accept` edit. 이름 표 예외: 경영지원 · 마케팅 · CS팀 · 상담총괄실장 = 보기, 마취과 = 전부. **덮어쓰지 않음**(사람이 고친 행 유지 · `:19-20`).
- → **태그 `doctor` 직무는 기본으로 수락 가능.** 웹 [수락] 버튼은 `board.accept` edit(또는 전체 권한 계정)일 때만(`board_parts.html:17-22 · 226`), 서버도 같은 키(`routers/board.py:508` · `routers/api/board.py:217`).
- 특정 병원에서 원장 직무 권한 행을 사람이 바꿨는지는 **확인 안 됨**(DB 미조회 · 범위 밖).

---

## F-6 차트 아이콘 표면

### Q10. 아이콘이 나오는 곳 전부 (grep: `chart_icons` · `square-pen` · `stethoscope` · `day-ic--disabled` · `day-proc__icons` · `nurse_on`/`doctor_on` · `assigneeNote`/`doctorNote` · `간호관리차트 없음` — `backend/` · `app/` 전체)

**그리는 곳**

| # | 화면 | 자리 | 파일:줄 | 판정 값 | 판정 |
|---|---|---|---|---|---|
| 1 | (공통) 매크로 | `ui.chart_icons(nurse_on, doctor_on)` — 간호 `square-pen` · 의사 `stethoscope`, on = `brand`, off = `disabled`(= `svg.day-ic.day-ic--disabled`) · aria-label 「간호관리차트 있음/없음」 · 「의사차트 있음/없음」 | `dev:backend/day/templates/ui.html:257-260` | 인자 | **웹만** — 고칠 곳의 중심 |
| 2 | 시술 현황 판 카드 — **완료 줄**(`day-proc-list--done`) | `proc_row` 완료 갈래 | `ui.html:280` ← 값 `board_parts.html:79`(`nurse_on: t.assigneeNote, doctor_on: t.doctorNote`) · 완료 줄 목록 `board_parts.html:173` | 스냅샷 `cards[].tasks[].assigneeNote/doctorNote` | 웹만 |
| 3 | 시술 현황 판 카드 — 미완료 줄(준비중 · 호출 · 수락 · 진행중) | `proc_row` 그 밖 갈래 — **아이콘 없음** | `ui.html:285-302`(:290 이름만) | — | 지금도 안 그림 · 고칠 것 없음 |
| 4 | 인박스 「시술 완료」 탭 카드(E28 · E29 · E30) | 시술 링크 줄 `day-linkrow` 안 | `dev:backend/day/templates/partials/board_parts.html:240-242` ← 목록 `board_done_list.html` · `board_regions.html:40` | 스냅샷 `doneTab[].tasks[].assigneeNote/doctorNote` | 웹만 |
| 5 | 개발용 키트 페이지(`/dev/kit…`) | 견본 | `dev:backend/day/templates/partials/kit_page.html:259-260 · 487-488` · `dev:backend/day/routers/kit.py:97-98 · 134-135` · `routers/kit_board.py:184 · 196` | 고정 값 | 웹만(견본 — 현장 화면 아님 · 맞출지 정할 것) |
| 6 | CSS | `.day-ic--disabled` · `.day-proc__icons` | `dev:backend/day/styles/app.css:197 · 474` · 빌드본 `dev:backend/day/static/day.css:292-294 · 1581` | — | `day-ic--disabled` 는 다른 아이콘도 쓸 수 있는 공용 tone — 지우지 말고 호출만 바꾸는 쪽이 안전 |
| 7 | 인박스 「수락 대기」 카드의 `stethoscope` | 원장 줄 머리 아이콘(차트 아님) | `board_parts.html:223` | — | **대상 아님**(같은 그림이지만 차트 아이콘이 아니다) |

**그리지 않는 곳(확인함)**

| 화면 | 근거 |
|---|---|
| 차트 모달(`board_chart.html` · `board_chart_parts.html` · `board_chart_saved.html`) | 아이콘은 닫기 `x` 하나뿐(`board_chart_parts.html:64`) |
| 인박스 「확인 필요」 · 「수락 대기」 카드 | `board_parts.html:195-230` — 차트 아이콘 없음 |
| JS(`day.js`) | 차트 아이콘을 만들거나 켜고 끄는 코드 없음(grep 0) — 서버 렌더 그대로 |
| **앱(Flutter) 전부** | `app/lib` 에 차트 아이콘 위젯 없음. `assigneeNote/doctorNote` 는 모델(`model/board.dart:84-85 · 115-116 · 268-291`)과 읽기 전용 차트 시트 글(`ui/chart_sheet.dart:9-11 · 60-61`)에만. 앱 「시술 완료」 탭은 1차에서 뺐다(SPEC-003 :222) — `doneTab` 은 파싱만 · `board_controller.dart:129` 에서 쓰는 곳은 차트 아이콘 아님 |
| 원내 현황 · 요청함 화면 | **dev 코드에 그 화면이 없다**(`routers/` = board · kit · kit_board · login · public_pages · api/*). 기획안만 있음 → 지금 고칠 곳 없음 · 앞으로 만들 때 같은 규칙을 넣을지 정할 것 |

**API 필드**: 스냅샷 `cards[].tasks[]` 와 `doneTab[].tasks[]` 의 `assigneeNote` · `doctorNote`(`board_rules.py:749-750 · 904-911`). 웹 · 앱이 같이 받는다. **필드는 그대로 두면 된다**(아이콘 표시는 템플릿 판단).

**테스트 단언(영향)**

| 파일:줄 | 무엇 | 영향 |
|---|---|---|
| `dev:backend/tests/architecture/test_screen_copy.py:126-127` | 화면 글자 허용표 「있음」 · 「없음」 = 차트 아이콘 aria-label | 미작성을 안 그리면 「없음」 글자가 화면에서 빠진다 — 이 표가 「쓰이지 않는 항목」을 거르는지 **확인 안 됨**(지울지 정할 것) |
| `dev:backend/tests/day/web/test_board_page.py:723` | 「시술 완료」 탭 견본 `assigneeNote: None, doctorNote: "20u"` | 그 둘레 단언이 아이콘 · aria-label 을 보는지 이번에 줄 단위로 안 열어 봄 — **확인 안 됨** |
| 그 밖 | `day-ic--disabled` · `간호관리차트 없음` · `chart_icons` 를 직접 단언하는 테스트 — grep 0 | — |
| 앱 테스트 | `app/test/capture/visual_capture_test.dart:144-155` · `app/test/support/fixtures.dart:167-168` — 값만 넣음 · 아이콘 단언 없음 | 영향 없음 |

### Q11. 「작성됨」 판정 원천

- 웹 · 앱 같은 원천 = **스냅샷 `assigneeNote` · `doctorNote` = `visit_task.assignee_note` · `doctor_note` 값의 참/거짓**(Jinja 진리값 — `None`·`""` = 미작성). `board_parts.html:79 · 241` · `board_rules.py:749-750 · 908-909`.
- 이 칸은 **KOS 사본**이다 — sync 가 KOS `assigneeMemo` · `doctorMemo` 로 덮는다(`mapper.py:506-507` · `dev:backend/day/emr/sync.py:1210-1211 · 1321`). DAY 저장도 이 칸을 바꾼다(아래).
- **어긋나는 자리(조용히 깨질 수 있음)**: 시술 전(준비중 · 호출) **의사차트**는 DAY 이력(`visit_task_chart_log`)에만 저장되고 `doctor_note` 는 안 바뀐다 — 수락 · [시작] 때 비로소 `doctor_note` 로 간다(`board.py:1190-1195` 독스트링 · `_prestart_doctor_chart` `:754-789` · SPEC-002 :346 · :437). 그래서 **시술 전에 의사차트를 써 둔 줄은 지금 판정으로는 「의사 미작성」**이다. 다만 지금 아이콘은 완료 줄 · 「시술 완료」 탭에만 그려지고, 완료된 줄은 수락 · 시작을 거쳐 `doctor_note` 가 채워졌을 것이라 **현재 표면에서는 드러나지 않는다**. 미완료 줄에도 아이콘을 넣기로 하면 이 차이가 바로 보인다. (단, 마지막 이력이 KOS 저장이면 미리 쓴 글은 보내지 않는다 — `board.py:762-767`.)
- 간호관리차트는 저장 즉시 `assignee_note` 를 바꾼다(`board.py:1253-1259`) — 이력과 칸이 같이 간다.
- 공백만 있는 글: 저장 때 `chart_body` 로 정리(`board.py:1159-1161`). KOS 에서 온 공백 글의 처리는 `mapper.text()` 를 따르며 「빈 글자 = 없음」(`tests/day/emr/test_kos_board_contract.py:68` 주석).

### Q12. 미작성 아이콘이 작성 진입로인가 — 아이콘을 없애면 진입로가 사라지는 곳

**없다(웹 · 앱 모두).**

| 쪽 | 아이콘 자리 | 차트를 여는 것 | 근거 |
|---|---|---|---|
| 웹 판 카드 완료 줄 | 아이콘은 줄 안의 장식 svg(버튼 아님) | **줄 전체**의 `data-day-row-get="/board/visits/{id}/chart?sec={시술}"` → 차트 모달(작성 가능 · 개정 ⑯) | `board_parts.html:80` · `ui.html:277 · 280` |
| 웹 「시술 완료」 탭 | 아이콘은 `<button class="day-linkrow">` 안의 장식 | **그 줄 버튼 전체** `hx-get=…/chart?sec=…` | `board_parts.html:241` |
| 웹 판 카드 미완료 줄 | 아이콘 없음 | 줄 전체(위와 같음) | `board_parts.html:80` |
| 앱 | 아이콘 없음 | 시술 카드 탭 → `showChart`(읽기 전용 · 작성 없음) | `room_screen.dart:523-527` · `chart_sheet.dart:1` |

- 아이콘 자체에 `hx-*` · `data-*` · 링크가 붙은 곳은 없다(`ui.html:259` 의 svg 는 `role="img" aria-label` 뿐). → **미작성 아이콘을 안 그려도 작성 진입로는 그대로**다.
- 스펙 문구는 「여는 곳 = 시술 이름 · 「시술 완료」 탭 카드의 시술 줄 · **차트 아이콘**」(SPEC-002 :170 · :337 · :341)이라 아이콘도 진입로로 적혀 있다. 코드상 아이콘은 줄 버튼 안에 있어 같은 동작이지만, **스펙 문장은 고쳐야 할 수 있다**(정할 것).
- 접근성: 지금 미작성 아이콘이 「간호관리차트 없음」을 읽어 준다. 안 그리면 스크린리더에는 「작성됨」만 들린다 — 의도와 맞는지 정할 것.

### F-6 항목별 판정

| 항목 | 판정 |
|---|---|
| `ui.chart_icons` 매크로(off 아이콘 안 그리기) | **웹만** — 한 곳 고치면 #2 · #4 · #5 가 같이 바뀐다 |
| 판 카드 완료 줄 · 「시술 완료」 탭 | 웹만(매크로를 따라감) |
| 판 카드 미완료 줄 | 지금 아이콘 없음 — 「아이콘이 나오는 모든 영역」이 미완료 줄을 포함하는지는 정할 것(포함이면 `ui.html:290` 에 추가 · Q11 시술 전 의사차트 차이 생김) |
| 스냅샷 · API 필드 | **API 같이 고칠 것 없음** |
| 앱(Flutter) | **앱 수정 불필요**(아이콘 없음). 앱 「시술 완료」 탭 · 줄 아이콘을 새로 넣을지는 범위 밖 |
| 테스트 | 화면 글자 허용표 「없음」(`test_screen_copy.py:127`) · `test_board_page.py:723` 둘레 확인 |
| 스펙 | SPEC-002 E30 문구(:165 · :170 · :318 · :337 · :341)에 「작성된 차트만」 반영 필요(문서 작업) |

---

## 고칠 방향 후보 (결정 아님)

**F-3**

- A. **지금 규칙 안에서 버튼만** — 「바로 시작 · N건」 = 고른 줄 중 `canStart` 인 줄만 시작(준비중 + KOS 집도의 있음 · 수락 줄). 서버 규칙 변경 없음 · 일괄 시작 엔드포인트(또는 웹이 단건을 N번) 추가. 현장이 원하는 「원장 없이」는 **안 풀린다**(집도의 없는 줄은 `no_doctor`).
- B. **기획 4-1 흐름 1 로 넓힘** — 준비중 줄은 담당의 없어도 시작(`no_doctor` 제거 또는 조건부) · 담당 원장 비어 있음 · 표시 「원장 없이」(기획 원내현황 :137). SPEC-002 U-7 :252 · 규칙 10 · 케이스 매트릭스 · S-4 · 화면 글자(「{원장} · 진행」 → 원장 없음 표시) · 원장 상태(`doctor_status`) · 앱 `canStart` 표시 · 의사차트 집도의 처음 값까지 연쇄. KOS 쪽 집도의 빈 작업의 진행 · 완료 쓰기는 **확인 안 됨** → 데모 지점 실물 확인 필요.
- C. **시술별로 가름** — 「호출 불필요 시술」 목록을 새로 둠(설정 · 시술명 · KOS 진료항목 등). 지금 데이터에 근거 칸이 없어(Q3) 새 칸 · 원천 결정이 먼저.
- 호출 중(수락 전) 줄을 「바로 시작」에 넣을지(기획 2b · 2c — 스펙 :113 에서 「안 함」)는 B · C 와 별개로 정할 것.

**F-7**

- 웹 수락 버튼을 앱(SPEC-003 U-6)처럼 분기 — 로그인 staff 가 `snapshot.doctors` 에 있으면 팝오버 없이 `hx-post …/accept doctorStaffId=본인` · 아니면 지금 팝오버. 서버 · API · 앱 수정 없음(템플릿 `board_parts.html:226-228` · `board_regions.html:55-60` 중심, 버튼 글자 「수락」 유지 여부는 정할 것). 테스트 `test_board_page.py:98 · 138-148 · 281` 영향.

**F-6**

- `ui.chart_icons` 에서 off 아이콘을 그리지 않게(빈 차트면 `day-proc__icons` 칸 자체를 생략할지 포함). 호출처 · API · 앱 변경 없음.

## 정할 것

1. **F-3 시작 규칙의 폭** — A(지금 규칙 그대로 · 버튼만) / B(준비중은 원장 없이도 시작 — 기획 4-1 흐름 1) / C(시술별 호출 불필요 목록). B · C 면 SPEC-002 U-7 :252 「원장 없이 시작하는 길 없음(사용자 2026-11-09)」을 뒤집는 결정이다.
2. F-3 — 「바로 시작 · N건」의 N: 지금 체크 N(준비중 + 호출 줄)과 같게 둘지, 시작 가능한 줄 수로 따로 셀지. 일부만 시작될 때(나머지 `no_doctor` · `call_not_accepted`) 화면 처리.
3. F-3 — 호출 중(수락 전) 줄도 「바로 시작」 대상인지(기획 2b · 2c — 지금 스펙 「안 함」).
4. F-3 — 원장 없이 시작한 줄의 KOS 쓰기: 집도의 빈 작업으로 `change-flow-step` · `change-tasks-complete` 를 보내도 되는지 데모 실물 확인(확인 안 됨). 원장 없이 시작한 줄의 화면 글자(시안 · SPEC 에 없음).
5. F-3 — 일괄 시작을 서버 엔드포인트 하나로 둘지, 웹이 단건을 여러 번 부를지. 앱에도 둘지.
6. F-7 — 웹 원장 계정이 **다른 원장 지정 호출**을 누를 때: 앱처럼 본인 수락(OQ-A28 · 서버는 이미 받음) / 지정 원장 기본값 팝오버 유지.
7. F-7 — 원장 직무 태그가 붙은 공용 · 마취용 계정(규칙 19 「빼지 않음」)으로 로그인한 웹 PC에서 「본인 즉시 수락」이 맞는지.
8. F-7 — 웹 버튼 글자를 앱처럼 「수락 · N건」 / 「원장 골라 수락 · N건」으로 맞출지, 「수락」 그대로 둘지(화면 글자는 지어 넣지 않는다 — 사용자 결정 필요).
9. F-6 — 「아이콘이 나오는 모든 영역」에 **판 카드 미완료 줄**(지금 아이콘 없음)을 넣는지. 넣으면 시술 전 의사차트(DAY 이력만)를 「작성됨」으로 볼지(지금 판정은 `doctor_note` 만 봄).
10. F-6 — 개발용 키트 견본(`kit_page.html` · `kit.py` · `kit_board.py`)도 맞출지.
11. F-6 — 스펙 「여는 곳 = … · 차트 아이콘」(SPEC-002 :170 · :337 · :341)과 화면 글자 허용표 「있음/없음」(`test_screen_copy.py:126-127`) 정리.
12. F-6 — 원내 현황 · 요청함은 dev 에 화면이 없다 — 앞으로 만들 때 같은 규칙을 기획 · 스펙에 미리 넣을지.

## 확인 안 됨 모음

- KOS 가 집도의 빈 작업의 일정 `change-flow-step(PROCEDURE)` · 작업 `change-tasks-complete` 를 받는지(Q2 ⓐ~ⓒ).
- KOS 원본 작업에 「호출 불필요」류 키가 있는지(우리 매퍼가 안 읽는 키 — Q3).
- KOS `doctors[]` 를 누가 · 언제 미리 채우는지(Q3).
- KOS 가 수락 토큰 주인으로 대리 / 본인을 구분해 남기는지(Q8).
- 병원별로 원장 직무 권한 행을 사람이 바꿨는지 · 공용 원장 계정 존재 여부(Q7 · Q9 — DB 미조회).
- `test_screen_copy.py` 가 안 쓰이는 글자 항목을 실패로 보는지 · `test_board_page.py:723` 둘레 단언 내용(Q10).
