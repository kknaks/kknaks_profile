---
type: work
id: WORK-012
title: "회의 종료 — async 재전사 → 최종 회의록 한 번 · 용어 보정 · payload"
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
  specs: [SPEC-008]
  works: [WORK-008, WORK-009, WORK-011]
  releases: []
  related: [SPEC-006, SPEC-007, WORK-010, WORK-013]
---

# 회의 종료 — async 재전사 → 최종 회의록 한 번 · 용어 보정 · `payload`

**종료 파이프라인이 셋에서 둘로 줄고, codex 호출이 둘에서 하나가 된다.** 지금은 「최종 배치 → 통합 호출」이고 재전사가 없다. 이 work 가 끝나면 **① async 재전사(Soniox `stt-async-v5`) → ② 최종 회의록 호출 한 번**이고, ② 가 `merged` 트랙 · `ai_headline` · `term_corrections` · 트랜스크립트 용어 치환을 **한 트랜잭션**으로 남긴다. **① 에 fallback 이 없다** — 실패하면 실시간 블록 그대로 `ended`+`failed` 다.

> 1 파일 = 1 work = **빌드 계획**. dev 가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC 의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs` 와 index 에서 연결한다.
> **결정 원본은 `reference/2026-09-06-task-management-app/Meeting flow.md`** — **MF-37 · 52 · 54 · 56 · 57 · 58 · 59 · 70**. 계약과 부딪히면 그쪽이 이긴다.

## Meta

- Baseline: BASE-003 #7(근거) · #8(종료 후 회의록) · L43(가리지 않는다)
- Covers spec
  - **SPEC-008 U-1**(생성중 — 단계 문구 둘 · 편집 잠금 · 폴링 실패 「다시 확인」) · **U-2**(실패 배너 · 「다시 시도」)
  - **SPEC-008 §4 API Contract 표**(`POST /end` · `GET /api/jobs/{jobId}` · **`POST /finalize`**) · **§4 Request/Response 의 `/end` · `/jobs` · `/finalize` · `MeetingDetail`(`mergedSummary` 다섯 · `activeJobId`)** · **§4 「수치」 표 전부** · **§4 「종료 파이프라인 — 검증 가능한 정의」 표 ①②** · **「② 의 `context`」 표** · **「② 출력의 최종 전용 필드」** · **「서버 검증」 표 8행** · **§4 Case Matrix 의 ①·② 실패 6행** · **§4 Validation 의 `/end`·`/finalize`·「② 출력(서버 재검증)」 행**
  - **SPEC-008 §5 구현 규칙** — 「① 실패에 fallback 코드를 두지 않는다」 · 「② 는 회의 중 배치와 같은 스키마 파일 · 같은 검증 함수를 쓴다」 · 「AI 트랙은 종료 후 손대지 않는다」 · 「외부 호출 중 트랜잭션을 열지 않는다」
  - **DEC-003 §4**(종료 파이프라인) · **§6**(보관) · **§7**(실패 정책) · **§STT**(재전사 · 용어 보정)
  - **ERD M-8 · M-8-a · M-9-a · M-9-b · M-19** · **BE §6**(비동기 API 규약) · **§5-3**(기동 스윕) · **§12 테스트 8**
- Depends on work: **WORK-011**(`ai_schemas/meeting_notes.json` · `_parse_output` · `_demote_if_needed` · `_persist` 를 011 이 만든다 — ② 가 **같은 것**을 쓴다) · **WORK-009**(`revoke_meeting_token()` · 옵션 빌더) · WORK-008(현행 종료 구현)
- Parallel work: 없음 — **코드 워커는 한 번에 하나**
- Follow-up work: **WORK-013**(편집 · payload 드로어 — 이 work 의 리비전 `0008` 이 `payload` 컬럼을 만든다)
- **External dependency**
  - **Soniox async API** — `POST /v1/files` → `POST /v1/transcriptions`(`model: stt-async-v5`) → 5초 폴링 → `GET /v1/transcriptions/{id}/transcript`. 키는 실시간과 **같은 `SONIOX_API_KEY`**(`integrations/soniox.py` 가 읽는 유일한 코드)
  - **실물 확인 1건(SYS-OQ-5)** — **헤더 없는 webm 을 `stt-async-v5` 가 받나.** 녹음 원본이 스트림 append 라 컨테이너 헤더가 온전하지 않을 수 있다. **Phase 1 안에서 파일 하나(≈$0.10)로 확인**하고 결과를 완료 증거에 적는다
  - open-kknaks 워커 · MCP · 토큰은 WORK-009

## Work Summary

| Field | Value |
|---|---|
| Type | refactor |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR | `kknaksss/docs-v1` |
| Blocker | 없음 — SYS-OQ-5 는 Phase 1 안에서 푼다 |
| Next | Phase 0 — 리비전 `0008` |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | SPEC-008 §6 AC 의 종료·재전사·실패 관련 12항목 대조 | todo |
| Design |  | 해당 없음 — 생성중·실패 화면은 디자인 시스템 조립(U-1 · U-2 규격이 정본) | — |
| FE |  | Phase 3 | todo |
| BE |  | Phase 0~2 | todo |
| QA |  | ① fallback 0건 · codex 호출 종료 후 **한 번** · `auto` 치환 · `guess` 미치환 · 화자 라벨 불변 · 상한 마감 · 토큰 폐기 | todo |
| Ops |  | 신규 env 없음(수치는 기본값). `SONIOX_API_KEY` 가 async 도 쓴다는 것만 확인 | todo |

## Scope

포함:

- **리비전 `0008`** — `pending_change` → `payload`(이름 변경 + CHECK) · `source_human_line_id`·`source_ai_line_id` + 부분 UNIQUE 2 + CHECK **삭제** · `meeting.term_corrections jsonb NULL` **신설** · `meeting_batch_run.phase` CHECK 에서 **`integration` 제거** · `job.error_code` CHECK **5종**으로
- **① async 재전사** — `integrations/soniox.py` 에 async 갈래 신설. 업로드 → 전사 요청(`context` 포함) → **5초 폴링** → 토큰 수신. sub-word 토큰을 **화자 변경 · 300자 · 2초 공백**으로 블록으로 묶는다(실시간과 **같은 규칙**). `meeting_transcript` **DELETE + INSERT 한 트랜잭션**. **fallback 없음**
- **② 최종 회의록 호출 한 번** — 같은 세션 `resume`. 입력은 **재전사 스크립트 전체 하나**. 출력은 **WORK-011 의 스키마 한 벌**에 `payload`·`headline`·`termCorrections` 가 채워진 것. 검증(안건 참조 전수 · 업무 참조 사후 · 페이로드 참조 · evidence 범위 · `payload.status≠done`) → `merged` INSERT + `ai_headline` + `term_corrections` + **`grade='auto'` 치환** + `ended`/`succeeded` 를 **한 트랜잭션**
- **`integrate()` → `finalize()`** · `run_pipeline` = ① → ② **한 번**(`final_batch` 스위치 폐기 · `resume` 여부는 「①부터 다시」 하나뿐)
- **`meeting_merge_service.py` 폐기** · `run_final` · `_load_final_input` · `build_final_prompt` · `_agenda_rows` · `ai_schemas/meeting_integration.json` 폐기
- **② 종결 시 `auth_service.revoke_meeting_token()`**(성공·실패 무관 · best-effort — WORK-009 가 만든 함수)
- **`/finalize` 재시도는 토큰을 새로 발급한다**(2026-09-08 코디 — 두 계약의 귀결: ② 종결이 행을 지우는데 재시도 ② 가 MCP 를 부르려면 행이 필요하고 TTL 이 분 단위라 「실패 시 안 지움」으로는 늦은 재시도가 못 산다). `finalize()` 가 `/start` 와 **같은 `auth_service.issue_meeting_token()`** 을 부른다(두 번째 발급 코드 0). 발급 전 그 회의의 `kind='meeting'` 행이 남아 있으면(폐기 best-effort 실패) 지우고 낸다 — **어느 시점에도 회의당 하나**(A-13). 테스트: 실패 → `/finalize` → 행 1 · 새 원문 · ② 가 그 원문으로 헤더
- **수치** — 재전사 상한 **1200초** · Soniox 폴링 **5초** · ② 시도당 **300초** × **3회** · job 상한 **2400초** · 프론트 폴링 **2초 · 1230회**
- **프론트** — 생성중 문구 **phase 둘**(`transcription`/`final`) · 실패 배너 「다시 시도」 → `POST /finalize` · AI 탭 안내 바 「배치 n회」 **그대로** · 한 줄 요약 바 **카운트 다섯** · 스크립트 푸터 「전체 스크립트 n분 · 화자 n명」 · 폴링 상한 1230
- 테스트 — BE §12 **8**(② 3회 실패 후 상태 · ① 실패 시 ② 로 안 감 · `merged` 0건)

제외:

- **편집 · 줄 추가/삭제 · payload 드로어 · 「넣기」 두 표면 · `work_type.description`** → **WORK-013**. 이 work 는 **컬럼만** 만든다(`payload`) — 드로어·`POST/PATCH lines` 의 `payload` 갈래는 013 이 연다
- **배치 입력·출력·스키마 파일** → WORK-011(선행). 이 work 는 **읽기만** 한다
- **웜스타트** → WORK-010
- **breadcrumb · 헤더 순서 · 미리보기 패널 · 「←」** → WORK-014
- **용어 보정 표를 보여 주는 화면** — 없다(§1 Out · API 로도 안 내보낸다)
- **재생성** — 성공한 회의록을 다시 만드는 경로를 만들지 않는다(DEC-003 §4)

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back` · `app/front`

