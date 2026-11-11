# 조사 — 기존 알림 · 푸시 이식 범위 / 직원 채팅 원천 (task_3756c85e0825 · ctx_2c871d04b209)

read-only 조사. 코드 · SPEC · 서버 · 기기 · DB 쓰기 0, 커밋 0. 테스트 · 빌드 · 기기 조작 0.
실행한 쓰기는 `git fetch origin dev`(CENTURION_DAY)와 `git fetch origin main`(spec tree) 두 번뿐이다. 둘 다 remote-tracking ref 만 갱신했다.

## 결론(짧게)

1. **직원 채팅 원천은 있다.** 프로토 `cc-prototype` **`origin/main` `77173cf`**(로컬 체크아웃 `dbf0b53` 에는 없음)에 들어 있다. PR #17 internal-chat · #18 forward · #19 invite 가 머지되어 있다.
   - 앱: `lib/chat/*` 8개 · `screens/chat_*` 9개 · 5번째 탭 「채팅」.
   - 서버: `/api/chat` 20개 경로 · 채팅 푸시 · SSE.
   - 채팅 SPEC(프로토 SPEC-007 internal-chat)은 보관 작업 기록이 경로를 가리킨다. 그 파일은 지금 경로에 없다(**미확인**).
   - `kknaks_profile/cc-2ck/app/back/dto/chat.py` 는 다른 서비스 코드다. 직원 채팅으로 보지 않았다.
2. **알림 디자인 · 앱 푸시 코드는 프로토에 있다.**
   - 디자인: 종 · 배지 99+ · 알림 목록 · 읽음 / 모두 읽음 · 역할별 알림 설정 · 폰 전체 화면 / iPad 오른쪽 시트.
   - 앱 푸시: iOS APNs 직접 · Firebase 0 · **Android 폴더 없음**.
3. **DAY 앱 현재** = iOS APNs 직접 등록 · 해제 · 원장 호출 알림 수락만 있다(Firebase 0 · `app/android` 없음 → Android 푸시 미구현). 알림 목록 · 배지 · 설정 · 채팅 화면은 없다(종만).
4. **DAY 서버(dev `91728737` · 앱 브랜치 `b6c034bf` · 옆 `day-procedure-board-2` `caa72435`) = 테이블만 있다.**
   - 있는 테이블: `device` · `notification` · `notification_setting` · `push_log` · `chat_room` · `chat_member` · `chat_message` · `chat_attachment`(모델 · migration).
   - 그 밖은 **모두 없다**: 기기 등록 API, APNs/FCM 발송, 알림 목록 · 미읽음 · 읽음 · 설정 API, 알림 · 채팅 실시간, 채팅 API, 권한 키(`chat`/`notification`).

## 1. 프로토 알림 · 푸시(실제 파일:줄 · ref `origin/main 77173cf`, 경로 `procedure/app/lib/…`)

