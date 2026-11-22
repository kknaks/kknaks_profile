# 리뷰 리포트 — day-cc-mig / doc — DAY-SPEC-000 §4A 「KOS 키 보충」 (2026-11-20)

대상: 워크트리 `mediness-mediness/day-cc-mig-spec` 미커밋 diff — `products/day/20-spec/spec-000-data-model.md`(+598/-32) · `40-architecture/erd.md` · `log.md`. 줄 번호는 지금 워킹트리 기준.
대조 원천: `_RESUME.md` §2 2026-11-20 행 · 2차 리포트 K3-2 · K2 · 3차 리포트 N3 · N4 · N7 · planner 브리프 §6 · §7 · `day.json` `data_rules` · CENTURION_DAY `origin/prod` `a6aa4ba5` · `origin/dev` `844eace4` 모델.

## 판정: FAIL — FAIL 2 · WARN 5

| 2절 항목 | 결과 |
|---|---|
| 1 반영 누락 0 | **PASS** — 632 = 630 + 뺀 2(OQ-4A-4 예약 태그 · OQ-4A-6 업무 종류 id), 테이블별 수가 리포트 K3-2 · N7-2 와 같다. 일부러 안 둠 196행 = 180 + 뺀 16(`categoryIds[]` 2차 12 · 3차 4 · OQ-4A-5) · 예약 규칙 26 = 25 + `zoneIds[]` 1. 뺀 사유는 모두 리포트상 값 0 또는 목록 경로 없음이라 정당하다. 키 단위로 다시 세 보니 K3-2 키 목록 514줄 전부가 §4A 에 있다(요일 키 5개는 `monday ~ sunday` 로 묶임). 무작위 20키를 거꾸로 따라가도 20/20 칸이 있다(아래 부록) |
| 2 prod 불변 | **PASS(WARN 1)** — prod 칸 이름 · 타입 변경 0. 새 칸은 모두 NULL 허용. 「prod 있음」 9표 · 「dev 에만」 15표 · 새 표 12개를 prod · dev 모델에서 직접 열어 확인했고 모두 맞다. 새 칸 이름이 기존 칸과 겹치는 곳도 0. 문장 하나만 틀렸다(W4) |
| 3 data_rules | **FAIL 1 · WARN 1** — enum 자리에 KOS 문자열을 그대로 둔 칸들이 SPEC 자기 규칙과 부딪힌다(F2). `tenant_info` 안 KOS `hospitalId`(W1). 시각 UTC · 암호화 · 연결 표(목록 금지) · KOS id → DAY FK 는 지켰다 |
| 4 시점 구분 | **PASS(WARN 1)** — 일정 상담 정보 ≠ 상담 기록, 산 시점 정가 ≠ 결제 금액, 고객 `is_new` ≠ 방문 `is_new`, 사본 총액 ≠ 계산 총액을 다른 칸으로 나눴다. 다만 한 칸에 KOS 경로 두 개가 들어간 곳이 있다(W2) |
| 5 planner 리뷰 요청 | ① **FAIL**(F1 — 뒤집은 결정이 본문 3곳에 안 고쳐짐) ② **WARN**(W1) ③ PASS(참고 R1) ④ **FAIL**(F1). S0:278 · 311-317 · 360 · 510 · 611 · 892 · 1429 · 1668 · 1698 은 일관되게 고쳐졌다 |
| 6 지어낸 것 | **PASS** — `PLATFORM` · `EASY_PAY` 같은 문자열 0건. 앱 결제 · 간편결제는 OQ-4A-1 로 열어 두었다. 휴무 모양은 cc 근거라고 밝히고 OQ-4A-2 로 열었다. 리포트에 없는 칸 0 |
| 7 범위 밖 침범 | **PASS** — 타이머 · 리액션 · 문진 · 수납(결제 설정) · 예약 칸 · 칸 점유 표 · ext 계약 · 코드 모두 0. 예약 규칙 표 3개는 브리프 §6-3 지시대로 만든 것이다 |
| lint | `python3 scripts/lint-pipeline.py --strict` → exit 0 · 전체 0 error / 263 warning · **products/day/ 0 error · 0 warning**(나머지 263 은 타 제품 — 무관) |

## FAIL

### F1. `visit.reservation_group_id` 를 뒤집었는데 본문 3곳은 아직 「두지 않는다」고 쓴다 (2절 5 ① · ④)

