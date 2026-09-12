# 코드 검수 4 — WP-003 메모·AI 배치 + 검수 3 F1 해소

- 작성: 2026-09-10 / `reviewer_code` (read-only · 검수 1~3 과 같은 세션)
- 범위: `git diff bfc9770..HEAD` — 커밋 하나(`80dd097`), 18파일 **+1,832 / −53**. frontend 는 이 커밋에 없다.
- **격리본으로 읽고 돌렸다.** 검수 도중 WP-004 워커가 워킹트리를 고치기 시작했다(`modules/jobs/domain.py`·`platform/persistence.py` 수정 + `finalize.py`·`finalize_service.py`·`ai_final_output.json` 신규). 인용한 `파일:줄`과 검증 수치는 전부 `git archive HEAD` 격리본 기준이고 `git stash` 는 쓰지 않았다.
- **아무 파일도 고치지 않았다.** 워크트리·`.git` 변경 0.

---

## 0. 총평 — **FAIL — 재발주 필요 (BE 1건)**

검수 3 F1(업스트림 소유자 게이트)은 **깔끔하게 해소됐다** — `is_owner` 가 admission 에 실리고, 게이트가 오디오·provider **앞**에 서며(`connect_count == 0` 을 테스트가 단정), 소유자·비소유·공유 구독 셋을 한 테스트가 덮는다. 메모 API·D26 셋·웜스타트·트리거·레지스트리·강등·전량 교체도 브리프 §3 을 조목조목 지켰고, 코디의 실물 e2e 관측 10가지가 전부 코드와 맞는다. 테스트 23개가 WP-003 Phase 1~3 검증 15항목을 빠짐없이 덮고, 격리본에서 **90 passed** 다.

막는 것은 **하나**다 — **출력 스키마가 provider 에 걸리지 않는다.** `ai_batch_output.json` 은 서버 재검증에만 쓰이고, 모델은 **어떤 모양으로 답해야 하는지 들은 적이 없다**: `AiConversationRequest` 에 스키마 자리가 없고, 두 프롬프트 어디에도 JSON 이라는 말조차 없다. 실제 Codex 로 배치를 한 번이라도 돌리면 `parse_output` 이 전부 폐기해 AI 트랙이 영원히 비어 있을 공산이 크다. 테스트가 못 잡은 이유는 `BatchAgent` 대역이 유효한 JSON 을 그냥 돌려주기 때문이고, 코디 e2e 도 **웜스타트 성공까지만** 봤지 배치 산출물을 본 적이 없다. 원형(`meeting_batch_service.py:71`·`:321`)은 같은 파일을 `--output-schema` 로 **걸고** 재검증하므로, 이건 「의도된 차이」가 아니라 절반이 빠진 것이다.

---

## 1. 검수 3 F1 해소 — **PASS**

| 확인 | 근거 |
|---|---|
| `MeetingAdmission` 에 소유자 정보 | `modules/meetings/stream_service.py:87-93` `__slots__` 에 `is_owner` · `application.py:473-479` `is_owner=str(principal.id) == meeting.owner_id` |
| 비소유 upstream 4409 `not_meeting_owner` | `stream.py:29` `REASON_NOT_OWNER = "not_meeting_owner"` · `stream_service.py:140-144` |
| **오디오·provider 앞**에서 나는가 | **PASS** — 게이트가 `room.upstream` 검사(`:145`)와 `_serve_upstream`(`:150`)보다 **먼저** 선다. 테스트 `test_meeting_stream.py:212` 이 `connector.connect_count == 0` 으로 provider 를 열지 않았음을 단정한다(과금이 걸린 자리다) |
| 테스트 3 | `test_only_the_person_who_called_the_meeting_may_send_audio`(`:200-222`) 하나가 셋을 덮는다 — 비소유 참석자 거부(`:208-212`) · 소유자 upstream ready(`:216-219`) · 공유받은 사람 subscribe ready(`:220-222`) |
| subscribe = 참석+공유 유지 (D27) | `application.py:471` 이 `_can_read_detail` 그대로 — 축 변경 없음 ✓ |

