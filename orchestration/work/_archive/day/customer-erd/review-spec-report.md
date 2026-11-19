# 리뷰 리포트 — customer-erd-spec / doc (2026-11-18)

- 검수: day `reviewer_doc` · task `task_8011ad8afa87` · dispatch `ctx_0f104ebe16ca`
- 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec` 미커밋 변경 (`git diff origin/main -- products/day/`) — 6 파일 · +544 / −75
- 대조 기준: `reference/2026-11-18-day-customer/erd-draft.md`(ERD v1) · planner 브리프 §2 · §6 · §7 · HAR 리포트 1 ~ 3차 · CENTURION_DAY `origin/prod` = `a6aa4ba5` `backend/day/models/*.py`
- 이 문서의 SPEC-000 줄 번호는 작업 트리 기준

## 판정: FAIL (고칠 곳 1개 · 작음) — 고치고 나면 WARN 으로 PASS 가능

| 축 | 판정 |
|---|---|
| 1. ERD v1 대조 | WARN — 빠진 것 0. 다르게 쓴 것 2개(`purchase_item.count` 해석 · `etc_task_type` 「만든다」)는 사용자 판단 |
| 2. 상용 운영 조건 | PASS(prod 모델 직접 대조) · WARN 1개(NOT NULL FK 와 백필) |
| 3. KOS 제거 조건 | PASS |
| 4. 이름 변경 일관성 | **FAIL** — `40-architecture/README.md:39` 에 `medical_service` 와 「1차에서 만들지 않음」이 남아 있음 |
| 5. 근거 · 열린 것 | PASS — v1 「열린 것」 6줄이 모두 OQ 로 감 · 추가된 줄의 개인정보 0 |
| 6. 범위 | PASS — `products/day/` 밖 변경 0 · SPEC-001 ~ 005 · WORK · 10-decision 변경 없음 |
| 7. 문서 정합 | WARN — erd.md 와 수 · 관계는 맞음. SPEC-000 안에 옛 문장 5곳이 남음 · 버전 0.0.2 규칙 충돌 |
| lint `--strict` | PASS — exit 0 · `0 error, 263 warning` · `products/day` 줄 0(263 WARN 은 모두 다른 제품 · **무관**) |

---

## FAIL

### F-1 `products/day/40-architecture/README.md:39` — 메뉴 도메인 줄을 안 고침(축 4 · 7)

- 지금 문장: `| 메뉴 (자체 운영 단계) | 상품 · 옵션 · 진료항목 — **1차에서 만들지 않음** | \`product\` · \`product_option\` · \`medical_service\` | DAY-SPEC-000 §4 | 해당 없음(1차) |`
- 근거: ERD v1 처음 4(`medicalService` = `treatment_item`) · SPEC-000 §4 04-1 L1278(이름 변경) · erd.md L116(「만든다」). 같은 `40-architecture/` 안에서 erd.md 는 「만든다」, README 는 「만들지 않음」이라고 서로 다르게 말한다. `products/day/` 전체에서 메뉴 뜻의 `medical_service` 가 남은 곳은 이 한 줄뿐이다.
- 고칠 것: 도메인 이름 「메뉴」(「자체 운영 단계」 삭제) · 책임 「상품 · 옵션 · 시술 항목 · 시술 외 품목 · 선불카드 상품 — 2026-11-18 만든다(원장 전환 대비 · prod 에 없음)」 · 대표 테이블 `product` · `product_option` · `treatment_item` · `prepaid_card_product` · Code source 「미작성」. 같은 표에 08 구매 · 결제 / 09 시술권 / 10 선불카드 / 11 처방 도메인 줄(대표 테이블 · `DAY-SPEC-000 §4 08 ~ 11`)을 더할지는 planner 가 정하면 된다. 더하는 쪽을 권한다. 표가 「핵심 도메인」 지도이기 때문이다.
- 이 줄 아래 「장기 invariant」의 「원장 두 단계」(README L46)에도 system.md 와 같은 한 줄(「예약 구현 뒤 DAY 원장 전환 · OQ-00-2」)을 붙이는 것을 권한다(WARN 수준).

---

## WARN

### W-1 SPEC-000 안에 남은 옛 문장 — 이번 개정과 맞지 않음(축 7)

모두 고칠 수 있는 곳이다(`products/day/`). 칸 · 타입은 바꾸지 않고 설명만 바꾸는 일이다.

| 줄 | 지금 문장 | 어긋나는 점 | 제안 |
|---|---|---|---|
| L505 | 「시술권은 KOS 데스크 몫이고 **1차에 시술권 테이블이 없다**」(`visit_requested_procedure` · `kind = ticket`) | §4 09 에서 시술권 테이블을 만든다. planner 리포트 §6 에도 「영향」으로 적혀 있다 | 「시술권 id 칸은 두지 않는다(prod 칸 그대로 · 2026-11-18 시술권 테이블은 §4 09 — 연결 여부는 OQ-041-7 과 함께)」 |
| L541 · L548 | `consultation_procedure` 「1차는 스냅샷만」 · `product_option_id` 「1차는 비워 둔다(**메뉴 테이블 없음** — 04-1)」 | 메뉴 테이블이 생긴다. 칸을 채울지는 OQ-041-7 로 열려 있다 | 「(메뉴 테이블은 §4 · 채울지 · FK 는 OQ-041-7)」로 이유만 바꾼다 |
| L579 | 개념 트리 `visit_task … → 1차는 스냅샷만(cc 방식 — 04-1 보류)` | 04-1 보류가 풀렸다. `treatment_item_id` · `ticket_id` 가 생긴다 | 「스냅샷 + 2026-11-18 참조 칸(`treatment_item_id` · `ticket_id`)」 |
| L728 | 「**1차는 스냅샷만**(cc 방식 · 04-1 보류)」 | 바로 아래 L729 「2026-11-18 추가」와 같은 목록 안에서 서로 다르게 말한다 | 앞 문장에 `~~04-1 보류~~` 표시를 하거나 「prod 칸은 스냅샷」으로 바꾼다 |
| L750 | 묶음 이름 「스냅샷 (1차 — **메뉴 테이블 없음**)」 | 같은 표 L759 에 메뉴 FK `treatment_item_id` 가 있다 | 「스냅샷」 |
| erd.md L166 | `consultation_procedure` 「상담 시술(참고 · 1차는 스냅샷만)」 | 위 L541 과 같다(prod 칸은 그대로라 사실 자체는 맞음) | L541 을 고치면 같이 고친다 |

### W-2 `purchase_item.count` — ERD v1 의 「수량」을 「회차」로 읽음(축 1 · **사용자 판단**)

- v1 은 `purchase_item` 스냅샷을 「이름 · 단위 · **수량**」이라고 적었다. SPEC-000 은 L1549 에서 `count` = KOS `optionConfiguration.count`(회차 · 5회권 = 5)로 두었다. L1507(정한 것)에는 「**수량** = 같은 옵션 항목을 한 행 더(**수량 칸 없음**)」라고 적었다.
- 근거는 있다. `har-check-report.md` L54(5회권 = 항목 1행 · `count 5`) · L163(화면 수량 1→2 = 행 추가 · 수량 칸 없음). planner 리포트 §5 도 확인을 요청했다.
- 걸리는 점: v1 문구와 SPEC 문구가 바로 충돌한다(「수량」 칸 있음 ↔ 「수량 칸 없음」). 이 칸은 「KOS 없이 시술권 N장 만들기」(L1258)의 근거라서 뜻이 중요하다.
- 사용자가 정할 것: v1 의 「수량」이 회차(`count`)라는 해석이 맞는가. 맞으면 L1507 문구를 「화면 수량 = 행 반복 · `count` 는 회차」로 바꿔 충돌을 없앤다.

### W-3 `etc_task_type` 을 「새 테이블 · 만든다」로 셈(축 1 · **사용자 판단**)

- v1 관계도 · 표 어디에도 `etc_task_type` 이 없다. 브리프 §6-1 은 「`etc_task_type` 등 기존 것은 그대로 둔다」였다. 그런데 §4 머리(L1225 「이 절의 테이블을 **만든다**」) · prod 표시(L1244 「메뉴 16개 … `etc_task_type` … 새 테이블」) · erd.md 인벤토리 L216 · 개수 문장 L234(28개 = 메뉴 16) 가 이 테이블을 이번에 만드는 것으로 센다.
- 이렇게 읽을 근거도 있다. v1 원천 줄 「메뉴: `04-1-menu.md` … **그대로 끌어옴**」이고, 04-1 에 `etc_task_type` 이 있다(6회).
- 사용자가 정할 것: `etc_task_type` 도 이번에 만드는가. 아니면 v1 그림대로 27개로 하고 `etc_task_type` 은 「설계만」으로 남기는가. 개수(28 / 80)는 이 답에 따라 바뀐다.

### W-4 NOT NULL FK 와 백필 · 동기화(축 2)

- `purchase.visit_id` 는 필수다(v1 처음 1 · L1531). `purchase_transaction.staff_id` 도 필수다(v1 그림 `staff ||--o{` · L1585). v1 대로라 정책 위반은 아니다.
- 다만 원장 전환 전에는 KOS → DAY 동기화 + **백필**로 채운다. 지금 `visit` 은 오늘 일정만 받는다(10초). 그래서 지난 구매를 백필하려면 그 방문(일정)도 같이 백필해야 한다. 퇴사 · 삭제된 KOS 담당자의 거래는 `staff` 행이 없을 수 있다.
- OQ-00-3(백필 범위 · L1746)에는 이 의존이 적혀 있지 않다. 「구매 백필은 방문 백필이 먼저 · 담당자가 없는 거래 처리」를 OQ-00-3 에 한 줄 더하기를 권한다. 결정은 하지 않는다. planner 리포트 §5 도 `staff_id` 위험을 적었다.

### W-5 SPEC `version` 0.0.2 — 규칙과 충돌(축 7 · **코디 · 사용자 판단**)

- `rules/document-pipeline.md` §타입별 추가 필드: `version` = 상위기획 사이클(제품 버전) · 「**문서를 고쳤다고 올리지 않는다**」. `00-baseline/planning/0.0.2-상위기획.md` 는 없다. lint 는 이걸 검사하지 않는다.
- 브리프가 버전을 올리라고 했고 planner 도 리포트 §5 에 이 충돌을 적었다. 되돌릴지(0.0.1 · 개정 노트 날짜로만 표시)는 코디가 정한다.

### W-6 작은 것

- erd.md L220 인벤토리 `etcetera_product` 핵심 키에 `hospital_id` 가 없다. SPEC-000 L1478 에는 `hospital_id` FK 가 필수로 있다. 다른 메뉴 행과 맞추려면 「FK `hospital_id` · `etcetera_product_category_id`」로 적는다.
- SPEC-000 `treatment_item` 표 L1389 「진료항목 코드」 · L1397 「진료항목 가격」 — 설명 글자에 옛 말 「진료항목」이 남아 있다. v1 처음 4 는 「피부과엔 진료 없음」이다. 칸 이름은 이미 바뀌었으니 「시술 항목 코드 · 가격」으로 맞추면 된다.
- `prepaid_card_ledger.deleted_at` 「이력은 채우지 않는다」(L1710) — v1 은 「쌓는다」까지만 적었다. 이력 원장의 성격에 맞아 문제는 없지만, v1 에 없는 문장이라 기록해 둔다.

---

## 축별 근거

### 1. ERD v1 대조 — 테이블 전수

v1 에 있는 테이블 28개(+ 지금 있는 `hospital` · `customer` · `visit` · `staff` · `customer_type`)를 SPEC-000 · erd.md 와 맞춰 본 결과다.

| v1 테이블 | SPEC-000 칸 표 | erd.md 관계 | erd.md 인벤토리 | v1 핵심 칸 · 정한 것 |
|---|---|---|---|---|
| product_category | L1295 | 메뉴도 | L203 | 04-1 그대로 ✓ |
| product | L1308 | 메뉴도 | ✓ | ✓ |
| product_category_link | L1327 | 메뉴도 | ✓ | ✓ |
| product_option | L1335 | 메뉴도 | ✓ | 옵션 단위 `unit_type · unit_value`(1차 8) ✓ |
| product_option_price | L1359 | 메뉴도 | ✓ | ✓ |
| product_option_composition | L1368 | 메뉴도 | ✓ | 이름 변경 ✓ |
| treatment | L1410 | 메뉴도 | ✓ | 처음 4 ✓ |
| treatment_item | L1383 | 메뉴도 | ✓ | 처음 4 ✓ |
| treatment_item_medicine | L1403 · L1408 | 메뉴도 | ✓ | ✓ |
| treatment_item_machine | L1403 · L1407 | 메뉴도 | ✓ | ✓ |
| medicine · machine | L1421 | 메뉴도 | ✓ | 「넣는다」 ✓ |
| prepaid_card_product | L1438 | 메뉴도 | ✓ | 이름 · 가격 · 충전 금액 · 포인트 · 유효 일수 · 순서 · 닫힘 · 설명 ✓(2차 1) |
| etcetera_product_category | L1457 | 메뉴도 | L219 | 이름 · 순서 · 닫힘 ✓ |
| etcetera_product | L1471 | 메뉴도 | L220 | 분류 FK · 이름 · 가격 하나 · 과세 칸 없음 ✓ (W-6) |
| purchase | L1525 | 관계도 | ✓ | `visit_id` 필수 · status 4 · process 3 ✓(처음 1 · 3차 1) |
| purchase_item | L1537 | 관계도 | ✓ | item_type 3 · 종류별 FK · 스냅샷 · 가격 5 · 조정 5 ✓ (W-2) |
| purchase_price_adjustment | L1561 | 관계도 | ✓ | v1 이 칸을 안 적음 → FK 2개 + 「칸 미정 OQ-08-4」 ✓ (HAR 표본 0) |
| purchase_transaction | L1573 | 관계도 | ✓ | 부호 금액 · status 2 · 자기 참조 · payment_type + jsonb · prepaid_card_id · staff_id ✓(1차 2 ~ 4) |
| purchase_assignee | L1592 | 관계도 | ✓ | v1 은 관계만 → FK 2개 + OQ-08-3 ✓ |
| ticket_bundle | L1619 | 관계도 | ✓ | customer · purchase_item · 이름 · 가격(여기만) ✓(1차 9) |
| ticket_set | L1631 | 관계도 | ✓ | treatment_item 참조 · 단위 · 이름 스냅샷 ✓(2차 6) |
| ticket | L1643 | 관계도 | ✓ | status 3 · 가격 칸 없음 ✓ |
| prepaid_card | L1669 | 관계도 | ✓ | 소유자 · purchase_item_id nullable · 잔액 2 · 만료 · deleted_at · 총액 없음 ✓ |
| prepaid_card_customer | L1685 | 관계도 | ✓ | 공유자만 ✓(1차 6 · 2차 8) |
| prepaid_card_ledger | L1695 | 관계도 | ✓ | kind 6 · pocket 2 · 부호 금액 · 사용자 · 거래 FK · staff · 메모 · 시각 ✓(2차 4) |
| prescription | L1721 | 관계도 | ✓ | id · visit_id · 시각만 ✓ · OQ-03-1 닫음 ✓ |
| visit_task(칸 추가) | L758 ~ 760 | `ticket |o--o| visit_task` · `treatment_item |o--o{ visit_task` | — | `treatment_item_id` · `ticket_id` · `machines` · `medicines` 유지 · 회차 스냅샷 그대로 ✓(처음 3 · 5) |

- **v1 의 「정한 것」**(처음 1 ~ 5 · 3-1 / 1차 1 ~ 9 / 2차 1 ~ 8 / 3차 1 ~ 8 · 결제 취소 ≠ 환불 표 · 선불카드 상품 환불 완료 · 처방 · 약품 · 기기 · 수납 추가 HAR): 모두 §4 각 절 「정한 것」(L1497 · L1608 · L1660) · 표(L1512) · L1278 ~ L1281 에 번호와 함께 있다. 빠진 것 0.
- **v1 에 없는데 만든 것**: 테이블은 `etc_task_type`(W-3)뿐이다. 칸 이름(`title` · `*_amount` · `sort_order` · `is_closed` · `adjusted_*` · `payment_config` · `occurred_at`)은 v1 이 뜻으로만 적은 것에 이름을 붙인 것이고, L1231 에 규칙으로 적혀 있다. 새 테이블의 `id` · `created_at/updated_at/deleted_at` 은 §2 공통 규칙을 따른 것이다. `payment_type` 값 7개는 `har-check-report.md` L95 ~ L102 · L188(수단별 설정 7종)이 근거다. `hospital_id` 를 메뉴에만 둔 것은 OQ-08-6 으로 열어 두었다. → 근거 없는 정책 없음.
- erd.md 관계 수: 1차 관계도 새 관계 23개 · 메뉴 관계도 23개 — 줄을 세어 맞음. v1 관계 중 빠진 것 0.

### 2. 상용 운영 조건 — prod 직접 대조(`git -C CENTURION_DAY show origin/prod:` · `a6aa4ba5`)

- prod `__tablename__` 52개(account … zone)를 SPEC-000 L1240 · erd.md L234 「prod 52개」와 맞춰 봄 → 맞음. 새 테이블 28개 중 prod 에 이름이 있는 것은 0이다(`etc_task_type` · `treatment*` · `purchase*` · `ticket*` · `prepaid_card*` · `prescription` 모두 없음).
- `visit_task`(`models/task.py` L51 ~ L95): `treatment_item_id` · `ticket_id` · `machines` 는 없다 → 「칸만 추가」 표시가 맞다. 셋 모두 nullable 로 적혀 있다(SPEC L758 ~ 760 필수 칸 비어 있음). 남는 칸 `medicines`(ARRAY String) · `medical_service_title` · `option_title` · `ticket_round_current/total` 도 그대로 남는다 → 이름 · 타입 변경 0.
- `external_ref.entity_type`: prod 타입은 `Mapped[str]`(열린 문자열)이다 → 「새 값만 · 칸 변경 없음」(L383)이 맞다.
- `visit_requested_procedure` · `consultation_procedure` `product_option_id`(`models/visit.py` L82 · L122): `UUID` 이고 FK 가 없다 → 「그대로 · OQ-041-7」이 맞다.
- `visit.purchase_ids` · `prescription_ids`: prod 에는 칸이 없다(모델 주석에만 「보류」로 있음). SPEC 은 이 두 칸을 만들지 않고 `purchase.visit_id` · `prescription.visit_id` 로 닫았다 → prod 영향 0.
- 백필 · 원장 전환 OQ: OQ-00-2(시점 · 절차 · 충돌 규칙을 뒤집는 시점 · DAY → KOS 명령 목록) · OQ-00-3(백필 범위) · OQ-00-4(동기화 주기) 모두 열려 있다(L1745 ~ L1747). §1 「원장 전환」(L81 ~ L93) · §2 「원장」(L135) · system.md L140 은 「전환 전까지는 지금 그대로」라고 적었다 → 열린 것을 닫힌 것처럼 쓴 곳 없음. (W-4 의존 하나는 더하기를 권함)

### 3. KOS 제거 조건

- 새 표 L1221 ~ L1730 의 칸 이름에 `kos` · `external_id` · `vendor` 가 없다. KOS id(`purchaseId` · `purchaseItemId` · 거래 `id` · `ticketGroupId` · 티켓 `id` · 카드 `id` · `chargingId` · `optionId` · 처방 id)는 모두 설명 · 「외부(KOS)」 열에서 `external_ref` 로 보낸다(L383 · L1229).
- enum 은 모두 소문자 DAY 말이다. KOS 대문자 · 오타 `ETCETRA_PRODUCT` 는 「외부(KOS)」 열에만 있다(`item_type` L1543 · `status` · `payment_type` · 티켓 · 이력 `kind` 표의 외부 열).
- DAY 칸만으로 되는지(L1251 ~ L1261): 결제 합계 · 완료(거래 `amount` · 항목 가격 / 조정 금액) ✓ · 부분 환불(번들 가격 ÷ 티켓 수 × `used` · `use` 이력 합 · 묶음 옵션은 직원 입력 = v1 3차 5) ✓ · 시술권 생성(단품 = `count` 장 · 코스 OQ-09-2) ✓ · 카드 생성 + `charge`(상품 메뉴 값 · OQ-10-4) ✓ · 잔액 칸 + 총액 = `charge` 합 ✓ · 선불카드 결제(주머니 순서 OQ-10-5) ✓. 안 되는 곳은 모두 OQ 로 열려 있다.
- KOS 계산값을 칸으로 두지 않음: 카드 총액 없음(L1683) · 티켓 가격 없음(L1653) · 결제액 칸 없음(L1502) ✓.

### 4. 이름 변경 일관성 — grep 분류

`grep -rnE 'medical_service|procedure' products/day/**/*.md`(90-archive 제외) 결과를 뜻별로 나눴다.

| 분류 | 위치 | 판정 |
|---|---|---|
| 메뉴 뜻 · 남은 곳 | **`40-architecture/README.md:39`** `medical_service` · 「1차에서 만들지 않음」 | **FAIL F-1** |
| 이름 변경 기록(「← 옛 이름」 · 줄 긋기) | SPEC-000 L1278 · L1346 · L1375 · L1383 · L1403 · L1410 · L1778 · erd.md L116 · log.md L17 | 정상 |
| KOS 필드 이름(외부 열) | `procedure.id` · `medicalService.id` · `medicalServiceConfiguration.*` | 정상 |
| prod 스냅샷 칸(이름 그대로 두는 것) | `visit_task.medical_service_title`(L752) · `visit_requested_procedure` · `consultation_procedure` · `procedure_note` | 정상(조건 1) |
| 다른 뜻 | 작업 단계 enum `procedure` · `procedure_done`(L456) · cc `procedure` 테이블(L726 · L736) · SPEC-002 `procedure-board` | 정상 · 제외 |
| 설명 글자 「진료항목」 | `treatment_item` 표 L1389 · L1397 | W-6 |

### 5. 근거 · 열린 것

- v1 「열린 것」 6줄 → OQ-08-1(과세 출처) · OQ-09-1(환불 뒤 티켓 · `in_use`) · OQ-10-1(공유 해제 · 공유 결제) · OQ-08-2(직원 수정 화면) · OQ-10-2(환불 뒤 이벤트) · OQ-08-8(`revokingItems`). 6/6 ✓. 브리프에서 요구한 원장 전환(OQ-00-2) · 백필(OQ-00-3) · 과세 출처(OQ-08-1)도 있다 ✓.
- 옮기면서 더한 OQ(00-4 · 041-7 · 08-3 ~ 7 · 09-2 · 10-3 ~ 6)는 모두 「v1 이 말하지 않음 / 표본 없음」을 이유로 연 것이다. 결정한 것이 아니다 ✓.
- 문장마다 v1 번호나 HAR 리포트 절이 붙어 있다. v1 에 없는 문장도 HAR 리포트에서 확인됐다(예: 「남길 금액 0 → `refunded`」 = 3차 S1 · 「KOS 는 환불 완료 때 잔액 · 총액 0 · 행은 남김」 = 3차 S5).
- 개인정보 grep `01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9a-f]{24}`: **이번에 더한 줄 0건**. 파일 전체로는 2건(SPEC-000 L232 · log.md L62)이 걸리지만, 둘 다 원래 있던 줄이고 이번 변경과 무관하다(데모 지점 기타 작업 id). 메뉴 이름(승모근보톡스100 · 비공개 멤버십1 · VIP 플랜1)은 브리프가 허용한 공개 정보다.

### 6. 범위

- `git diff origin/main --name-only`: 6개 모두 `products/day/` 안(20-spec.md · spec-000 · erd.md · system.md · README.md · log.md). 밖은 0.
- SPEC-001 ~ 005 · `30-work*` · `10-decision.md` · `21-*`: diff 0 ✓.

### 7. 문서 정합

- erd.md ↔ SPEC-000: 새 테이블 28개 = 인벤토리 28행(L203 ~ L230) = SPEC prod 표시(L1244 ~ L1248) ✓. 「prod 52 + 28 = 80」 ✓. 「이전 51개는 `visit_task_chart_log` 를 빼고 센 수」라는 정정도 prod 52개로 확인 ✓. 개수는 W-3 의 답에 따라 바뀐다.
- system.md L140: 지금 사실은 그대로 두고 한 줄만 더했다 ✓(브리프 §6-3).
- `20-spec.md` L30 · L39 · L40 · L55, `README.md` L34: 범위 문장을 바꾼 것 ✓. 줄 긋기(`~~…~~ →`)는 이 레포에서 개정을 표시하는 관례대로다.
- 남은 것: F-1 · W-1 · W-6.

---

## 사용자 판단 (결정하지 않고 모음)

1. **W-2**: v1 `purchase_item` 「수량」 = KOS `count`(회차)로 읽은 해석이 맞는가.
2. **W-3**: `etc_task_type` 도 이번에 「만든다」에 넣는가(28개) · 아니면 v1 그림대로 27개인가.
3. **W-5**: SPEC-000 `version` 0.0.2 를 유지하는가 · 규칙대로 0.0.1 로 되돌리는가(코디).
4. **W-4**: OQ-00-3 에 「구매 백필은 방문 백필이 먼저 · 담당 직원이 없는 거래 처리」를 더하는가.

## 직원이 실물에서 만날 자리

- 해당 없음(문서 단계 · 화면 변경 없음). 구현 때 처음 만날 자리: 지난 구매를 백필할 때 방문 · 담당 직원이 없는 행(W-4) · 코스 옵션 시술권 장 수(OQ-09-2) · 선불카드 주머니 순서(OQ-10-5).

## 참고(기존 부채)

- 개인정보 grep 에 걸리는 2건(SPEC-000 L232 · log.md L62)은 이번 변경 전부터 있던 것이다(데모 지점 KOS 기타 작업 id).
- `10-decision.md` 「현재 결론」의 SPEC-000 날짜(2026-11-11) — ESC 가 아니라 범위 밖이다(planner 리포트 §6).
- SPEC-002 동기화 표에 `visit_task` 새 칸 3개를 채우는 줄이 아직 없다. 다음 동기화 스펙 때 다룬다(planner 리포트 §6).

## FAIL 고칠 곳 목록

| # | 파일:줄 | 무엇으로 |
|---|---|---|
| F-1 | `products/day/40-architecture/README.md:39` | 「메뉴 (자체 운영 단계) … 1차에서 만들지 않음 … `medical_service` … 해당 없음(1차)」 → 「메뉴 · 상품 · 옵션 · 시술 항목 · 시술 외 품목 · 선불카드 상품 — 2026-11-18 만든다(prod 에 없음) · `product` · `product_option` · `treatment_item` · `prepaid_card_product` · DAY-SPEC-000 §4 04-1 · 미작성」. 08 ~ 11 도메인 줄 추가를 권함 |

(W-1 · W-6 은 같은 PR 에서 함께 고치기를 권하지만, PASS 를 막지는 않는다.)
