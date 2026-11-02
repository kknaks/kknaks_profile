# [researcher] 추가 지시 — 스케줄 표 시간축 = 예약 그룹 설정

앞 판들에 이어진다. 보고 · 질문은 예약 코디 **`term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**. 데모 assert · 운영 키 금지. **KOS 쓰기 0건**(HAR 해석 + 조회).

## 1. 무엇을 하나

사용자 결정(2026-10-26): 스케줄 표 시간축 = **기본 30분 + 예약 그룹에 있는 시간**(그룹별 운영 시간 · 간격 · 정원). 지금 KOS 화면의 시간축이 시술 쪽 설정 때문에 달라 보인다고 사용자가 본다. 사용자가 KOS 예약 그룹 설정 화면을 HAR 로 떴다.

## 2. 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/예약그룹.har` (214항목 · 코디가 본 KOS POST: `get-zones` · `get-roles` · `get-codes` · `get-accounts-status` · `issue-schedule-socket-token` · **`schedule/group/v1/queries/get-reservation-groups`** 등 — 전부 세어라)
- 앞 판: `reservation-read-report.md` §3.1 4행 · §3.3 · §5.2(#3 기본 운영 시간) · Q-5 / `reservation-create-report.md` §4(슬롯 · 정원 `intervalCapacities` · `get-reservation-time-slots` · `get-default-operation-timetable` · `get-reservation-rule`)

## 3. 할 일

1. `get-reservation-groups` 응답에서 그룹마다 시간 관련 필드 전부: 운영 시간표(`operationTimetable` — 요일별 시작 · 끝?) · 간격(`intervalMinutes`) · 정원(`intervalCapacities`) · 휴무 · 정렬(`order`) · 구역. 데모 13개 그룹의 값 모양(시각 · 분은 적어도 된다 — 개인정보 아님)
2. 병원 기본 운영 시간(`get-default-operation-timetable`)과 그룹 운영 시간의 관계 — 그룹이 비면 기본값을 쓰나
3. 「시간축이 시술 때문에 다르다」 — 시술 그룹(리프팅 60분 등)과 권역 그룹(30분)의 간격 · 시간 차이를 표로. KOS 「예약 현황」 화면이 칸마다 다른 간격을 어떻게 그리는지(JS 근거가 있으면)
4. 스케줄 표 그리는 규칙 후보(결정 말고 KOS 값으로 가능한 것): 전체 세로축 = 그룹 운영 시간의 합집합 · 줄 = 30분 · 그룹 칸마다 운영 밖은 회색 · 간격 60분 그룹의 칸 모양
5. 「정할 것」 Q-123 부터

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-timeaxis-report.md`

id · 토큰 · 이름 금지.
