---
type: work
id: WORK-011
title: "회의 중 — 배치 입력은 발화뿐 · AI 트랙 전량 교체 · 슬래시 5 · 줄 시각 제거"
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
created_at: 2026-09-07
updated_at: 2026-09-07
tags:
  - product/task-management
  - doc/work
  - status/todo
links:
  baselines: [BASE-003]
  decisions: [DEC-003]
  specs: [SPEC-007]
  works: [WORK-007, WORK-009, WORK-010]
  releases: []
  related: [SPEC-006, SPEC-008, WORK-012, WORK-013]
---

# 회의 중 — 배치 입력은 발화뿐 · AI 트랙 전량 교체 · 슬래시 5 · 줄 시각 제거

**AI 가 컨텍스트를 「받는」 것에서 「조회하는」 것으로 바뀐다.** 지금 배치는 안건 · 사람 줄 · AI 안건 · 화이트리스트를 payload 에 실어 보내고 **추가할 줄만** 받는다. 이 work 가 끝나면 배치 입력은 **미처리 발화 하나**뿐이고, AI 는 MCP 도구(WORK-009)로 그 순간을 조회하며, 출력은 **AI 트랙 전체**라 서버가 매 배치 **DELETE + INSERT** 로 갈아끼운다. 화면 쪽에서는 **슬래시 명령어 5개**가 생기고 **줄의 시각이 사라진다**.

