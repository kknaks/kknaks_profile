---
type: decision
id: STL-DEC-006
title: "백그라운드 녹화 정책 — keep-awake + 백그라운드 진입 시 자동 정지"
status: accepted
product: study-timelapse
created_at: 2026-05-04
updated_at: 2026-06-08
tags:
  - product/study-timelapse
  - doc/decision
  - status/accepted
links:
  baselines: []
  decisions:
    - "[[decision-004-recording-paradigm|STL-DEC-004]]"
  specs: []
  works: []
  releases: []
  related: []
up: []
---

# 백그라운드 녹화 정책 — keep-awake + 백그라운드 진입 시 자동 정지 (ADR-06)

iOS 카메라 제약 하에서 idle timer 비활성(화면 꺼짐 방지) + 백그라운드 진입 시 자동 정지 + 사용자 안내(C+A 조합)를 채택한다. 일반 앱 entitlement 범위 내에서 데이터 무결성 보장 최선.

> 원본: `study_timelapse/medi_docs/current/adr/adr-06-background-recording-policy.md`. [[decision-004-recording-paradigm|STL-DEC-004]] 의존.

## Context

- `AVCaptureSession` 은 백그라운드 전환·화면 잠금 시 중단. `multitasking-camera-access` entitlement 는 일반 앱 미제공(심사 탈락 위험).
- 현행 `focus.tsx` 는 AppState listener·idle timer 비활성 미구현 → 백그라운드 전환 시 타이머는 증가하나 캡처 중단 → 데이터 불일치.

## 근거 개념

없음 — iOS 정책 제약 안에서 고를 수 있는 것을 고른 결정이다.

## Options

| Option | 동작 | iOS 가능 | 사용자 영향 |
|---|---|---|---|
| A | 백그라운드 진입 시 즉시 정지 + 알림 | ✅ | 명확하나 화면 꺼짐 중단 위험 남음 |
| B | 백그라운드 계속 녹화 | ❌ entitlement 미제공 | App Store 탈락 |
| C+A (채택) | idle timer 비활성 + 백그라운드 진입 시 자동 정지 + 안내 | ✅ | 화면 꺼짐 방지 + 명확한 정지 |
| D | 화면 잠금 후 계속 | ❌ 물리적 불가 | — |

## Decision

**C+A 채택.**

- B/D 는 iOS 정책·물리적 제약상 불가.
- idle timer 비활성: 공부 중 화면이 꺼지지 않아야 한다는 기대에 부합.
- 백그라운드 진입 시 즉시 정지 + 안내: 현재까지 캡처 프레임 보존 후 stitch 진행 → "데이터 손실 없음" 충족.

## 구현 현황

- 정합. `frontend/mobile/app/focus.tsx:150` — `AppState.addEventListener('change', …)` 백그라운드/비활성 시 자동 정지(주석에 adr-06 명시).
- `focus.tsx:171` — `activateKeepAwakeAsync('focus-recording')`, 종료 시 `deactivateKeepAwake`.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 전화 수신(E1) interruption 을 동일 AppState 처리로 커버 가능 여부 | — | recording-state-machine spec |
| — | 사용자 안내 카피·위치 | — | spec UX 섹션 |
