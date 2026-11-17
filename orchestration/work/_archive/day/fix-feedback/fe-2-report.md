# fix-feedback frontend 2루프 결과 보고 — F-5 ⋮ · E3 간호관리 · E6 차트 여는 곳 · E5 · W2 · E2

## 상태: done (커밋 · push · PR 없음 — 워크트리 `CENTURION_DAY/fix-feedback` 1루프 미커밋 위에 변경만)

## 변경 파일 (fe 몫만 — be 파일 손대지 않음)

| 파일 | 무엇 |
|---|---|
| `backend/day/routers/board.py` | `TASK_ACTIONS["cancel-call"] = board.cancel_call` → `POST /board/tasks/{task_id}/cancel-call`(기존 `task_action` 경로 · `board` edit · 응답 = 같은 `_after` 카드 OOB + 함께 맞출 조각 + `X-Day-Version`) · `UNSET_MESSAGES` 에 `task_not_called`(토스트 글자 비움 · :782) |
| `templates/partials/board_parts.html` | `proc()` — ① 호출(수락 전 · `t.state == "called"` + `t.call`) 줄에 ⋮ · 준비중 · 수락 줄 ⋮ 없음(진행중 · 완료 그대로) ② `t.systemDoctor` → 원장 글자 「간호관리」 · `doctor_pop` 조건 `t.doctor or t.systemDoctor` ③ 줄의 `data-day-row-get` 제거 → `chart_url`. `proc_menu()` — 호출 줄 메뉴 「호출 취소」(확인 창 없이 바로 `hx-post …/cancel-call`) · 원장 변경 팝오버도 `systemDoctor` 줄에 그림. `done_card()` — 줄 전체 `button.day-linkrow` → `span.day-linkrow` + 이름만 버튼 |
| `templates/ui.html` | 새 매크로 `chart_name(name, url, cls)` — 이름 버튼(`day-proc__doc` 와 같은 호버 · `data-tip="차트 작성"` · `aria-label="{시술} 차트 작성"` · `data-day-row-get`) · `proc_row` 두 갈래가 이 매크로로 이름을 그림(`chart_url` 없으면 지금처럼 span — 키트 견본) |
| `static/day.js` | 차트: `rowGet` 이 INTERACTIVE 거르기 없이 `[data-day-row-get]`(이제 이름 버튼에만) · F18 settling 막기 그대로. E5: `show` 의 `document.hidden` 조건 제거(권한 granted 만). W2: `lastUnread`/`grew` 제거 — 신호마다 목록을 받아 `seen` 으로만 거름 · `ready` 플래그(붙을 때 `prime` 실패면 다음 목록은 `markSeen` 만 · 띄우지 않음) |
| `styles/app.css` → `static/day.css`(빌드) | E2: `.day-opt { position: relative }` · `.day-pick { overflow: clip }`(hidden 뒤 덮어씀) · E6: `.day-proc__chart { min-width:0; text-align:left }` · `span.day-linkrow:hover { background:none }` · `.day-linkrow__name.day-proc__chart { flex: 0 1 auto }` |
| `tests/day/web/test_board_page.py` | 새 7 · 기존 4 갱신(아래) |
| `tests/architecture/test_screen_copy.py` | 근거 표에 「호출 취소」 「간호관리」 「차트 작성」(허용 새 글자 3개 그대로) |

새 화면 글자 = 「호출 취소」 · 「간호관리」 · 「차트 작성」만 + 숨은 aria 「{시술} 차트 작성」 · 「간호관리 원장 변경」(기존 「{원장} 원장 변경」 틀 그대로).

## E2 원인 (의사 호출 팝오버 위가 잘리고 아래가 빔)