| 무엇 | 근거 | 이식 때 |
|---|---|---|
| 종 + 미읽음 배지(0 이면 없음 · 99+) → 알림 목록 | `widgets/header.dart:107-137` · `app_state.dart:79` `unread` · `:102-108` SSE `notification {unread}` | 모양 그대로 가능 · **서버 미읽음 API · 실시간 이벤트가 DAY 에 없음**(D-5) |
| 알림 목록 — 폰 전체 화면([‹ 닫기] · 「알림」 · [모두 읽음]) · iPad 오른쪽 시트 420 | `screens/shell.dart:321-335` · `screens/notifications_screen.dart:1-2 · 73-95` · 빈 글자 `:89` | 모양 그대로 · 문구 원문 사용 |
| 행 = 제목 · 시각 · 본문 · 안 읽음 파란 바탕 · 누르면 읽음 → 그 화면 | `notifications_screen.dart:109-137` · 읽음 `:53` 모두 / `:61` 하나 | 대상 화면(룸 상세 · 예약)은 DAY 범위 따라 |
| 종류 = `doctor_call` · `counselor_call` 둘만(목록에서 나머지 버림) | `model/notification.dart:8 · 46-57 · 62` | DAY 데이터 모델 `notification.kind` 도 같은 둘(SPEC-000 :965) |
| 알림 설정 = 역할이 받는 종류만 스위치 · 알림 꺼짐 안내 · 기기 이름 | `screens/settings_screen.dart:1 · 39 · 53 · 102-121` | DAY 설정 탭은 지금 계정 · 로그아웃만 — 사용자 결정 필요 |
| 앱 푸시 = APNs 직접 · Firebase 0 · 채널 `procedure/push` | `push/push.dart:1 · 12 · 64-111` | DAY 는 같은 방식(채널 `day/push`)으로 이미 구현 |
| 푸시 종류 = 원장 호출 · 상담사 호출 · 띄우기 · 채팅 | `push/push.dart:12-50` · 서버 `back/app/service/push.py:59` | DAY 는 원장 호출만 구현 · 나머지는 서버 · 앱 둘 다 없음 |
| 알림에서 바로 수락(CALL 카테고리) · 채팅은 앞에서 받으면 앱 안 배너 | `ios/Runner/AppDelegate.swift:11 · 28-31 · 144-162` | DAY 도 수락 카테고리 있음 · 채팅 배너는 없음 |
| 받는 사람 = 관리자 + 원장(전체/지정) · 의사만 CALL 카테고리 · 호출한 원장 제외 | `back/app/service/push.py:9-10 · 114-135` | **DAY 결정과 다름**: 사용자 2026-11-09 「호출 대상 그대로 · 관리자 추가 · 호출자 제외 없음」(SPEC-003 U-14) |
| 서버 APNs 발송 = httpx http2 · ES256 JWT(팀 · 키 id) | `back/app/push/apns.py:12-44` | DAY 서버에 없음 · 키는 서버 비밀(사용자) |
| Android | `procedure/app` 아래 `android` 폴더 없음 · firebase 문자열 0 | 프로토도 iOS 만 |

## 2. 프로토 채팅(직원 내부 채팅 · ref `origin/main 77173cf`)

- **앱**: `lib/chat/{chat_link,chat_model,chat_search,chat_state,chat_ui,chat_view,photo_pick,video_pick}.dart` · `screens/chat_{list,room,info,new,attach_sheet,forward_sheet,media,photo,video}_screen.dart` · 셸 5번째 탭 「채팅」 · 안 읽은 방 수 배지 · 앱 안 배너(`screens/shell.dart:2 · 19-31 · 104`) · 테스트 `test/chat_app1~7_test.dart`.
- **서버**: `back/app/api/chat.py:39` `prefix=/api/chat`. 경로는 아래와 같다(`:49-195`).
  - 사람 · 방 목록 · 1:1 방 · 그룹 방 · 멤버 추가 · 나가기 · 숨기기 · 알림 끄기
  - 메시지 목록 · 첨부 · 보내기 · 수정 · 삭제 · 전달 · 읽음
  - 사진 · 동영상 올리기 · 받기 · 썸네일
- **실시간 · 푸시**: SSE 이벤트(`service/chat.py:166-172`) · 채팅 푸시(`service/push.py:176-195` · `thread-id` · kind `chat`).
- **권한 · 범위 (이식 때 바꿀 곳)**
  - 프로토 상대 후보 = 「active + 비밀번호 있는 계정」 전체(`service/chat.py:53-55 · 200-205`). 병원 격리 · 권한 키가 없다.
  - DAY 는 KOS 계정 로그인이다(로컬 비밀번호 없음). 테이블은 `chat_room.hospital_id` 가 있어 병원 격리 모양을 갖췄다(SPEC-000 :1059-1064).
  - 따라서 상대 후보 · 권한 · 병원 범위는 DAY 규칙으로 새로 정해야 한다(사용자 결정).
- **원천 문서**
  - 보관 작업 기록: `kknaks_profile/day/orchestration/work/_archive/cc-prototype/internal-chat/`(브리프 · 리포트).
  - 그 기록이 가리키는 `…/cc-prototype/20-spec/spec-007-internal-chat.md` 는 현재 경로에 없다 → **채팅 SPEC 원문 미확인**.
  - 사용자가 말한 「기존 채팅」이 이 프로토 채팅인지 코디 확인이 필요하다(추측 금지).

