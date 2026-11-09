# #230 fix2 — #231 요청 두 가지 (백엔드)

## #231 영향
- 판 조각에 이제 `permissions` · `is_admin` 이 넘어간다. 템플릿의 버튼 숨김이 실제 `/board` 에서 동작한다.
- 새 값 두 개: 시술 줄 `call.lateAt` · 카드 `anesthesia.lateAt`. 시술 줄의 늦음 빨강이 서버 시각대로 되살아난다.
- **frontend 테스트 하나를 고쳤다**: `tests/day/web/test_board_page.py::test_시술_줄_시간_칸은_템플릿이_늦음을_정하지_않는다`.
  - 전에는 「서버가 lateAt 을 안 싣는다」를 전제로 `data-day-late-at` 이 없다고 단언했다.
  - 이제는 「템플릿은 `is-late` 를 정하지 않고, 서버 lateAt 을 `data-day-late-at` 으로 옮긴다」를 본다.
  - 템플릿 · day.js 는 건드리지 않았다.

## 1. 권한을 판 조각에
- `services/sessions.grants(session, current)` → (직무 권한 행, `is_admin`). 판정 규칙은 `require_permission` 과 같은 두 함수(`permissions_of` · `is_admin`)다.
- `routers/board._render_board`:
  - `GET /board` 는 `WebView.permissions` · `is_admin` 을 그대로 쓴다.
  - 모든 조작 응답은 `grants` 로 세션에서 다시 읽는다.
  - 둘 다 `render(..., permissions=, is_admin=)` 로 넘긴다.
- 조각 계약 독스트링의 `GET /board` 줄에 두 값을 더했다.
- 테스트(infra 3 · `test_board_api.py`):
  - view 만 → 판 조각에 시작 · 마취 버튼이 없다.
  - board edit 만 → 조작 응답에 마취는 있고 [수락]은 없다.
  - 권한 0 + `DAY_ADMIN_EMAILS` → 조작 응답에 [수락]까지 있다.
  - 템플릿 분기 6가지는 #231 의 DB 없는 테스트가 이미 본다.

## 2. `lateAt` — 원천 U12 그대로
- 시술 줄 `call.lateAt` = **지금 열린 호출**의 `created_at` + 5분이다. 재호출이면 새 호출부터 잰다(OQ-04 시간 ⓐ).
  - 응답을 기다리는 줄(state `called`)만 싣는다. 수락됨 · 시작 · 닫힌 호출 · 호출 없음이면 null 이다.
- 카드 `anesthesia.lateAt` = 진행 중 마취 시작 + 20분이다. 끝났거나 없으면 null 이다.
- 그 밖에는 lateAt 이 없다. 계산은 `board_rules.call_late_at` · `card_view` 한 곳이다.
- 테스트(DB 없이): `test_늦음_시각은_U12_그대로` — 재호출 줄 · 수락 줄 · 호출 없는 줄 · 진행 중/끝난 마취.

## 검증
| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | 280 passed |
| `scripts/test.sh -q` | 431 passed |
| ruff check · format --check | 통과 |
| compose | down 안 함 · `--profile app up -d --build --wait api` → `/health/ready` ok |

## 남은 것
- 없음(이번 범위). A8 실제 KOS 쓰기 · `PROCEDURE_WAITING` 결정 · SPEC 개정은 fix1 리포트 그대로.
