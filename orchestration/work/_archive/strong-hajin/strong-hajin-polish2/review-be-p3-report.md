# 리뷰 리포트 — strong-hajin-polish2 / backend · WORK-009 Phase 3 (E2E-6) (2026-10-02)

## 판정: WARN

S-9 8(fix1)의 아홉 칸이 도구 설명 둘과 라우팅 정책에 **모두** 실렸다. 다룬 범위는 탐색 · 상세 최대 3 · 근거 · 출처 · 못 찾음 · 연결 현행 · 사람은 대화가 이름을 댄 사람만 · 날짜 안 옮김 · 제동 예외다. 제동 예외는 다섯 곳에 꼬리로만 붙었고 원문은 한 글자도 지워지지 않았다. 상세 조회는 이미 있는 경로로 답변 참조에 묶이고, 그 경로를 실제로 타는 계약 테스트가 생겼다. FAIL 은 없다. 경미 4건이 남는다.
- 가장 중요한 것: 「날짜는 대화가 준 것만」과 Phase 1 의 「IDs **and dates** come only from the conversation **or lookup**」 문장이 영어·한국어 양쪽에 같이 남아 날짜 기준이 두 개로 읽힌다.
- 그다음: 실물 90초 안에서 **검색 호출 수 상한이 없다**.

## 검수 범위

- 대상: `backend/` + `docs/unified-operations-inventory.json` 미커밋 변경. 수정 5파일 — `tool_catalog.py` · `codex_cli.py` · `test_ax_work_lookup_policy.py` · `test_answer_resources.py` · inventory. +140 / −18. Phase 1 은 `6efdac1` 로 커밋돼 대상 밖
- 기준: WP Phase 3 · SPEC-001 S-9 7·8(fix1, `41361e1`)·§5·§6 · 조사 `be-survey2-report.md` §2-2·§4-1 · 워커 보고 `be-p3-worker-report.md`
- 실행한 검사
  - diff 전문
  - 조회 도구 9개의 카탈로그 설명을 실제로 출력: `graph_search`·`graph_neighbors`·`my_meeting_list`·`meeting_list`·`meeting_get`·`task_get`·`material_search`·`task_list`·`my_task_list`
  - inventory hunk 확인 → 3곳
  - **`make test-unit` → 407 passed** · **`make test-contract` → 병렬 1162 · 직렬 128, 실패 0**

## 위반 (FAIL 사유)

- 없음

## 경미 (WARN)

- **W1 날짜 기준이 두 문장으로 읽힌다 — `backend/src/ax_workspace/modules/ax_execution/tool_catalog.py:546`·`:648` · `backend/src/ax_workspace/platform/codex_cli.py:477-478` 대 `:479-481`**
  - Phase 1 이 넣은 문장이 그대로 남았다. 영어 도구 설명은 「**IDs and dates** come only from the conversation **or lookup**: ISO start_date and due_date, …」, 라우팅 정책은 「ID(프로젝트·업무·사람)와 **날짜**(`start_date`·`due_date`)는 **대화·조회가 준 것만**」이다
  - 이번에 더한 문장은 「날짜는 **대화가 준 것만**이다」 · 「never turn a follow-up due candidate or a date in a record into start_date or due_date」다
  - 사람 쪽은 「(사람은 다음 줄의 단서를 따른다)」로 앞 문장을 좁혔다. 날짜 쪽은 앞 문장이 「조회」를 날짜의 출처로 계속 허용하고 뒤 문장이 금지한다. 영어 설명에는 그 연결 단서조차 없다
  - 이번 판이 탐색으로 회의(할 일의 마감 후보 포함)·업무(마감일 포함)를 **새로 읽게** 만들었다. 그래서 바로 이 틈으로 날짜가 들어올 위험이 Phase 1 때보다 커졌다
  - 근거: SPEC-001 S-9 7 날짜 줄(「지금처럼 대화가 준 것만」) · S-9 8 「채우지 않는 것」 · 리뷰 브리프 ③ 「도구 설명·정책이 서로·SPEC 과 모순 없나」
  - 권장: 앞 문장을 「IDs come only from the conversation or lookup …; dates (start_date, due_date) only from the conversation」 / 「ID 는 대화·조회가 준 것만, 날짜는 대화가 준 것만」으로 가른다. 단언 테스트도 그 문장으로 바꾼다
