# Work Index

규칙: `para/projects/project.md`

> 현재 구현, QA, 릴리즈 상태를 추적하는 map이다. 상세 work 실행 본문은 `30-work/` 아래 1 파일 = 1 work로 둔다.
> `Status Board`는 실행 상태의 owning view다. Spec Coverage는 work frontmatter `links.specs`를 spec 중심으로 펼친 derived view다.

최종 수정: 2026-09-02

Status 값: `todo`, `in_progress`, `blocked`, `review`, `done`

**phase 가 태스크 단위다.** WP 5건이고 각 WP 안의 phase(3~5개)로 발주·재개·검증이 돈다 —
Status Board 의 Next 열이 그 다음 phase 를 가리킨다.

## Domain / Schema 관리 원칙

- Work는 구현 중 필요한 DDD 초안과 schema 가정을 적는 자리다.
- 실제 table schema, column, index, FK, migration 전문은 제품 코드/migration이 source of truth다.
- `30-work/`에는 aggregate boundary, 상태/invariant, migration 필요 여부, 코드 위치 후보만 적는다.
- 같은 invariant가 여러 work에 반복되거나 onboarding용 도메인 지도가 필요해지면 optional architecture 문서로 승격한다.
- SPEC에는 사용자/프론트/QA/외부 연동에 드러나는 resource, status, enum, API 계약만 환류한다.
- **이 제품은 파괴적 마이그레이션이 없다** — DB 산출물은 재빌드로 복원한다(DEC-001).

## Status Board

| Phase | Work | Scope | Status | Owner | 예상 기간 | 목표 완료 | PR/Branch | Blocker | Next |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [WORK-001 데이터 기반](work-001-data-foundation.md) | SPEC-001 | todo | @ontology-be | TBD | TBD | - | - | P1 DB 부트스트랩·브론즈 스키마 |
| 2 | [WORK-002 도구와 API](work-002-tools-and-api.md) | SPEC-002 · SPEC-003(채팅 제외) | todo | @ontology-be | TBD | TBD | - | WORK-001 | P1 FastMCP 골격·검증 계층 |
| 3 | [WORK-003 에이전트·채팅](work-003-agent-loop-and-chat.md) | SPEC-005 · SPEC-003(채팅) | todo | @ontology-be | TBD | TBD | - | WORK-002 | P1 제출부·codex 워커 |
| 2~4 | [WORK-004 프론트 3페이지](work-004-frontend-three-screens.md) | SPEC-004 | todo | @ontology-fe | TBD | TBD | - | P1~P3←002 · P4←003 (mock 선행 가능) | P1 셸·토큰 레이어·게이트 화면 |
| 5 | [WORK-005 통합·배포](work-005-integration-and-deploy.md) | 전 spec 재실행 · DEC-005 | todo | @ontology-be + @ontology-fe | TBD | TBD | - | WORK-003 · WORK-004 | P1 게이트 전건 재실행·PII 스캔 |

**병렬 축** — WORK-004 는 BE 와 병렬로 돈다. 계약(SPEC-003·004·005)이 고정돼 있어 FE 가
mock 으로 선행하고 API 가 붙으면 교체한다. P4(채팅)만 WORK-003 완주에 걸린다.

## Work List

work 문서를 만들거나 상태, owner, branch, 다음 작업이 바뀌면 이 표를 갱신한다.

| ID | Title | Type | Owner | Status | Progress | Phase 수 | File | Covers Spec |
|---|---|---|---|---|---|---|---|---|
| WORK-001 | 데이터 기반 — 브론즈~온톨로지 한 DB | new-feature | @ontology-be | todo | 0% | 5 | [work-001-data-foundation.md](work-001-data-foundation.md) | SPEC-001 |
| WORK-002 | 조회 도구 4종과 API 서버 | new-feature | @ontology-be | todo | 0% | 5 | [work-002-tools-and-api.md](work-002-tools-and-api.md) | SPEC-002 · SPEC-003 |
| WORK-003 | 에이전트 루프와 채팅 | new-feature | @ontology-be | todo | 0% | 4 | [work-003-agent-loop-and-chat.md](work-003-agent-loop-and-chat.md) | SPEC-005 · SPEC-003 |
| WORK-004 | 프론트 3페이지 | new-feature | @ontology-fe | todo | 0% | 4 | [work-004-frontend-three-screens.md](work-004-frontend-three-screens.md) | SPEC-004 |
| WORK-005 | 통합 검증과 배포 | **release** | @ontology-be + @ontology-fe | todo | 0% | 4 | [work-005-integration-and-deploy.md](work-005-integration-and-deploy.md) | SPEC-001~005 (재실행) |

