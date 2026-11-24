# 조사: 원내 현황 카드 금액(수납총액 · 결제총액 · 미수총액) · 상담 실장

읽기 전용이다. 코드 · 문서 · DB는 고치지 않았고 KOS는 부르지 않았다. DB에는 `default_transaction_read_only=on`을 건 SELECT만 썼다. 고객 이름 · 전화 · 메모는 적지 않았다.

## 답 한 줄씩

| # | 물음 | 답 | 한 줄 |
|---|---|---|---|
| 1 | KOS 원천 | **가공** | 수납 요약(`get-purchase-summaries`)에 합계 칸은 없다. 재료만 있다: 항목 `priceV2`(최종가) · `adjustPriceV2`(환불 뒤) · 거래 `price`(부호 있음). 구매 단위다. 방문과는 일정의 `purchaseIds[]`로 묶인다. |
| 2 | DAY DB 저장 | **가공** (재료는 다 있음) | `purchase.visit_id` → `purchase_item.price_amount` / `adjusted_amount`, `purchase_transaction.amount`(부호). 합계 칸은 일부러 두지 않았다(모델 docstring). |
| 3 | 「이번 방문」 경계 | **가공** (원천 필드로 가름) | 구매는 `purchase.visit_id`(KOS 일정 `purchaseIds`)로 이 방문에 붙는다. 다른 날 구매는 다른 visit에 붙어 빠진다. 시술권 쓰기는 구매가 없어 0원이다. 환불은 `adjusted_amount`, 취소는 음수 거래로 가른다. 할인은 이미 `priceV2`에 들어 있다. 다른 날 미수를 오늘 내는 경우의 거래 위치는 **확인 못 함**. |
| 4 | cc-prototype · centurion | cc = **가공** · centurion = **없음** | cc: 전체 = `items[].priceV2.amount` 합, 결제 = `APPROVED` ∧ `canceledRefId` 없음 거래 합. KOS를 직접 불렀고 `pendingItems` · 환불 조정은 안 셌다. centurion에 같은 계산은 없다. |
| 5 | 상담 실장 | **그대로** | 첫째 `consultation.counselor_id`(KOS `consultations[].counselors`, 시술 현황판이 쓰는 원천)다. 비면 `visit.consultation_info_counselor_id`다. `visit_task_staff`에는 상담 역할이 없다. |
| 6 | 데모 DB 표본 | 계산함 | 오늘 방문 10건 중 구매 있는 6건은 수납총액 = 결제총액, 미수 0이다. `588bfeb2`는 수납필요 작업이 2줄인데 금액은 0이다(아래 ⚠). |
| 7 | 빠진 것 | **있음** | ① 아직 구매에 안 들어간 수납필요 작업의 금액이 없다(KOS 작업에 판매가가 없음). ② 거래 상태 `SPENT` · `REQUESTED` · `FAILED`, 수단 `PLATFORM` · `EASY_PAY` · `MEDICAL_LOAN` 행은 매핑에서 빠진다. ③ 구매 단위 가격 조정의 값 · 상태(`PENDING`)를 저장하지 않는다. |

계산식 제안(지어낸 규칙 없이 원천 칸만 쓴 것):

```
수납총액 = Σ coalesce(purchase_item.adjusted_amount, purchase_item.price_amount)
결제총액 = Σ purchase_transaction.amount
미수총액 = 수납총액 − 결제총액
```

- 합산 범위: `purchase.visit_id = 이 방문`이고 purchase · item · transaction 모두 `deleted_at IS NULL`인 행.
- 결제총액은 부호 있는 합이라 취소가 이미 빠져 있다.

---

## 1. KOS 원천

**API**는 `purchase/v1/queries/get-purchase-summaries`다(DAY 내부 경로 `backend/day/emr/kos/sale_reads.py:60`). 공개판 경로는 `purchase/open/v1/queries/get-purchase-summaries`이고 문서는 `ax-clinic-project/para/archive/inbox_archive/2026-09-18-kos-openapi.yaml:1246`에 있다. 입력은 `purchaseIds[]`다.

**응답 `PurchaseSummary`**: 합계 · 미수 칸이 없다(openapi `protos.purchase.PurchaseSummary` 속성 전부 확인). 있는 칸은 다음과 같다.
- `items[]` · `pendingItems[]`(추가 대기 항목)
  - `priceV2` = **최종 가격**
  - `basePrice` = 가격 조정 기준 가격
  - `adjustPriceV2` = **조정 후 최종 가격**(환불)
  - `priceAdjustments[]`
- `transactions[]`
  - `price` = 거래 금액
  - `status`: `REQUESTED` · `APPROVED` · `CANCELED`(= 취소 **거래**, 음수) · `SPENT`(취소 없이 돌려준 음수 거래) · `FAILED`
  - `canceledRefId`
  - `paymentType`(7종)
