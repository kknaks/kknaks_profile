# research — DAY 직원 앱 다음 버전 현황 조사 (day-mobile-v2)

- 작성: day researcher(read-only) · 2026-11-20
- 원천 ref: CENTURION_DAY `origin/dev` = `844eace4` · interpret-pwa `origin/main` = `56e43a0` · 스펙 = mediness 워크트리 `day-mobile-v2-spec`(`ccede286`)
- 표기: 코드 근거는 `dev:<경로>:<줄>`(CENTURION_DAY origin/dev) · `tk:<경로>`(interpret-pwa origin/main) · 스펙은 `SPEC-00n §/줄`
- 이 리포트는 **지금 모양과 차이**만 적는다. 결정은 하지 않고 §F 로 모았다. 비밀값 · 도메인 · IP · Azure 이름은 적지 않았다.

---

## A. 앱 공통

### A1. 버전 · 빌드 번호 · dev/prod 가르기 · 절차 문서

| 항목 | 지금 값 | 근거 |
|---|---|---|
| pubspec | `version: 0.1.0+1` — 레포 값은 안 올림. 빌드 때 `--build-name` · `--build-number` 로 덮는다 | `dev:app/pubspec.yaml:5` · `dev:app/README.md:227` |
| iOS 개발 앱(DAY Dev) | TestFlight 0.1.0 (1) · (2) · **(3)** 업로드 | mobile-deployment §1-1(줄 60) |
| iOS 정식 앱(DAY) | 0.1.0 **(2)** 심사 제출 · Unlisted 신청 · 결과 대기 | mobile-deployment §1-1(줄 63) · §6(줄 188) |
| Android 개발 앱 | Play 내부 테스트 **vc3** | mobile-deployment §1-1(줄 68) |
| Android 정식 앱 | 비공개 테스트 vc3 → 프로덕션 **vc3**(공개됨 — `_RESUME.md` 배경) | mobile-deployment §1-1(줄 68) · android-app 회고 §1 |
| versionCode / CFBundleVersion | Flutter 값 그대로(`flutter.versionCode` · `$(FLUTTER_BUILD_NUMBER)` 계열) — 앱마다 따로 셈 | `dev:app/android/app/build.gradle.kts:65-66` · `dev:app/README.md:252` |

→ 다음 빌드 번호 최소값(앞 업로드보다 커야 함): **iOS DAY Dev ≥ 4 · iOS 정식 ≥ 3 · Android 개발 ≥ 4 · Android 정식 ≥ 4**(위 값에서 따라옴). 빌드 번호 규칙은 [미결] M-13(mobile-deployment §10 줄 346 · §13 줄 391). 버전 이름(0.1.0 그대로 / 올림)은 정해진 것 없음 → §F.

**dev/prod 가르기 — flavor 없음.** 세 축으로 갈린다.
1. 식별자 · 이름: iOS `DAY_BUNDLE_ID` · `DAY_DISPLAY_NAME`(`Identity.xcconfig` 기본값 placeholder · `Identity.local.xcconfig` 또는 xcodebuild 인자) / Android `DAY_APPLICATION_ID` · `DAY_APP_NAME`(`-P` > `identity.local.properties` > placeholder) — `dev:app/ios/Flutter/Identity.xcconfig` · `dev:app/android/app/build.gradle.kts:10-20,58-59` · `dev:app/android/identity.properties`
2. 서버: `--dart-define` `DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS` · `DAY_REQUIRE_ENVIRONMENT` · `DAY_APNS_ENV` · `DAY_DEV_LOCAL_ORIGIN` — `dev:app/lib/core/build_config.dart:1-12,107-115`. 개발 앱 = 진입점 · 허용 = dev 하나, 정식 앱 = 진입점 prod · 허용 prod+dev(`dev:app/README.md:44-46,205-206` · mobile-deployment §1 줄 54 · §9-1).
3. 세션 대상: 로그인 응답 `environment` · `api_base_url` 이 정한다(release 는 둘 다 없으면 `environment_unavailable`) — `dev:app/lib/state/session_controller.dart:269-289`.
- flavor 2개 안은 mobile-deployment §4 에 **[제안]** 으로만 남음(줄 132-134).
- **사용자 결정 「DAY Dev 로 먼저 → 같은 코드를 prod 설정으로」(_RESUME §2)는 지금 구조로 바로 된다** — 코드 같음 · 빌드 인자(식별자 · dart-define)만 다름.

**빌드 · 업로드 절차 문서 위치**
- `dev:app/README.md` — 빌드 설정 표(줄 28-50) · iOS 식별자(줄 61-63) · Android 빌드 · `play_upload.py`(줄 205-252)
- `dev:app/android/play_upload.py` — Play API(개발 → internal · 정식 → alpha 만 · 프로덕션은 Console 손 단계)
- mediness `40-architecture/mobile-deployment.md` — §1-1 지금 상태 · §7-3-2 Play 손 단계 · §10 버전 · §11 release 전 확인
- iOS 업로드 = altool + 로컬 키(코디 메모 `reference_testflight_upload`) — 레포 문서엔 iOS 업로드 명령 줄 없음(README 줄 63 은 archive 인자만). 서명 정식 방법 [미결] M-16(mobile-deployment §5-2 줄 160)
- 주의: Apple Unlisted 는 승인 뒤 **이후 버전 전부 Unlisted**(mobile-deployment §6 줄 188 · Apple 원문 인용 있음)

