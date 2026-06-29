---
id: STL-WORK-003
title: Session stats persistence and timezone fix
status: todo
progress: 0
type: bugfix
owner: kknaks
created: 2026-06-21
updated: 2026-06-21
target_release: TestFlight-before-submit
links:
  specs:
    - "[[spec-003-subscription-state-machine|STL-SPEC-003]]"
    - "[[spec-005-subscription-data-model|STL-SPEC-005]]"
    - "[[spec-010-session-domain|STL-SPEC-010]]"
    - "[[spec-012-stats-domain|STL-SPEC-012]]"
    - "[[spec-013-users-api|STL-SPEC-013]]"
  decisions: []
  prs: []
---

# STL-WORK-003 Session Stats Persistence And Timezone Fix

## Summary

사용자가 완료한 focus session 기록이 다음날 통계/캘린더에서 사라져 보이는 문제를 막는다. 원본 세션 저장, `daily_focus` 일별 집계, stats/users 조회, 모바일 날짜 표시가 모두 사용자 timezone 기준으로 같은 날짜를 보도록 정렬한다.

## Problem

현재 코드는 세션 원본(`sessions`)과 일별 집계(`daily_focus`)가 분리되어 있다. 앱의 Home/Stats 화면은 대부분 `daily_focus` 기반 stats API를 보므로, 집계가 누락되거나 잘못된 날짜에 들어가면 세션 원본이 남아 있어도 사용자는 기록이 사라진 것으로 본다.

## Code Findings

| Area | Finding | Code |
|---|---|---|
| Session completion date | `PUT /sessions/{id}` 완료 시 `_update_daily_focus()`가 session timestamp가 아니라 `datetime.now(user.timezone).date()`를 사용한다. 자정 경계 또는 저장 지연 시 기록 날짜가 실제 세션 날짜와 달라질 수 있다. | `backend/app/api/v1/sessions.py` |
| Stats default date | `/stats/daily`, `/stats/weekly` 기본 기준일이 `date.today()`라서 서버 timezone 날짜를 쓴다. 사용자 timezone과 다르면 조회 범위가 하루 밀릴 수 있다. | `backend/app/api/v1/stats.py` |
| Mobile today date | Home/Stats가 `new Date().toISOString().split('T')[0]`로 오늘을 계산한다. 한국 시간 오전 9시 전에는 UTC 전날 날짜가 되어 today 매칭이 틀어질 수 있다. | `frontend/mobile/app/index.tsx`, `frontend/mobile/app/stats.tsx` |
| Non-idempotent completion | 이미 완료된 session에 `status=completed` PUT이 다시 들어오면 `daily_focus`와 `user.total_focus_time`이 중복 증가한다. | `backend/app/api/v1/sessions.py` |
| Silent stats loss | 저장 화면에서 `updateSession()` 실패를 `console.warn`만 남기고 완료 처리한다. 로컬 동영상은 저장되지만 서버 통계 집계는 빠질 수 있다. | `frontend/mobile/app/saving.tsx` |

## Goal

- 완료된 session은 사용자 로컬 날짜 기준으로 정확히 한 번 `daily_focus`에 반영된다.
- stats/users API 기본 날짜는 사용자 timezone 기준이다.
- 모바일 today/week/month 매칭은 UTC 문자열 파생 날짜에 의존하지 않는다.
- 세션 PUT 실패 시 사용자가 통계 저장 실패를 인지하거나 재시도할 수 있다.

## Non-Goals

- 기존 잘못 집계된 운영 데이터 전체 마이그레이션은 이 WP에서 직접 수행하지 않는다. 필요 시 별도 backfill work로 분리한다.
- 영상 파일 저장 파이프라인 자체는 변경하지 않는다.

## Phase Plan

### Phase 1. Reproduce And Contract Lock

Status: todo

- [ ] Asia/Seoul 사용자 기준 자정 경계 케이스를 테스트로 재현
- [ ] `sessions` row는 존재하지만 `daily_focus`가 누락/오집계되는 케이스 확인
- [ ] 중복 `completed` PUT 시 집계가 두 번 증가하는 케이스 확인

### Phase 2. Backend Persistence Fix

Status: todo

- [ ] `daily_focus.date`를 session `end_time` 또는 `start_time`을 사용자 timezone으로 변환한 날짜에서 산출
- [ ] naive DB timestamp는 UTC로 해석하는 helper 추가
- [ ] `completed` 전이 시에만 집계하도록 idempotency 보강
- [ ] `/stats/daily`, `/stats/weekly`, `/users/me` 기본 날짜 기준을 사용자 timezone helper로 통일
- [ ] streak 계산 기준도 집계 날짜 기준으로 일관화

### Phase 3. Mobile Display And Failure Handling

Status: todo

- [ ] 모바일 local date formatter 추가
- [ ] Home/Stats today/week date key 생성에서 `toISOString()` 날짜 파생 제거
- [ ] `updateSession()` 실패 시 조용히 성공 처리하지 않도록 retry/user-visible failure 처리
- [ ] 저장 완료 후 stats query invalidation 또는 다음 진입 시 fresh fetch 확인

### Phase 4. QA

Status: todo

- [ ] Backend tests: Asia/Seoul midnight, duplicate completion, stats default date
- [ ] Mobile typecheck
- [ ] E2E: 당일 저장 후 Home/Stats 반영
- [ ] E2E: 다음날 앱 재진입 시 어제 캘린더 dot/weekly total 유지

## Acceptance Criteria

- Asia/Seoul 기준 23:xx~00:xx 경계의 완료 session이 의도한 로컬 날짜에 집계된다.
- 같은 session completion 요청이 재시도되어도 `daily_focus.session_count`, `total_seconds`, `user.total_focus_time`이 중복 증가하지 않는다.
- `/stats/weekly`를 파라미터 없이 호출해도 사용자 로컬 오늘이 포함된 주를 반환한다.
- 모바일 Home의 TODAY 값과 Stats의 TODAY 값이 같은 로컬 날짜 기준으로 표시된다.
- 세션 통계 저장 실패가 사용자에게 숨겨지지 않는다.

## Open Questions

- 이미 잘못 날짜에 들어간 `daily_focus` 운영 데이터 backfill이 필요한가?
- 세션 날짜 기준은 `end_time` 로컬 날짜로 확정할지, 긴 세션의 경우 `start_time` 또는 duration split이 필요한지 결정 필요.

## Release Notes

- TestFlight 전 blocking 후보. Apple Sign-In과 별도로 사용자 신뢰/기록 보존에 직접 영향을 주므로 우선순위 높음.
