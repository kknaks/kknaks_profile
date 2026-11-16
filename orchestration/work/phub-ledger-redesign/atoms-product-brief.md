# 발주서 — 기본 단위: 제품/장비 사전 (+ 제조사)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 경로는 이 레포 기준.

## 1. 목표 · 구조

Procedure Hub 는 **시술 원장**이다. 고민 · 시술 이름 · **제품** 어느 쪽에서 들어와도 같은 시술에 도착하는 데이터를 만든다. 「울쎄라」는 상품이 아니라 **제품(장비)** 이고 시술(HIFU)에 연결된다.
실버 3층: ① 기본 단위(사전) → ② 조합(시술 = 재료 + 기전 · 케이스 = 시술 + 작용 대상·부위·방법·**제품**) → ③ 관계.
확정 사전(`orchestration/work/phub-ledger-redesign/silver-model/silver/`): 계열 `modality.csv` · 재료 `material.csv`(+`material_spec.csv`) · 기전 `mechanism.csv` · 조직 `tissue.csv` · 방법 `method.csv`.

이번 일: ① 중 **제품/장비** 사전과 **제조사** 사전, 그리고 제품이 무엇으로 만들어졌거나 무엇을 내는지(재료) · 어떤 방식인지(방법)를 잇는 표. 시술·케이스 목록, 부위, 관계, 상품(수량·가격)은 하지 않는다.

## 2. 산출물 (작업 중 폴더에)

`orchestration/work/phub-ledger-redesign/silver-model/drafts/product/` 아래:
`product.csv` · `organization.csv` · `product_material.csv` · `product_method.csv` · `product-notes.md`
CSV 는 **UTF-8 BOM**(`utf-8-sig`) · 쉼표 · 필요한 칸 큰따옴표. 다른 파일은 읽기만(`silver/` 포함). 커밋·push 금지.

## 3. 읽을 것

- 원장(브론즈 3판): `orchestration/work/phub-recommend/bronze/phub-ledger/*.json` — **제품·장비를 가리키는 자리**:
  - products.json 전 섹션(name · name_en · manufacturer · country · mfds · ingredient · material · type · note · legal_warning · regulatory_status)
  - taxonomy `modality[].products[]`(59) · taxonomy 항목 중 제품·장비인 것(보툴렉스 · 쥬비덤 · 울쎄라 · 써마지FLX · 피코슈어 …: 항목 `name`·`detail`·`extracted.overview/mechanism`)
  - problem-packages `procedures[].products[]` · problem-combos `products[]` · procedure-comparison 이름 속 장비 · pih-risk 이름 속 장비 · synergy from/to 의 장비 이름 · market-pricing 이름 속 제품명(**이름만** — 수량·가격은 상품이라 안 다룬다)
- 확정 사전: 위 `silver/` 전부(재료·방법 코드로 잇는다).
- 참고(믿지 말고 원문 확인): `silver-model/archive/pilot-3level/item-judgment.csv`(M1·M8·M9 항목의 「제품」 판정) · `archive/pilot-set/item-judgment.csv`
- 색인(누락 확인): `first-pass/<원장>/source-map.json`

## 4. 테이블

**`product.csv`** — `code`(PRD-…) · `name_ko` · `name_en` · `name_en_source`(원장/보충) · `abbr` · `aliases`(`;`) · `kind` · `parent_code` · `manufacturer_code`(→ organization) · `country` · `mfds`(원장 값 그대로: true/false/빈칸) · `modality_code`(원장이 놓은 계열 — 하나, 여럿이면 `;`) · `description` · `basis`
- `kind`: 약제(톡신 등) · 필러 · 콜라겐 자극 주사제 · 스킨부스터 · 실 · 장비 · 키트 · 기타 — 원장 값으로 꼭 필요하면 추가하고 이유를 notes 에.
- `parent_code`: 제품 계열 > 모델·라인(울쎄라 > 울쎄라피프라임 · 쥬비덤 > 쥬비덤 볼라이트 · 슈링크 > 슈링크유니버스). 원장이 같은 제품의 판·라인으로 적은 것만.

**`organization.csv`** — `code`(ORG-…) · `name_ko` · `name_en` · `name_en_source` · `aliases` · `country` · `basis`
- 「앨러간/애브비」 같은 합성 표기는 원장 뜻대로 나눈다(인수·계열사 관계면 notes 에 근거).

