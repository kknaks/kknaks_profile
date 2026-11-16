# progress — treatment-optimization 1차 조사

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/treatment-optimization.json` sha256 `07b9ebe0a843280b4eef9487590951932192435ea46284aba425338ab9d9767b` · 22,887 bytes · 14,718 cp · 한 줄 · 백슬래시 0 · BOM 없음
- 구획 계획(14): SEG-00 상위(version·updated·consensus_method·optimization_principles + 루트·상위 컨테이너) · SEG-01~08 `/by_concern/0`~`/7` · SEG-09 `/by_age_group` · SEG-10 `/combination_rules` · SEG-11~13 `/annual_plans/0`~`/2`
- 직접 읽기 기록: `manual/seg-XX.json` (구획마다 읽은 즉시 저장). 없는 파일 = 미독.

## 로그 (최신이 아래)
- SEG-00·01·02 원문 직접 읽음 → manual 기록 작성
- SEG-03·04 직접 읽음 → manual 기록
- SEG-05·06 직접 읽음 → manual 기록
- SEG-07·08 직접 읽음 → manual 기록
- SEG-09·10 직접 읽음 → manual 기록
- SEG-11·12·13 직접 읽음 → manual 기록. 전 구획 1회차 직접 읽기 완료. 다음: build.py 작성
- build.py 1회차 실행(토큰 3,025). 다음: 토큰 전수 대조 → manual/segmentation-review.json
- 오분절 기록 생성기 manual/make-segmentation-review.py → 77출현. 다음: 자동 후보 오탐 검토
- 오분절 77출현·오탐 14·미덮임 어절 전수 검토 완료(A-01~04 수정). 다음: global-issues.json → verify.py → validation.md
- verify.py 140검사 통과·변이 7종 검출. 다음: 재현성·문서 확인·validation.md
- validation.md 작성. verify 140/140 · 변이 7종 · 재현성 확인.

## 현재 상태 (마지막 갱신)
- 마지막으로 읽은 Pointer: /annual_plans/2/schedule/11/procedures/2 (원장 끝). 현재 구획: 없음(14/14 직접 읽기 완료). 다음 구획: 없음.
- 열린 문제: issues.md — B 26 · I 12 · K 6 · F 14 · C 0. 1차 범위 종료, 원장 전체 완료 아님.
- 재현 명령(레포 루트):
  - `OMP_NUM_THREADS=1 uv run --no-project --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/treatment-optimization/build.py`
  - (manual 규칙을 고쳤을 때) `python3 .../manual/make-segmentation-review.py` · `python3 .../manual/make-expression-review.py` 실행 뒤 build 재실행
  - `python3 orchestration/work/phub-ledger-redesign/first-pass/treatment-optimization/verify.py`
  - `python3 orchestration/work/phub-ledger-redesign/first-pass/treatment-optimization/mutation-test.py`