- **원인 확정(코드)**: 원장 줄의 숨긴 라디오 `.day-opt__radio` 가 `position: absolute` 인데 줄(`.day-opt`)이 positioned 가 아니라 **기준(containing block)이 팝오버 `.day-pop`(fixed)** 였다. 그래서 라디오는 목록(`.day-call__list` · overflow-y:auto)의 스크롤에 안 갇히고, 팝오버 기준으로 「목록을 펼쳤을 때의 자리」 = 아래쪽 원장이면 **팝오버 바닥 밖**에 놓인다. 라벨을 누르면 브라우저가 라디오에 포커스를 주며 보이게 스크롤하는데, 그 대상이 `overflow: hidden` 인 **팝오버 자체**(`.day-pick` — hidden 은 프로그램 스크롤이 된다)라 팝오버 내용 전체가 위로 밀림 → 제목 · 검색 · 추천 · 「선택됨」이 잘리고 [호출] 밑이 빔. 사용자 스크린샷(맨 아래 「이건학 · A-룸4 시작 대기」 고름)과 맞음. 가설이던 `scrollIntoView` 호출은 day.js 에 이 경로로 없음(togglePop 은 검색칸에 포커스 — 위쪽이라 무해).
- **고침**: `.day-opt { position: relative }`(라디오가 그 줄 · 목록 스크롤 안에 있음 → 목록만 스크롤) + `.day-pick { overflow: clip }`(팝오버 자체는 어떤 경우에도 스크롤 안 됨 · 이중 안전). 같은 `.day-opt` + `.day-pick` 를 쓰는 **차트 담당자 고르기 · 방 옮기기 · 수락 · 원장 변경 팝오버도 같이 고쳐짐**.
- **1루프 전부터 있던 버그**: dev `4f8316a7` 의 `app.css` 에 같은 규칙(`.day-opt` 기준 없음 · `.day-opt__radio` absolute · `.day-pick` overflow hidden) — 1루프 변경 때문이 아님.
- 브라우저 실측은 못 함(사용자 포트 · 로컬 스택 금지) — CSS 단언 테스트만. E2E 에서 확인 필요.

## 계약 대조

| 항목 | 결과 |
|---|---|
| `board.cancel_call(session, current, task_id, now=None) -> ActionResult` | be 가 이 이름 · 시그니처로 넣었음(`services/board.py:774`) — 라우트가 그대로 부름(`TASK_ACTIONS`) |
| 웹 `POST /board/tasks/{task_id}/cancel-call` · 응답 `_after` | 같음 — 카드 OOB + 인박스 · 창 OOB + `X-Day-Version` · 판 전체 다시 받지 않음(`HX-Trigger` 없음) |
| 스냅샷 `tasks[].systemDoctor` | be `board_rules.py:799`(`system_doctor` — 담당 원장 있으면 false) — 템플릿은 `t.doctor` 먼저 · 없으면 `systemDoctor` 로 「간호관리」 |
| 거절 | `task_not_called` 토스트 비움 · `call_already_accepted` = 기존 「다른 원장이 먼저 받았습니다」 · `visit_home` 등 기존 |

## 검증

- `uv run pytest -q -m "not infra" backend/tests/day/web backend/tests/architecture` → **138 passed**(1루프 131 + 새 7)
- 확인 겸 `uv run pytest -q -m "not infra"` 전체 → **958 passed, 339 deselected**(be 2루프 테스트 포함)
- `scripts/build-css.sh` 1회 → `day.css 55.4KB`(CSS 지문 테스트 통과)
- `uv run ruff check backend` → All checks passed · `ruff format` 적용(내 파일 3개)
- `node --check backend/day/static/day.js` OK
- 인라인 스크립트 0(`<script` 은 전부 `src=`) · `style="` 0
- pending: infra(실 PostgreSQL) — 로컬 스택 금지. 브라우저 동작(E2 팝오버 · 툴팁 · OS 알림)은 E2E

