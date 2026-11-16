# 화면 피드백 F16 — KOS 쓰기 바로 보내기 (백엔드)

## #231 영향
없음 — 라우트 · 조각 · 값 그대로다. 버튼은 지금처럼 KOS 를 기다리지 않는다.

## 고친 것
- `day/services/outbox_kick.py`(새): `send_now(hospital_id)`.
  - 이름으로 발행한다. 태스크 `day.emr.send_outbox_hospital` 을 `taskiq.kicker.AsyncKicker` 로 `.kiq(병원 id)` 한다.
  - api 는 `day.tasks` 를 import 하지 않는다(경계 테스트 그대로).
  - 태스크 이름은 외부 계약이라 `day/tasks/emr.py` 가 이 상수를 그대로 쓴다.
  - 발행 실패는 로그 한 줄(`outbox kick failed` + 예외 이름)만 남기고 삼킨다.
- `services/board._finish`: commit → 판 신호 → **이번 조작이 KOS op 을 1개 이상 넣었으면 `send_now`**. op 이 없는 조작(마취 · 순서 · 닫힌 연결)은 발행하지 않는다.
- worker 쪽은 그대로다.
  - 병원별 잠금 · 억제(`emr_sync.run_outbox`)가 있어, 겹친 발행은 잠금이 건너뛴다.
  - 10초 주기(`day.emr.send_outbox`)는 재전송 · 놓친 것 메우기로 남는다.
  - 앞 회차가 잠금을 쥐고 있을 때 바로 발행이 건너뛰어지면, 그 op 은 다음 10초 회차에 나간다.

## 테스트
- DB 없이(`tests/day/board/test_outbox_kick.py` · 가짜 broker = `InMemoryBroker` 의 `kick` 만 바꿈):
  - 쓰기를 넣은 조작 → commit 1 · 발행 1번(`day.emr.send_outbox_hospital`).
  - 쓰기 없는 조작 → 발행 0.
  - broker 가 실패해도 `_finish` 는 결과를 그대로 돌려준다(응답 성공) · `send_now` → False.
- infra(`test_board_api.py`): 마취(쓰기 없음) → 발행 0 · 호출 → 그 병원 1번 · 200.
- board infra 테스트는 실제 스트림(`day:tasks`)에 넣지 않게 기록용으로 바꿨다(`conftest.kicked` autouse).
  - 처음엔 실제로 넣었다. 그러자 같은 테스트 Redis 를 읽는 `tests/runtime/test_tasks.py` 가 그 메시지를 먼저 받아 깨졌다. 그래서 바꿨다.

## 검증
| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | 299 passed |
| `scripts/test.sh -q` | 454 passed |
| ruff check · format --check | 통과 |
| compose | down 안 함 · `--profile app up -d --build --wait api worker scheduler` · `/health/ready` ok |

## 실물(데모 카드 · 사용자가 화면에서 [의사 호출] 한 번 · 상태 · 시각만 · UTC)
| 시각 | 일 |
|---|---|
| 07:56:49.820 | 조작 commit — op 3개 적재(방 · 담당자 · 호출) |
| 07:56:49.921 | worker 가 바로 보내기 태스크 `day.emr.send_outbox_hospital` 실행 시작(**+0.10초**) |
| 07:56:50.263 | 3개 모두 KOS 로 보냄 `{'sent': 3}`(**+0.44초**) |
| 07:56:55.147 | 다음 일정 조회(10초 주기)가 3개 모두 **confirmed**(+5.3초) |

- 전에는 10초 주기를 기다려 보냈다(최대 10초 + 조회). 이제 보내기는 1초 안쪽이다.
  - KOS 화면에 뜨는 시각은 KOS 쪽 반영 시각이다(보낸 직후).
  - DAY 의 confirmed 는 다음 조회 때다 — 「반영 중」 표시가 풀리는 시각.
- 같은 회차 뒤 10초 주기 발송은 `done {}`(보낼 것 없음)였다 — 겹쳐 두 번 나가지 않았다. api 로그 `outbox kick failed` 0.

## 남은 것
- 없음(이번 범위). 「반영 중」을 더 빨리 풀려면 보낸 직후 일정 조회를 한 번 당기는 방법이 있다(새 결정 · 이번엔 안 함).
