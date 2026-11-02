# WP4-BE 결과 보고 — 메시지함 → AX(서버)

## 상태: done (커밋하지 않음 · WP3 `cfc2e1c` 위 워크트리 변경)

- 근거: WORK-012 「Phase WP4-BE」 · SPEC-008 v0.6.0 §2.8 · §2.9 · §4.4 · §4.8 · §5 · DEC-009 D-27 · D-29~D-37 · **WP4 계약 고정 1**(`context_references[].turn_id` · `label`)
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/`
- 외부: 슬랙·Gmail·AX provider 는 시험에서 전부 대역이다. 실물 확인 거리는 §5에 따로 적었다

## 1. 계약 체크박스 6/6

| # | 계약 | 구현 위치 |
|---|---|---|
| 1 | **`inbox_message` 참고 자료** — 나열 지점 다섯 + 해석기(소유 404 · 소프트 딜리트 404 · 판 1) | **BE 몫 넷**: 명령 모델 `B/modules/ax_execution/conversation_commands.py:20` · HTTP 요청 모델 `B/entrypoints/http.py:438` · 해석기 `B/platform/conversations.py:1035`(`_inbox_message` · `INBOX_MESSAGE` `:1006`) · 도구 설명 `B/modules/ax_execution/tool_catalog.py:54`. 다섯째 `viewModels.ts` 는 FE 몫이다.<br>해석기 규칙:<br>— 남의 연동 · 지운 방 · 지운 연동 · 없는 id 는 `ConversationNotFound` → **404**(기존 task·work_request 의 「못 찾음」은 지금처럼 422)<br>— 판이 1 이 아니면 422(stale)<br>— `summary` = 「슬랙 메시지」·「메일 메시지」(바뀌지 않는 글자 — 실행 직전 낡음 검사가 방 이름 변경으로 깨지지 않게)<br>접수 때 한 번 + 실행 직전(`request_for`) 한 번 다시 해석한다(지금 규칙 그대로) |
| 2 | **맥락 조합 함수 하나**(입구와 분리) — 채널 위아래 100줄 · 스레드 = 스레드 전체 · 메일 = 그 메일 · 줄 모양 + `target` · 원문 JSON 제외 · 멘션 이름 풀기 · 메일 안전본 글자 | 새 모듈 `B/modules/external_channels/message_context.py` — `MessageContextComposer.compose(member_id, message_id)` `:227,238`. HTTP·대화를 모른다(회원 id·메시지 id 만) → 다음 판 자동 추천이 같은 함수를 부른다.<br>조합 규칙:<br>— 채널(최상위) = 위 100 + 그 메시지 + 아래 100(최상위 흐름 · 모자라면 있는 만큼). 답글 본문은 넣지 않고 `thread_reply_count` 만<br>— 스레드 답글 = 그 스레드 전체(부모 포함)<br>— 메일 = 한 줄(제목 + 본문 글자 · 첨부 이름)<br>— 줄 = `{at(+09:00), sender, text, attachments, thread_reply_count}` + 고른 메시지만 `target: true`<br>— 슬랙 글자는 `render_slack_text` `:167`(화면 `parseInline` 과 같은 규칙: `<@U>`→`@이름`(방 이름표) · `<#C|이름>` · `<!here>` · `<url\|글>` · 엔티티)<br>— 삭제 표지 = 「(삭제된 메시지)」 · 수정 = 「… (수정됨)」<br>— 메일 글자는 `safe_html_text` `B/modules/external_channels/inbox_html.py:368`(소독본 → 글자 · `<details>` 인용·`<style>` 제외 · 2만 자 상한)<br>**내부 조회**(공개 API 아님): `owned_message` · `room_neighbors`(`(sent_at,id)` 앞뒤 · `ix_external_messages_room_sent_at`) · `thread_messages` — `B/platform/external_channels_inbox_store.py:226,281,299` |
| 3 | 프롬프트에 맥락 JSON 을 **덩어리로**(한 줄 요약과 별도) | 실행 직전 조합 → `context_references[].context`(JSON 글자 = `{label, source, room, range, lines}`) `B/platform/conversations.py:335` → Codex `B/platform/codex_cli.py:594` · Claude `B/platform/claude_cli.py:360` 이 「Inbox message context …」 절로 따로 싣는다(기존 `- type:id: summary` 한 줄은 그대로).<br>**WP4 계약 고정 1**: 조합 때 만든 한 줄을 `conversation_context_references.label` 에 남기고, 대화 응답 `context_references[]` 에 `label` 을 싣는다(`turn_id` 는 원래 있었다) — `B/platform/conversations.py:850` · 결과 타입 `B/modules/ax_execution/conversation_results.py:58`. 조합 전은 `null`.<br>모양: `슬랙 · #채널 · {MM/DD HH:MM}~{MM/DD HH:MM} · N건` / `슬랙 · 스레드 · N건` / `카톡 · {방 이름} · … · N건` / `메일 · {제목}` |
| 4 | **업무 출처** — 원래 메시지를 남김 · 업무 상세 `origin.message` · 방 메시지·메일 응답 `made_task_count` | 칸: `tasks.source_inbox_message_id` · `work_requests.source_inbox_message_id`(외래 키 없음 · 부분 인덱스 `ix_tasks_source_inbox_message_id`) `B/platform/persistence.py:939,974,1724`.<br>남기는 자리: 확정 실행 `B/platform/actions.py:729`(`_record_message_origin` · 대상 `MESSAGE_ORIGIN_ACTION_TYPES` `:678` = `task.create_self`·`task.assign`·`work_request.create`). 그 확정이 만든 업무(`source_action_item_id`)와, 요청이면 요청 · 요청과 함께 선 업무에 같은 메시지를 적는다.<br>`origin.message = {message_id, source_kind, room_id, label}` — 포트 `MessageOriginPort` `B/modules/work/application.py:196` → 투영 `:2494,2522` · 결과 타입 `TaskOriginMessage` `B/modules/work/task_results.py:169` · 어댑터 `message_origins` `B/platform/external_channels_inbox_store.py:241` · 조립 `B/bootstrap/application.py:4973`. 「판단 보기」(`origin.source`)는 그대로이고 원래 메시지가 함께 선다.<br>`made_task_count` = 그 메시지를 출처로 남긴 **업무** 수(요청은 보낼 때 업무가 함께 서므로 업무만 센다 — 두 번 세지 않는다) `:269` → `B/modules/external_channels/inbox.py:585`(메일) · `:622,649`(방 메시지) |
| 5 | **`inbox.message_updated` 사건** — `{message_id, room_id\|null}` · 사용자 사건 채널 · **업무 확정 커밋 뒤** | 타입 `UserEventType.MESSAGE_UPDATED` `B/modules/external_channels/events.py:39`. 확정 실행이 `ActionServices.message_origin_recorded` `B/platform/actions.py:207,767` 로 알리고, 조립층 `_announce_message_updated` `B/bootstrap/application.py:1771`(연결 `:4921`)이 **확정 세션의 커밋 뒤 훅**(`_after_session_commit`)으로 새 세션에서 NOTIFY 한다 — 받는 사람 = 그 메시지의 연동 주인 · 본문 없음. PostgreSQL 이 아니면(시험) `application.local_user_events` 에 남는다 |
| 6 | **012 나간 방** — 그 회원의 방 / 보관·삭제는 고른 회원 전부 · 즉시 `paused` · 사건 · 운영 앱 구독 목록 | `B/modules/external_channels/sync.py`:<br>— 이벤트 표 `SLACK_LEFT_EVENTS` `:186` · `SLACK_CLOSED_EVENTS` `:192` · 구독 목록 상수 `SLACK_ROOM_CLOSURE_SUBSCRIPTIONS` `:200`<br>— 분기 `:255` → `_slack_room_closed` `:286`<br>나간 방은 그 회원의 방만 내린다. `member_left_channel` 은 `event.user` 로, `channel_left`·`group_left` 는 그 토큰의 주인(`authorizations[0].user_id`)으로 찾는다. 누구인지 모르면 아무 방도 내리지 않는다. 보관·삭제는 그 `(team, channel)` 을 고른 모든 회원의 방을 내린다.<br>→ `set_room_access(ok=False, reason=left_channel\|channel_archived\|channel_deleted)` = 즉시 `paused` + `room_meta.access_lost` + 상태가 바뀌면 `integration.changed`(기존 `_changed`) → 다음 이벤트부터 팬아웃에서 빠진다. 같은 실행의 재확인이 「보인다」 로 되살리지 않게 그 방을 확인됨으로 둔다.<br>저장소 `slack_channel_rooms` `B/platform/external_channels_sync_store.py:133` · `RoomState.slack_user_id` `:69`.<br>**보강**: 실행마다의 재확인이 `is_archived` 방도 `paused` 로 내린다 `sync.py:514`(보관 이벤트를 놓쳤을 때) |

