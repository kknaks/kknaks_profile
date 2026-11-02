# [backend] WP-003 — 메모 트랙 API + AI 중간 요약 배치(웜스타트 · MCP 도구 레지스트리 · 구조화 출력 · 전량 교체 · push)

너는 **sc-ax `backend` 워커**다. WP-001·002 를 한 세션이면 그 맥락을 쓴다. 역할 문서(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/backend/role.md` (+ `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (HEAD = WP-002+FE P3 커밋, 코디가 방금 커밋 → PR `main`). `frontend/` 읽기만.

## 1. SSOT

- **SPEC 0.4.1** `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/20-spec/spec-004-meeting-note.md` — **§6 메모 트랙 · §7 AI 중간 요약(7.1 배치 계약 · 7.2 도구 · 7.3 경계) · §4 안건·줄 · §12 R-## · §13 OQ-304/307/312/315**.
- **WP-003** `30-work/work-003-memo-ai-batch.md` — Scope·Domain·Phase 1~3 검증 = 완료 조건.
- **원형(task-management, 읽기만)**: `/Users/kknaks/git/toy_pr2/task_management/app/back/service/meeting_batch_service.py`(트리거 `evaluate/schedule/_arm_timer`, 회의당 lock `_lock_for`, `_run_once`, `_parse_output`·`_demote_if_needed`·`_persist` 전량 교체, `launch_warm_start`·`_WARM_START_PROMPT`·`build_batch_prompt`) · `integrations/agent.py`(`AgentGateway` 포트 · `build_mcp_config` · `install_gateway` 대역) · `ai_schemas/meeting_notes.json`(strict 스키마 — 선택 필드는 nullable, 전부 required · 실물 400 사례 주석) · `tests/test_meeting_batch.py`.
- **현행 AI 경로**: `orchestration/work/sc-meeting/survey-01-ai-provider-report.md` §2(Codex CLI `CodexCliProviderAdapter` — `converse` 가 `exec resume`·MCP override 지원, `generate` 는 스키마 출력) · `platform/codex_cli.py` · `modules/ax_execution/ai.py`(`AiConversationRequest`·`provider_session_ref`) · `entrypoints/mcp.py`(scax MCP 도구, persona 바인딩 필수) · `platform/conversations.py`·`conversation_provider_session_references`(세션 ref 저장 방식).
- **WP-002 산출**: `push_ai_batch(meeting_id, seq, payload)` 통로 · 「미처리 확정 블록 커서」 조회 — 완료 보고에서 이름 확인.

**기대는 개념** — 해당 없음.

## 2. 무엇을 만드나

회의가 도는 동안 **사람 메모 줄**(track memo)을 받고, **AI 트랙**(track ai)을 배치로 채운다. 배치는 회의당 provider 세션 하나를 **웜스타트**로 열어 두고 증분만 넣어 이어 쓰며, 우리 MCP 서버를 붙여 필요할 때 조회한다. 출력은 스키마로 강제된 **AI 트랙 전체**이고, 검증 통과분으로만 전량 교체 후 즉시 `push_ai_batch` 로 구독자에게 민다.

## 3. 계약 (코디 확정)

- **메모 API**(FE 가 이미 이 형태로 소비 — 바꾸지 마라): `POST /api/meetings/{id}/agendas/{agendaId}/lines` body `{text}` → 201 `Line{line_id, track:"memo", order, text, author, evidence:[], at_ms}`. 게이트: 만든 사람 · in_progress · 안건이 그 회의 것. 빈 문자열 422.
- **D26 (FE P3 인계 셋)**: ① `Line.at_ms: int|null` — memo 줄은 서버가 `now − started_at` 으로 채움(스크립트 탭 시각 축), ai/final 줄은 null. MeetingDetail 의 모든 Line 에 실림. ② `GET /api/meetings/{id}/transcript` → `{items:[{id, speakerLabel, atMs, endMs, content}], memos:[{line_id, agenda_id, text, author, atMs}]}` — 열람 = 참석·공유(상세와 같은 축), 상태 in_progress 이후 전부(scheduled·cancelled 404 아님, 빈 배열). WP-002 의 MeetingTranscript 저장분을 읽기만. ③-b MeetingDetail 응답에 `started_at`(ISO|null)도 싣는다 — 코디 e2e 에서 비어 있었다(`at_ms` 기준점을 FE 가 알아야 한다). ③ MeetingDetail 게이트에 `can_write_memo`(만든 사람 && in_progress) 추가 — FE 는 이 값으로 입력 칸을 세운다.
- **세션(웜스타트)**: `POST /start` 전이 직후 백그라운드로 회의당 provider 세션 열기 — `AiConversationRequest` 로 `converse`, 첫 turn 이 맥락(회의 정보·안건·참석자·이어진 이전 회의의 안건·결론)이고 응답은 버린다. `provider_session_ref` 를 **회의에 저장**(`meeting_ai_sessions` 테이블 또는 meetings 컬럼 — 현행 `conversation_provider_session_references` 와 같은 방식). 열기 실패 = 회의는 정상, 배치만 안 냄(로그만).
- **배치 트리거**(값은 상수로, OQ-307): ① 미처리 확정 발화 ≥ 600자 ② 안건 전환 즉시(미처리 < 80자면 생략) ③ 미처리 생긴 뒤 90초 경과. 회의당 동시 실행 1(lock). 실행 중 트리거는 끝난 뒤 커진 구간으로.
- **배치 입력**: 세션 resume + 직전 성공 배치 이후의 확정 블록(speakerLabel·atMs·endMs·text)과 새 메모 줄(agenda_id·text·author). 앞 구간은 세션이 기억한다.
- **MCP 도구**: `converse` 에 scax MCP 서버(`CodexCliMcpServer`)를 붙인다. **persona = 회의를 만든 사람**(현행 MCP 의 persona 바인딩 규칙 그대로 — OQ-315 기본값). **레지스트리** = 설정(env 또는 `bootstrap/settings.py`)의 도구 이름 allowlist. 최소 넷: `task_list`(업무 목록) · `project_list`(프로젝트) · `meeting_get`(이전 회의 안건·결론) · `member_list`(참석자 명부) — 현행 `entrypoints/mcp.py` 에 있는 도구 이름으로 매핑하고 없는 건 만든다(조회만). 도구는 전부 read-only.
- **출력 스키마**(strict — 원형 `meeting_notes.json` 규칙: 모든 object `additionalProperties:false`, 모든 키 required, 선택은 nullable): `{agendas:[{agenda_id: string|null, title, source:"manual"|"carried"|"ai", lines:[{text, evidence:[{from_ms,to_ms}], task_id: string|null}]}]}`. 회의 중 오면 안 되는 필드(제목 후보·todo)는 스키마에 두지 않는다. `agenda_id` null = AI 가 새로 세운 안건(source ai).
- **검증·적재**: 스키마 위반 → 배치 전체 폐기(직전 성공분 유지, 구간은 다음 배치로) · `task_id` 가 회의 참석자 범위 밖이거나 없으면 그 줄만 강등(`task_id` null) · evidence 가 미처리 구간 밖이면 그 줄만 강등. 통과분으로 **AI 트랙(track ai) 전량 교체** — 안건은 agenda_id 매칭, 없으면 신설(source ai, order 뒤에), 사람이 만든 안건은 제목·출처를 건드리지 않는다(§7.3). 트랜잭션 하나. 커밋 즉시 `push_ai_batch(meeting_id, seq, {agendas:[…MeetingDetail 의 Agenda 모양, lines 는 track ai 만]})`.
- **실패**: 조용히, 구간을 다음 배치에 합친다. 화면 표시 없음. provider 호출은 DB 트랜잭션 밖(현행 원칙 유지).
- **종료**: `/end` 뒤 새 배치 안 냄. 세션은 닫지 않는다(WP-004 합성이 같은 세션을 쓴다 — §8-3).

## 4. 먼저 읽을 파일

- 원형 `meeting_batch_service.py` 전문 · `agent.py` · `meeting_notes.json`
- `platform/codex_cli.py`(`converse`·`_mcp_overrides`·resume) · `modules/ax_execution/ai.py` · `entrypoints/mcp.py`(도구 목록·persona) · `bootstrap/conversation_worker.py`(대화 배치가 provider 를 어떻게 돌리는지 — 회의 배치 워커도 같은 방식으로 `bootstrap/meeting_worker.py` 에)
- WP-002 결과물: WS 서비스의 `push_ai_batch` · 확정 블록 커서
- `modules/meetings/application.py`(`append_line` 최소 표면 — 메모 API 로 완성) · `tests/contract/test_meeting_core.py`

## 5. allowed_paths

- `backend/` · `docker-compose.yml` · `Makefile`. `frontend/` 읽기 전용.

## 6. 단계 (WP-003 Phase 1→2→3)

1. 메모 API + 게이트 + `at_ms` · `can_write_memo` · `GET /transcript` + 테스트.
2. 세션 테이블/컬럼 · 웜스타트(백그라운드, `/start` 훅) · MCP 레지스트리 설정 · 배치 트리거(커서·lock·타이머) · 배치 실행(resume·증분 입력) — provider 는 테스트 대역(`install_*` 식 fake converse).
3. 출력 파싱·검증·강등·전량 교체·push · 실패 경로 · `/end` 뒤 미발행.
4. §8 검증 → 완료 보고(WP-004 인계: 세션 ref 접근 함수 · 스키마 파일 위치 · 커서).

## 7. 하지 말 것

- 합성·제목 후보·다음 할 일 추출(WP-004) · 자료·공유(WP-005) · 화면 금지.
- 실제 Codex/MCP 호출을 테스트에서 하지 않는다(대역). 실물은 코디.
- 사람 메모를 AI 가 고치거나 지우게 두지 않는다. 사람이 AI 줄을 회의 중에 고치는 API 를 만들지 않는다.
- 도구로 쓰기 금지(조회만). Alembic 금지. `make local-stack`·5176/8001 금지. `make reset-demo` 1회 허용.

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> -m 'not integration' + uv run pytest -q tests/architecture. 전체 스위트·integration 금지. 자기점검 — modules/* 가 fastapi/sqlalchemy/subprocess 를 import 하지 않는가 · entrypoints 가 platform 직접 import 안 하는가 · 스키마 변경은 reset_demo 안인가. 검증 1회
```

- WP-003 Phase 1~3 검증 항목 전부 테스트: memo `at_ms` 채움 · `can_write_memo` 셋 상태 · transcript 열람 축(비참석 404·공유 200·scheduled 빈 배열) · 비소유자 메모 403→404/409 · 진행 중 아닐 때 409 · 메모가 줄로 쌓임 · 웜스타트 실패해도 회의 정상 · 세션 ref 저장·resume 사용 · 트리거 셋(분량·안건 전환·시간) · 동시 실행 1 · 스키마 위반 시 직전 성공분 유지 · 없는 task_id 강등 · 전량 교체(사람 안건 불변) · push 호출 · `/end` 뒤 미발행.

## 9. 완료 보고 — **문구 변경 금지**

> ⚠ 핸들은 dispatch preamble 값 우선.

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: WP-003 메모 + AI 배치" \
  --body "변경 파일 / 구현 요약(메모 API·세션·트리거·도구 레지스트리·스키마·적재·push) / 검증 수치 / 계약 준수 / WP-004 인계 / reset-demo / 미결(OQ 수치)"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — WP-003. 상세는 인박스." --enter
```
