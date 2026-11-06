# WP-FE3 결과 보고 — SPEC-001 0.4.2 (D-18 최종 결제만) · 2026-10-29

## 상태: done · 커밋 안 함 · `back/` · README · 3800/8800 · `back/.env` · `back/data/` 무접촉 · `npm run build` 안 돌림(지시 — `.next` 공유)

## 변경 파일 (`front/` 만)

| 파일 | 무엇 |
|---|---|
| `lib/types.ts` | §4.2 0.4.2 — `LineKind = 'item'` · `lines[].paymentType` 지움 · 수납 `netTotal` · `paymentsNet` · `canceledPayments` · `refundedItems`(`approvedTotal` 지움) · counts `canceledPayments` · `refundedItems` · `hiddenPurchases` · `reflectedCancels` · `excludedItems`(`paymentLines` · `reversalLines` 지움) · 에이전시 `netTotal` |
| `lib/labels.ts` | `ITEM_STATUS` = `결제 완료`(ACCEPTED · PAID) · `부분 환불` · `환불` · `미수납` · `LINE_STATUS = { PRIOR_CANCEL: '취소' }` · `LINE_KIND_TEXT = { PRIOR_CANCEL: '앞 달 결제 취소' }`(옛 payment/cancel/spent · `lineText` 지움) · `statusLabel(status)` · `statusVariant(status)` |
| `components/monthly/format.ts` | `headAt = paidAt` · `isHidden`(실결제 0 · 줄 0 · itemsMissing 아님) · `sortLines` = §3.3(0원 줄 → 앞 유료 줄 바로 아래 · 앞에 유료 없으면 첫 유료 줄 아래 · 유료 0 이면 그대로) |
| `components/monthly/PurchaseGroup.tsx` | 품목 줄만(결제 · 취소 · 반환 줄 그리기 지움) · 머리 「실결제」 `netTotal`(음수 빨강) · 「취소 a · 환불 b」 회색 · 「앞 달 결제 취소 · 품목은 다른 달에 · 첫 승인 MM-DD」(빨강) · `⚠ 통화 섞임` = `netTotal === null` · `⚠ 결제 ≠ 품목` = `paymentsNet ≠ itemsTotal`(품목 줄 있는 묶음) |
| `components/monthly/SalesTable.tsx` | 머리 칸 「그달 결제」 → 「실결제」 · 줄 칸 「일시」 비움(품목 줄엔 시각 없음) · 숨김 묶음 거름 |
| `components/monthly/SummaryLine.tsx` | 칩 수납 · 품목 + 회색 「취소된 결제 a건 · 전액 환불 품목 b개 · 숨긴 수납 h(월별만) · 앞 달 품목에 반영된 취소 r(>0) · 뺀 품목 x(>0) · 제외 n(>0)」 · 에이전트별 칩 「실결제 합」 · 에이전시별 칩에 「실결제」 · 안내 문구 0.4.0 |
| `components/monthly/SalesScreen.tsx` | 월별 = 달 `counts` · 에이전트별 = 걸러진 `purchases[]` 로 셈(숨긴 수 없음) · 빈 에이전시 탭 문구 「이 달 보일 결제가 없어요 — 손님 n명 · 결제 손님 m명(취소 · 환불 · 다른 달 품목만)」 |

## 검증

- `npx tsc --noEmit` 통과 · `npm run lint` exit 0 · build 안 함
- 옛 필드 grep(`front/app components lib`): `approvedTotal` 0 · `paymentLines` 0 · `reversalLines` 0 · `paymentType`(단수 필드) 0 · `'payment'`/`'cancel'`/`'spent'` 0 · `refresh=1` 0 · `localStorage`/`sessionStorage` 0 · 「지금 기준」 0
- **#39 두 표**: front `labels.ts` ↔ back `labels.py`(BE3 가 지금 둔 것)를 같은 정규식으로 대조 — `ITEM_TYPE` · `ITEM_STATUS` · `LINE_STATUS` · `LINE_KIND_TEXT` · `PAYMENT_TYPE` **5개 모두 같음**(파이썬으로 비교 · back 은 읽기만)
- 스크린샷: front 를 scratchpad 로 복사해 `next dev -p 3892`(`NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8892`) + 가짜 back 8892(0.4.2 꼴 · 가명 · 에이전시A/B/C) · 1600×1000 · 8800 요청 playwright 차단(막힌 것 0) · 페이지 오류 0 · 끝나고 3892/8892 내리고 복사본 지움

## 스크린샷 — `shots-fe3/`

