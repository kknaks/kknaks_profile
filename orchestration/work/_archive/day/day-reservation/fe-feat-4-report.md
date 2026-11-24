# fe-feat-4 결과 보고 — 카드 폭 · 줄 접기 · 동행 그룹 끌어 놓기(E6 · E7)

## 상태: done — 실패 알림 꼴 하나는 코디 답 대기(아래 「코디가 볼 것」 1) · 커밋 0 · 스택 안 건드림

근거: 결정 R64 ~ R69 · `contract-v4-companion.md` · `research-companion-1-report.md` §4(G9 끌기 `static/day.js` · 폴링 미룸).
backend 는 아직 lane · line · rows · bands 를 안 싣는다(`presentation/reservations.py` 에 `stack_index` 그대로) — 화면은 계약 픽스처로 맞췄고,
옛 값(rows 없음)도 그린다(30분 한 줄 · lane 0).

## ① 카드 폭 · 자리(R64)
- 토큰 `--day-res-card-w: 140px`(183 → 140). day.js 기본값도 140.
- 카드 data: `data-day-res-lane` · `-line` · `-group`(companion_group_id · 없으면 빈 값). `data-day-res-stack` 없앰.
- 표 `data-day-res-rows="시작:끝:줄 수,…"`(계약 rows 그대로). day.js 가 행마다 높이 = lines × `--day-res-slot`(70px)으로 쌓는다(행 단위 분은 backend 가 정한 그대로 — 30분이 아니어도 됨).
  - 시각 → 세로 자리 = 그 행 안 비례(회색 면 · 현재 시각 선 · 처음 세로 위치).
  - 시간 글자(30분마다) 높이 = 그 30분이 차지하는 세로(접힌 행이면 140px).
  - 카드 top = (한 줄 행이면 지금처럼 시작 분 비례 · 접힌 행이면 행 top + line × 70) + 2 · left = 10 + lane × (140 + 4).
  - 카드 높이 = 끝 시각까지(최소 66). **접힌 행의 마지막 줄이 아니면 한 줄(66)** — 아래 줄 카드를 덮지 않게(아래 「코디가 볼 것」 2).
  - 열 폭 = 가장 많은 lane 수 × 140 + 사이 + 여백(5개면 730px).
- rows 가 비면(옛 조각) 30분 한 줄씩 — 지금과 같은 화면.

## ② 띠(R68)
- 열 안 `<div class="day-res-band" data-day-res-band=group_id data-day-res-start data-day-res-line data-day-res-lane-from data-day-res-lane-to aria-hidden="true">` · 글자 없음.
- 자리 = 그 줄 · 그 자리 구간(lane_from ~ lane_to **포함**으로 읽음)의 같은 그룹 카드를 감싸고 바깥 2px(`--day-res-band-pad`) · 높이 = 그 카드들 중 가장 긴 것.
- CSS = 토큰만: `--day-res-band-line: var(--ms-gray-500)`(1px 테두리 · 둥글기 6px) · `--day-res-drag-shadow`. 손 CSS 0(app.css → `scripts/build-css.sh`).

## ③ 끌어 놓기(R66 · R69)
- `companion_editable` 일 때만 표에 `is-companion` · `data-day-res-companion` + 숨은 폼 둘(`ui.write_attrs` · `hx-trigger="day:res-companion"` · target `#reservation-main` · innerHTML · `hx-push-url="false"`):
  - 묶기 `PUT /reservations/companions` — `visit_id`(끈 카드) · `target_visit_id`(놓은 카드)
  - 풀기 `PUT /reservations/companions/leave` — `visit_id`
- 카드 전체를 끈다(pointer · 4px 넘게 움직여야 끌기 — 그 전엔 툴팁 · 누름 그대로). 끄는 카드는 손을 따라오고(translate) `is-dragging`.
- 놓은 점 아래(`elementsFromPoint` — G9 와 같은 히트 테스트):
  - 다른 카드 → 묶기(조건 · 지난 날짜는 서버가 본다 — 화면은 다시 판정하지 않음)
  - 같은 카드만 · 자기 띠 안 빈 곳 · 표 밖 → 아무것도 안 함
  - 표 안 빈 곳(띠 밖) → 풀기(끈 카드에 그룹이 있을 때만)
