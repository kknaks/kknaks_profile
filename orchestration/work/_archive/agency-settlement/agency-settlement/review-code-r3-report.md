# 리뷰 리포트 — agency-settlement / code r3 — BE3 · FE3 ↔ SPEC-001 0.4.2 (2026-10-29)

대상: 워크트리 `agency-settlement`(커밋 전 · `back/**` · `front/**` · `README.md`) · 기준 SPEC-001 **0.4.2** · DEC-001 D-18 · WORK 3판 WP-REVIEW3 행 · `review-doc-r6-report.md` §3 「구현 때 지킬 것」 1 ~ 10 · `wp-fe3-report.md` · backend 판단 (1) ~ (5) · 코디 실물(숫자)
read-only. 이 파일 하나만 썼다. 코드 · `back/.env` · 8800 · 3800 무접촉 · 운영 KOS 호출 0. `back/data/sales.sqlite3` 는 `mode=ro` 로 **수납 끝 4자리 Ⓐ 한 건의 숫자 · 상태 · 시각만** 읽었다(이름 · 상품명 · 전체 id 안 봄 · 리포트에 안 실음).

## 판정: FAIL

FAIL 1 · WARN 2 · NOTE 9. 코드는 0.4.2 를 글자대로 구현했다(r6 「구현 때 지킬 것」 10 개 전부 지켜짐 · 시험 144 초록). FAIL 은 **SPEC 규칙 둘(§6.9 「품목이 다른 달인 수납은 이 달 승인을 더하지 않는다」 + §4.4 품목 달 고정)이 겹치는 자리에서 D-18 이 깨지는 돈 구멍**이다: 확정 달이 품목을 가진 수납이 다음 달에 「전액 취소 → 다른 금액 재승인」되면 **재승인 금액이 어느 달 실결제에도 안 들어간다**. 가짜 KOS 로 재현했다(아래 F-1). 고칠 곳은 SPEC §6.9 판정 한 줄 + `settle()` 한 곳이다(r6 W-5 「OQ-132 답이 바뀌면 고칠 곳 = §6.9 하나」 그대로).

코디가 물은 **9월 ⚠ 1 수납(Ⓐ)은 버그가 아니다** — SPEC 상 정상 꼴(§6.4 「달을 넘는 돈」)이다(§2).

### 돌린 것

| 무엇 | 결과 |
|---|---|
| `cd back && uv run --frozen --no-sync pytest -q -p no:cacheprovider` | **144 passed**(2.93s) |
| `ruff check --no-cache .` | All checks passed |
| `cd front && npx tsc --noEmit --incremental false` · `npx eslint .` | 0 · 0 |
| `npm run build` | 안 돌림 — 3800 dev 와 `.next/` 공유(r2 와 같은 이유) |
| 옛 필드 grep(back app · front app/components/lib): `approvedTotal` · `paymentLines` · `reversalLines` · `paymentType` 줄 필드 · `kind` 의 `payment`/`cancel`/`spent` · `refresh=1` · 브라우저 저장소 | **0** · `schemas/sales.py:72` `kind: Literal["item"]` |
| back `schemas` ↔ front `types.ts` 필드 대조(스크립트) | `Counts` 18 · `StoreInfo` 4 · `FetchInfo` 7 · `AgencyTotal` 4 · `Line` 9 · `Purchase` 20 · `SalesResponse` 10 — **전부 같음** |
| 탐침 시험(scratchpad · 레포 밖 · 가짜 KOS · 임시 DB) | F-1 재현 |

---

## FAIL

### F-1 확정 달이 품목을 가진 수납이 다음 달에 「전액 취소 → 다른 금액 재승인」 → 재승인 금액이 사라진다(두 달 합 ≠ KOS 최종)

