# 리뷰 리포트 — day-procedure-board-2 / code — CENTURION_DAY#236 frontend 단계 (2026-11-10)

대상: 워크트리 `CENTURION_DAY/day-procedure-board-2` 미커밋 — `templates/ui.html` · `partials/board_parts.html` · `board_main.html` · 새 `board_done_list.html` · `board_chart.html` · `base.html` · `routers/board.py` · `routers/kit_board.py` · `web.py` · `static/day.js` · `styles/app.css` · `static/day.css` · `tests/day/web/test_board_page.py` · `tests/architecture/test_screen_copy.py` · `tests/day/board/test_board_api.py`(웹 라우트 infra). 동시에 진행 중인 backend 테스트 보강 · migration 은 대상 아님.
SSOT: Delivery #236 v2 ①~⑯ · A1 ~ A10 · DAY-SPEC-002 개정 ⑬ ⑭ · `_RESUME.md` §2 · `fe-236-brief.md`.
파일 경로는 `backend/` 기준.

## 판정: WARN (FAIL 0)

화면 9항목 모두 스펙 · 결정대로이고 테스트가 그 모양을 단언한다. 인라인 스크립트 · 인라인 style · `on*=` 0, 새 클래스 · 색 없이 기존 `app.css` 규칙만 고쳤다. 아래 WARN 은 스펙에 글자가 없어 기존 글자를 다른 자리에 다시 쓴 것과 SSE 검색 깜빡임 · 스펙 문서 쪽 정리 거리다.

검증(직접 1회): `DAY_ENV_FILE=…/local.env scripts/test.sh -q` → **651 passed · 3 failed**(합 654). 실패 3건은 모두 `tests/migrations/test_alembic.py`이고 원인은 `assert ['0006_event_log_visit_type'] == ['0005_outbox_sender']` 하나다. backend 워커가 지금 만들고 있는 미추적 `migrations/versions/20261110_0006_event_log_visit_type.py` 때문이고 **이번 대상 밖**이다. frontend 몫(web · architecture · board 웹 라우트) 테스트는 전부 통과했다. backend 리뷰 때 실패하던 템플릿 테스트 25건도 이제 통과한다.

## FAIL

없음.

## WARN

### W1. 「원장 교체」 글자를 툴팁 밖 두 자리(원장 목록 머리 · 보내기 버튼)에도 썼다 — 스펙에는 툴팁뿐
- `templates/ui.html:357` `title` · `:366` `submit` 의 `"doctor": "원장 교체"` · `tests/architecture/test_screen_copy.py` VISIBLE 「원장 교체」 근거 = 「툴팁 「원장 교체」(기획 3-2) — 원장 목록 머리 · 버튼도 같은 글자」.
- 스펙 U-3 · 규칙 27 · 결정(11-09 「호출 수락(3-2)」)은 「원장 이름에 호버하면 툴팁 「원장 교체」 · 누르면 원장 목록에서 고름」까지만 말한다. 목록 창의 머리 · 버튼 글자는 정해지지 않았다. 새 낱말은 아니고(지어낸 글자 0) 기존 E51 창 모양(머리 + 보내기 버튼)을 따르려면 무언가가 들어가야 하므로 **FAIL 아님**. 코디 · 사용자 확인 뒤 spec-sync 에 U-3 한 줄(「원장 목록 머리 · 버튼 = 「원장 교체」」)로 남길 것.

### W2. 판 카드의 E35 경고 아이콘 · 빨강 테두리를 뺀 것은 근거가 있지만 스펙 문서 안에서 서로 다르다(스펙 쪽 정리 거리)
- 코드: `partials/board_parts.html` 방 카드 `dense_card("room", "", …)` · 머리 줄의 `icon("warn", … "확인 필요")` 제거 · `inbox_card` 의 `is-late` 제거(`:125-131` 근처 · `:154` 근처).
- 근거(맞음): SPEC-002 U-10 `spec-002:254` 「**보이기만 한다** — 인박스 「확인 필요」 칸 카드만. 팝업 알림 · **고객 카드 표시는 없다**」 · Delivery #236 ⑧ 「인박스(사이드) 「확인 필요」 칸에 보이기만(팝업 · 알림 · **고객 카드 표시 없음**)」 · §1 「이번에 안 하는 것」 1-3 「고객 카드」 행. 워커가 말한 「U-10 근거」는 맞다.
- 다만 같은 스펙의 `spec-002:138`(판 요소 표 「E35 경고 아이콘 … 넣음」)과 `:153`(카드 머리 줄 「손잡이 E34 · **경고 E35** · 방 이름 · 마취 칩」)은 아직 E35 를 카드에 둔다. 코드는 맞고 스펙이 앞뒤가 다르다 — planner 가 다음에 손볼 때 `:138` · `:153` 에서 E35 를 빼거나 「인박스 확인 필요 칸 머리 아이콘(U-10)」으로 옮길 것. 마취 20분 초과 칩 빨강(`a.long`)은 결정대로 판 카드에 남아 있다.

