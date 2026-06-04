---
type: work
id: MRT-WORK-008
title: "I1: 프로젝트 셋업 (3탭)"
status: done
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
  - status/done
links:
  baselines: []
  decisions: []
  specs: []
  works:
    - "[[work-005-websocket-server|MRT-WORK-005]]"
  releases:
    - "[[release-001-v1-0-0|MRT-REL-001]]"
  related: []
---

# I1: 프로젝트 셋업 (3탭)

SwiftUI iOS 앱 프로젝트를 생성하고, 3탭 TabView(창 목록 / 매크로 / 설정) 기본 구조를 만든다. 다크 테마, 청록(#5eead4) 포인트 컬러 적용.

> 원본: `mac-remote/doc/work/Work-08-ios-setup.md`.

## Work Summary

| 항목 | 내용 |
|---|---|
| 상태 | done |
| 시작일 | 2026-05-24 |
| 완료일 | 2026-05-24 |
| 의존 | [[work-005-websocket-server\|MRT-WORK-005]] |
| 관련 스펙 | — |

## 참조 스펙 체크리스트

| Spec 섹션 | 항목 | 반영 여부 |
|-----------|------|-----------|
| (공통) | 3탭 TabView 구조 | [x] |
| (공통) | 다크 테마 + 청록 포인트 컬러 | [x] |

## 태스크

| # | 태스크 | 상태 | 커밋 | 비고 |
|---|--------|------|------|------|
| 1 | Xcode iOS 프로젝트 생성 (iOSApp/) | [x] | 3e40451 | SwiftUI, iOS 17+ |
| 2 | 3탭 TabView 스켈레톤 | [x] | 0fc2b4c | 창 목록 / 매크로 / 설정 |
| 3 | 다크 테마 강제 적용 | [x] | 0fc2b4c | preferredColorScheme(.dark) |
| 4 | 청록 포인트 컬러 정의 (#5eead4) | [x] | d126736 | Color extension + 공유 모델 |
| 5 | 각 탭에 placeholder 화면 | [x] | 9addfd6 | Views + Components + MacroItem |

## 기술 메모

- Color.teal 대신 커스텀 Color(hex: "#5eead4") 사용
- TabView에 .tabItem { Label("창 목록", systemImage: "macwindow") } 형식

## 검증 방법 / Acceptance

| # | 검증 항목 | 방법 | 결과 |
|---|----------|------|------|
| 1 | 빌드 | Xcode에서 시뮬레이터 빌드 성공 | 수동 검증 (Xcode 필요) |
| 2 | 3탭 | 앱 실행 → 하단 3탭 전환 가능 | 수동 검증 (Xcode 필요) |
| 3 | 다크 테마 | 라이트 모드에서도 앱은 다크 | 수동 검증 (Xcode 필요) |

## 완료 기록

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-05-24 | 최초 작성 |
| 2026-05-24 | 전체 태스크 구현 완료 (Done) |
