# 발주서 — 시술 · material · tissue 세트 시범 (M1 · M8 · M16)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 경로는 이 레포 기준.

## 1. 목표 · 배경

피부과 시술 원장 21개를 실버로 정규화한다. 개체를 하나씩 확정하고 **연결 관계는 개체가 다 선 뒤에** 그린다.
확정: `silver-model/data/modality.csv`(M1~M17).

이번에는 **시술(procedure) · 재료·에너지(material) · 작용 대상 조직(tissue)** 세 테이블을 **한 세트로** 정한다. 시술 하나를 판정할 때 그 재료와 작용 대상이 같이 정해지기 때문이다.
앞서 material·tissue 를 따로 뽑았더니 정규화가 안 됐다(상·하위가 같은 층에 나란히 · 같은 개념이 두 테이블에 · 조직 아닌 것 섞임 · 단위 제각각 · 시술에 실제로 쓰이는지 기준을 못 씀). 그 CSV 는 **후보 목록으로만** 쓴다.

**시범 범위: modality M1 보톡스 · M8 레이저 · M16 수액치료** 세 개뿐. 규칙이 통하는지 보고 나머지로 넓힌다.

## 2. 산출물 (이 다섯만 · 새 폴더)

`orchestration/work/phub-ledger-redesign/silver-model/data/pilot-set/` 아래:
- `procedure.csv` · `procedure_name.csv` · `material.csv` · `tissue.csv`
- `item-judgment.csv` — 원장 항목별 판정
- `pilot-set-notes.md` — 짧게, 표 위주

CSV 는 **UTF-8 BOM**(`utf-8-sig`) · 쉼표 · 필요한 칸 큰따옴표. 그 밖의 파일은 만들거나 고치거나 지우지 않는다(기존 `silver-model/data/*.csv` 포함 — 읽기만). 커밋·push 금지.

## 3. 읽을 것

- 원장(브론즈 3판): `orchestration/work/phub-recommend/bronze/phub-ledger/*.json` — M1·M8·M16 에 해당하는 것: taxonomy `modality[0]`·`[7]`·`[15]`(하위분류·항목 name/detail/extracted·products) · extracted `M1`·`M8`·`M16`(overview·mechanism·related_techniques) · procedure-profiles · procedure-comparison · pih-risk(M8 procedures — 파장·펄스) · patient-education · products.json(해당 섹션).
- 확정분: `silver-model/data/modality.csv` · `modality-notes.md`(§2 하위 층으로 넘긴 기전 문장 — 시술 기전으로 쓴다).
- 후보: `silver-model/data/material.csv` · `tissue.csv` · `material-tissue-notes.md`(합친 표기·상위 후보·§4 판단 10건의 추천).
- 색인(누락 확인): `first-pass/<원장>/source-map.json`.

## 4. 사용자와 정한 정의 · 규칙

**시술** = 재료·에너지(material) + 작용 대상 조직(tissue) + 작용 원리가 같으면 같은 시술. 셋 중 하나라도 다르면 다른 시술.
- 보톡스(톡신 · 근육 · 아세틸콜린 차단) ≠ 스킨보톡스(톡신 · 피지샘·모공(진피) · 아세틸콜린 차단). **스킨보톡스 = 메조보톡스 = 더모톡신** 은 한 시술(사용자 확정).
- **부위는 시술의 정체가 아니다**(이마·사각턱 보톡스는 보톡스 한 행).
- **제품·장비 브랜드는 시술이 아니다**(보툴렉스·디스포트·피코슈어 — 제품).
- 레이저: **재료 = 파장(매질)**, **펄스(피코초 광음향 / Q-스위치·롱펄스 광열)는 작용 원리** 쪽(material-tissue-notes §4-3 추천 채택).

**원장 항목 판정**(item-judgment) — 각 항목을 하나로: `시술` / `제품` / `케이스`(시술 + 부위 등 좁힘) / `메뉴`(판매 이름·프로그램) / `성분` / `분류 칸` / `시술 아님`(홈케어·처방약 등) / `재분류`(다른 modality 로 — 어디로 갈지 후보). 판정 근거(원문 짧게)와 가리키는 시술 코드(있으면).

