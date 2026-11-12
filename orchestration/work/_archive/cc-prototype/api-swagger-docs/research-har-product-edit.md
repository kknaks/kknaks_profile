# KOS 상품 수정 뒤 이미 산 값이 바뀌나 · optionId 는 유지되나 — HAR 실측

- 조사일 **2026-11-11** · cc-prototype `researcher` 워커 · 조사 3(조사 2 = `research-purchase-snapshot.md` §0 Q-K1 · Q-K2 · §1.4)
- 원천 ①: 사용자가 데모 테넌트 KOS 웹에서 캡처한 HAR(2026-11-11 06:27~06:30 UTC, 레포 밖 gitignore 경로). **요청 · 응답 본문만** 읽었다. Authorization · 쿠키 · 토큰 헤더는 읽지 않았다. HAR 은 KOS **내부 API**(`api.kos-solution.com/tenants/…`)를 부른 기록이다
- 원천 ②: 공개 API 를 데모 키로 지금(수정 뒤) 조회했다. 조회 **6회**, 쓰기 **0회**, 운영 키 **0회**
- public 레포다. id · 이름 · 금액 원문은 적지 않았다. 금액은 기호로만 적는다: **A** = 수정 전 메뉴 정가, **B** = 수정 후 메뉴 정가(B/A ≈ 1.33)
- 표기: **확인** = 본 것, **추정** = 해석

---

## 0. 판정

| 질문 | 판정 |
|---|---|
| **Q-K1** 상품을 수정하면 이미 산 값도 바뀌나 | **확인됨: 안 바뀐다(산 시점 값 유지).** 메뉴 옵션의 **가격**을 A → B 로 바꾼 뒤에도, 2분 전에 수납된 구매 항목과 그 시술권은 **A 기준 값 그대로**였다(HAR 수정 전후 응답 모두 + 지금 공개 API). 같은 고객이 10월에 산 같은 옵션도 A 기준 그대로다. 단 확인한 칸은 **가격**(과 상품 설명)뿐이다. 이름 · 횟수 · 구성을 고친 사례는 이번 HAR 에 없다 |
| **Q-K2** 수정하면 optionId 가 유지되나 | **확인됨: 유지된다.** `update-product-option`(v2) 요청의 `id` = 수정 전 옵션 id = 수정 후 옵션 id. 상품 id 도 같고, 옵션 수도 1 → 1 이다. 지금 공개 API `getProducts` · `getProductOptions` 도 같은 id 로 B 를 준다. (조사 2 §1.3 ① 「같은 이름 · 다른 id」는 「수정」이 아니라 **삭제 후 다시 만들기**였을 가능성이 커졌다 — 추정) |

### 수정 전/후 비교 표

| 칸 | 메뉴 전(06:29:07) | 메뉴 후(06:29:44 · 지금 공개 API) | 구매 전(06:29:01) | 구매 후(06:30:17~29 · 지금 공개 API) | 시술권 전(06:28:48) | 시술권 후(06:30:09) |
|---|---|---|---|---|---|---|
| 옵션 id | X | **X**(같음) | X | X | X | X |
| 옵션 이름 | T | T(안 바꿈) | T | T | T | T |
| 옵션 정가 `price.amount` | **A** | **B** | — | — | — | — |
| 구매 `optionConfiguration.price` | — | — | A×1.1 | **A×1.1** | — | — |
| 구매 `priceV2.amount` · `basePrice.amount` | — | — | A×1.1 | **A×1.1** | — | — |
| 구매 `priceV2.suppliedAmount` | — | — | A | **A** | — | — |
| 시술권 묶음 `price` · `tickets[].price` | — | — | — | — | A×1.1 | **A×1.1** |
| 횟수 `count` · 진료항목 · 단위 | C · M · U | C · M · U(안 바꿈) | C · M · U | C · M · U | — | — |
| 상품 설명 `description` | D1 | **D2** | (구매에 칸 없음) | — | — | — |
| 상품 이름 | P | P(안 바꿈) | P | P | P | P |

- 구매 응답(내부 API `get-purchase-summaries`)은 06:28:00 부터 06:30:29 까지 **바이트까지 같았다**(수정 전 마지막 06:29:01 ↔ 수정 후 06:30:17 · 06:30:29 비교, 차이 0). 시술권 묶음(내부 `get-ticket-bundles`)도 06:28:48 ↔ 06:30:09 차이 0 이다
- 공개 API 를 지금 불렀을 때, 그 구매 항목의 `optionConfiguration` 은 HAR 06:30 응답과 **같았다**(확인)
- 「메뉴는 B, 구매는 A」가 **한 장면에** 나온다: 지금 공개 API 로 `getProducts(optionIds=[X])` 는 B 를 주고, `getPurchaseSummaries([그 수납])` 는 A×1.1 을 준다

---

## 1. 무엇을 수정했나(Q-K2)

HAR 06:29 의 상품 수정 흐름: `get-product`(06:29:07) → `update-product-information`(06:29:15) → `update-product-option` **v2**(06:29:44) → `get-product`(06:29:44).

