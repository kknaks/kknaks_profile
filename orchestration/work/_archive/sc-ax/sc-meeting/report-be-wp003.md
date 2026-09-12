WP-003 완료. 메모 트랙 API·`at_ms`·`can_write_memo`·`GET /transcript` 를 세우고, 회의당 provider 세션 하나를 웜스타트로 열어 MCP 도구 레지스트리를 붙인 배치가 트리거 셋으로 돌며 스키마로 강제한 출력을 검증해 AI 트랙 전량 교체 후 즉시 push 하게 했다. 검증 213 passed / 0 failed (memo·batch 23 + stream 21 + core 31 + mcp 16 + 영향 파일 + tests/architecture 15, -m 'not integration'), make reset-demo 새 스키마로 성공. 코디 추가분(검수 3 F1 업스트림 소유자 게이트)도 같은 트리에서 처리했고, 남은 것은 OQ-307 수치 실측과 WP-004 가 이어 쓸 세션이다.

## 변경 파일 (신규 4 · 수정 12)
신규: modules/meetings/batch.py(스키마·파서·강등·트리거 수치·프롬프트) · modules/meetings/batch_service.py(트리거·락·실행) · modules/meetings/schemas/ai_batch_output.json · tests/contract/test_meeting_memo_batch.py(23건)
수정: modules/meetings/application.py · modules/meetings/stream.py · modules/meetings/stream_service.py · platform/persistence.py · platform/meetings.py · platform/codex_cli.py · entrypoints/http.py · entrypoints/mcp.py · bootstrap/application.py · bootstrap/settings.py · docs/domain-model.md · tests/contract/{test_meeting_core,test_meeting_stream,test_mcp}.py

## 구현 요약
- **메모 API**: `POST /api/meetings/{id}/agendas/{agendaId}/lines` `{text}` → 201 Line(track memo). 게이트 = 만든 사람 · in_progress · 그 회의의 안건. 비소유자·비참석자는 404(존재 숨김), 상태 밖은 409, 빈 글자는 422.
- **D26 셋**: ① `Line.at_ms` — 메모 줄은 서버가 `now − started_at` 으로 채우고 ai/final 줄은 null. MeetingDetail 의 모든 Line 에 실린다. ② `GET /api/meetings/{id}/transcript` → `{items:[{id,speakerLabel,atMs,endMs,content}], memos:[{line_id,agenda_id,text,author,atMs}]}`, 열람은 참석·공유(상세와 같은 축), scheduled 는 404 가 아니라 빈 배열. ③ `can_write_memo`(만든 사람 && in_progress) ③-b `started_at`(ISO|null) 둘 다 MeetingDetail 머리에 추가.
- **세션(웜스타트)**: `/start` 커밋 뒤 백그라운드 스레드가 `converse`(session_ref=None)로 첫 turn 을 던지고 응답은 버린다. 참조는 `meeting_ai_sessions`(회의당 1행 · persona = 만든 사람). 열기 실패 = 로그 한 줄, 회의는 정상, 배치만 미제출.
- **트리거**: 확정 블록 적재(WP-002 `append_block`) → `transcript`, 메모 쓰기 → `agenda_switch`, 미처리가 남으면 `threading.Timer` 로 `timer`. 회의당 `threading.Lock` 하나 — 도는 중 트리거는 아무것도 하지 않는다. **배치 전체가 블로킹이라 이벤트 루프에 기대지 않는다**(요청 스레드에서도 WS 루프에서도 같게 돈다).
- **도구 레지스트리**: `settings.meeting_ai_tool_registry` = 바닥 넷 ∪ `AX_MEETING_AI_TOOLS`. `CodexCliMcpServer.enabled_tools` 로 `-c mcp_servers.scax.enabled_tools=[…]` 를 실어 **도구를 주지 않는 방식**으로 좁힌다(프롬프트로 「부르지 마라」 하지 않는다). 없던 `project_list`·`member_list` 를 조회 도구로 신설했고 `task_list` 에도 read-only annotation 을 달았다 — 넷 다 `read_only_hint=True` 를 테스트가 고정한다.
- **적재**: 스키마 위반 → 배치 전체 폐기(직전 성공분 유지) · 없는 task_id / 구간 밖 evidence → 그 줄만 강등 · 통과분으로 AI 트랙 전량 교체(사람 안건은 제목·출처 불변, AI 안건은 지우고 다시 세움) 한 트랜잭션 · 커밋 직후 `push_ai_batch_threadsafe`. provider 호출은 트랜잭션 밖이다.
- **커서**: `meeting_batch_runs.to_seq` 는 성공분만 전진 — 실패·폐기 구간은 다음 배치에 합쳐진다(테스트로 고정).