> 소소한 관찰(문제 아님): `:210` 이 `pytest.raises(Exception)` 이라 close code·reason 을 단정하지는 않는다. 실질은 `connect_count == 0` 이 잡고, `4409 not_meeting_owner` 자체는 코디 e2e 가 실물로 확인했다.

---

## 2. 메모 API — **PASS**

| 확인 | 근거 |
|---|---|
| 경로 | `entrypoints/http.py:773` `POST /api/meetings/{meeting_id}/agendas/{agenda_id}/lines` — **안건이 경로에** (SPEC §6-8) |
| body `{text}` | `http.py:298-302` `WriteMemoRequest` · `extra="forbid"` · 시각을 싣지 않는다 |
| 201 Line | `status_code=201`(`:773`) → `_line_view`(`application.py:881-891`) `{line_id, track, order, text, author, at_ms, evidence}` |
| track memo · author=member_id · at_ms 서버 계산 | `application.py:333-335` `track="memo", author_id=str(principal.id), at_ms=self._elapsed_ms(meeting)` — 클라이언트 시계를 믿지 않는다 (§6-5) |
| 게이트 만든 사람 | `:321-322` → `MeetingAccessDenied` → **404**(존재 숨김) ✓ 코디 e2e 「비소유 메모 404」와 일치 |
| 게이트 in_progress | `:323-324` → `MeetingStateConflict` → **409** ✓ 코디 e2e 「scheduled 메모 409」·「`/end` 뒤 메모 409」 |
| 게이트 안건 소속 | `:330-332` `self._repository.agenda(meeting, agenda_id)` — 회의 범위 질의라 남의 안건은 404 |
| 422 빈 문자열 | `WriteMemoRequest.text: Field(min_length=1)` → pydantic 422 ✓ (application 이 `:326-327` 로 한 번 더) |
| FE `api.ts` 와 모양 일치 | `frontend/src/api.ts:831-836` `addMeetingMemoLine(meetingId, agendaId, text)` → 같은 경로·`{text}`·`MeetingLine` 반환 ✓ |

---

## 3. D26 — **PASS** (FE 소비는 미착수 → §9 이월)

| 확인 | 근거 |
|---|---|
| 모든 Line 에 `at_ms`, ai/final 은 null | `_line_view`(`application.py:881-891`)가 모든 줄에 싣고, `replace_ai_track` 의 AI 줄은 `at_ms` 를 주지 않아 null(`:655-657`), 합성 줄도 같다 |
| `GET /transcript` 열람 축 | `application.py:509` `self._readable(...)` — 상세와 **같은 축**(참석·공유). 비참석 404 ✓ · 공유 200 ✓ (테스트 `test_meeting_memo_batch.py:215`) |
| scheduled 는 빈 배열(404 아님) | `_readable` 이 상태를 보지 않는다 → 빈 목록. 테스트 `:238` `test_a_meeting_that_has_not_started_answers_an_empty_transcript_rather_than_a_missing_one` ✓ 코디 e2e 「transcript 200 `{items:0, memos:1}`」 |
| 응답 키 | `:510-530` `items:[{id, speakerLabel, atMs, endMs, content}]` · `memos:[{line_id, agenda_id, text, author, atMs}]` — 브리프 §3 D26② 문자 그대로(메모 쪽 혼합 표기도 계약대로) ✓ |
| `can_write_memo` | `application.py:830` `str(principal.id) == meeting.owner_id and status is IN_PROGRESS` ✓ 테스트 `:183` · 코디 e2e 「start 뒤 true」 |
| `started_at` | `application.py:833` `_iso(meeting.started_at)` ✓ |
| **FE viewModels 와 충돌 없음** | **PASS** — BE 는 필드를 **더하기만** 했고 FE 타입은 초과 키를 무시한다. `npx tsc` 를 깨뜨릴 것이 없다 |

---

## 4. 웜스타트·세션 — **PASS**

