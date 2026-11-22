# 조사 리포트 3차 — 새 HAR 7개로 「확인 안 됨」 메우기 · 예약 현황 · 병원 설정 · 수납 경로 대조

- 작성: day `researcher` · 2026-11-20 · 조사만(판단 없음 — 판단은 N8 「정할 것」)
- 앞 판: 1차 `research-cc-ext-report.md` · 2차 `research-kos-keys-report.md`(이하 「2차」) — **판정 기준 · 표 형식 · 부록 A 스크립트를 2차 그대로 썼다**(2차 `rules.py` 를 고치지 않고 불러 씀 · 새로 판정한 행만 손 규칙 — 부록 A).
- 원천: `reference/2026-11-20-day-cc-mig/har/*.har` **7개**(`ls | wc -l` → 7) — 파일 그대로 읽기만(이동 · 복사 · 수정 · 사본 0).
- 읽은 ref(전부 read-only):
  - CENTURION_DAY `origin/dev` = **`844eace4`**(`git fetch origin dev` 뒤에도 같음) — `backend/day/`
  - mediness-mediness `origin/main` = **`ccede286`**(2차와 같음) — `products/day/20-spec/spec-000-data-model.md`(= `S0:줄`)
  - cc-prototype `origin/main` = **`0553173`** — `procedure/back/app/`(N5 대조)
  - 2차 HAR 67개(`/Users/kknaks/git/toy_pr2/kknaks_profile/reference/`) — 「2차 합집합」 다시 만들기 · N6-1 `pages[]` 에만
- 근거 표기: 코드 = `backend/day/` 아래 경로:줄(위 sha) · cc = `cc:파일:줄`(위 sha) · 문서 = `S0:줄` · HAR = `파일#엔트리`(0부터 · 3차 파일은 폴더 생략).
- **값 0**: HAR 값은 한 글자도 옮기지 않았다 — 키 경로 · 타입 · 모양 · KOS 코드 enum 만. 요청 헤더는 N6-1 지시대로 **`Referer` 하나만** 읽고 호스트 + 경로만 남겼다(Authorization · Cookie 는 읽지 않음). 요청 본문은 **키 이름과 날짜의 캡처일 기준 상대 일수(`D+n`)만** 봤다. KOS · DAY 서버 실호출 0.
- 범위에서 뺀 것(사용자 11-20): 시술 타이머 `taskTimers[]` · 리액션 `reactions[]` = **「사용 안 함(사용자)」**(대조 안 함) · 로그인 세션(`get-active-sign-ins`) · 결제 승인(데모 불가).

## 0. 요약

