# progress — problem-combos 1차

- 상태: **1차 범위 종료** (원장 전체 완료 아님 — issues.md 미결 B5·F6·I5·P1·K)
- 직접 읽기: S0~S8 전부 완료 (manual/S*.json, coverage.json direct_read=read)
- 기계 추출: 전부 완료 (build.py)
- 마지막으로 실제 읽은 Pointer: /combos/7/packages/1/riskBenefit (원장 마지막 말단) + 읽기 검토 재확인 완료
- 다음 구획: 없음
- 열린 문제: issues.md
- 재현:
  - `uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/problem-combos/build.py`
  - `python3 orchestration/work/phub-ledger-redesign/first-pass/problem-combos/verify.py`
