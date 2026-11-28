# [planner · 고침 3] 2차 검수 WARN 9 반영 — 배치 정의 한 곳으로

같은 터미널이면 앞 맥락 그대로. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec`(미커밋 이어서 · **커밋 · push 하지 마라**).

## 읽을 것
- 검수: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-doc-2-report.md`(W2-1 ~ W2-9 · 「OQ-R45 ~ R48 넣을 문장」)
- 결정 표 맨 위 행(R45 ~ R48 코디 기본값): `.../day-reservations-fix/_RESUME.md` §2

## 할 것
1. **W2-1 ~ W2-9 를 검수 「고칠 방향」대로**. 옛 「30분 = 1칸 · 60분 = 2칸 · 15분 = 반 칸 · 축 시작부터 분 비례 · 08:00 ~ 24:00 30분 한 줄 70」 문장은 전부 취소선 + 「→ 보충 2 · Rule 15」. **살아 있는 배치 정의 = Rule 15 ⓐ ~ ⓙ 하나만**(웹 · 앱).
2. W2-6: ⓑ 놓는 순서 = 시작 시각 → 같은 시작이면 R73 순서.
3. W2-7 · W2-8: 검수의 ⓖ ~ ⓙ 제안 문장을 그대로 Rule 15 에 넣는다(R45 = 지나는 아래 줄 띠도 덮고 그 자리는 찬 자리로 셈). OQ-R45 ~ R48 표 행 = 취소선 · 「닫음(2026-11-27 코디 기본값)」 · 케이스 칸도 규칙 문장으로.
4. W2-4 귀결(오픈 전 예약이 없는 날 오픈 전 회색 면 안 보임)은 R47 대로 받아들인다 — 본문 한 줄로 밝혀 둔다.
5. 참고의 `open_min = 0`(그룹 `start_time` 없음) = WORK 볼 것으로 log 에 한 줄(SPEC 규칙은 안 바꿈).
6. `python3 scripts/lint-pipeline.py --strict` products/day ERROR 0 · products/day 에서 `60분 = 2칸` · `30분 시간 칸` 이 취소선 밖에 남지 않았는지 grep 결과를 보고에.

## 금지
다른 결정 다시 열기 · 화면 문구 짓기 · 공개(open) KOS 호출 · 커밋 · push · WORK · Delivery.

## 보고
`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/planner-fix-3-report.md` — W 별 고친 줄 · grep · lint. 완료 보고 두 명령(subject 「planner 완료: 고침 3」 · 이번 dispatch 값 · 코디 `term_99b025fc-f3ef-403e-8162-509c41545e2e` — preamble 이 다르면 preamble).
