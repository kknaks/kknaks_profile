# 제품 사전 수정 — 올리지오 제조사 (사용자 확인 2026-11-11)

대상: `silver-model/drafts/product/product.csv` · `organization.csv` · `product-notes.md`

1. **올리지오 · 올리지오X 의 manufacturer_code = 원텍.** organization.csv 에 원텍 행이 없으면 만든다(basis = `taxonomy.json:/modality/8/subcategories/1/items/1/detail` 「원텍 · 모노폴라」).
   - 두 제품 행의 basis 에 위 원텍 근거 포인터를 넣는다. 「클래시스」 근거 포인터는 basis 에서 빼고 notes 의 오류 목록으로 옮긴다.
   - 올리지오와 올리지오X 는 행을 따로 둔다(같은 제조사의 다른 제품). parent 관계가 원장에 있으면 유지.
2. 클래시스 조직 행은 다른 제품(볼뉴머 등)이 쓰면 그대로 둔다.
3. `product-notes.md` 에 절 추가 — **원장 오류(올리지오 제조사)**:
   | 위치 | 원장 값 | 바른 값 |
   |---|---|---|
   | `products.json:/energy_device/products/3/manufacturer` | 클래시스 | 원텍 |
   | `taxonomy.json:/modality/8/products/4/manufacturer` (위의 복사본) | 클래시스 | 원텍 |
   | `taxonomy.json:/modality/8/subcategories/1/items/8/detail` 「클래시스 GX모드 입체가열」 | 클래시스 | 원텍 (GX모드 설명은 맞음) |
   - 근거: 원장 안 `taxonomy.json:/modality/8/subcategories/1/items/1/detail` 「원텍 · 모노폴라」 + 외부 확인(사용자 조사 2026-11-11: 패션비즈 「원텍, 비비와 손잡은 CM송 '오오오 올리지오'」 · 메디포뉴스 「원텍, 올리지오X 대만 인증」 · 메디게이트뉴스 「원텍, 올리지오X 브라질 ANVISA 인증」 · 한국경제 「원텍 올리지오 XM」). 원장 「다수 값」 셋 중 둘은 같은 값의 복사본이었다.
   - 원장(브론즈) 자체는 고치지 않았다(수정 여부는 사용자 결정).
4. 6번 판단 표의 2번 행을 「해결: 원텍」으로 갱신.
5. UTF-8 BOM 유지. 다른 행·파일은 건드리지 않는다.

완료: `git status` 확인 후 코디 터미널에 한 줄
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "product 올리지오 수정 완료" --enter`
(worker_done 은 다시 보내지 않는다.)
