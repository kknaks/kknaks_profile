# 코드 검수 2 — 검수 1 FAIL 해소분 + D19-3·D24 변경분

- 작성: 2026-09-10 / `reviewer_code` (read-only · 검수 1 과 같은 세션)
- 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` — **아무 파일도 고치지 않았다.**
- 범위: 검수 1(≈17:05) 이후 mtime 이 바뀐 파일만 — BE 6개(17:11~17:14) · FE 8개(16:57~17:16). 검수 1 에서 이미 PASS 한 자리는 다시 보지 않았다.

---

## 0. 총평 — **PASS (WARN 5)**

**검수 1 의 FAIL 넷이 모두 해소됐고 넷 다 회귀 테스트가 붙었다.** D22 처리 항목 8개, D19-3·D24 의 FE 계약 변경도 전부 반영됐다. 검증 3종이 깨끗하다(BE 45 passed · tsc 0 · vitest 26 passed).

특히 좋은 것 둘: ① F3 를 「상수에 `scheduled` 를 끼워 넣기」로 때우지 않고 `_AGENDA_EDITABLE` / `_NOTE_EDITABLE` 를 **정말로 갈랐다** — 검수 1 이 경고한 「줄 편집이 「예정」에 새는」 함정을 피했고, 테스트가 `can_edit_agendas is True and can_edit_note is False` 로 그 분리를 못박는다(`test_meeting_core.py:498`). ② 열람 축 셋째를 지우면서 캘린더 투영만 `_can_read_calendar_detail` 로 따로 남겨, SPEC §3.2 경계와 캘린더 요구를 한 함수에 뒤섞지 않았다.

남은 WARN 다섯은 **전부 타입 선언·오류 코드 수준이고 런타임을 깨지 않는다.** 재발주 없이 다음 WP 에 얹어도 된다.

---

## 1. F1~F4 해소 여부와 회귀 테스트

| # | 무엇 | 구현 | 회귀 테스트 | 판정 |
|---|---|---|---|---|
| **F1** | 「지난 날짜로 세운 회의」 자동 취소 예외 | `domain.py:107-119` — 시그니처에 `created_at` 추가, `:119` `return created_at is None or created_at < ends_at` | `test_meeting_core.py:344` `test_a_meeting_recorded_after_the_fact_is_never_auto_cancelled` **신설** · 검수 1 이 지적한 잘못된 단정(`:197-198`)이 `{"cancelled"}` → **`{"scheduled"}`** 로 뒤집혔고 주석도 §3.1-8·`X-149` 로 고쳐 달렸다 | **PASS** |
| **F2** | Todo = SPEC §8.1 여덟 필드 | BE `application.py:1116-1140` `_todo_view` 8필드 · `persistence.py:314-330` `MeetingTodoRecord` 가 `title`·`description`·`checklist_candidate`·`reference`·`linked_work_request_id` 로 재정의, **`assignee_candidate` 컬럼 제거** | `test_meeting_core.py:538` `test_a_todo_carries_the_eight_values_the_promotion_modal_needs` **신설** | **PASS** (필드명 8/8 일치 · `reference` 타입만 FE 쪽에 잔재 → §5 N1) |
| **F3** | `can_edit_agendas` / `can_edit_note` 분리 | BE `application.py:42-47` 두 상수 분리 · `:1107-1108` 두 필드 · `:964-965` `_agenda_target` 가 `_AGENDA_EDITABLE` 밖이면 `MeetingStateConflict`(409). FE `MeetingDetailPage.tsx:187-193` — `canEdit = canEditNote \|\| canEditAgendas`, `agendaEditing = noteEditing && canEditAgendas`, `lineEditing = noteEditing && canEditNote && (settled \|\| failedState)` | BE `test_meeting_core.py:486` (409 셋 + 예정/완료 대조) · FE `MeetingDetail.test.tsx:172` 「「예정」에서도 [수정]이 서고 안건을 더하고 뺀다 — 줄 편집 칸은 서지 않는다」 · `:191` 「고칠 권한이 둘 다 없으면 [수정] 자체가 서지 않는다」 **셋 다 신설** | **PASS** |
| **F4** | 패널 [다음 회의 예약] 제거 | `grep 'bookNext\|onBookNext' MeetingListPage.tsx` → **0건** | 검수 1 의 `MeetingList.test.tsx:137` 「읽기 패널에는 조작 버튼도 후보 건수 줄도 없다」가 계속 통과 | **PASS** |

**검수 1 의 죽은 코드가 살아났다** — `agendaEditing` 의 `planned` 갈래가 이제 실제로 도달한다(`can_edit_agendas` 가 `scheduled` 에서 true). 「예정」 회의에서 안건 추가·삭제가 화면에서 닿는다.

---

## 2. BE↔FE 계약

| 항목 | BE | FE | 판정 |
|---|---|---|---|
| `can_edit_agendas` | `application.py:1108` | `viewModels.ts:942` · `MeetingDetailPage.tsx:188` | **PASS** |
| `can_edit_note` (줄 편집 전용으로 좁아짐) | `:1107` `_NOTE_EDITABLE = {done, failed, cancelled}` | `:939` · `MeetingDetailPage.tsx:193` 가 `settled \|\| failedState` 로 한 번 더 좁힘 | **PASS** |
| **Todo 8필드** | `_todo_view` `todo_id`·`agenda_id`·`title`·`description`·`due_candidate`·`checklist_candidate`·`reference`·`linked` | `viewModels.ts:902-912` — **필드명 8/8 동일** | **PASS** (타입 2건 → §5) |
| 안건 반환형 | `add_agenda`·`update_agenda` → `_agenda_view`(Agenda 하나) | `api.ts:929`·`:941` **`Promise<MeetingAgenda>`** — 검수 1 W8 해소 | **PASS** |
| 승격 행 렌더 (D24) | `linked` = `{work_request_id, task_id\|null}` 또는 `null` | `MeetingDetailPage.tsx:623-626` · `MeetingListPage.tsx:385-387` — `todo.linked` 면 `<span>` 「요청됨」 텍스트, **누르는 자리 없음**. 미승격이면 [업무 생성] + `×` | **PASS** |
| [업무 생성] → CreateWorkDrawer | — | `MeetingDetailPage.tsx:36` import · `:776` 사용. 테스트 `MeetingDetail.test.tsx:273` 「제목·설명·기한·체크리스트만 채우고 담당은 비운 채로 연다」 | **PASS** |

---

## 3. 열람 축

| 확인 | 결과 |
|---|---|
| `_can_read_detail` 이 참석·공유 둘뿐인가 | **PASS** — `application.py` `_can_read_detail` 이 `owner \|\| attendee \|\| is_shared_with` 로 끝난다. 조직 범위 × `meeting.read.private` 갈래가 **사라졌다** |
| `_can_read_calendar_detail` 이 `list()` 에서만 쓰이는가 | **PASS** — `grep '_can_read_calendar_detail'` → 정의(`:990`) + 호출 **1곳**(`:187`, `list()` 안). `board`·`get`·`_readable` 은 `_can_read_detail` 만 부른다 |
| 비참석 대표 404 · 목록 0건 테스트 | **PASS** — `test_meeting_core.py:518` 신설. `:526` 이 유나가 `meeting.read.private` 를 **실제로 들고 있음**을 먼저 단정한 뒤 `:528` 404 · `:530` `upcoming/past` 공집합 · `:531` 제목 문자열이 응답 어디에도 없음까지 본다. `:534-535` 가 「공유가 유일한 예외」도 함께 고정 |
| `list_meetings` commit | **PASS** — `bootstrap/application.py:470-474` 에 `session.commit()` 추가(검수 1 W2 해소) |

**참고(누출 아님)**: `platform/meetings.py:155-156` 의 `meetings_visible_to` 는 여전히 조직 조건을 `or_` 로 걸어 조직 회의를 과잉 조회한다. 그러나 `board()` 가 `_can_read_detail` 로 거르므로 **응답에는 새지 않는다** — `:530-531` 테스트가 그 증거다. 질의 폭만 넓은 성능 나이트라 WARN 에도 넣지 않는다.

---

## 4. 안건 편집 게이트

| 확인 | 근거 | 판정 |
|---|---|---|
| in_progress·summarizing 에서 409 | `test_meeting_core.py:504`(POST 409) · `:505`(PATCH concluded 409) · `:506`(DELETE 409) · `:509`(정리 중 POST 409) | **PASS** |
| 「예정」에서 안건 편집 열리고 줄 편집 닫힘 | `:498` `can_edit_agendas is True and can_edit_note is False` · `:499` 안건 POST **201** / FE `MeetingDetail.test.tsx:172` 가 화면에서 같은 것을 본다 | **PASS** |
| 「완료」는 둘 다 열림 | `:514` `can_edit_agendas is True and can_edit_note is True` · `:515` 201 | **PASS** |
| 진행 중 두 칸 모두 false | `:503` | **PASS** |

---

## 5. 새 어긋남 점검

| 확인 | 결과 |
|---|---|
| **[수정] 을 둘 중 하나로 세운 FE 판단이 시안 `E77`(네 상태)과 맞는가** | **PASS.** `canEdit = canEditNote \|\| canEditAgendas`(`MeetingDetailPage.tsx:189`)를 상태별로 펴면 예정(agendas T) · 완료(둘 다 T) · 실패(둘 다 T) · 취소됨(둘 다 T) → **정확히 네 상태**, 진행 중·정리 중은 `:187-188` 의 `!live && !settling` 로 배제. 시안 `REPORT-회의실-v2.md:69` `E77` 「진행 중·정리 중을 뺀 네 상태」와 일치하고, 「예정·취소됨은 안건을, 완료·실패는 회의록을 연다」도 `agendaEditing`/`lineEditing` 이 그대로 구현한다 |
| 「연관 업무」 잔존 | **0건 ✓** — 유일한 hit 은 `MeetingDetail.test.tsx:300` 의 **부정 단정**(`queryByText(/연관 업무/)).toBeNull()`). 라벨도 `labels.ts` 에서 `requested: "요청됨"`(`:437`)로 교체됐다 |
| 「알림」 잔존 | **회의 화면 0건 ✓** — `labels.ts:540` `shared: "공유했습니다."` 로 교체, `:538` 에 왜 바꿨는지 주석. 남은 hit 은 전부 무관한 공용 Toast 부품(`Modal.tsx`·`styles.css`) |
| 코디 실물 확인과 코드 일치 — 과거 일시 회의 `scheduled` 유지 | **일치 ✓** `domain.py:119` + `test_meeting_core.py:198` |
| 코디 실물 확인 — 진행 중 안건 편집 409 | **일치 ✓** `application.py:964-965` + `test_meeting_core.py:504-506` |
| 코디 실물 확인 — 비참석 대표 404 / 목록 0건 | **일치 ✓** `_can_read_detail` + `test_meeting_core.py:528-531` |

### 남은 WARN 다섯 (재발주 불필요 — 다음 WP 에 얹으면 된다)

| # | 자리 | 내용 | 위험 |
|---|---|---|---|
| **N1** | `frontend/src/viewModels.ts:910` | `reference: string \| null` 인데 BE 는 **객체** `{meeting_id, agenda_id, line_ids[]}` 를 낸다(`application.py:1129-1133`, SPEC §8.1 대로). **F2 를 고치는 과정에서 새로 생긴 어긋남.** FE 가 `todo.reference` 를 **한 번도 읽지 않아**(grep 0) 런타임 무해 | 낮음 — 타입 한 줄 |
| **N2** | `viewModels.ts:906` | `description: string \| null` 인데 BE 는 `todo.description or ""` 로 **늘 문자열**. FE 타입이 넓기만 해 안전 | 아주 낮음 |
| **W9**(검수 1 잔존) | `viewModels.ts:891` | `author: string` — 계약·BE 는 `member_id \| null`(`application.py` line view). WP-001 은 늘 채우므로 지금은 안 터지고, AI 줄이 서는 WP-003 에서 터진다 | 낮음 — WP-003 전에 |
| **W5**(검수 1 잔존) | `entrypoints/http.py:466-473` | `MeetingVersionConflict` 가 어느 줄에도 안 걸려 `MeetingError` → **422**(409 가 아니라). D22 처리 목록 밖이라 손대지 않은 것으로 보인다 | 낮음 |
| **W6**(검수 1 잔존) | `entrypoints/http.py` `CreateMeetingRequest` | `model_config = ConfigDict(extra="forbid")` 없음(Update·Agenda 계열엔 있다) → 모르는 칸이 조용히 무시된다. D22 목록 밖 | 낮음 |

---

## 6. 검증 재현 (각 1회)

| 검사 | 명령 | 결과 |
|---|---|---|
| BE | `cd backend && uv run pytest -q tests/contract/test_meeting_core.py tests/architecture -m 'not integration'` | **45 passed** (21.34s) — 경계 14 + 회의 계약 31 |
| FE 타입 | `cd frontend && npx tsc --noEmit` | **0 에러** (exit 0) |
| FE 테스트 | `npx vitest run src/meetings/` | **26 passed** / 2 files (MeetingList 9 · MeetingDetail 17) |

- 경고 1건은 starlette `anyio.abc.BlockingPortal` deprecation — **무관·기존 부채**. 실패 0.
- 검수 1 대비 테스트가 늘었다: BE 회의 계약 +4(F1·F3·열람축·F2 각 1) · FE MeetingDetail 15→**17**(+2, F3 두 갈래).
- 서버·`make reset-demo`·`make local-stack`·dev 서버 **미실행**, 5176/8001 **미사용**. 전체 스위트·`-m integration` 미실행.

**git status**: 39항목(M 27 · D 2 · ?? 10). 검수 전후 동일 — **리뷰어가 만든 변경 0**, 산출물은 워크트리 밖 이 리포트 1개. 커밋·push·PR 없음.

---

## 7. 남은 것

1. **재발주할 것 — 없다.** F1~F4 와 D22·D19-3·D24 가 전부 반영됐고 회귀 테스트가 붙었다.
2. **다음 WP 에 얹을 것**: N1(`reference` 타입) · W9(`author` nullable, **WP-003 전에**) · N2 · W5 · W6.
3. **검수 1 §8 의 코디 결정 중 아직 열려 있는 것**: 「진행 중·정리 중의 사람 안건 편집」은 D22 가 **409 로 닫는 쪽**으로 정해져 해소됐다. `docs/domain-model.md` 의 allowed_paths 소유(검수 1 W7)와 `work-001` Open Issues 에 조회 시점 자동 취소를 적는 일(W3)은 **여전히 문서 쪽 숙제**로 남아 있다 — 코드 문제가 아니라 발주 문서 문제다.
