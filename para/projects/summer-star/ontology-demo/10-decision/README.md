# Decision Index

규칙: `para/projects/project.md`

> baseline을 제품에 어떻게 적용할지 판단한 결정 목록과 아직 풀어야 할 질문을 관리한다.

## 결정 로그

decision 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| DEC-001 | DB = 메달리온 전 계층 — 브론즈까지 한 DB 에 담고 빌드를 DB 로 이식 | accepted | BASE-001 | 전 계층 SQLite 적재 + 빌드 입출력만 DB 로(규칙·게이트는 기록 04·05 그대로) | (작성 예정) |
| DEC-002 | PII 경계 — 원값은 DB 보존, 표시·응답에서 마스킹 | accepted | BASE-001 | 마스킹 뷰 경유만(에이전트 포함) · 노출 0건 게이트 · 소거 사본 안 만듦 | (작성 예정) |
| DEC-003 | LLM 경로 — open-kknaks 경유 + 조회 도구 4종 MCP | accepted | BASE-001 | SDK 직접 import 금지(ADR-04) · codex(gpt-5.6-terra) · FastMCP 서버 · 자유 SQL 금지 | (작성 예정) |
| DEC-004 | 웹 = `app/front` 통합 3페이지 | accepted | BASE-001 | 단일 페이지·Streamlit 안 폐기 → 채팅·모니터링·데이터 3면, 백은 API 서버 | (작성 예정) |
| DEC-005 | 배포 = 내부 공유용 데모 | accepted | BASE-001 | 프론트 Vercel · 백/redis/워커 홈서버(NPM) · 가드는 공유 비밀번호 하나 | (작성 예정) |

## 미결 사항

spec으로 내리기 전에 판단해야 하는 질문을 적는다.

| ID | Question | Owner | Next |
|---|---|---|---|
| DEC-002 OQ-1 | 마스킹 표기 형식 — 어느 자리까지 남길지 | kknaks | spec 에서 확정 |
| DEC-003 OQ-1 | 조회 도구 4종의 파라미터·응답 스키마 (특히 `trace_ontology` 판정 구분) | kknaks | spec 에서 확정 |
| DEC-004 OQ-1 | 화면 상세(레이아웃·컴포넌트·카피) | kknaks | 디자인 별도 세션 진행 중 — 귀환 후 spec |
| DEC-004 OQ-2 | 채팅 `used_edges` → 그래프 하이라이트 방식(페이지 간 상태 공유) | kknaks | spec 에서 확정 |
| DEC-005 OQ-1 | 비밀번호 가드 위치 — 프론트 미들웨어 · 백 API · NPM 중 어디 | kknaks | spec 에서 확정 |
