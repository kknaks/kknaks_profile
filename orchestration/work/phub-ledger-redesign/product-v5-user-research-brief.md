# 발주서 — 제품 사전 v5: 사용자 조사(회사 · 영어 이름) 반영 + 정리 결정

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

Procedure Hub 시술 원장의 실버 제품 사전. v4(`drafts/product-v4/`)에서 제품의 회사를 **제품-회사 역할 표**(`product_organization`: 브랜드 · 제조원 · 수입사 · 유통사 · 허가권자, source 원장/외부 조사/식약처)로 바꿨다. 남은 빈칸(회사 없는 제품 60 · 영어 이름 빈 232)을 **사용자가 직접 웹 조사**해 채운 표가 왔다. 이걸 반영하고, 조사에서 드러난 정리 결정(사용자 승인)을 적용한다.

## 2. 산출물

`drafts/product-v5/`: `product.csv` · `organization.csv` · `product_organization.csv` · `product_material.csv` · `product_method.csv` · `procedure-name-candidates.csv` · `ledger-check-list.csv` · `product-v5-notes.md`
출발점 = `drafts/product-v4/` 복사. CSV 는 UTF-8 BOM. `silver/`·원장·`drafts/research-todo/` 변경 금지. 커밋·push 금지.

## 3. 읽을 것

- `drafts/product-v4/` 전부(특히 `product-v4-notes.md`)
- **사용자 조사**: `drafts/research-todo/1-company-filled.csv`(60행: 브랜드(회사) · 제조원 · 수입사 · 유통사 · 출처 URL · 메모) · `drafts/research-todo/2-name-en-filled.csv`(232행: 식약처 영문명 후보 · 영어 이름 · 출처 URL · 메모)
- 참고: `../../phub-recommend/step1-products.json`(10-28 식약처 조사) · `notes/product-research.csv` · `notes/product-notes.md`

## 4. 반영 규칙

**A. 회사 (1-company-filled)** — 칸에 값이 있는 행만:
- 각 회사 칸 → `product_organization` 행(role = 그 칸: 브랜드 / 제조원 / 수입사 / 유통사), `source` = **외부 조사**, `basis` = 출처 URL(여럿이면 `;`), `note` = 메모 요지.
- 칸 값에 「— 쥬베룩」처럼 브랜드명이 붙어 있으면 회사명만 쓴다. 조직이 없으면 organization 에 추가(name_ko 는 법인 표기 뺀 이름, 영문·옛 이름은 aliases — 바임 ↔ VAIM · 바임글로벌). 이미 있는 조직이면 그 코드.
- 메모가 「공식 사이트 미확인」「확정 못 함」 같은 출처 약함이면 note 에 그대로 남긴다(값은 넣는다 — 사용자 조사).
- **PLLA-SCA(PRD-112)는 반영하지 않는다**(아래 C-1).

**B. 영어 이름 (2-name-en-filled)** — `영어 이름` 칸에 값이 있는 행만:
- product `name_en` 에 넣고 `name_en_source` = **외부 조사**(새 값). 근거 URL 은 product `basis` 에 `name_en: <URL>` 로 덧붙인다(URL 이 없고 식약처 후보에서 왔다고 메모에 있으면 `name_en: 식약처 허가 영문명(step1)`).
- 메모에 회사 정보가 있어도(예: 「한스바이오메드 제조, 휴젤 분배」) **이번엔 회사 행을 만들지 않는다** — 그 제품에 v4 회사 행과 다르거나 없는 회사가 메모에 있으면 notes 에 목록만(제품 · 메모 회사 · v4 회사).
- 영어 이름 칸이 비면 그대로 빈칸(지어 넣지 않는다).
- PLLA-SCA → Sculptra 영어 이름도 반영하지 않는다(C-1).

**C. 정리 결정 (사용자 승인 — 그대로 적용)**
1. **PLLA-SCA(PRD-112)**: 스컬트라와 **합치지 않는다.** 사용자 조사(스컬트라 성분 표기)와 10-28 식약처 조사(식약처 PLLA-SCA 는 진오메디칼의 다른 제품)가 어긋남 → `ledger-check-list` 에 둘 다 근거로.
2. **하모니카(PRD-078) = HArmonyCa(PRD-114) 합친다.** HArmonyCa 행 하나로 남기고 「하모니카」는 aliases. 지워지는 행을 가리키던 product_organization · product_material · product_method · parent_code 는 남는 행으로 옮기고 중복 제거. basis 는 합친다. 어느 코드가 남는지 notes 에.
3. **쥬베룩 파인 · 쥬베룩 울트라**: 제품 행 유지 · `parent_code` = 쥬베룩 제품 행(있으면), description 에 「공개 라인업에 없는 이름 — 병원 메뉴명일 수 있음(사용자 조사)」. 회사는 A 대로.
4. **미스코 · 엑소힐러 · 크라이오셀 → 제품 사전에서 뺀다.** `procedure-name-candidates.csv`(`name_ko` · `from_product_code` · `reason`(사용자 메모) · `basis`(원장 근거 원문 그대로) · `source_url`)로 옮긴다 — 시술 단계에서 쓸 시술 이름 후보. 연결 행(product_organization · material · method)은 지우고 notes 에 지운 행 목록.
5. **캐번실 → 제품 사전에서 뺀다.** 실 모양 값 후보로 `procedure-name-candidates.csv` 에 같은 형식으로 넣되 `reason` 앞에 「실 모양 후보:」. 연결 행 처리는 4 와 같다.
6. **오기 의심(리프세라 · 아큐어 · 이모드 등 메모에 「오기 의심」)** 은 고치지 않는다 → `ledger-check-list` 로.

**D. 원장 작성자 확인 목록 `ledger-check-list.csv`**
칼럼: `product_code` · `name_ko` · `what`(회사 없음 / 오기 의심 / 합칠지 / 이름 미확인) · `ledger_basis`(원장 근거) · `searched`(사용자 메모의 검색한 곳) · `note`
- 반영 뒤에도 회사가 하나도 없는 제품 전부 + C-1 + C-6 + 쥬베룩 파인·울트라(이름 미확인).

## 5. 확인 (notes 에 표)

- 반영 전/후: 회사 없는 제품 수 · 영어 이름 빈 수 · name_en_source 분포 · product_organization source 분포
- 바임(쥬베룩 파인·울트라) · 콜라쥬(레겐보겐 브랜드 + 유벤타헬스케어 유통사) · 노보젯 · HArmonyCa 합친 결과 · 빠진 4개 행

## 6. 완료 기준

- 1-company-filled 의 값 있는 회사 칸 전부(PLLA-SCA 제외)가 product_organization 에 있다. 2-name-en-filled 의 영어 이름 전부(PLLA-SCA 제외)가 product 에 있다.
- 코드 참조 전부 존재(product · org · current_org · parent · material · method) · 이름 괄호 0 · basis 빈 행 0 · role 5종 · source 3종(원장/외부 조사/식약처).
- 빠진 제품 코드를 가리키는 행 0. `silver/`·원장·research-todo 변경 없음 · 산출물 외 변경 없음(`git status`).

## 7. 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(새 웹 조사 하지 않는다).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/product-v5/product-v5-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "product-v5 사용자 조사 반영 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/product-v5/" --enter`
