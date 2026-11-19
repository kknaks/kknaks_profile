# 2단계 실물 발견 반영 (사용자 2026-11-19 「나머지 진행 · PR 까지」)

근거: `be-2-report.md` 「실물에서 찾은 것」. 아래는 모두 정해졌다. planner 는 spec 워크트리(`customer-erd-spec` · 브랜치 `kknaksss/customer-erd-sync` · PR #952)를, backend 는 코드 워크트리(`customer-erd`)를 맡는다. 커밋 · push · PR 은 금지다.

## 정한 것

| # | 무엇 | 반영 |
|---|---|---|
| F-1 | 카드 이력 `chargingId` 가 환불할 때 두 주머니 행에 같은 값으로 온다 | `prepaid_card_ledger` 외부 id = **`chargingId:주머니`**(`balance` · `point`) · 거래 연결은 원래 `chargingId` 로 한다(backend 구현 그대로). SPEC-000 표 · ㉔ 「`prepaid_card_ledger` = `chargingId`」 줄을 고친다 |
| F-2 | 묶음 구성 `compositions[].title` 이 실물에서 비어 온다(34/34) | `product_option_composition.title` 을 **nullable** 로 바꾼다. 다른 칸으로 추정해 채우지 않는다. 구성은 건너뛰지 말고 쓴다 |
| F-3 | 티켓 상태 `CANCELED` 가 실물에 있다(4장) | `ticket.status` enum 에 **`canceled`** 를 더한다(0010 · 매핑 표) |
| F-4 | 열린 구매의 담은 항목은 `pendingItems[]` 에 있다 | **받는다.** 같은 `purchase_item` 에 넣는다(`items[]` · `pendingItems[]` 둘 다 · 항목 상태 칸 없음 — 상태는 구매에). 확정되면 KOS 가 `pendingItems` → `items` 로 옮기므로 같은 항목 id 로 upsert 된다(id 가 바뀌면 사라짐 → 소프트 딜리트). 「수납 필요 = 열린 구매」 결정과 맞춘다 |
| F-5 | 닫힌 선불카드 상품이 응답에 없어 `deleted_at` 이 된다 | `get-prepaid-card-product` 를 `{closed:false}` · `{closed:true}` **두 번** 불러 합친다. `is_closed` 는 응답 값을 쓴다. ㉔ 요청 키를 고친다 |

## 그대로 둔다

- 가격 조정은 관계만 쓰고 칸은 미정이다(OQ-08-4). 「표본 1건 생김」만 OQ 에 적는다.
- 지난 구매의 시술권(출처 항목 없음)은 건너뛴다 — 백필 몫. OQ-00-3 메모에 한 줄 더한다.
- 시술 항목 `priceAmount` · `durationTime` · `recommendedInterval` 은 지금 결정(「KOS 원천 없음」)대로 둔다. 공개 openapi 에 있다는 사실만 OQ 에 적는다.

## 할 일

- **planner**:
  - SPEC-000(F-1 · F-2 · F-3 · F-4 문구 · 「2026-11-19 개정」 표시)
  - SPEC-002 ㉔(F-1 · F-4 원천 · F-5 요청 키 · 매핑 표 `CANCELED`)
  - OQ 를 갱신하고 lint 를 돌린다. `spec-sync-report.md` 에 한 줄 남긴다.
- **backend**:
  - 0010(F-2 nullable · F-3 enum)
  - mapper · sync(F-1 이미 구현했으면 확인 · F-4 · F-5)
  - 테스트(F-2 구성 쓰기 · F-3 · F-4 pending → items 전환 · F-5 닫힌 상품)
  - **DEMO 실물을 다시 확인**한다(같은 방식 · 테스트 계정 · DEMO 테넌트만 · 세션 해제). 구성 34 · 닫힌 상품 · 열린 구매 항목 건수 · 판 해시 같음.
  - `be-2-report.md` 끝에 「실물 발견 반영」 절을 단다.
- 끝나면 각자 아래 명령으로 알린다:

  ```bash
  orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[worker_done] <planner|backend> 실물 발견 반영 완료 — <한 줄>" --enter
  ```