| 확인 | 근거 |
|---|---|
| `/start` 뒤 백그라운드 | `batch_service.py:155-161` `launch_warm_start` — 스레드만 띄우고 즉시 돌아온다. 「기다리면 회의 시작이 provider 를 기다리게 된다」 |
| 실패해도 회의 정상 | `:173-175` — 세션 참조가 없으면 로그 한 줄, 배치만 안 낸다. 테스트 `:267` |
| 세션 참조 저장 방식 | `persistence.py:392-400` `meeting_ai_sessions` — `provider_session_ref` + `persona_id` + `opened_at`, 회의당 유니크(`:393`). 현행 `conversation_provider_session_references` 와 **같은 결**(회의 하나에 참조 하나) ✓ |
| 첫 turn 이 맥락 | `batch.py:117-163` `build_warm_start_prompt` — 회의 정보·안건·참석자·이어진 이전 회의. **참석자 이름을 싣지 않는다**(`:121`, WP Pre-deploy) ✓ |
| `/end` 뒤 세션 유지 | 닫는 코드가 없다 — `grep` 상 `meeting_ai_sessions` 삭제 경로 0. WP-004 가 같은 세션을 쓴다 ✓ |
| 코디 e2e 「실제 Codex 웜스타트 성공, `meeting_ai_sessions` 1행」 | 위 경로와 일치 ✓ |

---

## 5. 트리거·동시성 — **PASS**

| 확인 | 근거 |
|---|---|
| 600 / 80 / 90 이 상수 한 곳 | `batch.py:27` `BATCH_CHARS=600` · `:29` `BATCH_SWITCH_MIN_CHARS=80` · `:31` `BATCH_MAX_WAIT_SECONDS=90` — 서비스는 주입으로만 받는다(`batch_service.py:101-103`). 테스트 `:532` 가 수치 자체를 고정 |
| 안건 전환 <80자 생략 | `batch_service.py:195-196` · 테스트 `:300` |
| 회의당 lock 1 | `:231-233` `lock.acquire(blocking=False)` — 잡혀 있으면 **기다리지 않고 돌아간다**. 테스트 `:309` |
| 실행 중 트리거 병합 | `:186-187` 실행 중이면 아무것도 안 하고, `:238-240` 이 끝난 뒤 미처리가 남아 있으면 타이머를 다시 건다 → 「끝난 뒤 커진 구간으로」(SPEC §7.1 동시성) ✓ |
| 커서가 실패 시 되돌아가나 | **PASS** — `_record`(`:287-298`)는 `record_run` 만 남기고 커서를 올리지 않으며, `batch_input` 의 커서는 `succeeded_batch_cursor`(`application.py:595`)다. 즉 실패·폐기 구간은 다음 배치에 합쳐진다. 테스트 `:332`·`:501` |
| provider 호출이 트랜잭션 밖 | `:242-258` — ① `load_batch_input`(tx 닫고 나옴) → ② `run_batch`(tx 밖) → ⑤ `replace_ai_track`(새 tx) ✓ |

> 관찰(문제 아님, §9 이월): 실행 중 도착한 **안건 전환** 트리거는 기억되지 않는다 — 끝난 뒤 분량이 모자라면 타이머(최대 90초)까지 기다린다. SPEC §7.1 동시성 문구는 충족한다.

---

## 6. MCP·레지스트리 — **PASS**

