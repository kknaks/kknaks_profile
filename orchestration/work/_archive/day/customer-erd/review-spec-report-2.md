# 리뷰 리포트 — customer-erd-spec / doc 재검수 1차 (2026-11-18)

- 검수: day `reviewer_doc` · task `task_1620013ca68c` · dispatch `ctx_b044fe92266d`
- 대상: planner 수정 1차(`spec-fix-1-instructions.md` · `spec-change-report.md` 「수정 1차」) — `git diff origin/main -- products/day/`(미커밋 · 7파일)
- 기준: 1차 리포트 `review-spec-report.md`(F-1 · W-1 ~ W-6) + 코디 결정 4건
- 줄 번호는 지금 작업 트리 기준

## 판정: PASS

F-1 · W-1 · W-6 이 닫혔고, 코디 결정 4건(W-2 · W-3 · W-4 · W-5)도 모두 반영됐다. 수정하면서 새로 깨진 곳은 없다. lint `--strict` 는 `0 error, 263 warning` 이고 `products/day` 줄은 0 이다(263 은 모두 다른 제품 · 무관).

## FAIL

없음.

## WARN

없음. 아래 두 곳은 기록만 남긴다(지시서 제안 범위 안 · 고치지 않아도 됨).

- SPEC-000 L541 · L548 의 「1차는 스냅샷만 / 1차는 비워 둔다」는 문구가 남아 있다. 다만 이유가 「메뉴 테이블은 §4 · 채울지 · FK 는 OQ-041-7」로 바뀌었고, prod 칸이 실제로 비어 있으니 사실과 어긋나지 않는다. 1차 리포트 W-1 제안(「이유만 바꾼다」)대로다.
- SPEC-000 L728 「옵션 · 진료항목 이름 …」은 prod 스냅샷 칸 `medical_service_title`(KOS `medicalServiceConfiguration.title`)을 설명하는 말이다. 메뉴 테이블 이름이 아니므로 그대로 둬도 된다.

## 1차 지적 → 닫힘 확인

| # | 확인한 곳 | 지금 | 판정 |
|---|---|---|---|
| F-1 | `40-architecture/README.md:39` | 「메뉴 \| 상품 · 옵션 · 시술 항목 · 시술 외 품목 · 선불카드 상품 — 2026-11-18 만든다(원장 전환 대비 · prod 에 없음) \| `product` · `product_option` · `treatment_item` · `prepaid_card_product` \| DAY-SPEC-000 §4 04-1 \| 미작성」 | 닫힘 |
| F-1 (추가 권고) | `README.md:40 ~ 43` | 구매 · 결제(§4 08) · 시술권(09) · 선불카드(10) · 처방(11) 도메인 줄을 같은 형식으로 추가. 대표 테이블이 SPEC-000 과 같음 | 닫힘 |
| F-1 (원장) | `README.md:50` | 「예약 구현 뒤 연동 기간 병원도 DAY 원장으로 전환(2026-11-18 · OQ-00-2)」 — system.md L140 과 같은 뜻 | 닫힘 |
| W-1 | SPEC-000 L505 | 「시술권 id 칸을 두지 않는다(prod 칸 그대로 · 시술권 테이블은 §4 09 — 연결 여부는 OQ-041-7 과 함께)」 | 닫힘 |
| W-1 | L541 · L548 | 이유 → 「메뉴 테이블은 §4 · 채울지 · FK 는 OQ-041-7」. 타입 `uuid FK` 그대로 | 닫힘 |
| W-1 | L579 | 트리 → 「스냅샷 + 2026-11-18 참조 칸(treatment_item_id · ticket_id)」 | 닫힘 |
| W-1 | L728 | 「prod 칸은 스냅샷(cc 방식 · ~~04-1 보류~~ — 2026-11-18 해제 · 아래 줄)」 | 닫힘 |
| W-1 | L750 | 묶음 이름 → 「스냅샷」(칸 · 타입 변경 없음) | 닫힘 |
| W-1 | `erd.md:166` | `consultation_procedure` 「상담 시술(참고 · prod 칸은 스냅샷 · 메뉴 참조를 채울지는 SPEC-000 OQ-041-7)」 | 닫힘 |
| W-6 | `erd.md:220` | `etcetera_product` 핵심 키 「`id` · FK `hospital_id` · `etcetera_product_category_id`」 — SPEC-000 표와 같음 | 닫힘 |
| W-6 | SPEC-000 L1390 · L1398 | 「시술 항목 코드」 · 「시술 항목 가격」 | 닫힘 |
| W-6 | `prepaid_card_ledger.deleted_at` 문장 | 지시대로 그대로 | 해당 없음 |