- 놓으면 카드는 곧장 제자리. 성공 = 응답 조각이 `#reservation-main` 을 바꿈(스크롤 · 탭 · 칩 · 필터는 폴링과 같이 지킴). 실패 = 바꿔 끼우지 않음(카드 제자리) + 공통 X-Day-Error 규칙.
- 폴링 미룸: 끄는 동안의 회차는 건너뛰고, 끌기 전에 떠난 폴링 응답도 끼우지 않는다. 놓았는데 쓰기를 안 보냈으면 밀린 폴링을 바로 한 번.
- 순서: 묶기 · 풀기 요청은 날짜 바꾸기와 같은 세대(`createResOrder` 의 nav) — 떠 있는 동안 폴링 없음 · 그 전에 떠난 폴링 응답이 늦게 와도 쓰기 응답을 덮지 않는다.

## ④ 시험
- `scripts/frontend/tests/res-companion.test.mjs`(새 · 10개 · 진짜 htmx + day.js + 서버 렌더 고정본):
  1. 다른 카드 위 → 묶기 PUT(폼 값) · 손을 따라옴 · 응답 조각으로 교체 · 주소 줄 그대로
  2. 같은 카드 · 자기 띠 안 · 표 밖 · 그룹 없는 카드 빈 곳 → 요청 0 · 제자리
  3. 띠 밖 빈 곳 → 풀기 PUT(visit_id 만)
  4. 누르기만(4px 안) → 끌기 아님
  5. 실패 409 `companion_condition`(본문 없음) → 표 그대로 · 카드 제자리 · 폴링 계속
  6. 끄는 동안 폴링 미룸(회차 건너뜀 · 떠 있던 응답 안 끼움 · 놓으면 바로 한 번)
  7. 쓰기 떠 있는 동안 폴링 0 · 늦은 옛 폴링 응답이 쓰기 응답을 덮지 않음
  8. **6장 2줄 배치** — 10:00 6명: 다섯은 top 282 · left 10/154/298/442/586, 여섯째 top 352 · left 10 · 10:00 행 140px · 다른 열 11:00 카드 492(전 열 공통) · 열 폭 730
  9. 띠 = lane 0 ~ 1 감쌈(280 · 8 · 288 × 70) · 글자 없음
  10. companion_editable 아님 → 끌기 없음
- 변이 확인(되돌림): 폴링 미룸 제거 → 6 실패 · 쓰기를 nav 세대에서 뺌 → 7 실패 · line 자리 제거 → 8 실패 · rows 무시 → 8 실패 · 떠 있던 폴링 응답 끼움 → 6 실패.
- 화면 pytest `backend/tests/day/web/test_reservations_companion_screen.py`(새 · 3개 — 700줄 규칙으로 화면 시험 파일에서 나눔): rows 「시작:끝:줄 수」 · lane/line · rows 없는 옛 값 · 띠 마크업 · 두 폼(경로 · 칸 · target · push 끊음) · editable false = 끌기 · 폼 없음(띠는 보임).
- `test_reservations_screen.py`: 픽스처를 계약 v4 로(`stack_index` → lane · line · companion_group_id · rows · bands · companion_editable · 다음 날 = 국내 10:00 6명) · 시간 글자 · 「조각 안 타이머 없음」 단언을 새 마크업에 맞춤. 고정본 다시 씀.
- 받침 `res-dom.mjs`: `pointer()`(jsdom 에 PointerEvent 없음 → MouseEvent + pointerId) · `setUnder()`(elementsFromPoint). `res-debounce` · `res-order` 가짜 전역에 `resDrag` · `resPollMissed`.

## 검증
| 명령 | 결과 |
|---|---|
| `npm run check`(build --check · ESLint · Stylelint · Prettier · node test) | 통과 · node 126 pass |
| `./scripts/test.sh --pure backend/tests/day/web backend/tests/architecture` | 503 passed |
| ruff check · format(바꾼 시험) | 통과 |
| 새 마크업 인라인 `<script` · `<style` · ` style=` | 0(자리는 CSSOM) |