| 경로 | 신규 / 수정 / 폐기 | 설명 |
|---|---|---|
| `app/back/alembic/versions/0008_meeting_payload_terms.py` | **신규** | `down_revision = "0007_auth_session_meeting_token"`. ① `meeting_line.pending_change` → `payload` **RENAME** + CHECK `payload IS NULL OR (track IN ('merged','human') AND kind IN ('action','task'))` ② `source_human_line_id`·`source_ai_line_id` 컬럼 · FK 2 · 부분 UNIQUE 2(`uq_meeting_line_source_human_line_id`·`uq_meeting_line_source_ai_line_id`) · CHECK `ck_meeting_line_source_only_merged` **삭제** ③ `meeting.term_corrections jsonb NULL` 추가 ④ `meeting_batch_run` phase CHECK 를 `incremental|final` 로 재작성(`integration` 행이 있으면 **삭제 후** 재작성) ⑤ `job.error_code` CHECK 를 5종으로 재작성. `downgrade` 는 역순 |
| `app/back/models/meeting.py` | 수정 | `MeetingLine.pending_change` → `payload` · `source_*_line_id` 두 컬럼과 `__table_args__` 의 CHECK·UNIQUE 2건 삭제 · `Meeting.term_corrections` 추가 |
| `app/back/models/job.py` | 수정 | `_ERROR_CODE_VALUES` 5종 |
| `app/back/dto/enums.py` | 수정 | `JobErrorCode` = `TRANSCRIPTION_FAILED` · `TRANSCRIPTION_TIMEOUT` · `FINAL_FAILED` · `FINAL_TIMEOUT` · `JOB_TIMEOUT`. `BatchPhase.INTEGRATION` **삭제**. `JobPhase` = `TRANSCRIPTION` · `FINAL`(`FINAL_BATCH`·`INTEGRATION` 삭제) |
| `app/back/integrations/soniox.py` | 수정(추가) | **async 갈래 신설** — `SttAsyncConnector` Protocol · `SonioxAsyncClient.transcribe(path, context, *, poll_sec, timeout_sec) -> list[SttToken]`(files → transcriptions → 폴링 → transcript). 실패는 `SttUpstreamError`. `install_async_connector()` 대역 지점. **실시간 갈래는 건드리지 않는다** |
| `app/back/service/meeting_transcript_blocks.py` | **신규** | **블록 묶기 한 곳** — 화자 변경 · 300자 · 2초 공백. `meeting_stream_service` 의 `_OpenBlock` 로직을 여기로 올리고 **실시간·재전사가 같은 함수를 쓴다**(SPEC-008 §4 「같은 규칙」) |
| `app/back/service/meeting_stream_service.py` | 수정(최소) | 블록 묶기를 위 모듈로 위임. 동작 변화 없음 |
| `app/back/service/meeting_finalize_service.py` | 수정(전면) | `integrate()` → **`finalize()`** · `_plans` 스위치 폐기 · `run_pipeline(job)` = ① → ② · `_transcribe()` 신규 · `_attempt_final()`(옛 `_attempt_integration`) · `_commit_success()` 가 `merged` + `ai_headline` + `term_corrections` + 치환 + 종결을 한 트랜잭션 · `_commit_failure()` 가 새 `error_code` · **종결 뒤 `auth_service.revoke_meeting_token()`** · `build_final_notes_prompt()` 신규(`build_integration_prompt` 폐기) · `_load_tree`·`_IntegrationInput` 폐기 |
| `app/back/service/meeting_merge_service.py` | **폐기** | 통합 규칙(사람 줄 전수 계승 · 이중 계승 금지 · 본문 복사)이 MF-56·57 로 사라졌다. 대체 = `meeting_batch_service._parse_output(fill_final=True)` + `meeting_finalize_service` 의 최종 검증 |
| `app/back/ai_schemas/meeting_integration.json` | **폐기** | 스키마 한 벌(`meeting_notes.json` — **WORK-011 소유**) |
| `app/back/service/meeting_batch_service.py` `run_final()` · `_run_final_once()` · `_load_final_input()` · `build_final_prompt()` · `_agenda_rows()` | **폐기** | 종료 시 배치가 없다(MF-56). `_agenda_rows` 는 **여기서 마지막 호출자가 사라진다** |
| 〃 `_parse_output()` · `_demote_if_needed()` · `_persist()` | 수정(확장) | `fill_final=True` 갈래 — `payload`·`headline`·`termCorrections` 를 **채워 돌려주고**, `_persist(track=…)` 로 `merged` 에도 쓴다. **WORK-011 이 만든 함수를 그대로 쓴다 — 복제하지 않는다** |
| `app/back/repository/meeting_transcript_repository.py` | 수정 | `delete_by_meeting()` · `bulk_create()` · `replace_content(stt→correct)` (용어 치환 — `speaker_label` 은 안 건드린다) |
| `app/back/repository/meeting_repository.py` | 수정 | `finish_integration(...)` 에 `term_corrections` 인자. 이름은 그대로(컬럼명이 `integration_state`다 — M-4) |
| `app/back/service/job_service.py` | 수정(최소) | `progress.phase` 파생 규칙 — job 이 ① 도는 동안 `transcription`, `meeting_batch_run(phase='final')` 이 생기면 `final` |
| `app/back/api/meeting_router.py` | 수정 | `POST …/integrate` → **`POST …/finalize`**(경로 문자열 · 핸들러 이름) |
| `app/back/config.py` | 수정 | `meeting_transcribe_timeout_sec = 1200` · `meeting_transcribe_poll_sec = 5` · `meeting_final_timeout_sec = 300`(옛 `meeting_integration_timeout_sec` 180 대체) · `meeting_final_attempts = 3` · `meeting_job_timeout_sec = 2400`. 옛 `meeting_final_batch_timeout_sec` · `meeting_integration_*` 폐기 |
| `app/back/schemas/meeting.py` · `dto/meeting.py` | 수정 | `pending_change` → `payload`(응답 키 `payload`) · `MergedSummary` 다섯 필드(`agendaCount`·`discussionCount`·`decisionCount`·`actionCount`·`taskCount`, **`integratedAt` 삭제**) |
| `app/back/tests/test_meeting_finalize.py` · `test_meeting_merge.py` | 수정 / **폐기** | `test_meeting_merge.py` 는 폐기(대상 모듈이 없다). `test_meeting_finalize.py` 전면 |
| `app/back/tests/fakes/` | 수정 | async STT 대역 |
| `app/front/src/features/meetings/components/MeetingStatusBar.tsx` | 수정 | `generating` 변형에 **phase 둘**(「녹음을 다시 받아쓰고 있습니다」/「회의록을 정리하고 있습니다 · 다시 시도 중 (n/2)」) · `failed` 변형 버튼 문구 「**다시 시도**」 · `headline` 변형 카운트 **다섯** |
| 〃 `hooks/useMeetingFinalizeJob.ts` | 수정 | `JOB_POLL_MAX_COUNT` 480 → **1230** · 주석 수치 · `progress.phase` 노출 |
| 〃 `api.ts` · `types.ts` | 수정 | `POST …/finalize` · `MergedSummary` 다섯 · `JobProgress.phase` 두 값 · `errorCode` 5종 |
| 〃 `components/MeetingClosedPage.tsx` | 수정 | 생성중 두 단계 · 실패 배너 「다시 시도」 · 스크립트 푸터 「전체 스크립트 n분 · 화자 n명」 |
| 〃 `components/TranscriptPanel.tsx` | 수정 | 종료 후 푸터(위) · 자동 따라가기 없음 |
| 〃 `closeFixtures.ts` · 관련 `*.test.tsx` | 수정 | 다섯 카운트 · phase 둘 |

