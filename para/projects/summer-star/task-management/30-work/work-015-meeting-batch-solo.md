---
type: work
id: WORK-015
title: "중간 배치는 AI 혼자 쓴다 — 도구 셋 · 미러 안건 폐기 · 조회 순서 절 삭제"
status: done
product: "task-management"
work_type: refactor
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 0
created_at: 2026-09-08
updated_at: 2026-09-08
tags:
  - product/task-management
  - doc/work
  - status/todo
links:
  baselines: [BASE-003]
  decisions: [DEC-003]
  specs: [SPEC-007]
  works: [WORK-009, WORK-010, WORK-011, WORK-012]
  releases: []
  related: [SPEC-008, WORK-013]
---

# 중간 배치는 AI 혼자 쓴다 — 도구 셋 · 미러 안건 폐기 · 조회 순서 절 삭제

**회의 중 AI 가 사람 노트를 읽는 길을 끊는다.** WORK-011 이 「배치는 컨텍스트를 받지 않고 **조회한다**」로 바꿨는데, 실물 회의 8·9 에서 그 조회가 **AI 요약을 사람 노트의 톤으로 끌고 갔다.** 「두 사람이 각자 적고 종료 후 합친다」(BASE-003 L37)가 무너진 것이다. 이 work 가 끝나면 회의 중 배치는 **발화만 보고** 안건을 스스로 가르고, `list_agendas` · `get_agenda` 는 **도구 자체가 열리지 않으며**(프롬프트 지시가 아니다), 미러 안건이 사라진다. **백엔드만 바뀐다 — 프론트 변경 0.**

