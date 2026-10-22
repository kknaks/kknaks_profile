---
type: concept
id: apns-direct-push
title: APNs 직접 발송 — Firebase 없이 iOS 푸시와 알림 액션 (APNs Direct Push)
aliases:
  - APNs
  - 애플 푸시
  - iOS 푸시
  - 원장 호출 푸시
  - 알림 액션
  - 알림에서 바로 수락
  - notification action
  - UNNotificationCategory
  - DeviceTokenNotForTopic
  - push_log
up:
  - 2026-10-22-myeongdong-poc-v2
tags:
  - push
  - ios
  - 알림
  - 외부 연동
---

# APNs 직접 발송 — Firebase 없이 iOS 푸시와 알림 액션

iOS 만 받는 앱이면 서버가 **Apple Push Notification service(APNs)에 HTTP/2 로 직접** 보낸다. 중계 서비스(FCM) 없이 키 하나(`.p8`)와 그 키로 서명한 단명 JWT 가 전부다. 알림에 **카테고리**를 달면 잠금 화면 · 워치에서 앱을 열지 않고 버튼(액션)으로 조작까지 끝낼 수 있다.

## 정의

1. **인증 = 프로바이더 토큰** — `.p8` 키로 ES256 JWT(`kid` = 키 id · `iss` = 팀 id · `iat`)를 서명해 `authorization: bearer` 로 싣는다. Apple 은 20 ~ 60분 재사용을 요구한다 → 40분마다 새로. 키 · 팀 id 는 레포 밖(Secret)
2. **요청** — `POST https://api.push.apple.com/3/device/<기기 토큰>`(sandbox 는 `api.sandbox…`). 헤더 `apns-topic` = 번들 id · `apns-push-type: alert` · `apns-priority: 10` · `apns-expiration: 0`(늦게 닿을 호출은 의미 없음)
3. **기기 토큰은 앱이 등록한다** — 로그인 뒤 알림 권한 → `registerForRemoteNotifications` → 토큰을 서버에 등록(한 기기 = 마지막 로그인 계정) · 로그아웃 때 먼저 지운다
4. **죽은 토큰은 행을 지운다** — 410 은 늘, 400 은 `reason` 이 `BadDeviceToken` · `DeviceTokenNotForTopic` · `Unregistered` 일 때. 네트워크 · 5xx · 429 만 재시도 1회
5. **알림 액션** — payload `aps.category = "CALL"` + 앱이 시작 때 `UNNotificationCategory`(액션 `ACCEPT`)를 등록. 액션을 누르면 **네이티브 `AppDelegate` 가 키체인의 서버 주소 · 토큰으로 백그라운드 요청**을 보내고 결과를 로컬 알림 한 줄로 알린다 — 앱이 꺼져 있어도 된다
6. **발송 기록은 따로 쌓는다** — 조작 이벤트가 아니므로 `event_log` 가 아니라 `push_log`(받는 기기마다 1행 · 상태 · APNs 상태/이유 · 토큰 끝 6자리만)

## 사용 예시

```text
POST /3/device/<token>  (HTTP/2)
authorization: bearer <ES256 JWT, 40분 캐시>
apns-topic: <번들 id>      apns-push-type: alert
apns-priority: 10          apns-expiration: 0

{"aps":{"alert":{"title":"원장 호출","body":"<방> · 시술 2건 · 지정 호출"},
        "sound":"default","category":"CALL"},
 "visitId":…, "callId":…}
```

본문에 고객 이름 · 국적 · 시술 이름을 넣지 않는다 — 잠금 화면에 뜬다. 카테고리는 **그 호출을 수락할 수 있는 수신자(의사)** 에게만 단다. 관리자는 원장을 골라야 해서 액션 없이 앱을 연다.

## 왜 중요한가

- **의존 0 · 키 하나** — iOS 만이면 FCM 은 중계만 하나 더 끼는 셈이다. httpx(h2) + JWT 서명 라이브러리로 끝난다
- **「앱을 안 열고 처리」 가 현장 동선을 바꾼다** — 원장이 휴대폰 · 워치에서 바로 [수락]. 수락 출처(`X-Accept-Source: push | app | web`)를 이벤트에 남겨 어느 길로 처리됐는지 본다
- **토큰은 번들 id 에 묶인다** — 번들 id 를 바꾼 뒤 옛 토큰이 400 `DeviceTokenNotForTopic` 을 냈다. 지우지 않으면 매 호출마다 실패가 쌓인다

## 경계와 오해

- **액션은 Flutter 가 아니라 네이티브가 받는다** — 앱이 꺼져 있을 때 Dart 엔진은 없다. 그래서 토큰을 Flutter 저장소 말고 네이티브 키체인에도 따로 둔다(백그라운드에서 읽히는 접근 등급)
- **조용한 푸시가 아니다** — 보이는 알림만 쓰고 Background Modes(remote notifications)는 켜지 않았다. 액션 처리는 사용자가 누른 뒤의 백그라운드 작업이다
- **개발 빌드와 TestFlight 는 환경이 다르다** — `aps-environment` 가 development / production 으로 바뀌고 APNs 호스트도 sandbox / production 이다. 둘을 엇갈리면 토큰이 안 맞는다 → [[build-flavor]]
- **[[desktop-native-notification]] 과 다르다** — 그쪽은 앱이 이미 받은 것을 OS 알림으로 띄우는 것, 이쪽은 앱이 꺼져 있어도 OS 가 받는 원격 푸시다
- **[[jwt]] 의 다른 쓰임** — 사용자 세션이 아니라 서버 → Apple 의 프로바이더 인증이다. 매 요청 새로 서명하면 Apple 이 거절할 수 있다(너무 잦은 갱신)

## 함께 보는 개념

- [[jwt]] — 프로바이더 토큰의 형식
- [[desktop-native-notification]] — 데스크톱에서 OS 알림을 띄우는 다른 길
- [[notification-coalescing]] — 배너를 줄이는 쪽
- [[relationship-based-notification]] — 누구에게 보낼지를 관계로 정하는 것
- [[build-flavor]] — 번들 id · 환경이 토큰과 묶이는 이유
- [[delegated-authorization]] — 알림 [수락] 도 back 이 역할 · 원장을 다시 검사한다

## 출처

- [[2026-10-22-myeongdong-poc-v2]] §2 — 명동 PoC v2 원장 호출 푸시 · 알림 [수락](SPEC-004 §5-1 · `push/apns.py` · `service/push.py` · `api/actions.py` · `AppDelegate.swift`)
