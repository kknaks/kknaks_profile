# 코드 검수 1 — WP-001 + WP-006 P1·2

- 작성: 2026-09-10 / `reviewer_code` (read-only 검수)
- 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (branch `kknaksss/sc-meeting`)
- **검수 범위 정정**: `git diff origin/main...HEAD` 는 **빈 diff** 다 — HEAD 가 곧 `origin/main`(a0bcee8)이다. 두 워커의 산출물은 전부 **커밋되지 않은 워킹트리 변경**이므로 `git diff HEAD` + untracked 를 범위로 잡았다. 파일 28개 수정·삭제(+2,226 / −1,123) + `frontend/src/meetings/` 신규 10개(3,003줄).
- **나는 아무 파일도 고치지 않았다.** 산출물은 이 리포트 1개뿐. 실행한 것은 §9 의 검증 4회뿐이고, 서버·DB reset·포트는 건드리지 않았다.

---

## 0. 총평 — **FAIL — 재발주 필요 (BE 3건 · FE 2건, 그중 2건은 양쪽 합의 필요)**

바닥은 잘 섰다. 도메인·스키마·상태 여섯·전이표·열람 판정·목록 두 구획·안건/줄 모델이 SPEC 대로 서 있고, WP-001 Phase 1~3 검증 10항목과 WP-006 Phase 1·2 검증 11항목이 **전부 테스트로 덮여 있다**. 경계 규칙(domain/application ↔ fastapi·sqlalchemy, entrypoints ↔ platform, reset_demo 밖 DDL)도 위반 0이고 검증 4종이 전부 통과한다.

막는 것은 **네 건**이다. ① 과거 일시로 세운 회의가 SPEC 이 금지한 자동 취소에 걸리고 그 동작이 테스트로 고정돼 있다 ② Todo 필드 집합이 BE·FE 사이에 **전혀 다르다** ③ `can_edit_note` 가 「예정」을 빼는 바람에 **「예정」 회의에서 안건을 더하거나 지울 길이 화면에 없다**(FE 에 그 갈래의 죽은 코드가 남아 있는 것이 증거다) ④ 읽기 전용이어야 할 SCR-105 패널에 시안에 없는 버튼이 하나 섰다.

| 축 | 판정 | 한 줄 |
|---|---|---|
| 1. 범위·경계 | **WARN** | 경계 규칙 위반 0·DDL 0. BE 가 allowed_paths 밖 `docs/domain-model.md` 를 고쳤다(규칙 충돌 — §1.2) |
| 2. BE↔FE 계약 일치 | **FAIL** | 7개 표면 중 5개 일치. **Todo 필드 전면 불일치**(F2) · `can_edit_note` 상태 집합(F3) · 안건 반환 타입(W8) |
| 3. SPEC·WP 정합 | **FAIL** | 검증 21항목 전부 덮임. 그러나 SPEC §3.1-8 「지난 날짜」 예외 미구현(F1) · 열람 축 셋(W1) |
| 4. 시안 정합 | **FAIL** | 패널에 시안에 없는 [다음 회의 예약](F4) · 「예정」 안건 편집 미도달(F3) · 창작 문구 1건(W10) |
| 5. 품질·위험 | **WARN** | 캘린더·MCP·graph·material_search 무손상(근거 §5.1). 조회 시점 쓰기는 브리프가 허가 — 다만 commit 경계가 갈린다(W2) |
| 6. 검증 재현 | **PASS** | architecture 14 · BE contract 124 · tsc 0 · vitest 30 — 전부 통과 |

---

## 1. 축 1 — 범위·경계

### 1.1 확인한 것 (PASS 근거)

| 검사 | 방법 | 결과 |
|---|---|---|
| `modules/*/domain.py`·`application.py` 가 fastapi·mcp·sqlalchemy 를 import 하지 않는가 | `grep -nE 'import (fastapi\|mcp\|sqlalchemy)'` 전수 | **0건** ✓ (`tests/architecture/test_architecture.py:60-69` 도 통과) |
| `entrypoints/` 가 `platform/` 구현을 직접 import 하지 않는가 | `grep -rn 'ax_workspace.platform' src/ax_workspace/entrypoints/` | **0건** ✓ (`test_architecture.py:78-81`) |
| `reset_demo` 밖 스키마 변경 | `grep -rn 'create_all\|DDL\|CREATE TABLE' src/` | `bootstrap/reset.py:20` 하나뿐 ✓ (Alembic 도입 없음) |
| FE `api.ts` 밖 fetch | `grep -rn 'fetch(' src/ --exclude api.ts` | **0건** ✓ |
| FE hex 리터럴 | `grep -rnE '#[0-9a-fA-F]{3,8}' src/meetings/` + `styles.css` 추가줄 | **0건** ✓ |
| FE 가시성 판단 축 | `MeetingDetailPage.tsx:176-199` | `status`·`viewer_relation`·`can_edit_info`·`can_edit_note` 넷으로만 갈린다 — kind 추론 **0건** ✓ |
| FE 가 `backend/` 를 건드렸나 | 변경 파일 목록 | **없음** ✓ |

### 1.2 WARN — W7 · allowed_paths 밖 파일 1개

