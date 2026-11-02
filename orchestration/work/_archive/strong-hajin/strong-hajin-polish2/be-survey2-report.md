# 고도화 2차 E2E-6 서버 조사

- 대상: `strong-hajin-polish2` 워크트리, `6efdac1`(Phase 1 커밋) 위. 읽기 전용 — 코드 수정·테스트 실행·서버/DB/codex 기동 없음.
- 경로 약어: `B/` = `backend/src/ax_workspace/`, `T/` = `backend/tests/`, `S/` = `backend/scripts/`.
- 줄 번호는 `6efdac1` 기준.

## 0. 한 줄 요약

업무 초안 전에 AX 에게 「무엇을 찾아보라」고 하는 문장은 **프로젝트와 기존 업무 둘뿐**이다. 도구 설명(`B/modules/ax_execution/tool_catalog.py:546`·`:648`)과 라우팅 정책(`B/platform/codex_cli.py:461-466`) 모두 `list_projects`·`graph_search`·`graph_neighbors`·`task_list` 넷만 이름을 들고, 회의(`meeting_get`·`my_meeting_list`)·자료(`material_search`)·업무 상세(`task_get`)는 업무 생성 맥락에서 **한 번도 이름이 나오지 않는다**. 여기에 「관계를 묻지 않은 질문에 graph 를 걷지 않는다 — 이미 답이 손에 있는데 더 걷는 것은 답을 늦출 뿐」(`codex_cli.py:372-374`) · 「`task_list` 는 명시적으로 물을 때만」(`tool_catalog.py:568`, `codex_cli.py:408`) 같은 제동 문장이 남아 있고, `graph_search` 는 **제목 부분 일치**뿐이라(`B/modules/work/search.py:25-27`) 긴 업무명 그대로는 잘 안 걸린다. 실행 설정은 `reasoning_effort="low"`·타임아웃 90초(`codex_cli.py:91-95`)다. 회의 본문·할 일·업무 체크리스트를 **돌려주는 도구는 이미 있다**(`meeting_get`·`meeting_transcript`·`task_get`·`material_search`). 근거 묶기는 답변 참조(`task/meeting/work_request/project/material/report`)까지만 되고, **초안 Submission 의 근거(Evidence)로 붙는 것은 같은 턴의 `material_search` 자료 조각뿐**이다.

---

## 1. AX 가 쓸 수 있는 조회 도구

### 1-0. 노출 규칙

- 카탈로그는 129개(`B/modules/ax_execution/tool_catalog.py`, `ToolDefinition(` 129건). 도구 메타(이름·설명)는 카탈로그가 정본이고 MCP 등록이 그대로 싣는다(`B/entrypoints/mcp_server.py:35-50` — 등록 시 title/description 을 따로 받으면 거부).
- 위임 턴(대화)의 노출 판정 `ToolDefinition.visible`(`tool_catalog.py:30-44`): 확인이 필요한 도구는 `action.decide` 가 있어야 보이고, `all_capabilities`·`any_capabilities` 로 거른다. 전 역량 기준 129개 모두 보이고 그중 **조회(확인 불필요) 65개**(카탈로그를 파이썬으로 세어 얻은 값).
- 대화 턴은 도구 목록을 **좁히지 않는다** — 대화 워커가 `create_conversation_provider(settings)` 를 `enabled_tools` 없이 만든다(`B/bootstrap/conversation_worker.py:61`). `enabled_tools` 로 좁히는 것은 회의 배치뿐이다(`B/bootstrap/application.py:2055-2063`, codex 반영 `B/platform/codex_cli.py:343-346`).

### 1-1. 업무 초안에 닿는 조회 도구 — 무엇을 돌려주나