## 2. 운영 슬랙 앱 — 이벤트 구독 추가 목록 (반영 단계용)

레포에 앱 매니페스트가 없다 — 운영 슬랙 앱 설정의 **Event Subscriptions → Subscribe to events on behalf of users**(user events)에 아래 7개를 **더한다**(코드 상수 `SLACK_ROOM_CLOSURE_SUBSCRIPTIONS`):

| 이벤트 | 처리 | 슬랙이 요구하는 권한(사용자 토큰 · 확인 필요) |
|---|---|---|
| `member_left_channel` | 그 회원의 방 | `channels:read` / 비공개 `groups:read` |
| `channel_left` | 그 회원의 방(토큰 주인) | `channels:read` |
| `group_left` | 그 회원의 방(토큰 주인) | `groups:read` |
| `channel_archive` | 고른 모든 회원의 방 | `channels:read` |
| `group_archive` | 고른 모든 회원의 방 | `groups:read` |
| `channel_deleted` | 고른 모든 회원의 방 | `channels:read` |
| `group_deleted` | 고른 모든 회원의 방 | `groups:read` |

- SPEC §5 의 여섯에 `group_deleted` 를 더했다 — 비공개 채널 삭제의 짝이다.
- 사용자 토큰에 `channels:read`·`groups:read` 가 이미 있는지(연결 때 받는 scope)는 반영 단계가 앱 설정에서 확인한다. 없으면 권한 추가 → 재동의가 따른다.

