# backend 2차 — 코드 검수 r1 WARN 수정

원 브리프(`ext-api-charty1-be-brief.md`) 제약 그대로(커밋 · push 금지 · KOS 호출 0 · 사용자 포트 금지 · public). 리포트 `review-code-r1.md`(같은 폴더) — W · Q 번호는 그 리포트 번호. 아래는 코디 답(코디 기본값). planner 가 SPEC-008 0.4.4 에 같은 내용 한 줄씩을 병렬로 넣는다 — 기다리지 말고 코드부터.

| # | 할 것 |
|---|---|
| W1 = Q1 | **고친다.** ⓐ 시도 예약 때 그 줄이 이미 `home` 이면 `final_tried = 1` 도 같이 세운다(ⓐ 가 ⓒ 몫을 겸함). 시험: 처음 봄 = 귀가 → board 여러 번 → 이력 1번 · 겹친 두 요청 → 1번 |
| W2 = Q2 | 코드 그대로(404 · 400+NotFound 둘 다 `customer_not_found`). 시험에 `get-visitor` = HTTP 404 갈래 1개 더함 |
| W3 | ⓐ · ⓑ · ⓒ · ⓓ 섞인 12줄 이상으로 첫 board 의 10개 집합 · **차례**(list 로) · 남은 줄 단언 시험 1개 |
| W4 | 상세 · 오더 메모 경로 caplog 단언(헤더 직원 id · 예약 id · 고객 값이 로그에 0) 각 1 |
| W5 | **이번에 고친다.** board 가 `event_log` `reception` · `consultation_add` 를 **그날 예약 id 로 거른 쿼리**로 읽게(고객 사본도 그날 줄의 고객만). repo 함수를 더하되 직원 쪽 기존 함수 · 동작은 그대로. 결과 동일 시험(T55 그대로 통과) |
| Q3 | 코드 그대로(사본 없으면 `customerId` null) |
| 참고 | 섞임 판정의 명시 `null` = 없음 — 지금 그대로 두고 T49 에 그 줄 1개 단언만 더함 |

검증: `uv run pytest -q tests/test_ext_board.py tests/test_ext_lookup2.py tests/test_ext_detail.py tests/test_ext_write.py tests/test_resv_detail.py tests/test_resv_board.py` → 끝에 전체 `uv run pytest -q` 1번 · ruff. 보고 = 원 브리프 §9 두 채널(고친 곳 파일:줄 · 수치).
