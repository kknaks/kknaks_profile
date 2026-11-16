# fix WP-BE-3 읽음 표시 서버 결과 보고

## 상태: done · migration 0 · 새 의존성 0 · 정정 1(correction-read-1.md) 반영

## 변경 파일 (서버 4 · 시험 5)

| 파일 | 무엇 |
|---|---|
| `backend/day/queries/chat.py:248-264 · 296-305` | `room_views` 의 **기존** 멤버 쿼리에 `from_seq` · `last_read_seq` 칸만 더함(새 쿼리 0) → `members[]` 항목에 `lastReadSeq` · `fromSeq` |
| `backend/day/services/chat.py:949-1012` | 읽음 #15 — 조건부 `UPDATE … WHERE last_read_seq < target RETURNING`(target = `least(seq, 방 last_seq)`)로 **실제로 오른 요청만** 행을 받음 · 안 오르면 `last_viewed_at` 만 갱신(기존 동작 그대로) · 올랐으면 커밋 뒤 그 방 지금 멤버(`_current_members` 재사용) 중 읽은 사람 아닌 계정에게 `chat_member_read {roomId, accountId, lastReadSeq}` · 나에게 가는 `chat_read`(seq>0) · #15 응답 · `unreadRooms` 그대로 |
| `backend/day/services/chat_events.py:8-11 · 41 · 85` | `EVENTS` 에 `chat_member_read`(구독 목록이 이것을 씀) · 주석 7종 |
| `backend/day/routers/api/chat.py:20-22` | 머리 주석만 7종(코드 변경 없음 — 스트림은 `chat_events.EVENTS` 를 구독) |
| 시험: `tests/day/chat/test_chat_api.py` · `test_chat_stream.py` · `test_chat_concurrency.py` · `test_chat_units.py` · `test_chat_queries.py` | 아래 표 |

확인만: `models/misc.py`(칸 있음) · `test_column_snapshot` · `test_constraints` 무변경 통과. 목록 `unread` · 탭 배지 · 푸시 · #15 응답 · `Message` 무변경.

## `Room` 을 만드는 자리 전수(grep `room_views(` · `"members"` · `_room_view(` · `_room_events(`)

`Room` dict 를 만드는 곳은 **`queries/chat.py` `room_views` 한 곳**(`"members": member_list` 는 `:320` 부근 하나뿐). 모든 길이 이것을 지난다:

| 응답 · 이벤트 | 지나는 길 | 자리 |
|---|---|---|
| #2 `GET /rooms` | `chat.rooms` → `q.room_views` | `services/chat.py:470` |
| #3 1:1 열기 · #4 그룹 만들기 · #5 초대 · #22 이름 바꾸기 응답 | `_room_view` → `q.room_views` | `:485 · 527 · 564 · 661 · 666` |
| `chat_room` 이벤트(만들기 · 1:1 · 초대 · 나가기 뒤 남은 멤버 · 알림 끄기 · 이름 바꾸기 · 숨김 풀림 · 전달) | `_room_events` → `q.room_views` | `:256-266`(호출 `:359 · 486 · 528 · 565 · 593 · 635 · 668 · 1099`) |

라우터 · 다른 서비스에서 `Room` 을 직접 만드는 곳 없음.

## 수용 항목 ↔ 시험

| 항목 | 시험 |
|---|---|
| C-A24 `members[].lastReadSeq` · `fromSeq`(목록 · 만들기 · 초대 · 이름 바꾸기) · 나간 멤버 빠짐 · #15 응답 칸 그대로 | `test_chat_api.py::test_Room_members_에_읽은_자리와_경계가_있다` |
| 정정 2 W4 — #3 1:1 열기(`POST /rooms/direct`) 응답 `members[]`(열 때 · 다시 열 때 · 보낸 사람 읽음 반영) | `test_chat_api.py::test_1대1_열기_응답의_Room_members_에도_읽은_자리와_경계` |
| C-A24 오를 때만 · 받는 사람(지금 멤버 − 읽은 사람) · 읽은 사람은 `chat_read` 만 · 같은/낮은/0 = 0 · 나간 멤버 · 같은 계정 B 병원 채널 · B 직원 0 · 방 끝으로 잘림 | `test_chat_stream.py::test_읽음이_오를_때만_다른_지금_멤버에게_chat_member_read` |
| C-A24 동시 읽음 단조 · 이벤트는 오른 만큼(같은 seq 6번 = 멤버마다 1번 · 섞인 seq = 끝값 7 · 값 중복 없음) | `test_chat_concurrency.py::test_동시_읽음은_단조_chat_member_read_는_오른_만큼` |
| C-A24 쿼리 수 늘지 않음(멤버 목록 쿼리 하나가 두 칸을 같이 읽음) · 기존 「방 수와 무관」 그대로 | `test_chat_queries.py::test_읽음_표시_칸은_멤버_쿼리에_칸만_더한다` · `::test_방_목록_쿼리_수는_방_수와_관계없다` |
| C-A11 7종 | `test_chat_units.py::test_채팅_이벤트는_7종` · 기존 `test_chat_stream.py::test_여섯_이벤트가_받을_사람에게만_간다`(통과) |
| **정정 1** 보내기는 `chat_member_read` 를 내지 않음 · 보낸 사람 `lastReadSeq` 는 다음 `Room.members[]` 에 그 seq | `test_chat_stream.py::test_보내기는_chat_member_read_를_내지_않고_보낸_사람_읽음은_다음_Room_에`(답장 뒤 다른 멤버 채널 = `chat_message` 만 · 뒤따르는 읽음 = 안 오름 → 이벤트 0 · 목록의 원장 `lastReadSeq` = 3) |