## 3. Code Surface WP4 대비 닿은 자리

| 행 | 닿은 자리 |
|---|---|
| 참고 자료 나열 지점 | 바꾼 넷(위 1) · 함께 보는 곳: `conversations.py:41,54,174`(입력 그대로 통과 · 변경 없음) · `platform/conversations.py`(해석 · 실행 직전 조합 · 응답 `label`) · `bootstrap/application.py`의 해석기 사용처(변경 없음 · 같은 해석기) · 저장 `persistence.py:774`(`label` 칸) |
| 프롬프트에 싣는 자리 | `codex_cli.py:594` · `claude_cli.py:360` |
| 메시지 응답 | `inbox.py`(`MailView`·`RoomMessageView` 에 `made_task_count` · 포트 `made_task_counts`) · 저장소 내부 함수 넷 |
| 업무 출처 | 확정 실행 분기(`actions.py` `execute` → `_record_message_origin`) · 투영(`work/application.py`) · 결과 타입 · 사건(커밋 뒤). **생성 경로 시그니처(`create_self`·`assign_task`·`create_work_request`)는 바꾸지 않았다** — 확정 직후 같은 트랜잭션에서 `source_action_item_id` 로 찾아 적는다 |
| 012 나간 방 | `sync.py` · `sync_store.py`. 봉투(`external_slack.py:388-396`)는 이미 모든 `events_api` 를 넘긴다 — 변경 없음 |
| **표 밖** | `docs/domain-model.md`(외부 채널 절에 한 항목) · 운영 SQL 둘(§4) |