| 확인 | 근거 |
|---|---|
| persona = 만든 사람 | `meeting_ai_sessions.persona_id`(`persistence.py:399`, 주석이 `OQ-315` 잠정값임을 밝힌다) → `batch_input` 이 그대로 싣고(`application.py:607`) → `AiDelegatedToolContext(principal_id=persona_id)`(`bootstrap/application.py:324-326`). 현행 MCP persona 바인딩 규칙 그대로 ✓ |
| allowlist 가 설정에서 | `settings.py:16-19` `AX_MEETING_AI_TOOLS`(쉼표) · `:49` 필드 · `:54-56` `meeting_ai_tool_registry` = 최소 넷 + 설정분, **넷이 먼저**(프롬프트가 그 순서로 읽힌다) ✓ SPEC §7.2-3 「바닥이지 천장이 아니다」 |
| 도구 4개가 read-only | `entrypoints/mcp.py` `task_list`(`:921`) · `project_list`(`:832`) · `meeting_get`(`:822`) · `member_list`(`:843`) — **넷 다 `annotations=_READ_ONLY_TOOL`** ✓ 테스트 `:370` |
| 쓰기 도구 노출 0 | `codex_cli.py:277-280` 이 `mcp_servers.scax.enabled_tools=[…]` 로 좁힌다 — 「부르지 마라」가 아니라 **주지 않는다**. 테스트 `:352` |
| env 값·키 인용 | `modules/`·`bootstrap/` 전수 grep **0건** ✓ |

> 관찰: 도구 필터가 **Codex CLI 의 `enabled_tools` config** 에 있다(MCP 서버는 여전히 전부 등록한다). 어댑터가 서버측 조립물이라 클라이언트가 뒤집을 수 없으므로 §7.2-3 구현으로 유효하다 — 다만 필터의 신뢰 기반이 CLI 라는 점은 기록해 둔다.

---

## 7. 스키마·검증·적재 — **FAIL (F-A)**

| 확인 | 결과 |
|---|---|
| strict 규격 | **PASS** — `schemas/ai_batch_output.json` 모든 object `additionalProperties:false`(`:6`·`:14`·`:28`·`:38`), properties 전 키가 required(`:7`·`:15`·`:29`·`:39`), 선택은 nullable(`agenda_id` `:19` · `task_id` `:48`). 제목 후보·todo 키 **없음** ✓ |
| 위반 시 전체 폐기 + 직전 성공분 유지 | **PASS** — `batch.py:64-72` 부분 파싱 없음 → `batch_service.py:261-265` `STATUS_DISCARDED` 로 접고 적재하지 않는다. 테스트 `:397`·`:536` |
| task_id 강등 | **PASS** — `batch.py:101-102`, 화이트리스트는 **검사 시점**에 읽는다(`bootstrap/application.py:261-267`) — 제출 뒤 생긴 업무를 도구로 보고 가리킨 것은 올바른 참조다. 테스트 `:417` |
| evidence 강등 | **PASS** — `batch.py:103-106` 구간 밖 span 만 떼고 본문은 산다. 테스트 `:432` |
| 전량 교체에서 사람 안건 제목·출처 불변 | **PASS** — `application.py:642-653`: `replace_track(meeting,"ai")` 가 track ai 줄 + **source="ai" 안건**만 지우고(`platform/meetings.py:452-474`), 매칭된 기존 안건은 줄만 매단다. 20개 상한도 지킨다(`:649-650`). 테스트 `:441` |
| 트랜잭션 하나 | **PASS** — `bootstrap/application.py:289-293` |
| provider 호출이 트랜잭션 밖 | **PASS** — §5 |
| push 페이로드가 FE `ai.batch` 기대와 일치 | **PASS** — `bootstrap/application.py:297-300` 이 `agenda["lines"]` 를 `track == "ai"` 로 걸러 MeetingDetail Agenda 모양 그대로 민다. 테스트 `:483` |
| `/end` 뒤 미발행 | **PASS** — `application.py:589-591` 이 in_progress 가 아니면 `None`. 테스트 `:520` |
| **구조화 출력을 세션 안에서 강제** | **FAIL** — 아래 |

### F-A · FAIL — 출력 스키마가 provider 에 걸리지 않는다 (담당: BE)

