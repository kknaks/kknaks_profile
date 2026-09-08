---
type: review
work: WORK-010
title: "WORK-010 검수 — `/start` 는 전이만 · 웜스타트는 컨텍스트 없이 백그라운드"
reviewer: reviewer
date: 2026-09-07
scope: "미커밋 변경 4 파일(back 2 · tests 2) + 신규 test_meeting_start_warm.py"
worktree: /Users/kknaks/orca/workspaces/task_management/docs-v1 (kknaksss/docs-v1 · HEAD 0b3f7b7)
verdict: "FAIL 0 · WARN 6 · 문서 공백 4"
---

# WORK-010 검수 리포트

**FAIL 0 · WARN 6 · 문서 공백 4.**
`tauri.conf.json` 은 범위 밖이라 보지 않았다. 테스트는 돌리지 않았다(코디 실측 — 595 passed). 앱 창 실측(SPEC-007 §6 AC)은 코디가 아침 항목으로 넘겼으므로 요구하지 않았다.

## 0. 축별 판정 한 줄

| 축 | 판정 | 한 줄 |
|---|---|---|
| 2-1 `/start` 트랜잭션 — 전이 + 토큰 INSERT · commit 0 | **PASS** | `meeting_service.py` 에 `commit()` 호출 0건 · 전이와 INSERT 가 한 트랜잭션 · 요청 안 외부 호출 0 · 훅은 커밋 성공 뒤에만 돈다 |
| 2-2 백그라운드 태스크 · 실패 처리 없음 | **PASS · WARN 2** | `create_task` 즉시 반환 · done 콜백 로그 하나가 전부 · `retry`/`attempt`/`warm_start_failed` 0건 · 토큰 없으면 미제출. 태스크 누수와 테스트 전용 헬퍼가 걸린다 |
| 2-3 프롬프트 — 컨텍스트 0 · 여섯 절 | **PASS · WARN 1** | 컨텍스트 키 0 · JSON 0 · 도구 7/7 정확 일치 · 여섯 절이 DEC-003 §8 문장과 맞다. 정적 단언 하나가 WP 문구보다 느슨하다 |
| 2-4 범위 준수 | **PASS** | 011·012 함수 diff 0 · finalize 무변경 · 프론트/compose/env/리비전 0. 삭제한 500 테스트는 **정말 뒤집힌 계약**이고 대체 테스트가 있다 |
| 2-5 테스트가 WP 검증을 덮나 | **PASS · WARN 3** | 32 테스트가 Phase 1·2 검증을 전부 덮고 **BE §12 8-a 는 문장 그대로** 있다. 단언 하나가 하네스 아티팩트고, 죽은 import 둘, 실측 캡처 미완 |

---

## 1. FAIL

**없다.**

브리프가 지목한 FAIL 조건 다섯을 전부 확인했다 — `commit()` 잔존 0 · 요청 안 외부 호출 0 · 실패 처리 갈래 0 · 프롬프트 컨텍스트 0 · 011/012 파일 변경 0.

---

## 2. PASS — 무엇을 확인했나

### 2-1. `/start` 트랜잭션 (MF-1 · BE §7 · SPEC-006 §5)

| 검사 | 결과 |
|---|---|
| ① `meeting_service.py` 의 `commit()` 호출 | **0건** — grep 이 잡는 것은 524·525 줄의 **docstring 문장**뿐이다. 파일 전체에 `.commit()` 호출식이 없다 |
| ① 전이 + 토큰 INSERT 가 한 트랜잭션 | `meeting_service.py:536` `start_recording()` → `:544` `issue_meeting_token()` → `:547` `register_after_commit()` → `:550` `build_detail()`. 사이에 커밋이 없다. **WORK-009 의 INSERT 줄이 유지됐다**(반환값을 안 쓰는 형태로만 바뀌었다 — 제출부가 `get_meeting_token()` 으로 읽으므로 맞다) |
| ② 훅 등록 · 커밋 안 되면 안 돎 | `api/deps.py:70-73` — `await session.commit()` **뒤**에만 `run_after_commit_hooks(session)` 가 온다. `AppError` 갈래는 `raise` 로 빠져 훅에 닿지 않는다. 테스트가 이를 두 방향으로 단언한다 — `test_meeting_start_warm.py:68`(훅 전 호출 0 → 훅 뒤 1) · `:84`(훅을 안 돌리면 **0건**) |
| ③ 요청 처리 중 게이트웨이 호출 0 · 응답 뒤 1 | `test_meeting_start_warm.py:76` `assert fake_agent.calls == []` → `:81` `assert len(...) == 1` |
| ④ 요청 안 외부 호출 0 (실측 7ms 근거) | `start()` 가 남긴 것은 UPDATE 1 · INSERT 1 · `register_after_commit`(리스트 append — `core/db.py:44-45`) · `build_detail`(DB 읽기)뿐이다. 훅이 부르는 `launch_warm_start` 도 `create_task` 한 줄이라 응답 경로에 대기가 없다. **codex 왕복이 요청 밖으로 완전히 나갔다** |

