# 리뷰 리포트 — day-data-architecture / code · #231 fix1 + #230 fix2 함께 재검수 (커밋 전 마지막 · 2026-11-06)

대상: 같은 워크트리의 미커밋 #230(fix1 · fix2 반영) + #231(fix1 반영).
근거 문서는 `frontend-231-fix1-{instructions,report}.md` · `backend-230-fix2-{instructions,report}.md`, 새 스크린샷은 `frontend-231-shots/` 16장, 앞 리포트는 `review-231-report.md` · `review-230-fix1-report.md` 다.
읽기 전용으로 봤다. KOS 호출은 하지 않았다. **compose 는 건드리지 않았다.** 테스트는 `-m "not infra"` 만 돌렸고, 전체 431 은 수정 리포트 · 코디 확인 수치를 따른다.

## 판정: PASS — **PR #228 커밋 가능**

#231 W1 ~ W3 와 #230 fix1 「#231 영향」 세 건이 반영됐다. #230 fix2(판 조각에 권한 · `is_admin`, `lateAt` = U12)도 들어왔다. 두 쪽이 맞물려 버튼 숨김이 실제 `/board` 에서 동작한다.
아래 「참고」 셋은 동작을 막지 않는 작은 것이다. W4(A4 · A6 실물)는 코드 밖(사용자의 `DAY_ADMIN_EMAILS`)이라 커밋을 막지 않는다. Issue 체크만 남긴다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **280 passed · 151 deselected / 3.3s**(fix2 리포트 280 과 같음 · 앞 재검수 때의 #231 실패 1건 해소) |
| `uv run ruff check backend scripts` | All checks passed |
| grep 전수(`templates/**` · `day.js`) | `style=` 0 · `<style>` 0 · `hx-on` 0 · `on*=` 0 · `<script>` 본문 0 · `innerHTML` · `eval` · `new Function` 0 |
| `styles/app.css` · `day.css` diff | 0 — 새 토큰 · 새 클래스 없음 |
| 실데이터(`명동` · `세라미크`) | 템플릿 · day.js · routers 0 |

## #231 W1 ~ W3

| | 판정 | 근거 |
|---|---|---|
| W1 시간 칸 「늦음」을 템플릿이 정함 | **닫힘** | `board_parts.html:70` 기본 `"late": false` · `:80` `late_at=c.lateAt or ""` — 재호출 · 5분 계산이 템플릿에서 사라지고 서버 `call.lateAt` 만 옮긴다. `recalled` 는 인박스 원장 줄의 「· 재호출 +mm:ss」 글자를 보일지만 정한다(`:163` · 표시용 · SPEC U-5 문장) |
| W2 권한 없는 조작 무표시 | **닫힘** | ① 버튼을 안 그린다 — `_edit_of`(`board_parts.html:14-20`)가 `permissions` · `is_admin` 으로 `EDIT`(board) · `ACCEPT`(board.accept)를 정한다. `PermissionLevel` 은 `StrEnum` 이라 `p.level == "edit"` 비교가 맞다. ② 그래도 403 이면 `htmx:responseError`(`day.js:382-`)가 `<template data-day-toast-on="403">`(`board.html`)을 띄운다. 문구 = `web_errors.FORBIDDEN_MESSAGE`(테스트가 글자 일치를 지킨다). 스크린샷 `15-forbidden-toast` |
| W3 미룬 판 다시 받기 | **닫힘** | `flushRefresh()`(`day.js:291`)를 창 `close`(`:379`) · 팝오버 닫기(`:90`) · 끌기 끝(`:236`)에서 부른다. 아직 다른 창 · 메뉴 · 끌기가 남아 있으면 계속 미룬다 |

## #230 fix1 「#231 영향」 반영

| 항목 | 판정 | 근거 |
|---|---|---|
| SSE `session_expired` | **반영** | `board.html` `<div hx-get="/board" hx-trigger="sse:session_expired" hx-swap="none" hx-params="none">` — 판을 한 번 다시 청한다. 그러면 #229 화면 규칙이 처리한다: `unauthorized` · 만료 → 204 + `HX-Redirect`(htmx 는 `hx-swap=none` 이어도 따른다), `forbidden` → 403 → 위 토스트 |
| `is_admin` + `permissions` 로 버튼 숨김 | **반영 · 맞물림 확인** | 아래 「맞물림」 |
| 웹 폼 모르는 칸 400 | **반영** | `#board-main` 과 카드에 `hx-params="none"`. 순서 form 은 `visitIds`, 호출 창은 `taskIds,target,doctorStaffId`, 재호출 창은 `target,doctorStaffId`, 수락 창은 `doctorStaffId`. 창 안 검색(`doctor_q`) · 라디오(`pick`)는 나가지 않는다. CSRF 는 `<body hx-headers>` 헤더라 `hx-params` 와 무관하게 실린다. 실제 요청 본문은 브라우저로 확인됐다(fix1 리포트) · 테스트 `test_웹_폼은_라우트가_받는_칸만_싣는다` |

## #230 fix2

| 항목 | 판정 | 근거 |
|---|---|---|
| 판 조각에 권한 · `is_admin` | **닫힘** | `routers/board._render_board`(`:130-155`) — `GET /board` 는 `WebView.permissions` · `is_admin`, 조작 응답은 `sessions.grants(session, current)`(`sessions.py:147-154` = `permissions_of` + `is_admin` — `require_permission` 과 같은 두 함수 · 판단 한 곳 유지)로 다시 읽어 `render(..., permissions=, is_admin=)` 로 넘긴다 |
| `lateAt` = U12 | **닫힘** | `board_rules.call_late_at`(`:407-412`) — 응답 기다리는(`called`) 줄 · 닫히지 않은 **지금 열린 호출**의 `created_at` + 5분(재호출이면 새 호출부터 = SPEC-002 OQ-04 시간 ⓐ). 수락 · 시작 · 닫힌 호출 · 호출 없음 = null. 카드 `anesthesia.lateAt` = 진행 중 마취 시작 + 20분(`:445`) · 끝났거나 없으면 null. 그 밖 lateAt 없음. DB 없는 테스트 `test_늦음_시각은_U12_그대로` |

### 맞물림 — 버튼 숨김이 실제로 동작하는가

**동작한다.**
- 서버(`_render_board`)가 모든 판 응답(`GET /board` · 조작 응답 전부)에 `permissions` · `is_admin` 을 넘긴다.
- 템플릿 `_edit_of` 는 그 값으로 `EDIT` · `ACCEPT` 를 정한다.
- 값이 없는 응답(dev 견본)만 「다 그림 + 403 토스트」로 떨어진다.

확인한 테스트:
- infra 3(`test_board_api.py`): view 만 → 시작 · 마취 버튼 없음 / board edit 만 → 마취 있음 · [수락] 없음 / 권한 0 + `DAY_ADMIN_EMAILS` → [수락]까지 있음.
- DB 없는 6가지(`test_board_page.py`): 값 없음 · 권한 0 · view 만 · board edit · board + accept · 권한 0 + `is_admin`.

### backend 가 고친 frontend 테스트 기대값

`test_시술_줄_시간_칸은_템플릿이_늦음을_정하지_않는다`(`test_board_page.py:178-189`):
- 「재호출 줄에 `is-late` 클래스가 없고(템플릿이 정하지 않음) `data-day-late-at` 이 있다(서버 값을 옮김)」로 바뀌었다.
- 서버가 이제 그 줄에 `lateAt` 을 싣고(재호출 = 열린 호출 + 5분), 템플릿 `:80` 이 그것을 `data-day-late-at` 으로 옮긴다. 그래서 **기대값이 맞다.** 템플릿 · day.js 는 backend 가 건드리지 않았다(fix2 리포트 · diff 확인).
- 다만 값 일치까지는 보지 않는다 → 아래 「조용히 통과」 1.

## 조용히 통과하는 자리

| 자리 | 왜 · 고칠 방향(낮음 · 커밋을 막지 않음) |
|---|---|
| 위 테스트의 `data-day-late-at="[^"]+"` | 값이 **있는지만** 본다. 템플릿이 다시 스스로 시각을 지어 넣어도(예: `firstCalledAt + 5분`) 통과한다. 그 줄의 값이 스냅샷 `call.lateAt` 과 같음을 단언하면 W1 이 잠긴다 |

## 참고 (판정 밖)

1. **마취 칩은 아직 템플릿이 늦음 시각을 계산한다** — `board_parts.html:53` `a.runningSince|day_plus_min(ANES_MIN)`. 값은 서버 `anesthesia.lateAt` 과 같다(같은 시작 시각 + 서버가 준 `limits.anesMin`). 그래서 실해는 없지만, 「서버 값만」으로 맞추려면 `a.lateAt` 을 쓰는 한 줄로 바꾼다.
2. **W4 — A4(두 화면 SSE) · A6(실물 토스트)** 는 사용자가 `DAY_ADMIN_EMAILS` 를 넣은 뒤 1회 확인할 것. 코드 쪽 준비(권한 · 스트림 · 토스트)는 끝났다. Issue #231 체크 항목으로 남긴다.
3. 남은 결정 · 후속(이번 커밋과 무관):
   - A8 실제 KOS 쓰기 1회(W5 b 같이)
   - `PROCEDURE_WAITING` 열기
   - SPEC-002 개정 목록(오류 본문 · `task_not_doing` · `doctorAssignedDateTimeUtc` · `overSec` · `lateAt` · SSE `session_expired` · `me.is_admin`)
   - 지은 문구(빈 판 등) 디자인 확인
   - 오류 토스트 확정 문구
