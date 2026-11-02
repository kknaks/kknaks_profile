# 리뷰 리포트 — strong-hajin-polish / backend (WORK-008 Phase 3a) (2026-10-01)

## 판정: WARN

FAIL 사유 없음. 경미 4건(W-1~W-4)은 진행을 막지 않는다. 수정 여부는 코디가 판단한다.

## 검수 범위
- diff: `9255028` 위 **미커밋** 변경 중 `backend/` 6개 + `docs/unified-operations-inventory.json` 1개 (untracked 백엔드 파일 없음). `frontend/` 는 제외.
  - `backend/src/ax_workspace/entrypoints/mcp.py` · `modules/actions/results.py` · `modules/ax_execution/tool_catalog.py` · `platform/action_center.py` · `platform/actions.py` · `backend/tests/contract/test_action_center.py` · `docs/unified-operations-inventory.json`
- 실행한 검사: `git diff` 정독 · grep(`기한을 입력` · `due_date.*required` · `required.*True` · AX 경로 `due_date` 전수 · `create_work_request(` 호출부 전수 · `created_at`/`submitted_at` 관례) · 정규화/편집 계약/실행기/MCP 시그니처를 생성 명령 모델과 직접 비교
- 테스트: `make test-unit` → **389 passed** (architecture 경계 · operation inventory drift 포함). `make test-contract` 는 다시 돌리지 않았다 — 워커 보고 1128+128 통과를 그대로 적는다. 서버·DB 는 띄우지 않았다.

## 위반 (FAIL 사유)
- 없음

## 경미 (WARN)

### W-1 `docs/unified-operations-inventory.json` 이 발주서 §3 allowed_paths 밖이다 — 발주서 안의 모순
- 발주서 §3 은 `backend/src/ax_workspace/` · `backend/tests/` 만 허용한다(WP「BE allowed paths (Phase 3a)」도 같다). 그런데 발주서 §2 마지막 줄과 WP Phase 3a 계약 6번은 「operation inventory drift 는 실패 diff 의 그 항목만 패치」하라고 **시킨다**. AGENTS.md 도 MCP 시그니처를 바꾸면 이 파일을 패치하라고 한다. 이 파일은 `docs/` 에만 있으니 계약을 지키면 §3 을 벗어날 수밖에 없다.
- reviewer rules 4(「allowed_paths 이탈 = 무조건 FAIL」)를 글자대로 적용하지 않은 이유: 원 발주서가 이 경로에 쓰라고 명시했고, diff 도 drift 항목 6개뿐이다(아래 「확인한 것」 4).
- 권장: 코디가 이 경로 사용을 추인한다. 다음 BE 발주서부터는 §3 에 `docs/unified-operations-inventory.json` 을 넣는다.

### W-2 P-1 대조 테스트의 일부는 같은 원천을 양쪽에 써서 늘 참이다
- `backend/tests/contract/test_action_center.py:859-860`: `normalize_ax_draft(...)` 의 키 집합을 `TaskCreateInput.model_fields` / `WorkRequestCreateInput.model_fields` 와 비교한다. 그런데 정규화 자체가 `TaskCreateInput.model_validate(...).model_dump()` 이고(`modules/work/drafts.py:24`, 요청은 `:52`), 허용 키 목록도 `frozenset(<Model>.model_fields)` 다(`drafts.py:12,14`). 그래서 이 두 줄은 정의상 늘 참이다.
- `:836` `set(edit_contract.values) == set(model.model_fields)` 도 같다. `values` 는 같은 `normalize_task_draft` / `normalize_work_request_draft` 결과다(`platform/actions.py:1695`, 요청 계약).
- 정규화가 나중에 모델이 아닌 다른 것을 쓰게 되면 잡아 주므로 회귀 방지 값은 조금 있다. 다만 P-1 의 「빠짐없이」를 실제로 재는 줄은 손으로 적은 목록과 모델을 비교하는 **`:872-873`(편집 계약 field id)** 와 **`:881-884`(MCP input_schema)** 뿐이다. 이 줄들은 의미가 있고 통과한다.
- 권장: 리포트나 테스트 docstring 에 「정규화·values 는 구성상 모델과 같다. 실제로 재는 것은 fields·MCP 다」라고 적는다. 테스트를 고칠 필요는 없다.

