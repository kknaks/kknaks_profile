# 리뷰 리포트 — strong-hajin-polish2 / backend · WORK-009 Phase 1 (2026-10-02)

## 판정: FAIL

1-1(초안 저장)·1-2(AI 지시문)·1-3(마감일 채움)의 핵심 계약은 코드와 테스트로 섰고, confirm 경로의 기록도 그대로다. FAIL 은 add1(라벨) 한 건이다. 워커가 「내부 이름이라 유지」로 분류한 pydantic `Field(title='기한')` 이 실제로는 **채팅 서랍의 명령 확인 폼 칸 라벨**로 화면에 나간다. 그래서 AX 의 업무 수정·업무 요청 수정·프로젝트 업무 계획 확인 폼에 아직 「기한」·「기한 없애기」가 보인다. 그 밖에 경미 4건이 있다. 그중 하나(첨부 자료가 붙은 초안은 저장 뒤 「등록」에서 회차가 또 오른다)는 Phase 2a-1 FE 계약과 함께 정해야 한다.

## 검수 범위

- 대상: `backend/` + `docs/unified-operations-inventory.json` 미커밋 변경. 수정 17파일 + 새 `backend/tests/contract/test_task_due_date_fill.py`. +731 / −85. `frontend/` 는 보지 않았다(FE 소비자 확인을 위한 읽기만)
- allowed_paths: `docs/unified-operations-inventory.json` 은 백엔드 범위 밖이다. 하지만 AGENTS.md 「operation inventory drift 는 diff 항목만 패치」가 요구하는 파일이고 워커가 보고했다 — 정당한 이탈로 본다
- 기준: WP Phase 1(1-1·1-2·1-3) · P-1·P-2·P-4 · SPEC-002 §2.9·§4 「초안 저장」·§5·§6 · SPEC-001 S-9 6·7·§5·U-17 · SPEC-003 「날짜 채움」 · SPEC-004 §5 · 발주서 + add1 · 워커 보고 원문
- 실행한 검사
  - 바뀐 소스 diff 전문
  - 호출 흐름 추적: `ActionCenterApplication.execute`(`modules/actions/domain.py:160-172`) → `AxProposalActionHandler.normalize`/`execute`/`_save_draft`/`_open_revised_round` → `decide_ax_confirmation`(`modules/actions/confirmation.py:178-246`) → `run_action_command`(`bootstrap/application.py:3393-3415`)
  - `transition_task`·`submit_completion` 의 날짜 채움 자리
  - `COMMAND_CONTRACTS` 칸 라벨을 만드는 `_command_edit_contract`(`platform/actions.py:1860-1894`)
  - grep: 백엔드 「기한」 잔존 · `ACTION_VERSION_STALE` · FE `schedule_release`·complete 소비자 · 인벤토리 diff 줄 집계
  - `COMMAND_CONTRACTS` 스키마 title 을 파이썬으로 실제 출력
  - **`make test-unit` → 403 passed** · **`make test-contract` → 병렬 1154 passed, 직렬 1 failed / 127 passed**. 직렬 실패 1건은 같은 직렬 필터로 `--lf` 재실행하자 통과했다(아래 「참고」)

## 위반 (FAIL 사유)

