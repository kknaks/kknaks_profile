WP-004 완료. `/end` 뒤 durable job 이 **같은 provider 세션**으로 합성을 돌려 두 트랙을 최종 줄로 합치고 다음 할 일·제목 후보·근거를 세우며, 승격은 언제나 업무 요청으로 나가고 출처 두 열이 수락 시 업무로 옮겨지며, 마지막 저장분을 HTML 로 내보낸다. 검증 305 passed / 0 failed (회의 107 + **work 회귀 124 · 실패 0** + architecture·영향 74, -m 'not integration'), make reset-demo 새 스키마로 성공. 코디 추가분 셋(F-A 스키마 결속 · W-b 지연 트리거 · W-c close code 단정)도 같은 트리에서 처리했고, 남은 것은 OQ-316/308/313 과 실제 Codex 1회 확인이다.

## 변경 파일 (신규 7 · 수정 17)
신규: modules/meetings/finalize.py(최종 스키마·파서·검증·프롬프트·중복 판정) · finalize_service.py(파이프라인) · export.py(HTML) · schemas/ai_final_output.json · bootstrap/meeting_worker.py · entrypoints/meeting_worker.py · tests/contract/test_meeting_finalize.py(28건)
수정: modules/meetings/{application,batch,batch_service,domain}.py · modules/jobs/domain.py · modules/ax_execution/ai.py · modules/work/requests.py · platform/{persistence,meetings,work_tasks,codex_cli}.py · bootstrap/{application,settings}.py · entrypoints/http.py · Makefile · docs/domain-model.md · tests/contract/{test_meeting_memo_batch,test_meeting_stream}.py

## 구현 요약
- **파이프라인**: `/end` 가 전이 + `meeting.finalize` 잡 등록 후 즉시 응답(테스트가 「응답 시점에 provider 미호출」을 고정). worker 가 claim → 합성 → 커밋 → 배달 완료. 시도 상한 3, 그래도 안 되면 `failed` + `failure_reason`. `POST /finalize` 는 「실패」에서만(그 밖 409) 상태를 되돌리고 잡을 다시 건다.
- **세션**: `ai_session_ref` 로 resume. 없으면 **콜드 스타트**(확정 발화 전량 적재) 폴백이고 `meeting_finalize.cold_starts` 가 센다. 배치와 **같은 lock** 을 잡는다 — 회의당 provider 호출은 언제나 하나다.
- **검증**: 스키마 → **사람 안건 전수 보존**(빠뜨림·병합이면 그 시도 실패) → 근거 구간 밖이면 그 근거만 강등 → 출처 문장 스탬프 → 이미 있는 업무면 후보 제외 → 기한 세 갈래(②는 서버가 다음 회의 전날로 채운다).
- **적재**: 한 트랜잭션 — final 줄 전량 교체 · todos 전량 교체(**승격된 것은 유지**, 테스트로 고정) · concluded · title_candidate(제목이 이미 있으면 쓰지 않는다) · last_saved_at · status done.
- **승격**: `POST …/todos/{id}/promote` → 업무 요청 하나. 모달 값 우선, 없으면 후보값. `work_requests.source_meeting_id·source_agenda_id` → 수락 시 `tasks` 로 복사 + `origin_kind="meeting"`. 중복 승격 409, 승격된 후보 삭제 409.
- **동시성**: `PATCH /agendas/{aid}` 가 `expected_last_saved_at` 을 받아 안건 단위로 판정하고, 불일치면 409 + `{"code":"meeting_agenda_stale","current":<지금 안건>}`. 안건 응답에 `last_saved_at` 을 실었다.
- **내보내기**: `GET …/export?format=html`. pdf·docx 는 422(데모 범위 밖). 링크·내부 값 없음을 테스트가 고정.

