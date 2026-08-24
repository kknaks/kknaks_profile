---
type: decision
id: MRT-DEC-002
title: "CGWindowListCopyWindowInfo를 창 목록 수집에 사용"
status: accepted
product: mac-remote
created_at: 2026-05-24
updated_at: 2026-06-01
tags:
  - product/mac-remote
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-iphone-mac-remote-idea|MRT-BL-001]]"
  decisions:
    - "[[decision-003-app-icon-only-no-capture|MRT-DEC-003]]"
  specs:
    - "[[spec-001-window-list|MRT-SPEC-001]]"
  works: []
  releases: []
  related: []
up: []
---

# CGWindowListCopyWindowInfo를 창 목록 수집에 사용 (ADR-002)

Mac에서 현재 열린 창 목록을 `CGWindowListCopyWindowInfo`로 수집한다.

> 원본: `mac-remote/doc/Decision.md` ADR-002.

## Context

- 관련 baseline: [[baseline-001-iphone-mac-remote-idea|MRT-BL-001]]
- Mac에서 현재 열린 창 목록을 수집해야 한다.
- "deprecated 아니냐"는 흔한 오해를 정리할 필요가 있다.

## 근거 개념

없음 — macOS API 둘 중 하나를 고른 선택이다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| CGWindowListCopyWindowInfo | 공식 창 목록 API | deprecated 아님, 권한 부담 적음 | 창 제목은 Screen Recording 권한 필요 | 채택 |
| ScreenCaptureKit | 화면 캡처 기반 | 풍부한 메타데이터 | 불필요한 권한·복잡도 추가 | 기각 |

## Decision

- 채택: `CGWindowListCopyWindowInfo`.
- 기각: ScreenCaptureKit.
- 보류: 없음.

## Rationale

- 판단 기준: 공식성, 권한 최소화.
- 대안 대비 이유: 이 API는 deprecated가 아니다. deprecated된 것은 화면 캡처용 `CGWindowListCreateImage`이며 이 프로젝트는 화면 캡처를 하지 않으므로 무관하다. ScreenCaptureKit은 불필요한 권한과 복잡도를 추가한다.
- 리스크: 화면 기록(Screen Recording) 권한이 있어야 창 제목(kCGWindowName)을 받을 수 있다. 권한 없으면 빈 문자열로 조용히 실패한다.

## Scope

- In: 창 목록 수집(Spec-01).
- Out: 화면 캡처/썸네일.
- 영향을 받는 spec 후보: [[spec-001-window-list|MRT-SPEC-001]].

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 없음 | | |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| MRT-SPEC-001 | create | 창 목록 수집. Screen Recording 권한 없으면 title 빈 문자열 |
