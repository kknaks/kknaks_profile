---
type: review
work: WORK-011
title: "WORK-011 검수 — 배치 입력은 발화뿐 · 스키마 한 벌 · AI 트랙 전량 교체 · 슬래시 5 · 줄 시각 제거"
reviewer: reviewer
date: 2026-09-07
scope: "미커밋 변경 28 파일(back 15 · front 12 · .env.example) + ai_schemas rename"
worktree: /Users/kknaks/orca/workspaces/task_management/docs-v1 (kknaksss/docs-v1 · HEAD 329fda6)
verdict: "FAIL 0 · WARN 4 · 문서 공백 4"
---

# WORK-011 검수 리포트

**FAIL 0 · WARN 4 · 문서 공백 4.**
`tauri.conf.json` 은 범위 밖이라 보지 않았다. 테스트는 돌리지 않았다(코디 실측 — back 611 · front tsc 0 · vitest 315). 앱 창 실측(SPEC-007 §6 AC 8항목)은 아침 항목이라 요구하지 않았다.

## 0. 축별 판정 한 줄

| 축 | 판정 | 한 줄 |
|---|---|---|
| 2-1 배치 입력에 컨텍스트 0 | **PASS** | `_BatchInput` 필드 셋 · `_load_input` 이 커서·블록만 · 프롬프트에 컨텍스트 키 0 · 조회 순서 세 단계가 그 순서로 · 「새로 드러난 것만」은 「그게 아니다」라는 주석에만 있다 |
| 2-2 검증 순서 0~5 · 전량 교체는 검증 뒤 | **PASS** | SPEC-007 §4 표 여섯 행이 코드 순서와 1:1. DELETE 는 `_persist` **한 자리**뿐이고 정적 테스트가 잠근다. 미러/신설 규칙도 맞다 |
| 2-3 스키마 한 벌 · WS 프레임 | **PASS** | `meeting_notes.json` 모양이 WP 그대로 · `meeting_batch.json` 없음 · `ai.batch` 중첩 · 상세와 **같은 직렬화 함수**(`build_tracks`) |
| 2-4 과도기 · 012 범위 | **PASS · WARN 3** | 지운 것 0 · `finalize`/`merge` diff 0 · WORK-010 diff 0 · WORK-010 검수 WARN 넷 전부 정리됐다. 최종 프롬프트 두 문장이 새 스키마로 바뀌었고(불가피) 죽은 함수·`NotImplementedError` 가 남았다 |
| 2-5 프론트 | **PASS** | 슬래시 5 · `applyPick` 한 자리 · 명령어 문자열이 서버로 0 · `mergeAiBatch` 통째 교체 · `orphaned` 0 · 줄 시각 0 · 안건 시각 유지 · 013/014 침범 0 |
| 2-6 테스트 | **PASS · WARN 1** | Phase 1~4 검증을 사실상 전부 덮고 BE §12 6·7·7-a 가 문장대로 있다. 999/1000 경계도 있다. 「같은 직렬화 함수」만 정적 검사가 아니라 행동 검사다 |

---

## 1. FAIL

**없다.** 브리프가 지목한 FAIL 조건 일곱을 전부 확인했다 — 배치 입력 컨텍스트 0 · 검증 전 DELETE 0 · 부분 파싱 0 · 스키마 모양 일치 · 명령어 문자열이 서버로 0 · 두 번째 트리 0 · 012 범위 삭제 0.

---

## 2. PASS — 무엇을 확인했나

### 2-1. 배치 입력 (MF-50 · SPEC-007 §4 「배치 입력」)