- **F1 `backend/src/ax_workspace/modules/work/task_commands.py:52`(`TaskEditFields`) · `backend/src/ax_workspace/modules/work/request_commands.py:54-55`(`WorkRequestRevisionInput`) · `backend/src/ax_workspace/modules/work/project_commands.py:56`(`ProjectWorkInput`)** — `Field(title='기한')`·`'기한 없애기'` 가 **화면 라벨이다**.
  - `ActionPresenter._command_edit_contract`(`platform/actions.py:1865`·`:1882`)가 `COMMAND_CONTRACTS` 모델의 JSON 스키마에서 `'label': definition.get('title', key)` 로 편집 계약 칸 라벨을 만든다. FE `CommandConfirmationForm` 이 그 라벨을 채팅 서랍 안 확인 폼에 그대로 그린다
  - 실제 출력(파이썬으로 스키마 title 을 뽑음):
    - `task.update` `due_date` → 「기한」
    - `work_request.amend` `due_date` → 「기한」, `clear_due_date` → 「기한 없애기」
    - `project.plan_work` `due_date` → 「기한」
  - 워커는 이 7곳을 「도구 입력 스키마·OpenAPI 의 내부 이름, AI 가 읽는 값」이라 유지했다. 하지만 add1 §3 이 유지를 허락한 것은 **필드 id·API 키 · FE 정규식이 매칭하는 오류 문구 · 프롬프트/도구 설명 속 표현**이다. 화면에 나가는 칸 라벨은 add1 §1 「서버가 화면용으로 내는 문자열 중 `due_date` 를 부르는 이름 전부」에 든다. 같은 판에서 미리보기 행(`actions.py:1478` task.update 변경 줄)은 「마감일」로 바꿨다. 그래서 **같은 카드 안에서 미리보기는 「마감일」, 편집 칸은 「기한」**으로 갈린다
  - 근거: SPEC-001 U-17 「`due_date` 의 화면 이름 — 「마감일」 하나」 · add1 §1·§3 · 리뷰 브리프 §3-6
  - 권장 수정: 화면에 닿는 모델의 title 을 「마감일」·「마감일 없애기」(·「마감일 삭제」)로 바꾼다. `task_creation.py:17`·`task_commands.py:131`·`:133` 도 같은 이름 계열이라 함께 맞춘다. 스키마 title 이 바뀌므로 inventory drift 를 그 항목만 다시 패치한다. FE 정규식(`/마감일|기한|due_date|schedule/`)은 오류 문구를 보는 것이라 이 변경과 무관하다

## 경미 (WARN)

- **W1 첨부 자료가 붙은 `task.create_self` 초안 — 저장 뒤 「등록」이 회차를 또 올린다** (`backend/src/ax_workspace/platform/action_center.py:603-610`·`confirmation.py:216-238`)
  - `normalize` 는 `attachment_draft_ids` 를 payload 에 키가 있을 때만 읽고, 없으면 `[]` 다. `decide_ax_confirmation` 은 첨부 ID 까지 넣은 스냅샷끼리 비교한다
  - FE 카드의 「등록」은 붙인(staged) 자료 ID 를 `attachment_draft_ids` 로 싣는다(`frontend/src/features/action/AxDraftCard.tsx:276-280`). 그래서 **저장 회차에 첨부 ID 가 없고 자료를 붙였다면**, draft 없는 confirm 의 최종 스냅샷이 기준과 달라 **새 회차를 연다**(회차 3)
  - 반대로 저장에 첨부 ID 를 실으면 스냅샷에 남는다. 이는 SPEC-002 §4 「자료 초안 — 이 명령의 대상이 **아니다**」와 결이 다르다. 워커의 FE 계약(`attachment_draft_ids?` 를 받음)도 이쪽을 열어 둔다
  - WP 1-1 「저장 뒤 등록 … 회차가 또 늘지 않는다」는 자료 없는 초안에서만 참이다. 새 테스트(`test_confirming_a_saved_draft_without_a_draft_…`)도 자료 없는 경우만 본다. `work_request.create` 는 `ATTACHABLE_ACTION_TYPES` 가 아니라 해당 없다
  - 근거: WP 1-1 · SPEC-002 §4 「자료 초안」 줄 · 리뷰 브리프 §3-1
  - 권장: 2a-1 FE 계약과 함께 정한다. (a) 저장도 지금 붙인 자료 ID 를 싣는다 — 스냅샷이 같아져 등록 때 회차가 안 오르고, SPEC 줄을 「저장도 붙인 자료 목록을 함께 남긴다」로 고친다 — 또는 (b) 서버가 저장·확인의 「바뀌었나」 비교에서 첨부를 뺀다. 어느 쪽이든 자료가 있는 경우의 계약 테스트 하나
