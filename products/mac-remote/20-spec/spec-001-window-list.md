---
type: spec
id: MRT-SPEC-001
title: "창 목록 수집"
status: implemented
product: mac-remote
created_at: 2026-05-24
updated_at: 2026-06-01
tags:
  - product/mac-remote
  - doc/spec
  - status/implemented
links:
  baselines: []
  decisions:
    - "[[decision-002-cgwindowlist-window-source|MRT-DEC-002]]"
  specs: []
  works:
    - "[[work-001-cli-prototype|MRT-WORK-001]]"
    - "[[work-005-websocket-server|MRT-WORK-005]]"
  releases:
    - "[[release-001-v1-0-0|MRT-REL-001]]"
  related: []
---

# 창 목록 수집

Mac에서 현재 화면에 표시된 일반 창 목록을 수집한다. iOS 앱이 어떤 창이 열려 있는지 표시하고 전환할 수 있게 하는 기반 데이터.

> 원본: `mac-remote/doc/spec/Spec-01-window-list.md`. 결정 근거는 [[decision-002-cgwindowlist-window-source|MRT-DEC-002]].

## Context

- 의존: 없음
- 관련 워크: [[work-001-cli-prototype|MRT-WORK-001]] (CLI 프로토타입), [[work-005-websocket-server|MRT-WORK-005]] (§3 계약)
- 범위
  - 포함: CGWindowListCopyWindowInfo 호출, 필터링, WindowInfo 모델 정의
  - 제외: 창 활성화(Spec-02), 화면 캡처/썸네일, 앱 아이콘(Spec-04)

## 데이터 모델

```
Entity: WindowInfo
├── id: Int           — kCGWindowNumber, 창 고유 ID
├── app: String       — kCGWindowOwnerName, 앱 이름
├── title: String     — kCGWindowName, 창 제목 (빈 문자열 가능)
├── pid: Int          — kCGWindowOwnerPID, 프로세스 PID
└── frontmost: Bool   — 현재 최전면 창 여부
```

### 제약 조건

| 필드 | 제약 | 비고 |
|------|------|------|
| id | 양의 정수, 시스템이 부여 | 세션 내 고유 |
| app | 빈 문자열 제외 | 빈 OwnerName은 필터링 |
| title | 빈 문자열 허용 | Screen Recording 권한 없으면 항상 빈 문자열 |
| pid | 양의 정수 | 실행 중 프로세스에 한함 |
| frontmost | 목록 중 최대 1개만 true | NSWorkspace로 판별 |

## 계약 (Contract)

### 메시지 / API

| 방향 | 이름 | 설명 |
|------|------|------|
| iOS → Mac | listWindows | 창 목록 요청 |
| Mac → iOS | windowList | 창 목록 응답 (주기적 push에도 사용) |

#### 요청 예시

```json
{"action":"listWindows"}
```

#### 응답 예시

```json
{
  "type":"windowList",
  "windows":[
    {"id":123,"app":"Arc","title":"디자인 레퍼런스 — 12개 탭","frontmost":true},
    {"id":124,"app":"Xcode","title":"MacroHelper — AppDelegate.swift","frontmost":false},
    {"id":125,"app":"Terminal","title":"bash","frontmost":false}
  ]
}
```

### 공유 상수 / Enum

```swift
// 필터링에서 제외할 시스템 프로세스
let excludedProcesses = ["Window Server", "Dock", "SystemUIServer", "Control Center", "Notification Center"]
```

## 상태 전이 (State Machine)

```
[대기] ──(listWindows 요청)──► [수집 중] ──(성공)──► [응답 전송] ──► [대기]
                                    │
                                 (실패)
                                    ▼
                              [에러 응답] ──► [대기]
```

| 현재 상태 | 이벤트 | 다음 상태 | 액션 | 비고 |
|-----------|--------|-----------|------|------|
| 대기 | listWindows 수신 | 수집 중 | CGWindowListCopyWindowInfo 호출 | |
| 수집 중 | 성공 | 응답 전송 | 필터링 → JSON 생성 → 전송 | |
| 수집 중 | 실패 | 에러 응답 | 에러 메시지 전송 | CGWindowList null 반환 |
| 대기 | 타이머(1.5초) | 수집 중 | 주기적 push | 폴링 방식 |

## 에러 처리

| 에러 코드/유형 | 발생 조건 | 처리 주체 | 복구 전략 | 사용자 메시지 |
|---------------|-----------|-----------|-----------|--------------|
| EMPTY_TITLE | Screen Recording 권한 없음 | Mac 헬퍼 | 경고 로그 출력, 빈 제목으로 계속 동작 | "화면 기록 권한을 허용하면 창 제목이 표시됩니다" |
| NULL_LIST | CGWindowListCopyWindowInfo null 반환 | Mac 헬퍼 | 빈 배열 반환 | "창 목록을 가져올 수 없습니다" |
| NO_WINDOWS | 일반 창이 0개 | Mac 헬퍼 | 빈 배열 정상 반환 | iOS에서 빈 상태 UI 표시 |

