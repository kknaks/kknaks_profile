# 로그인 뒤 갈 곳 = /board — 결과 보고 (사용자 요청 · 2026-11-06)

## 상태: done · 커밋 안 함 · compose 는 api 만 다시 올림(`/login` 200)

## 바꾼 것

- `routers/login.py`
  - `after_login()` 이 이제 늘 **`/board`** 를 준다(dev · prod 같음). 로그인 · 병원 고르기 성공 · 로그인한 채 `/login` 을 열 때 모두 이 값을 쓴다.
  - `/` 는 권한 행이 0이면 권한 없음 화면(SPEC-001 규칙 9 · 그대로), 아니면 `/board` 로 보낸다.
  - 권한이 없으면 `/board` 가 #229 화면 규칙대로 권한 없음 화면을 준다.
- `templates/home.html`(빈 홈) 삭제 — 이제 쓰는 곳이 없다.
- `/dev/kit` 은 그대로 둔다(dev 전용 · 로그인 필요). 셸(아이콘 줄 · 헤더 탭 · 로그인 화면)에서 거기로 가는 링크는 0개다. `kit.py` docstring 도 「기본 진입 아님」으로 고쳤다.
- 테스트 `tests/day/auth/test_web_login.py`: 이동 기대값 `/dev/kit` → `/board`(5곳). `/dev/kit` 을 직접 여는 CSRF · 견본 테스트는 그대로다.

## 검증

- `uv run pytest -q -m "not infra"` **280 passed**
- `scripts/test.sh -q backend/tests/day/auth backend/tests/day/web` **93 passed**
- ruff(`login.py` · `kit.py` · `test_web_login.py`) 통과
- 브라우저(headless Chromium · 데모 계정):
  - `/` → `/login` → 로그인 → **`/board` 200**
  - 로그인한 채 `/` 와 `/login` → `/board`
  - 셸에 `/dev/kit` 링크 0개
  - 로그아웃 → `/login?reason=logged_out`
  - 스크린샷 `frontend-231-shots/17-login-lands-on-board.png`

## 알림

- `deploy/local.env` 에 `DAY_ADMIN_EMAILS` 가 이제 들어 있다(사용자). 그래서 데모 계정으로 **실제 `/board` 가 열린다**.
  - 데모 지점 오늘 카드 1장: 확인 필요 · 수납 필요 · 호출 67분.
  - 시술 줄 시간 칸의 빨강은 서버가 싣는 `call.lateAt` 에서 온다(#231 fix1 W1 대로).
- 이제 #231 W4(A4 두 화면 SSE · A6 실물 토스트)를 할 수 있다.
