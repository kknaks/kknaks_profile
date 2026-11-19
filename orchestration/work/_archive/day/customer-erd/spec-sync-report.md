# customer-erd spec 2차 결과 보고 — KOS → DAY 새 테이블 동기화 (SPEC-002 개정 ㉔ · SPEC-000 칸 수정)

- 작성: day `planner` · 2026-11-19 · task `task_d2fb254fb44b` · dispatch `ctx_9a59a820e7f8`
- 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec` (base `origin/main` = `4585fb59` #951 머지분) — 커밋 · push · PR 안 함

## 상태: done

**범위 변경 반영(사용자 2026-11-19 · `spec-2-scope-change.md`)**: 백필 절차 · 「백필 안전 규칙」 절은 쓰지 않았다(한 번 쓴 뒤 지움). 결정 8 은 결정으로 쓰지 않았다. SPEC-000 OQ-00-3 은 **열린 채**로 두고, 「담당 별도 · 조사로 확인된 주의」 7줄 + 근거 리포트 Q2 만 붙였다.

## 1. 바꾼 파일 · 절

| 파일 | 바꾼 곳 |
|---|---|
| `products/day/20-spec/spec-002-procedure-board.md` | frontmatter(`last_updated` 2026-11-19 · `sources` + 조사 리포트 · version 그대로) · 개정 ㉔ 노트(L43) · **§3 새 절 「KOS 읽기 — 새 테이블 동기화 (개정 ㉔)」 L837 ~ L950** · 「동기화 추가분」 표 L809 한 줄(새 칸 3개 → 개정 ㉔) · §5 새 표 「동기화 (개정 ㉔)」 L1196(OQ-69 ~ 75) |
| `products/day/20-spec/spec-000-data-model.md` | `last_updated` · `sources` · 2026-11-19 개정 노트(L37) · §2 「동기화」 주기에 5분 · §4 공통 줄 · 04-1 「정한 것」 옵션 단위(L1283) · 원천 줄 · 칸 표(`product_option` · 구성 · `treatment_item` · `etcetera_product_category` · `purchase` · `purchase_item` · `prepaid_card` · `prepaid_card_ledger`) · §6 OQ |
| `products/day/40-architecture/erd.md` | 메뉴 관계도 `product_option` 라벨 · 인벤토리 `product_option` 책임(옵션 단위 뺌) · `last_updated` |
| `products/day/40-architecture/system.md` | 「읽기 — 폴링」 표: 기준 정보에 메뉴 · 오늘 구매 10초 · 병원 전체 변경 5분 두 줄 · `last_updated` |
| `products/day/log.md` | 2026-11-19 `spec-change, arch-change` 행 · 최종 수정 |

SPEC-001 · 003 ~ 005 · WORK · 코드 · 10-decision 은 건드리지 않았다.

## 2. 결정 → 줄 대응표

| 결정 | 어디 (파일:줄) |
|---|---|
| 1 오늘 고객 시술권 · 카드 = 바뀐 고객만 | SPEC-002 L862(루프 ③) · L896 「바뀐 것만」 표 · SPEC-000 OQ-00-4 닫음 L1759 |
| 2 오늘 밖 고객 = 공개 거래 · 카드 이벤트 통계 5분 | SPEC-002 L864(⑤ · ⑥) · SPEC-000 §2 「동기화」 · OQ-00-4 닫음 · system.md 폴링 표 |
| 3 원천 = 내부 API · 통계는 id 모으기 | SPEC-002 L847 「원천 고르기」 · L849 · L872 테이블별 원천 |
| 4 시술권 = 내부 `get-ticket-bundles` | SPEC-002 L886 |
| 5 매핑 표 · enum 추가 · 표본 없는 값 OQ · `entity_type` 새 값 | SPEC-002 L925 매핑 표 · `entity_type` 새 값 줄 L939 · SPEC-000 L1536 `paid` · L1537 `revoking` · `prepaid_card_item_substituting` · L1705 `REFUND → revoke` · L1706 `BALANCE` · OQ-08-9 L1809 · OQ-10-3 좁힘 L1828 · SPEC-002 OQ-70 |
| 6 `product_option` 옵션 단위 칸 뺌 · 1차 8 문구 | SPEC-000 L1351(칸 뺌 표시) · L1283(정한 것) · `purchase_item` 용량 변경 · 단위 칸 설명 · erd.md 인벤토리 |
| 7 구성 `ref_single_option_id` 뺌 · `treatment_item` 가격 · 시간 · 간격 유지 + 「KOS 원천 없음」 | SPEC-000 L1378 · L1401 · L1402 |
| 8 백필 | **범위 밖(범위 변경)** — SPEC-000 OQ-00-3 L1750 열림 · 주의 메모 L1751 ~ |
| 9 통계 = id 나열에만 | SPEC-002 L854 · 루프 표 ⑤ · ⑥ 「나열만」 |
| 10 DEMO 테넌트만 | SPEC-002 L944 「환경」 · L947 |

브리프 §4 규칙 ① ~ ⑤(백필 안전 규칙)는 범위 변경으로 **SPEC-002 에 쓰지 않았다**. 사실만 SPEC-000 OQ-00-3 메모로 옮겼다:

| 원래 규칙 · 사실 | OQ-00-3 메모 |
|---|---|
| 판은 오늘 창만 | ✓ |
| 사라짐 처리는 창 안 방문만 | ✓ |
| 동기화는 알림 없음 | ✓ |
| ① 백필 창 어제까지 | ✓ |
| ② S-8 자동 해제가 worker 세션을 끊음 | ✓ |
| ③ flow_log 마지막 단계만 | ✓ |
| ④ `visit (hospital_id, reserved_start_at)` 인덱스 없음 | ✓ (SPEC-000 `visit` 에 넣었던 인덱스 추가 줄은 지웠다 — 백필 몫) |
| ⑤ 호출 간격 · 상한 · 이어 하기 | 5분 루프 몫만 SPEC-002 OQ-72 에 남김 · 백필 몫은 쓰지 않음 |

## 3. SPEC-000 칸 · 타입을 바꾼 곳 (모두 「2026-11-19 개정」 표시 · prod 에 없는 새 테이블만)

| 테이블 | 바꾼 것 |
|---|---|
| `product_option` | `unit_type · unit_value` 뺌 |
| `product_option_composition` | `ref_single_option_id` 뺌 |
| `purchase` | `status` enum + `paid` · `process` enum + `revoking` · `prepaid_card_item_substituting` |
| (설명만) | `treatment_item` 가격 · 시간 · 간격 「KOS 원천 없음 — DAY 원장 뒤 입력」 · `prepaid_card_ledger.kind` · `pocket` 외부 열 매핑 · `etcetera_product_category.id` 「KOS id 옴」 · `prepaid_card.id` 외부 열(`streamId` 는 조회 응답에 없음) · `product_option.treatment_item_id` 「내부 응답에만」 |

prod 테이블 칸 · 타입 변경 0. SPEC-002 의 지금 10초 · 1시간 호출 · 칸 · 사라짐 규칙 변경 0(더하기만).

## 4. OQ 정리

- SPEC-000 닫음: OQ-00-4(주기 · 결정 1 · 2) · OQ-041-1(내부 응답에 `medicalService`) · OQ-10-2(`REFUND` 있음). 좁힘: OQ-10-3(`PAYMENT_CANCEL` · `EXPIRATION` · `SUBTRACT` 만 남음). 사실 보탬: OQ-041-2 · 041-3 · 10-5(표본 1 = 금액에서 먼저 빠짐 · 열린 채). 새: OQ-08-9(`PAID` · `REVOKING` · `…SUBSTITUTING` 뜻) · OQ-08-10(`conversion` · `purchaseMemo` · `migratedDateTimeUtc` 칸).
- **OQ-00-3 열린 채**(범위 변경).
- SPEC-002 새 OQ-69 ~ 75: 방문 없는 구매(기본 = 건너뜀) · 매핑 밖 값(기본 = 건너뜀) · 담당 직원 없는 거래 · 5분 루프 시작 시각 · 상한 · 시각 둘 자리 · 시술권 빠진 번들(기본 = 지우지 않음) · 일정 `updatedDateTimeUtc` 반응 · 처방 표본.

## 5. 조사 · 결정에 없어 이 SPEC 이 붙인 것 (기본값 · 모두 OQ 로 열림)

- 내부 경로가 없는 메뉴 셋(시술 항목 · 기기 · 약물)은 **공개 메뉴 API** 를 원천으로 쓴다. 결정 3 「내부」의 예외이고, 조사 Q1 · Q5 에서 내부 경로가 없거나 404 다. 통계가 아니라 메뉴 목록이다.
- 「바뀐 카드만」 ④(카드 `updatedDateTimeUtc` 비교)는 조사 Q4 표의 「카드가 바뀌었을 때」 줄 그대로다.
- 5분 루프에서 구매가 바뀐 고객도 ③(시술권 · 카드)을 부른다. 결정 1 의 「구매가 바뀐 고객」 규칙을 오늘 밖 고객에도 같게 쓴 것이다.
- OQ-69 · 70 · 73 의 기본값 「건너뛰어 센다 / 지우지 않는다」는 「동기화 추가분」의 추정 금지 원칙을 따랐다. 사용자 결정은 아니다.
- 메뉴 = 기준 정보 1시간. 조사 Q4 표 그대로이고, OQ-00-4 가 사용자 결정으로 닫혀 같이 적었다.

## 6. 영향 (범위 밖 · 건드리지 않음)

- 구현(CENTURION_DAY): `tasks/emr.py` 에 5분 루프 · `sync.py` 에 새 적용 함수 · 메뉴 동기화 · `external_ref.entity_type` 새 값 · migration(새 테이블 28 · `visit_task` 3칸).
- 백필 담당: SPEC-000 OQ-00-3 메모 · 조사 Q2.
- SPEC-001 S-8: 백필을 별도 프로세스로 돌릴 때만 영향이 있다(메모에만 적음).

## 7. 검증

- lint `python3 scripts/lint-pipeline.py --strict` → `0 error, 263 warning` · `products/day` 줄 **0**. 263 WARN 은 모두 다른 제품의 것이고 **무관**하다(작업 전과 같음).
- 개인정보 grep `01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9a-f]{24}` 를 이번에 더한 줄(`git diff -U0 | grep '^+'`)에 돌림 → **0건**. 테넌트 · 고객 · 구매 · 카드 id 값 · 이름은 옮기지 않았다. 문서에는 경로 · 키 이름 · 건수만 있다.
- version 은 두 SPEC 모두 `0.0.1` 그대로다.

## 삭제 규칙 반영 (사용자 2026-11-19 · `spec-2-delete-log.md`)

- SPEC-002 「upsert · 사라짐 · 삭제」에 두 원칙을 넣었다. 하나는 「삭제는 소프트 딜리트만 · 물리 `DELETE` 금지」(L920 부근)다. 다른 하나는 「새 테이블에서 지우거나 되살릴 때마다 `event_log` 한 줄」(L923 ~)이다.
- 로그 대상 경로는 셋이다: KOS `deleted:true` · 응답에서 사라짐 · DAY 동작(환불 회수). 되살림에도 로그를 남긴다.
- `event_log` 칸 표를 넣었다(칸 추가 없음). `type` = `record.delete` · `record.restore` 이고 `대상.동작` 관례를 따랐다. `actor_staff_id` 는 동기화면 NULL 이다. `visit_id` 는 구매 · 처방 계열만 채운다. `payload` 키는 `entity_type` · `entity_id` · `source` · `reason` · KOS 시각이다.
- §4 DB 의 `event_log.type` 값 목록(L1152)에 두 값을 더했다. SPEC-000 05 `event_log.type` 은 예시만 있고 목록이 아니라 그대로 뒀다.
- 새 OQ 둘: OQ-76(지금 테이블의 사라짐에도 로그를 붙일지 · 이번 범위 아님) · OQ-77(대량 삭제를 한 줄로 묶을지 · 기본값 = 행마다 한 줄). 개정 ㉔ 노트 · log.md 행도 맞췄다.
- 다시 검증: lint `--strict` `0 error, 263 warning` · `products/day` 줄 0 · 더한 줄 개인정보 grep 0.

## 삭제 로그 되돌림 (사용자 2026-11-19 · `spec-2-delete-log-revert.md`)

- 「로그는 다른 데서 남긴다」에 따라 위 「삭제 규칙 반영」의 **로그 부분을 뺐다**. 뺀 것은 넷이다: `event_log` `record.delete` · `record.restore` · `event_log` 칸 표 · §4 DB `event_log.type` 목록에 더한 두 값 · OQ-76 · 77. 두 OQ 는 머지 전 미커밋 추가분이라 번호를 남기지 않고 지웠다(OQ 는 69 ~ 75 로 끝남).
- 남긴 것: 「삭제는 소프트 딜리트(`deleted_at`)만 · 어떤 경로든 물리 `DELETE` 금지」 원칙 한 줄. 사라짐은 기존대로 `deleted_at` + `is_present_in_source = false` 다. 개정 ㉔ 노트 · log.md 행도 맞췄다. SPEC-000 `event_log` 설명은 처음부터 바꾸지 않았다.
- 다시 검증: lint `--strict` `0 error, 263 warning` · `products/day` 줄 0 · `record.delete` · `OQ-76` · `OQ-77` grep 0.

## 메뉴 키 보강 + 유일 1개 (사용자 2026-11-19 · `menu-keys-addition.md`)

- SPEC-000 §4 칸 표에 11칸을 「2026-11-19 추가」로 넣었다. 모두 nullable 이고 외부(KOS) 열을 채웠다.
  - `treatment.search_phonetic_name` · `registered_at`(createDate)
  - `machine` · `medicine` `search_phonetic_name`
  - `product.cautions`(text[] · `caution` 그대로 · 그 행의 외부 열은 `caution` 으로 좁힘) · `target_country_codes`(varchar[]) · `medicine_and_machine_names`(varchar[])
  - `product_option` · `product_option_composition` `medicine_and_machine_names`
  - `treatment_item.drafted_at`(그 표 `created_at · updated_at` 의 외부 열에서 drafted 를 뺌)
  - `prepaid_card_product.translations`(jsonb)
- 칸 이름 · 타입은 지시 그대로다. 관례(`badges` varchar[] · `visit_task.medicines` varchar[] · `translations` jsonb)와 맞아 바꾼 것은 없다.
- `treatment.category_ids` 는 「칸으로 두지 않는다」로 표시했다(OQ-041-3 에 한 줄).
- `ticket_bundle.purchase_item_id` 에 부분 유일(`WHERE deleted_at IS NULL`)을 적었다. erd.md 인벤토리 핵심 키도 맞췄다.
- 새 OQ-09-3: 남은 1 : 0..1 셋(`prepaid_card.purchase_item_id` · `visit_task.ticket_id` · `prepaid_card_ledger.purchase_transaction_id`)은 걸지 않는다. 근거는 review-code-1 §5 다.
- SPEC-002 ㉔ upsert 표 「시술권」 줄에 「옛 번들 삭제 표시 → 새 번들 생성」 순서 고정 한 줄을 넣었다. SPEC-000 2026-11-19 개정 노트도 맞췄다.
- 검증: lint `--strict` `0 error, 263 warning` · `products/day` 줄 0 · 더한 줄 개인정보 grep 0 · 커밋 없음.

## 실물 발견 반영 (사용자 2026-11-19 · `sync-fix-1.md`)

| # | 반영 |
|---|---|
| F-1 | SPEC-000 `prepaid_card_ledger.id`: 외부 id = `chargingId:주머니` · 거래 연결은 원래 `chargingId`. SPEC-002 ㉔: entity 줄 · 사라짐 표 「카드 이력」 |
| F-2 | SPEC-000 `product_option_composition.title`: 필수 → **NULL 허용**(2026-11-19 개정 · 추정 금지 · 구성은 씀) |
| F-3 | SPEC-000 `ticket.status`: `canceled` 추가 · 정한 것 문구. SPEC-002 ㉔ 매핑 표: `CANCELED` → `canceled` |
| F-4 | SPEC-000 08 정한 것 · `purchase_item.purchase_id` · `id` 외부 열: `pendingItems[]` 도 `purchase_item` 으로 · 확정 시 같은 id upsert(id 가 바뀌면 소프트 딜리트). SPEC-002 ㉔ 원천 표 구매 줄 |
| F-5 | SPEC-002 ㉔ 원천 표 `prepaid_card_product`: `{closed:false}` · `{closed:true}` 두 번 · `is_closed` 는 응답 값 |

- 그대로 둔 것 셋을 OQ · 메모로 적었다.
  - OQ-08-4: 가격 조정 「표본 1건 생김」.
  - OQ-00-3 메모: 출처 항목 없는 지난 구매의 번들은 건너뜀 · 백필 몫.
  - 새 OQ-041-8: 시술 항목 가격 · 시간 · 간격이 공개 openapi 에는 있다 · 결정 그대로.
- 개정 노트(SPEC-000 2026-11-19 · SPEC-002 ㉔)를 맞췄다.
- 검증: lint `--strict` `0 error, 263 warning` · `products/day` 줄 0 · 더한 줄 개인정보 grep 0 · 커밋 없음.

## 검수 3 반영 (코디 2026-11-19 · `sync-fix-2.md`)

- SPEC-002 ㉔ 를 네 곳 고쳤다.
  - 「바뀐 것만」 표: 「DAY 에 없는 티켓 포함」 뒤에 「단 한 번 받아도 풀리지 않은 티켓(출처 구매 항목 없음 · 백필 몫)은 그날 다시 부르지 않는다」를 붙였다.
  - 루프 표 아래: 오늘 구매 회차(② ~ ④)는 일정 회차 뒤 별도 태스크다. 같은 일정 응답을 입력으로 넘겨 KOS 호출은 늘지 않는다.
  - ⑥: 나열된 카드 id 로 ④ 를 직접 부른다(카드 요약은 소유자 ③).
  - 「지난 회차 시각」: 장 수 상한에 걸리면 받은 마지막 행 시각까지 부분 전진한다.
- 개정 ㉔ 노트도 맞췄다.
- 검증: lint `--strict` `0 error, 263 warning` · `products/day` 줄 0 · 개인정보 0 · 커밋 없음.

## 내부 API 만 반영 (사용자 2026-11-19 「공개 api 비싸」 · 「지금 우리 코드에서도 공개 안 쓰고 내부로만」 · `sync-fix-3-internal-only.md` + 「추가」)

- **원칙 한 줄**: 「DAY 운영 동기화는 공개 API(open)를 쓰지 않는다(비용)」. 넣은 곳 셋:
  - SPEC-000 §2 「동기화」
  - SPEC-002 ㉔ 「원천 고르기」
  - system.md 외부 시스템 표
  - 데모 시드 도구(`emr/kos/demo/`)만 예외다.
- **구역 목록**: 운영 루프의 유일한 공개 호출이었다. 이제 내부 `schedule/zone/v1/queries/get-zones` 로 받는다(SPEC-002 ㉔). 운영 경로에서 공개 토큰을 받지 않는다.
  - `open_api_key` 는 연결 설정에 필수 그대로 두었다. 새 SPEC-000 OQ-01-4 로 남겼고, 같은 칸 설명에 「운영 동기화는 쓰지 않음」을 적었다.
- **SPEC-002 ㉔ 메뉴**: 진료항목 · 약품 · 기기 원천이 ~~공개 `get-medical-services` · `get-machines` · `get-medicines`~~ → 내부 `get-products` 안 옵션 · 구성 `medicalService`(+ `machines[]` · `medicines[]` · `procedure`)에서 모으고 id 로 중복을 뺀다.
  - 「옵션에서 빠짐 ≠ 삭제」: 이 세 테이블은 사라짐 소프트 딜리트를 적용하지 않는다. 원천 표 아래 줄 · upsert 표 「메뉴」 줄에 적었다.
- **SPEC-002 ㉔ 5분 회차 뺌**:
  - 루프 표 행 · 「지난 회차 시각」 줄 · 「바뀐 것만」 「오늘 밖 고객」 줄은 취소선으로 남기고 「2026-11-19 뒤집음 — 공개 API 비용」을 달았다.
  - 결정 2 · 9 와 결정 3 의 공개 메뉴 부분도 같게 뒤집음 표시를 했다.
  - OQ-69 · 72 = 해당 없음. OQ-74 에서 5분 부분은 취소선으로 남겼다.
  - **새 OQ-76** = 오늘 밖 고객의 변경. 후보는 내부 `get-visitors` 하루 한 번 훑기다.
- **SPEC-000 OQ-00-4 다시 엶**: 오늘 고객 · 메뉴 주기는 그대로 정해져 있다. 「오늘 밖 고객」만 다시 열었다(이전 닫음 문구는 취소선).
  - §2 「동기화」의 5분은 취소선으로 남겼다.
  - system.md 폴링 표 5분 행도 취소선으로 남겼다.
  - 개정 노트를 맞췄다.
- 검증: lint `--strict` `0 error, 263 warning` · `products/day` 줄 0 · 더한 줄 개인정보 0 · 커밋 없음.
