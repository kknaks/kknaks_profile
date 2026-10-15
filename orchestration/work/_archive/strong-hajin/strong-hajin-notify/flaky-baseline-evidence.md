# 기존 실패 판정 — 날짜에 묶인 프론트 시험 8개 (2026-10-08 코디)

전체 테스트 1회(`verify-1-fe.log`)에서 `frontend-test` 8 failed / 1572 passed.

| 파일 | 시험 수 | 원인 |
|---|---|---|
| `features/work/TaskDetailDates.test.tsx` | 3 | 고정 픽스처 마감일 `2026-10-06` 이 **오늘(10-08) 기준 지남** → 화면이 「마감일 초과」 를 붙여 기대 문자열과 다르다 |
| `features/work/CreateWork.test.tsx` | 4 | `pickDate` 가 달력 `group` 안의 고정 날짜 칸을 누르는데 **이번 달 보기에 그 칸이 없다** → `Unable to fire a "click" event` |
| `features/work/CreateWorkLayout.test.tsx` | 1 | 같은 `pickDate` 계열 |

- 이번 작업의 `features/work/` 변경은 `MyWorkPage.tsx` +4줄(현재 보기 알림 — WP4)뿐 · 실패 컴포넌트(업무 생성 · 업무 상세 날짜) 무변경
- 판정: **기존 실패(날짜 폭탄)** — 알림 작업과 무관. E2E 를 막지 않는다
- 처분: 별도로 고친다(시험이 「오늘」 을 고정하거나 상대 날짜를 쓰게) — 이번 PR 범위 밖 · 회고 §7 후보
