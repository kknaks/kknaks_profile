# Spec Index

규칙: `para/projects/project.md`

> 기능, UX, 정책, acceptance criteria 계약으로 들어가는 map이다. 상세 계약은 `20-spec/` 아래 사용자 기능/정책 묶음 단위의 spec 파일로 둔다.
> 본문은 contract만 다룬다. 구현 진척·work 매핑은 `30-work/README.md`, 결정 로그는 `10-decision/README.md`, 변경 이력은 `log.md`, 리뷰 artifact는 `00-baseline/`, 내부 구조는 `40-architecture/`를 본다.

최종 수정: 2026-09-03

## Data / Domain Boundary

SPEC에는 Product, QA, frontend, 외부 연동자가 알아야 하는 도메인 용어와 API 계약만 둔다.

- SPEC에 둠: 테이블·뷰·도구·엔드포인트의 **이름**, 파라미터, enum, 상태, 게이트 수치, acceptance criteria.
- SPEC에 두지 않음: 컬럼 전문·DDL·인덱스·ORM·마이그레이션, service/repository 구조, 파일 경로.
- 실제 schema의 source of truth는 제품 코드와 migration이다. **변환 규칙·KPI 계산식의 SoT 는 기록 03·04·05**(`para/resources/note/ontology/`)다 — spec 은 그것을 인용만 한다.

## Scope

### In Scope

- 화면 3페이지의 라우트·셸·토큰 레이어·컴포넌트 계약(SPEC-004)
- 데이터 계층(브론즈·실버·골드·온톨로지)의 테이블 목록·경계·마스킹 뷰·적재 게이트
- 조회 도구 4종의 MCP 계약
- FE↔BE API(계층 조회·KPI·그래프·예보·채팅)와 접속 게이트
- 에이전트 루프·답변 응답 스키마·게이트 5종·회귀 3본

### Out Of Scope

- 시각 토큰 값(hex·px·타입 스케일) — 디자인 패키지 `design/01-tokens.md` 가 SoT
- 웹 raw 업로드·수집 자동화(파이프라인 단계), 알림 발송, 다지점 확장
- rate limit·계정·권한 등급(DEC-005 D2 — 두지 않기로 확정)

## Terms

| 용어 | 의미 |
|---|---|
| 계층 | 브론즈(원형) → 실버(표준화) → 골드(KPI) → 온톨로지(관계). 상위는 바로 아래만 읽는다 |
| 마스킹 뷰 | `v_*` — 소비자(화면·API·에이전트)가 브론즈·실버에 닿는 유일한 경로 |
| 판정 | 엣지의 확정 상태 — **채택 · 자동 확정 · 선언 · 보류 · 기각**(정본 한글값). 인과 서술에는 앞 3종만 |
| 노드 타입 | `kpi` · `intervention` · `organic` · `exogenous` · `unobserved` · `attribute`(정본 영문 enum). 한글 카피 매핑은 SPEC-004 |
| `lag` | 정본 문자열 원형(`0d`·`2w`·빈 값 등). API·도구는 `lag_days`(정수) 병기 |
| KPI 상태 | 그 시점 값의 판정 — 양호 · 주의 · 경고 (전 기간 백분위 25%/10%) |
| 노드 상태 | 최근 7일 빈도 — 정상 · 관찰(≥1) · 알림(≥3) |
| `used_edges` | 답변이 실제로 밟은 확정 엣지. 그래프 하이라이트의 유일한 입력 |
| `citations` | 답변에 실린 모든 수치의 역추적 근거(도구·테이블·컬럼) |

## Spec Bundle

| 묶음 | 포함 Spec | 파일 |
|---|---|---|
| 데이터 계층 | SPEC-001 | [spec-001-data-layer-contract.md](spec-001-data-layer-contract.md) |
| 에이전트 표면 | SPEC-002 · SPEC-005 | [spec-002-mcp-tools-contract.md](spec-002-mcp-tools-contract.md) · [spec-005-agent-loop-and-gates.md](spec-005-agent-loop-and-gates.md) |
| 앱 표면 | SPEC-003 · SPEC-004 | [spec-003-api-and-chat-contract.md](spec-003-api-and-chat-contract.md) · [spec-004-three-screens.md](spec-004-three-screens.md) |

## Spec List

spec 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다. work 진행률, owner, blocker, PR은 `30-work/README.md`로 보낸다.

