# 코드 검수 — WP2-BE(+ WP1 손질) · WP3-FE · 서버↔화면 맞춤

> reviewer(read-only) · 2026-10-08 · 대상 `strong-hajin-notify` 작업 트리 — `backend/` · `Makefile` · `docs/unified-operations-inventory.json` · `frontend/src/`(WP3 화면). **WP4-SHELL 자리**(`src-tauri/` · `lib/shell.ts` · `osNotifier`)는 제외
> 계약: WORK-013 WP2-BE · WP3-FE · SPEC-011 v0.2.3 §2 · §4.2~§4.5 · §4.7 · SPEC-008 v0.7.0 · 확정 시안 `handoff/alerts/` · `handoff/settings/js/`
> 약어: `B/` = `backend/src/ax_workspace/` · `BT/` = `backend/tests/` · `F/` = `frontend/src/`

## 0. 판정 — **FAIL** (FAIL 3 · WARN 6)

서버와 화면은 큰 틀에서 맞는다 — 경로 7 · 응답 `{items, next_cursor}` · 항목 모양(§4.5-2) · `read-all` 빈 본문 · 설정 PUT/409 · `target` · `notification.read` · SSE 항목. **68행은 생성기 자리와 행 id 시험이 전부 있다**(행 id 로 전수 확인 — 빠진 행 0). 원칙 ①②③ · M06 예외 · 관계 우선 · 슬랙 합침 · 설정 거름 · 흡수(`.emit(` 0) · `from_me` 셋 · 슬랙 안 읽음 버그 · 메시지함 읽음 → 알림 읽음 · meeting_worker 게시도 코드로 확인했다. 코디가 정한 W17 · W24 · W30 「늘 0 줄」 근거도 맞다.

FAIL 셋 가운데 둘은 **양쪽 시험이 각자 초록인데 맞물리면 문장이 틀리는** 자리이고, 하나는 화면 시험 실행이 빨갛게 끝나는 자리다.

| # | 무엇 | 몫 |
|---|---|---|
| F-1 | 담당 밀려남(W14)의 새 담당 **이름**을 서버가 주지 않는다 — 화면 문장 「…담당이 {이름}님으로 바뀝니다」 가 이름 없이 선다 | **backend** |
| F-2 | 회의 시간 변경(M04)의 `before/after` 가 서버는 **객체**(`{starts_at, ends_at, place}`), 화면은 **ISO 글자**를 기대한다 → 「회의 정보를 바꿨습니다」 로 떨어지고 「11:00 → 15:00」 보조 줄이 사라진다 | **frontend**(+ SPEC 한 줄) |
| F-3 | `App.test.tsx` 의 새 시험 「대상마다 고른 상태로 연다」 가 **처리 안 된 예외**를 남겨 `vitest run` 이 **exit 1** 로 끝난다(테스트 수는 다 통과로 찍힌다) | **frontend** |

### 실행한 것
- 코드: `git diff` · 새 파일(`notification_events.py` · `platform/notifications.py` · `modules/notifications.py` · SQL 넷 · `NotificationsPage` · `NotifySection` · `labels.ts` 알림 절 · `App.tsx` `openFocus`/`openNotification`/`refreshBadges`)
- 서버↔화면: 사건 자리의 `NotificationEvent(data=…)` 를 종류마다 읽어 `describeNotification` 의 `d.*` 와 대조
- 시험(관련만 · Makefile 타겟 · 고른 vitest · 사용자 포트 없음)
  - `make test-contract-serial FILES="tests/unit/test_notification_rules.py tests/contract/test_notification_rows.py tests/contract/test_notifications.py tests/contract/test_events_stream.py tests/contract/test_meeting_finalize.py tests/contract/test_personal_command_tools.py tests/architecture/test_operation_inventory.py tests/architecture/test_local_stack_targets.py tests/architecture/test_architecture.py tests/contract/test_task_successors.py"` → **189 passed**
  - `npx vitest run <WP3 아홉 파일> --no-file-parallelism` → **152 passed · Errors 1 · exit 1**(F-3)
  - `npx tsc --noEmit` → 0
  - PG(`make test-postgres`)는 이번에 돌리지 않았다 — 워커 리포트 6 passed. SQL 은 눈으로 검수(§5)
