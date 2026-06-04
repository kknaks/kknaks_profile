---
type: spec
id: MRT-SPEC-004
title: "앱 아이콘 수집"
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
    - "[[decision-003-app-icon-only-no-capture|MRT-DEC-003]]"
  specs:
    - "[[spec-001-window-list|MRT-SPEC-001]]"
  works:
    - "[[work-004-app-icon|MRT-WORK-004]]"
    - "[[work-005-websocket-server|MRT-WORK-005]]"
  releases:
    - "[[release-001-v1-0-0|MRT-REL-001]]"
    - "[[release-002-v1-0-1|MRT-REL-002]]"
  related: []
---

# 앱 아이콘 수집

실행 중인 앱들의 아이콘을 추출해 iOS 앱에 전송한다. 화면 캡처가 아니라 설치된 앱의 아이콘 파일을 읽는 것이며, 추가 권한이 필요 없다.

> 원본: `mac-remote/doc/spec/Spec-04-app-icon.md`. 결정 근거는 [[decision-003-app-icon-only-no-capture|MRT-DEC-003]].

## Context

- 의존: [[spec-001-window-list|MRT-SPEC-001]]
- 관련 워크: [[work-004-app-icon|MRT-WORK-004]] (아이콘 수집 구현), [[work-005-websocket-server|MRT-WORK-005]] (§계약 appIcons push 메시지)
- 범위
  - 포함: NSWorkspace/NSRunningApplication으로 아이콘 추출, PNG base64 인코딩, 앱별 1회 전송
  - 제외: 창 썸네일/스크린샷, ScreenCaptureKit

## 데이터 모델

```
Entity: AppIcon
├── appName: String    — 앱 이름 (키)
└── iconData: String   — PNG base64 인코딩 문자열
```

### 제약 조건

| 필드 | 제약 | 비고 |
|------|------|------|
| appName | Spec-01 WindowInfo.app과 동일한 이름 | 매칭 키 |
| iconData | 유효한 base64 PNG | 디코딩 실패 시 기본 아이콘 |

## 계약 (Contract)

### 메시지 / API

| 방향 | 이름 | 설명 |
|------|------|------|
| Mac → iOS | appIcons | 앱 아이콘 데이터 전송 (push) |

#### 요청 예시

요청 없음. windowList 전송 시 새 앱이 감지되면 자동 push.

#### 응답 예시

```json
{
  "type":"appIcons",
  "icons":{
    "Arc":"iVBORw0KGgo...(base64)...",
    "Xcode":"iVBORw0KGgo...(base64)...",
    "Terminal":"iVBORw0KGgo...(base64)..."
  }
}
```

### 공유 상수 / Enum

해당 없음

## 상태 전이 (State Machine)

```
[대기] ──(새 앱 감지)──► [아이콘 추출] ──(성공)──► [base64 인코딩] ──► [push 전송] ──► [대기]
                              │
                           (실패)
                              ▼
                         [기본 아이콘 사용] ──► [push 전송] ──► [대기]
```

| 현재 상태 | 이벤트 | 다음 상태 | 액션 | 비고 |
|-----------|--------|-----------|------|------|
| 대기 | windowList에 새 앱 이름 등장 | 아이콘 추출 | NSRunningApplication.icon 또는 NSWorkspace.icon(forFile:) | |
| 아이콘 추출 | 성공 | base64 인코딩 | PNG → base64 String | |
| 아이콘 추출 | 실패 | 기본 아이콘 | 시스템 기본 앱 아이콘 사용 | |
| base64 인코딩 | — | push 전송 | appIcons 메시지 전송 | 새 앱 아이콘만 전송 |

## 에러 처리

| 에러 코드/유형 | 발생 조건 | 처리 주체 | 복구 전략 | 사용자 메시지 |
|---------------|-----------|-----------|-----------|--------------|
| ICON_NOT_FOUND | 앱 번들에 아이콘 없음 | Mac 헬퍼 | 시스템 기본 아이콘으로 대체 | — |
| ENCODE_FAIL | PNG 인코딩 실패 | Mac 헬퍼 | 해당 앱 아이콘 건너뛰기 | — |

### 재시도 정책

| 에러 유형 | 재시도 | 최대 횟수 | 간격 | 비고 |
|-----------|--------|-----------|------|------|
| 모든 유형 | N | — | — | 아이콘은 변하지 않으므로 재시도 무의미 |

## 유효성 검증

| 검증 항목 | 규칙 | 검증 위치 | 실패 시 동작 |
|-----------|------|-----------|-------------|
| iconData | 유효한 base64 | Front (iOS) | 기본 아이콘 표시 |
| appName | windowList의 app 필드와 매칭 | Front (iOS) | 매칭 안 되면 아이콘 없이 표시 |

## 유저 플로우 (User Flow)

### 메인 플로우 (Happy Path)

```
1. Mac 헬퍼가 windowList push 시 새 앱 감지
   ▼
2. NSRunningApplication(pid).icon으로 아이콘 추출
   ▼
3. PNG base64 인코딩
   ▼
4. appIcons 메시지 push
   ▼
5. iOS 앱이 수신 → 앱 이름별 캐싱 → 창 목록 카드에 아이콘 표시
```

### 분기 플로우

| 분기 지점 | 조건 | 흐름 |
|-----------|------|------|
| Step 2 | PID로 아이콘 못 찾음 | NSWorkspace.icon(forFile: bundlePath) 시도 |
| Step 5 | 이미 캐시에 있는 앱 | push 안 함, iOS도 재요청 안 함 |

### 실패 플로우

| 실패 지점 | 원인 | 사용자에게 보이는 것 | 복구 경로 |
|-----------|------|---------------------|-----------|
| Step 2 | 아이콘 추출 실패 | 기본 아이콘 표시 | 없음 (정상 동작) |

## UI/UX 요구사항

### 화면 / 컴포넌트

| 화면 | 설명 | 목업 링크 |
|------|------|-----------|
| 창 목록 탭 | 카드 왼쪽에 앱 아이콘 표시 | macro_keyboard_mockup.html |

### 사용자 인터랙션

| 동작 | 트리거 | 기대 결과 | 피드백 |
|------|--------|-----------|--------|
| — | 자동 | 창 카드에 앱 아이콘 표시 | — |

## 엣지 케이스

| # | 시나리오 | 기대 동작 |
|---|----------|-----------|
| 1 | 같은 앱 창 3개 | 아이콘 1번만 전송, iOS에서 캐시 |
| 2 | 앱 종료 후 재실행 | 캐시에 있으므로 재전송 안 함 |
| 3 | 아이콘이 매우 큰 앱 | 적절한 크기(64x64 등)로 리사이즈 후 인코딩 |
| 4 | command line tool (아이콘 없음) | 시스템 기본 아이콘 사용 |

## 인수 조건 (Acceptance Criteria)

- [x] 실행 중 앱의 아이콘을 PNG base64로 추출할 수 있다
- [x] 앱 이름별로 1회만 전송된다 (중복 전송 없음)
- [x] 아이콘 추출 실패 시 기본 아이콘으로 대체된다
- [x] iOS 앱에서 아이콘을 디코딩해 카드에 표시할 수 있다
- [x] 추가 권한(Screen Recording 등) 없이 동작한다

## 변경 이력

| 날짜 | 변경 내용 | 작성자 |
|------|-----------|--------|
| 2026-05-24 | 최초 작성 | |