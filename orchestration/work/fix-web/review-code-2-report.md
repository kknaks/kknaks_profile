# 리뷰 리포트 — fix-web / code 2차 (2026-11-12)

대상: `CENTURION_DAY/fix-web` 미커밋 변경 전부(base `origin/dev` `c5045a99`) — 1차(`review-code-1-report.md`) 뒤 frontend 반영분(`fe-2-report.md`) 포함.
기준: 1차와 같은 브리프(결정 표 W1 ~ W11 · 결정 A · DAY-SPEC-002 개정 ⑳ · DAY-SPEC-003 개정 ⑬).
리뷰어 검증: `uv run pytest -q -m "not infra"` → **930 passed · 318 deselected** · `uv run ruff check backend` → 통과 · `node --check day.js` → 통과 · `static/day.css` 배너 `source-sha256:4f332af6…` = `app.css` sha256(일치). infra 는 돌리지 않음.

## 판정: PASS

1차 FAIL 1 · WARN 3 모두 해소. 새 FAIL · WARN 없음.

## 1차 지적 해소 확인

| 1차 | 고친 곳 | 확인 | 판정 |
|---|---|---|---|
| F1 귀가대기 머리에 경과 | `backend/day/templates/partials/board_parts.html:201` — `{% if item.why != "home" %}…분째{% endif %}` · 매크로 주석(`:192`)에 「귀가대기는 경과 없음 · U-10」 | SPEC-002 U-10 표 `home` 행 「귀가대기(경과 없음)」과 같음. 테스트 `backend/tests/day/web/test_board_page.py:511-523` — 머리 정규식을 배지 + 머리 닫힘까지로 묶고 `by_why["home"] == "귀가대기"`(정확 일치 → 경과가 붙으면 실패). 나머지 3상황은 `대기|마취|호출\d+분째` 그대로 | PASS |
| W1 다른(흐린) 카드 클릭이 해제 안 됨 | `backend/day/static/day.js:757-760` — click 위임 맨 앞에서 `[data-day-card].is-selected` · `[data-day-goto]` · `.day-pop` · `dialog` · `#modal-root` 밖이면 `clearCards(document)` · return 없음. 1차의 뒤쪽 `else if` 분기 삭제 | 아래 「W9 재검」 | PASS |
| W2 근거 표에 지운 문구 | `backend/tests/architecture/test_screen_copy.py:29-36` — 「현황」 · 「시작 가능」 · 「시술 대기」 · 「수락함」 삭제 · 금지 목록(`:175-177`)에 「수락함」 · 「시작 가능」 · 「귀가 대기 전」 | 허용 · 금지 겹침 없음. 「호출」(`:32`)은 E41 줄 상태 · 수락 대기 카드 「호출 mm:ss」로 계속 쓰여 남는 게 맞음 | PASS |
| W3 주석 · 단언 범위 · 중복 줄 | `test_board_page.py:97` — [수락] 단언을 `#inbox-call-list` ~ `#inbox-panel-done` 구간으로 좁힘 · `test_판_카드_호출_줄에는_재호출이_없다` 중복 `board =` 줄 삭제(`:558` 하나만) | 주석과 단언 범위 일치 | PASS |

## W9 재검 (day.js:757-760 · :912)

- **팝오버 · 창 안**: `.day-pop`(메뉴 · 고르기 목록 · 콤보 목록 모두 이 클래스 — `ui.html:109` · `:125`) · `dialog`(배경 클릭 target = dialog 자신) · `#modal-root` 제외 → 풀지 않음. SPEC-002 U-10 「팝오버 · 창(dialog) 안을 누르는 것은 풀지 않는다」와 같음.
- **고른 카드 안**: `[data-day-card].is-selected` 제외 — 고른 판 카드 안 버튼 · 줄 · 체크, 같은 방문의 인박스 카드(같이 `is-selected`)는 그대로. 「고른 카드를 다시 누르면 풀림」은 아래 기존 분기(`:776-783`)가 맡음.
- **다른 카드**: 흐린 판 카드 빈 곳 · 버튼 · 더보기 → 고르기를 풀고(return 없음) 그 버튼 · 팝오버 동작은 아래에서 그대로 이어짐. 1차 W1 해소.
- **인박스 카드 본문**(`[data-day-goto]`) 제외 — 아래 고르기 분기가 새 카드 고르기 / 같은 카드면 풀기를 한다(먼저 풀고 다시 고르는 깜빡임 없음). 인박스 카드의 [재호출] · [수락](goto 버튼 밖)은 그 카드가 고른 카드가 아니면 고르기를 풀고 동작 — 「고른 카드 밖」이라 맞음.
- **탭**: 클릭은 카드 밖이라 풀림. ←→ 키는 인박스 탭만 풂(`:912`). `selectTab` 안에는 넣지 않아 `restoreState → selectTab`(OOB 탭 줄 재그림)이 고르기를 풀지 않음.
- **복원 충돌**: `keepState` 는 `htmx:beforeSwap` · `oobBeforeSwap` 에서 그때 DOM 의 `.is-selected` 를 읽음 → 푼 고르기는 되살아나지 않고, 안 푼 고르기는 그대로 복원.
- **순서**: 해제가 차트 담당자 목록(`.day-pop` 안 → 제외) · 팝오버 트리거 early return 보다 앞에 있어도 부작용 없음(트리거 클릭 = 카드 밖이면 해제 + 팝오버 열기).
- **위임 누수**: 새 리스너 없음. 인라인 스크립트 · `eval` · `onclick` 없음.
- 실물 확인은 아무도 못 함(사용자 포트 금지) — 아래 「직원이 실물에서 만날 자리」 4.

