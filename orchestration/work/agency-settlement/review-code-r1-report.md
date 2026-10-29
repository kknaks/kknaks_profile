# 리뷰 리포트 — agency-settlement / code r1 (2026-10-29)

- 대상: 워크트리 `agency-settlement`(base `origin/main` 7de892e) 의 커밋 안 된 `back/**` · `front/**` · `README.md`
- 기준: SPEC-001 0.2.1 · WORK-001 WP-REVIEW 행 · DEC-001(부록 A 경유) · KOS openapi 1.0.1(2026-10-29 받음 · 읽기만)
- 직접 돌린 것(파일 안 바꿈): `uv run pytest -q` = **63 passed** · `uv run ruff check .` = **All checks passed** · `npx tsc --noEmit` = **0**. 가짜 transport 로 경계 사례 5개 탐침(스크래치 스크립트 · 레포 밖). 운영 · 데모 KOS 호출 0 · 서버 안 띄움

## 판정: **WARN** (FAIL 0 · WARN 7 · NOTE 9)

`/commands/` 로 가는 길 · 개인정보 로그 · 자유 텍스트 읽기 · cc-prototype import 는 **0**. 가드 · 「없음」 판정 · ③④⑤ 필드 줄이기 · 첫 승인 판정(s1~s5) · 결제일 · 정렬 · 계약 필드는 SPEC 과 같다.
WP-LIVE 전에 고치는 것을 권하는 것은 **W-1 · W-2** 두 개다. W-2 를 고치지 않으면 L2 를 확인할 방법이 없다.

---

## FAIL

없음.

## WARN

### W-1 ⑤ 에 수납은 있는데 `APPROVED` 거래가 0 이면 품목이 어느 달에도 안 나오고, 세는 곳도 없다
- `back/app/service/sales.py:253-255` — `cands` 가 비면 `First(items_here=False, first_approved_at=None)` · `unknown=False`
- 근거: SPEC §6.2 머리글 「한 수납의 품목은 **어느 달에든 정확히 한 번**」 · §6.2 끝 줄 「대체를 탄 수납은 전부 `firstApprovedUnknown` 으로 세어 드러낸다 — L11」 · 가장 가까운 규칙은 §6.2 표 「⑤ 에 수납 없음」(첫 승인을 정할 수 없다 → 이 달 승인 행이 있으면 `itemsHere = true` + `firstApprovedUnknown`)
- 탐침(가짜 transport): ① 10월 `APPROVED` 1행 · ⑤ 에 그 수납 = `REQUESTED` 거래만 → `itemsHere false` · `payment` 줄 1 · 머리 「품목은 다른 달에」(날짜 없음) · `itemsElsewhere 1` · `firstApprovedUnknown 0`. **품목은 어느 달에도 안 나온다.** 그런데 L11 에는 정상적인 분할 결제(`itemsElsewhere`)로 섞여 보인다
- backend 가 「SPEC 언급 없음」으로 적은 판단. **SPEC 원칙(한 번 · 대체는 센다)과 어긋난다.** 수정 제안: `cands` 가 비면 「⑤ 에 수납 없음」 줄과 똑같이 `First(items_here=bool(approved_rows), first_approved_at=None, unknown=True)`. 시험 하나 추가. SPEC §6.2 표에 「⑤ 에 수납은 있으나 승인 거래 0」 줄을 한 줄 더하는 것은 planner 몫
- 운영에서 생길지: ① 이 `APPROVED` 라고 하는데 ⑤ 에 승인이 없는 것은 데이터 모순이라 드물다(Q6 취소 25/25 가 원 결제를 찾음). 하지만 생기면 아무 숫자에도 안 잡힌다