## 바꾼 파일
- `backend/day/templates/partials/reservations_parts.html`(card · board · 띠 · 폼) · `reservations_main.html`(board 인자)
- `backend/day/static/day.js`(resLayout rows · 띠 · 끌어 놓기 · 폴링 미룸 · 순서) · `backend/day/styles/app.css` → `static/day.css`
- `backend/tests/day/web/test_reservations_screen.py` · `test_reservations_companion_screen.py`(새)
- `scripts/frontend/tests/res-companion.test.mjs`(새) · `res-dom.mjs` · `res-debounce.test.mjs` · `res-order.test.mjs` · `fixtures/*.html`

## 코디가 볼 것
1. **실패 알림 꼴** — backend 가 `CompanionCondition` · `CompanionPastDate` 를 `notice_error_handler`(본문 없음)로 묶어 두었다. 그러면 공통 X-Day-Error 규칙이 끼울 oob 토스트가 없어 **알림이 안 뜬다**(카드 제자리만). 브리프 「기존 오류 알림」대로면 backend 가 `board_error_handler`(시술 현황과 같은 oob 토스트 · 글자는 MESSAGES · 없으면 빈 토스트) 쪽이어야 한다 — 화면은 둘 다 그대로 동작(시험 5 는 본문 없는 꼴로 돌림). ask 로 물어 둠.
2. **접힌 행의 긴 카드** — 6명 칸에서 첫 줄 카드가 30분보다 길면, 아래 줄 카드를 덮지 않게 한 줄 높이로 자른다(마지막 줄 카드만 끝 시각까지 늘어남). backend 의 line 판정이 긴 카드를 마지막 줄에 두면 자르지 않는다 — 원하는 모양이 다르면 알려 달라.
3. `bands.lane_to` 를 **포함**으로 읽었다(lane_from 0 · lane_to 1 = 두 칸). backend worker_done 의 예시와 다르면 한 줄 고침.
4. 키보드 끌기(G9 의 화살표 키)는 넣지 않았다 — 결정에 없음.
5. 실물 확인은 backend 가 rows · bands · lane · line 을 싣고 코디가 스택을 다시 띄운 뒤.

## 고침 1 — R70 · R71 (task_db680baef210)
- R70: 카드 높이 = 한 줄 고정(`--day-res-card-h` 66px) · top = 그 시간 행 top + line × 줄 높이(70) + 2 — 시작 분만큼 내리거나 끝 시각까지 늘이지 않는다(접히지 않은 행도). `day.js` resLayout 만 바꿈(쓰지 않게 된 끝 시각 읽기 제거). 위 「코디가 볼 것」 2 는 이것으로 닫힘.
- node 시험 11번 추가: 폴링 응답의 중화권 카드를 10:45 ~ 12:00 으로 바꿔도 top 422(10:30 행 · 10:00 행이 2줄) · 높이 66 · 모든 카드 66. 변이(끝 시각까지 늘림)로 8 · 9 · 11 실패 확인 후 되돌림.
- 화면 pytest: 높이 · 자리는 day.js 몫이라 마크업 변경 없음 — 그대로 통과.
- R71 실패 알림 = backend oob 토스트(board_error_handler) — 화면 변경 없음(공통 X-Day-Error 규칙이 끼움). 위 「코디가 볼 것」 1 은 이것으로 닫힘.
- 검증: `npm run check` node 127 pass · `./scripts/test.sh --pure backend/tests/day/web backend/tests/architecture` 503 passed.

