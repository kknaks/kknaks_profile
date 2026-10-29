---
type: work
id: WORK-001
title: "월별 매출 리스트 — 새 레포 agency-settlement · back(KOS 조회 전용 · 조인) → front(cc-prototype 디자인 복사) → 운영 KOS 10월 실물 조회 1회 (SPEC-001 0.2.1)"
status: draft
product: agency-settlement
feature: monthly-sales
work_type: feature
owner: kknaks
progress: 0
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
  - "cc-prototype procedure/ main(읽기만 — back app/kos/client.py · config.py · main.py · front 디자인 파일)"
---

# 월별 매출 리스트 — 빌드 계획

계약은 **SPEC-001 0.2.1**(전부) — 이 문서는 빌드 계획만 적고 계약을 다시 쓰지 않는다. 결정 = DEC-001.

## Meta

- Covers spec: SPEC-001 0.2.1
- 코드 레포: **`kknaksss/agency-settlement`**(private · 로컬 `/Users/kknaks/git/toy_pr2/agency-settlement` · 지금 `README.md` · `.gitignore` 만) — 범위 **`back/**` · `front/**` · `README.md`**. cc-prototype 레포는 읽기만(디자인 · KOS 클라이언트 복사 원본 — 그 레포엔 아무것도 쓰지 않는다) · R§2 별도 프로젝트 줄 · D1-08
- base: 코드 레포 `kknaksss/agency-settlement` `main` · 워크트리 · 브랜치는 코디가 정한다
- 워커: backend · frontend · reviewer · 코디(실물 조회)
- 검증은 WP 마다 그 범위만. 전체 검증(pytest 전부 · front build · 로컬 두 프로세스)은 WP-LIVE 에서 한 번
- **완료 = 운영 명동점 KOS 를 로컬에서 실제로 1회(10월) 조회해 리스트가 화면에 뜬 것**(SPEC-001 §9.2 L1 ~ L12). 가짜 응답 · 데모 지점으로 대신하지 않는다
- 배포 없음(D1-09) · infra 레포 변경 없음
- **운영 데이터** — 근거 `_RESUME` §2 운영 키 줄(10-29 확장 — 「이 프로젝트 코드 · WP-LIVE 실물 조회까지 같은 조건(조회만 · 로컬만)」). 운영 키는 `back/.env`(gitignore)에만 · 코디가 넣는다. **워커는 운영 키를 쓰지 않는다**(WP-BE · WP-FE 는 가짜 transport · 가짜 응답만). 문서 레포(kknaks_profile)는 public · 코드 레포는 private — 어느 쪽이든 실명 · 실제 금액 · 유입 이름 · 키 · 테넌트 id 를 커밋 · 리포트 · 스크린샷에 넣지 않는다

