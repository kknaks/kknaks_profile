# [frontend] fix-feedback — 웹 화면 F-1 · F-2 · F-3 · F-4 · F-6 · F-7
# [frontend] <한 줄 제목>

너는 **day `frontend` 워커**다. 너는 앞 맥락이 없다 — 아래 파일이 전부다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **backend 워커가 같은 워크트리에서 동시에 작업한다** — 서로의 파일을 건드리지 마라. 계약(§3)이 둘 사이의 경계다. 상대 몫이 필요하면 고치지 말고 리포트에 「backend 몫」으로 적어라.

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

- `backend/day/routers/board.py` — `board_page` :260-267 · 조작 라우트 · `TASK_ACTIONS` :646-666 · `call` :475 · `accept` :502 · `home` :670
- `backend/day/templates/board.html` :4-17(SSE · `hx-get="/board"` :10) · `templates/base.html` :68-70(`#day-toasts`) · `templates/ui.html` :258-260(`chart_icons`) · :280 · :287(체크) · :290
- `templates/partials/board_parts.html` — :17-22 · :74-75 · :96-97 · :226-228(수락 버튼) · :241(시술 완료 탭) · 액션바(「의사 호출 · N건」) · 귀가 대기 배지(`day-badge--going-wait`) · ⋮ 더보기(`.day-proc__more`)
- `templates/partials/board_regions.html` :55-60(원장 팝오버 · `me_listed`)
- `backend/day/static/day.js`(토스트 :723 · 선택 · 액션바 N) · `backend/day/styles/app.css` · CSS 빌드 방법은 AGENTS.md
- 알림: `routers/api/notifications.py`(스트림 · 목록 — 웹 쿠키 세션 받음) · `services/notification_events.py`(이벤트 `notification` · 읽기만)
- 앱 F-7 기준(읽기만): `app/lib/ui/accept.dart:34-37`
- 화면 테스트: `backend/tests/day/` 의 `test_board_page.py`(:98 · :138-148 · :281 · :723) · `test_screen_copy.py`(:126-127)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/day/routers/ (api/ 제외) · backend/day/templates/ · backend/day/static/ · backend/day/styles/ 중 브리프가 지정한 곳`
- `backend/tests/day/ 의 화면 테스트`

## 6. 구현 단계

1. **F-6** `ui.chart_icons` — off 아이콘을 그리지 않음(둘 다 없으면 `day-proc__icons` 칸 생략). 키트 견본(`kit_page.html` 등)도 같은 규칙.
2. **F-7** 수락 버튼 — `me_listed`(로그인 staff 가 `snapshot.doctors` 에 있음)면 팝오버 없이 `hx-post …/accept` + `doctorStaffId=본인` · 아니면 지금 팝오버. 글자 「수락」 그대로.
3. **F-2** 정렬 탭 — 머리(`day-page-head`) 오른쪽 끝 탭 「시술순」 · 「방별순」 · `?sort=room` · 방별순에서는 끌기 손잡이 · 순서 저장 없음 · SSE `hx-get` · 조작 응답 · 판 조각이 현재 `sort` 를 유지.
4. **F-3** 액션바 — 「의사 호출 · N건」 옆 「바로 시작 · N건」(N = 선택 중 준비중 줄 수 · 0 이면 disabled) → `POST /board/visits/{id}/quick-start`(§3) · 거절마다 토스트(기존 코드 글자).
5. **F-1** 귀가 대기 카드 ⋮ → 「귀가 대기 취소」 → `POST /board/visits/{id}/undo-home`(§3) · 확인 창 · 성공 토스트 없음.
6. **F-4** `base.html` 에서 알림 스트림을 붙인다(로그인 화면 제외 · 인라인 스크립트 금지 — `static/` JS) · `notification` 이벤트가 오면 `GET /api/notifications` 로 새 원장 호출 행을 받아 `document.hidden` 일 때만 `new Notification(제목, {body, tag: 행 id})` · 권한은 첫 클릭 때 `Notification.requestPermission()` · 거절이면 아무것도 안 함 · 클릭 → `window.focus()` + `/board`. 알림 제목 · 본문은 SPEC-005 기존 글자(서버 행 값). 이미 띄운 행은 다시 안 띄움 · 끊긴 동안 생긴 것도 안 띄움(N13). `/board` 의 기존 SSE 와 충돌 없게.
7. 화면 테스트 — 위 각각 TestClient 렌더 단언(아이콘 off 없음 · 원장 계정 수락 버튼 팝오버 없음 · 탭 · sort 유지 · 바로 시작 버튼 · ⋮ 귀가 대기 취소). be 서비스가 아직 없으면 라우트 테스트는 서비스 가짜로 · 리포트에 적어라.

## 7. 범위 제약 — 하지 말 것

- `backend/day/services/` · `queries/` · `emr/` · `models/` · `routers/api/` · `app/` 수정 금지(backend 몫 / 범위 밖). 서비스 함수는 §3 이름 · 시그니처 그대로 부른다 — 다르면 리포트에.
- 화면 글자 발명 금지 — 허용: 「귀가 대기 취소」 · 「시술순」 · 「방별순」 · 「바로 시작 · N건」 · 「의사 호출 · N건」 · 「수락」 + 기존 글자. 손 CSS 0 · 인라인 스크립트 0(grep).
- 커밋 · push · PR 금지. 사용자 포트 · 프로세스 · 로컬 스택 금지.

## 8. 검증

```
uv run pytest -q <네가 만든 화면 테스트만>(TestClient 로 전체 페이지 · HX 조각 렌더 확인) — 1회. CSS 를 다시 빌드했다면 빌드 명령 1회. 인라인 스크립트 0 · 손 CSS 0(grep). 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fe-1-report.md` — 변경 파일 · 계약 준수(§3 이름 · 시그니처) · 테스트 명령과 수치 · 상대 몫으로 넘긴 것 · 사용자가 E2E 에서 만날 자리.
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
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
