# progress — post-procedure-timeline 1차 조사

- 상태: **1차 범위 종료**(원장 전체 완료 아님). 직접 읽기 S00~S10 11/11, 기계 추출 완료, verify 실패 0.
- 마지막으로 실제 읽은 Pointer: `/timelines/9/phases/3/emergency/2` (S10 끝)
- 남은 구획: 없음. 열린 미결은 issues.md(B21·P6·F4·I4·K3).
- 재현:
  - `uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/post-procedure-timeline/build.py`
  - `python3 orchestration/work/phub-ledger-redesign/first-pass/post-procedure-timeline/verify.py`
  - 구획 원문: `python3 orchestration/work/phub-ledger-redesign/first-pass/post-procedure-timeline/read_segment.py S06`
- 수동 기록 원천: manual/S00~S10.txt(직접 읽기), manual/global-issues.txt, manual/segmentation.txt(비어 있음 — 출현별 추가 판정 없음, 서명은 build.py SEQ_RULES).
