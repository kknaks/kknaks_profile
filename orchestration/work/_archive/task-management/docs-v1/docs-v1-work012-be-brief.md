# [backend] WORK-012 Phase 0~2 — 리비전 0008 · async 재전사 · 최종 회의록 한 번 · 용어 치환 · 토큰 폐기

너는 **task-management `backend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`). **WORK-009 · 010 · 011 이 들어와 있다** — `git log -4`. WORK-011 이 만든 `ai_schemas/meeting_notes.json` · `_parse_output(fill_final=)` · `_demote_if_needed` · `_persist` 를 **그대로 쓴다**(복제 금지).

문서는 전부 **코디 워크트리 절대경로 · 읽기 전용**이다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-012-meeting-close.md            ← 네 빌드 계획. **Phase 0 · 1 · 2**(3 은 프론트 — 다른 발주). Code Surface · Internal Interface(파이프라인 · context · 블록 · 검증 함수 하나 · 원자성 · 토큰 폐기) · Phase 검증
  20-spec/spec-008-meeting-close.md §4         ← API 표(/end · /jobs · /finalize) · Request/Response · Validation · Case Matrix · **「수치」 표** · **「종료 파이프라인 — 검증 가능한 정의」 표** · 「② 의 context」 · 「② 출력의 최종 전용 필드」 · 「서버 검증」 표
  20-spec/spec-008-meeting-close.md U-1 · U-2  ← 생성중 · 실패 배너(백엔드가 주는 값 — progress.phase · errorCode)
  10-decision/decision-003-meeting-notes.md    ← §4 종료 파이프라인 · 최종 회의록 작성 · 재시도 · §6 STT 용어 보정 · §7 실패 · §STT 재전사 모델
  40-architecture/backend/README.md            ← §5-3 · §6 · §7(외부 호출 중 트랜잭션 0) · §8-1 · §8-3 · §12 테스트 8
  40-architecture/database/domains/meeting.md  ← M-8 · M-8-a · M-9-a · M-9-b · M-19 · 컬럼 변경 표(payload · term_corrections · source_* 삭제 · phase)
  40-architecture/system/README.md             ← External Integrations Soniox stt-async-v5 행 · 흐름 ③ 종료 절 · 불변식 3 · 7 · 11 · 12
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/ai-prompt-draft.md §C   ← 최종 프롬프트 초안. 「AI 요약 트랙을 전체 재정리」 문구는 쓰지 않는다 — 최종은 merged 트랙(WP §Open Issues)
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/Meeting flow.md §3-2   ← MF-37 · 52 · 54 · 56 · 57 · 58 · 59 · 70
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/soniox-study.md   ← Soniox async API 사실
```

## 1. 범위 — Phase 0 · 1 · 2 (백엔드만)

```
Phase 0  리비전 0008 — pending_change → payload RENAME + CHECK · source_human/ai_line_id + 부분 UNIQUE 2 + CHECK 삭제 · meeting.term_corrections jsonb · batch_run.phase CHECK incremental|final · job.error_code 5종
         models · dto/enums(JobErrorCode 5 · JobPhase transcription|final · BatchPhase.INTEGRATION 삭제) · schemas/dto payload 키 · MergedSummary 다섯(integratedAt 삭제)
Phase 1  integrations/soniox.py async 갈래(files → transcriptions → 5초 폴링 → transcript · SttUpstreamError · install_async_connector)
         service/meeting_transcript_blocks.py 신설 — 블록 묶기 한 함수(화자 변경 · 300자 · 2초). meeting_stream_service 위임
         meeting_finalize_service._transcribe() — context(general 3 · text 직전 회의 headline · terms 비움) · meeting_transcript DELETE+INSERT 한 트랜잭션 · 폴링 사이 세션 0
         config.py 수치(1200 · 5 · 300 · 3 · 2400) · job_service progress.phase 파생
         **실물 확인 1건** — 실제 녹음 webm(헤더 없음) 1개를 stt-async-v5 에 올려 본다 ($0.10 · SONIOX_API_KEY 는 .env 에 있다)
