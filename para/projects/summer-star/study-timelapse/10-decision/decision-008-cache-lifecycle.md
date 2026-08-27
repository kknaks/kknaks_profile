---
type: decision
id: STL-DEC-008
title: "캐시 파일 생명주기 — stitch 즉시 삭제 + 캡처 프레임 5분 TTL"
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
up:
  - terminal-state-ttl
  - caching
---

# 캐시 파일 생명주기 — stitch 즉시 삭제 + 캡처 프레임 5분 TTL (ADR-08)

saving 완료 즉시 stitch MP4 를 정리하고, 캡처 프레임은 5분 재시도 윈도우 후 자동 삭제한다(D안). 재시도 가능성과 디스크 자동 회수의 균형.

> 원본: `study_timelapse/medi_docs/current/adr/adr-08-cache-lifecycle.md`. [[decision-004-recording-paradigm|STL-DEC-004]] 의존.

## Context

- 프레임 샘플링으로 캡처 프레임(JPEG ~1.8GB/4h)과 stitch MP4(~50~150MB) 캐시 발생. 현행 cleanup 호출 없음 → 세션마다 누적 → 디스크 부족(E3).
- "녹화본은 saving 완료 전까지 삭제되지 않는다" 신뢰성 원칙.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[terminal-state-ttl]] — 캡처 프레임을 **5분 뒤 자동 삭제**한다 — 재시도 창과 디스크 회수 사이를 시간으로 가른 것이라, 끝난 것을 얼마나 들고 있을지의 문제 그대로다
- [[caching]] — stitch MP4 는 즉시, 프레임은 TTL 로 정리한다. **다시 만들 수 있는 것**이라 버려도 되지만 재시도 동안은 남겨 둔다

## Options

| Option | 캡처 프레임 삭제 | stitch MP4 삭제 | 재시도 |
|---|---|---|---|
| A | saving 완료 즉시 | saving 완료 즉시 | ❌ |
| B | 24h TTL | saving 완료 즉시 | ✅ 24h |
| C | 즉시 + generating 실패 시 보존(resume) | saving 완료 즉시 | ✅ (resume 구현 시) |
| D (채택) | saving 완료 + 5분 TTL 후 자동 삭제 | saving 완료 즉시 | ✅ 5분 |

## Decision

**D 채택 — stitch MP4 즉시 삭제 + 캡처 프레임 5분 TTL.**

- A: stitch 실패 시 4시간치 재촬영 → 치명적. B: 24h 유지 시 디스크 포화 위험. C: resume 는 Phase 1 범위 초과.
- 5분 = generating(수십초) 대비 충분한 재시도 버퍼, 디스크 점유 짧음.
- 세션 취소(Exit)는 캡처 + stitch 즉시 삭제.

## 구현 현황

- 정합. `frontend/mobile/app/saving.tsx:172` — 갤러리 저장 완료 후 stitch(`finalPath`) `FileSystem.deleteAsync` 즉시 호출.
- `saving.tsx:194` — `setTimeout(() => FileSystem.deleteAsync(captureDir …))` 캡처 디렉토리 지연 삭제.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 5분 TTL 적정값(1분/10분 조정) | 사용자/admin | 운영 피드백 |
| — | 캡처 디렉토리 최대 크기·E3 경고 임계값 | — | resource-budget 정책 |
