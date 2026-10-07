# WORK-011 Phase BE-2 결과 보고 — 연동 워커

## 상태: done (커밋 안 함)

## 내 변경 파일 (BE-3·FE 의 동시 변경과 분리)
- 신규: modules/external_channels/sync_messages.py · platform/external_channels_sync_store.py · platform/external_slack.py · platform/external_gmail.py · platform/external_pubsub.py · bootstrap/external_worker.py · entrypoints/external_worker.py · entrypoints/slack_dev_connect.py
- 수정: modules/external_channels/sync.py(BE-1 자리 채움)
- 공용(한 줄씩): Makefile(external-worker · slack-dev-connect 타겟 + local-stack 감독 한 줄) · pyproject/uv.lock(`websockets>=13` — 이미 uvicorn[standard] 전이 의존)
- 시험: tests/contract/test_external_sync.py(10) · tests/unit/test_external_sync_messages.py(3) · tests/architecture/test_local_stack_targets.py(+1)
- **조정 1 준수**: platform/external_channels.py 는 건드리지 않음. 처음 `external_sync_store.py` 로 만든 저장소를 `external_channels_sync_store.py` 로 옮김(옮긴 것). bootstrap/application.py·http.py·inventory json 무변경 → inventory drift 없음
- bootstrap/external_worker.py 는 allowed_paths 에 명시가 없지만 WORK-011 BE-2 「파일」 칸이 지정하고, 계층 규칙(entrypoints 는 platform import 금지)상 조립 자리가 bootstrap 이라 신설

## 구현
- 워커: 주 루프(ExternalSync.tick) + Socket Mode 스레드 + Pub/Sub pull 스레드 + LISTEN ax_external_sync 스레드. 값이 없는 쪽은 스스로 쉬고 프로세스는 산다(local-stack 감독 안 깸). SIGTERM 정상 종료
- 슬랙: 이벤트 → (team, channel) 고른 모든 연동에 복제(팬아웃) · 중복 키 (연동,channel,ts) · 스레드 thread_key · 수정=원문 교체 · 삭제=raw.ax_deleted 표지(물리 삭제 없음) · 방 백필 = history 끝까지 + replies, 진행 backfill_cursor/count, 끝나면 live · 방 메타(종류·DM 상대 이름·그룹 DM 참여자 실명) · 재시작/재연결 메우기 = last_message_key 이후 · 토큰 거절 → disconnected
- Gmail: historyId 먼저 → 받은편지함 전체 백필(진행 backfill_cursor/count, 끝나면 connected) · users.watch(만료 6일 미만이면 갱신 = 매일) · Pub/Sub 알림 또는 60초 폴링 → history.list(messageAdded·INBOX) · historyId 만료(404) → 날짜 질의로 메움 · 토큰 자동 갱신 · invalid_grant/401 → disconnected · INBOX 아닌 메일은 버림
- NOTIFY ax_user_events: 실시간 저장은 메시지마다 inbox.message_arrived(한 번에 20건 넘으면 integration.changed 하나로 묶음) · 백필 쪽마다 integration.changed · 수정/삭제는 message_arrived(data.edited) · 상태 바뀜 integration.changed
- 첨부 aid(BE-3 중계가 받음): 슬랙 SHA-256("{연동}:{channel}:{ts}:{file_id}"), external_ref=file id / Gmail SHA-256("{연동}:{message_id}:{partId}"), external_ref=JSON {part_id, attachment_id}. state=reference
- safe_html(메일 소독본)은 쓰지 않음 — BE-3 몫으로 둠
- ★3: `make slack-dev-connect MEMBER=mina` — ~/.slack_test_token 을 stdin 으로, auth.test 로 team 확인 → 암호화 저장, 연결된 슬랙 연동. 운영 프로파일이면 슬랙 호출 전에 거절(시험 있음)

## 검증
- make test-unit 424 passed · make test-contract 1191 + serial 128 passed (exit 0)
- 실물(격리 PG 컨테이너 127.0.0.1:54399 · 사용자 54329 미접촉 · 종료함):
  - slack-dev-connect → MediSolve AI 연동 생성. 토큰 실제 권한 = identify + 11(channels/groups/im/mpim history·read · users:read · chat:write · files:write) — BE-1 의 추정 scope 와 일치
  - 본인과의 DM(남에게 안 보임)을 고른 방으로 → 백필 48건 · live
  - 그 DM 에 chat.postMessage 1건 → **0.53초 만에 저장 + NOTIFY inbox.message_arrived**(Socket Mode 사용자 이벤트 수신 확인)
  - 워커 종료 → 1건 보냄(0건) → 재시작 → 메우기로 저장, 전체 51건 중복 0
  - Pub/Sub: SA JWT 토큰 OK · 구독 ax-gmail-pull 은 pull 방식 · 토픽 = GMAIL_PUBSUB_TOPIC · 워커 pull 스레드 오류 없음
  - 시험 메시지 3건이 본인 DM 에 남아 있음(「[strong-hajin BE-2 수집 시험]」 머리)

## 미결·주의
- **Gmail 실물(백필·실시간·watch)은 코디 실물 확인 필요** — 실제 OAuth 동의가 있어야 연동이 생김. BE-1 보고대로 로컬 redirect_uri_mismatch 선결
- 답장+파일 전송(WORK 완료 조건)은 BE-3 라우트 몫
- acceptance-e2e 감독 목록에는 연동 워커를 넣지 않음(local-stack 만) — 시나리오가 외부 채널을 안 씀
- 메우기는 방의 최상위 글 이후만 — 워커가 꺼진 사이 **옛 스레드에 달린 답글**은 다음 실시간·백필이 아니면 안 들어온다
- 슬랙 토큰 로테이션(expires_in) 미지원 — 만료 시 disconnected 로 떨어짐
- 운영: worker kind `external`(이 엔트리포인트) replicas 1 고정은 INFRA 몫