- **W2 저장 권한 테스트 없음** — 권한 자체는 맞다.
  - 봉투는 `ACTION_DECIDE` + pending 일 때만 저장을 내린다(`policy.py:127-137`)
  - `_save_draft` 는 `owner_id == principal` 로 잠그고, 아니면 `ActionNotFound`(`action_center.py:997-1004`)
  - 그런데 **남(소유자가 아닌 사람)이 저장을 부르는 경우**의 계약 테스트가 없다. 정책 단위 테스트는 capability 축만 본다
  - 근거: SPEC-002 §4 「누가 — 봉투가 이 명령을 내려 준 사람만」 · 리뷰 브리프 §3-3
  - 권장: 다른 persona 로 `save_draft` → 404(또는 422)이고 회차가 그대로인 테스트 하나
- **W3 `backend/src/ax_workspace/modules/work/task_results.py:53`** — `TaskScheduleReleaseView` docstring 이 아직 「**날짜가 바뀌는 세 자리 전부가 이 묶음을 낸다** — 업무 수정 · 시작 전이 · 조건 변경 제안 동의」다. 이 docstring 은 OpenAPI·inventory 스키마 `description` 으로 그대로 나간다(인벤토리 diff 에 같은 문장이 새로 실렸다). 넷째 자리(완료의 마감일 채움)를 넣은 이번 판과 어긋난다. `http.py:2543-2547` 의 시작 docstring 은 고쳤다
  - 근거: SPEC-004 §5 「네 자리」(fix1) · 리뷰 브리프 §3-7
  - 권장: 문장에 「· 완료의 마감일 채움(완료·완료 보고 제출)」을 더하고, 인벤토리를 그 항목만 다시 패치한다
- **W4 넷째 자리 테스트가 「배정이 살아 있는 업무」를 보지 않는다** — `test_task_due_date_fill.py` 의 `released_count == 0` 단언 둘(직접 완료 · 완료 보고)은 **배정이 하나도 없는 업무**에서 잰다. 그래서 검증 훅이 안 돌아도 0 이다 — 조용히 통과한다. SPEC-004 §6 (fix1)은 「시작일만 있고 마감일이 빈 업무에 **살아 있는 배정을 만들어 두고** 최종 완료와 완료 보고 제출을 각각 부르면 … 검증이 돌며 `released_count` 가 `0`」을 요구한다
  - 근거: SPEC-004 §6 「완료의 마감일 채움 자리도 「닫을 것이 없음」을 증명한다」 · 리뷰 브리프 §3-9
  - 권장: 시작일 업무에 그날 배정을 만들고 완료 → 배정이 조회에 그대로 있고 `released_count == 0`. 훅이 돈다는 증거로 저장소 호출 횟수를 보거나, 시작일 채움 테스트(`test_task_schedules.py`)의 방식을 따른다

## 참고 (판정 제외)

