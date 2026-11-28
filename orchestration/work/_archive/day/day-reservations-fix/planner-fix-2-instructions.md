# [planner · 고침 2] OQ-R41 — 5장 규칙 유지 + 1시간 행(오픈 시간 기준)

같은 터미널이면 앞 맥락 그대로. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec`(미커밋 변경 그대로 이어서 · **커밋 · push 하지 마라**).

## 정해진 것(사용자 11-27 · 다시 열지 마라)
- 고침 1 에 넣은 「겹침 상한 없음 · 열 폭 늘림」은 **뒤집혔다**. **5장 규칙(R64) 유지** — 사용자 「5장 넘어가면 좌우 스크롤이 너무 많아져서 내려가야 해」
- **행 단위 = 병원 오픈 시간 기준 1시간씩**(KOS 처럼) — 사용자 「시간 단위는 오픈 시간 기준으로 한 시간씩 · 코스처럼」
- 길이 비례는 그대로: 카드 높이 = 예약 길이에 비례(60분 = 1시간 행 하나 높이 · 30분 = 반 · 15분 = 1/4) · 겹치면 옆 자리(12:00~13:00 첫 자리 · 12:30~13:30 옆 자리 12:30 위치부터)
- 한 행에서 동시 겹침이 5장을 넘으면 6번째부터 **아래로 줄 접기** · 그 행이 그만큼 높아짐
- 앱 예약현황 표도 같은 규칙(OQ-R44 닫힘 그대로)

## 할 것
1. 고침 1 의 R41 「상한 없음」 본문 · 열 폭 규칙 · `lines` 늘 1 을 **되돌리고** 위 규칙으로 다시 쓴다(spec-006 · spec-003 앱 표 · 서버 배치 값 · 20-spec · 10-decision · log). R64 · 열 폭 상한 5 복구.
2. 서버 배치 값(줄 · 자리 · 행)이 웹 · 앱 둘 다 같은 값으로 그려지게 한 번만 정의.
3. **경계 경우는 지어 메우지 말고 OQ 로**(각각 추천 기본값 한 줄): 예) 행 경계를 넘는 카드(12:30~13:30)가 줄 접기로 높아진 행을 지날 때 높이 · 위치 · 오픈 전 / 마감 뒤 예약 · 오픈 시간이 정각이 아닐 때.
4. `python3 scripts/lint-pipeline.py --strict` products/day ERROR 0.

## 금지
다른 결정 다시 열기 · 화면 문구 짓기 · 공개(open) KOS 호출 · 커밋 · push · WORK · Delivery.

## 보고
`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/planner-fix-2-report.md` — 되돌린 줄 · 새 규칙 · 남긴 OQ(추천 기본값) · lint. 완료 보고 두 명령(subject 「planner 완료: 고침 2」 · 이번 dispatch 값 · 코디 `term_99b025fc-f3ef-403e-8162-509c41545e2e` — preamble 이 다르면 preamble).
