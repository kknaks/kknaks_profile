# 리뷰 리포트 — agency-settlement / doc (2026-10-29)

- 검수자: cc-prototype `reviewer_doc` (task_402f39febcfc)
- 대상: `para/projects/summer-star/cc-prototype/20-spec/spec-007-monthly-sales-list.md`(이하 SPEC) · `30-work/work-011-monthly-sales-list.md`(이하 WORK) · `20-spec/README.md` · `30-work/README.md` 인덱스 줄
- 기준: DEC-009 · `_RESUME.md` §2 · `research-agency-attribution.md`(이하 리포트) · 공식 `openapi.yaml` 1.0.1(2026-10-29 받음 · 운영 KOS 호출 0) · 개념 `no-inference-from-free-text`
- 줄 번호는 검수 시점 워크트리 파일 기준

## 판정: FAIL

FAIL 1건 — KOS 는 「없음」을 **404 가 아니라 400 `NotFound`** 로 준다. SPEC 대로 만들면 수납 하나가 일정에 안 걸려도 그달 전체가 오류로 끝나고, 단위 시험(404 가짜 응답)은 초록으로 통과한다. 나머지는 WARN 6 · NOTE 8. 고치면 PASS 로 볼 수 있는 수준이다 — DEC-009 D-01~D-09 는 빠짐없이 들어갔고, 자유 텍스트 추정 · `/commands/` 쓰기 경로 · 실명 · 실금액 · 키는 계약에 없다.

---

## FAIL

### F-1. 일정 · 손님 「없음」 판정이 404 기준 — KOS 는 400 + `errorProperties[].reason = NotFound`