- **직렬 패스 1건 실패 → 재실행 통과** — `make test-contract` 의 직렬 패스(`-m serial -n0`)에서 1 failed(`_runtime_error` 트레이스)가 나왔다. 같은 필터 `--lf` 로 다시 돌리자 1 passed 였다. 직렬 표지는 정의상 「실시간 창을 재는 동시성 테스트」라 흔들림으로 본다. 다만 캐시가 비워져 **어느 테스트인지 이름을 남기지 못했다**. 워커 보고(직렬 128 passed)와는 다르니, 코디 `make verify` 에서 다시 나오면 그때 이름을 잡는다
- **`make test-postgres`** — 격리 `POSTGRES_TEST_URL` 이 없다. 사용자 DB(54329)는 금지라 돌리지 않았다 → **코디 몫**. 이번 판의 새 쓰기(`SubjectVersion`·`Submission`·`ReviewAssignment` 를 확정 없이 남기는 것)는 기존 confirm 과 같은 표·같은 유일 제약(`(decision_item_id, submission_version)`)을 쓴다. 그래도 PostgreSQL 의 `FOR UPDATE`·유일 제약 아래에서 저장 두 번 연속·저장 직후 확인이 도는지는 거기서 봐야 한다
- **FE 소비자** — `complete`·`completion-report` 응답에 `schedule_release` 가 **더해졌을 뿐**이다(필드 삭제 없음). FE 는 `transitionDirectTask` 결과를 `DirectTask` 로 읽고, `schedule_release` 를 읽는 곳은 캘린더 수정 경로(`CalendarPage.tsx:263`)뿐이다 → 깨지는 소비자 없음. FE 주석 `calendarWrites.ts:225` 「`schedule_release` 를 싣는 표면은 셋뿐」은 이제 넷이다(FE 몫)
- **범용 렌더러** — 워커가 짚은 대로 `ActionCenter` 상세 footer·`MessageList` `ActionCommandButtons` 는 `allowed_commands` 를 전부 그린다. 두 kind 가 그 경로로 떨어지면 「저장」 단추가 선다. 2a-1 에서 FE 가 막을 자리다

## 확인한 것 (PASS 근거)

**1. 계약 충실도 — 1-1 초안 저장**

| WP 체크박스 | 코드 | 결과 |
|---|---|---|
| 새 명령 · `revise` 재사용 검토 | `policy.py:28-35` `save_draft` 신설. `revise`(`action_center.py:263-275`)는 요청 판단의 재상신이고 `changes` 만 받아 계약이 다르다 — 이름을 나눈 이유가 맞다 | ✔ |
| 입력 = confirm+draft 와 같은 모양 · 같은 검증 | `normalize`(`action_center.py:580-610`)가 `confirm` 과 `save_draft` 를 한 분기로 처리 → `decide_ax_confirmation` 재사용(정규화·필수값·`validate_edit`) | ✔ |
| pending 유지 · 회차 +1 · diff | `_save_draft`(`:983-1037`)는 판정·실행·`resolve` 를 부르지 않고 `_open_revised_round` 만 부른다. 테스트가 `awaiting_review` · `submission_version 2` · `rounds[1].diff.title` · `decisions == []` 를 단언한다 | ✔ |
| 저장 뒤 판단 대기·대화가 새 값 | 둘 다 최신 Submission 스냅샷을 매번 읽는다(be-survey §2-3). 테스트가 `_pending` 과 대화 `actions[]` 를 둘 다 본다 | ✔ |
| 저장 뒤 draft 없는 confirm = 저장 값, 회차 안 오름 | `normalize` 가 draft 가 없으면 최신 스냅샷을 쓴다 → `revised=False` → 새 배정(저장이 연 `pending`)이 있어 통과. 테스트는 `[1, 2]` · 결정이 2회차에 붙음 · 만든 업무의 체크리스트까지 본다 | ✔ (자료가 붙은 경우는 **W1**) |
| confirm+draft 유지 | `_confirm` 이 그대로 `decision.open_round` 를 받아 `_open_revised_round` 를 부른다. 뽑아낸 함수는 원래 코드와 **줄 단위로 같다**(SubjectVersion → Submission(revises_id·diff·submitted_by) → Evidence 복사 → 앞 배정 `superseded/revised` → 새 `pending` 배정). 원래 지역 변수 `assignment` 에 담던 새 배정을 반환값으로 돌려줘 이어지는 판정·결정 기록이 같은 배정을 쓴다 → 같은 기록 | ✔ |
| 낡음 → confirm 과 같은 오류 | `decide_ax_confirmation` 그대로 → 422 「base submission version is stale」/「action version is stale」. 테스트가 저장과 confirm 의 상태·문장이 같음을 단언 | ✔ (SPEC 차이는 아래 8) |
| 변경 없음 = 200, 같은 회차 | `open_round is None` → return. 테스트 `submission_version == 1` · `rounds == [1]` | ✔ |
| effect 없음 | `/api/my-work`·`/api/work-requests` 전후 동일 단언. 업무·요청 원장 호출 0 | ✔ |
| 실시간 이벤트 없음 | 추가 0 | ✔ |
| 정책·명령 목록·편집 계약·inventory | `policy.py:135-137`(봉투) · `actions.py:533-538`(채팅 뷰 명령) · `actions.py:1856`·`:1988` `save_command` · `result_contracts.py:76-77` · inventory | ✔ |
| 두 kind 에만 | 봉투(`DRAFT_SAVE_ACTION_TYPES`)와 `normalize`(`:580-582`) 이중 경계. 테스트 `meeting.reservation.create` 거부 · 정책 단위 3케이스 | ✔ |
| 재전송 영수증 | `_is_saved_draft_receipt`(`:1039-1063`) — 같은 사람 · 앞 회차 기준 · 같은 action version · 같은 정규화 내용 해시 → 200 · 회차 안 오름. 다른 내용이면 낡음 422. 테스트가 셋 다 본다 | ✔ |

