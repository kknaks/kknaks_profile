# [backend] WP-004 — 종료 합성(같은 세션 · 줄 병합 · 다음 할 일 · 제목 후보 · 근거) + 후속업무 승격(업무 요청) + 내보내기(HTML)

너는 **sc-ax `backend` 워커**다. WP-001~003 을 한 세션이면 그 맥락을 쓴다. 역할 문서(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/backend/role.md` (+ `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (HEAD = WP-003 커밋, 코디가 방금 커밋 → PR `main`). ⚠ reviewer 가 같은 트리에서 HEAD 를 읽는다 — 커밋하지 마라(원래 금지). `frontend/` 읽기만.

## 1. SSOT

- **SPEC 0.4.1** — **§8 종료와 합성 · §8.1 중복 방지 · §8.2 Todo 값 · §9 승격 · §5.1 상태(summarizing→done|failed, failed→summarizing)**. `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/20-spec/spec-004-meeting-note.md`
- **WP-004** `30-work/work-004-final-merge-followup.md` — Scope·Domain·Phase 1~3 검증 = 완료 조건.
- **원형(task-management, 읽기만)**: `/Users/kknaks/git/toy_pr2/task_management/app/back/service/meeting_finalize_service.py`(종료→합성 job·실패 상태·재시도) · `meeting_batch_service.py`(`_parse_output`·`_final_payload`·`_demote_if_needed` — 최종에서만 차는 필드) · `ai_schemas/meeting_notes.json`(한 벌 스키마: `headline`·`payload` 는 회의 중 null, 최종에서 값).
- **WP-003 산출(실명)**: 세션 ref `MeetingApplication.ai_session_ref(meeting_id)`(`meeting_ai_sessions.provider_session_ref`, persona=만든 사람) · 회의 중 스키마 `modules/meetings/schemas/ai_batch_output.json`(**회의 중 전용 — 최종 스키마는 옆에 새 파일**) · 커서 `unprocessed_transcript_cursor` · `succeeded_batch_cursor` · `latest_succeeded_batch_seq` · 재사용 `batch.parse_output` · `batch.demote_line` · `application.replace_ai_track`(track 인자 넓혀 `final` 에) · 배치 스레드/lock 은 `MeetingBatchService`(`_spawn`·회의당 Lock) — 합성은 `/end` 뒤이므로 배치 lock 과 겹치지 않게 같은 lock 을 잡고 돈다. 리포트 `report-be-wp003.md`.
- **현행 승격·업무 요청 표면**: `entrypoints/http.py` `CreateWorkRequestRequest`(title·assignee_id·description·due_date·cc_member_ids·checklist·reference_task_ids) · `modules/work/requests.py` · `platform/work_tasks.py` · `persistence.py` `WorkRequestRecord`·`TaskRecord`(source_* 여섯 열).
- **코드 검수 이월**: 없음(WP-002/003 에서 소화).

## 2. 무엇을 만드나

`/end` 뒤 「정리 중」에서 **같은 AI 세션**으로 합성을 한 번 돌려 두 트랙을 **최종 줄(track final)** 로 합치고, **다음 할 일(Todo)** 을 뽑고, 제목이 비면 **제목 후보**를 내고, 근거를 타임칩으로 결박한다. 성공 → 「완료」, 실패 → 「실패」+`/finalize` 재시도. 승격은 **언제나 업무 요청**이고 출처 두 id 를 실어 보낸다. 마지막 저장분을 **HTML** 로 내보낸다.

## 3. 계약 (코디 확정)

- **종료 파이프라인**: `POST /end`(WP-001 소유, in_progress→summarizing, 즉시 응답) 뒤에 **durable job** `meeting.finalize` 등록(현행 `durable_jobs`·lease·fence 패턴 계승, WP-002 가 이미 스트림을 닫음). `bootstrap/meeting_worker.py` 가 잡을 claim → 합성 → 커밋. `POST /api/meetings/{id}/finalize` = 「실패」에서만 같은 잡 재등록(409 그 외).
- **합성 입력**: 확정 발화 전량(MeetingTranscript) · 메모 줄(track memo) · AI 트랙(track ai) · 안건 목록 · 이어진 이전 회의(있으면). **같은 provider 세션 resume**(WP-003 세션 ref). 세션이 없거나 죽었으면 **콜드 스타트**(맥락+전량을 한 번에 싣는 폴백) — 리포트에 횟수 남김.
- **최종 스키마**(WP-003 배치 스키마 **한 벌**에 최종 전용 필드 추가, strict): `{ title_candidate: string|null, agendas:[{agenda_id: string|null, title, source, concluded: bool, lines:[{text, evidence:[{from_ms,to_ms}], line_ids:[string]}], todos:[{title, description, due_candidate: string|null, checklist_candidate:[string], line_ids:[string]}] }] }`. 회의 중 배치에서는 `title_candidate`·`todos`·`concluded` 가 오면 버린다(WP-003 규칙 유지).
- **합성 규칙**(§8-5·§8.1·§8.2): 사람이 만든 안건은 하나도 빠지거나 합쳐지지 않는다(검증 실패 = 배치 폐기·「실패」) · 중복 접기 · **담당자 없음** · description 항상(2~4문장+근거 요약+마지막 줄 「회의 {제목} · 안건 N 에서」) · checklist 항상 2~5 · due 는 발화 날짜 → 이어진 다음 회의 전날 → null · **기존 업무와 같은 일이면 후보를 내지 않는다**(`task_list` 도구로 먼저 조회; 「같은 일」 판정은 제목 정규화 유사 + 같은 회의 참석자 담당 — 잠정, OQ-316) · 판단 안 서면 후보로 냄 · 근거 evidence 는 실재 확정 블록 구간만(밖이면 그 줄만 강등) · `concluded` 는 AI 가 채움(D17).
- **적재**: 트랜잭션 하나 — track final 줄 전량 교체 · meeting_todos 전량 교체(승격된 것은 유지) · 제목이 비어 있으면 `meetings.title_candidate`(새 컬럼)에 저장(사람이 머리 편집에서 확정) · `last_saved_at` · 상태 done. 실패는 failed + `failure_reason`.
- **줄 편집(완료·실패·취소됨, 만든 사람)**: **WP-001 의 `PATCH /agendas/{aid} {lines:[…]}` 덮어쓰기 하나로 간다.** 줄별 POST/PATCH/DELETE 는 만들지 않는다(문서 정렬은 planner 몫). 안건 단위 동시 저장 판정: `PATCH` 에 `expected_last_saved_at`(옵션) — 다르면 409 + 현재 줄 반환.
- **승격**: `POST /api/meetings/{id}/todos/{todoId}/promote` body `{assignee_id, title?, description?, due_date?, checklist?}`(모달에서 고친 값 우선, 없으면 후보값) → 내부에서 현행 업무 요청 생성 경로 호출(`CreateWorkRequestRequest` 필드 그대로 + `source_meeting_id`·`source_agenda_id`) → `linked.work_request_id` 저장 → 응답 Todo. 중복 승격 409. `DELETE /api/meetings/{id}/todos/{todoId}` 후보 삭제(확인 없음, 승격된 것은 409). **work 모듈 변경(D20)**: `work_requests.source_meeting_id·source_agenda_id`, `tasks.source_meeting_id·source_agenda_id`, `origin_kind="meeting"`, 수락 시 요청→업무로 두 열 복사. 이건 SPEC-001 소유 표면이라 **최소 변경 + 기존 work 테스트 회귀 0**.
- **내보내기**: `GET /api/meetings/{id}/export?format=html` — 마지막 저장분(회의 정보·안건별 최종 줄·다음 할 일). **pdf·docx 는 데모 범위 밖**(코디 결정 — 의존성 추가 없이 불가) → 400 `unsupported_format`. planner 가 §2.2 에 내린다.

## 4. 먼저 읽을 파일

- 원형 `meeting_finalize_service.py` 전문 · `meeting_batch_service.py` 의 최종 분기 · 스키마 파일.
- `bootstrap/meeting_worker.py`·`modules/jobs/domain.py`(durable job kind 추가) · `modules/meetings/application.py`(WP-001~003 결과) · `platform/persistence.py`(todos·lines·title_candidate·source 열).
- `modules/work/requests.py` · `platform/work_tasks.py` · `tests/contract/test_work_*`(회귀 기준).

## 5. allowed_paths

- `backend/` · `docker-compose.yml` · `Makefile`. `frontend/` 읽기 전용.

## 6. 단계 (WP-004 Phase 1→2→3)

1. `/end` 훅 → finalize job · worker claim · 상태 전이(summarizing→done|failed, failed→summarizing via `/finalize`) · 세션 resume/콜드 폴백.
2. 최종 스키마·파싱·검증(사람 안건 보존·근거 실재·중복 방지 도구 조회)·전량 교체 적재·제목 후보·todos.
3. 승격 API(+work 모듈 두 열·origin_kind·수락 시 복사) · 후보 삭제 · 줄 덮어쓰기 동시성 · HTML 내보내기.
4. §8 검증 → 완료 보고(FE 인계: promote/delete/export 경로·title_candidate 필드·expected_last_saved_at).

## 7. 하지 말 것

- 회의 중 배치(WP-003)·자료·공유(WP-005)·화면 금지. 줄별 엔드포인트 금지. pdf/docx 금지. 담당자 추측 금지. 회의록에 업무 링크 금지.
- 실제 Codex/MCP 호출 테스트 금지(대역). Alembic 금지. `make local-stack`·5176/8001 금지. `make reset-demo` 1회 허용.

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> -m 'not integration' + uv run pytest -q tests/architecture + 기존 work 계약 테스트(회귀 0). 전체 스위트·integration 금지. 자기점검 — modules/* 경계 · reset_demo 밖 스키마 변경 없음. 검증 1회
```

- WP-004 Phase 1~3 검증 항목 전부 테스트: `/end` 즉시 응답+job 등록 · 실패→failed→`/finalize` 재시도 · 사람 안건 누락/병합 시 실패 · 중복 접기 · 담당 없음·description/checklist 항상·due 세 갈래 · 기존 업무 있으면 후보 없음 · evidence 밖 강등 · 제목 후보 저장 · 승격이 업무 요청 생성 + 출처 두 열 + linked · 자기 자신 담당도 요청 · 중복 승격 409 · 수락 시 task 에 출처 복사 · 줄 덮어쓰기 409 동시성 · export html.

## 9. 완료 보고 — **문구 변경 금지**

> ⚠ 핸들은 dispatch preamble 값 우선.

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: WP-004 합성·승격·내보내기" \
  --body "변경 파일 / 구현 요약 / 검증 수치(+work 회귀) / 계약 준수 / FE 인계(경로·필드) / 콜드 폴백 여부 / reset-demo / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — WP-004. 상세는 인박스." --enter
```
