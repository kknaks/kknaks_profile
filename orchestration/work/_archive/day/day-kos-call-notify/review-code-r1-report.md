# 리뷰 리포트 — day-kos-call-notify / code r1 (2026-11-25)

- 대상: 워크트리 `CENTURION_DAY/day-kos-call-notify` 미커밋 변경(base `origin/dev` `55e60aa4`) — 수정 5 · 새 파일 6
- 기준: DAY-SPEC-002 개정 ㉚ 규칙 40 ① ~ ⑨ · OQ-99 ~ 107 · DAY-SPEC-005 §3 「KOS 에서 건 호출」 · 구현 보고 `be-impl-r1-report.md` · 문서 검수 r1 ~ r3
- 읽기만 했다. 리포 수정 · 커밋 · push 없음.

## 판정: **WARN**

FAIL 없음. 「같은 KOS 호출 → 호출 1 · 계정당 알림 1 · 푸시 1」은 정상 순서에서 지켜진다. 방문 잠금은 판정과 생성 구간을 실제로 감싼다. 판 조작(호출 · 재호출 · 수락 · 취소)과 겹쳐도 깨지는 순서는 찾지 못했다. 다만 아래 W1(오래된 사본이 늦게 커밋되면 같은 KOS 호출에 알림이 한 번 더 감)과 W2(시스템 계정으로 DAY 에 로그인해 누른 지정 호출의 받는 사람이 바뀜)는 prod 전에 코디가 고칠지 받아들일지 정해야 한다. 둘 다 잘 안 생기는 순서이고, 고치는 비용은 작다.

## 검증 — 명령과 수치

- `./scripts/test.sh -q -p no:cacheprovider` + 새 시험 4개 · `tests/day/notifications/` 전체 · `board/test_board_api_calls.py` · `test_board_rules_calls.py` · `test_board_locks.py` · `test_board_room_chain.py` · `emr/test_sync.py` · `emr/test_emr_sync_service.py` → **151 passed (31.5초)**. 격리 시험 인프라를 썼다. 브리프의 `uv run pytest` 대신 리포 정본 러너를 썼고, 사용자 스택 · 포트 · 공유 DB 는 건드리지 않았다.
- `uv run --frozen ruff check` 바뀐 파일 + 새 파일 11개 → **All checks passed** · `ruff format --check` 새 파일 2개 통과.
- 파일 크기: `notifications.py` 588 · `sync_tasks.py` 535 · `emr_sync.py` 542 · `kos_calls.py` 310. 모두 700줄 이하.

## 1. 규칙 40 대응표

