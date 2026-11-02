# [backend] WORK-011 Phase 1~2 — 배치 입력은 발화뿐 · 스키마 한 벌 · AI 트랙 전량 교체

너는 **task-management `backend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`). **WORK-009(MCP · 토큰) · WORK-010(웜스타트)이 들어와 있다** — `git log -3` 로 확인. 웜스타트가 이미 도구 목록·용어 다섯을 심어 두므로 배치 프롬프트는 그것을 전제로 짧다.

문서는 전부 **코디 워크트리 절대경로 · 읽기 전용**이다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-011-meeting-live.md             ← 네 빌드 계획. Phase 1 · 2 만(3 · 4 는 프론트 — 다른 발주)
                                                  Code Surface · Internal Interface(스키마 소유 · _parse_output 시그니처 · _persist · 과도기 규칙) · Phase 검증
  20-spec/spec-007-meeting-live.md §4          ← 「AI 배치 계약」 — 배치 입력 표 · 배치 출력 블록 · **검증 순서 0~5** · WS ai.batch 행 · AI 트랙 항목 형태
  20-spec/spec-007-meeting-live.md §5          ← 배치 트리거 1000자 · 전량 교체 · 검증 두 층
  10-decision/decision-003-meeting-notes.md    ← §4 배치 입력 · 배치 갱신 방식 · §7 실패 넷 · §STT 배치 입출력
  40-architecture/backend/README.md            ← §5-2 · §7 · §8-3 · §12 테스트 6 · 7 · 7-a
  40-architecture/database/domains/meeting.md  ← M-5-b · M-6 · M-7 · M-15 · M-16
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/ai-prompt-draft.md §B   ← 배치 프롬프트 초안 — **「조회 순서」 절만 가져온다.** 요청 문장은 계약(「AI 트랙 전체를 다시 정리해라」)이 이긴다(WP §Open Issues)
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/Meeting flow.md §2-3   ← MF-49 · 50 · 51 · 52 · 53
```

## 1. 범위 — Phase 1 · 2 (백엔드만)

**먼저 WORK-010 검수 WARN 넷을 정리한다**(같은 파일 · 리포트 `orchestration/work/docs-v1/work010-review-report.md` §2):
① `meeting_batch_service.reset_state()` 가 웜스타트 `_tasks` 도 비운다(테스트 사이 누수) ② `tests/test_meeting_live_api.py` L18 죽은 import 둘(`WARM_SESSION_ID` · `FakeAgentGateway`) 제거 ③ 같은 파일 L85 `ai_session_id is None` 단언을 하네스가 아니라 MF-1 을 증명하는 형태로(훅 실행 전 None · 실행 후 값) ④ `test_meeting_start_warm.py` 프롬프트 needle 이 bare `project` · `tasks`(단, `list_tasks` 는 도구 이름이라 제외) 를 잡게.

```
Phase 1  ai_schemas/meeting_batch.json → meeting_notes.json (git mv + 재작성 · 한 벌 · headline/termCorrections/payload nullable)
         _BatchInput 셋(meeting · seq · blocks) · _load_input 컨텍스트 제거 · build_batch_prompt 재작성 · _OutputAgenda 신설
         _parse_output(output, *, human_agenda_ids, last_end_ms, fill_final=False) · _demote_if_needed(line, allowed_task_ids, *, meeting_id)
         config.meeting_batch_chars 600 → 1000 · .env.example
Phase 2  _persist = DELETE(줄→안건) + INSERT 한 함수 · _run_once 에서 검증 통과 뒤에만 · push_ai_batch(agendas 트리 하나) · AiBatchMessage/AiBatchFrame 중첩
         run_final · _load_final_input · build_final_prompt 는 **컴파일만 되게** 최소 수정(과도기 규칙 — 의미는 WORK-012)
