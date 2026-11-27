# e2e 2 결과 보고 — 고침 3(e2e 1 발견 ② ③ ④) 실물

## 상태: done (스택 시작 · 멈춤 · 코드 수정 없음 · 웹 세션 하나 → 로그아웃)

스크립트 `/private/tmp/day-e2e-r3/run2.py` · `run2.out`(id 앞 8자 · 값 출력 없음). 시험 고객 = 이름 「E2E … (시험)」 · `example.com`.

| # | 시험 | O/X | 결과 |
|---|---|---|---|
| ② | 이메일만 초진 — KOS 에만 있는 같은 이름 + 이메일 고객(데모 확인 뒤 KOS 에 직접 만든 시험 고객 · DAY 사본 없음) | **O** | DAY 판정 `new` → [예약 생성] → W1(이름 + 이메일)이 KOS 고객을 찾음 → **409 `customer_ambiguous`** + 「고객 확인 필요」 댓글 · DAY 고객 0 · 쓰기 행 0 → **중복 고객 안 생김** |
| ③ | 상담사 지정해 생성 → 링키 E2 `change`(상담사 null) → [예약 수정] | **O** | 쓰기 = W4 `update-reservation` + W18 `update-reservation {counselor: {}}` 둘 다 confirmed(2.1s) · DAY 사본 `requested_counselor_id` = 없음 · **KOS 다시 읽기 `reservation.counselor.id` = 없음** |
| ④ | 생성 → 예약 현황에서 먼저 [예약 취소](W5 확인) → 링키 E2 `cancel` | **O** | E2 = **202 `status: canceled`** · 스레드 취소됨 · `reservation_applied` = create(누른 직원 있음) · cancel(누른 직원 없음) · E5 `canceled` |
| 정리 | ③ · ④ 예약 취소 확인 · ② 예약 없음 · 로그아웃 | O | KOS 에만 만든 시험 고객 1명 · e2e 시험 고객들은 남김(지우는 API 안 씀) |

버그 없음.
