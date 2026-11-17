# [backend] fix-feedback — 바로 시작 · 귀가 대기 취소 · 정렬 서비스(F-1 · F-2 · F-3)
# [backend] <한 줄 제목>

너는 **day `backend` 워커**다. 너는 앞 맥락이 없다 — 아래 파일이 전부다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **frontend 워커가 같은 워크트리에서 동시에 작업한다** — 서로의 파일을 건드리지 마라. 계약(§3)이 둘 사이의 경계다. 상대 몫이 필요하면 고치지 말고 리포트에 「frontend 몫」으로 적어라.

## 1. SSOT — 먼저 읽을 것

- **스펙(계약의 SoT — 여기 없는 건 발명하지 마라)**: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ㉑(머리 :42 · U-2 :207 · U-3 :217-219 · U-9 :292 · U-12 :342 · API :571-584 · 매트릭스 :720-726 · 검사 순서 :742 · 토스트 표 :765 · KOS 쓰기 :823-838 · 규칙 34 :922-926 · 35 :928 · 36 :929 · 37 · OQ-58 ~ 66 :988-996) · `spec-005-notifications.md` 2026-11-17 개정(U-5 :154-159 · S-6 :194 · §3 웹 OS 알림 :278-280 · 매트릭스 :301-304 · OQ-N8 ~ N13 :420-425). **이 스펙은 아직 미커밋(워크트리에만)** — 위 절대경로로 읽어라. 줄 번호는 근처를 grep 으로 확인.
- 「기본값(코디 2026-11-17 · 사용자 E2E 에서 확인)」 꼬리표가 붙은 값은 **그대로 짓는다**(OQ 는 열려 있어도 기본값이 계약).
- 사용자 결정 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/e2e-feedback.md` · 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/research-1-report.md` · planner `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/spec-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/spec-2-report.md` · 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/review-doc-1-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/review-doc-2-report.md`(있으면).
- 코드 레포 루트 `AGENTS.md` 를 먼저 읽어라(계층 · 화면/업무 경계).

기대는 개념: 해당 없음.

## 2. 배경

사용자 2026-11-17 DAY 현장 피드백 F-1 · F-2 · F-3 · F-4 · F-6 · F-7 을 구현한다(F-5 는 범위 밖). 목표는 **사용자가 로컬에서 E2E 를 할 수 있는 상태**다 — 1루프는 계약대로 세우고, 픽셀 · 문구는 E2E 뒤 2루프에서 잡는다.

| # | 무엇 |
|---|---|
| F-1 | 「시술 완료」 탭 귀가 대기 카드 ⋮ → 「귀가 대기 취소」 = 귀가 대기 직전 단계로 되돌림 + KOS `change-flow-step` · 카드가 판에 다시 앉음(규칙 35) |
| F-2 | `/board` 머리 오른쪽 탭 「시술순」 · 「방별순」(임시 이름) — 방별순 = `room.title` 문자열 오름차순 · 끌기 없음 · **서버 정렬 `GET /board?sort=room`** · 다시 그릴 때 탭 유지(규칙 36) |
| F-3 | 액션바 「의사 호출 · N건」 옆 「바로 시작 · N건」 — 선택한 준비중 줄 한 번에 시작 · KOS 집도의에 원장 없으면 **병원 시스템 계정을 KOS 집도의로**(`change-tasks-doctors` doctorIds=[시스템 계정] · 확인 `doctors_equal`) 쓰고 시작 · 수락 줄 거절 `task_not_waiting` · 귀가 대기 방문은 묶음 전체 409 · 일부 거절 = 코드마다 토스트 · `event_log` `task.quick_start` 1행(규칙 34). 단건 [시작] 의 `no_doctor` 는 그대로 |
| F-4 | 웹 OS 알림 — 서버 변경 없음 · 기존 `GET /api/notifications/stream`(`notification` 이벤트) + `GET /api/notifications` 를 **공통 틀(`base.html`)**에서 붙여 모든 화면에서 받음 · `document.hidden` 일 때만 · 첫 클릭 때 권한 · `tag` = 알림 행 id · 누르면 탭 앞으로 + `/board` · 원장 호출 알림만 |
| F-6 | `ui.chart_icons` — 작성된 차트만 파란(brand) 아이콘 · 미작성 안 그림 · 완료 줄 · 시술 완료 탭(규칙 37) |
| F-7 | 수락 대기 카드 [수락] — 로그인 계정이 `snapshot.doctors` 에 있으면 팝오버 없이 본인 수락 · 아니면 지금 팝오버(앱 SPEC-003 U-6 과 같음) |

## 3. 계약 (be ↔ fe — 이대로 제공 / 소비)

**be 가 제공 · fe 가 부른다** (`backend/day/services/board.py` · 이름은 이대로):

- `quick_start(session, current, visit_id: uuid.UUID, task_ids: list[uuid.UUID]) -> QuickStartResult` — `QuickStartResult` = `started: list[uuid.UUID]` · `rejected: list[tuple[uuid.UUID, str]]`(줄 id, 409 코드). 전부 거절이면 도메인 409(첫 거절 코드) · 귀가 대기 방문이면 줄 판정 전 묶음 전체 409 `visit_home` · 검증 실패(빈 목록 · 다른 카드 줄) = 기존 Validation 방식. dto 위치는 기존 관례(`day/dtos/board.py`).
- `undo_home(session, current, visit_id: uuid.UUID) -> None` — 귀가 대기(`procedure_done`) 방문만 · 아니면 409 `visit_not_home` · 방 없으면 409 `visit_not_home`.
- 정렬: 판 스냅샷을 만드는 기존 경로에 `sort: Literal["procedure", "room"] = "procedure"` 인자를 더한다(웹 판 · 조각이 쓰는 함수 — 앱 API 는 바꾸지 않는다 · 기본값이면 지금과 같은 결과). 어느 함수에 더했는지 리포트에 적는다.
- 거절 코드 글자: 새 코드가 없으면 기존 코드 글자 표를 쓴다. `visit_not_home` 글자는 비워 둔다(스펙).

**fe 가 짓는다** (`routers/board.py` 웹 · 템플릿 · static · styles):

- `POST /board/visits/{visit_id}/quick-start` (폼 `taskIds` 여러 개 · `board` edit) → `board.quick_start` · 판 조각 + 거절마다 토스트(oob `#day-toasts`).
- `POST /board/visits/{visit_id}/undo-home` (`board` edit) → `board.undo_home` · 판 조각.
- `GET /board?sort=room` — `sort` 를 받아 스냅샷에 넘김 · 탭 링크 · SSE 로 다시 받는 `hx-get`(`templates/board.html:10`) · 판 조각을 돌려주는 조작 응답이 같은 `sort` 를 유지.