### 새 · 바꾼 화면 테스트
새: `test_더보기는_호출_진행중_완료_줄만_준비중_수락_줄은_없다` · `test_조작_권한이_없으면_호출_줄에도_더보기가_없다` · `test_호출_취소_라우트는_다른_줄_조작과_같은_카드_조각`(`TASK_ACTIONS` 가 `board.cancel_call` 인지 단언 뒤 가짜로 — 200 OOB · version · 409 `task_not_called` 토스트 없음 · `call_already_accepted` 글자) · `test_시스템_계정_집도의_줄은_간호관리_원장_변경은_원장_줄과_같다`(진행 「간호관리 · 진행 mm:ss」 + 툴팁 · 팝오버 · 완료 「간호관리 · n분」 · systemDoctor 없으면 그대로) · `test_차트는_시술_이름_글자만_열고_호버는_차트_작성`(판 줄 5상태 · 시술 완료 탭 · day.js) · `test_웹_OS_알림은_신호마다_목록을_받아_본_것으로만_거른다` · `test_의사_호출_팝오버는_통째로_스크롤되지_않는다`.
바꿈: 시술 완료 탭 차트(`hx-get` → `data-day-row-get` 2곳) · 「메뉴에서 바로 보내지 않는다」(호출 취소 예외 추가) · OS 알림(`document.hidden` 없음 단언으로 뒤집음).

## 판단 · 코디가 볼 것

- **호출 줄 ⋮ 조건** = `board` edit + `t.state == "called"` + `t.call` 있음. 서버 `canCancelCall` 같은 값은 스냅샷에 없어(be 계약에 없음) 상태로만 그림 — 동시 수락 등은 서버 409 로 막힘.
- **⋮ 메뉴 = 확인 창 없음 · 성공 토스트 없음** — 지시서 그대로(시작 취소 · 완료 취소는 기존 확인 창 그대로).
- **완료 줄 「간호관리 · n분」** 은 글자만(원장 변경 없음 — 완료 줄은 원래 원장 변경이 없음 · U-3 「수락 · 진행중 줄」).
- **차트 이름 버튼**은 `.day-proc__doc`(원장 이름 버튼)과 같은 클래스 → 같은 호버 배경 · 같은 툴팁 모양. 이름 말줄임 유지.
- 시술 완료 탭 줄 호버 배경(줄 전체 회색)은 없앴다 — 이제 이름 글자만 호버 배경.

## 사용자가 E2E 에서 만날 자리

1. **F-5 ⋮** — 호출(수락 전) 줄 오른쪽 ⋮ → 「호출 취소」 누르면 **확인 창 없이 바로** 그 줄 준비중 · 성공 토스트 없음. 준비중 · 수락 줄엔 ⋮ 없음. 이미 수락됐거나(동시) 호출이 아니면 409 — `call_already_accepted` 는 「다른 원장이 먼저 받았습니다」, `task_not_called` 는 토스트 없음(글자 미정). KOS 데스크에는 「호출」이 남음(규칙 38 — 감수).
2. **E3** — 「바로 시작」으로 시스템 계정 집도의 시작한 줄 = 「간호관리 · 진행 mm:ss」. 「간호관리」에 마우스 → 「원장 변경」 툴팁 · 누르면 원장 목록 → 고르면 그 원장 이름으로. 완료되면 「간호관리 · n분」(누를 수 없음).
3. **E6** — 차트는 **시술 이름 글자만** 연다(판 카드 · 시술 완료 탭) · 이름 호버 = 옅은 배경 + 「차트 작성」 툴팁. 체크박스 · 시간 칸 · 버튼 · ⋮ · 빈 자리는 안 열림. 시술 완료 탭 줄은 이제 줄 전체 호버 배경 없음.
4. **E5** — 웹 OS 알림이 **탭이 앞에 있어도** 뜬다(같은 탭에서 호출해도 · 다른 모니터여도). 같은 호출을 두 탭이 받으면 tag 가 같아 하나로 겹침.
5. **W2** — 이제 알림 신호마다 `GET /api/notifications` 를 받는다(읽음 신호에도 1번 · 요청 조금 늘어남). 붙을 때 첫 목록을 못 받았으면 그다음 신호 1회는 띄우지 않고 「본 것」으로만 채움.
6. **E2** — 의사 호출 팝오버에서 맨 아래 원장을 골라도 제목 · 검색 · 추천 · 「선택됨」이 그대로 보이고 목록 안에서만 스크롤되는지 확인(차트 담당자 · 방 옮기기 · 수락 · 원장 변경 팝오버도 같은 고침). `overflow: clip` 은 Chrome 90+ · Safari 16+ — 웨일(크롬 기반) OK.
7. (1루프 그대로) D5 — `/board` 탭 SSE 2개.
