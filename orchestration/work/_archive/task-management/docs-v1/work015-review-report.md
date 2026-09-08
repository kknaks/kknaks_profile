---
type: review
work: WORK-015
title: "WORK-015 검수 — 중간 배치는 AI 혼자(MF-71): 옵션 빌더 phase · 프롬프트 · 미러 갈래 삭제"
reviewer: reviewer
date: 2026-09-08
scope: "미커밋 변경 7 파일(백엔드만 — 소스 3 · 테스트 4)"
worktree: /Users/kknaks/orca/workspaces/task_management/docs-v1 (kknaksss/docs-v1 · HEAD aa375ed)
verdict: "FAIL 0 · WARN 2 · 문서 공백 2"
---

# WORK-015 검수 리포트

**FAIL 0 · WARN 2 · 문서 공백 2.**
`tauri.conf.json` 은 범위 밖이라 보지 않았다. 테스트는 돌리지 않았다(코디 실측 — 652).

## 0. 축별 판정 한 줄

| 축 | 판정 | 한 줄 |
|---|---|---|
| 2-1 옵션 빌더 `phase` | **PASS** | `CodexPhase` 리터럴 · `batch` 셋 / `final` 일곱 · **갈리는 것은 `enabled_tools` 배열과 approval 줄 수뿐** · 기본값 없음 · `get_gateway().run(` 세 호출부가 전부 phase 를 명시 · 옵션 빌더 단일 정적 검사 유지 |
| 2-2 프롬프트 | **PASS** | 배치 프롬프트 520자에 `list_agendas`·`get_agenda`·`get_meeting`·`get_account` **0건** · 「미러」·「늘어나면」 0 · 「발화만 보고 네가 가른다」 추가 · 「처음부터 다시」 유지 · **웜스타트 프롬프트 diff 0** |
| 2-3 파서 · 저장 | **PASS** | `humanAgendaId` 를 `fill_final` 로 갈라 회의 중엔 **읽고 버린다**(폐기 아님) · `fill_final=True` 경로 동작 불변 · 미러 전체(조회 · `source_agenda_id` · 제목 · `state`)가 플래그 안 · `_run_once` 의 사람 안건 조회 삭제는 **계약이 요구한 것** |
| 2-4 불변 | **PASS** | `ai_schemas/` · `app/mcp/` · `app/front/src` **diff 0** · 전량 교체 · 검증 0~5 자리 그대로 · `test_meeting_finalize.py` 무수정 |
| 2-5 테스트 | **PASS · WARN 1** | 단계별 옵션 4 + WORK-009 함정 둘을 두 phase 로 재실행 · BE §12 6 확장 · 7-b 신설 · 정적 2 · 대역이 `phase` 를 기록. 옵션 기대값의 「손으로 적는다」가 약해졌다 |

---

## 1. FAIL

**없다.** 브리프가 지목한 FAIL 조건 다섯을 전부 확인했다 — batch 옵션에 안건 도구 0 · 회의 중 `source_agenda_id` 채움 0 · `humanAgendaId` 로 폐기 0 · 최종 경로 동작 변경 0 · 스키마/MCP 변경 0.

---

## 2. PASS — 무엇을 확인했나

### 2-1. 옵션 빌더 `phase` (MF-71 · SPEC-007 §4 도구 표 「단계」 열 · §5)