- **SPEC:343** (§6.4 「일정 없음」) 「③ 이 404 이거나 `data` 가 비면 … ④ 도 404 면 `visitorName = null`. 그 밖의 ③ · ④ 실패는 달 전체 오류」
- **SPEC:227** (§4.3) `kos_rejected` = 「KOS 4xx」 → 502 · **SPEC:231** 「그 밖의 실패는 달 전체를 오류로」
- **SPEC:435** (§9.1 #9) 「일정 없음(③ 404) → ④ … ④ 도 404」
- **WORK:71** WP-BE 완료 조건 = §9.1 1~15 통과
- 근거(스펙):
  - `info.description` 「에러 응답」 — 「조회 혹은 명령을 정상적으로 처리할 수 없는 경우, `400` HTTP 상태 코드와 함께」 · `reason: NotFound` = 「대상이 없음」
  - `findScheduleByPurchaseId` 400 = `FindScheduleByPurchaseIdPurchaseIdNotFoundError` — 예시 `{status: 400, className: InvalidRequestException, errorProperties: [{key: purchaseId, reason: NotFound}]}` 「수납 ID에 해당하는 스케줄을 찾을 수 없는 경우」
  - `getVisitor` 400 = `GetVisitorVisitorNotFoundError` — `{key: visitorId, reason: NotFound}` 「없거나 이미 삭제된 내원객」
  - 응답 스키마 `FindScheduleByPurchaseIdQueryResponse.data` · `GetVisitorResponse.data` 는 **required** — 「`data` 가 비면」은 스펙상 오지 않는 모양
  - 404 는 경로가 없을 때 나온다(`kos-demo-api.md:175` — `No static resource …`). 즉 404 를 「없음」으로 받으면 **경로 오타를 「일정 없음」으로 삼킨다**
- 실패 모양: 운영에서 일정에 안 걸린 수납 1건 → ③ 400 → §4.3 「4xx → `kos_rejected`」 → 10월 전체 502. 가짜 transport 는 404 로 시험하니 WP-BE 는 초록 · WP-LIVE 에서야 터진다(rules 「조용히 통과하는 자리」)
- 고칠 것: 「없음」 = **HTTP 400 이고 `errorProperties` 에 `{key: purchaseId|visitorId, reason: NotFound}`** 가 있을 때만. 그 밖 400 은 `kos_rejected`. 404 는 「없음」이 아니라 `kos_rejected`(경로 오류). §9.1 #9 를 이 모양으로 바꾸고 「400 이지만 다른 reason → 달 전체 502」 시험을 하나 더한다

---

## WARN

### W-1. 이름 · 방문일 작업이 `_RESUME` §2 와 다르다 — 발주 전 코디가 SoT 를 맞춰야

- **SPEC:251** ③ `findScheduleByPurchaseId` · **SPEC:504** OQ-903 「새로 · 코디 확인」
- 근거: `_RESUME.md:27` 「이름·방문일은 `getScheduleDetail`」 · SPEC:42 자기 SSOT 순서 「① `_RESUME` §2 … 이기는 순」 · DEC-009:63 열린 것 「이름 · 방문일을 어느 작업에서 읽을지」
- 판단: SPEC 의 대체 이유는 맞다 — ① · ② 응답에 일정 id 가 없고(스펙 `OpenTransactionStatisticsItem` · `OpenPurchaseItemStatisticsItem` 에 `scheduleId` 없음), ③ 응답은 `getScheduleDetail` 과 같은 `ScheduleContract` 다. 다만 SoT(`_RESUME`)가 다른 작업을 적고 있으니 **`_RESUME` §2 에 한 줄을 고치거나 더해** OQ-903 을 닫고 발주해야 한다. 열린 채 발주하면 워커가 SoT 와 SPEC 중 하나를 골라야 한다

### W-2. 운영 키 허용 범위 — `_RESUME` §2 는 「조사 단계에 한해」

- **SPEC:387** (§7.2) 운영 명동점 키를 `sales/.env` 에 · **WORK:48 · WORK:74** WP-LIVE 운영 조회
- 근거: `_RESUME.md:24` 「cc-prototype 의 「운영 키 금지」(kos-demo-api.md §1.2)는 **이 작업 조사 단계에 한해** 풀림」 · `kos-demo-api.md:30` 「`KOS_API_tenent` … 절대 쓰지 않는다」. DEC-009:54 D-05 는 「사용자 지시(운영 조회 허용 · 10-29)」로 기능까지 넓혀 적었다
- 판단: DEC 와 `_RESUME` 가 다르면 `_RESUME` 가 이긴다(DEC-009:32). 사용자 허용이 기능 코드 · WP-LIVE 까지인지 `_RESUME` §2 에 한 줄로 남겨야 한다. 지금 문서만 보면 WP-LIVE 가 SoT 밖이다

### W-3. 분할 결제가 달을 넘으면 같은 품목이 두 달에 다 나온다 — D-06 「결제 시각 귀속」과 어긋날 수 있다

- **SPEC:307** (§6.2) 「두 달 모두 품목 줄을 보인다 — `⚠ 결제 ≠ 품목`」 · **SPEC:507** OQ-906 「planner 기본값」
- 근거: DEC-009:55 D-06 「월 귀속 = 결제 시각(KST) 기준」 · DEC-009:36 「결제 내역을 상품 한 줄씩 **빠짐없이**」. 정산 쓰임새(수수료율이 품목마다 다름 — DEC-009 Context)에서 달마다 리스트를 뽑으면 그 품목은 **두 달 모두에서 전액으로** 세진다. 몇 건인지는 SPEC 도 「미확인」
- 판단: 이번 판엔 합계가 없어 화면에서 더해지진 않지만, 「한 품목이 두 번 나온다」는 돈 정책이라 planner 기본값으로 둘 자리가 아니다. OQ-906 상태를 「사용자」로 올리고, WP-LIVE 에 「승인 결제가 두 달에 걸친 수납 수」를 L 항목으로 세게 하라(아래 W-4 와 같이)

### W-4. 환불 품목 금액(OQ-902)을 WP-LIVE 에서 볼 확인 줄이 없다 — 이중 차감 가능

- **SPEC:332 · SPEC:503** OQ-902 「WP-LIVE 에서 환불 품목 한 건의 값을 보고 정함」 · **SPEC:447~457** §9.2 L1~L9 에 해당 줄 없음 · **WORK:93** 「OQ-902 … WP-LIVE 에서 실물로 보고 사용자에게 올린다」
- 근거: 스펙 `OpenPurchaseItemCost.totalAmount` = 「잔존 가치 금액 또는 최종가」. 리포트 Q6 — 품목 `REFUNDED` 28 · `PARTIALLY_REFUNDED` 12 · 취소 행 25/25 음수
- 돈 경로: 같은 달 승인 + 같은 달 취소인 수납에서 ② 금액이 **잔존(0)** 이면 품목 줄 0 + 취소 줄 −X → 그 수납이 **−X 로 보인다(이중 차감)**. **원 가격**이면 +X −X = 0 으로 맞다. 어느 쪽인지에 따라 리스트가 틀린다
- 고칠 것: §9.2 에 L10 「`REFUNDED` · `PARTIALLY_REFUNDED` 품목이 있는 수납 수 · 그중 `approvedTotal ≠ itemsTotal` 수」를 넣는다. 잔존 값으로 판명되면 그 수납들이 전부 `⚠ 결제 ≠ 품목`(W-6 · §4-7 ③)이 되므로 판정 기준이 된다. DEC-009:38 「품목 금액 합 = 결제 합(444/444)」이 **무엇을 무엇과**(승인만? 취소 뺀 순액?) 비교한 수인지 리포트에 없다(리포트엔 392 만 있음 — `research-agency-attribution.md:130`) → 코디가 444 의 정의를 SPEC §9.2 L5 옆에 적어 두면 OQ-902 가 바로 닫힌다

### W-5. 통화 — 화면 계약은 「통화 코드 같이」인데 응답에 통화 필드가 없다

- **SPEC:367** (§6.7) 「통화가 `KRW` 가 아닌 행 = … 금액 칸에 통화 코드를 같이 보인다」
- **SPEC:213** (§4.2) `lines[].amount` 정수만 · `approvedTotal` · `itemsTotal` 정수 합 — `currency` 필드 없음 · **WORK:56** 응답 고정점에도 없음
- 근거: 스펙 `protos.Money = {currency, value}`
- 판단: front 가 구현할 수 없는 계약(빈칸을 추측으로 메워야 함 — rules 「워커가 추측으로 메워야 하는 빈칸」). 둘 중 하나로 닫아라: (a) `lines[].currency` · 수납 `currency` 를 넣고 다른 통화가 섞이면 `approvedTotal` 을 어떻게 하는지 적기, (b) KRW 아닌 행은 줄로 만들지 않고 `ignoredTransactions` 처럼 따로 세기. 운영 10월은 전부 KRW(리포트 Q6)라 실물 영향은 낮다

### W-6. `⚠ 결제 ≠ 품목` 비교가 「그달 승인 결제(총액)」 ↔ 「품목 현재 금액」 — 정상 수납에도 뜰 자리가 구조적으로 있다

- **SPEC:134 · SPEC:342** 머리 배지 · **SPEC:190~191** `approvedTotal` = 그달 `APPROVED` 합 · `itemsTotal` = 품목 줄 합
- 배지가 정상인데도 뜨는 경우: ① 분할 결제가 달을 넘음(W-3) ② 환불 품목 금액이 잔존 값(W-4) ③ 앞 달에 일부 결제 · 이번 달 나머지 결제. 세 경우 모두 데이터 오류가 아닌데 같은 배지다
- 판단: 「숨김 없이 드러냄」 원칙은 맞다. 다만 배지가 많이 뜨면 진짜 품목 누락을 못 알아본다. WP-LIVE L5 결과를 보고 배지 문구 · 조건을 정할 것을 OQ-906 에 적어 두라

---

## NOTE

1. **결제일 = `lastUpdatedPaymentDateTimeUtc`**(SPEC:263 · SPEC:273 · OQ-904 SPEC:505) — 필드는 스펙에 있다(`OpenTransactionStatisticsItem.lastUpdatedPaymentDateTimeUtc` 「마지막 결제 상태 변경 일시」). 기간 필터(`createdTimeUtc`)와 다른 시각이라 10월 리스트 머리에 11월 날짜가 찍힐 수 있다(§4-7 ①). 대안(`getPurchaseSummaries` 의 결제 일시)은 허용 경로가 하나 느는 일이라 사용자 결정으로 올려 두면 된다
2. **`reservation.startDateTime` 은 UTC 고정이 아니다**(SPEC:266) — 스펙 `ScheduleDetailReservationContract.startDateTime` 설명은 「ISO 8601 date-time」뿐(…`Utc` 접미사 없음). 구현은 오프셋을 읽어 KST 로 바꿔야 하고 `Z` 를 가정하면 안 된다 — §9.1 에 `+09:00` 로 오는 값 시험 하나
3. **③ 응답은 개인정보가 많다** — `ScheduleContract` 에 `visitor.phone` · `dateOfBirth` · `chartNumber` · `memo` · `reservation.reservationMemo` 가 같이 온다. SPEC §7.3(SPEC:395~396)은 응답 · 로그만 말한다. 「③ · ④ 응답에서 `name` · `startDateTime` 둘만 꺼내고 원본은 캐시 · 로그에 남기지 않는다」를 한 줄 넣으면 WP-REVIEW 가 볼 기준이 생긴다
4. **토큰 만료 중 동시 8개** — 401 이 동시에 8개 나면 각자 토큰을 다시 받는다(SPEC:227 · SPEC:240). 「토큰 다시 받기는 한 번만(잠금)」을 §7.1 에 적어 두면 L8(토큰 교환 외 `/commands/` 0)이 깔끔하다. 현재 문구로도 L8 은 통과(종류 기준)
5. **기본값인데 OQ 번호가 없는 것** — 「일부 실패면 달 전체 오류」(SPEC:231) · `REQUESTED` · `FAILED` 제외(SPEC:318) · `Cache-Control: no-store`(SPEC:162). 정책 영향은 작지만 SPEC:44 스스로 「기본값 = §11 OQ 에 같이 올림」이라 했다
6. **KOS 필드 실재 — 전부 있음.** 경로 5개(①~④ · 토큰 교환) operationId 일치 · ① 요청 `createdTimeUtcFrom/To` · `limit`(1~5000) · `cursor` · 응답 `totalCount`(첫 페이지만) · `nextCursor`(마지막 페이지엔 없음) · `purchaseId` · `status`(enum `REQUESTED/APPROVED/CANCELED/SPENT/FAILED`) · `paymentType` · `cost.totalAmount` · `lastUpdatedPaymentDateTimeUtc` · `visitorId` · `visitorFunnelName` / ② 요청 `createdDateTimeUtcFrom/To` · 응답 `purchaseItemType`(enum 에 `PurchaseItemType_UNSPECIFIED` 포함 — SPEC:210 맞음) · `purchaseStatus`(enum 에 `PURCHASE_STATUS_UNSPECIFIED` 도 있음 → SPEC:329 「그 밖 = 값 그대로」로 덮임) · `productTitle` · `productOptionTitle` · `prepaidCardName` · `etceteraProductName` · `cost.totalAmount` / ③ 요청 `purchaseId` · 응답 `data.visitor.name`(required) · `data.reservation.startDateTime`(required) / ④ 요청 `id` · 응답 `data.name`(required) / 토큰 `{key}` → `{token}`(최상위 — `data` 감싸기 아님. SPEC:253 표기 맞음). 조인 키 `purchaseId` 는 ① · ② 둘 다 required. 품목 통계 필터(`purchaseItemTypes` · `purchaseStatuses` 등)는 SPEC 이 안 쓴다 — 기간만 쓰는 게 「빼지 않고 다 보인다」(D-07)와 맞다
7. **public — 대상 세 문서는 깨끗하다.** grep: 에이전시 이름 15종 · `본사` 등 유입 이름 0 · 금액은 가짜 `1,000,000` 만(SPEC:46 · 131 · 134 · 190 · 191) · UUID/object-id 꼴 0 · env 는 이름만(`KOS_API_tenent` · `KOS_OPEN_API_KEY`). **대상 밖 주의**: 같은 PR 에 들어갈 `orchestration/work/agency-settlement/` 에서 `_RESUME.md:25` 에 실제 금액(10월 결제 · 환불 합)이, `research-agency-attribution.md` Q1 · Q7 에 실제 에이전시 이름 · 금액이 있다(`_RESUME.md:16` 이 리포트만 [!] 로 적어 둠 — `:25` 도 같이)
8. **조회 전용 가드 — 쓰기 길 없음.** 허용 경로 상수 4 + `/queries/` 포함 검사 · 토큰 교환은 인증 함수 전용 상수(SPEC:377~381) · 내부 API 복사 안 함(SPEC:379) · back 경로는 GET 2개(SPEC:161) · WORK:71 grep 완료 조건. 자유 텍스트(`visitorFunnelDetail` · `reservationMemo` · 메모)는 읽지 않고(SPEC:362) 시험 #7(SPEC:433)이 있다 — 개념 `no-inference-from-free-text` 위반 없음

---

## DEC-009 대조 (§4-1)

| D | SPEC 자리 | 판정 |
|---|---|---|
| D-01 월별 · 기본 이번 달 · 수수료 · 필터 · 엑셀 밖 | SPEC:111~114 · 158 · 66~68 | 같음 |
| D-02 한 줄 = 품목 · 수납 묶음 · 품목 금액 · 결제 수단은 수납 참고 | SPEC:119~131 · 189 | 같음 (W-3 · W-6 은 금액 해석) |
| D-03 칸 9개 · 이름 안 가림 | SPEC:121~132 | 같음 (+ 품목 종류 = D-07) |
| D-04 `visitorFunnelName` · 예약 유입 아님 | SPEC:267 · 359 | 같음 |
| D-05 운영 조회만 · `/queries/` · 원천 작업 | SPEC:247~257 · 377 | 같음 (작업 선택은 W-1 · 키 범위는 W-2) |
| D-06 결제 시각 귀속 · 취소는 취소 달 음수 줄 | SPEC:297 · 306 · 316~317 | 같음 (분할 결제 W-3) |
| D-07 선불카드 · 기타 상품 포함 · 품목 종류 칸 · 상품명 대체 | SPEC:128 · 350~353 | 같음 |
| D-08 `sales/` · procedure 디자인 복사 · import 금지 | SPEC:77~98 · 401~418 | 같음 |
| D-09 로컬만 | SPEC:393 · 486~496 | 같음 |

결정에 없는 정책 중 OQ 밖에 있는 것: NOTE 5 의 세 가지(영향 작음). 분할 결제 정책(W-3)은 OQ 안에 있으나 상태가 「planner 기본값」이라 올려야 한다.

## BE↔FE 계약 · WP (§4-6)

- §4.2 shape · §4.3 오류 6종 · §3.4 상태 5종이 닫혀 있다. 빈칸은 W-5(통화) 하나
- WORK WP 4개 모두 완료 조건 · 검증 명령이 있다(WP-REVIEW 는 판정 PASS 가 조건 · 명령 없음 — 리뷰라 맞음). WP-BE 완료 조건이 §9.1 을 가리키므로 F-1 을 고치면 WP-BE 도 같이 고쳐진다
- 인덱스 두 줄(`20-spec/README.md` · `30-work/README.md`) — id · 판 0.1.0 · draft · 링크 파일명 일치

---

## 사용자가 실물에서 만날 자리 (§4-7)

막히지는 않는데 화면에서 이상해 보일 곳.

1. **10월 리스트에 11월 날짜** — 결제일이 「마지막 상태 변경 일시」라, 10월 말 승인 · 11월 초 취소면 10월 묶음 머리에 11월 날짜가 보일 수 있다(NOTE 1). 정렬도 그 값으로 된다
2. **지난 달 품목 배지가 바뀐다** — 10월에 판 품목을 11월에 환불하면, 10월 리스트를 다시 열 때 그 품목이 `환불` 배지인데 10월엔 음수 줄이 없다(SPEC:331 — 의도된 동작이지만 설명 없이 보면 버그로 보인다). 화면에 「상태는 지금 기준」 한 줄 안내가 있으면 좋다
3. **환불 수납마다 `⚠ 결제 ≠ 품목`** — 환불 품목 금액이 잔존 값이면 환불 · 부분 환불 수납이 모두 경고 배지(W-4 · W-6). 10월 기준 수납 `REFUNDED` 14 · `PARTIALLY_REFUNDED` 2(리포트 Q6)
4. **같은 품목이 두 달에** — 분할 결제가 달을 넘은 수납(W-3)
5. **품목 없는 묶음** — 원 결제가 앞 달이고 이번 달 취소만 있는 수납은 머리 + 음수 줄만, 「그달 결제 0」(SPEC:306). 리포트 Q5 기준 10월에 3행
6. **선불카드 판매 줄과 선불카드로 결제한 시술 줄이 둘 다** — 눈으로 더하면 이중 계산(SPEC:353 · 리포트 Q6 ⚠). 합계가 없으니 수치는 안 틀리지만, 정산 상대(에이전시)와 리스트를 맞춰 볼 때 혼동 자리
7. **유입이 지금 값** — 지난 달을 다시 보면 그 사이 바뀐 유입이 보인다(OQ-909). `(없음)` 은 일정 기준 8.9%(리포트 Q3)
8. **처음 열 때 수십 초** — 수납마다 ③ 1회(10월 약 390회 · 동시 8). 스피너 문구가 있다(SPEC:146). 이번 달은 600초 캐시라 그 사이 새 결제가 안 보인다 → `[다시 불러오기]`
9. **1초 틈** — 달 끝 23:59:59 KST 의 마지막 1초 결제가 빠질 수 있다(OQ-901)
10. **같은 수납 안 `미수납` 배지** — 품목 `INITIALIZED`(SPEC:328)가 승인 결제가 있는 수납 안에 섞여 보일 수 있다(리포트 Q6 수납 `INITIALIZED` 7)

## 참고(기존 부채)

- `kos-demo-api.md:30` 「`KOS_API_tenent` 절대 쓰지 않는다」가 그대로다. W-2 를 닫을 때 이 문서도 「sales 기능은 예외 — `_RESUME` agency-settlement §2」 같은 한 줄이 필요한지 코디가 판단
