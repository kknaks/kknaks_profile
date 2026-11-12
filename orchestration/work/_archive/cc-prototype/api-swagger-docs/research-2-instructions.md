# [researcher] 조사 2 — 고객이 산 것(수납 · 시술권)은 산 시점 스냅샷인가 · 고객 ↔ 상품 연결

너는 cc-prototype `researcher` 워커다. 원 브리프의 제약이 **그대로** 유효하다. 데모 키만 쓰고 운영 지점 키는 쓰지 않는다 · 조회만 한다(쓰기 0) · public 이라 이름 · id 값 · 키는 적지 않고 모양 · 건수만 적는다 · 리포트 1개만 쓴다.

- 원 브리프: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/api-swagger-docs-research-brief.md`
- 네 조사 1: `.../api-swagger-docs/research-procedure-menu.md` (§5 「스냅샷인지 문서에 없음」이 이번 질문의 출발점)
- 앞 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/reference/2026-10-12-cc-prototype/kos-demo-api.md` §2 B · §3.4 · §4(수납 → 시술권 → 작업)

## 배경

사용자의 우려: 「10월 상품 → 고객 구매 → 상품 정보 수정 → 고객 방문」 순서라면, 고객이 이미 산 것도 같이 바뀌어 버리지 않나? 이미 산 고객은 **산 시점의 상품**(가격 · 구성 · 횟수)을 써야 한다. 우리가 「메뉴 = 지금 기준」 · 「고객 보유 = 산 시점 그대로」로 나눠도 되는지, 그 근거를 KOS 실물로 확인한다.

## 알아낼 것

1. **스냅샷인가 · 참조인가** — 수납 `getPurchaseSummaries` · `getPurchaseSummariesByVisitor` 의 `items[].optionConfiguration`, 시술권 `getTicketBundlesQuery` 의 `optionConfiguration` · `price` · `ticketSets[]`, 일정 작업 `productOptionConfiguration` 을 데모 고객 여러 명으로 불러 **지금 메뉴(getProducts)와 칸별로 대조**한다(옵션 이름 · 상품 이름 · 가격 · 구성 시술 · 횟수 · 단위). 
   - 메뉴와 **다른** 값이 하나라도 있으면 → 스냅샷의 증거. 건수와 어떤 칸이 다른지(값 원문은 적지 않는다)를 적는다
   - 메뉴에 **없는** optionId(삭제 · 닫힌 옵션)를 가진 구매가 있는지
   - 전부 같으면 「구분 불가(데모 메뉴가 바뀐 적 없을 수 있음)」로 적는다. 추정으로 결론 내지 않는다
   - 구매 · 시술권 쪽 시각(`createdDateTimeUtc` 등)과 메뉴 쪽 수정 시각 칸이 있으면 비교한다
2. **문서 근거** — openapi.yaml 스키마 설명 · 공식 가이드(구매 · 시술권 · 상품)에 「스냅샷」 「구매 시점」 「변경되어도」 같은 서술이 있는지. 있으면 URL과 문장을 인용한다
3. **고객 ↔ 상품 연결 경로** — 고객(visitorId) → 수납 → `items[]` → 시술권 묶음(`purchaseId` · `purchaseItemId`) → `tickets[]`(status · 남은 장수) → 일정 작업(`ticketId`)까지, 어떤 키로 이어지는지 끝까지 그린다. 수납 `items[].optionConfiguration.id` 가 메뉴 옵션 id 와 같은 체계인지(조사 1 §5 에서 미확인이었다). 시술권 `status` 값별 건수. 다 쓴 · 취소된 시술권은 어디서 볼 수 있는지(`getTicketBundlesQuery` 는 AVAILABLE 만 준다)
4. **고객 한 명 단위 비용** — 고객 1명의 보유 시술권을 보려면 호출이 몇 번 · 얼마나 걸리는지

## 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/research-purchase-snapshot.md`
- 맨 위: 질문 1~4 한 줄 답과 **판정**(스냅샷 확인 / 참조 확인 / 구분 불가). 구분 불가면 KOS 에 물을 질문 문장을 한두 개 적는다
- 연결 그림 한 장(고객 → 수납 → 시술권 → 작업 · 메뉴는 점선 참조)
- 정할 것(결정하지 않고 모음)

완료 보고는 원 브리프 §9 와 같은 두 채널로 한다(이번 dispatch 의 taskId · dispatchId 를 쓴다).
