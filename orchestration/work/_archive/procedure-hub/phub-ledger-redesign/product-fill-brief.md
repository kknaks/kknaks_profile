# 발주서 — 제품 사전 보완: 정규화 3건 + 빈 제조사·재료 조사 + 약제 2개 조사

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/` 기준.

## 1. 배경

Procedure Hub 는 **시술 원장**이다(고민·시술 이름·제품 → 시술). 확정 사전은 `silver-model/silver/` 에 있다: modality · material(+material_spec) · mechanism · tissue · method · **product · organization · product_material · product_method**.
제품 사전을 확정했지만 점검에서 고칠 것과 빈 곳이 나왔다. 사용자 지시: 정규화는 고치고, 원장에 없어 빈 제조사·재료는 **조사해서 채운다.** 앞서 사용자가 직접 조사해 고친 사례(올리지오 = 원텍, 시크릿 = 클래시스(원 제조사 이루다), 아그네스 = 아그네스메디컬, 캔델라·사이노슈어 루트로닉 합병 정리)와 같은 방식이다 — **외부 조사 값은 출처와 함께 넣고, 원장 값과 구분한다.** 원장(브론즈) 자체는 고치지 않는다.

## 2. 산출물

`silver-model/drafts/product-v2/` 아래에 **확정본을 복사한 뒤 고친 판**:
`product.csv` · `organization.csv` · `product_material.csv` · `product_method.csv` · `product-research.csv` · `product-v2-notes.md`
CSV 는 UTF-8 BOM. `silver/` 의 확정본은 고치지 않는다(코디가 확인 후 옮긴다). 커밋·push 금지.

## 3. 할 일

**A. 정규화 3건**
1. aliases 에서 **띄어쓰기·하이픈만 다른 표기**를 지운다(정맥주사/정맥 주사 · 리쥬란 힐러/리쥬란힐러 등). 대상: product 의 aliases. (method 사전은 이번 범위가 아니다 — 같은 문제가 method 에 11건 중 8건 있으니 notes 에 목록만.)
2. product `kind` 에 **필링제** · **줄기세포·엑소좀 제제** 두 값을 추가하고, 현재 「기타」 9개를 다시 분류한다(PRX-T33 · 그린필 → 필링제 / 큐어스킨 · 에스에프 · AAPE · 노바스템 · 미라셀 · ASCEplus · EXOSOME SKIN → 줄기세포·엑소좀 제제). 다른 제품 중에도 이 두 종류에 맞는 것이 있으면 같이 옮기고 notes 에 목록.
3. AAPE 를 재료 「줄기세포 배양액」(`silver/material.csv` 코드)에 `product_material`(role 성분)로 잇는다. 원장 근거(description 의 「ADSC 추출 단백질」 출처)를 basis 로.

**B. 빈 제조사 조사 (116 제품)**
- `manufacturer_code` 가 빈 제품 전부를 웹으로 조사한다. 공식 사이트 · 식약처(MFDS) · FDA 510(k) · 신뢰할 만한 기사를 우선한다.
- 찾으면: organization 에 없으면 행을 만들고(인수·합병 연혁이 있으면 `current_org_code`·`description`), 제품 `manufacturer_code` 를 채운다. **제조사 = 현재 회사**, 원 제조사는 조직 행 + 제품 description(기존 기준).
- **product.csv 에 `manufacturer_source` 칼럼 추가**: `원장` / `외부 조사` / 빈칸. 기존에 원장으로 채워진 것은 `원장`.
- 못 찾거나 확신이 없으면 **빈칸으로 둔다**(추측 금지). 유통사와 제조사가 다르면 제조사만 넣고 유통사는 description.
- 원장의 제품 이름 자체가 틀렸거나 다른 제품과 같은 것으로 보이면 고치지 말고 notes 에 근거와 함께.

**C. 빈 재료 조사 (매쿰7 · 바이리즌 · 엘리실 · 로즈실 · 이모드 · 비타인젝터)**
- 성분·재질·내는 에너지를 조사해 `product_material` 로 잇는다. **재료 사전(`silver/material.csv`)에 있는 코드로만** 잇는다. 사전에 없는 재료가 필요하면 잇지 말고 notes 에 「재료 추가 후보」로. `product_material` 에도 `source` 칼럼(원장 / 외부 조사)을 추가.
- 비타인젝터 · 이모드처럼 재료가 아니라 방법(멀티니들 인젝터 · 전자기 등)이 맞으면 `product_method`(`silver/method.csv` 코드)로.

**D. 아큐탄 · 컨트라투벡스 조사 (범위 판단 자료)**
- 각각 무엇인지(제형 · 성분 · 허가 구분 · 처방/일반의약품), 원장에서 어떤 자리에 어떤 맥락으로 나오는지(원장 포인터와 원문), 피부과에서 「시술」로 쓰이는지 「처방·홈케어」인지 조사해 notes 에 정리한다. **제품 사전에서 빼거나 바꾸지 않는다** — 사용자가 판단한다. 같은 성격(먹는 약 · 바르는 약 · 홈케어)의 다른 제품이 제품 사전에 있으면 목록으로.

## 4. `product-research.csv`

조사한 제품마다 한 행: `product_code` · `name_ko` · `field`(manufacturer / material / method / scope) · `found_value` · `confidence`(확인 / 추정 / 못 찾음) · `sources`(URL `;` 여럿) · `note`
- 확인 = 공식 사이트·허가 기관 문서·복수의 신뢰 기사가 일치. 추정 = 단일 기사 등. **추정은 CSV 값에 넣지 않고** research 표에만 둔다.

## 5. notes (짧게)

1. 결과 집계: 제조사 채움(확인) / 추정(미반영) / 못 찾음 · 재료·방법 채움 · 새 조직 수
2. 정규화 3건 처리 내역 · method aliases 같은 문제 목록
3. D 조사 결과(아큐탄 · 컨트라투벡스 + 같은 성격 제품 목록)
4. 원장 오류로 보이는 것(이름·제조사) — 원장 포인터 · 원장 값 · 바른 값 · 출처
5. 재료 추가 후보

## 6. 완료 기준

- 모든 코드 참조가 존재(제조사 · current_org · 재료 · 방법 · 제품). 이름 괄호 0 · basis 빈 행 0.
- `manufacturer_source`·`product_material.source` 가 빠짐없이 채워짐(값이 있는 행). 외부 조사 값마다 product-research 에 출처.
- `silver/` 변경 없음. 산출물 외 변경 없음(`git status`).

## 7. 완료 보고

막히면 원문·출처를 먼저 확인하고, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다.
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/product-v2/product-v2-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "product-v2 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/product-v2/" --enter`