### W-3 `created_at` 의 시간대 표기를 테스트가 잡지 않는다
- `platform/action_center.py:759` `record.created_at.isoformat()`. 컬럼은 `DateTime(timezone=True)`(`platform/persistence.py:795`)이고 쓸 때 `datetime.now(UTC)`(`platform/actions.py:265,279`)를 쓴다. Postgres 에서는 `+00:00` 이 붙는다. SQLite(계약 테스트 스택)에서는 tz 없이 돌아올 수 있다. tz 없는 ISO 문자열을 FE 가 `new Date()` 로 읽으면 로컬 시각으로 해석해 「만든 지 며칠」이 9시간 어긋날 수 있다.
- 기존 `submitted_at`(`action_center.py:532`, `:1108`)도 같은 방식이라 새로 생긴 문제는 아니다. 다만 3b FE 가 이 값으로 날짜 계산을 하므로 계약으로 굳혀 둘 가치가 있다. 테스트는 `made.year >= 2026`(`test_action_center.py:840`)만 본다.
- 권장(선택): 운영(Postgres) 기준 「tz 포함 ISO 8601」을 FE 계약으로 적어 둔다. 또는 `test-postgres` 에 tzinfo 단언을 하나 더한다.

### W-4 뒤집은 「필수」 테스트의 업무 쪽 절반은 옛 동작과 새 동작을 가르지 못한다
- `test_action_center.py:770` `blank.status_code == 422 and "기한" not in blank.text`: 제목이 공백인 초안은 **옛 코드에서도** 정규화(제목 검증)에서 먼저 막혀 「기한」 문구가 나오지 않았다. 그래서 이 단언은 기한 필수를 되살려도 통과한다.
- 옛 동작과 새 동작을 가르는 것은 `:733` 테스트(기한 없는 confirm 이 200, 업무 `due_date is None`)이고, 이것만으로 회귀는 막힌다. `:757` 요청 쪽 절반(필수가 `{title, assignee_id}` 뿐, 담당 없으면 422, 기한 없이 발송 200)은 의미가 있다.
- 권장: 그대로 둬도 된다. 테스트 이름이 말하는 것보다 재는 것이 적다는 점만 기록한다.

## 의견 — `supersedes_request_id` 제외 (§3-6)
- **판단은 맞다고 본다.** SPEC-001 S-9 6 은 「초안은 생성 명령의 필드 **전부**를 싣는다」고 하고, SPEC-002 §4 표도 「없는 필드를 빼고 싣지 않는다」고 한다. 이번 diff 에서 `supersedes_request_id` 는 **`edit_contract.values` 에 그대로 실린다**(정규화가 모델 전부를 덤프한다). 「싣는다」는 조건은 글자대로 채운다.
- 편집 계약 `fields` 와 MCP 인자에서 뺀 것은 이 값이 만들기 창의 **편집 칸**이 아니기 때문이다. 재요청은 취소된 요청에서 `initial` 로 미리 채워 여는 자리다(WP 1-1 「재요청」·SPEC-003 §4 발송 `supersedes_request_id`). 그러니 「같은 필드·같은 필수·같은 검증」과 어긋나지 않는다. AI 가 대화만으로 재요청 계보를 지어내지 못하게 하는 효과도 있다.
- 권장: SPEC-001 S-9 6 이나 WP 3a 완료 증거에 「`supersedes_request_id` 는 값으로만 싣고 칸으로 세우지 않는다」를 한 줄 남긴다(문서 몫이고 코드 수정은 아니다).

## 기존 부채 (이번 판정 제외)
- `platform/actions.py` task.create_self 편집 계약의 approver 칸 주석 「요청 초안에는 이 칸이 없다 (SPEC-001 §7 OQ-M)」는 이미 낡았다. 요청 계약에도 결재자 칸이 있고, `WorkPayloadFields` docstring 도 「승인자·선행 업무는 여기 없다」고 하는데 실제로는 있다(`modules/work/task_creation.py:44-68`). 이번 diff 밖이다.
- `submitted_at` 도 SQLite 에서 tz 없이 나올 수 있다(W-3 과 같은 뿌리).

## 확인한 것 (PASS 근거)

