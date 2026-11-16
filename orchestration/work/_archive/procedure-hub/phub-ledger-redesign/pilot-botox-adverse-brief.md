# 발주서 — 시범: 보톡스 × 부작용 교차 비교 (phub-ledger-redesign)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 경로는 이 레포 기준.

## 1. 목표

피부과 시술 원장 21개를 정규화한 실버 ERD 를 설계하고 있다. 원장마다 같은 시술의 같은 부작용을 다르게 적어서(이름·빈도·시기·키 이름이 제각각) 이전 설계가 「원장 문장 한 줄 = 한 행」으로 흩어졌다.
이번 시범은 **보톡스 한 시술의 부작용만** 원장 21개에서 전부 모아, 원장끼리 나란히 비교하고, **적용 케이스당 값 하나**로 정리했을 때 담기는 테이블 구조를 실제 값으로 시험한다.

## 2. 산출물 (이 파일만 만든다)

`orchestration/work/phub-ledger-redesign/silver-model/pilot-botox-adverse.md`

그 밖의 파일은 만들거나 고치거나 지우지 않는다. 원장(`orchestration/work/phub-recommend/bronze/`)·`first-pass/`·`silver-model/tables-v0.md` 는 읽기 전용. 이슈 목록·관리 문서·스크립트 산출물을 따로 남기지 않는다(값 수집용 임시 스크립트는 레포 밖 임시 경로에서만 돌리고 결과만 문서에 옮긴다). 커밋·push 하지 않는다.

## 3. 읽을 것

1. 원장(브론즈 3판 · 이것이 최신 기준 데이터): `orchestration/work/phub-recommend/bronze/phub-ledger/*.json` 21개.
2. 색인: `orchestration/work/phub-ledger-redesign/first-pass/<원장>/source-map.json` — 모든 값의 포인터·원문. **누락 확인용 색인으로만** 쓴다. first-pass 의 해석·관찰은 믿지 말고 원문으로 판단한다. morphology.json 은 열지 않는다.
3. 참고(대조용, 전제 아님): `orchestration/work/phub-ledger-redesign/silver-model/tables-v0.md` §2 의 12 `adverse_event`, 23 `adverse_risk`, 2 `procedure_ref` 절.

## 4. 범위 — 「보톡스 부작용」 값을 빠짐없이

보톡스(계열 M1 · 그 하위분류·항목·제품 · 스킨보톡스·메조보톡스 같은 변형 포함)에 대해 원장이 적은 **부작용 관련 값** 전부. 최소한 아래 자리를 본다. 이 밖에도 보톡스 부작용을 말하는 자리가 있으면 source-map 과 원문 검색으로 찾아 넣는다.

- extracted `M1.safety.*` · taxonomy `modality[M1].extracted.safety.*` · 그 아래 하위분류 항목·제품의 `extracted.safety.*`
- complications 의 보톡스 카테고리(이름·severity·incidence·onset·duration·mechanism·risk_factors·management·prevention)
- consent-checklist `M1` mandatory_disclosures · emergency_signs
- post-procedure-timeline 보톡스 타임라인(phases × normal/abnormal/caution/emergency)
- anatomy-danger-zones `zones[].botox_specific`(risk·key_warning 등)·critical_safety_facts 중 보톡스
- literature-evidence `M1.adverse_effects`
- patient-education 보톡스 범주 · procedure-comparison · pih-risk(`notes` 의 M1 포함 범위) · pre-procedure-checklist 의 보톡스 관련

부작용이 아닌 것(효과·금기·고민)은 넣지 않는다. 단 같은 말이 다른 역할로 쓰인 사례(예: 「눈꺼풀 처짐」이 부작용이 아니라 치료 대상 고민으로 쓰인 patient-education)는 「역할이 다른 같은 표현」으로 짧게 적는다.

## 5. 합의된 모델 (이 틀로 쪼갠다)

**부작용 개념** — 명칭(의학용어) · 별칭(일반용어) · 현상 설명[]. 원장 표현은 셋 중 어디에 해당하는지 판정해 붙인다. 한 표현에 사건이 둘이면 나눈다(「윗눈꺼풀이나 눈썹이 처지는 현상」 = 안검하수 + 눈썹 처짐). 「주사 부위 반응 (부종·압통·멍·홍반)」 같은 묶음은 상위 사건 + 하위 사건(is-a)으로.

**적용 케이스** — 단위 시술(보톡스) + 원장이 적은 좁힘(부위 · 제품 · 용량 · 기법 · 반복 여부 등). 부위가 없으면 보톡스 자체. 부작용은 이 케이스에 붙는다.