SPEC-006 §5 「`/start` 는 상태 전이만 하고 즉시 응답한다 … 외부 호출(Soniox·codex)을 이 요청 안에서 하지 않는다 … service 가 요청 안에서 commit 할 이유가 없다(W-1 해소)」와 **문장 단위로 맞는다.** M-12 「**`/start` 가 채우지 않는다** — 웜스타트 워커가 끝나면 UPDATE 한다」도 그대로다.

### 2-2. 백그라운드 태스크 · 실패 처리 없음 (MF-70 · BE §5-3 · §8-1)

| 검사 | 결과 |
|---|---|
| ① `launch_warm_start` 즉시 반환 · 예외 안 냄 | `meeting_batch_service.py:634-641` — `create_task` · `_tasks.add` · `add_done_callback` 셋뿐. `await` 없음. **강한 참조를 `_tasks` 가 잡는다**(태스크가 GC 로 사라지는 asyncio 함정을 피한다) |
| ② 실패 갈래 0 | `meeting_batch_service.py` · `meeting_service.py` 전수에서 `retry` · `attempt` · `warm_start_failed` · `re_warm` **0건**. 상태·컬럼·에러코드 신설 0. 리비전 0 |
| ③ `except Exception` 0 · 삼키는 자리 | 두 파일의 `except` 는 5 개이고 **전부 기존·구체 타입**(`AgentRunFailed` · `AgentRunTimeout` · `_SchemaViolation` · `json.JSONDecodeError`). 웜스타트 절에는 `except` 가 **없다** — 예외를 읽는 곳은 `_on_warm_start_task_done`(`:645-655`)의 `task.exception()` 하나이고 거기서 하는 일은 `logger.error(..., exc_info=exc)` 뿐이다. 기본값으로 때우는 자리 0 |
| ④ `session_id` 저장이 새 세션 · 대기 중 트랜잭션 0 | `:658-690` — 토큰 읽기 `session_scope()` 하나로 열고 닫은 뒤 **트랜잭션 밖에서** `gateway.run()` 을 기다리고, 저장은 다시 새 `session_scope()` 다. BE §7 그대로 |
| ⑤ 토큰 `None` → 미제출 + 로그 | `:671-675` — `logger.warning("회의 %s 에 회의 토큰이 없어 웜스타트를 제출하지 않습니다")` 후 `return`. 재발급·재시도 없음. 테스트 `test_meeting_start_warm.py:121` |
| 세션 id 없이 끝나면 | `:684-686` `RuntimeError` 전파(콜백이 로그) — **조용한 기본값 없음**. 테스트 `:206` 이 `ai_session_id is None` 을 단언 |

DEC-003 §7 웜스타트 행 「별도 기록 테이블 · 재시도 경로 · 재웜스타트 갈래가 없고 **남기는 것은 예외 전파 로그뿐**」 · SPEC-007 §4 「웜스타트」 표 실패 행 · BE §5-3 「웜스타트 제출도 같은 방식의 백그라운드 태스크다 — 단 job 행은 만들지 않는다」와 전부 맞는다(8-a 테스트가 `job` 행 0건을 단언한다).

### 2-3. 프롬프트 (MF-50 · MF-55 · DEC-003 §8 · SPEC-007 §4)

