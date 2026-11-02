# 조사: E2E-12 — AX 대화의 `graph_search` 즉시 실패와 「프로젝트 연결 안 됨」

조사자: backend 워커(read-only). 로컬 스택 DB `ax_demo_polish` 는 SELECT 만 했고, 로컬 Codex rollout 파일(`backend/.scax/codex-runtime/sessions/…`)은 읽기만 했다. 코드 수정·서버 재시작·codex 실행·운영 접근은 하지 않았다.

## 0. 한 줄 원인

**`graph_search` 의 22ms 실패는 모델이 없는 인자 `kinds:["project"]` 를 지어내서 생겼다. MCP 서버가 `Unknown arguments: kinds` 로 거절했고, 모델은 같은 턴에서 인자 없이 다시 불러 성공했다. 사용자에게는 무해한 잡음이다.** 사용자가 실제로 본 문제는 두 가지다.
1. 처음 업무 생성안을 만들 때 AX 가 프로젝트를 탐색하지 않아 `project_id` 가 비었다. 탐색하라는 지침이 없다.
2. 「왜 연결이 안 됐냐」는 두 턴(원래 턴과 재시도)이 **턴 전체 실패**로 끝났다. 답변이 프로젝트를 가리키려 했지만 답변 참조 형식에 `project` 종류가 없다. 모델은 `task:<프로젝트 id>` 를 냈고 서버가 묶지 못했다(「답변의 참조를 확인하지 못했습니다」).

그래프 인덱스·권한·MCP 가드는 원인이 아니다. 그래프는 원장에서 바로 읽고(별도 인덱스 없음), 같은 턴의 `graph_search` 와 `graph_neighbors` 가 정상으로 결과를 냈다.

## 1. 증거

### 1-1. 도구 호출 기록 (`tool_invocations`, 2026-10-01 UTC)

| turn | seq | tool | state | ms | 입력 요약 |
|---|---|---|---|---|---|
| ecab56f3 (「…리서치 문서 작성 업무 만들어줘」) | 1-2 | material_search | completed | | query=하반기 제품 리서치 … |
| ecab56f3 | 3 | **task_create_self** | completed | 159 | title, description, checklist[4], idempotency_key — **project_id 없음** |
| 1bb8e2a7 (「프로젝트가 하반기 제품 개편 아니야?」) | 1-2 | graph_search, graph_neighbors | completed | 115/393 | |
| 0d2bc2e4 (「왜 프로젝트에 연결이 안됐냐고」) | 1 | **graph_search** | **failed** | **22** | query=하반기 제품 개편, **kinds=[1건]** |
| 0d2bc2e4 | 2-5 | graph_search ×2, graph_neighbors, action_item_list | completed | | kinds 없음 |
| c6adb8b5 (같은 질문 재시도) | 1-3 | graph_neighbors, graph_search, action_item_list | completed | | |

### 1-2. Codex rollout (실제 인자·오류·최종 답변)

`rollout-2026-10-01T17-55-32-01a0f6ad-10ba-….jsonl` (턴 0d2bc2e4):
```
EXEC  tools.mcp__scax__graph_search({query:"하반기 제품 개편", kinds:["project"]})
MCP   graph_search args={"query":"하반기 제품 개편","kinds":["project"]} status=failed
      result: {"content":[{"type":"text","text":"Unknown arguments: kinds"}],"isError":true}
EXEC  graph_search({query:"하반기 제품 개편"}) → project:ea0939bf-… 「하반기 제품 개편」 (성공)
...
final_answer: {"body":"… {{project}}와의 연결이 잡히지 않았습니다 …",
               "elements":[{"key":"project","type":"resource_reference","ref":"task:ea0939bf-eaf3-46da-8793-bb3ddb46a075"}]}
```
`rollout-…17-56-05-01a0f6ad-92b2-….jsonl` (재시도 c6adb8b5): `kinds` 실패는 없었다. 최종 답변은 **똑같이 `ref:"task:<프로젝트 id>"`** 였다.