> 1 파일 = 1 work = **빌드 계획**. dev 가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC 의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs` 와 index 에서 연결한다.
> **결정 원본은 `reference/2026-09-06-task-management-app/Meeting flow.md` §0 `MF-71` · §2-3 본문.** 계약과 부딪히면 그쪽이 이긴다.

## Meta

- Baseline: BASE-003 **L37**(회의에 사람과 AI 둘이 참가한다 — 각자 쓰고 종료 후 종합) · #6(AI 요약)
- Covers spec
  - **SPEC-007 §4 「AI 도구 7개」 표의 「단계」 열**(중간 셋 / 최종 일곱) · **`enabled_tools` 는 단계별 두 벌** 불릿
  - **SPEC-007 §4 「배치 입력」 표 3행**(싣지도 조회하지도 않는다 · 「조회 순서」 절을 두지 않는다)
  - **SPEC-007 §4 「배치 출력」** — `humanAgendaId` 는 회의 중 항상 `null`(값이 와도 서버가 무시)
  - **SPEC-007 §4 「검증 순서」 2 · 3 · 5행** — 2 에서 `humanAgendaId` 검사 제거(폐기 사유 아님) · 3 은 업무만 · 5 는 `source_agenda_id` 항상 `NULL`
  - **SPEC-007 §5** — 「AI 는 `track='ai'` 에만 쓰고, 회의 중에는 사람 것을 읽지도 않는다」 · 「빌더는 `phase` 를 받아 `enabled_tools` 를 두 벌로 낸다」
  - **SPEC-007 §6 AC** — 「워커가 `list_agendas`·`get_agenda` 를 **부른 흔적이 없다**」 · 「AI 안건에 배지가 없고 `source_agenda_id` 가 전부 `NULL`」 · 「중간 옵션 문자열의 `enabled_tools` 가 셋」
  - **DEC-003 §2**(AI 의 데이터 접근 — 단계별) · **§4**(AI 트랙 안건 축 · 배치 입력) · **§8 「단계별 도구」**
  - **BE `backend/README.md` §5-2**(배치 입력 · 옵션 빌더 `phase`) · **§10 MCP 도구 행** · **§12 6 · 7 · 7-b**
  - **ERD `database/domains/meeting.md` M-5-a · M-5-b · M-5-c · M-6 · M-7 · M-8**
- Depends on work: **WORK-011**(done — `_parse_output` · `_persist` · `build_batch_prompt` 의 현재 모양) · **WORK-012**(done — `fill_final=True` 최종 경로. 이 work 가 **건드리지 않아야 하는 쪽**이다). WORK-009(done — `build_codex_options` · 14줄 옵션 표)
- Parallel work: 없음 — **코드 워커는 한 번에 하나**
- Follow-up work: 없음
- **External dependency**
  - **코드 레포는 별도다** — 워크트리 `/Users/kknaks/orca/workspaces/task_management/docs-v1`(HEAD `5c72c25`)
  - 시안 없음 · 프론트 변경 없음 · 마이그레이션 없음

## Work Summary

| Field | Value |
|---|---|
| Type | refactor |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR | `kknaksss/docs-v1` |
| Blocker | 없음 |
| Next | Phase 1 — `build_codex_options(phase)` |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | SPEC-007 §6 AC 해당 3항목 대조 | todo |
| Design |  | 해당 없음 | — |
| FE |  | **해당 없음 — 프론트 파일을 열지 않는다** | — |
| BE |  | Phase 1~2 | todo |
| QA |  | 중간 옵션 문자열 10줄 · 배치 프롬프트 grep 0 · `source_agenda_id` 전부 NULL · 최종 경로 회귀 | todo |
| Ops |  | 없음 — 환경변수 변경 없음 | — |

## Scope

포함:

- **`build_codex_options(…, phase)`** — `phase: Literal["batch","final"]`. `enabled_tools` 와 툴별 `approval_mode` 줄이 **phase 별로 갈린다**(중간 셋 / 최종 일곱). 옵션을 만드는 곳은 **여전히 이 함수 하나**(WORK-009 의 정적 검사를 유지한다)
- **호출부에 `phase` 를 넘긴다** — 회의 중 배치 제출 = `"batch"` · 최종 제출(②) = `"final"` · 웜스타트 = `"final"`(도구 목록을 알려 주는 자리다. 실제 잠금은 매 제출의 `-c` 가 한다)
- **`build_batch_prompt()` 정리** — 「## 줄을 만들기 전에 — 순서대로 조회한다」 절(`list_agendas` → `get_agenda`)과 **「안건이 발화 구간마다 늘어나면 잘못하고 있는 것이다」** 문구를 **삭제**한다. 대신 「**발화만 보고 네가 안건을 가른다. 사람이 적은 것은 보지 않는다**」 + 남는 조회는 **업무 셋뿐**임을 적는다
- **`_parse_output(…, fill_final=False)` 가 `humanAgendaId` 를 무시한다** — 값이 와도 **`None` 으로 강제**하고 **`_SchemaViolation` 을 던지지 않는다**(MF-71 · SPEC-007 검증 2). `fill_final=True` 경로의 사람 안건 참조 검사는 **그대로**다
- **`_persist()` 의 미러 갈래 삭제**(중간 경로) — `human_agenda_id` 로 `source_agenda_id` 를 채우고 **사람 안건 제목을 복사**하던 분기를 없앤다. 중간 배치가 INSERT 하는 `track='ai'` 안건은 **`source_agenda_id=NULL` · `state=NULL` · `title` = 출력값 그대로**
- 테스트 — BE §12 **6**(`humanAgendaId` 가 와도 폐기 아님) · **7**(회의 중 참조 검사는 업무뿐) · **7-b**(신설 — 중간 배치는 혼자 쓴다) · **정적 검사 2종**

제외:

- **최종 경로(`fill_final=True` · `run_final` · `build_final_prompt` · `merged` 적재)** — **불변이다.** 사람 안건이 정확히 한 번씩 들어가는 검사(SPEC-008 §4)와 `merged` 안건의 `source_agenda_id` 는 **그대로 둔다**
- **MCP 서버(`app/mcp/`)** — 도구 일곱을 그대로 노출한다. 중간에 셋만 여는 것은 **워커 쪽 `enabled_tools`** 다. `app/mcp/` 파일을 열지 않는다
- **프론트** — AI 탭이 `sourceAgendaId` 로 배지/캡션을 가르는 코드가 있다면 **값이 항상 `null` 이라 캡션 갈래만 살아난다.** 화면 동작이 계약(SPEC-007 U-4)과 같으므로 이 work 는 프론트를 고치지 않는다 — 다르면 **Open Issues 로 올린다**
- **스키마 · 마이그레이션 · 트리거 수치 · WS 프레임 · 슬래시 명령어** — 바뀌지 않는다

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back` 만

