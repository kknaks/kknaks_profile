# #231 fix1 — 검수 W1 ~ W3 + #230 fix1 「#231 영향」 반영 결과 보고

- 작성: day frontend 워커 · 2026-11-06 · task_8fdde8b4d5d4
- 워크트리: 같은 워크트리 · 미커밋 · **커밋 안 함**
- compose: **내리지 않았다.** `--profile app up -d --build --wait api` 로 api 만 다시 올렸다(`/login` 200).
- **백엔드 파일은 건드리지 않았다.** 고친 것은 templates · `static/day.js` · `tests/day/web` 뿐이다. #230 fix1 리포트의 「#231 영향」 표를 보고 맞췄다.

## 상태: done — 버튼 숨김은 템플릿 쪽만 끝냈다. 백엔드가 값 둘을 넘겨야 실제 `/board` 에서 동작한다(아래 「요청」)

## W1 — 시술 줄 시간 칸 「늦음」 빨강을 템플릿이 정하던 것

- `board_parts.proc` 에서 재호출 여부와 5분 계산을 지웠다. 이제 시술 줄의 「호출」 글자와 시간 칸은 **늘 기본색**이다.
- 서버가 시술 줄 `call.lateAt` 을 실어 주면, 그 시각부터 빨강이 된다(`data-day-late-at` → day.js). 실어 주지 않으면 빨강은 없다.
  - #230 fix1 은 아직 `lateAt` 을 싣지 않는다. 그래서 지금 빨강이 남은 곳은 SPEC 이 정한 자리뿐이다: 마취 칩 20분(`anesthesia.long` · 서버 기준 시각) · 확인 필요 카드(`card.need`) · 인박스 원장 줄의 「호출」(`card.need.why == "call"`).
- 테스트 `test_시술_줄_시간_칸은_템플릿이_늦음을_정하지_않는다`: 재호출한 울쎄라 줄에 `is-late` · `data-day-late-at` 이 없음을 본다.

## W2 + #230 영향 (2) — 권한 없는 조작

조작 화면과 403 처리를 두 겹으로 막았다.

1. **버튼을 처음부터 그리지 않는다** — `board_parts` 맨 위에서 `EDIT` · `ACCEPT` 를 정한다.
   - 셸 값 `permissions`(+ **`is_admin` = 모든 키 · edit**)를 본다.
   - `board` edit 이 없으면 숨기는 것: 체크 · 전체 선택 · 시작 · 종료 · 더보기(되돌리기) · 마취 칩(배지로만 보임) · 손잡이와 끌기 · 호출 바 · 귀가 대기 · 재호출.
   - `board.accept` edit 이 없으면 숨기는 것: [수락](시술 줄 · 호출 탭).
   - **두 값을 넘기지 않는 응답이면 지금처럼 다 그린다.** 아래 2번 토스트가 받쳐 준다.
   - 테스트 `test_권한으로_조작_버튼을_숨긴다` 6가지: 값 없음 · 권한 0 · view 만 · board edit 만 · board + accept edit · 권한 0 + `is_admin`.
2. **403 토스트** — 조작이 403 인데 `X-Day-Error` 가 없으면(`web_errors` 의 권한 없음 조각) day.js 가 `board.html` 의 `<template data-day-toast-on="403">` 을 `#day-toasts` 에 띄운다.
   - 문구는 SPEC-001 대응표의 「이 화면을 볼 권한이 없습니다. 관리자에게 문의해 주세요」 그대로다. `web_errors.FORBIDDEN_MESSAGE` 와 같은 글자인지 테스트가 지킨다.
   - 브라우저 실물: 견본에서 [시작] → 403 → 토스트(`15-forbidden-toast.png`).

### 요청 (백엔드 · 코디) — 버튼 숨김이 실제 `/board` 에서 동작하려면

`routers/board.py` 의 `_render_board`(GET `/board` 과 모든 조작 응답)가 `render(..., permissions=…, is_admin=…)` 를 넘겨야 한다.

- 지금은 `session=current` 만 넘긴다. 그래서 템플릿이 권한을 모르고 다 그린다(403 토스트로만 알림).
- 조작 응답은 `CurrentSession` 만 갖고 있다. 그래서 `required_web_view` 또는 `sessions.me` 로 권한을 같이 읽어야 한다.
- 백엔드 파일이라 손대지 않았다.

## W3 — 미룬 판 다시 받기

