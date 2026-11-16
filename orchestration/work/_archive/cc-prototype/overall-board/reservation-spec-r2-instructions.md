# [planner] r2 — SPEC-005 · WORK-007 · DEC-006 고치기 (review-doc r1 + 사용자 결정 U1~U7 + WP-KOS 결과)

앞 판 브리프 `reservation-spec-brief.md`(같은 폴더)의 역할 · 금지 · 완료 보고 §5 · §7 그대로. **보고 대상 = 예약 코디 `term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**(preamble 과 다르면 preamble).

## 원천

1. **review-doc r1** = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-review-doc-r1.md` — FAIL 3(F1 · F2 · F3) · WARN 9 전부 처분. 각 지적의 「고칠 것」을 따른다
2. **사용자 결정** = `_RESUME.md` §2 「SPEC-005 r1 사용자 결정(U1~U7)」 줄:
   - U1 두 구역 전부(정원 · 사용 중 · 원내 현황 범위도 구역별로 — F3 · E2E #2 기준 「KOS 화면과 같음」 유지)
   - U2 [접수 완료] 켜짐 = KOS 신분 칸이 다 채워짐(외국인 = 여권 영문명 · 생년월일 · 여권번호 / 내국인 = SPEC 이 정한 칸) — ccc 「확인 완료」는 표시만(켜짐 조건 아님). OQ-719 닫음
   - U3 카드 값만(OQ-703 닫음 · 지금 SPEC 그대로)
   - U4 부도 고객 접수 허용(OQ-716 닫음 — KOS `recept` 가 받는 것 리포트 확인됨)
   - U5 이어 하기(OQ-718 닫음 — F1 고친 규칙으로)
   - U6 헤더 「현황」 첫 화면 = 시술 현황 유지(W9 · 드롭다운에 예약 현황 추가만)
   - U7 **예약 카드에 「수납 필요」 표시 넣는다**(W5 — 원천 `tasks[].paymentRequired` · 시술 현황 규칙과 같게 · 모양은 시안 톤에 맞춰 SPEC 에 정한다)
3. **WP-KOS 결과** = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-kos-probe-report.md` — K1~K10 모두 받음 · 귀가 거절 400 · funnel 모양 확정 · 모양 다름(문진 제출본 최상위 객체 · 제출본 없음 = 400 + errorProperties · 방 없음 = `room:{id:""}` · change-tasks-room 약 1초 뒤 보임 · 시각 밀리초 없음). SPEC §4 · §8 「미확인」 줄을 「(2026-10-26 데모 확인)」으로 · OQ-728 · OQ-739 · OQ-753 ~ OQ-756 닫음 · WORK-007 게이트 = 통과로

## 할 일

- SPEC-005 0.1.0 → **0.2.0**(변경 머리말 · 바뀐 절 · 부록에 r1 처분표 · U1~U7 반영표 · WP-KOS 반영표)
- DEC-006 에 U1~U7 줄 더함(D-44 ~) · WORK-007 WP 대상 파일 · 완료 조건 · 게이트 상태 고침(F2 `service/actions.py` 포함)
- review r1 「작은 기본값 묶음」은 §10 OQ 하나로 목록화

## allowed_paths

- `para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md` · `10-decision/decision-006-reservation-board.md` · `30-work/work-007-reservation-board.md` · `log.md`
- 보고서 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-spec-r2-report.md`

## 검증

FAIL 3 · WARN 9 처분표(빠짐 0) · U1~U7 반영표 · WP-KOS 판정 → SPEC 줄 대조 · 실명 · id grep 0