| 경로 | 신규 / 수정 / 폐기 | 설명 |
|---|---|---|
| `app/back/integrations/agent.py` `build_codex_options()` | 수정 | 인자에 **`phase: Literal["batch","final"]`** 추가(키워드 전용). `mcp_servers.tm.enabled_tools=[…]` 와 툴별 `approval_mode` 줄을 phase 로 가른다. **내장 스위치 4줄 · url · headers · `sandbox` · `resume` 는 그대로** |
| 〃 `AgentGateway.run()` | 수정 | `phase` 를 받아 빌더에 넘긴다(기본값을 두지 않는다 — 호출부가 반드시 고르게) |
| `app/back/service/meeting_batch_service.py` `build_batch_prompt()` | 수정 | 「조회 순서」 절 · 「안건이 늘어나면 잘못」 문구 삭제 · 「발화만 보고 가른다」 · 남는 조회는 업무 셋 |
| 〃 `_parse_output(…, fill_final)` | 수정 | `fill_final=False` 면 `humanAgendaId` 를 **읽고 버린다**(`None` 강제 · 위반 아님). `True` 는 불변 |
| 〃 `_persist()` | 수정 | 중간 경로의 **미러 분기 삭제** — `source_agenda_id` 는 항상 `NULL`, 제목은 출력값. 최종 경로가 같은 함수를 쓰면 **`fill_final`(또는 track) 로 갈라 최종만 미러를 유지**한다 |
| 〃 `_run_once()` | 수정(최소) | 배치 제출 호출에 `phase="batch"` |
| 〃 `run_final()` | 수정(최소) | 최종 제출 호출에 `phase="final"` — **그 밖은 손대지 않는다** |
| `app/back/service/meeting_batch_service.py` `_warm_start_once`(웜스타트 제출 — WORK-010 이 여기로 옮겼다) | 수정(최소) | `phase="final"` |
| `app/back/tests/test_meeting_batch.py` | 수정 | 아래 §Execution 검증 |
| `app/back/tests/`(WORK-009 의 옵션 문자열 테스트) | 수정 | **14줄 표를 phase 별 두 벌로** — `final` = 14줄(기존 그대로) · `batch` = **10줄**(내장 4 + url + headers + `enabled_tools`(셋) + 툴별 approval **3**) |

- Domain / schema note: **리비전 0건.** 컬럼은 그대로고 바뀌는 것은 **`source_agenda_id` 를 채우는 자리**다(중간 → 없음, 최종 → 그대로)

## Domain / Schema

| Entity | 역할 |
|---|---|
| `meeting_agenda(track='ai')` | **`source_agenda_id` · `state` 가 항상 `NULL`** 이 된다. 전량 교체 규칙은 그대로 |
| `meeting_agenda(track='merged')` | **불변** — `source_agenda_id` 로 사람 안건을 가리킨다(최종만) |
| `meeting_line(track='ai')` | 불변 |

- 상태 / invariant: **M-5-b**(채우는 것은 최종뿐 · 중간은 전부 신설) · **M-5-c**(`ai` 안건 `state` 는 `NULL`) · **M-6**(회의 중에는 읽지도 않는다) · **M-7**(전량 교체 · INSERT 는 전부 `source_agenda_id NULL`) · **M-8**(두 트랙이 만나는 자리는 최종 하나) · M-15 · M-16(불변)
- Migration 필요 여부: **없음**
- SPEC 에 환류해야 하는 변경: 없음(SPEC-007 이 2026-09-08 v0.0.3 으로 이미 반영됐다)

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-012 최종 회의록**(done) | `build_codex_options(phase="final")` · `_parse_output(fill_final=True)` · `_persist` 최종 갈래 | **동작이 바뀌면 안 된다.** 이 work 의 회귀 기준선이다 — 최종 옵션 문자열 14줄 · 사람 안건 참조 검사 · `merged` 의 `source_agenda_id` |
| **WORK-009 옵션 표**(done) | `provider_options["config"]` 문자열 순서 | 테스트가 문자열로 비교한다 — **순서를 바꾸지 않는다.** phase 로 갈리는 것은 `enabled_tools` 배열과 approval 줄 수뿐 |
| MCP 서버 `app/mcp/` | 도구 일곱 | **바뀌지 않는다.** 서버는 계속 일곱을 노출하고, 안 여는 것은 워커 설정이다 |

## Internal Interface Contract

