---
type: work
id: WORK-011
title: "직원 앱 내부 채팅 — 1판(표 · API 14 · SSE · 푸시 · 사진 · 5탭 · 대화 · 방 정보) → r3(수정 · 동영상 · 여러 개 · [+] 시트 · 입력창 · 5메뉴 · 공유 · 링크) → REVIEW → 시뮬레이터 → infra 확인 → 실기기 iOS E2E → r4(앱 안 전달 · 통역 드로어) → REVIEW3 → 시뮬레이터 → 빌드 13 → 실기기 → r5(사진 · 동영상 모아보기 · 초대 · 들어온 뒤 대화만) → REVIEW4 → 시뮬레이터 → 빌드 14 → 실기기"
status: draft
product: cc-prototype
feature: procedure
work_type: enhancement
owner: kknaks
progress: 96
created_at: 2026-10-29
updated_at: 2026-10-30
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/draft
links:
  baselines:
    - "[[baseline-010-internal-chat|BASE-010]]"
  decisions:
    - "[[decision-009-internal-chat|DEC-009]]"
  specs:
    - "[[spec-007-internal-chat|SPEC-007]]"
    - "[[spec-004-procedure-app|SPEC-004]]"
  works:
    - "[[work-009-app-v2|WORK-009]]"
    - "[[work-010-customer-questionnaire-web|WORK-010]]"
  releases: []
  related: []
sources:
  - "orchestration/work/internal-chat/_RESUME.md §1 · §2 (2026-10-29)"
  - "orchestration/work/internal-chat/research-mattermost-report.md §4 (붙일 자리)"
  - "cc-prototype procedure/ main dbf0b53 (읽기만 — back app/ · app lib/ · ios/Runner/)"
  - "cc-prototype 브랜치 kknaksss/internal-chat 0f0d969 (1판 코드 — r3 WP 대상 파일 줄 · 읽기만)"
  - "orchestration/work/internal-chat/sim-feedback.md (F1 ~ F4 — r3 · F5 · F6 · F7 · F9 — r4)"
  - "cc-prototype main a6c4123 (PR #17 머지 · 운영 · TestFlight 빌드 12) = 코드 워크트리 216b154 (r4 WP 대상 파일 줄 · 읽기만)"
  - "orchestration/work/internal-chat/_RESUME.md §5 (r3 WP 끝 · 배포 · infra #44 — r4 · r4 WP 끝 · PR #18 · infra #45 · 빌드 13 — r5)"
  - "cc-prototype main b988f21 (PR #18 머지 · 운영 · 빌드 13) · 코드 워크트리 kknaksss/internal-chat-invite 3ed1089 (= 8a6688b + F10 정렬 · 미배포 — r5 WP 대상 파일 줄 · 읽기만)"
  - "orchestration/work/internal-chat/sim-feedback.md (F10 · F11 · F13 · F14 — r5 · F12 안 함)"
  - "orchestration/work/internal-chat/r5-dispositions.md · review-code-r4.md (FAIL 0 · WARN 3 — 고치지 않고 마감) · cc-prototype main bf30db4 (PR #19 · infra #46 · 빌드 14 — r6 마감 · deploy.md)"
---

# 직원 앱 내부 채팅 — 빌드 계획

계약은 **SPEC-007 0.5.1**(전부 · 리뷰 r1 처분 · D9-38 ~ D9-44 — r2 · 동기 W2-1 ~ 6 · 코드 리뷰 r1 · D9-45 ~ D9-57 시뮬레이터 피드백 — r3 · 처분 동기 · D9-58 ~ D9-65 · 앱 안 전달 — r4 · 처분 동기(r4-dispositions · 코드 리뷰 r3 · F10) · D9-66 ~ D9-69 모아보기 · 초대 · 들어온 뒤 대화만 — r5 · 마감 동기 r5-dispositions — r6) — 이 문서는 빌드 계획만 적고 계약을 다시 쓰지 않는다. 결정 = DEC-009 · 화면 정본 = 확정 시안 r2(D9-35).

## Meta

