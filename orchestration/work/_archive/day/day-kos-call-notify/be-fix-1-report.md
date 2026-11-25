# day-kos-call-notify be-fix-1 결과 보고 (코드 검수 r1 지적 전부)

## 상태: done (커밋 · push 없음 — 1루프 미커밋 변경 위에 덧댐)

## 지적별 — 고친 곳 · 시험 · 변이

경로는 `backend/` 기준.

| 지적 | 고친 파일:줄 | 시험 | 변이 결과(되돌림 확인) |
|---|---|---|---|
| **W1 ①** 앞으로만 | `day/dtos/sync_state.py:43-51` `call_changed` = `before is None or called_at > before` | `tests/day/board/test_kos_call_rules.py:133`(앞 시각으로 되돌림 = 후보 아님) | `>` → `!=` 면 **빨강**(1 failed) |
| **W1 ②** 이미 만든 KOS 시각 이하 거름 | `day/services/kos_calls.py:105-132` `_made_kos_times`(event_log `call.create` · source kos · 오늘 · payload `kosCalledAt` 작업별 최댓값) · `:189` 거름 · `:277` payload `kosCalledAt: {taskId: ISO 시각}` · `:344` 같은 tx(방문 잠금 안)에서 조회 | `tests/day/notifications/test_kos_calls_flow.py:204` ⓐ ~ ⓔ 재현(V0 → V1 → 빈 값 → V1 → V0 → V1 = 호출 2개(V0 · V1) · K1 알림 1 · 푸시 1) + 정말 다시 부름(V2) = 새 호출 | 거름 삭제면 **빨강** |
| **W2** 시스템 계정 분기 합집합 | `day/services/notifications.py:337-355` `target_staff_id` ∪ `called_doctor` 원장 | `tests/day/notifications/test_kos_calls.py:123`(시스템 계정 로그인 DAY 지정 호출 · KOS 에 앞 원장 called_doctor → 지정 원장이 받음) · 기존 2명 지정 시험 그대로 통과 | 합집합 제거면 **빨강** |
| **W3** 상세 연쇄 커밋 두 곳 배선 | 코드 변경 없음(`day/services/emr_sync.py:468` · `:504`) | `tests/day/notifications/test_kos_calls_races.py:65` — `test_board_room_chain` 의 `BoardKos` 를 이어받은 가짜 KOS 로 `run_outbox` 연쇄 한 번 · 호출이 ① 첫 상세 / ② 확인 상세에서 보이는 두 경우(parametrize) → 각각 알림 1 · 푸시 1 | `:468` 삭제 → 「첫_상세_커밋」 **빨강** · `:504` 삭제 → 「확인_상세_커밋」 **빨강** |
| **W4** 판 조작 겹침 | 코드 변경 없음 | `tests/day/notifications/test_kos_calls_races.py:88` — DAY [의사 호출] 을 `_finish`(commit) 앞에서 멈춰 `board:{visit}` · op 을 쥔 채, 동기화(`_apply_detail` → `apply_visit_tasks`)를 띄움 → 0.5초 뒤 아직 기다리는 중 · 조작 commit 뒤 동기화는 메아리로 0건 · 호출 = DAY 호출 1개 · 푸시 1 | `apply_visit_tasks` 의 `lock_visits` 제거면 **빨강**(동기화가 기다리지 않고 KOS 호출을 하나 더 만듦) |
| **I1** `_call_path` 예외 | `day/services/kos_calls.py:67-71` `except EmrError`(`WriteNotSupportedError` · `UnsupportedVendorError` 둘 다) · 회차 rollback 동작은 그대로 | `tests/day/board/test_kos_call_rules.py:157`(KOS = 경로 · Vegas = None) | — |
| **I3** 묶음 대표 원장 | `day/services/kos_calls.py:218-228` 묶음마다 sequence 가 가장 작은 작업의 `calledDoctors` 첫 원장 | `tests/day/notifications/test_kos_calls.py:150`(가장 작은 sequence 가 받은 차례 · 시각 차례 모두 가운데) | 「마지막 작업」 · 「첫 작업」 둘 다 **빨강** |
| **I5** 공개 이름 | `day/services/board_transactions.py:349` `system_staff` · `:227` · `day/services/board_quick_start.py:31` · `:79-108`(지역 변수 `system_staff` → `system_id` — 이름 겹침) · `day/services/kos_calls.py:343` | 기존 판 「바로 시작」 시험 · 전체 회귀 | Taut check 진단 0 |
| **I2** | 변경 없음 | — | 그대로 둔 이유: 스펙 R3 판별(`last_error` BLOCKED · 토큰 없음 = 보내기 전) 그대로이고, `external_outbox` 에 2xx 이력 칸이 없어 migration 없이 더 가를 수 없다. 틀리면 알림이 한 번 더 가는 쪽(빠지지 않음) |
| **I4** | 변경 없음 | — | 그대로 둔 이유: 정상 회차의 새 호출은 0 ~ 2개다. `after_call` 은 호출마다 3초 상한에 실패를 삼키므로, 잠금 TTL(60초)에 닿는 것은 멈췄던 동기화의 첫 회차(⑦ · OQ-102 와 같은 운영 메모)에서 20개 넘게 생길 때뿐이다 |
| **I6** | 변경 없음 | — | 코디가 dev 실물에서 확인(OQ-101 KOS ↔ DAY 시각) |