**`product_material.csv`** — `product_code` · `material_code`(→ `silver/material.csv`) · `role`(성분 / 재질 / 내는 에너지) · `basis`
- 예: 보툴렉스 → 보툴리눔 톡신 A형(성분) · 쥬비덤 → 가교 히알루론산(성분) · 민트리프트 → PDO(재질) · 울쎄라 → 고강도 집속 초음파(내는 에너지) · 인모드 → 고주파 + 근적외선(복합이면 여러 행).
- 재료 사전에 없는 재료가 필요하면 **재료 사전을 고치지 말고** notes 에 「재료 추가 후보」로 원문과 함께.

**`product_method.csv`** — `product_code` · `method_code`(→ `silver/method.csv`) · `basis`
- 장비가 원장에서 방식이 명시된 것만(써마지FLX → 모노폴라 · 인모드 → 바이폴라 · 레블라이트SI → 큐스위치 · 피코슈어 → 피코초 펄스 · 제네시스 계열 → 롱펄스 · 니들RF 장비 → 절연/비절연 니들). 없으면 행을 만들지 않는다.

## 5. 규칙 (앞 사전들과 같은 기준)

1. 제품을 가리키는 자리에서만 모은다. **시술 이름(레이저토닝 · 백옥주사)·마케팅 주사명·시그니처 프로그램·패키지는 제품이 아니다.** 상품(제품 + 수량 + 가격: 「리쥬란 힐러 2cc 20만」)도 아니다 — 이름 속 제품명만 쓴다.
2. 한 제품은 한 행. 원장 곳곳의 같은 제품(products.json · taxonomy products · taxonomy 항목 · 다른 원장 언급)은 합치고 basis 를 여럿 둔다. **같은 제품인지 원장으로 판단이 안 되면 합치지 말고 notes 에 후보**(예: 리즈톡신 ↔ 리즈톡스).
3. **이름 3칸 + 괄호 금지**: 「보톡스(엘러간)」→ name_ko 보톡스 + manufacturer 엘러간 · 「클라리티2 (혈관)」→ 용도는 description · 「울쎄라 (턱라인)」→ 상품이라 제품명 「울쎄라」만. 다른 표기는 aliases.
4. 「보톡스」는 시술 이름이기도 하고 제품(앨러간 Botox)이기도 하다 — 제품 행은 제품으로서만(설명에 구분을 적는다).
5. 원장에 없는 제품·사실을 만들지 않는다. 영어 이름은 원장에 없으면 표준 표기로 채우되 `name_en_source`=보충. 문맥으로 판단 가능한 것은 판단한다.
6. 넣지 않는 것: 수량·가격 · 시술·케이스 · 부위 · 재료 자체(재료 사전) · 허가 번호 등 원장에 없는 값.

## 6. 확인 (완료 전)

notes 에 표로 — 아래가 제품 행 + 재료·방법 연결로 표현되는지: **울쎄라 → 집속 초음파**(→ 시술 HIFU) · **써마지FLX → 고주파 · 모노폴라** · **보툴렉스·디스포트·제오민 → 톡신**(제조사 다름) · **쥬비덤 → 가교 HA** · **리쥬란 → PN** · **민트리프트 → PDO 실** · **피코슈어 → 755nm · 피코초 펄스** · **인모드 → 고주파 + 근적외선 · 바이폴라**.
그리고 원장의 제품 언급 전부(위 자리)가 제품 행에 붙었는지(못 붙인 것 목록).

## 7. notes 형식 (짧게)

1. 행 수(kind 별 · 제조사 수 · 연결 행 수) · 누락 확인 방법
2. 확인 사례 표
3. 합친 것 / 합치지 않은 후보(같은 제품 의심)
4. 재료·방법 추가 후보(사전에 없어 못 이은 것)
5. 넣지 않은 것(시술명 · 상품 · 마케팅명 등 예)
6. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지(판단 가능한 건 올리지 않는다)

## 8. 완료 기준

- 모든 행 basis · 이름 괄호 0 · 수량·가격·시술명 없음 · 같은 제품 중복 0(의심은 notes).
- product_material·product_method 의 코드가 전부 `silver/` 사전에 있다.
- 확인 사례가 표현된다. 산출물 외 변경 없음(`git status` — `silver-model/` 은 미추적이라 산출물 경로만 새로 생겼는지).

## 9. 질문 · 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다.
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/product/product-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "product 사전 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/product/" --enter`
