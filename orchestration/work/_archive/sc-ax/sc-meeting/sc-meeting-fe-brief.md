# [frontend] WP-006 Phase 1·2 — 회의 목록(SCR-105)·예약 모달·회의 상세(SCR-106) 읽기/편집 — 확정 시안 이식

너는 **sc-ax `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (branch `kknaksss/sc-meeting`, base `origin/main` a0bcee8 → PR `main`)

⚠ **같은 워크트리에서 backend 워커가 `backend/` 를 병렬로 고친다(WP-001). `backend/` 는 읽기만.** 너는 `frontend/` 만 쓴다. 백엔드 API 는 네 작업 중에 **아직 없다** — §3 계약을 믿고 `api.ts` 를 그 계약대로 쓰고, 테스트는 vitest 모킹으로 한다. 실물 연결 확인은 코디가 한다.

## 1. SSOT — 먼저 읽을 것

- **화면 정본 = 확정 시안** (이대로 옮긴다. 화면 결정을 새로 하지 않는다):
  - `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/design/회의록.dc.html` — SCR-105 목록 + 읽기 패널 + MOD-102 예약 모달 + 삭제 확인 모달
  - `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/design/회의실.dc.html` — SCR-106 상세(6상태 × 3 viewer) + MOD-104 첨부 + MOD-105 공유 + 자료 드로어
  - `design/REPORT-회의록-v2.md` · `design/REPORT-회의실-v2.md` — 요소 체크리스트·상태×viewer 가시성 표·클래스 실재 목록·미결. **가시성 표가 곧 조건문이다.**
  - `design/CLAUDE.md`(타이포 단) · `design/_ds/scax-…/README.md`(클래스 어휘 — 이 워크트리의 `frontend/src/styles.css` 와 같은 DS)
- **SPEC**: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/20-spec/spec-004-meeting-note.md` (0.4.1) — §3 · §4 · §5.1 상태 표 · §10.
- **WP**: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/30-work/work-006-meeting-screens.md` — **Phase 1·2 만** 이번 범위. Phase 3(스트림·두 트랙 실시간)은 WP-002/003 뒤 별도 발주.
- 현행 프론트 사실: `frontend/src/MeetingDrawer.tsx`(삭제 대상) · `CalendarPage.tsx`(회의 목록 탭 제거) · `App.tsx`(내비게이션) · `api.ts`(회의 함수들) · `.design-sync/NOTES.md`.

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

현행은 캘린더 페이지 안 「회의 목록」 탭에서 드로어(`MeetingDrawer`)로 회의를 다룬다. 새 화면은 **좌측 메뉴 「회의 목록」** 아래 전체 화면 둘(목록·상세)이다. 시안 두 장이 `x-dc` 템플릿(DCLogic)으로 돼 있으니 **그 렌더 결과·조건·문구를 React 로 옮긴다.** 시안의 `renderVals()` 가 곧 뷰모델 명세다.

## 3. 계약 (backend 워커와 합의됨 — 이대로 소비. 필드명 바꾸지 마라)

상태 wire 값: `scheduled`·`in_progress`·`summarizing`·`done`·`failed`·`cancelled` → 라벨 예정·진행 중·정리 중·완료·실패·취소됨.

```
GET  /api/meetings → { upcoming: MeetingRow[], past: { items: MeetingRow[], next_cursor: string|null } }   (?cursor=)
MeetingRow = { meeting_id, title: string|null, starts_at, ends_at, location: string|null, status,
               viewer_relation: "attendee"|"shared", created_by, attendee_count }
GET  /api/meetings/{id} → MeetingDetail = { meeting: { meeting_id, title, purpose, starts_at, ends_at, location, status, created_by,
        attendees: [{member_id, display_name}], external_attendees: string[], viewer_relation, can_edit_info, can_edit_note,
        last_saved_at, carried_from_meeting_id }, agendas: Agenda[] }