**2. confirm 회귀 · 트랜잭션** — `run_action_command` 가 한 세션이고 예외면 `_rollback_action_session`(`bootstrap/application.py:3394-3402`)이다 → 저장 도중 실패하면 반쯤 쓴 회차가 남지 않는다. 저장은 `_actions.decide`·`execute_confirmed` 를 부르지 않는다 → 업무가 생기지 않는다. `_save_draft` 가 `ActionItemRecord` 를 `FOR UPDATE` 로 잡아 confirm 과 같은 직렬화 자리를 쓴다. 기존 계약 테스트 전부 통과(`make test-contract` 병렬 1154).

**3. 권한** — 위 W2 의 첫 문장. 봉투 밖 명령은 `domain.py:164-167` 이 422 로 막는다.

**4. AI 지시문 (1-2)**
- 두 도구 설명(`tool_catalog.py:546`·`:648`): 체크리스트·내용은 「Propose the content yourself … do not leave description or checklist empty」, ID·날짜는 「come only from the conversation or lookup … Never invent an ID or a date」. 옛 「Fill every field … leave a value empty rather than inventing one」은 0곳이다
- 라우팅 정책(`codex_cli.py:466-470`)과 답변 지침(`:500-501`)은 **줄을 더하기만** 했다 — 회의 참석자·진행 묶음 등 다른 절의 「지어내지 않는다」 문장은 diff 에 없다(변경 0)
- Claude 어댑터 동일 객체 단언(`test_ax_work_lookup_policy.py`)
- `task_assign` 설명은 범위 밖이라 그대로다 — WP 1-2 가 두 도구만 말한다

**5. 마감일 채움 (1-3)**
- 찍는 2곳 모두
  - 직접 완료 `application.py:2088-2092`(transition DONE — `open → done` 포함)
  - 완료 보고 제출 `:1904-1908`
- `completed_at =` 4곳 중 지우는 2곳(보완 요청 · 재개)에는 걸리지 않았다 → 되돌리지 않는다
- 빈 칸만 · 서울 날짜: `task_projection.due_date_on_completion`(`:40-48`)이 `task_day`(=`today_for_tasks` 와 같은 시간대 함수)로 계산한다
- 배정 검증 훅: 두 자리 모두 `dates_before` → `_schedule_release_for` 다. 날짜가 실제로 바뀔 때만 돈다(`:811-820`) — 시작일 채움과 같은 수준
- 스냅샷 diff: `touch` 가 스냅샷을 남기고, 테스트가 `history/diff` 의 `due_date: None → 2026-09-10` 을 본다
- 이력: 기존 `task.state_changed`/`task.completion_submitted` 그대로 — 시작일 채움과 같은 수준
- 응답 타입 `complete → TaskDateMutationResult`: 필드가 더해졌을 뿐이다. FE 깨짐 없음(참고)
- 경계 테스트가 실제 경계를 본다 — `_INSTANT = 2026-09-09T16:30Z`(서울로는 다음 날) → `due_date == 2026-09-10`. 시계를 고정해 오늘 의존이 없다. 미래 시작일보다 앞서는 채움(검사 우회) · 이미 있는 마감일 · 보완 요청 뒤 유지 · 재개 뒤 유지 · 요청 업무의 마감일 보존도 각각 단언한다

