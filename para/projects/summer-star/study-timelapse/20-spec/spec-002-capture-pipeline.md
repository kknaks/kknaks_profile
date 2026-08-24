---
type: spec
id: STL-SPEC-002
title: "캡처 파이프라인 (Native 모듈)"
status: implemented
product: study-timelapse
created_at: 2026-05-04
updated_at: 2026-06-08
tags:
  - product/study-timelapse
  - doc/spec
  - status/implemented
links:
  baselines: []
  decisions:
    - "[[decision-004-recording-paradigm|STL-DEC-004]]"
    - "[[decision-005-capture-schedule-function|STL-DEC-005]]"
    - "[[decision-007-stop-confirmation-ux|STL-DEC-007]]"
    - "[[decision-008-cache-lifecycle|STL-DEC-008]]"
    - "[[decision-009-camera-integration|STL-DEC-009]]"
  specs:
    - "[[spec-001-recording-state-machine|STL-SPEC-001]]"
  works: []
  releases: []
  related: []
---

# 캡처 파이프라인 (Native 모듈)

프레임 샘플링 기반 캡처 파이프라인의 native 모듈 인터페이스 계약. N초마다 JPEG 1장 캡처([[decision-004-recording-paradigm|STL-DEC-004]] + [[decision-005-capture-schedule-function|STL-DEC-005]]) → AVAssetWriter stitch → 옵션 burn-in. 카메라는 VisionCamera frame processor plugin 단독 점유([[decision-009-camera-integration|STL-DEC-009]]).

> 원본: `medi_docs/current/spec/spec-02-capture-pipeline.md`. 원본의 Swift/TS 구현 윤곽(AVAssetWriter 코드, frame processor 본문)·D-SPEC 선택지는 30-work/구현 영역이므로 제외하고, 모듈 함수 표면·이벤트·enum·디렉토리 계약만 둔다.

## Context

- 관련 decision: 프레임 샘플링 패러다임([[decision-004-recording-paradigm|STL-DEC-004]], 무음), sqrt 스케줄([[decision-005-capture-schedule-function|STL-DEC-005]]), stitch 시점 burn-in 연동([[decision-007-stop-confirmation-ux|STL-DEC-007]]), 캐시 위치/TTL([[decision-008-cache-lifecycle|STL-DEC-008]]), 카메라 통합([[decision-009-camera-integration|STL-DEC-009]])
- 짝 spec: 상태 전이 [[spec-001-recording-state-machine|STL-SPEC-001]] (이 모듈을 호출하는 화면 상태머신)
- 범위
  - In: native 모듈 함수 시그니처, 진행/에러 이벤트, sqrt 스케줄 함수, 해상도/오버레이 enum, 캡처 디렉토리 계약
  - Out: 화면 상태 전이([[spec-001-recording-state-machine|STL-SPEC-001]]), 오버레이 시각 디자인

## BE Contract (Native 모듈 함수 표면)

카메라 device 점유는 VisionCamera 단독([[decision-009-camera-integration|STL-DEC-009]]). 우리 모듈은 frame processor plugin 으로만 동작하며 자체 `AVCaptureSession`/`DispatchSourceTimer`를 두지 않는다.

| 함수 | 시그니처 | 역할 |
|---|---|---|
| `startCapture` | `(opts: CaptureStartOptions) => Promise<void>` | captureDir 생성 + 누적 상태 초기화 |
| `pauseCapture` | `() => Promise<void>` | frame 흐름/플래그 일시정지 |
| `resumeCapture` | `() => Promise<void>` | 재개 (pause 구간 elapsed 제외) |
| `stopCapture` | `() => Promise<CaptureResult>` | 정지 + `{captureCount, captureDir, elapsedSec}` 반환 |
| `stitchTimelapse` | `(opts: StitchOptions) => Promise<string>` | frame 시퀀스 → MP4 (generating·saving 양쪽) |

### CaptureStartOptions (입력 계약)

| 필드 | 타입 | 비고 |
|---|---|---|
| `sessionId` | string | 디렉토리 구분 |
| `goalSec` | number | 목표 집중 시간(초) |
| `outputSec` | number | 출력 타임랩스 길이(초) |
| `outputFps` | number | 30 고정 |
| `aspectRatio` | string | `'9:16'|'1:1'|'16:9'|'4:5'|'3:4'` |
| `cameraFacing` | `'front'|'back'` | 시작 전에만 전환 |
| `captureDir` | string | documentDirectory 하위 ([[decision-008-cache-lifecycle|STL-DEC-008]]) |

