---
type: work
id: MRT-WORK-014
title: "T1: 엔드투엔드 테스트"
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
    - "[[v1_0_1-work-007-pairing-qr|MRT-WORK-007]]"
    - "[[v1_0_1-work-013-status-handling|MRT-WORK-013]]"
  releases:
    - "[[v1_0_1-release-002-v1-0-1|MRT-REL-002]]"
  related: []
---

# T1: 엔드투엔드 테스트

같은 Wi-Fi에서 헬퍼↔앱 페어링 → 창 전환 · 매크로 동작을 엔드투엔드로 확인한다.

> 원본: `mac-remote/doc/work/Work-14-e2e-test.md`. 구현 계약은 [[v1_0_1-spec-001-window-list|MRT-SPEC-001]], [[v1_0_1-spec-002-window-focus|MRT-SPEC-002]], [[v1_0_1-spec-003-key-input|MRT-SPEC-003]], [[v1_0_1-spec-004-app-icon|MRT-SPEC-004]], [[v1_0_1-spec-005-websocket-protocol|MRT-SPEC-005]], [[v1_0_1-spec-006-permissions|MRT-SPEC-006]], [[v1_0_1-spec-007-pairing|MRT-SPEC-007]].

## Work Summary

| 항목 | 내용 |
|---|---|
| 상태 | done |
| 시작일 | 2026-05-24 |
| 완료일 | 2026-05-26 |
| 의존 | [[v1_0_1-work-007-pairing-qr\|MRT-WORK-007]], [[v1_0_1-work-013-status-handling\|MRT-WORK-013]] |
| 관련 스펙 | [[v1_0_1-spec-001-window-list\|MRT-SPEC-001]], [[v1_0_1-spec-002-window-focus\|MRT-SPEC-002]], [[v1_0_1-spec-003-key-input\|MRT-SPEC-003]], [[v1_0_1-spec-004-app-icon\|MRT-SPEC-004]], [[v1_0_1-spec-005-websocket-protocol\|MRT-SPEC-005]], [[v1_0_1-spec-006-permissions\|MRT-SPEC-006]], [[v1_0_1-spec-007-pairing\|MRT-SPEC-007]] |

## 참조 스펙 체크리스트

| Spec 섹션 | 항목 | 반영 여부 |
|-----------|------|-----------|
| Spec-07 §7 유저 플로우 | QR 페어링 E2E | [x] |
| Spec-01 §7 유저 플로우 | 창 목록 표시 E2E | [x] |
| Spec-02 §7 유저 플로우 | 창 전환 E2E | [x] |
| Spec-03 §7 유저 플로우 | 매크로 실행 E2E | [x] |

## 태스크

| # | 태스크 | 상태 | 커밋 | 비고 |
|---|--------|------|------|------|
| 1 | QR 페어링 → 연결 성공 | [x] | | |
| 2 | 창 목록 표시 + 아이콘 | [x] | | |
| 3 | 창 전환 (탭 → Mac 활성화) | [x] | | |
| 4 | 매크로 실행 (⌘C, ⌘V 등) | [x] | | |
| 5 | 권한 상태 표시 정확성 | [x] | | |

## 기술 메모

수동 테스트. 실기기 필요.

## 검증 방법 / Acceptance

| # | 검증 항목 | 방법 | 결과 |
|---|----------|------|------|
| 1 | 전체 플로우 | QR 스캔 → 창 목록 확인 → 창 전환 → 매크로 실행 | — |

## 완료 기록

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-05-24 | 최초 작성 |
| 2026-05-26 | done — 실제 배포(1.0.1) 및 운영 사용으로 E2E 플로우 충족 |
