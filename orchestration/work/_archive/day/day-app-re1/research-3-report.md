# research-3 — WORK-002 보충 조사: 앱 예약현황 탭 · 태블릿으로 보내기 · Android 스캔(read-only)

- 기준: cc-prototype `origin/main` = `0553173`(이하 **cc**) · CENTURION_DAY `96036397`(이하 **DAY**) · mediness `day-app-re1-spec` HEAD `319dd82e`(이하 **SPEC** · `products/day/20-spec/` 기준)
- `git show <ref>:<path>` 로만 읽었다. 빌드 · 실행 · KOS · 서버 · DB 접속 없음. 설계 · WP 없음.
- research-2 에서 센 것(여권 스캔 S1 ~ S10 · 문진 QR Q1 ~ Q8 · DAY 표 · 권한 문구 등)은 다시 세지 않고 「→ r2 §n」으로 가리킨다.
- 경로 줄임: cc 앱 `procedure/app/lib/` · cc 백 `procedure/back/app/` · cc 웹 `procedure/front/` · DAY 백 `backend/day/` · DAY 앱 `app/`

## 0. 한 화면 요약

| 묶음 | cc 에 있음 | DAY 에 있음 | 빠진 것(목록만) |
|---|---|---|---|
| 태블릿으로 보내기(§1 · §2) | 전부 — 기기 목록 API · 요청 만들기 · **그 기기 SSE + 푸시 둘 다** · pending 메우기 · 알림 누름 → pending · 태블릿 쪽 QR 화면 · 스캔 화면 · 보낸 쪽 5초 폴링. **여권 스캔도 보냄(kind = scan)** · **cc 웹에 「태블릿에 띄우기」 있음**(문진 · 스캔 둘 다) | `device` 표(`kind` phone/tablet · `platform` ios/android · `last_seen_at`) · `display_request` 표 · `PushKind.DISPLAY` 값 · APNs + FCM 발송 · 직무 태그 `coordinator` | 기기 목록 API · 띄우기 API 4개 · **기기 하나로 보내는 SSE / 푸시**(지금 둘 다 계정 단위) · 앱 푸시 kind `display` 처리(Dart · Android 네이티브 둘 다 모르는 kind 는 버림) · 「코디 기기」 판정 |
| 앱 예약현황 탭 · 상세(§3) | 앱 예약 현황 · 예약 상세 화면(cc) | 웹 예약 현황 · 상세 = **HTML 조각 + 세션 쿠키만** · 서비스 `detail_view` 는 dict(JSON 으로 옮길 값은 이미 한 곳) | 앱 `/api` 예약 읽기 · 쓰기 JSON **0** · 앱용 예약 실시간 채널 0 · 쓰기 결과 신호(`write_confirmed`)를 앱이 받을 길 0 |
| Android 카메라 여권 스캔(§4) | 없음(cc 는 iOS 만 → r2 §0-3) | minSdk 24 · Kotlin 채널 3개 · CAMERA 권한 없음 | 카메라 연속 프레임 · 글자 인식 · QR 그리기 · 화면 꺼짐 막기(Android) |
| 스펙 고칠 절(§5) | | | SPEC-003 4곳 · SPEC-005 1곳 · SPEC-006 1곳 · SPEC-007 7곳 · SPEC-004 1곳 · SPEC-000 1 ~ 2곳 |
| **정할 것** | | | **9개**(§6) |

핵심 사실 다섯:

1. **cc 는 여권 스캔도 태블릿으로 보낸다** — `KINDS = ("questionnaire", "scan")`(cc 백 `service/display.py:28`). 앱은 문진만 보내고 스캔은 웹에서만 보낸다(cc `screens/launchers.dart:3` · D7-72). cc 웹 예약 상세에 [태블릿에 띄우기](문진) · 스캔 단계(기기 고르기)가 있다(cc 웹 `components/reservations/Display.tsx:299` · `:415`).
2. **cc 는 「그 기기」로 보낸다 — DAY 실시간 · 푸시는 「그 계정」으로 간다.** cc SSE 는 `deviceId` 로 연 연결에만 `event: display`(cc 백 `api/board.py:41`) · 푸시도 그 기기 하나(`service/push.py:154-165`). DAY SSE 채널 = (병원, 계정) `day:notify:<hospital>:<account>`(DAY `services/notification_events.py:4-6` · `:26-27`) · 스트림 3개 모두 `deviceId` 를 받지 않음(grep 0) · 푸시 대상 = 계정 목록 → 그 계정의 살아 있는 세션 기기 **전부**(DAY `services/push.py:181-242`).
3. **「코디 기기」는 지금 구조로 칸 추가 없이 셀 수 있다** — 기기(`device.kind` · `last_seen_at` · `login_session_id`) → 세션 → 직원 → 직무 `tags` 에 `coordinator`(DAY `models/device.py:38-49` · `models/staff.py:56` · `:73` · `enums/staff.py:4-13` · KOS 정수 7 = coordinator `emr/kos/mapper.py:104`). 다만 cc 의 「코디 **계정**」 판정(`account.role == "coordinator"` · cc `service/display.py:29` · `:86`)과 DAY 직무 태그는 같은 것이 아니다(DAY 직무 = 태그 배열 · 한 직원 여러 태그). **한 계정 여러 기기 로그인 = 된다** — 같은 계정 다른 세션은 그대로(DAY `services/sessions.py:100`), 상한은 **KOS 동시 로그인 5개**(SPEC `spec-001-login-session.md:43` · `:174`).
4. **웹 예약 상세 · 현황은 앱 토큰으로 못 부른다.** 읽기 = `required_web_view`(쿠키 `day_session` 만 · DAY `session.py:151-156`) + HTML 조각(`routers/reservation_detail.py:170-180` · `routers/reservations.py:45-50`). 쓰기 11개는 `writable_session`(Bearer 도 됨 · `session.py:1-10` · `:63-68`)이지만 응답 = `HX-Trigger day:res-queued` · 결과는 쿠키 SSE `/reservations/stream` 의 `write_confirmed`(`routers/reservation_detail.py:7-11` · `routers/reservations_streams.py:1-15`). 값은 서비스 `reservation_detail.detail_view` 가 dict 로 이미 모은다(`services/reservation_detail.py:128-226`).
5. **Android 스캔 길은 공식 부품으로 있다 — 확인한 것은 문서까지.** ML Kit 글자 인식 v2(번들 = 오프라인 · Latin 약 4 MB/아키텍처 · API 23+) · CameraX(API 21+ · ImageAnalysis = ML Kit 로 넘기는 연속 프레임) 둘 다 DAY minSdk 24 안(DAY `app/android/app/build.gradle.kts:62`). cc `mrz.dart` 는 import 0줄 순수 Dart(시험 파일만 `flutter_test` · cc `test/mrz_test.dart:2-3`) — 파서 · 확정 규칙은 그대로 옮길 후보. 실기기 판독률은 확인 안 됨.