1. **P-1 필드 대조** — 생성 명령: `TaskCreateInput`(= `WorkPayloadFields` + `assignee_id`. `creation_commands.py` 가 import 해 쓰는 같은 모델), `WorkRequestCreateInput`(+ `assignee_id` 필수 · `supersedes_request_id`).

   | 필드 | Task 정규화/스냅샷 | Task 편집 계약 | `task_create_self` MCP | Req 정규화/스냅샷 | Req 편집 계약 | `work_request_create` MCP |
   |---|---|---|---|---|---|---|
   | title (필수) | ✓ | ✓ req | ✓ req | ✓ | ✓ req | ✓ req |
   | description | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
   | assignee_id | ✓ | ✓ (본인·고정) | ✓ | ✓ 필수 | ✓ req | ✓ req |
   | start_date | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
   | due_date | ✓ | ✓ **선택(이번)** | ✓ | ✓ | ✓ 선택 | ✓ |
   | project_id | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
   | cc_member_ids | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
   | preceding_task_ids | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
   | approver_id | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
   | checklist | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
   | reference_task_ids | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
   | parent_task_id | ✓ | ✓ **(이번)** | ✓ | ✓ | ✓ **(이번)** | ✓ **(이번)** |
   | supersedes_request_id | — | — | — | ✓ (값) | 제외 | 제외 |

   - 정규화·스냅샷: `normalize_task_draft` / `normalize_work_request_draft` 가 모델 전체를 덤프한다(`drafts.py:24,52`). confirm 의 `final_snapshot` 도 그 결과다(`modules/actions/confirmation.py` decide).
   - 실행기: `work_request.create` 는 `**command.model_dump()` 를 그대로 넘긴다(`platform/actions.py:706-716`). 요청 application 은 `parent_task_id` 를 실제로 쓴다(`modules/work/requests.py:393-447`). 새로 연 칸이 실행에서 버려지지 않는다.
   - MCP: `facade.create_work_request` 의 위치 인자 끝에 `parent_task_id` 를 붙였고, 호출부는 `mcp.py:1652` 하나뿐이며 순서가 맞다. 다른 `create_work_request(` 호출부(bootstrap·http·meetings)는 application 쪽이라 영향이 없다.
   - 어노테이션 `parent_task_id: str | None` 은 기존 `task_create_self`(`mcp.py:718`) 관례와 같다.

2. **AX 전용 검사 전수** — `기한을 입력`·`due_date.*required`·AX 경로 `due_date` 를 grep 했다. 남은 것은 preview 표시(`_date(...)`), 수정 제안 `clear_due_date`(`modules/actions/payloads.py:122-129`, 생성 경로가 아니다), `WorkRequestAmendCommand` 의 empty_policy(`command_contracts.py:54`, 생성 경로가 아니다)뿐이다. 생성 초안에 걸린 AX 전용 필수·검증은 **0** 이다. 편집 계약의 required 는 task `{title, assignee_id(고정)}`, request `{title, assignee_id}` 이고 「새 업무 추가」와 같다.

3. **confirm + draft 경로 보존** — `action_center.py:588-597` 은 정규화 결과를 `normalized["draft"]` 에 바로 넣는 것 말고는 바뀌지 않았다. `decide_ax_confirmation`(회차 +1 · `payload_diff` · `validate_edit`)은 diff 0줄이다. `:796` 테스트가 회차 `[1,2]`, title diff, 스냅샷 `due_date None` 을 단언한다.

4. **봉투 `created_at`**
   - `AxProposalActionHandler` 가 모든 `ax.*` 봉투를 만든다(`kind=f"ax.{record.action_type}"`, `action_center.py:723`). 목록과 상세가 같은 빌더라 둘 다에 실린다(테스트 `:839`). 형식은 `datetime.isoformat()` 이다(W-3 참고).
   - 다른 핸들러(DecisionItem·업무 요청·배정) 봉투에는 넣지 않았다. `ActionEnvelopeExtensions.created_at` 이 `NotRequired` 라(`modules/actions/results.py:23`) 다른 봉투의 모양은 바뀌지 않는다.
   - 이름 `created_at` 은 같은 결과 모듈의 기존 관례(`ActionAttachmentView`·`ActionDiscussionView` 의 `created_at: str`, `results.py:85,92`)와 같다. 회차 행의 `submitted_at` 과는 층위가 달라 충돌하지 않는다.

