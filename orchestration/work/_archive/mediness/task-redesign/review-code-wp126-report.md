# 리뷰 리포트 — task-redesign / WP-126 backend + frontend (2026-08-31)

## 판정: WARN (진행 가능 · FAIL 0)

계약(SPEC-152 재정비본 · WP-126 P0~P6 · _RESUME §2)이 요구한 **여섯 축이 전부 코드에 서 있다** —
판정 1벌 수렴 · 종결 사전조건 역할 분리 · run 감사 우회 0 · Slack fail-loud seam · RegenGate 이름
가드 5자리 전수 선언 · 죽은 코드 13종 per-symbol grep 0. allowed_paths 이탈 0, migration 신설 0,
모델 컬럼 diff 0. FAIL 사유는 없다.

WARN 6건은 **계약 위반이 아니라 「계약이 약속한 것 중 코드로 닿지 않는 자리」** 다. 특히 W1(재시도
표면 부재)은 P3 의 복구 서사가 제품 표면에서 실행 불가라 **배포 전 코디/사용자 판단이 필요**하다.

---

## 검수 범위

- diff: `HEAD(62e2400c)` 대비 **미커밋 delta** — modified 29 + untracked 3 = **32 파일**
  - `back/app` 21 · `back/tests` 5(+ 신규 2) · `back/alembic` 1 · `front/` 3(삭제만)
- 직전 커밋 62e2400c(WP-125)은 검수 범위 밖 — 재검수하지 않았다.
- 실행한 검사: `git diff`/`git status`, per-symbol `grep`(삭제 상수 13종 + 리터럴 13종),
  호출부 전수 grep(`active_round_complete`·`round_complete`·`set_run_status`·`RegenGate()`·
  `feedback_event`·`notify_event`·`WorkflowRunEvent`·`resolve_slack_user_ids`),
  시그니처·전이표·모델 컬럼 대조.
- **테스트는 실행하지 않았다**(리뷰어 tools.md 금지 항목 — 구현 워커·코디 몫). 테스트는 **읽어서**
  단언 내용만 검증했다.

---

## 위반 (FAIL 사유)

**없음.**

---

## 경미 (WARN)

### W1. `failed_retryable` 로 눕힌 incident 카드에 **재시도 표면이 없다** — P3 복구 서사가 닿지 않는다

- 근거(주장): `workflow/incident/workflow.py:102-114` (`err_slack_not_configured` docstring
  「토큰을 설정한 뒤 **retry 로 이어서 진행**된다」) · `routers/action_runtime_v2.py:818`
  (「카드는 인박스에 남으므로 토큰 설정 후 retry 로 이어진다」) ·
  `workflow/incident/const.py:88` · WP-126 P3 §검증 「설정 복구 후 retry → 채널 중복 생성 0」
- 근거(실측): retry 는 `actions/commands.py:233-234`(`intent == "retry"` → `kernel.retry`) 하나로만
  도달하고, 그 command endpoint 는 `routers/action_runtime_v2.py:1156-1157` 에서
  `_COMMAND_MOUNTED_TYPES` 화이트리스트 밖이면 **404** 다. 그 집합
  (`action_runtime_v2.py:850-866`)에 `INCIDENT_WORKFLOW_TYPE` 이 **없고**, 같은 파일
  `:1023` 이 「**incident 는 화이트리스트 밖이라 빈 목록 그대로**」라고 명시한다.
- 파급: fail-loud 전환 후 토큰 미설정 환경에서 declare 승인은 503 + 카드 `failed_retryable` 이
  되는데, **그 카드를 다시 밀 API 가 없다.** 구 버그(조용한 no-op → run 이 `responding` 좌초)보다는
  낫다(실패가 보인다) — 그러나 WP 가 약속한 「이어서 진행」은 현재 실행 불가다.
  같은 축이 P5 에도 걸린다: `_resolve_assignee_or_fail`(definitions.py:106-131) 실패도
  `failed_retryable` 로 눕고 같은 이유로 재시도 표면이 없다.