- 행 id 전수: `BT/contract/test_notification_rows.py` · `test_meeting_finalize.py` · `test_task_successors.py` 의 시험 이름에서 W01~W38 · X01~X15 · M01~M15 를 뽑아 대조 → **68/68**

---

## 1. 서버 ↔ 화면 맞춤 (`fe-wp3-report.md` §6 의 8 + 더)

| # | 자리 | 서버(`backend/`) | 화면(`frontend/src/`) | SPEC | 고칠 쪽 |
|---|---|---|---|---|---|
| 1 | 항목 모양 | `NotificationItem`(`B/modules/notifications.py:47-62`): `notification_id · seq · kind · theme · item · relation · failure · actor · subject{type,id,title} · data · target · created_at · updated_at · read_at` | `Notification`(`F/lib/viewModels.ts:1040-1060`) 같은 칸 | §4.5-2 | **맞음** |
| 2 | 경로 · 응답 | 목록 `{items, next_cursor}` · summary · `{id}/read` · read-all · badges · 설정 GET/PUT(`B/entrypoints/http.py:1391-1444`) | `api.ts:731-768` 같은 일곱 | §4.5-1 · §4.4-2 | **맞음** |
| 3a | `work.assigned`(`displaced`) | `{"mode": "displaced", "new_assignee_id": …}`(`B/modules/work/assignments.py:253`) — **이름이 없다** | `d.new_assignee_name` 을 읽고 없으면 「업무의 담당이 바뀝니다」(`F/lib/labels.ts` `work.assigned`) | §4.2-1 문장 「‘{업무}’ 업무의 담당이 **{새 담당}님**으로 바뀝니다」 · §2.1 「서버는 … 값(**사람** · 대상 이름 …)만 준다」 | **backend — F-1** |
| 3b | `meeting.changed`(`updated`) | `before`/`after` = `_schedule_data` **객체** `{starts_at, ends_at, place}`(`B/modules/meetings/application.py:586-587` · 시험 `test_notification_rows.py:818` 이 객체로 단언) | `text(d.before)` — ISO **글자**를 기대(`labels.ts` `meeting.changed` · 시험 `notificationLabels.test.ts:79` 가 글자로 단언) | §4.2-1 `{change, before?, after?}` — 모양 미정 · 문장 「회의 시간을 바꿨습니다」 | **frontend — F-2**(M04 는 시간 · 장소 둘 다라 객체가 더 맞다 · SPEC 에 모양 한 줄) |
| 3c | `message.slack` 채널 합침 | `senders`(5명까지) + `sender_count`(`B/platform/notifications.py` `_merge`) | `senders.length` 로 「외 N명」 — `sender_count` 를 읽지 않는다 | §4.2-1 「보낸 사람 … 외 N명」 | **둘 다 — W-1** |
| 3d | 그 밖의 `data` | `work.changed` `before/after` = 날짜 ISO(`application.py:638` · W31 `:2296-2297`) · `meeting.invited` `{starts_at, ends_at, place}` · `message.mail` `{subject, attachment_count, account, sent_at}` · `integration_lost` `{channel, reason, account, room_name?}` · `minutes_ready` `{}` | 같은 이름을 읽는다(`minutes_ready` 는 없으면 보조 줄 없음) | §4.2-1 | **맞음**(`minutes_ready` 의 `agenda_count`/`action_count` 는 SPEC 이 `?` — 보조 줄이 비는 것은 계약 안) |
| 4 | 외부 발신자 「님」 | `actor = {external_name}` — 사람/단체를 가르지 않는다 | 받은 이름 그대로(회원만 「님」) | 정하지 않음 | **사용자 판단**(§10) |
| 5 | `read-all` | 본문 없는 라우트(`http.py:1409`) · 전부 · `notification.read {all:true, theme:null}` | 본문 없이 POST(`api.ts:747`) | §4.5-1 · D-40 | **맞음** |
| 6 | 설정 PUT · 409 | `{enabled, themes}` 정확히 + `version` · 다르면 409 `SETTINGS_VERSION_CONFLICT`(`modules/notifications.py:172-198,226-238` · `http.py:538`) | 전체 + `version` · 409 는 상태로만(`NotifySection.tsx:71-100`) | §4.4-2 | **맞음** |
| 7 | `target` | 업무 `{task_id}` / `{work_request_id}` · 메일 · 방(+`message_id` · 스레드면 `thread_ts`) · 회의 · 설정 `tab` · 못 열면 `null` | `openFocus`(`App.tsx:386-432`) 일곱 갈래 · `thread_ts` 는 안 씀 | §4.5-2-3 | **맞음**(`thread_ts` 무시는 2루프 후보로 이미 적힘) |
| 8 | `notification.read` | `{v, notification_ids}` · `{v, all:true, theme:null}` | ids · `all` + `theme ?? 전부`(`NotificationsPage.tsx:224-232`) | §4.1-2 | **맞음** |
| 9 | SSE `notification` | `event_item` → `NotificationItem`(§1-1 같은 모양) | `StreamNotification = Notification` | §4.1-2 | **맞음** |
| 10 | 숫자 아닌 `Last-Event-ID` = 첫 연결(backend 정정) | `http_events.py:63` | 화면은 숫자 순번만 싣는다(`eventStreamUrl(number)`) — 해당 없음 | Validation | **맞음**(화면이 영향받지 않는다) |