- `priceAdjustments[]`(수납 단위)
  - `PENDING` 분배 대기 · `DISTRIBUTED` 분배됨
- `refundingItems[]`
- `status`: `INITIALIZED` 미수납 · `ACCEPTED` 수납 완료 · `PAID` · `REFUNDED` · `PARTIALLY_REFUNDED`
- `process`

**방문과의 묶음**: 구매 자체는 `visitorId`(고객)만 갖는다. 방문 하나에 묶는 것은 **일정(schedule)의 `purchaseIds[]`**다(`emr/kos/mapper_purchase.py:93-109` `schedule_sale`). 일정 작업에도 `purchaseId`가 있다(openapi :22152). 다만 DAY는 이 값을 작업 행에 저장하지 않는다.

**작업 줄 가격**: KOS 일정 작업 `procedureConfiguration`에 판매가가 없다. 있는 것은 `medicalServiceConfiguration.priceAmount` 「원가」뿐이다(openapi `FlowTaskProcedureConfiguration`). 이 값은 받을 돈이 아니다. `paymentRequired`는 불린뿐이다(openapi :22149 · DAY `emr/kos/mapper.py:471`).

판정: **가공**. 세 값 모두 항목 · 거래를 더해 만들어야 한다.

## 2. DAY DB 저장

모델은 `backend/day/models/purchase.py`다. docstring L1-5에 「결제 합계 칸은 두지 않는다(거래 합계로 계산)」라고 적혀 있다.

| 칸 | 원천 | 위치 |
|---|---|---|
| `purchase.visit_id` (필수) | 일정 `purchaseIds` → 그 일정의 방문. 없으면 이미 DAY에 있는 구매의 방문. 그래도 없으면 건너뜀(OQ-69) | `models/purchase.py:63` · `emr/sync_purchases.py:111-122` |
| `purchase.status` · `process` | KOS 그대로 | `:64-65` |
| `purchase_item.price_amount` | `priceV2.amount`(최종가) | `models/purchase.py:96` · `mapper_purchase.py:149` |
| `purchase_item.adjusted_amount` | `adjustPriceV2.amount`. 「환불 때만 · 환불 뒤 남는 금액」 | `models/purchase.py:101-102` · `mapper_purchase.py:155` |
| `items` + `pendingItems` | 같은 `purchase_item`에 합침(같은 id면 `items` 쪽) | `mapper_purchase.py:210-216` |
| `purchase_transaction.amount` | 부호 있는 금액(승인 + · 취소 −), `canceled_transaction_id` = `canceledRefId` | `models/purchase.py:166-174` · `mapper_purchase.py:173-181` |
| `purchase_transaction.payment_type` · `prepaid_card_id` | 수단 · 선불카드 | `:175-180` |
| `purchase_price_adjustment` | **관계 칸만**(값 · 상태 없음, OQ-08-4) | `models/purchase.py:155-163` |
| `visit_task.payment_required` | KOS 작업 `paymentRequired` | `models/task.py`(VisitTask) · `mapper.py:471` |

`visit_task`에는 가격 칸이 없다. 시술권(`ticket`) · 선불카드(`prepaid_card`)는 고객 단위 잔액 · 회차 표다. 방문 금액에 들어가는 길은 구매 항목(`item_type`)과 거래(`payment_type = prepaid_card`)뿐이다.

판정: **가공**(재료 있음 · 합계 없음).

## 3. 「이번 방문」 경계 (원천 필드로 가를 수 있는 것만)

- **같은 고객의 다른 날 구매**: KOS 일정 `purchaseIds`가 다른 일정을 가리킨다. 그래서 `purchase.visit_id`가 다르고, `visit_id = 이 방문`으로 빠진다. 데모 표본 실례: 오늘 고객의 11-18 `partially_refunded` · 11-19 `initialized`(1,500,000 · 미결제) 구매가 각자 그날 방문에 붙어 있다. 고객 · 방문 고객 불일치는 0건이다.
- **선결제 시술권 쓰기**: 작업에 `ticket_id`만 있고 이번 방문 구매가 없다 → 0원(필드로 가름). 시술권을 **사는** 구매는 그 구매가 붙은 방문에 들어간다.
- **선불카드**:
  - 카드를 **사는** 항목은 `item_type = prepaid_card_product`, `price_amount`가 받을 돈이다.
  - 카드 잔액으로 **내는** 것은 거래 `payment_type = prepaid_card`다.
  - 결제총액에 카드 결제를 넣을지는 제품 결정이다(필드로는 가를 수 있음).