`_WARM_START_PROMPT`(`meeting_batch_service.py:730-812`) — **2,323자 · 82줄.** WP Phase 2 「1페이지 안」을 만족하고 테스트가 4,000자 상한을 건다(`:285`).

| 검사 | 결과 |
|---|---|
| ① 컨텍스트 0 | 직접 파싱해서 셌다 — `humanAgendas` **0** · `taskWhitelist` **0** · `project`(ASCII) **0** · `{` **0** · `}` **0** · `[` **0** · `]` **0** · `dueDate` **0** · `workType` **0**. 남은 `task` 문자열은 도구 이름 `list_tasks` · `get_task` 두 줄뿐이다 |
| ② 여섯 절 | ① 역할(머리글 없는 첫 문단 「너는 회의에 참가하는 두 명 중 하나다」) ② `## 회의는 이렇게 흐른다` ③ `## 무엇을 만드나 — 안건이 뼈대고 나머지는 거기서 파생된다` ④ `## 어떻게 요약하나` ⑤ `## 쓸 수 있는 도구` ⑥ `## 쓰면 안 되는 것`. 테스트 `:269` 가 머리글 목록을 순서까지 고정한다 |
| ② DEC-003 §8 문장 대조 | 「액션과 업무를 가르는 선」 → 「이미 하고 있던 일의 현황 보고는 액션이 아니다 — 그건 업무다」 ✓ · 「업무는 반드시 실제로 있는 것만」 → 「반드시 실제로 있는 업무를 가리킨다. 없는 업무를 만들어 내지 마라 — 도구로 조회해서 확인해라」 ✓ · 「줄을 만들기 전에 먼저 어느 안건인지」 → 「그러니 줄을 만들기 전에 먼저 어느 안건인지를 정해라」 ✓ · 「넷은 전부 안건에서 파생 · 안건 없이 떠 있는 줄은 없다」 ✓ |
| ② 요약 원칙 다섯(SPEC-007 §4 「주는 것」) | 압축 ✓ · 이름 안 씀 ✓ · 숫자 그대로(「383,900원을 「약 38만원」으로 바꾸지 마라」) ✓ · 말 안 한 건 안 채움 ✓ · 확실치 않으면 한 단계 낮춤 ✓ |
| ③ 도구 이름 | 프롬프트의 snake_case 식별자를 전수로 뽑아 `integrations/agent.py:_TOOL_NAMES` 와 대조 — **7/7 정확 일치 · 목록 밖 0개.** 테스트가 두 방향으로 잠근다(`:245` 프롬프트 안 전수 · `:252` `_TOOL_NAMES` 와 대조) |
| ④ 「통합본」 0 · 「준비됨」 | `통합본` **0건**(MF-56 어휘 준수 — 「합쳐진 회의록」으로 쓴다) · 마지막 줄이 「이번 요청에는 아무것도 만들지 말고 「준비됨」이라고만 답하라.」 ✓ |
| ⑤ `output_schema=None` | `:681` · 테스트 `:107` 이 `call.output_schema is None` 단언 |

### 2-4. 범위 준수

| 검사 | 결과 |
|---|---|
| `build_batch_prompt` · `run_final` · `_load_final_input` · `build_final_prompt` · `_persist` · `evaluate` | diff **0줄** |
| `_agenda_rows` | 함수 본문 diff 0. diff 에 잡히는 1줄은 **폐기된 옛 `build_warm_start_prompt` 안의 호출자**다 — WP §Code Surface·Open Issues 가 말한 「호출자 하나만 줄고 함수는 WORK-012 가 지운다」 그대로 |
| `meeting_finalize_service.py` | diff **없음** |
| 프론트 · compose · env · 리비전 | **0** (`tauri.conf.json` 은 범위 밖 · 나머지 파일 변경 없음) |
| 죽은 import 잔존(back) | **0** — `MeetingAiContextDTO` · `TaskContextDTO` · `task_repository` · `meeting_child_repository` · `MeetingTrack` · `MeetingAgendaDTO` 전부 다른 곳에서 계속 쓰인다. `from datetime import date` 는 정확히 함께 지워졌다 |