- 코드: `back/app/service/sales.py:652-665` `settle()` — `itemsHere = false` 면 `net = −Σ(반영 안 된 취소)` 만 · 이 달 승인은 더하지 않음 · `back/app/repository/store.py:264-270` `_pin` — 앞 달이 `items_here = 1` 이면 이 달은 `items_here = false` · `pinned_elsewhere`
- SPEC: §6.9 `:649` 「품목이 다른 달인 수납 = 이 달 … 취소 합 — **이 달 승인(분할 결제 나머지 · 재결제)은 더하지 않는다**(그 돈은 품목 달의 품목 금액에 이미 있다)」 · §4.4 품목 달 고정 · §4.6 ② 「앞 달 수납의 첫 승인이 바뀜 → 다음 달은 … `itemsPinnedElsewhere`」. 「그 돈은 품목 달에 이미 있다」는 **분할 결제**에서는 맞지만, **고정(pinned) 수납의 재승인**에서는 틀리다 — 품목 달은 받은 때 금액(취소 전 X)이고 재승인 Y 는 그 뒤에 생긴 돈이다
- 재현(가짜 값 · `scratchpad/probe/test_probe_r3.py`):
  1. 10-05 에 9월을 받음: 수납 P 승인 500,000 · 품목 500,000 → 9월 `closed` · 실결제 500,000
  2. 10월: 10-20 P 전액 취소(−500,000) · 10-21 다른 금액 재승인 300,000 → KOS 최종 = **300,000**
  3. 10월 받기 결과: P `itemsHere false`(9월에 고정 · `itemsPinnedElsewhere 1`) · 실결제 **−500,000** · `paymentsNet −200,000` · 줄 0 · 숨김 아님
  4. **9월 500,000 + 10월 −500,000 = 0 ≠ 300,000**. ⚠ 도 없다(9월은 결제 = 품목 · 10월은 `itemsHere false` 라 ⚠ 비교 안 함). 드러나는 것은 응답 `counts.itemsPinnedElsewhere` 숫자뿐(화면 건수 줄에 안 보임)
- 어기는 것: **D-18**(「손님이 최종적으로 얼마 냈나 · 수수료 · 엑셀 기준은 품목 실결제」) · §6.9 머리 「어느 순서로 받아도 달을 모두 더하면 최종 금액」(`:660`) — SSOT 로 DEC 가 SPEC 을 이긴다. 에이전시 실결제 합 · 엑셀 「품목 금액」 합도 같이 300,000 이 빠진다(수수료 기준 금액이 빠짐)
- 실물에서 생길지: 생긴다. 코디가 본 Ⓐ 가 바로 「전액 취소 → 다른 금액 재승인」 꼴이다(8월 승인 → 9월 1일 취소 · 재승인). 그때는 8월이 저장 안 돼 있어 9월이 품목을 가졌고 맞게 나왔다. 같은 일이 **9월(확정 · 저장됨) 수납에 10월 이후** 생기면 F-1 이 된다. 지금 9월은 10-29 에 확정 저장돼 있으므로 10-29 ~ 이후 9월 수납의 「취소 후 다른 금액 재결제」 전부가 대상
- [전체 다시 받기] 로 낫나: §4.6 ② 순서(9월 전체 → 10월 전체)면 낫는다. 9월 전체만 누르면 10월이 `itemsNowhere` 인데 실결제는 여전히 −500,000(취소만 · 품목 달 없음 → 반영 안 됨) — 중간 상태도 틀린 숫자다. 사람이 `itemsPinnedElsewhere` 를 보고 두 번 누르라는 안내는 화면에 없다
- 고칠 것(planner → backend · 하나):
  - (a) **권함** — §6.9 에 「`pinned_elsewhere` 수납(품목 달이 고정된 다른 달 · 이 달 판정은 품목이 여기)의 실결제 = 이 달 `paymentsNet`(승인 + 반영 안 된 취소 · 음수)」 한 줄. 위 재현에서 9월 500,000 + 10월(300,000 − 500,000) = 300,000 ✓. 분할 결제 나머지(이 달 판정도 `items_here false` · `pinned_elsewhere false`)는 지금대로 0. 코드 `settle()` 한 곳(`sales.py:665`)에 `j.pinned_elsewhere` 갈래 + 엑셀 「앞 달 결제 취소」 행 조건(`export.py` `not p.itemsHere and p.netTotal`)은 그대로 맞음(음수 · 양수 모두 행). 머리 문구는 「품목은 다른 달에 · 첫 승인이 바뀜」 쪽이 맞다
  - (b) 고정을 풀어 이 달이 품목을 다시 받게 함(OQ-128 대안 — 확정 달 판정을 건드려 D-12 와 부딪침 · 권하지 않음)
  - 시험: 위 재현 꼴 그대로 「9월 저장 → 10월 전액 취소 + 다른 금액 재승인 → 두 달 실결제 합 = 재승인 금액 · 에이전시 합 · 엑셀 합 같음」 + 같은 금액 재승인 · 부분 취소 뒤 재승인

