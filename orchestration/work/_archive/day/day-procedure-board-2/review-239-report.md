# 리뷰 리포트 — day-procedure-board-2 / code — CENTURION_DAY#239 (차트 · 방 이동 · 「방 배정」 판정) (2026-11-10)

대상: `CENTURION_DAY/day-procedure-board-2` HEAD f1e67a2c 위 미커밋 50파일(수정 42 + 새 8 · migration `0008_chart_room`). 워커 보고 `code-239-report.md`.
SSOT: Delivery #239(승인) · SPEC-002 개정 ⑯ · SPEC-000(스펙 PR #921 워크트리) · `_RESUME.md` §2 차트 · 방 이동 · 결정 (가) · 「방 배정」 id 행.
파일 경로는 `backend/` 기준.

## 판정: WARN (FAIL 0 — 단 W1 은 머지 전 결정 필요)

A1 ~ A8 · A10 의 서버 계약은 스펙대로이고 API · infra 테스트가 실제로 막는다. 다룬 것: 「방 배정」 판정 · 기타 작업 · 차트(담당자 DAY 만 · 집도의 · 메모 · 이력 · 충돌 · 결정 (가)) · 방 이동 · 복귀 · migration · 웹 응답 모양 · 앱 JSON 계약.
남은 것:
- W1: 스펙(규칙 28 + 카드 방 규칙)을 그대로 따른 결과, 「방 배정」을 새로 만드는 점유 이동은 KOS 확인 뒤 카드가 원래 방으로 돌아가는 논리 결함이 있다.
- W2 · W3: 사용자가 누른 동작이 화면에 아무 표시 없이 안 되는 「조용히 통과」 자리 두 곳.
- W4: 완료 시술 집도의 변경의 KOS 부작용(확인 안 됨).

검증(직접 1회):
- `DAY_ENV_FILE=…/local.env scripts/test.sh -q` → **941 passed**(1 warning · 77초).
- `uv run ruff check backend scripts` → All checks passed.
- templates 인라인 `<script>`(src 없음 · kit 제외) 0 · `style="` 0.

## FAIL

없음.

## WARN

### W1. (높음) 「방 배정」을 **새로 만드는** 점유 이동은, KOS 반영이 확인된 뒤 카드 방이 원래 방으로 돌아가 점유가 사라진다
- 흐름:
  - `services/board.py` `room_move`(1328 ~) — 「방 배정」이 없으면 `add-flow-tasks` → 나머지 작업 `change-tasks-room`(새 방)을 쌓는다.
  - 다음 조회에서 새 sequence 를 알면 `follow_room_assign`(1483 ~)이 그 「방 배정」을 원래 방에 두는 `change-tasks-room` 을 **그 뒤에** 쌓는다.
- 카드 방 규칙은 그대로다 — `emr/kos/mapper.py:423` `card_room` = 「방이 붙은 작업(type 무관) 중 `roomAssignedDateTimeUtc` 가 **가장 늦은** 작업의 방」(SPEC-002 동기화 표 · 규칙 28 「카드 지금 방은 지금 규칙을 따른다」). 이번 diff 는 이 함수를 바꾸지 않았다(mapper diff = `etc_task_external_id` 한 줄).
- 그래서 KOS 가 `change-tasks-room` 때 배정 시각을 새로 찍으면(OQ-38 — 카드 방 규칙 전체가 이 전제에 기댄다), 원래 방에 마지막으로 놓인 「방 배정」이 가장 늦은 작업이 된다. 반영 대기가 풀린 뒤 조회는 `visit.room_id` = **원래 방**으로 되돌리고, 점유 판정(「방 배정」 방 ≠ 카드 방)은 거짓이 되어 띠가 사라진다. 시각을 찍지 않는 경우는 OQ-38 이 이미 말하는 다른 문제다. 어느 쪽이든 이 경로는 의도대로 끝나지 않는다.
- 「방 배정」이 이미 있는 보통 경로(접수 때 배정 — 가장 이른 시각)와 이동 · 복귀는 이 문제가 없다.
- 테스트 `tests/day/board/test_board_room_api.py::test_방배정이_없으면_만들고_다음_조회_뒤_원래_방에_둔다` 는 op 순서 · DAY 값까지만 보고, 확인 뒤 조회의 카드 방은 보지 않는다 — 그래서 통과한다.
- 고칠 길(스펙 결정 필요 · 사용자 「드묾」):
  - ⓐ 카드 방 규칙에서 「방 배정」(`is_room_assign`) 작업을 뺀다(OQ-38 의 대안과 같은 방향 — 보통 경로 결과는 같음).
  - ⓑ 이 경로만 DAY `visit.room_id` 를 지킨다.
  - ⓒ 만들기 경로를 데모 실물(A9 ④) 전까지 막는다.
  - ⓐ 가 가장 단순하다 → **planner · 사용자 확인 ①**.