| 검사 | 결과 |
|---|---|
| ① `_BatchInput` 필드 | `meeting_batch_service.py:207-217` — **`meeting` · `seq` · `blocks` 셋뿐.** `human_agendas`·`human_lines`·`ai_agendas`·`tasks`·`whitelist` 프로퍼티 전부 사라졌다. 최종 배치용 값은 **새 `_FinalInput`(`:220`)** 으로 갈라 나갔다 |
| ① `_load_input` | `:382-397` — `list_agendas_by_track` · `list_human_lines_since` · `list_meeting_context` 호출 **0건**. 커서(`next_seq`)와 `list_after` 블록만. 정적 테스트 `test_meeting_batch.py:692` 가 함수 본문을 잘라 세 needle 을 검사한다 |
| ② 프롬프트 컨텍스트 | `_BATCH_INSTRUCTIONS`(`:927`) **635자** 고정 + 발화 JSON. 직접 파싱해서 셌다 — `humanAgendas` **0** · `humanLines` **0** · `aiAgendas` **0** · `taskWhitelist` **0** · `newTitle` **0** · `aiAgendaId` **0** · `items` **0** · 「통합」 **0**(MF-56). `build_batch_prompt`(`:948`)가 싣는 것은 `speakerLabel`·`atMs`·`endMs`·`content` 넷뿐이다(블록 `id` 도 뺐다) |
| ② 테스트 | `test_meeting_batch.py:214`(컨텍스트 키 0) · `:235`(안건 제목·업무 제목이 프롬프트에 새지 않는다 — 실제 데이터를 만들어 놓고 본다) |
| ③ 조회 순서 | 인덱스로 확인 — `list_agendas`(201) < `get_agenda`(265) < `list_tasks`(339) < `get_task`(356) < `list_work_types`(378). 「업무를 가리킬 때만」 조건도 3단계에 붙어 있다. 테스트 `:259` |
| ③ 요청 문장 | 「**이번 구간을 반영해 AI 트랙 전체를 다시 정리해라.**」 + 「앞 배치에서 낸 안건과 줄도 포함해서 처음부터 다시 낸다」 — MF-53 · SPEC-007 §4 그대로 |
| ③ 초안 §B 의 「새로 드러난 것만」 | 소스에 1건 있으나 **`:926` 주석의 「초안 §B 의 「새로 드러난 것만」이 아니다」**다. 프롬프트 문자열에는 0건 |

### 2-2. 검증 순서 0~5 (SPEC-007 §4 표 · M-7 · M-15 · M-16)

SPEC 표 여섯 행과 코드가 1:1이다.

| # | SPEC | 코드 | 확인 |
|---|---|---|---|
| 0 | `ai_session_id` 없으면 **제출하지 않는다** · 화면 표시 없음 | `:293-295` `logger.info(...)` + `return` | **`RuntimeError` 가 아니다** — WORK-010 까지 남아 있던 전파가 조용한 미제출로 바뀌었다. 토큰 없음도 같은 모양(`:297-299` warning + return). 테스트 `:182`(제출 0 · `meeting_batch_run` 행 0) |
| 1 | 워커 오류 · 120초 → `failed` · 구간 다음으로 | 기존 `except (AgentRunFailed, AgentRunTimeout)` 그대로 | 테스트 `:453` |
| 2 | 스키마 위반 → `discarded` · 행 0 · **AI 트랙 직전 그대로** | `_parse_output`(`:531`) → `_SchemaViolation` | **부분 파싱 0** — 스키마 검증 → `humanAgendaId` 소속 → evidence 범위 순으로 돌고 어느 하나라도 어긋나면 전체가 예외다. `humanAgendaId` 는 **③ 직전에 조회한** 사람 안건 집합으로 본다(`:324-330`) — 입력에 안건을 안 실으므로 검사 시점 조회다. AI 안건 id 참조 갈래 **삭제**됨. 테스트 `:280` · `:320` |
| 3 | 업무 참조 **검사 시점 조회** → 그 줄만 `action` 강등 · `taskId` 떼기 · 본문 유지 | `:352-366` 이 `task_repository.list_meeting_context` 로 집합을 만들고 `_demote_if_needed`(`:595`)에 넘긴다 | 인자에서 `whitelist` 가 사라졌다. 테스트 `:341`(본문·상세·근거 유지) · **`:377`(제출 뒤 만든 업무는 강등되지 않는다)** — 이 항목이 「검사 시점」의 실증이다 |
| 4 | 회의 중 `payload`·`headline`·`termCorrections` **버림** | `_OutputLine`(`:235`)에 `payload` 자리가 **없다**. `_parse_output` 이 `headline`·`termCorrections` 를 읽지 않는다 | 폐기 사유가 아니다(스키마 `required` 라 오기만 하면 통과). 테스트 `:401` 이 컬럼 `NULL` 을 본다 |
| 5 | **전량 교체** 한 트랜잭션 · `seq` 증가 → 커밋 후 push | `_persist`(`:626`)가 `delete_by_track` → `delete_agendas_by_track` → INSERT 를 **한 함수 안에서** | `_run_once` `:366-378` 이 `session_scope` 안에서 `_persist` + `create_run`, 그 **밖에서** `push_ai_batch` |

