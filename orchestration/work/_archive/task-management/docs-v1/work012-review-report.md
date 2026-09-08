---
type: review
work: WORK-012
title: "WORK-012 검수 — async 재전사 → 최종 회의록 한 번 · 용어 보정 · payload 컬럼 · 종료 화면"
reviewer: reviewer
date: 2026-09-08
scope: "미커밋 변경 62 파일(back 34 · front 26) + 리비전 0008 · meeting_transcript_blocks.py 신설 · 폐기 4"
worktree: /Users/kknaks/orca/workspaces/task_management/docs-v1 (kknaksss/docs-v1 · HEAD f70a094)
verdict: "FAIL 0 · WARN 4 · 문서 공백 4"
---

# WORK-012 검수 리포트

**FAIL 0 · WARN 4 · 문서 공백 4.**
`tauri.conf.json` 은 범위 밖이라 보지 않았다. 테스트는 돌리지 않았다(코디 실측 — back 626 · front tsc 0 · vitest 327). 앱 창 실측 · 300분 실물은 아침 항목이라 요구하지 않았다.

## 0. 축별 판정 한 줄

| 축 | 판정 | 한 줄 |
|---|---|---|
| 2-1 fallback 0 · 한 번 | **PASS** | `run_pipeline` 의 ① 실패 두 갈래가 `_commit_failure` + `return` 으로 끝나고 정적 테스트가 그 블록에 `_attempt_final` 이 없음을 잠근다. ② 는 정확히 3회 · ① 은 0회 |
| 2-2 리비전 0008 · payload 자리 | **PASS** | 다섯 변경이 WP 그대로 · 자리 밖 옛 값을 CHECK 전에 NULL · downgrade 대칭 · 왕복 테스트 둘(0008 · 0007) · `JSONB(none_as_null=True)` 가 `payload`·`term_corrections` 둘 다에 |
| 2-3 외부 호출 중 트랜잭션 0 · 원자성 | **PASS** | `_transcribe`·`_attempt_final` 둘 다 읽기 세션을 닫고 나서 외부를 부른다 · `_commit_success` 가 `session_scope()` **하나**에 여섯 쓰기 · 정적 + 행동 테스트 둘 |
| 2-4 검증 함수 하나 · 스키마 한 벌 | **PASS** | `fill_final=True` 구현 · `NotImplementedError` 0 · 두 번째 파서 0 · `meeting_notes.json` 하나 · `termCorrections` `{stt,correct,grade}` · 최종 전용 검증 다섯 전부 · 011 WARN 4(같은 직렬화 함수 정적 검사)도 들어왔다 |
| 2-5 토큰 | **PASS** | 종결(성공·실패) 뒤 best-effort revoke · `finalize()` 가 revoke → `/start` 와 **같은** `issue_meeting_token` · 두 번째 발급 코드 0 · 전용 테스트 |
| 2-6 프론트 | **PASS · WARN 1** | 단계 문구 · 배너 · 툴팁 · 카운트 다섯 · 1230 · `follow={false}` · 소유자 하나 · 013/014 는 rename 뿐. 다만 ② 단계 문구가 성공 경로에서 화면에 뜨지 않는다 |
| 2-7 spec 에서 지워진 것 | **WARN 1** | `pendingChange`·`sourceHumanLineId` 는 깨끗이 사라졌다. **`finalBatchState` 만 14곳에 남았다** |
| 2-8 테스트 | **PASS · WARN 1** | BE §12 8 을 비롯해 Phase 0~3 검증을 사실상 전부 덮는다. Soniox 비결정을 전제한 테스트 0(대역 토큰). 창 하나가 빈다 |

---

## 1. FAIL

**없다.** 브리프가 지목한 FAIL 조건 일곱을 전부 확인했다 — fallback 경로 0 · 외부 호출 중 트랜잭션 0 · 원자성 유지 · 두 번째 파서/스키마 0 · 토큰 회의당 하나 · `task.status` 직접 대입 0 · 013/014 범위 침범 0.

---

## 2. PASS — 무엇을 확인했나

### 2-1. fallback 0 · 한 번 (MF-56 · 58)