- **환불**: `adjusted_amount`(환불 뒤 남는 값). 표본에서 부분 환불 2건 모두 Σadjusted = Σ거래였다(아래 표). 그래서 총액은 `coalesce(adjusted, price)`가 맞다.
- **취소**: 음수 거래 행이 따로 온다. Σamount면 자동으로 빠진다.
  - cc-prototype처럼 「`APPROVED` ∧ `canceledRefId` 없음」으로 세면 원거래가 남는다. 그 경우 취소분을 빼지 못할 수 있다(원거래에 `canceledRefId`가 붙는지는 표본으로 확인 못 함).
- **할인**: `priceV2` = 최종가(할인 반영). 할인액 표시(시안 「할인 금액」)에 필요한 `basePrice`는 저장하지 않는다. 다만 세 값에는 필요 없다.
- **확인 못 함**:
  - 다른 날 미수를 오늘 낼 때 거래가 옛 구매(옛 방문)에 붙는지, 새 구매가 생기는지. KOS 흐름 문서에 「미수납 → 강제 귀가 가능, 다음 내원 때 수납」(`ax-clinic-project/scripts/kos_flow/build_kos_flow.py:175`)만 있다.
  - 수납 단위 가격 조정이 `PENDING`(분배 전)일 때 항목 `priceV2`에 이미 반영됐는지.

## 4. cc-prototype · centurion

- cc-prototype `procedure/back/app/domain/reservation_rules.py:218-233` `purchase_amount`:
  - 전체 = `items[].priceV2.amount.value` 합
  - 결제 = `status == "APPROVED"` ∧ `canceledRefId` 없음인 거래 `price.value` 합
  - 방문 합은 `sum_amounts` → 예약 `purchase_ids` 묶음(`service/reservations.py:391`)
  - KOS를 직접 불러 메모리 캐시에 뒀다(`kos/reservation_sync.py:360-372` — 오늘 원내 일정의 `purchase_ids`)
  - `pendingItems` · `adjustPriceV2`(환불)는 세지 않았다
- 화면 `procedure/front/components/reservations/ResvAside.tsx:285-289`: 「전체」 = total, 「결제」 = paid, 「수납 필요」 = **건수**(`paymentRequiredCount` = 수납필요 작업 수, `reservation_rules.py:202`). 남은 **금액**은 표시하지 않았다.
- centurion(`/Users/kknaks/git/centurion`): KOS 수납 합계 계산은 **없음**. 비슷한 말은 `backend/linky` 구독 청구(`paid_amount`)뿐이고 무관하다.

## 5. 상담 실장

| 칸 | KOS 원천 | 뜻 | 위치 |
|---|---|---|---|
| `consultation.counselor_id` | 일정 `consultations[].counselors` (첫 1명 — `single`) | 실제 상담한 직원. 시술 현황판이 쓴다 | `emr/kos/mapper.py:497-507` · `queries/board.py:60-75`(상담 시작 순) |
| `visit.consultation_info_counselor_id` | 일정 `consultation.counselor` | 일정에 붙은 상담 정보 | `mapper_kos_keys.py:288-291` · `models/visit.py:115-117` |
| `visit.requested_counselor_id` | `reservation.counselor` | 예약 때 지정 · 희망 상담사 | `mapper.py:572-573` · `models/visit.py:91` |
| `customer.assigned_counselor_id` | 고객 `counselor` | 고객 담당(방문 아님) | `mapper_kos_keys.py:455` |

`visit_task_staff.role`은 `assignee` · `doctor` · `called_doctor`뿐이다(`enums/task.py:27-30`). 상담 역할은 **없다**.

cc-prototype 외부 상세도 「`consultations[].counselors[]` · 비면 `consultation.counselor`」 순이었다(`service/ext.py:576-587`). DAY에서는 `consultation.counselor_id` → `visit.consultation_info_counselor_id` 순이 같은 뜻이다.

데모 DB에서 오늘 방문 10건은 상담 행 0 · 두 칸 모두 비어 있다. 전체로는 상담 12건 중 8건에 상담사가 있다. 오늘 표본으로는 표시를 확인할 수 없다.

## 6. 데모 DB 표본 (오늘 · 2026-11-23 KST · `day_dev`)

오늘 방문 10건의 단계는 상담 대기 4 · 시술 대기 5 · 귀가 대기 1이다. 오늘 방문의 구매는 `accepted` 27건과 지운 `initialized` 1건이다. 거래는 `approved` · `cash` 27건, 합계 5,972,000이다.

계산 규칙은 §요약 식 그대로다.

| 방문 | 단계 | 수납총액 | 결제총액 | 미수총액 | 항목 · 거래 | 수납필요 작업 |
|---|---|---:|---:|---:|---|---:|
| bfe4f955 | 시술 대기 | 1,111,000 | 1,111,000 | 0 | 5 · 5 | 0 |
| 36a4d470 | 시술 대기 | 517,000 | 517,000 | 0 | 4 · 4 | 0 |
| 2c2a878c | 시술 대기 | 847,000 | 847,000 | 0 | 6 · 6 | 0 |
| f019f6c1 | 시술 대기 | 990,000 | 990,000 | 0 | 5 · 5 | 0 |
| 47c39572 | 시술 대기 | 1,507,000 | 1,507,000 | 0 | 6 · 6 | 0 |
| 588bfeb2 | 귀가 대기 | 1,000,000 | 1,000,000 | 0 | 1 · 1 | **2** |
| a1542ae1 · d637ff29 · 5a3f2f01 · 2ae3d92d | 상담 대기 | 0 | 0 | 0 | 구매 없음 | 0 |