| 명령 | 요청 본문 모양(값 없이) | 바뀐 칸(요청값을 수정 전 응답과 비교) |
|---|---|---|
| `procedure-menu/products/v1/commands/update-product-information` | `{id, categoryIds[], title, description, targetCountryCodes[], closed, isEvent, translsMap{title, description, caution, coverImageUrl, contentImageUrl}}` | **`description` 만 바뀜**. `title` · `closed` · `isEvent` · `categoryIds` 는 같음 |
| `procedure-menu/products/v2/commands/update-product-option` | `{id, productId, title, description, type, singleOptionConfiguration{medicalServiceId, price{amount, suppliedAmount, taxFreeAmount, vatAmount, taxation}, count, displayChannels[], frequentlyUsedOption}, translsMap{title, description}}` | **`price` 만 바뀜**(A → B). `title` · `description` · `count` · `medicalServiceId` · `displayChannels` 는 같음 |

`get-product` 수정 전 ↔ 수정 후 응답의 차이(전체 키를 펼쳐 비교):
- `options[0].price.amount` · `suppliedAmount` · `vatAmount` 값이 바뀜(A 기준 → B 기준)
- `description` 이 바뀜, 유의사항 목록 칸(`cautions`)이 0 → 1개
- **그 밖의 칸은 같음**: 상품 `id`, 옵션 `id`, 옵션 수, 이름, 횟수, 진료항목 등

→ **옵션 수정은 같은 id 를 고쳐 쓰는 방식이다**(확인 · 가격 수정 1건). 이름 · 구성(GROUP compositions) · 횟수를 바꿀 때도 id 가 유지되는지는 이번에 보지 못했다. 다만 같은 명령(`update-product-option`)이 `title` · `count` · `medicalServiceId` 를 함께 받는다(위 요청 모양)는 점에서, 같은 방식일 것으로 **추정**한다.

---

## 2. 이미 산 값(Q-K1)

### 2.1 그 구매

- 06:27 에 수납된 구매 1건(같은 HAR 안 `initialize-purchase` → … → `accept-purchase`). 상태는 `ACCEPTED` / `NOT_IN_PROCESS` 이고, 품목은 2개(SINGLE 1 · GROUP 1)다. **SINGLE 품목이 06:29 에 수정한 그 옵션(X)이다**(확인: `add-pending-purchase-items` 요청과 구매 응답의 `optionConfiguration.id` 둘 다 X)
- 시술권: 이 수납에서 묶음 2개가 생겼다(SINGLE 1 · GROUP 1). 같은 고객이 10월에 산 같은 옵션 X 의 묶음도 1개 더 있다

### 2.2 비교 결과(확인)

| 대상 | 수정 전 | 수정 후 | 결과 |
|---|---|---|---|
| 이번 구매 품목(X) 가격 칸 4개(`optionConfiguration.price` · `priceV2` · `basePrice` · 공급가) | A 기준 | A 기준 | **그대로** |
| 이번 구매 응답 전체 | — | — | 수정 전후 **바이트 동일** |
| 이번 수납의 시술권 묶음(X) `price` · 시술권 가격 | A×1.1 | A×1.1 | **그대로** |
| 같은 고객의 10월 구매(X) · 그 시술권 | A×1.1 | A×1.1 | **그대로** |
| 지금 공개 API `getPurchaseSummaries` · `getPurchaseSummariesByVisitor`(X 품목 2건) | — | A×1.1 | **그대로** |
| 지금 공개 API `getProducts` · `getProductOptions`(X) | — | **B** | 메뉴만 바뀜 |
| 지금 공개 API 일정 작업 `productOptionConfiguration`(X, 4건) | — | 옵션 이름 = 메뉴 | 가격 칸이 없어 비교할 수 없음 |

→ **메뉴 = 지금 값, 구매 · 시술권 = 산 시점 값**(가격 기준 확인).

### 2.3 남는 한계

- 바꾼 칸은 **가격 · 상품 설명 두 개**뿐이다. 옵션 이름 · 상품 이름 · 횟수 · 단위 · 구성을 고쳤을 때 구매 쪽이 그대로인지는 이번 HAR 로는 확인할 수 없다. 조사 2 §1.3 ① 에서 구매에 박힌 진료항목이 「삭제 후에도 `deleted: false`」였던 것과 합치면, 구매가 옵션 설정을 **통째로 복사해 둔다**고 보는 편이 자연스럽다(추정)
- HAR 은 내부 API 다. 수정 뒤 값은 공개 API 로도 같게 나오는 것을 따로 확인했다(§2.2 마지막 세 줄)

---

## 3. 덤 — 구매 때 단위 바꾸기(조사 2 §1.3 ②)의 출처

**확인**: `purchase/v1/commands/change-pending-purchase-items-option-unit` 가 그 출처다. HAR 에서 이번 수납 중 2번(06:27:43 · 06:27:51) 불렸다.