---

## WARN

### W-1 「앞 달 결제 취소」 머리의 결제일이 화면엔 「— 시각 없음」 · 엑셀엔 취소 시각 · 묶음 차례도 화면 ≠ 엑셀 (backend 판단 (3))

- back: 응답 `paidAt = iso(j.paid_at)`(`sales.py:708`) — 이 달 승인이 없는 수납(앞 달 결제의 이 달 취소만)은 `null`. 정렬은 `sort_at = paid_at or 첫 취소 시각`(`:677` · `:719`) · 엑셀 행 결제일 = `prior_cancel_at`(`export.py` 「앞 달 결제 취소」 행)
- front: `headAt = p.paidAt` 뿐(`front/components/monthly/format.ts` `headAt` 주석 「없으면 첫 취소 시각 — back 이 정함」 — back 은 안 정함) · `sortPurchases` 가 `paidAt` 으로 다시 정렬 → 그 묶음은 **「— 시각 없음」 + 맨 뒤**. 0.4.0 부터 줄에 시각이 없어 front 는 취소 시각을 알 길이 없다
- SPEC 이 둘로 갈림: §3.2 결제일 칸 `:166` 「살아 있는 승인이 없으면 그달 첫 승인 · **그것도 없으면 첫 취소 · 반환 시각**」 · §4.2 `paidAt` 주석 「… 없으면 그달 첫 승인 · **없으면 null**」. back 은 §4.2, front 는 §3.2 를 믿었다
- 결과: 화면은 시각 없음 · 맨 뒤, 엑셀(§3.6 「정렬 · 묶음 차례 = 화면」)은 취소 시각 · 시각 차례 → 화면과 엑셀 차례가 다르다. 금액은 같다
- 고칠 것: planner 가 §4.2 `paidAt` 을 §3.2 대로(「없으면 첫 취소 · 반환 시각」) 고치고 backend 가 `paidAt` 에 `sort_at` 값을 싣는다(한 줄). 또는 `headAt` 필드를 따로. front 는 그대로 맞게 된다

### W-2 반영 판정의 「품목을 받은 시각」 = 받기 **시작** 시각 — ② 를 부르기 전에 처리된 환불이 두 번 빠지는 창 (backend 판단 (2))

