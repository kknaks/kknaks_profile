---
type: decision
id: MRT-DEC-003
title: "화면 캡처 대신 앱 아이콘만 표시"
status: archived
original_status: accepted
archived_version: v1.0.1
archived_at: 2026-06-08
product: mac-remote
created_at: 2026-05-24
updated_at: 2026-06-01
tags:
  - product/mac-remote
  - doc/decision
  - status/archived
links:
  baselines:
    - "[[v1_0_1-baseline-001-iphone-mac-remote-idea|MRT-BL-001]]"
  decisions:
    - "[[v1_0_1-decision-002-cgwindowlist-window-source|MRT-DEC-002]]"
  specs:
    - "[[v1_0_1-spec-004-app-icon|MRT-SPEC-004]]"
  works: []
  releases: []
  related: []
---

# 화면 캡처 대신 앱 아이콘만 표시 (ADR-003)

iOS 앱에서 창을 식별할 시각 요소로 창 썸네일/스크린샷 대신 앱 아이콘만 표시한다.

> 원본: `mac-remote/doc/Decision.md` ADR-003.

## Context

- 관련 baseline: [[v1_0_1-baseline-001-iphone-mac-remote-idea|MRT-BL-001]]
- iOS 앱에서 창을 식별할 시각적 요소가 필요하다.
- 핵심 제약: 화면 캡처/썸네일 금지.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 앱 아이콘만 | NSWorkspace로 설치된 앱 아이콘 읽기 | 권한 불필요, 앱당 1개 캐싱 효율 | 같은 앱 여러 창은 아이콘 동일 | 채택 |
| 창 썸네일/스크린샷 | ScreenCaptureKit 지속 캡처 | 창 내용 구분 가능 | 권한 추가, 성능 부담 | 기각 |

## Decision

- 채택: 창 썸네일/스크린샷 대신 앱 아이콘만 표시.
- 기각: 지속적 화면 캡처.
- 보류: 없음.

## Rationale

- 판단 기준: 권한 최소화, 성능, 캐싱 효율.
- 대안 대비 이유: 화면 캡처는 ScreenCaptureKit 권한이 추가로 필요하고, 지속적 캡처는 성능 부담이 크다. 앱 아이콘은 NSWorkspace로 권한 없이 읽을 수 있고, 앱당 1개로 캐싱 효율이 높다.
- 리스크: 같은 앱의 여러 창은 아이콘이 동일하므로 창 제목으로 구분해야 한다.

## Scope

- In: 앱 아이콘 수집(Spec-04).
- Out: 화면 캡처/썸네일.
- 영향을 받는 spec 후보: [[v1_0_1-spec-004-app-icon|MRT-SPEC-004]].

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 없음 | | |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| MRT-SPEC-004 | create | NSWorkspace 기반 앱 아이콘. 같은 앱 여러 창은 창 제목으로 구분 |
