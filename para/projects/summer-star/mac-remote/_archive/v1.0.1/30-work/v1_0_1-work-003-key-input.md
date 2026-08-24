---
type: work
id: MRT-WORK-003
title: "M3: 키 입력"
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
    - "[[v1_0_1-spec-003-key-input|MRT-SPEC-003]]"
  works:
    - "[[v1_0_1-work-001-cli-prototype|MRT-WORK-001]]"
  releases:
    - "[[v1_0_1-release-001-v1-0-0|MRT-REL-001]]"
  related: []
---

# M3: 키 입력

key + modifiers를 인자로 받아 CGEvent로 Mac에 키 입력을 전송한다. 가상 키코드 매핑 테이블을 작성한다.

> 원본: `mac-remote/doc/work/Work-03-key-input.md`. 구현 계약은 [[v1_0_1-spec-003-key-input|MRT-SPEC-003]].

## Work Summary

| 항목 | 내용 |
|---|---|
| 상태 | done |
| 시작일 | 2026-05-24 |
| 완료일 | 2026-05-24 |
| 의존 | [[v1_0_1-work-001-cli-prototype\|MRT-WORK-001]] |
| 관련 스펙 | [[v1_0_1-spec-003-key-input\|MRT-SPEC-003]] |

## 참조 스펙 체크리스트

| Spec 섹션 | 항목 | 반영 여부 |
|-----------|------|-----------|
| Spec-03 §데이터 모델 | KeyCommand (key, modifiers), VirtualKeyMap | [x] |
| Spec-03 §상태 전이 | 키코드 조회 → 이벤트 생성 → keyDown → keyUp | [x] |
| Spec-03 §에러 처리 | UNKNOWN_KEY, AX_PERMISSION, EVENT_CREATE_FAIL | [x] |

## 태스크

| # | 태스크 | 상태 | 커밋 | 비고 |
|---|--------|------|------|------|
| 1 | VirtualKeyMap 정적 매핑 테이블 작성 | [x] | b463f9e | a~z, 0~9, 특수키, F1~F12, 화살표 |
| 2 | Modifier → CGEventFlags 매핑 | [x] | b463f9e | cmd/shift/alt/ctrl, #if canImport(CoreGraphics) |
| 3 | CGEvent keyDown/keyUp 전송 함수 | [x] | b463f9e | KeySender.send(), #if canImport(CoreGraphics) |
| 4 | 에러 처리 (알 수 없는 키, 권한 없음) | [x] | b463f9e | KeySendError enum, INVALID_MODIFIER 무시 |
| 5 | CLI에서 key+modifier 인자로 테스트 | [x] | c3c6e41 | main.swift key 서브커맨드 + formatKeyAckJSON |

## 기술 메모

- CGEvent(keyboardEventSource:nil, virtualKey:keyCode, keyDown:true/false)
- event.flags = [.maskCommand, .maskShift] 등으로 modifier 설정
- event.post(tap: .cghidEventTap)
- Accessibility 권한 필요

## 검증 방법 / Acceptance

| # | 검증 항목 | 방법 | 결과 |
|---|----------|------|------|
| 1 | ⌘C 전송 | 텍스트 선택 후 `swift run MacHelper key c cmd` → 클립보드에 복사됨 | 수동 검증 (macOS 필요) |
| 2 | ⌘⇧4 전송 | `swift run MacHelper key 4 cmd shift` → 스크린샷 모드 진입 | 수동 검증 (macOS 필요) |
| 3 | 알 수 없는 키 | `swift run MacHelper key xyz` → 에러 메시지 | 수동 검증 (macOS 필요) |

### 로그 추적 포인트

| # | 위치 (파일/함수) | 로그 레벨 | 로그 내용 |
|---|-----------------|-----------|-----------|
| 1 | KeySender.send() | INFO | "Sending key={key} modifiers={mods}" |
| 2 | KeySender.send() | ERROR | "Unknown key: {key}" |
| 3 | KeySender.send() | ERROR | "CGEvent creation failed" |
| 4 | KeySender.send() | ERROR | "Accessibility permission denied" |

## 완료 기록

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-05-24 | 최초 작성 |
| 2026-05-24 | TDD 구현 완료 (5/5 태스크), 커밋 b463f9e, c3c6e41 |