## 2. WP2-BE 체크박스 16 — 코드로

| # | 계약 | 확인 | 판정 |
|---|---|---|---|
| 1 | 스키마 · SQL · sync | 모델 칸 여덟 · `NotificationSettingsRecord` · `from_me` · SQL WP2 절(§5) · `Makefile:334` 전제 | PASS |
| 2 | 생성기 하나 | `NotificationGenerator.notify`(`notification_events.py:181-201`): 관계 우선(`RELATION_PRIORITY`) → ① 행위자 → ③ 비활성 → ② 설정. 저장소 `write` 가 같은 세션 · 멱등(받는 사람 · 원천) · 새 순번 · NOTIFY | PASS |
| 3 | 68행 | 행 id 전수 68/68(§0). 「없음」 행은 `_none(ledger, …)`(`test_notification_rows.py:72-74`)으로 **회원마다 새 줄 0** 을 단언한다 — 빈 단언이 아니다 | PASS |
| 4 | 흡수 | `\.emit\(` 0 · `WT append_audit` 는 감사 id 만 · W01 `requests.py:489` · W05 `:517,546` · 옛 종류 읽기 `LEGACY_KINDS` | PASS |
| 5 | W35 연다 · W21 그대로 | `application.py:1634` · 시험 0 → 1 | PASS |
| 6 | 저장 때 `from_me` · To/CC · 멘션 · 실시간만 · worker-external | `mail_from_me` · `mail_relation` · `slack_from_me`(`raw.user`) · `slack_mentions_me`(`<@id>`만) · `message_notification` 이 `from_me is True` 면 None(X07) | PASS |
| 7 | 슬랙 합침 | X06 만 `coalesce_key` · 안 읽은 같은 열쇠 줄을 고침 · 새 순번 · `created:false` | PASS(W-1 하나) |
| 8 | X10 · X11 · X12 없음 | `integration_lost_notification` · 항목 = 채널 · `integration` · 붉은 표식 | PASS |
| 9 | meeting_worker M09~M11 | `commit_finalized` · `fail_finalize` 가 `_notify_meeting`(같은 세션) · 상태 전이 가드(`ensure_transition`)로 다시 배달돼도 한 번 | PASS |
| 10 | 안 읽음 셈 | `_not_mine()`(`external_channels_inbox_store.py`) — 방 · `mail_page(unread_only)` · `mail_unread_count` + 메일 줄 · 상세 `unread` | PASS |
| 11 | 메시지함 읽음 → 알림 읽음 | `inbox.py:664-692` 세 자리 · `mark_message_notifications_read`(연동 끊김 제외 · 방은 시각 ≤ up_to · 합친 줄은 마지막 시각) · 같은 세션 `notification.read` | PASS |
| 12 | 공유 두 길 · M15 없음 | `share_many` `:1208` · `share` `:1282` · `apply_legacy_visibility` 부르지 않음 | PASS |
| 13 | 카톡 `from_me` | `KakaoMessageInput.from_me` · 없으면 `null` · `logId` 건너뛰기 그대로 | PASS |
| 14 | 알림 API · 인가 변경 | 줄은 남고 `target` 만 `target_open` 으로 · 저장한 제목/행위자/값 · 읽음 → 사건 | PASS |
| 15 | 설정 API | 기본 = 시안(`comment` 만 끔) · 상위 꺼도 아래 값 저장 · 캐시 없음 | PASS(참고: 같은 회원의 **첫 저장** 둘이 겹치면 행이 없어 잠금이 안 걸려 PK 충돌 500 이 날 수 있다 — 드묾) |
| 16 | MCP · 인벤토리 · 백필 SQL | 인벤토리 drift 시험이 `http_events.py` 를 읽고(`test_operation_inventory.py:138`) `http_count` 198 · 4 passed · 백필 §5 | PASS |

