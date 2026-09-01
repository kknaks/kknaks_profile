# 시멘틱 뷰 정의서 — 병원 매출 온톨로지 (실버·골드의 SoT)

> 상위: [[hospital-revenue-ontology-plan]] · 용어: [[hospital-revenue-glossary]] ·
> 원천: [[hospital-revenue-source-inventory]] · 2026-08-31

**이 문서가 실버·골드의 단일 원천이다.** 코드는 이 명세를 구현한 것이어야 하고, 여기 없는
변환·필터·파생을 코드가 임의로 하지 않는다. 명세를 바꿀 일이 생기면 **문서를 먼저 고치고**
재추출한다.

**진행 규칙** — 아래 STEP 을 번호 순서대로 진행한다. 각 STEP 은
`빌드 → 게이트(검증) → 사용자 승인` 을 통과해야 다음 STEP 으로 간다.
**STEP 의 시작(빌드 실행) 자체도 사용자 승인 후에만 한다.**

```text
STEP 0 (완료) → STEP 1 → STEP 2 → STEP 3 → STEP 4 → STEP 5 (EDA 진입)
                └─ 각 STEP: 빌드 → 게이트 → 승인 ─┘
```

---

## STEP 0. 1차 산출물 폐기 (2026-08-31 · 완료)

1차 실버·골드(visits · reviews · daily_kpi · promo_calendar)를 전량 폐기했다. 원인 셋 —
각 STEP 의 명세에 재발 방지 규칙으로 반영되어 있다.

| # | 무엇이 잘못됐나 | 반영 위치 |
| --- | --- | --- |
| 1 | 중복 제거 키에 `staff` 를 빼고 만들어, 같은 날 같은 환자의 복수 예약(다른 시술)이 오삭제됐을 수 있다. 제거된 3,493행을 검증하지 않고 사용했다 | STEP 1 |
| 2 | 리뷰 감성·시술 태그를 명세(LLM 추출) 대신 키워드 규칙으로 때웠다 — 시술 사전에 「추가·관리·가능」 같은 일반 단어가 절반이었다 | STEP 2 |
| 3 | 프로모션 변수를 명세 없이 「일별 활성 개수」로 즉흥 산출했다 — 상시 프로모션이 누적되는 우상향 추세일 뿐 개입 신호가 아니었고, 이것으로 가짜 상관(-0.71)을 보고했다 | STEP 3 |
| 공통 | **검증 게이트 없이 다음 층(EDA)으로 넘어갔다** | 전 STEP 의 게이트 |

---

## STEP 1. silver.visits — 예약·내원 행

### 1-1. 명세

**소스** `bronze/vegas/2026*.json` (235개 · 형태 A 최상위 배열 · 인코딩 `utf-8-sig`)

**필터** `NFC(branch) = '세라미크의원 강남'` 인 행만.

**컬럼 매핑**

| 출력 컬럼 | 소스 | 변환 |
| --- | --- | --- |
| date | resvDate | `YYYYMMDD` 8자리 그대로 |
| phone · chart_no | phone · chartNo | 원문 유지 (PII — reference/ 밖 반출 금지) |
| staff | staff | 빈 값 → `미지정` |
| status | visitStatus | 내원 · 취소 · 부도 세 값 외 등장 시 **빌드 중단하고 보고** |
| visit_count | visitCount | int. 음수 등장 시 빌드 중단 |
| sales · receipt | sales · receipt | int. 음수 등장 시 빌드 중단(환불은 덮어쓰기 방식이므로 음수가 없어야 정상) |

**중복 처리** — ⚠️ STEP 0 원인 1.

- 제거 대상: **모든 필드가 완전히 동일한 행**만 (date · phone · chart_no · staff · status ·
  visit_count · sales · receipt 전부 일치).
- 같은 날 같은 환자의 행이 staff 나 금액이 다르면 **별개 예약 건으로 유지한다**
  (용어 정의 「예약 건 = 행 하나」).
- 제거 건수와 무작위 표본 20건을 빌드 로그로 남긴다.

**파생 컬럼** (정의는 [[hospital-revenue-glossary]] §2·§3)

| 컬럼 | 식 |
| --- | --- |
| is_visit | status = 내원 |
| is_new | is_visit AND visit_count = 1 |
| is_return | is_visit AND visit_count ≥ 2 |
| is_new_lost | NOT is_visit AND visit_count = 0 |
| is_paying | is_visit AND sales > 0 |

### 1-2. 게이트

- [ ] 행수 대사: 브론즈 행수 = 실버 + 필터 제외 + 중복 제거 (수식이 정확히 맞아야 함)
- [ ] 중복 제거 표본 20건 육안 확인
- [ ] 무작위 3일을 원본 JSON 과 행 단위 대조
- [ ] enum · 음수 검사 통과 (걸리면 빌드 중단 상태여야 함)

