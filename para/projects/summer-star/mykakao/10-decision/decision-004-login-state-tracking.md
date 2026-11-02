---
type: decision
id: MK-DEC-004
title: "로그인 상태 감지·재조정 방식 — 파일감시/프로세스wait + 세션 캐싱 + 트레이 메뉴"
status: accepted
product: mykakao
created_at: 2026-09-03
updated_at: 2026-09-03
tags:
  - product/mykakao
  - platform/windows
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-005-login-state-tracking]]"
  decisions:
    - "[[decision-003-windows-v2-approach]]"
  specs:
    - "[[spec-004-login-state-tracking]]"
  works: []
  releases: []
  related:
    - "[[baseline-004-offline-key-derivation]]"
up: []
---

# 로그인 상태 감지·재조정 방식

3상태 트래킹을 어떻게 감지하고, 무거운 작업을 어떻게 트리거하며, 상태를 어디에 보여줄지 정한다.

## Context

- 관련 baseline: [[baseline-005-login-state-tracking]]
- 결정 필요 이유: 감지를 폴링으로 하면 무겁고, 로그인/로그아웃을 프로세스 on/off 로만 보면 부정확. 신호·트리거·표시를 정해야 구현 가능.

## 결정 1 — 로그인/로그아웃 감지 신호

| Option | Pros | Cons | 판정 |
|---|---|---|---|
| A. 계정 DB(chatListInfo/TalkUserDB) **열림·잠금** + 키 회수 가능 | 깨끗·이미 파일 건드림 | 로그아웃 시 파일 close 동작 실측 필요 | **채택(주)** |
| B. 메인 윈도우 존재(main_hwnd) | 명확 | 윈도우 열거 필요 | 보조(교차검증) |
| C. 메모리 점유량 | — | WebView 로 출렁여 부정확 | 기각 |

- 채택 A(+B 교차검증). 로그아웃 시 DB close 여부는 **구현 중 실측 확인**(OQ-1).

## 결정 2 — 감지 방식: **이벤트 우선, 무거운 건 트리거로만**

| 대상 | 방식 |
|---|---|
| 로그인/로그아웃·방열림·새메시지 | **파일 감시(notify)** 를 계정 폴더까지 확장 — P2 인프라 재사용. 이벤트 |
| 카톡 종료(DOWN) | 프로세스 핸들 `WaitForSingleObject` — 즉시 |
| 카톡 시작(UP) | 가벼운 프로세스 존재 체크(수 초) 또는 WMI 시작 이벤트 |
| **무거운 harvest(키 회수)** | **로그인/방열림 이벤트가 뜰 때만** 실행. 절대 폴링 안 함 |

- 폴링은 프로세스 존재(밀리초, 쌈)만. 메모리 스캔은 이벤트 트리거 전용.

## 결정 3 — 속도: **세션 키 캐싱** (파생식 셸빙에 따른 대체)

- 파생식은 anti-debug+DPAPI 로 막힘([[baseline-004-offline-key-derivation]] spike4b) → 셸빙.
- 대신 **harvest 결과(후보/회수 키)를 세션 동안 캐싱**해 재조정 루프의 반복 harvest 를 피한다. 첫 회수만 느리고 이후 빠름.
- 키는 **RAM 에만**(디스크 저장 금지 — 안전규칙 유지).

## 결정 4 — 상태 표시: **트레이 우클릭 메뉴 + 웹 ①섹션**

- 트레이 메뉴(TrackPopupMenu, P3 재사용)에 live 상태:
  ```
  로그인 상태            (MF_GRAYED 헤더)
    로그인 유저 : <닉네임> (MF_GRAYED)
    상태 : 🟢 로그인/⚪ 로그아웃 (MF_GRAYED)
  ───
  환경설정               (클릭 → 웹페이지)
  ───
  종료
  ```
- 우클릭마다 메뉴 재생성 → 현재 상태 실시간 반영.
- dot: **이모지 우선**(🟢/⚪), 렌더 이상하면 오너드로우(WM_DRAWITEM).
- **본인 닉네임**: UserAccounts 로 본인 userId 특정 → TalkUserDB 닉네임 해석(신규 소작업).

## 결정 5 — 추적 방 영속: **기존 SQLite `room.selected` 재사용**

- P1 의 `room.selected`·`last_synced_id` 커서가 이미 영속 → 앱 재시작해도 추적 목록·진행 유지. 신규 저장소 불필요.

## Rationale

- 판단 기준: SAC 미건드림 · 무거운 건 이벤트로만 · 기존 인프라 재사용 · 키 RAM only.
- 리스크: 로그아웃 파일 신호 불확실(OQ-1), 파일감시 누락(주기 재동기 폴백), 방 닫힘 시 키 zeroize.

## Open Questions

| ID | Question | Next |
|---|---|---|
| OQ-1 | 로그아웃 시 계정 DB 가 실제로 close/unlock 되어 파일 이벤트가 뜨는가 | 구현 중 실측(사용자 로그아웃 협조 or 워커 확인) |
| OQ-2 | 카톡 시작 감지 = 프로세스 폴링 vs WMI 이벤트 | 구현에서 택 |
| OQ-3 | dot 이모지 렌더 품질 → 오너드로우 필요 여부 | 구현에서 실측 |