| 규칙 | 코드 | 결과 |
|---|---|---|
| 머리 — 판정 자리 `_apply_tasks` · 같은 tx · 커밋 뒤 `after_call` | 관측 `emr/sync_tasks.py:403-416` → tx 에 담음(`_task_calls` `:66-84`) · 판정 `services/kos_calls.py:282-301` · 알림 `:304-310` | 같음. 관측은 `_apply_tasks` 에서 하고 판정은 같은 tx 를 커밋하는 서비스에서 한다. 정형 검증 AST 고정 때문에 생긴 위치 차이이고, 같은 tx 라 의미는 같다 |
| (ㄱ) 10초 조회 | `services/emr_sync.py:273`(apply) · `:297` commit · `:298` after_commit | 같음. 쓰기 큐 확인 `:288` **전**에 판정하므로 (다)가 지켜진다 |
| (ㄴ) 상세 연쇄 두 커밋 | `emr_sync.py:532`(`_apply_detail` 안) · `:467`/`:468` · `:503`/`:504` · `taken_by_poll` `:465` 는 rollback 이고 알림 없음 | 같음 |
| ext_sync 확장(코디 결정) | `ext_sync.py:107/115/116`(`_load_date`) · `:315/323/324`(`_save_scoped_schedules`) | 같음. 날짜 최신화와 백필은 오늘을 타지 않아 붙이지 않았다는 보고 근거(`emr_date_sync.py:172` · `emr_backfill.py:161`)를 확인했다 |
| ① 새로 생김 · 바뀜 · 잠금 뒤 이전 값 | `dtos/sync_state.py:43-46` · 이전 값 읽기 `sync_tasks.py:296-321`(잠금 `:240` · `sync_schedules.py:329` 뒤) | 같음. 단 W1(값이 **뒤로** 가도 「바뀜」으로 본다) |
| ② 대상 1명 · 0명 · 2명+ / 대표 = 첫 원장 | `policies/kos_calls.py:47-54` · `:37-40` | 같음(I3 대표 차례) |
| ② 받는 사람 — `kind=one` 규칙 40 호출만 `called_doctor` | `services/notifications.py:311-353` | 같음. 판별 = `is_system_account`(OQ-107 ⓒ) → W2 |
| ③ 묶음 — 같은 방문 · kind + 집합 · 가장 이른 시각과 30초 | `services/kos_calls.py:166-184` · `policies/kos_calls.py:81-92` | 같음. 경계 `<=` 30초는 묶이고 31초는 따로(시험 있음) |
| ④ 재호출 사슬 · 옮김 · 빈 앞 호출 닫기 | `services/kos_calls.py:186-193` · `:215-226` | 같음. DAY `call` 의 `_close_moved` 와 같은 `calls_to_close` 를 쓰고, 같은 회차의 여러 묶음도 합산한다 |
| ⑤ 수락 — 전이 · (i) op 진행 중 보류 · 첫 원장 · 호출 안 닫음 · `call.accept` actor = 원장 | `sync_state.py:48-55` · `services/kos_calls.py:247-279` | 같음. KOS 쓰기 없음. DAY 수락의 시술 전 의사차트 쓰기(`board_calls.py:271-287`)는 KOS 값이라 해당 없다 |
| ⑥ 메아리 (가) ~ (라) · `last_error` 판별 | `policies/kos_calls.py:57-73` · `services/kos_calls.py:56` · `:70-97` | 같음. `BLOCKED` 는 pending 에서만(`outbox_persistence.py:291-297`), `NO_TOKEN` 도 pending 에서만(`outbox_rules.py:78-86`) 붙는다 → 보내기 전 판별이 맞다(I2 경계) |
| ⑦ 늦은 관측 | `services/kos_calls.py:148-163` | 같음. `SETTLED` 글자가 `task_state` 반환값(`board_rules.py:108-114`)과 맞는다. 「오늘」은 `queries/board.py:80` 병원 시간대 |
| ⑧ 시스템 계정 · event payload · 쓰기 큐 0 | `services/kos_calls.py:203-235` | 같음. payload 키는 DAY `call.create`(`board_calls.py:146-151`) + `fromCallId?` + `source` |
| ⑨ 판 · 앱 동일 | 새 DTO · 새 칸 없음 · `called_by_staff_id` 를 그리는 화면 · API 없음(`queries/board.py:372` 뿐) | 같음 |

## 2. 하나의 KOS 호출 → 호출 1 · 계정당 알림 1 · 푸시 1

- **방문 잠금 범위**: 두 진입점 모두 잠금(`pg_advisory_xact_lock`, tx 끝까지 유지) → 이전 값 읽기 → 쓰기 → `kos_calls.apply`(세계 · 쓰기 큐 읽기 · 생성) → commit 순서다. 판정과 생성이 잠금 안에 있다. 판 조작은 같은 키(`board_transactions.py:70-73` · `_world :103-108`)를 잡은 **뒤** 세계를 읽는다.
- **판 조작과 겹칠 때**(코드로 따짐):
  - DAY 호출 · 재호출이 먼저 커밋하면 op 이 `pending` 이라 메아리로 걸린다. 동기화가 먼저면 KOS 호출 K 가 생기고, 그 뒤 DAY 호출은 「호출 중 줄 → 새 호출」(규칙 5)이 된다. 두 동작이 실제로 두 번 일어난 것이라 맞다.
  - DAY 수락이 먼저면 줄이 `accepted` 라 ⑤ · ⑦ 를 건너뛴다. 동기화가 먼저면 DAY 수락은 `accept_block` 409 다.
  - DAY 호출 취소가 먼저면 KOS 값이 그대로라 ① 에 걸리지 않는다. 동기화가 먼저면 취소가 K 를 닫는다.
  - 교착: 동기화는 정렬된 여러 키, 조작은 키 하나를 잡는다. `apply` 는 새 잠금을 잡지 않는다.
  - 깨지는 순서는 없다.