| 검사 | 결과 |
|---|---|
| 타입 | `CodexPhase = Literal["batch", "final"]`(`agent.py:48`) |
| 중간 셋 | `_BATCH_TOOL_NAMES = ("list_tasks", "get_task", "list_work_types")`(`:83`) — **SPEC-007 §4 표의 「중간 · 최종」 세 행과 정확히 같다.** `get_meeting`·`get_account`·`list_agendas`·`get_agenda` 는 표에서 「**최종만**」이고 코드에서도 빠졌다 |
| 갈리는 것 | `_TOOLS_BY_PHASE[phase]`(`:85` · `:112`)가 `enabled_tools` 배열과 approval 생성식 **둘에만** 쓰인다. 내장 4줄 · url · headers · `sandbox` · `resume` 은 두 phase 가 **같은 코드**를 지난다 |
| batch 문자열 | `enabled_tools=["list_tasks","get_task","list_work_types"]` + approval **3줄** = **10줄**. 안건·회의·계정 도구 문자열 **0건**(테스트 `test_agent_options.py:71`) |
| final 회귀 | **14줄이 WORK-009 목록과 문자열·순서까지 같다** — `test_the_final_phase_is_the_work009_list_unchanged`(`:63`)가 기준선이고 `test_only_the_tool_lines_differ_between_the_two_phases`(`:86`)가 「그 두 자리 말고는 같다」를 따로 잠근다 |
| 기본값 없음 | `build_mcp_config(…, *, phase)`(`:101`) · `build_codex_options(…, phase)`(`:127`) · `AgentGateway.run`(`:60`) · `OpenKknaksGateway.run`(`:182`) 어디에도 기본값이 없다. `test_phase_has_no_default`(`:191`)가 인자 없이 부르면 실패함을 단언 |
| 호출부 셋 | `meeting_batch_service.py:325` `phase="batch"`(회의 중) · `meeting_finalize_service.py:348` `phase="final"`(②) · `meeting_batch_service.py:712` `phase="final"`(웜스타트). **`get_gateway().run(` 호출부가 셋뿐이고 전부 명시**한다 |
| resume 에도 실린다 | `config` 는 `session_id` 와 무관하게 실린다 — `test_the_batch_allow_list_rides_the_resume_too`(`:97`). MF-71 의 「`-c` 는 resume 에도 산다」가 코드로 성립 |
| WORK-009 함정 둘 | `tm.` 접두 0 · `approval_policy` 0 — **두 phase × 두 세션 종류**로 parametrize 해 재실행(`:149` · `:161`). approval 줄 수도 `("batch",3)`·`("final",7)` 로 본다(`:171`) |
| 옵션 빌더 단일 | `provider_options`·`"config"`·`mcp_servers` 문자열을 만드는 곳이 `agent.py` 밖에 **0건**(정적 `:211` 유지) |

### 2-2. 프롬프트 (MF-71 · SPEC-007 §4 「배치 입력」 3행)

`_BATCH_INSTRUCTIONS` 를 직접 파싱해 세었다 — **520자**.

| needle | 개수 |
|---|---|
| `list_agendas` · `get_agenda` · `get_meeting` · `get_account` | **0** |
| `list_tasks` · `get_task` · `list_work_types` | 각 **1**(「업무를 가리킬 때만 조회한다」 한 줄) |
| 「미러」 · 「늘어나면」 | **0** |
| 「처음부터 다시」 | 1(MF-53 전량 교체 지시 유지) |
| 「발화만 보고」 | 1 |
| `humanAgendaId` | 1 — 「회의 중에는 쓰지 않는다 — null 로 둔다」 |

- 삭제된 것 — 「정리하기 전에 이 순서로 조회해라」 3단계 블록 · 「안건은 사람 안건을 미러하면 그 id 를 humanAgendaId 에 넣는다(제목은 서버가 사람 안건 것으로 맞춘다)」 두 줄.
- 더해진 것 — 「**안건은 발화만 보고 네가 가른다.** 사람이 적은 것은 보지 않는다 — 너는 네 회의록을 쓰고, 사람 것과 합치는 일은 회의가 끝난 뒤에 한다. 그래서 안건 제목도 네가 짓는다.」
- **웜스타트 프롬프트 diff 0** — `_WARM_START_PROMPT` 가 2,323자로 WORK-010 값 그대로이고 diff 에 한 줄도 없다(WP 가 「WORK-010 소관」으로 뺀 자리).
- 정적 검사 `test_meeting_live_static.py:111` 이 금지 needle 과 「발화만 보고 네가 가른다」·「AI 트랙 전체를 다시 정리해라」 존재를 함께 잠근다.

