# fix-feedback frontend 1루프 결과 보고 — F-1 · F-2 · F-3 · F-4 · F-6 · F-7

## 상태: done (커밋 · push · PR 없음 — 워크트리 `CENTURION_DAY/fix-feedback` 에 변경만)

## 수행 — 변경 파일

| 파일 | 무엇 |
|---|---|
| `backend/day/routers/board.py` | `GET /board` 쿼리 `sort`(room = 방별순 · 그 밖 = 시술순) → `board.board(..., sort=)` · `sort` 를 템플릿에 · `POST /board/visits/{id}/quick-start`(폼 `taskIds`) · `POST /board/visits/{id}/undo-home` · `_after(..., toasts=)`(거절 코드마다 토스트) · `message_of(code)` · `UNSET_MESSAGES` 에 `visit_not_home` · 머리 조각 계약 표 갱신 |
| `templates/ui.html` | F-6 `chart_icons` — 작성된 차트만 brand 아이콘 · 미작성 안 그림 · 둘 다 없으면 `day-proc__icons` 칸 생략 · `check_item(quick=)` → 준비중 체크에 `data-day-quick` |
| `templates/partials/board_parts.html` | F-2 방별순이면 손잡이(grip) 없음 · F-3 액션바 「바로 시작 · N건」 버튼 · F-7 원장 계정 [수락] = 팝오버 없이 `hx-post …/accept` + `hx-vals doctorStaffId=본인` · F-1 「귀가 대기」 카드 ⋮(`.day-proc__more`) + 메뉴 「귀가 대기 취소」 |
| `templates/partials/board_regions.html` | F-7 원장 계정이면 수락 팝오버를 그리지 않음 · 대리 수락 기본 선택에서 「본인」 갈래 뺌(지정 호출이면 지정 원장 · 아니면 없음) |
| `templates/partials/board_main.html` | F-2 머리 오른쪽 정렬 탭(`day-seg` 링크 「시술순」 `/board` · 「방별순」 `/board?sort=room` · `aria-current`) · 방별순이면 판 form 에 `data-day-sort` · `hx-put /board/order` 없음 |
| `templates/partials/board_action.html` | `toasts` → `ui.toast_oob(…, "error")` |
| `templates/board.html` | `#board-main` `hx-get="/board{?sort=room}"` (코디 D2) · `hx-trigger="sse:board, day:board-refresh from:body"` (D1) |
| `templates/base.html` | F-4 로그인 세션이 있을 때만 `body[data-day-notify="/api/notifications"]` |
| `static/day.js` | F-3 「바로 시작」 N(고른 `data-day-quick` 수) · 0 이면 disabled · `[data-day-clear-checks]` 를 form 밖 버튼에도 · F-4 OS 알림 모듈(`startNotify`) |
| `styles/app.css` → `static/day.css`(빌드) | 링크형 `a.day-seg__item` · `aria-current` 선택 모양 · 방별순 판(`.day-board__grid:not([data-day-sort])`)에서 `.day-grip` 숨김 |
| `tests/day/web/test_board_page.py` | 새 테스트 8 + 기존 3 개 갱신(아래) |
| `tests/architecture/test_screen_copy.py` | 근거 표에 「시술순」 「방별순」 「바로 시작 ·」 「귀가 대기 취소」 · 숨은 글자 「정렬」 「간호관리차트 있음」 「의사차트 있음」(「있음」 「없음」 단독 항목 → 대체). ※ 브리프 allowed_paths 는 `tests/day/` 화면 테스트지만 브리프 §4 가 이 파일(:126-127)을 지목했고 문구 근거 표라 함께 고쳤다 |

### 기능별 구현

