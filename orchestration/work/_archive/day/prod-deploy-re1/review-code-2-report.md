# 리뷰 리포트 — prod-deploy-re1 / code 재리뷰 2 (2026-11-11)

범위(코디 지정 · 전체 재리뷰 아님): review-code-1 W1 · W3 가 닫혔나 · 새 어긋남 · 종료 코드 문서. W2 는 스펙 쪽(mediness#933 `84561044`) 반영 확인만.
근거: be-1-report.md 「수정 1」 · SPEC-000 :1384(개정 `84561044`) · Delivery #243 A2 · A2b.

## 판정: PASS

FAIL 0 · WARN 0. 참고 2(막지 않음).

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q backend/tests/day/test_register_connection.py backend/tests/deploy -m "not infra"` | **115 passed**, 4 deselected(infra · 경로 안 바뀜) |
| `uv run ruff check` · `ruff format --check` (고친 2 파일) | All checks passed · 2 files already formatted |
| `cd backend && printf 'SECRETTAIL==\n' \| env -i … python -m day.register_connection --stdin` | `표준입력 1번째 줄: 모르는 이름 (표시 안 함)` · exit 1 |
| 같은 방식 `DAY_CONNECT_KOS_OPEN_API_KEY abc=x` | `(표시 안 함)` · exit 1 — `abc` 안 찍힘 |
| 같은 방식 `DAY_CONNECT_TYPO=v` | `모르는 이름 DAY_CONNECT_TYPO` · exit 1 (오타 이름은 보여 줌 · 값 없음) |

`public.py` · `crm_connections.py` 는 1차 리뷰 뒤 바뀌지 않았다(diff stat 동일 · W2 = 코드 그대로).

## W1 — 닫힘 (PASS)

- `backend/day/register_connection.py:40` `PRINTABLE_NAME = DAY_CONNECT_[A-Z0-9_]+` · `:62-64` 모르는 이름은 이 모양과 **정확히** 맞을 때만 찍고, 아니면 `(표시 안 함)` + 줄 번호. 공백이 섞인 이름 칸 · 잘린 키 조각(소문자 · `=` 패딩 · 접두 없음)은 fullmatch 를 못 지나간다.
- 시험: `test_register_connection.py:128-145` 에 `SECRETTAIL==` · `DAY_CONNECT_KOS_OPEN_API_KEY abc=x` 를 더했고, 전체 값이 아니라 **조각**(`SECRETTAIL` · `abc` · `DAY_SEED_BRAND_CODE` · `brand-x`)이 err 에 없음을 단언한다 — 1차의 「조용히 통과하는 자리」가 막혔다. `:148-151` 모양 맞는 오타는 이름이 보인다(운영자가 오타를 찾을 수 있음).

## W3 — 닫힘 (PASS)

- `register_connection.py:116-118` — `ConnectionKindConflict` 밖의 `Exception` 은 `등록 실패: <클래스 이름>` 만 찍고 exit 4. 예외 문자열(SQLAlchemy `[parameters: …]`)은 나가지 않는다.
- 「쓰기 없음」(문서) 주장: `register_kos_connection` 은 `ensure_connection` 뒤 `commit` 1회가 마지막이라(`public.py:67-77`), 예외가 나면 commit 전이거나 commit 자체가 실패 → `get_async_session` rollback. 맞다.
- 시험 `:154-162` — 값이 든 `RuntimeError` → err 가 정확히 `등록 실패: RuntimeError` · 비밀 없음.

## W2 — 스펙 반영 확인 (PASS)

mediness `84561044` SPEC-000 :1384 에 「**데모 시드도 같다** — 같은 브랜드 코드 · 병원 이름의 운영 연결(`is_demo = false`)을 만나면 덮지 않고 멈춘다(양방향 거절 · 코디 2026-11-11) · 데모 → 데모 다시 넣기는 그대로」 · 개정 ④ 요약(:31)에도 한 줄. 코드(`crm_connections.py:127-128` · `ensure_demo_connection`)와 같다.

## 종료 코드 문서 (`docs/development/deployment.md` 「운영 연결 등록」) — PASS

`0` 넣음/고침 · `1` 값 문제 · `2` `--stdin` 밖 인자 · `3` 데모 연결 있음(쓰기 0) · `4` 그 밖 실패(클래스 이름만 · 쓰기 없음) — 코드 `run` 의 return 2 · 1 · 1 · 3 · 4 · 0 과 하나씩 맞는다. 3 의 문구 「**데모** 연결」도 진입점이 늘 `demo=False` 로 부르므로 정확하다.

## 새 어긋남

없음. 참고만:

- 참고 1(문구): 문서 `1` 줄 「표준입력의 모르는 이름 · 모양이 틀린 줄은 줄 번호만」 — 실제로는 `DAY_CONNECT_…` 모양의 모르는 이름은 이름도 보인다(`:63`). 읽기에 따라 「모르는 이름도 줄 번호만」으로 읽힌다. 고칠 필요 낮음 — 원하면 「모양이 다른 이름 칸 · `=` 없는 줄은 줄 번호만」.
- 참고 2(가장자리): `parse_stdin` 앞의 표준입력 디코딩 오류(`UnicodeDecodeError` — 값 파일이 UTF-8 이 아님)와 `_main` 의 `dispose_engine` 예외는 `run` 의 try 밖이라 traceback 으로 나간다. 메시지는 바이트 위치 · 엔진 오류뿐이라 값이 실리지 않는다 — 막지 않음.

## Acceptance 변화

| # | 1차 | 2차 |
|---|---|---|
| A2 | 부분(W1 · W3) | **충족** — 파싱 오류 · 그 밖 실패 모두 값 없이 이름/줄 번호/클래스 이름만 |
| A2b · A3 | 충족(+W2 스펙 밖) | 충족 — 양방향 거절이 스펙에 들어감 |
| A1 · A4 · A5 | 충족 | 그대로(변경 없음 · 115 passed) |