---

## 1. cc 태블릿 띄우기 — 전수 · 단계별

### 1.1 부품

| 부품 | 무엇 | 근거 |
|---|---|---|
| 기기 목록 `GET /api/devices/targets` | **active `coordinator` 계정**의 기기 · `last_seen_at` 24시간 안 · 최근 순 · (계정, installId) 당 1개 · `online` = 지금 그 기기 SSE 열림(서버 메모리) · 다섯 역할 모두 부름 | cc 백 `api/display.py:33-48` · `service/display.py:29-30` · `:83-99` |
| 기기 행 | `kind` = 앱이 화면 짧은 변 ≥ 600 이면 `tablet` · 아니면 `phone` · 이름 없으면 「iPad」/「iPhone」 · 폰도 목록에 들어감(코디 계정이면) | cc 앱 `app_state.dart:30` · 백 `service/devices.py:8` · `:21-35` · 시트 아이콘 `launchers.dart:47` |
| 요청 만들기 `POST /api/display-requests {reservationId, kind, deviceId?}` | 같은 예약 · 종류의 열린 요청 canceled → 새 pending(10분) · `deviceId` 있으면 `reach` · 응답 = 스캔 `qrToken` / 문진 `qrUrl` | `api/display.py:51-77` · `service/display.py:102-132` |
| 닿기 `reach` | **그 기기 SSE 가 열려 있으면 그 연결에만 `event: display {requestId, deviceId, kind, reservationId, qrUrl?}` + 늘 푸시**(허브는 죽은 연결을 ping 전까지 online 으로 봄 → 둘 다) | `service/display.py:134-143` · 연결 `container.py:116-118` |
| 푸시 | 그 기기 하나 · 제목 「고객 입력 요청」(문진) / 「여권 스캔 요청」(스캔) · 본문 「데스크에서 보냈어요」 · 고객 이름 없음 · 소리 없음 · 알림 목록 밖 · payload `{kind: "display", requestId}` · **APNs 만**(cc 에 FCM 없음 · `push/apns.py`) | `service/push.py:154-165` |
| 메우기 `GET /api/display-requests/pending?deviceId=` | 자기 계정 기기만 · 스캔 pending → 돌려주며 opened · 문진은 pending 그대로 · `qrUrl` 은 문진 pending 만 | `api/display.py:80-100` · `service/display.py:146-161` |
| 받기 `POST …/claim {qrToken}` | 스캔 종류 QR(`ccc://display?t=`)로 다른 기기가 받아감 · 1회 · 문진 = 404 | `api/display.py:103-124` · `service/display.py:163-180` |
| 닫기 `POST …/{id}/close {done|canceled}` | 누구나 · 스캔 저장 성공 · 문진 제출 성공이면 서버가 대신 done | `api/display.py:127-147` · `service/display.py:190-216` |
| 상세 응답 `displays[]` | 그 예약 오늘 요청(상태 · 기기 이름 · 시각 · `qrUrl`) — 보낸 쪽이 진행을 보는 유일한 값 | `service/display.py:219-227` · `container.py:120` |

### 1.2 흐름