- `docs/domain-model.md:128-130` (+4줄) — BE 브리프 §5 의 allowed_paths 는 `backend/` · `docker-compose.yml` · `Makefile` 셋이고, 같은 브리프 §1 은 이 파일을 **read-only** 로 못박았다.
- **다만 규칙이 충돌한다**: `roles/sc-ax/reviewer/rules.md` 의 backend 체크리스트가 「새 표가 `docs/domain-model.md` 대조표에 올랐나」를 요구한다. 워커는 그쪽을 따랐다.
- 내용은 정확하다 — `meetings`·`meeting_attendees`·`meeting_agendas`·`meeting_lines`·`meeting_todos` 와 폐기한 note version 계열이 코드와 맞게 적혔다.
- **판정: WARN**(FAIL 로 올리지 않는다). 다른 워커의 소유 영역을 침범한 것이 아니고, 리뷰 기준 문서 자신이 요구한 4줄 동기화다. **담당: 코디** — 브리프 §5 에 `docs/domain-model.md` 를 넣을지 정해 주면 다음 발주부터 충돌이 없다.

---

## 2. 축 2 — BE↔FE 계약 일치 (핵심)

전수 대조는 §7 표에 있다. 여기에는 어긋난 것만 적는다.

### 2.1 **F2 · FAIL — Todo 필드 집합이 양쪽에서 전혀 다르다** (담당: 코디 결정 → BE)

| | 필드 |
|---|---|
| **BE 구현** (`modules/meetings/application.py:1116-1125`) | `todo_id` · `text` · `assignee_candidate` · `due_candidate` · `linked_task_id` |
| **FE 소비** (`frontend/src/viewModels.ts` `MeetingTodo`) | `todo_id` · `agenda_id` · `title` · `description` · `due_candidate` · `checklist_candidate` · `reference` · `linked` |
| **겹치는 것** | `todo_id` · `due_candidate` **둘뿐** |

- BE 는 **브리프 §3**(`Todo = { todo_id, text, assignee_candidate, due_candidate, linked_task_id }`)을 그대로 구현했다 — 계약 우선순위 1 을 지킨 것이다.
- FE 는 **SPEC 0.4.1 §8.1** 을 따랐다. 그 절은 오늘 **16:56 에 개정**됐고(파일 mtime), 지금 본문은 `assignee_candidate` 를 **삭제**하고(§8.1:385 「담당자는 Todo에 없다 — AI가 고르지 않는다」) `agenda_id`·`title`·`description`·`checklist_candidate`·`reference`·`linked` 를 세운다. FE 는 개정 뒤 SPEC 과 일치한다(`MeetingDetail.test.tsx:230`·`:248` 이 「담당 후보 칸 없음」을 고정).
- **DB 컬럼도 옛 모양이다** — `platform/persistence.py` `MeetingTodoRecord` 에 `text`·`assignee_candidate`·`linked_task_id`.
- **지금은 터지지 않는다.** WP-001 은 todo 를 하나도 만들지 않아 `todos` 가 늘 `[]` 다. 터지는 것은 WP-004 다.
- **권장 수정**: SPEC §8.1(최신)을 정본으로 삼아 **BE 의 `_agenda_view` todo 투영·`meeting_todos` 컬럼·브리프 §3 셋을 함께 고친다.** 지금 고치는 값이 가장 싸다.

### 2.2 **F3 · FAIL — `can_edit_note` 가 「예정」을 빼서 안건 편집이 화면에서 닿지 않는다** (담당: BE + FE)

- BE `modules/meetings/application.py:42` — `_NOTE_EDITABLE = {DONE, FAILED, CANCELLED}`, `:1079` 가 그대로 `can_edit_note` 로 나간다.
- FE `MeetingDetailPage.tsx:187` — `canEditNote = can_edit_note && !live && !settling`, `:529` 가 [수정] 버튼의 유일한 게이트다.
- FE `MeetingDetailPage.tsx:189` — `agendaEditing = noteEditing && (planned || cancelled)`, `:651` 이 `[안건 추가]`의 게이트다.
- **`planned` 갈래는 도달 불가능한 죽은 코드다** — `can_edit_note` 가 `scheduled` 에서 늘 false 이므로 `noteEditing` 이 참이 될 수 없다. FE 가 「예정」을 기대하고 짰다는 증거이자, 두 워커가 이 필드의 뜻을 다르게 읽었다는 증거다.
- **결과**: 「예정」 회의 상세에서 **안건을 더하거나 지울 수 있는 자리가 없다.** API(`POST/DELETE /api/meetings/{id}/agendas`)는 서 있는데 화면이 부르지 않는다.
- 어긋난 기준:
  - 시안 `REPORT-회의실-v2.md:69` `E77` — 「**진행 중·정리 중을 뺀 네 상태**. 예정·취소됨은 안건을, 완료·실패는 회의록을 연다」
  - 시안 `REPORT-회의실-v2.md:76` `E35` — 「예정·취소됨(안건 편집)과 완료·실패(회의록 편집) **양쪽에** 선다」 · `:77` `E71` 안건 지우기 「예정·취소됨에서도 선다」
  - 시안 `REPORT-회의실-v2.md:151` 가시성 표 「예정 / 만든 사람 → … **회의록 [수정](안건 손보기)**」
  - SPEC §4.1-5 「안건은 예약에서도, **회의 시작 전 상세에서도**, 회의록 편집 상태에서도 더한다」
  - WP-001 Scope 「안건 CRUD와 결론 표시 변경」
- **주의 — 단순히 `scheduled` 를 `_NOTE_EDITABLE` 에 넣으면 안 된다.** 같은 상수가 `_rewrite_note_lines`(`:497`)의 **줄 덮어쓰기** 게이트로도 쓰이는데, SPEC §5.1 「예정」 행은 **회의록 줄 편집을 명시적으로 막는다**.
- **권장 수정**: 둘을 가른다 — ① `can_edit_note`(= [수정] 버튼이 서는가) = 만든 사람 × `{scheduled, done, failed, cancelled}` ② `_rewrite_note_lines` 의 줄 게이트 = `{done, failed, cancelled}` 유지. FE 는 `:190` `lineEditing` 이 이미 `settled || failedState` 로 좁혀 두었으므로 **FE 는 손댈 것이 없다**(F3 는 사실상 BE 한 줄 분리 + FE 테스트 1건 추가). 브리프 §3 의 「회의록 [수정] = can_edit_note && status in (done, failed)」 매핑도 같이 고쳐야 한다.

