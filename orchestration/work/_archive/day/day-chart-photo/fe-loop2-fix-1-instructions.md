# [frontend] 2루프 fix-1 — 구조 테스트 실패

## 무엇이 실패했나
코디 전체 시험에서 2690 passed · 1 failed:
- `backend/tests/architecture/test_web_rules.py::test_day_js_는_innerHTML_로_글자를_넣지_않는다`
- 원인: `backend/day/static/day.js:1627` 의 `swap: "innerHTML"` — 네가 2루프에서 넣은 C30 다시 읽기 코드다.

## 할 것
- 문자열 `innerHTML` 없이 같은 동작을 만든다.
  - 예: 대상 요소의 `hx-swap`(템플릿에 이미 `hx-swap="innerHTML"`)을 그대로 쓰는 `htmx.trigger`
  - 또는 `htmx.ajax` 에서 swap 을 생략하고 대상 속성을 따르게 한다
- 테스트를 고치지 마라.

## 검증
- `scripts/test.sh -q backend/tests/architecture backend/tests/day/web`
- `npm run -s check`

## 보고
- 커밋 금지.
- preamble worker_done 두 채널로 보고한다. 수치를 넣는다.
- 앞으로 화면 변경 뒤에는 `backend/tests/architecture` 도 돌린다.