**삭제한 500 전파 테스트에 대한 판단** — `test_meeting_live_api.py` 의 `test_warm_start_failure_propagates_and_is_not_hidden`(웜스타트 예외가 `/start` 를 500 으로 만든다)은 **이 work 가 뒤집으라고 지시받은 바로 그 계약**이다. MF-1 · MF-70 · DEC-003 §7(「회의는 정상 시작된다」)이 200 을 요구한다. **회귀 보호를 잃지 않았다** — 대체가 `test_meeting_start_warm.py:186`(200 · `recording` · 로그에 스택)에 있고, 같이 지워진 단언들도 전부 옮겨 갔다(`calls == 1` → `:68` · `session_id is None`/`output_schema is None` → `:107` · 프롬프트 컨텍스트 → `:234` 로 **반대 방향**). 정당한 삭제다.

---

## 3. WARN

### W-1. `reset_state()` 가 `_tasks` 를 비우지 않는다 — 테스트 사이로 태스크가 샌다

- **자리**: `meeting_batch_service.py:97-102`(`_timers`·`_locks` 만 비운다) · `_tasks` 는 `:94` 의 모듈 전역 · `conftest.py` 에 태스크를 거두는 autouse 픽스처가 없다
- **무엇이 달라졌나**: 전에는 `/start` 가 웜스타트를 **인라인으로 기다렸다.** 이제 `/start` 를 부르는 **모든 테스트**가 태스크 하나를 띄운다 — `live_scope` 를 안 쓰는 파일(`test_meeting.py:324` 등)은 `wait_for_tasks()` 를 부르지 않으므로 태스크가 `_tasks` 에 남은 채 테스트가 끝난다.
- **왜 문제인가**: ① 다음 파일의 `start_meeting` 이 부르는 `wait_for_tasks()` 가 **남의 테스트 태스크**까지 gather 한다 ② 픽스처 teardown 이 `install_gateway(None)` 을 한 뒤(`conftest.py:64`) 그 태스크가 `get_gateway()` 에 닿으면 `agent.py:191-195` 가 **진짜 `OpenKknaksGateway`** 를 만든다 ③ 이벤트 루프가 닫힐 때 pending 태스크 경고
- **오늘 안 터지는 이유**: `live_scope` 없는 파일에서는 태스크가 실제 `SessionLocal` 을 열고 롤백 중인 테스트 트랜잭션의 토큰을 못 봐서 `meeting_token is None` 으로 **게이트웨이에 닿기 전에** 돌아간다. 설계로 보장된 것이 아니라 가시성으로 보장된 것이다 — 595 passed 는 맞지만 플레이크 표면이다.

### W-2. `test_meeting_live_api.py:85` 의 단언이 계약이 아니라 하네스 아티팩트다

- **자리**: `test_start_is_a_transition_only_and_does_not_wait_for_the_warm_start` — `assert row.ai_session_id is None`
- **무엇이 일어나나**: 이 파일은 `live_scope` 를 쓰지 않는다(grep 0건). 그래서 `session_scope` 가 실제 `SessionLocal` 이고, 웜스타트 태스크는 회의 토큰을 못 찾아 **제출 없이** 끝난다. `ai_session_id` 가 `None` 인 것은 「기다리지 않아서」가 아니라 「토큰이 안 보여서」다.
- **왜 WARN 인가**: 테스트 이름과 docstring 이 MF-1 을 증명한다고 말하는데 실제로 증명하는 것은 harness 가시성이다. 누가 이 파일에 `live_scope` 를 붙이면 단언이 뒤집힌다. 코드 안 주석은 이 사정을 정직하게 적어 두었고, **MF-1 의 진짜 증명은 `test_meeting_start_warm.py:68·84` 에 따로 있다** — 그래서 심각도는 낮다. 이름을 사실에 맞추거나 단언을 `status == "recording"` 쪽으로 좁히는 편이 낫다.

### W-3. 삭제한 테스트가 남긴 죽은 import 둘

- **자리**: `test_meeting_live_api.py:18` `from tests.fakes.agent import WARM_SESSION_ID, FakeAgentGateway` — 두 이름 모두 파일 안에서 **import 줄 말고는 쓰이지 않는다**(각 1회). 같은 파일의 픽스처 import 들과 달리 `# noqa: F401` 도 없다.
- 레포에 ruff 설정이 없어 지금은 아무도 잡지 않는다(`app/back/pyproject.toml` 에 lint 섹션 0). 파일 머리 docstring 과 `# --- Phase 2 — /start 웜스타트` 절 제목도 옛 내용을 가리킨다.