## §3 읽음 계약 표 ↔ 구현

| 계약 | 구현 |
|---|---|
| `Member` = `id · name · role · active · me · lastReadSeq · fromSeq`(`chat_member.last_read_seq` · `from_seq`) | 같음 |
| `Room` 의 모든 길(목록 · 만들기 · 초대 · 이름 바꾸기 · `chat_room`)에 같은 모양 | 같음(한 함수) |
| SSE `chat_member_read` `{"roomId": uuid, "accountId": uuid, "lastReadSeq": int}` | 같음(문자열 uuid · int = 새 읽은 자리) |
| 받는 사람 = 그 방 지금 멤버 중 읽은 사람 아닌 계정 · 그 방 병원 채널 | 같음(`left_at` null · `deleted_at` null 멤버 − 나 · 채널 = 방 병원) |
| #15 가 실제로 올렸을 때만 · 커밋 뒤 | 같음(`RETURNING` 행이 있을 때만 · `_Out` → `_finish` 가 커밋 뒤 발행) |
| 읽은 사람 = 기존 `chat_read` | 같음 |
| 정정 1 ③ 서버 그대로 · 보내기에서 이벤트 더 내지 않음 | 같음(보내기 코드 무변경) |

## 정정 2 확인(W4)

- 전수 표에 #3 1:1 열기가 이미 있다(`_room_view` → `room_views` · `services/chat.py:485`). 시험에는 없었으므로 1건 추가(위 표). 서버 코드 변경 없음.
- 추가 뒤 격리 스택 `scripts/test.sh -q tests/day/chat/test_chat_api.py` → **20 passed**(다시 `down -v`).

## 수치

- 격리 스택(`docker compose -p daybetest` · 127.0.0.1:11142/11143 · 일회용 자격 · 끝나고 `down -v` — 볼륨 0) · 사용자 `day-local-*` · 11040/11042/11043 무변경
- 구현 직후 기존 채팅 시험 `scripts/test.sh -q tests/day/chat` → 92 passed(깨진 것 0)
- 고친 시험 5 파일 `scripts/test.sh -q …` → **78 passed**
- `uv run ruff check backend` → All checks passed · `ruff format --check` → 222 files already formatted
- `uv run pytest -q -m "not infra"` → **848 passed**, 299 deselected
- 격리 스택 `scripts/test.sh -q` 전체 → **1147 passed**(경고 1 = 기존 `fastapi.testclient` deprecation)

## 스펙과 다른 곳 · 물을 것

1. 처음 쓴 기대(「그룹을 만든 사람은 초대 시스템 줄까지 읽음」)는 틀렸다 — 지금 서버는 **시스템 줄로 누구의 `last_read_seq` 도 올리지 않는다**(만든 사람도 0). 기존 동작이라 바꾸지 않고 시험을 실제 동작에 맞췄다. 앱 셈엔 영향 없음(시스템 줄엔 숫자 없음 · 정정 1 ① 도 시스템 줄 제외).
2. 받는 사람에 비활성 직원 멤버도 포함된다(스펙 = 「지금 멤버 중 읽은 사람 아닌 계정」 그대로 · 비활성 연결은 스트림 검사가 끊음). 비활성을 빼야 하면 알려 달라.
3. 그 밖 다른 곳 없음. 정정 1 은 서버 코드 변경 없이 시험 1건으로 반영.

## pending

- 로컬 day-local 두 계정 SSE 실물(계획 「실물 몫」) — 사용자 스택 금지로 하지 않음 · 격리 스택 끝에서 끝 시험이 같은 경로(실제 앱 · Redis pub/sub)를 덮음.
- 앱 C-A25(mobile) · 실기기(사용자 §7). 커밋 · push 없음.
