---
type: decision
id: STL-DEC-007
title: "정지 확인 UX — 실시간 인디케이터 + 정지 확인 모달"
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
    - "[[decision-005-capture-schedule-function|STL-DEC-005]]"
  specs: []
  works: []
  releases: []
  related: []
---

# 정지 확인 UX — 실시간 인디케이터 + 정지 확인 모달 (ADR-07)

화면에 현재 예상 결과 길이를 상시 표시하는 인디케이터 + 정지 버튼 탭 시 확인 모달(A+B 조합)을 채택한다. 정지 전 결과를 인지하고 실수 정지도 방지.

> 원본: `study_timelapse/medi_docs/current/adr/adr-07-stop-confirmation-ux.md`. [[decision-004-recording-paradigm|STL-DEC-004]] · [[decision-005-capture-schedule-function|STL-DEC-005]] 의존.

## Context

- sqrt 스케줄([[decision-005-capture-schedule-function|STL-DEC-005]]) 특성상 정지 시점에 따라 결과 길이가 크게 달라짐 (4h 설정·30분 정지 ≈ 16.7초, 2시간 정지 ≈ 42.4초).
- 현행 `focus.tsx` 는 정지 버튼 탭 시 즉시 정지(확인 없음) + 결과 길이 미표시.

## Options

| Option | 동작 | 장점 | 단점 |
|---|---|---|---|
| A | 인디케이터만 (실시간 예상 길이) | 항상 인지 | 잘못 누름 방지 안 됨 |
| B | 정지 모달만 | 잘못 누름 방지 | 평소 길이 인지 안 됨 |
| A+B (채택) | 인디케이터 상시 + 정지 탭 시 모달 | 인지 + 방지 모두 | 모달 1단계 추가(마찰 미미) |
| C | result 화면 사후 안내 | 구현 없음 | 정지 후에야 결과 인지 — 늦음 |

## Decision

**A+B 채택.**

- 인디케이터 표시: `"정지 시 결과 영상 약 {Z}초"`, `Z = floor(N_total × √(elapsed/goalSec)) / outputFps`, 매초 갱신.
- 정지 탭 → 확인 모달("계속하기" / "정지하고 타임랩스 생성").
- 자동 정지(타이머 만료)·백그라운드 강제 정지([[decision-006-background-recording-policy|STL-DEC-006]])는 모달 없이 즉시 정지(의도된 정지).

## 구현 현황

- 정합. `frontend/mobile/app/focus.tsx:403` — `"정지 시 결과 영상 약 {estimatedOutputSec}초"` 상시 인디케이터.
- `focus.tsx:485` — 정지 확인 모달 카피(`"결과 영상 약 {estimatedOutputSec}초."`).

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 모달 카피 최종 확정·디자인 | — | spec UX 섹션 |