- **진행 (r6 · 2026-10-30)**: **완료** = r5 WP 까지 운영 — 코드 main `bf30db4`(PR #17 · #18 · #19) · infra #44 · #45 · #46 · TestFlight 빌드 12 · 13 · 14(`deploy.md`) / **남음** = 사용자 실기기 SPEC-007 §13.3 C1 ~ C23 확인(WP-E2E3) · 코드 리뷰 r4 WARN 3(고치지 않고 마감 — SPEC-007 OQ-970 ~ OQ-972) / progress 96 = WP 25 중 24 완료(E2E3 남음)
- Covers spec: SPEC-007 0.5.1 (r6) · SPEC-004 0.4.2 는 고치지 않고 위에 얹는다(SPEC-007 §12 · SPEC-004 는 가리킴 줄 + r4 §6.5 통역 드로어 높이 한 줄 — D9-65) (r2 · r4)
- 코드 레포: `kknaksss/cc-prototype` — 범위 **`procedure/back/**` · `procedure/app/**`**. `procedure/front/**` 는 건드리지 않는다(웹 화면 없음 · D9-01 · `hooks.ts` 는 `board` 만 들어 그대로 — SPEC-007 §7)
- **infra (r5)**: **변경 없음** — 새 열 하나(`chat_member.from_message_id`)는 back 부팅 때 `MIGRATIONS` + 한 번 채우기로 생기고(같은 SQLite 파일 · PVC 그대로) · 모아보기는 기존 파일을 다시 열 뿐(볼륨 더 안 씀) · 새 env · Secret · 경로 · ingress 0. 배포는 back `imageTag` 값 PR 만(r4 #45 와 같은 꼴)
- **infra (r4)**: **변경 없음** — 전달은 파일을 복사하지 않고(볼륨 더 안 씀) 새 env · Secret · 경로 0 · `share_plus` 빼기는 앱 빌드만. r3 infra(D9-59 — ingress 100m · PVC 1Gi 그대로 + 주석)는 infra #44 `d9041ed` 로 배포 끝(`_RESUME` §5)
- **infra (r3 · D9-57)**: 1판은 변경 없음이었다 — 동영상(하나 최대 100MB · 보존 없음)이 같은 볼륨에 쌓이므로 **배포 전 코디가 infra 레포 PVC 크기를 확인 · 모자라면 infra PR**(WP-INFRA · WP-E2E 앞). 그 밖(새 env · Secret · 마운트 · 경로)은 여전히 0. 1판 설명: **infra 변경 없음** — 사진은 기존 `PROC_PHOTO_DIR`(배포 = PVC · compose = 이름 있는 볼륨 · SPEC-004 §2.3 · WORK-009 WP-INFRA) 하위 `chat/` 폴더를 back 이 만든다 · 새 env 0(한도 · 페이지 · 만료는 코드 상수) · 새 Secret 0 · 마운트 · 경로 그대로. 볼륨 크기만 열린 것(SPEC-007 OQ-931 — 코디가 infra 레포 PVC 정의를 보고 판단 · 바꾸면 그때 infra PR)
- base: 지금 main(`dbf0b53` 이후 운영본) · 워크트리 · 브랜치는 코디가 정한다(`new-work.sh cc-prototype internal-chat --workers backend,mobile`)
- 워커: backend · mobile · reviewer · 코디(E2E · 배포 · infra 확인)
- **r5 는 F10 정렬 커밋 위에 얹는다**: r4 WP(BE4 · APP6 · REVIEW3 · 수정 r4 · SIM2 · DEPLOY13)는 코드 `8a6688b` → main `b988f21`(PR #18) · infra #45 · TestFlight 빌드 13 으로 끝났다. 그 뒤 사용자 F10(정렬)은 코드 브랜치 `kknaksss/internal-chat-invite` `3ed1089`(미배포)로 고쳤다. r5 WP 는 이 브랜치 위 · 줄 번호 = `3ed1089` · SPEC-007 §12.4
- **r4 는 운영 코드 위에 얹는다**: r3 WP(BE3 · APP4 · APP5 · REVIEW2 · 수정 r2 · r3 · SIM · INFRA)는 코드 `edabe00` · `216b154` → main `a6c4123`(PR #17) 로 끝나 운영 · TestFlight 빌드 12 에 나갔다. r4 WP 의 줄 번호 = `216b154` · SPEC-007 §12.3
- **r3 는 1판 위에 얹는다**: 1판 WP(BE1 · BE2 · APP1 ~ APP3 · REVIEW r1 · 수정 r1)는 코드 `kknaksss/internal-chat` `0f0d969` 에 끝났다(pytest 500 · flutter test 186 · 코디 재확인 — `_RESUME` §5). r3 WP 의 줄 번호 = `0f0d969` · SPEC-007 §12.2 (r3)
- 검증은 WP 마다 그 범위만(`uv run pytest -q -k …` · `flutter analyze` · `flutter test`). **전체 검증(pytest 전부 · `flutter build ipa` · compose)은 WP-E2E 에서 한 번**
- **완료 = 사용자가 TestFlight 실기기(두 계정 · 두 기기 이상)에서 SPEC-007 §13.3 C1 ~ C23 을 본 것**(r5 — C21 모아보기 · C22 초대 · C23 들어온 뒤 대화만 더함 · C7 다시 초대 바뀜 · 빌드 13 에서 이미 본 것은 빌드 14 에서 회귀만)(r4 — C18 전달 · C19 통역 드로어 · C20 입력줄 · 키보드 더함 · 빌드 12 에서 이미 본 것은 빌드 13 에서 회귀만)(시뮬레이터 · 웹으로 대신하지 않는다 — 푸시 · 카메라는 실기기만)
- public — 실명 · 고객 정보 · 키 · 토큰 금지. E2E 대화는 가짜 문구(SPEC-007 OQ-902)

## 계약 고정점 (BE ∥ APP 병렬의 근거 — 이 표가 바뀌면 둘 다 멈춘다)

| 고정점 | 값 | SPEC-007 |
|---|---|---|
| 표 | `chat_room` · `chat_member` · `chat_message` · `chat_photo` · `push_log.kind = chat` · `push_log.chat_message_id` | §3 |
| 모양 | `Person` · `Member` · `Room`(보는 계정 기준) · `Preview` · `Message` · 시각 = KST 오프셋 · **밀리초**(`iso_ms`) · DB = UTC 밀리초(`to_db_ms`) (r2) | §3 · §6.1 |
| 셈 기준 | 안 읽음 = `id > last_read_message_id` · `since` = `updated_at >= since`(parse 뒤) · 앱이 `id` 로 겹침 지움 · 읽음 `{messageId}` (r2) | §5 · §6.2 |
| 핸들러 | SSE · 푸시 · 사진 경로 = `async def`(동기면 푸시 0) (r2) | §6.1 |
| API 14 | `GET people` · `GET rooms` · `POST rooms/direct` · `POST rooms` · `POST rooms/{id}/members` · `/leave` · `/hide` · `PUT /mute` · `GET` · `POST rooms/{id}/messages` · `DELETE messages/{id}` · `POST rooms/{id}/read` · `POST photos` · `GET photos/{id}` (prefix `/api/chat`) | §6.2 |
| 오류 코드 | §6.3 14개(`chat_peer_inactive` 더함) + 재사용 4 (r2) | §6.3 |
| 경로 수 | 51 + 14 = **65**(`test_route_count_65`) — r3 = 69(아래) | §6.4 |
| SSE | `chat_message` · `chat_message_deleted` · `chat_room` · `chat_room_removed` · `chat_read`(`lastReadMessageId` 더함) · `id:` 없음 · version 그대로 (r2) | §7 |
| 푸시 payload | `{aps:{alert:{title, body}, sound, "thread-id":"chat-<roomId>"}, kind:"chat", roomId, messageId}` · 만료 +1일 · 호출 0 | §8 |
| 사진 | `PROC_PHOTO_DIR/chat/` · JPEG ≤ 5MB · 앱 2048px · Bearer · `no-store` | §9 |
| 법적 검토 주석 | back ~~4곳~~ 5곳(r3 동영상 열기 더함) | §14 |
| **r3 표** | `chat_message.kind` 에 `video` · `edited_at` · `chat_photo` = 첨부(`kind` · `duration_ms` · `thumb_file_name`) · 이름은 그대로 · `MIGRATIONS` 4줄 | §3 |
| **r3 모양** | `Message.video{id, width, height, durationMs}` · `editedAt` · `Preview.kind` 에 `video` | §6.1 |
| **r3 API +4** | `PATCH messages/{id} {text}` · `POST videos`(multipart `roomId · video · thumb · width · height · durationMs`) · `GET videos/{id}`(`Range` → 206) · `GET videos/{id}/thumbnail` · 보내기 `{clientId, videoId}` → 경로 **69**(`test_route_count_69`) · 오류 코드 **20** | §6.2 · §6.3 · §6.4 |
| **r3 SSE** | `chat_message_edited {roomId, message}` · 멤버 전원 · `id:` 없음 | §7 |
| **r3 푸시** | 동영상 본문 「동영상」 · 수정 = 푸시 없음 · 여러 개 = 메시지마다 | §8 |
| **r3 한도** | 한 번에 10개 · 동영상 3분 · ~~100MB~~ **90MB**(D9-58 · r4 동기) · 썸네일 JPEG ≤ 5MB · 사진 5MB 그대로 · 동영상 올리기 300초 · `Content-Length` 필수 | §9.2 |
| **r4 API +1** | `POST messages/{id}/forward {targets:[{roomId\|accountId, clientId}]}` → `{results:[{ok, roomId, message\|error}]}`(대상 차례 · 일부 · 전부 실패 = 200) · 1 ~ 10 · 경로 **70**(`test_route_count_70`) · 오류 코드 **21**(`chat_not_forwardable`) | §5 「전달」 · §6.1 · §6.2 #19 · §6.3 · §6.4 |
| **r4 첨부** | 전달 = 대상마다 새 `chat_photo` 행 + **같은 파일** · 지우기 = 같은 `file_name` 안 지운 행 0 일 때만 파일 지움 · 인덱스 `chat_photo_file` | §3 r4 · §5 「삭제」 |
| **r4 SSE · 푸시** | 새 이벤트 · 새 푸시 종류 없음 — 만든 메시지마다 `chat_message` · 푸시(보내기와 같음) · 새 1:1 = `chat_room` | §7 · §8 |
| **r5 표** | `chat_member.from_message_id INTEGER NOT NULL DEFAULT 0`(보이는 경계 = 들어올 때 방 마지막 메시지 id) · `MIGRATIONS` 한 줄 · 열이 생기는 부팅에 한 번 채우기 | §3 r5 · §3.2 · §4.6 |
| **r5 API +1** | `GET /api/chat/rooms/{id}/attachments?before=&limit=`(1 ~ 60 · 기본 60) → `{items:[Message], hasMore}`(사진 · 동영상만 · 최근 것 위 · 커서 = 메시지 id) → 경로 **71**(`test_route_count_71`) · 오류 코드 **21 그대로** | §6.2 #20 · §6.4 |
| **r5 초대** | 1:1 [초대] = **지금 `POST /api/chat/rooms {accountIds:[상대, …]}` 그대로**(새 경로 없음) · #4 · #5 시스템 줄 = 「A님이 B님을 초대했습니다」(그룹 만들기도 한 줄) | §4.4 · §4.7 · §6.2 #4 · #5 |
| **r5 들어온 뒤 대화만** | 모든 읽기 길 `id > from_message_id`(목록 · `since` · 미리보기 null · 첨부 열기 404 · 전달 원본 404 · 고치기 · 지우기 404 · 모아보기) · SSE `chat_message_edited` · `chat_message_deleted` = 볼 수 있는 멤버만 · 새 이벤트 0 | §4.6 V1 ~ V12 · §7 |

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-BE1** | **표 · 방 · 메시지 API** — `CHAT_SCHEMA`(표 4 · 인덱스 · 법적 검토 주석 ①) · `MIGRATIONS` 한 줄 · `PUSH_LOG` 열 · repository 함수 · `service/chat.py`(상대 목록 · 1:1 재사용 · 그룹 · 추가 · 나가기 · 숨기기 · 알림 끄기 · 시스템 줄 · 보내기 · `clientId` · 삭제 · 안 읽음 · 읽음 · `before` · `since` · 방 이름 · 미리보기 · 주석 ②) · `api/chat.py`(사진 2 빼고 12 · **모두 `async def`**) · `schemas/chat.py` · `main.py` · `clock.py` `iso_ms` · `to_db_ms`(채팅 시각 밀리초) · `last_read_message_id` · 비활성 1:1 409 · 로그에 id 만 · **경로 65** (r2) | §2 ~ §6 · §14 | backend | `procedure/back/app/{domain/clock.py,repository/db.py,repository/repo.py,service/chat.py(새),api/chat.py(새),schemas/chat.py(새),main.py}` · `tests/test_chat*.py`(새) · `tests/test_order.py` (r2) | SPEC-007 §13.1 중 **BE1 줄만**: 「상대 목록」 · 「권한」(사진 올리기 · 열기 404 는 BE2) · 「1:1 재사용」 · 「그룹」 · 「추가 · 나가기」 · 「중복 방지」(메시지 1 · 200 · `clientId` 길이 — SSE · 푸시 줄은 BE2) · 「메시지」(사진 붙이기 줄은 BE2 — 사진 행을 시험 픽스처로 넣어도 됨) · 「삭제」(사진 줄은 BE2) · 「안 읽음」 · 「시각 경계」 · 「페이지」 · 「마이그레이션」 · 「경로 수」 · 「로그」(보내기) 통과 · 기존 시험 그 범위 회귀 없음 (r2 · R1:W-14) | `uv run ruff check . && uv run pytest -q -k "chat or route_count or migration or clock"` (r2) | **완료** — 1판 `0f0d969` → 운영 PR #17 `a6c4123` · 빌드 12 (r3 · r6) |
| **WP-BE2** | **SSE · 푸시 · 사진** — 커밋 뒤 SSE 5종(멤버마다 `send_to_account` · `container.py` 배선) · `push.py` 채팅 발송(받는 사람 · 제목 · 본문 100자 · `thread-id` · `notification` 안 씀 · 주석 ④) · `apns.py` 만료 인자(채팅만 +1일) · `push_log` · 사진 올리기 · 열기(`PROC_PHOTO_DIR/chat/` · JPEG · 5MB · Bearer · `no-store` · 로그 없음 · 주석 ③) · `photos.py` 전역 한도 주석 한 줄 · 붙기 전 사진 = 올린 사람만 · 파일 없음 404 · 폴더 없음 409 · `_send` 까지 `expiration` (r2) | §7 · §8 · §9 · §14 | backend | `procedure/back/app/{service/chat.py,service/push.py,push/apns.py,api/chat.py,api/photos.py,container.py}` · `tests/` | §13.1 「사진」 · 「푸시 대상」(**HTTP 경로 → 가짜 APNs 단언**) · 「푸시 내용」 · 「만료」 · 「SSE」 · 「중복 방지 — SSE · 푸시」 · 「삭제 — 사진」 · BE1 이 남긴 「권한」 사진 두 줄 · 「메시지」 사진 붙이기 줄 · 「로그」(푸시) 통과 (r2 · R1:W-14) · 원장 · 상담사 호출 · 띄우기 · 여권 사진 시험 회귀 없음 · `grep -rn "법적 검토 필요: 직원 채팅" procedure/back` = 4 | `uv run pytest -q -k "chat or push or apns or stream or photo or display"` | **완료** — 1판 `0f0d969` → 운영 PR #17 `a6c4123` · 빌드 12 (r3 · r6) |
| **WP-APP1** | **틀 · 상태 · 방 목록 · 새 대화** — `AppTab.chat`(설정 앞) · 탭 이름 · 아이콘 · `_root` · 탭바 · 레일 배지(`unreadRooms` · 시스템 줄 안 셈) · 채팅 탭 루트 = `TabScaffold` + 아래 [새 대화] 줄(D9-38) · `ui.dart` 작은 위젯(Input · Checkbox · Card · Progress · Banner — Toggle = `Switch.adaptive` · Chip = `StatusChip` · `MiniChip` 재사용) · `api.dart` 채팅 JSON 경로(`since` 는 `Uri` queryParameters) · SSE 파서 이름 5개 · `_onStreamEvent` → 채팅 상태(`lib/chat/`) · 방 목록(S1 · S2) · 새 대화(S3a ~ c) · 시각 글자 · 방 이름 · 미리보기 · 요청 차례를 단언하는 기존 `MockClient` 시험 기대 고침 (r2) | §6 · §7 · §10.0 ~ §10.3 · §12 A1 ~ A6 · A16 · A19 · A21 · A28 · A29 · A30 | mobile | `procedure/app/lib/{app_state.dart,screens/shell.dart,sse/board_stream.dart,api/api.dart,widgets/ui.dart,widgets/resv_ui.dart,screens/settings_screen.dart(_SwitchRow 공용화 시),chat/*(새),screens/chat_list_screen.dart(새),screens/chat_new_screen.dart(새)}` · `test/`(기존 `MockClient` 시험 포함) (r2 · R1:W-15) | 시뮬레이터(폰 · 패드)에서 가짜 응답 또는 WP-BE1 뒤 로컬 back 으로 S1 · S2 · S3a ~ c 스크린샷 · 5탭 · 배지 | `cd procedure/app && flutter analyze && flutter test` | **완료** — 1판 `0f0d969` → 운영 PR #17 `a6c4123` · 빌드 12 (r3 · r6) |
| **WP-APP2** | **대화 · 사진 · 삭제** — 대화(S4 · S5 · 이름 묶기 · 시스템 줄 · 날짜 구분선) · 폰 대화 머리 `DetailHeader` 「‹ 채팅」(D9-38) · 입력 한도 코드 포인트 2000 · 비활성 1:1 입력 막음(D9-42) · 보내는 중 · 실패 · 다시 보내기(같은 `clientId` · S6 · 12초 · 4xx 토스트) · `before` 위로 · `since` 겹침 `id` 로 지움 · 읽음(`messageId` · 보고 있는 방만 — D9-40) · 사진 시트 · `image_picker`(2048) + **늘 JPEG 다시 인코딩**(`flutter_image_compress` · 85 · 임시 파일 지움) · 올리는 중 %(S7a · S7b · 진행률 나오는 스트림 요청 · 40초) · (r2) 크게 보기(S8) · 사진 메모리 LRU · `Image.memory` · 길게 눌러 삭제 · 확인(S9a · S9b) · `pubspec.yaml` · `Info.plist` 문구 2 | §5 · §9 · §10.4 ~ §10.7 · §12 A14 · A15 · A17 · A22 · A27 | mobile | `procedure/app/{lib/screens/chat_room_screen.dart(새),lib/screens/chat_photo_screen.dart(새),lib/chat/*,lib/api/api.dart,lib/widgets/header.dart,pubspec.yaml,ios/Runner/Info.plist}` · `test/` (r2 · R1:W-15) | 시뮬레이터 S4 ~ S9b 스크린샷 · 앨범 사진 1회 · **PNG 스크린샷 1회**(JPEG 로 나감) 보내기(시뮬레이터 사진첩) · 실기기에서 카메라 · HEIC 사진이 JPEG 로 나오는지 1회(OQ-924 · 코디가 기기 연결 허락 뒤) (r2) | `flutter analyze && flutter test` | **완료** — 1판 `0f0d969` → 운영 PR #17 `a6c4123` · 빌드 12 (r3 · r6) |
| **WP-APP3** | **방 정보 · 아이패드 · 푸시 · 배너 · 생명주기** — 방 정보(S10a ~ c · Toggle) · 참여자 추가(S10d) · 나가기(S10e) · 숨기기 · 아이패드 두 칸 · 오른쪽 시트(S13a ~ d) · `PushKind.chat` · `_onTap` → 채팅 탭 그 방 · `onForeground` · `AppDelegate.swift` `willPresent`(채팅 = 시스템 배너 없이 Dart 로) · 넘기는 키에 `roomId` · `messageId` · 앱 안 배너(S11 · **셸 안 층** · 소리 없음(D9-39) · 보는 방(D9-40 — 다른 탭이면 뜸) · 알림 끈 방 · **띄우기 화면 열린 수**(`showQrScreen` · `showPassportScan` — 어느 길이든 · D9-44) · 겹침 `messageId`) · 아이패드 헤더 = `AppHeader` + 목록 칸 위 [새 대화] · 대화 칸 뒤로 없음(D9-38) · 앞으로 올 때 · `_onStreamChange` 다시 연결 때 `since` 메우기(실패 조용히) · 로그아웃 · 계정 바뀜 때 비움 (r2) | §8 · §10.8 ~ §10.12 · §11 · §12 A7 ~ A13 · A18 · A23 ~ A26 · A31 | mobile | `procedure/app/{lib/screens/chat_info_screen.dart(새),lib/screens/chat_list_screen.dart,lib/push/push.dart,lib/app_state.dart,lib/screens/shell.dart,lib/screens/qr_show_screen.dart,lib/screens/scan_screen.dart,lib/screens/launchers.dart(확인만),lib/main.dart(확인만 — 배너를 두지 않음),lib/widgets/header.dart,lib/chat/*,ios/Runner/AppDelegate.swift}` · `test/` (r2 · R1:W-15) | 시뮬레이터 S10a ~ e · S11 · S13a ~ d 스크린샷 · `push_test` 채팅 · 옛 3종 회귀 · 배너 거름 시험(**예약 상세에서 연 QR 중 · 여권 스캔 중 · 대기열 QR 중** 배너 없음 · 다른 탭 = 뜸) (r2) | `flutter analyze && flutter test` | **완료** — 1판 `0f0d969` → 운영 PR #17 `a6c4123` · 빌드 12 (r3 · r6) |
| **WP-REVIEW** | reviewer: SPEC-007 §2 ~ §14 ↔ 코드 · 부록 A · B · 경로 65 · 채팅 핸들러 `async def`(`grep -n "^def " procedure/back/app/api/chat.py` = 0) · 채팅 시각 밀리초 · `since >=` · 안 읽음 id 기준 · 배너 층(셸 안 · `main.dart` 아님) · 멤버 아닌 404 · 붙기 전 사진 · `clientId` · (r2) 푸시 대상 · 만료(호출 0 회귀) · `notification` 0 · SSE 받는 연결 · 사진 Bearer · 사진첩 저장 0 · 디스크 캐시 0 · 주석 4곳 · 실명 · 키 grep. FAIL 은 모아서 한 번에 수정 발주 | 전체 | reviewer | 코드 전체 | PASS | — | **완료** — 코드 리뷰 r1 FAIL 1 · WARN 1 → 수정 r1 로 닫힘(`review-code-r1.md`) (r3) |
| **WP-BE3** (r3) | **수정 · 동영상(back)** — 표 열 4 · `MIGRATIONS` 4줄 · 스키마(`video` · `editedAt` · `videoId` · `EditRequest`) · `service/chat.py` `edit()`(내 글만 · 같은 글 · SSE `chat_message_edited` · 푸시 안 부름) · `post` 동영상 갈래 · `delete` 동영상 두 파일 · `upload_video`(multipart · 전역 spool 그대로 → 임시 파일 조각 복사 · `ftyp` · JPEG 썸네일 · 100MB · 180000ms) · 열기 2(`FileResponse` `Range` 206 · 권한 = 사진과 같음 · 종류 다르면 404) · `push.py` `chat_body` 「동영상」 · 경로 69 · 오류 코드 6 · 주석 ⑤ | SPEC-007 §3 · §5 · §6 · §7 · §8 · §9.2 · §12.2 R-B1 ~ R-B18 · §14 | backend | `procedure/back/app/{repository/db.py,repository/repo.py(확인만 · 필요하면),schemas/chat.py,service/chat.py,api/chat.py,api/photos.py(주석 한 줄),service/push.py}` · `tests/test_chat*.py` · `tests/test_order.py` | SPEC-007 §13.1 r3 줄 전부(「경로 수 69」 · 「들어올 때 읽음」 · 「빈 방 읽음」 · 「1판 값」 · 「수정」 · 「동영상 올리기」 · 「동영상 보내기 · 열기」(`Range` 206 · 416) · 「동영상 지우기 · 푸시 · 미리보기」 · 「법적 검토 주석」 = 5) 통과 · 1판 채팅 · 신분증 사진 · 호출 푸시 시험 회귀 없음 · 라우트 핸들러 `def` 0(`grep -n -A1 "@router\." procedure/back/app/api/chat.py \| grep -c "^[0-9]*-def "` = 0) | `uv run ruff check . && uv run pytest -q -k "chat or route_count or migration or push or photo"` | **완료** — 2판 `edabe00` → 운영 PR #17 `a6c4123` · 빌드 12 (r4 · r6) |
| **WP-APP4** (r3) | **입력창 · [+] 시트 · 여러 개 · 변환 · 동영상 말풍선 · 재생(app)** — 넓은 입력창(2 ~ 6줄 · [+] · [전송]) · [+] 바텀 시트(최근 줄 · 카메라 칸 · 동그라미 차례 번호 · 10개 · [전송] · 「사진」 메뉴 = `pickMultipleMedia(limit: 10)`) · 사진 보관함 권한(limited · 거부 줄) · 여러 개 하나씩 차례로 · 「N개 보내는 중」 · 사진 = 1판 JPEG 길 · 동영상 = 길이 검사(3분) → 변환(H.264 MP4 1280) → 썸네일 → 100MB 검사 → `POST videos`(진행률 · 300초) → 보내기 · 실패 토스트 · 변환 임시 파일 지우기 · 동영상 말풍선(썸네일 · ▶ · 길이) · 재생 화면(Bearer · 끊어 받기 · 저장 없음) · `MsgKind.video` · 미리보기 · 배너 「동영상」 · `Info.plist` 문구 · 패키지(§9.3 권장 — 바꾸면 코디에게) | SPEC-007 §9 · §10.4 · §10.5 · §10.6 · §12.2 R-A1 ~ R-A3 · R-A7 ~ R-A12 · R-A15 · R-A17 ~ R-A20 | mobile | `procedure/app/{lib/chat/chat_model.dart,lib/chat/chat_state.dart,lib/chat/chat_view.dart,lib/chat/chat_ui.dart,lib/chat/photo_pick.dart,lib/chat/video_pick.dart(새),lib/screens/chat_room_screen.dart,lib/screens/chat_photo_screen.dart,lib/screens/chat_attach_sheet.dart(새),lib/screens/chat_video_screen.dart(새),lib/api/api.dart,pubspec.yaml,ios/Runner/Info.plist}` · `test/chat_*` | SPEC-007 §13.2 r3 줄 중 입력창 · [+] 시트 · 여러 개 · 동영상 말풍선 · 재생 · 미리보기 · 배너 통과 · 시뮬레이터(사진첩에 넣은 MOV · HEIC · PNG)로 입력창 · [+] 시트 · 보내는 중 N개 · 동영상 말풍선 · 재생 스크린샷 · **실기기 1회(코디가 기기 연결 허락 뒤)**: HEVC 4K · 슬로모 · 세로 영상이 H.264 MP4 로 나오는지(OQ-950) — 안 되면 네이티브 채널로 바꾸고 코디에게 알림 | `cd procedure/app && flutter analyze && flutter test test/chat_app*_test.dart` | **완료** — 2판 `edabe00` → 운영 PR #17 `a6c4123` · 빌드 12 (r4 · r6) |
| **WP-APP5** (r3) | **길게 누르기 5메뉴 · 복사 · 선택 복사 · 공유 · 수정 · 링크(app)** — 메뉴 표(§10.7 · 남의 것 · 사진 · 동영상 포함 · 시스템 · 지움 · 보내는 중 = 없음) · 복사(클립보드 · 토스트) · 선택 복사 시트(`SelectableText`) · 공유(`share_plus` · `excludedCupertinoActivities: [saveToCameraRoll]` · 사진 · 동영상 임시 파일 · 시트 닫히면 지움 · 아이패드 팝오버) · 수정 모드(원문 · [저장] · [✕] · `PATCH` · SSE `chat_message_edited` 반영 · 「수정됨」 · `since` 원천 = 서버 값만) · 링크(정규식 · 밑줄 · `url_launcher` externalApplication) · SSE 파서 이름 더함 | SPEC-007 §5 · §7 · §10.4 · §10.7 · §12.2 R-A4 ~ R-A6 · R-A13 · R-A14 · R-A16 · R-A18 · R-A22 | mobile | `procedure/app/{lib/screens/chat_room_screen.dart,lib/chat/chat_state.dart,lib/chat/chat_model.dart,lib/sse/board_stream.dart,lib/api/api.dart,lib/chat/chat_view.dart(링크 찾기),pubspec.yaml}` · `test/chat_*` | SPEC-007 §13.2 r3 줄 중 메뉴 · 복사 · 공유 인자 · 수정 · 「수정됨」 · `since` 원천(삭제 · 수정 뒤) · 링크 · SSE 파서 통과 · 시뮬레이터 스크린샷(메뉴 3가지 · 선택 복사 · 수정 모드 · 「수정됨」 · 링크 · 공유 시트에 「이미지 저장」 없음) | `flutter analyze && flutter test test/chat_app*_test.dart test/sse*` | **완료** — 2판 `edabe00` → 운영 PR #17 `a6c4123` · 빌드 12 (r4 · r6) |
| **WP-REVIEW2** (r3) | reviewer: SPEC-007 0.3.0 §3 · §5 · §6.2 #10 · #11 · #15 ~ #18 · §7 · §8 · §9.2 · §10.4 ~ §10.7 · §12.2 ↔ 코드 · 부록 A(D-45 ~ D-57) · 부록 C(F1 ~ F4) · 경로 69 · 라우트 `def` 0 · 수정 = 푸시 0 · 안 읽음 그대로 · `Range` 206 · 동영상 권한(붙기 전 · 나간 사람 · 종류 다름 404) · 전역 spool 그대로 · 임시 파일 남지 않음 · 공유 저장 뺌 · 디스크 · 사진첩 저장 0(공유 · 변환 임시 파일만 · 지워짐) · `since` 원천 = 서버 값 · 주석 5 · 실명 · 키 grep. FAIL 은 모아서 한 번에 수정 발주 | 전체 r3 | reviewer | 코드 r3 변경 | PASS | — | **완료** — 리뷰 r2 FAIL 0 · WARN 7 → 수정 r2(처분 `app-fix-r2-instructions.md`) (r4) |
| **WP-SIM** (r3) | 코디: 백엔드 커밋 뒤 로컬 compose 재기동(옛 코드 금지) → 시뮬레이터 2대(폰 · 패드 · 계정 둘)에 debug 빌드 → 사용자가 F1 ~ F4 를 본다 · 피드백은 모아서 한 번에 | §13.2 r3 스크린샷 · 부록 C | 코디 · 사용자 | — | 사용자 「됐다」 | — | **완료** — 사용자 F5 · F6 → D9-60 · D9-61 → 수정 r3 `216b154` (r4) |
| **WP-INFRA** (r3 · D9-57) | 코디: **OQ-931 닫기** — infra 레포의 procedure PVC 정의(크기 · 지금 쓴 양)를 보고 동영상(하나 ≤ 100MB · 보존 없음)이 쌓여도 되는지 판단 → 모자라면 **infra PR**(크기 올림 · 배포 전 머지) · 결과를 `_RESUME` · SPEC-007 OQ-931 에 한 줄 | §9.2 「볼륨」 · OQ-931 | 코디 | infra 레포(코디가 정함) | 판단 기록 · 필요하면 infra PR 머지 | — | **완료** — D9-59(ingress 100m · PVC 1Gi 그대로 + 주석) · infra #44 `d9041ed` 배포 · OQ-931 닫힘 (r4) |
| **WP-E2E** | 코디: **① OQ-931 = WP-INFRA 결과 확인(r3 · 닫혀 있어야 배포)** (r2 · R1:W-16 · D9-57) → 전체 검증 · compose 재기동(백엔드 커밋 뒤 · 옛 코드로 E2E 금지) → 로컬 시뮬레이터 두 대로 C2 · C4 · C6 흐름만 미리 → **배포**(코드 PR 머지 · 이미지 · infra `image.tag` — `deploy.md` 순서 · TestFlight 다음 빌드) → **사용자 실기기 E2E SPEC-007 §13.3 C1 ~ C17**(r3 — C5 · C8 은 r3 화면으로 · C13 ~ C17 더함) · 피드백은 모아서 한 번에 | §13.3 | 코디 · 사용자 · (수정) 각 워커 | — | C1 ~ C17 사용자 확인 (r3) | `uv run pytest -q` · `flutter analyze && flutter test && flutter build ipa --release --dart-define=API_BASE=https://ccc.medisolveai.xyz --build-number=<+1>` | **완료**(배포 — 코드 PR #17 `a6c4123` · infra #44 · TestFlight 빌드 12) · 실기기 피드백 F7 · F9 = r4 · 남은 확인은 WP-E2E3 로 (r4 · r6) |
| **WP-BE4** (r4) | **전달 API(back)** — `CHAT_SCHEMA` 인덱스 `chat_photo_file` 1줄 · repo `chat_photo_live_refs` · `post` · `open_direct` 의 안쪽을 꺼내 같이 씀(동작 그대로) · 새 `forward()`(원본 권한 · `chat_not_forwardable` · 대상별 검사 · 같은 방 하나로 · 대상마다 `clientId` · 첨부 새 행 + 같은 파일 · 한 트랜잭션 · 커밋 뒤 메시지마다 SSE · 푸시 · 로그 id 만) · `delete` 파일 지우기 = 마지막 참조일 때만 · 스키마 `ForwardTarget` · `ForwardRequest` · `ForwardResponse` · 라우트 `POST /messages/{message_id}/forward`(`async def`) · 경로 70 · 오류 코드 21 | SPEC-007 §3 r4 · §5 「전달」 · 「삭제」 · §6.1 · §6.2 #19 · §6.3 · §6.4 · §7 · §8 · §12.3 R4-B1 ~ R4-B11 | backend | `procedure/back/app/{repository/db.py,repository/repo.py,schemas/chat.py,service/chat.py,api/chat.py}` · `tests/test_chat*.py`(새 `test_chat_r4.py` 가능) · `tests/test_order.py` | SPEC-007 §13.1 r4 4줄(「전달 — 권한 · 모양」 · 「대상별」 · 「다시 보내기 · SSE · 푸시 · 읽음」(**HTTP 경로 → 가짜 APNs**) · 「첨부 · 지우기」(원본 지워도 전달본 열림 · 마지막 참조에 파일 지움)) · 「경로 수 70」 통과 · 1판 · r3 채팅 · 신분증 사진 · 호출 푸시 시험 회귀 없음 · 라우트 핸들러 `def` 0 · 법적 검토 주석 = 5 그대로 | `uv run ruff check . && uv run pytest -q -k "chat or route_count or migration or push or photo"` | **완료** — `8a6688b`(+ 수정 r4 · 잠금 W3-2 · pytest 522) → 운영 PR #18 `b988f21` · 빌드 13 (r5 · r6) |
| **WP-APP6** (r4) | **전달 시트 · [공유] 교체 · 시스템 공유 걷어냄 · 통역 드로어(app)** — `ChatMenu.share` → 전달 시트(§10.14 — 폰 바텀 시트 · 패드 가운데 · 검색 · **초성**(새 함수 · 전달 시트만) · [전체][사람] · 칩 줄 · 「대화방」(내 방 − 비활성 상대 1:1) + 「직원」(`chatPeople`) · 동그라미 10 · [전송] · 대상마다 `clientId` · 결과 토스트 · 네트워크 실패 = 시트 남김 · 같은 `clientId` 다시) · `chatForward` · 모델 `ForwardTarget` · `ForwardResult` · `ChatState.forward`(응답 `Message` 를 방 메모리에 · `id` 겹침 지움) · **걷어냄**: `chat_share.dart` 의 공유 부분(링크 열기만 남김) · `_share` · `_shareVideo` · `chatVideoDownload` · `pubspec.yaml` `share_plus`(lock · Pods 같이) · 공유 시험 → 전달 시험 · **통역 드로어**(`interpret_drawer.dart` 높이 = 놓인 칸 × 0.92 · 상태 표시줄 아래 · 손잡이 끌어 내려 닫기 · 아이패드) | SPEC-007 §10.7 · §10.11 · §10.12 · §10.14 · §10.15 · §12.3 R4-A1 ~ R4-A12 · SPEC-004 §6.5 | mobile | `procedure/app/{lib/chat/chat_share.dart,lib/chat/chat_model.dart,lib/chat/chat_state.dart,lib/chat/chat_search.dart(새 · 이름은 워커),lib/screens/chat_forward_sheet.dart(새),lib/screens/chat_room_screen.dart,lib/api/api.dart,lib/widgets/interpret_drawer.dart,lib/screens/room_screen.dart(확인만),pubspec.yaml,pubspec.lock,ios/Podfile.lock}` · `test/chat_app5_test.dart` · `test/`(새 전달 · 드로어 시험) | SPEC-007 §13.2 r4 줄(전달 시트 · 초성 · 결과 토스트 · `share_plus` · `chatVideoDownload` grep 0 · 통역 드로어) 통과 · 시뮬레이터(가짜 응답 또는 WP-BE4 뒤 로컬 back)로 §13.2 r4 스크린샷 · 기존 통역 시험 회귀 없음 | `cd procedure/app && flutter analyze && flutter test test/chat_app*_test.dart test/interpret_client_test.dart <새 드로어 시험>` · `grep -rn "share_plus\|SharePlus\|chatVideoDownload" lib pubspec.yaml` = 0 | **완료** — `8a6688b`(+ 수정 r4 · 공용 시트 · 보내는 중 · flutter test 235) → 운영 PR #18 `b988f21` · 빌드 13 (r5 · r6) |
| **WP-REVIEW3** (r4) | reviewer: SPEC-007 0.4.0 §3 r4 · §5 「전달」 · 「삭제」 · §6.2 #19 · §6.3 · §6.4 · §10.14 · §10.15 · §12.3 ↔ 코드 · 부록 A(D-58 ~ D-65) · 부록 C(F5 ~ F9) · 부록 D · 양쪽 대조(요청 · 결과 모양 · 대상 차례 · `clientId` · 오류 코드) · 원본 지워도 전달본 열림 · 마지막 참조에 파일 지움 · 같은 방 두 번 = 1개 · 비활성 1:1 대상 = 그것만 실패 · 경로 70 · 라우트 `def` 0 · 시스템 공유 코드 · 패키지 0 · 통역 드로어(폰 · 패드 · 통역 시험 회귀) · 실명 · 키 grep. FAIL 은 모아서 한 번에 수정 발주 | 전체 r4 | reviewer | 코드 r4 변경 | PASS | — | **완료** — 리뷰 r3 FAIL 0 · WARN 3 → 수정 r4(`app-fix-r4` · `be-fix-r4`) (r5) |
| **WP-SIM2** (r4) | 코디: 백엔드 커밋 뒤 로컬 compose 재기동(옛 코드 금지) → 시뮬레이터 2대(폰 · 패드 · 계정 둘) debug 빌드 → 사용자가 전달 · 통역 드로어를 본다 · 피드백은 모아서 한 번에 | §13.2 r4 스크린샷 | 코디 · 사용자 | — | 사용자 「됐다」 | — | **완료**(시뮬레이터 재설치 · `_RESUME` §5) (r5) |
| **WP-DEPLOY13** (r4) | 코디: 전체 검증 한 번(`uv run pytest -q` · `flutter analyze && flutter test`) → 코드 PR 머지 → back 이미지 → infra `back.imageTag` PR(값만 — 새 infra 변경 없음) → sync · `/api/health` → **TestFlight 빌드 13**(`flutter build ipa --release --dart-define=API_BASE=https://ccc.medisolveai.xyz --build-number=13` · `deploy.md` 순서) | — | 코디 | — | 운영 back = r4 · 빌드 13 처리 끝 | `uv run pytest -q` · `flutter analyze && flutter test && flutter build ipa …` | **완료** — PR #18 `b988f21` · infra #45 `f67ac5d` · sync · 빌드 13 업로드 (r5) |
| **WP-E2E2** (r4) | 사용자 실기기 E2E — **SPEC-007 §13.3 C18 · C19 · C20**(새) + 빌드 12 에서 남은 C1 ~ C17 · 회귀 C12 · 피드백은 모아서 한 번에 | §13.3 | 코디 · 사용자 | — | C1 ~ C20 사용자 확인 | — | **완료**(배포 빌드 13 · 실기기 피드백 F10 · F11 · F13 · F14 = r5 · F12 안 함) · 남은 확인은 WP-E2E3 로 (r5 · r6) |
| **WP-BE5** (r5) | **들어온 뒤 대화만 · 모아보기 API · 초대 문구(back)** — `chat_member.from_message_id` 열 · `MIGRATIONS` 한 줄 · `_backfill_chat_from`(열이 새로 생길 때만) · `_join` 이 경계를 씀 · **읽기 길 전부**(§4.6 V1 ~ V12 · §12.4 R5-B1 ~ B15 — 목록 · `since` · 미리보기 · 첨부 열기 · 전달 원본 · 고치기 · 지우기 · SSE 수정 · 삭제 받는 사람) · 새 `chat_attachments` · `attachments()` · 라우트 `GET /rooms/{room_id}/attachments`(`async def` · `MessageList`) · 시스템 줄 「…님을 초대했습니다」 · `create_group` 초대 줄 + SSE · 경로 71 · 옛 시험 기대 고침(R5-B17 — `test_chat.py:136-137` 「옛 메시지 보임」 등 grep 으로 전부) | SPEC-007 §3 r5 · §3.2 · §4.2 · §4.4 · §4.5 · §4.6 · §4.7 · §5 · §6.2 #4 · #5 · #9 · #11 · #14 · #15 · #17 · #19 · #20 · §6.4 · §7 · §12.4 R5-B1 ~ B17 | backend | `procedure/back/app/{repository/db.py,repository/repo.py,service/chat.py,api/chat.py,schemas/chat.py(재사용 확인)}` · `tests/test_chat*.py`(새 `test_chat_r5.py` 가능) · `tests/test_order.py` | SPEC-007 §13.1 r5 줄 전부(「들어온 뒤 대화만」 5줄 · 「안 읽음 불변식」 · 「초대 문구 · 그룹 만들기 줄」 · 「모아보기 #20」 · 「경로 수 71」) + 「추가 · 나가기」 바뀐 줄 통과 · 1판 ~ r4 채팅 · 신분증 사진 · 호출 푸시 시험 회귀 없음 · 라우트 핸들러 `def` 0 · 법적 검토 주석 = 5 그대로 · **§12.4 G1 ~ G3 다시 grep 해서 줄마다 처리 · 안 바꿈을 보고에 표로** | `uv run ruff check . && uv run pytest -q -k "chat or route_count or migration"` | **완료** — pytest 532 · 경로 71 · R5D:FAIL-1(푸시 · SSE 경계) · W-1 → 운영 PR #19 `bf30db4` · 빌드 14 (r6) |
| **WP-APP7** (r5) | **모아보기 · 초대 · 들어온 뒤(app)** — 방 정보 「사진 · 동영상」 줄 · 새 모아보기 화면(§10.16 — 3열 · 최근 위 · 60씩 · 사진 · 동영상 칸 · 빈 상태 · 실패 · 누르면 크게 보기 · 재생 · SSE 반영 · 아이패드 = 방 정보 시트 안 · 로그아웃 때 비움) · `chatAttachments` · [+ 참여자 추가] → [+ 초대] · 머리 「초대」 · **1:1 [+ 초대] → `createGroup([상대, …])` → 새 그룹으로**(비활성 상대 = 숨김) · 1:1 안내 줄 지움 · 나가기 대화상자 새 문구 · 픽스처 `/attachments` · 옛 글자 시험 고침 | SPEC-007 §10.0 r5 · §10.8 · §10.9 · §10.10 · §10.11 · §10.16 · §10.17 · §11 · §12.4 R5-A1 ~ A10 | mobile | `procedure/app/{lib/screens/chat_info_screen.dart,lib/screens/chat_new_screen.dart,lib/screens/chat_media_screen.dart(새 · 이름은 워커),lib/screens/chat_list_screen.dart(확인만),lib/chat/chat_state.dart,lib/chat/chat_model.dart(확인만),lib/api/api.dart}` · `test/chat_fixture.dart` · `test/chat_app2_test.dart` · `chat_app3_test.dart` · `chat_app6_test.dart` · `test/`(새 r5 시험) | SPEC-007 §13.2 r5 줄 통과 · 시뮬레이터(가짜 응답 또는 WP-BE5 뒤 로컬 back)로 §13.2 r5 스크린샷 · `grep -rn "참여자 추가\|그룹을 만들어요\|다시 초대받으면" lib` = 0(주석 포함 · 「초대」로) | `cd procedure/app && flutter analyze && flutter test test/chat_app*_test.dart <새 r5 시험>` | **완료** — flutter test 248 · R5D:W-2 ~ W-4 → 운영 PR #19 `bf30db4` · 빌드 14 (r6) |
| **WP-REVIEW4** (r5) | reviewer: SPEC-007 0.5.0 §3 r5 · §4.4 · §4.6(**V1 ~ V12 를 코드에서 다시 전수 — 빠진 읽기 길 0**) · §4.7 · §6.2 #4 · #5 · #20 · §6.4 · §7 · §10.8 ~ §10.10 · §10.16 · §10.17 · §12.4 ↔ 코드 · 부록 A(D-66 ~ D-69) · 부록 C(F10 ~ F14) · 부록 D.4 ~ D.7 · 같은 밀리초 경계 · 다시 초대 · 내 옛 메시지 404 · SSE 수정 · 삭제 받는 사람 · 옛 DB 채우기(두 번 부팅) · 경로 71 · 라우트 `def` 0 · 1:1 [초대]가 새 경로 없이 #4 · 실명 · 키 grep. FAIL 은 모아서 한 번에 수정 발주 | 전체 r5 | reviewer | 코드 r5 변경 | PASS | — | **완료** — 코드 리뷰 r4 FAIL 0 · WARN 3(`review-code-r4.md`) · **WARN 3 = 남음**(고치지 않고 마감 — SPEC-007 OQ-970 ~ OQ-972) (r6) |
| **WP-SIM3** (r5) | 코디: 백엔드 커밋 뒤 로컬 compose 재기동(옛 코드 금지 · **옛 DB 볼륨 그대로 띄워 채우기 1회 확인**) → 시뮬레이터 2대(폰 · 패드 · 계정 둘 이상) debug 빌드 → 사용자가 모아보기 · 초대 · 다시 초대를 본다 · 피드백은 모아서 한 번에 | §13.2 r5 스크린샷 | 코디 · 사용자 | — | 사용자 「됐다」 | — | **완료로 넘김** — 시뮬레이터 확인 기록은 `_RESUME` §5 에 없음 · 배포 PR #19 로 넘어감(코디 확인) (r6) |
| **WP-DEPLOY14** (r5) | 코디: 전체 검증 한 번(`uv run pytest -q` · `flutter analyze && flutter test`) → 코드 PR 머지(`kknaksss/internal-chat-invite` — F10 `3ed1089` 포함) → back 이미지 → infra `back.imageTag` PR(값만) → sync · `/api/health` → **TestFlight 빌드 14**(`flutter build ipa --release --dart-define=API_BASE=https://ccc.medisolveai.xyz --build-number=14` · `deploy.md` 순서) | — | 코디 | — | 운영 back = r5 · 빌드 14 처리 끝 | `uv run pytest -q` · `flutter analyze && flutter test && flutter build ipa …` | **완료** — PR #19 `bf30db4` · infra #46 `15a1b39` · 배포 전 운영 DB 사본 · 빌드 14 업로드(`deploy.md`) (r6) |
| **WP-E2E3** (r5) | 사용자 실기기 E2E — **SPEC-007 §13.3 C21 · C22 · C23**(새) · C7(바뀜) + 빌드 13 에서 남은 C1 ~ C20 · 회귀 C12 · 피드백은 모아서 한 번에 | §13.3 | 코디 · 사용자 | — | C1 ~ C23 사용자 확인 | — | **남음** — 사용자 실기기 SPEC-007 §13.3 C1 ~ C23(빌드 14) 확인 (r6) |

## 병렬

```text
(1판 · 끝) WP-BE1 ── WP-BE2 ─┐
           WP-APP1 ── WP-APP2 ── WP-APP3 ─┴─ WP-REVIEW(r1 · 수정 r1) ── 시뮬레이터(사용자 피드백 F1 ~ F4)

(r3)  WP-BE3 ────────────────────────┐
      WP-APP4(가짜 응답) ── WP-APP5 ──┴── WP-REVIEW2 ── WP-SIM(사용자) ── WP-E2E(배포 → 실기기 C1 ~ C17)
                                                     WP-INFRA(PVC · D9-57) ──┘ (WP-E2E 앞에 닫힘)
      (r3 · 끝 — 운영 a6c4123 · 빌드 12 · 실기기 피드백 F7 · F9)

(r4)  WP-BE4(전달 API) ─────────────────────────┐
      WP-APP6(전달 시트 · 공유 걷어냄 · 드로어) ──┴── WP-REVIEW3 ── WP-SIM2(사용자) ── WP-DEPLOY13(빌드 13) ── WP-E2E2(실기기 C1 ~ C20)
      (r4 · 끝 — 운영 b988f21 · 빌드 13 · 실기기 피드백 F10 → 3ed1089 · F11 · F13 · F14)

(r5)  WP-BE5(경계 · 모아보기 API · 초대 줄) ───────────┐
      WP-APP7(모아보기 화면 · 초대 · 1:1 → 새 그룹) ──┴── WP-REVIEW4 ── WP-SIM3(사용자) ── WP-DEPLOY14(빌드 14) ── WP-E2E3(실기기 C1 ~ C23)
      (r5 · 끝 — 운영 bf30db4 · PR #19 · infra #46 · 빌드 14 · 남음 = 실기기 C1 ~ C23 · 리뷰 r4 WARN 3 → OQ-970 ~ 972 — r6)
```

- **BE5 ∥ APP7 병렬 허용 (r5)** — 계약(모아보기 요청 · 응답 = `Message` 그대로 · 1:1 [초대] = 기존 #4 · 시스템 줄 문구 · 경계로 바뀌는 응답(빈 `lastMessage` · 404))이 SPEC-007 §4.4 · §4.6 · §4.7 · §6.2 #20 에 다 있다(위 「계약 고정점」 r5 줄). 앱은 가짜 응답으로 먼저 짓고 BE5 뒤 로컬 back 에 붙인다. 들어온 뒤 대화만은 거의 back 몫 — 앱은 나간 방 메모리를 지우는 지금 동작(§12.4 R5-A8)을 시험으로 지킨다
- **BE4 ∥ APP6 병렬 허용 (r4)** — 전달 계약(요청 · 결과 모양 · 대상 차례 · `clientId` · 오류 코드 · 첨부 규칙)이 SPEC-007 §5 「전달」 · §6.1 · §6.2 #19 에 다 있다(위 「계약 고정점」 r4 줄). 앱은 가짜 응답으로 먼저 짓고 BE4 뒤 로컬 back 에 붙인다. 통역 드로어는 back 과 무관 — APP6 안에서 먼저 해도 된다

- **BE3 ∥ APP4 병렬 허용** — r3 계약(수정 · 동영상 API · `Message.video` · `editedAt` · SSE `chat_message_edited` · 오류 코드 · 한도)이 SPEC-007 §6 · §7 · §9.2 에 다 있다(위 「계약 고정점」 r3 줄). 앱은 가짜 응답으로 먼저 짓고 BE3 뒤 로컬 back 에 붙인다
- APP4 → APP5 는 같은 mobile 워커(`chat_room_screen.dart` · `chat_state.dart` · `chat_model.dart` 가 겹친다) (r3)
- 1판 설명: BE ∥ APP 병렬 허용 — API · SSE 페이로드 · 푸시 payload · 오류 코드가 SPEC-007 §6 · §7 · §8 에 다 있다
- back 은 한 워커(`service/chat.py` · `service/push.py` · `repo.py` 가 겹친다) · 앱도 한 워커(`app_state.dart` · `shell.dart` · `lib/chat/` 가 겹친다)
- 계약을 바꿔야 하면 워커가 고치지 않고 코디에게 올린다 → SPEC-007 을 먼저 고치고 두 쪽에 알린다

## 주의

- 푸시는 실기기만 · **백그라운드 푸시 · 잠금 화면은 TestFlight(production APNs)로**(SPEC-004 OQ-614 — Xcode 직접 설치 sandbox 토큰과 섞지 않는다)
- 백엔드 커밋 뒤 compose 재기동 · 워커는 사용자 포트 · 프로세스 · 기기를 건드리지 않는다(실기기 확인은 코디가 허락한 1회만)
- 채팅 사진은 신분증과 같은 볼륨 — 시험 사진은 가짜(풍경 · 단색). 고객 · 여권 사진을 보내지 않는다(OQ-902)
- 경로 수 기준은 코드 51(SPEC-004 §7.3 의 49 가 아님 · SPEC-007 OQ-920 — 이 판도 SPEC-004 §7.3 은 안 고침) (r2)
- 채팅 router 는 모두 `async def` — 동기면 시험이 서비스 직접 호출만으로는 초록이고 실기기에서 푸시가 안 온다(SPEC-007 §6.1 · §13.1 「푸시 대상」 HTTP 경로 단언) (r2)
- 옛 TestFlight 빌드는 채팅 푸시(`kind:"chat"`)를 버린다(`push.dart` 모르는 kind) — 배포와 새 빌드를 같이 올린다
- (r3) 동영상 · 사진 시험 파일은 풍경 · 단색 · 사물만(사람 얼굴 · 고객 · 여권 없음 — OQ-902) · 시뮬레이터 사진첩에 넣는 MOV · HEIC 도 같다
- (r3) 1판 TestFlight 빌드는 `kind:"video"` 를 텍스트로 읽어 빈 말풍선 · `chat_message_edited` 는 버림 → back r3 배포와 새 빌드를 같이 올린다
- (r3) 패키지는 SPEC-007 §9.3 의 권장을 기본으로 — 워커가 다른 것을 고르면 코디에게 먼저(`video_compress` 는 마지막 판이 오래돼 실기기 확인 1회가 WP-APP4 완료 조건)
- (r4) 빌드 12(운영 TestFlight)는 [공유]가 시스템 공유 시트다 — back r4 배포(전달 API 더함 · 기존 API 그대로라 빌드 12 도 안 깨짐)와 빌드 13 을 같이 올린다 · 빌드 12 사용자는 13 으로 업데이트해야 전달이 보인다
- (r4) 전달 시험의 사진 · 동영상도 풍경 · 단색 · 사물만(OQ-902) · 「원본 지우고 전달본 열림」은 실기기 C18 에서 1회
- (r4) `share_plus` 를 빼면 `ios/Podfile.lock` 이 바뀐다 — 커밋에 같이 · 로컬 `pod install` 은 `flutter build` 가 한다
- (r3) 동영상 ~~100MB~~ 90MB(r4) 올리기는 시뮬레이터 · 로컬 back 에서도 컨테이너 `/tmp` 를 잠깐 쓴다 — 로컬 compose 디스크가 모자라면 코디에게
- (r5) **옛 DB 채우기는 운영 첫 부팅에 한 번** — 열이 생기면서 지금 멤버 · 나간 멤버 행의 경계가 `joined_at` 기준으로 채워진다(다시 초대됐던 사람은 그 뒤 옛 대화가 안 보이게 됨 — D9-69 의도). 배포 전 WP-SIM3 에서 옛 compose 볼륨으로 1회 · 두 번 부팅해도 그대로인지 확인(§13.1 「옛 DB」)
- (r5) 빌드 13 은 back r5 위에서도 안 깨진다 — #20 을 안 부르고 · 새 시스템 줄은 보통 시스템 줄로 그리고 · 경계로 걸러진 응답(빈 `lastMessage` · 옛 메시지 없음)은 기존 꼴. 다만 빌드 13 의 1:1 방 정보에는 옛 안내 줄 · [+ 초대] 없음 · 나가기 문구가 옛 것 → back r5 와 빌드 14 를 같이 올린다
- (r5) 모아보기 · 초대 시험 사진 · 동영상도 풍경 · 단색 · 사물만(OQ-902)
- (r5) 코드 브랜치는 `kknaksss/internal-chat-invite`(F10 `3ed1089` 위) — mobile · backend 가 같은 브랜치에서 `procedure/app` · `procedure/back` 을 나눠 쓴다(r4 와 같은 꼴)
