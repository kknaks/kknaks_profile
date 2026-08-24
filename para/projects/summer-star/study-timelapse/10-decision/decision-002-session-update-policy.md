---
type: decision
id: STL-DEC-002
title: "세션 업데이트 단일화 — saving 에서만 completed 처리"
status: accepted
product: study-timelapse
created_at: 2026-05-03
updated_at: 2026-06-08
tags:
  - product/study-timelapse
  - doc/decision
  - status/accepted
links:
  baselines: []
  decisions: []
  specs: []
  works: []
  releases: []
  related: []
up:
  - cohesion
---

# 세션 업데이트 단일화 — saving 에서만 completed 처리 (ADR-02)

`updateSession` 이 `generating.tsx` 와 `saving.tsx` 두 곳에서 중복 호출되던 것을 `saving.tsx` 에서만 호출하도록 단일화한다.

> 원본: `study_timelapse/medi_docs/current/adr/adr-02-session-update-policy.md`.

## Context

- `updateSession`(PATCH `/sessions/{id}`) 이 변환 완료(generating)와 갤러리 저장 완료(saving) 두 시점에서 호출됨.
- 동일 `sessionId` 에 두 번 PATCH → status 덮어쓰기, API 중복, 저장 실패 케이스도 `completed` 로 오기록될 위험.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[cohesion]] — 「세션 완료」를 기록하는 자리를 **한 곳(`saving.tsx`)으로 모은다.** 두 화면이 같은 상태를 쓰면 어느 쪽이 진실인지 정할 수 없다

## Options

| Option | Description | Pros | Cons |
|---|---|---|---|
| A (채택) | saving 에서만 (최종 완료 기준) | "완료" = 갤러리 저장까지 포함, 저장 실패 오기록 방지 | generating 메타를 saving 페이로드에 통합 필요 |
| B | generating 에서만 (변환 완료 기준) | duration 즉시 기록 | 저장 실패해도 completed → 사용자 의도와 불일치 |
| C | 현행 유지 (두 번 PATCH) | 단계별 중간 기록 | 중복 호출, 덮어쓰기, 오기록 위험 |

## Decision

**A 채택 — `saving.tsx` 에서만 `updateSession` 호출.**

- "세션 완료"의 의미는 갤러리 저장까지 포함한다. 변환만 끝나고 저장 실패한 케이스를 completed 로 기록하면 의도와 어긋난다.
- generating 의 변환 성공 여부는 status 가 아니라 별도 로깅으로 처리.
- API 중복 호출 제거.

## 구현 현황

- 정합. `frontend/mobile/app/generating.tsx` — `updateSession` 호출 없음.
- `frontend/mobile/app/saving.tsx:19` import, `:177` 호출 — 단일 호출 지점.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 변환 실패(generating crash) 시 세션 status (`failed`/`cancelled`) | — | spec(recording-state-machine) 단계 |
