---
type: work
id: MRT-WORK-011
title: "I4: 매크로 화면"
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
    - "[[v1_0_1-work-009-ws-client|MRT-WORK-009]]"
  releases:
    - "[[v1_0_1-release-001-v1-0-0|MRT-REL-001]]"
  related: []
---

# I4: 매크로 화면

2열 그리드 매크로 버튼 화면을 만든다. 기본 프리셋 + 사용자 정의 매크로. 탭하면 key 명령 전송 + 햅틱.

> 원본: `mac-remote/doc/work/Work-11-macro-ui.md`. 구현 계약은 [[v1_0_1-spec-003-key-input|MRT-SPEC-003]].

## Work Summary

| 항목 | 내용 |
|---|---|
| 상태 | done |
| 시작일 | 2026-05-24 |
| 완료일 | 2026-05-24 |
| 의존 | [[v1_0_1-work-009-ws-client\|MRT-WORK-009]] |
| 관련 스펙 | [[v1_0_1-spec-003-key-input\|MRT-SPEC-003]] |

## 참조 스펙 체크리스트

| Spec 섹션 | 항목 | 반영 여부 |
|-----------|------|-----------|
| Spec-03 §3 계약 | key action JSON 형식 | [x] |
| Spec-03 §8 UI/UX | 2열 그리드, 매크로 추가 | [x] |
| Spec-03 §9 엣지 케이스 | 빠른 연속 탭, 동시 탭 | [x] |

## 태스크

| # | 태스크 | 상태 | 커밋 | 비고 |
|---|--------|------|------|------|
| 1 | MacroItem 모델 (이름, key, modifiers) | [x] | 3b0aaf1 | Codable, isUserDefined, modifierSymbols, shortcutLabel |
| 2 | 기본 프리셋 정의 (⌘C/⌘V/⌘Z/⌘⇧Z/⌘⇧4/⌃⌘Q/⌘⇥) | [x] | 140f2fa | 7개 프리셋 |
| 3 | 2열 LazyVGrid 버튼 화면 | [x] | 9336a66 | EnvironmentObject 연결 포함 |
| 4 | 버튼 탭 → key 명령 전송 + 햅틱 | [x] | 610e936 | MacroButtonView + MacroButtonStyle |
| 5 | "매크로 추가" 시트 (키 + modifier 선택) | [x] | a10990f | AddMacroSheet (추가/편집 겸용) |
| 6 | 사용자 매크로 저장 (UserDefaults) | [x] | 903ea43 | MacroStore 클래스 분리 |

## 기술 메모

- LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())])
- UIImpactFeedbackGenerator(style: .medium)
- UserDefaults에 [MacroItem] JSON으로 저장
- MacroStore: ObservableObject로 CRUD 캡슐화
- MacroButtonStyle: 눌림 시 scale 0.95 + opacity 0.7
- AddMacroSheet: 편집 모드(editingMacro != nil) 겸용
- ContentView + iOSAppApp에 @EnvironmentObject WebSocketManager 연결

## 검증 방법 / Acceptance

| # | 검증 항목 | 방법 | 결과 |
|---|----------|------|------|
| 1 | 프리셋 표시 | 매크로 탭 → 7개 기본 버튼 표시 | 수동 검증 (Xcode 필요) |
| 2 | ⌘C 실행 | 텍스트 선택 후 ⌘C 버튼 탭 → 클립보드 복사 | 수동 검증 (Xcode 필요) |
| 3 | 매크로 추가 | "추가" → 키/modifier 선택 → 저장 → 목록에 표시 | 수동 검증 (Xcode 필요) |
| 4 | 햅틱 | 버튼 탭 시 진동 피드백 | 수동 검증 (실기기 필요) |

## 완료 기록

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-05-24 | 최초 작성 |
| 2026-05-24 | 6/6 태스크 완료 (Done) |