## 4. 스키마 · 인벤토리

- **운영 SQL**(이미지보다 먼저):
  - `backend/migrations/manual/2026-10-07-inbox-message-origin.sql`
    - nullable 칸 셋: `tasks.source_inbox_message_id` · `work_requests.source_inbox_message_id` · `conversation_context_references.label`
    - 격리 검증용으로 인덱스도 함께 놓는다 · `IF NOT EXISTS` 라 재적용 가능
  - `…origin.concurrent.sql` — 운영 인덱스. `CREATE INDEX CONCURRENTLY` 를 사람이 트랜잭션 밖에서 돌린다
- **로컬**: `make sync-demo-schema` 가 칸 셋을 만든다(postgres 시험으로 확인). 인덱스는 기존 표라 만들지 않는다(기존 규칙).
- **운영 인벤토리**: `docs/unified-operations-inventory.json` 에서 **diff 난 8항목만** 패치했다. 전부 도구다:
  - `conversations` · `conversation` · `conversation_create` · `conversation_message_send` · `conversation_turn_cancel` — 출력에 `label` · 입력 종류에 `inbox_message` · 설명
  - `my_task_list` · `task_list` · `task_get` — 출력 `origin.message`
- `docs/domain-model.md` 를 레포 규칙대로 갱신했다(보고 대상).

## 5. 검증 (바꾼 부분 관련 시험만)

| 명령 | 파일 | 결과 |
|---|---|---|
| `make test-contract-serial FILES="…"` | `tests/architecture` · `tests/unit/test_ax_work_lookup_policy.py` · contract: **`test_inbox_message_context.py`(새 19)** · `test_external_inbox.py` · `test_external_sync.py`(+나간 방 9) · `test_external_channels.py` · `test_kakao_ingest_and_profile.py` · `test_conversation_lifecycle.py` · `test_conversation_pagination.py` · `test_conversation_command_tools.py` · `test_answer_resources.py` · `test_action_center.py` · `test_task_origin.py` · `test_task_actor.py` · `test_task_creation_contract.py` · `test_mcp_action_items.py` · `test_unified_commands.py` · `test_unified_queries.py` · `test_mcp.py` · `test_codex_cli.py` · `test_claude_cli.py` | **462 passed · 1 failed** → 실패 1건은 `test_task_origin.py` 의 `origin` 정확 비교(새 칸 `message: null`)라 기대값에 한 줄을 더했고, 재실행 **15 passed** |
| `AX_POSTGRES_TEST_URL=… uv run pytest -m integration -n0` | **`test_inbox_message_origin_postgres.py`(새 3)** · `test_external_channels_postgres.py` · `test_postgres_integration.py`(+ 대역 import 경로 `test_meeting_rooms.py`) | **51 passed** |
| 인벤토리 drift | `tests/architecture/test_operation_inventory.py` | 패치 뒤 **45 passed**(architecture 전체) |

**새 시험이 잡는 것**:
- 참고 자료: 접수·`label` null · 남의 메시지 404 · 없는 id 404 · 지운 방·연동 404 · 판 2 = 422
- 조합:
  - 100줄 경계(201줄 · `target` 가운데 · 라벨 시각·건수) · 방 첫머리·끝 「있는 만큼」
  - 답글 본문 제외 + `thread_reply_count` · 스레드 전체 · 메일 한 통(인용·HTML·스크립트 제외 · 첨부 이름)
  - 줄 모양(원문 blocks·reactions 없음) · 멘션·채널·링크 풀기 · 삭제 표지 · 카톡 모양 · 남의 메시지