## 코디 추가분
- **F-A (스키마가 provider 에 걸리지 않던 것)**: `AiConversationRequest.output_schema: dict|None` 추가 → `codex_cli.converse` 가 `generate` 와 같은 모양으로 임시 파일을 써 `--output-schema` 를 붙인다. 배치는 `OUTPUT_SCHEMA`, 합성은 `FINAL_OUTPUT_SCHEMA` 를 건다(웜스타트는 「준비됨」 한 마디라 걸지 않고 형식만 예고). 프롬프트에도 「아래 스키마의 JSON 하나로만 답하라」 + 스키마 본문을 넣었다. 테스트 넷: 인자에 `--output-schema` 가 붙는지 · 안 걸면 안 붙는지 · 배치 요청의 `output_schema is OUTPUT_SCHEMA` · 프롬프트에 스키마와 지시문이 실리는지.
- **W-b**: 실행 중 도착한 트리거의 사유를 기억했다가 배치가 끝나는 자리에서 그대로 갚는다(90초 타이머를 기다리지 않는다). 테스트가 「도는 중 안건 전환 → 끝난 뒤 두 번째 제출 · 타이머 미무장」을 고정.
- **W-c**: 소유자 게이트 테스트가 close code `4409` 와 reason `not_meeting_owner` 를 단정한다.

## FE 인계 (경로·필드)
- `POST /api/meetings/{id}/finalize` → MeetingDetail(「실패」에서만, 그 밖 409).
- `POST /api/meetings/{id}/todos/{todoId}/promote` body `{assignee_id, title?, description?, due_date?, checklist?}` → 201 Todo(`linked.work_request_id` 참). 중복 409.
- `DELETE /api/meetings/{id}/todos/{todoId}` → 204. 승격된 것은 409.
- `GET /api/meetings/{id}/export?format=html` → `text/html` 첨부. 그 밖의 format 은 422.
- `MeetingDetail.meeting` 에 **`title_candidate`**(ISO 아님, 글자|null)와 **`failure_reason`** 추가. 제목이 비면 `title_candidate` 를 머리 편집의 기본값으로 놓고, 사람이 저장해야 제목이 된다.
- `Agenda` 에 **`last_saved_at`** 추가. 줄 저장은 `PATCH /agendas/{aid}` 에 `expected_last_saved_at` 을 함께 보내고, 409 `detail.code == "meeting_agenda_stale"` 이면 `detail.current` 로 화면을 갱신한다.
- Todo 는 WP-001 의 여덟 필드 그대로. **담당자 칸이 없다** — 승격 모달의 담당은 비어서 열린다.

## 발견한 것 (보고 필요)
- **팀장 역할에 `work_request.create` 가 없다.** 이 조직 카탈로그에서 팀장은 요청을 *받는* 역할이라, 참석자여도 승격이 403 이다. SPEC §9-5 는 「승격 진입점은 참석자」라 말하지만 실제 게이트는 SPEC-001 의 capability 다 — 테스트에 그대로 고정해 두었다. **역할 카탈로그를 고칠지는 planner/코디 판단**이고 나는 건드리지 않았다.
- 승격에서만 자기 자신 배정을 연다: `WorkRequestApplication.create(allow_self_assignment=True)` 를 회의 경로만 넘긴다. 기본값은 그대로라 기존 work 계약(교차 조직 배정 422)은 회귀 0.

## 미결
- `OQ-316`(「같은 일」 기준) — 제목 정규화 일치/포함을 잠정으로 썼다. `finalize.is_already_work` 한 곳이다.
- `OQ-308`(메모 줄과 AI 줄이 어긋날 때) · `OQ-313`(제목 후보 실패 시 기본값) — 손대지 않았다. 후자는 후보가 없으면 그냥 「제목 없는 회의」로 남는다.
- 합성 시도 상한 3 은 잠정값(`finalize.FINAL_ATTEMPTS`).
- 실제 Codex/MCP 호출은 하지 않았다(대역만). 실물 배치·합성 1회 확인은 코디 몫이다.
- 커밋·push·PR 하지 않았다. `frontend/` 는 읽기만 했다.