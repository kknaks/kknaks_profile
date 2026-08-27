---
type: decision
id: STL-DEC-005
title: "캡처 스케줄 함수 — Sqrt 스케줄 채택"
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
    - "[[decision-007-stop-confirmation-ux|STL-DEC-007]]"
    - "[[decision-008-cache-lifecycle|STL-DEC-008]]"
  specs: []
  works: []
  releases: []
  related: []
up: []
---

# 캡처 스케줄 함수 — Sqrt 스케줄 채택 (ADR-05)

캡처 타이머가 각 프레임을 언제 찍을지 결정하는 스케줄 함수로 Sqrt 를 채택한다. `schedule(t) = ceil(N_total × √(t / goalSec))` — 초반 집중·후반 여유 + 종점 정확 + 짧은 녹화 보호를 수식 1줄로 만족.

> 원본: `study_timelapse/medi_docs/current/adr/adr-05-capture-schedule-function.md`. [[decision-004-recording-paradigm|STL-DEC-004]] 의존.

## Context

- 프레임 샘플링 채택 후 "언제 찍을지" 스케줄 함수 필요.
- 입력: `goalSec`, `outputSec`, `outputFps`(기본 30), `N_total = outputSec × outputFps`.
- 6 보장 속성: 입력 의존 / 종점 정확 / 단조 증가 / 짧은 녹화 보호 / 연속 수식 / 인터벌 floor 가드.

## 근거 개념

없음 — 캡처 시점을 정하는 수식을 고른 결정이다.

## Options

| Option | 수식 | 짧은 녹화(4h·30초 정지) | 종점 정확 |
|---|---|---|---|
| A Linear | `ceil(N_total × t/goalSec)` | 4장 (취약) | ✅ |
| B Sqrt (채택) | `ceil(N_total × √(t/goalSec))` | 22장 (보호) | ✅ |
| C Power(α) | `ceil(N_total × (t/goalSec)^α)` | α=0.5 시 B와 동일 | ✅ |
| D Log | `ceil(N_total × log(1+t/goalSec)/log2)` | 높음 | ✅ (보정 필요) |
| E 계단식 lookup | 손튜닝 테이블 | 설계 의존 | 별도 보정 |

## Decision

**B 채택 — Sqrt 스케줄.** `schedule(t) = ceil(N_total × √(t / goalSec))`, `t_N = goalSec × (N / N_total)²`.

- 수식 1줄로 6 보장 속성 모두 만족.
- "초반 자주, 후반 띄엄" 사용자 직관과 일치.
- 인터벌 floor 가드: `max(interval_N, 100ms)` — 함수 본체 밖 clamp.
- α=0.5 고정 (0.3~0.7 조정은 spec 단계 정책화).

## 구현 현황

- 정합. `frontend/mobile/app/focus.tsx` — `estimatedOutputSec`(`focus.tsx:403`)이 sqrt 스케줄 기반 예상 길이를 계산. 캡처 시점 판정은 VisionCamera frame processor plugin([[decision-009-camera-integration|STL-DEC-009]]) 내 `nextCaptureTime` 순수 함수로 수행.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | N_total 상한(디스크 예산) 정의 | — | resource-budget 정책 |
| — | 인터벌 floor·종점 보정 구현 정밀 명세 | — | capture-pipeline spec |