- Domain / schema note: 리비전 **1건**(`0008`). **`payload` 컬럼은 여기서 생기고 쓰는 표면은 WORK-013 이 연다**

## Domain / Schema

| Entity | 역할 |
|---|---|
| `meeting` | `ai_headline` · **`term_corrections`(신설)** 가 ② 성공 트랜잭션에서 함께 찬다. 실패면 둘 다 `NULL` |
| `meeting_line` | `pending_change` → **`payload`**. `source_*_line_id` **없어진다** |
| `meeting_transcript` | ① 이 **전량 교체**. ② 가 `grade='auto'` 항목만 `content` 치환 |
| `meeting_agenda`·`meeting_line`(`track='merged'`) | ② 성공 트랜잭션에서 INSERT. `ai` 트랙은 **건드리지 않는다** |
| `job` | `error_code` 5종. `progress{phase, attempt}` 는 파생 |
| `auth_session(kind='meeting')` | ② 종결 뒤 **DELETE**(best-effort) |

- 상태 / invariant: **M-8**(최종은 AI 가 한 번에 쓴다 · 사람 문장도 다듬는다) · **M-8-a**(스키마 한 벌 · 서버 검증 넷) · **M-9-a**(재전사 전량 교체 · `at_ms` 기준 동일 · 매칭은 ms) · **M-9-b**(표대로만 치환 · `speaker_label` 불변) · **M-19**(`ai_headline` 은 ② 성공에만 · 부분 저장 없음 · 재생성 없음) · **M-3 · M-4** · **M-13**(녹음 영구 보관 — 재전사와 「다시 시도」의 입력)
- Migration 필요 여부: **있음** — `0008_meeting_payload_terms`
- SPEC 에 환류해야 하는 변경: 없음. 컬럼·수치는 SPEC-008 §4 와 `meeting.md` 컬럼 표가 이미 정본이다

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-013 편집** | `meeting_line.payload` 컬럼 · `MergedSummary` 다섯 · `_parse_output(fill_final=True)` 가 채우는 `payload` 두 모양 | 013 의 드로어가 이 값을 프리필한다 |
| 프론트 | `GET /api/jobs/{id}.progress.phase` · `POST /finalize` | U-1 단계 문구 · U-2 「다시 시도」 |
| **WORK-009** | `auth_service.revoke_meeting_token(meeting_id)` | 이 work 가 **부르는 자리**다(009 는 함수만 만들었다) |

