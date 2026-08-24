---
type: work
id: MRT-WORK-001
title: "M1: CLI 프로토타입 (창 목록)"
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
  decisions:
    - "[[v1_0_1-decision-004-mac-helper-first|MRT-DEC-004]]"
  specs:
    - "[[v1_0_1-spec-001-window-list|MRT-SPEC-001]]"
    - "[[v1_0_1-spec-006-permissions|MRT-SPEC-006]]"
  works: []
  releases:
    - "[[v1_0_1-release-001-v1-0-0|MRT-REL-001]]"
  related: []
---

# M1: CLI 프로토타입 (창 목록)

Swift Package로 Mac 헬퍼의 CLI 프로토타입을 만든다. CGWindowListCopyWindowInfo로 창 목록을 콘솔에 출력하고, 권한 상태를 확인할 수 있다.

> 원본: `mac-remote/doc/work/Work-01-cli-prototype.md`. 구현 계약은 [[v1_0_1-spec-001-window-list|MRT-SPEC-001]], [[v1_0_1-spec-006-permissions|MRT-SPEC-006]].

## Work Summary

| 항목 | 내용 |
|---|---|
| 상태 | done |
| 시작일 | 2026-05-24 |
| 완료일 | 2026-05-24 |
| 의존 | — |
| 관련 스펙 | [[v1_0_1-spec-001-window-list\|MRT-SPEC-001]], [[v1_0_1-spec-006-permissions\|MRT-SPEC-006]] |

## 참조 스펙 체크리스트

| Spec 섹션 | 항목 | 반영 여부 |
|-----------|------|-----------|
| Spec-01 §데이터 모델 | WindowInfo 구조체 (id, app, title, pid, frontmost) | [x] |
| Spec-01 §계약 | windowList JSON 형식 출력 | [x] |
| Spec-01 §유효성 검증 | layer==0 필터, 빈 OwnerName 제외, 시스템 프로세스 제외 | [x] |
| Spec-06 §데이터 모델 | PermissionStatus (accessibility, screenRecording) | [x] |
| Spec-06 §상태 전이 | AXIsProcessTrusted + 창 제목 테스트 | [x] |

## 태스크

| # | 태스크 | 상태 | 커밋 | 비고 |
|---|--------|------|------|------|
| 1 | Swift Package 프로젝트 생성 (MacHelper) | [x] | 2c9fe3b, 59c4ad1 | 초기 생성 + lib 타겟 분리 |
| 2 | WindowInfo 모델 정의 | [x] | 4ae29b0 | Codable, Equatable, public |
| 3 | CGWindowListCopyWindowInfo 호출 + 필터링 | [x] | 67e0567 | layer, OwnerName, 시스템 프로세스 |
| 4 | frontmost 판별 로직 | [x] | c4d3004 | 최대 1개만 true, NSWorkspace |
| 5 | 권한 상태 확인 (Accessibility + Screen Recording) | [x] | a59c7e8 | AXIsProcessTrusted, 창 제목 빈 값 체크 |
| 6 | JSON 형식으로 콘솔 출력 | [x] | bbb273b | Spec-01 §계약 + Spec-06 §계약 형식 |
| 7 | 권한 미허용 시 안내 메시지 출력 | [x] | a8ee52d | 권한별 안내 + 시스템 설정 경로 |

## 기술 메모

- CGWindowListCopyWindowInfo는 CoreGraphics 프레임워크 (import CoreGraphics)
- AppKit도 필요 (NSWorkspace, NSRunningApplication)
- Swift Package의 macOS 최소 타겟: .macOS(.v14)
- macOS 전용 코드는 `#if canImport(CoreGraphics) && canImport(AppKit)` 사용
- 순수 Swift 로직 (필터링, 모델, JSON 포맷) 은 Linux에서도 테스트 가능
- MacHelperLib (라이브러리) + MacHelper (executable) 타겟 분리로 테스트 가능성 확보

## 검증 방법 / Acceptance

| # | 검증 항목 | 방법 | 결과 |
|---|----------|------|------|
| 1 | 창 목록 출력 | `swift run MacHelper` → 현재 열린 창 목록이 JSON으로 출력 | 수동 검증 (macOS 필요) |
| 2 | 필터링 | Dock, Window Server 등이 목록에 없는지 확인 | 순수 로직 테스트 통과 (12개) |
| 3 | frontmost | 현재 최전면 앱의 창에 frontmost:true 표시 확인 | 순수 로직 테스트 통과 (5개) |
| 4 | 권한 미허용 | 화면 기록 권한 해제 후 실행 → 창 제목 빈 문자열 + 경고 로그 | 수동 검증 (macOS 필요) |
| 5 | Accessibility 미허용 | 손쉬운 사용 권한 해제 후 실행 → 안내 메시지 출력 | 순수 로직 테스트 통과 (8개) |

### 로그 추적 포인트

| # | 위치 (파일/함수) | 로그 레벨 | 로그 내용 |
|---|-----------------|-----------|-----------|
| 1 | WindowManager.listWindows() | INFO | 수집된 전체 창 수 + 필터 후 창 수 |
| 2 | WindowManager.listWindows() | WARN | Screen Recording 권한 없음 → 창 제목 빈 문자열 감지 |
| 3 | PermissionChecker.check() | ERROR | Accessibility 권한 거부 |
| 4 | WindowManager.listWindows() | WARN | CGWindowListCopyWindowInfo null 반환 |
| 5 | 필터링 | INFO | 제외된 시스템 프로세스 목록 (디버그용) |

## 완료 기록

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-05-24 | 최초 작성 |
| 2026-05-24 | 7개 태스크 TDD 구현 완료 (Done) |
