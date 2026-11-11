# CENTURION_DAY#239 구현 결과 보고 — 차트 작성 · 방 이동 (backend + frontend)

## 상태: done (커밋 · push · PR 없음 — 워크트리 변경만)

워크트리 `day-procedure-board-2` · 브랜치 `kknaksss/day-procedure-board-2` · base f1e67a2c(pull 최신 확인).
KOS 호출 없음 · 공유 DB 없음 · 사용자 포트/프로세스 손대지 않음 · `app/` 손대지 않음.

## 검증

| 항목 | 결과 |
|---|---|
| `DAY_ENV_FILE=…/local.env scripts/test.sh -q`(전부 · infra 포함) | **941 passed** |
| `uv run pytest -q -m "not infra"` | **658 passed** |
| `uv run ruff check backend` · `ruff format --check backend scripts` | 통과 · 209 files formatted |
| `scripts/build-css.sh` | day.css 52.4KB 다시 빌드(손으로 안 고침) |
| `alembic heads` | `0008_chart_room (head)` 하나 · `alembic check` 차이 없음(test_alembic) |
| 인라인 `<script>` · `style="` grep(kit 제외) | 0 · 0 |
| 화면 문구 | `test_screen_copy` — 새 글자 7개 모두 SPEC-002 「」 근거로 표에 더함 |

## Phase 별 수행

### 1 데이터 (① ② ⑦)
- migration `20261110_0008_chart_room.py`(revision `0008_chart_room` ← `0007_chat_device`): `visit_task.is_room_assign`(bool · server_default false) · `visit_task.started_room_id`(FK room) · 새 테이블 `visit_task_chart_log` + enum `chart_kind` · `chart_source` + 인덱스 `(task_id, chart)`. upgrade 는 지우거나 바꾸지 않음(테스트) · downgrade 는 테스트용.
- 모델 `models/task.py`(`VisitTaskChartLog`) · enums `ChartKind` · `ChartSource`.
- 동기화: mapper 가 `etceteraConfiguration.etceteraTaskId` → `NTask.etc_task_external_id` · `sync.is_room_assign()`(설정 id 와 같은 **기타 작업**만) · `apply_schedules(room_assign_etc_task_id=)` ← `emr_sync` 가 `crm_connection.config.room_assign_etc_task_id` 로 넘김(비면 「방 배정」 없음 · OQ-49).
- 판정 교체: `board_rules.is_room_task` = `t.is_room_assign`(방 붙은 기타 작업 + 미호출 판정 삭제). 그 밖 기타 작업은 시술 줄 · 체크 · 호출 · 전부 완료 판정(기타 작업 미완료면 canHome false).
- ⑦ 설정 값 넣기: `scripts/seed_demo_connection.py` 에 env `DAY_SEED_KOS_ROOM_ASSIGN_ETC_TASK_ID`(선택 · 비면 넣어 둔 값 유지) · 일회성 `scripts/set_room_assign_etc_task.py`(env `DAY_ROOM_ASSIGN_HOSPITAL_ID` · `DAY_ROOM_ASSIGN_ETC_TASK_ID` — 그 키만 넣고 다른 키 그대로). 값은 코드에 없음 · `deploy/local.env.example` 에 빈 칸.

