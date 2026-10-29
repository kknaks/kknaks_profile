---
type: spec
id: SPEC-001
title: "월별 매출 리스트 — 운영 명동점 KOS 결제를 월 단위 · 수납별 묶음 · 품목 한 줄씩 · 조회 전용 · 로컬만"
version: 0.2.1
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
  - "para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md (D-01 ~ D-09 · 열린 것)"
  - "orchestration/work/agency-settlement/_RESUME.md §2 — 2026-10-29 줄 전부(결정 원천 · DEC-001 와 다르면 이쪽 · 0.1.1 = 운영 키 확장 · ③ 작업 정정 · 분할 결제 줄 · 0.1.2 = ⑤ 추가 승인 · 결제일 원천 줄 · 0.2.0 = 별도 프로젝트 줄)"
  - "orchestration/work/agency-settlement/research-agency-attribution.md — Q1 · Q3 ~ Q6(필드 경로 · 결제/취소 모양 · 연결 근거)"
  - "orchestration/work/agency-settlement/review-spec-007-report.md — 0.1.0 검수(F-1 · W-1 ~ W-6 · NOTE 1 ~ 5)"
  - "orchestration/work/agency-settlement/planner-fix-1-instructions.md — 수정 1판 지시(444 일치의 정의 포함)"
  - "orchestration/work/agency-settlement/planner-fix-2-instructions.md — 수정 2판 지시(⑤ 승인 · OQ-104 닫음)"
  - "orchestration/work/agency-settlement/planner-fix-3-instructions.md — 수정 3판 지시(별도 프로젝트 · 번호 재부여)"
  - "orchestration/work/agency-settlement/review-spec-001-r2-report.md — 0.2.0 재검수(W-1 첫 승인 달 구멍 3 · W-2 sources 경로 · NOTE 1 · 2 · 6 · 7)"
  - "orchestration/work/agency-settlement/planner-fix-4-instructions.md — 수정 4판 지시(첫 승인 달 = 취소 안 된 첫 승인 결제 행의 ① 귀속 달)"
  - "reference/2026-10-12-cc-prototype/kos-demo-api.md §1.2 · §2 · §3.1 · §3.3 · §3.4(작업표 · 인증 · 응답 감싸기)"
  - "https://developers.kos-solution.com/openapi.yaml 1.0.1 · 작업 77(2026-10-29 받음) — 요청 · 응답 스키마 · 「에러 응답」 · 「호출 한도」"
  - "cc-prototype procedure/ main(읽기만 — back app/kos/client.py · app/config.py · app/domain/{clock,errors}.py · app/service/kos_errors.py · front tailwind.config.ts · app/layout.tsx · app/globals.css · app/styles/* · lib/{api,time}.ts · package.json)"
  - "ax-clinic-project scripts/kos_collect.py(읽기만 — 운영 키 이름 · 조회 전용 가드 모양 · 키 값은 읽지 않음)"
---

# 월별 매출 리스트 계약

> 운영 명동점 KOS 의 결제를 **월 단위로 조회**해 **수납별로 묶고 품목 한 줄씩** 보여 주는 로컬 페이지다. 병원 · 에이전시 수수료 정산의 첫 판이고, 이번 판은 **리스트만**이다(DEC-001 D-01).
>
> SSOT 순서(이기는 순): ① `_RESUME` §2 의 10-29 줄 ② DEC-001 ③ 이 문서 ④ 조사 리포트(사실) ⑤ 공식 스펙(필드 이름 · 뜻). 화면 시안은 없다 → **cc-prototype procedure 디자인(medikit · Céramique 테마) 기본값**으로 그리고 실물 확인 때 고친다.
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

## 1. 범위

### 1.1 In

| 무엇 | 근거 |
|---|---|
| 별도 프로젝트 코드 레포 **`kknaksss/agency-settlement`** — 루트에 `back/`(FastAPI) + `front/`(Next.js) · cc-prototype 은 읽기만(복사 원본) | D1-08 · R§2(별도 프로젝트 줄) |
| 화면 하나 — 월 선택 · 수납별 묶음 · 품목 줄 · 칸(D-03) · 상태 · 빈 달 · 불러오는 중 · 오류(§3) | D1-01 · D1-02 · D1-03 |
| back API 하나 — `GET /api/sales`(§4) | D1-01 · D1-05 |
| KOS 원천 매핑 — 칸마다 작업 · 필드 · 조인 키(§5) | D1-05 · R§2(원천 줄) · Q5 · Q6 |
| 규칙 — 월 경계(KST) · 수납 포함 · 분할 결제 · 취소 · 환불 · 선불카드 · 상품명 빈 품목 · 유입 빈 값 · 통화(§6) | D1-04 · D1-06 · D1-07 · R§2(분할 결제 줄) |
| 조회 전용 가드 · 개인정보 · 로그(§7) | D1-05 · D1-09 · R§2(운영 키 줄) · `kos_collect.py` |
| 디자인 복사 목록(§8) · 검증(§9) · env · 로컬 실행(§10) | D1-08 · D1-09 |

### 1.2 Out (이번 판 밖 — 다음 판은 OQ 로만)

| 무엇 | 근거 |
|---|---|
| 수수료율(상품별) · 수수료 계산 | D1-01 · DEC-001 열린 것 · OQ-112 |
| 에이전시별 보여 주기 · 유입 필터 · 「에이전시 코드 집합」 판정 | D1-01 · OQ-112 |
| 엑셀 · CSV 내려받기 | D1-01 · OQ-112 |
| 배포 · 외부 접속 · 로그인 | D1-09 · R§2(운영 키 줄 「로컬만」) · OQ-110 |
| KOS 쓰기(`/commands/` — 토큰 교환 하나 빼고) | D1-05 · R§2(운영 키 줄 「조회만」) |
| 월 합계 · 유입별 집계 · 선불카드 충전 · 사용 이중 계산 거르기 | D1-01 · D1-07(「뒤의 필터가 정한다」) |
| 메모 · 상세 유입(`…FunnelDetail`) 같은 자유 텍스트로 에이전시 짐작 | D1-04 · [[no-inference-from-free-text]] |
| DB · 파일 저장(조회 결과는 back 메모리에만 · §4.4) | 기본값(OQ-105) |

## 2. 폴더 · 실행 모양

```text
agency-settlement/          # 코드 레포 kknaksss/agency-settlement(private) 루트
├── README.md               # 이미 있음 — 실행 · env 채우기(§10)를 더한다
├── .gitignore              # 이미 있음 — .env · .env.* (! .env.example) · node_modules · .next · .venv
├── back/                   # FastAPI · Python 3.12 · uv(cc-prototype procedure/back 과 같은 도구)
│   ├── .env.example        # 이름만 — 복사해 back/.env(gitignore)
│   ├── app/
│   │   ├── main.py         # create_app 팩토리 · 오류 처리기 · CORS
│   │   ├── config.py       # Settings(env 로만)
│   │   ├── api/sales.py    # router — GET /api/sales · GET /api/health
│   │   ├── service/sales.py      # 월 경계 · 조인 · 줄 만들기 · 캐시
│   │   ├── kos/client.py   # 공개 토큰 교환 + 조회 전용 가드(§7.1)
│   │   ├── domain/{clock,errors}.py
│   │   └── schemas/sales.py      # 응답 모델(§4.2 — front 계약)
│   └── tests/              # KOS 가짜 transport
└── front/                  # Next.js · cc-prototype procedure/front 디자인 복사(§8)
    ├── app/{layout.tsx,page.tsx,globals.css,styles/}
    ├── components/monthly/   # 월 선택 · 수납 묶음 · 줄
    └── lib/{api.ts,time.ts,types.ts,labels.ts}
```

- 계층은 cc-prototype `procedure/back` 모양 그대로 — router → service → kos client · 아래층은 HTTP 를 모르고 도메인 예외만 던진다(코드 `domain/errors.py`). DB · repository 는 없다(저장할 것이 없다 — §4.4) · 기본값(OQ-111)
- cc-prototype 레포는 **읽기만** — 그 파일은 **복사**한다(import · 심볼릭 링크 · 공용 패키지 · git submodule 금지 — D1-08 「import 금지」). cc-prototype 레포에는 아무것도 쓰지 않는다
- 컨테이너 · compose 없음 — back 은 `uv run` · front 는 `npm run dev` 두 줄(§10.2) · 기본값(OQ-111)
- 레포 루트 `README.md`(이미 있음)에 실행 · env 채우기를 더한다

## 3. 화면

시안 없음 → cc-prototype procedure 디자인(§8)으로 그린다. 데스크 브라우저 · 가로 1280px 이상 기준 · 한 페이지(`/`) · 기본값(OQ-113).

### 3.1 틀