| 단계 | 보낸 쪽(웹 · 앱 예약 상세) | 서버 | 태블릿(코디 계정 기기) |
|---|---|---|---|
| ① 고르기 | 앱 [태블릿에 띄우기] → targets → 시트(폰) / 창(태블릿) · 「띄울 수 있는 기기가 없어요 — 코디 계정으로 로그인한 기기가 보여요」 · 오늘 이미 제출이면 노란 줄 | `GET /api/devices/targets` | — |
| ② 보내기 | `createDisplay(reservationId, kind, deviceId)` · 토스트 「{기기}에 표시 중」 | 요청 행 · `reach` = SSE(열려 있으면) + 푸시 | — |
| ③-a 앱이 열려 있음 | | | SSE `display` + 그 기기 것이면 → `refreshDisplays()`(pending 읽기) · 실패면 프레임으로 → 열 차례 큐(`displays`) → 셸이 하나씩 엶 · 이미 연 id 는 다시 안 엶 (cc 앱 `app_state.dart:102-117` · `:119-150` · `screens/shell.dart:46-71`) |
| ③-b 앱이 뒤 · 꺼짐 | | | 시스템 알림 → 누름 → `PushKind.display` → `refreshDisplays()` (`app_state.dart:211-213` · `push/push.dart:33` · `:49`) · 로그인 · 앞으로 올 때도 pending 읽음(`app_state.dart:183` · `:313` · `:385` · `:475`) |
| ④ 뜨는 화면 | | | `openDisplay`(cc 앱 `launchers.dart:107-124`): **문진** = QR 화면(흰 전체 화면 · 남은 시간 · 꺼짐 막기 → r2 §2.2) / **스캔** = `GET` 예약 상세 → 스캔 화면(`displayRequestId` 실음 → r2 §1.2) · 다른 띄우기 화면이 열려 있으면 끝날 때까지 기다림(`shell.dart:44` · `:61-71`) · 띄우기 중엔 채팅 배너 버림(`chat/chat_state.dart:18-25` · `:517`) |
| ⑤ 끝 | | 문진 제출 성공 · 스캔 저장 성공 = done · 스캔 [닫기] = canceled(cc 앱 `scan_screen.dart:205-211`) | QR 화면 = 5초마다 예약 상세 폴링 → pending 아니면 한 줄 뒤 닫힘(`qr_show_screen.dart:83-100`) |
| ⑥ 보낸 쪽이 아는 길 | **폴링** — 웹 상세 모달 5초(cc 웹 `DetailModal.tsx:19` · `:160` · `Display.tsx:3` 「단계는 상세 응답 displays[](5초 폴링)로만」) · 앱 보낸 쪽은 띄운 뒤 상세 `_load()` 한 번(`reservation_detail_screen.dart:412`) · SSE 로 알리는 길 없음 | | |

### 1.3 물음에 대한 답

| 물음 | 답 | 근거 |
|---|---|---|
| 여권 스캔도 태블릿으로 보내나 | **보낸다** — kind `scan`. 단 보내는 버튼은 **웹만**(앱엔 없음 · D7-72) | cc 백 `service/display.py:28` · 웹 `Display.tsx:384-415` · 앱 `launchers.dart:3` |
| cc 웹에 「태블릿에 보내기」 있나 | **있다** — 문진 [태블릿에 띄우기](기기 고르기 Popover · 「{기기}에 표시 중」) · 스캔 단계(기기 고르기 → 「{기기}에 보냈어요 · 여는 중…」/「{기기}에서 스캔 중 · 촬영 대기 중…」 · [취소] = close canceled) | cc 웹 `Display.tsx:89-120` · `:186-188` · `:299` · `:413-430` · `:475` |
| 기기 목록 출처 | `device` 행 ∩ active `coordinator` 계정 ∩ 24시간 안 접속 — 계정 역할이 정함(기기 종류는 아이콘만) | cc 백 `service/display.py:83-99` |
| 스캔 QR(claim) | 백엔드 길은 있으나 웹은 스캔에 QR 을 안 그림(「스캔은 기기 버튼만」) | `Display.tsx:3` · `api/display.py:103-124` |

---

## 2. DAY 기기 · 계정 · 알림 구조