**검증 전 DELETE 0** — `delete_by_track` · `delete_agendas_by_track` 의 프로덕션 호출은 `meeting_batch_service.py:643` · `:646`(둘 다 `_persist` 안) **각 1건뿐**이다. `test_meeting_batch.py:677` 이 함수 본문을 잘라 「소스 전체에 1건 · `_persist` 안에 1건」을 잠근다. `_run_final_once` 도 자기가 하던 DELETE 를 걷고 `_persist` 를 부르도록 통일됐다(동작 동일).

**미러 안건** — `_persist` 가 `human_titles.get(...)` 로 **사람 안건 제목을 복사**하고 `source_agenda_id=agenda.human_agenda_id`, 신설은 `None`, `state` 는 언제나 `None`. 테스트 `:577`.

**전량 교체 실증** — `:515`(두 번째 배치가 첫 배치 id 를 남기지 않는다) · `:548`(두 번째가 검증에 떨어지면 첫 배치 것이 그대로) — BE §12 **7-a** 문장 그대로.

### 2-3. 스키마 한 벌 · WS 프레임 (MF-52 · SPEC-007 §4)

- `ai_schemas/` 에 **`meeting_notes.json` · `meeting_integration.json` 둘**. `meeting_batch.json` **없다**(git rename). `meeting_integration.json` 은 WORK-012 가 지운다 — 정상. 테스트 `:701`
- 모양이 WP 그대로다 — 최상위 `{headline, termCorrections, agendas}` `required` 셋 · 안건 `{humanAgendaId, title, lines}` · 줄 `{kind, content, detail, evidence, taskId, payload}`. `headline`·`termCorrections`·`payload` 가 nullable. **`aiAgendaId`·`newTitle`·`items` 없음.** 전 레벨 `additionalProperties: false`
- `AiBatchFrame`(`dto/meeting_stream.py`) · `AiBatchMessage`(`schemas/meeting_stream.py`) 에서 최상위 `lines` 키가 **삭제**됐고 `agendas: list[AgendaItem]` 만 남았다. `push_ai_batch(meeting_id, *, seq, agendas)` 인자도 하나
- **같은 직렬화 함수** — `_persist` 가 `meeting_service.build_tracks(rows, lines).ai`(`:692`)를 돌려주고, 상세 응답도 `meeting_service.py:198` 이 같은 `_build_tracks`(별칭 `build_tracks = _build_tracks`, `:281`)를 지난다. 프레임 → `AgendaItem.from_dto` 로 상세와 같은 스키마 클래스. 테스트 `:603` 이 push 된 줄과 `GET` 상세의 `agendas.ai[0].lines` 를 **직접 대조**한다

### 2-4. 과도기 · 012 범위

| 검사 | 결과 |
|---|---|
| `run_final` · `_load_final_input` · `build_final_prompt` · `_agenda_rows` | **전부 남아 있다.** `_agenda_rows`(`:774`)는 `build_final_prompt`(`:905`)가 아직 쓴다 — WP Open Issues 의 「마지막 호출자를 지우는 WORK-012 가 폐기한다」 그대로 |
| `meeting_finalize_service.py` · `meeting_merge_service.py` | **diff 0** |
| `build_warm_start_prompt` · `launch_warm_start` · `_warm_start_once`(WORK-010) | **diff 0** |
| WORK-010 검수 WARN 넷 | **전부 정리됐다** — ① `reset_state()` 가 `_tasks` 를 cancel·clear 한다(W-1) ② `test_meeting_live_api.py:88` 이 `live_scope` + 직접 `start()` + 훅으로 **순서를 증명**하도록 다시 쓰였다(W-2) ③ 죽은 import `FakeAgentGateway` 제거·`WARM_SESSION_ID` 는 실사용(W-3) ④ 프롬프트 needle 이 `_prompt_without_tool_names()` 로 bare 검사가 되고 `task`·`agendaId` 가 추가됐다(W-5) |
| `_run_final_once` 의 세션 없음 | 여전히 `RuntimeError` — **맞다.** 회의 중은 「미제출」이고 종료 후는 ② `final_failed` 로 가야 한다(DEC-003 §7 · MF-70). 같은 파일에 두 갈래가 있는 것이 의도다 |

