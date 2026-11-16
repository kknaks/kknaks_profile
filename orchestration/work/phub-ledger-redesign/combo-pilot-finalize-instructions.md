# 지시서 — ② 조합 시범 확정: 재료를 연결 표로 + 판단 7건 반영

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 읽을 것

- `drafts/combo/` 전부(특히 `combo-notes.md` §2 · §6 판단 7건) · `combo-build.py` · `combo-check.py`
- `silver/` 전부 · 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)
- 원래 발주서 `../combo-pilot-brief.md`

## 사용자 결정 (11-14 「추천대로」)

1. **§6-3 = 재료를 연결 표로**: `procedure.csv` 에서 `material_code` 칸을 없애고 `procedure_material.csv`(`id` · `procedure_code` · `material_code`)를 만든다. 원장이 적은 성분마다 한 행 — 스노우주사 = 글루타치온 + 트라넥삼산, 마이어스칵테일 = 원장 「Mg+Ca+B/C」 의 성분 전부(사전에 없는 성분은 `dict-candidates.csv` 에). 단일 성분 시술은 지금 material_code 한 행 그대로. id 는 `P-1` 부터. 근거는 source_ref(target_table = procedure_material).
   - 시술 정체 검사를 「같은 modality · 재료 집합 · mechanism 인 시술 종류 2개 이상 = 0」으로 바꾼다. 스노우주사가 백옥주사와 재료 집합이 달라 갈리는지 확인.
2. §6-1 제네시스 = 지금대로(선택적 광열 레이저 · 대상 빈칸) · §6-4 열린 성분 수액 = 메뉴 · 패키지 · §6-5 · 6-6 = 보류(판정만, 코드 비움 — 나중에 원장 보강으로 채움) · §6-7 이름 = 지금대로.
3. §6-2 지방분해 주사 = **새 계열로 다른 워커가 처리 중**(drafts/combo-a/). 여기서는 「다른 계열」 판정 그대로, 손대지 않는다.

## 하지 않는 것

`silver/`·원장 · 다른 drafts 폴더(combo-a · combo-b · combo-c) 변경 금지. 커밋 · push 금지. 범위를 넓히지 않는다.

## 검증 (`combo-check.py` 갱신 — 코디가 다시 돌린다)

- 기존 검사 전부 + procedure_material: 모든 시술 ≥ 1행 · 참조 존재 · 중복 0 · 근거 ≥ 1 · procedure 에 material_code 칸 없음.
- 보존: 반영 전 시술 · 케이스 · 연결 · alias · 근거가 반영 후에 그대로 있음(재료 칸은 procedure_material 로 옮겨짐).
- 결과를 `combo-notes.md` 끝에 「## 7. 확정(11-14)」으로(무엇을 · 행 수 · 검증 출력).

## 완료 보고

preamble 의 `worker_done` 을 정확히 한 번(`--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/combo/combo-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "combo 시범 확정 완료: drafts/combo/combo-notes.md §7" --enter`