| 검사 | 결과 |
|---|---|
| ① 실패 → ② 경로 | `meeting_finalize_service.py:186-233` — `except TimeoutError` · `except SttUpstreamError` 두 갈래가 각각 `_commit_failure(...)` 뒤 **`return`**. 정적 테스트 `test_meeting_finalize.py:704` 가 `run_pipeline` 의 실패 팔만 잘라 「`_attempt_final` 없음 · `return` 정확히 2개」를 잠근다. 행동 테스트는 `:135`(codex 호출 0 · `merged` 0) |
| `run_pipeline` 스위치 | `_plans` 딕셔너리 없음. `/end`(`:106`)와 `/finalize`(`:121`)가 **같은 `_start_job`**(`:138`)을 부르고 그 job 이 `run_pipeline` 하나를 돈다 — resume 갈래 0. 테스트 `:551`(「①부터 다시 돈다」 — 재전사 호출 1회) |
| ② 시도 횟수 | `:215` `for attempt in range(1, attempts + 1)` · `meeting_final_attempts=3` → **최대 3회(재시도 2)**. ① 은 재시도 루프 자체가 없다(0회) |
| 시도 타임아웃 | `:218-224` `except AgentRunTimeout` → `timeouts += 1` · `_record_attempt` · `continue`. **실패로 세고 다음**이다. 전부 타임아웃이면 `final_timeout`, 아니면 `final_failed`(`:236-238`). 테스트 `:269` |
| 실시간 블록으로 ② | 없다 — ① 이 성공해야만 ② 에 닿고, `_attempt_final` 이 읽는 `list_blocks` 는 `_transcribe` 가 이미 갈아끼운 뒤다 |
| 재전사 뒤 실시간 블록 | `:281-285` 한 트랜잭션 안 `delete_by_meeting` → `bulk_create`. 테스트 `:71` |
| `at_ms` 기준 | `_transcribe` docstring 대로 파일 시작 = `recording_started_at` 이라 `base_ms=0`(M-9-a). 블록 경계는 `meeting_transcript_blocks` 한 함수 — 정적 테스트 `:682` 가 `BLOCK_MAX_CHARS`·`BLOCK_GAP_MS` 를 가진 파일이 하나임을 잠근다 |

### 2-2. 리비전 0008 · `payload` 자리 (M-14)

- **① RENAME** — `op.alter_column("meeting_line", "pending_change", new_column_name="payload")` 라 **값이 살아 옮겨진다**. 그 **다음**에 자리 밖 값을 `UPDATE … SET payload = NULL WHERE NOT (<check>)` 로 버리고, 그 **뒤에** CHECK 를 건다. 순서가 맞다 — CHECK 를 먼저 걸면 기존 행이 막힌다.
- **② 통합 잔재** — 부분 UNIQUE 2 → CHECK 1 → FK 2 → 컬럼 2 순으로 지운다(의존 순서 맞음).
- **③** `meeting.term_corrections jsonb NULL` · **④** `batch_run.phase` CHECK `incremental|final`(옛 `integration` 행 먼저 DELETE) · **⑤** `job.error_code` CHECK **5종**(옛 `integration_*` 행 먼저 DELETE).
- **downgrade 가 대칭이다** — 역순으로 되돌리고 마지막에 `payload → pending_change` RENAME. 지운 컬럼은 값 없이 되살아난다(WP 가 명시한 대로).
- **`JSONB(none_as_null=True)`** — `models/meeting.py:99`(`term_corrections`) · `:227`(`payload`) **둘 다**. 없으면 파이썬 `None` 이 JSONB `'null'` 로 들어가 `payload IS NULL` 이 거짓이 되고 자리 CHECK 가 멀쩡한 줄을 막는다(워커가 실측으로 밟았다).
- **왕복 테스트 둘** — `test_migrations.py:112`(0008 — `pending_change` 값이 `payload` 로 살아 옮겨지고 되감으면 옛 이름으로) · `:199`(0007). 컬럼·인덱스·CHECK 를 이름으로 확인한다.

### 2-3. 외부 호출 중 트랜잭션 0 · 원자성 (BE §7 · §5-3)

