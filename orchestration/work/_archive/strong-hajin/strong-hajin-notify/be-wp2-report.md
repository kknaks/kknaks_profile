# WP2-BE 결과 보고 — 알림 생성 · 설정 · 판정 재료 · 백필

## 상태: done (커밋 없음 · 워크트리에 변경만)

- SSOT: WORK-013 「Phase WP2-BE」 · SPEC-011 v0.2.2 §4.2 ~ §4.5 · §4.7 · SPEC-008 v0.7.0 §4.4 · §4.6 · P0(`p0-report.md`)
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `BT/` = `backend/tests/`
- 앞 WARN 손질은 `be-wp1fix-report.md`

## 1. 계약 체크박스 — 16/16

| # | 계약 | 구현 위치 |
|---|---|---|
| 1 | **스키마** — 알림 칸 · 순번 · 설정 표 · `from_me` · 옛 종류 값 · 수동 SQL + sync | 모델 `B/platform/persistence.py`<br>• 알림 칸 여덟(theme · item · relation · failure · actor · data · target · coalesce_key) — :1333-1347<br>• `NotificationSettingsRecord` — :1350<br>• `external_messages.from_me` — :2231<br>SQL `backend/migrations/manual/2026-10-08-notifications-v2.sql` 뒤쪽(WP2 절) — 칸 · 설정 표 · `from_me` · 옛 종류 두 개 바꾸기(테마 빈 행만 · 재적용 안전)<br>sync: 칸 · 새 표는 `schema_sync` 가 더한다(시퀀스는 WP1 에서 `B/bootstrap/schema_sync.py:28-33`)<br>local-stack 전제 `Makefile:334` 에 설정 표 · `from_me` 를 더했다 |
| 2 | **생성기 하나** — 원칙 ①②③ + M06 예외 · 관계 우선 · 같은 트랜잭션 · 멱등 | `B/modules/notification_events.py`<br>• `NotificationGenerator`(:175) — ① 행위자 · ③ 비활성 = 관계 없음(OQ-1109 제안) · ② 설정 `settings_allow`(:95)<br>• 관계 우선 `RELATION_PRIORITY`(:67) — 담당 > 요청자 > 배정자 > 참조 · 소유자 > 참석자 > 공유받음(OQ-1104 제안)<br>저장소 `B/platform/notifications.py` `write`(:82) — `(받는 사람, 원천)` 멱등 · 새 순번 · 같은 세션 NOTIFY<br>조립 `B/bootstrap/application.py:3047 · 3762 · 5048 · 5101` · `B/bootstrap/external_inbox.py:125-126 · 333` — 사건 자리마다 `notifier=` · 같은 session |
| 3 | **사건 자리 68행** — 알림 40 은 부르고 없음 28 은 시험으로 | 자리는 §2 표<br>시험 `BT/contract/test_notification_rows.py` 45건(**행 id 가 시험 이름**) + `test_meeting_finalize.py` M09 · M10 · M11 2건 + `test_task_successors.py` W35 1건 |
| 4 | **흡수(D-30)** — `WT:2116` 의 `emit` → 생성기 · 옛 종류 | `B/platform/work_tasks.py:2095` `append_audit` 은 이제 알림을 만들지 않고 감사 id 를 돌려준다. 그 id 를 원천으로 사건 자리(`requests.py:488` W01 · `:516` W05)가 생성기를 부른다<br>`emit` 은 지웠다(`\.emit\(` 1 → 0)<br>옛 행 읽기는 `LEGACY_KINDS`(`notification_events.py`) · `notification_item`(`B/modules/notifications.py:137`) — 마이그레이션 전에도 새 종류로 보인다 |
| 5 | **선행 해제 W35** 연다 · 이동 `APP:741` 그대로 | `B/modules/work/application.py:1632`. 시험 `test_task_successors.py:495` — 기대가 0 → **1줄**로 바뀌었다(해제한 사람은 없음) |
| 6 | **메시지 저장 때** `from_me` · To/CC · 멘션 · 실시간만 · worker-external | 슬랙 · 메일: `B/platform/external_channels_sync_store.py:192`(`from_me=_from_me` · `:460`) → `mode == "live"` 일 때만 `_notify_messages`(:227 · :232)<br>판정 `notification_events.py` — `mail_from_me`(:234, From == `account_key` · 대소문자 무시 · D-41) · `mail_relation`(:242, to · mail-cc · mail-other) · `slack_from_me`(:261, `raw.user`) · `slack_mentions_me`(:269, `<@내 id>` 만 · `@here` 류 아님 · OQ-1105)<br>카톡: `kakao_ingest.py:81` · `:212` · `:233` · `:274`<br>메일 · 슬랙 저장은 이 저장소를 쓰는 external_worker 프로세스에서 돈다 |
| 7 | **슬랙 채널 합침** | X06 만 `coalesce_key = slack-channel:{room}`(`notification_events.py` `message_notification`)<br>저장소 `_merge`(`platform/notifications.py:138`) — 안 읽은 같은 열쇠 줄에 count +1 · senders(5명까지 + `sender_count`) · 마지막 시각 · **새 순번** · `created: false`<br>DM · 멘션은 합치지 않는다. 방 읽음이 합친 줄도 읽는다(#11) |
| 8 | **X10 · X11** · 카톡 꺼짐 X12 없음 | X10: `external_channels_sync_store.py:405`(워커 `mark_disconnected`) · `B/modules/external_channels/inbox.py:1086`(API `_mark_disconnected`)<br>X11: `external_channels_sync_store.py:351`(`set_room_access` — 처음 잃을 때만)<br>`integration_lost_notification`(`notification_events.py:355`) — 항목 = 그 채널 · 꼬리표 `integration` · 붉은 표식 |
| 9 | **meeting_worker** M09 · M10 · M11 | `B/modules/meetings/application.py:1036`(완료 — 행위자 시스템 · 소유자 > 참석자) · `:1053`(실패)<br>워커는 `create_workflow_application` 의 `_meetings(session)` 조립을 쓰므로 같은 세션 · 같은 트랜잭션 NOTIFY |
| 10 | **안 읽음 셈** — 방 + 메일 넷 → `from_me is not true` | `B/platform/external_channels_inbox_store.py:201`(방 카드) · `:120`(`mail_page(unread_only)`) · `:136`(`mail_unread_count` = 레일 `counts["mail"]` `INB:503` 도 이것) · `:561` `_not_mine()`<br>`B/modules/external_channels/inbox.py:532`(메일 줄 `unread`)<br>**+ 표 밖 하나**: `:588` 메일 상세 `unread` |
| 11 | **메시지함 읽음 → 알림 읽음**(D-37) | `inbox.py:670`(메일 한 통) · `:681`(방 `up_to_ts` — 메시지 시각 ≤ up_to, 합친 줄은 마지막 시각) · `:692`(「모두 읽음」 출처별)<br>→ `mark_message_notifications_read`(`platform/notifications.py:297`) · 같은 세션 · `notification.read`<br>연동 끊김 줄은 빠지고, 반대 방향은 없다 |
| 12 | **회의 공유 두 길 M12 · 공개 전환 M15 없음** | `share_many`(`meetings/application.py:1207`) · `share`(:1281)<br>`apply_legacy_visibility` 는 생성기를 부르지 않는다(docstring 에 M15) — 시험 `test_m15_…` |
| 13 | **카톡 업로드 `from_me`** | `KakaoMessageInput.from_me: bool \| None`(`kakao_ingest.py:81`) → 저장 칸 · 없으면 `null`<br>`logId` 건너뛰기는 그대로. 알림은 그 묶음 **전에** 이미 `live` 였던 방의 줄만 낸다(`:212`) |
| 14 | **알림 API** — 목록 · summary · 읽음 · read-all · badges · 모양 · target · 읽기 인가 · 사건 | 라우트 `B/entrypoints/http.py:1391`(목록 `theme` · `cursor` · `limit` 1~100 · 422) · `:1404` summary · `:1409` read-all(본문 없음 · **전부** D-40) · `:1414` badges · `:1434` 읽음<br>모양 `NotificationItem`(`B/modules/notifications.py`) = §4.5-2 · cursor 는 서버 것만(`decode_cursor` :117)<br>**읽기 인가 변경**: 줄은 남고 저장한 제목 · 행위자 · 값, `target` 만 `_notification_target_open`(`application.py:2477`)이 가른다 — 못 여는 것만 null, 예상 밖 소유 오류는 삼키지 않는다. 옛 `_authorized_notification_view`(호출 0)는 지웠다<br>읽음 · 모두 읽음 → `notification.read`(`platform/notifications.py` `mark_read` · `mark_all_read` :286) |
| 15 | **설정 API** | `GET/PUT /api/me/notification-settings`(`http.py:1419` · `:1424`)<br>`validate_settings`(`modules/notifications.py:172`) — 테마 셋 · 항목 16 **정확히** · bool → 422<br>`version` 다르면 `409 SETTINGS_VERSION_CONFLICT`. 기본값 = 시안(`comment` 만 끔) · `version: 0`. 상위를 꺼도 아래 값은 그대로(D-18). 캐시 없음(사건마다 읽음) |
| 16 | **MCP · 도구 설명 · 인벤토리** · `tool_catalog.py:446` · **백필 SQL** | MCP `list_notifications` → `NotificationPage` · `notification_mark_read` → `NotificationItem`(`B/entrypoints/mcp.py`)<br>도구 설명: `tool_catalog.py` 의 list_notifications(종류 · target null) · notification_mark_read · **meeting_share(「공유받은 사람에게 meeting.shared 알림」)**<br>인벤토리: `be-wp1fix-report.md` W-1<br>백필 `backend/migrations/manual/2026-10-08-notification-from-me-backfill.sql` — `psql -v integration_id=… -v self_name=… -v apply=0\|1`<br>• **두 걸음**: 기본 셈만 출력 — 본인 줄 · 방 수 · 전체 · 빈 칸 수 · 이름 종류 · `authorId` 종류(같은 이름의 다른 사람 판별 재료)<br>• `apply=1` = 한 트랜잭션 · `from_me IS NULL` 만<br>• 카톡(이름 인자) · 슬랙(`raw.user`) · 메일(From 헤더 → 주소. 못 찾으면 null)<br>• 실명은 파일 · 시험에 없다(시험 이름은 가상) |

## 2. 사건 자리 — 행 → 코드

| 행 | 알림 | 자리 |
|---|---|---|
| W01 · W05(수락 · 거절) · W07 · W08 · W09 · W10 · W36 | ✅ | `B/modules/work/requests.py:488 · 516(+거절) · 580 · 638 · 710 · 754 · 1233`(댓글 · 독자 `party_of`) |
| W02 · W03 · W04 · W06 · W11 | — | 행위자 · CC · 결재자는 받는 사람에 없다 · 자료/정리/참고 읽음/자동 합류는 부르지 않는다 |
| W12 · W13(넘김 · 변경 제안) · W14 · W15(수락 · 거절) | ✅ | `B/modules/work/assignments.py:157 · 240 · 246 · 312 · 368` |
| W16 | — | `cancel` 은 부르지 않는다 |
| W17 · W24 · W25 · W28 · W29/30 · W31/32 · W33 · W35 | ✅ | `B/modules/work/application.py:629 · 2172 · 1946 · 1989 · 2240 · 2293 · 2352 · 1632` |
| W18~W23 · W26 · W27 · W34 · W37 · W38 | — | 부르지 않음(W38 은 실행된 업무 명령이 그 행을 탄다) |
| X01~X06 | ✅ | `external_channels_sync_store.py:227`(실시간만) · 판정은 `message_notification` |
| X08 · X09 | ✅ | `kakao_ingest.py:274` 부근 |
| X10 · X11 | ✅ | `sync_store.py:405 · 351` · `inbox.py:1086` |
| X07 | — | `from_me = true` → 사건 없음 |
| X12 · X13 · X14 · X15 | — | 부르지 않음 |
| M01 · M04 · M05 · M06 · M07 · M09/M10 · M11 · M12(두 길) | ✅ | `B/modules/meetings/application.py:370 · 583 · 590 · 596 · 665 · 1036 · 1053 · 1207 · 1281` |
| M02 · M03 · M08 · M13 · M14 · M15 | — | 행위자 · 외부 · 시작/종료 · 회수 · 진행 · 공개 전환은 부르지 않음 |

### ⚠ 코디 확인 — 지금 권한 모델로는 「알림」 행인데 늘 0 줄인 것 셋

사건 자리는 생성기를 부르지만, 그 명령을 부를 수 있는 사람이 곧 받는 사람이라 원칙 ① 이 걸러 낸다. 시험은 그 사실을 고정했다.

- **W17**(기한 · 시작일 수정 → 담당) · **W24**(업무 취소 → 담당)
  - `TaskApplication.update` · `transition` 은 `repository.task(task_id, principal)` = **활성 담당만** 연다(`B/platform/work_tasks.py:1095-1101`)
  - 그래서 행위자 = 담당 → 0 줄이다
  - 요청자가 기한을 바꾸는 길은 조건 변경 제안(W31 → W33)뿐이다
- **W30**(담당이 재개 → 요청자)
  - 요청 업무의 재개는 **요청자만** 된다(`_require_may_reopen`)
  - 본인 · 배정 업무에는 요청자가 없다 → 0 줄
- SPEC 표와 코드 권한이 다른 것인지, 권한을 넓힐 때를 위한 자리인지 **사용자 판단**이 필요하다(시험 `test_w17_…` · `test_w24_…` · `test_w29_w30_…` docstring 에 근거)

## 3. Code Surface WP2 표 대비

시작 시 `d2a06fa` 를 같은 패턴으로 다시 셌다(`git grep HEAD` · `B/`). **표의 수와 모두 같았다.**

| 패턴 | 표 | d2a06fa | 지금 | 처분 |
|---|---|---|---|---|
| `\.emit\(` | 1 | 1 | **0** | 흡수 — 사건 자리가 생성기를 부른다 |
| `SqlAlchemyNotificationRepository\|NotificationRecord\|NotificationApplication` | 27 / 6 | 27 | 71 | 정의만 있던 `_authorized_notification_view` 를 지우고 하나로 |
| `list_notifications\|mark_notification_read\|notification_mark_read\|notification\.mark_read` | 23 / 6 | 23 | 23 | 응답 모양 갱신. MCP 2 · HTTP · 실행 미리보기(`B/platform/actions.py` notification.mark_read — 새 `event_item` 으로) · 명령 계약 그대로 |
| `append_audit\(` | 37 / 5 | 37 | 37 | 알림은 감사 훅이 아니라 사건 자리에서 부른다(WT 훅은 id 만 돌려준다) |
| `알림의 자리` | 2 / 1 | 2 | 3 | `:741`(W21) 그대로 · `:1581` 을 열었다. 새 히트 1 은 W35 주석의 인용 |
| `\.record\(` (modules/work · WT) | 20 | 20 | 20 | 20 개 모두 §2 의 W 행에 대응했다(빠진 사건 없음) |
| 회의 사건 자리 · 공유 두 길 · 공개 전환 | — | — | — | §2 |
| 메시지 저장 · 팬아웃 · 이름 덮기 | — | — | — | 판정은 `raw.user` 로 해서 이름 덮기(`SYNC:484-485`)와 무관 |
| 안 읽음 「내 줄 빼기」 방 1 + 메일 넷 | 1 + 4 | — | 5 + 1 | **표 밖 1**: 메일 상세 `unread`(`inbox.py:588`) |
| 메시지함 읽음 → 알림 읽음 | — | — | 3 자리 | 메일 · 방 · 모두 읽음 |
| `class KakaoMessageInput` | 1 | — | 1 | `from_me` 명시 필드 |
| 회원 설정 본보기 | — | — | — | 새 표 `notification_settings`(회원마다 한 벌 · `version`) |
| 「알림을 내지 않는다」 문구 `tool_catalog.py:446` | 1 | — | 0 | 고쳤다. `F/…` 셋과 `docs/unified-operations.md:57,85,113` 은 FE · 코디 몫 |
| 시험 — 알림 5 파일 | 5 | — | — | §4 |

**표 밖에서 더 닿은 자리**
- `B/platform/actions.py:1703`(확인 미리보기가 옛 목록 모양을 읽었다 → `event_item`)
- `B/entrypoints/http_events.py`(SSE 항목 = 새 모양 그대로)
- `BT/contract/test_external_inbox.py` 시드에 `from_me`(내 줄 · 저장 자리와 같은 값)
- PG 시험의 「실시간 1건 → 사건 셋」(`notification.upserted` 가 더해짐)

## 4. 새 시험 · 검증 수치 (P-8 · Makefile 타겟만)

**새 · 바뀐 시험**

| 파일 | 내용 |
|---|---|
| `BT/unit/test_notification_rules.py`(새 · 8) | 관계 우선 두 축 · 행위자 · 비활성 · 시스템 자리 · 설정 셋 · 항목 16 · 종류 → 테마/항목 · 메일 From/To/CC · 슬랙 `raw.user` · 멘션(`@here` 아님) · 내 줄 사건 없음 |
| `BT/contract/test_notification_rows.py`(새 · 45) | W01~W38 · X01~X15 · M01~M08 · M12~M15 행 id 시험. 설정 거름(항목 · 테마 · 전체 · 켜도 소급 없음) · 비활성 수신자 · 백필 없음 · 합침 새 순번 · 메시지함 읽음 → 알림 읽음 · 빠진 참석자 `target: null` |
| `BT/contract/test_notifications.py`(다시 씀 · 8) | 흡수 W01/W05 · 목록 순번 순 · 테마 · 커서 · 422 다섯 · summary · 멱등 읽음 · 남의 것 404 · read-all 전부 · badges · 저장 제목 + `target: null` · 설정 기본/저장/409/422 · 옛 행 읽기 |
| `BT/contract/test_meeting_finalize.py`(+2) | M09 · M10 · M11 |
| `BT/contract/test_task_successors.py` | W35 — 0 → 1 줄로 바뀜 |
| `BT/contract/test_personal_command_tools.py` | 새 모양 · 원천 거부 = `target: null` · 읽음 됨 · 소유 오류는 삼키지 않음 |
| `BT/contract/test_events_stream.py`(+1) | read-all 사건 |
| `BT/integration/postgres/test_external_channels_postgres.py`(+1 · 2 갱신) | 백필 SQL 두 걸음(psql · 가상 이름) · v2 SQL 의 WP2 칸 · 옛 종류 바꾸기 · 생성기로 쓴 워커 세션 NOTIFY |

**검증 수치** — 격리 PG 는 사용자 54329 가 아닌 별도 컨테이너 `ax-notify-pgtest`(`127.0.0.1:55439` · DB `ax_test_notify` · 검증 뒤 정지)다.

| 명령 | 결과 |
|---|---|
| `make test-contract-serial FILES="tests/unit/test_notification_rules.py tests/contract/test_notifications.py tests/contract/test_task_successors.py tests/contract/test_task_assignments.py tests/contract/test_request_amendment.py tests/contract/test_request_creation_input.py tests/contract/test_meeting_core.py tests/contract/test_meeting_finalize.py tests/contract/test_external_inbox.py tests/contract/test_external_sync.py tests/contract/test_kakao_ingest_and_profile.py tests/contract/test_personal_command_tools.py tests/contract/test_unified_queries.py tests/architecture/test_operation_inventory.py tests/contract/test_notification_rows.py"` | **278 passed** · 0 failed · 4m11s |
| WP1 시험 줄(`be-wp1fix-report.md`) | **78 passed** · 0 failed |
| `PYTEST_ADDOPTS='tests/integration/postgres/test_external_channels_postgres.py' POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:55439/ax_test_notify make test-postgres` | **6 passed** · 0 failed · 0 skipped(psql 실행 포함) |

- 기존 실패 0(기준선 `be-baseline.md`)
- 고치며 바뀐 기존 시험은 계약 변경 때문이다: `test_external_inbox` 시드(`from_me`) · `test_personal_command_tools`(새 모양 · 읽기 인가) · PG 「실시간 1건 → 사건 셋」 · `test_task_successors` W35
- **돌리지 않은 관련 파일**(시험 줄 밖): `BT/architecture/test_local_stack_targets.py`(단언 갱신 — Makefile 글자는 grep 1 로만 확인) · `test_architecture.py` · `test_test_pyramid.py` → 코디 전체 돌기에서 본다

## 5. I-1 — AX 실행 업무 사건은 어느 프로세스에서 나나

- AX 턴의 MCP 도구 서버는 conversation_worker 의 CLI 공급자가 stdio 로 띄운다(`B/platform/claude_cli.py:302` · `codex_cli.py:360-383` · `AX_MCP_CAUSATION_ID`)
- 그 안의 명령은 `_propose_chat_action`(`B/entrypoints/mcp.py:823-839`)으로 **제안만** 세운다
- 실제 효과(배정 · 요청 · 댓글 · 회의 공유 …)는 사람이 판단함에서 확정할 때 **API 프로세스**의 `_action_services(session)`(`B/bootstrap/application.py` — `BA:1790` 의 `message_origin_recorded` 도 여기)에서 돈다
- 생성기는 프로세스와 무관하다(그 세션 + 같은 트랜잭션 NOTIFY). 시험: W38(`test_w38_…`)이 확정 → W12 한 줄

## 6. 미결 · 주의점

1. **W17 · W24 · W30 = 0 줄**(§2 ⚠) — 사용자 판단 필요
2. **운영 순서** — `2026-10-08-notifications-v2.sql` 은 이제 WP1 + WP2 를 담는다(이미지보다 먼저 · ② 뒤 한 번 더)
   - 그다음 인덱스 `.concurrent.sql`
   - 카톡 백필은 **새 수집기 dmg 뒤** `apply=0` → 코디 판단 → `apply=1`
   - 옛 종류 바꾸기는 `members` 와 조인한다(행위자 회원이 없는 옛 행은 남는다 — 읽을 때 `LEGACY_KINDS` 가 같은 뜻으로 보인다)
3. **카톡 「같은 이름의 다른 사람」** — 서버 줄에는 작성자 id 칸이 없다. 셈이 `raw.authorId` 종류 수를 내지만, 옛 수집기 줄에는 그 키가 없어 0 이다 → 코디가 이름 종류 수 · 방을 보고 판단(SPEC §4.7 「멈춘다」를 SQL 이 스스로 하지는 않는다)
4. **메일 백필**(I-5) — From 헤더를 SQL 로 풀었다(`<addr>` 또는 값 전체). 헤더가 없는 줄은 null 이다
5. **`actor_member_id`(옛 칸 · NOT NULL · FK)** — 시스템 · 외부 발신자 줄은 받는 사람을 채운다
   - demo DB 의 sync 가 NOT NULL 을 못 풀기 때문이다
   - 화면 · API 는 새 `actor` JSON 만 읽는다
   - 운영 SQL 에서 `DROP NOT NULL` 을 할지는 코디 판단(지금 SQL 은 하지 않는다)
6. **badges 의 `inbox`** — 메시지함 목록 셈(`list_messages(unread=True, limit=1)`)을 그대로 쓴다. 레일 숫자와 같은 값이지만 쿼리가 무거울 수 있다(사이드바가 부르는 빈도 — FE)
7. **합친 줄 `senders`** — 5명까지 + `sender_count`(「외 N명」 은 화면 몫). `target.message_id` 는 첫 메시지로 남는다(SPEC 「첫 안 읽은 메시지」)
8. **WP1-FE 에 알릴 것**
   - 숫자가 아닌 `Last-Event-ID` 는 **첫 연결**이다(앞 보고 정정)
   - SSE `notification` 은 이제 §4.5-2 모양이다(`resource` → `subject` 등)
9. **docs** — `docs/domain-model.md` 대조표(새 표 `notification_settings` · 알림 칸)와 `docs/unified-operations.md:57,85,113` 문구는 allowed_paths 밖이다 → 코디