### 2-5. 프론트 (MF-9 · 10 · 53 · SPEC-007 U-2 · U-3 · U-4)

| 검사 | 결과 |
|---|---|
| ① 슬래시 5개뿐 | `commandItems`(`PromptBar.tsx:88`)가 `buildPopoverItems("full", activeAgenda, [])` — **팝오버 목록 그대로**다. 이동 행은 `otherAgendas=[]` 로도 빠지고 `commandLabel`(`LineKindPopover.tsx:47`)이 `null` 을 주어 두 번 막힌다. 명령어 문자열을 손으로 적은 곳 0(정적 `static.test.ts` ㉑) |
| ① 스페이스에서 칩 | `onChange` — `spaceAt > 0` 이고 앞 토큰이 명령어면 `applyPick(command, value.slice(spaceAt+1))`. 명령어 문자열이 사라지고 뒤가 본문이 된다 |
| ① 백스페이스 복귀 | `onKeyDown` — 빈 입력 `Backspace` 에서 `setDraft(\`/${LINE_KIND_LABEL[lineKind]}\`)` · `/새안건`. 브라우저가 한 글자 더 갉지 않게 `preventDefault` |
| ① 그 밖 `/…` 는 본문 | 토큰이 안 맞으면 **그대로 `setDraft(value)`** — 갈래·이스케이프 없음. `/` 뒤 좁힘에서 남는 항목이 0이면 팝오버를 닫는다(`/api` · `/ㅁㄴㅇㄹ`) |
| ① 안건 없음 | `buildPopoverItems` 가 `activeAgenda` 없으면 line-kind 넷을 안 넣는다 → 팝오버·명령어 둘 다 「새 안건」만. 테스트 `PromptBar.test.tsx:239` |
| ① 안건 이동은 팝오버만 | 테스트 `:193`(`/안건 ` · `/이동 ` 은 본문 · `onActivateAgenda` 0건) |
| ① `applyPick` 한 자리 | 팝오버 `pick`(비-move)과 명령어가 **같은 함수**(`:120`)로 끝난다. 테스트 `:217` 이 「DOM 상 같다 · 같은 요청 본문」을 본다 |
| ② 서버 body | `onSendLine(lineKind ?? "discussion", text)` — `kind`·`content` 둘뿐. 명령어 문자열은 `draft` 에서 이미 떨어졌다. `MeetingLiveView.test.tsx` 의 MSW 단언이 「본문에 `/결정` 0건」을 본다 |
| ③ `mergeAiBatch` | `aiBatch.ts:14` — `agendas.ai = frame.agendas` **통째 교체**. `orphaned` 개념·재조회 갈래 삭제(`useMeetingStream.ts` `case "ai.batch"`). `latestBatchSeq` 는 `max` 유지(늦은 낮은 회차가 회차를 내리지 않는다). 프레임 배열을 복사해 캐시가 프레임 객체를 붙들지 않는다. 테스트 `aiBatch.test.ts` 3건 + `MeetingLiveView` 의 「펼침 접힘 · 미확인 점」 |
| ④ 줄 시각 | `LineRow.tsx` 에서 `formatClock(line.createdAt)` 블록과 `formatClock` import 삭제. `formatClock(line` **0건**(정적 ㉑). 안건 헤더 시각은 `AgendaLineTree.tsx:94` 에 **남아 있고** 정적 테스트가 그것을 반대 방향으로 잠근다. 안내 바·프롬프트 바 시각도 유지 |
| ⑤ 금지 목록 | 두 번째 트리 0(기존 정적 ⑮) · `fetch(` 직접 0(신규 ㉑) · 인라인 hex 0(수정 파일의 hex 넷은 전부 문서 주석 안 — `stripComments` 뒤 0) · `Sheet`/`Dialog` 직접 import 0(기존 ①) |
| ⑥ 013/014 침범 | 수정 파일은 `PromptBar` · `LineKindPopover` · `LineRow` · `aiBatch` · `useMeetingStream` · `types` + 테스트뿐. `LineRow` 변경은 시각 삭제 하나이고 `LineKindSelector` 는 그대로 남아 있다(013 이 걷는다). breadcrumb · 헤더 · 드로어 파일 diff 0 |

