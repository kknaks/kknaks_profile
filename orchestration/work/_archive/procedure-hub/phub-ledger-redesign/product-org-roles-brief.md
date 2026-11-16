# 발주서 — 제품-회사 역할 표로 바꾸기 (제조원 · 수입사 · 유통사 · 브랜드 · 허가권자)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/` 기준.

## 1. 배경 · 사용자 결정

Procedure Hub 시술 원장의 실버 제품 사전은 제품마다 `manufacturer_code` 칸 하나에 회사를 넣었다. 그런데 **원장 값은 대개 브랜드·판매사(채움 → 휴젤 · 포텐자 → 사이노슈어 루트로닉)**, **식약처 값은 허가상 제조원(채움 → 아크로스 · 포텐자 → 제이시스메디칼)** 이라 34개 제품에서 값이 다르게 나왔다. 사용자: 「제조사 · 유통사 · 수입사 다 다를 것」 → **한 칸을 없애고 제품-회사 역할 표로 바꾼다.**

## 2. 산출물

`phub-ledger-redesign/silver-model/drafts/product-v4/` 아래: `product.csv` · `organization.csv` · `product_organization.csv` · `product_material.csv` · `product_method.csv` · `product-v4-notes.md`
출발점은 `silver-model/drafts/product-v3/`(식약처 반영판). CSV 는 UTF-8 BOM. `silver/`·원장 변경 금지. 커밋·push 금지.

## 3. 읽을 것

- `phub-ledger-redesign/silver-model/drafts/product-v3/` 전부(특히 `mfds-fill-notes.md` §3 겹침 34 · `mfds-fill.csv`)
- `phub-recommend/step1-products.json` — 10-28 식약처 허가 조사(items 395: `4_license.licenses[]`(holder · holder_biz · manufacturer · state · official_name) · `6_companies`(manufacturer · importer · seller · license_holder · other — 각 name · basis · role · period))
- `phub-ledger-redesign/silver-model/notes/product-research.csv`(외부 조사 출처) · `notes/product-notes.md`
- 원장: `phub-recommend/bronze/phub-ledger/*.json`(products.json manufacturer · taxonomy 제품·항목 detail 의 회사 표기)

## 4. 새 표 `product_organization.csv`

칼럼: `product_code` · `org_code` · `role` · `source` · `basis` · `note`
- `role` (정해진 값만): **브랜드**(제품을 내놓고 판매·마케팅하는 회사 — 사람들이 「○○ 제품」이라 부르는 회사) · **제조원**(실제 만드는 회사 · 허가상 제조자) · **수입사**(해외 제품의 국내 수입 · 대개 수입 허가권자) · **유통사**(국내 판매·유통 — 수입사와 다를 때) · **허가권자**(국내 품목허가 보유자 — 제조원·수입사와 다를 때만)
- 한 제품에 같은 회사가 여러 역할이면 역할마다 한 행(예: 국내 자체 생산 → 브랜드 + 제조원 둘 다 같은 회사).
- `source`: 원장 / 외부 조사 / 식약처.

## 5. 옮기는 규칙

1. **원장 값**(products.json manufacturer · taxonomy detail 의 회사 표기) → 기본 **브랜드**. 단 원장 문구가 「유통」「수입」을 말하면 그 역할(에스테필 「휴메딕스 유통」 → 유통사).
2. **외부 조사 값**(product-research · 사용자 조사: 올리지오 원텍 · 시크릿 클래시스 · 아그네스 아그네스메디컬 · 아발란체 포토나 · 에스테필 리젠바이오텍 등) → notes·출처의 뜻대로 역할을 정한다(대개 브랜드 + 제조원). 원 제조사(이루다 · 팔로마 · 엘먼)는 제품에 행을 두지 않고 조직의 `current_org_code`·`description` 연혁으로 둔다(지금처럼).
3. **식약처 값(step1)** → 313 제품 **전부**에 대해 step1 item 과 매칭(이름 · search_names, 띄어쓰기·괄호 무시, 애매하면 매칭하지 않음). `4_license.status` = 정상(또는 허가 취소 이력 — note 에 상태)인 것만:
   - `6_companies.manufacturer` · `licenses[].manufacturer` → **제조원**
   - `6_companies.importer` · 수입 허가의 holder(holder_biz 에 「수입」) → **수입사**
   - `6_companies.seller` → **유통사**
   - 국내 제조 허가의 holder 가 제조원과 같으면 행 추가 없음, 다르면 **허가권자**
   - basis = `step1-products.json:<ledger_id>/…` 포인터. 「근거 없음」「웹 보도」 수준은 넣지 않는다.
   - step1 이 다른 제품을 섞은 경우(PLLA-SCA ↔ 스컬트라 · 에이비오톡신 ↔ 디스포트 · 채움 ↔ 더채움 같은 search_names 혼동)는 **넣지 않고** notes 에 목록 — 제품이 같은지 원장·이름으로 확인될 때만.
4. product description 에 적어 둔 「국내 수입 ○○」「유통 ○○」 문구는 행으로 옮긴 뒤 description 에서 지운다(연혁 설명은 남김).
5. organization 에 없는 회사는 행 추가(name_ko 는 법인 표기 「(주)」「주식회사」「유한회사」 뺀 이름, 원문은 aliases). 같은 회사의 표기 차이(엘지화학 ↔ LG화학 · 엘지화학익산공장)는 한 조직(공장·지점은 aliases 또는 note).

## 6. product.csv 정리

- `manufacturer_code` · `manufacturer_source` 칼럼을 **지운다**(회사는 이제 product_organization 이 갖는다).
- 다른 칼럼(name · kind · parent · country · mfds · modality · name_check · description · basis)은 그대로. `name_check` 는 v3 값 유지.

## 7. 확인

notes 에 표로 — 아래가 역할 표로 표현되는지: **채움**(휴젤 브랜드 · 아크로스 제조원) · **포텐자**(사이노슈어 루트로닉 브랜드 · 제이시스메디칼 제조원) · **아테콜**(EMCM 제조원 · 티알엠코리아 수입사) · **에스테필**(리젠바이오텍 제조원 · 휴메딕스 유통사) · **보톡스**(앨러간/애브비 브랜드 · 한국애브비 수입사 · 해외 제조원) · **올리지오**(원텍 브랜드·제조원) · **시크릿**(클래시스, 원 제조사 이루다는 조직 연혁).

## 8. notes (짧게)

1. 집계: product_organization 행 수(역할별 · 출처별) · 회사가 하나도 없는 제품 수 · 새 조직 수
2. 확인 사례 표
3. step1 혼동으로 넣지 않은 것 목록
4. 회사가 하나도 없는 제품 목록(원장 작성자 확인 목록 — v3 notes §4 와 대조)

## 9. 완료 기준

- product 에 manufacturer_code 없음 · product_organization 의 product_code·org_code 전부 존재 · role 값이 정해진 5개뿐 · 모든 행 source·basis.
- 이름 괄호 0 · basis 빈 행 0 · 다른 표(material · method 연결)는 v3 그대로.
- `silver/`·원장 변경 없음 · 산출물 외 변경 없음(`git status`).

## 10. 완료 보고

막히면 원문·출처 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다.
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/product-v4/product-v4-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "product-v4 역할 표 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/product-v4/" --enter`
