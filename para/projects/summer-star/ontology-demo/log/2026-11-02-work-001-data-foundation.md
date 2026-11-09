# 작업 요약 — work-001-data-foundation (ontology-demo)

기간: `2026-09-02` ~ `2026-09-03`
결과: 코드 PR #33 `ontology-demo` 에 머지(413 passed / 5 skipped). 홈서버 실배포는 안 함(2026-11-02 확인 — 컨테이너 없음)

## 1. 무엇을 했나

기록 01~08 이 CSV 로 검증한 온톨로지 스택(메달리온 3계층 + nodes/edges + 에이전트)을 내부 공유용 데모 앱으로 옮겼다.
WORK-001~005 다섯 WP 를 backend·frontend 워커가 구현하고 WP 마다 read-only 리뷰어가 검수(FAIL/WARN → fix → 재확인)했다.
착지: `app/ontology-agent/`(SQLite 한 DB · FastMCP 도구 4종 · FastAPI · open-kknaks 경유 codex 에이전트) + `app/front/(ontology)` 3페이지 + compose·README 배포 절차.

## 2. 적용한 기술·개념

- **[[staging-area]] — 단일 트랜잭션 스테이징 후 스왑** — 빌드가 게이트에 걸리면 이전 DB 가 그대로 남게
  - 무엇이 어려웠나: 첫 구현은 게이트 2·3 실패에도 이전 DB 가 남지 않았다(검수 F2). SAVEPOINT 가 바깥 트랜잭션 처리 때문에 무력화돼 있었고, 실패 주입 회귀 7본으로 실증한 뒤 닫았다
  - 근거: `review-work-001-report.md` F2 · `review-work-001-fix-report.md`
- **[[medallion-architecture]] — 계층 경계를 테스트로** — 「상위는 바로 아래만 읽는다」
  - 무엇이 어려웠나: CSV 스크립트를 이식하자 골드가 브론즈를 직접 읽었다(F1). 같은 이식 과정에서 강남언니 정합률 게이트가 계산만 하고 막지 않게 됐다(F3) — 포팅은 규칙만 옮기고 차단력은 놓친다
  - 근거: `review-work-001-report.md` F1·F3 · 재현 대조 25항 + 1,487,414셀 전수 일치
- **[[pii-masking]] — 값 형태로 판정하는 마스킹** — `chart_no`
  - 왜 이걸 골랐나: PII 전면 스캔(needle 2.4만 종)이 차트번호 자리에 이름이 앉은 원천 오염 1건을 잡았다. 78,216행 중 1행 때문에 필드 전체를 마스킹으로 선언하면 화면이 반대로 오해한다 → 숫자가 아닌 값만 `[비정형]` 토큰으로
  - 근거: PR #33 리뷰 포커스 ① · SPEC-001 AC-7
- **AST 정적 게이트로 「마스킹 뷰 경유」 강제** (AC-8, 54본)
  - 왜 이걸 골랐나: 리뷰·런타임 테스트로는 새 쿼리가 원 테이블을 읽는 걸 못 막는다
  - 무엇이 어려웠나: 검수가 f-string 접두어 조합 우회 두 갈래를 찾았고(WORK-002 W2), 게이트를 보강하자 기존 코드가 걸렸다. whitelist 로 덮지 않고 코드를 검증 가능한 형태로 고쳤다. 못 잡는 한계(동적 컬럼 조립)는 테스트 이름에 명시
  - 근거: `review-work-002-report.md` W2
- **MCP 도구와 API 가 같은 `service/` 함수를 부른다** — 화면·도구 수치 오차 0(AC-5)을 대조가 아니라 구조로
  - 왜 이걸 골랐나: MCP → API 래퍼 안은 두 경로가 갈라질 여지를 남긴다