- 권장 수정: ⓐ `_COMMAND_MOUNTED_TYPES` 에 `C.INCIDENT_WORKFLOW_TYPE` 추가(한 줄, `back/` 안 —
  단 「승인·취소 버튼이 함께 뜬다」는 FE 파급이 있어 **범위 판단은 코디/사용자**), 또는
  ⓑ 이 라운드는 그대로 두고 **§Pre-deploy 에 「fail-loud 카드의 수동 처분 방침」을 명시**한다.
  코드 수정 없이 닫으려면 ⓑ 가 맞다 — WP-126 이 retry 표면 신설을 발주하지 않았다.

### W2. run 감사 P2 §검증 4항이 **테스트로 덮이지 않았다**(구조 근거만 있다)

- 근거: WP-126 P2 §검증 — 「세 종결 경로 전부에서 `workflow_run_events` 행 1건」·「Task 0건 run
  (경로 B)에서도 원장 행이 남음 — **구 문제의 회귀 테스트**」·「조인으로 정리 대상 복원」.
  delta 의 신규/수정 테스트 7파일에 `workflow_run_events`·`WorkflowRunEvent` 단언이 **0건**이다
  (`grep -rl WorkflowRunEvent back/tests` → `test_wp118_run_ledger.py` 하나뿐, 이번 delta 밖).
- 다만 **우회 0 자체는 구조로 참**이다(이건 확인했다): run.status 대입 지점은
  `engine/runtime.py:412` 한 줄이고 그것이 `set_run_status`(`:363-412`) 안이며, 착지는 전부
  `engine/runner.py:227-231 _land()` → `set_run_status` 를 지난다. 종결(`destination.is_terminal`)도
  같은 호출 뒤에 온다. 그래서 「세 종결 경로가 원장을 우회한다」는 상태가 **만들어질 수 없다**.
- 권장 수정: 회귀 가치가 큰 것은 **경로 B(Task 0건)** 한 건이다. 통합 테스트 1개 추가 권장.
  (코드 결함이 아니므로 재발주 없이 후속으로 미뤄도 된다.)

### W3. 새 공용 래퍼 `resolve_slack_user_ids` 가 **참조 0** 이고, 옛 이름이 남은 docstring 1건

- 근거: `tools/slack.py:66-72` — `resolve_slack_user_map` 의 값만 펴 주는 래퍼로 남겼는데
  실호출부가 **0** 이다(`grep -rn resolve_slack_user_ids back mcp` → 정의 1 + docstring 2).
  같은 Phase(P6)가 「참조 0 상수를 남기면 다음 라운드가 계약으로 읽는다」를 근거로 13종을 지웠다 —
  **같은 잣대가 이 함수에는 적용되지 않았다.**
- 함께: `workflow/incident/definitions.py:323` docstring 이 여전히
  「초대 대상(gatekeeper+invite_candidate 합류·**resolve_slack_user_ids**)」로 옛 이름을 든다.
  실제 호출은 `resolve_slack_user_map`(`:48`, `:381`)이다.
- 권장 수정: 래퍼를 지우거나(호출 0), 남긴다면 **왜 남기는가**를 한 줄로 적는다. docstring 이름은
  `resolve_slack_user_map` 으로 정정.

### W4. 삭제한 상수의 **문자열을 FE 가 아직 읽는다** — 둘 다 이미 죽은 분기

- `front/app/(authenticated)/ax/workspace.tsx:394` — `event.event_type === "ai_triage_completed"`
- `front/app/(authenticated)/ax/workspace.tsx:294` — `e?.code === "ACTION_STALE_PLAN_VERSION"`
- 근거: WP-126 §Pre-deploy 「응답·감사에서 사라지는 값을 읽는 **외부 소비자 없음** 확인」.
- 다만 **회귀는 없다**: 두 리터럴 모두 `back`·`mcp` 에서 산출 grep **0** 이다(상수도 참조 0이었고,
  `ACTION_STALE_PLAN_VERSION` 은 `routers/action_runtime_common.py:82-83` 이 400 평문으로 매핑해
  애초에 code 로 나간 적이 없다 — `const.py:79-80` 주석이 같은 사실을 적어 두었다).
  ⇒ FE 분기는 **이미 도달 불가**였고 이번 삭제로 달라지는 동작이 없다.
- 권장 수정: FE 워커 브리프가 「BFF 3건 삭제만·그 외 front 수정 금지」였으므로 이번 범위 밖이 맞다.
  **후속 FE 청소 목록에 2줄만 올린다.**

