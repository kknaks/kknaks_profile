# 발주서 — 계열 테이블 설계 (phub-ledger-redesign)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 경로는 이 레포 기준.

## 1. 목표

피부과 시술 원장 21개를 정규화한 실버 ERD 를 위에서부터 다시 세우고 있다. 큰 분류 8개(1 시술 · 2 재료·기구 · 3 인체 · 4 결과 · 5 사람 · 6 시술 간 · 7 판매 · 8 근거) 중 **1 시술의 맨 위 = 계열(M1~M17)** 부터 설계한다.
계열은 taxonomy 를 뺀 원장 20개 중 18개가 M 코드로 가리키는 공통 축이고, 원장 주장의 상당수가 계열 단위로 적혀 있다. 계열을 세우면 그 아래 시술 → 적용 케이스(시술 + 부위·제품·기법·반복 등 좁힘)로 내려가며 계열 주장을 상속한다.

이번 범위는 **계열과 그 바로 아래(하위분류)의 뼈대, 그리고 원장들이 계열을 가리키는 방식**까지다. 시술 행 전체·케이스·부작용·부위 목록은 하지 않는다.

## 2. 산출물 (이 파일만 만든다)

`orchestration/work/phub-ledger-redesign/silver-model/family-design.md`

그 밖의 파일은 만들거나 고치거나 지우지 않는다. 원장·`first-pass/`·`silver-model/` 다른 파일은 읽기 전용. 이슈 목록·관리 문서를 따로 남기지 않는다(임시 스크립트는 레포 밖 임시 경로에서만). 커밋·push 하지 않는다.

## 3. 읽을 것

1. 원장(브론즈 3판 · 최신 기준): `orchestration/work/phub-recommend/bronze/phub-ledger/*.json` — 특히 `taxonomy.json` 의 `modality[]`(id·category·category_en·group·name·extracted·products·subcategories[].id/label/description/items[].name/detail 및 드문 키 reclassified_to·canonical_category·classification_issue 등).
2. 계열을 가리키는 다른 원장 전부(extracted 의 키 `M1`… 와 procedure_id, consent·complications·post-procedure-timeline 의 category, pih-risk `notes` 의 `M1_to_M7` 같은 범위 키, treatment-sequence `sequence_order[].categories`, synergy·market-pricing·products 의 category_id·섹션 등).
3. 시범 결과(틀 참고): `silver-model/pilot-botox-adverse.md` §3.3·§5 — 케이스 개념과 상속.
4. 색인: `first-pass/<원장>/source-map.json` — 누락 확인용으로만. first-pass 의 해석은 믿지 말고 원문으로 판단.
5. 대조용(전제 아님): `silver-model/tables-v0.md` §2 의 1 procedure·19 catalog_node·§3 상하위 절.

## 4. 할 일

**A. 계열 17개마다 정의**
- 묶는 기준이 무엇인가 — 재료(보톡스·필러), 에너지원·장비 원리(레이저·기기 리프팅), 기법(MTS·니들RF), 관리 묶음(메디컬스킨케어), 기타. 원문 근거(category·overview·mechanism·하위분류 구성)로 판단.
- 그 계열이 **시술의 상위 개념**(「레이저」를 받는다 = 시술)인지, **분류 이름일 뿐**(묶음)인지 판정. 원장이 그 계열 단위로 시술처럼 주장을 적는지(예: consent 「보톡스는 영구적이 아니며 …」)를 근거로.
- 그룹(주사/주입 · 시술/기기 · 관리)의 위치 — 계열 위 층으로 둘지.

**B. 하위분류 74개 판정**
하위분류마다 성격을 원문으로 가린다: 하위 시술(원리·재료가 갈림 — 「HIFU (초음파)」「PLLA」) / 제품 분류(원산지 「수입·국산」, 브랜드, 재질별·형태별처럼 제품을 묶는 칸) / 용도·메뉴 묶음(「용도별」「시그니처 프로그램」) / 기타(「추가」「기타」). 하위 시술이면 계열과 is-a, 제품 분류면 시술 축이 아니라 「2 재료·기구」 쪽으로 넘긴다고 표시만 한다(제품 설계는 하지 않는다).

