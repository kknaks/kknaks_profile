---
type: decision
id: MRT-DEC-004
title: "Mac 헬퍼를 먼저 개발"
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
  decisions: []
  specs: []
  works:
    - "[[work-001-cli-prototype|MRT-WORK-001]]"
  releases: []
  related: []
---

# Mac 헬퍼를 먼저 개발 (ADR-004)

핵심 기능(창 목록, 아이콘, 활성화, 키 입력)을 Mac 헬퍼 CLI에서 검증한 뒤 iOS 앱에 착수한다.

> 원본: `mac-remote/doc/Decision.md` ADR-004. 이 결정은 특정 기능 계약이 아니라 개발 순서(work 진행 순서)를 정하는 process decision이다.

## Context

- 관련 baseline: [[baseline-001-iphone-mac-remote-idea|MRT-BL-001]]
- 두 컴포넌트(Mac 헬퍼, iOS 앱)의 개발 순서를 정해야 한다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| Mac 헬퍼 먼저 | CLI에서 핵심 기능 검증 후 iOS | 터미널 즉시 검증, 낯선 iOS 절차 후순위 | iOS 통합이 늦게 드러남 | 채택 |
| iOS 먼저 | UI부터 | 사용자 경험 조기 검증 | 실제 제어 로직 없이는 빈 껍데기 | 기각 |

## Decision

- 채택: Mac 헬퍼를 먼저 만든다. CLI에서 핵심 기능을 검증한 뒤 iOS 앱에 착수한다.
- 기각: iOS 우선.
- 보류: 없음.

## Rationale

- 판단 기준: 검증 속도, 리스크 후순위화.
- 대안 대비 이유: 터미널에서 바로 검증 가능하고, iOS의 시뮬레이터/프로비저닝/권한 등 낯선 절차를 나중으로 미룰 수 있다.
- 리스크: iOS 통합 이슈가 늦게 드러날 수 있음.

## Scope

- In: work 진행 순서 — M1~M7(Mac) → I1~I6(iOS) → T1~T3(통합).
- Out: 기능 계약 자체(각 spec).
- 영향을 받는 work: [[work-001-cli-prototype|MRT-WORK-001]] 이하 전체.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 없음 | | |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| — | — | spec 생성이 아니라 work 진행 순서를 결정 |