## Internal Interface Contract

외부 계약(`/end` · `/jobs` · `/finalize` · 파이프라인 표 · 검증 표 · 수치)은 **SPEC-008 §4** 가 정본이다. 여기는 Phase 사이 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **파이프라인** | `run_pipeline(job)` = **① → ②**. 스위치가 없다 — `/end` 도 `/finalize` 도 **①부터** 돈다(MF-58). `_plans` 딕셔너리 폐기 |
| **① `transcribe(meeting_id) -> None`** | 읽기(경로 · `context` 재료) → commit → **Soniox(트랜잭션 없음 · 폴링 사이에도 세션 없음)** → 새 세션에서 `meeting_transcript` DELETE + INSERT. 상한 **1200초** · 폴링 **5초**. 실패·상한 → `transcription_failed`/`transcription_timeout` 으로 **즉시 종결**(② 로 가지 않는다). **실시간 블록으로 ② 를 부르는 코드 경로가 없다**(정적 검사) |
| **① 의 `context`** | `general = [{key:"회의 제목"},{key:"프로젝트"},{key:"화자 수"}]` · `text` = **직전 회의 요약**(같은 프로젝트 · 무소속이면 무소속 · `start_at` 이 앞선 가장 최근 `ended`+`succeeded` 의 `ai_headline` · 없으면 **키 생략**) · **`terms` 는 비운다**(DEC-003 OQ-10 — SPEC 이 자리를 잡았다. 새로 묻지 않는다). 상한 8000 토큰 |
| **블록 경계** | `meeting_transcript_blocks.build_blocks(tokens)` **한 함수** — 화자 변경 · 300자 · 토큰 사이 2초 공백. 실시간 중계와 재전사가 **같은 함수**를 쓴다(두 벌이면 근거 칩이 어긋난다) |
| **② `attempt_final(meeting_id, *, timeout_sec) -> _FinalPlan`** | 읽기 → commit → `gateway.run(prompt=build_final_notes_prompt(script), session_id=ai_session_id, output_schema=meeting_batch_service.OUTPUT_SCHEMA, timeout_sec, meeting_token=…)` → **`meeting_batch_service._parse_output(..., fill_final=True)`** + 최종 전용 검증. **`ai_session_id` 가 `NULL` 이면 그 시도 실패**(MF-70 — 재웜스타트 갈래 없음) |
| **검증 함수는 하나다** | 스키마 · 안건 참조 · **업무 참조 사후 검사** · evidence 범위는 **WORK-011 이 만든 함수**를 그대로 쓴다. 최종만 더하는 것 — ① `humanAgendaId` 가 **모든 사람 안건을 정확히 한 번** 덮는가 ② `headline` 1~200자 한 문장(필수) ③ `termCorrections` 배열(빈 배열 가능 · `grade ∈ {auto,guess}`) ④ **페이로드 참조**(유형·프로젝트·연관 업무가 본인의 삭제 안 된 것 — 틀리면 **그 키만 `null`**, 줄·시도는 산다) ⑤ **`payload.status ∈ {todo,in_progress}`** — `done`·`cancelled` 면 **그 키를 뗀다**(줄은 산다) |
| **② 성공 트랜잭션(원자성)** | `merged` 안건 INSERT → `merged` 줄 INSERT → `meeting.ai_headline` · `term_corrections` → **`grade='auto'` 치환**(`meeting_transcript.content` 문자열 치환 · `speaker_label` 불변) → `status='ended'` · `integration_state='succeeded'` → `meeting_batch_run(phase='final', status='succeeded')` → job `succeeded`. **하나라도 실패하면 전부 없다** |
| **미러 안건의 `state`** | `merged` 안건은 `source_agenda_id` 의 사람 안건에서 `state` 를 **복사**한다. `/end` 가 `active→done` 을 이미 했으므로 `active` 가 없다. AI 신설 안건은 `source_agenda_id`·`state` 둘 다 `NULL` |
| **토큰 폐기** | ② 가 **종결될 때**(성공·실패 무관) `auth_service.revoke_meeting_token(meeting_id)`. **best-effort** — 실패해도 job 결과를 뒤집지 않고 로그만(MF-4) |
| **`progress.phase`** | `transcription` = job 이 ① 을 도는 동안 · `final` = 그 회의에 `meeting_batch_run(phase='final')` 행이 생긴 뒤. **컬럼이 아니다** |
| **`mergedSummary`** | **파생 다섯** — `merged` 안건 수 + `kind` 별 줄 수 넷. 저장하지 않는다. **`integratedAt` 은 없다**(SPEC-008 §4 Data Contract) |
| **프론트 폴링** | 2초 · **1230회** 상한. 상한·조회 실패에서 **멈추고** 「다시 확인」만 남긴다. 자동 재시도 없음 |

