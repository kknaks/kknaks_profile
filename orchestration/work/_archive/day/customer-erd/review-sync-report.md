# 리뷰 리포트 — customer-erd 동기화 스펙 / doc (2026-11-19)

- 검수: day `reviewer_doc` · task `task_13e04279c99e` · dispatch `ctx_7de93fad295d`
- 대상: `git diff origin/main -- products/day/`(base `4585fb59` #951 · 미커밋 · 5파일). 검수 중에 planner 가 event_log 를 되돌렸다. 마지막 스냅샷은 11:0x 기준 `181 insertions / 34 deletions` 이다.
- 대조 기준: `customer-erd-spec-2-brief.md` §3 결정 1 ~ 10 · `spec-2-scope-change.md` · `spec-2-delete-log.md` · `kos-sync-research-report.md` · `spec-sync-report.md` · CENTURION_DAY `origin/prod`
- **축 4 변경(코디 · 사용자 2026-11-19)**: 삭제 로그(`event_log`)는 빼기로 했다. 그래서 축 4 는 「물리 삭제 0 · 소프트 딜리트 원칙」만 판정하고, event_log 줄은 「되돌림 대상」으로만 적는다(아래).

## 판정: PASS (WARN 6 · FAIL 0)

| 축 | 판정 |
|---|---|
| 1. 결정 1 ~ 10 반영 | WARN — 빠진 것 0. 결정 밖 추가 3개는 근거가 있고 리포트에도 밝혔다(W-2 · W-3 · W-5). REFUND 매핑 해석 1개(W-4) |
| 2. 사실 대조 | PASS — 경로 · 요청 키 · 공개/내부 · 매핑 값이 조사 리포트와 같다. 지어낸 경로 0. 조사에서 관찰되지 않은 안쪽 키 1곳은 OQ-12 로 밝혔다(W-6) |
| 3. 백필 | PASS(WARN 1 · W-1) — 절차 · 안전 규칙 절이 없다. OQ-00-3 은 열린 채 메모 7줄 + Q2 링크다 |
| 4. 삭제(변경된 축) | PASS — 물리 삭제 금지 문구 · 소프트 딜리트 원칙이 있다. event_log 줄은 판정 안 함(되돌림 대상) |
| 5. SPEC-000 수정 | PASS — 결정 5 · 6 · 7 과 조사 사실에 따른 설명만 고쳤다. prod 칸 · 타입 변경 0. version 0.0.1 |
| 6. 범위 · 개인정보 · lint | PASS — `products/day/` 밖 0 · 더한 줄 개인정보 0 · lint `--strict` `0 error, 263 warning` · `products/day` 0(263 은 모두 다른 제품 · 무관) |

## FAIL

없음.

## WARN

| # | 파일:줄 | 무엇 | 고칠 것 / 판단 |
|---|---|---|---|
| W-1 | `spec-000-data-model.md:37` | 개정 노트가 SPEC-002 절 이름을 「KOS 읽기 — 새 테이블 동기화 **· 백필**」로 적었다. 실제 절 제목(SPEC-002 L837)은 「KOS 읽기 — 새 테이블 동기화 (개정 ㉔ · 2026-11-19)」이고, 백필은 범위 밖이다(scope-change). 범위 변경 전 이름이 남은 것으로 보인다 | 「· 백필」을 지운다 |
| W-2 | `spec-002:864`(루프 ⑤) | 결정 2 는 「공개 **거래** 통계 · **카드 이벤트** 통계」 둘이다. ⑤ 에는 `get-purchase-item-statistics`(새 구매 나열)가 더 있다. 근거는 조사 Q3(「새 구매는 구매 항목 통계 `createdDateTimeUtcFrom`」)이고, id 나열에만 쓰므로 결정 9 와 맞는다 | **사용자 판단** — 셋째 통계를 넣어도 되는가(빼면 거래 없는 새 구매를 5분 루프가 놓친다) |
| W-3 | `spec-002:849` · 원천 표 `treatment_item` · `machine` · `medicine` 줄 | 결정 3 「원천 = 내부」의 예외로 공개 메뉴 API 를 쓴다. 근거는 조사 Q1 · Q5 다: 시술 항목은 내부 경로가 없고, 기기 · 약물 내부 경로는 404 다. 통계가 아니라 메뉴 목록이다. planner 리포트 §5 에 밝혔다 | **사용자 확인** — 다른 길이 없으므로 그대로 두기를 권한다 |
| W-4 | `spec-002` 매핑 표 `prepaid_card_ledger.kind` 줄 · `spec-000:1705` | 결정 5 는 「실측된 값(… 카드 이벤트 `REFUND` · `amount.type BALANCE`)은 SPEC-000 enum 에 **더한다**」이다. planner 는 새 enum 값을 만들지 않고 기존 `revoke` · `balance` 에 매핑했다. `BALANCE` → `balance` 는 이미 있는 값이라 문제없다. `REFUND` → `revoke` 는 뜻이 맞다. ERD v1 의 `revoke` = 환불 완료 회수이고, 실측 REFUND = 환불 때 남은 잔액을 주머니마다 뺀다. 다만 문구는 해석이다 | **사용자 판단** — `REFUND` = `revoke` 로 확정하는가(새 값 `refund` 를 따로 두지 않음) |
| W-5 | `spec-002:864` · 「바뀐 것만」 표 오늘 밖 고객 줄 | 5분 루프에서 나열된 고객에게 ③(시술권 · 카드)도 부른다. 결정 1 의 「구매가 바뀐 고객」 규칙을 오늘 밖 고객에게도 쓴 것이다. planner 리포트 §5 에 밝혔다 | 기록만(결정 1 · 2 를 합친 결과라 자연스럽다) |
| W-6 | `spec-002` 원천 표 아래 `visit_task` 새 칸 줄 | `treatment_item_id` = `procedureConfiguration.medicalServiceConfiguration.id` · `machines` = `…machines[].name` 은 조사 리포트에서 관찰되지 않았다(SPEC-000 HAR 1차 · 외부 열 근거). 본문에 「안쪽 키 관찰은 OQ-12 와 같이 남는다」고 밝혔다 | 기록만 |

## 축별 근거

### 1. 결정 1 ~ 10

| 결정 | 위치(spec-002 / spec-000) | 판정 |
|---|---|---|
| 1 바뀐 고객만(10초 회차 안) | 루프 표 ③ · ④ · 「바뀐 것만」 표 · L871 「`2 + 2V` 를 부르지 않는다」 · SPEC-000 OQ-00-4 닫음 | ✓ |
| 2 오늘 밖 = 통계 5분 · OQ-00-4 닫음 | 루프 표 ⑤ · ⑥ · SPEC-000 §2 「동기화」 · OQ-00-4 · system.md L149 ~ 151 | ✓ (W-2) |
| 3 원천 내부 · 통계는 id | 「원천 고르기」 L847 ~ | ✓ (W-3) |
| 4 시술권 내부 `get-ticket-bundles` | 원천 표 | ✓ |
| 5 매핑 표 · enum 추가 · 표본 없는 값 OQ · `entity_type` 새 값 | 매핑 표 · `entity_type` 20개 · SPEC-000 `purchase.status` `paid` · `process` `revoking` · `prepaid_card_item_substituting` · OQ-08-9 · OQ-10-3 좁힘 · `conversion` 은 OQ-08-10 | ✓ (W-4) |
| 6 옵션 단위 칸 뺌 · 1차 8 문구 | SPEC-000 L1283 · L1351 · L1511 · L1552 · erd.md L124 · L208 | ✓ |
| 7 구성 `ref_single_option_id` 뺌 · `treatment_item` 가격 · 시간 · 간격 유지 + 「KOS 원천 없음」 | SPEC-000 L1378 · L1401 · L1402 | ✓ |
| 8 백필 | 범위 밖(scope-change) — 결정으로 쓰지 않음 | ✓ |
| 9 통계 = id 나열만 | 「원천 고르기」 · ⑤ · ⑥ 「나열만」 · 매핑 아래 「거래 id 는 원장 API 로만」 | ✓ |
| 10 DEMO 테넌트만 | 「환경」 절(L944 ~) — `hospitalName` DEMO 테넌트 · 실 테넌트 이름은 안 적음 | ✓ |

- **기본값으로 열어 둔 OQ** — 지금 스냅샷 기준이다. 모두 「기본값 · 조사 · 결정에 없음」이 표시돼 있어 열린 채다 ✓.
  - OQ-69: 방문 없는 구매 = 건너뜀
  - OQ-70: 매핑 밖 값 = 건너뜀
  - OQ-73: 빠진 번들 = 지우지 않음
  - 넷째였던 OQ-77(삭제 로그 묶기)은 event_log 와 함께 되돌려져 지금은 없다.
  - OQ-71 · 72 는 「미결」이다.

### 2. 사실 대조 (조사 리포트 실호출 표 · Q1 · Q3 · Q4)

- 메뉴 경로 · 요청 키(`{sort}` · `{deleted:false, includePromotions:false}` · `{deleted:false}` · `{closed:false}` · `{}`) · 내부/공개 구분이 조사 L32 ~ 48 · Q1 표와 같다.
- 구매: 내부 `get-purchase-summaries {purchaseIds[], includeDeleted:true}` · 87개 한 번(L116) ✓. 시술권: 내부 `get-ticket-bundles {visitorId, sort?}` ✓. 카드: 요약 · 이벤트 · 공유 고객 경로와 「`available` 넣지 않음」(L59) ✓. 처방 표본 0(L162) ✓.
- 통계 키: 거래 `createdTimeUtcFrom/To` · 항목 `createdDateTimeUtcFrom/To` · 카드 이벤트 `chargedDateTimeUtcFrom/To` · `limit` · `cursor`(L69 ~ 71 · L148) ✓.
- 매핑 값: 실측 표본(L123 ~ 125 · L150 ~ 155)과 openapi 값(L127 ~ 129 · L155)을 근거 열에서 나눠 적었다 ✓.
- prod 코드 이름: `mark_absent(within=…)` · `RefIndex.lookup` · `link`(`emr/sync.py` L131 · L146 · L192) · 「앞 회차가 안 끝난 병원은 건너뛴다」(`tasks/emr.py` L11) · `external_ref.external_updated_at`(`models/customer.py` L98)이 prod 에 있다 ✓.
- 지어낸 경로 · 필드: 0.

### 3. 백필

- SPEC-002 에 더한 줄에서 「백필」은 3곳에만 나온다: 개정 노트 · 절 머리 「범위 밖」 · 근거 줄 「8 백필은 범위 밖」. 절차 · 안전 규칙 절은 없다 ✓.
- SPEC-000 OQ-00-3 은 「열린 채 · 담당 별도 · 결정 아님」이다. 메모 7줄이 scope-change 목록과 하나씩 맞는다(판 · 사라짐 · 알림 · 어제까지 · S-8 · flow_log · 인덱스) · Q2 링크 ✓.
- `visit` 인덱스를 더하는 줄은 지웠다(planner 리포트 §2) ✓. 남은 것: W-1(개정 노트의 절 이름).

### 4. 삭제 (변경된 축)

- `spec-002:911` 「**삭제는 소프트 딜리트만 쓴다** … 어떤 경로든 물리 삭제(`DELETE`)는 금지」 ✓. 사라짐 표(L913 ~ 921)는 모든 범위가 `deleted_at` 이거나 「지우지 않음」이다 ✓.
- 더한 줄 전체에서 물리 삭제를 허용하는 문구는 0 이다(`DELETE` 는 금지 문장에만 나옴).
- **되돌림 대상(판정 안 함)** — planner 가 되돌리는 중이다. 지금 스냅샷에서 아래 항목이 남아 있는지 확인했다. 확인한 스냅샷에서는 모두 이미 빠져 있었다. 코디가 최종 diff 에서 한 번 더 보면 된다.
  - SPEC-002 upsert 절의 「지우면 로그를 남긴다」 · `event_log` 칸 표(`record.delete` · `record.restore` · payload 키)
  - §4 DB `event_log.type` 값 목록의 `record.delete` · `record.restore`
  - §5 OQ-76 · OQ-77
  - 개정 ㉔ 노트(L43)와 log.md L17 의 「삭제 로그」 문구(지금 log 행은 「새 OQ-69 ~ 75」)
  - planner 리포트 「삭제 규칙 반영」 절(리포트 파일 · 범위 밖)

### 5. SPEC-000 수정

- 칸 · 타입을 바꾼 곳은 셋이다. 모두 prod 에 없는 새 테이블이고 「2026-11-19 개정」 표시가 있다.
  - `product_option.unit_*` 뺌(결정 6)
  - `product_option_composition.ref_single_option_id` 뺌(결정 7)
  - `purchase.status` · `process` enum 추가(결정 5)
  - prod 52 테이블 목록에 `product_option` · `purchase` 는 없다.
- 설명만 바꾼 곳은 다섯이다. 모두 조사 사실이고 칸 · 타입은 그대로다.
  - `treatment_item` 가격 · 시간 · 간격
  - `etcetera_product_category.id` 외부 열
  - `prepaid_card.id` 외부 열
  - `kind` · `pocket` 외부 열 매핑
  - `product_option.treatment_item_id` 「내부에만」
- §2 「동기화」 행: 주기에 5분 한 마디를 더했다(결정 2) ✓.
- OQ: 00-4 · 041-1 · 10-2 를 닫았다(근거 결정 1 · 2 / 조사 Q1 / 실측 REFUND) · 10-3 은 좁혔다 · 08-9 · 08-10 은 새로 열었다 · 041-2 · 041-3 · 10-5 는 사실만 보탰다(열린 채) ✓.
- `version: 0.0.1` — SPEC-000 · SPEC-002 둘 다 ✓.

### 6. 범위 · 개인정보 · lint

- 바뀐 파일은 `spec-000` · `spec-002` · `erd.md` · `system.md` · `log.md` 이다. 모두 `products/day/` 안이다. SPEC-001 · 003 ~ 005 · WORK · 10-decision 은 0 이다.
- 더한 줄 grep `01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9a-f]{24}` → 0. 테넌트 이름 · id · 고객 · 직원 이름은 없다(「실 명동점」은 지점 구분 글자 · 브리프 결정 10 문구).
- lint `--strict` → `0 error, 263 warning` · `products/day` 0.

## 사용자 판단 (모음)

1. **W-2**: 5분 루프에 구매 항목 통계(새 구매 나열)를 넣는가.
2. **W-3**: 시술 항목 · 기기 · 약물은 공개 메뉴 API 를 원천으로 하는가(내부 경로 없음 · 404).
3. **W-4**: KOS `REFUND` = DAY `revoke` 로 확정하는가(새 enum 값 없음).

## 직원이 실물에서 만날 자리

해당 없음(문서 단계). 구현 때 처음 만날 자리: 지난 구매의 방문이 DAY 에 없을 때 건너뛴 수(OQ-69) · 매핑 밖 값 건너뜀(OQ-70) · 5분 루프 첫 회차 시작 시각(OQ-72).

## 참고(기존 부채)

- 1차 검수와 같다. 원래 있던 개인정보 grep 2건(SPEC-000 데모 작업 id · log.md 2026-11-10 행)이 있다.
- 공개 · 내부 상품 수가 2건 다른 이유는 OQ-75 로 남아 있다.
