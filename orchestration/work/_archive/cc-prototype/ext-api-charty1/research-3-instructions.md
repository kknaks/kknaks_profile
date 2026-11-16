# researcher 3차 — 새 HAR 2개: 예약 이력 · 병원 정보

원 브리프(`ext-api-charty1-research-brief.md`) 제약 그대로: 데모만 · 조회만(쓰기 0) · 내부 실호출 안 함 · public 이라 값 원문 금지(경로 · 칸 이름 · 모양 · 건수만) · 리포트 1개만.

## 새 HAR (사용자가 KOS 웹에서 캡처)

- `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-11-16-cc-charty1/har/예약이력.har` — 예약 이력 탭
- `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-11-16-cc-charty1/har/병원정보.har` — 병원 정보(설정) 화면

## 알아낼 것

1. **2-3 처음 상담 대기 시각** — `예약이력.har` 에서 단계 변경 이력을 주는 호출(경로 · 메서드 · 요청 본문 키 · 응답 키 트리). 이력 원소에 단계 · 시각 · 행위자가 있나. 같은 단계를 여러 번 거친 기록이 각각 남나. 「처음 `CONSULTATION_WAITING` 이 된 시각」을 이 응답으로 뽑을 수 있나. 일정 1건당 호출인가, 여러 건을 한 번에 받나(board 에 넣을 때 KOS 호출 수). 공개 스펙에 같은 것이 있나(1차 결론: 없음 — 다시 대조)
2. **병원 정보** — `병원정보.har` 에서 내부 `get-hospital`(또는 실제로 불린 것)의 응답 키 트리 전체. 2차 리포트의 JS 추정 칸(이름 · 전화 · 주소 · 대표자 · 사업자 번호 · 요양기관 번호 · 국적 · 언어 · `addressContract`)과 대조. 운영 시간(`get-default-operation-timetable` 등)이 같이 불렸으면 그 모양도

## 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/research-har-history-hospital.md`
- 맨 위 요약: 질문 1 · 2 한 줄 답 + 분류(A~E) + KOS 호출 수
- 정할 것(결정하지 않고 모음)

완료 보고는 원 브리프 §9 의 두 채널 그대로.
