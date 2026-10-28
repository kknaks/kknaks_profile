# E2E batch 2 수정 — 사용자 지적 8건 (backend · frontend)

기준 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-e2e-feedback.md` 의 **「# batch 2」 표**(#1 · #2 · #4 ~ #9 — #3 공지 [수정하기]는 HAR 기다려 보류 · 이번엔 하지 않음). 처분 칸이 할 일. 앞 판 brief(`reservation-e2e-batch1-brief.md`)의 금지 · 검증 · 보고 그대로. 코드 기준 커밋 `1d482d8`. 보고 대상 = 예약 코디 `term_fa2737b7-e69a-40e1-9fac-019199b9dad3`.

| # | backend | frontend |
|---|---|---|
| 1 날짜 이동 느림 | — (board API 0.2초 · 코디 측정) | 원인 찾기 · 날짜 바뀌면 **즉시** 요청 · 응답 오기 전엔 이전 표를 흐리게 유지(빈 「불러오는 중」 대신) · 원인을 보고에 |
| 2 상세 404 반복 | 상세에서 KOS 일정 404 → 도메인 예외 → 404 `reservation_gone`(또는 SPEC 맞는 코드) · 로그 WARNING 폭주 막기 | 404 면 상세 폴링 멈춤 · 「KOS 에서 사라진 예약이에요」 + 닫기 |
| 4 상담사 팝오버 | — | 고르면 닫힘 → [실장 호출] 흐름 · 팝오버 portal(모달 위 레이어) · 아래 공간 모자라면 위로 |
| 5 상담사 목록 | 상담사 목록(form · 상세 `counselors`)에서 시스템 계정 · 마취용 제외 — 시술 현황과 같은 규칙(`KOS_EXCLUDE_ACCOUNT_IDS` · 이름 「마취용」 판정이 있는 곳 재사용) | — |
| 6 시술실 팝오버 | (정렬에 필요한 값 있으면) | 시안 `M:1826-1832` 코드 읽고 **똑같이**(사용 중 위 · 회색 · 빈 방 아래 · 머리 문구 · 열 수) · 보고에 시안 대조 줄 |
| 7 이전 방문 | — | 기본 = 전부 펼침 |
| 8 영문 값 | — | 이전 방문 Badge · 시술 내역 줄의 KOS 영문 상태를 한글 표시(값 판정은 그대로) |
| 9 내원 현황 카드 | — | 한 줄: [제목] [상세] …… [HH:MM 오른쪽] · 상담 · 시술 · 귀가 카드도 같은 꼴 |

검증: backend `ruff` · `pytest` / frontend `tsc` · `lint` · 화면 확인 스크린샷(#6 · #9 · #1) → `orchestration/work/overall-board/fe-shots-reservation/e2e-b2-*.png`. 커밋 금지.
