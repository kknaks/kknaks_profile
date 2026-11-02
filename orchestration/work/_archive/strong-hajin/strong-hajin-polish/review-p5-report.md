# 리뷰 리포트 — strong-hajin-polish / Phase 5 AX 탐색 (backend) (2026-10-01)

## 판정: FAIL

**FAIL 1 · WARN 3 · 참고 2.**
- 계약 1~3은 문구 · 스키마 · bind로 모두 섰다. 권한 없는 프로젝트가 근거로 새는 길도 찾지 못했다(읽을 때 소유 모듈이 다시 확인한다).
- 다만 **`list_projects`에 붙인 `_remember`가 회의 배치 · 합성의 `project_list` 도구를 깨뜨린다.** 계약 1의 「다른 흐름을 깨지 않나」에 걸린다(FAIL-1). 한 줄로 닫히고, 같은 원인으로 이미 깨져 있던 `task_list` · `meeting_get`도 함께 닫힌다.

## 검수 범위
- 대상: HEAD `94cacfd` 위 `backend/` · `docs/` 미커밋 8파일 + 신규 `tests/unit/test_ax_work_lookup_policy.py`. `frontend/`는 대상이 아니다.
- 기준: WP Phase 5 · `research-graph-search.md` · `strong-hajin-polish-be-p5-brief.md`
- 실행한 검사
  - diff 정독
  - 호출 경로 추적
    - `_remember` → `record_answer_resources` → `record_resources`
    - 읽기 쪽 `_SessionAnswerResources.resolve`
    - causation id 출처
  - `UUID("meeting-batch:abc")` → `ValueError` 직접 확인
  - `make test-unit`: **401 passed**
  - `make test-contract`: **1139 + serial 128 passed**, 실패 0

## 위반 (FAIL)

### FAIL-1 회의 배치 · 합성의 `project_list`가 이제 매번 실패한다
- **경로**
  1. 회의 배치와 합성은 MCP를 `causation_id=f"meeting-batch:{persona_id}"` · `f"meeting-finalize:{persona_id}"`로 띄운다(`bootstrap/application.py:613` · `:502`).
  2. 이 값이 그대로 `AX_MCP_CAUSATION_ID`가 된다(`platform/codex_cli.py:362`, Claude `claude_cli.py:294`).
  3. 회의 레지스트리에는 `project_list`가 있다(`bootstrap/settings.py:13` `DEFAULT_MEETING_AI_TOOLS = ("task_list", "project_list", "meeting_get", "member_list")`).
  4. 이번 diff에서 `McpReportsFacade.list_projects`가 `self._remember(...)`를 부르게 됐다(`entrypoints/mcp.py:1294-1300`).
  5. `_remember`는 causation이 비어 있을 때만 넘어간다. 그 밖에는 `UUID(causation_id)`를 부른다(`mcp.py:474-479`).
  6. `"meeting-batch:<id>"`는 UUID가 아니므로 **`ValueError: badly formed hexadecimal UUID string`**이 난다. 그래서 `project_list` 도구가 오류로 끝난다.
- **영향**
  - 회의 후속업무에 프로젝트를 고르던 재료가 사라진다. 회의 배치 · 합성은 실패하지 않고 모델이 도구 없이 넘어간다. **조용한 품질 저하**다.
  - 실행 단계 기록에는 「× 실패」가 남는다.
- **같은 원인의 기존 결함(이번 diff 전부터)**: `task_list`(`list_tasks` → `_remember_tasks`, `mcp.py:486-494`)와 `meeting_get`(`get_meeting` → `_remember`, `mcp.py:800-805`)도 회의 배치에서 같은 이유로 이미 실패하고 있었다. 이번 diff로 회의 레지스트리 넷 중 셋이 깨지고 `member_list`만 남는다.
- **테스트가 못 본다**: 계약 테스트는 대화 턴(UUID causation)만 돈다. 회의 causation으로 MCP 읽기 도구를 부르는 시험이 없다.
- **권장(한 자리)**
  - `_remember`에서 causation이 UUID가 아니면 기억하지 않고 넘어간다. 대화 턴이 아닌 실행은 답변 근거가 필요 없다.
  - 그러면 `record_resources`의 「execution not found」 `ValueError`(`platform/work_tasks.py:197-199`)를 회의 쪽에서 밟을 일도 없다.
  - 시험: `AX_MCP_CAUSATION_ID="meeting-batch:x"`로 `list_projects` · `list_tasks` · `get_meeting`이 값을 돌려준다.
  - 기존 결함까지 함께 닫히므로 코디가 범위를 정한다.

## 1. 계약 대조

