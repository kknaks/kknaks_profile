# 원천 인벤토리 — 병원 매출 온톨로지 (1단계 산출물)

> 상위 계획: [[hospital-revenue-ontology-plan]] · 탐색일 2026-08-30 · NEXUS 레포 prod 브랜치 정적 분석

## 0. 원천 시스템의 배치

| 시스템 | 담당 | 상태 |
| --- | --- | --- |
| **NEXUS** | 수요 측 — 고객 등록 · 예약 · 상품 · 프로모션 | 아래 정리 완료 |
| **외부 EMR** (Vegas · Motion E차트) | 매출 측 — 내원 · 시술 · 수납 | **대기** — 매출 일지 입수 후 |
| prod DB 실측 | 데이터 기간 · 건수 · 단위 | **대기** — 내일 입력 |

NEXUS 는 홈페이지 + 예약 CMS 다. 결제·수납·환불 테이블이 없고, 예약 확정 시 외부
EMR 로 전송만 한다. 따라서 사슬에서 NEXUS 가 커버하는 구간은 다음과 같다.

```text
고객 등록 → (장바구니) → 예약 신청 → 확정 · 완료 · 노쇼 │ 내원 → 시술 → 수납
└────────────────── NEXUS ──────────────────┘ └─── 외부 EMR (대기) ───┘
                          조인 키 후보: 전화번호 · 예약코드
```

스택: FastAPI · Tortoise ORM · PostgreSQL 16. 브랜드 3개가 지점별 독립 DB.
전 업무 테이블에 `branch_id` 스코프. 총 89 테이블 중 맵과 관련 있는 것만 아래에 남긴다.

## 1. 핵심 트랜잭션 — 시계열이 나오는 곳

### reservations

| 컬럼 | 내용 |
| --- | --- |
| reservation_code | UNIQUE, `{지점코드}-YYYYMMDD-{seq}` |
| customer_id | FK → customers |
| **status** | pending / staff_check / confirmed / completed / cancelled / **no_show** / duplicated / away |
| **reserved_date** | DATE — 예약된 날 |
| reserved_time | TIMETZ — 날짜와 분리된 컬럼. 결합해서 써야 함 |
| total_amount | INT — **예약 시점 견적. 실수납액 아님** |
| device | web / mobile / app |
| created_at | 신청 시각 (TIMESTAMPTZ) |

→ KPI: 예약 건수 · 노쇼율 · 취소율 · 예약 리드타임(created_at → reserved_date) · 견적액 합계

### reservation_items

| 컬럼 | 내용 |
| --- | --- |
| reservation_id | FK CASCADE |
| product_type | **procedure / event** — 일반 시술인지 이벤트 상품인지 |
| product_id | INT — FK 아님, 예약 시점 스냅샷 |
| product_name · quantity | |
| unit_price · discount_rate · total_price | 예약 시점 고정. 이후 갱신 경로 없음 |

→ KPI: 상품별 예약 수요 · 예약 객단가(견적) · 할인율 분포 · 이벤트/일반 비중

### customers

| 컬럼 | 내용 |
| --- | --- |
| customer_type | guest / member |
| birth_date · gender · is_foreigner · preferred_language | 인구통계 |
| phone | EMR 측과 조인 키 후보 |
| marketing_consent | |
| created_at | 등록일 |

→ KPI: 신규 고객 수 · 속성별 분포. **신환/재진 구분 컬럼 없음** — 고객별 예약 순번으로 파생.

### cart_items

customer_id 또는 session_id · 상품 참조 · created_at.
→ 장바구니 → 예약 전환의 앞단 보조 지표.

## 2. 상품 · 가격 마스터

| 테이블 | 핵심 컬럼 | 비고 |
| --- | --- | --- |
| procedure_products | 상품코드 · **정가 · 할인가 · 할인율** · 소요시간 · 노출 여부 | **language 별 독립 행** — 집계 시 `language='ko'` 필터 필수 |
| event_procedure_products | 위와 동일 구조 | 이벤트 상품 |
| procedure_packages · categories(2단계) · 그룹/매핑 | 분류 체계 | KPI 를 카테고리 단위로 묶는 축 |
| non_covered_fee_items | 비급여 고지 수가표 | 법정 게시용. 판매 상품과 FK 없음 — 참고만 |

## 3. 프로모션 — 개입 변수

| 테이블 | 핵심 컬럼 |
| --- | --- |
| promotions / **promotion_v2s** | **promotion_started_at / ended_at** (TIMESTAMPTZ) + 노출 기간 별도 |
| promotion_group_mappings · promotion_event_group_mappings | 어느 상품 그룹에 걸렸나 |

마케팅비·유입채널 데이터가 없는 이 데이터셋에서 **유일하게 시각이 정확한 개입 변수**다.
계절(외생)과 달리 병원이 조작 가능 — Meta 의 `조작 가능` 노드.

- 엣지 후보: `프로모션 진행중 ─(+)→ 해당 상품군 예약 수` · `프로모션 진행중 ─(−)→ 예약 객단가`
- 시차 상관의 첫 검증 대상: 프로모션 시작 후 N일 예약 반응
- ⚠️ v1 → v2 이관 이력 있음. 분석 시점의 정본이 어느 쪽인지 확인 필요

## 4. 캘린더 · 공급 능력

| 테이블 | 핵심 컬럼 | 쓰임 |
| --- | --- | --- |
| reservation_restrictions | **target_date** · restriction_type(HOLIDAY/…) · 영업 여부 | 계절·연휴 외생 노드의 재료 |
| reservation_configs · time_slots · disabled_slot_configs | 슬롯 간격 · 요일별 최대 수용량 | **공급 능력** — 가동률 = 예약 수 ÷ 수용량 |

## 5. 구조 축

- `branches` · `brands` · `branch_groups` — 전 테이블에 branch_id. **Node 인스턴스
  레벨은 「지점 × 시술(카테고리)」이 데이터가 지탱하는 자연 단위**다.
- `medical_staffs` — 마스터는 있으나 **예약과 FK 연결이 없다.** 의사·상담사 단위
  분석 축은 이 데이터로 불가.

## 6. 제약 — 분석 설계가 피해 갈 수 없는 것

1. **상태 전이 시각이 없다.** confirmed_at / completed_at 부재. status 덮어쓰기 +
   updated_at 뿐이고 정책상 모든 상태 간 전환이 허용돼 이력이 소실된다.
   → 「신청 → 확정」 리드타임 불가. 시간축은 created_at(신청)과 reserved_date(예약일)만 신뢰.
2. **total_amount 는 견적이다.** 매출로 쓰면 틀린다. 실매출은 EMR 측 대기.
3. **유입채널이 없다.** UTM · referrer 추적 전무. device(web/mobile/app)가 유일한 근사.
4. **신환/재진 구분이 없다.** 고객별 예약 순번으로 파생해야 한다.
5. 다국어 테이블은 언어별 독립 행 — ko 필터 누락 시 이중 집계.

## 7. 대기 중 — 내일 입력

- [ ] prod DB 실측 — 데이터 기간 · 건수 규모 · 지점 수 (4단계 EDA 성립 조건 판정)
- [ ] **매출 일지** — 형태(엑셀? EMR 추출?) · 단위(일별? 건별?) · 기간 · NEXUS 와 조인 가능 여부
- [ ] promotion v1/v2 정본 확인
