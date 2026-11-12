# [backend] add1 고침 1 — 문서 검수(review-doc-add1.md) 결과. SPEC 은 planner 가 0.3.1 로 맞추는 중 — 아래가 먼저다

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/review-doc-add1.md` §2 의 「구현자가 다르게 할 것」을 전부 따른다. 요지:
- W1: 일정 응답 `resp.get("data", [])` — 키 없음 · `[]` = 빈 목록(200) · 있으면서 배열 아님 = 502. `_data_list` 그대로 쓰지 말 것. 시험 `{}` → 200 빈 목록
- W2(코디 결정): `deleted: true` 일정은 과거 시술 · 예약 내역 둘 다에서 **뺀다**. 고르기 함수 한 곳에서
- W3: `test_ext_docs.py` parameters 단언을 지우지 말고 `availability` 의 `date`(query)만 허용 — `name`/`email` 이 query 에 생기면 실패해야 함
- W4: `git grep -n "셋\|세 경로\|세 엔드포인트" app/` 전부 → 「외부 경로 전부 합산」 · 429 줄 단언
- W5: `date: str = Query(...)`(pydantic date 금지) · 빈 문자열 먼저 400 · 꼴 10글자 + fromisoformat · 범위 오늘~90일. `date` 없음은 지금 검증 규칙 그대로(`query.date: …`)
- W6: runtime 없음 → 502 · KOS 호출 0 / 이름 검색 5xx → 502 · 일정 읽기 0 / `POST /api/ext/availability` → 405 — 경로마다 시험 1줄 · 새 셋 모두 `responses=errors(*COMMON, …)`
- I2(권장): `refresh_slots` 를 날짜 잠금(`ensure` 의 `_locks`) 안에서
리포트 `add1-be-report.md` 에 「고침 1」 절로 대조.