**코디 결정 확인 — W17 · W24 · W30 「늘 0 줄」 근거가 맞다.**
- W17(`update`)과 W24(`transition`)는 `self.repository.task(task_id, principal)`(`application.py:561` · `:2107`)이다 → `WT task()` = **활성 담당만**(`work_tasks.py:1095-1101`). 그래서 행위자 = 담당이고 원칙 ① 로 0 줄이다
- W30 재개는 `_require_may_reopen`(`application.py:2248-2261`)이 정한다
  - 요청 업무(`source_work_request_id` 있음)는 **요청자만**
  - 그 밖은 담당만 — 그리고 그 업무엔 요청자 자리가 없다(`_requester_people` = ())
  - 그래서 담당이 열 때 받을 요청자가 없다
- 시험이 고정한다: `test_w17_w18_w19_w20_…`(:245) · `test_w24_…`(:270) · `test_w29_w30_…`(:316)
- 코드 자리는 남아 있다(권한이 넓어지면 바로 선다)

## 3. WP3-FE 체크박스 6 — 코드로

| # | 계약 | 확인 | 판정 |
|---|---|---|---|
| 1 | 알림 목록 화면 | `surface="notifications"` · 머리 · 필터 넷 · 탭 수 · 날짜 넷 · 한 줄 · 상태 넷 · 자동 이어 불러오기(IntersectionObserver · 실패 한 줄) · [모두 읽음] 전부 · 비활성 전체 기준 | PASS |
| 2 | 문장 함수 하나 | `describeNotification` 19 종류 · `title`/`text` 를 OS 알림과 공유 | PASS(F-1 · F-2 는 입력 쪽) |
| 3 | 실시간 | upserted 끼우기/고치기 · read 반영 · resync 다시 읽기 · 요약 다시 읽기 | PASS |
| 4 | 누르면 | `openNotification` → 읽음 API · `null` 이면 「열 수 없는 항목입니다」 · `openFocus`(AX 서랍 `onOpenResource` 다섯 갈래도 같은 함수로) · 방에 `message_id` 없으면 방만 | PASS |
| 5 | 사이드바 점 둘 | `disabled` 걷음 · `dot` · `refreshBadges` 겹침 방지 · §2.2 의 때 + 메시지함 읽음 뒤 | PASS(W-3 서버 무게) |
| 6 | 설정 알림 탭 | 시안 B · `Switch` · 바꿀 때마다 저장(줄 세운 version) · 그 칸만 잠금 · 실패 되돌림 · 409 다시 읽기 · `tab=notify` | PASS |

