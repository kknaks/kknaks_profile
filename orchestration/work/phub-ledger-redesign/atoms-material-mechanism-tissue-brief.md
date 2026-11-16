# 발주서 — 기본 단위: 재료/에너지 · 작용 기전 · 작용 대상 조직 (계열 17개 전체)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 경로는 이 레포 기준.

## 1. 목표 · 사용자와 합의한 구조

Procedure Hub 는 **시술 원장**이다. 목표는 고민 · 시술 이름 · 제품 어느 쪽에서 들어와도 같은 시술에 정확히 도착하는 데이터다.
실버는 3층으로 만든다:

```text
① 기본 단위(사전): 계열 · 재료/에너지 · 작용 기전 · 작용 대상 조직 · 부위 · 제품/장비 · 방법 · 고민 · 효과 · 부작용 · 사람 조건
② 조합: 시술 = 재료/에너지 + 작용 기전 (+ 계열) · 케이스 = 시술 + 작용 대상 · 부위 · 방법 · 제품
③ 관계: 적응 · 부작용 위험 · 금기 · 시술 간(보완·같은 날·순서·간격·회피)
```

**아래 층부터 만든다.** 확정: 계열(`silver-model/data/modality.csv`). 이번 일은 ① 중 **재료/에너지 · 작용 기전 · 작용 대상 조직** 세 사전을 계열 17개 전체에 대해 만드는 것이다. 시술·케이스 목록, 부위, 제품, 관계는 만들지 않는다.

이 세 사전은 시술과 케이스를 정의하는 재료다:
- 보톡스 = 보툴리눔 톡신 A형(재료) + 아세틸콜린 차단(기전). 근육 / 피지샘(스킨보톡스) / 땀샘(다한증)은 작용 대상 → 케이스.
- 기기 리프팅: 고주파 + 조직 가열 / 집속 초음파 + 열응고 / 마이크로웨이브 + … — 에너지가 다르면 다른 시술.
- 수액: **성분이 다르면 다른 시술**(사용자 확정): 백옥주사 = 글루타치온, 마늘주사 = 비타민B1, 신데렐라주사 = 알파리포산.

## 2. 산출물 (새 폴더 · 이것만)

`orchestration/work/phub-ledger-redesign/silver-model/data/atoms/` 아래:
`material.csv` · `mechanism.csv` · `tissue.csv` · `atoms-notes.md`

CSV 는 **UTF-8 BOM**(`utf-8-sig`) · 쉼표 · 필요한 칸 큰따옴표. 그 밖의 파일은 읽기만(기존 `silver-model/data/**` 포함). 커밋·push 금지.

## 3. 읽을 것

- 원장(브론즈 3판): `orchestration/work/phub-recommend/bronze/phub-ledger/*.json`. 값은 **재료·기전·대상을 말하는 자리**에서만 모은다:
  - extracted `M*` 의 overview · mechanism · related_techniques
  - taxonomy `modality[]` 의 하위분류 label·description, 항목·제품의 `extracted.overview`·`extracted.mechanism`, `ingredient_basis`, 제품 `ingredient`·`material`·`type`
  - procedure-profiles `mechanism[]`·`moa_summary` · procedure-comparison `mechanism_simple` · products.json `ingredient`·`material`·`type` · literature-evidence `moa`
- 참고(이전 시범 — 재사용 가능, 그대로 믿지 말고 원문 확인): `silver-model/data/pilot-3level/`(M1·M8·M9 의 material 20 · tissue 12 · procedure_type 의 principle 값) · `silver-model/data/modality-notes.md`(§2 하위로 넘긴 기전 문장) · `silver-model/data/material.csv`·`tissue.csv`·`material-tissue-notes.md`(앞선 **실패작** — 원장 단어를 다 쓸어 담아 정규화가 안 됐다. 후보 목록·합친 표기·판단 메모로만 참고)
- 색인(누락 확인): `first-pass/<원장>/source-map.json`.

## 4. 테이블

**`material.csv`** — 몸에 넣거나 가하는 것
`code`(MAT-…) · `name_ko` · `name_en` · `kind`(물질 / 에너지 / 기계적 자극) · `parent_code` · `description`(원장 근거 한 문장, 없으면 비움) · `basis`(포인터, `;` 여럿)

**`mechanism.csv`** — 어떤 원리로 작용하나
`code`(MEC-…) · `name_ko` · `name_en` · `parent_code` · `description` · `basis`
예(원장 문장으로 확인할 것): 아세틸콜린 차단 · 채움(볼륨) · 이물반응으로 콜라겐 생성 자극 · 선택적 광열 · 광음향 · 박피 · 비박피 미세 열손상 · 조직 가열 · 열응고 · 근육 강제 수축 · 냉각으로 지방세포 사멸 · 미세 상처 → 성장인자 → 재생 · 정맥 투여로 성분 공급 …