| 도구 (등록 `B/entrypoints/mcp.py`) | 설명 요지 (`tool_catalog.py`) | 입력 | 돌려주는 것 | 본문을 주나 |
|---|---|---|---|---|
| `graph_search` (:1939) | :394 「이름으로 시작 node 를 찾는다. 인자는 `query`·`limit` 뿐, 종류 필터 없음. person/team/project/task/work_request/meeting」 | `query`, `limit`(기본 20, 최대 50 — `B/modules/work/graph.py:34-35`) | node 목록 `kind·id·title·state·date·project_id`(`B/modules/work/graph_results.py:12-20`) | **아니오 — 이름·ID·상태·날짜만** |
| `graph_neighbors` (:1942) | :378 「한 hop. `<kind>:<id>`. 최대 50 edge」 | `node`, `limit` | edge + node(같은 모양) | 아니오 |
| `graph_overview` (:1936) | :386 「나/내 관계의 시작」 | `view`, `limit`(120) | 그래프 | 아니오 |
| `material_search` (:1948) | :402 「task·work_request·meeting·report·개인/팀 자료함의 자료 **본문** 검색. 회의 hit 는 MeetingNote 판·전사 revision 포함」 | `query`, `resource_types`, `resource_type`+`resource_id`, `material_id`, `limit`(기본 5, 상한 8 — `B/modules/work/material_extraction.py:24`), 등록일 범위 | 발췌(excerpt)·source_contexts·source_locator·integrity | **예 — 발췌문** |
| `my_meeting_list` (:1698) | :445 「내가 만들거나 참석한 회의」 | 없음 | 행 `meeting_id·title·starts_at·ends_at·location·status·viewer_relation·attendee_count`(`B/modules/meetings/application.py:1742-1766`) | 아니오 — 제목·시각만 |
| `meeting_list` (:1694) | :430 「조직 캘린더 투영. 상세 권한 밖은 busy 블록」 | 없음 | 같은 행 | 아니오 |
| `meeting_get` (:1702) | :429 「회의 하나 — 정보·안건·회의록 줄·후속 후보」 | `meeting_id` | `meeting{title·purpose·…}` + `agendas[]`(안건마다 회의록 줄·할 일 후보)(`application.py:1768-1815`, `:1956-`) | **예 — 회의록 줄·할 일** |
| `meeting_transcript` (:1710) | :413 「확정 전사 블록·회의 중 메모」 | `meeting_id` | 전사 블록 | **예 — 원문** |
| `meeting_export` (:1722) | :416 「최신 회의 정보·안건 줄·후속 후보를 HTML 한 장으로」 | `meeting_id` | HTML | 예 |
| `task_list` (:1971) | :568 「조직·프로젝트로 읽을 수 있는 업무. **요청이 팀/프로젝트 업무를 명시적으로 물을 때만**」 | `include_closed` | 업무 행 = `_view` + `checklist_progress{done,total}`(`B/modules/work/application.py:1095-1113`). `description` 포함, **체크리스트 항목은 없음** | 내용(description)은 예, 체크리스트 항목은 아니오 |
| `my_task_list` (:1968) | :447 「내가 담당하는 업무만」 | `include_closed` | 같은 모양 | 같음 |
| `task_get` (:1974) | :552 「업무 하나」 | `task_id` | 담당자면 `checklist[]` 항목 포함(`application.py:1115-1125`, `:2686-2692`). **담당자가 아니면 읽기 전용 갈래 — 체크리스트 없음**(같은 docstring `:1118-1121`) | 예(담당자만 체크리스트) |
| `task_checklist_list` (:1983) | :508 「업무 안 단계」 | `task_id` | `task_get` 의 `checklist` 를 그대로 옮김(`mcp.py:1087-1089`) → 담당자 아니면 빈 목록 | 담당자만 |
| `task_materials_list` (:1986) | :576 「업무의 입력·산출 자료와 추출 상태」 | `task_id` | 자료 메타 | 아니오(본문은 `material_search`) |
| `task_history` (:1977) | :560 「버전 스냅샷과 활동」 | `task_id` | 스냅샷(체크리스트 포함) | 예 |
| `list_projects` (:1531) · `project_list` (:1726) | :238 · :431 「업무·요청 초안의 project_id 를 찾는 데 쓴다」 | 없음 | 프로젝트 행 | 아니오 |
| `get_project` (:1535) | :245 「프로젝트와 참여자」 | `project_id` | 프로젝트 상세 | 이름·참여자 |
| `conversation_search` (:1561) | :335 「이전 사용자 발화 검색」 | `query`, `limit`(최대 20 — `mcp.py:1012`) | 발췌 | 예 |