### W5. 활성 라운드 코호트 산식이 정본 밖에 **한 벌 더** 있다(판정은 아니다)

- 근거: `workflow/incident/workflow.py:963-968` `_assemble_completion_context` 가
  `prevention` 필터 → `max(round_no)` → 코호트 추출을 인라인으로 다시 쓴다. 정본
  `tasks/round_rule.py:47-55 active_round_tasks` 와 **같은 산식**이다.
- 「판정 1벌」 계약은 **깨지지 않았다** — 이 함수는 완료 판정이 아니라 LLM 근거용 완료 코멘트
  수집이고(`status == DONE` 필터), `active_round_complete` 를 부르지 않는 것이 옳다.
  그러나 이번 라운드가 `active_round_tasks` 를 **공개 심볼로 새로 만들었으므로**(round_rule.py:81
  `__all__`) 재사용 자리다.
- 이번 delta 가 만진 줄이 아니므로 rules.md §2(기존 부채) 경계에 있다 — **판정에는 넣지 않는다.**
- 권장 수정: `active_round_tasks(tasks, C.PREVENTION_TASK_TYPES)` 로 교체(1줄).

### W6. `EV_SLACK_INVITE_UNRESOLVED` 가 **에러코드 절에** 들어 있다(자리 규칙)

- 근거: `workflow/incident/const.py:91` — 파일이 스스로 나눈 절
  「`# ---- 도메인 이벤트명 ----`」(`:77`, `EV_ASSIGNEE_RESOLUTION_FAILED` 가 사는 자리)과
  「`# ---- 에러코드 ----`」(`:82`) 중 **후자**에 EV\_ 상수가 놓였다.
- 권장 수정: 이벤트 절로 이동(값·동작 무변경).

---

## 기존 부채 (이번 판정 제외)

- **`run_fanout` 에 멱등 키가 없다** — `tasks/factory.py:238-256` 은 items 루프 중간에 예외가 나면
  이미 만든 태스크가 그대로 커밋되고(커널이 삼키고 라우터가 commit), 재시도 시 중복 생성된다.
  P5 의 `_resolve_assignee_or_fail` 이 **실패 지점을 앞당기지 않았다**(구 판본도 같은 아이템의
  태스크 생성 자리에서 터졌다) — 성질·시점 동일이라 이번 delta 의 회귀가 아니다.
- **서비스 층 raw 쿼리** — `tools/slack.py:57-63` 이 `select(User.id, User.slack_id)` 를 서비스에서
  조립한다(구 `resolve_slack_user_ids` 도 같은 자리였다). 이번 delta 는 **위치를 옮기지 않고**
  반환 형태만 바꿨다. `repositories/user_repo.py` 가 제 자리지만 이관은 이번 범위 밖.
- **담당자 사다리 4단째가 2단째와 같다** — `workflow/incident/workflow.py:1009` `approver=lead`.
  아래 §워커 미결 ② 참조.

---

## 확인한 것 (PASS 근거 — 체크리스트 항목별)

### ① 판정 1벌 · 종결 사전조건 역할 분리 — **PASS**

- 정본: `tasks/round_rule.py:58-66 active_round_complete`(+ `:47-55 active_round_tasks`).
  모수 = `task_type` allowlist → 최대 `round_no` 코호트, terminal = `machine.TERMINAL_STATUSES`
  (`done`·`canceled`) **조건 없음**, 모수 공집합 → `False`. `deleted_at` 은 판정 층에 얹지 않고
  `_scoped()` 앵커에 둔다(`soft_delete.py:71-78` 주석 갱신 일치).
- 구 3벌 전부 위임으로 교체: `round_piece.py:38-40`(자체 `_active_round_complete` 삭제 · `:53` 자리
  주석) · `tasks_surface.py:319-327` · `round_eval.py:134-144`.
  `tasks_surface` 는 **의미가 「전량」→「활성 라운드」로 바뀌었고**, 유일한 외부 호출부인
  `decision/surface.py:655` 는 단일 라운드 도메인이라 실효 동일(근거를
  `decision/declaration.py:96-104` 주석이 명시).
