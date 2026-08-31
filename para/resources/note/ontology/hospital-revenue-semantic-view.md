# 시멘틱 뷰 정의서 — 병원 매출 온톨로지 (실버·골드의 SoT)

> 상위: [[hospital-revenue-ontology-plan]] · 용어: [[hospital-revenue-glossary]] ·
> 원천: [[hospital-revenue-source-inventory]] · 2026-08-31

**이 문서가 실버·골드의 단일 원천이다.** 코드는 이 명세를 구현한 것이어야 하고, 여기 없는
변환·필터·파생을 코드가 임의로 하지 않는다. 명세를 바꿀 일이 생기면 **문서를 먼저 고치고**
재추출한다. **재추출은 매번 사용자 승인 후에만 실행한다.**

## 0. 1차 산출물 폐기 기록 (2026-08-31)

1차 실버·골드(visits · reviews · daily_kpi · promo_calendar)를 전량 폐기했다. 원인 셋 —
각 명세 항목에 재발 방지 규칙으로 반영되어 있다.

| # | 무엇이 잘못됐나 | 어디에 반영했나 |
| --- | --- | --- |
| 1 | 중복 제거 키에 `staff` 를 빼고 만들어, 같은 날 같은 환자의 복수 예약(다른 시술)이 오삭제됐을 수 있다. 제거된 3,493행을 검증하지 않고 사용했다 | §1 중복 처리 |
| 2 | 리뷰 감성·시술 태그를 명세(LLM 추출) 대신 키워드 규칙으로 때웠다 — 시술 사전에 「추가·관리·가능」 같은 일반 단어가 절반이었다 | §2 |
| 3 | 프로모션 변수를 명세 없이 「일별 활성 개수」로 즉흥 산출했다 — 상시 프로모션이 누적되는 우상향 추세일 뿐 개입 신호가 아니었고, 이것으로 가짜 상관(-0.71)을 보고했다 | §4 |
| 공통 | **검증 게이트 없이 다음 층(EDA)으로 넘어갔다** | §6 |

## 1. silver.visits — 예약·내원 행

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

**중복 처리** — ⚠️ 1차 폐기 원인 1.

- 제거 대상: **모든 필드가 완전히 동일한 행**만 (date · phone · chart_no · staff · status ·
  visit_count · sales · receipt 전부 일치).
- 같은 날 같은 환자의 행이 staff 나 금액이 다르면 **별개 예약 건으로 유지한다**
  (용어 정의 「예약 건 = 행 하나」).
- 제거 건수와 무작위 표본 20건을 빌드 로그로 남기고, **사람 확인 후에만 다음 층으로**.

**파생 컬럼** (정의는 [[hospital-revenue-glossary]] §2·§3)

| 컬럼 | 식 |
| --- | --- |
| is_visit | status = 내원 |
| is_new | is_visit AND visit_count = 1 |
| is_return | is_visit AND visit_count ≥ 2 |
| is_new_lost | NOT is_visit AND visit_count = 0 |
| is_paying | is_visit AND sales > 0 |

## 2. silver.reviews — 리뷰 행

**소스** `세라미크의원_강남_STG_리뷰_2026-08-31.csv` (1,962건 · `utf-8-sig` · 파일명 NFC 주의)

**컬럼 매핑** — date(리뷰일→YYYYMMDD) · platform(naver | gangnam) · rating(강남언니만) ·
replied(답변상태) · text(리뷰내용 — PII 주의: 반출 금지, 추출 결과만 하위 층으로).

**감성 (sentiment)** — ⚠️ 1차 폐기 원인 2. **키워드 규칙 금지.**

- 강남언니: 평점으로 결정 — ≥4 pos · ≤2.5 neg · 그 외 neu. LLM 을 쓰지 않는다.
- 네이버(평점 없음): **LLM 이 리뷰 전문을 읽고 판정** (pos/neu/neg). S-002 방식 —
  AI 추출 → 규칙 검증(값 범위·건수 대사) → 확신 낮은 건만 사람 검토. 수정 이력 보존.