**검색 방식**: `graph_search` 의 업무·회의·프로젝트·팀은 **제목 부분 일치**다 — `matches(query, title)` = 정규화한 질의가 제목 안에 그대로 있는가(`B/modules/work/search.py:25-27`; 업무 `B/bootstrap/application.py:701`, 회의 `:849`, 프로젝트·팀 `B/modules/work/graph.py:113-114`). 본문·체크리스트·회의록은 graph 로 찾을 수 없고, 본문 검색은 `material_search`(자료로 올라간 것 — 업무 description·체크리스트는 자료가 아니다)뿐이다.

---

## 2. 업무 생성 턴에서 도구를 고르게 하는 문장 전부

턴 프롬프트는 정책 6절 + 접수 시각 + 최근 대화 + 시드 참조 + 사용자 메시지다(`B/platform/codex_cli.py:500-551`). Claude 어댑터도 같은 정책 객체를 쓴다(`T/unit/test_ax_work_lookup_policy.py` 의 동일 객체 단언).

### 2-1. 업무 생성에 직접 닿는 문장

| 위치 | 원문 |
|---|---|
| `tool_catalog.py:546` `task_create_self` | "Before drafting, look up what a person would pick in that form: the project this work belongs to (list_projects, or graph_search by name) and related existing Tasks (graph_neighbors on `project:<id>`, or task_list) for parent, preceding and reference. Fill a link only when one candidate clearly matches; if none or several match, leave it empty and say so in the answer — never invent an ID." |
| 같은 줄 (Phase 1) | "Propose the content yourself: write description … and checklist … from the topic of the conversation, even when the user named no steps." |
| `tool_catalog.py:648` `work_request_create` | 같은 탐색 문장(프로젝트·업무만) + 같은 제안 문장 |
| `codex_cli.py:402-404` 관계 지침 | "사용자가 본인 업무 생성이나 승인할 수 있는 생성안을 요청하면 필요한 자료 근거와 연결할 프로젝트·기존 업무를 먼저 조회한 뒤(업무 생성·보고 상태 선택 지침의 탐색 규칙) `task_create_self`로 Action 제안을 준비한다." |
| `codex_cli.py:461-466` 라우팅 | "업무(`task_create_self`)·업무 요청(`work_request_create`) 초안을 만들기 전에 **연결할 프로젝트와 관련 기존 업무를 찾는다** — … 프로젝트는 `list_projects`(참여 프로젝트) 또는 이름으로 `graph_search`, 그 프로젝트의 업무는 `graph_neighbors(node='project:<id>')` 또는 `task_list`로 찾는다. 대화에 나온 이름이나 업무 주제와 **한 후보로 확정될 때만** … 채운다." |
| `codex_cli.py:467-468` (Phase 1) | "업무·업무 요청 초안의 **체크리스트(첫 단계들을 순서대로)와 업무 내용(`description`)은 대화의 업무 주제로부터 제안해 채운다**" |
| `codex_cli.py:469-470` (Phase 1) | "**ID(프로젝트·업무·사람)와 날짜(`start_date`·`due_date`)는 대화·조회가 준 것만** 채운다." |

- 「자료 근거」를 먼저 조회하라는 말은 관계 지침 한 줄(`:402`)에만 있고, 그 줄이 가리키는 「탐색 규칙」(`:461-466`)에는 자료·회의가 없다.
- 체크리스트·내용을 **무엇으로부터** 제안하나는 「대화의 업무 주제」(`:467`)다 — 조회한 회의·업무·자료를 근거로 쓰라는 문장은 없다.

### 2-2. 제동·한정 문장(업무 생성 턴에도 함께 실림)

