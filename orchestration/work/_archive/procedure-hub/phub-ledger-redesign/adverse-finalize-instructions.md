# 지시서 — 부작용 개념 사전 확정: 결정 12건 반영 + silver 합치기

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 읽을 것

- `drafts/adverse/` 전부(특히 `adverse-notes.md` §3 · §4 · §6 판단 12건) · `adverse-build.py` · `adverse_lexicon.py` · `adverse-check.py`
- `silver/` 전부(공통 `alias.csv` · `source_ref.csv`)
- 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 사용자 결정 (「추천으로」)

- §6 1 · 2 · 3 · 4 · 5 · 7 · 8 · 9 · 10 · 11 · 12 = **지금대로(A / 현재 자리)**.
- §6 **6 = B: 「미소 비대칭」 행 신설** — 원장 complications M1 기전 문장(「미소 특이 비대칭은 … '비대칭 미소'로 별도 분리」)이 분리를 명시. 이름은 원장 표현 중 명사형(「비대칭 미소」를 명사형으로 하면 「미소 비대칭」 — 원장 표기 「비대칭 미소」는 alias 별칭), 부모 = 비대칭 행, level 소분류(비대칭은 중분류로). 원장에서 미소 비대칭을 가리키는 자리는 비대칭 행에서 이 행으로 옮긴다(가를 수 있는 것만, 못 가르면 비대칭에 그대로). 설명 · 근거 규칙 같음. 그 밖 자리를 뺀 이름(눈썹 처짐 · 교근 섬유화 · 하악변연신경 손상)은 지금대로 합침 유지.

## silver 합치기

- 고치기 전 `silver/alias.csv` · `silver/source_ref.csv` 를 `archive/silver-before-adverse/` 에, 반영 전 drafts 를 `archive/adverse-before-finalize/` 에 복사.
- `silver/adverse.csv` 새로 두고, 부작용 계열 alias · source_ref 행을 공통 표에 덧붙인다(기존 행 바이트 그대로). drafts 도 최종판으로 갱신.

## 검증 (`adverse-check.py` 갱신 — 코디가 다시 돌린다)

- 기존 검사 전부(silver 기준) + 미소 비대칭 행 있음 · 부모 = 비대칭 · 깊이 ≤ 3.
- 보존: 반영 전 이름(name_ko ∪ alias) ⊆ 후 · 반영 전 근거 ⊆ 후.
- silver 의 부작용 밖 표 바이트 불변 · alias/source_ref 앞쪽 행 바이트 그대로.
- 결과를 `adverse-notes.md` 끝에 「## 7. 확정(11-12)」으로(무엇을 · 행 수 전/후 · 옮긴 근거 · 검증 출력).

## 완료 보고

범위를 넓히지 않는다. preamble 의 `worker_done` 을 정확히 한 번(`--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/adverse/adverse-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "adverse 확정 완료: drafts/adverse/adverse-notes.md §7" --enter`