- 잔존 0: `grep "all(t.status"` / `max(...round_no)` 전수 — 판정 성격의 사본 **0**.
  (`incident/workflow.py:968`·`decision/workflow.py:626`·`decision/surface.py:1078` 은 라운드
  **번호 산식**·컨텍스트 수집이지 완료 판정이 아니다 → W5 참조.)
- `factory.has_open_in_run_chain`(`:181-200`)은 **위임하지 않고 남았고**, docstring 표가
  「모수·묻는 것·실패 시」 세 축으로 두 술어를 갈라 적는다. WP-126 P1 「두 뜻을 한 함수가 겸하지
  않는다」와 일치. 함수 본문은 무변경(byte 동형) — 종결 사전조건 의미가 흔들리지 않았다.
- `eval_statuses` 에 `CANCELED` 추가(`round_eval.py:69-76`)는 **판정 의미를 바꾸지 않는다** —
  이건 「언제 물어보나」(트리거)이지 술어가 아니다(같은 파일 `:44-51` dataclass 주석). 계약
  terminal = `done`·`canceled` 이므로 **「취소도 terminal」의 착지가 맞다**. decision 은 이미
  두 값이었고 incident 만 갈려 있었다(`test_wp126_fail_loud.py:118-132` 가 동형을 단언).

### ② run 감사 — **PASS**(테스트 커버리지만 W2)

- 우회 0: `run.status` 대입은 `engine/runtime.py:412` **한 줄**뿐(전수 grep). 그 함수가
  `set_run_status`(`:363`)이고 대입 **전에** `WorkflowRunEvent` 를 append(`:397-411`),
  `cause ∉ RUN_TRANSITION_CAUSES` 면 `InvalidActionState` 로 **선다**(`:389-395`).
  착지는 전부 `runner.py:227-231 _land()` 를 지난다(종결 포함).
- payload 미사용: `WorkflowRunEvent` 에 자유 본문 칸 신설 **0**(모델 파일 diff 없음 —
  `git status back/app/models/` 빈손). 정리 목록은 각 Task 의 `task_canceled` 에 남는다.
- cause: 세 종결 경로 전부 카드 결재 → `run_ledger.by_approval`(`:57-72`)의
  `RUN_CAUSE_HUMAN_APPROVAL`. 어휘 확장 **0**.
- migration 0: alembic diff 는 `0135`(WP-125 OI-6 backfill) 하나뿐 — run 감사 축 신설 없음.
- 원장이 판정에 안 읽힘: `WorkflowRunEvent` 소비처는 `audit_repo.py:80-95 list_run_events`
  (감사 projection) 하나. 판정 경로 참조 **0**.
- 추적 Task 정리 훅: `definitions.py:133-158 cancel_open_tracking_tasks` — `task_type ==
  INCIDENT_RESPONSE_TRACKING` 만, 이미 terminal 은 skip(멱등), `lifecycle.apply_system_transition`
  (`lifecycle.py:279-307`)으로 **합법 전이**를 지난다. `todo/in_progress/blocked → canceled` 전부
  전이표 안(`machine.py:52-54`)이고 `canceled_at` 스탬프 + `task_canceled` 이벤트
  (`machine.py:60-75`), `cause` 가 payload 로 내려간다(`lifecycle.py:183-184`).
  `const.py:219 CLOSE_CAUSE_RUN_CLOSED = "run_closed"` ✔ 계약값 일치.
- finalize `[완료]` 가 **같은 검사**를 받게 됨: `definitions.py:92-97` — 열린 예방 Task 422
  (`ERR_TASK_ROUND_NOT_COMPLETE`) · 열린 Action 409, feedback(`:418-436`)과 동형. 두 처분(거부 vs
  정리)을 섞지 않는다. `[승인]`(decision 없음)은 종결이 아니라 검사 skip — 테스트가 단언
  (`test_incident_declaration.py` 신규 3건).

### ③ Slack fail-loud — **PASS**

- seam: `errors.py:21-38 ExecutionUnavailable(DomainError)` + `runtime.py:899-901`
  `isinstance(error, ExecutionUnavailable)` 일 때만 `commit()` → `raise`.
  **일반 DomainError 삼킴 경로 회귀 0** — else 분기는 종전대로 `return action`
  (`test_wp126_fail_loud.py:92-110` 이 `commits == 1`·`returned is action` 로 고정).