### 2.3 일치 확인한 것

- (a) `GET /api/meetings` → `{upcoming, past:{items, next_cursor}}` — BE `application.py:205` / FE `api.ts listMeetings`·`viewModels MeetingListPayload` ✓. `?cursor=` 양쪽 ✓ (`http.py:566-573` / `MeetingListPage.tsx:103`).
- (b) `MeetingDetail.meeting` 의 `can_edit_info`·`can_edit_note`·`viewer_relation` — 필드명·타입 일치 ✓ (`application.py:1076-1079` / `viewModels MeetingInfo`). 값 집합은 F3.
- (c) **안건 POST 201 을 FE 가 받는가 — ✓.** `http.py:655` 가 `status_code=201`, `api.ts:60-77` 의 `request<T>` 는 **204 만** 특별 처리하고 나머지는 `response.json()` 한다. 201 본문이 정상 파싱된다.
- (d) **PATCH agendas `lines` — ✓.** BE `UpdateAgendaRequest.lines: list[str]|None`(`http.py:188`) → `update_agenda`(`:485`) → `_rewrite_note_lines` 덮어쓰기(`:509` `replace_lines(track="final")`). FE `api.ts updateMeetingAgenda({lines})` → `MeetingDetailPage.tsx:290-292` 가 빈 줄을 보내기 전에 버린다. 계약대로 ✓.
- (e) **DELETE `?scope=` — ✓.** BE `Literal["meeting","note"]` 기본 `meeting`(`http.py:628`), 204 반환(`:639`). FE `removeMeeting(id, scope)`(`api.ts`) + `MeetingListPage.tsx:120`. 테스트가 `("u1","meeting")` 고정(`MeetingList.test.tsx:125`) ✓.
- (f) **quick-start — ✓.** `POST /api/meetings/quick-start` → 201 MeetingDetail, `status=in_progress`, 참석자 = 만든 사람 하나, title null (`application.py:293-314`). FE `quickStartMeeting()` → `MeetingListPage.tsx:132-137` ✓.
- (g) **오류 404/409/422 — ✓.** `http.py:466-473` 이 `MeetingNotFound`·`MeetingAccessDenied` → **404**(존재 숨김), `MeetingStateConflict` → **409**, `MeetingError` → **422**. 상속 순서도 옳다(StateConflict 를 Error 보다 먼저 검사). FE 는 `ApiError(status, detail)` 로 받아 `onError` 배너 한 줄로 그린다(`MeetingDetailPage.tsx:245-246`) — 상태코드별로 다른 문구를 내지는 않는다. 시안이 실패 경로 문구를 안 줬으므로(`REPORT-회의실-v2.md:110` 「서버 실패 경로라 정적 시안에서 낼 자리가 없다」) **위반 아님**.

---

## 3. 축 3 — SPEC·WP 정합

### 3.1 **F1 · FAIL — SPEC §3.1-8 「지난 날짜로 세운 회의는 이 규칙에 걸리지 않는다」 미구현** (담당: BE)

- `modules/meetings/domain.py:107-109` `is_auto_cancellable(status, ends_at, now, has_record)` — 판정에 **회의를 언제 세웠는지가 들어가지 않는다.**
- `modules/meetings/application.py:994-1009` `_settle_auto_cancel` 도 같다. `_validate_schedule`(`:1430`)은 과거 일시를 막지도 않는다.
- **결과**: 지난 날짜로 회의를 세우면 **바로 다음 조회에서 `cancelled` 가 된다.**
- 어긋난 기준: SPEC §3.1-8 — 「미리 잡은 회의가 종료 시각까지 아무 기록도 없이 지나면 … 「취소됨」이 된다. … **지난 날짜로 세운 회의는 이 규칙에 걸리지 않는다** (`X-185` · `X-149`)」. 시안 `REPORT-회의록-v2.md:184` 도 같은 `X-149` 를 「지난 날짜로 세운 「예정」 회의는 「지난」 구획에 붙는다」로 읽는다.
- **테스트가 어긋난 동작을 고정하고 있다** — `tests/contract/test_meeting_core.py:197-198`:
  ```
  # 종료 시각이 지났고 줄이 없으므로 지난 회의는 전부 「취소됨」이다 (SPEC §3.1-8).
  assert {row["status"] for row in first["past"]["items"]} == {"cancelled"}
  ```
  주석이 §3.1-8 을 근거로 대는데, 그 절의 두 번째 문장이 정확히 이 경우를 예외로 뺀다. 재발주 시 이 테스트도 함께 고쳐야 한다.
- **권장 수정**: `is_auto_cancellable` 에 「회의를 세운 시각이 `ends_at` 보다 앞인가」를 더한다(`meetings.created_at` 이 이미 있다). 「예정」으로 남고 `_is_past`(`:986-992`)가 이미 `ends_at <= now` 로 「지난」 구획에 넣으므로 `X-149` 도 함께 맞는다.

### 3.2 WARN — W1 · 열람 축이 셋이다 (담당: 코디 판단 → BE)

