# [planner] DAY-SPEC-000 동기화 — #225 구현 · 검수에서 나온 결정과 정리 (PR #909 같은 워크트리 · 미커밋으로)

너는 day planner 워커다. 계약 그대로 — 같은 mediness 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec`. 커밋 금지.
읽을 것: 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-225-report.md`(「판단한 곳」 판정 · 「조용히 통과」 5 · 6) · 구현 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-225-report.md`(「판단한 곳」) · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/README.md`(공통 규칙 「유일 · 삭제」 새 줄) · `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/07-misc.md`(chat_room.direct_key).

## 반영할 것

1. **사용자 결정 2026-11-05** — (a) 유일은 살아 있는 행만: §2 공통 규칙에 원천 새 줄 그대로 · 각 표의 UNIQUE 표기는 그대로 두되 §2 를 가리키게. (b) `chat_room.direct_key` = UNIQUE(hospital_id, direct_key).
2. **구현이 정한 것 — 표에 적기**(검수가 받아들임 · 「SPEC 정리 요청」): 「uuid FK」만 적힌 칸의 대상(구현 리포트 목록 그대로) · 02 코드 테이블 5개 타입 · 필수(구현 그대로) · `event_log` · `push_log` · `external_outbox` 의 `deleted_at`(§2 우선 — 「쌓기만」 문장과 부딪히지 않게 한 줄) · 하위 테이블은 `hospital_id` 를 부모로 안다는 한 줄(§2).
3. 40-architecture/erd.md 에 영향이 있으면 같이(direct_key).
4. log.md 한 줄 · lint `--strict` 1회.

새 결정을 만들지 마라 — 위 목록 밖 차이를 찾으면 리포트 「제안」으로.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec000-sync-report.md`. 완료는 preamble 의 worker_done 절차대로.