## 코디 결정 반영 확인

| 결정 | 확인한 곳 | 지금 | 판정 |
|---|---|---|---|
| W-2 `count` = 회차 | SPEC-000 L1508 | 「**화면 수량** = 같은 항목 행 반복(수량 칸 없음) · ERD v1 스냅샷의 「수량」 = `count` = 회차(5회권 = 5 · HAR 1차 Q1 · Q4 — 코디 결정 2026-11-18)」. 1차 리포트가 지적한 v1 「수량」 ↔ 「수량 칸 없음」 충돌이 없어졌다. `purchase_item.count` 칸 설명(L1549 부근)과도 맞다 | 반영 |
| W-3 `etc_task_type` 만든다 | SPEC-000 L1233 | 「ERD v1 그림엔 없으나 원천 「`04-1-menu.md` 그대로 끌어옴」에 포함되어 함께 만든다(코디 결정 · 메뉴 16 · 새 28)」. 개수 28 / 80 은 SPEC-000 prod 표시 · erd.md 와 같음 | 반영 |
| W-5 version 0.0.1 | SPEC-000 L9 `version: 0.0.1` · L36 개정 노트 · `log.md:17` 「버전 0.0.1」 | `grep -rn '0\.0\.2' products/day/` 결과 **0건** | 반영 |
| W-4 OQ-00-3 한 줄 | SPEC-000 L1747 | 「구매 백필은 해당 방문(`purchase.visit_id` 필수) 백필이 먼저이고, KOS 담당자가 DAY `staff` 에 없는 거래(`purchase_transaction.staff_id` 필수) 처리도 정해야 한다(결정하지 않음 · 검수 W-4)」 — 결정하지 않고 열어 둔 채로 적었다 | 반영 |

## 수정이 새로 깨뜨린 곳 — 없음

- **칸 · 타입**: `git diff origin/main` 중 §4 앞(prod 테이블 절 · L1221 앞)에서 바뀐 표 줄은 설명 · 묶음 이름 · 주제 표 · 이미 승인된 `visit_task` 새 칸 3개뿐이다. 칸 이름 · 타입이 바뀐 줄은 0 이다(L548 `uuid FK` 그대로 · L750 은 묶음 칸만). prod 표시(L1235 ~)도 그대로다.
- **범위**: 바뀐 파일 7개가 모두 `products/day/` 안에 있다. 1차 때보다 `40-architecture/README.md` 가 하나 늘었고, 이는 F-1 수정 때문이다. SPEC-001 ~ 005 · `30-work*` · `10-decision.md` 의 diff 는 0 이다.
- **개인정보**: `git diff origin/main -- products/day` 에서 더한 줄 중 `01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9a-f]{24}` 에 걸리는 것은 0건이다.
- **lint**: `python3 scripts/lint-pipeline.py --strict` → `0 error, 263 warning` · `products/day` 줄 0.

## 남은 grep 분류 (`grep -rn "medical_service\|1차에서 만들지 않음\|0\.0\.2" products/day/` · 90-archive 제외)

| 줄 | 분류 |
|---|---|
| `spec-000:36` · `erd.md:116` · `log.md:17` | 개정 기록 · 줄 긋기 → 정상 |
| `spec-000:1279` · `:1347` · `:1376` · `:1384` · `:1404` | 이름 변경 기록(「← `medical_service…`」) → 정상 |
| `spec-000:752` · `:759` · `spec-002-procedure-board.md:809` | prod 스냅샷 칸 `visit_task.medical_service_title`(이름 그대로 — 조건 1) → 정상 |
| 메뉴 뜻으로 남은 곳 · `0.0.2` | **0** |

## 직원이 실물에서 만날 자리

해당 없음(문서 단계).

## 참고(기존 부채)

1차 리포트와 같다. 원래 있던 개인정보 grep 2건(SPEC-000 L232 · log.md L62 · 데모 지점 KOS 작업 id)이 있고, 10-decision 「현재 결론」 날짜 · SPEC-002 동기화 표의 새 칸 3개는 이번 범위 밖이다.
