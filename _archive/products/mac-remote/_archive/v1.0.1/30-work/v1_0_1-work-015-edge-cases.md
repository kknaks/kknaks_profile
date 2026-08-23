---
type: work
id: MRT-WORK-015
title: "T2: 엣지 케이스 대응"
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
    - "[[v1_0_1-spec-001-window-list|MRT-SPEC-001]]"
    - "[[v1_0_1-spec-002-window-focus|MRT-SPEC-002]]"
    - "[[v1_0_1-spec-003-key-input|MRT-SPEC-003]]"
    - "[[v1_0_1-spec-004-app-icon|MRT-SPEC-004]]"
    - "[[v1_0_1-spec-005-websocket-protocol|MRT-SPEC-005]]"
    - "[[v1_0_1-spec-006-permissions|MRT-SPEC-006]]"
    - "[[v1_0_1-spec-007-pairing|MRT-SPEC-007]]"
  works:
    - "[[v1_0_1-work-014-e2e-test|MRT-WORK-014]]"
  releases:
    - "[[v1_0_1-release-002-v1-0-1|MRT-REL-002]]"
  related: []
---

# T2: 엣지 케이스 대응

헬퍼 꺼짐, Wi-Fi 변경, 권한 회수, 창 0개, 같은 앱 다중 창 등 엣지 케이스를 테스트하고 대응한다.

> 원본: `mac-remote/doc/work/Work-15-edge-cases.md`. 구현 계약은 [[v1_0_1-spec-001-window-list|MRT-SPEC-001]], [[v1_0_1-spec-002-window-focus|MRT-SPEC-002]], [[v1_0_1-spec-003-key-input|MRT-SPEC-003]], [[v1_0_1-spec-004-app-icon|MRT-SPEC-004]], [[v1_0_1-spec-005-websocket-protocol|MRT-SPEC-005]], [[v1_0_1-spec-006-permissions|MRT-SPEC-006]], [[v1_0_1-spec-007-pairing|MRT-SPEC-007]].

## Work Summary

| 항목 | 내용 |
|---|---|
| 상태 | done |
| 시작일 | 2026-05-24 |
| 완료일 | 2026-05-26 |
| 의존 | [[v1_0_1-work-014-e2e-test\|MRT-WORK-014]] |
| 관련 스펙 | [[v1_0_1-spec-001-window-list\|MRT-SPEC-001]], [[v1_0_1-spec-002-window-focus\|MRT-SPEC-002]], [[v1_0_1-spec-003-key-input\|MRT-SPEC-003]], [[v1_0_1-spec-004-app-icon\|MRT-SPEC-004]], [[v1_0_1-spec-005-websocket-protocol\|MRT-SPEC-005]], [[v1_0_1-spec-006-permissions\|MRT-SPEC-006]], [[v1_0_1-spec-007-pairing\|MRT-SPEC-007]] |

## 참조 스펙 체크리스트

| Spec 섹션 | 항목 | 반영 여부 |
|-----------|------|-----------|
| Spec-01 §9 | 창 0개, 같은 앱 다중 창, 긴 제목 | [x] |
| Spec-02 §9 | 창 닫힘 race condition, 전체 화면 앱 | [x] |
| Spec-05 §9 | Wi-Fi 변경, Mac 슬립, iOS 백그라운드 | [x] |
| Spec-06 §9 | 권한 허용 후 회수, 두 권한 모두 거부 | [x] |

## 태스크

| # | 태스크 | 상태 | 커밋 | 비고 |
|---|--------|------|------|------|
| 1 | 헬퍼 꺼짐 → 재연결 동작 확인 | [x] | | |
| 2 | 권한 회수 → graceful degradation | [x] | | |
| 3 | 창 0개 → 빈 상태 UI | [x] | | |
| 4 | 같은 앱 다중 창 → AXRaise 정확성 | [x] | | |
| 5 | iOS 백그라운드 → 복귀 시 재연결 | [x] | | |
| 6 | 발견된 버그 수정 | [x] | | |

## 기술 메모

수동 테스트 위주. 발견된 문제는 해당 워크의 기술 메모에도 기록.

## 검증 방법 / Acceptance

| # | 검증 항목 | 방법 | 결과 |
|---|----------|------|------|
| 1 | 각 엣지 케이스별 | 시나리오대로 재현 → 기대 동작 확인 | — |

## 완료 기록

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-05-24 | 최초 작성 |
| 2026-05-26 | done — 1.0.1에서 재연결·네트워크 전환·아이콘 snapshot 등 엣지 케이스 대응, 운영 사용으로 검증 |
