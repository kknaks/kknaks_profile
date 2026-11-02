# WORK-007 WP-FIX3 backend 결과 보고 — 공지 [저장] · 드래그(b4 #1)

## 상태: done

브랜치 `kknaksss/overall-board-2`(base main `64e1989`) · 커밋 · push 안 함. 워크트리의 `procedure/front/components/reservations/ScheduleTable.tsx` 변경은 frontend 워커 몫이다(backend 는 front 를 고치지 않았다).

## 수행 — 바뀐 파일

| 파일 | 내용 |
|---|---|
| `procedure/back/app/api/reservations.py` | `PUT /api/reservations/notice` 경로 더함(`require_real_board` → 가짜 모드면 403 `fake_board`) |
| `procedure/back/app/schemas/reservations.py` | `ReservationBoard.noticeEditable` · `NoticeRequest{date, noticeId?, content}`(모르는 필드 = 400) · `NoticeResponse{ok, notice \| null}` · `NOTICE_MAX = 2000` |
| `procedure/back/app/service/reservations.py` | `notice()` — §5.15 표 그대로: 날짜 형식 400 → trim 길이 > 2000 400 → 지난 날짜 409 `notice_past_date`(KOS 안 부름) → **KOS `get-notices` 다시 읽기(캐시 없음)** → 첫 번째 공지 기준으로 `change-content{id, content: trim 안 한 값}` / `create-notice{content: trim, releaseDateTimeUtc: 그 날 KST 00:00 의 UTC "…T15:00:00.000Z"}` / `delete-notice{id}` / 없음 + 빈 값 = 호출 없음 · `{ok:true, notice:null}` → `event_log(notice_save {date, action, noticeId, length})` → 그 날짜 캐시 비움 → 다시 읽어 응답. KOS 실패 = 기존 `kos_write` 공통(409 `kos_rejected` · 502 `kos_unavailable` · `event_log(kos_rejected)`). board 에 `noticeEditable = 날짜 ≥ 오늘(KST)` |
| `procedure/back/app/service/fake_reservations.py` | 가짜 board 에 `noticeEditable` |
| `procedure/back/tests/fake_kos.py` | 가짜 KOS 에 `change-content` · `create-notice` · `delete-notice`(소프트 삭제 · 빈 고치기 거절) · `get-notices deleted:false` 거르기 |
| `procedure/back/tests/test_resv_notice.py` (새) | 14 시험 — 4갈래(고치기 · 새로 쓰기 · 지우기 · 호출 없음) · 다시 읽기가 캐시보다 우선(둘째 create 막기) · 첫 번째만 · 지난 날짜 409(KOS 0 호출) · trim 2000 경계 · 날짜 400 · 캐시 비움 · `noticeEditable` · 409/502 · HTTP 401/400/502 |
| `procedure/back/tests/test_order.py` | `test_route_count_34` → **`test_route_count_35`**(예약 HTTP 16 · 합 35) |
| `procedure/back/tests/test_resv_contract.py` | board 키에 `noticeEditable` · 지난 날짜 false · 조작 403 목록에 `PUT notice` |

## 검증

- `cd procedure/back && uv run ruff check . && uv run pytest -q` → **All checks passed · 351 passed**(경고 1 = starlette httpx 폐기 예고 · 기존)

## 데모 실물 호출 (2026-10-27 · 날짜 2026-11-11 KST · ccc API 로)

- 방법: `TestClient(create_app(Settings()))`(앱 안에서 실행 — **포트 안 띄움** · 3700 · 8700 안 건드림) · `PROC_DB_PATH` = 스크래치 임시 DB · `PROC_FAKE_BOARD=false` · admin 로그인 → `PUT /api/reservations/notice`
- 시작 전 assert(값 출력 없음): `KOS_TENANT_ID` == `공지사항.har`(데모) 요청 경로 테넌트(HAR 안 테넌트 1개) → OK · `.env` · 환경에 `KOS_API_tenent`(운영) 없음 → OK

| 단계 | 요청 | 상태 | 응답 | 다음 board |
|---|---|---|---|---|
| 0 | GET board 11-11 | 200 | 공지 0 · `noticeEditable: true` | — |
| 1 쓰기 | `{date, noticeId:null, content:"[ccc 시험] 공지 쓰기 확인 — WP-FIX3"}` | 200 | notice(내용 같음) — `create` 경로 | 공지 1 · 내용 같음 |
| 2 고치기 | `{noticeId:<1 의 ccc id>, content:"[ccc 시험] 공지 고치기 확인 — WP-FIX3"}` | 200 | notice(내용 같음) — `change` 경로 | 공지 1 · 내용 같음 |
| 3 비우기 | `{noticeId:<같은 id>, content:""}` | 200 | `notice: null` — `delete` 경로 | 공지 0 |

- `event_log(notice_save)` = `create · change · delete` 3줄 · `kos_rejected` 0
- 반영 지연: 세 번 모두 바로 다음 board 에 보였다(캐시 비움 → 다시 읽기)
- **남긴 데모 흔적**: 데모 테넌트 2026-11-11 KST 에 **소프트 삭제된 공지 행 1개**(`deleted:true` · 마지막 내용 「[ccc 시험] 공지 고치기 확인 — WP-FIX3」). `deleted:false` 조회(= KOS 웹 · ccc)에는 안 보인다. KOS 에 완전히 없애는 명령은 없다(notice 리포트 §1). 다른 날짜 · 예약은 건드리지 않았다
- 실행 중 로그 `APNs JWT 서명 실패(FileNotFoundError)` 1줄 — 앱 시작 때 푸시 키 파일 경로(로컬 env)가 없어서 나는 기존 로그 · 공지와 상관없음 · 푸시 발송 대상 없음