- `modules/meetings/application.py:967-977` `_can_read_detail` 의 마지막 줄:
  ```
  return meeting.organization_id in principal.organization_scope and MEETING_READ_PRIVATE in principal.capabilities
  ```
- `platform/meetings.py:154-158` `meetings_visible_to` 도 조직 조건을 **OR** 로 함께 건다(`:161` `or_(*conditions)`) — 목록 질의가 조직 전체 회의를 긁어 온 뒤 `_can_read_detail` 로 거른다.
- `modules/organization_access/catalog.py:147-152` — **`executive`(대표) 역할이 `meeting.read.private` 를 조직 범위로 들고 있다.** 즉 대표는 참석하지도 공유받지도 않은 회의를 열고 목록에서도 본다.
- 어긋난 기준: SPEC §3.2-1·2 「참석자가 아닌 사람은 그 회의가 있다는 것도 알지 못한다 … **공유가 유일한 예외다**」 · §10-1 동일 · WP-001 Open Issue 「열람 판정의 축은 `SCAX-ESC-006` 회신에 걸린다 — **관계 하나로 구현하고** 두 축이면 확장」.
- **테스트가 없다** — `test_meeting_core.py` 에 `read.private`·`executive` 를 찌르는 케이스가 0건이다. `test_someone_without_a_relationship_is_not_told_the_meeting_exists`(`:156`)는 그 권한이 없는 페르소나(SORA)로만 확인한다.
- **WARN 인 이유**: 이 축은 WP-001 이 만든 것이 아니라 **현행에서 이어받은 것**이고, `SCAX-ESC-006` 회신 대기 중이라고 WP 자신이 적어 두었다. 다만 SPEC 본문은 지금 「유일한 예외」라고 단정하므로 **코디가 셋 중 하나를 정해야 한다**: ① 축을 떼고 SPEC 대로 둘로 ② SPEC §3.2 에 대표 예외를 명시 ③ ESC-006 회신까지 보류하고 테스트로 현 동작을 고정.

### 3.3 WP-001 Phase 1~3 검증 10항목 — **전부 덮임** ✓

| WP 검증 | 테스트 | |
|---|---|---|
| 허용 안 된 전이 거부 | `test_meeting_core.py:67` (parametrize) | ✓ |
| 안건 21번째 거부 | `:85` | ✓ |
| 안건 삭제가 줄을 함께 지운다 | `:99` | ✓ |
| 비참석자 상세가 존재를 알리지 않는다 | `:156` (404 + 목록 공집합) | ✓ |
| 목록에 남의 회의가 안 섞인다 | `:161-162` | ✓ |
| 진행 중 편집 거부 | `:263` | ✓ |
| 참석자(비소유자) 편집 허용 | `:243` | ✓ |
| 회의록만 삭제가 회의를 남긴다 | `:291` | ✓ |
| quick-start 가 참석자 없이 선다 | `:229` | ✓ |
| 자동 취소·해제 | `:326` | ✓ (다만 F1 의 예외는 반대로 고정됨) |

- 안건 20개 한도 구현도 옳다 — `create` 의 `ensure_agenda_capacity(max(len(drafts)-1, 0))`(`application.py:273`)은 20개 통과·21개 거부로 정확히 동작한다(표현이 에두르지만 결과는 맞다).

### 3.4 BE 자기보고 「주의점」 6건 판정

| # | 워커 주의점 | 판정 | 근거 |
|---|---|---|---|
| 1 | 자동 취소를 **조회 시점**에 판정 | **OK** | BE 브리프 §3 이 명시 허가(「스케줄러가 없으면 조회 시점 판정으로 구현하고」). 위험도는 §5.2 |
| 2 | 열람 축을 조직→참석(`meetings_visible_to`)으로 | **OK (방향 맞음)** | SPEC §3.2-1 대로. 다만 세 번째 축 잔존 → W1 |
| 3 | 생성 body 에서 `organization_id`·`visibility` 제거 | **OK** | 계약 §3 에 없는 필드다. SPEC §3.1 에 조직 귀속 칸이 없고 `REPORT-회의실-v2.md:45` 도 「조직 귀속은 빼기로 했다」(D14) |
| 4 | 안건 POST **201** | **OK** | 계약이 코드를 안 정했고 REST 관례에 맞다. FE `request<>` 가 받는다(§2.3-c) |
| 5 | **`can_edit_note` 가 cancelled 에서도 true** (브리프는 done\|failed) | **코드가 맞다 → 브리프를 고쳐라 (WARN·W11)** | SPEC §5.1 취소됨 행: 열리는 것 = 「회의 시작 · **회의록 줄 편집**(둘 중 하나로 취소가 풀린다) · 공유」. 시안 `REPORT-회의실-v2.md:156` 도 동일. **담당: 코디**(브리프 §3 매핑 줄 수정) |
| 6 | `failed→summarizing` 허용 | **코드가 맞다 (WARN·W12)** | SPEC §5.1 실패 행 「**다시 시도**」 · §8-8 「[다시 시도]로 합성만 다시 건다」. `domain.py:48` 이 전이표에 정확히 넣었다. 브리프 §3 이 이 전이를 안 적었을 뿐 |
| + | `MeetingAccessDenied` 403→404 | **코드가 맞다 (WARN·W13)** | SPEC §3.2-1 · §10-1 「존재 자체를 알리지 않는다」. `http.py:466` 이 NotFound 와 같은 줄에 둔 것이 옳다 |

### 3.5 WP-006 Phase 1·2 검증 11항목 — **전부 덮임** ✓