### A2. 모르는 코드 · 값 처리 — 「깔린 옛 앱 + 새 서버」에서 깨질 곳 전수

공통 바탕: 앱 HTTP 오류는 본문 `code` 만 읽는다(`dev:app/lib/data/day_api.dart:186-191`). 2xx 본문이 Map 이 아니면 `unexpected_response`(같은 파일 :181-184).

| # | 표면 | 옛 앱이 받으면 | 근거 |
|---|---|---|---|
| 1 | 로그인 200 의 새 `status`(예: `choose_device`) | `status != signed_in` · `!= choose_hospital` → 로그인 실패 · 오류 칸 **`unexpected_response` 코드 글자** | `session_controller.dart:186-203` |
| 2 | 로그인 · 세션 새 오류 코드 | 표에 없으면 **코드 글자 그대로**(`codeOnly`) | `dev:app/lib/core/copy.dart:5-16,49-51` |
| 3 | 로그인 응답 `environment` 새 값 | `prod`·`dev` 밖이면 `environment_unavailable` | `session_controller.dart:51,272` |
| 4 | 시술 현황 조작 새 오류 코드 | `actionMessage` → **코드 글자 그대로**. 지금도 앱 표에 없는 서버 코드: `conflict` · `task_not_assignable` · `chart_conflict` · `chart_staff_required` · `staff_not_listed` · `visit_not_on_board` · `room_same` · `room_not_held` · `room_held` · `visit_not_home` · `task_not_called` · `task_start_reflecting`(웹은 뒤 8개를 「토스트 없음」으로 둠) | 앱 `copy.dart:24-43,52` · 서버 `dev:backend/day/routers/board_messages.py:4-38` |
| 5 | 시술 줄 `state` 새 값 | 「준비중」으로 표시 | `dev:app/lib/ui/format.dart:113-120` |
| 6 | `needs[].why` 새 값 | `why` 원문 글자 표시 | `format.dart:94-103` |
| 7 | 스냅샷 새 칸(예: `systemDoctor` · `systemDoctorTaskIds`) | 무시(이름으로만 읽음) — 안전. 단 화면에도 안 나옴 | `dev:app/lib/model/board.dart` 전체 · tolerant-reader 개념 |
| 8 | 알림 목록 새 `kind` | 목록에서 **버림** · 그러나 서버 `unread` 는 종류 안 가리고 셈 → **종 배지 숫자 ≠ 목록** | 앱 `dev:app/lib/notify/notification_model.dart:13,69-75` · 서버 `dev:backend/day/services/notifications.py:106-120` |
| 9 | 알림 설정 새 `kind` | 이름 표(`notifKindName`)에 없으면 줄을 안 그림 — 켜고 끌 수 없음 | `notification_model.dart:16,84-87` |
| 10 | 푸시 새 `kind`(iOS) | OS 가 배너 · 소리는 띄움(chat 만 Dart 로 돌림) · **눌러도 아무 데도 안 감** | `dev:app/ios/Runner/AppDelegate.swift:109-130` · `dev:app/lib/state/push_coordinator.dart:200-205` |
| 11 | 푸시(Android) | 채널 스텁 — 토큰 안 냄 · 푸시 자체 없음 | `dev:app/android/app/src/main/kotlin/day/medisolveai/PushChannel.kt` |
| 12 | SSE 새 이벤트 이름 | 판 스트림은 `board` · `kos_failed` · `session_expired` 만, 알림 스트림은 `notification` 만 — 나머지 무시 | `dev:app/lib/data/board_stream.dart:130-148` · `dev:app/lib/notify/notification_controller.dart:55` |
| 13 | 통역 WS 새 서버 메시지(예: 통키 `audio_stop`) | `switch` 에 default 없음 → 무시 | `dev:app/lib/interpret/interpret_client.dart:212-235` |
| 14 | 통역 서버가 새 클라이언트 메시지를 기대(예: 통키 `playback_stopped`) · 반이중 해제 전제 | 옛 앱은 보내지 않음 · 재생 중 마이크를 막음(반이중) — 서버 동작이 그 전제를 요구하면 끼어들기 등이 옛 앱에선 안 일어남 | `interpret_client.dart:6,255-275` · `tk:front/lib/interpret.ts`(c7a582f) |
| 15 | 통역 핸드셰이크 거절 | 403 은 한 문구로 뭉침(OQ-A42) | SPEC-003 OQ-A42(줄 1029) |

---

## B. 기기 로그인 제한

