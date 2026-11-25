# day-kos-call-notify e2e-1 — 로컬 스택 + KOS DEMO 실물 (#283 완료 조건)

- 스택: `http://127.0.0.1:11140`(코디가 띄움 · 시작/멈춤/코드 수정 없음) · 로컬 DB `day_dev` 는 **읽기 전용 트랜잭션**(`default_transaction_read_only=on`)으로 SELECT 만 · 로그 `.run/worker.log`
- KOS 호출은 테스트 계정 직원 토큰으로 직접 보냈다. 코드는 `KosStaffAuthenticator` · `KosStaffWriter`(`emr/kos/staff_client.py`)와 같은 브라우저 헤더 · UA 관례를 따른다. 비밀값은 출력하지 않았다.
- 시각은 모두 UTC(2026-11-25)

## 결과 표

| # | 시험 | 결과 | 수치 | 비고 |
|---|---|---|---|---|
| 1 | 지정 1명 | **O** | KOS 호출 04:21:07.304Z → `doctor_call` 664a9b85 생성 04:21:13.2(6초) · kind `one` · target 원장 A · called_by 시스템 · `event_log` `call.create` actor 비움 · payload `source: kos` · `kosCalledAt` = KOS 시각 그대로 · `day.notifications.call_push` 실행 1 | 알림 행 0 — **환경상 미검증**(아래 「환경」) |
| 2 | 전체 호출 | **O** | `doctorIds` 없이 → KOS `calledDoctors: []`(빈 배열) · DAY `doctor_call` 8b52f3ba kind `all` · target 없음 | 받는 사람 = 원장 목록 10명(시스템 계정 제외) 중 계정 있는 원장 0명 → 알림 행 0. **OQ-99 닫음** |
| 3 | 여러 작업 한 번에 | **O** | `sequences [2,3]` 한 요청 → 두 작업 `doctorCallDateTime` = `04:22:14.78Z` **밀리초까지 같음** → `doctor_call` c38a7672 1개(seq 2,3) · push 1 | **OQ-106 닫음** |
| 4 | 재호출 | **O** | 1번 작업(seq 2)을 KOS 에서 다시 호출(원장 B) 04:22:38.664Z → 새 `doctor_call` 2c5038f9(사슬 `fromCallId` = 664a9b85) · 앞 호출 `closed_at` 04:22:43.3 · `closedCallIds` 에 앞 호출 · push 1 더 | 알림 행은 환경상 미검증 |
| 5 | DAY 에서 호출(메아리) | **O** | DAY 웹 세션으로 `POST /api/visits/be30279d…/calls`(seq 4 · 지정 원장 C) → `doctor_call` 8e026c08 1개(called_by 테스트 계정) · 그 뒤 동기화 회차들이 **새 호출 0** · push 1(DAY 쪽 한 번) | 쓰기 큐 3개(room · assignees · call) 모두 `confirmed` |
| 6 | KOS 수락 | **O** | `change-tasks-doctors`(seq 3 · 원장 A) → KOS `READY` · `doctors [원장 A]` → DAY `doctor_call_accept` 1행(call 8b52f3ba · 원장 A · 04:23:53.2) · `call.accept` actor = 원장 A · payload `source: kos` · 호출 `closed_at` 비움 · 새 push 없음(5 호출 = 5 push) | 알림 추가 없음 |
| 7 | 배포 직후 모양 | **설명** | 03:48Z 에 이미 waiting 이던 6작업(방문 2162d1b1 seq 2,4,5,6 · e7296b43 seq 2,3) → `doctor_call` 0 | 근거 아래 |

### 7 — 왜 0인가 (코드 근거)

- 이 스택의 **첫 일정 회차(04:15:54.704)는 기준 정보 전**에 돌았다.
  - 로그 `emr schedules … 'needs_master': True` · `skipped: {visit_occupied_resource: 13, visit_task_staff: 41}`
  - 방 · 직원 `external_ref` 가 처음 생긴 때 = 04:15:55.017. 기준 정보 회차가 첫 일정 회차 **뒤**다.
- 그래서 그 회차에는 방문의 방이 비어 있었다(방 참조 없음). → **⑦ 「판 카드 아님」** 거름: `services/kos_calls.py` `_card_task` → `policies/board_rules.py:67-68` `is_card`(`room_id is not None` 필요).
- 다음 회차부터는 방이 생겨 카드가 됐다. 그러나 `doctor_called_at` 이 이미 저장된 값과 같아 **① 「바뀌지 않음」**이다(`dtos/sync_state.py:43-51` `call_changed`). → 그 뒤로도 0이다.
- 확인 방법: 지금 DB 로 같은 6작업을 「처음 보는 작업」으로 넣어 판정만 돌렸다(읽기 전용 · 재현 스크립트). → 카드 · `ready_wait` · 오늘 · 만들 수 있음. 지금 값으로는 걸리는 거름이 없다 → 0의 원인은 첫 회차의 방 없음 + 그 뒤 ① 이다.
- **prod 첫 배포 근거로 쓸 때는 이 이유가 아니다**. prod 는 기준 정보와 `doctor_called_at` 이 이미 저장돼 있다. 그래서 배포 뒤 첫 회차가 오늘 남은 KOS 「호출」을 받아도 **① 「바뀌지 않음」**(`sync_state.py:43-51`) 하나로 0이다. 「옛 사본」 거름 `kos_calls.py` `_made_kos_times` 는 규칙 40 호출이 없으니 해당 없다. 같은 값 그대로인 경우는 단위 · 통합 시험 「값이 그대로면 아무것도 안 함」이 덮는다.
- 부수 관찰(OQ-103 과 같은 뜻 · 버그 아님): 동기화가 **처음 켜지는 병원**에서 기준 정보 전 회차에 이미 KOS 「호출」인 작업은 앞으로도 DAY 호출이 되지 않는다. prod 처럼 이미 돌고 있는 병원은 해당 없다.

