# KOS 수납 · 시술권은 산 시점 스냅샷인가 · 고객 ↔ 상품 연결

- 조사일 **2026-11-11** · cc-prototype `researcher` 워커 · 조사 2(조사 1 = `research-procedure-menu.md`)
- 스펙: `https://developers.kos-solution.com/openapi.yaml` 1.0.1(조사 1 과 같은 날 받은 사본)
- 공식 문서 묶음 `https://developers.kos-solution.com/docs.zip`(739개 파일)을 받아 전문 검색했다
- 데모 호출: 앞 조사 `reference/2026-10-12-cc-prototype/kos-demo-api.md` §1.2 의 **데모 키만** 썼다. 조회 **39회**, 쓰기(`/commands/`) **0회**, 운영 지점 키 **0회**. 메뉴 쪽(`getProducts` · 옵션 검색 · `getMedicalServices` · `getProcedures` · 일정)은 조사 1 에서 **같은 날** 받은 응답을 그대로 썼다
- 고객: 데모 일정에서 고른 10명과 구매 통계에서 고른 10명, **모두 20명**이다. 수납 53건 · 구매 항목 63건 · 시술권 묶음 17개 · 시술권 41장을 봤고, 구매 항목 통계로는 데모 전체 162건을 봤다
- public 레포다. 키 · 토큰 · id 값 · 사람 이름 · 상품/시술 이름 원문은 적지 않았다. **모양 · 건수 · 비율**만 적는다
- 표기: **확인** = 불러서 본 것, **스펙** = openapi.yaml, **문서** = 공식 문서, **추정** = 해석

---

## 0. 요약

### 판정

> **스냅샷 확인(부분).** 구매 항목과 시술권은 메뉴를 실시간으로 가리키지 않는다. **산 시점의 옵션 · 시술 · 진료항목 · 단위 · 가격을 자기 안에 들고 있다.** 근거는 두 가지다(§1.3).
> 1. 메뉴에서 **삭제된** 옵션 · 시술 · 진료항목을 가진 구매 1건이 있다. 그 구매와 시술권(AVAILABLE)은 지금도 산 시점 값을 그대로 준다. 박혀 있는 진료항목은 `deleted: false` 인데, 지금 메뉴에는 그 진료항목이 없다
> 2. 구매 3건은 단위 수량과 가격이 지금 메뉴와 **다르다**(구매할 때 수량을 바꾼 건으로 보인다)
>
> **관찰하지 못한 것**: 메뉴에서 이름 · 가격 · 구성을 **수정**한 뒤에도 구매 쪽이 옛 값을 유지하는 사례. 데모에는 구매 뒤에 수정된 메뉴 항목이 없다. 그래서 이 경우는 실물로 확인하지 못했다. KOS 에 물을 질문은 아래 Q-K1 · Q-K2 다.

**KOS 에 물을 질문**
- **Q-K1** 「상품 옵션의 이름 · 가격 · 구성(시술 · 횟수 · 단위)을 수정하면, 이미 수납된 구매 항목(`getPurchaseSummaries.items[].optionConfiguration`)과 이미 발행된 시술권(`getTicketBundlesQuery`)의 값도 바뀌나요, 아니면 수납 시점 값이 유지되나요?」
- **Q-K2** 「옵션을 수정하면 같은 `optionId` 가 유지되나요, 아니면 새 옵션 id 가 생기나요? 데모에서 같은 이름의 옵션이 다른 id 로 다시 만들어진 사례가 있었습니다.」

### 질문 1~4 한 줄 답