| 위치 | 원문 | 업무 생성에 미치는 것 |
|---|---|---|
| `codex_cli.py:368-371` | "관계 의도는 목록 의도보다 우선한다. 질문이 … 관계나 연결을 묻거나, 관계를 따라 대상을 찾으라고 하면 … 관계 도구로 시작한다." | 「업무 만들어 줘」는 관계 의도가 아니므로 이 문장이 graph 를 켜지 않는다 |
| `codex_cli.py:372-374` | "관계 의도가 없을 때만 목록 하나로 답할 수 있는 질문은 소유 도구를 바로 부르고 거기서 멈춘다. … 관계를 묻지 않은 질문에 graph를 걷지 않는다 — 이미 답이 손에 있는데 더 걷는 것은 답을 늦출 뿐이다." | graph 탐색을 아끼라는 일반 문장 |
| `codex_cli.py:381` | "주변 node의 상세를 일괄 조회하지 않는다." | 관련 업무·회의 상세를 여러 개 읽는 것을 막는 쪽 |
| `codex_cli.py:385` | "회의에서 결정한 날짜·담당자·재논의 이유 등 **회의 내용을 묻는 질문**은 `material_search`로 시작한다." | 회의 탐색이 「질문」일 때만 켜짐 |
| `codex_cli.py:395-398` | "자료 본문 질문은 `material_search`로 시작한다. … 최초 호출을 포함해 최대 세 번까지 찾고" | 자료 탐색이 「자료 본문 질문」일 때만 켜짐 |
| `codex_cli.py:408-410` | "`my_task_list`는 본인이 담당하는 업무만 반환한다. 열람 가능한 팀/프로젝트 업무를 명시적으로 묻는 질문에는 `task_list`를 사용하고" | `task_list` 를 「명시적으로 물을 때」로 한정 — 업무 생성 규칙(`:463`)과 결이 다름 |
| `tool_catalog.py:568` `task_list` | "Use only when the request explicitly asks for readable team/project work." | 같음 |
| `codex_cli.py:458-460` | "**사람을 찾으려고** `graph_search`를 먼저 호출하지 않는다" | Phase 5 가 「사람 찾기」로 좁혔다 |
| `tool_catalog.py:394` `graph_search` | "Material and report are evidence nodes reached through relationships, not title search." | 자료는 이름 검색 대상이 아님 |

### 2-3. Phase 5(`33e8f1b`)가 바꾼 것 / 아직 막는 것

`git show 33e8f1b -- B/platform/codex_cli.py B/modules/ax_execution/tool_catalog.py` 기준.

| 바꾼 것 | 전 → 후 |
|---|---|
| `project_list` | 제목 「회의용 프로젝트 후보 조회」·"use when preparing meeting follow-up work" → 「프로젝트 후보 조회」·업무/요청 초안의 project_id 용 |
| `list_projects` | 설명에 "Use it to find the project_id for a Task or WorkRequest draft" 추가 |
| `graph_search` | 인자가 `query`·`limit` 뿐이고 종류 필터가 없다는 설명 추가 |
| 두 생성 도구 | "Fill every field the conversation gives you" → "Before drafting, look up … project … related existing Tasks" |
| 관계 지침 `:402` | "필요한 자료 근거를 먼저 조회한 뒤" → "필요한 자료 근거와 **연결할 프로젝트·기존 업무를** 먼저 조회한 뒤" |
| 라우팅 `:458` | "관계 자체를 묻지 않은 한 `graph_search`를 먼저 호출하지 않는다" → "**사람을 찾으려고** … 먼저 호출하지 않는다" |
| 라우팅 `:461-466` | 프로젝트·업무 탐색 규칙 신설 |
| 답변 지침 | 참조 종류에 `project:` 추가 |

**아직 그대로인 것**: 2-2 표 전부 — `:372-374`(graph 를 걷지 않는다), `:381`(일괄 상세 조회 안 함), `:385`·`:395`(회의·자료는 「질문」일 때), `:408` 과 `tool_catalog.py:568`(`task_list` 는 명시적일 때만). 탐색 대상에 회의·자료·업무 상세는 Phase 5 에서도 들어가지 않았다.

