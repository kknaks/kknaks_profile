# WORK-011 BE-3 결과 보고 — 메시지함·답장·프로필·카톡 수신 API

## 상태: done (커밋 안 함 · 워크트리 변경만)

## 수행 내용 (BE-3 파일)
신규
- `modules/external_channels/inbox.py` — 목록(카드: 메일 단건/방 하나 · source·unread·cursor · `unread_counts`) · 메일 본문(안전본 lazily 생성·`safe_html` 저장) · 방 메시지(페이지·thread_ts) · 읽음(메일·방 up_to_ts 단조·read-all) · 첨부 중계(메일=partId 로 최신 attachmentId 재조회 · 슬랙 · 카톡 저장본/410) · remote-image(본문에 있는 주소만) · 답장(슬랙·메일 · Idempotency-Key · 실패분 같은 키 재전송 = 「다시 보내기」 · 결과 `inbox.reply_result` 사건) · Gmail 토큰 갱신 · 상류 거절 시 연동 `disconnected` + `integration.changed`
- `modules/external_channels/inbox_html.py` — nh3 허용목록 소독 + lxml 전처리(원격 img → `data-ax-remote-src`, `cid:` → 첨부 중계 경로, 인용 `<details>`) + CSP meta. BE-2 가 수집 때 `sanitize_mail_html` 을 불러도 된다
- `modules/external_channels/kakao_ingest.py` — messages(403·413·중복 `(연동,chatId,logId)`·aid=domain 식·`backfill_done`→live·미업로드 첨부 슬롯) · attachments(**연동 범위 + aid** · 50MB · hostPath) · status(전문 저장 · 바뀐 보고만 사건 · `selected_rooms_version`) · handshake 전 = 409 `handshake_required`
- `modules/organization_access/profile_settings.py` — 이미지(1MB·PNG/JPG 바이트 판정·교체 시 옛 저장본 삭제) · 비밀번호 변경(현재 확인 401 `current_password_incorrect` · 규칙 422 `password_rejected` · **이 세션 외 일괄 revoke + 기기 토큰 일괄 철회**, 한 트랜잭션)
- `platform/external_channels_inbox_store.py` (조정 1 의 BE-3 저장소) · `platform/external_inbox_upstream.py`(Gmail/슬랙 중계·보내기 · SSRF 이미지 fetcher: http(s)·포트 제한·**모든 해석 주소 공인**·해석 주소에 핀 연결·리다이렉트 안 따름·래스터 MIME 만(SVG 거절)·5MB) · `platform/external_storage.py`(hostPath 키 검사) · `platform/user_event_hub.py`(LISTEN 스레드 1개 → member_id 큐)
- `bootstrap/external_inbox.py` — 조립 믹스인(시험 대역 자리 `_inbox_mail_api`·`_inbox_slack_api`·`_inbox_image_fetcher`)
- `entrypoints/http_inbox.py` — 라우트 18 + WS `/api/inbox/stream`
- 시험: `tests/contract/test_external_inbox.py`(15) · `tests/contract/test_kakao_ingest_and_profile.py`(9) · `tests/unit/test_inbox_rules.py`

공용 파일(최소 수정)
- `entrypoints/http.py` — import 1줄 + `register_inbox_routes(app)` 1줄
- `bootstrap/application.py` — import 1줄 · `class WorkflowApplication(ExternalInboxOperations)` · `my_organization_profile` 이 `profile_image_url` 을 더함(3줄)
- `modules/organization_access/results.py` — `MyOrganizationProfileView.profile_image_url: NotRequired[str|None]`
- `backend/pyproject.toml`·`uv.lock` — `nh3`, `lxml`(이미 전이 의존 — 직접 import 하므로 명시)
- `docs/unified-operations-inventory.json` — MCP `my_organization_profile` output_schema diff 1항목 패치 + BE-3 HTTP 18행(excluded/E2) 추가 · http_count 173→191
- `tests/architecture/test_operation_inventory.py` — drift 검사가 `http_inbox.py` 도 읽게(안 그러면 새 라우트가 drift 검사를 빠져나간다)
- `tests/contract/test_product_operations.py` — `/api/organization/me` 기대 모양에 `profile_image_url: None` (의도된 계약 변경)
- **`platform/external_channels.py` 는 건드리지 않았다**(조정 1 — 옮긴 것 없음, 처음부터 새 파일). 스키마 변경 없음(BE-1 표 그대로)

