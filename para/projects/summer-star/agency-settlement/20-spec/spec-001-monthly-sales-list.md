---
type: spec
id: SPEC-001
title: "월별 매출 리스트 — 운영 명동점 KOS 결제를 월 단위 · 수납별 묶음 · 품목 한 줄씩 · 에이전트별 조회 · SQLite 저장 · 증분 조회 · 엑셀 내보내기 · 조회 전용 · 로컬만"
version: 0.4.3
status: draft
product: agency-settlement
feature: monthly-sales
created_at: 2026-10-29
updated_at: 2026-10-29
tags:
  - product/agency-settlement
  - feature/monthly-sales
  - doc/spec
  - status/draft
links:
  baselines: []
  decisions:
    - "[[decision-001-monthly-sales-list|DEC-001]]"
  specs: []
  works:
    - "[[work-001-monthly-sales-list|WORK-001]]"
  releases: []
  related:
    - "[[no-inference-from-free-text]]"
up: []
sources:
  - "para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md (D-01 ~ D-18 · 열린 것)"
  - "orchestration/work/agency-settlement/_RESUME.md §2 — 2026-10-29 줄 전부(결정 원천 · DEC-001 와 다르면 이쪽 · 0.1.1 = 운영 키 확장 · ③ 작업 정정 · 분할 결제 줄 · 0.1.2 = ⑤ 추가 승인 · 결제일 원천 줄 · 0.2.0 = 별도 프로젝트 줄 · 0.3.0 = 시안 v1 채택 · 에이전트별 · SQLite · 받은 시점 · 시안 v2 채택(정할 것) · 엑셀 줄 · 0.3.1 = 손님 셈 visitorId 줄 · 0.4.0 = 결제 손님 0원 · 엑셀 이름 · 증분 해석 · D-18 정정(최종 결제만) 줄)"
  - "orchestration/work/agency-settlement/research-agency-attribution.md — Q1 · Q3 ~ Q6(필드 경로 · 결제/취소 모양 · 연결 근거)"
  - "orchestration/work/agency-settlement/review-spec-007-report.md — 0.1.0 검수(F-1 · W-1 ~ W-6 · NOTE 1 ~ 5)"
  - "orchestration/work/agency-settlement/planner-fix-1-instructions.md — 수정 1판 지시(444 일치의 정의 포함)"
  - "orchestration/work/agency-settlement/planner-fix-2-instructions.md — 수정 2판 지시(⑤ 승인 · OQ-104 닫음)"
  - "orchestration/work/agency-settlement/planner-fix-3-instructions.md — 수정 3판 지시(별도 프로젝트 · 번호 재부여)"
  - "orchestration/work/agency-settlement/review-spec-001-r2-report.md — 0.2.0 재검수(W-1 첫 승인 달 구멍 3 · W-2 sources 경로 · NOTE 1 · 2 · 6 · 7)"
  - "orchestration/work/agency-settlement/planner-fix-4-instructions.md — 수정 4판 지시(첫 승인 달 = 취소 안 된 첫 승인 결제 행의 ① 귀속 달)"
  - "orchestration/work/agency-settlement/review-code-r1-report.md — code r1(W-1 · W-3 · W-5 · W-6 = SPEC 정리 몫 · 0.3.0)"
  - "orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v1.dc.html · design-report.md — 시안 v1(D-10 채택 · 「정할 것」)"
  - "orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v2.dc.html · design-v2-report.md — 시안 v2(채택 · 12장면 · 「정할 것」 — 값은 R§2 시안 v2 줄)"
  - "orchestration/work/agency-settlement/planner-v3-add-excel.md — 0.3.0 추가 지시(엑셀 · D-14)"
  - "운영 명동점 수집본 2026-10-28T17213*(ax-clinic-project kos-raw · 읽기만 · 레포 밖) — getPurchaseItemStatistics · getPurchaseSummaries · getTransactionStatistics 필드 대조(0.4.0 부분 환불 금액 · 0원 품목 차례 — 건수만 · 이름 · 금액 · id 는 적지 않음)"
  - "orchestration/work/agency-settlement/review-doc-r3-report.md · planner-v3-fix-1-instructions.md — doc r3(F-1 ~ F-3 · W-1 ~ W-8 · NOTE 1 ~ 7) · 0.3.1 수정 지시"
  - "agency-settlement 코드 워크트리 back/app/service/sales.py · config.py · schemas/sales.py · README.md(읽기만 — 0.3.0 기준 구현 · 수정 1판 반영본)"
  - "reference/2026-10-12-cc-prototype/kos-demo-api.md §1.2 · §2 · §3.1 · §3.3 · §3.4(작업표 · 인증 · 응답 감싸기)"
  - "https://developers.kos-solution.com/openapi.yaml 1.0.1 · 작업 77(2026-10-29 받음) — 요청 · 응답 스키마 · 「에러 응답」 · 「호출 한도」"
  - "cc-prototype procedure/ main(읽기만 — back app/kos/client.py · app/config.py · app/domain/{clock,errors}.py · app/service/kos_errors.py · front tailwind.config.ts · app/layout.tsx · app/globals.css · app/styles/* · lib/{api,time}.ts · package.json)"
  - "ax-clinic-project scripts/kos_collect.py(읽기만 — 운영 키 이름 · 조회 전용 가드 모양 · 키 값은 읽지 않음)"
---

# 월별 매출 리스트 계약