| 자리 | 계약 | 근거 |
|---|---|---|
| 머리 | 제목 「월별 매출」 · 오른쪽에 「운영 명동점 · 조회 전용」 회색 글자. 로그인 · 메뉴 없음 | D1-05 · D1-09 · 기본값 |
| 월 선택 | `[‹]  2026년 10월  [›]` — 앞 · 뒤 달로 한 칸씩. **이번 달(KST)보다 뒤는 못 고른다**(`[›]` 꺼짐). 앞쪽 끝은 두지 않는다 | D1-01 · 기본값(OQ-107) |
| 기본 달 | 주소 `?month=YYYY-MM` 이 있으면 그 달, 없으면 **이번 달(KST)**. 달을 바꾸면 주소도 바뀐다(새로고침 · 공유 때 같은 달) | D1-01 「기본 = 이번 달」 |
| 다시 불러오기 | 월 옆 `[다시 불러오기]` — back 캐시를 건너뛴다(`refresh=1` · §4.1). 마지막으로 불러온 시각 「HH:MM 기준」 | 기본값(OQ-105) |
| 건수 줄 | 「수납 N건 · 품목 M줄 · 결제 · 취소 · 환불 K줄」 — **금액 합은 보이지 않는다**(합계 · 집계는 이번 판 밖) | D1-01 · 기본값(OQ-108) |
| 안내 한 줄 | 표 위 회색 글자 「상태 배지는 지금 기준이에요 — 다른 달에 환불된 품목도 `환불` 로 보여요」(§6.3) | 검수 「실물에서 만날 자리」 2 · 기본값(OQ-113) |
| 표 | §3.2 · 정렬 §3.3 | D1-02 · D1-03 |

### 3.2 표 — 수납 묶음 · 품목 줄

**한 줄 = 품목 하나 · 같은 수납의 품목은 묶어 보인다**(D1-02). 묶음 머리 = 수납 단위 칸, 그 아래 줄 = 품목 단위 칸(품목 줄은 그 수납의 **첫 승인 결제가 있는 달에만** — §6.2). 칸은 D1-03 + 품목 종류(D1-07).

| 칸 | 단위 | 보이는 값 | 근거 |
|---|---|---|---|
| 결제일 | 수납(머리) · 결제 · 취소 · 환불 줄 | `MM-DD HH:mm`(KST). 머리 = 그달 그 수납 승인 결제의 **⑤ 승인 일시 중 가장 이른 것**(승인이 없으면 첫 취소 · 환불 줄 시각) · 결제 줄 = 승인 일시 · 취소 줄 = 취소 일시 · 환불(반환) 줄 = 반환 일시. ⑤ 와 잇지 못한 거래는 `—` + 흐린 「시각 없음」(§5.4) | D1-03 · D1-06 · R§2(⑤ 줄) · §5.2 · §5.4 |
| 손님 이름 | 수납 | 이름 그대로(가리지 않는다 — 병원 내부 화면). 못 찾으면 `—` + 흐린 「이름 없음」 | D1-03 |
| 방문일 | 수납 | `MM-DD`(KST) — 그 수납이 걸린 일정의 예약 시작 날짜(`reservation.startDateTime`). 없으면 `—` | D1-03 · R§2(원천 줄) · §5.2 |
| 최초 유입 채널 | 수납 | `visitorFunnelName` 문자열 그대로. 비면 `(없음)` 회색 | D1-04 · §6.6 |
| 수납 | 수납 | 수납 id **끝 6자리** + 결제 수단 칩(참고 · 예: `카드` `현금` · 분할이면 칩 여러 개) | D1-02 「결제 수단 · 분할 결제는 수납 단위 참고로만」 · 기본값(OQ-113) |
| 품목 종류 | 품목 | `상품` · `기타 상품` · `선불카드` | D1-07 |
| 상품 | 품목 | 상품명(§6.5 — 비면 선불카드명 · 기타 상품명). 결제 · 취소 · 환불 줄 = `—` | D1-03 · D1-07 |
| 옵션 | 품목 | 상품 옵션명 · 없으면 `—` | D1-03 |
| 품목 금액 | 품목 · 결제 · 취소 · 환불 줄 | `1,000,000` (원 · 천 단위 쉼표 · 오른쪽 정렬). 음수는 `-1,000,000` 빨간 글자. 통화가 `KRW` 가 아니면 숫자 뒤에 통화 코드(§6.7) | D1-02 · D1-06 |
| 상태 | 품목 · 결제 · 취소 · 환불 줄 | 배지 — `승인` · `부분 환불` · `환불` · `취소` · `결제` · 그 밖은 KOS 뜻 그대로(§6.3 표) | D1-03 · 스펙 |

- 묶음 머리 오른쪽 끝에 **「그달 결제 1,000,000」**(그 수납의 그달 승인 결제 합 · 참고). 품목 줄이 있는 묶음에서 품목 합과 다르면 `⚠ 결제 ≠ 품목` 작은 배지(§6.4) — **문구 · 조건은 WP-LIVE L5 · L10 결과로 다시 정한다**(OQ-106) · 통화가 섞인 수납은 합 대신 `⚠ 통화 섞임`(§6.7)
- 품목 줄이 이 달에 없는 수납(첫 승인 결제가 다른 달 — §6.2)은 머리 + 결제 · 취소 · 환불 줄만 · 머리에 「품목은 다른 달에 · 첫 승인 MM-DD」 회색 글자(`firstApprovedAt` 이 `null` 이면 「품목은 다른 달에」)
- 품목을 못 찾은 수납(`itemsMissing`)은 머리만 있고 그 아래 줄 자리에 「품목을 찾지 못했어요」 한 줄(§6.4)
- 줄을 눌러도 아무 일 없음(상세 · 링크 없음) · 기본값(OQ-113)

### 3.3 정렬

묶음 = 머리 결제일(§3.2 — ⑤ 승인 일시 · 승인이 없으면 첫 취소 · 반환 일시) 오름차순 · 시각 없는 묶음은 맨 뒤 · 같으면 수납 id · 묶음 안 = 품목 줄(KOS 응답 차례) 다음 결제 · 취소 · 환불 줄(§5.4 시각 차례 · 시각 없는 줄은 맨 뒤). ① `lastUpdatedPaymentDateTimeUtc` 로 정렬하지 않는다(R§2 ⑤ 줄). 차례 세부는 기본값(OQ-113).

### 3.4 상태 화면

| 상태 | 화면 | 근거 |
|---|---|---|
| 불러오는 중 | 표 자리 스피너(medikit `Loading`) + 「KOS 에서 불러오는 중이에요 — 수십 초 걸릴 수 있어요」. 월 선택 · `[다시 불러오기]` 꺼짐 | §5.3(수납마다 일정 조회) · 기본값(OQ-113) |
| 빈 달 | 「이 달에는 결제가 없어요」 · 건수 줄 0 | 기본값(OQ-113) |
| back 주소 비어 있음 | 「back 주소(NEXT_PUBLIC_API_BASE_URL)가 비어 있어요 — front/.env.local 에 넣고 front 를 다시 띄우세요」 · back 을 부르지 않는다 | 코드(cc-prototype procedure `lib/api.ts` `CONFIG_ERROR`) |
| 오류 | 「매출을 불러오지 못했어요」 + 오류 `message`(§4.3) + `[다시 시도]` — 이전 달 결과를 남겨 두지 않는다(어느 달 것인지 헷갈리지 않게) | 기본값(OQ-113) |
| back 이 안 뜸(네트워크) | 「back 에 연결하지 못했어요(back 이 떠 있나요?)」 + `[다시 시도]` | 기본값(OQ-113) |

## 4. back API

### 4.1 경로

| 경로 | 요청 | 응답 | 근거 |
|---|---|---|---|
| **`GET /api/sales`** | 쿼리 `month=YYYY-MM`(없으면 이번 달 KST) · `refresh=1`(선택 — 캐시 건너뜀) | 200 §4.2 · 오류 §4.3 | D1-01 · D1-05 |
| `GET /api/health` | 없음 | `{ok: true, kosConfigured: bool}` — 키 · 주소 값은 싣지 않는다 | 코드(cc-prototype procedure `HealthResponse` 모양) · 기본값(OQ-111) |

- 경로는 이 둘뿐(`test_route_count_2`). 쓰기 경로(POST · PUT · DELETE) 0
- 모든 응답 헤더 `Cache-Control: no-store`(이름 · 결제가 브라우저 캐시에 남지 않게) · 기본값(OQ-117)

### 4.2 응답 shape (front 계약 — `schemas/sales.py` ↔ `front/lib/types.ts`)