| 항목 | 결과 | 근거 |
|---|---|---|
| 1 「한 후보로 확정될 때만 채우고, 못 찾거나 여럿이면 비우고 말한다, ID를 지어내지 않는다」 | PASS | 정책 `codex_cli.py:461-466`: 「**한 후보로 확정될 때만** … 채운다. 못 찾았거나 후보가 여럿이면 비워 두고, 답변에 「연결할 프로젝트를 찾지 못했습니다」처럼 무엇을 비웠는지(후보가 여럿이면 그 이름들)를 말한다. 조회 결과에 없는 ID를 지어내지 않는다」. 도구 설명 `tool_catalog.py:546` · `:648`: 「Fill a link only when one candidate clearly matches; if none or several match, leave it empty and say so in the answer — never invent an ID」. 대화 지침 `:402-404`도 업무 생성 전에 프로젝트 · 기존 업무 조회를 말한다 |
| 1 「graph_search 먼저 부르지 말라」 축소가 사람 찾기를 깨나 | PASS | `:458-460`: 「**사람을 찾으려고** `graph_search`를 먼저 호출하지 않는다 — 직책·소속 관계로 사람을 특정하거나 관계 자체를 물었을 때만 graph로 사람을 찾는다」. 수신자는 여전히 후보 도구(`work_request_assignee_candidates` · `task_assignment_candidates`)가 먼저다(`:455-457` 불변). 금지의 대상이 「사람 찾기」로 좁혀졌을 뿐, 사람 흐름의 규칙은 그대로다 |
| 1 `project_list` 「회의용」 풀기 | PASS | 제목 「프로젝트 후보 조회」, 설명에 Task · WorkRequest(`tool_catalog.py:432-434`) |
| 1 Claude 어댑터 동일 | PASS | 두 어댑터가 같은 정책 객체를 쓴다. 테스트 `test_the_claude_adapter_reads_the_same_policies`가 `is`로 단언한다 |
| 2 `project` 참조 종류 | PASS | `answer_documents.py:22` 패턴에 `project`. 출력 스키마까지 반영됐다(`test_the_provider_output_schema_admits_project_references`). 허용 ref 문구에 `project:<project_id>` + 「프로젝트를 task:로 가리키지 않는다」(`codex_cli.py:477-481`) |
| 2 graph로 본 대상이 근거로 묶임 | PASS | `mcp.py:1032-1068`. overview · search · neighbors가 `task` · `work_request` · `meeting` · `project` node만 기억한다. 사람 · 팀 · 자료 · 보고서는 뺐다(자료 · 보고서는 무결성 근거가 있는 소유 도구로만 근거가 된다). 계약 테스트 3건(graph search · neighbors · list_projects) + 「프로젝트를 task:로 가리키면 여전히 실패」 1건 |
| 2 권한 없는 프로젝트가 새나 | **새지 않는다** | 아래 §2 |
| 3 graph_search 인자 설명 = 스키마 | PASS | 실제 서명 `mcp.py:1930` `graph_search(query: str, limit: int = 20)`. 설명(`tool_catalog.py:397`) 「Arguments are exactly `query` … and optional `limit`; there is no kind filter」. 정책(`codex_cli.py:382-383`)도 같다. `kinds`를 떠올리게 하던 「시작 종류는 …」 문구는 지웠다 |
| inventory는 문자열만 | PASS | `docs/unified-operations-inventory.json` diff 5곳 = `list_projects` · `graph_search` · `task_create_self` · `project_list`(제목+설명) · `work_request_create`의 description/title뿐. 스키마 · exposure 변경 0 |

## 2. 누설 · 오인용 (계약 2)

- **기록 범위**
  - `_remember`가 남기는 것은 `(type, id, version)`뿐이다. 제목 · 상태는 저장하지 않는다.
  - 기록 대상은 graph · 프로젝트 조회가 **이 principal에게 이미 돌려준** node다. graph 응답 자체가 소유 모듈의 권한 조회를 거친 「authorized nodes」다(`application.py:687-699`, 조사 §3).
  - `record_resources`는 턴의 대화 소유자가 principal과 다르면 거부한다(fail closed, `work_tasks.py:200-202`).
- **읽기 시 재인가**
  - 대화를 읽을 때마다 `_SessionAnswerResources.resolve`(`application.py:296-345`)가 `project` → `readable_project`(`_EAGER_LOOKUP`, `:293`)로 다시 묻는다.
  - 지금 읽을 수 없으면 그 줄을 **통째로 뺀다**(제목 · 개수 모두 없음). 저장된 답변 요소는 `project_answer_document`가 ref를 `None`으로 가린다(`answer_documents.py:100-110`).
  - 프로젝트에서 빠진 사람이 예전 답변을 열어도 이름이 보이지 않는다. **새지 않는다.**
- **범위가 넓어져 생기는 일(WARN-1)**
  - `graph_overview`는 한 번에 최대 120 node를 기억한다.
  - 모델이 「본 적 있는」 대상이 많아질수록 **실제로 확인하지 않은 대상을 근거로 삼는 오인용**의 문턱이 낮아진다. 예: overview에서 스치기만 한 업무를 「관련 업무」로 인용하는 경우다.
  - 권한 누설은 아니다. 근거 품질 문제다.
  - 정책(`codex_cli.py:380-381` 「주대상이 Task·업무 요청·회의이면 해당 소유 조회 도구로 한 번 확인하여 정본 링크를 남긴다」)이 이를 막는 유일한 장치다. 코드상으로는 overview node도 묶인다.
  - 필요하면 overview는 기억에서 빼는 것을 검토한다(search · neighbors는 의도적 탐색이라 유지).