---

## 3. WARN

### W-1. `build_final_prompt` 의 본문이 새 스키마로 바뀌었다 — 「컴파일만 되게」를 넘는다

- **자리**: `meeting_batch_service.py:888-920` — 「줄은 반드시 안건 하나에 붙인다 … `newTitle` … **`aiAgendaId` 는 쓰지 마라**」 두 문장이 「안건은 … `humanAgendaId` 에 그 id 를 … 줄은 그 안건의 `lines` 안에 넣는다」로 교체됐다.
- **어긋난 문서**: WP §Internal Interface 「과도기 규칙」 — 「`_BatchInput` 이 줄었으므로 그 셋이 필요로 하던 값은 함수 안에서 직접 조회하도록 **최소 수정**한다 — 「빌드는 되고 동작은 옛것」 상태로 남긴다」
- **판단: 불가피했고 올바른 선택이다.** `OUTPUT_SCHEMA` 가 **한 벌**이라 최종 배치도 새 스키마로 강제된다. 옛 문장을 그대로 뒀다면 codex 가 `items`/`newTitle` 을 내려 하고 스키마가 막아 **최종 배치가 100% `discarded`** 가 됐을 것이다. 실제로 `test_meeting_finalize.py` 의 ① 관련 테스트들이 새 모양(`notes_output`)으로 통과한다.
- **왜 기록하나**: WORK-012 가 물려받는 것은 「옛것 그대로」가 아니라 **부분 이관된** 최종 경로다 — 스키마·`_parse_output`·`_demote_if_needed`·`_persist` 는 이미 새것이고, 남은 옛것은 **입력 컨텍스트(`_FinalInput` 의 `human_agendas`·`human_lines`·`tasks`)와 프롬프트 본문**뿐이다. WORK-012 브리프가 이 전제로 서야 한다.

### W-2. `find_ai_agenda_by_source` 가 죽은 함수가 됐다

- **자리**: `app/back/repository/meeting_child_repository.py:144`
- 유일한 호출자였던 `_persist` 의 「미러 안건이 이미 있으면 재사용」 분기가 전량 교체로 사라졌다. 전수 grep 결과 **정의 1 · 호출 0**(테스트 포함).
- WP §Code Surface 는 `_persist` 에서 「`ai_agenda_id` 분기 · `created_by_title` 분기 삭제」만 적었고 이 repository 함수는 언급하지 않았다. `_agenda_rows` 는 Open Issues 가 폐기 시점을 WORK-012 로 못 박았는데 이쪽은 어느 문서에도 없다(→ D-4).

### W-3. `_parse_output(fill_final=True)` 가 `NotImplementedError` 를 던진다

- **자리**: `meeting_batch_service.py:557-559`
- WP §Dependency 는 「이 work 가 그 함수들을 **`fill_final: bool` 스위치를 받을 수 있는 모양**으로 남긴다」고 했다. 지금은 「받을 수 있는 모양」이라기보다 **받으면 터지는 모양**이다.
- 오늘 아무도 `True` 로 부르지 않아 동작에는 문제가 없고, 조용한 기본값보다 낫다(BE §8-1 의 결). 다만 프로덕션 모듈에 남는 지뢰이므로 WORK-012 의 첫 항목으로 세워 두어야 한다.

### W-4. 테스트 공백 — 「같은 직렬화 함수」가 정적 검사가 아니다

- WP Phase 2 검증 — 「`ai.batch` 프레임의 `agendas[].lines[]` 가 상세 응답 `agendas.ai` 와 같은 모양이다(**같은 직렬화 함수를 지난다는 정적 검사**)」
- 실제로 있는 것은 `test_meeting_batch.py:603` 의 **행동 검사**다(push 된 줄과 `GET` 상세의 `agendas.ai[0].lines` 를 대조 + `not hasattr(frame, "lines")`). 두 경로가 `build_tracks` 를 지난다는 **구조 검사**는 없다.
- 행동 검사가 더 강한 면도 있지만, 나중에 누가 push 쪽에 별도 직렬화를 끼워 넣고 그 테스트의 한 케이스만 맞춰 두면 통과한다. 다른 정적 검사 셋(`_persist` 단일 DELETE · `_load_input` needle · 스키마 파일 하나)은 다 들어갔는데 이것만 빠졌다.

