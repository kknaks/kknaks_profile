# BE 수정 판 1·2·3 결과 보고 (한 판)

## 상태: done (커밋 안 함 · frontend/ 무접촉)

## 판 1 — BE-1 검수 WARN + 답장 내구
| 항목 | 한 일 | 시험 |
|---|---|---|
| W-2 링크 넘기기 | 콜백에 세션 쿠키가 있고 그 회원 ≠ state 회원이면 400(state 는 소비됨). 쿠키 없으면(데스크톱 OS 브라우저) 종전대로 | contract `test_callback_refuses_a_link_opened_in_someone_elses_logged_in_browser` |
| W-3 repr | OAuthGrant·RefreshedToken·IntegrationState/RoomState 토큰 칸 `repr=False` | `test_oauth_grants_never_print_their_tokens` |
| W-4 부팅 | 키가 주어지면 부팅 때 Fernet 생성(잘못된 키 = 부팅 실패) · **운영 + OAuth 설정 + 키 없음 = 부팅 실패**(OAuth 를 안 쓰는 운영은 그대로 뜸 — 기존 운영·시험 보호) · `AX_API_ORIGIN` 도 web_origin 과 같은 검사 | `test_a_bad_encryption_key_or_a_missing_production_key_stops_the_boot` |
| W-5 카톡 해제 | 카톡 disconnect 가 그 회원 기기 토큰도 철회 → handshake 가 되살리지 못함. 뺀 방은 handshake·업로드(403)에서 돌아오지 않음 | `test_disconnecting_kakao_revokes_the_collector...` |
| W-7 경합 | 기기 토큰 발급 = 회원 행 잠금 후 철회·추가 · 첫 handshake 유니크 위반은 잡아 다시 읽음(1회 재시도) | `test_racing_first_handshakes_reread_the_winner...` |
| W-8 state 정리 | 연동 워커 주기 일(1시간) — 만료 1일 지난 state 삭제 | `test_spent_oauth_states_are_purged_after_a_day` |
| W-9 시험 | PG NOTIFY integration 시험 신설 · 비활성 회원 기기 토큰 401 | `tests/integration/postgres/test_external_channels_postgres.py` · `test_a_device_token_of_an_inactive_member_is_refused` |
| **답장 내구** | BackgroundTasks 제거. 접수 = 「보내는 중」 행 + 첨부 대기 저장본(hostPath `replies/<local_id>/<n>`) + `durable_jobs` 잡(`external.reply_deliver`, 같은 방·메일은 순서대로) **한 트랜잭션** + `ax_external_sync` 깨움. 연동 워커가 잡을 집어 보내고 결과 반영. lease 만료 = 재시도 · 5회 넘으면 failed · 1분마다 5분 넘게 「보내는 중」인 답장 재투입 · 저장본 유실 = failed(`attachments_lost`). at-least-once(상류 수락 직후·커밋 전 죽으면 한 번 더 갈 수 있음) | `test_an_accepted_reply_survives_a_crash...` · `test_lost_attachments_fail_the_reply_and_stuck_replies_are_requeued` |

## 판 2 — BE-2·3 검수 FAIL 2 · WARN
| 항목 | 한 일 | 시험 |
|---|---|---|
| **F-1 누출** | 슬랙 방 추가 = 그 회원 토큰으로 `conversations.info`(공개 채널은 is_member 까지) — 실패 422 · 클라 종류·이름 무시, 슬랙 답 사용 · `room_meta.verified_at` · **팬아웃 = 확인된 방만** · 워커가 실행마다 방 재확인 → 잃으면 `paused`+`access_lost`(팬아웃·수집 제외), 되찾으면 복귀 · 백필 중 channel_not_found 도 같은 처리 | `test_a_member_cannot_pick_someone_elses_dm_and_never_receives_its_events` · `test_a_room_whose_access_is_lost_pauses_and_recovers...` · BE-1 시험 `D-someone-else`→422 |
| **F-2** | `GET /api/integrations/slack/available-rooms?q&cursor` → `{rooms:[{room_id,type,name,is_bot,member_count,already_added}],next_cursor}` (users.conversations · 참여한 방만 · DM=상대 이름 · 그룹 DM=참여자 실명 · 봇 표시) · 연동 없음 404 · 끊김 409 `{code:disconnected}` · 상류 장애 502 | `test_available_rooms_lists_what_my_token_can_see_with_added_marks` |
| W-1 | 알 수 없는 예외 → failed(`internal_error`, retryable=false)+사건 · 주소 개행 422 · 제목 개행 폄 | `test_an_unexpected_delivery_error...` · `test_header_injection...` |
| W-2 | 슬랙 파일 host = `d` 또는 `.d` 로 끝남 | `test_slack_file_hosts_need_a_real_subdomain_boundary` |
| W-3 | Socket Mode 처리 실패 → 메우기 요청 | (코드) |
| W-4 | `pg_try_advisory_lock` 리더 하나 — 못 잡으면 대기 | 실물 로그 「holds the single-owner lock」 |
| W-5 | 카톡 첨부 업로드는 `pending` 슬롯만 — 그 밖 409 `attachment_not_accepted`(덮어쓰기·동영상·만료 거절) | kakao 시험 보강 |
| W-6 | 메우기 때 최근 스레드 20개 답글을 지점 이후로 다시 훑음 | `test_restart_gap_fill_also_picks_up_new_replies_in_old_threads` |
| W-7 | 슬랙 OAuth 응답에 refresh_token/expires_in(로테이션 켜짐) → 연결 실패(connect=error) + 로그 · **운영 체크리스트 「슬랙 앱 토큰 로테이션 끔」은 WORK 문서 몫** | `test_a_slack_app_with_token_rotation_fails_the_connection` |
| W-8 | 답장 첨부 읽기를 50MB+1 에서 끊음 · 개수 초과는 읽기 전 422 (ingress 60m 은 INFRA) | (기존 413 시험 통과) |
| W-9 | WS `Origin` ≠ AX_WEB_ORIGIN 이면 4403(루프백끼리 같은 포트는 같다 · Origin 없으면 쿠키로만) | `test_inbox_stream_refuses_a_cross_site_origin` |
| W-10 | 프로필 키 = `profiles/<회원 id SHA-256 앞 32자>/<uuid>`(옛 키도 읽음) | 프로필 시험 보강 |
| W-12 | ①②③ 모두 위 시험 | — |