### 1-3. 턴 결과 (`conversation_turns` / `conversation_audit_events`)
- 0d2bc2e4, c6adb8b5: `state=failed`, `normalized_error="답변의 참조를 확인하지 못했습니다. 다시 요청해 주세요."`. assistant 메시지는 `body_state=failed` 이고 본문이 비어 있다.
- 두 턴의 `conversation_answer_resources` 는 **0행**이다. `conversation_graph_receipts` 에는 node/edge 영수증이 남았다.

### 1-4. 코드
- `kinds` 를 받지 않는 서명: `backend/src/ax_workspace/entrypoints/mcp.py:1905` `graph_search(query: str, limit: int = 20)`.
- 모델이 `kinds` 를 떠올릴 만한 문구: `platform/codex_cli.py:382` 「graph_search **시작 종류는 person/team/project/task/work_request/meeting** 이다」. 종류 필터가 있는 것처럼 읽힌다(추정).
- 턴 전체 실패 지점: `bootstrap/conversation_worker.py:222-229` `_complete` → `bind_answer_resources` 가 실패하면 `ProviderResponseInvalid("답변의 참조를 확인하지 못했습니다…")`.
- 참조 종류 제한: `modules/ax_execution/answer_documents.py:22` `ResourceRef` 패턴이 `^(task|meeting|work_request|material|report):…$` 다. **`project` 가 없어서** 출력 스키마가 프로젝트 참조를 받지 않는다. 그래서 모델은 `task:` 를 붙였다.
- 묶기 규칙: `answer_documents.py:86-96` 은 이 대화에서 `_remember` 로 기록된 `answer_resources` 만 허용하고, 하나라도 없으면 전체 실패다.
- graph 도구는 `_remember` 를 부르지 않는다: `entrypoints/mcp.py:1039-1050` `graph_search`·`graph_neighbors` 는 graph 영수증만 남긴다(`bootstrap/application.py:2597-2625`). `_remember` 를 부르는 쪽은 task/meeting/work_request/material 소유 도구다(`mcp.py:474-479` 외). 그러니 `project:` 종류가 허용됐더라도 graph 로만 본 대상은 묶이지 않는다.

## 2. 업무 생성 때 프로젝트·기존 업무 탐색 흐름

**탐색하도록 되어 있지 않다.** 도구 서명에는 필드가 있지만, 채우라는 지시가 「대화가 준 값」으로 한정된다.
- `task_create_self` 서명에는 `project_id`, `reference_task_ids`, `preceding_task_ids`, `parent_task_id` 가 있다(`entrypoints/mcp.py:1979-1992`).
- 도구 설명 `modules/ax_execution/tool_catalog.py:546` (task_create_self), `:648` (work_request_create): 「**Fill every field the conversation gives you** … project_id … preceding_task_ids … reference_task_ids」. 대화에 없는 값을 찾아 채우라는 말이 없고, 「지어내지 말라」 쪽만 있다.
- 시스템 지침 `platform/codex_cli.py:449-458` `WORK_AND_REPORT_ROUTING_POLICY` 는 수신자 찾기만 다룬다. 오히려 「관계 자체를 묻지 않은 한 **`graph_search` 를 먼저 호출하지 않는다**」(:456-457)고 한다. 자기 업무 생성(`task_create_self`)에서 프로젝트·관련 업무를 찾으라는 지침은 어디에도 없다. 지침은 `codex_cli.py:500-504` 에서 조립되고 Claude 어댑터도 같은 것을 쓴다(`claude_cli.py:302-316`).
- 프로젝트 후보 도구 `project_list` 의 설명은 「**회의용** 프로젝트 후보 조회 — when preparing meeting follow-up work」(`tool_catalog.py:432-434`)다. 업무 생성에 쓰라는 신호로 읽히지 않는다.
- 실제 턴(ecab56f3): `material_search` 두 번 뒤 `task_create_self` 를 project_id 없이 불렀다(1-1 표).

## 3. 운영 영향