**시술 태그 (procedures)** — ⚠️ 같은 원인. **일반 단어 사전 금지.**

- 태그는 **폐쇄 목록**에서만 고른다. 목록은 이벤트 그룹명·상품명에서 사람이 승인한
  시술·장비명만으로 만든다 (예: 제모 · 레이저토닝 · 아발란체 · 젠틀맥스 · 보톡스 ·
  필러 · 리프팅 · 스킨부스터 …). 「추가·관리·여름·가능」류 일반 단어는 목록에 넣지 않는다.
- LLM 이 리뷰 전문을 읽고 목록 안에서 태깅. 목록에 없는 시술이 반복 등장하면
  목록 추가를 **제안만** 하고 사람이 승인한다.

## 3. gold.daily_kpi — 일별 KPI

소스 silver.visits. 날짜별 집계. 식은 전부 [[hospital-revenue-glossary]] 를 따른다.

| 컬럼 | 식 |
| --- | --- |
| visits · new_patients · returns · new_lost · no_show · cancel · paying_visits | 해당 파생/status 카운트 |
| sales · receipt | **is_visit 행만** 합산 |
| no_show_rate | no_show ÷ (visits + no_show) — 취소 제외 |
| cancel_rate | cancel ÷ (visits + no_show + cancel) |
| avg_ticket | sales ÷ paying_visits (paying_visits = 0 이면 공란) |

결측일(설날 2026-02-17)은 행을 만들지 않는다 — 0 으로 채우지 않는다.

## 4. gold.promo_starts — 프로모션 개입 이벤트

⚠️ 1차 폐기 원인 3. **「일별 활성 개수」를 쓰지 않는다** — 상시 프로모션 누적으로
추세만 남는 변수다.

- 단위: **시작 이벤트** — `promotion_started_at` 이 그 날짜인 프로모션 수.
- 정본: v2 (`promotion_v2s`). 2026-01~06 구간은 v1 도 포함하되 출처 컬럼으로 분리.
- 제외: `deleted_at` 이 있는 행.
- 미결: v2 의 노출 플래그(`is_displayed` 등)를 시작 판정에 쓸지 — **재추출 승인 전에
  사람이 정한다.**
- 확장(선택): `promotion_v2_event_group_mappings` → 이벤트 그룹 → 상품 연결로
  프로모션을 시술군 단위로 태깅할 수 있다. 매핑 CSV 는 반입 완료 상태.

## 5. gold.daily_reviews — 일별 리뷰

소스 silver.reviews. 날짜 × 플랫폼 카운트 · 강남언니 평점 평균 · 부정 리뷰 수.
플랫폼을 합산한 단일 컬럼은 만들지 않는다 (네이버 = 개입 변수, 강남언니 = 유기 신호).

## 6. 검증 게이트 — 이걸 통과해야 다음 층으로 간다

빌드는 **한 층씩** 진행하고, 각 층은 아래를 통과한 뒤 **사용자 승인을 받아야** 다음
층(궁극적으로 EDA)으로 넘어간다. 1차 폐기의 공통 원인이 이 게이트 부재였다.

| 층 | 검사 |
| --- | --- |
| silver.visits | ① 행수 대사: 브론즈 행수 = 실버 + 필터 제외 + 중복 제거 (수식이 맞아야 함) ② 중복 제거 표본 20건 육안 ③ 무작위 3일 원본 JSON 과 행 단위 대조 ④ enum·음수 검사 통과 |
| silver.reviews | ① 1,962건 전건 태깅 완료(누락 0) ② 감성 표본 30건 재검(사람) ③ 태그가 폐쇄 목록 밖 값 0건 |
| gold.* | ① 일별 합 = 실버 재집계와 일치 ② 알려진 값 대조(예: 8개월 매출 합, 월별 표) ③ 결측일 행 없음 확인 |

## 7. 빌드 순서

```text
[승인] → silver.visits → 게이트 → [승인] → silver.reviews → 게이트 → [승인]
      → gold.* → 게이트 → [승인] → 4단계 EDA (여기서부터가 분석)
```
