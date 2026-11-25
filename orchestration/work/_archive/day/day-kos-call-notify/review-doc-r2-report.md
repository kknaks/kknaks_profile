# 리뷰 리포트 — day-kos-call-notify / doc r2 (2026-11-25)

- 대상: 워크트리 `mediness-mediness/day-kos-call-notify-spec` 미커밋 diff(`git diff origin/main -- products/day/` · 6 파일 +112 −15)
- 기준: r1 리포트 `review-doc-r1-report.md`(W1 ~ W9) · r2 발주서 `day-kos-call-notify-spec-r2-brief.md` §3(코디 결정) · r1 발주서 §3
- 코드 대조: CENTURION_DAY `origin/dev` `55e60aa4`(읽기만)
- lint: `python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning · exit 0** · `products/day/` 줄 0(나머지는 다른 제품이라 무관)
- allowed_paths: 리포 수정 0 · 산출물 = 이 파일 1개

## 판정: WARN

FAIL 은 없다. W1 ~ W9 는 r2 발주서 §3 대로 모두 고쳐졌다. 그중 W2 · W3 · W4 · W6 · W7 · W8 · W9 는 닫혔다.
남은 것은 둘이다. W1 은 planner 가 짚은 「2xx 없이 failed」 경우에 엉뚱한 수락이 그대로 남아 **부분만 닫혔다**. W5 는 고친 문장이 새 해석 갈래 둘을 만들었다(N1 · N2).
**N1 은 구현 전에 한 줄로 정하기를 강하게 권한다.** 문장을 한쪽으로 읽으면 KOS 「전체 호출」 알림이 0건이 된다.

## r1 W 닫힘 / 남음

| W | r2 발주서 §3 결정 | 고친 곳 | 판정 | 비고 |
|---|---|---|---|---|
| W1 | ⑤에 메아리 거름 두 조건 (i) 그 sequence 의 `call-tasks-doctors` op 이 `pending` · `sent` 면 안 함 (ii) READY · `doctors[]` 를 호출 `created_at` 뒤 회차에서 본 경우만 | `spec-002-procedure-board.md:1274` | **남음(부분)** | 결정대로 들어갔다. 다만 두 조건 밖 경우에 엉뚱한 수락이 남는다 → 아래 R1 |
| W2 | 판정 자리 = `_apply_tasks` · 두 경로 이름 · 두 커밋 뒤 `after_call` | `spec-002:1269` · `spec-005-notifications.md:251` | 닫힘 | (ㄱ) `sync_schedules.py:329` 잠금 → `:421` · (ㄴ) `emr_sync.py:457` · `:493` → `sync_tasks.py:196` → 같은 `_apply_tasks` — 코드와 맞다. 「(ㄴ) 이 먼저 저장해도 놓치지 않음」도 맞다(판정이 같은 자리라서) |
| W3 | ①에 방문 잠금 뒤 이전 값 읽기 · migration 없음 | `spec-002:1270` | 닫힘 | 두 경로 모두 잠금(`sync_tasks.py:91-101` · `:215`)을 잡은 뒤 `existing` 을 읽는다(`:268-295`) · 판 조작도 같은 키(`board_transactions.py:70-72` · `:105-110`) |
| W4 | ③ 근거를 「미확인」으로 · OQ 하나 · 기본값 = 허용 오차 안이면 한 호출 | `spec-002:1272` · OQ-106 `:1495` · `spec-005:253` | 닫힘 | 「차」가 두 개씩 비교인지 전체 범위(최대 − 최소)인지는 정하지 않았다 → R4(낮음) |
| W5 | 2명 이상 = 그 원장들만 · OQ-100 ⓐ 기본값 · kind · target · 본문 · 재호출 · 표시를 한 가지로 | `spec-002:1271` · OQ-100 `:1489` · OQ-107 `:1496` · `spec-005:234` · `:252` · OQ-N22 `:500` | **남음(새 갈래)** | 결정대로 들어갔다. 고친 문장이 해석 갈래 둘을 만들었다 → N1(높음) · N2(중간) |
| W6 | (라) = 2xx 없이 failed 만 「안 불림」 · 2xx 뒤 failed 는 `updated_at` + 허용 오차까지 메아리 | `spec-002:1275` · OQ-101 `:1490` | 닫힘 | 판별 칸이 따로 없다 → R3(낮음) |
| W7 | ④에 「prod 동기화가 배포 직전까지 돌 때」 조건 · 운영 메모에 worker 확인 · OQ-102 배포 전 닫기 | `spec-002:1276` · OQ-102 `:1491` · `spec-005:260` | 닫힘 | — |
| W8 | 「적지 않음 = 꺼짐 · 빈 값은 쓰지 않는다」 | `spec-006-reservation-board.md:556` | 닫힘 | `common/config.py:80` 사실과 맞다 |
| W9 | ⑨ [재호출] 대상 = 사슬 맨 처음 호출의 대상 | `spec-002:1278` | 닫힘 | `board_rules.py:190-195` `recall_target` → `chain_root` 와 맞다. 2명 이상이 뿌리일 때 대표 한 명에게만 간다는 결과도 OQ-107 ⓑ 에 적었다 |

## FAIL

없음.

## WARN

### N1 [높음] 「called_doctor 행으로 받는 사람 계산」이 `kind = all` 규칙 40 호출에도 걸리는지 문장이 갈린다. 걸리면 전체 호출 알림이 0건이 된다
- 위치: `spec-002-procedure-board.md:1271`(「이 계산은 **규칙 40 이 만든 호출**(`called_by_staff_id` = 그 병원 시스템 계정 직원 — ⑧)에만 쓴다」) · `spec-005-notifications.md:252`(「규칙 40 이 만든 호출 — `called_by_staff_id` = 시스템 계정 직원 — 에만」)
- 근거: 이 판별 문구는 2명 이상 줄 안에 있다. 그런데 판별 조건으로 `called_by_staff_id` 하나만 이름 지었고 `kind` 는 적지 않았다. 구현이 「호출자 = 시스템 계정이면 called_doctor 행으로 계산」으로 짜면, ② 기본값의 **전체 호출**(빈 `calledDoctors` → `kind = all`)은 called_doctor 원장 행이 0개라 받는 사람이 0명이다. 지금 `_recipients` 는 `kind` 로만 가른다(`services/notifications.py:310-330`). 이 계산을 끼워 넣을 자리가 이 함수 하나라, 판별 조건을 무엇으로 쓰는지가 결과를 그대로 정한다. 이 경우는 OQ-99 기본값이 가리키는 **바로 그 경우**다.
- 고칠 방향: 두 곳에 「`kind = one` 인 규칙 40 호출만 called_doctor 행으로 계산 · `kind = all` 은 위 「받는 계정」(원장 목록 전부) 그대로」를 한 줄 넣는다.

### N2 [중간] 2명 이상 지정에서 ③ 묶음의 「같은 ② 대상」이 집합 일치인지 대표 일치인지 정해지지 않았다
- 위치: `spec-002:1272` · `spec-005:253`
- 근거: 2명 이상이면 호출 칸은 `kind = one` · `target_staff_id` = 첫 원장뿐이다(`spec-002:1271`). 같은 회차에 작업 X 가 `{A, B}`, 작업 Y 가 `{A, C}` 로 불렸다면, 「대상」을 칸 값(`one` · A)으로 비교하면 한 호출로 묶인다. 그러면 받는 사람 = 두 작업 called_doctor 합 `{A, B, C}` 가 된다. 이때 B 는 Y 를, C 는 X 를 지정받지 않았는데 「시술 2건」 알림을 받는다. 집합으로 비교하면 호출이 둘이 된다. 두 해석 모두 스펙과 어긋나지 않는다.
- 고칠 방향: ③에 「② 대상이 같다 = 같은 `kind` 이고, 지정이면 원장 목록 원장 **집합**이 같음」을 적는다.

### R1 [중간] W1 두 조건 밖 — 2xx 없이 `failed` 된 DAY 호출에 KOS 옛 READY · 옛 집도의가 수락으로 들어간다(planner 주의 사항 판단)
- 위치: `spec-002:1274` (i) · (ii)
- 근거: DAY [의사 호출]의 `call-tasks-doctors` op 이 보내기 전에 `failed` 가 되면(직원 토큰 없음 `decide_token_wait` · `outbox_rules.py:79-87` / 앞 쓰기 실패로 막힘 BLOCKED · `outbox_persistence.py:297`) KOS 는 불리지 않았다. 그 작업이 KOS 에서 옛 집도의를 가진 READY 였다면 그대로 READY 다. 이때 두 조건이 모두 통과된다. (i) op 이 `pending` · `sent` 가 아니고 (ii) 호출 `created_at` 뒤에 시작한 회차에서도 KOS 는 계속 READY 를 준다. 그래서 ⑤가 옛 집도의로 `doctor_call_accept` 를 만들고, 원장이 누르지 않은 「{원장} 수락 완료」가 생긴다. 직원 토큰 없음은 실제로 생길 수 있는 경로다(OQ-104 기본값이라 DAY 호출에 걸린다). 정상 경로에서는 이 문제가 없다. op 이 `confirmed` 되려면 KOS 에 WAITING 이 보여야 하므로(`outbox_rules.py:89-111` · `writes.py:492-497` 확인 = `waiting`) 그 뒤 READY 는 새 수락이다. 규칙 40 이 만든 호출도 ⑦ 「KOS WAITING」에서만 생기므로 괜찮다.
- 고칠 방향: (ii)를 「잠금 뒤 읽은 이전 DAY 값이 READY 가 아니었다가 이번에 READY(전이)」로 바꾸거나, (i)에 「그 작업의 그 호출 op 이 `failed` 면(2xx 여부 무관) ⑤를 하지 않음」을 더한다. 앞쪽이 더 단순하고 W3 의 잠금 뒤 읽기와 같은 자리다. 참고로 op 이 대기 중일 때 동기화는 `status` 칸을 DAY 이전 값으로 둔다(`sync_tasks.py:335-336` held). 그래서 전이 판정은 op 이 끝난 뒤 회차에서 자연스럽게 일어난다.

### R2 [낮음] SPEC-002 개정 ㉚ 머리 요약이 r2 와 어긋난다
- 위치: `spec-002:49`(「묶음 = 같은 방문 · 같은 회차 · 같은 시각 · 같은 대상」)
- 근거: 본문 ③ `:1272` 은 「시각 차가 허용 오차 안」으로 바뀌었다(W4). 머리 요약에는 W1 거름 · W5 「그 원장들만」 · W2 두 경로도 들어 있지 않다. `log.md` 의 r1 줄(「2명 이상 = 전체 — 기본값」)은 이력이라 r2 줄이 더해진 것으로 맞다.
- 고칠 방향: `:49` 의 「같은 시각」을 「시각 차 허용 오차 안(r2)」으로 고치고 r2 요약 한 구절을 더한다.

### R3 [낮음] (라)의 「2xx 를 한 번도 받지 않은 op」을 가릴 칸이 따로 없다
- 위치: `spec-002:1275`
- 근거: `external_outbox` 에는 2xx 이력 칸이 없다(`models/task.py:303-326` — `status` · `attempts` · `checks` · `last_error`). 가를 수 있는 근거는 `last_error` 값(BLOCKED · 토큰 없음 = 보내기 전 · STALE = 2xx 뒤)이다. `_retry_or_fail`(`outbox_rules.py:35-39`)은 보내기 오류(4xx · 5xx · 시간 초과)와 「반영 안 됨」 재전송 소진 모두에서 나오므로 2xx 여부가 섞인다. 스펙대로 「`_retry_or_fail` = 메아리 창」으로 두면 안전한 쪽(알림 덜 감)이다.
- 고칠 방향: 「판별 = `last_error` 가 BLOCKED · 토큰 없음이면 보내기 전 · 그 밖 `failed` 는 모두 메아리 창」으로 한 줄 적는다.

### R4 [낮음] ③ 「새 시각끼리의 차」 기준이 두 개씩인지 범위인지
- 위치: `spec-002:1272` · OQ-106 `:1495`
- 근거: 두 개씩 비교면 0 · 25 · 50초 세 작업이 사슬처럼 한 호출로 이어진다. 범위(최대 − 최소 ≤ 허용 오차)면 둘로 갈린다. 10초 회차 하나 안에서는 드문 경우다.
- 고칠 방향: 「가장 이른 새 시각과의 차」처럼 기준 하나를 적는다.

## 검수 항목 2 — W5 고친 줄이 다른 곳과 어긋나나

| 닿는 곳 | 결과 | 근거 |
|---|---|---|
| `after_call` 받는 사람 | N1 만 남음 | `notifications.py:310-330` 이 kind 로 가르므로 끼울 자리가 하나 · 행 중복 막기는 그대로(`:332-407`) |
| 늦은 재시도 다시 계산 | 감수로 적음(OQ-107 ⓓ) | `send_call_push` 가 `ensure_call_rows` 를 다시 부름(`notifications.py:546-549`) · 새로 쓰는 행은 추가뿐(`fresh = to − have`) |
| 앱 대리 수락 | 맞음 | 기본 원장 = 대표(`app/lib/ui/accept.dart:17-18` `proxyDefault`) · 수락은 원장 목록 누구나(`board_calls.py:244-246` `is_listed_doctor`) → 다른 지정 원장도 고를 수 있음 |
| 푸시 [수락] 버튼(`CALL` 카테고리) | 영향 없음 | 대상이 아니라 권한으로 판정(`notifications.py:438-462` `_accept_staff`) → 대표가 아닌 지정 원장도 버튼을 받음 |
| [재호출] | 맞음(OQ-107 ⓑ) | `recall_target` 은 뿌리의 `one` · `target_staff_id` → 대표 한 명 |
| 판 표시 | 맞음(OQ-107 ⓐ) | 웹 `board_parts.html:238` · `:82` `doctor_name(call.targetStaffId)` · 앱 `format.dart:145-146` `callTargetLabel` → 대표 이름 하나 · 새 글자 없음 |
| 앱 「응답 없음」 | 정보 | `room_screen.dart:263-266` — 사슬 처음 대상과 지금 대상이 다르면 「{처음 원장} 응답 없음」(기존 글자). ④가 KOS 대상으로 사슬을 이으면 이 줄이 처음 보이게 된다. 어긋남이 아니라 의도대로 읽힌다 |
| 호출 취소 알림 받는 사람(SPEC-005 「호출 취소」 `:302`) | 맞음 | 받는 사람 = 그 호출의 원장 호출 알림 행을 받은 계정(`notification_cancel.py:125-137`) → 2명 이상 지정이면 그 원장들 그대로 · 원래 알림 닫기도 같은 행 기준(`:170-181`) |
| 본문 「지정 호출」 | 맞음 | `call_body` 가 `kind = one` 이면 「지정 호출」(`notifications.py:96-102`) · 0.1.0 payload 모양 그대로 |
| OQ-99 와 얽힘 | 적힘 | KOS 전체 호출이 원장 전원을 주면 「전원 지정 호출」이 된다 — OQ-99 `:1488` 에 「그때는 고쳐야」로 적혀 있음 |

## 검수 항목 4 — r1 에서 맞다고 본 줄

다시 쓰인 곳이 없다. A1 · A3 · A6 ~ A9 · B1 ~ B4 · C 줄과 planner 7건의 근거 문장은 그대로다. 바뀐 것은 r2 결정이 닿는 문장뿐이다. lint `--strict` 결과 `products/day/` 는 ERROR 0 · WARN 0 이다.

## 직원이 실물에서 만날 자리

- KOS 「전체 호출」 뒤 원장 누구에게도 알림이 안 간다 — N1 을 `called_by` 로만 갈라 구현했을 때.
- KOS 토큰이 없는 간호사가 DAY 에서 의사 호출 → 「KOS 반영 실패」 토스트 뒤, KOS 에 남아 있던 옛 집도의 이름으로 「수락 완료」가 뜬다(R1).
- 한 고객의 두 시술에 서로 다른 원장 두 명씩 지정하면, 한 원장이 자기가 지정받지 않은 시술까지 「시술 2건」 알림으로 받는다(N2 · 대표 비교로 구현했을 때).
- 2명 지정 호출이 판 · 앱에는 첫 원장 이름 하나로만 보이고, DAY [재호출]은 그 한 명에게만 간다(OQ-107 · 감수).

## 참고(기존 부채)

- SPEC-002 ㉘ 본문 「㉚ C36」 글자 — r2 발주서대로 건드리지 않았다(맞음).