### 2 차트 (③ ④)
- KOS 쓰기 종류 3 추가(`emr/base.py` · `kos/writes.py`): `assignee_memo`(change-flow-tasks-assignee-memo) · `doctor_memo`(change-flow-tasks-doctor-memo) · `add_room_assign`(add-flow-tasks · ETCETERA 하나만 열림). 확인 키 `assignee_memo/_from` · `doctor_memo/_from` · `room_assign_added`.
- outbox: 글 확인 · **밀려남**(`memo_overtaken` — KOS 값이 보낸 글도 보내기 전 글도 아니면 confirmed · 재전송 없음) · 「방 배정」 만들기 확인(`added_room_assign` — 만들기 전에 없던 sequence).
- 동기화: 반영 대기 글 guard(조회가 안 덮음) · KOS 글이 DAY 사본과 다르면 DAY 값 + 이력 `source=kos`(작성자 없음 = 「KOS」 · 담당자 = 그때 DAY 담당자/집도의 · 시각 = 조회 시각) · 방 쓰기가 반영 대기면 `visit.room_id` 도 DAY 값 유지.
- service `save_chart`: 404 → `chart_conflict`(baseLogId ≠ 마지막 이력 · 새 값 `details`) → `chart_staff_required` → `staff_not_listed`/`doctor_not_listed` → 바뀐 것 없음(200 no-op) → 이력 1행 + DAY 값 + outbox(간호관리 = assignee-memo 만 · KOS assignees 안 씀 / 의사 수락 · 진행중 = 규칙 27 전부(`task.doctor_change`) → change-tasks-doctors → doctor-memo / 완료 = 집도의만 / **시술 전 = 이력만**) + `event_log task.chart_save`. 글은 앞뒤 빈칸 정리(KOS mapper 와 같게 — 가짜 「KOS 수정」 방지).
- 시술 전 의사차트 보내기(`_prestart_doctor_chart`): [수락] 때(호출 없는 [시작]이면 [시작] 때) 마지막 이력이 DAY 면 실제 원장과 다를 때 덮은 이력(누른 직원 · 그 시각) + 글이 KOS 사본과 다르면 doctor-memo 를 그 조작 op 뒤에 · 마지막 이력이 KOS 면 안 보냄.
- 차트 JSON(규칙 위치 = `board_rules.chart`): `firstTab`(의사 → doctor · 그 밖 assignee) · 담당자 처음 값 3단계 · `staffOptions`(간호관리 = nurse · skincare 태그 · 시스템 계정 뺌 / 원장 목록).

### 3 방 이동 (⑤ ⑥)
- `board_rules`: `hold_room`(살아 있는 「방 배정」 방 ≠ 카드 방) · `home_room`(취소 포함 · sort_order 첫 · 없으면 카드 방) · `room_move_block`(visit_not_on_board → room_held(점유 · 만드는 중) → room_same) · `room_return_block` · `move_plan`(점유 이동 = 지금 방 「방 배정」 남기고 나머지(완료 포함 · 취소 뺌) / 이동 = 전부).
- service `room_move` · `room_return` · `follow_room_assign`(「방 배정」 확인된 조회에서 새 sequence 를 원래 방에 두는 change-tasks-room 을 같은 조작 · 같은 보낼 직원으로 쌓고 DAY 작업 방도 원래 방) — `emr_sync.run_schedules` 가 confirm 뒤 부름.
- `started_room_id`: [시작] 때 카드 방 · 「시작 취소」 때 비움.
- 스냅샷: `cards[].holdRoom` · `canMoveRoom` · `canReturnRoom` · `rooms[]` · `doneTab[].homeRoom`(doneTab 은 원래 방 room.order 묶음 순 · 묶음 안 지금 순서).