---

## 3. 실물 대화가 `task_list`·`list_projects` 만 부른 이유로 코드에서 보이는 것

코드만으로 확정할 수 없다(모델 판단). 코드에 보이는 정황:

1. **이름이 나온 도구가 그 둘이다.** 생성 도구 설명과 탐색 규칙이 고르라고 이름을 든 것은 `list_projects`·`graph_search`·`graph_neighbors`·`task_list` 넷이고(`tool_catalog.py:546`, `codex_cli.py:462-463`), 「또는(or)」으로 묶여 있다 — `list_projects` **또는** `graph_search`, `graph_neighbors` **또는** `task_list`. 앞쪽(프로젝트) 하나와 뒤쪽(업무) 하나면 지시를 다 지킨 셈이다.
2. **회의·자료·업무 상세를 업무 생성에서 부르라는 문장이 없다.** 회의·자료 탐색 문장은 「회의 내용을 묻는 질문」「자료 본문 질문」 조건부다(`codex_cli.py:385`, `:395`).
3. **제동 문장**: 「관계를 묻지 않은 질문에 graph 를 걷지 않는다 — … 답을 늦출 뿐」(`codex_cli.py:372-374`), 「주변 node 의 상세를 일괄 조회하지 않는다」(`:381`).
4. **graph_search 는 제목 부분 일치**(`search.py:25-27`). 「명동점 데이터 분석하기」처럼 업무명 전체를 질의로 쓰면 제목에 그 문자열이 그대로 있어야 걸린다 — 결과가 비면 `task_list`(전체 목록) 쪽이 남는다. (실물 질의 인자는 보지 못했다 — §9)
5. **체크리스트·내용의 근거 지시**: 「대화의 업무 주제로부터 제안」(`codex_cli.py:467`, `tool_catalog.py:546`) — 조회 결과에서 끌어오라는 말이 없으므로, 제목만으로 일반론을 써도 지시에 맞는다.
6. **실행 설정**: 모델 `gpt-5.6-terra`, `service_tier="fast"`, **`model_reasoning_effort="low"`**, 대화 턴 타임아웃 **90초**(`B/platform/codex_cli.py:91-95`, 대화 인자 `:300-306`, 타임아웃 적용 `:216-223`). Claude 어댑터는 180초(`B/platform/claude_cli.py:74`). 서버 쪽에 **도구 호출 횟수 상한·턴 예산은 없다**(grep `max_tool`·`tool_budget` 0건). 노출 도구 수는 좁히지 않는다(§1-0).
7. **평가 스크립트의 기준**: 라이브 라우팅 평가 `S/search_routing_live_profile.py:24-30` 의 업무 생성 케이스는 하나(`precreation`)이고, 사용자가 「견적서에서 먼저 확인하고」라고 **자료를 명시**한 질문에만 `material_search` 를 요구한다(`:30`, `max_calls 4`). 「목록」 케이스는 `max_calls 1`(`:24`) — 적게 부르는 것을 통과 조건으로 둔다.

---

## 4. 근거 묶기

### 4-1. 답변 근거(answer resources)

- 위임 턴의 조회가 돌려준 대상은 `_remember` → `record_answer_resources` → `SqlAlchemyGraphReceiptRepository.record_resources` 로 그 턴의 근거로 남는다(`B/entrypoints/mcp.py:489-494`, `B/bootstrap/application.py:2720-2738`). 대화를 읽을 때 소유 모듈이 다시 권한을 확인한다(같은 docstring).
- 답변이 가리킬 수 있는 종류: `task|meeting|work_request|project|material|report`(`B/modules/ax_execution/answer_documents.py:22`).
- 도구별로 근거로 남는 것:

