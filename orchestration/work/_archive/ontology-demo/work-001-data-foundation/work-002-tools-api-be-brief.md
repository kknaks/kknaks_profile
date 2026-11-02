
# [backend] WORK-002 도구와 API — MCP 4종 + 계층·KPI·그래프·예보 API + 접속 게이트

너는 **ontology-demo `backend` 워커**다. WORK-001 에 이어 같은 워크트리·같은 브랜치에서 계속한다
(WORK-001 은 커밋됨). 역할 문서는 그대로 유효하다.

⚠ 워크트리 공유: FE 워커가 `app/front/` 에서 병행 중 — 너는 `app/ontology-agent/` 만. git 조작 금지(add·commit 포함 — 커밋은 코디가 한다).

## 1. SSOT — 먼저 읽을 것 (read-only 절대경로)

- `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline/para/projects/summer-star/ontology-demo/30-work/work-002-tools-and-api.md` ← 이번 작업의 SoT (P1~P5)
- 같은 폴더 `../20-spec/spec-002-mcp-tools-contract.md`(v0.0.3 — 도구 4종 파라미터·응답·에러 10종·allowlist·상한 거부) · `spec-003-api-and-chat-contract.md`(v0.0.4 — 엔드포인트 15·게이트·lineage 확장 필드·edge_id `<from>__<to>`·lag_days) · `spec-001-data-layer-contract.md`(v0.0.7 — 뷰·enum·Case Matrix 13) · `spec-005-agent-loop-and-gates.md`(답변 객체 — 채팅 API 는 WORK-003 이지만 shape 참조)
- **조사 리포트**: `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/docs-baseline/research-codex-mcp-report.md` — §5.0(재발명 금지: `app/mcp` FastMCP 패턴·`app/back` 라우터 패턴 재사용) · §5.3(MCP 서버 기동) · §5.4(가져올 패턴). codex 결선 자체는 WORK-003 몫.

## 2. 계약 — 코디 확정값

- **AC-8(뷰 경유) 강제를 게이트로**: 리뷰어 조건 — `connect_ro` 만으론 부족하다. 도구·API 코드가
  `v_*` 마스킹 뷰와 허용 테이블(골드·온톨로지)만 조회함을 **정적 검사(grep/AST) 테스트**로 고정하라.
  브론즈·실버 원 테이블 문자열이 tools/·api/ 에 나오면 FAIL.
- 접속 게이트: env `ONTOLOGY_DEMO_PASSWORD` 단일 — 프론트 미들웨어와 같은 값을 백 API 가 검증
  (SPEC-003 U-1·S-5, 401 NO_SESSION). 값 하드코딩 금지, 로컬 검증은 임시값.
- MCP 서버: FastMCP Streamable HTTP, `app/mcp` 모범. 도구 4종 이름·시그니처는 SPEC-002 그대로.
- WORK-001 재검수의 관찰 반영: **build_meta**(빌드 성공 표식 — 미빌드/실패빌드 구분) 도입해
  `connect_ro`·API 기동이 실패 빌드 DB 를 정상처럼 서빙하지 않게.
- **nit 6건 정리**(재검수 리포트 review-work-001-fix-report.md 하단): stale 주석·spec 버전 참조
  v0.0.7 갱신·README 코드 13종·Settings.sources 미사용·masking 함수내 import — 이번에 같이 청소.

## 3. 구현 단계 — work-002 문서의 P1~P5 그대로. phase 마다 [진행] 보고.

## 4. 하지 말 것

- 채팅 API·에이전트 루프(WORK-003)·화면(FE) 금지. `app/front/` 접근 금지.
- 자유 SQL 도구 금지 · 상한 초과는 절단이 아니라 거부(SPEC-002) · PII 원값 금지.
- git 조작 금지 · allowed_paths(`app/ontology-agent/`) 밖 금지 · spec 어긋나면 코드 말고 질문.

## 5. 검증

```
cd app/ontology-agent && uv run pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지). 검증 1회.
API 는 uvicorn 기동 + 대표 엔드포인트 수동 호출 확인(게이트 401 포함).
```

## 6. 완료 보고 — 2채널 (preamble 값 우선)

```bash
orca orchestration send --to term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: WORK-002 도구·API" --body "변경 파일 / phase 요약 / AC-8 정적 게이트 수치 / 테스트 / 미결"
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --text "[worker_done] backend 완료 — WORK-002. 상세는 인박스." --enter
# 막히면: orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --text "[질문] backend: <질문>" --enter
```
