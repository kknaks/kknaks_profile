# day-kos-call-notify BE 1루프 결과 보고 (#283)

## 상태: done (커밋 · push · PR 없음 — 워크트리 변경만)

- 워크트리 `CENTURION_DAY/day-kos-call-notify` · base `origin/dev` `55e60aa4`
- 계약: DAY-SPEC-002 개정 ㉚ 규칙 40 ① ~ ⑨ · DAY-SPEC-005 §3 「KOS 에서 건 호출」

## 수행 — 파일

| 파일 | 내용 |
|---|---|
| `backend/day/dtos/sync_state.py` | `PreviousTaskData.doctor_called_at`(기본 None) · 새 `TaskCallData`(이전 호출 시각 · 이전 상태 · KOS 값 · `call_changed` ① · `became_ready` ⑤ (ii)) |
| `backend/day/emr/sync_tasks.py` | `_apply_tasks` — 방문 잠금 뒤 같은 transaction 의 existing 읽기에 `doctor_called_at` 추가 · 후보(호출 시각 바뀜 · READY 전이)를 그 transaction 에 모음 · `take_task_calls`(지금 transaction 것만 꺼냄 — 앞/rollback transaction 것은 버림) |
| `backend/day/policies/kos_calls.py` (새) | 순수 규칙 — 허용 오차 `TOLERANCE = 30초`(상수 · OQ-101) · ② `target_of` · ③ `bundle`(가장 이른 새 시각 기준) · ⑥ `is_echo`(pending/sent · confirmed/그 밖 failed = `updated_at`+오차 · BLOCKED/토큰 없음 failed = 창 아님) · ⑤ (i) `call_op_in_flight` |
| `backend/day/services/kos_calls.py` (새) | `apply`(같은 transaction 에서 판정 · 호출 · 수락 생성) · `after_commit`(= 호출마다 `notifications.after_call`). ⑦ 거름 · ④ 사슬/닫기 · ⑤ 수락 행 · ⑧ 시스템 계정 · `event_log` `call.create`(actor 비움) / `call.accept`(actor = 원장) payload `source: "kos"` · 쓰기 큐 0행 |
| `backend/day/services/notifications.py` | `_recipients` — `kind = one` 이고 호출자가 시스템 계정이면 그 호출 작업들의 `called_doctor` 중 원장 전부 · `kind = all` · DAY 지정 호출은 그대로 |
| `backend/day/services/emr_sync.py` | (ㄱ) `run_schedules` · (ㄴ) `_apply_detail` 두 커밋 — 판정 + 커밋 뒤 `after_commit` |
| `backend/day/services/ext_sync.py` | 코디 답(기본값) — `_load_date` · `_save_scoped_schedules` 커밋에도 같은 판정 + 커밋 뒤 알림 |
| 시험 4개(새) | `tests/day/board/test_kos_call_rules.py`(순수 12) · `tests/day/notifications/kos_call_support.py` · `test_kos_calls.py`(infra 11) · `test_kos_calls_flow.py`(infra 14) |

**설계 메모** — `emr/sync*.py`(Taut `participant`)는 services · queries · policies 를 import 할 수 없다. 그래서 `_apply_tasks` 는 잠금 뒤 이전 값 · KOS 값 관측만 모으고, 판정 · 생성은 그 경로를 커밋하는 서비스가 **같은 transaction 안에서** `kos_calls.apply` 로 한다(판 세계 `load_world` 는 후보가 있을 때만 1회). 관측은 `SyncCounts` 가 아니라 세션 transaction 에 싣는다 — `emr/sync_references.py` 와 `apply_visit_tasks` 본문은 차트 정형 검증(`verify-day-chart` source-map)이 AST 해시로 고정해 손대면 `test_verification_formal` 이 깨진다(한 번 깨뜨려 보고 되돌림). migration · 새 kind · 새 글자 · 새 설정 · 환경 분기 없음.

## `_apply_tasks` 를 타는 모든 커밋 경로