- `modules/meetings/batch.py:20-22` — `OUTPUT_SCHEMA` 가 로드되지만 쓰이는 곳은 **`_validator` 하나**뿐이다. 전수 grep 결과 `OUTPUT_SCHEMA`·`SCHEMA_PATH` 는 그 파일 세 줄에서만 등장하고, 어디로도 나가지 않는다.
- `modules/ax_execution/ai.py:48-61` — `AiConversationRequest` 에 **스키마 자리가 없다**(`prompt`·`provider_session_ref`·`context_references`·`delegated_tool_context`·`seed_references`·`recent_exchanges`·`asked_at`·`timezone_name`).
- `platform/codex_cli.py:412` — `--output-schema` 는 `_arguments`(= `generate` 경로)에만 붙는다. `_conversation_arguments`(`converse` 경로)에는 없다.
- `bootstrap/application.py:317-328` `_converse` — 배치가 부르는 자리인데 스키마를 넘길 인자 자체가 없다.
- **프롬프트에도 없다.** `build_warm_start_prompt`(`batch.py:117-163`)와 `_BATCH_INSTRUCTIONS`(`:166-173`)를 통독했다 — 필드 이름(`agenda_id`·`source`·`evidence`·`task_id`)을 산문으로 언급할 뿐, **JSON 으로 답하라는 말도, 스키마도, 예시도 없다.** 웜스타트는 「준비됨」이라고만 답하라로 끝난다.
- 즉 **모델은 어떤 모양으로 답해야 하는지 들은 적이 없고, provider 도 강제하지 않는다.** 실제로 돌리면 `parse_output`(`batch.py:67-72`)이 「출력이 JSON 이 아닙니다」로 매 배치를 `STATUS_DISCARDED` 처리하고 AI 트랙이 끝내 비어 있을 공산이 크다.
- 어긋난 기준:
  - SPEC §7.2-6 — 「**구조화 출력은 세션 안에서 스키마로 강제한다** — 대화로 돌아도 줄 증분과 후보는 정해진 모양으로만 나온다」
  - WP-003 Phase 2 검증 — 「대화 세션에서도 출력이 스키마를 벗어나지 못한다」
  - 브리프 §3 「출력 스키마(strict …)」
  - **자기 docstring** `batch.py:5` — 「스키마는 파일 하나다 — **provider 에 그대로 걸고** 서버가 같은 파일로 다시 검증한다」. 코드가 그 문장의 앞 절을 하지 않는다.
- **원형과 대조 — 「의도된 차이」가 아니다.** `meeting_batch_service.py:71` 이 「출력 스키마 — codex `--output-schema` 와 재검증이 **같은 파일**을 본다」고 적고 `:321` 이 실제로 `output_schema=OUTPUT_SCHEMA` 를 제출 호출에 넘긴다. 이쪽은 그 절반(재검증)만 옮겨 왔다.
- **테스트·e2e 가 못 잡은 이유**: `BatchAgent` 가 포트라 테스트는 대역이 **이미 유효한 JSON** 을 돌려준다(`test_meeting_memo_batch.py` 의 fake agent) — 프롬프트·provider 경로를 타지 않는다. 코디 e2e 도 **웜스타트 성공까지만** 확인했고 배치 산출물을 본 적이 없다.
- **고칠 방향 한 줄**: `AiConversationRequest` 에 `output_schema: dict | None` 을 더하고 `codex_cli._conversation_arguments` 가 그것을 `--output-schema` 로 붙인다(원형과 같은 모양). 프롬프트에 스키마를 박는 것은 차선이다 — 강제와 검증이 같은 파일을 보는 구조가 깨진다.
- **검증 제안**: 대역이 아니라 **실제 Codex 로 배치 한 회차**를 돌려 `meeting_batch_runs` 가 `succeeded` 인지 보는 것이 이 결함을 잡는 유일한 관측이다.

---

## 8. 경계·회귀 — **PASS**