### W-2 `counts.transactions` = 받은 행 수 · `totalCount` 는 버려짐 → L2 를 확인할 수 없고, 페이지가 덜 와도 조용히 지나간다
- `back/app/service/sales.py:386` `counts.transactions = len(rows)` · `:319-330` `_pages` 가 `totalCount` 를 읽지 않음
- 근거: SPEC §9.1 #10 「`counts.transactions` = 첫 페이지 `totalCount`」 · §4.2 주석 「KOS 결제 통계 행 수(totalCount 와 같아야 함 — §9.2)」 · §9.2 L2 「`counts.transactions` = ① 첫 페이지 `totalCount` — 같음」
- 판정: 「받은 행 수」로 읽는 것 자체는 §4.2 와 맞고, 그래야 L2 가 뜻이 있다(받은 수 ↔ KOS 가 말한 수). 하지만 `totalCount` 가 응답에도 로그에도 없다. 그래서 **WP-LIVE 에서 코디가 L2 를 확인할 길이 없다**(KOS 는 back 을 거쳐서만 부른다). cursor 가 일찍 끊겨 행이 빠져도 아무 신호가 없다
- 시험도 이것을 못 잡는다: `back/tests/test_paging_cache.py:23` 주석은 「= 첫 페이지 totalCount」인데, 가짜는 `totalCount == len(rows)`(`tests/fake_kos.py:138,143`)라 두 정의를 가르지 못한다
- 수정 제안(어느 하나): (a) `counts` 에 `totalCount`(숫자만)를 더함 — 계약 변경이라 SPEC §4.2 · front `types.ts` 를 같이 고침 / (b) `len(rows) != totalCount` 이면 `log.warning("sales month=%s totalCount=%d rows=%d")`(숫자만 — §7.3 허용 「건수」) / (c) 다르면 달 전체를 오류로(OQ-114 「일부 빠진 리스트를 보이지 않음」과 같은 결). 시험: 가짜가 `totalCount` 를 행 수와 다르게 주는 사례

