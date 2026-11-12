# [reviewer] 외부 연동 API 재검수 r2 — 수정 1 확인
원 브리프(`ext-api-review-brief.md`) 제약 그대로(read-only · KOS 0 · 서버 기동 0).
- 지난 리포트 `ext-review-r1.md` W1 ~ W6 가 각각 닫혔는지(닫힘 / 덜 닫힘 / 새 문제) — `ext-be-report.md` 「수정 1」의 주장을 실물로(재현 스크립트 다시 돌려라 · W1 `{"data":null}` 예약 → 502 · create-visitor 0 · W5 지연 주입 동시 150 → 200 60 · W6 예외 → ext_call 1줄 · no-store)
- W7 · W1 · W3 은 SPEC 0.2.2 와 코드가 맞는지
- 수정으로 생긴 회귀(직원 경로 · 문서 개수 단언 · 「설명 빠진 곳 0」)
- `uv run pytest -q` · `ruff` 1회
산출물 `ext-review-r2.md`. 완료 보고는 원 브리프 §4 두 채널.