| FE 브리프 §8 검증 | 테스트 |
|---|---|
| 여섯 상태 배지 전부 | `MeetingList.test.tsx:83` |
| 「열람」 | `:101` |
| 패널에 조작 버튼·후보 건수 줄 없음 | `:137` |
| 예약에 반복 칸 없음 | `:173` |
| 회의실 「가능」 배지 없음 · the Connect 요청 0 | `:173` (+ `grep '가능\|the Connect' src/meetings/` → 주석 외 0건) |
| 진행 중·정리 중·실패·취소됨에 연필 없음 | `MeetingDetail.test.tsx:127` |
| 비소유 참석자에게 연필 있고 회의록 [수정] 없음 | `:136` |
| 편집 중 [회의 시작] 비활성 | `:143` |
| 줄에 종류 배지 없음 | `:173` |
| 공유받은 사람에게 조작 버튼 0 | `:198` |
| 자료가 드로어로 열림 | `:217` |

---

## 4. 축 4 — 시안 정합

### 4.1 **F4 · FAIL — SCR-105 읽기 패널에 시안에 없는 [다음 회의 예약]** (담당: FE)

- `frontend/src/meetings/MeetingListPage.tsx:403-408` — `<footer className="meeting-panel-foot">` 첫 자리에 `!planned && [다음 회의 예약]`.
- 어긋난 기준:
  - 시안 `REPORT-회의록-v2.md:41-43` — 패널 푸터 요소는 `E27` [공유] · `E28` [내보내기] · `E25` [회의록 열기] **셋뿐**이다. [다음 회의 예약]에 해당하는 요소 ID 가 SCR-105 요소표에 없다(그것은 `SCR-106-E11` 이고 `REPORT-회의실-v2.md:52` 가 「완료 × 참석자」로 머리 버튼 줄에 둔다).
  - SPEC §3.4-6 — 「패널에서 하는 조작은 회의록을 바꾸지 않는 것 **둘이다** — [공유] · [내보내기]. 고치려면 [회의록 열기]로 상세로 간다.」
  - 같은 파일 `:324` 의 주석이 스스로 「읽기 전용이다. 조작 버튼도 후보 건수 줄도 두지 않는다」라고 적어 놓았다.
- **권장 수정**: 패널 푸터에서 [다음 회의 예약]을 뺀다(상세 `MeetingDetailPage.tsx:478` 의 것은 시안대로이므로 그대로 둔다).

### 4.2 시안대로 확인한 것 ✓

- 상태 배지 — 목록은 여섯 전부(`labels.ts meetingStatusClass`), 상세 머리는 **정리 중·실패·취소됨 셋만**(`labels.ts:388-392` `meetingBadgeClass` + `MeetingDetailPage.tsx:443`) — `REPORT-회의실-v2.md:44` `E02` 와 일치.
- [공유] — 「예정」을 뺀 다섯 상태 × 참석자(`MeetingDetailPage.tsx:463`) = `E84`(`:50`) ✓
- [내보내기] — 완료에만, 공유받은 사람에게도(`:468`, relation 무관) = `E65`(`:51`) ✓
- [회의 시작] — 예정·취소됨 × 참석자, 편집 중 비활성(`:451-455`) = `E07`(`:47`) + 시안 §3 주 ✓
- 연필 — `can_edit_info && (planned || settled)`(`:343-344`) = `E59`·가시성 표 ✓
- 탭 — 자료는 참석자만(`:195`), 스크립트는 예정·취소됨에 없음(`:196`) = `E63`(`:96`)·`REPORT-회의실-v2.md:165-168` ✓
- 안건 출처 셋 — `직접 입력 / 지난 회의에서 넘어옴 / AI 정리`(`labels.ts:394-398`) = `E21`(`:72`) ✓
- 예약 모달 — 칸 순서 주제·일시·목적·안건·참석자·장소, 반복 칸 없음, 회의실 정적(`BookingModal.tsx:21-22`·`:50`·`:281`) = `REPORT-회의록-v2.md:89`·`:105`·`:106` ✓
- 삭제 두 갈래 문구 — `T08`「무엇을 삭제할까요?」/「회의 삭제 시 회의 자료가 삭제되고 회의도 취소됩니다.」 · `T09`「회의를 취소했습니다.」 · `T10`「회의록을 삭제했습니다.」(`labels.ts` deleteTitle/deleteBody/deletedMeeting/deletedNote) — **원문 그대로** ✓

### 4.3 WARN — W10 · 창작 문구 1건 (담당: 코디)

- `frontend/src/labels.ts` — `scriptEmpty: "아직 원문이 없습니다."`. 시안 두 장에 **0 hit**. 워커가 바로 위 주석으로 「시안에 이 자리의 문구가 없고 … 원문 읽기 계약이 서면 이 문구도 확정 문구로 받아야 한다」고 스스로 신고했다. 브리프가 알려진 건으로 지정 → **WARN, 문구 위치만 기록**.
- **오해였던 것 하나** — `shared: "공유했습니다. 알림을 보냈습니다."` 는 SPEC §3.2-5(「**알림은 가지 않는다**」)와 정면으로 어긋나 보이지만, `design/회의실.dc.html` 에 **그대로 있다**(grep 1 hit). FE 는 화면 정본을 옳게 옮겼다. **시안 ↔ SPEC 충돌**이므로 §8-4 에 코디 결정 항목으로 올린다. FE 잘못이 아니다.
- 그 밖의 MOD-104·MOD-105 문구(「추가한 사람은 이 회의록을 읽을 수 있습니다…」 · 「첨부할 수 없는 형식입니다…」 등)는 전부 시안에 실재함을 grep 으로 확인했다 ✓

---

## 5. 축 5 — 품질·위험

