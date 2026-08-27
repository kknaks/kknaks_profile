---
type: spec
id: STL-SPEC-012
title: "Stats 도메인 (통계 API)"
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
    - "[[spec-010-session-domain|STL-SPEC-010]]"
    - "[[spec-003-subscription-state-machine|STL-SPEC-003]]"
    - "[[spec-008-mobile-revenuecat-integration|STL-SPEC-008]]"
  works: []
  releases: []
  related: []
---

# Stats 도메인 (통계 API)

`daily_focus` 기반 일별·주간 포커스 시간/streak 을 제공하는 BE API + 모바일 Stats 화면 계약.

> 원본: `medi_docs/current/spec/spec-12-stats-domain.md`. frontmatter 에 ADR depends 없음 → `links.decisions` 비움. 세션 집계 출처는 [[spec-010-session-domain|STL-SPEC-010]].

## Context

- 짝 spec: 세션 집계 [[spec-010-session-domain|STL-SPEC-010]] (daily_focus 생성), 구독 상태 [[spec-003-subscription-state-machine|STL-SPEC-003]] (설정 sync)
- 범위: stats API + 모바일 stats 화면

## BE Contract (Stats Endpoints)

### GET /api/stats/daily
- Query: `start_date`(기본 오늘-30일), `end_date`(기본 오늘)
- Response: `[{date, total_seconds, session_count}]` — 데이터 없는 날 미포함(sparse), 날짜 오름차순

### GET /api/stats/weekly
- Query: `target_date`(기본 오늘)
- Response: `{week_start, week_end, total_seconds, session_count, daily[], streak, longest_streak}`
- 주 시작 = 월요일(ISO). `week_start = target_date - weekday`, `week_end = +6`
- `streak`/`longest_streak` = User 누적값 그대로

## FE Contract (모바일 stats.tsx)

| 섹션 | 내용 |
|---|---|
| 오늘/Streak 카드 | 오늘 누적 시간 + streak |
| 주간 바 차트 | 7일 바, 탭 시 말풍선 |
| 월별 캘린더 | 세션 있는 날 점, 탭 시 말풍선 |
| Settings 모달 | 이름 편집·구독 sync·로그아웃·Upgrade |

- 구독 sync: `POST /sync` + invalidate, 30초 쿨다운 ([[spec-008-mobile-revenuecat-integration|STL-SPEC-008]])

## 구현 현황 (코드 grounding)

ground truth: `study_timelapse/backend/` + `frontend/mobile/`.

| 계약 | 코드 근거 | 정합 |
|---|---|---|
| GET /stats/daily (sparse/asc) | `backend/app/api/v1/stats.py:18-57` | ✅ |
| GET /stats/weekly (월요일 ISO/daily/streak) | `stats.py:60-111` | ✅ |
| 모바일 stats 화면(카드/바/캘린더/설정/sync) | `frontend/mobile/app/stats.tsx` (sync `:83-101,462`) | ✅ |
| stats API timezone | `stats.py:26-33` (`date.today()` UTC, 사용자 tz 미적용) | ⚠ 알려진 부채 |

## Open Questions

- **[known debt] stats API timezone 미적용** — `daily_focus.date` 저장은 사용자 timezone 기준([[spec-010-session-domain|STL-SPEC-010]])이나, stats 조회는 `date.today()`(UTC) 파라미터 기준(`stats.py:26-33`). UTC 자정 경계에서 non-UTC 사용자 날짜 정렬 불일치 가능. 원본 spec 도 "알려진 부채"로 명시. 핵심 계약은 동작하므로 status=implemented 유지하되 tz-aware 조회 보강 필요.
