# 제품 사전 수정 — 시크릿(시크릿RF) 제조사 (사용자 조사 2026-11-11)

대상: `silver-model/drafts/product/product.csv` · `organization.csv` · `product-notes.md` (UTF-8 BOM 유지)

## 사실 (사용자 외부 조사)
- 시크릿RF 원 제조사 = **이루다(Ilooda)** — 미국 FDA 510(k) 신청자 Ilooda Co., Ltd. · 국내 기사(데일리메디).
- **2024-10-01 클래시스가 이루다를 흡수합병**(클래시스 존속, 이루다 소멸) — 바이오스펙테이터 · 메디게이트뉴스. 현재 클래시스 공식 사이트 제품 페이지에 시크릿RF.
- 원장의 「아이닉」은 근거가 없는 오류 값. 원장의 「일루다」는 Ilooda 를 소리대로 옮긴 표기 — 회사 한글 이름은 **이루다**.

## 할 일
1. PRD-552 시크릿: `manufacturer_code` = **클래시스(ORG-025)**(현재 제조사). `description` 에 「원 제조사 이루다(ORG-085) — 2024-10-01 클래시스에 흡수합병」을 덧붙인다. basis 에서 제조사 근거로 쓰인 `products.json:/energy_device/products/9/manufacturer`(아이닉)는 빼고, `taxonomy.json:/modality/10/products/2/manufacturer`(일루다)는 원 제조사 근거로 남긴다.
2. ORG-085: `name_ko` = **이루다**, `aliases` = 일루다, `name_en` = Ilooda(name_en_source 원장), description(또는 비고 칸이 없으면 notes)에 「2024-10-01 클래시스(ORG-025)에 흡수합병」.
3. ORG-084 아이닉: 이 행을 쓰는 제품이 시크릿뿐이면 **행을 지우고** notes 의 원장 오류 표로 옮긴다. 다른 제품이 쓰면 남기고 보고.
4. PRD-430 시크릿맥스(M9, 원장 「클래시스 · 침습+비침습 RF」)는 바꾸지 않는다. 시크릿(PRD-552)과 같은 제품으로 합치지 않는다.
5. `product-notes.md` 7절(원장 오류)에 시크릿 행 추가: `products.json:/energy_device/products/9/manufacturer` 「아이닉」 → 오류(근거 없음) · `taxonomy.json:/modality/10/products/2/manufacturer` 「일루다(Ilooda)」 → 원 제조사 맞음(한글 표기 이루다), 현재 클래시스. 출처: 사용자 조사 2026-11-11(FDA 510(k) Ilooda · 데일리메디 · 바이오스펙테이터 · 메디게이트뉴스 · 클래시스 공식 사이트). 6절 표 3번을 「해결: 클래시스(원 제조사 이루다)」로 갱신.
6. 다른 행·파일은 건드리지 않는다. 원장(브론즈)은 고치지 않는다.

## 완료
`git status` 확인 후 preamble 의 worker_done(--outcome, --report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/product/product-notes.md) 한 번, 그리고 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "product 시크릿 수정 완료" --enter`