**material 정규화**
- 이 세 modality 의 시술이 **실제로 쓰는 것만**.
- 같은 층은 같은 단위(물질 종류 / 에너지 종류). 하위(글리콜산 ⊂ AHA · 1064nm ⊂ Nd:YAG 등)는 `parent_code` 로 상위를 가리킨다 — 상위·하위를 평평하게 나란히 두지 않는다.
- 한 개념은 한 행, 그리고 material·tissue 둘 중 **한 테이블에만**.

**tissue 정규화**
- **층(깊이)** 과 **구조(조직·기관·세포)** 만. 표적 물질(멜라닌·헤모글로빈·물)은 빛 시술의 작용 대상이라 필요하면 `kind=표적` 으로 둔다. 병변(면포·흉터)·미생물·투여 경로(혈류)·모공(구멍)은 tissue 가 아니다 — 필요하면 notes 에 어디로 가야 하는지만.
- 수액(M16)처럼 국소 조직이 없으면 시술의 target 을 비우고 이유를 notes 에.

**공통**: 원장에 있는 값만, 외부 지식 보충 금지. 문맥으로 판단 가능한 것은 판단해서 채운다. 이름·별칭은 **그 이름이 실제로 무엇을 가리키는지** 원문으로 확인하고 그 대상에만 넣는다.

## 5. 테이블 칼럼

**`procedure.csv`**: `code`(P-001…) · `name_ko` · `name_en` · `modality_code` · `material_code` · `target_code`(→ tissue) · `principle`(짧은 값: 「아세틸콜린 차단」「선택적 광열」「광음향」…) · `overview` · `mechanism` · `method`(시행 방법 한두 문장: 깊이·농도·주사 방식 등 원장에 있을 때) · `basis`(포인터).
- 재료가 둘 이상 섞이는 시술(마이어스칵테일 같은 혼합 수액)은 대표 재료 하나 + notes, 또는 판단을 notes 에.

**`procedure_name.csv`**: `procedure_code` · `name` · `name_type`(다른 이름 / 영문 / 약어) · `basis`. 같은 시술임을 원문으로 확인한 이름만. 제품명·메뉴명·부위 붙은 이름은 넣지 않는다.

**`material.csv`**: `code`(MAT-…) · `name_ko` · `name_en` · `kind`(물질 / 에너지 / 기계적 자극) · `parent_code` · `description`(원장 근거 한 문장, 없으면 비움) · `basis`.

**`tissue.csv`**: `code`(TIS-…) · `name_ko` · `name_en` · `kind`(층 / 구조 / 표적) · `parent_code` · `description` · `basis`.

**`item-judgment.csv`**: `source`(원장) · `pointer` · `name`(원문) · `judgment` · `procedure_code`(해당 시 · 케이스·메뉴·제품은 가리키는 시술) · `reason`(원문 근거 짧게).

## 6. notes 형식

1. 판정 집계(modality × 판정 종류 개수)와 누락 확인 방법(한 단락)
2. 시술 목록 요약(modality 별 시술 이름 · 재료 · 대상 · 원리) — 왜 이 단위로 나눴는지 한 줄씩
3. 재분류 대상(항목 · 원문 · 갈 곳 후보)
4. 후보 CSV 대비 바뀐 점(합친 것 · 상위로 묶은 것 · tissue 에서 뺀 것)
5. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지. 판단 가능한 건 판단하고 여기 올리지 않는다.

## 7. 완료 기준

- M1·M8·M16 의 원장 항목(taxonomy 하위분류·항목·제품 + 다른 원장의 해당 시술 이름)이 전부 item-judgment 에 판정돼 있다.
- 시술마다 material·target 이 채워졌거나 비운 이유가 있다. material·tissue 에 시술이 쓰지 않는 값이 없다. 상위·하위가 parent 로 이어졌고 한 개념이 두 테이블에 있지 않다.
- 산출물 외 변경 없음(`git status`).

## 8. 질문 · 9. 완료 보고

막히면 원문을 먼저 확인하고, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(다른 modality · 부위 · 제품 테이블 · 연결로 넘어가지 않는다).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/data/pilot-set/pilot-set-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "procedure-set-pilot 완료: orchestration/work/phub-ledger-redesign/silver-model/data/pilot-set/" --enter`