---

## 4. 문서 공백

| # | 자리 | 무엇이 비었나 |
|---|---|---|
| **D-1** | WP §Dependency 「`fill_final: bool` 스위치」 | `True` 일 때 **무엇을 어디에 채우는지**가 WORK-011 에도 없고 WORK-012 WP 에도 아직 없다 — `headline`·`termCorrections` 는 `_OutputAgenda` 밖의 값이라 반환 형태 자체가 달라져야 하는데 그 모양이 정해져 있지 않다. WORK-012 브리프가 먼저 정할 자리(W-3 의 뿌리) |
| **D-2** | `reference/2026-09-06-task-management-app/ai-prompt-draft.md` §B (L180 · L208~209) | 「여기서 **새로 드러난 것만** 추가할 줄로 낸다. 앞서 낸 줄은 그대로 두고 건드리지 않는다」가 **그대로 남아 있다.** WP Open Issues 가 「계약이 이긴다」로 닫았고 코드는 계약을 따랐지만, 초안 파일에는 정정 표시가 없다 — 다음에 §B 를 읽는 사람이 같은 함정을 밟는다. 최종 프롬프트를 쓰는 WORK-012 가 바로 그 다음 독자다 |
| **D-3** | SPEC-007 U-3 「안건 없음」 절 | 「나머지 넷은 그대로 텍스트」라고만 하고, 그때 **팝오버가 어떻게 되는지**(`/논` 처럼 좁혀서 남는 항목이 0이면 닫는다)가 없다. 코드가 정한 동작은 합리적이나 문서에 근거가 없다 |
| **D-4** | WP §Code Surface / Open Issues | 「마지막 호출자가 사라진 repository 함수」의 폐기 시점 규약이 없다. `_agenda_rows` 는 Open Issues 가 WORK-012 로 못 박았는데 `find_ai_agenda_by_source` 는 어느 문서에도 없다(W-2 의 뿌리) |

---

## 5. WP 검증 항목 ↔ 테스트 대응표

**Phase 1 — 스키마 한 벌 · 배치 입력 · 검증 순서**

| WP 검증 항목 | 테스트 |
|---|---|
| 프롬프트에 `humanAgendas`·`humanLines`·`aiAgendas`·`taskWhitelist` 0 · `transcript` 만 | `test_meeting_batch.py:214` · `:235`(실제 안건·업무를 만들어 놓고 제목이 새는지 본다) |
| 조회 순서 세 단계가 그 순서로 | `:259` |
| 스키마 파일이 하나 | `:701` |
| **BE §12 6** — 잘못된 JSON → 줄 0 · 구간 다음 배치로 | `:280` · `:320`(AI 안건 id 를 `humanAgendaId` 에 넣으면 위반) |
| **BE §12 7** — 프로젝트 밖 `taskId` → `action` 강등 · 본문 유지 | `:341` |
| 〃 회의 중 `payload`·`headline`·`termCorrections` 미저장 | `:401` |
| `taskId` 검사가 **검사 시점 조회** | `:377`(제출 뒤 만든 업무는 강등되지 않는다) |
| (추가) `kind≠task` 인 줄의 `taskId` 는 사유 로그와 함께 뗀다 | `:426` |
| 검증 0 — 세션 없으면 조용히 미제출 | `:182` |
| 트리거 **999/1000 경계** | `:88`(999 는 안 돌고 1000 에서 돈다 · 타이머 무장/해제까지) · `:112`(전환 79/80) · `:126`(타이머) · `:139`(동시 실행 0 · 구간 합침) |

**Phase 2 — 전량 교체 · WS**