- 커밋→재-raise 순서 안전: 이 시점 세션에 실린 것은 **실패 원장뿐**이다 — 승인·`EXECUTING` 전이는
  같은 함수 앞부분(`runtime.py:871`)이 이미 commit 했고, `_execute_declare` 는 **첫 줄에서**
  세우므로(`definitions.py:224-226`) 부분 부수효과가 없다. 세션은
  `core/db.py:17 expire_on_commit=False` 라 중간 commit 이 상위 객체 접근을 깨지 않는다.
  같은 함수가 이미 mid-flight commit 을 쓰는 **기존 패턴**이다.
- 503 이 표면까지: `map_action_error`(`action_runtime_common.py:84-85`)가 DomainError 를 자기
  `http_status` 로 매핑 → `SLACK_NOT_CONFIGURED` **503**. `expected_rejection_types()` 에 넣지
  않은 것도 옳다(장애 아님/거절 아님 축).
- run 은 `awaiting_declare` 유지: 실행 실패 시 `_notify_verdict` 를 건너뛰므로(`runtime.py:903-911`)
  run 착지가 일어나지 않는다.
- 초대 미해소 감사: `definitions.py:381-401` — `resolve_slack_user_map` 으로 **입력 키 보존**
  (`tools/slack.py:37-64`), 차집합으로 `unresolved` 산출 후 `EV_SLACK_INVITE_UNRESOLVED` 감사.
  `_slack_id_for`(`:403-412`)의 `as_uuid` 는 깨진 값에 **raise 하지 않고 None**
  (`orgref/person_axis.py:121-128`), `resolve_many` 는 **파싱된 UUID 키**로 돌려주므로
  (`person_axis.py:147-159`) 조회가 성립한다. 채널 생성 자체는 실패로 치지 않는다 ✔ 계약.
  순서 보존 dedupe(`:384`)로 중복 초대 방지.
- 멱등 앵커 유지: `execution.result` partial `external_refs` 보존 경로 무변경
  (`runtime.py:884-887`), 골든 스냅샷 `test_p2d_slack_idempotent.py` 의 `_INV` 값 불변
  (스텁만 map 형태로 갱신 — 산출 동형).
- 완료 수신구 단일화: `POST /incidents/slack/complete` 라우트 grep **0**(주석 1건만 —
  `action_runtime_common.py:42`). WP-125 P3 착지 확인 완료.

### ④ RegenGate 이벤트 이름 가드 — **PASS**

- 가드: `actions/regen_gate.py:115-127` — `event.name != expected` 면 살아 있는 카드에
  `GATE_EVENT_IGNORED` 감사 후 **no-op(None)**. 카드가 없으면 감사 없이 no-op(터지지 않음).
- 소비자 **5자리 전수** 선언 확인: `RegenGate()` 인스턴스화 = incident 3
  (`incident/declaration.py:128·152·176`, 전부 `_regen_params`(`:95-109`) 경유) + decision_draft 1
  (`:103-111`) + task_draft 1(`:105-113`). **5/5 가 `feedback_event: DEFAULT_FEEDBACK_EVENT` 선언.**
- 행위 동형 검증: 그 5자리를 실제로 깨우는 producer 전수 —
  `runs_surface.py:122`(`"feedback"`) · `incident/surface.py:318`(`"feedback"`). 둘 다 기본값과
  일치 ⇒ **정상 접수 경로 회귀 0**. 다른 producer(`round_eval.py:131` `task_done` ·
  `llm/background.py:97` `drafted` · `decision/surface.py:722` `intake_revise` ·
  `meeting/surface.py:341` `revise`)는 RegenGate 스테이지가 목적지가 아니거나(decision·meeting 은
  `Gate` 조각), 닿더라도 **구 판본이 오접수하던 바로 그 경우**다.
- 재상정 경로는 영향 없음: resubmit 은 background 셸이 커널로 하고 `notify_event` 를 쓰지 않는다
  (`regen_gate.py:12`·`:101-102`).
