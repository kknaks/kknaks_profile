---
type: spec
id: STL-SPEC-010
title: "세션 도메인 (Session API)"
status: implemented
product: study-timelapse
created_at: 2026-05-18
updated_at: 2026-06-08
tags:
  - product/study-timelapse
  - doc/spec
  - status/implemented
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-001-recording-state-machine|STL-SPEC-001]]"
    - "[[spec-002-capture-pipeline|STL-SPEC-002]]"
    - "[[spec-003-subscription-state-machine|STL-SPEC-003]]"
    - "[[spec-008-mobile-revenuecat-integration|STL-SPEC-008]]"
  works: []
  releases: []
  related: []
---

# 세션 도메인 (Session API)

홈 "Start Focus Session" → 타임랩스 갤러리 저장까지의 세션 흐름과 Session API 계약. 모바일 녹화 흐름([[spec-001-recording-state-machine|STL-SPEC-001]])과 BE Session API 연동, 일일 한도([[spec-003-subscription-state-machine|STL-SPEC-003]]).

> 원본: `medi_docs/current/spec/spec-10-session-domain.md`. frontmatter 에 ADR depends 없음 → `links.decisions` 비움. 녹화/구독 연계는 `links.specs` 로 연결.

## Context

- 짝 spec: 녹화 상태머신([[spec-001-recording-state-machine|STL-SPEC-001]]), 캡처 파이프라인([[spec-002-capture-pipeline|STL-SPEC-002]]), 구독 한도([[spec-003-subscription-state-machine|STL-SPEC-003]])
- 범위: Session/DailyFocus API + 모바일 세션 화면 흐름

## BE Contract (Session Endpoints)

### POST /api/sessions (201)
- Request: `{start_time, output_seconds, aspect_ratio, overlay_style}`
- 검증: `output_seconds ∈ {5,10,15,30,45,60,90,120}`, `aspect_ratio ∈ {9:16,16:9,1:1,4:5,3:4}` → 위반 422
- 일일 한도: free/expired/cancelled(만료) + 오늘 `session_count ≥ 1` → 403 `DAILY_QUOTA_EXCEEDED`. trial/pro 무제한
- Response: SessionResponse (status=`recording`)

### PUT /api/sessions/{id}
- Request(optional): `{end_time, duration, status, file_id, task_id}`
- 완료(`status=completed`+duration): `daily_focus` upsert(사용자 로컬 날짜) + `user.total_focus_time` 누적 + streak 갱신
- `duration` 자동 계산(`end_time - start_time`), 명시 시 우선. tzinfo 있으면 naive 변환
- 404: 타인/미존재 세션

### GET /api/sessions
- Query: `limit`(≤100, 기본 20), `offset`(기본 0). created_at desc

## Data Contract

```text
FocusSession
  id, user_id, start_time(naive), end_time?, duration?(초),
  output_seconds, aspect_ratio, overlay_style(기본 stopwatch),
  status('recording'|'completed'), file_id?, task_id?

DailyFocus (집계)
  id, user_id, date(사용자 로컬 날짜), total_seconds, session_count
```

streak: 오늘부터 과거로 연속 `daily_focus` row 수 → `user.streak`, `longest_streak` 갱신.

## FE Contract (화면 흐름)

```
/ → session-setup → focus(캡처) → generating(stitch) → result(오버레이) → saving(저장)
```
- session-setup: DAILY_QUOTA_EXCEEDED → 한도 모달(resetsAt + paywall)
- 화면 상세 상태는 [[spec-001-recording-state-machine|STL-SPEC-001]]

## Case Matrix (에지)

| 케이스 | 처리 |
|---|---|
| 일일 한도 초과 | 403 + `daily_quota_resets_at` 모달 |
| 집중 >2h + 5s/10s 선택 | 5s/10s 비활성, 15s 자동 |
| output_seconds 허용 외 | 422 |
| 세션 PUT 타인/미존재 | 404 |
| saving 세션 업데이트 실패 | console.warn 무시 (저장 자체 완료) |

## 구현 현황 (코드 grounding)

ground truth: `study_timelapse/backend/` + `frontend/mobile/`. 전 계약 정합 — gap 없음.

| 계약 | 코드 근거 |
|---|---|
| POST /sessions (검증/한도 403/201) | `backend/app/api/v1/sessions.py:28-103`, allowed sets `:24-25` |
| PUT /sessions (완료/daily_focus/streak/404) | `sessions.py:106-170`, daily_focus `:222-246`, streak `:248-263` |
| GET /sessions (limit/offset) | `sessions.py:173-214` |
| 모델 (start_time naive) | `app/models/session.py:13-36`, `app/models/daily_focus.py:13-32` |
| 모바일 6화면 흐름 | `frontend/mobile/app/{index,session-setup,focus,generating,result,saving}.tsx` |

## Open Questions

- 없음 (구현·배포 완료).