**재검수 review-doc-2 반영(코디 2026-11-17 — 스펙보다 이 줄이 우선 · 스펙은 뒤에 맞춘다)**

- **D1 귀가 대기 취소 웹 응답 = 판 전체 다시 받기.** 지금 조작 응답 `_after`(`routers/board.py:223-254`) → `partials/board_action.html` 은 `#card-{id}` 를 OOB 로 바꾸거나 지울 뿐이라 판에 없는 카드를 넣지 못하고, `X-Day-Version` 때문에 `day.js`(:36-37 · :565)가 자기 조작의 `board` 신호를 건너뛴다. → undo-home 응답은 `X-Day-Version` 을 싣지 않고 판 다시 받기를 일으키거나(`HX-Trigger` 등), `#board-main` 을 지금 `sort` 로 다시 그린다 — 방식은 fe 가 고르고 리포트에 적는다. 바로 시작(카드가 이미 판에 있음)은 기존 `_after` 그대로.
- **`sort` 는 `GET /board` 쿼리로만 다닌다** — 조작 POST 폼 칸에 넣지 마라(`_fields` :188-199 가 모르는 칸 → 400). 「조작 응답이 sort 를 싣는다」는 판 전체를 다시 그리는 응답에만 해당.
- **D2** `#board-main` 의 SSE 다시 받기는 `hx-get="/board"` + `hx-params="none"`(`board.html:10`) — 판을 그릴 때 `hx-get` 속성에 지금 `sort` 를 박는다(`/board?sort=room`). 탭 = `/board?sort=room` · `/board` 로 이동하는 링크.
- **D5** 공통 틀 알림 스트림 때문에 `/board` 탭이 SSE 를 둘 연다 — 리포트 「E2E 에서 만날 자리」에 적어라(탭 여러 개).

