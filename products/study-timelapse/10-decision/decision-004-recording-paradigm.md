---
type: decision
id: STL-DEC-004
title: "녹화 패러다임 — 프레임 샘플링(음성 제외) + Native 모듈 재작성"
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
    - "[[decision-005-capture-schedule-function|STL-DEC-005]]"
    - "[[decision-006-background-recording-policy|STL-DEC-006]]"
  specs: []
  works: []
  releases: []
  related: []
---

# 녹화 패러다임 — 프레임 샘플링(음성 제외) + Native 모듈 재작성 (ADR-04)

연속 30fps 녹화 대신 N초마다 1프레임 캡처(음성 제외) + Native 모듈 재작성을 채택한다. 음성을 포기해 디스크 약 1/4, 변환 시간 대폭 단축, 발열·배터리 개선 + WYSIWYG 자동 보장.

> 원본: `study_timelapse/medi_docs/current/adr/adr-04-recording-paradigm.md`. D-PLAN-7/8/9 통합.

## Context

- 현행: VisionCamera 연속 30fps 녹화(`audio=true`) + `scaleTimeRange` 배속 변환 + CALayer 오버레이.
- 문제: 4시간 녹화 원본 4~8GB, 변환 수 분, 발열·배터리 부담. RN preview 와 Swift 합성본 불일치(WYSIWYG 버그).

## Options

| Option | 음성 | 녹화 | 변환 | 원본(4h) | WYSIWYG |
|---|---|---|---|---|---|
| A | 포함 | 연속 30fps | scaleTimeRange (현행) | 4~8GB | 이중 경로 유지 |
| B (채택) | 미포함 | N초마다 1캡처 | AVAssetWriter stitch | ~1.8GB | 자동 보장 |
| C | 미포함 | N초마다 1캡처 | ffmpeg-kit-react-native | ~1.8GB | 자동 보장 (외부 패키지 의존) |

## Decision

**B 채택 — 음성 미포함 + 프레임 샘플링 + Native 모듈 재작성.**

- 음성 제거로 비기능 지표 대폭 개선.
- 캡처 시점에 정적 오버레이를 JPEG에 burn-in → preview/저장본 일치 → WYSIWYG 근원 해소.
- C(ffmpeg-kit)는 외부 의존 + AVFoundation HW 가속 포기라 불리.
- 타임랩스는 SNS 공유용 무음이 표준이라 사용자 가치 손실 미미.

## 구현 현황

- 정합. `frontend/mobile/app/focus.tsx:363` — `audio={false}`.
- 재작성된 Native 캡처/stitch: `frontend/mobile/modules/timelapse-creator/ios/VisionCameraTimelapseCapture.swift`.
- 캡처 방법의 구체화는 [[decision-009-camera-integration|STL-DEC-009]] 에서 확정.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | Android(Phase 4) MediaCodec stitch 이식 | — | Phase 4 |
