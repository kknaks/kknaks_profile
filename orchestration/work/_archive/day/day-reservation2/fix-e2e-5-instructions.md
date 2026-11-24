# [고침 · 화면 확인 5] B41 만 — 화면 렉

같은 터미널 · 같은 맥락. `e2e-1-feedback.md` 의 **B41 만**.
- api.log: 표 전체 `GET /reservations` 가 5 ~ 10초마다 · 한 순간 3 ~ 6번 겹침(12:00:11 · :16 · :21 · :31 · 12:00:35 ×3 · 12:10:40 ×6)
- **backend**: 오늘 동기화 · 다른 날짜 최신화 · 쓰기 확인이 SSE `reservation` 신호를 보내는 조건 = **예약 현황에 보이는 값이 실제로 바뀌었을 때만**(upsert 건수가 아니라 바뀐 행이 있을 때 · 같은 회차 안 신호는 한 번). 바뀐 게 없으면 신호 없음
- **frontend**: SSE `reservation` 신호 · write_confirmed 가 짧은 시간에 여러 번 와도 **표 다시 받기는 한 번으로 합침**(이미 받는 중이면 끝난 뒤 한 번만) · 모달 다시 받기도 같게
검증 = 관련 테스트 + `scripts/check.sh` 1회. 스택 손대지 마라. 완료 보고 두 명령(subject 「backend|frontend 완료: 고침 화면 확인 5」 · 이번 dispatch 값).
