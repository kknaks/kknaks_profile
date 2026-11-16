# 발주서 — 제품 제조사 빈칸: 10-28 식약처 조사 결과 반영 + 식약처 재조회

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/` 기준.

## 1. 배경

Procedure Hub 시술 원장의 실버 제품 사전(`phub-ledger-redesign/silver-model/silver/product.csv` 313행)에 **제조사 빈칸 74개**가 있다. 대부분 의료기기(장비 · 실 · 필러 · 스킨부스터).
**10-28 에 식약처 의료기기 DB(emedi)·의약품 DB 로 제품 395개 허가를 조사한 결과**가 `phub-recommend/step1-products.json` 에 있는데, 직전 조사에서 쓰지 않았다. 이걸 반영하고, 그 파일로 안 풀리는 것만 식약처를 다시 조회한다.
(KPIC/약학정보원은 의약품 DB 라 이번 빈칸(의료기기)에는 쓰지 않는다.)

## 2. 산출물

`phub-ledger-redesign/silver-model/drafts/product-v3/` 에 **silver 의 product 4개 파일을 복사해 고친 판**:
`product.csv` · `organization.csv` · `product_material.csv` · `product_method.csv` · `mfds-fill.csv` · `mfds-fill-notes.md`
CSV 는 UTF-8 BOM. `silver/` 와 원장은 고치지 않는다(코디가 확인 후 옮긴다). 커밋·push 금지.

## 3. 읽을 것

- `phub-recommend/step1-products.json`(items 395 · 각 item 의 `2_names`(display_name · ledger_name · search_names) · `4_license`(status · licenses[]: license_no · kind · state · item · official_name · holder · holder_biz · manufacturer · date …, history[]) · `6_companies`(manufacturer · importer · seller · license_holder) · `evidence`). 관련 설명: `phub-recommend/step1-products.md`
- 실버: `silver-model/silver/product.csv`(`manufacturer_code` · `manufacturer_source` · `name_check`) · `organization.csv`(`current_org_code` · `description`)
- 지난 조사 기록: `silver-model/notes/product-research.csv` · `notes/product-notes.md`

## 4. 할 일

**A. 매칭** — 빈 제조사 74개 각각을 step1 item 과 이름(name_ko · aliases · name_en ↔ display_name · ledger_name · search_names, 띄어쓰기·괄호 무시)으로 맞춘다. 같은 이름이 여럿이면 계열·종류로 가르고, 가를 수 없으면 맞추지 않는다.

**B. 반영 기준 (step1 의 식약처 값)**
- `4_license.status` = 정상 이고 licenses 에 회사가 있으면 채운다:
  - **수입품**(holder_biz 에 수입 · 또는 manufacturer 가 해외 회사): 제조사 = 제조원(`licenses[].manufacturer` / `6_companies.manufacturer`), 수입사(holder)는 product description 에 「국내 수입 ○○」.
  - **국내 제조 허가**: 제조사 = 허가권자(holder) — 제조원이 따로 있으면 제조원.
  - organization 에 없는 회사는 행을 만든다(name_ko 는 식약처 표기에서 「(주)」「주식회사」 같은 법인 표기를 뺀 이름, 원문 표기는 aliases).
  - `manufacturer_source` = **식약처**(새 값). basis 에 `step1-products.json:<ledger_id>/4_license/licenses/<i>` 형태 포인터.
- status = 허가 취소(이력) · 미허가 · 허가 대상 아님: 이력 속 회사(history 의 holder/manufacturer)가 있으면 채우고 description 에 「허가 취소 이력」 등 상태를 적는다. 회사가 없으면 빈칸.
- status = 확인 불가 · 회사 칸이 「근거 없음」·「웹 보도」 수준: 채우지 않는다.

**C. 식약처 재조회** — step1 에 없거나(약 6) 정상인데 회사 칸이 빈 것(리프세라 · 트릴리프트 · 제니스 등 약 3)만 식약처 의료기기 DB(의료기기안심책방 emedi.mfds.go.kr · 의료기기 전자민원) · 의약품안전나라(nedrug)에서 제품명·영문명으로 조회한다. **요청 간격을 충분히 두어** 503 에 막히지 않게 한다. 확인되면 B 기준으로 채우고 source = 식약처, 조회 URL·검색어를 mfds-fill 에 남긴다.

**D. 끝까지 안 되는 것** — `name_check` 를 갱신: step1 이 식약처를 조회해 「확인 불가」였거나 C 에서 다시 안 나온 것은 **`웹·식약처 미확인`**, 식약처를 조회하지 않은 것만 `웹 미확인`. 채운 것은 `확인`.

**E. 겹침 점검** — 이미 채워진 제조사(원장 · 외부 조사)와 step1 의 식약처 값이 다르면 **고치지 말고** mfds-fill-notes 에 목록(제품 · 지금 값 · 식약처 값 · 포인터). 사용자가 판단한다.

## 5. `mfds-fill.csv`

빈칸 74개마다 한 행: `product_code` · `name_ko` · `step1_ledger_id` · `step1_status` · `result`(채움 / 이력만 / 못 채움) · `manufacturer` · `importer` · `source_pointer`(step1 포인터 또는 식약처 URL) · `note`

## 6. notes (짧게)

1. 집계: 74 → 채움 / 이력만 / 못 채움, 새 조직 수, manufacturer_source 분포
2. C 재조회 내역(검색어 · URL · 결과)
3. E 겹침 목록
4. 못 채운 것 목록(원장 작성자 확인이 필요한 목록 — 이름 · 원장 자리 · 원장 원문)

## 7. 완료 기준

- 74개 전부 mfds-fill 에 결과가 있다. 채운 값은 모두 식약처 근거(step1 포인터 또는 조회 URL).
- 코드 참조 전부 존재 · 이름 괄호 0 · basis 빈 행 0. `silver/` 변경 없음 · 산출물 외 변경 없음(`git status`).

## 8. 완료 보고

막히면 원문·출처를 먼저 확인하고, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(제조사 칸 외 다른 칸은 고치지 않는다 — 단 description 의 수입사·허가 상태 문구는 예외).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/product-v3/mfds-fill-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "product-v3 식약처 반영 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/product-v3/" --enter`
