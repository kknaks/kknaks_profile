# 리뷰 리포트 — agency-settlement / doc 재검수 r2 (2026-10-29)

- 검수자: `reviewer_doc` (task_402f39febcfc · 재검수 — 지시서 `review-doc-2-instructions.md`)
- 대상: `para/projects/summer-star/agency-settlement/` — DEC-001 · SPEC-001 0.2.0(이하 SPEC) · WORK-001(이하 WORK) · 인덱스 README 4개
- 기준: `_RESUME.md` §2 · DEC-001 · 앞 판 `review-spec-007-report.md` · `planner-fix-1/2/3-instructions.md` · 공식 `openapi.yaml` 1.0.1(2026-10-29 받음 · **운영 KOS 호출 0**) · 개념 `no-inference-from-free-text`
- 줄 번호는 검수 시점 워크트리 파일 기준

## 판정: WARN

FAIL 0. **앞 판 F-1 · W-1~W-6 · NOTE 2~5 는 모두 실제로 닫혔다**(§1 표). 새 WARN 은 3건이다.
- **W-1**: 수정 2판의 「첫 승인 달」 판정(⑤ 기준)에 품목을 **어느 달에서도 안 보이게** 하거나 **두 달에 보이게** 하는 길이 셋 있다. 드문 경우지만 R§2 분할 결제 줄의 목적(「한 품목이 두 달에 전액으로 두 번 나오지 않게」)과 DEC-001 「빠짐없이」에 닿는다. **발주 전에 닫기를 권한다** — 몇 줄 고치면 된다.
- **W-2 · W-3**: 이동 흔적(깨진 sources 경로 1 · 역할 문서 2).

① 행 ↔ ⑤ 거래 잇기(§5.4)는 **돈을 틀리게 만들지 않는다.** 금액 · 상태 · 묶음은 늘 ① 에서 오고, ⑤ 는 시각(`at`)만 준다. 못 이으면 「시각 없음」으로 드러날 뿐이다.

---

## 1. 앞 판 지적 — 닫힘 확인

| 앞 판 | 닫힌 자리 (줄) | 판정 |
|---|---|---|
| **F-1** 「없음」 = 404 | SPEC:246 · 250 · 251 · 279 · 391 · 392 · 393 · 시험 #9 SPEC:490 · #9b SPEC:491 · WORK:57 · WORK:72(「없음」 시험은 400 + `NotFound` 꼴로 · 404 → 502) | **닫힘** — 스펙 `FindScheduleByPurchaseIdPurchaseIdNotFoundError` · `GetVisitorVisitorNotFoundError` 와 일치 |
| W-1 ③ 작업 ≠ `_RESUME` | `_RESUME.md:28` 정정 · SPEC:272 · OQ-103 닫음 SPEC:570 | **닫힘** |
| W-2 운영 키 범위 | `_RESUME.md:25` 확장 줄 · SPEC:440 · 507 · WORK:48 · 75 | **닫힘** |
| W-3 분할 결제 두 달 전액 | `_RESUME.md:30` · SPEC:349 · 350 · 354 · 355 · L11 SPEC:521 · 시험 #17 SPEC:499 | **닫힘**(판정 방식에 새 구멍 — 아래 W-1) |
| W-4 환불 품목 금액 · L10 | SPEC:380(444 의 정의 · 원 가격 근거) · L10 SPEC:520 · OQ-102 SPEC:569 | **닫힘** |
| W-5 통화 | SPEC:207 · 208 · 209 · 232 · 419 · 420 · 시험 #18 SPEC:500 · WORK:56 | **닫힘** |
| W-6 배지 | SPEC:144 · 390 · OQ-106 SPEC:573 · SPEC:526 · WORK:75 ⑥ | **닫힘** |
| NOTE 1 결제일 | ⑤ 로 바꿔 OQ-104 닫음 SPEC:571 · §5.4 | **닫힘**(→ 수정 2판 · §2) |
| NOTE 2 오프셋 | SPEC:292 · 342 · 시험 #16 SPEC:498 | **닫힘** |
| NOTE 3 ③ 개인정보 | SPEC:272 · 273 · 449 · 시험 #20 SPEC:502 | **닫힘**(⑤ 는 NOTE 2) |
| NOTE 4 토큰 잠금 | SPEC:261 · 431 · 시험 #19 SPEC:501 | **닫힘** |
| NOTE 5 번호 없는 기본값 | OQ-114 SPEC:581 · OQ-115 SPEC:582 · OQ-117 SPEC:584 | **닫힘** |

---

## FAIL

없음.

## WARN

### W-1. 「첫 승인 달」 판정에서 품목이 빠지거나 두 번 나오는 길 3개

