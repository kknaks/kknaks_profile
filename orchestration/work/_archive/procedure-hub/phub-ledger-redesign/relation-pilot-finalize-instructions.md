# 지시서 — ③ 관계 시범 확정: 정규화 표 추가 · 제품 층 · 케이스 4 · 충돌 5

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 읽을 것

- `drafts/relation-pilot/` 전부(특히 `relation-notes.md` §4 · §6 · `relation-judgment.csv` 의 「담을 칸 없음」 227 · `relation-conflicts.csv` 5) · `relation-build.py` · `relation-check.py`
- 원래 발주서 `../relation-pilot-brief.md` · `silver/` 전부 · 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 사용자 결정 (11-15 「추천대로」 + 정규화)

**A. 담을 칸 없던 값 → 정규화해서 담는다.** 값이 하나뿐인 것만 칸, 여럿이거나 척도가 원장마다 다른 것은 표.

| 값 | 담을 곳 |
|---|---|
| 부정 진술(해당 없음 · 보고 없음) | `adverse_risk.polarity` 칸 — 값 3개로 고정: 발생함 / 해당 없음 / 보고 없음(기존 행은 발생함). 사전 후보 「중독」은 dict-candidates 유지 |
| 위험 등급(위험 부위 1~5 · bleedingRisk · swellingRisk …) | `rating_scale`(RSC — id · name · min · max · meaning_text(원장의 척도 설명 원문) · ledger) + `adverse_rating`(ARA — id · adverse_risk_id(또는 target_table · target_code — 사건 없는 등급) · scale_id · value · text). 척도가 다르면 다른 rating_scale 행 |
| 환자용 번역문 | `statement_translation`(STR — id · citation_link_id · lang(ko/en/zh/ja) · text) |
| PMC 번호 | `citation.pmc` 칸 |
| 다운타임 · 회복 기간 | `recovery`(REC — id · target_table · target_code · text/min/max/unit/qualifier) |
| 시너지 목표(효과) | `procedure_relation_effect`(PRE — id · relation_id · effect_code · text) |
| 연령대 · 사람 조건 권장 | `indication_condition`(INC — id · indication_id · condition_code · text) · `package_condition`(PKC — id · package_id · condition_code · text) |
| 패키지 기대 결과 · 총 기간 · 근거 수준 · 레시피 설명 | `package` 칸: expected_text · duration_text/min/max/unit/qualifier · evidence_text · subtitle · goal · intensity(원장에 있는 것만) |
| 패키지 후속 일정 | `package_schedule`(PKS — id · package_id · week_text/min/max · action_text) |
| 합의 수준(procedure_relation) | `procedure_relation.evidence_text` 칸 |

- 칸 · 표 이름은 위대로. 숫자 규칙 · 원문 그대로 규칙은 같다(숫자는 원문에 있을 때만). 이 밖에도 227 중 위 꼴로 담을 수 있는 것은 담고, 끝내 못 담는 것은 notes 판단 목록.

**B. 붙는 자리에 제품 추가.** `target_table` 에 `product` 허용(모든 관계 표 · package_item). 원장이 제품 · 제품 항목(taxonomy 제품 · 보톡스 엘러간 · 쥬비덤 …)에 대해 말한 값은 그 제품(silver product 코드)에 붙인다 — 지금 시술 층(PRC-001 · 100 · 101 · 102)에 붙인 제품 진술을 옮긴다(근거 포인터로 가린다). 제품이 사전에 없으면 시술 층 그대로 + dict-candidates.

**C. 케이스 4 추가(silver ② 에).** 보톡스 관자놀이(측두근) · 팔자(상순거근) · 입술(구륜근 — lip flip), 미간 히알루론산 필러를 `silver/procedure_case.csv` 에 행 추가(② 규칙: 원장이 말한 조합 · 대상 anatomy/tissue · site 하나 · 이름은 원장이 붙인 것만 · description 원장 인용 · source_ref). 코드는 그 시술 범위의 다음 번호(보톡스 CAS-0xx 대 · 히알루론산 필러 CAS-10xx 대 — 기존 코드와 겹치지 않게). 지금 시술 층 + note 로 둔 그 자리 관계 행을 새 케이스로 옮긴다. `notes/combo-item-judgment.csv` 에 해당 판정 행이 있으면 코드 채움. 필러 「코」는 두 케이스(콧대 · 코끝) 그대로.

**D. 충돌 5 (relation-conflicts.csv) = 각 행 추천:** RCF-001 둘 다 유지 · RCF-002 2~4주 채택(5일은 근거) · RCF-003 complications 3개월 이상 · RCF-004 treatment-sequence 「필러 먼저」 채택 · RCF-005 4주 이상(14일은 최소선 근거). 채택 쪽 행에 표시(`relation-conflicts.csv` 에 decision 칸 추가), 진 쪽 값은 행을 지우지 말고 그 행 source_ref 로 남기거나 행 유지 + 충돌 표시 — 지금 구조에서 값이 사라지지 않게.

**E. 그대로:** §6-5 쁘띠시술 = 적응 안 만듦.

## 쓰기 · 검증

- 고치기 전 `drafts/relation-pilot/` 를 `archive/relation-pilot-before-finalize/` 에, `silver/procedure_case.csv` · `silver/source_ref.csv` · `notes/combo-item-judgment.csv` 를 `archive/silver-before-relation-pilot-finalize/` 에 복사.
- silver 는 C 의 케이스 4행 · 그 근거 덧붙임만(기존 행 바이트 그대로). 관계 표는 drafts 에 그대로(silver 합치기는 나머지 계열까지 끝난 뒤).
- `relation-check.py` 갱신: 기존 검사 전부 + 새 표 · 칸 참조 · 근거 ≥ 1 · 원문 · 숫자 대조 · polarity 값 3개 밖 0 · rating 값이 그 scale 범위 안 · target_table=product 참조 존재 · 「담을 칸 없음」 = notes 판단 목록과 같음(227 → 몇) · 보존(반영 전 관계 값이 반영 후 어딘가에 — 옮긴 것 대응표) · silver 변경 = 케이스 4 + 근거만 · `git status`.
- 결과를 `relation-notes.md` 끝에 「## 9. 확정(11-15)」으로(무엇을 · 새 표 행 수 · 담을 칸 없음 전/후 · 옮긴 제품 진술 수 · 검증 출력). **이 표 구조가 나머지 계열의 기준이 되므로 §9 에 최종 표 · 칸 목록을 한 번에 적는다.**
- 원장 변경 · 커밋 · push 금지. 범위를 넓히지 않는다(M1 · M2 밖 계열 하지 않음).

## 완료 보고

preamble 의 `worker_done` 을 정확히 한 번(`--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/relation-pilot/relation-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "관계 시범 확정 완료: drafts/relation-pilot/relation-notes.md §9" --enter`