## 기능 5 — 동행 띠 잘 보이게(E8 · R72 · task_ecdede24f23b)
- 띠 = 파란 굵은 테두리: 토큰 `--day-res-band-line: var(--ms-primary-500)` · `--day-res-band-w: 2px`(box-sizing border-box — 테두리가 띠 여백 2px 안이라 카드를 덮지 않음). 손 CSS 0(app.css → build-css).
- 꼬리표 「동행그룹」 = 기존 `ui.sq_badge("동행그룹", "primary", "solid")`(작은 파란 바탕 · 흰 글자)를 `.day-res-band__tag` 로 위 테두리 왼쪽에 걸쳐 얹음(`--day-res-band-tag-x 6px` · `-y -11px`) — 행 높이 · 카드 자리 그대로. R68 의 `aria-hidden` 은 뺌(글자가 생겨서).
- 가리지 않게: 띠 `pointer-events: none`(z-index 4 — 꼬리표가 위 행 카드 아래 끝에 걸려도 보이고, 누름 · hover · 끌기는 카드가 받음). 그래서 놓을 때 「자기 띠 안」 판정을 elementsFromPoint 대신 띠 상자(getBoundingClientRect) 안인지로 바꿈.
- 문구: `test_screen_copy.py` VISIBLE 에 「동행그룹」(결정 R72 · 사용자 문구).
- 시험: node — 띠 글자 「동행그룹」 · primary solid 배지 · 카드 top 282 / left 154 · 10:00 행 70px 그대로 · 「자기 띠 안 빈 곳」은 띠 상자로(변이: 띠 판정 끄면 실패) · 화면 pytest 띠 마크업 갱신 · 고정본 다시 씀.
- 검증: `npm run check` node 127 pass · web+architecture pytest 503 passed · ruff 통과.

## 기능 5 고침 1 — 책갈피 탭(R74 · E9 · 보충 note-1 · task_79a2d8c8f474)
- 탭 = 띠 왼쪽 위(띠 바깥 왼쪽 끝)에 붙은 **사다리꼴**(clip-path · 오른쪽 끝 8px 비스듬 「\」) · 진한 파랑 `--ms-primary` 바탕 · 흰 글자 · 흐림 없음 · 아래 끝 = 띠 위 테두리(띠 왼쪽 위 모서리는 각지게). 이전 사각 배지(연한 tint)는 뺌.
- 띠 테두리도 진하게: `--day-res-band-line: var(--ms-primary)`(이전 `--ms-primary-500` #99cbff 는 연파랑이었다).
- 행 높이: **bands 가 있는 시간 행만** `--day-res-band-tab-h`(18px)만큼 위 여백 → 그 행 카드 · 띠가 18px 아래로 · 시간 라벨 높이도 같이(10:00 = 88px) · 다른 행 그대로. day.js resRows 가 bands 의 start_min 으로 행을 찾는다.
- 끌기 · hover: 띠 · 탭은 그대로 pointer-events: none(자기 띠 판정 = 띠 상자).
- 시험(node): 띠 행 = 1 × 70 + 18 · 같은 행 그룹 밖 카드도 내려감 · 다음 행 370 · 열 높이 +18 · 위 행(09:30) 카드 아래 끝 278 < 탭 위 끝 280(안 겹침) · 변이(여백 0)로 두 시험 실패 확인 · 받침 `boot({page})` 추가. 화면 pytest 탭 마크업 · 문구 근거 R74 · 고정본 갱신.
- 검증: `npm run check` node 128 pass · web+architecture pytest 503 passed · ruff 통과. 남은 것: 실물에서 사다리꼴 · 색 눈 확인(재기동 뒤).

## 기능 5 고침 2 — 꼬리표 · 탭 없앰(R75 · task_5c28ffbc427d)
- 마크업: 띠 안 `<span class="day-res-band__tag">동행그룹</span>` 뺌 · 글자가 없어져 R68 의 `aria-hidden="true"` 되살림.
- CSS(app.css → build): `.day-res-band__tag`(사다리꼴 clip-path) · `--day-res-band-tab-h/-x/-slant` 토큰 뺌 · 띠 왼쪽 위 각짐 → `border-radius: 6px`. 색 `--ms-primary` · 굵기 2px 그대로.
- day.js: resRows 의 띠 행 여백(pad) 뺌 → 행 높이 = lines × 줄 높이(R70 그대로) · 카드 / 띠 top = 행 top + line × 줄 + 2.
- 시험: test_screen_copy VISIBLE 「동행그룹」 뺌 · 화면 pytest 띠 마크업(aria-hidden · 「동행그룹」 없음) · node 띠 시험 되돌림(띠 280 · 카드 282 · 10:00 행 70 · 다음 행 352 · 열 32×70) · 탭 겹침 시험 삭제 · 고정본 다시 씀. 변이(10:00 행 +18)로 node 3 실패 확인 후 되돌림.
- 검증: `npm run check` node 127 pass · web+architecture pytest 503 passed · ruff 통과. 커밋 0 · 스택 안 건드림.