## OQ 실측

| OQ | 실측 | 결론 |
|---|---|---|
| **OQ-99** 전체 호출 `calledDoctors` | 요청에 `doctorIds` 없음 → 일정 상세 `calledDoctors: []` | 스펙 기본값 「비어 있으면 전체 호출」 그대로 맞다. 고칠 것 없음 |
| **OQ-106** 한 요청 여러 작업 시각 | `sequences [2,3]` → 두 작업 `doctorCallDateTime` 둘 다 `2026-11-25T04:22:14.78Z`(같음) | 같은 시각. 묶음 허용 오차 30초가 없어도 한 호출이 된다(오차는 안전 여유) |
| **OQ-101 · I6** KOS ↔ DAY 시각 차 | DAY 호출(시험 5): op `created_at` 04:23:08.633 · KOS `doctorCallDateTime` 04:23:08.938 · op `updated_at`(confirmed) 04:23:13.161 → **KOS − created = +0.31초 · updated − KOS = +4.22초**. KOS 직접 호출: 요청 끝난 시각 − KOS 시각 = 0.02 ~ 0.03초 | 30초 창 안에 넉넉히 든다. 메아리 판정이 맞게 일한다(시험 5 = 0건) |

## 환경 · 미검증

- 알림 행 1행(시험 1 · 4): **환경상 미검증**.
  - 이 DEMO 병원의 원장 직원 10명 모두 DAY 계정이 없다(`staff.account_id` 없음). 받는 사람은 「계정 있는 원장」이라 0명이다.
  - 테스트 계정은 간호(테스트 계정)다.
  - 코디가 준 두 번째 계정(`~/.config/day/dev-login.local.json`)은 로컬 로그인이 `401 invalid_credentials`(KOS 거부)였다. 잠김을 피하려고 다시 시도하지 않았다.
  - 그래서 `push_log` 도 0행이다(받는 사람이 없음).
  - 대신 호출마다 커밋 뒤 `after_call` → `day.notifications.call_push` 태스크가 **호출당 정확히 1번** 돈 것을 worker 로그로 확인했다(5 호출 = 5 실행 · 수락은 0).
  - 받는 사람 계산 · 계정당 1행은 시험(`test_kos_calls*.py`)이 덮는다.
- 웹 OS 알림 · iPad 시뮬레이터: 이번 브리프 범위 밖이라 보지 않았다.

## KOS 실물에서 알게 된 것 (시험 도구 관점 · DAY 코드 영향 없음)

- `call-tasks-doctors` 는 작업에 방이 없으면 `400 InvalidRequestException {roomId: NotFound}` 다. DAY 의 호출 쓰기 계획이 「방 → 담당자 → 호출」 순서인 이유와 맞는다(`services/board_calls.py` `_call_intents`).
- `change-tasks-assignees` 만 보내도 KOS 작업 상태가 `NOT_STARTED → READY` 로 바뀌었다(데모 관찰).

## 남긴 KOS 상태 (되돌리는 명령 없음 — KOS 에 호출 취소 · 담당 해제 명령을 쓰지 않았다)

| 일정(방문) | seq | KOS 상태 | 남은 값 |
|---|---|---|---|
| `73ccb7bc…`(DAY 747fc58c · A-룸6) | 2 | WAITING | 호출 04:22:38.664Z · 호출 원장 원장 B · 담당 시스템 · 방 A-룸6 |
| 〃 | 3 | READY | 호출 04:21:49.713Z(전체) · 집도의 원장 A · 담당 시스템 · 방 A-룸6 |
| `511ec5c7…`(DAY be30279d · A-룸7) | 2 · 3 | WAITING | 호출 04:22:14.78Z · 호출 원장 원장 D · 담당 시스템 · 방 A-룸7 |
| 〃 | 4 | WAITING | DAY 호출(전체 — KOS 요청에 원장 없음) 04:23:08.938Z · 담당 시스템 · 방 A-룸7 |

- 다른 사람이 쓰던 작업(이미 waiting · 진행 · 완료)은 건드리지 않았다. 처음에 호출이 없던 `NOT_STARTED` 작업만 썼다.
- DAY 로컬 쪽: 위 호출 5개 · 수락 1개가 남는다(열린 호출 4개). 정리하려면 판에서 「호출 취소」를 하면 된다(DAY 만 · KOS 쓰기 없음).

## KOS 세션 해제

- 테스트 계정: 이번에 만든 sign-in 2개(스크립트 04:19:34 · DAY 로컬 로그인 04:19:40)를 `revoke-active-sign-in` 으로 해제했다. DAY 로컬 세션은 `/logout` 으로 끝냈다. 남은 2개(02:50 · 00:31)는 이번 작업 전부터 있던 것이라 두었다.
- 두 번째 계정: 로그인이 거부돼 KOS 세션이 생기지 않았다 → 해제할 것 없음.
- 스크래치의 토큰 파일은 지웠다.

## 버그

- 없음. 규칙 40 경로(지정 · 전체 · 여러 작업 · 재호출 · 메아리 · KOS 수락)가 실물에서 스펙대로 돌았다.