### 1-3. 승인 → STEP 2 로

---

## STEP 2. silver.reviews — 리뷰 행

### 2-0. 선행 결정 (빌드 전에 사람이 정한다)

- [ ] **시술 태그 폐쇄 목록 승인** — 이벤트 그룹명·상품명에서 시술·장비명만 추린 목록.
  「추가·관리·여름·가능」류 일반 단어 금지.

### 2-1. 명세

**소스** `세라미크의원_강남_STG_리뷰_2026-08-31.csv` (1,962건 · `utf-8-sig` · 파일명 NFC 주의)

**컬럼 매핑** — date(리뷰일→YYYYMMDD) · platform(naver | gangnam) · rating(강남언니만) ·
replied(답변상태) · text(리뷰내용 — PII 주의: 반출 금지, 추출 결과만 하위 층으로).

**감성 (sentiment)** — ⚠️ STEP 0 원인 2. **키워드 규칙 금지.**

- 강남언니: 평점으로 결정 — ≥4 pos · ≤2.5 neg · 그 외 neu. LLM 을 쓰지 않는다.
- 네이버(평점 없음): **LLM 이 리뷰 전문을 읽고 판정** (pos/neu/neg). S-002 방식 —
  AI 추출 → 규칙 검증(값 범위·건수 대사) → 확신 낮은 건만 사람 검토. 수정 이력 보존.

**시술 태그 (procedures)** — ⚠️ 같은 원인.

- LLM 이 리뷰 전문을 읽고 **2-0 에서 승인된 폐쇄 목록 안에서만** 태깅.
- 목록에 없는 시술이 반복 등장하면 목록 추가를 **제안만** 하고 사람이 승인한다.

### 2-2. 게이트

- [ ] 1,962건 전건 처리 완료 (누락 0)
- [ ] 감성 표본 30건 사람 재검
- [ ] 태그가 폐쇄 목록 밖 값 0건

### 2-3. 승인 → STEP 3 으로

---

## STEP 3. gold — 일별 뷰 3종

### 3-0. 선행 결정 (빌드 전에 사람이 정한다)

- [ ] 프로모션 시작 판정에 **노출 플래그**(`is_displayed` · display 기간)를 쓸지.

### 3-1. gold.daily_kpi 명세

소스 silver.visits. 날짜별 집계. 식은 전부 [[hospital-revenue-glossary]] 를 따른다.

| 컬럼 | 식 |
| --- | --- |
| visits · new_patients · returns · new_lost · no_show · cancel · paying_visits | 해당 파생/status 카운트 |
| sales · receipt | **is_visit 행만** 합산 |
| no_show_rate | no_show ÷ (visits + no_show) — 취소 제외 |
| cancel_rate | cancel ÷ (visits + no_show + cancel) |
| avg_ticket | sales ÷ paying_visits (paying_visits = 0 이면 공란) |

결측일(설날 2026-02-17)은 행을 만들지 않는다 — 0 으로 채우지 않는다.

### 3-2. gold.promo_starts 명세

⚠️ STEP 0 원인 3. **「일별 활성 개수」를 쓰지 않는다.**

- 단위: **시작 이벤트** — `promotion_started_at` 이 그 날짜인 프로모션 수.
- 정본: v2 (`promotion_v2s`). 2026-01~06 구간은 v1 도 포함하되 출처 컬럼으로 분리.
- 제외: `deleted_at` 이 있는 행.
- 확장(선택): `promotion_v2_event_group_mappings` → 이벤트 그룹 → 상품 연결로
  프로모션을 시술군 단위로 태깅할 수 있다. 매핑 CSV 는 반입 완료 상태.

### 3-3. gold.daily_reviews 명세

소스 silver.reviews. 날짜 × 플랫폼 카운트 · 강남언니 평점 평균 · 부정 리뷰 수.
플랫폼을 합산한 단일 컬럼은 만들지 않는다 (네이버 = 개입 변수, 강남언니 = 유기 신호).

### 3-4. 게이트

- [ ] 일별 합 = 실버 재집계와 일치
- [ ] 알려진 값 대조 (예: 8개월 매출 합 · 월별 표)
- [ ] 결측일 행 없음 확인
- [ ] promo_starts 가 추세성 누적이 아님을 육안 확인 (주별 값이 이벤트성으로 튀는가)

### 3-5. 승인 → STEP 4 로

---

## STEP 4. EDA 진입 — 여기서부터가 분석

STEP 1~3 이 전부 게이트·승인을 통과했을 때만 시작한다. 방법은 계획 문서 4단계
(요일·계절 통제 · 시차 상관 · 추세 제거)를 따르고, 산출물은 엣지 후보 표
(`쌍 · 부호 · 시차 · 근거 수치 · 판정 칸`) — **판정 칸은 사람이 채운다.**

## STEP 5. 이후 — Meta 확정 (계획 문서 5단계)
