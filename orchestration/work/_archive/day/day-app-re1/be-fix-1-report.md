# be-fix-1 리포트 — review-code-1 W5 · W6 · W7

워크트리 `day-app-re1` · base `43ba40a3` · 커밋 · push 없음. 동작 변경 없음 · 계약 차이 없음.

## 변경 파일
- **새** `backend/day/routers/photo_forms.py` — 웹 · 앱 사진 라우터 공용(`board_messages.py` 와 같은 routers 공용 모듈 자리). `MAX_FILES` · `BODY_MAX_BYTES` · `FILE_HEADERS` · `photo_id_of()`(옛 `_photo_id`) · `read_photo_form()`(옛 `_form`). 본문 그대로 옮김.
- `backend/day/routers/board_photos.py` — 위 정의 빼고 `photo_forms` 에서 import(호출 이름만 바뀜).
- `backend/day/routers/api/board_photos.py` — `day.routers.board_photos` 의 `_` 이름 import 제거 → `photo_forms` 공개 이름.
- `backend/day/errors.py` — W6 `ChartConflict` docstring = `{"conflicts": [{taskId, body, staffId, base: {body, doctorStaffId}, baseLogId}]}`(C2 · `chart_conflicts_json`).
- `backend/tests/day/board/test_board_api_chart_photos.py` — W7 `!= 200` → `== 303 and location == "/login"`(`required_web_view` → `LoginRequired` → 비HTMX 303). `BODY_MAX_BYTES` monkeypatch 대상 → `photo_forms`.
- `backend/tests/day/board/test_board_loop3.py` — `BODY_MAX_BYTES` monkeypatch · 단언 대상 → `photo_forms`(상한 값이 이제 그 모듈에 있음).

주의: `routers/board_photos.py` 는 브리프 §5 상 frontend 몫 경로지만 W5 지시대로 정의 이동 · 호출 이름 변경만 했다(템플릿 · static · 동작 무변경).

## 검증
- `scripts/test.sh` 만진 테스트 3파일(api_chart_photos · loop3 · board_photos) — 62 passed.
- ruff check · format(만진 6파일) — 통과.
- `scripts/check.sh`(전체 · 격리 인프라) — 구조/Jinja(654 sources) · ruff · format · mypy · taut-audit · taut-check · frontend · tests 전부 통과. pytest 2902 passed · frontend 단계(npm) fail 0. 증거 `.local/checks/20261125-115843-85280`.

## 남은 것
없음. (워크트리의 `app/` 변경 · `app/test/ui/session_leave_test.dart` 는 mobile 워커 몫 — 건드리지 않음.)
