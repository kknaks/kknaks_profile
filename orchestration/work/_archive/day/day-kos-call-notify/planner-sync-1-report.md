# planner sync-1 결과 — 상태: done

#965 스펙을 #283 구현에서 정한 것에 맞췄다. 커밋 `fe203994` 을 PR #965 에 push 했다(PR head = `fe2039949a333583e04109929a77dbb34a0bf3ef` 확인 · OPEN · 머지 안 함). 코드 레포는 읽기만 했다.

## 반영한 것

| # | 자리 | 바뀐 것 |
|---|---|---|
| 1 | SPEC-002 규칙 40 ① · §3 KOS 읽기 `doctor_called_at` 줄 · 「호출 취소」 줄 | 「바뀌었고」 → 「늦어졌고(앞으로만 · 빈 값 → 값 포함)」. 앞 시각으로 되돌린 값은 새 호출이 아니다. 「값이 그대로이거나 앞 시각으로 돌아가면 아무것도 안 함」 |
| 2 | 규칙 40 ① · ⑧ | 규칙 40 이 이미 만든 호출의 KOS 시각(`event_log` `call.create` payload `kosCalledAt`) 중 최댓값 이하면 만들지 않는다(오늘 것 · 같은 tx · 방문 잠금 안). 형식이 틀린 행은 그 행만 건너뛰고 회차는 계속한다(경고 로그 1줄). `doctor_called_at` 저장 규칙은 그대로다. ⑧ payload 에 `kosCalledAt: {taskId: 시각}` 를 더했다 |
| 3 | 규칙 40 ② · OQ-107 ⓒ · SPEC-005 「KOS 에서 건 호출」 받는 계정 · OQ-N22 | 시스템 계정 직원이 부른 `kind = one` 호출의 받는 사람 = `target_staff_id` ∪ `called_doctor` 원장. 규칙 40 호출은 결과가 같다. 시스템 계정으로 DAY 에서 누른 지정 호출은 지정 원장 + `called_doctor` 원장이 받는다(~~지정 원장이 못 받음~~) |
| 4 | 규칙 40 ② · SPEC-005 받는 계정 | 대표 = 묶음에서 sequence 가 가장 작은 작업의 `calledDoctors` 첫 원장 |
| 5 | 규칙 40 머리 · SPEC-005 「언제」 ② | 「(ㄱ)(ㄴ) 두 경로」를 코드 표대로 고쳤다. 포함: 10초 일정 조회 · 예약 상세 연쇄 두 커밋(점유 이동은 `taken_by_poll` 이면 rollback) · 외부 연동 사본 `_save_scoped_schedules` · 외부 연동 날짜 `_load_date`(오늘은 안 탐 · 무해). 뺌: `emr_date_sync`(오늘이면 건너뜀) · `emr_backfill`(오늘 이상이면 입력 오류) |
| 6 | 개정 ㉚ 머리 요약 · `log.md` | 위 1 ~ 5 를 한 줄로 요약해 넣었다. log 에 spec-change 한 줄(DAY-SPEC-002 · 005) |

## 검증

- `python3 scripts/lint-pipeline.py --strict` → 0 error · 263 warning(모두 다른 제품 · products/day 0 줄). pre-commit hook 도 같은 결과.
- diff: spec-002 16줄 · spec-005 6줄 · log 1줄. 다른 계약은 바꾸지 않았다.

## 반영하지 않은 것 · 코디가 볼 것

- be-impl-r1 이슈 1(관측 = `_apply_tasks` · 판정 · 생성 = 같은 transaction 의 커밋 서비스 `kos_calls.apply`): 지시 목록 밖이라 넣지 않았다. 스펙은 「`_apply_tasks` 에서 판정」 그대로다. 결과(같은 transaction · 잠금 뒤)는 같다.
- be-fix-1 이슈(DAY 호출 메아리 시각은 `kosCalledAt` 에 없음 → 빈 값으로 되돌렸다 다시 오는 경우는 ⑥ 창에만 기댐): 계약 변경이라 넣지 않았다.
- 개정 ㉚ 머리의 「**코드에는 아직 없다.**」는 #283 이 아직 머지되지 않아 그대로 두었다.