- **알림 · 푸시 중복**: 계정당 행 하나는 기존 `ensure_call_rows`(호출 행 `FOR UPDATE` + 있는 행 빼기)가 지키고, 푸시는 행 기준 + `PushLog` 가 지킨다. 새 코드는 호출 하나에 `after_call` 을 정확히 한 번 부른다.
- **시험 판별력**: `test_두_회차가_겹쳐도…`는 보고서 말대로 잠금을 빼도 통과한다. 판 조작과 겹치는 경우를 재현한 시험도 없다. 다만 잠금 자체는 기존 코드(#230 W7)가 깔아 둔 것이고, 이번 변경은 그 안에서 읽기만 더했다. 「잠금 뒤 읽기」가 앞으로 깨지는 것을 막을 시험은 없다 → W4.
- **잠금으로 못 막는 순서** → W1.

## 3. 커밋 뒤 `after_call`

- 보고서 표의 경로 7개를 모두 확인했다. 각 경로는 commit 다음 줄에서 `after_commit` 을 정확히 한 번 부른다. 상세 연쇄 확인 루프는 회차마다 한 번이다. commit 이 예외면 `after_commit` 까지 가지 않는다. `taken_by_poll` 은 `async with` 안의 return 이라 rollback 되고 `[]` 를 돌려준다. rollback 된 후보는 `take_task_calls` 가 tx 정체성을 비교해 버린다(시험 있음).
- `after_call` 은 `Exception` 을 삼키고 3초 상한이 있다(`notifications.py:447-458`) → 알림 실패가 동기화 회차를 죽이지 않는다.
- **`apply` 자체의 예외는 회차를 죽인다**(I1). 예외가 날 자리는 찾지 못했다 — `doctor_call_task` PK 충돌은 같은 tx 의 같은 작업 중복이 앞 단계 upsert 에서 이미 막힌다.

## 4. 경계값

- 메아리: `called_at < created_at − 30s` 이면 창 밖이다(`<`, 정확히 −30초는 창 안). confirmed · 그 밖 failed 는 `called_at <= updated_at + 30s`. 비교 기준이 관측 시각이 아니라 KOS 호출 시각이다. 그래서 동기화가 몇 분 늦게 돌아도 메아리 판정이 흔들리지 않는다. 시험 있음.
- 수락: `before_status is None` 이면(처음 받는 작업) 전이가 아니다. 쓰기 큐가 진행 중이면 `status` 가 held 라 `written_status` 가 이전 값이다. 그래서 전이는 op 이 끝난 회차에 한 번 생긴다. 스펙 근거와 같다.
- 늦은 관측: `day_start <= called_at < day_end`.
- 묶음: 가장 이른 시각을 기준으로 잰다(0 · 20 · 40초면 0 · 20 / 40). 시험 있음.

## 5. `_recipients` 변경

- 시스템 계정이 아닌 직원이 누른 호출: `kind=one` 은 기존 `Staff.id == target` 그대로, `kind=all` 은 분기 밖이라 그대로다 → **바뀌지 않는다**(시험 `test_DAY_에서_누른_지정_호출은_지금처럼`).
- 시스템 계정 직원이 DAY 에서 누른 지정 호출 → W2.

## 6. 0.1.0 호환

- 알림 행: `kind=doctor_call` · `TITLE` · `call_body(kind)` 그대로. 푸시 payload · 카테고리 그대로(`call_deliveries` 무변경). 판 · 앱 DTO 와 스키마도 무변경이다. 바뀐 것은 내부 `event_log` payload 의 `source` 키 하나라 0.1.0 이 받는 모양은 **그대로다**.

## 7. 성능

- 후보가 없는 회차: 추가 쿼리는 **0**이다. `doctor_called_at` 한 칸을 같은 SELECT 에 더했을 뿐이다.
- 후보가 있는 회차(호출 시각이 바뀌었거나 READY 전이 — 메아리 포함): `load_world` 1회(병원 판 전체 · 기존 판 조작과 같은 쿼리 묶음) + 쓰기 큐 1 + 시스템 계정 1. 이어서 호출마다 insert 몇 개와 `after_call`(새 세션 · 3초 상한 · 순차)을 탄다. `_recipients` 는 지정 호출마다 `_by_system` 1 쿼리가 늘어난다. 작업별 루프에 쿼리가 없어 N+1 은 없다.
- 주의(I4): `after_call` 은 순차이고 각각 3초 상한이다. 한 회차에 호출이 20개를 넘게 생기면 스케줄 잠금 TTL(기본 60초)에 닿을 수 있다. 정상 회차는 0 ~ 2개라 문제가 안 된다. 동기화가 멈췄다 다시 돈 첫 회차만 해당한다(⑦ · OQ-102 와 같은 상황).

## 8. 시험 판별력 (머릿속 변이)

| 변이 | 잡나 |
|---|---|
| `_by_system` 항상 False | 잡음 — 2명 지정 시험 |
| `_by_system` 항상 True | 잡음 — DAY 지정 시험 |
| 메아리 pending/sent 분기 삭제 · `never_sent` 무시 · `updated_at` 창 삭제 | 잡음 — 메아리 파라미터 시험 · BLOCKED/NO_TOKEN 시험 · 창 지난 뒤 시험 |
| ⑦ 오늘 · WAITING · 카드 · SETTLED · 시스템 계정 거름 각각 삭제 | 잡음 — 거름 시험 3개 |
| 묶음 기준을 「직전 항목과의 차」로 | 잡음 — 순수 묶음 시험 |
| 같은 대상 키를 대표 id 로 | 잡음 — 집합 다름 시험 |
| ④ 사슬 판정 · 닫기 삭제 | 잡음 — 사슬 · 일부 옮김 시험 |
| `take_task_calls` tx 비교 삭제 | 잡음 — rollback 시험 |
| `run_schedules` 의 after_commit 을 commit 앞으로 | 잡음 — 커밋 전이라 행이 안 보여 알림 0 |
| **`_chain_room_assign` 의 after_commit 두 줄 삭제** | **못 잡음** — 시험 `detail_round` 가 `_apply_detail` 을 직접 부르고 스스로 commit 한다 → W3 |
| **`ext_sync._load_date` 의 apply/after_commit 삭제** | **못 잡음**(오늘이 아니라 영향은 0) |
| **(ㄱ) 실제 `apply_schedules` → `_apply_tasks` 연결** | 시험은 `apply_schedules` 를 `apply_visit_tasks` 로 바꿔 끼운다 → `sync_schedules.py` 경로의 잠금 순서는 이 시험이 보지 않는다(공통 `_apply_tasks` 라 위험은 낮음) |
| **방문 잠금 제거 / 이전 값 읽기를 잠금 앞으로** | **못 잡음** → W4 |
| 오래된 사본이 늦게 커밋되는 순서 · 시스템 계정 DAY 지정 호출 | 시험 없음(W1 · W2) |

## FAIL

없음.

## WARN

**W1 [중 · 중복 알림] 오래된 KOS 사본이 늦게 커밋되면 같은 KOS 호출이 호출 · 알림 2번이 된다** — `dtos/sync_state.py:43-46` · `services/emr_sync.py:447/490`(연쇄 상세 조회) · `services/ext_sync.py:95` · `_save_scoped_schedules` 의 사본 조회
- 근거: KOS 조회는 세 경로 모두 tx 와 잠금 **밖**에서 한다(`emr_sync.py:255` 주석 「transaction 밖」). 잠금은 읽기와 쓰기를 차례로 세울 뿐, 먼저 조회한 사본이 먼저 커밋된다는 보장은 없다. `_apply_tasks` 는 작업 사본이 오래돼도 그대로 덮는다.
- 순서 예: ⓐ 연쇄 · 외부 연동이 T−1 에 조회(V0 = 빈 값) ⓑ 간호사가 KOS 에서 호출 V1 ⓒ 10초 조회가 T+1 에 조회 → 커밋 → 호출 K1 · 알림 ⓓ ⓐ 가 커밋해 V1 → 빈 값으로 되돌림(① 미해당) ⓔ 다음 10초 조회가 빈 값 → V1 을 「새로 생김」으로 봄. 메아리 op 이 없으니 호출 K2(④ 재호출 사슬, K1 닫힘)와 **알림 · 푸시가 한 번 더** 간다. V0 이 앞 호출 시각이면 ⓓ 에서 바로 K2 가 생긴다.
- 빈도: 두 조회 사이에 KOS 호출이 끼고 커밋 순서가 뒤집혀야 한다(초 단위 창). 드물지만 스펙 ① 「한 변화에 호출 하나」를 잠금만으로는 못 지킨다.
- 고칠 방향(작음): `call_changed` 를 **앞으로만** 본다 — `before is None or called_at > before`(KOS 호출 시각은 다시 부르면 늘어나기만 한다 · 스펙 「다시 부르면 시각이 바뀐다」). 이것으로 ⓓ 의 V1 → V0 은 닫힌다. 빈 값으로 되돌렸다가 다시 생기는 경우(ⓓ → ⓔ)까지 막으려면 `_apply_tasks` 에서 KOS 가 빈 값 · 더 이른 값을 줄 때 `doctor_called_at` 을 이전 값으로 두는 규칙이 필요하다. 스펙에 없는 판단이라 코디나 사용자가 정해야 한다. 적어도 앞의 한 줄과 그 시험은 prod 전에 넣기를 권한다.

**W2 [중 · 엉뚱한 받는 사람] 시스템 계정으로 DAY 에 로그인해 누른 지정 호출은 받는 사람이 `called_doctor`(KOS 옛 값)로 바뀐다** — `services/notifications.py:337-351`
- 근거: OQ-107 ⓒ 는 「이 계산을 탈 수 있음」을 받아들였다. 그런데 결과가 「추가로 더 받음」이 아니라 **지정한 원장이 못 받음**일 수 있다. DAY 호출 직후 `after_call` 시점에는 KOS 쓰기(`call-tasks-doctors`, `doctorIds` 없음 · `kos/writes.py:481-496`)가 아직 pending 이다. 그래서 `called_doctor` 행은 앞 KOS 호출의 원장이거나 0명이다 → 받는 사람이 0명이거나 다른 원장이 된다. 이 변경 전에는 그 원장 한 명이 받았다 → **회귀**다(시스템 계정 로그인을 실제로 쓰는 병원에서만).
- 고칠 방향(작음 · 스펙 결과 무변경): 시스템 계정 분기에서 `Staff.id == target_staff_id OR Staff.id IN (called_doctor…)` 로 **합친다**. 규칙 40 호출은 대표가 `called_doctor` 의 첫 원장이라 결과가 같고, ⓒ 의 경우 지정 원장이 반드시 받는다. 시험 1개(시스템 계정 직원으로 DAY 지정 호출 → 그 원장 받음)를 더한다. 시스템 계정 DAY 로그인을 실제로 쓰는지는 코디 확인.

**W3 [하 · 시험 공백] 상세 연쇄 커밋 두 곳의 `after_commit` 배선을 지키는 시험이 없다** — `services/emr_sync.py:468` · `:504` · 시험 `kos_call_support.py:83-97`
- `detail_round` 가 `_apply_detail` 을 직접 부르고 스스로 commit 한다. 그래서 `_chain_room_assign` 에서 두 줄을 지워도 시험은 초록이다. 지금 코드는 맞다. 고칠 방향: `_chain_room_assign` 을 가짜 adapter 로 한 번 돌려 알림 1 을 확인하는 시험(기존 `test_board_room_chain.py` 틀 재사용).

**W4 [하 · 시험 공백] 「잠금 뒤 이전 값 읽기」와 판 조작 겹침을 판별하는 시험이 없다** — `tests/.../test_kos_calls_flow.py:204-209`
- 보고서 주의 2 대로 겹침 시험은 `Refs.link` 행 잠금 덕분에 통과한다. 지금 잠금 범위는 코드로 맞음을 확인했다(§2). 고칠 방향(선택): 판 조작 tx 가 `board:{visit}` 를 잡은 채 DAY 호출 op 을 만들고, 그동안 동기화 `apply_visit_tasks` 를 띄운다. 이어서 조작 commit 뒤 동기화가 메아리로 0건인지 보는 시험이다. hotfix 범위 밖이면 다음 루프로 미뤄도 된다.

## 참고 (INFO)

- I1 `kos_calls.apply` 예외는 savepoint 없이 회차 전체를 rollback 한다. 같은 KOS 값이 매 회차 같은 예외를 내면 그 병원 동기화가 멈춘다. 예외가 날 자리는 못 찾았다. 감싸서 삼키면 후보를 잃어(다음 회차 「바뀌지 않음」) 알림이 빠지므로, 지금 쪽이 낫다고 본다. `_call_path` 는 `WriteNotSupportedError` 만 잡는다. Vegas 는 `UnsupportedVendorError`(`emr/factory.py:167`)를 낸다. Vegas 동기화가 지금은 없어 실제로 탈 일은 없다(나중에 Vegas 를 붙일 때 `EmrError` 로 넓힐 것).
- I2 (라) 판별의 남은 틈: 보내기 오류(타임아웃 등)로 retry → pending → `NO_TOKEN` failed 가 된 op 은 KOS 가 실제로 받았을 수 있는데 「보내기 전」으로 친다. 이때 KOS 호출로 한 번 더 만든다. 스펙 R3 판별 그대로이고 드물다.
- I3 묶음 대표 원장: 같은 집합이면서 작업마다 `calledDoctors` 차례가 다르면 `targets[key]` 는 **마지막** 작업의 첫 원장이다(`kos_calls.py:176`). 스펙 「차례상 첫 원장」이 묶음 안에서 어느 작업 기준인지는 정해지지 않았다. 표시 이름에만 영향이 있다.
- I4 `after_call` 순차 × 3초 상한과 스케줄 잠금 TTL 60초(§7).
- I5 `_system_staff` 는 `board_transactions` 의 비공개 이름을 다른 모듈에서 import 한다(`kos_calls.py:49`). `board_quick_start.py:82` 에 선례가 있고 Taut 는 통과했다. 정리 거리일 뿐이다.
- I6 KOS 와 DAY 시계가 30초 넘게 어긋나면 메아리 판정이 깨져 DAY 호출마다 중복 알림이 생긴다. OQ-101 첫 실물(DAY 호출 1회 → KOS `doctorCallDateTime` ↔ op `created_at`/`updated_at`)을 **dev 에서 prod 전에** 꼭 보기를 권한다.

## 직원이 실물에서 만날 자리

1. 간호사가 KOS 에서 원장을 부르면 10초 안에 원장 앱 · 웹에 「원장 호출」 알림 · 푸시가 1번 오고, 판 줄은 「호출」이 된다. 「늦음」은 DAY 가 알게 된 때부터 센다(보고 주의 3 · 최대 10초 차).
2. DAY 에서 누른 호출은 KOS 를 거쳐 돌아와도 알림이 더 가지 않아야 한다. **KOS 시계가 어긋나 있으면 여기서 두 번 온다**(I6). dev 첫 실물에서 꼭 볼 것.
3. 아주 드물게 같은 KOS 호출에 원장 푸시가 몇 초 간격으로 두 번 온다(W1 · 동기화 경로가 겹칠 때).
4. 시스템 계정으로 DAY 에 로그인해 원장 한 명을 지정해 부르면 그 원장이 알림을 못 받거나 다른 원장이 받을 수 있다(W2).
5. KOS 에서 2명을 지정하면 둘 다 알림을 받지만, 판 · 앱에는 첫 원장 이름만 보인다. DAY [재호출]은 그 첫 원장에게만 간다(OQ-107 ⓐ ⓑ · 스펙대로).
6. KOS 에서 집도의를 정하면 DAY 줄이 「수락」이 된다. DAY 호출 쓰기가 아직 KOS 에 닿기 전이면 한 회차(~10 ~ 30초) 늦게 「수락」이 된다.
7. 배포 전 prod worker 가 멈춰 있었다면 첫 회차에 오늘 남은 KOS 「호출」이 한꺼번에 알림으로 갈 수 있다(⑦ · OQ-102 · 운영 메모).