- 범위 준수: 「선언한 이름과 일치할 때만 접수」라는 **버그 수정까지만** — SPEC-150 조각 계약 개정
  없음(OI-3 준수).

### ⑤ 추적 Task cc (B 유지) — **PASS**

- `definitions.py` 의 `cc_member_ids` 산출 **코드 무변경** — 삭제·확대 0, 위에 사유 주석만 붙었다
  (「계약과 다르다 — 알고 유지한다」 + OI-4 발명 금지 4항 명시).
- _RESUME §2 2026-08-31 「추적 Task cc = declare 의 AI 초대 후보 유지(현행 보존)」와 일치.
- 활성 버전 유추·트리거 버전 축 추가·제품 참여자 확대 **0**.

### ⑥ 죽은 코드 13종 — **PASS**(STATUS_FAILED 존치 ✔ · W6 죽은 인자 처리 ✔)

- per-symbol grep 재확인(정의 파일 제외) — 13종 전부 **참조 0**:
  `EV_TRIGGER_RECEIVED`·`EV_WORKFLOW_RUN_STARTED`·`EV_DECLARE_SUBJECT_CREATED`·
  `EV_AI_TRIAGE_STARTED`·`EV_AI_TRIAGE_COMPLETED`·`EV_INBOX_CARD_AVAILABLE`·
  `EV_REVIEW_DRAFT_CREATED`·`EV_REVIEW_REGENERATED`·`EV_FEEDBACK_REVIEW_CREATED`·
  `EV_FEEDBACK_REGENERATED`·`EV_FEEDBACK_REVIEW_FALLBACK`·`ERR_ACTION_STALE_PLAN_VERSION`·
  `META_DECLARE_SUBJECT_ID`. 리터럴 값도 back/mcp 에서 **0**(front 2건 = W4).
- **`STATUS_FAILED` 존치 확인**: `const.py:42` 살아 있고 소비처
  `incident/surface.py:70 _TERMINAL_RUN_STATUSES` 그대로 ✔.
- `EV/ERR_ASSIGNEE_RESOLUTION_FAILED` 는 P5 가 되살렸으므로 **유지가 맞다**(계약대로) —
  `definitions.py:120-127` · `workflow.py:114-121` 이 실제 소비.
- 거절 축 잔재: `ERR_TASK_DECLINE_REASON_REQUIRED` grep **0**(이미 없음).
  `runs_projection.py:306 "task_declined"` 는 **과거 원장 행 렌더 순서**라 존치가 맞다
  (`tasks/const.py:14-15` 이 append-only 근거를 명시).
- **W6(WP-125 이월 — `patch_task` 죽은 인자 4개) 처리 완료**: `tasks_surface.patch_task` 시그니처에서
  `runner`·`round_task_types`·`round_done_event`·`round_eval_statuses` 제거
  (`tasks_surface.py:330-355`), 호출부 2곳 동반 정리(`incident/surface.py:164-168` ·
  `decision/surface.py:562-568`). decision 은 `runner` 를 `delete_task` 시그니처 정합용으로만
  남기고 그 사유를 적었다 — 죽은 인자가 아니다.

### ⑦ 0135 backfill — **PASS**

- **append-only 준수**: `_backfill_orphan_accepted_events`(`:97-120`)는 `INSERT ... SELECT` 뿐이고
  `tasks`·기존 `task_events` 를 **UPDATE/DELETE 하지 않는다**. `NOT EXISTS` 로 이미 이벤트가 있는
  행은 건너뛰므로 **재실행 안전**.
- **가드가 뒤에 남아 있다**: `upgrade()` 순서 `:159-163` = backfill → `_guard_orphan_accepted_at()`
  → `drop_column`. 가드 본문 무변경(재발 방지로 존치), docstring만 정정.
- 스키마 정합: `TaskEvent`(`models/action_runtime.py:732-748`)의 NOT NULL 칼럼
  (`task_id`·`event_type`·`actor_kind`·`payload`·`created_at`) 전부 채워지고, nullable
  (`actor_id`·`actor_member_id`)은 생략/NULL. `actor_kind='system'` 은 PG enum
  `runtime_actor_kind` 의 **값**(`ActorKind.SYSTEM = "system"`, `_actor_kind_column` 이
  `values_callable` 로 값 저장)과 일치. `gen_random_uuid()` 는 `0028`·`0109`·`0110` 선례 존재.
