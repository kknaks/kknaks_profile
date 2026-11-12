# [backend] add1 고침 2 — 코드 검수 r1(`add1-review-r1.md`) 반영

- **W1**: `app/api/ext.py` `AVAIL_INVALID` 400 줄을 SPEC §6.6 표대로 — 「`date` 없음(message `query.date: …`) · 빈 문자열 · `YYYY-MM-DD` 꼴 아님 · 오늘(KST) 앞 · 오늘 + 90일 뒤(message `date: <이유>`)」. T29 단언에 `query.date:` 하나 더
- **N1(코디 결정)**: 외부 두 경로(과거 시술 · 예약 내역)에서 일정 **원소** 모양이 깨져 처리 중 예외가 나면 `502 kos_unavailable`(KOS 응답 모양 깨짐 = 1차 W1 과 같은 분류). 직원 「이전 방문」 동작은 바꾸지 않는다(감싸는 곳은 외부 서비스 쪽). 시험: `reservation` 문자열 · `reservationTime` 문자열 · 작업 `title` 숫자 → 502 · 본문에 원문 0
- **N2**: 경계 시험 두 줄 — 시계 = 일정 시작 정각 → 과거 시술에 없음 · 예약 내역에 있음 / 오늘 00:00(KST) 일정 → 예약 내역에 있음. 일정 읽기 4xx · 401 → 502 한 줄
- N3 은 SPEC 몫(planner) — 코드 그대로

부분 검증 → 끝에 `uv run pytest -q` · `uv run ruff check .` 1회. 리포트 `add1-be-report.md` 에 「고침 2」 절. 완료 보고는 원 브리프 §7 두 채널(이번 dispatch 의 taskId · dispatchId).
