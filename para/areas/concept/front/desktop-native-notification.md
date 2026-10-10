---
type: concept
id: desktop-native-notification
title: 데스크톱 OS 알림을 셸이 네이티브 API 로 직접 띄우기
aliases:
  - OS 알림
  - 데스크톱 알림
  - 시스템 알림
  - UNUserNotificationCenter
  - tauri-plugin-notification
  - 알림 클릭
  - 알림 권한
up:
  - 2026-10-10-strong-hajin-notify
tags:
  - tauri
  - macos
  - 알림
  - webview
---

# 데스크톱 OS 알림을 셸이 네이티브 API 로 직접 띄우기

웹뷰 데스크톱 앱(Tauri)에서 OS 알림(배너)을 띄울 때 **웹은 사건을 받고, 셸(Rust)이 OS 의 알림 API 를 직접 불러 띄우는 것.** 웹 → 셸은 커맨드 둘(권한 묻기 · 띄우기), 셸 → 웹은 클릭 사건 하나다.

## 정의

1. **역할 가르기** — 웹이 실시간 채널(SSE)로 알림을 받고 「띄울지」 를 정한다. 셸은 띄우기와 클릭만 안다. 서버 푸시(APNs)가 없으므로 **앱이 켜져 있을 때만** 뜬다
2. **진짜 권한** — macOS 는 `UNUserNotificationCenter` 로 권한을 묻고(첫 요청 때 시스템 프롬프트), 거부 상태를 그대로 웹에 돌려준다
3. **클릭은 delegate 로** — 배너 클릭은 delegate 콜백으로 온다. 셸이 항목 id 를 웹 사건으로 넘기고 웹은 그 항목을 고른 상태까지 연다
4. **창이 없을 때의 클릭** — 트레이에 상주하는 앱은 창이 닫힌 상태에서 남은 배너가 눌릴 수 있다. 셸이 클릭을 잠깐(예: 60초) 보관했다가 웹이 준비됐다고 알리면 보낸다
5. **delegate 수명과 실행 환경** — delegate 객체를 앱 수명 동안 살려 둬야 콜백이 온다. 번들 id 가 없는 개발 실행(서명 안 된 바이너리)에서는 알림 센터가 없을 수 있다 — panic 없이 「지원 안 함」 으로 떨어진다

## 왜 중요한가

- **공식 플러그인이 데스크톱에서 반쪽일 수 있다** — Tauri 공식 알림 플러그인(2.5.1)은 데스크톱에서 클릭 응답을 버리고 권한을 늘 「허용」 으로 답한다(소스로 확인). 「클릭하면 그 항목이 열린다」 · 「거부하면 안내한다」 가 요구라면 플러그인으로는 안 된다
- 고를 수 있는 다른 길 — 폐기된 API(`NSUserNotification`) · 1인 유지 서드파티 플러그인 — 은 수명이 짧다. 네이티브 API 를 직접 부르는 코드(objc2)는 길지만 동작을 쥔다

## 경계와 오해

- **문서의 「지원」 ≠ 데스크톱에서 같은 동작** — 모바일 기준으로 쓰인 플러그인 API 가 데스크톱에서는 빈 구현일 수 있다. 소스를 열어 확인한다
- **OS 마다 길이 갈린다** — macOS 는 직접, Windows 는 공식 플러그인(클릭 없음)처럼 OS 별로 다른 구현이 섞인다. 한쪽을 위해 올린 의존성이 다른 쪽을 흔들 수 있다 → [[dependency-upgrade-regression]]
- **실측은 서명된 판으로만** — 알림 권한은 번들 id 와 서명에 묶인다. 개발 실행으로 본 결과는 사용자 앱과 다르다 → [[code-signing]] · [[dev-prod-parity]]
- 띄우는 수단과 얼마나 띄울지는 다른 문제다 → [[notification-coalescing]]

## 함께 보는 개념

- [[webview-attachment-download]] — 웹뷰가 못 하는 것을 셸이 가로채 하는 같은 모양
- [[rust-ownership-and-borrowing]] — delegate 수명을 Rust 쪽에서 쥐는 문제
- [[server-sent-events]] — 웹이 알림을 받는 채널
- [[code-signing]] — 권한 · 공증과 묶이는 번들 정체성

## 출처

- [[2026-10-10-strong-hajin-notify]] §2 — Strong Hajin WORK-013 WP4. P0 에서 공식 `tauri-plugin-notification` 2.5.1 이 데스크톱 클릭을 버리고 권한을 늘 허용으로 답함을 소스로 확인 → macOS `UNUserNotificationCenter` 를 objc2 로 직접(`notify_permission` · `notify_show`) · 클릭 60초 보관 중계 · Windows 는 공식 플러그인(`frontend/src-tauri/src/notify.rs` · `W/review-wp4-report.md`)