**C. 계열 사이의 겹침·재배치**
엑소좀(M4·M17), PDO(M3·M7), SVF(M6·M17), 볼뉴머(M4·M9), 그 밖에 찾은 것. taxonomy 의 reclassified_to·canonical_category·classification_issue 메모 포함. 같은 것인지, 다른 것인지(같은 재료라도 다른 시술), 어디로 두는지 판정과 근거.

**D. 원장이 계열을 가리키는 방식 → 하나로 연결**
원장마다 계열을 어떻게 적는지 전수: M 코드 · `M1-BOTOX` 같은 합성 id · `M1_to_M7` 범위 · `M16-DCA`·`M15-도포` 같은 하위 코드 · 이름 표기 차이(market-pricing 「PRP/엑소좀」「에너지기기(HIFU/RF)」 등) · 영문 슬러그(timeline id 등). 각 표기가 어느 계열(또는 하위분류)을 가리키는지 대응표. 대응이 안 되는 표기는 원문과 함께.

**E. 계열 단위로 붙는 정보의 종류**
원장들이 계열 단위로 적는 정보가 무엇인지 종류만 정리한다(개요·기전·적응·금기·부작용·효과 시간·관리·고지·가격 범위·PIH·시간 순서 …, 원장·키 경로). 값을 옮기지 않는다 — 이것들이 나중에 계열 → 시술 → 케이스로 상속될 대상이라는 것을 확인하는 목록이다.

## 5. 설계 기준 (사용자 합의)

- 시술은 부위 없이 한 행. 부위·제품·기법·반복 등은 적용 케이스의 좁힘이다. 계열·시술·케이스는 is-a 로 위아래가 이어지고, 주장은 원문이 적힌 층에 저장하고 아래로 상속한다(복사하지 않는다).
- taxonomy 트리를 그대로 is-a 로 옮기지 않는다. 층마다 성격을 원문으로 가린다.
- 같은 문자열이라도 역할이 다르면 합치지 않는다. 원문에 없는 사실을 보충하지 않는다. 문맥으로 판단 가능한 것은 판단해서 채우고 미루지 않는다.
- 테이블은 적게. 계열을 별도 테이블로 둘지, 시술 테이블의 최상위 행(종류 칸)으로 둘지 둘 다 따져 추천하고 이유를 적는다.

## 6. 문서 형식

1. **계열 17 정의 표** — 코드 · 이름 · 그룹 · 묶는 기준 · 시술인가/묶음인가 · 근거(원장·포인터·원문).
2. **하위분류 74 판정 표** — 계열 · 하위분류 · 성격(하위 시술 / 제품 분류 / 용도·메뉴 / 기타) · 근거 · 다음 행선지.
3. **겹침·재배치 판정** — 대상 · 원문 · 판정 · 근거.
4. **계열 참조 대응표** — 원장 · 표기 · 가리키는 계열(·하위분류) · 비고. 대응 안 되는 표기 목록.
5. **계열 단위 정보 종류 목록**.
6. **테이블 설계** — 계열(또는 시술 최상위) · 계열 상하위(그룹 > 계열 > 하위 시술) · 계열 표기 대응(별칭) 등 필요한 테이블과 칼럼, 각 칼럼의 실제 값 예. 담을 칸 없는 값 0 또는 원문과 함께.
7. **사용자 판단이 필요한 것** — 원문으로 판단 가능한 것은 판단해서 반영하고, 실제 선택만 원문·이유·추천·선택지·영향과 함께. 없으면 비운다.

분량은 표 위주로 대략 400행 이하.

## 7. 완료 기준

- 계열 17·하위분류 74 가 전부 판정돼 있고 근거가 원문 포인터로 달려 있다.
- 원장 20개의 계열 표기가 전부 대응표에 있다(대응 안 되는 것은 원문과 함께).
- 테이블 설계가 있고 담을 칸 없는 값이 0 이거나 원문과 함께 적혀 있다.
- 산출물은 `silver-model/family-design.md` 하나. `git status` 로 다른 변경이 없음을 확인한다.

## 8. 질문

설계를 실제로 막는 것이 있으면 먼저 원문을 확인하고, 그래도 사용자 선택이 필요하면 preamble 의 ask 로 묻는다. 범위를 혼자 넓히지 않는다(시술 행 전체·케이스·부작용·부위로 넘어가지 않는다).

## 9. 완료 보고

preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/family-design.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "family-design 완료: orchestration/work/phub-ledger-redesign/silver-model/family-design.md" --enter`