| 경로 | 반영 | 커밋 | 규칙 40 판정 · 알림 |
|---|---|---|---|
| (ㄱ) 10초 일정 조회 `emr_sync.run_schedules` | `services/emr_sync.py:263` → `emr/sync_schedules.py:421` | `services/emr_sync.py:297` | 판정 `:273` · 알림 `:298` |
| (ㄴ) 예약 상세 연쇄 ① `_chain_room_assign` | `services/emr_sync.py:463` → `_apply_detail` `:522` → `emr/sync_tasks.py:243` | `services/emr_sync.py:467` (`taken_by_poll` 이면 rollback · 알림 없음) | 판정 `:532` · 알림 `:468` |
| (ㄴ) 예약 상세 연쇄 ② 마지막 확인 | `services/emr_sync.py:499` | `services/emr_sync.py:503` | 판정 `:532` · 알림 `:504` |
| 외부 연동 사본 `ext_sync._save_scoped_schedules`(← `refresh_history :229` · `refresh_visit :270` · `save_visit_snapshot :415` ← `reservation_confirm.py:147` 예약 상세 쓰기 확인) | `services/ext_sync.py:301` | `services/ext_sync.py:323` | 판정 `:315` · 알림 `:324` — **오늘 가능** |
| 외부 연동 날짜 `ext_sync._load_date`(← `refresh_date :56`) | `services/ext_sync.py:97` | `services/ext_sync.py:115` | 판정 `:107` · 알림 `:116` — 오늘은 안 탐(`ext_refresh.py:65` `needs_date_refresh` = 오늘 아님) · 붙임(무해) |
| 다른 날짜 최신화 `emr_date_sync.run_reservation_date` | `services/emr_date_sync.py:204` | `:276` | **안 붙임** — 오늘이면 `skipped_today`(`emr_date_sync.py:172` `is_today`) |
| 백필 `emr_backfill` | `services/emr_backfill.py:303` | `:318` | **안 붙임** — `--to` 가 오늘 이상이면 `BackfillInputError`(`emr_backfill.py:161`) |

안 붙인 두 경로의 후보는 그 transaction 이 끝나면 버려진다(`take_task_calls` 가 transaction 을 확인). 그 경로가 저장한 값은 오늘 것이 아니라 ⑦ 로도 만들어지지 않는다.

## 검증 — 명령과 수치

- `./scripts/test.sh -q backend/tests/day/notifications/test_kos_calls.py backend/tests/day/notifications/test_kos_calls_flow.py` (격리 PG · Redis) → **25 passed**
- `./scripts/test.sh --pure -q backend/tests/day/board/test_kos_call_rules.py backend/tests/devtools/test_verification_formal.py` → **26 passed**
- 변이 확인(되돌림): 메아리 판정 · 「오늘」 거름 · 수락 보류를 끄면 해당 시험 3개가 실패함을 확인
- `./scripts/check.sh --static` → ruff · format · strict mypy(654 파일) · Taut check(진단 0) · Taut audit 통과. **frontend 단계만 실패** — 이 워크트리에 npm 패키지 없음(`@tailwindcss/postcss` 없음). 프론트 파일은 건드리지 않음 · 설치는 하지 않음
- 전체 회귀 `./scripts/test.sh -q`(격리 PG · Redis · 최종 코드) → **2902 passed · 0 failed**(337초) — 동기화 · 판 호출 · 알림 · 정형 검증 · 아키텍처 포함

## 계약 대조 — 규칙 40

