# 작업 요약 — docs-baseline (ontology-demo)

기간: `2026-09-02` ~ `2026-09-03`
결과: 문서 PR #32 `ontology-demo` 에 머지. 2026-11-02 `ontology-demo → main` PR 로 함께 올림

## 1. 무엇을 했나

온톨로지 실행 기록 01~08 과 기록 09(데모 앱 계획)는 note 였지 발주할 수 있는 계약이 아니었다.
이를 제품 문서 파이프라인(baseline → decision → spec → work)으로 내려
`para/projects/summer-star/ontology-demo/` 에 BASE-001 · DEC-001~005 · SPEC-001~005 · WORK-001~005 를 세웠다.
문서 본문은 이 프로젝트에 한해 docs 워커가 쓰고(config 예외), 코디는 검증·사용자 문답·커밋만 맡았다.
spec 은 코드 작업(work-001-data-foundation)과 함께 24차례 상호 개정되며 PR #32 하나로 닫혔다.

## 2. 적용한 기술·개념

- **[[pii-masking]] — 원값 보존 + 표면 마스킹, 가리는 지점은 뷰 하나** — DEC-002
  - 왜 이걸 골랐나: 수집 단계 소거안은 드릴다운에서 「여기 실명이 있었다」가 사라지고, 소거 사본안은 원천이 둘이 된다. 내부 공유(DEC-005)라는 전제를 결정 본문에 재검토 조건으로 박았다
  - 무엇이 어려웠나: 처음 spec 은 「PII 컬럼명은 목록에 없다 / UNKNOWN_FIELD 로 거부」로 썼는데, 구현은 컬럼명을 유지하고 값만 바꿔야 화면이 성립했다. 보증 주체를 「컬럼 숨김」이 아니라 「뷰의 SELECT 목록 + 뷰 경유 강제(AC-8)」로 다시 썼다
  - 근거: `10-decision/decision-002-pii-masking-boundary.md` · `log.md` 2026-09-03 SPEC-001 v0.0.8 행
- **[[medallion-architecture]] — 브론즈 원형까지 한 DB 에** — DEC-001
  - 왜 이걸 골랐나: 데모의 목적이 「어느 계층이든 원본까지 드릴다운」이라 브론즈를 빼면 역추적이 끊긴다. 빌드는 변환 규칙을 재설계하지 않고 입출력만 파일→DB 로 이식
  - 근거: `10-decision/decision-001-db-medallion-all-layers.md`
- **정본 대조로 spec 발명 걷어내기** — spec 이 만든 판정 라벨(`산출0`·`외생`)·노드 id 8건이 원천 `nodes.csv` 와 달랐다
  - 무엇이 어려웠나: 문서끼리는 정합해 보여 리뷰로는 안 잡혔고, backend 가 실데이터를 적재하면서 드러났다. 정본 한글값(`자동 확정`·`선언`)으로 전수 교체하고 번역 축을 `node_type` 하나로 줄였다
  - 근거: `log.md` 2026-09-02 「정본 대조 정정」 행
- **디자인 실현성 검토를 spec 앞에** — 핸드오프 시안을 read-only 리뷰어가 페이지별로 판정(전 페이지 FEASIBLE-WITH-CHANGES · BLOCKED 0)한 뒤 SPEC-004 를 썼다
  - 왜 이걸 골랐나: 시안이 요구하는 수치(파생 카운트 12항)를 API 가 주지 못하면 화면이 하드코딩으로 간다. 이 표를 spec 에 「하드코딩 금지 표」로 박았다
  - 근거: `review-design-feasibility-report.md` · `20-spec/spec-004-three-screens.md`

## 3. 막혔던 것 / 사고

- runbook 을 「단일 레포형 문서도 워커 발주」로 전면 개정했다가 kknaks-dev 기존 방식이 조용히 뒤집히는 걸 사용자가 잡음 → 같은 날 runbook 원복, ontology-demo 한정 예외로 config notes 에만 둠(4a3690a). 이후 main 에서 「코디 워크트리 탑승 문서 워커」로 일반화됐다
- 브리프가 「SPEC-001 AC-3(마스킹)」이라 했지만 실제 마스킹은 AC-7 — 워커가 확인 후 대상 확대로 진행. 브리프에 번호를 박을 땐 원문을 열어 확인할 것
- 계약에 쿼리 전송 형식(`verdicts` 콤마 vs 반복 파라미터)을 안 적어 E2E 에서 FE·BE 가 갈라짐 → SPEC-003 v0.0.12 에 정본 명시

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-09-02 | ~~단일 레포형 문서도 워커 발주(runbook 개정)~~ → runbook 원복, ontology-demo 한정 예외로 config 에만 | 사용자 지시 — 다른 프로젝트 방식이 조용히 바뀜 |
| 2026-09-02 | 문서 위치 = `para/projects/summer-star/ontology-demo/` | 사용자 선택 |
| 2026-09-02 | 프론트 = `app/front/` 통합 3페이지(채팅·모니터링·데이터). 기록 09 의 「FastAPI 단일 페이지 또는 Streamlit」 폐기 | 사용자 지시 (DEC-004) |
| 2026-09-02 | 마스킹 표기 `김○○`/`010-****-1234`/`1990-**-**` · 게이트 env 비번 1개 · 채팅 미니그래프 제거(칩 + `?edge=` 점프) · Pretendard next/font · 정량 추정 문구 제거 · 월 집계 = `gold_kpi_monthly` View | 사용자 문답 |
| 2026-09-02 | WP 10건 → 5건 · 22 phase (태스크는 WP 안 phase) | 사용자 지시 |

## 5. 날짜별 로그

- `2026-09-02` runbook 개정·원복 → BASE-001 → DEC-001~005 → 디자인 실현성 검토 → SPEC-001~005 → WORK-001~005 (PR #32 머지)
- `2026-09-03` 코드 작업 실측으로 spec 연속 개정(Case Matrix 13행·부분 월·`has_prev_period`·`source_group`·`error_code`·CORS·`chart_no` 값 형태 마스킹)

## 6. 산출물

- 문서 PR: https://github.com/kknaks/kknaks_profile/pull/32
- 커밋: `bce52d7` (스캐폴딩·docs 워커) · `43dd669` (pii-masking 개념) · `4a3690a` (runbook 원복)
- 리포트: `research-codex-mcp-report.md` · `review-design-feasibility-report.md`

## 7. 잔여

- DEC-004 `up: []` — front 개념 출처 노트가 생기면 잇는다
- nexus 13종 컬럼 스키마 미고정(`columns_note` 로 표기) — 필요 시 SPEC-001 확장