## 판 3 — FE 요청 응답 칸 (바뀐 응답 모양)
| 경로 | 더한 칸 | 값 |
|---|---|---|
| `GET /api/inbox/rooms/{id}/messages` | `users: {user_id: {name, is_bot, avatar}}` (페이지 최상위) | 연동 워커가 그 회원 토큰으로 보낸 사람·답글 단 사람·본문 멘션 `<@U…>` 을 풀어 `room_meta.users` 에 모음. 카톡은 `{}` |
| 같은 응답 `room` | `permalink: str\|null` | `https://<domain>.slack.com/archives/<channel>` (슬랙만) |
| 같은 응답 `messages[]` | `permalink: str\|null` | `…/archives/<channel>/p<ts 점 없이>` · 답글이면 `?thread_ts=…&cid=…` |
| 같은 응답 `messages[].author` · 목록 preview | (값 변경) | 슬랙 user id → **이름**(풀었을 때) |
| `GET /api/integrations` 항목 | `domain: str\|null` | 슬랙 워크스페이스 `<team>.slack.com`(워커가 auth.test 로 1회 · 개발 토큰 이음새도 저장) |
| `GET /api/organization/me`·`/api/auth/me`·로그인 응답 | `position: str\|null` · `job: str\|null` | 주 보직의 직책 · 주 직무(명부, 읽기 전용) |
| `GET /api/integrations/slack/available-rooms` | 신설(위 F-2) | SPEC §4.3 모양 그대로 = fe-report 기대와 같음 |
| `POST /api/inbox/{rooms\|mail}/…/reply` | 응답 모양 그대로 `{local_id}` | 전송이 내구 잡으로 — 결과는 종전대로 WS `inbox.reply_result`. 「보낸 답장」 payload.files 에 내부 저장 키는 내지 않음 |

## 검증
- make test-unit 470 passed
- make test-contract: 병렬 1233 passed + 1 failed(`test_product_operations::test_organization_profile_is_a_persisted_authorized_projection` — `/me` 에 판 3 의 두 칸이 생겨 정확 일치 기대가 깨짐 → 기대에 두 칸 추가 후 통과) · make test-serial SERIAL_PATHS=tests/contract 128 passed
- 격리 PG(127.0.0.1:54399 · 종료) make test-postgres 106 passed(새 NOTIFY 시험 포함)
- tests/architecture 45 passed · inventory 는 다른 항목만 패치(available-rooms 행 추가 · 답장 두 라우트 서명 · `/me` 가 부르는 소유 호출 3행 · MCP `my_organization_profile` 출력 스키마)
- (주의) 중간에 `make test-contract-serial` 을 FILES 없이 불러 전체 직렬로 돌기 시작한 것을 끊었다 — 결과 무관
- 실물(격리 PG · 실제 슬랙 · 개발 토큰): domain=medi-solve-ai.slack.com · available-rooms 첫 쪽 100개(채널 52·비공개 4·그룹 DM 35·DM 9 · 봇 5) 그룹 DM 실명 · 본인 DM 추가 202 · 볼 수 없는 DM id 422 · 워커 리더 잠금 · 백필 뒤 방 permalink·메시지 permalink·users 이름표·author 이름 확인

## 미결·주의
- **available-rooms 첫 쪽이 실측 20.6초**(그룹 DM 35개마다 참여자 조회 + users.info). 같은 프로세스 안에서는 이름을 기억해 두 번째부터 빠르다. FE 는 로딩 상태 필수 · 더 줄이려면 users.list 선읽기나 그룹 DM 이름 지연 풀기(다음 판)
- 공개 채널은 참여(is_member)해야 고를 수 있다 — 참여 안 한 공개 채널은 available-rooms 에도 안 나옴(users.conversations)
- 답장 전송은 이제 **연동 워커가 떠 있어야** 나간다(local-stack 에 이미 포함). 워커가 없으면 「보내는 중」 유지 → 워커가 뜨면 나감
- W-1(검수 BE-1 의 운영 AX_WEB_ORIGIN)은 이번 목록 밖 — INFRA 몫 그대로
- 슬랙 토큰 로테이션 끔 확인은 운영 체크리스트에 한 줄 필요(문서)
- docs/domain-model.md 에 답장 내구 잡·방 접근 확인·이름표 한 줄씩 추가
