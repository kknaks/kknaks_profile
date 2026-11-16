# fix WP-BE-1 채팅 · 알림 서버 결과 보고

## 상태: done (로컬 day-local 실물 확인만 pending — 사용자 스택 금지)

## 수행 — 변경 파일(새 파일 없음 · migration 없음)

| 파일 | 무엇 |
|---|---|
| `backend/day/routers/api/chat.py` | `PUT /api/chat/rooms/{room_id}/title` (`rename`) — `mute` 와 같은 모양 · `writable_session` · 잘못된 id = 404 `chat_room_not_found` |
| `backend/day/schemas/chat.py` | `TitleRequest {title: str \| None}` — 칸 필수 · 모르는 칸 거절(`_Req` extra=forbid) |
| `backend/day/services/chat.py` | `rename()` — `actor`(활성 직원 403) → `_room_for(lock=True)`(방 범위 404 · 방 행 `FOR UPDATE`) → 그룹만(1:1 = 400 `chat_group_only` · detail 내부 문장) · `strip` · `MAX_TITLE` 40 재사용(`chat_invalid` → 400 `invalid_request` `field=title`) · 같은 이름 = Room 200 · 이벤트 0 · 아니면 `title` 만 바꾸고 커밋 뒤 `_room_events(지금 멤버 전부)` · 시스템 줄 · `seq` · `last_message_at` · 푸시 없음 · 로그 id 만 |
| `backend/day/services/chat_push.py` | `deliveries` 받는 사람에서 `notification_setting(kind='chat', is_enabled=false, deleted_at null)` 계정 제외(`_chat_off`) — 방별 `is_muted` 와 OR · 제목은 기존대로 발송 때 다시 읽은 `room.title` |
| `backend/day/services/notifications.py` | `_receivable` = `doctor_call`(원장 목록) → `chat`(채팅 활성 직원 — `chat.actor` 를 그대로 호출 · 복사 없음) · `CHAT_SETTING = PushKind.CHAT.value` · `put_setting` 무변경(받는 종류 검사로 `chat` 허용) |
| 시험 6 파일 | 아래 표 |

확인만: `models/misc.py` `NotificationSetting.kind` = String(migration 없음) · `NotificationKind`(DB enum) 에 `chat` 넣지 않음 · 새 이벤트 · 새 오류 코드 없음.

## 수용 항목 ↔ 시험

| 항목 | 시험 |
|---|---|
| C-A20(서버) #22 규칙 | `tests/day/chat/test_chat_api.py::test_그룹_이름_바꾸기_규칙`(지금 멤버 누구나 · 공백 · 40/41자 `field=title` · 빈 문자열 · 공백만 · null → 나열 이름 · 같은 이름 200 이벤트 0 · 칸 없음 · 모르는 칸 · 타입 400 · 시스템 줄 0 · `lastMessageAt` · 안 읽음 · 미리보기 그대로 · 푸시 발행 0) |
| C-A20 1:1 · 404 · 403 · 401 | `test_chat_api.py::test_그룹_이름_바꾸기_1대1_나간_사람_다른_병원_비활성` |
| C-A20 실시간 | `test_chat_stream.py::test_그룹_이름_바꾸기는_지금_멤버_전부에게_chat_room_만`(바꾼 사람 채널 포함 · 받는 계정 기준 `me` · 나간 멤버 · 같은 계정 B 병원 채널 · B 직원 0) |
| C-A20 동시 | `test_chat_concurrency.py::test_동시_그룹_이름_바꾸기는_직렬_나중_저장이_남는다`(다른 트랜잭션이 방 행을 잡으면 기다렸다가 그 위에 저장 · 동시 둘 다 200 · 시스템 줄 0) |
| C-A20 푸시 제목 | `test_devices_push.py::test_이름_바꾼_뒤_푸시_제목은_발송_때_읽은_새_이름`(+ 이름 없앰 → 받는 사람 기준 나열) |
| C-A14 · C-A21 · N-A13(서버) | `test_devices_push.py::test_채팅_전체_알림_끈_계정은_받는_사람에서_빠지고_방별_알림과_OR`(끈 계정 APNs 0 · `push_log` 0 · 저장 없음 = 받음 · 방별 `muted` 그대로 · 다시 켜면 방별대로) |
| N-A5 | `test_notifications_api.py::test_설정은_원장이면_doctor_call_채팅_활성_직원이면_chat`(원장 = 둘 · 간호 = chat · 다른 병원 코디 = chat · 차례 · PUT chat · 계정 단위(B 세션도 같은 값) · 받지 않는 종류 400 · 형식 400 · 계정 × 종류 한 행) · `::test_설정_시스템_계정_비활성_직원은_빈_목록` · `::test_설정을_끈_원장은_행_푸시_로그_없음`(응답 모양 갱신) |
| OQ-N6 이름 | `test_notification_units.py::test_채팅_설정_종류_이름은_채팅_푸시_kind_와_같다` |

