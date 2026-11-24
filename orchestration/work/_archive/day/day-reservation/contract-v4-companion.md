# 계약 v4 — 동행 그룹 · 카드 배치(E6 · E7) · 결정 R64 ~ R69

## 보기 모델 (기존 V 바꿈 · 더함)
- `cards[]` 에 `lane: int`(0 ~ 4 · 줄 안 자리) · `line: int`(0 ~ · 그 시간칸 안 몇째 줄) · `companion_group_id: str|null` 추가. 기존 `stack_index` 는 없앰(→ lane · line).
- `rows: [{start_min, end_min, lines}]` — 시간 행(전 열 공통 단위 · backend 가 정해 worker_done 에 적음). `lines` = 그 행에서 가장 많은 줄 수(최소 1). 화면은 행마다 높이 = lines × 카드 줄 높이로 쌓아 카드 top 을 계산.
- `bands: [{group_id, column_id, start_min, line, lane_from, lane_to}]` — 띠 하나 = 한 줄 안 이어진 자리 구간(그룹이 줄을 넘으면 줄마다 하나).
- `companion_editable: bool`(오늘 · 앞날 ∧ 권한).
- 카드 폭 140px(CSS 토큰).

## 쓰기
- `PUT /reservations/companions` form `visit_id`(끈 카드) · `target_visit_id`(놓은 카드) → 묶기 / 옮기기
- `PUT /reservations/companions/leave` form `visit_id` → 풀기
- 200 = `#reservation-main` 조각(폴링과 같은 것) · 400 형식 · 403 권한 · 409 `companion_condition`(다른 열 · 다른 칸 · 닫힌 카드) · 409 `companion_past_date`. 오류 꼴은 기존 화면 규약(X-Day-Error).
