# 리뷰 리포트 — day-kos-call-notify / doc r3 (2026-11-25)

- 대상: 워크트리 `mediness-mediness/day-kos-call-notify-spec` 미커밋 diff 중 r2 지적 6건(N1 · N2 · R1 ~ R4)만. r2 에서 닫힌 것은 다시 보지 않는다.
- 기준: r2 리포트 `review-doc-r2-report.md` · r3 발주서 `day-kos-call-notify-spec-r3-brief.md` §3
- 코드 대조: CENTURION_DAY `origin/dev` `55e60aa4`(읽기만)
- lint: `python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning · exit 0** · `products/day/` 줄 0(나머지는 다른 제품이라 무관)
- allowed_paths: 리포 수정 0 · 산출물 = 이 파일 1개

## 판정: PASS

6건 모두 r3 발주서 §3 대로 고쳐졌다. 구현을 틀리게 만들 새 모순은 없다. 남은 것은 낮음 2건(참고)이고, 둘 다 구현 착수를 막지 않는다.

## 6건 닫힘 / 남음

| 건 | r3 발주서 §3 결정 | 고친 곳 | 판정 | 근거 |
|---|---|---|---|---|
| N1 | called_doctor 행 받는 사람 계산은 `kind = one` 규칙 40 호출만 · `kind = all` 은 원장 목록 전부 그대로(두 곳) | `spec-002-procedure-board.md:1271` · `spec-005-notifications.md:252` | 닫힘 | 두 곳 모두 「`kind = one` 인 규칙 40 호출만 · `kind = all` 은 위 「받는 계정」 그대로」를 적었다. 코드 `_recipients` 가 `kind` 로 가르는 자리(`services/notifications.py:324-327`)에 그대로 들어간다 → 전체 호출 0명 위험이 사라졌다 |
| N2 | ③ 같은 대상 = 같은 `kind` · 지정이면 원장 집합 | `spec-002:1272` · `spec-005:253` · OQ-106 `spec-002:1495` | 닫힘 | 「대표 `target_staff_id` 만 같은 것은 같은 대상이 아님」까지 적어 해석이 하나로 정해졌다 |
| R1 | ⑤ (ii) = 잠금 뒤 이전 DAY 값이 READY 아님 → 이번 회차 READY · 원장(전이) · (i) 그대로 · held 근거 | `spec-002:1274` | 닫힘 | 옛 문장은 취소선 · (i)은 그대로 · 근거 `emr/sync_tasks.py:335-336`(op 대기 중 `status` held)이 맞다. 2xx 없이 `failed` 된 경우 DB `status` 가 옛 READY 에서 바뀌지 않으므로 전이가 없다 → 엉뚱한 수락이 막힌다 |
| R2 | 개정 ㉚ 머리 요약을 r2 · r3 본문과 맞춤 | `spec-002:49` | 닫힘 | 허용 오차 묶음 · 같은 대상(집합) · 두 경로 · W1 거름 + 전이 · 그 원장들만 · `kind = one` 만 계산 — 모두 들어갔다. OQ 범위 표기 낡음 → 아래 L2 |
| R3 | (라) 판별 = `last_error` BLOCKED · 토큰 없음이면 보내기 전 · 그 밖 `failed` 는 메아리 창 | `spec-002:1275` | 닫힘 | 2xx 이력 칸이 없다는 코드 사실(`models/task.py:303-326`)과 `_retry_or_fail` 섞임(`emr/outbox_rules.py:35-39`)을 근거로 달았다 |
| R4 | ③ · OQ-106 시각 차 = 묶음의 가장 이른 새 시각과의 차 | `spec-002:1272` · `:1495` · `spec-005:253` | 닫힘 | 세 곳이 같은 기준이다(옛 「끼리의 차」는 취소선) |

`log.md` 에 r3 한 줄이 있다(형식 맞음).

## 새 모순 점검(검수 항목 2)

| 짝 | 결과 | 근거 |
|---|---|---|
| R1 전이 × W1 (i) | 모순 없음 | (i)은 op 이 `pending` · `sent` 인 회차를 막는다. 그 회차들에는 `status` 가 held 되어(`sync_tasks.py:335-336` · `pending_guards` 는 `pending` · `sent` 만 · `:104-120`) DB 값이 바뀌지 않는다. 그래서 두 조건은 같은 구간을 가리키고 서로 부딪히지 않는다. op 이 끝난 뒤 회차에서 전이가 보인다 |
| R1 × op held 중 status | 놓침이 생길 수 있음(안전한 쪽) → L1 | DB 값이 옛 READY 인 채로 op 이 진행되는 동안 KOS 가 WAITING → READY(새 수락)로 가면, op 이 끝난 뒤 DB 는 READY → READY 라 전이가 안 보인다. 엉뚱한 수락은 없고, 그 줄은 「호출」에 남는다(지금과 같은 결과) |
| R1 × 규칙 40 이 만든 호출 | 맞음 | 그 호출은 ⑦ 「KOS `WAITING`」일 때만 생기고 같은 transaction 에서 DB `status` 가 `waiting` 으로 쓰인다 → 다음 KOS READY 는 전이다 |
| R1 × 보통 작업 | 맞음 | KOS 작업 처음 상태는 `not_started`(`enums/task.py:9-14`)라, 옛 READY 상태로 시작하는 경우는 드물다 |
| N1 × kind = all 받는 사람 | 맞음 | 원장 목록 전부(`notifications.py:310-330` 그대로) · 호출 취소 알림은 원래 알림 행 기준이라 그대로 따라간다(`notification_cancel.py:125-137`) |
| N2 × R4 | 맞음 | 대상(`kind` + 집합)으로 먼저 나누고, 그 안에서 가장 이른 새 시각 기준 허용 오차로 묶는다 — 한 가지로 짤 수 있다 |

## 남음(낮음 · 착수 막지 않음)

### L1 [낮음 · 안 막음] 옛 READY 인 작업에 DAY 호출 → 짧은 사이 KOS 수락이면 수락 반영을 놓친다
- 위치: `spec-002:1274` (ii)
- 근거: DB `status` 가 옛 `ready` 인 작업(KOS 에 옛 집도의가 남은 경우)에 DAY [의사 호출]을 하면, op 이 `pending` · `sent` 인 동안 `status` 가 held 된다(`sync_tasks.py:335-336`). op 확인(KOS `waiting` 관측) 뒤 다음 10초 회차 전에 KOS 에서 원장이 수락하면, DB 는 `ready` → `ready` 라 전이가 없다. 결과는 「수락 반영 없음」이고, 줄은 「호출」에 남는다. 지금 코드와 같은 결과이고 엉뚱한 수락보다 안전한 쪽이다.
- 고칠 방향(선택): 스펙에 「놓칠 수 있음 · 감수」 한 줄, 또는 OQ-104 에 메모. 구현을 막지 않는다.

### L2 [낮음 · 안 막음] 개정 ㉚ 머리 요약의 OQ 범위 표기가 낡았다
- 위치: `spec-002:49`(「§5 새 「KOS 에서 건 호출」(OQ-99 ~ 105)」)
- 근거: 표에는 OQ-106 · OQ-107 까지 있다(`spec-002:1495-1496`). 같은 줄의 「메아리 거름 — r2 W1」 표기도 원래 지적 번호로는 r1 W1 이다(뜻은 같음).
- 고칠 방향: 「OQ-99 ~ 107」로 고친다. 구현을 막지 않는다.

## 직원이 실물에서 만날 자리

- KOS 에 옛 집도의가 남아 있던 시술을 DAY 에서 다시 부른 직후 KOS 에서 바로 수락하면, DAY 판 줄이 「수락」으로 바뀌지 않고 「호출」에 남는다(L1 · 지금과 같음).
