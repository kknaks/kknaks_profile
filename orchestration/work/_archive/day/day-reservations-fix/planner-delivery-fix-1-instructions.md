# [planner] Delivery 검수 WARN 9 반영 — Issue #300 · #301 · #302 본문 고치기

같은 터미널이면 앞 맥락 그대로. 검수: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-delivery-1-report.md`(D1 ~ D9 · 참고).

## 할 것
1. D1 ~ D9 를 검수 「고칠 방향」대로 세 Issue 에 반영. **세 Issue 공통 계약 ① ~ ⑤ 는 한 글자씩 같게**(한 번 쓰고 셋에 똑같이 붙임).
   - D3 = 코디 기본값: 「누르기 · 놓기 시각 = 30분 단위 그대로 · y ↔ 분은 행 높이를 따른 매핑」(지금 동작 유지 · SPEC 한 줄은 머지 뒤 v2 재결속 때)
   - D2 = R71 동행 판정(`can_join` · `valid_members`)은 30분 그대로 · 배치 행(60분)과 함수 · 상수 나눔
   - 참고(차트 「초진 설문」에 `source = read` 행 보임)는 #300 「동작 변화」 한 줄
2. Issue 본문 고치기는 `mediness start-delivery` 의 정해진 길(request v1 → 고친 request 로 plan/apply · 같은 key)이 있으면 그 길로, 없으면 `gh issue edit` 로 사람용 본문만 — 어느 길을 썼는지 보고에. 막히면 우회 말고 출력 그대로 보고.
3. **재검수 없음**(코디 결정 · 검수는 코드 끝에 한 번). 그래서 고친 뒤 스스로 검수의 grep · 대조를 다시 돌려 D1 ~ D9 각각 반영 줄을 보고에 남겨라.

## 금지
SPEC 본문 바꾸기 · 코드 수정 · 승인 receipt · PR 머지 · 공개 KOS 호출 · 화면 문구 짓기.

## 보고
`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/delivery-fix-1-report.md` — D 별 반영 자리 · 쓴 길 · 막힌 것. 완료 보고 두 명령(subject 「planner 완료: Delivery 고침 1」 · 코디 `term_99b025fc-f3ef-403e-8162-509c41545e2e` — preamble 이 다르면 preamble).