| # | 질문 | 한 줄 답 |
|---|---|---|
| 1 | 스냅샷인가 · 참조인가 | 구매 · 시술권은 산 시점 값을 **자기 안에 복사해서** 들고 있다(확인 1건 + 3건). 메뉴에 없는 optionId 를 가진 구매 · 시술권이 **1건** 있다. 이름 · 시술 · 횟수가 메뉴와 다른 경우는 그 1건 말고는 없다. 가격은 63/63 이 다르지만, 이것은 「구매 가격 = 메뉴 정가 × 1.1(부가세 포함)」이라는 **일정한 환산**이다 |
| 2 | 문서 근거 | 수납 · 시술권 · 상품 문서에 「스냅샷 · 구매 시점 · 변경되어도」 같은 서술은 **없다**. 스펙에서 「스냅샷」이라는 말을 쓰는 곳은 만족도 조사뿐이다. 시술권은 「구매한 상품 옵션을 … 관리하는 권리 단위」, 「수납 완료로 티켓그룹 생성」이라고만 적혀 있다 |
| 3 | 고객 ↔ 상품 연결 | `visitorId` → 수납 → `items[].id` · `optionConfiguration.id` → 시술권 묶음(`purchaseId` · `purchaseItemId`) → `ticketSets[].tickets[].id` → 일정 작업 `ticketConfiguration.ticketId`. 구매 항목의 `optionConfiguration.id` 는 메뉴 옵션 id 와 **같은 체계**다(63/63 이 메뉴에 있음, 1건은 삭제된 옵션). 다 쓴 묶음은 Open API 로 직접 볼 길이 **없다**. 통계 작업은 서버에서 404 가 나고, 일정 작업으로만 거슬러 볼 수 있다 |
| 4 | 고객 1명 비용 | 보유 시술권은 **호출 1번**(`getTicketBundlesQuery`)이면 되고 약 40ms · 0~14KB 다. 구매 내역을 더하면 +1번(약 50ms · 3~30KB), 사용 이력을 더하면 +1번(약 75~110ms · 65~77KB)이다. 이름을 메뉴로 다시 풀 필요는 없다(응답에 이미 들어 있다) |

### 연결 그림

```text
visitorId ──────────────────────────────────────────────────────────────────────┐
   │ getPurchaseSummariesByVisitor(visitorId)                                    │ getTicketBundlesQuery(visitorId)
   ▼                                                                             ▼
수납 Purchase{id, visitorId, status, process, createdDateTimeUtc, …}        시술권 묶음 TicketBundle  ← AVAILABLE 가 1장 이상 남은 묶음만
   └ items[]  PurchaseItem{id, type=PRODUCT_OPTION, priceV2, basePrice, …}     {purchaseId ──► 수납.id            (17/17)
        └ optionConfiguration  ◀═══ 산 시점 복사본 ═══▶                         purchaseItemId ──► items[].id     (17/17)
            {id(=optionId), title, productTitle, optionType,                     optionConfiguration{optionId ──► items[].optionConfiguration.id (17/17),
             SINGLE: procedure{id,name}, count, unit, medicalService{…}            optionTitle, productTitle}
             GROUP : compositions[{procedure, count, unit, price, medicalService}]  price(= 묶음에 담긴 시술권 가격 합, 16/17)
             price}                                                              ticketSets[]{procedure, medicalService, ticketGroupId,
                                                                                     tickets[]{id(uuid), status, price, createdDateTimeUtc}}}
                                                                                              │
                                                                                              │ tickets[].id
                                                                                              ▼
                                                   일정 작업 tasks[].procedureConfiguration.ticketConfiguration{ticketId, round{total, current}}
                                                   (getSchedulesByVisitor · getSchedulesByFlowStep …)  + productOptionConfiguration{optionId, …}

┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
메뉴(지금 기준, 조사 1)   getProducts.options[].id · procedure.id · medicalService.id
   ┆ 구매 · 시술권 · 작업의 optionId · procedure.id · medicalService.id 는 이 id 들과 「같은 체계」다(점선 = 참조만 가능, 실시간 연결 아님)
   ┆ 메뉴에서 삭제되면 메뉴 쪽 조회로는 안 풀린다(getProductOptions 빈 응답). 구매 · 시술권 쪽은 산 시점 값을 계속 준다
```

---

## 1. 스냅샷인가 · 참조인가

### 1.1 무엇을 무엇과 비교했나