### B1. 앱 로그인 흐름 지금 모양
- 화면: 로그인(이메일 · 비밀번호) → 병원 고르기(여럿일 때) → 판. `Phase { booting, restoring, signedOut, choosingHospital, board, forbidden }` — `session_controller.dart:15`
- API: `POST {진입점}/api/auth/login {email,password,client:"app"}`(75초 · 자동 재시도 없음) → 200 `signed_in` 또는 `choose_hospital{pending_token,hospitals}` → `POST {대상}/api/auth/hospital {pending_token,hospital_id,client}` → `GET /api/auth/me` 로 환경 확인 뒤 저장 — `dev:app/lib/data/day_api.dart:109-126` · `session_controller.dart:170-257`
- 병원 고르기 임시 토큰 만료 · 이미 씀 = `session_expired` → 입력 화면 + 문구 — `session_controller.dart:240-249`
- 「처음으로」 = `backToStart()` — `session_controller.dart:259-266`
- 데모 계정은 prod 서버가 dev 로 넘김(`environments.relay_login`) — `dev:backend/day/routers/api/auth.py:90-92`

### B2. 앱 경로의 `SignInLimitExceeded` · 웹 기기 선택 API · 앱 재사용 가능성
**지금 앱 경로 응답** — 401 `invalid_credentials`(틀린 비밀번호와 같음) · 목록 · 임시 토큰 안 만듦 · 로그에만 기기 제한.
- `dev:backend/day/routers/api/auth.py:9-10,93-97`(`device_choice=False`) · `dev:backend/day/services/auth.py:248-256` · SPEC-001 개정 ⑨ 보충 ④(줄 46) · OQ-K17 닫음(줄 620) · SPEC-003 개정 ⑱(줄 72) · U-? 행(줄 234 · 748)
- 앱 화면 = 「이메일 또는 비밀번호가 맞지 않습니다 (KOS 계정과 같습니다)」(`copy.dart:7`) — 원인 오안내 알고 감수.
- 데모 계정: dev 의 401 을 prod 가 그대로 넘김(SPEC-001 「앱 환경 연결」 규칙 9 · 줄 366).

**웹 기기 선택이 쓰는 것**(웹 전용 · JSON 아님)
- 경로: `POST /login` → service `auth.login(device_choice=True)` 가 막히면 `PendingDeviceChoiceData` → HTML 조각. 제출 `POST /login/device`(폼 `pending_token` · `device_id`) → `auth.choose_device` → 해제 → sign-in 다시 → `login` 과 같은 갈래(세션 · 병원 고르기 · 다시 막히면 새 목록) — `dev:backend/day/routers/login.py:146-152,207-229` · `services/auth.py:405-482`
- service 결과 모양: `{status:"choose_device", pending_token, expires_in_seconds(5분), devices:[{id, label, ip_address, signed_in_at}]}` — `dev:backend/day/dtos/auth.py:39-65` · SPEC-001 줄 296(「JSON 으로 내보내지 않음」)
- 임시 값 = 이메일 · 비밀번호 · 목록 id 를 **암호문**으로 Redis 5분 · 꺼내면 지움 · 종류 `kind="device"` 로 병원 고르기 토큰과 가름 — `services/auth.py:405-431,443-464` · SPEC-001 §3 「기기 선택 동안 비밀번호」(줄 420-424)
- 빈 · 목록 밖 `device_id` · 만료 · 다른 종류 토큰 = `session_expired`(웹은 `/login?reason=session_expired`) — `services/auth.py:448-464`
- 해제 4xx 는 그래도 sign-in 다시(OQ-K8 ①) · 목록 실패 · 빈 목록 = `kos_unavailable` 503(OQ-K12) — `services/auth.py:410-413,469-475`
- `label` = 서버가 KOS `userAgent` 를 「{OS} {브라우저}」로 읽음(못 읽으면 원문) — `services/auth.py:484-512`
- 웹 화면 글자(KOS 화면 그대로): 「이미 로그인 중인 기기가 있습니다」 · 「최대 5개 기기에서만 동시 로그인이 가능합니다.」 · 「아래 목록 중 로그아웃 시킬 기기를 선택해주세요.」 · 「{label} · {IP}」 · 「n분 전」/「방금 전」 · [계속하기] · 「처음으로」 없음 — `dev:backend/day/templates/partials/login_card.html:15-34` · SPEC-001 U-4(줄 103-110 · 166-170)