### 2-3. 파서 · 저장

**`_parse_output`** — `human_agenda_id = agenda["humanAgendaId"] if fill_final else None`(`meeting_batch_service.py:477`). 회의 중이면 값이 무엇이든(사람 안건 id 든 없는 id 든) `None` 이 되고, 그 아래 소속 검사는 `human_agenda_id is not None` 이 거짓이라 **도달하지 않는다** — `_SchemaViolation` 이 나지 않는다. SPEC-007 §4 검증 2행 「무엇이 오든 무시하고 `null` 로 저장한다. **폐기 사유가 아니다**」와 문장 단위로 맞는다. `fill_final=True` 갈래는 한 줄도 안 바뀌었다(diff 가 그 조건식 한 줄과 docstring 뿐).

**`_persist`** — 미러 전체가 플래그 안으로 들어갔다.

| 자리 | 전 | 후 |
|---|---|---|
| 사람 안건 조회 | **항상** | `if mirror_human_agendas:`(`:615`) 안에서만 |
| `source_agenda_id` | `agenda.human_agenda_id`(항상) | `… if mirror_human_agendas else None`(`:632`) |
| 제목 | `source.title`(찾히면) | 같은 식이지만 `source` 는 미러일 때만 채워진다 → 회의 중은 **출력 `title` 그대로** |
| `state` | `source.state if (copy_human_state and source is not None)` | `source.state if source is not None` |

**최종 경로 동작이 동일함을 확인했다** — `mirror_human_agendas=True` 면 `human` 이 채워지므로 `source` 가 옛 코드와 같고, `state` 의 `copy_human_state and` 가 빠진 것은 `source` 자체가 이미 그 플래그로 걸러지기 때문이라 **결과가 같다**. 플래그 이름 변경(`copy_human_state` → `mirror_human_agendas`)은 이제 셋(조회 · `source_agenda_id` · 제목/state)을 다 가르므로 이름이 사실에 맞다.

**`_run_once` 의 사람 안건 조회 삭제는 계약이 요구한 것이다** — 브리프 §Code Surface 는 `_run_once` 를 「`phase="batch"` 만」으로 적었지만, ① SPEC-007 §5 「AI 는 `track='ai'` 에만 쓰고, **회의 중에는 사람 것을 읽지도 않는다**」 ② M-6 ③ SPEC-007 §6 AC 「`list_agendas`·`get_agenda` 를 부른 흔적이 없다」가 DB 조회까지 포함해 읽지 말 것을 요구한다. 남겨 두면 **죽은 조회**이면서 계약 위반이다. 정적 검사 `test_meeting_live_static.py:127` 이 `_run_once` 본문에 `MeetingTrack.HUMAN` · `list_agendas_by_track` 가 0건임을, 그리고 `_persist` 본문에서 `MeetingTrack.HUMAN.value` 가 **정확히 한 번** 나오고 그것이 `if mirror_human_agendas:` **뒤**임을 인덱스 비교로 잠근다. **타당한 최소 변경이다.**

### 2-4. 불변 (WORK-012 회귀 기준선)

| 검사 | 결과 |
|---|---|
| `ai_schemas/`(`meeting_notes.json`) | **diff 0** |
| `app/mcp/` | **diff 0** — MCP 서버는 계속 일곱을 노출하고, 안 여는 것은 워커 `enabled_tools` 다(WP §Dependency) |
| `app/front/src` | **diff 0** — 변경 목록에 프론트 소스가 하나도 없다 |
| 전량 교체 · 검증 0~5 자리 | `_run_once` 의 단계 주석·순서가 그대로이고 DELETE 는 여전히 `_persist` 안 하나 |
| WORK-012 최종 테스트 | `test_meeting_finalize.py` 가 **변경 목록에 없다** — 무수정 통과가 회귀 증거다 |
| 마이그레이션 · env | 없음 |

