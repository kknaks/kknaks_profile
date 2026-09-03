---
type: work
id: WORK-001
title: "데이터 기반 — 브론즈 적재부터 온톨로지까지 한 DB (게이트 1·2)"
status: todo
product: ontology-demo
work_type: new-feature
owner: kknaks
roles:
  pm: "kknaks"
  design: "—"
  fe: "—"
  be: "@ontology-be"
  qa: "coordinator"
  ops: "kknaks"
progress: 0
created_at: 2026-09-02
updated_at: 2026-09-02
tags:
  - product/ontology-demo
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-001-demo-agent-app|BASE-001]]"
  decisions:
    - "[[decision-001-db-medallion-all-layers|DEC-001]]"
    - "[[decision-002-pii-masking-boundary|DEC-002]]"
  specs:
    - "[[spec-001-data-layer-contract|SPEC-001]]"
  works: []
  releases: []
  related: []
---

# 데이터 기반 — 브론즈 적재부터 온톨로지까지 한 DB

SQLite 한 파일에 `bronze_*` → `silver_*` → `gold_*` → `ontology_*` 를 전부 세우고,
그 위에 마스킹 뷰를 얹는다. 기존 빌드 스크립트는 **입출력만 DB 로 갈아 끼우고 변환
규칙은 기록 04·05 그대로** 쓴다 — 이식이지 재설계가 아니다.
**비목표**: 조회 도구·API(WORK-002) · 에이전트(WORK-003) · 화면(WORK-004) · 업로드 UI.

## Meta

- Baseline: BASE-001
- Covers spec: SPEC-001 전체 (§4 4계층 + 마스킹 뷰 · §6 AC-1~AC-9)
- Depends on work: 없음 — 이 제품의 첫 실행 단위다
- Parallel work: 없음 (모든 후속 work 가 이 위에 선다)
- Follow-up work: WORK-002(도구·API)
- External dependency: 원천 데이터와 산출 DB 는 **레포 밖 로컬**이다 — 경로는
  `ONTOLOGY_DATA_DIR` env 로 주입한다(`app/ontology-agent/config.py` 의 `data_dir`).
  커밋 금지. 변환 규칙·게이트 기준의 SoT 는 기록 03·04·05 이며 **바꾸지 않는다.**

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | @ontology-be |
| Status | todo |
| Progress | 0% |
| Branch/PR | - |
| Blocker | - |
| Next | Phase 1 착수 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | todo |
| Design | — | 해당 없음 | todo |
| FE | — | 해당 없음 | todo |
| BE | @ontology-be | 스키마·적재기·빌드 이식·뷰 | todo |
| QA | coordinator | 게이트 1·2 재현 검증 | todo |
| Ops | kknaks | DB 파일 위치·env | todo |

## Scope

포함:

- DB 부트스트랩 — 경로 해석, 계층 접두어 규약, 읽기 전용 커넥션 헬퍼
- `bronze_*` 16테이블 스키마와 적재기 `load_bronze`(원형 보존) + **게이트 1**
- 마스킹 뷰 `v_bronze_*` · `v_silver_*` 와 표기 형식
- 실버 4종 + 부속 2종 빌드의 DB 이식(fail-fast 포함)
- 골드 빌드 이식 + **`gold_kpi_monthly` 신설**(빌드가 집계, 조회자는 집계하지 않는다)
- `ontology_nodes`·`ontology_edges` 적재 — 고아 0 · `node_id` 25종 1:1 대조
- **게이트 2(빌드 재현)** — 대조값 전항 일치

제외:

- 조회 도구·API·인증 → WORK-002 / 에이전트·채팅 → WORK-003 / 화면 → WORK-004
- 게이트 전건 재실행·PII 스캔·배포 → WORK-005
- 웹 raw 업로드·수집 자동화(DEC-001 Out — 파이프라인 단계)

## Code Surface

- Repo / module: `kknaks_profile` — `app/ontology-agent/`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `app/ontology-agent/config.py` | `data_dir`·`db_path` 사용(기존 스캐폴드 확장) |
| `app/ontology-agent/db/`(신설 후보) | 커넥션·스키마 부트스트랩·read-only 헬퍼·뷰 |
| `app/ontology-agent/build/` | `load_bronze` · 실버·골드·온톨로지 빌드 · 게이트 |
| `app/ontology-agent/tests/` | 적재·대사·마스킹·재현 테스트 |