## Execution

### Phase 0 — 리비전 `0008` · 모델 · enum (백엔드)

- **Status**: TODO
- **설명**: 컬럼이 먼저 서야 ①②의 쓰기가 갈 곳을 갖는다.
- **작업**:
  - [ ] `0008_meeting_payload_terms` — 다섯 변경 + `downgrade`
  - [ ] `models/meeting.py` · `models/job.py` · `dto/enums.py`
  - [ ] `dto/meeting.py` · `schemas/meeting.py` — `payload` 키 · `MergedSummary` 다섯
  - [ ] 기존 `pending_change` 참조를 전부 `payload` 로(백·프론트 타입까지)
- **검증**:
  - [ ] `alembic upgrade head` → `downgrade -1` → `upgrade` 왕복. 기존 `pending_change` 값이 `payload` 로 **살아서** 옮겨진다(RENAME 이라 데이터가 남는다)
  - [ ] `source_human_line_id`·`source_ai_line_id` 컬럼 · FK · 부분 UNIQUE 2 · CHECK 가 **DB 에 없다**(`\d meeting_line` 캡처)
  - [ ] `meeting.term_corrections` 가 `jsonb NULL` 이다. `job.error_code` CHECK 가 5종이다. `meeting_batch_run.phase` CHECK 에 `integration` 이 없다
  - [ ] **정적 검사**: 코드베이스에 `pending_change` · `pendingChange` · `source_human_line_id` · `source_ai_line_id` · `integration_failed` · `final_batch`(JobPhase) 0건(grep)
  - [ ] `make test` 통과(이 Phase 는 동작을 안 바꾼다 — 이름만)