5. **계층 경계** — `modules/actions/results.py` 는 TypedDict 한 줄, `modules/ax_execution/tool_catalog.py` 는 설명 문자열만 바뀌었다(fastapi/mcp/sqlalchemy import 없음). `entrypoints/mcp.py` 는 `modules` 모델만 쓴다. `make test-unit` 의 architecture 테스트가 통과한다.

6. **envelope 를 서버가 만드나** — 편집 계약(required·options·editable)과 `created_at` 을 모두 `ActionPresenter` / `AxProposalActionHandler` 가 쓴다. FE 가 추론할 자리는 생기지 않았다.

7. **operation 재사용** — 새 도구·새 엔드포인트가 없다. 기존 `task_create_self`·`work_request_create`·`GET /api/action-items` 를 넓히기만 했다. 편집 칸의 options 는 기존 `reference_options` 를 재사용한다.

8. **inventory diff 범위** — 6개 항목뿐이다. `ActionEnvelopeResult.created_at` 3곳 + 최상위 properties 1곳, 도구 설명 2개(`task_create_self`·`work_request_create`), `work_request_create.parent_task_id` 입력 스키마 1개. 전체 재작성 흔적은 없다. drift 테스트도 통과한다.

9. **도구 설명** — 두 설명 모두 「새 업무 추가」 form 의 필드를 채워 초안을 만든다는 말과 전 필드 목록, 「기한은 선택이니 지어내지 말라」를 담는다. 테스트 `:885` 가 「새 업무 추가」 문구를 단언한다.

10. **예외** — 새 `HTTPException`·`except Exception` 이 없다. 기존 `ActionError` 경로를 그대로 쓴다.

11. **스키마** — DDL·`create_all` 변경이 없다. 새 표도 없다.

12. **allowed_paths** — `frontend/` 를 건드리지 않았다(`frontend/` 변경은 Phase 2 FE 워커 몫). `docs/` 1건은 W-1 에 적었다.

13. **확인 안 함** — `make test-contract`·`make test-postgres` 는 다시 돌리지 않았다(워커 보고를 믿었다). 상위 업무 options 가 「한 단계」 제약(상위가 이미 하위인 업무)을 미리 거르지 않는 점은 선행 칸과 같은 방식이다. 서버가 실행 때 `parent_for` 로 다시 거른다(`requests.py:393`). 위반으로 보지 않는다.

## 3b FE 가 쓸 계약 (요약)

| 자리 | 필드 | 모양 | 비고 |
|---|---|---|---|
| `GET /api/action-items` · `GET /api/action-items/{id}` 의 `ax.*` 봉투 | `created_at` | ISO 8601 문자열(운영 Postgres 는 `+00:00` 포함) | 「만든 지 며칠」의 원천. **`ax.*` 에만** 있고 다른 kind 에는 없다 → optional 로 다룬다 |
| 같은 봉투 `edit_contract.values` | 초안 필드 전체 | Task: `title, description, start_date, due_date, project_id, parent_task_id, checklist[], reference_task_ids[], cc_member_ids[], preceding_task_ids[], approver_id, assignee_id`. Request: 같은 것 + `supersedes_request_id` | 카드 요약은 여기서 읽는다. 날짜는 `YYYY-MM-DD` 또는 `null`, UUID 는 문자열 |
| `edit_contract.fields[]` | `{id, label, type, required, editable, options?, value?, label_value?}` | Task 12칸 · Request 12칸(`supersedes_request_id` 칸 없음) | `due_date.required` 는 이제 **false**. required 는 task `title`(+`assignee_id` 고정 person), request `title`·`assignee_id` |
| 새 칸 `parent_task_id` | `type: "select"`, label 「상위 업무」, options = 읽을 수 있는 업무(`{value: task_id, label: title}`) | task·request 둘 다 | 단일 선택. 비우면 `null` |
| confirm 명령 | `draft` = 위 values 모양 전체 · `base_submission_version` · `expected_version` | 변경 없음 | 고친 draft 면 회차 +1, diff 기록 |
| 자료 | `material_drafts[]` (기존) | 변경 없음 | 「파일 N · 링크 N」 요약은 여기서 센다(S-9 6) |