| 파일 | 확인한 값 |
|---|---|
| `monthly.png` | 10월 묶음 9 · 결제·취소 줄 0 · `환불` 배지 0 · 건수 「수납 9건 · 품목 14줄 / 취소된 결제 5건 · 전액 환불 품목 1개 · 숨긴 수납 2 · 앞 달 품목에 반영된 취소 1 · 뺀 품목 1 · 제외 1」 · 안내 0.4.0 문구 |
| `repayment.png` | 재결제(800,000 → 전액 취소 → 600,000) — 머리 「취소 1 · 600,000」 · 품목 600,000 결제 완료 · ⚠ 없음 |
| `partial-refund.png` | 선불카드 50만원권 → 남은 300,000 · `부분 환불` 배지 · 머리 「취소 1 · 300,000」 |
| `prior-cancel.png` | 앞 달 결제 취소 — 머리 「취소 2 · −300,000」(빨강) · 「앞 달 결제 취소 · 품목은 다른 달에 · 첫 승인 09-20」 · 품목 줄 없음 |
| `zero-order.png` | ② 차례 [마스크팩 0 · 써마지 1,000,000 · 마취 크림 30,000] → 화면 써마지 · └ 마스크팩 · 마취 크림 |
| `refunded-item.png` | 전액 환불 품목 줄 없음 · 머리 「취소 1 · 환불 1」 |
| `mismatch.png` | `paymentsNet` 800,000 ≠ 품목 1,200,000 → `⚠ 결제 ≠ 품목` |
| `mixed-currency.png` | `netTotal null` → `⚠ 통화 섞임`(합 없음) |
| `agency-all.png` | 에이전시 손님 7 · 결제 손님 6(숨긴 수납 손님 포함) · **실결제 합 5,900,000** · 수납 6 · 품목 8 · 취소된 결제 5 · 전액 환불 1(숨긴 수 없음) · A 4명·3명·3,900,000 / B 2·2·2,000,000 / C 1·1·0 · 탭 전체 6 · A 4 · B 1 · C 1 |
| `agency-one.png` | 에이전시A 손님 4 · 결제 손님 3 · 실결제 합 3,900,000(= 3,300,000 + 600,000 − 300,000 + 300,000) |
| `monthly-closed.png` | 9월 확정 · 숨긴 수납 1(전액 환불) |
| `agency-hidden-only.png` | 9월 에이전시B(수납이 전부 숨김 · 탭 숫자 0) — 「이 달 보일 결제가 없어요 — 손님 1명 · 결제 손님 1명(취소 · 환불 · 다른 달 품목만)」 · 주소 그대로(그달 `agencies[]` 에 있음) |

## WP-FE3 완료 조건 (WORK 3판 행)

| 조건 | 결과 |
|---|---|
| `lib/types.ts`(0.4.0 이후) | 충족(0.4.2 — `reflectedCancels` 포함) |
| 머리 실결제 | 충족(`netTotal` · 음수 빨강) |
| 「취소 a · 환불 b」 | 충족 |
| 「앞 달 결제 취소」(음수) 머리 | 충족 |
| 실결제 0 · 줄 0 묶음 숨김(그리지 않음) | 충족(back 이 빼고 + front `isHidden` 한 번 더 · itemsMissing 은 안 숨김) |
| 빈 에이전시 탭 문구(손님 n · 결제 손님 m) | 충족 |
| 결제 · 취소 · 환불 줄 그리기 지움 | 충족(줄 0 — grep · 스크린샷) |
| 배지 이름 `결제 완료` | 충족 |
| 건수 줄 · 안내 문구 | 충족 |
| 에이전시 요약 실결제 합 | 충족(`agencyTotal.netTotal` · `agencies[].netTotal` · null → 「통화 섞임」) |
| `⚠ 통화 섞임` = `netTotal === null` | 충족 |
| ⚠ 배지 = `paymentsNet ≠ itemsTotal` | 충족 |
| 숨긴 수납 수(월별 건수 줄만) | 충족 |
| §9.3 0.4.0 줄 스크린샷(가짜 값) | 충족(12장) |
| tsc · lint | 충족 · **build 0 = 안 돌림**(지시 — 3800 dev 와 `.next` 공유) |

## 구현 때 지킬 것 1 ~ 10

| # | 결과 |
|---|---|
| 1 schema 1→2 채우기 잠금 · 한 트랜잭션 | 해당 없음(back) |
| 2 판정 함수 하나 · 응답 · 엑셀 · 에이전시 합 | 해당 없음(back) — front 는 `netTotal` · `agencies[].netTotal` 을 다시 계산하지 않고 그대로 보인다 |
| 3 증분 ② 갈아 끼우기 대상 | 해당 없음(back) |
| 4 살아 있는 승인 저장값 | 해당 없음(back) — front 는 `paidAt` · `paymentTypes` 그대로 |
| 5 「앞 달 결제 취소」 글자 두 표 | **충족** — `LINE_KIND_TEXT.PRIOR_CANCEL = '앞 달 결제 취소'` · `LINE_STATUS.PRIOR_CANCEL = '취소'` · back `labels.py` 와 5표 같음(대조) |
| 6 숨긴 수납 수는 월별만 · front 가 만들지 않음 | **충족** — 에이전트별 `countLines` 에 hidden 없음 |
| 7 `⚠ 통화 섞임` = `netTotal === null` | **충족** |
| 8 옛 필드 grep 0(front `types.ts` 포함) | **충족**(위 grep) |
| 9 시각 비교는 파싱한 시각 | 해당 없음 — front 는 반영 판정을 하지 않는다(정렬은 기존 `toMs` 파싱) |
| 10 로그 · 오류에 netTotal · paymentsNet 값 없음 | 해당 없음 — front 는 로그를 남기지 않는다(오류 토스트는 back `message` 그대로) |

