# planner 수정 1차 — review-spec-report.md 반영

검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/review-spec-report.md` (FAIL 1 · WARN 6 · 사용자 판단 4). 아래대로 고친다. allowed_paths · 금지 규칙은 원 브리프 그대로. 커밋 금지.

## 고칠 것

1. **F-1** `products/day/40-architecture/README.md:39` 메뉴 줄 → 리포트 「FAIL 고칠 곳 목록」 제안대로(2026-11-18 만든다 · prod 에 없음 · `treatment_item` · DAY-SPEC-000 §4). 구매 · 시술권 · 선불카드 · 처방 도메인 줄도 같은 형식으로 추가. README L46 「원장 두 단계」에 system.md 와 같은 한 줄(예약 구현 뒤 DAY 원장 전환 · OQ-00-2).
2. **W-1** SPEC-000 옛 문장 5곳(L505 · L541/548 · L579 · L728 · L750) + erd.md L166 — 리포트 표의 「제안」대로. 칸 · 타입은 바꾸지 않는다.
3. **W-6** erd.md L220 `etcetera_product` 핵심 키에 FK `hospital_id` · SPEC-000 L1389 · L1397 「진료항목」 → 「시술 항목」. `prepaid_card_ledger.deleted_at` 문장은 그대로 둔다.

## 코디 결정(2026-11-18 · 사용자 위임 「완주」 — 추천값)

- **W-2** `purchase_item.count` = KOS `optionConfiguration.count`(회차) 해석 유지. L1507 문구를 「화면 수량 = 같은 항목 행 반복(수량 칸 없음) · `count` = 회차(5회권 = 5)」로 바꿔 충돌을 없앤다. 근거 `har-check-report.md` L54 · L163.
- **W-3** `etc_task_type` 은 「만든다」에 둔다(ERD v1 원천 「04-1 그대로 끌어옴」). 개수 28 / 80 유지. §4 에 「ERD v1 그림엔 없으나 04-1 그대로 끌어옴에 포함」 한 줄 근거.
- **W-5** `version` 을 0.0.1 로 되돌린다(rules/document-pipeline.md — 문서 수정으로 올리지 않음). 개정 표시는 `last_updated` · 개정 노트 날짜로만. erd.md · 20-spec.md 등에서 0.0.2 를 언급했으면 같이 되돌린다.
- **W-4** OQ-00-3 에 한 줄: 「구매 백필은 해당 방문 백필이 먼저 · KOS 담당자가 DAY `staff` 에 없는 거래 처리(`purchase_transaction.staff_id` NOT NULL)」. 결정은 하지 않는다.

## 검증 · 보고

- lint `--strict` products/day ERROR 0 · `grep -rn "medical_service\|1차에서 만들지 않음\|0\.0\.2" products/day/` 결과를 리포트에 붙인다(메뉴 뜻 0 · 다른 뜻은 분류).
- `spec-change-report.md` 끝에 「수정 1차」 절 추가(고친 곳 파일:줄).
- 완료 보고는 원 브리프 §9 와 같은 두 명령(같은 task-id · dispatch-id 는 이번 dispatch preamble 값).