- **완료 증거**: 미작성

### Phase 1 — ① async 재전사 · 블록 묶기 한 곳 (백엔드 + 실물 확인 1건)

- **Status**: TODO
- **설명**: MF-37 · 54. **fallback 이 없다** — 이 단계가 실패하면 회의록은 사람 원본으로 끝난다.
- **작업**:
  - [ ] `integrations/soniox.py` async 갈래(files → transcriptions → 5초 폴링 → transcript) · `install_async_connector()`
  - [ ] `service/meeting_transcript_blocks.py` 로 블록 묶기 이관 · `meeting_stream_service` 위임
  - [ ] `meeting_finalize_service._transcribe()` — `context` 조립 · DELETE + INSERT 한 트랜잭션
  - [ ] `config.py` 수치 · `job_service.progress.phase`
  - [ ] **실물 확인** — 실제 회의 녹음 파일(헤더 없는 webm) 1건을 `stt-async-v5` 에 올려 본다
- **검증**:
  - [ ] **SYS-OQ-5 답** — 헤더 없는 webm 을 `stt-async-v5` 가 받는가. **받으면** 그대로, **거절하면** 그 사실과 응답 코드를 완료 증거에 적고 **코디에게 올린다**(포맷 결정은 사용자 몫 — 여기서 컨테이너를 바꾸지 않는다)
  - [ ] 재전사가 끝나면 `meeting_transcript` 의 실시간 블록이 **전부 사라지고** 재전사 블록만 있다(한 트랜잭션)
  - [ ] **`at_ms` 기준이 같다** — 같은 발화의 근거 칩(`evidence`)이 재전사 뒤에도 같은 구간을 가리킨다(ms 매칭 — M-9-a)
  - [ ] 블록 경계가 실시간과 **같은 함수**를 지난다(정적 검사: 300자·2초 상수가 **한 파일**에만)
  - [ ] 서버 로그에 `stt-async-v5` 호출과 `context.general`(제목·프로젝트·화자 수)이 있고 **`context.terms` 가 비어 있다**
  - [ ] Soniox 키를 막으면 job 이 `failed` · `errorCode='transcription_failed'` · `ended`+`failed` 이고 **`merged` 0건 · `ai_headline NULL`** 이며 **② 가 불리지 않았다**(로그에 codex 호출 0건)
  - [ ] 상한 1200초를 넘기면 `transcription_timeout`
  - [ ] **정적 검사**: ① 실패 경로에서 ② 로 가는 분기가 코드에 **없다**(`_transcribe` 실패 뒤 `attempt_final` 호출 0건 — grep + 테스트)
  - [ ] 폴링 사이에 DB 세션이 열려 있지 않다(코드 리뷰 + `session_scope` 사용 위치)
  - [ ] `make test` 전체 통과
- **완료 증거**: 미작성

### Phase 2 — ② 최종 회의록 한 번 · 용어 치환 · 토큰 폐기 (백엔드)

- **Status**: TODO
- **설명**: MF-52 · 56 · 57 · 59. codex 호출이 **하나**가 되고 `meeting_merge_service` 가 사라진다.
- **작업**:
  - [ ] `meeting_finalize_service` 재작성 — `finalize()` · `run_pipeline` · `_attempt_final` · `_commit_success` · `_commit_failure` · `build_final_notes_prompt`
  - [ ] `_parse_output(fill_final=True)` · `_persist(track='merged')` 확장(WORK-011 함수)
  - [ ] 최종 전용 검증 5(안건 전수 · headline · termCorrections · 페이로드 참조 · `payload.status`)
  - [ ] `grade='auto'` 치환 · `term_corrections` 저장
  - [ ] `revoke_meeting_token()` 호출(종결 시 · best-effort)
  - [ ] `meeting_merge_service.py` · `meeting_integration.json` · `run_final` 계열 · `_agenda_rows` 폐기
  - [ ] `meeting_router` `/finalize`
  - [ ] `tests/test_meeting_finalize.py` 전면 · `test_meeting_merge.py` 삭제
