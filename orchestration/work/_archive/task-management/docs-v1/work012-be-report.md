# WORK-012 Phase 0~2 backend 완료 보고 — 리비전 0008 · async 재전사 · 최종 회의록 한 번 · 용어 치환 · 토큰 폐기

워크트리 `/Users/kknaks/orca/workspaces/task_management/docs-v1` · HEAD `f70a094`(WORK-011). **커밋하지 않았다.**
`app/front/` 는 손대지 않았다(Phase 3 는 다른 워커).

## 1. SYS-OQ-5 실물 — **받는다**

별도 파일: `…/scratchpad/work-012-sys-oq5-evidence.md`(원본 `oq5.webm` 도 같은 디렉토리).

compose `api` 컨테이너의 실제 녹음 `/data/recordings/3.bin`(1.78MB · 62초 · 스트림 append)을 그대로 올렸다.
헤더는 EBML/`webm` 이 있고 **Segment 크기가 unknown**(`0x01FF…FF`) — SYS-OQ-5 가 걱정한 그 모양이다.

```
ACCEPTED — 토큰 307개 · 9.1초 · 화자 ['1','2','3'] · 마지막 endMs 62190
```

거절 없음(4xx·error 상태 0). 같은 토큰을 `build_blocks()` 에 넣으면 블록 6개가 나오고 화자 변경에서 끊긴다.
**컨테이너를 바꾸지 않았다.** 300분짜리 실물은 아직 안 올려 봤다 — 상한 1200초는 그 규모에서 다시 볼 값이다.

## 2. 변경 파일

```
신규  alembic/versions/0008_meeting_payload_terms.py
신규  service/meeting_transcript_blocks.py        블록 경계 한 곳(실시간·재전사 공용)
폐기  service/meeting_merge_service.py · ai_schemas/meeting_integration.json · tests/test_meeting_merge.py
수정  models/meeting.py · dto/enums.py · dto/meeting.py · schemas/meeting.py · schemas/job.py
수정  integrations/soniox.py                      async 갈래(SttAsyncConnector · SonioxAsyncClient · TranscribeContext · install_async_connector)
수정  service/meeting_finalize_service.py         전면 재작성
수정  service/meeting_batch_service.py            fill_final · _persist(track·copy_human_state) · 공개 별칭 · run_final 계열 폐기
수정  service/meeting_stream_service.py           블록 묶기 위임
수정  service/job_service.py                      progress.phase 파생 · meeting_job_timeout_sec
수정  service/meeting_service.py · meeting_edit_service.py · meeting_task_link_service.py
수정  repository/ meeting_repository · meeting_transcript_repository · meeting_line_repository · meeting_child_repository · meeting_batch_run_repository
수정  api/meeting_router.py                       /integrate → /finalize
수정  config.py · pyproject.toml · uv.lock        수치 5종 · httpx 를 런타임 의존으로
수정  tests/ fakes/soniox.py · meeting_close_fixtures.py · test_meeting_finalize.py(전면) ·
      test_job.py · test_meeting_edit.py · test_meeting_task_link.py · test_meeting_batch.py · test_migrations.py
```

## 3. Phase 0 — 리비전 0008 · 모델 · enum

- `pending_change` → **`payload` RENAME**(값이 살아 옮겨진다) + CHECK `payload IS NULL OR (track IN ('merged','human') AND kind IN ('action','task'))`.
  **자리 밖에 실려 있던 옛 값은 버린다**(SPEC-008 §4 「`payload` 자리」) — 개발 DB 에 그런 행이 있어 CHECK 가 걸렸다. 마이그레이션이 먼저 `NULL` 로 만든다.
- `source_human_line_id` · `source_ai_line_id` + FK 2 + 부분 UNIQUE 2 + CHECK **삭제**.
- `meeting.term_corrections jsonb NULL` 신설 · `batch_run.phase` CHECK `incremental|final` · `job.error_code` CHECK **5종**.
- `JobErrorCode` 5 · `JobPhase` = `transcription|final` · `BatchPhase.INTEGRATION` 삭제 · `MergedSummary` **다섯**(`integratedAt` 없음).
- **`JSONB(none_as_null=True)`** 를 `payload`·`term_corrections` 에 걸었다 — 없으면 파이썬 `None` 이 JSONB `'null'` 로 들어가 `payload IS NULL` 이 거짓이 되어 자리 CHECK 가 멀쩡한 줄을 막는다(실측으로 밟았다).

## 4. Phase 1 — ① async 재전사 · 블록 경계 한 곳

- `SonioxAsyncClient` — `POST /v1/files` → `POST /v1/transcriptions`(`stt-async-v5` · `ko` · diarization · `context`) → 상태 폴링 → `GET …/transcript`.
  실패는 `SttUpstreamError`, **상한은 `TimeoutError`** 로 갈라 낸다(부르는 쪽이 `transcription_failed` 와 `transcription_timeout` 을 가른다).
  2xx 가 아니면 **본문째** 예외에 싣는다(SYS-OQ-5 같은 확인의 근거가 된다).