외부 계약(도구 표 · 배치 입출력 · 검증 순서)은 **SPEC-007 §4** 가 정본이다. 여기는 Phase 사이 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **`build_codex_options(*, session_id, output_schema, timeout_sec, meeting_token, phase)`** | `phase` 는 **키워드 전용 · 기본값 없음**. `"batch"` → `enabled_tools=["list_tasks","get_task","list_work_types"]` + 그 셋의 `approval_mode` 3줄. `"final"` → 일곱 + 7줄(WORK-009 표 그대로). **다른 줄은 두 phase 가 완전히 같다** |
| **`config` 줄 수** | `final` **14줄** · `batch` **10줄**. 순서는 WORK-009 목록 그대로(내장 4 → url → headers → enabled_tools → 툴별 approval) |
| **호출부 ↔ phase** | 웜스타트 = `"final"` · 회의 중 배치 = `"batch"` · 최종 제출(②) = `"final"`. **기본값이 없으므로 새 호출부가 생기면 컴파일/타입 검사에서 걸린다** |
| **`build_batch_prompt(...)`** | 출력 문자열에 **`list_agendas` · `get_agenda` 가 0건.** 「조회 순서」 · 「안건이 … 늘어나면 잘못」 문구 없음. 담는 것 — 발화 블록 · 「이번 구간을 반영해 **AI 트랙 전체를 다시 정리해라**」(MF-53 · 불변) · 「**안건은 발화만 보고 네가 가른다. 사람이 적은 것은 보지 않는다**」 · 「업무를 가리킬 때만 `list_tasks` · `get_task` · `list_work_types`」 |
| **`_parse_output(output, *, human_agenda_ids, last_end_ms, fill_final=False)`** | 시그니처 **유지**. `fill_final=False` 면 `humanAgendaId` 를 **읽고 버린다** — `human_agenda_ids` 대조를 하지 않고 `_SchemaViolation` 도 던지지 않는다(`payload`·`headline`·`termCorrections` 와 같은 취급 — SPEC-007 검증 4행의 자리로 내려온다). `fill_final=True` 는 **한 글자도 바뀌지 않는다** |
| **`_persist(...)`** | 중간 경로가 INSERT 하는 안건 = `{track:'ai', title:<출력 title>, source_agenda_id: NULL, state: NULL}`. **사람 안건을 조회하는 코드가 이 경로에 0건.** 최종 경로는 그대로 |
| **바뀌지 않는 것** | 스키마 파일 한 벌(`meeting_notes.json`) · 전량 교체 · 검증 순서 0~5 의 **자리** · 트리거 수치 · WS `ai.batch` 프레임 · 업무 사후 검사 · 프론트 |

## Execution

### Phase 1 — 옵션 빌더가 `phase` 를 받는다 (백엔드)

- **Status**: TODO
- **설명**: MF-71 의 잠금 축. **프롬프트로 「부르지 마라」 하는 것이 아니라 도구를 안 준다.** `-c` 는 `resume` 에도 실리므로 매 제출이 자기 phase 의 allow list 를 가져간다.
- **작업**:
  - [ ] `build_codex_options()` 에 `phase` 추가 — `enabled_tools` 배열과 툴별 `approval_mode` 줄만 갈린다
  - [ ] `AgentGateway.run()` 시그니처에 `phase` 전달(기본값 없음)
  - [ ] 호출부 셋에 phase 지정 — 웜스타트 `"final"` · `_run_once` `"batch"` · `run_final` `"final"`
  - [ ] WORK-009 옵션 문자열 테스트를 **두 벌로** 갱신(14줄 / 10줄)
- **검증**:
  - [ ] `phase="batch"` 옵션의 `config` 가 **10줄**이고 `mcp_servers.tm.enabled_tools=["list_tasks","get_task","list_work_types"]` 이며 **`list_agendas` · `get_agenda` · `get_meeting` · `get_account` 문자열이 0건**이다
  - [ ] `phase="final"` 옵션이 **WORK-009 의 14줄과 문자열·순서까지 동일**하다(회귀)
  - [ ] `enabled_tools` 에 `tm.` 접두가 없고 `approval_policy` 키가 없다(WORK-009 의 함정 두 개 — 회귀)
  - [ ] **정적 검사**: `provider_options` · `"config"` · `mcp_servers` 문자열을 만드는 곳이 `build_codex_options` **한 함수**뿐(WORK-009 검사 유지)
  - [ ] `phase` 인자 없이 부르는 호출부가 **0건**이다(기본값이 없어 실패해야 한다)
  - [ ] `make test` 전체 통과
