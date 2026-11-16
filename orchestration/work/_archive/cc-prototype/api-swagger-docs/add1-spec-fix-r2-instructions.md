# [planner] add1 r2 — 문서 검수 WARN 6 반영 → SPEC-008 0.3.1 · DEC-011 · WORK-013

원 브리프 제약 그대로. 근거 `review-doc-add1.md` §2 · §8. 리포트 「고칠 방향」 문구대로:
- **W1** §6.7 · §6.8 2단계: `data` 키 없음(`{}`) · `data: []` = 일정 없음 → `[]` / `data` 가 있으면서 배열 아님 = 502. T39 에 `{}` → 200 빈 목록 줄
- **W2 · Q-add1-A 답(코디 기본값)**: `deleted: true` 일정은 과거 시술 · 예약 내역 **둘 다에서 뺀다**(사본 쓰기 `apply_schedule` 과 같은 규칙). DEC-011 에 D 번호 하나 더(코디 기본값) · §6.7 · §6.8 3단계 · 시험 줄
- **W3** §8 시험 고침: parameters 단언 = `X-Api-Key`(header) + `GET /api/ext/availability` 의 `date`(query) 하나만 · 그 밖 query · path 0
- **W4** §8: 「세 경로 합산」「세 엔드포인트 합산」 문구 → 「외부 경로 전부 합산」 · T29 에 429 줄 단언
- **W5** (가): `date` 없음 = message `query.date: …`(지금 규칙) · 꼴 · 범위 = `date: …` · 받는 타입 `str`(pydantic date 금지) · 빈 문자열 400
- **W6** T36 · T39 · T44 에 리포트 줄 그대로 더함
- I2 는 WORK-013 주의에 「refresh_slots 를 날짜 잠금 안에서」 권장 한 줄

SPEC `0.3.1` · 변경 이력 · README 행. 완료 보고는 원 브리프 §9 두 채널.