| 검사 | 결과 |
|---|---|
| `_transcribe` | `:246-258` 읽기 `session_scope` → **닫힘** → `:275` Soniox `transcribe(...)`(폴링 포함) → `:281` 새 `session_scope` 로 DELETE+INSERT. **폴링 사이에 세션을 잡는 코드가 없다** — 폴링이 커넥터 안에 있고 그 바깥에 세션이 없다 |
| `_attempt_final` | `:322-334` 읽기 세션 닫힘 → `:342` `gateway.run(...)` → `_apply_reference_checks`(`:393`)가 **자기 세션**을 새로 연다. codex 대기 중 세션 0 |
| `_commit_success` 원자성 | `:476-511` — `session_scope()` **하나** 안에 `persist(merged)` → `auto` 치환 → `create_run(final,succeeded)` → `finish_integration(headline, term_corrections)` → `job.finish(succeeded)` 여섯. 폐기(`_revoke_token`)만 그 밖이다(계약대로 best-effort). 정적 테스트 `:447` + 행동 테스트 `:471`(중간 예외 → job `running`·회의 `generating` — 부분 성공 없음) |
| AI 트랙 불변 | 종료 파이프라인 어디에도 `track='ai'` 쓰기가 없다. 테스트 `:304` 가 종료 전후 id·본문 동일을 본다 |
| `speaker_label` 불변 | `meeting_transcript_repository.replace_content`(`:129-141`)가 `content` 컬럼만 `func.replace` 한다 |
| `guess` 본문 불변 · 표 밖 치환 0 | `:492-497` — `row["grade"] != "auto"` 면 `continue`. 부르는 쪽이 `auto` 항목만 넘기므로 표 밖 치환이 성립할 수 없다. 테스트 `:337` · `:359` |

### 2-4. 검증 함수 하나 · 스키마 한 벌 (MF-52)

- **`fill_final=True` 가 구현됐다** — `NotImplementedError` 가 백엔드 전체에 **0건**(011 검수 W-3 해소). `meeting_batch_service` 가 `parse_output` · `SchemaViolation` · `demote_if_needed` · `persist` 를 **공개 별칭**으로 내고 `_attempt_final`(`:350-357`)이 그것을 그대로 쓴다 — 두 번째 파서 0.
- `_persist` 는 `track=` · `copy_human_state=` 인자만 늘었다(확장). `merged` 안건이 사람 안건의 `state` 를 복사한다 — 테스트 `:203`.
- **`ai_schemas/` 에 `meeting_notes.json` 하나.** `meeting_integration.json` 삭제 ✓.
- **`termCorrections` 항목이 `{stt, correct, grade}`** 로 고쳐졌다(SPEC-008 §4). WORK-011 이 `{from,to}` 로 둔 것을 바꾼 것인데, 회의 중 경로는 그 값을 읽지 않고 `null`/빈 배열이라 **영향 0**이다(`_parse_output` 의 회의 중 갈래가 `termCorrections` 를 읽지 않는다). 스키마가 한 벌이라 이 수정 없이는 ② 가 통과 자체를 못 한다 — 올바른 정정이다.
- **최종 전용 검증 다섯이 전부 있다** — `_validate_final`(`:368`) ① 사람 안건 전수·정확히 한 번 ② `headline` 1~200 한 문장(줄바꿈 금지) ③ `termCorrections`/`grade`, `_apply_reference_checks`(`:393`)+`_clean_payload`(`:435`) ④ 페이로드 참조(`workTypeId`·`projectId` 는 그 키만 `null` · `relatedTaskIds` 는 걸러낸다) ⑤ `payload.status ∉ {todo,in_progress}` 면 **그 키만 제거**. 업무 참조 강등은 011 함수이고 **강등 시 `payload` 도 뗀다**(`:418-421`).
- `build_final_notes_prompt` — 「새로 드러난」·「추가할 줄」 **0건**, 「처음부터 다시 읽고 최종 회의록 한 벌을 써라」 + 조회 순서 3단계. 싣는 것은 **재전사 스크립트 하나**(테스트 `:185`).
- **폐기 전수 0건** — `meeting_merge_service` · `meeting_integration.json` · `run_final` · `build_final_prompt` · `_agenda_rows` · `BatchPhase.INTEGRATION` · `find_ai_agenda_by_source`(011 W-2 해소) 가 소스에 **하나도 없다**(남은 히트는 전부 정적 테스트의 needle 목록과 주석). 정적 테스트 `:662`.
- **011 WARN 4 해소** — `test_no_second_serializer_for_the_agenda_tree`(`:693`)가 `MeetingAgendaTracksDTO(` 를 만드는 곳이 `meeting_service.py` 하나임을 잠근다.