## Spec Coverage

각 spec이 어느 work에서 구현되며 현재 진척이 어떤지 한눈에 보는 spec-centric view다.
Covering Work의 Status를 종합한 derived view다 — 원본은 각 work 의 `links.specs` 다.

| Spec | Status | Covering Work | 구현 상태 |
|---|---|---|---|
| SPEC-001 데이터 계층 | ready | WORK-001 (전부) · WORK-005 (재실행) | todo |
| SPEC-002 조회 도구 4종 | ready | WORK-002 (전부) · WORK-005 (재실행) | todo |
| SPEC-003 FE↔BE API | ready | WORK-002 (채팅 제외) · WORK-003 (채팅 절) · WORK-004 (소비) | todo |
| SPEC-004 화면 3페이지 | draft | WORK-004 (전부) | todo |
| SPEC-005 에이전트·게이트 | ready | WORK-003 (전부) · WORK-005 (게이트 재실행) | todo |

**커버리지 공백 없음** — spec 5건이 전부 최소 1개 WP 에 물려 있다.
다만 SPEC-004 는 `draft` 이고 §7.2 「디자인 조정 대기」 20건이 미해소라, WORK-004 착수
시점에 그 목록이 먼저 정리돼야 한다.

## 게이트 배치

SPEC-005 의 게이트 5종이 어느 WP 의 완료 증거인지.

| 게이트 | 기준 | 완료 증거를 내는 WP |
|---|---|---|
| 1 브론즈 대사 | 원본 행수 = 테이블 행수, 전 테이블 오차 0 | **WORK-001 P2** |
| 2 빌드 재현 | 대조값 전항 일치(매출 2,615,555,218 · 결제 내원 5,428 · 신환 3,447 · 내원 47,537 · 일별 235) | **WORK-001 P5** |
| 3 PII 마스킹 | 화면·에이전트 응답 원값 노출 0건 | **WORK-005 P1** (뷰 구현은 WORK-001 P3) |
| 4 회귀 3본 | R-1 현황 · R-2 전제 교정 · R-3 드릴다운 | **WORK-003 P4** |
| 5 근거 무결성 | 수치 재조회 일치 · `used_edges` ⊆ 확정 · 하이라이트 = `used_edges` | **WORK-003 P4** (③ 화면 대조는 WORK-005 P1) |

전건 재실행은 **WORK-005 P1** 이 한다.

## Release Gate

### Scope

- [ ] 릴리즈 대상 spec이 정해졌다 — SPEC-001~005
- [ ] 포함/제외 범위가 decision/spec과 맞다 — 외부 공개·rate limit·수집 자동화 제외(DEC-005)

### Code

- [ ] 연결된 제품 PR이 merge됐다
- [ ] 필요한 env(`ONTOLOGY_DATA_DIR` · `ONTOLOGY_DEMO_PASSWORD` · API base URL)가 반영됐다
- [ ] 파괴적 migration 없음 — DB 는 재빌드로 복원 가능

### Spec

- [ ] `20-spec/` 변경이 리뷰됐다
- [ ] blocker open question이 없다 — **현재 SPEC-004 `draft` + 디자인 조정 20건이 미해소**

### Baseline / UX

- [ ] BASE-001 이 연결됐다
- [ ] Known UX issue(디자인 조정 대기 20건)를 owner 가 승인했다

### QA

- [ ] 게이트 1~5 전건 재실행 통과
- [ ] PII 원값 노출 0건 스캔 통과
- [ ] blocking fail이 없다

### Approval

- [ ] Product (kknaks)
- [ ] QA (coordinator)
- [ ] Tech Lead (kknaks)
- [ ] 범위·비용·공개 범위가 바뀐 경우 Decision Owner — 특히 **외부 공개 전환은
      DEC-002·DEC-005 재검토 사안**이다