**`tissue.csv`** — 무엇에 작용하나
`code`(TIS-…) · `name_ko` · `name_en` · `kind`(층 / 구조 / 표적) · `parent_code` · `description` · `basis`
- 층(표피·진피·피하지방층·SMAS·골막상 …) · 구조(근육·피지샘·땀샘·모낭·혈관·지방세포 …) · 표적(빛이 겨누는 멜라닌·문신 색소 등).

## 5. 규칙 (사용자 합의 · 앞선 실패에서)

1. **그 단위로 쓰인 자리에서만 모은다.** 문장 속에 스쳐 나온 단어(화장품 성분 나열 등)를 다 넣지 않는다. 기준: 「이 값이 시술 하나 이상의 재료/기전/대상으로 실제로 쓰이는가」.
2. **한 개념은 한 행, 한 테이블에만.** (콜라겐: 주입 재료면 material, 수축 대상이면 tissue — 둘 중 원장 쓰임에 맞는 쪽 하나. 둘 다 쓰이면 notes 에 근거와 함께 어디에 뒀는지)
3. **상·하위는 parent 로.** 같은 층에 상위와 하위를 나란히 두지 않는다(AHA > 글리콜산 · 레이저 > Nd:YAG > 1064nm · 집속 초음파 ⊂ 초음파).
4. 같은 것의 다른 표기(HA · 히알루론산 · Hyaluronic acid)는 한 행. 합친 표기는 notes 에(별칭 테이블은 만들지 않는다).
5. **이름은 원장 표현을 쓴다.** 원장에 없는 이름을 짓지 않는다(앞에서 「선택적 광열 레이저」 같은 지은 이름이 문제였다). 기전 이름은 원장 기전 문장의 말을 줄여 쓴다.
6. **넣지 않는 것**: 제품·장비 브랜드(쥬비덤·울쎄라 — 제품 사전에서) · 부위(이마·턱선) · 이름 있는 해부 구조(전두근·활차상동맥) · 병변(면포·흉터) · 미생물 · 투여 경로(혈류) · 모공(구멍) · 상품·가격(market-pricing — 나중에) · 먹는 약·바르는 약·홈케어 성분(시술인지 아직 미정 — notes 에 목록만).
7. 레이저 파장(1064nm 등)은 재료의 **하위 행**으로 둔다(시술을 가를지 케이스의 방법으로 둘지는 미정 — 하위 행이면 어느 쪽이든 쓸 수 있다).
8. 원장에 없는 사실 보충 금지. 문맥으로 판단 가능한 것은 판단한다.

## 6. 확인 (완료 전 반드시)

대표 사례 5개가 이 세 사전만으로 표현되는지 notes 에 표로: **보톡스 · HA 필러 · HIFU · 레이저토닝 · 백옥주사** — 각각 재료 코드 · 기전 코드 · (케이스 쪽) 대상 코드 · 근거 원문. 하나라도 안 되면 사전을 고친다.
그리고 계열 17개마다: 그 계열에서 찾은 (재료, 기전) 쌍 목록 — 시술 후보를 세우는 게 아니라 **빠진 재료·기전이 없는지 보는 용도**. 재료나 기전을 원장에서 못 찾은 항목은 원문과 함께 목록으로.

## 7. notes 형식

1. 집계(테이블별 행 수 · kind 별) · 누락 확인 방법(한 단락)
2. 대표 사례 5개 표 · 계열별 (재료, 기전) 쌍 · 못 찾은 항목
3. 합친 표기 · parent 로 묶은 것
4. 넣지 않은 것(규칙 6 분류별 · 먹는 약/바르는 약/홈케어 목록)
5. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지(판단 가능한 건 올리지 않는다)

## 8. 완료 기준

- 세 CSV 모든 행에 basis 포인터 · 브랜드·부위·이름 있는 구조·병변·미생물·경로·가격이 없다 · 상·하위가 parent 로 이어졌다 · 한 개념이 두 테이블에 없다.
- 대표 사례 5개가 표현된다. 계열 17개 확인 표가 있다.
- 산출물 외 변경 없음(`git status`).

## 9. 질문 · 완료 보고

막히면 원문을 먼저 확인하고, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(시술·케이스 목록 · 부위 · 제품 · 관계로 넘어가지 않는다).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/data/atoms/atoms-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "atoms 완료: orchestration/work/phub-ledger-redesign/silver-model/data/atoms/" --enter`
