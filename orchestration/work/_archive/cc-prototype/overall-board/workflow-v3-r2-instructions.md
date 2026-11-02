# [planner] r2 — workflow-v3 에 사용자 답 반영 + workflow-v2 를 지금 결정에 맞춤

앞 판(`reservation-workflow-brief.md` · 네 보고 `reservation-workflow-v3-report.md`)에 이어진다. 역할 · 금지 · 완료 보고 방식은 그 브리프 §5 · §7 과 같다. **보고 대상 = 예약 코디 `term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**(preamble 과 다르면 preamble).

## 1. workflow-v3.md 고치기

`/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/_RESUME.md` §2 의 **2026-10-26 새 줄 4개**를 반영한다(원문은 거기서 읽어라):
- 「v3 「정할 것」 사용자 답」 줄 — 시간축 · 카드 이름(KOS 이름 그대로 + 한글 발음 · 잘라 읽지 않음) · 총 예약 수 · 공지(그 날짜 · 날짜 이동과 같이) · 신분증 이미지 KOS 업로드 · 방 목록 KOS 그대로 · 건강 확인 필요 기준 · 여정 리포트 뺌 · 처방전 KOS 출력(딥링크 `tab=etceteraWork` — `_RESUME` 「[처방전 출력]」 줄 · 리포트 `reservation-prescription-report.md` · `reservation-prescription-detail-report.md` · KOS 반영 표에 한 행 · 머리말 리포트 목록에 둘 더) · [귀가 완료] 수납 필요면 못 함 · 코디 권한 제한 없음(직무별 제한은 마지막) · 이름 같은 고객 경고(코디 기본값)
- 「상담사 「지금 상태」 · 스케줄 표 시간축」 줄 — 새 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-timeaxis-report.md` 를 읽고 1절(스케줄 표) · KOS 반영 표(그룹 조회) · 머리말 리포트 목록(13번째)에 넣는다
- 「후납」 · 「후납 수납 확인」 쪽은 앞 판에 이미 들어갔는지 확인만

그리고:
- 위 결정으로 닫힌 줄은 「정할 것」에서 뺀다(새 문서라 취소선 없이). 남는 줄의 근거 Q 번호 유지
- 사용자 지시 / 코디 기본값 구분을 지킨다

## 2. workflow-v2.md 를 지금 결정에 맞추기

`/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-12-cc-prototype/workflow-v2.md` — 시술 현황 되돌리기 작업이 끝났다(사용자 2026-10-26). 네가 앞 판 보고에 적은 **v2 와 어긋난 곳 7개**를 고친다:
- 원천: `_RESUME` §2 의 2026-10-23 · 10-25 · 10-26 시술 현황 줄(작업 type 규칙 하나 · 「방 배정」 숨김 · 카드 방 판정 · KOS 반영 실패 = 토스트 · 되돌리기 추가 등) · `para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md`(지금 판) · `spec-004-procedure-app.md`
- v2 의 규칙대로 **뒤집힌 줄은 지우지 않고 ~~취소선~~ + 「(2026-10-2X 바뀜)」 + 바로 아래 지금 것**
- 머리말 갱신 날짜 · 「뒤 구간 = v2 / 앞 구간 = v3」 상호 링크 한 줄
- D-10 범위(시술 구간만 · 예약 구간은 v3)를 v2 원칙에 한 줄
- 「코디 · 상담사 역할」은 v2 계정 절에 「예약 구간 = v3 · 코디 역할 추가 · 직무별 제한은 마지막」으로 참조만
- 그 밖에 v2 를 다시 쓰지 마라 — 7곳 + 링크만

## 3. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-26-cc-reservation/workflow-v3.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-12-cc-prototype/workflow-v2.md`
- 보고서는 이번엔 **`/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-workflow-v3-r2-report.md`** 에(scratchpad 말고)

## 4. 검증

- 새 결정 줄 4개 → v3 절 대조표(빠진 항목 0) · v2 7곳 → 고친 줄 대조표
- 실명 · id grep 0(v2 · v3 둘 다)