- 고친 곳: `spec-000-data-model.md:1010`(06 「다른 곳으로」 표) · `:2010`(§4A.3 — 「§3 06 「visit.reservation_group_id 두지 않음」 뒤집음」).
- **안 고친 곳**:
  - `spec-000-data-model.md:605` — 「3번에서 미룬 예약 그룹(`reservation_group_id`)은 06 에서 정함 — `visit` 에 두지 않고 `visit_occupied_resource` 로.」
  - `spec-000-data-model.md:912-913` — 「그래서 `visit.reservation_group_id` 를 두지 않고 **`visit_occupied_resource`** …로 둔다.」 §4A.3 이 뒤집었다고 가리키는 바로 그 줄이다.
  - `spec-000-data-model.md:2311` — OQ 03 「(해결) … `visit` 에 두지 않고 `visit_occupied_resource` 로.」
- 근거: 브리프 §6-1 「뒤집은 원래 줄은 본문에서 고치고 변경 이력에 남긴다」 · §4A 공통 `:1773` 「뒤집은 원래 줄은 본문에서 고쳤다(취소선 + 이 절 링크)」 · rules.md 「닫힌 것을 다시 연 곳」. stable SPEC 안에서 같은 칸을 두고 「둔다」와 「두지 않는다」가 함께 있어, 구현 워커가 추측으로 골라야 한다.
- 고칠 방향: 세 줄에 취소선을 긋고 「2026-11-20 — KOS 예약 단위 사본은 `visit.reservation_group_id · reservation_zone_id`(§4A.3 · OQ-4A-7). 점유는 그대로 `visit_occupied_resource`」 한 줄을 단다.

### F2. enum 자리에 KOS 문자열을 그대로 두어 SPEC 자기 규칙과 부딪힌다 (2절 3)

- 규칙: `spec-000-data-model.md:97` 「상태 · 종류 enum 은 **DAY 말**이고 KOS 문자열은 「외부(KOS)」 열 · 동기화 매핑에만 둔다」 · `:1241` 같은 말 · 브리프 §1 data_rules 요약 「enum 은 DAY 말」.
- §4A 에서 상태 · 종류 칸을 `varchar`「KOS 값 그대로」로 둔 곳:
  - `:2097` `visit_etc_work.status`(`WAITING` · `COMPLETED`)
  - `:2083` `visit_task.urgency_level`(`URGENCY_LEVEL_UNSPECIFIED`)
  - `:2025` `visit_requested_procedure.price_reason`(`GENERAL`)
  - `:1917-1919` `reservation_rule.requested_procedure_repetition` · `occupancy_policy` · `zone_occupancy_policy`
  - `:1943` `reservation_rule_event.event_type`
  - `:1932` 구성 `requested_procedure_repetition`
  - TI 묶음 `:1796` `treatment_item_status` — 같은 값의 원본 `treatment_item.status` 는 `enum` 인데(`:1411`) 스냅샷만 `varchar` 다
- OQ-4A-9(`:2391`)가 「DAY enum 으로 바꾸려면 값 목록이 필요」라고 열어 둔 것은 맞다. 그러나 규칙의 예외라는 말이 §1 · §2 · §4A 공통 어디에도 없다. 그래서 「enum 은 DAY 말」과 「KOS 값 그대로」가 같은 SPEC 에 둘 다 서 있고, KOS 를 떼면 업무 표에 KOS 낱말이 남는다(§2 「외부 CRM 흔적」의 취지와 반대).
- 고칠 방향: §4A 공통에 「값 목록 미관찰 상태 칸은 KOS 문자열 임시 저장 — DAY enum 전환은 OQ-4A-9」 예외를 사용자 확인을 받아 적거나, 관찰된 값은 지금 DAY enum(소문자)으로 매핑하고 모르는 값을 어떻게 처리할지 정한다.

## WARN

### W1. `crm_connection.tenant_info` — KOS `hospitalId` 가 `external_ref` 밖에 있다 (2절 5 ② · 3)

- `spec-000-data-model.md:1859` — `tenant_info` jsonb `{hospitalId, hospitalCode, hospitalNationality, mode, namespace}`.
- 사용자 결정(`_RESUME.md:57` 「병원 정보는 `hospital` 에 · 병원 = KOS 테넌트」)과 비교: 병원 정보인 P25 14키와 P22 `hospitalName` 은 `hospital` 에 붙였으니 결정과 맞다. `mode` · `namespace` · `hospitalCode` 처럼 KOS 에서만 뜻이 있는 값을 KOS 를 떼면 함께 지우는 `crm_connection` 에 둔 것도 §2 `:143` 와 `config.tenant_id` 선례(prod `hospital.py:26-27`)에 비춰 받아들일 수 있다.
- 그러나 `hospitalId` 는 KOS 가 병원에 붙인 **외부 id** 다. data_rules 「외부 id 는 external_ref 한 테이블에만(entity_type + entity_id)」을 글자 그대로 따르면 `external_ref(entity_type = hospital)` 에 있어야 한다. `hospitalNationality` 도 병원 속성이라 OQ-4A-8 결론에 따라 `hospital.nationality` 와 합칠 후보다.
- 고칠 방향: `hospitalId` 는 `external_ref`(hospital)로 옮기거나, 「테넌트 정보 jsonb 안의 KOS id」를 §2 예외로 적어 사용자 확인을 받는다.