### 재시도 정책

| 에러 유형 | 재시도 | 최대 횟수 | 간격 | 비고 |
|-----------|--------|-----------|------|------|
| NULL_LIST | Y | 3 | 500ms | 일시적 실패 가능성 |
| EMPTY_TITLE | N | — | — | 권한 문제, 재시도 무의미 |

## 유효성 검증

| 검증 항목 | 규칙 | 검증 위치 | 실패 시 동작 |
|-----------|------|-----------|-------------|
| kCGWindowLayer | == 0 (일반 창만) | Back (Mac) | 해당 창 제외 |
| kCGWindowOwnerName | 빈 문자열 아닐 것 | Back (Mac) | 해당 창 제외 |
| 시스템 프로세스 | excludedProcesses에 포함되지 않을 것 | Back (Mac) | 해당 창 제외 |
| windows 배열 | JSON 배열일 것 | Front (iOS) | 파싱 실패 시 기존 목록 유지 |

## 유저 플로우 (User Flow)

### 메인 플로우 (Happy Path)

```
1. iOS 앱에서 "창 목록" 탭 진입
   ▼
2. 앱이 Mac 헬퍼에 {"action":"listWindows"} 전송
   ▼
3. 헬퍼가 CGWindowListCopyWindowInfo 호출 → 필터링 → windowList 응답
   ▼
4. iOS 앱이 리스트 렌더링, frontmost 창에 청록 테두리
   ▼
5. 이후 헬퍼가 1.5초마다 windowList push → 목록 자동 갱신
```

### 분기 플로우

| 분기 지점 | 조건 | 흐름 |
|-----------|------|------|
| Step 3 | Screen Recording 권한 없음 | 창 제목이 빈 문자열로 옴 → iOS에서 앱 이름만 표시 |
| Step 5 | 새 창 열림/닫힘 | 다음 push 주기에 반영 |

### 실패 플로우

| 실패 지점 | 원인 | 사용자에게 보이는 것 | 복구 경로 |
|-----------|------|---------------------|-----------|
| Step 2 | WebSocket 미연결 | 연결 표시등 빨간색 | 재연결 시도 후 재요청 |
| Step 3 | CGWindowList null | 빈 목록 | 500ms 후 자동 재시도 (최대 3회) |

## UI/UX 요구사항

### 화면 / 컴포넌트

| 화면 | 설명 | 목업 링크 |
|------|------|-----------|
| 창 목록 탭 | 세로 리스트, 카드형 아이템 | macro_keyboard_mockup.html |

### 사용자 인터랙션

| 동작 | 트리거 | 기대 결과 | 피드백 |
|------|--------|-----------|--------|
| 창 목록 보기 | 탭 진입 | 현재 열린 창 리스트 표시 | — |
| 당겨서 새로고침 | Pull-to-refresh | listWindows 재요청 | 리스트 갱신 |
| 창 탭 | 카드 탭 | focus 명령 전송 (Spec-02) | 햅틱 피드백 |

## 엣지 케이스

| # | 시나리오 | 기대 동작 |
|---|----------|-----------|
| 1 | 열린 창이 0개 | 빈 상태 UI 표시 ("열린 창이 없습니다") |
| 2 | 같은 앱이 창 여러 개 | 각각 별도 항목, 창 제목으로 구분 |
| 3 | Screen Recording 권한 없음 | 창 제목 빈 문자열, 앱 이름만 표시 |
| 4 | macOS 백그라운드 프로세스 혼입 | excludedProcesses + layer 필터로 제거 |
| 5 | 창 제목이 매우 긴 경우 | iOS에서 말줄임 처리 |
| 6 | 앱이 창을 빠르게 열고 닫을 때 | 다음 push 주기에 반영, 일시적 불일치 허용 |

## 인수 조건 (Acceptance Criteria)

- [x] CGWindowListCopyWindowInfo 호출로 현재 화면의 창 목록을 가져올 수 있다
- [x] layer == 0인 일반 창만 반환된다
- [x] 시스템 프로세스(Window Server, Dock 등)가 제외된다
- [x] 빈 OwnerName 창이 제외된다
- [x] 각 창의 id, app, title, pid, frontmost 필드가 포함된다
- [x] frontmost 표시가 정확하다
- [x] Screen Recording 권한 없을 때 title이 빈 문자열이고 에러 없이 동작한다
- [x] JSON 응답이 계약(§계약) 형식을 따른다

## Work Handoff

| Work | 범위 |
|---|---|
| [[work-001-cli-prototype\|MRT-WORK-001]] | 창 목록 수집 + 필터 + WindowInfo 모델 (CLI) |
| [[work-005-websocket-server\|MRT-WORK-005]] | §계약 windowList 메시지 (WS 서버) |