### 2-5. 토큰 (A-13 · MF-69)

- `_revoke_token`(`:536`)이 `_commit_success`(`:511`)와 `_commit_failure`(`:534`) **둘 다**의 끝에서 불린다 — 성공·실패 무관 ✓. `on_timeout`(`:180`)에도 있다.
- **best-effort** — 실패해도 job 을 뒤집지 않는다. 테스트 `:513`(폐기 실패를 심어도 job 결과 불변) · `:495`(종결 뒤 행 0건).
- **`/finalize` 재발급**(`:132-135`) — `revoke_meeting_token` **먼저**(폐기가 best-effort 라 남아 있을 수 있다) → `auth_service.issue_meeting_token`, 즉 **`/start` 와 같은 함수**다. 두 번째 발급 코드 0. 어느 시점에도 회의당 하나 — 전용 테스트 `:572` 가 행 1 · 새 원문 · ② 헤더까지 본다.

### 2-6. 프론트 (SPEC-008 U-1 · 2 · 4)

| 검사 | 결과 |
|---|---|
| 단계 문구 둘 | `MeetingStatusBar.tsx:108-120` `generatingLabel(phase, attempt)` 하나가 정한다. `phase !== "final"`(첫 폴링 전 `null` 포함) → 「녹음을 다시 받아쓰고 있습니다」 · `final` → 「회의록을 정리하고 있습니다」 + `attempt>1` 이면 「· 다시 시도 중 (n−1/2)」. 처리 시간을 안 적는다(MF-37) |
| 새로고침 폴링 | `useMeetingFinalizeJob.ts:38` — `meeting.status === "generating"` 일 때 `meeting.activeJobId` 로 잇는다. job id 를 따로 기억하지 않는다 |
| 폴링 실패 | 상한 · 조회 실패에서 **멈추고** 「상태를 확인하지 못했습니다 · 다시 확인」만 — 실패로 꾸미지 않는다. `retry:false` · 타이머 0(정적 ⑲) |
| 「다시 시도」 | `ended`+`failed` 에서만 · `POST …/finalize`. 사유는 **툴팁으로만**(`failedReasonTooltip` — `transcription_*` / 그 밖 두 갈래) |
| 화면 문구 | 「종결」·「다시 생성」 **0건**(정적 ㉒ · 주석 제외) |
| 카운트 다섯 | `:191` `mergedSummary` 를 그대로 그린다(화면이 세지 않는다). `integratedAt` 0 · `headline` 은 `ai_headline` 파생 |
| 호출자 · 소유자 | `finalizeMeeting(` 호출자 = `api.ts` + 폴링 훅 **둘**(정적 ㉒) · 단계 문구·배너 소유자 = `MeetingStatusBar.tsx` **하나**(정적 ㉒) |
| 스크립트 | `TranscriptPanel` 에 `follow` prop · 종료 후 `follow={false}` — 자동 따라가기 없음 |
| 상한 상수 | `JOB_POLL_MAX_COUNT = 1230`(정적 ⑲) |
| 금지 목록 | `fetch(` 직접 0 · 인라인 hex 0 · `Sheet`/`Dialog` 직접 import 0(기존 정적 ① · ② · ㉑) |
| 013/014 침범 | **0** — `useMeetingEdit` · `LineTaskButton` · `LinkTaskDrawer` · `useMeetingTaskLink` 의 diff 는 `pendingChange → payload` · `pendingChangeSummary → payloadSummary` **기계적 rename** 뿐이고 모양·흐름이 그대로다. `MeetingDetailDrawer.tsx` · `MeetingEditMode.tsx` 소스는 손대지 않았다(테스트만 갱신). breadcrumb · 헤더 · 미리보기 패널 0 |