- 추적성: `actor_label='wp125-oi6-backfill'` + `payload.backfill/source` 로 소급분이
  **원본 이벤트와 구별된다**. 시각 = `t.accepted_at`(발명 아님).
- 은퇴 어휘(`task_accepted`)로 소급 기입하는 점은 _RESUME §2 2026-08-31 「accepted_at 고아 60건 =
  이벤트 소급 backfill 후 drop(OI-6 최종)」 **사용자 확정**과 일치 — 지적하지 않는다.

### ⑧ allowed_paths — **PASS**

- BE 워커: `back/` **28파일**(app 21 · tests 6 · alembic 1) — 이탈 0. `mcp/` 무변경(허용됐으나 불필요).
- FE 워커: `front/` **삭제 3건만**, 그 외 front 수정 **0**(`git status front/` = D 3줄).
  삭제한 3 라우트의 호출자 grep **0**, 형제 `review/feedback/route.ts` 는 살아 있어 오삭제 없음.
- 문서 레포·`config/` 등 침범 0.

### ⑨ 워커 미결 5건 중 ② resolver 실효 3단 — **판단 적정(보고로 남긴 것이 맞다)**

- 실측 일치: `workflow/incident/workflow.py:1004-1010` — 사다리는
  `named_member → product_lead=lead → commander → **approver=lead**` 로, **4단째가 2단째와 같은
  값**이다. 즉 실효 3단이고 WP-126 P5 §작업의 「4단(… → approve actor)」 표기와 코드가 어긋난다.
- 워커가 배선을 바꾸지 않고 보고로 남긴 것은 **옳다**: ⓐ P5 는 「**실측 확인**」이지 재배선 발주가
  아니고, ⓑ `approver` 를 실제 승인 actor 로 바꾸는 것은 **담당자가 달라지는 행위 변경**이며,
  ⓒ WP-126 §Domain/Schema 가 「구현 중 계약과 어긋나는 사실이 나오면 **코드를 고치지 말고 SPEC 으로
  되돌린다**」를 명시했다. ⇒ SPEC-152 §담당자 축 정정 대상으로 올리는 것이 정본 처리다.
- 나머지 미결(P0 운영 DB 실측 4항 미접근 · cc 계약 정정 · OI-7 파생 전이 · 죽은코드 재실측)도
  전부 **계약이 「사용자/후속 판단」으로 열어 둔 자리**이고, 코드로 발명한 흔적이 없다
  (`round_eval.py:20-30` 이 파생 전이 미호출을 명시 유지).

### 그 밖에 확인한 것

- 테스트 갱신 정합(읽기 검증): 신규 2파일(`test_wp126_round_rule.py` 12케이스 ·
  `test_wp126_fail_loud.py` 4케이스) + 수정 5파일. 스텁 갱신이 **골든 값을 바꾸지 않는다**
  (`test_p2d` `_INV = ["gk_s","u2_s"]` 불변). 약화된 단언 없음.
  `test_wp126_round_rule.py:113-127` 은 세 자리의 소스에 `active_round_complete` 존재 +
  `all(t.status` 부재를 단언해 **판정 사본 재발을 기계로 막는다**(다소 취약한 소스-문자열 단언이나
  의도는 유효).
- 계층: 신규 코드가 전부 제 자리 — 순수 술어는 `services/.../tasks/round_rule.py`, 조회는
  repositories, 라우터에 비즈니스 로직 추가 0(diff 의 라우터 변경 2건은 **주석뿐**).
- 스키마 경계·응답 모델 변경 0.

---

## 코디에게 넘기는 판단 2건

1. **W1** — fail-loud 카드의 재시도 표면. 코드로 닫을지(화이트리스트 1줄, FE 파급 있음) / 문서로
   닫을지(§Pre-deploy 수동 처분 방침). **배포 전에 정해야 하는 항목**이다.
2. **⑨ / W5·W3·W6** — SPEC-152 §담당자 축 「4단」 표기 정정(코드 3단)과 원라이너 3건
   (docstring 이름·상수 자리·코호트 재사용). 재발주 없이 코디 직접 정정 가능한 크기다.