## 4. 먼저 읽을 핵심 파일

- `backend/day/services/board_rules.py` — `start_block` :280-292 · `kos_doctor` :142 · `is_listed_doctor` :138 · 카드 순서(규칙 18 · `board_card_order`) · 스냅샷 조립 :795 · :868
- `backend/day/services/board.py` — `_system_account` :225 · `call` :581(시스템 계정 담당자 쓰기 :556) · `accept` :694(`change-tasks-doctors` :736-750) · `start` :807-851(`_prestart_doctor_chart` :829-834 · 첫 시작 `change-flow-step`) · `home` :948-985
- `backend/day/emr/kos/writes.py` :10-29 · :145-169(doctors · flow-step 확인 조건 · `doctors_equal` :154-161)
- `backend/day/queries/board.py` · `backend/day/dtos/board.py` · `backend/day/models/visit.py`(flow_step · visit_flow_log)
- 테스트: `backend/tests/day/board/` (test_board_rules · test_board_api · 서비스 테스트 관례)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/ (frontend 몫 — backend/day/routers/(api 제외) · templates/ · static/ · styles/ — 제외) 중 브리프가 지정한 곳`
- `pyproject.toml · uv.lock (의존성 추가가 브리프에 있을 때만)`
- `deploy/ · scripts/ (브리프가 지정할 때만)`

## 6. 구현 단계

1. **F-3 `quick_start`** — 규칙 34 · KOS 쓰기 표 · 검사 순서(:742) 그대로. 줄마다 판정: 준비중(`ready_wait`) 아님 → `task_not_waiting`(수락 줄 포함) · 호출 중 줄 → 기존 코드 · KOS 집도의에 원장 있으면 기존 [시작]과 같은 쓰기 · 없으면 outbox 에 `change-tasks-doctors`(doctorIds=[시스템 계정 KOS id] · 확인 `doctors_equal`) 먼저 → 기존 [시작] 쓰기(첫 시작 `change-flow-step` · 시술 전 의사차트 글은 지금 경로 그대로 — OQ-65 ⓐ). 시스템 계정 KOS id 가 없으면 그 줄 409 `conflict`(OQ-66 ⓒ). 한 transaction · `event_log` `task.quick_start` 1행. DAY 쪽 집도의(`visit_task_staff`) 기록은 스펙대로.
2. **F-1 `undo_home`** — 규칙 35 그대로: 직전 단계 = `visit_flow_log` 에서 귀가 대기 바로 앞 단계 · `flow_step` 되돌림 + `visit_flow_log`(source day · actor) + outbox KOS `change-flow-step(그 단계)` · 마취 · 「방 배정」 되살리지 않음 · 카드 자리 규칙 18 · `event_log` `visit.undo_home` 1행.
3. **F-2 정렬** — §3 대로 `sort` 인자. `room` 이면 `room.title` 문자열 오름차순 · 같은 이름은 시술순 순서 · `board_card_order` 를 쓰지 않음.
4. 단건 [시작] · 앱 API(`routers/api/`) 동작은 바꾸지 않는다 — 회귀 테스트로 확인.
5. 테스트 — 위 셋 각각: 성공 · 거절 코드 · 일부 거절 · 시스템 계정 경로 · outbox 순서 · event_log 1행 · sort 기본값 = 지금 순서.

## 7. 범위 제약 — 하지 말 것

- `backend/day/routers/`(api 제외) · `templates/` · `static/` · `styles/` · `app/` 수정 금지(frontend 몫 / 앱 범위 밖). migration 금지(스펙: 칸 변경 없음).
- 앱 API 응답 모양 변경 금지. F-4 · F-6 · F-7 은 서버 변경 없음 — 손대지 마라.
- 커밋 · push · PR 금지. 사용자 포트 · 프로세스 · 로컬 스택(`day-local` 등) 금지. KOS 실호출 금지(테스트는 기존 가짜 · outbox 단언).

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/be-1-report.md` — 변경 파일 · 계약 준수(§3 이름 · 시그니처) · 테스트 명령과 수치 · 상대 몫으로 넘긴 것 · 사용자가 E2E 에서 만날 자리.
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_94fbe396-828d-4fa4-8bd8-829294f10614 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