- `service/meeting_transcript_blocks.py` — `BlockBuilder`(실시간이 토큰마다 부른다) · `build_blocks()`(재전사가 한 번에 부른다).
  **300자 · 2초 상수가 이 파일에만** 있다. `meeting_stream_service` 는 판정을 여기로 위임했고 동작은 그대로다.
- `_transcribe()` — 읽기 → 커밋 → **Soniox(트랜잭션 없음)** → 새 세션에서 `meeting_transcript` DELETE + INSERT.
  `context.general` 셋(제목 · 프로젝트 · 화자 수) · `text` 는 같은 프로젝트 직전 `ended+succeeded` 의 `ai_headline`(없으면 **키 생략**) · **`terms` 비움**.
- 수치 — `meeting_transcribe_timeout_sec=1200` · `meeting_transcribe_poll_sec=5` · `meeting_final_timeout_sec=300` · `meeting_final_attempts=3` · `meeting_job_timeout_sec=2400`. 옛 셋 폐기.

## 5. Phase 2 — ② 최종 회의록 한 번

- `run_pipeline(job)` = **① → ②**. `_plans` 스위치 폐기 — `/end` 도 `/finalize` 도 ①부터.
  ① 실패는 `_commit_failure` 로 **즉시 종결**하고 `return` 한다(그 갈래 안에 `_attempt_final` 이 없다 — 정적 검사).
- `_attempt_final` — `build_final_notes_prompt(script)` · `session_id=ai_session_id` · `output_schema=meeting_notes.json` · 300초 · 토큰 헤더.
  `ai_session_id`·토큰이 없으면 **그 시도 실패**(재웜스타트 없음).
- 검증은 **WORK-011 함수 그대로** — `parse_output(fill_final=True)` · `demote_if_needed` · `persist(track='merged', copy_human_state=True)`.
  최종만 더한 다섯 — 사람 안건 전수 · `headline` 1~200 한 문장 · `termCorrections` 배열/`grade` · 페이로드 참조(그 키만 `null`) · `payload.status ∈ {todo,in_progress}`(아니면 키 제거).
- `_commit_success` 가 **한 트랜잭션** — merged INSERT → `auto` 치환 → `batch_run(final,succeeded)` → `ai_headline`·`term_corrections` → job. 폐기만 그 밖이다.
- `/integrate` → **`/finalize`**. `meeting_merge_service` · `meeting_integration.json` · `run_final` 계열 · `_agenda_rows` · `test_meeting_merge.py` 폐기.

## 6. 검증

| 항목 | 결과 |
|---|---|
| `make test` 전체 | **626 passed** · Errors 줄 0 |
| 리비전 왕복 | `0008` · `0007` 둘 다 테스트로 있다(`test_migrations.py`). `pending_change` 값이 `payload` 로 **살아서** 옮겨지고 되감으면 옛 이름으로 돌아온다 |
| `\d meeting_line` | `source_*` 컬럼 · FK · 부분 UNIQUE 2 · CHECK **없음** · `payload jsonb` + `ck_meeting_line_payload` 있음 |
| `meeting.term_corrections` | `jsonb` · `ck_meeting_batch_run_phase` 에 `integration` 없음 · `ck_job_error_code` 5종 |
| **BE §12 8** | ② 3회 실패 → `ended`+`failed` · `merged` 0건 · 사람 줄 3 · 재전사 블록 2 그대로 |
| ① 실패 → ② 미호출 | `transcription_failed`·`transcription_timeout` 둘 다 codex 호출 **0건** · `merged` 0건 · 실시간 블록 그대로 |
| codex 호출 횟수 | 종료 후 **한 번**(세션 resume · 스키마 `meeting_notes.json` · 300초) |
| AI 트랙 불변 | 종료 전후 `track='ai'` 안건·줄의 **id·본문이 그대로** |
| 용어 치환 | `auto` 만 본문이 바뀌고 `guess` 는 표에만 · `speaker_label` 불변 · 표가 비면 치환 0 |
| 줄 단위 완화 | 프로젝트 밖 `taskId` → `action` 강등(`payload` 도 뗀다) · 삭제된 유형 → 그 키만 `null` · `done`/`cancelled` → 그 키 제거 · 논의 줄 `payload` 버림 |
| 원자성 | `_commit_success` 가 `session_scope()` **하나**(정적) + 중간 예외 시 job `running`·회의 `generating` 유지(부분 성공 없음) |
| `/finalize` | `ended`+`failed` 에서만 202 · `succeeded` 면 409 · ①부터 다시 돈다(재전사 호출 1회) |
| 토큰 | ② 종결(성공·실패) 뒤 `auth_session(kind='meeting')` **0건** · 폐기 실패를 심어도 job 결과 불변 · `/finalize` 가 **하나** 다시 발급하고 ② 가 그 원문으로 헤더 |
| job 상한 | 수치 다섯이 계약대로(2400 · 1200 · 5 · 300 · 3). 넘겼을 때의 마감(`job_timeout` + 회의 `ended`)은 `test_job.py` 가 실행기째 본다 |
| `progress.phase` | ① 도는 동안 `transcription` → `batch_run(final)` 생긴 뒤 `final` |
| `mergedSummary` | 다섯 · `integratedAt` 없음 · 회의록 탭 줄 수와 일치 |