| 구매 쪽(산 것) | 칸 | 메뉴 쪽(지금) |
|---|---|---|
| `getPurchaseSummaries` · `getPurchaseSummariesByVisitor` → `items[]`(PRODUCT_OPTION) 63건 | `optionConfiguration.id · title · productTitle · optionType · price` · SINGLE `count · procedure.id · unit · medicineAndMachines · medicalService{id, title, code, unit, updatedDateTimeUtc}` · GROUP `compositions[]{procedure.id, count, unit, price}` · 항목 `priceV2 · basePrice` | `getProducts` 옵션 · 옵션 검색의 SINGLE 진료항목 · `getMedicalServices` |
| `getTicketBundlesQuery` 묶음 17개 | `optionConfiguration{optionId, optionTitle, productTitle}` · `price` · `ticketSets[]{procedure, medicalService, tickets 수}` | 위와 같음 + 그 묶음의 구매 항목 |
| `getPurchaseItemStatistics`(데모 전체 162건, 2026-08-25 ~ 11-10) | `productTitle · productOptionTitle · basePriceAmountV2 · procedureConfigurations[]{medicalService{code, unit}, finalUnit}` | 위와 같음(옵션 id 칸이 없어서 상품명 + 옵션명 쌍으로 맞췄다. 쌍은 메뉴에서 모두 하나뿐이었다) |
| 일정 작업 `productOptionConfiguration` 93건 | 조사 1 §5 | 조사 1 §5 |

### 1.2 칸별 결과(확인)

| 칸 | 같음 | 다름 | 해석 |
|---|---:|---:|---|
| `optionConfiguration.id` 가 메뉴에 있음 | 63 | 0 | 구매 항목 쪽. 시술권 쪽은 **16/17**(1건 없음 → §1.3 ①) |
| 옵션 `title` | 63 | 0 | |
| `productTitle` | 63 | 0 | 시술권 쪽도 16/16 같음 |
| `optionType` | 63 | 0 | |
| SINGLE `count` | 54 | 0 | |
| SINGLE `procedure.id` | 54 | 0 | |
| SINGLE `unit`(메뉴는 진료항목의 단위) | 51 | **3** | §1.3 ② |
| SINGLE `medicalService.id · title · code · unit` | 54 | 0 | |
| 박힌 진료항목 `updatedDateTimeUtc` == 지금 진료항목 | 72 | 0 | 72건 모두 진료항목의 마지막 수정이 **구매보다 앞선다**. 그래서 이 칸으로는 스냅샷인지 참조인지 가를 수 없다 |
| GROUP 구성 수 · 시술 id · `count` · `unit` | 9 | 0 | |
| `optionConfiguration.price` · `priceV2.amount` · `basePrice.amount` vs 메뉴 정가 | 0 | **63** | 63건 모두 **구매 가격 = 메뉴 `amount` × 1.1**. 구매 쪽 `suppliedAmount` 가 메뉴 `amount` 와 같고(63/63), `suppliedAmount + vatAmount == amount`(63/63)다. 메뉴의 「정가」는 부가세 별도, 구매는 부가세 포함으로 보인다(추정 · 문서에 없음). **값이 바뀐 것이 아니라 일정한 환산이다** |
| GROUP 구성 `price.amount` | 0 | 9 | 위와 같은 × 1.1. 구성 가격 합 == 옵션 가격(9/9) |
| 구매 `priceV2.taxation` vs 메뉴 `taxation` | 49 | 14 | 메뉴가 `Taxation_UNKNOWN` 인 14건이 구매 쪽에서는 `TAXABLE` 이다(진료항목 과세 유형을 따른 것으로 추정) |
| SINGLE `medicineAndMachines` | 3 | 51 | 구매 쪽은 **54/54 가 빈 배열**이다. 메뉴에는 51건에 값이 있다. 기기 · 약물은 구매 쪽의 박힌 진료항목 `configuration.machines/medicines` 에만 있다. 구매 쪽이 이 칸을 채우지 않는 것으로 보인다(일정한 차이) |
| 통계 162건: 상품명 + 옵션명 쌍이 메뉴에 있음 | 158 | 0 | PRODUCT_OPTION 158건 전부. 나머지 4건은 선불카드 상품 |
| 통계: `basePriceAmountV2` == 메뉴 × 1.1 | 155 | **3** | §1.3 ② 와 같은 3건 |
| 통계: 박힌 진료항목 `code · unit` 이 지금 메뉴와 같음 | 182 | 0 | |
| 시술권 묶음 `optionTitle · productTitle` | 16 | 0 | 메뉴에 있는 16건 기준 |
| 시술권 `ticketSets[].procedure` 집합 == 메뉴 옵션의 시술 집합 | 15 | 1 | 다른 1건은 GROUP 인데 묶음에 세트가 1개만 남은 경우다(§3.3). 값이 바뀐 것은 아니다 |
| 세트당 시술권 장수 == 메뉴 `count` | 17 | 0 | |