**6. add1 라벨** — 바꾼 12곳(`actions.py` 9 · `action_center.py` 3)을 diff 와 대조해 맞았다. 서버가 만드는 업무 날짜 **값 문자열**은 배정 거절 문장 하나(`application.py:907`, `%Y/%m/%d`)다. 미리보기 값은 ISO + `kind:"date"` 로 FE 가 그린다. 유지 목록 중 오류 문구 2(`payloads.py:127` · `requests.py:296`)와 프롬프트 예시는 지시대로다. **pydantic title 7 은 화면에 나가므로 지시와 다르다 → F1**.

**7. inventory drift** — diff 줄을 집계했다.
- `save_command` 블록 **63곳**: `ActionEditContract` TypedDict 하나에 선택 필드가 붙었고, 그 타입이 `ActionProposalResult` 경유로 AX 결과를 내는 도구 output_schema 마다 박혀 있어서 생긴 것이다. 같은 변경이 반복된 것이지 다른 계약이 바뀐 것이 아니다 — 의도된 결과 계약 변경이다
- 그 밖: `TaskScheduleReleaseView`/`schedule_release` 정의(완료 결과 타입) · `complete` http_signature · 두 도구 description
- 다른 줄의 재배열·재직렬화 흔적 없음 → 「실패 diff 항목만」을 지켰다

**8. SPEC 차이(낡음 오류)** — 코디 판단(**코드가 맞고 SPEC 을 고친다**)에 반하는 근거가 **없다**. `ACTION_VERSION_STALE` 은 백엔드·프론트 어디에도 정의된 적이 없다(grep 0). 기존 confirm·판단 명령 전부가 `ActionError` → 422 + 문장이다. FE 도 그 문장으로 다시 읽는다. SPEC-002 Case Matrix 를 「422 · `base submission version is stale` / `action version is stale` — 확인과 같은 문장」으로 고치면 된다.

**9. 조용히 통과하는 자리** — 빈 단언 없음. 날짜 경계는 고정 시계로 실제 경계를 본다. 남은 것은 W4(배정 없는 업무에서 0 을 재는 단언)와 W1(자료 없는 경우만 보는 「회차 안 오름」)이다.

**10. `make test-postgres`** — 코디 몫(참고).

## 코디 확인 목록 (실물·화면)

1. **AX 업무 수정 확인 폼**(채팅 서랍, `task.update` 제안) — 지금은 칸 라벨이 「기한」이다(F1). 고친 뒤 「마감일」인지 본다. 업무 요청 수정(「기한 없애기」)·프로젝트 업무 계획 폼도 같다
2. **로컬 스택에서 「…업무 만들어 줘」 1회** — 초안 카드 체크리스트 페이지가 「없음」이 아니고, 답변이 「체크리스트·내용을 비워 두었으니 보완」을 말하지 않는다. 프로젝트·날짜를 말하지 않았으면 그 둘은 비고 답변이 그것만 말한다
3. **저장 → 카드 「N회차」** — 2a-1 이후. 수정 창 「저장」 뒤 카드가 2회차 값으로 다시 서고, 「등록」 뒤 같은 2회차에 결정이 붙는다
4. **자료를 붙인 초안**에서 저장 → 등록 — 회차가 3으로 오르는지(W1 결정 전 현재 동작)
5. **마감일 없는 업무 완료**(서울 00:00~09:00 사이면 경계까지) — 상세 마감일이 그날로 선다. 보완 요청·재개 뒤에도 남는다
6. `make test-postgres`(격리 DB) · `make verify` — 직렬 패스 흔들림 재현 여부와 실패 테스트 이름