| 도구 | 남기는 근거 | 근거 |
|---|---|---|
| `my_task_list`·`task_list` | 업무 전부(`task:<id>@version`) | `mcp.py:496-509` |
| `task_get` | 그 업무 + 읽을 수 있는 하위 | `mcp.py:511-518` |
| `my_meeting_list`·`meeting_list` | 회의 행 전부(`kind=meeting` 만) | `mcp.py:796-813` |
| `meeting_get` | 그 회의 | `mcp.py:815-820` |
| `graph_search`·`graph_neighbors` | node 중 `task/work_request/meeting/project` (Phase 5) | `mcp.py:1055-1075`, 종류 `:1068` |
| `graph_overview` | **남기지 않음**(120 node 를 스치므로) | `mcp.py:1045-1053` 주석 |
| `list_projects`·`get_project` | 프로젝트 (Phase 5) | `mcp.py:1301-1314` |
| `task_materials_list` | 자료(`material`, integrity·source_contexts) | `mcp.py:1137-1146` |
| `material_search` | hit 자료(`material`, source_locator 포함) | `mcp.py:1151-1162` |
| `conversation_search` | `conversation_turn` | `mcp.py:1035-1043` |
| `meeting_transcript`·`meeting_export`·`task_checklist_list`·`task_history` | **남기지 않음**(`_remember` 호출 없음) | `mcp.py:975-986`, `:1087-1089`, `:724-725` |

- **회의록 줄·회의 할 일·체크리스트 항목은 근거 종류가 아니다.** 회의는 회의 전체(`meeting:<id>`)로만, 회의록 텍스트는 `material_search` 가 찾은 MeetingNote 자료(`material:<id>` + `source_locator`)로만 가리킬 수 있다.

### 4-2. 초안(SubjectVersion·Submission) 근거

- AX 제안이 저장될 때 1회차 Submission 에 `EvidenceRecord` 가 붙는 길은 **하나** — 제안한 턴이 `material_search` 로 남긴 `ConversationContentEvidenceRecord`(자료 조각)를 지금 권한으로 다시 읽은 것(`B/platform/actions.py:404-421`, 읽기 `:422-428` → `B/bootstrap/application.py:4424-4432`, 쓰기 `B/platform/material_extraction.py:518`). `evidence_role="supporting"`, `fixed_snapshot_ref="conversation_content_evidence:<id>@<integrity>"`.
- 회의·업무·프로젝트를 조회한 사실은 Submission Evidence 가 되지 않는다(`_readable_turn_materials` 가 자료 조각만 본다).
- 사람이 고친 회차(confirm+draft·save_draft)는 앞 회차의 Evidence 를 그대로 복사한다(`B/platform/action_center.py` `_open_revised_round` 의 Evidence 복사 루프).
- 판단 대기·채팅 카드는 미리보기에 근거 줄을 붙인다(`ActionPresenter._evidence` — `B/platform/actions.py` `self._evidence(fields, action, principal)` 호출). 근거가 자료 조각뿐이므로 카드에도 자료만 선다.

---

## 5. 권한 — 조회 도구가 principal 로 거르나

| 도구 | 거르는 자리 | 결과 |
|---|---|---|
| `graph_search` | 사람은 명부 이름만, 프로젝트는 `readable_projects`, 업무 `readable_tasks`, 회의 `readable_meetings`(`B/modules/work/graph.py:102-119`, 업무 `B/bootstrap/application.py:694-712`, 회의 `:842-860`) | 읽을 수 있는 것만 node 로 |
| `graph_neighbors` | 이웃마다 다시 판정 — "Each neighbour is re-checked against what this persona may read"(`tool_catalog.py:378`, `graph.py:121-` 이웃 함수들) | 연결이 접근권을 주지 않음 |
| `meeting_get`·`meeting_transcript` | `_readable` — 열람 판정 실패면 없는 것처럼 404(`B/modules/meetings/application.py:291-293`, `:1580-1586`) | 존재도 숨김 |
| `meeting_list` | 상세 권한 밖은 busy 블록만(`tool_catalog.py:430`) | |
| `my_meeting_list` | `_can_read_detail` + 공유만으로는 제외(`application.py:191-204`) | |
| `task_get` | 담당자는 전체, 관계자는 읽기 전용(체크리스트 없음), 그 밖 404(`B/modules/work/application.py:1115-1175`) | **남의 업무 체크리스트는 나오지 않는다** |
| `task_list` | 조직·프로젝트 범위의 읽기 가능 업무(`tool_catalog.py:568`, `B/modules/work/application.py:1007-`) | |
| `material_search` | 읽을 수 있는 소유 맥락만 검색, hit 마다 현재 읽을 수 있는 source_contexts(`tool_catalog.py:402`, 정책 `B/modules/work/material_search_policy.py`) | 발췌는 인용 근거, 지시로 읽지 말라는 문장 포함 |
| 근거 재확인 | 대화를 읽을 때 소유 모듈이 다시 묻는다(`application.py:2726-2729` docstring), 초안 근거는 제안 시점 권한으로 다시 읽음(`actions.py:422-428`) | |