- Domain / schema note: SQLite 신규 파일이다. **파괴적 마이그레이션이 없다** — 스키마
  변경은 재빌드로 처리한다. 컬럼 전문은 코드가 SoT 이고 spec 은 이름·enum 만 갖는다.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `bronze_*` (16) | 원천 3종의 원형 — 불변 |
| `silver_*` (6) | 표준화 — 기록 04 변환 규칙 |
| `gold_*` (5) | KPI — 일별·주별·**월별**·프로모션 캘린더·리텐션 |
| `ontology_*` (2) | nodes 25 · edges 27 — 판정·사유 보존 |
| `v_bronze_*` · `v_silver_*` | 소비자가 브론즈·실버에 닿는 **유일한 경로** |

- 상태 / invariant:
  - 브론즈는 **적재 이후 불변**. 어떤 빌드도 브론즈에 쓰지 않는다.
  - 상위 계층은 **바로 아래 계층만** 읽는다(골드가 브론즈를 직접 읽지 않는다).
  - `ontology_edges` 의 원인·결과는 `ontology_nodes` 에 존재한다(고아 0).
- Migration 필요 여부: 없음(신규 DB 파일). 재적재는 파일 재생성.
- SPEC 환류: 테이블 이름·enum·마스킹 표기·`node_id` 가 SPEC-001 §4 와 어긋나면 **임의
  변경 금지** — 코디네이터에 보고해 spec 을 먼저 고친다.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-002 도구·API | `v_bronze_*` · `v_silver_*` · `gold_*` · `ontology_*` | 원 테이블 직접 조회 경로를 열지 않는다 |
| WORK-003 에이전트 | 같은 뷰·View | 도구를 통해서만 닿는다 |
| WORK-005 통합 | 게이트 1·2 스크립트 | 전건 재실행이 이 구현을 그대로 부른다 |

## Internal Interface Contract

- 빌드 진입점은 CLI 다 — 단계별 실행(`bronze` / `silver` / `gold` / `ontology` / `all`)과
  게이트 단독 재실행을 지원한다. **WORK-005 의 전건 재실행이 이 인터페이스를 쓴다.**
- 게이트 실패는 **exit code ≠ 0** 이고, SPEC-001 §4 Case Matrix 의 코드
  (`BRONZE_ROWCOUNT_MISMATCH` · `ENUM_VIOLATION` · `NEGATIVE_AMOUNT` ·
  `CLOSED_LIST_VIOLATION` · `REBUILD_MISMATCH` · `ORPHAN_EDGE` · `PII_LEAK`)와
  기대·실측값을 로그로 남긴다.
- 읽기 전용 커넥션 헬퍼를 여기서 만들고 WORK-002 가 그대로 쓴다.

## Execution

### Phase 1 — DB 부트스트랩과 브론즈 스키마

- **Status**: TODO
- **설명**: 이후 모든 work 가 딛는 토대. 경로·접두어·커넥션 규약을 여기서 고정한다.
- **작업**:
  - [ ] DB 경로 해석(env 우선, 기본 `data_dir/db/ontology_demo.db`) · 디렉토리 생성
  - [ ] `bronze_*` 16테이블 스키마 — 이름은 SPEC-001 §4 표 그대로
  - [ ] 읽기 전용 커넥션 헬퍼(쓰기 시도가 실패하는 모드)
  - [ ] 빌드 CLI 골격(단계별 실행 + 게이트 단독 재실행)
- **검증**:
  - [ ] 빈 DB 부트스트랩 후 `bronze_*` 16개 생성
  - [ ] 읽기 전용 커넥션에서 INSERT 실패
- **완료 증거**: 미작성 — 테이블 16개 목록 출력 + read-only 쓰기 실패 로그 + CLI `--help`

### Phase 2 — `load_bronze` 적재와 **게이트 1**

- **Status**: TODO
- **설명**: 원형 보존이 이 제품의 근거 추적 전체를 떠받친다. 한 테이블이라도 어긋나면
  적재를 실패시키고 부분 적재를 남기지 않는다.