### 2-5. 테스트

| 항목 | 테스트 |
|---|---|
| batch 10줄 · 안건 도구 0 | `test_agent_options.py:71` |
| final 14줄 회귀 | `:63` |
| 두 phase 가 그 두 자리만 다르다 | `:86` |
| resume 에도 batch allow list | `:97` |
| `phase` 기본값 없음 | `:191` |
| `tm.` 접두 · `approval_policy` (두 phase) | `:149` · `:161` |
| approval 줄 수 3/7 | `:171` |
| 옵션 빌더 단일 | `:211` |
| **BE §12 6 확장** — `humanAgendaId` 가 실려도 폐기 아님 | `test_meeting_batch.py` `test_a_human_agenda_id_is_ignored_instead_of_discarding_the_batch`(옛 `…is_a_schema_violation` 을 **뒤집었다**) |
| **BE §12 7-b** — 중간 배치는 혼자 쓴다 | `:602` — 사람 안건 id 와 **다른 제목**을 함께 넣고 `(title, source_agenda_id, state, order_index)` 를 튜플로 대조 · 사람 안건 제목이 AI 트랙에 없음 · `sourceAgendaId` 전부 `null` |
| 프롬프트가 안건 도구를 안 부른다 | `test_the_batch_prompt_tells_the_ai_to_split_the_agendas_alone` + 정적 `test_meeting_live_static.py:111` |
| 중간 경로가 사람 안건을 안 읽는다 | 정적 `:127` |
| 대역이 `phase` 를 기록 | `fakes/agent.py` `AgentCall.phase` |

**BE §12 7-b 세 절이 전부 덮인다** — ① `source_agenda_id` 전부 `NULL`(`:602`) ② 프롬프트에 안건 도구 0(정적 `:111`) ③ `phase="batch"` 옵션의 `enabled_tools` 셋 · `phase="final"` 일곱(`test_agent_options.py:71` · `:63`).

---

## 3. WARN

### W-1. 옵션 기대값의 「손으로 적는다」가 약해졌다

- **자리**: `test_agent_options.py:31-48` `expected_config(tools)`
- WORK-009 는 approval 7줄을 **리터럴로 나열**했고, 이 함수의 docstring 은 지금도 「WP §Internal Interface Contract 의 목록 — **손으로 적는다**(빌더에서 만들면 검사가 아니다)」라고 말한다. 그런데 approval 줄이 `*(f'mcp_servers.tm.tools.{name}.approval_mode="approve"' for name in tools)` **생성식**으로 바뀌었다.
- **실질 강도는 크게 안 떨어진다** — 도구 이름은 `BATCH_TOOLS` · `FINAL_TOOLS` 리터럴이고 포맷 문자열도 프로덕션(`agent.py:120`, `_MCP_KEY` 를 씀)과 **독립적으로** 적혀 있어 포맷 오타는 여전히 잡힌다. 다만 「전 줄을 손으로 적는다」는 성질은 사라졌고 **docstring 이 사실과 어긋난다.**
- phase 가 둘이 되면서 14+10줄을 전부 나열하기 어려워진 사정은 이해되지만, 문구를 사실에 맞추거나 최소한 `final` 쪽만이라도 리터럴을 남기는 편이 WORK-009 가 세운 성질을 지킨다.

### W-2. `_run_once` 가 `human_agenda_ids=frozenset()` 를 넘긴다 — 지금은 무해하지만 뜻이 뒤집힌 자리다