| 요청 본문 모양(값 없이) |
|---|
| `{purchaseId, purchaseItemIds[], changedBasePrice{amount, suppliedAmount, taxFreeAmount, vatAmount, taxation}, groupOptionUnitChangeConfiguration{optionPrice{value, currency}, compositions[{procedure{id, name}, count, unit{type, value}, price{…}, medicalService{…}}]}}` |

- 대상: 이번 수납의 GROUP 품목(`purchaseItemIds` 에 들어 있다). SINGLE 용 칸(`singleOption…`)은 이번 요청에 나오지 않았다
- 1회차: 구성 1개의 단위 ×1.33 → 그 구성 가격 = 메뉴 × **1.467** · 품목 기준가 = 메뉴 × 1.283
- 2회차: 구성 2개(×1.33 · ×1.67) → 품목 기준가 = 메뉴 × 1.650
- 최종 구매 품목의 구성 단위 · 가격과 `basePrice` 는 **2회차 요청값과 같다**(확인). 조사 2 의 「단위 ×1.33 → 가격 ×1.467」과 같은 계산 규칙이다(단위 비율 × 1.1)
- 즉 수납 **확정 전**(pending)에 품목 단위를 바꾸면, 바꾼 값이 그 구매의 값으로 굳는다. 메뉴는 바뀌지 않는다

---

## 4. 곁가지 관찰

- 내부 API `ticket/v1/queries/get-ticket-bundles`(요청 `{visitorId, sort}`)는 **다 쓴 시술권 묶음도 준다**. 이번 HAR 에서 `USED` · `IN_USE` 시술권만 든 묶음 3개가 나왔다. 공개 API `getTicketBundlesQuery` 는 같은 고객에 대해 지금 `{}` 를 준다(AVAILABLE 이 하나도 없어서). 조사 2 §3.3 의 「다 쓴 묶음은 공개 API 로 못 본다」를 다시 확인했다. 내부 API 는 우리가 쓸 경로가 아니다
- 내부 `get-purchase-summaries` 요청에는 `includeDeleted` 칸이 있다. 공개 API 요청에는 없다

---

## 5. 조사 2 「정할 것」 중 이번 결과로 닫히는 것

| 조사 2 §5 | 이번 결과 | 상태 |
|---|---|---|
| 1. 나눌 기준(메뉴 = 지금 · 고객 보유 = 산 시점) | 가격 수정 뒤에도 구매 · 시술권은 산 시점 값을 유지한다(Q-K1 확인) | **근거가 닫혔다.** 남은 것은 사용자의 채택 결정뿐이다. 이름 · 구성 수정은 미관찰 |
| 7. 우리 쪽 저장(복사 vs 매번 KOS 읽기)의 전제 「KOS 가 산 시점 값을 들고 있나」 | 들고 있다(가격 기준 확인) | **전제는 닫혔다.** 복사할지 말지는 여전히 정할 것 |
| 5. 같은 이름 · 다른 id 를 같은 상품으로 볼지 | 수정은 id 를 유지한다(Q-K2). 그래서 다른 id 는 「다시 만든 옵션」이다(추정) | 판단 근거가 늘었다. 결정은 남음 |
| 4. 삭제된 옵션 처리 | 변화 없음 | 열림 |
| 2 · 3 · 6(원천 · 가격 표시 · 남은 장수) | 변화 없음. 단, 구매가 = 메뉴 × 1.1 규칙과 단위 변경 규칙은 다시 확인했다(§3) | 열림 |

**KOS 문의 Q-K1 · Q-K2 는 가격 수정 범위에서는 닫혔다.** 이름 · 구성 수정까지 확실히 하려면 같은 방식의 HAR 한 번(옵션 이름 · 횟수를 바꾸는 수정)이면 된다.

---

## 출처

- HAR: 사용자 캡처(데모 테넌트 · 2026-11-11 06:27~06:30 UTC · 레포 밖). 사용한 본문: `update-product-information` · `update-product-option`(v2) · `get-product` ×2 · `get-purchase-summaries`(27회 중 수정 전후) · `get-ticket-bundles` ×3 · `add-pending-purchase-items` · `change-pending-purchase-items-option-unit` ×2 · `get-products`
- 공개 API(데모 키, 2026-11-11 지금 조회): [getPurchaseSummaries](https://developers.kos-solution.com/docs/openapi/purchase#getPurchaseSummaries) · [getPurchaseSummariesByVisitor](https://developers.kos-solution.com/docs/openapi/purchase#getPurchaseSummariesByVisitor) · [getTicketBundlesQuery](https://developers.kos-solution.com/docs/openapi/ticket#getTicketBundlesQuery) · [getProducts](https://developers.kos-solution.com/docs/openapi/product#getProducts) · [getProductOptions](https://developers.kos-solution.com/docs/openapi/product#getProductOptions) · [getSchedulesByVisitor](https://developers.kos-solution.com/docs/openapi/schedule#getSchedulesByVisitor)
- 공개 스펙에는 상품 수정 쓰기 작업 `updateProductOption`(v1 경로)이 있다. HAR 의 내부 명령은 v2 경로다. 공개 쪽 동작이 같은지는 쓰기 금지라 확인하지 않았다
