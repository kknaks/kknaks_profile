# 코드 검수 — WORK-011 BE-2·BE-3 (커밋 `db57ba7`) (2026-10-06)

## 판정: FAIL

FAIL 은 2건이다.
- **F-1** — **남의 슬랙 메시지가 새는 길이 하나 있다.** 슬랙 방 추가가 그 사람이 그 방을 볼 수 있는지 검사하지 않는다. 그런데 Socket Mode 팬아웃은 「그 방을 고른 모든 연동」에 복제한다.
- **F-2** — SPEC-008 §4.3 의 **`GET /api/integrations/slack/available-rooms` 가 없다.** 슬랙 방 고르기 창이 그릴 목록이 없다. 이 경로는 F-1 을 막을 자리이기도 하다. WORK-011 이 이 경로를 어느 Phase 에도 두지 않았고, 4차 검수(r4)도 못 잡았다 — 워커 탓이 아니라 계획 누락이다.

나머지 큰 축은 잘 서 있고, 시험이 실제로 덮는다.
- 조회·첨부 중계·이미지 프록시·WS·카톡 업로드의 회원 범위
- HTML 소독
- SSRF
- 한도
- hostPath
- 비밀값 로그
- Gmail watch·pull·history 공백

> 검수 방법: `git show db57ba7:…` 로만 읽었다(작업 트리는 수정 판 진행 중). 34 파일 +6550/−29. 시험·빌드는 돌리지 않았다.
> 기준: SPEC-008 v0.5.1 §2.1(F-3)·§4.3·§4.4·§4.6·§4.7·§5 · WORK-011 BE-2·BE-3 · `be2-report.md` · `be3-report.md`.
> 약칭: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/`.

## FAIL

| # | 근거 파일:줄(커밋 db57ba7) | 무엇 | 고칠 것 |
|---|---|---|---|
| **F-1** 남의 메시지 누출 | `B/modules/external_channels/application.py` `add_rooms`(BE-1 · 슬랙 `room_ids` 를 **아무 id 나** 받고 종류는 `D` 머리로 어림 · 접근 검사 없음) → `B/platform/external_channels_sync_store.py:111-117` `slack_fanout_targets`(**`(team, channel)` 만으로** 고른 방 전부) → `B/modules/external_channels/sync.py` `handle_slack_event`(대상마다 `save_messages`) | 같은 워크스페이스의 B 가 A 의 **DM·비공개 채널 id**(링크·스크린샷에서 보인다)를 `POST /api/integrations/{B 슬랙}/rooms` 에 넣는다. 그러면 A 의 사용자 토큰 쪽으로 들어온 Socket Mode 이벤트가 **B 의 연동에도 복제 저장**되고, B 의 메시지함에 뜬다. B 의 토큰으로 하는 백필은 `channel_not_found` 로 실패하지만 **실시간 팬아웃은 막히지 않는다.** D-24(본인만 본다) 위반이다 | ① 슬랙 방 추가 때 **그 회원 토큰으로 접근을 확인**한다(`conversations.info` 성공 + 채널이면 `is_member`). 실패한 id 는 422. 가장 쉬운 자리는 F-2 의 available-rooms 결과 안의 id 만 받는 것 ② 팬아웃은 **접근이 확인된 방**만 받는다(방 메타에 `verified_at`, 백필이 `channel_not_found`·`not_in_channel` 이면 그 방을 `paused`+사유로 떨어뜨리고 팬아웃 대상에서 뺀다) ③ contract 시험: 「남의 DM id 를 고른 회원에게 그 DM 이벤트가 가지 않는다」 |
| **F-2** 계약 누락 | SPEC-008 §4.3 `GET /api/integrations/slack/available-rooms?q&cursor` → `{rooms:[{room_id, type, name, is_bot, member_count, already_added}], next_cursor}` · AC-02·03 / 커밋 전체에 경로 없음(`git grep available-rooms db57ba7 -- backend/src` 0) · `B/platform/external_slack.py` 에 `conversations.list`(users.conversations) 없음 | 설정 슬랙 「방 추가」 창(DC-2 §2.2)이 그릴 목록이 없다 — FE-b 가 막힌다. 그룹 DM 실명 풀기(D-12)·봇 DM `앱`(D-13)·「추가됨」도 이 응답의 몫이다 | 백엔드에 한 경로 추가: 사용자 토큰으로 `users.conversations`(types=public_channel,private_channel,im,mpim · cursor) → DM 은 상대 이름, mpim 은 참여자 실명, 봇이면 `is_bot`, 이미 고른 방은 `already_added`. 끊김이면 409. WORK-011 에 이 줄을 더한다 |

## 항목별 판정

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| 1 | 슬랙 Socket Mode 단일 소유 | **WARN(W-4)** | `B/bootstrap/external_worker.py`(Socket Mode 스레드 하나 · 앱 토큰 없으면 끔) — 레플리카 1 은 **가정**일 뿐 코드가 강제하지 않는다. 둘이 뜨면 슬랙이 이벤트를 연결끼리 나눠 주므로 저장 누락은 없다. 다만 백필·메우기·watch 를 두 번 한다 |
| 2 | 사람별 팬아웃·중복 0 | **FAIL(F-1)** / 중복은 PASS | 중복 키 `(연동, channel, ts)` + `save_messages` 가 연동 행을 잠그고 기존 키를 거른다(`external_channels_sync_store.py:130-`) · 시험 `T/contract/test_external_sync.py:153` · 실물 51건 중복 0(be2-report). 대상 선정이 F-1 |
| 3 | 백필·메우기 정확성 | PASS(경미 W-6) | 방 백필 = history 끝까지 + 스레드 replies · `backfill_cursor` 이어 가기 · 끝나면 `live`(`sync.py` `_slack_backfill_page`) · 재시작 메우기 = `last_message_key` 이후(`_slack_gap_fill`) · 시험 `:194`·`:222`. 꺼져 있던 동안 **옛 스레드에 달린 답글**은 빠진다(보고서 자인) → W-6 |
| 4 | Gmail watch 갱신·pull ack·history 공백 | PASS | `sync.py` `_mail_step`: historyId 를 **백필보다 먼저** 잡음 · watch 만료 6일 미만이면 갱신(=매일) · 60초 history 폴링 + Pub/Sub 알림 즉시 · `HistoryExpired`(404) → 마지막 수집 하루 전부터 날짜 질의로 메움 + 새 historyId · INBOX 아닌 메일 버림(D-10) · 토큰 자동 갱신·`invalid_grant` → disconnected. `external_pubsub.py` 는 알림을 「훑어라」 신호로만 쓰고 바로 ack 한다 — 놓쳐도 폴링이 받는다(설계상 맞음). watch 는 `labelIds:["INBOX"]`. 시험 `:268`·`:297`·`:312` |
| 5 | 남의 메시지 누출 — 조회 | PASS | `external_channels_inbox_store.py` `mail_for`·`room_for`(회원 + 연동·방 미삭제 조건) · 목록·미읽음·read-all 전부 `member_id` 범위 · 시험 `T/contract/test_external_inbox.py:260`·`:305`·`:328`·`:344` |
| 5b | — 첨부 중계 | PASS | 메일: `_owned_mail` 뒤 aid 를 **원문 partId 로 다시 계산해 대조**(`inbox.py` `mail_attachment`) · 방: `_owned_room` 뒤 `attachment_in_room(room.id, aid)` · 시험 `:376-377`·`:410` |
| 5c | — 이미지 프록시 | PASS | `_owned_mail` 뒤 **그 메일 안전본의 `data-ax-remote-src` 집합에 있는 주소만**(`inbox.py` `remote_image` · `inbox_html.py` `remote_image_urls`) · 시험 `:413-422` |
| 5d | — WS | PASS(경미 W-9) | `user_event_hub.py` 가 `member_id` 큐에만 넣음 · 미인증 4401 · 시험 `:513`·`:532` · `T/contract/test_kakao_ingest_and_profile.py:175` |
| 5e | — 카톡 업로드 | PASS | 기기 토큰 회원의 카톡 연동 → `selected_room(integration.id, room_id)`(아니면 403) · 첨부는 **연동 범위 + aid**(`kakao_attachment(integration.id, aid)`) — BE-1 리뷰 지적 반영 · 시험 `:89-95`·`:132-135` |
| 6 | HTML 소독 우회 | PASS | `inbox_html.py`: lxml 로 먼저 `src` 를 다시 씀(cid → 중계 경로 · 원격 → `data-ax-remote-src` · 그 밖 제거) → **nh3 허용 목록**(태그·속성 제한 · `clean_content_tags` 에 script/style/iframe/object/embed/form/svg/math · href 는 http(s)/mailto/tel/# 만 · img src 는 래스터 `data:`·`/api/inbox/mail/` 만 · style 은 `url(`·`@import`·`expression(`·`javascript:` 거절 · `target` 은 `_blank` 고정 · `rel=noopener noreferrer`) → **소독 뒤에** CSP meta(`default-src 'none'; img-src 'self' data:`). 원문 `raw` 는 그대로(D-28). 시험 `T/unit/test_inbox_rules.py:47`(적대 입력 묶음)·`:56` · contract `:284`. iframe 토큰(`allow-same-origin allow-popups allow-popups-to-escape-sandbox`)은 FE 계약 — 프론트 검수 몫 |
| 7 | 이미지 프록시 SSRF | PASS | `external_inbox_upstream.py` `SafeImageFetcher`: http(s)만 · 자격증명 URL 거절 · 포트 80/443/8080/8443 · **푼 주소 전부가 공인**(사설·루프백·링크로컬(169.254 메타데이터)·멀티캐스트·예약·미지정 · IPv4-mapped IPv6 도 풂) · **푼 주소로 핀 연결**(SNI·인증서는 원래 이름 — DNS rebinding 차단) · 리다이렉트 안 따름 · 래스터 MIME 만(SVG 거절) · 5MB(Content-Length + 실제 바이트). 시험 unit `:107`·`:122`·`:130` |
| 8 | 첨부 한도 | PASS(경미 W-8) | 메일 **합계** 25MB(`inbox.py` `accept_mail_reply` · 인코딩 전 바이트 합) · 슬랙 파일당 50MB · 카톡 파일당 50MB(`file.size` 사전 검사 + 읽은 바이트 재검사) · 프로필 1MB(바이트 머리로 PNG/JPG 판정) · 시험 `:451` · kakao `:211` |
| 9 | hostPath 경로 조작(`../`) | PASS(경미 W-10) | `B/platform/external_storage.py`: 키 정규식(`kakao/<uuid>/<sha256>` · `profiles/<id>/<uuid>`) + `..` 거절 + resolve 뒤 루트 안인지 확인 · 키는 서버가 만든다(`kakao_storage_key(integration.id, attachment.aid)` — 요청의 aid 가 아니라 DB 의 aid) · 임시 파일 → `os.replace` |
| 10 | 비밀값 로그 | PASS | 상류 로그는 host·HTTP 코드·슬랙 error 코드만(`external_inbox_upstream.py` `_call`·`SlackInboxApi._api` · `external_pubsub.py`) · SA 키는 메모리만 · 개발 슬랙 토큰은 stdin(`slack_dev_connect.py`) · 중계 응답 `X-Content-Type-Options: nosniff` + `Content-Security-Policy: … sandbox` + `CORP same-origin`(`http_inbox.py` `RELAY_HEADERS`) |
| 11 | 답장(BackgroundTasks 비내구) | **WARN(W-1)** — 지적만 | `http_inbox.py` `reply_inbox_room`·`reply_inbox_mail` → `background.add_task(deliver_inbox_reply)` · 아래 W-1 의 「삼키지 않는 예외」는 수정 판에서 함께 볼 것 |
| 12 | 시험이 계약을 덮나 | PASS(빈칸 W-12) | contract 34(inbox 15 · sync 10 · kakao/profile 9) + unit 13 · 실물: 슬랙 Socket Mode 0.53초 수신·메우기 · PG NOTIFY→WS(be2·be3 보고) · inventory drift 검사가 `http_inbox.py` 도 읽게 고침 |

## 경미 (WARN) — 고칠 것

| # | 근거 파일:줄 | 무엇 | 고칠 것 (한 줄) |
|---|---|---|---|
| W-1 | `B/modules/external_channels/inbox.py` `deliver_reply`(`except (UpstreamFailed, IntegrationUnavailable)` 만) · `_send_mail`(`EmailMessage` 머리에 개행이 든 주소·제목이면 `ValueError`) · `TokenDecryptionFailed` | 비내구성(알려진 것)에 더해, 위 두 종류 밖의 예외가 나면 그 답장은 **`sending` 에 영원히 남고 사건도 안 간다**(화면은 「보내는 중」에서 멈춤) | 수정 판의 durable job 에서 「알 수 없는 예외 → `failed`(`internal_error`, retryable=false) + 사건」 한 갈래를 더한다. 받는 사람·제목 개행은 accept 단계에서 422 |
| W-2 | `B/platform/external_inbox_upstream.py` `SlackInboxApi.download` — `hostname.endswith(("slack.com", "slack-edge.com", "slack-files.com"))` | 점이 없어 `evilslack.com` 도 통과한다 → 그 주소로 **회원의 슬랙 토큰이 실린다.** 주소는 슬랙이 만든 `files[]` 에서 오므로 지금은 위험이 낮다. 하지만 이 검사가 존재하는 이유를 스스로 깬다 | `host == d or host.endswith("." + d)` |
| W-3 | `B/platform/external_slack.py:138-148` `SlackSocketMode.run` — envelope 를 **먼저 ack** 하고 처리 · 처리 실패는 로그만 | DB 가 잠깐 끊기면 그 이벤트는 슬랙이 다시 안 보낸다. 다음 재시작·재연결 메우기 때까지 빠진다 | 처리 실패면 `on_reconnect`(=`request_gap_fill`)를 불러 다음 바퀴에 메우게 한다 |
| W-4 | `B/bootstrap/external_worker.py` · `entrypoints/external_worker.py` | 단일 소유를 코드가 강제하지 않는다. 차트의 공용 `worker.replicas` 를 누가 올리면 백필·메우기·watch 를 두 프로세스가 한다(중복 저장은 키가 막는다) | 시작 때 `pg_try_advisory_lock(<상수>)` — 못 잡으면 대기(리더 하나) |
| W-5 | `B/modules/external_channels/kakao_ingest.py` `store_attachment` — 첨부 `state` 를 보지 않고 저장 · 덮어씀 | `not_stored`(동영상·음성)·`expired`·`too_large` 슬롯에도 바이트를 올려 `stored` 로 바꿀 수 있다(D-31 「동영상·음성 = 표시만」을 앱이 어기면 서버가 받아 줌) | `pending` 일 때만 받고 나머지는 409 |
| W-6 | `sync.py` `_slack_gap_fill`(최상위 글 이후만) | 꺼져 있던 동안 옛 스레드에 달린 답글이 빠진다(be2-report 자인) | 메우기 때 `reply_count>0` 이고 `latest_reply > last_message_key` 인 부모의 `replies` 를 함께 훑는다 |
| W-7 | `B/platform/external_slack.py` · be2-report 「토큰 로테이션 미지원」 | 슬랙 앱에 토큰 로테이션이 켜져 있으면 12시간 뒤 전원 `disconnected` | 슬랙 앱 설정에서 로테이션이 **꺼져 있음**을 운영 체크리스트(WORK-011 Pre-deploy)에 한 줄 |
| W-8 | `B/entrypoints/http_inbox.py` `_outgoing`(파일 전부를 메모리로 읽은 뒤 한도 검사) · CHART `proxyBodySize: 50m` | 한도 판정 전에 메모리를 먼저 쓴다(ingress 가 상한). ingress 50m 이 앱 한도 50MB 와 같아 nginx 가 먼저 413(INFRA 알려진 할 일) | 읽기를 `read(limit+1)` 로 끊고, INFRA 에서 `proxyBodySize` 60m 이상 |
| W-9 | `http_inbox.py` `inbox_stream` — `Origin` 검사 없음 | 쿠키 인증 WS 는 교차 사이트 핸드셰이크를 SameSite=Lax 에 기댄다. 내용은 id 뿐이라 영향은 작다 | 핸드셰이크에서 `Origin == AX_WEB_ORIGIN`(데스크톱은 같은 origin) 확인 한 줄 |
| W-10 | `external_storage.py` `_SAFE_KEY` 의 `profiles/[A-Za-z0-9_.-]{1,100}/…` | 회원 id 에 이 밖의 글자(`@`·한글 등)가 있으면 프로필 저장이 `ValueError` → 500 | 키에 회원 id 대신 그 id 의 SHA-256 앞 32자를 쓴다 |
| W-11 | be3-report 「목록 메일 카드 `from` → `sender`」 | SPEC-008 §4.4 와 어긋남 | SPEC 쪽을 `sender` 로 고치는 것이 맞다(코디 판단) — FE-a 에 알림 |
| W-12 | 시험 빈칸 | ① **F-1**(남의 방 id 를 골라도 이벤트가 안 감) ② `deliver_reply` 의 알 수 없는 예외 → `failed` ③ 카톡 첨부를 `pending` 아닌 슬롯에 올리면 거절(W-5) | 각 contract 하나 |

## 확인한 것 — 참고

- 우리가 보낸 슬랙 답장은 방에 바로 넣지 않고 Socket Mode 가 같은 키로 들여온다(be3-report 3) — 중복 키 `(연동, channel, ts)` 와 맞는다. 다만 **고른 방 쪽 이벤트가 안 오면**(예: 내 DM 이 아닌 방에서 F-1 수정으로 접근 확인이 실패해 `paused`) 보낸 글이 안 보일 수 있다 — F-1 고칠 때 함께 볼 것
- 개발 슬랙 토큰 이음새(`connect_dev_slack`)는 운영·개발 인증이 꺼진 프로파일이면 **슬랙 호출 전에** 거절 — 시험 `test_external_sync.py:325`. 4차 ★3 해소
- 중계 응답 inline 허용은 래스터 이미지 + 기존 `inline_media_type`(PDF·markdown)뿐이고, 응답 CSP 에 `sandbox` 가 있어 같은 origin 에서 실행되지 않는다

## 총평

**FAIL** — 구조와 보안 기본기(소독·SSRF·회원 범위·경로·로그)는 좋다. 다음 Phase 에 넘기기 전에 이 두 건을 닫는다.
- **F-1** — 슬랙 방 접근 확인 + 팬아웃 대상 제한
- **F-2** — `available-rooms` 경로. F-1 의 확인 자리이기도 하다

둘은 한 번에 고칠 수 있는 크기다. W-1 은 진행 중인 수정 판(durable 답장)에서 함께 닫는다. W-2·W-5 는 한두 줄짜리라 같이 고치기를 권한다. 재검수는 **F-1·F-2·W-1·W-2·W-5·W-12①** 만 보면 된다.