```

**Phase 3 · 4(프론트)는 다른 워커다. `app/front/` 를 건드리지 마라.**

## ⛔ 2. 하지 말 것 · 이미 있는 것

```
build_warm_start_prompt · launch_warm_start   WORK-010 것. 건드리지 마라
run_final · _load_final_input · build_final_prompt · _agenda_rows · meeting_finalize_service · meeting_merge_service   WORK-012 가 갈아엎는다. **지우지 마라** — _BatchInput 이 줄어 깨지는 곳만 「함수 안에서 직접 조회」로 최소 수정
build_codex_options · meeting_token 전달   WORK-009 것. 부르기만
검증 전에 DELETE 하지 마라   — 실패 시 직전 성공분이 사라진다(M-7). 검증 0~4 를 다 지난 뒤 _persist 한 트랜잭션
부분 파싱 금지   스키마 위반 = 전체 폐기(discarded) · 행 0
except Exception · 임의 재시도 · 조용한 기본값 금지
```

## 3. 계약

- **스키마 파일은 하나** — `ai_schemas/meeting_notes.json`. 모양 = `{headline, termCorrections, agendas[{humanAgendaId, title, lines[{kind, content, detail, evidence, taskId, payload}]}]}`. `aiAgendaId` · `newTitle` · `items` 없음. WORK-012 가 같은 파일을 `output_schema` 로 건다
- **배치 입력 = 미처리 확정 블록 하나**(`{speakerLabel, atMs, endMs, content}`) + 「이번 구간을 반영해 AI 트랙 전체를 다시 정리해라」 + 조회 순서 지시(`list_agendas` → `get_agenda` → 업무 가리킬 때만 `list_tasks` · `get_task` · `list_work_types`). 안건 · 줄 · 업무 · 유형 · 화이트리스트를 **싣지 않는다**
- **검증 순서**(SPEC-007 §4 표) — 0 `ai_session_id` 없으면 **조용히 미제출**(지금 `_run_once` 가 RuntimeError 를 내는 것을 SPEC 검증 0 대로 「평가만 하고 제출 안 함 · 화면 표시 없음」으로 — WORK-010 미결 (5)) / 1 워커 오류·120초 → failed · 구간 다음으로 / 2 스키마 위반 → discarded · 행 0 · AI 트랙 직전 그대로 / 3 업무 참조 사후 검사(검사 시점 `task_repository.list_meeting_context` 조회) → 그 줄만 action 강등 · payload 떼기 / 4 회의 중 payload · headline · termCorrections **버림**(`null`) / 5 전량 교체 한 트랜잭션 → seq 증가 → 커밋 후 push
- **`_persist(session, meeting_id, agendas)`** — DELETE(줄 → 안건) + INSERT. `humanAgendaId` 있으면 `source_agenda_id` = 그 id · 제목은 사람 안건 제목 복사, 없으면 NULL
- **WS `ai.batch`** = `{type, seq, agendas:[AgendaItem…]}` — 줄이 `lines[]` 안에 중첩. 상세 응답 `agendas.ai` 와 **같은 직렬화 함수**
- **`meeting_batch_chars` = 1000**

## 4. allowed_paths

```
app/back/   .env.example
```
`app/front/` · 문서 · compose · `app/mcp/` 금지.

## 5. 검증

WP §Execution Phase 1 · 2 의 검증 체크리스트 전부. 특히

- **BE §12 6** — 스키마 위반 결과 → 줄 0건 · `discarded` · 구간 다음 배치 · **AI 트랙 직전 성공분 그대로**
- **BE §12 7** — 회의 프로젝트 밖 `taskId` → 그 줄만 `action` 강등 · 본문 유지 · 회의 중 `payload` 미저장(`null`)
- **BE §12 7-a** — 두 번째 배치가 첫 배치의 AI 안건·줄을 **남기지 않고**, 두 번째가 검증에 떨어지면 첫 것이 그대로
- 제출 payload(프롬프트 문자열)에 `humanAgendas` · `tasks` · `taskWhitelist` · 안건 제목 · 업무 제목이 **0건**(테스트 단언)
- 트리거 1000자 경계 테스트(999 미제출 · 1000 제출)
- `run_final` 계열이 **import 되고 호출 가능**(컴파일)하되 동작은 옛것 — `test_meeting_finalize.py` 가 여전히 통과
- **정적 검사**: `_persist` 밖에서 `delete_by_track` · `delete_agendas_by_track` 을 부르는 곳 0건 · `_load_input` 안에 `list_agendas_by_track` · `list_human_lines_since` · `list_meeting_context` 0건(grep 결과를 보고에)

```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1 && make test    # 전체 · Errors 0
```

막히면 30분 넘기지 말고 §9 (2) 로 물어라.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_fd9fc1ce-619d-4f87-b218-10dfaefaa275 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WORK-011 Phase 1~2" \
  --body "변경 파일 목록 / Phase 별 구현 요약 / 검증 결과(수치 · 정적 검사 grep) / 계약 준수 / 미결·주의점"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] backend 완료 — WORK-011 회의 중 백엔드. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] backend: <질문>" --enter`