### W2. 「점유 이동」이 아무 표시 없이 거절되는 자리 — 설정이 비었을 때 `room_assign_unset`(새 코드) · 오류 토스트를 비움
- `services/board.py` `room_move` — 남길 「방 배정」이 없고 설정 id 가 비면 409 `room_assign_unset`. `web_errors.py` 는 `UNSET_MESSAGES`(routers/board.py)에 든 코드면 토스트 글자를 비우고, `partials/board_toast_error.html` 은 `{% if message %}` 라 **토스트가 안 뜬다**.
- prod 설정을 넣기 전(OQ-49 — 배포 체크)에는 `is_room_assign` 이 전부 false 라, 모든 카드의 「점유 이동」이 이렇게 된다: 눌러도 아무 일도 없고 아무 표시도 없다. `room_held` · `room_same` 은 화면이 버튼을 감추거나(팝오버에 [복귀하기]만 · 지금 방 뺌) 거의 생기지 않는다. `room_assign_unset` 만 화면이 미리 막지 않는다.
- 코드 이름 `room_assign_unset` 은 스펙에 없다 — 워커가 밝혔다(OQ-49 「거절」의 코드). 이름 자체는 제안 표기로 spec-sync 하면 된다.
- 권함:
  - ⓐ 스냅샷에 `canHoldMove`(또는 `rooms` 응답에 「점유 이동 가능」)를 실어 설정이 비면 「점유 이동」 버튼을 끈다(새 글자 0).
  - ⓑ 비운 토스트 정책(OQ-41 · 48)을 「거절은 공용 폴백 글자 「요청이 올바르지 않습니다」」로 되돌린다(앞 #236 의 `task_not_assignable` 처리와 같은 방식).
  - → **사용자 확인 ②**.

### W3. 「방 배정」을 만들 이름을 본 적이 없으면 점유 이동이 조용히 「이동」이 된다
- `services/board.py` `_room_assign_title`(1307 ~) — 그 병원에서 `is_room_assign` 작업을 본 적이 있어야 `add-flow-tasks` 의 `title` · `etceteraConfiguration.name` 을 채운다. 없으면 `Skipped("add_room_assign")`(event_log `payload.kos`).
- 그런데 DAY 는 이미 모든 작업을 새 방으로 옮겼고(`room_move` 앞부분 · keep 없음), 응답은 200 이다. 그래서 사용자가 「점유 이동」을 눌렀는데 결과는 점유 없는 「이동」과 같다. 원래 방 기록이 없어 띠 · [복귀하기]도 없다.
- 워커 보고 #3 이 짚었다. 설정이 있는 병원은 접수 때 「방 배정/」을 거의 늘 보므로 드물다. 다만 「조용히 통과」라 기록한다 — 이름을 못 구하면 `room_assign_unset` 처럼 409 로 거절하는 편이 안전하다(코드 한 줄 · 사용자 확인 ② 와 같이).

### W4. 완료 시술의 의사차트 집도의 변경 → KOS `change-tasks-doctors` — 상태가 바뀌는지 확인 안 됨
- `services/board.py` `save_chart` — 완료 시술이면 `_set_task_doctor` + `change_doctor` op(규칙 31 「완료는 집도의만」 · 스펙대로).
- 근거 두 가지:
  - 사용자가 확인한 KOS 사실: 「집도의를 고르면 그 시술이 수락 → 시술 진행 중으로 바뀐다」(`_RESUME.md` §2 :71).
  - DAY [수락] op 의 확인 조건도 같은 요청 뒤 `status = READY` 다(`emr/kos/writes.py` accept_doctor).
- 그래서 **DONE 작업에 `change-tasks-doctors`** 를 보내면 KOS 가 그 작업을 READY · 진행으로 되돌릴 수 있다. `change_doctor` 확인 조건은 `doctors_equal` 뿐이라 이것을 잡지 못한다. 그러면 다음 조회가 DAY 작업 상태를 KOS 값으로 바꿔, 완료가 풀린다. 이것은 「완료 취소」를 누르지 않았는데 일어나는 일이다.
- A9 ⑧ 은 「의사차트 집도의 KOS 반영(수락 뒤)」만 적었다 → **완료 시술 집도의 변경을 A9 데모 실물에 더할 것**. 확인 전까지 완료 시술은 KOS 쓰기를 미루는 선택지도 있다 → **사용자 확인 ③**.

### W5. (낮음) 웹 자동 저장 · 팝오버 동작은 화면 테스트(문자열) · 정적 스크린샷까지만
- `static/day.js` 자동 저장(입력 멈춤 2초 · 줄 blur · select change · 창 닫힐 때 · 한 줄 직렬화)과 방 팝오버 푸터 켜기는 브라우저 동작이다. 실물 클릭 확인이 남았다(워커 보고 #8 — 코디가 로컬 재기동 뒤). A3 · A7 「스크린샷 · 화면 테스트」의 화면 쪽 확인 거리.

## PASS

### A1 「방 배정」 판정 · 기타 작업 (①)
- `emr/kos/mapper.py`: `etceteraConfiguration.etceteraTaskId` → `NTask.etc_task_external_id`. `emr/sync.py` `is_room_assign`(설정 id 와 같은 **기타 작업**만). `services/emr_sync.py` 가 연결 `config.room_assign_etc_task_id` 를 넘긴다 · 비면 「방 배정」 없음(OQ-49).
- `board_rules.is_room_task` = `t.is_room_assign`(옛 「방 붙은 기타 작업 + 미호출」 판정 삭제). 그 밖 기타 작업은 시술 줄 · 체크 · 호출 · 전부 완료(기타 작업 미완료면 `canHome` false) — 재리뷰 답 ①.
- [귀가 대기] KOS 취소 op = `is_room_assign` 작업만.
- 테스트: `test_방배정_판정은_…` · `test_방배정은_연결_설정_id_와_같은_기타_작업만`(infra) · `test_방_붙은_다른_기타_작업은_시술_줄이고_…` · `test_기타_작업도_종료해야_귀가_대기` · `test_설정이_비면_…`.

### A2 데이터 · migration (②)
- `migrations/versions/20261110_0008_chart_room.py`: `0007_chat_device` → `0008_chart_room` · head 하나(`test_alembic` · `alembic check` 차이 없음).
- `is_room_assign`(server_default false — 기존 행 업그레이드 안전 · 다음 동기화가 채움) · `started_room_id`(FK room · null) · `visit_task_chart_log`(enum 2 · 인덱스 `(task_id, chart)` · FK 기본 RESTRICT).
- 머리말에 「forward-only — 운영에서 downgrade 를 돌리지 않는다(차트 이력 = 의료 기록) · downgrade 는 테스트 스키마 왕복용」 — #239 WP 리뷰 W3 대로다. `downgrade()` 도 있다(test_alembic 왕복 통과).
- 이력을 지우는 경로 없음(`test_차트_이력은_지우는_경로가_없다`) · `test_chart_room_migration`(기존 데이터에서 upgrade) · column snapshot · enum labels 갱신.

### 차트 (③ ④ · A3 서버 · A4 · A5)
- `save_chart` 검사 순서 = 404 → `chart_conflict`(baseLogId ≠ 마지막 이력 · rollback · `details` = 새 값) → `chart_staff_required`(409 — 스펙 W4 반영) → `staff_not_listed` · `doctor_not_listed` → 바뀐 것 없음(no-op · rollback). 스펙 규칙 31 매트릭스 순서와 같다.
- 간호관리 = 이력 + `assignee_note` + `assignee_memo` op 만(KOS assignees 안 씀). 의사:
  - 수락 · 진행중이면 규칙 27 전부(`_change_doctor_rows` · `task.doctor_change`) → `change-tasks-doctors` → `doctor-memo`(op 순서 = 스펙 「집도의 먼저 → 메모」).
  - 완료면 집도의만(W4).
  - **시술 전(`is_pre_start`)이면 이력만** — op · `doctor_note` · 집도의 그대로라 [시작] 조건이 바뀌지 않는다(결정 (가)).
- 글 앞뒤 빈칸 정리(`chart_body`)를 KOS mapper 와 같게 해서 가짜 「KOS 수정」 이력을 막는다.
- 결정 (가) 보내기 `_prestart_doctor_chart`(754 ~): [수락]과 호출 없는 [시작](`effective_call is None` · 실제 원장 = `kos_doctor`) 때 마지막 이력이 DAY 면 ① 집도의 ≠ 실제 원장일 때 덮은 이력(작성자 = 누른 직원 · 지금 — OQ-50) ② 글이 KOS 사본과 다르면 `doctor_note` 갱신 + `doctor-memo` 를 **그 조작 op 뒤에**(accept: `[intent, *_memo_intents]` · start: flow_step 뒤). 마지막 이력이 KOS 면 보내지 않는다(재리뷰 답 ③).
- 동기화(`emr/sync.py`): 반영 대기 글 guard · KOS 글 ≠ DAY 사본이면 DAY 값 + 이력 `source=kos`(작성자 없음 = 「KOS」 · 시각 = 조회). outbox `memo_overtaken`(KOS 값이 보낸 글도 보내기 전 글도 아니면 confirmed · 재전송 없음).
- 테스트: A4 · A5 이름들(워커 보고 표) — `test_시술_전_의사차트는_이력만_수락_때_덮고_메모를_수락_뒤에` · `test_시술_전_글_뒤_KOS_수정이_마지막이면_…` · `test_글_확인_때_제3_값이면_KOS_가_이기고_…` · `test_반영_대기_차트_글과_방은_조회가_덮지_않는다`(infra) 등.
- 「처음 본 KOS 글」 이력(워커 #4)은 스펙 규칙 32 ② 그대로라 맞음.

### 방 이동 (⑤ ⑥ · A6)
- `board_rules` `room_move_block` 순서 = `visit_not_on_board` → `room_held`(점유 중 · 「방 배정」 만드는 중 = 반영 대기 add op) → `room_same`. `move_plan`: 점유 이동 = 지금 방 살아 있는 「방 배정」 남기고 나머지(완료 포함 · 취소 뺌) · 이동 = 전부. `hold_room` = 살아 있는 「방 배정」 방 ≠ 카드 방 · `home_room` = 취소 포함 · sort_order 첫 · 없으면 카드 방.
- `room_return`: 「방 배정」 DAY 즉시 canceled + `cancel-flow-tasks` → 나머지 `change-tasks-room`(원래 방) — 스펙 순서. 같은 방문 잠금(`_world`)으로 동시 조작을 막는다.
- 「방 배정」 만들기 확인 `added_room_assign` = 그 설정 id 의 살아 있는 작업 중 **만들기 전 알던 sequence 에 없던 것**(여럿이면 가장 큼) — KOS 에서 따로 생긴 다른 작업을 「방 배정」으로 잘못 고르지 않는다.
- `started_room_id` = [시작] 때 카드 방 · 「시작 취소」 때 비움(규칙 30). 카드 순서 자리 그대로 · `event_log visit.room_move` · `visit.room_return`.
- 테스트: `test_board_room_api.py` 4 + rules · web.

### 웹 응답 · 화면 (④ ⑤ · #236 ⑲)
- `room-move` · `room-return` = `_after`(누른 카드 + OOB + version) — #239 WP 리뷰 W2 대로다.
- 차트 저장 = 그 줄 OOB(baseLogId · 작성자 · 최근 저장 — 쓰는 중인 글 칸은 안 바꿈) · 충돌이면 그 줄 통째 + 토스트 「다른 직원이 먼저 저장한 줄은 저장하지 않았습니다」 · 집도의를 바꿨으면 카드 · 원장 상태 OOB + version 헤더(routers/board.py `_chart_saved`).
- 새 화면 글자 9개(`test_screen_copy`) = 시술명 · 담당자 · 차트 내용 · 최근 저장 : · 점유 이동 · 이동 · 복귀하기 · 간호관리차트 · 의사차트 — 모두 SPEC-002 U-14 · U-15 「」. 새로 지은 글자 0. 정해지지 않은 거절 글자는 비움(W2).
- CSS 는 `styles/app.css` 토큰 · 클래스만 + 빌드. 인라인 0.

### 앱 JSON 계약 (#239 ⑥ · 앱은 다음 작업)
- `GET /api/visits/{id}/chart` = `{visitId, visitDate, customer, firstTab, tasks[{id, title, assignee: Cell, doctor: Cell}], staffOptions}` · `Cell = {body, staffId, author: {staffId, name}|"KOS"|null, savedAt, logId}` — SPEC-002 차트 JSON 과 같다.
- `POST /api/tasks/{id}/chart {chart, body, staffId, baseLogId}`(extra 금지) · `room-move {mode: hold|all, roomId}` · `room-return`(빈 본문 · `{}`) · 스냅샷 `holdRoom` · `canMoveRoom` · `canReturnRoom` · `rooms[]` · `doneTab[].homeRoom` — 스펙 모양과 같다.
- 스펙 밖: 오류 코드 `room_assign_unset`(W2) · 충돌 응답 `details`(공용 오류 모양에 더한 칸 — 스펙 「409 + 새 값」의 구현) — spec-sync 거리.

### 회귀
- 941 passed — #234 · #236(체크박스 · 재호출 · 확인 필요 · 카드 순서 · version) · 앱 · 채팅 · 알림 테스트를 포함한다. 기존 「방 붙은 기타 작업 = 방 배정」 단언은 새 판정으로 고쳐졌다(`test_kos_board_contract` · rules).

## 사용자 · 코디 확인

| # | 무엇 | 근거 |
|---|---|---|
| ① | 「방 배정」을 새로 만드는 점유 이동은 KOS 확인 뒤 카드가 원래 방으로 돌아간다 — ⓐ 카드 방 규칙에서 「방 배정」 작업 빼기(권함) ⓑ 이 경로만 DAY 방 지키기 ⓒ 데모 실물 전까지 막기(W1) | mapper.py:423 · board.py room_move · follow_room_assign · SPEC-002 규칙 28 · OQ-38 |
| ② | 설정이 비었을 때(prod 설정 전) 「점유 이동」이 아무 표시 없이 안 됨 — 버튼 끄기(`canHoldMove`) 또는 공용 폴백 토스트(W2) · 「방 배정」 이름을 못 구하면 조용히 「이동」이 됨 → 409 로 바꿀지(W3) | web_errors.py · board_toast_error.html · board.py `_room_assign_title` |
| ③ | 완료 시술 의사차트 집도의 변경이 KOS 에서 시술을 다시 진행으로 바꿀 수 있음 — A9 데모 실물에 더하기 · 확인 전엔 완료 시술 KOS 쓰기 미루기(W4) | `_RESUME.md` §2 :71 · writes.py accept_doctor 확인 조건 |
| ④ | A8 데이터 넣기(로컬 · dev 데모 연결 `room_assign_etc_task_id`)와 웹 자동 저장 · 팝오버 실물 확인(W5) | 워커 보고 #1 · #8 |