⚠ **`588bfeb2`**: 작업 2줄(상품 옵션, 시술권 아님)이 `payment_required = true`인데 살아 있는 구매는 다 결제됐다. 지운 `initialized` · `pending` 구매 1건은 항목 1 · 0원이다. R42로는 「수납 필요」 배지가 뜨지만 금액 미수는 0이다. 이 2줄의 금액은 DAY에 없다. KOS 화면에서 이 방문의 「수납 필요」 금액과 대조할 1순위다.

환불 대조(전체 DB):

| 구매 | 상태 | Σprice | Σcoalesce(adjusted, price) | Σ거래 |
|---|---|---:|---:|---:|
| 8df23950 | partially_refunded | 328,900 | 65,780 | 65,780 |
| d03789d9 | partially_refunded | 500,000 | 440,000 | 440,000 |
| 72515d78 | refunded | 500,000 | 0 | 0 |
| ca6bde1a | refunded | 110,000 | 0 | 0 |

→ 환불 구매는 `coalesce(adjusted, price)`로 미수 0이 된다. `price_amount`만 쓰면 미수가 거짓으로 생긴다.

그 밖의 전체 DB 값:
- 거래: `canceled` 10행(음수, 최소 −30,000,000), `prepaid_card` 결제 4 · 취소 1, `transfer` 1.
- 항목 종류: `product_option` 295 · `prepaid_card_product` 9 · `etcetera_product` 2.
- `initialized` 구매 16건 중 살아 있는 4건(550,000 · 550,000 · 1,500,000 · 550,000)은 거래가 0이다.

## 7. 빠진 것 (동기화를 더 받아야 할 것)

1. **구매 전 수납필요 작업의 금액**: KOS 일정 작업에 판매가가 없다(원가 `priceAmount`뿐). 금액은 KOS가 그 작업을 수납 항목(`pendingItems` / `items`)으로 만든 뒤에만 `get-purchase-summaries`로 온다. 따라서 「미수 = 수납필요 작업 금액」은 지금 원천으로는 **없음**이다.
   - 메뉴 정가(`product_option` 가격)로 채우면 추정이 되므로 하지 말 것.
   - 일정 작업의 `purchaseId`(openapi :22152)를 저장하면 「어느 작업이 어느 구매에 들었나」는 알 수 있다. 지금은 저장 안 함.
2. **거래 상태 · 수단 빠짐**:
   - `TRANSACTION_STATUSES` = `APPROVED` · `CANCELED`만 있다(`emr/kos/mapper_sale_values.py:43-46`). `SPENT`(돌려준 음수) · `REQUESTED` · `FAILED`는 매핑 오류로 그 거래 행이 빠진다.
   - `PAYMENT_TYPES` = 카드 · 현금 · 선불카드 · 이체만 있다(`:50-55`). `PLATFORM` · `EASY_PAY` · `MEDICAL_LOAN` 결제도 빠진다.
   - 그러면 결제총액이 실제와 달라진다(SPENT 누락 = 많게, 앱 · 간편 · 의료론 누락 = 적게).
   - 표본에는 이런 값이 0건이라 지금 데모 숫자에는 영향이 없다. 같은 API(`get-purchase-summaries`)에서 매핑만 넓히면 된다(OQ-08-5 · OQ-4A-1 표본 필요).
3. **수납 단위 가격 조정**: `purchase_price_adjustment`는 관계만 있다. `priceAdjustment.value` · `method` · `status`(`PENDING` / `DISTRIBUTED`)는 저장하지 않는다. `PENDING` 조정이 항목 `priceV2`에 반영되기 전이라면 총액이 다를 수 있다. 표본으로는 확인 못 함(데모에 조정 행 7건, 구매 7건).
4. 시안 「할인 금액」을 보이려면 `basePrice`도 필요하다(지금 미저장). 세 값에는 필요 없다.

## 코디가 정할 것
- 결제총액에 선불카드 잔액 결제(`payment_type = prepaid_card`)를 넣는가(제품 결정 · 필드로는 가름).
- `588bfeb2` 사례처럼 「수납필요 작업은 있는데 금액 미수 0」일 때 카드에 무엇을 보이나(배지는 R42, 금액은 0 / 없음).
- 거래 매핑 확대(빠진 것 2)를 이 피처에 넣을지.
