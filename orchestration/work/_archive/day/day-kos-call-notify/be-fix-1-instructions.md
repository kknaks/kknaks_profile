# [backend] #283 코드 검수 r1 지적 전부 고치기 (be-fix-1)

같은 워크트리 · 같은 맥락(`/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify` · 미커밋 1루프 변경 위). 역할 · allowed_paths · 금지는 첫 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/day-kos-call-notify-be-brief.md` 그대로.

검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-code-r1-report.md` — **WARN 4 · INFO 6 전부 읽어라.** 사용자 지시 「작은 지적도 해야지」 — 아래 전부 이번에 고친다.

## 코디 결정 (되묻지 마라)

- **W1 중복 알림(늦은 사본)** 두 겹으로 막는다:
  1. `call_changed` 는 앞으로만 — `before is None or called_at > before`.
  2. 빈 값/옛 값으로 되돌았다가 다시 같은 시각이 오는 경우(ⓓ → ⓔ): `doctor_called_at` 저장 규칙은 **바꾸지 않는다**(동기화는 KOS 값을 그대로 씀). 대신 규칙 40 이 호출을 만들 때 `event_log` payload 에 그 KOS 호출 시각(`kosCalledAt`)을 남기고, 후보의 KOS 시각이 그 작업에 대해 **이미 호출로 만든 KOS 시각 중 최댓값 이하**면 만들지 않는다(같은 transaction · 방문 잠금 안에서 조회). migration 없음 · 새 테이블 없음. 기존 event_log 칸 · 인덱스로 조회가 무거우면 보고서에 쿼리 비용을 적어라.
  - 시험: ⓐ ~ ⓔ 순서 그대로 재현 → 호출 1 · 알림 1.
- **W2** 시스템 계정 분기 받는 사람 = `target_staff_id` ∪ `called_doctor` 원장(합집합). 시험: 시스템 계정 직원으로 DAY 지정 호출 → 그 원장이 받음 · KOS 2명 지정 규칙 40 호출 결과는 전과 같음.
- **W3** `_chain_room_assign`(상세 연쇄) 커밋 두 곳의 after_commit 배선 시험 — 가짜 adapter 로 연쇄 한 번 → 알림 1(`test_board_room_chain.py` 틀 재사용). 두 줄을 지우면 빨개지는지 변이로 확인.
- **W4** 판 조작 겹침 시험 — 판 조작 tx 가 `board:{visit}` 를 잡은 채 DAY 호출 op 을 만드는 동안 동기화 `apply_visit_tasks` 를 띄우고, 조작 commit 뒤 동기화가 메아리로 0건. 방문 잠금을 빼면 빨개져야 한다(변이 확인 · 안 되면 이유 보고).
- **I1** `_call_path` 가 잡는 예외를 `EmrError` 계열로 넓힌다(Vegas `UnsupportedVendorError` 포함). 회차 전체 rollback 동작(예외 삼키지 않음)은 그대로 둔다.
- **I3** 묶음 대표 원장 = 그 묶음에서 **sequence 가 가장 작은 작업**의 `calledDoctors` 첫 원장. 시험 1개.
- **I5** `_system_staff` 를 공개 이름으로(`board_transactions` 에서 `system_staff` 등 · 기존 `board_quick_start.py:82` 사용처도 같이) · Taut 통과.
- **I2 · I4** 코드 변경 없음 — 보고서에 「그대로 둔 이유」 한 줄씩. **I6** 코드 변경 없음(코디가 dev 실물에서 확인).

## 검증

- `cd backend && uv run pytest -q <새 · 바뀐 시험 + 동기화 · 판 호출 · 알림 기존 시험>` 1회 · `uv run ruff check · ruff format --check · mypy` 바뀐 파일 · 끝에 `scripts/test.sh` 전체 1회(수치).
- 커밋 · push 금지. 스펙과 다른 판단(W1-2 · I3)은 보고서에 「스펙 반영 필요」로 표시 — 코디가 #965 에 넣는다.

## 보고

`/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/be-fix-1-report.md` — 지적마다 [고친 파일:줄 · 시험 · 변이 결과]. 완료 보고 두 명령(subject 「backend 완료: be-fix-1」 · 이번 dispatch 값 · 코디 term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce):

```bash
orca orchestration send --to term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: be-fix-1" --body "<요약>"
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[worker_done] backend 완료 — be-fix-1 <한 줄>. 상세는 인박스." --enter
```