### 4 frontend
- 차트 모달 `partials/board_chart_parts.html`(새) · `board_chart.html` · 저장 응답 `board_chart_saved.html`(새): 탭 간호관리차트 | 의사차트 · 표 「시술명 · 담당자 · 차트 내용」 · 담당자 = medikit `ms-input` select(빈 칸 = 빈 option · 글자 없음) · 작성자 · 「최근 저장 : HH:MM」 · 권한 없으면 읽기만. 저장 응답 = OOB(baseLogId · 작성자 · 최근 저장)만 — 쓰는 중인 글 칸은 안 바뀜 · 충돌 = 그 줄 통째 OOB + 토스트 · 집도의 바꿨으면 + 조작 응답 OOB(카드 · 원장 상태 · version 헤더).
- `day.js`: 자동 저장(textarea 입력 멈춤 2초 · 줄에서 포커스 나감 · 담당자 select change · 창 닫힐 때 · 한 줄에 요청 하나 직렬화 · 담당자 비면 안 보냄) · `data-day-row-get`(시술 줄 → 차트 GET → #modal-root) · 방 고르면 푸터 버튼 켜기.
- 판 카드(`board_parts.html`): 방 이름 = 방 옮기기 팝오버 트리거 · 팝오버(방 이름만 · 지금 방 뺌 · 점유 중인 방 포함 · 「점유 이동」 · 「이동」 / 점유 중 [복귀하기]만) · 점유 파란 띠(이전 방 + [복귀하기]). pops 에서 미리 그린 읽기 전용 차트 창 제거(열 때 GET).
- 「시술 완료」 탭(`board_done_list.html`): 원래 방 접는 칸(E17 accordion) 묶음 · 방 없는 방문은 머리 없이.
- 오류 토스트: 글자가 정해지지 않은 코드(chart_staff_required · staff_not_listed · visit_not_on_board · room_same · room_not_held · room_held · room_assign_unset)는 **토스트를 비움**(OQ-41 · OQ-48). chart_conflict = 「다른 직원이 먼저 저장한 줄은 저장하지 않았습니다」.
- CSS(`styles/app.css` 토큰 · 클래스만 → build): `day-modal--chart-table` · `day-chart__row/__cell/__saved/__author…` · `day-card__room` · `day-card__hold`.
- 견본(`kit_board.py`): 방 목록 · 점유 카드(시술실 B ← 시술실 D) · 기타 작업 줄(모델링팩).

### 스크린샷(정적 렌더 · headless Chrome — 실물 11040 아님)
`screens-239/` — `a1-a7-board-etc-line-hold-band.png`(기타 작업 줄 · 파란 띠 · 「방 배정/」 안 보임) · `a3-chart-nurse-tab.png` · `a3-chart-doctor-tab.png`(작성자 「KOS」 · 최근 저장) · `a7-room-popover.png`. 시술 완료 탭 묶음은 화면 테스트로만 확인.

## Acceptance 판정(테스트 이름)

| A | 판정 | 근거 |
|---|---|---|
| A1 | ✓ | `test_방배정_판정은_기타_작업_종류_id_와_연결_설정_id` · `test_방배정은_연결_설정_id_와_같은_기타_작업만`(infra) · `test_방_붙은_다른_기타_작업은_시술_줄이고_체크_호출_대상이다` · `test_기타_작업도_종료해야_귀가_대기` · `test_설정이_비면_방배정이_없어_기타_작업이_전부_보인다` · 귀가 대기 cancel op = is_room_assign 만(`test_cc_근거_쓰기는…` 갱신) · 스크린샷 |
| A2 | ✓ | migration 테스트 3 · `test_alembic`(head · check) · `test_column_snapshot`(52 테이블) · `test_enum_labels`(32) · `test_차트_이력은_지우는_경로가_없다` · `test_호출_없이_시작하면_시작_때_보내고_진행한_방을_남긴다`(started_room_id 채움 · 비움) |
| A3 | ✓(화면 테스트 + 정적 스크린샷) | `test_차트_조각은_두_탭_표_담당자_자동_저장_칸` · `test_차트_권한이_없으면_읽기만…` · `test_차트_저장_응답은_OOB_충돌이면…` · `test_차트_첫_탭_담당자_처음_값_목록` · `test_웹_차트_저장은_OOB…` — 자동 저장 타이밍(2초 · blur) 자체는 브라우저 동작이라 실물 확인 필요 |
| A4 | ✓ | `test_간호관리차트_저장_이력_DAY값_assignee_memo_만` · `test_연_때_값과_다르면_409_chart_conflict_와_새_값` · `test_담당자_없음_목록_밖_404` · `test_수락_뒤_의사차트_집도의_변경은_규칙27_전부_후_메모` · `test_차트_글_쓰기는_통째_덮어쓰기_확인은_KOS_사본` |
| A5 | ✓ | `test_시술_전_의사차트는_이력만_수락_때_덮고_메모를_수락_뒤에` · `test_시술_전_글_뒤_KOS_수정이_마지막이면_수락_때_보내지_않는다` · `test_호출_없이_시작하면…` · `test_KOS_차트_글_변경은_DAY값과_이력_source_kos`(infra) · `test_반영_대기_차트_글과_방은_조회가_덮지_않는다`(infra) · `test_글_확인_때_제3_값이면_KOS_가_이기고_다시_보내지_않는다` |
| A6 | ✓ | `test_점유_이동은_방배정만_남기고_완료까지_새_방_복귀는_취소와_원래_방`(op · DAY 값 · holdRoom · room_held · room_not_held · 카드 순서 자리 · event_log) · `test_이동은_방배정까지_전부…` · `test_방_이동_오류_코드`(room_same · 404 · 400 · visit_not_on_board) · `test_방배정이_없고_설정도_비면…`(room_assign_unset) · `test_방배정이_없으면_만들고_다음_조회_뒤_원래_방에_둔다` · `test_방배정_만들기_확인은…` |
| A7 | ✓(화면 테스트 + 정적 스크린샷) | `test_방_이름은_방_옮기기_팝오버_점유면_파란_띠와_복귀하기` · `test_시술_완료_탭은_원래_방으로_묶는다` · `test_웹_방_이동은_누른_카드와_OOB_거절_글자는_비움` |
| A8 | 코드 ✓ · 데이터 넣기는 코디 | `test_room_assign_setting.py` 3 — 로컬 · dev DB 에 실제로 넣는 것은 하지 않음(아래 「코디가 할 것」) |
| A9 | 미실행(범위 밖) | KOS 호출 금지 — 데모 실물은 코디 · 사용자 |
| A10 | ✓ | 위 검증 표 |

## 앱이 쓸 새 JSON API (`/api` · Bearer · 오류 = `{detail, code, field[, details]}`)

| 동작 | 경로 | 본문 | 성공 |
|---|---|---|---|
| 차트 조회(모양 바뀜) | `GET /api/visits/{visitId}/chart` | — | `{visitId, visitDate, customer, firstTab: "assignee"\|"doctor", tasks: [{id, title, assignee: Cell, doctor: Cell}], staffOptions: {assignee: [{staffId, name}], doctor: [{staffId, name}]}}` · `Cell = {body, staffId, author: {staffId, name}\|"KOS"\|null, savedAt, logId}` |
| 차트 저장 | `POST /api/tasks/{taskId}/chart` | `{chart: "assignee"\|"doctor", body: str\|null, staffId: uuid\|null, baseLogId: uuid\|null}`(extra 금지) | 그 줄 · 그 차트 `Cell` · 409 `chart_conflict` 의 `details` = `{taskId, chart, ...Cell}` · 409 `chart_staff_required` · `staff_not_listed` · `doctor_not_listed` · 404 `not_found` |
| 방 이동 | `POST /api/visits/{visitId}/room-move` | `{mode: "hold"\|"all", roomId: uuid}` | `{ok: true}` · 409 `visit_not_on_board` · `room_held` · `room_same` · `room_assign_unset` · 404 |
| 복귀 | `POST /api/visits/{visitId}/room-return` | 없음 또는 `{}` | `{ok: true}` · 409 `visit_not_on_board` · `room_not_held` |
| 스냅샷 추가 칸 | `GET /api/board` · SSE | — | `cards[].holdRoom{id,title}\|null` · `canMoveRoom` · `canReturnRoom` · `rooms[{id,title}]` · `doneTab[].homeRoom` · 기타 작업이 `tasks[]`(kind `etc`)에 새로 보임 |

## 이슈 · 코디가 확인할 것

1. **A8 데이터 넣기(코디 · 배포 뒤)**: 로컬 = `DAY_SEED_KOS_ROOM_ASSIGN_ETC_TASK_ID=683ba150dccf503ddc5487e9` 를 local.env 에 넣고 seed 다시, 또는 `DAY_ROOM_ASSIGN_HOSPITAL_ID=<데모 병원 id> DAY_ROOM_ASSIGN_ETC_TASK_ID=683ba150dccf503ddc5487e9 uv run python scripts/set_room_assign_etc_task.py`(migration 0008 뒤). dev = 같은 일회성 스크립트를 VM 에서(앱 env). 다음 일정 동기화부터 판에 기타 작업이 보이고 「방 배정/」만 숨는다. 넣기 전엔 OQ-49 기본값 = 기타 작업 전부 보임 · [귀가 대기]가 「방 배정」을 취소하지 않음.
2. **새 오류 코드 `room_assign_unset`(제안 · 발명)**: OQ-49 「점유 이동은 만들 id 가 없어 거절」의 코드가 SPEC 에 없어 만들었다(409 · 토스트 비움). spec-sync 때 SPEC 매트릭스에 반영 또는 이름 결정 필요.
3. **「방 배정」 만들기 본문 이름**: add-flow-tasks 는 `title` · `etceteraConfiguration.name` 이 필요한데 설정엔 id 만 있다 → 그 병원에서 본 「방 배정」 작업 이름(`etc_task_title`)을 쓴다. 본 적이 없으면 op 을 만들지 않고 `event_log.payload.kos` 에 `skipped`(DAY 이동은 됨). 데모 실물(A9 ④)에서 확인.
4. **이력 「처음 본 KOS 글」**: 동기화가 처음 보는 작업에 KOS 메모가 있으면 이력 1행(source kos)을 남긴다(DAY 사본 없음 = 다름). 배포 전부터 있던 작업(사본 같음)은 이력 없음 — 작성자 칸이 비어 보인다.
5. **카드 방 규칙(OQ-38)**: DAY 는 이동 즉시 `visit.room_id` 를 바꾸고 방 쓰기가 반영 대기인 동안 조회가 안 덮는다. 확인 뒤엔 KOS `roomAssignedDateTimeUtc` 가장 늦은 작업 방으로 돌아간다 — KOS 가 그 시각을 새로 찍지 않으면 카드가 옛 방으로 돌아갈 수 있음(A9 ①에서 확인).
6. change-tasks-room 은 옮길 작업 전부를 **한 요청 `sequences` 여러 개**로 보낸다(OQ-38 확인 안 됨 — A9 ⑥). 메모는 작업마다 한 요청.
7. 차트 이력 「최근 저장」은 그 방문 차트 이력 마지막 행(KOS 행 포함). 차트 JSON 에 따로 칸을 두지 않고 화면이 `savedAt` 최대값으로 그린다.
8. 웹 자동 저장 · 팝오버 동작은 정적 렌더 + 테스트로만 확인 — 로컬 11040 재기동 뒤 실물 클릭 확인 필요(코디).
9. 기존 `ui.chart_modal`(읽기 전용) 매크로는 dev 견본(kit_page)만 쓴다 — 판에서는 안 씀.

## 변경 파일
backend/day: dtos/board.py · emr/{base,normalized,outbox,sync}.py · emr/kos/{mapper,writes}.py · enums/task.py · errors.py · models/{__init__,task}.py · public.py · queries/board.py · routers/{board,kit_board}.py · routers/api/board.py · services/{board,board_rules,crm_connections,emr_sync}.py · web_errors.py · static/{day.js,day.css(빌드)} · styles/app.css · templates/partials/{board_chart,board_chart_parts(새),board_chart_saved(새),board_done_list,board_parts,board_regions,board_toast_error}.html
backend/migrations/versions/20261110_0008_chart_room.py(새)
backend/tests: architecture/test_screen_copy.py · day/{test_column_snapshot,test_enum_labels,test_models,test_room_assign_setting(새)}.py · day/board/{test_board_api,test_board_queries,test_board_rules,test_board_chart_api(새),test_board_room_api(새)}.py · day/emr/{test_kos_board_contract,test_sync}.py · day/web/test_board_page.py · migrations/{test_alembic,test_chart_room_migration(새)}.py
scripts/{seed_demo_connection.py, set_room_assign_etc_task.py(새)} · deploy/local.env.example