- 실행 직전 조합이 provider 요청과 대화 응답 `label`/`turn_id` 에 실림 · 프롬프트 덩어리(Codex·Claude)
- 출처:
  - `task.create_self` → `origin.message` + `made_task_count` 1 + 사건 1(받는 사람·`room_id`)
  - `work_request.create`(단계 카드로 **다음 턴**에 제안) → 요청·업무 둘 다 · 메일 `made_task_count`
  - 메시지 없는 대화 → 표시·사건 없음 · 지운 연동의 출처는 이름 없는 링크 + 메일 404
- 나간 방 팬아웃 두 회원 대역: 나간 사람 방만 `paused` + 다음 이벤트는 남은 사람에게만 · 같은 실행에서 안 되살아남 · `channel_left`/`group_left` 의 `authorizations` · 보관·삭제 넷 = 둘 다 `paused` · 재확인의 `is_archived` · 구독 목록 상수
- postgres: 원래 메시지 칸 왕복 · 운영 SQL 이 옛 DB 에 칸 셋 + 인덱스(재적용 포함) · `schema_sync` 가 칸 셋

전체 `make test` · `make verify` 는 돌리지 않았다(코디 지시).

## 6. 실물 확인 거리 (코디 E2E)

1. 슬랙 테스트 채널을 **실제로 나가** 그 회원 방이 `paused` 가 되는지. 운영 앱에 §2 구독이 더해진 뒤라야 이벤트가 온다. 슬랙이 `member_left_channel` 을 사용자 토큰 구독으로 나간 본인에게 보내는지, `channel_left` 만 오는지가 실물에서 갈린다 — 둘 다 받게 해 두었다.
2. 실메시지 1건으로 맥락 JSON 조합 — 채널 메시지 1 · 스레드 답글 1 · 메일 1. 실제 Slack `text` 의 멘션·링크 모양, Gmail 안전본 글자가 읽을 만한지.
3. 운영 SQL 적용 순서: 칸 셋 → 이미지 → 인덱스(concurrent).

## 7. 판단 · 미결

1. **「그 턴의 참고 자료」**: 「제안을 낸 턴까지 그 대화에 실린 가장 최근 메시지 참고 자료」로 읽었다. AX 업무 생성은 단계 카드로 몇 턴에 걸칠 수 있다(「이 메시지 읽고 업무 생성해 줘」 → 질문·답 → 제안). 새 메시지를 실으면 그것이 이긴다. 문자 그대로 「같은 턴」만으로 좁혀야 하면 한 줄로 바꿀 수 있다 — 코디 판정 거리.
2. **`origin.message` 의 이름 노출**:
   - 보는 사람이 그 메시지의 주인이고 연동·방이 살아 있을 때만 「슬랙 #채널」·「메일 {제목}」 을 싣는다.
   - 그 밖에는 「원래 메시지」·「원래 메일」 만 싣는다(링크는 서고, 열면 404).
   - 이유: `task.assign` 으로 남에게 배정한 업무의 담당자에게 배정자의 채널 이름·메일 제목이 흘러가지 않게 하려는 것이다. SPEC 의 「링크는 서되 누르면 찾을 수 없음」 과 맞는다.
3. 기존 task·work_request 참고 자료의 「못 찾음」 은 지금처럼 422다. `inbox_message` 만 SPEC 대로 404다.
4. 같은 메시지를 다시 참고 자료로 실어도 막지 않는다. 같은 메시지로 업무를 또 만들면 `made_task_count` 가 는다(OQ-907 「막지 않는다」).
5. 되살림: 나간 방은 이벤트로 되살리지 않는다. 다만 다음 워커 실행의 재확인(기존 동작)이 슬랙에서 「다시 보인다」 고 답하면 기존 규칙대로 되살아난다 — 기존 시험이 그 동작을 고정하고 있어 손대지 않았다.
6. 맥락 조합은 실행 직전에 한 번 한다. 접수와 실행 사이에 새 메시지가 오면 실행 시점의 둘레가 실린다(`label` 도 그 범위).
