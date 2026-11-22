# 조사 리포트 — KOS 응답 키 ↔ DAY 칸 전수 대조 (HAR 기준)

- 작성: day `researcher` · 2026-11-20 · 조사만(판단 없음 — 판단은 K6 「정할 것」)
- 앞 판: `research-cc-ext-report.md`(cc ext 가 쓰는 칸만 대조) — 이번 판은 **KOS 가 주는 응답 키 전부**로 넓혔다.
- 읽은 ref(전부 read-only · `git fetch` · `git show` · `git grep` 만):
  - CENTURION_DAY `origin/dev` = **`844eace4`**(시작 때 `git fetch` 뒤에도 같음) — `backend/`
  - mediness-mediness `origin/main` = **`ccede286`** — `products/day/20-spec/spec-000-data-model.md`(아래 `S0:줄`)
  - cc-prototype `origin/main`(경로 상수만 — `procedure/back/app/service/{ext,reservations}.py` · `kos/reservation_sync.py`)
  - HAR: `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/` 아래 `*.har` **67개**(`find … -name "*.har" | wc -l` → 67 · 폴더별 8 · 1 · 23 · 7 · 1 · 5 · 22) — 파일 그대로 읽기만
  - 판단 기준: `orchestration/config/projects/day.json` `data_rules` · `orchestration/work/_archive/day/customer-erd/customer-erd-spec-brief.md` §2 · SPEC-000 결정 · OQ
- 근거 표기: 코드 = `backend/day/` 아래 경로:줄(위 sha) · 문서 = `S0:줄` 또는 파일:줄 · HAR = `폴더/…/파일#엔트리`(부록 B).
- **값 0**: HAR 의 값은 한 글자도 옮기지 않았다 — 키 경로 · 타입 · 모양만. enum 은 KOS 코드값만(부록 C 검증). 요청 헤더 · Authorization · Cookie 는 읽지 않았다. KOS · DAY 서버 실호출 0.
- 일회용 파싱 스크립트는 scratchpad 에만 두었다(부록 A) — 워크트리에 남긴 파일은 이 리포트 하나.

## 0. 요약

| 항목 | 값 |
|---|---|
| 경로 수 | **DAY 부름 23** · **ext 이관에 새로 필요 11** · **HAR 에만 있는 읽기 경로 43**(K1 · §K1-2) |
| HAR 응답 | 34경로 중 **28** 있음 · **6** 없음(DAY 부름 1 · 새로 필요 5 — K5-1) |
| 키 총수 | **1,965**(28경로 · 경로마다 스크립트 합집합 키 수 = K2 표 행 수 · 빠진 키 0 — K1 오른쪽 두 칸) |
| 판정별 | 저장됨 **769** · 칸 있음·미동기화 **95** · 칸 없음 **431**(그중 번역 `translsMap` 잎 246) · 칸 없음(시점 다름) **306**(그중 번역 40) · 일부러 안 둠 **54** · 계산으로 대체 **160** · 해당 없음 **126** · 확인 안 됨 **24** |
| DB 확장 후보 | **832행 · 고유 618키**(같은 키가 여러 경로에 나오면 하나로) — 테이블별: `visit_task` 62 · `purchase_item` 180 · 구매 항목 구성 스냅샷(새 표) 104 · `customer` 28 · `ticket_set` 53 · 병원 기본 운영 시간(새 표) 49 · `ticket_bundle` 38 · `visit` 10 · 기타 업무(새 표) 17 · `hospital` 19 · `purchase_transaction` 15 · 그 밖 16개 표 43(K3-2) |
| 확인 안 됨 | 키 **24**(K3-3) + HAR 없는 경로 **6** + DAY 가 읽는데 HAR 에서 값을 못 본 키 · 값 **11**(K5) |
| 정할 것 | **22**(K6 — 앞 판 C 번호와 겹치면 적음) |

핵심 사실 여섯:

1. **고객 키 24행(DAY 칼럼 22개)은 DAY 에 칼럼이 이미 있는데 동기화가 안 채운다**(`칸 있음 · 미동기화` · P24 기준 — 이메일 · 언어 · 여권 4 · 주민/외국인 등록번호 · 주소 3 · 동의 3 · 지정 의사/상담사 · 유입 2 · 추천인 · 등록 시각 · 삭제 · 수정 시각). DAY 는 고객을 **일정 안 `visitor`(12칸)** 로만 받는다(`emr/kos/mapper.py:300-329`). 그런데 HAR 상 **백필이 이미 부르는 `visitor/v2/queries/get-visitors` 목록 응답이 `get-visitor` 단건과 같은 키 63개(+ `count`)를 준다**(P20 · P24 키 비교 — `count` 하나만 다름). 지금은 `id` 만 읽는다(`emr/kos/sale_reads.py:316-333`).
2. **`칸 없음(시점 다름)` 306행은 대부분 「메뉴 참조의 그때 값」** — 구매 항목 · 시술권 세트 · 작업 · 희망 시술이 가리키는 상품 · 옵션 · 시술 항목 · 구성의 **산 시점 스냅샷**이다. DAY 는 이름 · 단위 · 가격 일부만 스냅샷으로 두고 나머지는 지금 메뉴 표(`treatment_item` · `product_option` …)에만 있다. data_rules 「메뉴 참조 = id + 그때 값 스냅샷」 기준으로 판정했다(K6-1).
3. **결제 수단 `CARD` 가 HAR 에 있다 — DAY 매핑 표 밖이라 카드 결제 거래 행이 동기화에서 빠진다.** 표는 `CASH` · `PREPAID_CARD` · `TRANSFER` 셋뿐이고(`emr/kos/mapper_sale_values.py:47-52` 「실측 셋만 — 나머지 넷 … 표본 없음(OQ-08-5)」), 표 밖 값은 그 행을 뺀다(`emr/kos/mapper_purchase.py:165-168` · `_sub_rows` `:192-204`). HAR P15 에는 `paymentType: CARD` 와 `cardConfiguration{approvalNumber, cardCompany.name}` 이 있다(K5-3 · K6-4).
4. **SPEC-000 은 `created_at ← KOS createdDateTimeUtc` 로 적었는데 코드는 받지 않는다** — 구매(`S0:1549`) · 거래(`:1601`) · 시술권(`:1665`) · 선불카드(`:1695`) · 상담 기록(`:537`). DAY `created_at` 은 지금 DAY 행 생성 시각이다(앞 판 E2 `purchasedDate` · `issuedDate`). data_rules 는 「DAY 테이블에는 created_at · updated_at · deleted_at 만」(K6-13).
5. **병원 정보 · 기본 운영 시간 · 휴무는 경로 자체를 부르지 않는다**(P25 · P26 · P27 — 칸 없음 62 · 시점 다름 1 · 일부러 안 둠 6 · 확인 안 됨 2). 병원 전화 · 주소는 `S0:278` 이 「두지 않는다(사용자 2026-11-03)」로 정했다 — 사용자 2026-11-20 「KOS 가 주는 키는 다 저장」과 맞부딪힌다(K6-8). 일부러 안 둠 54행 전체가 같은 문제다(K6-9).
6. **범위 때문에 비는 것**(K4): 미래 일정(오늘 창만) · 오늘 안 오는 고객의 고객 정보 · 시술권 · 카드 · 구매 · 칸 정원/예약 수 · `get-codes` 의 다른 범주(상담 결과 · 이미지) — 키를 다 받아도 이 범위면 그 행이 DAY 에 없다.

판정 기준(K2 전체에 같게):

- `저장됨` — 매퍼가 그 키를 읽어 DAY 칼럼에 쓴다(칼럼 `models/*.py:줄` + 매퍼 `emr/kos/*.py:줄`). 「새로 필요」 경로(P24 · P34 등)의 키는 **같은 값을 다른 경로(일정 안 visitor 등)로 이미 받으면** `저장됨` 으로 두고 비고에 그 경로를 적었다.
- `칸 있음 · 미동기화` — DAY 칼럼(또는 SPEC 이 그 키로 적은 칼럼)이 있는데 매퍼가 안 읽는다.
- `칸 없음(시점 다름)` — 같은 이름 칼럼이 있으나 다른 시점 · 다른 KOS 기록의 값(예: 지금 메뉴 값 vs 산 시점 스냅샷 · 상담 기록 상담사 vs 일정 단일 상담 정보 상담사).
- `일부러 안 둠` — 근거 문서:줄이 있을 때만. 근거 없으면 `칸 없음`(OQ 가 「열림」인 것도 `칸 없음` + 비고에 OQ).
- `계산으로 대체` — 다른 칸에서 얻는다(대부분 참조 객체의 `name` → join).
- `해당 없음` — 응답 껍데기 · 묶음(객체 · 배열 칸 자체 — 안쪽 키가 따로 행) · `count`.
- 참조 객체(예: `reservation.counselor`)와 그 `.id` 는 같은 판정으로 두었다.

## K1. 경로 목록

| # | 경로 | 갈래 | 공개/내부 | DAY 가 부르나(`backend/day/` 파일:줄) | 주기(앞 판 §B3) | HAR 엔트리(전체 · 200+JSON) | HAR 파일 | 스크립트 키 수 | K2 행 수 |
|---|---|---|---|---|---|---|---|---|---|
| P01 | `schedule/zone/v1/queries/get-zones` | DAY 부름 | 내부 | emr/kos/__init__.py:114 · 168 | 기준 정보 3600초 · 서버 시작 1회(tasks/emr.py:5-6 · 121-126) | 12 · 8 | 2026-10-12/…/로그인.har(1) · 2026-10-23/…/수납필요 확인.har(4) · 2026-10-23/…/예약그룹 .har(3) · 2026-10-23/…/예약그룹.har(3) · 2026-11-16/…/예약이력.har(1) | 5 | 5 |
| P02 | `schedule/zone/room/v1/queries/get-rooms` | DAY 부름 | 내부 | emr/kos/__init__.py:120 | 기준 정보 3600초 | 32 · 29 | 2026-10-12/…/시술완료.har(2) · 2026-10-12/…/시술완료_상태 copy.har(1) · 2026-10-12/…/시술현황_방배정.har(1) · 2026-10-12/…/시술현황_새로고침.har(1) · 2026-10-12/…/의사호출.har(2) · 2026-10-12/…/의사호출_2.har(2) · 2026-10-23/…/고객정보 수정.har(1) · 2026-10-23/…/설문전송.har(1) · 2026-10-23/…/예약현황_조회.har(1) · 2026-10-23/…/방배정.har(3) · 2026-11-09/…/고객예약접수시술.har(2) · 2026-11-09/…/방이동.har(2) · 2026-11-09/…/삭제후의사호출.har(1) · 2026-11-09/…/차트작성2.har(1) · 2026-11-09/…/차트작성3.har(4) · 2026-11-18/…/결제취소2.har(5) · 2026-11-18/…/수납추가.har(1) · 2026-11-18/…/시술사용후환불.har(1) | 5 | 5 |
| P03 | `schedule/group/v1/queries/get-reservation-groups` | DAY 부름 | 내부 | emr/kos/__init__.py:122-124 | 기준 정보 3600초 | 8 · 8 | 2026-10-23/…/수납필요 확인.har(2) · 2026-10-23/…/예약그룹 .har(1) · 2026-10-23/…/예약현황_조회.har(1) · 2026-10-23/…/예약그룹.har(1) · 2026-11-16/…/상담대기2.har(1) · 2026-11-16/…/상담대기3.har(1) · 2026-11-16/…/예약이력.har(1) | 63 | 63 |
| P04 | `role/v2/queries/get-roles` | DAY 부름 | 내부 | emr/kos/__init__.py:130 | 기준 정보 3600초 | 89 · 84 | 2026-10-12/…/로그인.har(1) · 2026-10-12/…/시술완료.har(2) · 2026-10-12/…/의사호출.har(1) · 2026-10-12/…/의사호출_2.har(1) · 2026-10-23/…/고객정보 수정.har(2) · 2026-10-23/…/공지사항.har(1) · 2026-10-23/…/국적_언어_여권번호변경.har(1) · 2026-10-23/…/귀가.har(1) · 2026-10-23/…/설문전송.har(1) · 2026-10-23/…/수납.har(4) · 2026-10-23/…/수납필요 추가.har(1) · 2026-10-23/…/수납필요 확인.har(2) · 2026-10-23/…/여권스캔.har(1) · 2026-10-23/…/예약.har(1) · 2026-10-23/…/예약그룹 .har(1) · 2026-10-23/…/예약부도.har(1) · 2026-10-23/…/예약상세_수정.har(1) · 2026-10-23/…/예약이동.har(1) · 2026-10-23/…/예약취소.har(1) · 2026-10-23/…/예약취소_되돌리기.har(1) · 2026-10-23/…/예약현황_조회.har(1) · 2026-10-23/…/처방전.har(10) · 2026-10-23/…/처방전상세.har(1) · 2026-10-23/…/방배정.har(2) · 2026-10-23/…/상담.har(3) · 2026-10-23/…/예약그룹.har(1) · 2026-11-09/…/고객예약접수시술.har(1) · 2026-11-09/…/삭제후의사호출.har(1) · 2026-11-09/…/차트작성2.har(1) · 2026-11-09/…/차트작성3.har(2) · 2026-11-16/…/병원정보.har(1) · 2026-11-16/…/상담대기.har(1) · 2026-11-16/…/상담대기2.har(1) · 2026-11-16/…/상담대기3.har(5) · 2026-11-16/…/예약이력.har(3) · 2026-11-18/…/결제 취소.har(1) · 2026-11-18/…/결제취소2.har(5) · 2026-11-18/…/고객상세.har(1) · 2026-11-18/…/고객정보.har(1) · 2026-11-18/…/다회권구매.har(1) · 2026-11-18/…/선불카드 결제.har(1) · 2026-11-18/…/선불카드.har(1) · 2026-11-18/…/선불카드결제.har(1) · 2026-11-18/…/선불카드결제취소.har(2) · 2026-11-18/…/선불카드공유.har(2) · 2026-11-18/…/선불카드생성.har(1) · 2026-11-18/…/수납.har(4) · 2026-11-18/…/수납추가.har(1) · 2026-11-18/…/시술권2.har(1) · 2026-11-18/…/용량,수량변경.har(1) · 2026-11-18/…/재결제.har(2) · 2026-11-18/…/환불1.har(1) · 2026-11-18/…/환불2.har(2) | 13 | 13 |
| P05 | `account/v2/queries/get-accounts` | DAY 부름 | 내부 | emr/kos/__init__.py:133-135 | 기준 정보 3600초 | 68 · 63 | 2026-10-12/…/의사호출_2.har(1) · 2026-10-23/…/고객정보 수정.har(5) · 2026-10-23/…/수납.har(3) · 2026-10-23/…/수납필요 추가.har(2) · 2026-10-23/…/수납필요 확인.har(7) · 2026-10-23/…/예약.har(4) · 2026-10-23/…/예약현황_조회.har(2) · 2026-10-23/…/처방전.har(1) · 2026-10-23/…/처방전상세.har(2) · 2026-11-09/…/고객예약접수시술.har(2) · 2026-11-09/…/방이동.har(2) · 2026-11-11/…/상품 수납.har(4) · 2026-11-16/…/상담대기.har(1) · 2026-11-16/…/상담대기2.har(4) · 2026-11-16/…/상담대기3.har(4) · 2026-11-16/…/예약이력.har(2) · 2026-11-18/…/고객상세.har(8) · 2026-11-18/…/고객정보조회 .har(3) · 2026-11-18/…/다회권구매.har(1) · 2026-11-18/…/상품 수납.har(4) · 2026-11-18/…/선불카드결제.har(1) · 2026-11-18/…/선불카드결제취소.har(1) · 2026-11-18/…/수납.har(3) · 2026-11-18/…/수납추가.har(1) | 19 | 19 |
| P06 | `meta/codes/v1/queries/get-codes` | DAY 부름 | 내부 | emr/kos/__init__.py:139 | 기준 정보 3600초(VISITOR_CATEGORY · FUNNEL_CATEGORY · FUNNEL) | 148 · 146 | 2026-10-12/…/로그인.har(1) · 2026-10-23/…/고객정보 수정.har(5) · 2026-10-23/…/수납필요 확인.har(13) · 2026-10-23/…/여권스캔.har(2) · 2026-10-23/…/예약.har(19) · 2026-10-23/…/예약그룹 .har(5) · 2026-10-23/…/예약상세_수정.har(5) · 2026-10-23/…/예약취소.har(4) · 2026-10-23/…/처방전상세.har(5) · 2026-10-23/…/방배정.har(7) · 2026-10-23/…/상담.har(3) · 2026-10-23/…/예약그룹.har(5) · 2026-11-09/…/고객예약접수시술.har(1) · 2026-11-11/…/상품 수납.har(13) · 2026-11-16/…/상담대기.har(5) · 2026-11-16/…/상담대기2.har(9) · 2026-11-16/…/상담대기3.har(14) · 2026-11-16/…/예약이력.har(2) · 2026-11-18/…/고객상세.har(5) · 2026-11-18/…/고객정보.har(5) · 2026-11-18/…/고객정보조회 .har(2) · 2026-11-18/…/상품 수납.har(13) · 2026-11-18/…/시술권2.har(5) | 8 | 8 |
| P07 | `schedule/v2/queries/get-schedules-grouped-by-zone` | DAY 부름 | 내부 | emr/kos/__init__.py:171-175 | 10초 · 병원 현지 오늘 창만(services/emr_sync.py:111-115) · 백필(어제까지 · 수동) | 5 · 3 | 2026-10-12/…/시술현황_새로고침.har(1) · 2026-10-23/…/귀가.har(2) · 2026-10-23/…/방배정.har(2) | 230 | 230 |
| P08 | `schedule/v1/queries/get-schedule-detail` | DAY 부름 | 내부 | emr/kos/__init__.py:214 | 이벤트 — 작업 다시 읽기(services/emr_sync.py:324 · 364) | 18 · 17 | 2026-10-23/…/수납필요 확인.har(1) · 2026-10-23/…/예약.har(3) · 2026-10-23/…/예약상세_수정.har(1) · 2026-10-23/…/예약취소.har(1) · 2026-10-23/…/처방전상세.har(1) · 2026-10-23/…/방배정.har(1) · 2026-11-11/…/상품 수납.har(2) · 2026-11-16/…/상담대기.har(1) · 2026-11-16/…/상담대기2.har(1) · 2026-11-16/…/상담대기3.har(2) · 2026-11-18/…/고객정보.har(1) · 2026-11-18/…/상품 수납.har(2) · 2026-11-18/…/시술권2.har(1) | 242 | 242 |
| P09 | `procedure-menu/categories/queries/get-categories` | DAY 부름 | 내부 | emr/kos/sale_reads.py:163-165 | 메뉴 — 기준 정보 회차 뒤(tasks/emr.py:89-95) | 10 · 7 | 2026-11-09/…/고객예약접수시술.har(2) · 2026-11-11/…/상품 수납.har(3) · 2026-11-18/…/상품 수납.har(3) · 2026-11-18/…/수납추가.har(1) · 2026-11-18/…/환불2.har(1) | 14 | 14 |
| P10 | `procedure-menu/products/queries/get-products` | DAY 부름 | 내부 | emr/kos/sale_reads.py:168-170 | 메뉴 | 7 · 5 | 2026-11-11/…/상품 수납.har(3) · 2026-11-18/…/상품 수납.har(3) · 2026-11-18/…/상품가격.har(1) | 210 | 210 |
| P11 | `procedure-menu/v2/queries/get-procedures` | DAY 부름 | 내부 | emr/kos/sale_reads.py:192 | 메뉴 | 12 · 8 | 2026-11-11/…/상품 수납.har(6) · 2026-11-18/…/상품 수납.har(6) | 7 | 7 |
| P12 | `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks` | DAY 부름 | 내부 | emr/kos/sale_reads.py:199 | 메뉴 | 4 · 2 | 2026-10-23/…/방배정.har(2) · 2026-11-09/…/고객예약접수시술.har(2) | 7 | 7 |
| P13 | `procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product` | DAY 부름 | 내부 | emr/kos/sale_reads.py:207-209 | 메뉴(closed false · true 두 번) | 5 · 5 | 2026-11-18/…/결제취소2.har(1) · 2026-11-18/…/선불카드결제.har(1) · 2026-11-18/…/선불카드결제취소.har(1) · 2026-11-18/…/수납추가.har(1) · 2026-11-18/…/환불2.har(1) | 21 | 21 |
| P14 | `procedure-menu/etcetera-products/v1/queries/get-etcetera-products` | DAY 부름 | 내부 | emr/kos/sale_reads.py:213 | 메뉴 | 3 · 2 | 2026-11-09/…/고객예약접수시술.har(2) · 2026-11-18/…/수납추가.har(1) | 13 | 13 |
| P15 | `purchase/v1/queries/get-purchase-summaries` | DAY 부름 | 내부 | emr/kos/sale_reads.py:250-252 | 일정 회차 뒤 별도 태스크 — 오늘 일정의 purchaseIds(tasks/emr.py:74-85 · 98-105) · 백필 | 433 · 427 | 2026-10-23/…/귀가.har(1) · 2026-10-23/…/수납.har(26) · 2026-10-23/…/수납필요 추가.har(26) · 2026-10-23/…/수납필요 확인.har(13) · 2026-10-23/…/여권스캔.har(13) · 2026-10-23/…/처방전상세.har(6) · 2026-11-09/…/고객예약접수시술.har(15) · 2026-11-09/…/차트작성.har(15) · 2026-11-11/…/상품 수납.har(28) · 2026-11-18/…/결제 취소.har(7) · 2026-11-18/…/결제취소2.har(24) · 2026-11-18/…/다회권구매.har(6) · 2026-11-18/…/상품 수납.har(28) · 2026-11-18/…/선불카드 결제.har(4) · 2026-11-18/…/선불카드.har(7) · 2026-11-18/…/선불카드결제.har(14) · 2026-11-18/…/선불카드결제취소.har(26) · 2026-11-18/…/선불카드공유.har(8) · 2026-11-18/…/수납.har(26) · 2026-11-18/…/수납추가.har(10) · 2026-11-18/…/시술권2.har(2) · 2026-11-18/…/시술사용후환불.har(24) · 2026-11-18/…/용량,수량변경.har(14) · 2026-11-18/…/재결제.har(15) · 2026-11-18/…/환불1.har(17) · 2026-11-18/…/환불2.har(58) | 455 | 455 |
| P16 | `ticket/v1/queries/get-ticket-bundles` | DAY 부름 | 내부 | emr/kos/sale_reads.py:263-269 | 오늘 일정 고객(services/emr_sale_sync.py:257) · 백필(services/emr_backfill.py:369) | 48 · 46 | 2026-10-23/…/고객정보 수정.har(3) · 2026-10-23/…/국적_언어_여권번호변경.har(2) · 2026-10-23/…/수납필요 추가.har(5) · 2026-10-23/…/수납필요 확인.har(1) · 2026-10-23/…/예약.har(5) · 2026-10-23/…/예약상세_수정.har(1) · 2026-10-23/…/예약취소.har(1) · 2026-10-23/…/처방전상세.har(1) · 2026-10-23/…/방배정.har(2) · 2026-11-09/…/고객예약접수시술.har(2) · 2026-11-11/…/상품 수납.har(3) · 2026-11-16/…/상담대기.har(1) · 2026-11-16/…/상담대기2.har(2) · 2026-11-16/…/상담대기3.har(3) · 2026-11-18/…/고객상세.har(3) · 2026-11-18/…/고객정보.har(1) · 2026-11-18/…/고객정보조회 .har(2) · 2026-11-18/…/상품 수납.har(3) · 2026-11-18/…/시술권2.har(1) · 2026-11-18/…/시술사용후환불.har(3) · 2026-11-18/…/환불1.har(1) · 2026-11-18/…/환불2.har(2) | 116 | 116 |
| P17 | `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` | DAY 부름 | 내부 | emr/kos/sale_reads.py:282-284 | 오늘 일정 고객(services/emr_sale_sync.py:258) · 백필(:420) | 103 · 99 | 2026-10-23/…/고객정보 수정.har(1) · 2026-10-23/…/수납.har(3) · 2026-10-23/…/수납필요 추가.har(4) · 2026-10-23/…/수납필요 확인.har(3) · 2026-10-23/…/예약.har(3) · 2026-10-23/…/예약상세_수정.har(1) · 2026-10-23/…/예약취소.har(1) · 2026-10-23/…/처방전상세.har(1) · 2026-10-23/…/방배정.har(1) · 2026-11-09/…/고객예약접수시술.har(2) · 2026-11-11/…/상품 수납.har(4) · 2026-11-16/…/상담대기.har(1) · 2026-11-16/…/상담대기2.har(1) · 2026-11-16/…/상담대기3.har(2) · 2026-11-18/…/결제 취소.har(3) · 2026-11-18/…/결제취소2.har(9) · 2026-11-18/…/고객상세.har(2) · 2026-11-18/…/고객정보.har(1) · 2026-11-18/…/고객정보조회 .har(1) · 2026-11-18/…/다회권구매.har(2) · 2026-11-18/…/상품 수납.har(4) · 2026-11-18/…/선불카드 결제.har(1) · 2026-11-18/…/선불카드.har(1) · 2026-11-18/…/선불카드결제.har(3) · 2026-11-18/…/선불카드결제취소.har(6) · 2026-11-18/…/선불카드생성.har(2) · 2026-11-18/…/수납.har(3) · 2026-11-18/…/수납추가.har(2) · 2026-11-18/…/시술권2.har(1) · 2026-11-18/…/시술사용후환불.har(6) · 2026-11-18/…/재결제.har(6) · 2026-11-18/…/환불1.har(5) · 2026-11-18/…/환불2.har(17) | 23 | 23 |
| P18 | `purchase/prepaid-card/v1/queries/get-prepaid-card-charging-events` | DAY 부름 | 내부 | emr/kos/sale_reads.py:296 | 바뀐 카드(services/emr_sale_sync.py:268) · 백필(:430) | 5 · 5 | 2026-11-18/…/선불카드결제.har(1) · 2026-11-18/…/선불카드결제취소.har(1) · 2026-11-18/…/선불카드생성.har(3) | 15 | 15 |
| P19 | `purchase/prepaid-card/v1/queries/get-prepaid-card-visitors` | DAY 부름 | 내부 | emr/kos/sale_reads.py:297 | 바뀐 카드(위와 같음) | 6 · 6 | 2026-11-18/…/선불카드결제.har(1) · 2026-11-18/…/선불카드결제취소.har(1) · 2026-11-18/…/선불카드공유.har(1) · 2026-11-18/…/선불카드생성.har(3) | 5 | 5 |
| P20 | `visitor/v2/queries/get-visitors` | DAY 부름 | 내부 | emr/kos/sale_reads.py:323 | 백필만(수동 · services/emr_backfill.py:396) — id · count 만 읽음 | 10 · 8 | 2026-10-23/…/고객정보 수정.har(1) · 2026-10-23/…/예약.har(3) · 2026-11-16/…/상담대기2.har(1) · 2026-11-16/…/상담대기3.har(1) · 2026-11-18/…/고객상세.har(2) · 2026-11-18/…/고객정보조회 .har(1) · 2026-11-18/…/선불카드공유.har(1) | 64 | 64 |
| P21 | `v1/account/queries/get-user-account` | DAY 부름 | 내부(테넌트 경로) | emr/kos/client.py:422 · emr/kos/staff_client.py:154 | 로그인 때(services/auth.py) | 2 · 1 | 2026-10-12/…/로그인.har(2) | 11 | 11 |
| P22 | `common/v1/tenant/queries/get-user-tenants` | DAY 부름 | 내부(테넌트 밖) | emr/kos/staff_client.py:136 | 로그인 때(services/auth.py:273) | 2 · 1 | 2026-10-12/…/로그인.har(2) | 8 | 8 |
| P23 | `common/user/v1/queries/get-active-sign-ins` | DAY 부름 | 내부(테넌트 밖) | emr/kos/client.py:190 | 로그인 기기 제한 때(services/auth.py:410) | 0 · 0 | **없음** | 0 | 0 |
| P24 | `visitor/v2/queries/get-visitor` | 새로 필요 | 내부 | 부르지 않음 | cc: 요청마다(앞 판 E2 · E8) | 54 · 52 | 2026-10-23/…/고객정보 수정.har(4) · 2026-10-23/…/국적_언어_여권번호변경.har(1) · 2026-10-23/…/수납필요 확인.har(1) · 2026-10-23/…/예약.har(5) · 2026-10-23/…/예약상세_수정.har(2) · 2026-10-23/…/예약이동.har(1) · 2026-10-23/…/예약취소.har(2) · 2026-10-23/…/처방전상세.har(3) · 2026-10-23/…/방배정.har(1) · 2026-11-11/…/상품 수납.har(7) · 2026-11-16/…/상담대기.har(3) · 2026-11-16/…/상담대기2.har(2) · 2026-11-16/…/상담대기3.har(4) · 2026-11-18/…/고객상세.har(6) · 2026-11-18/…/고객정보.har(2) · 2026-11-18/…/고객정보조회 .har(1) · 2026-11-18/…/상품 수납.har(7) · 2026-11-18/…/시술권2.har(2) | 63 | 63 |
| P25 | `v1/hospital/queries/get-hospital` | 새로 필요 | 내부 | 부르지 않음 | cc: 요청마다(앞 판 E12) | 2 · 2 | 2026-11-16/…/병원정보.har(1) · 2026-11-16/…/예약이력.har(1) | 22 | 22 |
| P26 | `schedule/default-operation-time/v1/queries/get-default-operation-timetable` | 새로 필요 | 내부 | 부르지 않음 | cc: 요청마다(앞 판 E12) | 16 · 16 | 2026-10-23/…/수납필요 확인.har(1) · 2026-10-23/…/예약.har(4) · 2026-10-23/…/예약현황_조회.har(1) · 2026-11-11/…/상품 수납.har(2) · 2026-11-16/…/상담대기2.har(3) · 2026-11-16/…/상담대기3.har(3) · 2026-11-18/…/상품 수납.har(2) | 50 | 50 |
| P27 | `schedule/default-operation-time/v1/queries/get-default-days-off` | 새로 필요 | 내부 | 부르지 않음 | cc: 요청마다 · 오늘~+90일(앞 판 E12) | 22 · 22 | 2026-10-23/…/수납필요 확인.har(3) · 2026-10-23/…/예약.har(6) · 2026-10-23/…/예약현황_조회.har(1) · 2026-11-11/…/상품 수납.har(2) · 2026-11-16/…/상담대기2.har(4) · 2026-11-16/…/상담대기3.har(4) · 2026-11-18/…/상품 수납.har(2) | 1 | 1 |
| P28 | `schedule/open/v2/queries/get-reservation-slots-by-groups` | 새로 필요 | 공개 | 부르지 않음 | cc: 요청마다(앞 판 E4) | 0 · 0 | **없음** | 0 | 0 |
| P29 | `schedule/open/v1/queries/get-schedules-by-visitor` | 새로 필요 | 공개 | 부르지 않음 | cc: 요청마다(앞 판 E5 · E6 · E8) | 0 · 0 | **없음** | 0 | 0 |
| P30 | `visitor/open/v1/queries/get-visitor-questionnaire` | 새로 필요 | 공개 | 부르지 않음 | cc: 상세 요청마다(앞 판 E8 health) | 0 · 0 | **없음** | 0 | 0 |
| P31 | `visitor/open/v1/queries/get-questionnaire-submit` | 새로 필요 | 공개 | 부르지 않음 | cc: 상세 요청마다(앞 판 E8 health) | 0 · 0 | **없음** | 0 | 0 |
| P32 | `schedule/v1/queries/get-schedule-event-logs` | 새로 필요 | 내부 | 부르지 않음 | cc: 접수 목록 요청 때(앞 판 E7 firstConsultationWaitingAt) | 0 · 0 | **없음** | 0 | 0 |
| P33 | `schedule/v2/queries/get-schedules-for-reservation` | 새로 필요 | 내부 | 부르지 않음(DAY 는 P07 로 대체) | cc: 그날 · 10초 캐시(앞 판 「cc reservation 사본」) | 19 · 19 | 2026-10-23/…/수납필요 확인.har(1) · 2026-10-23/…/예약.har(2) · 2026-10-23/…/예약현황_조회.har(2) · 2026-11-11/…/상품 수납.har(4) · 2026-11-16/…/상담대기2.har(3) · 2026-11-16/…/상담대기3.har(3) · 2026-11-18/…/상품 수납.har(4) | 226 | 226 |
| P34 | `visitor/v1/queries/find-duplicated-visitor` | 새로 필요 | 내부 | 부르지 않음 | cc: 예약 쓰기 때(앞 판 B2 E3) | 6 · 3 | 2026-10-23/…/고객정보 수정.har(2) · 2026-10-23/…/국적_언어_여권번호변경.har(2) · 2026-10-23/…/예약.har(2) | 49 | 49 |

### K1-1. 센 명령

**DAY 부름 23** — 경로 상수(문자열)를 모았다:

```sh
git -C /Users/kknaks/git/CENTURION_DAY grep -hoE '"[^" ]*queries/[^" ]*"' origin/dev -- \
  'backend/day/emr/kos/*.py' 'backend/day/emr/*.py' 'backend/day/services/emr_*.py' ':!backend/day/emr/kos/demo/*' \
  | sort -u | wc -l        # → 23
```

- 23개 모두 실제 호출부가 있다(K1 표 「DAY 가 부르나」 — 상수 이름으로 `git grep` 한 줄). `v1/account/queries/get-user-account` 는 두 파일(`emr/kos/client.py:47` · `emr/kos/staff_client.py:57`)에 같은 문자열.
- 쓰기(`/commands/`) 경로는 브리프 범위 밖이라 세지 않았다(토큰 교환 · sign-in · `writes.py` 10개 등).
- `emr/sync_*.py` · `services/emr_*.py` 에는 KOS 경로 문자열이 없다(위 명령의 그 두 pathspec 기여 0 — 경로는 어댑터 `emr/kos/` 에만).

**새로 필요 11** — 앞 판 리포트가 「DAY 에 없음」으로 적은 KOS 읽기 경로:

```sh
grep -oE '[a-z0-9-]+(/[A-Za-z0-9{}_-]+)*/queries/[A-Za-z0-9-]+' orchestration/work/day-cc-mig/research-cc-ext-report.md | sort -u
git -C /Users/kknaks/git/toy_pr2/cc-prototype grep -noE '"[^" ]*(get-default-days-off|get-questionnaire-submit|…)[^" ]*"' origin/main -- procedure/back/app   # 줄임 경로 · 짧은 이름의 전체 경로
```

- 앞 판에서 나온 읽기 경로 16(+ 줄임 `.../get-default-days-off` · 짧은 이름 `get-questionnaire-submit` 을 cc 상수로 풀어 `cc:service/ext.py:84` · `cc:service/reservations.py:82`) = 18 중 **DAY 가 이미 부르는 5**(`account/v2/get-accounts` · `role/v2/get-roles` · `schedule/v1/get-schedule-detail` · `ticket/v1/get-ticket-bundles` · `visitor/v2/get-visitors`)와 **DAY 가 내부 대응 경로로 이미 받는 공개 2**(`account/open/v1/queries/get-accounts` → 내부 `account/v2` · `emr/kos/__init__.py:22-23` · `purchase/open/prepaid-card/v1/queries/get-prepaid-card-summaries` → 내부 `purchase/prepaid-card/v1/...`)를 빼면 11. `visitor/v1/queries/find-duplicated-visitor` 는 예약 쓰기(E3) 흐름의 **읽기** 경로라 넣었다.
- `schedule/v2/queries/get-schedules-for-reservation`(P33)은 cc 의 일정 원천(앞 판 「cc reservation 사본」)이고 DAY 는 P07 로 대체한다 — 같은 일정 객체라 같은 규칙으로 대조했다.

**HAR 에만 43** — HAR 67개 요청 URL 중 `/queries/` 가 든 서로 다른 경로(테넌트 접두 `tenants/{id}/` 제거)는 **71**(부록 A `keys.py paths` · `collect.py`). 그중 K1 의 34경로에 드는 것 **28**, 나머지 **43** = K1-2 표 행 수. (71 중 70 은 200 + JSON 응답이 1건 이상 있고, `purchase/tax-refund-settings/...` 하나는 200 JSON 응답이 없다.)

### K1-2. HAR 에만 있는 읽기 경로(대조 안 함 · 목록만)

센 방법: HAR 67개의 요청 URL 중 `/queries/` 가 든 경로(테넌트 접두 제거) − K1 의 34경로. 「무엇인지」는 **경로 이름 · HAR 파일 이름 풀이**이고 응답 키로 확인한 것이 아니다.

| # | 경로 | 엔트리 | HAR 파일 | 무엇인지(이름 풀이) |
|---|---|---|---|---|
| 1 | `account/v2/queries/get-accounts-last-update-date-time-utc` | 96 | 2026-10-12/…/시술완료_상태 copy.har · 2026-10-12/…/시술현황_방배정.har · 2026-10-12/…/시술현황_새로고침.har 외 31 | 직원 목록 마지막 수정 시각(바뀐 것만 받기용으로 보임) |
| 2 | `account/v2/queries/get-accounts-status` | 8 | 2026-10-12/…/로그인.har · 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/예약그룹 .har 외 1 | 직원 계정 상태 |
| 3 | `common/feature-flags/v1/queries/get-feature-flags` | 2 | 2026-10-12/…/로그인.har | KOS 기능 플래그 |
| 4 | `common/kcd-codes/v1/queries/get-kcd-codes` | 1 | 2026-10-23/…/처방전상세.har | KCD(질병 분류) 코드 — 처방 화면 |
| 5 | `common/medicine-and-machines/v2/queries/get-medicine-and-machines` | 6 | 2026-11-11/…/상품 수납.har · 2026-11-18/…/상품 수납.har | 약물 · 기기 목록(DAY 는 상품 응답 안에서 모은다 — S0 메뉴) |
| 6 | `consultation/v1/queries/get-consultations-by-visitor-id` | 24 | 2026-10-23/…/고객정보 수정.har · 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/예약.har 외 14 | 고객별 상담 기록 목록 — 상담 차트 이력 |
| 7 | `image/visitor-image/v1/queries/get-visitor-images` | 8 | 2026-10-23/…/수납필요 추가.har · 2026-10-23/…/여권스캔.har · 2026-10-23/…/처방전상세.har 외 2 | 고객 이미지(여권 스캔 등) |
| 8 | `meta/connect/v1/queries/get-connect-apps` | 10 | 2026-10-23/…/고객정보 수정.har · 2026-10-23/…/예약.har · 2026-11-11/…/상품 수납.har 외 2 | KOS 연결 앱 목록 |
| 9 | `meta/notice/v1/queries/get-notices` | 20 | 2026-10-12/…/로그인.har · 2026-10-12/…/시술현황_새로고침.har · 2026-10-23/…/공지사항.har 외 8 | KOS 공지 |
| 10 | `meta/template/v1/queries/get-hospital-text-snippets` | 9 | 2026-10-12/…/로그인.har · 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/처방전상세.har 외 4 | 병원 문구 조각(템플릿) |
| 11 | `notification/computer-telephone/v1/queries/find-computer-telephone-settings` | 6 | 2026-10-12/…/로그인.har · 2026-10-23/…/예약그룹 .har · 2026-10-23/…/예약그룹.har | CTI(전화) 설정 |
| 12 | `notification/message/sender/v1/queries/get-sender-profiles` | 2 | 2026-11-18/…/고객상세.har | 메시지 발신 프로필 |
| 13 | `prescription/v1/queries/get-prescription` | 3 | 2026-10-23/…/처방전.har | 처방전 단건 |
| 14 | `prescription/v1/queries/get-prescriptions` | 1 | 2026-11-18/…/환불2.har | 처방전 목록 |
| 15 | `prescription/v1/queries/get-prescriptions-by-ids` | 1 | 2026-10-23/…/처방전상세.har | 처방전 여러 건(id 로) |
| 16 | `procedure-menu/currency-settings/queries/get-currency-settings` | 30 | 2026-10-23/…/수납.har · 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/예약.har 외 11 | 통화 설정 — S0:1505 「두지 않음(지금)」 |
| 17 | `procedure-menu/procedure-categories/queries/get-procedure-categories` | 6 | 2026-11-11/…/상품 수납.har · 2026-11-18/…/상품 수납.har | 시술 카테고리 목록 — S0 OQ-041-3 |
| 18 | `procedure-menu/product-options/v2/queries/search-product-option-summaries` | 36 | 2026-10-23/…/수납.har · 2026-10-23/…/수납필요 추가.har · 2026-10-23/…/수납필요 확인.har 외 11 | 상품 옵션 검색(수납 화면) |
| 19 | `procedure-menu/products/queries/get-product` | 9 | 2026-11-11/…/상품 수납.har · 2026-11-18/…/상품 수납.har · 2026-11-18/…/상품가격.har | 상품 단건 |
| 20 | `procedure-menu/products/v3/queries/get-products` | 5 | 2026-11-09/…/고객예약접수시술.har · 2026-11-18/…/수납추가.har · 2026-11-18/…/환불2.har | 상품 목록 v3(DAY 는 v1 경로) |
| 21 | `procedure-menu/target-countries/v1/queries/get-target-countries` | 18 | 2026-10-12/…/로그인.har · 2026-10-23/…/고객정보 수정.har · 2026-10-23/…/수납필요 확인.har 외 6 | 타겟 국가 — S0:1505 「두지 않음(지금)」 |
| 22 | `procedure-menu/vat-settings/queries/get-vat-settings` | 10 | 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/처방전상세.har · 2026-10-23/…/방배정.har 외 5 | 부가세 설정 — S0:1505 「두지 않음(지금)」 |
| 23 | `procedure-menu/visitors/queries/get-visitors` | 99 | 2026-10-23/…/고객정보 수정.har · 2026-10-23/…/귀가.har · 2026-10-23/…/설문전송.har 외 36 | 메뉴 쪽 고객 조회(가격 · 수가 유형용으로 보임) |
| 24 | `purchase/payment-settings/v1/queries/get-payment-settings` | 44 | 2026-10-23/…/수납.har · 2026-10-23/…/수납필요 추가.har · 2026-10-23/…/수납필요 확인.har 외 20 | 결제 수단 설정 |
| 25 | `purchase/prepaid-card/v1/queries/get-visitor-prepaid-card-balance` | 25 | 2026-10-23/…/고객정보 수정.har · 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/예약.har 외 16 | 고객별 선불카드 잔액 합 |
| 26 | `purchase/tax-refund-receipts/v1/queries/get-tax-refund-receipts` | 4 | 2026-11-18/…/시술사용후환불.har · 2026-11-18/…/환불1.har · 2026-11-18/…/환불2.har | 택스 리펀드 영수증 |
| 27 | `purchase/tax-refund-settings/v1/queries/get-tax-refund-settings` | 9 | 2026-10-12/…/로그인.har · 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/처방전상세.har 외 4 | 택스 리펀드 설정 |
| 28 | `schedule/default-operation-time/v1/queries/get-default-reservation-policy` | 9 | 2026-10-23/…/예약.har · 2026-11-16/…/상담대기2.har · 2026-11-16/…/상담대기3.har | 병원 기본 예약 정책 |
| 29 | `schedule/group/v1/queries/get-reservation-group` | 151 | 2026-10-23/…/귀가.har · 2026-10-23/…/설문전송.har · 2026-10-23/…/수납.har 외 36 | 예약 그룹 단건 |
| 30 | `schedule/group/v1/queries/get-reservation-group-days-offs` | 15 | 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/예약.har · 2026-10-23/…/예약현황_조회.har 외 4 | 예약 그룹 휴무 — 앞 판 E4 가능 시간대와 닿음 |
| 31 | `schedule/occupied-time/v2/queries/get-occupied-times` | 12 | 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/예약.har · 2026-10-23/…/예약현황_조회.har 외 4 | 점유 시간(예약 현황) |
| 32 | `schedule/reservation-rule/v1/queries/get-reservation-rule` | 5 | 2026-10-23/…/예약.har · 2026-11-16/…/상담대기2.har · 2026-11-16/…/상담대기3.har | 예약 규칙 단건 |
| 33 | `schedule/reservation-rule/v1/queries/get-reservation-rule-summaries` | 5 | 2026-10-23/…/예약.har · 2026-11-16/…/상담대기2.har · 2026-11-16/…/상담대기3.har | 예약 규칙 목록 |
| 34 | `schedule/reservation-time-slot/v1/queries/get-occupied-resources-by-reservation-time-slot` | 9 | 2026-10-23/…/예약.har · 2026-11-16/…/상담대기2.har · 2026-11-16/…/상담대기3.har | 예약 칸별 점유 — 앞 판 E4 와 닿음 |
| 35 | `schedule/reservation-time-slot/v1/queries/get-reservation-time-slots` | 13 | 2026-10-23/…/예약.har · 2026-11-16/…/상담대기2.har · 2026-11-16/…/상담대기3.har | 예약 칸(타임 슬롯) — 앞 판 E4 와 닿음 |
| 36 | `schedule/v1/queries/get-payment-required-tasks` | 26 | 2026-10-23/…/고객정보 수정.har · 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/예약.har 외 13 | 수납 필요 작업 |
| 37 | `schedule/v1/queries/get-schedule-summaries` | 73 | 2026-10-23/…/고객정보 수정.har · 2026-10-23/…/국적_언어_여권번호변경.har · 2026-10-23/…/귀가.har 외 38 | 일정 요약 목록 — 희망 시술 안쪽 키가 보이는 유일한 HAR 경로(K5-2) |
| 38 | `schedule/v2/queries/get-schedule-list-items` | 1 | 2026-11-16/…/예약이력.har | 일정 목록 항목(예약이력.har) — 앞 판 E5 · E6 과 닿음 |
| 39 | `security/v2/queries/check-message-permission` | 14 | 2026-10-23/…/고객정보 수정.har · 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/예약.har 외 6 | 메시지 권한 확인 |
| 40 | `v1/visitor/queries/get-visitor` | 85 | 2026-10-23/…/귀가.har · 2026-10-23/…/설문전송.har · 2026-10-23/…/수납.har 외 29 | 고객 단건 v1(DAY · cc 는 v2) |
| 41 | `visitor/files/v1/queries/get-visitor-files` | 1 | 2026-11-18/…/다회권구매.har | 고객 파일 |
| 42 | `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` | 26 | 2026-10-23/…/고객정보 수정.har · 2026-10-23/…/수납필요 확인.har · 2026-10-23/…/예약.har 외 13 | 문진 제출본(내부 · legacy) — P31 공개 경로의 내부 쪽으로 보임 · 같은지 확인 안 됨 |
| 43 | `visitor/v1/queries/get-custom-attribute-definitions` | 9 | 2026-10-23/…/고객정보 수정.har · 2026-10-23/…/예약.har · 2026-11-11/…/상품 수납.har 외 2 | 고객 사용자 정의 항목 정의 — S0:312 반려(`custom_attributes`) |

## K2. 키 전수 대조

읽는 법: 판정 = `저장됨` · `칸 있음 · 미동기화` · `칸 없음` · `칸 없음(시점 다름)` · `일부러 안 둠` · `계산으로 대체` · `해당 없음` · `확인 안 됨`. 근거의 코드 줄은 CENTURION_DAY `origin/dev` `844eace4` 의 `backend/day/` 아래(`models/…` · `emr/…` · `services/…`), `S0:줄` = mediness `origin/main` `ccede286` `products/day/20-spec/spec-000-data-model.md`. 「묶음」= 객체 · 배열 칸 자체(안쪽 키가 따로 행). 「JSON 통째」= 그 하위 키가 한 jsonb 칸에 그대로 들어간다. 타입 · 모양만 적고 값은 적지 않았다(enum 은 KOS 코드값만).

### P01 `schedule/zone/v1/queries/get-zones`

스크립트 합집합 키 **5** · 표 행 **5** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:142 |
| 3 | `data[].isDefault` | bool | zone.is_default (models/room.py:37) | 저장됨 | emr/kos/mapper.py:145 |
| 4 | `data[].order` | int | zone.sort_order (models/room.py:36) | 저장됨 | emr/kos/mapper.py:144 |
| 5 | `data[].title` | string | zone.title (models/room.py:35) | 저장됨 | emr/kos/mapper.py:143 |

### P02 `schedule/zone/room/v1/queries/get-rooms`

스크립트 합집합 키 **5** · 표 행 **5** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:152 |
| 3 | `data[].order` | int | room.sort_order (models/room.py:49) | 저장됨 | emr/kos/mapper.py:155 |
| 4 | `data[].title` | string | room.title (models/room.py:48) | 저장됨 | emr/kos/mapper.py:154 |
| 5 | `data[].zoneId` | string | room.zone_id (models/room.py:47) | 저장됨 | emr/kos/mapper.py:153 |

### P03 `schedule/group/v1/queries/get-reservation-groups`

스크립트 합집합 키 **63** · 표 행 **63** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:203 |
| 3 | `data[].intervalCapacities[]` | array / object | reservation_group_capacity (models/room.py:68) | 저장됨 | emr/kos/mapper.py:189-201 |
| 4 | `data[].intervalCapacities[].enabled` | bool | 행 있음 = 켜짐 | 계산으로 대체 | emr/kos/mapper.py:190-191 — 꺼진 구역은 행을 만들지 않는다 |
| 5 | `data[].intervalCapacities[].intervalCapacity` | int | reservation_group_capacity.capacity (models/room.py:74) | 저장됨 | emr/kos/mapper.py:197-199 |
| 6 | `data[].intervalCapacities[].zoneId` | string | reservation_group_capacity.zone_id (models/room.py:73) | 저장됨 | emr/kos/mapper.py:194-196 |
| 7 | `data[].intervalMinutes` | int | reservation_group.interval_minutes (models/room.py:61) | 저장됨 | emr/kos/mapper.py:206 |
| 8 | `data[].isDefault` | bool |  | 칸 없음 | 기본 예약 그룹 — cc ext E4 가 「기본 그룹」을 쓴다 |
| 9 | `data[].memo` | string(empty) |  | 칸 없음 |  |
| 10 | `data[].operationTimetable` | object | reservation_group_timetable (models/room.py:80) | 저장됨 | emr/kos/mapper.py:165-183 |
| 11 | `data[].operationTimetable.friday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | emr/kos/mapper.py:125-133 · 168 |
| 12 | `data[].operationTimetable.friday.breaktime` | object |  | 해당 없음 | 묶음 |
| 13 | `data[].operationTimetable.friday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | emr/kos/mapper.py:180 |
| 14 | `data[].operationTimetable.friday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | emr/kos/mapper.py:179 |
| 15 | `data[].operationTimetable.friday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | emr/kos/mapper.py:174-176 |
| 16 | `data[].operationTimetable.friday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | emr/kos/mapper.py:178 |
| 17 | `data[].operationTimetable.friday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 |
| 18 | `data[].operationTimetable.monday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | emr/kos/mapper.py:125-133 · 168 |
| 19 | `data[].operationTimetable.monday.breaktime` | object |  | 해당 없음 | 묶음 |
| 20 | `data[].operationTimetable.monday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | emr/kos/mapper.py:180 |
| 21 | `data[].operationTimetable.monday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | emr/kos/mapper.py:179 |
| 22 | `data[].operationTimetable.monday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | emr/kos/mapper.py:174-176 |
| 23 | `data[].operationTimetable.monday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | emr/kos/mapper.py:178 |
| 24 | `data[].operationTimetable.monday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 |
| 25 | `data[].operationTimetable.saturday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | emr/kos/mapper.py:125-133 · 168 |
| 26 | `data[].operationTimetable.saturday.breaktime` | object |  | 해당 없음 | 묶음 |
| 27 | `data[].operationTimetable.saturday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | emr/kos/mapper.py:180 |
| 28 | `data[].operationTimetable.saturday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | emr/kos/mapper.py:179 |
| 29 | `data[].operationTimetable.saturday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | emr/kos/mapper.py:174-176 |
| 30 | `data[].operationTimetable.saturday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | emr/kos/mapper.py:178 |
| 31 | `data[].operationTimetable.saturday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 |
| 32 | `data[].operationTimetable.sunday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | emr/kos/mapper.py:125-133 · 168 |
| 33 | `data[].operationTimetable.sunday.breaktime` | object |  | 해당 없음 | 묶음 |
| 34 | `data[].operationTimetable.sunday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | emr/kos/mapper.py:180 |
| 35 | `data[].operationTimetable.sunday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | emr/kos/mapper.py:179 |
| 36 | `data[].operationTimetable.sunday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | emr/kos/mapper.py:174-176 |
| 37 | `data[].operationTimetable.sunday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | emr/kos/mapper.py:178 |
| 38 | `data[].operationTimetable.sunday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 |
| 39 | `data[].operationTimetable.thursday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | emr/kos/mapper.py:125-133 · 168 |
| 40 | `data[].operationTimetable.thursday.breaktime` | object |  | 해당 없음 | 묶음 |
| 41 | `data[].operationTimetable.thursday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | emr/kos/mapper.py:180 |
| 42 | `data[].operationTimetable.thursday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | emr/kos/mapper.py:179 |
| 43 | `data[].operationTimetable.thursday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | emr/kos/mapper.py:174-176 |
| 44 | `data[].operationTimetable.thursday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | emr/kos/mapper.py:178 |
| 45 | `data[].operationTimetable.thursday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 |
| 46 | `data[].operationTimetable.tuesday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | emr/kos/mapper.py:125-133 · 168 |
| 47 | `data[].operationTimetable.tuesday.breaktime` | object |  | 해당 없음 | 묶음 |
| 48 | `data[].operationTimetable.tuesday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | emr/kos/mapper.py:180 |
| 49 | `data[].operationTimetable.tuesday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | emr/kos/mapper.py:179 |
| 50 | `data[].operationTimetable.tuesday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | emr/kos/mapper.py:174-176 |
| 51 | `data[].operationTimetable.tuesday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | emr/kos/mapper.py:178 |
| 52 | `data[].operationTimetable.tuesday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 |
| 53 | `data[].operationTimetable.wednesday` | object | reservation_group_timetable.weekday (models/room.py:85) | 저장됨 | emr/kos/mapper.py:125-133 · 168 |
| 54 | `data[].operationTimetable.wednesday.breaktime` | object |  | 해당 없음 | 묶음 |
| 55 | `data[].operationTimetable.wednesday.breaktime.endTime` | string(empty) | reservation_group_timetable.break_end (models/room.py:90) | 저장됨 | emr/kos/mapper.py:180 |
| 56 | `data[].operationTimetable.wednesday.breaktime.startTime` | string(empty) | reservation_group_timetable.break_start (models/room.py:89) | 저장됨 | emr/kos/mapper.py:179 |
| 57 | `data[].operationTimetable.wednesday.enabled` | bool | reservation_group_timetable.is_enabled (models/room.py:86) | 저장됨 | emr/kos/mapper.py:174-176 |
| 58 | `data[].operationTimetable.wednesday.endTime` | string(ISO UTC) | reservation_group_timetable.end_time (models/room.py:88) | 저장됨 | emr/kos/mapper.py:178 |
| 59 | `data[].operationTimetable.wednesday.startTime` | string(ISO UTC) | reservation_group_timetable.start_time (models/room.py:87) | 저장됨 | emr/kos/mapper.py:177 — 병원 현지 시계 시간으로 바꿔 저장 |
| 60 | `data[].order` | int | reservation_group.sort_order (models/room.py:60) | 저장됨 | emr/kos/mapper.py:205 |
| 61 | `data[].sameDayCloseBufferMinutes` | int | reservation_group.same_day_close_buffer_minutes (models/room.py:62) | 저장됨 | emr/kos/mapper.py:207 |
| 62 | `data[].startDate` | string(ISO UTC) |  | 칸 없음 | 그룹 시작일 |
| 63 | `data[].title` | string | reservation_group.title (models/room.py:59) | 저장됨 | emr/kos/mapper.py:204 |

### P04 `role/v2/queries/get-roles`

스크립트 합집합 키 **13** · 표 행 **13** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].featureList[]` | array / array(empty) / object |  | 일부러 안 둠 | S0:611 「KOS 화면 권한(featureList)은 쓰지 않는다」 |
| 3 | `data[].featureList[].domain` | string |  | 일부러 안 둠 | S0:611 「KOS 화면 권한(featureList)은 쓰지 않는다」 |
| 4 | `data[].featureList[].featureId` | string(empty) |  | 일부러 안 둠 | S0:611 「KOS 화면 권한(featureList)은 쓰지 않는다」 |
| 5 | `data[].featureList[].name` | string |  | 일부러 안 둠 | S0:611 「KOS 화면 권한(featureList)은 쓰지 않는다」 |
| 6 | `data[].featureList[].subFeatureList[]` | array / string |  | 일부러 안 둠 | S0:611 「KOS 화면 권한(featureList)은 쓰지 않는다」 |
| 7 | `data[].featureList[].subFeatures[]` | array / object |  | 일부러 안 둠 | S0:611 「KOS 화면 권한(featureList)은 쓰지 않는다」 |
| 8 | `data[].featureList[].subFeatures[].name` | string |  | 일부러 안 둠 | S0:611 「KOS 화면 권한(featureList)은 쓰지 않는다」 |
| 9 | `data[].featureList[].translsMap` | object(empty) |  | 일부러 안 둠 | S0:611 「KOS 화면 권한(featureList)은 쓰지 않는다」 |
| 10 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:224 |
| 11 | `data[].isDefault` | bool | job_role.is_default (models/staff.py:70) | 저장됨 | emr/kos/mapper.py:227 |
| 12 | `data[].name` | string | job_role.name (models/staff.py:68) | 저장됨 | emr/kos/mapper.py:225 |
| 13 | `data[].roleTags[]` | array / array(empty) / int | job_role.tags (models/staff.py:69) | 저장됨 | emr/kos/mapper.py:226 · 91-103 — 0 등 모르는 값은 뺀다 |

### P05 `account/v2/queries/get-accounts`

스크립트 합집합 키 **19** · 표 행 **19** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].activate` | bool | staff.is_active (models/staff.py:57) | 저장됨 | emr/kos/mapper.py:248 |
| 3 | `data[].createdAt` | string(ISO UTC) |  | 칸 없음 | KOS 계정 생성 시각 — S0 직원 표에 대응 없음 |
| 4 | `data[].defaultWorkingZoneId` | string | staff.default_zone_id (models/staff.py:56) | 칸 있음 · 미동기화 | S0:663 · 매퍼 없음(emr/kos/mapper.py:236-251) |
| 5 | `data[].email` | string(email꼴) | staff.email (models/staff.py:53) | 저장됨 | emr/kos/mapper.py:241 |
| 6 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:236 |
| 7 | `data[].licenseNumber` | string(digits) / string(empty) | staff.license_number (models/staff.py:54) | 저장됨 | emr/kos/mapper.py:242 |
| 8 | `data[].mfaMethods[]` | array(empty) |  | 칸 없음 | 2단계 인증 — 로그인 때만 봄(services/auth.py:523) |
| 9 | `data[].name` | string / string(email꼴) | staff.name (models/staff.py:51) | 저장됨 | emr/kos/mapper.py:239 |
| 10 | `data[].profileImageUrl` | string(url) |  | 칸 없음 |  |
| 11 | `data[].realName` | string / string(email꼴) / string(empty) | staff.real_name (models/staff.py:52) | 저장됨 | emr/kos/mapper.py:240 |
| 12 | `data[].role` | object | staff.job_role_id (models/staff.py:55) | 저장됨 | emr/kos/mapper.py:245-247 |
| 13 | `data[].role.id` | string | staff.job_role_id (models/staff.py:55) | 저장됨 | emr/kos/mapper.py:245-247 |
| 14 | `data[].role.name` | string | join job_role (models/staff.py:64-70) | 계산으로 대체 |  |
| 15 | `data[].role.roleTags[]` | array / array(empty) / int | join job_role (models/staff.py:64-70) | 계산으로 대체 |  |
| 16 | `data[].roleId` | string | staff.job_role_id (models/staff.py:55) | 저장됨 | emr/kos/mapper.py:245-247 |
| 17 | `data[].roleName` | string | join job_role (models/staff.py:64-70) | 계산으로 대체 |  |
| 18 | `data[].updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 칸 있음 · 미동기화 | 직원은 안 채움 |
| 19 | `data[].userId` | string | (staff.account_id 는 로그인 때 이음 — S0:647) | 칸 없음 | KOS 사용자 id |

### P06 `meta/codes/v1/queries/get-codes`

스크립트 합집합 키 **8** · 표 행 **8** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / array(empty) / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].category` | enum: CONSULTATION_RESULT\|FUNNEL\|IMAGE_CATEGORY\|IMAGE_EQUIPMENT\|VISITOR_CATEGORY | 어느 코드 표인지(요청 `category` 로 정함) | 계산으로 대체 | emr/kos/__init__.py:139 — DAY 는 VISITOR_CATEGORY · FUNNEL_CATEGORY · FUNNEL 만 부른다(K4) |
| 3 | `data[].closed` | bool | .is_closed (models/customer.py:131 · 141 · 152) | 저장됨 | emr/kos/mapper.py:263 |
| 4 | `data[].color` | string | customer_category.color (models/customer.py:129) | 저장됨 | emr/kos/mapper.py:264 |
| 5 | `data[].default` | bool | funnel.is_default (models/customer.py:153) | 저장됨 | emr/kos/mapper.py:265 |
| 6 | `data[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:260 |
| 7 | `data[].name` | string | customer_category · funnel_category · funnel .name (models/customer.py:128 · 139 · 150) | 저장됨 | emr/kos/mapper.py:261 |
| 8 | `data[].order` | int | .sort_order (models/customer.py:130 · 140 · 151) | 저장됨 | emr/kos/mapper.py:262 |

### P07 `schedule/v2/queries/get-schedules-grouped-by-zone`

스크립트 합집합 키 **230** · 표 행 **230** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 구역 묶음 껍데기(emr/kos/mapper.py:286-297) |
| 2 | `data[].schedules[]` | array / object | visit (models/visit.py:52) | 저장됨 | emr/kos/mapper.py:531 |
| 3 | `data[].schedules[].consultation` | object |  | 해당 없음 | 묶음 |
| 4 | `data[].schedules[].consultation.consultationMemo` | string / string(empty) | (consultation.consultation_note 는 consultations[].content.text) | 칸 없음(시점 다름) | 앞 판 M3 · C5 — 공개 쓰기 경로와 같은 칸 |
| 5 | `data[].schedules[].consultation.counselor` | object | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 6 | `data[].schedules[].consultation.counselor.id` | string / string(empty) | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 7 | `data[].schedules[].consultation.counselor.name` | string / string(empty) | (id 가 없으니 join 불가) | 칸 없음(시점 다름) | 이름 스냅샷 |
| 8 | `data[].schedules[].consultation.doctor` | object | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 9 | `data[].schedules[].consultation.doctor.id` | string / string(empty) | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 10 | `data[].schedules[].consultation.doctor.name` | string / string(empty) | (id 가 없으니 join 불가) | 칸 없음(시점 다름) | 이름 스냅샷 |
| 11 | `data[].schedules[].consultations[]` | array / array(empty) / object | consultation (models/visit.py:119) | 저장됨 | emr/kos/mapper.py:553 |
| 12 | `data[].schedules[].consultations[].consultationDoctors[]` | array / array(empty) / object | consultation.doctor_id (models/visit.py:133) | 저장됨 | emr/kos/mapper.py:506 — **1명일 때만**(emr/kos/mapper.py:491-494) |
| 13 | `data[].schedules[].consultations[].consultationDoctors[].id` | string | consultation.doctor_id (models/visit.py:133) | 저장됨 | emr/kos/mapper.py:506 — **1명일 때만**(emr/kos/mapper.py:491-494) |
| 14 | `data[].schedules[].consultations[].consultationDoctors[].name` | string | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 15 | `data[].schedules[].consultations[].consultationProcedures[]` | array(empty) | consultation_procedure (models/visit.py:140) | 칸 있음 · 미동기화 | emr/kos/mapper.py:500 「안쪽 키 미관찰이라 받지 않는다」 · HAR 에서 늘 빈 배열 |
| 16 | `data[].schedules[].consultations[].consultationStartedDateTimeUtc` | string(ISO UTC) | consultation.started_at (models/visit.py:131) | 저장됨 | emr/kos/mapper.py:504 |
| 17 | `data[].schedules[].consultations[].content` | object |  | 해당 없음 | 묶음 |
| 18 | `data[].schedules[].consultations[].content.text` | string | consultation.consultation_note (models/visit.py:134) | 저장됨 | emr/kos/mapper.py:507 |
| 19 | `data[].schedules[].consultations[].counselors[]` | array / object | consultation.counselor_id (models/visit.py:132) | 저장됨 | emr/kos/mapper.py:505 — **1명일 때만**(둘 이상이면 비움 · emr/kos/mapper.py:491-494 · OQ-13) |
| 20 | `data[].schedules[].consultations[].counselors[].id` | string | consultation.counselor_id (models/visit.py:132) | 저장됨 | emr/kos/mapper.py:505 — **1명일 때만**(둘 이상이면 비움 · emr/kos/mapper.py:491-494 · OQ-13) |
| 21 | `data[].schedules[].consultations[].counselors[].name` | string | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 22 | `data[].schedules[].consultations[].createdDateTimeUtc` | string(ISO UTC) | consultation.created_at (S0:537 「created_at ← createdDateTimeUtc」) | 칸 있음 · 미동기화 | 매퍼 없음 — DAY created_at 은 DAY 행 생성 시각 |
| 23 | `data[].schedules[].consultations[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:503 |
| 24 | `data[].schedules[].consultations[].scheduleId` | string(uuid) | consultation.visit_id (models/visit.py:130) | 저장됨 | 부모 일정 |
| 25 | `data[].schedules[].consultations[].updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 칸 있음 · 미동기화 | 매퍼 없음(상담 기록은 external_updated_at 안 채움) |
| 26 | `data[].schedules[].consultations[].visitor` | object | visit.customer_id (models/visit.py:67) | 계산으로 대체 | 같은 일정의 고객 |
| 27 | `data[].schedules[].consultations[].visitor.id` | string | visit.customer_id (models/visit.py:67) | 계산으로 대체 | 같은 일정의 고객 |
| 28 | `data[].schedules[].consultations[].visitor.isNew` | bool | (visit.is_new 와 같은 값인지 확인 안 됨) | 확인 안 됨 |  |
| 29 | `data[].schedules[].consultations[].visitor.name` | string | join customer.name | 계산으로 대체 |  |
| 30 | `data[].schedules[].createdDateTimeUtc` | string(ISO UTC) | visit.booked_at (models/visit.py:68) | 저장됨 | emr/kos/mapper.py:559 |
| 31 | `data[].schedules[].deleted` | bool | visit.deleted_at (S0:477) | 저장됨 | emr/kos/mapper.py:557 · emr/sync_schedules.py:314 |
| 32 | `data[].schedules[].etceteraWorks[]` | array / array(empty) / object |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 33 | `data[].schedules[].etceteraWorks[].assignees[]` | array(empty) |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 34 | `data[].schedules[].etceteraWorks[].etceteraWorkConfiguration` | object |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 35 | `data[].schedules[].etceteraWorks[].etceteraWorkConfiguration.id` | string |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 36 | `data[].schedules[].etceteraWorks[].etceteraWorkConfiguration.title` | string |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 37 | `data[].schedules[].etceteraWorks[].etceteraWorkConfiguration.translsMap` | object |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 38 | `data[].schedules[].etceteraWorks[].etceteraWorkConfiguration.translsMap.title` | object |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 39 | `data[].schedules[].etceteraWorks[].etceteraWorkConfiguration.translsMap.title.translation` | object(empty) |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 40 | `data[].schedules[].etceteraWorks[].memo` | string(empty) |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 41 | `data[].schedules[].etceteraWorks[].sequence` | int |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 42 | `data[].schedules[].etceteraWorks[].status` | enum: WAITING |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 43 | `data[].schedules[].flowStep` | enum: CONSULTATION\|CONSULTATION_WAITING\|PROCEDURE\|PROCEDURE_DONE\|PROCEDURE_WAITING\|RECEPTION\|RESERVED | visit.flow_step (models/visit.py:86) | 저장됨 | emr/kos/mapper.py:588-590 |
| 44 | `data[].schedules[].flowStepUpdatedDateTimeUtc` | string(ISO UTC) / string(empty) | visit.flow_step_at (models/visit.py:87) | 저장됨 | emr/kos/mapper.py:591 |
| 45 | `data[].schedules[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:555 |
| 46 | `data[].schedules[].occupiedResources[]` | array / object | visit_occupied_resource (models/room.py:96) | 저장됨 | emr/kos/mapper.py:542 |
| 47 | `data[].schedules[].occupiedResources[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:368 |
| 48 | `data[].schedules[].occupiedResources[].reservationGroup` | object |  | 해당 없음 | 묶음 |
| 49 | `data[].schedules[].occupiedResources[].reservationGroup.doctors[]` | array(empty) | visit_occupied_resource_doctor (models/room.py:108) | 저장됨 | emr/kos/mapper.py:380-384 |
| 50 | `data[].schedules[].occupiedResources[].reservationGroup.reservationGroupId` | string | visit_occupied_resource.reservation_group_id (models/room.py:101) | 저장됨 | emr/kos/mapper.py:372 |
| 51 | `data[].schedules[].occupiedResources[].reservationGroup.zoneId` | string | visit_occupied_resource.zone_id (models/room.py:102) | 저장됨 | emr/kos/mapper.py:375 |
| 52 | `data[].schedules[].occupiedResources[].reservationTime` | object |  | 해당 없음 | 묶음 |
| 53 | `data[].schedules[].occupiedResources[].reservationTime.endDateTimeUtc` | string(ISO UTC) | visit_occupied_resource.end_at (models/room.py:104) | 저장됨 | emr/kos/mapper.py:379 |
| 54 | `data[].schedules[].occupiedResources[].reservationTime.startDateTimeUtc` | string(ISO UTC) | visit_occupied_resource.start_at (models/room.py:103) | 저장됨 | emr/kos/mapper.py:378 |
| 55 | `data[].schedules[].occupiedResources[].type` | enum: RESERVATION_GROUP | visit_occupied_resource.type (models/room.py:100) | 저장됨 | emr/kos/mapper.py:371 |
| 56 | `data[].schedules[].orderMemo` | string / string(empty) | visit.procedure_order_note (models/visit.py:92) | 저장됨 | emr/kos/mapper.py:598 |
| 57 | `data[].schedules[].prescriptionIds[]` | array(empty) | prescription.visit_id (models/prescription.py:20) | 저장됨 | emr/kos/mapper_purchase.py:104 · S0:501 |
| 58 | `data[].schedules[].purchaseIds[]` | array / array(empty) / string(uuid) | purchase.visit_id (models/purchase.py:58) | 저장됨 | emr/kos/mapper_purchase.py:103 · S0:500 |
| 59 | `data[].schedules[].purchases[]` | array(empty) | purchase.visit_id (models/purchase.py:58) | 계산으로 대체 | S0:500 — purchaseIds[] 로 받는다 · HAR 에서 늘 빈 배열(안쪽 키 확인 안 됨) |
| 60 | `data[].schedules[].reactions[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 · S0 OQ-03-1(:1789) 열림 |
| 61 | `data[].schedules[].receptionDateTimeUtc` | string(ISO UTC) / string(empty) | visit.reception_at (models/visit.py:88) | 저장됨 | emr/kos/mapper.py:592 |
| 62 | `data[].schedules[].reservation` | object |  | 해당 없음 | 묶음 |
| 63 | `data[].schedules[].reservation.connectedChannel` | string | visit.connected_channel (models/visit.py:81) | 저장됨 | emr/kos/mapper.py:580 — `Channel_UNSPEICIFED` 는 None(emr/kos/mapper.py:113-118) |
| 64 | `data[].schedules[].reservation.consultationRequired` | bool | visit.consultation_required (models/visit.py:82) | 저장됨 | emr/kos/mapper.py:581 |
| 65 | `data[].schedules[].reservation.counselor` | object | visit.requested_counselor_id (models/visit.py:77) | 저장됨 | emr/kos/mapper.py:572-574 — 예약 지정 희망 상담사(앞 판 M1) |
| 66 | `data[].schedules[].reservation.counselor.id` | string / string(empty) | visit.requested_counselor_id (models/visit.py:77) | 저장됨 | emr/kos/mapper.py:572-574 — 예약 지정 희망 상담사(앞 판 M1) |
| 67 | `data[].schedules[].reservation.counselor.name` | string / string(empty) | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 68 | `data[].schedules[].reservation.doctor` | object | visit.requested_doctor_id (models/visit.py:78) | 저장됨 | emr/kos/mapper.py:575-577 |
| 69 | `data[].schedules[].reservation.doctor.id` | string(empty) | visit.requested_doctor_id (models/visit.py:78) | 저장됨 | emr/kos/mapper.py:575-577 |
| 70 | `data[].schedules[].reservation.doctor.name` | string(empty) | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 71 | `data[].schedules[].reservation.endDateTime` | string(ISO UTC) | visit.reserved_end_at (models/visit.py:71) | 저장됨 | emr/kos/mapper.py:563 |
| 72 | `data[].schedules[].reservation.funnel` | object |  | 해당 없음 | 묶음 |
| 73 | `data[].schedules[].reservation.funnel.funnel` | object | visit.funnel_id (models/visit.py:79) | 저장됨 | emr/kos/mapper.py:578 |
| 74 | `data[].schedules[].reservation.funnel.funnel.category` | enum: FUNNEL | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 75 | `data[].schedules[].reservation.funnel.funnel.closed` | bool | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 76 | `data[].schedules[].reservation.funnel.funnel.default` | bool | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 77 | `data[].schedules[].reservation.funnel.funnel.id` | string(uuid) | visit.funnel_id (models/visit.py:79) | 저장됨 | emr/kos/mapper.py:578 |
| 78 | `data[].schedules[].reservation.funnel.funnel.name` | string | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 79 | `data[].schedules[].reservation.funnel.funnel.order` | int | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 80 | `data[].schedules[].reservation.funnel.funnelDetail` | string(empty) | visit.funnel_detail (models/visit.py:80) | 저장됨 | emr/kos/mapper.py:579 |
| 81 | `data[].schedules[].reservation.requestedProcedures[]` | array(empty) | visit_requested_procedure (models/visit.py:100) · sort_order = 배열 순서(models/visit.py:113) | 저장됨 | emr/kos/mapper.py:536-541 — P07 · P08 · P33 HAR 에서 늘 빈 배열 — 안쪽 키는 HAR 에만 있는 `schedule/v1/queries/get-schedule-summaries` 응답에서만 보인다(K5) |
| 82 | `data[].schedules[].reservation.reservationAssignee` | object | visit.reservation_assignee_id (models/visit.py:76) | 저장됨 | emr/kos/mapper.py:569-571 |
| 83 | `data[].schedules[].reservation.reservationAssignee.id` | string | visit.reservation_assignee_id (models/visit.py:76) | 저장됨 | emr/kos/mapper.py:569-571 |
| 84 | `data[].schedules[].reservation.reservationAssignee.name` | string / string(email꼴) | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 85 | `data[].schedules[].reservation.reservationGroupId` | string | (visit_occupied_resource 쪽 칸은 있음 — 같은 값인지 확인 안 됨) | 칸 없음 | S0:598 「visit 에 두지 않고 visit_occupied_resource 로」는 그룹 칸 얘기 — 이 키 자체의 결정은 없음 |
| 86 | `data[].schedules[].reservation.reservationMemo` | string / string(empty) | visit.reservation_notes (models/visit.py:75) | 저장됨 | emr/kos/mapper.py:568 |
| 87 | `data[].schedules[].reservation.sedationRequired` | bool | visit.sedation_required (models/visit.py:83) | 저장됨 | emr/kos/mapper.py:584 |
| 88 | `data[].schedules[].reservation.startDateTime` | string(ISO UTC) | visit.reserved_start_at (models/visit.py:70) | 저장됨 | emr/kos/mapper.py:560 |
| 89 | `data[].schedules[].reservation.status` | enum: CANCELED\|IN_PROGRESS\|RESERVED | visit.reservation_status (models/visit.py:72) | 저장됨 | emr/kos/mapper.py:564-567 |
| 90 | `data[].schedules[].reservation.zoneId` | string | (visit_occupied_resource 쪽 칸은 있음 — 같은 값인지 확인 안 됨) | 칸 없음 | S0:598 「visit 에 두지 않고 visit_occupied_resource 로」는 그룹 칸 얘기 — 이 키 자체의 결정은 없음 |
| 91 | `data[].schedules[].taskTimers[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 · S0 OQ-05-1(:1850) 열림 |
| 92 | `data[].schedules[].tasks[]` | array / array(empty) / object | visit_task (models/task.py:68) | 저장됨 | emr/kos/mapper.py:545-552 |
| 93 | `data[].schedules[].tasks[].anesthesiaType` | enum: ANESTHESIA_TYPE_UNSPECIFIED | visit_task.anesthesia_type (models/task.py:102) | 저장됨 | emr/kos/mapper.py:472 |
| 94 | `data[].schedules[].tasks[].assigneeMemo` | string(empty) | visit_task.assignee_note (models/task.py:104) | 저장됨 | emr/kos/mapper.py:474 |
| 95 | `data[].schedules[].tasks[].assignees[]` | array / array(empty) / object | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 96 | `data[].schedules[].tasks[].assignees[].id` | string | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 97 | `data[].schedules[].tasks[].assignees[].name` | string(email꼴) | join staff.name | 계산으로 대체 |  |
| 98 | `data[].schedules[].tasks[].calledDoctors[]` | array(empty) | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 99 | `data[].schedules[].tasks[].completedDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.completed_at (models/task.py:114) | 저장됨 | emr/kos/mapper.py:481 |
| 100 | `data[].schedules[].tasks[].doctorAssignedDateTimeUtc` | string(ISO UTC) | visit_task.doctor_assigned_at (models/task.py:110) | 저장됨 | emr/kos/mapper.py:480 |
| 101 | `data[].schedules[].tasks[].doctorCallDateTime` | string(ISO UTC) / string(empty) | visit_task.doctor_called_at (models/task.py:109) | 저장됨 | emr/kos/mapper.py:479 |
| 102 | `data[].schedules[].tasks[].doctorMemo` | string(empty) | visit_task.doctor_note (models/task.py:105) | 저장됨 | emr/kos/mapper.py:475 |
| 103 | `data[].schedules[].tasks[].doctors[]` | array / array(empty) / object | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 104 | `data[].schedules[].tasks[].doctors[].id` | string | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 105 | `data[].schedules[].tasks[].doctors[].name` | string | join staff.name | 계산으로 대체 |  |
| 106 | `data[].schedules[].tasks[].etceteraConfiguration` | object |  | 해당 없음 | 묶음 |
| 107 | `data[].schedules[].tasks[].etceteraConfiguration.etceteraTaskId` | string / string(empty) | (etc_task_type 표는 있으나 작업 → 종류 FK 없음) | 칸 없음 | emr/kos/mapper.py:485-487 → `is_room_assign`(models/task.py:91) 판정에만 씀(emr/sync_tasks.py:132) |
| 108 | `data[].schedules[].tasks[].etceteraConfiguration.name` | string / string(empty) | visit_task.etc_task_title (models/task.py:88) | 저장됨 | emr/kos/mapper.py:469 |
| 109 | `data[].schedules[].tasks[].etceteraConfiguration.translsMap` | object / object(empty) |  | 칸 없음 |  |
| 110 | `data[].schedules[].tasks[].etceteraConfiguration.translsMap.name` | object |  | 칸 없음 |  |
| 111 | `data[].schedules[].tasks[].etceteraConfiguration.translsMap.name.translation` | object(empty) |  | 칸 없음 |  |
| 112 | `data[].schedules[].tasks[].memo` | string(empty) | visit_task.procedure_note (models/task.py:103) | 저장됨 | emr/kos/mapper.py:473 |
| 113 | `data[].schedules[].tasks[].order` | int | visit_task.sort_order (models/task.py:75) | 저장됨 | emr/kos/mapper.py:456 |
| 114 | `data[].schedules[].tasks[].paymentRequired` | bool | visit_task.payment_required (models/task.py:101) | 저장됨 | emr/kos/mapper.py:471 |
| 115 | `data[].schedules[].tasks[].procedureConfiguration` | object / object(empty) |  | 해당 없음 | 묶음 |
| 116 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration` | object |  | 해당 없음 | 묶음 |
| 117 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.caution` | string(empty) | (treatment_item.code · caution = 지금 메뉴 값 models/menu.py:173 · 176) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 118 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.code` | string | (treatment_item.code · caution = 지금 메뉴 값 models/menu.py:173 · 176) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 119 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.id` | string | visit_task.treatment_item_id (models/task.py:98) | 저장됨 | emr/kos/mapper_purchase.py:88 |
| 120 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.machines[]` | array / array(empty) / object | visit_task.machines (models/task.py:96) | 저장됨 | emr/kos/mapper_purchase.py:89 — 이름 스냅샷 |
| 121 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.machines[].id` | string | (이름 스냅샷만 — id 없음) | 칸 없음 |  |
| 122 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.machines[].name` | string | visit_task.machines (models/task.py:96) | 저장됨 | emr/kos/mapper_purchase.py:89 — 이름 스냅샷 |
| 123 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.machines[].searchPhoneticName` | string | (machine · medicine.search_phonetic_name = 지금 값) | 칸 없음(시점 다름) |  |
| 124 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[]` | array / array(empty) / object | visit_task.medicines (models/task.py:94) | 저장됨 | emr/kos/mapper.py:449 · 470 — 이름 스냅샷 |
| 125 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].id` | string | (이름 스냅샷만 — id 없음) | 칸 없음 |  |
| 126 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].name` | string | visit_task.medicines (models/task.py:94) | 저장됨 | emr/kos/mapper.py:449 · 470 — 이름 스냅샷 |
| 127 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].searchPhoneticName` | string | (machine · medicine.search_phonetic_name = 지금 값) | 칸 없음(시점 다름) |  |
| 128 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.title` | string | visit_task.medical_service_title (models/task.py:80) | 저장됨 | emr/kos/mapper.py:462 |
| 129 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap` | object |  | 칸 없음 |  |
| 130 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title` | object |  | 칸 없음 |  |
| 131 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation` | object |  | 칸 없음 |  |
| 132 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.en` | string |  | 칸 없음 |  |
| 133 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.ja` | string |  | 칸 없음 |  |
| 134 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.ko` | string |  | 칸 없음 |  |
| 135 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.zh-Hans` | string |  | 칸 없음 |  |
| 136 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.zh-Hant` | string |  | 칸 없음 |  |
| 137 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.unit` | object | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) |
| 138 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.unit.type` | enum: SHOT\|UNIT | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) |
| 139 | `data[].schedules[].tasks[].procedureConfiguration.medicalServiceConfiguration.unit.value` | number | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) |
| 140 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration` | object |  | 해당 없음 | 묶음 |
| 141 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.medicineAndMachines[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 142 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.optionId` | string |  | 일부러 안 둠 | S0:892 「상품 옵션 id 는 ERD v1 이 작업에 두지 않음」 |
| 143 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.optionTitle` | string | visit_task.option_title (models/task.py:79) | 저장됨 | emr/kos/mapper.py:461 |
| 144 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.procedure` | object | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 145 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 「시술 카테고리 칸으로 두지 않는다」 |
| 146 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.createDate` | string(empty) | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 147 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.id` | string | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 148 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.name` | string | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 149 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.productTitle` | string | (product.title 은 지금 메뉴 값 · 작업 → 옵션 참조 없음) | 칸 없음(시점 다름) | data_rules 「메뉴 참조 = id + 그때 값 스냅샷」 |
| 150 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap` | object |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 151 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle` | object |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 152 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation` | object / object(empty) |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 153 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.en` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 154 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.ja` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 155 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.ko` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 156 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.zh-Hans` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 157 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.zh-Hant` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 158 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle` | object |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 159 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation` | object / object(empty) |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 160 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.en` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 161 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.ja` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 162 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.ko` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 163 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.zh-Hans` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 164 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.zh-Hant` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 165 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.unit` | object |  | 해당 없음 | 묶음 |
| 166 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.unit.type` | enum: SHOT\|UNIT\|UnitType_UNKNOWN | visit_task.unit_type · unit_value (models/task.py:82 · 85) | 저장됨 | emr/kos/mapper.py:447-466 — `UnitType_UNKNOWN` 은 None |
| 167 | `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.unit.value` | number | visit_task.unit_type · unit_value (models/task.py:82 · 85) | 저장됨 | emr/kos/mapper.py:447-466 — `UnitType_UNKNOWN` 은 None |
| 168 | `data[].schedules[].tasks[].procedureConfiguration.ticketConfiguration` | object(empty) |  | 해당 없음 | 묶음(시술권이 아니면 빈 객체) |
| 169 | `data[].schedules[].tasks[].readyDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.ready_at (models/task.py:108) | 저장됨 | emr/kos/mapper.py:478 |
| 170 | `data[].schedules[].tasks[].room` | object | visit_task.room_id (models/task.py:106) | 저장됨 | emr/kos/mapper.py:450-452 · 카드 방 visit.room_id(models/visit.py:93) emr/kos/mapper.py:388-408 |
| 171 | `data[].schedules[].tasks[].room.id` | string / string(empty) | visit_task.room_id (models/task.py:106) | 저장됨 | emr/kos/mapper.py:450-452 · 카드 방 visit.room_id(models/visit.py:93) emr/kos/mapper.py:388-408 |
| 172 | `data[].schedules[].tasks[].room.order` | int | join room (models/room.py:43-49) | 계산으로 대체 |  |
| 173 | `data[].schedules[].tasks[].room.title` | string / string(empty) | join room (models/room.py:43-49) | 계산으로 대체 |  |
| 174 | `data[].schedules[].tasks[].room.zoneId` | string / string(empty) | join room (models/room.py:43-49) | 계산으로 대체 |  |
| 175 | `data[].schedules[].tasks[].roomAssignedDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.room_assigned_at (models/task.py:107) | 저장됨 | emr/kos/mapper.py:477 |
| 176 | `data[].schedules[].tasks[].sequence` | int | visit_task.sequence (models/task.py:74) | 저장됨 | emr/kos/mapper.py:454 |
| 177 | `data[].schedules[].tasks[].status` | enum: DONE\|NOT_STARTED\|READY | visit_task.status (models/task.py:76) | 저장됨 | emr/kos/mapper.py:457-459 |
| 178 | `data[].schedules[].tasks[].title` | string | visit_task.title (models/task.py:78) | 저장됨 | emr/kos/mapper.py:460 |
| 179 | `data[].schedules[].tasks[].translsMap` | object |  | 칸 없음 | 작업 이름 번역 |
| 180 | `data[].schedules[].tasks[].translsMap.title` | object |  | 칸 없음 | 작업 이름 번역 |
| 181 | `data[].schedules[].tasks[].translsMap.title.translation` | object / object(empty) |  | 칸 없음 | 작업 이름 번역 |
| 182 | `data[].schedules[].tasks[].translsMap.title.translation.de` | string |  | 칸 없음 | 작업 이름 번역 |
| 183 | `data[].schedules[].tasks[].translsMap.title.translation.en` | string |  | 칸 없음 | 작업 이름 번역 |
| 184 | `data[].schedules[].tasks[].translsMap.title.translation.es` | string |  | 칸 없음 | 작업 이름 번역 |
| 185 | `data[].schedules[].tasks[].translsMap.title.translation.fr` | string |  | 칸 없음 | 작업 이름 번역 |
| 186 | `data[].schedules[].tasks[].translsMap.title.translation.id` | string |  | 칸 없음 | 작업 이름 번역 |
| 187 | `data[].schedules[].tasks[].translsMap.title.translation.ja` | string |  | 칸 없음 | 작업 이름 번역 |
| 188 | `data[].schedules[].tasks[].translsMap.title.translation.mn` | string |  | 칸 없음 | 작업 이름 번역 |
| 189 | `data[].schedules[].tasks[].translsMap.title.translation.ms` | string |  | 칸 없음 | 작업 이름 번역 |
| 190 | `data[].schedules[].tasks[].translsMap.title.translation.nl` | string |  | 칸 없음 | 작업 이름 번역 |
| 191 | `data[].schedules[].tasks[].translsMap.title.translation.pt` | string |  | 칸 없음 | 작업 이름 번역 |
| 192 | `data[].schedules[].tasks[].translsMap.title.translation.ru` | string |  | 칸 없음 | 작업 이름 번역 |
| 193 | `data[].schedules[].tasks[].translsMap.title.translation.th` | string |  | 칸 없음 | 작업 이름 번역 |
| 194 | `data[].schedules[].tasks[].translsMap.title.translation.uz` | string |  | 칸 없음 | 작업 이름 번역 |
| 195 | `data[].schedules[].tasks[].translsMap.title.translation.vi` | string |  | 칸 없음 | 작업 이름 번역 |
| 196 | `data[].schedules[].tasks[].translsMap.title.translation.zh-Hans` | string |  | 칸 없음 | 작업 이름 번역 |
| 197 | `data[].schedules[].tasks[].translsMap.title.translation.zh-Hant` | string |  | 칸 없음 | 작업 이름 번역 |
| 198 | `data[].schedules[].tasks[].type` | enum: ETCETERA\|PROCEDURE | visit_task.kind (models/task.py:73) | 저장됨 | emr/kos/mapper.py:455 |
| 199 | `data[].schedules[].tasks[].urgencyLevel` | enum: URGENCY_LEVEL_UNSPECIFIED |  | 칸 없음 | 긴급도 |
| 200 | `data[].schedules[].updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 저장됨 | emr/kos/mapper.py:556 · emr/sync_schedules.py:271 |
| 201 | `data[].schedules[].visitor` | object | customer (models/customer.py:33) | 저장됨 | emr/kos/mapper.py:558 |
| 202 | `data[].schedules[].visitor.categories[]` | array / array(empty) / object | customer_category_link (models/customer.py:157) | 저장됨 | emr/kos/mapper.py:322-327 |
| 203 | `data[].schedules[].visitor.categories[].color` | string | join customer_category (models/customer.py:124-131) | 계산으로 대체 | get-codes VISITOR_CATEGORY 로 채움 |
| 204 | `data[].schedules[].visitor.categories[].id` | string(uuid) | customer_category_link (models/customer.py:157) | 저장됨 | emr/kos/mapper.py:322-327 |
| 205 | `data[].schedules[].visitor.categories[].name` | string | join customer_category (models/customer.py:124-131) | 계산으로 대체 | get-codes VISITOR_CATEGORY 로 채움 |
| 206 | `data[].schedules[].visitor.categories[].order` | int | join customer_category (models/customer.py:124-131) | 계산으로 대체 | get-codes VISITOR_CATEGORY 로 채움 |
| 207 | `data[].schedules[].visitor.chartNumber` | string(digits) | customer.chart_number (models/customer.py:43) + external_ref.external_number (models/customer.py:107) | 저장됨 | emr/kos/mapper.py:308 · emr/sync_schedules.py:150 |
| 208 | `data[].schedules[].visitor.dateOfBirth` | string / string(empty) | customer.birth_date (models/customer.py:52) | 저장됨 | emr/kos/mapper.py:312 |
| 209 | `data[].schedules[].visitor.gender` | enum: FEMALE\|GENDER_UNSPECIFIED\|MALE | customer.gender (models/customer.py:51) | 저장됨 | emr/kos/mapper.py:311 — `GENDER_UNSPECIFIED` 는 None |
| 210 | `data[].schedules[].visitor.id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:307 |
| 211 | `data[].schedules[].visitor.isNew` | bool | visit.is_new (models/visit.py:91) | 저장됨 | emr/kos/mapper.py:597 — 방문마다 값(S0:301 · 360) |
| 212 | `data[].schedules[].visitor.memo` | string / string(empty) | customer.customer_notes (models/customer.py:72) | 저장됨 | emr/kos/mapper.py:316 |
| 213 | `data[].schedules[].visitor.name` | string | customer.name (models/customer.py:46) | 저장됨 | emr/kos/mapper.py:309 |
| 214 | `data[].schedules[].visitor.nationality` | string | customer.nationality (models/customer.py:53) | 저장됨 | emr/kos/mapper.py:313 |
| 215 | `data[].schedules[].visitor.phone` | object |  | 해당 없음 | 묶음 |
| 216 | `data[].schedules[].visitor.phone.countryCode` | string(digits) | customer.phone_country_code (models/customer.py:61) | 저장됨 | emr/kos/mapper.py:314 |
| 217 | `data[].schedules[].visitor.phone.phoneNumber` | string(digits) | customer.phone_number (models/customer.py:62) | 저장됨 | emr/kos/mapper.py:315 |
| 218 | `data[].schedules[].visitor.phoneticName` | string / string(empty) | customer.name_pronunciation (models/customer.py:47) | 저장됨 | emr/kos/mapper.py:310 |
| 219 | `data[].schedules[].visitor.snsInfo` | object |  | 해당 없음 | 묶음 |
| 220 | `data[].schedules[].visitor.snsInfo.accountId` | string / string(email꼴) / string(empty) | customer.sns_account_id (models/customer.py:70) | 저장됨 | emr/kos/mapper.py:318 |
| 221 | `data[].schedules[].visitor.snsInfo.snsType` | string | customer.sns_type (models/customer.py:69) | 저장됨 | emr/kos/mapper.py:317 |
| 222 | `data[].schedules[].visitor.visitorType` | object | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 |
| 223 | `data[].schedules[].visitor.visitorType.id` | string / string(empty) | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 |
| 224 | `data[].schedules[].visitor.visitorType.name` | string / string(empty) | customer_type.name (models/customer.py:120) | 저장됨 | emr/kos/mapper.py:319-321 |
| 225 | `data[].schedules[].visitorLocation` | object |  | 해당 없음 | 묶음 |
| 226 | `data[].schedules[].visitorLocation.zoneId` | string | visit.current_zone_id (models/visit.py:90) | 저장됨 | emr/kos/mapper.py:594-596 |
| 227 | `data[].schedules[].zone` | object |  | 해당 없음 | 묶음 |
| 228 | `data[].schedules[].zone.id` | string | visit.reception_zone_id (models/visit.py:89) | 저장됨 | emr/kos/mapper.py:593 |
| 229 | `data[].schedules[].zone.title` | string | join zone.title (models/room.py:35) | 계산으로 대체 | 구역 이름 — 기준 정보 1시간 |
| 230 | `data[].zoneId` | string |  | 해당 없음 | 구역 묶음 키 — 일정 안 `zone` · `visitorLocation` 으로 받음 |

### P08 `schedule/v1/queries/get-schedule-detail`

스크립트 합집합 키 **242** · 표 행 **242** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data` | object | visit_task 만 씀 | 저장됨 | emr/kos/mapper.py:511-528 — DAY 는 이 응답의 `tasks` 만 읽는다(__init__.py:214) · 나머지 키 판정은 같은 칸을 일정 목록 동기화가 채우는지 기준 |
| 2 | `data.consultation` | object |  | 해당 없음 | 묶음 |
| 3 | `data.consultation.consultationMemo` | string / string(empty) | (consultation.consultation_note 는 consultations[].content.text) | 칸 없음(시점 다름) | 앞 판 M3 · C5 — 공개 쓰기 경로와 같은 칸 |
| 4 | `data.consultation.counselor` | object | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 5 | `data.consultation.counselor.id` | string / string(empty) | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 6 | `data.consultation.counselor.name` | string / string(empty) | (id 가 없으니 join 불가) | 칸 없음(시점 다름) | 이름 스냅샷 |
| 7 | `data.consultation.doctor` | object | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 8 | `data.consultation.doctor.id` | string / string(empty) | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 9 | `data.consultation.doctor.name` | string / string(empty) | (id 가 없으니 join 불가) | 칸 없음(시점 다름) | 이름 스냅샷 |
| 10 | `data.consultations[]` | array / array(empty) / object | consultation (models/visit.py:119) | 저장됨 | emr/kos/mapper.py:553 |
| 11 | `data.consultations[].consultationDoctors[]` | array / object | consultation.doctor_id (models/visit.py:133) | 저장됨 | emr/kos/mapper.py:506 — **1명일 때만**(emr/kos/mapper.py:491-494) |
| 12 | `data.consultations[].consultationDoctors[].id` | string | consultation.doctor_id (models/visit.py:133) | 저장됨 | emr/kos/mapper.py:506 — **1명일 때만**(emr/kos/mapper.py:491-494) |
| 13 | `data.consultations[].consultationDoctors[].name` | string | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 14 | `data.consultations[].consultationProcedures[]` | array(empty) | consultation_procedure (models/visit.py:140) | 칸 있음 · 미동기화 | emr/kos/mapper.py:500 「안쪽 키 미관찰이라 받지 않는다」 · HAR 에서 늘 빈 배열 |
| 15 | `data.consultations[].consultationStartedDateTimeUtc` | string(ISO UTC) | consultation.started_at (models/visit.py:131) | 저장됨 | emr/kos/mapper.py:504 |
| 16 | `data.consultations[].content` | object |  | 해당 없음 | 묶음 |
| 17 | `data.consultations[].content.text` | string | consultation.consultation_note (models/visit.py:134) | 저장됨 | emr/kos/mapper.py:507 |
| 18 | `data.consultations[].counselors[]` | array / array(empty) / object | consultation.counselor_id (models/visit.py:132) | 저장됨 | emr/kos/mapper.py:505 — **1명일 때만**(둘 이상이면 비움 · emr/kos/mapper.py:491-494 · OQ-13) |
| 19 | `data.consultations[].counselors[].id` | string | consultation.counselor_id (models/visit.py:132) | 저장됨 | emr/kos/mapper.py:505 — **1명일 때만**(둘 이상이면 비움 · emr/kos/mapper.py:491-494 · OQ-13) |
| 20 | `data.consultations[].counselors[].name` | string | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 21 | `data.consultations[].createdDateTimeUtc` | string(ISO UTC) | consultation.created_at (S0:537 「created_at ← createdDateTimeUtc」) | 칸 있음 · 미동기화 | 매퍼 없음 — DAY created_at 은 DAY 행 생성 시각 |
| 22 | `data.consultations[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:503 |
| 23 | `data.consultations[].scheduleId` | string(uuid) | consultation.visit_id (models/visit.py:130) | 저장됨 | 부모 일정 |
| 24 | `data.consultations[].updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 칸 있음 · 미동기화 | 매퍼 없음(상담 기록은 external_updated_at 안 채움) |
| 25 | `data.consultations[].visitor` | object | visit.customer_id (models/visit.py:67) | 계산으로 대체 | 같은 일정의 고객 |
| 26 | `data.consultations[].visitor.id` | string | visit.customer_id (models/visit.py:67) | 계산으로 대체 | 같은 일정의 고객 |
| 27 | `data.consultations[].visitor.isNew` | bool | (visit.is_new 와 같은 값인지 확인 안 됨) | 확인 안 됨 |  |
| 28 | `data.consultations[].visitor.name` | string | join customer.name | 계산으로 대체 |  |
| 29 | `data.createdDateTimeUtc` | string(ISO UTC) | visit.booked_at (models/visit.py:68) | 저장됨 | emr/kos/mapper.py:559 |
| 30 | `data.deleted` | bool | visit.deleted_at (S0:477) | 저장됨 | emr/kos/mapper.py:557 · emr/sync_schedules.py:314 |
| 31 | `data.etceteraWorks[]` | array / array(empty) / object |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 32 | `data.etceteraWorks[].assignees[]` | array / object |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 33 | `data.etceteraWorks[].assignees[].id` | string |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 34 | `data.etceteraWorks[].assignees[].name` | string |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 35 | `data.etceteraWorks[].assignees[].role` | object |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 36 | `data.etceteraWorks[].assignees[].role.id` | string |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 37 | `data.etceteraWorks[].assignees[].role.name` | string |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 38 | `data.etceteraWorks[].assignees[].role.roleTags[]` | array / string |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 39 | `data.etceteraWorks[].etceteraWorkConfiguration` | object |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 40 | `data.etceteraWorks[].etceteraWorkConfiguration.id` | string |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 41 | `data.etceteraWorks[].etceteraWorkConfiguration.title` | string |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 42 | `data.etceteraWorks[].etceteraWorkConfiguration.translsMap` | object |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 43 | `data.etceteraWorks[].etceteraWorkConfiguration.translsMap.title` | object |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 44 | `data.etceteraWorks[].etceteraWorkConfiguration.translsMap.title.translation` | object(empty) |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 45 | `data.etceteraWorks[].memo` | string(empty) |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 46 | `data.etceteraWorks[].sequence` | int |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 47 | `data.etceteraWorks[].status` | enum: COMPLETED |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 48 | `data.flowStep` | enum: COMPLETED\|CONSULTATION_WAITING\|PROCEDURE_WAITING\|RECEPTION\|RESERVED | visit.flow_step (models/visit.py:86) | 저장됨 | emr/kos/mapper.py:588-590 |
| 49 | `data.flowStepUpdatedDateTimeUtc` | string(ISO UTC) / string(empty) | visit.flow_step_at (models/visit.py:87) | 저장됨 | emr/kos/mapper.py:591 |
| 50 | `data.id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:555 |
| 51 | `data.occupiedResources[]` | array / object | visit_occupied_resource (models/room.py:96) | 저장됨 | emr/kos/mapper.py:542 |
| 52 | `data.occupiedResources[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:368 |
| 53 | `data.occupiedResources[].reservationGroup` | object |  | 해당 없음 | 묶음 |
| 54 | `data.occupiedResources[].reservationGroup.doctors[]` | array(empty) | visit_occupied_resource_doctor (models/room.py:108) | 저장됨 | emr/kos/mapper.py:380-384 |
| 55 | `data.occupiedResources[].reservationGroup.reservationGroupId` | string | visit_occupied_resource.reservation_group_id (models/room.py:101) | 저장됨 | emr/kos/mapper.py:372 |
| 56 | `data.occupiedResources[].reservationGroup.zoneId` | string | visit_occupied_resource.zone_id (models/room.py:102) | 저장됨 | emr/kos/mapper.py:375 |
| 57 | `data.occupiedResources[].reservationTime` | object |  | 해당 없음 | 묶음 |
| 58 | `data.occupiedResources[].reservationTime.endDateTimeUtc` | string(ISO UTC) | visit_occupied_resource.end_at (models/room.py:104) | 저장됨 | emr/kos/mapper.py:379 |
| 59 | `data.occupiedResources[].reservationTime.startDateTimeUtc` | string(ISO UTC) | visit_occupied_resource.start_at (models/room.py:103) | 저장됨 | emr/kos/mapper.py:378 |
| 60 | `data.occupiedResources[].type` | enum: RESERVATION_GROUP | visit_occupied_resource.type (models/room.py:100) | 저장됨 | emr/kos/mapper.py:371 |
| 61 | `data.orderMemo` | string / string(empty) | visit.procedure_order_note (models/visit.py:92) | 저장됨 | emr/kos/mapper.py:598 |
| 62 | `data.prescriptionIds[]` | array / array(empty) / string(uuid) | prescription.visit_id (models/prescription.py:20) | 저장됨 | emr/kos/mapper_purchase.py:104 · S0:501 |
| 63 | `data.purchaseIds[]` | array / array(empty) / string(uuid) | purchase.visit_id (models/purchase.py:58) | 저장됨 | emr/kos/mapper_purchase.py:103 · S0:500 |
| 64 | `data.purchases[]` | array(empty) | purchase.visit_id (models/purchase.py:58) | 계산으로 대체 | S0:500 — purchaseIds[] 로 받는다 · HAR 에서 늘 빈 배열(안쪽 키 확인 안 됨) |
| 65 | `data.reactions[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 · S0 OQ-03-1(:1789) 열림 |
| 66 | `data.receptionDateTimeUtc` | string(ISO UTC) / string(empty) | visit.reception_at (models/visit.py:88) | 저장됨 | emr/kos/mapper.py:592 |
| 67 | `data.reservation` | object |  | 해당 없음 | 묶음 |
| 68 | `data.reservation.connectedChannel` | string / enum: HOMEPAGE | visit.connected_channel (models/visit.py:81) | 저장됨 | emr/kos/mapper.py:580 — `Channel_UNSPEICIFED` 는 None(emr/kos/mapper.py:113-118) |
| 69 | `data.reservation.consultationRequired` | bool | visit.consultation_required (models/visit.py:82) | 저장됨 | emr/kos/mapper.py:581 |
| 70 | `data.reservation.counselor` | object | visit.requested_counselor_id (models/visit.py:77) | 저장됨 | emr/kos/mapper.py:572-574 — 예약 지정 희망 상담사(앞 판 M1) |
| 71 | `data.reservation.counselor.id` | string(empty) | visit.requested_counselor_id (models/visit.py:77) | 저장됨 | emr/kos/mapper.py:572-574 — 예약 지정 희망 상담사(앞 판 M1) |
| 72 | `data.reservation.counselor.name` | string(empty) | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 73 | `data.reservation.doctor` | object | visit.requested_doctor_id (models/visit.py:78) | 저장됨 | emr/kos/mapper.py:575-577 |
| 74 | `data.reservation.doctor.id` | string(empty) | visit.requested_doctor_id (models/visit.py:78) | 저장됨 | emr/kos/mapper.py:575-577 |
| 75 | `data.reservation.doctor.name` | string(empty) | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 76 | `data.reservation.endDateTime` | string(ISO UTC) | visit.reserved_end_at (models/visit.py:71) | 저장됨 | emr/kos/mapper.py:563 |
| 77 | `data.reservation.funnel` | object |  | 해당 없음 | 묶음 |
| 78 | `data.reservation.funnel.funnel` | object | visit.funnel_id (models/visit.py:79) | 저장됨 | emr/kos/mapper.py:578 |
| 79 | `data.reservation.funnel.funnel.category` | enum: FUNNEL | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 80 | `data.reservation.funnel.funnel.closed` | bool | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 81 | `data.reservation.funnel.funnel.default` | bool | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 82 | `data.reservation.funnel.funnel.id` | string(uuid) | visit.funnel_id (models/visit.py:79) | 저장됨 | emr/kos/mapper.py:578 |
| 83 | `data.reservation.funnel.funnel.name` | string | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 84 | `data.reservation.funnel.funnel.order` | int | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 85 | `data.reservation.funnel.funnelDetail` | string(empty) | visit.funnel_detail (models/visit.py:80) | 저장됨 | emr/kos/mapper.py:579 |
| 86 | `data.reservation.requestedProcedures[]` | array(empty) | visit_requested_procedure (models/visit.py:100) · sort_order = 배열 순서(models/visit.py:113) | 저장됨 | emr/kos/mapper.py:536-541 — P07 · P08 · P33 HAR 에서 늘 빈 배열 — 안쪽 키는 HAR 에만 있는 `schedule/v1/queries/get-schedule-summaries` 응답에서만 보인다(K5) |
| 87 | `data.reservation.reservationAssignee` | object | visit.reservation_assignee_id (models/visit.py:76) | 저장됨 | emr/kos/mapper.py:569-571 |
| 88 | `data.reservation.reservationAssignee.id` | string / string(empty) | visit.reservation_assignee_id (models/visit.py:76) | 저장됨 | emr/kos/mapper.py:569-571 |
| 89 | `data.reservation.reservationAssignee.name` | string / string(email꼴) / string(empty) | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 90 | `data.reservation.reservationGroupId` | string | (visit_occupied_resource 쪽 칸은 있음 — 같은 값인지 확인 안 됨) | 칸 없음 | S0:598 「visit 에 두지 않고 visit_occupied_resource 로」는 그룹 칸 얘기 — 이 키 자체의 결정은 없음 |
| 91 | `data.reservation.reservationMemo` | string / string(empty) | visit.reservation_notes (models/visit.py:75) | 저장됨 | emr/kos/mapper.py:568 |
| 92 | `data.reservation.sedationRequired` | bool | visit.sedation_required (models/visit.py:83) | 저장됨 | emr/kos/mapper.py:584 |
| 93 | `data.reservation.startDateTime` | string(ISO UTC) | visit.reserved_start_at (models/visit.py:70) | 저장됨 | emr/kos/mapper.py:560 |
| 94 | `data.reservation.status` | enum: COMPLETED\|IN_PROGRESS\|RESERVED | visit.reservation_status (models/visit.py:72) | 저장됨 | emr/kos/mapper.py:564-567 |
| 95 | `data.reservation.statusUpdatedDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 예약 상태 바뀐 시각 — visit_flow_log 는 flowStep 만 |
| 96 | `data.reservation.zoneId` | string | (visit_occupied_resource 쪽 칸은 있음 — 같은 값인지 확인 안 됨) | 칸 없음 | S0:598 「visit 에 두지 않고 visit_occupied_resource 로」는 그룹 칸 얘기 — 이 키 자체의 결정은 없음 |
| 97 | `data.reservationTagIds[]` | array(empty) |  | 칸 없음 | 예약 태그 id — DAY 칸 없음 |
| 98 | `data.taskTimers[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 · S0 OQ-05-1(:1850) 열림 |
| 99 | `data.tasks[]` | array / array(empty) / object | visit_task (models/task.py:68) | 저장됨 | emr/kos/mapper.py:545-552 |
| 100 | `data.tasks[].anesthesiaType` | enum: ANESTHESIA_TYPE_UNSPECIFIED\|CREAM | visit_task.anesthesia_type (models/task.py:102) | 저장됨 | emr/kos/mapper.py:472 |
| 101 | `data.tasks[].assigneeMemo` | string / string(empty) | visit_task.assignee_note (models/task.py:104) | 저장됨 | emr/kos/mapper.py:474 |
| 102 | `data.tasks[].assignees[]` | array / array(empty) / object | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 103 | `data.tasks[].assignees[].id` | string | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 104 | `data.tasks[].assignees[].name` | string | join staff.name | 계산으로 대체 |  |
| 105 | `data.tasks[].calledDoctors[]` | array / array(empty) / object | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 106 | `data.tasks[].calledDoctors[].id` | string | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 107 | `data.tasks[].calledDoctors[].name` | string | join staff.name | 계산으로 대체 |  |
| 108 | `data.tasks[].completedDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.completed_at (models/task.py:114) | 저장됨 | emr/kos/mapper.py:481 |
| 109 | `data.tasks[].doctorAssignedDateTimeUtc` | string(ISO UTC) | visit_task.doctor_assigned_at (models/task.py:110) | 저장됨 | emr/kos/mapper.py:480 |
| 110 | `data.tasks[].doctorCallDateTime` | string(ISO UTC) / string(empty) | visit_task.doctor_called_at (models/task.py:109) | 저장됨 | emr/kos/mapper.py:479 |
| 111 | `data.tasks[].doctorMemo` | string(empty) | visit_task.doctor_note (models/task.py:105) | 저장됨 | emr/kos/mapper.py:475 |
| 112 | `data.tasks[].doctors[]` | array / array(empty) / object | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 113 | `data.tasks[].doctors[].id` | string | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 114 | `data.tasks[].doctors[].name` | string | join staff.name | 계산으로 대체 |  |
| 115 | `data.tasks[].etceteraConfiguration` | object |  | 해당 없음 | 묶음 |
| 116 | `data.tasks[].etceteraConfiguration.etceteraTaskId` | string / string(empty) | (etc_task_type 표는 있으나 작업 → 종류 FK 없음) | 칸 없음 | emr/kos/mapper.py:485-487 → `is_room_assign`(models/task.py:91) 판정에만 씀(emr/sync_tasks.py:132) |
| 117 | `data.tasks[].etceteraConfiguration.name` | string / string(empty) | visit_task.etc_task_title (models/task.py:88) | 저장됨 | emr/kos/mapper.py:469 |
| 118 | `data.tasks[].etceteraConfiguration.translsMap` | object / object(empty) |  | 칸 없음 |  |
| 119 | `data.tasks[].etceteraConfiguration.translsMap.name` | object |  | 칸 없음 |  |
| 120 | `data.tasks[].etceteraConfiguration.translsMap.name.translation` | object(empty) |  | 칸 없음 |  |
| 121 | `data.tasks[].memo` | string(empty) | visit_task.procedure_note (models/task.py:103) | 저장됨 | emr/kos/mapper.py:473 |
| 122 | `data.tasks[].order` | int | visit_task.sort_order (models/task.py:75) | 저장됨 | emr/kos/mapper.py:456 |
| 123 | `data.tasks[].paymentRequired` | bool | visit_task.payment_required (models/task.py:101) | 저장됨 | emr/kos/mapper.py:471 |
| 124 | `data.tasks[].procedureConfiguration` | object / object(empty) |  | 해당 없음 | 묶음 |
| 125 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration` | object |  | 해당 없음 | 묶음 |
| 126 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.caution` | string(empty) | (treatment_item.code · caution = 지금 메뉴 값 models/menu.py:173 · 176) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 127 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.code` | string | (treatment_item.code · caution = 지금 메뉴 값 models/menu.py:173 · 176) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 128 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.id` | string | visit_task.treatment_item_id (models/task.py:98) | 저장됨 | emr/kos/mapper_purchase.py:88 |
| 129 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.machines[]` | array / array(empty) / object | visit_task.machines (models/task.py:96) | 저장됨 | emr/kos/mapper_purchase.py:89 — 이름 스냅샷 |
| 130 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.machines[].id` | string | (이름 스냅샷만 — id 없음) | 칸 없음 |  |
| 131 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.machines[].name` | string | visit_task.machines (models/task.py:96) | 저장됨 | emr/kos/mapper_purchase.py:89 — 이름 스냅샷 |
| 132 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[]` | array / array(empty) / object | visit_task.medicines (models/task.py:94) | 저장됨 | emr/kos/mapper.py:449 · 470 — 이름 스냅샷 |
| 133 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].id` | string | (이름 스냅샷만 — id 없음) | 칸 없음 |  |
| 134 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].name` | string | visit_task.medicines (models/task.py:94) | 저장됨 | emr/kos/mapper.py:449 · 470 — 이름 스냅샷 |
| 135 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].searchPhoneticName` | string | (machine · medicine.search_phonetic_name = 지금 값) | 칸 없음(시점 다름) |  |
| 136 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.title` | string | visit_task.medical_service_title (models/task.py:80) | 저장됨 | emr/kos/mapper.py:462 |
| 137 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap` | object |  | 칸 없음 |  |
| 138 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title` | object |  | 칸 없음 |  |
| 139 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation` | object / object(empty) |  | 칸 없음 |  |
| 140 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.en` | string |  | 칸 없음 |  |
| 141 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.ja` | string |  | 칸 없음 |  |
| 142 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.ko` | string |  | 칸 없음 |  |
| 143 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.zh-Hans` | string |  | 칸 없음 |  |
| 144 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.zh-Hant` | string |  | 칸 없음 |  |
| 145 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.unit` | object | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) |
| 146 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.unit.type` | enum: CC\|SHOT\|UNIT | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) |
| 147 | `data.tasks[].procedureConfiguration.medicalServiceConfiguration.unit.value` | number | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) |
| 148 | `data.tasks[].procedureConfiguration.productOptionConfiguration` | object |  | 해당 없음 | 묶음 |
| 149 | `data.tasks[].procedureConfiguration.productOptionConfiguration.medicineAndMachines[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 150 | `data.tasks[].procedureConfiguration.productOptionConfiguration.optionId` | string |  | 일부러 안 둠 | S0:892 「상품 옵션 id 는 ERD v1 이 작업에 두지 않음」 |
| 151 | `data.tasks[].procedureConfiguration.productOptionConfiguration.optionTitle` | string | visit_task.option_title (models/task.py:79) | 저장됨 | emr/kos/mapper.py:461 |
| 152 | `data.tasks[].procedureConfiguration.productOptionConfiguration.procedure` | object | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 153 | `data.tasks[].procedureConfiguration.productOptionConfiguration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 「시술 카테고리 칸으로 두지 않는다」 |
| 154 | `data.tasks[].procedureConfiguration.productOptionConfiguration.procedure.createDate` | string(empty) | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 155 | `data.tasks[].procedureConfiguration.productOptionConfiguration.procedure.id` | string | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 156 | `data.tasks[].procedureConfiguration.productOptionConfiguration.procedure.name` | string | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 157 | `data.tasks[].procedureConfiguration.productOptionConfiguration.productTitle` | string / string(empty) | (product.title 은 지금 메뉴 값 · 작업 → 옵션 참조 없음) | 칸 없음(시점 다름) | data_rules 「메뉴 참조 = id + 그때 값 스냅샷」 |
| 158 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap` | object |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 159 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle` | object |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 160 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation` | object / object(empty) |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 161 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.en` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 162 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.ja` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 163 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.ko` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 164 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.zh-Hans` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 165 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.zh-Hant` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 166 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle` | object |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 167 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation` | object |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 168 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.en` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 169 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.ja` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 170 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.ko` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 171 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.zh-Hans` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 172 | `data.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.zh-Hant` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 173 | `data.tasks[].procedureConfiguration.productOptionConfiguration.unit` | object |  | 해당 없음 | 묶음 |
| 174 | `data.tasks[].procedureConfiguration.productOptionConfiguration.unit.type` | enum: CC\|SHOT\|UNIT\|UnitType_UNKNOWN | visit_task.unit_type · unit_value (models/task.py:82 · 85) | 저장됨 | emr/kos/mapper.py:447-466 — `UnitType_UNKNOWN` 은 None |
| 175 | `data.tasks[].procedureConfiguration.productOptionConfiguration.unit.value` | number | visit_task.unit_type · unit_value (models/task.py:82 · 85) | 저장됨 | emr/kos/mapper.py:447-466 — `UnitType_UNKNOWN` 은 None |
| 176 | `data.tasks[].procedureConfiguration.ticketConfiguration` | object / object(empty) |  | 해당 없음 | 묶음(시술권이 아니면 빈 객체) |
| 177 | `data.tasks[].procedureConfiguration.ticketConfiguration.round` | object |  | 해당 없음 | 묶음 |
| 178 | `data.tasks[].procedureConfiguration.ticketConfiguration.round.current` | int | visit_task.ticket_round_current (models/task.py:86) | 저장됨 | emr/kos/mapper.py:467 |
| 179 | `data.tasks[].procedureConfiguration.ticketConfiguration.round.total` | int | visit_task.ticket_round_total (models/task.py:87) | 저장됨 | emr/kos/mapper.py:468 |
| 180 | `data.tasks[].procedureConfiguration.ticketConfiguration.ticketId` | string(uuid) | visit_task.ticket_id (models/task.py:99) | 저장됨 | emr/kos/mapper_purchase.py:85-87 |
| 181 | `data.tasks[].readyDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.ready_at (models/task.py:108) | 저장됨 | emr/kos/mapper.py:478 |
| 182 | `data.tasks[].room` | object | visit_task.room_id (models/task.py:106) | 저장됨 | emr/kos/mapper.py:450-452 · 카드 방 visit.room_id(models/visit.py:93) emr/kos/mapper.py:388-408 |
| 183 | `data.tasks[].room.id` | string / string(empty) | visit_task.room_id (models/task.py:106) | 저장됨 | emr/kos/mapper.py:450-452 · 카드 방 visit.room_id(models/visit.py:93) emr/kos/mapper.py:388-408 |
| 184 | `data.tasks[].room.order` | int | join room (models/room.py:43-49) | 계산으로 대체 |  |
| 185 | `data.tasks[].room.title` | string / string(empty) | join room (models/room.py:43-49) | 계산으로 대체 |  |
| 186 | `data.tasks[].room.zoneId` | string / string(empty) | join room (models/room.py:43-49) | 계산으로 대체 |  |
| 187 | `data.tasks[].roomAssignedDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.room_assigned_at (models/task.py:107) | 저장됨 | emr/kos/mapper.py:477 |
| 188 | `data.tasks[].sequence` | int | visit_task.sequence (models/task.py:74) | 저장됨 | emr/kos/mapper.py:454 |
| 189 | `data.tasks[].status` | enum: DONE\|NOT_STARTED\|READY\|WAITING | visit_task.status (models/task.py:76) | 저장됨 | emr/kos/mapper.py:457-459 |
| 190 | `data.tasks[].title` | string | visit_task.title (models/task.py:78) | 저장됨 | emr/kos/mapper.py:460 |
| 191 | `data.tasks[].translsMap` | object |  | 칸 없음 | 작업 이름 번역 |
| 192 | `data.tasks[].translsMap.title` | object |  | 칸 없음 | 작업 이름 번역 |
| 193 | `data.tasks[].translsMap.title.translation` | object / object(empty) |  | 칸 없음 | 작업 이름 번역 |
| 194 | `data.tasks[].translsMap.title.translation.de` | string |  | 칸 없음 | 작업 이름 번역 |
| 195 | `data.tasks[].translsMap.title.translation.en` | string |  | 칸 없음 | 작업 이름 번역 |
| 196 | `data.tasks[].translsMap.title.translation.es` | string |  | 칸 없음 | 작업 이름 번역 |
| 197 | `data.tasks[].translsMap.title.translation.fr` | string |  | 칸 없음 | 작업 이름 번역 |
| 198 | `data.tasks[].translsMap.title.translation.id` | string |  | 칸 없음 | 작업 이름 번역 |
| 199 | `data.tasks[].translsMap.title.translation.ja` | string |  | 칸 없음 | 작업 이름 번역 |
| 200 | `data.tasks[].translsMap.title.translation.ko` | string |  | 칸 없음 | 작업 이름 번역 |
| 201 | `data.tasks[].translsMap.title.translation.mn` | string |  | 칸 없음 | 작업 이름 번역 |
| 202 | `data.tasks[].translsMap.title.translation.ms` | string |  | 칸 없음 | 작업 이름 번역 |
| 203 | `data.tasks[].translsMap.title.translation.nl` | string |  | 칸 없음 | 작업 이름 번역 |
| 204 | `data.tasks[].translsMap.title.translation.pt` | string |  | 칸 없음 | 작업 이름 번역 |
| 205 | `data.tasks[].translsMap.title.translation.ru` | string |  | 칸 없음 | 작업 이름 번역 |
| 206 | `data.tasks[].translsMap.title.translation.th` | string |  | 칸 없음 | 작업 이름 번역 |
| 207 | `data.tasks[].translsMap.title.translation.uz` | string |  | 칸 없음 | 작업 이름 번역 |
| 208 | `data.tasks[].translsMap.title.translation.vi` | string |  | 칸 없음 | 작업 이름 번역 |
| 209 | `data.tasks[].translsMap.title.translation.zh-Hans` | string |  | 칸 없음 | 작업 이름 번역 |
| 210 | `data.tasks[].translsMap.title.translation.zh-Hant` | string |  | 칸 없음 | 작업 이름 번역 |
| 211 | `data.tasks[].type` | enum: ETCETERA\|PROCEDURE | visit_task.kind (models/task.py:73) | 저장됨 | emr/kos/mapper.py:455 |
| 212 | `data.tasks[].urgencyLevel` | enum: URGENCY_LEVEL_UNSPECIFIED |  | 칸 없음 | 긴급도 |
| 213 | `data.updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 저장됨 | emr/kos/mapper.py:556 · emr/sync_schedules.py:271 |
| 214 | `data.visitor` | object | customer (models/customer.py:33) | 저장됨 | emr/kos/mapper.py:558 |
| 215 | `data.visitor.categories[]` | array / array(empty) / object | customer_category_link (models/customer.py:157) | 저장됨 | emr/kos/mapper.py:322-327 |
| 216 | `data.visitor.categories[].color` | string | join customer_category (models/customer.py:124-131) | 계산으로 대체 | get-codes VISITOR_CATEGORY 로 채움 |
| 217 | `data.visitor.categories[].id` | string(uuid) | customer_category_link (models/customer.py:157) | 저장됨 | emr/kos/mapper.py:322-327 |
| 218 | `data.visitor.categories[].name` | string | join customer_category (models/customer.py:124-131) | 계산으로 대체 | get-codes VISITOR_CATEGORY 로 채움 |
| 219 | `data.visitor.categories[].order` | int | join customer_category (models/customer.py:124-131) | 계산으로 대체 | get-codes VISITOR_CATEGORY 로 채움 |
| 220 | `data.visitor.chartNumber` | string(digits) | customer.chart_number (models/customer.py:43) + external_ref.external_number (models/customer.py:107) | 저장됨 | emr/kos/mapper.py:308 · emr/sync_schedules.py:150 |
| 221 | `data.visitor.dateOfBirth` | string / string(empty) | customer.birth_date (models/customer.py:52) | 저장됨 | emr/kos/mapper.py:312 |
| 222 | `data.visitor.gender` | enum: FEMALE\|GENDER_UNSPECIFIED\|MALE | customer.gender (models/customer.py:51) | 저장됨 | emr/kos/mapper.py:311 — `GENDER_UNSPECIFIED` 는 None |
| 223 | `data.visitor.id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:307 |
| 224 | `data.visitor.isNew` | bool | visit.is_new (models/visit.py:91) | 저장됨 | emr/kos/mapper.py:597 — 방문마다 값(S0:301 · 360) |
| 225 | `data.visitor.memo` | string / string(empty) | customer.customer_notes (models/customer.py:72) | 저장됨 | emr/kos/mapper.py:316 |
| 226 | `data.visitor.name` | string | customer.name (models/customer.py:46) | 저장됨 | emr/kos/mapper.py:309 |
| 227 | `data.visitor.nationality` | string | customer.nationality (models/customer.py:53) | 저장됨 | emr/kos/mapper.py:313 |
| 228 | `data.visitor.phone` | object |  | 해당 없음 | 묶음 |
| 229 | `data.visitor.phone.countryCode` | string(digits) | customer.phone_country_code (models/customer.py:61) | 저장됨 | emr/kos/mapper.py:314 |
| 230 | `data.visitor.phone.phoneNumber` | string(digits) | customer.phone_number (models/customer.py:62) | 저장됨 | emr/kos/mapper.py:315 |
| 231 | `data.visitor.phoneticName` | string / string(empty) | customer.name_pronunciation (models/customer.py:47) | 저장됨 | emr/kos/mapper.py:310 |
| 232 | `data.visitor.snsInfo` | object |  | 해당 없음 | 묶음 |
| 233 | `data.visitor.snsInfo.accountId` | string / string(empty) | customer.sns_account_id (models/customer.py:70) | 저장됨 | emr/kos/mapper.py:318 |
| 234 | `data.visitor.snsInfo.snsType` | string | customer.sns_type (models/customer.py:69) | 저장됨 | emr/kos/mapper.py:317 |
| 235 | `data.visitor.visitorType` | object | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 |
| 236 | `data.visitor.visitorType.id` | string / string(empty) | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 |
| 237 | `data.visitor.visitorType.name` | string / string(empty) | customer_type.name (models/customer.py:120) | 저장됨 | emr/kos/mapper.py:319-321 |
| 238 | `data.visitorLocation` | object |  | 해당 없음 | 묶음 |
| 239 | `data.visitorLocation.zoneId` | string | visit.current_zone_id (models/visit.py:90) | 저장됨 | emr/kos/mapper.py:594-596 |
| 240 | `data.zone` | object |  | 해당 없음 | 묶음 |
| 241 | `data.zone.id` | string | visit.reception_zone_id (models/visit.py:89) | 저장됨 | emr/kos/mapper.py:593 |
| 242 | `data.zone.title` | string | join zone.title (models/room.py:35) | 계산으로 대체 | 구역 이름 — 기준 정보 1시간 |

### P09 `procedure-menu/categories/queries/get-categories`

스크립트 합집합 키 **14** · 표 행 **14** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].deleted` | bool | external_ref.is_present_in_source · deleted_at | 저장됨 | emr/kos/mapper_menu.py:73 · emr/kos/sale_reads.py:153-156 |
| 3 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_menu.py:75 |
| 4 | `data[].name` | string | product_category.name (models/menu.py:52) | 저장됨 | emr/kos/mapper_menu.py:76 |
| 5 | `data[].opened` | bool | product_category.is_open (models/menu.py:54) | 저장됨 | emr/kos/mapper_menu.py:78 |
| 6 | `data[].order` | int | product_category.sort_order (models/menu.py:53) | 저장됨 | emr/kos/mapper_menu.py:77 |
| 7 | `data[].translsMap` | object |  | 해당 없음 | 묶음(`name` 만 저장) |
| 8 | `data[].translsMap.name` | object | product_category.name_translations (models/menu.py:56) | 저장됨 | emr/kos/mapper_menu.py:79 — JSON 통째 |
| 9 | `data[].translsMap.name.translation` | object | product_category.name_translations (models/menu.py:56) | 저장됨 | emr/kos/mapper_menu.py:79 — JSON 통째 |
| 10 | `data[].translsMap.name.translation.en` | string | product_category.name_translations (models/menu.py:56) | 저장됨 | emr/kos/mapper_menu.py:79 — JSON 통째 |
| 11 | `data[].translsMap.name.translation.ja` | string | product_category.name_translations (models/menu.py:56) | 저장됨 | emr/kos/mapper_menu.py:79 — JSON 통째 |
| 12 | `data[].translsMap.name.translation.ko` | string | product_category.name_translations (models/menu.py:56) | 저장됨 | emr/kos/mapper_menu.py:79 — JSON 통째 |
| 13 | `data[].translsMap.name.translation.zh-Hans` | string | product_category.name_translations (models/menu.py:56) | 저장됨 | emr/kos/mapper_menu.py:79 — JSON 통째 |
| 14 | `data[].translsMap.name.translation.zh-Hant` | string | product_category.name_translations (models/menu.py:56) | 저장됨 | emr/kos/mapper_menu.py:79 — JSON 통째 |

### P10 `procedure-menu/products/queries/get-products`

스크립트 합집합 키 **210** · 표 행 **210** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].badges[]` | array(empty) | product.badges (models/menu.py:74) | 저장됨 | emr/kos/mapper_menu.py:171 — HAR 에서 늘 빈 배열 |
| 3 | `data[].categories[]` | array / object | product_category_link (models/menu.py:86) | 저장됨 | emr/kos/mapper_menu.py:175-181 |
| 4 | `data[].categories[].id` | string | product_category_link (models/menu.py:86) | 저장됨 | emr/kos/mapper_menu.py:175-181 |
| 5 | `data[].categories[].name` | string | join product_category (models/menu.py:48-56) | 계산으로 대체 |  |
| 6 | `data[].categories[].translsMap` | object | join product_category (models/menu.py:48-56) | 계산으로 대체 |  |
| 7 | `data[].categories[].translsMap.name` | object | join product_category (models/menu.py:48-56) | 계산으로 대체 |  |
| 8 | `data[].categories[].translsMap.name.translation` | object | join product_category (models/menu.py:48-56) | 계산으로 대체 |  |
| 9 | `data[].categories[].translsMap.name.translation.en` | string | join product_category (models/menu.py:48-56) | 계산으로 대체 |  |
| 10 | `data[].categories[].translsMap.name.translation.ja` | string | join product_category (models/menu.py:48-56) | 계산으로 대체 |  |
| 11 | `data[].categories[].translsMap.name.translation.ko` | string | join product_category (models/menu.py:48-56) | 계산으로 대체 |  |
| 12 | `data[].categories[].translsMap.name.translation.zh-Hans` | string | join product_category (models/menu.py:48-56) | 계산으로 대체 |  |
| 13 | `data[].categories[].translsMap.name.translation.zh-Hant` | string | join product_category (models/menu.py:48-56) | 계산으로 대체 |  |
| 14 | `data[].caution` | string(empty) | product.caution (models/menu.py:66) | 저장됨 | emr/kos/mapper_menu.py:162 |
| 15 | `data[].cautions[]` | array / array(empty) / string(empty) | product.cautions (models/menu.py:78) | 저장됨 | emr/kos/mapper_menu.py:163 |
| 16 | `data[].closed` | bool | product.is_closed (models/menu.py:68) | 저장됨 | emr/kos/mapper_menu.py:165 |
| 17 | `data[].deleted` | bool | external_ref.is_present_in_source · deleted_at | 저장됨 | emr/kos/mapper_menu.py:146 · emr/kos/sale_reads.py:153-156 |
| 18 | `data[].description` | string | product.description (models/menu.py:65) | 저장됨 | emr/kos/mapper_menu.py:161 |
| 19 | `data[].displayPeriod` | object |  | 해당 없음 | 묶음 |
| 20 | `data[].displayPeriod.endDateTimeUtc` | string(ISO UTC) | product.display_to (models/menu.py:71) | 저장됨 | emr/kos/mapper_menu.py:168 |
| 21 | `data[].displayPeriod.startDateTimeUtc` | string(ISO UTC) | product.display_from (models/menu.py:70) | 저장됨 | emr/kos/mapper_menu.py:167 |
| 22 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_menu.py:159 |
| 23 | `data[].isEvent` | bool | product.is_event (models/menu.py:67) | 저장됨 | emr/kos/mapper_menu.py:164 |
| 24 | `data[].medicineAndMachines[]` | array / array(empty) / object | product.medicine_and_machine_names (models/menu.py:80) | 저장됨 | emr/kos/mapper_menu.py:174 — 이름만 |
| 25 | `data[].medicineAndMachines[].id` | string | (이름만 저장) | 칸 없음 |  |
| 26 | `data[].medicineAndMachines[].name` | string | product.medicine_and_machine_names (models/menu.py:80) | 저장됨 | emr/kos/mapper_menu.py:174 — 이름만 |
| 27 | `data[].offeringPeriod` | object |  | 해당 없음 | 묶음 |
| 28 | `data[].offeringPeriod.endDateTimeUtc` | string(ISO UTC) | product.offering_to (models/menu.py:73) | 저장됨 | emr/kos/mapper_menu.py:170 |
| 29 | `data[].offeringPeriod.startDateTimeUtc` | string(ISO UTC) | product.offering_from (models/menu.py:72) | 저장됨 | emr/kos/mapper_menu.py:169 |
| 30 | `data[].options[]` | array / array(empty) / object | product_option (models/menu.py:100) | 저장됨 | emr/kos/mapper_menu.py:150-157 |
| 31 | `data[].options[].badges[]` | array(empty) | product_option.badges (models/menu.py:122) | 저장됨 | emr/kos/mapper_menu.py:136 — HAR 에서 늘 빈 배열 |
| 32 | `data[].options[].compositions[]` | array / array(empty) / object | product_option_composition (models/menu.py:144) · sort_order = 배열 순서(models/menu.py:161) | 저장됨 | emr/kos/mapper_menu.py:118 · 93-96 |
| 33 | `data[].options[].compositions[].count` | int | product_option_composition.count (models/menu.py:154) | 저장됨 | emr/kos/mapper_menu.py:102 |
| 34 | `data[].options[].compositions[].medicalService` | object | treatment_item (models/menu.py:169) | 저장됨 | emr/kos/mapper_menu.py:187-221 · emr/kos/sale_reads.py:85-103 |
| 35 | `data[].options[].compositions[].medicalService.caution` | string(empty) | treatment_item.caution (models/menu.py:176) | 저장됨 | emr/kos/mapper_menu.py:197 |
| 36 | `data[].options[].compositions[].medicalService.configuration` | object |  | 해당 없음 | 묶음 |
| 37 | `data[].options[].compositions[].medicalService.configuration.code` | string | treatment_item.code (models/menu.py:173) | 저장됨 | emr/kos/mapper_menu.py:194 |
| 38 | `data[].options[].compositions[].medicalService.configuration.healthcareReimbursement` | string | treatment_item.healthcare_reimbursement (models/menu.py:181) | 저장됨 | emr/kos/mapper_menu.py:202 |
| 39 | `data[].options[].compositions[].medicalService.configuration.machines[]` | array / array(empty) / object | treatment_item_machine (models/menu.py:193) | 저장됨 | emr/kos/mapper_menu.py:207-213 |
| 40 | `data[].options[].compositions[].medicalService.configuration.machines[].id` | string | external_ref.external_id (models/customer.py:106) · machine | 저장됨 | emr/kos/mapper_menu.py:237 · emr/kos/sale_reads.py:115-118 |
| 41 | `data[].options[].compositions[].medicalService.configuration.machines[].name` | string | machine.name (models/menu.py:228) | 저장됨 | emr/kos/mapper_menu.py:238 |
| 42 | `data[].options[].compositions[].medicalService.configuration.machines[].searchPhoneticName` | string | machine.search_phonetic_name (models/menu.py:230) | 저장됨 | emr/kos/mapper_menu.py:239 |
| 43 | `data[].options[].compositions[].medicalService.configuration.medicines[]` | array / array(empty) / object | treatment_item_medicine (models/menu.py:202) | 저장됨 | emr/kos/mapper_menu.py:214-220 |
| 44 | `data[].options[].compositions[].medicalService.configuration.medicines[].id` | string | external_ref.external_id (models/customer.py:106) · medicine | 저장됨 | emr/kos/mapper_menu.py:245 |
| 45 | `data[].options[].compositions[].medicalService.configuration.medicines[].name` | string | medicine.name (models/menu.py:238) | 저장됨 | emr/kos/mapper_menu.py:246 |
| 46 | `data[].options[].compositions[].medicalService.configuration.medicines[].searchPhoneticName` | string | medicine.search_phonetic_name (models/menu.py:240) | 저장됨 | emr/kos/mapper_menu.py:247 |
| 47 | `data[].options[].compositions[].medicalService.configuration.procedure` | object | treatment_item.treatment_id (models/menu.py:178) | 저장됨 | emr/kos/mapper_menu.py:199 |
| 48 | `data[].options[].compositions[].medicalService.configuration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 |
| 49 | `data[].options[].compositions[].medicalService.configuration.procedure.id` | string | treatment_item.treatment_id (models/menu.py:178) | 저장됨 | emr/kos/mapper_menu.py:199 |
| 50 | `data[].options[].compositions[].medicalService.configuration.procedure.name` | string | join treatment (models/menu.py:213-220) | 계산으로 대체 |  |
| 51 | `data[].options[].compositions[].medicalService.configuration.procedure.searchPhoneticName` | string | join treatment (models/menu.py:213-220) | 계산으로 대체 |  |
| 52 | `data[].options[].compositions[].medicalService.configuration.taxation` | string | treatment_item.taxation (models/menu.py:182) | 저장됨 | emr/kos/mapper_menu.py:203 |
| 53 | `data[].options[].compositions[].medicalService.configuration.unit` | object | treatment_item.unit_type · unit_value (models/menu.py:179-180) | 저장됨 | emr/kos/mapper_menu.py:191 |
| 54 | `data[].options[].compositions[].medicalService.configuration.unit.type` | enum: CC\|KJ\|PULSE\|SHOT | treatment_item.unit_type · unit_value (models/menu.py:179-180) | 저장됨 | emr/kos/mapper_menu.py:191 |
| 55 | `data[].options[].compositions[].medicalService.configuration.unit.value` | number | treatment_item.unit_type · unit_value (models/menu.py:179-180) | 저장됨 | emr/kos/mapper_menu.py:191 |
| 56 | `data[].options[].compositions[].medicalService.deleted` | bool | treatment_item.deleted_at | 저장됨 | emr/kos/sale_reads.py:101-112 |
| 57 | `data[].options[].compositions[].medicalService.description` | string(empty) | treatment_item.description (models/menu.py:175) | 저장됨 | emr/kos/mapper_menu.py:196 |
| 58 | `data[].options[].compositions[].medicalService.draftedDateTimeUtc` | string(ISO UTC) | treatment_item.drafted_at (models/menu.py:189) | 저장됨 | emr/kos/mapper_menu.py:205 |
| 59 | `data[].options[].compositions[].medicalService.id` | string | product_option_composition.treatment_item_id (models/menu.py:150) + external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_menu.py:98-100 · 193 |
| 60 | `data[].options[].compositions[].medicalService.status` | enum: PUBLISHED | treatment_item.status (models/menu.py:177) | 저장됨 | emr/kos/mapper_menu.py:198 |
| 61 | `data[].options[].compositions[].medicalService.title` | string | treatment_item.title (models/menu.py:174) | 저장됨 | emr/kos/mapper_menu.py:195 |
| 62 | `data[].options[].compositions[].medicalService.translsMap` | object | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 63 | `data[].options[].compositions[].medicalService.translsMap.title` | object | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 64 | `data[].options[].compositions[].medicalService.translsMap.title.translation` | object | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 65 | `data[].options[].compositions[].medicalService.translsMap.title.translation.en` | string | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 66 | `data[].options[].compositions[].medicalService.translsMap.title.translation.ja` | string | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 67 | `data[].options[].compositions[].medicalService.translsMap.title.translation.ko` | string | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 68 | `data[].options[].compositions[].medicalService.translsMap.title.translation.zh-Hans` | string | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 69 | `data[].options[].compositions[].medicalService.translsMap.title.translation.zh-Hant` | string | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 70 | `data[].options[].compositions[].medicalService.updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 저장됨 | emr/kos/mapper_menu.py:206 · emr/sync_menu.py:122 |
| 71 | `data[].options[].compositions[].medicineAndMachines[]` | array / object | product_option_composition.medicine_and_machine_names (models/menu.py:163) | 저장됨 | emr/kos/mapper_menu.py:106 |
| 72 | `data[].options[].compositions[].medicineAndMachines[].id` | string | (이름만 저장) | 칸 없음 |  |
| 73 | `data[].options[].compositions[].medicineAndMachines[].name` | string | product_option_composition.medicine_and_machine_names (models/menu.py:163) | 저장됨 | emr/kos/mapper_menu.py:106 |
| 74 | `data[].options[].compositions[].price` | object |  | 해당 없음 | 묶음 |
| 75 | `data[].options[].compositions[].price.additional[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 · 구성에 수가 유형별 가격 표 없음 |
| 76 | `data[].options[].compositions[].price.amount` | object |  | 해당 없음 | 묶음 |
| 77 | `data[].options[].compositions[].price.amount.currency` | enum: KRW | (구성 표에 통화 칸 없음) | 칸 없음 | 앞 판 E1 |
| 78 | `data[].options[].compositions[].price.amount.value` | int | product_option_composition.price_amount (models/menu.py:157) | 저장됨 | emr/kos/mapper_menu.py:105 |
| 79 | `data[].options[].compositions[].price.suppliedAmount` | object | product_option_composition.supplied_amount (models/menu.py:158) | 저장됨 | emr/kos/mapper_menu.py:105 |
| 80 | `data[].options[].compositions[].price.suppliedAmount.currency` | enum: KRW | (구성 표에 통화 칸 없음) | 칸 없음 | 앞 판 E1 |
| 81 | `data[].options[].compositions[].price.suppliedAmount.value` | int | product_option_composition.supplied_amount (models/menu.py:158) | 저장됨 | emr/kos/mapper_menu.py:105 |
| 82 | `data[].options[].compositions[].price.taxFreeAmount` | object | product_option_composition.tax_free_amount (models/menu.py:160) | 저장됨 | emr/kos/mapper_menu.py:105 |
| 83 | `data[].options[].compositions[].price.taxFreeAmount.currency` | enum: KRW | (구성 표에 통화 칸 없음) | 칸 없음 | 앞 판 E1 |
| 84 | `data[].options[].compositions[].price.taxFreeAmount.value` | int | product_option_composition.tax_free_amount (models/menu.py:160) | 저장됨 | emr/kos/mapper_menu.py:105 |
| 85 | `data[].options[].compositions[].price.taxation` | string | (매퍼는 읽으나 구성 표에 과세 칸 없음 — emr/kos/mapper_sale_values.py:130) | 칸 없음 |  |
| 86 | `data[].options[].compositions[].price.vatAmount` | object | product_option_composition.vat_amount (models/menu.py:159) | 저장됨 | emr/kos/mapper_menu.py:105 |
| 87 | `data[].options[].compositions[].price.vatAmount.currency` | enum: KRW | (구성 표에 통화 칸 없음) | 칸 없음 | 앞 판 E1 |
| 88 | `data[].options[].compositions[].price.vatAmount.value` | int | product_option_composition.vat_amount (models/menu.py:159) | 저장됨 | emr/kos/mapper_menu.py:105 |
| 89 | `data[].options[].compositions[].procedure` | object | product_option_composition.treatment_id (models/menu.py:151) | 저장됨 | emr/kos/mapper_menu.py:101 |
| 90 | `data[].options[].compositions[].procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 |
| 91 | `data[].options[].compositions[].procedure.createDate` | string(empty) | join treatment | 계산으로 대체 |  |
| 92 | `data[].options[].compositions[].procedure.id` | string | product_option_composition.treatment_id (models/menu.py:151) | 저장됨 | emr/kos/mapper_menu.py:101 |
| 93 | `data[].options[].compositions[].procedure.name` | string | join treatment | 계산으로 대체 |  |
| 94 | `data[].options[].compositions[].title` | string(empty) | product_option_composition.title (models/menu.py:153) | 저장됨 | emr/kos/mapper_menu.py:97 |
| 95 | `data[].options[].compositions[].unit` | object | product_option_composition.unit_type · unit_value (models/menu.py:155-156) | 저장됨 | emr/kos/mapper_menu.py:94 |
| 96 | `data[].options[].compositions[].unit.type` | enum: CC\|KJ\|PULSE\|SHOT\|UnitType_UNKNOWN | product_option_composition.unit_type · unit_value (models/menu.py:155-156) | 저장됨 | emr/kos/mapper_menu.py:94 |
| 97 | `data[].options[].compositions[].unit.value` | number | product_option_composition.unit_type · unit_value (models/menu.py:155-156) | 저장됨 | emr/kos/mapper_menu.py:94 |
| 98 | `data[].options[].count` | int | product_option.count (models/menu.py:108) | 저장됨 | emr/kos/mapper_menu.py:127 |
| 99 | `data[].options[].deleted` | bool | (지운 옵션은 받지 않음 → 사라짐) | 저장됨 | emr/kos/mapper_menu.py:151-152 · emr/kos/sale_reads.py:173-181 |
| 100 | `data[].options[].description` | string | product_option.description (models/menu.py:107) | 저장됨 | emr/kos/mapper_menu.py:126 |
| 101 | `data[].options[].displayChannels[]` | array / string | product_option.display_channels (models/menu.py:119) | 저장됨 | emr/kos/mapper_menu.py:119 · 135 — 표 밖 값은 뺀다 |
| 102 | `data[].options[].frequentlyUsedOption` | bool | product_option.is_frequently_used (models/menu.py:117) | 저장됨 | emr/kos/mapper_menu.py:133 |
| 103 | `data[].options[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_menu.py:121 |
| 104 | `data[].options[].medicalService` | object | treatment_item (models/menu.py:169) | 저장됨 | emr/kos/mapper_menu.py:187-221 · emr/kos/sale_reads.py:85-103 |
| 105 | `data[].options[].medicalService.caution` | string(empty) | treatment_item.caution (models/menu.py:176) | 저장됨 | emr/kos/mapper_menu.py:197 |
| 106 | `data[].options[].medicalService.configuration` | object |  | 해당 없음 | 묶음 |
| 107 | `data[].options[].medicalService.configuration.code` | string | treatment_item.code (models/menu.py:173) | 저장됨 | emr/kos/mapper_menu.py:194 |
| 108 | `data[].options[].medicalService.configuration.healthcareReimbursement` | string | treatment_item.healthcare_reimbursement (models/menu.py:181) | 저장됨 | emr/kos/mapper_menu.py:202 |
| 109 | `data[].options[].medicalService.configuration.machines[]` | array / array(empty) / object | treatment_item_machine (models/menu.py:193) | 저장됨 | emr/kos/mapper_menu.py:207-213 |
| 110 | `data[].options[].medicalService.configuration.machines[].id` | string | external_ref.external_id (models/customer.py:106) · machine | 저장됨 | emr/kos/mapper_menu.py:237 · emr/kos/sale_reads.py:115-118 |
| 111 | `data[].options[].medicalService.configuration.machines[].name` | string | machine.name (models/menu.py:228) | 저장됨 | emr/kos/mapper_menu.py:238 |
| 112 | `data[].options[].medicalService.configuration.machines[].searchPhoneticName` | string | machine.search_phonetic_name (models/menu.py:230) | 저장됨 | emr/kos/mapper_menu.py:239 |
| 113 | `data[].options[].medicalService.configuration.medicines[]` | array / array(empty) / object | treatment_item_medicine (models/menu.py:202) | 저장됨 | emr/kos/mapper_menu.py:214-220 |
| 114 | `data[].options[].medicalService.configuration.medicines[].id` | string | external_ref.external_id (models/customer.py:106) · medicine | 저장됨 | emr/kos/mapper_menu.py:245 |
| 115 | `data[].options[].medicalService.configuration.medicines[].name` | string | medicine.name (models/menu.py:238) | 저장됨 | emr/kos/mapper_menu.py:246 |
| 116 | `data[].options[].medicalService.configuration.medicines[].searchPhoneticName` | string | medicine.search_phonetic_name (models/menu.py:240) | 저장됨 | emr/kos/mapper_menu.py:247 |
| 117 | `data[].options[].medicalService.configuration.procedure` | object | treatment_item.treatment_id (models/menu.py:178) | 저장됨 | emr/kos/mapper_menu.py:199 |
| 118 | `data[].options[].medicalService.configuration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 |
| 119 | `data[].options[].medicalService.configuration.procedure.id` | string | treatment_item.treatment_id (models/menu.py:178) | 저장됨 | emr/kos/mapper_menu.py:199 |
| 120 | `data[].options[].medicalService.configuration.procedure.name` | string | join treatment (models/menu.py:213-220) | 계산으로 대체 |  |
| 121 | `data[].options[].medicalService.configuration.procedure.searchPhoneticName` | string | join treatment (models/menu.py:213-220) | 계산으로 대체 |  |
| 122 | `data[].options[].medicalService.configuration.taxation` | string | treatment_item.taxation (models/menu.py:182) | 저장됨 | emr/kos/mapper_menu.py:203 |
| 123 | `data[].options[].medicalService.configuration.unit` | object | treatment_item.unit_type · unit_value (models/menu.py:179-180) | 저장됨 | emr/kos/mapper_menu.py:191 |
| 124 | `data[].options[].medicalService.configuration.unit.type` | enum: CC\|KJ\|MINUTE\|PULSE\|QUANTITY\|SHOT\|UNIT | treatment_item.unit_type · unit_value (models/menu.py:179-180) | 저장됨 | emr/kos/mapper_menu.py:191 |
| 125 | `data[].options[].medicalService.configuration.unit.value` | number | treatment_item.unit_type · unit_value (models/menu.py:179-180) | 저장됨 | emr/kos/mapper_menu.py:191 |
| 126 | `data[].options[].medicalService.deleted` | bool | treatment_item.deleted_at | 저장됨 | emr/kos/sale_reads.py:101-112 |
| 127 | `data[].options[].medicalService.description` | string / string(empty) | treatment_item.description (models/menu.py:175) | 저장됨 | emr/kos/mapper_menu.py:196 |
| 128 | `data[].options[].medicalService.draftedDateTimeUtc` | string(ISO UTC) | treatment_item.drafted_at (models/menu.py:189) | 저장됨 | emr/kos/mapper_menu.py:205 |
| 129 | `data[].options[].medicalService.id` | string | product_option.treatment_item_id (models/menu.py:110) + external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_menu.py:129-131 · 193 |
| 130 | `data[].options[].medicalService.status` | enum: PUBLISHED | treatment_item.status (models/menu.py:177) | 저장됨 | emr/kos/mapper_menu.py:198 |
| 131 | `data[].options[].medicalService.title` | string | treatment_item.title (models/menu.py:174) | 저장됨 | emr/kos/mapper_menu.py:195 |
| 132 | `data[].options[].medicalService.translsMap` | object | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 133 | `data[].options[].medicalService.translsMap.caution` | object | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 134 | `data[].options[].medicalService.translsMap.caution.translation` | object(empty) | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 135 | `data[].options[].medicalService.translsMap.description` | object | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 136 | `data[].options[].medicalService.translsMap.description.translation` | object | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 137 | `data[].options[].medicalService.translsMap.description.translation.ko` | string | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 138 | `data[].options[].medicalService.translsMap.title` | object | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 139 | `data[].options[].medicalService.translsMap.title.translation` | object / object(empty) | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 140 | `data[].options[].medicalService.translsMap.title.translation.en` | string | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 141 | `data[].options[].medicalService.translsMap.title.translation.ja` | string | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 142 | `data[].options[].medicalService.translsMap.title.translation.ko` | string | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 143 | `data[].options[].medicalService.translsMap.title.translation.zh-Hans` | string | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 144 | `data[].options[].medicalService.translsMap.title.translation.zh-Hant` | string | treatment_item.translations (models/menu.py:187) | 저장됨 | emr/kos/mapper_menu.py:204 — JSON 통째 |
| 145 | `data[].options[].medicalService.updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 저장됨 | emr/kos/mapper_menu.py:206 · emr/sync_menu.py:122 |
| 146 | `data[].options[].medicineAndMachines[]` | array / array(empty) / object | product_option.medicine_and_machine_names (models/menu.py:126) | 저장됨 | emr/kos/mapper_menu.py:139 |
| 147 | `data[].options[].medicineAndMachines[].id` | string | (이름만 저장) | 칸 없음 |  |
| 148 | `data[].options[].medicineAndMachines[].name` | string | product_option.medicine_and_machine_names (models/menu.py:126) | 저장됨 | emr/kos/mapper_menu.py:139 |
| 149 | `data[].options[].price` | object |  | 해당 없음 | 묶음 |
| 150 | `data[].options[].price.additional[]` | array(empty) | product_option_price (models/menu.py:132) | 저장됨 | emr/kos/mapper_menu.py:83-90 · 115-116 |
| 151 | `data[].options[].price.amount` | object |  | 해당 없음 | 묶음 |
| 152 | `data[].options[].price.amount.currency` | enum: KRW | product_option.currency (models/menu.py:115) | 저장됨 | emr/kos/mapper_sale_values.py:131 |
| 153 | `data[].options[].price.amount.value` | int | product_option.price_amount (models/menu.py:111) | 저장됨 | emr/kos/mapper_menu.py:132 · emr/kos/mapper_sale_values.py:122-132 |
| 154 | `data[].options[].price.suppliedAmount` | object | product_option.supplied_amount (models/menu.py:112) | 저장됨 | emr/kos/mapper_sale_values.py:127 |
| 155 | `data[].options[].price.suppliedAmount.currency` | enum: KRW | (통화는 amount 쪽 하나만) | 칸 없음 |  |
| 156 | `data[].options[].price.suppliedAmount.value` | int | product_option.supplied_amount (models/menu.py:112) | 저장됨 | emr/kos/mapper_sale_values.py:127 |
| 157 | `data[].options[].price.taxFreeAmount` | object | product_option.tax_free_amount (models/menu.py:114) | 저장됨 | emr/kos/mapper_sale_values.py:129 |
| 158 | `data[].options[].price.taxFreeAmount.currency` | enum: KRW | (통화는 amount 쪽 하나만) | 칸 없음 |  |
| 159 | `data[].options[].price.taxFreeAmount.value` | int | product_option.tax_free_amount (models/menu.py:114) | 저장됨 | emr/kos/mapper_sale_values.py:129 |
| 160 | `data[].options[].price.taxation` | string | product_option.taxation (models/menu.py:116) | 저장됨 | emr/kos/mapper_sale_values.py:130 |
| 161 | `data[].options[].price.vatAmount` | object | product_option.vat_amount (models/menu.py:113) | 저장됨 | emr/kos/mapper_sale_values.py:128 |
| 162 | `data[].options[].price.vatAmount.currency` | enum: KRW | (통화는 amount 쪽 하나만) | 칸 없음 |  |
| 163 | `data[].options[].price.vatAmount.value` | int | product_option.vat_amount (models/menu.py:113) | 저장됨 | emr/kos/mapper_sale_values.py:128 |
| 164 | `data[].options[].procedure` | object | product_option.treatment_id (models/menu.py:109) | 저장됨 | emr/kos/mapper_menu.py:128 |
| 165 | `data[].options[].procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 |
| 166 | `data[].options[].procedure.createDate` | string(empty) | join treatment (models/menu.py:213-220) | 계산으로 대체 |  |
| 167 | `data[].options[].procedure.id` | string | product_option.treatment_id (models/menu.py:109) | 저장됨 | emr/kos/mapper_menu.py:128 |
| 168 | `data[].options[].procedure.name` | string | join treatment (models/menu.py:213-220) | 계산으로 대체 |  |
| 169 | `data[].options[].promotionConfigurations[]` | array(empty) | product_option.promotions (models/menu.py:123) | 저장됨 | emr/kos/mapper_menu.py:137 — HAR 에서 늘 빈 배열 |
| 170 | `data[].options[].title` | string | product_option.title (models/menu.py:106) | 저장됨 | emr/kos/mapper_menu.py:125 |
| 171 | `data[].options[].translsMap` | object | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 172 | `data[].options[].translsMap.description` | object | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 173 | `data[].options[].translsMap.description.translation` | object / object(empty) | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 174 | `data[].options[].translsMap.description.translation.en` | string | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 175 | `data[].options[].translsMap.description.translation.ja` | string | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 176 | `data[].options[].translsMap.description.translation.ko` | string | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 177 | `data[].options[].translsMap.description.translation.zh-Hans` | string | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 178 | `data[].options[].translsMap.description.translation.zh-Hant` | string | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 179 | `data[].options[].translsMap.title` | object | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 180 | `data[].options[].translsMap.title.translation` | object / object(empty) | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 181 | `data[].options[].translsMap.title.translation.en` | string | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 182 | `data[].options[].translsMap.title.translation.ja` | string | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 183 | `data[].options[].translsMap.title.translation.ko` | string | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 184 | `data[].options[].translsMap.title.translation.zh-Hans` | string | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 185 | `data[].options[].translsMap.title.translation.zh-Hant` | string | product_option.translations (models/menu.py:124) | 저장됨 | emr/kos/mapper_menu.py:138 — JSON 통째 |
| 186 | `data[].options[].type` | enum: GROUP\|SINGLE | product_option.type (models/menu.py:105) | 저장됨 | emr/kos/mapper_menu.py:122-124 |
| 187 | `data[].order` | int | product.sort_order (models/menu.py:69) | 저장됨 | emr/kos/mapper_menu.py:166 |
| 188 | `data[].targetCountryCodes[]` | array / string | product.target_country_codes (models/menu.py:79) | 저장됨 | emr/kos/mapper_menu.py:173 |
| 189 | `data[].title` | string | product.title (models/menu.py:64) | 저장됨 | emr/kos/mapper_menu.py:160 |
| 190 | `data[].translsMap` | object | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 191 | `data[].translsMap.caution` | object | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 192 | `data[].translsMap.caution.translation` | object(empty) | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 193 | `data[].translsMap.contentImageUrl` | object | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 194 | `data[].translsMap.contentImageUrl.translation` | object(empty) | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 195 | `data[].translsMap.coverImageUrl` | object | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 196 | `data[].translsMap.coverImageUrl.translation` | object(empty) | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 197 | `data[].translsMap.description` | object | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 198 | `data[].translsMap.description.translation` | object / object(empty) | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 199 | `data[].translsMap.description.translation.en` | string | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 200 | `data[].translsMap.description.translation.ja` | string | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 201 | `data[].translsMap.description.translation.ko` | string | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 202 | `data[].translsMap.description.translation.zh-Hans` | string | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 203 | `data[].translsMap.description.translation.zh-Hant` | string | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 204 | `data[].translsMap.title` | object | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 205 | `data[].translsMap.title.translation` | object / object(empty) | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 206 | `data[].translsMap.title.translation.en` | string | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 207 | `data[].translsMap.title.translation.ja` | string | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 208 | `data[].translsMap.title.translation.ko` | string | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 209 | `data[].translsMap.title.translation.zh-Hans` | string | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |
| 210 | `data[].translsMap.title.translation.zh-Hant` | string | product.translations (models/menu.py:75) | 저장됨 | emr/kos/mapper_menu.py:172 — JSON 통째 |

### P11 `procedure-menu/v2/queries/get-procedures`

스크립트 합집합 키 **7** · 표 행 **7** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 · OQ-041-3(:1801) |
| 3 | `data[].createDate` | string(ISO UTC) | treatment.registered_at (models/menu.py:220) | 저장됨 | emr/kos/mapper_menu.py:231 |
| 4 | `data[].deleted` | bool | deleted_at · external_ref | 저장됨 | emr/kos/mapper_menu.py:226 |
| 5 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_menu.py:228 |
| 6 | `data[].name` | string | treatment.name (models/menu.py:217) | 저장됨 | emr/kos/mapper_menu.py:229 |
| 7 | `data[].searchPhoneticName` | string | treatment.search_phonetic_name (models/menu.py:219) | 저장됨 | emr/kos/mapper_menu.py:230 |

### P12 `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks`

스크립트 합집합 키 **7** · 표 행 **7** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].deleted` | bool | deleted_at · external_ref | 저장됨 | emr/kos/mapper_menu.py:252 |
| 3 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_menu.py:254 |
| 4 | `data[].title` | string | etc_task_type.title (models/menu.py:250) | 저장됨 | emr/kos/mapper_menu.py:255 |
| 5 | `data[].translsMap` | object / object(empty) |  | 칸 없음 |  |
| 6 | `data[].translsMap.title` | object |  | 칸 없음 |  |
| 7 | `data[].translsMap.title.translation` | object(empty) |  | 칸 없음 |  |

### P13 `procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product`

스크립트 합집합 키 **21** · 표 행 **21** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].balance` | object |  | 해당 없음 | 묶음 |
| 3 | `data[].balance.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 |  |
| 4 | `data[].balance.value` | int | prepaid_card_product.charge_amount (models/menu.py:262) | 저장됨 | emr/kos/mapper_menu.py:266 |
| 5 | `data[].closed` | bool | prepaid_card_product.is_closed (models/menu.py:266) | 저장됨 | emr/kos/mapper_menu.py:270 |
| 6 | `data[].description` | string | prepaid_card_product.description (models/menu.py:267) | 저장됨 | emr/kos/mapper_menu.py:271 |
| 7 | `data[].expirationDurationInDays` | int | prepaid_card_product.expiration_days (models/menu.py:264) | 저장됨 | emr/kos/mapper_menu.py:268 |
| 8 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_menu.py:262 |
| 9 | `data[].order` | int | prepaid_card_product.sort_order (models/menu.py:265) | 저장됨 | emr/kos/mapper_menu.py:269 |
| 10 | `data[].point` | object |  | 해당 없음 | 묶음 |
| 11 | `data[].point.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 |  |
| 12 | `data[].point.value` | int | prepaid_card_product.charge_point (models/menu.py:263) | 저장됨 | emr/kos/mapper_menu.py:267 |
| 13 | `data[].price` | object |  | 해당 없음 | 묶음 |
| 14 | `data[].price.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 |  |
| 15 | `data[].price.value` | int | prepaid_card_product.price_amount (models/menu.py:261) | 저장됨 | emr/kos/mapper_menu.py:265 |
| 16 | `data[].title` | string | prepaid_card_product.title (models/menu.py:260) | 저장됨 | emr/kos/mapper_menu.py:264 |
| 17 | `data[].translsMap` | object | prepaid_card_product.translations (models/menu.py:269) | 저장됨 | emr/kos/mapper_menu.py:272 — JSON 통째 |
| 18 | `data[].translsMap.description` | object | prepaid_card_product.translations (models/menu.py:269) | 저장됨 | emr/kos/mapper_menu.py:272 — JSON 통째 |
| 19 | `data[].translsMap.description.translation` | object(empty) | prepaid_card_product.translations (models/menu.py:269) | 저장됨 | emr/kos/mapper_menu.py:272 — JSON 통째 |
| 20 | `data[].translsMap.title` | object | prepaid_card_product.translations (models/menu.py:269) | 저장됨 | emr/kos/mapper_menu.py:272 — JSON 통째 |
| 21 | `data[].translsMap.title.translation` | object(empty) | prepaid_card_product.translations (models/menu.py:269) | 저장됨 | emr/kos/mapper_menu.py:272 — JSON 통째 |

### P14 `procedure-menu/etcetera-products/v1/queries/get-etcetera-products`

스크립트 합집합 키 **13** · 표 행 **13** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].category` | object | etcetera_product.etcetera_product_category_id (models/menu.py:291) | 저장됨 | emr/kos/mapper_menu.py:293-295 |
| 3 | `data[].category.category` | enum: ETCETRA_PRODUCT_CATEGORY |  | 해당 없음 | 분류 종류 상수(KOS 코드 표 이름) |
| 4 | `data[].category.closed` | bool | etcetera_product_category.is_closed (models/menu.py:281) | 저장됨 | emr/kos/mapper_menu.py:285 |
| 5 | `data[].category.id` | string(uuid) | external_ref.external_id (models/customer.py:106) · etcetera_product_category | 저장됨 | emr/kos/mapper_menu.py:281 |
| 6 | `data[].category.name` | string | etcetera_product_category.name (models/menu.py:279) | 저장됨 | emr/kos/mapper_menu.py:283 |
| 7 | `data[].category.order` | int | etcetera_product_category.sort_order (models/menu.py:280) | 저장됨 | emr/kos/mapper_menu.py:284 |
| 8 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_menu.py:292 |
| 9 | `data[].price` | object |  | 해당 없음 | 묶음 |
| 10 | `data[].price.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 |  |
| 11 | `data[].price.value` | int | etcetera_product.price_amount (models/menu.py:295) | 저장됨 | emr/kos/mapper_menu.py:297 |
| 12 | `data[].title` | string | etcetera_product.title (models/menu.py:294) | 저장됨 | emr/kos/mapper_menu.py:296 |
| 13 | `data[].translsMap` | object(empty) |  | 칸 없음 |  |

### P15 `purchase/v1/queries/get-purchase-summaries`

스크립트 합집합 키 **455** · 표 행 **455** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].assignee` | object |  | 칸 없음 | 대표 담당 — S0 OQ-08-3(:1819) 열림 |
| 3 | `data[].assignee.id` | string |  | 칸 없음 | 대표 담당 — S0 OQ-08-3(:1819) 열림 |
| 4 | `data[].assignee.name` | string / string(email꼴) |  | 칸 없음 | 대표 담당 — S0 OQ-08-3(:1819) 열림 |
| 5 | `data[].assignees[]` | array / object | purchase_assignee.staff_id (models/purchase.py:144) | 저장됨 | emr/kos/mapper_purchase.py:227-231 |
| 6 | `data[].assignees[].id` | string | purchase_assignee.staff_id (models/purchase.py:144) | 저장됨 | emr/kos/mapper_purchase.py:227-231 |
| 7 | `data[].assignees[].name` | string / string(email꼴) | join staff.name | 계산으로 대체 |  |
| 8 | `data[].createdDateTimeUtc` | string(ISO UTC) | purchase.created_at (S0:1549) | 칸 있음 · 미동기화 | 매퍼 없음 — DAY created_at 은 DAY 행 생성 시각 |
| 9 | `data[].deleted` | bool | purchase.deleted_at | 저장됨 | emr/kos/mapper_purchase.py:237 · emr/sync_purchases.py:139 |
| 10 | `data[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_purchase.py:233 |
| 11 | `data[].items[]` | array / array(empty) / object | purchase_item (models/purchase.py:66) | 저장됨 | emr/kos/mapper_purchase.py:212-217 |
| 12 | `data[].items[].adjustPriceV2` | object |  | 해당 없음 | 묶음 |
| 13 | `data[].items[].adjustPriceV2.amount` | object | purchase_item.adjusted_amount (models/purchase.py:93) | 저장됨 | emr/kos/mapper_purchase.py:155 |
| 14 | `data[].items[].adjustPriceV2.amount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 15 | `data[].items[].adjustPriceV2.amount.value` | int | purchase_item.adjusted_amount (models/purchase.py:93) | 저장됨 | emr/kos/mapper_purchase.py:155 |
| 16 | `data[].items[].adjustPriceV2.suppliedAmount` | object | purchase_item.adjusted_supplied_amount (models/purchase.py:94) | 저장됨 | emr/kos/mapper_purchase.py:156 |
| 17 | `data[].items[].adjustPriceV2.suppliedAmount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 18 | `data[].items[].adjustPriceV2.suppliedAmount.value` | int | purchase_item.adjusted_supplied_amount (models/purchase.py:94) | 저장됨 | emr/kos/mapper_purchase.py:156 |
| 19 | `data[].items[].adjustPriceV2.taxFreeAmount` | object | purchase_item.adjusted_tax_free_amount (models/purchase.py:95) | 저장됨 | emr/kos/mapper_purchase.py:157 |
| 20 | `data[].items[].adjustPriceV2.taxFreeAmount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 21 | `data[].items[].adjustPriceV2.taxFreeAmount.value` | int | purchase_item.adjusted_tax_free_amount (models/purchase.py:95) | 저장됨 | emr/kos/mapper_purchase.py:157 |
| 22 | `data[].items[].adjustPriceV2.taxation` | string | purchase_item.adjusted_taxation (models/purchase.py:97) | 저장됨 | emr/kos/mapper_purchase.py:159 |
| 23 | `data[].items[].adjustPriceV2.vatAmount` | object | purchase_item.adjusted_vat_amount (models/purchase.py:96) | 저장됨 | emr/kos/mapper_purchase.py:158 |
| 24 | `data[].items[].adjustPriceV2.vatAmount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 25 | `data[].items[].adjustPriceV2.vatAmount.value` | int | purchase_item.adjusted_vat_amount (models/purchase.py:96) | 저장됨 | emr/kos/mapper_purchase.py:158 |
| 26 | `data[].items[].adjustedPrice` | object | = purchase_item.adjusted_amount | 계산으로 대체 | S0:1568 「adjustedPrice.value」 — 코드는 adjustPriceV2 를 읽는다 |
| 27 | `data[].items[].adjustedPrice.currency` | enum: KRW | = purchase_item.adjusted_amount | 계산으로 대체 | S0:1568 「adjustedPrice.value」 — 코드는 adjustPriceV2 를 읽는다 |
| 28 | `data[].items[].adjustedPrice.value` | int | = purchase_item.adjusted_amount | 계산으로 대체 | S0:1568 「adjustedPrice.value」 — 코드는 adjustPriceV2 를 읽는다 |
| 29 | `data[].items[].basePrice` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 30 | `data[].items[].basePrice.amount` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 31 | `data[].items[].basePrice.amount.currency` | enum: KRW | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 32 | `data[].items[].basePrice.amount.value` | int | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 33 | `data[].items[].basePrice.suppliedAmount` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 34 | `data[].items[].basePrice.suppliedAmount.currency` | enum: KRW | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 35 | `data[].items[].basePrice.suppliedAmount.value` | int | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 36 | `data[].items[].basePrice.taxFreeAmount` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 37 | `data[].items[].basePrice.taxFreeAmount.currency` | enum: KRW | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 38 | `data[].items[].basePrice.taxFreeAmount.value` | int | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 39 | `data[].items[].basePrice.taxation` | string | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 40 | `data[].items[].basePrice.vatAmount` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 41 | `data[].items[].basePrice.vatAmount.currency` | enum: KRW | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 42 | `data[].items[].basePrice.vatAmount.value` | int | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 43 | `data[].items[].etceteraConfiguration` | object |  | 해당 없음 | 묶음 |
| 44 | `data[].items[].etceteraConfiguration.id` | string | purchase_item.etcetera_product_id (models/purchase.py:79) | 저장됨 | emr/kos/mapper_purchase.py:140-144 |
| 45 | `data[].items[].etceteraConfiguration.price` | object | (etcetera_product.price_amount = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷(구매 금액은 priceV2) |
| 46 | `data[].items[].etceteraConfiguration.price.currency` | enum: KRW | (etcetera_product.price_amount = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷(구매 금액은 priceV2) |
| 47 | `data[].items[].etceteraConfiguration.price.value` | int | (etcetera_product.price_amount = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷(구매 금액은 priceV2) |
| 48 | `data[].items[].etceteraConfiguration.title` | string | purchase_item.title (models/purchase.py:81) | 저장됨 | emr/kos/mapper_purchase.py:145 — 종류에 맞는 것 하나 |
| 49 | `data[].items[].etceteraConfiguration.translsMap` | object(empty) |  | 칸 없음 |  |
| 50 | `data[].items[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_purchase.py:127 |
| 51 | `data[].items[].optionConfiguration` | object |  | 해당 없음 | 묶음 |
| 52 | `data[].items[].optionConfiguration.compositions[]` | array / array(empty) / object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 53 | `data[].items[].optionConfiguration.compositions[].count` | int | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 54 | `data[].items[].optionConfiguration.compositions[].medicalService` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 55 | `data[].items[].optionConfiguration.compositions[].medicalService.caution` | string(empty) | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 56 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 57 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.code` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 58 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.healthcareReimbursement` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 59 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.machines[]` | array / object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 60 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.machines[].id` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 61 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.machines[].name` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 62 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.medicines[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 63 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.procedure` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 64 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 |
| 65 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.procedure.id` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 66 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.procedure.name` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 67 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.taxation` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 68 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.unit` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 69 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.unit.type` | enum: SHOT | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 70 | `data[].items[].optionConfiguration.compositions[].medicalService.configuration.unit.value` | number | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 71 | `data[].items[].optionConfiguration.compositions[].medicalService.deleted` | bool | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 72 | `data[].items[].optionConfiguration.compositions[].medicalService.description` | string(empty) | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 73 | `data[].items[].optionConfiguration.compositions[].medicalService.draftedDateTimeUtc` | string(ISO UTC) | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 74 | `data[].items[].optionConfiguration.compositions[].medicalService.id` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 75 | `data[].items[].optionConfiguration.compositions[].medicalService.status` | enum: PUBLISHED | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 76 | `data[].items[].optionConfiguration.compositions[].medicalService.title` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 77 | `data[].items[].optionConfiguration.compositions[].medicalService.translsMap` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 78 | `data[].items[].optionConfiguration.compositions[].medicalService.translsMap.title` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 79 | `data[].items[].optionConfiguration.compositions[].medicalService.translsMap.title.translation` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 80 | `data[].items[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.en` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 81 | `data[].items[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.ja` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 82 | `data[].items[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.ko` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 83 | `data[].items[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.zh-Hans` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 84 | `data[].items[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.zh-Hant` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 85 | `data[].items[].optionConfiguration.compositions[].medicalService.updatedDateTimeUtc` | string(ISO UTC) | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 86 | `data[].items[].optionConfiguration.compositions[].medicineAndMachines[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 87 | `data[].items[].optionConfiguration.compositions[].price` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 88 | `data[].items[].optionConfiguration.compositions[].price.additional[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 89 | `data[].items[].optionConfiguration.compositions[].price.amount` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 90 | `data[].items[].optionConfiguration.compositions[].price.amount.currency` | enum: KRW | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 91 | `data[].items[].optionConfiguration.compositions[].price.amount.value` | int | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 92 | `data[].items[].optionConfiguration.compositions[].price.suppliedAmount` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 93 | `data[].items[].optionConfiguration.compositions[].price.suppliedAmount.currency` | enum: KRW | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 94 | `data[].items[].optionConfiguration.compositions[].price.suppliedAmount.value` | int | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 95 | `data[].items[].optionConfiguration.compositions[].price.taxFreeAmount` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 96 | `data[].items[].optionConfiguration.compositions[].price.taxFreeAmount.currency` | enum: KRW | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 97 | `data[].items[].optionConfiguration.compositions[].price.taxFreeAmount.value` | int | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 98 | `data[].items[].optionConfiguration.compositions[].price.taxation` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 99 | `data[].items[].optionConfiguration.compositions[].price.vatAmount` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 100 | `data[].items[].optionConfiguration.compositions[].price.vatAmount.currency` | enum: KRW | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 101 | `data[].items[].optionConfiguration.compositions[].price.vatAmount.value` | int | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 102 | `data[].items[].optionConfiguration.compositions[].procedure` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 103 | `data[].items[].optionConfiguration.compositions[].procedure.id` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 104 | `data[].items[].optionConfiguration.compositions[].procedure.name` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 105 | `data[].items[].optionConfiguration.compositions[].unit` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 106 | `data[].items[].optionConfiguration.compositions[].unit.type` | enum: SHOT | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 107 | `data[].items[].optionConfiguration.compositions[].unit.value` | number | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 108 | `data[].items[].optionConfiguration.count` | int | purchase_item.count (models/purchase.py:85) | 저장됨 | emr/kos/mapper_purchase.py:148 |
| 109 | `data[].items[].optionConfiguration.id` | string | purchase_item.product_option_id (models/purchase.py:75) | 저장됨 | emr/kos/mapper_purchase.py:130-134 |
| 110 | `data[].items[].optionConfiguration.medicalService` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 111 | `data[].items[].optionConfiguration.medicalService.caution` | string(empty) | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 112 | `data[].items[].optionConfiguration.medicalService.configuration` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 113 | `data[].items[].optionConfiguration.medicalService.configuration.code` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 114 | `data[].items[].optionConfiguration.medicalService.configuration.healthcareReimbursement` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 115 | `data[].items[].optionConfiguration.medicalService.configuration.machines[]` | array / array(empty) / object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 116 | `data[].items[].optionConfiguration.medicalService.configuration.machines[].id` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 117 | `data[].items[].optionConfiguration.medicalService.configuration.machines[].name` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 118 | `data[].items[].optionConfiguration.medicalService.configuration.medicines[]` | array / array(empty) / object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 119 | `data[].items[].optionConfiguration.medicalService.configuration.medicines[].id` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 120 | `data[].items[].optionConfiguration.medicalService.configuration.medicines[].name` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 121 | `data[].items[].optionConfiguration.medicalService.configuration.procedure` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 122 | `data[].items[].optionConfiguration.medicalService.configuration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 |
| 123 | `data[].items[].optionConfiguration.medicalService.configuration.procedure.id` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 124 | `data[].items[].optionConfiguration.medicalService.configuration.procedure.name` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 125 | `data[].items[].optionConfiguration.medicalService.configuration.taxation` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 126 | `data[].items[].optionConfiguration.medicalService.configuration.unit` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 127 | `data[].items[].optionConfiguration.medicalService.configuration.unit.type` | enum: CC\|UNIT | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 128 | `data[].items[].optionConfiguration.medicalService.configuration.unit.value` | number | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 129 | `data[].items[].optionConfiguration.medicalService.deleted` | bool | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 130 | `data[].items[].optionConfiguration.medicalService.description` | string(empty) | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 131 | `data[].items[].optionConfiguration.medicalService.draftedDateTimeUtc` | string(ISO UTC) | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 132 | `data[].items[].optionConfiguration.medicalService.id` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 133 | `data[].items[].optionConfiguration.medicalService.status` | enum: PUBLISHED | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 134 | `data[].items[].optionConfiguration.medicalService.title` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 135 | `data[].items[].optionConfiguration.medicalService.translsMap` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 136 | `data[].items[].optionConfiguration.medicalService.translsMap.title` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 137 | `data[].items[].optionConfiguration.medicalService.translsMap.title.translation` | object / object(empty) | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 138 | `data[].items[].optionConfiguration.medicalService.translsMap.title.translation.en` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 139 | `data[].items[].optionConfiguration.medicalService.translsMap.title.translation.ja` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 140 | `data[].items[].optionConfiguration.medicalService.translsMap.title.translation.ko` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 141 | `data[].items[].optionConfiguration.medicalService.translsMap.title.translation.zh-Hans` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 142 | `data[].items[].optionConfiguration.medicalService.translsMap.title.translation.zh-Hant` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 143 | `data[].items[].optionConfiguration.medicalService.updatedDateTimeUtc` | string(ISO UTC) | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 144 | `data[].items[].optionConfiguration.medicineAndMachines[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 145 | `data[].items[].optionConfiguration.optionType` | enum: GROUP\|SINGLE | (product_option.type = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 146 | `data[].items[].optionConfiguration.price` | object | (product_option.price_amount = 지금 정가) | 칸 없음(시점 다름) | 산 시점 정가 스냅샷 |
| 147 | `data[].items[].optionConfiguration.price.currency` | enum: KRW | (product_option.price_amount = 지금 정가) | 칸 없음(시점 다름) | 산 시점 정가 스냅샷 |
| 148 | `data[].items[].optionConfiguration.price.value` | int | (product_option.price_amount = 지금 정가) | 칸 없음(시점 다름) | 산 시점 정가 스냅샷 |
| 149 | `data[].items[].optionConfiguration.procedure` | object | (treatment = 지금 값 · 항목 → 시술 참조 없음) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 150 | `data[].items[].optionConfiguration.procedure.id` | string | (treatment = 지금 값 · 항목 → 시술 참조 없음) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 151 | `data[].items[].optionConfiguration.procedure.name` | string | (treatment = 지금 값 · 항목 → 시술 참조 없음) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 152 | `data[].items[].optionConfiguration.productTitle` | string | (product.title = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 153 | `data[].items[].optionConfiguration.title` | string | purchase_item.title (models/purchase.py:81) | 저장됨 | emr/kos/mapper_purchase.py:145 — 종류에 맞는 것 하나 |
| 154 | `data[].items[].optionConfiguration.translsMap` | object |  | 칸 없음 |  |
| 155 | `data[].items[].optionConfiguration.translsMap.productTitle` | object |  | 칸 없음 |  |
| 156 | `data[].items[].optionConfiguration.translsMap.productTitle.translation` | object / object(empty) |  | 칸 없음 |  |
| 157 | `data[].items[].optionConfiguration.translsMap.productTitle.translation.en` | string |  | 칸 없음 |  |
| 158 | `data[].items[].optionConfiguration.translsMap.productTitle.translation.ja` | string |  | 칸 없음 |  |
| 159 | `data[].items[].optionConfiguration.translsMap.productTitle.translation.ko` | string |  | 칸 없음 |  |
| 160 | `data[].items[].optionConfiguration.translsMap.productTitle.translation.zh-Hans` | string |  | 칸 없음 |  |
| 161 | `data[].items[].optionConfiguration.translsMap.productTitle.translation.zh-Hant` | string |  | 칸 없음 |  |
| 162 | `data[].items[].optionConfiguration.translsMap.title` | object |  | 칸 없음 |  |
| 163 | `data[].items[].optionConfiguration.translsMap.title.translation` | object / object(empty) |  | 칸 없음 |  |
| 164 | `data[].items[].optionConfiguration.translsMap.title.translation.en` | string |  | 칸 없음 |  |
| 165 | `data[].items[].optionConfiguration.translsMap.title.translation.ja` | string |  | 칸 없음 |  |
| 166 | `data[].items[].optionConfiguration.translsMap.title.translation.ko` | string |  | 칸 없음 |  |
| 167 | `data[].items[].optionConfiguration.translsMap.title.translation.zh-Hans` | string |  | 칸 없음 |  |
| 168 | `data[].items[].optionConfiguration.translsMap.title.translation.zh-Hant` | string |  | 칸 없음 |  |
| 169 | `data[].items[].optionConfiguration.unit` | object | purchase_item.unit_type · unit_value (models/purchase.py:82-83) | 저장됨 | emr/kos/mapper_purchase.py:125 |
| 170 | `data[].items[].optionConfiguration.unit.type` | enum: CC\|UNIT | purchase_item.unit_type · unit_value (models/purchase.py:82-83) | 저장됨 | emr/kos/mapper_purchase.py:125 |
| 171 | `data[].items[].optionConfiguration.unit.value` | number | purchase_item.unit_type · unit_value (models/purchase.py:82-83) | 저장됨 | emr/kos/mapper_purchase.py:125 |
| 172 | `data[].items[].prepaidCardConfiguration` | object |  | 해당 없음 | 묶음 |
| 173 | `data[].items[].prepaidCardConfiguration.balance` | object | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 174 | `data[].items[].prepaidCardConfiguration.balance.currency` | enum: KRW | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 175 | `data[].items[].prepaidCardConfiguration.balance.value` | int | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 176 | `data[].items[].prepaidCardConfiguration.description` | string | (prepaid_card_product.* = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 177 | `data[].items[].prepaidCardConfiguration.expirationDateTimeUtc` | string(ISO UTC) | prepaid_card.expires_at (models/prepaid_card.py:40) | 계산으로 대체 | 발급된 카드 쪽 값 |
| 178 | `data[].items[].prepaidCardConfiguration.expirationDurationInDays` | int | (prepaid_card_product.* = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 179 | `data[].items[].prepaidCardConfiguration.id` | string | purchase_item.prepaid_card_product_id (models/purchase.py:76) | 저장됨 | emr/kos/mapper_purchase.py:135-139 |
| 180 | `data[].items[].prepaidCardConfiguration.point` | object | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 181 | `data[].items[].prepaidCardConfiguration.point.currency` | enum: KRW | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 182 | `data[].items[].prepaidCardConfiguration.point.value` | int | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 183 | `data[].items[].prepaidCardConfiguration.prepaidCardId` | string(uuid) | prepaid_card.purchase_item_id (models/prepaid_card.py:36) | 저장됨 | emr/kos/mapper_purchase.py:160 |
| 184 | `data[].items[].prepaidCardConfiguration.price` | object | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 185 | `data[].items[].prepaidCardConfiguration.price.currency` | enum: KRW | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 186 | `data[].items[].prepaidCardConfiguration.price.value` | int | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 187 | `data[].items[].prepaidCardConfiguration.title` | string | purchase_item.title (models/purchase.py:81) | 저장됨 | emr/kos/mapper_purchase.py:145 — 종류에 맞는 것 하나 |
| 188 | `data[].items[].prepaidCardConfiguration.translsMap` | object |  | 칸 없음 |  |
| 189 | `data[].items[].prepaidCardConfiguration.translsMap.description` | object |  | 칸 없음 |  |
| 190 | `data[].items[].prepaidCardConfiguration.translsMap.description.translation` | object(empty) |  | 칸 없음 |  |
| 191 | `data[].items[].prepaidCardConfiguration.translsMap.title` | object |  | 칸 없음 |  |
| 192 | `data[].items[].prepaidCardConfiguration.translsMap.title.translation` | object(empty) |  | 칸 없음 |  |
| 193 | `data[].items[].price` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 194 | `data[].items[].price.currency` | enum: KRW | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 195 | `data[].items[].price.value` | int | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 196 | `data[].items[].priceAdjustments[]` | array(empty) | purchase_price_adjustment.purchase_item_id (models/purchase.py:109) | 저장됨 | emr/kos/mapper_purchase.py:224-226 — 관계만 |
| 197 | `data[].items[].priceV2` | object |  | 해당 없음 | 묶음 |
| 198 | `data[].items[].priceV2.amount` | object | purchase_item.price_amount (models/purchase.py:87) | 저장됨 | emr/kos/mapper_purchase.py:149 |
| 199 | `data[].items[].priceV2.amount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 200 | `data[].items[].priceV2.amount.value` | int | purchase_item.price_amount (models/purchase.py:87) | 저장됨 | emr/kos/mapper_purchase.py:149 |
| 201 | `data[].items[].priceV2.suppliedAmount` | object | purchase_item.supplied_amount (models/purchase.py:88) | 저장됨 | emr/kos/mapper_purchase.py:150 |
| 202 | `data[].items[].priceV2.suppliedAmount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 203 | `data[].items[].priceV2.suppliedAmount.value` | int | purchase_item.supplied_amount (models/purchase.py:88) | 저장됨 | emr/kos/mapper_purchase.py:150 |
| 204 | `data[].items[].priceV2.taxFreeAmount` | object | purchase_item.tax_free_amount (models/purchase.py:89) | 저장됨 | emr/kos/mapper_purchase.py:151 |
| 205 | `data[].items[].priceV2.taxFreeAmount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 206 | `data[].items[].priceV2.taxFreeAmount.value` | int | purchase_item.tax_free_amount (models/purchase.py:89) | 저장됨 | emr/kos/mapper_purchase.py:151 |
| 207 | `data[].items[].priceV2.taxation` | string | purchase_item.taxation (models/purchase.py:91) | 저장됨 | emr/kos/mapper_purchase.py:153 |
| 208 | `data[].items[].priceV2.vatAmount` | object | purchase_item.vat_amount (models/purchase.py:90) | 저장됨 | emr/kos/mapper_purchase.py:152 |
| 209 | `data[].items[].priceV2.vatAmount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 210 | `data[].items[].priceV2.vatAmount.value` | int | purchase_item.vat_amount (models/purchase.py:90) | 저장됨 | emr/kos/mapper_purchase.py:152 |
| 211 | `data[].items[].type` | enum: ETCETRA_PRODUCT\|PREPAID_CARD_PRODUCT\|PRODUCT_OPTION | purchase_item.item_type (models/purchase.py:73) | 저장됨 | emr/kos/mapper_purchase.py:113-115 — `ETCETRA_PRODUCT` 오타 그대로 매핑 |
| 212 | `data[].lastUpdatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 저장됨 | emr/kos/mapper_purchase.py:246 · emr/sync_purchases.py:4 |
| 213 | `data[].pendingItems[]` | array / array(empty) / object | purchase_item (models/purchase.py:66) | 저장됨 | emr/kos/mapper_purchase.py:212-217 |
| 214 | `data[].pendingItems[].basePrice` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 215 | `data[].pendingItems[].basePrice.amount` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 216 | `data[].pendingItems[].basePrice.amount.currency` | enum: KRW | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 217 | `data[].pendingItems[].basePrice.amount.value` | int | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 218 | `data[].pendingItems[].basePrice.suppliedAmount` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 219 | `data[].pendingItems[].basePrice.suppliedAmount.currency` | enum: KRW | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 220 | `data[].pendingItems[].basePrice.suppliedAmount.value` | int | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 221 | `data[].pendingItems[].basePrice.taxFreeAmount` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 222 | `data[].pendingItems[].basePrice.taxFreeAmount.currency` | enum: KRW | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 223 | `data[].pendingItems[].basePrice.taxFreeAmount.value` | int | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 224 | `data[].pendingItems[].basePrice.taxation` | string | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 225 | `data[].pendingItems[].basePrice.vatAmount` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 226 | `data[].pendingItems[].basePrice.vatAmount.currency` | enum: KRW | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 227 | `data[].pendingItems[].basePrice.vatAmount.value` | int | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 228 | `data[].pendingItems[].etceteraConfiguration` | object |  | 해당 없음 | 묶음 |
| 229 | `data[].pendingItems[].etceteraConfiguration.id` | string | purchase_item.etcetera_product_id (models/purchase.py:79) | 저장됨 | emr/kos/mapper_purchase.py:140-144 |
| 230 | `data[].pendingItems[].etceteraConfiguration.price` | object | (etcetera_product.price_amount = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷(구매 금액은 priceV2) |
| 231 | `data[].pendingItems[].etceteraConfiguration.price.currency` | enum: KRW | (etcetera_product.price_amount = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷(구매 금액은 priceV2) |
| 232 | `data[].pendingItems[].etceteraConfiguration.price.value` | int | (etcetera_product.price_amount = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷(구매 금액은 priceV2) |
| 233 | `data[].pendingItems[].etceteraConfiguration.title` | string | purchase_item.title (models/purchase.py:81) | 저장됨 | emr/kos/mapper_purchase.py:145 — 종류에 맞는 것 하나 |
| 234 | `data[].pendingItems[].etceteraConfiguration.translsMap` | object(empty) |  | 칸 없음 |  |
| 235 | `data[].pendingItems[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_purchase.py:127 |
| 236 | `data[].pendingItems[].optionConfiguration` | object |  | 해당 없음 | 묶음 |
| 237 | `data[].pendingItems[].optionConfiguration.compositions[]` | array / array(empty) / object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 238 | `data[].pendingItems[].optionConfiguration.compositions[].count` | int | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 239 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 240 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.caution` | string(empty) | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 241 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 242 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.code` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 243 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.healthcareReimbursement` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 244 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.machines[]` | array / object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 245 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.machines[].id` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 246 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.machines[].name` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 247 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.medicines[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 248 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.procedure` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 249 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 |
| 250 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.procedure.id` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 251 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.procedure.name` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 252 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.taxation` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 253 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.unit` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 254 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.unit.type` | enum: SHOT | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 255 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.unit.value` | number | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 256 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.deleted` | bool | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 257 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.description` | string(empty) | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 258 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.draftedDateTimeUtc` | string(ISO UTC) | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 259 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.id` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 260 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.status` | enum: PUBLISHED | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 261 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.title` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 262 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.translsMap` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 263 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.translsMap.title` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 264 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.translsMap.title.translation` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 265 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.en` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 266 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.ja` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 267 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.ko` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 268 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.zh-Hans` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 269 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.zh-Hant` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 270 | `data[].pendingItems[].optionConfiguration.compositions[].medicalService.updatedDateTimeUtc` | string(ISO UTC) | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 271 | `data[].pendingItems[].optionConfiguration.compositions[].medicineAndMachines[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 272 | `data[].pendingItems[].optionConfiguration.compositions[].price` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 273 | `data[].pendingItems[].optionConfiguration.compositions[].price.additional[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 274 | `data[].pendingItems[].optionConfiguration.compositions[].price.amount` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 275 | `data[].pendingItems[].optionConfiguration.compositions[].price.amount.currency` | enum: KRW | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 276 | `data[].pendingItems[].optionConfiguration.compositions[].price.amount.value` | int | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 277 | `data[].pendingItems[].optionConfiguration.compositions[].price.suppliedAmount` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 278 | `data[].pendingItems[].optionConfiguration.compositions[].price.suppliedAmount.currency` | enum: KRW | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 279 | `data[].pendingItems[].optionConfiguration.compositions[].price.suppliedAmount.value` | int | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 280 | `data[].pendingItems[].optionConfiguration.compositions[].price.taxFreeAmount` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 281 | `data[].pendingItems[].optionConfiguration.compositions[].price.taxFreeAmount.currency` | enum: KRW | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 282 | `data[].pendingItems[].optionConfiguration.compositions[].price.taxFreeAmount.value` | int | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 283 | `data[].pendingItems[].optionConfiguration.compositions[].price.taxation` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 284 | `data[].pendingItems[].optionConfiguration.compositions[].price.vatAmount` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 285 | `data[].pendingItems[].optionConfiguration.compositions[].price.vatAmount.currency` | enum: KRW | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 286 | `data[].pendingItems[].optionConfiguration.compositions[].price.vatAmount.value` | int | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 287 | `data[].pendingItems[].optionConfiguration.compositions[].procedure` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 288 | `data[].pendingItems[].optionConfiguration.compositions[].procedure.id` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 289 | `data[].pendingItems[].optionConfiguration.compositions[].procedure.name` | string | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 290 | `data[].pendingItems[].optionConfiguration.compositions[].unit` | object | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 291 | `data[].pendingItems[].optionConfiguration.compositions[].unit.type` | enum: SHOT | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 292 | `data[].pendingItems[].optionConfiguration.compositions[].unit.value` | number | (product_option_composition = 지금 메뉴 구성) | 칸 없음(시점 다름) | 산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음 |
| 293 | `data[].pendingItems[].optionConfiguration.count` | int | purchase_item.count (models/purchase.py:85) | 저장됨 | emr/kos/mapper_purchase.py:148 |
| 294 | `data[].pendingItems[].optionConfiguration.id` | string | purchase_item.product_option_id (models/purchase.py:75) | 저장됨 | emr/kos/mapper_purchase.py:130-134 |
| 295 | `data[].pendingItems[].optionConfiguration.medicalService` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 296 | `data[].pendingItems[].optionConfiguration.medicalService.caution` | string(empty) | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 297 | `data[].pendingItems[].optionConfiguration.medicalService.configuration` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 298 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.code` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 299 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.healthcareReimbursement` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 300 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.machines[]` | array / array(empty) / object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 301 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.machines[].id` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 302 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.machines[].name` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 303 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.medicines[]` | array / array(empty) / object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 304 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.medicines[].id` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 305 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.medicines[].name` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 306 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.procedure` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 307 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 |
| 308 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.procedure.id` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 309 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.procedure.name` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 310 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.taxation` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 311 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.unit` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 312 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.unit.type` | enum: UNIT | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 313 | `data[].pendingItems[].optionConfiguration.medicalService.configuration.unit.value` | number | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 314 | `data[].pendingItems[].optionConfiguration.medicalService.deleted` | bool | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 315 | `data[].pendingItems[].optionConfiguration.medicalService.description` | string(empty) | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 316 | `data[].pendingItems[].optionConfiguration.medicalService.draftedDateTimeUtc` | string(ISO UTC) | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 317 | `data[].pendingItems[].optionConfiguration.medicalService.id` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 318 | `data[].pendingItems[].optionConfiguration.medicalService.status` | enum: PUBLISHED | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 319 | `data[].pendingItems[].optionConfiguration.medicalService.title` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 320 | `data[].pendingItems[].optionConfiguration.medicalService.translsMap` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 321 | `data[].pendingItems[].optionConfiguration.medicalService.translsMap.title` | object | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 322 | `data[].pendingItems[].optionConfiguration.medicalService.translsMap.title.translation` | object / object(empty) | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 323 | `data[].pendingItems[].optionConfiguration.medicalService.translsMap.title.translation.en` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 324 | `data[].pendingItems[].optionConfiguration.medicalService.translsMap.title.translation.ja` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 325 | `data[].pendingItems[].optionConfiguration.medicalService.translsMap.title.translation.ko` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 326 | `data[].pendingItems[].optionConfiguration.medicalService.translsMap.title.translation.zh-Hans` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 327 | `data[].pendingItems[].optionConfiguration.medicalService.translsMap.title.translation.zh-Hant` | string | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 328 | `data[].pendingItems[].optionConfiguration.medicalService.updatedDateTimeUtc` | string(ISO UTC) | (treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷(SINGLE 옵션) |
| 329 | `data[].pendingItems[].optionConfiguration.medicineAndMachines[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 330 | `data[].pendingItems[].optionConfiguration.optionType` | enum: GROUP\|SINGLE | (product_option.type = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 331 | `data[].pendingItems[].optionConfiguration.price` | object | (product_option.price_amount = 지금 정가) | 칸 없음(시점 다름) | 산 시점 정가 스냅샷 |
| 332 | `data[].pendingItems[].optionConfiguration.price.currency` | enum: KRW | (product_option.price_amount = 지금 정가) | 칸 없음(시점 다름) | 산 시점 정가 스냅샷 |
| 333 | `data[].pendingItems[].optionConfiguration.price.value` | int | (product_option.price_amount = 지금 정가) | 칸 없음(시점 다름) | 산 시점 정가 스냅샷 |
| 334 | `data[].pendingItems[].optionConfiguration.procedure` | object | (treatment = 지금 값 · 항목 → 시술 참조 없음) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 335 | `data[].pendingItems[].optionConfiguration.procedure.id` | string | (treatment = 지금 값 · 항목 → 시술 참조 없음) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 336 | `data[].pendingItems[].optionConfiguration.procedure.name` | string | (treatment = 지금 값 · 항목 → 시술 참조 없음) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 337 | `data[].pendingItems[].optionConfiguration.productTitle` | string | (product.title = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 338 | `data[].pendingItems[].optionConfiguration.title` | string | purchase_item.title (models/purchase.py:81) | 저장됨 | emr/kos/mapper_purchase.py:145 — 종류에 맞는 것 하나 |
| 339 | `data[].pendingItems[].optionConfiguration.translsMap` | object |  | 칸 없음 |  |
| 340 | `data[].pendingItems[].optionConfiguration.translsMap.productTitle` | object |  | 칸 없음 |  |
| 341 | `data[].pendingItems[].optionConfiguration.translsMap.productTitle.translation` | object / object(empty) |  | 칸 없음 |  |
| 342 | `data[].pendingItems[].optionConfiguration.translsMap.productTitle.translation.en` | string |  | 칸 없음 |  |
| 343 | `data[].pendingItems[].optionConfiguration.translsMap.productTitle.translation.ja` | string |  | 칸 없음 |  |
| 344 | `data[].pendingItems[].optionConfiguration.translsMap.productTitle.translation.ko` | string |  | 칸 없음 |  |
| 345 | `data[].pendingItems[].optionConfiguration.translsMap.productTitle.translation.zh-Hans` | string |  | 칸 없음 |  |
| 346 | `data[].pendingItems[].optionConfiguration.translsMap.productTitle.translation.zh-Hant` | string |  | 칸 없음 |  |
| 347 | `data[].pendingItems[].optionConfiguration.translsMap.title` | object |  | 칸 없음 |  |
| 348 | `data[].pendingItems[].optionConfiguration.translsMap.title.translation` | object / object(empty) |  | 칸 없음 |  |
| 349 | `data[].pendingItems[].optionConfiguration.translsMap.title.translation.en` | string |  | 칸 없음 |  |
| 350 | `data[].pendingItems[].optionConfiguration.translsMap.title.translation.ja` | string |  | 칸 없음 |  |
| 351 | `data[].pendingItems[].optionConfiguration.translsMap.title.translation.ko` | string |  | 칸 없음 |  |
| 352 | `data[].pendingItems[].optionConfiguration.translsMap.title.translation.zh-Hans` | string |  | 칸 없음 |  |
| 353 | `data[].pendingItems[].optionConfiguration.translsMap.title.translation.zh-Hant` | string |  | 칸 없음 |  |
| 354 | `data[].pendingItems[].optionConfiguration.unit` | object | purchase_item.unit_type · unit_value (models/purchase.py:82-83) | 저장됨 | emr/kos/mapper_purchase.py:125 |
| 355 | `data[].pendingItems[].optionConfiguration.unit.type` | enum: UNIT | purchase_item.unit_type · unit_value (models/purchase.py:82-83) | 저장됨 | emr/kos/mapper_purchase.py:125 |
| 356 | `data[].pendingItems[].optionConfiguration.unit.value` | number | purchase_item.unit_type · unit_value (models/purchase.py:82-83) | 저장됨 | emr/kos/mapper_purchase.py:125 |
| 357 | `data[].pendingItems[].prepaidCardConfiguration` | object |  | 해당 없음 | 묶음 |
| 358 | `data[].pendingItems[].prepaidCardConfiguration.balance` | object | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 359 | `data[].pendingItems[].prepaidCardConfiguration.balance.currency` | enum: KRW | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 360 | `data[].pendingItems[].prepaidCardConfiguration.balance.value` | int | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 361 | `data[].pendingItems[].prepaidCardConfiguration.description` | string | (prepaid_card_product.* = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 362 | `data[].pendingItems[].prepaidCardConfiguration.expirationDateTimeUtc` | string(ISO UTC) | prepaid_card.expires_at (models/prepaid_card.py:40) | 계산으로 대체 | 발급된 카드 쪽 값 |
| 363 | `data[].pendingItems[].prepaidCardConfiguration.expirationDurationInDays` | int | (prepaid_card_product.* = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 364 | `data[].pendingItems[].prepaidCardConfiguration.id` | string | purchase_item.prepaid_card_product_id (models/purchase.py:76) | 저장됨 | emr/kos/mapper_purchase.py:135-139 |
| 365 | `data[].pendingItems[].prepaidCardConfiguration.point` | object | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 366 | `data[].pendingItems[].prepaidCardConfiguration.point.currency` | enum: KRW | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 367 | `data[].pendingItems[].prepaidCardConfiguration.point.value` | int | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 368 | `data[].pendingItems[].prepaidCardConfiguration.prepaidCardId` | string(uuid) | prepaid_card.purchase_item_id (models/prepaid_card.py:36) | 저장됨 | emr/kos/mapper_purchase.py:160 |
| 369 | `data[].pendingItems[].prepaidCardConfiguration.price` | object | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 370 | `data[].pendingItems[].prepaidCardConfiguration.price.currency` | enum: KRW | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 371 | `data[].pendingItems[].prepaidCardConfiguration.price.value` | int | (prepaid_card_product.* = 지금 상품 값) | 칸 없음(시점 다름) | 산 시점 상품 스냅샷 |
| 372 | `data[].pendingItems[].prepaidCardConfiguration.title` | string | purchase_item.title (models/purchase.py:81) | 저장됨 | emr/kos/mapper_purchase.py:145 — 종류에 맞는 것 하나 |
| 373 | `data[].pendingItems[].prepaidCardConfiguration.translsMap` | object |  | 칸 없음 |  |
| 374 | `data[].pendingItems[].prepaidCardConfiguration.translsMap.description` | object |  | 칸 없음 |  |
| 375 | `data[].pendingItems[].prepaidCardConfiguration.translsMap.description.translation` | object(empty) |  | 칸 없음 |  |
| 376 | `data[].pendingItems[].prepaidCardConfiguration.translsMap.title` | object |  | 칸 없음 |  |
| 377 | `data[].pendingItems[].prepaidCardConfiguration.translsMap.title.translation` | object(empty) |  | 칸 없음 |  |
| 378 | `data[].pendingItems[].price` | object | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 379 | `data[].pendingItems[].price.currency` | enum: KRW | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 380 | `data[].pendingItems[].price.value` | int | = purchase_item.price_amount | 계산으로 대체 | S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음 |
| 381 | `data[].pendingItems[].priceAdjustments[]` | array(empty) | purchase_price_adjustment.purchase_item_id (models/purchase.py:109) | 저장됨 | emr/kos/mapper_purchase.py:224-226 — 관계만 |
| 382 | `data[].pendingItems[].priceV2` | object |  | 해당 없음 | 묶음 |
| 383 | `data[].pendingItems[].priceV2.amount` | object | purchase_item.price_amount (models/purchase.py:87) | 저장됨 | emr/kos/mapper_purchase.py:149 |
| 384 | `data[].pendingItems[].priceV2.amount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 385 | `data[].pendingItems[].priceV2.amount.value` | int | purchase_item.price_amount (models/purchase.py:87) | 저장됨 | emr/kos/mapper_purchase.py:149 |
| 386 | `data[].pendingItems[].priceV2.suppliedAmount` | object | purchase_item.supplied_amount (models/purchase.py:88) | 저장됨 | emr/kos/mapper_purchase.py:150 |
| 387 | `data[].pendingItems[].priceV2.suppliedAmount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 388 | `data[].pendingItems[].priceV2.suppliedAmount.value` | int | purchase_item.supplied_amount (models/purchase.py:88) | 저장됨 | emr/kos/mapper_purchase.py:150 |
| 389 | `data[].pendingItems[].priceV2.taxFreeAmount` | object | purchase_item.tax_free_amount (models/purchase.py:89) | 저장됨 | emr/kos/mapper_purchase.py:151 |
| 390 | `data[].pendingItems[].priceV2.taxFreeAmount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 391 | `data[].pendingItems[].priceV2.taxFreeAmount.value` | int | purchase_item.tax_free_amount (models/purchase.py:89) | 저장됨 | emr/kos/mapper_purchase.py:151 |
| 392 | `data[].pendingItems[].priceV2.taxation` | string | purchase_item.taxation (models/purchase.py:91) | 저장됨 | emr/kos/mapper_purchase.py:153 |
| 393 | `data[].pendingItems[].priceV2.vatAmount` | object | purchase_item.vat_amount (models/purchase.py:90) | 저장됨 | emr/kos/mapper_purchase.py:152 |
| 394 | `data[].pendingItems[].priceV2.vatAmount.currency` | enum: KRW | (구매 항목 통화 칸 없음) | 칸 없음 |  |
| 395 | `data[].pendingItems[].priceV2.vatAmount.value` | int | purchase_item.vat_amount (models/purchase.py:90) | 저장됨 | emr/kos/mapper_purchase.py:152 |
| 396 | `data[].pendingItems[].type` | enum: ETCETRA_PRODUCT\|PREPAID_CARD_PRODUCT\|PRODUCT_OPTION | purchase_item.item_type (models/purchase.py:73) | 저장됨 | emr/kos/mapper_purchase.py:113-115 — `ETCETRA_PRODUCT` 오타 그대로 매핑 |
| 397 | `data[].priceAdjustments[]` | array(empty) | purchase_price_adjustment (models/purchase.py:103) · 항목 없음 | 저장됨 | emr/kos/mapper_purchase.py:221-223 — 관계만 |
| 398 | `data[].process` | string | purchase.process (models/purchase.py:60) | 저장됨 | emr/kos/mapper_purchase.py:242-245 |
| 399 | `data[].refundingItems[]` | array / array(empty) / object | purchase_item.adjusted_* (models/purchase.py:93-97) | 칸 있음 · 미동기화 | S0:1568 「진행 중 refundingItems[].adjustedPrice.amount」 · 매퍼 없음 |
| 400 | `data[].refundingItems[].adjustedPrice` | object | purchase_item.adjusted_* (models/purchase.py:93-97) | 칸 있음 · 미동기화 | S0:1568 · 매퍼 없음 |
| 401 | `data[].refundingItems[].adjustedPrice.amount` | object | purchase_item.adjusted_* (models/purchase.py:93-97) | 칸 있음 · 미동기화 | S0:1568 · 매퍼 없음 |
| 402 | `data[].refundingItems[].adjustedPrice.amount.currency` | enum: KRW |  | 칸 없음 |  |
| 403 | `data[].refundingItems[].adjustedPrice.amount.value` | int | purchase_item.adjusted_* (models/purchase.py:93-97) | 칸 있음 · 미동기화 | S0:1568 · 매퍼 없음 |
| 404 | `data[].refundingItems[].adjustedPrice.suppliedAmount` | object | purchase_item.adjusted_* (models/purchase.py:93-97) | 칸 있음 · 미동기화 | S0:1568 · 매퍼 없음 |
| 405 | `data[].refundingItems[].adjustedPrice.suppliedAmount.currency` | enum: KRW |  | 칸 없음 |  |
| 406 | `data[].refundingItems[].adjustedPrice.suppliedAmount.value` | int | purchase_item.adjusted_* (models/purchase.py:93-97) | 칸 있음 · 미동기화 | S0:1568 · 매퍼 없음 |
| 407 | `data[].refundingItems[].adjustedPrice.taxFreeAmount` | object | purchase_item.adjusted_* (models/purchase.py:93-97) | 칸 있음 · 미동기화 | S0:1568 · 매퍼 없음 |
| 408 | `data[].refundingItems[].adjustedPrice.taxFreeAmount.currency` | enum: KRW |  | 칸 없음 |  |
| 409 | `data[].refundingItems[].adjustedPrice.taxFreeAmount.value` | int | purchase_item.adjusted_* (models/purchase.py:93-97) | 칸 있음 · 미동기화 | S0:1568 · 매퍼 없음 |
| 410 | `data[].refundingItems[].adjustedPrice.taxation` | string | purchase_item.adjusted_* (models/purchase.py:93-97) | 칸 있음 · 미동기화 | S0:1568 · 매퍼 없음 |
| 411 | `data[].refundingItems[].adjustedPrice.vatAmount` | object | purchase_item.adjusted_* (models/purchase.py:93-97) | 칸 있음 · 미동기화 | S0:1568 · 매퍼 없음 |
| 412 | `data[].refundingItems[].adjustedPrice.vatAmount.currency` | enum: KRW |  | 칸 없음 |  |
| 413 | `data[].refundingItems[].adjustedPrice.vatAmount.value` | int | purchase_item.adjusted_* (models/purchase.py:93-97) | 칸 있음 · 미동기화 | S0:1568 · 매퍼 없음 |
| 414 | `data[].refundingItems[].targetItemId` | string(uuid) | (대상 purchase_item) | 칸 있음 · 미동기화 | S0:1568 · 매퍼 없음 |
| 415 | `data[].revokingItems[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 · S0 OQ-08-8(:1815) |
| 416 | `data[].status` | enum: ACCEPTED\|INITIALIZED\|PARTIALLY_REFUNDED\|REFUNDED | purchase.status (models/purchase.py:59) | 저장됨 | emr/kos/mapper_purchase.py:238-241 |
| 417 | `data[].transactions[]` | array / array(empty) / object | purchase_transaction (models/purchase.py:115) | 저장됨 | emr/kos/mapper_purchase.py:218-220 |
| 418 | `data[].transactions[].assignee` | object | purchase_transaction.staff_id (models/purchase.py:132) | 저장됨 | emr/kos/mapper_purchase.py:185 |
| 419 | `data[].transactions[].assignee.id` | string | purchase_transaction.staff_id (models/purchase.py:132) | 저장됨 | emr/kos/mapper_purchase.py:185 |
| 420 | `data[].transactions[].assignee.name` | string / string(email꼴) | join staff.name | 계산으로 대체 |  |
| 421 | `data[].transactions[].canceledRefId` | string(empty) / string(uuid) | purchase_transaction.canceled_transaction_id (models/purchase.py:125) | 저장됨 | emr/kos/mapper_purchase.py:179-181 |
| 422 | `data[].transactions[].cardConfiguration` | object / object(empty) | purchase_transaction.payment_config (models/purchase.py:130) | 저장됨 | emr/kos/mapper_purchase.py:169 · 183 · emr/kos/mapper_sale_values.py:68-76 · 156-160 — `…Id` 키만 빼고 JSON |
| 423 | `data[].transactions[].cardConfiguration.approvalNumber` | string | purchase_transaction.payment_config (models/purchase.py:130) | 저장됨 | emr/kos/mapper_purchase.py:169 · 183 · emr/kos/mapper_sale_values.py:68-76 · 156-160 — `…Id` 키만 빼고 JSON |
| 424 | `data[].transactions[].cardConfiguration.cardCompany` | object | purchase_transaction.payment_config (models/purchase.py:130) | 저장됨 | emr/kos/mapper_purchase.py:169 · 183 · emr/kos/mapper_sale_values.py:68-76 · 156-160 — `…Id` 키만 빼고 JSON |
| 425 | `data[].transactions[].cardConfiguration.cardCompany.name` | string | purchase_transaction.payment_config (models/purchase.py:130) | 저장됨 | emr/kos/mapper_purchase.py:169 · 183 · emr/kos/mapper_sale_values.py:68-76 · 156-160 — `…Id` 키만 빼고 JSON |
| 426 | `data[].transactions[].cashConfiguration` | object(empty) | purchase_transaction.payment_config (models/purchase.py:130) | 저장됨 | emr/kos/mapper_purchase.py:169 · 183 · emr/kos/mapper_sale_values.py:68-76 · 156-160 — `…Id` 키만 빼고 JSON |
| 427 | `data[].transactions[].createdDateTimeUtc` | string(ISO UTC) | purchase_transaction.created_at (S0:1601) | 칸 있음 · 미동기화 | 매퍼 없음 |
| 428 | `data[].transactions[].easyPayConfiguration` | object(empty) | purchase_transaction.payment_config (models/purchase.py:130) | 저장됨 | emr/kos/mapper_purchase.py:169 · 183 · emr/kos/mapper_sale_values.py:68-76 · 156-160 — `…Id` 키만 빼고 JSON |
| 429 | `data[].transactions[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_purchase.py:172 |
| 430 | `data[].transactions[].medicalLoanConfiguration` | object(empty) | purchase_transaction.payment_config (models/purchase.py:130) | 저장됨 | emr/kos/mapper_purchase.py:169 · 183 · emr/kos/mapper_sale_values.py:68-76 · 156-160 — `…Id` 키만 빼고 JSON |
| 431 | `data[].transactions[].paymentDateTime` | object |  | 칸 없음 | 승인 · 취소 시각 — S0 OQ-08-5(a)(:1821) 열림 |
| 432 | `data[].transactions[].paymentDateTime.approvedDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 승인 · 취소 시각 — S0 OQ-08-5(a)(:1821) 열림 |
| 433 | `data[].transactions[].paymentDateTime.canceledDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 승인 · 취소 시각 — S0 OQ-08-5(a)(:1821) 열림 |
| 434 | `data[].transactions[].paymentDateTime.lastUpdatedDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 승인 · 취소 시각 — S0 OQ-08-5(a)(:1821) 열림 |
| 435 | `data[].transactions[].paymentType` | enum: CARD\|CASH\|PREPAID_CARD\|TRANSFER | purchase_transaction.payment_type (models/purchase.py:128) | 저장됨 | emr/kos/mapper_purchase.py:165-168 — **HAR 의 `CARD` 는 매핑 표(emr/kos/mapper_sale_values.py:48-52) 밖 → 그 거래 행이 빠진다**(K5) |
| 436 | `data[].transactions[].platformConfiguration` | object(empty) | purchase_transaction.payment_config (models/purchase.py:130) | 저장됨 | emr/kos/mapper_purchase.py:169 · 183 · emr/kos/mapper_sale_values.py:68-76 · 156-160 — `…Id` 키만 빼고 JSON |
| 437 | `data[].transactions[].prepaidCardConfiguration` | object | purchase_transaction.payment_config (models/purchase.py:130) | 저장됨 | emr/kos/mapper_purchase.py:169-170 |
| 438 | `data[].transactions[].prepaidCardConfiguration.chargingId` | string(empty) / string(uuid) | prepaid_card_ledger.purchase_transaction_id (models/prepaid_card.py:67) | 저장됨 | emr/kos/mapper_purchase.py:186-188 |
| 439 | `data[].transactions[].prepaidCardConfiguration.prepaidCardId` | string(empty) / string(uuid) | purchase_transaction.prepaid_card_id (models/purchase.py:131) | 저장됨 | emr/kos/mapper_purchase.py:184 |
| 440 | `data[].transactions[].prepaidCardConfiguration.prepaidCardName` | string / string(empty) | purchase_transaction.payment_config (models/purchase.py:130) | 저장됨 | emr/kos/mapper_sale_values.py:156-160 — JSON 안 |
| 441 | `data[].transactions[].price` | object | purchase_transaction.amount (models/purchase.py:121) | 저장됨 | emr/kos/mapper_purchase.py:173-174 — 부호 있는 금액 |
| 442 | `data[].transactions[].price.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 |  |
| 443 | `data[].transactions[].price.value` | int | purchase_transaction.amount (models/purchase.py:121) | 저장됨 | emr/kos/mapper_purchase.py:173-174 — 부호 있는 금액 |
| 444 | `data[].transactions[].status` | enum: APPROVED\|CANCELED | purchase_transaction.status (models/purchase.py:122) | 저장됨 | emr/kos/mapper_purchase.py:175-178 |
| 445 | `data[].transactions[].suppliedAmount` | object |  | 칸 없음 | 금액 분해 — S0 OQ-08-5(a) 열림 |
| 446 | `data[].transactions[].suppliedAmount.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 |  |
| 447 | `data[].transactions[].suppliedAmount.value` | int |  | 칸 없음 | 금액 분해 — S0 OQ-08-5(a) 열림 |
| 448 | `data[].transactions[].taxFreeAmount` | object |  | 칸 없음 | 금액 분해 — S0 OQ-08-5(a) 열림 |
| 449 | `data[].transactions[].taxFreeAmount.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 |  |
| 450 | `data[].transactions[].taxFreeAmount.value` | int |  | 칸 없음 | 금액 분해 — S0 OQ-08-5(a) 열림 |
| 451 | `data[].transactions[].transferConfiguration` | object(empty) | purchase_transaction.payment_config (models/purchase.py:130) | 저장됨 | emr/kos/mapper_purchase.py:169 · 183 · emr/kos/mapper_sale_values.py:68-76 · 156-160 — `…Id` 키만 빼고 JSON |
| 452 | `data[].transactions[].vatAmount` | object |  | 칸 없음 | 금액 분해 — S0 OQ-08-5(a) 열림 |
| 453 | `data[].transactions[].vatAmount.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 |  |
| 454 | `data[].transactions[].vatAmount.value` | int |  | 칸 없음 | 금액 분해 — S0 OQ-08-5(a) 열림 |
| 455 | `data[].visitorId` | string | purchase.customer_id (models/purchase.py:57) | 저장됨 | emr/kos/mapper_purchase.py:234-236 |

### P16 `ticket/v1/queries/get-ticket-bundles`

스크립트 합집합 키 **116** · 표 행 **116** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].optionConfiguration` | object |  | 해당 없음 | 묶음 |
| 3 | `data[].optionConfiguration.optionId` | string | purchase_item.product_option_id (models/purchase.py:75) | 계산으로 대체 | 번들 → 구매 항목 |
| 4 | `data[].optionConfiguration.optionTitle` | string | ≈ purchase_item.title (models/purchase.py:81) | 계산으로 대체 | 같은 값인지 확인 안 됨(앞 판 E2 `optionTitle`) |
| 5 | `data[].optionConfiguration.productTitle` | string | (product.title = 지금 값) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 6 | `data[].optionConfiguration.promotionConfiguration` | object(empty) |  | 칸 없음 |  |
| 7 | `data[].optionConfiguration.translsMap` | object |  | 칸 없음 |  |
| 8 | `data[].optionConfiguration.translsMap.optionTitle` | object / object(empty) |  | 칸 없음 |  |
| 9 | `data[].optionConfiguration.translsMap.optionTitle.translation` | object |  | 칸 없음 |  |
| 10 | `data[].optionConfiguration.translsMap.optionTitle.translation.en` | string |  | 칸 없음 |  |
| 11 | `data[].optionConfiguration.translsMap.optionTitle.translation.ja` | string |  | 칸 없음 |  |
| 12 | `data[].optionConfiguration.translsMap.optionTitle.translation.ko` | string |  | 칸 없음 |  |
| 13 | `data[].optionConfiguration.translsMap.optionTitle.translation.zh-Hans` | string |  | 칸 없음 |  |
| 14 | `data[].optionConfiguration.translsMap.optionTitle.translation.zh-Hant` | string |  | 칸 없음 |  |
| 15 | `data[].optionConfiguration.translsMap.productTitle` | object / object(empty) |  | 칸 없음 |  |
| 16 | `data[].optionConfiguration.translsMap.productTitle.translation` | object |  | 칸 없음 |  |
| 17 | `data[].optionConfiguration.translsMap.productTitle.translation.en` | string |  | 칸 없음 |  |
| 18 | `data[].optionConfiguration.translsMap.productTitle.translation.ja` | string |  | 칸 없음 |  |
| 19 | `data[].optionConfiguration.translsMap.productTitle.translation.ko` | string |  | 칸 없음 |  |
| 20 | `data[].optionConfiguration.translsMap.productTitle.translation.zh-Hans` | string |  | 칸 없음 |  |
| 21 | `data[].optionConfiguration.translsMap.productTitle.translation.zh-Hant` | string |  | 칸 없음 |  |
| 22 | `data[].price` | object |  | 해당 없음 | 묶음 |
| 23 | `data[].price.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 | 앞 판 E2 |
| 24 | `data[].price.value` | number | ticket_bundle.price_amount (models/ticket.py:40) | 저장됨 | emr/kos/mapper_purchase.py:300 |
| 25 | `data[].purchaseId` | string(uuid) | purchase_item.purchase_id (models/purchase.py:72) | 계산으로 대체 | 번들 → 구매 항목 → 구매 |
| 26 | `data[].purchaseItemId` | string(uuid) | ticket_bundle.purchase_item_id (models/ticket.py:37) + external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_purchase.py:295-298 |
| 27 | `data[].ticketSets[]` | array / object | ticket_set (models/ticket.py:46) | 저장됨 | emr/kos/mapper_purchase.py:301 |
| 28 | `data[].ticketSets[].medicalService` | object | ticket_set.treatment_item_id (models/ticket.py:50) | 저장됨 | emr/kos/mapper_purchase.py:282-284 |
| 29 | `data[].ticketSets[].medicalService.caution` | string(empty) | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 30 | `data[].ticketSets[].medicalService.configuration` | object | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 31 | `data[].ticketSets[].medicalService.configuration.code` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 32 | `data[].ticketSets[].medicalService.configuration.healthcareReimbursement` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 33 | `data[].ticketSets[].medicalService.configuration.machines[]` | array / object | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 34 | `data[].ticketSets[].medicalService.configuration.machines[].id` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 35 | `data[].ticketSets[].medicalService.configuration.machines[].name` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 36 | `data[].ticketSets[].medicalService.configuration.medicines[]` | array / object | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 37 | `data[].ticketSets[].medicalService.configuration.medicines[].id` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 38 | `data[].ticketSets[].medicalService.configuration.medicines[].name` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 39 | `data[].ticketSets[].medicalService.configuration.procedure` | object | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 40 | `data[].ticketSets[].medicalService.configuration.procedure.id` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 41 | `data[].ticketSets[].medicalService.configuration.procedure.name` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 42 | `data[].ticketSets[].medicalService.configuration.taxation` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 43 | `data[].ticketSets[].medicalService.configuration.unit` | object | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 44 | `data[].ticketSets[].medicalService.configuration.unit.type` | enum: CC\|MINUTE\|QUANTITY\|SHOT\|UNIT | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 45 | `data[].ticketSets[].medicalService.configuration.unit.value` | number | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 46 | `data[].ticketSets[].medicalService.description` | string(empty) | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 47 | `data[].ticketSets[].medicalService.draftedDateTimeUtc` | string(ISO UTC) | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 48 | `data[].ticketSets[].medicalService.id` | string | ticket_set.treatment_item_id (models/ticket.py:50) | 저장됨 | emr/kos/mapper_purchase.py:282-284 |
| 49 | `data[].ticketSets[].medicalService.status` | enum: PUBLISHED | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 50 | `data[].ticketSets[].medicalService.title` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 51 | `data[].ticketSets[].medicalService.translsMap` | object | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 52 | `data[].ticketSets[].medicalService.translsMap.title` | object / object(empty) | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 53 | `data[].ticketSets[].medicalService.translsMap.title.translation` | object | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 54 | `data[].ticketSets[].medicalService.translsMap.title.translation.en` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 55 | `data[].ticketSets[].medicalService.translsMap.title.translation.ja` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 56 | `data[].ticketSets[].medicalService.translsMap.title.translation.ko` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 57 | `data[].ticketSets[].medicalService.translsMap.title.translation.zh-Hans` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 58 | `data[].ticketSets[].medicalService.translsMap.title.translation.zh-Hant` | string | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 59 | `data[].ticketSets[].medicalService.updatedDateTimeUtc` | string(ISO UTC) | (treatment_item.* = 지금 메뉴 값) | 칸 없음(시점 다름) | 산 시점 시술 항목 스냅샷 |
| 60 | `data[].ticketSets[].procedure` | object | (treatment = 지금 값 · 세트 → 시술 참조 없음) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 61 | `data[].ticketSets[].procedure.id` | string | (treatment = 지금 값 · 세트 → 시술 참조 없음) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 62 | `data[].ticketSets[].procedure.name` | string | (treatment = 지금 값 · 세트 → 시술 참조 없음) | 칸 없음(시점 다름) | 산 시점 스냅샷 |
| 63 | `data[].ticketSets[].ticketGroupId` | string | external_ref.external_id (models/customer.py:106) · ticket_set | 저장됨 | emr/kos/mapper_purchase.py:281 |
| 64 | `data[].ticketSets[].tickets[]` | array / object | ticket (models/ticket.py:61) | 저장됨 | emr/kos/mapper_purchase.py:271-278 |
| 65 | `data[].ticketSets[].tickets[].createdDateTimeUtc` | string(ISO UTC) | ticket.created_at (S0:1665) | 칸 있음 · 미동기화 | 매퍼 없음 · 앞 판 E2 `purchasedDate` · M10 |
| 66 | `data[].ticketSets[].tickets[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_purchase.py:260 |
| 67 | `data[].ticketSets[].tickets[].price` | object |  | 일부러 안 둠 | S0:1626 · 1668 「KOS 티켓 price 는 받지 않는다(번들 ÷ 회차)」 · customer-erd-spec-brief.md:37 |
| 68 | `data[].ticketSets[].tickets[].price.currency` | enum: KRW |  | 일부러 안 둠 | S0:1626 · 1668 「KOS 티켓 price 는 받지 않는다(번들 ÷ 회차)」 · customer-erd-spec-brief.md:37 |
| 69 | `data[].ticketSets[].tickets[].price.value` | number |  | 일부러 안 둠 | S0:1626 · 1668 「KOS 티켓 price 는 받지 않는다(번들 ÷ 회차)」 · customer-erd-spec-brief.md:37 |
| 70 | `data[].ticketSets[].tickets[].status` | enum: AVAILABLE\|IN_USE\|USED | ticket.status (models/ticket.py:65) | 저장됨 | emr/kos/mapper_purchase.py:261-264 |
| 71 | `data[].ticketSets[].title` | string | ticket_set.title (models/ticket.py:51) | 저장됨 | emr/kos/mapper_purchase.py:285 |
| 72 | `data[].ticketSets[].translsMap` | object |  | 칸 없음 |  |
| 73 | `data[].ticketSets[].translsMap.title` | object |  | 칸 없음 |  |
| 74 | `data[].ticketSets[].translsMap.title.translation` | object |  | 칸 없음 |  |
| 75 | `data[].ticketSets[].translsMap.title.translation.de` | string |  | 칸 없음 |  |
| 76 | `data[].ticketSets[].translsMap.title.translation.en` | string |  | 칸 없음 |  |
| 77 | `data[].ticketSets[].translsMap.title.translation.es` | string |  | 칸 없음 |  |
| 78 | `data[].ticketSets[].translsMap.title.translation.fr` | string |  | 칸 없음 |  |
| 79 | `data[].ticketSets[].translsMap.title.translation.id` | string |  | 칸 없음 |  |
| 80 | `data[].ticketSets[].translsMap.title.translation.ja` | string |  | 칸 없음 |  |
| 81 | `data[].ticketSets[].translsMap.title.translation.ko` | string |  | 칸 없음 |  |
| 82 | `data[].ticketSets[].translsMap.title.translation.mn` | string |  | 칸 없음 |  |
| 83 | `data[].ticketSets[].translsMap.title.translation.ms` | string |  | 칸 없음 |  |
| 84 | `data[].ticketSets[].translsMap.title.translation.nl` | string |  | 칸 없음 |  |
| 85 | `data[].ticketSets[].translsMap.title.translation.pt` | string |  | 칸 없음 |  |
| 86 | `data[].ticketSets[].translsMap.title.translation.ru` | string |  | 칸 없음 |  |
| 87 | `data[].ticketSets[].translsMap.title.translation.th` | string |  | 칸 없음 |  |
| 88 | `data[].ticketSets[].translsMap.title.translation.uz` | string |  | 칸 없음 |  |
| 89 | `data[].ticketSets[].translsMap.title.translation.vi` | string |  | 칸 없음 |  |
| 90 | `data[].ticketSets[].translsMap.title.translation.zh-Hans` | string |  | 칸 없음 |  |
| 91 | `data[].ticketSets[].translsMap.title.translation.zh-Hant` | string |  | 칸 없음 |  |
| 92 | `data[].ticketSets[].unit` | object / object(empty) | ticket_set.unit_type · unit_value (models/ticket.py:52 · 55) | 저장됨 | emr/kos/mapper_purchase.py:279 |
| 93 | `data[].ticketSets[].unit.type` | enum: CC\|MINUTE\|QUANTITY\|SHOT\|UNIT | ticket_set.unit_type · unit_value (models/ticket.py:52 · 55) | 저장됨 | emr/kos/mapper_purchase.py:279 |
| 94 | `data[].ticketSets[].unit.value` | number | ticket_set.unit_type · unit_value (models/ticket.py:52 · 55) | 저장됨 | emr/kos/mapper_purchase.py:279 |
| 95 | `data[].title` | string | ticket_bundle.title (models/ticket.py:38) | 저장됨 | emr/kos/mapper_purchase.py:299 |
| 96 | `data[].translsMap` | object |  | 칸 없음 |  |
| 97 | `data[].translsMap.title` | object / object(empty) |  | 칸 없음 |  |
| 98 | `data[].translsMap.title.translation` | object |  | 칸 없음 |  |
| 99 | `data[].translsMap.title.translation.de` | string |  | 칸 없음 |  |
| 100 | `data[].translsMap.title.translation.en` | string |  | 칸 없음 |  |
| 101 | `data[].translsMap.title.translation.es` | string |  | 칸 없음 |  |
| 102 | `data[].translsMap.title.translation.fr` | string |  | 칸 없음 |  |
| 103 | `data[].translsMap.title.translation.id` | string |  | 칸 없음 |  |
| 104 | `data[].translsMap.title.translation.ja` | string |  | 칸 없음 |  |
| 105 | `data[].translsMap.title.translation.ko` | string |  | 칸 없음 |  |
| 106 | `data[].translsMap.title.translation.mn` | string |  | 칸 없음 |  |
| 107 | `data[].translsMap.title.translation.ms` | string |  | 칸 없음 |  |
| 108 | `data[].translsMap.title.translation.nl` | string |  | 칸 없음 |  |
| 109 | `data[].translsMap.title.translation.pt` | string |  | 칸 없음 |  |
| 110 | `data[].translsMap.title.translation.ru` | string |  | 칸 없음 |  |
| 111 | `data[].translsMap.title.translation.th` | string |  | 칸 없음 |  |
| 112 | `data[].translsMap.title.translation.uz` | string |  | 칸 없음 |  |
| 113 | `data[].translsMap.title.translation.vi` | string |  | 칸 없음 |  |
| 114 | `data[].translsMap.title.translation.zh-Hans` | string |  | 칸 없음 |  |
| 115 | `data[].translsMap.title.translation.zh-Hant` | string |  | 칸 없음 |  |
| 116 | `data[].visitorId` | string | ticket_bundle.customer_id (models/ticket.py:36) | 저장됨 | emr/kos/sale_reads.py:260-275(요청 고객) |

### P17 `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries`

스크립트 합집합 키 **23** · 표 행 **23** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / array(empty) / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].createdDateTimeUtc` | string(ISO UTC) | prepaid_card.created_at (S0:1695) | 칸 있음 · 미동기화 | 매퍼 없음 · 앞 판 E2 `issuedDate` |
| 3 | `data[].description` | string / string(empty) |  | 칸 없음 |  |
| 4 | `data[].expirationDateTimeUtc` | string(ISO UTC) | prepaid_card.expires_at (models/prepaid_card.py:40) | 저장됨 | emr/kos/mapper_purchase.py:321 |
| 5 | `data[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper_purchase.py:310 |
| 6 | `data[].ownerId` | string | prepaid_card.customer_id (models/prepaid_card.py:35) | 저장됨 | emr/kos/mapper_purchase.py:311-313 |
| 7 | `data[].remainingBalance` | object |  | 해당 없음 | 묶음 |
| 8 | `data[].remainingBalance.balance` | object | prepaid_card.balance_amount (models/prepaid_card.py:38) | 저장됨 | emr/kos/mapper_purchase.py:315-317 |
| 9 | `data[].remainingBalance.balance.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 |  |
| 10 | `data[].remainingBalance.balance.value` | int | prepaid_card.balance_amount (models/prepaid_card.py:38) | 저장됨 | emr/kos/mapper_purchase.py:315-317 |
| 11 | `data[].remainingBalance.total` | object |  | 일부러 안 둠 | S0:1698 「total 은 받지 않는다(이력에서 계산)」 · customer-erd-spec-brief.md:37 |
| 12 | `data[].remainingBalance.total.currency` | enum: KRW |  | 일부러 안 둠 | S0:1698 「total 은 받지 않는다(이력에서 계산)」 · customer-erd-spec-brief.md:37 |
| 13 | `data[].remainingBalance.total.value` | int |  | 일부러 안 둠 | S0:1698 「total 은 받지 않는다(이력에서 계산)」 · customer-erd-spec-brief.md:37 |
| 14 | `data[].remainingPoint` | object / object(empty) |  | 해당 없음 | 묶음 |
| 15 | `data[].remainingPoint.balance` | object | prepaid_card.point_balance (models/prepaid_card.py:39) | 저장됨 | emr/kos/mapper_purchase.py:318-320 |
| 16 | `data[].remainingPoint.balance.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 |  |
| 17 | `data[].remainingPoint.balance.value` | int | prepaid_card.point_balance (models/prepaid_card.py:39) | 저장됨 | emr/kos/mapper_purchase.py:318-320 |
| 18 | `data[].remainingPoint.total` | object |  | 일부러 안 둠 | S0:1698 「total 은 받지 않는다(이력에서 계산)」 · customer-erd-spec-brief.md:37 |
| 19 | `data[].remainingPoint.total.currency` | enum: KRW |  | 일부러 안 둠 | S0:1698 「total 은 받지 않는다(이력에서 계산)」 · customer-erd-spec-brief.md:37 |
| 20 | `data[].remainingPoint.total.value` | int |  | 일부러 안 둠 | S0:1698 「total 은 받지 않는다(이력에서 계산)」 · customer-erd-spec-brief.md:37 |
| 21 | `data[].title` | string | prepaid_card.title (models/prepaid_card.py:37) | 저장됨 | emr/kos/mapper_purchase.py:314 |
| 22 | `data[].translsMap` | object(empty) |  | 칸 없음 |  |
| 23 | `data[].updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 저장됨 | emr/kos/mapper_purchase.py:322 · emr/sync_tickets.py:206 |

### P18 `purchase/prepaid-card/v1/queries/get-prepaid-card-charging-events`

스크립트 합집합 키 **15** · 표 행 **15** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].amount` | object |  | 해당 없음 | 묶음 |
| 3 | `data[].amount.amount` | object |  | 해당 없음 | 묶음 |
| 4 | `data[].amount.amount.currency` | enum: KRW | (통화 칸 없음) | 칸 없음 |  |
| 5 | `data[].amount.amount.value` | int | prepaid_card_ledger.amount (models/prepaid_card.py:64) | 저장됨 | emr/kos/mapper_purchase.py:350 |
| 6 | `data[].amount.type` | enum: POINT | prepaid_card_ledger.pocket (models/prepaid_card.py:63) | 저장됨 | emr/kos/mapper_purchase.py:336-341 |
| 7 | `data[].chargingId` | string(uuid) | external_ref.external_id (models/customer.py:106) (`chargingId:주머니`) | 저장됨 | emr/kos/mapper_purchase.py:326-343 |
| 8 | `data[].createdDateTimeUtc` | string(ISO UTC) | prepaid_card_ledger.occurred_at (models/prepaid_card.py:72) | 저장됨 | emr/kos/mapper_purchase.py:355 |
| 9 | `data[].memo` | string / string(empty) | prepaid_card_ledger.memo (models/prepaid_card.py:71) | 저장됨 | emr/kos/mapper_purchase.py:354 |
| 10 | `data[].type` | enum: CHARGE\|PAYMENT | prepaid_card_ledger.kind (models/prepaid_card.py:62) | 저장됨 | emr/kos/mapper_purchase.py:345-348 |
| 11 | `data[].visitor` | object |  | 해당 없음 | 묶음 |
| 12 | `data[].visitor.chartNumber` | string(digits) | join customer | 계산으로 대체 |  |
| 13 | `data[].visitor.name` | string | join customer | 계산으로 대체 |  |
| 14 | `data[].visitor.owner` | bool | prepaid_card.customer_id 와 견줌 | 계산으로 대체 |  |
| 15 | `data[].visitor.visitorId` | string | prepaid_card_ledger.customer_id (models/prepaid_card.py:66) | 저장됨 | emr/kos/mapper_purchase.py:351-353 |

### P19 `purchase/prepaid-card/v1/queries/get-prepaid-card-visitors`

스크립트 합집합 키 **5** · 표 행 **5** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].chartNumber` | string(digits) | join customer | 계산으로 대체 |  |
| 3 | `data[].name` | string | join customer | 계산으로 대체 |  |
| 4 | `data[].owner` | bool | (소유자 = prepaid_card.customer_id · 아니면 prepaid_card_customer) | 저장됨 | emr/kos/mapper_purchase.py:363 |
| 5 | `data[].visitorId` | string | prepaid_card_customer.customer_id (models/prepaid_card.py:52) | 저장됨 | emr/kos/mapper_purchase.py:359-364 · emr/kos/sale_reads.py:299-307(소유자 아닌 고객만) |

### P20 `visitor/v2/queries/get-visitors`

스크립트 합집합 키 **64** · 표 행 **64** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `count` | int |  | 해당 없음 | 전체 수 — 백필 페이지(emr/kos/sale_reads.py:327) |
| 2 | `data[]` | array / object |  | 해당 없음 | 목록 — DAY 는 이 경로에서 **id 만** 읽는다(emr/kos/sale_reads.py:316-333) |
| 3 | `data[].address` | object |  | 해당 없음 | 묶음 |
| 4 | `data[].address.address` | string / string(digits) / string(empty) | customer.address (models/customer.py:66) | 칸 있음 · 미동기화 |  |
| 5 | `data[].address.detailedAddress` | string / string(empty) | customer.address_detail (models/customer.py:67) | 칸 있음 · 미동기화 |  |
| 6 | `data[].address.zipCode` | string(empty) | customer.zip_code (models/customer.py:68) | 칸 있음 · 미동기화 |  |
| 7 | `data[].aggrementAdvertisements` | bool | customer.agreed_marketing (models/customer.py:84) | 칸 있음 · 미동기화 | S0:355 |
| 8 | `data[].aggrementPersonalInformation` | bool | customer.agreed_personal_info (models/customer.py:83) | 칸 있음 · 미동기화 | S0:355 |
| 9 | `data[].agreementInformationalNotification` | bool | customer.agreed_informational (models/customer.py:85) | 칸 있음 · 미동기화 | S0:355 |
| 10 | `data[].chartNumber` | string(digits) | customer.chart_number (models/customer.py:43) | 저장됨 | emr/kos/mapper.py:308 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 11 | `data[].counselor` | object | customer.assigned_counselor_id (models/customer.py:75) | 칸 있음 · 미동기화 | S0:350 |
| 12 | `data[].counselor.id` | string / string(empty) | customer.assigned_counselor_id (models/customer.py:75) | 칸 있음 · 미동기화 | S0:350 |
| 13 | `data[].counselor.name` | string / string(empty) | join staff.name | 계산으로 대체 |  |
| 14 | `data[].createdDateTimeUtc` | string(ISO UTC) | customer.registered_at (models/customer.py:44) | 칸 있음 · 미동기화 | S0:330 · 매퍼 없음 |
| 15 | `data[].customAttributes[]` | array(empty) |  | 일부러 안 둠 | S0:312 반려(`custom_attributes` · 명동점 정의 0개) |
| 16 | `data[].dateOfBirth` | string / string(empty) | customer.birth_date (models/customer.py:52) | 저장됨 | emr/kos/mapper.py:312 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 17 | `data[].deleted` | bool | customer.deleted_at (S0:331) | 칸 있음 · 미동기화 | 매퍼 없음 |
| 18 | `data[].detailedFunnel` | string(empty) |  | 칸 없음 | S0:414 「옛 칸」(결정 없음) |
| 19 | `data[].doctor` | object | customer.assigned_doctor_id (models/customer.py:74) | 칸 있음 · 미동기화 | S0:350 |
| 20 | `data[].doctor.id` | string(empty) | customer.assigned_doctor_id (models/customer.py:74) | 칸 있음 · 미동기화 | S0:350 |
| 21 | `data[].doctor.name` | string(empty) | join staff.name | 계산으로 대체 |  |
| 22 | `data[].email` | string(email꼴) / string(empty) | customer.email (models/customer.py:65) | 칸 있음 · 미동기화 | 앞 판 B1 · C1 |
| 23 | `data[].foreignRegistrationNumber` | string(empty) | customer.foreign_registration_number (models/customer.py:57) | 칸 있음 · 미동기화 | **암호화 대상**(data_rules) |
| 24 | `data[].funnel` | string(empty) / string(uuid) |  | 칸 없음 | S0:414 「옛 칸」(결정 없음) |
| 25 | `data[].gender` | enum: FEMALE\|GENDER_UNSPECIFIED\|MALE | customer.gender (models/customer.py:51) | 저장됨 | emr/kos/mapper.py:311 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 26 | `data[].id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:307 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 27 | `data[].isNew` | bool | (visit.is_new — 방문마다) | 일부러 안 둠 | S0:301 · 360 「is_new → 3번 방문」 · 앞 판 M4 |
| 28 | `data[].language` | string / string(empty) / enum: en\|ja\|ko\|mn\|th\|vi\|zh\|zh-CN | customer.language (models/customer.py:54) | 칸 있음 · 미동기화 | 앞 판 B1 |
| 29 | `data[].lastVisitedDateTimeUtc` | string(ISO UTC) / string(empty) | max(visit.*) — S0:360 「방문 기록에서 계산」 | 계산으로 대체 | KOS 정의(예약 · 접수 · 완료) 확인 안 됨 — 앞 판 M9 · 과거 방문은 백필 범위만 |
| 30 | `data[].lineInformation[]` | array(empty) |  | 일부러 안 둠 | S0:312 · 314-317 |
| 31 | `data[].memo` | string / string(empty) | customer.customer_notes (models/customer.py:72) | 저장됨 | emr/kos/mapper.py:316 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 32 | `data[].migratedMemo` | string(empty) |  | 일부러 안 둠 | S0:311 반려(`legacy_notes`) |
| 33 | `data[].name` | string | customer.name (models/customer.py:46) | 저장됨 | emr/kos/mapper.py:309 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 34 | `data[].nationality` | string | customer.nationality (models/customer.py:53) | 저장됨 | emr/kos/mapper.py:313 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 35 | `data[].passportExpiryDate` | string(empty) | customer.passport_expiry_date (models/customer.py:59) | 칸 있음 · 미동기화 |  |
| 36 | `data[].passportGivenNames` | string / string(empty) | customer.passport_given_names (models/customer.py:49) | 칸 있음 · 미동기화 |  |
| 37 | `data[].passportNumber` | string(empty) | customer.passport_number (models/customer.py:58) | 칸 있음 · 미동기화 | **암호화 대상**(data_rules) |
| 38 | `data[].passportSurname` | string / string(empty) | customer.passport_surname (models/customer.py:48) | 칸 있음 · 미동기화 |  |
| 39 | `data[].phoneNumber` | object |  | 해당 없음 | 묶음 |
| 40 | `data[].phoneNumber.countryCode` | string(digits) | customer.phone_country_code (models/customer.py:61) | 저장됨 | emr/kos/mapper.py:314(일정 visitor `phone.countryCode`) — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 41 | `data[].phoneNumber.phoneNumber` | string(digits) | customer.phone_number (models/customer.py:62) | 저장됨 | emr/kos/mapper.py:315(일정 visitor `phone.phoneNumber`) — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 42 | `data[].phoneticName` | string / string(empty) | customer.name_pronunciation (models/customer.py:47) | 저장됨 | emr/kos/mapper.py:310 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 43 | `data[].recommenderName` | string(empty) | customer.referrer_name (models/customer.py:81) | 칸 있음 · 미동기화 | S0:354 |
| 44 | `data[].registrationNumber` | string(empty) / string(숫자·기호) | customer.registration_number (models/customer.py:56) | 칸 있음 · 미동기화 | **암호화 대상**(data_rules) |
| 45 | `data[].snsInfo` | object |  | 해당 없음 | 묶음 |
| 46 | `data[].snsInfo.accountId` | string / string(digits) / string(empty) | customer.sns_account_id (models/customer.py:70) | 저장됨 | emr/kos/mapper.py:318 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 47 | `data[].snsInfo.snsType` | string | customer.sns_type (models/customer.py:69) | 저장됨 | emr/kos/mapper.py:317 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 48 | `data[].unniInformation[]` | array(empty) |  | 일부러 안 둠 | S0:311 · 317 |
| 49 | `data[].unregistered` | object |  | 칸 없음 |  |
| 50 | `data[].unregistered.name` | string(empty) |  | 칸 없음 |  |
| 51 | `data[].updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 칸 있음 · 미동기화 | 고객은 external_number 만 씀(emr/sync_schedules.py:150) |
| 52 | `data[].visitorCategories[]` | array / array(empty) / object | customer_category_link (models/customer.py:157) | 저장됨 | emr/kos/mapper.py:322-327(일정 visitor `categories[]`) — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 53 | `data[].visitorCategories[].color` | string | join customer_category (models/customer.py:124-131) | 계산으로 대체 |  |
| 54 | `data[].visitorCategories[].id` | string(uuid) | customer_category_link (models/customer.py:157) | 저장됨 | emr/kos/mapper.py:322-327(일정 visitor `categories[]`) — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 55 | `data[].visitorCategories[].name` | string | join customer_category (models/customer.py:124-131) | 계산으로 대체 |  |
| 56 | `data[].visitorCategories[].order` | int | join customer_category (models/customer.py:124-131) | 계산으로 대체 |  |
| 57 | `data[].visitorCategoryId` | string(empty) |  | 칸 없음 | S0:413 에 키만 있음(결정 없음) |
| 58 | `data[].visitorFunnel` | object |  | 해당 없음 | 묶음 |
| 59 | `data[].visitorFunnel.funnelCategoryId` | string(empty) | join funnel.category_id (models/customer.py:149) | 계산으로 대체 |  |
| 60 | `data[].visitorFunnel.funnelDetail` | string(empty) | customer.funnel_detail (models/customer.py:78) | 칸 있음 · 미동기화 | S0:352 |
| 61 | `data[].visitorFunnel.funnelId` | string(empty) / string(uuid) | customer.funnel_id (models/customer.py:77) | 칸 있음 · 미동기화 | S0:351 |
| 62 | `data[].visitorType` | object | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 63 | `data[].visitorType.id` | string / string(empty) | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 64 | `data[].visitorType.name` | string / string(empty) | customer_type.name (models/customer.py:120) | 저장됨 | emr/kos/mapper.py:319-321 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |

### P21 `v1/account/queries/get-user-account`

스크립트 합집합 키 **11** · 표 행 **11** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data` | object |  | 해당 없음 | 묶음 |
| 2 | `data.email` | string(email꼴) | staff.email (models/staff.py:53) | 저장됨 | emr/kos/mapper.py:660 · services/auth_membership.py:75 · 84-85 |
| 3 | `data.id` | string | external_ref.external_id (models/customer.py:106) · staff | 저장됨 | emr/kos/mapper.py:658 · services/auth_membership.py:65 |
| 4 | `data.mfaMethods[]` | array(empty) |  | 칸 없음 | 로그인 막는 판정에만(services/auth.py:523) |
| 5 | `data.name` | string(email꼴) | staff.name (models/staff.py:51) | 저장됨 | emr/kos/mapper.py:659 · services/auth_membership.py:74 · 83 |
| 6 | `data.role` | object | staff.job_role_id (models/staff.py:55) + external_ref.external_id (models/customer.py:106) · job_role | 저장됨 | emr/kos/mapper.py:646-652 · services/auth_membership.py:26 |
| 7 | `data.role.featureList[]` | array(empty) |  | 일부러 안 둠 | S0:611 |
| 8 | `data.role.id` | string | staff.job_role_id (models/staff.py:55) + external_ref.external_id (models/customer.py:106) · job_role | 저장됨 | emr/kos/mapper.py:646-652 · services/auth_membership.py:26 |
| 9 | `data.role.isDefault` | bool | job_role.is_default (models/staff.py:70) | 저장됨 | services/auth_membership.py:42-43 |
| 10 | `data.role.name` | string | job_role.name (models/staff.py:68) | 저장됨 | services/auth_membership.py:30 |
| 11 | `data.role.roleTags[]` | array / int | job_role.tags (models/staff.py:69) | 저장됨 | services/auth_membership.py:31 |

### P22 `common/v1/tenant/queries/get-user-tenants`

스크립트 합집합 키 **8** · 표 행 **8** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | 응답 껍데기 · 목록 |
| 2 | `data[].hospitalCode` | string(digits) |  | 칸 없음 | KOS 테넌트 정보 |
| 3 | `data[].hospitalId` | string |  | 칸 없음 | KOS 테넌트 정보 |
| 4 | `data[].hospitalName` | string | (hospital.name = DAY 가 정한 이름 models/hospital.py:46) | 칸 없음(시점 다름) | emr/kos/mapper.py:632 — 병원 고르기 표시에만 · 앞 판 E12 `name` |
| 5 | `data[].hospitalNationality` | string |  | 칸 없음 | KOS 테넌트 정보 |
| 6 | `data[].id` | string | crm_connection 테넌트 매칭 · external_session.external_tenant_id (models/staff.py:110) | 저장됨 | emr/kos/mapper.py:631 · services/auth.py:273-276 |
| 7 | `data[].mode` | int |  | 칸 없음 | KOS 테넌트 정보 |
| 8 | `data[].namespace` | string |  | 칸 없음 | KOS 테넌트 정보 |

### P23 `common/user/v1/queries/get-active-sign-ins`

HAR 에 응답 없음 → 키 대조 불가 · **K5** 「확인 안 됨」.

### P24 `visitor/v2/queries/get-visitor`

스크립트 합집합 키 **63** · 표 행 **63** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data` | object |  | 해당 없음 | DAY 는 이 경로를 부르지 않음 |
| 2 | `data.address` | object |  | 해당 없음 | 묶음 |
| 3 | `data.address.address` | string / string(empty) | customer.address (models/customer.py:66) | 칸 있음 · 미동기화 |  |
| 4 | `data.address.detailedAddress` | string / string(empty) | customer.address_detail (models/customer.py:67) | 칸 있음 · 미동기화 |  |
| 5 | `data.address.zipCode` | string(empty) | customer.zip_code (models/customer.py:68) | 칸 있음 · 미동기화 |  |
| 6 | `data.aggrementAdvertisements` | bool | customer.agreed_marketing (models/customer.py:84) | 칸 있음 · 미동기화 | S0:355 |
| 7 | `data.aggrementPersonalInformation` | bool | customer.agreed_personal_info (models/customer.py:83) | 칸 있음 · 미동기화 | S0:355 |
| 8 | `data.agreementInformationalNotification` | bool | customer.agreed_informational (models/customer.py:85) | 칸 있음 · 미동기화 | S0:355 |
| 9 | `data.chartNumber` | string(digits) | customer.chart_number (models/customer.py:43) | 저장됨 | emr/kos/mapper.py:308 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 10 | `data.counselor` | object | customer.assigned_counselor_id (models/customer.py:75) | 칸 있음 · 미동기화 | S0:350 |
| 11 | `data.counselor.id` | string(empty) | customer.assigned_counselor_id (models/customer.py:75) | 칸 있음 · 미동기화 | S0:350 |
| 12 | `data.counselor.name` | string(empty) | join staff.name | 계산으로 대체 |  |
| 13 | `data.createdDateTimeUtc` | string(ISO UTC) | customer.registered_at (models/customer.py:44) | 칸 있음 · 미동기화 | S0:330 · 매퍼 없음 |
| 14 | `data.customAttributes[]` | array(empty) |  | 일부러 안 둠 | S0:312 반려(`custom_attributes` · 명동점 정의 0개) |
| 15 | `data.dateOfBirth` | string / string(empty) | customer.birth_date (models/customer.py:52) | 저장됨 | emr/kos/mapper.py:312 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 16 | `data.deleted` | bool | customer.deleted_at (S0:331) | 칸 있음 · 미동기화 | 매퍼 없음 |
| 17 | `data.detailedFunnel` | string(empty) |  | 칸 없음 | S0:414 「옛 칸」(결정 없음) |
| 18 | `data.doctor` | object | customer.assigned_doctor_id (models/customer.py:74) | 칸 있음 · 미동기화 | S0:350 |
| 19 | `data.doctor.id` | string(empty) | customer.assigned_doctor_id (models/customer.py:74) | 칸 있음 · 미동기화 | S0:350 |
| 20 | `data.doctor.name` | string(empty) | join staff.name | 계산으로 대체 |  |
| 21 | `data.email` | string(empty) | customer.email (models/customer.py:65) | 칸 있음 · 미동기화 | 앞 판 B1 · C1 |
| 22 | `data.foreignRegistrationNumber` | string(empty) | customer.foreign_registration_number (models/customer.py:57) | 칸 있음 · 미동기화 | **암호화 대상**(data_rules) |
| 23 | `data.funnel` | string(empty) / string(uuid) |  | 칸 없음 | S0:414 「옛 칸」(결정 없음) |
| 24 | `data.gender` | enum: FEMALE\|GENDER_UNSPECIFIED\|MALE | customer.gender (models/customer.py:51) | 저장됨 | emr/kos/mapper.py:311 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 25 | `data.id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:307 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 26 | `data.isNew` | bool | (visit.is_new — 방문마다) | 일부러 안 둠 | S0:301 · 360 「is_new → 3번 방문」 · 앞 판 M4 |
| 27 | `data.language` | string / string(empty) / enum: en\|ko\|zh\|zh-CN | customer.language (models/customer.py:54) | 칸 있음 · 미동기화 | 앞 판 B1 |
| 28 | `data.lastVisitedDateTimeUtc` | string(ISO UTC) / string(empty) | max(visit.*) — S0:360 「방문 기록에서 계산」 | 계산으로 대체 | KOS 정의(예약 · 접수 · 완료) 확인 안 됨 — 앞 판 M9 · 과거 방문은 백필 범위만 |
| 29 | `data.lineInformation[]` | array(empty) |  | 일부러 안 둠 | S0:312 · 314-317 |
| 30 | `data.memo` | string / string(empty) | customer.customer_notes (models/customer.py:72) | 저장됨 | emr/kos/mapper.py:316 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 31 | `data.migratedMemo` | string(empty) |  | 일부러 안 둠 | S0:311 반려(`legacy_notes`) |
| 32 | `data.name` | string | customer.name (models/customer.py:46) | 저장됨 | emr/kos/mapper.py:309 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 33 | `data.nationality` | string | customer.nationality (models/customer.py:53) | 저장됨 | emr/kos/mapper.py:313 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 34 | `data.passportExpiryDate` | string(empty) | customer.passport_expiry_date (models/customer.py:59) | 칸 있음 · 미동기화 |  |
| 35 | `data.passportGivenNames` | string(empty) | customer.passport_given_names (models/customer.py:49) | 칸 있음 · 미동기화 |  |
| 36 | `data.passportNumber` | string(digits) / string(empty) | customer.passport_number (models/customer.py:58) | 칸 있음 · 미동기화 | **암호화 대상**(data_rules) |
| 37 | `data.passportSurname` | string / string(empty) | customer.passport_surname (models/customer.py:48) | 칸 있음 · 미동기화 |  |
| 38 | `data.phoneNumber` | object |  | 해당 없음 | 묶음 |
| 39 | `data.phoneNumber.countryCode` | string(digits) | customer.phone_country_code (models/customer.py:61) | 저장됨 | emr/kos/mapper.py:314(일정 visitor `phone.countryCode`) — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 40 | `data.phoneNumber.phoneNumber` | string(digits) | customer.phone_number (models/customer.py:62) | 저장됨 | emr/kos/mapper.py:315(일정 visitor `phone.phoneNumber`) — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 41 | `data.phoneticName` | string / string(empty) | customer.name_pronunciation (models/customer.py:47) | 저장됨 | emr/kos/mapper.py:310 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 42 | `data.recommenderName` | string(empty) | customer.referrer_name (models/customer.py:81) | 칸 있음 · 미동기화 | S0:354 |
| 43 | `data.registrationNumber` | string(empty) / string(숫자·기호) | customer.registration_number (models/customer.py:56) | 칸 있음 · 미동기화 | **암호화 대상**(data_rules) |
| 44 | `data.snsInfo` | object |  | 해당 없음 | 묶음 |
| 45 | `data.snsInfo.accountId` | string / string(empty) | customer.sns_account_id (models/customer.py:70) | 저장됨 | emr/kos/mapper.py:318 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 46 | `data.snsInfo.snsType` | string | customer.sns_type (models/customer.py:69) | 저장됨 | emr/kos/mapper.py:317 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 47 | `data.unniInformation[]` | array(empty) |  | 일부러 안 둠 | S0:311 · 317 |
| 48 | `data.unregistered` | object |  | 칸 없음 |  |
| 49 | `data.unregistered.name` | string(empty) |  | 칸 없음 |  |
| 50 | `data.updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 칸 있음 · 미동기화 | 고객은 external_number 만 씀(emr/sync_schedules.py:150) |
| 51 | `data.visitorCategories[]` | array / array(empty) / object | customer_category_link (models/customer.py:157) | 저장됨 | emr/kos/mapper.py:322-327(일정 visitor `categories[]`) — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 52 | `data.visitorCategories[].color` | string | join customer_category (models/customer.py:124-131) | 계산으로 대체 |  |
| 53 | `data.visitorCategories[].id` | string(uuid) | customer_category_link (models/customer.py:157) | 저장됨 | emr/kos/mapper.py:322-327(일정 visitor `categories[]`) — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 54 | `data.visitorCategories[].name` | string | join customer_category (models/customer.py:124-131) | 계산으로 대체 |  |
| 55 | `data.visitorCategories[].order` | int | join customer_category (models/customer.py:124-131) | 계산으로 대체 |  |
| 56 | `data.visitorCategoryId` | string(empty) |  | 칸 없음 | S0:413 에 키만 있음(결정 없음) |
| 57 | `data.visitorFunnel` | object |  | 해당 없음 | 묶음 |
| 58 | `data.visitorFunnel.funnelCategoryId` | string(empty) | join funnel.category_id (models/customer.py:149) | 계산으로 대체 |  |
| 59 | `data.visitorFunnel.funnelDetail` | string(empty) | customer.funnel_detail (models/customer.py:78) | 칸 있음 · 미동기화 | S0:352 |
| 60 | `data.visitorFunnel.funnelId` | string(empty) / string(uuid) | customer.funnel_id (models/customer.py:77) | 칸 있음 · 미동기화 | S0:351 |
| 61 | `data.visitorType` | object | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 62 | `data.visitorType.id` | string / string(empty) | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 63 | `data.visitorType.name` | string / string(empty) | customer_type.name (models/customer.py:120) | 저장됨 | emr/kos/mapper.py:319-321 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |

### P25 `v1/hospital/queries/get-hospital`

스크립트 합집합 키 **22** · 표 행 **22** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data` | object |  | 해당 없음 | DAY 는 이 경로를 부르지 않음 |
| 2 | `data.addressContract` | object |  | 일부러 안 둠 | S0:278 |
| 3 | `data.addressContract.address` | string(empty) |  | 일부러 안 둠 | S0:278 |
| 4 | `data.addressContract.detailedAddress` | string(empty) |  | 일부러 안 둠 | S0:278 |
| 5 | `data.addressContract.translsMap` | object(empty) |  | 일부러 안 둠 | S0:278 |
| 6 | `data.addressContract.zipCode` | string(empty) |  | 일부러 안 둠 | S0:278 |
| 7 | `data.businessLicenseImageUrl` | string(empty) |  | 칸 없음 | KOS 병원 설정 |
| 8 | `data.companyName` | string(empty) |  | 칸 없음 | KOS 병원 설정 |
| 9 | `data.companyRegistrationNumber` | string(empty) |  | 칸 없음 | KOS 병원 설정 |
| 10 | `data.hospitalMapImageUrl` | string(empty) |  | 칸 없음 | KOS 병원 설정 |
| 11 | `data.hospitalName` | string | (hospital.name = DAY 가 정한 이름 models/hospital.py:46) | 칸 없음(시점 다름) | 앞 판 E12 |
| 12 | `data.hospitalPhoneNumber` | string(empty) |  | 일부러 안 둠 | S0:278 「hospital 의 phone · address 는 두지 않는다」 — 앞 판 E12 · C14 와 충돌(K6) |
| 13 | `data.languages[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 14 | `data.logoImageUrl` | string(empty) |  | 칸 없음 | KOS 병원 설정 |
| 15 | `data.nationality` | string |  | 칸 없음 | KOS 병원 설정 |
| 16 | `data.nursingInstitutionNumber` | string(digits) |  | 칸 없음 | KOS 병원 설정 |
| 17 | `data.qualifiedInvoiceIssuerNumber` | string(empty) |  | 칸 없음 | KOS 병원 설정 |
| 18 | `data.representativeName` | string(empty) |  | 칸 없음 | KOS 병원 설정 |
| 19 | `data.representativeStampImageUrl` | string(empty) |  | 칸 없음 | KOS 병원 설정 |
| 20 | `data.taxBillEmail` | string(empty) |  | 칸 없음 | KOS 병원 설정 |
| 21 | `data.translsMap` | object(empty) |  | 칸 없음 | KOS 병원 설정 |
| 22 | `data.websiteUrl` | string(empty) |  | 칸 없음 | KOS 병원 설정 |

### P26 `schedule/default-operation-time/v1/queries/get-default-operation-timetable`

스크립트 합집합 키 **50** · 표 행 **50** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data` | object |  | 해당 없음 | DAY 는 이 경로를 부르지 않음 |
| 2 | `data.friday` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 3 | `data.friday.breaktime` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 4 | `data.friday.breaktime.endTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 5 | `data.friday.breaktime.startTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 6 | `data.friday.enabled` | bool | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 7 | `data.friday.endTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 8 | `data.friday.startTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 9 | `data.monday` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 10 | `data.monday.breaktime` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 11 | `data.monday.breaktime.endTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 12 | `data.monday.breaktime.startTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 13 | `data.monday.enabled` | bool | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 14 | `data.monday.endTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 15 | `data.monday.startTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 16 | `data.saturday` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 17 | `data.saturday.breaktime` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 18 | `data.saturday.breaktime.endTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 19 | `data.saturday.breaktime.startTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 20 | `data.saturday.enabled` | bool | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 21 | `data.saturday.endTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 22 | `data.saturday.startTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 23 | `data.sunday` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 24 | `data.sunday.breaktime` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 25 | `data.sunday.breaktime.endTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 26 | `data.sunday.breaktime.startTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 27 | `data.sunday.enabled` | bool | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 28 | `data.sunday.endTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 29 | `data.sunday.startTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 30 | `data.thursday` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 31 | `data.thursday.breaktime` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 32 | `data.thursday.breaktime.endTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 33 | `data.thursday.breaktime.startTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 34 | `data.thursday.enabled` | bool | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 35 | `data.thursday.endTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 36 | `data.thursday.startTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 37 | `data.tuesday` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 38 | `data.tuesday.breaktime` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 39 | `data.tuesday.breaktime.endTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 40 | `data.tuesday.breaktime.startTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 41 | `data.tuesday.enabled` | bool | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 42 | `data.tuesday.endTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 43 | `data.tuesday.startTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 44 | `data.wednesday` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 45 | `data.wednesday.breaktime` | object | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 46 | `data.wednesday.breaktime.endTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 47 | `data.wednesday.breaktime.startTime` | string(empty) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 48 | `data.wednesday.enabled` | bool | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 49 | `data.wednesday.endTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |
| 50 | `data.wednesday.startTime` | string(ISO UTC) | (reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님) | 칸 없음 | 앞 판 E12 `operatingHours` |

### P27 `schedule/default-operation-time/v1/queries/get-default-days-off`

스크립트 합집합 키 **1** · 표 행 **1** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array(empty) |  | 확인 안 됨 | HAR 22개 응답 모두 빈 배열 — 안쪽 키 확인 안 됨 · cc 는 `startDateTime` · `endDateTime` 을 읽었다(앞 판 E12) |

### P28 `schedule/open/v2/queries/get-reservation-slots-by-groups`

HAR 에 응답 없음 → 키 대조 불가 · **K5** 「확인 안 됨」.

### P29 `schedule/open/v1/queries/get-schedules-by-visitor`

HAR 에 응답 없음 → 키 대조 불가 · **K5** 「확인 안 됨」.

### P30 `visitor/open/v1/queries/get-visitor-questionnaire`

HAR 에 응답 없음 → 키 대조 불가 · **K5** 「확인 안 됨」.

### P31 `visitor/open/v1/queries/get-questionnaire-submit`

HAR 에 응답 없음 → 키 대조 불가 · **K5** 「확인 안 됨」.

### P32 `schedule/v1/queries/get-schedule-event-logs`

HAR 에 응답 없음 → 키 대조 불가 · **K5** 「확인 안 됨」.

### P33 `schedule/v2/queries/get-schedules-for-reservation`

스크립트 합집합 키 **226** · 표 행 **226** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data[]` | array / object |  | 해당 없음 | DAY 는 이 경로를 부르지 않음 — 판정은 같은 칸을 grouped-by-zone 동기화가 채우는지 기준 |
| 2 | `data[].consultation` | object |  | 해당 없음 | 묶음 |
| 3 | `data[].consultation.consultationMemo` | string / string(empty) | (consultation.consultation_note 는 consultations[].content.text) | 칸 없음(시점 다름) | 앞 판 M3 · C5 — 공개 쓰기 경로와 같은 칸 |
| 4 | `data[].consultation.counselor` | object | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 5 | `data[].consultation.counselor.id` | string / string(empty) | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 6 | `data[].consultation.counselor.name` | string / string(empty) | (id 가 없으니 join 불가) | 칸 없음(시점 다름) | 이름 스냅샷 |
| 7 | `data[].consultation.doctor` | object | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 8 | `data[].consultation.doctor.id` | string / string(empty) | (consultation.counselor_id · doctor_id 는 consultations[] 기록 값) | 칸 없음(시점 다름) | 앞 판 M2 — 일정 단일 상담 정보의 사람 |
| 9 | `data[].consultation.doctor.name` | string / string(empty) | (id 가 없으니 join 불가) | 칸 없음(시점 다름) | 이름 스냅샷 |
| 10 | `data[].consultations[]` | array / array(empty) / object | consultation (models/visit.py:119) | 저장됨 | emr/kos/mapper.py:553 |
| 11 | `data[].consultations[].consultationDoctors[]` | array / object | consultation.doctor_id (models/visit.py:133) | 저장됨 | emr/kos/mapper.py:506 — **1명일 때만**(emr/kos/mapper.py:491-494) |
| 12 | `data[].consultations[].consultationDoctors[].id` | string | consultation.doctor_id (models/visit.py:133) | 저장됨 | emr/kos/mapper.py:506 — **1명일 때만**(emr/kos/mapper.py:491-494) |
| 13 | `data[].consultations[].consultationDoctors[].name` | string | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 14 | `data[].consultations[].consultationProcedures[]` | array(empty) | consultation_procedure (models/visit.py:140) | 칸 있음 · 미동기화 | emr/kos/mapper.py:500 「안쪽 키 미관찰이라 받지 않는다」 · HAR 에서 늘 빈 배열 |
| 15 | `data[].consultations[].consultationStartedDateTimeUtc` | string(ISO UTC) | consultation.started_at (models/visit.py:131) | 저장됨 | emr/kos/mapper.py:504 |
| 16 | `data[].consultations[].content` | object |  | 해당 없음 | 묶음 |
| 17 | `data[].consultations[].content.text` | string | consultation.consultation_note (models/visit.py:134) | 저장됨 | emr/kos/mapper.py:507 |
| 18 | `data[].consultations[].counselors[]` | array / object | consultation.counselor_id (models/visit.py:132) | 저장됨 | emr/kos/mapper.py:505 — **1명일 때만**(둘 이상이면 비움 · emr/kos/mapper.py:491-494 · OQ-13) |
| 19 | `data[].consultations[].counselors[].id` | string | consultation.counselor_id (models/visit.py:132) | 저장됨 | emr/kos/mapper.py:505 — **1명일 때만**(둘 이상이면 비움 · emr/kos/mapper.py:491-494 · OQ-13) |
| 20 | `data[].consultations[].counselors[].name` | string | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 21 | `data[].consultations[].createdDateTimeUtc` | string(ISO UTC) | consultation.created_at (S0:537 「created_at ← createdDateTimeUtc」) | 칸 있음 · 미동기화 | 매퍼 없음 — DAY created_at 은 DAY 행 생성 시각 |
| 22 | `data[].consultations[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:503 |
| 23 | `data[].consultations[].scheduleId` | string(uuid) | consultation.visit_id (models/visit.py:130) | 저장됨 | 부모 일정 |
| 24 | `data[].consultations[].updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 칸 있음 · 미동기화 | 매퍼 없음(상담 기록은 external_updated_at 안 채움) |
| 25 | `data[].consultations[].visitor` | object | visit.customer_id (models/visit.py:67) | 계산으로 대체 | 같은 일정의 고객 |
| 26 | `data[].consultations[].visitor.id` | string | visit.customer_id (models/visit.py:67) | 계산으로 대체 | 같은 일정의 고객 |
| 27 | `data[].consultations[].visitor.isNew` | bool | (visit.is_new 와 같은 값인지 확인 안 됨) | 확인 안 됨 |  |
| 28 | `data[].consultations[].visitor.name` | string | join customer.name | 계산으로 대체 |  |
| 29 | `data[].createdDateTimeUtc` | string(ISO UTC) | visit.booked_at (models/visit.py:68) | 저장됨 | emr/kos/mapper.py:559 |
| 30 | `data[].deleted` | bool | visit.deleted_at (S0:477) | 저장됨 | emr/kos/mapper.py:557 · emr/sync_schedules.py:314 |
| 31 | `data[].etceteraWorks[]` | array(empty) |  | 칸 없음 | 기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음) |
| 32 | `data[].flowStep` | enum: COMPLETED\|CONSULTATION_WAITING\|PROCEDURE\|PROCEDURE_WAITING\|RECEPTION\|RESERVED | visit.flow_step (models/visit.py:86) | 저장됨 | emr/kos/mapper.py:588-590 |
| 33 | `data[].flowStepUpdatedDateTimeUtc` | string(ISO UTC) / string(empty) | visit.flow_step_at (models/visit.py:87) | 저장됨 | emr/kos/mapper.py:591 |
| 34 | `data[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:555 |
| 35 | `data[].occupiedResources[]` | array / object | visit_occupied_resource (models/room.py:96) | 저장됨 | emr/kos/mapper.py:542 |
| 36 | `data[].occupiedResources[].id` | string(uuid) | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:368 |
| 37 | `data[].occupiedResources[].reservationGroup` | object |  | 해당 없음 | 묶음 |
| 38 | `data[].occupiedResources[].reservationGroup.doctors[]` | array(empty) | visit_occupied_resource_doctor (models/room.py:108) | 저장됨 | emr/kos/mapper.py:380-384 |
| 39 | `data[].occupiedResources[].reservationGroup.reservationGroupId` | string | visit_occupied_resource.reservation_group_id (models/room.py:101) | 저장됨 | emr/kos/mapper.py:372 |
| 40 | `data[].occupiedResources[].reservationGroup.zoneId` | string | visit_occupied_resource.zone_id (models/room.py:102) | 저장됨 | emr/kos/mapper.py:375 |
| 41 | `data[].occupiedResources[].reservationTime` | object |  | 해당 없음 | 묶음 |
| 42 | `data[].occupiedResources[].reservationTime.endDateTimeUtc` | string(ISO UTC) | visit_occupied_resource.end_at (models/room.py:104) | 저장됨 | emr/kos/mapper.py:379 |
| 43 | `data[].occupiedResources[].reservationTime.startDateTimeUtc` | string(ISO UTC) | visit_occupied_resource.start_at (models/room.py:103) | 저장됨 | emr/kos/mapper.py:378 |
| 44 | `data[].occupiedResources[].type` | enum: RESERVATION_GROUP | visit_occupied_resource.type (models/room.py:100) | 저장됨 | emr/kos/mapper.py:371 |
| 45 | `data[].orderMemo` | string / string(empty) | visit.procedure_order_note (models/visit.py:92) | 저장됨 | emr/kos/mapper.py:598 |
| 46 | `data[].prescriptionIds[]` | array(empty) | prescription.visit_id (models/prescription.py:20) | 저장됨 | emr/kos/mapper_purchase.py:104 · S0:501 |
| 47 | `data[].purchaseIds[]` | array / array(empty) / string(uuid) | purchase.visit_id (models/purchase.py:58) | 저장됨 | emr/kos/mapper_purchase.py:103 · S0:500 |
| 48 | `data[].purchases[]` | array(empty) | purchase.visit_id (models/purchase.py:58) | 계산으로 대체 | S0:500 — purchaseIds[] 로 받는다 · HAR 에서 늘 빈 배열(안쪽 키 확인 안 됨) |
| 49 | `data[].reactions[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 · S0 OQ-03-1(:1789) 열림 |
| 50 | `data[].receptionDateTimeUtc` | string(ISO UTC) / string(empty) | visit.reception_at (models/visit.py:88) | 저장됨 | emr/kos/mapper.py:592 |
| 51 | `data[].reservation` | object |  | 해당 없음 | 묶음 |
| 52 | `data[].reservation.connectedChannel` | string / enum: HOMEPAGE | visit.connected_channel (models/visit.py:81) | 저장됨 | emr/kos/mapper.py:580 — `Channel_UNSPEICIFED` 는 None(emr/kos/mapper.py:113-118) |
| 53 | `data[].reservation.consultationRequired` | bool | visit.consultation_required (models/visit.py:82) | 저장됨 | emr/kos/mapper.py:581 |
| 54 | `data[].reservation.counselor` | object | visit.requested_counselor_id (models/visit.py:77) | 저장됨 | emr/kos/mapper.py:572-574 — 예약 지정 희망 상담사(앞 판 M1) |
| 55 | `data[].reservation.counselor.id` | string / string(empty) | visit.requested_counselor_id (models/visit.py:77) | 저장됨 | emr/kos/mapper.py:572-574 — 예약 지정 희망 상담사(앞 판 M1) |
| 56 | `data[].reservation.counselor.name` | string / string(empty) | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 57 | `data[].reservation.doctor` | object | visit.requested_doctor_id (models/visit.py:78) | 저장됨 | emr/kos/mapper.py:575-577 |
| 58 | `data[].reservation.doctor.id` | string(empty) | visit.requested_doctor_id (models/visit.py:78) | 저장됨 | emr/kos/mapper.py:575-577 |
| 59 | `data[].reservation.doctor.name` | string(empty) | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 60 | `data[].reservation.endDateTime` | string(ISO UTC) | visit.reserved_end_at (models/visit.py:71) | 저장됨 | emr/kos/mapper.py:563 |
| 61 | `data[].reservation.funnel` | object |  | 해당 없음 | 묶음 |
| 62 | `data[].reservation.funnel.funnel` | object | visit.funnel_id (models/visit.py:79) | 저장됨 | emr/kos/mapper.py:578 |
| 63 | `data[].reservation.funnel.funnel.category` | enum: FUNNEL | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 64 | `data[].reservation.funnel.funnel.closed` | bool | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 65 | `data[].reservation.funnel.funnel.default` | bool | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 66 | `data[].reservation.funnel.funnel.id` | string(uuid) | visit.funnel_id (models/visit.py:79) | 저장됨 | emr/kos/mapper.py:578 |
| 67 | `data[].reservation.funnel.funnel.name` | string | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 68 | `data[].reservation.funnel.funnel.order` | int | join funnel (models/customer.py:145-153) | 계산으로 대체 | funnel 표는 get-codes FUNNEL 로 채움(emr/kos/mapper.py:269-280) |
| 69 | `data[].reservation.funnel.funnelDetail` | string(empty) | visit.funnel_detail (models/visit.py:80) | 저장됨 | emr/kos/mapper.py:579 |
| 70 | `data[].reservation.requestedProcedures[]` | array(empty) | visit_requested_procedure (models/visit.py:100) · sort_order = 배열 순서(models/visit.py:113) | 저장됨 | emr/kos/mapper.py:536-541 — P07 · P08 · P33 HAR 에서 늘 빈 배열 — 안쪽 키는 HAR 에만 있는 `schedule/v1/queries/get-schedule-summaries` 응답에서만 보인다(K5) |
| 71 | `data[].reservation.reservationAssignee` | object | visit.reservation_assignee_id (models/visit.py:76) | 저장됨 | emr/kos/mapper.py:569-571 |
| 72 | `data[].reservation.reservationAssignee.id` | string / string(empty) | visit.reservation_assignee_id (models/visit.py:76) | 저장됨 | emr/kos/mapper.py:569-571 |
| 73 | `data[].reservation.reservationAssignee.name` | string(email꼴) / string(empty) | join staff.name (models/staff.py:51) | 계산으로 대체 |  |
| 74 | `data[].reservation.reservationGroupId` | string | (visit_occupied_resource 쪽 칸은 있음 — 같은 값인지 확인 안 됨) | 칸 없음 | S0:598 「visit 에 두지 않고 visit_occupied_resource 로」는 그룹 칸 얘기 — 이 키 자체의 결정은 없음 |
| 75 | `data[].reservation.reservationMemo` | string / string(empty) | visit.reservation_notes (models/visit.py:75) | 저장됨 | emr/kos/mapper.py:568 |
| 76 | `data[].reservation.sedationRequired` | bool | visit.sedation_required (models/visit.py:83) | 저장됨 | emr/kos/mapper.py:584 |
| 77 | `data[].reservation.startDateTime` | string(ISO UTC) | visit.reserved_start_at (models/visit.py:70) | 저장됨 | emr/kos/mapper.py:560 |
| 78 | `data[].reservation.status` | enum: COMPLETED\|IN_PROGRESS\|RESERVED | visit.reservation_status (models/visit.py:72) | 저장됨 | emr/kos/mapper.py:564-567 |
| 79 | `data[].reservation.statusUpdatedDateTimeUtc` | string(ISO UTC) |  | 칸 없음 | 예약 상태 바뀐 시각 — visit_flow_log 는 flowStep 만 |
| 80 | `data[].reservation.zoneId` | string | (visit_occupied_resource 쪽 칸은 있음 — 같은 값인지 확인 안 됨) | 칸 없음 | S0:598 「visit 에 두지 않고 visit_occupied_resource 로」는 그룹 칸 얘기 — 이 키 자체의 결정은 없음 |
| 81 | `data[].taskTimers[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 · S0 OQ-05-1(:1850) 열림 |
| 82 | `data[].tasks[]` | array / array(empty) / object | visit_task (models/task.py:68) | 저장됨 | emr/kos/mapper.py:545-552 |
| 83 | `data[].tasks[].anesthesiaType` | enum: ANESTHESIA_TYPE_UNSPECIFIED | visit_task.anesthesia_type (models/task.py:102) | 저장됨 | emr/kos/mapper.py:472 |
| 84 | `data[].tasks[].assigneeMemo` | string(empty) | visit_task.assignee_note (models/task.py:104) | 저장됨 | emr/kos/mapper.py:474 |
| 85 | `data[].tasks[].assignees[]` | array / array(empty) / object | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 86 | `data[].tasks[].assignees[].id` | string | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 87 | `data[].tasks[].assignees[].name` | string / string(email꼴) | join staff.name | 계산으로 대체 |  |
| 88 | `data[].tasks[].calledDoctors[]` | array / array(empty) / object | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 89 | `data[].tasks[].calledDoctors[].id` | string | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 90 | `data[].tasks[].calledDoctors[].name` | string | join staff.name | 계산으로 대체 |  |
| 91 | `data[].tasks[].completedDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.completed_at (models/task.py:114) | 저장됨 | emr/kos/mapper.py:481 |
| 92 | `data[].tasks[].doctorAssignedDateTimeUtc` | string(ISO UTC) | visit_task.doctor_assigned_at (models/task.py:110) | 저장됨 | emr/kos/mapper.py:480 |
| 93 | `data[].tasks[].doctorCallDateTime` | string(ISO UTC) / string(empty) | visit_task.doctor_called_at (models/task.py:109) | 저장됨 | emr/kos/mapper.py:479 |
| 94 | `data[].tasks[].doctorMemo` | string / string(empty) | visit_task.doctor_note (models/task.py:105) | 저장됨 | emr/kos/mapper.py:475 |
| 95 | `data[].tasks[].doctors[]` | array / array(empty) / object | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 96 | `data[].tasks[].doctors[].id` | string | visit_task_staff (models/task.py:140) | 저장됨 | emr/kos/mapper.py:482-484 |
| 97 | `data[].tasks[].doctors[].name` | string | join staff.name | 계산으로 대체 |  |
| 98 | `data[].tasks[].etceteraConfiguration` | object |  | 해당 없음 | 묶음 |
| 99 | `data[].tasks[].etceteraConfiguration.etceteraTaskId` | string / string(empty) | (etc_task_type 표는 있으나 작업 → 종류 FK 없음) | 칸 없음 | emr/kos/mapper.py:485-487 → `is_room_assign`(models/task.py:91) 판정에만 씀(emr/sync_tasks.py:132) |
| 100 | `data[].tasks[].etceteraConfiguration.name` | string / string(empty) | visit_task.etc_task_title (models/task.py:88) | 저장됨 | emr/kos/mapper.py:469 |
| 101 | `data[].tasks[].etceteraConfiguration.translsMap` | object / object(empty) |  | 칸 없음 |  |
| 102 | `data[].tasks[].etceteraConfiguration.translsMap.name` | object |  | 칸 없음 |  |
| 103 | `data[].tasks[].etceteraConfiguration.translsMap.name.translation` | object(empty) |  | 칸 없음 |  |
| 104 | `data[].tasks[].memo` | string(empty) | visit_task.procedure_note (models/task.py:103) | 저장됨 | emr/kos/mapper.py:473 |
| 105 | `data[].tasks[].order` | int | visit_task.sort_order (models/task.py:75) | 저장됨 | emr/kos/mapper.py:456 |
| 106 | `data[].tasks[].paymentRequired` | bool | visit_task.payment_required (models/task.py:101) | 저장됨 | emr/kos/mapper.py:471 |
| 107 | `data[].tasks[].procedureConfiguration` | object / object(empty) |  | 해당 없음 | 묶음 |
| 108 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration` | object |  | 해당 없음 | 묶음 |
| 109 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.caution` | string(empty) | (treatment_item.code · caution = 지금 메뉴 값 models/menu.py:173 · 176) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 110 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.code` | string | (treatment_item.code · caution = 지금 메뉴 값 models/menu.py:173 · 176) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 111 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.id` | string | visit_task.treatment_item_id (models/task.py:98) | 저장됨 | emr/kos/mapper_purchase.py:88 |
| 112 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.machines[]` | array / array(empty) / object | visit_task.machines (models/task.py:96) | 저장됨 | emr/kos/mapper_purchase.py:89 — 이름 스냅샷 |
| 113 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.machines[].id` | string | (이름 스냅샷만 — id 없음) | 칸 없음 |  |
| 114 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.machines[].name` | string | visit_task.machines (models/task.py:96) | 저장됨 | emr/kos/mapper_purchase.py:89 — 이름 스냅샷 |
| 115 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.machines[].searchPhoneticName` | string | (machine · medicine.search_phonetic_name = 지금 값) | 칸 없음(시점 다름) |  |
| 116 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[]` | array / array(empty) / object | visit_task.medicines (models/task.py:94) | 저장됨 | emr/kos/mapper.py:449 · 470 — 이름 스냅샷 |
| 117 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].id` | string | (이름 스냅샷만 — id 없음) | 칸 없음 |  |
| 118 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].name` | string | visit_task.medicines (models/task.py:94) | 저장됨 | emr/kos/mapper.py:449 · 470 — 이름 스냅샷 |
| 119 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].searchPhoneticName` | string | (machine · medicine.search_phonetic_name = 지금 값) | 칸 없음(시점 다름) |  |
| 120 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.title` | string | visit_task.medical_service_title (models/task.py:80) | 저장됨 | emr/kos/mapper.py:462 |
| 121 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap` | object |  | 칸 없음 |  |
| 122 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title` | object |  | 칸 없음 |  |
| 123 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation` | object / object(empty) |  | 칸 없음 |  |
| 124 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.en` | string |  | 칸 없음 |  |
| 125 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.ja` | string |  | 칸 없음 |  |
| 126 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.ko` | string |  | 칸 없음 |  |
| 127 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.zh-Hans` | string |  | 칸 없음 |  |
| 128 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.zh-Hant` | string |  | 칸 없음 |  |
| 129 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.unit` | object | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) |
| 130 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.unit.type` | enum: CC\|SHOT\|UNIT | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) |
| 131 | `data[].tasks[].procedureConfiguration.medicalServiceConfiguration.unit.value` | number | (treatment_item.unit_* = 지금 메뉴 값 models/menu.py:179-180) | 칸 없음(시점 다름) | 작업 단위는 옵션 단위만 저장(emr/kos/mapper.py:447) |
| 132 | `data[].tasks[].procedureConfiguration.productOptionConfiguration` | object |  | 해당 없음 | 묶음 |
| 133 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.medicineAndMachines[]` | array(empty) |  | 확인 안 됨 | HAR 에서 늘 빈 배열 |
| 134 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.optionId` | string |  | 일부러 안 둠 | S0:892 「상품 옵션 id 는 ERD v1 이 작업에 두지 않음」 |
| 135 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.optionTitle` | string | visit_task.option_title (models/task.py:79) | 저장됨 | emr/kos/mapper.py:461 |
| 136 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.procedure` | object | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 137 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.categoryIds[]` | array(empty) |  | 일부러 안 둠 | S0:1429 「시술 카테고리 칸으로 두지 않는다」 |
| 138 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.createDate` | string(empty) | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 139 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.id` | string | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 140 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.procedure.name` | string | (treatment 표는 지금 값 · 작업 → 시술 참조 없음) | 칸 없음(시점 다름) | 메뉴 스냅샷 |
| 141 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.productTitle` | string / string(empty) | (product.title 은 지금 메뉴 값 · 작업 → 옵션 참조 없음) | 칸 없음(시점 다름) | data_rules 「메뉴 참조 = id + 그때 값 스냅샷」 |
| 142 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap` | object |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 143 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle` | object |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 144 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation` | object / object(empty) |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 145 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.en` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 146 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.ja` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 147 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.ko` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 148 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.zh-Hans` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 149 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.zh-Hant` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 150 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle` | object |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 151 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation` | object / object(empty) |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 152 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.en` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 153 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.ja` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 154 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.ko` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 155 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.zh-Hans` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 156 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.zh-Hant` | string |  | 칸 없음 | 옵션 · 상품 이름 번역 스냅샷 |
| 157 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.unit` | object |  | 해당 없음 | 묶음 |
| 158 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.unit.type` | enum: CC\|SHOT\|UNIT\|UnitType_UNKNOWN | visit_task.unit_type · unit_value (models/task.py:82 · 85) | 저장됨 | emr/kos/mapper.py:447-466 — `UnitType_UNKNOWN` 은 None |
| 159 | `data[].tasks[].procedureConfiguration.productOptionConfiguration.unit.value` | number | visit_task.unit_type · unit_value (models/task.py:82 · 85) | 저장됨 | emr/kos/mapper.py:447-466 — `UnitType_UNKNOWN` 은 None |
| 160 | `data[].tasks[].procedureConfiguration.ticketConfiguration` | object / object(empty) |  | 해당 없음 | 묶음(시술권이 아니면 빈 객체) |
| 161 | `data[].tasks[].procedureConfiguration.ticketConfiguration.round` | object |  | 해당 없음 | 묶음 |
| 162 | `data[].tasks[].procedureConfiguration.ticketConfiguration.round.current` | int | visit_task.ticket_round_current (models/task.py:86) | 저장됨 | emr/kos/mapper.py:467 |
| 163 | `data[].tasks[].procedureConfiguration.ticketConfiguration.round.total` | int | visit_task.ticket_round_total (models/task.py:87) | 저장됨 | emr/kos/mapper.py:468 |
| 164 | `data[].tasks[].procedureConfiguration.ticketConfiguration.ticketId` | string(uuid) | visit_task.ticket_id (models/task.py:99) | 저장됨 | emr/kos/mapper_purchase.py:85-87 |
| 165 | `data[].tasks[].readyDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.ready_at (models/task.py:108) | 저장됨 | emr/kos/mapper.py:478 |
| 166 | `data[].tasks[].room` | object | visit_task.room_id (models/task.py:106) | 저장됨 | emr/kos/mapper.py:450-452 · 카드 방 visit.room_id(models/visit.py:93) emr/kos/mapper.py:388-408 |
| 167 | `data[].tasks[].room.id` | string / string(empty) | visit_task.room_id (models/task.py:106) | 저장됨 | emr/kos/mapper.py:450-452 · 카드 방 visit.room_id(models/visit.py:93) emr/kos/mapper.py:388-408 |
| 168 | `data[].tasks[].room.order` | int | join room (models/room.py:43-49) | 계산으로 대체 |  |
| 169 | `data[].tasks[].room.title` | string / string(empty) | join room (models/room.py:43-49) | 계산으로 대체 |  |
| 170 | `data[].tasks[].room.zoneId` | string / string(empty) | join room (models/room.py:43-49) | 계산으로 대체 |  |
| 171 | `data[].tasks[].roomAssignedDateTimeUtc` | string(ISO UTC) / string(empty) | visit_task.room_assigned_at (models/task.py:107) | 저장됨 | emr/kos/mapper.py:477 |
| 172 | `data[].tasks[].sequence` | int | visit_task.sequence (models/task.py:74) | 저장됨 | emr/kos/mapper.py:454 |
| 173 | `data[].tasks[].status` | enum: CANCELED\|DONE\|NOT_STARTED\|READY\|WAITING | visit_task.status (models/task.py:76) | 저장됨 | emr/kos/mapper.py:457-459 |
| 174 | `data[].tasks[].title` | string | visit_task.title (models/task.py:78) | 저장됨 | emr/kos/mapper.py:460 |
| 175 | `data[].tasks[].translsMap` | object |  | 칸 없음 | 작업 이름 번역 |
| 176 | `data[].tasks[].translsMap.title` | object |  | 칸 없음 | 작업 이름 번역 |
| 177 | `data[].tasks[].translsMap.title.translation` | object / object(empty) |  | 칸 없음 | 작업 이름 번역 |
| 178 | `data[].tasks[].translsMap.title.translation.de` | string |  | 칸 없음 | 작업 이름 번역 |
| 179 | `data[].tasks[].translsMap.title.translation.en` | string |  | 칸 없음 | 작업 이름 번역 |
| 180 | `data[].tasks[].translsMap.title.translation.es` | string |  | 칸 없음 | 작업 이름 번역 |
| 181 | `data[].tasks[].translsMap.title.translation.fr` | string |  | 칸 없음 | 작업 이름 번역 |
| 182 | `data[].tasks[].translsMap.title.translation.id` | string |  | 칸 없음 | 작업 이름 번역 |
| 183 | `data[].tasks[].translsMap.title.translation.ja` | string |  | 칸 없음 | 작업 이름 번역 |
| 184 | `data[].tasks[].translsMap.title.translation.ko` | string |  | 칸 없음 | 작업 이름 번역 |
| 185 | `data[].tasks[].translsMap.title.translation.mn` | string |  | 칸 없음 | 작업 이름 번역 |
| 186 | `data[].tasks[].translsMap.title.translation.ms` | string |  | 칸 없음 | 작업 이름 번역 |
| 187 | `data[].tasks[].translsMap.title.translation.nl` | string |  | 칸 없음 | 작업 이름 번역 |
| 188 | `data[].tasks[].translsMap.title.translation.pt` | string |  | 칸 없음 | 작업 이름 번역 |
| 189 | `data[].tasks[].translsMap.title.translation.ru` | string |  | 칸 없음 | 작업 이름 번역 |
| 190 | `data[].tasks[].translsMap.title.translation.th` | string |  | 칸 없음 | 작업 이름 번역 |
| 191 | `data[].tasks[].translsMap.title.translation.uz` | string |  | 칸 없음 | 작업 이름 번역 |
| 192 | `data[].tasks[].translsMap.title.translation.vi` | string |  | 칸 없음 | 작업 이름 번역 |
| 193 | `data[].tasks[].translsMap.title.translation.zh-Hans` | string |  | 칸 없음 | 작업 이름 번역 |
| 194 | `data[].tasks[].translsMap.title.translation.zh-Hant` | string |  | 칸 없음 | 작업 이름 번역 |
| 195 | `data[].tasks[].type` | enum: ETCETERA\|PROCEDURE | visit_task.kind (models/task.py:73) | 저장됨 | emr/kos/mapper.py:455 |
| 196 | `data[].tasks[].urgencyLevel` | enum: URGENCY_LEVEL_UNSPECIFIED |  | 칸 없음 | 긴급도 |
| 197 | `data[].updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 저장됨 | emr/kos/mapper.py:556 · emr/sync_schedules.py:271 |
| 198 | `data[].visitor` | object | customer (models/customer.py:33) | 저장됨 | emr/kos/mapper.py:558 |
| 199 | `data[].visitor.categories[]` | array / array(empty) / object | customer_category_link (models/customer.py:157) | 저장됨 | emr/kos/mapper.py:322-327 |
| 200 | `data[].visitor.categories[].color` | string | join customer_category (models/customer.py:124-131) | 계산으로 대체 | get-codes VISITOR_CATEGORY 로 채움 |
| 201 | `data[].visitor.categories[].id` | string(uuid) | customer_category_link (models/customer.py:157) | 저장됨 | emr/kos/mapper.py:322-327 |
| 202 | `data[].visitor.categories[].name` | string | join customer_category (models/customer.py:124-131) | 계산으로 대체 | get-codes VISITOR_CATEGORY 로 채움 |
| 203 | `data[].visitor.categories[].order` | int | join customer_category (models/customer.py:124-131) | 계산으로 대체 | get-codes VISITOR_CATEGORY 로 채움 |
| 204 | `data[].visitor.chartNumber` | string(digits) | customer.chart_number (models/customer.py:43) + external_ref.external_number (models/customer.py:107) | 저장됨 | emr/kos/mapper.py:308 · emr/sync_schedules.py:150 |
| 205 | `data[].visitor.dateOfBirth` | string / string(empty) | customer.birth_date (models/customer.py:52) | 저장됨 | emr/kos/mapper.py:312 |
| 206 | `data[].visitor.gender` | enum: FEMALE\|GENDER_UNSPECIFIED\|MALE | customer.gender (models/customer.py:51) | 저장됨 | emr/kos/mapper.py:311 — `GENDER_UNSPECIFIED` 는 None |
| 207 | `data[].visitor.id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:307 |
| 208 | `data[].visitor.isNew` | bool | visit.is_new (models/visit.py:91) | 저장됨 | emr/kos/mapper.py:597 — 방문마다 값(S0:301 · 360) |
| 209 | `data[].visitor.memo` | string / string(empty) | customer.customer_notes (models/customer.py:72) | 저장됨 | emr/kos/mapper.py:316 |
| 210 | `data[].visitor.name` | string | customer.name (models/customer.py:46) | 저장됨 | emr/kos/mapper.py:309 |
| 211 | `data[].visitor.nationality` | string | customer.nationality (models/customer.py:53) | 저장됨 | emr/kos/mapper.py:313 |
| 212 | `data[].visitor.phone` | object |  | 해당 없음 | 묶음 |
| 213 | `data[].visitor.phone.countryCode` | string(digits) | customer.phone_country_code (models/customer.py:61) | 저장됨 | emr/kos/mapper.py:314 |
| 214 | `data[].visitor.phone.phoneNumber` | string(digits) | customer.phone_number (models/customer.py:62) | 저장됨 | emr/kos/mapper.py:315 |
| 215 | `data[].visitor.phoneticName` | string / string(empty) | customer.name_pronunciation (models/customer.py:47) | 저장됨 | emr/kos/mapper.py:310 |
| 216 | `data[].visitor.snsInfo` | object |  | 해당 없음 | 묶음 |
| 217 | `data[].visitor.snsInfo.accountId` | string / string(empty) | customer.sns_account_id (models/customer.py:70) | 저장됨 | emr/kos/mapper.py:318 |
| 218 | `data[].visitor.snsInfo.snsType` | string | customer.sns_type (models/customer.py:69) | 저장됨 | emr/kos/mapper.py:317 |
| 219 | `data[].visitor.visitorType` | object | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 |
| 220 | `data[].visitor.visitorType.id` | string / string(empty) | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 |
| 221 | `data[].visitor.visitorType.name` | string / string(empty) | customer_type.name (models/customer.py:120) | 저장됨 | emr/kos/mapper.py:319-321 |
| 222 | `data[].visitorLocation` | object |  | 해당 없음 | 묶음 |
| 223 | `data[].visitorLocation.zoneId` | string | visit.current_zone_id (models/visit.py:90) | 저장됨 | emr/kos/mapper.py:594-596 |
| 224 | `data[].zone` | object |  | 해당 없음 | 묶음 |
| 225 | `data[].zone.id` | string | visit.reception_zone_id (models/visit.py:89) | 저장됨 | emr/kos/mapper.py:593 |
| 226 | `data[].zone.title` | string | join zone.title (models/room.py:35) | 계산으로 대체 | 구역 이름 — 기준 정보 1시간 |

### P34 `visitor/v1/queries/find-duplicated-visitor`

스크립트 합집합 키 **49** · 표 행 **49** · 빠진 키 **0**

| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |
|---|---|---|---|---|---|
| 1 | `data` | object |  | 해당 없음 | DAY 는 이 경로를 부르지 않음 · 응답 모양이 get-visitor 와 같다 |
| 2 | `data.address` | object |  | 해당 없음 | 묶음 |
| 3 | `data.address.address` | string(empty) | customer.address (models/customer.py:66) | 칸 있음 · 미동기화 |  |
| 4 | `data.address.detailedAddress` | string(empty) | customer.address_detail (models/customer.py:67) | 칸 있음 · 미동기화 |  |
| 5 | `data.address.zipCode` | string(empty) | customer.zip_code (models/customer.py:68) | 칸 있음 · 미동기화 |  |
| 6 | `data.aggrementAdvertisements` | bool | customer.agreed_marketing (models/customer.py:84) | 칸 있음 · 미동기화 | S0:355 |
| 7 | `data.aggrementPersonalInformation` | bool | customer.agreed_personal_info (models/customer.py:83) | 칸 있음 · 미동기화 | S0:355 |
| 8 | `data.agreementInformationalNotification` | bool | customer.agreed_informational (models/customer.py:85) | 칸 있음 · 미동기화 | S0:355 |
| 9 | `data.chartNumber` | string(digits) | customer.chart_number (models/customer.py:43) | 저장됨 | emr/kos/mapper.py:308 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 10 | `data.counselor` | object | customer.assigned_counselor_id (models/customer.py:75) | 칸 있음 · 미동기화 | S0:350 |
| 11 | `data.counselor.id` | string(empty) | customer.assigned_counselor_id (models/customer.py:75) | 칸 있음 · 미동기화 | S0:350 |
| 12 | `data.counselor.name` | string(empty) | join staff.name | 계산으로 대체 |  |
| 13 | `data.createdDateTimeUtc` | string(ISO UTC) | customer.registered_at (models/customer.py:44) | 칸 있음 · 미동기화 | S0:330 · 매퍼 없음 |
| 14 | `data.customAttributes[]` | array(empty) |  | 일부러 안 둠 | S0:312 반려(`custom_attributes` · 명동점 정의 0개) |
| 15 | `data.dateOfBirth` | string | customer.birth_date (models/customer.py:52) | 저장됨 | emr/kos/mapper.py:312 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 16 | `data.deleted` | bool | customer.deleted_at (S0:331) | 칸 있음 · 미동기화 | 매퍼 없음 |
| 17 | `data.detailedFunnel` | string(empty) |  | 칸 없음 | S0:414 「옛 칸」(결정 없음) |
| 18 | `data.doctor` | object | customer.assigned_doctor_id (models/customer.py:74) | 칸 있음 · 미동기화 | S0:350 |
| 19 | `data.doctor.id` | string(empty) | customer.assigned_doctor_id (models/customer.py:74) | 칸 있음 · 미동기화 | S0:350 |
| 20 | `data.doctor.name` | string(empty) | join staff.name | 계산으로 대체 |  |
| 21 | `data.foreignRegistrationNumber` | string(empty) | customer.foreign_registration_number (models/customer.py:57) | 칸 있음 · 미동기화 | **암호화 대상**(data_rules) |
| 22 | `data.funnel` | string(empty) |  | 칸 없음 | S0:414 「옛 칸」(결정 없음) |
| 23 | `data.gender` | enum: GENDER_UNSPECIFIED | customer.gender (models/customer.py:51) | 저장됨 | emr/kos/mapper.py:311 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 24 | `data.id` | string | external_ref.external_id (models/customer.py:106) | 저장됨 | emr/kos/mapper.py:307 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 25 | `data.isNew` | bool | (visit.is_new — 방문마다) | 일부러 안 둠 | S0:301 · 360 「is_new → 3번 방문」 · 앞 판 M4 |
| 26 | `data.language` | string(empty) | customer.language (models/customer.py:54) | 칸 있음 · 미동기화 | 앞 판 B1 |
| 27 | `data.lastVisitedDateTimeUtc` | string(empty) | max(visit.*) — S0:360 「방문 기록에서 계산」 | 계산으로 대체 | KOS 정의(예약 · 접수 · 완료) 확인 안 됨 — 앞 판 M9 · 과거 방문은 백필 범위만 |
| 28 | `data.lineInformation[]` | array(empty) |  | 일부러 안 둠 | S0:312 · 314-317 |
| 29 | `data.memo` | string(empty) | customer.customer_notes (models/customer.py:72) | 저장됨 | emr/kos/mapper.py:316 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 30 | `data.migratedMemo` | string(empty) |  | 일부러 안 둠 | S0:311 반려(`legacy_notes`) |
| 31 | `data.name` | string | customer.name (models/customer.py:46) | 저장됨 | emr/kos/mapper.py:309 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 32 | `data.nationality` | string | customer.nationality (models/customer.py:53) | 저장됨 | emr/kos/mapper.py:313 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 33 | `data.passportNumber` | string(empty) | customer.passport_number (models/customer.py:58) | 칸 있음 · 미동기화 | **암호화 대상**(data_rules) |
| 34 | `data.recommenderName` | string(empty) | customer.referrer_name (models/customer.py:81) | 칸 있음 · 미동기화 | S0:354 |
| 35 | `data.registrationNumber` | string(empty) | customer.registration_number (models/customer.py:56) | 칸 있음 · 미동기화 | **암호화 대상**(data_rules) |
| 36 | `data.snsInfo` | object |  | 해당 없음 | 묶음 |
| 37 | `data.snsInfo.accountId` | string(empty) | customer.sns_account_id (models/customer.py:70) | 저장됨 | emr/kos/mapper.py:318 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 38 | `data.snsInfo.snsType` | string | customer.sns_type (models/customer.py:69) | 저장됨 | emr/kos/mapper.py:317 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 39 | `data.unniInformation[]` | array(empty) |  | 일부러 안 둠 | S0:311 · 317 |
| 40 | `data.updatedDateTimeUtc` | string(ISO UTC) | external_ref.external_updated_at (models/customer.py:108) | 칸 있음 · 미동기화 | 고객은 external_number 만 씀(emr/sync_schedules.py:150) |
| 41 | `data.visitorCategories[]` | array(empty) | customer_category_link (models/customer.py:157) | 저장됨 | emr/kos/mapper.py:322-327(일정 visitor `categories[]`) — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 42 | `data.visitorCategoryId` | string(empty) |  | 칸 없음 | S0:413 에 키만 있음(결정 없음) |
| 43 | `data.visitorFunnel` | object |  | 해당 없음 | 묶음 |
| 44 | `data.visitorFunnel.funnelCategoryId` | string(empty) | join funnel.category_id (models/customer.py:149) | 계산으로 대체 |  |
| 45 | `data.visitorFunnel.funnelDetail` | string(empty) | customer.funnel_detail (models/customer.py:78) | 칸 있음 · 미동기화 | S0:352 |
| 46 | `data.visitorFunnel.funnelId` | string(empty) | customer.funnel_id (models/customer.py:77) | 칸 있음 · 미동기화 | S0:351 |
| 47 | `data.visitorType` | object | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 48 | `data.visitorType.id` | string(empty) | customer.customer_type_id (models/customer.py:73) | 저장됨 | emr/kos/mapper.py:319-321 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |
| 49 | `data.visitorType.name` | string(empty) | customer_type.name (models/customer.py:120) | 저장됨 | emr/kos/mapper.py:319-321 — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4) |

## K3. 집계

### K3-1. 경로별 · 판정별 수

| # | 경로 | 키 | 저장됨 | 칸 있음 · 미동기화 | 칸 없음 | 칸 없음(시점 다름) | 일부러 안 둠 | 계산으로 대체 | 해당 없음 | 확인 안 됨 |
|---|---|---|---|---|---|---|---|---|---|---|
| P01 | `schedule/zone/v1/queries/get-zones` | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| P02 | `schedule/zone/room/v1/queries/get-rooms` | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| P03 | `schedule/group/v1/queries/get-reservation-groups` | 63 | 51 | 0 | 3 | 0 | 0 | 1 | 8 | 0 |
| P04 | `role/v2/queries/get-roles` | 13 | 4 | 0 | 0 | 0 | 8 | 0 | 1 | 0 |
| P05 | `account/v2/queries/get-accounts` | 19 | 9 | 2 | 4 | 0 | 0 | 3 | 1 | 0 |
| P06 | `meta/codes/v1/queries/get-codes` | 8 | 6 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| P07 | `schedule/v2/queries/get-schedules-grouped-by-zone` | 230 | 99 | 3 | 62 | 19 | 2 | 23 | 18 | 4 |
| P08 | `schedule/v1/queries/get-schedule-detail` | 242 | 103 | 3 | 71 | 18 | 2 | 24 | 17 | 4 |
| P09 | `procedure-menu/categories/queries/get-categories` | 14 | 12 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| P10 | `procedure-menu/products/queries/get-products` | 210 | 168 | 0 | 11 | 0 | 4 | 17 | 9 | 1 |
| P11 | `procedure-menu/v2/queries/get-procedures` | 7 | 5 | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| P12 | `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks` | 7 | 3 | 0 | 3 | 0 | 0 | 0 | 1 | 0 |
| P13 | `procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product` | 21 | 14 | 0 | 3 | 0 | 0 | 0 | 4 | 0 |
| P14 | `procedure-menu/etcetera-products/v1/queries/get-etcetera-products` | 13 | 8 | 0 | 2 | 0 | 0 | 0 | 3 | 0 |
| P15 | `purchase/v1/queries/get-purchase-summaries` | 455 | 88 | 14 | 75 | 214 | 4 | 41 | 10 | 9 |
| P16 | `ticket/v1/queries/get-ticket-bundles` | 116 | 15 | 1 | 57 | 34 | 3 | 3 | 3 | 0 |
| P17 | `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` | 23 | 9 | 1 | 4 | 0 | 6 | 0 | 3 | 0 |
| P18 | `purchase/prepaid-card/v1/queries/get-prepaid-card-charging-events` | 15 | 7 | 0 | 1 | 0 | 0 | 3 | 4 | 0 |
| P19 | `purchase/prepaid-card/v1/queries/get-prepaid-card-visitors` | 5 | 2 | 0 | 0 | 0 | 0 | 2 | 1 | 0 |
| P20 | `visitor/v2/queries/get-visitors` | 64 | 17 | 24 | 5 | 0 | 5 | 7 | 6 | 0 |
| P21 | `v1/account/queries/get-user-account` | 11 | 8 | 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| P22 | `common/v1/tenant/queries/get-user-tenants` | 8 | 1 | 0 | 5 | 1 | 0 | 0 | 1 | 0 |
| P23 | `common/user/v1/queries/get-active-sign-ins` | (HAR 없음) | | | | | | | | |
| P24 | `visitor/v2/queries/get-visitor` | 63 | 17 | 24 | 5 | 0 | 5 | 7 | 5 | 0 |
| P25 | `v1/hospital/queries/get-hospital` | 22 | 0 | 0 | 13 | 1 | 6 | 0 | 1 | 1 |
| P26 | `schedule/default-operation-time/v1/queries/get-default-operation-timetable` | 50 | 0 | 0 | 49 | 0 | 0 | 0 | 1 | 0 |
| P27 | `schedule/default-operation-time/v1/queries/get-default-days-off` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| P28 | `schedule/open/v2/queries/get-reservation-slots-by-groups` | (HAR 없음) | | | | | | | | |
| P29 | `schedule/open/v1/queries/get-schedules-by-visitor` | (HAR 없음) | | | | | | | | |
| P30 | `visitor/open/v1/queries/get-visitor-questionnaire` | (HAR 없음) | | | | | | | | |
| P31 | `visitor/open/v1/queries/get-questionnaire-submit` | (HAR 없음) | | | | | | | | |
| P32 | `schedule/v1/queries/get-schedule-event-logs` | (HAR 없음) | | | | | | | | |
| P33 | `schedule/v2/queries/get-schedules-for-reservation` | 226 | 102 | 3 | 54 | 19 | 2 | 24 | 18 | 4 |
| P34 | `visitor/v1/queries/find-duplicated-visitor` | 49 | 13 | 20 | 3 | 0 | 5 | 4 | 4 | 0 |
| | **합** | **1965** | **769** | **95** | **431** | **306** | **54** | **160** | **126** | **24** |

### K3-2. DB 확장 후보(`칸 있음 · 미동기화` · `칸 없음` · `칸 없음(시점 다름)`) — DAY 테이블별

키는 경로 뿌리(`@` = 그 경로의 행 · 일정이면 일정 1건)를 기준으로 겹친 것을 하나로 셌다(같은 키가 P07 · P08 · P33 에 함께 나오는 등). 「행」= K2 표의 행 수 합, 「고유」= 겹침을 뺀 수. 설계가 아니라 후보 목록이다.

| 대상 테이블 | 있는 표 / 새 표 | 행 | 고유 | 미동기화 | 칸 없음 | 시점 다름 | 민감 정보 | KOS 경로 |
|---|---|---|---|---|---|---|---|---|
| `visit_task` | 있는 표 | 184 | 62 | 0 | 50 | 12 | — | P07 · P08 · P33 |
| `purchase_item` | 있는 표 | 180 | 180 | 12 | 58 | 110 | — | P15 |
| `purchase_item(구성 스냅샷 — 새 표 필요)` | 새 표 필요 | 104 | 104 | 0 | 0 | 104 | — | P15 |
| `customer` | 있는 표 | 78 | 28 | 23 | 5 | 0 | **암호화 대상**: `foreignRegistrationNumber`, `passportNumber`, `registrationNumber` · 개인정보(암호화 대상 아님): `address`, `detailedAddress`, `email`, `name`, `passportExpiryDate`, `passportGivenNames`, `passportSurname`, `recommenderName` … | P20 · P24 · P34 |
| `ticket_set` | 있는 표 | 53 | 53 | 0 | 20 | 33 | — | P16 |
| `새 표 필요(병원 기본 운영 시간)` | 새 표 필요 | 49 | 49 | 0 | 49 | 0 | — | P26 |
| `ticket_bundle` | 있는 표 | 38 | 38 | 0 | 37 | 1 | — | P16 |
| `visit` | 있는 표 | 29 | 10 | 0 | 3 | 7 | 개인정보(암호화 대상 아님): `consultationMemo`, `name` | P07 · P08 · P33 |
| `새 표 필요(기타 업무)` | 새 표 필요 | 29 | 17 | 0 | 17 | 0 | 개인정보(암호화 대상 아님): `memo`, `name` | P07 · P08 · P33 |
| `hospital` | 있는 표 | 20 | 19 | 0 | 18 | 1 | 개인정보(암호화 대상 아님): `representativeName` | P22 · P25 |
| `purchase_transaction` | 있는 표 | 15 | 15 | 1 | 14 | 0 | — | P15 |
| `external_ref` | 있는 표 | 7 | 2 | 2 | 0 | 0 | — | P05 · P07 · P08 · P20 · P24 · P33 · P34 |
| `staff` | 있는 표 | 6 | 5 | 1 | 4 | 0 | — | P05 · P21 |
| `product_option_composition` | 있는 표 | 6 | 6 | 0 | 6 | 0 | — | P10 |
| `prepaid_card` | 있는 표 | 5 | 5 | 1 | 4 | 0 | — | P17 |
| `product_option` | 있는 표 | 4 | 4 | 0 | 4 | 0 | — | P10 |
| `purchase` | 있는 표 | 4 | 4 | 1 | 3 | 0 | 개인정보(암호화 대상 아님): `name` | P15 |
| `reservation_group` | 있는 표 | 3 | 3 | 0 | 3 | 0 | 개인정보(암호화 대상 아님): `memo` | P03 |
| `consultation_procedure` | 있는 표 | 3 | 1 | 1 | 0 | 0 | — | P07 · P08 · P33 |
| `consultation` | 있는 표 | 3 | 1 | 1 | 0 | 0 | — | P07 · P08 · P33 |
| `etc_task_type` | 있는 표 | 3 | 3 | 0 | 3 | 0 | — | P12 |
| `prepaid_card_product` | 있는 표 | 3 | 3 | 0 | 3 | 0 | — | P13 |
| `etcetera_product` | 있는 표 | 2 | 2 | 0 | 2 | 0 | — | P14 |
| `visit (태그 — 새 표 필요)` | 새 표 필요 | 1 | 1 | 0 | 1 | 0 | — | P08 |
| `product` | 있는 표 | 1 | 1 | 0 | 1 | 0 | — | P10 |
| `ticket` | 있는 표 | 1 | 1 | 1 | 0 | 0 | — | P16 |
| `prepaid_card_ledger` | 있는 표 | 1 | 1 | 0 | 1 | 0 | — | P18 |

<details><summary>테이블별 키 목록(고유 · 번역 언어 잎은 묶어 셈)</summary>


**`visit_task`**

- `@.tasks[].etceteraConfiguration.etceteraTaskId` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].etceteraConfiguration.translsMap` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].etceteraConfiguration.translsMap.name` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].etceteraConfiguration.translsMap.name.translation` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.caution` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.code` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.machines[].id` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.machines[].searchPhoneticName` — 칸 없음(시점 다름) — P07 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].id` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.medicines[].searchPhoneticName` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.translsMap.title.translation.<언어>` ×5 — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.unit` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.unit.type` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.medicalServiceConfiguration.unit.value` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.procedure` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.procedure.createDate` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.procedure.id` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.procedure.name` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.productTitle` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.translsMap` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.optionTitle.translation.<언어>` ×5 — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].procedureConfiguration.productOptionConfiguration.translsMap.productTitle.translation.<언어>` ×5 — 칸 없음 — P07 · P08 · P33
- `@.tasks[].translsMap` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].translsMap.title` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].translsMap.title.translation` — 칸 없음 — P07 · P08 · P33
- `@.tasks[].translsMap.title.translation.<언어>` ×17 — 칸 없음 — P07 · P08 · P33
- `@.tasks[].urgencyLevel` — 칸 없음 — P07 · P08 · P33

**`purchase_item`**

- `@.items[].adjustPriceV2.amount.currency` — 칸 없음 — P15
- `@.items[].adjustPriceV2.suppliedAmount.currency` — 칸 없음 — P15
- `@.items[].adjustPriceV2.taxFreeAmount.currency` — 칸 없음 — P15
- `@.items[].adjustPriceV2.vatAmount.currency` — 칸 없음 — P15
- `@.items[].etceteraConfiguration.price` — 칸 없음(시점 다름) — P15
- `@.items[].etceteraConfiguration.price.currency` — 칸 없음(시점 다름) — P15
- `@.items[].etceteraConfiguration.price.value` — 칸 없음(시점 다름) — P15
- `@.items[].etceteraConfiguration.translsMap` — 칸 없음 — P15
- `@.items[].optionConfiguration.medicalService` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.caution` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.code` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.healthcareReimbursement` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.machines[]` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.machines[].id` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.machines[].name` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.medicines[]` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.medicines[].id` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.medicines[].name` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.procedure` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.procedure.id` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.procedure.name` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.taxation` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.unit` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.unit.type` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.configuration.unit.value` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.deleted` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.description` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.draftedDateTimeUtc` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.id` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.status` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.title` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.translsMap` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.translsMap.title` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.translsMap.title.translation` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.translsMap.title.translation.<언어>` ×5 — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.medicalService.updatedDateTimeUtc` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.optionType` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.price` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.price.currency` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.price.value` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.procedure` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.procedure.id` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.procedure.name` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.productTitle` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.translsMap` — 칸 없음 — P15
- `@.items[].optionConfiguration.translsMap.productTitle` — 칸 없음 — P15
- `@.items[].optionConfiguration.translsMap.productTitle.translation` — 칸 없음 — P15
- `@.items[].optionConfiguration.translsMap.productTitle.translation.<언어>` ×5 — 칸 없음 — P15
- `@.items[].optionConfiguration.translsMap.title` — 칸 없음 — P15
- `@.items[].optionConfiguration.translsMap.title.translation` — 칸 없음 — P15
- `@.items[].optionConfiguration.translsMap.title.translation.<언어>` ×5 — 칸 없음 — P15
- `@.items[].prepaidCardConfiguration.balance` — 칸 없음(시점 다름) — P15
- `@.items[].prepaidCardConfiguration.balance.currency` — 칸 없음(시점 다름) — P15
- `@.items[].prepaidCardConfiguration.balance.value` — 칸 없음(시점 다름) — P15
- `@.items[].prepaidCardConfiguration.description` — 칸 없음(시점 다름) — P15
- `@.items[].prepaidCardConfiguration.expirationDurationInDays` — 칸 없음(시점 다름) — P15
- `@.items[].prepaidCardConfiguration.point` — 칸 없음(시점 다름) — P15
- `@.items[].prepaidCardConfiguration.point.currency` — 칸 없음(시점 다름) — P15
- `@.items[].prepaidCardConfiguration.point.value` — 칸 없음(시점 다름) — P15
- `@.items[].prepaidCardConfiguration.price` — 칸 없음(시점 다름) — P15
- `@.items[].prepaidCardConfiguration.price.currency` — 칸 없음(시점 다름) — P15
- `@.items[].prepaidCardConfiguration.price.value` — 칸 없음(시점 다름) — P15
- `@.items[].prepaidCardConfiguration.translsMap` — 칸 없음 — P15
- `@.items[].prepaidCardConfiguration.translsMap.description` — 칸 없음 — P15
- `@.items[].prepaidCardConfiguration.translsMap.description.translation` — 칸 없음 — P15
- `@.items[].prepaidCardConfiguration.translsMap.title` — 칸 없음 — P15
- `@.items[].prepaidCardConfiguration.translsMap.title.translation` — 칸 없음 — P15
- `@.items[].priceV2.amount.currency` — 칸 없음 — P15
- `@.items[].priceV2.suppliedAmount.currency` — 칸 없음 — P15
- `@.items[].priceV2.taxFreeAmount.currency` — 칸 없음 — P15
- `@.items[].priceV2.vatAmount.currency` — 칸 없음 — P15
- `@.pendingItems[].etceteraConfiguration.price` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].etceteraConfiguration.price.currency` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].etceteraConfiguration.price.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].etceteraConfiguration.translsMap` — 칸 없음 — P15
- `@.pendingItems[].optionConfiguration.medicalService` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.caution` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.code` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.healthcareReimbursement` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.machines[]` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.machines[].id` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.machines[].name` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.medicines[]` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.medicines[].id` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.medicines[].name` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.procedure` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.procedure.id` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.procedure.name` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.taxation` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.unit` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.unit.type` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.configuration.unit.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.deleted` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.description` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.draftedDateTimeUtc` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.id` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.status` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.title` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.translsMap` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.translsMap.title` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.translsMap.title.translation` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.translsMap.title.translation.<언어>` ×5 — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.medicalService.updatedDateTimeUtc` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.optionType` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.price` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.price.currency` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.price.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.procedure` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.procedure.id` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.procedure.name` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.productTitle` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.translsMap` — 칸 없음 — P15
- `@.pendingItems[].optionConfiguration.translsMap.productTitle` — 칸 없음 — P15
- `@.pendingItems[].optionConfiguration.translsMap.productTitle.translation` — 칸 없음 — P15
- `@.pendingItems[].optionConfiguration.translsMap.productTitle.translation.<언어>` ×5 — 칸 없음 — P15
- `@.pendingItems[].optionConfiguration.translsMap.title` — 칸 없음 — P15
- `@.pendingItems[].optionConfiguration.translsMap.title.translation` — 칸 없음 — P15
- `@.pendingItems[].optionConfiguration.translsMap.title.translation.<언어>` ×5 — 칸 없음 — P15
- `@.pendingItems[].prepaidCardConfiguration.balance` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].prepaidCardConfiguration.balance.currency` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].prepaidCardConfiguration.balance.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].prepaidCardConfiguration.description` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].prepaidCardConfiguration.expirationDurationInDays` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].prepaidCardConfiguration.point` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].prepaidCardConfiguration.point.currency` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].prepaidCardConfiguration.point.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].prepaidCardConfiguration.price` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].prepaidCardConfiguration.price.currency` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].prepaidCardConfiguration.price.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].prepaidCardConfiguration.translsMap` — 칸 없음 — P15
- `@.pendingItems[].prepaidCardConfiguration.translsMap.description` — 칸 없음 — P15
- `@.pendingItems[].prepaidCardConfiguration.translsMap.description.translation` — 칸 없음 — P15
- `@.pendingItems[].prepaidCardConfiguration.translsMap.title` — 칸 없음 — P15
- `@.pendingItems[].prepaidCardConfiguration.translsMap.title.translation` — 칸 없음 — P15
- `@.pendingItems[].priceV2.amount.currency` — 칸 없음 — P15
- `@.pendingItems[].priceV2.suppliedAmount.currency` — 칸 없음 — P15
- `@.pendingItems[].priceV2.taxFreeAmount.currency` — 칸 없음 — P15
- `@.pendingItems[].priceV2.vatAmount.currency` — 칸 없음 — P15
- `@.refundingItems[]` — 칸 있음 · 미동기화 — P15
- `@.refundingItems[].adjustedPrice` — 칸 있음 · 미동기화 — P15
- `@.refundingItems[].adjustedPrice.amount` — 칸 있음 · 미동기화 — P15
- `@.refundingItems[].adjustedPrice.amount.currency` — 칸 없음 — P15
- `@.refundingItems[].adjustedPrice.amount.value` — 칸 있음 · 미동기화 — P15
- `@.refundingItems[].adjustedPrice.suppliedAmount` — 칸 있음 · 미동기화 — P15
- `@.refundingItems[].adjustedPrice.suppliedAmount.currency` — 칸 없음 — P15
- `@.refundingItems[].adjustedPrice.suppliedAmount.value` — 칸 있음 · 미동기화 — P15
- `@.refundingItems[].adjustedPrice.taxFreeAmount` — 칸 있음 · 미동기화 — P15
- `@.refundingItems[].adjustedPrice.taxFreeAmount.currency` — 칸 없음 — P15
- `@.refundingItems[].adjustedPrice.taxFreeAmount.value` — 칸 있음 · 미동기화 — P15
- `@.refundingItems[].adjustedPrice.taxation` — 칸 있음 · 미동기화 — P15
- `@.refundingItems[].adjustedPrice.vatAmount` — 칸 있음 · 미동기화 — P15
- `@.refundingItems[].adjustedPrice.vatAmount.currency` — 칸 없음 — P15
- `@.refundingItems[].adjustedPrice.vatAmount.value` — 칸 있음 · 미동기화 — P15
- `@.refundingItems[].targetItemId` — 칸 있음 · 미동기화 — P15

**`purchase_item(구성 스냅샷 — 새 표 필요)`**

- `@.items[].optionConfiguration.compositions[]` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].count` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.caution` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.code` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.healthcareReimbursement` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.machines[]` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.machines[].id` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.machines[].name` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.procedure` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.procedure.id` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.procedure.name` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.taxation` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.unit` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.unit.type` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.configuration.unit.value` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.deleted` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.description` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.draftedDateTimeUtc` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.id` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.status` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.title` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.translsMap` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.translsMap.title` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.translsMap.title.translation` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.<언어>` ×5 — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].medicalService.updatedDateTimeUtc` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.amount` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.amount.currency` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.amount.value` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.suppliedAmount` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.suppliedAmount.currency` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.suppliedAmount.value` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.taxFreeAmount` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.taxFreeAmount.currency` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.taxFreeAmount.value` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.taxation` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.vatAmount` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.vatAmount.currency` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].price.vatAmount.value` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].procedure` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].procedure.id` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].procedure.name` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].unit` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].unit.type` — 칸 없음(시점 다름) — P15
- `@.items[].optionConfiguration.compositions[].unit.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[]` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].count` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.caution` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.code` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.healthcareReimbursement` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.machines[]` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.machines[].id` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.machines[].name` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.procedure` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.procedure.id` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.procedure.name` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.taxation` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.unit` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.unit.type` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.configuration.unit.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.deleted` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.description` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.draftedDateTimeUtc` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.id` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.status` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.title` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.translsMap` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.translsMap.title` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.translsMap.title.translation` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.translsMap.title.translation.<언어>` ×5 — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].medicalService.updatedDateTimeUtc` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.amount` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.amount.currency` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.amount.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.suppliedAmount` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.suppliedAmount.currency` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.suppliedAmount.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.taxFreeAmount` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.taxFreeAmount.currency` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.taxFreeAmount.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.taxation` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.vatAmount` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.vatAmount.currency` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].price.vatAmount.value` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].procedure` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].procedure.id` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].procedure.name` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].unit` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].unit.type` — 칸 없음(시점 다름) — P15
- `@.pendingItems[].optionConfiguration.compositions[].unit.value` — 칸 없음(시점 다름) — P15

**`customer`**

- `@.address.address` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.address.detailedAddress` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.address.zipCode` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.aggrementAdvertisements` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.aggrementPersonalInformation` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.agreementInformationalNotification` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.counselor` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.counselor.id` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.createdDateTimeUtc` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.deleted` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.detailedFunnel` — 칸 없음 — P20 · P24 · P34
- `@.doctor` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.doctor.id` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.email` — 칸 있음 · 미동기화 — P20 · P24
- `@.foreignRegistrationNumber` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.funnel` — 칸 없음 — P20 · P24 · P34
- `@.language` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.passportExpiryDate` — 칸 있음 · 미동기화 — P20 · P24
- `@.passportGivenNames` — 칸 있음 · 미동기화 — P20 · P24
- `@.passportNumber` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.passportSurname` — 칸 있음 · 미동기화 — P20 · P24
- `@.recommenderName` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.registrationNumber` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.unregistered` — 칸 없음 — P20 · P24
- `@.unregistered.name` — 칸 없음 — P20 · P24
- `@.visitorCategoryId` — 칸 없음 — P20 · P24 · P34
- `@.visitorFunnel.funnelDetail` — 칸 있음 · 미동기화 — P20 · P24 · P34
- `@.visitorFunnel.funnelId` — 칸 있음 · 미동기화 — P20 · P24 · P34

**`ticket_set`**

- `@.ticketSets[].medicalService.caution` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.code` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.healthcareReimbursement` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.machines[]` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.machines[].id` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.machines[].name` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.medicines[]` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.medicines[].id` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.medicines[].name` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.procedure` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.procedure.id` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.procedure.name` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.taxation` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.unit` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.unit.type` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.configuration.unit.value` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.description` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.draftedDateTimeUtc` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.status` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.title` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.translsMap` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.translsMap.title` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.translsMap.title.translation` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.translsMap.title.translation.<언어>` ×5 — 칸 없음(시점 다름) — P16
- `@.ticketSets[].medicalService.updatedDateTimeUtc` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].procedure` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].procedure.id` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].procedure.name` — 칸 없음(시점 다름) — P16
- `@.ticketSets[].translsMap` — 칸 없음 — P16
- `@.ticketSets[].translsMap.title` — 칸 없음 — P16
- `@.ticketSets[].translsMap.title.translation` — 칸 없음 — P16
- `@.ticketSets[].translsMap.title.translation.<언어>` ×17 — 칸 없음 — P16

**`새 표 필요(병원 기본 운영 시간)`**

- `@.friday` — 칸 없음 — P26
- `@.friday.breaktime` — 칸 없음 — P26
- `@.friday.breaktime.endTime` — 칸 없음 — P26
- `@.friday.breaktime.startTime` — 칸 없음 — P26
- `@.friday.enabled` — 칸 없음 — P26
- `@.friday.endTime` — 칸 없음 — P26
- `@.friday.startTime` — 칸 없음 — P26
- `@.monday` — 칸 없음 — P26
- `@.monday.breaktime` — 칸 없음 — P26
- `@.monday.breaktime.endTime` — 칸 없음 — P26
- `@.monday.breaktime.startTime` — 칸 없음 — P26
- `@.monday.enabled` — 칸 없음 — P26
- `@.monday.endTime` — 칸 없음 — P26
- `@.monday.startTime` — 칸 없음 — P26
- `@.saturday` — 칸 없음 — P26
- `@.saturday.breaktime` — 칸 없음 — P26
- `@.saturday.breaktime.endTime` — 칸 없음 — P26
- `@.saturday.breaktime.startTime` — 칸 없음 — P26
- `@.saturday.enabled` — 칸 없음 — P26
- `@.saturday.endTime` — 칸 없음 — P26
- `@.saturday.startTime` — 칸 없음 — P26
- `@.sunday` — 칸 없음 — P26
- `@.sunday.breaktime` — 칸 없음 — P26
- `@.sunday.breaktime.endTime` — 칸 없음 — P26
- `@.sunday.breaktime.startTime` — 칸 없음 — P26
- `@.sunday.enabled` — 칸 없음 — P26
- `@.sunday.endTime` — 칸 없음 — P26
- `@.sunday.startTime` — 칸 없음 — P26
- `@.thursday` — 칸 없음 — P26
- `@.thursday.breaktime` — 칸 없음 — P26
- `@.thursday.breaktime.endTime` — 칸 없음 — P26
- `@.thursday.breaktime.startTime` — 칸 없음 — P26
- `@.thursday.enabled` — 칸 없음 — P26
- `@.thursday.endTime` — 칸 없음 — P26
- `@.thursday.startTime` — 칸 없음 — P26
- `@.tuesday` — 칸 없음 — P26
- `@.tuesday.breaktime` — 칸 없음 — P26
- `@.tuesday.breaktime.endTime` — 칸 없음 — P26
- `@.tuesday.breaktime.startTime` — 칸 없음 — P26
- `@.tuesday.enabled` — 칸 없음 — P26
- `@.tuesday.endTime` — 칸 없음 — P26
- `@.tuesday.startTime` — 칸 없음 — P26
- `@.wednesday` — 칸 없음 — P26
- `@.wednesday.breaktime` — 칸 없음 — P26
- `@.wednesday.breaktime.endTime` — 칸 없음 — P26
- `@.wednesday.breaktime.startTime` — 칸 없음 — P26
- `@.wednesday.enabled` — 칸 없음 — P26
- `@.wednesday.endTime` — 칸 없음 — P26
- `@.wednesday.startTime` — 칸 없음 — P26

**`ticket_bundle`**

- `@.optionConfiguration.productTitle` — 칸 없음(시점 다름) — P16
- `@.optionConfiguration.promotionConfiguration` — 칸 없음 — P16
- `@.optionConfiguration.translsMap` — 칸 없음 — P16
- `@.optionConfiguration.translsMap.optionTitle` — 칸 없음 — P16
- `@.optionConfiguration.translsMap.optionTitle.translation` — 칸 없음 — P16
- `@.optionConfiguration.translsMap.optionTitle.translation.<언어>` ×5 — 칸 없음 — P16
- `@.optionConfiguration.translsMap.productTitle` — 칸 없음 — P16
- `@.optionConfiguration.translsMap.productTitle.translation` — 칸 없음 — P16
- `@.optionConfiguration.translsMap.productTitle.translation.<언어>` ×5 — 칸 없음 — P16
- `@.price.currency` — 칸 없음 — P16
- `@.translsMap` — 칸 없음 — P16
- `@.translsMap.title` — 칸 없음 — P16
- `@.translsMap.title.translation` — 칸 없음 — P16
- `@.translsMap.title.translation.<언어>` ×17 — 칸 없음 — P16

**`visit`**

- `@.consultation.consultationMemo` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.consultation.counselor` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.consultation.counselor.id` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.consultation.counselor.name` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.consultation.doctor` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.consultation.doctor.id` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.consultation.doctor.name` — 칸 없음(시점 다름) — P07 · P08 · P33
- `@.reservation.reservationGroupId` — 칸 없음 — P07 · P08 · P33
- `@.reservation.statusUpdatedDateTimeUtc` — 칸 없음 — P08 · P33
- `@.reservation.zoneId` — 칸 없음 — P07 · P08 · P33

**`새 표 필요(기타 업무)`**

- `@.etceteraWorks[]` — 칸 없음 — P07 · P08 · P33
- `@.etceteraWorks[].assignees[]` — 칸 없음 — P07 · P08
- `@.etceteraWorks[].assignees[].id` — 칸 없음 — P08
- `@.etceteraWorks[].assignees[].name` — 칸 없음 — P08
- `@.etceteraWorks[].assignees[].role` — 칸 없음 — P08
- `@.etceteraWorks[].assignees[].role.id` — 칸 없음 — P08
- `@.etceteraWorks[].assignees[].role.name` — 칸 없음 — P08
- `@.etceteraWorks[].assignees[].role.roleTags[]` — 칸 없음 — P08
- `@.etceteraWorks[].etceteraWorkConfiguration` — 칸 없음 — P07 · P08
- `@.etceteraWorks[].etceteraWorkConfiguration.id` — 칸 없음 — P07 · P08
- `@.etceteraWorks[].etceteraWorkConfiguration.title` — 칸 없음 — P07 · P08
- `@.etceteraWorks[].etceteraWorkConfiguration.translsMap` — 칸 없음 — P07 · P08
- `@.etceteraWorks[].etceteraWorkConfiguration.translsMap.title` — 칸 없음 — P07 · P08
- `@.etceteraWorks[].etceteraWorkConfiguration.translsMap.title.translation` — 칸 없음 — P07 · P08
- `@.etceteraWorks[].memo` — 칸 없음 — P07 · P08
- `@.etceteraWorks[].sequence` — 칸 없음 — P07 · P08
- `@.etceteraWorks[].status` — 칸 없음 — P07 · P08

**`hospital`**

- `@.businessLicenseImageUrl` — 칸 없음 — P25
- `@.companyName` — 칸 없음 — P25
- `@.companyRegistrationNumber` — 칸 없음 — P25
- `@.hospitalCode` — 칸 없음 — P22
- `@.hospitalId` — 칸 없음 — P22
- `@.hospitalMapImageUrl` — 칸 없음 — P25
- `@.hospitalName` — 칸 없음(시점 다름) — P22 · P25
- `@.hospitalNationality` — 칸 없음 — P22
- `@.logoImageUrl` — 칸 없음 — P25
- `@.mode` — 칸 없음 — P22
- `@.namespace` — 칸 없음 — P22
- `@.nationality` — 칸 없음 — P25
- `@.nursingInstitutionNumber` — 칸 없음 — P25
- `@.qualifiedInvoiceIssuerNumber` — 칸 없음 — P25
- `@.representativeName` — 칸 없음 — P25
- `@.representativeStampImageUrl` — 칸 없음 — P25
- `@.taxBillEmail` — 칸 없음 — P25
- `@.translsMap` — 칸 없음 — P25
- `@.websiteUrl` — 칸 없음 — P25

**`purchase_transaction`**

- `@.transactions[].createdDateTimeUtc` — 칸 있음 · 미동기화 — P15
- `@.transactions[].paymentDateTime` — 칸 없음 — P15
- `@.transactions[].paymentDateTime.approvedDateTimeUtc` — 칸 없음 — P15
- `@.transactions[].paymentDateTime.canceledDateTimeUtc` — 칸 없음 — P15
- `@.transactions[].paymentDateTime.lastUpdatedDateTimeUtc` — 칸 없음 — P15
- `@.transactions[].price.currency` — 칸 없음 — P15
- `@.transactions[].suppliedAmount` — 칸 없음 — P15
- `@.transactions[].suppliedAmount.currency` — 칸 없음 — P15
- `@.transactions[].suppliedAmount.value` — 칸 없음 — P15
- `@.transactions[].taxFreeAmount` — 칸 없음 — P15
- `@.transactions[].taxFreeAmount.currency` — 칸 없음 — P15
- `@.transactions[].taxFreeAmount.value` — 칸 없음 — P15
- `@.transactions[].vatAmount` — 칸 없음 — P15
- `@.transactions[].vatAmount.currency` — 칸 없음 — P15
- `@.transactions[].vatAmount.value` — 칸 없음 — P15

**`external_ref`**

- `@.consultations[].updatedDateTimeUtc` — 칸 있음 · 미동기화 — P07 · P08 · P33
- `@.updatedDateTimeUtc` — 칸 있음 · 미동기화 — P05 · P20 · P24 · P34

**`staff`**

- `@.createdAt` — 칸 없음 — P05
- `@.defaultWorkingZoneId` — 칸 있음 · 미동기화 — P05
- `@.mfaMethods[]` — 칸 없음 — P05 · P21
- `@.profileImageUrl` — 칸 없음 — P05
- `@.userId` — 칸 없음 — P05

**`product_option_composition`**

- `@.options[].compositions[].medicineAndMachines[].id` — 칸 없음 — P10
- `@.options[].compositions[].price.amount.currency` — 칸 없음 — P10
- `@.options[].compositions[].price.suppliedAmount.currency` — 칸 없음 — P10
- `@.options[].compositions[].price.taxFreeAmount.currency` — 칸 없음 — P10
- `@.options[].compositions[].price.taxation` — 칸 없음 — P10
- `@.options[].compositions[].price.vatAmount.currency` — 칸 없음 — P10

**`prepaid_card`**

- `@.createdDateTimeUtc` — 칸 있음 · 미동기화 — P17
- `@.description` — 칸 없음 — P17
- `@.remainingBalance.balance.currency` — 칸 없음 — P17
- `@.remainingPoint.balance.currency` — 칸 없음 — P17
- `@.translsMap` — 칸 없음 — P17

**`product_option`**

- `@.options[].medicineAndMachines[].id` — 칸 없음 — P10
- `@.options[].price.suppliedAmount.currency` — 칸 없음 — P10
- `@.options[].price.taxFreeAmount.currency` — 칸 없음 — P10
- `@.options[].price.vatAmount.currency` — 칸 없음 — P10

**`purchase`**

- `@.assignee` — 칸 없음 — P15
- `@.assignee.id` — 칸 없음 — P15
- `@.assignee.name` — 칸 없음 — P15
- `@.createdDateTimeUtc` — 칸 있음 · 미동기화 — P15

**`reservation_group`**

- `@.isDefault` — 칸 없음 — P03
- `@.memo` — 칸 없음 — P03
- `@.startDate` — 칸 없음 — P03

**`consultation_procedure`**

- `@.consultations[].consultationProcedures[]` — 칸 있음 · 미동기화 — P07 · P08 · P33

**`consultation`**

- `@.consultations[].createdDateTimeUtc` — 칸 있음 · 미동기화 — P07 · P08 · P33

**`etc_task_type`**

- `@.translsMap` — 칸 없음 — P12
- `@.translsMap.title` — 칸 없음 — P12
- `@.translsMap.title.translation` — 칸 없음 — P12

**`prepaid_card_product`**

- `@.balance.currency` — 칸 없음 — P13
- `@.point.currency` — 칸 없음 — P13
- `@.price.currency` — 칸 없음 — P13

**`etcetera_product`**

- `@.price.currency` — 칸 없음 — P14
- `@.translsMap` — 칸 없음 — P14

**`visit (태그 — 새 표 필요)`**

- `@.reservationTagIds[]` — 칸 없음 — P08

**`product`**

- `@.medicineAndMachines[].id` — 칸 없음 — P10

**`ticket`**

- `@.ticketSets[].tickets[].createdDateTimeUtc` — 칸 있음 · 미동기화 — P16

**`prepaid_card_ledger`**

- `@.amount.amount.currency` — 칸 없음 — P18

</details>

### K3-3. `확인 안 됨` 키(K5 로 이어짐)

- P07: `data[].schedules[].consultations[].visitor.isNew` · `data[].schedules[].reactions[]` · `data[].schedules[].taskTimers[]` · `data[].schedules[].tasks[].procedureConfiguration.productOptionConfiguration.medicineAndMachines[]`
- P08: `data.consultations[].visitor.isNew` · `data.reactions[]` · `data.taskTimers[]` · `data.tasks[].procedureConfiguration.productOptionConfiguration.medicineAndMachines[]`
- P10: `data[].options[].compositions[].price.additional[]`
- P15: `data[].items[].optionConfiguration.compositions[].medicalService.configuration.medicines[]` · `data[].items[].optionConfiguration.compositions[].medicineAndMachines[]` · `data[].items[].optionConfiguration.compositions[].price.additional[]` · `data[].items[].optionConfiguration.medicineAndMachines[]` · `data[].pendingItems[].optionConfiguration.compositions[].medicalService.configuration.medicines[]` · `data[].pendingItems[].optionConfiguration.compositions[].medicineAndMachines[]` · `data[].pendingItems[].optionConfiguration.compositions[].price.additional[]` · `data[].pendingItems[].optionConfiguration.medicineAndMachines[]` · `data[].revokingItems[]`
- P25: `data.languages[]`
- P27: `data[]`
- P33: `data[].consultations[].visitor.isNew` · `data[].reactions[]` · `data[].taskTimers[]` · `data[].tasks[].procedureConfiguration.productOptionConfiguration.medicineAndMachines[]`

## K4. 동기화 범위 — 키가 아니라 범위 때문에 비는 것

키를 다 받아도 **그 행이 DAY 에 들어오지 않는** 자리. 근거는 앞 판 §B3 표와 코드 줄.

| # | 무엇이 비나 | 영향받는 경로 · 키 | 왜(범위) | 근거 | 앞 판 |
|---|---|---|---|---|---|
| R1 | **미래 일정 전부** | P07 의 일정 행 전체(방문 · 점유 · 작업 · 희망 시술 · 상담) | 일정 동기화 창 = 병원 현지 **오늘 00:00 ~ 다음 날 00:00** | `services/emr_sync.py:111-115` · `tasks/emr.py:3-4` | E4 · E6 · C2 |
| R2 | 과거 일정 | P07 · P15 ~ P19 의 지난 행 | 수동 백필(`python -m runtime.backfill`) · **어제까지** · 운영 동기화와 따로 | `services/emr_backfill.py:1-17` | E5 · E8 이전 방문 |
| R3 | 오늘 일정 없는 고객의 **고객 정보 갱신** | 고객 칸 전부(P24 계열 `저장됨` 칸도 그 고객이 마지막으로 일정에 나온 때 값) | 고객 행은 일정 반영으로만 들어온다 — 백필도 「고객 목록은 나열에만」 | `services/emr_backfill.py:11-13` · `emr/kos/mapper.py:558` | E2 · C1 |
| R4 | 오늘 일정 없는 고객의 **시술권 · 선불카드 · 구매** | P15 ~ P19 | 판매 동기화는 일정 회차 뒤 「오늘 일정 응답의 참조」만(오늘 일정 없으면 발행 안 함) · 그 밖은 백필 시점 값. S0:1775 「오늘 밖 고객의 변경 다시 열림 · 후보 = `get-visitors` 하루 한 번(DAY-SPEC-002 OQ-76)」 | `tasks/emr.py:74-85 · 98-105` · `services/emr_sale_sync.py:257-268` | E2 · C3 |
| R5 | **칸 정원 · 예약 수** | P28(HAR 없음) | S0:907 · 1002 「칸별 정원 · 예약 수는 테이블로 두지 않는다 — 정원(`reservation_group_capacity`)과 방문 점유에서 계산」 — 그런데 R1 때문에 **미래 `visit_occupied_resource` 가 없어 계산할 재료가 없다** | `S0:907` · `S0:1002` · `services/emr_sync.py:111` | E4 · C2 |
| R6 | `get-codes` 의 다른 범주 | P06 응답의 `category` = `CONSULTATION_RESULT` · `IMAGE_CATEGORY` · `IMAGE_EQUIPMENT`(HAR 에 응답 있음) | DAY 는 `VISITOR_CATEGORY` · `FUNNEL_CATEGORY` · `FUNNEL` 세 범주만 부른다 — 키 모양은 같고(P06 8키) 범주가 빠진다 | `emr/kos/__init__.py:138-151` · 독스트링 `:13-14` | — |
| R7 | 병원 기본 운영 시간 · 기본 휴무 · 그룹 휴무 · 병원 정보 | P25 · P26 · P27 · HAR 에만 `get-reservation-group-days-offs` | 경로 자체를 부르지 않는다 | K1 「부르지 않음」 | E12 · C14 |
| R8 | 예약 상세(P08) 의 작업 밖 키 | P08 의 방문 · 고객 · 상담 키 | DAY 는 P08 에서 `tasks` 만 읽고, 그것도 이벤트 때만(작업 다시 읽기) — 나머지는 P07 이 오늘 창에서 채우는 칸과 같다 | `emr/kos/__init__.py:210-216` · `emr/kos/mapper.py:511-528` · `services/emr_sync.py:324 · 364` | — |
| R9 | 고객 목록(P20) | P20 의 `id` 밖 62키 | `id` · `count` 만 읽고 백필(수동) 때만 부른다 | `emr/kos/sale_reads.py:316-333` · `services/emr_backfill.py:396` | — |
| R10 | 문진 | P30 · P31(HAR 없음) · HAR 에만 내부 `get-questionnaire-submit/legacy` | 경로 미호출 · `questionnaire_history` 표(`models/reception.py:88-99`)는 있으나 쓰는 동기화 코드 0 | 앞 판 B1 「E8 health」 | E8 · C17 |
| R11 | 처방 내용 | HAR 에만 `prescription/v1/...` 3경로 | `prescription` 표는 `id` · `visit_id` 만(`models/prescription.py:15-20`) — 일정의 `prescriptionIds[]` 로 연결만 | `emr/kos/mapper_purchase.py:104` | — |
| R12 | 선불카드 이력 · 공유 고객 | P18 · P19 | 「바뀐 카드」만 다시 읽는다(오늘 고객 · 백필) | `services/emr_sale_sync.py:268` · `services/emr_backfill.py:430` | — |

## K5. HAR 로 확인 안 되는 것

### K5-1. HAR 에 응답이 없는 경로 — 6

| # | 경로 | 갈래 | DAY 가 읽는 키(매퍼) | 비고 |
|---|---|---|---|---|
| P23 | `common/user/v1/queries/get-active-sign-ins` | DAY 부름 | `data[]{id, userAgent, ipAddress, signedInDateTimeUtc}`(`emr/kos/mapper.py:666-676`) | 로그인 HAR 에 없음 |
| P28 | `schedule/open/v2/queries/get-reservation-slots-by-groups` | 새로 필요(공개) | — | KOS 웹 HAR 은 내부 API 만 — 공개 경로는 HAR 로 볼 수 없다. cc 는 `capacity` · `reservationCount` 를 읽었다(앞 판 E4) |
| P29 | `schedule/open/v1/queries/get-schedules-by-visitor` | 새로 필요(공개) | — | 같은 이유 · 내부 쪽 후보는 HAR 에만 `schedule/v2/queries/get-schedule-list-items`(예약이력.har) — 같은 응답인지 확인 안 됨 |
| P30 | `visitor/open/v1/queries/get-visitor-questionnaire` | 새로 필요(공개) | — | 같은 이유 |
| P31 | `visitor/open/v1/queries/get-questionnaire-submit` | 새로 필요(공개) | — | 내부 쪽 후보 = HAR 에만 `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy`(26 엔트리 · 200+JSON 3) — 같은 응답인지 확인 안 됨 |
| P32 | `schedule/v1/queries/get-schedule-event-logs` | 새로 필요(내부) | — | 내부인데도 67개 HAR 어디에도 없다 |

### K5-2. DAY 가 읽는데 HAR 에서 키 · 값을 못 본 것 — 11

| # | 키(경로) | DAY 매퍼 | HAR 에서 본 것 |
|---|---|---|---|
| 1 | 일정 `reservation.desiredDischargeDateTimeUtc`(P07 · P08) | `emr/kos/mapper.py:587` → `visit.desired_discharge_at` | **키 자체가 없다**(P07 · P08 · P33 합집합 · HAR 에만 경로까지 전부 0) |
| 2 | 일정 `reservation.requestedProcedures[]` 안쪽(P07 · P08) | `emr/kos/mapper.py:332-360 · 536-541` | P07 · P08 · P33 에서 늘 빈 배열. 안쪽 키는 **HAR 에만 있는 `get-schedule-summaries`** 응답에만 있다(`type: OPTION` · `optionConfiguration{optionId, optionTitle, productTitle, optionType, price{amount, currency, reason.type}, medicalService{…}, compositions[], translsMap}`) — DAY 가 읽는 칸 이름 · 모양(`price.amount` 정수)과 맞는다. 다른 경로라 같은 모양인지는 확인 안 됨 |
| 3 | 희망 시술 `ticketConfiguration.{productTitle, ticketTitle}` | `emr/kos/mapper.py:338-346` | 어디에도 없다(`type: TICKET` 행 0) |
| 4 | `occupiedResources[].reservationGroup.doctors[]` 안쪽 | `emr/kos/mapper.py:380-384` → `visit_occupied_resource_doctor` | 늘 빈 배열 |
| 5 | `reservation.doctor.id`(희망 의사) | `emr/kos/mapper.py:575-577` | 키는 있으나 **늘 빈 문자열** |
| 6 | `consultations[].consultationProcedures[]` | 받지 않음(`emr/kos/mapper.py:500` 「안쪽 키 미관찰」) | 늘 빈 배열 — 그대로 미관찰 |
| 7 | 상품 옵션 `price.additional[]`(수가 유형별 가격) | `emr/kos/mapper_menu.py:83-90 · 115-116` → `product_option_price` | 늘 빈 배열 |
| 8 | 상품 · 옵션 `badges[]` · `promotionConfigurations[]` | `emr/kos/mapper_menu.py:136-137 · 171` | 늘 빈 배열 |
| 9 | 구매 · 항목 `priceAdjustments[]` 안쪽 | `emr/kos/mapper_purchase.py:221-226`(관계만) | 늘 빈 배열(S0 OQ-08-4 의 데모 표본 1건은 HAR 에 없다) |
| 10 | 카드 이력 `amount.type` · `type` | `emr/kos/mapper_sale_values.py:60-65` | `POINT` · `CHARGE` · `PAYMENT` 만 — `BALANCE` · `REFUND` 미관찰 |
| 11 | 로그인 `mfaMethods[]`(P21) | `emr/kos/mapper.py:653-656` | 늘 빈 배열 — 값 모양 미관찰 |

### K5-3. 값 · 문서와 HAR 이 다른 것(사실만)

| # | 무엇 | HAR | DAY · 문서 |
|---|---|---|---|
| 1 | 결제 수단 `CARD` | P15 `transactions[].paymentType` enum 에 `CARD` · `cardConfiguration{approvalNumber, cardCompany.name}` | 매핑 표 `CASH` · `PREPAID_CARD` · `TRANSFER` 만(`emr/kos/mapper_sale_values.py:47-52`) → 표 밖이면 `MappingError` 로 그 거래 행을 뺀다(`emr/kos/mapper_purchase.py:165-168 · 192-204`). S0 OQ-08-5(:1821) 는 「KOS paymentType 문자열(표본 0)」 |
| 2 | 고객 단건의 전화번호 | P24 `data.phoneNumber{countryCode, phoneNumber}` 있음 | `S0:412` 「**전화번호는 이 응답에 없다**」(고객상세.har 기준) — HAR 합집합과 다르다(어느 HAR 엔트리에서 생긴 키인지는 부록 B · 응답마다 키가 다를 수 있다) |
| 3 | 구매 응답 키 `conversion` · `purchaseMemo` · `migratedDateTimeUtc` | P15 합집합에 **없다** | `S0:1824`(OQ-08-10) 「구매 응답에만 있는 키」 — 데모 실호출에서 본 것으로 보이며 HAR 로는 확인 안 됨 |
| 4 | 병원 기본 휴무 | P27 22개 응답 모두 빈 배열 | cc 는 `startDateTime` · `endDateTime` 을 읽었다(앞 판 E12) — 키 확인 안 됨 |
| 5 | 일정 `reservation.statusUpdatedDateTimeUtc` · `reservationTagIds[]` | `statusUpdatedDateTimeUtc` 는 P08 · P33, `reservationTagIds[]` 는 P08 에만(P07 엔 둘 다 없음) | S0 에 언급 없음(`grep` 0) |

### K5-4. `확인 안 됨` 판정 키 — 24

K3-3 목록. 전부 「HAR 에서 늘 빈 배열 · 빈 객체」라 안쪽 키를 못 본 것이다.

## K6. 정할 것 (결정하지 않음)

| # | 질문 | 선택지 | 근거(사실) | 앞 판 |
|---|---|---|---|---|
| K6-1 | **메뉴 참조의 「그때 값」 스냅샷 범위** — 구매 항목 · 시술권 세트 · 작업 · 희망 시술이 가리키는 상품 · 옵션 · 시술 항목 · 구성의 산 시점 값을 어디까지 칸으로 둘지 | ① data_rules 대로 KOS 가 주는 스냅샷 전부(구성 · 시술 항목 · 정가 · 단위 · 과세) ② 이름 · 가격 · 단위만(지금 수준 + 빠진 것 몇) ③ 지금 메뉴 join 으로 충분(규칙 예외로 적음) | `칸 없음(시점 다름)` 306행 중 대부분(K3-2 `purchase_item` · 구성 스냅샷 새 표 · `ticket_set` · `ticket_bundle` · `visit_task`) · data_rules 「메뉴 참조 = id + 그때 값(이름 · 가격 · 진료항목) 스냅샷」 | — |
| K6-2 | **고객 미동기화 칸(DAY 칼럼 22개)의 원천** | ① 일정 회차에서 바뀐 고객만 `get-visitor` 1회 ② 백필이 이미 부르는 `get-visitors` 목록에서 전부 읽기(+ 하루 한 번 훑기 — S0:1775 OQ-76) ③ ①+② | P20 목록 응답 = P24 단건과 같은 키 63 + `count`(K2) · 지금은 `id` 만(`emr/kos/sale_reads.py:316-333`) · R3 | C1(email) |
| K6-3 | 암호화 대상 3칸(`registrationNumber` · `foreignRegistrationNumber` · `passportNumber`)을 K6-2 에 넣을 때 범위 | ① 같이 받는다(칼럼은 「암호화 text」 S0:338-340) ② 따로 정한다 | data_rules 「민감한 개인정보는 암호화해 저장」 · DAY 칼럼 있음(`models/customer.py:56-58`) | — |
| K6-4 | 결제 수단 `CARD` 매핑 | ① HAR 실측대로 표에 더함(+ `cardConfiguration` 은 `payment_config` JSON) ② OQ-08-5 표본(플랫폼 · 간편결제 · 의료대출)까지 모은 뒤 한 번에 | K5-3 #1 — 지금 카드 결제 거래 행이 동기화에서 빠진다 | — |
| K6-5 | 거래 금액 분해(공급 · 면세 · 부가세) · 승인 / 취소 시각(`paymentDateTime`) · 거래 생성 시각 | ① 칸 추가 ② 그대로(「부호 있는 금액」만) | S0 OQ-08-5(a)(:1821) 열림 · 사용자 11-20 「KOS 키 다 저장」 | — |
| K6-6 | 미래 일정의 원천(동기화 창) | ① 창을 미래로 넓힘(며칠 · 어떤 주기) ② 미래만 다른 경로 ③ 범위 밖 | R1 · R5 | C2 |
| K6-7 | 칸 정원 · 예약 수 | ① S0:907 대로 계산(K6-6 이 미래를 열어야 가능) ② `get-reservation-slots-by-groups` 동기화 | R5 · P28 HAR 없음 | C2 |
| K6-8 | 병원 정보(P25) — **`S0:278` 「hospital 의 phone · address 는 두지 않는다」와 사용자 11-20 지시 충돌** | ① S0:278 을 뒤집어 병원 설정 칸(이름 · 전화 · 주소 · 사업자 · 언어 …)을 둠 ② 유지(ext E12 는 KOS 실시간) ③ 일부만 | P25 22행(칸 없음 13 · 일부러 안 둠 6 · 시점 다름 1 · 확인 안 됨 1 · 해당 없음 1) | C14 |
| K6-9 | **`일부러 안 둠` 54행 재검토** — 사용자 11-20 「KOS 가 주는 키는 다 저장」과 기존 결정이 부딪히는 것: `featureList`(S0:611) · `migratedMemo` · `customAttributes` · `lineInformation` · `unniInformation`(S0:311-317) · 고객 `isNew`(S0:360) · 시술권 장 `price`(S0:1668) · 카드 `total`(S0:1698) · `categoryIds`(S0:1429) · 작업 `optionId`(S0:892) · 희망 시술 가격 사유 · 진료항목 구성(S0:510) · 병원 전화 · 주소(S0:278) | 항목마다 ① 유지 ② 뒤집어 칸 추가 | K2 판정 `일부러 안 둠` 행 · 근거 줄 | — |
| K6-10 | 일정 **단일 상담 정보**(`consultation.{consultationMemo, counselor, doctor}`)를 칸으로 둘지 | ① `visit` 에 칸(시점이 다른 상담사 · 원장 · 메모) ② 상담 기록(`consultation`)으로 충분 | 시점 다름 3키(K2 P07 · P08 · P33) · 앞 판 M2 · M3 | C4 · C5 |
| K6-11 | 상담 기록의 **상담사 · 원장이 둘 이상**일 때 | ① 사람 목록 표 ② 지금처럼 1명일 때만(`emr/kos/mapper.py:491-494` · OQ-13) | KOS 는 배열(`counselors[]` · `consultationDoctors[]`) | C4 |
| K6-12 | 일정의 나머지 키 — `etceteraWorks[]`(기타 업무) · `taskTimers[]` · `reactions[]` · `tasks[].urgencyLevel` · `reservationTagIds[]` · `reservation.statusUpdatedDateTimeUtc` · 예약 단위 `reservation.reservationGroupId · zoneId` | 항목마다 ① 칸 / 표 ② 범위 밖 | S0 OQ-05-1(:1850) · OQ-03-1(:1789) 열림 · 나머지는 S0 언급 없음 | — |
| K6-13 | **KOS 생성 시각** — S0 가 `created_at ← createdDateTimeUtc` 로 적은 5표(구매 · 거래 · 시술권 · 선불카드 · 상담 기록) + 고객 `registered_at` | ① `created_at` 에 KOS 값 ② 따로 칸(고객 `registered_at` 처럼) ③ 그대로(DAY 행 생성 시각) | `S0:537 · 1549 · 1601 · 1665 · 1695 · 330` · data_rules 「DAY 테이블에는 created_at · updated_at · deleted_at 만」 · 코드는 안 받음 | — (앞 판 E2 `purchasedDate` · `issuedDate`) |
| K6-14 | `external_ref.external_updated_at` 을 안 채우는 엔티티(고객 · 직원 · 상담 기록) | ① 채움(바뀐 것만 받기) ② 그대로 | `칸 있음 · 미동기화` 행(K3-2 `external_ref`) · 고객은 `external_number` 만(`emr/sync_schedules.py:150`) | — |
| K6-15 | 번역(`translsMap`) — 작업 · 기타 작업 종류 · 시술권 · 카드 · 기타 품목 · 스냅샷의 번역 칸 | ① 메뉴처럼 jsonb 로 둠 ② 범위 밖 | `칸 없음` 431 중 번역 잎 246 · 메뉴 표는 이미 jsonb(`models/menu.py:56 · 75 · 124 · 187 · 269`) | — |
| K6-16 | 통화(`currency`) | ① 금액 칸마다 통화 ② 병원(또는 연결) 단위 하나 ③ 그대로(옵션 · 희망 시술만) | HAR 은 `KRW` 만 · 통화 칸은 `product_option.currency` · `visit_requested_procedure.currency` 뿐 | 앞 판 E1 · E2 |
| K6-17 | **HAR 에만 있는 읽기 경로 43** 중 다음 판 대조 대상 | 예: 상담 기록 `get-consultations-by-visitor-id` · 일정 이력 `get-schedule-list-items` · 일정 요약 `get-schedule-summaries` · 예약 그룹 휴무 · 예약 칸 · 처방 3 · 고객 이미지 · 파일 · 문진 legacy | K1-2 | — |
| K6-18 | HAR 로 못 본 6경로 · 빈 배열 키 24 · K5-2 11 을 무엇으로 확인할지 | ① 데모 테넌트 조회(tools.md 「KOS 확인(조회만)」 — 데모 키만) ② HAR 추가 요청 ③ 그대로 | K5 | — |
| K6-19 | 직원 `default_zone_id`(칼럼 있음 · 매퍼 없음) | ① 매퍼에 더함 ② 그대로 | `models/staff.py:56` · `S0:663` · `emr/kos/mapper.py:231-251` | — |
| K6-20 | 구매 대표 담당 `assignee` | ① 칸(대표 · 순서) ② `purchase_assignee` 로 충분 | S0 OQ-08-3(:1819) 열림 | — |
| K6-21 | 진행 중 환불 `refundingItems[]` | ① 매퍼에 더함(S0:1568 이 이미 원천으로 적음) ② 그대로 | `칸 있음 · 미동기화` 12행(K2 P15) | — |
| K6-22 | 희망 시술 옵션 id(`visit_requested_procedure.product_option_id`) | ① 이제 메뉴 표가 있으니 채움 ② 「1차는 비워 둔다」 유지 | `S0:551`(OQ-041-7) · `emr/kos/mapper.py:333-336` 「1차 메뉴 테이블 없음」 — 메뉴 표는 2026-11-18 생김(`models/menu.py:100`) | — |

정할 것 = **22**.

## 부록 A. 재현 — 스크립트 · 명령

스크립트는 scratchpad 에만 두었다(워크트리에 없음). 실행은 `python3 -I`(현재 폴더 import 막음). HAR 내용 사본은 남기지 않았다 — 중간 산출 `keys.pkl` 은 **키 경로 · 모양만**(enum 은 KOS 코드값만) 담았고 리포트를 쓴 뒤 지웠다.

```sh
R=/Users/kknaks/git/toy_pr2/kknaks_profile/reference
find $R -name "*.har" | wc -l                      # 67
python3 -I keys.py $R paths                        # 읽기 경로별 엔트리 수 · 200 수 · 폴더
python3 -I keys.py $R keys <KOS 경로>              # 그 경로의 키 합집합(모양만)
python3 -I collect.py $R x                         # 한 번 읽어 keys.pkl(키 · 모양 · 엔트리 위치)
python3 -I gen.py                                  # K1 · K2 · K3 · 부록 B 본문
python3 -I k13.py                                  # K1-2
python3 -I verify.py <리포트> $R ; python3 -I verify2.py <리포트> $R   # 부록 C
```

판정 규칙(`rules.py`)이 K2 의 「DAY 칸 · 근거 · 판정 · 비고」 그대로다 — 규칙은 정규식(경로 뿌리 `@` 기준) 첫 일치. 규칙에 안 걸리면 묶음(객체 · 배열)은 `해당 없음`, 빈 값만 관찰은 `확인 안 됨`, 나머지는 `칸 없음` — **이 기본값으로 떨어진 키는 0**(검토 출력 `default: 0`). 「늘 빈 배열」 메모가 붙은 행은 모양이 비어 있지 않거나 하위 키가 있으면 걸러 내는 검사를 돌려 0건을 확인했다.

<details><summary><code>keys.py</code></summary>

```python
# 일회용: HAR 응답 JSON 의 키 경로 · 타입 모양만 뽑는다. 값은 출력하지 않는다(KOS 코드 enum 만 화이트리스트).
# 헤더 · 쿠키 · 요청 본문은 읽지 않는다. 결과는 stdout 만(파일로 남기지 않음).
import json, sys, re, glob, base64, collections
from urllib.parse import urlsplit
ROOT = sys.argv[1]; MODE = sys.argv[2]; ARG = sys.argv[3:] 
UUID = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
IDKEY = re.compile(r'^(\d+|[0-9a-fA-F-]{36})$')
ENUM_KEY = re.compile(r'(status|Status|type|Type|kind|Kind|step|Step|gender|Gender|category|Category|currency|Currency|language|Language|unit|Unit|state|State|dayOfWeek|DayOfWeek|eventType|level|Level|method|Method|sex|Sex|purpose|Purpose|discriminator|reason|Reason|channel|Channel|by|order|direction|code|Code|format|Format|weekday|Weekday|policy|Policy|mode|Mode|scope|Scope|grade|Grade|result|Result|target|Target)$')
DENY_KEY = re.compile(r'(?i)(name|memo|note|text|email|phone|mobile|address|number|title|description|content|passport|birth|chart|nation|country|zip|url|path|file|token|password|key|id)$')
ENUM_VAL = re.compile(r'^([A-Z][A-Z0-9]*(_[A-Za-z0-9]+)*|[A-Z][a-z]+Type_[A-Z_]+|[a-z]{2}(-[A-Z]{2})?|[A-Z][A-Za-z]+)$')
def shape(k, v):
    if v is None: return 'null'
    if isinstance(v, bool): return 'bool'
    if isinstance(v, int): return 'int'
    if isinstance(v, float): return 'number'
    if isinstance(v, str):
        if v == '': return 'string(empty)'
        if UUID.match(v): return 'string(uuid)'
        if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?Z$', v): return 'string(ISO UTC)'
        if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?[+-]\d{2}:?\d{2}$', v): return 'string(ISO offset)'
        if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?$', v): return 'string(ISO local)'
        if re.match(r'^\d{4}-\d{2}-\d{2}$', v): return 'string(date)'
        if re.match(r'^\d{2}:\d{2}(:\d{2})?$', v): return 'string(HH:MM)'
        if re.match(r'^-?\d+$', v): return 'string(digits)'
        if re.match(r'^-?\d+\.\d+$', v): return 'string(decimal)'
        if re.match(r'^https?://', v): return 'string(url)'
        if '@' in v and '.' in v: return 'string(email꼴)'
        if re.match(r'^[\d\-+() ]{7,}$', v): return 'string(숫자·기호)'
        if re.match(r'^[A-Za-z0-9+/=_-]{40,}$', v): return 'string(token꼴)'
        if ENUM_KEY.search(k) and not DENY_KEY.search(k) and ENUM_VAL.match(v) and len(v) <= 40: return 'ENUM:' + v
        return 'string'
    if isinstance(v, dict): return 'object'
    if isinstance(v, list): return 'array'
    return type(v).__name__
def walk(node, path, acc, key=''):
    if isinstance(node, dict):
        ks = list(node.keys())
        if ks and all(IDKEY.match(x) for x in ks):
            acc[path + '{id}'].add('object(map)')
            for x in ks: walk(node[x], path + '{id}.', acc, '')
            return
        if path: acc[path.rstrip('.')].add('object' if ks else 'object(empty)')
        for x in ks: walk(node[x], path + x + '.', acc, x)
    elif isinstance(node, list):
        p = path.rstrip('.') + '[]'
        acc[p].add('array' if node else 'array(empty)')
        for x in node: walk(x, p + '.', acc, key)
    else:
        acc[path.rstrip('.')].add(shape(key, node))
def kospath(url):
    p = urlsplit(url).path
    if '/tenants/' in p: p = re.sub(r'^.*?/tenants/[^/]+/', '', p)
    else: p = p.lstrip('/')
    return p
def entries():
    for f in sorted(glob.glob(ROOT + '/**/*.har', recursive=True)):
        rel = f[len(ROOT)+1:]
        h = json.load(open(f, encoding='utf-8'))
        for i, e in enumerate(h['log']['entries']):
            p = kospath(e['request']['url'])
            if '/queries/' not in p and '/commands/' not in p: continue
            yield rel, i, p, e
def body(e):
    c = e['response'].get('content', {}); t = c.get('text')
    if t is None: return None, 'no-text'
    if c.get('encoding') == 'base64':
        try: t = base64.b64decode(t).decode('utf-8')
        except Exception: return None, 'b64-fail'
    try: return json.loads(t), 'ok'
    except Exception: return None, 'not-json'
if MODE == 'paths':   # 읽기 경로별 엔트리 수 · 응답 상태
    c = collections.defaultdict(list)
    for rel, i, p, e in entries():
        if '/queries/' not in p: continue
        b, st = body(e)
        c[p].append((rel, i, e['response']['status'], st))
    for p in sorted(c): 
        L = c[p]; ok = sum(1 for x in L if x[3]=='ok' and x[2]==200)
        print(f'{p}\t{len(L)}\tok200={ok}\t' + ' '.join(sorted({x[0].split("/")[0] for x in L})))
elif MODE == 'where':  # 경로의 엔트리 위치
    for rel, i, p, e in entries():
        if p == ARG[0]:
            b, st = body(e); print(f'{rel}#{i}\t{e["response"]["status"]}\t{st}')
elif MODE == 'keys':   # 경로의 키 합집합
    acc = collections.defaultdict(set); n = 0
    for rel, i, p, e in entries():
        if p != ARG[0]: continue
        b, st = body(e)
        if st != 'ok' or e['response']['status'] != 200: continue
        n += 1; walk(b, '', acc)
    print(f'# responses={n} keys={len(acc)}')
    for k in sorted(acc):
        s = acc[k]; en = sorted(x[5:] for x in s if x.startswith('ENUM:')); o = sorted(x for x in s if not x.startswith('ENUM:'))
        if en: o.append('enum:' + '|'.join(en) if len(en) <= 15 else f'enum({len(en)}종)')
        print(f'{k}\t{" / ".join(o)}')
```

</details>

<details><summary><code>collect.py</code></summary>

```python
# 일회용: HAR 를 한 번 읽어 대상 경로의 키 합집합(모양만) · 엔트리 위치를 pickle 로 — 값은 담지 않는다(enum 화이트리스트만)
import sys, runpy, pickle, collections
ROOT = sys.argv[1]
K = runpy.run_path(sys.argv[2], run_name='keysmod') if False else None
sys.argv = ['k', ROOT, 'none']
K = runpy.run_path('/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-day-cc-mig/e39d60ae-ec21-487b-ab3f-1fd72bdeef25/scratchpad/kos/keys.py')
out = {}
allq = collections.defaultdict(list)
for rel, i, p, e in K['entries']():
    if '/queries/' not in p: continue
    b, st = K['body'](e)
    allq[p].append((rel, i, e['response']['status'], st))
    if st != 'ok' or e['response']['status'] != 200: continue
    d = out.setdefault(p, collections.defaultdict(set))
    K['walk'](b, '', d)
pickle.dump({'keys': {p: dict(v) for p, v in out.items()}, 'entries': dict(allq)}, open('/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-day-cc-mig/e39d60ae-ec21-487b-ab3f-1fd72bdeef25/scratchpad/kos/keys.pkl', 'wb'))
print(len(out), sum(len(v) for v in out.values()))
```

</details>

<details><summary><code>classify.py</code></summary>

```python
import pickle, re, runpy
D = pickle.load(open('/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-day-cc-mig/e39d60ae-ec21-487b-ab3f-1fd72bdeef25/scratchpad/kos/keys.pkl', 'rb'))
R = runpy.run_path('/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-day-cc-mig/e39d60ae-ec21-487b-ab3f-1fd72bdeef25/scratchpad/kos/rules.py')
RULES = R['RULES']
def rel(key, root):
    if key == root: return '@'
    if key.startswith(root + '.'): return '@' + key[len(root):]
    return key
def classify(path):
    root, rules = RULES[path]
    rows = []
    for k in sorted(D['keys'][path]):
        shapes = D['keys'][path][k]
        rk = rel(k, root)
        hit = None
        for (p, v, c, n, t) in rules:
            if re.fullmatch(p, rk): hit = (v, c, n, t, p); break
        if hit is None:
            plain = {s for s in shapes if not s.startswith('ENUM:')}
            if plain and plain <= {'object', 'array', 'object(map)'}: hit = ('F', '', '묶음', '', '*generic')
            elif plain and plain <= {'array(empty)', 'object(empty)'}: hit = ('U', '', '빈 값만 관찰 — 안쪽 키 확인 안 됨', '', '*generic')
            else: hit = ('C', '', '', '', '*default')
        rows.append((k, shapes, hit))
    return rows
```

</details>

<details><summary><code>rules.py</code></summary>

```python
# 일회용: KOS 응답 키 → DAY 칸 판정 규칙. 값은 다루지 않는다(키 경로만).
# 판정 코드: A 저장됨 · B 칸 있음·미동기화 · C 칸 없음 · C2 칸 없음(시점 다름) · D 일부러 안 둠 · E 계산으로 대체 · F 해당 없음 · U 확인 안 됨
# 근거 줄: CENTURION_DAY origin/dev 844eace4 `backend/` 아래 · mediness origin/main ccede286 `products/day/20-spec/spec-000-data-model.md`(= S0)
V = {'A': '저장됨', 'B': '칸 있음 · 미동기화', 'C': '칸 없음', 'C2': '칸 없음(시점 다름)', 'D': '일부러 안 둠',
     'E': '계산으로 대체', 'F': '해당 없음', 'U': '확인 안 됨'}
M = 'emr/kos/mapper.py:'; MM = 'emr/kos/mapper_menu.py:'; MP = 'emr/kos/mapper_purchase.py:'; MV = 'emr/kos/mapper_sale_values.py:'
mv = 'models/visit.py:'; mc = 'models/customer.py:'; mr = 'models/room.py:'; ms = 'models/staff.py:'; mt = 'models/task.py:'
mm = 'models/menu.py:'; mpu = 'models/purchase.py:'; mpc = 'models/prepaid_card.py:'; mti = 'models/ticket.py:'
S0 = 'S0:'
ER = 'external_ref.external_id (' + mc + '106)'
EU = 'external_ref.external_updated_at (' + mc + '108)'
TR = r'(\..*)?'  # 하위 전부

def r(p, v, col='', note='', tbl=''):
    return (p, v, col, note, tbl)

# ---------- 일정 객체(@ = 일정 1건) ----------
SCHED = [
    r(r'@\.id', 'A', ER, M + '555'),
    r(r'@\.updatedDateTimeUtc', 'A', EU, M + '556 · emr/sync_schedules.py:271'),
    r(r'@\.deleted', 'A', 'visit.deleted_at (S0:477)', M + '557 · emr/sync_schedules.py:314'),
    r(r'@\.createdDateTimeUtc', 'A', 'visit.booked_at (' + mv + '68)', M + '559'),
    r(r'@\.flowStep', 'A', 'visit.flow_step (' + mv + '86)', M + '588-590'),
    r(r'@\.flowStepUpdatedDateTimeUtc', 'A', 'visit.flow_step_at (' + mv + '87)', M + '591'),
    r(r'@\.receptionDateTimeUtc', 'A', 'visit.reception_at (' + mv + '88)', M + '592'),
    r(r'@\.zone\.id', 'A', 'visit.reception_zone_id (' + mv + '89)', M + '593'),
    r(r'@\.zone\.title', 'E', 'join zone.title (' + mr + '35)', '구역 이름 — 기준 정보 1시간'),
    r(r'@\.visitorLocation\.zoneId', 'A', 'visit.current_zone_id (' + mv + '90)', M + '594-596'),
    r(r'@\.orderMemo', 'A', 'visit.procedure_order_note (' + mv + '92)', M + '598'),
    r(r'@\.purchaseIds\[\]', 'A', 'purchase.visit_id (' + mpu + '58)', MP + '103 · S0:500'),
    r(r'@\.prescriptionIds\[\]', 'A', 'prescription.visit_id (models/prescription.py:20)', MP + '104 · S0:501'),
    r(r'@\.purchases\[\]' + TR, 'E', 'purchase.visit_id (' + mpu + '58)', 'S0:500 — purchaseIds[] 로 받는다 · HAR 에서 늘 빈 배열(안쪽 키 확인 안 됨)'),
    r(r'@\.reactions\[\]' + TR, 'U', '', 'HAR 에서 늘 빈 배열 · S0 OQ-03-1(:1789) 열림'),
    r(r'@\.taskTimers\[\]' + TR, 'U', '', 'HAR 에서 늘 빈 배열 · S0 OQ-05-1(:1850) 열림'),
    r(r'@\.reservationTagIds\[\]' + TR, 'C', '', '예약 태그 id — DAY 칸 없음', 'visit (태그 — 새 표 필요)'),
    r(r'@\.etceteraWorks\[\]' + TR, 'C', '', '기타 업무 — S0 OQ-05-1(:893 · :1850) 「확인 필요」 열림(결정 없음)', '새 표 필요(기타 업무)'),
    # 단일 상담 정보 — DAY consultation 은 consultations[] 기록
    r(r'@\.consultation', 'F', '', '묶음'),
    r(r'@\.consultation\.consultationMemo', 'C2', '(consultation.consultation_note 는 consultations[].content.text)', '앞 판 M3 · C5 — 공개 쓰기 경로와 같은 칸', 'visit'),
    r(r'@\.consultation\.(counselor|doctor)(\.id)?', 'C2', '(consultation.counselor_id · doctor_id 는 consultations[] 기록 값)', '앞 판 M2 — 일정 단일 상담 정보의 사람', 'visit'),
    r(r'@\.consultation\.(counselor|doctor)\.name', 'C2', '(id 가 없으니 join 불가)', '이름 스냅샷', 'visit'),
    # 상담 기록
    r(r'@\.consultations\[\]', 'A', 'consultation (' + mv + '119)', M + '553'),
    r(r'@\.consultations\[\]\.id', 'A', ER, M + '503'),
    r(r'@\.consultations\[\]\.scheduleId', 'A', 'consultation.visit_id (' + mv + '130)', '부모 일정'),
    r(r'@\.consultations\[\]\.consultationStartedDateTimeUtc', 'A', 'consultation.started_at (' + mv + '131)', M + '504'),
    r(r'@\.consultations\[\]\.counselors\[\](\.id)?', 'A', 'consultation.counselor_id (' + mv + '132)', M + '505 — **1명일 때만**(둘 이상이면 비움 · ' + M + '491-494 · OQ-13)'),
    r(r'@\.consultations\[\]\.consultationDoctors\[\](\.id)?', 'A', 'consultation.doctor_id (' + mv + '133)', M + '506 — **1명일 때만**(' + M + '491-494)'),
    r(r'@\.consultations\[\]\.(counselors|consultationDoctors)\[\]\.name', 'E', 'join staff.name (' + ms + '51)', ''),
    r(r'@\.consultations\[\]\.content', 'F', '', '묶음'),
    r(r'@\.consultations\[\]\.content\.text', 'A', 'consultation.consultation_note (' + mv + '134)', M + '507'),
    r(r'@\.consultations\[\]\.consultationProcedures\[\]' + TR, 'B', 'consultation_procedure (' + mv + '140)', M + '500 「안쪽 키 미관찰이라 받지 않는다」 · HAR 에서 늘 빈 배열', 'consultation_procedure'),
    r(r'@\.consultations\[\]\.createdDateTimeUtc', 'B', 'consultation.created_at (S0:537 「created_at ← createdDateTimeUtc」)', '매퍼 없음 — DAY created_at 은 DAY 행 생성 시각', 'consultation'),
    r(r'@\.consultations\[\]\.updatedDateTimeUtc', 'B', EU, '매퍼 없음(상담 기록은 external_updated_at 안 채움)', 'external_ref'),
    r(r'@\.consultations\[\]\.visitor(\.id)?', 'E', 'visit.customer_id (' + mv + '67)', '같은 일정의 고객'),
    r(r'@\.consultations\[\]\.visitor\.name', 'E', 'join customer.name', ''),
    r(r'@\.consultations\[\]\.visitor\.isNew', 'U', '(visit.is_new 와 같은 값인지 확인 안 됨)', ''),
    # 예약
    r(r'@\.reservation', 'F', '', '묶음'),
    r(r'@\.reservation\.startDateTime', 'A', 'visit.reserved_start_at (' + mv + '70)', M + '560'),
    r(r'@\.reservation\.endDateTime', 'A', 'visit.reserved_end_at (' + mv + '71)', M + '563'),
    r(r'@\.reservation\.status', 'A', 'visit.reservation_status (' + mv + '72)', M + '564-567'),
    r(r'@\.reservation\.statusUpdatedDateTimeUtc', 'C', '', '예약 상태 바뀐 시각 — visit_flow_log 는 flowStep 만', 'visit'),
    r(r'@\.reservation\.reservationMemo', 'A', 'visit.reservation_notes (' + mv + '75)', M + '568'),
    r(r'@\.reservation\.reservationAssignee(\.id)?', 'A', 'visit.reservation_assignee_id (' + mv + '76)', M + '569-571'),
    r(r'@\.reservation\.counselor(\.id)?', 'A', 'visit.requested_counselor_id (' + mv + '77)', M + '572-574 — 예약 지정 희망 상담사(앞 판 M1)'),
    r(r'@\.reservation\.doctor(\.id)?', 'A', 'visit.requested_doctor_id (' + mv + '78)', M + '575-577'),
    r(r'@\.reservation\.(reservationAssignee|counselor|doctor)\.name', 'E', 'join staff.name (' + ms + '51)', ''),
    r(r'@\.reservation\.funnel', 'F', '', '묶음'),
    r(r'@\.reservation\.funnel\.funnel(\.id)?', 'A', 'visit.funnel_id (' + mv + '79)', M + '578'),
    r(r'@\.reservation\.funnel\.funnel\.(name|order|closed|default|category)', 'E', 'join funnel (' + mc + '145-153)', 'funnel 표는 get-codes FUNNEL 로 채움(' + M + '269-280)'),
    r(r'@\.reservation\.funnel\.funnelDetail', 'A', 'visit.funnel_detail (' + mv + '80)', M + '579'),
    r(r'@\.reservation\.connectedChannel', 'A', 'visit.connected_channel (' + mv + '81)', M + '580 — `Channel_UNSPEICIFED` 는 None(' + M + '113-118)'),
    r(r'@\.reservation\.consultationRequired', 'A', 'visit.consultation_required (' + mv + '82)', M + '581'),
    r(r'@\.reservation\.sedationRequired', 'A', 'visit.sedation_required (' + mv + '83)', M + '584'),
    r(r'@\.reservation\.desiredDischargeDateTimeUtc', 'A', 'visit.desired_discharge_at (' + mv + '84)', M + '587'),
    r(r'@\.reservation\.(reservationGroupId|zoneId)', 'C', '(visit_occupied_resource 쪽 칸은 있음 — 같은 값인지 확인 안 됨)', 'S0:598 「visit 에 두지 않고 visit_occupied_resource 로」는 그룹 칸 얘기 — 이 키 자체의 결정은 없음', 'visit'),
    r(r'@\.reservation\.requestedProcedures\[\]', 'A', 'visit_requested_procedure (' + mv + '100) · sort_order = 배열 순서(' + mv + '113)', M + '536-541 — P07 · P08 · P33 HAR 에서 늘 빈 배열 — 안쪽 키는 HAR 에만 있는 `schedule/v1/queries/get-schedule-summaries` 응답에서만 보인다(K5)'),
    r(r'@\.reservation\.requestedProcedures\[\]\.type', 'A', 'visit_requested_procedure.kind (' + mv + '104)', M + '337'),
    r(r'@\.reservation\.requestedProcedures\[\]\.optionConfiguration', 'F', '', '묶음'),
    r(r'@\.reservation\.requestedProcedures\[\]\.optionConfiguration\.productTitle', 'A', 'visit_requested_procedure.product_title (' + mv + '108)', M + '355'),
    r(r'@\.reservation\.requestedProcedures\[\]\.optionConfiguration\.optionTitle', 'A', 'visit_requested_procedure.option_title (' + mv + '109)', M + '356'),
    r(r'@\.reservation\.requestedProcedures\[\]\.optionConfiguration\.optionType', 'A', 'visit_requested_procedure.option_type (' + mv + '110)', M + '357'),
    r(r'@\.reservation\.requestedProcedures\[\]\.optionConfiguration\.price', 'F', '', '묶음'),
    r(r'@\.reservation\.requestedProcedures\[\]\.optionConfiguration\.price\.amount', 'A', 'visit_requested_procedure.price_amount (' + mv + '111)', M + '358'),
    r(r'@\.reservation\.requestedProcedures\[\]\.optionConfiguration\.price\.currency', 'A', 'visit_requested_procedure.currency (' + mv + '112)', M + '359'),
    r(r'@\.reservation\.requestedProcedures\[\]\.optionConfiguration\.price\.reason(\..*)?', 'D', '', 'S0:510 「가격 사유(정상가 · 수가 유형가) … 두지 않는다」'),
    r(r'@\.reservation\.requestedProcedures\[\]\.optionConfiguration\.optionId', 'B', 'visit_requested_procedure.product_option_id (' + mv + '105)', 'S0:551 「1차는 비워 둔다 · 채울지는 OQ-041-7」 · ' + M + '333-336', 'visit_requested_procedure'),
    r(r'@\.reservation\.requestedProcedures\[\]\.optionConfiguration\.(medicalService|compositions\[\])(\..*)?', 'D', '', 'S0:510 「진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다」'),
    r(r'@\.reservation\.requestedProcedures\[\]\.optionConfiguration\.translsMap' + TR, 'C', '', '희망 옵션 · 상품 이름 번역', 'visit_requested_procedure'),
    r(r'@\.reservation\.requestedProcedures\[\]\..*', 'U', '', '이 키는 HAR 에 없음'),
    # 점유
    r(r'@\.occupiedResources\[\]', 'A', 'visit_occupied_resource (' + mr + '96)', M + '542'),
    r(r'@\.occupiedResources\[\]\.id', 'A', ER, M + '368'),
    r(r'@\.occupiedResources\[\]\.type', 'A', 'visit_occupied_resource.type (' + mr + '100)', M + '371'),
    r(r'@\.occupiedResources\[\]\.reservationGroup', 'F', '', '묶음'),
    r(r'@\.occupiedResources\[\]\.reservationGroup\.reservationGroupId', 'A', 'visit_occupied_resource.reservation_group_id (' + mr + '101)', M + '372'),
    r(r'@\.occupiedResources\[\]\.reservationGroup\.zoneId', 'A', 'visit_occupied_resource.zone_id (' + mr + '102)', M + '375'),
    r(r'@\.occupiedResources\[\]\.reservationGroup\.doctors\[\](\.id)?', 'A', 'visit_occupied_resource_doctor (' + mr + '108)', M + '380-384'),
    r(r'@\.occupiedResources\[\]\.reservationGroup\.doctors\[\]\.name', 'E', 'join staff.name', ''),
    r(r'@\.occupiedResources\[\]\.reservationTime', 'F', '', '묶음'),
    r(r'@\.occupiedResources\[\]\.reservationTime\.startDateTimeUtc', 'A', 'visit_occupied_resource.start_at (' + mr + '103)', M + '378'),
    r(r'@\.occupiedResources\[\]\.reservationTime\.endDateTimeUtc', 'A', 'visit_occupied_resource.end_at (' + mr + '104)', M + '379'),
    # 작업
    r(r'@\.tasks\[\]', 'A', 'visit_task (' + mt + '68)', M + '545-552'),
    r(r'@\.tasks\[\]\.sequence', 'A', 'visit_task.sequence (' + mt + '74)', M + '454'),
    r(r'@\.tasks\[\]\.type', 'A', 'visit_task.kind (' + mt + '73)', M + '455'),
    r(r'@\.tasks\[\]\.order', 'A', 'visit_task.sort_order (' + mt + '75)', M + '456'),
    r(r'@\.tasks\[\]\.status', 'A', 'visit_task.status (' + mt + '76)', M + '457-459'),
    r(r'@\.tasks\[\]\.title', 'A', 'visit_task.title (' + mt + '78)', M + '460'),
    r(r'@\.tasks\[\]\.paymentRequired', 'A', 'visit_task.payment_required (' + mt + '101)', M + '471'),
    r(r'@\.tasks\[\]\.anesthesiaType', 'A', 'visit_task.anesthesia_type (' + mt + '102)', M + '472'),
    r(r'@\.tasks\[\]\.memo', 'A', 'visit_task.procedure_note (' + mt + '103)', M + '473'),
    r(r'@\.tasks\[\]\.assigneeMemo', 'A', 'visit_task.assignee_note (' + mt + '104)', M + '474'),
    r(r'@\.tasks\[\]\.doctorMemo', 'A', 'visit_task.doctor_note (' + mt + '105)', M + '475'),
    r(r'@\.tasks\[\]\.room(\.id)?', 'A', 'visit_task.room_id (' + mt + '106)', M + '450-452 · 카드 방 visit.room_id(' + mv + '93) ' + M + '388-408'),
    r(r'@\.tasks\[\]\.room\.(title|order|zoneId)', 'E', 'join room (' + mr + '43-49)', ''),
    r(r'@\.tasks\[\]\.roomAssignedDateTimeUtc', 'A', 'visit_task.room_assigned_at (' + mt + '107)', M + '477'),
    r(r'@\.tasks\[\]\.readyDateTimeUtc', 'A', 'visit_task.ready_at (' + mt + '108)', M + '478'),
    r(r'@\.tasks\[\]\.doctorCallDateTime', 'A', 'visit_task.doctor_called_at (' + mt + '109)', M + '479'),
    r(r'@\.tasks\[\]\.doctorAssignedDateTimeUtc', 'A', 'visit_task.doctor_assigned_at (' + mt + '110)', M + '480'),
    r(r'@\.tasks\[\]\.completedDateTimeUtc', 'A', 'visit_task.completed_at (' + mt + '114)', M + '481'),
    r(r'@\.tasks\[\]\.(assignees|doctors|calledDoctors)\[\](\.id)?', 'A', 'visit_task_staff (' + mt + '140)', M + '482-484'),
    r(r'@\.tasks\[\]\.(assignees|doctors|calledDoctors)\[\]\.name', 'E', 'join staff.name', ''),
    r(r'@\.tasks\[\]\.urgencyLevel', 'C', '', '긴급도', 'visit_task'),
    r(r'@\.tasks\[\]\.translsMap' + TR, 'C', '', '작업 이름 번역', 'visit_task'),
    r(r'@\.tasks\[\]\.etceteraConfiguration', 'F', '', '묶음'),
    r(r'@\.tasks\[\]\.etceteraConfiguration\.name', 'A', 'visit_task.etc_task_title (' + mt + '88)', M + '469'),
    r(r'@\.tasks\[\]\.etceteraConfiguration\.etceteraTaskId', 'C', '(etc_task_type 표는 있으나 작업 → 종류 FK 없음)', M + '485-487 → `is_room_assign`(' + mt + '91) 판정에만 씀(emr/sync_tasks.py:132)', 'visit_task'),
    r(r'@\.tasks\[\]\.etceteraConfiguration\.translsMap' + TR, 'C', '', '', 'visit_task'),
    r(r'@\.tasks\[\]\.procedureConfiguration', 'F', '', '묶음'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.ticketConfiguration', 'F', '', '묶음(시술권이 아니면 빈 객체)'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.ticketConfiguration\.ticketId', 'A', 'visit_task.ticket_id (' + mt + '99)', MP + '85-87'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.ticketConfiguration\.round', 'F', '', '묶음'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.ticketConfiguration\.round\.current', 'A', 'visit_task.ticket_round_current (' + mt + '86)', M + '467'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.ticketConfiguration\.round\.total', 'A', 'visit_task.ticket_round_total (' + mt + '87)', M + '468'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.productOptionConfiguration', 'F', '', '묶음'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.productOptionConfiguration\.optionTitle', 'A', 'visit_task.option_title (' + mt + '79)', M + '461'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.productOptionConfiguration\.unit', 'F', '', '묶음'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.productOptionConfiguration\.unit\.(type|value)', 'A', 'visit_task.unit_type · unit_value (' + mt + '82 · 85)', M + '447-466 — `UnitType_UNKNOWN` 은 None'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.productOptionConfiguration\.optionId', 'D', '', 'S0:892 「상품 옵션 id 는 ERD v1 이 작업에 두지 않음」'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.productOptionConfiguration\.productTitle', 'C2', '(product.title 은 지금 메뉴 값 · 작업 → 옵션 참조 없음)', 'data_rules 「메뉴 참조 = id + 그때 값 스냅샷」', 'visit_task'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.productOptionConfiguration\.procedure(\.(id|name|createDate))?', 'C2', '(treatment 표는 지금 값 · 작업 → 시술 참조 없음)', '메뉴 스냅샷', 'visit_task'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.productOptionConfiguration\.procedure\.categoryIds\[\]', 'D', '', 'S0:1429 「시술 카테고리 칸으로 두지 않는다」'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.productOptionConfiguration\.medicineAndMachines\[\]' + TR, 'U', '', 'HAR 에서 늘 빈 배열'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.productOptionConfiguration\.translsMap' + TR, 'C', '', '옵션 · 상품 이름 번역 스냅샷', 'visit_task'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.medicalServiceConfiguration', 'F', '', '묶음'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.medicalServiceConfiguration\.id', 'A', 'visit_task.treatment_item_id (' + mt + '98)', MP + '88'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.medicalServiceConfiguration\.title', 'A', 'visit_task.medical_service_title (' + mt + '80)', M + '462'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.medicalServiceConfiguration\.(code|caution)', 'C2', '(treatment_item.code · caution = 지금 메뉴 값 ' + mm + '173 · 176)', '메뉴 스냅샷', 'visit_task'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.medicalServiceConfiguration\.unit(\.(type|value))?', 'C2', '(treatment_item.unit_* = 지금 메뉴 값 ' + mm + '179-180)', '작업 단위는 옵션 단위만 저장(' + M + '447)', 'visit_task'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.medicalServiceConfiguration\.medicines\[\](\.name)?', 'A', 'visit_task.medicines (' + mt + '94)', M + '449 · 470 — 이름 스냅샷'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.medicalServiceConfiguration\.machines\[\](\.name)?', 'A', 'visit_task.machines (' + mt + '96)', MP + '89 — 이름 스냅샷'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.medicalServiceConfiguration\.(medicines|machines)\[\]\.id', 'C', '(이름 스냅샷만 — id 없음)', '', 'visit_task'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.medicalServiceConfiguration\.(medicines|machines)\[\]\.searchPhoneticName', 'C2', '(machine · medicine.search_phonetic_name = 지금 값)', '', 'visit_task'),
    r(r'@\.tasks\[\]\.procedureConfiguration\.medicalServiceConfiguration\.translsMap' + TR, 'C', '', '', 'visit_task'),
    # 고객
    r(r'@\.visitor', 'A', 'customer (' + mc + '33)', M + '558'),
] + []

CUST_FROM_SCHED = [
    r(r'@\.visitor\.id', 'A', ER, M + '307'),
    r(r'@\.visitor\.chartNumber', 'A', 'customer.chart_number (' + mc + '43) + external_ref.external_number (' + mc + '107)', M + '308 · emr/sync_schedules.py:150'),
    r(r'@\.visitor\.name', 'A', 'customer.name (' + mc + '46)', M + '309'),
    r(r'@\.visitor\.phoneticName', 'A', 'customer.name_pronunciation (' + mc + '47)', M + '310'),
    r(r'@\.visitor\.gender', 'A', 'customer.gender (' + mc + '51)', M + '311 — `GENDER_UNSPECIFIED` 는 None'),
    r(r'@\.visitor\.dateOfBirth', 'A', 'customer.birth_date (' + mc + '52)', M + '312'),
    r(r'@\.visitor\.nationality', 'A', 'customer.nationality (' + mc + '53)', M + '313'),
    r(r'@\.visitor\.phone', 'F', '', '묶음'),
    r(r'@\.visitor\.phone\.countryCode', 'A', 'customer.phone_country_code (' + mc + '61)', M + '314'),
    r(r'@\.visitor\.phone\.phoneNumber', 'A', 'customer.phone_number (' + mc + '62)', M + '315'),
    r(r'@\.visitor\.memo', 'A', 'customer.customer_notes (' + mc + '72)', M + '316'),
    r(r'@\.visitor\.snsInfo', 'F', '', '묶음'),
    r(r'@\.visitor\.snsInfo\.snsType', 'A', 'customer.sns_type (' + mc + '69)', M + '317'),
    r(r'@\.visitor\.snsInfo\.accountId', 'A', 'customer.sns_account_id (' + mc + '70)', M + '318'),
    r(r'@\.visitor\.visitorType(\.id)?', 'A', 'customer.customer_type_id (' + mc + '73)', M + '319-321'),
    r(r'@\.visitor\.visitorType\.name', 'A', 'customer_type.name (' + mc + '120)', M + '319-321'),
    r(r'@\.visitor\.categories\[\](\.id)?', 'A', 'customer_category_link (' + mc + '157)', M + '322-327'),
    r(r'@\.visitor\.categories\[\]\.(name|color|order)', 'E', 'join customer_category (' + mc + '124-131)', 'get-codes VISITOR_CATEGORY 로 채움'),
    r(r'@\.visitor\.isNew', 'A', 'visit.is_new (' + mv + '91)', M + '597 — 방문마다 값(S0:301 · 360)'),
]
SCHED = SCHED + CUST_FROM_SCHED

# ---------- 고객 전체(get-visitor · find-duplicated · get-visitors 한 행) — DAY 가 이 경로로 채우지 않음 ----------
VIA = ' — 일정 안 visitor 로 받음(오늘 일정 고객만 · K4)'
CUST_FULL = [
    r(r'@\.id', 'A', ER, M + '307' + VIA),
    r(r'@\.chartNumber', 'A', 'customer.chart_number (' + mc + '43)', M + '308' + VIA),
    r(r'@\.name', 'A', 'customer.name (' + mc + '46)', M + '309' + VIA),
    r(r'@\.phoneticName', 'A', 'customer.name_pronunciation (' + mc + '47)', M + '310' + VIA),
    r(r'@\.gender', 'A', 'customer.gender (' + mc + '51)', M + '311' + VIA),
    r(r'@\.dateOfBirth', 'A', 'customer.birth_date (' + mc + '52)', M + '312' + VIA),
    r(r'@\.nationality', 'A', 'customer.nationality (' + mc + '53)', M + '313' + VIA),
    r(r'@\.memo', 'A', 'customer.customer_notes (' + mc + '72)', M + '316' + VIA),
    r(r'@\.phoneNumber', 'F', '', '묶음'),
    r(r'@\.phoneNumber\.countryCode', 'A', 'customer.phone_country_code (' + mc + '61)', M + '314(일정 visitor `phone.countryCode`)' + VIA),
    r(r'@\.phoneNumber\.phoneNumber', 'A', 'customer.phone_number (' + mc + '62)', M + '315(일정 visitor `phone.phoneNumber`)' + VIA),
    r(r'@\.snsInfo', 'F', '', '묶음'),
    r(r'@\.snsInfo\.snsType', 'A', 'customer.sns_type (' + mc + '69)', M + '317' + VIA),
    r(r'@\.snsInfo\.accountId', 'A', 'customer.sns_account_id (' + mc + '70)', M + '318' + VIA),
    r(r'@\.visitorType(\.id)?', 'A', 'customer.customer_type_id (' + mc + '73)', M + '319-321' + VIA),
    r(r'@\.visitorType\.name', 'A', 'customer_type.name (' + mc + '120)', M + '319-321' + VIA),
    r(r'@\.visitorCategories\[\](\.id)?', 'A', 'customer_category_link (' + mc + '157)', M + '322-327(일정 visitor `categories[]`)' + VIA),
    r(r'@\.visitorCategories\[\]\.(name|color|order)', 'E', 'join customer_category (' + mc + '124-131)', ''),
    r(r'@\.createdDateTimeUtc', 'B', 'customer.registered_at (' + mc + '44)', 'S0:330 · 매퍼 없음', 'customer'),
    r(r'@\.updatedDateTimeUtc', 'B', EU, '고객은 external_number 만 씀(emr/sync_schedules.py:150)', 'external_ref'),
    r(r'@\.deleted', 'B', 'customer.deleted_at (S0:331)', '매퍼 없음', 'customer'),
    r(r'@\.email', 'B', 'customer.email (' + mc + '65)', '앞 판 B1 · C1', 'customer'),
    r(r'@\.language', 'B', 'customer.language (' + mc + '54)', '앞 판 B1', 'customer'),
    r(r'@\.passportSurname', 'B', 'customer.passport_surname (' + mc + '48)', '', 'customer'),
    r(r'@\.passportGivenNames', 'B', 'customer.passport_given_names (' + mc + '49)', '', 'customer'),
    r(r'@\.passportNumber', 'B', 'customer.passport_number (' + mc + '58)', '**암호화 대상**(data_rules)', 'customer'),
    r(r'@\.passportExpiryDate', 'B', 'customer.passport_expiry_date (' + mc + '59)', '', 'customer'),
    r(r'@\.registrationNumber', 'B', 'customer.registration_number (' + mc + '56)', '**암호화 대상**(data_rules)', 'customer'),
    r(r'@\.foreignRegistrationNumber', 'B', 'customer.foreign_registration_number (' + mc + '57)', '**암호화 대상**(data_rules)', 'customer'),
    r(r'@\.address', 'F', '', '묶음'),
    r(r'@\.address\.address', 'B', 'customer.address (' + mc + '66)', '', 'customer'),
    r(r'@\.address\.detailedAddress', 'B', 'customer.address_detail (' + mc + '67)', '', 'customer'),
    r(r'@\.address\.zipCode', 'B', 'customer.zip_code (' + mc + '68)', '', 'customer'),
    r(r'@\.doctor(\.id)?', 'B', 'customer.assigned_doctor_id (' + mc + '74)', 'S0:350', 'customer'),
    r(r'@\.counselor(\.id)?', 'B', 'customer.assigned_counselor_id (' + mc + '75)', 'S0:350', 'customer'),
    r(r'@\.(doctor|counselor)\.name', 'E', 'join staff.name', ''),
    r(r'@\.visitorFunnel', 'F', '', '묶음'),
    r(r'@\.visitorFunnel\.funnelId', 'B', 'customer.funnel_id (' + mc + '77)', 'S0:351', 'customer'),
    r(r'@\.visitorFunnel\.funnelDetail', 'B', 'customer.funnel_detail (' + mc + '78)', 'S0:352', 'customer'),
    r(r'@\.visitorFunnel\.funnelCategoryId', 'E', 'join funnel.category_id (' + mc + '149)', ''),
    r(r'@\.recommenderName', 'B', 'customer.referrer_name (' + mc + '81)', 'S0:354', 'customer'),
    r(r'@\.aggrementPersonalInformation', 'B', 'customer.agreed_personal_info (' + mc + '83)', 'S0:355', 'customer'),
    r(r'@\.aggrementAdvertisements', 'B', 'customer.agreed_marketing (' + mc + '84)', 'S0:355', 'customer'),
    r(r'@\.agreementInformationalNotification', 'B', 'customer.agreed_informational (' + mc + '85)', 'S0:355', 'customer'),
    r(r'@\.isNew', 'D', '(visit.is_new — 방문마다)', 'S0:301 · 360 「is_new → 3번 방문」 · 앞 판 M4'),
    r(r'@\.lastVisitedDateTimeUtc', 'E', 'max(visit.*) — S0:360 「방문 기록에서 계산」', 'KOS 정의(예약 · 접수 · 완료) 확인 안 됨 — 앞 판 M9 · 과거 방문은 백필 범위만'),
    r(r'@\.migratedMemo', 'D', '', 'S0:311 반려(`legacy_notes`)'),
    r(r'@\.customAttributes\[\]' + TR, 'D', '', 'S0:312 반려(`custom_attributes` · 명동점 정의 0개)'),
    r(r'@\.lineInformation\[\]' + TR, 'D', '', 'S0:312 · 314-317'),
    r(r'@\.unniInformation\[\]' + TR, 'D', '', 'S0:311 · 317'),
    r(r'@\.visitorCategoryId', 'C', '', 'S0:413 에 키만 있음(결정 없음)', 'customer'),
    r(r'@\.funnel', 'C', '', 'S0:414 「옛 칸」(결정 없음)', 'customer'),
    r(r'@\.detailedFunnel', 'C', '', 'S0:414 「옛 칸」(결정 없음)', 'customer'),
    r(r'@\.unregistered' + TR, 'C', '', '', 'customer'),
]

ROOT_BOX = [r(r'@', 'F', '', '응답 껍데기 · 목록')]

RULES = {}
RULES['schedule/zone/v1/queries/get-zones'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, M + '142'), r(r'@\.title', 'A', 'zone.title (' + mr + '35)', M + '143'),
    r(r'@\.order', 'A', 'zone.sort_order (' + mr + '36)', M + '144'), r(r'@\.isDefault', 'A', 'zone.is_default (' + mr + '37)', M + '145')])
RULES['schedule/zone/room/v1/queries/get-rooms'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, M + '152'), r(r'@\.zoneId', 'A', 'room.zone_id (' + mr + '47)', M + '153'),
    r(r'@\.title', 'A', 'room.title (' + mr + '48)', M + '154'), r(r'@\.order', 'A', 'room.sort_order (' + mr + '49)', M + '155')])
WD = r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday)'
RULES['schedule/group/v1/queries/get-reservation-groups'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, M + '203'), r(r'@\.title', 'A', 'reservation_group.title (' + mr + '59)', M + '204'),
    r(r'@\.order', 'A', 'reservation_group.sort_order (' + mr + '60)', M + '205'),
    r(r'@\.intervalMinutes', 'A', 'reservation_group.interval_minutes (' + mr + '61)', M + '206'),
    r(r'@\.sameDayCloseBufferMinutes', 'A', 'reservation_group.same_day_close_buffer_minutes (' + mr + '62)', M + '207'),
    r(r'@\.intervalCapacities\[\]', 'A', 'reservation_group_capacity (' + mr + '68)', M + '189-201'),
    r(r'@\.intervalCapacities\[\]\.zoneId', 'A', 'reservation_group_capacity.zone_id (' + mr + '73)', M + '194-196'),
    r(r'@\.intervalCapacities\[\]\.intervalCapacity', 'A', 'reservation_group_capacity.capacity (' + mr + '74)', M + '197-199'),
    r(r'@\.intervalCapacities\[\]\.enabled', 'E', '행 있음 = 켜짐', M + '190-191 — 꺼진 구역은 행을 만들지 않는다'),
    r(r'@\.operationTimetable', 'A', 'reservation_group_timetable (' + mr + '80)', M + '165-183'),
    r(r'@\.operationTimetable\.' + WD, 'A', 'reservation_group_timetable.weekday (' + mr + '85)', M + '125-133 · 168'),
    r(r'@\.operationTimetable\.' + WD + r'\.enabled', 'A', 'reservation_group_timetable.is_enabled (' + mr + '86)', M + '174-176'),
    r(r'@\.operationTimetable\.' + WD + r'\.startTime', 'A', 'reservation_group_timetable.start_time (' + mr + '87)', M + '177 — 병원 현지 시계 시간으로 바꿔 저장'),
    r(r'@\.operationTimetable\.' + WD + r'\.endTime', 'A', 'reservation_group_timetable.end_time (' + mr + '88)', M + '178'),
    r(r'@\.operationTimetable\.' + WD + r'\.breaktime', 'F', '', '묶음'),
    r(r'@\.operationTimetable\.' + WD + r'\.breaktime\.startTime', 'A', 'reservation_group_timetable.break_start (' + mr + '89)', M + '179'),
    r(r'@\.operationTimetable\.' + WD + r'\.breaktime\.endTime', 'A', 'reservation_group_timetable.break_end (' + mr + '90)', M + '180'),
    r(r'@\.isDefault', 'C', '', '기본 예약 그룹 — cc ext E4 가 「기본 그룹」을 쓴다', 'reservation_group'),
    r(r'@\.memo', 'C', '', '', 'reservation_group'),
    r(r'@\.startDate', 'C', '', '그룹 시작일', 'reservation_group')])
RULES['role/v2/queries/get-roles'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, M + '224'), r(r'@\.name', 'A', 'job_role.name (' + ms + '68)', M + '225'),
    r(r'@\.roleTags\[\]', 'A', 'job_role.tags (' + ms + '69)', M + '226 · 91-103 — 0 등 모르는 값은 뺀다'),
    r(r'@\.isDefault', 'A', 'job_role.is_default (' + ms + '70)', M + '227'),
    r(r'@\.featureList\[\]' + TR, 'D', '', 'S0:611 「KOS 화면 권한(featureList)은 쓰지 않는다」')])
RULES['account/v2/queries/get-accounts'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, M + '236'), r(r'@\.name', 'A', 'staff.name (' + ms + '51)', M + '239'),
    r(r'@\.realName', 'A', 'staff.real_name (' + ms + '52)', M + '240'), r(r'@\.email', 'A', 'staff.email (' + ms + '53)', M + '241'),
    r(r'@\.licenseNumber', 'A', 'staff.license_number (' + ms + '54)', M + '242'),
    r(r'@\.(roleId|role|role\.id)', 'A', 'staff.job_role_id (' + ms + '55)', M + '245-247'),
    r(r'@\.(roleName|role\.name|role\.roleTags\[\])', 'E', 'join job_role (' + ms + '64-70)', ''),
    r(r'@\.activate', 'A', 'staff.is_active (' + ms + '57)', M + '248'),
    r(r'@\.defaultWorkingZoneId', 'B', 'staff.default_zone_id (' + ms + '56)', 'S0:663 · 매퍼 없음(' + M + '236-251)', 'staff'),
    r(r'@\.updatedDateTimeUtc', 'B', EU, '직원은 안 채움', 'external_ref'),
    r(r'@\.createdAt', 'C', '', 'KOS 계정 생성 시각 — S0 직원 표에 대응 없음', 'staff'),
    r(r'@\.profileImageUrl', 'C', '', '', 'staff'),
    r(r'@\.userId', 'C', '(staff.account_id 는 로그인 때 이음 — S0:647)', 'KOS 사용자 id', 'staff'),
    r(r'@\.mfaMethods\[\]' + TR, 'C', '', '2단계 인증 — 로그인 때만 봄(services/auth.py:523)', 'staff')])
RULES['meta/codes/v1/queries/get-codes'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, M + '260'),
    r(r'@\.name', 'A', 'customer_category · funnel_category · funnel .name (' + mc + '128 · 139 · 150)', M + '261'),
    r(r'@\.order', 'A', '.sort_order (' + mc + '130 · 140 · 151)', M + '262'),
    r(r'@\.closed', 'A', '.is_closed (' + mc + '131 · 141 · 152)', M + '263'),
    r(r'@\.color', 'A', 'customer_category.color (' + mc + '129)', M + '264'),
    r(r'@\.default', 'A', 'funnel.is_default (' + mc + '153)', M + '265'),
    r(r'@\.category', 'E', '어느 코드 표인지(요청 `category` 로 정함)', 'emr/kos/__init__.py:139 — DAY 는 VISITOR_CATEGORY · FUNNEL_CATEGORY · FUNNEL 만 부른다(K4)')])
RULES['schedule/v2/queries/get-schedules-grouped-by-zone'] = ('data[].schedules[]', [
    r(r'data\[\]', 'F', '', '구역 묶음 껍데기(' + M + '286-297)'), r(r'data\[\]\.zoneId', 'F', '', '구역 묶음 키 — 일정 안 `zone` · `visitorLocation` 으로 받음'),
    r(r'@', 'A', 'visit (' + mv + '52)', M + '531')] + SCHED)
RULES['schedule/v1/queries/get-schedule-detail'] = ('data', [r(r'@', 'A', 'visit_task 만 씀', M + '511-528 — DAY 는 이 응답의 `tasks` 만 읽는다(__init__.py:214) · 나머지 키 판정은 같은 칸을 일정 목록 동기화가 채우는지 기준')] + SCHED)
RULES['schedule/v2/queries/get-schedules-for-reservation'] = ('data[]', [r(r'@', 'F', '', 'DAY 는 이 경로를 부르지 않음 — 판정은 같은 칸을 grouped-by-zone 동기화가 채우는지 기준')] + SCHED)

# ---------- 메뉴 ----------
TRS = lambda col, ln: r(r'@\.translsMap' + TR, 'A', col, ln + ' — JSON 통째')
RULES['procedure-menu/categories/queries/get-categories'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, MM + '75'), r(r'@\.deleted', 'A', 'external_ref.is_present_in_source · deleted_at', MM + '73 · emr/kos/sale_reads.py:153-156'),
    r(r'@\.name', 'A', 'product_category.name (' + mm + '52)', MM + '76'), r(r'@\.order', 'A', 'product_category.sort_order (' + mm + '53)', MM + '77'),
    r(r'@\.opened', 'A', 'product_category.is_open (' + mm + '54)', MM + '78'),
    r(r'@\.translsMap', 'F', '', '묶음(`name` 만 저장)'),
    r(r'@\.translsMap\.name' + TR, 'A', 'product_category.name_translations (' + mm + '56)', MM + '79 — JSON 통째'),
    r(r'@\.translsMap\..*', 'C', '', '`name` 밖 번역', 'product_category')])
MSVC = [  # @ = medicalService 객체(상품 응답 안) → treatment_item
    r(r'@', 'A', 'treatment_item (' + mm + '169)', MM + '187-221 · emr/kos/sale_reads.py:85-103'),
    r(r'@\.id', 'A', ER, MM + '193'), r(r'@\.title', 'A', 'treatment_item.title (' + mm + '174)', MM + '195'),
    r(r'@\.description', 'A', 'treatment_item.description (' + mm + '175)', MM + '196'),
    r(r'@\.caution', 'A', 'treatment_item.caution (' + mm + '176)', MM + '197'),
    r(r'@\.status', 'A', 'treatment_item.status (' + mm + '177)', MM + '198'),
    r(r'@\.deleted', 'A', 'treatment_item.deleted_at', 'emr/kos/sale_reads.py:101-112'),
    r(r'@\.draftedDateTimeUtc', 'A', 'treatment_item.drafted_at (' + mm + '189)', MM + '205'),
    r(r'@\.updatedDateTimeUtc', 'A', EU, MM + '206 · emr/sync_menu.py:122'),
    r(r'@\.translsMap' + TR, 'A', 'treatment_item.translations (' + mm + '187)', MM + '204 — JSON 통째'),
    r(r'@\.configuration', 'F', '', '묶음'),
    r(r'@\.configuration\.code', 'A', 'treatment_item.code (' + mm + '173)', MM + '194'),
    r(r'@\.configuration\.healthcareReimbursement', 'A', 'treatment_item.healthcare_reimbursement (' + mm + '181)', MM + '202'),
    r(r'@\.configuration\.taxation', 'A', 'treatment_item.taxation (' + mm + '182)', MM + '203'),
    r(r'@\.configuration\.unit(\.(type|value))?', 'A', 'treatment_item.unit_type · unit_value (' + mm + '179-180)', MM + '191'),
    r(r'@\.configuration\.procedure(\.id)?', 'A', 'treatment_item.treatment_id (' + mm + '178)', MM + '199'),
    r(r'@\.configuration\.procedure\.(name|searchPhoneticName)', 'E', 'join treatment (' + mm + '213-220)', ''),
    r(r'@\.configuration\.procedure\.categoryIds\[\]', 'D', '', 'S0:1429'),
    r(r'@\.configuration\.machines\[\]', 'A', 'treatment_item_machine (' + mm + '193)', MM + '207-213'),
    r(r'@\.configuration\.medicines\[\]', 'A', 'treatment_item_medicine (' + mm + '202)', MM + '214-220'),
    r(r'@\.configuration\.machines\[\]\.id', 'A', ER + ' · machine', MM + '237 · emr/kos/sale_reads.py:115-118'),
    r(r'@\.configuration\.machines\[\]\.name', 'A', 'machine.name (' + mm + '228)', MM + '238'),
    r(r'@\.configuration\.machines\[\]\.searchPhoneticName', 'A', 'machine.search_phonetic_name (' + mm + '230)', MM + '239'),
    r(r'@\.configuration\.medicines\[\]\.id', 'A', ER + ' · medicine', MM + '245'),
    r(r'@\.configuration\.medicines\[\]\.name', 'A', 'medicine.name (' + mm + '238)', MM + '246'),
    r(r'@\.configuration\.medicines\[\]\.searchPhoneticName', 'A', 'medicine.search_phonetic_name (' + mm + '240)', MM + '247'),
]
def sub(rules, prefix):
    return [(p.replace('@', prefix, 1), v, c, n, t) for (p, v, c, n, t) in rules]
PRICE_OPT = [
    r(r'@\.price', 'F', '', '묶음'),
    r(r'@\.price\.amount', 'F', '', '묶음'),
    r(r'@\.price\.amount\.value', 'A', 'product_option.price_amount (' + mm + '111)', MM + '132 · ' + MV + '122-132'),
    r(r'@\.price\.amount\.currency', 'A', 'product_option.currency (' + mm + '115)', MV + '131'),
    r(r'@\.price\.suppliedAmount(\.value)?', 'A', 'product_option.supplied_amount (' + mm + '112)', MV + '127'),
    r(r'@\.price\.vatAmount(\.value)?', 'A', 'product_option.vat_amount (' + mm + '113)', MV + '128'),
    r(r'@\.price\.taxFreeAmount(\.value)?', 'A', 'product_option.tax_free_amount (' + mm + '114)', MV + '129'),
    r(r'@\.price\.taxation', 'A', 'product_option.taxation (' + mm + '116)', MV + '130'),
    r(r'@\.price\.(suppliedAmount|vatAmount|taxFreeAmount)\.currency', 'C', '(통화는 amount 쪽 하나만)', '', 'product_option'),
    r(r'@\.price\.additional\[\]', 'A', 'product_option_price (' + mm + '132)', MM + '83-90 · 115-116'),
    r(r'@\.price\.additional\[\]\..*', 'U', '', 'HAR 에서 늘 빈 배열'),
]
PRICE_COMP = [
    r(r'@\.price', 'F', '', '묶음'), r(r'@\.price\.amount', 'F', '', '묶음'),
    r(r'@\.price\.amount\.value', 'A', 'product_option_composition.price_amount (' + mm + '157)', MM + '105'),
    r(r'@\.price\.suppliedAmount(\.value)?', 'A', 'product_option_composition.supplied_amount (' + mm + '158)', MM + '105'),
    r(r'@\.price\.vatAmount(\.value)?', 'A', 'product_option_composition.vat_amount (' + mm + '159)', MM + '105'),
    r(r'@\.price\.taxFreeAmount(\.value)?', 'A', 'product_option_composition.tax_free_amount (' + mm + '160)', MM + '105'),
    r(r'@\.price\.taxation', 'C', '(매퍼는 읽으나 구성 표에 과세 칸 없음 — ' + MV + '130)', '', 'product_option_composition'),
    r(r'@\.price\.(amount|suppliedAmount|vatAmount|taxFreeAmount)\.currency', 'C', '(구성 표에 통화 칸 없음)', '앞 판 E1', 'product_option_composition'),
    r(r'@\.price\.additional\[\]' + TR, 'U', '', 'HAR 에서 늘 빈 배열 · 구성에 수가 유형별 가격 표 없음'),
]
RULES['procedure-menu/products/queries/get-products'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, MM + '159'), r(r'@\.deleted', 'A', 'external_ref.is_present_in_source · deleted_at', MM + '146 · emr/kos/sale_reads.py:153-156'),
    r(r'@\.title', 'A', 'product.title (' + mm + '64)', MM + '160'), r(r'@\.description', 'A', 'product.description (' + mm + '65)', MM + '161'),
    r(r'@\.caution', 'A', 'product.caution (' + mm + '66)', MM + '162'), r(r'@\.cautions\[\]', 'A', 'product.cautions (' + mm + '78)', MM + '163'),
    r(r'@\.isEvent', 'A', 'product.is_event (' + mm + '67)', MM + '164'), r(r'@\.closed', 'A', 'product.is_closed (' + mm + '68)', MM + '165'),
    r(r'@\.order', 'A', 'product.sort_order (' + mm + '69)', MM + '166'),
    r(r'@\.displayPeriod', 'F', '', '묶음'), r(r'@\.offeringPeriod', 'F', '', '묶음'),
    r(r'@\.displayPeriod\.startDateTimeUtc', 'A', 'product.display_from (' + mm + '70)', MM + '167'),
    r(r'@\.displayPeriod\.endDateTimeUtc', 'A', 'product.display_to (' + mm + '71)', MM + '168'),
    r(r'@\.offeringPeriod\.startDateTimeUtc', 'A', 'product.offering_from (' + mm + '72)', MM + '169'),
    r(r'@\.offeringPeriod\.endDateTimeUtc', 'A', 'product.offering_to (' + mm + '73)', MM + '170'),
    r(r'@\.badges\[\]' + TR, 'A', 'product.badges (' + mm + '74)', MM + '171 — HAR 에서 늘 빈 배열'),
    r(r'@\.targetCountryCodes\[\]', 'A', 'product.target_country_codes (' + mm + '79)', MM + '173'),
    r(r'@\.translsMap' + TR, 'A', 'product.translations (' + mm + '75)', MM + '172 — JSON 통째'),
    r(r'@\.medicineAndMachines\[\](\.name)?', 'A', 'product.medicine_and_machine_names (' + mm + '80)', MM + '174 — 이름만'),
    r(r'@\.medicineAndMachines\[\]\.id', 'C', '(이름만 저장)', '', 'product'),
    r(r'@\.categories\[\](\.id)?', 'A', 'product_category_link (' + mm + '86)', MM + '175-181'),
    r(r'@\.categories\[\]\.(name|translsMap.*)', 'E', 'join product_category (' + mm + '48-56)', ''),
    r(r'@\.options\[\]', 'A', 'product_option (' + mm + '100)', MM + '150-157'),
    r(r'@\.options\[\]\.id', 'A', ER, MM + '121'),
    r(r'@\.options\[\]\.deleted', 'A', '(지운 옵션은 받지 않음 → 사라짐)', MM + '151-152 · emr/kos/sale_reads.py:173-181'),
    r(r'@\.options\[\]\.type', 'A', 'product_option.type (' + mm + '105)', MM + '122-124'),
    r(r'@\.options\[\]\.title', 'A', 'product_option.title (' + mm + '106)', MM + '125'),
    r(r'@\.options\[\]\.description', 'A', 'product_option.description (' + mm + '107)', MM + '126'),
    r(r'@\.options\[\]\.count', 'A', 'product_option.count (' + mm + '108)', MM + '127'),
    r(r'@\.options\[\]\.procedure(\.id)?', 'A', 'product_option.treatment_id (' + mm + '109)', MM + '128'),
    r(r'@\.options\[\]\.procedure\.(name|createDate)', 'E', 'join treatment (' + mm + '213-220)', ''),
    r(r'@\.options\[\]\.procedure\.categoryIds\[\]', 'D', '', 'S0:1429'),
    r(r'@\.options\[\]\.frequentlyUsedOption', 'A', 'product_option.is_frequently_used (' + mm + '117)', MM + '133'),
    r(r'@\.options\[\]\.displayChannels\[\]', 'A', 'product_option.display_channels (' + mm + '119)', MM + '119 · 135 — 표 밖 값은 뺀다'),
    r(r'@\.options\[\]\.badges\[\]' + TR, 'A', 'product_option.badges (' + mm + '122)', MM + '136 — HAR 에서 늘 빈 배열'),
    r(r'@\.options\[\]\.promotionConfigurations\[\]' + TR, 'A', 'product_option.promotions (' + mm + '123)', MM + '137 — HAR 에서 늘 빈 배열'),
    r(r'@\.options\[\]\.translsMap' + TR, 'A', 'product_option.translations (' + mm + '124)', MM + '138 — JSON 통째'),
    r(r'@\.options\[\]\.medicineAndMachines\[\](\.name)?', 'A', 'product_option.medicine_and_machine_names (' + mm + '126)', MM + '139'),
    r(r'@\.options\[\]\.medicineAndMachines\[\]\.id', 'C', '(이름만 저장)', '', 'product_option'),
    r(r'@\.options\[\]\.compositions\[\]', 'A', 'product_option_composition (' + mm + '144) · sort_order = 배열 순서(' + mm + '161)', MM + '118 · 93-96'),
    r(r'@\.options\[\]\.compositions\[\]\.title', 'A', 'product_option_composition.title (' + mm + '153)', MM + '97'),
    r(r'@\.options\[\]\.compositions\[\]\.count', 'A', 'product_option_composition.count (' + mm + '154)', MM + '102'),
    r(r'@\.options\[\]\.compositions\[\]\.unit(\.(type|value))?', 'A', 'product_option_composition.unit_type · unit_value (' + mm + '155-156)', MM + '94'),
    r(r'@\.options\[\]\.compositions\[\]\.procedure(\.id)?', 'A', 'product_option_composition.treatment_id (' + mm + '151)', MM + '101'),
    r(r'@\.options\[\]\.compositions\[\]\.procedure\.(name|createDate)', 'E', 'join treatment', ''),
    r(r'@\.options\[\]\.compositions\[\]\.procedure\.categoryIds\[\]', 'D', '', 'S0:1429'),
    r(r'@\.options\[\]\.compositions\[\]\.medicineAndMachines\[\](\.name)?', 'A', 'product_option_composition.medicine_and_machine_names (' + mm + '163)', MM + '106'),
    r(r'@\.options\[\]\.compositions\[\]\.medicineAndMachines\[\]\.id', 'C', '(이름만 저장)', '', 'product_option_composition'),
    r(r'@\.options\[\]\.compositions\[\]\.medicalService\.id', 'A', 'product_option_composition.treatment_item_id (' + mm + '150) + ' + ER, MM + '98-100 · 193'),
    r(r'@\.options\[\]\.medicalService\.id', 'A', 'product_option.treatment_item_id (' + mm + '110) + ' + ER, MM + '129-131 · 193'),
] + sub(PRICE_OPT, r'@\.options\[\]') + sub(PRICE_COMP, r'@\.options\[\]\.compositions\[\]')
  + sub(MSVC, r'@\.options\[\]\.medicalService') + sub(MSVC, r'@\.options\[\]\.compositions\[\]\.medicalService'))
RULES['procedure-menu/v2/queries/get-procedures'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, MM + '228'), r(r'@\.deleted', 'A', 'deleted_at · external_ref', MM + '226'),
    r(r'@\.name', 'A', 'treatment.name (' + mm + '217)', MM + '229'),
    r(r'@\.searchPhoneticName', 'A', 'treatment.search_phonetic_name (' + mm + '219)', MM + '230'),
    r(r'@\.createDate', 'A', 'treatment.registered_at (' + mm + '220)', MM + '231'),
    r(r'@\.categoryIds\[\]' + TR, 'D', '', 'S0:1429 · OQ-041-3(:1801)')])
RULES['schedule/etcetera-tasks/v1/queries/get-etcetera-tasks'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, MM + '254'), r(r'@\.deleted', 'A', 'deleted_at · external_ref', MM + '252'),
    r(r'@\.title', 'A', 'etc_task_type.title (' + mm + '250)', MM + '255'),
    r(r'@\.translsMap' + TR, 'C', '', '', 'etc_task_type')])
MONEY = lambda key, col, ln, t: [r(r'@\.' + key, 'F', '', '묶음'), r(r'@\.' + key + r'\.value', 'A', col, ln),
                                 r(r'@\.' + key + r'\.currency', 'C', '(통화 칸 없음)', '', t)]
RULES['procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, MM + '262'), r(r'@\.title', 'A', 'prepaid_card_product.title (' + mm + '260)', MM + '264'),
    r(r'@\.expirationDurationInDays', 'A', 'prepaid_card_product.expiration_days (' + mm + '264)', MM + '268'),
    r(r'@\.order', 'A', 'prepaid_card_product.sort_order (' + mm + '265)', MM + '269'),
    r(r'@\.closed', 'A', 'prepaid_card_product.is_closed (' + mm + '266)', MM + '270'),
    r(r'@\.description', 'A', 'prepaid_card_product.description (' + mm + '267)', MM + '271'),
    r(r'@\.translsMap' + TR, 'A', 'prepaid_card_product.translations (' + mm + '269)', MM + '272 — JSON 통째')]
    + MONEY('price', 'prepaid_card_product.price_amount (' + mm + '261)', MM + '265', 'prepaid_card_product')
    + MONEY('balance', 'prepaid_card_product.charge_amount (' + mm + '262)', MM + '266', 'prepaid_card_product')
    + MONEY('point', 'prepaid_card_product.charge_point (' + mm + '263)', MM + '267', 'prepaid_card_product'))
RULES['procedure-menu/etcetera-products/v1/queries/get-etcetera-products'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, MM + '292'), r(r'@\.title', 'A', 'etcetera_product.title (' + mm + '294)', MM + '296'),
    r(r'@\.category', 'A', 'etcetera_product.etcetera_product_category_id (' + mm + '291)', MM + '293-295'),
    r(r'@\.category\.id', 'A', ER + ' · etcetera_product_category', MM + '281'),
    r(r'@\.category\.name', 'A', 'etcetera_product_category.name (' + mm + '279)', MM + '283'),
    r(r'@\.category\.order', 'A', 'etcetera_product_category.sort_order (' + mm + '280)', MM + '284'),
    r(r'@\.category\.closed', 'A', 'etcetera_product_category.is_closed (' + mm + '281)', MM + '285'),
    r(r'@\.category\.category', 'F', '', '분류 종류 상수(KOS 코드 표 이름)'),
    r(r'@\.translsMap' + TR, 'C', '', '', 'etcetera_product')]
    + MONEY('price', 'etcetera_product.price_amount (' + mm + '295)', MM + '297', 'etcetera_product'))

# ---------- 구매 ----------
ITEM = [
    r(r'@', 'A', 'purchase_item (' + mpu + '66)', MP + '212-217'),
    r(r'@\.id', 'A', ER, MP + '127'), r(r'@\.type', 'A', 'purchase_item.item_type (' + mpu + '73)', MP + '113-115 — `ETCETRA_PRODUCT` 오타 그대로 매핑'),
    r(r'@\.optionConfiguration', 'F', '', '묶음'), r(r'@\.prepaidCardConfiguration', 'F', '', '묶음'), r(r'@\.etceteraConfiguration', 'F', '', '묶음'),
    r(r'@\.optionConfiguration\.id', 'A', 'purchase_item.product_option_id (' + mpu + '75)', MP + '130-134'),
    r(r'@\.prepaidCardConfiguration\.id', 'A', 'purchase_item.prepaid_card_product_id (' + mpu + '76)', MP + '135-139'),
    r(r'@\.etceteraConfiguration\.id', 'A', 'purchase_item.etcetera_product_id (' + mpu + '79)', MP + '140-144'),
    r(r'@\.(optionConfiguration|prepaidCardConfiguration|etceteraConfiguration)\.title', 'A', 'purchase_item.title (' + mpu + '81)', MP + '145 — 종류에 맞는 것 하나'),
    r(r'@\.optionConfiguration\.unit(\.(type|value))?', 'A', 'purchase_item.unit_type · unit_value (' + mpu + '82-83)', MP + '125'),
    r(r'@\.optionConfiguration\.count', 'A', 'purchase_item.count (' + mpu + '85)', MP + '148'),
    r(r'@\.priceV2', 'F', '', '묶음'), r(r'@\.adjustPriceV2', 'F', '', '묶음'),
    r(r'@\.priceV2\.amount(\.value)?', 'A', 'purchase_item.price_amount (' + mpu + '87)', MP + '149'),
    r(r'@\.priceV2\.suppliedAmount(\.value)?', 'A', 'purchase_item.supplied_amount (' + mpu + '88)', MP + '150'),
    r(r'@\.priceV2\.taxFreeAmount(\.value)?', 'A', 'purchase_item.tax_free_amount (' + mpu + '89)', MP + '151'),
    r(r'@\.priceV2\.vatAmount(\.value)?', 'A', 'purchase_item.vat_amount (' + mpu + '90)', MP + '152'),
    r(r'@\.priceV2\.taxation', 'A', 'purchase_item.taxation (' + mpu + '91)', MP + '153'),
    r(r'@\.adjustPriceV2\.amount(\.value)?', 'A', 'purchase_item.adjusted_amount (' + mpu + '93)', MP + '155'),
    r(r'@\.adjustPriceV2\.suppliedAmount(\.value)?', 'A', 'purchase_item.adjusted_supplied_amount (' + mpu + '94)', MP + '156'),
    r(r'@\.adjustPriceV2\.taxFreeAmount(\.value)?', 'A', 'purchase_item.adjusted_tax_free_amount (' + mpu + '95)', MP + '157'),
    r(r'@\.adjustPriceV2\.vatAmount(\.value)?', 'A', 'purchase_item.adjusted_vat_amount (' + mpu + '96)', MP + '158'),
    r(r'@\.adjustPriceV2\.taxation', 'A', 'purchase_item.adjusted_taxation (' + mpu + '97)', MP + '159'),
    r(r'@\.(priceV2|adjustPriceV2)\.\w+\.currency', 'C', '(구매 항목 통화 칸 없음)', '', 'purchase_item'),
    r(r'@\.(price|basePrice)(\..*)?', 'E', '= purchase_item.price_amount', 'S0:1565 「priceV2.amount(= price · basePrice)」 · 통화 칸은 없음'),
    r(r'@\.adjustedPrice(\..*)?', 'E', '= purchase_item.adjusted_amount', 'S0:1568 「adjustedPrice.value」 — 코드는 adjustPriceV2 를 읽는다'),
    r(r'@\.prepaidCardConfiguration\.prepaidCardId', 'A', 'prepaid_card.purchase_item_id (' + mpc + '36)', MP + '160'),
    r(r'@\.prepaidCardConfiguration\.expirationDateTimeUtc', 'E', 'prepaid_card.expires_at (' + mpc + '40)', '발급된 카드 쪽 값'),
    r(r'@\.prepaidCardConfiguration\.(price|balance|point)(\..*)?', 'C2', '(prepaid_card_product.* = 지금 상품 값)', '산 시점 상품 스냅샷', 'purchase_item'),
    r(r'@\.prepaidCardConfiguration\.(expirationDurationInDays|description)', 'C2', '(prepaid_card_product.* = 지금 값)', '산 시점 스냅샷', 'purchase_item'),
    r(r'@\.prepaidCardConfiguration\.translsMap' + TR, 'C', '', '', 'purchase_item'),
    r(r'@\.etceteraConfiguration\.price(\..*)?', 'C2', '(etcetera_product.price_amount = 지금 값)', '산 시점 스냅샷(구매 금액은 priceV2)', 'purchase_item'),
    r(r'@\.etceteraConfiguration\.translsMap' + TR, 'C', '', '', 'purchase_item'),
    r(r'@\.optionConfiguration\.productTitle', 'C2', '(product.title = 지금 값)', '산 시점 스냅샷', 'purchase_item'),
    r(r'@\.optionConfiguration\.optionType', 'C2', '(product_option.type = 지금 값)', '산 시점 스냅샷', 'purchase_item'),
    r(r'@\.optionConfiguration\.price(\..*)?', 'C2', '(product_option.price_amount = 지금 정가)', '산 시점 정가 스냅샷', 'purchase_item'),
    r(r'@\.optionConfiguration\.procedure(\..*)?', 'C2', '(treatment = 지금 값 · 항목 → 시술 참조 없음)', '산 시점 스냅샷', 'purchase_item'),
    r(r'@\.optionConfiguration\.medicineAndMachines\[\]' + TR, 'U', '', 'HAR 에서 늘 빈 배열'),
    r(r'@\.optionConfiguration\.translsMap' + TR, 'C', '', '', 'purchase_item'),
    r(r'@\.optionConfiguration\.compositions\[\]\.medicineAndMachines\[\]' + TR, 'U', '', 'HAR 에서 늘 빈 배열'),
    r(r'@\.optionConfiguration\.compositions\[\]\.medicalService\.configuration\.medicines\[\]' + TR, 'U', '', 'HAR 에서 늘 빈 배열'),
    r(r'@\.optionConfiguration\.compositions\[\]\.price\.additional\[\]' + TR, 'U', '', 'HAR 에서 늘 빈 배열'),
    r(r'@\.optionConfiguration\.compositions\[\]\.medicalService\.configuration\.procedure\.categoryIds\[\]', 'D', '', 'S0:1429'),
    r(r'@\.optionConfiguration\.medicalService\.configuration\.procedure\.categoryIds\[\]', 'D', '', 'S0:1429'),
    r(r'@\.optionConfiguration\.medicalService(\..*)?', 'C2', '(treatment_item.* = 지금 메뉴 값 · 구매 항목 → 시술 항목 참조 없음)', '산 시점 시술 항목 스냅샷(SINGLE 옵션)', 'purchase_item'),
    r(r'@\.optionConfiguration\.compositions\[\](\..*)?', 'C2', '(product_option_composition = 지금 메뉴 구성)', '산 시점 구성 스냅샷 — 구매 항목엔 구성 칸 없음', 'purchase_item(구성 스냅샷 — 새 표 필요)'),
    r(r'@\.priceAdjustments\[\]', 'A', 'purchase_price_adjustment.purchase_item_id (' + mpu + '109)', MP + '224-226 — 관계만'),
    r(r'@\.priceAdjustments\[\]\..*', 'U', '', 'HAR 에서 늘 빈 배열 · S0 OQ-08-4(:1820)'),
]
RULES['purchase/v1/queries/get-purchase-summaries'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, MP + '233'), r(r'@\.visitorId', 'A', 'purchase.customer_id (' + mpu + '57)', MP + '234-236'),
    r(r'@\.deleted', 'A', 'purchase.deleted_at', MP + '237 · emr/sync_purchases.py:139'),
    r(r'@\.status', 'A', 'purchase.status (' + mpu + '59)', MP + '238-241'), r(r'@\.process', 'A', 'purchase.process (' + mpu + '60)', MP + '242-245'),
    r(r'@\.lastUpdatedDateTimeUtc', 'A', EU, MP + '246 · emr/sync_purchases.py:4'),
    r(r'@\.createdDateTimeUtc', 'B', 'purchase.created_at (S0:1549)', '매퍼 없음 — DAY created_at 은 DAY 행 생성 시각', 'purchase'),
    r(r'@\.assignees\[\](\.id)?', 'A', 'purchase_assignee.staff_id (' + mpu + '144)', MP + '227-231'),
    r(r'@\.assignees\[\]\.name', 'E', 'join staff.name', ''),
    r(r'@\.assignee(\.id|\.name)?', 'C', '', '대표 담당 — S0 OQ-08-3(:1819) 열림', 'purchase'),
    r(r'@\.priceAdjustments\[\]', 'A', 'purchase_price_adjustment (' + mpu + '103) · 항목 없음', MP + '221-223 — 관계만'),
    r(r'@\.priceAdjustments\[\]\..*', 'U', '', 'HAR 에서 늘 빈 배열 · S0 OQ-08-4'),
    r(r'@\.revokingItems\[\]' + TR, 'U', '', 'HAR 에서 늘 빈 배열 · S0 OQ-08-8(:1815)'),
    r(r'@\.refundingItems\[\]', 'B', 'purchase_item.adjusted_* (' + mpu + '93-97)', 'S0:1568 「진행 중 refundingItems[].adjustedPrice.amount」 · 매퍼 없음', 'purchase_item'),
    r(r'@\.refundingItems\[\]\.targetItemId', 'B', '(대상 purchase_item)', 'S0:1568 · 매퍼 없음', 'purchase_item'),
    r(r'@\.refundingItems\[\]\.adjustedPrice(\.\w+)?(\.value)?', 'B', 'purchase_item.adjusted_* (' + mpu + '93-97)', 'S0:1568 · 매퍼 없음', 'purchase_item'),
    r(r'@\.refundingItems\[\]\.adjustedPrice\.\w+\.currency', 'C', '', '', 'purchase_item'),
    r(r'@\.transactions\[\]', 'A', 'purchase_transaction (' + mpu + '115)', MP + '218-220'),
    r(r'@\.transactions\[\]\.id', 'A', ER, MP + '172'),
    r(r'@\.transactions\[\]\.price(\.value)?', 'A', 'purchase_transaction.amount (' + mpu + '121)', MP + '173-174 — 부호 있는 금액'),
    r(r'@\.transactions\[\]\.status', 'A', 'purchase_transaction.status (' + mpu + '122)', MP + '175-178'),
    r(r'@\.transactions\[\]\.canceledRefId', 'A', 'purchase_transaction.canceled_transaction_id (' + mpu + '125)', MP + '179-181'),
    r(r'@\.transactions\[\]\.paymentType', 'A', 'purchase_transaction.payment_type (' + mpu + '128)', MP + '165-168 — **HAR 의 `CARD` 는 매핑 표(' + MV + '48-52) 밖 → 그 거래 행이 빠진다**(K5)'),
    r(r'@\.transactions\[\]\.(cashConfiguration|cardConfiguration|transferConfiguration|platformConfiguration|easyPayConfiguration|medicalLoanConfiguration)(\..*)?', 'A', 'purchase_transaction.payment_config (' + mpu + '130)', MP + '169 · 183 · ' + MV + '68-76 · 156-160 — `…Id` 키만 빼고 JSON'),
    r(r'@\.transactions\[\]\.prepaidCardConfiguration', 'A', 'purchase_transaction.payment_config (' + mpu + '130)', MP + '169-170'),
    r(r'@\.transactions\[\]\.prepaidCardConfiguration\.prepaidCardId', 'A', 'purchase_transaction.prepaid_card_id (' + mpu + '131)', MP + '184'),
    r(r'@\.transactions\[\]\.prepaidCardConfiguration\.chargingId', 'A', 'prepaid_card_ledger.purchase_transaction_id (' + mpc + '67)', MP + '186-188'),
    r(r'@\.transactions\[\]\.prepaidCardConfiguration\.prepaidCardName', 'A', 'purchase_transaction.payment_config (' + mpu + '130)', MV + '156-160 — JSON 안'),
    r(r'@\.transactions\[\]\.assignee(\.id)?', 'A', 'purchase_transaction.staff_id (' + mpu + '132)', MP + '185'),
    r(r'@\.transactions\[\]\.assignee\.name', 'E', 'join staff.name', ''),
    r(r'@\.transactions\[\]\.createdDateTimeUtc', 'B', 'purchase_transaction.created_at (S0:1601)', '매퍼 없음', 'purchase_transaction'),
    r(r'@\.transactions\[\]\.paymentDateTime(\..*)?', 'C', '', '승인 · 취소 시각 — S0 OQ-08-5(a)(:1821) 열림', 'purchase_transaction'),
    r(r'@\.transactions\[\]\.(suppliedAmount|taxFreeAmount|vatAmount)(\.value)?', 'C', '', '금액 분해 — S0 OQ-08-5(a) 열림', 'purchase_transaction'),
    r(r'@\.transactions\[\]\.(price|suppliedAmount|taxFreeAmount|vatAmount)\.currency', 'C', '(통화 칸 없음)', '', 'purchase_transaction'),
] + sub(ITEM, r'@\.items\[\]') + sub(ITEM, r'@\.pendingItems\[\]'))

# ---------- 시술권 ----------
RULES['ticket/v1/queries/get-ticket-bundles'] = ('data[]', ROOT_BOX + [
    r(r'@\.purchaseItemId', 'A', 'ticket_bundle.purchase_item_id (' + mti + '37) + ' + ER, MP + '295-298'),
    r(r'@\.purchaseId', 'E', 'purchase_item.purchase_id (' + mpu + '72)', '번들 → 구매 항목 → 구매'),
    r(r'@\.visitorId', 'A', 'ticket_bundle.customer_id (' + mti + '36)', 'emr/kos/sale_reads.py:260-275(요청 고객)'),
    r(r'@\.title', 'A', 'ticket_bundle.title (' + mti + '38)', MP + '299'),
    r(r'@\.price', 'F', '', '묶음'),
    r(r'@\.price\.value', 'A', 'ticket_bundle.price_amount (' + mti + '40)', MP + '300'),
    r(r'@\.price\.currency', 'C', '(통화 칸 없음)', '앞 판 E2', 'ticket_bundle'),
    r(r'@\.translsMap' + TR, 'C', '', '', 'ticket_bundle'),
    r(r'@\.optionConfiguration', 'F', '', '묶음'),
    r(r'@\.optionConfiguration\.optionId', 'E', 'purchase_item.product_option_id (' + mpu + '75)', '번들 → 구매 항목'),
    r(r'@\.optionConfiguration\.optionTitle', 'E', '≈ purchase_item.title (' + mpu + '81)', '같은 값인지 확인 안 됨(앞 판 E2 `optionTitle`)'),
    r(r'@\.optionConfiguration\.productTitle', 'C2', '(product.title = 지금 값)', '산 시점 스냅샷', 'ticket_bundle'),
    r(r'@\.optionConfiguration\.promotionConfiguration' + TR, 'C', '', '', 'ticket_bundle'),
    r(r'@\.optionConfiguration\.translsMap' + TR, 'C', '', '', 'ticket_bundle'),
    r(r'@\.ticketSets\[\]', 'A', 'ticket_set (' + mti + '46)', MP + '301'),
    r(r'@\.ticketSets\[\]\.ticketGroupId', 'A', ER + ' · ticket_set', MP + '281'),
    r(r'@\.ticketSets\[\]\.title', 'A', 'ticket_set.title (' + mti + '51)', MP + '285'),
    r(r'@\.ticketSets\[\]\.unit(\.(type|value))?', 'A', 'ticket_set.unit_type · unit_value (' + mti + '52 · 55)', MP + '279'),
    r(r'@\.ticketSets\[\]\.medicalService(\.id)?', 'A', 'ticket_set.treatment_item_id (' + mti + '50)', MP + '282-284'),
    r(r'@\.ticketSets\[\]\.medicalService\.configuration\.procedure\.categoryIds\[\]', 'D', '', 'S0:1429'),
    r(r'@\.ticketSets\[\]\.medicalService\..*', 'C2', '(treatment_item.* = 지금 메뉴 값)', '산 시점 시술 항목 스냅샷', 'ticket_set'),
    r(r'@\.ticketSets\[\]\.procedure(\..*)?', 'C2', '(treatment = 지금 값 · 세트 → 시술 참조 없음)', '산 시점 스냅샷', 'ticket_set'),
    r(r'@\.ticketSets\[\]\.translsMap' + TR, 'C', '', '', 'ticket_set'),
    r(r'@\.ticketSets\[\]\.tickets\[\]', 'A', 'ticket (' + mti + '61)', MP + '271-278'),
    r(r'@\.ticketSets\[\]\.tickets\[\]\.id', 'A', ER, MP + '260'),
    r(r'@\.ticketSets\[\]\.tickets\[\]\.status', 'A', 'ticket.status (' + mti + '65)', MP + '261-264'),
    r(r'@\.ticketSets\[\]\.tickets\[\]\.createdDateTimeUtc', 'B', 'ticket.created_at (S0:1665)', '매퍼 없음 · 앞 판 E2 `purchasedDate` · M10', 'ticket'),
    r(r'@\.ticketSets\[\]\.tickets\[\]\.price(\..*)?', 'D', '', 'S0:1626 · 1668 「KOS 티켓 price 는 받지 않는다(번들 ÷ 회차)」 · customer-erd-spec-brief.md:37'),
])

# ---------- 선불카드 ----------
RULES['purchase/prepaid-card/v1/queries/get-prepaid-card-summaries'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', ER, MP + '310'), r(r'@\.ownerId', 'A', 'prepaid_card.customer_id (' + mpc + '35)', MP + '311-313'),
    r(r'@\.title', 'A', 'prepaid_card.title (' + mpc + '37)', MP + '314'),
    r(r'@\.remainingBalance', 'F', '', '묶음'), r(r'@\.remainingPoint', 'F', '', '묶음'),
    r(r'@\.remainingBalance\.balance(\.value)?', 'A', 'prepaid_card.balance_amount (' + mpc + '38)', MP + '315-317'),
    r(r'@\.remainingPoint\.balance(\.value)?', 'A', 'prepaid_card.point_balance (' + mpc + '39)', MP + '318-320'),
    r(r'@\.remaining(Balance|Point)\.balance\.currency', 'C', '(통화 칸 없음)', '', 'prepaid_card'),
    r(r'@\.remaining(Balance|Point)\.total(\..*)?', 'D', '', 'S0:1698 「total 은 받지 않는다(이력에서 계산)」 · customer-erd-spec-brief.md:37'),
    r(r'@\.expirationDateTimeUtc', 'A', 'prepaid_card.expires_at (' + mpc + '40)', MP + '321'),
    r(r'@\.updatedDateTimeUtc', 'A', EU, MP + '322 · emr/sync_tickets.py:206'),
    r(r'@\.createdDateTimeUtc', 'B', 'prepaid_card.created_at (S0:1695)', '매퍼 없음 · 앞 판 E2 `issuedDate`', 'prepaid_card'),
    r(r'@\.description', 'C', '', '', 'prepaid_card'),
    r(r'@\.translsMap' + TR, 'C', '', '', 'prepaid_card')])
RULES['purchase/prepaid-card/v1/queries/get-prepaid-card-charging-events'] = ('data[]', ROOT_BOX + [
    r(r'@\.chargingId', 'A', ER + ' (`chargingId:주머니`)', MP + '326-343'),
    r(r'@\.type', 'A', 'prepaid_card_ledger.kind (' + mpc + '62)', MP + '345-348'),
    r(r'@\.amount', 'F', '', '묶음'), r(r'@\.amount\.amount', 'F', '', '묶음'),
    r(r'@\.amount\.type', 'A', 'prepaid_card_ledger.pocket (' + mpc + '63)', MP + '336-341'),
    r(r'@\.amount\.amount\.value', 'A', 'prepaid_card_ledger.amount (' + mpc + '64)', MP + '350'),
    r(r'@\.amount\.amount\.currency', 'C', '(통화 칸 없음)', '', 'prepaid_card_ledger'),
    r(r'@\.visitor', 'F', '', '묶음'),
    r(r'@\.visitor\.visitorId', 'A', 'prepaid_card_ledger.customer_id (' + mpc + '66)', MP + '351-353'),
    r(r'@\.visitor\.(name|chartNumber)', 'E', 'join customer', ''),
    r(r'@\.visitor\.owner', 'E', 'prepaid_card.customer_id 와 견줌', ''),
    r(r'@\.memo', 'A', 'prepaid_card_ledger.memo (' + mpc + '71)', MP + '354'),
    r(r'@\.createdDateTimeUtc', 'A', 'prepaid_card_ledger.occurred_at (' + mpc + '72)', MP + '355')])
RULES['purchase/prepaid-card/v1/queries/get-prepaid-card-visitors'] = ('data[]', ROOT_BOX + [
    r(r'@\.visitorId', 'A', 'prepaid_card_customer.customer_id (' + mpc + '52)', MP + '359-364 · emr/kos/sale_reads.py:299-307(소유자 아닌 고객만)'),
    r(r'@\.owner', 'A', '(소유자 = prepaid_card.customer_id · 아니면 prepaid_card_customer)', MP + '363'),
    r(r'@\.(name|chartNumber)', 'E', 'join customer', '')])

# ---------- 고객 ----------
RULES['visitor/v2/queries/get-visitors'] = ('data[]', [r(r'count', 'F', '', '전체 수 — 백필 페이지(emr/kos/sale_reads.py:327)'),
    r(r'@', 'F', '', '목록 — DAY 는 이 경로에서 **id 만** 읽는다(emr/kos/sale_reads.py:316-333)')] + CUST_FULL)
RULES['visitor/v2/queries/get-visitor'] = ('data', [r(r'@', 'F', '', 'DAY 는 이 경로를 부르지 않음')] + CUST_FULL)
RULES['visitor/v1/queries/find-duplicated-visitor'] = ('data', [r(r'@', 'F', '', 'DAY 는 이 경로를 부르지 않음 · 응답 모양이 get-visitor 와 같다')] + CUST_FULL)

# ---------- 로그인 ----------
RULES['v1/account/queries/get-user-account'] = ('data', [r(r'@', 'F', '', '묶음'),
    r(r'@\.id', 'A', ER + ' · staff', M + '658 · services/auth_membership.py:65'),
    r(r'@\.name', 'A', 'staff.name (' + ms + '51)', M + '659 · services/auth_membership.py:74 · 83'),
    r(r'@\.email', 'A', 'staff.email (' + ms + '53)', M + '660 · services/auth_membership.py:75 · 84-85'),
    r(r'@\.role(\.id)?', 'A', 'staff.job_role_id (' + ms + '55) + ' + ER + ' · job_role', M + '646-652 · services/auth_membership.py:26'),
    r(r'@\.role\.name', 'A', 'job_role.name (' + ms + '68)', 'services/auth_membership.py:30'),
    r(r'@\.role\.roleTags\[\]', 'A', 'job_role.tags (' + ms + '69)', 'services/auth_membership.py:31'),
    r(r'@\.role\.isDefault', 'A', 'job_role.is_default (' + ms + '70)', 'services/auth_membership.py:42-43'),
    r(r'@\.role\.featureList\[\]' + TR, 'D', '', 'S0:611'),
    r(r'@\.mfaMethods\[\]' + TR, 'C', '', '로그인 막는 판정에만(services/auth.py:523)', 'staff')])
RULES['common/v1/tenant/queries/get-user-tenants'] = ('data[]', ROOT_BOX + [
    r(r'@\.id', 'A', 'crm_connection 테넌트 매칭 · external_session.external_tenant_id (' + ms + '110)', M + '631 · services/auth.py:273-276'),
    r(r'@\.hospitalName', 'C2', '(hospital.name = DAY 가 정한 이름 ' + 'models/hospital.py:46)', M + '632 — 병원 고르기 표시에만 · 앞 판 E12 `name`', 'hospital'),
    r(r'@\.(hospitalCode|hospitalId|hospitalNationality|mode|namespace)', 'C', '', 'KOS 테넌트 정보', 'hospital')])

# ---------- 새로 필요한 것 ----------
RULES['v1/hospital/queries/get-hospital'] = ('data', [r(r'@', 'F', '', 'DAY 는 이 경로를 부르지 않음'),
    r(r'@\.hospitalName', 'C2', '(hospital.name = DAY 가 정한 이름 models/hospital.py:46)', '앞 판 E12', 'hospital'),
    r(r'@\.hospitalPhoneNumber', 'D', '', 'S0:278 「hospital 의 phone · address 는 두지 않는다」 — 앞 판 E12 · C14 와 충돌(K6)'),
    r(r'@\.addressContract' + TR, 'D', '', 'S0:278'),
    r(r'@\.languages\[\]' + TR, 'U', '', 'HAR 에서 늘 빈 배열'),
    r(r'@\..*', 'C', '', 'KOS 병원 설정', 'hospital')])
RULES['schedule/default-operation-time/v1/queries/get-default-operation-timetable'] = ('data', [r(r'@', 'F', '', 'DAY 는 이 경로를 부르지 않음'),
    r(r'@\..*', 'C', '(reservation_group_timetable 은 **그룹별** — 병원 기본 시간표 아님)', '앞 판 E12 `operatingHours`', '새 표 필요(병원 기본 운영 시간)')])
RULES['schedule/default-operation-time/v1/queries/get-default-days-off'] = ('data[]', [
    r(r'@', 'U', '', 'HAR 22개 응답 모두 빈 배열 — 안쪽 키 확인 안 됨 · cc 는 `startDateTime` · `endDateTime` 을 읽었다(앞 판 E12)')])
```

</details>

<details><summary><code>gen.py</code></summary>

```python
# 일회용: 리포트 본문(K1 · K2 · K3 집계 · 부록 B)을 만든다. 값은 다루지 않는다.
import runpy, collections, re, sys
BASE = '/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-day-cc-mig/e39d60ae-ec21-487b-ab3f-1fd72bdeef25/scratchpad/kos/'
C = runpy.run_path(BASE + 'classify.py')
D, RULES, classify = C['D'], C['RULES'], C['classify']
V = runpy.run_path(BASE + 'rules.py')['V']
ORDER = 'A B C C2 D E F U'.split()

P = [  # (번호, 경로, 갈래, 공개/내부, DAY 부름, 주기)
 ('P01', 'schedule/zone/v1/queries/get-zones', 1, '내부', 'emr/kos/__init__.py:114 · 168', '기준 정보 3600초 · 서버 시작 1회(tasks/emr.py:5-6 · 121-126)'),
 ('P02', 'schedule/zone/room/v1/queries/get-rooms', 1, '내부', 'emr/kos/__init__.py:120', '기준 정보 3600초'),
 ('P03', 'schedule/group/v1/queries/get-reservation-groups', 1, '내부', 'emr/kos/__init__.py:122-124', '기준 정보 3600초'),
 ('P04', 'role/v2/queries/get-roles', 1, '내부', 'emr/kos/__init__.py:130', '기준 정보 3600초'),
 ('P05', 'account/v2/queries/get-accounts', 1, '내부', 'emr/kos/__init__.py:133-135', '기준 정보 3600초'),
 ('P06', 'meta/codes/v1/queries/get-codes', 1, '내부', 'emr/kos/__init__.py:139', '기준 정보 3600초(VISITOR_CATEGORY · FUNNEL_CATEGORY · FUNNEL)'),
 ('P07', 'schedule/v2/queries/get-schedules-grouped-by-zone', 1, '내부', 'emr/kos/__init__.py:171-175', '10초 · 병원 현지 오늘 창만(services/emr_sync.py:111-115) · 백필(어제까지 · 수동)'),
 ('P08', 'schedule/v1/queries/get-schedule-detail', 1, '내부', 'emr/kos/__init__.py:214', '이벤트 — 작업 다시 읽기(services/emr_sync.py:324 · 364)'),
 ('P09', 'procedure-menu/categories/queries/get-categories', 1, '내부', 'emr/kos/sale_reads.py:163-165', '메뉴 — 기준 정보 회차 뒤(tasks/emr.py:89-95)'),
 ('P10', 'procedure-menu/products/queries/get-products', 1, '내부', 'emr/kos/sale_reads.py:168-170', '메뉴'),
 ('P11', 'procedure-menu/v2/queries/get-procedures', 1, '내부', 'emr/kos/sale_reads.py:192', '메뉴'),
 ('P12', 'schedule/etcetera-tasks/v1/queries/get-etcetera-tasks', 1, '내부', 'emr/kos/sale_reads.py:199', '메뉴'),
 ('P13', 'procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product', 1, '내부', 'emr/kos/sale_reads.py:207-209', '메뉴(closed false · true 두 번)'),
 ('P14', 'procedure-menu/etcetera-products/v1/queries/get-etcetera-products', 1, '내부', 'emr/kos/sale_reads.py:213', '메뉴'),
 ('P15', 'purchase/v1/queries/get-purchase-summaries', 1, '내부', 'emr/kos/sale_reads.py:250-252', '일정 회차 뒤 별도 태스크 — 오늘 일정의 purchaseIds(tasks/emr.py:74-85 · 98-105) · 백필'),
 ('P16', 'ticket/v1/queries/get-ticket-bundles', 1, '내부', 'emr/kos/sale_reads.py:263-269', '오늘 일정 고객(services/emr_sale_sync.py:257) · 백필(services/emr_backfill.py:369)'),
 ('P17', 'purchase/prepaid-card/v1/queries/get-prepaid-card-summaries', 1, '내부', 'emr/kos/sale_reads.py:282-284', '오늘 일정 고객(services/emr_sale_sync.py:258) · 백필(:420)'),
 ('P18', 'purchase/prepaid-card/v1/queries/get-prepaid-card-charging-events', 1, '내부', 'emr/kos/sale_reads.py:296', '바뀐 카드(services/emr_sale_sync.py:268) · 백필(:430)'),
 ('P19', 'purchase/prepaid-card/v1/queries/get-prepaid-card-visitors', 1, '내부', 'emr/kos/sale_reads.py:297', '바뀐 카드(위와 같음)'),
 ('P20', 'visitor/v2/queries/get-visitors', 1, '내부', 'emr/kos/sale_reads.py:323', '백필만(수동 · services/emr_backfill.py:396) — id · count 만 읽음'),
 ('P21', 'v1/account/queries/get-user-account', 1, '내부(테넌트 경로)', 'emr/kos/client.py:422 · emr/kos/staff_client.py:154', '로그인 때(services/auth.py)'),
 ('P22', 'common/v1/tenant/queries/get-user-tenants', 1, '내부(테넌트 밖)', 'emr/kos/staff_client.py:136', '로그인 때(services/auth.py:273)'),
 ('P23', 'common/user/v1/queries/get-active-sign-ins', 1, '내부(테넌트 밖)', 'emr/kos/client.py:190', '로그인 기기 제한 때(services/auth.py:410)'),
 ('P24', 'visitor/v2/queries/get-visitor', 2, '내부', '부르지 않음', 'cc: 요청마다(앞 판 E2 · E8)'),
 ('P25', 'v1/hospital/queries/get-hospital', 2, '내부', '부르지 않음', 'cc: 요청마다(앞 판 E12)'),
 ('P26', 'schedule/default-operation-time/v1/queries/get-default-operation-timetable', 2, '내부', '부르지 않음', 'cc: 요청마다(앞 판 E12)'),
 ('P27', 'schedule/default-operation-time/v1/queries/get-default-days-off', 2, '내부', '부르지 않음', 'cc: 요청마다 · 오늘~+90일(앞 판 E12)'),
 ('P28', 'schedule/open/v2/queries/get-reservation-slots-by-groups', 2, '공개', '부르지 않음', 'cc: 요청마다(앞 판 E4)'),
 ('P29', 'schedule/open/v1/queries/get-schedules-by-visitor', 2, '공개', '부르지 않음', 'cc: 요청마다(앞 판 E5 · E6 · E8)'),
 ('P30', 'visitor/open/v1/queries/get-visitor-questionnaire', 2, '공개', '부르지 않음', 'cc: 상세 요청마다(앞 판 E8 health)'),
 ('P31', 'visitor/open/v1/queries/get-questionnaire-submit', 2, '공개', '부르지 않음', 'cc: 상세 요청마다(앞 판 E8 health)'),
 ('P32', 'schedule/v1/queries/get-schedule-event-logs', 2, '내부', '부르지 않음', 'cc: 접수 목록 요청 때(앞 판 E7 firstConsultationWaitingAt)'),
 ('P33', 'schedule/v2/queries/get-schedules-for-reservation', 2, '내부', '부르지 않음(DAY 는 P07 로 대체)', 'cc: 그날 · 10초 캐시(앞 판 「cc reservation 사본」)'),
 ('P34', 'visitor/v1/queries/find-duplicated-visitor', 2, '내부', '부르지 않음', 'cc: 예약 쓰기 때(앞 판 B2 E3)'),
]
NAME = {p: n for n, p, *_ in P}
esc = lambda s: s.replace('|', '\\|')

def shape_txt(shapes):
    en = sorted(x[5:] for x in shapes if x.startswith('ENUM:'))
    o = sorted(x for x in shapes if not x.startswith('ENUM:'))
    if en: o.append('enum: ' + '\\|'.join(en))
    return ' / '.join(o)

def files_of(path):
    E = D['entries'].get(path, [])
    by = collections.OrderedDict()
    for rel, i, st, ok in E:
        by.setdefault(rel, []).append((i, st, ok))
    return by

out = []
w = out.append
# ---- K1 ----
w('## K1. 경로 목록\n')
w('| # | 경로 | 갈래 | 공개/내부 | DAY 가 부르나(`backend/day/` 파일:줄) | 주기(앞 판 §B3) | HAR 엔트리(전체 · 200+JSON) | HAR 파일 | 스크립트 키 수 | K2 행 수 |')
w('|---|---|---|---|---|---|---|---|---|---|')
stats = {}
for n, p, g, pub, call, cyc in P:
    by = files_of(p)
    tot = sum(len(v) for v in by.values()); ok = sum(1 for v in by.values() for x in v if x[1] == 200 and x[2] == 'ok')
    keys = len(D['keys'].get(p, {}))
    rows = classify(p) if p in D['keys'] else []
    stats[p] = rows
    fl = ' · '.join(f'{f.split("/")[0][:10]}/…/{f.split("/")[-1]}({len(v)})' for f, v in by.items()) or '**없음**'
    w(f'| {n} | `{p}` | {["", "DAY 부름", "새로 필요"][g]} | {pub} | {call} | {cyc} | {tot} · {ok} | {fl} | {keys} | {len(rows)} |')
w('')
# ---- K2 ----
w('## K2. 키 전수 대조\n')
w('읽는 법: 판정 = `저장됨` · `칸 있음 · 미동기화` · `칸 없음` · `칸 없음(시점 다름)` · `일부러 안 둠` · `계산으로 대체` · `해당 없음` · `확인 안 됨`. '
  '근거의 코드 줄은 CENTURION_DAY `origin/dev` `844eace4` 의 `backend/day/` 아래(`models/…` · `emr/…` · `services/…`), `S0:줄` = mediness `origin/main` `ccede286` `products/day/20-spec/spec-000-data-model.md`. '
  '「묶음」= 객체 · 배열 칸 자체(안쪽 키가 따로 행). 「JSON 통째」= 그 하위 키가 한 jsonb 칸에 그대로 들어간다. 타입 · 모양만 적고 값은 적지 않았다(enum 은 KOS 코드값만).\n')
for n, p, g, pub, call, cyc in P:
    w(f'### {n} `{p}`\n')
    if p not in D['keys']:
        w('HAR 에 응답 없음 → 키 대조 불가 · **K5** 「확인 안 됨」.\n'); continue
    rows = stats[p]
    w(f'스크립트 합집합 키 **{len(D["keys"][p])}** · 표 행 **{len(rows)}** · 빠진 키 **{len(D["keys"][p]) - len(rows)}**\n')
    w('| # | 키 경로 | 타입 · 모양 | DAY 칸 · 근거 | 판정 | 비고 |')
    w('|---|---|---|---|---|---|')
    for i, (k, s, h) in enumerate(rows, 1):
        v, col, note, tbl, pat = h
        w(f'| {i} | `{esc(k)}` | {shape_txt(s)} | {esc(col)} | {V[v]} | {esc(note)} |')
    w('')
# ---- K3 집계 ----
w('## K3. 집계\n')
w('### K3-1. 경로별 · 판정별 수\n')
w('| # | 경로 | 키 | ' + ' | '.join(V[x] for x in ORDER) + ' |')
w('|---|---|---|' + '---|' * len(ORDER))
tot = collections.Counter(); totk = 0
for n, p, *_ in P:
    if p not in D['keys']: w(f'| {n} | `{p}` | (HAR 없음) |' + ' |' * len(ORDER)); continue
    c = collections.Counter(h[0] for k, s, h in stats[p]); tot.update(c); totk += len(stats[p])
    w(f'| {n} | `{p}` | {len(stats[p])} | ' + ' | '.join(str(c.get(x, 0)) for x in ORDER) + ' |')
w(f'| | **합** | **{totk}** | ' + ' | '.join(f'**{tot.get(x, 0)}**' for x in ORDER) + ' |')
w('')
# DB 확장 후보
ENC = re.compile(r'(registrationNumber|foreignRegistrationNumber|passportNumber)$')
PII = re.compile(r'(name|Name|email|phone|Phone|phoneNumber|address|Address|zipCode|dateOfBirth|memo|Memo|passport\w*|recommenderName|accountId)$')
cand = collections.defaultdict(lambda: collections.defaultdict(set))
for n, p, *_ in P:
    for k, s, h in stats.get(p, []):
        if h[0] in ('B', 'C', 'C2'):
            root = RULES[p][0]
            rk = '@' + k[len(root):] if k.startswith(root + '.') or k == root else k
            cand[h[3] or '(표 미지정)'][(rk, h[0])].add(n)
w('### K3-2. DB 확장 후보(`칸 있음 · 미동기화` · `칸 없음` · `칸 없음(시점 다름)`) — DAY 테이블별\n')
w('키는 경로 뿌리(`@` = 그 경로의 행 · 일정이면 일정 1건)를 기준으로 겹친 것을 하나로 셌다(같은 키가 P07 · P08 · P33 에 함께 나오는 등). 「행」= K2 표의 행 수 합, 「고유」= 겹침을 뺀 수. 설계가 아니라 후보 목록이다.\n')
w('| 대상 테이블 | 있는 표 / 새 표 | 행 | 고유 | 미동기화 | 칸 없음 | 시점 다름 | 민감 정보 | KOS 경로 |')
w('|---|---|---|---|---|---|---|---|---|')
TBLS = set('customer external_ref visit visit_task consultation consultation_procedure reservation_group staff hospital product_category product product_option product_option_composition etc_task_type prepaid_card_product etcetera_product purchase purchase_item purchase_transaction ticket_bundle ticket_set ticket prepaid_card prepaid_card_ledger'.split())
summary_rows = []
for t in sorted(cand, key=lambda t: -sum(len(v) for v in cand[t].values())):
    items = cand[t]
    rows_n = sum(len(v) for v in items.values()); uniq = len(items)
    cb = collections.Counter(v for (rk, v) in items)
    paths = sorted({x for v in items.values() for x in v})
    enc = sorted({rk.split('.')[-1] for (rk, v) in items if ENC.search(rk)})
    PCTX = re.compile(r'(visitor|counselor|doctor\b|doctor\.|assignee|Assignee|Doctors|counselors|representative)')
    pii = sorted({rk.split('.')[-1] for (rk, v) in items if PII.search(rk) and not ENC.search(rk)
                  and (t == 'customer' or PCTX.search(rk) or re.search(r'(memo|Memo)$', rk) or rk.endswith('representativeName'))})
    sens = ('**암호화 대상**: ' + ', '.join(f'`{x}`' for x in enc) + ' · ' if enc else '') + (('개인정보(암호화 대상 아님): ' + ', '.join(f'`{x}`' for x in pii[:8]) + (' …' if len(pii) > 8 else '')) if pii else ('—' if not enc else ''))
    kind = '있는 표' if t in TBLS else '새 표 필요'
    summary_rows.append((t, kind, rows_n, uniq))
    w(f'| `{t}` | {kind} | {rows_n} | {uniq} | {cb.get("B", 0)} | {cb.get("C", 0)} | {cb.get("C2", 0)} | {sens} | {" · ".join(paths)} |')
w('')
w('<details><summary>테이블별 키 목록(고유 · 번역 언어 잎은 묶어 셈)</summary>\n')
for t in sorted(cand, key=lambda t: -sum(len(v) for v in cand[t].values())):
    w(f'\n**`{t}`**\n')
    grouped = collections.OrderedDict()
    for (rk, v), ps in sorted(cand[t].items()):
        g = re.sub(r'\.translation\..*$', '.translation.<언어>', rk)
        e = grouped.setdefault((g, v), set()); e |= ps
        grouped[(g, v)] = e
    cnt = collections.Counter(re.sub(r'\.translation\..*$', '.translation.<언어>', rk) + '|' + v for (rk, v) in cand[t])
    for (g, v), ps in grouped.items():
        m = cnt[g + '|' + v]
        w(f'- `{g}`{f" ×{m}" if m > 1 else ""} — {V[v]} — {" · ".join(sorted(ps))}')
w('\n</details>\n')
# U 목록
w('### K3-3. `확인 안 됨` 키(K5 로 이어짐)\n')
for n, p, *_ in P:
    us = [k for k, s, h in stats.get(p, []) if h[0] == 'U']
    if us: w(f'- {n}: ' + ' · '.join(f'`{u}`' for u in us))
w('')
# 부록 B
B = ['## 부록 B. HAR 엔트리 위치(파일#엔트리 번호 · 0부터 · HTTP 상태)\n']
B.append('엔트리 번호는 HAR `log.entries[]` 의 순번이다. `200*` = 200 이지만 응답 본문이 JSON 이 아니거나 비어 키를 못 읽음.\n')
for n, p, *_ in P:
    by = files_of(p)
    if not by: B.append(f'- {n} `{p}` — 없음'); continue
    parts = []
    for f, v in by.items():
        parts.append(f'`{f}`#' + ','.join(f'{i}' + ('' if st == 200 and ok == 'ok' else f'({st}{"*" if st == 200 else ""})') for i, st, ok in v))
    B.append(f'- {n} `{p}` — ' + ' ; '.join(parts))
open(BASE + 'body.md', 'w').write('\n'.join(out))
open(BASE + 'appB.md', 'w').write('\n'.join(B) + '\n')
c = collections.Counter(); [c.update(h[0] for k, s, h in stats[p]) for p in stats]
print('keys', totk, dict(tot))
print('cand tables', [(t, k, r_, u) for t, k, r_, u in summary_rows])
print('cand rows', sum(r_ for _, _, r_, _ in summary_rows), 'uniq', sum(u for *_, u in summary_rows))
print('U', tot.get('U'))
```

</details>

<details><summary><code>k13.py</code></summary>

```python
import runpy
C = runpy.run_path('/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-day-cc-mig/e39d60ae-ec21-487b-ab3f-1fd72bdeef25/scratchpad/kos/classify.py')
DESC = {
 'account/v2/queries/get-accounts-last-update-date-time-utc': '직원 목록 마지막 수정 시각(바뀐 것만 받기용으로 보임)',
 'account/v2/queries/get-accounts-status': '직원 계정 상태',
 'common/feature-flags/v1/queries/get-feature-flags': 'KOS 기능 플래그',
 'common/kcd-codes/v1/queries/get-kcd-codes': 'KCD(질병 분류) 코드 — 처방 화면',
 'common/medicine-and-machines/v2/queries/get-medicine-and-machines': '약물 · 기기 목록(DAY 는 상품 응답 안에서 모은다 — S0 메뉴)',
 'consultation/v1/queries/get-consultations-by-visitor-id': '고객별 상담 기록 목록 — 상담 차트 이력',
 'image/visitor-image/v1/queries/get-visitor-images': '고객 이미지(여권 스캔 등)',
 'meta/connect/v1/queries/get-connect-apps': 'KOS 연결 앱 목록',
 'meta/notice/v1/queries/get-notices': 'KOS 공지',
 'meta/template/v1/queries/get-hospital-text-snippets': '병원 문구 조각(템플릿)',
 'notification/computer-telephone/v1/queries/find-computer-telephone-settings': 'CTI(전화) 설정',
 'notification/message/sender/v1/queries/get-sender-profiles': '메시지 발신 프로필',
 'prescription/v1/queries/get-prescription': '처방전 단건',
 'prescription/v1/queries/get-prescriptions': '처방전 목록',
 'prescription/v1/queries/get-prescriptions-by-ids': '처방전 여러 건(id 로)',
 'procedure-menu/currency-settings/queries/get-currency-settings': '통화 설정 — S0:1505 「두지 않음(지금)」',
 'procedure-menu/procedure-categories/queries/get-procedure-categories': '시술 카테고리 목록 — S0 OQ-041-3',
 'procedure-menu/product-options/v2/queries/search-product-option-summaries': '상품 옵션 검색(수납 화면)',
 'procedure-menu/products/queries/get-product': '상품 단건',
 'procedure-menu/products/v3/queries/get-products': '상품 목록 v3(DAY 는 v1 경로)',
 'procedure-menu/target-countries/v1/queries/get-target-countries': '타겟 국가 — S0:1505 「두지 않음(지금)」',
 'procedure-menu/vat-settings/queries/get-vat-settings': '부가세 설정 — S0:1505 「두지 않음(지금)」',
 'procedure-menu/visitors/queries/get-visitors': '메뉴 쪽 고객 조회(가격 · 수가 유형용으로 보임)',
 'purchase/payment-settings/v1/queries/get-payment-settings': '결제 수단 설정',
 'purchase/prepaid-card/v1/queries/get-visitor-prepaid-card-balance': '고객별 선불카드 잔액 합',
 'purchase/tax-refund-receipts/v1/queries/get-tax-refund-receipts': '택스 리펀드 영수증',
 'purchase/tax-refund-settings/v1/queries/get-tax-refund-settings': '택스 리펀드 설정',
 'schedule/default-operation-time/v1/queries/get-default-reservation-policy': '병원 기본 예약 정책',
 'schedule/group/v1/queries/get-reservation-group': '예약 그룹 단건',
 'schedule/group/v1/queries/get-reservation-group-days-offs': '예약 그룹 휴무 — 앞 판 E4 가능 시간대와 닿음',
 'schedule/occupied-time/v2/queries/get-occupied-times': '점유 시간(예약 현황)',
 'schedule/reservation-rule/v1/queries/get-reservation-rule': '예약 규칙 단건',
 'schedule/reservation-rule/v1/queries/get-reservation-rule-summaries': '예약 규칙 목록',
 'schedule/reservation-time-slot/v1/queries/get-occupied-resources-by-reservation-time-slot': '예약 칸별 점유 — 앞 판 E4 와 닿음',
 'schedule/reservation-time-slot/v1/queries/get-reservation-time-slots': '예약 칸(타임 슬롯) — 앞 판 E4 와 닿음',
 'schedule/v1/queries/get-payment-required-tasks': '수납 필요 작업',
 'schedule/v1/queries/get-schedule-summaries': '일정 요약 목록 — 희망 시술 안쪽 키가 보이는 유일한 HAR 경로(K5-2)',
 'schedule/v2/queries/get-schedule-list-items': '일정 목록 항목(예약이력.har) — 앞 판 E5 · E6 과 닿음',
 'security/v2/queries/check-message-permission': '메시지 권한 확인',
 'v1/visitor/queries/get-visitor': '고객 단건 v1(DAY · cc 는 v2)',
 'visitor/files/v1/queries/get-visitor-files': '고객 파일',
 'visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy': '문진 제출본(내부 · legacy) — P31 공개 경로의 내부 쪽으로 보임 · 같은지 확인 안 됨',
 'visitor/v1/queries/get-custom-attribute-definitions': '고객 사용자 정의 항목 정의 — S0:312 반려(`custom_attributes`)',
}
E = C['D']['entries']; rows = []
for p in sorted(E):
    if p in C['RULES'] or p in ('common/user/v1/queries/get-active-sign-ins',): continue
    files = sorted({x[0] for x in E[p]})
    fl = ' · '.join(f.split('/')[0][:10] + '/…/' + f.split('/')[-1] for f in files[:3]) + (f' 외 {len(files)-3}' if len(files) > 3 else '')
    rows.append(f'| {len(rows)+1} | `{p}` | {len(E[p])} | {fl} | {DESC.get(p, "**설명 없음**")} |')
print('### K1-2. HAR 에만 있는 읽기 경로(대조 안 함 · 목록만)\n')
print('센 방법: HAR 67개의 요청 URL 중 `/queries/` 가 든 경로(테넌트 접두 제거) − K1 의 34경로. 「무엇인지」는 **경로 이름 · HAR 파일 이름 풀이**이고 응답 키로 확인한 것이 아니다.\n')
print('| # | 경로 | 엔트리 | HAR 파일 | 무엇인지(이름 풀이) |'); print('|---|---|---|---|---|')
print('\n'.join(rows)); print()
import sys; print(len(rows), file=sys.stderr)
```

</details>

<details><summary><code>verify.py</code></summary>

```python
# 일회용: 리포트에 HAR 값이 섞였는지 검사 — 출력은 건수와 키 이름뿐(값은 출력하지 않는다)
import sys, re, glob, json, base64, collections
REPORT, ROOT = sys.argv[1], sys.argv[2]
rep = open(REPORT, encoding='utf-8').read()
email = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', rep)
phone = re.findall(r'(?<![0-9])(?:\+?82[- ]?)?0?1[016789][- ]?[0-9]{3,4}[- ]?[0-9]{4}(?![0-9])', rep)
longnum = re.findall(r'(?<![0-9A-Za-z])[0-9]{7,}(?![0-9A-Za-z])', rep)
print('email', len(email)); print('phone', len(phone)); print('digits>=7', len(longnum))
NAMEKEY = re.compile(r'(?i)(name|memo|email|phone|address|passport|registration|birth|chartnumber|accountid|text|title|description|note)')
vals = collections.defaultdict(set)
def walk(n, k=''):
    if isinstance(n, dict):
        for a, b in n.items(): walk(b, a)
    elif isinstance(n, list):
        for x in n: walk(x, k)
    elif isinstance(n, str) and NAMEKEY.search(k):
        v = n.strip()
        if len(v) >= 2: vals[k].add(v)
for f in glob.glob(ROOT + '/**/*.har', recursive=True):
    for e in json.load(open(f, encoding='utf-8'))['log']['entries']:
        c = e['response'].get('content', {}); t = c.get('text')
        if not t: continue
        if c.get('encoding') == 'base64':
            try: t = base64.b64decode(t).decode('utf-8')
            except Exception: continue
        try: walk(json.loads(t))
        except Exception: pass
# 사람 이름 · 연락처 · 메모 꼴 키의 값이 리포트에 그대로 나오나(한글 포함 값 · 2자 이상)
person = re.compile(r'(?i)^(name|realName|visitorName|phoneticName|passportSurname|passportGivenNames|recommenderName|representativeName|memo|migratedMemo|email|phoneNumber|accountId|address|detailedAddress|chartNumber|dateOfBirth|registrationNumber|passportNumber|text|consultationMemo|orderMemo|reservationMemo|assigneeMemo|doctorMemo)$')
hits = collections.Counter(); checked = 0
for k, vs in vals.items():
    if not person.match(k): continue
    for v in vs:
        checked += 1
        if v in rep: hits[k] += 1
print('person-like values checked', checked, 'hits', sum(hits.values()), dict(hits))
# 맞은 값의 꼴만(값은 출력하지 않는다): 길이 · 글자 종류 · 리포트에 나온 횟수 · 앞뒤가 단어 경계인가
def kind(v):
    return ''.join(sorted({('H' if '가' <= ch <= '힣' else 'D' if ch.isdigit() else 'L' if ch.isalpha() else 'S') for ch in v}))
for k, vs in vals.items():
    if not person.match(k): continue
    for v in vs:
        if v in rep:
            whole = len(re.findall(r'(?<![0-9A-Za-z가-힣])' + re.escape(v) + r'(?![0-9A-Za-z가-힣])', rep))
            print('  hit', k, 'len', len(v), 'kind', kind(v), 'count', rep.count(v), 'whole-word', whole)
```

</details>

<details><summary><code>verify2.py</code></summary>

```python
# 일회용: 리포트에 나온 한글 값이 HAR 의 어느 키 경로(모양만)에서 왔는지 — 값은 출력하지 않는다
import sys, re, glob, json, base64, collections
REPORT, ROOT = sys.argv[1], sys.argv[2]
rep = open(REPORT, encoding='utf-8').read()
H = re.compile(r'[가-힣]')
where = collections.defaultdict(set)
def walk(n, path):
    if isinstance(n, dict):
        for a, b in n.items(): walk(b, path + '.' + a)
    elif isinstance(n, list):
        for x in n: walk(x, path + '[]')
    elif isinstance(n, str):
        v = n.strip()
        if len(v) >= 2 and H.search(v) and re.search(r'(?i)name$', path): where[v].add(re.sub(r'^.*?((?:\.[^.\[\]]+(?:\[\])?){1,3})$', r'\1', path))
for f in glob.glob(ROOT + '/**/*.har', recursive=True):
    for e in json.load(open(f, encoding='utf-8'))['log']['entries']:
        c = e['response'].get('content', {}); t = c.get('text')
        if not t: continue
        if c.get('encoding') == 'base64':
            try: t = base64.b64decode(t).decode('utf-8')
            except Exception: continue
        try: walk(json.loads(t), '')
        except Exception: pass
i = 0
for v, ps in where.items():
    if v in rep:
        i += 1
        print(f'hit#{i} len={len(v)} paths={sorted(ps)[:8]}')
```

</details>

## 부록 B. HAR 엔트리 위치(파일#엔트리 번호 · 0부터 · HTTP 상태)

엔트리 번호는 HAR `log.entries[]` 의 순번이다. `200*` = 200 이지만 응답 본문이 JSON 이 아니거나 비어 키를 못 읽음.

- P01 `schedule/zone/v1/queries/get-zones` — `2026-10-12-cc-prototype/로그인.har`#29 ; `2026-10-23-cc-overall-board/har/수납필요 확인.har`#27,30(200*),33,34(200*) ; `2026-10-23-cc-overall-board/har/예약그룹 .har`#155,156(200*),193 ; `2026-10-23-cc-overall-board/har/예약그룹.har`#155,156(200*),193 ; `2026-11-16-cc-charty1/har/예약이력.har`#10
- P02 `schedule/zone/room/v1/queries/get-rooms` — `2026-10-12-cc-prototype/시술완료.har`#1,3(200*) ; `2026-10-12-cc-prototype/시술완료_상태 copy.har`#2 ; `2026-10-12-cc-prototype/시술현황_방배정.har`#1 ; `2026-10-12-cc-prototype/시술현황_새로고침.har`#2 ; `2026-10-12-cc-prototype/의사호출.har`#2,5 ; `2026-10-12-cc-prototype/의사호출_2.har`#1,4 ; `2026-10-23-cc-overall-board/har/고객정보 수정.har`#1 ; `2026-10-23-cc-overall-board/har/설문전송.har`#10 ; `2026-10-23-cc-overall-board/har/예약현황_조회.har`#1 ; `2026-10-23-cc-overall-board/har/방배정.har`#81,82(200*),91 ; `2026-11-09-cc-day/har/고객예약접수시술.har`#29,30(200*) ; `2026-11-09-cc-day/har/방이동.har`#5,12 ; `2026-11-09-cc-day/har/삭제후의사호출.har`#1 ; `2026-11-09-cc-day/har/차트작성2.har`#1 ; `2026-11-09-cc-day/har/차트작성3.har`#1,6,12,20 ; `2026-11-18-day-customer/har/결제취소2.har`#5,81,88,96,103 ; `2026-11-18-day-customer/har/수납추가.har`#5 ; `2026-11-18-day-customer/har/시술사용후환불.har`#16
- P03 `schedule/group/v1/queries/get-reservation-groups` — `2026-10-23-cc-overall-board/har/수납필요 확인.har`#36,111 ; `2026-10-23-cc-overall-board/har/예약그룹 .har`#196 ; `2026-10-23-cc-overall-board/har/예약현황_조회.har`#9 ; `2026-10-23-cc-overall-board/har/예약그룹.har`#196 ; `2026-11-16-cc-charty1/har/상담대기2.har`#9 ; `2026-11-16-cc-charty1/har/상담대기3.har`#9 ; `2026-11-16-cc-charty1/har/예약이력.har`#11
- P04 `role/v2/queries/get-roles` — `2026-10-12-cc-prototype/로그인.har`#30 ; `2026-10-12-cc-prototype/시술완료.har`#0,2(200*) ; `2026-10-12-cc-prototype/의사호출.har`#1 ; `2026-10-12-cc-prototype/의사호출_2.har`#0 ; `2026-10-23-cc-overall-board/har/고객정보 수정.har`#0,9 ; `2026-10-23-cc-overall-board/har/공지사항.har`#0 ; `2026-10-23-cc-overall-board/har/국적_언어_여권번호변경.har`#0 ; `2026-10-23-cc-overall-board/har/귀가.har`#1 ; `2026-10-23-cc-overall-board/har/설문전송.har`#5 ; `2026-10-23-cc-overall-board/har/수납.har`#0,60,65(200*),71 ; `2026-10-23-cc-overall-board/har/수납필요 추가.har`#0 ; `2026-10-23-cc-overall-board/har/수납필요 확인.har`#28,183 ; `2026-10-23-cc-overall-board/har/여권스캔.har`#9 ; `2026-10-23-cc-overall-board/har/예약.har`#1 ; `2026-10-23-cc-overall-board/har/예약그룹 .har`#157 ; `2026-10-23-cc-overall-board/har/예약부도.har`#0 ; `2026-10-23-cc-overall-board/har/예약상세_수정.har`#0 ; `2026-10-23-cc-overall-board/har/예약이동.har`#0 ; `2026-10-23-cc-overall-board/har/예약취소.har`#1 ; `2026-10-23-cc-overall-board/har/예약취소_되돌리기.har`#0 ; `2026-10-23-cc-overall-board/har/예약현황_조회.har`#0 ; `2026-10-23-cc-overall-board/har/처방전.har`#3,6,7,11,12,16,18,23,25,29 ; `2026-10-23-cc-overall-board/har/처방전상세.har`#0 ; `2026-10-23-cc-overall-board/har/방배정.har`#0,3(200*) ; `2026-10-23-cc-overall-board/har/상담.har`#0,45,47(200*) ; `2026-10-23-cc-overall-board/har/예약그룹.har`#157 ; `2026-11-09-cc-day/har/고객예약접수시술.har`#0 ; `2026-11-09-cc-day/har/삭제후의사호출.har`#0 ; `2026-11-09-cc-day/har/차트작성2.har`#0 ; `2026-11-09-cc-day/har/차트작성3.har`#0,2 ; `2026-11-16-cc-charty1/har/병원정보.har`#0 ; `2026-11-16-cc-charty1/har/상담대기.har`#0 ; `2026-11-16-cc-charty1/har/상담대기2.har`#0 ; `2026-11-16-cc-charty1/har/상담대기3.har`#0,102,106,110,118 ; `2026-11-16-cc-charty1/har/예약이력.har`#0,5,6 ; `2026-11-18-day-customer/har/결제 취소.har`#1 ; `2026-11-18-day-customer/har/결제취소2.har`#0,76,83,91,98 ; `2026-11-18-day-customer/har/고객상세.har`#0 ; `2026-11-18-day-customer/har/고객정보.har`#1 ; `2026-11-18-day-customer/har/다회권구매.har`#0 ; `2026-11-18-day-customer/har/선불카드 결제.har`#0 ; `2026-11-18-day-customer/har/선불카드.har`#1 ; `2026-11-18-day-customer/har/선불카드결제.har`#5 ; `2026-11-18-day-customer/har/선불카드결제취소.har`#5,58 ; `2026-11-18-day-customer/har/선불카드공유.har`#12,18 ; `2026-11-18-day-customer/har/선불카드생성.har`#0 ; `2026-11-18-day-customer/har/수납.har`#0,60,65(200*),71 ; `2026-11-18-day-customer/har/수납추가.har`#0 ; `2026-11-18-day-customer/har/시술권2.har`#0 ; `2026-11-18-day-customer/har/용량,수량변경.har`#1 ; `2026-11-18-day-customer/har/재결제.har`#1,23 ; `2026-11-18-day-customer/har/환불1.har`#1 ; `2026-11-18-day-customer/har/환불2.har`#1,50
- P05 `account/v2/queries/get-accounts` — `2026-10-12-cc-prototype/의사호출_2.har`#3 ; `2026-10-23-cc-overall-board/har/고객정보 수정.har`#3,4,34,35,36 ; `2026-10-23-cc-overall-board/har/수납.har`#7,8(200*),46 ; `2026-10-23-cc-overall-board/har/수납필요 추가.har`#7,27 ; `2026-10-23-cc-overall-board/har/수납필요 확인.har`#37,68,70,73,112,191,230 ; `2026-10-23-cc-overall-board/har/예약.har`#5,133,134,135 ; `2026-10-23-cc-overall-board/har/예약현황_조회.har`#7,8 ; `2026-10-23-cc-overall-board/har/처방전.har`#8 ; `2026-10-23-cc-overall-board/har/처방전상세.har`#19,83 ; `2026-11-09-cc-day/har/고객예약접수시술.har`#46,94 ; `2026-11-09-cc-day/har/방이동.har`#4,6(200*) ; `2026-11-11-cc-product/har/상품 수납.har`#38,224,225,226 ; `2026-11-16-cc-charty1/har/상담대기.har`#11 ; `2026-11-16-cc-charty1/har/상담대기2.har`#6,7,8,20 ; `2026-11-16-cc-charty1/har/상담대기3.har`#6,7,8,20 ; `2026-11-16-cc-charty1/har/예약이력.har`#19,20 ; `2026-11-18-day-customer/har/고객상세.har`#2,3,4(200*),5(200*),46,62,63,64 ; `2026-11-18-day-customer/har/고객정보조회 .har`#1,2,12 ; `2026-11-18-day-customer/har/다회권구매.har`#16 ; `2026-11-18-day-customer/har/상품 수납.har`#38,224,225,226 ; `2026-11-18-day-customer/har/선불카드결제.har`#29 ; `2026-11-18-day-customer/har/선불카드결제취소.har`#29 ; `2026-11-18-day-customer/har/수납.har`#7,8(200*),46 ; `2026-11-18-day-customer/har/수납추가.har`#42
- P06 `meta/codes/v1/queries/get-codes` — `2026-10-12-cc-prototype/로그인.har`#26 ; `2026-10-23-cc-overall-board/har/고객정보 수정.har`#16,17,31,32,49 ; `2026-10-23-cc-overall-board/har/수납필요 확인.har`#38,55,65,67,71,72,76,106,108,109,110,154,155 ; `2026-10-23-cc-overall-board/har/여권스캔.har`#15,16 ; `2026-10-23-cc-overall-board/har/예약.har`#6,7,62,64,81,82,93,94,109,110,130,131,138,155,156,167,168,178,179 ; `2026-10-23-cc-overall-board/har/예약그룹 .har`#158,179,180,181,182 ; `2026-10-23-cc-overall-board/har/예약상세_수정.har`#8,9,11,14,15 ; `2026-10-23-cc-overall-board/har/예약취소.har`#10,11,15,16 ; `2026-10-23-cc-overall-board/har/처방전상세.har`#21,22,25,43,44 ; `2026-10-23-cc-overall-board/har/방배정.har`#8,9(200*),101,102,104,107,108 ; `2026-10-23-cc-overall-board/har/상담.har`#6,7(200*),40 ; `2026-10-23-cc-overall-board/har/예약그룹.har`#158,179,180,181,182 ; `2026-11-09-cc-day/har/고객예약접수시술.har`#5 ; `2026-11-11-cc-product/har/상품 수납.har`#127,128,135,136,138,204,205,212,213,215,221,222,238 ; `2026-11-16-cc-charty1/har/상담대기.har`#13,14,17,25,26 ; `2026-11-16-cc-charty1/har/상담대기2.har`#21,22,52,53,61,62,76,77,88 ; `2026-11-16-cc-charty1/har/상담대기3.har`#21,22,52,53,61,62,76,77,88,132,133,140,141,143 ; `2026-11-16-cc-charty1/har/예약이력.har`#12,13 ; `2026-11-18-day-customer/har/고객상세.har`#48,50,59,60,83 ; `2026-11-18-day-customer/har/고객정보.har`#15,16,18,21,22 ; `2026-11-18-day-customer/har/고객정보조회 .har`#15,16 ; `2026-11-18-day-customer/har/상품 수납.har`#127,128,135,136,138,204,205,212,213,215,221,222,238 ; `2026-11-18-day-customer/har/시술권2.har`#8,9,11,14,15
- P07 `schedule/v2/queries/get-schedules-grouped-by-zone` — `2026-10-12-cc-prototype/시술현황_새로고침.har`#3 ; `2026-10-23-cc-overall-board/har/귀가.har`#9,10(200*) ; `2026-10-23-cc-overall-board/har/방배정.har`#83,84(200*)
- P08 `schedule/v1/queries/get-schedule-detail` — `2026-10-23-cc-overall-board/har/수납필요 확인.har`#41 ; `2026-10-23-cc-overall-board/har/예약.har`#102,103(200*),183 ; `2026-10-23-cc-overall-board/har/예약상세_수정.har`#5 ; `2026-10-23-cc-overall-board/har/예약취소.har`#7 ; `2026-10-23-cc-overall-board/har/처방전상세.har`#7 ; `2026-10-23-cc-overall-board/har/방배정.har`#98 ; `2026-11-11-cc-product/har/상품 수납.har`#124,201 ; `2026-11-16-cc-charty1/har/상담대기.har`#6 ; `2026-11-16-cc-charty1/har/상담대기2.har`#82 ; `2026-11-16-cc-charty1/har/상담대기3.har`#82,129 ; `2026-11-18-day-customer/har/고객정보.har`#12 ; `2026-11-18-day-customer/har/상품 수납.har`#124,201 ; `2026-11-18-day-customer/har/시술권2.har`#5
- P09 `procedure-menu/categories/queries/get-categories` — `2026-11-09-cc-day/har/고객예약접수시술.har`#66,68(200*) ; `2026-11-11-cc-product/har/상품 수납.har`#93,95(200*),158 ; `2026-11-18-day-customer/har/상품 수납.har`#93,95(200*),158 ; `2026-11-18-day-customer/har/수납추가.har`#21 ; `2026-11-18-day-customer/har/환불2.har`#89
- P10 `procedure-menu/products/queries/get-products` — `2026-11-11-cc-product/har/상품 수납.har`#103,104(200*),164 ; `2026-11-18-day-customer/har/상품 수납.har`#103,104(200*),164 ; `2026-11-18-day-customer/har/상품가격.har`#2
- P11 `procedure-menu/v2/queries/get-procedures` — `2026-11-11-cc-product/har/상품 수납.har`#96,100(200*),101,102(200*),160,163 ; `2026-11-18-day-customer/har/상품 수납.har`#96,100(200*),101,102(200*),160,163
- P12 `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks` — `2026-10-23-cc-overall-board/har/방배정.har`#58,59(200*) ; `2026-11-09-cc-day/har/고객예약접수시술.har`#15,16(200*)
- P13 `procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product` — `2026-11-18-day-customer/har/결제취소2.har`#34 ; `2026-11-18-day-customer/har/선불카드결제.har`#16 ; `2026-11-18-day-customer/har/선불카드결제취소.har`#16 ; `2026-11-18-day-customer/har/수납추가.har`#37 ; `2026-11-18-day-customer/har/환불2.har`#60
- P14 `procedure-menu/etcetera-products/v1/queries/get-etcetera-products` — `2026-11-09-cc-day/har/고객예약접수시술.har`#63,64(200*) ; `2026-11-18-day-customer/har/수납추가.har`#30
- P15 `purchase/v1/queries/get-purchase-summaries` — `2026-10-23-cc-overall-board/har/귀가.har`#0 ; `2026-10-23-cc-overall-board/har/수납.har`#26,27(200*),35,50,51,53,56,57,68,70,77,79,82,84,85,89,90,94,96,97,99,100,107,109,111,113 ; `2026-10-23-cc-overall-board/har/수납필요 추가.har`#16,21,29,30,37,39,42,46,49,54,60,66,73,74,76,77,83,89,94,95,99,107,112,116,118,119 ; `2026-10-23-cc-overall-board/har/수납필요 확인.har`#152,182,202,210,214,219,224,234,236,241,242,247,248 ; `2026-10-23-cc-overall-board/har/여권스캔.har`#1,2,4,5,6,8,14,19,21,34,36,37,38 ; `2026-10-23-cc-overall-board/har/처방전상세.har`#63,77,81,87,89,90 ; `2026-11-09-cc-day/har/고객예약접수시술.har`#82,83(200*),86,98,101,102,120,121,125,126,132,137,138,139,140 ; `2026-11-09-cc-day/har/차트작성.har`#8,9(200*),13,15,17,23,26,31,34,37,38,44,47,52,56 ; `2026-11-11-cc-product/har/상품 수납.har`#10,11(200*),14,22,24,29,30,33,43,44,46,60,61,62,63,64,66,72,76,145,150,152,154,247,250,253,256,257 ; `2026-11-18-day-customer/har/결제 취소.har`#0,7,12,16,17,18,20 ; `2026-11-18-day-customer/har/결제취소2.har`#7,10,14,19,20,21,23,27,33,40,47,49,55,56,57,60,64,69,70,72,73,75,90,105 ; `2026-11-18-day-customer/har/다회권구매.har`#10,18,20,21,28,30 ; `2026-11-18-day-customer/har/상품 수납.har`#10,11(200*),14,22,24,29,30,33,43,44,46,60,61,62,63,64,66,72,76,145,150,152,154,247,250,253,256,257 ; `2026-11-18-day-customer/har/선불카드 결제.har`#5,9,12,13 ; `2026-11-18-day-customer/har/선불카드.har`#0,7,9,11,15,17,18 ; `2026-11-18-day-customer/har/선불카드결제.har`#2,14,18,19,24,31,33,36,38,40,46,52,55,56 ; `2026-11-18-day-customer/har/선불카드결제취소.har`#2,14,18,19,24,31,33,36,38,40,46,52,55,56,57,64,65,68,71,73,75,77,81,82,83,84 ; `2026-11-18-day-customer/har/선불카드공유.har`#1,4,8,10,11,23,25,26 ; `2026-11-18-day-customer/har/수납.har`#26,27(200*),35,50,51,53,56,57,68,70,77,79,82,84,85,89,90,94,96,97,99,100,107,109,111,113 ; `2026-11-18-day-customer/har/수납추가.har`#10,17,27,31,35,39,45,47,53,55 ; `2026-11-18-day-customer/har/시술권2.har`#27,30 ; `2026-11-18-day-customer/har/시술사용후환불.har`#0,2,6,11,14,18,21,24,28,32,33,35,42,44,50,53,58,59,63,65,67,72,75,76 ; `2026-11-18-day-customer/har/용량,수량변경.har`#0,12,16,21,22,24,28,32,34,39,41,45,46,47 ; `2026-11-18-day-customer/har/재결제.har`#0,7,12,16,17,18,20,21,22,29,33,36,37,41,43 ; `2026-11-18-day-customer/har/환불1.har`#0,7,8,16,23,25,27,29,30,32,33,35,36,37,40,44,46 ; `2026-11-18-day-customer/har/환불2.har`#0,7,8,16,23,25,27,29,30,32,33,35,36,37,40,44,46,47,48,49,63,67,74,76,82,93,102,109,110,111,116,121,123,129,137,139,140,143,144,146,147,148,149,151,152,153,154,155,157,161,162,163,167,168,173,174,178,179
- P16 `ticket/v1/queries/get-ticket-bundles` — `2026-10-23-cc-overall-board/har/고객정보 수정.har`#20,62,63 ; `2026-10-23-cc-overall-board/har/국적_언어_여권번호변경.har`#18,20 ; `2026-10-23-cc-overall-board/har/수납필요 추가.har`#36,41,45,84,100 ; `2026-10-23-cc-overall-board/har/수납필요 확인.har`#84 ; `2026-10-23-cc-overall-board/har/예약.har`#44,45(200*),84,161,170 ; `2026-10-23-cc-overall-board/har/예약상세_수정.har`#19 ; `2026-10-23-cc-overall-board/har/예약취소.har`#20 ; `2026-10-23-cc-overall-board/har/처방전상세.har`#10 ; `2026-10-23-cc-overall-board/har/방배정.har`#39,112 ; `2026-11-09-cc-day/har/고객예약접수시술.har`#14,116 ; `2026-11-11-cc-product/har/상품 수납.har`#67,131,208 ; `2026-11-16-cc-charty1/har/상담대기.har`#8 ; `2026-11-16-cc-charty1/har/상담대기2.har`#49,64 ; `2026-11-16-cc-charty1/har/상담대기3.har`#49,64,136 ; `2026-11-18-day-customer/har/고객상세.har`#20,21(200*),37 ; `2026-11-18-day-customer/har/고객정보.har`#26 ; `2026-11-18-day-customer/har/고객정보조회 .har`#9,13 ; `2026-11-18-day-customer/har/상품 수납.har`#67,131,208 ; `2026-11-18-day-customer/har/시술권2.har`#19 ; `2026-11-18-day-customer/har/시술사용후환불.har`#3,5,36 ; `2026-11-18-day-customer/har/환불1.har`#10 ; `2026-11-18-day-customer/har/환불2.har`#10,124
- P17 `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` — `2026-10-23-cc-overall-board/har/고객정보 수정.har`#18 ; `2026-10-23-cc-overall-board/har/수납.har`#41,42(200*),106 ; `2026-10-23-cc-overall-board/har/수납필요 추가.har`#25,34,70,81 ; `2026-10-23-cc-overall-board/har/수납필요 확인.har`#156,228,240 ; `2026-10-23-cc-overall-board/har/예약.har`#65,67(200*),157 ; `2026-10-23-cc-overall-board/har/예약상세_수정.har`#16 ; `2026-10-23-cc-overall-board/har/예약취소.har`#17 ; `2026-10-23-cc-overall-board/har/처방전상세.har`#45 ; `2026-10-23-cc-overall-board/har/방배정.har`#109 ; `2026-11-09-cc-day/har/고객예약접수시술.har`#92,114 ; `2026-11-11-cc-product/har/상품 수납.har`#36,52,129,206 ; `2026-11-16-cc-charty1/har/상담대기.har`#27 ; `2026-11-16-cc-charty1/har/상담대기2.har`#54 ; `2026-11-16-cc-charty1/har/상담대기3.har`#54,134 ; `2026-11-18-day-customer/har/결제 취소.har`#8,9,15 ; `2026-11-18-day-customer/har/결제취소2.har`#11,13,17,28,44,53,61,63,68 ; `2026-11-18-day-customer/har/고객상세.har`#38,41(200*) ; `2026-11-18-day-customer/har/고객정보.har`#23 ; `2026-11-18-day-customer/har/고객정보조회 .har`#17 ; `2026-11-18-day-customer/har/다회권구매.har`#14,25 ; `2026-11-18-day-customer/har/상품 수납.har`#36,52,129,206 ; `2026-11-18-day-customer/har/선불카드 결제.har`#10 ; `2026-11-18-day-customer/har/선불카드.har`#16 ; `2026-11-18-day-customer/har/선불카드결제.har`#27,45,48 ; `2026-11-18-day-customer/har/선불카드결제취소.har`#27,45,48,69,70,79 ; `2026-11-18-day-customer/har/선불카드생성.har`#5,14 ; `2026-11-18-day-customer/har/수납.har`#41,42(200*),106 ; `2026-11-18-day-customer/har/수납추가.har`#40,52 ; `2026-11-18-day-customer/har/시술권2.har`#16 ; `2026-11-18-day-customer/har/시술사용후환불.har`#37,39,47,51,56,71 ; `2026-11-18-day-customer/har/재결제.har`#8,9,15,31,32,40 ; `2026-11-18-day-customer/har/환불1.har`#11,13,19,22,41 ; `2026-11-18-day-customer/har/환불2.har`#11,13,19,22,41,71,80,106,117,125,127,133,136,159,166,171,177
- P18 `purchase/prepaid-card/v1/queries/get-prepaid-card-charging-events` — `2026-11-18-day-customer/har/선불카드결제.har`#49 ; `2026-11-18-day-customer/har/선불카드결제취소.har`#49 ; `2026-11-18-day-customer/har/선불카드생성.har`#6,15,18
- P19 `purchase/prepaid-card/v1/queries/get-prepaid-card-visitors` — `2026-11-18-day-customer/har/선불카드결제.har`#50 ; `2026-11-18-day-customer/har/선불카드결제취소.har`#50 ; `2026-11-18-day-customer/har/선불카드공유.har`#6 ; `2026-11-18-day-customer/har/선불카드생성.har`#7,16,19
- P20 `visitor/v2/queries/get-visitors` — `2026-10-23-cc-overall-board/har/고객정보 수정.har`#7 ; `2026-10-23-cc-overall-board/har/예약.har`#33,34(200*),149 ; `2026-11-16-cc-charty1/har/상담대기2.har`#42 ; `2026-11-16-cc-charty1/har/상담대기3.har`#42 ; `2026-11-18-day-customer/har/고객상세.har`#7,8(200*) ; `2026-11-18-day-customer/har/고객정보조회 .har`#4 ; `2026-11-18-day-customer/har/선불카드공유.har`#2
- P21 `v1/account/queries/get-user-account` — `2026-10-12-cc-prototype/로그인.har`#15,22(200*)
- P22 `common/v1/tenant/queries/get-user-tenants` — `2026-10-12-cc-prototype/로그인.har`#6,7(200*)
- P23 `common/user/v1/queries/get-active-sign-ins` — 없음
- P24 `visitor/v2/queries/get-visitor` — `2026-10-23-cc-overall-board/har/고객정보 수정.har`#12,39,50,61 ; `2026-10-23-cc-overall-board/har/국적_언어_여권번호변경.har`#17 ; `2026-10-23-cc-overall-board/har/수납필요 확인.har`#39 ; `2026-10-23-cc-overall-board/har/예약.har`#35,36(200*),77,151,164 ; `2026-10-23-cc-overall-board/har/예약상세_수정.har`#1,3 ; `2026-10-23-cc-overall-board/har/예약이동.har`#1 ; `2026-10-23-cc-overall-board/har/예약취소.har`#3,5 ; `2026-10-23-cc-overall-board/har/처방전상세.har`#1,2,5 ; `2026-10-23-cc-overall-board/har/방배정.har`#96 ; `2026-11-11-cc-product/har/상품 수납.har`#120,122,196,199,229,239,240 ; `2026-11-16-cc-charty1/har/상담대기.har`#1,2,4 ; `2026-11-16-cc-charty1/har/상담대기2.har`#44,58 ; `2026-11-16-cc-charty1/har/상담대기3.har`#44,58,126,127 ; `2026-11-18-day-customer/har/고객상세.har`#11,12(200*),67,71,86,87 ; `2026-11-18-day-customer/har/고객정보.har`#7,10 ; `2026-11-18-day-customer/har/고객정보조회 .har`#6 ; `2026-11-18-day-customer/har/상품 수납.har`#120,122,196,199,229,239,240 ; `2026-11-18-day-customer/har/시술권2.har`#1,3
- P25 `v1/hospital/queries/get-hospital` — `2026-11-16-cc-charty1/har/병원정보.har`#2 ; `2026-11-16-cc-charty1/har/예약이력.har`#2
- P26 `schedule/default-operation-time/v1/queries/get-default-operation-timetable` — `2026-10-23-cc-overall-board/har/수납필요 확인.har`#29 ; `2026-10-23-cc-overall-board/har/예약.har`#17,20,115,118 ; `2026-10-23-cc-overall-board/har/예약현황_조회.har`#3 ; `2026-11-11-cc-product/har/상품 수납.har`#111,187 ; `2026-11-16-cc-charty1/har/상담대기2.har`#2,29,32 ; `2026-11-16-cc-charty1/har/상담대기3.har`#2,29,32 ; `2026-11-18-day-customer/har/상품 수납.har`#111,187
- P27 `schedule/default-operation-time/v1/queries/get-default-days-off` — `2026-10-23-cc-overall-board/har/수납필요 확인.har`#0,4,26 ; `2026-10-23-cc-overall-board/har/예약.har`#19,24,89,117,122,175 ; `2026-10-23-cc-overall-board/har/예약현황_조회.har`#2 ; `2026-11-11-cc-product/har/상품 수납.har`#110,186 ; `2026-11-16-cc-charty1/har/상담대기2.har`#1,31,36,74 ; `2026-11-16-cc-charty1/har/상담대기3.har`#1,31,36,74 ; `2026-11-18-day-customer/har/상품 수납.har`#110,186
- P28 `schedule/open/v2/queries/get-reservation-slots-by-groups` — 없음
- P29 `schedule/open/v1/queries/get-schedules-by-visitor` — 없음
- P30 `visitor/open/v1/queries/get-visitor-questionnaire` — 없음
- P31 `visitor/open/v1/queries/get-questionnaire-submit` — 없음
- P32 `schedule/v1/queries/get-schedule-event-logs` — 없음
- P33 `schedule/v2/queries/get-schedules-for-reservation` — `2026-10-23-cc-overall-board/har/수납필요 확인.har`#140 ; `2026-10-23-cc-overall-board/har/예약.har`#22,120 ; `2026-10-23-cc-overall-board/har/예약현황_조회.har`#10,12 ; `2026-11-11-cc-product/har/상품 수납.har`#115,116,191,192 ; `2026-11-16-cc-charty1/har/상담대기2.har`#10,12,34 ; `2026-11-16-cc-charty1/har/상담대기3.har`#10,12,34 ; `2026-11-18-day-customer/har/상품 수납.har`#115,116,191,192
- P34 `visitor/v1/queries/find-duplicated-visitor` — `2026-10-23-cc-overall-board/har/고객정보 수정.har`#56,57(200*) ; `2026-10-23-cc-overall-board/har/국적_언어_여권번호변경.har`#13,14(200*) ; `2026-10-23-cc-overall-board/har/예약.har`#145,146(200*)

## 부록 C. 개인정보 검증

명령(리포트 완성본에 대해 — 출력은 건수 · 키 이름 · 글자 꼴뿐, 값은 출력하지 않음):

```sh
python3 -I verify.py  research-kos-keys-report.md $R   # 이메일 · 전화 · 7자리 이상 숫자 · 사람/연락처/메모 키 값 대조
python3 -I verify2.py research-kos-keys-report.md $R   # 리포트에 나온 한글 값이 HAR 의 어느 엔드포인트 · 키에서 왔는지
```

| 검사 | 결과 |
|---|---|
| 이메일 꼴 `[…]@[…].[a-z]{2,}` | **0** |
| 전화 꼴(국내 휴대 · `+82`) | **0** |
| 7자리 이상 숫자 | **0** |
| HAR 의 사람 · 연락처 · 메모 꼴 키(`name` · `realName` · `phoneticName` · `passport*` · `memo` · `email` · `phoneNumber` · `address` · `chartNumber` · `dateOfBirth` · `registrationNumber` · `accountId` · 메모 4종 등 25키) 값 2,405개 중 리포트에 **문자열로** 나오는 것 | 64 — 아래 셋으로 전부 설명된다 |
| ↳ 숫자만 2 ~ 4자리(`chartNumber` 50 · `address` 1 · `accountId` 3) | 리포트의 코드 줄 번호 · 개수와 겹침(예: `mapper.py:308` 의 `308`) — 그 숫자는 코드 줄 · 집계에서 왔다 |
| ↳ 라틴 2 ~ 3자(`memo` 1 · `name` 1) · 기호만 2자(`name` 1) | 라틴은 다른 낱말의 일부(단어 경계로는 0회) · 기호 2자는 표 · 구분 기호와 같은 글자 |
| ↳ 한글 2 ~ 3자(`name` 7) | `verify2.py` 로 출처를 보면 전부 **직무 이름**(`role.name` · `roleName`) · **코드 이름**(`get-codes`) · **메뉴 · 카테고리 · 기기 이름**(`get-products` · `get-categories` · `get-medicine-and-machines`) · **결제 플랫폼 이름**(`get-payment-settings`) · **이미지 분류 이름**(`get-visitor-images` `category.name`) — 사람 이름 키(고객 `visitor.name` · 직원 `get-accounts data[].name` · `realName` · 담당자 `assignees[].name` 등)에서 온 값은 **0**. 리포트 본문의 일반 낱말(직무 · 단계 이름)과 같은 글자다 |

정리 — 리포트에 실린 HAR 유래 문자열은 **키 경로 · 타입 모양 · KOS 코드값 enum** 뿐이다. 환자 · 직원 이름 · 연락처 · 메모 · 번호 · 토큰 · 쿠키 값 0.