> 1 파일 = 1 work = **빌드 계획**. dev 가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC 의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs` 와 index 에서 연결한다.
> **결정 원본은 `reference/2026-09-06-task-management-app/Meeting flow.md`** — **MF-9 · 10 · 49 · 50 · 51 · 52 · 53**. 계약과 부딪히면 그쪽이 이긴다.

## Meta

- Baseline: BASE-003 #5(회의 중 입력) · #6(AI 요약) · #7(근거)
- Covers spec
  - **SPEC-007 U-2**(사람 트랙 — **줄에 시각을 붙이지 않는다** · 회의 중 읽기 전용) · **U-3**(프롬프트 바 · `/` 팝오버 · **슬래시 명령어 5개** · 좁혀지는 팝오버) · **U-4**(AI 요약 탭 — **트리가 통째로 바뀐다** · 줄 시각 없음 · `payload` 항상 `null`)
  - **SPEC-007 §4 「AI 배치 계약」 → 「배치 입력」 표 · 「배치 출력」 블록 · 「검증 순서」 표 0~5행** · **§4 WS 서버→클라이언트 `ai.batch` 행**(AI 트랙 **전체**) · **§4 「AI 트랙 항목 형태」**
  - **SPEC-007 §5** — 「배치 트리거 … 미처리 확정 발화 **1000자**」 · 「AI 는 `track='ai'` 에만 쓰고 읽기는 도구로 한다」 · 「배치마다 AI 트랙을 전량 교체한다 — 검증을 통과한 결과로만」 · 「프롬프트 바의 슬래시 명령어는 화면 안에서 끝난다」 · 「줄에 시각을 그리지 않는다」
  - **SPEC-007 §6 AC** 해당 8항목(1000자 → 배치 1회 · 트리 · 두 번째 배치 전량 교체 · 스키마 위반 폐기 · `/결` 좁힘 · `/api 경로를…` 본문 · 줄 시각 없음 · 강등)
  - **FE §8**(AI 증분 = AI 트랙 전체 · 트리 통째 교체 · 줄에 시각 없음) · **ERD M-6 · M-6-a · M-7 · M-15 · M-16**
- Depends on work: **WORK-009**(MCP 도구 7개 · 토큰 · `build_codex_options`) · **WORK-010**(웜스타트 프롬프트가 도구 목록·용어 다섯을 이미 심어 둔다 — 배치 프롬프트가 그것을 전제로 짧아진다. **같은 파일 `meeting_batch_service.py` 를 만지므로 010 이 먼저다**) · WORK-007(현행 배치 구현)
- Parallel work: 없음 — **코드 워커는 한 번에 하나**
- Follow-up work: **WORK-012**(같은 스키마 파일 · 같은 검증 함수를 쓴다) → WORK-013
- **External dependency**
  - **코드 레포는 별도다** — 워크트리 `/Users/kknaks/orca/workspaces/task_management/docs-v1`
  - **`ai_schemas/meeting_notes.json` 은 이 work 가 만든다**(아래 §Code Surface 주 — 소유 WP 하나). WORK-012 는 **같은 파일을 읽기만** 한다
  - 시안 없음 — 프롬프트 바 · 팝오버 규격은 **시안 L918~972 그대로**이고 더하는 것은 슬래시 명령어(화면 안 동작)뿐이다

## Work Summary

| Field | Value |
|---|---|
| Type | refactor |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR | `kknaksss/docs-v1` |
| Blocker | 없음 |
| Next | Phase 1 — 스키마 한 벌 · 배치 입력·출력 재작성 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | SPEC-007 §6 AC 해당 8항목 대조 | todo |
| Design |  | 해당 없음 — 새 시안 없음(팝오버·트리는 기존 규격) | — |
| FE |  | Phase 3~4 | todo |
| BE |  | Phase 1~2 | todo |
| QA |  | 배치 입력에 발화만 · 두 번째 배치 후 첫 배치 행 0건 · 폐기 시 직전 성공분 유지 · 슬래시 5개 밖은 본문 · 줄 시각 0건 | todo |
| Ops |  | `MEETING_BATCH_CHARS` 기본값 변경(600→1000) — `.env.example` 주석 | todo |

## Scope

포함:

- **배치 입력을 발화 하나로**(MF-50) — `_BatchInput` 에서 `human_agendas` · `human_lines` · `ai_agendas` · `tasks` 를 뺀다. `_load_input()` 이 읽는 것은 **회의 컨텍스트 · `seq` · 미처리 확정 블록**뿐
- **배치 프롬프트 재작성**(초안 `ai-prompt-draft.md` §B) — **조회 순서 지시**(`list_agendas()` → `get_agenda(id)` → 업무를 가리킬 때만 `list_tasks()` · `get_task(id)` · `list_work_types()`) + 「이번 구간을 반영해 **AI 트랙 전체를 다시 정리해라**」
- **출력 스키마 한 벌** — `ai_schemas/meeting_batch.json` → **`ai_schemas/meeting_notes.json`** 으로 이름을 바꾸고 모양을 `{headline, termCorrections, agendas[{humanAgendaId, title, lines[{kind, content, detail, evidence, taskId, payload}]}]}` 로 재작성. `headline` · `termCorrections` · `payload` 는 **nullable**(회의 중은 `null` · 최종에서만 값 — MF-52)
- **검증 순서 0~5 를 SPEC 표대로**(§4 「검증 순서」) — ② 스키마 위반 = 전체 폐기 · ③ 업무 참조 **검사 시점 조회** 강등 · ④ 회의 중 `payload`/`headline`/`termCorrections` **버림** · ⑤ **전량 교체**
- **`_persist()` 를 전량 교체로**(MF-53) — 지금 `run_final` 에 있는 「줄 → 안건 DELETE 후 INSERT」를 **매 배치**로 옮긴다. **검증을 통과한 뒤에만 지운다**
- **트리거 수치 1000자**(MF-49) — `config.meeting_batch_chars` 600 → 1000
- **WS `ai.batch` 프레임을 AI 트랙 전체로** — 안건 안에 줄이 중첩된 모양(상세 응답 `agendas.ai` 와 같다)
- **프론트** — 슬래시 명령어 5개 · 좁혀지는 팝오버 · **줄 시각 제거** · `mergeAiBatch` 를 **통째 교체**로
- 테스트 — BE §12 **6**(스키마 위반 폐기) · **7**(강등 · 회의 중 `payload` 미저장) · **7-a**(전량 교체) · FE §11 (프롬프트 바 · AI 탭 교체)

제외:

- **웜스타트 · `/start`** → WORK-010(선행). 이 work 는 `build_warm_start_prompt` 를 건드리지 않는다
- **`run_final` · `_load_final_input` · `build_final_prompt` · 재전사 · 최종 회의록 · `merged`** → WORK-012. 이 work 는 **`run_final` 을 남겨 둔다**(012 가 폐기) — 단 `_BatchInput` 이 줄어들면서 `_load_final_input` 도 **같이 컴파일돼야 한다**(아래 §Internal Interface 「과도기 규칙」)
- **종료 후 편집 · payload 드로어 · 줄 삭제** → WORK-013
- **breadcrumb · 헤더 순서 · 미리보기 패널** → WORK-014
- 안건 전환 트리거 · 180초 · 120초 상한 · WS 인증 · 백프레셔 — 바뀌지 않는다

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · `app/front`(FE) · `.env.example`

| 경로 | 신규 / 수정 / 폐기 | 설명 |
|---|---|---|
| `app/back/ai_schemas/meeting_notes.json` | **신규(이름 변경 + 재작성)** | **이 work 가 소유한다.** `meeting_batch.json` 을 이 이름으로 옮기고 모양을 바꾼다 — 최상위 `{headline, termCorrections, agendas[]}`, 안건 `{humanAgendaId, title, lines[]}`, 줄 `{kind, content, detail, evidence, taskId, payload}`. `headline`·`termCorrections`·`payload` nullable. **`aiAgendaId`·`newTitle`·`items` 는 없다** |
| `app/back/ai_schemas/meeting_batch.json` | **폐기** | 위 파일로 대체(git mv) |
| `app/back/service/meeting_batch_service.py` `_BatchInput` | 수정 | 필드 = `meeting` · `seq` · `blocks` **셋**. `whitelist` 프로퍼티 **폐기**(검사 시점 조회로 옮긴다) |
| 〃 `_load_input()` | 수정 | `list_agendas_by_track`·`list_human_lines_since`·`list_meeting_context` 호출 **삭제**. 커서 · 블록만 |
| 〃 `build_batch_prompt()` | 수정(전면) | 발화만 + 조회 순서 + 「AI 트랙 전체를 다시 정리해라」(§Internal Interface) |
| 〃 `_OutputLine` | 수정 | `human_agenda_id` · `ai_agenda_id` · `new_title` → **`_OutputAgenda`(신규 dataclass: `human_agenda_id: int\|None` · `title` · `lines`)** 아래로 옮긴다. 줄은 `kind`·`content`·`detail`·`evidence`·`task_id` |
| 〃 `_parse_output()` | 수정 | 새 스키마. `humanAgendaId` 가 이 회의 **사람 안건**인지 확인(검사 시점 조회) · `evidence` 범위 · **AI 안건 id 참조 갈래 삭제**(매 배치 새로 생긴다) · `payload`·`headline`·`termCorrections` 는 **읽고 버린다** |
| 〃 `_demote_if_needed()` | 수정 | 인자에서 `whitelist` 제거 → **검사 시점에** `task_repository.list_meeting_context(account_id, project_id)` 로 조회한 id 집합을 받는다(`_run_once` 가 ④ 직전에 한 번 조회) |
| 〃 `_persist()` | 수정 | 앞에 **`delete_by_track` → `delete_agendas_by_track`**(줄 → 안건 순 · FK) 를 넣고 그 뒤 INSERT. `ai_agenda_id` 분기 · `created_by_title` 분기 삭제 — 출력이 안건 목록을 그대로 주므로 안건마다 한 번씩 만든다 |
| 〃 `_run_once()` | 수정 | ④ 강등 앞에 화이트리스트 조회 · ⑤ 트랜잭션이 전량 교체를 포함 · push 는 **전체 트리** |
| 〃 `run_final()` · `_load_final_input()` · `build_final_prompt()` | 수정(최소) | `_BatchInput` 변경에 맞춰 **컴파일만 되게** 손본다. **의미는 WORK-012 가 갈아엎는다** — 여기서 지우지 않는다 |
| 〃 `_agenda_rows()` | 수정 없음 | `build_final_prompt` 가 아직 쓴다. 폐기는 WORK-012 |
| `app/back/service/meeting_stream_service.py` `push_ai_batch()` | 수정 | 인자 `agendas` **하나**(줄이 중첩된 트리 DTO). `lines` 인자 폐기 |
| `app/back/schemas/meeting_stream.py` `AiBatchMessage` | 수정 | `agendas: list[AgendaItem]` — 줄이 안건 안에 중첩(SPEC-007 §4 `ai.batch` 행). 최상위 `lines` 키 삭제 |
| `app/back/dto/meeting_stream.py` `AiBatchFrame` | 수정 | 〃 |
| `app/back/config.py` | 수정 | `meeting_batch_chars: int = 600` → **`1000`**(MF-49) |
| `.env.example` | 수정 | `MEETING_BATCH_CHARS` 주석의 값 |
| `app/back/tests/test_meeting_batch.py` | 수정(전면) | 입력·출력·전량 교체·강등 |
| `app/front/src/features/meetings/components/PromptBar.tsx` | 수정 | **슬래시 명령어 5개**(`/논의` `/결정` `/업무` `/액션` `/새안건`) — 스페이스에서 칩으로 · 백스페이스로 되돌림 · 그 밖의 `/…` 는 본문. 「안건 이동」은 슬래시로 하지 않는다 |
| 〃 `LineKindPopover.tsx` | 수정 | `/` 뒤 글자로 **좁혀지는** 목록(앞글자 일치). 항목 4종·「새 안건」·「다른 안건으로 이동」 구조는 그대로 |
| 〃 `LineRow.tsx`(L118 부근) | 수정 | `formatClock(line.createdAt)` **삭제**(MF-9). `formatClock` import 가 이 파일에서 안 쓰이면 함께 정리 |
| 〃 `AgendaHeader.tsx` | 수정 없음(확인) | 안건 우측 시각은 **남는다**(MF-9 — 시각은 안건에만) |
| 〃 `aiBatch.ts` `mergeAiBatch()` | 수정(전면) | 병합 → **`agendas.ai` 를 프레임의 트리로 통째 교체.** `orphaned` 개념 폐기 |
| 〃 `hooks/useMeetingStream.ts`(L214 `case "ai.batch"`) | 수정 | 교체 결과를 `setQueryData` — `orphaned>0` 재조회 갈래 삭제 |
| 〃 `features/meetings/types.ts` | 수정 | `AiBatchFrame` 타입을 중첩 트리로 |
| 〃 `PromptBar.test.tsx` · `aiBatch.test.ts` · `MeetingLiveView.test.tsx` | 수정 | 위 동작 |

- Domain / schema note: **리비전 0건.** DB 컬럼은 그대로다 — 바뀌는 것은 **쓰는 방식**(INSERT 만 → 전량 교체)이다

## Domain / Schema

| Entity | 역할 |
|---|---|
| `meeting_agenda(track='ai')` · `meeting_line(track='ai')` | **배치마다 통째로 갈린다.** id 가 매번 새로 생긴다 |
| `meeting_batch_run` | 커서(성공분 `to_transcript_id`) · `seq` · `status`. 규칙 그대로 |
| `meeting_transcript` | 읽기만 — 커서 이후 확정 블록 |

- 상태 / invariant: **M-7**(전량 교체 · 검증 뒤에만 DELETE) · **M-6**(AI 는 `ai` 트랙에만 쓰고 읽기는 도구로) · **M-6-a**(즉시 push · 회차는 파생) · **M-15 · M-15-a**(사후 검사 기준 = 검사 시점 조회 · 무소속 회의는 무소속 업무) · **M-16**(스키마 위반 전체 폐기) · **M-5-b**(미러 안건 = `source_agenda_id`, 신설 = `NULL`) · **M-11**(줄에 시각을 붙이지 않는다)
- Migration 필요 여부: **없음**
- SPEC 에 환류해야 하는 변경: 없음

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-012 회의 종료** | `ai_schemas/meeting_notes.json` · `_parse_output()` · `_demote_if_needed()` · `_persist()` | ② 최종 회의록이 **같은 스키마 파일 · 같은 검증 함수**를 쓴다(SPEC-008 §5 「다른 것은 「버리나 채우나」 스위치 하나뿐」). 이 work 가 그 함수들을 **`fill_final: bool` 스위치를 받을 수 있는 모양**으로 남긴다 |
| **WORK-013 편집** | `LineRow.tsx` · `LineKindPopover.tsx` | 013 이 같은 파일에서 `LineKindSelector` 를 걷어낸다 — **011 이 먼저** |
| 프론트 화면 | WS `ai.batch` | 프레임 모양이 바뀐다 — 백·프론트가 **한 PR 안**에 있어야 한다 |

## Internal Interface Contract

외부 계약(배치 입출력 · 검증 순서 · WS 프레임)은 **SPEC-007 §4** 가 정본이다. 여기는 Phase 사이 · 후속 WP 가 기대는 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **스키마 파일** | **`ai_schemas/meeting_notes.json` 하나.** 이 work 가 만들고 WORK-012 는 **읽기만** 한다. 두 WP 가 같은 파일을 만들지 않는다. 배치·최종이 같은 파일을 `output_schema` 로 건다 |
| **`_parse_output(output, *, human_agenda_ids, last_end_ms, fill_final: bool = False)`** | 하나의 함수가 배치와 최종을 모두 판다. `fill_final=False` 면 `payload`·`headline`·`termCorrections` 를 **읽고 버린다**(폐기 사유 아님 — MF-52 · 검증 순서 4행). `True` 는 WORK-012 가 켠다. **부분 파싱 없음** — 어긋나면 `_SchemaViolation` |
| **`_demote_if_needed(line, allowed_task_ids, *, meeting_id)`** | 화이트리스트를 **입력에 싣지 않고 검사 시점에 조회**한 집합을 받는다(MF-50 · M-15). 밖이거나 `kind='task'` 인데 `taskId` 없음 → **그 줄만** `taskId`·`payload` 를 떼고 `action` 강등. 본문·상세·근거는 산다 |
| **`_persist(session, meeting_id, agendas)`** | **DELETE(줄 → 안건) + INSERT 를 한 함수 안에서.** 호출 전에 검증이 끝나 있어야 한다 — 검증 전에 지우면 실패 시 직전 성공분이 사라진다(M-7). `humanAgendaId` 가 있으면 `source_agenda_id` = 그 id · 제목은 **사람 안건의 제목을 복사**, 없으면 `source_agenda_id=NULL` |
| **트리거** | 셋 중 먼저 오는 것 — ① 미처리 **1000자** ② 안건 전환(미처리 80자 미만이면 생략) ③ 180초. **동시 실행 0 · `ai_session_id` 없으면 미제출** — 기존 규칙 그대로다 |
| **WS `ai.batch`** | `{type:"ai.batch", seq, agendas:[AgendaItem…]}` — **`AgendaItem.lines[]` 안에 줄이 중첩**된다. 상세 응답 `agendas.ai` 와 **같은 직렬화 함수**를 쓴다(모양이 둘로 갈리지 않게) |
| **프론트 `mergeAiBatch(detail, frame)`** | 이름은 남기되 **동작은 교체**다 — `detail.agendas.ai = frame.agendas`. 병합·고아 판정이 없다. 반환은 새 `MeetingDetail` |
| **슬래시 명령어** | **5개뿐**(`/논의` `/결정` `/업무` `/액션` `/새안건`). **스페이스가 들어오는 순간** 명령어 문자열이 사라지고 칩이 붙는다. 백스페이스로 칩 앞에서 지우면 텍스트로 복귀. 그 밖의 `/…` 는 **그대로 본문**(이스케이프·갈래 없음). **서버는 `kind` 와 `content` 만 받는다** — 명령어 문자열을 파싱하는 코드가 백엔드에 0건 |
| **과도기 규칙** | 이 work 는 `run_final` · `_load_final_input` · `build_final_prompt` 를 **지우지 않는다**(WORK-012 가 지운다). `_BatchInput` 이 줄었으므로 그 셋이 필요로 하던 값은 **함수 안에서 직접 조회**하도록 최소 수정한다 — 「빌드는 되고 동작은 옛것」 상태로 남긴다 |

## Execution

### Phase 1 — 스키마 한 벌 · 배치 입력 · 검증 순서 (백엔드)

- **Status**: TODO
- **설명**: MF-50 · 52. 입력에서 컨텍스트를 걷어내고 스키마를 한 벌로 만든다. 이 Phase 뒤에도 **트랙은 아직 INSERT 만** 한다(전량 교체는 Phase 2).
- **작업**:
  - [ ] `git mv ai_schemas/meeting_batch.json ai_schemas/meeting_notes.json` + 모양 재작성
  - [ ] `_BatchInput` 축소 · `_load_input` 축소 · `whitelist` 프로퍼티 폐기
  - [ ] `_OutputAgenda` 신설 · `_parse_output` 재작성(`fill_final` 스위치) · `_demote_if_needed` 인자 변경
  - [ ] `build_batch_prompt` 재작성(발화 + 조회 순서 + 「전체를 다시 정리해라」)
  - [ ] `config.meeting_batch_chars` 1000 · `.env.example`
  - [ ] `run_final`·`_load_final_input`·`build_final_prompt` 최소 수정(컴파일)
- **검증**:
  - [ ] 제출된 배치 프롬프트에 **`humanAgendas`·`humanLines`·`aiAgendas`·`taskWhitelist` 가 0건**이고 `transcript` 블록만 있다(테스트 단언 + grep)
  - [ ] 프롬프트에 조회 순서 세 단계(`list_agendas` → `get_agenda` → `list_tasks`/`get_task`/`list_work_types`)가 그 순서로 있다
  - [ ] 스키마 파일이 **하나**다 — `ai_schemas/` 에 `meeting_batch.json` 이 없다(`meeting_integration.json` 은 WORK-012 가 지운다)
  - [ ] **BE §12 6** — 잘못된 JSON 이 오면 줄이 하나도 안 들어가고 구간이 다음 배치로 넘어간다
  - [ ] **BE §12 7** — 회의 프로젝트 밖 `taskId` 줄이 `action` 으로 강등되고 **본문이 남는다**. 회의 중 결과의 `payload`·`headline`·`termCorrections` 는 **저장되지 않는다**(컬럼이 `NULL`)
  - [ ] `taskId` 검사가 **입력이 아니라 검사 시점 조회**를 쓴다 — 배치 제출 뒤에 만든 업무를 AI 가 참조해도 강등되지 않는다(테스트)
  - [ ] `make test` 전체 통과
- **완료 증거**: 미작성

### Phase 2 — AI 트랙 전량 교체 · WS 프레임 (백엔드)

- **Status**: TODO
- **설명**: MF-53 · M-7. 「앞 배치가 잘못 가른 안건을 다음 배치가 합친다」가 성립하는 자리.
- **작업**:
  - [ ] `_persist()` 앞에 DELETE(줄 → 안건) 를 넣고 INSERT 를 안건 목록 기준으로 재작성
  - [ ] `_run_once()` — ④ 앞 화이트리스트 조회 · ⑤ 한 트랜잭션 · push 전체 트리
  - [ ] `push_ai_batch(agendas)` · `AiBatchFrame` · `AiBatchMessage` 중첩 모양
  - [ ] `tests/test_meeting_batch.py` 전량 교체 케이스
- **검증**:
  - [ ] **BE §12 7-a** — 두 번째 배치 결과가 들어오면 **첫 배치의 AI 안건·줄 id 가 DB 에 남아 있지 않다**. 두 번째가 검증에 떨어지면 **첫 배치 것이 그대로다**
  - [ ] 검증 실패(스키마 위반) 경로에서 **DELETE 가 실행되지 않는다**(코드 순서 + 테스트)
  - [ ] `ai.batch` 프레임의 `agendas[].lines[]` 가 상세 응답 `agendas.ai` 와 **같은 모양**이다(같은 직렬화 함수를 지난다는 정적 검사)
  - [ ] 미러 안건은 `source_agenda_id` 가 사람 안건을 가리키고 제목이 사람 안건 것과 같다. AI 신설 안건은 `source_agenda_id IS NULL` · `state IS NULL`
  - [ ] `make test` 전체 통과
- **완료 증거**: 미작성

### Phase 3 — 프롬프트 바 슬래시 5 · 좁혀지는 팝오버 (프론트)

- **Status**: TODO
- **설명**: MF-10. **마우스 길(팝오버)과 키보드 길(명령어)이 같은 상태로 끝난다.** 팝오버를 없애지 않는다.
- **작업**:
  - [ ] `PromptBar.tsx` — 입력 파서: 앞 토큰이 5개 중 하나 + 스페이스 → 칩. 백스페이스 복귀. 그 밖은 본문
  - [ ] `LineKindPopover.tsx` — `/` 뒤 글자로 항목 좁힘(앞글자 일치)
  - [ ] `/새안건 <제목>` → `POST …/agendas` → `PATCH …/agendas/{id} {state:"active"}` 두 요청(기존 「새 안건」 경로 재사용)
  - [ ] `PromptBar.test.tsx`
- **검증**:
  - [ ] `/결` 까지 치면 팝오버가 「결정」만 남고, `/결정 `(스페이스)에서 **[결정] 칩**이 붙으며 명령어 문자열이 사라진다. 백스페이스로 되돌아온다
  - [ ] `/api 경로를 바꾸자` → **논의 줄 본문에 `/api …` 그대로**. `/논의 /api` → [논의] + 본문 `/api`. `/ㅁㄴㅇㄹ 어쩌고` → 본문
  - [ ] **「안건 이동」이 슬래시로 되지 않는다** — 명령어 목록에 없다
  - [ ] 팝오버로 고른 상태와 명령어로 고른 상태가 **DOM 상 같다**(같은 칩 · 같은 요청 본문 — 테스트)
  - [ ] 안건이 없으면 칩이 「안건 선택」이고 전송 버튼 비활성이며 `/새안건` 만 칩이 된다
  - [ ] `vitest` 전체 통과
- **완료 증거**: 미작성

### Phase 4 — AI 탭 통째 교체 · 줄 시각 제거 (프론트)

- **Status**: TODO
- **설명**: MF-53 · MF-9. 트리가 통째로 바뀌므로 화면이 id 를 붙들면 안 된다.
- **작업**:
  - [ ] `aiBatch.ts mergeAiBatch()` 를 교체 동작으로 · `orphaned` 폐기
  - [ ] `useMeetingStream.ts` `case "ai.batch"` 정리(재조회 갈래 삭제)
  - [ ] `LineRow.tsx` — `formatClock(line.createdAt)` 블록 삭제
  - [ ] `aiBatch.test.ts` · `MeetingLiveView.test.tsx` · `AgendaLineTree.test.tsx` 갱신
- **검증**:
  - [ ] 두 번째 `ai.batch` 가 오면 AI 탭 트리가 **새 결과로 통째로** 바뀌고 펼쳐 둔 줄이 접힌다(id 가 새로 생겨서)
  - [ ] **회의록 탭 · AI 탭 어느 줄에도 시각이 없다.** 안건 헤더 시각 · 「배치 n회 반영 · HH:MM」 · 「자동 저장 · HH:MM」 · 프롬프트 바 현재 시각은 **남아 있다**(MF-9 의 경계)
  - [ ] AI 탭을 안 보고 있어도 탭 라벨 옆 미확인 점이 켜지고, 열면 꺼진다(기존 동작 유지)
  - [ ] **정적 검사**: `features/meetings` 안에서 줄 행이 `createdAt` 을 포맷하는 코드 0건(grep `formatClock(line`)
  - [ ] `vitest` 전체 통과
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] `.env` 의 `MEETING_BATCH_CHARS` — 명시돼 있으면 **1000 으로 올린다**(기본값만 바꾸면 옛 값이 남는다)
- [ ] 백·프론트가 **같이 배포**돼야 한다 — `ai.batch` 프레임 모양이 바뀐다
- [ ] 리비전 없음
- [ ] 진행 중인 회의가 있으면 배포 뒤 첫 배치에서 AI 트랙이 통째로 갈린다(정상 — 사용자에게 보이는 것은 트리 교체뿐)

## Rollback

- **스키마**: 없음
- **백엔드**: revert 하면 `meeting_notes.json` 이 사라지고 `meeting_batch.json` 이 돌아온다 — **WORK-012 가 들어간 뒤에는 되돌리지 않는다**(012 가 같은 파일을 읽는다)
- **프론트**: `ai.batch` 프레임 모양이 짝이라 **백엔드와 함께** 되돌린다
- 부분 revert 시: Phase 3·4(프론트)만 되돌리면 화면이 옛 병합으로 돌아가 **AI 탭이 중복 표시**된다 — 백엔드가 전체를 보내는데 화면이 붙이기 때문이다. **프론트만 되돌리지 않는다**

## Done Criteria

- [x] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다 — 커밋 `f70a094` · 검수 `orchestration/work/docs-v1/work011-review-report.md`(FAIL 0 · WARN 4 → WORK-012)
- [ ] **SPEC-007 §6 AC 8항목**(1000자 배치 1회 + 서버 로그에 입력이 발화뿐 + 워커가 `list_agendas`·`get_agenda` 를 부른 흔적 / 트리 통째 교체 / 스키마 위반 시 직전 결과 유지 / `/결` 좁힘 / `/api …` 본문 / 줄 시각 없음 / 강등 / AI 안건이 회의록 탭에 안 나옴)이 **실측 캡처로** 완료 증거에 있다 — **미완: 앱 창 실측은 사용자(09-08 아침)**. REST·테스트 층은 검수로 확인
- [x] BE §12 **6 · 7 · 7-a** 테스트가 있다
- [x] 정적 검사 4종(프롬프트 컨텍스트 키 0 · `taskWhitelist` 0 · 스키마 파일 하나 · 줄 `createdAt` 포맷 0)
- [x] `make test` 611 · `vitest` 315 · tsc 0
- [x] `30-work/README.md` 갱신

## Open Issues

- **`ai-prompt-draft.md` §B 와 MF-53 의 어긋남 — 계약이 이긴다.** 초안 §B 는 「새로 드러난 것만 낸다 · 앞서 낸 줄은 그대로 두고 건드리지 않는다」로 적혀 있는데, **MF-53 · SPEC-007 §4 「배치 입력」은 「이번 구간을 반영해 AI 트랙 전체를 다시 정리해라」**다. **§B 에서 가져오는 것은 「조회 순서」 절이고, 요청 문장은 계약을 따른다.** 새 결정이 아니다(초안 < 계약 < `Meeting flow.md`)
- **`ai-prompt-draft.md` §A 의 「통합본」 어휘** — MF-56 으로 통합 단계가 없어졌다. WORK-010 이 웜스타트 프롬프트에서 「최종 회의록」으로 쓴다. 이 work 의 배치 프롬프트에도 「통합」이라는 말을 쓰지 않는다
- **`payload` 필드가 스키마에 있는데 회의 중에는 항상 버려진다** — MF-52 의 「스키마 한 벌」이 그런 모양이다. 스키마에서 빼면 최종(WORK-012)이 다른 파일을 갖게 된다
- OQ-10 · 11 · 12 는 **SPEC 대로**다 — 이 work 에 걸리는 것은 없다(전부 최종·유형 쪽)

## Related

- SPEC: SPEC-007 U-2 · U-3 · U-4 · §4 · §5 · §6 · DEC-003 §4 · §7 · §8
- Architecture: `backend/README.md` §5-1(AI 증분 push) · §5-2 · §7 · §8-3 · §12 6 · 7 · 7-a · `frontend/README.md` §8 · §2 규칙 7 · `database/domains/meeting.md` M-6 · M-6-a · M-7 · M-11 · M-15 · M-16
- 프롬프트 초안: `reference/2026-09-06-task-management-app/ai-prompt-draft.md` §B(조회 순서)
- Work: WORK-009 · WORK-010(선행) · WORK-012 · WORK-013(소비)
