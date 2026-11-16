# 제품 사전 마무리 + 확정본으로 쓰기 (코디 판단 · 사용자 승인된 기준 안)

대상: `silver-model/drafts/product/` 전부 → 확정본 `silver-model/silver/`

## 남은 3건 처리 (판단 근거 함께 notes 에)
1. **리젠바이오텍 두 행(ORG-021 · ORG-089)은 한 회사로 합친다.** 같은 이름이고 원장에 다른 회사라는 근거가 없다. 코드 하나(앞 번호 ORG-021)만 남기고 ORG-089 를 쓰던 제품(에스테필)을 ORG-021 로 다시 연결, basis 합침. notes §8 옛→새 코드표에 추가.
2. **product_method 에서 제니스(PRD 제니스 행)의 MET-047 절연 니들 연결을 아그네스(PRD-554)로 옮긴다.** 원장의 name_en·type 이 아그네스로 옮겨졌으므로 같은 근거를 따라간다. basis 그대로.
3. **브이빔(PRD-324, 브이빔퍼펙타의 부모) 제조사 = 캔델라(ORG-031).** 근거: 사용자 조사 2026-11-11 FDA 510(k) K230990 「Candela Vbeam Family」 · 자식 브이빔퍼펙타가 캔델라. notes §7 에 출처 한 줄.

## 확정본으로 쓰기
4. `product.csv` · `organization.csv` · `product_material.csv` · `product_method.csv` · `product-notes.md` 를 `silver-model/silver/` 에 쓴다(UTF-8 BOM). notes 6절 판단 대기 0 · 이번 3건을 한 절로.
5. 검사: product 의 manufacturer_code · organization 의 current_org_code · product_material 의 material_code · product_method 의 method_code 가 전부 존재하는 코드인지(`silver/material.csv` · `silver/method.csv` 포함). 이름 괄호 0 · basis 빈 행 0.
6. 확정본을 쓴 뒤 `silver-model/drafts/product/` 폴더는 그대로 둔다(코디가 archive 로 옮긴다). 원장은 고치지 않는다.

## 완료
`git status` 확인 후 preamble 의 worker_done(--outcome, --report-path orchestration/work/phub-ledger-redesign/silver-model/silver/product-notes.md) 한 번, 그리고 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "product 확정 완료" --enter`
