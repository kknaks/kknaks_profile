# day-kos-call-notify be-fix-2 결과 보고 (재검수 r2 N1 · I-a)

## 상태: done (커밋 · push 없음)

경로는 `backend/` 기준.

| 지적 | 고친 파일:줄 | 시험 | 변이(되돌림 확인) |
|---|---|---|---|
| **N1** 메아리 시각이 오래 뒤 빈 값을 거쳐 같은 값으로 와도 0건 — 고정 시험 | 코드 변경 없음. 시험 도구 `tests/day/notifications/kos_call_support.py:84` `detail_round(..., at=)`(그 회차의 관측 시각) | `tests/day/notifications/test_kos_calls_flow.py:231` — DAY 호출 → op `confirmed` · `updated_at = E+2초` → `detail_round(E)` 0건 → 관측 시각 10분 뒤 빈 값 0건 → 다시 E 0건 · 호출 = DAY 호출 1개 · 푸시 1 | 창 비교를 관측 시각 `now` 기준으로 바꾸면(`is_echo(self.now, …)`) **빨강** |
| **I-a** `kosCalledAt` 파싱 실패 | `day/services/kos_calls.py:113-154` `_made_kos_times` — `(EventLog.id, payload)` 를 읽고, 형식이 틀린 행(`AttributeError` · `TypeError` · `ValueError`)은 그 행만 건너뛴다 · 경고 1줄 `kos call times skipped (bad payload) hospital=… event=…`(값 없음) · 회차는 계속 · 병원 id 인자 추가(부르는 곳 `apply`) | `tests/day/notifications/test_kos_calls_flow.py:249` — 틀린 payload 의 `call.create`(source kos) 행이 있어도 KOS 호출 1개가 생기고, 경고 1줄에 병원 · event id 가 있고 값은 없다 | 거름을 빼면(`except KeyError`) **빨강**(회차 예외) |
| **I-b** | 변경 없음 | — | 스펙 반영 3(#965 · W2 합집합)에 들어가면 닫힌다 |
| **I-c** | 변경 없음 | — | 리포트가 「문제없음」으로 판정(거짓 실패 없음 · 변이 판별은 뒤쪽 단언) |

## 검증

- `./scripts/test.sh -q`(격리 PG · Redis): `test_kos_calls.py` · `test_kos_calls_flow.py` · `test_kos_calls_races.py` · `board/test_kos_call_rules.py` → **46 passed**(9.97초).
- `uv run ruff check` · `ruff format --check`(636 파일) · `mypy backend/day`(311 파일) · `mypy backend/tests/day/notifications` → 모두 통과.
- 변이 2건: 모두 빨강을 확인한 뒤 되돌렸다(`cmp` 로 원본과 같음 확인).
- 브리프 범위대로 전체 `scripts/test.sh` 는 돌리지 않았다. 바뀐 코드는 `_made_kos_times` 하나이고, 위 시험이 그 경로를 덮는다.

## 이슈

- 없음. 스펙 반영 4건(W1 ① · W1 ② · W2 · I3 → #965)은 be-fix-1 보고서 그대로다.