Phase 2  meeting_finalize_service 재작성 — integrate() → finalize() · run_pipeline = ① → ② 한 번(스위치 없음) · _attempt_final · _commit_success(한 트랜잭션) · _commit_failure · build_final_notes_prompt
         _parse_output(fill_final=True) · _persist(track='merged') 확장 · 최종 전용 검증 5 · grade='auto' 치환 · revoke_meeting_token 종결 시
         폐기 — meeting_merge_service.py · ai_schemas/meeting_integration.json · run_final · _run_final_once · _load_final_input · build_final_prompt · _agenda_rows · test_meeting_merge.py
         meeting_router /integrate → /finalize
```

**Phase 3(프론트)는 다른 워커다. `app/front/` 를 건드리지 마라.**

## ⛔ 2. 하지 말 것 · 이미 있는 것

```
fallback 금지          ① 실패 → ② 로 가는 코드 경로가 있으면 반려(MF-58). 실시간 블록으로 최종을 만들지 않는다
검증 함수 하나          _parse_output · _demote_if_needed · _persist 는 WORK-011 것. 확장(fill_final · track)만. 두 번째 파서·두 번째 persist 금지
스키마 파일 하나        meeting_notes.json — 읽기만. 새 파일 금지. meeting_integration.json 은 폐기
외부 호출 중 트랜잭션 0  Soniox 폴링 사이 · codex 대기 중 세션을 잡지 마라(BE §7). 읽기 → commit → 외부 → 새 세션에서 쓰기
원자성                 ② 성공 = merged INSERT + ai_headline + term_corrections + auto 치환 + ended/succeeded + batch_run(final) + job 이 한 트랜잭션. 중간 예외면 전부 없음
AI 트랙 불변            종료 전후 track='ai' 행이 바뀌지 않는다(MF-56)
speaker_label 불변      용어 치환은 content 문자열만. guess 는 본문 불변. 표에 없는 치환 없음
ai_session_id NULL      ② 그 시도 실패(final_failed). 재웜스타트 갈래 없음(MF-70)
payload 표면            컬럼만 만든다. POST/PATCH lines 의 payload 갈래 · 드로어 · 「넣기」 는 WORK-013
except Exception · 임의 재시도(② 는 정확히 2회 재시도 · ① 은 0회) · 조용한 기본값 금지
```

**WORK-011 검수(`work011-review-report.md`) 에서 넘어온 것 — 이 발주에서 닫는다**
```
fill_final=True 의 뜻      _parse_output(fill_final=True) 는 지금 NotImplementedError 다. 너가 구현한다 — 회의 중(False)은 headline·termCorrections 를 버리고(null) 안건 목록만, 최종(True)은 셋을 다 돌려준다. 반환 형태는 한 함수가 두 모드로 — 두 번째 파서 금지
build_final_prompt 잔재    WORK-011 이 컴파일만 되게 두 문장을 새 스키마로 바꿔 둔 「부분 이관」 상태다. 옛것을 참고하지 말고 build_final_notes_prompt 를 WP §Internal Interface 대로 새로 쓴다. **「새로 드러난 것만」·「추가할 줄」 문구 0** — 최종은 사람 안건 전부를 정확히 한 번씩 · AI 트랙 전체(MF-53 · 초안 §B 의 그 문장은 폐기됐다)
죽은 함수                meeting_child_repository.find_ai_agenda_by_source 는 호출 0건이다. 최종 경로에서 쓰면 쓰고, 안 쓰면 이 발주에서 지운다(남기면 반려)
같은 직렬화 정적 검사      ai.batch 프레임과 상세 응답 agendas.ai 가 같은 함수(meeting_service.build_tracks)를 지나는지 행동 검사만 있다. 정적 검사(테스트에서 두 번째 직렬화 함수 0) 하나 추가
```

## 3. 계약

- **`run_pipeline(job)` = ① → ②.** `/end` 도 `/finalize` 도 ①부터. `_plans` 스위치 폐기
- **①** `transcribe(meeting_id)` — 상한 1200초 · 폴링 5초 · 실패/상한 → `transcription_failed|transcription_timeout` 즉시 종결. `context.general` = 회의 제목 · 프로젝트 · 화자 수(실시간 speakerCount) / `context.text` = 같은 프로젝트(무소속이면 무소속) 직전 `ended+succeeded` 회의의 `ai_headline`(없으면 키 생략) / **`context.terms` 비움**. 결과 sub-word 토큰 → `meeting_transcript_blocks.build_blocks()`(실시간과 같은 함수) → DELETE + INSERT
- **②** `attempt_final` — `gateway.run(prompt=build_final_notes_prompt(script), session_id=ai_session_id, output_schema=OUTPUT_SCHEMA(meeting_notes.json), timeout_sec=300, meeting_token=get_meeting_token)` × 최대 3회. `_parse_output(fill_final=True)` + 최종 전용 검증 — ① 모든 사람 안건이 `humanAgendaId` 로 정확히 한 번 ② `headline` 1~200 한 문장 필수 ③ `termCorrections` 배열 · `grade ∈ {auto,guess}` ④ 페이로드 참조(유형·프로젝트·연관 업무 본인 삭제 안 된 것 — 틀리면 그 키만 null) ⑤ `payload.status ∈ {todo,in_progress}` — `done`·`cancelled` 면 그 키 제거. 업무 참조 사후 검사는 WORK-011 함수(그 줄만 action 강등)
- **미러 안건 state** — `source_agenda_id` 의 사람 안건에서 복사. AI 신설은 둘 다 NULL
- **토큰 폐기** — ② 종결(성공·실패) 뒤 `revoke_meeting_token` best-effort · 실패해도 job 결과 불변
- **`progress.phase`** 파생 — ① 도는 동안 `transcription` · `meeting_batch_run(phase='final')` 생기면 `final`
- **`mergedSummary`** 파생 다섯 · `integratedAt` 없음
- **수치** — `meeting_transcribe_timeout_sec=1200` · `meeting_transcribe_poll_sec=5` · `meeting_final_timeout_sec=300` · `meeting_final_attempts=3` · `meeting_job_timeout_sec=2400`. 옛 `meeting_final_batch_timeout_sec` · `meeting_integration_*` 폐기

## 4. allowed_paths

```
app/back/   .env.example
```
`app/front/` · 문서 · compose · `app/mcp/` 금지.

## 5. 검증

WP §Execution Phase 0 · 1 · 2 의 검증 체크리스트 전부. 특히

- Phase 0 — 리비전 왕복 · `pending_change` 값이 `payload` 로 살아 옮겨짐 · `\d meeting_line` 에 `source_*` 없음 · 정적 `pending_change|pendingChange|source_human_line_id|source_ai_line_id|integration_failed|FINAL_BATCH` 0(back 만 — 프론트는 Phase 3)
- Phase 1 — **SYS-OQ-5 실물**: 헤더 없는 webm 을 `stt-async-v5` 가 받는가. 받으면 그대로. **거절하면 응답 코드·본문을 보고에 적고 컨테이너를 바꾸지 마라**(사용자 결정). 재전사 뒤 실시간 블록 0 · `at_ms` 기준 동일 · 300자/2초 상수 한 파일 · 키 막으면 `transcription_failed` + ② 호출 0 · 정적: `_transcribe` 실패 뒤 `attempt_final` 0
- Phase 2 — **BE §12 8** · codex 호출 종료 후 1회 · AI 트랙 행 불변 · `auto` 치환 · `guess` 불변 · `speaker_label` 불변 · 사람 안건 누락 → 시도 실패 · 밖 taskId → 줄 강등 · 삭제된 유형 → 키 null · `done` → 키 제거 · 성공 트랜잭션 원자성(중간 예외 → 전부 없음) · `/finalize` 는 `ended+failed` 만 202 · job 2400 · 토큰 행 0 · 정적: `meeting_merge_service|meeting_integration.json|run_final|build_final_prompt|_agenda_rows|BatchPhase.INTEGRATION` 0 · `NotImplementedError` 0(`meeting_batch_service`) · `find_ai_agenda_by_source` 0 또는 호출 ≥1 · 최종 프롬프트 본문에 `새로 드러난|추가할 줄` 0

```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1 && make test    # 전체 · Errors 0
```

막히면 30분 넘기지 말고 §9 (2) 로 물어라. 특히 **Soniox async 가 webm 을 거절하면 즉시 보고** — 그건 결정이지 네가 고칠 게 아니다.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_fd9fc1ce-619d-4f87-b218-10dfaefaa275 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WORK-012 Phase 0~2" \
  --body "변경 파일 목록 / Phase 별 구현 요약 / SYS-OQ-5 실물 결과 / 검증 결과(수치 · 정적 검사 grep) / 계약 준수 / 미결·주의점"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] backend 완료 — WORK-012 회의 종료 백엔드. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] backend: <질문>" --enter`
