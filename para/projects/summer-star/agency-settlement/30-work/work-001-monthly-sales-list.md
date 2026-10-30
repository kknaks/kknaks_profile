---
type: work
id: WORK-001
title: "월별 매출 리스트 — 새 레포 agency-settlement · back(KOS 조회 전용 · 조인) → front(cc-prototype 디자인 복사) → 운영 KOS 10월 실물 조회 1회 · 2판(저장 · 증분 · 에이전트별 · 엑셀 — SPEC-001 0.3.0) · 3판(최종 결제만 — SPEC-001 0.4.3 · 코드 PR #1)"
status: draft
product: agency-settlement
feature: monthly-sales
work_type: feature
owner: kknaks
progress: 100
created_at: 2026-10-29
updated_at: 2026-10-29
tags:
  - product/agency-settlement
  - feature/monthly-sales
  - doc/work
  - status/draft
links:
  baselines: []
  decisions:
    - "[[decision-001-monthly-sales-list|DEC-001]]"
  specs:
    - "[[spec-001-monthly-sales-list|SPEC-001]]"
  works: []
  releases: []
  related: []
up: []
sources:
  - "orchestration/work/agency-settlement/_RESUME.md §2 — 2026-10-29 줄 전부"
  - "orchestration/work/agency-settlement/research-agency-attribution.md (Q5 · Q6)"
  - "orchestration/work/agency-settlement/review-spec-007-report.md · planner-fix-1-instructions.md (수정 1판 — F-1 · W-1 ~ W-6) · planner-fix-2-instructions.md (수정 2판 — ⑤ 승인 · 결제일 원천) · planner-fix-3-instructions.md (수정 3판 — 별도 프로젝트) · review-spec-001-r2-report.md · planner-fix-4-instructions.md (수정 4판 — 첫 승인 달 규칙)"
  - "orchestration/work/agency-settlement/_RESUME.md §2 — 0.3.0 줄(시안 v1 채택 · 에이전트별 · SQLite · 받은 시점 · 시안 v2 채택 · 엑셀)"
  - "orchestration/work/agency-settlement/review-code-r1-report.md · backend-fix-1-instructions.md (code r1 · 수정 1판)"
  - "orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v1.dc.html · v2.dc.html · design-report.md · design-v2-report.md (시안)"
  - "cc-prototype procedure/ main(읽기만 — back app/kos/client.py · config.py · main.py · front 디자인 파일)"
---

# 월별 매출 리스트 — 빌드 계획

계약은 **SPEC-001 0.4.3**(전부) — 이 문서는 빌드 계획만 적고 계약을 다시 쓰지 않는다. 결정 = DEC-001(D-01 ~ D-18).

- **1판**(WP-BE · WP-FE · WP-REVIEW · WP-LIVE) = SPEC 0.2.1 — 구현 · 운영 10월 조회 성공(_RESUME §5)
- **2판**(WP-BE2 · WP-FE2 · WP-REVIEW2 · WP-LIVE2) = SPEC 0.3.1(0.3.0 + doc r3 수정)
- **3판**(WP-BE3 · WP-FE3 · WP-REVIEW3 · WP-LIVE3) = SPEC 0.4.3(0.4.0 + doc r5 · r6 수정 + 구현 뒤 동기) — **D-18 최종 결제만**(머리 실결제 · 품목 = 최종 결제 · 취소 · 전액 환불은 숫자만). 2판 위에 얹는다(아래 「3판」 — 2판과 다르면 3판이 이긴다) — 저장 · 증분 · 에이전트별 · 엑셀 · 시안 v1 · v2 적용 · code r1 SPEC 정리(아래 「2판」)

## Meta

- Covers spec: SPEC-001 0.4.3(1판 = 0.2.1 · 2판 = 0.3.1)
- 코드 레포: **`kknaksss/agency-settlement`**(private · 로컬 `/Users/kknaks/git/toy_pr2/agency-settlement` · 1판 코드 있음 — 워크트리 `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement`) — 범위 **`back/**` · `front/**` · `README.md`**. cc-prototype 레포는 읽기만(디자인 · KOS 클라이언트 복사 원본 — 그 레포엔 아무것도 쓰지 않는다) · R§2 별도 프로젝트 줄 · D1-08
- base: 코드 레포 `kknaksss/agency-settlement` `main` · 워크트리 · 브랜치는 코디가 정한다
- **코드 PR**: https://github.com/kknaksss/agency-settlement/pull/1 (커밋 `2b299dc` — 1 · 2 · 3판 전부 · SPEC 0.4.2 구현 + code r3 수정 1 · 2 · SPEC 0.4.3 은 이 코드에 맞춘 동기)
- 워커: backend · frontend · reviewer · 코디(실물 조회)
- 검증은 WP 마다 그 범위만. 전체 검증(pytest 전부 · front build · 로컬 두 프로세스)은 WP-LIVE 에서 한 번
- **완료 = 운영 명동점 KOS 를 로컬에서 실제로 1회(10월) 조회해 리스트가 화면에 뜬 것**(SPEC-001 §9.2 L1 ~ L12). 가짜 응답 · 데모 지점으로 대신하지 않는다
- 배포 없음(D1-09) · infra 레포 변경 없음
- **운영 데이터** — 근거 `_RESUME` §2 운영 키 줄(10-29 확장 — 「이 프로젝트 코드 · WP-LIVE 실물 조회까지 같은 조건(조회만 · 로컬만)」). 운영 키는 `back/.env`(gitignore)에만 · 코디가 넣는다. **워커는 운영 키를 쓰지 않는다**(WP-BE · WP-FE 는 가짜 transport · 가짜 응답만). 문서 레포(kknaks_profile)는 public · 코드 레포는 private — 어느 쪽이든 실명 · 실제 금액 · 유입 이름 · 키 · 테넌트 id 를 커밋 · 리포트 · 스크린샷에 넣지 않는다