## 테스트 결과
- `make test-unit`(unit+architecture): **470 passed**
- `make test-contract`(병렬, 1회): 1214 passed / 1 failed → 실패 = `/me` 응답 모양(의도된 변경) → 기대값 갱신 후 해당 + 관련 파일 `make test-contract-serial FILES=…` **64 passed**
- 실물 1회(로컬, scratchpad 의 일회용 PG17 + 별도 uvicorn — 사용자 스택·포트 안 건드림, 끝나고 정리): **26/26 PASS** — 가짜 수집기(기기 토큰→handshake→웹 방 고르기→묶음·중복·첨부 업로드→hostPath→메시지함 카드·대화·저장본 받기·읽음) · 고르지 않은 방/뺀 방 403 · **WS 새 메시지 알림(PG NOTIFY→LISTEN)** · **다른 프로세스 NOTIFY → 그 회원 WS 만(남의 것·깨진 페이로드 버림)** · 메일 HTML 소독(script·on*·form·iframe·javascript: 제거·원격 이미지 차단·인용 details·원문 보존) · 프로필 이미지 저장/조회/me 반영/1MB 413 · 비밀번호 변경 → 이 세션 유지·다른 세션 401·기기 토큰 401
  - 실물에서 WS 닫힘 버그 1건 발견·수정(클라이언트가 먼저 떠난 뒤 close → traceback). 재확인 traceback 0
- 슬랙·Gmail **답장/첨부 중계 실물은 미확인 — 코디 실물 확인 필요**(BE-2 연동 생성 뒤). 계약 시험은 상류 대역으로 통과

## 다른 팀 영향 (FE)
- 목록 `GET /api/inbox/messages` → `{items, next_cursor, unread_counts:{all,mail,slack,kakao}}`. 모든 카드에 `kind`(mail/slack/kakao)·`at`. 메일 카드 `{message_id, integration_id, account, subject, sender, unread, attach_count, snippet}` · 방 카드 `{room_id, integration_id, room_type, title, member_count, unread_count, last_at, preview:[{author,text,at}]}`. **SPEC 의 `from` 은 `sender` 로 냈다**(Python 예약어 회피 — FE 에 알림 필요)
- 메일 본문 → `{…, sender, to[], cc[], reply_to[], date, safe_html, attachments[{aid,name,size,mime,kind,state}], sent_replies[{local_id,status,payload,error,created_at,sent_at}]}`. **원격 이미지는 `<img data-ax-remote-src="…">`(src 없음)** — 「이미지 보기」 때 FE 가 `src=/api/inbox/mail/{id}/remote-image?u=<encode>` 로 바꿔 단다. 안전본 맨 앞에 CSP meta
- 방 메시지 → `{room:{room_id,integration_id,kind,room_type,name,member_count,external_id,read_up_to_key}, messages:[{id,key,at,author,thread_key,raw,attachments}], next_cursor}` — 페이지 안은 오래된→최신, cursor 는 과거로
- 답장은 **multipart**: 슬랙 `text`·`thread_ts`·`files` / 메일 `body`·`reply_all`·`to`(반복)·`cc`(반복)·`files` + `Idempotency-Key` 헤더. 응답 `202 {local_id}`, 결과는 WS `inbox.reply_result {data:{local_id,status:sent|failed,error?,retryable?}}`. 실패 후 **같은 키로 다시 POST = 다시 보내기**. 메일 `to` 를 비우면 원문 Reply-To/From, 전체 답장이면 cc 를 원문 To+Cc(나 제외)로 채운다
- WS `/api/inbox/stream`: 쿠키 인증, 첫 프레임 `{"type":"ready"}`, 이후 `{type, integration_id?, room_id?, message_id?, source_kind?, data?}`. 미인증 = close 4401
- 오류 코드: 409 `{code: integration_disconnected|read_only|handshake_required}` · 410 `{code: expired|too_large|not_stored}` · 400 `remote_image_rejected` · 401 `current_password_incorrect` · 422 `password_rejected|invalid_request` · 502 `upstream_failed`
- 프로필: `PUT /api/profile/image`(multipart `file`) → `{profile_image_url: "/api/profile/image?v=<ms>"}`; `/api/organization/me`·`/api/auth/me`·로그인 응답에 `profile_image_url`
- 카톡 첨부 업로드(SPEC-009 Rust): **multipart `file`** + 선택 `name`·`mime` 폼 필드

## SPEC 과 어긋남·미결 (planner/코디 판단)
1. 목록 메일 카드의 `from` → `sender` 로 이름 바꿈(위). 수용 여부 확인 필요
2. 답장 보내기는 FastAPI BackgroundTasks — **비내구**(back 이 보내는 도중 죽으면 그 답장은 `sending` 에 남음). durable job 화는 후속 판단
3. 우리가 보낸 슬랙 메시지는 방 대화에 바로 넣지 않는다 — BE-2 Socket Mode 수집이 같은 키 `(연동,channel,ts)` 로 들여온다(중복 없음)
4. 프로필 이미지 「정사각형」은 서버가 강제하지 않는다(크기·형식만). WS `/api/inbox/stream` 은 inventory(HTTP 데코레이터만 스캔) 밖 — 회의 WS 와 같은 처지
5. 신규 표 없음이라 `docs/domain-model.md` 는 안 고쳤다(BE-1 이 표를 이미 적음). 필요하면 모듈 줄 추가는 코디 판단
6. BE-2 와의 계약 가정: Gmail `raw` = messages.get format=full, 첨부 aid = SHA-256("{연동}:{gmail id}:{partId}") / 슬랙 첨부 `external_ref` = file id — BE-2 의 `sync_messages.py` 와 일치 확인함. `safe_html` 은 비어 있어도 됨(메시지함이 처음 열 때 채움)