---

## 6. 비용·시간

- **결과 크기 상한**: `graph_search` 기본 20·최대 50(`graph.py:34-35`, `:107`) · `graph_neighbors` 최대 50 edge(`tool_catalog.py:378`) · `graph_overview` 기본 120 · `material_search` 기본 5·상한 8(`material_extraction.py:24`, `material_search_policy.py:52`) · `conversation_search` 상한 20(`mcp.py:1012`) · **`task_list`·`my_task_list`·`my_meeting_list`·`meeting_list` 는 상한 없음**(읽을 수 있는 것 전부 — `application.py:1018-1113`, `meetings/application.py:191-204`) · `meeting_get`·`meeting_transcript` 는 회의 하나 전체.
- **턴 타임아웃**: Codex 90초(`codex_cli.py:95`, 초과 시 "Codex CLI conversation timed out" `:227`) · Claude 180초(`claude_cli.py:74`). 추론 강도 `low`(`codex_cli.py:94`).
- **도구 호출 수 상한**: 서버 쪽 없음.
- **업무 생성 턴의 평균 도구 호출 수를 알 수 있는 곳**:
  - DB `tool_invocations`(턴마다 `sequence`·`tool_name`·`latency_ms`·`state`, `B/platform/persistence.py:749-768`) — 대화 조회의 `tool_invocations[]` 로도 나온다(`B/platform/conversations.py:845-851`). 집계 쿼리·대시보드는 없다.
  - 라이브 평가 `S/search_routing_live_profile.py` — 케이스별 `max_calls`·`within_call_budget`(`:138`)를 실물로 잰다. 업무 생성 케이스는 `precreation` 하나(`:30`).
  - 단위·계약 테스트로 평균을 재는 것은 없다.

---

## 7. 테스트

| 테스트 | 무엇을 보나 |
|---|---|
| `T/unit/test_ax_work_lookup_policy.py` | 정책 **문장** 단언 — 라우팅에 6개 도구 이름(`task_create_self`·`work_request_create`·`list_projects`·`graph_search`·`graph_neighbors`·`task_list`)과 4개 필드, 「연결할 프로젝트를 찾지 못했습니다」·「지어내지 않는다」(:10-17) · 사람 찾기 graph 금지 문장(:20-23) · 두 생성 도구의 "Before drafting, look up"·"never invent an ID"·`list_projects`·`graph_neighbors`(:26-31) · `project_list` 회의 한정 해제(:34-38) · graph_search 인자 문장(:41-46) · project 참조(:49-52) · Claude 동일 객체(:55-57) · Phase 1 제안/ID·날짜 문장(끝 두 테스트). **회의·자료 탐색 문장 단언은 없다** |
| `T/unit/test_search_routing_live_profile.py` | 라이브 평가 스크립트의 채점 규칙(필수 도구 없이 사실만 맞은 답은 실패 등) — 도구 **경로**를 보는 유일한 자리. 실물 모델은 부르지 않는다 |
| `S/search_routing_live_profile.py` | 실물 대화로 첫 도구·필수 도구·호출 수를 잰다(`:24-32`, 채점 `:120-200`). 업무 생성 케이스 `precreation` 은 자료를 명시한 질문 |
| `T/contract/test_answer_resources.py` | Phase 5 — graph·project 조회가 근거로 묶이고 project 참조 답변이 턴 실패가 되지 않음 |
| 계약 테스트 전반 | 도구를 직접 부르거나 제안을 직접 세운다 — **모델이 어떤 순서로 도구를 고르는지 보는 테스트는 없다** |