### 정적 검사 (grep · 0건)

```
meeting_merge_service 0 · meeting_integration.json 0 · run_final 0 · build_final_prompt 0 · _agenda_rows 0
BatchPhase.INTEGRATION 0 · pending_change 0 · pendingChange 0 · source_human_line_id 0 · source_ai_line_id 0
integration_failed 0 · FINAL_BATCH 0 · NotImplementedError(meeting_batch_service) 0
find_ai_agenda_by_source → 호출 0건이라 **지웠다**(브리프 지시)
ai_schemas/ = meeting_notes.json 하나
BLOCK_MAX_CHARS · BLOCK_GAP_MS 를 가진 파일 = meeting_transcript_blocks.py 하나
MeetingAgendaTracksDTO( 를 만드는 곳 = meeting_service.py 하나(두 번째 직렬화 0)
```

옛 리비전(`0005`·`0006`)은 그 시점의 스키마라 검사에서 뺐다.

## 7. 미결 · 주의점

1. **`/finalize` 가 회의 토큰을 다시 발급한다** — 코디 확정(2026-09-08)대로 넣었다. 조건 셋 다 지켰다:
   `/start` 와 **같은 `auth_service.issue_meeting_token`**, 발급 **전에 `revoke_meeting_token` 으로 남은 행을 지운다**(폐기가 best-effort 라 남아 있을 수 있다), ② 종결 폐기는 그대로.
   테스트 `test_finalize_reissues_exactly_one_meeting_token` 이 행 1 · 새 원문 · ② 헤더까지 본다.
2. **`meeting_notes.json` 의 `termCorrections` 항목 모양을 고쳤다** — WORK-011 이 `{from,to}` 로 두었는데 SPEC-008 §4 는 `{stt, correct, grade}` 다. WP 는 「WORK-012 는 읽기만」이라고 했지만 그 모양으로는 ② 가 아예 통과하지 못한다(실측으로 밟았다). **SPEC 대로 고쳤다** — 회의 중 경로는 `null`/빈 배열이라 영향이 없다.
3. **`_demote_if_needed` 가 강등할 때 `payload` 도 뗀다** — SPEC-008 §4 「그 줄만 `taskId` · `payload` 를 떼고」. WORK-011 시점엔 `payload` 가 없어 `taskId` 만 뗐다.
4. **원자성 테스트는 정적 + 행동 둘로 나눴다** — 하네스가 모든 단계를 한 세션에 묶어(`close_scope`) 커밋 경계를 실행으로 볼 수 없다. `_commit_success` 가 `session_scope()` 하나이고 여섯 쓰기가 그 안에 있다는 것을 코드에서 보고, 실행 쪽은 「중간 예외 → job `running` · 회의 `generating`(부분 성공 없음)」으로 본다.
5. **`httpx` 를 런타임 의존으로 올렸다**(전에는 dev 전용). 재전사 REST 가 쓴다.
6. **`prepare_recording` 이 AI 트랙 행을 직접 심는다** — 종료 시 배치가 없어져(MF-56) AI 줄이 저절로 생기지 않는데, 「AI 트랙 불변」과 편집 테스트가 그 줄을 필요로 한다. 배치를 돌리면 대역 게이트웨이 응답 순서를 테스트가 못 쥔다.
7. **`job_timeout_sec` → `meeting_job_timeout_sec`** 으로 이름이 바뀌었다(`job_service` 가 읽는다). job kind 가 하나뿐이라 그대로 뒀는데, 다른 kind 가 생기면 kind 별 상한이 필요하다.
8. **Phase 3(프론트)이 아직 없다** — `/integrate` → `/finalize` · `MergedSummary` 다섯 · `errorCode` 5종 · `phase` 두 값이 바뀌었으므로 **같은 PR 로 나가야 한다**.
9. **300분 실물 · 워커 로그 실측**은 안 했다. Done Criteria 의 앱 창 캡처도 남아 있다.
10. **job 상한 「넘겼을 때」 테스트를 두 벌 두지 않았다** — 처음엔 `test_meeting_finalize.py` 에도 handler 대역을 넣었는데
    `test_job.py` 의 같은 대역과 부딪혀 전체 스위트에서만 흔들렸다(단독 실행은 통과). 수치 단언만 남기고 동작은 `test_job.py` 하나가 본다.
11. 커밋·push 하지 않았다.