> 운영 명동점 KOS 의 결제를 **월 단위로 조회**해 **수납별로 묶고 품목 한 줄씩** 보여 주는 로컬 페이지다. 병원 · 에이전시 수수료 정산의 첫 판이고, 이번 판은 **리스트 + 에이전트별 조회 + 엑셀 내보내기**다(DEC-001 D-01 · D-11 · D-14). 받은 데이터는 back 의 SQLite 에 저장하고 지난 달은 다시 부르지 않는다(D-12).
>
> SSOT 순서(이기는 순): ① `_RESUME` §2 의 10-29 줄 ② DEC-001 ③ 이 문서 ④ 조사 리포트(사실) ⑤ 공식 스펙(필드 이름 · 뜻). **화면 정본 = 시안 v1(`Ceramique 월별 매출 v1.dc.html` · D-10) + 시안 v2(`Ceramique 월별 매출 v2.dc.html` · 채택 — 에이전시 탭 · 저장 상태 · R§2 시안 v2 줄)**. 이 문서는 화면의 계약(무엇이 보이나 · 어느 필드인가 · 언제 KOS 를 부르나)만 갖고, 배치 · 간격 · 색 · 문구 세부는 시안 대로다(§3).
>
> 근거 표기: `D1-nn` = DEC-001 결정 줄 · `R§2` = `_RESUME` §2 10-29 줄(괄호 안에 어느 줄인지) · `Qn` = 조사 리포트 질문 절 · `스펙` = openapi 1.0.1 스키마(이름을 같이 적음) · `KA§` = `kos-demo-api.md` 절 · `코드` = cc-prototype procedure 구현(읽기만) · `검수` = 0.1.0 검수 리포트 항목 · **`기본값`** = 결정에 없어 이 문서가 고른 값(§11 OQ 에 같이 올림).
>
> **이 레포는 public** — 키 · 토큰 값 · 테넌트 id · 실명 · 실제 매출 금액 · 에이전시 이름을 쓰지 않는다. env 는 이름만, 예시는 가짜 값(`홍**` · `1,000,000`) · 유입은 「(에이전시) 코드」로 쓴다.
>
> **0.1.1(2026-10-29)** — 검수 FAIL 1 · WARN 6 반영: 「없음」 = KOS 400 + `NotFound`(F-1) · ③ 작업 확정 · OQ-103 닫음(W-1) · 운영 키 근거(W-2) · **분할 결제 품목 줄은 첫 승인 달에만 + ⑤ `getPurchaseSummaries`**(W-3) · L10 · L11 · 환불 품목 금액 기본값(W-4) · `currency`(W-5) · 배지 조건은 실물 뒤(W-6) · NOTE 2 ~ 5.
>
> **0.1.2(2026-10-29)** — ⑤ `getPurchaseSummaries` 승인(R§2 ⑤ 줄) · **OQ-104 닫음: 결제일 = ⑤ `paymentDateTime.approvedDateTimeUtc` · 취소 줄 = `canceledDateTimeUtc` · 반환 줄 = `spentDateTimeUtc`** · ① `lastUpdatedPaymentDateTimeUtc` 는 보이지도 정렬하지도 않는다 · ① 행 ↔ ⑤ 거래 잇기(§5.4) · 달 귀속과 결제일이 다를 때 OQ-119 · 시험 #21 · L12.
>
> **0.2.0(2026-10-29)** — **구조 변경**: cc-prototype 의 기능 폴더(`sales/`)가 아니라 **별도 프로젝트 `agency-settlement`**(코드 레포 `kknaksss/agency-settlement` · 루트에 `back/` · `front/`)다(R§2 별도 프로젝트 줄 · D1-08). 문서 번호 DEC-001 · SPEC-001 · WORK-001 · OQ-1nn 으로 바뀜. cc-prototype 은 디자인 · KOS 클라이언트 본보기로 읽기만. 계약(API · 규칙 · 시험)은 0.1.2 와 같다.
>
> **0.2.1(2026-10-29)** — 재검수 W-1 · W-2: **「품목 줄은 그 수납의 *취소 안 된 첫 승인 결제 행*이 ① 로 귀속된 달에 나온다」**(§6.2) — 전액 취소된 승인은 첫 승인에서 뺌(a) · 달 판정은 ① 귀속 시계 하나(b) · ⑤ 시각이 없을 때도 같은 규칙 + `firstApprovedUnknown`(c) · 시험 #22 ~ #24 · L11 확장 · sources 경로. NOTE 1(시각은 파싱해 초 단위 비교) · 2(⑤ 에서 꺼낼 것만) · 6 · 7 반영.
>
> **0.3.0(2026-10-29)** — DEC-001 D-10 ~ D-13: **저장 · 증분(§4.4 · §4.5 — SQLite · 지난 달 = 한 번 받고 끝 · 이번 달 = 마지막 받은 시각 − 겹침 여유 이후 ① 만 · `refresh=new|full`)** · **에이전트별 조회(§3.5 · §4.2 `agency` · `agencies` — 같은 응답을 front 가 거름 · 판정 = 최초 유입 채널 이름 끝 「(에이전시)」)** · 화면 = 시안 v1 · v2(헤더 메뉴 · 넓은 폭 · 「받은 시점 기준」 · 마지막 받은 시각 · 이번 달/지난 달 버튼 — §3.1) · 메모리 캐시(OQ-105) 대체 · **엑셀 내보내기(D-14 — §3.6 · §4.7 `GET /api/sales.xlsx` · 저장본으로만 · KOS 0)** · 시안 v2 채택 · 정할 것(R§2 시안 v2 줄) · code r1 SPEC 정리(W-3 §5.4 · W-1 §6.2 · W-5 §6.7 · W-6 §10.1) · 시험 #12 고침 · #25 ~ #40 · L13 ~ L18 · OQ-122 ~ OQ-131.
>
> **0.3.1(2026-10-29)** — doc r3 FAIL 3 · WARN 8: **손님 셈 = `visitorId`(D-15 · F-1 — §6.8 · #35 · OQ-126 닫음)** · **증분 = ① 달 전체 1회 + 묶음 키 수로 새 행(F-2 · W-7 — §4.5 · #27 · OQ-123)** · **전체 받기 갈아 끼우기 범위(F-3 — `items` 는 이 달 itemsHere 수납만 · #31)** · 품목 달 고정 확인을 쓰기 트랜잭션 안에서(W-1 · #41) · `itemsNowhere`(W-2 · #42) · 증분에서 itemsHere 가 바뀐 수납도 ②(W-3 · #43) · 줄 선 요청은 저장본만(W-4 · #12) · 엑셀 글자 셀(W-5 · #38) · `data/` 700 · umask 077 · `-wal` · `-shm` 600 · 경로 규칙(W-6 · #36) · NOTE 1 · 2 · 3 · 5 · 6 · L19(돈 경로 숫자). 같은 날 사용자 결정 2개: 결제 손님에 0 원 · 순액 0 이하 포함(OQ-126 닫음) · 엑셀 이름 안 가림(OQ-130 닫음).
>
> **0.4.0(2026-10-29)** — **D-18(정정) 최종 결제만 보인다**: 수납 머리 = 그달 **실결제**(① 승인 + 취소 · 반환 음수 — §6.9) · 줄 = **최종 결제된 품목만**(결제 완료 · 부분 환불은 남은 금액) · **취소된 결제 · 전액 환불 품목 · 결제 · 취소 · 반환 행은 줄로 그리지 않는다**(건수만 — 건수 줄 · 「정보」 시트) · `lines[].kind` 는 `item` 하나 · `approvedTotal` → `netTotal` · `⚠ 결제 ≠ 품목` = 실결제 vs 품목 합 · 에이전시 실결제 합 `netTotal` · 0원 품목은 앞 유료 품목 바로 아래(§3.3) · **부분 환불 금액 = ② `cost.totalAmount`(남은 금액) — 운영 수집본 대조로 찾음 · OQ-102 뒤집어 닫음**(§6.3) · 엑셀 「품목 금액」 = 남은 실결제 · 시험 #45 ~ #53 · L20 ~ L23 · OQ-132 ~ OQ-136. D-16(결제 손님 0원 포함) · D-17(엑셀 이름 안 가림)은 0.3.1 에 이미 반영.
>
> **0.4.1(2026-10-29)** — doc r5 FAIL 2 · WARN: **증분이 새 행이 생긴 이번 달 저장 수납의 ② · ⑤ 를 다시 불러 품목을 갈아 끼움**(F-1 — 같은 달 환불 · 재결제 · §4.5 증분 5 · #54 ~ #56) · **합 기준 = 품목 실결제 합 + 앞 달 결제의 이 달 취소(음수)**(F-2 · OQ-132 코디 결정 — `netTotal` 뜻 바뀜 · 옛 「① 순액」은 `paymentsNet`(⚠ 비교만) · 엑셀 「앞 달 결제 취소」 음수 행 · #57) · 실결제 0 · 줄 0 묶음 숨김 `hiddenPurchases`(W-1 · #58) · 살아 있는 승인 판정을 받을 때 저장(W-2 · #59) · `INITIALIZED` 등은 줄 · 합에서 빼고 `excludedItems`(W-4 · #60 · OQ-137).
>
> **0.4.2(2026-10-29)** — doc r6 F-1 · WARN 5(구현 전 마지막 · 재검수 없음): **「앞 달 결제 취소」 음수는 품목 달 `items` 를 받은 뒤에 생긴 취소만**(이미 남은 금액에 반영된 취소는 `counts.reflectedCancels` 로만 · 다른 달 환불이 두 번 빠지는 길 0 · §6.9 · §4.6 ⑧ · #61 ~ #63 · L24) · 분할 결제 나머지는 품목 달에 전액(W-1 · OQ-132 알림 · L20 「분할 나머지」 따로 셈) · WORK · §9.3 의 「전액 환불 b개」 줄 · 「마이그레이션 없음」 정리(W-2) · schema 2 빈 칸 채우기 = 「지금 ⑤」로 한 번(W-3 · §4.6 ⑨) · 숨긴 수납만 있는 에이전시 탭 = 빈 탭 문구(W-4 · §3.5) · OQ-132 답이 바뀌면 고칠 곳 = §6.9 판정 하나(W-5).
>
> **0.4.3(2026-10-29)** — **구현 뒤 동기(코드 PR kknaksss/agency-settlement#1 · 커밋 `2b299dc` 가 정본 · 새 정책 없음)**: 원칙 「**달을 모두 더하면 KOS 최종 금액**」(R§2 마지막 줄) — 품목이 다른 달인 수납이 **품목 달에 고정됐거나(`pinned_elsewhere` · code r3 F-1) 이 달에 취소가 있으면** 이 달 실결제 = 이 달 살아 있는 승인 + 반영 안 된 취소(be3-fix-2) · 취소 없는 분할 나머지만 0(§6.9) · 반영 판정 기준 = **② 응답을 받은 직후 시각**(code r3 W-2) · `itemsNowhere` 는 숨기지 않음(NOTE-1) · 묶음 차례 = back 응답 차례(front 다시 정렬 안 함) · 「앞 달 결제 취소」 머리 결제일 칸 = 그 글자(`paidAt` 은 `null` 그대로 · code r3 W-1) · 폭 = 가운데 1600 · 증분 「바뀜」 갈아 끼움(code r2 W-1) · 로그 `changedPurchases` · `repaidAfterCancel` · 「정보」 시트 괄호 정리(NOTE-3) · OQ-132 · OQ-136 상태 · 시험 #27(g) · #64 ~ #67.

## 1. 범위

### 1.1 In

| 무엇 | 근거 |
|---|---|
| 별도 프로젝트 코드 레포 **`kknaksss/agency-settlement`** — 루트에 `back/`(FastAPI) + `front/`(Next.js) · cc-prototype 은 읽기만(복사 원본) | D1-08 · R§2(별도 프로젝트 줄) |
| 화면 둘(헤더 메뉴 「월별 조회 \| 에이전트별 조회」) — 월 선택 · 수납별 묶음 · 품목 줄 · 칸(D-03) · 상태 · 빈 달 · 불러오는 중 · 오류 · 저장 상태(§3) · 화면 세부 = 시안 v1 · v2 | D1-01 · D1-02 · D1-03 · D1-10 · D1-11 |
| 에이전트별 조회 — 탭 「에이전시 전체」 + 에이전시마다 탭 · 손님 수 · 결제 손님 수(§3.5 · §6.8) | D1-11 |
| back API — `GET /api/sales`(§4 · 에이전시 판정 · 요약을 같은 응답에) + **`GET /api/sales.xlsx`**(§4.7 · 엑셀) | D1-01 · D1-05 · D1-11 · D1-14 |
| **엑셀 내보내기** — 지금 보는 화면(월 + 탭) 그대로 품목 한 줄씩 펼친 xlsx · 저장본으로만(§3.6 · §4.7) | **D1-14** · R§2(엑셀 줄) |
| **SQLite 저장 · 증분 조회**(§4.4 · §4.5) — 지난 달 = 한 번 받고 끝 · 이번 달 = 마지막 받은 시각 이후만 · 전체 다시 받기는 사람이 누를 때만 | D1-12 · D1-13 |
| KOS 원천 매핑 — 칸마다 작업 · 필드 · 조인 키(§5) | D1-05 · R§2(원천 줄) · Q5 · Q6 |
| 규칙 — 월 경계(KST) · 수납 포함 · 분할 결제 · 취소 · 환불 · 선불카드 · 상품명 빈 품목 · 유입 빈 값 · 통화(§6) | D1-04 · D1-06 · D1-07 · R§2(분할 결제 줄) |
| 조회 전용 가드 · 개인정보 · 로그(§7) | D1-05 · D1-09 · R§2(운영 키 줄) · `kos_collect.py` |
| 디자인 복사 목록(§8) · 검증(§9) · env · 로컬 실행(§10) | D1-08 · D1-09 |

### 1.2 Out (이번 판 밖 — 다음 판은 OQ 로만)

| 무엇 | 근거 |
|---|---|
| 수수료율(상품별) · 수수료 계산 | D1-01 · DEC-001 열린 것 · OQ-112 |
| 에이전시 확인 절차 · 유입 필터(에이전시 말고 다른 유입으로 거르기) · 「에이전시 코드 집합」 같은 목록 관리(판정은 이름 끝 「(에이전시)」 하나 — §6.8) | D1-01 · D1-11 · OQ-112 · OQ-125 |
| CSV · 엑셀 밖 형식 · 엑셀 합계 행 · 수수료 칸 | D1-14(xlsx 하나) · D1-01 |
| 배포 · 외부 접속 · 로그인 | D1-09 · R§2(운영 키 줄 「로컬만」) · OQ-110 |
| KOS 쓰기(`/commands/` — 토큰 교환 하나 빼고) | D1-05 · R§2(운영 키 줄 「조회만」) |
| 월 금액 합계 · 에이전시별 금액 합 · 선불카드 충전 · 사용 이중 계산 거르기(에이전시 요약은 사람 수 · 수납 수만 — §6.8) | D1-01 · D1-07(「뒤의 필터가 정한다」) · D1-11 「수수료는 다음 판」 |
| 메모 · 상세 유입(`…FunnelDetail`) 같은 자유 텍스트로 에이전시 짐작 | D1-04 · [[no-inference-from-free-text]] |
| KOS 원본 응답(JSON) 저장 · 전화 · 생년월일 · 메모 등 이름 밖 개인정보 저장(§4.4 — 줄인 필드만) | D1-12 · §7.3 |
| 자동으로 지난 달을 다시 받기(지난 달은 [전체 다시 받기] 를 누를 때만) | D1-12 |

## 2. 폴더 · 실행 모양

```text
agency-settlement/          # 코드 레포 kknaksss/agency-settlement(private) 루트
├── README.md               # 이미 있음 — 실행 · env 채우기(§10)를 더한다
├── .gitignore              # 이미 있음 — .env · .env.* (! .env.example) · node_modules · .next · .venv · **0.3.0 더함: `back/data/` · `*.sqlite3*`**
├── back/                   # FastAPI · Python 3.12 · uv(cc-prototype procedure/back 과 같은 도구)
│   ├── .env.example        # 이름만 — 복사해 back/.env(gitignore)
│   ├── data/               # 0.3.0 — SQLite 파일 자리(기본 `data/sales.sqlite3` · gitignore · §4.4)
│   ├── app/
│   │   ├── main.py         # create_app 팩토리 · 오류 처리기 · CORS
│   │   ├── config.py       # Settings(env 로만)
│   │   ├── api/sales.py    # router — GET /api/sales · GET /api/sales.xlsx(0.3.0) · GET /api/health
│   │   ├── service/export.py     # 0.3.0 — 저장본 → xlsx(openpyxl · §4.7) · service/labels.py(한글 이름 표)
│   │   ├── service/sales.py      # 월 경계 · 조인 · 줄 만들기 · 저장 · 증분 판단(§4.5) · 에이전시 판정(§6.8)
│   │   ├── repository/store.py   # 0.3.0 — SQLite(표준 `sqlite3` · ORM 없음) · 표 만들기 · 읽기 · 한 트랜잭션 쓰기(§4.4)
│   │   ├── kos/client.py   # 공개 토큰 교환 + 조회 전용 가드(§7.1)
│   │   ├── domain/{clock,errors}.py
│   │   └── schemas/sales.py      # 응답 모델(§4.2 — front 계약)
│   └── tests/              # KOS 가짜 transport
└── front/                  # Next.js · cc-prototype procedure/front 디자인 복사(§8)
    ├── app/{layout.tsx,page.tsx,agency/page.tsx,globals.css,styles/}   # 0.3.0 — /agency 더함(§3.5)
    ├── components/{common,monthly,agency}/   # 헤더 메뉴 · 월 선택 · 수납 묶음 · 줄 · 에이전시 탭
    └── lib/{api.ts,time.ts,types.ts,labels.ts}
```

- 계층은 cc-prototype `procedure/back` 모양 그대로 — router → service → kos client · **repository(SQLite — 0.3.0)** · 아래층은 HTTP 를 모르고 도메인 예외만 던진다(코드 `domain/errors.py`). SQL 은 repository 밖으로 나가지 않는다 · 서비스는 dataclass 로만 주고받는다 · 기본값(OQ-111 · OQ-122)
- cc-prototype 레포는 **읽기만** — 그 파일은 **복사**한다(import · 심볼릭 링크 · 공용 패키지 · git submodule 금지 — D1-08 「import 금지」). cc-prototype 레포에는 아무것도 쓰지 않는다
- 컨테이너 · compose 없음 — back 은 `uv run` · front 는 `npm run dev` 두 줄(§10.2) · 기본값(OQ-111)
- 레포 루트 `README.md`(이미 있음)에 실행 · env 채우기를 더한다

## 3. 화면

**화면 정본 = 시안 v1 · v2**(D1-10 — claude design `dda9a931` 「Ceramique 월별 매출 v1.dc.html」 · v2 는 같은 프로젝트의 「v2」 파일 · 로컬 사본 `orchestration/work/agency-settlement/design-upload/`). 아래 표는 **무엇이 보이고 어느 필드에서 오나**만 정한다 — 배치 · 간격 · 색 · 아이콘 · 문구의 세부는 시안 대로, 시안과 이 문서가 다르면 **값 · 필드 · KOS 호출은 이 문서, 모양은 시안**이 이긴다. 데스크 브라우저 · 화면 좌우를 넓게(본문 폭 제한 없음 · 1440 ~ 1920 에서 표가 화면을 채움 — 시안 v1) · D1-10.

### 3.1 틀

| 자리 | 계약 | 근거 |
|---|---|---|
| 헤더 | 로고 + **메뉴 「월별 조회 \| 에이전트별 조회」**(고른 메뉴 강조) · 오른쪽 지점 이름 + 「운영 · 조회 전용」 칩. 로그인 · 로그아웃 없음. 주소 = 월별 `/` · 에이전트별 `/agency`(§3.5) — 메뉴를 바꿔도 `?month=` 는 이어 간다 | D1-10 · D1-05 · D1-09 · 시안 v1 |
| 폭 | **본문 · 헤더 안쪽 최대 폭 1600px · 가운데**(0.4.3 — 2판 수정 1 사용자 지적 · 구현본이 정본 · 시안 v1 의 「폭 제한 없음」을 바꿈). 유입 · 상품 · 옵션은 한 줄 + 넘치면 말줄임 · 전체는 `title` | D1-10 · 시안 v1 |
| 월 선택 | `[‹]  2026년 10월  [›]` — 앞 · 뒤 달로 한 칸씩. **이번 달(KST)보다 뒤는 못 고른다**(`[›]` 꺼짐). 앞쪽 끝은 두지 않는다 | D1-01 · 기본값(OQ-107) |
| 기본 달 | 주소 `?month=YYYY-MM` 이 있으면 그 달, 없으면 **이번 달(KST)**. 달을 바꾸면 주소도 바뀐다(새로고침 · 공유 때 같은 달) | D1-01 「기본 = 이번 달」 |
| 저장 상태 · 받기 버튼 | 응답 `store.state`(§4.2)로 가른다. **`current`(이번 달 · 아직 확정 아님)** = `[새 결제 받기]`(`refresh=new` — 마지막 받은 시각 이후만 · §4.5) + 작게 `[전체 다시 받기]`. **`closed`(지난 달 · 확정)** = 「확정 · 저장됨」 표시 + 작게 `[전체 다시 받기]` 만(새 결제 받기 없음 — 다시 부르지 않는다). `[전체 다시 받기]`(`refresh=full`)는 누르면 확인 한 번(「이 달을 KOS 에서 처음부터 다시 받아요 — 수십 초 걸려요」) 뒤 부른다 | **D1-12**(「지난 달 = 다시 안 부른다 · 전체 다시 받기는 사람이 누를 때만」) · 시안 v2 · **R§2 시안 v2 줄**(「이번 달에도 작게 · 확인 1번」) |
| 마지막 받은 시각 | 「MM-DD HH:mm 받음」(KST) = `store.fetchedAt` — **이 요청이 KOS 를 불렀든 저장본을 읽었든** 그 달을 KOS 에서 마지막으로 받은 시각. 이 요청에서 새로 받은 결제가 있으면 옆에 「새 결제 N」(= `fetch.newTransactions`). **증분인데 0 건이면 「새 결제 없음 · HH:MM 확인」**(HH:MM = `store.fetchedAt`) | D1-12 · 시안 v2 · R§2 시안 v2 줄 |
| 「새로 받음」 배지 | 그달 **마지막 받기가 증분**이고 그 받기로 처음 저장된 수납(`purchases[].newInLastFetch = true`)의 묶음 머리에 배지. **다음 받기 전까지** 붙는다(저장된 값이라 화면을 떠났다 와도 같음 · 전체 받기 뒤엔 0). J6 으로 저절로 한 증분도 「다음 받기」라 배지가 사람 손 없이 바뀔 수 있다(doc r3 NOTE-6 — 그대로 둔다) | 시안 v2 · R§2 시안 v2 줄(「다음 받기 전까지」) |
| [엑셀 내보내기] | 툴바 오른쪽 끝 버튼 하나(시안 v2 에 없음 — v2 툴바 버튼 모양을 따른다) · §3.6 | **D1-14** · R§2(엑셀 줄 「버튼 툴바 오른쪽」) |
| 건수 줄 | 「수납 N건 · 품목 M줄」 + 회색으로 「취소된 결제 a건 · 전액 환불 품목 b개 · 숨긴 수납 h · 앞 달 품목에 반영된 취소 r」(r = `reflectedCancels` · 0 이면 안 보임 · 0.4.2)(+ 제외 n — 0.4.1 `hiddenPurchases` · §6.9) — 취소 · 환불은 **숫자로만**(줄 없음 · 0.4.0 · D1-18). **월 금액 합은 보이지 않는다**(합계는 이번 판 밖) | D1-18 · D1-01 · 기본값(OQ-108) |
| 안내 한 줄 | 「금액은 **받은 시점 기준 실결제**예요 — 취소 · 전액 환불은 줄로 보이지 않아요 · 그 뒤 다른 달의 환불은 그 달 실결제에서 빠져요」(§6.9 · D1-13 · D1-18) | **D1-13** · **D1-18** · 시안 v2 문구를 바꿈(OQ-136) |
| 표 | §3.2 · 정렬 §3.3 | D1-02 · D1-03 |

### 3.2 표 — 수납 묶음 · 품목 줄

**한 줄 = 최종 결제된 품목 하나 · 같은 수납의 품목은 묶어 보인다**(D1-02 · **D1-18**). 묶음 머리 = 수납 단위 칸 + **실결제**, 그 아래 줄(들여 쓴 두 번째 층 — 시안 v1) = 품목 단위 칸(품목 줄은 그 수납의 **첫 승인 결제가 있는 달에만** — §6.2). **결제 · 취소 · 반환 줄은 없다**(0.4.0 — 1 · 2판의 `payment` · `cancel` · `spent` 줄 · 시안의 결제 · 취소 줄은 그리지 않는다) · **전액 환불 품목(`REFUNDED`) 줄도 없다**(건수만 · §6.9). 금액 0 인 결제 완료 품목(구성품)은 보인다 — 흐리게 · 앞 유료 품목 바로 아래(§3.3 · 시안 v1).

| 칸 | 단위 | 보이는 값 | 근거 |
|---|---|---|---|
| 결제일 | 수납(머리) | `MM-DD HH:mm`(KST). 머리 = 그달 그 수납 **살아 있는 승인 결제**(전액 취소되지 않은 승인 — §6.9)의 **⑤ 승인 일시 중 가장 이른 것** · 살아 있는 승인이 없으면 그달 첫 승인(응답 `paidAt` — 받을 때 저장한 값 · §6.9). **그달 승인이 없는 「앞 달 결제 취소」 머리는 `paidAt = null` 이고 결제일 칸에 빨간 글자 「앞 달 결제 취소」**(0.4.3 — code r3 W-1 · 시각은 엑셀 행에만). 그 밖에 ⑤ 와 잇지 못하면 `—` + 흐린 「시각 없음」(§5.4). 품목 줄에는 결제일이 없다 | D1-03 · D1-06 · D1-18 · R§2(⑤ 줄) · §5.4 |
| 손님 이름 | 수납 | 이름 그대로(가리지 않는다 — 병원 내부 화면). 못 찾으면 `—` + 흐린 「이름 없음」 | D1-03 |
| 방문일 | 수납 | `MM-DD`(KST) — 그 수납이 걸린 일정의 예약 시작 날짜(`reservation.startDateTime`). 없으면 `—` | D1-03 · R§2(원천 줄) · §5.2 |
| 최초 유입 채널 | 수납 | `visitorFunnelName` 문자열 그대로. 비면 `(없음)` 회색 · 에이전시 값(`agency ≠ null` — §6.8)은 강조(시안 v1) | D1-04 · §6.6 · §6.8 |
| 수납 | 수납 | 수납 id **끝 6자리** + 결제 수단 칩(참고 · 예: `카드` `현금` · 분할이면 칩 여러 개 · 이름은 front `lib/labels.ts` — KOS `TransactionPaymentType` 마다 한글 이름 · 모르는 값은 그대로) | D1-02 「결제 수단 · 분할 결제는 수납 단위 참고로만」 · 시안 v1 · 기본값(OQ-113) |
| 품목 종류 | 품목 | `상품` · `기타 상품` · `선불카드` | D1-07 |
| 상품 | 품목 | 상품명(§6.5 — 비면 선불카드명 · 기타 상품명) | D1-03 · D1-07 |
| 옵션 | 품목 | 상품 옵션명 · 없으면 `—` | D1-03 |
| 품목 금액 | 품목 | **남은 실결제** = ② `cost.totalAmount`(부분 환불이면 남은 금액 · §6.3) · `1,000,000`(원 · 천 단위 쉼표 · 오른쪽 정렬) · 음수 없음. 통화가 `KRW` 가 아니면 숫자 뒤에 통화 코드(§6.7) | D1-02 · **D1-18** · §6.3 |
| 상태 | 품목 | 배지 — `결제 완료`(`ACCEPTED` · `PAID`) · `부분 환불`(남은 금액만 보임 — 환불된 금액 · 원래 금액은 보이지 않는다 · OQ-133) 만 — `환불`(`REFUNDED`)은 줄이 없어 배지도 없고, `INITIALIZED`(미수납) · 그 밖 상태도 줄이 없다(0.4.1 · `excludedItems` · OQ-137) | D1-03 · **D1-18** · 스펙 |

- 묶음 머리 오른쪽 끝에 **「실결제 1,000,000」**(`netTotal` — §6.9 합 기준: 품목이 이 달이면 품목 줄 합 · 품목이 다른 달이면 이 달 취소 합(음수) · D1-18). 품목 줄이 있는 묶음에서 **결제 순액 ≠ 품목 합**(`paymentsNet ≠ itemsTotal`)이면 `⚠ 결제 ≠ 품목` 작은 배지(§6.4 · OQ-106) · 실결제가 음수면 `-1,000,000` 빨간 글자 · 통화가 섞인 수납은 합 대신 `⚠ 통화 섞임`(§6.7). 그 수납에 이 달 취소된 결제 · 전액 환불 품목이 있으면 머리에 회색 작은 글자 「취소 a · 환불 b」(숫자만 · OQ-134)
- 품목 줄이 이 달에 없는 수납(첫 승인 결제가 다른 달 — §6.2)은 **실결제가 0 이 아닐 때만** 머리로 보인다(실결제 = §6.9 — 고정 수납이나 이 달 취소가 있는 수납은 이 달 살아 있는 승인 + 반영 안 된 취소 · 음수 · 양수 다 있음 · 머리 「앞 달 결제 취소」 · 품목 줄 없음 — D1-06 · OQ-132 · 0.4.3). 실결제 0(취소 없는 분할 나머지 · 반영된 취소만)이면 **숨긴다**(§6.9 · `hiddenPurchases`) — `itemsNowhere` 는 0 이어도 보인다
- 품목이 이 달에 있는데 **전부 전액 환불**(또는 같은 달 전액 취소)이라 보일 줄 0 · 실결제 0 인 수납은 **숨긴다**(0.4.1 · doc r5 W-1 — 건수만 · §6.9). `itemsMissing`(품목을 못 찾음)은 숨기지 않는다
- 품목을 못 찾은 수납(`itemsMissing`)은 머리만 있고 그 아래 줄 자리에 「품목을 찾지 못했어요」 한 줄(§6.4)
- 품목이 어느 달에도 없는 수납(§4.4 · 0.3.1 — 응답 `purchases[].itemsNowhere = true`)은 「품목은 다른 달에」 대신 「품목이 어느 달에도 없어요 — 이 달 [전체 다시 받기]」 한 줄
- 줄을 눌러도 아무 일 없음(상세 · 링크 없음) · 기본값(OQ-113)

### 3.3 정렬

**묶음 차례 = back 응답 차례 그대로**(0.4.3 — front 는 다시 정렬하지 않는다 · 엑셀과 같은 차례 · code r3 W-1). back 은 「정렬 시각」 = 저장 `paid_at`(살아 있는 승인) · 없으면 그달 첫 취소 · 반환 시각(반영된 취소 포함) 오름차순 · 시각 없는 묶음은 맨 뒤 · 같으면 수납 id 로 놓는다 · **묶음 안 = 품목 줄만**(0.4.0): ② 응답 차례로 두되 **금액 0 인 품목 줄은 ② 차례에서 바로 앞에 있는 유료(금액 > 0) 품목 줄 바로 아래**로 붙인다(그 유료 줄 · 그 뒤 0원 줄들 · 다음 유료 줄 …). 앞에 유료 줄이 없는 0원 줄은 첫 유료 줄 바로 아래 · 유료 줄이 하나도 없으면 ② 차례 그대로. ② · ⑤ 에 「어느 품목의 구성품인지」를 잇는 필드는 없다(운영 수집본 — 0원 품목 159개 중 같은 상품명의 유료 품목이 있는 것 4개 · ⑤ `items` 와 ② 행을 잇는 id 없음) — **이 차례는 보이기 규칙이지 부모 판정이 아니다**(구성품이라고 적지 않는다 · OQ-135). ① `lastUpdatedPaymentDateTimeUtc` 로 정렬하지 않는다(R§2 ⑤ 줄). 차례 세부는 기본값(OQ-113).

### 3.4 상태 화면

| 상태 | 화면 | 근거 |
|---|---|---|
| 불러오는 중 | 표 자리 스피너(medikit `Loading`) + 「KOS 에서 불러오는 중이에요 — 수십 초 걸릴 수 있어요」. 월 선택 · 받기 버튼 · 메뉴 · 에이전시 탭 꺼짐. 저장본만 읽는 요청은 바로 끝나 문구가 거의 안 보인다(front 는 요청이 KOS 를 부를지 미리 모른다 — 같은 화면) | §5.3(수납마다 일정 조회) · §4.5 · 기본값(OQ-113) |
| 빈 달 | 「이 달에는 결제가 없어요」 · 건수 줄 0 | 기본값(OQ-113) |
| back 주소 비어 있음 | 「back 주소(NEXT_PUBLIC_API_BASE_URL)가 비어 있어요 — front/.env.local 에 넣고 front 를 다시 띄우세요」 · back 을 부르지 않는다 | 코드(cc-prototype procedure `lib/api.ts` `CONFIG_ERROR`) |
| 오류 | 「매출을 불러오지 못했어요」 + 오류 `message`(§4.3) + `[다시 시도]` — 이전 달 결과를 남겨 두지 않는다(어느 달 것인지 헷갈리지 않게). 받기(증분 · 전체)가 실패해도 **DB 는 바뀌지 않는다**(§4.4 한 트랜잭션) — 다시 시도하면 그 전 저장본에서 이어 받는다 | 기본값(OQ-113 · OQ-122) |
| 잘못된 달 | `?month=2026-13` 처럼 꼴이 틀리면 back 400 `bad_month` 문구 + ‹ › 로 고르라는 안내(시안 v1 `monthly-bad-month`) | 시안 v1 · §4.3 |
| back 이 안 뜸(네트워크) | 「back 에 연결하지 못했어요(back 이 떠 있나요?)」 + `[다시 시도]` | 기본값(OQ-113) |

### 3.5 에이전트별 조회 (`/agency`)

D1-11 — 같은 달 같은 응답(§4.2)을 **front 가 걸러서** 보인다(back 을 따로 부르지 않는다 · §4.1 · OQ-127). 묶음 · 줄 · 칸 · 정렬은 §3.2 · §3.3 그대로(시안 v1 `agency` · v2 `agency-all` · `agency-one`).

| 자리 | 계약 | 근거 |
|---|---|---|
| 주소 | `/agency?month=YYYY-MM[&agency=<에이전시 이름>]` — `agency` 가 없으면 「에이전시 전체」 탭. 그달 `agencies[]` 에 없는 이름이면 「에이전시 전체」로 바꾸고 주소에서 뺀다 | D1-11 · 기본값(OQ-125) |
| 탭 | 맨 앞 **「에이전시 전체」** + 그달 `agencies[]` 차례대로 에이전시마다 탭 하나. **탭 글자 = 이름 끝 「(에이전시)」를 뗀 것**(값 · 판정 · 주소는 원래 값 그대로 · `title` 에 원래 값) · 탭 숫자 = 그달 수납 건수(`agencies[].purchases`). **그달에 나온 에이전시만** 탭이 있다(다른 달에만 나온 에이전시는 탭 없음 — §6.8) | **D1-11** · 시안 v2 · **R§2 시안 v2 줄**(「탭 목록 = 그 달에 나온 에이전시만 · 『(에이전시)』 뗌」) |
| 「에이전시 전체」 | `agency ≠ null` 인 수납 전부 · 같은 묶음 모양(유입 칸으로 어느 에이전시인지 보임) + 요약 = `agencyTotal`(손님 · 결제 손님 · 수납 · **실결제 합** — 0.4.0) + 에이전시별 손님 수 · 결제 손님 수 · 실결제 합(`agencies[]`). **손님 셈은 시안 v2(이름 기준 — `v2.dc.html` 셈 · design-v2-report 정할 것)가 정본이 아니다** — back 이 준 숫자(D-15 `visitorId` 기준 · §6.8)를 그대로 보인다 · front 가 다시 세지 않는다 | D1-11 · 시안 v2 · **D1-15** |
| 에이전시 탭 | `agency = 그 이름` 인 수납만 + 요약 = 그 `agencies[]` 한 줄(손님 · 결제 손님 · 수납 · 실결제 합) | D1-11 · D1-18 · 시안 v1 `agency` |
| 수수료 | 요약 줄 끝 점선 칩 「수수료 — 다음 판」 자리만. 수수료 칸 없음 · **실결제 합은 보인다**(D1-18 「수수료 · 엑셀의 기준은 품목 실결제 금액」 — 0.4.1 합 기준 §6.9 = 같은 화면 엑셀 「품목 금액」 열 합 · 시안에 없는 칸 · OQ-136) | D1-01 · D1-11 · D1-18 · 시안 v1 |
| 저장 상태 · 받기 버튼 · 마지막 받은 시각 · 안내 | §3.1 과 같다(같은 응답 · 같은 달). 받기를 누르면 월별 · 에이전트별이 같은 결과를 본다 | D1-12 · D1-13 |
| 빈 탭 | 그달 수납이 있는 에이전시는 모두 탭이 있다(§6.8 — 숨긴 수납만 있어도). 그 에이전시 수납이 **전부 숨김**(전액 환불 · 같은 달 전액 취소 · 분할 나머지 · 반영된 취소만)이면 묶음 0 → 빈 탭 문구 「이 달 보일 결제가 없어요 — 손님 n명 · 결제 손님 m명(취소 · 환불 · 다른 달 품목만)」(n · m = 그 `agencies[]` 의 `customers` · `payingCustomers` — 숨긴 수납 포함 · 탭 숫자 = `purchases` 0). 「에이전시 전체」가 0 이면 「이 달에는 에이전시 손님의 결제가 없어요」. back 은 에이전시별 숨긴 수를 주지 않는다(새 필드 없음) | 시안 `agency-empty` 꼴 · doc r6 W-4 · 기본값(OQ-125) |
| 건수 줄 | 걸러진 묶음으로 다시 센다(수납 · 품목 · 취소된 결제 · 전액 환불 — 0.4.0 · 숨긴 수납 수는 `purchases[]` 에 없어 back 이 준 달 `counts.hiddenPurchases` 를 거르지 못한다 → 에이전트별 화면에서는 숨긴 수납 수를 보이지 않는다 · 0.4.1) — front 가 `purchases[].lines` 로 센다. `counts`(달 전체)는 월별 화면에만 | 기본값(OQ-127) |

### 3.6 엑셀 내보내기 (D-14)

| 자리 | 계약 | 근거 |
|---|---|---|
| 버튼 | 툴바 오른쪽 끝 `[엑셀 내보내기]` — 월별 · 에이전트별 두 화면 다. 불러오는 중 · 오류 · 저장본 없음일 때 꺼짐 · 빈 달 · 빈 탭이면 헤더만 있는 파일이 나온다(꺼지지 않음) | D1-14 · R§2 엑셀 줄 |
| 범위 | **지금 보는 화면 그대로** — 월별 = 그달 수납 전부(`view=monthly`) · 「에이전시 전체」 = `agency ≠ null` 수납(`view=agency`) · 에이전시 탭 = 그 에이전시(`view=agency&agency=<원래 값>`). 정렬 · 묶음 차례 = 화면(§3.3) | D1-14 「지금 보는 화면(월 + 탭) 그대로」 |
| 받기 | 누르면 `GET /api/sales.xlsx?…`(§4.7)를 브라우저 내려받기로 연다 — **KOS 를 부르지 않는다**(화면에 보이는 저장본으로 만든다). 내려받는 중 버튼 꺼짐 · 실패하면 오류 `message` 를 토스트로 | D1-14 「back 이 저장된 데이터로 만든다(KOS 호출 0)」 |

## 4. back API

### 4.1 경로

| 경로 | 요청 | 응답 | 근거 |
|---|---|---|---|
| **`GET /api/sales`** | 쿼리 `month=YYYY-MM`(없으면 이번 달 KST) · `refresh`(선택) = **`new`**(이번 달 — 마지막 받은 시각 이후만 더 받기) · **`full`**(그 달을 처음부터 다시 받기). 없으면 §4.5 판단표대로(저장본 · 필요할 때만 증분). 그 밖 값(옛 `1` 포함) → 400 `bad_refresh` | 200 §4.2 · 오류 §4.3 | D1-01 · D1-05 · D1-12 · §4.5 |
| **`GET /api/sales.xlsx`** | 쿼리 `month=YYYY-MM`(필수) · `view=monthly\|agency`(기본 `monthly`) · `agency=<에이전시 값>`(`view=agency` 일 때만 · 없으면 「에이전시 전체」) | 200 xlsx 파일(§4.7) · 오류 §4.3 | **D1-14** |
| `GET /api/health` | 없음 | `{ok: true, kosConfigured: bool}` — 키 · 주소 값은 싣지 않는다 | 코드(cc-prototype procedure `HealthResponse` 모양) · 기본값(OQ-111) |

- 경로는 **셋뿐**(`test_route_count_3` — 0.3.0 에 `sales.xlsx` 더함). 쓰기 경로(POST · PUT · DELETE) 0 — **`refresh` 도 GET 쿼리**다(KOS 를 다시 읽는 것이고 KOS 에 쓰는 것이 아니다 · 로컬 저장본만 바뀐다)
- **에이전트별 조회는 경로를 늘리지 않는다** — `/api/sales` 응답에 수납마다 `agency` · 달 요약 `agencies[]` · `agencyTotal` 을 싣고 front 가 거른다(§3.5). 근거: 한 달 수납이 수백 건이라 한 응답에 다 담겨도 가볍고 · 탭을 바꿀 때 back · KOS 를 다시 부르지 않으며 · 월별 · 에이전트별이 같은 저장본 · 같은 받은 시각을 본다(서로 다른 숫자가 날 자리가 없다). 대안(`GET /api/agencies?month=` + `GET /api/sales?month=&agency=`)은 OQ-127
- 모든 응답 헤더 `Cache-Control: no-store`(이름 · 결제가 브라우저 캐시에 남지 않게) · 기본값(OQ-117)

### 4.2 응답 shape (front 계약 — `schemas/sales.py` ↔ `front/lib/types.ts`)

```jsonc
{
  "month": "2026-10",
  "rangeUtc": { "from": "2026-09-30T15:00:00Z", "to": "2026-10-31T14:59:59Z" },  // §6.1 — KOS 에 보낸 값 그대로
  "fetchedAt": "2026-10-29T14:03:12+09:00",   // = store.fetchedAt — 그 달을 KOS 에서 마지막으로 받은 시각(KST)
  "cached": false,                            // 이 요청이 KOS 를 한 번도 안 불렀으면 true(저장본만 읽음) = fetch.mode == "none"
  "store": {                                  // §4.4 — 0.3.0
    "state": "current",                       // "current"(아직 확정 아님 · 증분 가능) | "closed"(확정 · 다시 안 부름)
    "fetchedAt": "2026-10-29T14:03:12+09:00", // 마지막으로 받은 시각(KST)
    "fullFetchedAt": "2026-10-29T09:00:05+09:00", // 마지막으로 처음부터 받은 시각(KST — 첫 조회 · refresh=full)
    "closedAt": null                          // closed 가 된 시각(KST) · current 면 null
  },
  "fetch": {                                  // 이 요청이 한 일 — §4.5
    "mode": "incremental",                    // "none"(저장본만) | "full" | "incremental"
    "fromUtc": "2026-09-30T15:00:00Z",        // ① 에 보낸 시작(full · incremental 둘 다 달 시작 — 0.3.1) · none 이면 null
    "kosCalls": 3,                            // 이 요청의 KOS 호출 수(토큰 교환 포함 · none = 0)
    "newTransactions": 2,                     // 이 요청으로 새로 저장된 ① 행 수(겹침에서 걸러진 것은 빼고)
    "duplicateTransactions": 5,               // 증분에서 다시 온(이미 저장된) ① 행 수(§4.5 증분 2 — 묶음 키 수 비교)
    "missingTransactions": 0,                 // 저장 행보다 KOS 가 적게 준 ① 행 수(지우지 않음 · §4.5 증분 2 · L15)
    "newPurchases": 1                         // 이 요청으로 처음 저장된 수납 수(③ · ② 를 부른 수)
  },
  "counts": {
    "purchases": 2,          // 보이는 묶음 수 = purchases.length(숨긴 수납 빼고 · 0.4.1)
    "itemLines": 2,          // 품목 줄 수(전액 환불 품목은 빼고 — §6.9)
    "canceledPayments": 1,   // 0.4.0 — 이 달 ① 의 CANCELED · SPENT 행 수(줄 없음 · 건수 줄 「취소된 결제 a건」)
    "refundedItems": 0,      // 0.4.0 — 이 달 품목 중 REFUNDED(줄 없음 · 「전액 환불 품목 b개」)
    "hiddenPurchases": 0,    // 0.4.1 — 실결제 0 · 품목 줄 0 이라 purchases[] 에 넣지 않은 수납 수(§6.9 · 손님 셈엔 들어감)
    "reflectedCancels": 0,   // 0.4.2 — 이 달 취소 · 반환 중 품목 달 품목에 이미 반영돼 실결제에 안 더한 행 수(§6.9 반영 판정 · 품목이 다른 달인 수납만)
    "excludedItems": 0,      // 0.4.1 — INITIALIZED · 그 밖 상태라 줄 · 합에서 뺀 품목 수(§6.9 · OQ-137)
    "transactions": 4,       // KOS 결제 통계 행 수(totalCount 와 같아야 함 — §9.2)
    "ignoredTransactions": 0,  // REQUESTED · FAILED 등 줄로 안 만든 행(§6.3) — 0 이 아니면 화면 건수 줄 옆에 「제외 n」
    "itemsMissing": 0,       // itemsMissing = true 인 수납 수
    "visitorMissing": 0,     // 이름을 못 찾은 수납 수
    "itemsElsewhere": 1,     // itemsHere = false 이고 이 달 ① 에 승인 행이 있는 수납 수(§6.2 · L11)
    "firstApprovalCanceled": 0, // 전액 취소된 승인이 첫 승인 후보에서 빠진 수납 수(§6.2 (a) · L11)
    "firstApprovedUnknown": 0,  // 첫 승인 결제 · 그 귀속 달을 대체 규칙으로 정한 수납 수(§6.2 (c) · L11)
    "unmatchedTransactions": 0, // ① 행 중 ⑤ 거래와 잇지 못해 at = null 인 줄 · 승인 행 수(§5.4 · L12)
    "atOutsideMonth": 0,     // 이은 시각(at)이 조회 달(KST) 밖인 ① 행 수(OQ-119 · L12)
    "itemsPinnedElsewhere": 0, // 이 달 판정은 itemsHere 인데 다른 달 저장본이 이미 품목을 보여서 이 달엔 안 보인 수납 수(§4.4 품목 달 고정 · OQ-128)
    "itemsNowhere": 0         // 고정한 다른 달이 이제 품목을 안 보여 품목이 어느 달에도 없는 수납 수(§4.4 · OQ-128 · 0.3.1)
  },
  "agencyTotal": { "customers": 4, "payingCustomers": 3, "purchases": 4, "netTotal": 1000000 },  // §6.8 — agency ≠ null 인 수납 전체 · netTotal = 수납 netTotal 합(통화 섞이면 null · 0.4.0)
  "agencies": [                               // §6.8 — 그달 수납이 하나라도 있는 에이전시만 · name 차례
    { "name": "에이전시A(에이전시)", "customers": 4, "payingCustomers": 3, "purchases": 4, "netTotal": 1000000 }
  ],
  "purchases": [
    {
      "purchaseId": "…a1b2c3",              // KOS 수납 id(전체 문자열 · 화면은 끝 6자리)
      "paidAt": "2026-10-03T11:20:00+09:00",  // §3.2 결제일 — 그달 살아 있는 승인 결제(⑤ 와 이은 것 · 전액 취소 안 됨)의 approvedDateTimeUtc 중 가장 이른 것 · 없으면 그달 첫 승인 · 없으면 null
      "firstApprovedAt": "2026-10-03T11:20:00+09:00", // 「취소 안 된 첫 승인 결제」(§6.2)의 ⑤ approvedDateTimeUtc · 없으면 null
      "itemsHere": true,                    // 품목 줄을 이 달에 보이나 = 첫 승인 결제 행이 이 달 ① 에 귀속됐나(§6.2)
      "visitorId": "…",
      "visitorName": "홍**",                // null = 못 찾음
      "visitDate": "2026-10-03",            // KST 날짜 · null = 일정 없음
      "visitorFunnelName": "에이전시A(에이전시)", // null = 빈 값(§6.6)
      "agency": "에이전시A(에이전시)",       // §6.8 — visitorFunnelName 이 「(에이전시)」로 끝나면 그 값 · 아니면 null
      "newInLastFetch": false,              // 그달 마지막 받기가 증분이고 그 받기로 처음 저장된 수납이면 true(§3.1 「새로 받음」)
      "itemsNowhere": false,                // §4.4 「품목이 어느 달에도 없음」 — itemsHere = false 이고 고정한 달도 이제 품목을 안 보임
      "paymentTypes": ["CARD", "CASH"],     // 그달 살아 있는 승인 결제의 수단(중복 없음 · 처음 나온 차례 · 전액 취소된 승인의 수단은 뺌 — 0.4.0)
      "currency": "KRW",                    // 이 수납 줄들의 통화 — 둘 이상 섞이면 null(§6.7)
      "netTotal": 1000000,                  // 0.4.1 — 실결제(합 기준 §6.9) = itemsHere 면 itemsTotal · 아니면 이 달 CANCELED · SPENT 합(음수) · currency = null(섞임)이면 null
      "paymentsNet": 1000000,               // 0.4.1 — 이 달 ① APPROVED + CANCELED · SPENT(음수) 합 · ⚠ 비교만(§6.4) · 합 · 엑셀에 안 씀
      "itemsTotal": 1000000,                // 품목 줄 amount 합(= 남은 실결제 합 · 전액 환불 0 원이라 빼도 같음) · itemsHere = false 면 0 · currency = null 이면 null
      "canceledPayments": 0,                // 0.4.0 — 이 수납의 이 달 CANCELED · SPENT 행 수
      "refundedItems": 0,                   // 0.4.0 — 이 수납의 REFUNDED 품목 수(itemsHere 일 때)
      "itemsMissing": false,
      "lines": [
        { "kind": "item", "itemType": "PRODUCT_OPTION", "productName": "시술 A", "productNameFrom": "product",
          "optionName": "1회", "amount": 600000, "currency": "KRW", "status": "ACCEPTED", "at": null },
        { "kind": "item", "itemType": "PREPAID_CARD_PRODUCT", "productName": "선불카드 B", "productNameFrom": "prepaidCard",
          "optionName": null, "amount": 400000, "currency": "KRW", "status": "PARTIALLY_REFUNDED", "at": null }
      ]
    }
  ]
}
```

| 필드 | 값 | 비고 |
|---|---|---|
| `lines[].kind` | **`item` 하나**(0.4.0 — `payment` · `cancel` · `spent` 줄은 없어짐 · D1-18) | 결제 · 취소 · 반환은 `netTotal` · `canceledPayments` 로만(§6.9) |
| `lines[].itemType` | `PRODUCT_OPTION` · `ETCETRA_PRODUCT` · `PREPAID_CARD_PRODUCT` · `PurchaseItemType_UNSPECIFIED` | 스펙 `OpenPurchaseItemStatisticsItem.purchaseItemType` 그대로 · 화면 이름은 front `lib/labels.ts` 한 곳 · `item` 줄에만 |
| `lines[].productNameFrom` | `product` · `prepaidCard` · `etcetera` · `none` | §6.5 — 어느 칸에서 읽었나(시험 · 확인용) |
| `lines[].status` | 스펙 `purchaseStatus` 값 — **`REFUNDED` 는 오지 않는다**(줄 없음 · `refundedItems` 로 셈) | 화면 이름 §6.3 |
| `lines[].amount` | 정수 · **남은 실결제** = ② `cost.totalAmount.value` 그대로(부분 환불은 남은 금액 · 음수 없음) | KOS `Money.value`(int64) · §6.3 |
| `lines[].currency` | KOS `Money.currency` 그대로(예: `KRW`) | 스펙 `protos.Money = {currency, value}` · 검수 W-5 |
| `lines[].at` | 늘 `null`(0.4.0 — 품목 줄만 남아 쓰는 곳 없음 · 필드는 둠) | §5.4 |
| `lines[].paymentType` | 없어짐(0.4.0 — 결제 · 취소 · 반환 줄이 없다) | D1-18 |
| 금액 합 필드 | 수납 `netTotal`(합 기준) · `itemsTotal` · `paymentsNet`(⚠ 비교만) · 에이전시 `agencies[].netTotal` · `agencyTotal.netTotal`(0.4.0) | 월 합계 필드 없음(§1.2) · `approvedTotal` 은 없어짐 |
| `counts` | **저장본 전체**(그 달에 저장된 ① 행 · 수납)로 센다 — 이 요청에서 새로 받은 것만이 아니다 · `transactions` = 저장된 ① 행 수 | §4.4 |
| `store` · `fetch` | §4.4 · §4.5 — 시각은 KST ISO · `fetch.kosCalls` 는 LIVE2 확인용(L13 ~ L15) | D1-12 |
| `purchases[].agency` · `agencies[]` · `agencyTotal` | §6.8 — 판정 · 셈 정의 | D1-11 |

### 4.3 오류

본문은 cc-prototype procedure 와 같은 꼴 `{"error": {"code", "message"}}`(코드 `main._error`).

| HTTP | `code` | 언제 | `message`(화면에 그대로) |
|---|---|---|---|
| 400 | `bad_month` | `month` 가 `YYYY-MM` 꼴이 아님 · 없는 달(`2026-13`) · 이번 달(KST)보다 뒤 | 「조회할 달이 올바르지 않아요」 |
| 503 | `kos_not_configured` | `KOS_OPEN_API_BASE` · `KOS_OPEN_API_KEY` 중 하나라도 비어 있음 | 「KOS 연결 설정이 비어 있어요 — back/.env 를 채워 주세요」 |
| 503 | `kos_busy` | KOS 가 429(호출 한도 — 스펙 「같은 IP 1분 3,000회」) | 「KOS 호출이 너무 많아요 — 1분 뒤 다시 시도해 주세요」 |
| 502 | `kos_rejected` | KOS 4xx 중 **「없음」(§6.4)이 아닌 것 전부** — 다른 reason 의 400 · **404(경로 없음 — KA§2 `getTicketGroupStatistics` 404 「No static resource」)** · 401(토큰 다시 받기 1회 뒤에도 401) | 「KOS 가 조회를 거절했어요 (오류 이름)」 — 오류 이름 = KOS `className` 끝(코드 `_error_of`) · 본문 · 값 없음 |
| 502 | `kos_unavailable` | 네트워크 · 시간 초과 · KOS 5xx | 「KOS 에 연결하지 못했어요」 |
| 500 | `guard_blocked` | 조회 전용 가드가 막음(§7.1 — 코드 버그) | 「허용되지 않은 KOS 호출이에요」 |
| 400 | `bad_view` | `sales.xlsx` 의 `view` 가 `monthly` · `agency` 가 아니거나 `month` 가 없음 · `view=monthly` 인데 `agency` 가 있음 | 「내보낼 화면이 올바르지 않아요」 |
| 409 | `not_fetched` | `sales.xlsx` 를 부른 달이 **아직 저장되지 않음**(`months` 에 행 없음) — 엑셀은 KOS 를 부르지 않는다(§4.7 · OQ-131) | 「이 달은 아직 받지 않았어요 — 화면에서 먼저 받아 주세요」 |
| 400 | `bad_refresh` | `refresh` 가 `new` · `full` 이 아님(0.3.0 — 옛 `1` 도 여기) | 「다시 받기 방식이 올바르지 않아요」 |
| 500 | `store_failed` | SQLite 를 열거나 쓰지 못함(경로 없음 · 권한 · 디스크 · 잠금 시간 초과) — 쓰던 트랜잭션은 되돌린다 | 「저장 파일을 쓰지 못했어요 — back 로그를 보세요」(경로 · SQL · 값은 싣지 않는다) |

- **「없음」은 오류가 아니다** — ③ · ④ 가 HTTP 400 이고 `errorProperties` 에 `{key: "purchaseId", reason: "NotFound"}`(③) · `{key: "visitorId", reason: "NotFound"}`(④)가 있을 때만 그 수납의 칸을 비운다(§6.4). 스펙 「에러 응답」(`reason: NotFound` = 「대상이 없음」) · `FindScheduleByPurchaseIdPurchaseIdNotFoundError` · `GetVisitorVisitorNotFoundError` · 검수 F-1
- **그 밖의 실패(「없음」 아닌 4xx · 5xx · 429 · 네트워크)는 달 전체를 오류로** 낸다 — 일부만 빠진 리스트를 보여 주지 않는다 · 기본값(OQ-114)
- 오류 · 로그에 키 · 토큰 · 테넌트 id · 이름 · 금액을 싣지 않는다(§7.3)

### 4.4 저장 (SQLite) · 동시성

D1-12 「받은 데이터는 SQLite 에 저장 · 다시 부르지 않는다」. 0.2.1 의 메모리 캐시(`SALES_CACHE_SEC` · OQ-105)를 **대신한다** — 메모리 캐시는 두지 않는다(응답은 늘 저장본에서 만든다).

| 항목 | 계약 | 근거 |
|---|---|---|
| 파일 | `SALES_DB_PATH`(기본 `data/sales.sqlite3` — `back/` 기준 상대 경로 · 절대 경로도 됨). **경로 규칙**(doc r3 W-6): 레포 안이면 `back/data/` 아래 · 확장자 `.sqlite3` 만 — 그 밖의 레포 안 경로(gitignore 밖)면 back 이 뜨지 않고 멈춘다(오류 로그 한 줄 · 경로 값은 싣지 않음). 레포 밖 절대 경로는 허용. **gitignore**(레포 `.gitignore` 에 `back/data/` · `*.sqlite3*` 더함 — `-wal` · `-shm` 포함). back 을 내려도 남는다 · 지우면 처음부터 다시 받는다 | D1-12 · D1-09(로컬만) · 기본값(OQ-122) |
| 권한 | 폴더가 없으면 **`700`** 으로 만든다 · back 은 SQLite 를 열기 전 **umask `077`** 을 건다 — 본 파일 · `-wal` · `-shm` 이 모두 **`600`**(WAL 의 받은 지 얼마 안 된 행도 다른 계정이 못 읽게 · doc r3 W-6). 뜰 때 셋의 권한이 600 보다 넓으면 600 으로 고친다 | §7.3 · 기본값(OQ-122) |
| 엔진 | 파이썬 표준 `sqlite3`(ORM 없음 · 새 의존성 없음) · `journal_mode=WAL` · `busy_timeout` 5초 · 표는 back 이 뜰 때 없으면 만든다(`CREATE TABLE IF NOT EXISTS` · `schema_version` 1). 표 모양을 바꾸면 판을 올리고 **사람이 파일을 지우고 다시 받는다**(옮기기 스크립트 없음). 파일의 `schema_version` 이 코드와 다르면 back 은 **뜨지 않고 멈춘다**(파일을 저절로 지우지 않는다 — 저절로 지우면 확정 달이 조용히 다시 받힌다 · D1-12 · doc r3 NOTE-3). **예외 하나(0.4.1)**: `schema_version` 1 → 2 는 `month_purchases` 에 빈 칸 두 개(`paid_at_utc` · `payment_types`)를 **더하기만** 하므로 back 이 뜰 때 `ALTER TABLE … ADD COLUMN` 으로 올린다(KOS 0 · 지우는 것 없음). 빈 칸인 행은 처음 읽을 때 저장된 ⑤ · ① 로 한 번 판정해 채우고 저장한다(KOS 0 — 확정 달을 다시 받지 않는다) | 기본값(OQ-122) |
| 무엇을 | **KOS 응답을 줄인 필드만** — 원본 JSON(응답 본문 · `data` 객체)을 통째로 저장하지 않는다. 개인정보는 **손님 이름 하나**(③ `visitor.name` · ④ `name`) + 방문일(날짜). 전화 · 생년월일 · 여권 · 차트번호 · 메모 · 예약 메모 · 수납 메모 · 담당자는 저장하지 않는다(§7.3) | D1-12 · 브리프 · §7.3 |
| 키 · 토큰 | 저장하지 않는다(토큰은 메모리만 · §7.1) | §7.2 |

**표(열 이름은 구현이 정한다 — 담는 것만 계약):**

| 표 | 한 행 | 담는 것 | 원천 |
|---|---|---|---|
| `months` | 달 하나 | `month`(`YYYY-MM` · 키) · `state`(`current` \| `closed`) · `fetched_at`(마지막 받은 시각 · UTC) · `last_fetch_mode`(`full` \| `incremental` — 「새로 받음」 판정) · `full_fetched_at` · `closed_at` · `kos_total_count`(마지막 **전체** 받기 때 ① 첫 페이지 `totalCount` — L2 확인용 숫자) | §4.5 |
| `transactions` | ① 결제 통계 한 행 | `month`(귀속 달) · `purchase_id` · `status` · `payment_type` · `value` · `currency` · `visitor_id` · `visitor_funnel_name` · `last_updated_utc`(§5.4 동점 가르기에만) · **`tx_id`**(§5.4 로 이은 ⑤ 거래 id · 못 이으면 null) · `at_utc`(이은 시각 · 없으면 null) · `fetched_at` | §5.1 ① · §5.4 |
| `purchase_txs` | ⑤ 거래 하나 | `purchase_id` · `tx_id`(키 = 둘) · `status` · `payment_type` · `value` · `currency` · `approved_utc` · `canceled_utc` · `spent_utc` · `last_updated_utc` · `created_utc` · `canceled_ref_id` — §7.3 에서 꺼내는 것과 같다. 수납 하나를 다시 받으면 그 수납 행을 **통째로 갈아 끼운다** | §5.1 ⑤ · §6.2 |
| `items` | ② 품목 한 행 | `purchase_id` · `seq`(② 응답 차례) · `item_type` · `product_name` · `product_name_from` · `option_name` · `amount` · `currency` · `status`(**받은 시점 상태** — D1-13) · `fetched_at` | §5.1 ② · §6.5 |
| `visitors` | 수납 하나 | `purchase_id`(키) · `visitor_name`(이름 · 못 찾으면 null) · `visit_date`(KST 날짜 · 없으면 null) · `fetched_at` | §5.1 ③ ④ |
| `month_purchases` | 달 × 수납 | `month` · `purchase_id`(키 = 둘) · `items_here` · `first_approved_utc` · `canceled_skipped` · `first_unknown` · `pinned_elsewhere` · **`paid_at_utc` · `payment_types`(살아 있는 승인 판정 — 받을 때 저장 · 쉼표로 이은 KOS 값 · 0.4.1 doc r5 W-2)** · `first_fetched_at`(이 달에 이 수납이 처음 저장된 받기의 시작 시각 — `newInLastFetch` = 마지막 받기가 증분이고 이 값 = `months.fetched_at`) — §6.2 판정 결과(받을 때 정하고 저장 · 읽을 때 다시 판정하지 않는다) | §6.2 |

| 항목 | 계약 | 근거 |
|---|---|---|
| 응답 만들기 | 응답(§4.2)은 **늘 저장본으로** 만든다 — `transactions` · `month_purchases` · `items` · `visitors` 를 **읽기 트랜잭션 하나로** 읽어(다른 달 받기의 커밋이 섞이지 않게 · doc r3 NOTE-1) §6 규칙대로 묶음 · 줄 · `counts` · `agencies` 를 만든다. KOS 를 부른 요청도 쓰기를 마친 뒤 저장본을 다시 읽어 만든다(받은 직후 응답과 다음에 연 응답이 같다) | D1-12 · 기본값(OQ-122) |
| 한 트랜잭션 | 한 번 받기(전체 · 증분)는 **KOS 호출을 다 마친 뒤 하나의 트랜잭션**(`BEGIN IMMEDIATE`)으로 쓴다. KOS 가 중간에 실패하면 아무것도 쓰지 않는다 → 그 달은 받기 전 상태 그대로(오류는 §4.3 · 달 전체 오류 OQ-114 그대로) | 기본값(OQ-122) |
| 품목 달 고정 | 한 수납의 품목은 **저장된 달 중 한 달에만** 보인다. 새로 판정한 `items_here = true` 인데 **다른 달 `month_purchases` 에 이미 `items_here = true`** 가 있으면 이 달은 `false` 로 두고 `pinned_elsewhere = true` · `counts.itemsPinnedElsewhere`. 먼저 저장된 달이 이긴다 — 저장 뒤엔 앞 달을 다시 판정하지 않기 때문(D1-12)에 생기는 자리(§4.6 ②). **「다른 달에 이미 있나」 확인과 `month_purchases` 쓰기는 같은 쓰기 트랜잭션(`BEGIN IMMEDIATE`) 안에서** 한다 — 두 달을 동시에 받아도(KOS 를 받는 동안엔 서로 모름) 늦게 쓰는 쪽이 앞 쪽 커밋을 보고 고정한다(doc r3 W-1) | §6.2 「정확히 한 번」 · D1-12 · 기본값(OQ-128) |
| 품목이 어느 달에도 없음 | 이 달 `pinned_elsewhere = true` 인데 고정한 달(다른 달)이 **이제 `items_here = true` 가 아닌** 수납(그 달을 [전체 다시 받기] 해서 첫 승인이 옮겨 감 — §4.6 ②) → 응답을 만들 때 셈 `counts.itemsNowhere` · 머리에 「품목이 어느 달에도 없어요 — 이 달 [전체 다시 받기]」(그러면 이 달이 다시 판정하며 고정할 달이 없어 품목을 가져온다). 저장본만 보고 정한다(KOS 0) · `itemsPinnedElsewhere` 에서는 뺀다 | doc r3 W-2 (b) · 기본값(OQ-128) |
| 같은 달 겹친 요청 | **달별 잠금**(프로세스 안 `asyncio.Lock`) — 같은 달 요청은 줄을 서고, 앞 요청이 받는 중이면 뒤 요청은 끝나기를 기다린 뒤 **§4.5 판단표를 다시** 본다(방금 받았으면 저장본만 · KOS 0). 다른 달은 동시에 받아도 되고, 쓰기는 **쓰기 잠금 하나**(프로세스 안)로 한 번에 하나 · SQLite `BEGIN IMMEDIATE` · `busy_timeout` 5초 넘으면 500 `store_failed` | D1-12 · 기본값(OQ-122) |
| 프로세스 | back 은 프로세스 하나(`uvicorn` 워커 1 — §10.2)를 전제로 한다. 여러 프로세스가 같은 파일을 쓰는 것은 이번 판 밖 | 기본값(OQ-122) |
| 수납별 조회 동시성 | 일정 조회(§5.3 ③)를 **동시에 최대 `SALES_KOS_CONCURRENCY`(기본 8)** 개. 스펙 한도 「같은 IP 1분 3,000회」 · 한 달 수납 수백 건(Q5 — 수납 id 394) 기준 여유 | 스펙 「호출 한도」 · Q5 · 기본값(OQ-105 → OQ-122) |
| 토큰 다시 받기 | 401 이 동시에 여러 개 나도 **토큰 교환은 한 번만**(잠금 — 먼저 받은 쪽 토큰을 나머지가 쓴다) | 검수 NOTE 4 · 기본값 |
| 시간 초과 | KOS 호출 하나 15초(코드 `httpx timeout=15`) | 코드 |

### 4.5 언제 KOS 를 부르나 — 전체 · 증분 · 확정

**판단표**(요청 하나 · 달 잠금 안에서 · 위에서 처음 맞는 줄):

| # | 그 달 저장 상태 | `refresh` | 하는 일 | `fetch.mode` |
|---|---|---|---|---|
| J1 | 무엇이든 | `full` | **전체 받기**(아래 「전체」) | `full` |
| J2 | 저장 없음(`months` 에 행 없음) | 없음 · `new` | **전체 받기** — 지난 달도 이번 달도 첫 조회 때 한 번 | `full` |
| J3 | `closed` | 없음 · `new` | **아무것도 안 부른다**(KOS 0) — 저장본만 | `none` |
| J4 | `current` 이고 그 달이 이미 끝남(지금 ≥ 다음 달 1일 00:00 KST) | 없음 · `new` | **증분 받기 한 번** → 아래 「확정」 판단 | `incremental` |
| J5 | `current` · 이번 달 | `new` | **증분 받기** | `incremental` |
| J6 | `current` · 이번 달 | 없음 | 마지막 받은 시각이 `SALES_CURRENT_STALE_SEC`(기본 600초)보다 오래면 **증분 받기**, 아니면 저장본만 | `incremental` · `none` |

- **전체**: §5.3 순서를 처음부터(① 달 범위 전부 · ⑤ 그 달 수납 전부 · ② · ③ · ④ 그 달 수납 전부) 부른 뒤, **한 쓰기 트랜잭션 안에서** 그 달의 `transactions` · `month_purchases` 를 지우고 새로 쓴다(지우기도 같은 트랜잭션 — 실패하면 지운 것도 돌아온다). `full_fetched_at` · `fetched_at` = 받기 시작 시각 · `kos_total_count` 기록. **수납 단위 표의 갈아 끼우기 범위**(doc r3 F-3):

  | 표 | 갈아 끼우는 수납 | 건드리지 않는 수납 |
  |---|---|---|
  | `items` | 이번 판정(품목 달 고정 뒤)으로 **이 달 `items_here = true`** 인 수납만 — 그 수납의 `items` 행을 지우고 이번 ② 결과로 | 이 달 `items_here = false` 인 수납(분할 결제로 다른 달이 품목을 가진 수납 · `pinned_elsewhere` 수납 포함) — 다른 달이 보이는 품목이 지워지지 않게 |
  | `purchase_txs` · `visitors` | 이 달 ① 에 나온 수납 전부 | 이 달 ① 에 없는 수납 |

  다른 달의 `transactions` · `month_purchases` · `months` 는 건드리지 않는다(갈아 끼운 `purchase_txs` · `visitors` 값은 수납 단위 표라 다른 달 응답에도 보인다 — 이름 · 방문일만 · 판정은 그 달 저장값 그대로)
- **증분**(D1-12 「이번 달 = 마지막으로 받은 시각 이후만 **더**」 — 0.3.1: **새로 생긴 것만 저장하고, 비싼 조회(⑤ · ② · ③ · ④)는 새 것에만** 한다. ① 은 한 번 부르는 값이 같으므로 달 전체로 부른다 · OQ-123):
  1. ① 을 **달 범위 전부**(§6.1 `from` · `to` · cursor 끝까지 — 보통 한 페이지 · 1회)로 부른다. 0.3.0 의 「앞 `fetched_at` − 겹침 여유부터」는 쓰지 않는다 — ① 행에는 만든 시각 · 거래 id 가 없어 저장 행과 「겹침 창 안의 행」을 가를 수 없고(§5.2 · 스펙 `OpenTransactionStatisticsItem`), 그래서 **같은 수단 · 같은 금액의 새 거래를 중복으로 버리는 길**(doc r3 F-2)과 **늦게 들어온 행을 놓치는 길**(§4.6 ⑤)이 생겼다
  2. **새 행 = 수로 가른다**: 수납마다 **묶음 키 G = (수납 · 상태 · 수단 · 금액 · 통화)** 로 받은 ① 행 수 `n_new` 와 그 달 저장 행 수 `n_stored` 를 센다. `n_new > n_stored` 인 묶음만 **새 행 `n_new − n_stored` 개**가 있다 · 같으면 새 행 0(다시 온 행은 `fetch.duplicateTransactions` 로 셈 · 저장 행은 고치지 않는다) · `n_new < n_stored` 면 저장 행을 지우지 않고 `fetch.missingTransactions` 로 센다(받은 시점 기준 · 로그 숫자 · L15). `last_updated` 는 묶음 키에 넣지 않는다(받은 뒤 바뀌는 값 — doc r3 W-7) · **「바뀜」(0.4.3 — code r2 W-1 · 구현 `diff_rows`)**: 한 수납에서 남는 묶음(`n_new > n_stored`)과 모자란 묶음(`n_new < n_stored`)이 **같이** 나오면(같은 거래의 상태 · 금액이 바뀜 — 예: `REQUESTED → APPROVED` · 부분 취소로 금액 정정) 그 수납의 **이 달 ① 행을 받은 행 전부로 갈아 끼운다**(KOS 대로 · 두 번 들어가지 않게). 셈은 그대로(남는 쪽 = `newTransactions` · 모자란 쪽 = `missingTransactions`) · 응답 필드는 더하지 않고 로그 `changedPurchases=N`(수만)
  3. 새 행이 있는 수납 = **처음 보는 수납**(`visitors` · `purchase_txs` 에 없음) **또는 새 거래가 생긴 저장 수납**(예: 지난 달 수납의 이번 달 취소 · 분할 결제 두 번째 승인 · 같은 수단 · 같은 금액 재결제) — 이 수납들만 ⑤ 를 다시 부르고(100개씩) `purchase_txs` 를 갈아 끼운 뒤, 그 수납의 **받은 ① 행 전부**를 §5.4 로 다시 잇는다. 묶음 G 마다 저장 행이 이미 가진 `tx_id` 와 다른 거래에 이어진 행부터 새 행으로 고른다(그런 행이 모자라면 못 이은 행 · 그래도 모자라면 남은 행 아무거나 — 수는 늘 `n_new − n_stored`). 고른 새 행을 `transactions` 에 더하고 `fetch.newTransactions` 로 센다
  4. **새 행이 생긴 수납만** §6.2 판정을 다시 해서 그 달 `month_purchases` 를 고친다(품목 달 고정 §4.4 포함 — 쓰기 트랜잭션 안)
  5. ② 는 아래 수납이 하나라도 있으면 **한 번**(범위 호출 · §6.4 범위) 부르고, 그 수납들 것만 `items` 를 **갈아 끼운다**: (i) `items_here = true` 인데 `items` 가 저장돼 있지 않은 수납(처음 보는 수납 · 증분 판정으로 `false → true` — doc r3 W-3) (ii) **이 달 `items_here = true` 인 저장 수납 중 이번 증분에서 새 행(취소 · 반환 · 승인)이 생긴 수납**(0.4.1 · doc r5 F-1 — 같은 달 전액 · 부분 환불이면 `REFUNDED` · 남은 금액으로 · 「승인 → 전액 취소 → 다른 금액 재승인」이면 재승인 품목으로 바뀐다 · 취소된 결제의 품목이 줄로 남는 길 0). 그 수납의 ⑤ 는 증분 3 에서 이미 다시 불렀고, 살아 있는 승인 판정(`paid_at_utc` · `payment_types`)도 이 달 것만 다시 저장한다. **품목이 다른 달(특히 `closed` 달)에 있는 수납의 `items` · 그 달 판정은 건드리지 않는다**(D1-12 · D1-13 — 확정 달 그대로). ③ · ④ 는 **처음 보는 수납만**. 그 밖 저장 수납의 품목 · 이름 · 방문일은 다시 받지 않는다(§4.6)
  6. `fetched_at` = 이번 받기 **시작 시각**(① 을 부르기 직전 시계). `fetch.fromUtc` 는 달 시작(① 에 보낸 값)
- **확정**(달이 바뀌는 순간 · `current` → `closed`): 받기(전체 · 증분)를 마친 뒤 **받기 시작 시각 ≥ 다음 달 1일 00:00 KST + `SALES_OVERLAP_SEC`** 이면 그 달을 `closed` · `closed_at` 기록. 그래서 ① 이번 달은 늘 `current` ② 지난 달을 처음 열면 전체 받기 한 번에 바로 `closed`(J2) ③ `current` 로 저장된 채 달이 끝난 달은 다음에 열 때 증분 한 번(J4 — 달 끝까지의 늦은 결제를 받음)으로 `closed` ④ 달이 끝나고 겹침 여유 안(00:00 ~ 00:10)에 받으면 아직 `current` — 다음 열 때 J4 를 한 번 더. `closed` 를 `current` 로 되돌리는 길은 없다(J1 `full` 은 받은 뒤 같은 규칙으로 다시 `closed`)
- **KOS 호출 수**: 전체 ≈ 토큰 1 + ① 1 + ⑤ (수납 수 ÷ 100) + ② 1 + 수납 수 + ④ 몇 건(§5.3) · 증분 ≈ 토큰(메모리에 없을 때) 1 + ① 1(달 전체 · 보통 한 페이지) + ⑤ (새 행이 있는 수납 ÷ 100 · 0 이면 0) + ② (0 또는 1) + 처음 보는 수납 수 + ④ 몇 건 · `closed` · 신선한 저장본 = **0**. 이 요청의 수를 `fetch.kosCalls` 로 돌려준다
- **줄 선 요청**(doc r3 W-4): 달 잠금을 기다린 요청은 **기다리는 동안 같은 달 받기가 하나라도 끝났으면 `refresh` 와 상관없이 저장본만**(`fetch.mode none` · KOS 0) — [새 결제 받기] · [전체 다시 받기] 를 두 번 눌러도, `/` · `/agency` 가 같이 보내도 한 번만 받는다

### 4.6 증분 · 저장이 놓치는 것 (D1-13 — 받은 시점 기준)

저장 뒤엔 다시 부르지 않으므로, **받은 뒤 KOS 에서 바뀐 것 중 아래는 저장본에 안 들어온다.** 화면 안내 「받은 시점 기준」(§3.1)이 이것을 말한다. 돈의 움직임(취소 · 환불 금액)은 취소된 달의 ① 취소 행으로 들어오므로 **줄 · 금액은 빠지지 않는다**(D1-06 · D1-13).

| # | 놓치는 것 | 저장본에 남는 것 | 다시 맞추는 길 |
|---|---|---|---|
| ① | 이미 받은 **품목의 상태 변화** — **다른 달**의 환불(10월에 판 품목이 11월에 환불 → ② `purchaseStatus`). **같은 달(이번 달)은 놓치지 않는다** — 증분이 새 행이 생긴 수납의 ② 를 다시 불러 맞춘다(§4.5 증분 5 (ii) · 0.4.1) | 확정 달 = 받은 시점 배지 · 금액(예: `결제 완료` · 받은 때 남은 금액). 환불 돈은 11월 「앞 달 결제 취소」(음수 머리 · 엑셀 음수 행)로 11월 실결제에서 빠진다 | 그 달 `[전체 다시 받기]`(그러면 배지 · 금액이 그때 상태로 — 받은 시각도 바뀜) · D1-13 |
| ② | 앞 달 수납의 **「첫 승인」이 바뀜**(앞 달 첫 승인이 다음 달에 전액 취소 → §6.2 s2 로 다음 달 승인이 첫 승인이 됨) | 앞 달 저장본이 품목을 보인다 · 다음 달은 품목 달 고정(§4.4)으로 품목을 안 보이고 `itemsPinnedElsewhere` | 앞 달 `[전체 다시 받기]` 뒤 다음 달 `[전체 다시 받기]`(그 순서로 눌러야 품목이 다음 달로 옮겨진다 · OQ-128). **앞 달만 다시 받으면** 품목이 어느 달에도 없게 되고 다음 달 머리에 「품목이 어느 달에도 없어요」 · `counts.itemsNowhere`(§4.4 — 숫자로 드러난다 · doc r3 W-2) |
| ③ | 손님 **이름 · 방문일 · 최초 유입 채널**이 받은 뒤 바뀜 | 받은 시점 값(유입은 ① 행 값 — 에이전시 판정도 받은 시점). 한 수납 · 한 손님이 여러 달에 저장되면 **달마다 받은 시점 유입이 달라 에이전시 판정이 달마다 다를 수 있다**(doc r3 NOTE-2 · L16 읽을 때). 이름 · 방문일은 수납 단위 표라 마지막으로 받은 값이 모든 달에 보인다 | 그 달 `[전체 다시 받기]` · OQ-109 |
| ④ | 이번 달 증분에서 **이미 저장된 수납의 품목이 늘거나 바뀜**(같은 수납에 품목을 더한 뒤 결제) | 처음 받을 때 품목. 새 승인 행은 들어오므로 `⚠ 결제 ≠ 품목` 으로 드러날 수 있다 | `[전체 다시 받기]` · OQ-123 |
| ⑤ | ~~겹침 여유보다 늦게 통계에 들어온 ① 행~~ — **0.3.1 에서 없어짐**: 증분이 ① 을 달 전체로 부르므로 늦게 들어온 행도 다음 증분에 새 행으로 들어온다 | — | (L15 로 확인) |
| ⑥ | ~~같은 수단 · 같은 금액의 새 거래가 중복으로 버려짐 · `last_updated` 가 바뀐 행이 두 번 들어감~~ — **0.3.1 에서 없어짐**: 새 행은 묶음 키(수납 · 상태 · 수단 · 금액 · 통화) **수**로 가르고 `last_updated` 를 쓰지 않는다(doc r3 F-2 · W-7). 남는 것: 같은 묶음 안에서 **어느 행이 새 행인지**(결제일 `at` · `tx_id`)는 §5.4 잇기에 달렸다 — 수 · 금액은 맞고 시각만 바뀌어 붙을 수 있다 | 줄 수 · 금액은 KOS 와 같음 | `[전체 다시 받기]` · L15 · OQ-123 |
| ⑦ | KOS 가 저장 행보다 ① 행을 적게 줌(받은 뒤 KOS 에서 행이 사라짐 — 스펙에 없는 일) | 저장 행 그대로(받은 시점) · `fetch.missingTransactions`. **단 같은 수납에 같은 받기에서 새 행도 오면 「바뀜」으로 그 수납 이 달 행이 KOS 대로 갈아 끼워져 빠진 행은 지워진다**(0.4.3 · 증분 2 · 로그 `changedPurchases`) | `[전체 다시 받기]`(그러면 KOS 대로) · L15 |
| ⑧ | **「앞 달 결제 취소」 반영 판정은 읽을 때 한다**(저장값 아님 · §6.9) — 품목 달(예: 9월)을 나중에 처음 받거나 [전체 다시 받기] 하면, 그 뒤 다른 달(10월 · `closed` 여도) 응답에서 그 수납의 「앞 달 결제 취소」 음수가 「반영됨」으로 바뀌어 빠진다(KOS 0 · 10월 숫자가 9월 받기에 따라 바뀜) | 두 달 합 = KOS 최종 금액(맞는 쪽으로만 바뀜) · 확정 10월 화면의 머리 · 에이전시 합이 바뀔 수 있다 | — (바뀌는 것이 맞다 · L24) · doc r6 F-1 |
| ⑨ | **schema 1 → 2 로 올릴 때 한 번**(§4.4 예외) — 이미 저장된 달의 `paid_at_utc` · `payment_types` 빈 칸은 「받은 때」 ⑤ 가 아니라 **그때 저장돼 있는 ⑤**(다른 달 증분이 갈아 끼웠으면 그 뒤 값)로 채워진다. 그 뒤로는 그 달 받기 · 그 달 증분에서만 바뀐다 | 머리 결제일 · 결제 수단 칩이 한 번 「지금 기준」 · 돈 · 품목 · 합은 안 바뀜 | 그 달 `[전체 다시 받기]`(원하면 · KOS 그 달만) · doc r6 W-3 |

### 4.7 엑셀 내보내기 — `GET /api/sales.xlsx` (D-14)

| 항목 | 계약 | 근거 |
|---|---|---|
| 원천 | **저장본으로만** — `/api/sales` 와 같은 저장본 · 같은 §6 규칙(묶음 · 줄 · 정렬 · §6.8 거르기)으로 만든다. **KOS 호출 0** · §4.5 판단표를 타지 않는다(이번 달이 오래돼도 증분하지 않는다 — 화면에 보이던 저장본 그대로) · 달 잠금은 잡는다(받는 중이면 끝나고 그 결과로) | **D1-14**(「back 이 저장된 데이터로 만든다(KOS 호출 0)」) · R§2 엑셀 줄 |
| 저장 안 된 달 | 409 `not_fetched` — 먼저 받기를 하지 않는다(받기는 화면에서만 · 사람이 보고 누른 것만 내보낸다) | D1-14 「KOS 호출 0」 · 기본값(OQ-131) |
| 거르기 | `view=monthly` = 그달 수납 전부 · `view=agency` = `agency ≠ null` 수납 · `&agency=<값>` = `agency` 가 그 값과 같은 수납(원래 값 · 공백 뗀 것으로 비교). 그달에 없는 에이전시 값이면 헤더만 있는 파일 | D1-14 「지금 보는 화면(월 + 탭) 그대로」 · §3.6 |
| 라이브러리 | **`openpyxl`**(back 의존성에 더함 · 쓰기만). 메모리에서 만들어 바로 응답(서버 디스크에 파일을 남기지 않는다) | 기본값(OQ-130) |
| 시트 1 「매출」 | 1행 = **헤더**(굵게 · 틀 고정 · 자동 필터). 2행부터 **줄 하나 = 행 하나**(§4.2 `lines[]` 전부 — 최종 결제된 품목 줄 · 0원 결제 완료 품목 줄 · 빼거나 합치지 않는다. 0.4.0: 결제 · 취소 · 반환 줄 · 전액 환불 품목은 `lines[]` 에 없어 행도 없다). 묶음 머리 행 · 빈 행 · **합계 행은 없다**(D1-01 · §1.2) | D1-14 · 지시서 |
| 칸 순서 | **결제일 · 손님 이름 · 방문일 · 최초 유입 채널 · 수납 · 품목 종류 · 상품 · 옵션 · 품목 금액 · 상태 · 결제 수단** (11칸 · D-14 차례 그대로) | **D1-14** |
| 칸 값 | **행 = 최종 결제된 품목 줄 + 「앞 달 결제 취소」 행**(0.4.1 · D1-18 — `REFUNDED` · `INITIALIZED` 등 품목 · 이 달 결제 · 취소 행은 넣지 않는다 · 0원 결제 완료 품목은 넣는다 · 차례 §3.3 · 숨긴 수납은 행 0). **「앞 달 결제 취소」 행** = 품목이 다른 달이고 이 달 **반영 안 된** 취소가 있는 수납 하나에 한 행(§6.9 반영 판정 · 반영된 취소는 행 없음 · 0.4.2): 결제일 = 그 수납 이 달 첫 취소 시각 · 품목 종류 `앞 달 결제 취소` · 상품 · 옵션 빈 칸 · 품목 금액 = 수납 `netTotal`(음수) · 상태 `취소` · 결제 수단 = 그 취소 행 수단 이름. 그래서 **「품목 금액」 열 합 = 같은 화면의 실결제 합**(§6.9). 결제일 = 수납 머리 결제일(`paidAt` · §3.2) · 없으면 빈 칸 / 손님 이름 · 방문일 · 최초 유입 채널 = 수납 값(줄마다 되풀이 · 빈 값은 빈 칸 — `(없음)` 같은 글자를 넣지 않는다) / 수납 = **수납 id 전체**(화면은 끝 6자리 · 엑셀은 대조용이라 전체) / 품목 종류 = 품목 종류 이름(`상품` · `기타 상품` · `선불카드`) / 상품 · 옵션 / **품목 금액 = 남은 실결제**(`lines[].amount` — 부분 환불은 남은 금액 · 헤더 글자는 D-14 그대로 「품목 금액」 · 뜻은 시트 「정보」 안내에) / 상태 = §6.3 화면 이름(`결제 완료` · `부분 환불` · 받은 시점 — D1-13) / 결제 수단 = 수납 `paymentTypes` 이름을 `, ` 로 이음. **「원래 금액」 칸은 두지 않는다**(부분 환불 전 금액이 KOS 에 없다 — §6.3 · OQ-133) | D1-03 · D1-14 · **D1-18** · §3.2 · §6.3 |
| 이름 표 | 품목 종류 · 상태 · 결제 수단의 한글 이름은 front `lib/labels.ts` 와 **같은 표**를 back 에 하나 둔다(`app/service/labels.py` · 두 표가 같음을 시험 — #39) · 모르는 값은 KOS 값 그대로 | §6.3 · OQ-113 |
| 셀 형식 | 결제일 = 날짜 · 시각 셀(KST · 시간대 없는 값 · `yyyy-mm-dd hh:mm`) · 방문일 = 날짜 셀(`yyyy-mm-dd`) · 품목 금액 = **숫자 셀**(`#,##0` · 음수 `-#,##0` · 통화가 `KRW` 가 아니면 `#,##0 "USD"` 처럼 형식에 통화 코드) · 수납 id = 글자 셀(숫자로 바뀌지 않게) · 나머지 글자. **글자 칸은 늘 글자 셀로 쓴다**(`openpyxl` 셀 `data_type = "s"` — 수식으로 해석하지 않음). 상품명 · 옵션 · 손님 이름 · 유입 채널은 사람이 넣은 글자라 `=` · `+` · `-` · `@` 로 시작해도 **값 그대로 글자**(`=HYPERLINK(…)` 가 받는 쪽 엑셀에서 수식 · 링크로 돌지 않게 · doc r3 W-5) | 지시서(「숫자 칸은 숫자 형식」) · §6.7 |
| 시트 2 「정보」 | 달 · 화면(`월별` · `에이전시 전체` · 에이전시 이름) · 마지막 받은 시각(`store.fetchedAt`) · 상태(`확정` · `이번 달`) · 행 수 · **취소된 결제 수(`canceledPayments`) · 전액 환불 품목 수(`refundedItems`) · 숨긴 수납 수(`hiddenPurchases` — 월별 화면만) · 뺀 품목 수(`excludedItems`) · 앞 달 품목에 반영된 취소 수(`reflectedCancels` · 0.4.2) · 실결제 합(= 「품목 금액」 열 합)**(그 화면으로 거른 수납만 · 0.4.0) · 안내 「금액은 받은 시점 기준 실결제 — 취소 · 전액 환불은 행이 없음 · 그 뒤 다른 달의 환불은 그 달 실결제에서 빠짐」(D1-13 · D1-18) — 숫자 · 글자만(금액 칸은 「실결제 합」 하나 · 0.4.3 NOTE-3) | D1-13 · 기본값(OQ-130) |
| 파일 이름 | `매출_YYYY-MM_월별.xlsx` · `매출_YYYY-MM_에이전시전체.xlsx` · `매출_YYYY-MM_<에이전시 이름 — 「(에이전시)」 뗀 것>.xlsx` · 파일 이름에 못 쓰는 글자(`/ \ : * ? " < > \|`)는 `_` · `Content-Disposition: attachment; filename*=UTF-8''<퍼센트 인코딩>` | 지시서 예(`매출_2026-10_전체.xlsx`) · 기본값(OQ-130) |
| 응답 | `Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` · `Cache-Control: no-store` · CORS 는 `/api/sales` 와 같음(GET · 출처 하나) — 브라우저가 `Content-Disposition` 을 읽게 `Access-Control-Expose-Headers: Content-Disposition` | §4.1 · OQ-117 |
| 로그 | 달 · `view` · 행 수 · 걸린 시간만. **에이전시 이름 · 손님 이름 · 금액 · 수납 id · 파일 이름을 남기지 않는다**(§7.3) | §7.3 · 지시서 |
| 개인정보 | 파일에 **손님 이름이 그대로** 들어간다(화면과 같음 — D1-03). **가리지 않는다**(사용자 2026-10-29 「엑셀 이름 가리지마」 · OQ-130 닫음) — 내려받은 파일은 사람이 다룬다(레포 · 리포트에 올리지 않는다 — L18) | D1-03 · D1-14 · 사용자 지시 |

## 5. KOS 원천 매핑

### 5.1 부르는 작업 (전부 `POST` · 공개 API · 호스트 `https://open-api.kos-solution.com`)

| # | 작업 | 경로 | 요청 | 쓰는 응답 필드 | 근거 |
|---|---|---|---|---|---|
| ① | `getTransactionStatistics` | `/statistics/open/v1/queries/get-transaction-statistics` | `createdTimeUtcFrom` · `createdTimeUtcTo`(§6.1) · `limit: 5000` · 다음 페이지는 `cursor = nextCursor` | `data[].purchaseId` · `status` · `paymentType` · `cost.totalAmount{value,currency}` · `visitorId` · `visitorFunnelName` · 첫 페이지 `totalCount` · (`lastUpdatedPaymentDateTimeUtc` 는 §5.4 동점 가르기에만 — 보이지 · 정렬하지 않음) | D1-05 · R§2(원천 줄) · Q6 · 스펙 `OpenGetTransactionStatisticsQuery` · `OpenTransactionStatisticsItem` |
| ② | `getPurchaseItemStatistics` | `/statistics/open/v1/queries/get-purchase-item-statistics` | `createdDateTimeUtcFrom` · `createdDateTimeUtcTo`(§6.4 — 달 시작 31일 앞부터) · `limit: 5000` · `cursor` | `data[].purchaseId` · `purchaseItemType` · `purchaseStatus` · `productTitle` · `productOptionTitle` · `prepaidCardName` · `etceteraProductName` · `cost.totalAmount{value,currency}` | D1-05 · R§2(원천 줄) · Q6 · 스펙 `OpenGetPurchaseItemStatisticsQuery` · `OpenPurchaseItemStatisticsItem` |
| ③ | `findScheduleByPurchaseId` | `/schedule/open/v1/queries/find-schedule-by-purchase-id` | `purchaseId` | `data.visitor.name` · `data.reservation.startDateTime` **둘만**(§7.3) | **R§2(원천 줄 10-29 정정 — 「이름·방문일은 `findScheduleByPurchaseId` · 일정 없으면 `getVisitor`」)** · Q5(수납이 두 일정에 걸린 경우 0) · 스펙 `FindScheduleByPurchaseIdQuery` · `ScheduleContract` |
| ④ | `getVisitor` | `/visitor/open/v1/queries/get-visitor` | `id = visitorId` | `data.name` **하나만**(§7.3) | ③ 이 「없음」일 때만(§6.4) · R§2(원천 줄 「일정 없으면 `getVisitor`」) · 스펙 `GetVisitor` · `VisitorInformation` |
| ⑤ | `getPurchaseSummaries` | `/purchase/open/v1/queries/get-purchase-summaries` | `purchaseIds`(① 의 수납 id · **100개씩 나눠** 부름) | `data[].id` · `transactions[]` 의 `id` · `status` · `paymentType` · `price{value,currency}` · `paymentDateTime.{approvedDateTimeUtc, canceledDateTimeUtc, spentDateTimeUtc, lastUpdatedDateTimeUtc}` | **R§2 ⑤ 줄(10-29 — 「⑤ 추가 승인 · 결제일 = ⑤ `approvedDateTimeUtc` · 취소 줄은 `canceledDateTimeUtc`」)** · R§2 분할 결제 줄(첫 승인 결제 달 판정) · 스펙 `GetPurchaseSummariesQuery` · `PurchaseSummaryTransaction`(변형 7개 모두 `id` · `status` · `paymentType` · `price` required) · `TransactionPaymentDateTime`(`lastUpdatedDateTimeUtc` 만 required · 나머지는 있을 때만) · Q5(수집 때 수납 id 621개를 7회로 받음) · 묶음 크기 기본값(OQ-116) |
| 인증 | `exchangeToken` | `/open/authorization/commands/exchange-token` | `{"key": KOS_OPEN_API_KEY}` | `token` → 이후 `Authorization: <token>`(Bearer 없음) | KA§1.2 · 코드 `client.open_token` |

- 응답 감싸기: 목록 · 통계 = `{"data": [...], "totalCount", "nextCursor"}` · 단건 = `{"data": {...}}`(KA§3.1 · 스펙). `totalCount` 는 첫 페이지에만 온다 · 마지막 페이지엔 `nextCursor` 가 없다(스펙)
- ① · ② 는 한 달이 한 페이지(`limit` 5000)로 끝나는 것이 보통이지만(Q6 — 한 달 결제 500행 안쪽) **`nextCursor` 가 있으면 끝까지 돈다**
- ③ · ④ 의 `data` 는 스펙상 required — 「없음」은 빈 `data` 가 아니라 400 `NotFound` 로 온다(§4.3 · 검수 F-1)
- 다른 작업은 부르지 않는다 — `getScheduleDetail` 은 일정 id 가 필요한데 ① · ② 에 일정 id 가 없다(Q5 「결제 통계에는 `scheduleId` 가 없다」) → ③ 으로 대신한다(R§2 원천 줄 정정)

### 5.2 칸 ↔ 필드

필드 · 작업의 근거는 §5.1 같은 번호 줄(① ~ ⑤ — R§2 · Q · 스펙 스키마)이다. 아래 표는 칸에 어느 필드가 가는지만 적는다.

| 칸(§3.2) | 응답 필드 | KOS 원천 | 조인 키 |
|---|---|---|---|
| 결제일(머리) | `paidAt` | 그달 ① `APPROVED` 행과 이은(§5.4) ⑤ 거래의 `paymentDateTime.approvedDateTimeUtc` 중 가장 이른 것 → KST | `purchaseId` + §5.4 |
| ~~결제일(결제 · 취소 · 반환 줄)~~ | — | 0.4.0 에서 줄이 없어짐(D1-18) — ⑤ 시각은 머리 `paidAt` 에만 쓴다 | — |
| (품목을 보일 달) | `firstApprovedAt` · `itemsHere` | ⑤ `transactions[]` 로 「취소 안 된 첫 승인 결제」를 고르고(§6.2 s1 ~ s3) · 그 거래가 이 달 ① `APPROVED` 행과 이어졌나(§5.4)로 판정(§6.2 s4 · s5) | `purchaseId` = ⑤ `data[].id` + §5.4 |
| 손님 이름 | `visitorName` | ③ `data.visitor.name` · 「없음」이면 ④ `data.name` | `purchaseId` → ③ · `visitorId`(①) → ④ |
| 방문일 | `visitDate` | ③ `data.reservation.startDateTime` → **오프셋을 읽어** KST 날짜(필드 이름에 `Utc` 가 없고 스펙 설명은 「ISO 8601 date-time」뿐 — `Z` 를 가정하지 않는다) | `purchaseId` |
| 최초 유입 채널 | `visitorFunnelName` | ① `visitorFunnelName`(같은 수납 행들의 첫 비어 있지 않은 값) | `purchaseId` |
| 수납 | `purchaseId` · `paymentTypes` | ① `purchaseId` · `APPROVED` 행 `paymentType` | — |
| 품목 종류 · 상품 · 옵션 · 품목 금액 · 상태 | `lines[]`(`kind = item`) | ② `purchaseItemType` · `productTitle`(§6.5) · `productOptionTitle` · `cost.totalAmount{value,currency}` · `purchaseStatus` | `purchaseId`(② ↔ ①) |
| 결제 줄 | `lines[]`(`kind = payment`) | ① `APPROVED` 행 `cost.totalAmount` · `paymentType` | `purchaseId` |
| ~~취소 · 환불 줄~~ | — | 0.4.0 에서 없어짐 — ① 취소 · 반환 행은 `netTotal` · `canceledPayments` 로만(§6.9) | `purchaseId` |
| 실결제(머리) | `netTotal` · `paymentsNet` | `netTotal` = §6.9 합 기준(품목 합 · 또는 이 달 취소 합) · `paymentsNet` = 이 달 ① `APPROVED` + `CANCELED` · `SPENT`(음수) 합(⚠ 비교만 · 0.4.1) | `purchaseId` |

- **결제일 원천**: ① 행에는 결제 생성 · 승인 시각 필드가 없다(스펙 `OpenTransactionStatisticsItem` 에 시각은 `lastUpdatedPaymentDateTimeUtc` · `visitorCreatedDateTimeUtc` 뿐 · 거래 id 도 없음). 그래서 결제일은 **⑤ 거래의 승인 · 취소 · 반환 일시**에서 읽고(R§2 ⑤ 줄), ① 행과 ⑤ 거래는 §5.4 로 잇는다. 달 귀속 필터는 ① `createdTimeUtc` 그대로다 — 보이는 결제일과 다를 수 있다(OQ-119)
- **결제 통계 행만으로 유입 · 손님 · 금액이 나온다** — 운영 10월 수집본에서 결제 행의 유입 = 일정 유입 451/451(Q5). 그래서 유입은 ③ 이 아니라 ① 에서 읽는다
- 손님 유입은 조회 시점 값이다 — 한 손님의 `visitorFunnelName` 이 행마다 다른 경우 0(Q4 · 추정 「조회 시점의 손님 값」). **0.3.0 — 받은 시점 값이 저장된다**(§4.4 `transactions.visitor_funnel_name`) — 지난 달은 다시 부르지 않으므로 그 사이 바뀐 유입은 `[전체 다시 받기]` 때만 보인다 · OQ-109 · §4.6 ③

### 5.3 전체 받기의 순서

§4.5 「전체」(J1 · J2)의 순서다. 증분은 §4.5 「증분」 1 ~ 6 이 이 순서에서 고른 것만 부른다.

```text
GET /api/sales?month=2026-10   (저장 없음 · refresh=full)
 ① 결제 통계 — 달 범위(§6.1) 전부 · cursor 끝까지         → 행 T[]
    purchaseIds = T 의 purchaseId 중복 없이(처음 나온 차례)
 ⑤ 수납 요약 — purchaseIds 100개씩                          → 수납마다 「취소 안 된 첫 승인 결제」 → ① 행과 잇기(§5.4) → itemsHere(§6.2)
 ② 품목 통계 — 달 시작 −31일 ~ 달 끝 · cursor 끝까지       → 행 I[] · itemsHere 인 수납 것만 남김
 ③ 수납마다 findScheduleByPurchaseId(동시 최대 8)           → 이름 · 방문일만 꺼냄
 ④ ③ 이 「없음」인 수납만 getVisitor(visitorId)             → 이름만 꺼냄
 ⑥ 줄인 필드를 한 트랜잭션으로 저장(§4.4) → 저장본으로 묶음 · 줄 만들기(§6 · §6.8) → 200
```

KOS 호출 수 ≈ 토큰 1 + ① 1 + ⑤ (수납 수 ÷ 100) + ② 1 + 수납 수 + ④ 몇 건. 한 달 수백 회(Q5 기준) — 스펙 한도 안.

### 5.4 ① 행 ↔ ⑤ 거래 잇기 (결제일 원천)

① 행에는 거래 id 가 없고(스펙 `OpenTransactionStatisticsItem`), ⑤ 거래에는 `id` 가 있다(스펙 `PurchaseSummaryTransaction` · required). 둘을 이을 공통 id 가 없으므로 **같은 수납 안에서 값으로 잇는다.** 운영 10월 수집본에서 취소 행 25/25 가 ⑤ `canceledRefId` 로 원 결제를 찾았다(Q6) — 수납 안의 거래는 ⑤ 에 다 있다.

| 단계 | 계약 | 근거 |
|---|---|---|
| 범위 | 같은 수납 — ① `purchaseId` = ⑤ `data[].id` | 스펙 · Q5 |
| 키 | `status` 같음 · `paymentType` 같음 · **금액 같음**(① `cost.totalAmount.value` 와 ⑤ `price.value` 의 **절댓값** · 통화 같음 — ⑤ `price` 의 부호는 스펙에 적혀 있지 않아 절댓값으로 비교) | 스펙 `OpenTransactionStatisticsItem` · `PurchaseSummaryTransaction` · 기본값(OQ-120) |
| 하나 | 후보가 정확히 하나면 잇는다. ⑤ 거래 하나는 ① 한 행에만 쓴다(이은 것은 후보에서 뺀다) | 기본값(OQ-120) |
| 여럿 | 같은 수단 · 같은 금액 거래가 여럿이면 ① `lastUpdatedPaymentDateTimeUtc` = ⑤ `paymentDateTime.lastUpdatedDateTimeUtc`(둘 다 스펙 뜻 「마지막 결제 상태 변경 일시」)인 것 하나를 고른다 — **두 값을 시각으로 파싱해 초 단위로 비교**한다(문자열 비교 금지 · 소수점 · `Z`/`+00:00` 표기 차이를 무시). **이 값은 고르는 데만 쓰고 화면 · 정렬 · 응답에 싣지 않는다**(R§2 ⑤ 줄 「`lastUpdatedPaymentDateTimeUtc` 안 씀」 = 결제일로 쓰지 않음). 그래도 여럿이거나 0 이면 못 이음 | 스펙 · 기본값(OQ-120) |
| 이은 뒤 시각 | `APPROVED` → `approvedDateTimeUtc` · `CANCELED` → `canceledDateTimeUtc` · `SPENT` → `spentDateTimeUtc`. 그 필드가 비어 있으면(스펙상 required 아님) **`at` 만 `null`**(화면 「시각 없음」 · 정렬 맨 뒤 · `counts.unmatchedTransactions` 로 셈 — 아래 「못 이음」과 화면 · 셈은 같다) · **잇기(거래 짝 · `tx_id`)는 유지**한다 — §6.2 s4 판정 · §4.5 거래 키는 이은 거래로 본다(0.3.0 — code r1 W-3: 짝이 확실한데 버리지 않는다) | R§2 ⑤ 줄 · 스펙 `TransactionPaymentDateTime` · code r1 W-3 |
| 못 이음 | (후보 0 · 동점을 못 가름) 줄 · 금액 · 상태 · 묶음은 ① 그대로(달에서 빠지지 않는다) · **`at = null`** · `tx_id = null` → 화면 결제일 `—` + 흐린 「시각 없음」 · 정렬 맨 뒤 · `counts.unmatchedTransactions` 로 센다. **① `lastUpdatedPaymentDateTimeUtc` 로 채우지 않는다**. 머리 `paidAt` 은 이은 승인만으로 정한다(하나도 없으면 `null` → `—`) | R§2 ⑤ 줄 · 기본값(OQ-120) |
| ⑤ 에 수납 없음 | 그 수납의 모든 ① 행이 못 이음 · `itemsHere` 는 §6.2 판정 표 「⑤ 에 수납 없음」 줄 | 스펙 `GetPurchaseSummariesQuery.purchaseIds` · §6.2 |

## 6. 규칙

### 6.1 월 경계 — KST

| 항목 | 계약 | 근거 |
|---|---|---|
| 귀속 | **결제 시각(KST) 기준** — ① 을 그 달 범위(`createdTimeUtc` 필터)로 부른 결과가 그 달이다. 보이는 결제일(⑤ 승인 · 취소 일시)이 그 달 밖이어도 묶음은 ① 이 정한 달에 둔다 — 결제일 칸에 다른 달 날짜가 그대로 보이고 `counts.atOutsideMonth` 로 센다 | D1-06 · R§2(원천 줄 · ⑤ 줄) · Q6 · 기본값(OQ-119) |
| 범위 | `from` = `YYYY-MM-01T00:00:00+09:00` → UTC(`전달 말일T15:00:00Z`) · `to` = **다음 달 1일 00:00 KST − 1초** → UTC(`말일T14:59:59Z`) | D1-06 · 스펙 예시(`…T23:59:59Z` 꼴 종료) · 기본값(OQ-101) |
| 이번 달 | `to` 는 그대로 달 끝(미래 시각). 조회 시각까지의 결제만 돌아온다 | 기본값(OQ-101) |
| 시간대 | 계산 · 화면 모두 `Asia/Seoul` — 서버 · 브라우저 시간대와 상관없이(코드 `domain/clock.py` `KST` · front `lib/time.ts` 그대로 복사). KOS 시각은 **오프셋을 읽어** 바꾼다(`…Z` · `+09:00` 둘 다) | 코드 · 검수 NOTE 2 |

### 6.2 그 달에 보이는 수납 · 분할 결제

**규칙 한 줄: 품목 줄은 그 수납의 「취소 안 된 첫 승인 결제 행」이 ① 로 귀속된 달에 나온다.** 다른 달엔 머리(실결제)만 나온다(0.4.0 — 결제 · 취소 줄은 없다 · §6.9). 달을 정하는 시계는 ① 귀속(`createdTimeUtc` 필터) 하나뿐이고, ⑤ 는 「어느 거래가 첫 승인인가」만 정한다 — 그래서 한 수납의 품목은 **어느 달에든 정확히 한 번** 나온다(R§2 분할 결제 줄 · 수정 4판 지시 · 검수 r2 W-1).

| 경우 | 보이는 것 | 근거 |
|---|---|---|
| 그 달 ① 에 행이 하나라도 있는 수납 | 묶음이 된다(승인이든 취소든) | D1-06 |
| **`itemsHere = true`**(아래 s4 · s5) | 최종 결제 품목 줄(② · `REFUNDED` 뺌) · 머리 실결제 = 품목 줄 합(§6.9 · 0.4.1). 결제 · 취소 행은 줄로 만들지 않는다(0.4.0 · §6.9) | **R§2(분할 결제 줄)** · D1-02 |
| **`itemsHere = false` 이고 이 달 승인 행 있음**(분할 결제가 달을 넘음 · 재결제 등) | **품목 줄 없음 · 이 달 승인은 실결제에 안 더함**(0.4.1 — 그 돈은 품목 달의 품목 금액에 있다) · 이 달 취소가 있으면 머리 실결제 = 취소 합(음수) · 없으면 숨김(§6.9) · 머리 「품목은 다른 달에 · 첫 승인 MM-DD」 · `counts.itemsElsewhere` | **R§2(분할 결제 줄 — 「다른 달엔 결제 · 취소 줄만 · 한 품목이 두 달에 전액으로 두 번 나오지 않게」)** |
| 취소 · 반환만 이 달에 있는 수납(원 결제는 앞 달) | 품목 줄 없이 **머리만**(실결제 = 취소 합 · 음수 · 「앞 달 결제 취소」 · 엑셀 음수 행 · 0.4.1) · `paidAt = null` → 머리 결제일은 첫 취소 · 반환 시각(⑤ `canceledDateTimeUtc` · `spentDateTimeUtc` — §5.4). 원 결제 달의 리스트는 고치지 않는다 | D1-06 「원 결제 달을 고치지 않는다」 · Q6 「취소 행은 취소한 시각으로 기간에 들어간다」 |

**판정 순서(s1 ~ s5 · 수납마다 · ⑤ 는 수납의 모든 달 거래를 준다 — 조회 달과 상관없이 같은 답이 나온다):**

| 단계 | 계약 | 근거 |
|---|---|---|
| s1 후보 | ⑤ `transactions[]` 중 `status = APPROVED` | 스펙 `PurchaseSummaryTransaction` |
| s2 (a) 전액 취소 뺌 | 같은 수납 ⑤ `CANCELED` 거래 중 `canceledRefId` 가 그 승인 `id` 를 가리키는 것들의 `price.value` 절댓값 합 ≥ 그 승인 금액 절댓값이면 **후보에서 뺀다**. 부분 취소는 후보에 남긴다. 뺀 것이 있으면 `counts.firstApprovalCanceled`. **후보가 다 빠지면**(수납 전체 취소) 빼지 않은 원래 후보로 되돌린다 — 품목은 원 첫 승인 달에 한 번 나오고 취소 줄로 순액 0 | 스펙 `canceledRefId` 「취소 참조 ID」 · `getTransactionList` 설명 「환불 · 취소는 음수 금액의 새 거래 … `canceledRefId` 가 원거래의 `id`」 · Q6(취소 25/25 가 `canceledRefId` 로 원 결제를 찾음) · 검수 r2 W-1 a · 부분 취소 · 다 빠짐 = 기본값(OQ-121) |
| s3 「첫」 고르기 | 남은 후보를 `paymentDateTime.approvedDateTimeUtc` 차례로(파싱한 시각). 승인 시각이 없는 후보가 있으면 **그 수납의 모든 후보를** `createdDateTimeUtc`(⑤ 「거래 생성 일시」 · deprecated) → 없으면 `paymentDateTime.lastUpdatedDateTimeUtc`(required) 차례로 정렬하고 · 같으면 `id` 차례. 대체 정렬을 쓴 수납은 `counts.firstApprovedUnknown` | 스펙 `TransactionPaymentDateTime`(`lastUpdatedDateTimeUtc` 만 required) · `PurchaseSummaryTransaction.*.paymentDateTime` 설명(「없다면 하위 호환을 위해 `createdDateTimeUtc`」) · 검수 r2 W-1 c · 기본값(OQ-121) |
| s4 귀속 달 = 품목 달 | 그 「첫 승인 결제」가 **이 달 ① `APPROVED` 행과 이어지면**(§5.4) `itemsHere = true` · 아니면 `false`. 자정 경계(10-31 23:59 생성 · 11-01 승인)여도 ① 이 10월에 넣은 행이면 10월에 품목이 나온다 · 11월엔 그 수납 묶음이 없다 | D1-06(귀속 = ① 결제 시각) · 수정 4판 지시 (b) · 검수 r2 W-1 b |
| s5 잇기 실패 | 「첫 승인 결제」가 이 달 ① 의 어떤 행과도 이어지지 않았는데 이 달 ① 에 **못 이은 `APPROVED` 행**이 있으면, 그 거래의 ⑤ `createdDateTimeUtc`(없으면 `lastUpdatedDateTimeUtc`) KST 달 = 이 달일 때만 `itemsHere = true` — ① 귀속 시계와 같은 축으로 보는 대체(추정 — `createdDateTimeUtc` 가 ① `createdTimeUtc` 와 같은 값인지는 스펙에 없음) · `counts.firstApprovedUnknown` | 검수 r2 W-1 c · NOTE 1 · 기본값(OQ-121) |
| **⑤ 에 수납은 있으나 `APPROVED` 거래 0**(s1 후보 0) | 「⑤ 에 수납 없음」 줄과 같다 — 이 달 ① 에 `APPROVED` 행이 있으면 `itemsHere = true` · `counts.firstApprovedUnknown`(① 은 승인이라는데 ⑤ 에 승인이 없는 데이터 모순 — 품목이 어느 달에도 안 나오는 것을 막는다 · 0.3.0 — code r1 W-1) | §6.2 머리글 「정확히 한 번」 · 「대체는 센다」 · code r1 W-1 |
| ⑤ 에 수납 없음 | ⑤ 가 아무 거래도 안 줘서 첫 승인을 정할 수 없다 → 이 달 ① 에 `APPROVED` 행이 있으면 `itemsHere = true` · `counts.firstApprovedUnknown`. **이 경우만 분할 결제 수납이 두 달에 품목을 보일 수 있다**(달마다 독립 판정) — 운영 10월은 ① 에 있는 수납이 ⑤ 에서 빠진 경우 0(Q5 — 안 돌아온 170건은 결제 · 품목 통계에도 없음) | 스펙 `GetPurchaseSummariesQuery.purchaseIds` 「존재하지 않거나 삭제된 수납 ID는 응답에 포함되지 않습니다」 · Q5 · 기본값(OQ-116) |

- `firstApprovedAt` = 고른 「첫 승인 결제」의 ⑤ `approvedDateTimeUtc`(없으면 `null`) — 화면 머리 문구에만 쓴다. 달 판정에는 쓰지 않는다(s4)
- 대체(s3 대체 정렬 · s5 잇기 실패 · ⑤ 에 승인 0 · ⑤ 에 수납 없음)를 탄 수납은 전부 `firstApprovedUnknown` 으로 세어 드러낸다 — L11
- **저장(0.3.0)**: 판정은 받을 때 하고 `month_purchases` 에 저장한다(§4.4). 저장된 앞 달은 다시 판정하지 않으므로, 「정확히 한 번」은 **품목 달 고정**(§4.4 — 먼저 저장된 달이 이김 · `itemsPinnedElsewhere`)으로 지킨다 · 놓치는 자리 §4.6 ②

### 6.3 상태 · 취소 · 환불

① `status`(결제 통계 — 스펙 `TransactionStatus`) 처리:

| ① `status` | 스펙 뜻 | 처리 | 화면 상태 |
|---|---|---|---|
| `APPROVED` | 승인됨 | 묶음 · 결제일 · 결제 수단(살아 있는 승인만) · **`paymentsNet` 에 더함**(실결제 `netTotal` 은 품목 합 — §6.9). **줄은 만들지 않는다**(0.4.0 · D1-18) | — |
| `CANCELED` | 취소 거래 — 「거래가 취소된 상태가 아니라 취소 거래」 · 금액 음수(Q6 25/25) | **`paymentsNet` 에 음수로 더함** · 품목이 다른 달인 수납이면 `netTotal`(이 달 취소 합)에도 · `canceledPayments` +1 · **줄 없음**(0.4.0 · D1-18) | — |
| `SPENT` | 반환 거래 — 「거래 취소 없이 돈을 돌려줄 때 · 금액이 음수」 | **`paymentsNet` 에 음수로 더함** · 품목이 다른 달인 수납이면 `netTotal` 에도 · `canceledPayments` +1 · **줄 없음** · 운영 10월 0건(Q6) | — |
| `REQUESTED` · `FAILED` · 그 밖 | 요청됨 · 처리 실패(돈이 움직이지 않음) | 줄 · 합에 넣지 않음 · `counts.ignoredTransactions` 로 센다 · 운영 10월 0건(Q6) | — · 기본값(OQ-115) |

② `purchaseStatus`(품목 — 스펙 `PurchaseStatus`) 는 품목 줄 상태 배지로 그대로:

| `purchaseStatus` | 스펙 뜻 | 화면 상태 |
|---|---|---|
| `ACCEPTED` | 수납 완료 | `결제 완료`(0.4.0) |
| `PAID` | 지불 수납 | `결제 완료`(0.4.0) |
| `PARTIALLY_REFUNDED` | 부분 환불 | `부분 환불` — 금액 = 남은 금액(`cost.totalAmount`) |
| `REFUNDED` | 환불 | **줄 없음**(0.4.0 · D1-18 — `refundedItems` 로 셈 · `cost.totalAmount` = 0) |
| `INITIALIZED` | 미수납 | `미수납` |
| 그 밖(`PURCHASE_STATUS_UNSPECIFIED` 포함) | — | 값 그대로 |

- **품목 상태는 받은 시점의 상태**다(D1-13 · 0.3.0 — ② 에 달별 상태가 없고, 저장 뒤 다시 부르지 않는다 · §4.6 ①). 10월에 판 품목이 11월에 환불돼도 저장된 10월 리스트의 배지는 받은 때 그대로다(§3.1 안내 「받은 시점 기준」). 돈의 움직임(음수)은 **취소된 달의 취소 줄**에만 있다 — D1-06. `[전체 다시 받기]` 를 누르면 그때 상태로 바뀐다
- **품목 금액 = 남은 실결제(0.4.0 — OQ-102 뒤집어 닫음)**. 운영 수집본(2026-10-28 · ② 1,462행 · ⑤ 453수납 · ① 454행 — 레포 밖) 대조: ① `REFUNDED` 품목 **28/28 이 `cost.totalAmount = 0`** ② 이 달 ① 이 있는 수납 **392/392 가 「① 승인 + 취소(음수) 합 = 그 수납 ② `cost.totalAmount` 합」** — 환불 품목이 있는 수납 12 · 부분 환불 품목이 있는 수납 2 포함. 그래서 ② `cost.totalAmount` 는 **원 가격이 아니라 환불 뒤 남은 금액**이다(전액 환불 = 0 · 부분 환불 = 남은 금액 — 스펙 뜻 「잔존 가치 금액 또는 최종가」 중 잔존 가치). 0.1.1 ~ 0.3.1 의 「원 가격으로 본다」(444/444 를 「`REFUNDED` 를 빼야 맞는다」로 읽은 것)는 틀렸다 — `REFUNDED` 가 0 이라 빼도 넣어도 같았다
- **부분 환불의 환불된 금액 · 원래 금액은 KOS 에 없다**(품목 단위로): ② 의 `firstPriceAmount` · `basePriceAmountV2` 는 정가 · 기준가라 결제 완료 품목에서도 `cost` 보다 큰 것이 많다(결제 완료 1,422 중 685 — 할인) → 「환불 전 금액」으로 쓸 수 없다. ⑤ `items[]`(`price` · `priceV2` · `basePrice` · `adjustedPrice`)는 ② 행과 잇는 키가 없고, ⑤ `refundingItems` · `revokingItems` 는 수집본 453수납 모두 비어 있다(`priceAdjustments` 5 · `pendingItems` 5 만 값). 환불된 금액은 **수납 단위**(① 취소 행 · ⑤ 취소 거래)로만 있다 → 화면 · 엑셀은 **남은 금액만**(D1-18) · 품목별 환불 금액이 필요해지면 OQ-133
- 결제 통계의 취소 행과 품목은 이어지지 않는다(결제 수단 · 취소는 수납 단위 — DEC-001 Context 「결제 수단은 품목과 이어지지 않는다」). 그래서 취소된 결제가 어느 품목의 것이었는지는 알 수 없다 — 처음 결제의 품목 구성도 공개 API 에 없다(R§2 D-18 줄 「취소된 결제의 품목 구성은 공개 API 에 없음」) · 0.4.0 은 취소된 결제를 줄로 보이지 않으므로 필요 없다

### 6.4 품목 조인 · 못 찾은 것

| 항목 | 계약 | 근거 |
|---|---|---|
| 조인 키 | ② `purchaseId` = ① `purchaseId` | Q6 · DEC-001 Context(10월 승인 수납 392건 전부 품목 있음) |
| ② 범위 | ② 의 기간 필터는 **품목 생성 시각**(`createdDateTimeUtc` — 「구매 일시」)이라 결제 시각과 다를 수 있다. 앞 달에 수납을 만들고 이번 달에 첫 결제한 경우를 잡으려고 **달 시작 −31일 ~ 달 끝**으로 부르고 `itemsHere` 인 수납만 남긴다 | 스펙 `OpenGetPurchaseItemStatisticsQuery.createdDateTimeUtcFrom` · 기본값(OQ-116) |
| 그래도 없음 | `itemsHere = true` 인데 품목이 0줄인 수납 = `itemsMissing: true` · 머리만 · 「품목을 찾지 못했어요」 · `counts.itemsMissing` — **빠뜨리지 않고 드러낸다** | 기본값(OQ-116) |
| 결제 ≠ 품목 | `itemsHere = true` 이고 **`paymentsNet ≠ itemsTotal`**(이 달 결제 순액 ≠ 품목 합 · 0.4.1 — 0.4.0 의 `netTotal` 이 이름만 바뀜)이면 머리에 `⚠ 결제 ≠ 품목`. 숫자를 맞추려고 고치지 않는다. 근거: 운영 수집본에서 이 달 ① 이 있는 수납 **392/392** 가 「① 승인 + 취소(음수) 합 = ② `cost.totalAmount` 합」(환불 · 부분 환불 수납 14 포함 — §6.3). 정상인데도 뜰 수 있는 자리 = **달을 넘는 돈**(분할 결제 나머지를 다음 달에 냄 · 다음 달 환불 — 품목 금액은 받은 시점 남은 금액 · 취소는 다음 달 ①) · 실물 L20 | 운영 수집본 대조(0.4.0) · OQ-106 |
| 일정 「없음」 | ③ 이 **HTTP 400 이고 `errorProperties` 에 `{key: "purchaseId", reason: "NotFound"}`** 면 `visitDate = null` · ④ 로 이름만 | 스펙 「에러 응답」 · `FindScheduleByPurchaseIdPurchaseIdNotFoundError`(「수납 ID에 해당하는 스케줄을 찾을 수 없는 경우」) · R§2(원천 줄) · 검수 F-1 |
| 손님 「없음」 | ④ 가 **HTTP 400 이고 `{key: "visitorId", reason: "NotFound"}`** 면 `visitorName = null` · `counts.visitorMissing` | 스펙 `GetVisitorVisitorNotFoundError`(「없거나 이미 삭제된 내원객」) · 검수 F-1 |
| 그 밖의 ③ · ④ 실패 | 다른 reason 의 400 · **404**(경로 없음 — 「없음」으로 삼키지 않는다) · 401 · 429 · 5xx · 네트워크 = **달 전체 오류**(§4.3) | 검수 F-1 · 기본값(OQ-114) |
| 품목 줄 단위 | ② 한 행 = 한 줄. ② 행에 품목 id 가 없다(스펙) — 행을 합치거나 지우지 않는다 | 스펙 `OpenPurchaseItemStatisticsItem` |

### 6.5 상품명 빈 품목 · 선불카드

| 항목 | 계약 | 근거 |
|---|---|---|
| 상품명 | `productTitle` → 비면 `prepaidCardName` → 비면 `etceteraProductName` → 다 비면 `—`(`productNameFrom: none`) | D1-07 「상품명이 빈 품목은 선불카드명 · 기타 상품명 칸에서」 · 스펙 필드 |
| 선불카드 판매 품목 | `PREPAID_CARD_PRODUCT` 품목도 **빼지 않고** 한 줄 · 품목 종류 칸 `선불카드` | D1-07 |
| 선불카드 사용 결제 | ① `paymentType = PREPAID_CARD` 승인 결제도 빼지 않는다 — 수납 결제 수단 칩 `선불카드` | D1-07 · Q6 ⚠(충전 · 사용 이중 계산 위험) |
| 이중 계산 | **거르지 않는다.** 이번 판에는 합계가 없어 화면에서 이중으로 더해지지 않는다. 충전 · 사용 중 어느 쪽을 셀지는 뒤의 필터가 정한다 | D1-07 · OQ-112 |

### 6.6 최초 유입 채널

| 항목 | 계약 | 근거 |
|---|---|---|
| 필드 | **① `visitorFunnelName`**(손님의 최초 유입 채널). 예약 유입(`reservationFunnelName`)이 아니다 | D1-04 · R§2(판정 줄) |
| 값 | 문자열 그대로 · 바꾸거나 묶지 않는다. 에이전시인지는 이 값의 **이름 끝**으로만 가른다(§6.8) | D1-11 · Q1 「KOS 에 에이전시 구조화 표시 없음」 |
| 빈 값 | `null` → `(없음)`. 운영 10월 일정 기준 손님 유입 빈 값 8.9%(Q3) | Q3 |
| 자유 텍스트 | `visitorFunnelDetail` · `reservationMemo` · 손님 메모 등은 **읽지도 보이지도 않는다** — 빈 유입을 메모로 채우지 않는다 | [[no-inference-from-free-text]] · Q3 「자유 텍스트에만 있음 6건 — 세지 않았다」 |

### 6.7 금액 · 통화

| 항목 | 계약 | 근거 |
|---|---|---|
| 금액 기준 | 품목 금액 = ② `cost.totalAmount.value` · 결제 금액 = ① `cost.totalAmount.value`(공급가 · VAT 가 아니라 총액) | D1-02 「금액은 품목 금액」 · 리포트 「정할 것 7」 열림 → 기본값(OQ-108) |
| 통화 | 줄마다 `currency` = KOS `Money.currency` 그대로. 수납 `currency` = 그 수납 줄들 · 그달 승인 행의 통화(**빈 값은 세지 않는다**)가 하나면 그 값, **둘 이상 섞이면 `null`** — 이때 `netTotal` · `itemsTotal` 도 `null`, 머리는 합 대신 `⚠ 통화 섞임` · `⚠ 결제 ≠ 품목` 비교 안 함 | 스펙 `protos.Money = {currency, value}` · 검수 W-5 (a) · 기본값(OQ-118) |
| **통화 0개** | 줄도 승인 행도 통화를 하나도 못 읽으면(줄 0 — 예: ① 에 `REQUESTED` 행만 · 통화가 빈 행만) **섞임이 아니다** → 그 수납의 이 달 ① 행 통화(빈 값 뺌)가 하나면 그 값 · 그래도 없으면 `currency = null` · **합은 숫자 그대로**(줄 0 이면 `netTotal = 0` · `itemsTotal = 0`). 그래서 front 는 **`⚠ 통화 섞임` 을 `netTotal === null` 일 때만** 보인다(`currency === null` 로 가르지 않는다) · 합 칸은 `currency = null` 이면 숫자만 | 0.3.0 — code r1 W-5 · 수정 1판 구현(`sales.py` 통화 판정) · 기본값(OQ-118) |
| 화면 | `KRW` 줄은 숫자만 · 그 밖 통화는 숫자 뒤에 통화 코드. 운영 10월은 전부 `KRW`(Q6) | Q6 · 기본값(OQ-118) |

### 6.8 에이전시 판정 · 손님 수 (D1-11)

| 항목 | 계약 | 근거 |
|---|---|---|
| 판정 | 수납의 `visitorFunnelName`(§6.6 — ① 최초 유입 채널)이 **앞뒤 공백을 뗀 뒤 정확히 `(에이전시)` 로 끝나면** 그 수납은 에이전시 손님 · `agency` = 그 값(공백 뗀 문자열 그대로 · 끝 글자를 떼거나 바꾸지 않는다). 아니면 `agency = null`. 반각 괄호 `(` `)` 만 — 전각 · 다른 표기 · 「에이전시」가 가운데 있는 값은 에이전시가 아니다(규칙을 넓히지 않는다) | **D1-11**(「최초 유입 채널이 『(에이전시)』인 값」) · D1-04 · 브리프 · 기본값(OQ-125) |
| 자유 텍스트 | 빈 유입(`null`)을 메모 · 상세 유입 · 예약 유입으로 채워 에이전시로 넣지 않는다 — 빈 유입 수납은 「에이전시 전체」에도 없다 | [[no-inference-from-free-text]] · §6.6 · D1-04 |
| 에이전시 목록 | `agencies[]` = **그달 저장본**에서 `agency ≠ null` 인 수납의 `agency` 값 중복 없이 · 차례 = 이름 문자열 오름차순(유니코드 코드포인트). 미리 정한 에이전시 목록 · 표는 없다(KOS 에 구조화 표시 없음 — Q1) · **그달에 나온 에이전시만**(다른 달 저장본은 보지 않는다) | D1-11 · Q1 · **R§2 시안 v2 줄**(「탭 목록 = 그 달에 나온 에이전시만」) · 차례 = 기본값(OQ-125) |
| 손님 수 `customers` | 그 에이전시(「전체」면 에이전시 수납 전부)의 그달 묶음에서 **손님을 중복 없이** 센 수. 손님 = **KOS 손님 id `visitorId`**(① 행 · `purchases[].visitorId` · 저장 `transactions.visitor_id`) · 없으면 그 수납 id(수납 하나 = 손님 하나). **이름으로 세지 않는다** — 동명이인은 두 명 | **D1-15** · **R§2 손님 셈 줄**(「시안 v2 · SPEC 0.3.0 OQ-126 의 『이름 기준』을 뒤집음」) |
| 결제 손님 수 `payingCustomers` | 그중(같은 키 — `visitorId` · 없으면 수납 id) **그달 ① `APPROVED` 행이 하나라도 있는** 수납을 가진 손님 수(취소 · 환불 줄만 있는 손님은 뺀다 · **승인 금액이 0 원이거나 같은 달 전액 취소로 순액이 0 이하인 손님도 센다** — 사용자 2026-10-29 「결제 0 원도 일단 포함해」) | 시안 v1 「정할 것」 · 기본값(OQ-126) |
| 수납 수 `purchases` | 그 에이전시의 그달 묶음 수 | 시안 v1 |
| 「에이전시 전체」 `agencyTotal` | 위 셋을 에이전시 수납 전부로 다시 센다(에이전시별 손님 수의 단순 합이 아니다 — **같은 `visitorId`** 가 두 에이전시에 걸리면 한 번 · 유입 채널은 손님당 하나라 그런 경우 0 — Q4) | D1-15 · 기본값 |
| 실결제 합 `netTotal` | 그 에이전시(「전체」면 에이전시 수납 전부)의 그달 수납 `netTotal`(§6.9 합 기준) 합 = **같은 화면 엑셀 「품목 금액」 열 합**(0.4.1 · D1-18 「기준은 품목 실결제 금액」 · doc r5 F-2). 통화가 섞인 수납이 하나라도 있으면 `null` · 수수료는 **없다**(D1-01 · D1-11) | D1-18 · D1-11 · OQ-132 |
| 받은 시점 | 판정은 저장된 ① 행의 유입 값으로 한다 — 받은 뒤 KOS 에서 손님 유입이 바뀌어도 저장본은 그대로(§4.6 ③) | D1-13 · OQ-109 |

### 6.9 최종 결제만 — 실결제 · 줄 · 합 기준 (D-18 · 0.4.0 · 0.4.1)

**규칙 한 줄: 화면 · 엑셀 = 손님이 최종적으로 어떤 상품을 얼마 냈나.** 취소된 결제 · 전액 환불 품목은 줄로 보이지 않고 숫자로만 센다(D1-18 · R§2 D-18 정정 줄 「최종적으로 취소된 거는 필요 없잖아」).

**합 기준(0.4.1 — doc r5 F-2 · OQ-132 코디 결정 · 사용자에게 추천안 통보 · 답이 오면 바뀔 수 있음): 실결제 = 품목 실결제 합 + 앞 달 결제의 이 달 취소(음수).** 수납 머리 · 손님 · 에이전시 실결제 합 · 엑셀 금액 합이 **이 하나로 같은 숫자**다.

| 항목 | 계약 | 근거 |
|---|---|---|
| 실결제 `netTotal`(수납 머리 · 합 기준) | **품목이 이 달에 있는 수납(`itemsHere = true`) = 품목 줄 금액 합(`itemsTotal` — ② `cost.totalAmount` = 남은 금액).** **품목이 다른 달인 수납(`itemsHere = false`)** — 원칙 「**달을 모두 더하면 KOS 최종 금액**」(R§2 마지막 줄 · 0.4.3 구현 `settle()`): (1) 품목 달에 **고정된 수납**(`pinned_elsewhere` — 이 달 판정은 품목이 여기인데 먼저 저장된 달이 가짐 · code r3 F-1) **또는 이 달에 취소 · 반환이 있는 수납**(부분 · 전액 취소 뒤 다른 금액 재승인 · be3-fix-2) = **이 달 살아 있는 승인 합**(이 달에 `canceledRefId` 로 전액 취소된 승인은 뺌 · ⑤ 와 못 이은 승인은 산 것) **+ 반영 안 된 취소 합(음수 — 아래 「반영 판정」)** — 양수일 수도 음수일 수도 있다 · 머리 글자는 「앞 달 결제 취소」 그대로 (2) **이 달 취소가 없는 분할 결제 나머지 = 0**(그 돈은 품목 달 품목 금액에 있다 → 숨김) — 고정 · 취소 없는 수납의 이 달 승인은 더하지 않는다(그 돈은 품목 달의 품목 금액에 이미 있다 — **분할 결제는 품목 달에 전액**: 9월에 X 만 내고 나머지 Y 를 10월에 내기로 한 수납은 9월 실결제 X+Y · 10월 0. Y 를 끝내 안 내도 9월은 X+Y 이고, 9월 `⚠ 결제 ≠ 품목`(`paymentsNet` X ≠ 품목 X+Y)으로만 드러난다 · D-06 결제 시각 귀속과 다른 자리 · 수집본에 이 꼴 없음 · doc r6 W-1 · OQ-132 에 같이 알림). 예: 승인 X → 전액 취소 → 같은 금액 재승인 · 품목 합 X → **X** · 승인 X → 전액 취소 → 다른 금액 Y 재승인 · 품목 합 Y → **Y** | **D1-18**(「기준은 품목 실결제 금액」) · D1-06 · OQ-132 |
| 결제 순액 `paymentsNet`(참고 · ⚠ 비교만) | 이 달 ① 의 그 수납 행 `cost.totalAmount.value` 합 — `APPROVED`(양수) + `CANCELED` · `SPENT`(음수) · `REQUESTED` · `FAILED` 는 빼고 `ignoredTransactions`. **화면 합 · 에이전시 합 · 엑셀에 쓰지 않는다** — `⚠ 결제 ≠ 품목`(§6.4)과 L20 에만 | D1-18 · doc r5 F-2 |
| 살아 있는 승인 | 같은 수납 ⑤ 에서 `canceledRefId` 로 그 승인을 가리키는 취소 금액 합 < 승인 금액인 승인(§6.2 s2 와 같은 판정). 결제일(`paidAt`) · 결제 수단 칩(`paymentTypes`)은 살아 있는 승인으로만 정한다. ⑤ 와 못 이은 승인은 살아 있는 것으로 본다(`unmatchedTransactions`). **판정은 그 달을 받을 때 하고 `month_purchases` 에 저장한다**(`paid_at_utc` · `payment_types` — §4.4) — 다른 달 받기로 ⑤ 가 갈아 끼워져도 확정 달 머리 결제일 · 칩은 바뀌지 않는다(D1-12 · D1-13 · doc r5 W-2). 이번 달은 증분에서 새 행이 생긴 수납만 다시 정한다 | D1-18 · §6.2 · doc r5 W-2 · OQ-132 |
| 취소된 결제 | 줄 없음. `canceledPayments` = 이 달 ① 의 `CANCELED` · `SPENT` 행 수(수납 · 달) — 건수 줄 「취소된 결제 a건」 · 머리 「취소 a」 · 엑셀 「정보」 시트 | **D1-18**(「건수만 숫자로」) · OQ-134 |
| 품목 줄 | `itemsHere = true` 인 수납의 ② 행 중 **`purchaseStatus` ∈ {`ACCEPTED` · `PAID` · `PARTIALLY_REFUNDED`}** 인 것만(금액 = `cost.totalAmount` — 남은 금액 · §6.3). 0원 결제 완료 품목은 보인다(차례 §3.3). `REFUNDED` 는 `refundedItems` 로 셈. **`INITIALIZED`(미수납 — 돈을 안 냄) · `PURCHASE_STATUS_UNSPECIFIED` · 그 밖 값은 「최종 결제」가 아니므로 줄 · 합 · 엑셀에서 빼고 `counts.excludedItems` 로 센다**(운영 수집본 0건 — doc r5 W-4 · OQ-137) | **D1-18** · §6.3 · OQ-137 |
| 앞 달 결제의 이 달 취소 | 그 수납은 이 달 묶음이 된다(D1-06) · 머리 실결제 = 이 달 **반영 안 된** 취소 합(음수 · 아래 「반영 판정」) · 품목 줄 없음 · 머리 「앞 달 결제 취소」 · **엑셀에도 음수 한 행**(§4.7 「앞 달 결제 취소」 행 — 반영 안 된 취소가 있을 때만) · 손님 · 에이전시 실결제 합에 음수로 들어감. 반영 안 된 취소가 0 이면 실결제 0 · 줄 0 → 숨김 | D1-06 · D1-18 · OQ-132(코디 결정) · doc r6 F-1 |
| **반영 판정**(doc r6 F-1 · 0.4.2) | 이 달 취소 · 반환 행 하나마다, 그 수납의 **품목 달**(저장된 `month_purchases.items_here = true` 인 다른 달)의 `items` 를 받은 시각(`items.fetched_at` = **② 응답을 받은 직후 시계** — 받기 시작 시각이 아니다 · 0.4.3 code r3 W-2 · 그 수납 품목 행들 중 가장 이른 값)과 그 취소의 시각을 **파싱한 시각으로** 비교한다(문자열 비교 금지). 취소 시각 = 저장 `transactions.at_utc`(⑤ `canceledDateTimeUtc` · `spentDateTimeUtc` — §5.4) · `at_utc` 가 없으면 그 행을 받은 시각 `transactions.fetched_at`. **취소 시각 < 품목을 받은 시각이면 「반영됨」** — 품목 달 ② `cost` 가 이미 그 환불 뒤 남은 금액이다(§6.3 · 수집본 392/392) → 이 달 실결제 · 엑셀에 더하지 않고 `counts.reflectedCancels` 로만 센다(건수 줄 · 「정보」 시트). **취소 시각 ≥ 품목을 받은 시각이면 「반영 안 됨」** → 음수로 더한다(품목 달은 받은 때 금액 그대로라 그 환불이 아직 없다). **품목 달이 저장돼 있지 않거나 그 수납 `items` 행이 없으면**(9월을 아직 안 받음 · `itemsMissing`) 「반영 안 됨」(음수로 보임) — 품목 달을 받은 뒤 다시 읽으면 「반영됨」으로 바뀌어 빠진다. 판정은 **읽을 때 한다**(저장값 아님 — §4.6 ⑧). 그래서 품목 달 금액 + 다른 달 「앞 달 결제 취소」 합 = KOS 의 최종 금액(전액 환불이면 0) | **D1-18**(「최종적으로 얼마 냈나」) · OQ-132 결정 문장 · doc r6 F-1 |
| **숨기는 묶음**(doc r5 W-1) | **실결제 0 · 보일 품목 줄 0** 인 수납은 묶음(머리)도 보이지 않는다 — 전액 환불 · 같은 달 전액 취소(품목이 전부 `REFUNDED`) · 품목이 다른 달인데 이 달 취소가 없는 수납(분할 결제 나머지 · 재결제만 이 달에 있음). `purchases[]` 에 넣지 않고 `counts.hiddenPurchases` 로만 센다(건수 줄 「숨긴 수납 h」 · 「정보」 시트). **`itemsMissing`(품목을 못 찾음) · `itemsNowhere`(품목이 어느 달에도 없음 — §4.4)는 실결제 0 · 줄 0 이어도 숨기지 않는다**(0.4.3 NOTE-1 — 빠뜨리지 않고 드러냄 · front 도 같은 규칙)(빠뜨리지 않고 드러낸다 — §6.4). 숨긴 수납의 손님도 **손님 수 · 결제 손님 수에 그대로 센다**(D-15 · D-16 — 결제 손님은 이 달 `APPROVED` 행이 있으면 0 원 · 순액 0 이하도 셈) | **D1-18** · D1-15 · D1-16 · OQ-132 |
| 에이전시 · 손님 | `agencies[].netTotal` · `agencyTotal.netTotal` = 그 수납들 `netTotal` 합(= 같은 화면 엑셀 「품목 금액」 열 합 · 숨긴 수납은 0 이라 상관없음). 손님 수 · 결제 손님 수는 D-15 · D-16 그대로(숨긴 수납 포함) · `agencies[].purchases` = 보이는 묶음 수 | D1-15 · D1-16 · D1-18 · doc r5 F-2 |
| 받은 시점 | **이번 달**: 증분이 새 행이 생긴 저장 수납의 ② · ⑤ 를 다시 불러 품목 상태 · 금액을 갈아 끼운다(§4.5 증분 5 — 같은 달 환불 · 재결제가 품목에 들어온다 · doc r5 F-1). **확정 달(`closed`)**: 품목 금액은 받은 때 남은 금액 그대로(D1-12 · D1-13). 그 뒤 다른 달에 환불되면 환불 돈은 환불된 달의 「앞 달 결제 취소」(음수 머리)로 그 달 실결제에서 빠진다. 품목 달을 환불 **뒤에** 받았거나 [전체 다시 받기] 했으면 품목 금액이 이미 남은 금액이므로 그 취소는 「반영됨」(더하지 않음 · `reflectedCancels`) → **어느 순서로 받아도 달을 모두 더하면 최종 금액**(위 「반영 판정」 · #61 ~ #63) | D1-12 · D1-13 · D1-06 |

## 7. 조회 전용 · 개인정보

### 7.1 조회 전용 가드 (`back/app/kos/client.py`)

`kos_collect.py` 의 가드(허용 경로 집합 + 경로에 `/queries/`)와 같은 모양을 코드에 둔다.

| 항목 | 계약 |
|---|---|
| 허용 경로 | **상수 집합 5개** — §5.1 ① ~ ⑤ 경로. 그 밖 경로 · 경로에 `/queries/` 가 없는 것 → 네트워크 전에 `GuardBlocked`(→ 500 `guard_blocked`) |
| 토큰 교환 | `exchange-token` 은 별도 상수 하나(인증 전용 함수에서만 부름) — 일반 호출 함수로는 부를 수 없다. 다시 받기는 잠금으로 한 번만(§4.4) |
| 내부 API | cc-prototype procedure 의 내부(`sign-in` · `tenants/{id}/…`) 호출부는 **복사하지 않는다** — 공개 API 만 |
| 메서드 | `POST` 만(KOS 공개 API 가 전부 POST — KA§1.2) |
| 시험 | 허용 밖 경로 · `/commands/` 경로를 부르면 가짜 transport 가 한 번도 불리지 않고 `GuardBlocked`(§9.1) |

### 7.2 운영 키

| 항목 | 계약 | 근거 |
|---|---|---|
| 허용 | 운영 명동점 키로 **이 프로젝트 코드 · WP-LIVE 실물 조회까지** — 조회만 · 로컬만 | **R§2(운영 키 줄 — 「10-29 확장: 이 프로젝트 코드 · WP-LIVE 실물 조회까지 같은 조건(조회만 · 로컬만)」)** · D1-05 · 검수 W-2 |
| 키 | **운영 명동점 공개 API 키** — `back/.env` 의 `KOS_OPEN_API_KEY` 에 넣는다. 원본은 ax-clinic-project `scripts/.env` 의 `KOS_API_tenent`(이름만 · 값은 그 파일에서 사람이 옮긴다) | R§2(운영 키 줄) · KA§1.2(cc-prototype procedure 는 데모 키 — 그쪽 운영 키 금지는 그대로) |
| 범위 | 이 키는 **이 레포 `back/.env` 에만** 둔다. cc-prototype 의 어떤 `.env` 에도 넣지 않는다 | R§2(운영 키 줄 「이 프로젝트 코드」 · 별도 프로젝트 줄) |
| 레포 | `back/.env` 는 gitignore · `.env.example` 은 이름만 · 커밋 전 `git status --ignored` 로 `.env` 가 추적되지 않음을 본다 | 코드(cc-prototype procedure `.env.example` 관례) · 레포 `.gitignore`(`.env` · `.env.*` · `!.env.example`) |

### 7.3 로그 · 노출

- back 은 **`127.0.0.1` 에만** 뜬다(`--host 127.0.0.1`) — 같은 Wi-Fi 의 다른 기기도 못 붙는다 · D1-09 · R§2(운영 키 줄 「로컬만」) · OQ-110
- CORS = `SALES_FRONT_ORIGIN` 하나 · 메서드 `GET` 만
- **③ · ④ 응답에서 꺼내는 것은 `visitor.name` · `reservation.startDateTime`(③) · `name`(④) 뿐**이다. ③ 응답(`ScheduleContract`)에 같이 오는 전화 · 생년월일 · 차트번호 · 메모 · 예약 메모, ④ 응답의 전화 · 여권 · 생년월일은 **변수에 남기지 않고 DB · 로그 · 응답에 싣지 않는다**(파싱 직후 두 값만 남김) · 검수 NOTE 3
- **⑤ 응답에서 꺼내는 것은 `data[].id` · `transactions[].{id, status, paymentType, price, paymentDateTime, canceledRefId, createdDateTimeUtc}` 뿐**이다. 같이 오는 `purchaseMemo`(자유 텍스트) · `items` · `assignees` · 거래 담당자 · 카드 설정은 남기지 않는다(DB 에도) · 검수 r2 NOTE 2
- **① · ② 에서 저장하는 것은 §4.4 `transactions` · `items` 표의 칸뿐**이다 — ① `visitorFunnelDetail` · `reservationFunnelName` · 그 밖 손님 칸, ② 의 손님 · 담당자 칸은 저장하지 않는다
- 로그에 남기는 것: 달 · 건수(`counts`) · `fetch`(mode · kosCalls · 새 행 수 · 중복 수) · `store.state` · 걸린 시간 · KOS 오류 이름 · `totalCount` ↔ 받은 행 수(숫자만) · 엑셀은 달 · `view` · 행 수(§4.7) · 0.4.3 구현 수: `itemsRefetched` · `filledLiveApprovals` · `changedPurchases` · `repaidAfterCancel`(이 달 취소 뒤 재승인 갈래를 탄 수납 수 — 드묾) — 전부 수만. **이름 · 금액 · 상품명 · 수납 id · 손님 id · 키 · 토큰 · 테넌트 id 를 남기지 않는다**. `httpx` 로그는 WARNING 이상만(요청 URL 이 찍히지 않게 — 코드 `main.py`)
- **저장은 `SALES_DB_PATH` SQLite 파일 하나뿐**(§4.4 · 0.3.0) — 이름 · 방문일 · 결제 · 품목이 들어 있는 **운영 개인정보 파일**이다: gitignore · 권한 600 · 이 맥 밖으로 옮기지 않는다(복사 · 업로드 · 스크린샷 금지) · 레포 · 리포트에 파일 내용(행 · 값)을 붙이지 않는다 · 필요 없어지면 파일을 지운다. 그 밖 파일 · 브라우저 저장소(`localStorage` 등) 0 · 메모리 캐시 0
- 오류 응답 · 로그에 DB 경로의 사용자 홈 · SQL 문 · 행 값을 싣지 않는다(`store_failed` 는 문구만 — §4.3)
- 이 화면의 스크린샷 · 실물 확인 결과를 레포(public)에 올릴 때는 이름 · 금액 · 유입 이름을 가린다(§9.2)

## 8. 디자인 — cc-prototype procedure/front 에서 복사할 것

cc-prototype 레포의 `procedure/front` 를 **복사**한다(import · 링크 금지 — D1-08). 복사한 파일 머리에 `// 원본: cc-prototype procedure/front/<경로> (복사 — 레포끼리 공유 없음)` 한 줄.

| 복사 | 원본(`procedure/front/`) | 고칠 것 |
|---|---|---|
| Tailwind 설정 | `tailwind.config.ts` | 그대로(medikit preset · `typo-heading-sm-600`) |
| PostCSS | `postcss.config.mjs` | 그대로 |
| 테마 | `app/styles/ceramique-theme.css` | 그대로 |
| medikit 보정 | `app/styles/medikit-patches.css` | 그대로 |
| 공통 스타일 | `app/globals.css` | 쓰는 규칙만(`html,body` · `a` · `.cc-btn` 등) — 안 쓰는 현황판 규칙은 옮기지 않는다 |
| 루트 레이아웃 | `app/layout.tsx` | import 차례(pretendard → medikit styles → 테마 → 보정 → globals) · `<html lang="ko" data-product="ceramique">` 그대로 · `flag-icons` 빼기 · 제목 「Céramique 명동점 · 월별 매출」 · `robots noindex` |
| 로고 | `public/ceramique-logo-color.svg` | 그대로(머리 왼쪽) |
| 시각 도우미 | `lib/time.ts` | KST 함수(`pad` · `toMs` · `hm`)만 + `md`(MM-DD) · 월 계산 |
| API 바탕 | `lib/api.ts` 의 `API_BASE` · `CONFIG_ERROR` 부분 | 세션 · 다른 호출 빼고 `getSales(month, refresh)` 하나. 안내 경로 `front/.env.local` |
| 의존성 | `package.json` | `@medisolve-ai/medikit` **1.4.0**(같은 판) · `next` · `react` · `react-dom` · `pretendard` + dev(tailwind · postcss · autoprefixer · typescript · eslint · eslint-config-next · `@types/*`). `flag-icons` · `qrcode` 빼기 · 스크립트 포트 3800(§10) |
| 린트 · TS 설정 | `eslint.config.mjs` · `tsconfig.json` · `next.config.ts` · `global.d.ts` | `output: 'standalone'` 빼도 됨(배포 없음) |

- **헤더(0.3.0)**: `components/common/AppHeader.tsx` 를 복사해 **세션 · 로그아웃 · 시계 · 시술 현황 링크를 빼고** 메뉴 「월별 조회 \| 에이전트별 조회」 두 개 + 오른쪽 지점 이름 · 「운영 · 조회 전용」 칩만 남긴다(시안 v1 헤더 = AppHeader 꼴 · D1-10)
- **안 복사**: `lib/session.ts` · `lib/hooks.ts` 의 세션 훅 · `app/login` · `(main)` 묶음
- medikit 컴포넌트는 패키지에서 바로 쓴다(복사 아님): `Button`(월 이동 · 새 결제 받기 · 전체 다시 받기 · 다시 시도 · 메뉴 · 에이전시 탭 — 탭 · 메뉴 모양은 시안 v1 · v2) · `Badge`(상태 · 결제 수단 · 경고) · `Loading`(불러오는 중). 표는 일반 `<table>` + Tailwind(medikit 1.4.0 에 표 컴포넌트를 cc-prototype procedure 가 안 쓴다 — 코드 import 집계)
- medikit 설치는 cc-prototype procedure/front 와 같은 방식(사용자 npm 설정) — 이 문서는 레지스트리 · 토큰을 적지 않는다

## 9. 검증

### 9.1 back 단위 시험 (pytest · KOS 가짜 transport · 운영 호출 0)

> **0.4.0 읽는 법**: #1 ~ #44 가운데 `payment` · `cancel` · `spent` 줄 · 음수 줄 · `at`(결제 · 취소 줄) · `approvedTotal` 을 단언하는 곳(#3 ~ #5 · #17 · #21 · #22 · #28 · #33 등)은 **같은 사례를 #45 ~ #53 의 규칙으로** 단언한다 — 줄 대신 머리 `netTotal` · `canceledPayments` · `refundedItems`, `paidAt` 은 살아 있는 승인. 판정(§6.2 s1 ~ s5 · 잇기 §5.4 · 저장 · 증분)은 그대로라 그 부분 단언은 바뀌지 않는다

| # | 시험 |
|---|---|
| 1 | 월 경계 — `2026-10` → `from 2026-09-30T15:00:00Z` · `to 2026-10-31T14:59:59Z` · 12월 → 다음 해 1월 경계 · `bad_month`(꼴 · 13월 · 다음 달) |
| 2 | 조회 전용 가드 — 허용 밖 경로 · `/commands/` 경로 → `GuardBlocked` · 가짜 transport 호출 0 · 토큰 교환은 인증 함수에서만 · 허용 경로 상수가 정확히 5개 |
| 3 | 조인 — 승인 결제 2행(카드 · 현금) + 품목 2행 → 묶음 1 · 품목 줄 2 · `paymentTypes` 2 · `paidAt` = 이른 쪽 |
| 4 | 취소 — 같은 달 승인 + 취소 → 품목 줄 + 음수 `cancel` 줄 · 취소만 있는 수납 → 품목 줄 0 · `paidAt null` |
| 5 | `SPENT` → 음수 `spent` 줄 · `REQUESTED` · `FAILED` → 줄 0 · `ignoredTransactions` 증가 |
| 6 | 상품명 — `productTitle` 빈 품목이 `prepaidCardName` · `etceteraProductName` 순으로 · 다 비면 `none` |
| 7 | 유입 빈 값 → `visitorFunnelName null` · `visitorFunnelDetail` 에 값이 있어도 응답 어디에도 안 나옴 |
| 8 | 품목 없음 → `itemsMissing true` · `counts.itemsMissing` · 결제 ≠ 품목 → `paymentsNet ≠ itemsTotal` 그대로 |
| 9 | **「없음」** — ③ 이 400 `{errorProperties:[{key:"purchaseId",reason:"NotFound"}]}` → ④ 로 이름 · `visitDate null` · ④ 도 400 `{key:"visitorId",reason:"NotFound"}` → `visitorName null` · `visitorMissing` 1 · 달은 200 |
| 9b | **「없음」 아님** — ③ 이 400 이지만 다른 reason(예: `{key:"purchaseId",reason:"Required"}`) → 달 전체 502 `kos_rejected` · ③ 404 → 달 전체 502 `kos_rejected`(「없음」으로 삼키지 않음) · ③ 500 → 502 `kos_unavailable` |
| 10 | 페이지 — ① 이 `nextCursor` 를 주면 다음 요청에 `cursor` · `limit` 같이 · 끝까지 · `counts.transactions` = 첫 페이지 `totalCount` |
| 11 | 오류 매핑 — 429 → 503 `kos_busy` · 401 → 토큰 다시 받기 1회 → 또 401 → 502 `kos_rejected` · 네트워크 → 502 `kos_unavailable` · 키 비어 있음 → 503 `kos_not_configured` |
| 12 | **저장 · 줄 선 요청**(0.3.0 · 0.3.1 doc r3 W-4) — 같은 달 두 번째 요청(신선한 `current` · `closed`)은 KOS 호출 0 · `cached true` · `fetch.mode none` · `kosCalls 0` · 첫 요청과 응답 본문이 같다(`store` · `fetch` · `cached` 빼고) · `refresh=1` → 400 `bad_refresh` · 동시 두 요청(같은 달)에서 **(a) 값 없음 · (b) 둘 다 `refresh=new` · (c) 둘 다 `refresh=full`** 세 경우 모두 ① 호출 1 · 뒤 요청 `fetch.mode none` |
| 13 | 동시성 — ③ 이 동시에 `SALES_KOS_CONCURRENCY` 를 넘지 않음 |
| 14 | 로그 — caplog 에 가짜 이름 · 가짜 금액 · 수납 id · 키 · 토큰 문자열 0 |
| 15 | 경로 수 3(`sales` · `sales.xlsx` · `health` — 0.3.0) · 응답 헤더 `Cache-Control: no-store` · CORS 허용 출처 하나 |
| 16 | 시각 오프셋 — ③ `startDateTime` 이 `2026-10-03T23:30:00Z` → `visitDate 2026-10-04` · `2026-10-03T23:30:00+09:00` → `2026-10-03` |
| 17 | 분할 결제 — ⑤ 첫 승인이 9월 · ① 10월 승인 1행 → 10월 묶음 품목 줄 0 · 줄 0 · 이 달 취소가 없으므로 **숨김**(`hiddenPurchases` 1 · 0.4.1) · `itemsHere false` · `counts.itemsElsewhere` 1 · 같은 수납을 9월로 조회하면 품목 줄 있음 · ⑤ 에 수납이 없으면 이 달 승인 행으로 봄 + `firstApprovedUnknown` 1 · ⑤ 가 100개씩 나뉘어 불림 |
| 18 | 통화 — 줄 `currency` 가 KOS 값 그대로 · 한 수납에 `KRW` · `USD` 가 섞이면 수납 `currency null` · `netTotal null` · `itemsTotal null` |
| 19 | 토큰 다시 받기 잠금 — ③ 8개가 동시에 401 → 토큰 교환 호출 1 |
| 20 | 개인정보 — 가짜 ③ 응답에 전화 · 생년월일 · 메모 값을 넣어도 응답 · **SQLite 파일(모든 표 · 모든 칸을 덤프)** · caplog 어디에도 없음 |
| 21 | **결제일 = ⑤ 시각(§5.4)** — 동점 가르기 시각이 `…T01:02:03Z` ↔ `…T01:02:03.000+00:00` 처럼 표기만 다르면 같은 시각으로 잇는다(NOTE 1) — ① 승인 1 · 취소 1 + ⑤ 같은 거래(승인 `approvedDateTimeUtc` · 취소 `canceledDateTimeUtc` · ① `lastUpdatedPaymentDateTimeUtc` 는 다른 값)를 주면 `paidAt` · 결제 줄 `at` = 승인 일시 · 취소 줄 `at` = 취소 일시 · 응답 어디에도 ① `lastUpdatedPaymentDateTimeUtc` 값 없음 · 같은 수단 · 같은 금액 승인 2건은 `lastUpdated` 로 갈라 잇는다 · ⑤ 에 맞는 거래가 없으면 줄은 남고 `at null` · `unmatchedTransactions` 1 · ⑤ 시각이 다음 달(11-01 KST)이면 묶음은 10월에 남고 `atOutsideMonth` 1 · 정렬은 ⑤ 시각 차례 · 시각 없는 묶음 맨 뒤 |
| 22 | **(a) 전액 취소된 승인** — ⑤ 9월 승인 A · 9월 취소(`canceledRefId` = A · 같은 금액) · 10월 승인 B, ① 9월(A · 취소) · 10월(B) → **10월에 품목 줄 · `itemsHere true`** · 9월엔 품목 없이 머리만(실결제 = A − 취소 = 0 · `canceledPayments 1`) · `firstApprovalCanceled` 1. 부분 취소(취소 금액 < A)면 A 가 첫 승인으로 남아 9월에 품목 · 10월은 머리만. 수납 전체 취소(A 만 · 전액 취소)면 9월에 품목(전액 취소 수납이라 품목 상태가 환불이면 줄 0 · `refundedItems`) + `canceledPayments` |
| 23 | **(b) 자정 경계** — ⑤ 첫 승인 `approvedDateTimeUtc` = 11-01 00:00 KST · ① 10월 조회에 그 행이 있고(§5.4 로 이어짐) 11월 조회엔 없음 → **10월 `itemsHere true`** · 11월 결과에 그 수납 없음 · 10월 · 11월을 합쳐 품목 줄이 정확히 한 번 |
| 24 | **(c) ⑤ 시각 없음** — 분할 결제 수납(9월 승인 A · 10월 승인 B)에서 A · B 모두 `approvedDateTimeUtc` 없음 · `createdDateTimeUtc` 있음 → 9월 · 10월 조회가 같은 「첫 승인」(A)을 고르고 품목은 9월에만 · 두 달 다 `firstApprovedUnknown` 1. A 가 9월 ① 행과 못 이어지고 9월 ① 에 못 이은 승인 행이 있으면 A 의 `createdDateTimeUtc` 달(9월)로 9월 `itemsHere true` |

| 25 | **지난 달 = 한 번** — 시계 = 11-05 · `month=2026-10` 첫 요청 → `fetch.mode full` · `store.state closed` · 같은 달 다시(값 없이 · `refresh=new`) → KOS 호출 0 · **새 서비스 인스턴스(같은 DB 파일 — back 재시작 흉내)로 다시 → KOS 호출 0**(J3) |
| 26 | **이번 달 증분 범위(0.3.1)** — 시계 10-29 14:00 첫 요청(full) → 10-29 14:20 `refresh=new` → ① 한 번 · 요청 `createdTimeUtcFrom` = **달 시작**(`2026-09-30T15:00:00Z`) · `fetch.fromUtc` 같음 · `store.fetchedAt` = 14:20 · ② · ③ · ⑤ 호출 0(새 행 없음) · `kosCalls` = ① 수(+ 토큰) |
| 27 | **새 행 = 수(0.3.1 · doc r3 F-2 · W-7)** — (a) 증분 ① 이 저장 행 3개 + 새 행 1개(다른 묶음)를 주면 저장 행 +1 · `duplicateTransactions 3` · `newTransactions 1`. (b) **저장된 카드 승인 A(500,000)와 같은 수단 · 같은 금액의 새 승인 B** → 저장 행 +1 · 그 수납 ⑤ 다시 부름 1 · `newTransactions 1` · `duplicateTransactions 0`(A 다시 온 것 1 이면 1) · 승인 합 +500,000 → B 의 `tx_id` ≠ A. (c) 같은 금액 부분 취소 두 번 → 음수 줄 2. (d) 저장 행 A 의 `last_updated` 만 바뀌어 다시 옴 → 새 행 0(두 번 안 들어감). (e) KOS 가 저장 행보다 1 적게 줌 → 저장 행 그대로 · `missingTransactions 1`. (f) 앞 받기 뒤 늦게 통계에 들어온(만든 시각이 앞 `fetched_at` 보다 이른) 행 → 새 행으로 들어옴 (g) **「바뀜」**(0.4.3 · code r2 W-1) — 같은 수납에서 저장 행 하나가 상태 · 금액이 바뀌어 다시 옴(남는 묶음 + 모자란 묶음) → 그 수납 이 달 행 = KOS 대로 · 두 번 들어가지 않음 · `newTransactions` · `missingTransactions` 각 1 · 로그 `changedPurchases=1` |
| 28 | **새 수납 · 새 거래만 다시 봄** — 증분에 ① 새 수납 P2(승인) + 저장된 P1 의 새 취소 행: ⑤ 는 P1 · P2 둘만(1 회) · ③ 은 P2 만 · ② 는 P2 가 `itemsHere` 일 때만 1 회(그 결과에서 P2 품목만 저장) · P1 품목 · 이름은 다시 안 받음 · P1 에 음수 `cancel` 줄 +1 |
| 29 | **J6 신선도** — `current` 를 받은 지 `SALES_CURRENT_STALE_SEC` 안이면 값 없는 요청은 KOS 0 · 넘으면 증분 1 회 |
| 30 | **확정(달이 바뀜)** — 10-31 23:50 에 10월 full(`current`) → 시계 11-01 00:05 에 10월 요청 → J4 증분 · 아직 `current`(겹침 여유 안) → 11-01 00:20 요청 → 증분 · `closed` · `closedAt` → 11-02 요청 → KOS 0. 11월(이번 달)은 같은 때 `current` |
| 31 | **전체 다시 받기 · 갈아 끼우기 범위(doc r3 F-3)** — `refresh=full` 이 그 달 저장 행을 지우고 다시 받음(① 이 행을 하나 덜 주면 응답에서도 하나 빠짐) · ② 품목 상태가 바뀐 가짜를 주면 배지가 새 상태(§4.6 ①) · 다른 달 저장 행 수 그대로 · `closed` 달도 받은 뒤 `closed` · **9월이 품목을 가진 분할 결제 수납 X(10월 `items_here false`) → 10월 전체 뒤에도 9월 응답의 X 품목 줄 수 그대로 · 9월 `itemsMissing` 0** · X 의 `visitors` · `purchase_txs` 는 갈아 끼워짐 |
| 32 | **실패하면 안 바뀜** — 증분 · 전체 중 ③ 이 500 → 502 `kos_unavailable` · DB 의 모든 표 행 수 · `months` 행이 요청 전과 같음 · 다음 요청이 같은 `fromUtc` 로 다시 받음 |
| 33 | **품목 달 고정** — 수납 X 가 9월 저장본에서 `itemsHere true` · 10월 증분에서 ⑤ 가 바뀌어(9월 승인 전액 취소 · 10월 승인) 판정이 `itemsHere true` 가 나와도 10월은 품목 줄 0 · 머리만(실결제) · `itemsPinnedElsewhere 1` · 9월 응답 그대로(§4.6 ②) |
| 34 | **에이전시 판정** — `visitorFunnelName` = `에이전시A(에이전시)` · ` 에이전시B(에이전시) `(앞뒤 공백) → `agency` 는 공백 뗀 값 · `에이전시C(에이전시)메모` · `（에이전시）`(전각) · `(에이전시)가 아님` · `null` → `agency null` · `agencies` 이름 차례 · 그달 수납 없는 에이전시는 목록에 없음 · `visitorFunnelDetail` 에 「(에이전시)」가 있어도 `agency null` |
| 35 | **손님 수(D-15)** — 승인 금액 0 원 손님 · 같은 달 전액 취소 손님도 `payingCustomers` 에 셈 · 에이전시A: **이름이 같고 `visitorId` 가 다른 수납 2 → 손님 2**(동명이인) · `visitorId` 가 같은 수납 2 → 손님 1 · `visitorId` 없는 수납 → 수납 id 로 손님 1 · 그중 취소 줄만 있는 손님은 `payingCustomers` 에서 빠짐 · `purchases` = 묶음 수 · 이름이 바뀌어도(같은 `visitorId`) 셈 그대로 · 「새로 받음」: 증분으로 처음 저장된 수납만 `newInLastFetch true` · 그 뒤 전체 받기면 전부 `false` · `agencyTotal` 은 에이전시 수납 전부로 다시 셈 · 응답에 에이전시 금액 합 필드 0 |
| 36 | **저장 칸 · 권한(doc r3 W-6)** — SQLite 의 표 · 칸 목록이 §4.4 표의 칸과 같음(그 밖 칸 0 · `json` · `raw` · `body` 꼴 칸 0) · `data/` 폴더 700 · 본 파일 · `-wal` · `-shm` 모두 600(쓰기 뒤 확인) · `SALES_DB_PATH` 가 없는 폴더면 만듦 · 레포 안 `back/data/` 밖 경로 · `.db` 확장자면 뜨지 않음 · `schema_version` 이 다른 파일이면 뜨지 않고 파일이 그대로 남음(NOTE-3) · 경로 수 3(#15) |

| 37 | **엑셀 KOS 0** — 저장된 10월에 `sales.xlsx?month=2026-10` · `view=agency` · `view=agency&agency=에이전시A(에이전시)` → 가짜 transport 호출 0 · 저장 안 된 달 → 409 `not_fetched` · KOS 0 · `view=foo` → 400 `bad_view` |
| 38 | **엑셀 행 = 화면 줄**(+ 수식 막기 — 상품명 `=1+1` · 옵션 `+A1` · 손님 이름 `@SUM(1)` · 유입 `-1` 인 가짜 수납 → 다시 읽은 셀 `data_type == "s"` · 값이 글자 그대로 · 수식 셀 0) — `openpyxl` 로 다시 읽어: 1행 헤더 11칸이 D-14 차례 · 행 수 = 같은 거르기의 `/api/sales` `lines` 합 · 0원 품목 줄 · `payment` · 음수 `cancel` 줄이 다 있음 · 합계 행 없음 · 금액 셀 숫자형(음수 그대로) · 결제일 날짜형 · 수납 id 글자형 전체 · 빈 값은 빈 칸 |
| 39 | **엑셀 이름 · 파일** — 품목 종류 · 상태 · 결제 수단이 한글 이름 · back `labels.py` 표 = front `labels.ts` 표(같은 키 · 같은 값) · 파일 이름 3꼴 · 못 쓰는 글자 `_` · `Content-Disposition` 에 `filename*=UTF-8''` · `no-store` · 시트 「정보」 에 받은 시각 · 상태 |
| 40 | **엑셀 로그** — caplog 에 가짜 이름 · 가짜 에이전시 이름 · 금액 · 수납 id · 파일 이름 0 · 서버 디스크(작업 폴더 · 임시 폴더)에 xlsx 파일 0 |
| 41 | **두 달 동시 받기(doc r3 W-1)** — 저장 없는 9월 · 10월을 동시에 요청(KOS 가짜가 둘 다 끝날 때까지 기다리게)하고, ⑤ 에 수납이 없는 분할 결제 수납 Y(두 달 다 「이 달 승인 행 있음 → itemsHere」 대체) → 두 달 합쳐 Y 품목 줄 정확히 한 번 · 늦게 쓴 달 `itemsPinnedElsewhere 1` |
| 42 | **품목이 어느 달에도 없음(doc r3 W-2)** — 9월 X 품목 · 10월 `pinned_elsewhere` 상태에서 ⑤ 가짜를 바꿔(9월 첫 승인 전액 취소) **9월만** `refresh=full` → 9월 X `items_here false` · 10월 응답 X `itemsNowhere true` · `counts.itemsNowhere 1` · `itemsPinnedElsewhere 0` · KOS 0(10월 요청) → 10월 `refresh=full` → 10월 X 품목 줄 · `itemsNowhere 0` |
| 43 | **증분에서 itemsHere 가 바뀜(doc r3 W-3)** — 10월에 X 를 `items_here false` 로 저장(`items` 없음) → 증분에서 X 첫 승인의 전액 취소 행이 들어와 다시 판정 `true` → ② 한 번 · X 품목 줄 저장 · `itemsMissing 0` |
| 44 | **전체 받기 지우기도 한 트랜잭션(NOTE-5)** — `refresh=full` 중 ② 가 500 → 그 달 `transactions` · `month_purchases` · `items` 행 수가 요청 전과 같음 |
| 45 | **실결제 — 같은 금액 재결제**(0.4.0 · D-18) — ① 이 달 승인 X → 취소 −X → 승인 X · ⑤ 취소 `canceledRefId` = 첫 승인 · ② 품목 합 X → 머리 `netTotal` = X(품목 합) · `paymentsNet` = X · `itemsTotal` = X · `⚠ 결제 ≠ 품목` 없음 · `canceledPayments 1` · 줄은 품목만(결제 · 취소 줄 0) · `paidAt` = **둘째 승인** 시각 · `paymentTypes` = 둘째 승인 수단 |
| 46 | **실결제 — 다른 금액 재결제** — 승인 X → 전액 취소 → 승인 Y(Y < X) · ② 품목 3개 합 Y → `netTotal` = Y · ⚠ 없음 · 처음 결제의 품목 구성은 응답 어디에도 없음 |
| 47 | **전액 환불 품목** — ② 품목 2(하나 `REFUNDED` · `cost` 0) · ① 승인 + 부분 취소 → 품목 줄 1 · `refundedItems 1` · `lines` 에 `REFUNDED` 0 · 품목이 전부 `REFUNDED` 인 수납 → 줄 0 · `itemsMissing false` · `refundedItems` = 품목 수 |
| 48 | **부분 환불** — `PARTIALLY_REFUNDED` 품목 `cost.totalAmount` = 남은 금액 → 줄 금액 = 그 값 · 상태 `부분 환불` · 응답 · 엑셀에 「원래 금액」 · 「환불된 금액」 필드 0 · ① 승인 + 부분 취소 합 = 품목 합 → ⚠ 없음 |
| 49 | **앞 달 결제의 이 달 취소** — 9월 승인 · 10월 취소만 → 10월 묶음 머리만 · `netTotal` 음수 · 줄 0 · `canceledPayments 1` · 에이전시 수납이면 `agencies[].netTotal` 에 음수로 들어감 · 손님은 셈 · 결제 손님은 안 셈(D-16 — 이 달 승인 없음) |
| 50 | **분할 결제(여러 승인 · 취소 없음)** — 같은 달 카드 X + 현금 Y → `netTotal` X+Y · 칩 2 · 줄은 품목만 / 다음 달 나머지 결제 → 그 달 **숨김**(`netTotal` 0 · `hiddenPurchases` 1 — 0.4.1 · 그 돈은 품목 달의 품목 금액에 있다) · 다음 달에 그 나머지를 취소하면 그 달 머리 「앞 달 결제 취소 −Y」 |
| 51 | **0원 품목 차례** — ② 차례가 [0원 a · 유료 P · 0원 b · 유료 Q · 0원 c] → 줄 차례 P · a · b · Q · c(앞 유료 바로 아래 · 앞 유료가 없는 a 는 첫 유료 아래) · 유료가 없는 수납은 ② 차례 그대로 · 응답에 「구성품」 · 부모 id 필드 0 |
| 52 | **에이전시 실결제 합(0.4.1 합 기준)** — 에이전시A 수납 3(품목 합 X · 품목 합 Y · 앞 달 결제 취소 −Z) → `agencies[].netTotal` = X+Y−Z(`paymentsNet` 합이 아니다 — 분할 결제 나머지 +W 가 있어도 더하지 않음) · `agencyTotal.netTotal` = 에이전시 수납 전부 합 · 통화 섞인 수납이 있으면 `null` |
| 53 | **엑셀(0.4.0)** — 행 = 최종 결제 품목 줄만(`REFUNDED` · 결제 · 취소 행 0 · 0원 품목 있음 · 차례 #51) · 「품목 금액」 = 남은 금액 · 「원래 금액」 칸 없음 · 11칸 헤더 D-14 그대로 · 시트 「정보」 에 `canceledPayments` · `refundedItems` · `hiddenPurchases` · `excludedItems` 수(그 화면 거른 수납만) · **「앞 달 결제 취소」 음수 행**(품목 종류 · 금액 = 수납 `netTotal`) |
| 54 | **같은 달 전액 환불 증분(doc r5 F-1)** — 10-20 전체 받기(품목 P `ACCEPTED`) → 10-25 증분: ① P 수납 취소 행 · 가짜 ② 에서 P `REFUNDED` · `cost` 0 → ② 호출 1 · P 줄 0 · `refundedItems 1` · 실결제 0 · 줄 0 이면 숨김 · ⚠ 없음 · 엑셀 행 0 |
| 55 | **같은 달 부분 환불 증분** — 같은 꼴 · ② P `PARTIALLY_REFUNDED` · 남은 금액 → 줄 금액 = 남은 금액 · `부분 환불` · `netTotal` = 남은 금액 · `paymentsNet` = 같음 · ⚠ 없음 |
| 56 | **재결제 증분** — 승인 X(품목 A · B) → 받기 → 전액 취소 + 다른 금액 Y 재승인(가짜 ② 품목 C) → 증분: ⑤ · ② 다시 · 줄 = **C 만**(A · B 0) · `netTotal` = Y · `paidAt` = 재승인 시각 · 같은 수납이 9월(`closed`)에 품목을 가진 경우엔 ② 를 불러도 9월 `items` 안 바뀜 |
| 57 | **엑셀 합 = 화면 합(doc r5 F-2)** — 10월 에이전시A 에 품목 수납 2 · 앞 달 결제 취소 1 · 분할 결제 나머지만 있는 수납 1 → 엑셀 「품목 금액」 열 합 = `agencies[].netTotal` = 화면 머리 합 · 분할 나머지 수납은 화면 · 엑셀에 없음 · 시트 「정보」 실결제 합 같음 |
| 58 | **숨기는 묶음(doc r5 W-1)** — 같은 달 「승인 → 전액 취소」만 있는 수납(품목 전부 `REFUNDED`) → `purchases[]` 에 없음 · `hiddenPurchases 1` · 그 손님은 `customers` · `payingCustomers`(이 달 승인 있음 — D-16)에 셈 · `itemsMissing` 수납(품목을 못 찾음)은 실결제 0 이어도 보임 |
| 59 | **살아 있는 승인 고정(doc r5 W-2)** — 9월(`closed`) 승인 A 수납 X 의 머리 결제일 · 칩 기록 → 10월 증분이 A 의 취소를 받아 X 의 ⑤ 를 갈아 끼움 → 9월 응답 X 의 `paidAt` · `paymentTypes` 그대로(저장값) · 10월 X 는 「앞 달 결제 취소」 |
| 60 | **최종 결제 상태 경계(doc r5 W-4)** — ② 품목 `INITIALIZED` · `PURCHASE_STATUS_UNSPECIFIED` 하나씩 → 줄 · `itemsTotal` · 엑셀 0 · `excludedItems 2` · `PAID` 는 `결제 완료` 로 보임 |
| 61 | **품목 달을 환불 뒤 처음 받음(doc r6 F-1)** — 10월 먼저 받음: 9월 수납 P(품목 500,000)의 10월 부분 환불 −200,000 → 10월 머리 「앞 달 결제 취소 −200,000」(9월 저장 없음 → 반영 안 됨). 그 뒤(시계 = 환불 뒤) 9월 처음 받기 → ② P `cost` 300,000 · `items.fetched_at` > 취소 시각 → 10월 다시 읽기: 그 취소 「반영됨」 · 10월 그 수납 숨김 · `reflectedCancels 1` · 엑셀 행 0 · **9월 + 10월 합 = 300,000**(KOS 최종 · KOS 호출은 9월 받기뿐) |
| 62 | **품목 달 [전체 다시 받기]** — 9월을 환불 전에 받음(P 500,000) · 10월 −200,000 → 합 300,000(반영 안 됨 · 음수 더함). 9월 `refresh=full`(환불 뒤 · ② P 300,000) → 10월 다시 읽기: 「반영됨」 · 합 **300,000 그대로** · 앞뒤 둘 다 KOS 최종과 같음. 취소 `at_utc` 가 없는 행은 `transactions.fetched_at` 으로 같은 판정 · 시각은 파싱해 비교(`…Z` ↔ `+00:00` 표기 차이 무시) |
| 63 | **다른 달 전액 환불** — 9월 P(500,000) · 10월 전액 취소. (a) 9월을 환불 전에 받음 → 9월 500,000 + 10월 −500,000 = **0** (b) 9월을 환불 뒤 받음 → 9월 P `REFUNDED` · 숨김 · 10월 취소 「반영됨」 · 숨김 → **0** · 두 경우 다 엑셀 합 = 화면 합 = 0 · 손님 셈 그대로(D-15 · D-16) |
| 64 | **고정 수납의 취소 + 다른 금액 재승인(code r3 F-1)** — 10-05 에 9월 받음(수납 P 승인 500,000 · 품목 500,000 · `closed`) → 10월 P 전액 취소 −500,000 · 다른 금액 재승인 300,000 → 10월 P `itemsHere false` · `pinned_elsewhere` · 실결제 = 300,000 − 500,000 = −200,000 · **9월 + 10월 = 300,000(KOS 최종)** · 에이전시 합 · 엑셀 「품목 금액」 합 같음 · 같은 금액 재승인 · 부분 취소 뒤 재승인 꼴도 두 달 합 = KOS 최종 |
| 65 | **반영 판정 기준 = ② 받은 직후(code r3 W-2)** — 9월 [전체 다시 받기] 시작(`started`) 뒤 · ② 를 부르기 전 시각에 환불이 처리된 꼴(가짜 시계) → `items.fetched_at` = ② 응답 직후 시각 > 취소 시각 → 「반영됨」(10월에 두 번 안 빠짐) |
| 66 | **부분 취소 뒤 다른 금액 재승인(be3-fix-2)** — 9월 품목 500,000 · 10월 취소 −200,000 + 재승인 100,000 → 10월 실결제 −100,000 · 두 달 합 400,000 · 분할 결제 나머지(취소 없음) 꼴은 그대로 0 · 숨김 · 엑셀 · 에이전시 합 같음 · 로그 `repaidAfterCancel=1`(수만) |
| 67 | **front 차례 · 글자 · 숨김(0.4.3)** — 가짜 back 이 시각 차례가 아닌 차례로 주면 화면 묶음 차례 = back 차례 · `paidAt null` 「앞 달 결제 취소」 머리의 결제일 칸 = 「앞 달 결제 취소」(「시각 없음」 0) · `itemsNowhere` · 실결제 0 · 줄 0 수납 보임 · 본문 · 헤더 최대 폭 1600 가운데 |

### 9.2 운영 KOS 실물 조회 (완료 조건 · 10월 · 1회)

근거: R§2(운영 키 줄 — 「이 프로젝트 코드 · WP-LIVE 실물 조회까지 · 조회만 · 로컬만」). 코디가 `back/.env` 에 운영 키를 넣고(§7.2) 로컬에서 back · front 를 띄워 **`month=2026-10` 한 번** 조회한다.

| # | 확인 | 통과 |
|---|---|---|
| L1 | 화면에 10월 리스트가 뜬다(수납 묶음 · 품목 줄 · 칸 §3.2) | 눈으로 |
| L2 | `counts.transactions` = ① 첫 페이지 `totalCount` | 같음 |
| L3 | `counts.purchases` = ① 수납 id 중복 없이 센 수 | 같음 |
| L4 | `counts.itemsMissing` | 0 이거나, 0 이 아니면 그 수와 수납 id 끝 4자리를 보고(레포 밖) — DEC-001 Context(392/392)와 비교 |
| L5 | `itemsHere = true` 이고 `paymentsNet ≠ itemsTotal`(0.4.1 — 결제 순액) 인 수납 수 | 수만 보고. 참고 기준 = 444/444 일치의 정의(수납마다 「`REFUNDED` 아닌 품목 합」 = 「결제 행 `APPROVED` + `CANCELED` 전부 합」 — §6.3). 리스트 비교(그달 승인 합 ↔ 품목 전부 합)는 정의가 달라 환불이 낀 수납은 다를 수 있다 |
| L6 | `counts.canceledPayments` = ① `CANCELED` · `SPENT` 행 수(0.4.0 — 줄 대신 수) | 같음 |
| L7 | `visitorFunnelName` 빈 수납 수 · `visitorMissing` 수 | 수만 보고 |
| L8 | KOS 호출 로그(경로만)에 `/commands/` 가 토큰 교환 1개뿐 | 0 건(토큰 교환 빼고) |
| L9 | back 로그에 이름 · 금액 · 키 0 | grep 0 |
| L10 | `REFUNDED` · `PARTIALLY_REFUNDED` 품목이 있는 수납 수 · 그중 `paymentsNet ≠ itemsTotal` 수 · 그중 한 건씩 환불 품목 `cost.totalAmount` 가 원 가격인지(레포 밖에서 KOS 화면과 대조) | 수만 보고 — 원 가격이면 OQ-102 닫음, 아니면 사용자에게 올림 |
| L11 | **분할 결제 · 첫 승인 판정**: `counts.itemsElsewhere`(승인 결제가 두 달에 걸친 수납 · 재결제 포함) · `counts.firstApprovalCanceled`(전액 취소된 승인을 건너뛴 수납 — (a)) · `counts.firstApprovedUnknown`(대체 규칙 — (c)) | 수만 보고 — R§2 분할 결제 줄이 실제로 몇 건에 걸리는지 · (a) · (c) 가 0 이 아니면 OQ-121 을 사용자에게 올림 |
| L12 | `counts.unmatchedTransactions` · `counts.atOutsideMonth` | 수만 보고 — 0 이 아니면 OQ-119 · OQ-120 을 사용자에게 올림 |

- 결과 보고(`orchestration/work/…` — public)에는 **건수 · 같음/다름만** 적는다. 이름 · 금액 · 유입 이름 · 스크린샷 원본은 레포에 올리지 않는다(스크린샷은 가린 것만)
- 조사 리포트 수치(Q5 · Q6)는 10-28 17:21 까지라 10월 전체와 같지 않다 — 일치를 요구하지 않는다
- L5 · L10 결과로 `⚠ 결제 ≠ 품목` 배지의 문구 · 조건을 다시 정한다(OQ-106)

### 9.3 front

- `npx tsc --noEmit && npm run lint && npm run build` 통과
- back 가짜 응답(§4.2 예시 꼴)으로 상태 화면(§3.4) · 묶음 · 머리 실결제(음수 포함) · 「품목은 다른 달에」 · `⚠ 결제 ≠ 품목` · `⚠ 통화 섞임`(`netTotal null` 일 때만 — 통화 0개 수납은 안 뜸 · §6.7) · `itemsMissing` 스크린샷(가짜 값)
- **0.3.0**: 헤더 메뉴 두 화면 · `store.state` 두 가지(`current` = [새 결제 받기] + 작은 [전체 다시 받기] / `closed` = 「확정 · 저장됨」 + 작은 [전체 다시 받기]) · 「MM-DD HH:mm 받음」 · 「새 결제 N」 · 「받은 시점 기준」 안내 · `/agency` 「에이전시 전체」 · 에이전시 탭 · 빈 탭 · 없는 `agency=` 주소 → 「에이전시 전체」 · 걸러진 건수 줄 — 시안 v2 장면(`monthly-current` · `monthly-closed` · `agency-all` · `agency-one`)과 나란히 스크린샷(가짜 값)
- **엑셀(D-14)**: 툴바 오른쪽 `[엑셀 내보내기]` 가 두 화면 · 모든 탭에 있음 · 지금 탭에 맞는 `view` · `agency` 로 `sales.xlsx` 를 엶(가짜 back 으로 요청 주소 확인) · 불러오는 중 · 오류 때 꺼짐
- **0.4.0(D-18)**: 머리 「실결제」(음수 빨강) · 줄은 품목만(결제 · 취소 · 환불 줄 0 · `환불` 배지 0) · `결제 완료` · `부분 환불`(남은 금액) 배지 · 건수 줄 「취소된 결제 a건 · 전액 환불 품목 b개」 · 머리 「취소 a · 환불 b」 · ~~「전액 환불 b개」 한 줄~~(0.4.1 에서 숨김으로 바뀜 — 그리지 않는다) · 「앞 달 결제 취소」 · 0원 품목 차례(#51 꼴 가짜 응답) · 에이전시 요약 실결제 합 · 안내 문구 바뀜 — 가짜 응답 스크린샷
- **0.4.1**: 머리 실결제 = `netTotal`(합 기준) · ⚠ = `paymentsNet ≠ itemsTotal` · 「앞 달 결제 취소」 머리(음수) · 숨긴 수납은 그리지 않음 · 건수 줄 「숨긴 수납 h」(월별만) · 에이전트별 건수 줄은 숨긴 수 없음 · `미수납` 배지 없음
- `refresh=new` · `refresh=full` 만 보낸다(옛 `refresh=1` 0 — `grep -rn "refresh=1\|refresh: *1" front` = 0) · `[전체 다시 받기]` 는 확인 뒤에만 요청

### 9.4 운영 KOS 실물 조회 2 (0.3.0 완료 조건 · LIVE2)

근거: R§2 운영 키 줄(조회만 · 로컬만) · D1-12. §9.2 와 같은 조건(코디 · 로컬 · `back/.env` 운영 키). **9월 · 10월**을 본다. 결과 보고에는 수 · 같음/다름만(§9.2 끝 줄과 같음).

| # | 확인 | 통과 |
|---|---|---|
| L13 | **9월 한 번** — 빈 DB 에서 `month=2026-09` 첫 요청 → `fetch.mode full` · `store.state closed` · `kosCalls` 기록. 같은 화면을 다시 열기 · 메뉴를 오가기 · 에이전시 탭 바꾸기 · **back 재시작 뒤 다시 열기** → 매번 `fetch.kosCalls = 0` · back 로그의 KOS 호출(경로만)도 0 | **KOS 호출 0** |
| L14 | **10월 증분 호출 수** — 10월 첫 요청(full · `kosCalls` 기록) → 몇 분 뒤 [새 결제 받기] → `fetch.mode incremental` · `kosCalls`(① 1 + 토큰 + ⑤ · ② · ③ 는 새 행이 있는 수납이 있을 때만) · `newTransactions` · `duplicateTransactions` · `missingTransactions` · `newPurchases` | 수 기록 · **증분 `kosCalls` ≪ full `kosCalls`**(새 행이 0 이면 ① 1 + 토큰) · `missingTransactions 0`(0 이 아니면 로그 `changedPurchases` 와 같이 — 「바뀜」 길인지 · §4.6 ⑦ 길인지) |
| L15 | **증분 ↔ 전체** — L14 뒤(사용자에게 알린 뒤 한 번) 10월 `[전체 다시 받기]` → 전체 뒤 `counts.transactions` · `counts.purchases` · 줄 수 · 묶음별 승인 합 차이 수 ↔ 증분까지의 값 · `kos_total_count`(로그 숫자) | 같음. **증분 쪽이 많으면** 두 번 들어간 행(§4.6 ⑥ · doc r3 W-7) · **적으면** 빠진 행(F-2 꼴) — 차이 수를 보고하고 OQ-123 을 사용자에게 올림 |
| L16 | **에이전트별** — 10월 `agencies` 개수 · 각 `customers` · `payingCustomers` · `purchases`(이름은 레포 밖) · `agencyTotal` ↔ 에이전시 수납을 손으로 센 값(레포 밖) · 「(에이전시)」로 끝나지 않는데 에이전시처럼 보이는 유입 값 수(레포 밖에서 눈으로) | 수만 보고 — 0 이 아니면 OQ-125 를 사용자에게 올림 |
| L17 | **저장 파일** — `git status --ignored` 에 `back/data/` 가 ignored · `data/` 700 · 본 파일 · `-wal` · `-shm` 권한 600 · 표 · 칸 목록이 §4.4 와 같음(`sqlite3 … ".schema"` — 칸 이름만 보고 값은 안 봄) | 같음 |
| L18 | **엑셀** — 10월 월별 · 「에이전시 전체」 · 에이전시 탭 하나를 내려받아 엑셀(또는 Numbers)로 열기 · 행 수 = 화면 줄 수 · 금액 칸이 숫자(합계 함수가 먹음) · 내려받는 동안 back 로그의 KOS 호출 0 · 파일은 레포 · 리포트에 올리지 않고 확인 뒤 지움 | 같음 · **KOS 0** |
| L19 | **돈 경로 숫자(0.3.1 — doc r3 F-2 · F-3 · W-1 ~ W-3 · W-7)** — 9월 · 10월 받은 뒤 DB 에서 숫자만(값 · 이름은 안 봄): ① 두 달 이상에 `items_here = true` 인 수납 수(`month_purchases` — W-1) ② `counts.itemsNowhere`(W-2) · `counts.itemsPinnedElsewhere` ③ 증분 뒤 `counts.itemsMissing` ↔ 전체 뒤 `itemsMissing`(W-3) ④ 10월 [전체 다시 받기] 앞뒤 9월 응답의 품목 줄 수 · `itemsMissing`(F-3) ⑤ L14 의 `newTransactions` 중 같은 수단 · 같은 금액 묶음에 더해진 수(F-2) ⑥ L15 차이 · `missingTransactions` 합(doc r4 W-3 — 0 이 아니면 「바뀜」(`changedPurchases`) 길인지 · §4.6 ⑦ 길인지) | ① 0 · ② 0 · ③ 같음 · ④ 같음 · ⑤ 수만 · ⑥ 0 — 아니면 그 수납 수를 보고(id 는 레포 밖) |
| L20 | **결제 순액 · ⚠(0.4.1)** — **LIVE3 전에 10월 [새 결제 받기](증분) 1회**(0.4.1 증분이 같은 달 환불 · 재결제를 품목에 반영한 뒤 · doc r5 F-1) → 10월 `itemsHere` 수납 중 `paymentsNet ≠ itemsTotal`(⚠) 수 · 1 · 2판 ⚠ 수(앞 L5 기록)와 나란히 · 증분이 ② 를 다시 부른 수납 수(로그 숫자) · **남은 ⚠ 중 「분할 나머지」**(그 수납에 다른 달 ① `APPROVED` 행이 있음 — 품목 달에 전액 · doc r6 W-1) 수를 따로 | **⚠ 0**(남으면 그 수 · 달을 넘는 돈인지 · 수납 id 끝 4자리는 레포 밖) |
| L21 | **같은 금액 재결제 · 다른 금액 재결제 꼴** — 10월에 「승인 → 전액 취소 → 같은 금액 재승인」 수납 하나 · 「승인 → 전액 취소 → 다른 금액 재승인」 수납 하나를 골라(레포 밖) 머리 실결제 = KOS 화면의 최종 결제 금액 · 줄 = 품목만 · 취소된 결제 줄 0 · 머리 「취소 1」 | 같음(금액 · id 는 레포에 안 적음) |
| L22 | **부분 환불 하나** — 10월(없으면 9월) `부분 환불` 품목 하나 · 줄 금액 = KOS 화면의 남은 금액 · 수납 실결제 = 품목 합 | 같음 · 없으면 「해당 없음」 |
| L23 | **숫자로만** — 건수 줄 「취소된 결제 a건 · 전액 환불 품목 b개」 ↔ ① `CANCELED` 행 수 · ② `REFUNDED` 품목 수(그달 itemsHere 수납) · 엑셀 「정보」 시트 같은 수 · 0원 품목이 앞 유료 품목 바로 아래(눈으로) | 같음 |
| L24 | **합 기준(0.4.1 · 0.4.2)** — 10월 에이전시 탭 하나 · 「에이전시 전체」 · 월별: 화면 실결제 합 ↔ 그 화면 엑셀 「품목 금액」 열 합 · `hiddenPurchases` · `reflectedCancels` 수 · 「앞 달 결제 취소」 묶음 수. **+ 두 달 합 = KOS 최종**: 9월 품목 · 10월 취소가 걸친 수납 하나(레포 밖에서 고름)의 9월 머리 + 10월 머리 = KOS 화면의 그 수납 최종 결제 금액 · 9월을 늦게 받았거나 다시 받았어도 같음(doc r6 F-1) | **합 같음**(세 화면) · **두 달 합 = KOS 최종** · 수만 기록 |

## 10. env · 로컬 실행

### 10.1 env (`back/.env` 하나 · gitignore · `back/.env.example` 은 이름만)

| 이름 | 기본 | 뜻 |
|---|---|---|
| `KOS_OPEN_API_BASE` | (비어 있음 — `.env.example` 에 `https://open-api.kos-solution.com`) | KOS 공개 API 호스트(KA§1.2) |
| `KOS_OPEN_API_KEY` | (비어 있음) | 운영 명동점 공개 API 키(§7.2) — 비면 503 `kos_not_configured` |
| `SALES_BACK_PORT` | `8800` | back 포트 — **앱 코드는 읽지 않는다.** 실행 명령(§10.2)이 `back/.env` 를 셸로 읽어 `uvicorn --port ${SALES_BACK_PORT:-8800}` 에 넘긴다. front `.env.local` 의 `NEXT_PUBLIC_API_BASE_URL` 포트와 같게 둔다(0.3.0 — code r1 W-6 · 수정 1판 README) |
| `SALES_FRONT_ORIGIN` | `http://localhost:3800` | CORS 허용 출처 |
| (의존성) | — | back 에 **`openpyxl`** 더함(§4.7 · `uv add openpyxl`) — env 없음 |
| ~~`SALES_CACHE_SEC`~~ | — | **0.3.0 에서 없앰**(메모리 캐시 없음 — §4.4). 남아 있어도 읽지 않는다 |
| `SALES_DB_PATH` | `data/sales.sqlite3` | SQLite 파일 경로(`back/` 기준 상대 · 절대 가능 · gitignore — §4.4) |
| `SALES_OVERLAP_SEC` | `600` | 확정 판단 여유(초 · §4.5 「확정」). 0.3.1 부터 증분 ① 범위에는 안 쓴다(증분은 달 전체) |
| `SALES_CURRENT_STALE_SEC` | `600` | 이번 달 저장본이 이보다 오래면 값 없는 요청이 증분을 한 번 부른다(§4.5 J6). `0` 이면 매 요청 증분 |
| `SALES_KOS_CONCURRENCY` | `8` | 수납별 일정 조회 동시 수(§4.4) |
| `NEXT_PUBLIC_API_BASE_URL` | — | front 전용 · `front/.env.local`(gitignore)에 `http://localhost:8800` |

- 포트 8800 · 3800 = cc-prototype procedure(8700 · 3700)와 같은 맥에서 겹치지 않게 · 기본값(OQ-111)
- back 은 `back/.env` 하나를 읽는다(실제 환경변수가 먼저 · 빈 값은 기본값 — cc-prototype procedure `config.py` 의 `env_ignore_empty` 방식)

### 10.2 실행

```bash
# back
cd back && uv sync
set -a; [ -f .env ] && . ./.env; set +a          # SALES_BACK_PORT 를 back/.env 에서 읽는다(W-6)
uv run uvicorn app.main:create_app --factory --host 127.0.0.1 --port ${SALES_BACK_PORT:-8800}   # 워커 1(§4.4)
uv run pytest -q && uv run ruff check .

# front
cd front
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8800" > .env.local
npm install && npm run dev        # http://localhost:3800
```

## 11. 열린 것

| # | 무엇 | 기본값(제안) | 상태 |
|---|---|---|---|
| OQ-101 | 월 경계 종료값 — KOS `createdTimeUtcTo` 가 포함인지 아닌지 문서에 없음 | 다음 달 1일 00:00 KST − 1초(스펙 예시 `…23:59:59Z` 꼴). 그 1초 안 결제는 빠질 수 있음 | 새로 · planner 기본값 |
| ~~OQ-102~~ | ~~환불 · 부분 환불 품목 금액~~ | **닫음(0.4.0) — 뒤집음**: ② `cost.totalAmount` = **환불 뒤 남은 금액**(전액 환불 0 · 28/28 · 수납 392/392 가 ① 순액 = 품목 합 — 운영 수집본 · §6.3). 「원 가격」 기본값은 틀렸다 | 닫음 |
| ~~OQ-103~~ | ~~이름 · 방문일 원천~~ | **닫음(0.1.1)** — `findScheduleByPurchaseId` · 방문일 = `reservation.startDateTime` · 일정 없으면 `getVisitor`(R§2 원천 줄 10-29 정정) | 닫음 |
| ~~OQ-104~~ | ~~결제일 칸 원천~~ | **닫음(0.1.2)** — 결제일 = ⑤ `paymentDateTime.approvedDateTimeUtc` · 취소 줄 = `canceledDateTimeUtc` · 반환 줄 = `spentDateTimeUtc` · ① `lastUpdatedPaymentDateTimeUtc` 는 보이지 · 정렬하지 않음(R§2 ⑤ 줄 · §5.4) | 닫음 |
| ~~OQ-105~~ | ~~조회를 요청마다 할지 저장해 둘지 · 동시성 · 토큰 잠금~~ | **닫음(0.3.0)** — D1-12 「SQLite 에 저장 · 다시 부르지 않는다」로 대체 → 저장 세부는 OQ-122 · 수납별 조회 동시 8 · 토큰 다시 받기 한 번만은 그대로(§4.4) | 닫음 |
| OQ-106 | `⚠ 결제 ≠ 품목` 배지 | **0.4.1 — 조건 = 이 달 결제 순액(`paymentsNet`) ≠ 품목 합(`itemsTotal`)**(§6.4 · 운영 수집본 392/392 일치 · 1 · 2판의 「승인 합 ≠ 품목 합」 20 수납은 순액으로 0 — R§2 D-18 줄 · L20). 남는 ⚠ = 달을 넘는 돈(분할 결제 나머지 · 다른 달 환불 · **앞 달 승인의 이 달 취소** — 「승인 → 다음 달 전액 취소 → 다른 금액 재승인」 꼴은 실결제 = 품목 = KOS 최종인데 `paymentsNet` 에 앞 달 승인의 취소가 들어가 ⚠ 가 뜬다 · LIVE3 9월 ⚠ 1 이 이 꼴 · code r3 §2) · 증분 전 저장본. 배지를 줄이는 안(⚠ 비교에서 `canceledRefId` 가 다른 달 승인을 가리키는 취소를 뺌)은 이번 판 밖 | 조건 닫음 · L20 으로 확인 |
| OQ-107 | 고를 수 있는 달의 앞쪽 끝 | 두지 않음(뒤쪽 끝 = 이번 달) | 새로 · planner 기본값 |
| OQ-108 | 화면 합계 · 금액 기준(총액 · 공급가) | 합계 없음(건수만) · 금액 = 총액(`totalAmount`) — 리포트 「정할 것 7」 | 새로 · 사용자(다음 판) |
| OQ-109 | 손님 유입 · 이름 · 방문일이 받은 시점 값 | **0.3.0 — 받은 시점 값이 저장된다**(① 행 유입 · ③ 이름 · 방문일 · §4.6 ③). 바뀐 값은 `[전체 다시 받기]` 로만 들어온다 · 에이전시 판정도 받은 시점. 정산 확정 절차(에이전시와 서로 확인한 판)가 생기면 그때 「확인한 판」 저장을 따로 정함 | 기본값 바뀜 · 사용자(다음 판) |
| OQ-110 | 접근 — 로그인 없음 · 운영 고객 이름이 보이는 화면 · **0.3.0: 이름이 든 SQLite 파일이 디스크에 남음** | 로컬 `127.0.0.1` 만 · 로그인 없음 · 배포는 따로 정함(D1-09 · R§2 운영 키 줄 「로컬만」) · DB 파일은 gitignore · 600 · 이 맥 밖 반출 금지(§7.3) | 새로 · 사용자 |
| OQ-111 | 실행 모양 · 포트 · health 경로 | compose 없이 uv · npm · 8800 · 3800 · `GET /api/health` | 새로 · planner 기본값 |
| OQ-112 | 다음 판 — 수수료율(상품별) · 에이전시별 금액 · 선불카드 충전/사용 중 어느 쪽을 셀지 · 에이전시 확인 절차 | 이번 판 밖(에이전시별 **보여 주기**(§3.5 · §6.8) · **엑셀**(§4.7 · D-14)은 0.3.0 에 들어옴) | 열림 · 사용자(다음 판) |
| OQ-113 | 화면 세부(수납 id 끝 6자리 · 정렬 · 배지 색 · 상태 화면 문구 · 결제 수단 한글 이름 · 0원 구성품 흐림) | **0.3.0 — 시안 v1 · v2 가 정본**(D1-10). 이 문서가 남기는 것은 값 · 필드 · 정렬 규칙뿐 · 시안에 없는 결제 수단 이름(TRANSFER · PLATFORM · MEDICAL_LOAN 등)은 front `labels.ts` 가 KOS 뜻을 한글로(모르면 값 그대로) | 시안으로 넘김 · 시안 v2 |
| OQ-114 | 일부 실패 처리 — 「없음」 아닌 ③ · ④ 실패 하나가 달 전체를 오류로 | 달 전체 오류(일부 빠진 리스트를 보이지 않음). 대안 = 그 수납만 칸 비우고 `counts` 에 실패 수 | 새로 · planner 기본값 |
| OQ-115 | `REQUESTED` · `FAILED` 결제 행 | 줄 · 합에서 빼고 `ignoredTransactions` 로만 셈(운영 10월 0건) | 새로 · planner 기본값 |
| OQ-116 | 품목 통계 조회 범위 · ⑤ 묶음 크기 · ⑤ 에 없는 수납 | ② = 달 시작 −31일 ~ 달 끝 · 그래도 없으면 `itemsMissing` · ⑤ = 100개씩 · ⑤ 에 없으면 이 달 승인 행으로 봄(+ `firstApprovedUnknown` · 이 경우만 두 달 노출 가능) | 새로 · planner 기본값 |
| OQ-117 | 응답 브라우저 캐시 | `Cache-Control: no-store` | 새로 · planner 기본값 |
| OQ-118 | 통화가 섞인 수납 | 줄은 그대로 · 수납 합 `null` · `⚠ 통화 섞임`(운영 10월 전부 KRW) | 새로 · planner 기본값 |
| OQ-119 | 달 귀속(① `createdTimeUtc` 필터)과 보이는 결제일(⑤ 승인 · 취소 일시)이 다른 달일 때 | 묶음은 ① 이 정한 달에 둔다 · 결제일 칸엔 다른 달 날짜 그대로 · `counts.atOutsideMonth` · L12 로 실물 건수 확인. 대안 = 귀속도 ⑤ 시각으로(① 범위를 넓혀 불러야 함) | 새로 · 사용자 |
| OQ-120 | ① 행 ↔ ⑤ 거래 잇기(공통 id 없음) | 수납 · 상태 · 수단 · 금액 절댓값 · 통화로 잇고, 동점은 「마지막 결제 상태 변경 일시」 같음(파싱 · 초 단위)으로 가름(고르는 데만) · 못 이으면 `at null` · 「시각 없음」 · L12. 대안(L12 가 크면): 동점 가르기를 ⑤ `createdDateTimeUtc`(① 기간 필터와 같은 축)로 · 거래 id 가 있는 `getTransactionList`(31일 · `limit` 1000 · 허용 경로 하나 늘어 R§2 승인 필요) | 새로 · planner 기본값 |
| OQ-121 | 「첫 승인 결제」 고르기 세부(§6.2 s2 ~ s5) | 전액 취소(`canceledRefId` 합 ≥ 승인 금액)만 뺌 · 부분 취소는 남김 · 다 빠지면 원래 후보 · 승인 시각 없으면 수납 전체를 `createdDateTimeUtc` → `lastUpdatedDateTimeUtc` → `id` 로 · 잇기 실패면 ⑤ `createdDateTimeUtc` 달(추정 — ① 귀속과 같은 축) · 전부 `firstApprovedUnknown` · L11 | 새로 · planner 기본값 |
| OQ-122 | 저장 세부(§4.4) | SQLite 표준 `sqlite3` · `SALES_DB_PATH=data/sales.sqlite3` · WAL · 표 6개 · 받기는 KOS 다 마친 뒤 한 트랜잭션(실패면 안 바뀜) · 응답은 늘 저장본에서 · 달별 잠금 + 쓰기 잠금 하나 · 프로세스 1 · 표 모양 바뀌면 파일 지우고 다시 받음 · [전체 다시 받기] 확인 창 · 받기 실패 = 오류 화면(저장본을 대신 보이지 않음). 대안 = 받기가 실패하면 저장본을 보이고 「받기 실패」 표시 | 새로 · planner 기본값 |
| OQ-123 | 증분 새 행 가르기(0.3.1 — doc r3 F-2 · W-7) | **증분도 ① 을 달 전체로 1회 · 새 행 = 묶음 키(수납 · 상태 · 수단 · 금액 · 통화)마다 받은 수 − 저장 수 · `last_updated` 안 씀 · 줄어들면 지우지 않고 `missingTransactions`** · ⑤ · ② · ③ · ④ 는 새 행이 있는 수납 · 새 수납에만(비싼 조회는 여전히 「마지막 이후 새 것만」). D1-12 「마지막 이후만 더 부른다」를 「새로 생긴 것만 더 받는다」로 읽은 것 — ① 1 회는 범위와 상관없이 같은 수(보통 한 페이지). 대안(doc r3) = (a) 쓰인 거래와 이을 때 `last_updated` 초가 같을 때만 중복 · (b) 겹침 창 안 행만 중복 후보(① 에 만든 시각이 없어 구현 불가). 이미 저장된 수납의 품목 변화는 안 받음(§4.6 ④) · L15 · L19 | 새로 · **코디 판단(돈 경로 기본값) → 사용자 통보** |
| OQ-124 | 확정 시점 | 받기 시작 시각 ≥ 다음 달 1일 00:00 KST + `SALES_OVERLAP_SEC` 이면 `closed` · 그 전엔 `current`(J4 로 한 번 더) · 되돌리기 없음(`full` 만). 대안 = 다음 달 N일(예: 3일)까지는 `current` 로 두어 늦은 취소 · 정정을 받음 | 새로 · planner 기본값 |
| OQ-125 | 에이전시 판정 · 목록 | 최초 유입 채널을 앞뒤 공백 뗀 뒤 반각 `(에이전시)` 로 **정확히 끝나는** 값만 · 목록 = 그달 데이터에서만 · 이름 차례 · 없는 `agency=` 주소는 「에이전시 전체」로 · 탭 이름에서 「(에이전시)」를 뗄지는 시안 v2. 대안 = 관리 목록(설정 파일) — 이번 판 밖 | 새로 · planner 기본값 · L16 |
| ~~OQ-126~~ | ~~손님 · 결제 손님 정의~~ | **닫음** — 손님 = `visitorId` 중복 없이(없으면 수납 id · D1-15 · 0.3.1) · 결제 손님 = 그달 ① `APPROVED` 행이 있는 손님 — **0 원 · 순액 0 이하도 포함**(사용자 2026-10-29 「결제 0 원도 일단 포함해」) | 닫음 |
| OQ-127 | 에이전트별 API 모양 | **같은 `/api/sales` 응답에 `agency` · `agencies` · `agencyTotal` → front 가 거름**(조회 경로 하나 그대로 · 탭 바꿀 때 호출 0 · 두 화면이 같은 저장본 · 엑셀만 back 이 같은 규칙으로 거름 §4.7). 대안 = `GET /api/agencies?month=` 목록 + `GET /api/sales?month=&agency=`(응답이 작아지고 back 이 거름 — 같은 달을 두 경로가 따로 셈) | 새로 · planner 기본값 |
| OQ-128 | 저장 뒤 「첫 승인」이 바뀌는 수납(§4.6 ②) | 품목 달 고정 — 먼저 저장된 달이 이김(확인 · 쓰기 = 같은 쓰기 트랜잭션 · W-1) · 다음 달은 머리만(실결제) · `itemsPinnedElsewhere` · 앞 달만 다시 받아 품목이 어느 달에도 없게 되면 `itemsNowhere` 로 드러냄 + 그 달 [전체 다시 받기] 안내(doc r3 W-2 (b)). 대안 = 전체 받기가 끝날 때 같은 수납을 고정한 다른 달을 저장본으로 다시 판정(W-2 (a) — 품목이 저장 안 돼 있으면 ② 가 필요해 KOS 0 이 깨질 수 있음) | 새로 · planner 기본값 · 코디 판단 · L11 · L19 |
| OQ-129 | 저장본 지우기 · 보관 기간 | 지우기 기능 없음 — 사람이 파일을 지운다(전체 다시 받기) · 보관 기간 없음. 운영 개인정보(이름)가 남으므로 PoC 가 끝나면 파일을 지운다 | 새로 · 사용자 |
| ~~OQ-130~~ | ~~엑셀 세부(§4.7)~~ | **닫음** — `openpyxl` · 시트 「매출」(헤더 + 줄 하나 = 행 하나 · 합계 없음) + 「정보」 · 수납 id 전체 · 빈 값 빈 칸 · 파일 이름 `매출_YYYY-MM_<화면>.xlsx` · **손님 이름은 가리지 않는다**(사용자 2026-10-29 「엑셀 이름 가리지마」) · 가린 판은 만들지 않는다 | 닫음 |
| OQ-131 | 저장 안 된 달을 엑셀로 | 409 `not_fetched`(KOS 0 · 먼저 받지 않음) — 화면 버튼은 저장본이 있을 때만 켜져 보통은 안 생김. 대안 = 받기와 같은 규칙(§4.5)으로 먼저 받고 내보내기 | 새로 · planner 기본값 |
| OQ-132 | 합 기준 · 앞 달 결제의 이 달 취소 · 실결제 0 묶음(D-06 ↔ D-18) | **코디 추천안(기본값) · 사용자 답 대기**(R§2 OQ-132 줄 「사용자에게 두 번 물음 · 답 오면 고침」): 실결제 = 품목 실결제 합 + 앞 달 결제의 이 달 돈(반영 안 된 취소 음수 · 고정 수납이나 이 달 취소가 있는 수납은 이 달 살아 있는 승인도 — R§2 마지막 줄 「달을 모두 더하면 KOS 최종」) · 화면 · 에이전시 합 · 엑셀이 같은 숫자 · 실결제 0 · 줄 0 묶음은 숨김(손님 셈엔 포함) · 분할 결제는 품목 달에 전액. 운영 9 · 10월에 「이 달 취소 뒤 재승인」 갈래 0 건(R§2). **답이 바뀌면 고칠 곳 = §6.9 판정 하나**(코드 `settle()` 하나). 대안 = (b) 두 숫자를 다 보임 · 앞 달 취소를 이 달에서 빼고 숫자로만 | 기본값 · **사용자 답 대기** |
| OQ-133 | 부분 환불의 환불된 금액 · 원래 금액 | 화면 · 엑셀 = 남은 금액만(D1-18). 품목 단위 환불 금액 · 환불 전 금액은 **문서 · 데이터에 없음**(§6.3 — `firstPriceAmount` · `basePriceAmountV2` 는 정가 · ⑤ `items` 는 ② 와 잇는 키 없음 · `refundingItems` 빈 값). 필요하면 수납 단위 환불 합(① 취소 행)을 따로 보이는 것만 가능 | 새로 · planner 기본값(데이터 없음) |
| OQ-134 | 취소 · 환불을 숫자로 보이는 자리 | 건수 줄 「취소된 결제 a건 · 전액 환불 품목 b개」 + 수납 머리 회색 「취소 a · 환불 b」 + 엑셀 「정보」 시트 · 취소된 결제 행은 엑셀에 넣지 않는다(지시서 기본 = 넣지 않음 · D1-18 로 굳음). 대안 = 머리 글자 없이 건수 줄만 | 새로 · planner 기본값 |
| OQ-135 | 0원 품목 차례 | ② 차례에서 앞 유료 품목 바로 아래(앞에 없으면 첫 유료 아래) — 보이기 규칙 · 부모 판정 아님(② · ⑤ 에 구성품 ↔ 부모 연결 필드 없음 · 운영 수집본 0원 품목 159 중 같은 상품명 유료 품목이 있는 것 4). 대안 = ⑤ `items[].optionConfiguration.compositions`(117 품목에 있음)로 묶기 — ② 행과 잇는 키가 없어 이번 판 밖 | 새로 · planner 기본값 |
| ~~OQ-136~~ | ~~시안 v1 · v2 와 달라지는 화면~~ | **닫음(0.4.3)** — **시안 v3 은 만들지 않는다** · SPEC 0.4.x 대로 구현 · 구현본(코드 PR #1)이 정본(R§2 OQ-136 줄 · role 「배포된 웹은 구현본이 정본」) | 닫음 |
| OQ-137 | 「최종 결제」 품목 상태 경계(doc r5 W-4) | 줄 · 합 · 엑셀 = `ACCEPTED` · `PAID` · `PARTIALLY_REFUNDED` 만 · `REFUNDED` = `refundedItems` · `INITIALIZED`(미수납) · `PURCHASE_STATUS_UNSPECIFIED` · 그 밖 = `excludedItems` 로 셈(운영 수집본 0건). 대안 = `INITIALIZED` 를 「미수납」 배지로 보이되 합에서 뺌 | 새로 · planner 기본값 |

## 부록 A. DEC-001 · `_RESUME` §2 대응표

| 원천 | 절 |
|---|---|
| D-01 첫 화면 = 월별 매출 리스트 · 기본 이번 달 · 수수료 밖(에이전시 탭 = D-11 · 엑셀 = D-14) | §1 · §3.1 · §4.1 · OQ-108 · OQ-112 |
| D-02 한 줄 = 품목 · 수납 묶음 · 품목 금액 · 결제 수단은 수납 참고 | §3.2 · §4.2 · §5.2 · §6.4 |
| D-03 칸(결제일 · 이름 · 방문일 · 최초 유입 · 수납 · 상품 · 옵션 · 품목 금액 · 상태) · 이름 안 가림 | §3.2 · §5.2 |
| D-04 에이전시 판정 = `visitorFunnelName` | §5.2 · §6.6 |
| D-05 운영 명동점 조회만 · `/queries/` · 원천 작업 | §5.1 · §7.1 · §7.2 |
| D-06 월 귀속 = 결제 시각(KST) · 취소는 취소된 달(0.4.0: 음수 줄 대신 그 달 실결제에서 뺌) | §6.1 · §6.2 · §6.3 · §6.9 |
| D-07 선불카드 · 기타 상품 안 뺌 · 품목 종류 칸 · 상품명 빈 품목 | §3.2 · §6.5 |
| D-08 별도 프로젝트 `agency-settlement`(레포 루트 `back/` · `front/`) · cc-prototype 디자인 복사 · import 금지 | §1.1 · §2 · §8 |
| D-09 로컬에서만 | §7.3 · §10 · OQ-110 |
| D-10 시안 v1 채택 · 헤더 메뉴 「월별 조회 \| 에이전트별 조회」 · 좌우 넓게 | §3 머리 · §3.1 · §3.2 · OQ-113 |
| D-11 에이전트별 조회 — 「에이전시 전체」 + 에이전시마다 탭 · 같은 묶음 모양 · 수수료는 다음 판 | §1.1 · §3.5 · §4.1 · §4.2 · §6.8 · #34 · #35 · L16 · OQ-125 ~ OQ-127 |
| D-12 SQLite 저장 · 지난 달 한 번 · 이번 달 마지막 이후만 · 전체 다시 받기는 사람이 | §3.1 · §4.4 · §4.5 · §7.3 · §10.1 · #12 · #25 ~ #33 · #36 · L13 ~ L15 · L17 · OQ-122 ~ OQ-124 · OQ-128 · OQ-129 |
| D-13 받은 시점 기준(지난 달 배지는 나중 환불로 안 바뀜) | §3.1 · §4.6 · §6.3 · §6.8 · §4.7 시트 「정보」 · OQ-109 |
| D-15 손님 수 = `visitorId` 기준(없으면 수납 id) · 이름으로 세지 않음 | §3.5 · §6.8 · #35 · OQ-126 닫음 |
| D-16 결제 손님 = 그달 승인 있는 손님(0원 · 순액 0 이하 포함) | §6.8 · §6.9 · #35 · #49 · OQ-126 닫음 |
| D-17 엑셀 손님 이름 안 가림 | §4.7 · OQ-130 닫음 |
| doc r5(0.4.1 — 증분 ② 다시 · 합 기준 · 숨김 · 살아 있는 승인 저장 · 상태 경계) | §4.4 · §4.5 증분 5 · §4.6 ① · §4.7 · §6.9 · #54 ~ #60 · L20 · L24 · OQ-132 · OQ-137 |
| doc r6(0.4.2 — 앞 달 결제 취소 반영 판정 · 분할 결제는 품목 달에 전액 · 빈 탭 · schema 2 채우기 한 번) | §3.1 · §3.2 · §3.5 · §4.2 `reflectedCancels` · §4.6 ⑧ ⑨ · §4.7 · §6.9 · #61 ~ #63 · L20 · L24 · OQ-132 |
| 구현 동기(0.4.3 — 코드 PR #1 · code r3 F-1 · W-1 · W-2 · NOTE-1 · 3 · 8 · code r2 W-1 · doc r4 W-3 · be3-fix-2 · fe3-fix-1) · R§2 마지막 두 줄(OQ-136 · 「달을 모두 더하면 KOS 최종」) | §3.1 폭 · §3.2 결제일 · §3.3 차례 · §4.5 증분 2 · §4.6 ⑦ · §4.7 · §6.9 · §7.3 · #27(g) · #64 ~ #67 · L14 · L19 · OQ-132 · OQ-136 |
| D-18(정정) 최종 결제만 — 머리 실결제 · 품목 = 최종 결제(부분 환불 남은 금액) · 취소된 결제 · 전액 환불 품목은 줄 없음(숫자만) · 결제 · 취소 행 줄 없음 · 기준 = 품목 실결제 금액 | §3.1 · §3.2 · §3.3 · §3.5 · §4.2 · §4.7 · §6.2 · §6.3 · §6.4 · §6.8 · §6.9 · #45 ~ #53 · L20 ~ L23 · OQ-102 · OQ-106 · OQ-132 ~ OQ-136 |
| R§2 증분 해석 줄(OQ-123 — ① 달 전체 1회 · 비싼 조회는 새 것만) | §4.5 · OQ-123 |
| D-14 엑셀 내보내기 — 화면(월 + 탭) 그대로 · 품목 한 줄씩 · 11칸 · 저장본으로(KOS 0) · 툴바 오른쪽 | §1.1 · §3.1 · §3.6 · §4.1 · §4.3 · §4.7 · #37 ~ #40 · L18 · OQ-130 · OQ-131 |
| R§2 시안 v2 줄(채택 · 탭 = 그 달 에이전시만 · 「(에이전시)」 뗌 · [전체 다시 받기] 이번 달에도 · 확인 1번 · 「새로 받음」 = 다음 받기 전까지 · 0건 문구 · 나머지 = 시안 v2 값) | §3.1 · §3.5 · §4.2 `newInLastFetch` (손님 셈은 R§2 손님 셈 줄 · D-15 가 뒤집음 — §6.8) |
| R§2 손님 셈 줄(`visitorId` · 이름 기준을 뒤집음) | §6.8 · #35 · OQ-126 |
| DEC-001 열린 것(조회 방식 · 이름 · 방문일 작업 · 월 경계 시간대) | §4.4(OQ-105 닫음 → D-12) · §5.1 ③(OQ-103 닫음) · §6.1 · OQ-101 |
| code r1 SPEC 정리 몫(W-1 · W-3 · W-5 · W-6) | §6.2(⑤ 승인 0 줄) · §5.4(이은 뒤 시각) · §6.7(통화 0개) · §10.1(`SALES_BACK_PORT`) |
| R§2 운영 키 줄(10-29 확장 — 이 프로젝트 코드 · WP-LIVE · 조회만 · 로컬만) | §7.2 · §7.3 · §9.2 |
| R§2 별도 프로젝트 줄(코드 레포 `kknaksss/agency-settlement` · 루트 `back/` · `front/` · 디자인만 cc-prototype 복사) | §1.1 · §2 · §7.2 · §8 · §10 |
| R§2 원천 줄(10-29 정정 — `findScheduleByPurchaseId` · 없으면 `getVisitor`) | §5.1 ③ ④ · §6.4 |
| R§2 분할 결제 줄(품목 줄은 첫 승인 결제가 있는 달에만) — 수정 4판: 「취소 안 된 첫 승인 결제 행이 ① 로 귀속된 달」 | §5.1 ⑤ · §6.2 · OQ-106 · OQ-121 · #17 · #22 ~ #24 · L11 |
| R§2 ⑤ 줄(⑤ 승인 · 결제일 = ⑤ `approvedDateTimeUtc` · 취소 = `canceledDateTimeUtc` · OQ-104 닫음) | §3.2 · §3.3 · §5.1 ⑤ · §5.2 · §5.4 · §6.1 · OQ-104 · OQ-119 · OQ-120 · #21 · L12 |