### W2. 한 칸에 KOS 경로 두 개 — `treatment_id` 가 TI 묶음과 따로 적은 칸 양쪽에서 정의된다 (2절 4)

- TI 묶음 `:1804` `treatment_id` ← `medicalService.configuration.procedure.id`. 같은 표에 `treatment_id · treatment_name` 을 다른 경로로 또 적었다:
  - `purchase_item` `:2149`(`optionConfiguration.procedure.{id,name}`)
  - `purchase_item_composition` `:2174`(`.procedure.{id,name}`)
  - `ticket_set` `:2201`(`ticketSets[].procedure.{id,name}`)
- 두 경로가 늘 같은 값인지는 리포트에 없다. 다르면 어느 쪽이 이기는지 매퍼가 추측해야 하고, 시점이 다른 값이 한 칸에 섞일 수 있다.
- 고칠 방향: 한 칸 · 한 원천으로 정하고(다른 쪽은 「같은 값 — 확인은 첫 실값」) 다르게 나오면 OQ 로 둔다.

### W3. 고객 `created_at` 과 `registered_at` 의 원천이 모호하다

- §2 새 규칙(`:150`): 「연동 기간에 외부에서 받은 행은 `created_at` = 외부 생성 시각(`createdDateTimeUtc`)」. 그런데 §4A.2 `:1965` 는 고객 `createdDateTimeUtc` → `registered_at` 만 적었다. 고객 `created_at` 도 같은 키로 덮는지 적혀 있지 않다(덮으면 두 칸이 늘 같은 값).
- 고칠 방향: 고객 행에서 `created_at` 을 규칙에서 빼는지 · 같은 키를 두 칸에 받는지 한 줄로 적는다.

### W4. 「prod 칸」 표시 하나가 틀렸다 (2절 2)

- `:1814` 「이름 배열 칸(`visit_task.medicines · machines` · `…medicine_and_machine_names`)은 그대로 둔다(**prod 칸** · 표시용)」.
- 실제: `visit_task.machines`(dev `task.py:96`) · `medicine_and_machine_names`(dev `menu.py` product · option · composition)는 **dev 에만** 있다. prod `task.py` `VisitTask` 에는 `medicines` 만 있다.
- 고칠 방향: 「`medicines` = prod · 나머지 = dev 에만(2026-11-18 · 11-19)」.

### W5. 사본 「수정 시각」 칸 두 개 — data_rules 「동기화 칸은 external_ref 에만」과 경계에 있다

- `:1802` TI `treatment_item_revised_at` ← `.updatedDateTimeUtc` · `:2188` `purchase_transaction.payment_updated_at` ← `paymentDateTime.lastUpdatedDateTimeUtc`.
- planner 가 「스냅샷 값 · 동기화 칸 아님」이라고 적어 뜻은 갈라 두었다. 다만 이름 · 원천이 `external_updated_at` 과 같은 종류여서 구현에서 바뀐 것을 가려내는 데 쓰일 위험이 있다. 결정이 필요한 것은 아니고, 칸 설명을 지금처럼 유지하면 된다(코드 검수 때 확인).

## 직원이 실물에서 만날 자리

- 없음 — 이번 개정은 칸 · 표만 정한다(화면 · 입력 기능 없음 · `:1761`). F1 이 그대로 남으면 예약 현황 작업 때 어느 그룹 칸을 볼지 헷갈린다(OQ-4A-7).

## 참고(기존 부채 · 판단 기록)