- **F-6** 키트 견본(`kit_page.html`)은 같은 매크로라 자동으로 같은 규칙(`chart_icons(false,false)` 는 이제 아무것도 안 그림). 키트 아이콘 팔레트(`square-pen disabled` 등)는 아이콘 견본이라 그대로.
- **F-7** 판정 = 세션 `staff_id` 가 `snapshot.doctors[].staffId` 에 있음(`board_regions` 의 기존 `me_listed` 와 같은 식). 글자 「수락」 그대로.
- **F-2** 탭은 전체 페이지 이동 링크(기억 안 함 — 새로 열면 시술순). SSE 다시 받기 · D1 다시 받기는 `#board-main` 의 `hx-get` 에 박힌 sort 를 쓴다. 조작 POST 는 sort 를 싣지 않는다(폼 칸 400 그대로 — 테스트로 확인). 조작 응답(OOB `_after`)은 sort 를 모르므로 카드 안쪽을 다시 그릴 때 손잡이가 생길 수 있어 **CSS 로 방별순 판의 손잡이를 숨긴다** — 끌기 자체는 판 form 에 `data-day-sort` 가 없어 day.js 가 시작하지 않는다(키보드도 같음).
- **F-3** 버튼 = `hx-post …/quick-start` · `hx-include="[data-day-quick='{방문}']"`(체크된 것만) · `hx-params="taskIds"` · 성공(<300)이면 그 카드 체크를 푼다. 응답 = 기존 `_after`(그 카드 OOB + `X-Day-Version` — `QuickStartResult` 가 `ActionResult` 를 상속해 version 이 실림) + 거절 **코드마다** 토스트 1장(중복 코드 1장 · 순서 유지 · 글자 = 기존 MESSAGES · 글자 미정 코드는 토스트 없음 · 모르는 코드(`conflict` 등)는 `invalid_request` 글자 — `web_errors.board_error_handler` 와 같은 규칙). 전부 거절 · `visit_home` · 400 은 서비스 예외 → 기존 오류 토스트 경로.
- **F-1** ⋮ → 메뉴 줄이 바로 `hx-post …/undo-home`. **확인 창 없음 · 성공 토스트 없음**(SPEC-002 U-9 · 규칙 35 · OQ-58 ⓔ 「확인 창 없음」을 따랐다 — 브리프 §6-5 「확인 창 · 성공 토스트 없음」을 둘 다 없음으로 읽음. 확인 창이 필요하면 `ui.confirm_modal` 한 줄로 바꿀 수 있다). **D1 방식 = 응답 본문 없음 + `HX-Trigger: day:board-refresh` + `HX-Reswap: none` + `X-Day-Action: 1`(열린 메뉴 닫기) · `X-Day-Version` 없음** → `#board-main` 이 지금 sort 로 판 전체를 다시 받는다(메뉴가 열려 있는 순간에 오면 day.js 기존 미루기로 메뉴 닫힌 직후 받음). 거절 `visit_not_home` = 409 · 토스트 글자 비움.
- **F-4** `day.js` `startNotify()` — `EventSource('/api/notifications/stream')`(웹 쿠키 세션) · 붙을 때마다(`open` — 재연결 포함) `GET /api/notifications` 목록 id 를 「본 것」으로(끊긴 동안 생긴 것 안 띄움 · N13) · `notification {unread}` 가 **늘었을 때만** 목록을 다시 받아 안 본 `kind == "doctor_call"` · 안 읽은 행을 `document.hidden` 이고 권한 granted 일 때 `new Notification(title, {body, tag: 행 id})` · 권한은 첫 클릭 때 1회 `requestPermission()`(거절이면 아무것도 안 함 · 안내 글자 없음) · 누르면 `window.focus()` + `/board` 가 아니면 `/board` 로 이동 · 읽음 처리 없음 · `session_expired` 면 스트림 닫음. 서버 변경 없음.

## 검증

- `uv run pytest -q -m "not infra" backend/tests/day/web backend/tests/architecture` → **131 passed**(화면 테스트 · 경계 · 문구 · CSS 지문)
- 확인 겸 `uv run pytest -q -m "not infra"` 전체 → **948 passed, 333 deselected**(backend 워커의 새 테스트 포함)
- `scripts/build-css.sh` 1회 → `day.css 55.2KB` (지문 테스트 통과)
- `uv run ruff check backend/day/routers backend/tests/day/web backend/tests/architecture` → All checks passed · `ruff format --check` 변경 없음
- `node --check backend/day/static/day.js` OK
- 인라인 스크립트 0(`grep "<script"` 은 전부 `src=`) · `style="` 0
- **pending**: infra(실 PostgreSQL) 테스트 — 로컬 스택을 띄우지 않았다(브리프 금지). `tests/day/board/test_board_api.py:727` 은 로그인 계정이 간호라 F-7 영향 없음을 코드로 확인.

### 새 · 바꾼 화면 테스트 (`tests/day/web/test_board_page.py`)

새: `test_차트_아이콘은_작성된_차트만_파랑_미작성은_그리지_않는다` · `test_보는_사람이_원장이면_수락은_팝오버_없이_본인` · `test_원장이_아니면_수락은_원장_골라_대리_수락_기본_선택_없음` · `test_정렬_탭은_머리_오른쪽_링크_GET_board_sort_room`(실 라우트 · sort 전달 · hx-get · 손잡이) · `test_바로_시작_버튼은_의사_호출_옆_준비중_줄만_센다` · `test_바로_시작_라우트는_서비스_결과로_카드_조각과_거절_토스트`(코드마다 1장 · version 헤더 · sort 폼 칸 400) · `test_귀가_대기_카드만_더보기_귀가_대기_취소` · `test_귀가_대기_취소_라우트는_판_전체를_지금_sort_로_다시_받게`(HX-Trigger · X-Day-Version 없음 · visit_not_home 토스트 없음) · `test_웹_원장_호출_OS_알림은_공통_틀에서_로그인_뒤만`.
바꿈: 셸 테스트의 `day-seg` 부재 단언(→ 보기 바꾸기 tablist 부재) · 원장 수락 기본 선택 테스트(→ F-7) · clear-checks 셀렉터 · 「메뉴에서 바로 보내지 않는다」(귀가 대기 취소만 예외).
라우트 테스트는 **서비스를 가짜로**(`services.board.board` · `quick_start` · `undo_home` · `_allowed` · `sessions.grants` · `db` 의존성) — DB 없이 라우트 · 조각 계약만 본다. 서비스 자체는 backend 몫 테스트.