## 3. DAY 앱 현재 푸시(`day-app` HEAD `b6c034bf`)

| 무엇 | 근거 |
|---|---|
| 채널 `day/push` — ready · requestPermission · register · installId · appId · appName / onToken · onTap | `app/lib/data/push_bridge.dart:33-70` · `ios/Runner/AppDelegate.swift:9-16 · 45` |
| 권한 요청 → APNs 등록 · 토큰 수신 | `AppDelegate.swift:63-73 · 89` |
| 기기 등록 `PUT {세션 api_base_url}/api/devices/{install_id}` {push_token · platform · app_id · push_env · kind} · 해제 `DELETE` · 토큰 바뀌면 다시 | `app/lib/state/push_coordinator.dart:3 · 82-126` |
| 알림에서 바로 수락(카테고리 · 「수락」) — 네이티브가 세션 묶음 Bearer 로 `POST /api/calls/{id}/accept` | `AppDelegate.swift:16 · 31-33` |
| 누른 알림 = `kind == doctor_call` 만 처리 | `push_coordinator.dart:164` |
| 세션 · 환경 격리(세션 origin 으로만 · 다른 environment 알림 무시) | SPEC-003 §3 「푸시」 · 기존 테스트 |
| `aps-environment` = development(배포 서명이 바꿈) | `ios/Runner/Runner.entitlements:5-6` |
| Firebase · FCM | 없음(코드 · pubspec 검색 0) |
| Android | **`app/android` 폴더 없음 — Android 푸시 미구현**(빌드 대상조차 없음) |
| 알림 목록 · 배지 · 알림 설정 · 채팅 화면 | 없음 — 종만(U-2 · D-5) · 채팅 탭은 빈 자리(OQ-A18) |

## 4. DAY 서버 · 계약

| 범위 | 기기 등록 API | APNs/FCM 발송 | 알림 목록 · 미읽음 · 읽음 · 설정 API | 알림 · 채팅 실시간 | 채팅 API | 테이블 |
|---|---|---|---|---|---|---|
| `origin/dev` `917287374723871d554f8a094610d46c39450534`(오늘 fetch · remote 와 같음) | 없음 | 없음 | 없음 | 없음 | 없음 | 있음(`backend/day/models/misc.py:58-105 · 192-260` · migration `20261105_0002`) |
| 앱 브랜치 `b6c034bf` | 없음 | 없음 | 없음 | 없음 | 없음 | 같음 |
| 옆 tree `day-procedure-board-2` HEAD `caa7243514f1f43fd7ab691e60145ebdf9aef663`(clean · remote 와 같음) | 없음 | 없음 | 없음 | 없음 | 없음 | 같음 |

- 위 표의 「있음」 검색은 `backend` 전체 대상이다. 패턴은 `/api/devices` · `/api/notifications` · `/api/chat` · `apns` · `firebase` 이다. 잡힌 파일은 모델 · migration · 컬럼 · 암호화 테스트뿐이다. routers · services · tasks 에서는 해당 모델을 쓰지 않는다.
- enum 에는 `PushKind`(doctor_call · counselor_call · display · chat) · `NotificationKind`(doctor_call · counselor_call)가 있다(`enums/misc.py`). 쓰는 코드는 없다.
- 권한 키는 `board` · `board.accept` 둘뿐이다(`services/default_permissions.py:35-36 · 51-53`). 채팅 · 알림 권한 키는 없다.
- SPEC
  - main `9692e1fb`(오늘 fetch): SPEC-000 07 「알림 · 접수 · 채팅」 데이터 모델만 있다(`:927-988 · 1059-…` · 법적 검토 DAY-ESC-001 `:942`).
  - `mobile-deployment.md`: 「서버가 APNs 직접 · Android 는 FCM 후보 · Android 착수 미결」(`:30-36 · 52-74`).
  - SPEC-003(브랜치 `06239a1c` · main 미머지)이 정한 것
    - 기기 등록 계약은 제안이다(D-2 서버 미구현).
    - 알림 목록 · 미읽음 계약은 없다(D-5).
    - 채팅은 자리만 있다.
  - 채팅 API 계약은 어느 DAY SPEC 에도 없다.