### W1 ② 쿼리 비용

- 후보가 있는 회차에만 1회 돈다(후보 없는 회차는 추가 쿼리 0). `SELECT payload FROM event_log WHERE visit_id IN (후보 방문들) AND type = 'call.create' AND deleted_at IS NULL AND occurred_at >= 오늘 0시`.
- 기존 부분 인덱스 `ix_event_log_visit_id_type (visit_id, type) WHERE deleted_at IS NULL`(migration 0006)를 탄다. 방문 하나의 오늘 `call.create` 행 수(DAY · KOS 호출 수 — 보통 몇 개)만 읽고 payload 는 Python 에서 거른다. 새 인덱스 · migration 없음.

## 스펙 반영 필요 (코디 → #965)

1. **W1 ①** 규칙 40 ① 「바뀌었고」 → 「**늦어졌고**(앞으로만 · 빈 값 → 값 포함)」. 늦게 커밋된 옛 사본이 앞 시각으로 되돌린 값은 새 호출이 아니다.
2. **W1 ②** 규칙 40 ①(또는 ⑧): 규칙 40 이 호출을 만들 때 `event_log` `call.create` payload 에 작업별 KOS 호출 시각 `kosCalledAt`(`{taskId: 시각}` — 이름 제안)을 남긴다. 후보의 KOS 시각이 그 작업에 대해 이미 만든 KOS 시각 중 최댓값 이하면 만들지 않는다(오늘 것 · 같은 tx · 방문 잠금 안). `doctor_called_at` 저장 규칙은 그대로다(동기화는 KOS 값을 그대로 씀).
3. **W2** DAY-SPEC-005 「KOS 에서 건 호출」 받는 계정 · 규칙 40 ②: 시스템 계정 직원이 부른 `kind = one` 호출의 받는 사람 = **`target_staff_id` ∪** 그 호출 작업들의 `called_doctor` 원장. 규칙 40 호출은 결과가 같다. OQ-107 ⓒ 의 결과가 「지정 원장이 못 받음」에서 「지정 원장 + called_doctor 원장」으로 바뀐다.
4. **I3** 규칙 40 ② 2명 이상: 묶음의 대표(`target_staff_id`) = 묶음에서 **sequence 가 가장 작은 작업**의 `calledDoctors` 차례상 첫 원장.

## 검증 — 명령과 수치

- 새 · 바뀐 시험 + 동기화 · 판 호출 · 알림 회귀는 아래 전체 실행에 포함된다. 개별: `test_kos_calls.py` 13 · `test_kos_calls_flow.py` 15 · `test_kos_calls_races.py` 3 · `test_kos_call_rules.py` 13(순수) — 모두 통과.
- `./scripts/test.sh --pure -q backend/tests/day/board/test_kos_call_rules.py backend/tests/devtools/test_verification_formal.py backend/tests/architecture` → **346 passed**.
- `./scripts/check.sh --static` → ruff · format(658 파일) · strict mypy(655 파일) · Taut check 진단 0 · Taut audit 완료. frontend 단계만 실패한다(이 워크트리에 npm 패키지 없음 · 1루프와 같음 · 프론트 미수정).
- 전체 `./scripts/test.sh -q`(격리 PG · Redis) → **2909 passed · 0 failed**(343초).
- 변이 9건(위 표): 모두 빨강을 확인한 뒤 되돌렸다.
- 브리프의 `uv run pytest` 대신 리포 정본 러너 `scripts/test.sh` 를 썼다(격리 인프라 · 사용자 스택 · 포트 · 공유 DB 무접촉).

## 이슈 · 코디가 확인할 것

- W1 ② 는 **규칙 40 이 만든 호출만** 기록한다. DAY 에서 누른 호출이 KOS 를 거쳐 돌아온 시각(메아리)은 `kosCalledAt` 에 없다. 그래서 메아리 창이 지난 뒤 옛 사본이 그 DAY 호출의 시각을 빈 값 → 값으로 되돌려 놓으면, 그 경우는 여전히 ⑥ 창에만 기댄다. 다만 W1 ① 이 「앞 시각으로 되돌림」은 막는다. 빈 값으로 되돌렸다가 다시 오는 경우만 남는다(r1 W1 보다 좁다).
- 1루프 보고의 「겹침 시험 한계」(이슈 2)는 W4 시험으로 닫혔다. 방문 잠금을 빼면 빨강이다.