## 계약 준수
FE 가 소비하는 메모 API 모양·경로 그대로. 출력 스키마는 `{agendas:[{agenda_id,title,source,lines:[{text,evidence:[{from_ms,to_ms}],task_id}]}]}` 이고 strict 규격(모든 object additionalProperties:false · 모든 키 required · 선택은 nullable). 회의 중에 오면 안 되는 필드(제목 후보·todo)는 **스키마에 키 자체가 없다**. `/end` 뒤 새 배치 없음(진행 중이 아니면 입력이 None) · 세션은 닫지 않는다.

## 검수 3 F1 (업스트림 역할 게이트)
`MeetingAdmission.is_owner`(created_by == principal) 추가 → `role=upstream` 인데 소유자가 아니면 **오디오를 받기 전·provider 를 열기 전에** `4409 not_meeting_owner` 로 닫는다. subscribe 는 그대로 참석자+공유받은 사람(D27). 테스트: 참석자(비소유) upstream → 4409 이고 `connect_count == 0` · 소유자 upstream OK · 공유받은 사람 subscribe OK.

## WP-004 인계
- 세션 참조: `MeetingApplication.ai_session_ref(meeting_id)` → `str|None` (`meeting_ai_sessions.provider_session_ref`). 종료 합성이 **같은 세션**을 이어 쓴다.
- 스키마 파일: `backend/src/ax_workspace/modules/meetings/schemas/ai_batch_output.json`. 합성은 제목 후보·다음 할 일이 필요하므로 **다른 스키마**를 옆에 두면 된다 — 이 파일은 회의 중 전용이다.
- 커서: `MeetingApplication.unprocessed_transcript_cursor(meeting_id, after_seq=)` (WP-002) · `succeeded_batch_cursor` · `latest_succeeded_batch_seq`.
- 재사용 가능한 검증 함수: `batch.parse_output` · `batch.demote_line` · `application.replace_ai_track`(track 인자를 넓히면 `final` 에도 쓴다).
- 승격은 여전히 `meeting_todos.linked_*` 자리이고 지금은 채우는 코드가 없다.

## 미결
- **OQ-307 수치는 잠정값이다** — 600자 / 안건 전환(미처리 80자 미만이면 생략) / 90초. 상수는 `modules/meetings/batch.py` 한 곳이고 env(`AX_MEETING_BATCH_*`)로 갈아 끼운다. 실측 뒤 SPEC §13 을 닫을 수 있다.
- **OQ-315**: 도구 권한 범위는 「회의를 만든 사람이 보는 범위」를 잠정으로 썼다(persona = 소유자).
- OQ-304(정제를 이 경로에 걸지) · OQ-312(AI 안건과 사람 안건이 같은 주제일 때) · 세션이 300분을 견디는지 · 후보 최대 건수 — 손대지 않았다.
- 실제 Codex/MCP 호출은 하지 않았다(대역만). 실물 확인은 코디 몫이다.
- 커밋·push·PR 하지 않았다. `frontend/` 는 읽기만 했다.

## 그 밖
- 검증 중 이전 세션에서 남은 hung pytest 프로세스 다수가 머신을 붙들고 있어 **내가 띄운 것만** 정리하고 다시 돌렸다(코디 postgres 54329 는 건드리지 않았다). 최종 수치는 정리 뒤 깨끗한 2회 분할 실행의 합이다: 91 + 122.