| 항목 | 결과 | 시험 |
|---|---|---|
| 머리 — 판정 자리 `_apply_tasks` · 두 경로 같은 transaction · 커밋 뒤 `after_call` · 알림 실패해도 동기화 성공 | 같음(관측은 `_apply_tasks`, 판정은 같은 transaction 의 커밋 서비스) | 10초 조회 알림 · 예약 상세 먼저 → 알림 1번 · 외부 연동 먼저 → 알림 1번 |
| ① 바뀐 값만 · 잠금 뒤 이전 값 | 같음 | 같은 변화 두 회차 = 호출 1 · 두 회차 겹침 = 1 · rollback 후보 버림 |
| ② 1명 지정 · 0명 전체 · 2명+ 그 원장들(대표 = 첫 원장) · `kind = one` 규칙 40 호출만 called_doctor 계산 | 같음 | 지정 1명 · 2명 · 전체(빈 · 시스템만) · DAY 지정 그대로 |
| ③ 같은 방문 · 회차 · kind + 원장 집합 · 가장 이른 시각과 30초 | 같음 | 묶음 1개 · 31초 · 집합 다름 = 따로 |
| ④ 받을 시술 전부 = 재호출 사슬 · 아니면 사슬 없음 · 빈 앞 호출 닫기 · 대상은 KOS 대상 | 같음(같은 회차 여러 묶음이 한 앞 호출을 나눠 옮겨도 닫힘 — 옮긴 줄을 합쳐 계산) | 재호출 사슬 · 일부 옮김 |
| ⑤ 열린 미수락 호출 + `doctors[]` 원장 + 전이(이전 ≠ READY → READY) + op pending/sent 아님 → `doctor_call_accept`(첫 원장 · 알게 된 시각) · 호출 안 닫음 · `call.accept` actor = 원장 · DAY 호출에도 | 같음 | KOS 수락 · op 진행 중 보류 · 옛 READY 거름 |
| ⑥ 메아리 창 (가) ~ (라) | 같음(`never_sent` = `last_error` 가 BLOCKED · 토큰 없음) | pending · sent · confirmed · STALE · 창 지난 뒤 · BLOCKED · 토큰 없음 |
| ⑦ 수락/진행/완료 · KOS ≠ WAITING · 오늘 아님 · 판 카드 아님 · 시스템 계정 없음(로그만) | 같음 | 각 거름 시험 |
| ⑧ `called_by_staff_id` = 시스템 계정 · `call.create` payload + `source: "kos"` · KOS 쓰기 0 | 같음 | 지정 1명 시험(payload 전체 비교) |
| ⑨ 판 · 앱 동일 · [재호출] = 사슬 맨 처음 대상 | 같음 | 재호출 사슬 시험(DAY 재호출 → 가원장) |
| SPEC-005 — kind `doctor_call` · 글자 · payload 그대로 · 계정당 1행 · 푸시 호출당 1번 | 같음 | `notified` 가 계정 중복을 막음 · `call_push_kicks` |

## 이슈 · 코디가 확인할 것

1. **정형 검증 고정 파일** — `emr/sync_references.py` · `apply_visit_tasks` 를 고치면 `test_verification_formal` 이 깨진다. 그래서 `SyncCounts` 에 칸을 더하지 않고 세션 transaction 에 실었다. 스펙 문장(「`_apply_tasks` 에서 판정」)과 위치가 조금 다르다(관측 = `_apply_tasks` · 판정 = 같은 transaction 의 커밋 서비스).
2. **경쟁 시험의 한계** — 「두 회차 겹침 = 호출 1」은 방문 잠금을 빼도 통과한다. 작업 외부 id 연결(`Refs.link` upsert 행 잠금)이 이전 값 읽기보다 먼저라 두 동기화 회차는 이미 차례로 돈다. 판 조작과의 겹침은 같은 `board:{visit}` 잠금(기존)이 막는다 — 이 겹침을 따로 재현한 시험은 없다.
3. **DAY 호출 `created_at`** — 규칙 40 호출의 `created_at` 은 DB 기본값(만든 시각)이다. KOS `doctorCallDateTime` 으로 바꾸지 않았다(스펙에 없음) → 「늦음」은 DAY 가 알게 된 때부터 센다(최대 10초 늦음).
4. 실물 e2e(A10 · OQ-99 · OQ-106)는 이번 단계 아님.