```jsonc
{
  "month": "2026-10",
  "rangeUtc": { "from": "2026-09-30T15:00:00Z", "to": "2026-10-31T14:59:59Z" },  // §6.1 — KOS 에 보낸 값 그대로
  "fetchedAt": "2026-10-29T14:03:12+09:00",   // KOS 에서 받은 시각(KST) — 캐시면 그때 시각
  "cached": false,
  "counts": {
    "purchases": 2,          // 묶음 수 = purchases.length
    "itemLines": 2,          // kind = "item" 줄 수
    "paymentLines": 1,       // kind = "payment" 줄 수(품목이 다른 달인 수납의 승인 결제 — §6.2)
    "reversalLines": 1,      // kind = "cancel" | "spent" 줄 수
    "transactions": 4,       // KOS 결제 통계 행 수(totalCount 와 같아야 함 — §9.2)
    "ignoredTransactions": 0,  // REQUESTED · FAILED 등 줄로 안 만든 행(§6.3) — 0 이 아니면 화면 건수 줄 옆에 「제외 n」
    "itemsMissing": 0,       // itemsMissing = true 인 수납 수
    "visitorMissing": 0,     // 이름을 못 찾은 수납 수
    "itemsElsewhere": 1,     // itemsHere = false 이고 이 달 ① 에 승인 행이 있는 수납 수(§6.2 · L11)
    "firstApprovalCanceled": 0, // 전액 취소된 승인이 첫 승인 후보에서 빠진 수납 수(§6.2 (a) · L11)
    "firstApprovedUnknown": 0,  // 첫 승인 결제 · 그 귀속 달을 대체 규칙으로 정한 수납 수(§6.2 (c) · L11)
    "unmatchedTransactions": 0, // ① 행 중 ⑤ 거래와 잇지 못해 at = null 인 줄 · 승인 행 수(§5.4 · L12)
    "atOutsideMonth": 0      // 이은 시각(at)이 조회 달(KST) 밖인 ① 행 수(OQ-119 · L12)
  },
  "purchases": [
    {
      "purchaseId": "…a1b2c3",              // KOS 수납 id(전체 문자열 · 화면은 끝 6자리)
      "paidAt": "2026-10-03T11:20:00+09:00",  // §3.2 결제일 — 그달 승인 결제(⑤ 와 이은 것)의 approvedDateTimeUtc 중 가장 이른 것 · 없으면 null
      "firstApprovedAt": "2026-10-03T11:20:00+09:00", // 「취소 안 된 첫 승인 결제」(§6.2)의 ⑤ approvedDateTimeUtc · 없으면 null
      "itemsHere": true,                    // 품목 줄을 이 달에 보이나 = 첫 승인 결제 행이 이 달 ① 에 귀속됐나(§6.2)
      "visitorId": "…",
      "visitorName": "홍**",                // null = 못 찾음
      "visitDate": "2026-10-03",            // KST 날짜 · null = 일정 없음
      "visitorFunnelName": "(에이전시) 코드", // null = 빈 값(§6.6)
      "paymentTypes": ["CARD", "CASH"],     // 그달 승인 결제의 수단(중복 없음 · 처음 나온 차례)
      "currency": "KRW",                    // 이 수납 줄들의 통화 — 둘 이상 섞이면 null(§6.7)
      "approvedTotal": 1000000,             // 그달 승인 결제 cost.totalAmount.value 합(원) · currency = null 이면 null
      "itemsTotal": 1000000,                // kind = "item" 줄 amount 합 · itemsHere = false 면 0 · currency = null 이면 null
      "itemsMissing": false,
      "lines": [
        { "kind": "item", "itemType": "PRODUCT_OPTION", "productName": "시술 A", "productNameFrom": "product",
          "optionName": "1회", "amount": 600000, "currency": "KRW", "status": "ACCEPTED", "at": null },
        { "kind": "item", "itemType": "PREPAID_CARD_PRODUCT", "productName": "선불카드 B", "productNameFrom": "prepaidCard",
          "optionName": null, "amount": 400000, "currency": "KRW", "status": "PARTIALLY_REFUNDED", "at": null },
        { "kind": "cancel", "itemType": null, "productName": null, "productNameFrom": null,
          "optionName": null, "amount": -400000, "currency": "KRW", "status": "CANCELED", "at": "2026-10-20T16:05:00+09:00",
          "paymentType": "CARD" }
      ]
    }
  ]
}
```

| 필드 | 값 | 비고 |
|---|---|---|
| `lines[].kind` | `item` · `payment` · `cancel` · `spent` | `payment` = 품목이 다른 달인 수납의 그달 `APPROVED` 행(§6.2) · `cancel` = `CANCELED` 행 · `spent` = `SPENT` 행(§6.3) |
| `lines[].itemType` | `PRODUCT_OPTION` · `ETCETRA_PRODUCT` · `PREPAID_CARD_PRODUCT` · `PurchaseItemType_UNSPECIFIED` | 스펙 `OpenPurchaseItemStatisticsItem.purchaseItemType` 그대로 · 화면 이름은 front `lib/labels.ts` 한 곳 · `item` 줄에만 |
| `lines[].productNameFrom` | `product` · `prepaidCard` · `etcetera` · `none` | §6.5 — 어느 칸에서 읽었나(시험 · 확인용) |
| `lines[].status` | 품목 = 스펙 `purchaseStatus` 값 · 결제 줄 = `APPROVED` · 취소 줄 = `CANCELED` · 반환 줄 = `SPENT` | 화면 이름 §6.3 |
| `lines[].amount` | 정수 · 취소 · 반환 줄은 음수 | KOS `Money.value`(int64) 그대로 |
| `lines[].currency` | KOS `Money.currency` 그대로(예: `KRW`) | 스펙 `protos.Money = {currency, value}` · 검수 W-5 |
| `lines[].at` | 결제 줄 = ⑤ `approvedDateTimeUtc` · 취소 줄 = ⑤ `canceledDateTimeUtc` · 반환 줄 = ⑤ `spentDateTimeUtc`(KST ISO) · 잇지 못하면 `null` · 품목 줄 = `null` | §5.2 · §5.4 · R§2(⑤ 줄) |
| `lines[].paymentType` | 결제 · 취소 · 반환 줄에만 | 스펙 `TransactionPaymentType` |
| 금액 합 필드 | `approvedTotal` · `itemsTotal` 만(수납 단위) | 월 합계 필드 없음(§1.2) |

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

- **「없음」은 오류가 아니다** — ③ · ④ 가 HTTP 400 이고 `errorProperties` 에 `{key: "purchaseId", reason: "NotFound"}`(③) · `{key: "visitorId", reason: "NotFound"}`(④)가 있을 때만 그 수납의 칸을 비운다(§6.4). 스펙 「에러 응답」(`reason: NotFound` = 「대상이 없음」) · `FindScheduleByPurchaseIdPurchaseIdNotFoundError` · `GetVisitorVisitorNotFoundError` · 검수 F-1
- **그 밖의 실패(「없음」 아닌 4xx · 5xx · 429 · 네트워크)는 달 전체를 오류로** 낸다 — 일부만 빠진 리스트를 보여 주지 않는다 · 기본값(OQ-114)
- 오류 · 로그에 키 · 토큰 · 테넌트 id · 이름 · 금액을 싣지 않는다(§7.3)

### 4.4 캐시 · 동시성

