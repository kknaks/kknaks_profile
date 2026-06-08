---
type: decision
id: STL-DEC-001
title: "비율 4:5 통일 — 백엔드 VALID_ASPECT_RATIOS 수정"
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
---

# 비율 4:5 통일 — 백엔드 VALID_ASPECT_RATIOS 수정 (ADR-01)

모바일이 허용하는 `4:5` 비율이 백엔드 `VALID_ASPECT_RATIOS` 에 없어 `createSession` 400 오류가 나던 문제를, 백엔드에 `4:5` 를 추가하고 `4:3` 을 제거해 해소한다.

> 원본: `study_timelapse/medi_docs/current/adr/adr-01-aspect-ratio-unify.md`.

## Context

- 모바일(React Native)은 비율 옵션 `9:16 / 1:1 / 16:9 / 4:5 / 3:4` 를 제공한다.
- 백엔드(FastAPI) 세션 API의 `VALID_ASPECT_RATIOS` 는 `9:16 / 16:9 / 1:1 / 4:3 / 3:4` 라 `4:5` 를 허용하지 않았다.
- 결과: `4:5` 로 `createSession` 호출 시 400 → 세션 메타 기록 누락. (타임랩스 영상 자체는 로컬 생성)
- 인스타그램 세로 포맷(`4:5`)이 핵심 SNS 공유 시나리오라 즉시 해소 대상.

## Options

| Option | Description | Pros | Cons |
|---|---|---|---|
| A (채택) | 4:5 통일 — 백엔드에 `4:5` 추가, `4:3` 제거 | SNS 세로 포맷 최적, 모바일 UI 변경 0, 백엔드 1줄 수정 | 기존 `4:3` row 존재 시 마이그레이션 고려 |
| B | 4:3 통일 — 모바일 `4:5` → `4:3` | 전통 사진 비율 호환 | 인스타 세로 포맷 제거, 모바일 UI·해상도 변경 비용 |
| C | 둘 다 지원 (4:3 + 4:5) | 선택지 최대 | 비율 6종 → UI 복잡, 해상도 정의 추가 |

## Decision

**A 채택 — 4:5 통일, 백엔드 `VALID_ASPECT_RATIOS` 수정.**

- 인스타그램 세로 포맷(`4:5`)이 핵심 공유 시나리오 표준 비율.
- 상수 집합 1줄 수정으로 해결 → 모바일 UI·해상도 변경 비용 0.
- `aspect_ratio` 컬럼이 `String` 이라 alembic migration 불필요.

## 구현 현황

- 정합. `backend/app/api/v1/sessions.py:25` — `VALID_ASPECT_RATIOS = {"9:16", "16:9", "1:1", "4:5", "3:4"}` (4:5 포함, 4:3 제거됨).
- 검증은 `sessions.py:45` 에서 수행.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 운영 DB에 기존 `4:3` row 존재 시 마이그레이션 (현재 dev 데이터는 무시) | — | 운영 배포 전 확인 |