- **참고 R-1** `get_project`는 `resource_id`를 인자 문자열 그대로 기록한다(`mcp.py:1304`). 대문자 · 하이픈 없는 UUID로 부르면 `project:<정규형>` ref와 맞지 않아 bind가 실패할 수 있다. `str(UUID(project_id))`로 정규화하면 닫힌다. 모델은 도구 결과의 id를 그대로 쓰므로 실제 빈도는 낮다.

## 3. `test_material_identity` 단언 좁힘 — 정당한가

- 변경(`tests/contract/test_material_identity.py:47-53`): `after['answer_resources']` 전체 → **`resource_type == 'material'`인 것만** 본다.
- 이 시험의 계약은 「자료 결합을 떼면 그 **자료 관찰**은 다른 읽을 수 있는 문맥으로 되살아나지 않는다」다. 이번 변경으로 같은 턴의 graph neighbors가 **업무 node**(task:first/second)도 기억하게 됐다. 그 업무들은 MINA가 읽을 수 있으므로 정당하게 남는다. 그래서 전체 `== []` 단언은 성립할 수 없다.
- 자료에 대한 단언(관찰 1건 · `source_contexts == {second}` / 0건)은 **그대로**다. **계약 약화가 아니다** — PASS.
- 다만 「자료 말고 무엇이 남는가」를 이제 아무도 보지 않는다(WARN-2). `{(type, id)} == {("task", first), ("task", second)}`처럼 기대 집합을 적으면, 예상 밖의 종류(person · team 등)가 섞이는 회귀도 잡힌다.

## 4. 경미 (WARN) · 참고

- **WARN-1** graph overview까지 기억해 근거 범위가 넓다(§2).
- **WARN-2** `test_material_identity`의 비자료 근거를 보는 단언이 없다(§3).
- **WARN-3 조용히 통과하는 자리**
  - FAIL-1: 회의 causation으로 MCP 읽기 도구를 부르는 시험이 없다.
  - 「프로젝트 접근을 잃은 뒤 예전 답변」 시험이 없다. 재인가는 기존 공용 경로(`resolve`)라 동작한다고 판단하지만, `project` 종류로 단언한 시험은 없다.
  - 정책 회귀 단언(`test_ax_work_lookup_policy.py`)은 **문구 존재**만 본다. 모델이 실제로 탐색하는지는 가짜 provider로 볼 수 없다. E2E로 남긴다(아래).
  - 묶지 못한 참조 **하나**가 여전히 턴 전체를 실패시킨다(`answer_documents.py:86-96` · `conversation_worker.py:222-229`, 조사 §4-A). 이번 계약은 「프로젝트를 가리킨 답변」만 살렸다. 다른 잘못된 ref(예: 회의 id를 `task:`로)는 그대로 턴 실패다. 범위 밖이지만 남는 위험이다.
- **참고 R-2** `persistence.py:1521` `ConversationAnswerResourceRecord.resource_type` 주석에 `project`가 없다(diff 밖, 문서 drift). DB 제약은 없어서(String(40), CHECK 없음) 동작에는 지장이 없다.
- **FE**: `project:` 참조를 그리는 일은 다른 워커 몫이다(발주 기준). BE는 `answer_resources`에 `resource_type: "project"` · 제목(`name`) · 상태를 낸다(`resolve`).

## 5. 사용자 E2E 후보

1. 「하반기 제품 개편 프로젝트에 리서치 문서 작성 업무 만들어 줘」 → 초안 카드의 업무 연결 페이지에 그 프로젝트가 찍혔는지 본다.
2. 이름이 비슷한 프로젝트가 둘인 상태에서 요청한다 → project가 비고, 답변에 두 후보 이름이 나오는지 본다.
3. 없는 프로젝트 이름으로 요청한다 → 비우고 「연결할 프로젝트를 찾지 못했습니다」 류가 나오는지 본다.
4. 「왜 프로젝트에 연결이 안 됐어?」 → 턴이 성공하고 답변에 프로젝트 링크가 서는지 본다(FE 렌더 포함).
5. 「김○○님에게 … 요청해 줘」 → 수신자를 여전히 후보 도구로 찾는지 본다(실행 단계에 graph_search가 먼저 나오지 않는지).
6. 실행 단계에 `graph_search` 「× 실패」(지어낸 `kinds`)가 더는 없는지 본다.
7. **(FAIL-1 수정 뒤)** 회의 하나를 진행 · 종료한다 → 실행 기록에 `project_list` · `task_list` 실패가 없고, 후속업무 후보에 프로젝트가 붙는지 본다.

## 확인한 것
- 계약 1~3 ✔ · Claude 동일 ✔ · inventory 문자열만 ✔ · 권한 누설 없음(읽기 시 재인가) ✔
- `test_material_identity` 좁힘 = 정당(자료 단언 그대로) ✔
- 회의 레지스트리 도구 회귀 ✗(FAIL-1)
- allowed: backend/docs만 변경 ✔ · `make test-unit` 401 · `make test-contract` 1139 + 128, 실패 0 ✔
