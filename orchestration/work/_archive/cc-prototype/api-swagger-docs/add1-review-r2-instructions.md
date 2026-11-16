# [reviewer] add1 재검수 r2

원 브리프(`add1-review-brief.md`) 제약 그대로(read-only · KOS 0 · 서버 기동 금지). 기준 SPEC-008 **0.3.2**(N1 → D-16 · N3 · T45 ~ T47) · 고침 지시 `add1-be-fix-1.md` · be 리포트 `add1-be-report.md` 「고침 2」 절.
- 지난 리포트 `add1-review-r1.md` W1 · N1 · N2 가 닫혔는지 하나씩(닫힘 / 덜 닫힘 / 새 문제). N1 은 직원 「이전 방문」 동작이 바뀌지 않았는지도
- `uv run pytest -q` · `uv run ruff check .` 1회씩 직접
산출 `add1-review-r2.md`. 판정 PASS / WARN / FAIL. 완료 보고는 원 브리프 §4 두 채널(이번 dispatch 의 taskId · dispatchId · 리포트 이름 r2).
