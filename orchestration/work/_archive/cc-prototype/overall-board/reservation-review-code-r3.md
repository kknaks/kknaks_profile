# 리뷰 리포트 — overall-board 예약 현황 WP-FIX3 / code r3 (2026-10-27)

- 대상: 워크트리 `cc-prototype/overall-board` · branch `kknaksss/overall-board-2` · `64e1989` 이후 커밋 안 된 변경 전체(13 파일 `git diff` + 새 `procedure/back/tests/test_resv_notice.py`) — read-only
- 기준: SPEC-005 **0.4.0** §3.2 `notice_save` · §5.4 · §5.15 · §6.4 · §7.2 · §7.5 · §7.6 · §9 #11 · #46 · `reservation-review-doc-r3-dispositions.md` · `_RESUME.md` 2026-10-27 줄 · 화면 정본 = 배포된 웹 구현(D-60)
- 직접 돌린 결과(포트 안 띄움 · 파일 수정 없음):
  - `cd procedure/back && uv run ruff check . && uv run pytest -q` → **All checks passed · 352 passed**(경고 1 = 원래 있던 starlette/httpx 폐기 예고)
  - `cd procedure/front && npx tsc --noEmit && npm run lint` → **tsc 오류 0 · eslint 문제 0**

## 판정: WARN (FAIL 0 · WARN 3)