| 항목 | 값 |
|---|---|
| N1 경로 | 새 HAR 읽기 경로 **58**(엔트리 347 · 200+JSON 283 · OPTIONS 61 · 400 3) = 2차 **P 21** · 2차 **K1-2 30** · **새 경로 7** · 쓰기 경로 11(목록만) |
| N2 재판정 | 대상 **45**(K3-3 24 · K5-1 6 · K5-2 11 · K5-3 #2 ~ #5 4) → **메움 5** · **범위 제외 6**(타이머 · 리액션 — 사용 안 함) · **여전히 확인 안 됨 34** |
| N3 새 키 | P 경로 4개에 2차 합집합에 없던 키 **190**(P02 1 · P08 86 · P10 16 · P33 87) — 판정: 저장됨 17 · 칸 있음·미동기화 2 · 칸 없음 19 · 일부러 안 둠 142 · 계산으로 대체 1 · 해당 없음 8 · 확인 안 됨 1 |
| N4 예약 현황 · 정원 · 병원 설정 | 내부 경로 **12**(새로 대조 8경로 · **121키** + 2차 표 그대로 4경로 P03 · P25 · P26 · P27 — 새 키 0). **칸별 정원 · 예약 수를 주는 내부 경로는 HAR 에 없다**(P28 대신할 경로 없음 — 정원은 P03 `intervalCapacities`, 예약 칸은 `available` bool 만) · 휴무 · 점유 시간 · 예약 정책은 **3차에도 빈 배열 · 빈 객체** |
| N5 고객별 일정 · 문진 · 이력 | 내부 **2경로 168키**(`get-schedule-list-items` 54 · `get-schedules-summarized-by-task` 114) + 문진 legacy(**400 `visitorId NotFound` 만** — 키 0). P29 를 혼자 대신하는 내부 경로 없음 · P30 · P32 대응 경로 HAR 에 없음 |
| N6 수납 | 읽기 **5경로 87키**(결제 설정 64 · 고객 선불 잔액 17 · 통화 2 · 부가세 3 · 택스리펀드 영수증 1) · 쓰기 11경로(목록만). 결제 설정 결제 수단 **7종**(카드 · 현금 · 계좌이체 · 플랫폼 · 간편결제 · 선불카드 · 의료대출) — 켜짐 6 · 꺼짐 1(의료대출) · `order` 0 ~ 5 순서가 화면 6개 순서와 같다 |
| N6-1 딥링크 | 3차 HAR `pages[]` **0** · `Referer` = **origin 만**(경로 없음). 2차 HAR `pages[]` 에서 화면 URL 모양 4가지(`/{tenantId}` · `/reservation/schedule/?scheduleId&tab&visitorId` · `/reservation/procedure?id` · `/reservation/settings`) — **수납 화면 URL · 구매 id 가 든 URL 은 확인 안 됨** · 새 창 직접 열기 확인 안 됨 |
| N7 2차 → 3차 | 키 1,965 → **2,155** · 확인 안 됨 키 24 → **17** · DB 확장 후보 832행 · 고유 618 → **853행 · 고유 632** · (2차 범위 밖이던 K1-2 14경로 + 새 경로 1 · 376키를 새로 판정 — 후보 133행, 2차 수에 더하지 않음 · N7-3) |
| 정할 것 | **13**(N8 — 2차 K6 번호와 겹치면 적음) |

핵심 사실 일곱:

1. **희망 시술 안쪽 키 · 귀가 희망 시각이 처음 보였다**(K5-2 #1 · #2) — P08 `get-schedule-detail`(예약내역.har#28) · P33(예약내역.har#6) 에 `reservation.desiredDischargeDateTimeUtc`(ISO UTC) · `requestedProcedures[].optionConfiguration{optionId, optionTitle, productTitle, optionType, price{amount(int), currency, reason.type}, medicalService, compositions[], translsMap}`. DAY 매퍼가 읽는 이름 · 모양(`emr/kos/mapper.py:337 · 355-359 · 587`)과 맞는다. 다만 `type` 은 `OPTION` 만 — **시술권(`TICKET`) 희망 시술은 여전히 0**(K5-2 #3), **희망 의사 `reservation.doctor.id` 는 3차 응답 전부 빈 문자열**(K5-2 #5).
2. **수가 유형별 가격 `price.additional[]` 이 처음 보였다**(K5-2 #7 · 시술기기약품.har#74 · #80) — 원소 = `{visitorType{id,name}, amount, suppliedAmount, vatAmount, taxFreeAmount, taxation}`. DAY `product_option_price` 는 `customer_type_id` · `amount` 만(`models/menu.py:129-138`) — 공급가 · 부가세 · 면세 · 과세 · 통화 8키는 칸 없음.
3. **예약 현황 화면은 날짜 하루씩 P33 을 부른다** — 예약현황.har 요청 본문: `get-schedules-for-reservation{baseDateUtc, reservationGroupIds[], zoneIds[]}` 를 D+0 · D+1 · D+2 로(#21 · #31 · #38 · #43), 같은 날짜로 `get-reservation-group-days-offs` · `get-default-days-off` · `get-occupied-times` 를 함께. 미래 날짜 응답은 데모라 **일정 0건**. 칸 정원은 `get-reservation-groups`(= P03 · DAY 이미 저장 `reservation_group_capacity`)의 `intervalCapacities[]` 뿐이고 **칸별 예약 수 · 남은 자리를 주는 내부 경로는 없다**.
4. **휴무 · 점유 시간 · 예약 정책 · 병원 언어는 3차에도 키를 못 봤다** — `get-default-days-off`(8응답) · `get-reservation-group-days-offs`(7) · `get-occupied-times`(7) 모두 빈 배열, `get-default-reservation-policy`(2) 빈 객체, `get-hospital.languages[]` 빈 배열. 병원설정.har 에는 **휴무 · 운영 시간 경로 자체가 없다**(`get-hospital` · 메뉴 · 방만 — N1).
5. **`get-schedule-list-items` 는 고객별 목록이 아니라 「수정 시각 창」 목록이다** — 요청 본문 키 `updatedDateTimeUtcFrom/To · limit`(고객 id 없음 · 예약내역.har#19). 응답 54키 = 예약 단위 요약(예약 상태 · 시작 · 메모 · 상담사 · 담당 · 유입 · 점유 그룹 · 희망 시술 제목 · 고객 요약). 고객 id 로 부르는 것은 **`get-schedules-summarized-by-task{visitorId}`**(작업 목록) · **`get-purchase-summaries-by-visitor-id`**(키 235 = P15 합집합 안). cc 가 P29 에서 읽는 `reservation.status` · `flowStep` · `deleted` 는 `summarized-by-task` 에 없다(N5).
6. **결제 설정은 7종 · 켜짐 6** — `paymentTypeConfiguration.{card, cash, transfer, platform, easyPay, prepaidCard, medicalLoan}Configuration`, 각각 `enabled · order · method.{manual, terminal}Configuration`. 켜진 6종의 `order` 0 ~ 5 순서(카드 · 현금 · 계좌이체 · 플랫폼 · 간편결제 · 선불카드)가 화면 6개 순서(카드 · 현금 · 계좌이체 · 앱 결제 · 간편결제 · 선불카드)와 같다 — **「앱 결제」 ↔ `platformConfiguration` 은 순서 일치로만 본 것**이고 거래의 `paymentType` 문자열은 둘 다 여전히 모른다(3차 거래 `paymentType` = `CASH` · `PREPAID_CARD` 만).
7. **KOS 웹 화면 URL 은 `/{tenantId}/…` 꼴이고 DAY 가 그 id 들을 이미 가진다** — 2차 HAR `pages[]`: 고객 · 예약 상세 = `https://app.kos-solution.com/{tenantId}/reservation/schedule/?scheduleId={uuid}&tab={…}&visitorId={24자 hex}`(수납필요 확인.har). `scheduleId` = 일정 id(같은 HAR 의 P08 `data.id` · P33 `data[].id` 와 같은 값) → DAY `external_ref`(일정 · `emr/kos/mapper.py:555`), `visitorId` = 고객 id → `external_ref`(고객 · `:307`), `tenantId` → `crm_connection.config.tenant_id`(`models/hospital.py:26-27`) · `external_session.external_tenant_id`(`models/staff.py:110`). 관찰된 `tab` 값은 `consultation` 하나 — **수납 탭 값 · 수납 전용 URL 은 HAR 에 없다.**

판정 기준: 2차 「판정 기준」 그대로(저장됨 · 칸 있음·미동기화 · 칸 없음 · 칸 없음(시점 다름) · 일부러 안 둠 · 계산으로 대체 · 해당 없음 · 확인 안 됨). 더한 것 하나 — **「사용 안 함(사용자)」**: 사용자 11-20 「KOS 타이머 안 쓴다」로 대조에서 뺀 `taskTimers[]` · `reactions[]`.

## N1. 새 HAR 경로 목록

센 방법: 7개 HAR 의 요청 URL 중 `/queries/` 가 든 경로(테넌트 접두 `tenants/{id}/` 제거 — 2차 `keys.py kospath` 그대로). 「200+JSON」 = 상태 200 이고 본문이 JSON. 「그 밖」의 `OPTIONS·빈 본문` 은 CORS 사전 요청(61건 모두 메서드 OPTIONS · 본문 없음). 「2차 HAR 키」 = 2차 HAR 67개로 다시 만든 같은 경로의 합집합 키 수(P 경로는 2차 K1 「스크립트 키 수」와 같다 — P03 63 · P08 242 · P10 210 · P15 455 · P33 226 확인).

| 갈래 | 경로 | 엔트리 | 200+JSON | 그 밖 | 200+JSON 파일(수) | 3차 키 | 2차 HAR 키 | 3차에만 있는 키 |
|---|---|---|---|---|---|---|---|---|
| P01 | `schedule/zone/v1/queries/get-zones` | 2 | 1 | OPTIONS·빈 본문(1) | 예약현황.har(1) | 5 | 5 | 0 |
| P02 | `schedule/zone/room/v1/queries/get-rooms` | 3 | 2 | OPTIONS·빈 본문(1) | 병원설정.har(1) · 예약등록.har(1) | 6 | 5 | 1 |
| P03 | `schedule/group/v1/queries/get-reservation-groups` | 3 | 2 | OPTIONS·빈 본문(1) | 예약현황.har(2) | 63 | 63 | 0 |
| P04 | `role/v2/queries/get-roles` | 10 | 10 |  | 병원설정.har(1) · 상담기록.har(1) · 시술결제환불.har(4) · 시술기기약품.har(2) · 예약내역.har(1) · 예약등록.har(1) | 6 | 13 | 0 |
| P05 | `account/v2/queries/get-accounts` | 9 | 9 |  | 시술결제환불.har(2) · 예약내역.har(2) · 예약등록.har(1) · 예약현황.har(4) | 17 | 19 | 0 |
| P06 | `meta/codes/v1/queries/get-codes` | 20 | 18 | OPTIONS·빈 본문(2) | 상담기록.har(1) · 시술결제환불.har(1) · 시술기기약품.har(1) · 예약내역.har(7) · 예약등록.har(8) | 7 | 8 | 0 |
| P08 | `schedule/v1/queries/get-schedule-detail` | 3 | 2 | OPTIONS·빈 본문(1) | 예약내역.har(1) · 예약등록.har(1) | 192 | 242 | 86 |
| P09 | `procedure-menu/categories/queries/get-categories` | 5 | 4 | OPTIONS·빈 본문(1) | 병원설정.har(1) · 시술기기약품.har(3) | 14 | 14 | 0 |
| P10 | `procedure-menu/products/queries/get-products` | 2 | 1 | OPTIONS·빈 본문(1) | 시술기기약품.har(1) | 226 | 210 | 16 |
| P11 | `procedure-menu/v2/queries/get-procedures` | 12 | 10 | OPTIONS·빈 본문(2) | 병원설정.har(2) · 시술기기약품.har(8) | 7 | 7 | 0 |
| P13 | `procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product` | 2 | 1 | OPTIONS·빈 본문(1) | 시술결제환불.har(1) | 21 | 21 | 0 |
| P14 | `procedure-menu/etcetera-products/v1/queries/get-etcetera-products` | 2 | 1 | OPTIONS·빈 본문(1) | 시술기기약품.har(1) | 13 | 13 | 0 |
| P15 | `purchase/v1/queries/get-purchase-summaries` | 36 | 35 | OPTIONS·빈 본문(1) | 시술결제환불.har(35) | 336 | 455 | 0 |
| P16 | `ticket/v1/queries/get-ticket-bundles` | 6 | 5 | OPTIONS·빈 본문(1) | 시술결제환불.har(1) · 예약내역.har(1) · 예약등록.har(3) | 86 | 116 | 0 |
| P17 | `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` | 12 | 11 | OPTIONS·빈 본문(1) | 시술결제환불.har(9) · 예약내역.har(1) · 예약등록.har(1) | 23 | 23 | 0 |
| P20 | `visitor/v2/queries/get-visitors` | 2 | 1 | OPTIONS·빈 본문(1) | 예약등록.har(1) | 61 | 64 | 0 |
| P24 | `visitor/v2/queries/get-visitor` | 4 | 3 | OPTIONS·빈 본문(1) | 예약내역.har(1) · 예약등록.har(2) | 49 | 63 | 0 |
| P25 | `v1/hospital/queries/get-hospital` | 2 | 1 | OPTIONS·빈 본문(1) | 병원설정.har(1) | 22 | 22 | 0 |
| P26 | `schedule/default-operation-time/v1/queries/get-default-operation-timetable` | 6 | 5 | OPTIONS·빈 본문(1) | 예약내역.har(1) · 예약등록.har(3) · 예약현황.har(1) | 50 | 50 | 0 |
| P27 | `schedule/default-operation-time/v1/queries/get-default-days-off` | 9 | 8 | OPTIONS·빈 본문(1) | 예약내역.har(1) · 예약등록.har(3) · 예약현황.har(4) | 1 | 1 | 0 |
| P33 | `schedule/v2/queries/get-schedules-for-reservation` | 10 | 9 | OPTIONS·빈 본문(1) | 예약내역.har(2) · 예약등록.har(3) · 예약현황.har(4) | 304 | 226 | 87 |
| K1-2 #1 | `account/v2/queries/get-accounts-last-update-date-time-utc` | 10 | 9 | OPTIONS·빈 본문(1) | 상담기록.har(1) · 시술결제환불.har(1) · 예약내역.har(3) · 예약등록.har(3) · 예약현황.har(1) | 1 | 1 | 0 |
| K1-2 #5 | `common/medicine-and-machines/v2/queries/get-medicine-and-machines` | 5 | 4 | OPTIONS·빈 본문(1) | 병원설정.har(1) · 시술기기약품.har(3) | 5 | 5 | 0 |
| K1-2 #6 | `consultation/v1/queries/get-consultations-by-visitor-id` | 5 | 4 | OPTIONS·빈 본문(1) | 상담기록.har(1) · 시술결제환불.har(1) · 예약내역.har(1) · 예약등록.har(1) | 19 | 19 | 0 |
| K1-2 #7 | `image/visitor-image/v1/queries/get-visitor-images` | 2 | 1 | OPTIONS·빈 본문(1) | 예약내역.har(1) | 1 | 23 | 0 |
| K1-2 #9 | `meta/notice/v1/queries/get-notices` | 8 | 7 | OPTIONS·빈 본문(1) | 예약내역.har(1) · 예약등록.har(2) · 예약현황.har(4) | 1 | 5 | 0 |
| K1-2 #14 | `prescription/v1/queries/get-prescriptions` | 2 | 1 | OPTIONS·빈 본문(1) | 예약내역.har(1) | 1 | 1 | 0 |
| K1-2 #16 | `procedure-menu/currency-settings/queries/get-currency-settings` | 2 | 1 | OPTIONS·빈 본문(1) | 시술기기약품.har(1) | 2 | 2 | 0 |
| K1-2 #17 | `procedure-menu/procedure-categories/queries/get-procedure-categories` | 5 | 4 | OPTIONS·빈 본문(1) | 병원설정.har(1) · 시술기기약품.har(3) | 1 | 1 | 0 |
| K1-2 #18 | `procedure-menu/product-options/v2/queries/search-product-option-summaries` | 7 | 6 | OPTIONS·빈 본문(1) | 시술결제환불.har(4) · 예약등록.har(2) | 172 | 172 | 0 |
| K1-2 #19 | `procedure-menu/products/queries/get-product` | 2 | 1 | OPTIONS·빈 본문(1) | 시술기기약품.har(1) | 127 | 147 | 0 |
| K1-2 #21 | `procedure-menu/target-countries/v1/queries/get-target-countries` | 6 | 5 | OPTIONS·빈 본문(1) | 병원설정.har(2) · 시술기기약품.har(3) | 3 | 4 | 0 |
| K1-2 #22 | `procedure-menu/vat-settings/queries/get-vat-settings` | 2 | 1 | OPTIONS·빈 본문(1) | 시술기기약품.har(1) | 3 | 3 | 0 |
| K1-2 #23 | `procedure-menu/visitors/queries/get-visitors` | 21 | 19 | OPTIONS·빈 본문(2) | 병원설정.har(3) · 상담기록.har(1) · 시술결제환불.har(6) · 시술기기약품.har(4) · 예약내역.har(1) · 예약등록.har(4) | 6 | 6 | 0 |
| K1-2 #24 | `purchase/payment-settings/v1/queries/get-payment-settings` | 8 | 6 | OPTIONS·빈 본문(2) | 상담기록.har(1) · 시술결제환불.har(4) · 예약내역.har(1) | 64 | 64 | 0 |
| K1-2 #25 | `purchase/prepaid-card/v1/queries/get-visitor-prepaid-card-balance` | 3 | 2 | OPTIONS·빈 본문(1) | 예약내역.har(1) · 예약등록.har(1) | 17 | 17 | 0 |
| K1-2 #26 | `purchase/tax-refund-receipts/v1/queries/get-tax-refund-receipts` | 2 | 1 | OPTIONS·빈 본문(1) | 시술결제환불.har(1) | 1 | 1 | 0 |
| K1-2 #28 | `schedule/default-operation-time/v1/queries/get-default-reservation-policy` | 3 | 2 | OPTIONS·빈 본문(1) | 예약등록.har(2) | 1 | 1 | 0 |
| K1-2 #29 | `schedule/group/v1/queries/get-reservation-group` | 10 | 9 | OPTIONS·빈 본문(1) | 상담기록.har(1) · 시술결제환불.har(4) · 시술기기약품.har(1) · 예약내역.har(1) · 예약등록.har(2) | 63 | 63 | 0 |
| K1-2 #30 | `schedule/group/v1/queries/get-reservation-group-days-offs` | 8 | 7 | OPTIONS·빈 본문(1) | 예약내역.har(1) · 예약등록.har(2) · 예약현황.har(4) | 1 | 1 | 0 |
| K1-2 #31 | `schedule/occupied-time/v2/queries/get-occupied-times` | 8 | 7 | OPTIONS·빈 본문(1) | 예약내역.har(1) · 예약등록.har(2) · 예약현황.har(4) | 1 | 1 | 0 |
| K1-2 #32 | `schedule/reservation-rule/v1/queries/get-reservation-rule` | 2 | 1 | OPTIONS·빈 본문(1) | 예약등록.har(1) | 27 | 27 | 0 |
| K1-2 #33 | `schedule/reservation-rule/v1/queries/get-reservation-rule-summaries` | 2 | 1 | OPTIONS·빈 본문(1) | 예약등록.har(1) | 11 | 11 | 0 |
| K1-2 #34 | `schedule/reservation-time-slot/v1/queries/get-occupied-resources-by-reservation-time-slot` | 2 | 1 | OPTIONS·빈 본문(1) | 예약등록.har(1) | 9 | 9 | 0 |
| K1-2 #35 | `schedule/reservation-time-slot/v1/queries/get-reservation-time-slots` | 7 | 6 | OPTIONS·빈 본문(1) | 예약등록.har(6) | 8 | 8 | 0 |
| K1-2 #36 | `schedule/v1/queries/get-payment-required-tasks` | 4 | 3 | OPTIONS·빈 본문(1) | 예약내역.har(1) · 예약등록.har(2) | 1 | 1 | 0 |
| K1-2 #37 | `schedule/v1/queries/get-schedule-summaries` | 10 | 9 | OPTIONS·빈 본문(1) | 상담기록.har(1) · 시술결제환불.har(4) · 시술기기약품.har(1) · 예약내역.har(1) · 예약등록.har(2) | 123 | 99 | 37 |
| K1-2 #38 | `schedule/v2/queries/get-schedule-list-items` | 2 | 1 | OPTIONS·빈 본문(1) | 예약내역.har(1) | 54 | 34 | 20 |
| K1-2 #40 | `v1/visitor/queries/get-visitor` | 14 | 12 | OPTIONS·빈 본문(2) | 상담기록.har(2) · 시술결제환불.har(7) · 시술기기약품.har(1) · 예약내역.har(2) | 49 | 63 | 0 |
| K1-2 #41 | `visitor/files/v1/queries/get-visitor-files` | 2 | 1 | OPTIONS·빈 본문(1) | 예약내역.har(1) | 1 | 1 | 0 |
| K1-2 #42 | `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` | 4 | 0 | 400(3) · OPTIONS·빈 본문(1) |  | 0 | 36 | 0 |
| **새 경로** | `notification/message/v1/queries/get-sent-messages` | 2 | 1 | OPTIONS·빈 본문(1) | 예약내역.har(1) | 1 | 0 | 1 |
| **새 경로** | `procedure-menu/machines/v1/queries/get-machines` | 4 | 3 | OPTIONS·빈 본문(1) | 시술기기약품.har(3) | 7 | 0 | 7 |
| **새 경로** | `procedure-menu/medical-service/v1/queries/get-medical-services` | 3 | 2 | OPTIONS·빈 본문(1) | 시술기기약품.har(2) | 41 | 0 | 41 |
| **새 경로** | `procedure-menu/medicine/v1/queries/get-medicines` | 4 | 3 | OPTIONS·빈 본문(1) | 시술기기약품.har(3) | 7 | 0 | 7 |
| **새 경로** | `procedure-menu/products/v1/queries/count-products-by-targeted-country` | 2 | 1 | OPTIONS·빈 본문(1) | 병원설정.har(1) | 3 | 0 | 3 |
| **새 경로** | `purchase/v1/queries/get-purchase-summaries-by-visitor-id` | 2 | 1 | OPTIONS·빈 본문(1) | 예약내역.har(1) | 235 | 0 | 235 |
| **새 경로** | `schedule/v2/queries/get-schedules-summarized-by-task` | 2 | 1 | OPTIONS·빈 본문(1) | 예약내역.har(1) | 114 | 0 | 114 |


- 갈래 수: **P 21 · K1-2 30 · 새 경로 7 = 58**. 2차 P 34 중 3차 HAR 에 없는 것 13 — P07 · P12 · P18 · P19 · P21 · P22 · P23 · P28 ~ P32 · P34.
- 새 경로 7(2차 HAR 67개에도 없음): `get-purchase-summaries-by-visitor-id`(고객별 구매 — 키 235 모두 P15 합집합 안) · `get-schedules-summarized-by-task`(고객별 일정의 작업 — 키 111 이 P33 합집합 안, 나머지 3 = `scheduleId` · `startDateTimeUtc` · `endDateTimeUtc`) · `get-medical-services`(41 · 진료항목) · `get-medicines`(7) · `get-machines`(7) · `count-products-by-targeted-country`(3) · `get-sent-messages`(1 · `data[]` 빈 배열).
- 파일 설명과 다른 점(HAR 안 경로 기준): **병원설정.har 에 운영 시간 · 휴무 경로가 없다**(병원 정보 · 메뉴 · 방 · 타겟 국가만). 운영 시간 · 기본 휴무 · 그룹 휴무는 예약현황.har · 예약등록.har · 예약내역.har 에 있다. **시술결제환불.har 의 #1 ~ #17 은 상담기록.har #1 ~ #17 과 같은 경로 · 같은 번호**(같은 기록이 이어진 것으로 보임 — 확인 안 됨). 예약현황.har 에 **그룹 정원을 바꾸는 쓰기 경로 · 휴무 쓰기 경로는 없다**(쓰기 11경로 — 아래).

쓰기(commands) — 목록만(대조 안 함 · 본문 안 읽음):

| 쓰기 경로(commands) | 엔트리 | 파일 |
|---|---|---|
| `consultation/v1/commands/create-consultation` | 4 | 상담기록.har(2) · 시술결제환불.har(2) |
| `purchase/v1/commands/accept-purchase` | 3 | 시술결제환불.har(3) |
| `purchase/v1/commands/add-canceled-transaction` | 2 | 시술결제환불.har(2) |
| `purchase/v1/commands/add-pending-purchase-items` | 3 | 시술결제환불.har(3) |
| `purchase/v1/commands/add-transaction` | 3 | 시술결제환불.har(3) |
| `purchase/v1/commands/complete-purchase-refund` | 2 | 시술결제환불.har(2) |
| `purchase/v1/commands/initialize-purchase` | 3 | 시술결제환불.har(3) |
| `purchase/v1/commands/mark-purchase-items-for-refund` | 2 | 시술결제환불.har(2) |
| `purchase/v1/commands/start-purchase-refund` | 2 | 시술결제환불.har(2) |
| `schedule/reservation/v2/commands/reserve` | 2 | 예약등록.har(2) |
| `schedule/v1/commands/register-purchase` | 3 | 시술결제환불.har(3) |


## N2. 2차 「확인 안 됨」 · K5 재판정

판정은 2차 기준. 「본 곳」 = 3차 HAR 파일#엔트리. 「여전히」 = 3차 HAR 로도 못 봄.

### N2-1. 2차 K3-3 `확인 안 됨` 키 24

| # | 경로 | 키 | 3차 | 본 곳 · 모양 | 3차 판정 |
|---|---|---|---|---|---|
| 1 | P07 | `data[].schedules[].consultations[].visitor.isNew` | 여전히(경로 없음) | P07 은 3차 HAR 에 없다. 같은 일정 객체의 같은 키는 P08 · P33 에서 bool(아래 #5 · #9) | 확인 안 됨 |
| 2 | P07 | `data[].schedules[].reactions[]` | 범위 제외 | — | **사용 안 함(사용자)** |
| 3 | P07 | `data[].schedules[].taskTimers[]` | 범위 제외 | — | **사용 안 함(사용자)** |
| 4 | P07 | `…tasks[].procedureConfiguration.productOptionConfiguration.medicineAndMachines[]` | 여전히(경로 없음) | 같은 키가 P33 · `summarized-by-task` 에서 **빈 배열**(예약내역.har#6 · #56) | 확인 안 됨 |
| 5 | P08 | `data.consultations[].visitor.isNew` | **봄** | 예약내역.har#28 · bool | **계산으로 대체** — `visit.is_new`(`models/visit.py:91` · `emr/kos/mapper.py:597`). 같은 일정의 `visitor.isNew` 와 3차 15/15 같은 값(P08 · P33 · 값 비교만) |
| 6 | P08 | `data.reactions[]` | 범위 제외 | 예약내역.har#28 빈 배열 | **사용 안 함(사용자)** |
| 7 | P08 | `data.taskTimers[]` | 범위 제외 | 예약내역.har#28 빈 배열 | **사용 안 함(사용자)** |
| 8 | P08 | `data.tasks[]…productOptionConfiguration.medicineAndMachines[]` | 여전히 | P08 3차 2응답에 키 없음(작업 없음) | 확인 안 됨 |
| 9 | P33 | `data[].consultations[].visitor.isNew` | **봄** | 예약내역.har#6 · bool | **계산으로 대체**(#5 와 같음) |
| 10 | P33 | `data[].reactions[]` | 범위 제외 | 예약내역.har#6 빈 배열 | **사용 안 함(사용자)** |
| 11 | P33 | `data[].taskTimers[]` | 범위 제외 | 예약내역.har#6 빈 배열 | **사용 안 함(사용자)** |
| 12 | P33 | `data[].tasks[]…productOptionConfiguration.medicineAndMachines[]` | 여전히 | 예약내역.har#6 빈 배열 | 확인 안 됨 |
| 13 | P10 | `data[].options[].compositions[].price.additional[]` | 여전히 | 시술기기약품.har#74 빈 배열(옵션 쪽 `price.additional[]` 은 채워짐 — N3) | 확인 안 됨 |
| 14 ~ 21 | P15 | `items[]` · `pendingItems[]` 의 `optionConfiguration.compositions[].medicalService.configuration.medicines[]` · `…compositions[].medicineAndMachines[]` · `…compositions[].price.additional[]` · `optionConfiguration.medicineAndMachines[]`(8키) | 여전히 | 시술결제환불.har#147(items) · #129(pendingItems) 빈 배열 — 시술기기약품.har 에서 메뉴 쪽(P10 `options[].medicineAndMachines[]` · `compositions[].medicineAndMachines[]`)은 원소가 있는데 **구매 스냅샷 쪽은 비어 있다** | 확인 안 됨 |
| 22 | P15 | `data[].revokingItems[]` | 여전히 | 시술결제환불.har#49 빈 배열(환불은 `refundingItems[]` 쪽에 원소 — 2차 K6-21 칸 있음·미동기화) | 확인 안 됨 |
| 23 | P25 | `data.languages[]` | 여전히 | 병원설정.har#7 빈 배열 | 확인 안 됨 |
| 24 | P27 | `data[]` | 여전히 | 8응답 모두 빈 배열(예약현황.har 미래 D+0 ~ D+2 범위 포함) | 확인 안 됨 |

→ 메움 **2**(#5 · #9) · 범위 제외 **6** · 여전히 **16**.

### N2-2. 2차 K5-1 HAR 에 응답이 없는 경로 6

| # | 경로 | 3차 | 이유(갱신) |
|---|---|---|---|
| P23 | `common/user/v1/queries/get-active-sign-ins` | 여전히 | **KOS 웹에 로그인 세션 관리 화면이 없다(사용자 11-20)** — 웹 HAR 로는 볼 길이 없다 |
| P28 | `schedule/open/v2/queries/get-reservation-slots-by-groups` | 여전히 | 공개 경로 — 웹 HAR 은 내부 API 만. 같은 정보(칸별 정원 · 예약 수)를 주는 내부 경로도 3차 HAR 에 없다(N4) |
| P29 | `schedule/open/v1/queries/get-schedules-by-visitor` | 여전히 | 공개 경로. 내부 후보 `get-schedules-summarized-by-task` · `get-schedule-list-items` 는 같은 응답이 아니다(N5) |
| P30 | `visitor/open/v1/queries/get-visitor-questionnaire` | 여전히 | 공개 경로 · 문진 **양식**을 주는 내부 경로가 3차 HAR 에도 없다 |
| P31 | `visitor/open/v1/queries/get-questionnaire-submit` | 여전히 | 공개 경로. 내부 legacy 는 3차에 **400 `InvalidRequestException` · `errorProperties[{key: visitorId, reason: NotFound}]` 만**(예약내역.har#36 · 예약등록.har#56 · #73) — 데모 고객에 제출본 없음. cc 는 공개 쪽 같은 오류를 「제출본 없음」으로 다룬다(`cc:service/reservations.py:614-615`) |
| P32 | `schedule/v1/queries/get-schedule-event-logs` | 여전히 | 내부 경로인데 3차 HAR 7개에도 없다(N1 58경로에 없음). 예약내역.har 의 일정 변경 이력 화면이 이 경로를 부르지 않았다 |

→ 메움 **0** · 여전히 **6**.

### N2-3. 2차 K5-2 DAY 가 읽는데 HAR 에서 키 · 값을 못 본 것 11

| # | 키 | 3차 | 본 곳 · 모양 | 3차 판정 |
|---|---|---|---|---|
| 1 | 일정 `reservation.desiredDischargeDateTimeUtc` | **봄** | P08 예약내역.har#28 · P33 예약내역.har#6 · string(ISO UTC) | 저장됨(`emr/kos/mapper.py:587` → `visit.desired_discharge_at`) — 2차 규칙 그대로 |
| 2 | `reservation.requestedProcedures[]` 안쪽 | **봄** | P08 #28 · P33 #6 · `get-schedule-summaries`(상담기록.har#6): `type`=`OPTION` · `optionConfiguration{optionId, optionTitle, productTitle, optionType(GROUP\|SINGLE), price{amount int, currency KRW, reason.type GENERAL}, medicalService{…}, compositions[]{medicalService{…}}, translsMap}` | 저장됨 6(`type` · `productTitle` · `optionTitle` · `optionType` · `price.amount` · `price.currency` — `emr/kos/mapper.py:337 · 355-359`) · 나머지 N3 표 |
| 3 | 희망 시술 `ticketConfiguration.{productTitle, ticketTitle}` | 여전히 | `requestedProcedures[].type` 은 3차 전 응답에서 `OPTION` 만. 3차 HAR 의 `ticketConfiguration` 은 **작업** 쪽(`tasks[].procedureConfiguration.ticketConfiguration{ticketId, round{current,total}}` — 2차에 이미 있던 키)뿐 | 확인 안 됨 |
| 4 | `occupiedResources[].reservationGroup.doctors[]` | 여전히 | P08 #28 · P33 #6 · `get-occupied-resources-by-reservation-time-slot`(예약등록.har#42) 모두 빈 배열 | 확인 안 됨 |
| 5 | `reservation.doctor.id`(희망 의사) | 여전히 | P08(예약내역.har#28 · 예약등록.har#115) · P33 전 응답에서 `doctor{id, name}` 둘 다 **빈 문자열** — 예약등록.har 에서 희망 의사를 넣은 일정이 응답에 있는지는 확인 안 됨 | 2차 그대로 |
| 6 | `consultations[].consultationProcedures[]` | 여전히 | P08 #28 · P33 #6 · `get-consultations-by-visitor-id`(상담기록.har#15) 모두 빈 배열 — 상담기록.har 에서 상담 시술을 넣었다는데 응답 키는 비어 있다 | 확인 안 됨 |
| 7 | 옵션 `price.additional[]`(수가 유형별 가격) | **봄** | P10 시술기기약품.har#74 · `get-product` #80 · `search-product-option-summaries` 시술결제환불.har#33 · 원소 `{visitorType{id,name}, amount{value,currency}, suppliedAmount, vatAmount, taxFreeAmount, taxation}` | 저장됨 3 · 칸 없음 8 · 계산 1 · 해당 없음 4(N3 P10) |
| 8 | 상품 · 옵션 `badges[]` · `promotionConfigurations[]` | 여전히 | P10 #74 · `get-product` #80 빈 배열 · `get-ticket-bundles.optionConfiguration.promotionConfiguration` 빈 객체(시술결제환불.har#153) | 2차 그대로 |
| 9 | 구매 · 항목 `priceAdjustments[]` | 여전히 | P15(시술결제환불.har#49 · #95) · `by-visitor-id`(예약내역.har#52) 빈 배열 | 2차 그대로 |
| 10 | 카드 이력 `amount.type` · `type` | 여전히 | P18 이 3차 HAR 에 없다 | 2차 그대로 |
| 11 | 로그인 `mfaMethods[]` | 여전히 | P21 이 3차 HAR 에 없다 | 2차 그대로 |

→ 메움 **3**(#1 · #2 · #7) · 여전히 **8**.

### N2-4. 2차 K5-3 #2 ~ #5

| # | 무엇 | 3차 HAR | 3차 판정 |
|---|---|---|---|
| 2 | 고객 단건 전화번호 | **P24 3차 3응답(예약내역.har#26 · 예약등록.har#50 · #71) 모두 `phoneNumber` 키 없음** — `S0:412` 「이 응답에 없다」와 이번엔 같다. 2차 합집합의 `phoneNumber` 는 수납필요 확인.har#39 하나에서 생겼다. 3차 P24 에 없는 2차 키 14 = `email` · `passportExpiryDate` · `passportGivenNames` · `passportSurname` · `phoneNumber{,.countryCode,.phoneNumber}` · `phoneticName` · `unregistered{,.name}` · `visitorCategories[].{color,id,name,order}` — 값이 빈 고객이면 키를 빼는 꼴로 보인다(확인 안 됨). 같은 3차 HAR 의 P20 목록(예약등록.har#47)에는 `phoneNumber{countryCode, phoneNumber}` 가 있다 | 여전히(응답마다 다름) |
| 3 | 구매 키 `conversion` · `purchaseMemo` · `migratedDateTimeUtc` | P15 3차 35응답 · `by-visitor-id` 1응답 합집합에 **없다** | 여전히 |
| 4 | 병원 기본 휴무 키 | `get-default-days-off` 8응답 모두 빈 배열 | 여전히 |
| 5 | `reservation.statusUpdatedDateTimeUtc` · `reservationTagIds[]` | 둘 다 P08 · P33 에 있다(`reservationTagIds[]` 는 P33 에 이번에 처음 — 빈 배열). P07 은 3차 HAR 에 없어 P07 에 있는지는 여전히 모른다 | 여전히(P07) |

→ 메움 **0** · 여전히 **4**.

**N2 합계: 대상 45 = 메움 5 + 범위 제외 6 + 여전히 34.**

## N3. 기존 경로(P01 ~ P34)의 새 키

3차 HAR 에 나온 P 경로 21 중 **2차 합집합에 없던 키가 있는 경로 4** — P02 1 · P08 86 · P10 16 · P33 87 = **190**. 나머지 17경로는 새 키 0(N1 오른쪽 칸). 판정은 2차 `rules.py` 그대로(P02 · P08 · P33 — 2차가 `get-schedule-summaries` 에서 미리 본 희망 시술 규칙이 그대로 걸렸다 · 기본값으로 떨어진 키 0). **P10 16키만 손 판정** — 2차 규칙의 「늘 빈 배열 → 확인 안 됨」이 더는 사실이 아니라서(근거 `emr/kos/mapper_menu.py:83-90 · 110-116` · `emr/kos/mapper_sale_values.py:90-97` · `models/menu.py:129-138`).

- P08 · P33 의 `일부러 안 둠` 142행 = 희망 시술 **진료항목 · 구성 스냅샷**(`optionConfiguration.medicalService.*` · `compositions[].medicalService.*`) — 근거 `S0:510`(2차 규칙 그대로). 사용자 · 코디네이터 기본값 「일부러 안 둠 54행에도 다 저장」(_RESUME §2 마지막 행)이 이 142행에도 걸리는지는 N8-11.
- P33 `data[].reservationTagIds[]` 는 P33 에 처음 · P08 에서는 2차에 이미 `칸 없음` — 판정 같음.

#### P02 `schedule/zone/room/v1/queries/get-rooms` — 새 키 **1** · 표 행 **1** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data[].roomCategoryIds[]` | array(empty) |  | 확인 안 됨 | 빈 값만 관찰 — 안쪽 키 확인 안 됨 · 병원설정.har#49 |

#### P08 `schedule/v1/queries/get-schedule-detail` — 새 키 **86** · 표 행 **86** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data.reservation.desiredDischargeDateTimeUtc` | string(ISO UTC) | visit.desired_discharge_at (models/visit.py:84) | 저장됨 | emr/kos/mapper.py:587 · 예약내역.har#28 |
| 2 | `data.reservation.requestedProcedures[].optionConfiguration` | object |  | 해당 없음 | 묶음 · 예약내역.har#28 |
| 3 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[]` | array / array(empty) / object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 4 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 5 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.caution` | string(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 6 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 7 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.code` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 8 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.healthcareReimbursement` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 9 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.machines[]` | array / object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 10 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.machines[].id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 11 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.machines[].name` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 12 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.machines[].searchPhoneticName` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 13 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.medicines[]` | array(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 14 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.procedure` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 15 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 16 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.procedure.id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 17 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.procedure.name` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 18 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.procedure.searchPhoneticName` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 19 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.taxation` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 20 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.unit` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 21 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.unit.type` | enum:SHOT |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 22 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.unit.value` | number |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 23 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.deleted` | bool |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 24 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.description` | string(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 25 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.draftedDateTimeUtc` | string(ISO UTC) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 26 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 27 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.status` | enum:PUBLISHED |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 28 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.title` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 29 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 30 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 31 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 32 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.en` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 33 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.ja` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 34 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.ko` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 35 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.zh-Hans` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 36 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.zh-Hant` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 37 | `data.reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.updatedDateTimeUtc` | string(ISO UTC) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 38 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 39 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.caution` | string(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 40 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 41 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.code` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 42 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.healthcareReimbursement` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 43 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.machines[]` | array(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 44 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.medicines[]` | array / object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 45 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.medicines[].id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 46 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.medicines[].name` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 47 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.medicines[].searchPhoneticName` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 48 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.procedure` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 49 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 50 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.procedure.id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 51 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.procedure.name` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 52 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.procedure.searchPhoneticName` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 53 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.taxation` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 54 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.unit` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 55 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.unit.type` | enum:UNIT |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 56 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.unit.value` | number |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 57 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.deleted` | bool |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 58 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.description` | string(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 59 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.draftedDateTimeUtc` | string(ISO UTC) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 60 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 61 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.status` | enum:PUBLISHED |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 62 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.title` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 63 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 64 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 65 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 66 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation.en` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 67 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation.ja` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 68 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation.ko` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 69 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation.zh-Hans` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 70 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation.zh-Hant` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 71 | `data.reservation.requestedProcedures[].optionConfiguration.medicalService.updatedDateTimeUtc` | string(ISO UTC) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#28 |
| 72 | `data.reservation.requestedProcedures[].optionConfiguration.optionId` | string | visit_requested_procedure.product_option_id (models/visit.py:105) | 칸 있음 · 미동기화 | S0:551 「1차는 비워 둔다 · 채울지는 OQ-041-7」 · emr/kos/mapper.py:333-336 · 예약내역.har#28 |
| 73 | `data.reservation.requestedProcedures[].optionConfiguration.optionTitle` | string | visit_requested_procedure.option_title (models/visit.py:109) | 저장됨 | emr/kos/mapper.py:356 · 예약내역.har#28 |
| 74 | `data.reservation.requestedProcedures[].optionConfiguration.optionType` | enum:GROUP|SINGLE | visit_requested_procedure.option_type (models/visit.py:110) | 저장됨 | emr/kos/mapper.py:357 · 예약내역.har#28 |
| 75 | `data.reservation.requestedProcedures[].optionConfiguration.price` | object |  | 해당 없음 | 묶음 · 예약내역.har#28 |
| 76 | `data.reservation.requestedProcedures[].optionConfiguration.price.amount` | int | visit_requested_procedure.price_amount (models/visit.py:111) | 저장됨 | emr/kos/mapper.py:358 · 예약내역.har#28 |
| 77 | `data.reservation.requestedProcedures[].optionConfiguration.price.currency` | enum:KRW | visit_requested_procedure.currency (models/visit.py:112) | 저장됨 | emr/kos/mapper.py:359 · 예약내역.har#28 |
| 78 | `data.reservation.requestedProcedures[].optionConfiguration.price.reason` | object |  | 일부러 안 둠 | S0:510 「가격 사유(정상가 · 수가 유형가) … 두지 않는다」 · 예약내역.har#28 |
| 79 | `data.reservation.requestedProcedures[].optionConfiguration.price.reason.type` | enum:GENERAL |  | 일부러 안 둠 | S0:510 「가격 사유(정상가 · 수가 유형가) … 두지 않는다」 · 예약내역.har#28 |
| 80 | `data.reservation.requestedProcedures[].optionConfiguration.productTitle` | string | visit_requested_procedure.product_title (models/visit.py:108) | 저장됨 | emr/kos/mapper.py:355 · 예약내역.har#28 |
| 81 | `data.reservation.requestedProcedures[].optionConfiguration.translsMap` | object |  | 칸 없음 | 희망 옵션 · 상품 이름 번역 · 예약내역.har#28 |
| 82 | `data.reservation.requestedProcedures[].optionConfiguration.translsMap.optionTitle` | object |  | 칸 없음 | 희망 옵션 · 상품 이름 번역 · 예약내역.har#28 |
| 83 | `data.reservation.requestedProcedures[].optionConfiguration.translsMap.optionTitle.translation` | object(empty) |  | 칸 없음 | 희망 옵션 · 상품 이름 번역 · 예약내역.har#28 |
| 84 | `data.reservation.requestedProcedures[].optionConfiguration.translsMap.productTitle` | object |  | 칸 없음 | 희망 옵션 · 상품 이름 번역 · 예약내역.har#28 |
| 85 | `data.reservation.requestedProcedures[].optionConfiguration.translsMap.productTitle.translation` | object(empty) |  | 칸 없음 | 희망 옵션 · 상품 이름 번역 · 예약내역.har#28 |
| 86 | `data.reservation.requestedProcedures[].type` | enum:OPTION | visit_requested_procedure.kind (models/visit.py:104) | 저장됨 | emr/kos/mapper.py:337 · 예약내역.har#28 |

#### P10 `procedure-menu/products/queries/get-products` — 새 키 **16** · 표 행 **16** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data[].options[].price.additional[].amount` | object |  | 해당 없음 | 묶음 · 시술기기약품.har#74 |
| 2 | `data[].options[].price.additional[].amount.currency` | enum:KRW | (통화 칸 없음 — product_option_price 는 amount 만) | 칸 없음 | 사용자 11-20 「통화는 KOS 와 같게」(K6-16) · 시술기기약품.har#74 |
| 3 | `data[].options[].price.additional[].amount.value` | int | product_option_price.amount (models/menu.py:138) | 저장됨 | emr/kos/mapper_menu.py:89 · 2차 「늘 빈 배열」 → 3차 처음 관찰 · 시술기기약품.har#74 |
| 4 | `data[].options[].price.additional[].suppliedAmount` | object |  | 해당 없음 | 묶음 · 시술기기약품.har#74 |
| 5 | `data[].options[].price.additional[].suppliedAmount.currency` | enum:KRW | (통화 칸 없음 — product_option_price 는 amount 만) | 칸 없음 | 사용자 11-20 「통화는 KOS 와 같게」(K6-16) · 시술기기약품.har#74 |
| 6 | `data[].options[].price.additional[].suppliedAmount.value` | int | (product_option_price 는 amount 만 · 옵션 본가격은 product_option.supplied_amount 등에 있음) | 칸 없음 | 수가 유형별 공급가 · 부가세 · 면세 · 과세 · 시술기기약품.har#74 |
| 7 | `data[].options[].price.additional[].taxFreeAmount` | object |  | 해당 없음 | 묶음 · 시술기기약품.har#74 |
| 8 | `data[].options[].price.additional[].taxFreeAmount.currency` | enum:KRW | (통화 칸 없음 — product_option_price 는 amount 만) | 칸 없음 | 사용자 11-20 「통화는 KOS 와 같게」(K6-16) · 시술기기약품.har#74 |
| 9 | `data[].options[].price.additional[].taxFreeAmount.value` | int | (product_option_price 는 amount 만 · 옵션 본가격은 product_option.supplied_amount 등에 있음) | 칸 없음 | 수가 유형별 공급가 · 부가세 · 면세 · 과세 · 시술기기약품.har#74 |
| 10 | `data[].options[].price.additional[].taxation` | string | (product_option_price 는 amount 만 · 옵션 본가격은 product_option.supplied_amount 등에 있음) | 칸 없음 | 수가 유형별 공급가 · 부가세 · 면세 · 과세 · 시술기기약품.har#74 |
| 11 | `data[].options[].price.additional[].vatAmount` | object |  | 해당 없음 | 묶음 · 시술기기약품.har#74 |
| 12 | `data[].options[].price.additional[].vatAmount.currency` | enum:KRW | (통화 칸 없음 — product_option_price 는 amount 만) | 칸 없음 | 사용자 11-20 「통화는 KOS 와 같게」(K6-16) · 시술기기약품.har#74 |
| 13 | `data[].options[].price.additional[].vatAmount.value` | int | (product_option_price 는 amount 만 · 옵션 본가격은 product_option.supplied_amount 등에 있음) | 칸 없음 | 수가 유형별 공급가 · 부가세 · 면세 · 과세 · 시술기기약품.har#74 |
| 14 | `data[].options[].price.additional[].visitorType` | object | product_option_price.customer_type_id (models/menu.py:135) | 저장됨 | emr/kos/mapper_menu.py:86-88 · 시술기기약품.har#74 |
| 15 | `data[].options[].price.additional[].visitorType.id` | string | product_option_price.customer_type_id (models/menu.py:135) | 저장됨 | emr/kos/mapper_menu.py:86-88 · 시술기기약품.har#74 |
| 16 | `data[].options[].price.additional[].visitorType.name` | string | join customer_type.name (models/customer.py:120) | 계산으로 대체 | 시술기기약품.har#74 |

#### P33 `schedule/v2/queries/get-schedules-for-reservation` — 새 키 **87** · 표 행 **87** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data[].reservation.desiredDischargeDateTimeUtc` | string(ISO UTC) | visit.desired_discharge_at (models/visit.py:84) | 저장됨 | emr/kos/mapper.py:587 · 예약내역.har#6 |
| 2 | `data[].reservation.requestedProcedures[].optionConfiguration` | object |  | 해당 없음 | 묶음 · 예약내역.har#6 |
| 3 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[]` | array / array(empty) / object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 4 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 5 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.caution` | string(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 6 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 7 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.code` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 8 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.healthcareReimbursement` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 9 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.machines[]` | array / object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 10 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.machines[].id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 11 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.machines[].name` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 12 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.machines[].searchPhoneticName` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 13 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.medicines[]` | array(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 14 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.procedure` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 15 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 16 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.procedure.id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 17 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.procedure.name` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 18 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.procedure.searchPhoneticName` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 19 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.taxation` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 20 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.unit` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 21 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.unit.type` | enum:SHOT |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 22 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.configuration.unit.value` | number |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 23 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.deleted` | bool |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 24 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.description` | string(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 25 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.draftedDateTimeUtc` | string(ISO UTC) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 26 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 27 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.status` | enum:PUBLISHED |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 28 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.title` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 29 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 30 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 31 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 32 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.en` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 33 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.ja` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 34 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.ko` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 35 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.zh-Hans` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 36 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.zh-Hant` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 37 | `data[].reservation.requestedProcedures[].optionConfiguration.compositions[].medicalService.updatedDateTimeUtc` | string(ISO UTC) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 38 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 39 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.caution` | string(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 40 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 41 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.code` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 42 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.healthcareReimbursement` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 43 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.machines[]` | array(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 44 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.medicines[]` | array / object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 45 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.medicines[].id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 46 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.medicines[].name` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 47 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.medicines[].searchPhoneticName` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 48 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.procedure` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 49 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 50 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.procedure.id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 51 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.procedure.name` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 52 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.procedure.searchPhoneticName` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 53 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.taxation` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 54 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.unit` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 55 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.unit.type` | enum:UNIT |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 56 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.configuration.unit.value` | number |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 57 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.deleted` | bool |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 58 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.description` | string(empty) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 59 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.draftedDateTimeUtc` | string(ISO UTC) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 60 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.id` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 61 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.status` | enum:PUBLISHED |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 62 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.title` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 63 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 64 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 65 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation` | object |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 66 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation.en` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 67 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation.ja` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 68 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation.ko` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 69 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation.zh-Hans` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 70 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.translsMap.title.translation.zh-Hant` | string |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 71 | `data[].reservation.requestedProcedures[].optionConfiguration.medicalService.updatedDateTimeUtc` | string(ISO UTC) |  | 일부러 안 둠 | S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」 · 예약내역.har#6 |
| 72 | `data[].reservation.requestedProcedures[].optionConfiguration.optionId` | string | visit_requested_procedure.product_option_id (models/visit.py:105) | 칸 있음 · 미동기화 | S0:551 「1차는 비워 둔다 · 채울지는 OQ-041-7」 · emr/kos/mapper.py:333-336 · 예약내역.har#6 |
| 73 | `data[].reservation.requestedProcedures[].optionConfiguration.optionTitle` | string | visit_requested_procedure.option_title (models/visit.py:109) | 저장됨 | emr/kos/mapper.py:356 · 예약내역.har#6 |
| 74 | `data[].reservation.requestedProcedures[].optionConfiguration.optionType` | enum:GROUP|SINGLE | visit_requested_procedure.option_type (models/visit.py:110) | 저장됨 | emr/kos/mapper.py:357 · 예약내역.har#6 |
| 75 | `data[].reservation.requestedProcedures[].optionConfiguration.price` | object |  | 해당 없음 | 묶음 · 예약내역.har#6 |
| 76 | `data[].reservation.requestedProcedures[].optionConfiguration.price.amount` | int | visit_requested_procedure.price_amount (models/visit.py:111) | 저장됨 | emr/kos/mapper.py:358 · 예약내역.har#6 |
| 77 | `data[].reservation.requestedProcedures[].optionConfiguration.price.currency` | enum:KRW | visit_requested_procedure.currency (models/visit.py:112) | 저장됨 | emr/kos/mapper.py:359 · 예약내역.har#6 |
| 78 | `data[].reservation.requestedProcedures[].optionConfiguration.price.reason` | object |  | 일부러 안 둠 | S0:510 「가격 사유(정상가 · 수가 유형가) … 두지 않는다」 · 예약내역.har#6 |
| 79 | `data[].reservation.requestedProcedures[].optionConfiguration.price.reason.type` | enum:GENERAL |  | 일부러 안 둠 | S0:510 「가격 사유(정상가 · 수가 유형가) … 두지 않는다」 · 예약내역.har#6 |
| 80 | `data[].reservation.requestedProcedures[].optionConfiguration.productTitle` | string | visit_requested_procedure.product_title (models/visit.py:108) | 저장됨 | emr/kos/mapper.py:355 · 예약내역.har#6 |
| 81 | `data[].reservation.requestedProcedures[].optionConfiguration.translsMap` | object |  | 칸 없음 | 희망 옵션 · 상품 이름 번역 · 예약내역.har#6 |
| 82 | `data[].reservation.requestedProcedures[].optionConfiguration.translsMap.optionTitle` | object |  | 칸 없음 | 희망 옵션 · 상품 이름 번역 · 예약내역.har#6 |
| 83 | `data[].reservation.requestedProcedures[].optionConfiguration.translsMap.optionTitle.translation` | object(empty) |  | 칸 없음 | 희망 옵션 · 상품 이름 번역 · 예약내역.har#6 |
| 84 | `data[].reservation.requestedProcedures[].optionConfiguration.translsMap.productTitle` | object |  | 칸 없음 | 희망 옵션 · 상품 이름 번역 · 예약내역.har#6 |
| 85 | `data[].reservation.requestedProcedures[].optionConfiguration.translsMap.productTitle.translation` | object(empty) |  | 칸 없음 | 희망 옵션 · 상품 이름 번역 · 예약내역.har#6 |
| 86 | `data[].reservation.requestedProcedures[].type` | enum:OPTION | visit_requested_procedure.kind (models/visit.py:104) | 저장됨 | emr/kos/mapper.py:337 · 예약내역.har#6 |
| 87 | `data[].reservationTagIds[]` | array(empty) |  | 칸 없음 | 예약 태그 id — DAY 칸 없음 · 예약내역.har#6 |


## N4. 예약 현황 · 칸 정원 · 병원 설정 재료

### N4-1. 예약 현황 화면이 부르는 것(예약현황.har · 요청 본문 키 · 날짜는 캡처일 기준)

| 엔트리 | 경로 | 요청 본문 키(값 아님) | 날짜 범위 | 응답 |
|---|---|---|---|---|
| #1 · #30 · #37 · #42 | `get-default-days-off`(P27) | `startDateTime · endDateTime` | D-1~D+0 · D+0~D+1 · D+1~D+2 · D+2~D+3 | 빈 배열 4 |
| #3 | `get-default-operation-timetable`(P26) | 없음(빈 객체) | — | 요일 7 × `{enabled, startTime, endTime, breaktime{startTime,endTime}}` |
| #5 · #32 · #39 · #44 | `get-occupied-times`(K1-2 #31) | `dateTimeRange{startDateTimeUtc,endDateTimeUtc} · deleted` | 위와 같음 | 빈 배열 4 |
| #9 | `get-zones`(P01) | — | — | 2차와 같은 5키 |
| #11 · #14 | `get-reservation-groups`(P03) | `deleted · zoneIds[]` | — | 그룹 13개(건수만) · 2차와 같은 63키 |
| #19 · #29 · #36 · #41 | `get-reservation-group-days-offs`(K1-2 #30) | `reservationGroupIds[] · startDateTime · endDateTime` | 위와 같음 | 빈 배열 4 |
| #21 · #31 · #38 · #43 | `get-schedules-for-reservation`(P33) | `baseDateUtc · reservationGroupIds[] · zoneIds[]` | D-1 · D+0 · D+1 · D+2 | 일정 10 · 0 · 0 · 0건 |

- **미래 날짜는 P33 `baseDateUtc` 를 날짜마다 바꿔 부른다** — DAY 는 P33 을 부르지 않고 P07 을 오늘 창만 부른다(2차 R1 · `services/emr_sync.py:111-115`). 데모라 미래 일정이 0건이어서 미래 응답의 키 모양은 이번에도 못 봤다(오늘 일정 응답과 같은 경로라 같은 모양일 것으로 보이나 확인 안 됨).
- **그룹 정원**: `get-reservation-groups.data[].intervalCapacities[]{zoneId, intervalCapacity, enabled}` + `intervalMinutes` — DAY 가 이미 `reservation_group_capacity` · `reservation_group.interval_minutes` 로 저장(2차 P03 · `emr/kos/mapper.py:189-203`). 예약현황.har 에서 바뀐 키 0.
- **칸별 예약 수 · 남은 자리**: 3차 HAR 의 어느 내부 응답에도 `capacity` · `reservationCount` 꼴 키가 없다. 예약 칸 경로 `get-reservation-time-slots`(예약등록.har#28 등 200 응답 6개 · 각 32칸)는 칸마다 `available` · `offeringPeriodViolated` · `reservationPolicyViolated` **bool 만** 준다(3차 관찰: 모든 칸 `available` true). → **P28(공개 · `capacity` · `reservationCount` — cc 가 읽던 값, 1차 E4 · `cc:kos/reservation_sync.py:29` · `cc:service/ext.py:470-479`)을 같은 정보로 대신할 내부 경로는 HAR 에 없다.** S0:907 · S0:1002 의 「정원과 방문 점유에서 계산」 재료 = P03 정원 + P33(또는 P07) 미래 일정의 `occupiedResources[]`.
- **병원 기본 운영 시간**: P26(예약현황.har#3 등 5응답) 키 50 = 2차와 같음 · 새 키 0 — 판정은 2차 K2 P26 그대로(칸 없음 49 · 해당 없음 1 — 「새 표 필요(병원 기본 운영 시간)」). 모양: 요일 `startTime` · `endTime` 이 **string(ISO UTC)**(날짜 붙은 시각) · `breaktime` 은 3차에서 늘 빈 문자열. 그룹 시간표 `operationTimetable` 도 같은 모양(DAY `reservation_group_timetable` 은 `time` — `models/room.py:86-90` · S0:908 「현지 시계 시간」).
- **병원 정보**: P25(병원설정.har#7) 키 22 = 2차와 같음 · 새 키 0 — 2차 K2 P25 판정 그대로(칸 없음 13 · 일부러 안 둠 6 · 시점 다름 1 · 확인 안 됨 1 · 해당 없음 1). 사용자 11-20 「병원 설정 그대로 DB」로 `S0:278` 근거의 `일부러 안 둠` 6 은 뒤집힘 대상(_RESUME §2) — 판정 칸은 2차 기준 그대로 두고 N7 에서 따로 센다.
- **휴무**: 기본(P27) · 그룹(K1-2 #30) · 점유 시간(#31) · 예약 정책(#28) — 3차에도 키 못 봄(N2 · 아래 표 `확인 안 됨`).

### N4-2. 새로 대조한 내부 경로 8 — 121키

판정: 그룹 단건(#29)은 P03 과 같은 객체라 2차 P03 규칙 그대로(저장됨 = P03 경로로 이미 받음). 예약 규칙(#32 · #33) · 예약 칸(#34 · #35)은 DAY 칸 · S0 언급이 없어 `칸 없음`(안쪽 객체 · 배열은 `해당 없음`, 빈 값만 본 것은 `확인 안 됨`).

#### K1-2 #29 `schedule/group/v1/queries/get-reservation-group`

스크립트 키 **63** · 표 행 **63** · 빠진 키 **0** · 키 집합 = P03 과 같음(`data.` ↔ `data[].`)

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data` | object |  | 해당 없음 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · 응답 껍데기 · 목록 · 상담기록.har#8 |
| 2 | `data.id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:203 · 상담기록.har#8 |
| 3 | `data.intervalCapacities[]` | array / object | reservation_group_capacity (models/room.py:68) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:189-201 · 상담기록.har#8 |
| 4 | `data.intervalCapacities[].enabled` | bool | 행 있음 = 켜짐 | 계산으로 대체 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:190-191 — 꺼진 구역은 행을 만들지 않는다 · 상담기록.har#8 |
| 5 | `data.intervalCapacities[].intervalCapacity` | int | reservation_group_capacity.capacity (models/room.py:74) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:197-199 · 상담기록.har#8 |
| 6 | `data.intervalCapacities[].zoneId` | string | reservation_group_capacity.zone_id (models/room.py:73) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:194-196 · 상담기록.har#8 |
| 7 | `data.intervalMinutes` | int | reservation_group.interval_minutes (models/room.py:61) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:206 · 상담기록.har#8 |
| 8 | `data.isDefault` | bool |  | 칸 없음 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · 기본 예약 그룹 — cc ext E4 가 「기본 그룹」을 쓴다 · 상담기록.har#8 |
| 9 | `data.memo` | string(empty) |  | 칸 없음 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · 상담기록.har#8 |
| 10 | `data.operationTimetable` | object | reservation_group_timetable (models/room.py:80) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:165-183 · 상담기록.har#8 |
| 11 | `data.operationTimetable.friday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:125-133 · 168 · 상담기록.har#8 |
| 12 | `data.operationTimetable.friday.breaktime` | object |  | 해당 없음 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · 묶음 · 상담기록.har#8 |
| 13 | `data.operationTimetable.friday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:180 · 상담기록.har#8 |
| 14 | `data.operationTimetable.friday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:179 · 상담기록.har#8 |
| 15 | `data.operationTimetable.friday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:174-176 · 상담기록.har#8 |
| 16 | `data.operationTimetable.friday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:178 · 상담기록.har#8 |
| 17 | `data.operationTimetable.friday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 · 상담기록.har#8 |
| 18 | `data.operationTimetable.monday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:125-133 · 168 · 상담기록.har#8 |
| 19 | `data.operationTimetable.monday.breaktime` | object |  | 해당 없음 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · 묶음 · 상담기록.har#8 |
| 20 | `data.operationTimetable.monday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:180 · 상담기록.har#8 |
| 21 | `data.operationTimetable.monday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:179 · 상담기록.har#8 |
| 22 | `data.operationTimetable.monday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:174-176 · 상담기록.har#8 |
| 23 | `data.operationTimetable.monday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:178 · 상담기록.har#8 |
| 24 | `data.operationTimetable.monday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 · 상담기록.har#8 |
| 25 | `data.operationTimetable.saturday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:125-133 · 168 · 상담기록.har#8 |
| 26 | `data.operationTimetable.saturday.breaktime` | object |  | 해당 없음 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · 묶음 · 상담기록.har#8 |
| 27 | `data.operationTimetable.saturday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:180 · 상담기록.har#8 |
| 28 | `data.operationTimetable.saturday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:179 · 상담기록.har#8 |
| 29 | `data.operationTimetable.saturday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:174-176 · 상담기록.har#8 |
| 30 | `data.operationTimetable.saturday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:178 · 상담기록.har#8 |
| 31 | `data.operationTimetable.saturday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 · 상담기록.har#8 |
| 32 | `data.operationTimetable.sunday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:125-133 · 168 · 상담기록.har#8 |
| 33 | `data.operationTimetable.sunday.breaktime` | object |  | 해당 없음 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · 묶음 · 상담기록.har#8 |
| 34 | `data.operationTimetable.sunday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:180 · 상담기록.har#8 |
| 35 | `data.operationTimetable.sunday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:179 · 상담기록.har#8 |
| 36 | `data.operationTimetable.sunday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:174-176 · 상담기록.har#8 |
| 37 | `data.operationTimetable.sunday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:178 · 상담기록.har#8 |
| 38 | `data.operationTimetable.sunday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 · 상담기록.har#8 |
| 39 | `data.operationTimetable.thursday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:125-133 · 168 · 상담기록.har#8 |
| 40 | `data.operationTimetable.thursday.breaktime` | object |  | 해당 없음 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · 묶음 · 상담기록.har#8 |
| 41 | `data.operationTimetable.thursday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:180 · 상담기록.har#8 |
| 42 | `data.operationTimetable.thursday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:179 · 상담기록.har#8 |
| 43 | `data.operationTimetable.thursday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:174-176 · 상담기록.har#8 |
| 44 | `data.operationTimetable.thursday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:178 · 상담기록.har#8 |
| 45 | `data.operationTimetable.thursday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 · 상담기록.har#8 |
| 46 | `data.operationTimetable.tuesday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:125-133 · 168 · 상담기록.har#8 |
| 47 | `data.operationTimetable.tuesday.breaktime` | object |  | 해당 없음 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · 묶음 · 상담기록.har#8 |
| 48 | `data.operationTimetable.tuesday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:180 · 상담기록.har#8 |
| 49 | `data.operationTimetable.tuesday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:179 · 상담기록.har#8 |
| 50 | `data.operationTimetable.tuesday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:174-176 · 상담기록.har#8 |
| 51 | `data.operationTimetable.tuesday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:178 · 상담기록.har#8 |
| 52 | `data.operationTimetable.tuesday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 · 상담기록.har#8 |
| 53 | `data.operationTimetable.wednesday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:125-133 · 168 · 상담기록.har#8 |
| 54 | `data.operationTimetable.wednesday.breaktime` | object |  | 해당 없음 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · 묶음 · 상담기록.har#8 |
| 55 | `data.operationTimetable.wednesday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:180 · 상담기록.har#8 |
| 56 | `data.operationTimetable.wednesday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:179 · 상담기록.har#8 |
| 57 | `data.operationTimetable.wednesday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:174-176 · 상담기록.har#8 |
| 58 | `data.operationTimetable.wednesday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:178 · 상담기록.har#8 |
| 59 | `data.operationTimetable.wednesday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 · 상담기록.har#8 |
| 60 | `data.order` | int | reservation_group.sort_order (models/room.py:60) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:205 · 상담기록.har#8 |
| 61 | `data.sameDayCloseBufferMinutes` | int | reservation_group.same_day_close_buffer_minutes (models/room.py:62) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:207 · 상담기록.har#8 |
| 62 | `data.startDate` | string(ISO UTC) |  | 칸 없음 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · 그룹 시작일 · 상담기록.har#8 |
| 63 | `data.title` | string | reservation_group.title (models/room.py:59) | 저장됨 | P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음 · emr/kos/mapper.py:204 · 상담기록.har#8 |

#### K1-2 #30 `schedule/group/v1/queries/get-reservation-group-days-offs`

스크립트 키 **1** · 표 행 **1** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data[]` | array(empty) |  | 확인 안 됨 | 3차 응답 7개 모두 빈 배열(예약현황.har 미래 3일 범위 포함) — 안쪽 키 확인 안 됨 · 예약내역.har#3 |

#### K1-2 #31 `schedule/occupied-time/v2/queries/get-occupied-times`

스크립트 키 **1** · 표 행 **1** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data[]` | array(empty) |  | 확인 안 됨 | 3차 응답 7개 모두 빈 배열 — 안쪽 키 확인 안 됨 · 예약내역.har#4 |

#### K1-2 #28 `schedule/default-operation-time/v1/queries/get-default-reservation-policy`

스크립트 키 **1** · 표 행 **1** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data` | object(empty) |  | 확인 안 됨 | 3차 응답 2개 모두 빈 객체 — 안쪽 키 확인 안 됨 · 예약등록.har#22 |

#### K1-2 #32 `schedule/reservation-rule/v1/queries/get-reservation-rule`

스크립트 키 **27** · 표 행 **27** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data` | object |  | 해당 없음 | 묶음 · 예약등록.har#29 |
| 2 | `data.events[]` | array / object |  | 해당 없음 | 묶음 · 예약등록.har#29 |
| 3 | `data.events[].eventType` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 4 | `data.events[].initiator` | object |  | 해당 없음 | 묶음 · 예약등록.har#29 |
| 5 | `data.events[].initiator.account` | object |  | 해당 없음 | 묶음 · 예약등록.har#29 |
| 6 | `data.events[].initiator.account.id` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 7 | `data.events[].initiator.account.name` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 8 | `data.events[].occurredDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 9 | `data.events[].payload` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 10 | `data.events[].reservationRuleId` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 11 | `data.id` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 12 | `data.isActive` | bool |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 13 | `data.isDefault` | bool |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 14 | `data.ruleSet` | object |  | 해당 없음 | 묶음 · 예약등록.har#29 |
| 15 | `data.ruleSet.components[]` | array / object |  | 해당 없음 | 묶음 · 예약등록.har#29 |
| 16 | `data.ruleSet.components[].rule` | object |  | 해당 없음 | 묶음 · 예약등록.har#29 |
| 17 | `data.ruleSet.components[].rule.occupancyTarget` | object |  | 해당 없음 | 묶음 · 예약등록.har#29 |
| 18 | `data.ruleSet.components[].rule.occupancyTarget.reservationGroup` | object |  | 해당 없음 | 묶음 · 예약등록.har#29 |
| 19 | `data.ruleSet.components[].rule.occupancyTarget.reservationGroup.id` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 20 | `data.ruleSet.components[].rule.occupancyTarget.zoneIds[]` | array(empty) |  | 확인 안 됨 | 빈 값만 관찰 — 안쪽 키 확인 안 됨 · 예약등록.har#29 |
| 21 | `data.ruleSet.components[].rule.requestedProcedureRepetition` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 22 | `data.ruleSet.components[].rule.title` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 23 | `data.ruleSet.occupancyPolicy` | enum:ALL_MATCHED_SEQUENTIAL |  | 확인 안 됨 | 빈 값만 관찰 — 안쪽 키 확인 안 됨 · 예약등록.har#29 |
| 24 | `data.ruleSet.requestedProcedureRepetition` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 25 | `data.ruleSet.title` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |
| 26 | `data.ruleSet.zoneOccupancyPolicy` | enum:SINGLE_ZONE_ONLY |  | 확인 안 됨 | 빈 값만 관찰 — 안쪽 키 확인 안 됨 · 예약등록.har#29 |
| 27 | `data.title` | string |  | 칸 없음 | 예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0) · 예약등록.har#29 |

#### K1-2 #33 `schedule/reservation-rule/v1/queries/get-reservation-rule-summaries`

스크립트 키 **11** · 표 행 **11** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 묶음 · 예약등록.har#23 |
| 2 | `data[].createdDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 예약 규칙 목록 — DAY 칸 없음 · 예약등록.har#23 |
| 3 | `data[].id` | string |  | 칸 없음 | 예약 규칙 목록 — DAY 칸 없음 · 예약등록.har#23 |
| 4 | `data[].isActive` | bool |  | 칸 없음 | 예약 규칙 목록 — DAY 칸 없음 · 예약등록.har#23 |
| 5 | `data[].isDefault` | bool |  | 칸 없음 | 예약 규칙 목록 — DAY 칸 없음 · 예약등록.har#23 |
| 6 | `data[].lastModifiedBy` | object |  | 해당 없음 | 묶음 · 예약등록.har#23 |
| 7 | `data[].lastModifiedBy.account` | object |  | 해당 없음 | 묶음 · 예약등록.har#23 |
| 8 | `data[].lastModifiedBy.account.id` | string |  | 칸 없음 | 예약 규칙 목록 — DAY 칸 없음 · 예약등록.har#23 |
| 9 | `data[].lastModifiedBy.account.name` | string |  | 칸 없음 | 예약 규칙 목록 — DAY 칸 없음 · 예약등록.har#23 |
| 10 | `data[].title` | string |  | 칸 없음 | 예약 규칙 목록 — DAY 칸 없음 · 예약등록.har#23 |
| 11 | `data[].updatedDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 예약 규칙 목록 — DAY 칸 없음 · 예약등록.har#23 |

#### K1-2 #34 `schedule/reservation-time-slot/v1/queries/get-occupied-resources-by-reservation-time-slot`

스크립트 키 **9** · 표 행 **9** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 묶음 · 예약등록.har#42 |
| 2 | `data[].dateTimeRangeUtc` | object |  | 해당 없음 | 묶음 · 예약등록.har#42 |
| 3 | `data[].dateTimeRangeUtc.endDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 예약 쓰기 화면이 시각 범위 · 규칙을 보내 받는 점유 자원(요청 본문 키: dateTimeRangeUtc · reservationRuleId · requestedProcedureOptionIds …) · 예약등록.har#42 |
| 4 | `data[].dateTimeRangeUtc.startDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 예약 쓰기 화면이 시각 범위 · 규칙을 보내 받는 점유 자원(요청 본문 키: dateTimeRangeUtc · reservationRuleId · requestedProcedureOptionIds …) · 예약등록.har#42 |
| 5 | `data[].reservationGroup` | object |  | 해당 없음 | 묶음 · 예약등록.har#42 |
| 6 | `data[].reservationGroup.doctors[]` | array(empty) |  | 확인 안 됨 | 빈 값만 관찰 — 안쪽 키 확인 안 됨 · 예약등록.har#42 |
| 7 | `data[].reservationGroup.reservationGroupId` | string |  | 칸 없음 | 예약 쓰기 화면이 시각 범위 · 규칙을 보내 받는 점유 자원(요청 본문 키: dateTimeRangeUtc · reservationRuleId · requestedProcedureOptionIds …) · 예약등록.har#42 |
| 8 | `data[].reservationGroup.zoneId` | string |  | 칸 없음 | 예약 쓰기 화면이 시각 범위 · 규칙을 보내 받는 점유 자원(요청 본문 키: dateTimeRangeUtc · reservationRuleId · requestedProcedureOptionIds …) · 예약등록.har#42 |
| 9 | `data[].type` | enum:RESERVATION_GROUP |  | 확인 안 됨 | 빈 값만 관찰 — 안쪽 키 확인 안 됨 · 예약등록.har#42 |

#### K1-2 #35 `schedule/reservation-time-slot/v1/queries/get-reservation-time-slots`

스크립트 키 **8** · 표 행 **8** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 묶음 · 예약등록.har#28 |
| 2 | `data[].available` | bool |  | 칸 없음 | 예약 칸 가능 여부 — 정원 · 예약 수는 없다(bool 만) · 예약등록.har#28 |
| 3 | `data[].dateTimeRangeUtc` | object |  | 해당 없음 | 묶음 · 예약등록.har#28 |
| 4 | `data[].dateTimeRangeUtc.endDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 예약 칸 가능 여부 — 정원 · 예약 수는 없다(bool 만) · 예약등록.har#28 |
| 5 | `data[].dateTimeRangeUtc.startDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 예약 칸 가능 여부 — 정원 · 예약 수는 없다(bool 만) · 예약등록.har#28 |
| 6 | `data[].offeringPeriodViolated` | bool |  | 칸 없음 | 예약 칸 가능 여부 — 정원 · 예약 수는 없다(bool 만) · 예약등록.har#28 |
| 7 | `data[].reservationPolicyViolated` | bool |  | 칸 없음 | 예약 칸 가능 여부 — 정원 · 예약 수는 없다(bool 만) · 예약등록.har#28 |
| 8 | `timeSlotIntervalMinutes` | int |  | 칸 없음 | 예약 칸 가능 여부 — 정원 · 예약 수는 없다(bool 만) · 예약등록.har#28 |

## N5. 고객별 일정 · 문진 · 일정 이력의 내부 경로

### N5-1. cc 가 공개 P29 · P30 · P31 · 내부 P32 에서 읽는 키(cc `origin/main` 0553173)

| 경로 | cc 가 읽는 곳 | 읽는 키 |
|---|---|---|
| P29 `get-schedules-by-visitor{visitorId}` | `cc:service/ext.py:482-545`(`visits` · `reservations`) · `cc:service/reservations.py:598-623`(이전 방문) | `data[]` 의 `id` · `deleted` · `occupiedResources[].reservationTime.{start,end}DateTimeUtc` · `reservationGroup.{reservationGroupId, zoneId, doctors[]}` · `reservation.{startDateTime, status, reservationGroupId, zoneId}` · `flowStep` · `zone.id` · `tasks[].{type, title, status, completedDateTimeUtc}` · `consultations[].consultationStartedDateTimeUtc`(`cc:domain/reservation_rules.py:355-376` · `cc:kos/reservation_sync.py:80-98`) |
| P30 `get-visitor-questionnaire{visitorId}` | `cc:service/questionnaire.py:140` · `cc:service/reservations.py:598` | `pages[].{title, questions[].{questionId, title, sequence}}`(`cc:domain/reservation_rules.py:330-348`) |
| P31 `get-questionnaire-submit{visitorId}` | `cc:service/questionnaire.py:170` · `cc:service/reservations.py:599 · 614-648` | `createdDateTimeUtc` · `answers[].{questionId, seq, answerTitle, memo}` · 오류 `visitorId NotFound` = 제출본 없음 |
| P32 `get-schedule-event-logs{scheduleId}`(내부) | `cc:service/ext.py:796-820` | `data[].{eventType(끝 조각 FlowStepChanged), payload(JSON 문자열 · flowStep), raisedDateTimeUtc}` |

### N5-2. 내부 후보와의 사실 대조

| 공개/내부 | 3차 내부 후보 | 같은 정보인가(사실만) |
|---|---|---|
| P29 | `get-schedules-summarized-by-task{visitorId}`(예약내역.har#56 · 일정 4) | 일정 id(`scheduleId` = P33 `data[].id` 4/4) · `tasks[]`(P33 `tasks[]` 와 같은 키) 는 있다. **cc 가 읽는 `reservation.status` · `flowStep` · `deleted` · `occupiedResources[]` · `consultations[]` 는 없다.** `startDateTimeUtc` · `endDateTimeUtc` 는 같은 일정의 예약 시작 · 점유 · 접수 · 생성 · 작업 시각 어느 것과도 같지 않다(4건 · 늘 30분 · 같은 날 — 뜻 확인 안 됨) |
| P29 | `get-schedule-list-items`(예약내역.har#19 · 14행) | **고객 id 로 부르지 않는다**(본문 `updatedDateTimeUtcFrom/To · limit` — 수정 시각 창 목록). 같은 날 P33(#6)과 겹친 11행에서 `reservationStartDateTime` = `reservation.startDateTime` · `reservationStatus` = `reservation.status` · `occupiedReservationGroups[].{start,end}DateTimeUtc` = `occupiedResources[].reservationTime.*` · `counselor` = `reservation.counselor` · `reservationAssignee` · `reservationMemo` · `funnel` · `zone` · `createdDateTimeUtc` · `updatedDateTimeUtc` 모두 11/11 같은 값(빈 값은 빈 값끼리) · `requestedProcedureTitles[]` = 희망 시술 `optionTitle` 목록 11/11. **`flowStep` · `deleted` · `tasks[]` · `consultations[]` 는 없다** |
| P29(구매) | `get-purchase-summaries-by-visitor-id`(예약내역.har#52) | 고객별 구매 — 키 235 모두 P15 합집합 안(새 키 0). P29 대응이 아니라 2차 R4 「오늘 밖 고객의 구매」와 닿는 경로 |
| P30 | 없음 | 3차 HAR 에 문진 **양식** 경로 0 |
| P31 | `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` | 3차 3응답 모두 400 `visitorId NotFound`(N2-2) — 200 응답 0이라 키 대조 불가. 2차 HAR 의 200 응답 3건 키 36(2차 K1-2 #42)은 이번 범위 밖(대조 안 함) |
| P32 | 없음 | 3차 HAR 에 `get-schedule-event-logs` 0. 예약 규칙 단건(#32)의 `events[]{eventType, payload(string), occurredDateTimeUtc, initiator}` 가 꼴이 비슷하나 **예약 규칙의 이력**이고 일정 이력이 아니다 |

### N5-3. 키 전수 대조 — 168키

판정: 두 경로 모두 P33 과 같은 일정 객체 조각이라 **2차 P33 규칙**으로 판정(`get-schedule-list-items` 는 이름이 다른 키를 P33 키로 대응 — 비고 「= P33 `…`」 · 대응 11쌍은 부록 A `gen3.py ALIAS`). `저장됨` = 같은 값을 P07 · P33 일정 객체로 이미 받는다는 뜻(2차 기준 「새로 필요」 경로 규칙).

#### K1-2 #38 `schedule/v2/queries/get-schedule-list-items`

스크립트 키 **54** · 표 행 **54** · 빠진 키 **0** · 요청 본문 키 = `tenantId` · `updatedDateTimeUtcFrom` · `updatedDateTimeUtcTo` · `limit`(고객 id 없음 — 예약내역.har#19)

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | = P33 같은 키 · DAY 는 이 경로를 부르지 않음 — 판정은 같은 칸을 grouped-by-zone 동기화가 채우는지 기준 · 예약내역.har#19 |
| 2 | `data[].counselor` | object | visit.requested_counselor_id (models/visit.py:77) | 저장됨 | = P33 `data[].reservation.counselor` · emr/kos/mapper.py:572-574 — 예약 지정 희망 상담사(앞 판 M1) · 예약내역.har#19 |
| 3 | `data[].counselor.id` | string | visit.requested_counselor_id (models/visit.py:77) | 저장됨 | = P33 `data[].reservation.counselor.id` · emr/kos/mapper.py:572-574 — 예약 지정 희망 상담사(앞 판 M1) · 예약내역.har#19 |
| 4 | `data[].counselor.name` | string | join staff.name (models/staff.py:51) | 계산으로 대체 | = P33 `data[].reservation.counselor.name` · 예약내역.har#19 |
| 5 | `data[].createdDateTimeUtc` | string(ISO UTC) | visit.booked_at (models/visit.py:68) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:559 · 예약내역.har#19 |
| 6 | `data[].funnel` | object |  | 해당 없음 | = P33 `data[].reservation.funnel` · 묶음 · 예약내역.har#19 |
| 7 | `data[].funnel.funnel` | object | visit.funnel_id (models/visit.py:79) | 저장됨 | = P33 `data[].reservation.funnel.funnel` · emr/kos/mapper.py:578 · 예약내역.har#19 |
| 8 | `data[].funnel.funnel.category` | enum:FUNNEL | join funnel (models/customer.py:145-153) | 계산으로 대체 | = P33 `data[].reservation.funnel.funnel.category` · funnel 표는 get-codes FUNNEL 로 채운다(emr/kos/mapper.py:269-280) · 예약내역.har#19 |
| 9 | `data[].funnel.funnel.closed` | bool | join funnel (models/customer.py:145-153) | 계산으로 대체 | = P33 `data[].reservation.funnel.funnel.closed` · funnel 표는 get-codes FUNNEL 로 채운다(emr/kos/mapper.py:269-280) · 예약내역.har#19 |
| 10 | `data[].funnel.funnel.default` | bool | join funnel (models/customer.py:145-153) | 계산으로 대체 | = P33 `data[].reservation.funnel.funnel.default` · funnel 표는 get-codes FUNNEL 로 채운다(emr/kos/mapper.py:269-280) · 예약내역.har#19 |
| 11 | `data[].funnel.funnel.id` | string(uuid) | visit.funnel_id (models/visit.py:79) | 저장됨 | = P33 `data[].reservation.funnel.funnel.id` · emr/kos/mapper.py:578 · 예약내역.har#19 |
| 12 | `data[].funnel.funnel.name` | string | join funnel (models/customer.py:145-153) | 계산으로 대체 | = P33 `data[].reservation.funnel.funnel.name` · funnel 표는 get-codes FUNNEL 로 채운다(emr/kos/mapper.py:269-280) · 예약내역.har#19 |
| 13 | `data[].funnel.funnel.order` | int | join funnel (models/customer.py:145-153) | 계산으로 대체 | = P33 `data[].reservation.funnel.funnel.order` · funnel 표는 get-codes FUNNEL 로 채운다(emr/kos/mapper.py:269-280) · 예약내역.har#19 |
| 14 | `data[].funnel.funnelDetail` | string(empty) | visit.funnel_detail (models/visit.py:80) | 저장됨 | = P33 `data[].reservation.funnel.funnelDetail` · emr/kos/mapper.py:579 · 예약내역.har#19 |
| 15 | `data[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:555 · 예약내역.har#19 |
| 16 | `data[].occupiedReservationGroups[]` | array / object | visit_occupied_resource (models/room.py:96) | 저장됨 | = P33 `data[].occupiedResources[]` · emr/kos/mapper.py:542 · 예약내역.har#19 |
| 17 | `data[].occupiedReservationGroups[].doctors[]` | array(empty) | visit_occupied_resource_doctor (models/room.py:108) | 저장됨 | = P33 `data[].occupiedResources[].reservationGroup.doctors[]` · emr/kos/mapper.py:380-384 · 예약내역.har#19 |
| 18 | `data[].occupiedReservationGroups[].endDateTimeUtc` | string(ISO UTC) | visit_occupied_resource.end_at (models/room.py:104) | 저장됨 | = P33 `data[].occupiedResources[].reservationTime.endDateTimeUtc` · emr/kos/mapper.py:379 · 예약내역.har#19 |
| 19 | `data[].occupiedReservationGroups[].reservationGroupId` | string | visit_occupied_resource.reservation_group_id (models/room.py:101) | 저장됨 | = P33 `data[].occupiedResources[].reservationGroup.reservationGroupId` · emr/kos/mapper.py:372 · 예약내역.har#19 |
| 20 | `data[].occupiedReservationGroups[].startDateTimeUtc` | string(ISO UTC) | visit_occupied_resource.start_at (models/room.py:103) | 저장됨 | = P33 `data[].occupiedResources[].reservationTime.startDateTimeUtc` · emr/kos/mapper.py:378 · 예약내역.har#19 |
| 21 | `data[].requestedProcedureTitles[]` | array / array(empty) / string | visit_requested_procedure.option_title (models/visit.py:109) | 계산으로 대체 | 예약내역.har#19 ↔ #6 같은 일정 11건 대조 — `optionTitle` 목록과 11/11 같음(`productTitle` 과는 10/11) · 예약내역.har#19 |
| 22 | `data[].reservationAssignee` | object | visit.reservation_assignee_id (models/visit.py:76) | 저장됨 | = P33 `data[].reservation.reservationAssignee` · emr/kos/mapper.py:569-571 · 예약내역.har#19 |
| 23 | `data[].reservationAssignee.id` | string | visit.reservation_assignee_id (models/visit.py:76) | 저장됨 | = P33 `data[].reservation.reservationAssignee.id` · emr/kos/mapper.py:569-571 · 예약내역.har#19 |
| 24 | `data[].reservationAssignee.name` | string | join staff.name (models/staff.py:51) | 계산으로 대체 | = P33 `data[].reservation.reservationAssignee.name` · 예약내역.har#19 |
| 25 | `data[].reservationGroupId` | string | (visit_occupied_resource 쪽 칸은 있음 — 같은 값인지 확인 안 됨) | 칸 없음 | = P33 `data[].reservation.reservationGroupId` · S0:598 「visit 에 두지 않고 visit_occupied_resource 로」는 그룹 칸 얘기 — 이 키 자체의 결정은 없음 · 예약내역.har#19 |
| 26 | `data[].reservationMemo` | string | visit.reservation_notes (models/visit.py:75) | 저장됨 | = P33 `data[].reservation.reservationMemo` · emr/kos/mapper.py:568 · 예약내역.har#19 |
| 27 | `data[].reservationStartDateTime` | string(ISO UTC) | visit.reserved_start_at (models/visit.py:70) | 저장됨 | = P33 `data[].reservation.startDateTime` · emr/kos/mapper.py:560 · 예약내역.har#19 |
| 28 | `data[].reservationStatus` | enum:IN_PROGRESS|RESERVED | visit.reservation_status (models/visit.py:72) | 저장됨 | = P33 `data[].reservation.status` · emr/kos/mapper.py:564-567 · 예약내역.har#19 |
| 29 | `data[].reservationTagIds[]` | array(empty) |  | 칸 없음 | = P33 같은 키 · 예약 태그 id — DAY 칸 없음 · 예약내역.har#19 |
| 30 | `data[].updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:556 · emr/sync_schedules.py:271 · 예약내역.har#19 |
| 31 | `data[].visitor` | object | customer (models/customer.py:33) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:558 · 예약내역.har#19 |
| 32 | `data[].visitor.categories[]` | array(empty) | customer_category_link (models/customer.py:157) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:322-327 · 예약내역.har#19 |
| 33 | `data[].visitor.chartNumber` | string(digits) | customer.chart_number (models/customer.py:43) + external_ref.external_number (models/customer.py:107) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:308 · emr/sync_schedules.py:150 · 예약내역.har#19 |
| 34 | `data[].visitor.dateOfBirth` | string | customer.birth_date (models/customer.py:52) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:312 · 예약내역.har#19 |
| 35 | `data[].visitor.gender` | enum:GENDER_UNSPECIFIED|MALE | customer.gender (models/customer.py:51) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:311 — `GENDER_UNSPECIFIED` 는 None · 예약내역.har#19 |
| 36 | `data[].visitor.id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:307 · 예약내역.har#19 |
| 37 | `data[].visitor.isNew` | bool | visit.is_new (models/visit.py:91) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:597 — 방문마다 값(S0:301 · 360) · 예약내역.har#19 |
| 38 | `data[].visitor.memo` | string(empty) | customer.customer_notes (models/customer.py:72) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:316 · 예약내역.har#19 |
| 39 | `data[].visitor.name` | string | customer.name (models/customer.py:46) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:309 · 예약내역.har#19 |
| 40 | `data[].visitor.nationality` | string | customer.nationality (models/customer.py:53) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:313 · 예약내역.har#19 |
| 41 | `data[].visitor.phone` | object |  | 해당 없음 | = P33 같은 키 · 묶음 · 예약내역.har#19 |
| 42 | `data[].visitor.phone.countryCode` | string(digits) | customer.phone_country_code (models/customer.py:61) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:314 · 예약내역.har#19 |
| 43 | `data[].visitor.phone.phoneNumber` | string(digits) | customer.phone_number (models/customer.py:62) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:315 · 예약내역.har#19 |
| 44 | `data[].visitor.phoneticName` | string(empty) | customer.name_pronunciation (models/customer.py:47) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:310 · 예약내역.har#19 |
| 45 | `data[].visitor.snsInfo` | object |  | 해당 없음 | = P33 같은 키 · 묶음 · 예약내역.har#19 |
| 46 | `data[].visitor.snsInfo.accountId` | string(empty) | customer.sns_account_id (models/customer.py:70) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:318 · 예약내역.har#19 |
| 47 | `data[].visitor.snsInfo.snsType` | string | customer.sns_type (models/customer.py:69) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:317 · 예약내역.har#19 |
| 48 | `data[].visitor.visitorType` | object | customer.customer_type_id (models/customer.py:73) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:319-321 · 예약내역.har#19 |
| 49 | `data[].visitor.visitorType.id` | string / string(empty) | customer.customer_type_id (models/customer.py:73) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:319-321 · 예약내역.har#19 |
| 50 | `data[].visitor.visitorType.name` | string / string(empty) | customer_type.name (models/customer.py:120) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:319-321 · 예약내역.har#19 |
| 51 | `data[].zone` | object |  | 해당 없음 | = P33 같은 키 · 묶음 · 예약내역.har#19 |
| 52 | `data[].zone.id` | string | visit.reception_zone_id (models/visit.py:89) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:593 · 예약내역.har#19 |
| 53 | `data[].zone.title` | string | join zone.title (models/room.py:35) | 계산으로 대체 | = P33 같은 키 · 구역 이름 — 기준 정보 1시간 · 예약내역.har#19 |
| 54 | `totalCount` | int |  | 해당 없음 | count · 예약내역.har#19 |

#### 새 경로 `schedule/v2/queries/get-schedules-summarized-by-task`

스크립트 키 **114** · 표 행 **114** · 빠진 키 **0** · 요청 본문 키 = `visitorId`(예약내역.har#56) · 키 111 이 P33 합집합 안

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | = P33 같은 키 · DAY 는 이 경로를 부르지 않음 — 판정은 같은 칸을 grouped-by-zone 동기화가 채우는지 기준 · 예약내역.har#56 |
| 2 | `data[].endDateTimeUtc` | string(ISO UTC) |  | 확인 안 됨 | 같은 일정의 예약 시작 · 점유 · 접수 · 생성 · 작업 시각 어느 것과도 같지 않다(예약내역.har#56 ↔ #6 4건 · 늘 30분 · 같은 날) — 뜻 확인 안 됨 · 예약내역.har#56 |
| 3 | `data[].scheduleId` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | 일정 id — P07 · P33 의 `@.id` 와 같은 값(예약내역.har#56 ↔ #6 4/4) · 예약내역.har#56 |
| 4 | `data[].startDateTimeUtc` | string(ISO UTC) |  | 확인 안 됨 | 같은 일정의 예약 시작 · 점유 · 접수 · 생성 · 작업 시각 어느 것과도 같지 않다(예약내역.har#56 ↔ #6 4건 · 늘 30분 · 같은 날) — 뜻 확인 안 됨 · 예약내역.har#56 |
| 5 | `data[].tasks[]` | array / array(empty) / object | visit_task (models/task.py:68) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:545-552 · 예약내역.har#56 |
| 6 | `data[].tasks[].anesthesiaType` | enum:ANESTHESIA_TYPE_UNSPECIFIED | visit_task.anesthesia_type (models/task.py:102) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:472 · 예약내역.har#56 |
| 7 | `data[].tasks[].assigneeMemo` | string(empty) | visit_task.assignee_note (models/task.py:104) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:474 · 예약내역.har#56 |
| 8 | `data[].tasks[].assignees[]` | array / array(empty) / object | visit_task_staff (models/task.py:140) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:482-484 · 예약내역.har#56 |
| 9 | `data[].tasks[].assignees[].id` | string | visit_task_staff (models/task.py:140) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:482-484 · 예약내역.har#56 |
| 10 | `data[].tasks[].assignees[].name` | string | join staff.name | 계산으로 대체 | = P33 같은 키 · 예약내역.har#56 |
| 11 | `data[].tasks[].calledDoctors[]` | array(empty) | visit_task_staff (models/task.py:140) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:482-484 · 예약내역.har#56 |
| 12 | `data[].tasks[].completedDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.completed_at (models/task.py:114) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:481 · 예약내역.har#56 |
| 13 | `data[].tasks[].doctorAssignedDateTimeUtc` | string(ISO UTC) | visit_task.doctor_assigned_at (models/task.py:110) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:480 · 예약내역.har#56 |
| 14 | `data[].tasks[].doctorCallDateTime` | string(ISO UTC) / string(empty) | visit_task.doctor_called_at (models/task.py:109) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:479 · 예약내역.har#56 |
| 15 | `data[].tasks[].doctorMemo` | string(empty) | visit_task.doctor_note (models/task.py:105) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:475 · 예약내역.har#56 |
| 16 | `data[].tasks[].doctors[]` | array / array(empty) / object | visit_task_staff (models/task.py:140) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:482-484 · 예약내역.har#56 |
| 17 | `data[].tasks[].doctors[].id` | string | visit_task_staff (models/task.py:140) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:482-484 · 예약내역.har#56 |
| 18 | `data[].tasks[].doctors[].name` | string | join staff.name | 계산으로 대체 | = P33 같은 키 · 예약내역.har#56 |
| 19 | `data[].tasks[].etceteraConfiguration` | object |  | 해당 없음 | = P33 같은 키 · 묶음 · 예약내역.har#56 |
| 20 | `data[].tasks[].etceteraConfiguration.etceteraTaskId` | string / string(empty) | (etc_task_type 표는 있으나 작업 → 종류 FK 없음) | 칸 없음 | = P33 같은 키 · emr/kos/mapper.py:485-487 → `is_room_assign`(models/task.py:91) 판정에만 씀(emr/sync_tasks.py:132) · 예약내역.har#56 |
| 21 | `data[].tasks[].etceteraConfiguration.name` | string / string(empty) | visit_task.etc_task_title (models/task.py:88) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:469 · 예약내역.har#56 |
| 22 | `data[].tasks[].etceteraConfiguration.translsMap` | object / object(empty) |  | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 23 | `data[].tasks[].etceteraConfiguration.translsMap.name` | object |  | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 24 | `data[].tasks[].etceteraConfiguration.translsMap.name.translation` | object(empty) |  | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 25 | `data[].tasks[].memo` | string(empty) | visit_task.procedure_note (models/task.py:103) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:473 · 예약내역.har#56 |
| 26 | `data[].tasks[].order` | int | visit_task.sort_order (models/task.py:75) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:456 · 예약내역.har#56 |
| 27 | `data[].tasks[].paymentRequired` | bool | visit_task.payment_required (models/task.py:101) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:471 · 예약내역.har#56 |
| 28 | `data[].tasks[].procedureConfiguration` | object / object(empty) |  | 해당 없음 | = P33 같은 키 · 묶음 · 예약내역.har#56 |
| 29 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration` | object |  | 해당 없음 | = P33 같은 키 · 묶음 · 예약내역.har#56 |
| 30 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.caution` | string(empty) | (treatment_item.code · caution = 지금 메뉴 값 models/menu.py:173 · 176) | 칸 없음(시점 다름) | = P33 같은 키 · 메뉴 스냅샷 · 예약내역.har#56 |
| 31 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.code` | string | (treatment_item.code · caution = 지금 메뉴 값 models/menu.py:173 · 176) | 칸 없음(시점 다름) | = P33 같은 키 · 메뉴 스냅샷 · 예약내역.har#56 |
| 32 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.id` | string | visit_task.treatment_item_id (models/task.py:98) | 저장됨 | = P33 같은 키 · emr/kos/mapper_purchase.py:88 · 예약내역.har#56 |
| 33 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.machines[]` | array(empty) | visit_task.machines (models/task.py:96) | 저장됨 | = P33 같은 키 · emr/kos/mapper_purchase.py:89 — 이름 스냅샷 · 예약내역.har#56 |
| 34 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[]` | array / object | visit_task.medicines (models/task.py:94) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:449 · 470 — 이름 스냅샷 · 예약내역.har#56 |
| 35 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].id` | string | (이름 스냅샷만 — id 없음) | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 36 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].name` | string | visit_task.medicines (models/task.py:94) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:449 · 470 — 이름 스냅샷 · 예약내역.har#56 |
| 37 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].searchPhoneticName` | string | (machine · medicine.search_phonetic_name = 지금 값) | 칸 없음(시점 다름) | = P33 같은 키 · 예약내역.har#56 |
| 38 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.title` | string | visit_task.medical_service_title (models/task.py:80) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:462 · 예약내역.har#56 |
| 39 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap` | object |  | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 40 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title` | object |  | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 41 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation` | object / object(empty) |  | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 42 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.en` | string |  | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 43 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.ja` | string |  | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 44 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.ko` | string |  | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 45 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.zh-Hans` | string |  | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 46 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.zh-Hant` | string |  | 칸 없음 | = P33 같은 키 · 예약내역.har#56 |
| 47 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.unit` | object | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | = P33 같은 키 · 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) · 예약내역.har#56 |
| 48 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.unit.type` | enum:CC|UNIT | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | = P33 같은 키 · 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) · 예약내역.har#56 |
| 49 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.unit.value` | number | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | = P33 같은 키 · 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) · 예약내역.har#56 |
| 50 | `data[].tasks[].procedureConfiguration.productOptionConfiguration` | object |  | 해당 없음 | = P33 같은 키 · 묶음 · 예약내역.har#56 |
| 51 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.medicineAndMachines[]` | array(empty) |  | 확인 안 됨 | = P33 같은 키 · HAR 에서 늘 빈 배열 · 예약내역.har#56 |
| 52 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.optionId` | string |  | 일부러 안 둠 | = P33 같은 키 · S0:892 「상품 옵션 id 는 ERD v1 이 작업에 두지 않음」 · 예약내역.har#56 |
| 53 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.optionTitle` | string | visit_task.option_title (models/task.py:79) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:461 · 예약내역.har#56 |
| 54 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.procedure` | object | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | = P33 같은 키 · 메뉴 스냅샷 · 예약내역.har#56 |
| 55 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | = P33 같은 키 · S0:1429 「시술 카테고리 칸으로 두지 않는다」 · 예약내역.har#56 |
| 56 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.createDate` | string(empty) | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | = P33 같은 키 · 메뉴 스냅샷 · 예약내역.har#56 |
| 57 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.id` | string | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | = P33 같은 키 · 메뉴 스냅샷 · 예약내역.har#56 |
| 58 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.name` | string | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | = P33 같은 키 · 메뉴 스냅샷 · 예약내역.har#56 |
| 59 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.productTitle` | string / string(empty) | (product.title 은 지금 메뉴 값 · 작업 → 옵션 참조 없음) | 칸 없음(시점 다름) | = P33 같은 키 · data_rules 「메뉴 참조 = id + 그때 값 스냅샷」 · 예약내역.har#56 |
| 60 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap` | object |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 61 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle` | object |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 62 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation` | object / object(empty) |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 63 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.en` | string |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 64 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.ja` | string |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 65 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.ko` | string |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 66 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.zh-Hans` | string |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 67 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.zh-Hant` | string |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 68 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle` | object |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 69 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation` | object / object(empty) |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 70 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.en` | string |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 71 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.ja` | string |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 72 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.ko` | string |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 73 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.zh-Hans` | string |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 74 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.zh-Hant` | string |  | 칸 없음 | = P33 같은 키 · 옵션 · 상품 이름 번역 스냅샷 · 예약내역.har#56 |
| 75 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.unit` | object |  | 해당 없음 | = P33 같은 키 · 묶음 · 예약내역.har#56 |
| 76 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.unit.type` | enum:CC|UNIT|UnitType_UNKNOWN | visit_task.unit_type · unit_value (models/task.py:82 · 85) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:447-466 — `UnitType_UNKNOWN` 은 None · 예약내역.har#56 |
| 77 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.unit.value` | number | visit_task.unit_type · unit_value (models/task.py:82 · 85) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:447-466 — `UnitType_UNKNOWN` 은 None · 예약내역.har#56 |
| 78 | `data[].tasks[].procedureConfiguration.ticketConfiguration` | object / object(empty) |  | 해당 없음 | = P33 같은 키 · 묶음(시술권이 아니면 빈 객체) · 예약내역.har#56 |
| 79 | `data[].tasks[].procedureConfiguration.ticketConfiguration.round` | object |  | 해당 없음 | = P33 같은 키 · 묶음 · 예약내역.har#56 |
| 80 | `data[].tasks[].procedureConfiguration.ticketConfiguration.round.current` | int | visit_task.ticket_round_current (models/task.py:86) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:467 · 예약내역.har#56 |
| 81 | `data[].tasks[].procedureConfiguration.ticketConfiguration.round.total` | int | visit_task.ticket_round_total (models/task.py:87) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:468 · 예약내역.har#56 |
| 82 | `data[].tasks[].procedureConfiguration.ticketConfiguration.ticketId` | string(uuid) | visit_task.ticket_id (models/task.py:99) | 저장됨 | = P33 같은 키 · emr/kos/mapper_purchase.py:85-87 · 예약내역.har#56 |
| 83 | `data[].tasks[].readyDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.ready_at (models/task.py:108) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:478 · 예약내역.har#56 |
| 84 | `data[].tasks[].room` | object | visit_task.room_id (models/task.py:106) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:450-452 · 카드 방 visit.room_id(models/visit.py:93) emr/kos/mapper.py:388-408 · 예약내역.har#56 |
| 85 | `data[].tasks[].room.id` | string / string(empty) | visit_task.room_id (models/task.py:106) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:450-452 · 카드 방 visit.room_id(models/visit.py:93) emr/kos/mapper.py:388-408 · 예약내역.har#56 |
| 86 | `data[].tasks[].room.order` | int | join room (models/room.py:43-49) | 계산으로 대체 | = P33 같은 키 · 예약내역.har#56 |
| 87 | `data[].tasks[].room.title` | string / string(empty) | join room (models/room.py:43-49) | 계산으로 대체 | = P33 같은 키 · 예약내역.har#56 |
| 88 | `data[].tasks[].room.zoneId` | string / string(empty) | join room (models/room.py:43-49) | 계산으로 대체 | = P33 같은 키 · 예약내역.har#56 |
| 89 | `data[].tasks[].roomAssignedDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.room_assigned_at (models/task.py:107) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:477 · 예약내역.har#56 |
| 90 | `data[].tasks[].sequence` | int | visit_task.sequence (models/task.py:74) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:454 · 예약내역.har#56 |
| 91 | `data[].tasks[].status` | enum:CANCELED|DONE|NOT_STARTED|READY | visit_task.status (models/task.py:76) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:457-459 · 예약내역.har#56 |
| 92 | `data[].tasks[].title` | string | visit_task.title (models/task.py:78) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:460 · 예약내역.har#56 |
| 93 | `data[].tasks[].translsMap` | object |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 94 | `data[].tasks[].translsMap.title` | object |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 95 | `data[].tasks[].translsMap.title.translation` | object / object(empty) |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 96 | `data[].tasks[].translsMap.title.translation.de` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 97 | `data[].tasks[].translsMap.title.translation.en` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 98 | `data[].tasks[].translsMap.title.translation.es` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 99 | `data[].tasks[].translsMap.title.translation.fr` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 100 | `data[].tasks[].translsMap.title.translation.id` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 101 | `data[].tasks[].translsMap.title.translation.ja` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 102 | `data[].tasks[].translsMap.title.translation.ko` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 103 | `data[].tasks[].translsMap.title.translation.mn` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 104 | `data[].tasks[].translsMap.title.translation.ms` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 105 | `data[].tasks[].translsMap.title.translation.nl` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 106 | `data[].tasks[].translsMap.title.translation.pt` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 107 | `data[].tasks[].translsMap.title.translation.ru` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 108 | `data[].tasks[].translsMap.title.translation.th` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 109 | `data[].tasks[].translsMap.title.translation.uz` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 110 | `data[].tasks[].translsMap.title.translation.vi` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 111 | `data[].tasks[].translsMap.title.translation.zh-Hans` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 112 | `data[].tasks[].translsMap.title.translation.zh-Hant` | string |  | 칸 없음 | = P33 같은 키 · 작업 이름 번역 · 예약내역.har#56 |
| 113 | `data[].tasks[].type` | enum:ETCETERA|PROCEDURE | visit_task.kind (models/task.py:73) | 저장됨 | = P33 같은 키 · emr/kos/mapper.py:455 · 예약내역.har#56 |
| 114 | `data[].tasks[].urgencyLevel` | enum:URGENCY_LEVEL_UNSPECIFIED |  | 칸 없음 | = P33 같은 키 · 긴급도 · 예약내역.har#56 |

## N6. 수납 화면 경로

### N6-0. 무엇이 있나

- **읽기**: `get-payment-settings`(K1-2 #24 · 64키) · `get-visitor-prepaid-card-balance`(#25 · 17) · `get-currency-settings`(#16 · 2) · `get-vat-settings`(#22 · 3) · `get-tax-refund-receipts`(#26 · 1) — 87키 표 아래. 그 밖 수납 화면이 함께 부른 읽기 = P15 `get-purchase-summaries`(새 키 0) · P13 · P17 · `search-product-option-summaries`(K1-2 #18 · 172키 · 2차 HAR 합집합과 같음 · 새 키 0 — **표는 만들지 않았다**: 메뉴 검색 응답이라 P10 옵션 대조와 겹침, 정할 것 N8-5).
- **`initialize-purchase` 는 쓰기(commands) 경로다** — 읽기가 아니라 대조 안 함. 같은 화면 쓰기 9경로: `initialize-purchase` · `add-pending-purchase-items` · `register-purchase`(schedule) · `add-transaction` · `accept-purchase` · `start-purchase-refund` · `mark-purchase-items-for-refund` · `complete-purchase-refund` · `add-canceled-transaction`(N1 쓰기 표 · 전부 시술결제환불.har · 응답 200).
- 3차 거래(P15 `transactions[]`)의 `paymentType` = `CASH` · `PREPAID_CARD` 만 · `cardConfiguration` 빈 객체 — 데모 결제 불가(사용자)라 **카드 · 플랫폼 · 간편결제 거래 문자열은 이번에도 없다.**

### N6-2. 결제 수단 · 결제 단말 설정의 모양(`get-payment-settings` · 상담기록.har#2 등 6응답)

| 결제 수단 키(`data.paymentTypeConfiguration.…`) | `enabled` | `order` | `method.manualConfiguration` | `method.terminalConfiguration` | 회사 목록(건수만) |
|---|---|---|---|---|---|
| `cardConfiguration` | true | 0 | enabled true · `cardCompanies[]{name, order}` | enabled true(목록 없음) | 카드사 30 |
| `cashConfiguration` | true | 1 | enabled true | — | — |
| `transferConfiguration` | true | 2 | enabled true | — | — |
| `platformConfiguration` | true | 3 | enabled true · `platformCompanies[]{name, order}` | — | 6 |
| `easyPayConfiguration` | true | 4 | enabled true · `easyPayCompanies[]{name, order}` | enabled true · `easyPayCompanies[]{name, order}` | 10 · 10 |
| `prepaidCardConfiguration` | true | 5 | (`method` 없음) | — | — |
| `medicalLoanConfiguration` | **false** | 6 | enabled false · `medicalLoanCompanies[]`(빈 배열) | enabled false | 0 |

- 그 밖 최상위: `data.paymentTerminalIntegration.vendor`(string — 결제 단말 연동 업체 이름 · 값 안 적음) · `data.cashReceiptConfiguration.enabled`(bool — 현금영수증).
- 화면(`reference/2026-11-20-day-cc-mig/2026-11-20-kos-payment-screen.png(기본 체크아웃 · 개인정보 · 커밋 안 함)`) 6개 = 카드 · 현금 · 계좌이체 · 앱 결제 · 간편결제 · 선불카드. 설정의 켜진 6종을 `order` 로 놓으면 같은 자리에 카드 · 현금 · 계좌이체 · **플랫폼** · 간편결제 · 선불카드 — 「앱 결제」 = `platformConfiguration` 으로 **보이나 화면 라벨 ↔ 키의 직접 근거는 없다**(확인 안 됨). 「결제 단말기로 결제하기 / 직접 입력」 = `method.terminalConfiguration` / `method.manualConfiguration` 으로 보인다(같은 이유로 확인 안 됨).
- DAY 쪽: 결제 수단 매핑은 `CASH` · `PREPAID_CARD` · `TRANSFER` 셋(`emr/kos/mapper_sale_values.py:47-52` · 2차 K5-3 #1) — 설정의 7종 키 이름(`card` · `platform` · `easyPay` · `medicalLoan`)은 **거래 `paymentType` 문자열이 아니다**(문자열 표본은 2차 `CARD` 하나 · 3차 0).

### N6-3. 키 전수 대조 — 87키

#### K1-2 #24 `purchase/payment-settings/v1/queries/get-payment-settings`

스크립트 키 **64** · 표 행 **64** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 2 | `data.cashReceiptConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 3 | `data.cashReceiptConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 4 | `data.paymentTerminalIntegration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 5 | `data.paymentTerminalIntegration.vendor` | string |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 6 | `data.paymentTypeConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 7 | `data.paymentTypeConfiguration.cardConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 8 | `data.paymentTypeConfiguration.cardConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 9 | `data.paymentTypeConfiguration.cardConfiguration.method` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 10 | `data.paymentTypeConfiguration.cardConfiguration.method.manualConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 11 | `data.paymentTypeConfiguration.cardConfiguration.method.manualConfiguration.cardCompanies[]` | array / object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 12 | `data.paymentTypeConfiguration.cardConfiguration.method.manualConfiguration.cardCompanies[].name` | string |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 13 | `data.paymentTypeConfiguration.cardConfiguration.method.manualConfiguration.cardCompanies[].order` | int |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 14 | `data.paymentTypeConfiguration.cardConfiguration.method.manualConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 15 | `data.paymentTypeConfiguration.cardConfiguration.method.terminalConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 16 | `data.paymentTypeConfiguration.cardConfiguration.method.terminalConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 17 | `data.paymentTypeConfiguration.cardConfiguration.order` | int |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 18 | `data.paymentTypeConfiguration.cashConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 19 | `data.paymentTypeConfiguration.cashConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 20 | `data.paymentTypeConfiguration.cashConfiguration.method` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 21 | `data.paymentTypeConfiguration.cashConfiguration.method.manualConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 22 | `data.paymentTypeConfiguration.cashConfiguration.method.manualConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 23 | `data.paymentTypeConfiguration.cashConfiguration.order` | int |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 24 | `data.paymentTypeConfiguration.easyPayConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 25 | `data.paymentTypeConfiguration.easyPayConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 26 | `data.paymentTypeConfiguration.easyPayConfiguration.method` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 27 | `data.paymentTypeConfiguration.easyPayConfiguration.method.manualConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 28 | `data.paymentTypeConfiguration.easyPayConfiguration.method.manualConfiguration.easyPayCompanies[]` | array / object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 29 | `data.paymentTypeConfiguration.easyPayConfiguration.method.manualConfiguration.easyPayCompanies[].name` | string |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 30 | `data.paymentTypeConfiguration.easyPayConfiguration.method.manualConfiguration.easyPayCompanies[].order` | int |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 31 | `data.paymentTypeConfiguration.easyPayConfiguration.method.manualConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 32 | `data.paymentTypeConfiguration.easyPayConfiguration.method.terminalConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 33 | `data.paymentTypeConfiguration.easyPayConfiguration.method.terminalConfiguration.easyPayCompanies[]` | array / object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 34 | `data.paymentTypeConfiguration.easyPayConfiguration.method.terminalConfiguration.easyPayCompanies[].name` | string |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 35 | `data.paymentTypeConfiguration.easyPayConfiguration.method.terminalConfiguration.easyPayCompanies[].order` | int |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 36 | `data.paymentTypeConfiguration.easyPayConfiguration.method.terminalConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 37 | `data.paymentTypeConfiguration.easyPayConfiguration.order` | int |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 38 | `data.paymentTypeConfiguration.medicalLoanConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 39 | `data.paymentTypeConfiguration.medicalLoanConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 40 | `data.paymentTypeConfiguration.medicalLoanConfiguration.method` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 41 | `data.paymentTypeConfiguration.medicalLoanConfiguration.method.manualConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 42 | `data.paymentTypeConfiguration.medicalLoanConfiguration.method.manualConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 43 | `data.paymentTypeConfiguration.medicalLoanConfiguration.method.manualConfiguration.medicalLoanCompanies[]` | array(empty) |  | 확인 안 됨 | 빈 값만 관찰 · 상담기록.har#2 |
| 44 | `data.paymentTypeConfiguration.medicalLoanConfiguration.method.terminalConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 45 | `data.paymentTypeConfiguration.medicalLoanConfiguration.method.terminalConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 46 | `data.paymentTypeConfiguration.medicalLoanConfiguration.order` | int |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 47 | `data.paymentTypeConfiguration.platformConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 48 | `data.paymentTypeConfiguration.platformConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 49 | `data.paymentTypeConfiguration.platformConfiguration.method` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 50 | `data.paymentTypeConfiguration.platformConfiguration.method.manualConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 51 | `data.paymentTypeConfiguration.platformConfiguration.method.manualConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 52 | `data.paymentTypeConfiguration.platformConfiguration.method.manualConfiguration.platformCompanies[]` | array / object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 53 | `data.paymentTypeConfiguration.platformConfiguration.method.manualConfiguration.platformCompanies[].name` | string |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 54 | `data.paymentTypeConfiguration.platformConfiguration.method.manualConfiguration.platformCompanies[].order` | int |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 55 | `data.paymentTypeConfiguration.platformConfiguration.order` | int |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 56 | `data.paymentTypeConfiguration.prepaidCardConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 57 | `data.paymentTypeConfiguration.prepaidCardConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 58 | `data.paymentTypeConfiguration.prepaidCardConfiguration.order` | int |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 59 | `data.paymentTypeConfiguration.transferConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 60 | `data.paymentTypeConfiguration.transferConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 61 | `data.paymentTypeConfiguration.transferConfiguration.method` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 62 | `data.paymentTypeConfiguration.transferConfiguration.method.manualConfiguration` | object |  | 해당 없음 | 묶음 · 상담기록.har#2 |
| 63 | `data.paymentTypeConfiguration.transferConfiguration.method.manualConfiguration.enabled` | bool |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |
| 64 | `data.paymentTypeConfiguration.transferConfiguration.order` | int |  | 칸 없음 | 병원 결제 설정 — DAY 칸 · S0 언급 없음 · 상담기록.har#2 |

#### K1-2 #25 `purchase/prepaid-card/v1/queries/get-visitor-prepaid-card-balance`

스크립트 키 **17** · 표 행 **17** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data` | object |  | 해당 없음 | 묶음 · 예약내역.har#40 |
| 2 | `data.lastBalanceChargedDateTimeUtc` | string(ISO UTC) | prepaid_card_ledger.occurred_at 최댓값 (models/prepaid_card.py:72) | 계산으로 대체 | 충전 이력에서 — kind 구분은 ledger.kind · 예약내역.har#40 |
| 3 | `data.lastPointChargedDateTimeUtc` | string(ISO UTC) | prepaid_card_ledger.occurred_at 최댓값 (models/prepaid_card.py:72) | 계산으로 대체 | 충전 이력에서 — kind 구분은 ledger.kind · 예약내역.har#40 |
| 4 | `data.remainingBalance` | object |  | 해당 없음 | 묶음 · 예약내역.har#40 |
| 5 | `data.remainingBalance.balance` | object |  | 해당 없음 | 묶음 · 예약내역.har#40 |
| 6 | `data.remainingBalance.balance.currency` | enum:KRW | (prepaid_card 에 통화 칸 없음) | 칸 없음 | K6-16 · 예약내역.har#40 |
| 7 | `data.remainingBalance.balance.value` | int | Σ prepaid_card.balance_amount (models/prepaid_card.py:38) | 계산으로 대체 | 고객별 합 — 공유 카드 포함 여부 확인 안 됨 · 예약내역.har#40 |
| 8 | `data.remainingBalance.total` | object |  | 해당 없음 | 묶음 · 예약내역.har#40 |
| 9 | `data.remainingBalance.total.currency` | enum:KRW |  | 일부러 안 둠 | S0:1698 「총액 칸 없음 — remainingBalance.total · remainingPoint.total 받지 않는다」(카드 단위 결정 · 같은 키) · 예약내역.har#40 |
| 10 | `data.remainingBalance.total.value` | int |  | 일부러 안 둠 | S0:1698 「총액 칸 없음 — remainingBalance.total · remainingPoint.total 받지 않는다」(카드 단위 결정 · 같은 키) · 예약내역.har#40 |
| 11 | `data.remainingPoint` | object |  | 해당 없음 | 묶음 · 예약내역.har#40 |
| 12 | `data.remainingPoint.balance` | object |  | 해당 없음 | 묶음 · 예약내역.har#40 |
| 13 | `data.remainingPoint.balance.currency` | enum:KRW | (prepaid_card 에 통화 칸 없음) | 칸 없음 | K6-16 · 예약내역.har#40 |
| 14 | `data.remainingPoint.balance.value` | int | Σ prepaid_card.point_balance (models/prepaid_card.py:39) | 계산으로 대체 | 고객별 합 — 공유 카드 포함 여부 확인 안 됨 · 예약내역.har#40 |
| 15 | `data.remainingPoint.total` | object |  | 해당 없음 | 묶음 · 예약내역.har#40 |
| 16 | `data.remainingPoint.total.currency` | enum:KRW |  | 일부러 안 둠 | S0:1698 「총액 칸 없음 — remainingBalance.total · remainingPoint.total 받지 않는다」(카드 단위 결정 · 같은 키) · 예약내역.har#40 |
| 17 | `data.remainingPoint.total.value` | int |  | 일부러 안 둠 | S0:1698 「총액 칸 없음 — remainingBalance.total · remainingPoint.total 받지 않는다」(카드 단위 결정 · 같은 키) · 예약내역.har#40 |

#### K1-2 #16 `procedure-menu/currency-settings/queries/get-currency-settings`

스크립트 키 **2** · 표 행 **2** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data` | object |  | 해당 없음 | 묶음 · 시술기기약품.har#12 |
| 2 | `data.currency` | enum:KRW |  | 일부러 안 둠 | S0:1505 「타겟 국가 · 통화 · 부가세 설정 — 두지 않음(지금)」 · 사용자 11-20 「통화는 KOS 와 같게」와 닿음(K6-16) · 시술기기약품.har#12 |

#### K1-2 #22 `procedure-menu/vat-settings/queries/get-vat-settings`

스크립트 키 **3** · 표 행 **3** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data` | object |  | 해당 없음 | 묶음 · 시술기기약품.har#10 |
| 2 | `data.includeVATInPrice` | bool |  | 일부러 안 둠 | S0:1505 「타겟 국가 · 통화 · 부가세 설정 — 두지 않음(지금)」 · 사용자 11-20 「통화는 KOS 와 같게」와 닿음(K6-16) · 시술기기약품.har#10 |
| 3 | `data.vatRate` | number |  | 일부러 안 둠 | S0:1505 「타겟 국가 · 통화 · 부가세 설정 — 두지 않음(지금)」 · 사용자 11-20 「통화는 KOS 와 같게」와 닿음(K6-16) · 시술기기약품.har#10 |

#### K1-2 #26 `purchase/tax-refund-receipts/v1/queries/get-tax-refund-receipts`

스크립트 키 **1** · 표 행 **1** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |
|---|---|---|---|---|---|
| 1 | `data[]` | array(empty) |  | 확인 안 됨 | 3차 응답 1개 빈 배열 · 시술결제환불.har#156 |

### N6-1(추가 지시). KOS 웹 화면 URL 모양 · 딥링크

센 방법: 3차 HAR 7개의 `log.pages[]` 와 요청 헤더 `Referer`(쿼리 · 커맨드 요청 376건) · 2차 HAR 67개의 `log.pages[]`. 경로의 id 는 `{uuid}` · `{24자 hex}` · `{tenantId}` 로 바꾸고 쿼리는 **키 이름만** 남겼다(부록 A `collect3.py urlshape` · `pages.py`).

| 원천 | 본 것 |
|---|---|
| 3차 HAR `pages[]` | **0**(7파일 모두 빈 배열 — 화면 이동 기록 없음) |
| 3차 `Referer` | 7파일 376건 모두 **`https://app.kos-solution.com/`**(origin 만 · 경로 없음 — 브라우저가 경로를 빼고 보낸다) |
| 2차 `Referer` | 같음(origin 만) |
| 2차 `pages[]` 11개 중 KOS 앱 10 | 아래 4가지 |

| URL 모양 | 2차 HAR | 쿼리 키 · id 모양 | id 가 무엇인가(같은 HAR 응답과 값 비교 — 값은 안 적음) | DAY 에 있나 |
|---|---|---|---|---|
| `https://app.kos-solution.com/{tenantId}/reservation/schedule/?scheduleId=…&tab=…&visitorId=…` | 2026-10-23/…/수납필요 확인.har | `scheduleId` uuid · `tab` = `consultation`(이 값 하나만 관찰) · `visitorId` 24자 hex | `scheduleId` = P08 `data.id` · P33 `data[].id` · `get-schedule-summaries.data[].id` 와 같은 값 → **일정 id**. `visitorId` = P24 `data.id` · P33 `data[].visitor.id` · P15 `data[].visitorId` 등과 같은 값 → **고객 id** | 일정 id → `external_ref.external_id`(일정 · `emr/kos/mapper.py:555`) · 고객 id → `external_ref.external_id`(고객 · `emr/kos/mapper.py:307`) — 2차 판정 `저장됨` |
| `https://app.kos-solution.com/{tenantId}/reservation/procedure?id=…` | 2026-10-12/…/시술완료.har · 의사호출_2.har | `id` uuid | 같은 HAR 의 읽기 응답 어디에도 같은 값이 없다 — **무슨 id 인지 확인 안 됨** | 확인 안 됨 |
| `https://app.kos-solution.com/{tenantId}/reservation/settings` | 예약그룹.har · 예약그룹 .har · 처방전상세.har | 없음 | — | — |
| `https://app.kos-solution.com/{tenantId}` | 병원정보.har · 상담대기2 · 3.har · 예약이력.har | 없음 | — | — |

- `{tenantId}` = 첫 경로 조각. 같은 HAR 의 API 경로 `tenants/{id}/` 와 같은 값(10개 중 9 — `처방전상세.har` 1개는 다름 · 이유 확인 안 됨). DAY: `crm_connection.config.tenant_id`(평문 · `models/hospital.py:26-27`) · 로그인 토큰 행 `external_session.external_tenant_id`(`models/staff.py:110`).
- **수납 화면 URL · 구매(purchase) id 가 든 URL 은 HAR 에 없다** — 확인 안 됨. 고객 · 예약 상세 URL 의 `tab` 에 수납 탭 값이 있는지도 확인 안 됨(관찰 `consultation` 하나).
- **새 창으로 바로 열 수 있는지**(KOS 로그인 세션 없는 브라우저 · 다른 창에서 그 URL 을 열면 그 화면이 뜨는지)는 HAR 로 알 수 없다 — 확인 안 됨. HAR 의 `pages[]` 는 「그 화면에 있었다」는 기록일 뿐이다.

## N7. 갱신 집계 — 2차 → 3차

### N7-1. 요약 표의 수

| 항목 | 2차 | 3차 | 바뀐 이유 |
|---|---|---|---|
| 경로 — DAY 부름 · 새로 필요 · HAR 에만 | 23 · 11 · 43 | 23 · 11 · **50** | 새 경로 7(N1) |
| P 경로 중 HAR 응답 있음 / 없음 | 28 / 6 | 28 / 6 | 3차가 메운 P 경로 0(N2-2) |
| 키 총수(P 경로) | 1,965 | **2,155** | N3 새 키 +190 |
| 저장됨 | 769 | **786** | +17(N3) |
| 칸 있음 · 미동기화 | 95 | **97** | +2(N3 — 희망 시술 `optionId` P08 · P33) |
| 칸 없음 | 431 | **450** | +19(N3) |
| 칸 없음(시점 다름) | 306 | 306 | — |
| 일부러 안 둠 | 54 | **196** | +142(N3 — 희망 시술 구성 스냅샷 `S0:510`) |
| 계산으로 대체 | 160 | **163** | +1(N3 P10 `visitorType.name`) +2(N2 `consultations[].visitor.isNew` P08 · P33 재판정) |
| 해당 없음 | 126 | **134** | +8(N3) |
| 확인 안 됨 | 24 | **17** | −6(사용 안 함) −2(isNew 메움) +1(N3 P02 `roomCategoryIds[]` 빈 배열) |
| 사용 안 함(사용자) | — | **6** | 타이머 · 리액션(P07 · P08 · P33 각 2) |
| 확인 안 됨 — HAR 없는 경로 | 6 | 6 | N2-2 |
| 확인 안 됨 — K5-2 | 11 | **8** | 메움 3(N2-3) |
| DB 확장 후보 | 832행 · 고유 618 | **853행 · 고유 632** | +21행(N3 B 2 · C 19) · 고유 +14(P08 · P33 같은 키 6 은 하나로, P33 `reservationTagIds[]` 는 P08 에 이미 있어 0) |

### N7-2. DB 확장 후보(2차 K3-2)에 새로 들어오는 행 — 테이블별

| DAY 테이블 | 2차 → 3차 | 새 행(경로 · 키) |
|---|---|---|
| `visit_requested_procedure` | +12행 · 고유 +6 | P08 · P33 `reservation.requestedProcedures[].optionConfiguration.optionId`(칸 있음·미동기화 · `S0:551` OQ-041-7 · 2차 K6-22) · `…optionConfiguration.translsMap` · `.optionTitle` · `.optionTitle.translation` · `.productTitle` · `.productTitle.translation`(칸 없음 · 번역 — 2차 K6-15) |
| `product_option_price` | +8행 · 고유 +8 | P10 `options[].price.additional[]` 의 `amount.currency` · `suppliedAmount.{value,currency}` · `vatAmount.{value,currency}` · `taxFreeAmount.{value,currency}` · `taxation` |
| `visit`(태그 — 새 표 필요) | +1행 · 고유 0 | P33 `data[].reservationTagIds[]`(P08 같은 키 2차에 이미 있음) |

### N7-3. 2차 범위 밖이던 경로를 3차에 새로 판정한 것(2차 수에 더하지 않음)

2차는 K1-2(HAR 에만 43)를 「대조 안 함」으로 두었다. 3차 N4 · N5 · N6 에서 그중 **14경로 + 새 경로 1(`summarized-by-task`) = 15경로 · 376키**를 판정했다(그룹 단건 63 · 그룹 휴무 1 · 점유 시간 1 · 예약 정책 1 · 예약 규칙 27 · 규칙 목록 11 · 칸 점유 9 · 예약 칸 8 · 일정 목록 54 · 작업 요약 114 · 결제 설정 64 · 선불 잔액 17 · 통화 2 · 부가세 3 · 택스리펀드 1 — 표마다 「빠진 키 0」).

| 후보 표 | 행 | 판정별 | 경로 |
|---|---|---|---|
| visit_task | 60 | 칸 없음 49 · 칸 없음(시점 다름) 11 | get-schedules-summarized-by-task |
| 새 표 필요(병원 결제 설정) | 33 | 칸 없음 33 | get-payment-settings |
| 새 표 필요(예약 규칙) | 23 | 칸 없음 23 | get-reservation-rule · get-reservation-rule-summaries |
| (질의 결과 — 저장 대상인지 N8-4) | 10 | 칸 없음 10 | get-occupied-resources-by-reservation-time-slot · get-reservation-time-slots |
| reservation_group | 3 | 칸 없음 3 | get-reservation-group |
| prepaid_card | 2 | 칸 없음 2 | get-visitor-prepaid-card-balance |
| visit | 1 | 칸 없음 1 | get-schedule-list-items |
| visit (태그 — 새 표 필요) | 1 | 칸 없음 1 | get-schedule-list-items |
| **합** | **133** | | |


- 이 중 **같은 KOS 칸을 P 경로로 이미 센 것**(2차 후보와 겹침): `visit_task` 60(작업 요약 = P33 `tasks[]`) · `reservation_group` 3(그룹 단건 = P03) · 일정 목록 2(`reservationGroupId` · `reservationTagIds[]` = P33 · P08).
- **새로 생기는 후보 표**: 병원 결제 설정 33 · 예약 규칙 23 · 질의 결과(예약 칸 · 칸 점유) 10 · `prepaid_card` 통화 2.

## N8. 정할 것 (결정하지 않음)

| # | 질문 | 선택지 | 근거(사실) | 2차 |
|---|---|---|---|---|
| N8-1 | **미래 일정을 무엇으로 받을지** | ① P07 창을 미래로 넓힘 ② 예약 현황 화면처럼 P33 `baseDateUtc` 를 날짜마다 ③ `get-schedule-list-items` 의 수정 시각 창(바뀐 일정만) ④ 조합 | N4-1(화면은 ②) · N5-2(③은 고객 id 없이 `updatedDateTimeUtcFrom/To`) · 2차 R1 | K6-6 |
| N8-2 | **칸 정원 · 예약 수 원천** — 내부 경로에 칸별 예약 수가 없다 | ① S0:907 대로 P03 정원 + 미래 일정 점유로 계산(N8-1 이 필요) ② 공개 P28 을 그대로 부름(HAR 로 키 확인 불가 · cc 실호출 키 `capacity` · `reservationCount`) | N4-1 · 2차 R5 | K6-7 |
| N8-3 | 휴무(기본 · 그룹) · 점유 시간 · 예약 정책 · 병원 언어 — **3차에도 빈 값** | ① 데모에서 휴무 등을 실제로 넣고(쓰기 — 사용자) HAR 다시 ② 키 모른 채 받기만(jsonb 통째) ③ 범위 밖 | N2-1 #23 · #24 · N4-2 #28 · #30 · #31 · 병원설정.har 에 휴무 경로 없음(N1) | K6-18 |
| N8-4 | 예약 규칙(#32 · #33 · 27 + 11키) · 예약 칸(#35) · 칸 점유(#34) — 「KOS 키 다 저장」에 **질의 결과**까지 드는지 | ① 예약 규칙은 표로 · 칸 · 점유는 질의 때마다 KOS ② 셋 다 저장 ③ 셋 다 범위 밖 | N4-2 · 예약 칸 · 칸 점유는 요청 본문(시각 범위 · 규칙 · 희망 시술)에 따라 답이 바뀌는 응답 | — |
| N8-5 | 수납 화면 메뉴 검색 `search-product-option-summaries`(172키) 대조 여부 | ① 다음 판 대조 ② P10 대조로 충분 | N6-0 · 2차 합집합과 같은 키 | K6-17 |
| N8-6 | **병원 결제 설정**(결제 설정 64키 중 칸 없음 33) — 결제는 KOS 화면으로 연다(추가 지시 1)는데 저장할지 | ① 새 표(사용자 11-20 「다 저장」) ② 범위 밖(DAY 는 결제를 안 함) | N6-2 · N6-3 | — |
| N8-7 | **앱 결제 · 간편결제 거래 `paymentType` 문자열** | ① 이번엔 `CARD` 만(_RESUME 결정) · 나머지는 표본 생길 때 ② 운영(명동점) 표본으로 확인 — 사용자 허락 필요 | N6-2 · 데모 결제 불가 · 「앱 결제」 ↔ `platform` 은 순서 일치뿐(N6-2) | K6-4 |
| N8-8 | **수납 딥링크** — 수납 화면 URL 이 HAR 에 없다 | ① 사용자가 KOS 에서 수납 화면을 연 상태로 HAR 를 다시(페이지 이동이 `pages[]` 에 남게 — 주소창 URL 을 그대로 적어 줘도 됨) ② 고객 · 예약 상세 URL(`/reservation/schedule/?scheduleId&visitorId&tab`)로 열고 수납은 사람이 탭 이동 ③ 새 창 직접 열기 동작부터 사용자가 확인 | N6-1(추가) | — |
| N8-9 | **공개 P29 를 내부로 바꿀지** | ① 공개 P29 그대로(cc 방식) ② `summarized-by-task` + P33/P08 조합(상태 · 단계 · 삭제는 일정 경로에서) ③ DAY 사본(미래 · 과거 일정 동기화)에서 읽기 | N5-2 — `summarized-by-task` 에 `reservation.status` · `flowStep` · `deleted` 없음 | C 2(1차) |
| N8-10 | 문진(P30 · P31) · 일정 이력(P32)을 HAR 로 더 볼지 | ① 데모 고객 문진 제출 · 일정 이력 화면 HAR 다시 ② 공개 · 내부 경로를 cc 처럼 실시간 ③ 범위 밖 | N2-2 — legacy 400 NotFound 만 · P32 0 | K6-18 · C17(1차) |
| N8-11 | **희망 시술 진료항목 · 구성 스냅샷 142행**(`일부러 안 둠` — `S0:510`) 이 코디네이터 기본값 「일부러 안 둠에도 다 저장」(_RESUME §2) 범위에 드는지 | ① 든다(칸 · 표 추가) ② 54행만(2차 범위) | N3 · N7-1 | K6-9 · K6-1 |
| N8-12 | 사용자가 넣었다는 **희망 의사 · 시술권 희망 시술 · 상담 시술**이 응답에 비어 있다 | ① 사용자가 화면에서 실제로 저장됐는지 확인 뒤 HAR 다시 ② 그대로(확인 안 됨 유지) | N2-3 #3 · #5 · #6 | K6-18 |
| N8-13 | 고객 단건(P24)이 **빈 값이면 키를 뺀다**(3차 14키 없음) — 동기화가 「키 없음」을 「비움」으로 볼지 「모름(안 건드림)」으로 볼지 | ① 비움 ② 안 건드림 | N2-4 #2 | K6-2 |

정할 것 = **13**.

## 부록 A. 재현 — 스크립트 · 명령

스크립트는 scratchpad 에만(`/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-day-cc-mig/93a3b7e0-7e1d-430f-aa5c-5845cc5aa9aa/scratchpad/`) — 워크트리에 남긴 파일은 이 리포트 하나. 실행은 `python3 -I`. 2차 스크립트 8개(`keys.py` · `collect.py` · `classify.py` · `rules.py` · `gen.py` · `k13.py` · `verify.py` · `verify2.py`)는 **2차 리포트 부록 A 의 코드 블록을 그대로 뽑아** `old/` 에 두고 불렀다(`rules.py` 수정 0). 중간 산출 `new.pkl` · `old.pkl` 은 **키 경로 · 모양 · 엔트리 위치 · URL 모양(id 치환)만** 담았고 리포트를 쓴 뒤 지웠다.

```sh
H=/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/reference/2026-11-20-day-cc-mig/har
R=/Users/kknaks/git/toy_pr2/kknaks_profile/reference
ls $H | wc -l                                              # 7
python3 -I old/keys.py $H paths                            # 읽기 경로 58 · 엔트리 · 200 수
python3 -I k3/collect3.py $H k3/new.pkl                    # 3차: 57경로(200 JSON) · 2690키 · 쓰기 11
python3 -I k3/collect_old.py $R k3/old.pkl                 # 2차 HAR 다시: 70경로 · 3178키 · 쓰기 42(2차 K1 「71 중 70」과 같음)
python3 -I k3/diff.py <scratch>                            # 경로별 3차 키 · 2차 키 · 3차에만 있는 키
python3 -I k3/q.py <scratch> new '<키 정규식>' [경로]       # N2 재판정 조회(모양만)
python3 -I k3/gen3.py <scratch>                            # N3 · N4 · N5 · N6 표 · 집계(기본값으로 떨어진 키 0 — 걸리면 SystemExit)
python3 -I k3/n1.py <scratch>                              # N1 표 · 쓰기 표
python3 -I k3/verify3.py <리포트> $H $R                    # 부록 B
```

- N2 · N4 · N5 · N6-1 의 「같은 값」 대조는 일회용 인라인 스크립트로 **두 응답의 값을 메모리에서 비교해 참/거짓 · 건수만 출력**했다(값 출력 0) — 대조쌍: 예약내역.har#19 ↔ #6(일정 목록 ↔ P33 11행) · #56 ↔ #6(작업 요약 ↔ P33 4행) · P08 · P33 `consultations[].visitor.isNew` ↔ `visitor.isNew`(15) · 2차 `pages[]` 쿼리 id ↔ 같은 HAR 읽기 응답 값.
- 요청 본문(N4-1 · N5)은 키 이름 · 배열 길이 · 날짜의 캡처일 기준 상대 일수만 출력했다.

<details><summary><code>collect3.py</code>(3차 · <code>collect_old.py</code> 는 glob 을 재귀로 바꾼 같은 파일)</summary>

```python
# 일회용(3차): 새 HAR 7개 — 경로별 엔트리 · 키 합집합(모양만) · 키가 처음 보인 파일#엔트리 · 명령 목록 · 화면 URL 모양(경로만)
# 요청 헤더 중 Referer 하나만 읽고 경로 부분만 남긴다(값 id 는 {uuid}/{n} 로 치환 · 쿼리는 키 이름만). Authorization · Cookie 는 읽지 않는다.
import sys, runpy, pickle, collections, re, json, glob
from urllib.parse import urlsplit, parse_qsl
ROOT = sys.argv[1]; OUT = sys.argv[2]
sys.argv = ['k', ROOT, 'none']
K = runpy.run_path(sys.argv[0] if False else OUT.rsplit('/',2)[0] + '/old/keys.py')
UU = re.compile(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
def urlshape(u):
    s = urlsplit(u)
    p = UU.sub('{uuid}', s.path); p = re.sub(r'/\d+(?=/|$)', '/{n}', p)
    q = sorted({k for k, _ in parse_qsl(s.query, keep_blank_values=True)})
    return f'{s.scheme}://{s.netloc}{p}' + (('?' + '&'.join(k + '=…' for k in q)) if q else '')
keys = {}; first = {}; ent = collections.defaultdict(list); cmds = collections.defaultdict(list); refs = collections.Counter(); refpaths = collections.defaultdict(set)
for f in sorted(glob.glob(ROOT + '/*.har')):
    rel = f.rsplit('/',1)[1]
    h = json.load(open(f, encoding='utf-8'))
    for i, e in enumerate(h['log']['entries']):
        p = K['kospath'](e['request']['url'])
        ref = [x['value'] for x in e['request'].get('headers', []) if x['name'].lower() == 'referer']
        if ref and ('/queries/' in p or '/commands/' in p):
            rs = urlshape(ref[0]); refs[(rel, rs)] += 1; refpaths[rs].add(p)
        if '/commands/' in p:
            cmds[p].append((rel, i, e['response']['status'])); continue
        if '/queries/' not in p: continue
        b, st = K['body'](e)
        ent[p].append((rel, i, e['response']['status'], st))
        if st != 'ok' or e['response']['status'] != 200: continue
        acc = collections.defaultdict(set); K['walk'](b, '', acc)
        d = keys.setdefault(p, collections.defaultdict(set))
        for k, v in acc.items():
            d[k] |= v; first.setdefault((p, k), f'{rel}#{i}')
pages = []
for f in sorted(glob.glob(ROOT + '/*.har')):
    h = json.load(open(f, encoding='utf-8'))
    for pg in h['log'].get('pages', []):
        t = pg.get('title', '')
        pages.append((f.rsplit('/',1)[1], urlshape(t) if t.startswith('http') else '(제목이 URL 아님)'))
pickle.dump({'keys': {p: dict(v) for p, v in keys.items()}, 'first': first, 'entries': dict(ent), 'cmds': dict(cmds),
             'refs': dict(refs), 'refpaths': {k: sorted(v) for k, v in refpaths.items()}, 'pages': pages}, open(OUT, 'wb'))
print(len(keys), sum(len(v) for v in keys.values()), len(cmds))
```

</details>

<details><summary><code>cls3.py</code> · <code>q.py</code></summary>

```python
# 일회용(3차): 2차 rules.py 의 판정 규칙을 새 HAR 키에 그대로 적용(값 없음 · 키 경로만)
import pickle, re, runpy, sys
S = sys.argv[1]
D = pickle.load(open(S + '/k3/new.pkl', 'rb')); O = pickle.load(open(S + '/k3/old.pkl', 'rb'))
R = runpy.run_path(S + '/old/rules.py'); RULES = R['RULES']; V = R['V']
def rel(key, root):
    if key == root: return '@'
    if key.startswith(root + '.'): return '@' + key[len(root):]
    return key
def classify(path, k, shapes):
    root, rules = RULES[path]; rk = rel(k, root)
    for (p, v, c, n, t) in rules:
        if re.fullmatch(p, rk): return (v, c, n, t, p)
    plain = {s for s in shapes if not s.startswith('ENUM:')}
    if plain and plain <= {'object', 'array', 'object(map)'}: return ('F', '', '묶음', '', '*generic')
    if plain and plain <= {'array(empty)', 'object(empty)'}: return ('U', '', '빈 값만 관찰 — 안쪽 키 확인 안 됨', '', '*generic')
    return ('C', '', '', '', '*default')
def fmt(shapes):
    en = sorted(x[5:] for x in shapes if x.startswith('ENUM:')); o = sorted(x for x in shapes if not x.startswith('ENUM:'))
    if en: o.append('enum:' + '|'.join(en) if len(en) <= 15 else f'enum({len(en)}종)')
    return ' / '.join(o)
```

```python
# 일회용: 키 경로 정규식으로 새/옛 합집합의 모양 조회(값 없음)
import pickle, re, sys, runpy
S=sys.argv[1]; which=sys.argv[2]; rx=re.compile(sys.argv[3]); pth=sys.argv[4] if len(sys.argv)>4 else ''
sys.argv=['x',S]; C=runpy.run_path(S+'/k3/cls3.py')
D = C['D'] if which=='new' else C['O']
for p in sorted(D['keys']):
    if pth and pth not in p: continue
    for k in sorted(D['keys'][p]):
        if rx.search(k): print(p.split('queries/')[-1], '|', k, '|', C['fmt'](D['keys'][p][k]), '|', D['first'].get((p,k),''))
```

</details>

<details><summary><code>gen3.py</code></summary>

```python
# 일회용(3차): N3 · N4 · N5 · N6 키 표를 만든다. 값은 다루지 않는다(키 경로 · 모양 · 2차 판정 규칙).
import sys, runpy, re, collections, unicodedata, json
S = sys.argv[1]; sys.argv = ['x', S]
C = runpy.run_path(S + '/k3/cls3.py'); D = C['D']; O = C['O']; RULES = C['RULES']; V = C['V']; fmt = C['fmt']; classify = C['classify']
nfc = lambda s: unicodedata.normalize('NFC', s)
P33 = 'schedule/v2/queries/get-schedules-for-reservation'; P03 = 'schedule/group/v1/queries/get-reservation-groups'
def first(p, k): return nfc(D['first'].get((p, k), ''))
def row(i, k, sh, col, v, note): return f'| {i} | `{k}` | {sh} | {col} | {V[v]} | {note} |'
OUT = []; STATS = collections.OrderedDict(); CAND = []   # CAND: (표, 경로, 키, 판정)
def table(title, p, judge, extra_note=''):
    keys = sorted(D['keys'][p]); rows = []; cnt = collections.Counter()
    for i, k in enumerate(keys, 1):
        v, col, note, tbl = judge(k, D['keys'][p][k])
        cnt[v] += 1
        if v in ('B', 'C', 'C2'): CAND.append((tbl or '(표 미정)', p, k, v))
        rows.append(row(i, k, fmt(D['keys'][p][k]), col, v, (note + (' · ' if note else '') + first(p, k)).strip(' ·')))
    STATS[p] = (len(keys), len(rows), cnt)
    OUT.append(f'#### {title} `{p}`\n\n스크립트 키 **{len(keys)}** · 표 행 **{len(rows)}** · 빠진 키 **{len(keys) - len(rows)}**{extra_note}\n')
    OUT.append('| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |\n|---|---|---|---|---|---|')
    OUT.extend(rows); OUT.append('')
def by_rules(rp, mapk=lambda k: k, note_pre=''):
    def j(k, sh):
        v, col, note, tbl, pat = classify(rp, mapk(k), sh)
        if pat == '*default': raise SystemExit('default hit ' + rp + ' ' + k)
        n = (note_pre + (' · ' if note_pre and note else '') + note)
        return v, col, n, tbl
    return j
# ---------- N3 : P 경로의 새 키만 ----------
def newonly(p): return sorted(set(D['keys'][p]) - set(O['keys'].get(p, {})))
MV = 'models/menu.py:'; MM = 'emr/kos/mapper_menu.py:'
def p10(k, sh):
    a = re.sub(r'^data\[\]\.options\[\]\.price\.additional\[\]\.?', '', k)
    T = 'product_option_price'
    if a in ('amount', 'suppliedAmount', 'taxFreeAmount', 'vatAmount'): return 'F', '', '묶음', ''
    if a == 'amount.value': return 'A', f'product_option_price.amount ({MV}138)', MM + '89 · 2차 「늘 빈 배열」 → 3차 처음 관찰', ''
    if a == 'visitorType' or a == 'visitorType.id': return 'A', f'product_option_price.customer_type_id ({MV}135)', MM + '86-88', ''
    if a == 'visitorType.name': return 'E', 'join customer_type.name (models/customer.py:120)', '', ''
    if a.endswith('.currency'): return 'C', '(통화 칸 없음 — product_option_price 는 amount 만)', '사용자 11-20 「통화는 KOS 와 같게」(K6-16)', T
    return 'C', '(product_option_price 는 amount 만 · 옵션 본가격은 product_option.supplied_amount 등에 있음)', '수가 유형별 공급가 · 부가세 · 면세 · 과세', T
NEWKEYROWS = collections.OrderedDict()
for p, tag in [('schedule/zone/room/v1/queries/get-rooms', 'P02'), ('schedule/v1/queries/get-schedule-detail', 'P08'),
               ('procedure-menu/products/queries/get-products', 'P10'), (P33, 'P33')]:
    ks = newonly(p); rows = []; cnt = collections.Counter()
    for i, k in enumerate(ks, 1):
        if tag == 'P10': v, col, note, tbl = p10(k, D['keys'][p][k])
        else:
            v, col, note, tbl, pat = classify(p, k, D['keys'][p][k])
            if pat == '*default': raise SystemExit('default ' + k)
        cnt[v] += 1
        if v in ('B', 'C', 'C2'): CAND.append((tbl or '(표 미정)', p, k, v))
        rows.append(row(i, k, fmt(D['keys'][p][k]), col, v, (note + ' · ' + first(p, k)).strip(' ·')))
    NEWKEYROWS[(tag, p)] = (len(ks), rows, cnt)
N3 = []
for (tag, p), (n, rows, cnt) in NEWKEYROWS.items():
    N3.append(f'#### {tag} `{p}` — 새 키 **{n}** · 표 행 **{len(rows)}** · 빠진 키 **{n - len(rows)}**\n')
    N3.append('| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 · 처음 본 곳(3차 HAR#엔트리) |\n|---|---|---|---|---|---|')
    N3.extend(rows); N3.append('')
N3CNT = {tag: (n, cnt) for (tag, p), (n, rows, cnt) in NEWKEYROWS.items()}
n3cand = len(CAND)
# ---------- N4 ----------
OUT.append('<!--N4-->')
table('K1-2 #29', 'schedule/group/v1/queries/get-reservation-group', by_rules(P03, lambda k: re.sub(r'^data(?=\.|$)', 'data[]', k), 'P03 과 같은 그룹 객체(단건) — 판정은 P03 규칙 · 저장됨 = P03 경로로 이미 받음'),
      ' · 키 집합 = P03 과 같음(`data.` ↔ `data[].`)')
U1 = lambda note: (lambda k, sh: ('U', '', note, '') if k in ('data[]', 'data') else ('?', '', '', ''))
table('K1-2 #30', 'schedule/group/v1/queries/get-reservation-group-days-offs', U1('3차 응답 7개 모두 빈 배열(예약현황.har 미래 3일 범위 포함) — 안쪽 키 확인 안 됨'))
table('K1-2 #31', 'schedule/occupied-time/v2/queries/get-occupied-times', U1('3차 응답 7개 모두 빈 배열 — 안쪽 키 확인 안 됨'))
table('K1-2 #28', 'schedule/default-operation-time/v1/queries/get-default-reservation-policy', U1('3차 응답 2개 모두 빈 객체 — 안쪽 키 확인 안 됨'))
def rule_tbl(T, note):
    def j(k, sh):
        plain = {s for s in sh if not s.startswith('ENUM:')}
        if plain <= {'array(empty)', 'object(empty)'}: return 'U', '', '빈 값만 관찰 — 안쪽 키 확인 안 됨', ''
        if plain <= {'object', 'array'}: return 'F', '', '묶음', ''
        return 'C', '', note, T
    return j
table('K1-2 #32', 'schedule/reservation-rule/v1/queries/get-reservation-rule', rule_tbl('새 표 필요(예약 규칙)', '예약 규칙 — DAY 칸 · S0 언급 없음(`grep 예약 규칙` 0)'))
table('K1-2 #33', 'schedule/reservation-rule/v1/queries/get-reservation-rule-summaries', rule_tbl('새 표 필요(예약 규칙)', '예약 규칙 목록 — DAY 칸 없음'))
table('K1-2 #34', 'schedule/reservation-time-slot/v1/queries/get-occupied-resources-by-reservation-time-slot', rule_tbl('(질의 결과 — 저장 대상인지 N8-4)', '예약 쓰기 화면이 시각 범위 · 규칙을 보내 받는 점유 자원(요청 본문 키: dateTimeRangeUtc · reservationRuleId · requestedProcedureOptionIds …)'))
table('K1-2 #35', 'schedule/reservation-time-slot/v1/queries/get-reservation-time-slots', rule_tbl('(질의 결과 — 저장 대상인지 N8-4)', '예약 칸 가능 여부 — 정원 · 예약 수는 없다(bool 만)'))
# ---------- N5 ----------
OUT.append('<!--N5-->')
ALIAS = [(r'^data\[\]\.counselor', 'data[].reservation.counselor'), (r'^data\[\]\.reservationAssignee', 'data[].reservation.reservationAssignee'),
         (r'^data\[\]\.reservationGroupId$', 'data[].reservation.reservationGroupId'), (r'^data\[\]\.reservationMemo$', 'data[].reservation.reservationMemo'),
         (r'^data\[\]\.reservationStartDateTime$', 'data[].reservation.startDateTime'), (r'^data\[\]\.reservationStatus$', 'data[].reservation.status'),
         (r'^data\[\]\.funnel', 'data[].reservation.funnel'),
         (r'^data\[\]\.occupiedReservationGroups\[\]$', 'data[].occupiedResources[]'),
         (r'^data\[\]\.occupiedReservationGroups\[\]\.doctors\[\]', 'data[].occupiedResources[].reservationGroup.doctors[]'),
         (r'^data\[\]\.occupiedReservationGroups\[\]\.reservationGroupId$', 'data[].occupiedResources[].reservationGroup.reservationGroupId'),
         (r'^data\[\]\.occupiedReservationGroups\[\]\.(start|end)DateTimeUtc$', r'data[].occupiedResources[].reservationTime.\1DateTimeUtc')]
def li(k, sh):
    if k == 'totalCount': return 'F', '', 'count', ''
    if k == 'data[].requestedProcedureTitles[]':
        return 'E', 'visit_requested_procedure.option_title (models/visit.py:109)', '예약내역.har#19 ↔ #6 같은 일정 11건 대조 — `optionTitle` 목록과 11/11 같음(`productTitle` 과는 10/11)', ''
    mk = k
    for a, b in ALIAS:
        if re.search(a, k): mk = re.sub(a, b, k); break
    v, col, note, tbl, pat = classify(P33, mk, sh)
    if pat == '*default': raise SystemExit('li default ' + k)
    pre = ('= P33 `' + mk + '`') if mk != k else '= P33 같은 키'
    return v, col, pre + ' · ' + note if note else pre, tbl
table('K1-2 #38', 'schedule/v2/queries/get-schedule-list-items', li, ' · 요청 본문 키 = `tenantId` · `updatedDateTimeUtcFrom` · `updatedDateTimeUtcTo` · `limit`(고객 id 없음 — 예약내역.har#19)')
def st(k, sh):
    if k == 'data[].scheduleId': return 'A', 'external_ref.external_id (models/customer.py:106)', '일정 id — P07 · P33 의 `@.id` 와 같은 값(예약내역.har#56 ↔ #6 4/4)', ''
    if k in ('data[].startDateTimeUtc', 'data[].endDateTimeUtc'):
        return 'U', '', '같은 일정의 예약 시작 · 점유 · 접수 · 생성 · 작업 시각 어느 것과도 같지 않다(예약내역.har#56 ↔ #6 4건 · 늘 30분 · 같은 날) — 뜻 확인 안 됨', ''
    v, col, note, tbl, pat = classify(P33, k, sh)
    if pat == '*default': raise SystemExit('st default ' + k)
    return v, col, ('= P33 같은 키 · ' + note) if note else '= P33 같은 키', tbl
table('새 경로', 'schedule/v2/queries/get-schedules-summarized-by-task', st, ' · 요청 본문 키 = `visitorId`(예약내역.har#56) · 키 111 이 P33 합집합 안')
# ---------- N6 ----------
OUT.append('<!--N6-->')
def pay(k, sh):
    plain = {s for s in sh if not s.startswith('ENUM:')}
    if plain <= {'array(empty)', 'object(empty)'}: return 'U', '', '빈 값만 관찰', ''
    if plain <= {'object', 'array'}: return 'F', '', '묶음', ''
    return 'C', '', '병원 결제 설정 — DAY 칸 · S0 언급 없음', '새 표 필요(병원 결제 설정)'
table('K1-2 #24', 'purchase/payment-settings/v1/queries/get-payment-settings', pay)
def bal(k, sh):
    if k in ('data', 'data.remainingBalance', 'data.remainingPoint', 'data.remainingBalance.balance', 'data.remainingPoint.balance', 'data.remainingBalance.total', 'data.remainingPoint.total'):
        return 'F', '', '묶음', ''
    if k == 'data.remainingBalance.balance.value': return 'E', 'Σ prepaid_card.balance_amount (models/prepaid_card.py:38)', '고객별 합 — 공유 카드 포함 여부 확인 안 됨', ''
    if k == 'data.remainingPoint.balance.value': return 'E', 'Σ prepaid_card.point_balance (models/prepaid_card.py:39)', '고객별 합 — 공유 카드 포함 여부 확인 안 됨', ''
    if '.total.' in k: return 'D', '', 'S0:1698 「총액 칸 없음 — remainingBalance.total · remainingPoint.total 받지 않는다」(카드 단위 결정 · 같은 키)', ''
    if k.endswith('.currency'): return 'C', '(prepaid_card 에 통화 칸 없음)', 'K6-16', 'prepaid_card'
    return 'E', 'prepaid_card_ledger.occurred_at 최댓값 (models/prepaid_card.py:72)', '충전 이력에서 — kind 구분은 ledger.kind', ''
table('K1-2 #25', 'purchase/prepaid-card/v1/queries/get-visitor-prepaid-card-balance', bal)
D1505 = lambda k, sh: ('F', '', '묶음', '') if k == 'data' else ('D', '', 'S0:1505 「타겟 국가 · 통화 · 부가세 설정 — 두지 않음(지금)」 · 사용자 11-20 「통화는 KOS 와 같게」와 닿음(K6-16)', '')
table('K1-2 #16', 'procedure-menu/currency-settings/queries/get-currency-settings', D1505)
table('K1-2 #22', 'procedure-menu/vat-settings/queries/get-vat-settings', D1505)
table('K1-2 #26', 'purchase/tax-refund-receipts/v1/queries/get-tax-refund-receipts', U1('3차 응답 1개 빈 배열'))
for p, (n, r, c) in STATS.items():
    assert '?' not in c, p
open(S + '/k3/n3.md', 'w').write('\n'.join(N3)); open(S + '/k3/n456.md', 'w').write('\n'.join(OUT))
import pickle; pickle.dump({'STATS': STATS, 'N3CNT': N3CNT, 'CAND': CAND, 'n3cand': n3cand}, open(S + '/k3/stats.pkl', 'wb'))
for p, (n, r, c) in STATS.items(): print(n, r, dict(c), p)
for t, (n, c) in N3CNT.items(): print('N3', t, n, dict(c))
print('cand', len(CAND), collections.Counter(x[0] for x in CAND))
```

</details>

<details><summary><code>diff.py</code> · <code>n1.py</code></summary>

```python
import pickle, re, sys, collections
S = sys.argv[1]
N = pickle.load(open(S + '/k3/new.pkl', 'rb')); O = pickle.load(open(S + '/k3/old.pkl', 'rb'))
t = open('research-kos-keys-report.md', encoding='utf-8').read()
P = dict(re.findall(r'^\| (P\d\d) \| `([^`]+)`', t, re.M)); P = {v: k for k, v in P.items()}
K12 = {m[1]: m[0] for m in re.findall(r'^\| (\d+) \| `([^`]+)` \| \d+ \|', t[t.index('### K1-2'):t.index('## K2.')], re.M)}
pickle.dump((P, K12), open(S + '/k3/idx.pkl', 'wb'))
allp = sorted(set(N['entries']))
for p in allp:
    tag = P.get(p) or (('K1-2#' + K12[p]) if p in K12 else '새 경로')
    E = N['entries'][p]; ok = sum(1 for x in E if x[2] == 200 and x[3] == 'ok')
    nk = set(N['keys'].get(p, {})); ok_old = set(O['keys'].get(p, {}))
    files = collections.Counter(x[0] for x in E)
    sts = collections.Counter((x[2], x[3]) for x in E if not (x[2] == 200 and x[3] == 'ok'))
    print(f'{tag}\t{p}\t{len(E)}\t{ok}\tkeys={len(nk)}\told={len(ok_old)}\tnewkeys={len(nk-ok_old)}\t' + ' · '.join(f'{k}({v})' for k, v in sorted(files.items())) + ('\tNON200:' + str(dict(sts)) if sts else ''))
```

```python
# 일회용(3차): N1 경로 표(엔트리 수 · 메서드 · 200 JSON 수 · 파일별) — 값 없음
import pickle, sys, collections, unicodedata, re
S = sys.argv[1]
N = pickle.load(open(S + '/k3/new.pkl', 'rb')); O = pickle.load(open(S + '/k3/old.pkl', 'rb')); P, K12 = pickle.load(open(S + '/k3/idx.pkl', 'rb'))
nfc = lambda s: unicodedata.normalize('NFC', s)
rows = []
def order(p):
    if p in P: return (0, P[p])
    if p in K12: return (1, int(K12[p]))
    return (2, p)
tot = ok = 0
for p in sorted(N['entries'], key=order):
    E = N['entries'][p]; o = sum(1 for x in E if x[2] == 200 and x[3] == 'ok'); tot += len(E); ok += o
    tag = P.get(p) or (f'K1-2 #{K12[p]}' if p in K12 else '**새 경로**')
    files = collections.Counter(nfc(x[0]) for x in E if x[2] == 200 and x[3] == 'ok')
    other = collections.Counter(('OPTIONS·빈 본문' if x[3] == 'no-text' else f'{x[2]}') for x in E if not (x[2] == 200 and x[3] == 'ok'))
    nk = len(N['keys'].get(p, {})); ok2 = len(O['keys'].get(p, {}))
    newk = len(set(N['keys'].get(p, {})) - set(O['keys'].get(p, {})))
    rows.append(f"| {tag} | `{p}` | {len(E)} | {o} | {' · '.join(f'{k}({v})' for k, v in other.items())} | {' · '.join(f'{k}({v})' for k, v in sorted(files.items()))} | {nk} | {ok2} | {newk} |")
hdr = '| 갈래 | 경로 | 엔트리 | 200+JSON | 그 밖 | 200+JSON 파일(수) | 3차 키 | 2차 HAR 키 | 3차에만 있는 키 |\n|---|---|---|---|---|---|---|---|---|'
open(S + '/k3/n1.md', 'w').write(hdr + '\n' + '\n'.join(rows) + '\n')
c = collections.Counter('P' if p in P else ('K' if p in K12 else 'N') for p in N['entries'])
print(len(rows), tot, ok, dict(c))
cm = []
for p, L in sorted(N['cmds'].items()):
    fs = collections.Counter(nfc(f) for f, i, s in L)
    cm.append(f"| `{p}` | {len(L)} | {' · '.join(f'{k}({v})' for k, v in fs.items())} |")
open(S + '/k3/cmds.md', 'w').write('| 쓰기 경로(commands) | 엔트리 | 파일 |\n|---|---|---|\n' + '\n'.join(cm) + '\n')
print(len(cm))
```

</details>

## 부록 B. 검증

명령(부록 A 마지막 줄):

```sh
python3 -I k3/verify3.py <리포트> $H $R     # 3차 HAR 7 + 2차 HAR 67 의 응답 값과 대조 · 출력은 건수뿐
```

| 검사 | 결과 |
|---|---|
| 새 HAR 파일 수 | **7**(`ls $H \| wc -l`) |
| 키 표 수 · 「스크립트 키 = 표 행 = 실제 행」 | 표 **19**(N3 4 · N4 8 · N5 2 · N6 5) · 어긋남 **0** · 빠진 키 0 |
| 이메일 꼴 | **0** |
| 전화번호 꼴 | **0** |
| 7자리 이상 숫자 | 2 — 모두 cc 커밋 sha(HAR 값 아님) |
| uuid 꼴 · 24자 hex | uuid 1 — 부록 A 의 scratchpad 경로(세션 폴더 이름 · HAR 값 아님) · hex24 0 |
| HAR 의 id 값(uuid · 24자 hex · 테넌트 id 26,532종)이 리포트에 | **0** |
| HAR 의 사람 · 연락처 · 메모 · 이름 꼴 키 값(3,093종)이 리포트에 낱말로 | 38 — 전부 **짧은 숫자 · 기호**(리포트의 줄 번호 · 건수 · `**` 와 같은 글자인 차트번호 · 계정 꼴 값 1 ~ 3자리) · 한글 0 |
| HAR 의 한글 값(24,793종)이 리포트에 낱말로 | 7 — 보통 낱말(메뉴 · 문진 · 결과 칸의 짧은 값이 리포트 본문 낱말과 같음 · 키 `title` · `questionTitle` · `answerTitle` · `result`) · **이름 꼴 키(`name` · `visitorName` 등)에서 온 한글 0** |

- 처음 돌렸을 때 이름 꼴 키에서 온 한글 낱말 3개가 걸렸다 — 리포트 본문의 보통 낱말(사람 역할 · 동사 · 명사 각 1)이 데모 데이터의 이름 값과 우연히 같은 글자였다. 뜻이 같은 다른 말로 바꿔 다시 돌렸다(`assemble.py` 의 바꿈 3쌍 — 스크립트 원문은 scratchpad).
- 요청 헤더는 `Referer` 만 읽었고(N6-1) Authorization · Cookie 는 읽지 않았다. HAR 이동 · 복사 · 수정 0 · KOS · DAY 실호출 0 · 레포 수정 0(이 리포트 1개 생성).