### W-4. 테스트 전용 헬퍼 `wait_for_tasks()` 가 프로덕션 모듈에 산다

- **자리**: `meeting_batch_service.py:693-699`. 프로덕션 경로 호출 **0건**(호출자는 `meeting_live_fixtures.py:86` 과 `test_meeting_start_warm.py` 7곳뿐)
- **완화**: 같은 파일 `:97` 의 `reset_state()` 가 이미 같은 성격이라 파일 관례와 일치하고, docstring 이 「프로덕션 경로는 이것을 부르지 않는다. 부르면 「기다리지 않는다」가 깨진다」고 못 박았다. WP §Code Surface 에는 이 함수가 없다 — **계획에 없던 산출물**이라는 점만 기록한다.

### W-5. 프롬프트 정적 단언이 WP 문구보다 느슨하다

- **자리**: `test_meeting_start_warm.py:231-236` — needle 이 `"humanAgendas", "taskWhitelist", '"tasks"', '"project"', "컨텍스트:"`
- WP §Internal Interface 는 「`project` 같은 **키**가 0건」이라고 적었는데 테스트는 **따옴표를 씌운 JSON 키 형태**만 본다. 지금 문자열에는 bare `project` 가 실제로 0건이지만(직접 확인), 나중에 누가 `project: …` 같은 줄을 넣으면 테스트가 안 잡는다.
- `tasks` 를 bare 로 못 보는 것은 **불가피하다** — 도구 이름 `list_tasks` 가 있다. 그래서 이건 코드 잘못이라기보다 WP 의 needle 목록이 문자 그대로 쓸 수 없다는 문제다(→ D-1). `{`/`}` 는 `:239` 가 따로 0건을 건다.

### W-6. Phase 2 「워커 로그 실측 캡처」가 아직 없다

- WP Phase 2 검증 마지막 항목 — 「워커 로그에서 웜스타트 요청 본문이 **1페이지 안**이고 회의 데이터가 없다(실측 캡처)」. 길이(2,323자)와 컨텍스트 0 은 테스트가 정적으로 잠갔지만 **워커 로그 캡처는 없다.**
- Done Criteria 의 앱 창 실측(SPEC-007 §6 AC)은 코디가 아침 항목으로 넘겼으므로 여기서 세지 않았다. WP Phase 1·2 `Status` 와 `완료 증거` 는 `TODO` · `미작성` 그대로다.

---

## 4. 문서 공백

| # | 자리 | 무엇이 비었나 |
|---|---|---|
| **D-1** | WP §Internal Interface 「프롬프트에 없는 것」 | needle 을 `humanAgendas` · `tasks` · `taskWhitelist` · `project` 로 적었는데 **`tasks` 는 문자 그대로 쓸 수 없다** — 도구 이름 `list_tasks` 가 프롬프트에 반드시 있어야 한다. 정적 검사 needle 을 JSON 키 형태(`"tasks"`)로 못 박든지, 「도구 이름 제외」를 적든지 해야 한다(W-5 의 뿌리) |
| **D-2** | WP §Code Surface 의 「고칠 테스트」 행 | `test_meeting.py` · `test_meeting_batch.py` 를 지목했는데 실제로 고쳐야 했던 것은 `meeting_live_fixtures.py`(`start_meeting` 이 태스크를 거두게) · `test_meeting_live_api.py` 였다. 지목한 둘은 손대지 않고도 통과한다. **코드가 맞고 문서가 틀렸다** |
| **D-3** | `backend/README.md` §12 | `reset_state()` · `wait_for_tasks()` 처럼 **테스트 격리 헬퍼를 프로덕션 모듈에 두는 관례**가 문서에 없다. 이미 두 개가 있으므로 규약을 한 줄로 정하거나(어디에 두고 어떻게 표시하는가) 금지하거나 결정이 필요하다(W-4 의 뿌리) |
| **D-4** | `backend/README.md` §5-3 「기동 스윕」 | 「`queued`/`running` 으로 남은 job 을 훑는다」만 있고 **웜스타트 태스크가 스윕 대상이 아니라는 문장이 없다.** 그 사실(job 행을 안 만들므로 프로세스가 죽으면 그 회의는 `ai_session_id` `NULL` 로 남고 아무 처리도 안 한다)은 WP §Open Issues 에만 있다 — 아키텍처 문서에도 한 줄이 필요하다 |

