# be-3 리포트 — N1

## 고친 것
- `backend/day/services/board_rules.py` `system_doctor` — `task_state(t)` 가 `doing` · `done` 이 아니면 False 를 먼저 돌려준다(SPEC-002 U-3 :225). 그래서 「시작 취소」 뒤 준비중 줄과 그 줄을 다시 호출한 줄은 `systemDoctor=false` 가 되고, 템플릿에는 원래 글자(호출 대상 「전체」 · 지정 원장)가 보인다. 템플릿 · 앱 계약은 바꾸지 않았다(칸 뜻만 스펙 조건에 맞춤).

## 테스트
- `backend/tests/day/board/test_board_feedback_rules.py` 에 `test_systemDoctor_는_진행중_완료_줄만_시작_취소_뒤_준비중_호출_줄은_아님` 추가(DB 없음): 준비중(집도의 남음) false · 호출 false · 진행중 true · 완료 true.
- 실행: `uv run pytest -q tests/day/board/test_board_feedback_rules.py tests/day/board/test_board_rules.py tests/day/web/test_board_page.py -m "not infra"` → 140 passed. `ruff check` 통과 · format 통과.
- infra 테스트는 고치지 않았다. `test_board_feedback_service.py:477` 은 바로 시작 직후(진행중) 줄을 보므로 영향 없음 — 실행하지는 않았다.

## 남은 것
- 없음. 커밋 안 함.