| 항목 | 사실 | 근거 |
|---|---|---|
| `device` 표 | 설치 1개 = 1행 · `account_id` · `login_session_id`(서버가 채움) · `install_id`(살아 있는 행 유일) · `push_token`(암호화) · `push_token_hash` · `platform` ios/android · `app_id` · `push_env` · `name` · `kind` phone/tablet · `last_seen_at` | DAY `models/device.py:21-49` · `enums/device.py:4-20` · SPEC `spec-000-data-model.md:1085-1112` |
| 기기 등록 API | `PUT` · `DELETE /api/devices/{install_id}` · 응답 늘 `{ok}` · 늦은 이전 세션 무시 · 같은 토큰 = 연결 하나 | DAY `routers/api/devices.py:36-83` · `services/devices.py:1-25` |
| 앱이 보내는 `kind` | 화면 짧은 변 ≥ 600 = `tablet`(cc 와 같은 기준) | DAY `app/lib/app.dart:111-117` · `state/push_coordinator.dart:164` |
| `name` · `last_seen_at` | 칸은 있음 · **채우는 코드 확인 안 됨**(등록 서비스 인자에 `name` 없음 — `routers/api/devices.py:57-66`) · `last_seen_at` 갱신 grep 확인 안 함 | 위 |
| 푸시 경로 | **APNs · FCM 둘 다** — `platform = android` 는 `push_env` 없이 · FCM 키 없으면 `skipped_no_key` · 같은 본문 모양을 FCM data 로 | DAY `services/push.py:1-24` · `adapters/apns.py` · `adapters/fcm.py` · Android 빌드 `firebase-messaging`(`app/android/app/build.gradle.kts:128-131`) |
| 푸시 대상 고르기 | **계정 목록 → 그 계정의 살아 있는 세션 기기 전부**(그 병원 세션 · 활성 직원 · 시스템 계정 제외). 기기 하나를 고르는 함수 없음 | DAY `services/push.py:181-242`(`LoginSession.account_id.in_(ids)`) |
| `PushKind.DISPLAY` | enum 값만 있음 · 쓰는 곳 0 | DAY `enums/notification.py:14` · grep |
| 앱 푸시 누름 | Dart = `chat` · `doctor_call` · `doctor_call_cancel` 만 처리, 그 밖 kind 는 버림 · Android 네이티브 = 알는 kind 셋 밖이면 **알림을 띄우지도 않음** · iOS 는 `willPresent` · `didReceive` 에서 kind 로 가름 | DAY `app/lib/state/push_coordinator.dart:196-216` · `app/android/.../PushLogic.kt:16-33` · `app/ios/Runner/AppDelegate.swift:113-151` |
| 실시간 채널 | 앱 SSE 3개 — `/api/board/stream`(병원 판) · `/api/chat/stream` · `/api/notifications/stream`(둘 다 (병원, 계정) Redis 채널) · 공통 본문 `routers/api/streams.py` · **기기 단위 채널 0**(세 라우터 · `stream_sessions` grep `device_id` 0) | DAY `routers/api/streams.py:1-8` · `services/live.py:1-6` · `services/notification_events.py:4-6` · 앱 `app/lib/data/board_stream.dart:1` · `chat/chat_stream.dart:19` · `notify/notification_controller.dart:54` |
| 재사용 후보 | 알림 스트림(`event: notification` 한 종류 · 계정 채널) — 이벤트 이름 집합 `EVENTS` 만 넓히면 같은 구독 틀(`live.Subscription`)을 쓸 수 있는 구조. 단 계정 채널이라 **같은 계정 다른 기기도 받는다** | `services/notification_events.py:23` · `services/live.py:26-50` |
| 계정 · 역할 | `account`(이메일 · 이름) — 역할 칸 없음 · 역할은 병원별 `staff.job_role_id` → `job_role.tags[]`(admin · doctor · counselor · nurse · skincare · call_counselor · **coordinator**) + 권한 키 표 | DAY `models/staff.py:22-86` · `enums/staff.py:4-13` |
| 「코디용 태블릿 계정」 표현 | **새 칸 없이** 「세션 직원 직무 태그에 coordinator ∧ `device.kind = tablet`」로 고를 수 있음. 「코디 전용 계정」을 따로 가리킬 칸(계정 표시 · 기기 표시)은 **없음** | 위 · `models/device.py:48` |
| 한 계정 여러 기기 | **된다** — 로그인 = 새 `login_session` 행 · 같은 계정 다른 세션은 안 건드림 · 기기마다 자기 세션에 결속 · 상한 = KOS 동시 로그인 5개(꽉 차면 기기 선택 단계) | DAY `services/sessions.py:83-110` · `services/auth.py:22-33` · `:445-485` · SPEC `spec-001-login-session.md:43` · `:113` · `:174` |
| `display_request` 표 | `visit_id`(uuid · cc 는 `reservation_id`) · `device_id` · `qr_token_hash` · `qr_nonce`(필수 — cc 는 스캔이면 null) · 상태 5 · 쓰는 코드 0 | DAY `models/reception.py:33-49` · → r2 §3 |

---

## 3. 웹 예약 상세 모달 → 앱 이식 범위

공통: 모달 = `GET /reservations/visits/{id}` HTML 조각 · `required_web_view`(쿠키만) · 값 = `reservation_detail.detail_view` dict(DAY `routers/reservation_detail.py:170-180` · `services/reservation_detail.py:128-226`). 쓰기 = `writable_session`(Bearer 통과) · 응답 HTMX 헤더 · 결과 = 쿠키 SSE `write_confirmed` · `kos_failed`. 앱 `/api` 에 예약 경로 0(→ r2 §3 「예약 / 접수 API」). 아래 「앱 토큰」 열 = 그 HTTP 경로를 Bearer 로 부를 수 있나.

### 3.1 상세 모달 — 칸 · 상자 · 버튼