### StitchOptions (입력 계약)

| 필드 | 타입 | 비고 |
|---|---|---|
| `captureDir` | string | frame_NNNNNN.jpg 시퀀스 |
| `outputPath` | string | 출력 MP4 경로 |
| `width`,`height` | number | aspectRatio 기반 사전 계산 (SIZE_MAP) |
| `outputFps` | number | 30 |
| `overlayStyle` | OverlayStyle | `'none'`이면 burn-in 없음 |
| `overlayMeta.showAppMark` | bool | 워터마크 (Free=true, Pro/Trial=false) |

### 이벤트

| 이벤트 | payload | 시점 |
|---|---|---|
| `onCaptureProgress` | `{count, totalEstimate, nextAtMs, previewSec}` | 매 캡처 후 |
| `onStitchProgress` | `{progress: 0.0~1.0}` | stitch 진행 |
| `onCaptureError` | `{code, message}` | 비동기 캡처 실패 |

## Validation (캡처 스케줄 계약, [[decision-005-capture-schedule-function|STL-DEC-005]])

| 항목 | 규칙 |
|---|---|
| 목표 총 프레임 | `N_total = outputSec × outputFps` |
| N번째 캡처 시각 | `t_N = goalSec × (N / N_total)²` (sqrt 스케줄) |
| frame processor 판정 | 매 frame 마다 `elapsedSec ≥ t_N` 이면 캡처, 아니면 drop |
| 0장 캡처 stitch | `empty_capture_dir` throw (최소 캡처 보장) |
| outputFps | 30 고정 ([[decision-005-capture-schedule-function|STL-DEC-005]] 입력 변수 안정) |

## Data Contract

```text
OverlayStyle  = 'none' | 'timer-up' | 'timer-down' | 'progress' | 'streak'

SIZE_MAP (aspectRatio → [width, height])
  '9:16' → 720×1280   '1:1' → 720×720    '16:9' → 1280×720
  '4:5'  → 720×900    '3:4' → 810×1080

디렉토리: {documentDirectory}/sessions/{sessionId}/captures/frame_%06d.jpg
출력 MP4: H.264, ~3.5 Mbps, 오디오 트랙 없음 (무음, STL-DEC-004)
```

오버레이 burn-in 시점: raw JPEG 보존 → stitch 시점에 frame 별 burn-in (preview.mp4 = 오버레이 없음, 최종 mp4 = 선택 오버레이 + 워터마크).

## 구현 현황 (코드 grounding)

ground truth: `study_timelapse/frontend/mobile/`. 전 계약 요소 코드 정합 — gap 없음.

| 계약 | 코드 근거 |
|---|---|
| frame processor plugin | `app/focus.tsx:28,181-193` (`captureTimelapseFrame`), `ios/TimelapseCreatorModule.swift:87-92` 등록, `:73` "AVCaptureSession/DispatchSourceTimer 폐기" |
| sqrt 스케줄 | `ios/TimelapseCreatorModule.swift:16-19` (`goalSec * pow(n/totalFrames, 2.0)`), `:17` `N_total = outputSec*outputFps` |
| 모듈 함수 | `modules/timelapse-creator/src/TimelapseCreatorModule.ts:74-78`, Swift `ios/TimelapseCreatorModule.swift:102-126` |
| 이벤트 | `ios/TimelapseCreatorModule.swift:94-98`, onStitchProgress `:306` |
| outputFps 30 / SIZE_MAP / overlay enum | `src/constants/captureTuning.ts:2`, `app/generating.tsx:10-16`, `app/result.tsx:18` |
| 디렉토리/파일명 | documentDirectory `app/focus.tsx:199,209`, `frame_%06d.jpg` `ios/TimelapseCreatorModule.swift:28-29` |
| AVAssetWriter H.264 3.5Mbps 무음 | `ios/TimelapseCreatorModule.swift:242-252` |
| 워터마크 showAppMark | `ios/TimelapseCreatorModule.swift:350-378` |

## Open Questions

- 없음 (구현·배포 완료). D-SPEC-2-1(B)/2-2(B)/2-3(A) 모두 코드 반영 확인.