**케이스 × 부작용 = 값 하나 + 출처 여럿.** 칸:
- 빈도 {원문 · 수치 범위(있을 때만) · 분모/대상(있을 때만) · 서술 등급} — 서술 등급은 우리가 정하는 순서 척도(대부분 > 흔함 > 가끔 > 드묾 > 매우 드묾). **%로 바꾸지 않는다.** 원장 키 `common`/`uncommon` 은 빈도 등급 근거로 쓴다.
- 심각도 — 원장 키 `serious`/`emergency` 는 **빈도가 아니라 심각도**다. complications severity 등.
- 발현 · 지속 {원문 · 값 범위(있을 때만) · 단위 · 기준점(시술 후/발현 후) · 수식(대개 등)} — 「수일」처럼 숫자 없는 말은 단위 수준까지만, 숫자를 만들지 않는다. timeline 단계는 그 단계의 period 를 시기로.
- 정도(경미/심함) · 조건·원인(「안와상연 너무 가까이 주사 시」「반복 시술 시」) · 출처[](원장 · 포인터 · 원문)

**원장끼리 다를 때 — 셋 중 하나로 가린다**
1. **같은 케이스가 아니었다** — 조건(부위·제품·용량·기법·반복)이 다르다 → 적용 케이스를 나눈다.
2. **칸을 잘못 읽어 달라 보였다** — 예: 빈도 uncommon vs 「드물게」 vs `serious`(심각도) → 칸을 바로 나누면 같다 → 하나로 합치고 출처 둘 다 기록.
3. **진짜 불일치** — 예: extracted 「드물게 … 감기 비슷한 증상」 vs complications 독감 유사 증상 「1.7-20%」 → 충돌로 표시하고 어느 값을 쓸지 추천과 이유. 임의로 고르지 않는다.
완전히 같은 복사본(extracted `M1` = taxonomy 계열 extracted 처럼)은 같은 출처 하나로 센다(복사 관계 표시).

외부 임상 사실로 보충하지 않는다. 원문에 없는 칸은 비운다. 문맥으로 판단 가능한 것(수식 대상·기준점·역할)은 판단해서 채우고 「미결」로 미루지 않는다.

## 6. 문서 형식

1. **수집 범위** — 본 원장·자리별 값 개수, source-map 대조로 빠진 값이 없음을 어떻게 확인했는지(포인터 목록 대조 방식 한 단락).
2. **부작용 개념 표** — 명칭 · 별칭 · 현상 설명 · 상위 사건 · 이 개념에 붙은 원장 표현(원장·포인터).
3. **케이스 × 부작용 비교 표** — 행 = (적용 케이스, 부작용). 원장별 원문을 나란히 놓고 → 정리된 값 하나(빈도·심각도·발현·지속·정도·조건) → 차이 판정(1/2/3/차이 없음).
4. **판정 3(진짜 불일치) 목록** — 원문 · 이유 · 추천 · 선택지 · 영향. 사용자 판단 대상은 이것만.
5. **테이블 초안** — 이 시범 값을 담는 데 필요한 테이블과 칼럼(부작용 개념 · 별칭 · 현상 설명 · 상위 사건 · 적용 케이스 · 케이스×부작용 · 출처 · 충돌 등). 각 칼럼에 실제 값 예. 그리고 「담을 칸이 없었던 값」 — 있으면 원문과 함께, 없으면 0 이라고.
6. **v0 대비 바뀐 점** — tables-v0 의 `adverse_event`·`adverse_risk`·`procedure_ref` 와 무엇이 달라졌는지 몇 줄.

분량은 표 위주로, 대략 400행 이하.

## 7. 완료 기준

- §4 자리의 보톡스 부작용 값이 전부 2·3번 표에 들어가 있고, 빠짐 확인 방법이 적혀 있다.
- 원장 차이가 전부 1/2/3/차이 없음 중 하나로 판정돼 있다.
- 5번 테이블 초안의 「담을 칸 없는 값」이 실제로 0 이거나 원문과 함께 적혀 있다.
- 산출물은 `silver-model/pilot-botox-adverse.md` 하나. `git status` 로 다른 변경이 없음을 확인한다.

## 8. 질문

설계를 실제로 막는 것이 있으면 먼저 원문을 확인하고, 그래도 사용자 선택이 필요하면 preamble 의 ask 로 묻는다. 범위를 혼자 넓히지 않는다(다른 시술·다른 분류로 넘어가지 않는다).

## 9. 완료 보고

preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/pilot-botox-adverse.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "pilot-botox-adverse 완료: orchestration/work/phub-ledger-redesign/silver-model/pilot-botox-adverse.md" --enter`