- **SPEC:290** `firstApprovedAt` = ⑤ `transactions[]` 중 `status = APPROVED` 의 `approvedDateTimeUtc` 가장 이른 것(값이 있는 거래만 · 하나도 없으면 「⑤ 에 수납이 안 돌아옴」과 같게)
- **SPEC:352** ⑤ 에 수납이 없으면 「이 달에 승인 행이 있으면 이 달로 본다」 · **SPEC:354** 「다른 달」 = `firstApprovedAt` 의 KST 달 ≠ 조회 달
- **SPEC:499** 시험 #17 이 「⑤ 에 수납이 없으면 이 달 첫 승인으로 봄」을 고정한다
- 근거: `_RESUME.md:30` 「품목 줄은 첫 승인 결제가 있는 달에만 … 한 품목이 두 달에 전액으로 두 번 나오지 않게」 · DEC-001:36 「상품 한 줄씩 **빠짐없이**」

| # | 길 | 결과 | 근거(스펙) |
|---|---|---|---|
| a | **취소된 승인도 「첫 승인」으로 센다.** 9월 승인 → 취소(9월이든 10월이든) → 10월에 다시 결제 | 품목은 9월(순액 0인 달)에만, 10월엔 품목 없는 `payment` 줄만. 10월에 실제로 낸 돈이 상품과 이어지지 않는다(수수료율이 품목마다 다르니 정산이 안 됨) | ⑤ 원 승인 거래는 `APPROVED` 로 남고 취소는 새 거래 · `canceledRefId` = 원거래 `id`(`PurchaseSummaryTransaction.*.canceledRefId` 「취소 참조 ID」 · `getTransactionList` 설명 「환불·취소는 음수 금액의 새 거래 … `canceledRefId`가 원거래의 `id`」) |
| b | **달을 판정하는 시계가 둘이다.** ① 귀속은 `createdTimeUtc`, 첫 승인 달은 ⑤ `approvedDateTimeUtc`. 10-31 23:59 KST 에 생성 · 11-01 00:00 에 승인된 거래가 그 수납의 첫 결제면 | 10월: `firstApprovedAt` 달 = 11월 → `itemsHere = false`(`payment` 줄만). 11월: ① 에 그 수납 행이 없어 묶음 자체가 없다 → **품목이 어느 달에도 안 나온다** | SPEC:339(귀속 = ① `createdTimeUtc`) · SPEC:290 |
| c | **⑤ 시각이 없을 때 대체가 달마다 따로 돈다.** ⑤ 에 수납이 없거나 승인 거래에 `approvedDateTimeUtc` 가 없으면 「이 달에 승인 행이 있으면 이 달」 | 분할 결제 수납이면 승인이 있는 **두 달 모두** `itemsHere = true` → W-3(앞 판)의 이중 노출이 돌아온다. 일부 승인만 시각이 없으면 첫 달을 늦게 잡아 앞 달 품목이 빠진다 | `TransactionPaymentDateTime` 은 `lastUpdatedDateTimeUtc` 만 required · `PurchaseSummaryTransaction.*.paymentDateTime` 설명 「`paymentDateTime.lastUpdatedDateTimeUtc`가 없다면 하위 호환을 위해 `createdDateTimeUtc`를 사용하세요」 → 오래된 거래는 시각 블록이 빌 수 있다 |

- 빈도: 리포트 Q5 기준 10월은 ⑤ 에서 빠진 수납 0 이라 c 는 실물에서 드물다. a · b 는 조사하지 않았다(미확인). L11(SPEC:521)은 「두 달에 걸친 수납 수」만 세서 a · b 를 잡지 못한다
- 고칠 것(셋 다 §6.2 · §5.2 몇 줄):
  - a — 「첫 승인」에서 **전액 취소된 승인은 뺀다**: 같은 수납 ⑤ `CANCELED` 거래의 `canceledRefId` 가 그 승인 `id` 를 가리키고 금액 절댓값 합이 승인 금액과 같으면 제외. 부분 취소는 승인으로 남긴다
  - b — 이 달 ① 에 `APPROVED` 행이 있는데 `firstApprovedAt` 이 **이 달보다 뒤**면 이 달을 첫 승인 달로 본다(「다른 달」을 「앞 달」로만 한정). 또는 달 판정만 ⑤ 거래 `createdDateTimeUtc`(① 의 귀속 시계와 같은 축 · deprecated 지만 스펙이 대체로 지정)로 한다 — 어느 쪽인지는 planner 기본값 + OQ
  - c — 대체로 판정한 수납을 `counts.firstApprovedUnknown` 같은 수로 세어 드러내고 L 줄을 하나 더한다. 대체 판정 자체는 기본값(OQ-116)으로 둬도 된다
  - 시험 #17 에 a · b 두 경우를 더한다