- **W2 검색 호출 수 상한이 없다 — 실물 90초 위험(`codex_cli.py:462-466`·`:395-398`)**
  - 상한은 「상세 최대 3건」뿐이다. 업무 생성 턴의 예상 호출은 다음과 같다
    - 탐색: `graph_search` + `my_meeting_list` + `material_search`
    - 상세: 최대 3
    - 연결: `list_projects` + `graph_neighbors`/`task_list`
    - 요청이면 후보 조회
    - 생성 도구 1
  - 합치면 **8~10회**다. 앞 판 실물은 3회였다
  - 자료 본문 지침의 「최초 호출을 포함해 **최대 세 번까지** 찾고」(`:396-398`)는 예외 꼬리(`:395`) **뒤** 같은 줄에 남아 있다. 업무 생성 턴에서 그 상한이 살아 있는지 꺼졌는지 문장만으로 갈리지 않는다. 회의 꼬리(`:385`)도 같은 모양이라, 뒤따르는 「회의 ID 를 찾기 위한 graph 조회를 먼저 하지 않는다」의 적용이 모호하다
  - `my_meeting_list` 는 기간 인자 없이 내 회의 전부를 돌려줄 수 있다(설명 105자, 범위 언급 없음)
  - 근거: E2E-6 ⑦(「타임아웃·추론 그대로 — 실물에서 시간 초과가 보이면 다시 본다」) · 리뷰 브리프 ⑥
  - 권장: 코디 실물 1회에서 **도구 호출 수와 턴 시간**을 기록한다. 넘치면 「탐색 검색은 종류마다 1회(`material_search` 는 재검색 없이 1회)」 같은 호출 상한 한 줄을 라우팅에 더하는 것이 첫 손잡이다
- **W3 예외 꼬리의 범위가 줄 중간에서 모호하다 — `codex_cli.py:410`**
  - 다섯째 꼬리는 `my_task_list`/`task_list` 줄의 **끝**, 「그렇게 넓혀 받은 목록으로 `내 업무`를 답하지 않는다 — 읽을 수 있다는 것이 그 사람의 일이라는 뜻은 아니다」 **뒤**에 붙었다. 의도는 「`task_list` 는 명시적으로 물을 때만」의 예외다
  - 문장 위치로는 「넓혀 받은 목록으로 내 업무를 답하지 않는다」까지 예외처럼 읽힌다. 업무 생성 턴에서 그 금지가 풀릴 이유는 없다
  - 위 W2 의 `:385`·`:395` 도 같은 꼴(꼬리 뒤에 원 문장이 이어진다)이다
  - 근거: 리뷰 브리프 ② 「다른 질문 턴 문장 의미가 그대로인가」 · S-9 8 「제동 문장」 칸
  - 권장: 꼬리를 「`task_list` 를 사용하고」 바로 뒤로 옮긴다. 또는 꼬리 문구를 「(업무 초안 턴은 **`task_list` 를 관련 업무 탐색에 써도 된다**)」처럼 무엇이 풀리는지 이름을 대는 꼴로 바꾼다. `:385`·`:395` 도 「material_search 로 시작하지 않아도 된다」처럼 대상을 좁힌다
- **W4 빈 단언 — `backend/tests/unit/test_ax_work_lookup_policy.py` `test_the_brakes_keep_their_words_and_except_only_the_drafting_turn`**
  - `brakes` 튜플(원문 다섯)을 만들고 `assert len(brakes) == 5` 만 한다. 튜플 원문이 정책에 있는지는 보지 않는다. 첫 원소에는 `"` 가 섞인 깨진 문자열(`관계를 묻지 않은 질문에" graph를…`)도 있다
  - 실제 검증은 바로 아래 for 문(꼬리 붙은 문장 다섯 · `count == 5` · 「거기서 멈춘다」 유지)이 한다. 그래서 테스트의 결론은 맞다. 다만 「원문이 남았다」는 docstring 의 주장 일부를 이 튜플이 지키는 것처럼 보인다
  - 근거: 리뷰 브리프 ⑤ 「빈 단언」
  - 권장: 튜플을 지우거나, 원소마다 `assert sentence in flattened` 로 바꾼다

## 확인한 것 (PASS 근거)

**① 문장 충실도 — S-9 8 ↔ 코드**

| S-9 8 칸 | 도구 설명(`tool_catalog.py:546`·`:648`) | 라우팅(`codex_cli.py`) |
|---|---|---|
| 찾는다 — 짧은 핵심어 · 회의·업무·자료 | 「short topic keyword (2–3 words … title substring match)」 · `graph_search`·`my_meeting_list`·`material_search` | `:462-464` 같은 셋 · 「제목 부분 일치」 |
| 읽는다 — 상세 최대 3 | 「at most 3 of the most relevant ones — meeting_get … task_get …」 | `:464-465` · 일괄 조회 금지 꼬리(`:381`)에도 「최대 3건」 |
| 근거로 쓴다 · 출처 | 「basis for description and checklist; name those meetings and Tasks as sources」 | `:467` 「resource_reference」 |
| 못 찾으면 | 「no related meeting or Task was found」 | `:468` 문장 그대로 |
| 연결 — 한 후보 확정일 때만 | 「Also look up …」 원문 유지 | `:469-474` 원문 유지 |
| 사람 — 대화가 이름을 댄 사람만 | 「only when the conversation named that person — lookup only resolves that name to an ID; never copy meeting attendees, follow-up owners or Task holders」 | `:479-480` 같은 뜻 |
| 날짜 — 옮기지 않음 | 「never turn a follow-up due candidate or a date in a record into start_date or due_date」 | `:480-481` |
| 제동 예외 | `task_list` 설명 꼬리 1 | 꼬리 5 + `:465-466` 이 넷을 이름으로 든다(graph 안 걷기 · 상세 일괄 · 회의·자료 질문 · task_list) |
| 바꾸지 않는 것 · 초안 근거 | 서버 로직·엔진·타임아웃·추론·Evidence 무변(diff 가 문장과 테스트뿐) | — |