| # | 요소 | 웹 위치(`templates/partials/reservations_detail.html`) | 데이터 · API | 읽기/쓰기 | 앱 토큰 | 앱에 지금 |
|---|---|---|---|---|---|---|
| 1 | 머리 — 단계 이름(10단계) · 색 · [닫기] | `:17-21` · `:68-71` | `detail.stage` | 읽기 | ✗(쿠키 HTML) | 없음 |
| 2 | 이전 방문 기록(재진 · 카드 펼침 · 예약 담당 · 상담 · 시술 · 받은 시술) | `:73-92` | `previous_visits[]` | 읽기 | ✗ | 없음 |
| 3 | 고객 이름(누르면 차트 — 스펙은 「준비중입니다」 D46) · 초진/재진 배지 | `:97-98` | `customer.name` · `is_new` | 읽기 | ✗ | 없음(판 카드에 이름만 → r2 §3) |
| 4 | [문진 QR] · [여권 스캔] — 비활성 | `:100-101` | `editable.qr` · `editable.scan` | (자리) | ✗ | 없음 |
| 5 | 성명(여권) · 연락처 · 생년월일/성별(만 나이) · 국적/통역 · 특이사항 | `:103-107` · `:120` | `customer.*` | 읽기 | ✗ | 일부(판 고객 = 이름 · 성별 · 생년월일 · 국적 → r2 §3) |
| 6 | 신분확인 — 내국인 「신분증 확인」 체크 / O / 미확인 | `:108-117` | `PUT /reservations/visits/{id}/identity` | **쓰기**(DAY 기록만) | 경로 ○ · 응답 HTML 모달(`target="#modal-root"`) | 없음 |
| 7 | 초진 문진 「작성 필요」 · 건강정보 「문진 전」(값 비움) | `:118-119` | 없음(고정 글) | 읽기 | — | 없음 |
| 8 | 예약 정보 머리 [예약 변경] · [예약 취소] | `:124-132` | 변경 = `GET …/edit`(HTML 창) → `PUT …/schedule` · 취소 = 확인 창 → `POST …/cancel` | **쓰기**(KOS 쓰기 큐) | GET ✗ · PUT/POST 경로 ○(응답 HTMX 헤더) | 없음 |
| 9 | 담당자 · 예약 일시 · 유입채널 · 예약메모 | `:134-135` · `:173-174` | `reservation.*` | 읽기 | ✗ | 없음 |
| 10 | 동행 — 이름(누르면 그 상세) · [수정]/[+ 동행 추가] → 체크 목록 [저장] | `:136-160` | `companions` · `candidates` · `PUT /reservations/companions/group`(이 쓰기만 `required_web_view` 도 요구 → 쿠키 필요) | **쓰기**(DAY 만) | ✗(`routers/reservation_detail.py:312-316`) | 없음 |
| 11 | 의사 지정 — 값 버튼 → 고르기 → 바로 KOS | `:161-172` | `doctors[]` · `PUT …/doctor` | **쓰기**(큐) | 경로 ○ | 없음 |
| 12 | 시술 목록(상품명 · 회차 · 「오늘」 ✓ 체크 · 상태 태그) | `:180-204` | `treatments[]` · `editable.today_check` | 읽기 + (체크 = 화면에 담음 → #16 에 실림) | ✗ | 없음 |
| 13 | 오더 메모 글 칸(예약 · 접수 ∧ 시술만 진행 ∧ ✓) | `:205-208` | `POST …/order-memo` 또는 #16 에 실림 | **쓰기** | 경로 ○ | 없음 |
| 14 | 귀가 사유 | `:209-211` | `discharge_reason` | 읽기 | ✗ | 없음 |
| 15 | 수납 정보(상품 합계 · 할인 · 총 수납 · 수납 완료 · 수납 필요 · 경고) | `:213-231` | `payment.*` | 읽기 | ✗ | 없음 |
| 16 | 바닥 줄 — [처방전 출력](KOS 링크) · 「시술만 진행」 · [상담사 ▴] · [관리실 ▴] · [접수] · [상담 대기] / [시술 대기] · [N원 수납](KOS 링크) · [귀가 처리](확인 창) | `:234-281` · 확인 창 `:283-291` | `POST …/reception` · `…/consultation-waiting` · `…/procedure-waiting` · `PUT …/counselor` · `…/room` · `POST …/discharge` · 링크 `links.prescription` · `links.purchase` | **쓰기**(큐 · 결과 전 잠금 D52) | 경로 ○(응답 HTMX 헤더 · 결과는 쿠키 SSE) | 없음 |
| 17 | KOS 실패 [다시 시도] | `POST …/{id}/retry` · `POST /reservations/retry` | **쓰기** | 경로 ○ | 없음 |

- 쓰기 경로 전수 = `routers/reservation_detail.py:234-512`(POST `/reservations` · PUT `schedule` · POST `cancel` · PUT `doctor` · PUT `companions/group` · POST `retry` × 2 · POST `reception` · PUT `identity` · POST `consultation-waiting` · PUT `counselor` · PUT `room` · POST `procedure-waiting` · PUT `order-memo` · POST `discharge`).
- 쓰기 응답이 「큐에 넣음」까지만이고 결과는 `/reservations/stream`(쿠키 · `required_web_view`)으로만 온다(`routers/reservations_streams.py:1-15` · `:125-131`). 앱 `/api/board/stream` 은 `board` · `kos_failed` · `session_expired` 만(`routers/api/board.py:21-24`) — `write_confirmed` · `reservation` 이벤트 없음.

### 3.2 웹 예약 현황 목록

| # | 요소 | 웹 위치 | 데이터 · API | 읽기/쓰기 | 앱 토큰 | 앱에 지금 |
|---|---|---|---|---|---|---|
| L1 | 날짜 머리 ‹ 날짜(요) › · [오늘] · 달력 | `partials/reservations_main.html:13-23` · `reservations_parts.html:38-53` | `GET /reservations?date=` | 읽기 | ✗(쿠키 · HTML) | 없음 |
| L2 | [필터] 상태 팝오버(전체 · 상태별 수) | `reservations_parts.html:54-64` | `filter{total, counts}` | 읽기(화면 안 거르기) | ✗ | 없음 |
| L3 | 시간 × 열 표 · 카드(이름 · 국적 · 수납 필요 · 담당 · 초진 · 동행 띠) · 현재 시각 선 | `reservations_parts.html:66-138` | `axis` · `columns` · `cards` · `rows` · `bands` | 읽기 | ✗ | 없음 |
| L4 | 카드 누름 = 예약 상세 · 우클릭 메뉴(예약 변경 · 예약 취소 · 동행 추가) · 빈 칸 누름 = 예약 등록 창 | `reservations_parts.html:66-70` · `:99` · `reservations_dialogs.html:60-62` | 상세 §3.1 · `GET /reservations/book` | 쓰기로 이어짐 | ✗ | 없음 |
| L5 | 오른쪽 패널 — 공지 / 예약 탭 · 원내 현황 | `reservations_parts.html:139-230` | `notice` · `inhouse` · `PUT /reservations/notice` | 읽기 + 공지 쓰기 | 공지 PUT 경로 ○ · 읽기 ✗ | 없음 |
| L6 | 실시간 — SSE `reservation` 신호 → `?poll=1` 로 조각 다시 받기 | `reservations_main.html:34-36` | `/reservations/stream` | 읽기 | ✗ | 없음 |

- 앱 예약 JSON 빠진 것(목록만): 예약 목록(날짜 · 필터 수) · 예약 상세 값 · 쓰기 응답 JSON(지금 HTMX 헤더) · 쓰기 결과 신호(앱 스트림) · 동행 저장(쿠키 의존 풀기) · 상세의 `displays[]` 같은 띄우기 상태 · 권한 판정(`editable`)을 앱에 싣는 자리. 파트너용 `/api/ext`(`X-Api-Key` · DAY `routers/api/ext.py:44` · `:97-100`)는 직원 토큰 길이 아님.

---

## 4. Android 카메라 여권 스캔 길

### 4.1 DAY 앱 사실

| 항목 | 값 | 근거 |
|---|---|---|
| minSdk · targetSdk | 24 · 36 | DAY `app/android/app/build.gradle.kts:59-64` |
| CAMERA 권한 | **없음**(INTERNET · RECORD_AUDIO · READ_MEDIA_* · POST_NOTIFICATIONS) | `app/android/app/src/main/AndroidManifest.xml:5-13` |
| 네이티브 채널 | `day/session` · `day/push` · `day/video`(스텁) | `MainActivity.kt:9-29` |
| 네이티브 의존 | firebase-bom · firebase-messaging · androidx.core | `build.gradle.kts:128-131` |
| Flutter 패키지 | http · crypto · flutter_tts · record · audio_session · flutter_pcm_sound · image_picker · flutter_image_compress · photo_manager · video_player · url_launcher — 카메라 스트림 · OCR 0 | `app/pubspec.yaml` dependencies |
| iOS 배포 대상 | 13.0 | `app/ios/Runner.xcodeproj/project.pbxproj:478` |

### 4.2 후보

| 후보 | 오프라인 | 라이선스 | 앱 크기 | cc `mrz.dart` 그대로 | iOS cc 꼴(네이티브 채널)로 | 근거 |
|---|---|---|---|---|---|---|
| **A. 네이티브 Kotlin 채널 = CameraX(ImageAnalysis) + ML Kit 글자 인식 v2 번들(Latin)** | ○ — 번들 모델은 빌드 때 앱에 묶임 · 「즉시 사용」 · 입력 · 결과를 Google 서버로 안 보냄(업데이트 확인 · 사용 지표는 보냄 → 사용자 고지 필요) | CameraX = Jetpack(Apache 2.0 — 페이지에 명시 없음 · 확인 안 됨) · ML Kit = ML Kit 약관 + Google APIs ToS(모델 역공학 금지) · 무료 여부 문구 없음 | ML Kit 번들 Latin **약 4 MB / 아키텍처** · CameraX 크기 = 확인 안 됨 | ○ — 줄 문자열을 Dart `checkMrz` 로 묻는 cc 구조(`scan_channel.dart:49-62`)와 같게 가능(Kotlin 이 줄을 넘김) | ○ — cc 채널 메서드 = `scanPassport{windows, windowSec, debug}` · `checkMrz`(네이티브 → Dart) · `qrImage{text,size}` · `keepAwake`(cc `scan/scan_channel.dart:18-60`) — 같은 이름 · 모양을 Kotlin 에 둘 수 있음. API 23+ / 21+ ⊂ minSdk 24 | developers.google.com/ml-kit/vision/text-recognition/v2/android · developers.google.com/ml-kit/terms · developer.android.com/media/camera/camerax |
| B. ML Kit 비번들(Play 서비스) | △ — Play 서비스가 처음에 모델을 내려받아야 하고 받기 전 요청은 결과 없음 | 위와 같음 | 약 260 KB | ○ | ○ | 위 ML Kit 페이지 |
| C. Flutter `camera`(flutter.dev · BSD-3) 이미지 스트림 + `google_mlkit_text_recognition`(flutter-ml.dev · MIT · Google 비공식 유지 · 1.0.3) | ○(Android 번들 Latin 기본) | BSD-3 + MIT + ML Kit 약관 | 확인 안 됨 | ○(Dart 에서 바로) | ✗ — Dart 쪽 공용 경로라 cc 네이티브 꼴과 다름 · **`google_mlkit_text_recognition` iOS 최소 15.0 > DAY 13.0** · iOS 는 `LatinOCRResources.bundle` 수동 추가 · `camera` 페이지에 매크로 · 초점 조절 언급 없음(cc 가 실기기에서 막힌 지점 → r2 §1.4) | pub.dev/packages/camera · pub.dev/packages/google_mlkit_text_recognition |
| D. Android 는 손 입력만 | ○ | — | 0 | (파서 불필요) | — | cc 손 입력 길 → r2 §5 Q3(사용자 범위로 뒤집힘 — 참고만) |

- 공통으로 Android 에 더 필요한 것(목록만): `CAMERA` 권한(매니페스트 · 실행 중 요청) · QR 그리기(cc = iOS CoreImage · Android 길 없음 → r2 §2.2) · 화면 꺼짐 막기 · 원본 메모리만 원칙(cc D-50 → r2 §1.3)을 Android 에서 지킬 방법.
- 실기기에서 갤럭시 탭 카메라로 여권 MRZ(OCR-B) 판독률 · 근접 초점 = **확인 안 됨**(실행 금지).
- `image_picker` 카메라는 한 장 촬영(인텐트)이라 cc 가 버린 방식(→ r2 §1.4)과 같은 꼴.

---

## 5. 스펙 대조 — 바꾸려면 고칠 절

| 문서 · 줄 | 지금 | 사용자 범위와 부딪힘 |
|---|---|---|
| SPEC `spec-003-mobile-app.md:29` · `:108` · `:144` | 앱 셸 = 하단 3메뉴(예약현황 숨김 · 개정 ⑮) | 예약현황 탭 신설 |
| SPEC-003 `:71`(개정 ⑮ — 2026-11-13 App Store 2.1 거절 뒤 숨김) | 숨긴 이유 = 심사 거절 · 「예약 기능이 생기면 다시 넣음」 | 다시 넣는 조건 충족 여부를 이 개정에 적어야 |
| SPEC-003 `:123`(범위 밖 표) | 예약현황 메뉴 · 기능 · **띄우기(`display`) · 여권 스캔** 뺌 | 셋 다 넣음 |
| SPEC-003 `:134` · `:1099` | 「여권 스캐너 · 문진 QR · 예약 탭 = 다음 작업(WORK-002)」 | WORK-002 범위로 옮김 |
| SPEC-003 `:1044` | 권한 = 알림 · 마이크만 · **카메라(여권 스캔 · 띄우기 · QR) 안 넣음** · 채팅 카메라는 SPEC-004 | iOS 문구 · Android CAMERA 권한 |
| SPEC `spec-005-notifications.md:77` | 띄우기 푸시 · 여권 스캔 · 웹 기기 목록 · 기기 이름 = DAY 범위 밖 | 띄우기 푸시 · 기기 목록 넣음 |
| SPEC `spec-006-reservation-board.md:111` | R5 「앱으로 보내기 — 여권 스캔 · 전후 사진 · 문진」 뺌 | 웹에서 태블릿으로 보내기 |
| SPEC `spec-007-reservation-detail.md:67` · `:109` · `:152` · `:202` · `:345` · `:626` | [문진 QR] · [여권 스캔] = 자리만 · 비활성 · 안내 없음 · B4 띄우기 · B6 스캔 취소 · B8 건강정보 펼침 뺌 | 웹 버튼 켜기 · 기기 고르기 · 진행 표시 |
| SPEC-007 결정 `:726` D13 · `:733` D20 · `:768` D55 | 비활성 · 값 비움 · 보이는 조건 | D13 · D20 고침(D55 조건은 그대로 쓸 수 있음) |
| SPEC `spec-004-internal-chat.md:538` · `:636` OQ-C7 | iOS 카메라 문구에서 「여권 사진면을 찍거나」 일부러 뺌 | 문구 다시 넣음(→ r2 S10) |
| SPEC `spec-000-data-model.md:1153-1164` (`display_request`) · `:1085-1112` (device 규칙 「보내기 대상」) | 기기 하나로 보내는 규칙 없음 · `kind` 「문진 등」 · `qr_nonce` 필수 | 스캔 종류(nonce 없음) · 기기 하나 대상 규칙 |

---

## 6. 정할 것 — 9개(범위 안 · 사용자만)

| # | 질문 | 추천 | 근거 |
|---|---|---|---|
| T1 | **보낼 대상 기기 목록 = 무엇으로 고르나** — (a) 직무 태그 coordinator 직원의 `kind = tablet` 기기만 / (b) coordinator 직원 기기 전부(폰 포함 · cc 와 같음) / (c) 따로 「띄우기 받는 기기」 표시(새 칸) | **(a)** | 사용자 말 「코디용 계정으로 로그인한 기기 = 태블릿」 · 칸 추가 없이 됨(§2) · cc 는 폰도 보였음(`launchers.dart:47`) |
| T2 | 「코디용 계정」 = 공용 코디 계정 하나를 여러 태블릿이 같이 쓰나 / 코디마다 자기 계정 | **확인 필요(추천 없음)** — 공용이면 KOS 동시 로그인 5개 상한이 태블릿 수 상한이 됨 | SPEC-001 `:43` · `:174` · cc 는 「코디 계정」 하나 가정(`service/display.py:29`) |
| T3 | 기기 이름 — 목록에 무엇을 보이나(기기 `name` 을 앱이 채움 / 직원 이름 + 「태블릿」 / 설정에 「이 기기 이름」 칸) | **설정에 「이 기기 이름」 칸**(cc 와 같음) | 태블릿 여러 대면 「iPad」 「iPad」로 못 가림 · DAY `device.name` 칸은 있는데 채우는 곳 없음(§2) · cc `screens/settings_screen.dart:118-122`(SPEC-005:77 인용) |
| T4 | 같은 계정 · 같은 병원 다른 기기(코디 폰)에도 띄우기가 가나 — 기기 하나로만 | **그 기기 하나로만** | DAY 채널 · 푸시가 계정 단위라 그대로 쓰면 같은 계정 기기가 다 띄움(§0-2) · cc 는 기기 하나 |
| T5 | 태블릿 앱이 꺼져 있을 때 알림 — 소리 · 알림 목록에 남기나 | **cc 그대로(보이는 알림 · 소리 없음 · 목록 밖 · 고객 이름 없음)** | cc D7-67 · E2E 거친 값(`service/push.py:155-163`) |
| T6 | 웹 · 앱 보낸 쪽이 진행(보냄 · 여는 중 · 입력 중 · 제출됨 · 스캔 저장됨)을 어떻게 아나 — 폴링 / 실시간 신호 | **실시간 신호**(DAY 웹 예약 상세는 이미 SSE 로 다시 받음) | cc 는 5초 폴링(`DetailModal.tsx:19`) · DAY 는 개정 ⑫ 로 폴링을 SSE 로 바꿈(`reservations_main.html:34-36`) — 같은 기준이면 신호 |
| T7 | 앱 예약 상세의 쓰기 — 웹 모달 쓰기 11개(접수 · 상담 대기 · 의사 지정 · 동행 · 귀가 · 취소 · 변경 등)를 앱에서 **누를 수 있나** / 보기만 | **확인 필요 — 사용자 말 「내용이 그대로 뜬다」가 쓰기까지인지** | 「그대로 뜬다」는 보기로도 읽힘 · 쓰기까지면 쓰기 결과 신호 · 잠금(D52)도 앱에 필요(§3.1 끝) |
| T8 | 앱 예약 현황 목록 꼴 — 웹 같은 시간 × 열 표 / 폰은 목록 · 태블릿은 표 | **폰 = 목록 · 태블릿 = 표** | 웹 표는 가로 넘김 · 열 폭 계산(`reservations_main.html:5-6`) · cc 앱은 예약 현황을 따로 그림(cc `screens/shell.dart:78-84`) — 시안 없음이면 시안 먼저(화면 문구 지어 넣지 않기) |
| T9 | Android 스캐너 부품 — A(네이티브 CameraX + ML Kit 번들) / C(Flutter 패키지) | **A** | cc iOS 와 같은 채널 꼴 · 파서 · 확정 규칙 공유 · C 의 ML Kit 플러그인은 iOS 15.0 이 최소라 DAY iOS 13.0 과 안 맞음 · 번들 = 오프라인(§4.2) — 실기기 판독률은 구현 뒤 확인 |

(r2 §5 의 Q4 · Q5 · Q6 · Q8 · Q12 는 이번 범위로 뒤집히지 않아 그대로 남는다 — 여기서 다시 세지 않음. Q7 은 사용자가 「KOS 에 제출」로 정함 · Q6 은 「KOS + DAY 저장소 둘 다」로 정함.)

---

## 7. 확인 안 됨

- DAY `device.name` · `last_seen_at` 을 채우는 코드(등록 서비스 인자에 `name` 없음 · `last_seen_at` 갱신 grep 안 함)
- KOS 동시 로그인 5개가 계정당인지 기기 종류 무관인지(SPEC-001 문구만 읽음 · KOS 접속 금지)
- ML Kit 번들 Latin 으로 여권 MRZ(OCR-B · `<` 줄) 판독률 · 갤럭시 탭 근접 초점 · CameraX 크기 · CameraX 라이선스 문구
- ML Kit 사용 지표 전송을 DAY 개인정보 처리 안내에 넣어야 하는지(약관은 「사용자에게 알려야」)
- DAY 배포 파드 수(기기 단위 신호를 메모리로 둘 수 있는지 — cc 는 한 파드 메모리 허브)
- iOS 가 푸시 kind `display` 를 받았을 때 지금 코드가 배너를 띄우는지(`AppDelegate.swift:113-151` 의 갈래만 봄 · 실행 안 함)