- **같은 일이 운영에서도 난다.** 그래프는 별도 인덱스가 없고 요청마다 원장에서 읽는다(`bootstrap/application.py:2562` `GraphApplication(_SessionGraphSource)`, `:687-699` 각 소유 모듈의 권한 조회). 그래서 「인덱스 미적재」 같은 운영 전용 조건은 없다.
- `kinds` 같은 지어낸 인자는 모델 행동이다. 운영 노드 codex 0.146 도 같은 MCP 서버(mcp 2.1.1)를 쓰므로 거절도 같다. 무해한 재시도로 끝나지만 실행 단계 UI 에 「× 실패」가 보인다.
- 프로젝트를 가리키려는 답변이 턴 전체를 실패시키는 것과 업무 생성 시 프로젝트 미탐색은 프롬프트·스키마·코드가 운영과 같으므로 그대로 재현된다(코드 경로 근거, 운영 로그는 보지 않음).

## 4. 고칠 자리 후보 (위치만)

**A. 프로젝트를 가리키면 턴 전체가 실패한다 (사용자 영향 가장 큼)**
- `modules/ax_execution/answer_documents.py:22` `ResourceRef` 허용 종류(`project` 없음)
- `answer_documents.py:86-96` `bind_answer_resources`: 묶지 못한 참조 하나가 턴 전체 실패
- `bootstrap/conversation_worker.py:222-229`: 그 실패를 `ProviderResponseInvalid` 로 턴 실패 처리
- `entrypoints/mcp.py:1039-1050`(graph_search·graph_neighbors)과 project 조회 도구: `_remember` 미호출, 즉 graph 로 본 대상이 답변 참조가 될 수 없다
- 답변 참조를 보여 주는 쪽(프론트 렌더러)이 `project:` 를 다룰 수 있는지는 FE 확인 필요
- `platform/codex_cli.py:460-475` `ANSWER_PRESENTATION_POLICY`: 허용 ref 목록(task/meeting/work_request/material/report) 문구

**B. 업무 생성 시 프로젝트·기존 업무 탐색**
- `platform/codex_cli.py:449-458` `WORK_AND_REPORT_ROUTING_POLICY` (특히 :456-457 「graph_search 를 먼저 호출하지 않는다」)
- `modules/ax_execution/tool_catalog.py:546`(task_create_self), `:648`(work_request_create) 설명의 「Fill every field the conversation gives you」
- `tool_catalog.py:432-434` `project_list` 설명(「회의용」으로 한정)
- 회의 배치 레지스트리 `bootstrap/settings.py` `DEFAULT_MEETING_AI_TOOLS` 에 `project_list` 가 있다. 대화 쪽 도구 노출 범위와는 별개이니 확인 대상이다.

**C. `kinds` 지어낸 인자 (무해한 잡음)**
- `platform/codex_cli.py:382` 「graph_search 시작 종류는 …」 문구
- `entrypoints/mcp.py:1905` `graph_search` 서명, `tool_catalog.py:395-398` 설명
- 실행 단계 UI 가 「모델이 스스로 고친 인자 오류」를 「× 실패」로 똑같이 보이는 표시: `tool_invocations.state=failed`, error_summary 「실패: failed」. 원문 `Unknown arguments: kinds` 는 요약에서 사라진다.

## 5. 한계

- 로컬 스택의 conversation worker stdout(`local-stack.log`)에는 도구 오류가 남지 않는다. 원인은 로컬 Codex rollout 파일로 확인했다. 운영에는 이 파일을 볼 수 있는 경로가 다르고(파드 런타임 홈), 운영 로그는 이번에 보지 않았다.
- 같은 대화의 두 번째 턴(1bb8e2a7)이 첫 턴의 세션(01a0f68f)을 잇지 않고 새 세션(01a0f6ac)에서 돈 이유는 보지 않았다. 범위 밖이지만 맥락 손실의 한 요인일 수 있다.
- 프론트가 `project:` 참조를 렌더링할 수 있는지는 확인하지 않았다(FE 범위).
- `kinds` 를 지어낸 원인을 `codex_cli.py:382` 문구로 본 것은 추정이다.
