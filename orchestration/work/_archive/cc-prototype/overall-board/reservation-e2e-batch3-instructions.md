# E2E batch 3 수정 — 3건 (frontend 중심 · backend 는 #2 값)

기준 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-e2e-feedback.md` 「# batch 3」 표 #1 ~ #3. 금지 · 검증 · 보고는 앞 판 brief 그대로. 코드 기준 `09b1edc`. 보고 = `term_fa2737b7-e69a-40e1-9fac-019199b9dad3`.

| # | backend | frontend |
|---|---|---|
| 1 내원 현황 지난 단계 회색 | — | 지난 단계 점 · 카드 = 회색 · 지금 단계만 강조 |
| 2 단계 줄 시각 | 상세 `flow` 의 상담 · 시술 단계에 시각 값이 없으면 KOS 값으로 채움(상담 = `consultations[].consultationStartedDateTimeUtc` 가 예약 시각과 같으면 쓰지 말고 `flowStepUpdatedDateTimeUtc` · ccc 이벤트 시각 중 근거 있는 것) — 없으면 비움(지어내지 않음) | 한 줄 [제목][상세] …… [HH:MM] 에 시각 있으면 표시 |
| 3 부상태 색 규칙 | — | 대기 = 연한 배경(100) + 주 상태 색 글자 · 점 ○ / 진행 = 주 상태 색 채움 + 흰 글자 · 점 ● / 완료 = 회색. 스케줄 표 카드 부상태 칩 · 내원 현황 단계 · 원내 현황 Badge 전부 한 규칙(공용 함수 하나로). 시술 현황판 코드는 건드리지 않음 |

검증 backend ruff · pytest / frontend tsc · lint · 스크린샷 `fe-shots-reservation/e2e-b3-*.png`(카드 칩 3종 · 내원 현황). 커밋 금지.