**앱이 그대로 쓸 수 있나 — 아니다.** 앱용 JSON 짝이 없다.
- `POST /api/auth/device` 는 의도적으로 뺐다(SPEC-001 줄 265 · OQ-K4 · OQ-K14).
- 앱 JSON 로그인 응답 타입에 기기 선택이 없다(`response_model=SignedIn | ChooseHospital` — `routers/api/auth.py:75-80`).
- 깔린 앱(0.1.0)과 새 앱을 서버가 **가려야** 한다 — 깔린 앱에 새 `status` 를 주면 `unexpected_response`(A2 #1). 가르는 방법은 미정(SPEC-001 OQ-K14 줄 630 「요청 칸 등」).
- 앱용으로 더 필요해 보이는 것(사실 나열 · 정하지 않음): ① 새 앱 표시(요청 칸 등) ② 앱 JSON 기기 선택 응답 모양 · 제출 경로 ③ 데모 넘김 경로(`environments.relay_login`)에도 같은 갈래 ④ 앱 화면 · 글자(웹은 KOS 화면 글자) ⑤ 앱 `Phase` 에 단계 하나 · 「처음으로」 여부(웹은 없음 — OQ-K10).
- 참고 사실: KOS 가 보는 UA 는 **DAY 서버의 UA**(KOS 웹 UA + ` (dev|prod|local)` 표시)라, 앱 · 웹으로 DAY 에 로그인한 세션은 목록에서 같은 「macOS Chrome · {서버 IP}」로 보인다 — 직원 폰인지 가릴 수 없다 — `dev:backend/day/emr/kos/client.py:10-20,53-65,93-101` · SPEC-001 OQ-K2 · OQ-K6. `(dev)` 표시를 보일지 글자 미정(kos-signin-limit 회고 §7).
- KOS 해제가 토큰을 즉시 막는지 = **확인 안 됨**(OQ-K11 줄 628).

### B3. DAY 로그아웃 때 KOS 세션 해제 — 앱 경로 포함 **안 된다**
- 앱 로그아웃: 기기 해제(`DELETE /api/devices/{id}`) → `POST /api/auth/logout` → 묶음 삭제 — `session_controller.dart`(logout · 파일 줄 384 근처) · `day_api.dart:128-140`
- 서버 `sessions.logout` = DAY 세션 `revoked_at` 만 · 「KOS 에 알리지 않는다」 — `dev:backend/day/services/sessions.py:80-92`
- 결정: 「로그아웃 때 해제 안 함 · 다시 로그인할 때 고르면 된다」(비밀번호가 없어 불가) — kos-signin-limit 회고 §2 · §4 · SPEC-001 규칙 15(줄 542)

---

## C. 시술 현황 탭

### C1. 웹 동작 전수 × 앱 — 서버 라우터를 다 셈
웹 라우트 = `dev:backend/day/routers/board.py`(grep `@router.` 17개 + task action 5개). 앱 JSON = `dev:backend/day/routers/api/board.py`(prefix `/api` · 15개). 앱 호출 = `dev:app/lib/state/board_controller.dart:150-170` · `board_stream.dart:92`.

| # | 웹 동작 | 웹 경로 | 앱 JSON 경로 | 앱이 부름? |
|---|---|---|---|---|
| 1 | 판 보기 | GET `/board` | GET `/api/board` | ○(SSE 스냅샷 · `/api/board/stream`) |
| 2 | **정렬 탭**(시술순 / 방별순 `?sort=room`) | GET `/board?sort=` | **없음**(api 에 `sort` 인자 없음) | ✗ |
| 3 | 고객 검색 | GET `/board/search` | GET `/api/board/search` | ✗(SPEC-003 뺌 · OQ-A30) |
| 4 | 차트 보기(방문) | GET `/board/visits/{id}/chart` | GET `/api/visits/{id}/chart` | ✗(앱은 스냅샷 노트 읽기만 — `chart_sheet.dart:1`) |
| 5 | 차트 저장 | POST `/board/tasks/{id}/chart` | POST `/api/tasks/{id}/chart` | ✗(OQ-A34) |
| 6 | 마취 시작 / 종료 | POST `/board/visits/{id}/anesthesia/{start\|end}` | 같은 꼴 `/api/…` | ○ |
| 7 | 의사 호출 | POST `/board/visits/{id}/calls` | POST `/api/visits/{id}/calls` | ○ |
| 8 | 재호출 | POST `/board/calls/{id}/recall` | POST `/api/calls/{id}/recall` | ○ |
| 9 | 수락(본인 · 대리) | POST `/board/calls/{id}/accept` | POST `/api/calls/{id}/accept` | ○(+ iOS 푸시 [수락] 네이티브) |
| 10 | 원장 바꾸기 | POST `/board/tasks/{id}/doctor` | POST `/api/tasks/{id}/doctor` | ✗(SPEC-003 뺌) |
| 11 | 방 옮기기 | POST `/board/visits/{id}/room-move` | POST `/api/visits/{id}/room-move` | ✗(SPEC-003 뺌) |
| 12 | 방 복귀 | POST `/board/visits/{id}/room-return` | POST `/api/visits/{id}/room-return` | ✗ |
| 13 | [시작] | POST `/board/tasks/{id}/start` | POST `/api/tasks/{id}/start` | ○ |
| 14 | **호출 취소** | POST `/board/tasks/{id}/cancel-call` | POST `/api/tasks/{id}/cancel-call` — **있음**(웹과 같은 `TASK_ACTIONS` 를 import) | ✗ |
| 15 | [종료] | POST `/board/tasks/{id}/finish` | 같은 꼴 | ○ |
| 16 | 시작 취소 | POST `/board/tasks/{id}/undo-start` | 같은 꼴 | ○(확인 창) |
| 17 | 완료 취소 | POST `/board/tasks/{id}/undo-finish` | 같은 꼴 | ○(확인 창) |
| 18 | 귀가 대기 | POST `/board/visits/{id}/home` | POST `/api/visits/{id}/home` | ○ |
| 19 | 순서 끌기 | PUT `/board/order` | PUT `/api/board/order` | ✗ |
| 20 | **바로 시작**(체크한 준비중 줄 · 집도의 없으면 시스템 계정) | POST `/board/visits/{id}/quick-start` | **없음** | ✗ |
| 21 | **귀가 대기 취소** | POST `/board/visits/{id}/undo-home` | **없음** | ✗ |

근거: `routers/board.py:246-640`(라우트) · `:544-549`(`TASK_ACTIONS` = start · cancel-call · finish · undo-start · undo-finish) · `routers/api/board.py:37,60,89-363` · 앱 `room_screen.dart:512-521,562-586`.
- 웹 ⋮ 메뉴(F-5): 호출 줄 → 「호출 취소」(확인 창 · 성공 토스트 없음) · 진행중 → 「시작 취소」 · 완료 → 「완료 취소」 · 준비중 ⋮ 없음 — `dev:backend/day/templates/partials/board_parts.html:117-126` · fix-feedback 회고 §4 F-5
- 웹 귀가 대기 탭 ⋮ 「귀가 대기 취소」(확인 창 · 성공 토스트 없음) — `board_parts.html:255,262-269`
- 웹 [바로 시작 · N건] = 액션바 버튼(N = 체크한 준비중 줄) — `board_parts.html:188-196`
- **스냅샷 쪽**: 호출 취소 · 바로 시작 · 귀가 대기 취소 가능 여부를 알리는 `can*` 칸이 **없다**(웹은 템플릿에서 줄 `state` 로 그림). 스냅샷 `can*` 전수 = `canCall · canEnd · canFinish · canHoldMove · canHome · canMoveRoom · canRecall · canReturnRoom · canStart · canUndoFinish · canUndoStart` + `systemDoctor`(presentation/schemas grep). 앱 규칙 「서버가 계산한 값만 쓴다」(AGENTS.md 「앱」 · SPEC-003 규칙 1 줄 827)와 부딪히는 자리 → §F.

### C2. 각 동작의 서버 API · 오류 코드 · 토스트 글자
| 동작 | 거절 코드(검사 순서) | 웹 토스트 | 앱 표에 있나 |
|---|---|---|---|
| 호출 취소 | `not_found` → `visit_home` → `call_already_accepted` → `task_not_called` | `task_not_called` = **미정(토스트 없음)** · 나머지 정해진 글자 · 성공 토스트 없음 | `task_not_called` 없음 |
| 바로 시작 | `invalid_request`(빈 · 중복 taskIds) · `not_found` · `visit_home` · 줄별 `call_not_accepted` · `task_not_waiting` · `conflict`(시스템 계정 KOS id 없음) — **일부만 성공 가능**: 응답에 `rejected:[{taskId, code}]` · `systemDoctorTaskIds` | `conflict` = 일반 거절 글자(미정 — fix-feedback 회고 §7) | `conflict` 없음 |
| 귀가 대기 취소 | `not_found` → `visit_not_home` · KOS `change-flow-step` outbox | `visit_not_home` = **미정(토스트 없음)** · 성공 토스트 없음 | 없음 |
| 정렬 탭 | — | 「시술대기 순」 · 「방별 순」(SPEC-002 개정 ㉓) | — |

근거: `dev:backend/day/policies/board_rules.py:640-665` · `dev:backend/day/services/board_calls.py:291-330` · `dev:backend/day/services/board_quick_start.py:37-125`(거절 `conflict` 줄 ~95 · 응답 `rejected` · `systemDoctorTaskIds`) · `dev:backend/day/services/board_home.py:23-60` · `board_messages.py:4-38` · 웹 `message_of`(`routers/board.py:600-607` — 표 밖 코드는 「요청이 올바르지 않습니다」).
- 앱 성공 토스트(프로토 원문)에 호출 취소 · 바로 시작 · 귀가 대기 취소 글자 없음 — `copy.dart:68-82`. 원천 없는 글자는 「미정」.
- 「간호관리」(시스템 계정 원장 칸 표시)는 웹만 · 앱은 `systemDoctor` 를 안 읽음(SPEC-002 개정 ㉒ E3 · fix-feedback 회고 §2).

### C3. 앱 화면 구조 vs 웹 · 시안 · 스펙
- 앱: 하단 3메뉴(시술현황 · 채팅 · 설정) · 시술현황 = **카드 목록 + 인박스 칸 칩**(인박스 탭 · 호출 탭 · 시술 완료 탭 없음) → 카드 누르면 룸 상세(시술 줄 · [시작] [종료] · ⋮ 시작 취소 / 완료 취소 · 의사 호출 · 재호출 · 수락 · 마취 · 귀가 대기) — SPEC-003 범위 표(줄 96-115) · 개정 ⑤ · ⑮ · `dev:app/lib/ui/board_screen.dart` · `room_screen.dart`
- 웹: 판 + 인박스 나란히 · 정렬 탭 · 카드 안 체크박스 + 액션바([의사 호출 · N건] [바로 시작 · N건]) · 줄마다 ⋮ · 귀가 대기 탭 ⋮ — `board_parts.html`
- **시안: 없다.** mediness `products/day/21-screen/` · `21-html/` 둘 다 빈 폴더(`.gitkeep` 만). SPEC-003 은 「프로토(cc-prototype `procedure/app`) 디자인 유지 · DAY 색」(줄 29-33). 앱에 「귀가 대기 탭」 · 「선택 체크」가 지금 없음 → 웹 꼴을 그대로 옮길 자리가 앱에 없는 동작이 있다(바로 시작의 다중 선택 · 귀가 대기 취소의 목록 자리).
- SPEC-003 개정 ⑰(줄 70): F-1 ~ F-7 은 「앱 코드 무수정」으로 연결만 해 둠.

---

## D. 호출 취소 알림

### D1. 지금 notification_kind · 호출 취소 때 서버 · 푸시 경로
| 층 | 값 | 근거 |
|---|---|---|
| DB enum `notification_kind` | `doctor_call` · `counselor_call`(상담사 호출 — 미사용 · 향후) | `dev:backend/migrations/versions/20261105_0002_data_model_first_data_model.py:80` · `dev:backend/day/enums/notification.py:4-6` |
| DB enum `push_kind` | `doctor_call` · `counselor_call` · `display` · `chat` | 같은 migration `:97` · `enums/notification.py:9-13` |
| `notification_setting.kind` | 문자열 칸(enum 아님) — `doctor_call` · `chat` | SPEC-005 줄 444 |
| 앱 | 그리는 종류 `{'doctor_call'}` · 설정 이름 `{doctor_call, chat}` | `notification_model.dart:13,16` |

- **호출 취소 때 서버**: 그 줄 `doctor_call_task.deleted_at` · 받을 시술이 안 남으면 `doctor_call.closed_at`. **알림 행 · 푸시 · KOS 쓰기 없음**(DAY 만) — `dev:backend/day/services/board_calls.py:291-330` · SPEC-002 규칙 38(줄 280 · 1074) · SPEC-005 줄 261-263.
- **푸시 경로**: iOS = APNs(`adapters/apns.py`) · 원장 호출 payload `{aps{alert,sound,category:"CALL"(수락 가능자만)}, kind:"doctor_call", environment, hospitalId, visitId, callId}` — `dev:backend/day/services/notifications.py:488-498`. dev 서버 → DAY Dev · prod 서버 → 정식 앱만(M-20 안 함 — mobile-deployment 줄 18 · 341). **Android = FCM 없음**(채널 스텁 · M-9) — `PushChannel.kt` · mobile-deployment §1 줄 41 · android-app 회고 §7.

### D2. 새 종류 추가에 필요한 것 · 옛 앱이 받으면
필요해 보이는 것(SPEC-005 OQ-N14 ⓐ ~ ⓕ 가 정본 목록 — 줄 433):
1. DB enum `notification_kind` 값 추가 = migration(값은 더하면 못 뺌) · 푸시까지면 `push_kind` 도 — SPEC-005 줄 444 · fix-feedback 회고 §2
2. 알림 행 `title` · `body` NOT NULL — 글자 미정(OQ-N14 ⓑ)
3. 받는 계정 · 설정 줄 · 원래 호출 알림 행을 닫을지(ⓐ · ⓕ)
4. 앱: `notifKinds` · `notifKindName` · 푸시 탭 분기(`push_coordinator.dart:205`) · iOS 앞화면 처리(`AppDelegate.swift:109-130` · `AcceptLogic.swift:149-168` tapKeys) · 종 배지
5. `unread` 를 앱이 아는 종류만 셀지(ⓓ) — 지금 서버는 종류 무관(`notifications.py:106-120`)
6. 웹 OS 알림(ⓔ) — 지금 웹은 원장 호출 행만 띄움(SPEC-005 줄 159)

**옛 앱(0.1.0)이 새 종류를 받으면**: 목록에서 버림 · 배지는 셈(어긋남) · 설정 줄 안 보임 · iOS 푸시는 배너 · 소리 뜨고 눌러도 이동 없음 · Android 는 푸시 자체 없음 — A2 #8 ~ #11. 「앱 업데이트 뒤」의 「뒤」가 무엇인지(새 앱 출시 즉시 / 옛 앱 비율) 정해진 것 없음 → §F.

---

## E. 통역

### E1. DAY 통역 지금 구현 · 이식 시점
- 이식 원천: **interpret-pwa `origin/main` `17c26b5`**(#10 — 사전 `.6` · 통역 기록(서버만) · 언어별 한도) — `dev:backend/day/services/interpret/__init__.py:1` · `session.py:3` · `adapters/soniox.py:3`. 이식 = CENTURION_DAY #242(`7b099e8f` · 2026-11-11). 그 뒤 dev 의 통역 관련 커밋은 리팩토링 3개뿐(`f36c5a1f` · `3752c6c4` · `540062ff` — `git log origin/dev -- <통역 경로>`).
- 서버: WS `/api/interpret`(`routers/api/interpret.py`) · 세션 `services/interpret/session.py` · 조립 `policies/interpret/{assembler,languages,chinese}.py` · 사전 `policies/glossary.py` · `bootstrap/{interpret,glossary}.py` · Soniox `adapters/soniox.py`
- Soniox 설정: **STT `stt-rt-v5`** · TTS `tts-rt-v2` · `max_endpoint_delay_ms` 1000 — `adapters/soniox.py:29-32,64-80`
- 사전: `backend/day/seed/glossary.json` **version `2026-10-27.6`** · 170 term · 7언어
- 통역 기록(records) **옮기지 않음**(OQ-A39) — `session.py:11`
- 동시 세션 상한 `DAY_INTERPRET_MAX_SESSIONS` 기본 **6**(1~50) · dev · prod env 미설정(코드 기본값) — `dev:backend/common/config.py:184` · `dev:deploy/config/{dev,prod}.env:38-39`
- 앱: `interpret_client.dart`(프로토 반이중 — 재생 중 + 400ms 마이크 안 보냄 · `{start, pause, resume, stop}` · 서버 `{ready, caption, audio_start, PCM, audio_end, error}`) · `interpret_controller.dart` · `interpret_widgets.dart`(대화 통역 · 빠른 말하기 = 기기 TTS) — `interpret_client.dart:1-7` · SPEC-003 줄 453. 누르고 말하기(통키 D-36) · 언어 고르기 오버레이(D-34)는 PWA 화면 기능이라 앱에 없음(grep `ptt` 0).

### E2. 통키 `17c26b5` 뒤 바뀐 것 전수(`git log 17c26b5..56e43a0` = 5커밋)
| 커밋 | DEC | 무엇 | DAY 에 맞나(사실만) |
|---|---|---|---|
| `e0fbda8` #11 | D-42 | 통역 기록 보관 기간 env | **DAY 는 기록이 없다**(OQ-A39) — 대상 아님으로 보임 |
| `6d57ba3` #12 | D-43 ~ D-66 | STT **v6**(v5 는 **2026-12-15 제거** — D-43) · 역할 context 문안(D-45 · D-49) · 빈 원문 막기(D-48) · 언어별 context 한도 재측정(D-56) · 시드 `.7` ~ `.10`(D-46 · D-51 ~ D-53 · D-60 ~ D-63) · **번역 뒤 시술명 바로잡기** `correct.py`(D-58 · D-63 ~ D-66) | 서버 이식 후보. 단 `correct.py` 가 `app.service.records`(`_norm · _spans · hays_of · match_spans`)를 import — DAY 는 records 를 안 옮겨 그 함수가 없음(`tk:back/app/service/interpret/correct.py:17`). 품질 스크립트(`scripts/quality_check.py` 등)는 통키 운영 도구 |
| `fe375ad` #13 | D-67 | `max_endpoint_delay_ms` 2000 · `endpoint_sensitivity` -0.3 | 서버 설정만 — 후보 |
| `c7a582f` #14 | D-68 ~ D-70 | **세 참여자**: 차례 끝(서버 시계 1초)에만 TTS · 재생 중에도 듣기(반이중 걷음) · 반대 언어 끼어들면 `audio_stop` · 클라이언트 `playback_stopped` · Soniox agent text(v6 만) · `turn.py` 신규 | **서버 + 클라이언트 둘 다 바뀜.** 앱은 반이중이라 그대로면 끼어들기가 안 일어남 · `audio_stop` 무시 · `playback_stopped` 안 보냄(A2 #13 · #14). 옛 앱 + 새 서버 동작은 **확인 안 됨** |
| `56e43a0` #15 | D-71 | Soniox context = 고유명사 74개 · 정방향 + 역방향만 · 시드 `.11` | 서버 후보. **시드 `.11` 은 DAY 로더가 거절** — term 칸 `proper` · entry 칸 `wrong` 이 DAY 허용 키에 없어 `SeedError("unknown_field")`(`dev:backend/day/policies/glossary.py:39-55,83-92`) |

- PWA 전용으로 보이는 것: 데모 원탭 로그인(#2) · 시작 오버레이 언어 단추(D-34) · 누르고 말하기(D-36) · 용어집 API 삭제(D-37) · 통역 기록 · 보관(D-42) — 모두 `17c26b5` 이전이거나 records 계열.
- 통키 SPEC 버전 · 회고: `para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md`(0.9.5 까지 · D 대응표 줄 2663~) · 회고 `log/2026-11-16-tongky-quality-re1.md` · `log/2026-11-16-interpreter-idea.md`
- DAY 쪽 OQ: 시드 다시 가져오기 = 「고칠 때마다 사람이 PR 로」(SPEC-003 OQ-A41 줄 1028) · 사전 전 병원 한 벌(OQ-A45).

### E3. Soniox 한도
- 사실(2026-11-11 코디 API 조회): 조직 전체 **STT 10 · TTS 3** · 프로젝트 한도 없음 · DAY 상한 6 > TTS 3 · 통키와 같은 조직 — `orchestration/work/_archive/day/fix/_RESUME.md:38` · fix 회고 §7(줄 115) · 개념 `websocket-relay`
- 그 뒤 바뀐 기록 **없음**(profile · 아카이브 grep). 지금 한도 값 = **확인 안 됨**(이 조사는 실호출 금지).
- 관련 열린 것: OQ-A43(상한 찼을 때 글자 — 키 없음과 같은 글자) · OQ-A46(수명 · 무활동 상한 없음) — SPEC-003 줄 1036-1037.
- 통키 D-68 이후 TTS 를 차례 끝에만 여는지 · 세션 내내 쥐는지에 따라 TTS 3 의 무게가 달라짐 — **확인 안 됨**.

---

## F. 정할 것 (사용자 · 스펙 몫 — 추천은 한 줄)

1. **버전 이름 · 빌드 번호** — 다음 판을 0.1.0 으로 둘지 올릴지 · 빌드 번호 규칙(M-13). 최소값은 A1(iOS Dev 4 · iOS 정식 3 · Android 둘 다 4).
2. **iOS 0.1.0 (2) 심사 중 새 빌드** — 심사 결과 전 올릴 때 정식 앱 버전 이름 · 심사 대기 빌드 처리(빼고 바꿀지). Apple 규칙은 이 조사에서 공식 문서와 대조 안 함.
3. **새 앱 · 깔린 앱 가르기 방법**(SPEC-001 OQ-K14) — 요청 칸(예 `client` 값 · 앱 버전 칸) 등. 기기 선택 · 새 알림 종류 · 통역 프로토콜 셋 다 이 답에 걸린다. 추천: 한 가지 방법을 세 범위에 같이 쓴다.
4. **앱 기기 선택 JSON 계약** — 응답 모양(웹 service 결과 재사용 여부) · 제출 경로 이름(`POST /api/auth/device` 제안 있었음) · 데모 넘김 경로 포함 여부 · 「처음으로」(웹 없음).
5. **앱 기기 선택 화면 · 글자** — 웹은 KOS 화면 글자 · 시안 없음. 같은 글자를 쓸지. `(dev)` 표시 보일지(글자 미정).
6. **시술 현황 앱 범위** — 바로 시작 · 호출 취소 · 귀가 대기 취소 외에 정렬 탭 · 「간호관리」 표시 · 순서 끌기 · 차트 작성 · 방 이동 · 원장 바꾸기를 넣을지(SPEC-003 「뺌」 표 · OQ-A30 · OQ-A34).
7. **API 공백** — 바로 시작 · 귀가 대기 취소 JSON 경로 없음 · 정렬 `sort` 인자 없음. 만들지 · 이름.
8. **가능 여부 칸** — 호출 취소 · 바로 시작 · 귀가 대기 취소의 `can*` 가 스냅샷에 없음. 서버 계산 칸을 더할지(앱 규칙 「서버 값만」) / 앱이 `state` 로 그릴지.
9. **앱 화면 자리** — 바로 시작의 다중 선택 · 귀가 대기 취소 목록(앱에 귀가 대기 탭 없음) · 시안 필요 여부(21-screen 비어 있음).
10. **토스트 글자** — `task_not_called` · `visit_not_home` · `conflict` 미정(웹은 비움/일반 글자) · 앱 성공 토스트 원천 없음(호출 취소 · 바로 시작 · 귀가 대기 취소).
11. **호출 취소 알림**(SPEC-005 OQ-N14 ⓐ ~ ⓕ) — 종류 이름 · 받는 계정 · 제목 · 본문 · 앱 푸시 · `unread` 셈(앱이 아는 종류만?) · 원래 호출 알림 닫기 · 웹 OS 알림.
12. **「앱 업데이트 뒤」의 시점** — 새 앱 출시 즉시 서버를 바꿀지 / 옛 앱이 남는 동안 배지 어긋남을 감수할지(A2 #8).
13. **Android 푸시(FCM)** — 호출 취소 푸시 · 원장 호출 푸시 모두 Android 엔 없음(M-9). 이번 범위인지.
14. **통역 이식 범위** — 통키 5커밋 중 어디까지(STT v6 는 2026-12-15 v5 제거 때문에 기한 있음 — 추천: 최소 v6 는 이번에). 세 참여자(D-68 ~ D-70)는 앱 클라이언트까지 바뀌어야 함.
15. **바로잡기(D-58) 이식 방식** — records 함수 의존(`correct.py:17`). DAY 는 기록 없음 — 함수만 가져올지.
16. **시드 `.11` 가져오기** — DAY 로더 허용 키(`proper` · `wrong`)를 넓혀야 로드됨.
17. **Soniox 동시 상한** — TTS 3 vs 상한 6(fix 회고 §7 · OQ-A43 · OQ-A46). 지금 한도 재조회 · 상향 요청 · 상한 3 중 무엇.
18. **옛 앱 + 새 통역 서버** — 반이중 앱이 세 참여자 서버에 붙을 때의 동작(확인 안 됨) · 버전 가르기(3번)로 서버가 옛 동작을 유지할지.

## 확인 안 됨 (이 조사에서 못 본 것)
- KOS 해제가 토큰을 즉시 막는지(OQ-K11)
- 지금 Soniox 조직 한도 값(실호출 금지)
- 옛 반이중 앱 + D-68 서버 실동작
- Apple 심사 대기 중 새 빌드 · 버전 규칙(공식 문서 미대조)
- 통키 D-68 이후 세션당 TTS 연결 수명