### 1.3 스냅샷의 증거(확인)

**① 메뉴에서 삭제된 옵션을 가진 구매 · 시술권 — 1건**

| 관찰 | 값 |
|---|---|
| 구매 시점 | 2026-08 하순(데모에서 가장 이른 구매 무렵), 수납 상태 `ACCEPTED` |
| 시술권 | 묶음 1개 · 세트 1개 · 시술권 1장 `AVAILABLE`(지금도 쓸 수 있는 상태) |
| `optionId` | 지금 `getProducts` 에 **없다**. `getProductOptions([그 id])` → `{"data": []}`. `getProducts(optionIds=[그 id])` → `{"data": []}` |
| 구매 항목 시술 `procedure.id` | 지금 `getProcedures`(「삭제되지 않은 시술」)에 **없다** |
| 구매 항목 진료항목 `medicalService.id` | 지금 `getMedicalServices`(「삭제되지 않은 진료항목」)에 **없다**. 그런데 구매 항목에 박힌 진료항목은 `status: PUBLISHED`, `deleted: false` 로 온다 → **산 시점 상태가 그대로 박혀 있다** |
| 지금 메뉴 | **같은 상품명 · 같은 옵션명**의 옵션이 **다른 id** 로 있다. 가격(× 1.1 환산) · 횟수 · 단위는 같고, 시술 id 와 진료항목 id 는 다르다. 그 진료항목은 이 구매 **뒤에** 만들어졌다(`draftedDateTimeUtc` > 구매 `createdDateTimeUtc`) |
| 시술권 쪽 | 묶음의 `optionTitle · productTitle`, 세트의 `procedure.id · medicalService.id` 가 구매 항목(옛 값)과 같다 |

해석(추정): 구매 뒤 메뉴가 **다시 만들어졌다**(옛 옵션 · 시술 · 진료항목 삭제 → 같은 이름으로 새로 만듦). 구매와 시술권은 옛 id 와 옛 내용을 그대로 들고 있다. 메뉴를 가리키기만 하는 구조였다면 지울 때 같이 사라지거나 `deleted` 로 보였어야 한다. **최소한 「삭제」에 대해서는 스냅샷이다.**

**② 구매 시 단위 수량이 메뉴와 다른 구매 — 3건**

| 구매 | 메뉴와 다른 칸 | 비율 |
|---|---|---|
| SINGLE 2건 | `unit.value`(종류는 같음) · 가격 | 단위 ×2 → 가격 = 메뉴 × 1.1 × 2 |
| GROUP 1건 | 구성 1개의 `unit.value` · 그 구성 가격 · 옵션 가격 | 단위 ×1.33 → 그 구성 가격 ×1.47(= 1.1 × 1.33) |

- 통계 쪽 `procedureConfigurations[].finalUnit` 이 진료항목의 단위와 다른 3건이 위 3건과 같다. 「구매할 때 최종 단위를 바꿀 수 있고, 그 값이 구매에 남는다」로 보인다(추정 · `finalUnit` 칸 설명은 문서에 없음)
- 이 3건은 메뉴가 바뀐 것이 아니다. 다만 **구매 항목이 메뉴와 다른 자기 값(단위 · 가격)을 들고 있다**는 확인이다

### 1.4 관찰하지 못한 것

- 메뉴에서 **수정**(이름 · 가격 · 횟수 · 구성)한 뒤 구매 쪽이 옛 값을 유지하는지. 데모의 진료항목 226개 중 첫 구매(08-25) 뒤에 수정된 것은 2개뿐이고, 그 2개를 가진 구매는 모두 수정 **뒤에** 만들어졌다(상세를 불러 본 구매 항목 63건 기준). 상품 · 옵션에는 수정 시각 칸이 없다(조사 1 §1.2). → **구분 불가**(Q-K1)
- 옵션을 「수정」하면 id 가 유지되는지, 「새로 만들기」처럼 id 가 바뀌는지(Q-K2). ① 의 사례가 수정이었는지 삭제 후 재생성이었는지는 API 로 알 수 없다
- 시각 비교: 수납 `createdDateTimeUtc` · `lastUpdatedDateTimeUtc`(63/63 이 생성보다 뒤), 시술권 `createdDateTimeUtc`(41/41 이 수납 생성 시각 이후), 박힌 진료항목 `updatedDateTimeUtc`. 메뉴 쪽에서 비교할 수 있는 시각은 진료항목의 `draftedDateTimeUtc` · `updatedDateTimeUtc` 뿐이다