| 항목 | 계약 | 근거 |
|---|---|---|
| 캐시 | back **메모리**에 달별 응답 하나(§4.2 꼴 — KOS 원본 응답이 아니다) · 유효 `SALES_CACHE_SEC`(기본 600초). 지난 달 · 이번 달 구분 없음. `refresh=1` 이면 무시하고 새로 받아 덮는다. back 을 내리면 사라진다(파일 · DB 0) | DEC-001 열린 것 「요청마다 할지 저장해 둘지」 → 기본값(OQ-105) |
| 같은 달 겹친 요청 | 같은 달을 받는 중이면 뒤 요청은 그 결과를 기다린다(달별 잠금) — KOS 를 두 번 돌지 않게 | 기본값(OQ-105) |
| 수납별 조회 동시성 | 일정 조회(§5.3 ③)를 **동시에 최대 `SALES_KOS_CONCURRENCY`(기본 8)** 개. 스펙 한도 「같은 IP 1분 3,000회」 · 한 달 수납 수백 건(Q5 — 수납 id 394) 기준 여유 | 스펙 「호출 한도」 · Q5 · 기본값(OQ-105) |
| 토큰 다시 받기 | 401 이 동시에 여러 개 나도 **토큰 교환은 한 번만**(잠금 — 먼저 받은 쪽 토큰을 나머지가 쓴다) | 검수 NOTE 4 · 기본값(OQ-105) |
| 시간 초과 | KOS 호출 하나 15초(코드 `httpx timeout=15`) | 코드 |

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
| 결제일(결제 · 취소 · 반환 줄) | `lines[].at` | 그 ① 행과 이은 ⑤ 거래의 `approvedDateTimeUtc`(결제) · `canceledDateTimeUtc`(취소) · `spentDateTimeUtc`(반환) → KST | `purchaseId` + §5.4 |
| (품목을 보일 달) | `firstApprovedAt` · `itemsHere` | ⑤ `transactions[]` 로 「취소 안 된 첫 승인 결제」를 고르고(§6.2 s1 ~ s3) · 그 거래가 이 달 ① `APPROVED` 행과 이어졌나(§5.4)로 판정(§6.2 s4 · s5) | `purchaseId` = ⑤ `data[].id` + §5.4 |
| 손님 이름 | `visitorName` | ③ `data.visitor.name` · 「없음」이면 ④ `data.name` | `purchaseId` → ③ · `visitorId`(①) → ④ |
| 방문일 | `visitDate` | ③ `data.reservation.startDateTime` → **오프셋을 읽어** KST 날짜(필드 이름에 `Utc` 가 없고 스펙 설명은 「ISO 8601 date-time」뿐 — `Z` 를 가정하지 않는다) | `purchaseId` |
| 최초 유입 채널 | `visitorFunnelName` | ① `visitorFunnelName`(같은 수납 행들의 첫 비어 있지 않은 값) | `purchaseId` |
| 수납 | `purchaseId` · `paymentTypes` | ① `purchaseId` · `APPROVED` 행 `paymentType` | — |
| 품목 종류 · 상품 · 옵션 · 품목 금액 · 상태 | `lines[]`(`kind = item`) | ② `purchaseItemType` · `productTitle`(§6.5) · `productOptionTitle` · `cost.totalAmount{value,currency}` · `purchaseStatus` | `purchaseId`(② ↔ ①) |
| 결제 줄 | `lines[]`(`kind = payment`) | ① `APPROVED` 행 `cost.totalAmount` · `paymentType` | `purchaseId` |
| 취소 · 환불 줄 금액 · 상태 | `lines[]`(`kind = cancel · spent`) | ① `cost.totalAmount{value,currency}`(음수) · `status` | `purchaseId` |
| 그달 결제(참고) | `approvedTotal` | ① `APPROVED` 행 `cost.totalAmount.value` 합 | `purchaseId` |

- **결제일 원천**: ① 행에는 결제 생성 · 승인 시각 필드가 없다(스펙 `OpenTransactionStatisticsItem` 에 시각은 `lastUpdatedPaymentDateTimeUtc` · `visitorCreatedDateTimeUtc` 뿐 · 거래 id 도 없음). 그래서 결제일은 **⑤ 거래의 승인 · 취소 · 반환 일시**에서 읽고(R§2 ⑤ 줄), ① 행과 ⑤ 거래는 §5.4 로 잇는다. 달 귀속 필터는 ① `createdTimeUtc` 그대로다 — 보이는 결제일과 다를 수 있다(OQ-119)
- **결제 통계 행만으로 유입 · 손님 · 금액이 나온다** — 운영 10월 수집본에서 결제 행의 유입 = 일정 유입 451/451(Q5). 그래서 유입은 ③ 이 아니라 ① 에서 읽는다
- 손님 유입은 조회 시점 값이다 — 한 손님의 `visitorFunnelName` 이 행마다 다른 경우 0(Q4 · 추정 「조회 시점의 손님 값」). 지난 달을 다시 보면 그 사이 바뀐 유입이 보일 수 있다 · OQ-109

### 5.3 한 번 조회의 순서