- **R1 `medicine_machine_ref`(owner_type + owner_id)** — §2 「목록」(JSON 에 id 목록 금지 · 연결 테이블)을 지키는 방법이고 `external_ref` 와 같은 다형 참조라 규칙 위반은 아니다. 다만 FK 가 없어 부모 소프트 딜리트가 따라오지 않는다. 9개 owner 표의 정합은 매퍼 · 코드 검수에서 본다. dev 에는 이미 `treatment_item_machine` · `treatment_item_medicine` 연결 표가 있다 — 지금 메뉴의 시술 항목 쪽은 그 표, 스냅샷 · 상품 쪽은 새 표로 두 갈래다(의도라면 그대로).
- **R2 3차 N6 「고객 선불 잔액」 2키(`remainingBalance.balance.currency` · `remainingPoint.balance.currency`)** — 수납 경로라 범위 밖으로 뺐다. 같은 값은 P17 카드 단위 `prepaid_card.balance_currency` · `point_currency`(`:2213`)로 이미 받으므로 빠진 칸은 없다.
- **R3 N7-3 병원 결제 설정 33키** — 범위 밖. `_RESUME.md:22` 「다음 작업으로 넘김 … 결제 설정 저장 N8-6」 · `:55` 와 맞다.
- **R4 4A.10 대조표 표기** — `「일부러 안 둠」 2차 54행 | 54 | 42 | 12(`categoryIds[]` 6경로…)` 의 「6경로」와 아래 내역 「`categoryIds[]` 12」는 행 · 경로를 다르게 센 것이다. 수 자체(12)는 맞는다.
- **R5 erd.md** — 새 표 12개 · 인벤토리 80 → 92 · 「prod 9개 · dev 에만 15개」는 SPEC 과 같다. `log.md` 2026-11-20 행의 수(632 / 630 · 196 / 180 · 16)도 §4A.10 과 같다.

## 부록 — 무작위 20키 역추적 (2차 K3-2 키 목록 514줄 · seed 20261120)

| 리포트 키 | SPEC 칸 |
|---|---|
| P25 `translsMap` | `hospital.translations` `:1846` |
| P26 `wednesday.startTime` | `hospital_operation_timetable.start_time` `:1869` |
| `foreignRegistrationNumber` | `customer.foreign_registration_number`(암호화 · 동기화로 채움) `:1959` |
| `items[].optionConfiguration.compositions[].price` | `purchase_item_composition.price_*` `:2171` |
| `pendingItems[].optionConfiguration.price.value` | `purchase_item.option_price_amount` `:2148` |
| `etceteraWorks[].assignees[].role.roleTags[]` | `visit_etc_work_staff` → `staff` · `job_role.tags`(prod `staff.py` 확인) `:2108` |
| `pendingItems[].etceteraConfiguration.price.value` | `purchase_item.etcetera_price_amount` `:2157` |
| `etceteraWorks[].memo` | `visit_etc_work.memo` `:2098` |
| `pendingItems[]…medicalService.translsMap.title…` | TI `treatment_item_translations` `:1800` |
| `pendingItems[]…medicalService.description` | TI `treatment_item_description` `:1795` |
| `ticketSets[].medicalService.configuration.code` | `ticket_set` TI `treatment_item_code` `:2200` |
| `items[]…compositions[].price.suppliedAmount` | `purchase_item_composition.supplied_amount` `:2171` |
| `options[].compositions[].medicineAndMachines[].id` | `medicine_machine_ref`(owner `product_option_composition`) `:2120` |
| P26 `thursday.breaktime` | `hospital_operation_timetable.break_start · break_end` `:1870` |
| `ticketSets[].medicalService.translsMap.title…` | `ticket_set` TI `treatment_item_translations` `:2200` |
| `pendingItems[].prepaidCardConfiguration.point.currency` | `purchase_item.prepaid_point_currency` `:2154` |
| `passportSurname` | `customer.passport_surname`(동기화로 채움) `:1958` |
| `items[].prepaidCardConfiguration.expirationDurationInDays` | `purchase_item.prepaid_expiration_days` `:2155` |
| `items[]…medicalService.configuration.procedure.id` | TI `treatment_id` `:1804`(W2 겹침) |
| `pendingItems[]…medicalService.configuration.medicines[].id` | `medicine_machine_ref`(owner `purchase_item`) `:1807` |

20/20 반영. 3차 N3 「일부러 안 둠」 142행(희망 시술)도 경로를 하나씩 대조했다. TI 묶음 · `medicine_machine_ref` · `visit_requested_procedure_composition` · `price_reason` 으로 모두 받고, 남은 것은 `categoryIds[]` 4행뿐이다.

---

## 재검수 2 (2026-11-20 — planner 고침 1 반영본 · 같은 워크트리 미커밋 diff)

### 판정: PASS — FAIL 0 · WARN 0 (참고 2)