---

## 5. WP 검증 항목 ↔ 테스트 대응표 (`test_meeting_start_warm.py` 32)

**Phase 1**

| WP 검증 항목 | 테스트 |
|---|---|
| **BE §12 8-a** — 워커를 막은 채 `/start` → 응답 · `recording` · `recording_started_at` 참 · `ai_session_id IS NULL` · 트리거 밀어도 제출 0 | **`:143`** — 문장 네 절을 전부 단언하고 `recording_started_at` 과 MF-70(행 0건)까지 더 본다 |
| 대역 게이트웨이가 응답 반환 뒤에 불린다(요청 중 0건) | `:68` |
| 훅을 안 돌리면 호출 **0건** — 커밋이 안 되면 웜스타트도 없다 | `:84` |
| 성공하면 `ai_session_id` 가 새 세션에서 차고, 그 뒤 배치가 정상 제출 | `:94` |
| 제출 파라미터(새 세션 · 스키마 없음 · `ai_timeout_sec` · 회의 토큰 원문) | `:107` |
| 토큰 없으면 미제출 + 로그(WORK-009 규칙) | `:121` |
| 예외로 죽어도 `recording` · 응답은 이미 나갔다 | `:186` |
| **DB 어디에도 실패 기록 없음**(`meeting_batch_run` 0 · `job` 0) | `:143` 끝 |
| 세션 id 없이 끝나면 조용히 저장하지 않는다 | `:206` |
| 정적: `session.commit(` · `load_warm_start_context` · `WarmStartContext` 0 | `:297`(param 3) |
| 정적: `_task_rows` · `WarmStartContext` · `load_warm_start_context` 0 | `:305`(param 3) |
| 실패 갈래 0(`retry` · `attempt` · `warm_start_failed`) | `:310` — 웜스타트 절만 잘라서 본다(배치·종료의 기존 `attempt` 는 살려 둔다) |

**Phase 2**

| WP 검증 항목 | 테스트 |
|---|---|
| 컨텍스트 키 0건 | `:231`(param 5) — needle 이 WP 보다 느슨하다(W-5) |
| JSON 블록 0건 | `:239` |
| 도구 7개 전부 · 그 밖 0 | `:245` · `:252`(`_TOOL_NAMES` 와 교차) |
| 용어 다섯의 뜻이 각각 한 절 | `:259`(param 5) |
| 「안건이 뼈대」 | `:265` |
| 여섯 절 + 「준비됨」 마무리 | `:269` |
| `output_schema=None` | `:107` |
| 인자 없음 | `:226` |
| 1페이지 안 | `:285`(4,000자 상한) |
| **워커 로그 실측 캡처** | **없음** — W-6 |

---

## 6. 요약

**이 work 는 문서대로 섰다.** `/start` 는 전이 UPDATE + 토큰 INSERT 한 트랜잭션이 되었고 `commit()` 이 사라졌으며, codex 왕복이 요청 밖으로 완전히 나갔다. 웜스타트 프롬프트는 컨텍스트가 0이고 도구 이름 일곱이 `enabled_tools` 와 글자 그대로 같으며 DEC-003 §8 의 용어 다섯이 문장까지 옮겨졌다. **실패 갈래는 만들어지지 않았고**(MF-70) 삭제한 500 전파 테스트는 이 work 가 뒤집으라고 지시받은 계약이라 정당하며 대체 테스트가 있다. 011·012 범위 침범 0.

남은 것은 테스트 위생과 증거 셋이다 — ① **W-1** `_tasks` 누수(오늘은 안 터지지만 보장이 설계가 아니라 가시성에 기대 있다) ② **W-2·W-3** 옛 테스트의 잔재(단언 이름·죽은 import) ③ **W-6** 워커 로그 실측 캡처. 어느 것도 커밋을 막을 무게는 아니다.