- **완료 증거**: 미작성

### Phase 2 — 배치 프롬프트 · `humanAgendaId` 무시 · 미러 갈래 삭제 (백엔드)

- **Status**: TODO
- **설명**: MF-71 의 본체. **회의 중 AI 트랙은 사람 트랙과 완전히 분리된다.** 여기서 최종 경로를 건드리면 WORK-012 가 깨진다 — `fill_final` 로 갈린 자리만 만진다.
- **작업**:
  - [ ] `build_batch_prompt()` — 「조회 순서」 절 삭제 · 「안건이 발화 구간마다 늘어나면 잘못하고 있는 것이다」 삭제 · 「발화만 보고 네가 가른다 · 사람이 적은 것은 보지 않는다」 추가 · 남는 조회는 업무 셋
  - [ ] `_parse_output(fill_final=False)` — `humanAgendaId` 를 `None` 으로 강제하고 위반으로 세지 않는다
  - [ ] `_persist()` — 중간 경로의 미러 분기(`source_agenda_id` 대입 · 사람 안건 제목 복사) 삭제. 최종 경로 유지
  - [ ] `tests/test_meeting_batch.py` — 아래 검증 케이스
- **검증**:
  - [ ] **정적**: `build_batch_prompt` 가 낸 문자열에 `list_agendas` · `get_agenda` 가 **0건**(테스트 단언 + grep)
  - [ ] **BE §12 6 회귀 + 확장** — 잘못된 JSON 은 여전히 전체 폐기이고, **`humanAgendaId` 가 실린 정상 JSON 은 폐기되지 않는다**(줄이 들어가고 `source_agenda_id IS NULL`)
  - [ ] **BE §12 7-b** — 중간 배치 뒤 `track='ai'` 안건의 `source_agenda_id` 가 **전부 `NULL`**, `state` 가 전부 `NULL`, 제목이 **출력의 `title` 그대로**(사람 안건 제목을 복사하지 않는다)
  - [ ] **BE §12 7 회귀** — 회의 프로젝트 밖 `taskId` 강등 · 회의 중 `payload`·`headline`·`termCorrections` 미저장은 **그대로**다
  - [ ] **BE §12 7-a 회귀** — 전량 교체(두 번째 배치 뒤 첫 배치 행 0건 · 검증 실패 시 직전 성공분 유지)가 그대로다
  - [ ] **최종 경로 회귀** — `fill_final=True` 로 사람 안건 참조 검사가 살아 있고, `merged` 안건이 **사람 안건을 정확히 한 번씩** 가리킨다(WORK-012 테스트 무수정 통과)
  - [ ] **정적**: `_persist` 의 중간 갈래에서 사람 안건을 조회하는 호출이 0건
  - [ ] `make test` 전체 통과
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] 환경변수 변경 **없음**
- [ ] 마이그레이션 **없음**
- [ ] **프론트 배포와 짝을 이루지 않는다** — WS 프레임·응답 모양이 그대로다. 백엔드만 올려도 된다
- [ ] **진행 중인 회의가 있으면** 배포 뒤 첫 배치부터 미러 안건이 사라진다(전량 교체라 자동으로 정리된다 — 사용자에게 보이는 것은 AI 탭 배지가 캡션으로 바뀌는 것뿐)
- [ ] 이미 끝난 회의의 `merged` 안건은 **건드리지 않는다**(백필 없음)

## Rollback

- **스키마**: 없음
- **백엔드**: revert 하면 중간 배치가 다시 안건 도구 둘을 열고 미러 안건을 만든다. **데이터 손상은 없다** — AI 트랙은 매 배치 전량 교체라 다음 배치가 덮는다
- **프론트**: 변경 없음 — 되돌릴 것이 없다
- 부분 revert: **Phase 1 만 되돌리면 안 된다** — 도구는 열려 있는데 프롬프트가 조회를 안 시키는 어정쩡한 상태가 된다. 되돌린다면 **둘을 함께** 되돌린다

## Done Criteria