## 4. 조용히 통과하는 자리

- **F-2**(위) — 서버 시험은 객체로(`test_notification_rows.py:818`), 화면 시험은 글자로(`notificationLabels.test.ts:79`) 각자 초록이다. 맞물리는 시험이 없다
- **F-1** — 서버 시험은 `{"mode": "displaced"}` 계열만 보고, 화면 시험은 이름이 있는 대역을 쓴다(없을 때는 문장을 줄여 조용히 넘어간다)
- **F-3** — `App.test.tsx:2628` 의 대역은 `/api/meetings…` 전부에 **목록 모양**(`{title, upcoming, past}`)을 돌려준다. 회의 대상을 누르면 `MeetingDetailPage` 가 `/api/meetings/g1` 의 `record.meeting.status` 를 읽다가 `TypeError`(`MeetingDetailPage.tsx:269`)를 던진다. 시험 단언은 「g1 을 불렀다」 뿐이라 통과로 찍힌다. 그러나 vitest 는 **Unhandled Errors 1 → exit 1** 이라 `make frontend-test` · `make verify` 가 빨갛다(직접 재현: `npx vitest run src/App.test.tsx -t "대상마다 고른 상태로"` → exit 1). 워커 리포트의 「0 failed」 는 이 줄을 놓쳤다
- 그 밖 — `_none` 은 회원마다 새 줄을 직접 센다. 설정 시험은 저장 줄 세우기 · 그 칸만 잠금 · 409 다시 읽기를 순서대로 단언한다. 빈 단언 · 폴백으로 지나는 곳은 더 찾지 못했다

## 5. 운영 안전

| 항목 | 확인 | 판정 |
|---|---|---|
| `2026-10-08-notifications-v2.sql`(WP1 + WP2) | 칸 여덟 · `notification_settings` · `external_messages.from_me` 모두 `IF NOT EXISTS` · nullable(대표 큰 표 `external_messages` 의 칸 추가는 기본값 없는 nullable 이라 메타 변경만 — 잠금이 짧다) · 「② 이미지 뒤 한 번 더」 를 머리에 적었다 | PASS |
| 옛 종류 바꾸기 | `theme IS NULL` 인 행만 · `members` 조인(행위자가 없는 옛 행은 남고 읽을 때 `LEGACY_KINDS` 가 같은 뜻) · 재적용 안전 | PASS |
| 인덱스 CONCURRENTLY | WP1 그대로(앞 검수 PASS) | PASS |
| 백필 SQL 두 걸음 | `apply` 기본 0 = 셈만 · 1 = 한 트랜잭션 · `from_me IS NULL` 만 · 카톡(이름 인자) · 슬랙(`raw.user`) · 메일(From) · `self_author_ids`(같은 이름 다른 사람 재료 — 옛 줄엔 0) · 「dmg 먼저」 머리 · 인자 없으면 멈춤 | PASS(참고: 슬랙 연동에 `account_meta.user_id` 가 없으면 그 연동 줄은 모두 `false` 가 된다 — 「아님」 과 같은 셈이라 해는 없다) |
| **실명** | SQL 파일 · 시험 · 코드에서 사람 이름 인자를 쓰지 않는다. PG 시험은 `self_name=가상본인`(`test_external_channels_postgres.py:307`). 화면 시험의 「유하람」 은 기존 시안 페르소나 대역이다(이번 diff 의 새 실명 아님) | PASS |
| `actor_member_id` NOT NULL | 시스템 · 외부 발신자 줄은 **받는 사람**으로 채운다(`platform/notifications.py:120`) — 화면 · API 는 `actor` JSON 만 읽는다. 옛 `notification_item` 의 레거시 갈래만 `actor_member_id` 를 읽고, 그 갈래는 옛 두 종류에만 탄다 | PASS(운영 `DROP NOT NULL` 은 코디 판단 그대로) |
| `/api/me/badges` 메시지함 셈 | **W-3** — §6 | WARN |