### 2-8. 테스트 · Soniox 비결정

`test_meeting_finalize.py` 가 Phase 1~2 검증을 거의 전부 덮는다(아래 §5 표). **BE §12 8** 은 `:250` 에 문장 그대로 있다.
**Soniox 비결정을 전제한 테스트는 없다** — `tests/fakes/soniox.py:95 FakeAsyncStt Connector` 가 스크립트 토큰을 돌려주므로 블록 수가 흔들릴 여지가 없다. 증거 파일이 경고한 「블록 5~6」은 실물에만 해당하고 스위트에 영향이 없다 ✓.

---

## 3. WARN

### W-1. `except Exception` 이 하나 생겼고, **그것을 잡던 정적 검사가 같은 변경에서 삭제됐다**

- **자리**: `app/back/service/meeting_finalize_service.py:544`
  ```python
  except Exception:  # noqa: BLE001 — best-effort 폐기의 정의가 「무엇이 나도 job 을 뒤집지 않는다」다(MF-4)
  ```
- **어긋난 문서**: `backend/README.md` §8-1 「**`except Exception` 을 쓰지 않는다.** 포착은 구체 예외 타입으로만 한다.」
- **삭제된 가드**: `test_meeting_finalize.py` 의 `test_static_end_has_no_stream_condition_and_no_broad_except` 가 통째로 없어졌다. 그 테스트가 잠그던 것은 셋이다 —
  1. `except Exception`·`except BaseException` 0 in **`meeting_finalize_service` · `meeting_merge_service` · `meeting_edit_service` · `job_service` · `meeting_batch_service`** + **`job_repository` · `meeting_line_repository`** → **대체 없음**
  2. `is_active(` · `meeting_stream_disconnected` not in finalize(「WS 연결 있음」을 조건으로 보지 않는다 — SPEC-008 §4) → **대체 없음**(속성 자체는 아직 0건으로 지켜지고 있다)
  3. `ai_headline` 단일 writer → **대체됐다**(`test_only_the_finalize_service_writes_the_headline_and_terms`, `:714`)
- **남은 가드의 사각**: `test_meeting_live_static.py:78-88` 은 `meeting_stream_service` · `meeting_batch_service` · `meeting_service` 와 integrations 셋만 본다. **finalize · edit · job service 와 두 repository 는 이제 아무도 안 본다.**
- **좁힐 수 있었다**: 잡는 대상은 `revoke_meeting_token` → `delete_meeting_tokens` 의 SQLAlchemy 예외라 `SQLAlchemyError` 로 충분하다. 「무엇이 나도」라는 주석의 의도는 이해되지만, BE §8-1 은 그 예외를 두지 않았다.
- **판단**: 코드를 문서에 맞추든 문서에 예외를 적든 둘 중 하나가 필요하다. 어느 쪽이든 **가드를 되살려야** 한다 — 지금은 위반이 하나 있고 그것을 잡을 검사가 없다.

### W-2. ② 단계 문구가 **성공 경로에서 화면에 뜨지 않는다**

- **자리**: `job_service.py:212-221` `derive_progress(job, final_started=…)` · `:226-234` `final_started = meeting_batch_run(phase='final') 행이 있는가`
- **무엇이 일어나나**: `phase='final'` 행이 처음 생기는 시점은 둘뿐이다 — ② **시도가 실패**한 뒤(`_record_attempt`, `:461`) 또는 `_commit_success`(`:493-501`) **안**. 성공 트랜잭션은 같은 세션에서 `job.finish(succeeded)` 까지 하므로, `phase` 가 `final` 이 되는 순간 job 은 이미 `succeeded` 다 → 프론트는 폴링을 멈추고 한 줄 요약 바로 넘어간다.
- **결과**: **② 가 한 번도 실패하지 않는 정상 경로에서 「회의록을 정리하고 있습니다」가 단 한 번도 안 보인다.** 사용자는 ① 문구만 보다가 바로 완료 화면을 본다.
- **어긋난 문서**: SPEC-008 U-1 「생성중 — **단계 문구 둘**」 · WP Phase 3 검증 「상단 바가 「녹음을 다시 받아쓰고 있습니다」 → 「회의록을 정리하고 있습니다」 **순으로 바뀐다**」
- **코드는 계약에 충실하다** — 파생 규칙이 SPEC-008 §4 · WP §Internal Interface 의 문장 그대로다(「그 회의에 `meeting_batch_run(phase='final')` 행이 생긴 뒤」). **깨진 것은 규칙 쪽이다**(→ D-2). 그래서 FAIL 이 아니라 WARN 이고, 고치는 방향(② 시작 때 `running` 행을 먼저 넣을지, job 에 단계를 둘지)은 문서가 정할 몫이다.