| 확인 | 결과 |
|---|---|
| `modules/*` 가 fastapi·mcp·sqlalchemy·subprocess import | **0건 ✓** (`batch.py`·`batch_service.py` 포함 — 새 모듈 둘 다 포트로만 말한다) |
| reset_demo 밖 스키마 변경 | `create_all` 은 `bootstrap/reset.py:20` 하나뿐 ✓. 새 표 `meeting_ai_sessions`(`persistence.py:392`)·`meeting_batch_runs`(`:403`)가 `Base` 하위라 reset 이 만든다 |
| 검증 재현 (격리본) | `pytest -q tests/contract/test_meeting_core.py tests/contract/test_meeting_stream.py tests/contract/test_meeting_memo_batch.py tests/architecture -m 'not integration'` → **90 passed** (38.45s) |
| 리포트 주장 vs 코드 | 「strict 스키마」는 파일로는 참이나 **provider 강제가 없다**(F-A) — 리포트·docstring 이 주장하는 「provider 에 그대로 걸고」가 코드에 없다. 그 밖의 주장은 코드와 일치 |

**WP-003 Phase 1~3 검증 15항목 — 전부 테스트로 덮임** (Phase 1: `:162`·`:162`·`:201`·`:215`·`:183` / Phase 2: `:267`·`:332`·`:370`·**F-A**·`:309`·`:501` / Phase 3: `:397`·`:417`·`:441`·`:432`). Phase 2 의 「대화 세션에서도 출력이 스키마를 벗어나지 못한다」만 **대역이 유효 JSON 을 돌려주는 것으로 대신하고 있어 실질이 비어 있다**(F-A).

경고 2건은 starlette deprecation — **무관·기존 부채**.

**워킹트리 귀속**: 실행 직전 `git status` 에 WP-004 진행분 5건(`modules/jobs/domain.py`·`platform/persistence.py` 수정, `finalize.py`·`finalize_service.py`·`ai_final_output.json` 신규)이 떠 있었다. 격리본으로 돌렸으므로 **90 passed 는 HEAD 의 수치**다.

---

## 9. WARN 이월

| # | 자리 | 내용 | 담당 |
|---|---|---|---|
| **W-a** | `frontend/src/viewModels.ts` | D26 셋(`at_ms`·`can_write_memo`·`started_at`)이 **FE 타입에 아직 없다.** BE 는 계약대로 냈으니 WP-003 결함이 아니다. 다만 `MeetingDetailPage.tsx:807` 이 메모 시각을 **`Date.now() - startedAtMs`** 로 자체 계산한다 — SPEC §6-5 「클라이언트 시계를 믿지 않는다」가 서버 `at_ms` 를 쓰라고 한 자리다. 다음 FE 발주에서 세 필드를 소비하면 닫힌다 | FE |
| **W-b** | `batch_service.py:186-187`·`:238-240` | 실행 중 도착한 **안건 전환** 트리거가 기억되지 않는다 — 끝난 뒤 분량이 모자라면 타이머(최대 90초)까지 기다린다. SPEC §7.1 동시성 문구는 충족 | 코디 판단 |
| **W-c** | `test_meeting_stream.py:210` | 소유자 게이트 테스트가 close code·reason 을 단정하지 않는다(`pytest.raises(Exception)`). 실질은 `connect_count == 0` 이 잡고 코디 e2e 가 `4409 not_meeting_owner` 를 실물 확인 | BE(선택) |
| **W-d** | `codex_cli.py:277-280` | 도구 필터가 CLI 의 `enabled_tools` config 에 산다(MCP 서버는 전부 등록). 서버측 조립물이라 유효하나 신뢰 기반이 CLI 라는 점 기록 | — |
| ~~W9~~ | `viewModels.ts:751` | **해소** — `bfc9770` 이 `author: string \| null` 로 고치고 `MeetingDetailPage.tsx:399` 가 `memo.line.author ? personName(…) : ""` 로 갈랐다 | ✅ |

---

## 10. 재발주 요약

| # | 담당 | 무엇 | 크기 |
|---|---|---|---|
| **F-A** | BE | `AiConversationRequest.output_schema` 추가 + `codex_cli._conversation_arguments` 가 `--output-schema` 로 붙인다(원형 `:321` 과 같은 모양) · 실제 Codex 배치 1회차로 `succeeded` 확인 | 소~중 |
| W-a | FE | D26 세 필드 소비(서버 `at_ms` 로 스크립트 시각 축 전환) | 소 |
| W-b·W-c | 코디/BE | 선택 | — |
