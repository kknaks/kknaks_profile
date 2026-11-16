# [researcher] 조사 3 — HAR 로 Q-K1 · Q-K2 닫기(상품 수정 뒤 이미 산 값이 바뀌나 · optionId 유지되나)

너는 cc-prototype `researcher` 워커다. 원 브리프의 제약은 **그대로** 유효하다. 데모 키만 쓰고 운영 지점 키는 쓰지 않는다 · 공개 API 는 조회만 한다(쓰기 0) · public 이라 이름 · id 값 · 토큰 · 키 · 연락처는 적지 않고 모양 · 건수만 적는다 · 리포트 1개만 쓴다.

- 원 브리프: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/api-swagger-docs-research-brief.md`
- 조사 2: `.../api-swagger-docs/research-purchase-snapshot.md` — §0 Q-K1 · Q-K2 · §1.4 「관찰하지 못한 것」이 이번 질문이다
- **HAR(사용자가 데모 테넌트 KOS 웹에서 캡처 · gitignore · 레포에 복사하지 마라)**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/reference/2026-11-11-cc-product/har/상품 수납.har` (9.4MB · 2026-11-11 06:27~06:30 UTC)
  - 흐름(코디가 URL 만 훑음): 06:27 수납 — `initialize-purchase` → `add-pending-purchase-items` → `register-purchase` → `change-pending-purchase-items-option-unit` ×2 → `add-transaction` → `accept-purchase` → `add-flow-tasks` / 06:29 상품 수정 — `get-product` → `update-product-information` → `update-product-option`(v2) → `get-product` / 06:30 `search-product-option-summaries`. `get-purchase-summaries` 27회 · `ticket/v1/queries/get-ticket-bundles` 3회(내부 API)
  - HAR 안의 Authorization · 쿠키 · 토큰은 **읽지도 옮기지도 마라**. 요청 본문 · 응답 본문만 본다

## 알아낼 것

1. **Q-K2 optionId** — `update-product-option` 요청 · 응답과 그 전후 `get-product` 를 비교해 수정한 옵션의 id 가 **유지되는지 · 새로 생기는지**. 무엇을 바꿨는지(이름 · 가격 · 횟수 · 단위 · 구성 중 어느 칸 — 값 원문 없이 칸 이름과 「바뀜」만)
2. **Q-K1 이미 산 값** — 06:27 에 수납된 구매(그 visitorId · purchaseId 는 HAR 에서 찾는다)의 `items[].optionConfiguration` · 가격과 시술권 묶음을 **수정 전**(HAR 안 06:29:15 이전 응답)과 **수정 후**(HAR 안 06:29:44 이후 응답이 있으면 그것, 없으면 **지금 공개 API** `getPurchaseSummaries` · `getPurchaseSummariesByVisitor` · `getTicketBundlesQuery` 로 데모 키 조회)로 칸별 비교. 수정한 칸이 구매 · 시술권 쪽에서 **옛 값 그대로인지 · 새 값으로 바뀌었는지**
3. 수정 후 메뉴(`getProducts` 공개 API 지금 조회)에서 그 옵션이 새 값인지도 확인 — 「메뉴는 바뀌고 구매는 그대로」가 한 장면에 나오는지
4. 덤 — `change-pending-purchase-items-option-unit` 이 조사 2 §1.3 ② 의 「구매 때 단위 바꾸기」 출처인지(그 요청 본문 모양)
5. 판정 — Q-K1 · Q-K2 를 각각 **확인됨(어느 쪽)** / **여전히 구분 불가(이유)** 로

## 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/research-har-product-edit.md`
- 맨 위: Q-K1 · Q-K2 판정 한 줄씩 + 수정 전/후 비교 표(칸 · 메뉴 전 · 메뉴 후 · 구매 전 · 구매 후 — 값은 「A」「B」 같은 기호로)
- 조사 2 「정할 것」 중 이번 결과로 닫히는 것

완료 보고는 원 브리프 §9 와 같은 두 채널로 한다(이번 dispatch 의 taskId · dispatchId 를 쓴다).