### W-3. `finalBatchState` 가 14곳에 남았다 — SPEC 은 09-07 에 지웠다

- **어긋난 문서**: SPEC-008 §7 변경 이력 **#3** — 「SPEC-006 · 007 의 「통합본」 · 「종료 시 배치」 · 「다시 생성」 · **`finalBatchState`** · `pendingChange` · `sourceHumanLineId` | 2026-09-07 같은 발주에서 지웠다」. `pendingChange` · `sourceHumanLineId` 는 이 발주가 깨끗이 걷어냈는데 `finalBatchState` 만 남았다.

| 파일:줄 | 성격 |
|---|---|
| `app/back/dto/meeting.py:174` · `:185` | DTO 필드 `final_batch_state: str \| None` |
| `app/back/schemas/meeting.py:465` · `:484` · `:534` | 응답 스키마 필드 + 매핑 — **API 가 아직 내보낸다** |
| `app/back/service/meeting_service.py:189` · `:214` · `:222` · `:223` | `_final_batch_state()` 조회 함수 + 호출 |
| `app/back/service/meeting_batch_service.py:420` | 주석 — 「AI 탭 안내 바 「종결 정리 실패」의 원천(`finalBatchState`)」. **「종결」 어휘까지 남아 있다**(MF-56 로 사라진 말) |
| `app/back/repository/meeting_batch_run_repository.py:54` | docstring — 「`finalBatchState`(`phase='final'`) · `mergedSummary.integratedAt`(`phase='integration'`) 의 원천」. **셋 다 사라진 것을 가리킨다** |
| `app/back/tests/test_meeting.py:66` | 응답 단언 |
| `app/front/src/features/meetings/types.ts:150` · `closeFixtures.ts:83` · `:93` · `testUtils.tsx:67` | 타입 + 픽스처 |

- **프론트는 읽지 않는다** — 타입·픽스처 밖에서 `finalBatchState` 를 참조하는 코드가 0건이다(확인함). 백엔드가 빼면 프론트는 네 줄만 지우면 된다.
- 브리프 지시대로 **판정은 WARN**(제거 대상 · 코디가 수정 발주).

### W-4. 테스트 공백 셋

| 빈 것 | 왜 |
|---|---|
| **② 진행 중 창의 `progress.phase`** | `test_progress_phase_is_transcription_then_final`(`:625`)이 보는 것은 **파이프라인 전**(`transcription`)과 **완료 후**(`final`) 둘뿐이다. ② 시도 1 이 도는 동안을 보는 단언이 없어 W-2 가 안 잡혔다 |
| **job 상한 「넘겼을 때」 동작** | 워커 보고 10 대로 `test_meeting_finalize.py` 에는 수치 단언(`:609`)만 있고 동작은 `test_job.py` 하나가 본다. 두 벌이 대역 handler 로 부딪혀서인데, 결과적으로 **회의 마감(`on_timeout` → `ended`+`failed` + 토큰 폐기)** 을 finalize 쪽 맥락에서 보는 테스트가 없다 |
| **실측 증거** | Phase 1 「서버 로그에 `stt-async-v5` 호출과 `context.general` · `terms` 비움」은 코드·단위 테스트로만 확인됐다. WP Phase 0~3 의 `Status`·`완료 증거` 는 `TODO`·`미작성` 그대로다(앱 창 · 300분은 아침 항목이라 제외) |