### W-3 ⑤ 시각이 비어도 `tx` 잇기는 유지된다 — SPEC 의 「못 이음과 같게」와 다르다(SPEC 을 고칠 쪽)
- `back/app/service/sales.py:241-243` — 후보가 하나면 `row.tx` 는 잇고 `row.at` 만 `None` · `:278` s4 는 `r.tx is first` 로 판정
- 근거: SPEC §5.4 「이은 뒤 시각 … 그 필드가 비어 있으면(스펙상 required 아님) **못 이음과 같게**」 · §6.2 s4 「이 달 ① `APPROVED` 행과 이어지면(§5.4)」
- 차이: 글자대로 보면 승인 시각이 빈 첫 승인은 「못 이음」 → s5(⑤ `createdDateTimeUtc` 달) 대체로 가야 한다. 코드는 거래 짝은 확실히 맞으니 s4 로 바로 판정한다. 화면(`at null` · 「시각 없음」 · `unmatchedTransactions` +1)은 SPEC 과 같다. s3 대체 정렬을 타므로 `firstApprovedUnknown` 에도 잡힌다
- 판정: 코드 쪽이 더 정확하다(짝을 아는데 버리지 않음). **코드는 두고 SPEC §5.4 「이은 뒤 시각」 줄을 「`at` 만 null · 잇기(§6.2 s4)는 유지」로 고치기를 권함**(planner). 이 사례를 덮는 시험은 없다(#24 는 `approved` 없이 ① `last` 도 없어 단일 후보로 이어짐 — `test_first_approval.py:91-102` 가 우연히 이 경로를 지나간다)

### W-4 방문일 — 오프셋 없는 `startDateTime` 은 UTC 로 본다(「Z 를 가정하지 않는다」와 반대)
- `back/app/domain/clock.py:39` `at if at.tzinfo else at.replace(tzinfo=UTC)` → `back/app/service/sales.py:374-375`
- 근거: SPEC §5.2 방문일 「필드 이름에 `Utc` 가 없고 스펙 설명은 『ISO 8601 date-time』뿐 — `Z` 를 가정하지 않는다」 · 스펙 `ScheduleDetailReservationContract.startDateTime`(`format: date-time`, 이름에 Utc 없음)
- 탐침: `"2026-10-03T16:30:00"`(오프셋 없음) → `visitDate 2026-10-04`. KOS 가 KST 벽시계 값을 오프셋 없이 주면, **15:00 이후 예약은 방문일이 하루 밀린다**(조용히). #16 은 `Z` · `+09:00` 두 꼴만 본다(`test_sales_rules.py:106`)
- 수정 제안: 방문일 경로에서 오프셋이 없으면 (a) `visitDate = null` 로 두고 셈 하나를 두거나 (b) WP-LIVE 에서 실물 꼴을 본 뒤 정한다. 최소한 L 목록에 「`startDateTime` 실물 꼴(오프셋 유무)」 한 줄을 더하기를 권함. ⑤ 시각(`…Utc` 이름)은 UTC 가정이 맞다

### W-5 통화가 비거나 줄이 없는 수납은 「⚠ 통화 섞임」으로 보인다
- `back/app/service/sales.py:457-458` — `currencies` 에 `None` 이 들어가거나(통화 빈 줄) 비면(줄 0) `currency = None` → `front/components/monthly/PurchaseGroup.tsx:83-86` 이 「⚠ 통화 섞임」
- 근거: SPEC §6.7 「**둘 이상 섞이면** `null`」 — 하나도 없거나 비어 있는 경우는 섞임이 아니다
- 탐침: ① 에 `REQUESTED` 행만 있는 수납 → 줄 0 · `currency null` → 머리 「⚠ 통화 섞임」(실제로는 통화 1개 · 돈 안 움직임). ① `currency` 가 빠진 행 + 품목 `KRW` → 「통화 섞임」
- 운영 영향은 작다(§6.3 `REQUESTED` · `FAILED` 운영 10월 0건 · `Money.currency` 는 required). 수정 제안: 통화를 셀 때 `None` 을 빼고, 하나도 없으면(줄 0) 「섞임」 배지 대신 합 칸을 비우거나 `—` 로 둔다. SPEC §6.7 에 「통화 0개」 줄을 더할지는 planner

### W-6 `SALES_BACK_PORT` 를 아무 데서도 안 읽는다
- `back/app/config.py:17` 정의뿐 · 실행 포트는 `README.md` 의 `--port 8800` 명령이 정한다
- 근거: SPEC §10.1 표 「`SALES_BACK_PORT` 8800 — back 포트」
- 영향: `.env` 에 다른 포트를 적어도 안 바뀐다 → front `.env.local` 과 어긋나면 「back 에 연결하지 못했어요」. 수정 제안: README 의 명령에 `--port ${SALES_BACK_PORT:-8800}` 을 쓰거나, env 표에서 「uvicorn 명령의 `--port` 와 같게 둘 것」으로 뜻을 바꾼다

### W-7 가짜 transport 가 실제 응답과 다른 자리 — 시험은 초록인데 운영에서 다를 수 있는 곳
| # | 자리 | 가짜 | 실제(스펙 · 조사) | 놓치는 것 |
|---|---|---|---|---|
| a | `tests/fake_kos.py:138,143` ① `totalCount` | 늘 `len(rows)` | 첫 페이지에만 · 전체 수 | W-2 |
| b | `tests/fake_kos.py:121` ② | 기간 무시 · 페이지 없음 | `createdDateTimeUtc` 필터 · cursor | ② −31일 범위 밖 품목 · ② 페이지 넘김(`_pages` 공용이라 코드는 같음). 범위는 요청 본문만 본다(`test_paging_cache.py:26-32`) |
| c | `tests/fake_kos.py:45` ⑤ `last` 기본값 `2026-10-01T00:00:00Z` | 모든 거래가 10월 1일 | 상태가 바뀔 때마다 바뀜(취소 · 환불 뒤 다른 달) | s5 대체(`sales.py:282`)가 `lastUpdated` 로 갈 때 10월 시험에서 우연히 맞는다(`test_sales_rules.py:136,145` p-3). NOTE-4 참조 |
| d | `trow` 대부분 `last` 없음 | ① `lastUpdatedPaymentDateTimeUtc` 없음 | 운영 ① 은 늘 줌(스펙 optional) · ⑤ 값과 같은 초인지는 **모름** | 같은 수단 · 같은 금액 둘 이상인 수납의 잇기 성공률. L12 `unmatchedTransactions` 로만 보인다 |
| e | `tests/fake_kos.py:64` 「없음」 `className` | `InvalidQueryException` | ③④ = `InvalidRequestException` · 토큰 키 없음 = `InternalServiceException` | 판정엔 영향 없음(`errorProperties` 만 봄). 화면 문구만 다름(실물 2) |
| f | ① `cost.totalAmount.value` | JSON 숫자 | int64 → proto JSON 이면 문자열일 수 있음 | 탐침: `"1000"` 도 `int()` 로 맞게 읽음 — 문제 없음 |
| g | ⑤ 승인 거래가 0 인 수납 | 사례 없음 | 데이터 모순이면 생김 | W-1 |
| h | ③ `startDateTime` | `Z` · `+09:00` 만 | 오프셋 없는 꼴일 수 있음(스펙 설명 없음) | W-4 |
| i | ③ 가짜 PII 키 | `phoneNumber` · `birthDate` | `phone` · `dateOfBirth` · `chartNumber` · `memo` | 코드는 이름 · 예약 시작 두 값만 꺼내서 결과는 같음. 다만 #20 의 「안 나옴」이 실제 키로 확인된 것은 아니다 |

---

## 고객이 실물에서 만날 자리

1. **front 를 `http://127.0.0.1:3800` 으로 열면** CORS 가 `http://localhost:3800` 하나만 허용해서(`back/app/main.py:50`) 브라우저가 막는다 → 화면은 「back 에 연결하지 못했어요(back 이 떠 있나요?)」(`front/lib/api.ts:33`). back 은 떠 있으니 문구가 사람을 헷갈리게 한다. README 에 「`localhost` 로 열 것」 한 줄을 권함
2. **키가 틀리면** 토큰 교환이 400 `InternalServiceException`(스펙 `ExchangeTokenApiKeyNotFoundError`) → 화면 「KOS 가 조회를 거절했어요 (InternalServiceException)」(`back/app/kos/client.py:60` · `sales.py:53`). 키 문제인지 알 수 없다. `errorProperties` 의 `apiKey/NotFound` 로 문구를 가르는 것은 다음 판(SPEC §4.3 에 없음)
3. 「품목은 다른 달에」인데 첫 승인 날짜가 없는 머리 — W-1(⑤ 승인 0) · ⑤ 승인 시각 없음 · ⑤ 에 수납 없음일 때. 정상 분할 결제와 구분이 안 된다
4. 같은 날 같은 수단 · 같은 금액으로 두 번 결제한 수납 — ① · ⑤ 의 「마지막 결제 상태 변경 일시」 초가 다르면 두 줄 다 「시각 없음」이고 묶음이 맨 뒤로 간다(§5.4 대로 · L12)
5. 오후 3시 이후 예약 방문일이 하루 밀릴 수 있음 — W-4(KOS 가 오프셋 없이 줄 때만)
6. 품목 배지는 지금 상태 — 안내 한 줄이 있음(§3.1 · `MonthlySales.tsx:82`). SPEC 대로
7. 「그달 결제 0」 — 취소만 있는 수납 머리(FE 보고 7번). SPEC §3.2 대로지만 0 이 눈에 띈다
8. 한 달 조회에 ③ 이 수납 수만큼 나간다(동시 8 · 15초 한도) — 수백 건이면 수십 초. 「다시 불러오기」를 짧은 사이에 많이 누르면 KOS 1분 3,000회 한도(429 → 「1분 뒤 다시」)에 닿을 수 있다(한 번 ≈ 수납 수 + 몇 회)

---

## backend 가 스스로 적은 판단 — 판정

| 판단 | 판정 | 근거 |
|---|---|---|
| `counts.transactions` = 받은 ① 행 수 | **WARN(W-2)** | §4.2 와 맞음 · §9.1 #10 글자와 다름 · `totalCount` 를 버려 L2 를 확인할 수 없음 |
| ⑤ 시각이 비면 `at` 만 null | **WARN(W-3) — SPEC 을 고칠 쪽** | §5.4 「못 이음과 같게」와 다름. 화면 · 셈은 같고 s4 만 다름 |
| ⑤ 에 수납 없으면 `firstApprovedUnknown` | **PASS** | §6.2 표 「⑤ 에 수납 없음」 그대로(`sales.py:249-250`). 이 달 승인 행이 없어도(취소만) 센다 — 많이 세는 쪽이라 안전(NOTE-5) |
| ⑤ 에 `APPROVED` 0 이면 `itemsHere=false` | **WARN(W-1)** | §6.2 「정확히 한 번」 · 「대체는 센다」와 어긋남 |
| 수납 `currency` 판정 | **PASS + WARN(W-5)** | 줄 + 승인 행 통화를 함께 보는 것은 §6.7 뜻(합을 낼 수 있나)과 맞음. `None` · 0개를 「섞임」으로 보는 것만 W-5 |
| 취소 금액 `-abs` | **PASS** | §4.2 「취소 · 반환 줄은 음수」 · §6.3. NOTE-6: 원본 부호가 뒤집혀 와도 늘 음수라 L6 「음수」 확인은 늘 통과한다 |
| `back/.gitignore` 추가 | **PASS** | `.ruff_cache/` · `.pytest_cache/` 뿐 · 루트 `.gitignore` 의 `.env` 규칙과 안 부딪침(`git check-ignore` 로 `back/.env` → 루트 1행) |
| FastAPI `include_router` 지연 포장 | **PASS** | FastAPI 0.162(`uv.lock:98`)가 라우터를 감싸는 판이라 시험 도우미가 펼침(`tests/test_privacy_app.py:61-71`). 모르는 꼴이면 `AssertionError` 로 터져 조용히 지나가지 않음. `/docs` · `/redoc` · `/openapi.json` 404 도 확인 |

## 계약 대조 — `back/app/schemas/sales.py` ↔ `front/lib/types.ts` ↔ SPEC §4.2

| 묶음 | 필드 | 결과 |
|---|---|---|
| 최상위 | `month` · `rangeUtc{from,to}` · `fetchedAt` · `cached` · `counts` · `purchases` | 같음. `from` 은 별칭 직렬화(`schemas/sales.py:9-11`) — `test_month.py:26` 이 실제 JSON 키 `"from"` 을 확인 |
| `counts` 13개 | `purchases` · `itemLines` · `paymentLines` · `reversalLines` · `transactions` · `ignoredTransactions` · `itemsMissing` · `visitorMissing` · `itemsElsewhere` · `firstApprovalCanceled` · `firstApprovedUnknown` · `unmatchedTransactions` · `atOutsideMonth` | 이름 · 개수 같음(`schemas/sales.py:15-28` ↔ `types.ts:8-22`). 월 합계 필드 없음(§1.2 · §4.2 「금액 합 필드」) |
| `purchases[]` 14개 | `purchaseId` … `lines` | 같음(`schemas/sales.py:51-65` ↔ `types.ts:44-59`) |
| `lines[]` 10개 | `kind` · `itemType` · `productName` · `productNameFrom` · `optionName` · `amount` · `currency` · `status` · `at` · `paymentType` | 같음. `paymentType` 은 품목 줄에서 키째 빠짐(`schemas/sales.py:43-48`) ↔ front `paymentType?:`(`types.ts:41`) — §4.2 「결제 · 취소 · 반환 줄에만」과 맞음 |
| null 허용 | `visitorId` · `lines[].currency` · `lines[].paymentType` | back · front 둘 다 null 허용(FE 보고와 같음). KOS 원천이 required 라 실제로 null 일 일은 거의 없다 — PASS(NOTE-7) |
| `itemType` | `PurchaseItemType_UNSPECIFIED` 포함 4값 | front 유니온 = 스펙 enum. back 은 `str` 로 받아 넘김 — 새 값이 오면 front 타입은 거짓이지만 `labels.ts:11` 이 값 그대로 보여 화면은 안전 |
| 오류 | `{error:{code,message}}` | `main.py:29-30` ↔ `api.ts:37-38`. 6개 코드 · 문구가 §4.3 표와 글자까지 같음(`sales.py:48-54` · `:299` · `:42`) |
| health | `{ok, kosConfigured}` | 같음 · 키 · 주소 값 없음(§4.1) |

## WP-REVIEW 행 — 항목별

| 볼 것 | 결과 | 근거 · 위치 |
|---|---|---|
| 경로 2 · 쓰기 0 | PASS | `api/sales.py:10,15` 둘뿐 · docs 끔(`main.py:46-47`) · POST 405 · CORS `GET` 만(`test_privacy_app.py:74-92`) · §4.1 |
| 가드 — 허용 경로 5 · `/queries/` | PASS | `kos/client.py:24-32` 상수 집합 5 · `:108` 「집합에 없거나 `/queries/` 없음」 → 네트워크 전 `GuardBlocked`. 5개 경로 = 스펙 operationId ①~⑤ 와 같음(openapi 대조). `/commands/` · `..` · 허용 밖 조회 시험(`test_guard.py:28-40`) · §7.1 · D1-05 |
| 토큰 교환 분리 · 잠금 | PASS | `client.py:22` 별도 상수 · `_token`(`:87-103`)에서만 · `asyncio.Lock` + `stale` 비교로 한 번만(`test_paging_cache.py:74-85` = 교환 2회 · 401 8개). 응답 `{token}` = 스펙 `ExchangeTokenResponse`. `follow_redirects=False`(`:75`) · §4.4 |
| 내부 API 0 | PASS | `sign-in` · `tenants/` 0(grep). `self.http` 를 직접 쓰는 곳은 `_post_raw` 하나(grep) · §7.1 |
| 「없음」 = 400 `NotFound` 만 | PASS | `sales.py:57-59` `status == 400 and has(key,"NotFound")` · ③ key `purchaseId`(`:349`) · ④ key `visitorId`(`:363`) = 스펙 `FindScheduleByPurchaseIdPurchaseIdNotFoundError` · `GetVisitorVisitorNotFoundError` 의 `const` 와 같음. 404 · 다른 reason · 다른 key → `kos_rejected`(`test_errors.py:35-56`) · §4.3 · §6.4 |
| ③④ 응답 — 이름 · 예약 시작 외 변수 · 캐시 · 로그 0 | PASS | `sales.py:352-355`(③ 두 값만 return) · `:366-367`(④ 이름만). 전체 응답은 함수 안 지역 변수로만 있다가 버려짐 · `Visitor` 는 `name` · `visit_date` 둘(`:168-171`) · 캐시엔 `SalesResponse` 만(`:185-187`) · §7.3 · NOTE 3 |
| ⑤ 응답 — 지정 필드만 | PASS | `Tx`(`sales.py:109-141`)가 `id` · `status` · `paymentType` · `price` · `paymentDateTime.{approved,canceled,spent,lastUpdated}` · `createdDateTimeUtc` · `canceledRefId` 만. `purchaseMemo` · `items` · `assignee(s)` · `*Configuration` 안 읽음. 수납 쪽은 `id` 만(`:339-340`) · §7.3 · r2 NOTE 2 |
| 캐시 · 메모리만 | PASS | `_cache` dict(`sales.py:293`) · 파일 · DB 0 · front 저장소 0(grep `localStorage`/`sessionStorage`/`indexedDB` 0) · `Cache-Control: no-store` 오류 응답까지(`main.py:52-57`) · §4.4 · §7.3 |
| 품목 줄 = 취소 안 된 첫 승인의 ① 귀속 달 한 번(s1~s5 · #22~#24) | PASS(W-1 · W-3 빼고) | s1 `:253` · s2 `:257-264`(다 빠지면 되돌림 · 부분 취소 남김) · s3 `:267-276`(한 후보라도 시각 없으면 전체 대체 정렬 · `id` 동점) · s4 `:278` · s5 `:280-283`. #22 a 3사례 · #23 · #24 2사례가 두 달을 합쳐 「한 번」을 단언(`test_first_approval.py`) · §6.2 |
| 결제일 · 정렬 = ⑤ 시각 | PASS | `at` = 이은 ⑤ 거래의 상태별 시각(`sales.py:143-144,243`) · `paidAt` = 이은 승인 중 가장 이른 것(`:464,478`) · 묶음 정렬 `(시각 없음, 시각, 수납 id)`(`:421-426`) · 줄 정렬(`:453`). front 도 같은 규칙으로 다시 정렬(`format.ts:17-47`) · §3.3 · §5.4 |
| ① `lastUpdatedPaymentDateTimeUtc` 응답 · 화면 0 | PASS | `Row.last_updated` 는 `link_rows` 동점 가르기(`:237-238`)에만 · 응답 모델에 그 자리 없음 · #21 이 값 부재를 단언(`test_sales_rules.py:150`) · R§2 ⑤ 줄 |
| 동점 가르기 = 파싱 · 초 단위 | PASS | `_same_second`(`sales.py:225-226`) — 파싱한 aware 시각 · 마이크로초 버림 · `Z`/`+00:00`/소수점 표기 차이 시험(`test_sales_rules.py:133-144`) · r2 NOTE 1 |
| 응답 키 = §4.2 | PASS | 위 계약 대조 |
| 자유 텍스트 0 | PASS | `…FunnelDetail` · `reservationFunnel*` · `purchaseMemo` · `memo` · `visitorRequest` · `orderMemo` 를 읽는 코드 0(grep · back/app · front). 유입은 `visitorFunnelName` 하나(`sales.py:104`). KOS 오류의 `message` 도 안 읽음(`client.py:54-66` = `className` · `errorProperties.{key,reason}` 만) · §6.6 · [[no-inference-from-free-text]] |
| 로그에 이름 · 금액 · id · 키 0 | PASS | 로그 4곳뿐: `sales.py:312`(달 · 오류 이름/상태) · `:315`(달 · `counts` 숫자 · 초) · `client.py:102,115`(고정 문구). `httpx` · `httpcore` WARNING(`main.py:25-26`). #14 가 정상 · 오류 두 경로에서 이름 · 금액 · 수납 id · 손님 id · 키 · 토큰 · 상품명 0 을 단언 · §7.3 |
| `127.0.0.1` | PASS(NOTE-1) | README 실행 명령 `--host 127.0.0.1`(uvicorn 기본도 127.0.0.1) · D1-09 · §7.3 |
| `.env` 미추적 | PASS | `back/.env` · `front/.env.local` 없음 · `git check-ignore` = 루트 `.gitignore:1` · `front/.gitignore:8` · `.env.example` 둘은 이름만(키 값 없음) · §7.2 |
| cc-prototype import 0 | PASS | `cc-prototype` 문자열 = 「원본:」 주석만(back 3 · front 11) · 상대 경로 `../../` 0 · front 의존성에 cc-prototype 패키지 없음 · D1-08 · §8 |
| 비밀값 · 하드코딩 주소 | PASS | KOS 호스트 · 키는 env 로만(`config.py:15-16`) · front 주소는 `NEXT_PUBLIC_API_BASE_URL` 로만(`api.ts:7`) · 시험 값은 `kos.example.invalid` · `fake-key-zzz` |
| 부록 A — D-01~D-09 | PASS | 월 선택 · 기본 이번 달(D-01 `page.tsx:8`) · 수납 묶음 · 품목 한 줄(D-02) · 칸 10개 · 이름 안 가림(D-03 `SalesTable.tsx:6`) · `visitorFunnelName`(D-04) · 조회만(D-05) · KST 귀속 · 취소 음수(D-06) · 선불카드 · 기타 안 뺌 · 상품명 대체(D-07 `sales.py:157-160`) · 별도 레포 · 복사(D-08) · 로컬(D-09) |

---

## 참고(NOTE — 고치지 않아도 됨)

- **NOTE-1** front `next dev -p 3800`(`front/package.json:6`)은 모든 인터페이스에 뜬다. front 는 데이터를 들고 있지 않고, 다른 기기 브라우저는 자기 `localhost:8800` 을 부르니 새는 길은 없다. 맞추려면 `-H 127.0.0.1`(D1-09)
- **NOTE-2** back 이 `127.0.0.1` 에만 뜨는 것은 실행 명령에만 달려 있다(코드에서 강제하지 않음). SPEC §7.3 이 명령으로 정했으니 PASS
- **NOTE-3** KOS 쪽 오류가 아닌 예외(예: 잘못된 `KOS_OPEN_API_BASE` → `httpx.InvalidURL`)는 `HTTPError` 가 아니라서(`client.py:84`) 처리기 없는 500 이 된다 → front 「요청을 처리하지 못했어요」. 값이 새지는 않음
- **NOTE-4** s5 대체가 ⑤ `createdDateTimeUtc`(deprecated · optional)가 없으면 `lastUpdatedDateTimeUtc` 로 간다(`sales.py:282`). 이 값은 나중 취소 · 환불 때 바뀌므로, 그 경우 품목이 0번 나올 수 있다. SPEC §6.2 s5 · OQ-121 이 고른 대체이고 `firstApprovedUnknown` 으로 드러나니 SPEC 대로. L11 이 0 이 아니면 이것부터 볼 것
- **NOTE-5** ⑤ 에 수납이 없으면 이 달 승인 행이 없어도(취소만) `firstApprovedUnknown` 을 센다(`sales.py:249-250`). SPEC 표 문장으로는 승인 행이 있을 때만 세는 것으로도 읽힌다. 많이 세는 쪽이라 둠
- **NOTE-6** 취소 · 반환 `-abs`(`sales.py:449`) 때문에 L6 「음수」 확인은 늘 통과한다. 원 부호를 보려면 WP-LIVE 에서 ① 원본 부호를 따로 봐야 한다(Q6 은 25/25 음수)
- **NOTE-7** `_money` 는 통화 · 값이 없으면 0 · `None` 으로 채운다(`sales.py:63-72`). 스펙상 required 라 운영에서는 생기지 않을 자리. 생기면 W-5 로 보인다
- **NOTE-8** ② 기간 끝 = 달 끝(`sales.py:404-405`). 지난 달을 볼 때 그 달이 끝난 뒤 수납에 덧붙인 품목(`process = PENDING` 등)은 어느 달에도 안 나온다. `⚠ 결제 ≠ 품목` 이 잡을 수 있다(§6.4 · OQ-116 범위 안)
- **NOTE-9** `tools.md` 는 「테스트 실행 금지」인데 이 브리프 §6.1 은 허용 → 브리프대로 pytest · ruff · tsc 만 돌렸다(파일 안 바꿈 · `PYTHONDONTWRITEBYTECODE=1` 로 탐침)

## 수정 발주 제안(코디 판단)

1. **WP-LIVE 전**: W-1(⑤ 승인 0 → 「⑤ 에 수납 없음」과 같게 · 시험 1) · W-2(`totalCount` ↔ 받은 행 수를 비교해 숫자를 드러냄 · 가짜가 다른 `totalCount` 를 주는 시험 1)
2. **WP-LIVE 에서 볼 것 더하기**: W-4 `startDateTime` 실물 꼴 · W-7 d ① · ⑤ `lastUpdated` 가 같은 초인지(L12 와 함께)
3. **SPEC(planner)**: W-3 §5.4 「이은 뒤 시각」 줄 · W-1 §6.2 표 한 줄 · W-5 §6.7 「통화 0개」 · W-6 `SALES_BACK_PORT` 뜻
4. 나머지 W-5 · W-6 · 실물 1 · 2 는 WP-LIVE 뒤 한 번에 모아도 된다