## 5. 앱 토큰 받기 vs 서버 발송 vs 플랫폼 등록 (구분)

| 층 | iOS | Android | 지금 DAY |
|---|---|---|---|
| 앱이 토큰 받기 | APNs 등록(OS) — 구현됨 | FCM SDK 필요 — **없음**(android 폴더도 없음) | iOS 만 |
| 서버에 토큰 전달 | `PUT /api/devices/{install_id}` — 앱 구현 · **서버 없음**(D-2) | 같은 계약에 `platform` 확장 필요(지금 `ios` 하나) | 앱만 |
| 서버 발송 | APNs 직접(키 = 서버 비밀) — **없음** | FCM HTTP v1(서비스 계정) — **없음** | 0 |
| 플랫폼 등록 · 설정 | Apple App ID · Push capability · APNs 키(사용자) | Firebase 프로젝트 · `google-services.json`(클라이언트 설정 · 발송 자격증명과 다름) · 서명 키(사용자) | 미등록 |

- 선택지 두 가지는 **결정하지 않았다**.
  - FCM 으로 iOS · Android 통일 — iOS FCM 도 APNs 키 · 설정이 필요하다.
  - iOS APNs 직접 + Android FCM — 지금 DAY 구현과 mobile-deployment 방향이다.
- FCM 토큰 · 식별 방식은 전환 안내가 있다. SDK 를 정할 때 Firebase 공식 문서(get-started · manage-tokens)의 현행 내용으로 다시 검증해야 한다. 버전은 지정하지 않았다.

## 6. 정리 — 그대로 / 바꿀 것 / 없는 것 / 결정

- **그대로 가져올 수 있는 디자인**(프로토 원형 + DAY 색)
  - 종 배지
  - 알림 목록(폰 전체 · iPad 시트 · 모두 읽음 · 행 모양 · 빈 글자)
  - 알림 설정 스위치 행
  - 채팅 화면 묶음: 방 목록 · 대화 · 입력줄 · 첨부 시트 · 전달 · 정보 · 사진 · 동영상 · 앱 안 배너 · 탭 배지
- **DAY 에 맞춰 바꿀 것**
  - id: 정수 → uuid
  - 로그인 · 계정: 비밀번호 계정 → KOS 세션 · staff · 병원 격리
  - 받는 사람 규칙: 관리자 추가 · 호출자 제외 → 호출 대상 그대로(사용자 2026-11-09)
  - 권한 키: `board`/`board.accept` 외 채팅 · 알림 키 없음
  - 세션 `api_base_url` 환경 격리
  - 푸시 payload 에 `environment`
  - 셸: DAY 4메뉴 「채팅」 자리 사용(프로토 5탭 아님)
- **서버에 없는 기능**(앱만으로 불가)
  - 기기 등록 API
  - APNs · FCM 발송
  - 알림 목록 · 미읽음 · 읽음 · 설정 API
  - 알림 · 채팅 실시간 이벤트
  - 채팅 API 20개 · 사진 · 동영상 저장
  - 권한 키
- **사용자 결정 필요**
  - 「기존 채팅」 = 프로토 `origin/main` 채팅이 맞는지 · 그 SPEC 원문 위치
  - 채팅 상대 범위 · 권한(누가 누구와 · 병원 안 전체인지)
  - 알림 종류 범위(원장 호출만 · 상담사 호출 · 채팅 알림 포함 여부)
  - 설정 탭 알림 스위치 · 기기 이름 포함 여부
  - Android 착수 시점과 FCM 통일 / APNs 직접 + FCM
  - 사진 · 동영상 저장소와 보관 · 법적 검토(DAY-ESC-001)
  - Apple · Firebase 등록 · 키(사용자)
