# 리뷰 리포트 — day-kos-call-notify / doc (2026-11-25)

- 대상: 워크트리 `mediness-mediness/day-kos-call-notify-spec` 미커밋 diff(`git diff origin/main -- products/day/`) — SPEC-005 · SPEC-002(개정 ㉚ · 규칙 40 · OQ-99 ~ 105) · SPEC-006(개정 ⑭) · SPEC-007 · `20-spec.md` · `log.md`
- 계약 기준: 발주 브리프 `day-kos-call-notify-spec-brief.md` §2 · §3 · §7
- 코드 대조: CENTURION_DAY `origin/dev` `55e60aa4`(워크트리 `day-kos-call-notify` HEAD = `55e60aa4` 확인) · prod `a6aa4ba5`(④ 확인용)
- 실물: HAR `의사호출2.har` — `call-tasks-doctors` 요청 2건만 있다(01:48:50Z `{scheduleId, sequences:[1]}` · 01:48:56Z `+doctorIds:[1명]`). **일정 응답(`doctorCallDateTime` · `calledDoctors`)은 HAR 에 없다.**
- lint: `python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning · exit 0** · `products/day/` 줄 0(ERROR · WARN 모두). 263 WARN 은 다른 제품(selly 등) — 무관.
- allowed_paths: 리포 파일 수정 0 · 산출물 = 이 파일 1개.

## 판정: WARN

FAIL 은 없다. 브리프 §3 A1 ~ A9 · B1 ~ B4 · C 가 모두 들어갔고 금지 사항(새 알림 종류 · 새 글자 · 새 스위치 · 환경 이름 분기 · 화면 문구 · 「전체 호출」 확정)을 어긴 곳이 없다. planner 가 말한 「브리프와 다른 곳」 7건도 코드 사실과 맞는다(①은 브리프보다 코드가 맞다).
다만 **W1 · W2 · W3 는 구현 착수 전에 스펙에 한 줄씩 넣기를 권한다.** 지금 문장 그대로 짜면 구현자가 두 갈래 중 하나를 고르게 되고, 한쪽은 드문 경쟁 상황에서 틀린 동작(엉뚱한 원장 수락 · KOS 호출을 놓침 · 두 번 만듦)을 낸다.

## FAIL

없음.

## WARN

### W1 [높음] KOS 수락 반영(규칙 40 ⑤)이 DAY 호출 직후 메아리 창에서 옛 KOS 집도의로 자동 수락할 수 있다
- 위치: `spec-002-procedure-board.md:1274`(⑤) · `:1275`(⑥) · `:1493`(OQ-104 기본값 「한다」) · `spec-005-notifications.md:255`
- 근거: ⑤ 조건 = 「수락 안 된 열린 유효 호출 + KOS `doctors[]` 에 원장 목록 원장 + KOS `status = READY`」. OQ-104 기본값으로 **DAY 에서 누른 호출에도** 적용된다. DAY [의사 호출] 직후, 쓰기 큐 op 이 아직 KOS 에 닿기 전(⑥ (가) 구간 — `pending` · 토큰 대기는 `decide_token_wait` 상한까지 길어질 수 있다 · `emr/outbox_rules.py:79-87`)에는 KOS 값이 옛 값 그대로다. 그 작업이 KOS 에서 이미 집도의가 있는 READY 였다면(코드도 「KOS 집도의는 앞 의사로 남아 있을 수 있다」고 적고 있다 · `policies/board_rules.py:140-142` `task_doctor` docstring) 동기화가 곧바로 `doctor_call_accept` 를 만든다. 원장이 누르지 않았는데 「{원장} 수락 완료」가 된다. 메아리 판정(⑥)은 호출을 만들 때만 걸고 ⑤에는 걸지 않았다.
- 고칠 방향: ⑤에도 ⑥과 같은 거름을 넣는다. 예: 「그 작업 `sequence` 가 든 `call-tasks-doctors` op 이 `pending` · `sent` 면 ⑤를 하지 않음」, 또는 「KOS READY 를 그 호출 `created_at` 뒤에 처음 본 경우만」. 어느 쪽을 쓸지 한 줄로 정한다.

### W2 [높음] 규칙 40 을 거는 자리가 「10초 일정 조회」뿐인지, 예약 상세 반영 경로까지인지 하나로 정해지지 않았다
- 위치: `spec-002-procedure-board.md:1269`(「시술 현황 동기화(10초 일정 조회 · 작업 쓰기 `emr/sync_tasks.py`)」)
- 근거: 작업 행을 쓰는 경로가 둘이다. ① 10초 일정 조회(`emr/sync_schedules.py:329` 잠금 → `:421` `_apply_tasks`) ② 이벤트 연쇄의 예약 상세 반영(`services/emr_sync.py:457` · `:493` `_apply_detail` → `emr/sync_tasks.py:196` `apply_visit_tasks` → 같은 `_apply_tasks`). 둘 다 `doctor_called_at` 을 쓴다(`emr/sync_tasks.py:330` · 상세도 같은 `mapper.task` · `emr/kos/mapper.py:516-533`). 스펙 문장대로 ①에만 걸면, 점유 이동 연쇄가 그 방문 상세를 먼저 읽은 경우 KOS 에서 막 건 호출 시각을 ②가 조용히 저장한다. 그러면 다음 10초 회차는 「바뀌지 않음」으로 보고(① 「값이 그대로면 아무것도 하지 않는다」) **그 KOS 호출은 영영 알림이 안 간다.** 반대로 `_apply_tasks` 에 걸면 ②의 커밋(`services/emr_sync.py:464` · `:496`) 뒤에도 `after_call` 을 불러야 하는데 스펙에 그 자리가 없다.
- 고칠 방향: 「규칙 40 은 작업 쓰기 공통 경로(`_apply_tasks`)에서 하고, 그 경로를 부르는 모든 커밋 뒤 이번에 만든 호출마다 `after_call`」로 적는다(②에서는 그 op 이 `sent` 라 ⑥으로 메아리가 된다). 또는 「② 경로는 `doctor_called_at` 을 쓰지 않고 10초 회차에 맡긴다」. 둘 중 하나를 고른다.

### W3 [중간] 같은 KOS 호출로 `doctor_call` 이 두 번 생기지 않는다는 보장(잠금 · 비교 시점)이 스펙에 적혀 있지 않다(검수 항목 3)
- 위치: `spec-002-procedure-board.md:1269-1270`
- 근거: 코드에는 보장 수단이 이미 있다. 판 조작과 두 동기화 경로가 모두 같은 방문 advisory lock `board:{visit_id}` 을 transaction 끝까지 잡는다(`emr/sync_tasks.py:86-101` · `services/board_transactions.py:70-72` · `:105-110`). 그래서 「쓰기 전 값」을 **그 잠금을 잡은 뒤** 읽으면 두 회차 · API 프로세스가 겹쳐도 한 번만 걸린다. 그런데 스펙은 「같은 동기화 transaction 안」이라고만 적었다. 또 지금 비교용으로 읽는 이전 값(`dtos/sync_state.py:12-18` `PreviousTaskData`)에는 `doctor_called_at` 이 없어 구현이 새로 읽어야 한다. 잠금 밖에서 읽는 구현이 나와도 스펙과 어긋나지 않는다. 별도 유일 제약은 없다(`models/task.py:223-235` `doctor_call` 에 호출 근원 칸 · 유일 색인 없음).
- 고칠 방향: ①에 「비교할 이전 `doctor_called_at` 은 방문 잠금(`lock_visits` — 판 조작과 같은 키)을 잡은 뒤 같은 transaction 에서 읽는다. 그래서 동기화 두 회차 · 판 조작이 겹쳐도 한 변화에 호출 하나」를 한 줄 넣는다. migration 은 필요 없다.

### W4 [중간] 묶음(③)의 근거 「한 요청이 그 작업들에 같은 시각을 찍는다」는 확인되지 않은 사실이다. 어긋나면 KOS 클릭 한 번에 알림이 N번 간다
- 위치: `spec-002-procedure-board.md:1272`(③ 근거) · `spec-005-notifications.md:253`
- 근거: HAR `의사호출2.har` 의 두 요청은 모두 `sequences:[1]`(작업 1개)이고, 일정 응답이 없어 `doctorCallDateTime` 값도 없다. 여러 작업을 한 번에 부를 때 KOS 가 작업마다 같은 시각(밀리초까지)을 주는지 본 실물이 없다. 묶음 기준이 「같은 새 `doctor_called_at`」 완전 일치라서, 작업마다 몇 ms 라도 다르면 호출 N개 → 원장 계정마다 알림 · 푸시 N번이 된다(검수 항목 4 「KOS 호출 1건 → 계정당 1번」이 깨진다). 「추측으로 사실 확정 금지」(브리프 §7)에도 걸린다.
- 고칠 방향: ③ 근거 문장을 「미확인 — 첫 실물로 확인」으로 낮추고 OQ 하나를 연다(OQ-99 와 같은 첫 실물 1회에서 여러 작업 동시 호출 1건). 기본값은 「같은 회차 · 같은 방문 · 같은 대상이면서 시각 차가 허용 오차(예: ⑥과 같은 값) 안이면 한 호출」처럼 어긋남에 버티는 쪽을 권한다.

### W5 [중간] 지정 원장 2명 이상을 「전체 호출」로 바꾼 것은 사용자 결정 A2 「지정(1명 이상) = 그 원장(들)」과 다르다
- 위치: `spec-002-procedure-board.md:1271`(② 「2명 이상 = 전체 호출」) · `:1489` OQ-100 · `spec-005-notifications.md:252` · `:500` OQ-N22
- 근거: 브리프 §3 A2 「지정(1명 이상) = 그 원장(들)」. HAR 의 `doctorIds` 는 배열이라 KOS 가 여러 명을 받을 수 있는 모양이다. planner 가 고른 기본값을 따르면 지정되지 않은 원장에게도 알림 · 푸시가 가고, 본문이 「전체 호출」이 된다. planner 는 이것을 「브리프와 다른 곳」 ②로 밝혔고 근거(`doctor_call.target_staff_id` 1칸 · `models/task.py:231`)도 맞다. 그런데 OQ-100 ⓐ(받는 사람을 그 호출 작업들의 `called_doctor` 행으로 계산)는 **migration 없이** A2 를 그대로 지킬 수 있는 안이다. 그 안을 두고도 결정을 뒤집는 쪽이 기본값이 됐다.
- 고칠 방향: 사용자 확인을 받는다(위험으로 보고). 스펙을 고칠 때는 OQ-N22 · OQ-100 「착수 막나」 칸에 「사용자 확인 — 결정 A2 와 다름」을 분명히 적는다. 참고로 지정 1명은 `kind = one` 으로 정확하다.

### W6 [낮음] 메아리 (라) 「op 이 `failed` 면 KOS 가 불리지 않았다」는 코드 사실과 다르다
- 위치: `spec-002-procedure-board.md:1275`((라))
- 근거: `failed` 는 보내기 전 막힘(BLOCKED · 토큰 없음 — `emr/outbox_persistence.py:297` · `emr/outbox_rules.py:79-87`)으로도 되지만, **2xx(`sent`)를 받은 뒤** 확인이 오래 안 되거나(`decide_stale` · `emr/outbox_rules.py:69-76`) 다시 보내기를 다 쓴 경우(`_retry_or_fail` · `:107-108`)에도 된다. 뒤쪽 두 경우는 KOS 가 불렸고 호출 시각이 찍혔을 수 있다. 그 값이 늦게 보이면 (라) 규칙대로 「KOS 에서 건 호출」로 판정된다 → DAY 호출이 하나 더 생기고 알림이 두 번 간다.
- 고칠 방향: (라)를 「`failed` 이면서 한 번도 2xx 를 받지 않았을 때(`attempts` 0 · 보내기 전 막힘)」로 좁힌다. 2xx 를 받은 뒤 `failed` 가 된 op 은 `updated_at` + 허용 오차까지 메아리 창으로 본다.

### W7 [낮음] 「배포 직후 첫 동기화는 ①에 걸리지 않는다」(④)는 prod 동기화가 배포 직전까지 돌았을 때만 맞다
- 위치: `spec-002-procedure-board.md:1276`
- 근거: 코드 사실로는 맞다. prod `a6aa4ba5` 도 이 칸을 동기화한다(`backend/day/emr/sync.py:1530` `"doctor_called_at": t.doctor_called_at` · `mapper.py:512` · migration `0002`). 다만 이번 배포 할 일에 「worker」가 들어 있다(브리프 §3 C · `_RESUME.md:26`). 배포 전 prod worker 가 멈춰 있었다면 첫 회차가 오늘 WAITING 인 KOS 호출을 한꺼번에 「새로 생김」으로 본다. ⑦의 다른 거름(오늘 · WAITING · 수락 · 진행 · 완료 아님 · 판 카드)이 대부분 막지만, 오늘 남아 있는 WAITING(예: DAY 호출 취소 뒤 KOS 에 남은 「호출」 · 규칙 38)은 그때 알림이 몰릴 수 있다.
- 고칠 방향: ④ 문장에 「prod 동기화가 배포 직전까지 돌고 있었을 때」 조건을 붙이고, 아니면 OQ-102 후보(호출 시각이 오래된 것 거르기)를 배포 메모로 가리킨다.

### W8 [낮음] 설정값 「비운 칸은 꺼짐」이 bool 환경 변수에서는 그대로 되지 않는다
- 위치: `spec-006-reservation-board.md:556`
- 근거: `common/config.py:80` `SettingsConfigDict(extra="ignore", frozen=True, hide_input_in_errors=True)` 에 `env_ignore_empty` 가 없다. bool 칸에 `X=`(빈 값)를 주면 pydantic-settings 가 시작할 때 검증 오류를 낸다. 기존 fail-closed 관례(`deploy/config/dev.env:20` · `prod.env:21` · `local.env.example:58-81`)는 모두 **문자열** 칸(`""` = 꺼짐)이라 bool 과 다르다. 「적지 않음 = 꺼짐(코드 기본 `False`)」은 맞다.
- 고칠 방향: 「적지 않음 = 꺼짐 · 빈 값은 쓰지 않는다」로 적거나, 「빈 값도 꺼짐으로 읽는다(구현)」를 한 줄 더한다.

### W9 [낮음] 규칙 40 ⑨ 「[재호출](처음 호출 대상 = ② 대상)」은 사슬 뿌리가 KOS 호출일 때만 맞다
- 위치: `spec-002-procedure-board.md:1278`
- 근거: DAY [재호출] 대상은 **사슬 맨 처음 호출**의 대상이다(`policies/board_rules.py:190-195` `recall_target` → `chain_root`). ④가 DAY 호출에 `reassigned_from_call_id` 를 이어 KOS 재호출을 붙이면, 뒤이어 누르는 DAY [재호출]은 KOS 가 부른 대상(②)이 아니라 처음 DAY 호출 대상으로 간다.
- 고칠 방향: 「처음 호출 대상 = 사슬 맨 처음 호출의 대상(규칙 6 그대로 — KOS 가 이어 받은 호출이라도)」으로 고치거나, 사슬을 잇지 않는 쪽으로 ④를 정한다.

## 검수 항목별 결과

### 1. 브리프 §3 반영 · 사용자 결정 준수

| 항목 | 들어간 곳 | 결과 |
|---|---|---|
| A1 언제 · 메아리 아님 · 기존 경로 그대로 | 005 `:233`(「언제」 ①②) · `:251` · 002 `:1270` ① | 맞음 |
| A2 받는 사람 · 전체 호출 OQ | 005 `:252` · OQ-N21 `:499` · 002 `:1271` ② · OQ-99 `:1488` | 반영. 다만 2명 이상 = 전체 → **W5** |
| A3 묶음 · 근거 | 005 `:253` · 002 `:1272` ③ | 반영. 근거가 미확인 → **W4** |
| A4 재호출 | 005 `:254` · 002 `:1273` ④ | 맞음(W9 참고) |
| A5 수락 · 닫힘 · 호출 취소 해당 없음 | 005 `:255` · 002 `:1274` ⑤ · 상태도 `:606` | 맞음(코드 사실로 「닫지 않음」). 경쟁 → **W1** |
| A6 메아리 · 경쟁 | 005 `:256` · 002 `:1275` ⑥ (가) ~ (라) · `:1103` | 반영. (라) 사실 오류 → **W6** |
| A7 늦은 관측 · OQ | 005 `:257` · 002 `:1276` ⑦ · OQ-102 · 103 · 105 | 맞음(W7 참고) |
| A8 호출한 사람 · migration 없음 | 005 `:258` · 002 `:1277` ⑧ | 맞음 — `called_by_staff_id` NOT NULL(`models/task.py:232`) · `_system_staff`(`board_transactions.py:349-359`) · 시스템 계정은 `_is_doctor` 에서 빠짐(`notifications.py:225-232`) · 호출자는 화면에 나오지 않음(`queries/board.py:372` DTO 에만) |
| A9 웹 OS 알림 · 푸시 · 목록 그대로 | 005 `:259` · `:330` | 맞음 |
| User Scenario 한 줄 | 005 S-7 `:210-214` | 맞음 |
| B1 프론트만 | 006 `:555` · 007 `:39` | 맞음 |
| B2 대상 · 그대로 | 006 `:554` · `:555` | 맞음 — 판 · 차트 모달이 `/reservations` · `/customers` 를 부르지 않는 것 확인(`static/day.js` 의 해당 경로는 예약 화면 코드뿐 · 판 템플릿에 없음) |
| B3 설정값 하나 · 환경 이름 분기 없음 | 006 `:556` · `:557` | 맞음(W8 참고) |
| B4 새 글자 없음 · OQ | 006 `:559` · OQ-R41 `:808` | 맞음 |
| C 운영 메모 · deployment 가리키기 | 005 `:260` · 006 `:561` | 맞음 — `40-architecture/deployment.md:83` 「브랜치 → 배포 흐름」이 있다 · 백필 나중 · 0.1.0 깨짐 감수 |
| 금지: 새 종류 · 글자 · 스위치 · 환경 분기 · 문구 · 전체 호출 확정 | 전반 | 어긴 곳 없음(`kind = doctor_call` · `call_body` 그대로 · `APP_ENV` 분기 없음 · OQ-N21/99 열림) |
| 30-work WP 안 씀 · log 한 줄씩 · 20-spec.md | `log.md:17-18` · `20-spec.md:35-36` | 맞음 |

### 2. planner 「브리프와 다른 곳」 7건 — 코드 사실 대조

| # | 주장 | 판정 | 근거 |
|---|---|---|---|
| ① | A5 수락 = `doctor_call_accept` · 호출 안 닫음 | **맞음**(브리프 「호출 닫힘」보다 코드가 맞다) | `services/board_calls.py:232-288` `accept` 는 `DoctorCallAccept` 만 넣고 `closed_at` 을 쓰지 않는다. 닫힌 호출은 유효 호출에서 빠진다(`policies/board_rules.py:49-58`) → 닫으면 `task_state` 가 `ready_wait`(준비중)로 돌아간다(`:106-114`) |
| ② | 지정 2명 이상 = 전체(target 1칸) | **사실은 맞음 · 결정과 다름** | `models/task.py:231` `target_staff_id` 1칸 · `notifications.py:324-327` 지정은 그 1명만 → **W5** |
| ③ | 메아리 = op 시간 창 + 허용 오차 30초 | **대체로 맞음** | op 칸 `created_at` · `updated_at` · `status` · `path` · `body` 있음(`models/task.py:303-326` · Timestamps) · 전이마다 `updated_at` 갱신(`outbox_persistence.py:238`) · DAY 는 호출 때 `doctor_called_at` 을 쓰지 않아 값 비교로는 못 가림(`board_calls.py:130-136`). (라)만 틀림 → **W6** · ⑤ 미적용 → **W1** |
| ④ | 배포 직후 첫 동기화가 안 걸림 | **맞음(조건부)** | 동기화가 매 회차 같은 값을 쓴다(`emr/sync_tasks.py:330`) · prod `a6aa4ba5` 도 같은 칸 동기화(`emr/sync.py:1530`) → **W7** |
| ⑤ | KOS 호출 줄이 DAY 판에도 「호출」 · 호출 취소 뒤 되살아나지 않음 | **맞음** | 판 줄 상태는 `doctor_call` 로만 계산(`board_rules.py:106-114`) · ①이 「바뀐 값만」이라 취소 뒤 같은 시각은 다시 안 걸림 · 호출 취소는 `doctor_call_task.deleted_at`(`board_calls.py:316-325`) |
| ⑥ | 고객 화면 스펙 부재 → SPEC-006 정본 | **맞음** | `products/day/20-spec/` 에 `/customers` 화면 계약 없음 · 코드 `routers/customers.py`(`/customers` · `/customers/{id}/chart[...]`) · OQ-R40 |
| ⑦ | `deploy/config/<env>.env` · `DAY_WEB_RESERVATION_CUSTOMER_ENABLED` · 메뉴 숨김 + 303 /board · HX-Redirect · SSE | **맞음** | 비밀이 아닌 값은 Git env, Key Vault 는 뒤에서 덮음(`deploy/compose.yaml:9`) · prod.env 머리 「PR 로 바꾼다」 · 메뉴 `day/menu.py` `RAIL` · `TABS` · `HREFS` · 303/HX-Redirect 도우미가 이미 있음(`day/web.py:278-285` — HTMX 는 204 + `HX-Redirect`) · 로그인 착지 `/board`(`routers/login.py:77`) · 환경 분기 선례 `routers/kit.py:26`(쓰지 않음). bool 빈 값 → **W8** |

### 3. 한 가지로 짤 수 있나

- 묶음 기준: 적혀 있음(같은 방문 · 회차 · 시각 · 대상). 「같은 시각」 근거 → W4
- 메아리 (가) ~ (라): 적혀 있음. (라) → W6 · ⑤ 경쟁 → W1
- 늦은 관측 거름: 적혀 있음(⑦ 다섯 조건)
- 재호출 사슬: 적혀 있음(④ 「받을 시술 전부와 같으면 사슬 · 아니면 사슬 없이」 — `call` · `recall` 와 대응). ⑨ 대상 → W9
- 동시 실행 · 두 번 만들기 방지: **적혀 있지 않음** → W3 · 거는 경로 → W2

### 4. 알림 중복(KOS 호출 1건 → 계정당 알림 1 · 푸시 1)

- 호출 하나 안에서는 보장된다: `ensure_call_rows` 가 `doctor_call` 행 잠금(`with_for_update`) 안에서 (호출, 계정)의 기존 행을 보고 쓴다(`notifications.py:332-407`). 푸시는 호출 단위 Redis 표지와 행마다 `push_log` 로 한 번만 간다(`:551-555` · `:487-492`). SPEC-005 「중복」 줄(`:239`)과 맞다.
- 「KOS 호출 1건 = `doctor_call` 1개」가 깨지면 계정당 N번이 된다. 깨지는 자리는 W4(시각 어긋남) · W6(failed 메아리) · W2/W3(경로 · 비교 시점)이다.

### 5. 정식 앱 0.1.0 이 받는 모양

바뀌지 않는다. 알림 행 `kind = doctor_call` · `title` · `body`(`call_body` — `notifications.py:96-102`) · 푸시 payload `{aps, kind:"doctor_call", environment, hospitalId, visitId, callId}`(`:508-516`) 모두 그대로다. 새 칸은 `event_log` payload `source: "kos"`(서버 내부)뿐이다. 2명 이상 지정이 「전체 호출」 본문이 되는 것은 W5.

### 6. OQ 기본값 · 착수 막음 · 추측 확정

- OQ-N21 ~ N24 · OQ-99 ~ 105 · OQ-R40 · R41 모두 기본값이 있고 착수를 막지 않는다.
- 추측으로 사실을 확정한 곳: ③ 「한 요청이 같은 시각」(W4) · (라) 「failed = KOS 안 불림」(W6). 「전체 호출」 표현은 열린 채로 둬서 맞다.
- 참고: ②의 기본값대로면 KOS 가 「전체 호출」 때 원장 전원(2명 이상)을 돌려줘도 이미 전체 호출이 된다. OQ-99 의 「원장 전원이 오면 고친다」는 OQ-100 을 바꾸지 않는 한 고칠 게 없다. OQ-100 을 바꾸는 경우에만 둘이 얽힌다.

### 7. lint

`python3 scripts/lint-pipeline.py --strict` → 0 error · 263 warning · exit 0 · `products/day/` 해당 줄 0. 나머지 WARN 은 다른 제품이라 무관하다.

## 직원이 실물에서 만날 자리

- KOS 에서 2명을 지정해 불렀는데 원장 전원 폰이 울리고 본문이 「전체 호출」로 뜬다(W5 · 기본값 그대로일 때).
- DAY 에서 의사 호출을 누른 직후, KOS 에 예전 집도의가 남아 있던 작업이 아무도 안 눌렀는데 「{원장} 수락 완료」가 된다(W1).
- KOS 에서 한 고객의 시술 여러 개를 한 번에 불렀는데 원장 폰에 같은 알림이 여러 개 온다 — KOS 시각이 작업마다 다를 때(W4).
- 점유 이동 직후 KOS 에서 건 호출이 알림 없이 판에만 「준비중」으로 남는다 — 규칙 40 을 10초 경로에만 걸었을 때(W2).
- prod 배포 직후 worker 가 처음 돌 때 오늘 남아 있던 KOS 「호출」 작업 알림이 한꺼번에 울린다 — 배포 전 prod 동기화가 멈춰 있었을 때(W7).
- 호출 「늦음」 시각은 KOS 호출 시각이 아니라 동기화가 호출을 만든 시각(최대 10초 뒤 · 동기화가 멈췄다 돌면 더 뒤)부터 센다(`board_rules.py:166-171` `call_late_at` = `call.created_at` + 호출 분). 스펙은 이 차이를 말하지 않는다(정보).
- prod 웹에서 예약 · 고객 아이콘 · 「예약 현황」 탭이 사라진다. 북마크한 `/reservations` 는 안내 없이 시술 현황으로 간다(의도 · OQ-R41).

## 참고(기존 부채)

- SPEC-002 개정 ㉘ 본문 안 목록 번호 「㉚ C36 …」(`origin/main` 판에도 있음)이 새 「개정 ㉚」과 같은 글자다. 개정 번호 충돌은 아니지만 grep 할 때 헷갈린다.
- 웹 OS 알림은 `GET /api/notifications` 목록을 다시 읽는 방식(㉠)이라, 이번 변경으로 호출 수가 늘어도 서버 변경은 없다(SPEC-005 `:333`).
