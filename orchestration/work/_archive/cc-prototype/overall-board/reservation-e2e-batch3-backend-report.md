# 예약 현황 E2E batch 3 — backend 결과 보고
- 2026-10-27 · 기준 `09b1edc` 위 미커밋(procedure/back 만)
## 상태: done

## 처리
| # | 처리 |
|---|---|
| 1 · 3 | 해당 없음(front) |
| 2 | ✔ 상세 `flow.times = {consultation, procedure, home}`(ISO · 근거 없으면 null) — 코디 전달 계약 그대로 |

## 시각 규칙(근거 있는 것만 · 지어내지 않음)
- 원천 = 사본 `flow_step_at`(KOS `flowStepUpdatedDateTimeUtc` = **지금 단계가 된 시각**) + 상세가 매번 다시 읽는 KOS 일정 원본(`consultations[]` · `tasks[]`)
- `consultation`: 상담 대기 · 진행 = 그 단계가 된 시각 / 완료 = 지금 단계가 시술 대기면 그 시각(= 상담 끝) · 아니면 KOS `consultations[].consultationStartedDateTimeUtc` 중 **예약 시작 시각과 다른** 마지막 값(상담 **시작**) · 없으면 null
- `procedure`: 시술 대기 · 진행 · 귀가 대기 = 지금 단계가 된 시각 / 귀가 완료 = KOS 시술(PROCEDURE · DONE) 작업 `completedDateTimeUtc` 마지막 · 없으면 null
- `home`: 귀가 대기 · 귀가 완료 = 그 단계가 된 시각
- ccc 이벤트 시각: 상담 줄에 쓸 만한 것은 [실장 호출] 뿐인데 이미 `consultation.calledAt` 로 있어 front 기본값(times 없으면 since/calledAt)과 겹쳐 `times` 에는 넣지 않음
- 한계: 지난 단계의 「된 시각」은 KOS 가 기록하지 않는다(단계 이력 없음) — 그래서 「상담 완료」 줄은 시술 중 이후엔 KOS 상담 기록이 없으면 비고, 「시술 완료」는 귀가 완료 뒤엔 작업 완료 시각으로만

## 파일
- `app/schemas/reservations.py` — `FlowTimes` · `Flow.times`
- `app/domain/reservation_rules.py` — `consultation_started_at` · `procedure_done_at`
- `app/service/reservations.py` — `refresh_schedule(sink=)` 로 원본을 받아 `_flow` 가 times 계산
- `app/service/fake_reservations.py` — 가짜 times
- tests: `test_resv_reception.py::test_flow_times_from_kos_evidence_only`

## 검증
- `uv run ruff check .` All checks passed · `uv run pytest -q` **334 passed**
