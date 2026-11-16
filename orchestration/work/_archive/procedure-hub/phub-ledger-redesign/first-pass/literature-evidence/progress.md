# progress — literature-evidence 1차 조사

- 상태: **1차 범위 종료**(원장 전체 완료 아님). 구획 18/18 직접 읽기·형태소 전수 대조·읽기 검토·verify 통과
- 마지막으로 실제 읽은 Pointer: `/categories/M17/effects` (S17 끝). 형태소 마지막 값 `/categories/M17/adverse_effects/0/patient_ko`
- 기계 추출 완료 18/18 · 직접 읽기 완료 18/18 (coverage.json `reading_state`)
- 다음: 없음(코디 보고). 후속은 issues.md 의 B·I·F·K 묶음 — 2단계 공통 의미·ERD 에서 다룸
- 열린 문제: issues.md (I 33 · B 20 · F 17 · K 1 + 형태소 18규칙 34출현 · C 0 · A 0)
- 재현 명령(레포 루트):
  - `uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/literature-evidence/build.py`
  - `python3 orchestration/work/phub-ledger-redesign/first-pass/literature-evidence/verify.py [--selftest]`
  - 구획 읽기 출력: `python3 orchestration/work/phub-ledger-redesign/first-pass/literature-evidence/read_segment.py S01`
