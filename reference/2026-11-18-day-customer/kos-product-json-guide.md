# KOS 상품 구조 → JSON 정리 가이드 (실제 병원 · 읽기만)

2026-11-19 · 근거: `orchestration/work/customer-erd/kos-sync-research-report.md`(데모 지점 실호출) · DAY-SPEC-000 §4 04-1(mediness #951)

KOS 한 병원의 **상품 구조**(카테고리 · 상품 · 옵션 · 가격 · 묶음 구성 · 시술 항목 · 시술 · 약품 · 기기 · 시술 외 품목 · 선불카드 상품 · 기타 작업)를 읽어서 아래 「출력 JSON」 모양 하나로 정리한다.

---

## 0. 지킬 것

- **읽기만 한다.** 조회(`…/queries/…`)와 로그인(`sign-in`)만 호출한다. 생성 · 수정 · 삭제 · 결제 같은 `…/commands/…`는 부르지 않는다. 예외는 §2-4 「기기 제한 해제」 하나다.
- **계정은 테스트 계정만 쓴다.** 아이디와 비밀번호는 따로 전달받는다.
  - 이 문서 · 코드 · 출력 파일 · 로그 · 화면 캡처 어디에도 쓰지 않는다. 실행할 때 환경변수로만 읽는다(`KOS_TEST_EMAIL` · `KOS_TEST_PASSWORD`).
- **상품 구조만 읽는다.** 고객 · 일정 · 구매 · 시술권 · 선불카드 잔액 · 처방 · 직원 API는 부르지 않는다.
  - 실제 병원이라 그쪽에는 개인정보가 있다. 이 작업에 필요 없다.
- **토큰과 테넌트 id는 출력하지 않는다.** 콘솔과 로그에도 찍지 않는다.
- 호출 사이에 0.3초 이상 쉰다. 로그인은 한 번만 하고 토큰을 재사용한다(로그인할 때마다 기기 자리를 하나씩 먹는다).
- 결과 JSON은 **레포에 커밋하지 않는다**(프로필 레포는 공개다). 전달받은 곳으로만 보낸다.

## 1. 주소 · 헤더

| 무엇 | 값 |
|---|---|
| 내부 API 베이스 | `https://api.kos-solution.com` |
| KOS 웹 | `https://app.kos-solution.com` |
| 방식 | 모두 `POST` · 본문 JSON · 응답 `{ "data": … }` |

내부 API는 **브라우저 헤더가 없으면 매 요청 403**(`Unsupported client.`)이 난다. 모든 요청에 아래 헤더를 싣는다.

```text
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 (product-json)
Origin: https://app.kos-solution.com
kos-client-uri: https://app.kos-solution.com/<tenantId>/reservation/schedule/
Content-Type: application/json
Authorization: Bearer <token>        ← sign-in 뒤부터
```

- UA 끝의 ` (product-json)`은 이 작업의 세션 표시다. §2-4 에서 내 세션만 골라 해제할 때 쓴다.
- `kos-client-uri` 는 KOS 웹처럼 단계마다 다르다(DAY `staff_client.py` 와 같음):
  - sign-in = `https://app.kos-solution.com/auth/sign-in`
  - 테넌트 목록 = `https://app.kos-solution.com/hospital/select`
  - 그 뒤 테넌트 요청 = 위 `…/<tenantId>/reservation/schedule/`

## 2. 로그인 · 병원 고르기

1. **sign-in** — `POST /common/v1/user/commands/sign-in` `{ "email", "password" }`
   - 응답 `data.token` 을 토큰으로 쓴다. `tokenExpiredDateTimeUtc` 전까지 재사용한다.
2. **테넌트 목록** — `POST /common/v1/tenant/queries/get-user-tenants` `{}`
   - 응답 `data[]` 는 `{ id, hospitalName, … }` 이다. 테스트 계정은 테넌트가 2개다(데모 지점 + 실제 병원). **읽을 병원의 `hospitalName` 으로 골라** 그 `id` 를 `tenantId` 로 쓴다.
   - 이름이 헷갈리면 멈추고 묻는다.
3. 이후 모든 요청은 `https://api.kos-solution.com/tenants/<tenantId>/<경로>` 로 보낸다.
4. **기기 제한(동시 로그인 5개)**
   - sign-in 이 401 이고 본문 `message` 가 `SignInLimitExceeded` 면 자리가 다 찬 것이다.
   - `POST /common/user/v1/queries/get-active-sign-ins` `{ "email", "password" }` 로 목록을 받는다.
   - **UA 끝이 ` (product-json)` 인 내 세션만** 가장 오래된 것 하나를 `POST /common/user/v1/commands/revoke-active-sign-in` `{ "email", "password", "signInId" }` 로 해제한다. 그다음 sign-in 을 한 번 더 한다.
   - 이때 헤더 `kos-client-uri` 는 `https://app.kos-solution.com/auth/active-sign-in-limit` 이다.
   - 내 표시가 없는 세션(사람 · DAY 서버)은 **해제하지 않는다.** 멈추고 묻는다.
5. 끝나면 내 세션을 4의 방법으로 해제해 자리를 돌려준다.

## 3. 부를 API (테넌트 경로 · 전부 조회)

| # | 무엇 | 경로 (`/tenants/<tenantId>/` 뒤) | 본문 | 데모 건수 |
|---|---|---|---|---|
| A | 상품 카테고리 | `procedure-menu/categories/queries/get-categories` | `{"sort":{"by":"order","order":"ASC"}}` | 15 |
| B | **상품 · 옵션 · 가격 · 묶음 구성 · 시술 항목** | `procedure-menu/products/queries/get-products` | `{"deleted":false,"includePromotions":false}` | 상품 103 · 옵션 326 |
| C | 시술(이름 목록) | `procedure-menu/v2/queries/get-procedures` | `{"deleted":false}` | 804 |
| D | 시술 외 품목(+ 분류) | `procedure-menu/etcetera-products/v1/queries/get-etcetera-products` | `{"deleted":false}` | 11 |
| E | 선불카드 상품 | `procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product` | `{"closed":false}` | 8 |
| F | 기타 작업 종류(방 배정 등) | `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks` | `{}` | 10 |

- **B 하나가 핵심이다.**
  - 상품 → `options[]` → 옵션마다 가격 · 수가 유형별 가격(`price.additional[]`) · 묶음 구성(`compositions[]`) · **시술 항목(`medicalService`)**이 한 번에 온다.
  - 시술 항목 안에 시술(`procedure`) · 약품(`medicines[]`) · 기기(`machines[]`) · 단위(`unit`)가 있다.
- 시술 항목 · 약품 · 기기를 따로 부르는 내부 경로는 없다. 예전 `common/medicine-and-machines/v2/…` 는 지금 404 다.
  - 그래서 **옵션 안의 `medicalService` 에서 모은다**(같은 `id` 는 하나로).
- 닫힌(판매 중지) 것도 보려면 B 에 `"closed"` 를 넣지 않는다(위 본문 그대로면 닫힌 것도 온다). E 는 `{"closed":false}` 와 `{"closed":true}` 를 둘 다 부른다.

### B 응답에서 쓰는 키 (데모 실측)

```text
data[] (상품)
  id · title · order · closed · deleted · isEvent · caution · targetCountryCodes[]
  categories[] { id · name }
  options[] (옵션)
    id · title · type(SINGLE | GROUP) · count(회차 — 5회권 = 5) · closed · deleted · displayChannels[]
    price { amount{value,currency} · suppliedAmount · taxFreeAmount · vatAmount · taxation
            additional[] { visitorType · amount … } }       ← 수가 유형별 가격
    medicalService                                           ← SINGLE 옵션의 시술 항목(내부 응답에만)
      id · title · status · draftedDateTimeUtc · updatedDateTimeUtc · caution
      configuration { code · healthcareReimbursement · taxation
                      unit { type · value }                  ← 단위(없는 항목도 있음)
                      procedure { id · name }
                      medicines[] { id · name } · machines[] { id · name } }
    compositions[] (GROUP 옵션의 구성 — 묶음)
      title · count · unit · price · procedure · medicalService · medicineAndMachines[]
```

알아 둘 것 (데모 실측):
- **옵션 자체에는 `unit` 이 없다.** 단위는 `medicalService.configuration.unit` 에만 있다.
- **묶음 구성에는 `id` 가 없고, 「어느 단품 옵션을 가리키는지」 키도 없다.** 구성 안의 값을 그대로 옮긴다.
- **시술 항목에는 가격 · 시술 시간 · 권장 간격이 없다.** 가격은 옵션에 있다.

## 4. 출력 JSON

파일 하나. 이름은 DAY 테이블 이름(DAY-SPEC-000)을 따르고, KOS 원래 id 는 `kos_id` 로 남긴다. 값은 아래 예시처럼 **응답에 있는 것만** 넣는다. 응답에 없으면 `null` 이다. 추정해서 채우지 않는다.

```json
{
  "meta": {
    "source": "KOS internal API",
    "hospital_name": "<병원 이름>",
    "fetched_at": "2026-11-19T00:00:00Z",
    "counts": { "categories": 0, "products": 0, "options": 0, "treatment_items": 0,
                "treatments": 0, "medicines": 0, "machines": 0,
                "etcetera_products": 0, "prepaid_card_products": 0, "etc_task_types": 0 }
  },
  "product_categories": [
    { "kos_id": "…", "name": "보톡스", "order": 0, "opened": true, "deleted": false }
  ],
  "products": [
    {
      "kos_id": "…", "title": "…", "order": 0, "closed": false, "deleted": false, "is_event": false,
      "category_kos_ids": ["…"],
      "options": [
        {
          "kos_id": "…", "title": "…", "type": "single", "count": 5, "closed": false, "deleted": false,
          "price": { "amount": 328900, "supplied_amount": 299000, "tax_free_amount": 0,
                     "vat_amount": 29900, "taxation": "TAXABLE" },
          "additional_prices": [ { "visitor_type": "…", "amount": 0 } ],
          "treatment_item_kos_id": "…",
          "compositions": []
        },
        {
          "kos_id": "…", "title": "울쎄라 + 써마지", "type": "group", "count": 1,
          "price": { "amount": 165000, "supplied_amount": null, "tax_free_amount": null,
                     "vat_amount": null, "taxation": null },
          "additional_prices": [],
          "treatment_item_kos_id": null,
          "compositions": [
            { "title": "…", "count": 1, "unit": { "type": "SHOT", "value": 100 },
              "price": 73333, "treatment_item_kos_id": "…", "treatment_kos_id": "…" }
          ]
        }
      ]
    }
  ],
  "treatment_items": [
    {
      "kos_id": "…", "title": "…", "code": "…", "status": "…",
      "unit": { "type": "CC", "value": 1 },
      "taxation": "TAXABLE", "healthcare_reimbursement": "…",
      "treatment_kos_id": "…",
      "medicine_kos_ids": ["…"], "machine_kos_ids": ["…"],
      "updated_at": "…"
    }
  ],
  "treatments": [ { "kos_id": "…", "name": "…", "deleted": false } ],
  "medicines":  [ { "kos_id": "…", "name": "…" } ],
  "machines":   [ { "kos_id": "…", "name": "…" } ],
  "etcetera_product_categories": [ { "kos_id": "…", "name": "약 처방", "order": 0, "closed": false } ],
  "etcetera_products": [ { "kos_id": "…", "title": "진단서 발급", "price": 10000, "category_kos_id": "…" } ],
  "prepaid_card_products": [
    { "kos_id": "…", "title": "…", "price": 500000, "charge_balance": 500000, "charge_point": 50000,
      "expiration_days": 365, "order": 0, "closed": false, "description": "…" }
  ],
  "etc_task_types": [ { "kos_id": "…", "title": "방 배정", "deleted": false } ]
}
```

만드는 규칙:
- `products[].options[].treatment_item_kos_id` 는 옵션의 `medicalService.id` 다. `treatment_items[]` 는 그 `medicalService` 들을 id 로 모아 중복을 뺀 것이다.
- `medicines` · `machines` 는 시술 항목 `configuration.medicines[] · machines[]` 를 id 로 모은 것이다.
  - 구성 안의 `medicineAndMachines[]` 도 합친다(이름만 있고 id 가 없으면 `kos_id: null`).
- `treatments` 는 C 의 목록 전체다. 시술 항목이 가리키지 않는 시술도 넣는다.
- `type` · `taxation` · `unit.type` 의 값은 KOS 값 그대로 둔다(`type` 만 소문자).
- 이름 · 가격 · 순서는 응답 그대로 옮긴다. 정렬은 `order` → `title`.

## 5. 끝나고 확인

- `meta.counts` 가 각 응답 건수와 맞는다.
- 옵션 중 `type: single` 인데 `treatment_item_kos_id` 가 `null` 인 수를 따로 센다. 데모는 0 이었다.
- JSON 안에 고객 · 직원 이름, 전화번호, 토큰, 계정 값이 없다(메뉴 이름 · 가격만).
- 내 KOS 세션을 해제했다(§2-5).
