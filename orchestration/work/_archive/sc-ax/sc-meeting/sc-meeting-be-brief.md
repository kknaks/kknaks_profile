# [backend] WP-001 — 회의·안건·줄 도메인 + 상태 여섯 + 회의 API

너는 **sc-ax `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (branch `kknaksss/sc-meeting`, base `origin/main` a0bcee8 → PR `main`)

⚠ **같은 워크트리에서 frontend 워커가 `frontend/` 를 병렬로 고친다. `frontend/` 는 읽기만, 절대 쓰지 마라.** 너는 `backend/` 만 쓴다.

## 1. SSOT — 먼저 읽을 것

- **SPEC**: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/20-spec/spec-004-meeting-note.md` (0.4.1) — §3 Meeting·참석·열람 · §4 안건·줄 · §5.1 상태 여섯 · §10 Functional Rules · §11 현행과의 차이. **여기 없는 건 발명하지 마라.**
- **WP**: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/30-work/work-001-meeting-agenda-domain-api.md` — Scope·Interface Contract·Phase 1~3 검증이 완료 조건이다.
- **현행 코드 사실**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/survey-01-ai-provider-report.md` §4(현행 5단계)·§6.2 — 무엇이 남고 무엇이 폐기되는지.
- **화면 정본**(응답이 무엇을 채워야 하는지의 근거): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/design/회의록.dc.html` · `회의실.dc.html` — 읽기만.
- 아키텍처 경계: 워크트리의 `backend/tests/architecture/` · `docs/domain-model.md`(read-only).

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

현행 회의 모듈(`modules/meetings/`)은 note 를 version 으로 쌓고, AI 요약을 「채택」해 붙이고, 실시간 전사를 임시로 두고 파일을 재전사한다. 새 계약은 **회의록 = 안건 > 줄 목록**, **상태 여섯**, **판 없음(덮어쓰기)**, **참석자만 열람**이다. 이 WP 는 그 바닥(도메인·스키마·회의 API)만 세운다. 스트림·AI 배치·합성·자료·공유는 다음 WP 다 — **건드리지 마라.** 단, 이 WP 가 그 다섯의 바닥이므로 모델에 `track`·`evidence` 같은 자리는 지금 열어 둔다(§3 계약).

폐기 대상(survey-01 §11.1·WP §Code Surface): note version 계열(`meeting_notes`·`meeting_note_versions`), `adopt_summary`, realtime credential·segment 경로, 파일 재전사 경로. **이 WP 에서는 회의 API 가 그것들을 더 이상 노출하지 않게 하고 스키마에서 note version 을 제거한다.** 스트림·전사 코드 자체 삭제는 WP-002 가 한다 — 지금은 라우터에서 떼어내고 import 가 깨지지 않을 만큼만.

## 3. 계약 (frontend 워커와 합의됨 — 이대로 제공. 필드명 바꾸지 마라)

상태 wire 값(OQ-301 — 코디 확정): `scheduled` · `in_progress` · `summarizing` · `done` · `failed` · `cancelled` (화면 라벨 예정·진행 중·정리 중·완료·실패·취소됨).

```
GET  /api/meetings
  → { "upcoming": [MeetingRow...], "past": { "items": [MeetingRow...], "next_cursor": str|null } }   // past 20건/페이지, ?cursor=
MeetingRow = { meeting_id, title: str|null, starts_at, ends_at, location: str|null, status,
               viewer_relation: "attendee"|"shared", created_by: member_id, attendee_count: int }

GET  /api/meetings/{id}   → MeetingDetail  (참석자·공유받은 사람 외 404)
MeetingDetail = { meeting: { meeting_id, title, purpose: str|null, starts_at, ends_at, location, status,
                             created_by, attendees: [{member_id, display_name}], external_attendees: [str],
                             viewer_relation, can_edit_info: bool, can_edit_note: bool, last_saved_at: ts|null,
                             carried_from_meeting_id: str|null },
                  agendas: [Agenda...] }
Agenda = { agenda_id, order: int, title, source: "manual"|"carried"|"ai", concluded: bool,
           lines: [Line...], todos: [Todo...] }
Line  = { line_id, track: "memo"|"ai"|"final", order: int, text, author: member_id|null,
          evidence: [{start_ms, end_ms}] }        // WP-003/004 가 채움. 이 WP 는 빈 배열
Todo  = { todo_id, text, assignee_candidate: str|null, due_candidate: date|null, linked_task_id: str|null }  // WP-004 가 채움

POST /api/meetings            body { title, purpose?, starts_at, ends_at, location?, attendee_ids: [], external_attendees?: [],
                                     agendas?: [{title}], carried_from_meeting_id? }  → 201 MeetingDetail (status scheduled)
POST /api/meetings/quick-start  body {}  → 201 MeetingDetail (status in_progress, title null, attendees [만든 사람])
PATCH /api/meetings/{id}      body { title?, starts_at?, ends_at?, location?, attendee_ids?, external_attendees? }
                                — scheduled·done 에서만(409). actor = 그 회의의 참석자(만든 사람으로 좁히지 않는다)