- [x] 모든 Phase 가 `DONE` 이다
- [ ] **SPEC-007 §6 AC 3항목**이 실측으로 확인된다 — ① 서버 로그에 워커가 `list_agendas`·`get_agenda` 를 **부른 흔적이 없다** ② AI 탭 안건이 전부 「AI 안건」 캡션이고 DB 의 `track='ai'` `source_agenda_id` 가 전부 `NULL` ③ 회의록 탭에 안건을 적어 둔 뒤 배치를 돌려도 AI 탭에 그 사본이 생기지 않는다
- [ ] **실물 회의 1건**에서 AI 요약이 사람 노트의 문장을 따라 적지 않는다(MF-71 이 풀려던 그 증상 — 사용자 확인)
- [ ] BE §12 **6 · 7 · 7-a · 7-b** 테스트가 있다
- [ ] 정적 검사 3종(배치 프롬프트 안건 도구 0 · 중간 옵션 문자열 안건 도구 0 · 옵션 빌더 한 함수)
- [ ] WORK-012 의 최종 경로 테스트가 **무수정으로** 통과한다
- [x] `make test` 전체 통과 · `vitest` 무변경
- [x] `30-work/README.md` 갱신

> 2026-09-08 — 커밋 `1ca243e`. 검수 `orchestration/work/docs-v1/work015-review-report.md` FAIL 0 · WARN 2(옵션 테스트 docstring 문구 · `_run_once` 의 `frozenset()` 센티널 — 다음 백엔드 발주에). pytest 652. **미완: 실물 회의에서 톤이 갈라지는지 확인은 사용자(버그 다 닫힌 뒤 한 번에)** · 웜스타트 phase=final 은 사용자 확인 대기

## Open Issues

- **웜스타트에 어느 phase 를 주나 — 이 work 는 `"final"` 로 둔다.** MF-71 본문은 「중간 배치의 `enabled_tools` 는 업무 셋 · 최종 제출은 일곱」만 정했고 **웜스타트는 말하지 않았다.** 웜스타트는 도구 **목록을 알려 주는** 자리이고 그때는 요청이 없으므로 실제 잠금은 매 제출의 `-c` 가 한다(`-c` 는 resume 에도 산다 — MF-71 본문). 판단이 틀렸다면 웜스타트도 `"batch"` 로 바꾸면 되고 **다른 코드는 그대로다.** ⚠ **사용자 확인 항목**
- **웜스타트 프롬프트의 도구 목록 문구** — WORK-010 이 심은 「쓸 수 있는 도구」에 일곱이 적혀 있다면, 회의 중에 그중 넷이 안 열린다. 도구가 없으면 codex 는 그냥 못 부르므로 **동작은 안전**하지만 문구는 어긋난다. **이 work 는 웜스타트 프롬프트를 건드리지 않는다**(WORK-010 소관) — 실물에서 AI 가 「도구를 못 찾겠다」는 말을 내면 그때 문구를 좁힌다. ⚠ **관찰 항목**
- ~~`get_meeting` · `get_account` 도 중간에 닫힌다~~ — **닫힘**(검수 2026-09-08): DEC-003 §8 「단계별 도구」 행과 SPEC-007 §4 표가 그 둘을 「최종만」으로 명시했다. 추측이 아니라 결정의 인용이다
- **프론트의 미러 배지 코드** — SPEC-007 U-4 가 미러 배지 갈래를 지웠으나 이 work 는 프론트를 열지 않는다. `sourceAgendaId` 가 항상 `null` 이라 **화면은 계약대로 캡션만 그린다.** 죽은 갈래를 지우는 것은 별건이다(값이 `merged` 에서는 여전히 살아 있어 SPEC-008 화면이 쓴다)
- **이미 저장된 미러 AI 안건** — 백필하지 않는다. AI 트랙은 매 배치 전량 교체라 진행 중 회의는 다음 배치에서 정리되고, 끝난 회의의 `ai` 트랙은 최종 회의록이 나온 뒤에는 참조되지 않는다

## Related

- 결정 원본: `reference/2026-09-06-task-management-app/Meeting flow.md` §0 **MF-71** · §2-3(MF-50 · 51 의 괄호 정정 포함) · **`ai-prompt-draft.md` §B 정정 2**
- SPEC: SPEC-007 §4 · §5 · §6 · U-4 · DEC-003 §2 · §4 · §8
- Architecture: `backend/README.md` §5-2 · §10 · §12 6 · 7 · 7-b · `database/domains/meeting.md` M-5-a · M-5-b · M-5-c · M-6 · M-7 · M-8
- Work: WORK-009 · WORK-011(선행) · WORK-012(회귀 기준선)