| ID | Title | Area | Status | Decision | File |
|---|---|---|---|---|---|
| SPEC-001 | 데이터 계층 계약 — 메달리온 전 계층 DB · 마스킹 뷰 · 적재 게이트 | data | **ready** (v0.0.6) | DEC-001 · DEC-002 | [spec-001-data-layer-contract.md](spec-001-data-layer-contract.md) |
| SPEC-002 | 조회 도구 계약 — MCP 4종 | agent | **ready** (v0.0.3) | DEC-002 · DEC-003 | [spec-002-mcp-tools-contract.md](spec-002-mcp-tools-contract.md) |
| SPEC-003 | FE↔BE API 계약 — 계층·KPI·그래프·예보·채팅·접속 게이트 | api | **ready** (v0.0.4) | DEC-003 · DEC-004 · DEC-005 | [spec-003-api-and-chat-contract.md](spec-003-api-and-chat-contract.md) |
| SPEC-004 | 화면 계약 3페이지 — 모니터링 · 채팅 · 데이터 | ui | **ready** (v0.1.0) | DEC-004 · DEC-002 · DEC-005 | [spec-004-three-screens.md](spec-004-three-screens.md) |
| SPEC-005 | 에이전트 루프와 게이트 — `used_edges` · 게이트 5종 · 회귀 3본 | agent | **ready** (v0.0.3) | DEC-003 | [spec-005-agent-loop-and-gates.md](spec-005-agent-loop-and-gates.md) |

**SPEC-004 `ready` (2026-09-02)** — 디자인 실현성 검토(전 페이지 FEASIBLE-WITH-CHANGES ·
BLOCKED 0건) 후 작성했고, design-fix 세션이 **조정 20건을 전건 해소**해 `ready` 로 올렸다.
정정 이력은 SPEC-004 §7.2, 답변 예문 소재는 §7.3.

## Reading Order

| Area | Spec |
|---|---|
| 데이터부터 보는 사람 | SPEC-001 → SPEC-002 → SPEC-005 → SPEC-003 |
| 백엔드 구현자 | SPEC-001 → SPEC-003 → SPEC-002 → SPEC-005 → SPEC-004(화면이 요구한 필드) |
| 프론트 구현자 | SPEC-004 → SPEC-003 → SPEC-005(`used_edges`) → SPEC-001(enum·마스킹 표기) |
| 에이전트 구현자 | SPEC-005 → SPEC-002 → SPEC-001 |

## Open Questions

각 spec §7 의 요약이다. 직전(2026-09-02) 「제안」 21건은 **전건 승인**돼 확정 서술로 바뀌었고,
아래는 **남은 것**이다.

| ID | Question | Owner | Next |
|---|---|---|---|
| SPEC-003 OQ-8 | 컬럼 값 분포 엔드포인트를 둘 것인가 | kknaks | 분포 바 제거 권고 — 유지 시 엔드포인트 추가 |
| SPEC-004 OQ-1 | KPI 카드 클릭의 목적지 | kknaks | 그래프 노드 선택 제안 |
| SPEC-004 OQ-2 | 「그 외 KPI」 카드 표기 | kknaks | 상태별 내역 파생 |
| SPEC-004 OQ-3 | 좌표 자산 보관 위치·형식 | kknaks | 구현 재량 |
| SPEC-005 OQ-6 | timeout·재시도 확정값 | kknaks | 실측 후 조정 |

**닫힌 것 (2026-09-02)** — SPEC-005 OQ-4(게이트 5-③ 검증 대상 = **모니터링 그래프 단일**) ·
SPEC-002 OQ-2(`grain=monthly` = **골드 월 View 조회**) · SPEC-003 OQ-4(가드 위치 = 프론트
미들웨어 + 백 API) · SPEC-003 OQ-5(`node_state` 산정식) · SPEC-001 OQ-1·2·3·4·5·6 ·
**SPEC-004 OQ-4**(최소 폭 문구 — design-fix).

## 디자인 조정 — 전건 해소

design-fix 세션(2026-09-02)이 SPEC-004 §7.2 의 **20건을 전건 해소**했다 — 마스킹 표기 ·
중립 바 카피 · 브론즈 테이블 수 · 계층별 행수 · `noshow_rate` 계산식 · `visit_status` enum ·
그래프 노드·엣지 구성 · 예보 예시 수치 · 답변 패턴 A·B 예문 · 메시지 상태 5종 시각 설계 ·
접속 게이트 화면 · 라우팅 표 · Responsive · 채팅 레이아웃 · 분포 바 · 시작 카드 ·
골드 표 컬럼. 정정 이력은 SPEC-004 §7.2, 답변 예문 소재는 §7.3 이다.

**남은 비고 하나** — 프로토타입 4종(`Monitoring`·`Data`·`Frames`·`DesignSystem`.dc.html)은
정정 이전 값을 일부 품고 있다. **참조물이라 정정 대상이 아니며**, 값이 갈리면
문서(`01`~`08`)와 `data/*.json` 이 맞다(SPEC-004 §7.2 말미).