### W3. 검색 중 SSE 로 판을 다시 받으면 거르지 않은 목록이 잠깐 보였다가 다시 걸러진다
- `partials/board_main.html:39` `#done-list` 는 `#board-main` 안에 있어 SSE 다시 받기 때 `snapshot.doneTab` 전체로 다시 그려진다. `static/day.js:450-453` 은 검색어가 남아 있으면 그 뒤에 `day:research` 로 `/board/search` 를 다시 청한다. 그래서 결과는 맞지만, 다시 청한 응답이 올 때까지(한 번 왕복) 전체 목록이 보인다. 10초 조회 · 조작마다 SSE 가 오므로 검색해 둔 채 보면 목록이 깜빡인다.
- 데이터는 틀리지 않으니 WARN. 고치는 방법(예: 판 조각을 그릴 때 서버가 지금 검색어를 알 수 없으니, 다시 받기 전에 `#done-list` 를 `data-day-keep` 으로 두고 검색어가 있으면 바꾸지 않기)은 frontend 판단이다. 실물에서 거슬리는지 사용자 확인 거리.

### W4. 검색 칸 글자 「고객 이름」 · 「고객 이름으로 찾기」는 이제 원장 · 관리실로도 찾는 칸과 맞지 않다(스펙에 새 글자 없음 · 그대로 둔 것은 규칙대로)
- `partials/board_main.html:39` placeholder 「고객 이름」(시안 L1446) · aria-label 「고객 이름으로 찾기」.
- 찾는 말이 이름 + 담당 원장 + 관리실(U-13)로 넓어졌는데 글자는 옛 시안 그대로다. 새 글자를 지어내지 않은 것은 맞다(브리프 「없으면 비우고 질문」). 다만 직원이 원장 · 방 이름으로 찾을 수 있다는 것을 화면에서 알 수 없다 — 기획 1-2 의 검색 칸 글자가 있으면 planner 가 스펙에 옮길 거리(OQ 후보).

### W5. 원장 교체 버튼은 화면 읽기 프로그램에 「원장 교체」 뜻이 전해지지 않는다
- `templates/ui.html:259-260` `_proc_doctor` — `<button class="hover:underline" data-tip="원장 교체" data-day-pop=…>{원장 이름}</button>`. 키보드로 닿고(버튼) Enter 로 팝오버가 열리지만, 툴팁은 `data-tip`(마우스 호버 표시)뿐이라 읽기 프로그램은 원장 이름만 읽는다. 다른 `pop_trigger` 버튼처럼 `aria-haspopup="dialog"` · `aria-controls` 가 붙는지도 `pop_trigger` 매크로에 달려 있다. 「원장 교체」는 이미 있는 글자라 `aria-description` · `aria-describedby` 로 붙여도 새 글자가 아니다 — 낮음.

## 참고 · 낮음

- `task_not_assignable` 토스트: `MESSAGES` 에 없어 `web_errors.py:113` 의 공용 폴백 「요청이 올바르지 않습니다」(invalid_request)가 나온다. 새 글자를 만들지 않았고 OQ-33(글자 미정)대로다 — 정해지면 `routers/board.py:98` `MESSAGES` 에 한 줄 넣으면 된다.
- 완료 줄 「{원장} · n분」(`ui.html:270`): `p.doctor` 는 `t.doctor` 가 없고 호출이 「모든 의사」면 「전체」가 된다(`board_parts.html` `proc` 의 `doctor` 값 — 앞 판부터 있던 대체). 완료 시술은 보통 담당의가 있어 실물에서 만날 일은 드물지만, 그때는 「전체 · n분」으로 보인다.
- 호출 줄에 [수락](원장 · board.accept)과 [재호출](board edit)이 같이 보이면 줄 오른쪽 폭이 좁아진다 — 스크린샷으로만 확인 가능(A2/A4 스크린샷 때).
- `.day-proc__more` 규칙에 이제 쓰지 않는 `transition: width … opacity …`가 남아 있다(`styles/app.css` 더보기 줄) — 동작 영향 없음.
- `routers/board.py:217` `_PARTS_SNAPSHOT = {"now": None, …}` — 검색 조각은 `now` 없이 그린다. `done_card` 는 `NOW` 를 쓰지 않아(시각 = `inAt` · `homeAt` HH:MM) 문제없다.

