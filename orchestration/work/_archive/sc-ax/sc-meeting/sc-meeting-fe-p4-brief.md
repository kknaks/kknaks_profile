# [frontend] WP-006 Phase 4 — 회의 뒤 화면 실계약 배선: 스크립트 원문 · 근거 점프 · 승격·후보 삭제 · 다시 시도 · 내보내기 · 제목 후보 · 동시 저장 409

너는 **sc-ax `frontend` 워커**다. WP-006 P1~3 을 한 세션이면 그 맥락을 쓴다. 역할 문서(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/frontend/role.md` (+ `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (HEAD = **8397d8f** WP-004 커밋 → PR `main`). backend 워커가 같은 트리에서 후속(E1~E6)을 고친다 — `backend/` 읽기만, 커밋 금지. `backend/` 읽기만 — **서버가 이미 있다. 모킹 대신 `entrypoints/http.py` 의 실제 응답 모양을 읽고 맞춰라.**

## 1. SSOT

- **SPEC 0.4.1** `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/20-spec/spec-004-meeting-note.md` — **§5.1 상태표 · §5.4-7 스크립트 · §8-9 줄 편집(안건 덮어쓰기·409) · §8-10 내보내기 HTML · §8.1 Todo 8필드 · §9 승격(언제나 업무 요청) · §13 OQ-311**.
- **WP-006** `30-work/work-006-meeting-screens.md` **Phase 4**.
- **시안(정본)** `orchestration/work/sc-meeting/design/회의실.dc.html` 정리 중·완료·실패·취소됨 상태 · `REPORT-회의실-v2.md` 가시성 표(E31 근거 칩 → I05 스크립트 점프 · E54/E55 실패 안내+다시 시도 · 「요청됨」).
- 네 P3 리포트 `orchestration/work/sc-meeting/report-fe-p3.md` §7 미결 1~5 — 이번에 닫는다.

## 2. 계약 (BE 가 구현한 실물 — 코디 e2e 로 확인, 이름은 `http.py` 에서 재확인)

- **실물 확정 모양**: `PATCH /agendas/{aid}` body `{lines: string[], expected_last_saved_at, title?, concluded?}` — **lines 는 문자열 배열**(줄 객체 아님) · 409 응답 `{detail:{code:"meeting_agenda_stale", current:<Agenda>}}` · `Agenda.last_saved_at` 실림 · `meeting.title_candidate: string|null` · `meeting.failure_reason: string|null` · export 미지원 format **422** · promote 201 Todo(`linked.work_request_id`) · 승격은 지금 참석자 교차 조직이 422 인데 BE 후속(E4)이 참석자 예외로 연다 — 화면은 422 를 오류 문장으로 보이면 된다.

- **`GET /api/meetings/{id}/transcript`** → `{items:[{id, speakerLabel, atMs, endMs, content}], memos:[{line_id, agenda_id, text, author, atMs}]}`. 열람 = 참석·공유. 끝난 회의(정리 중·완료·실패)의 「스크립트」 탭은 이걸 읽어 같은 시각 축에 발화+메모를 그린다(GutterList). 예정·취소됨엔 탭 없음.
- **`Line.at_ms`**(memo 줄 서버 경과 ms) · **`can_write_memo`** · **`meeting.started_at`** — P3 의 `created_by` 판별과 `Date.now() − startedAtMs` 자체 계산(MeetingDetailPage.tsx:807, 검수 4 W-a)을 서버 값으로 대체. viewModels 에 세 필드 추가.
- **`meeting.title_candidate`** — 제목이 비어 있고 후보가 있으면 머리에 후보를 흐리게 보이고, 연필 편집에서 저장하면 title 이 된다(후보는 비워짐). 문구는 시안대로.
- **줄 편집 저장** = `PATCH /api/meetings/{id}/agendas/{agendaId} {lines:[…], expected_last_saved_at}` — 409 면 서버가 준 현재 줄로 갈아 끼우고 「다른 곳에서 먼저 저장됐다」 표시(문구 OQ-311 임시, 표에 추가).
- **승격** `POST /api/meetings/{id}/todos/{todoId}/promote` body `{assignee_id, title?, description?, due_date?, checklist?}` → Todo(`linked.work_request_id` 채워짐). **CreateWorkDrawer 는 계속 열되(prefill 그대로), 제출을 `POST /api/work-requests` 직접이 아니라 promote 로 보낸다** — 드로어의 onSubmit 을 주입 가능하게 만드는 최소 변경(다른 화면의 드로어 동작은 그대로). 성공 후 행이 「요청됨」. 중복 승격 409 → 재조회.
- **후보 삭제** `DELETE /api/meetings/{id}/todos/{todoId}` (× 버튼, 확인 없음; 승격된 것은 × 없음).
- **다시 시도** `POST /api/meetings/{id}/finalize` (실패 상태 · 만든 사람) → 정리 중 화면으로.
- **내보내기** `GET /api/meetings/{id}/export?format=html` — 새 탭/저장은 브라우저 기본. 형식 고르는 자리 없음.
- **작성자 표시**: `Line.author` 는 member_id 다 — 화면에서는 `meeting.attendees` 명부로 표시 이름을 찾고, 없으면 이름 자리를 비운다(id 를 그대로 그리지 않는다). W9 미결 해소.
- 자료·공유는 **WP-005 뒤**(이번 범위 밖, 현행 유지).

## 3. 그릴 것

- 정리 중: 영역 로딩(M2) · 스크립트 탭(원문 read) · 배지.
- 완료: 회의록 한 벌(track final) · 근거 칩 → 오른쪽 스크립트 탭 전환 + 해당 구간 하이라이트·스크롤(I05) · 다음 할 일 행([업무 생성]·× / 「요청됨」) · 회의록 [수정]→줄 편집(안건 단위 저장) · [내보내기] · 연필(제목 후보 포함).
- 실패: E54 안내 + E55 [다시 시도] · 회의록 [수정] · 스크립트.
- 취소됨: 시안대로.

## 4. allowed_paths

- `frontend/` 만. `backend/` 읽기 전용.

## 5. 하지 말 것

- 회의록에 업무 링크 금지 · 담당자 자동 채움 금지 · pdf/docx 금지 · 줄별 저장 금지(안건 덮어쓰기 하나) · 시안에 없는 요소 금지 · `api.ts` 밖 fetch 금지 · hex 리터럴 금지 · dev 서버·5176 금지.
- **D25**: DS 에 없는 부품은 재사용 컴포넌트로 분리(범용이면 `src/` 최상위) + 완료 보고에 「DS 추가 후보」 표(이름·자리·props/상태·로컬 클래스).

## 6. 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run <네가 만들거나 고친 테스트만>. 전체 빌드·e2e 금지. 검증 1회
```

- 테스트로: 끝난 회의 스크립트가 transcript 를 읽고 메모가 at_ms 자리에 선다 · 근거 칩이 탭 전환+구간 하이라이트 · 승격이 promote 를 부르고 「요청됨」이 되며 링크 없음 · 담당 칸 비어서 열림(참석자 우선) · × 가 삭제 · 실패에서 다시 시도 → 정리 중 · 409 저장 충돌 표시 · 제목 후보 표시·확정 · 공유받은 사람 조작 0 · 내보내기 링크 형식 하나.

## 7. 완료 보고 — **문구 변경 금지**

> ⚠ 핸들은 dispatch preamble 값 우선.

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: WP-006 Phase 4 회의 뒤 배선" \
  --body "변경 파일 / 검증 수치 / 계약 준수(경로별) / DS 추가 후보 표 / 임시 문구 표 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — WP-006 Phase 4. 상세는 인박스." --enter
```
