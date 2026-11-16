# KOS 시술 · 상품 메뉴(procedure-menu) — 어느 깊이까지 오나

- 조사일 **2026-11-11** · cc-prototype `researcher` 워커
- 스펙: `https://developers.kos-solution.com/openapi.yaml` 를 2026-11-11 에 받았다. `info.version` 은 **1.0.1** 로, 앞 조사(10-20)와 같다
- 공식 가이드: [시술 메뉴판 개발하기](https://developers.kos-solution.com/docs/guide/procedure-menu/start-procedure-menu.md) · [상품 태그 개요(주요 개념)](https://developers.kos-solution.com/docs/openapi/product.md) · [Webhook 이벤트](https://developers.kos-solution.com/docs/guide/webhook/webhook-events.md)
- 데모 호출은 앞 조사 `reference/2026-10-12-cc-prototype/kos-demo-api.md` §1.2 의 **데모 키만** 썼다(운영 호스트 안의 데모 테넌트). 조회 **16회**(작업마다 1~2회), 쓰기(`/commands/`) **0회**, 운영 지점 키 사용 **0회**
- 이 레포는 public 이다. 키 · 토큰 · 테넌트 · id 값 · 사람 이름은 적지 않았다. 상품 · 시술 · 진료항목 이름과 코드 원문도 적지 않았다. 값은 **모양 · 건수 · enum** 만 적는다
- 표기는 앞 조사를 따른다. **확인** = 이번에 불러서 본 것, **스펙** = openapi.yaml 에 적힌 것, **가이드** = 공식 가이드 문서에 적힌 것, **추정** = 해석. 문서가 말하지 않는 것은 「문서에 없음」으로 적었다

---

## 0. 요약

### 깊이 그림

```text
getCategories ── Category{id, name, order, opened, deleted, translsMap}                    15
      ▲ categories[].id (같은 id · 확인 101/101)
getProducts / getProduct ── Product{id, title, isEvent, closed, order, …}                  101
  │   (메뉴 트리는 이것 하나로 끝까지 내려온다. 아래 ①~④ 단계가 모두 이 응답 안에 있다)
  │
  ├─ ① options[]  ── oneOf type ──┬─ SINGLE        307   price · count · procedure · medicineAndMachines[]
  │                               │                       (+ medicalService: getProductOptions · 검색에서만 옴)
  │                               ├─ GROUP          16   price · compositions[] (SINGLE 칸들은 「없어야 함」)
  │                               └─ CONSULTATION    0   (스펙에만 있음. 가격 · 구성 없음)
  │
  ├─ ② compositions[]  (GROUP 에만 있음 · 옵션마다 2개 · 32)
  │        title · count · unit · price · procedure · medicineAndMachines[] · medicalService
  │
  ├─ ③ procedure{id, name, …}  ───────────►  getProcedures 의 id 와 같다(확인 339/339)
  │    medicalService{id, …, configuration} ─►  getMedicalServices 의 id 와 같다(확인 339/339)
  │        └ configuration.procedure.id  ==  같은 단계의 procedure.id (확인 339/339)
  │
  └─ ④ medicineAndMachines[{id, name}]  ──►  getMachines ∪ getMedicines (두 목록의 id 는 서로 겹치지 않음)
           == medicalService.configuration.machines[] ∪ medicines[] (확인 307/307)

  ※ 다국어 translsMap 은 카테고리 · 상품 · 옵션 · 진료항목, 그리고 일정의 옵션 스냅샷 모든 층에 붙는다
  ※ 노출 채널(displayChannels)은 「옵션」에만 붙는다. 프로모션(promotionConfigurations, deprecated)도 옵션에 붙는다
  ※ 타겟 국가는 응답 칸이 아니다. 요청 필터(targetCountryCode)이고, 상품 목록과 옵션 검색에만 있다

일정(우리 back 이 받는 것)  tasks[].procedureConfiguration.productOptionConfiguration
      optionId ──► 메뉴 options[].id (확인 93/93) · procedure.id ──► 그 옵션의 procedure / compositions[].procedure (93/93)
```

깊이는 **상품 → 옵션 → (GROUP 이면) 구성 → 시술 · 진료항목 · 기기/약물**. 이렇게 **3~4단**이다. `getProducts` 한 번이면 진료항목 객체(일부만)까지 다 들어 있다(§1.2). 나머지 목록 작업 5개(`getProcedures` · `getMachines` · `getMedicines` · `getMedicalServices` · `getTargetCountries`)는 평평한 목록이다. 메뉴 트리에서는 id 로 가리키기만 한다.

### 질문 1~6 한 줄 답

| # | 질문 | 한 줄 답 |
|---|---|---|
| 1 | 작업별 전체 키 트리 | §1. 키 경로를 끝까지 펼쳤다. 데모 응답에는 JSON `null` 이 **0개**다. 비어 있는 칸은 `""` · `[]` · `0` 으로 오거나 **키가 아예 빠진다**. 스펙에만 있는 칸에는 「스펙」을 달았다 |
| 2 | 관계 · 깊이 | 3~4단(위 그림). 옵션과 구성의 `procedure.id` 는 `getProcedures` 와 **같은 id 체계**다(확인 339/339). `type` 은 oneOf 판별자다. SINGLE 은 시술이 1개, GROUP 은 구성이 N개(데모에서는 늘 2개), CONSULTATION 은 가격도 시술도 없다 |
| 3 | 가격 | 옵션 · 구성마다 `price{amount(정가), suppliedAmount(과세 공급가액), vatAmount(부가세), taxFreeAmount(면세), taxation, additional[](수가 유형별 특별가)}` 가 있고, 금액은 모두 `{value:int, currency}` 다. 통화는 KRW 뿐이다. 할인은 deprecated `promotionConfigurations[].discountedPrice` 뿐이고 데모에서는 비어 있다. 데모 323건 중 319건이 `taxation: Taxation_UNKNOWN` 이고 세부 금액이 0 이다 |
| 4 | 상태 · 개수 | 카테고리 15(전부 `opened`) · 상품 101(`closed` 0 · `deleted` 0 · `isEvent` 45) · 옵션 323 · 구성 32. 시술 804 · 진료항목 226 · 기기 302 · 약물 349. **페이징 없음**: 요청 스키마에 page · cursor · limit 칸이 없고, 한 번에 전부 온다. 정렬은 카테고리만 `sort` 를 받는다. 상품 `order` 는 데모에서 전부 1 이다 |
| 5 | 우리 쪽 접점 | 일정 `productOptionConfiguration.optionId` 는 메뉴 옵션 id 와 **같다**(확인 93/93). `procedure.id` 도 `getProcedures` 와 같다(93/93). 다만 `productId` 칸은 **없다**. 시술권으로 잡힌 작업은 `productTitle` 이 **빈 문자열**이다(52/52) |
| 6 | 크기 · 속도 | `getProducts` 약 **575KB · 0.3초**, 옵션 검색(빈 검색어) 약 **729KB · 0.2초**. 나머지는 0.1~185KB 이고 대개 0.03~0.12초다(약물 1회 0.8초). 메뉴 한 바퀴는 약 **870KB**, 검색 전체까지 더하면 약 **1.6MB** 다(§6). 상품이 바뀌면 Webhook `PRODUCT_CREATED · UPDATED · DELETED` 가 온다(가이드) |

---

## 1. 작업별 키 트리

### 1.0 읽는 법

- 경로 표기: `.` = 객체 안, `[]` = 배열 원소, `{}` = 맵(키가 동적), `<SINGLE>` = oneOf 갈래
- **관찰** 칸: `n/N` = 그 칸이 있는 원소 수 / 부모 원소 수. 「빈」 = `""` · `[]` · `0`. `null` 은 어느 응답에도 없었다
- **필수** 칸: 스펙 `required`. ○ = 필수, 빈칸 = 선택
- 값 예시는 **모양**만 적었다. id 는 모두 24자리 hex(ObjectId 모양, 스펙 `format: object-id`)다. 일시는 `YYYY-MM-DDTHH:MM:SS.sssZ` 다
- 같은 하위 모양이 여러 작업에 반복된다. 그래서 §1.1 에 **공통 조각**을 먼저 정의하고, 작업별 표(§1.2~)는 그 조각을 가리킨다

### 1.1 공통 조각

#### `TranslsMap` (다국어)

| 경로 | 타입 | 관찰 | 근거 |
|---|---|---|---|
| `translsMap{필드명}` | map → object | 키 = 번역 대상 필드 이름(`title` · `name` · `description` · `caution` · `coverImageUrl` · `contentImageUrl` · `optionTitle` · `productTitle`) | 확인 · 스펙 |
| `translsMap{필드명}.translation{언어}` | map → string | 언어 키: `ko` · `ja` · `zh-Hans` · `zh-Hant` · `en`. 다섯 개가 다 오지 않는 칸도 있다(`ko` 만 있는 칸 등) | 확인 |

가이드 예제의 로케일 목록에는 `th` 도 있지만 데모에서는 보지 못했다. 스펙은 「키는 언어 코드」라고만 적었고 허용 목록은 **문서에 없음**.

#### `Money` · `Price`

| 경로 | 타입 | 필수 | 관찰 | 근거 |
|---|---|---|---|---|
| `Money.value` | int32 | ○ | 원 단위 정수 | 확인 · 스펙 |
| `Money.currency` | string(ISO 4217) | ○ | `KRW` 뿐. `taxation` 이 UNKNOWN 인 세부 금액에서는 `""` | 확인 |
| `price.amount` | Money | ○ | 정가. 323/323 | 확인 · 스펙 「정가」 |
| `price.suppliedAmount` | Money |  | 과세 공급가액. `getProducts` 에서는 늘 있고 UNKNOWN 이면 `0`·`""`. `getProductOptions` · 검색에서는 UNKNOWN 이면 **키가 빠진다** | 확인 |
| `price.vatAmount` | Money |  | 부가세(위와 같음) | 확인 |
| `price.taxFreeAmount` | Money |  | 면세 금액(위와 같음) | 확인 |
| `price.taxation` | enum |  | `Taxation_UNKNOWN` 319 · `TAXABLE` 4 (스펙: + `TAX_FREE` · `MIXED`) | 확인 · 스펙 |
| `price.additional[]` | array<object> |  | 323/323 빈 배열 | 확인 |
| `price.additional[].visitorType{id, name}` | object | ○ | 고객 수가 유형 | 스펙 |
| `price.additional[].amount · suppliedAmount · vatAmount · taxFreeAmount · taxation` | Money · enum |  | 수가 유형별 특별가 | 스펙 |

#### `Procedure` (옵션 · 구성 안에 박힌 시술)

| 경로 | 타입 | 필수 | 관찰 | 근거 |
|---|---|---|---|---|
| `id` | object-id | ○ | `getProcedures` 의 id 와 같다 | 확인 |
| `name` | string | ○ | 있음 | 확인 |
| `createDate` | string | ○ | **339/339 빈 문자열** | 확인 |
| `categoryIds` | array<string> |  | 339/339 빈 배열 | 확인 |
| `commonProcedureConfiguration{id, name}` | object |  | 0/339 | 스펙 |
| `deleted` | boolean |  | 0/339 | 스펙 |
| `searchPhoneticName` | string |  | 0/339(진료항목 안의 `configuration.procedure` 에는 있다) | 스펙 |

#### `MedicalService` (진료항목 — `getMedicalServices` 원소와 같은 객체)

| 경로 | 타입 | 필수 | 관찰(getMedicalServices 226건) | 근거 |
|---|---|---|---|---|
| `id` | object-id | ○ | 226/226 | 확인 |
| `title` | string | ○ | 226/226 | 확인 |
| `description` | string |  | 15/226. 옵션 안에 박힌 진료항목은 `""` 로 늘 온다 | 확인 |
| `caution` | string |  | 0/226. 박힌 쪽은 `""` 로 온다 | 확인 |
| `deleted` | boolean | ○(박힌 쪽 스펙) | `getMedicalServices` 에는 칸이 없다(스펙에도 없음). 박힌 쪽은 `false` | 확인 · 스펙 |
| `status` | enum | ○ | `PUBLISHED` 226 (스펙: + `DRAFT` · `MedicalServiceStatus_UNKNOWN`) | 확인 · 스펙 |
| `configuration.code` | string | ○ | 226/226, 서로 다름. 모양은 `NN-영문약어-…`(값은 안 적음) | 확인 |
| `configuration.procedure{id, name, searchPhoneticName, categoryIds[]}` | object | ○ | 226/226. id 는 `getProcedures` 안에 있다(226/226) | 확인 |
| `configuration.machines[{id, name, searchPhoneticName}]` | array |  | 63/226 이 1개, 나머지는 빈 배열 | 확인 |
| `configuration.medicines[{id, name, searchPhoneticName}]` | array |  | 159/226 이 1개, 나머지는 빈 배열 | 확인 |
| `configuration.unit{type, value:double}` | object |  | 150/226. `type`: `CC` 62 · `UNIT` 38 · `SHOT` 18 · `KJ` 16 · `QUANTITY` 7 · `PULSE` 5 · `MINUTE` 2 · `VIAL` 1 · `SYRINGE` 1 (스펙 enum 22종) | 확인 · 스펙 |
| `configuration.healthcareReimbursement` | enum | ○ | `NON_REIMBURSABLE` 226 (스펙: + `REIMBURSABLE`) | 확인 |
| `configuration.taxation` | enum | ○ | `TAXABLE` 226 | 확인 |
| `draftedDateTimeUtc` · `updatedDateTimeUtc` | date-time | ○ | 226/226 | 확인 |
| `translsMap` | TranslsMap |  | `title` 226 · `description` 15 · `caution` 1 | 확인 |
| `priceAmount{value, currency}` | Money |  | 0/226 | 스펙 |
| `durationTime` | double |  | 0/226 | 스펙 |
| `contributionConstant` | int32 |  | 0/226 | 스펙 |
| `recommendedInterval` | int32 |  | 0/226 | 스펙 |

#### `Option` — oneOf, 판별자 `type`

| 경로 | 타입 | 필수 | SINGLE | GROUP | CONSULTATION | 근거 |
|---|---|---|---|---|---|---|
| `id` | object-id | ○ | 307/307 | 16/16 | 스펙 | 확인 |
| `type` | enum const | ○ | `SINGLE` | `GROUP` | `CONSULTATION` | 확인(CONSULTATION 은 스펙) |
| `title` · `description` | string | ○ | 있음(설명은 모두 채워져 있음) | 있음 | 스펙 | 확인 |
| `deleted` | boolean | ○ | 전부 `false` | 전부 `false` | 스펙 | 확인 |
| `price` | Price | ○(SINGLE · GROUP) | 307/307 | 16/16 | **없어야 함**(스펙 `not`) | 확인 · 스펙 |
| `count` | int32 | ○(SINGLE) | 1 → 259 · 3 → 19 · 5 → 25 · 10 → 4 | 없어야 함 | 없어야 함 | 확인 · 스펙(「시술 횟수」) |
| `unit{type, value}` | object |  | **0/307**(단위는 진료항목 `configuration.unit` 에 있다) | 없어야 함 | 없어야 함 | 확인 · 스펙 |
| `procedure` | Procedure |  | 307/307 | 없어야 함 | 없어야 함 | 확인 · 스펙 |
| `medicineAndMachines[{id, name}]` | array |  | 302/307 에 1~2개, 5건은 빈 배열 | 스펙은 「없어야 함」인데 **빈 배열로 온다**(16/16) | 없어야 함 | 확인 · 스펙 |
| `medicalService` | MedicalService | ○(SINGLE 스펙) | `getProducts` · `getProduct` 에서는 **0/307 — 빠진다**. `getProductOptions` · 검색에서는 온다 | 없어야 함 | 없어야 함 | 확인 · 스펙 |
| `compositions[]` | array<Composition> | ○(GROUP) | 스펙은 「없어야 함」인데 **빈 배열로 온다**(307/307) | 16/16, 원소 늘 2개 | 없어야 함 | 확인 · 스펙 |
| `displayChannels[]` | array<enum> |  | `HOMEPAGE` 307 · `GANGNAMUNNI` 2 · `KOS_CONNECT` 2 | `HOMEPAGE` 16 · `GANGNAMUNNI` 1 · `KOS_CONNECT` 1 | 스펙 | 확인 · 스펙(+ `DisplayChannel_UNKNOWN`) |
| `badges[]` | array<int32> |  | 전부 빈 배열 | 전부 빈 배열 | 스펙 | 확인 · 스펙(0 UNKNOWN · 1 NEW · 2 POPULAR · 3 RECOMMENDED) |
| `frequentlyUsedOption` | boolean |  | 전부 `false` | 전부 `false` | 스펙 | 확인 |
| `promotionConfigurations[]` | array · **deprecated** |  | 전부 빈 배열 | 전부 빈 배열 | 스펙 | 확인 · 스펙 |
| `promotionConfigurations[].{id, optionId, title, startDate, endDate, discountedPrice:Price}` | object | ○ | — | — | — | 스펙 |
| `translsMap` | TranslsMap |  | `title` · `description` | 같음 | — | 확인 |

#### `Composition` (GROUP 옵션의 `compositions[]` 원소)

| 경로 | 타입 | 필수 | 관찰(32건) | 근거 |
|---|---|---|---|---|
| `title` | string | ○ | 32/32 | 확인 |
| `count` | int32 | ○ | 1 → 26 · 5 → 4 · 10 → 2 | 확인 |
| `unit{type, value:double}` | object | ○ | `UnitType_UNKNOWN`(값 0) 14 · `SHOT` 10 · `KJ` 3 · `CC` 3 · `VIAL` 1 · `PULSE` 1 | 확인 |
| `price` | Price | ○ | 32/32. **구성 가격의 합 == 옵션 가격**(16/16) | 확인 |
| `procedure` | Procedure | ○ | 32/32 | 확인 |
| `medicineAndMachines[{id, name}]` | array |  | 32/32 에 1개 | 확인 |
| `medicalService` | MedicalService |  | 32/32 | 확인 |
| `refSingleOptionId` | string · **deprecated** | ○ | `getProducts` · `getProduct` 에서는 **32/32 빈 문자열**. `getProductOptions` · 검색에서는 키가 빠진다 | 확인 · 스펙 |

### 1.2 `getProducts` — 상품 목록 · [문서](https://developers.kos-solution.com/docs/openapi/product#getProducts) · [md](https://developers.kos-solution.com/docs/openapi/get-products.md)

요청 칸(스펙): `title` · `categoryId` · `isEvent` · `optionIds[]` · `targetCountryCode` · `deleted`(무시됨) · `includePromotions`(deprecated). 필수 칸은 없다. **페이징 칸 없음.** 스펙 설명: 「요청한 API Key에 해당하는 채널에 노출 가능한 상품만 반환」, 「Open API 에서는 요청값과 관계없이 삭제되지 않은 상품만」.

| 경로 | 타입 | 필수 | 관찰(101건) | 근거 |
|---|---|---|---|---|
| `data[]` | array<Product> |  | 101 | 확인 |
| `.id` | object-id | ○ | 101 | 확인 |
| `.title` · `.description` | string | ○ | 101 · 101 | 확인 |
| `.caution` | string |  | 101 전부 `""` | 확인 |
| `.cautions[]` | array<string> · deprecated |  | 101 전부 빈 배열 | 확인 · 스펙(대체: `caution`) |
| `.categories[{id, name, translsMap}]` | array |  | **101/101 에 1개씩**(스펙 개념 문서에는 「여러 카테고리 가능」) | 확인 · 스펙 |
| `.options[]` | array<Option> |  | 1~28개. 1개짜리 상품 54 · 2개 18 · 3개 7 · … 합계 323 | 확인 |
| `.medicineAndMachines[{id, name}]` | array |  | 1~7개. **옵션들의 합집합과 같다**(101/101) | 확인 |
| `.closed` | boolean | ○ | `false` 101 | 확인 · 스펙(true = 사용 안 함) |
| `.deleted` | boolean | ○ | `false` 101 | 확인 |
| `.isEvent` | boolean |  | `true` 45 · `false` 56 | 확인 |
| `.order` | int32 |  | **101 전부 `1`** | 확인 |
| `.badges[]` | array<int32> |  | 101 전부 빈 배열 | 확인 |
| `.translsMap` | TranslsMap |  | `title` · `description` 101, `caution` · `coverImageUrl` · `contentImageUrl` 2 | 확인 |
| `.coverImageUrl` · `.contentImageUrl` | string |  | **0/101**(키가 빠짐. 번역 맵 쪽에만 2건) | 스펙 |
| `.displayPeriod{startDateTimeUtc, endDateTimeUtc}` | object |  | 0/101. 「미설정 시 상시 노출」 | 스펙 |
| `.offeringPeriod{startDateTimeUtc, endDateTimeUtc}` | object |  | 0/101. 「미설정 시 상시 제공(예약/수납 가능)」 | 스펙 |
| `.startDateTimeUtc` · `.endDateTimeUtc` | string · deprecated |  | 0/101 | 스펙 |

### 1.3 `getProduct` — 상품 단건 · [문서](https://developers.kos-solution.com/docs/openapi/product#getProduct)

- 요청은 `id`(필수) 하나다. 응답은 **`data` 로 감싸지 않고 상품 객체가 최상위**에 온다(앞 조사와 같음)
- GROUP 옵션이 있는 상품 1건을 불렀다. 같은 상품의 `getProducts` 원소와 **키 집합 · 값이 같았다**. 옵션 안의 키도 같았다. SINGLE 에 `medicalService` 가 빠지는 것도 같다
- 오류(스펙): 400 `GetProductProductNotFoundError`

### 1.4 `getProductOptions` — 옵션 id 로 상세 · [문서](https://developers.kos-solution.com/docs/openapi/product#getProductOptions)

- 요청: `optionIds[]`(필수, 1개 이상) · `includePromotions`(필수인데 **deprecated**) · `refOptionIds[]`(deprecated)
- 스펙 설명: 「삭제되지 않고 사용 중인 상품에 속한, 삭제되지 않은 옵션만. 삭제된 상품 · 사용 중지된 상품 · 삭제된 옵션 · 없는 id 는 응답에서 빠진다」
- 옵션 4개(SINGLE 3 · GROUP 1)를 `includePromotions: true` 로 한 번, `false` 로 한 번 불렀다. **두 응답이 바이트까지 같았다**

`getProducts` 의 같은 옵션과 비교한 차이(확인):

| 칸 | `getProducts` · `getProduct` | `getProductOptions` |
|---|---|---|
| SINGLE `medicalService`(MedicalService 전체) | 없음 | **있음**(3/3) |
| `price` 세부 금액(`taxation` 이 UNKNOWN 일 때) | `0` · `""` 로 옴 | **키가 빠짐** |
| GROUP `compositions[].refSingleOptionId` | `""` 로 옴 | 키가 빠짐 |
| 응답 감싸기 | `data[]` | `data[]`(원소가 Option 이고 상품 정보 없음) |

### 1.5 `searchProductOptionSummaries` — 옵션 검색 · [문서](https://developers.kos-solution.com/docs/openapi/product#searchProductOptionSummaries)

- 요청: `searchText`(필수) · `targetCountryCode`. 「채널에 노출 가능한 옵션만 검색」(스펙)
- `searchText: "a"` → 279건. `searchText: ""` → **323건 = 메뉴의 옵션 전부**(확인). 가이드는 「빈 문자열은 API 를 호출하지 말라」고 권한다
- 원소 = Option(§1.1) **+ 상품 요약 칸**, **− 일부 칸**:

| 경로 | 타입 | 관찰(323건) | 근거 |
|---|---|---|---|
| `productId` | object-id · **deprecated** | 323/323. 메뉴 상품 id 와 일치 323/323 | 확인 · 스펙(대체: `productConfiguration.id`) |
| `productTitle` | string · deprecated | 323/323 | 확인 · 스펙(대체: `productConfiguration.title`) |
| `productIsEvent` | boolean · deprecated | `true` 63 · `false` 260 | 확인 · 스펙(대체: `productConfiguration.isEvent`) |
| `productConfiguration{id, title, isEvent, displayPeriod, offeringPeriod}` | object | **0/323 — 대체 칸이 아직 안 온다** | 스펙 · 가이드 |
| SINGLE `medicalService` | MedicalService | 307/307(검색에는 있다) | 확인 |
| `deleted` · `displayChannels` · `badges` · `frequentlyUsedOption` · `promotionConfigurations` | — | **칸 없음**(스펙에도 없음) | 확인 · 스펙 |

### 1.6 `getCategories` — 카테고리 · [문서](https://developers.kos-solution.com/docs/openapi/product#getCategories)

- 요청: `opened`(Open API 는 값과 관계없이 노출 카테고리만 준다) · `sort{by, order: ASC|DESC|Order_UNKNOWN}`. 오류(스펙): 400 `InvalidSortCriteria`
- 요청 본문 `{}` 로 불렀다. 응답은 `order` 0~14 순서대로 왔다

| 경로 | 타입 | 필수 | 관찰(15건) | 근거 |
|---|---|---|---|---|
| `data[].id` | object-id | ○ | 15. 상품 `categories[].id` 15종과 같은 집합 | 확인 |
| `data[].name` | string | ○ | 15 | 확인 |
| `data[].order` | int32 | ○ | 0~14, 겹치지 않음 | 확인 |
| `data[].opened` | boolean | ○ | `true` 15 | 확인 |
| `data[].deleted` | boolean | ○ | `false` 15 | 확인 |
| `data[].translsMap` | TranslsMap |  | `name` 15(5개 언어) | 확인 |

상품 수는 카테고리마다 1~46 으로 고르지 않다(카테고리 15개 전부에 상품이 있다).

### 1.7 `getProcedures` · `getMachines` · `getMedicines` — 평평한 목록 · [문서](https://developers.kos-solution.com/docs/openapi/product)

| 작업 | 요청 | 응답 | 관찰 | 근거 |
|---|---|---|---|---|
| `getProcedures` | `name`(부분 검색, 생략하면 전부) | `data[{id ○, name ○}]` | 804. 이름 중복 0 | 확인 · 스펙(「삭제되지 않은 시술」) |
| `getMachines` | `name` | `data[{id ○, name ○}]` | 302 | 확인 · 스펙 |
| `getMedicines` | `name` | `data[{id ○, name ○}]` | 349 | 확인 · 스펙 |

- 세 목록의 id 는 서로 겹치지 않는다(기기 ∩ 약물 0, 시술 ∩ 기기 0)
- 메뉴(옵션)가 실제로 쓰는 것은 일부다. 시술 **86/804**, 기기 **19/302**, 약물 **44/349**(진료항목 기준). 나머지는 메뉴에 걸리지 않은 기준 데이터다(추정)
- 시술 · 기기 · 약물 객체에는 가격 · 단위 · 상태 칸이 **없다**(스펙도 `id` · `name` 둘뿐)

### 1.8 `getMedicalServices` — 진료항목 · [문서](https://developers.kos-solution.com/docs/openapi/product#getMedicalServices)

- 요청: `title`(부분 검색). 응답: `data[MedicalService]`(§1.1). 226건이다. 「삭제되지 않은 진료항목」(스펙)
- 시술 1개에 진료항목이 여러 개 걸릴 수 있다. 진료항목이 걸린 시술은 87개이고, 한 시술에 최대 16개가 걸렸다(확인). 진료항목은 「시술 + 단위 + 기기/약물 + 코드」 조합의 단위다(추정)
- 메뉴 옵션이 쓰는 진료항목은 225/226 이다

### 1.9 `getTargetCountries` — 타겟 국가 · [문서](https://developers.kos-solution.com/docs/openapi/targetcountry#getTargetCountries)

| 경로 | 타입 | 필수 | 관찰(4건) | 근거 |
|---|---|---|---|---|
| `data[].code` | string(ISO 3166-1 alpha-2 · `ETC`) | ○ | `KR` 2 · `ETC` 2 (**같은 코드가 두 번씩** 온다) | 확인 |
| `data[].order` | int32 | ○ | 0 · 1 · 1 · 3 | 확인 |
| `data[].suggestingVisitorTypeId` | string |  | 0/4. 「값이 없으면 기본 수가 유형인 `정상가`」 | 스펙 |

※ 앞 조사의 문서 링크 `…/docs/openapi/target-country#…` 는 지금 **404** 다. 지금 경로는 `…/docs/openapi/targetcountry` 다(200 확인).

---

## 2. 관계 · 깊이

### 2.1 단계와 잇는 키

| 단계 | 부모 → 자식 | 잇는 키 | 실제 대조(확인) |
|---|---|---|---|
| 0 → 1 | 카테고리 → 상품 | 상품 `categories[].id` = 카테고리 `id` | 101/101 일치 |
| 1 → 2 | 상품 → 옵션 | 포함 관계(`options[]`). 옵션 쪽에서 위로 가는 키는 검색 응답의 `productId`(deprecated)뿐이다 | 옵션 id 323개는 상품 사이에 중복 없음 · 검색 `productId` 323/323 일치 |
| 2 → 3 | GROUP 옵션 → 구성 | 포함 관계(`compositions[]`). 구성에는 자기 id 가 **없다**. `refSingleOptionId` 는 deprecated 이고 값도 비어 있다 | 32/32 빈 값 |
| 2·3 → 시술 | 옵션(SINGLE) · 구성 → 시술 | `procedure.id` = `getProcedures[].id` | SINGLE 307/307 · 구성 32/32 |
| 2·3 → 진료항목 | 옵션(SINGLE) · 구성 → 진료항목 | `medicalService.id` = `getMedicalServices[].id` | 307/307 · 32/32 |
| 진료항목 → 시술 | 진료항목 → 시술 | `medicalService.configuration.procedure.id` | 같은 단계의 `procedure.id` 와 339/339 같음 |
| 2·3 → 기기 · 약물 | 옵션 · 구성 → 기기/약물 | `medicineAndMachines[].id` ∈ `getMachines` ∪ `getMedicines` | SINGLE: 기기 88 · 약물 215 · 미일치 0 / 구성: 기기 24 · 약물 8 · 미일치 0 |
| 〃 | 〃 | `medicineAndMachines` = 진료항목 `configuration.machines ∪ medicines` | 307/307 |
| 1 ← 2 | 상품 `medicineAndMachines` | 옵션들 `medicineAndMachines` 의 합집합 | 101/101 |

**판단 요점**(확인): `medicineAndMachines` 는 기기와 약물을 한 배열에 섞는다. 원소에 종류를 가르는 칸이 없다. 어느 쪽인지는 `getMachines` · `getMedicines` 의 id 와 대조하거나, 진료항목 `configuration.machines` / `medicines` 를 보고 갈라야 한다.

### 2.2 `type` 이 구조를 바꾸는 방식(스펙 `oneOf` + `discriminator: type`, 갈래마다 `allOf: not required` 로 금지 칸을 둔다)

| type | 있는 것 | 없어야 하는 것(스펙) | 데모에서 실제로 온 것 |
|---|---|---|---|
| `SINGLE` | `price` · `count` · `procedure` · `medicineAndMachines` · `medicalService`(필수) · `unit` | `compositions` | `compositions: []` 가 온다. `unit` 은 0/307. `medicalService` 는 상품 계열 응답에서 빠진다 |
| `GROUP` | `price` · `compositions[]`(필수) | `unit` · `count` · `procedure` · `medicineAndMachines` · `medicalService` | `medicineAndMachines: []` 가 온다. 시술 · 단위 · 횟수는 구성마다 따로 있다 |
| `CONSULTATION` | `id` · `title` · `description` · `displayChannels` · `badges` · … | `price` · `unit` · `count` · `procedure` · `medicineAndMachines` · `compositions` · `medicalService` | 데모에 **0건** |

즉 **시술이 붙는 깊이가 type 에 따라 다르다**. SINGLE 은 옵션 바로 아래(2단)에 붙고, GROUP 은 구성 아래(3단)에 붙고, CONSULTATION 은 아무 데도 붙지 않는다.

### 2.3 부가 축이 붙는 곳

| 축 | 붙는 층 | 근거 |
|---|---|---|
| 다국어 `translsMap` | 카테고리(`name`) · 상품(`title` · `description` · `caution` · 이미지 URL) · 상품 안 카테고리 · 옵션(`title` · `description`) · 진료항목(`title` · `description` · `caution`) · 검색 원소(`productTitle` 포함) · 일정의 옵션 스냅샷(`optionTitle`) | 확인 |
| 노출 채널 `displayChannels` | **옵션만**. 상품 · 구성에는 없다. 검색 원소에도 없다 | 확인 · 스펙 |
| 채널 필터 | 상품 목록 · 상품 단건 · 옵션 검색은 「**API Key 의 채널**에 노출 가능한 것만」 준다. 데모 옵션 323건은 모두 `HOMEPAGE` 를 가진다. 그래서 데모 키의 채널이 HOMEPAGE 라고 보는 것이 **추정**이다. 키와 채널의 대응표는 **문서에 없음** | 스펙 · 확인 · 추정 |
| 프로모션 | 옵션 `promotionConfigurations[]`(deprecated). 요청 `includePromotions`(deprecated)를 true/false 로 바꿔도 응답이 **같았다**. 가이드는 이벤트를 `isEvent` 로 다루라고 권한다 | 확인 · 스펙 · 가이드 |
| 이벤트 | 상품 `isEvent`(+ 요청 필터 `isEvent`). 검색 원소는 `productIsEvent`(deprecated) | 확인 · 스펙 |
| 타겟 국가 | **응답 칸이 아니다.** 요청 필터 `targetCountryCode` 이고, `getProducts` 와 옵션 검색에만 있다. 데모에서 `ETC` 로 거르니 101/323 이 그대로였고 값도 같았다. 국가 → `suggestingVisitorTypeId` → `price.additional[].visitorType` 으로 이어진다는 것은 **추정**이다(국가별 가격이 어떻게 고르는지는 문서에 없음) | 확인 · 스펙 · 추정 |
| 노출 · 제공 기간 | 상품 `displayPeriod` · `offeringPeriod`. 검색은 `productConfiguration.*Period`. 데모에서는 둘 다 0건 | 스펙 · 가이드 |

---

## 3. 가격

| 위치 | 종류 | 데모 |
|---|---|---|
| `options[].price` (SINGLE · GROUP) | 정가 `amount` · 과세 공급가액 `suppliedAmount` · 부가세 `vatAmount` · 면세 `taxFreeAmount` · 과세 유형 `taxation` · 수가 유형별 특별가 `additional[]` | 323건 모두 정가가 0보다 크다. `TAXABLE` 4건 · UNKNOWN 319건. `additional` 은 전부 빈 배열이다 |
| `compositions[].price` | 위와 같은 모양 | **구성 가격의 합 = 옵션 정가**(16/16) |
| `promotionConfigurations[].discountedPrice` (deprecated) | 할인가(위와 같은 모양) + 기간 `startDate` · `endDate` | 전부 빈 배열 |
| `medicalService.priceAmount` | 진료항목 기준가 `{value, currency}` | 0/226(스펙에만 있음) |
| 시술 · 기기 · 약물 | — | 가격 칸 없음 |

- **단위**: 금액은 `Money{value:int32, currency}` 이고 `currency` 는 `KRW` 뿐이다. 수량 단위는 가격 칸과 따로 있다. SINGLE 은 `count` 와 진료항목의 `configuration.unit{type, value}`, 구성은 `count` 와 `unit` 이다. 「1회당 가격」 칸은 없다(문서에 없음)
- **세금 관찰(확인)**: `TAXABLE` 4건은 모두 `suppliedAmount == amount` 이고 `vatAmount` = 정가의 10% 다. 그래서 `amount ≠ suppliedAmount + vatAmount` 다. 정가가 부가세를 포함한 값인지는 **문서에 없음**. UNKNOWN 319건은 세부 금액이 전부 0 이다(`getProducts`) 또는 키가 빠진다(`getProductOptions` · 검색)
- **가이드와 스펙의 차이**: 가이드 「상품 카드 구성」 표는 `originalPrice` · `discountRate` 를 원가/할인 칸으로 들었다. 그러나 메뉴 스키마에는 **이 칸이 없다**. 스펙 전체에서 `discountRate` 는 시술권 통계(`OpenTicketGroupStatisticsItem`)에만 있고, 이름이 비슷한 `originalPriceAmount` 도 거기에만 있다. 가이드는 「옵션별 가격이 `null` 이면 상담 후 결정」이라고도 적었지만, 데모에서 가격 없는 SINGLE · GROUP 은 0건이었다(CONSULTATION 이 가격 없는 갈래다)

---

## 4. 상태 · 개수 · 정렬 · 페이징

| 항목 | 값 | 근거 |
|---|---|---|
| 카테고리 | 15 · `opened` 15 · `deleted` 0 | 확인 |
| 상품 | 101 · `closed` 0 · `deleted` 0 · `isEvent` 45 | 확인 |
| 옵션 | 323(SINGLE 307 · GROUP 16 · CONSULTATION 0) · `deleted` 0 | 확인 |
| 구성 | 32(GROUP 16 × 2) | 확인 |
| 시술 / 진료항목 / 기기 / 약물 | 804 / 226 / 302 / 349 | 확인 |
| 타겟 국가 | 4(`KR` × 2 · `ETC` × 2) | 확인 |
| 10-20 대비 | 상품 101 · 검색 "a" 279 · 시술 804 · 기기 302 · 약물 349 · 진료항목 226 · 카테고리 15 · 국가 4. **모두 같다**(데모 메뉴가 3주 동안 바뀌지 않았다) | 확인 |
| 걸러서 주는 것 | Open API 는 삭제된 상품 · 숨긴 카테고리를 요청값과 관계없이 빼고 준다. 채널에 안 걸린 상품 · 옵션도 뺀다. `getProductOptions` 는 사용 중지된(`closed`) 상품의 옵션도 뺀다. `getProducts` 가 `closed: true` 상품을 주는지는 **문서에 없음**이고, 데모에는 0건이라 확인할 수 없었다 | 스펙 |
| 정렬 | 카테고리만 요청 `sort{by, order}` 를 받는다. 응답도 `order` 순서였다. 상품 `order` 는 101건 전부 `1` 이라서 목록 순서가 무엇을 기준으로 정해지는지 **문서에 없음**. 옵션 · 구성에는 순서 칸이 없다(배열 순서뿐) | 확인 · 스펙 |
| 페이징 | **없다.** 10개 작업 모두 요청 스키마에 page · cursor · limit · offset 칸이 없다. 응답에도 `totalCount` · next 칸이 없다. 한 번에 전부 온다 | 스펙 · 확인 |

---

## 5. 우리 쪽과의 접점 — 일정 `productOptionConfiguration`

`getSchedulesByFlowStep` 을 `COMPLETED` · `PROCEDURE_WAITING` 두 단계로 불렀다(범위 2026-10-01 ~ 11-12 UTC). 일정 55건, 작업 141건이 나왔다. 그중 `productOptionConfiguration` 이 있는 작업은 93건이고, 나머지 48건은 `ETCETERA`(기타 작업)다. [문서](https://developers.kos-solution.com/docs/openapi/schedule#getSchedulesByFlowStep)

모양(확인 · 93건 모두 같은 키):

```text
productOptionConfiguration{
  optionId, optionTitle, productTitle,
  procedure{id, name, createDate, categoryIds[]},
  unit{type, value}, medicineAndMachines[],
  translsMap{optionTitle{translation{ko, ja, zh-Hans, zh-Hant, en}}}
}
```

| 대조 | 결과(확인) |
|---|---|
| `optionId` ∈ 메뉴 `options[].id` | **93/93** |
| `optionTitle` == 메뉴 옵션 `title` | 93/93(지금은 같다. 일정 쪽 값이 그 시점의 스냅샷인지 메뉴를 가리키는 값인지는 문서에 없음) |
| `productTitle` == 메뉴 상품 `title` | 41/93 같음. **52/93 빈 문자열**. 빈 52건은 모두 `ticketConfiguration` 이 있는 작업, 즉 시술권으로 잡힌 작업이다(52/52) |
| `procedure.id` ∈ `getProcedures` | 93/93 |
| `procedure.id` ∈ 그 옵션의 시술(SINGLE 은 `procedure`, GROUP 은 `compositions[].procedure`) | SINGLE 59/59 · GROUP 34/34 |
| GROUP 옵션 하나 → 작업 수 | 구성마다 작업이 따로 생긴다(16번 모두 「구성 2개 → 시술이 다른 작업 2개」) |
| `medicalServiceConfiguration.id` ∈ `getMedicalServices` | 93/93 |
| `productId` | **칸이 없다.** 상품으로 거슬러 가려면 `optionId` 로 메뉴를 찾아야 한다 |
| 예약 `requestedProcedures[].optionConfiguration` | 3건을 봤다. 2건은 `{optionId, optionTitle, optionType, productTitle, price, compositions, medicalService, translsMap}` 이고 `optionId` 가 메뉴에 있었다. 1건은 빈 객체였다 |

수납 `items[].optionConfiguration{id, …}`(앞 조사 §3.4)는 이번에 부르지 않았다. 메뉴 id 와 맞는지는 **미확인**이다.

---

## 6. 응답 크기 · 속도

데모, 2026-11-11, 각 작업 1회(KST 오후, 우리 쪽 맥에서 운영 호스트로). 시간은 요청부터 본문 수신 끝까지다.

| 작업 | 요청 | 바이트 | 건수 | 시간 |
|---|---|---:|---:|---:|
| `getCategories` | `{}` | 4,252 | 15 | 51ms |
| `getProducts` | `{}` | 588,465 | 101 상품 / 323 옵션 | 321ms |
| `getProducts` | `targetCountryCode: ETC` | 588,465 | 101 / 323 | 370ms |
| `getProduct` | `id` 1개 | 4,785 | 1 상품 / 2 옵션 | 62ms |
| `getProductOptions` | 옵션 4개 · promo true | 7,972 | 4 | 34ms |
| `getProductOptions` | 옵션 4개 · promo false | 7,972 | 4 | 37ms |
| `searchProductOptionSummaries` | `"a"` | 652,388 | 279 | 167ms |
| `searchProductOptionSummaries` | `""` | 746,467 | 323 | 172ms |
| `getProcedures` | `{}` | 49,676 | 804 | 75ms |
| `getMachines` | `{}` | 17,328 | 302 | 66ms |
| `getMedicines` | `{}` | 20,818 | 349 | 794ms(1회 측정이라 튄 값일 수 있음) |
| `getMedicalServices` | `{}` | 189,582 | 226 | 120ms |
| `getTargetCountries` | `{}` | 108 | 4 | 50ms |
| (참고) `getSchedulesByFlowStep` | 단계 1개 · 6주 | 132,329 / 228,732 | 17 / 38 일정 | 134 / 112ms |

- 메뉴 한 바퀴(카테고리 + 상품 + 시술 + 기기 + 약물 + 진료항목 + 국가)는 약 **870KB** 다. 검색 전체까지 더하면 약 **1.6MB** 다
- `getProducts` 의 바이트는 대부분 옵션 · 구성 안에 박힌 진료항목과 다국어 맵(5개 언어)이 차지한다(추정. 키 수로 봤고 따로 재지는 않음)
- **변경 알림**: Webhook `PRODUCT_CREATED` · `PRODUCT_UPDATED`(상품 정보나 **옵션** 수정) · `PRODUCT_DELETED` 가 `productId` 만 담아서 온다. 상세는 `getProduct` 로 다시 읽으라고 한다([Webhook 이벤트](https://developers.kos-solution.com/docs/guide/webhook/webhook-events.md)). 카테고리 · 시술 · 진료항목 · 기기 · 약물의 변경 이벤트는 그 문서에 **없다**
- 호출 한도(rate limit)는 **문서에 없음**

---

## 7. 스펙과 실제가 다른 곳(데모에서 확인)

| # | 스펙 | 실제 |
|---|---|---|
| 1 | SINGLE `medicalService` 필수 | `getProducts` · `getProduct` 에서 307/307 빠진다(`getProductOptions` · 검색에는 있다) |
| 2 | SINGLE 은 `compositions` 금지, GROUP 은 `medicineAndMachines` 금지 | 둘 다 빈 배열로 온다 |
| 3 | 옵션 `unit` 선택 칸 | SINGLE 0/307. 단위는 진료항목 `configuration.unit` 에 있다 |
| 4 | 검색 `productConfiguration`(새 칸) | 0/323. deprecated `productId` · `productTitle` · `productIsEvent` 만 온다 |
| 5 | `procedure.createDate` 필수 | 339/339 빈 문자열 |
| 6 | 가격 세부 금액 | 같은 옵션인데 작업에 따라 `0`·`""` 로 오기도 하고 키가 빠지기도 한다 |
| 7 | 가이드 `originalPrice` · `discountRate` | 메뉴 스키마에 없음 |
| 8 | 개념 문서 「상품에 여러 카테고리」 | 데모는 101/101 이 1개 |
| 9 | `getTargetCountries` | 같은 코드가 두 번씩(`order` 만 다름) |

---

## 8. 정할 것 (결정하지 않고 모음)

1. **노출 깊이** — 우리 API 가 어디까지 내줄지. (a) 상품 → 옵션까지만 줄지, (b) 구성 · 시술까지 줄지, (c) 진료항목(코드 · 과세 · 단위)과 기기/약물까지 줄지
2. **원천 작업** — `getProducts` 하나로 트리를 만들지, 아니면 SINGLE 의 진료항목이 필요해서 `searchProductOptionSummaries("")` 나 `getProductOptions` 를 함께 부를지. 가이드는 빈 검색어 호출을 권하지 않는다. 다른 길은 `getMedicalServices` 를 따로 받아 id 로 붙이는 것이다
3. **type 갈래 표현** — SINGLE · GROUP · CONSULTATION 을 하나의 모양으로 펼칠지(SINGLE = 구성 1개짜리 GROUP 처럼), 아니면 KOS 처럼 판별자로 나눠 둘지. CONSULTATION(데모 0건)을 받을지
4. **가격 칸 범위** — 정가만 줄지, 공급가 · 부가세 · 면세 · 과세 유형까지 줄지. `TAXABLE` 에서 「정가 = 공급가, 부가세 별도」로 보이는 값을 어떻게 해석할지(KOS 에 물을 것). `additional`(수가 유형별 특별가)과 deprecated 프로모션을 받을지
5. **다국어** — `translsMap` 을 그대로 넘길지, 언어 하나를 골라 펼칠지. 어느 언어 목록을 받을지(데모 5개, 가이드 예제는 6개)
6. **채널 · 국가 필터** — 키 하나 = 채널 하나인 구조라서, 우리 키의 채널에 걸린 메뉴만 보인다. 협업자가 원하는 것이 「지점 전체 메뉴」인지 「홈페이지 노출 메뉴」인지. `targetCountryCode` · `isEvent` · `categoryId` 를 우리 API 의 질의 칸으로 열지
7. **캐시** — 1시간 캐시 같은 시간 기반으로 할지, Webhook `PRODUCT_*` 로 무효화할지, 둘 다 할지. 카테고리 · 시술 · 진료항목은 Webhook 이 없다
8. **id 노출** — KOS ObjectId 를 그대로 우리 id 로 쓸지. 일정 `optionId` · `procedure.id` 와 바로 맞는다(§5)
9. **일정과 잇기** — 작업에 `productId` 가 없고, 시술권 작업은 `productTitle` 이 비어 있다. 이 빈칸을 메뉴로 채울지(채우면 「가공」이다. 추정해서 채우는 것은 아니다)
10. **목록 순서** — 상품 `order` 가 다 같은 값이라 순서 기준이 없다. KOS 가 준 배열 순서를 그대로 쓸지, 이름 · 카테고리 순으로 정렬할지
11. **기기/약물 구분** — `medicineAndMachines` 를 그대로 넘길지, 기기 · 약물로 갈라서 줄지(가르려면 목록 두 개를 대조해야 한다)
12. **스펙과 실제의 차이(§7)** — 스펙을 기준으로 받을지 실제 응답을 기준으로 받을지. 특히 「검색 `productConfiguration` 이 아직 안 옴」과 「상품 계열 응답에서 SINGLE 진료항목이 빠짐」

---

## 출처

- 스펙: https://developers.kos-solution.com/openapi.yaml (1.0.1, 2026-11-11 받음)
- 작업 문서: https://developers.kos-solution.com/docs/openapi/product (`#getCategories` · `#getProducts` · `#getProduct` · `#getProductOptions` · `#searchProductOptionSummaries` · `#getProcedures` · `#getMachines` · `#getMedicines` · `#getMedicalServices`) · https://developers.kos-solution.com/docs/openapi/targetcountry#getTargetCountries · https://developers.kos-solution.com/docs/openapi/schedule#getSchedulesByFlowStep
- 개념: https://developers.kos-solution.com/docs/openapi/product.md (「주요 개념」)
- 가이드: https://developers.kos-solution.com/docs/guide/procedure-menu/start-procedure-menu.md · https://developers.kos-solution.com/docs/guide/webhook/webhook-events.md
- 인증 · 오류: https://developers.kos-solution.com/docs/openapi/authorization
- 앞 조사: `reference/2026-10-12-cc-prototype/kos-demo-api.md` §1 · §2 E · §3.5