## PASS — 화면 9항목

| # | 항목 | 코드 | 테스트 |
|---|---|---|---|
| 1 | 체크박스 준비중만 · 완료는 체크된 채 꺼짐 · 전체 선택 = `canCall` 없으면 꺼짐 | `ui.html` `proc_row`(`status == "wait" and not locked` · 완료 `check_item(checked=true, disabled=true)`) · `board_parts.html:154` | `test_체크박스는_준비중만_완료는_체크된_채_꺼짐` |
| 1 | 고객 이름 누르기 없음(`<span>`) · 시술 이름(줄) → 차트 | `ui.html` `customer_line(button=false)` · `board_parts.html` `row_attrs data-day-row-open` · `button.day-cust:hover` 로 호버도 버튼만 | `test_고객_이름은_누르는_동작이_없고_시술_이름은_차트` |
| 1 | 「⋯」 늘 보임 · 카드 스크롤 → 끝이면 판(`overscroll-behavior` 뺌) | `styles/app.css` `.day-proc__more`(16px · 호버 규칙 삭제) · `.day-card__scroll` | `test_더보기는_늘_보이고_카드_스크롤은_판으로_넘어간다`(CSS 단언 — 실제 스크롤은 수동 · A2 스크린샷) |
| 2 | 고객 검색 = 「시술 완료」 탭 칸 → 서버(`GET /board/search` · 300ms · board view) · 결과 0 = 「검색 결과 없음」 + [조건 지우기](OQ-28 그대로) · 빈 검색어 = 원래 목록 · 카드 시술 줄 → `GET /board/visits/{id}/chart`(판과 같은 `chart_modal`) · E06 뺌 | `board_main.html:39` · `board_done_list.html` · `board_chart.html` · `routers/board.py:220-264` · `base.html` | `test_검색_목록_조각은_결과가_없으면_검색_결과_없음` · `test_차트_조각은_열린_채로_누른_시술을_깜빡인다` · `test_상단_고객_검색_칸은_없다` · infra `test_웹_고객_검색은_시술_완료_탭_목록_조각` · `test_웹_차트는_열린_모달_조각_다른_방문은_404` · copy 테스트 「고객 검색」 · 「조건에 맞는 고객이 없어요」 금지 |
| 3 | 확인 필요 5카드 — 상황 1개 = 1장 · 빨강(`is-late`) · 「대기 n분째」 · 「마취 n분째」 · 「호출 n분째」 · 「{원장} 수락 n분째」 · 「귀가 대기 전」 · n = day.js 1분 단위 · 받지 않은 호출 카드 [재호출] 검정(`day-btn--black` = 흰 바탕 · 기본 글자색) · 귀가 대기 전 카드 [귀가 대기](확인 창 없음) · 팝업 · 토스트 없음 · 누르면 판 카드로 | `board_parts.html:203-` `need_card` · `board_main.html:23` | `test_확인_필요_5상황_카드는_인박스에만_빨강`(why 5개 · `is-late` 5 · 글자 정규식 · 버튼 class · `<dialog` 없음) |
| 3 | 호출 중 줄 [재호출] 늘(`canRecall` · board edit) | `board_parts.html` `proc` `recall_attrs` · `ui.html` `proc_row` | `test_호출_줄은_재호출이_늘_있다` |
| 4 | 마취: [마취 시작] → 「마취중 mm:ss」 + [마취 종료] → 「마취 완료 mm:ss」 + [마취 시작] · 20분 넘으면 빨강(서버 `long` · `lateAt` 부터 day.js) · 인박스는 칩만 | `board_parts.html:50-` `anesthesia_chip` · `web.py` `day_clock` · `day_secs` · `day.js` `clock` 형식 | `test_확인_필요_마취_3상태_…` 등 기존 갱신 · copy 테스트 「마취 재시작」 뺌 |
| 5 | 줄 글자 「{원장} 수락 완료 HH:MM」 · 「{원장} · 진행 mm:ss」 · 「{원장} · n분」 | `ui.html:260-300` `proc_row` · `_proc_doctor` · `:270` | `test_수락_진행_완료_줄의_원장_글자` |
| 6 | 원장 교체 — 수락 · 진행중 줄 원장 이름 버튼 · 툴팁 「원장 교체」 · 원장 목록(E51 모양 · 「모든 의사」 줄 없음 · 기본 선택 없음) · `POST /board/tasks/{id}/doctor`(`doctorStaffId` · board edit · `/tasks/{id}/{action}` 앞) | `board_parts.html:72` · `proc_menu` · `ui.html` `doctor_call_modal` `doctor` 모드 · `routers/board.py:452-467` | `test_원장_이름에_원장_교체_툴팁과_원장_목록`(준비중 · 호출 · 완료 줄엔 없음) · infra `test_웹_원장_교체는_판_조각을_돌려준다` · `test_원장_바꾸기는_웹_조작과_같은_권한` |
| 7 | 동시 수락 토스트 「다른 원장이 먼저 받았습니다」 | `routers/board.py:107` `MESSAGES` | `test_동시_수락_거절_토스트_글자` · infra `test_웹_동시_수락_거절은_토스트_글자` |
| 8 | 시작 취소 · 완료 취소 확인 창 — 메뉴 줄은 창만 열고 · 창 머리 「{시술} 시작을 취소할까요?」 · 「{시술} 완료를 취소할까요?」 · [닫기](보내지 않음) · [시작 취소]/[완료 취소] = 지금 되돌리기 `hx-post` · `<dialog>.showModal()`(포커스 가둠 · Esc) | `ui.html:318-` `confirm_modal` · `board_parts.html:110-` `proc_menu` · `day.js` `data-day-open-dialog` | `test_시작_취소_완료_취소는_확인_창을_거친다`(메뉴에 `hx-post` 없음 단언) · infra `test_웹_시작_취소는_확인_창을_그리고_되돌리기는_그대로` |