### 5.1 열람 축 변경이 다른 소비자를 깨뜨리지 않는가 — **깨뜨리지 않는다** ✓

- **캘린더·MCP 는 옛 축을 그대로 쓴다.** `application.py:181` 의 `list()` 는 여전히 `meetings_in_organizations` 를 읽고, 새 `meetings_visible_to` 는 **`board()` 전용**이다(`:196`). 두 투영을 갈라 둔 것이 이 변경의 안전판이다(`:174-179` docstring 이 그 의도를 적는다).
- 그래프·자료 검색은 응답 모양 변화(`title` nullable · `owner_id`→`created_by` · `visibility`→`status` · 상세가 `{meeting, agendas}` 로 감싸짐)를 **어댑터에서 흡수**했다: `bootstrap/application.py` `readable_meeting` 이 `detail["meeting"]` 을 납작하게 펴고 `owner_id` 를 되살린다. `meeting_followup_tasks` 는 새로 분리된 `transcript_record` 를 읽는다.
- **테스트 근거**: `test_answer_resources.py`·`test_link_materials.py`·`test_relation_graph.py`·`test_relation_graph_scale.py`·`test_meeting_material_search.py` 가 함께 고쳐져 **124건 전부 통과**(§9). 회의 version 을 견주던 자리는 「판을 쌓지 않는다」에 맞춰 `None` 을 돌려주도록 바뀌었다(`bootstrap/application.py` `_current_version`).

### 5.2 조회 시점 자동 취소 — **위험도 중, 브리프가 허가한 범위**

- `_settle_auto_cancel`(`application.py:994-1009`)이 `list`·`board`·`_readable` 셋에서 불리며 **GET 이 상태를 바꾼다.** `meeting_board`·`get_meeting` 은 `session.commit()` 을 붙였다(`bootstrap/application.py`).
- **판정: WARN** — BE 브리프 §3 이 명시적으로 허가했다(「스케줄러가 없으면 조회 시점 판정으로 구현하고 WP Open Issue 에 적어라」). 판정식이 결정적(`ends_at` · 줄 개수)이라 읽는 사람마다 다른 답이 나오지도 않는다.
- 남는 위험 둘:
  - **W2 · commit 경계가 갈린다.** `list_meetings`(캘린더·MCP)는 `_settle_auto_cancel` 을 **부르지만 commit 하지 않는다** — 그 경로의 판정은 휘발한다. 같은 회의가 캘린더에서는 「취소됨」으로 보이고 DB 에는 「예정」으로 남아 있다가, 누군가 회의 목록을 열어야 비로소 굳는다. 한쪽으로 통일해야 한다(읽기에서 아예 쓰지 않거나, 둘 다 commit 하거나).
  - **W3 · WP Open Issue 기록이 없다.** 브리프가 요구했지만 WP 파일은 스펙 리포에 있고 BE 의 allowed_paths 밖이라 워커가 쓸 수 없었다. **담당: 코디/planner** — `work-001` Open Issues 에 한 줄 추가.
- 쓰기 부하 자체는 작다(조건에 걸린 회의만 UPDATE 1건). 다중 GET 동시성에서 같은 행을 두 세션이 쓰는 경우가 있으나 결과가 같아 수렴한다.

### 5.3 폐기 코드 — 라우터에서만 떼졌고 import 는 성하다 ✓

- 제거된 라우트: `POST/PATCH /api/meetings/{id}/note`·`/note/finalize`·`/summaries/{id}/adopt`·`/realtime-credential`·`/realtime-segments` — `grep 'api/meetings' entrypoints/http.py` 로 전수 확인, **0건**.
- 잔존(코디 결정 A): `recordings/start`·`recordings/{id}/stop`·`summaries/…/promote`·`speaker-assignments`. 브리프가 제거를 요구한 셋만 떼는 범위와 맞다.
- `platform/soniox.py`·`liveTranscription.ts`·`MeetingDrawer.tsx` 파일은 남아 있고 **빌드를 깨지 않는다** — `npx tsc --noEmit` **0 에러**, BE 테스트 124건 통과가 근거. WP-002 가 지운다.
- `MeetingDrawer`·캘린더 회의 탭 미노출 확인: `CalendarPage.tsx:96` 주석만 남고 탭·드로어 연결이 사라졌다. `CalendarMeetings.test.tsx` 는 삭제(staged D) ✓.

### 5.4 그 밖의 WARN

| # | 자리 | 내용 | 담당 |
|---|---|---|---|
| **W4** | `application.py:461-522` | `add_agenda`·`update_agenda`(title·concluded·order)·`remove_agenda` 에 **상태 게이트가 없다.** 만든 사람이면 「진행 중」·「정리 중」에도 안건을 고칠 수 있다. 시안 `E35`·`E71` 은 「**편집 중에만**」이고 진행 중·정리 중에는 편집 상태가 없다. 다만 SPEC §4.1-6 은 회의 중 AI 가 안건을 세운다고 하므로 **사람과 AI 를 가르는 규칙이 SPEC 에 없다** — 근거 불충분, 코디 판단 요청 | 코디 |
| **W5** | `http.py:466-473` | `MeetingVersionConflict` 가 어느 줄에도 안 걸려 `MeetingError` 로 떨어져 **422** 가 된다(409 가 아니라). 새 회의 표면은 `expected_version` 을 안 쓰지만 `stop_recording`(`:727`)이 여전히 던진다 | BE |
| **W6** | `http.py:147-156` | `CreateMeetingRequest` 만 `model_config = ConfigDict(extra="forbid")` 가 없다(Update·Agenda 계열엔 있다). 모르는 칸이 조용히 무시된다 | BE |
| **W8** | `api.ts addMeetingAgenda`·`updateMeetingAgenda` | 반환 타입이 `MeetingRecord` 인데 BE 는 **Agenda 하나**를 낸다(`application.py:469`·`:489` `_agenda_view`). `MeetingDetailPage.tsx:237-242` 의 `run()` 이 결과를 버리고 `reload()` 하므로 **런타임 무해**하지만, `MeetingDetail.test.tsx:190` 이 잘못된 모양을 mock 으로 고정한다 | FE |
| **W9** | `viewModels.ts MeetingLine` | `author: string` — 계약·BE 는 `author: member_id \| null`(`application.py:1111`). WP-001 은 늘 채우므로 지금은 안 터진다 | FE |
| **W14** | `MeetingDetailPage.tsx:491` | 「실패」의 **[다시 시도]가 `POST /end` 를 부른다.** 전이(`failed→summarizing`)는 도메인이 허용해 동작하지만, 「회의 종료」 표면을 「합성 재시도」로 겸용하는 셈이다. 표면을 가를지는 WP-004 몫 | 코디 |