### W-2. SPEC sources 의 DEC 경로가 옛 폴더를 가리킨다(깨진 경로)

- **SPEC:28** `para/projects/summer-star/cc-prototype/10-decision/decision-001-monthly-sales-list.md` — 이 파일은 없다. 실제 = `para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md`
- 같은 이름의 `cc-prototype` 쪽 DEC-001(`decision-001-feature-lab.md`)과 헷갈릴 자리라 기계 치환의 흔적으로 보인다. 위키 링크(`[[decision-001-monthly-sales-list|DEC-001]]` 등)는 4종 모두 볼트에 파일이 하나씩만 있어 문제없다

### W-3. 역할 문서에 cc-prototype 흔적 2곳 (검수 대상 밖 · 다음 리뷰어가 읽는 문서)

- `orchestration/roles/agency-settlement/reviewer/role.md:3` 「담당: **CC Prototype** 문서(SPEC·WORK)와 코드(레포 `kknaksss/agency-settlement`)」
- `orchestration/roles/agency-settlement/reviewer/rules.md:8` 「DEC-001(**레포 구조 · 기능 독립 · 스택**)과 …」 — 이 뜻은 cc-prototype DEC-001(feature-lab)이다. 이 프로젝트의 DEC-001 은 월별 매출 결정이라, WP-REVIEW 리뷰어가 엉뚱한 문서로 대조하게 된다. 「cc-prototype DEC-001」 또는 이 프로젝트 D1-08 로 고칠 것
- 코디 몫(planner allowed_paths 밖)이다

---

## NOTE