- `flushRefresh()` 를 새로 뒀다. 미룬 다시 받기가 있으면 다음 경우에 한 번 부른다: 창 `close` · 팝오버 닫기(`closePop`) · 끌기 끝(`endDrag`).
- 그때 아직 다른 창 · 메뉴 · 끌기가 남아 있으면 계속 미룬다(`busy`).
- 테스트 `test_미룬_판_다시_받기는_메뉴_닫기와_끌기_끝에도_풀린다`.

## #230 fix1 「#231 영향」

| 항목 | 반영 |
|---|---|
| (1) SSE `session_expired` | `board.html` 에 `<div hx-get="/board" hx-trigger="sse:session_expired" hx-swap="none">` 를 두었다. 이벤트가 오면 판을 한 번 다시 청한다. 그러면 #229 화면 규칙이 처리한다: `unauthorized` → `/login`, 만료 → `/login?reason=session_expired`(HTMX 204 + `HX-Redirect`), `forbidden` → 403 토스트. 테스트 `test_SSE_session_expired_면_판을_다시_청해_login_으로` |
| (2) `is_admin` + `permissions` 로 버튼 숨김 | 위 W2 1번(템플릿 끝 · 백엔드가 값을 넘겨야 함) |
| (3) 웹 폼은 정한 칸만(모르는 칸은 400) | `hx-params` 로 실을 칸을 못 박았다. 바깥 판(`#board-main`)과 카드마다 `none` — 조작 버튼(시작 · 종료 · 마취 · 귀가 대기 · 되돌리기)이 둘러싼 순서 form 의 칸을 싣지 않게 했다. 순서 form 은 `visitIds`. 호출 창은 `taskIds,target,doctorStaffId` · 재호출 창은 `target,doctorStaffId` · 수락 창은 `doctorStaffId`. 창 안 검색 글자(`doctor_q`) · 고르기 라디오(`pick`)는 나가지 않는다. **브라우저로 실제 요청 본문을 확인했다**(아래). 테스트 `test_웹_폼은_라우트가_받는_칸만_싣는다` |
| `sync.lastError` · `need.overSec` | 화면 변경 없음(순서는 서버가 정함 · 「동기화 멈춤」 표시는 범위 밖) |

실제 요청 본문(견본 · 브라우저):

```
POST /board/visits/{id}/calls          ← taskIds={id}&target=one&doctorStaffId={id}
POST /board/visits/{id}/anesthesia/start ← (빈 본문)
POST /board/tasks/{id}/finish            ← (빈 본문)
PUT  /board/order                        ← visitIds={id}&visitIds={id}&…(5개 · 순서대로)
```

## 바꾼 파일

- `templates/board.html`: `hx-params="none"` · 403 토스트 `<template>` · `session_expired` 다시 받기
- `templates/partials/board_parts.html`: W1 · 권한 `EDIT` / `ACCEPT` · 창 `params` · 카드 `hx-params`
- `templates/partials/board_main.html`: 순서 form `hx-params="visitIds"`
- `templates/ui.html`: `doctor_call_modal(params=)` 인자 하나
- `static/day.js`: `flushRefresh` · `htmx:responseError` 403 토스트
- `tests/day/web/test_board_page.py`: 새 테스트 13개(권한 6 가지 포함)

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **279 passed** |
| `scripts/test.sh -q backend/tests/day/board`(#230 infra · 새 템플릿으로 실제 라우트) | **60 passed** |
| `uv run ruff check` — 내 파일(`web.py` · `kit_board.py` · `tests/day/web` · `tests/architecture`) | 통과 |
| 브라우저 견본 `/dev/kit/board` | 앞 리포트의 동작이 모두 그대로였다. 추가로 [시작] 403 → 권한 없음 토스트, 요청 본문 위와 같음 |
| 스크린샷 | `frontend-231-shots/` 01 ~ 14 를 다시 찍고 **15-forbidden-toast** 를 더했다(00 실제 `/board` 권한 없음은 그대로 · 모두 16장) |

## 남은 것

- 백엔드가 `_render_board` 에 `permissions` · `is_admin` 을 넘기기(위 「요청」).
- 시술 줄 늦음 빨강을 되살릴지: 서버 `call.lateAt` 규칙(SPEC U12 와 맞게 · 사용자 · 코디 결정).
- W4: A4 · A6 실물 — 사용자가 `DAY_ADMIN_EMAILS` 를 넣은 뒤(이번에는 하지 않음).