- **[[ai-agent]] 에 도메인 지식 0건 · 응답 스키마 검증기** — 관계는 `trace_ontology` 조회로만
  - 왜 이걸 골랐나: 프롬프트에 관계를 넣으면 기각된 엣지도 말한다. `used_edges ⊆ 확정 판정` · 인용 재조회 일치 · 정량 추정 금지를 검증기가 강제, 위반은 목록만 실어 1회 재제출
  - 무엇이 어려웠나: codex 승인 축이 둘이라 per-tool `approval_mode=approve` 와 `features.apps=false` 를 제출 페이로드에 매번 실어야 했다(조사 리포트의 함정 2건). 라이브 회귀 3본이 에이전트 결함 2건을 잡아 테스트가 아니라 에이전트를 고쳤다
  - 근거: `../docs-baseline/research-codex-mcp-report.md` §3 · `review-work-003-report.md`
- **[[design-token]] 컨테이너 스코프** — `--ont-*` + `color-scheme: light` 재선언으로 기존 포트폴리오 `globals.css` diff 0
- **배포 차단 결함 사전 발견 — CORS · [[cookie]] SameSite** — 프론트 Vercel · 백 홈서버라 교차 오리진
  - 왜 이걸 골랐나: credentials 요청이라 와일드카드 불가 → 명시 오리진 목록, 미설정이면 기동 거부([[fail-fast]]). SameSite·Secure 는 배포 스킴에서 파생해 두 곳에 손으로 적지 않는다
  - 근거: SPEC-003 v0.0.11 · AC-22·23

## 3. 막혔던 것 / 사고

- WORK-001 1차 검수 FAIL(차단 3) — 전부 「CSV 스크립트를 이식」하는 과정에서 생긴 계층·게이트 위반. 이식은 재설계가 아니라는 원칙이 오히려 「옮겼으니 같다」는 착각을 만들었다 → 검수가 잡고 fix → 재검수 PASS
- 쿼리 전송 형식 미기재로 사용자 E2E 에서 FE(반복 파라미터)·BE(콤마)가 갈라짐 → 서버가 둘 다 받게 하고 SPEC-003 에 정본 명시
- 코디·워커 터미널 핸들이 중간에 죽고 재생성됨(term_7d777e3b → 3fb7e8e1). 워커는 preamble 규약 덕에 보고가 끊기지 않았다
- 라이브 게이트의 LLM 비결정성 — 단언을 느슨하게 하지 않고 「도구가 계산식을 실제로 준다」는 기준값 계층으로 과녁을 고정

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-09-02 | WP 5건 · 22 phase | 사용자 지시 |
| 2026-09-02 | BE 순차(001→002→003) 중 디자인 세션 병행, WORK-004 는 디자인 조정 20건 해소 후 | 사용자 합의 |
| 2026-09-02 | 코드 PR 은 전 WP 완료 후 1건 | 사용자 지시 |
| 2026-09-03 | `chart_no` 는 필드 마스킹 대신 값 형태 판정 | PII 스캔 실측 1건 |

## 5. 날짜별 로그

- `2026-09-02` WORK-001 발주 → 검수 FAIL → fix → PASS
- `2026-09-03` WORK-002·003·004·005 → 최종 413 passed → PR #33 머지

## 6. 산출물

- 코드 PR: https://github.com/kknaks/kknaks_profile/pull/33
- 문서 PR: https://github.com/kknaks/kknaks_profile/pull/32
- 리포트: `review-work-001-report.md` · `review-work-001-fix-report.md` · `review-work-002-report.md` · `review-work-003-report.md` · `review-work-004-report.md`

## 7. 잔여

- 홈서버 실배포 · Vercel env — README 「배포」 절차, 사용자 실행. 2026-11-02 기준 미배포
- 로컬 E2E 7단계 중 게이트 5-③(칩 클릭 하이라이트) 육안 확인 기록 없음
- nexus 13종 컬럼 스키마 계약 미고정

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/ontology-demo/work-001-data-foundation/README|work-001-data-foundation]]
<!-- work-links:end -->
