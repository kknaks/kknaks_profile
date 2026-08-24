---
type: work
id: MRT-WORK-002
title: "M2: 창 활성화"
status: archived
original_status: done
archived_version: v1.0.1
archived_at: 2026-06-08
product: mac-remote
work_type: new-feature
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 100
created_at: 2026-05-24
updated_at: 2026-06-01
tags:
  - product/mac-remote
  - doc/work
  - status/archived
links:
  baselines: []
  decisions: []
  specs:
    - "[[v1_0_1-spec-002-window-focus|MRT-SPEC-002]]"
  works:
    - "[[v1_0_1-work-001-cli-prototype|MRT-WORK-001]]"
  releases:
    - "[[v1_0_1-release-001-v1-0-0|MRT-REL-001]]"
  related: []
---

# M2: 창 활성화

windowId를 인자로 받아 해당 창을 최전면으로 활성화한다. PID 기반 앱 활성화 후 AXUIElement로 개별 창을 raise한다.

> 원본: `mac-remote/doc/work/Work-02-window-focus.md`. 구현 계약은 [[v1_0_1-spec-002-window-focus|MRT-SPEC-002]].

## Work Summary

| 항목 | 내용 |
|---|---|
| 상태 | done |
| 시작일 | 2026-05-24 |
| 완료일 | 2026-05-24 |
| 의존 | [[v1_0_1-work-001-cli-prototype\|MRT-WORK-001]] |
| 관련 스펙 | [[v1_0_1-spec-002-window-focus\|MRT-SPEC-002]] |

## 참조 스펙 체크리스트

| Spec 섹션 | 항목 | 반영 여부 |
|-----------|------|-----------|
| Spec-02 §데이터 모델 | FocusRequest (windowId) | [x] |
| Spec-02 §상태 전이 | PID 조회 → 앱 활성화 → AXRaise | [x] |
| Spec-02 §에러 처리 | WINDOW_NOT_FOUND, PROCESS_DEAD, AX_PERMISSION | [x] |
| Spec-02 §엣지 케이스 | 이미 frontmost, 같은 앱 다중 창 | [x] |

## 태스크

| # | 태스크 | 상태 | 커밋 | 비고 |
|---|--------|------|------|------|
| 1 | windowId → PID 조회 함수 (Work-01의 창 목록 활용) | [x] | 7b2e137 | lookupPID, lookupWindow, FocusError, FocusAckResponse |
| 2 | NSRunningApplication.activate() 구현 | [x] | c52f4ee | PID 기반, macOS 전용 |
| 3 | AXUIElement 기반 창 목록 조회 + AXRaise 구현 | [x] | 87afbe5 | Accessibility API, 100ms 재시도 |
| 4 | 에러 처리 (창 없음, 프로세스 종료, 권한 없음) | [x] | b367488 | focusWithAck() 통합 함수 |
| 5 | CLI에서 windowId 인자로 테스트 | [x] | 36c4064 | `swift run MacHelper focus <windowId>` |

## 기술 메모

- AXUIElementCreateApplication(pid) → AXUIElementCopyAttributeValue(.windows) → AXUIElementPerformAction(.raise)
- Accessibility 권한 필수. 없으면 앱 활성화만 가능.

## 검증 방법 / Acceptance

| # | 검증 항목 | 방법 | 결과 |
|---|----------|------|------|
| 1 | 앱 활성화 | `swift run MacHelper focus {windowId}` → 해당 앱이 최전면 | 수동 검증 (macOS 필요) |
| 2 | 개별 창 raise | 같은 앱 창 2개 열고 뒤쪽 창 windowId로 실행 → 해당 창이 앞으로 | 수동 검증 (macOS 필요) |
| 3 | 없는 windowId | 존재하지 않는 ID 입력 → 에러 메시지 | 수동 검증 (macOS 필요) |

### 로그 추적 포인트

| # | 위치 (파일/함수) | 로그 레벨 | 로그 내용 |
|---|-----------------|-----------|-----------|
| 1 | WindowFocuser.focus() | INFO | "Focusing windowId={id}, pid={pid}" |
| 2 | WindowFocuser.focus() | ERROR | "Window not found: {id}" |
| 3 | WindowFocuser.focus() | ERROR | "Process dead: pid={pid}" |
| 4 | WindowFocuser.axRaise() | WARN | "AXRaise failed, app activated only" |
| 5 | WindowFocuser.focus() | ERROR | "Accessibility permission denied" |

## 완료 기록

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-05-24 | 최초 작성 |
| 2026-05-24 | 5개 태스크 구현 완료 (Done) |
