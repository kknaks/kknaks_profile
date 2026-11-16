# 확정본 추가 수정 — name_en 출처 칸 (사용자 승인 2026-11-10 · 추천 B)

대상: `silver-model/silver/material.csv` · `mechanism.csv` · `tissue.csv` · `method-candidates.csv`

## 할 일
1. 네 CSV 모두 `name_en` 바로 뒤에 `name_en_source` 칼럼을 추가한다. 값: `원장` / `보충` / (name_en 이 비었으면 빈 칸).
2. 판정: 그 영어 이름(또는 대소문자·하이픈·공백만 다른 같은 표기)이 원장 21개(`orchestration/work/phub-recommend/bronze/phub-ledger/*.json`) 어딘가에 실제로 나오면 `원장`, 아니면 `보충`. 철자만 비교하지 말고, 같은 말의 표기 차이(Platelet-Rich Fibrin ↔ platelet rich fibrin)는 원장으로 본다. 판정은 스크립트로 전수 하되 경계 사례는 눈으로 확인한다.
3. `보충` 인 영어 이름 자체는 고치지 않는다(표준 용어 유지). 지어낸 듯한 서술형(예: 「growth-factor stimulation of fibroblasts」처럼 용어가 아닌 문장)은 그대로 두되 notes 에 목록만.
4. `atoms-notes.md` 에 한 절 추가: 테이블별 원장/보충 개수, 서술형 목록.
5. UTF-8 BOM 유지. 다른 칼럼·행·파일은 건드리지 않는다.

## 완료
`git status` 로 위 파일 외 변경 없음 확인 후 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "atoms name_en_source 완료" --enter`
(이전 dispatch 의 worker_done 은 이미 보냈으니 다시 보내지 않는다.)
