# review-doc-13 — 마감 스펙 검수 (SPEC-006 개정 ⑪ · SPEC-000 2026-11-24 개정 · SPEC-002 개정 ㉗)

- 대상: 워크트리 `day-reservation-spec` HEAD `682f2aed` 위 미커밋 변경 6 파일(planner-fix-21). 고치지 않음 · 커밋 안 함.
- 기준: `review-doc-12-report.md` · `planner-fix-21-report.md` · 결정 R73 ~ R75 · 코드 `CENTURION_DAY/day-reservation`(HEAD `4d8878ab`).
- 줄 번호 = 지금 워크트리 파일.

## 판정: **PASS** (WARN 3)

| # | 항목 | 확인한 곳 | 판정 |
|---|---|---|---|
| ① | R73 · R75 반영 · R72 꼬리표 · R74 낡은 문장 | SPEC-006 L36 · L49(개정 ⑪) · L51(⑩ 보충 2 꼬리표 취소선 → R75) · L138 RV-45 · L191 U-5 순서 · L288 U-9 표시 · L290 누가 · 언제(둘 다 지난 날 아님 ∧ 같은 날 KST) · L330 S-8 · L428 API · L574 · L580 · L581 케이스 · L668 Rule 8 · L675 Rule 15 · L676 Rule 16 · L720 시안 차이 | PASS |
| ② | migration 0018 ~ 0023 = 코드 | `20261123_0018_reservation_permission`(down `0017_ext_catalog`) · `0019_transaction_status_more` · `0020_purchase_task_visit_index` · `0021_notice_permission` · `0022_companion_tables` · `0023_companion_permission` — revision · down_revision 체인 · 내용(키 · level · ON CONFLICT DO NOTHING · 되돌리면 키 행 삭제) 모두 SPEC 문장과 같음 | PASS |
| ③ | SPEC-000 개정 | 08 status 5값(코드 `TRANSACTION_STATUSES` 5개 · `ADD VALUE` 3개) · 수단 7종(코드 `PAYMENT_TYPES` 7개) · 02 `entity_type = notice`(코드 `sync_notices.py` `NOTICE = "notice"`) · 03 `companion_group`(id · hospital_id · created_by_staff_id · 시각 3칸) · `companion_member`(id · hospital_id · companion_group_id · visit_id · added_by_staff_id · 시각 3칸) = `models/companion.py` · migration 0022 칸과 같음 · `uq_companion_member_visit_id`(부분 유일) · `ix_companion_member_companion_group_id`(부분) · `ix_purchase_visit_id` · `ix_visit_task_visit_id`(0020 · 둘 다 `deleted_at IS NULL`) · OQ-07-2 닫음 · OQ-4A-1 좁힘 · `event_log` `companion_join` / `companion_leave`(코드 `reservation_companions.py`) | PASS |
| ④ | SPEC-002 개정 ㉗ | 키 표 `reservation` view · `reservation.notice` edit · `reservation.companion` edit · 「어느 묶음이든 같은 세 행」 = `policies/permissions.py` ROWS `full` · `view` 둘 다 세 키 같은 level · migration 0018 · 0021 · 0023 · OQ-02 덧붙임 | PASS |
| ⑤ | SPEC-006 「다른 스펙과 다른 곳」 | L728 · L729 · L730 · L732 · L733 취소선 + 「반영 · 이제 다른 곳 없음」 · L87 Domain note 「아직 없음」 취소선 · L749 칸 정본 = SPEC-000 · 남은 L727(수납 원천 = 같음) · L731(KOS 기다림) · L735(카드 단위)는 실제 차이라 남는 게 맞음 | PASS |
| ⑥-1 | PLATFORM · EASY_PAY · MEDICAL_LOAN 표본 없는 매핑 | 결정 R53 「수단 PLATFORM · EASY_PAY · MEDICAL_LOAN」 그대로 · 코드 주석 「openapi 문자열 그대로 · 표본 없음」 · OQ-4A-1 닫지 않고 「좁힘」 = 맞음 | PASS |
| ⑥-2 | 404 추가 | 코드 `reservation_companions.py` L8 · L283 · L364 `NotFound` · 라우터 docstring 순서 400 → 404 → 409 = SPEC L428 | PASS |
| ⑥-3 | 동행 절 위치 | SPEC-000 §3 03 「예약 / 방문」 끝(L614 ~) — 멤버 = `visit` 행 · 날짜도 `visit` 에서 앎 → 맞는 자리 | PASS |
| ⑦ | lint | `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning(모두 다른 제품 · `products/day` 0) | PASS |

## 낡은 문장 grep (취소선 밖)

| 대상 | 결과 | 판정 |
|---|---|---|
| 「동행그룹」 · 꼬리표 · 책갈피 · 18px · 걸쳐 — SPEC-006 | L36 · L49 · L51(결정 범위 · 뒤집음 설명) · L288 「꼬리표 · 책갈피 탭(R74) 없음」 · 나머지 취소선 안 | PASS |
| 같은 말 — 10-decision · 20-spec · log | 10-decision L29 · log L17 = 뒤집음 요약 · log L18 = 개정 ⑩ 보충 2 이력 행(이력이라 그대로) · 20-spec 예약 현황 줄 = 「진한 파란 굵은 띠 · 글자 없음(R75 — ~~R72 꼬리표~~)」 | PASS |
| `group_id`(동행) | SPEC-006 L746 취소선 · 나머지는 `reservation_group_id` · `companion_group_id` | PASS |
| 「같은 시작 칸」 | 바뀐 문서 취소선 안만 | PASS |

## WARN

- **W13-1**: SPEC-006 L191 U-5 「순서」 문장에 옛 사슬(취소 · 노쇼 뒤 → 동행 그룹 이웃 자리 → 그룹 생긴 순 → `reserved_start_at` → 생성 순)이 취소선 없이 남고, 그 뒤에 R73 문장(그룹 카드 먼저 → 그룹 없는 카드)이 붙었다. 옛 사슬은 「그룹을 시작 시각 사이에 끼운다」로도 읽힐 수 있다. Rule 15(L675)와 코드(`reservation_layout.py` — 그룹 먼저 · 그다음 `alone.sort(closed, start_min, created_at)`)는 R73 과 같아 구현이 잘못 갈 위험은 낮다. 옛 사슬을 취소선으로 하거나 「→ R73」 한 마디를 넣으면 깔끔하다.
- **W13-2**: SPEC-000 개정 노트 ①(L41) 「enum 값은 더하면 못 뺀다」 — 코드 0019 downgrade 는 새 값 행을 지우고 참조를 끊은 뒤 enum 을 다시 만들어 **뺄 수 있다**(행 손실 있음). 0013 때와 같은 관용 문장이라 틀린 계약은 아니지만, 「되돌리면 새 값 거래 행을 지운다」가 더 사실에 가깝다.
- **W13-3**(범위 밖 · 코드): `day/models/companion.py` docstring 에 「같은 시작 칸」이 남아 있다(R71 = 같은 30분 행). SPEC 쪽은 맞다 — 코드 정리 몫.

## 남은 것 (범위 밖 · 그대로)

- `40-architecture/erd.md` 에 동행 두 테이블 없음 · 30-work Coverage · Delivery #267 ~ #269 재결속(코디 몫) · 띠 두께 · 둥글기 = 구현.