---

## 8. grep 개수표

| 심볼 / 패턴 | 범위 | 개수 |
|---|---|---|
| `ToolDefinition(` | `tool_catalog.py` | 129 |
| 위임 턴 노출(전 역량) / 그중 조회 | 카탈로그 계산 | 129 / 65 |
| 생성 도구 설명에 이름이 나온 조회 도구 | `tool_catalog.py:546`·`:648` | 4 (`list_projects`·`graph_search`·`graph_neighbors`·`task_list`) |
| 생성 도구 설명의 `meeting`·`material_search`·`task_get` | `:546`·`:648` | 0 |
| 업무 생성 라우팅에 이름이 나온 조회 도구 | `codex_cli.py:461-466` | 4 (같은 넷) |
| 「회의 내용을 묻는 질문」·「자료 본문 질문」 조건 문장 | `codex_cli.py` | 2 (`:385`, `:395`) |
| graph 제동 문장(「걷지 않는다」·「일괄 조회하지 않는다」) | `codex_cli.py` | 2 (`:374`, `:381`) |
| `task_list` 「명시적」 한정 | `tool_catalog.py:568` · `codex_cli.py:408` | 2 |
| `_remember` 정의 + 호출 | `mcp.py` | 정의 1 · 호출 21 (`self._remember` 등장 기준, `_remember_tasks`·`_remember_meetings`·`_remember_graph_nodes` 포함) |
| `_remember` 없는 본문 조회 도구 | `mcp.py` | 4 (`meeting_transcript`·`meeting_export`·`task_checklist`·`task_history`) |
| 답변 참조 종류 | `answer_documents.py:22` | 6 |
| 초안 Evidence 를 붙이는 자리 | `actions.py:404-421` | 1 (자료 조각만) |
| `matches(` 제목 검색 사용 | `graph.py` · `bootstrap/application.py` | 2 · 2 |
| 서버 쪽 도구 호출 상한(`max_tool`·`tool_budget`) | `B/` | 0 |
| 정책 문장 단언 테스트 파일 | `T/unit` | 1 (`test_ax_work_lookup_policy.py`) |
| 도구 순서를 보는 단위·계약 테스트 | `T/` | 0 (라이브 스크립트 채점 단위 테스트 1 파일 제외) |

---

## 9. 조사 한계

- **실물 대화를 보지 않았다.** 사용자 로컬 E2E 의 `tool_invocations`(인자 요약·순서)·codex 이벤트 로그를 열지 않았다(로컬 스택·DB 접근 금지). 그래서 `task_list`·`list_projects` 만 부른 이유는 §3 의 **정황**이고 확정이 아니다. `graph_search` 를 아예 부르지 않았는지, 불렀으나 빈 결과였는지 구분하지 못한다(사용자 보고는 「0」).
- 모델이 129개 도구 목록·정책 6절 중 무엇에 더 무게를 두는지, `reasoning_effort="low"` 가 탐색 횟수에 미치는 영향은 코드로 답할 수 없다.
- `meeting_get` 의 회의록 줄·할 일의 정확한 필드(줄 텍스트·할 일 후보 모양)는 `_agenda_view` 앞부분(`B/modules/meetings/application.py:1956-1970`)까지만 읽었다.
- 도구 결과의 바이트 크기(예: `task_list` 업무 수백 건)·토큰 비용은 재지 않았다.
- `material_search` 가 업무 description·체크리스트를 찾지 못한다는 판단은 검색 대상이 「자료(material) 소유 맥락」이라는 설명·정책(`tool_catalog.py:402`, `material_search_policy.py:13`)에서 끌어냈다 — 색인 코드 전체는 추적하지 않았다.