## 계약 고정점

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
| **WP-BE** | **back 전부** — `back/` 뼈대(uv · pyproject · ruff · pytest — cc-prototype procedure/back 과 같은 판) · `config.py`(env §10.1 · `back/.env` 하나) · `domain/{clock,errors}.py`(cc-prototype procedure 에서 복사) · `kos/client.py`(cc-prototype procedure `client.py` 의 **공개 토큰 · `_call` · `_error_of` 만 복사** + 조회 전용 가드 · 토큰은 메모리) · `service/sales.py`(월 경계 · 오프셋 파싱 · ①② cursor 끝까지 · ⑤ 100개씩 · 첫 승인 결제 고르기(전액 취소 뺌 · 대체 정렬) · ① 귀속 달 판정 · ① ↔ ⑤ 거래 잇기 · 결제일 = ⑤ 시각 · ③④ 동시 제한 · 「없음」 = 400 `NotFound` 만 · 이름 · 예약 시작만 꺼냄 · 묶음 · 줄 · 상태 · 상품명 · 통화 · 캐시 · 달별 잠금 · 토큰 잠금) · `api/sales.py` · `schemas/sales.py` · `main.py`(오류 처리기 · CORS GET 하나 · `no-store` · httpx 로그 WARNING) · `tests/`(KOS 가짜 transport) · `back/.env.example` · 레포 루트 `README.md`(실행 · env 채우기 더함) | SPEC-001 §2 · §4 · §5 · §6 · §7 · §10 | backend | `back/**` · `README.md` | SPEC-001 §9.1 1 ~ 24(9b 포함) 전부 통과 — **「없음」 시험은 가짜 응답을 400 + `NotFound` 꼴로**(404 로 「없음」을 시험하지 않는다 · 9b 의 「다른 reason 400 → 502」 · 「404 → 502」 포함) · `grep -rn "commands/" back/app` = 토큰 교환 상수 1줄 · `grep -rn "sign-in\|tenants/" back/app` = 0 · `git status --ignored` 에 `back/.env` 가 추적 안 됨 · **운영 · 데모 KOS 호출 0** | `cd back && uv run ruff check . && uv run pytest -q` | 대기 |
| **WP-FE** | **front 전부** — §8 복사 목록(tailwind · postcss · 테마 · 보정 · globals 일부 · layout · 로고 · `lib/time.ts` 일부 · `lib/api.ts` 의 `API_BASE` · `CONFIG_ERROR`) · `package.json`(medikit 1.4.0 · 포트 3800) · `lib/types.ts`(§4.2 그대로) · `lib/labels.ts`(품목 종류 · 상태 · 결제 수단 이름 — §6.3 표) · `app/page.tsx`(`?month=` · 기본 이번 달 KST) · `components/monthly/*`(월 선택 `[‹] [›]` · 다시 불러오기 · 건수 줄 · 수납 묶음 머리 · 품목 줄 · `payment` 줄 · 「품목은 다른 달에 · 첫 승인 MM-DD」 · 결제일 「시각 없음」 · 음수 줄 · `⚠ 결제 ≠ 품목` · `⚠ 통화 섞임` · `itemsMissing` 줄 · 「상태는 지금 기준」 안내 · 상태 화면 5종) · 복사 파일 머리 「원본:」 주석 | SPEC-001 §3 · §4.2 · §8 | frontend | `front/**` | 가짜 응답(§4.2 꼴 · 가짜 이름 `홍**` · 가짜 금액)으로 §3.4 상태 5종 · 묶음 · `payment` 줄 · 음수 줄 · 경고 배지 2종 스크린샷 · cc-prototype import 0(`grep -rn "procedure/\|cc-prototype" front --include=*.ts --include=*.tsx` = 「원본:」 주석만) · `localStorage` · `sessionStorage` 0 | `cd front && npx tsc --noEmit && npm run lint && npm run build` | 대기 (WP-BE 계약 고정점만 보고 화면 먼저 · 붙이기는 WP-BE 뒤) |
| **WP-REVIEW** | reviewer: SPEC-001 §1 ~ §10 ↔ 코드 · 부록 A · 경로 2 · 가드(허용 경로 5 · 내부 API 0 · 토큰 잠금) · 「없음」 판정 = 400 `NotFound` 만(404 · 다른 reason 은 `kos_rejected`) · ③ ④ 응답에서 이름 · 예약 시작 외 필드가 변수 · 캐시 · 로그에 안 남음 · 품목 줄 = 취소 안 된 첫 승인 결제 행의 ① 귀속 달 한 번(#22 ~ #24) · ⑤ 응답에서 꺼낼 필드만 남음(메모 · items 0) · 결제일 · 정렬이 ⑤ 시각(① `lastUpdatedPaymentDateTimeUtc` 가 응답 · 화면에 0) · 응답 키 = §4.2 · 자유 텍스트 필드(`…FunnelDetail` · 메모)가 응답 · 코드에서 안 읽힘 · 로그에 이름 · 금액 · id · 키 0 · `127.0.0.1` · `.env` 미추적 · cc-prototype import 0(복사만). FAIL 은 모아서 한 번에 수정 발주 | 전체 | reviewer | `back/**` · `front/**` · `README.md` | PASS | — | 대기 |
| **WP-LIVE** | **코디: 운영 KOS 실물 조회 1회(10월)** — 근거 `_RESUME` §2 운영 키 줄(10-29 확장). ① `back/.env` 에 운영 키(원본 ax-clinic-project `scripts/.env` 의 `KOS_API_tenent` — 이름만 · 값은 파일에서 옮김) · ② 전체 검증(pytest 전부 · front build) · ③ back `127.0.0.1:8800` · front `3800` 띄움(커밋 뒤 옛 프로세스 아님을 확인) · ④ 브라우저에서 `?month=2026-10` **한 번** · ⑤ §9.2 L1 ~ L12 기록(L10 = 환불 품목 수납 · L11 = 두 달에 걸친 수납 · 전액 취소 건너뛴 수납(a) · 대체 판정 수납(c) · L12 = 잇지 못한 거래 · 결제일이 달 밖인 행) · ⑥ L5 · L10 결과로 `⚠ 결제 ≠ 품목` 배지 문구 · 조건 제안(OQ-106) · ⑦ 사용자에게 화면 확인 요청 · 피드백은 모아서 한 번에 | SPEC-001 §9.2 | 코디 · 사용자 · (수정) 각 워커 | `back/.env`(gitignore · 커밋 안 함) | **L1 화면에 10월 리스트가 뜸** + L2 ~ L12 통과(수 · 같음/다름만 기록) · 사용자 확인 | `cd back && uv run pytest -q` · `cd front && npm run build` | 대기 |

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