## 브리프 3 — 인라인 · 손 CSS · 접근성 · 권한 · SSE

- 인라인 `<script>`(src 없는 것) 0 · `style="` 0 · `on*=` 0(templates 전체 grep). `day.css` 는 다시 빌드한 결과물.
- CSS: 기존 규칙만 고침(`.day-card__scroll` · `.day-cust:hover` → `button.day-cust:hover` · `.day-proc__more`) — 새 클래스 · 색 · 치수 없음. 템플릿의 `hover:underline` 은 Tailwind 유틸(빌드 대상).
- 권한: 검색 · 차트 조각 = `board` view(`_allowed VIEW` · 비 HTMX 는 `/board` 로 돌림) · 원장 교체 = `writable_session`(CSRF) + `board` edit. 화면은 `EDIT` 일 때만 원장 버튼 · [재호출] · 확인 창 · 카드 버튼, `ACCEPT` 일 때만 [수락].
- SSE · 모달 충돌: 판 다시 받기는 `dialog[open]` · 열린 팝오버 · 끌기 중이면 미룬다(`day.js:392-404` `busy`) → 확인 창 · 원장 목록 · 차트(`#modal-root`) 열린 동안 안 바뀐다. 차트 모달은 `#board-main` 밖(`#modal-root`)이라 SSE 로 지워지지 않는다. 검색은 W3.
- 접근성: 확인 창 = 네이티브 `<dialog>` + `aria-labelledby` · `showModal` · [닫기] 먼저. 원장 버튼은 W5.

## 브리프 4 — 테스트가 실제로 막나

- 대부분 렌더된 HTML 단언(글자 · 클래스 · `hx-*` · 금지 글자)이고, 웹 라우트 5개는 infra 로 실제 요청을 보낸다. 다만 **day.js 동작**(검색 다시 청하기 · 확인 창 열기 · 「n분째」 1초 갱신 · 스크롤 넘김)은 `test_서버_검색과_새_경과_글자는_day_js_가` 의 소스 문자열 단언과 CSS 문자열 단언뿐이라 실제 브라우저 동작은 막지 못한다. Delivery A1 · A2 · A4 · A5 · A9 의 「화면 스크린샷 · 수동」이 그 몫이니 실물 확인 때 보면 된다.

## 직원이 실물에서 만날 자리

- 「시술 완료」 탭에서 검색해 둔 채 기다리면 목록이 10초마다 깜빡인다(W3).
- 검색 칸에 「고객 이름」이라고 써 있어 원장 · 방 이름으로도 찾을 수 있는 줄 모른다(W4).
- 판 카드에는 확인 필요 표시가 없다(빨간 테두리 · 경고 아이콘 없음) — 왼쪽 「확인 필요」 칸만 본다(결정대로 · W2).
- 원장 이름을 눌러 열리는 창의 머리 · 버튼이 「원장 교체」(W1).
- 원장 교체 · [재호출] 의 KOS 실물은 dev 데모 지점에서(A7).
