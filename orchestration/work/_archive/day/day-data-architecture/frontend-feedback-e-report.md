# 화면 피드백 F17 · F18 · F19 — 결과 보고

- 작성: day frontend 워커 · 2026-11-06 · task_224b0dfa45e1
- 커밋 `292d0996` 위 미커밋 · **커밋 안 함**
- compose: **내리지 않았다.** api 만 다시 빌드했다(`/login` 200).
- **백엔드 로직 파일은 건드리지 않았다.** 바꾼 라우터는 dev 견본 `routers/kit_board.py` 하나다(`?finish=<작업 id>` — 견본에서 「종료 뒤」 모습을 보려고).

## 상태: done

- **실제 `/board` 는 지금 판에 카드가 0장이다**(데모 두 방문 모두 귀가 대기). 그래서 F17 · F18 · F19 는 같은 템플릿 · 같은 day.js 인 견본 `/dev/kit/board` 에서 브라우저로 확인했다.
- 조작 요청(`POST …/calls` · `…/finish` · `PUT /board/order`)은 견본 id 가 서버에 없어서, Playwright 가 견본 판 조각으로 대신 응답했다. **실제 서버 · KOS 쓰기는 0건**이다.

## F17 — 호출(재호출)이 나가면 그 카드 선택 해제

- 원인: 성공 응답으로 판을 다시 그릴 때 day.js 가 체크를 되살렸다(화면 상태 지키기).
- 고침:
  - 의사 호출 · 재호출 창 form 에 `data-day-clear-checks="<방문 id>"` 를 단다.
  - **성공(2xx) 응답일 때만** 그 카드의 체크를 되살리지 않는다. 체크 기억 열쇠를 「묶음(방문)|칸=값」 으로 바꿨다.
  - 오류(409 등)면 체크는 그대로 남는다.
- 브라우저: 체크 2 · 바 켜짐 → 「모든 의사」 호출 → **체크 0 · 바 꺼짐**(`f17-after-call.png`). 보낸 칸은 `taskIds · target · doctorStaffId` 그대로다.

## F18 — [종료] 뒤 더보기가 저절로 열림

- **원인(재현)**:
  - [종료] 를 누르면 판을 다시 받는다. 그 줄은 완료 칸으로 내려가고, 포인터 밑에는 완료 줄이 온다.
  - 완료 줄의 ⋮(더보기)는 hover 때 나타나는데, 그 자리가 **[종료] 가 있던 자리와 같다**. 그래서 ⋮ 가 바로 미끄러져 나왔다(`f18-after-finish-before-fix.png`).
  - 이어서 한 번 더 누르면(더블클릭 · 성급한 클릭) 그 ⋮ 메뉴가 열리거나, 줄을 눌러 **차트가 열렸다**(재현함).
  - htmx 포커스 이어짐은 원인이 아니었다(포커스는 body).
- **고침**:
  1. 판을 다시 받은 뒤 짧은 동안(**`--day-motion-guard` 450ms**) 판 루트에 `is-day-settling` 을 둔다. 그동안은:
     - 시술 줄 ⋮ 를 숨기고 누를 수 없게 한다(CSS)
     - 줄 누름(차트) · 줄의 팝오버 트리거를 받지 않는다(day.js)
  2. **바뀌는 모습은 짧게 미끄러진다(FLIP)**: 다시 받기 전후의 줄(`data-day-flip="t:<id>"`) · 카드 자리를 비교해 **`--day-motion-flip` 220ms · `--day-ease-out`** 으로 옮긴다. 줄은 카드 기준 자리라 카드와 같이 두 번 움직이지 않는다. 새 줄은 옅게 나타난다.
- 브라우저(견본 · 시술실 B [종료]):
  - +150ms: 판 루트 settling · 보이는 ⋮ **0** · 이어 누름 → 열린 팝오버 **없음** · 차트 **안 열림**
  - +850ms(가드 뒤): 평소처럼 hover 에만 ⋮(`f18-after-finish.png`)

## F19 — 카드 D&D 를 cc-prototype 처럼

- day.js 끌기를 다시 썼다:
  - **끄는 카드가 손을 따라온다**: `translate`. 잡은 자리와 손의 간격이 처음부터 끝까지 같다(18, 16).
  - 다른 카드 위로 가면 그 자리로 들어가고 **다른 카드가 비켜난다**: FLIP · 220ms. 비켜나는 동안은 다시 바꾸지 않는다(왔다 갔다 방지).
  - 끄는 카드는 위로 뜬다: `z-index` · 끌기 그림자 토큰.
  - **놓으면 부드럽게 제자리로 들어간다**: `--day-motion-settle` 200ms. 다 들어간 뒤 저장 한 번(`day:sorted` → `PUT /board/order`, 칸 `visitIds` 그대로).
  - 끄는 동안과 자리 잡는 동안에는 SSE 판 다시 받기를 미룬다(busy). 끝나면 미룬 것을 받는다.
  - 화살표 키 순서 바꾸기도 같은 FLIP 이다.
- 브라우저(견본 · 레이저실 1 을 세 번째 자리로):
  - 중간: `translate(75px, 20px)` · 미리보기 순서 `시술실 A, 레이저실 1, …`(`f19-drag-mid.png`)
  - 끝: `translate(150px, 40px)` · `시술실 A, 레이저실 2, 레이저실 1, 시술실 B`(`f19-drag-end.png`)
  - 놓음: 자리 잡기 애니메이션 1 → 끝(`f19-dropped.png`) · PUT 1번(visitIds 4개 · 새 순서)
  - **녹화: `f19-drag.gif`**(마지막 3.2초 · 12fps)
- 시안 FLIP(L1534-1558)과 cc `OrderCard`(미리보기 순서 · 놓을 때 저장)를 본으로 삼았다. HTML5 drag ghost 대신 포인터 이벤트로 카드 자체가 따라온다.
- 손 CSS 0: 위치는 day.js(CSSOM · WAAPI), 시간 · 곡선은 토큰이다.

## 검증

- `uv run pytest -q -m "not infra"`: **305 passed**
- `scripts/test.sh -q backend/tests/day/board backend/tests/day/web backend/tests/day/auth`: **182 passed**
- ruff 통과 · CSS 다시 빌드
- 새 테스트:
  - `test_호출_재호출_창은_보낸_뒤_그_카드_체크를_푼다`
  - `test_줄_카드_자리_열쇠와_움직임_토큰`
- 스크린샷 · 녹화(`frontend-feedback-shots/`): `f17-after-call.png` · `f18-after-finish-before-fix.png` · `f18-after-finish.png` · `f19-drag-mid.png` · `f19-drag-end.png` · `f19-dropped.png` · **`f19-drag.gif`**

## 바꾼 파일

- `static/day.js`: FLIP · 움직임 토큰 읽기 · 끌기 다시 쓰기 · settling 가드 · F17 체크 풀기
- `styles/app.css` + `static/day.css`: `--day-motion-flip/settle/guard` · `[data-day-sort-item].is-dragging` · settling 더보기 숨김
- `templates/ui.html`: `doctor_call_modal(clears)`
- `templates/partials/board_parts.html`: 줄 `data-day-flip` · `clears`
- `templates/partials/board_main.html`: 호출 · 재호출 `clears=card.visitId`
- `routers/kit_board.py`: 견본 `?finish=`
- `tests/day/web/test_board_page.py`

## 남은 것

- 실제 `/board` 실물: 데모 지점에 판 카드가 2장 이상 생기면 끌기를 한 번 해 본다(지금은 카드 0).