- **자리**: `meeting_batch_service.py:344`
- 회의 중 경로는 `fill_final=False` 라 `_parse_output` 안에서 **이 인자가 아예 읽히지 않는다**(소속 검사가 `fill_final` 갈래에만 있다). 그래서 오늘 동작에는 영향이 없고 주석도 이유를 적었다.
- **문제는 값의 뜻이다** — 빈 집합은 「사람 안건이 하나도 없다」로 읽힌다. 누군가 나중에 이 호출에 `fill_final=True` 를 켜면 **모든 `humanAgendaId` 가 위반**이 되어 배치가 통째로 폐기된다. 「안 쓴다」를 「빈 집합」으로 표현한 자리라 다음 사람이 밟기 쉽다.
- WP §Internal Interface 가 「시그니처 **유지**」를 못박아 생긴 자리다 — 인자를 `frozenset() | None` 으로 두든 docstring 에 「`fill_final=False` 면 무시된다」를 인자 설명으로 올리든, 표현을 뜻에 맞추면 닫힌다.

---

## 4. 문서 공백

| # | 자리 | 무엇이 비었나 |
|---|---|---|
| **D-1** | WP §Code Surface — `app/back/service/meeting_service.py`(웜스타트 제출) 행 | 웜스타트 제출은 **WORK-010 이 `meeting_batch_service._warm_start_once` 로 옮겼다**(`:704-712`). WP 가 가리킨 `meeting_service.py` 에는 그 호출이 없고, 실제 수정도 `meeting_batch_service.py` 에서 났다. **코드가 맞고 WP 행이 옛 위치를 가리킨다** — 다음 WP 가 같은 자리를 짚을 때 헷갈릴 곳이다 |
| **D-2** | WP §Open Issues — 「`get_meeting` · `get_account` 도 중간에 닫힌다 … **본문에 명시된 셋이 전부이므로 추측으로 넓히지 않았다**」 | **이미 닫힌 것을 열린 판단으로 적어 두었다.** DEC-003 §8 「단계별 도구」 행이 「**`get_meeting` · `get_account` 도 중간 셋에 없다**」로 명시했고, SPEC-007 §4 도구 표도 그 둘을 「**최종만**」으로 적었다. 코드는 두 문서와 정확히 같다 — 이 Open Issue 는 **추측이 아니라 결정의 인용**이므로 닫아도 된다 |

---

## 5. 요약

**잠금이 프롬프트에서 설정으로 내려왔다.** `build_codex_options` 가 `phase` 를 받고 `_TOOLS_BY_PHASE` 하나가 `enabled_tools` 배열과 approval 줄 수 **둘만** 가른다 — 나머지 줄과 순서는 두 단계가 같은 코드를 지나므로 WORK-009 의 14줄 표가 `final` 에서 문자열까지 그대로다. `phase` 에 기본값이 없어 세 호출부가 모두 단계를 명시하고, `config` 가 resume 에도 실려 세션을 이어 써도 매 제출이 자기 allow list 를 가져간다.

**회의 중 AI 가 사람 것을 보는 길이 셋 다 끊겼다** — 도구(옵션 셋), 프롬프트(안건 도구 0건 · 「발화만 보고 네가 가른다」), DB(`_run_once` 의 사람 안건 조회 삭제 · `_persist` 의 미러 갈래가 플래그 안으로). `humanAgendaId` 는 오면 `None` 으로 눌리고 **폐기 사유가 아니다**(SPEC-007 §4 검증 2와 문장 단위로 일치). 최종 경로는 조건식 한 줄 밖에서 손대지 않았고 `test_meeting_finalize.py` 가 무수정이며 스키마·MCP·프론트 diff 가 0이다.

남은 둘은 가벼운 정리다 — **W-1** 옵션 기대값의 docstring 과 실제(생성식)가 어긋나고, **W-2** 「안 쓰는 인자」를 빈 집합으로 표현한 자리가 나중에 뜻이 뒤집힐 수 있다. 문서 쪽은 WP 두 줄(웜스타트 위치 · 이미 닫힌 Open Issue)을 손보면 된다. 커밋을 막을 무게는 없다.
