# customer-erd-spec 결과 보고 — DAY-SPEC-000 · ERD v1 반영

- 작성: day `planner` · 2026-11-18 · task `task_ae694ca36919` · dispatch `ctx_aa5a97ada3f7`
- 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec` (브랜치 `kknaksss/customer-erd-spec` · base `origin/main`) — 커밋 · push · PR 안 함

## 상태: done

## 1. 바꾼 파일 · 절

| 파일 | 바꾼 곳 |
|---|---|
| `products/day/20-spec/spec-000-data-model.md` | frontmatter(`version` 0.0.1 → 0.0.2 · `last_updated` 2026-11-18 · `sources` 5줄 추가 · `status: stable` 그대로) · 머리 개정 노트 · §1 새 절 「원장 전환」(두 조건) · 주제 표(4-1 해제 · 8 ~ 11 행) · §2 「원장」 · 「참조 + 스냅샷」 · §2.1 `product_option_id` 한 줄 · §3 02 `external_ref.entity_type` 새 값 · §3 03 `visit` 「KOS 데스크 몫」 2행 · 「시술 개념 셋」 · §3 05 「정한 것」 · `visit_task` 칸 3개 추가 · 「다른 곳으로」 2행 · **§4 전체 다시 씀**(공통 · prod 표시 · KOS 없이 되는지 · 04-1 이름 변경 + 새 메뉴 3 · 08 구매 · 결제 · 09 시술권 · 10 선불카드 · 11 처방) · §6 OQ(공통 · 03 · 04-1 · 08 · 09 · 10) |
| `products/day/40-architecture/erd.md` | 관계도 제목 · 문장 + 새 관계 23개 · 메뉴 관계도(이름 변경 · 「1차에서 만들지 않음」 정리 · 23개) · 인벤토리 새 28행 · 개수 문장 · `last_updated` |
| `products/day/40-architecture/system.md` | 「원장 두 단계」 아래 한 줄(2026-11-18 전환 결정 · 시점 OQ-00-2) · `last_updated` |
| `products/day/20-spec.md` | 최종 수정 · In Scope 의 SPEC-000 요약 · Out Of Scope 메뉴 · 시술권/수납/선불카드 줄 · 용어 「스냅샷」 |
| `products/day/README.md` | 1차 범위 「메뉴 테이블 1차에 만들지 않음」 한 줄 |
| `products/day/log.md` | 2026-11-18 `spec-change, arch-change` 행(PR 칸 = 「PR 전 · 코디가 PR」) · 최종 수정 |

건드리지 않음: SPEC-001 ~ 005 · WORK · 화면 문서 · `10-decision.md`(DEC 없음) · `30-work.md`.

## 2. 새 테이블 수

새 테이블 28개(prod 에 없음) + 칸만 추가 1개(`visit_task`).

- 메뉴 16 = 2026-11-03 설계 13(이름 변경 4 포함) + ERD v1 새 3(`prepaid_card_product` · `etcetera_product_category` · `etcetera_product`)
- 구매 5 · 시술권 3 · 선불카드 3 · 처방 1
- ERD v1 에서 처음 생긴 테이블은 15개(새 메뉴 3 + 12). 나머지 13개는 2026-11-03 메뉴 설계에 있었고, 이번에 「만든다」로 바뀌었다.

## 3. prod 표시 (CENTURION_DAY `origin/prod` = `a6aa4ba5` · `backend/day/models/*.py` `__tablename__` 직접 확인)

| 테이블 | prod | 이번 변경 |
|---|---|---|
| prod 52개(customer 7 · hospital 3 · misc 13 · room 7 · staff 7 · task 10 · visit 5) | 있음 | 이름 · 타입 변경 0 |
| `visit_task` | 있음(`treatment_item_id` · `ticket_id` · `machines` 없음 확인) | 칸만 추가 3개 · 모두 nullable |
| `external_ref` | 있음(`entity_type` = `String` 열린 값) | 칸 변경 없음 · 새 값만 |
| `visit_requested_procedure` · `consultation_procedure` | 있음(`product_option_id` FK 없는 UUID) | 변경 없음(OQ-041-7) |
| 메뉴 16 · 구매 5 · 시술권 3 · 선불카드 3 · 처방 1 | 없음 | 새 테이블 |

## 4. KOS 없이 되는지 (SPEC-000 §4 표 요약)

| 주제 | DAY 칸만으로 |
|---|---|
| 결제 합계 · 완료 | 된다 — Σ 거래 `amount` vs Σ(조정 금액 또는 `price_amount`) |
| 부분 환불 금액 | 단일 시술권(번들 ÷ 티켓 수 × `used` 수) · 선불카드 상품(`use` 이력 합)은 된다 · 묶음 옵션은 안 된다(직원 입력 · 3차 5) |
| 구매 확정 때 시술권 N장 | 단품 옵션은 된다(`purchase_item.count`) · 코스 옵션은 세트별 장 수 규칙 표본 없음(OQ-09-2) |
| 선불카드 상품 확정 때 카드 + 충전 이력 | 된다(`prepaid_card_product` 값 사용) · 담아 둔 뒤 메뉴가 바뀐 경우 OQ-10-4 |
| 잔액 · 총액 | 된다 — 잔액 칸 + 총액 = `charge` 이력 합 |
| 선불카드 결제 | 된다 — 다만 주머니(금액 · 포인트) 순서는 표본 없음(OQ-10-5) |
| 처방 | 안 한다 — 처방은 KOS. 최소 행만 |

## 5. ERD v1 과 다르게 쓴 곳 · 이 SPEC 이 붙인 것

- **칸 이름**: ERD v1 이 뜻으로만 적은 칸에는 기존 표 관례대로 이름을 붙였다. 예: `title` · `price_amount` · `charge_amount` · `charge_point` · `expiration_days` · `sort_order` · `is_closed` · `balance_amount` · `point_balance` · `expires_at` · `adjusted_*` · `payment_config` · `occurred_at` · `memo`. 이 규칙은 §4 「공통」에 적어 두었다.
- **enum 값**: DAY 말은 소문자로 썼다. 예: `initialized` · `accepted` · `refunded` · `partially_refunded` / `pending` · `not_in_process` · `refunding` / `approved` · `canceled` / `available` · `in_use` · `used` / `product_option` · `prepaid_card_product` · `etcetera_product`. KOS 대문자 · 오타 `ETCETRA_PRODUCT` 는 「외부(KOS)」 열에만 있다.
- **`payment_type` 값 7개**: KOS `…Configuration` 7종 이름에서 가져왔다(cash · card · transfer · platform · prepaid_card · easy_pay · medical_loan). KOS 문자열은 본 값 3개(CASH · PREPAID_CARD · TRANSFER)만 적었다. 나머지는 OQ-08-5.
- **`purchase_item.count`**: ERD v1 「스냅샷(이름 · 단위 · 수량)」의 「수량」을 KOS `optionConfiguration.count`(회차)로 읽었다. 화면 「수량」은 행을 반복하는 것이라(HAR 1차 Q4) 설명에 그 사실을 적었다. **검수 때 이 해석이 맞는지 확인해 주세요.**
- **`purchase_item` 가격 · 조정 칸**: 「가격(금액 · 공급가 · 면세 · 부가세 · 과세)」을 칸 다섯 개로 나눴다. 원래 가격의 `supplied/tax_free/vat` 는 필수로 두었다(KOS 가 늘 줌).
- **새 테이블 `id` uuid PK**: 연결 테이블(`prepaid_card_customer` · `purchase_assignee`)도 §2 「id uuid」를 따랐다. 복합 PK 는 ERD v1 이 말하지 않았다.
- **`hospital_id`**: 메뉴 테이블에만 두었다(ERD v1 그림이 메뉴에만 `hospital` 선을 그림). 나머지는 §2.1 대로 부모를 거쳐 안다. 칸을 둘지는 OQ-08-6.
- **`purchase_transaction.staff_id` 필수**: ERD 그림 `staff ||--o{` 대로 했다. 동기화 때 KOS 담당자가 DAY 에 없는 경우는 구현 때 확인할 것.
- **`prepaid_card_ledger.pocket` · `amount` nullable**: `expiry_change` 행 때문이다. 바뀐 만료 시각 자리는 OQ-10-6.
- **`revoke` = 주머니마다 1행**: `pocket` 칸이 하나뿐이라 그렇게 적었다.
- **ERD v1 이 칸을 안 적은 테이블**: `purchase_price_adjustment` 는 관계 FK 2개 + 「칸 미정 — OQ-08-4」(KOS `priceAdjustments` 표본 0). `purchase_assignee` 는 FK 2개(HAR `assigneeIds[]`) + 대표 담당 구분은 OQ-08-3.
- **넣지 않은 KOS 값**: 통화(`currency`) · 다국어(`translsMap`) · 카드 `description` · 거래 금액 분해 · 승인 / 취소 시각. ERD v1 에 없어 칸으로 두지 않았고, 거래 쪽은 OQ-08-5 에 적었다.
- **erd.md 개수 정정**: 이전 문장 「1차 51개」를 52개로 고쳤다. 인벤토리 행 수와 prod 모델 수가 모두 52 다. 2026-11-10 `visit_task_chart_log` 를 세지 않은 수로 보인다.
- **SPEC 버전 0.0.2**: 브리프대로 올렸다. 다만 `rules/document-pipeline.md` 는 `version` 을 「상위기획 사이클 = 제품 버전 · 문서를 고쳤다고 올리지 않는다」로 정하고 있다. 짝이 되는 `00-baseline/planning/0.0.2-상위기획.md` 는 없다(lint 는 검사하지 않음). 되돌릴지는 코디 판단.

## 6. 영향 (SPEC-000 범위 밖 · 건드리지 않음)

- `visit_requested_procedure` 설명의 「1차에 시술권 테이블이 없다」(SPEC-000 §3 03)는 사실과 어긋나게 됐다. ERD v1 이 말하지 않아 그대로 두었다.
- SPEC-002(시술 현황)의 `visit_task` 동기화 표에 새 칸 3개(`treatment_item_id` · `ticket_id` · `machines`)를 채우는 줄이 필요하다. 다음 동기화 스펙 때 다룰 것.
- `10-decision.md` 의 「현재 결론」에 SPEC-000 날짜(2026-11-11)가 남아 있다. ESC 가 아니라 건드리지 않았다.

## 7. 검증

### lint (`python3 scripts/lint-pipeline.py --strict`)

- 작업 전: `0 error, 263 warning` · `products/day` 줄 0
- 작업 후: `0 error, 263 warning` · `products/day` 줄 0 → **products/day 범위 ERROR 0 · WARN 0**
- 263 warning 은 모두 다른 제품의 것으로 이번 변경과 **무관**하다(예: selly `doc_no` · `version` 누락 등). 작업 전후 수가 같다.

### ERD v1 테이블 → SPEC-000 칸 표 (헤딩 줄)

| 테이블 | 줄 | 테이블 | 줄 |
|---|---|---|---|
| product_category | L1295 | purchase | L1525 |
| product | L1308 | purchase_item | L1537 |
| product_category_link | L1327 | purchase_price_adjustment | L1561 |
| product_option | L1335 | purchase_transaction | L1573 |
| product_option_price | L1359 | purchase_assignee | L1592 |
| product_option_composition | L1368 | ticket_bundle | L1619 |
| treatment_item | L1383 | ticket_set | L1631 |
| treatment_item_machine · treatment_item_medicine | L1403 | ticket | L1643 |
| treatment | L1410 | prepaid_card | L1669 |
| machine · medicine | L1421 | prepaid_card_customer | L1685 |
| etc_task_type(그대로) | L1428 | prepaid_card_ledger | L1695 |
| prepaid_card_product | L1438 | prescription | L1721 |
| etcetera_product_category | L1457 | visit_task(칸 추가) | §3 05 표 |
| etcetera_product | L1471 | | |

ERD v1 의 테이블 28개 + `visit_task` 가 모두 칸 표를 가진다.

### 개인정보 grep

`grep -nE '01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9a-f]{24}'` 를 바꾼 파일 6개에 돌림:

- **이번에 더한 줄(`git diff` 의 `+` 줄)에서는 0건.**
- 파일 전체에서는 2건이 걸린다. 둘 다 원래 있던 줄의 KOS **데모 지점** 기타 작업 id 다(SPEC-000 L232 · log.md 2026-11-10 행). 이번 변경과 무관하고 손대지 않았다.
- HAR 값(고객 · 직원 이름 · 전화 · 차트번호 · 메모 · KOS id · tenant id)은 옮기지 않았다. 문서에는 필드 이름 · 건수 · 메뉴 이름(비공개 멤버십1 · VIP 플랜 · 승모근보톡스100 등)만 있다.

## 8. 열린 것 (§6 · 새로 연 OQ)

- **공통**
  - OQ-00-2 원장 전환 시점 · 절차
  - OQ-00-3 백필 범위
  - OQ-00-4 새 테이블 동기화 주기
- **04-1** OQ-041-7 희망 · 상담 시술의 `product_option_id` 를 채울지 · FK 를 걸지
- **08 구매 · 결제**
  - ERD v1 「열린 것」: OQ-08-1 과세 출처 · OQ-08-2 직원 수정 화면 · OQ-08-8 `revokingItems`
  - 옮기며 드러난 것: OQ-08-3 담당 구분 · OQ-08-4 조정 칸 · OQ-08-5 거래 세부 · OQ-08-6 `hospital_id` · OQ-08-7 `payment_required` 관계
- **09 시술권**
  - ERD v1 「열린 것」: OQ-09-1 환불 뒤 티켓 · `in_use`
  - 옮기며 드러난 것: OQ-09-2 코스 옵션 세트 규칙
- **10 선불카드**
  - ERD v1 「열린 것」: OQ-10-1 공유 해제 · 공유 고객 결제 · OQ-10-2 환불 뒤 이벤트
  - 옮기며 드러난 것: OQ-10-3 `kind` 매핑 · OQ-10-4 확정 시점 메뉴 값 · OQ-10-5 주머니 순서 · OQ-10-6 `expiry_change` 자리
- **닫은 것**
  - OQ-041-6(이름 → `treatment` · `treatment_item`)
  - OQ-03-1 의 수납 · 처방 연결(반응 `reactions` 만 열림)

ERD v1 「열린 것」 6줄은 모두 OQ 로 옮겼다(08-1 · 08-2 · 08-8 · 09-1 · 10-1 · 10-2).

---

## 수정 1차 (2026-11-18 · task `task_c753d29567a5` · 지시서 `spec-fix-1-instructions.md` · 검수 `review-spec-report.md`)

### 고친 곳

| 항목 | 파일:줄 | 무엇 |
|---|---|---|
| F-1 | `products/day/40-architecture/README.md:39` | 메뉴 줄 → 「메뉴 · 상품 · 옵션 · 시술 항목 · 시술 외 품목 · 선불카드 상품 — 2026-11-18 만든다(prod 에 없음)」 · `treatment_item` · `prepaid_card_product` · DAY-SPEC-000 §4 04-1 · 미작성 |
| F-1 | `40-architecture/README.md:40 ~ 43` | 도메인 줄 추가 — 구매 · 결제(§4 08) · 시술권(09) · 선불카드(10) · 처방(11) |
| F-1 | `40-architecture/README.md:50` | 「원장 두 단계」 끝에 예약 구현 뒤 DAY 원장 전환 · OQ-00-2 한 줄 |
| W-1 | `20-spec/spec-000-data-model.md:505` | 희망 시술 「1차에 시술권 테이블이 없다」 → 시술권 id 칸 없음(prod 그대로) · 시술권 테이블은 §4 09 · 연결은 OQ-041-7 과 함께 |
| W-1 | `spec-000:541` · `:548` | 상담 시술 「1차는 스냅샷만」 · `product_option_id` 이유를 「메뉴 테이블은 §4 · 채울지 · FK 는 OQ-041-7」로 |
| W-1 | `spec-000:579` | 개념 트리 → 「스냅샷 + 2026-11-18 참조 칸(treatment_item_id · ticket_id)」 |
| W-1 | `spec-000:728` | 「1차는 스냅샷만(04-1 보류)」 → 「prod 칸은 스냅샷(~~04-1 보류~~ — 2026-11-18 해제)」 |
| W-1 | `spec-000:750` | 묶음 이름 「스냅샷 (1차 — 메뉴 테이블 없음)」 → 「스냅샷」 |
| W-1 | `40-architecture/erd.md:166` | `consultation_procedure` 책임 → 「prod 칸은 스냅샷 · 메뉴 참조를 채울지는 SPEC-000 OQ-041-7」 |
| W-6 | `erd.md:220` | `etcetera_product` 핵심 키에 FK `hospital_id` |
| W-6 | `spec-000:1390` · `:1398` | 「진료항목 코드 · 가격」 → 「시술 항목 코드 · 가격」 (`prepaid_card_ledger.deleted_at` 문장은 지시대로 그대로) |
| W-2 | `spec-000:1508` | 「화면 수량 = 같은 항목 행 반복(수량 칸 없음) · ERD v1 스냅샷의 「수량」 = `count` = 회차(5회권 = 5)」 — 코디 결정 |
| W-3 | `spec-000:1233` | §4 「공통」에 `etc_task_type` 근거 한 줄(ERD v1 원천 「04-1 그대로 끌어옴」 포함) · 개수 28 / 80 유지 |
| W-5 | `spec-000:9` · `:36` · `log.md:17` | `version` 0.0.2 → **0.0.1** · 개정 노트 · log 행의 「0.0.2」 문구도 「버전 0.0.1 그대로(문서 수정으로 올리지 않음)」로 |
| W-4 | `spec-000:1747` | OQ-00-3 에 「구매 백필은 방문 백필이 먼저 · KOS 담당자가 DAY `staff` 에 없는 거래(`staff_id` 필수) 처리」 한 줄(결정하지 않음) |

### 검증

- lint `python3 scripts/lint-pipeline.py --strict` → `0 error, 263 warning` · `products/day` 줄 0(263 WARN 은 모두 타 제품 · 무관 · 작업 전과 같음).
- `grep -rn "medical_service\|1차에서 만들지 않음\|0\.0\.2" products/day/` (90-archive 제외) — **메뉴 뜻으로 남은 곳 0 · `0.0.2` 0**. 남은 줄 분류:

| 줄 | 분류 |
|---|---|
| `spec-000:36`(개정 노트 「§4 를 「1차에서 만들지 않음」에서 새 테이블 절로 바꿨다」) · `erd.md:116`(줄 긋기 `~~…1차에서 만들지 않음~~ → 만든다`) | 개정 기록 · 정상 |
| `spec-000:1279` · `:1347` · `:1376` · `:1384` · `:1404` | 이름 변경 기록(「← `medical_service…`」) · 정상 |
| `spec-000:752` · `:759` · `spec-002-procedure-board.md:809` | prod 스냅샷 칸 `visit_task.medical_service_title`(이름 그대로 — 조건 1) · 정상 |
| `log.md:17` | 이번 개정 log 행(「버전 0.0.1」 — grep 은 행 안 `medical_service` 이름 변경 서술로 걸림) · 정상 |

- 이번 수정 줄 개인정보 grep 0.
