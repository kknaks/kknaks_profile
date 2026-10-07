# BE 재검수 — 커밋 `b2ba11a` (review-be23.md F-1·F-2·W-1·W-2·W-5·W-12① + review-be1.md W-2~W-9) (2026-10-06)

## 판정: PASS

지시된 항목은 **W-7 의 반쪽(기기 토큰 동시 발급)만 남기고 전부 닫혔다.** 새로 생긴 WARN 이 셋 있다. 그중 하나(W-N1)는 F-1 의 잔여 창이라 운영 전에 닫기를 권한다. 다음 단계를 막을 FAIL 은 없다.

> 검수 방법: `git show b2ba11a` 로만 읽었다(29 파일 +1512/−137). 시험은 돌리지 않았다.
> 약칭: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/`.

## review-be23.md

| # | 판정 | 근거(커밋 b2ba11a) |
|---|---|---|
| **F-1** 남의 슬랙 메시지 누출 | **해소** | ① 방 추가 — `B/modules/external_channels/application.py` `add_rooms`: 슬랙은 **그 회원 토큰으로 `describe`**(`B/platform/external_slack.py` `SlackRoomDirectory.describe` = `conversations.info` · DM/그룹 DM/비공개는 참여자가 아니면 `channel_not_found` · **공개 채널은 `is_member` 까지** · 보관 채널 거절). 못 보면 `InvalidRoomSelection`(422). 클라이언트가 보낸 종류·이름은 버리고 슬랙 답을 쓴다 · `verified_at` 표지 ② 팬아웃 — `B/platform/external_channels_sync_store.py` `slack_fanout_targets` 가 **`verified` 이고 `access_lost` 가 없는 방만** ③ 워커 실행마다 방별 재확인(`sync.py` `_verify_slack_room` — 잃으면 `paused`+사유, 되찾으면 복구) · 백필이 `channel_not_found`·`not_in_channel`… 이면 그 방만 멈춤(`UpstreamRoomDenied`). 시험 `T/contract/test_external_sync.py` 「a_member_cannot_pick_someone_elses_dm_and_never_receives_its_events」 · 「a_room_whose_access_is_lost_pauses_and_recovers…」 |
| **F-2** available-rooms 없음 | **해소** | `application.py` `available_slack_rooms`(회원 토큰 · `users.conversations` = 참여한 공개·비공개·DM·그룹 DM · DM 상대 이름 · 그룹 DM 참여자 실명(D-12) · 봇 `is_bot`(D-13) · `already_added`) · 끊김 409 · 상류 장애 502(`entrypoints/http.py`) · 인벤토리 json 갱신. 시험 「available_rooms_lists_what_my_token_can_see_with_added_marks」 |
| **W-1** 답장 비내구 · 알 수 없는 예외 | **해소** | `BackgroundTasks` 삭제 → 접수가 「보내는 중」 행 + 첨부 대기 저장본(`replies/<uuid>/<n>`) + **내구 잡 `external.reply_deliver`** 를 한 트랜잭션에 넣는다. 연동 워커가 보낸다(`B/bootstrap/external_inbox.py` `run_inbox_reply_jobs` · 재시도 지수 물러서기 · 한도 넘으면 fail · 오래 멈춘 `sending` 재투입). `inbox.py` `deliver_reply` 에 `except Exception` → `failed`(`internal_error`) + 사건 · `abandon_reply`(저장본 유실). 받는 사람 개행은 접수에서 422 · 제목 개행 펴기. 시험 `T/contract/test_external_inbox.py` 「…survives_a_crash…」·「…unexpected_delivery_error…」·「lost_attachments…requeued」·「header_injection…」 |
| **W-2** 슬랙 파일 host 검사 | **해소** | `B/platform/external_inbox_upstream.py` `slack_file_host` — `host == d or host.endswith("." + d)`. 시험 「slack_file_hosts_need_a_real_subdomain_boundary」 |
| **W-5** 카톡 첨부 슬롯 상태 | **해소** | `B/modules/external_channels/kakao_ingest.py` `store_attachment` — `pending` 만 받고 나머지 409 `attachment_not_accepted`(동영상·음성·만료·너무 큼·이미 저장됨 · 덮어쓰기도 막음) |
| **W-12①** F-1 시험 | **해소** | 위 F-1 시험 둘 |

덤으로 닫힌 것(be23): W-3(Socket Mode 처리 실패 → gap fill 요청) · W-4(`pg_try_advisory_lock` 리더) · W-6(옛 스레드 답글 메우기 — 최근 20 스레드) · W-7(토큰 로테이션 켜진 앱은 연결 실패로 — 시험) · W-8(첨부를 읽으면서 50MB 한도) · W-9(WS `Origin` 검사, 4403) · W-10(프로필 키 = 회원 id SHA-256 앞 32자 · 옛 키도 읽음) · fe-report gap(이름표 `users` · 퍼머링크 · 워크스페이스 domain · 직책/직무).

## review-be1.md W-2~W-9

| # | 판정 | 근거 |
|---|---|---|
| W-2 state 가 브라우저에 안 묶임 | **해소** | `application.py` `complete_callback(… browser_member_id)` — 콜백 요청에 세션이 있고 그 회원이 `state` 의 회원과 다르면 `OAuthStateRejected`(400). 세션이 없으면(데스크톱이 연 OS 브라우저) 종전대로 진행. 시험 `T/contract/test_external_channels.py` 「callback_refuses_a_link_opened_in_someone_elses_logged_in_browser」 |
| W-3 `OAuthGrant` repr 토큰 | **해소** | `access_token`·`refresh_token` `field(repr=False)` + 같은 처리가 `sync.py` `IntegrationState`·`RoomState` · `inbox.py` 토큰 칸에도 · 시험 「oauth_grants_never_print_their_tokens」 |
| W-4 잘못된 키 · api_origin 검사 | **해소** | `B/bootstrap/application.py` — 키가 있으면 부팅 때 Fernet 을 만들어 잘못된 키로 실패 · **운영에서 OAuth 가 설정됐는데 키가 없으면 부팅 거절** · `settings.py` `_origin()` 로 `AX_API_ORIGIN` 도 `AX_WEB_ORIGIN` 과 같은 검사. 시험 「a_bad_encryption_key_or_a_missing_production_key_stops_the_boot」 |
| W-5 카톡 해제를 handshake 가 되살림 | **해소** | `application.py` `disconnect` — 카톡이면 그 회원의 기기 토큰도 철회 → 다음 handshake 401. 시험 「disconnecting_kakao_revokes_the_collector…」 |
| W-6 저장소 파일 겹침 | **해소(이미)** | db57ba7 에서 `external_channels_sync_store.py`·`external_channels_inbox_store.py` 로 갈림 — 이번 커밋도 그 경계 안 |
| W-7 동시 handshake·발급 경합 | **부분** | handshake — `IntegrityError` 를 잡아 이긴 쪽을 다시 읽음(`bootstrap/application.py` · 시험 「racing_first_handshakes…」). **기기 토큰 동시 발급은 그대로**(`issue_device_token` 이 회원 행을 잠그지 않고 「철회 → 추가」) — 두 탭이 동시에 누르면 활성 토큰 둘이 남을 수 있다(D-45). 영향 작음 |
| W-8 OAuth state 정리 | **해소** | `external_channels_sync_store.py` `purge_spent_oauth_states`(만료 1일 지난 것) · 연동 워커가 주기로 부름 · 시험 「spent_oauth_states_are_purged_after_a_day」 |
| W-9 시험 빈칸 | **해소** | ① PG `LISTEN/NOTIFY` — `T/integration/postgres/test_external_channels_postgres.py`(`@integration` · 커밋 뒤 사건 도착) ② 비활성 회원 기기 토큰 — 「a_device_token_of_an_inactive_member_is_refused」 ③ 카톡 해제 — 위 W-5 시험 |

## 새 WARN

| # | 근거 | 무엇 | 고칠 것 |
|---|---|---|---|
| **W-N1** (F-1 잔여 창) | `sync.py` `_verified_this_run`(방별 재확인은 **워커 실행마다 한 번**) · `slack_fanout_targets`(확인 표지만 봄) | A 가 비공개 채널·그룹 DM 에서 **나간 뒤에도**, 워커가 다시 뜰 때까지 그 방 표지가 살아 있다. 그동안 남은 동료의 토큰으로 들어오는 이벤트가 A 의 연동에 계속 복제된다(나간 뒤의 대화가 A 에게 샌다). 운영 워커는 며칠씩 재시작하지 않는다 | Socket Mode `member_left_channel`·`channel_left`·`group_left` 이벤트에서 그 회원 방을 즉시 `set_room_access(ok=False)` 하고, 재확인을 「실행마다」가 아니라 **주기(예: 1시간)**로 돌린다 |
| W-N2 | `bootstrap/external_inbox.py` 접수 → 워커 전송 | 답장이 이제 **연동 워커가 떠 있어야** 나간다. 로컬은 `make local-stack` 이 워커를 감독하니 괜찮다. 운영은 INFRA 의 연동 워커 Deployment 가 빠지면 답장이 「보내는 중」에 쌓인다(재투입은 되지만 보낼 프로세스가 없다). 또 첨부 대기 저장본(`replies/…`)은 보낸 뒤에도 지우지 않는다 | WORK-011 INFRA·반영 순서에 「연동 워커 = 답장 전송 담당」을 적는다. 저장본은 「보낸 기록」으로 둘지(D-49 대체 「계속 보관」과 같은 결) 보낸 뒤 지울지 코디가 정한다 |
| W-N3 | `application.py` `available_slack_rooms` — `q` 검색이 **받은 한 쪽(100개) 안에서만** 거름 | 방이 수백 개면 검색어에 맞는 방이 다음 쪽에 있어도 「찾는 방이 없습니다」가 뜰 수 있다 | `q` 가 있으면 커서를 끝까지 넘기며 거르거나(상한 두고), 프론트가 전체를 받아 거른다 |

## 범위 밖 · 아직 열린 것(참고)

- **BE-1 W-1**(운영 configmap 에 `AX_WEB_ORIGIN` 없음 → redirect_uri 가 localhost)은 이번 지시 범위 밖이고 **여전히 열려 있다.** 이번 커밋의 `_origin()` 검사는 형식만 본다. 운영에서 기본값 `http://localhost:5173` 은 그대로 통과한다 — INFRA·반영에서 반드시 닫을 것
- 시험·빌드는 돌리지 않았다(역할 규칙). 커밋 메시지·주석의 시험 이름으로 존재만 확인했다

## 총평

**PASS** — F-1·F-2 를 포함한 지시 항목이 닫혔다. 특히 F-1 은 접수(회원 토큰 확인) · 팬아웃(확인된 방만) · 워커(재확인·접근 상실 시 멈춤) **세 겹**으로 막혔다. 운영 전에는 이 둘을 닫기를 권한다.
- **W-N1** — 나간 방의 잔여 팬아웃 창
- **BE-1 W-1** — 운영 `AX_WEB_ORIGIN`