- `store.py:274-277` `item_fetched = min(items.fetched_at)` · `items.fetched_at = started`(`write_full` · `write_incremental` 의 받기 시작 시각 — ① 부르기 직전 · `sales.py:427` · `:449`) · 판정 `sales.py:654-656` `at < item_fetched → 반영됨`
- 길: 9월 [전체 다시 받기] 가 `started` 에 시작 → ① · ⑤ 를 부르는 수 초 ~ 수십 초 사이에 10월 날짜로 9월 수납 환불이 처리됨 → 그 뒤 부른 ② 의 `cost` 는 **이미 환불 뒤 남은 금액** · 그런데 그 취소 시각 ≥ `started` 라 「반영 안 됨」 → 10월에 음수로 또 빠진다(두 번 차감). 반대로 KOS 시계(취소 `canceledDateTimeUtc`)와 back 시계(`started`)의 어긋남도 같은 창에 든다
- 창은 전체 받기 한 번의 길이(② 는 ① · ⑤ 뒤 · ③ 앞)라 드물다. 다만 돈 경로이고 시험(#61 ~ #63)은 시계를 고정해 이 창을 못 본다
- 고칠 것(backend · SPEC 한 단어): `items.fetched_at` 을 **② 응답을 받은 직후 시계**로 쓴다(받기 시작 시각은 `months.fetched_at` 에 그대로). 남는 창은 ② 호출 하나(보통 1초 안). SPEC §6.9 반영 판정 「`items` 를 받은 시각」 = 「② 를 받은 시각」으로 한 단어

---

## 1. SPEC 0.4.2 · r6 「구현 때 지킬 것」 대조

| # | 항목 | 코드 | 판정 |
|---|---|---|---|
| r6-1 | schema 1→2 채우기 = 달 잠금 + 쓰기 잠금 + 한 트랜잭션 · 채운 뒤 다시 읽음 | `sales.py:325-326` · `:341-342` · `:346-352` · `store.py:281-295` | 맞음 |
| r6-2 | `netTotal` · 앞 달 결제 취소 · 숨김 · `excludedItems` 판정 = 함수 하나 · 응답 · 엑셀 · 에이전시가 그 결과만 | `settle()` `sales.py:634-677` · `View.settled` · `export.py` 「view.settled 그대로」 | 맞음 |
| r6-3 | 증분 ② 갈아 끼우기 = 이 달 `items_here` + 새 행 · 다른 달 · pinned 제외 | `sales.py:478-485` · `store.py:418-423`(고정 뒤 `items_here` 다시 확인) | 맞음 · r2 W-2(옛 `itemsMissing` 도 ② 후보 — `:481`)도 닫힘 |
| r6-4 | 살아 있는 승인 저장값 = 그 달 받기 · 그 달 증분(새 행 수납)에서만 | `sales.py:438` · `:476` · `live_approval` `:566-586` | 맞음(#59) |
| r6-5 | 「앞 달 결제 취소」 글자 두 표 · 글자 셀 | `labels.py` `PRIOR_CANCEL` · `labels.ts:24-29` · `_text` | 맞음(#39 두 표 같음 초록) |
| r6-6 | 숨긴 수납 수 = 월별만 | `SummaryLine.tsx` `monthCounts` 만 `hiddenPurchases` · `countLines` 에 없음 · 엑셀 「정보」 `view_kind == "monthly"` 일 때만 | 맞음 |
| r6-7 | `⚠ 통화 섞임` = `netTotal === null` | `PurchaseGroup.tsx` `mixed = p.netTotal === null` | 맞음 |
| r6-8 | 옛 필드 grep 0 | 위 표 | 맞음 |
| r6-9 | 반영 판정 시각 비교 = 파싱한 시각 | `sales.py:654-655`(`datetime` 끼리) · `store.py` `parse(...)` | 맞음(시각 기준점은 W-2) |
| r6-10 | 로그에 `netTotal` · `paymentsNet` 값 0 | 로그 = 달 · mode · 숫자 · `counts`(금액 칸 없음) · `itemsRefetched` · `filledLiveApprovals` 수 | 맞음 |
| §6.9 | 줄 = `ACCEPTED` · `PAID` · `PARTIALLY_REFUNDED` 만 · `REFUNDED` → `refundedItems` · 그 밖 → `excludedItems` | `sales.py:590` · `:640-643` | 맞음 |
| §6.9 | 숨김 = 줄 0 · 실결제 0 · `itemsMissing` 아님 | `sales.py:675`(+ `itemsNowhere` 도 안 숨김 — 판단 (1)) | 맞음 · NOTE-1 |
| §6.9 | 반영 판정(`at_utc` · 없으면 행 `fetched_at` · 품목 달 없음/품목 없음 → 반영 안 됨) | `sales.py:652-658` · `store.py:272-277` | 맞음(#61 ~ #63) · W-2 |
| §6.4 | ⚠ = `itemsHere` · `paymentsNet ≠ itemsTotal` | `PurchaseGroup.tsx` `mismatch` | 맞음 |
| §3.3 | 0원 줄 = 앞 유료 줄 바로 아래 · 앞 유료 없으면 첫 유료 아래 | back `order_zero_lines` `sales.py:615-631` · front `sortLines`(`format.ts`) — 같은 결과 | 맞음 |
| §6.8 | 손님 · 결제 손님 = 숨긴 수납 포함 · `purchases` · `netTotal` = 보이는 수납 | `_agencies` `sales.py:766-781` | 맞음 |
| §4.7 | 엑셀 행 = 품목 줄 + 「앞 달 결제 취소」 행 · 「품목 금액」 합 = 실결제 합 · 「정보」 수 | `export.py` `build_xlsx` | 맞음(#57) · NOTE-4 · NOTE-5 |
| §3.5 | 숨긴 수납만 있는 에이전시 탭 = 빈 탭 문구(손님 n · 결제 손님 m) | `SalesScreen.tsx:141-147` | 맞음 |
| 확정 달 | 증분 (ii) 가 다른 달 · `closed` 달 `items` 를 건드리지 않음 · schema 채우기 KOS 0 | `store.py:418-423` · `fill_live` | 맞음 |

**r2 지적**: F-1(달 옮길 때 `refresh=full` 잔류) → `page.tsx:11` · `agency/page.tsx:12` `key={month}` 로 **닫힘** · W-2(증분 ② 범위) → 닫힘 · W-3(access log 쿼리) → `main.py:30-49` `DropQueryString` · README `:49` **닫힘** · W-1(「바뀜」 SPEC 줄) → SPEC 0.4.2 에 아직 없음(NOTE-8).

## 2. 코디 실물 — 9월 ⚠ 1 수납(끝 4자리 Ⓐ) 판정: **정상(SPEC 꼴) · 버그 아님**

저장본 숫자(`mode=ro`):

| 표 | 값 |
|---|---|
| ⑤ 거래 | 승인 〈금액7〉(카드 · **8월 26일**) · 취소 −〈금액7〉(카드 · 9월 1일 · `canceledRefId` = 그 8월 승인) · 승인 〈금액5〉(카드 · 9월 1일) |
| 9월 ① 행 | 취소 −〈금액7〉 · 승인 〈금액5〉 — 9월 `paymentsNet` = **−〈금액6〉** ✓ |
| 9월 판정 | `items_here 1` · `canceled_skipped 1`(8월 승인이 전액 취소돼 첫 승인 후보에서 빠짐 — §6.2 s2) · 첫 승인 = 9월 1일 〈금액5〉 |
| 품목 | 1개 · `PARTIALLY_REFUNDED` · 〈금액5〉 |
| 8월 | 저장 없음 |

- 이것은 「승인 X → 전액 취소 → **다른 금액** Y 재승인」(§6.9 `:649` 예 「품목 합 Y → Y」)이 **달을 넘은** 꼴이다. 9월 실결제 = 품목 〈금액5〉 = KOS 최종 ✓. 8월을 나중에 받아도 8월은 `items_here false`(첫 승인이 9월) · 8월 취소 행 0 → 실결제 0 · 숨김 → **두 달 합 〈금액5〉 ✓**
- ⚠ 는 `paymentsNet`(−〈금액6〉)에 **8월 승인의 9월 취소**가 들어가서 뜬다 — §6.4 「정상인데도 뜰 수 있는 자리 = 달을 넘는 돈」 그대로. 품목 상태가 `PARTIALLY_REFUNDED` 인 것은 KOS 가 수납 단위 취소를 품목 상태에 그렇게 적은 것(코드는 받은 값 그대로)
- 배지를 줄이려면(OQ-106 · planner): ⚠ 비교에서 「`canceledRefId` 가 다른 달 승인을 가리키는 취소」를 빼는 안 — 이 수납은 〈금액5〉 = 〈금액5〉 으로 ⚠ 가 꺼진다. 돈 · 합에는 영향 없음
- 단 **같은 꼴이 8월이 저장된 상태에서** 생겼다면 F-1 이 된다(그래서 FAIL 로 올림)

## 3. backend 판단 (1) ~ (5) — 판정

| # | 판단 | 판정 |
|---|---|---|
| (1) | `itemsNowhere` 는 실결제 0 · 줄 0 이어도 안 숨김 | **받아들임** — `itemsMissing` 과 같은 「빠뜨리지 않고 드러냄」 · SPEC §3.2 `itemsNowhere` 줄과 맞음. §6.9 숨김 줄에 「`itemsNowhere` 도 숨기지 않는다」 한마디(NOTE-1) |
| (2) | 반영 판정은 시계 순서에 기댐 | **WARN W-2** — 기준점을 ② 받은 시각으로 |
| (3) | 묶음 정렬 = 저장 `paid_at` · 없으면 이 달 첫 취소 — front 와 다를 수 있음 | **WARN W-1** — SPEC §3.2 ↔ §4.2 갈림 · `paidAt` 에 실으면 끝 |
| (4) | 엑셀 「정보」 시트에 실결제 합 한 줄 | **맞음** — §4.7 「정보」 줄이 「실결제 합(= 「품목 금액」 열 합)」을 적고 있다. 같은 줄 끝 「(금액 합 없음)」은 옛 글이 남은 것(NOTE-3) |
| (5) | schema 1→2 | **맞음** — §4.4 예외대로 `ADD COLUMN` 둘 · `BEGIN IMMEDIATE` · 판 2 밖은 여전히 뜨지 않음(`store.py:146-156`) · 채우기는 읽을 때 한 번(§4.6 ⑨) |

---

## 사용자가 실물에서 만날 자리

1. **9월에 결제했던 손님이 10월에 취소하고 다른 금액으로 다시 결제** → 9월 · 10월 · 에이전시 실결제 합 · 엑셀 합에서 그 재결제 금액이 빠짐(10월 머리는 「앞 달 결제 취소」 음수만 · ⚠ 없음) — F-1
2. 「앞 달 결제 취소」 묶음의 결제일이 「— 시각 없음」이고 표 맨 뒤 · 같은 화면 엑셀에서는 취소 날짜가 찍히고 중간에 있음 — W-1
3. 9월 ⚠ 1 건(Ⓐ) — 실결제는 맞음 · 달을 넘는 취소 때문에 뜨는 배지(§2)
4. 앞 달 [전체 다시 받기] 를 누르는 수십 초 사이 그 달 수납이 환불되면 다음 달에 그 환불이 한 번 더 빠질 수 있음 — W-2(드묾)

## 참고 (NOTE)

- **NOTE-1** `sales.py:675` — `itemsNowhere` 수납은 안 숨김(판단 (1)). SPEC §6.9 숨김 줄에 명시
- **NOTE-2** `back/data/sales.sqlite3.bak-schema1`(600 · 14:27 · 2.1MB) — schema 1 사본이 **두 번째 운영 개인정보 파일**로 남아 있다. `back/data/` 라 gitignore 는 됨. SPEC §7.3 「저장은 `SALES_DB_PATH` 파일 하나뿐 · 필요 없어지면 지운다」 — LIVE3 끝나면 지울 것(코디)
- **NOTE-3** SPEC §4.7 「정보」 줄 `:443` 이 「실결제 합」을 적고 끝에 「(금액 합 없음)」이 남아 있다 — planner 가 끝 괄호를 지움
- **NOTE-4** `export.py` 「앞 달 결제 취소」 행 조건 `not p.itemsHere and p.netTotal` — 통화가 섞여 `netTotal = null` 이면 행이 없다(화면은 ⚠ 통화 섞임으로 보임). 운영 전부 KRW 라 해 없음
- **NOTE-5** `itemsNowhere` 수납(실결제 0)은 화면엔 묶음이 있고 엑셀엔 행이 없다(품목 · 취소 행 둘 다 없음) — 「행 = 화면 줄」 뜻으로는 맞음(줄 0)
- **NOTE-6** front `isHidden`(`format.ts`)이 back 숨김을 한 번 더 거름 — `itemsNowhere` 조건이 없어 back 이 보낸 `itemsNowhere` · 실결제 0 수납을 front 가 숨긴다. back (1) 판단과 어긋남 → `&& !p.itemsNowhere` 한 조각(front). 운영 `itemsNowhere` 0 이면 안 보임
- **NOTE-7** 「앞 달 결제 취소」 머리의 `sort_at` 은 반영된 취소까지 포함한 첫 취소 시각(`sales.py:669` · `:677`), 엑셀 행 결제일은 **반영 안 된** 첫 취소 시각 — 둘이 다를 수 있다. W-1 을 고칠 때 하나로
- **NOTE-8** r2 W-1(증분 「바뀜」 = 그 수납 이 달 ① 행 갈아 끼움)이 SPEC 0.4.2 §4.5 증분 2 · §4.6 ⑦ 에 아직 없다 — 코드 · 시험(#27g)만 있음
- **NOTE-9** 탐침 시험 `scratchpad/probe/test_probe_r3.py` 는 레포 밖 · F-1 시험의 꼴로 그대로 옮겨 쓸 수 있다

## 고칠 것 — 모아서

| # | 누가 | 무엇 |
|---|---|---|
| F-1 | planner → backend | §6.9 「`pinned_elsewhere` 수납 실결제 = 이 달 `paymentsNet`(반영 판정 적용)」 · `settle()` 갈래 하나 · 시험(9월 저장 → 10월 전액 취소 + 다른 금액 재승인 → 두 달 합 = 재승인 · 에이전시 · 엑셀 합 같음) |
| W-1 | planner → backend | §4.2 `paidAt` = 「없으면 첫 취소 · 반환 시각」(§3.2 와 같게) · back `paidAt` 에 `sort_at` |
| W-2 | backend (+ SPEC 한 단어) | `items.fetched_at` = ② 응답 받은 직후 시각 |
| NOTE-6 | frontend | `isHidden` 에 `!p.itemsNowhere` |
| NOTE-1 · 3 · 8 | planner | SPEC 글 세 군데 |
| NOTE-2 | 코디 | `back/data/sales.sqlite3.bak-schema1` 지우기(LIVE3 뒤) |