Agenda = { agenda_id, order, title, source: "manual"|"carried"|"ai", concluded, lines: Line[], todos: Todo[] }
Line  = { line_id, track: "memo"|"ai"|"final", order, text, author, evidence: [{start_ms,end_ms}] }
Todo  = { todo_id, text, assignee_candidate, due_candidate, linked_task_id }
POST /api/meetings { title, purpose?, starts_at, ends_at, location?, attendee_ids, external_attendees?, agendas?: [{title}], carried_from_meeting_id? } → 201 MeetingDetail
POST /api/meetings/quick-start {} → 201 MeetingDetail(in_progress)
PATCH /api/meetings/{id} { title?, starts_at?, ends_at?, location?, attendee_ids?, external_attendees? }   (scheduled·done, 참석자 전원)
DELETE /api/meetings/{id}?scope=meeting|note → 204
POST /api/meetings/{id}/start · /end
POST|PATCH|DELETE /api/meetings/{id}/agendas[/{aid}]
사람 명부·조직도: 현행 `api.ts` 의 organization 조회를 그대로 쓴다(WP-001 범위 밖).
오류: 404(존재 숨김) · 409(상태) · 422. 문구는 화면(시안 §5.8 T-ID)이 소유.
```

**시안 요소 ↔ 계약 매핑**: 「열람」 배지 = `viewer_relation === "shared"` · 「제목 없는 회의」 = `title === null` · 연필/편집 = `can_edit_info && status in (scheduled, done)` · 회의록 [수정] = `can_edit_note && status in (done, failed)`(예정·취소됨은 안건 편집만) · 안건 블록 = `agendas[].lines(track final 또는 memo·ai 표시 규칙은 시안대로)`.

## 4. 먼저 읽을 핵심 파일

- `design/회의록.dc.html` 의 `<script type="text/x-dc">` — `MEETINGS`·`renderVals()`·상태 배지 맵·삭제 모달·예약 모달 로직 전부.
- `design/회의실.dc.html` 의 같은 자리 — `screenState`×`viewer` 가시성, 머리 편집, 안건 블록·줄 편집, 자료 드로어·첨부·공유 모달.
- `frontend/src/App.tsx:19-26` — 내비게이션 배열(「회의 목록」 추가, 라벨은 시안 rail 8개 중 데모에 있는 것만).
- `frontend/src/CalendarPage.tsx:42-160` — 「회의 목록」 탭·MeetingDrawer 연결(제거).
- `frontend/src/api.ts:760-830` — 현행 회의 함수(계약대로 교체) · `frontend/src/styles.css` — 클래스 실재 확인.
- `frontend/src/org/*` — 조직도·명부 부품(예약·공유 모달의 참석자 고르기에 재사용).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `frontend/`
- (`backend/` 는 **읽기 전용** — backend 워커 소유)

## 6. 구현 단계

1. **골격** — 메뉴 「회의 목록」 → `MeetingListPage`, 행 선택 → 패널, [회의록 열기]/[회의 시작] → `MeetingDetailPage`. `api.ts` 를 §3 계약으로 교체(현행 회의 함수·realtime 함수는 제거하지 말고 **미사용으로 남긴다** — WP-002 가 지운다).
2. **WP-006 Phase 1** — 목록 두 구획·[더 보기]·행 상태 배지·「열람」·삭제 두 갈래(× 모달, [회의록만 삭제]·[회의 취소], 토스트) · 읽기 패널(안건 블록·[공유]·[내보내기]·[회의록 열기]; 조작 버튼·후보 건수 줄 없음) · MOD-102 예약(칸 순서 주제·일시·목적·안건·참석자·장소, 반복 없음, 사외 참석자는 이름 찾기 안, 회의실 정적 목록, [회의실까지 예약]/[회의록만 생성]) · quick-start.
3. **WP-006 Phase 2** — 상세 머리(회의 정보 + 연필 인라인 편집: 제목·날짜·시각 30분·장소 글자·참석자, scheduled·done 만, 참석자 전원, 편집 중 [회의 시작] 비활성) · 안건 블록(제목·결론·출처·내용 줄·근거 타임칩 자리·다음 할 일) · 줄 단위 편집·저장(덮어쓰기)·마지막 저장 표시 · 상태별 가시성(시안 리포트 표) · 오른쪽 탭 자료(드로어)·스크립트(정적 — 실시간은 Phase 3) · MOD-104·MOD-105 는 **화면만**(API 는 WP-005 — 호출 자리는 `TODO(WP-005)` 로 남김).
4. `MeetingDrawer.tsx`·캘린더 회의 탭은 **미노출**(라우트에서 뗀다). 파일 삭제는 WP-002 와 한 배포.
5. §8 검증 → 자기점검 → 완료 보고.

## 7. 범위 제약 — 하지 말 것

- 화면 결정을 새로 하지 않는다. 시안에 없는 요소·문구 금지, 시안에 있는 것 생략 금지. 애매하면 시안 리포트 미결(M#)을 확인하고 그래도 없으면 코디에게 묻는다.
- Phase 3(WS·마이크·메모 입력 자동 저장·AI 탭 실시간)은 만들지 않는다. 진행 중 상태 화면은 **정적**(시안의 픽스처 대신 API 값)으로만.
- 상단 AI 채팅 입력·알림·일시정지·회의실 「가능」 판정·the Connect 요청 — 데모 범위 밖.
- `api.ts` 밖에서 fetch 금지. 새 색·그림자·클래스 발명 금지(DS 어휘만). hex 리터럴 금지. `backend/` 수정 금지.

## 8. 검증

```
cd frontend && npx tsc --noEmit (네가 만진 파일 0 에러) + npx vitest run <네가 만들거나 고친 테스트 파일만>. 전체 빌드·acceptance-e2e 금지 — 사용자 방침. 자기점검 — envelope(allowed_commands·waiting_on)로 권한을 판단했는가(kind 로 추론 금지) · api.ts 밖에서 fetch 하지 않았는가 · 기존 컴포넌트·viewModels 를 재사용했는가. 검증은 1회만
```

- 이 화면은 envelope 대신 **`viewer_relation`·`can_edit_info`·`can_edit_note`·`status`** 로 가시성을 가른다 — 역할(kind)로 추론하지 마라.
- 테스트로 덮을 것(WP-006 Phase 1·2 검증 항목): 여섯 상태 배지 전부 · 「열람」 · 패널에 조작 버튼·건수 줄 없음 · 예약에 반복 칸 없음 · 회의실 배지 없음·the Connect 요청 0 · 진행 중·정리 중·실패·취소됨에 연필 없음 · 비소유 참석자에게 연필 있고 회의록 [수정] 없음 · 편집 중 [회의 시작] 비활성 · 줄에 종류 배지 없음 · 공유받은 사람에게 조작 버튼 0 · 자료가 드로어로 열림.
- 사용자 포트·프로세스 금지: `make local-stack`·dev 서버를 **띄우지 마라**(5176 은 코디가 쓰고 있다). 실물 확인은 코디가 한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_bb3a4c59-dfaf-446f-a7a0-e4ad168067f2 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: WP-006 Phase 1·2 회의 화면" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(tsc·vitest 수치) / 시안 요소 체크리스트 충족 수 / 계약 준수 / TODO(WP-005·Phase 3) 자리 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — WP-006 Phase 1·2. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
