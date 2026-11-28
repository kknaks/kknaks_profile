# [planner · 고침 1] SPEC 개정 검수 1차 WARN 8 + OQ 닫기 반영

같은 터미널이면 앞 맥락 그대로. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec`(미커밋 변경 그대로 이어서 · **커밋 · push 하지 마라**).

## 읽을 것
- 검수: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-doc-1-report.md`(WARN W1 ~ W8 · 참고 · OQ 분류 표)
- 결정 표 새 행(맨 위 3행 · 11-27): `.../day-reservations-fix/_RESUME.md` §2

## 할 것
1. **W1 ~ W7 고치기**(검수 「고칠 방향」대로). W8(log PR 칸)은 그대로 둔다 — 코디가 PR 때.
   - W2 = 문진 읽기는 **일정 회차 뒤 별도 태스크**(구매 회차 꼴 · 입력 = 같은 일정 응답의 고객)로 확정 · spec-007 · spec-002 같은 말로
   - W4 = 앱 JSON `questionnaire.expired`(이름 제안)
2. **OQ 닫기(결정 표 반영 · OQ 에서 「닫힘」으로 옮기고 본문 규칙으로)**:
   - **OQ-R41** = 겹침 장수 상한 없음 · 열 폭 = 동시 겹침 최대 수만큼 · `lines` 늘 1 · R64 줄 접기 · 열 폭 상한 5 없앰
   - **OQ-R44** = **앱 예약현황 표도 이번에 같이 고침**(60분 = 2칸 · 겹치면 옆 자리 · 서버 같은 배치 값) → spec-003 「앱 화면 변경 없음」 메모를 바꿔 앱 표 규칙으로
   - **OQ-D47** = 앱 상세도 「6개월 경과」(앱 이번에 같이 고침)
   - R42 · R43 · D44(링크 다시 씀) · D45 · D46 ① ~ ④ · D49 = 결정 표 「검수 1차 OQ 코디 기본값」 행 그대로
   - **남길 OQ(사용자 글자)**: D43 진행 칸 · 복사 알림 글자 · D48 다른 날 낸 문진 글자 — 열린 채 두고 「그 전까지 지금 글자 · 알림 없음」
3. 참고의 「중복 가르기 빈틈」(고침 8 전 DAY 제출 행 external_ref 없음) = 「알고 감」으로 한 줄
4. `20-spec.md` · `log.md` 반영 · `python3 scripts/lint-pipeline.py --strict` products/day ERROR 0

## 금지
결정 다시 열기 · 화면 문구 짓기 · 공개(open) KOS 호출 새로 두기 · 커밋 · push · WORK · Delivery(다음 단계).

## 보고
`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/planner-fix-1-report.md` — W 별 고친 줄 · 닫은 OQ · 남은 OQ · lint 결과. 완료 보고 두 명령(subject 「planner 완료: 고침 1」 · 이번 dispatch 값 · 코디 `term_99b025fc-f3ef-403e-8162-509c41545e2e` — preamble 이 다르면 preamble).