```text
GET /api/sales?month=2026-10
 ① 결제 통계 — 달 범위(§6.1) 전부 · cursor 끝까지         → 행 T[]
    purchaseIds = T 의 purchaseId 중복 없이(처음 나온 차례)
 ⑤ 수납 요약 — purchaseIds 100개씩                          → 수납마다 「취소 안 된 첫 승인 결제」 → ① 행과 잇기(§5.4) → itemsHere(§6.2)
 ② 품목 통계 — 달 시작 −31일 ~ 달 끝 · cursor 끝까지       → 행 I[] · itemsHere 인 수납 것만 남김
 ③ 수납마다 findScheduleByPurchaseId(동시 최대 8)           → 이름 · 방문일만 꺼냄
 ④ ③ 이 「없음」인 수납만 getVisitor(visitorId)             → 이름만 꺼냄
 ⑥ 묶음 · 줄 만들기(§6) → 캐시(§4.4) → 200
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
| 이은 뒤 시각 | `APPROVED` → `approvedDateTimeUtc` · `CANCELED` → `canceledDateTimeUtc` · `SPENT` → `spentDateTimeUtc`. 그 필드가 비어 있으면(스펙상 required 아님) 못 이음과 같게 | R§2 ⑤ 줄 · 스펙 `TransactionPaymentDateTime` |
| 못 이음 | 줄 · 금액 · 상태 · 묶음은 ① 그대로(달에서 빠지지 않는다) · **`at = null`** → 화면 결제일 `—` + 흐린 「시각 없음」 · 정렬 맨 뒤 · `counts.unmatchedTransactions` 로 센다. **① `lastUpdatedPaymentDateTimeUtc` 로 채우지 않는다**. 머리 `paidAt` 은 이은 승인만으로 정한다(하나도 없으면 `null` → `—`) | R§2 ⑤ 줄 · 기본값(OQ-120) |
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

**규칙 한 줄: 품목 줄은 그 수납의 「취소 안 된 첫 승인 결제 행」이 ① 로 귀속된 달에 나온다.** 다른 달엔 결제 · 취소 · 환불 줄만 나온다. 달을 정하는 시계는 ① 귀속(`createdTimeUtc` 필터) 하나뿐이고, ⑤ 는 「어느 거래가 첫 승인인가」만 정한다 — 그래서 한 수납의 품목은 **어느 달에든 정확히 한 번** 나온다(R§2 분할 결제 줄 · 수정 4판 지시 · 검수 r2 W-1).

| 경우 | 보이는 것 | 근거 |
|---|---|---|
| 그 달 ① 에 행이 하나라도 있는 수납 | 묶음이 된다(승인이든 취소든) | D1-06 |
| **`itemsHere = true`**(아래 s4 · s5) | 품목 줄(②) + 이 달 취소 · 환불 줄. 이 달 승인 결제는 줄로 만들지 않는다(품목이 대신) | **R§2(분할 결제 줄)** · D1-02 |
| **`itemsHere = false` 이고 이 달 승인 행 있음**(분할 결제가 달을 넘음 · 재결제 등) | **품목 줄 없이** 이 달 승인 결제를 `payment` 줄(양수)로 + 취소 · 환불 줄 · 머리 「품목은 다른 달에 · 첫 승인 MM-DD」 · `counts.itemsElsewhere` | **R§2(분할 결제 줄 — 「다른 달엔 결제 · 취소 줄만 · 한 품목이 두 달에 전액으로 두 번 나오지 않게」)** |
| 취소 · 반환만 이 달에 있는 수납(원 결제는 앞 달) | 품목 줄 없이 취소 · 반환 줄만 · `paidAt = null` → 머리 결제일은 첫 취소 · 반환 줄 시각(⑤ `canceledDateTimeUtc` · `spentDateTimeUtc` — §5.4). 원 결제 달의 리스트는 고치지 않는다 | D1-06 「원 결제 달을 고치지 않는다」 · Q6 「취소 행은 취소한 시각으로 기간에 들어간다」 |

**판정 순서(s1 ~ s5 · 수납마다 · ⑤ 는 수납의 모든 달 거래를 준다 — 조회 달과 상관없이 같은 답이 나온다):**

| 단계 | 계약 | 근거 |
|---|---|---|
| s1 후보 | ⑤ `transactions[]` 중 `status = APPROVED` | 스펙 `PurchaseSummaryTransaction` |
| s2 (a) 전액 취소 뺌 | 같은 수납 ⑤ `CANCELED` 거래 중 `canceledRefId` 가 그 승인 `id` 를 가리키는 것들의 `price.value` 절댓값 합 ≥ 그 승인 금액 절댓값이면 **후보에서 뺀다**. 부분 취소는 후보에 남긴다. 뺀 것이 있으면 `counts.firstApprovalCanceled`. **후보가 다 빠지면**(수납 전체 취소) 빼지 않은 원래 후보로 되돌린다 — 품목은 원 첫 승인 달에 한 번 나오고 취소 줄로 순액 0 | 스펙 `canceledRefId` 「취소 참조 ID」 · `getTransactionList` 설명 「환불 · 취소는 음수 금액의 새 거래 … `canceledRefId` 가 원거래의 `id`」 · Q6(취소 25/25 가 `canceledRefId` 로 원 결제를 찾음) · 검수 r2 W-1 a · 부분 취소 · 다 빠짐 = 기본값(OQ-121) |
| s3 「첫」 고르기 | 남은 후보를 `paymentDateTime.approvedDateTimeUtc` 차례로(파싱한 시각). 승인 시각이 없는 후보가 있으면 **그 수납의 모든 후보를** `createdDateTimeUtc`(⑤ 「거래 생성 일시」 · deprecated) → 없으면 `paymentDateTime.lastUpdatedDateTimeUtc`(required) 차례로 정렬하고 · 같으면 `id` 차례. 대체 정렬을 쓴 수납은 `counts.firstApprovedUnknown` | 스펙 `TransactionPaymentDateTime`(`lastUpdatedDateTimeUtc` 만 required) · `PurchaseSummaryTransaction.*.paymentDateTime` 설명(「없다면 하위 호환을 위해 `createdDateTimeUtc`」) · 검수 r2 W-1 c · 기본값(OQ-121) |
| s4 귀속 달 = 품목 달 | 그 「첫 승인 결제」가 **이 달 ① `APPROVED` 행과 이어지면**(§5.4) `itemsHere = true` · 아니면 `false`. 자정 경계(10-31 23:59 생성 · 11-01 승인)여도 ① 이 10월에 넣은 행이면 10월에 품목이 나온다 · 11월엔 그 수납 묶음이 없다 | D1-06(귀속 = ① 결제 시각) · 수정 4판 지시 (b) · 검수 r2 W-1 b |
| s5 잇기 실패 | 「첫 승인 결제」가 이 달 ① 의 어떤 행과도 이어지지 않았는데 이 달 ① 에 **못 이은 `APPROVED` 행**이 있으면, 그 거래의 ⑤ `createdDateTimeUtc`(없으면 `lastUpdatedDateTimeUtc`) KST 달 = 이 달일 때만 `itemsHere = true` — ① 귀속 시계와 같은 축으로 보는 대체(추정 — `createdDateTimeUtc` 가 ① `createdTimeUtc` 와 같은 값인지는 스펙에 없음) · `counts.firstApprovedUnknown` | 검수 r2 W-1 c · NOTE 1 · 기본값(OQ-121) |
| ⑤ 에 수납 없음 | ⑤ 가 아무 거래도 안 줘서 첫 승인을 정할 수 없다 → 이 달 ① 에 `APPROVED` 행이 있으면 `itemsHere = true` · `counts.firstApprovedUnknown`. **이 경우만 분할 결제 수납이 두 달에 품목을 보일 수 있다**(달마다 독립 판정) — 운영 10월은 ① 에 있는 수납이 ⑤ 에서 빠진 경우 0(Q5 — 안 돌아온 170건은 결제 · 품목 통계에도 없음) | 스펙 `GetPurchaseSummariesQuery.purchaseIds` 「존재하지 않거나 삭제된 수납 ID는 응답에 포함되지 않습니다」 · Q5 · 기본값(OQ-116) |

- `firstApprovedAt` = 고른 「첫 승인 결제」의 ⑤ `approvedDateTimeUtc`(없으면 `null`) — 화면 머리 문구에만 쓴다. 달 판정에는 쓰지 않는다(s4)
- 대체(s3 대체 정렬 · s5 잇기 실패 · ⑤ 에 수납 없음)를 탄 수납은 전부 `firstApprovedUnknown` 으로 세어 드러낸다 — L11

### 6.3 상태 · 취소 · 환불

① `status`(결제 통계 — 스펙 `TransactionStatus`) 처리:

| ① `status` | 스펙 뜻 | 처리 | 화면 상태 |
|---|---|---|---|
| `APPROVED` | 승인됨 | 묶음 · 결제일 · 결제 수단 · `approvedTotal` 에 넣음. `itemsHere = true` 면 줄을 만들지 않고(줄은 품목), `false` 면 **양수 `payment` 줄**(§6.2) | `결제`(`payment` 줄) |
| `CANCELED` | 취소 거래 — 「거래가 취소된 상태가 아니라 취소 거래」 · 금액 음수(Q6 25/25) | **음수 줄 `kind: cancel`** | `취소` |
| `SPENT` | 반환 거래 — 「거래 취소 없이 돈을 돌려줄 때 · 금액이 음수」 | **음수 줄 `kind: spent`** · 운영 10월 0건(Q6) | `환불` |
| `REQUESTED` · `FAILED` · 그 밖 | 요청됨 · 처리 실패(돈이 움직이지 않음) | 줄 · 합에 넣지 않음 · `counts.ignoredTransactions` 로 센다 · 운영 10월 0건(Q6) | — · 기본값(OQ-115) |

② `purchaseStatus`(품목 — 스펙 `PurchaseStatus`) 는 품목 줄 상태 배지로 그대로:

| `purchaseStatus` | 스펙 뜻 | 화면 상태 |
|---|---|---|
| `ACCEPTED` | 수납 완료 | `승인` |
| `PAID` | 지불 수납 | `승인` |
| `PARTIALLY_REFUNDED` | 부분 환불 | `부분 환불` |
| `REFUNDED` | 환불 | `환불` |
| `INITIALIZED` | 미수납 | `미수납` |
| 그 밖(`PURCHASE_STATUS_UNSPECIFIED` 포함) | — | 값 그대로 |

- **품목 상태는 조회 시점의 현재 상태**다(② 에 달별 상태가 없다). 10월에 판 품목이 11월에 환불되면, 10월 리스트를 다시 볼 때 그 품목 배지가 `환불` 로 보인다(§3.1 안내 한 줄). 돈의 움직임(음수)은 **취소된 달의 취소 줄**에만 있다 — D1-06
- **환불 품목 금액 = 원 가격으로 본다**(기본값 · OQ-102). 근거: 코디가 10-28 수집본에서 수납마다 「`purchaseStatus ≠ REFUNDED` 인 품목 `cost.totalAmount` 합」 = 「그 수납의 결제 행(`APPROVED` + `CANCELED` 음수) 전부 합」을 비교해 **품목 있는 수납 444건 전부 일치**(DEC-001 Context 「444/444」의 정의 — 수정 1판 지시 W-4). `REFUNDED` 품목을 **빼야** 순액과 맞았다 = 환불 품목의 `cost.totalAmount` 는 0 이 아니라 원 가격이다(스펙 뜻 「잔존 가치 금액 또는 최종가」 중 최종가). 그래서 같은 달 승인 + 취소인 수납은 품목 줄 +X · 취소 줄 −X 로 순액이 맞고, 이중 차감은 없다. `PARTIALLY_REFUNDED` 품목 값이 어느 쪽인지는 이 비교로 갈리지 않는다 → WP-LIVE L10 으로 실물 확인
- 결제 통계의 취소 행과 품목은 이어지지 않는다(결제 수단 · 취소는 수납 단위 — DEC-001 Context 「결제 수단은 품목과 이어지지 않는다」). 그래서 취소 줄은 어느 품목의 취소인지 적지 않는다(상품 · 옵션 `—`)

### 6.4 품목 조인 · 못 찾은 것

| 항목 | 계약 | 근거 |
|---|---|---|
| 조인 키 | ② `purchaseId` = ① `purchaseId` | Q6 · DEC-001 Context(10월 승인 수납 392건 전부 품목 있음) |
| ② 범위 | ② 의 기간 필터는 **품목 생성 시각**(`createdDateTimeUtc` — 「구매 일시」)이라 결제 시각과 다를 수 있다. 앞 달에 수납을 만들고 이번 달에 첫 결제한 경우를 잡으려고 **달 시작 −31일 ~ 달 끝**으로 부르고 `itemsHere` 인 수납만 남긴다 | 스펙 `OpenGetPurchaseItemStatisticsQuery.createdDateTimeUtcFrom` · 기본값(OQ-116) |
| 그래도 없음 | `itemsHere = true` 인데 품목이 0줄인 수납 = `itemsMissing: true` · 머리만 · 「품목을 찾지 못했어요」 · `counts.itemsMissing` — **빠뜨리지 않고 드러낸다** | 기본값(OQ-116) |
| 결제 ≠ 품목 | `itemsHere = true` 이고 `approvedTotal ≠ itemsTotal` 이면 머리에 `⚠ 결제 ≠ 품목`. 숫자를 맞추려고 고치지 않는다. 정상인데도 뜰 수 있는 자리(같은 달 환불 · 부분 환불 품목 — 승인 합엔 취소가 안 들어감 · 첫 승인은 이 달인데 나머지를 다음 달에 결제)가 있어 **문구 · 조건은 WP-LIVE L5 · L10 결과로 다시 정한다** | DEC-001 Context(444/444 — §6.3) · 검수 W-6 · OQ-106 |
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
| 값 | 문자열 그대로 · 바꾸거나 묶지 않는다(어느 코드가 에이전시인지 이 판은 판정하지 않음) | D1-01 · Q1 「KOS 에 에이전시 구조화 표시 없음」 |
| 빈 값 | `null` → `(없음)`. 운영 10월 일정 기준 손님 유입 빈 값 8.9%(Q3) | Q3 |
| 자유 텍스트 | `visitorFunnelDetail` · `reservationMemo` · 손님 메모 등은 **읽지도 보이지도 않는다** — 빈 유입을 메모로 채우지 않는다 | [[no-inference-from-free-text]] · Q3 「자유 텍스트에만 있음 6건 — 세지 않았다」 |

### 6.7 금액 · 통화

| 항목 | 계약 | 근거 |
|---|---|---|
| 금액 기준 | 품목 금액 = ② `cost.totalAmount.value` · 결제 금액 = ① `cost.totalAmount.value`(공급가 · VAT 가 아니라 총액) | D1-02 「금액은 품목 금액」 · 리포트 「정할 것 7」 열림 → 기본값(OQ-108) |
| 통화 | 줄마다 `currency` = KOS `Money.currency` 그대로. 수납 `currency` = 그 수납 줄들의 통화가 하나면 그 값, **둘 이상 섞이면 `null`** — 이때 `approvedTotal` · `itemsTotal` 도 `null`, 머리는 합 대신 `⚠ 통화 섞임` · `⚠ 결제 ≠ 품목` 비교 안 함 | 스펙 `protos.Money = {currency, value}` · 검수 W-5 (a) · 기본값(OQ-118) |
| 화면 | `KRW` 줄은 숫자만 · 그 밖 통화는 숫자 뒤에 통화 코드. 운영 10월은 전부 `KRW`(Q6) | Q6 · 기본값(OQ-118) |

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
- **③ · ④ 응답에서 꺼내는 것은 `visitor.name` · `reservation.startDateTime`(③) · `name`(④) 뿐**이다. ③ 응답(`ScheduleContract`)에 같이 오는 전화 · 생년월일 · 차트번호 · 메모 · 예약 메모, ④ 응답의 전화 · 여권 · 생년월일은 **변수에 남기지 않고 캐시 · 로그 · 응답에 싣지 않는다**(파싱 직후 두 값만 남김) · 검수 NOTE 3
- **⑤ 응답에서 꺼내는 것은 `data[].id` · `transactions[].{id, status, paymentType, price, paymentDateTime, canceledRefId, createdDateTimeUtc}` 뿐**이다. 같이 오는 `purchaseMemo`(자유 텍스트) · `items` · `assignees` · 거래 담당자 · 카드 설정은 남기지 않는다 · 검수 r2 NOTE 2
- 로그에 남기는 것: 달 · 건수(`counts`) · 걸린 시간 · KOS 오류 이름. **이름 · 금액 · 상품명 · 수납 id · 손님 id · 키 · 토큰 · 테넌트 id 를 남기지 않는다**. `httpx` 로그는 WARNING 이상만(요청 URL 이 찍히지 않게 — 코드 `main.py`)
- 응답 · 캐시는 메모리에만 — 파일 · DB · 브라우저 저장소(`localStorage` 등) 0
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

- **안 복사**: `components/common/AppHeader.tsx`(메뉴 · 세션 · 시술 현황 링크 — 이 앱엔 없음) · `lib/session.ts` · `lib/hooks.ts` 의 세션 훅 · `app/login` · `(main)` 묶음
- medikit 컴포넌트는 패키지에서 바로 쓴다(복사 아님): `Button`(월 이동 · 다시 불러오기 · 다시 시도) · `Badge`(상태 · 결제 수단 · 경고) · `Loading`(불러오는 중). 표는 일반 `<table>` + Tailwind(medikit 1.4.0 에 표 컴포넌트를 cc-prototype procedure 가 안 쓴다 — 코드 import 집계)
- medikit 설치는 cc-prototype procedure/front 와 같은 방식(사용자 npm 설정) — 이 문서는 레지스트리 · 토큰을 적지 않는다

## 9. 검증

### 9.1 back 단위 시험 (pytest · KOS 가짜 transport · 운영 호출 0)

| # | 시험 |
|---|---|
| 1 | 월 경계 — `2026-10` → `from 2026-09-30T15:00:00Z` · `to 2026-10-31T14:59:59Z` · 12월 → 다음 해 1월 경계 · `bad_month`(꼴 · 13월 · 다음 달) |
| 2 | 조회 전용 가드 — 허용 밖 경로 · `/commands/` 경로 → `GuardBlocked` · 가짜 transport 호출 0 · 토큰 교환은 인증 함수에서만 · 허용 경로 상수가 정확히 5개 |
| 3 | 조인 — 승인 결제 2행(카드 · 현금) + 품목 2행 → 묶음 1 · 품목 줄 2 · `paymentTypes` 2 · `paidAt` = 이른 쪽 |
| 4 | 취소 — 같은 달 승인 + 취소 → 품목 줄 + 음수 `cancel` 줄 · 취소만 있는 수납 → 품목 줄 0 · `paidAt null` |
| 5 | `SPENT` → 음수 `spent` 줄 · `REQUESTED` · `FAILED` → 줄 0 · `ignoredTransactions` 증가 |
| 6 | 상품명 — `productTitle` 빈 품목이 `prepaidCardName` · `etceteraProductName` 순으로 · 다 비면 `none` |
| 7 | 유입 빈 값 → `visitorFunnelName null` · `visitorFunnelDetail` 에 값이 있어도 응답 어디에도 안 나옴 |
| 8 | 품목 없음 → `itemsMissing true` · `counts.itemsMissing` · 결제 ≠ 품목 → `approvedTotal ≠ itemsTotal` 그대로 |
| 9 | **「없음」** — ③ 이 400 `{errorProperties:[{key:"purchaseId",reason:"NotFound"}]}` → ④ 로 이름 · `visitDate null` · ④ 도 400 `{key:"visitorId",reason:"NotFound"}` → `visitorName null` · `visitorMissing` 1 · 달은 200 |
| 9b | **「없음」 아님** — ③ 이 400 이지만 다른 reason(예: `{key:"purchaseId",reason:"Required"}`) → 달 전체 502 `kos_rejected` · ③ 404 → 달 전체 502 `kos_rejected`(「없음」으로 삼키지 않음) · ③ 500 → 502 `kos_unavailable` |
| 10 | 페이지 — ① 이 `nextCursor` 를 주면 다음 요청에 `cursor` · `limit` 같이 · 끝까지 · `counts.transactions` = 첫 페이지 `totalCount` |
| 11 | 오류 매핑 — 429 → 503 `kos_busy` · 401 → 토큰 다시 받기 1회 → 또 401 → 502 `kos_rejected` · 네트워크 → 502 `kos_unavailable` · 키 비어 있음 → 503 `kos_not_configured` |
| 12 | 캐시 — 같은 달 두 번째 요청은 KOS 호출 0 · `cached true` · `refresh=1` 은 다시 부름 · 동시 두 요청에 ① 호출 1 |
| 13 | 동시성 — ③ 이 동시에 `SALES_KOS_CONCURRENCY` 를 넘지 않음 |
| 14 | 로그 — caplog 에 가짜 이름 · 가짜 금액 · 수납 id · 키 · 토큰 문자열 0 |
| 15 | 경로 수 2 · 응답 헤더 `Cache-Control: no-store` · CORS 허용 출처 하나 |
| 16 | 시각 오프셋 — ③ `startDateTime` 이 `2026-10-03T23:30:00Z` → `visitDate 2026-10-04` · `2026-10-03T23:30:00+09:00` → `2026-10-03` |
| 17 | 분할 결제 — ⑤ 첫 승인이 9월 · ① 10월 승인 1행 → 10월 묶음 품목 줄 0 · 양수 `payment` 줄 1 · `itemsHere false` · `counts.itemsElsewhere` 1 · 같은 수납을 9월로 조회하면 품목 줄 있음 · ⑤ 에 수납이 없으면 이 달 승인 행으로 봄 + `firstApprovedUnknown` 1 · ⑤ 가 100개씩 나뉘어 불림 |
| 18 | 통화 — 줄 `currency` 가 KOS 값 그대로 · 한 수납에 `KRW` · `USD` 가 섞이면 수납 `currency null` · `approvedTotal null` · `itemsTotal null` |
| 19 | 토큰 다시 받기 잠금 — ③ 8개가 동시에 401 → 토큰 교환 호출 1 |
| 20 | 개인정보 — 가짜 ③ 응답에 전화 · 생년월일 · 메모 값을 넣어도 응답 · 캐시 객체 · caplog 어디에도 없음 |
| 21 | **결제일 = ⑤ 시각(§5.4)** — 동점 가르기 시각이 `…T01:02:03Z` ↔ `…T01:02:03.000+00:00` 처럼 표기만 다르면 같은 시각으로 잇는다(NOTE 1) — ① 승인 1 · 취소 1 + ⑤ 같은 거래(승인 `approvedDateTimeUtc` · 취소 `canceledDateTimeUtc` · ① `lastUpdatedPaymentDateTimeUtc` 는 다른 값)를 주면 `paidAt` · 결제 줄 `at` = 승인 일시 · 취소 줄 `at` = 취소 일시 · 응답 어디에도 ① `lastUpdatedPaymentDateTimeUtc` 값 없음 · 같은 수단 · 같은 금액 승인 2건은 `lastUpdated` 로 갈라 잇는다 · ⑤ 에 맞는 거래가 없으면 줄은 남고 `at null` · `unmatchedTransactions` 1 · ⑤ 시각이 다음 달(11-01 KST)이면 묶음은 10월에 남고 `atOutsideMonth` 1 · 정렬은 ⑤ 시각 차례 · 시각 없는 묶음 맨 뒤 |
| 22 | **(a) 전액 취소된 승인** — ⑤ 9월 승인 A · 9월 취소(`canceledRefId` = A · 같은 금액) · 10월 승인 B, ① 9월(A · 취소) · 10월(B) → **10월에 품목 줄 · `itemsHere true`** · 9월엔 품목 없이 취소 줄만(+ A 는 `payment` 줄) · `firstApprovalCanceled` 1. 부분 취소(취소 금액 < A)면 A 가 첫 승인으로 남아 9월에 품목 · 10월은 `payment` 줄. 수납 전체 취소(A 만 · 전액 취소)면 9월에 품목 + 취소 줄 |
| 23 | **(b) 자정 경계** — ⑤ 첫 승인 `approvedDateTimeUtc` = 11-01 00:00 KST · ① 10월 조회에 그 행이 있고(§5.4 로 이어짐) 11월 조회엔 없음 → **10월 `itemsHere true`** · 11월 결과에 그 수납 없음 · 10월 · 11월을 합쳐 품목 줄이 정확히 한 번 |
| 24 | **(c) ⑤ 시각 없음** — 분할 결제 수납(9월 승인 A · 10월 승인 B)에서 A · B 모두 `approvedDateTimeUtc` 없음 · `createdDateTimeUtc` 있음 → 9월 · 10월 조회가 같은 「첫 승인」(A)을 고르고 품목은 9월에만 · 두 달 다 `firstApprovedUnknown` 1. A 가 9월 ① 행과 못 이어지고 9월 ① 에 못 이은 승인 행이 있으면 A 의 `createdDateTimeUtc` 달(9월)로 9월 `itemsHere true` |

### 9.2 운영 KOS 실물 조회 (완료 조건 · 10월 · 1회)

근거: R§2(운영 키 줄 — 「이 프로젝트 코드 · WP-LIVE 실물 조회까지 · 조회만 · 로컬만」). 코디가 `back/.env` 에 운영 키를 넣고(§7.2) 로컬에서 back · front 를 띄워 **`month=2026-10` 한 번** 조회한다.

| # | 확인 | 통과 |
|---|---|---|
| L1 | 화면에 10월 리스트가 뜬다(수납 묶음 · 품목 줄 · 칸 §3.2) | 눈으로 |
| L2 | `counts.transactions` = ① 첫 페이지 `totalCount` | 같음 |
| L3 | `counts.purchases` = ① 수납 id 중복 없이 센 수 | 같음 |
| L4 | `counts.itemsMissing` | 0 이거나, 0 이 아니면 그 수와 수납 id 끝 4자리를 보고(레포 밖) — DEC-001 Context(392/392)와 비교 |
| L5 | `itemsHere = true` 이고 `approvedTotal ≠ itemsTotal` 인 수납 수 | 수만 보고. 참고 기준 = 444/444 일치의 정의(수납마다 「`REFUNDED` 아닌 품목 합」 = 「결제 행 `APPROVED` + `CANCELED` 전부 합」 — §6.3). 리스트 비교(그달 승인 합 ↔ 품목 전부 합)는 정의가 달라 환불이 낀 수납은 다를 수 있다 |
| L6 | 취소 줄 수 = ① `CANCELED` 행 수 · 음수 | 같음 |
| L7 | `visitorFunnelName` 빈 수납 수 · `visitorMissing` 수 | 수만 보고 |
| L8 | KOS 호출 로그(경로만)에 `/commands/` 가 토큰 교환 1개뿐 | 0 건(토큰 교환 빼고) |
| L9 | back 로그에 이름 · 금액 · 키 0 | grep 0 |
| L10 | `REFUNDED` · `PARTIALLY_REFUNDED` 품목이 있는 수납 수 · 그중 `approvedTotal ≠ itemsTotal` 수 · 그중 한 건씩 환불 품목 `cost.totalAmount` 가 원 가격인지(레포 밖에서 KOS 화면과 대조) | 수만 보고 — 원 가격이면 OQ-102 닫음, 아니면 사용자에게 올림 |
| L11 | **분할 결제 · 첫 승인 판정**: `counts.itemsElsewhere`(승인 결제가 두 달에 걸친 수납 · 재결제 포함) · `counts.firstApprovalCanceled`(전액 취소된 승인을 건너뛴 수납 — (a)) · `counts.firstApprovedUnknown`(대체 규칙 — (c)) | 수만 보고 — R§2 분할 결제 줄이 실제로 몇 건에 걸리는지 · (a) · (c) 가 0 이 아니면 OQ-121 을 사용자에게 올림 |
| L12 | `counts.unmatchedTransactions` · `counts.atOutsideMonth` | 수만 보고 — 0 이 아니면 OQ-119 · OQ-120 을 사용자에게 올림 |

- 결과 보고(`orchestration/work/…` — public)에는 **건수 · 같음/다름만** 적는다. 이름 · 금액 · 유입 이름 · 스크린샷 원본은 레포에 올리지 않는다(스크린샷은 가린 것만)
- 조사 리포트 수치(Q5 · Q6)는 10-28 17:21 까지라 10월 전체와 같지 않다 — 일치를 요구하지 않는다
- L5 · L10 결과로 `⚠ 결제 ≠ 품목` 배지의 문구 · 조건을 다시 정한다(OQ-106)

### 9.3 front

- `npx tsc --noEmit && npm run lint && npm run build` 통과
- back 가짜 응답(§4.2 예시 꼴)으로 상태 화면 5종(§3.4) · 묶음 · 음수 줄 · `payment` 줄 · 「품목은 다른 달에」 · `⚠ 결제 ≠ 품목` · `⚠ 통화 섞임` · `itemsMissing` 스크린샷(가짜 값)

## 10. env · 로컬 실행

### 10.1 env (`back/.env` 하나 · gitignore · `back/.env.example` 은 이름만)

| 이름 | 기본 | 뜻 |
|---|---|---|
| `KOS_OPEN_API_BASE` | (비어 있음 — `.env.example` 에 `https://open-api.kos-solution.com`) | KOS 공개 API 호스트(KA§1.2) |
| `KOS_OPEN_API_KEY` | (비어 있음) | 운영 명동점 공개 API 키(§7.2) — 비면 503 `kos_not_configured` |
| `SALES_BACK_PORT` | `8800` | back 포트 |
| `SALES_FRONT_ORIGIN` | `http://localhost:3800` | CORS 허용 출처 |
| `SALES_CACHE_SEC` | `600` | 달별 캐시 유효(초 · §4.4) |
| `SALES_KOS_CONCURRENCY` | `8` | 수납별 일정 조회 동시 수(§4.4) |
| `NEXT_PUBLIC_API_BASE_URL` | — | front 전용 · `front/.env.local`(gitignore)에 `http://localhost:8800` |