| WP 검증 항목 | 테스트 |
|---|---|
| **BE §12 7-a** — 두 번째 배치가 첫 배치 id 를 남기지 않는다 | `:515` |
| 〃 두 번째가 떨어지면 첫 배치 것이 그대로 | `:548` |
| 검증 실패 경로에서 DELETE 0 | `:548` + 정적 `:677` |
| `ai.batch` 가 상세 `agendas.ai` 와 같은 모양 | `:603` — **행동 검사만**(W-4) |
| 미러 `source_agenda_id` + 제목 복사 · 신설 `NULL` | `:577` |
| AI 는 사람 트랙에 안 쓴다(M-6) | `:650` |

**Phase 3 — 슬래시 · 팝오버**

| WP 검증 항목 | 테스트 |
|---|---|
| `/결` 좁힘 · `/새` 좁힘 · 이동 행 빠짐 | `PromptBar.test.tsx:144` |
| `/결정 ` → 칩 · `Enter` → `kind:'decision'` · 백스페이스 복귀 | `:158` |
| `/api …` · `/ㅁㄴㅇㄹ …` · `/논의 /api` → 본문 | `:179` |
| 안건 이동이 슬래시로 안 된다 | `:193` |
| `/새안건 <제목>` → `onCreateAgenda` · 줄 전송 0 | `:205` · `MeetingLiveView`(두 요청 순서) |
| 팝오버 상태 = 명령어 상태(DOM · 요청 본문) | `:217` |
| 안건 없음 → `/새안건` 만 | `:239` |

**Phase 4 — 통째 교체 · 줄 시각**

| WP 검증 항목 | 테스트 |
|---|---|
| 두 번째 `ai.batch` → 트리 통째 교체 · 펼침 접힘 | `aiBatch.test.ts:44` · `MeetingLiveView.test.tsx` |
| 빈 트리 · 낮은 seq · 배열 복사 | `aiBatch.test.ts:67` · `:74` |
| 줄 시각 0 · 안건/안내 바 시각 유지 | `MeetingLiveView.test.tsx` + 정적 `static.test.ts` ㉑ 2건 |
| 미확인 점 켜짐/꺼짐 | `MeetingLiveView.test.tsx` |
| 정적 — `formatClock(line` 0 · `orphaned` 0 · 명령어 원천 하나 · `fetch(` 0 | `static.test.ts` ㉑ |

**빠진 것** — SPEC-007 §6 AC 8항목의 **실측 캡처**(워커 로그의 `list_agendas`·`get_agenda` 호출 흔적 포함)와 WP Phase 1~4 `완료 증거`. 코디가 아침 항목으로 잡았으므로 여기서는 세지 않았다.

---

## 6. 요약

**핵심 네 가지가 전부 문서대로 섰다.** 배치 입력이 `meeting`·`seq`·`blocks` 셋으로 줄었고 프롬프트에 컨텍스트 키가 0이다. 검증 순서 0~5가 SPEC-007 §4 표와 1:1이고, DELETE 를 부르는 곳이 `_persist` 한 자리뿐이라 「검증 뒤에만 지운다」(M-7)가 구조로 지켜진다. 스키마가 한 벌로 합쳐졌고 `ai.batch` 가 상세 응답과 **같은 `build_tracks`** 를 지난다. 프론트는 슬래시 5개와 팝오버가 `applyPick` 한 자리에서 만나고, 명령어 문자열이 서버로 나가지 않으며, 줄 시각이 사라지고 안건 시각은 남았다.

**범위도 지켜졌다** — `run_final` 계열과 `_agenda_rows` 를 지우지 않았고 `meeting_finalize_service`·`meeting_merge_service`·WORK-010 웜스타트는 diff 0이며, 013/014 파일에 손대지 않았다. **WORK-010 검수 WARN 넷도 전부 정리됐다.**

남은 넷은 전부 다음 WP 로 넘어갈 성격이다 — ① **W-1** 최종 경로가 「옛것 그대로」가 아니라 부분 이관됐다(WORK-012 브리프의 전제가 바뀐다) ② **W-3** `fill_final=True` 가 `NotImplementedError` 이고 그 스위치가 무엇을 채울지 문서에 없다(D-1) ③ **W-2** 죽은 repository 함수 하나 ④ **W-4** 「같은 직렬화 함수」 정적 검사 하나. 커밋을 막을 무게는 없다.