## 계약 대조 (§3)

| 항목 | 결과 |
|---|---|
| `quick_start(session, current, visit_id, task_ids)` | 같음 — backend 는 `now: datetime | None = None` 을 덧붙였고 라우트는 `_now()` 를 넘긴다. 반환 `QuickStartResult(ActionResult)` · `started` · `rejected: list[(uuid, code)]` 사용 |
| `undo_home(session, current, visit_id)` | 같음 (+ 선택 인자 `now` 넘김). 반환 `ActionResult` 는 쓰지 않음(D1 — version 안 실음) |
| `sort` 인자 | backend 가 **`services.board.board(..., sort: BoardSort = "procedure")`** 에 더함(`BoardSort` = `services/board_rules.py:41`). 라우트는 `GET /board` 에서만 넘긴다 · 조작 응답 `_after` 는 기본값 |
| 웹 경로 | `POST /board/visits/{id}/quick-start`(폼 `taskIds` 여럿 · board edit) · `POST /board/visits/{id}/undo-home`(board edit · 칸 없음) · `GET /board?sort=room` — 브리프 그대로 |
| 화면 글자 | 새 글자 = 「귀가 대기 취소」 「시술순」 「방별순」 「바로 시작 · N건」 + 숨은 aria 「정렬」 「간호관리차트 있음」 「의사차트 있음」(기존 aria 글자에서 「없음」 갈래만 뺀 것) · ⋮ aria-label = 「{고객} 더보기」(기존 「더보기」) |
| SPEC-002 §3 「귀가 대기 취소 응답 = 판 조각 + 시술 완료 탭 OOB」 | **다름(코디 D1 우선)** — 판 전체 다시 받기로 구현 |

## 상대 몫 · 코디가 확인할 것

- (backend 몫 아님 · 참고) `web_errors.py` 의 토스트 글자 규칙과 `routers/board.py` `message_of` 가 같은 규칙을 두 군데 둔다 — `web_errors.py` 는 allowed_paths 밖이라 손대지 않음. 정리하려면 `web_errors.board_error_handler` 가 `message_of` 를 쓰면 된다.
- `conflict`(시스템 계정 KOS id 없음 · OQ-66) 거절 토스트는 MESSAGES 에 없어 「요청이 올바르지 않습니다」(invalid_request 글자)로 나온다 — 기존 일반 처리. 글자가 필요하면 스펙/사용자 결정.
- 확인 창 해석(F-1) — 위 「F-1」 참고.
- 고객 검색 조각(`GET /board/search`)은 권한 값을 넘기지 않아 view 권한 계정에도 ⋮ 가 그려진다(누르면 403 토스트) — 기존 검색 조각의 다른 버튼과 같은 동작.

## 사용자가 E2E 에서 만날 자리

1. **F-4 SSE 두 개(D5)** — `/board` 탭은 판 스트림(`/board/stream`)과 알림 스트림(`/api/notifications/stream`)을 **둘 다** 연다. HTTP/1.1 이면 브라우저가 한 origin 에 연결 6개까지라 **DAY 탭을 3개 넘게 열면** 요청이 막힐 수 있다(로컬 `uvicorn` 직접 접속 시 · Caddy HTTP/2 뒤에서는 해당 없음).
2. **F-4 권한 창** — 로그인 뒤 **아무 데나 처음 클릭할 때** 브라우저 알림 권한을 묻는다. 거절하면 이후 아무 안내 없음(브라우저 설정에서 다시 켜야 함). 알림은 DAY 탭이 **뒤에 있을 때만** 뜨고, **원장 목록 계정**으로 로그인한 웹에만 뜬다(간호 계정엔 원장 호출 행이 없음). macOS 는 브라우저 자체의 시스템 알림 허용도 필요.
3. **F-4** 알림을 눌러도 읽음 처리 안 됨 · 스트림이 끊긴 동안 생긴 호출은 다시 붙어도 안 뜸(기본값).
4. **F-2** 방별순은 URL `?sort=room` 이라 새로 고침하면 방별순이 유지된다(「새로 열면 시술순」 = 메뉴/주소로 `/board` 로 들어올 때). 탭 모양은 기존 세그먼트(`day-seg`, 164px) 재사용 — 픽셀은 2루프.
5. **F-3** 「바로 시작 · N건」은 준비중 줄을 고를 때만 켜진다(호출 중 줄만 고르면 꺼진 채). 시작 뒤 그 카드 체크가 풀린다. 일부 거절이면 코드마다 빨간 토스트.
6. **F-1** ⋮ → 「귀가 대기 취소」는 **확인 창 없이 바로** 실행 → 판 전체가 다시 그려지며 카드가 판에 돌아온다(KOS `change-flow-step` 반영은 backend · E2E 확인 대상).
7. **F-7** 원장 계정으로 로그인하면 수락 대기 카드의 [수락]이 팝오버 없이 바로 본인 수락. 간호 계정은 지금처럼 팝오버(기본 선택: 지정 호출이면 지정 원장 · 아니면 없음 — 예전 「보는 사람이 원장이면 본인」 기본 선택 갈래는 사라짐).
