---
type: work
id: MRT-WORK-006
title: "M6: 메뉴바 앱화"
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
  specs:
    - "[[spec-006-permissions|MRT-SPEC-006]]"
  works:
    - "[[work-005-websocket-server|MRT-WORK-005]]"
  releases:
    - "[[release-001-v1-0-0|MRT-REL-001]]"
  related: []
---

# M6: 메뉴바 앱화

CLI를 메뉴바 앱(MenuBarExtra)으로 전환한다. 상태 아이콘, 연결 상태, IP:포트, 권한 상태를 표시한다. Dock 아이콘 숨김.

> 원본: `mac-remote/doc/work/Work-06-menubar-app.md`. 구현 계약은 [[spec-006-permissions|MRT-SPEC-006]].

## Work Summary

| 항목 | 내용 |
|---|---|
| 상태 | done |
| 시작일 | 2026-05-24 |
| 완료일 | 2026-05-24 |
| 의존 | [[work-005-websocket-server\|MRT-WORK-005]] |
| 관련 스펙 | [[spec-006-permissions\|MRT-SPEC-006]] |

## 참조 스펙 체크리스트

| Spec 섹션 | 항목 | 반영 여부 |
|-----------|------|-----------|
| Spec-06 §유저 플로우 | 첫 실행 권한 확인 → 메뉴바 표시 | [x] |
| Spec-06 §UI/UX | 메뉴바 권한 상태 + 시스템 설정 열기 | [x] |

## 태스크

| # | 태스크 | 상태 | 커밋 | 비고 |
|---|--------|------|------|------|
| 1 | Swift Package → Xcode App 프로젝트 전환 또는 App 프로토콜 사용 | [x] | dd63337 | AppState 모델 + MacHelperApp 타겟 추가 |
| 2 | MenuBarExtra 구현 (상태 아이콘) | [x] | f1d8789 | MenuBarContentView + SF Symbol 아이콘 |
| 3 | 메뉴: 연결 상태 (클라이언트 수), IP:포트 표시 | [x] | 7dbe8cd | NetworkInfo + fullAddressText |
| 4 | 메뉴: 권한 상태 표시 + 시스템 설정 열기 버튼 | [x] | 9b2c54f | SystemSettingsOpener + 설정 열기 버튼 |
| 5 | Info.plist: LSUIElement=true (Dock 아이콘 숨김) | [x] | 3cd706c | Info.plist + Package.swift 타겟 분리 |
| 6 | 앱 시작 시 WebSocket 서버 자동 시작 | [x] | e03db04 | AppLifecycleManager — 서버+권한+상태 |

## 기술 메모

- MenuBarExtra는 SwiftUI App 프로토콜에서 사용
- LSUIElement로 Dock 아이콘 숨김
- NSWorkspace.shared.open(URL(string: "x-apple.systempreferences:...")!)로 시스템 설정 열기
- CLI 타겟(MacHelper)은 유지, 새로운 MacHelperApp 타겟이 메뉴바 앱
- AppState: 순수 Swift 상태 모델 (Linux 테스트 가능)
- AppLifecycleManager: 서버 시작/종료, 권한 확인, 상태 갱신 주기적 실행
- NetworkInfo: getifaddrs로 로컬 IP 조회 (en0 Wi-Fi 우선)

## 검증 방법 / Acceptance

| # | 검증 항목 | 방법 | 결과 |
|---|----------|------|------|
| 1 | 메뉴바 아이콘 | 앱 실행 → 메뉴바에 아이콘 표시 | 수동 검증 (macOS 필요) |
| 2 | Dock 숨김 | 앱 실행 → Dock에 아이콘 없음 | 수동 검증 (macOS 필요) |
| 3 | 권한 표시 | 메뉴 열기 → 권한 상태 확인 | 수동 검증 (macOS 필요) |
| 4 | 시스템 설정 | "설정 열기" 클릭 → 해당 설정 페이지 열림 | 수동 검증 (macOS 필요) |
| 5 | AppState 상태 모델 | 단위 테스트 (AppStateTests) | 수동 검증 (Swift 미설치) |
| 6 | 시스템 설정 URL 상수 | 단위 테스트 (SystemSettingsTests) | 수동 검증 (Swift 미설치) |
| 7 | AppLifecycleManager 초기화 | 단위 테스트 (AppLifecycleManagerTests) | 수동 검증 (Swift 미설치) |

## 완료 기록

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-05-24 | 최초 작성 |
| 2026-05-24 | 6개 태스크 완료 (Done) |