- **검증**:
  - [ ] **BE §12 8** — ② 가 2회 재시도 후 실패하면 `ended`+`failed` 이고 사람 줄 · AI 줄 · 트랜스크립트가 **그대로**다. **① 이 실패하면 ② 로 가지 않고** `merged` 0건이다
  - [ ] 서버 로그에 codex 호출이 **회의 종료 후 한 번**뿐이다(종료 시 배치 0 · 통합 호출 0)
  - [ ] AI 트랙(`track='ai'`)이 종료 전후로 **행 하나도 안 바뀐다**(M-6 · MF-56)
  - [ ] `term_corrections` 표가 DB 에 있고, **`auto` 항목의 STT 표기가 스크립트 본문에서 바뀌어 있으며 `guess` 는 본문 그대로**다. **`speaker_label` 은 바뀌지 않았다**
  - [ ] 사람 안건 하나를 AI 가 빠뜨린 출력 → **그 시도 실패**(재시도). 회의 프로젝트 밖 `taskId` → **그 줄만 `action` 강등**(시도는 산다). `payload.workTypeId` 가 삭제된 유형 → **그 키만 `null`**(줄·시도는 산다). `payload.status='done'` → **그 키만 제거**(줄은 산다)
  - [ ] ② 성공 트랜잭션이 **하나**다 — 중간에 예외를 넣으면 `merged` 0건 · `ai_headline NULL` · `term_corrections NULL` · 치환 안 됨(테스트)
  - [ ] `POST /finalize` 는 `ended`+`failed` 에서만 `202`. `succeeded` 면 `409 invalid_meeting_status`. **①부터** 다시 돈다(로그)
  - [ ] job 상한 2400초를 넘기면 `job_timeout` 으로 마감된다. 기동 스윕이 `running` 을 마감한다
  - [ ] ② 종결(성공·실패 둘 다) 뒤 `auth_session(kind='meeting')` 행이 **0건**이고, 폐기 실패를 심어도 job 결과가 뒤집히지 않는다
  - [ ] **정적 검사**: `meeting_merge_service` · `meeting_integration.json` · `run_final` · `build_final_prompt` · `_agenda_rows` · `BatchPhase.INTEGRATION` 0건(grep)
  - [ ] `make test` 전체 통과
- **완료 증거**: 미작성

### Phase 3 — 생성중 · 실패 · 카운트 다섯 (프론트)

- **Status**: TODO
- **설명**: U-1 · U-2 · U-3 상단 바. **새 시안이 없다** — 회색 상태 바(SPEC-007 U-1)와 [09] L727~733 규격으로 조립한다.
- **작업**:
  - [ ] `MeetingStatusBar` — `generating` 에 phase 둘 · 「다시 시도 중 (n/2)」 · `failed` 버튼 「다시 시도」 · `headline` 카운트 다섯
  - [ ] `useMeetingFinalizeJob` 상한 1230 · `progress.phase` 노출
  - [ ] `api.ts` `/finalize` · `types.ts` `MergedSummary` 다섯 · `errorCode` 5종
  - [ ] `MeetingClosedPage` 생성중 두 단계 · 실패 배너 · `TranscriptPanel` 종료 후 푸터
  - [ ] `closeFixtures.ts` · 관련 테스트
- **검증**:
  - [ ] 회의를 끝내면 상단 바가 「**녹음을 다시 받아쓰고 있습니다**」 → 「**회의록을 정리하고 있습니다**」 순으로 바뀐다. ② 재시도 중이면 「· 다시 시도 중 (n/2)」
  - [ ] 생성중에 「편집」이 없고 줄 버튼 · 「삭제」가 비활성이며 회의록 탭에 **회의 중 원본**이 보인다. **AI 탭 안내 바가 회의 중 값 그대로**(「종결」 문구 0건 — grep)
  - [ ] 새로고침해도 `activeJobId` 로 폴링이 이어진다. 폴링 실패면 스피너 유지 + 「상태를 확인하지 못했습니다 · 다시 확인」이고 **실패로 꾸미지 않는다**
  - [ ] 실패 상태에서만 「**다시 시도**」가 보이고 `POST …/finalize` 를 부른다. 성공한 회의록에는 없다
  - [ ] 상단 바 카운트가 「**안건 n · 논의 n · 결정 n · 액션 n · 업무 n**」 다섯이고 **회의록 탭에 그려진 수와 정확히 같다**. 드로어(U-4)는 같은 값을 두 줄로
  - [ ] 스크립트 푸터가 「전체 스크립트 n분 · 화자 n명」이고 자동 따라가기가 없다
  - [ ] 폴링 상한 상수가 **1230** 이다
  - [ ] `vitest` 전체 통과
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] `alembic upgrade head` → `0008`. **되돌릴 때 `payload` 값이 `pending_change` 로 돌아간다**(RENAME 이라 손실 없음)
- [ ] `SONIOX_API_KEY` 가 async API 에도 유효한지 확인(같은 키)
- [ ] `.env` 에 옛 `MEETING_INTEGRATION_TIMEOUT_SEC` · `MEETING_FINAL_BATCH_TIMEOUT_SEC` 가 있으면 **지운다**(새 이름으로 대체됐다)
- [ ] 백·프론트 같이 배포 — `/integrate` 경로가 사라진다
- [ ] 진행 중인 `generating` 회의가 있으면 기동 스윕이 마감한다(`job_timeout`) — 배포 전 확인

## Rollback

