# [frontend · 1판 고침 1] book_view 키워드

같은 터미널 · 같은 규칙. `routers/reservation_detail.py:177` `book_view(group_id=…)` → `group_text=…`(backend 가 바꿈 · `contract-v1.md` §5 · 구조 검사 `identifiers.py` 가 `*_id: str` 인자 금지). 그 밖에 contract §5 의 이름 바뀜이 화면에 걸리는 곳 전부 맞춰라. 검증 = `backend/scripts/check.sh` 의 mypy strict · 네 화면 테스트 · `npm run check` 각 1회. 완료 보고 두 명령(subject 「frontend 완료: 1판 고침 1」 · 이번 dispatch 값).