## 시안 · 앞 판과 다른 곳 · 미결

1. 머리 오른쪽 칸 이름 「그달 결제」 → 「실결제」 · 줄 칸 「일시」 비움(0.4.0 — 품목 줄에 시각 없음 · 칸 너비는 시안 그대로 둠)
2. 「취소 a · 환불 b」 = 머리 오른쪽 실결제 앞 회색 작은 글(시안 없음 · OQ-134 자리)
3. 「앞 달 결제 취소」는 머리 아래 첫 줄에 빨간 작은 글(「품목은 다른 달에」와 같은 자리)
4. 건수 줄의 회색 글 차례: 취소된 결제 · 전액 환불 품목 · 숨긴 수납(월별만) · 반영된 취소(>0) · 뺀 품목(>0 · `excludedItems` — SPEC 건수 줄 문장엔 없으나 「정보」 시트와 맞춤) · 제외(>0)
5. 에이전시 실결제 합이 0 이하면 빨강 · null 이면 「통화 섞임」
6. 본문 폭은 2판 수정 1(사용자 지적)의 **1600 가운데 그대로** — SPEC §3.1 「폭 max-width 없음」 줄은 아직 옛 문구(planner 정리 몫)
7. 진짜 back(BE3) 붙여 보기 안 함 — 3800 dev 는 hot reload 로 이미 이 코드. 8800 이 0.4.2 응답 전이면 그 화면은 깨질 수 있음
8. 시험 스크립트 사본 `fe3-fake-back.mjs` · `fe3-shoot.mjs`(같은 폴더)

---

## 수정 1 (지시서 `fe3-fix-1-instructions.md` — code r3 W-1 · NOTE-6 · 사용자 화면 hydration 경고)

| # | 고친 것 | 파일 |
|---|---|---|
| W-1 | **묶음 차례 = back 응답 차례 그대로**(front `sortPurchases` · `byTime` 지움 — 엑셀과 같은 차례) · 「앞 달 결제 취소」 머리의 결제일 칸 = 「— 시각 없음」 대신 빨간 「앞 달 결제 취소」(back 이 `paidAt` 을 주면 「MM-DD HH:mm 앞 달 결제 취소」) · 머리 아래 글은 「품목은 다른 달에 · 첫 승인 MM-DD」(회색 · 겹치는 글자 뺌) | `components/monthly/{format.ts,SalesTable.tsx,PurchaseGroup.tsx}` |
| NOTE-6 | `isHidden` 에 `&& !p.itemsNowhere` — back 과 같은 규칙(itemsMissing · itemsNowhere 는 숨기지 않음) | `components/monthly/format.ts` |
| hydration | **코드 변경 없음** — 원인 아래 | — |

### hydration 경고 원인

- 3800 dev 로그 `front/.next/dev/logs/next-development.log`(읽기만)의 React 차이(`+` = 클라이언트 · `-` = 서버): `<header style>` 에서 **클라이언트에는 `justifyContent: "space-between"` · `gap: 16` 이 있고 서버 HTML 에는 없음**. 이 두 속성은 2판 수정 1(폭 1600)에서 `<header>` → 안쪽 `<div>` 로 옮긴 것
- 즉 **서버 = 새 코드(수정 1 뒤), 브라우저 = 수정 1 전 클라이언트 묶음**. 코드 수정 중 hot reload 사이에 페이지를 열어 새 HTML 을 옛 JS 가 hydrate 한 것 — 서버/클라이언트 분기 · 시각 · 브라우저 값 · 확장 프로그램 문제가 아니다. 로그의 hydration 줄 12개 모두 이 한 꼴
- 지금 코드 확인: 3800 을 새 브라우저로 **읽기만**(GET 한 번 · 8800 요청 2건 playwright 에서 막음 — back · KOS 호출 0) → hydration 메시지 0. 복사본 3892 에서도 `/` · `/agency` · 9월 · 탭 주소 · `2026-13` 모두 0
- 사용자 쪽: 브라우저 새로고침(필요하면 강력 새로고침) 한 번이면 사라진다. 다시 나오면 그 로그 줄을 주면 원인을 다시 본다

### 확인(`fe3-fix1-check.mjs` · 복사본 dev 3892 + 가짜 back 8892 · 끝나고 내림)

- 가짜 back 이 시각 차례가 아닌 차례로 줌(10-02 취소 묶음이 6번째) → 화면 차례 = back 차례 **같음**(10묶음)
- 「앞 달 결제 취소」 머리(`paidAt null`): 결제일 칸 「앞 달 결제 취소」 · 「시각 없음」 0 — `shots-fe3/prior-cancel.png`
- `itemsNowhere` · 실결제 0 · 줄 0 수납: **보임** + 「품목이 어느 달에도 없어요 — 이 달 [전체 다시 받기]」 — `shots-fe3/items-nowhere.png` · `monthly.png` 다시 찍음
- console error 0 · `npx tsc --noEmit` 통과 · `npm run lint` exit 0 · build 안 돌림
