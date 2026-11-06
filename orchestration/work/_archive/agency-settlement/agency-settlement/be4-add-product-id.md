# backend WP-BE4 추가 — 상품 키 = KOS 상품 id (사용자 결정 · OQ-138 뒤집음)

사용자: 「상품 id 로 매핑하는 게 아니야?」 → **id 로 잇는다.** 코디가 운영 수집본으로 확인함:
- ② 품목 행엔 id 가 없지만, 같은 수납의 ⑤ `items[].optionConfiguration{id, title, productTitle}` 와 **옵션 이름(② `productOptionTitle` = ⑤ `optionConfiguration.title`)으로 짝지으면 671/671 하나로 정해짐(겹침 0)** → 옵션 id
- ⑦ `getProducts` 의 `options[].id` → 상품 `id` (상품 · 옵션 둘 다 `deleted` 칸 있음)

규칙:
1. 품목 → 옵션 id: 같은 수납 ⑤ items 에서 옵션 이름으로(이미 ⑤ 를 부른다 · 꺼낼 칸에 `items[].optionConfiguration.{id,title}` 더함 — 개인정보 아님). 같은 이름 둘 이상이면 금액(`price`)으로 · 그래도 못 정하면 이름 키로 대체 + 셈
2. 옵션 id → 상품 id: ⑦ 목록(삭제 포함). 목록에 없는 옵션은 **옵션 id 를 키로**(「KOS 목록에 없음」 줄) · 기타 상품 · 선불카드는 지금처럼 (종류, 이름)
3. 수수료율 표의 키 = 상품 id(없으면 위 대체 키). 같은 이름 다른 id 는 따로 줄
4. 저장(PG)에 품목별 option_id · product_id 칸 · 시험(짝짓기 · 대체 · 이름 바뀜에도 같은 id)
- 이미 만든 이름 키 코드는 대체 경로로 남겨라. SPEC 은 코디가 planner 에게 맞춘다