## 드래그(b4 #1) — back 원인 없음

board 카드 `draggable` = `main ∈ {reserved, reception}`(§5.4 · OQ-714 그대로 · `reservation_rules.draggable`) · 이동 API(`POST …/move`)는 정원 · 구역 · 같은 날짜 · 길이 유지 검사 후 KOS `update-reservation` — 기존 시험(`test_resv_write.py` 이동) 통과. 「끌기 시작이 안 됨」은 이동 API 를 부르기 전 단계라 front 쪽 원인이다(frontend 워커 보고 참고).

## 계약 대조

| SPEC | 같음 / 다름 |
|---|---|
| §5.15 표 4갈래 · trim 규칙(고치기 = trim 안 함 · 새로 쓰기 = trim) · 2000 · 지난 날짜 409 · 다시 읽기 · 첫 번째만 · event_log · 캐시 비움 · 다시 읽어 응답 | 같음 |
| §7.2 `noticeEditable` · `notices` 배열 모양 그대로 | 같음 |
| §7.5 요청 · 응답 모양 · 409 `notice_past_date` 문구 「지난 날짜 공지는 고칠 수 없어요」 · 400 `invalid_request` | 같음 |
| §7.6 경로 35 | 같음 |
| §8 공지 줄 경로 · 본문 · `releaseDateTimeUtc` | 같음 |
| Q-143 응답 · 화면에 KOS id 없음 | 같음(시험이 응답에 KOS id 없음을 본다) |

## 이슈 · 코디가 확인할 것

1. **「공지 없음 + 빈 값」은 호출도 `event_log` 도 없다** — §5.15 「성공 = event_log」 는 KOS 쓰기가 있을 때로 읽었다. 이 경우도 남겨야 하면 한 줄 더하면 된다
2. 저장 직전 **다시 읽기(`get-notices`)가 실패**하면 `kos_write` 공통을 써서 `event_log(kos_rejected {op:"get-notices"})` 1줄 + 409/502 — 읽기 실패도 같은 오류 모양으로 맞췄다
3. 응답 · board 의 「첫 번째」 = 사본 순서(`released_at, id`) · 저장 대상 「첫 번째」 = KOS `get-notices` 응답 순(§5.15). 같은 날 둘 이상일 때만 다를 수 있다(OQ-770 · 데모는 날짜당 하나)
4. OQ-770(같은 날 둘째 `create-notice` 를 KOS 가 막는가)은 이번에도 시험하지 않았다(허가 밖) — ccc 는 다시 읽기로 막는다

---

## 추가 지시 1 (2026-10-27 · `reservation-fix3-backend-addendum-1.md`)

### 상태: done

| 지시 | 한 것 | 파일 |
|---|---|---|
| **W1** 저장 대상 | 요청 `noticeId`(ccc 행 id) → `kos_id`(`repo.notice_row(id_=…)`) → 저장 직전 다시 읽은 KOS 목록(`deleted:false`)에 **있으면 그것** · 없으면 KOS 응답 **첫 번째** · 그것도 없으면 `create-notice`(빈 값이면 호출 없음 · event_log 없음 — 그대로) | `app/service/reservations.py` `notice()` · `app/repository/repo.py` `notice_row()`(새 · 행 id 또는 kos_id · 지운 행 포함) |
| **W2-2** event_log noticeId | `event_log(notice_save).noticeId` = **저장 뒤 다시 읽은 행의 ccc id** — change = 고친 행 · create = 새 행(`create-notice` 응답 `data.id` → 다시 읽은 사본 행) · delete = 지운 행(사본에서 `deleted=1` 로 바뀐 그 행). 그래서 event 는 다시 읽기 **뒤에** 쓴다. 요청 값은 `requestedNoticeId` 로 따로 남긴다(기록용) | `app/service/reservations.py` |
| 응답 | change · create = **저장한 그 행**(같은 날 둘일 때 다른 행을 돌려주지 않게) · delete = `notice: null`(§7.5 「지웠거나 빈 날 = null」) | `app/service/reservations.py` |
| 시험 | `test_two_same_day_saves_the_one_screen_picked`(같은 날 둘 — 화면이 고른 둘째를 고침 · 응답 · event id = 둘째 · 고른 행이 KOS 에서 사라지면 첫 번째로) 더함 · create / delete 시험에 event `noticeId` = 새 행 / 지운 행 확인 더함 | `tests/test_resv_notice.py`(15) |

### 검증

- `cd procedure/back && uv run ruff check . && uv run pytest -q` → **All checks passed · 352 passed**(경고 1 · 기존)
- 데모 재호출 안 함(지시대로)

### 위 「이슈」 갱신

- 3번(첫 번째 순서 차이)은 W1 로 저장 대상이 화면이 고른 행이 되어 작아졌다 — 고른 행이 없을 때만 KOS 응답 첫 번째
- 지운 공지가 사본에 한 번도 없었던 행이면(화면이 본 적 없는 행) event `noticeId` = null

---

## 리뷰 r3 수정 (2026-10-27 · `reservation-review-code-r3-fix-instructions.md` W1)

- `event_log(notice_save)` 키 **`action` → `op`** — 모양 = `{date, op, noticeId, requestedNoticeId, length}`(`requestedNoticeId` · `length` 그대로). 값(`create` · `change` · `delete`)은 같다
- 파일: `procedure/back/app/service/reservations.py`(`notice()` event 한 줄) · `procedure/back/tests/test_resv_notice.py`(키를 보는 시험 3곳)
- 검증: `uv run ruff check .` → All checks passed · `uv run pytest -q` → **352 passed**