- **작업**:
  - [ ] vegas JSON 235개 → `bronze_vegas_reservations`(11필드 원형, 값 변환 없음)
  - [ ] 리뷰 CSV → `bronze_reviews` — **csv 파서로 읽는다**(셀 내 개행 때문에 라인 수로
        세면 안 된다)
  - [ ] nexus CSV 14개 → `bronze_nexus_*`
  - [ ] 게이트 1 — 원본 행수 = 테이블 행수 대사, 불일치 시 중단
- **검증**:
  - [ ] 결측일(2026-02-17) 행이 생기지 않는다
  - [ ] 파일 하나를 빼면 `BRONZE_ROWCOUNT_MISMATCH` 로 중단된다
- **완료 증거**: 미작성 — **게이트 1 통과**: vegas **78,216** · 리뷰 **1,962**(csv 파서
  기준) · nexus 14테이블(branches 3 · categories 157 · category_translations_ko 128 ·
  procedure_groups 2,154 · procedure_products_ko 2,996 ·
  procedure_group_product_mappings 5,632 · event_procedure_groups 1,769 ·
  event_procedure_products_ko 2,179 · event_procedure_group_product_mappings 3,199 ·
  procedure_packages_ko 323 · promotions_v1 24 · promotion_v2s 287 ·
  promotion_v2_event_group_mappings 858 · promotion_v2_group_mappings 0) —
  **전 테이블 오차 0** 대사표 첨부 (SPEC-001 AC-1)

### Phase 3 — 마스킹 뷰와 표기 형식

- **Status**: TODO
- **설명**: 사람과 에이전트가 같은 경계를 지나게 하는 자리. 여기서 새는 것이 곧 게이트 3
  위반이다.
- **작업**:
  - [ ] `v_bronze_vegas_reservations` — `patientName` `김○○`(성 1자) ·
        `phone` `010-****-1234` · `birthday` `1990-**-**`(연도만)
  - [ ] `v_bronze_reviews` — 본문 내 직원 실명 마스킹(기록 03·04 실명 사전) +
        `authorName`(원천 마스킹 닉네임 유지, 뷰 목록에 대상으로 명시)
  - [ ] `v_silver_reservations` · `v_silver_reviews` — 소비자 진입점 단일화용
  - [ ] 소비자용 접근 함수는 **뷰만** 연다(원 테이블 직접 조회 경로 없음)
- **검증**:
  - [ ] 뷰 산출에서 `patientName`·`phone`·`birthday` 원값 검색 0건
  - [ ] `chart_no` 는 마스킹하지 않고 그대로 나온다(기록 03 확정)
- **완료 증거**: 미작성 — 뷰 전건 스캔 원값 **0건**(SPEC-001 AC-7) + 마스킹 표기 샘플 행

### Phase 4 — 실버·골드 빌드 DB 이식 + 월 View

- **Status**: TODO
- **설명**: **이식이지 재설계가 아니다.** 입출력만 파일에서 DB 로 갈고 변환 규칙·게이트
  기준은 기록 04·05 그대로 쓴다.
- **작업**:
  - [ ] 실버 4종 + 부속 2종(`branch_alias`·`mappings`) 빌드 — 브론즈만 읽는다
  - [ ] fail-fast — `visit_status` enum 밖·금액/횟수 음수는 **경고가 아니라 빌드 중단**
  - [ ] 골드 빌드 이식(일별·주별·프로모션 캘린더·리텐션) + 파생(`_dod`·`_dod_pct`·
        `_ma7`·`_status`)
  - [ ] **`gold_kpi_monthly` 신설** — 일별에서 집계. 계수형은 월 합계, **비율형(객단가·
        취소율·노쇼율)은 월 합계에서 재계산**. 부분 월 플래그. 지표·계산식은 일별 것 그대로
- **검증**:
  - [ ] 오염 표본(enum 밖 값·음수) 주입 시 빌드가 실제로 중단(exit ≠ 0)
  - [ ] 전 일자에서 신환 + 재진 = 총 내원(235일 오차 0)
  - [ ] 주별·월별 합계 = 일별 합계(오차 0)
