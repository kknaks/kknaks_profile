# 지시서 — ② 조합 합치기: 네 초안 → silver

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

Procedure Hub 실버 ② 조합(시술 종류 · 케이스)을 네 워커가 나눠 만들었다. 모두 각자 검증 PASS:

| 초안 | 계열 | 코드 |
|---|---|---|
| `drafts/combo/` (시범) | M1 · M8 · M16 | PRC-001~ · CAS-001~ |
| `drafts/combo-a/` | M2 · M3 · M4 · M5 · M6 · M17 + 새 계열 M18 지방분해 주사 | PRC-100~ · CAS-1000~ |
| `drafts/combo-b/` | M7 · M9 · M10 · M11 · M14 | PRC-300~ · CAS-3000~ |
| `drafts/combo-c/` | M12 · M13 · M15 | PRC-500~ · CAS-5000~ |

이번 일: 넷을 **한 벌로 합쳐 silver 에 올린다.** 판정 · 조합 내용은 바꾸지 않는다(아래 §3 결정과 §4 겹침 정리만).

## 2. 읽을 것

- 네 초안 폴더 전부(notes · build · check 스크립트 포함)
- `silver/` 전부 · 원래 발주서 `../combo-pilot-brief.md` · `../combo-a-brief.md`(형식 기준)
- 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 3. 사용자 결정 (11-14 「추천대로」)

- 네 notes §6 판단 전부 = 각 notes 의 **추천대로**(데이터 그대로). 특히: B §6-1 실 = 재질 × 원리(지금대로) · B §6-4 인모드FX = 고주파 시술까지만, 케이스 비움 · B §6-5 잼버실 = 제품만, 코드 비움 · C §6-7 모발이식 = 보류 · B §6-7 problem-packages 「지방분해」(M14 자리) = 분류 칸, 코드 비움.
- 인모드FX(원장 「RF 니들」 ↔ 제품 사전 비침습 RF) · 잼버실(원장 PCA ↔ 제품 사전 PDO)은 `notes/product-ledger-check-list.csv` 에 행 추가(원장 작성자 확인 목록 — 기존 행 바이트 그대로, 같은 칸 형식).
- **새 계열 M18**: `drafts/combo-a/modality-add.csv` 의 행을 `silver/modality.csv` 끝에 붙인다. `drafts/combo-a/product-modality-change.csv` 11행을 `silver/product_modality.csv` 에 반영(M16 → M18 바꿈 · LDM 의 M16 연결 삭제). 근거는 source_ref.

## 4. 합칠 때 할 일

1. **겹침 점검**(표를 notes 에):
   - 같은 원장 포인터를 둘 이상의 초안이 판정한 것 — 판정 · 코드가 같으면 하나로, 다르면 **그 계열을 맡은 묶음의 판정을 따르고** 다른 쪽(「다른 계열」 판정 등)은 그 행으로 대체. 둘 다 시술 · 케이스로 잡았으면 판단 목록(아래 6).
   - 같은 이름(name_ko 또는 alias, 띄어쓰기 무시)이 둘 이상의 시술 · 케이스에 걸린 것 — 원장이 다르게 쓰면 그대로 + 표, 같은 것이면 판단 목록. 알려진 후보: 「두피 메조테라피」(A 는 미녹시딜을 M15 로, C 는 멀티니들 주입 케이스로) · 엑소좀 · 콜라겐 · PDO(M3 시술 vs M7 실) · 고주파(M9 vs 니들RF).
   - 같은 (계열 · 재료 집합 · 원리) 시술 종류가 묶음 사이에 생긴 것 = 0 이어야 한다(있으면 판단 목록).
2. **코드**: 시술 · 케이스 코드는 그대로 둔다(PRC-001 … · CAS-001 …). 연결 표 id 는 silver 관례(`ANS-0001` 꼴)대로 다시 매긴다: procedure_material `PMA-0001` · case_method `CME-0001` · case_product `CPR-0001`. source_ref 의 target_id 도 새 id 로 바꾸고 옛 id → 새 id 대응표를 notes 에.
3. **silver 에 새로 둘 표**: `procedure.csv` · `procedure_material.csv` · `procedure_case.csv` · `case_method.csv` · `case_product.csv`. 공통 `alias.csv` · `source_ref.csv` 에는 시술 · 케이스 · 연결 행을 **덧붙인다**(기존 행 바이트 그대로, 같은 행 중복 제거).
4. **silver 밖(notes/)에 둘 것**: `notes/combo-item-judgment.csv`(네 판정 합본 — 계열 칸 추가) · `notes/combo-dict-candidates.csv`(사전 추가 후보 합본 — 같은 후보는 한 행, 어느 묶음에서 왔는지 칸) · `notes/combo-notes.md`(아래 §6).
5. 고치기 전: `silver/` 전체를 `archive/silver-before-combo/` 에, 네 초안 폴더를 `archive/combo-drafts-before-merge/` 에 복사. 초안 폴더 자체는 지우지 않는다.

## 5. 검증 (`drafts/combo-merge/merge-build.py` · `merge-check.py` — 코디가 다시 돌린다)

- 네 초안의 check 기준 전부를 합본에 대해 다시(참조 존재 · `;` 0 · 이름 괄호 0 · 근거 ≥ 1 · 「」 인용 원장 글자 그대로 · 케이스 조합 중복 0 · 시술 정체 중복 0 · 모든 시술 procedure_material ≥ 1).
- 보존: 네 초안의 시술 · 케이스 · 연결 · alias · 근거가 합본에 전부 있음(id 바뀐 것은 대응표로) · 판정 행 전부(대체한 것은 표로).
- modality 18행 · M18 참조 존재 · product_modality 변경 = 11행 그대로 · 그 밖 silver 표(사전 · 기존 관계) 바이트 불변 · alias/source_ref 앞쪽 행 바이트 그대로.
- **매핑 현황 집계**(notes 에 숫자로): 시술 · 케이스 수(계열별) · 원리 빈 시술 · 대상 빈 케이스 · 케이스에 못 닿고 시술까지만 닿는 제품 · 어느 시술에도 안 닿는 시술용 제품 · 보류 판정 · 메뉴 · 패키지 판정 · 사전 추가 후보 수(사전별).
- `git status` 로 산출물 외 변경 없음.

## 6. notes (`notes/combo-notes.md`, 짧게)

1. 합친 결과 행 수 · 계열별 시술 · 케이스 수
2. 겹침 점검 표(포인터 겹침 · 이름 겹침 · 처리)
3. id 대응표 위치 · M18 · product_modality 변경 내역
4. 매핑 현황 집계(§5 마지막)
5. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지(겹침에서 나온 것만)
6. 검증 출력

## 7. 하지 않는 것 · 완료 보고

판정 · 조합을 새로 하지 않는다 · 사전(material · mechanism 등)에 행 추가하지 않는다 · ③ 관계 · 외부 조사 하지 않는다 · 원장 변경 금지 · 커밋 · push 금지.
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/notes/combo-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "combo 합치기 완료: silver-model/notes/combo-notes.md" --enter`