---

## 6. 축 6 — 검증 재현 (§9 에 수치)

지시대로 **각 1회만** 실행했다. 서버·DB reset·`make local-stack`·dev 서버는 실행하지 않았고 5176/8001 포트를 건드리지 않았다.

---

## 7. 계약 대조표 — 엔드포인트별

| 엔드포인트 | BE 구현 | FE 소비 | 일치 |
|---|---|---|---|
| `GET /api/meetings[?cursor=]` | `http.py:566` → `application.py:189-205` `{upcoming, past:{items,next_cursor}}` | `api.ts listMeetings` → `MeetingListPayload` | ✅ |
| `MeetingRow` 9필드 | `application.py:1029-1040` | `viewModels MeetingRow` | ✅ 필드명·타입 전부 일치 |
| `GET /api/meetings/{id}` | `http.py:606` → `_detail` `{meeting, agendas}` | `api.ts readMeeting` → `MeetingRecord` | ✅ |
| `MeetingDetail.meeting` 15필드 | `application.py:1062-1082` | `viewModels MeetingInfo` | ✅ 모양 · ⚠️ `can_edit_note` **값 집합**(F3) |
| `Agenda` 7필드 | `application.py:1099-1126` | `viewModels MeetingAgenda` | ✅ |
| `Line` 6필드 | `application.py:1106-1113` | `viewModels MeetingLine` | ⚠️ `author` nullability(W9) |
| **`Todo`** | `application.py:1116-1125` `{todo_id,text,assignee_candidate,due_candidate,linked_task_id}` | `viewModels MeetingTodo` `{todo_id,agenda_id,title,description,due_candidate,checklist_candidate,reference,linked}` | ❌ **F2 — 겹치는 필드 2개** |
| `POST /api/meetings` → 201 | `http.py:577` `CreateMeetingRequest` 9칸 | `api.ts bookMeeting` 9칸 | ✅ (⚠️ FE `title` 이 non-null 타입 — BE 는 null 허용) |
| `POST /api/meetings/quick-start` → 201 | `http.py:598` | `api.ts quickStartMeeting` | ✅ |
| `PATCH /api/meetings/{id}` | `http.py:613` 7칸 · scheduled\|done · 참석자 전원 | `api.ts updateMeetingInfo` 6칸(purpose 미사용) | ✅ |
| `DELETE /api/meetings/{id}?scope=` | `http.py:625` `meeting\|note` · 204 | `api.ts removeMeeting` | ✅ |
| `POST …/start` · `…/end` | `http.py:641`·`:648` → MeetingDetail | `api.ts startMeeting`·`endMeeting` | ✅ |
| `POST …/agendas` → **201** | `http.py:655` → **Agenda** | `api.ts addMeetingAgenda` → `MeetingRecord` 타입 | ⚠️ **W8** (201 수신은 ✅, 타입만 오류) |
| `PATCH …/agendas/{aid}` | `http.py:666` `{title?,concluded?,order?,lines?}` → **Agenda** | `api.ts updateMeetingAgenda` `{title?,concluded?,lines?}` → `MeetingRecord` 타입 | ⚠️ **W8** (`lines` 계약 ✅) |
| `DELETE …/agendas/{aid}` → 204 | `http.py:680` | `api.ts removeMeetingAgenda` | ✅ |
| 오류 404 / 409 / 422 | `http.py:466-473` | `ApiError(status, detail)` → 배너 | ✅ |

**불일치 3건** (F2 · F3 · W8) — 그중 런타임을 지금 깨는 것은 **0건**, 화면 기능을 막는 것은 **F3 1건**, WP-004 에서 깨질 것이 **F2 1건**.

---

## 8. 코디가 정해야 할 것 (최소로)