- **스키마**: `alembic downgrade -1` — `payload` → `pending_change` RENAME 복귀. **`source_*_line_id` 는 컬럼이 되살아나되 값은 없다**(지운 값을 되돌리지 않는다 — 통합 규칙 자체가 폐기됐다). `term_corrections` 는 컬럼과 함께 사라진다
- **백엔드**: revert 하면 `/finalize` 가 사라지고 `/integrate` 가 돌아온다 — **`meeting_merge_service` 와 `meeting_integration.json` 이 함께 복구돼야 한다**(같은 커밋으로 지운다)
- **프론트**: 경로·프레임이 짝이라 백엔드와 함께 되돌린다
- **WORK-013 이 들어간 뒤에는 되돌리지 않는다** — 013 이 `payload` 컬럼 위에 선다
- 부분 revert 시: Phase 3(프론트)만 되돌리면 카운트 셋 · 「통합」 문구로 돌아가고 `/finalize` 를 못 부른다(실패 상태에서 복구 불가) — **프론트만 되돌리지 않는다**

## Done Criteria

- [x] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다
- [ ] **SPEC-008 §6 AC 중 이 work 의 12항목**(생성중 두 단계 / 편집 잠금 / 새로고침 / 재전사 후 화자 구분 · `context` 로그 / 정리 후 최종 회의록 · codex **한 번** / 카운트 다섯 일치 / 용어 보정 표 · `auto` 치환 · 화자 라벨 불변 / Soniox 막아 실패 → 배너 · `merged` 0건 · 「다시 시도」로 **재전사부터** / 워커 내려 ② 3회 실패 / job 상한 / 줄 시각 없음 / 「다시 시도」는 실패에서만)이 **실측 캡처로** 완료 증거에 있다
- [ ] **SYS-OQ-5 실물 확인 결과**(헤더 없는 webm)가 적혀 있다
- [ ] BE §12 **8** 테스트가 있다
- [ ] 정적 검사 6종(`pending_change` 0 · `source_*_line_id` 0 · `meeting_merge_service` 0 · `meeting_integration.json` 0 · ① 실패 → ② 분기 0 · 「종결」 문구 0)
- [x] `make test` · `vitest` 전체 통과 · `Errors` 줄 0
- [x] `30-work/README.md` 갱신

> 2026-09-08 — 커밋 `0415290`(be+fe). 검수 `orchestration/work/docs-v1/work012-review-report.md` FAIL 0 · WARN 4(W-1·W-3 닫음 · W-2 progress.phase 규칙과 errorCode 재진입·안내 바 시각은 사용자 결정 대기). pytest 628 · tsc 0 · vitest 327. **미완: 앱 창 실측 · 300분 실물 · 워커 로그 실측은 사용자(아침)**. SYS-OQ-5 통과(`work012-sys-oq5-evidence.md`)

## Open Issues

- **Soniox async 출력은 결정적이지 않다**(2026-09-08 실물 — 같은 62초 webm 을 2회 올려 토큰 시각·화자 배정이 조금 흔들려 2초 공백 경계가 옮겨갔다. 블록 5개/6개. 규칙 셋(화자 변경·300자·2초)은 두 회차 모두 그대로). **재전사 결과가 결정적이라고 전제하는 테스트를 쓰지 않는다** — 이 work 의 테스트는 대역 토큰. 증거 `orchestration/work/docs-v1/work012-sys-oq5-evidence.md`
- **SYS-OQ-5 — 헤더 없는 webm 을 `stt-async-v5` 가 받나.** Phase 1 안에서 파일 하나로 확인한다. **거절하면 그 사실만 보고하고 여기서 포맷을 바꾸지 않는다**(녹음 컨테이너 변경은 SPEC-007 §C-8 「포맷을 못박지 않는다」에 걸린 사용자 결정 영역)
- **OQ-10 `context.terms`** → **SPEC 대로 비운다.** 새로 묻지 않는다
- **`integration_state` 라는 컬럼 이름** — 뜻은 「최종 회의록 생성 상태」로 바뀌었지만 **이름은 그대로**다(M-4). 이름을 바꾸는 리비전을 만들지 않는다
- **`_persist(track=…)` 의 확장 범위** — WORK-011 이 만든 함수에 트랙 인자를 더하는 것이 이 work 다. 011 이 먼저 머지돼야 한다(§Depends)
- **`ai-prompt-draft.md` §C 의 「AI 요약 트랙을 전체 재정리한다」** — 최종은 `merged` 트랙에 쓴다(MF-56 · M-8). 초안 문구를 그대로 쓰지 않는다

## Related

- SPEC: SPEC-008 U-1 · U-2 · §4 · §5 · §6 · SPEC-007 §4(스키마 한 벌 · 블록 규칙) · DEC-003 §4 · §6 · §7 · §STT
- Architecture: `backend/README.md` §5-2 · §5-3 · §6 · §7 · §8-3 · §12 8 · `frontend/README.md` §8 · `system/README.md` §③ · `database/domains/meeting.md` M-8 · M-8-a · M-9-a · M-9-b · M-13 · M-19
- Work: WORK-009 · WORK-011(선행) · WORK-013(소비)
