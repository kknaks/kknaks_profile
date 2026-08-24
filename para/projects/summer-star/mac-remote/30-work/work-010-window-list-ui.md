---
type: work
id: MRT-WORK-010
title: "I3: 창 목록 화면"
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
    - "[[spec-001-window-list|MRT-SPEC-001]]"
    - "[[spec-002-window-focus|MRT-SPEC-002]]"
    - "[[spec-004-app-icon|MRT-SPEC-004]]"
  works:
    - "[[work-009-ws-client|MRT-WORK-009]]"
  releases:
    - "[[release-001-v1-0-0|MRT-REL-001]]"
  related: []
---

# I3: 창 목록 화면

windowList를 카드형 리스트로 표시한다. 앱 아이콘 + 앱 이름 + 창 제목, frontmost 청록 테두리, 탭으로 focus 명령 전송.

> 원본: `mac-remote/doc/work/Work-10-window-list-ui.md`. 구현 계약은 [[spec-001-window-list|MRT-SPEC-001]], [[spec-002-window-focus|MRT-SPEC-002]], [[spec-004-app-icon|MRT-SPEC-004]].

## Work Summary

| 항목 | 내용 |
|---|---|
| 상태 | done |
| 시작일 | 2026-05-24 |
| 완료일 | 2026-05-24 |
| 의존 | [[work-009-ws-client\|MRT-WORK-009]] |
| 관련 스펙 | [[spec-001-window-list\|MRT-SPEC-001]], [[spec-002-window-focus\|MRT-SPEC-002]], [[spec-004-app-icon\|MRT-SPEC-004]] |

## 참조 스펙 체크리스트

| Spec 섹션 | 항목 | 반영 여부 |
|-----------|------|-----------|
| Spec-01 §8 UI/UX | 카드형 리스트, 당겨서 새로고침 | [x] |
| Spec-02 §8 UI/UX | 카드 탭 → focus 전송 | [x] |
| Spec-04 §8 UI/UX | 카드에 앱 아이콘 표시 | [x] |
| Spec-01 §9 엣지 케이스 | 빈 목록, 긴 제목 | [x] |

## 태스크

| # | 태스크 | 상태 | 커밋 | 비고 |
|---|--------|------|------|------|
| 1 | WindowCardView 컴포넌트 | [x] | e37ec2c | 아이콘+이름+제목+상태 |
| 2 | frontmost 창 청록 테두리 | [x] | e37ec2c | Task 1과 동시 구현 (overlay stroke) |
| 3 | 카드 탭 → focus 명령 전송 + 햅틱 | [x] | 93f5b7b | onTapGesture + UIImpactFeedbackGenerator |
| 4 | 당겨서 새로고침 | [x] | 93f5b7b | .refreshable + sendListWindows |
| 5 | 앱 아이콘 캐싱 + 표시 | [x] | 93f5b7b | base64 → Data → UIImage, Dictionary 캐시 |
| 6 | 빈 상태 UI ("열린 창이 없습니다") | [x] | 93f5b7b | 빈 목록 + 연결 끊김 상태 분리 |

## 기술 메모

- base64 String → Data → UIImage → Image
- 아이콘 캐시: Dictionary<String, UIImage>

## 검증 방법 / Acceptance

| # | 검증 항목 | 방법 | 결과 |
|---|----------|------|------|
| 1 | 목록 표시 | Mac에서 창 여러 개 열고 → iOS에서 목록 확인 | 수동 검증 (Xcode 필요) |
| 2 | 창 전환 | 카드 탭 → Mac에서 해당 창 활성화 | 수동 검증 (Xcode 필요) |
| 3 | frontmost 표시 | 활성 창에 청록 테두리 | 수동 검증 (Xcode 필요) |
| 4 | 아이콘 | 앱별 아이콘이 올바르게 표시 | 수동 검증 (Xcode 필요) |

## 완료 기록

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-05-24 | 최초 작성 |
| 2026-05-24 | 전체 태스크 구현 완료 (6/6) |