## 계약 표(wp-plan §3) ↔ 구현

| 무엇 | 필드 | 구현 |
|---|---|---|
| #22 요청 | `PUT /api/chat/rooms/{roomId}/title` · Bearer · `{"title": string \| null}` · 모르는 칸 400 | 같음(칸이 없으면도 400 `invalid_request`) |
| #22 응답 | 200 `Room`(요청 계정 기준 — 기존 `q.room_views` 그대로라 id · kind · title · name · members · memberCount · muted · unread · lastMessage · lastMessageAt · createdAt · fromSeq · lastReadSeq 모두 같은 모양) · 같은 이름 200 이벤트 없음 | 같음 |
| #22 오류 | 400 `chat_group_only` · 400 `invalid_request` `field=title` · 404 `chat_room_not_found` · 403 `forbidden` · 401 | 같음(시험으로 다 봄) |
| 이름 바뀜 알림 | SSE `chat_room` `{"room": Room}` 지금 멤버 전부 | 같음 |
| 설정 읽기 | `{"items": [{"kind":"doctor_call",…},{"kind":"chat",…}]}` 받는 종류만 · 차례 · 저장 없으면 true | 같음 |
| 설정 쓰기 | `PUT {"kind":"chat","enabled":bool}` → `{items}` · 400 `setting_not_allowed` · 400 `invalid_request` | 같음 |
| 채팅 푸시 | `chat` 끈 계정 0 · 제목 = 발송 때 읽은 이름 | 같음 |
| 채팅 403 | 기존 그대로(무변경) | 같음 |

## 돌린 명령 · 수치

격리 스택(사용자 `day-local-*` · 11040/11042/11043 미사용): `docker compose -p daybetest` postgres · redis 를 127.0.0.1:11142/11143 · 일회용 자격(스크래치 env).

- 변경 전 회귀 확인: `scripts/test.sh -q backend/tests/day/chat backend/tests/day/notifications` → 106 passed · 2 failed(예상 — 옛 「doctor_call 만」 단정 · 이번에 계약대로 고침)
- `scripts/test.sh -q tests/day/chat/test_chat_api.py tests/day/notifications/test_notifications_api.py` → **35 passed**
- `scripts/test.sh -q test_chat_stream.py test_chat_concurrency.py test_devices_push.py` → **27 passed**
- `uv run pytest -q tests/day/notifications/test_notification_units.py` → **4 passed**
- `uv run ruff check day tests/day/chat tests/day/notifications` → All checks passed

## 스펙과 달라진 곳 · 물을 것

- 없음. 메모: `chat` 받는 종류는 `chat.actor`(채팅 API 의 403 판정)를 그대로 써서 「활성 직원」 정의가 한 곳.
- 설정 `chat` 은 계정 단위라, 활성 직원이 아닌 병원 세션(시스템 계정 등)에서는 바꿀 수 없지만 다른 병원 세션에서 끈 값은 적용된다(스펙 「계정 단위」 그대로).

## pending

- 로컬 day-local 로 API · SSE 실물 확인(계획 「실물 몫」) — 브리프가 사용자 스택 사용을 막아 하지 않음. 격리 스택 end-to-end 시험이 같은 경로를 덮는다.
- dev 배포 뒤 로그 · `push_log`(코디) · 실기기(사용자 §7 3 · 4).