1. **§5.4 잇기 — 시각 비교는 「같은 순간」으로.** SPEC:328 의 동점 가르기 「① `lastUpdatedPaymentDateTimeUtc` = ⑤ `paymentDateTime.lastUpdatedDateTimeUtc`」는 통계 API(`format: date-time`)와 수납 API(형식 표기 없는 `string`)를 비교한다. 문자열로 비교하면 소수점 · `Z`/`+00:00` 표기 차이로 동점이 전부 「못 이음」이 된다. 돈은 안 틀리지만(시각만 `null`) L12 가 크게 나온다 → 「파싱한 시각을 초 단위로 비교」 한 줄과 시험 #21 에 표기가 다른 같은 시각 한 쌍을 권한다. 대안 키: ⑤ 거래 `createdDateTimeUtc`(deprecated · 「거래 생성 일시」)는 ① 의 기간 필터(`createdTimeUtc`)와 같은 축이라 동점 가르기에 더 맞을 수 있다 — OQ-120 에 대안으로 적어 두면 L12 결과를 볼 때 쓸 수 있다
2. **⑤ 응답도 꺼낼 것만** — `PurchaseSummary` 에 `purchaseMemo`(자유 텍스트) · `items` · `assignees` 가 같이 온다. SPEC:449(§7.3)는 ③ · ④ 만 적었다. 「⑤ 에서는 `id` · `transactions[].{id,status,paymentType,price,paymentDateTime,canceledRefId}` 만 꺼낸다」 한 줄이면 WP-REVIEW 기준이 된다(W-1 a 를 고치면 `canceledRefId` 가 필요하다)
3. **⑤ 금액은 `PriceAmount`(int32)** — SPEC:274 · 326 은 `price{value,currency}` 로 맞게 적었다. ① `Money.value` 는 int64, ⑤ `PriceAmount.value` 는 int32 다(스펙 `protos.procedure.PriceAmount`). 원화 수납에서는 문제없다 — 비교 때 같은 정수 타입으로 바꾸면 된다
4. **거래 id 가 있는 다른 작업** — 공개 스펙에 `getTransactionList`(`/purchase/open/v1/queries/get-transaction-list`)가 있다. 거래 `id` · `canceledRefId` 가 있고 기간은 「마지막 결제 상태 변경 일시」 기준 · **최대 31일** · `limit` 최대 1000. 지금 계약을 바꾸자는 것이 아니다 — L12 에서 못 이은 거래가 많으면 OQ-120 의 대안 후보로 기록할 것(허용 경로가 하나 늘어 R§2 승인이 필요하다)
5. **DEC-001 본문은 `_RESUME` 정정을 다 따라가지 않았다** — DEC-001:54 D-05 원천에 ③ `findScheduleByPurchaseId` · ⑤ `getPurchaseSummaries` 가 없고(「이름 · 방문일은 일정 상세 등」), 분할 결제 · 결제일 결정(`_RESUME.md:30 · 31`)이 D 줄에 없다. DEC-001:32 「`_RESUME` 가 이긴다」와 SPEC 부록 A(SPEC:603~607)가 `_RESUME` 줄을 직접 매핑하므로 계약은 닫혀 있다. DEC 를 보는 사람을 위해 D-05 · D-06 에 한 줄씩 보태면 좋다(코디 몫)
6. **이동 흔적 — 문구만** — SPEC:472 「시술 현황 링크 — **sales 엔** 없음」. 모듈 이름(`api/sales.py` · `GET /api/sales` · `SALES_*` env)은 폴더 흔적이 아니라 이름이라 그대로 둬도 된다. grep `sales/ · 기능 폴더 · cc-prototype 루트 · SPEC-007 · WORK-011 · DEC-009 · OQ-9nn · D9-` 결과: SPEC:54(0.2.0 변경 기록 — 의도) · DEC-001:57(「기능 폴더가 아니다」 — 의도) 외 0. 옛 cc-prototype 쪽 파일 · 인덱스 줄은 지워져 있다(`git status` 깨끗)
7. **OQ 표 차례** — SPEC:585~587 이 OQ-119 · OQ-120 · OQ-118 순서다. 내용 문제 없음
8. **public 레포 — 대상 문서는 깨끗하다.** grep: 에이전시 이름 15종 · 유입 이름 0 · 금액은 가짜 `1,000,000` 만(SPEC:48 · 141 · 144 · 208 · 209) · UUID/object-id 꼴 0 · env 는 이름만. `_RESUME.md` 의 실제 금액은 지워졌다(`_RESUME.md:26`). **남은 것**: `research-agency-attribution.md`(실제 에이전시 이름 · 금액)가 아직 `orchestration/work/agency-settlement/`(public 레포 · untracked)에 있다. `00-baseline/README.md:8` 은 「public 레포에 두지 않는다」고 적었고 `_RESUME.md:17` 은 [!] 미결 — 커밋 전에 옮겨야 한다
9. **조회 전용 가드** — 허용 경로 상수 5(SPEC:430 · 시험 #2 「정확히 5개」) · 5개 모두 `/queries/` 경로(스펙 확인: `get-transaction-statistics` · `get-purchase-item-statistics` · `find-schedule-by-purchase-id` · `get-visitor` · `get-purchase-summaries`) · `/commands/` 는 토큰 교환 하나. 자유 텍스트 추정 없음(SPEC:412 · 시험 #7)

---

## 2. 수정 2판 — 돈 · 날짜를 틀리게 만드는 길 (지시서 2)

| 질문 | 답 |
|---|---|
| ⑤ 필드가 스펙에 있나 | 있다 — `getPurchaseSummaries` 요청 `purchaseIds`(required · 크기 제한 없음) · 응답 `data[]` = `PurchaseSummary`(`id` required) · `transactions[]` = `PurchaseSummaryTransaction` oneOf 7개(`id` · `status` · `paymentType` · `price` required) · `paymentDateTime` = `TransactionPaymentDateTime`(`lastUpdatedDateTimeUtc` 만 required · `approvedDateTimeUtc` · `canceledDateTimeUtc` · `spentDateTimeUtc` 선택). SPEC:274 표기와 같다 |
| 결제일이 틀린 값이 되나 | 잘못 잇는 길: 수납 · 상태 · 수단 · 금액이 같은 후보가 **하나뿐인데 그게 다른 거래**인 경우만이다(진짜 짝이 ⑤ 에서 빠졌을 때 — 「존재하지 않거나 삭제된」). 드물고, 날짜만 틀리고 돈은 안 틀린다. 그 밖엔 「못 이음 → `at null`」로 안전하게 드러난다(SPEC:330) |
| 같은 수단 · 같은 금액 두 건 | SPEC:328 — 「마지막 상태 변경 일시」로 가르고, 그래도 같으면 못 이음. 다른 달 승인이 후보에 섞여도(⑤ 는 수납 전체 거래를 준다) 이 비교로 갈린다. 표기 차이는 NOTE 1 |
| 돈(금액 · 상태 · 묶음) | ① 그대로(SPEC:330 「달에서 빠지지 않는다」) — ⑤ 는 금액에 손대지 않는다. **유일한 돈 경로는 ⑤ 가 정하는 「품목을 보일 달」**(W-1) |
| ① 귀속 ≠ 보이는 결제일 | OQ-119(SPEC:585) · `counts.atOutsideMonth` · L12 로 드러냄. W-1 b 는 이 차이가 **품목 노출**까지 번지는 경우다 |

## 3. DEC-001 D-01~D-09 · `_RESUME` §2 대조 (지시서 4)

| 원천 | SPEC 자리 | 판정 |
|---|---|---|
| D-01 월별 · 기본 이번 달 · 수수료 · 필터 · 엑셀 밖 | SPEC:120~123 · 169 · 74~76 | 같음 |
| D-02 한 줄 = 품목 · 수납 묶음 · 품목 금액 · 결제 수단 수납 참고 | SPEC:129~142 · 206 | 같음(`payment` 줄은 R§2 분할 결제 줄로 생긴 것) |
| D-03 칸 9개 · 이름 안 가림 | SPEC:131~142 | 같음 |
| D-04 `visitorFunnelName` | SPEC:293 · 409 | 같음 |
| D-05 운영 조회만 · `/queries/` | SPEC:266~280 · 430 | 같음(원천 목록은 `_RESUME:28 · 31` 로 넓어짐 — NOTE 5) |
| D-06 결제 시각 귀속 · 취소 달 음수 줄 | SPEC:339 · 351 · 364 | 같음(W-1 b 주의) |
| D-07 선불카드 · 기타 상품 포함 | SPEC:138 · 400~403 | 같음 |
| **D-08 별도 프로젝트 · 레포 루트 `back/` · `front/` · 디자인 복사** | SPEC:62 · 85~109 · 454~474 · WORK:42 · 54 | 같음 |
| D-09 로컬만 | SPEC:447 · 550~562 | 같음 |
| `_RESUME:25` 운영 키 확장 | SPEC:440 · 507 · WORK:48 · 75 | 같음 |
| `_RESUME:28` ③ 정정 | SPEC:272 · 570 | 같음 |
| `_RESUME:30` 분할 결제 | SPEC:349~355 | 같음(판정 방식 W-1) |
| `_RESUME:31` ⑤ · 결제일 | SPEC:274 · 288~290 · 319~331 · 571 | 같음 |
| `_RESUME:33` 별도 프로젝트 | SPEC:54 · 62 · 85 · WORK:42 | 같음 |

frontmatter: DEC-001 · SPEC-001 · WORK-001 모두 `product: agency-settlement` · `id` 새 번호 · `links` 새 번호(DEC→SPEC/WORK · SPEC→DEC/WORK · WORK→DEC/SPEC). 인덱스: `20-spec/README.md:5` 0.2.0 · `30-work/README.md:5` SPEC-001 0.2.0 · `10-decision/README.md:5` · 루트 `README.md` 표 — 판 · 링크 파일명 일치. 깨진 경로는 W-2 하나.

---

## 고객이 실물에서 만날 자리

앞 판 목록 중 1(11월 날짜)은 ⑤ 결제일로 줄었고(OQ-119 경계만 남음), 2(지난 달 배지)는 안내 한 줄로 막혔다(SPEC:124). 새로 생기거나 남은 것:

1. **「시각 없음」 줄** — ⑤ 와 못 이은 거래는 결제일이 `—` · 묶음이 맨 뒤로 간다(SPEC:330 · 151). L12 가 크면 표 끝에 몰려 보인다(NOTE 1)
2. **품목 없는 결제 줄 「품목은 MM월에」** — 분할 결제 · 재결제 수납. W-1 a 경우엔 그 「MM월」이 환불로 순액 0 인 달이라, 그 달을 열어도 품목 +X · 취소 −X 만 있어 헷갈린다
3. **결제일이 다른 달 날짜** — 10-31 밤 생성 · 11-01 승인처럼 경계에 걸친 거래(OQ-119 · `atOutsideMonth`)
4. **첫 승인 달 묶음의 `⚠ 결제 ≠ 품목`** — 분할 결제 수납은 첫 달에 품목 전액 · 그달 결제 일부라 늘 배지가 뜬다(SPEC:390 — 의도 · L5 뒤 재정)
5. **처음 열 때 수십 초** — ⑤ 몇 회가 더해졌다(SPEC:317). 문구는 그대로 맞다
6. 앞 판 6 · 7 · 9 · 10(선불카드 판매 · 사용 둘 다 보임 · 유입은 지금 값 · 1초 틈 · `미수납` 배지)은 계약상 그대로다(OQ-112 · OQ-109 · OQ-101 · SPEC:376)

## 참고(기존 부채)

- `reference/2026-10-12-cc-prototype/kos-demo-api.md:30` 「`KOS_API_tenent` 절대 쓰지 않는다」 — cc-prototype 범위 문서라 그대로 두는 게 맞다. SPEC:441 이 「그쪽 운영 키 금지는 그대로」로 경계를 적어 두었다