1. **Todo 필드 집합(F2)** — SPEC 0.4.1 §8.1 이 오늘 16:56 에 개정되며 브리프 §3 과 갈렸다. **SPEC 을 정본으로 삼아 BE·브리프를 고친다**가 자연스러워 보이지만 계약 우선순위상 코디 결정이다. 정하면 BE 재발주 한 덩어리(투영 + `meeting_todos` 컬럼 + 브리프 §3).
2. **`can_edit_note` 의 뜻(F3)** — 「[수정] 버튼이 서는가」인가, 「회의록 **줄**을 고칠 수 있는가」인가. 전자로 정하면 상태 집합에 `scheduled` 를 넣고 BE 안에서 줄 게이트를 따로 둔다(§2.2 권장안). 후자로 정하면 FE 가 안건 편집용 파생값을 따로 만들어야 하고 시안 `E35`·`E71` 을 어떻게 열지 다시 정해야 한다.
3. **열람 축(W1)** — `meeting.read.private` × 조직 범위(대표 역할)를 ① 뗀다 ② SPEC §3.2 에 예외로 적는다 ③ `SCAX-ESC-006` 회신까지 현 동작을 테스트로 고정한다. 셋 중 하나.
4. **「공유했습니다. 알림을 보냈습니다.」** — 시안(`회의실.dc.html`)에는 있고 SPEC §3.2-5 는 「알림은 가지 않는다」이며 시안 리포트의 금지어 검사도 「알림 0」을 세었다. **시안과 SPEC 중 어느 쪽을 고칠지** 정해야 한다(FE 코드는 시안대로이므로 어느 쪽이든 한 줄).
5. **진행 중·정리 중의 안건 편집(W4)** — 사람이 그때 안건을 고칠 수 있어야 하는가. SPEC 이 사람과 AI 를 가르지 않아 근거가 없다.
6. **`docs/domain-model.md` 의 소유(W7)** — BE 브리프 §5 에 넣을지. 리뷰 체크리스트가 이미 그 갱신을 요구하고 있어 지금은 두 문서가 서로 다른 말을 한다.
7. **`work-001` Open Issues 기록(W3)** — 조회 시점 자동 취소를 적어야 하는데 스펙 리포는 BE 워커의 쓰기 범위 밖이다. planner 발주로 넘길 것.

---

## 9. 검증 재현 수치 · git status

| 검사 | 명령 | 결과 |
|---|---|---|
| BE 경계 | `cd backend && uv run pytest -q tests/architecture` | **14 passed** (13.67s) |
| BE 계약 (워커가 고친 파일 8개) | `uv run pytest -q -m 'not integration' tests/contract/{test_meeting_core,test_meeting_followups,test_meeting_material_search,test_meeting_recordings,test_answer_resources,test_link_materials,test_relation_graph,test_relation_graph_scale}.py` | **124 passed** (65.13s) |
| FE 타입 | `cd frontend && npx tsc --noEmit` | **0 에러** (exit 0) |
| FE 테스트 | `npx vitest run src/meetings/ src/labels.test.ts` | **30 passed** / 3 files (labels 6 · MeetingList 9 · MeetingDetail 15), 1.19s |

- 경고 2종은 **무관·기존 부채**다: `anyio.abc.BlockingPortal` deprecation(starlette) · `HTTP_422_UNPROCESSABLE_ENTITY` deprecation(starlette 최신). 실패 0.
- FE 워커의 자기보고 「vitest 65/65」는 프론트 전체 스위트 수치로 보인다. 이번 범위(`src/meetings/` + `labels.test.ts`)의 실측은 **30** 이다.
- 전체 스위트·`-m integration`·`make reset-demo`·`make local-stack`·dev 서버는 **실행하지 않았다**(브리프 §3-6·§5).

**git status (검수 전후 동일 — 리뷰어가 만든 변경 0)**

```
 M backend/src/ax_workspace/bootstrap/application.py       M frontend/src/App.tsx
 M backend/src/ax_workspace/bootstrap/material_sources.py  D frontend/src/CalendarMeetings.test.tsx
 M backend/src/ax_workspace/bootstrap/scenario.py          M frontend/src/CalendarPage.tsx
 M backend/src/ax_workspace/entrypoints/http.py            M frontend/src/api.ts
 M backend/src/ax_workspace/entrypoints/mcp.py             M frontend/src/labels.ts
 M backend/src/ax_workspace/modules/meetings/application.py M frontend/src/styles.css
 M backend/src/ax_workspace/modules/meetings/domain.py     M frontend/src/viewModels.ts
 M backend/src/ax_workspace/modules/work/graph.py          ?? frontend/src/meetings/  (10 files)
 M backend/src/ax_workspace/platform/meetings.py
 M backend/src/ax_workspace/platform/persistence.py
 M docs/domain-model.md                                     ← allowed_paths 밖 (W7)
 M backend/tests/contract/*.py (8)  D backend/tests/contract/test_meeting_realtime.py
```

합계 30항목 (M 27 · D 2 · ?? 10파일 1디렉터리). **커밋·push·PR 없음.**

---

## 10. 재발주 요약

| # | 담당 | 무엇 | 크기 |
|---|---|---|---|
| **F1** | BE | 자동 취소에 「지난 날짜로 세운 회의」 예외를 넣고 `test_meeting_core.py:197-198` 을 함께 고친다 | 소 |
| **F2** | BE (코디 결정 후) | Todo 투영·`meeting_todos` 컬럼을 SPEC §8.1 최신 모양으로 | 중 |
| **F3** | BE (+FE 테스트 1건) | `can_edit_note` 에 `scheduled` 를 넣고 줄 편집 게이트를 분리 | 소 |
| **F4** | FE | `MeetingListPage.tsx:404-408` 의 [다음 회의 예약] 제거 | 소 |
| W1·W4·W7·W3 | 코디 | §8 의 결정 항목 | — |
| W2·W5·W6 | BE | commit 경계 통일 · 409 매핑 · `extra="forbid"` | 소 |
| W8·W9·W10 | FE | 반환 타입 2건 · `author` nullable · 창작 문구 확정 대기 | 소 |
| W11·W12·W13 | 코디 | **브리프 §3 을 코드에 맞춰 고칠 항목**(코드가 SPEC 대로다 — 재발주 아님) | — |
