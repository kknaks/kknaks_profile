# 메뉴 키 보강 + 유일 제약 1개 (사용자 2026-11-19 「응」)

근거: 코디가 HAR 의 KOS 메뉴 응답 키와 0010 모델 칸을 테이블별로 대조했다(`reference/2026-11-18-day-customer/har/*.har` · `backend/day/models/menu.py`). 아래 키만 빠져 있었다. 모든 칸은 nullable 이다. 메뉴 테이블은 prod 에 없어서(0010 새 테이블) 운영 영향이 없다.

## 더할 칸

| 테이블 | 칸 | 타입 | KOS 키 | 설명 |
|---|---|---|---|---|
| `treatment` | `search_phonetic_name` | varchar | `searchPhoneticName` | 초성 검색어 |
| `treatment` | `registered_at` | timestamptz | `createDate` | KOS 에 등록된 시각(DAY `created_at` 과 다름) |
| `medicine` | `search_phonetic_name` | varchar | `searchPhoneticName` | 초성 검색어 |
| `machine` | `search_phonetic_name` | varchar | `searchPhoneticName` | 초성 검색어 |
| `product` | `cautions` | text[] | `cautions[]` | 주의사항 목록(`caution` 한 칸은 그대로 둔다) |
| `product` | `target_country_codes` | varchar[] | `targetCountryCodes` | 노출 국가 |
| `product` | `medicine_and_machine_names` | varchar[] | `medicineAndMachines[].name` | 표시용 약품 · 기기 이름 스냅샷 |
| `product_option` | `medicine_and_machine_names` | varchar[] | `medicineAndMachines[].name` | 같음 |
| `product_option_composition` | `medicine_and_machine_names` | varchar[] | `medicineAndMachines[].name` | 같음 |
| `treatment_item` | `drafted_at` | timestamptz | `draftedDateTimeUtc` | 작성 시각 |
| `prepaid_card_product` | `translations` | jsonb | `translsMap` | 번역(다른 메뉴 테이블의 `translations` 와 같은 모양) |

- `treatment.categoryIds` 는 **넣지 않는다**. 804건 모두 비었고 카테고리 목록도 0건이다. OQ 로만 남긴다.
- 칸 이름 · 배열 타입은 기존 관례(`badges` · `display_channels` · `visit_task.medicines` 등)와 다르면 그 관례를 따른다. 바꿨으면 리포트에 적는다.

## 유일 제약 1개 (코드 검수 §5 권고)

- `ticket_bundle.purchase_item_id` 에 부분 유일(`WHERE deleted_at IS NULL`)을 건다.
- 나머지 셋은 **걸지 않는다**: `prepaid_card.purchase_item_id` · `visit_task.ticket_id` · `prepaid_card_ledger.purchase_transaction_id`. 이유는 `review-code-1-report.md` §5 — 동기화가 막혀 현황판이 멈출 위험이다.
- 2단계 upsert 는 「옛 번들 삭제 표시 → 새 번들 생성」 순서로 고정한다. 이 순서는 SPEC 에 한 줄로 적는다.

## 누가 무엇을

- **planner**(spec 워크트리 `customer-erd-spec` · 브랜치 `kknaksss/customer-erd-sync` · PR #952):
  - SPEC-000 §4 칸 표에 위 칸을 「2026-11-19 추가」로 넣는다. 외부(KOS) 열을 채운다.
  - `ticket_bundle` 표에 유일 제약을 적는다.
  - OQ: 시술 카테고리 · 남은 1:0..1 셋.
  - SPEC-002 ㉔ upsert 절에 번들 순서를 한 줄 넣는다.
  - `erd.md` 인벤토리 핵심 키가 바뀌면 맞춘다.
  - lint 를 돌린다. 리포트 `spec-sync-report.md` 에 한 줄 남긴다.
- **backend**(코드 워크트리 `customer-erd`):
  - 0010 마이그레이션과 모델에 위 칸 · 유일 제약을 넣는다(새 파일 만들지 말고 0010 을 고친다 — 아직 아무 데도 적용되지 않았다).
  - 칸 스냅샷 테스트를 갱신하고, 마이그레이션 왕복과 alembic check 를 돌린다.
  - 리포트 `be-1-report.md` 끝에 「보강」 절을 단다.
- 커밋 · push · PR 은 금지다.
- 끝나면 각자 아래 명령으로 알린다:

  ```bash
  orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[worker_done] <planner|backend> 메뉴 키 보강 완료 — <한 줄>" --enter
  ```