---

## 4. 문서 공백

| # | 자리 | 무엇이 비었나 |
|---|---|---|
| **D-1** | SPEC-008 U-2 실패 배너 「사유 툴팁」 + §4 `MeetingDetail` | **새로고침으로 실패 화면에 들어오면 사유가 없다.** U-2 표는 사유의 출처를 `job.errorCode` 로 적었는데, `activeJobId` 는 `queued`/`running` 인 job 만 가리키므로(§4 Data Contract) 종결된 job 을 다시 읽을 길이 없다. 프론트는 폴링 훅의 React state 로 들고 있다가 배너에 주므로 **같은 세션에서만** 뜬다(`useMeetingFinalizeJob.ts:42-43`). 배너·「다시 시도」는 정상이고 툴팁만 빈다. 사유를 항상 보여야 한다면 상세 응답에 필드가 필요하다 — **결정을 만들지 않았다** |
| **D-2** | SPEC-008 §4 `progress.phase` 파생 규칙 · WP §Internal Interface 같은 행 | 「`final` = 그 회의에 `meeting_batch_run(phase='final')` 행이 생긴 뒤」라는 규칙이 **「② 가 지금 돌고 있다」를 표현하지 못한다** — 그 행은 시도가 끝나야 생긴다. U-1 이 요구하는 두 단계가 ② 가 한 번 실패해야만 성립한다(W-2 의 뿌리). 행을 시도 **시작**에 넣을지, job 에 단계를 둘지, U-1 을 고칠지가 정해져 있지 않다 |
| **D-3** | SPEC-007 U-4 / SPEC-008 — AI 탭 안내 바 문구 | 시안 문구는 「배치 n회 반영 · **HH:MM**」인데 그 시각의 원천이 상세 응답에 없다(`integratedAt` 은 MF-56 으로 사라졌고 회의 중 화면이 세던 값이라 재진입하면 없다). 프론트는 다른 시각을 끌어다 쓰지 않고 **시각 없이** 그린다 — 합리적이나 문서에 근거가 없다 |
| **D-4** | `system/README.md` §외부 연동 Soniox 행 · SYS-OQ-5 | ① **300분 실물이 없다** — SYS-OQ-5 는 62초 파일로 답했고(받는다 ✓) 상한 1200초는 그 규모에서 다시 볼 값이다. ② **재전사 출력이 비결정이라는 사실**(같은 파일 2회에서 토큰 시각이 흔들려 블록이 5개/6개로 갈렸고 문장부호 하나가 따로 블록이 됐다 — 증거 파일)이 어느 문서에도 없다. 계약(화자 변경 · 300자 · 2초)은 어긋나지 않지만 「재전사 결과가 결정적이다」를 전제하면 안 된다는 것은 남는 사실이다 |

---

## 5. WP 검증 항목 ↔ 테스트 대응표

**Phase 0 — 리비전 · 모델 · enum**

| 검증 항목 | 테스트 |
|---|---|
| 0008 왕복 · `pending_change` 값이 `payload` 로 살아 옮겨진다 | `test_migrations.py:112` |
| `source_*` 컬럼 · FK · 부분 UNIQUE 2 · CHECK 가 DB 에 없다 | `:136` · `:158` · `:164` |
| `term_corrections jsonb` · `job.error_code` 5종 · `batch_run.phase` 에 `integration` 없음 | `:193` 외 |
| 정적 — 옛 이름 0건 | `test_meeting_finalize.py:662`(needle 8종) · FE `static.test.ts` ㉒ |

**Phase 1 — ① async 재전사**

| 검증 항목 | 테스트 |
|---|---|
| 실시간 블록이 전부 사라지고 재전사 블록만(한 트랜잭션) | `:71` |
| `context.general` 셋 · `terms` 비움 | `:95` |
| `text` = 직전 회의 `ai_headline`(없으면 키 생략) | `:111` |
| **① 실패 → ② 미호출**(codex 0 · `merged` 0) | `:135` + 정적 `:704` |
| 블록 경계가 한 함수 | 정적 `:682` |
| `at_ms` 기준 동일 | 증거 파일(실물) + `:71` |
| SYS-OQ-5 | `work012-sys-oq5-evidence.md` — **받는다**(토큰 307 · 9.1초 · 화자 셋) |