사용자 E2E(§9 #11 · #46)를 막는 결함은 없다. 드래그 원인 · 수정과 공지 back ↔ front 계약은 SPEC 과 맞다. `event_log` 키 이름 하나가 SPEC 과 다르다(W1).

## FAIL

없음.

## WARN

| # | 자리 | 내용 | 근거 | 고칠 사람 |
|---|---|---|---|---|
| W1 | `procedure/back/app/service/reservations.py:1016` | `event_log(notice_save)` payload = `{date, action, noticeId, requestedNoticeId, length}` ↔ SPEC = `{date, noticeId, op}`. **`op` 대신 `action`** 키를 쓰고, SPEC 에 없는 `requestedNoticeId` · `length` 가 더 있다. 값(`change`/`create`/`delete`) · `noticeId` 뜻(저장 뒤 다시 읽은 행 id · W2-2)은 SPEC 과 같다. 내용 값은 싣지 않는다(`length` 는 글자 수라 §3.2 「내용 값은 싣지 않음」 위반 아님). 시험 `tests/test_resv_notice.py:49` 도 `action` 으로 고정했다 | §3.2 `notice_save` 줄 | **backend**: `action` → `op` 로 바꾸고 시험 3곳(`:49` · `:60` · `:81`)을 같이 고친다. `requestedNoticeId` · `length` 를 남기려면 **planner** 가 §3.2 에 두 키를 더한다(어느 쪽이든 코디 결정 — E2E 영향 없음) |
| W2 | `procedure/front/app/(main)/reservations/live/page.tsx:94-96` | `goToday()` 는 이미 오늘을 보고 있어도(날짜가 안 바뀌어도) `leaveDate()` 를 불러 공지 편집을 버리고 토스트 「저장하지 않은 공지 편집을 취소했어요」를 낸다. 달력(`:171`)은 같은 날짜면 버리지 않게 막았는데 [오늘]만 빠졌다. 오늘 공지를 쓰다 [오늘]을 잘못 누르면 쓴 글자가 사라진다 | §5.15 「편집 중 날짜 이동 = 버림」(날짜가 바뀔 때만) | **frontend**: `if (date !== null) leaveDate()`(또는 `shownDate !== 오늘` 일 때만) |
| W3 | `procedure/front/components/reservations/ResvAside.tsx:114-119` | [수정하기] 다시 읽기(`GET board`) 가 끝나기 전에 날짜를 옮기면, `RequestsTab` 은 `key={board.date}` 로 새로 그려지지만 늦게 온 응답이 **옛 날짜**로 `setDraft` 한다. 화면엔 안 보이지만(`draft.date === board.date` 거름) 다음 날짜 이동 때 엉뚱한 「편집 취소」 토스트가 한 번 뜬다. 드묾 | §5.15 | frontend(선택 · 응답 시 날짜 확인) |

## 볼 것 대조

### 1. 드래그(b4 #1 · §5.4 · §9 #11) — 같음

- **원인 = 코드로 맞다**: 고치기 전 `cells` 는 `dragKey && over?.allowed` 이면 원본 카드를 건너뛰고 `over` 칸에 다시 넣었다(diff 삭제 줄). React 가 원본 DOM 을 언마운트 · 이동 → Chrome 이 드래그 원본을 잃고 끌기를 끝냄. 고친 뒤 `cells` 는 `board.cards` 만 본다(`ScheduleTable.tsx:98-109`) — 원본은 제자리(`dragging` → opacity 0.4) · 미리보기는 별도 복제 `CardView key="preview"`(`:299`, `pointerEvents:none` · `aria-hidden` · `draggable=false` · `onClick` 없음). dragstart 안 상태 바꿈은 `setTimeout 0`(`:290`)
- **클릭과 충돌 없음**: 원본 `onClick={onOpen}` 그대로 · 움직이지 않은 누르기는 dragstart 가 안 남. 미리보기는 누를 수 없음
- **끌 수 없는 카드**: `canDrag = card.draggable && !preview`(`:355`) → `draggable=false` · `onDragStart` 없음 · 커서 pointer. back `draggable` = `main ∈ {reserved, reception}` 그대로(back 변경 없음)
- **정원 찬 칸 막기**: `onDragOver` 판정(`:257-266`) 바뀐 것 없음 — 「그룹 없음」 · 구역 꺼짐 · `fullOf` → 빨간 점선 · `preventDefault` 안 함 · `onDrop` 이 `!o.allowed` 면 return. 제자리 허용 · 제자리 놓기 = 호출 없음. 미리보기도 제자리면 안 그림(`previewAt` `:111-112`)
- **KOS 거절 원위치 · 길이 유지**: `page.tsx:101-122` `move` 바뀐 것 없음(낙관 `moves` → 실패 `drop()` + `fail(e)` · 길이 = `end - start`)
- 칸 폭 = 미리보기 1장 더해 계산(`:118-124`) — 미리보기가 넘쳐 겹치지 않음
- 스크린샷 `fix3-drag-during.png` — 원본 제자리 흐림 + 동남아 11:00 점선 미리보기 확인

### 2. 공지 back ↔ front 계약(§5.15 · §7.2 · §7.5) — 같음

| 항목 | back | front | 판정 |
|---|---|---|---|
| 요청 `{date, noticeId?, content}` | `NoticeRequest`(`_Req` = 모르는 필드 400 · `noticeId: StrictInt \| None`) | `api.saveNotice(date, noticeId, content)` · content trim 안 하고 보냄 | 같음 |
| 응답 `{ok:true, notice \| null}` | `NoticeResponse` · delete · 빈 날 = null · KOS id 없음(시험 `:47`) | `put<{ok; notice: ResvNotice \| null}>` | 같음 |
| 409 `notice_past_date`(KOS 안 부름) | `day < 오늘(KST)` → Conflict 「지난 날짜 공지는 고칠 수 없어요」 · KOS 호출 전 · 시험 `test_past_date_409_without_kos` | 실패 = `onError` 토스트 + 편집 유지 | 같음 |
| 400 | 빈/틀린 날짜 · trim > 2000 · 모르는 필드 · 순서 401 → 400 → 502 | — | 같음 |
| `noticeEditable` | board · 가짜 board 모두 `day >= today` | `editable && [수정하기]` | 같음 |
| 저장 대상 | 요청 `noticeId` → `notice_row(id_)` → `kos_id` 가 다시 읽은 `deleted:false` 목록에 있으면 그것 · 없으면 KOS 첫 번째 · 없으면 create(`:998`) | `noticeId` = [수정하기] 때 다시 읽은 첫 공지 id | 같음(처분 W1) |
| 빈 값 | 대상 있음 = `delete-notice` · 없음 = 호출 0 · event 0 | 그대로 보냄(back 이 정함) | 같음(W2-1) |
| trim 2000 | `len(strip()) > 2000` → 400 | `draft.text.trim().length > 2000` → [저장] 끔 · 빨강 | 같음(W2-3) |
| change = trim 안 한 값 · create = trim · KST 0시 UTC | `:1005` · create `releaseDateTimeUtc=kos_utc(start)` · 시험 「…T15:00:00.000Z」 | — | 같음 |
| 캐시 비움 · 다시 읽어 응답 | `after_write` → `ensure_day` → 사본 행 | 성공 → `refreshSoon()` · 다음 응답까지 응답 공지 표시 | 같음 |
| 편집 중 날짜 이동 = 버림 + 토스트 | — | `leaveDate()` ‹ › · [오늘] · 달력 | 같음(W2 는 [오늘] 같은 날짜 경우) |
| 실패 = 편집 유지 · 폴링이 안 덮음 | — | `save` catch 에서 `setDraft(null)` 안 함 · draft 는 page 상태 · `RequestsTab key=board.date` 라 폴링에 리마운트 없음 | 같음 |
| 가짜 모드 403 | `dependencies=write`(require_real_board) · contract 시험 OPS 에 넣음 | — | 같음 |

### 3. `event_log(notice_save)` 키 — **다름 → WARN W1**

SPEC §3.2 = `{date, noticeId, op}` / 구현 = `{date, action, noticeId, requestedNoticeId, length}`. **구현 쪽이 SPEC 과 다르다**(키 이름 `op` → `action` · 키 2개 더함). backend 보고 본문(「`{date, action, noticeId, length}`」)도 SPEC 과 다른 채로 「계약 대조 = 같음」 이라 적었다. 사용자 E2E 에는 안 보이는 기록 칸이라 FAIL 아님.

### 4. 회귀 — 없음

- 시술 현황(SPEC-003): 이번 diff 는 `procedures` 쪽 파일을 건드리지 않음 · pytest 352 전부 통과
- 경로 수 35: `test_route_count_35`(예약 HTTP 16 · `PUT /api/reservations/notice` 있음 · `len == 35`) — §7.6 0.4.0 과 같음
- 가짜 모드 403: `test_resv_contract.py` OPS 에 notice 더함 · 통과
- 기존 시험: 이름 바뀐 것은 `test_route_count_34 → 35` 하나(SPEC 지시)

### 5. DS · public 누출 — 문제 없음

- diff 안 native `<select>` · `<input>` · `<textarea>` · `<button>` · `type="date|time"` **0** — 공지는 medikit `Textarea` · `Button`
- 실명 · KOS 실 id · 테넌트 · 토큰 · 키 **0**(시험은 가짜 `ntc-1` · `고객 A` 류 · front 응답 · 화면에 KOS id 없음)

## 고객이 실물에서 만날 자리

- §9 #46 (a)~(h) 는 실 KOS 로 아직 front 에서 안 눌러 봤다(front = 가로채기 · back = 11-11 데모 create/change/delete 3번 실호출 · 바로 다음 board 에 보임). 코디 데모 E2E 필요
- 오늘 공지를 고치다 [오늘] 을 누르면 쓴 글자가 사라짐(W2)
- 2000자 근처에서 앞뒤 공백이 많은 글: front · back 모두 trim 기준이라 통과하지만 `change-content` 는 trim 안 한 값을 보낸다(SPEC 대로). KOS 가 원문 길이로 2000 을 재면 거절(→ 409 `kos_rejected` 토스트 · 편집 유지) 가능 — 실물에서 관찰되면 기록
- 데모 흔적: 2026-11-11 KST 소프트 삭제 공지 1행(backend 보고 · `deleted:false` 조회에는 안 보임)

## 참고(기존 부채)

- frontend 보고 이슈 2: 끄는 중 그 예약이 폴링으로 사라지면 `dragend` 가 안 와 끄는 상태가 남을 수 있음(다음 끌기에서 풀림 · 드묾)
- 저장 직전 `get-notices` 실패도 `kos_write` 공통으로 `event_log(kos_rejected {op:"get-notices"})` — 읽기 실패를 「rejected」 로 남김(시험 `test_kos_reject_409_and_unavailable_502` 가 고정 · SPEC 에 따로 없음)
- Next.js 16.4.0 보안 업그레이드 안내(범위 밖)