## 나머지 항목 (1차 PASS 유지 — 변경 없음 재확인)

- W2 · W3 탭 글자 · 숫자, W6 · W7 목록 하나, W4 카드 구조(이름 줄 · 버튼 칸), W5 상태 글자, W8 판 시술 줄 [수락] 없음, W10 · W11 버튼, W1 메모 12px · 80px — 1차 표 그대로(`board_regions.html:20-36` · `board_parts.html:91-93` · `:195-229` · `styles/app.css:161` · `:448`).
- 결정 A(서버 accept 제거 · `acceptMin` · `doctorName` · env 삭제) · `inbox.section` · `urgency` · `calls[]` 유지 — 백엔드 파일은 1차 뒤 바뀌지 않음.
- 앱 호환: `app/lib/model/board.dart` `Need.parse` · `Limits.parse` · 칩 `inbox.section` — 깨질 자리 없음(1차 그대로).
- 「조용히 통과하는 자리」: 지운 키(`startable`·`waiting`(inbox 칸)·`acceptMin`·`doctorName`·`doctor_changed_at`·`inbox_card`·`call_lines`) 다시 grep → 남은 읽기 0(앱용 `inbox_section()` · 무관 enum · 부재 단언만).

## 스펙 ⑳ 과 코드가 다른 곳

없음(1차의 귀가대기 경과 · 다른 카드 클릭 둘 다 맞춤).

## infra 테스트 — 영향 받는 것(코디가 `scripts/test.sh` 로 확인 · 1차와 같음)

- `backend/tests/day/board/test_board_api.py::test_웹_판_조각_계약`
- `backend/tests/day/board/test_board_api.py::test_수락_뒤_오래_시작하지_않아도_확인_필요가_없다`
- `backend/tests/day/board/test_board_queries.py::test_방문_1개와_10개의_쿼리_수가_같다`(16 → 15)
- 삭제: `test_board_queries.py::test_원장_바꾼_시각_조회는_event_log_인덱스를_탄다`
- fe-2 변경은 템플릿 · JS · non-infra 테스트뿐이라 infra 쪽 영향 추가 없음. 전체 `scripts/test.sh` 는 아직 아무도 안 돌림.

## 직원이 실물에서 만날 자리

1. 확인 필요 카드: 「대기 n분째」 · 「마취 n분째」 · 「호출 n분째」 · 「귀가대기」(경과 없음).
2. 수락 뒤 오래 시작 안 한 고객이 웹 확인 필요 · 앱 「확인 필요」 칩에서 빠지고 앱 「시작 가능」 칩으로 감(결정 A · 의도).
3. 판 시술 줄에 [수락] 없음 — 수락은 「수락 대기」 탭에서(W8 · 의도).
4. 카드를 고른 뒤 다른 카드의 [시작] · 더보기를 누르면 그 동작과 함께 고르기가 풀린다 — E2E 에서 눈으로 확인 권장(fe-2 리포트도 같은 권고).

## 참고(기존 부채 · 무관)

- OOB 로 인박스 목록만 다시 그릴 때 `keepState(target)` 이 그 자리 안의 `.is-selected` 만 봐서, 판 카드를 고른 상태의 인박스 카드 흐림이 풀린 채 그려질 수 있음 — 이번 변경 전부터(`day.js` keepState · oobAfterSwap).