| 항목 | 결과 | 근거 |
|---|---|---|
| F1 `visit.reservation_group_id` 본문 모순 | **닫힘** | `:605` · `:914` · `:987`(점유 자원 `id` 설명 — 지난번 놓친 줄도 고침) · OQ 03 `:2315` 에 취소선과 「2026-11-20 — KOS 예약 단위 사본 … (§4A.3 · OQ-4A-7)」을 달았다. `reservation_group_id` 줄 가운데 취소선 밖에서 「두지 않」는다고 쓴 줄은 0이다. 남은 `:2013` 은 「뒤집음」 표시라 맞다 |
| F2 enum 규칙 충돌 | **닫힘** | §4A 공통 `:1780` 「enum 은 DAY 말 · 이 절에 예외 없음 · 목록 밖 값 = 행 유지 · 그 칸만 null + 동기화 경고」(사용자 승인 코디 추천과 같음). 바꾼 칸: `urgency_level` `unspecified` · 기타 업무 `status` `waiting · completed` · `price_reason` `general` · `occupancy_policy` · `zone_occupancy_policy`(관찰 값 소문자) · `requested_procedure_repetition`(규칙 · 구성) · `event_type`(값 미관찰 enum) · TI `treatment_item_status` = `treatment_item.status` 와 같은 enum. KOS 문자열은 「외부(KOS)」 열 매핑에만 있다. §4A 를 grep 했을 때 상태 · 종류 꼴인데 `varchar`「KOS 값 그대로」인 칸은 0이다. 남은 「KOS 값 그대로」는 이름 · 주소 · 통화 코드 · 금액 · 시각 같은 값 칸이라 규칙 대상이 아니다. OQ-4A-9 `:2391` 을 「관찰 값 밖 = enum 값 추가 마이그레이션」으로 고쳤다 |
| W1 `hospitalId` | **닫힘** | `:1862` → `external_ref(entity_type = hospital)` · `entity_type` 새 값 목록 `:2004` 에 `hospital` 을 더했다. `tenant_info` `:1859` 는 `{hospitalCode, hospitalNationality, mode, namespace}` 로 KOS id 0. `hospitalNationality` 를 합칠지는 OQ-4A-8 에 조건(같은 값이면 `hospital.nationality` 하나로)과 함께 적었다. 대조표 `:2236` 의 수 19 = 14 + 1 + 4 로 맞다 |
| W2 `treatment_id` 두 경로 | **닫힘** | TI `:1804` 「원천은 이 경로 하나」. `purchase_item` · `purchase_item_composition` · `ticket_set` 의 따로 적은 `treatment_id · treatment_name` 칸을 지우고 「확인용 경로」 행으로 바꿨다. 새 OQ-4A-15 를 두었다. `visit_task` `:2077` 은 TI 묶음을 쓰지 않는 표라 원천이 하나뿐이어서 해당 없다 |
| W3 고객 `created_at` · `registered_at` | **닫힘** | `:1968` 「두 칸 같은 값 — `created_at` 은 §2 규칙 · `registered_at` 은 prod 칸이라 남김」 |
| W4 「prod 칸」 표시 | **닫힘** | `:1817` `medicines` = prod · `machines`(11-18) · `…medicine_and_machine_names`(11-19) = dev 에만. dev `task.py:96` · `menu.py` 와 같다 |
| W5 | 그대로(설명 유지 — 지시대로) | — |
| 새로 깬 것 | **없음** | ① 바뀐 파일은 SPEC 1개뿐(erd.md · log.md 는 1차와 같음). prod 칸 이름 · 타입 변경 0이고, 새 enum 칸은 모두 NULL 허용이라 「그 칸만 null」 규칙과 부딪히지 않는다. ② 다른 절과의 모순 0 — §1 `:97` · §4 `:1241` 「enum 은 DAY 말」과 §4A 공통이 이제 같은 말을 한다. 머리말 개정 노트에 「같은 날 검수 고침 1」을 더했다. ③ `lint-pipeline.py --strict` exit 0 · 전체 0 error / 263 warning · **products/day/ 0 error · 0 warning**(263 은 타 제품 — 무관) |

### 참고 (막지 않음)

- **R6** — 값을 하나도 못 본 enum 두 칸(`requested_procedure_repetition` · `event_type`)은 enum 값을 더하는 마이그레이션 전까지 늘 null 이다. 그동안 KOS 원래 값은 어디에도 남지 않는다. 이렇게 되는 것은 사용자가 승인한 정책 때문이다. 코드 단계에서 「동기화 경고」에 KOS 원래 문자열을 함께 남겨야 나중에 마이그레이션 때 값 목록을 만들고 채울 수 있다(코드 검수 때 확인).
- **R7** — §4A 공통 `:1775` 의 「예외: KOS 테넌트 정보는 … `crm_connection` 에」는 `tenant_info` 에서 KOS id 가 빠진 뒤로 「예외」라는 말이 조금 낡았다. 뜻은 틀리지 않아 고치지 않아도 된다.