DELETE /api/meetings/{id}?scope=meeting|note   — scheduled 에서만. meeting → status cancelled. note → 회의록 줄·자료 삭제, 회의는 남음. 204
POST /api/meetings/{id}/start  → scheduled→in_progress   /   POST /api/meetings/{id}/end → in_progress→summarizing (전이만. 후속은 WP-004)
POST   /api/meetings/{id}/agendas          body { title }             → Agenda (source manual, 20개 초과 409)
PATCH  /api/meetings/{id}/agendas/{aid}    body { title?, concluded?, order? }
DELETE /api/meetings/{id}/agendas/{aid}    → 204 (줄·todo 함께 삭제)
오류: 권한 밖·존재 숨김 404 · 상태 불일치 409 · 검증 422. 응답에 storage key·provider ref 같은 내부 값 금지.
```

자동 취소(WP Scope): `ends_at` 이 지났고 줄이 하나도 없는 scheduled 회의 → cancelled. 줄이 생기면 해제. 스케줄러가 없으면 **조회 시점 판정**으로 구현하고 WP Open Issue 에 적어라.

## 4. 먼저 읽을 핵심 파일

- `backend/src/ax_workspace/modules/meetings/application.py` — 현행 `MeetingApplication`·`MeetingRepository` Protocol(31~135줄). 열람 판정 `_can_read_detail`·`list` 의 busy 투영은 **계승**(공유받은 사람은 shared 로).
- `backend/src/ax_workspace/platform/meetings.py` · `platform/persistence.py:248-520` — 회의 테이블 12개. note version·summary·refinement 계열이 폐기/이관 대상.
- `backend/src/ax_workspace/entrypoints/http.py` — `/api/meetings*` 16 라우트(539~780줄 부근).
- `backend/src/ax_workspace/entrypoints/reset_demo.py` · `bootstrap/scenario*.py` — 스키마 reset 과 시나리오가 새 모델을 알아야 한다(회의 3건 시딩이 깨지지 않게).
- `backend/tests/contract/test_meeting_core.py` · `test_meeting_followups.py` — 현행 계약 테스트. **바뀐 계약에 맞게 고치고**, 폐기 표면 테스트는 지운다.
- `backend/tests/architecture/test_architecture.py` — 경계 규칙.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/`
- `docker-compose.yml`
- `Makefile`
- (`frontend/` 는 **읽기 전용** — frontend 워커 소유)

## 6. 구현 단계 (WP-001 Phase 1→2→3 순서 그대로)

1. **도메인·스키마** — `MeetingAgenda`·`MeetingLine`(track·order·evidence JSON 자리)·`MeetingTodo` 신설, 상태 enum 여섯과 허용 전이를 도메인에서 강제(scheduled→in_progress→summarizing→done|failed, scheduled→cancelled, cancelled→scheduled 는 자동 취소 해제만, done→summarizing 없음). note version 계열 제거. `reset_demo` 가 새 스키마를 만든다(README 「스키마」 절 방식 — Alembic 아님).
2. **열람·조회** — 참석자/공유 판정 계승, 목록 두 구획(upcoming 전량·past 20건 cursor), 상세(안건+줄+todo 포함).
3. **생성·편집·취소** — 예약·quick-start·PATCH(actor=참석자, scheduled|done)·DELETE 두 갈래·start/end 전이·안건 CRUD·자동 취소 판정.
4. 데모 시나리오(`scenario_meetings` 계약)가 새 모델로 회의를 만들도록 맞춘다. 단 **dataset 폴더는 리포에 넣지 않는다.**
5. §8 검증 → 자기점검 → 완료 보고.

## 7. 범위 제약 — 하지 말 것

- 스트림·WS·Soniox·AI 배치·합성·자료·공유·화면을 만들지 않는다(WP-002~006). 관련 현행 코드는 **라우터에서 떼는 것까지만**, 파일 삭제는 WP-002.
- 계약(§3)의 필드명·경로·상태값을 바꾸지 않는다. 빠진 게 있으면 코디에게 묻는다.
- `frontend/` 수정 금지. 데이터 폴더·비밀값 커밋 금지. Alembic 도입 금지(리포 방식은 reset_demo).
- 회의실 「가능」 판정·the Connect·알림·일시정지 — 데모 범위 밖.

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> -m 'not integration' + uv run pytest -q tests/architecture (경계 테스트는 항상). 전체 스위트·integration 마커 금지 — 사용자 방침. 자기점검 — modules/*/domain.py·application.py 가 fastapi/mcp/sqlalchemy 를 import 하지 않는가 · entrypoints 가 platform 구현을 직접 import 하지 않는가 · 스키마 변경을 reset_demo 밖에서 하지 않았는가. 검증은 1회만
```

- 추가로 **WP-001 Phase 1~3 의 검증 체크리스트 각 항목을 테스트로 덮어라**(허용 안 된 전이 거부 · 안건 21번째 거부 · 안건 삭제가 줄 삭제 · 비참석자 상세 404 · 목록에 남의 회의 없음 · 진행 중 편집 409 · 참석자(비소유자) 편집 허용 · note 삭제가 회의 유지 · quick-start 참석자 없이 생성 · 자동 취소·해제).
- `make reset-demo` 가 새 스키마로 성공하는지 1회(로컬 postgres 54329 는 코디가 띄워 둠 — **다른 포트·프로세스 건드리지 말 것**, `make local-stack` 실행 금지).
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다. 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WP-001 회의 도메인·API" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수(§3 대비 차이 0 확인) / reset-demo 결과 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — WP-001. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