- **완료 증거**: 미작성 — 산출 행수(`silver_reservations` **75,479** ·
  `silver_reviews` **1,962** · `silver_catalog` **6,198** · `silver_promotions` **73** ·
  `silver_branch_alias` **11** · `silver_mappings` **9,689** · `gold_kpi_daily` **235**
  (2026-02-17 행 없음) · `gold_kpi_weekly` **34** · `gold_promo_calendar` **57**) +
  월 View·리텐션 **실측 행수**(SPEC-001 OQ-3 — 이 phase 에서 확정해 보고) +
  fail-fast 중단 로그 (SPEC-001 AC-3·AC-4·AC-5·AC-6b)

### Phase 5 — 온톨로지 적재와 **게이트 2**

- **Status**: TODO
- **설명**: 관계를 데이터 자산으로 세우고, DB 기반 재빌드가 기존 CSV 산출물과 같은지
  대조값으로 증명한다.
- **작업**:
  - [ ] `ontology_nodes` 25 · `ontology_edges` 27 적재 — 판정·사유·신뢰도·근거 보존
  - [ ] `node_id` **snake_case** 전건 + SPEC-001 §4 25종 표와 **1:1 대조** — 어긋나면
        적재 실패시키고 어긋난 id·라벨을 보고(표를 조용히 맞추지 않는다)
  - [ ] **`lag` 는 정본 문자열 원형 그대로 적재** — 형식을 강제하지 않는다(`2w`·빈 값 허용).
        `14d` 로 고쳐 넣지 않는다. 일 단위는 API·도구가 `lag_days` 로 병기한다(SPEC-002·003)
  - [ ] 고아 엣지 0 · `exogenous` 3종의 들어오는 엣지 0 · 기각·보류 행의 사유 필드 존재
  - [ ] 게이트 2 — DB 기반 재빌드 산출물 = 기존 CSV 산출물 대조
- **검증**:
  - [ ] 없는 노드를 가리키는 엣지를 주입하면 `ORPHAN_EDGE` 로 실패
  - [ ] 게이트 2 를 단독으로 재실행할 수 있다(WORK-005 가 쓴다)
- **완료 증거**: 미작성 — **게이트 2 통과**: 매출 합 **2,615,555,218원**(예외 1건 제외) ·
  결제 내원 **5,428** · 신환 **3,447** · 총 내원 **47,537**(실버 기준, 브론즈 47,602 와는
  「47,537 + 내원 중복 65 = 47,602」로 대사) · 일별 **235행** 전항 일치 +
  `ontology_nodes` 25 · `ontology_edges` 27 · **고아 0** · `node_id` 1:1 대조 결과
  (SPEC-001 AC-2·AC-6)

## Pre-deploy Check

- [ ] DB 파일·원천 데이터가 레포에 커밋되지 않았다(`.gitignore` 확인)
- [ ] 로그에 PII 원값이 남지 않는다(대사 로그는 행수·합계만)
- [ ] `.env` 신규 키는 예시 파일에만 둔다
- [ ] 소비자 표면(후속 work 가 쓸 접근 함수)에 원 테이블 경로가 없다

## Rollback

- 산출물은 DB 파일 하나다 — 지우고 다시 빌드하면 원복된다. **파괴적 마이그레이션이 없다.**
- 아직 서비스 표면이 없어 외부 영향 범위도 없다.

## Done Criteria

- [ ] 모든 Phase 가 `DONE`
- [ ] SPEC-001 AC-1~AC-9(+AC-6b) 가 게이트 수치로 커버됐다
- [ ] SPEC-001 OQ-3(월 View·리텐션 행수)이 실측값으로 확정돼 보고에 있다
- [ ] product `log.md` · `30-work/README.md` 갱신(코디네이터)

## Open Issues

- 브론즈 nexus 원형의 컬럼 타입을 전부 TEXT 로 둘지 원천 타입을 살릴지는 코드 조사 후
  워커가 정하고 근거를 보고에 남긴다 — **행수 대사에 영향을 주지 않는 범위**여야 한다.
- `node_id` 25종 중 SPEC-001 §4 의 ※ 6행(정본 대조 필요)이 `ontology_nodes` 와 어긋나면
  **spec 개정 사안**이다 — 워커가 고치지 말고 보고한다(SPEC-001 OQ-6).

## Related

- SPEC: frontmatter `links.specs` · Work: 후속 WORK-002