## 6. WARN

| # | 무엇 | 파일:줄 | 고칠 것 | 몫 |
|---|---|---|---|---|
| **W-1** | 합친 슬랙 줄의 「외 N명」 이 6명 넘으면 틀린다 — 서버 `senders` 를 5명으로 자른 뒤 `sender_count = max(옛 값, len(자르기 전 목록))` 인데, 자른 목록에 새 이름이 붙어 다시 세므로 6에서 멈춘다. 화면은 `sender_count` 를 읽지 않고 `senders.length` 로 센다 | `B/platform/notifications.py` `_merge`(`COALESCED_SENDERS`) · `F/lib/labels.ts` `message.slack` 채널 | 서버: 보낸 사람 수를 따로 올린다(새 이름이 자른 목록에 없을 때 +1 — 정확히 하려면 이름 집합 해시 · 근사도 좋다). 화면: `sender_count` 가 있으면 그것으로 「외 N명」 | backend · frontend |
| **W-2** | W29 재개를 요청자가 하면 **회의 승격자**도 `requester` 꼬리표로 받는다 — DEC 표 W29 의 받는 사람은 담당뿐이다 | `B/modules/work/application.py:2241-2245`(`_requester_people` 이 승격자를 넣는다) | W29 이면 담당만 넘기고, W30 일 때만 요청자 · 승격자를 넘긴다 | backend |
| **W-3** | `/api/me/badges` 의 메시지함 점이 `list_messages(unread=True, limit=1)` 전체 셈을 돈다 — 방 카드마다 count 쿼리(`room_cards`) · 메일 셈. 사이드바는 앱 시작 · 모든 메시지함 사건 · 알림 사건 · 읽음 뒤마다 부른다 | `B/bootstrap/application.py:2525-2530` | 「안 읽은 것이 하나라도 있나」 만 묻는 `EXISTS` 쿼리 하나로(같은 `_not_mine` · 읽음 규칙). 지금 규모에선 동작은 맞다 | backend |
| **W-4** | W11(요청 자료 첨부 · 해제 · 채택 · 목록 정리 · 자동 합류)은 시험이 **참고 읽음 하나만** 돈다 | `BT/contract/test_notification_rows.py:173-177` | 자료 채택 · 목록 정리도 `_none` 한 번씩 | backend |
| **W-5** | `openFocus` 의 `useCallback` 의존이 `[setSurface]` 인데 안에서 `changeSurface` 를 부른다(메시지함 갈래) — `changeSurface` 가 렌더마다 바뀌면 낡은 클로저 | `F/App.tsx:386-432` | 의존에 `changeSurface` 를 더하거나 ref 로 | frontend |
| **W-6** | 사이드바 머리 `titleEnd` 슬롯 신설 — 프로젝트 화면 선례(WORK-005 D-25 「셸 신설 안 함」)와 다르다(워커가 이미 코디 확인 자리로 올림) | `F/shell/AppShell.tsx:28-31,51,67-75` | 코디 판단(SPEC §2.1 이 머리에 「안 읽음 N」 을 정했으니 받아들일 근거는 있다) | 코디 |

## 7. 시안 일치(화면)

| 축 | 결과 |
|---|---|
| 설정 항목 16 · label · desc · 기본 on | `notifySettingsCopy.groups` 가 `settings/js/data.js` `NOTIFY_GROUPS` 와 글자까지 같다 · 기본값은 서버(`DEFAULT_OFF = {(work, comment)}`) — 시험이 「8개 중 7개」 · ⑥⑦ 문구를 단언 · **16/16** |
| 꼬리표 16 | `notificationRelationLabel` ↔ `alerts.v1.jsx` `RELATIONS` 표 전체 대조 시험 · **16/16** |
| 상태 넷 | 기본 · 빈(전체/테마별) · 로딩(제목 1 + 줄 6) · 오류(+다시 시도) · 빈/로딩/오류에서 머리 숨김 · **4/4** |
| 사이드바 점 둘 | 알림 `badges.notifications` · 메시지함 `badges.inbox` · 숫자 없음 · `SideNav` 무변경 |

