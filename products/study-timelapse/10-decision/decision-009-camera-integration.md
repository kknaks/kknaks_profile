---
type: decision
id: STL-DEC-009
title: "카메라 점유 통합 — VisionCamera frame processor plugin"
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
---

# 카메라 점유 통합 — VisionCamera frame processor plugin (ADR-09)

프레임 샘플링에서 "1장을 어떻게 얻을지"의 캡처 방법으로 VisionCamera frame processor plugin(B-3)을 채택한다. 자체 `AVCapturePhotoOutput` 의 셔터음·점유 충돌·timer crash 를 원천 회피.

> 원본: `study_timelapse/medi_docs/current/adr/adr-09-camera-integration.md`. [[decision-004-recording-paradigm|STL-DEC-004]] 와 별개 축(캡처 방법).

## Context

- [[decision-004-recording-paradigm|STL-DEC-004]] 는 "얼마나 자주" 만 결정, "어떻게 1장을" 은 미명시.
- 자체 `AVCapturePhotoOutput` 구현 결과 3가지 치명 문제: 셔터음 강제(8초×4h=1,800회), VisionCamera 와 device 점유 충돌(preview 멈춤), `DispatchSourceTimer` resume 누락 crash.

## Options

| Option | 동작 | 셔터음 | VisionCamera 충돌 |
|---|---|---|---|
| B-1 | `AVCapturePhotoOutput` | 🔊 강제 | ❌ 점유 충돌 |
| B-2 | 자체 `AVCaptureVideoDataOutput` + delegate | ❌ 무음 | ❌ 점유 충돌 잔존 |
| B-3 (채택) | VisionCamera frame processor plugin | ❌ 무음 | ✅ 카메라 1개 단독 점유 |

## Decision

**B-3 채택 — VisionCamera frame processor plugin.**

- 카메라는 VisionCamera 만 점유, 우리 plugin 은 frame stream 에 얹혀 schedule 시점에 frame → JPEG 저장.
- 셔터음 없음, preview 유지, capture pipeline 단순화.
- B-1: 셔터음은 iOS 시스템 정책이라 우회 불가. B-2: device point-of-truth 이중화 시 contention 상존.

## 구현 현황

- 정합. `frontend/mobile/modules/timelapse-creator/ios/VisionCameraTimelapseCapture.swift` + `VisionCameraTimelapseCapturePlugin.m` (frame processor plugin).
- `frontend/mobile/app/focus.tsx:181` — `useFrameProcessor`, `:367` `<Camera frameProcessor={…}>`.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | expo-modules-core ↔ VisionCamera plugin 등록 패턴 정밀 검증 | — | 구현 단계 검증됨 (현 코드 동작) |