**Phase 2 — ② 최종 회의록**

| 검증 항목 | 테스트 |
|---|---|
| codex 호출이 종료 후 **한 번** | `:169` |
| 프롬프트가 재전사 스크립트뿐 | `:185` |
| `merged` 가 사람 안건 전부 미러 · `state` 복사 | `:203` |
| 사람 안건 누락 → 그 시도 실패 | `:219` · `headline` 위반 `:235` |
| **BE §12 8** — 3회 실패 → `ended`+`failed` · 나머지 그대로 | `:250` |
| 전부 타임아웃 → `final_timeout` | `:269` |
| `ai_session_id` 없음 → 시도 실패(재웜스타트 0) | `:282` |
| AI 트랙 불변 | `:304` |
| `auto` 치환 · `guess` 본문 불변 · 표 밖 치환 0 | `:337` · `:359` |
| 줄 단위 완화 4종(강등 · 유형 `null` · `status` 제거 · 논의 줄 `payload` 버림) | `:377` `:392` `:412` `:430` |
| 원자성 | 정적 `:447` + 행동 `:471` |
| 토큰 — 종결 뒤 0건 · 폐기 실패 무해 · `/finalize` 재발급 하나 | `:495` `:513` `:572` |
| `mergedSummary` 다섯 · `integratedAt` 없음 | `:528` |
| `/finalize` 202/409 · ①부터 | `:551` |
| job 상한 2400 | `:609`(수치) · 동작은 `test_job.py` |
| `progress.phase` | `:625` — **② 진행 중 창은 안 본다**(W-4) |
| 정적 — 폐기 이름 0 · 스키마 하나 · 블록 상수 하나 · 두 번째 직렬화 0 · ① 실패 팔 · headline writer | `:662` `:678` `:682` `:693` `:704` `:714` |

**Phase 3 — 프론트**: FE 보고의 단언 목록과 `static.test.ts` ㉒(신설 4) · ⑲(갱신)로 U-1 · U-2 · U-4 검증 항목이 전부 덮인다. 카운트 다섯은 **DOM 에서 세어 `mergedSummary` 와 대조**한다.

---

## 6. 요약

**파이프라인이 계약대로 섰다.** `run_pipeline` 에 스위치가 없고 ① 실패는 두 갈래 모두 그 자리에서 끝난다 — 정적·행동 테스트가 둘 다 잠근다. ② 는 최대 3회이고 성공 트랜잭션이 `session_scope()` 하나에 여섯 쓰기를 담는다. 외부 호출(Soniox 폴링 · codex 대기) 어느 쪽에도 세션이 걸려 있지 않다. 검증 함수는 WORK-011 것 하나이고 `fill_final=True` 가 구현돼 011 검수의 W-3 이 닫혔으며, 스키마 파일도 한 벌이다. 토큰은 종결마다 best-effort 로 지워지고 `/finalize` 가 `/start` 와 같은 함수로 하나만 다시 발급한다. 폐기 대상 일곱(merge service · integration 스키마 · `run_final` 계열 · `_agenda_rows` · `BatchPhase.INTEGRATION` · `find_ai_agenda_by_source`)이 소스에서 완전히 사라졌고, 011 검수 WARN 넷 중 코드에 걸린 둘이 해소됐다. 프론트는 013/014 파일을 rename 외에 건드리지 않았다.

닫아야 할 것은 넷이다 — ① **W-1** `except Exception` 하나와, 그것을 포함해 **정적 가드 둘이 대체 없이 삭제된 것**(가드를 되살리거나 문서에 예외를 적어야 한다) ② **W-2** 성공 경로에서 ② 단계 문구가 안 보이는 것(뿌리는 D-2 의 파생 규칙이다) ③ **W-3** `finalBatchState` 14곳 ④ **W-4** 테스트 공백 셋. 어느 것도 커밋을 막을 무게는 아니지만, W-1 과 W-2 는 **문서 결정이 먼저** 필요하다.
