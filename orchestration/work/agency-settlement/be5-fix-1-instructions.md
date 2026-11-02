# backend code r4 수정 — F-1 · W-1 ~ W-3 (코디 결정)

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r4-report.md`.
**코디 결정(F-1)**: (1) **잠긴 달 품목은 다시 잇지 않는다**(달 잠금 = 키도 얼림) · (2) 풀린 달에서 키가 바뀐 줄은 **옛 키 비율을 새 키로 옮긴다**(새 키에 이미 값이 있으면 그대로 두고 충돌 수만 셈) · `fee_rate_changes` 에 기록 · (3) 상품 받기 응답에 `rekeyedItems` · `carriedRates` · `conflicts` 수 · 설정 화면용 같은 수.
- W-1 · W-2 · W-3 리포트대로(잠긴 달 `purchase_options` 안 바꿈 · PUT 은 설정 줄에 있는 키만 · 풀 기다림 짧게 + 503/429 로 바로 알림)
- 시험: 리포트 F-1 시험 둘 + 옮기기 · 충돌
- 운영 PG(5434) · 8800 · back/.env 건드리지 마라 · ruff · pytest · WP-BE4 브리프 §9 두 채널(같은 task/dispatch) · subject 「backend code r4 수정 완료」