- 포트 8800 · 3800 = cc-prototype procedure(8700 · 3700)와 같은 맥에서 겹치지 않게 · 기본값(OQ-111)
- back 은 `back/.env` 하나를 읽는다(실제 환경변수가 먼저 · 빈 값은 기본값 — cc-prototype procedure `config.py` 의 `env_ignore_empty` 방식)

### 10.2 실행

```bash
# back
cd back && uv sync
uv run uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8800
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
| OQ-102 | 환불 · 부분 환불 품목 금액(`cost.totalAmount` 「잔존 가치 또는 최종가」) | **원 가격으로 본다** — 444/444 일치의 정의(`REFUNDED` 품목을 빼야 결제 순액과 맞음 · §6.3). 부분 환불은 이 비교로 안 갈림 → WP-LIVE L10 실물 확인 | 기본값(근거 있음) · L10 확인 |
| ~~OQ-103~~ | ~~이름 · 방문일 원천~~ | **닫음(0.1.1)** — `findScheduleByPurchaseId` · 방문일 = `reservation.startDateTime` · 일정 없으면 `getVisitor`(R§2 원천 줄 10-29 정정) | 닫음 |
| ~~OQ-104~~ | ~~결제일 칸 원천~~ | **닫음(0.1.2)** — 결제일 = ⑤ `paymentDateTime.approvedDateTimeUtc` · 취소 줄 = `canceledDateTimeUtc` · 반환 줄 = `spentDateTimeUtc` · ① `lastUpdatedPaymentDateTimeUtc` 는 보이지 · 정렬하지 않음(R§2 ⑤ 줄 · §5.4) | 닫음 |
| OQ-105 | 조회를 요청마다 할지 저장해 둘지(DEC-001 열린 것) · 동시성 · 토큰 잠금 | back 메모리 캐시 600초 + `[다시 불러오기]` · 파일 · DB 0 · 수납별 조회 동시 8 · 토큰 다시 받기 한 번만 | 새로 · planner 기본값 |
| OQ-106 | 분할 결제가 달을 넘는 수납 · `⚠ 결제 ≠ 품목` 배지 | **분할 결제 정책 닫음(0.1.1)** — 품목 줄은 첫 승인 결제가 있는 달에만, 다른 달엔 결제 · 취소 줄만(R§2 분할 결제 줄 · §6.2). **배지 문구 · 조건은 WP-LIVE L5 · L10 결과로 정함**(그때까지 §6.4 조건 그대로) | 정책 닫음 · 배지 = WP-LIVE 뒤 |
| OQ-107 | 고를 수 있는 달의 앞쪽 끝 | 두지 않음(뒤쪽 끝 = 이번 달) | 새로 · planner 기본값 |
| OQ-108 | 화면 합계 · 금액 기준(총액 · 공급가) | 합계 없음(건수만) · 금액 = 총액(`totalAmount`) — 리포트 「정할 것 7」 | 새로 · 사용자(다음 판) |
| OQ-109 | 손님 유입이 조회 시점 값 — 지난 달을 다시 보면 바뀐 유입이 보일 수 있음 | 그대로(스냅샷 저장 안 함) · 정산 확정 절차가 생기면 그때 저장 | 새로 · 사용자(다음 판) |
| OQ-110 | 접근 — 로그인 없음 · 운영 고객 이름이 보이는 화면 | 로컬 `127.0.0.1` 만 · 로그인 없음 · 배포는 따로 정함(D1-09 · R§2 운영 키 줄 「로컬만」) | 새로 · 사용자 |
| OQ-111 | 실행 모양 · 포트 · health 경로 | compose 없이 uv · npm · 8800 · 3800 · `GET /api/health` | 새로 · planner 기본값 |
| OQ-112 | 다음 판 — 수수료율(상품별) · 에이전시별 보여 주기 · 「에이전시 코드」 판정 · 선불카드 충전/사용 중 어느 쪽을 셀지 · 엑셀 · 에이전시 확인 절차 | 이번 판 밖 | 열림 · 사용자(다음 판) |
| OQ-113 | 화면 세부 — 시안 없음(수납 id 끝 6자리 · 정렬 · 배지 색 · 1280px 기준 · 상태 화면 문구 · 「상태는 지금 기준」 안내) | cc-prototype procedure 디자인 기본값 · 실물 확인 때 고침 | 새로 · planner 기본값 |
| OQ-114 | 일부 실패 처리 — 「없음」 아닌 ③ · ④ 실패 하나가 달 전체를 오류로 | 달 전체 오류(일부 빠진 리스트를 보이지 않음). 대안 = 그 수납만 칸 비우고 `counts` 에 실패 수 | 새로 · planner 기본값 |
| OQ-115 | `REQUESTED` · `FAILED` 결제 행 | 줄 · 합에서 빼고 `ignoredTransactions` 로만 셈(운영 10월 0건) | 새로 · planner 기본값 |
| OQ-116 | 품목 통계 조회 범위 · ⑤ 묶음 크기 · ⑤ 에 없는 수납 | ② = 달 시작 −31일 ~ 달 끝 · 그래도 없으면 `itemsMissing` · ⑤ = 100개씩 · ⑤ 에 없으면 이 달 승인 행으로 봄(+ `firstApprovedUnknown` · 이 경우만 두 달 노출 가능) | 새로 · planner 기본값 |
| OQ-117 | 응답 브라우저 캐시 | `Cache-Control: no-store` | 새로 · planner 기본값 |
| OQ-118 | 통화가 섞인 수납 | 줄은 그대로 · 수납 합 `null` · `⚠ 통화 섞임`(운영 10월 전부 KRW) | 새로 · planner 기본값 |
| OQ-119 | 달 귀속(① `createdTimeUtc` 필터)과 보이는 결제일(⑤ 승인 · 취소 일시)이 다른 달일 때 | 묶음은 ① 이 정한 달에 둔다 · 결제일 칸엔 다른 달 날짜 그대로 · `counts.atOutsideMonth` · L12 로 실물 건수 확인. 대안 = 귀속도 ⑤ 시각으로(① 범위를 넓혀 불러야 함) | 새로 · 사용자 |
| OQ-120 | ① 행 ↔ ⑤ 거래 잇기(공통 id 없음) | 수납 · 상태 · 수단 · 금액 절댓값 · 통화로 잇고, 동점은 「마지막 결제 상태 변경 일시」 같음(파싱 · 초 단위)으로 가름(고르는 데만) · 못 이으면 `at null` · 「시각 없음」 · L12. 대안(L12 가 크면): 동점 가르기를 ⑤ `createdDateTimeUtc`(① 기간 필터와 같은 축)로 · 거래 id 가 있는 `getTransactionList`(31일 · `limit` 1000 · 허용 경로 하나 늘어 R§2 승인 필요) | 새로 · planner 기본값 |
| OQ-121 | 「첫 승인 결제」 고르기 세부(§6.2 s2 ~ s5) | 전액 취소(`canceledRefId` 합 ≥ 승인 금액)만 뺌 · 부분 취소는 남김 · 다 빠지면 원래 후보 · 승인 시각 없으면 수납 전체를 `createdDateTimeUtc` → `lastUpdatedDateTimeUtc` → `id` 로 · 잇기 실패면 ⑤ `createdDateTimeUtc` 달(추정 — ① 귀속과 같은 축) · 전부 `firstApprovedUnknown` · L11 | 새로 · planner 기본값 |

## 부록 A. DEC-001 · `_RESUME` §2 대응표

| 원천 | 절 |
|---|---|
| D-01 첫 화면 = 월별 매출 리스트 · 기본 이번 달 · 수수료 · 필터 · 엑셀 밖 | §1 · §3.1 · §4.1 · OQ-108 · OQ-112 |
| D-02 한 줄 = 품목 · 수납 묶음 · 품목 금액 · 결제 수단은 수납 참고 | §3.2 · §4.2 · §5.2 · §6.4 |
| D-03 칸(결제일 · 이름 · 방문일 · 최초 유입 · 수납 · 상품 · 옵션 · 품목 금액 · 상태) · 이름 안 가림 | §3.2 · §5.2 |
| D-04 에이전시 판정 = `visitorFunnelName` | §5.2 · §6.6 |
| D-05 운영 명동점 조회만 · `/queries/` · 원천 작업 | §5.1 · §7.1 · §7.2 |
| D-06 월 귀속 = 결제 시각(KST) · 취소는 취소된 달 음수 줄 | §6.1 · §6.2 · §6.3 |
| D-07 선불카드 · 기타 상품 안 뺌 · 품목 종류 칸 · 상품명 빈 품목 | §3.2 · §6.5 |
| D-08 별도 프로젝트 `agency-settlement`(레포 루트 `back/` · `front/`) · cc-prototype 디자인 복사 · import 금지 | §1.1 · §2 · §8 |
| D-09 로컬에서만 | §7.3 · §10 · OQ-110 |
| DEC-001 열린 것(조회 방식 · 이름 · 방문일 작업 · 월 경계 시간대) | OQ-105 · §5.1 ③(OQ-103 닫음) · §6.1 · OQ-101 |
| R§2 운영 키 줄(10-29 확장 — 이 프로젝트 코드 · WP-LIVE · 조회만 · 로컬만) | §7.2 · §7.3 · §9.2 |
| R§2 별도 프로젝트 줄(코드 레포 `kknaksss/agency-settlement` · 루트 `back/` · `front/` · 디자인만 cc-prototype 복사) | §1.1 · §2 · §7.2 · §8 · §10 |
| R§2 원천 줄(10-29 정정 — `findScheduleByPurchaseId` · 없으면 `getVisitor`) | §5.1 ③ ④ · §6.4 |
| R§2 분할 결제 줄(품목 줄은 첫 승인 결제가 있는 달에만) — 수정 4판: 「취소 안 된 첫 승인 결제 행이 ① 로 귀속된 달」 | §5.1 ⑤ · §6.2 · OQ-106 · OQ-121 · #17 · #22 ~ #24 · L11 |
| R§2 ⑤ 줄(⑤ 승인 · 결제일 = ⑤ `approvedDateTimeUtc` · 취소 = `canceledDateTimeUtc` · OQ-104 닫음) | §3.2 · §3.3 · §5.1 ⑤ · §5.2 · §5.4 · §6.1 · OQ-104 · OQ-119 · OQ-120 · #21 · L12 |
