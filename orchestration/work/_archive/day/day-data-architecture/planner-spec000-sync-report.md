# DAY-SPEC-000 동기화 — #225 구현 · 검수 결과 반영 보고

## 상태: done

## 수행 내용

워크트리 `mediness-mediness/day-data-architecture-spec`(PR #909 브랜치) · `products/day/` 만 · 커밋 안 함. SPEC-000 은 생성기(원천 표 그대로 옮김)로 다시 만들고, 원천에 없는 구현 결정은 생성기 골격(skeleton)에 별도 절로 넣었다 — 원천 표의 칸은 고치지 않았다.

### 1. 사용자 결정 (원천에 이미 반영된 것 → 다시 옮김)

| 자리 (`products/day/20-spec/spec-000-data-model.md`) | 내용 |
|---|---|
| :101 §2 공통 규칙 새 행 「유일 · 삭제」 | 원천 README 새 줄 그대로 — 유일은 살아 있는 행만(`WHERE deleted_at IS NULL` 부분 유일) · 지운 행 값 재사용 가능 · 복합 PK 는 그대로 |
| :77 「표 읽는 법」 | 「표의 `UNIQUE` · 「유일」 표기는 §2 「유일 · 삭제」대로 살아 있는 행만」 한 줄 — 각 표의 UNIQUE 표기는 그대로 두고 §2 를 가리킨다 |
| :1062 07 `chat_room.direct_key` | 원천 그대로 — 타입 `varchar`(전역 UNIQUE 빠짐) · 설명에 **UNIQUE(hospital_id, direct_key)** |

### 2. 구현이 정한 것 (검수가 받아들인 것 — 「SPEC 정리 요청」)

| 자리 | 내용 |
|---|---|
| :103 §2.1 「구현(#225)으로 정한 것」 새 절 | ① **병원을 아는 방법** — 표에 `hospital_id` 가 없는 하위 테이블은 칸을 덧붙이지 않고 부모 행(`visit` · `customer` 등)을 거쳐 병원을 안다. ② **`event_log` · `push_log` · `external_outbox` 의 `deleted_at`** — §2 우선으로 둔다(NULL 허용). 「쌓기만」은 기록 내용을 고치거나 행을 물리 삭제하지 않는다는 뜻으로 읽는다는 한 줄 · `updated_at` 은 표대로. ③ **「uuid FK」 대상 표**(구현 리포트 목록 그대로 — 직원류 → staff · `*_zone_id` → zone · `room_id` → room · `funnel_id` → funnel · `referrer_customer_id` → customer · `event_log/external_outbox/board_card_order.hospital_id` → hospital · `board_card_order.visit_id` → visit). ④ **FK 안 거는 칸** 3개(`external_ref.entity_id` · `product_option_id` · `external_outbox.visit_id`) |
| :78 「표 읽는 법」 | 「대상이 적히지 않은 uuid FK → §2.1」 한 줄 |
| :374 02 뒤 「코드 테이블 타입 · 필수 (#225 구현으로 정함)」 새 표 | 구현 그대로 — `id` · `hospital_id` · `name` 필수, `color` · `sort_order` · `is_closed` · `is_default` · `category_id`(→ funnel_category) NULL 허용, 타입은 같은 이름 칸(varchar · int · bool · uuid FK) · link 테이블 PK 두 칸 · 생성/수정 ✓ · `deleted_at` NULL 허용 |

### 3. `products/day/40-architecture/erd.md`

- :110 공통 줄 — 하위 테이블은 부모 행으로 병원 · 「유일」/UNIQUE 는 살아 있는 행만(§2 「유일 · 삭제」) 두 가지를 붙임.
- :160 `chat_room` 핵심 키 `direct_key` UNIQUE → (`hospital_id`, `direct_key`) UNIQUE.

### 4. `products/day/log.md:17` — 2026-11-05 `spec-change, arch-change` · DAY-SPEC-000 · #909.

## 검증

```
python3 scripts/lint-pipeline.py --strict → 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0 (263 은 타 제품 기존 — 무관)
```

원천 → SPEC-000 대조(생성기 · 스크립트): 원천 표 69 · 데이터 행 571 → 누락 0(04 의 「로그인 · 세션 계약」 표는 SPEC-001 링크로 둔 것이라 대조에서 뺌 — fix2 와 같음).

## 제안 (만들지 않음 — 목록 밖에서 찾은 차이)

1. **계정에 달린 테이블은 「부모로 병원을 안다」가 맞지 않는다** — `device` · `notification_setting` · `push_log`(→ account · device) · `chat_member`(→ account)는 부모가 `account` 인데 `account` 는 병원에 묶이지 않는다(계정 1 : 직원 N). §2.1 ①은 예시로 `visit` · `customer` 하위만 적었다. 이 테이블들이 병원과 무관한지(계정 단위) 한 줄로 정해 두기를 권장 — 특히 `push_log` 는 표 설명상 알림(→ hospital_id 있음)을 거쳐 병원을 알 수 있다.
2. **§2 「생성 · 수정 · 삭제 시각」과 `event_log` · `push_log`** — §2 는 「DAY 테이블에는 `created_at` · `updated_at` · `deleted_at` 만」인데 두 표는 `created_at` 만이고 구현은 `updated_at` 을 안 붙였다(검수 「§2 가 강제하지 않음」). 이 줄을 「쌓기만 테이블은 `updated_at` 없음」 예외로 §2 에 적을지 사용자 확인.
3. **필수 bool 칸에 기본값이 없다**(검수 판정 「받아들임」) — #226 동기화가 모든 필수 bool 을 직접 채워야 한다. SPEC 이 아니라 #226 브리프 몫으로 보이지만 기록.
4. 검수 「조용히 통과」 7(병원 경계 FK 없음 — `visit.room_id` 가 다른 병원의 방을 가리켜도 DB 가 막지 않음)은 SPEC 에 제약이 없다 — 서비스 몫으로 둘지 SPEC 에 「같은 병원」 규칙을 둘지 정할 거리.