## 8. 사람 눈에 이상해 보일 자리

| # | 자리 | 왜 |
|---|---|---|
| ① | 「‘견적서 정리’ 업무의 담당이 바뀝니다」 — **누구로** 바뀌는지 없다 | F-1 |
| ② | 회의 시간을 바꿨는데 「회의 **정보**를 바꿨습니다」 · 「11:00 → 15:00」 줄이 없다 | F-2 |
| ③ | 시끄러운 채널에서 「민수 · 지훈 외 4명」 이 더 늘지 않는다 | W-1 |
| ④ | 메일 · 슬랙 · 카톡 사람 이름에 「님」 이 없다(「김민아님이」 와 「노을웍스 인사팀이」 가 섞여 보인다) — 서버가 사람/단체를 가르지 않는다 | 사용자 판단 |
| ⑤ | 업무 요청을 받으면 **업무 수신함 카드 · 알림 줄 · OS 알림**이 함께 서고 읽음이 따로다 | D-30 결정대로 |
| ⑥ | 요청자가 업무를 다시 열면 회의에서 승격한 사람에게도 「다시 열었습니다」 가 간다 | W-2 |
| ⑦ | 기한 변경 · 취소 · 담당이 재개를 해도 알림이 늘 없다(W17 · W24 · W30) | 코디 결정 — 권한상 행위자가 늘 받는 사람이다. 사용자 E2E 체크리스트의 「기한 변경」 항목이 이 때문에 「알림 없음」 으로 보일 수 있다 → 체크리스트 문구 손질 필요 |

---

## 9. 목록

### FAIL — 재발주용

| # | 몫 | 파일:줄 | 고칠 것 |
|---|---|---|---|
| **F-1** | **backend** | `backend/src/ax_workspace/modules/work/assignments.py:253` | `data` 에 `new_assignee_name`(새 담당 `display_name`)을 더한다 — 화면 키 이름 그대로. 시험(`test_notification_rows.py` W14)에 단언 한 줄 |
| **F-2** | **frontend**(+ writer 한 줄) | `frontend/src/lib/labels.ts` `meeting.changed` 갈래 · `frontend/src/lib/notificationLabels.test.ts:79` | `before`/`after` 를 `{starts_at, ends_at, place}` 객체로 읽는다(시간이 바뀌면 「회의 시간을 바꿨습니다」 + 「HH:MM → HH:MM」, 장소만 바뀌면 「회의 장소를 바꿨습니다」 등). 시험 대역을 서버 모양으로. SPEC-011 §4.2-1 `meeting.changed` `data` 에 「`before`/`after` = `{starts_at, ends_at, place}`」 한 줄(writer) |
| **F-3** | **frontend** | `frontend/src/App.test.tsx:2628` | `/api/meetings/g1` 에 상세 모양(`{meeting: {…, status}, …}`)을 돌려주거나 그 시험에서 회의 상세 렌더를 막는다 — `npx vitest run src/App.test.tsx` 가 exit 0 이어야 한다 |

### WARN
W-1(backend + frontend) · W-2(backend) · W-3(backend) · W-4(backend) · W-5(frontend) · W-6(코디) — §6

### 사용자에게 물을 것
1. **외부 발신자 이름에 「님」** 을 붙일까? 메일 · 슬랙 · 카톡 사람에게 붙이면 단체 이름에도 붙는다. 서버가 사람/단체를 가르지 않는다(§8 ④)
2. (확인) **W17 · W24 · W30 「늘 0 줄」** — 코디 결정대로 두되, 사용자 E2E 체크리스트의 「기한 변경」 항목을 「담당이 아닌 사람이 바꿀 길이 없어 알림이 서지 않는다」 로 손질할지(§8 ⑦)