---

## 2. 문서 근거

| 찾은 곳 | 결과 |
|---|---|
| openapi.yaml 모든 `description` 을 `스냅샷|snapshot|시점|변경되어도|당시|원본|최신` 으로 검색 | 수납 · 시술권 · 상품에는 **해당 서술이 없다**. 「스냅샷」이 나오는 곳은 만족도 조사뿐이다: `SatisfactionSurveyAnswer.template` 「제출 시점의 설문 템플릿 스냅샷」, `submittedVisitor` 「제출 시점의 내원객 정보 스냅샷」 등. 그 밖에는 `ConsultationVisitor.isNew` 「상담 생성 시점의 신규 내원객 여부」 |
| docs.zip(739개) 전문 검색(같은 낱말 + `반영되지 · 수정해도`) | 위 만족도 조사 문서 2개, 그리고 예약 생성의 「기존 내원객으로 예약되면 반영되지 않습니다」(성별 칸 · 무관)뿐이다 |
| [시술권 태그 「주요 개념」](https://developers.kos-solution.com/docs/openapi/ticket.md) | 「시술권: 내원객이 **구매한 상품 옵션**을 실제 시술에 사용할 수 있도록 관리하는 권리 단위」, 「상품 옵션 연결: 시술권이 **어떤 상품 옵션에서 생성되었는지** 나타내는 정보 … 상품명, 옵션명, 프로모션 정보를 통해 시술권의 판매 구성을 확인」 |
| [수납 태그 「주요 개념」](https://developers.kos-solution.com/docs/openapi/purchase.md) | 「구매 항목: 하나의 수납 안에서 내원객이 **무엇을 샀는지**를 나타내는 개별 항목」. 시점 언급은 없다 |
| [상품 태그 「주요 개념」](https://developers.kos-solution.com/docs/openapi/product.md) | 「예약의 희망 시술, 구매 항목, 시술권은 보통 **상품 옵션 단위로 연결**됩니다」. 연결 방식(복사인지 참조인지)은 없다 |
| 스펙 `OpenTicketGroupStatisticsItem.issuedDateTimeUtc` | 「발행 일시(**수납 완료로 티켓그룹 생성**)」 → 시술권은 수납이 끝날 때 만들어진다(문서) |
| 스펙 `GetTicketBundlesQueryResponse.data` | 「삭제되지 않았고, 포함된 시술권 중 `AVAILABLE` 상태가 하나 이상 있는 묶음만 포함」 |
| 스펙 `GetPurchaseSummariesQuery.purchaseIds` | 「존재하지 않거나 삭제된 수납 ID 는 응답에 포함되지 않습니다」 |

→ 「수정해도 산 것은 그대로」라는 **문서 근거는 없다**(문서에 없음). 지금 근거는 §1.3 의 실물 관찰뿐이다.

---

## 3. 고객 ↔ 상품 연결 경로

### 3.1 잇는 키(확인)

| 단계 | 키 | 데모 대조 |
|---|---|---|
| 고객 → 수납 | `getPurchaseSummariesByVisitor(visitorId)` → `data[]`. 수납 `visitorId` | 10명 · 1~5건씩 |
| 일정 → 수납 | 일정 `purchaseIds[]` → `getPurchaseSummaries(purchaseIds)` | 46개를 넣어 44건이 왔다(2건은 문서대로 「없거나 삭제」로 추정) |
| 수납 → 구매 항목 | `items[].id`(ObjectId 모양) | |
| 구매 항목 → 메뉴 | `items[].optionConfiguration.id` = 메뉴 `options[].id` | **63/63 이 메뉴에 있다 · 같은 체계**(+ 시술권 쪽 1건은 삭제된 옵션) |
| 구매 항목 → 시술권 묶음 | 묶음 `purchaseId` = 수납 `id`, `purchaseItemId` = `items[].id` | 17/17 · 그 품목이 그 수납 안에 있다 17/17 · 묶음 `visitorId` = 수납 `visitorId` 17/17 |
| 묶음 → 옵션 | 묶음 `optionConfiguration.optionId` = 구매 항목 `optionConfiguration.id` | 17/17 |
| 묶음 → 시술권 | `ticketSets[]`(구성 · 시술마다 1세트) → `tickets[]{id(**UUID**), status, price, createdDateTimeUtc}` | 세트당 장수 = 메뉴 `count`(17/17) |
| 시술권 → 일정 작업 | 작업 `procedureConfiguration.ticketConfiguration.ticketId` = `tickets[].id`, `round{total, current}` | 2명 · 작업 26개 중 묶음에 있는 것 12개. `round.total` = 세트 장수(12/12). 작업 `productOptionConfiguration.optionId` = 묶음 `optionId`(12/12) |

### 3.2 시술권 상태

| 어디서 | 값 · 건수 |
|---|---|
| 묶음 안 `tickets[].status`(41장) | `AVAILABLE` 33 · `USED` 8. `CANCELED` · `IN_USE` 는 보지 못했다(스펙 enum: `AVAILABLE · USED · CANCELED · IN_USE · TicketStatus_UNSPECIFIED`) |
| 묶음이 있는 고객 | 20명 중 6명. 나머지 14명은 `{}` 가 왔다(`data` 키 없음 · 앞 조사와 같다) |
| 작업 상태 ↔ 시술권 상태(2명) | 작업 `DONE` → 시술권 `USED` 7/7. 작업 `CANCELED` → 시술권 `AVAILABLE` 4, `USED` 1 |
| 묶음에 없는 시술권 | 2명의 작업 중 14개가 가리키는 시술권은 묶음 조회에 **나오지 않는다**(작업 상태 `DONE` 9 · `CANCELED` 2 · `READY` 2 · `WAITING` 1). 다 쓴 묶음이거나 사용 중인 시술권으로 추정된다 |

### 3.3 다 쓴 · 취소된 시술권은 어디서 보나

| 경로 | 결과 |
|---|---|
| `getTicketBundlesQuery` | AVAILABLE 이 1장 이상 **남은 묶음만** 준다(스펙). 그 묶음 안에서는 `USED` 시술권도 보인다(확인 8장). **다 쓴 묶음은 통째로 빠진다**. GROUP 에서 한 세트를 다 쓰면 그 세트가 빠지는 것으로 보인다(확인 1건: 구성 2개인데 세트 1개만 왔고, 묶음 `price` 가 구매가의 0.5배 = 남은 시술권 가격 합) |
| `getTicketGroupStatistics`(스펙: `statuses` `REMAINING · EXHAUSTED · REFUNDED` · `usedCount` · `canceledCount` · `availableCount` · `totalCount` · `perRoundPrice` · `remainingLiabilityAmount` · `productOptionId` · `purchaseItemId`) | 오늘도 **404** `No static resource statistics/open/v1/queries/get-ticket-group-statistics`(10-20 과 같다). 스펙과 문서에는 있지만 서버에 경로가 없다. 운영 호스트에서도 같은지는 확인하지 않았다(운영 키 금지) |
| 일정 작업 `ticketConfiguration{ticketId, round{total, current}}` | 쓴 시술권은 작업으로만 거슬러 볼 수 있다(`getSchedulesByVisitor` 등). 남은 장수는 따로 주지 않는다. `round` 와 작업 상태를 세어야 한다 |
| `getPurchaseItemStatistics` · `getProcedureTaskStatistics` | 시술권 상태 칸이 없다 |

→ 「고객이 산 것 전체(다 쓴 것 포함)」를 시술권 단위로 한 번에 주는 작업은 지금 **없다**. 수납(무엇을 샀나) + 묶음(남은 것) + 일정 작업(쓴 것)을 맞춰야 한다.

---

## 4. 고객 한 명 단위 비용(데모, 2026-11-11, 1회 측정)

| 보고 싶은 것 | 호출 | 시간 | 크기 |
|---|---|---|---|
| 남은 시술권 | `getTicketBundlesQuery(visitorId)` **1번** | 36~60ms(20회) | 묶음 없으면 2B(`{}`), 있으면 2~14KB |
| 산 것 전체(수납 · 구매 항목 · 거래) | `getPurchaseSummariesByVisitor(visitorId)` 1번 | 42~67ms(10회) | 3~30KB(수납 1~5건) |
| 쓴 이력(작업 · 회차) | `getSchedulesByVisitor(visitorId)` 1번 | 75~110ms(2회) | 65~77KB(일정 8~13건) |
| 여러 고객의 수납을 한 번에 | `getPurchaseSummaries(purchaseIds[])` 1번 | 77~225ms | 46개 → 154KB |

- 묶음 · 구매 항목 안에 옵션명 · 상품명 · 시술 · 진료항목이 이미 들어 있다. **메뉴를 다시 부를 필요가 없다**(삭제된 옵션도 풀린다)
- 고객 1명을 세 작업 모두로 보면 호출 3번 · 약 0.2초 · 최대 약 120KB 다. 데모 전체 구매 항목 통계 162건은 1번(144ms · 216KB)에 왔다(`limit` 최대 5000, 커서 페이징)

---

## 5. 정할 것 (결정하지 않고 모음)

1. **나눌 기준** — 「메뉴 = 지금 기준(`getProducts`)」 · 「고객 보유 = 산 시점(구매 항목 · 시술권 응답 그대로)」으로 나눌지. 지금 근거는 삭제 1건과 단위 조정 3건이다. 「수정」 사례는 Q-K1 답을 받은 뒤에 정할지
2. **고객 보유 화면의 원천** — 묶음(`getTicketBundlesQuery`)만 쓸지, 다 쓴 것까지 보여 주려고 수납 + 일정 작업을 맞출지. `getTicketGroupStatistics` 가 살아나기를 기다릴지(KOS 문의)
3. **가격 표시 기준** — 메뉴 정가(부가세 별도로 보임)와 구매 가격(× 1.1, 부가세 포함으로 보임)이 다르다. 우리 API 가 어느 쪽을 「가격」으로 줄지, 둘 다 줄지. 이 해석은 KOS 확인이 필요하다(문서에 없음)
4. **삭제된 옵션의 처리** — 구매 · 시술권의 `optionId` 가 메뉴에 없을 때(데모 1건) 우리 쪽에서 메뉴와 묶지 않고 구매 쪽 값만 보여 줄지, 「메뉴에 없음」 표시를 할지
5. **같은 이름 · 다른 id** — 메뉴 재생성으로 같은 이름의 옵션이 새 id 로 생긴 경우 둘을 같은 상품으로 볼지(이름으로 잇는 것은 추정이 된다)
6. **남은 장수 계산** — 묶음의 AVAILABLE 장수를 그대로 쓸지, `round` 와 작업 상태로 셀지. 작업 `CANCELED` 인데 시술권 `USED` 인 1건처럼 어긋나는 경우의 기준
7. **우리 쪽 저장** — 고객 보유를 우리 DB 에 복사해 둘지, 매번 KOS 에서 읽을지(고객 1명 1~3번 · 0.2초 이하). 산 시점 값을 KOS 가 이미 들고 있다는 전제가 Q-K1 에 달려 있다

---

## 출처

- 스펙: https://developers.kos-solution.com/openapi.yaml (1.0.1)
- 수납: https://developers.kos-solution.com/docs/openapi/purchase#getPurchaseSummaries · https://developers.kos-solution.com/docs/openapi/purchase#getPurchaseSummariesByVisitor · 개념 https://developers.kos-solution.com/docs/openapi/purchase.md
- 시술권: https://developers.kos-solution.com/docs/openapi/ticket#getTicketBundlesQuery · 개념 https://developers.kos-solution.com/docs/openapi/ticket.md
- 상품 개념: https://developers.kos-solution.com/docs/openapi/product.md
- 통계: https://developers.kos-solution.com/docs/openapi/statistics#getTicketGroupStatistics · https://developers.kos-solution.com/docs/openapi/statistics#getPurchaseItemStatistics
- 일정: https://developers.kos-solution.com/docs/openapi/schedule#getSchedulesByVisitor
- 만족도 조사(스냅샷 서술이 있는 유일한 곳): https://developers.kos-solution.com/docs/openapi/satisfactionsurvey.md
- 앞 조사: `reference/2026-10-12-cc-prototype/kos-demo-api.md` §2 B · §3.4 · §4 · 조사 1 `research-procedure-menu.md` §5