## 계약 고정점 — 1판(SPEC 0.2.1)

> **1판 표다. 2판 워커는 아래 「2판」 표를 따른다 — 둘이 다르면 2판이 이긴다**(`refresh=1` · 경로 2 · 메모리 캐시 `SALES_CACHE_SEC` 는 0.3.0 에서 없어졌다)

| 고정점 | 값 | SPEC-001 |
|---|---|---|
| 레포 구조 | `kknaksss/agency-settlement` 루트에 `back/` · `front/` · cc-prototype import 0(복사만) · compose 없음 | §2 |
| API | `GET /api/sales?month=YYYY-MM[&refresh=1]` · `GET /api/health` · 경로 2 · `Cache-Control: no-store` | §4.1 |
| 응답 | `month` · `rangeUtc` · `fetchedAt` · `cached` · `counts{purchases,itemLines,paymentLines,reversalLines,transactions,ignoredTransactions,itemsMissing,visitorMissing,itemsElsewhere,firstApprovalCanceled,firstApprovedUnknown,unmatchedTransactions,atOutsideMonth}` · `purchases[{purchaseId,paidAt,firstApprovedAt,itemsHere,visitorId,visitorName,visitDate,visitorFunnelName,paymentTypes,currency,approvedTotal,itemsTotal,itemsMissing,lines[{kind,itemType,productName,productNameFrom,optionName,amount,currency,status,at,paymentType?}]}]` | §4.2 |
| 오류 | `bad_month` 400 · `kos_not_configured` 503 · `kos_busy` 503 · `kos_rejected` 502 · `kos_unavailable` 502 · `guard_blocked` 500 · **「없음」 = 400 + `errorProperties {key: purchaseId|visitorId, reason: NotFound}` 일 때만**(그 밖 400 · 404 = `kos_rejected`) | §4.3 · §6.4 |
| KOS 작업 | ① `getTransactionStatistics` ② `getPurchaseItemStatistics`(달 시작 −31일부터) ③ `findScheduleByPurchaseId` ④ `getVisitor`(③ 「없음」일 때만) ⑤ `getPurchaseSummaries`(100개씩 · 첫 승인 시각) + 토큰 교환 · ③ ④ 응답에선 이름 · 예약 시작만 꺼냄 | §5.1 · §5.3 · §7.3 |
| 가드 | 허용 경로 상수 5개 + `/queries/` · 토큰 교환은 인증 함수만 · 다시 받기 잠금 1회 · 내부 API 복사 안 함 | §7.1 |
| 월 경계 | KST `YYYY-MM-01 00:00` ~ 다음 달 1일 00:00 − 1초 → UTC · 귀속은 ① `createdTimeUtc` 필터(OQ-119) | §6.1 |
| 결제일 | **⑤ `approvedDateTimeUtc`(결제) · `canceledDateTimeUtc`(취소) · `spentDateTimeUtc`(반환)** · ① 행 ↔ ⑤ 거래는 수납 · 상태 · 수단 · 금액 절댓값 · 통화로 잇고 동점만 「마지막 상태 변경 일시」로 가름 · 못 이으면 `at null` · ① `lastUpdatedPaymentDateTimeUtc` 는 보이지 · 정렬하지 않음 | §5.4 · §3.3 |
| 줄 | 품목 = **그 수납의 「취소 안 된 첫 승인 결제 행」이 ① 로 귀속된 달에만**(⑤ 로 첫 승인을 고르고 · 전액 취소 뺌 · 달은 ① 귀속 · 시각 없으면 대체 + `firstApprovedUnknown`) · 다른 달이면 승인 결제를 `payment` 양수 줄로 · `CANCELED` → `cancel` 음수 줄 · `SPENT` → `spent` 음수 줄 · `REQUESTED` · `FAILED` → 제외 수 · 통화 섞인 수납 = 합 `null` | §6.2 · §6.3 · §6.7 |
| 상품명 | `productTitle` → `prepaidCardName` → `etceteraProductName` → `—` | §6.5 |
| 유입 | ① `visitorFunnelName` 그대로 · 빈 값 `null` · 자유 텍스트 읽지 않음 | §6.6 |
| 캐시 | 메모리 · 달별 · `SALES_CACHE_SEC` 600 · 동시 `SALES_KOS_CONCURRENCY` 8 | §4.4 |
| 실행 | back `127.0.0.1:8800` · front `localhost:3800` | §10 |

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-BE** | **back 전부** — `back/` 뼈대(uv · pyproject · ruff · pytest — cc-prototype procedure/back 과 같은 판) · `config.py`(env §10.1 · `back/.env` 하나) · `domain/{clock,errors}.py`(cc-prototype procedure 에서 복사) · `kos/client.py`(cc-prototype procedure `client.py` 의 **공개 토큰 · `_call` · `_error_of` 만 복사** + 조회 전용 가드 · 토큰은 메모리) · `service/sales.py`(월 경계 · 오프셋 파싱 · ①② cursor 끝까지 · ⑤ 100개씩 · 첫 승인 결제 고르기(전액 취소 뺌 · 대체 정렬) · ① 귀속 달 판정 · ① ↔ ⑤ 거래 잇기 · 결제일 = ⑤ 시각 · ③④ 동시 제한 · 「없음」 = 400 `NotFound` 만 · 이름 · 예약 시작만 꺼냄 · 묶음 · 줄 · 상태 · 상품명 · 통화 · 캐시 · 달별 잠금 · 토큰 잠금) · `api/sales.py` · `schemas/sales.py` · `main.py`(오류 처리기 · CORS GET 하나 · `no-store` · httpx 로그 WARNING) · `tests/`(KOS 가짜 transport) · `back/.env.example` · 레포 루트 `README.md`(실행 · env 채우기 더함) | SPEC-001 §2 · §4 · §5 · §6 · §7 · §10 | backend | `back/**` · `README.md` | SPEC-001 §9.1 1 ~ 24(9b 포함) 전부 통과 — **「없음」 시험은 가짜 응답을 400 + `NotFound` 꼴로**(404 로 「없음」을 시험하지 않는다 · 9b 의 「다른 reason 400 → 502」 · 「404 → 502」 포함) · `grep -rn "commands/" back/app` = 토큰 교환 상수 1줄 · `grep -rn "sign-in\|tenants/" back/app` = 0 · `git status --ignored` 에 `back/.env` 가 추적 안 됨 · **운영 · 데모 KOS 호출 0** | `cd back && uv run ruff check . && uv run pytest -q` | 완료(pytest 63 → 수정 1판 67 · code r1 W-1 · W-2 · W-5 · W-6) |
| **WP-FE** | **front 전부** — §8 복사 목록(tailwind · postcss · 테마 · 보정 · globals 일부 · layout · 로고 · `lib/time.ts` 일부 · `lib/api.ts` 의 `API_BASE` · `CONFIG_ERROR`) · `package.json`(medikit 1.4.0 · 포트 3800) · `lib/types.ts`(§4.2 그대로) · `lib/labels.ts`(품목 종류 · 상태 · 결제 수단 이름 — §6.3 표) · `app/page.tsx`(`?month=` · 기본 이번 달 KST) · `components/monthly/*`(월 선택 `[‹] [›]` · 다시 불러오기 · 건수 줄 · 수납 묶음 머리 · 품목 줄 · `payment` 줄 · 「품목은 다른 달에 · 첫 승인 MM-DD」 · 결제일 「시각 없음」 · 음수 줄 · `⚠ 결제 ≠ 품목` · `⚠ 통화 섞임` · `itemsMissing` 줄 · 「상태는 지금 기준」 안내 · 상태 화면 5종) · 복사 파일 머리 「원본:」 주석 | SPEC-001 §3 · §4.2 · §8 | frontend | `front/**` | 가짜 응답(§4.2 꼴 · 가짜 이름 `홍**` · 가짜 금액)으로 §3.4 상태 5종 · 묶음 · `payment` 줄 · 음수 줄 · 경고 배지 2종 스크린샷 · cc-prototype import 0(`grep -rn "procedure/\|cc-prototype" front --include=*.ts --include=*.tsx` = 「원본:」 주석만) · `localStorage` · `sessionStorage` 0 | `cd front && npx tsc --noEmit && npm run lint && npm run build` | 완료(tsc · lint · build 0 · 스크린샷 7) |
| **WP-REVIEW** | reviewer: SPEC-001 §1 ~ §10 ↔ 코드 · 부록 A · 경로 2 · 가드(허용 경로 5 · 내부 API 0 · 토큰 잠금) · 「없음」 판정 = 400 `NotFound` 만(404 · 다른 reason 은 `kos_rejected`) · ③ ④ 응답에서 이름 · 예약 시작 외 필드가 변수 · 캐시 · 로그에 안 남음 · 품목 줄 = 취소 안 된 첫 승인 결제 행의 ① 귀속 달 한 번(#22 ~ #24) · ⑤ 응답에서 꺼낼 필드만 남음(메모 · items 0) · 결제일 · 정렬이 ⑤ 시각(① `lastUpdatedPaymentDateTimeUtc` 가 응답 · 화면에 0) · 응답 키 = §4.2 · 자유 텍스트 필드(`…FunnelDetail` · 메모)가 응답 · 코드에서 안 읽힘 · 로그에 이름 · 금액 · id · 키 0 · `127.0.0.1` · `.env` 미추적 · cc-prototype import 0(복사만). FAIL 은 모아서 한 번에 수정 발주 | 전체 | reviewer | `back/**` · `front/**` · `README.md` | PASS | — | 완료 WARN(F 0 · W 7 — `review-code-r1-report.md`) |
| **WP-LIVE** | **코디: 운영 KOS 실물 조회 1회(10월)** — 근거 `_RESUME` §2 운영 키 줄(10-29 확장). ① `back/.env` 에 운영 키(원본 ax-clinic-project `scripts/.env` 의 `KOS_API_tenent` — 이름만 · 값은 파일에서 옮김) · ② 전체 검증(pytest 전부 · front build) · ③ back `127.0.0.1:8800` · front `3800` 띄움(커밋 뒤 옛 프로세스 아님을 확인) · ④ 브라우저에서 `?month=2026-10` **한 번** · ⑤ §9.2 L1 ~ L12 기록(L10 = 환불 품목 수납 · L11 = 두 달에 걸친 수납 · 전액 취소 건너뛴 수납(a) · 대체 판정 수납(c) · L12 = 잇지 못한 거래 · 결제일이 달 밖인 행) · ⑥ L5 · L10 결과로 `⚠ 결제 ≠ 품목` 배지 문구 · 조건 제안(OQ-106) · ⑦ 사용자에게 화면 확인 요청 · 피드백은 모아서 한 번에 | SPEC-001 §9.2 | 코디 · 사용자 · (수정) 각 워커 | `back/.env`(gitignore · 커밋 안 함) | **L1 화면에 10월 리스트가 뜸** + L2 ~ L12 통과(수 · 같음/다름만 기록) · 사용자 확인 | `cd back && uv run pytest -q` · `cd front && npm run build` | 10월 조회 성공(_RESUME §5) · 사용자 확인 → 2판 결정(D-10 ~ D-14) |

## 병렬

```text
WP-BE ───────────────┐
                     ├── WP-REVIEW ── WP-LIVE(운영 10월 1회 → 사용자 확인)
WP-FE(화면 먼저 · 가짜 응답 → WP-BE 뒤 붙이기) ┘
```

- back · front 는 파일이 겹치지 않는다 — 동시에. front 는 §4.2 응답 꼴로 가짜 응답을 먼저 그리고 WP-BE 뒤 로컬 back 에 붙인다(붙일 때도 KOS 는 가짜 — back 시험용 가짜 transport 를 쓰는 개발 모드는 만들지 않는다. 붙이기 확인은 WP-LIVE 에서)
- 레포 루트 `README.md` 는 WP-BE 가 갖는다(겹침 방지)

## 주의

- **운영 KOS 는 WP-LIVE 에서 코디만 · 10월 1회.** 다시 부를 일이 생기면(수정 뒤 재확인) 그때마다 사용자에게 알린다. `/commands/` 는 토큰 교환 하나뿐
- 백엔드 커밋 뒤 back 재기동(옛 코드로 확인 금지) · 워커는 사용자 포트 · 프로세스를 건드리지 않는다
- WP-LIVE 결과 · 스크린샷을 문서 레포(public)에 올릴 때 이름 · 금액 · 유입 이름 · 수납 id 를 가린다 — 수와 같음/다름만
- 마감 전 `git status --ignored` — `back/.env` · `front/.env.local` 은 커밋하지 않고 워크트리 정리 때 옮길 곳을 사용자에게 묻는다
- 열린 것(SPEC-001 §11 OQ-101 ~ OQ-121 · OQ-103 · OQ-104 는 닫힘)은 기본값으로 구현한다. OQ-102(환불 품목 금액 — 기본값 원 가격)는 WP-LIVE L10 으로 실물 확인 · OQ-106 배지는 L5 · L10 뒤 · OQ-119(귀속 ≠ 결제일 달) · OQ-120(거래 잇기)은 L12 결과와 함께 사용자에게 올린다

## 2판 — SPEC-001 0.3.1 (저장 · 증분 · 에이전트별 · 엑셀)

### 계약 고정점 (2판에서 바뀌거나 더해진 것만)

| 고정점 | 값 | SPEC-001 |
|---|---|---|
| 경로 | `GET /api/sales?month=[&refresh=new\|full]` · **`GET /api/sales.xlsx?month=&view=monthly\|agency[&agency=]`** · `GET /api/health` — **경로 3** · 옛 `refresh=1` → 400 `bad_refresh` | §4.1 · §4.3 |
| 응답 더함 | `store{state,fetchedAt,fullFetchedAt,closedAt}` · `fetch{mode,fromUtc,kosCalls,newTransactions,duplicateTransactions,newPurchases}` · `counts.itemsPinnedElsewhere` · `counts.itemsNowhere` · `fetch.missingTransactions` · `purchases[].itemsNowhere` · `agencyTotal{customers,payingCustomers,purchases}` · `agencies[{name,customers,payingCustomers,purchases}]` · `purchases[].agency` · `purchases[].newInLastFetch` · `cached` = `fetch.mode == none` | §4.2 |
| 오류 더함 | `bad_refresh` 400 · `bad_view` 400 · `not_fetched` 409 · `store_failed` 500 | §4.3 |
| 저장 | SQLite(표준 `sqlite3` · ORM 없음) · `SALES_DB_PATH=data/sales.sqlite3`(레포 안이면 `back/data/` · `.sqlite3` 만) · gitignore `back/data/` · `*.sqlite3*` · `data/` 700 · umask 077 · 본 파일 · `-wal` · `-shm` 600 · `schema_version` 다르면 멈춤 · 응답 = 읽기 트랜잭션 하나 · WAL · 표 6개(`months` · `transactions` · `purchase_txs` · `items` · `visitors` · `month_purchases`) · 줄인 필드만(원본 JSON 0 · 개인정보 = 이름 · 방문일) · 받기 = KOS 다 마친 뒤 한 트랜잭션 · 응답은 늘 저장본에서 · 메모리 캐시 없앰 | §4.4 · §7.3 |
| 받기 판단 | J1 ~ J6 — `closed` = KOS 0 · 저장 없음 = 전체 · `current` = 증분(`refresh=new` · 또는 `SALES_CURRENT_STALE_SEC` 넘음) · 끝난 `current` 달 = 증분 한 번 뒤 확정 · 증분 = ① 달 전체 1회 · 새 행 = 묶음 키(수납 · 상태 · 수단 · 금액 · 통화) 수 차이(`last_updated` 안 씀 · 줄면 `missingTransactions`) · 줄 선 요청 = 저장본만 · 전체 받기 `items` 갈아 끼우기 = 이 달 itemsHere 수납만 · 품목 달 고정 확인 = 쓰기 트랜잭션 안 · `itemsNowhere` · itemsHere 인데 품목 없는 수납 = ② 1회 · ⑤ = 새 수납 · 새 거래 수납만 · ② · ③ · ④ = 새 수납만 · 품목 달 고정 | §4.5 · §4.6 |
| 에이전시 | `agency` = 유입 값(공백 뗌)이 반각 `(에이전시)` 로 정확히 끝남 · 목록 = 그달에 나온 것만 · 이름 차례 · 손님 = **`visitorId` 중복 없이(없으면 수납 id · D-15 — 이름으로 세지 않음)** · 결제 손님 = 그달 승인 행 있음(0 원 · 순액 0 이하 포함 — 사용자) · 금액 합 없음 | §6.8 |
| 엑셀 | 저장본으로만(KOS 0 · 저장 없음 409) · `openpyxl` · 시트 「매출」 11칸(D-14 차례) · 글자 칸 = 글자 셀(수식 해석 0) · 줄 하나 = 행 하나(0원 · 음수 포함 · 합계 없음) · 숫자 · 날짜 셀 · 수납 id 전체 · 시트 「정보」 · 파일 이름 `매출_YYYY-MM_<화면>.xlsx` · 이름 표 back = front | §4.7 |
| code r1 정리 | W-3 = ⑤ 시각 비어도 잇기 유지(`at` 만 null) · W-1 = ⑤ 승인 0 → 「⑤ 에 수납 없음」과 같게 · W-5 = 통화 0개는 섞임 아님(front 는 `approvedTotal === null` 일 때만 「통화 섞임」) · W-6 = `SALES_BACK_PORT` 는 실행 명령이 읽음 — **1판 코드 · 수정 1판이 이미 이대로**(문서를 코드에 맞춤 · 2판에서 코드 변경 없음 · W-5 front 판정만 FE2) | §5.4 · §6.2 · §6.7 · §10.1 |
| 화면 | 시안 v1 · v2 가 정본 — 헤더 메뉴 2 · 넓은 폭 · 두 층 표 · `current` = [새 결제 받기] + 작은 [전체 다시 받기] / `closed` = 「확정 · 저장됨」 + 작은 [전체 다시 받기] · 확인 1번 · 「MM-DD HH:mm 받음」 · 「새 결제 N」 / 「새 결제 없음 · HH:MM 확인」 · 「새로 받음」 배지 · 「받은 시점 기준」 · `/agency` 탭(「에이전시 전체」 + 그달 에이전시 · 글자 「(에이전시)」 뗌) · 툴바 오른쪽 [엑셀 내보내기] | §3 |

### Work Packages (2판)

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-BE2** | **저장 · 증분 · 에이전시 · 엑셀** — `repository/store.py`(표 6개 · `CREATE TABLE IF NOT EXISTS` · WAL · busy_timeout · 600 · 한 트랜잭션 쓰기 · 읽기) · `service/sales.py`(메모리 캐시 걷어 내기 · J1 ~ J6 판단 · 전체 · 증분(① 달 전체 · 묶음 키 수로 새 행 · 새 행 있는 수납만 ⑤ · itemsHere 인데 품목 없는 수납 ② · 새 수납만 ③) · 확정 · 품목 달 고정 · 응답은 저장본에서 · `store` · `fetch` · `newInLastFetch` · `agency` · `agencies` · `agencyTotal` · 달별 잠금 + 쓰기 잠금) · `service/export.py`(xlsx · `openpyxl`) · `service/labels.py`(front `labels.ts` 와 같은 표) · `api/sales.py`(`refresh=new\|full` · `sales.xlsx` · `bad_refresh` · `bad_view` · `not_fetched` · `store_failed`) · `schemas/sales.py` · `config.py`(`SALES_DB_PATH` · `SALES_OVERLAP_SEC` · `SALES_CURRENT_STALE_SEC` · `SALES_CACHE_SEC` 없앰) · `.env.example` · 레포 `.gitignore`(`back/data/` · `*.sqlite3*`) · `pyproject`(`openpyxl`) · README(env · 저장 파일 · 지우는 법) · 시험(가짜 transport + 임시 DB 파일 · 가짜 시계) | SPEC-001 §2 · §4 · §6.8 · §7.3 · §10 | backend | `back/**` · `.gitignore` · `README.md` | SPEC-001 §9.1 1 ~ 44 전부(#12 · #15 · #20 고친 것 포함 · 1판 시험은 그대로 초록) · `test_route_count_3` · DB 칸 덤프에 가짜 전화 · 메모 0 · `git status --ignored` 에 `back/data/` ignored · **운영 · 데모 KOS 호출 0** | `cd back && uv run ruff check . && uv run pytest -q` | 완료(코드 PR #1 에 합쳐짐 · 수정 1판 뒤 pytest 122) |
| **WP-FE2** | **시안 v1 · v2 적용 · 에이전시 탭 · 받기 · 엑셀 버튼** — 헤더 메뉴(`AppHeader` 복사 → 메뉴 2 · 세션 뺌) · 넓은 폭 · 두 층 표 · 결제 · 취소 줄의 수단 · 설명 글 · 0원 구성품 흐림 · `lib/types.ts`(§4.2 0.3.0) · `lib/api.ts`(`getSales(month, refresh?: 'new'\|'full')` · `salesXlsxUrl(month, view, agency?)`) · `lib/labels.ts`(결제 수단 한글 이름 더함 — back `labels.py` 와 같은 표) · 받기 버튼 두 상태 · 확인 1번 · 받은 시각 · 「새 결제 N」 · 0건 문구 · 「새로 받음」 배지 · 「받은 시점 기준」 · `app/agency/page.tsx`(탭 · `?agency=` · 없는 값 → 전체 · 걸러진 건수 줄 · 요약 · 「수수료 — 다음 판」) · `⚠ 통화 섞임` 판정 = `approvedTotal === null`(W-5) · 툴바 오른쪽 [엑셀 내보내기] | SPEC-001 §3 · §4.2 · §8 · §9.3 · 시안 v1 · v2 | frontend | `front/**` | SPEC-001 §9.3 전부 · 시안 v2 장면(`monthly-current` · `monthly-closed` · `agency-all` · `agency-one`)과 나란히 스크린샷(가짜 값) · `refresh=1` grep 0 · `localStorage` · `sessionStorage` 0 · cc-prototype import 0 | `cd front && npx tsc --noEmit && npm run lint && npm run build` | 완료(코드 PR #1 · 시안 v1 · v2 적용 · 폭 1600 — 2판 수정 1) |
| **WP-REVIEW2** | reviewer: SPEC-001 0.3.1 ↔ 코드 — **돈 경로 먼저**(증분 새 행 = 수 · 같은 수단 · 같은 금액 새 거래 · 전체 받기 갈아 끼우기 범위 · 두 달 동시 · `itemsNowhere` · 증분 itemsHere 바뀜 · 줄 선 요청) · — §4.4 표 · 칸(원본 JSON · 이름 밖 개인정보 0) · §4.5 판단표 J1 ~ J6 · 증분 `from` · 거래 키 · 새 수납 · 새 거래만 · 확정 시점 · 실패 시 DB 안 바뀜 · 품목 달 고정 · 잠금 · §6.8 판정(반각 · 정확히 끝 · 자유 텍스트 0) · 손님 셈 · §4.7 엑셀(KOS 0 · 11칸 차례 · 행 = 줄 · 셀 형식 · 파일 이름 · 로그) · labels 두 표 같음 · 경로 3 · `back/data/` gitignore · 로그에 이름 · 금액 · id · 에이전시 이름 0 · front 받기 버튼 · 탭 · 엑셀 주소 · 시안 v2 대조. FAIL 은 모아서 한 번에 수정 발주 | 2판 전체 | reviewer | `back/**` · `front/**` · `README.md` · `.gitignore` | PASS | — | 완료(code r2 · 지적은 BE · FE 수정 1 · SPEC 0.4.3 으로 닫음) |
| **WP-LIVE2** | **코디: 운영 KOS 실물 조회 2** — 근거 R§2 운영 키 줄 · D1-12. ① 커밋 뒤 back 재기동(옛 프로세스 아님 확인) · **빈 DB** ② 전체 검증(pytest 전부 · front build) ③ **9월 한 번 받고 → 다시 열기 · 메뉴 · 탭 · back 재시작 뒤 다시 열기 = KOS 호출 0**(L13) ④ 10월 첫 받기(full · `kosCalls` 기록) → 몇 분 뒤 [새 결제 받기] = **증분 호출 수**(L14) ⑤ 사용자에게 알린 뒤 10월 [전체 다시 받기] 한 번 · 증분과 같은지(L15) ⑥ 에이전트별 수(L16) · 저장 파일(L17) · 엑셀 3종(L18) · 돈 경로 숫자(L19) ⑦ 사용자 화면 확인 · 피드백은 모아서 한 번에 | SPEC-001 §9.4 | 코디 · 사용자 · (수정) 각 워커 | `back/.env` · `back/data/`(gitignore · 커밋 안 함) | **L13 KOS 0** · **L14 증분 `kosCalls` ≪ full** · L15 ~ L19 통과(수 · 같음/다름만 기록) · 사용자 확인 | `cd back && uv run pytest -q` · `cd front && npm run build` | 일부 완료 → 3판 LIVE3 로 이어짐(9월 첫 받기 full 657 calls · `closed` · 다시 열기 · 재시작 · `refresh=new` KOS 0 · 엑셀 3종 200 · 11칸 · 수식 0) |

### 병렬 (2판)

```text
WP-BE2 ─────────────────────────┐
                                ├── WP-REVIEW2 ── WP-LIVE2(9월 1회 · 10월 full + 증분 + 전체 1회 → 사용자 확인)
WP-FE2(시안 v2 · 가짜 응답 먼저 ┘
       → WP-BE2 뒤 붙이기)
```

- back · front 파일이 겹치지 않는다 — 동시에. 레포 루트 `README.md` · `.gitignore` 는 WP-BE2 가 갖는다
- `labels` 두 표(back `labels.py` · front `labels.ts`)는 WP-BE2 가 front 1판 `labels.ts` 를 원본으로 옮기고, WP-FE2 가 결제 수단 이름을 더하면 BE2 에 같은 값을 알린다(코디가 중계 · REVIEW2 가 대조)

### 주의 (2판)

- **운영 KOS 는 WP-LIVE2 에서 코디만.** 9월 1회 · 10월 full 1회 + 증분 · 10월 [전체 다시 받기] 1회(L15 — 누르기 전 사용자에게 알림). 그 밖에 다시 부를 일이 생기면 그때마다 사용자에게 알린다
- `back/data/sales.sqlite3` 는 **운영 개인정보 파일**(이름 · 결제) — 커밋 · 복사 · 업로드 금지 · 마감 때 `git status --ignored` 로 보고 지울지 · 옮길지 사용자에게 묻는다(`back/.env` · `front/.env.local` 과 함께)
- 내려받은 엑셀 파일(L18)도 이름이 들어 있다 — 레포 · 리포트에 올리지 않고 확인 뒤 지운다
- 2판 열린 것(SPEC-001 §11 OQ-122 ~ OQ-131 · OQ-126 · OQ-130 은 닫힘 — 손님 셈 D-15 · 결제 손님 0 원 포함 · 엑셀 이름 안 가림)은 기본값으로 구현한다. OQ-123(증분 새 행 가르기 — 코디 판단 기본값)은 L15 · L19 · OQ-125 는 L16 결과와 함께 사용자에게 올린다

## 3판 — SPEC-001 0.4.3 (최종 결제만 · D-18)

### 계약 고정점 (3판에서 바뀐 것만 — 2판과 다르면 이것이 이긴다)

| 고정점 | 값 | SPEC-001 |
|---|---|---|
| 줄 | `lines[].kind` = **`item` 하나** · `REFUNDED` 품목 0 · `payment` · `cancel` · `spent` 줄 0 · `lines[].paymentType` 없어짐 · `at` 늘 `null` | §4.2 · §6.9 |
| 머리 · 합 기준 | `approvedTotal` 없앰 · **`netTotal` = 실결제(합 기준) = 품목이 이 달이면 품목 줄 합 · 품목이 다른 달이면 이 달 취소 합(음수 · 「앞 달 결제 취소」)** · `paymentsNet` = 이 달 ① 순액(⚠ 비교만) · 실결제 0 · 줄 0 묶음 = 숨김(`hiddenPurchases` · 손님 셈엔 포함) · `paidAt` · `paymentTypes` = 살아 있는 승인 — **받을 때 판정해 `month_purchases` 에 저장**(확정 달 머리 고정) · 수납 `canceledPayments` · `refundedItems` | §4.2 · §4.4 · §6.9 · OQ-132(코디 결정) |
| 셈 | `counts.canceledPayments` · `counts.refundedItems` · `counts.hiddenPurchases` · `counts.excludedItems`(`INITIALIZED` 등) 더함 · `paymentLines` · `reversalLines` 없어짐 · `agencies[].netTotal` · `agencyTotal.netTotal` 더함 | §4.2 · §6.8 |
| 품목 금액 | ② `cost.totalAmount` = **남은 실결제**(전액 환불 0 · 부분 환불 = 남은 금액 — 운영 수집본 392/392) · 「원래 금액」 · 「환불된 금액」 없음(KOS 에 없음) | §6.3 · OQ-102 · OQ-133 |
| ⚠ | `paymentsNet ≠ itemsTotal`(itemsHere 수납) | §6.4 · OQ-106 |
| 차례 | 0원 품목 = ② 차례에서 앞 유료 품목 바로 아래(부모 판정 아님) | §3.3 · OQ-135 |
| 화면 | 머리 「실결제」(음수 빨강) · 「취소 a · 환불 b」 · 「앞 달 결제 취소」(음수) · 실결제 0 · 줄 0 묶음 숨김(그리지 않음) · 빈 에이전시 탭 문구(손님 n · 결제 손님 m) · 배지 `결제 완료` · `부분 환불` · 건수 줄 「취소된 결제 a건 · 전액 환불 품목 b개」 · 안내 「받은 시점 기준 실결제」 · 에이전시 요약 실결제 합 — 시안 v1 · v2 와 다름(시안 고침 = 코디 · OQ-136) | §3 |
| 엑셀 | 행 = 최종 결제 품목 + **「앞 달 결제 취소」 음수 행** · 「품목 금액」 = 남은 금액 · **열 합 = 같은 화면 실결제 합** · 11칸 그대로 · 「정보」 시트에 취소된 결제 · 전액 환불 · 숨긴 수납 · 뺀 품목 수 · 실결제 합 | §4.7 |
| 증분(바뀜) | 이번 달 증분에서 **새 행이 생긴 `items_here` 저장 수납의 ② · ⑤ 를 다시 불러 `items` 갈아 끼움**(② 범위 1회 +1 · 같은 달 환불 · 재결제 반영) · 확정 달 품목 · 판정은 안 건드림 | §4.5 증분 5 |
| 저장(바뀜) | `month_purchases` 에 `paid_at_utc` · `payment_types` 더함 — `schema_version` 2 · 뜰 때 `ADD COLUMN`(KOS 0) · 빈 칸은 처음 읽을 때 저장본으로 채움 | §4.4 |
| 앞 달 결제 취소(0.4.2 · 0.4.3) | 품목이 다른 달인 수납의 이 달 취소 · 반환은 **품목 달 `items.fetched_at`(② 응답 받은 직후 시각 · 0.4.3) 이후(파싱한 시각 비교 · `at_utc` 없으면 `transactions.fetched_at`)인 것만** 음수로 더함 · **고정 수납 · 이 달 취소가 있는 수납은 이 달 살아 있는 승인도 더함**(달을 모두 더하면 KOS 최종 — 0.4.3) · 취소 없는 분할 나머지 = 0 · 그 전 것 = `counts.reflectedCancels`(이미 남은 금액에 반영) · 품목 달 저장 없음 = 음수 · 읽을 때 판정(확정 달 숫자도 품목 달 받기에 따라 맞는 쪽으로 바뀜) · 분할 결제는 품목 달에 전액 | §6.9 · §4.6 ⑧ |
| 그대로 | 그 밖 저장 · 증분 · 판정(§6.2 s1 ~ s5) · 잇기(§5.4) · 에이전시 판정 · 손님 셈(D-15 · D-16) · 경로 3 | — |

### Work Packages (3판)

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-BE3** | **실결제 · 최종 결제 줄 · 증분 ② 다시** — `service/sales.py`(줄 만들기: `ACCEPTED` · `PAID` · `PARTIALLY_REFUNDED` 만 · `REFUNDED` · `excludedItems` 셈 · 0원 차례 · `netTotal` 합 기준 · `paymentsNet` · 숨김 · 살아 있는 승인을 받을 때 판정해 저장 · `canceledPayments` · `refundedItems` · ⚠ 조건 · 에이전시 `netTotal` · **증분 5 (ii) 새 행 생긴 이 달 itemsHere 저장 수납 ② 다시 · `items` 갈아 끼움** · **0.4.2 앞 달 결제 취소 반영 판정 · `reflectedCancels` — §6.9 판정 함수 하나 안에**) · `repository/store.py`(schema 2 `ADD COLUMN` · 빈 칸 채움) · `schemas/sales.py`(필드 바꿈 — `approvedTotal` · `paymentLines` · `reversalLines` · `paymentType` 뺌) · `service/export.py`(행 = 품목 + 「앞 달 결제 취소」 음수 행 · 「정보」 시트 수 · 실결제 합) · `labels.py`(`결제 완료`) · 시험(옛 줄 단언을 0.4.0 규칙으로 · #45 ~ #53). 저장 표 변경 = `month_purchases` 칸 두 개(schema 2 · 뜰 때 `ADD COLUMN` · 그 밖 마이그레이션 없음 — 줄 · 합 · 반영 판정은 읽을 때 만든다) | SPEC-001 §4.2 · §4.7 · §6.3 · §6.4 · §6.8 · §6.9 · §3.3 | backend | `back/**` | §9.1 1 ~ 63 전부(0.4.0 읽는 법 · #61 ~ #63 = 앞 달 결제 취소 반영 판정) · 옛 줄 단언 grep 0(`kind` ≠ `item` · `approvedTotal` · `paymentType` — doc r5 NOTE-2) · 운영 · 데모 KOS 호출 0 | `cd back && uv run ruff check . && uv run pytest -q` | 완료(코드 PR #1 · 수정 1(code r3 F-1 · W-2) · 수정 2(이 달 취소 뒤 재승인) · pytest 149) |
| **WP-FE3** | **최종 결제 화면** — `lib/types.ts`(0.4.0) · 머리 실결제 · 「취소 a · 환불 b」 · 「앞 달 결제 취소」(음수) · 실결제 0 · 줄 0 묶음 숨김(그리지 않음) · 빈 에이전시 탭 문구(손님 n · 결제 손님 m) · 결제 · 취소 · 환불 줄 그리기 지움 · 배지 이름(`labels.ts` `결제 완료`) · 건수 줄 · 안내 문구 · 에이전시 요약 실결제 합 · `⚠ 통화 섞임` = `netTotal === null` · ⚠ 배지 = `paymentsNet ≠ itemsTotal` · 「앞 달 결제 취소」 머리 · 숨긴 수납 수(월별 건수 줄만) | SPEC-001 §3 · §4.2 · §9.3 | frontend | `front/**` | §9.3 0.4.0 줄 스크린샷(가짜 값) · tsc · lint · build 0 | `cd front && npx tsc --noEmit && npm run lint && npm run build` | 완료(코드 PR #1 · 수정 1(차례 = back · 「앞 달 결제 취소」 글자 · `itemsNowhere` 안 숨김) · tsc · lint 0) |
| **WP-REVIEW3** | reviewer: SPEC 0.4.2 ↔ 코드 — **「앞 달 결제 취소」 반영 판정(`items.fetched_at` vs 취소 시각 · 파싱 비교 · #61 ~ #63)** · 줄 = 최종 결제 품목만(`REFUNDED` · `INITIALIZED` · 결제 · 취소 줄 0) · `netTotal` 합 기준 · 엑셀 합 = 화면 합 · 숨김 · 증분 ② 다시(같은 달 환불 · 재결제) · 확정 달 안 건드림 · schema 2 · `paymentsNet` · 살아 있는 승인 · ⚠ 조건 · 0원 차례 · 엑셀 행 · 「정보」 수 · 에이전시 `netTotal` · 옛 필드 0(`approvedTotal` · `paymentType` · `kind≠item`) · 로그에 금액 0 | 3판 | reviewer | `back/**` · `front/**` | PASS | — | 완료(code r3 FAIL 1 · WARN 2 → BE · FE 수정 1 · 2 로 닫음 · SPEC 0.4.3 동기) |
| **WP-LIVE3** | **코디: 운영 10월 실물** — 커밋 뒤 back 재기동(schema 2 로 올라감 · KOS 0 · 9월은 읽기만 — KOS 0) · **10월 [새 결제 받기] 1회**(0.4.1 증분이 같은 달 환불 · 재결제를 품목에 반영 · `kosCalls` 기록 — 저장본이 없으면 LIVE2 순서로 먼저) · L20(⚠ 수 — **0**) · L21(「승인 → 전액 취소 → 같은 금액 재승인」 꼴 하나 · 「승인 → 전액 취소 → 다른 금액 재승인」 꼴 하나 — 실결제 = KOS 화면 최종 금액) · L22(부분 환불 하나 — 남은 금액) · L23(숫자 · 0원 차례) · L24(화면 합 = 엑셀 합 · 세 화면 · **두 달 합 = KOS 최종** — 9월 · 10월에 걸친 수납 하나) · 엑셀 1개 열어 확인 · 사용자 화면 확인 · 피드백 모아서 | SPEC-001 §9.4 L20 ~ L23 | 코디 · 사용자 | `back/data/`(gitignore) | L20 ⚠ 0 · L21 ~ L24 같음 · 사용자 확인 | `cd back && uv run pytest -q` · `cd front && npm run build` | 완료(10월 KOS 0 · ⚠ 0 · 9월 KOS 0 · ⚠ 1 = 앞 달 승인의 9월 취소 꼴(정상 · SPEC §6.4 OQ-106) · 확정 달 KOS 0 · 사용자 화면 확인) |

### 주의 (3판)

- 3판 저장 표 변경은 **`month_purchases` 칸 두 개 더하기뿐**(schema 2 · `ADD COLUMN` · KOS 0) — 2판 저장본(9월 · 10월)을 지우지 않는다. 9월(`closed`)은 KOS 를 다시 부르지 않는다. 10월(`current`)은 증분 한 번으로 같은 달 환불 · 재결제를 맞춘다. 확정 달 품목 금액은 받은 때 남은 금액(D-13)
- LIVE3 의 수납 id · 금액 · 이름은 레포 · 리포트에 적지 않는다(꼴 · 같음/다름 · 수만)
- 사용자 답 대기: OQ-132(합 기준 = 품목 실결제 합 + 앞 달 결제 취소 — 코디 결정 · 추천안 통보 · 답이 다르면 §6.9 · 엑셀 행 · #52 · #57 · L24 가 바뀐다) · 코디 몫: OQ-136(시안 v3) · planner 기본값: OQ-137(상태 경계)

