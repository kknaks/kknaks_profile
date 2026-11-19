# planner 2차 — 삭제 규칙 추가 (사용자 2026-11-19)

「upsert · 삭제」 절에 아래를 원칙으로 넣는다.

## 원칙

1. **삭제는 소프트 딜리트만 쓴다.** `deleted_at` 을 채우고 행은 지우지 않는다. 동기화 · 백필 · 환불 · 어떤 경로든 물리 삭제(DELETE)는 금지다.
2. **지우면 로그를 남긴다.** 이번에 동기화하는 새 테이블(SPEC-000 §4)에서 `deleted_at` 을 채울 때마다 `event_log` 에 한 줄을 쌓는다.
   - 대상 경로는 셋이다:
     - KOS `deleted:true`
     - 응답에서 사라짐(`mark_absent`)
     - DAY 동작(예: 선불카드 환불 완료 회수)
   - 되살아날 때(KOS 에 다시 나타나 `deleted_at` 을 비울 때)도 한 줄을 쌓는다.

## event_log 칸 (지금 dev 모델 그대로 · 칸 추가 없음)

`event_log` = `hospital_id` · `occurred_at` · `actor_staff_id`(nullable) · `type` · `visit_id`(nullable) · `payload` jsonb — 「쌓기만」(origin/dev `backend/day/models/task.py` `EventLog`).

| 칸 | 값 |
|---|---|
| `type` | 삭제 · 되살림 두 값. 이름은 이 SPEC 의 기존 `event_log.type` 관례에 맞춰 정한다 |
| `actor_staff_id` | 동기화면 NULL · DAY 직원 동작이면 그 직원 |
| `visit_id` | 방문에 속한 행(구매 등)이면 그 방문 · 아니면 NULL |
| `payload` | 아래 키 |

`payload` 키:
- `entity_type`: `external_ref.entity_type` 과 같은 값
- `entity_id`: DAY id
- `source`: `kos` 또는 `day`
- `reason`: `kos_deleted` · `absent` · `refund_revoke` …
- 필요하면 KOS 쪽 시각(`lastUpdatedDateTimeUtc` 등)

## 쓸 곳

- SPEC-002 「upsert · 삭제」 절에 위 원칙과 표를 넣는다.
- `event_log.type` 새 값이 SPEC-000 05 `event_log` 설명에 목록으로 있으면 거기도 더한다.

## 범위와 열린 것

- 지금 있는 테이블(방문 · 작업 등)의 `mark_absent` 에도 로그를 붙일지는 이번 범위가 아니다. OQ 한 줄로 남긴다.
- 로그가 많아지는 경우(메뉴 대량 사라짐 등)를 한 줄로 묶을지도 OQ 로 둔다.

리포트 `spec-sync-report.md` 에 「삭제 규칙 반영」 한 줄을 남긴다.