- 카탈로그의 다른 조회 도구 설명(`graph_search`·`my_meeting_list`·`meeting_get`·`task_get`·`material_search`)에는 「~일 때만 써라」 류 제동이 없다(실제 출력 확인). 영어 쪽 예외는 `task_list` 하나로 충분하다. `my_task_list` 에는 예외가 번지지 않았다(단언 있음)
- `meeting_get` 설명이 「follow-up candidates」(할 일 후보 — 담당·마감 후보 포함)를 돌려준다고 말한다. 그래서 「follow-up owners · follow-up due candidate 를 옮기지 않는다」가 정확히 그 위험을 겨눈다

**② 제동 예외의 범위** — 원문 다섯이 그대로 남고 꼬리만 붙었다. 예외 문구 개수는 정확히 5이고, 「목록 하나로 답할 수 있는 질문은 … 거기서 멈춘다」 원문은 유지됐다(단언). 다른 질문 턴에서는 꼬리가 「업무·업무 요청 초안을 준비하는 턴은 예외」라는 조건문이라 의미가 그대로다. 모호한 자리는 W3.

**③ 정책 상호·SPEC 정합** — 「업무 생성 줄」(관계 지침 `:402-403`)과 라우팅 탐색 줄이 같은 말(「관련 회의·기존 업무·자료와 연결할 프로젝트를 먼저 찾아 읽은 뒤」)을 한다. Claude 어댑터는 같은 객체다(앞 판 단언 유지 · 정책 절 6 동일). 날짜 기준 하나만 둘로 갈린다(W1).

**④ 근거 묶기** — 새로 부르게 한 도구가 모두 이미 `_remember` 경로에 있다(조사 §4-1 표: `graph_search`·`my_meeting_list`·`meeting_get`(meeting) · `task_get`(task + 하위) · `material_search`(material)). 새 계약 테스트 `test_details_read_before_drafting_work_can_be_cited_as_sources`(`test_answer_resources.py`)가 **실제 경로**를 탄다.
- 위임 턴 causation id(`AX_MCP_CAUSATION_ID`)를 걸고 `McpReportsFacade.get_task`·`get_meeting` 을 부른다
- 답변 요소 `resource_list` 로 두 ref 를 인용한다
- 턴이 `completed` 이고 `answer_resources` 에 `(meeting, 회의 제목)`·`(task, 업무 제목)` 이 선다

이 테스트는 문장 존재가 아니라 묶임 결과를 본다.

**⑤ 테스트 · inventory**
- 정책 단언 4종(탐색·최대 3 / 사람·날짜 / 라우팅·출처·못 찾음 / 제동 범위)은 문장 단언이다. 문장이 곧 계약인 Phase 라 적절하다. 예외 범위는 **개수**(5)와 **번지지 않음**(`my_task_list`)까지 본다. 빈 단언은 W4 하나다
- inventory hunk 는 정확히 3곳(`task_list`·`task_create_self`·`work_request_create` description) — 그 항목만이다

**⑥ 실물 위험** — W2.
- 「상세 최대 3」은 문장 상한이라 모델이 넘을 여지가 있다. 서버 강제 없음(E2E-6 ⑦ 「바꾸지 않는다」로 계약상 맞다)
- 회의록 본문은 `meeting_get` 이 「note lines」로 돌려준다. 회의가 길면 토큰·시간이 늘 수 있다

## 코디 확인 목록 (실물 1회)

1. 데모 DB 의 회의가 있는 주제로 「…업무 만들어 줘」 → 도구 호출 기록에 `meeting_get` 또는 `task_get` 이 있고(3건 이하), **전체 호출 수와 턴 시간**(90초 안)을 적는다
2. 초안 체크리스트에 그 회의 할 일·업무 체크리스트에서 온 항목이 있고, 답변에 회의·업무 이름이 출처로 선다(답변 참조 칩)
3. 같은 초안에 **참조자·결재자·마감일이 비어 있다** — 회의 참석자·할 일 마감 후보가 들어오지 않았다(W1 의 틈을 실물로 확인)
4. 관련 기록이 없는 주제 → 「관련 회의·업무를 찾지 못해 일반 단계로 제안했습니다」
5. 업무 생성이 아닌 질문(예: 「내 업무 뭐 있어?」) — 지금처럼 `my_task_list` 하나로 끝나고 graph·회의·자료를 걷지 않는다
