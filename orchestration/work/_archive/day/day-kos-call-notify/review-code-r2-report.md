# 리뷰 리포트 — day-kos-call-notify / code r2 (2026-11-25)

- 대상: 같은 워크트리 미커밋 변경(1루프 + be-fix-1)
- 기준: r1 리포트 · `be-fix-1-instructions.md`(코디 결정) · `be-fix-1-report.md` · DAY-SPEC-002 규칙 40 · DAY-SPEC-005 「KOS 에서 건 호출」
- 읽기만 했다. 리포 수정 · 커밋 · push 없음.

## 판정: **PASS**

r1 의 W1 ~ W4 · I1 · I3 · I5 는 코디 지시대로 고쳐졌고 시험도 붙었다. 수정이 만든 새 문제는 없다. 보고서가 「남은 좁은 틈」으로 적은 경우(DAY 호출 메아리 시각이 옛 사본으로 빈 값 → 값으로 되돌아옴)는 **기존 메아리 창이 이미 막는다**(§3). 코드 변경 없이 시험 1개만 더하면 된다(N1 · 선택).

남은 것은 코드 밖에 있다:
- I6: KOS ↔ DAY 시계 차이를 dev 실물에서 확인
- 스펙 반영 4건(#965): W1 ① · W1 ② · W2 · I3

## 검증 — 명령과 수치

- `./scripts/test.sh -q -p no:cacheprovider` 로 아래를 돌렸다 → **163 passed (36.7초 · 격리 인프라)**.
  - `board/test_kos_call_rules.py`
  - `notifications/` 전체(새 `test_kos_calls_races.py` 포함)
  - `board/test_board_api_calls.py` · `test_board_rules_calls.py` · `test_board_locks.py` · `test_board_room_chain.py` · `test_board_api_quick_start.py`(I5)
  - `emr/test_sync.py` · `emr/test_emr_sync_service.py`
- `ruff check` 와 `ruff format --check` 를 바뀐 파일 · 새 파일 14개에 돌렸다 → 모두 통과.
- 프로젝트 `mypy`(strict) → **Success: no issues found in 655 source files**.
- 브리프의 `uv run pytest` 대신 리포 정본 러너를 썼다. 사용자 스택 · 포트 · 공유 DB 는 건드리지 않았다. 전체 회귀(2909 passed)는 backend 보고 수치이고, 나는 다시 돌리지 않았다.

## 1. 닫힘 / 남음

| r1 | 고친 곳(backend/) | 시험 · 변이(코드로 확인) | 상태 |
|---|---|---|---|
| W1 ① 앞으로만 | `day/dtos/sync_state.py:43-51` — `called_at is None` 이면 False · `before is None or called_at > before` | `test_kos_call_rules.py:133`. 비교를 `!=` 로 되돌리면 앞 시각 되돌림 단언이 깨진다 | **닫힘** |
| W1 ② 이미 만든 KOS 시각 이하 거름 | 조회 `day/services/kos_calls.py:105-132` · 거름 `:186-188`(메아리 판정 앞) · 기록 `:277` `kosCalledAt {taskId: isoformat}` · 조회 시점 `:344`(`apply` 안 = 같은 tx · 방문 잠금 뒤) | `test_kos_calls_flow.py:204-227` 이 ⓐ ~ ⓔ 와 ⓓ' ⓔ' 를 재현한다 → 호출 2(V0 · V1) · K1 알림 1 · 푸시 `[first, k1]`. V2(+40초)는 새 호출. 거름을 지우면 ⓔ 에서 호출이 3개가 돼 깨진다 | **닫힘** |
| W2 합집합 | `day/services/notifications.py:337-355` — `Staff.id == target OR IN (called_doctor…)` · 시스템 계정 분기 안에서만 | `test_kos_calls.py:123`(시스템 계정 DAY 지정 · KOS 앞 원장) · 2명 지정 시험 그대로 통과 | **닫힘** |
| W3 상세 연쇄 배선 | 코드 무변경(`services/emr_sync.py:468` · `:504`) | `test_kos_calls_races.py:65` — 실제 `run_outbox` → `_chain_room_assign` 을 가짜 KOS(`BoardKos` 상속)로 돌리고, `from_detail` 1 · 2 로 커밋 두 곳을 따로 친다. 각 줄을 지우면 그 경우의 `notified`/`call_push_kicks` 단언이 깨진다 | **닫힘** |
| W4 판 조작 겹침 | 코드 무변경 | `test_kos_calls_races.py:88` — DAY 호출을 `_finish`(commit) 앞에서 멈춰 잠금과 op 을 쥔 채, `detail_round` 를 띄운다. 0.5초 뒤 아직 기다리는지(`waited`) 보고, 조작 commit 뒤 메아리 0건 · 호출 = DAY 호출 1 · 푸시 1 인지 본다. `lock_visits` 를 빼면 동기화가 op 을 못 본 채 먼저 진행해 KOS 호출이 하나 더 생긴다 → 깨진다 | **닫힘**(I-c 참고) |
| I1 `_call_path` 예외 | `kos_calls.py:67-71` `except EmrError` — 회차 rollback 동작은 그대로 | `test_kos_call_rules.py:157`(KOS = 경로 · Vegas = None) | **닫힘** |
| I3 대표 = 가장 작은 sequence | `kos_calls.py:218-228` — 묶음 키(kind + 집합)는 그대로, 대표만 `min(sequence)` 의 `called_doctor_ids` 로 다시 계산. 같은 집합이라 kind 와 대상은 바뀌지 않는다 | `test_kos_calls.py:150` | **닫힘** |
| I5 공개 이름 | `board_transactions.py:349` `system_staff` · `:227` · `board_quick_start.py:31` · `:79-108`(지역 변수 이름 겹침 정리) · `kos_calls.py:343` | 바로 시작 시험 통과 · mypy 통과 | **닫힘** |
| I2 · I4 · I6 | 변경 없음 | — | **남음 · 이유 타당**(아래) |

「그대로 둔 이유」 검토:
- **I2 타당.** `external_outbox` 에 2xx 이력 칸이 없어 migration 없이 더 가를 수 없다. 틀리면 알림이 빠지는 쪽이 아니라 한 번 더 가는 쪽이다. 그 한 번은 W1 ② 덕분에 사본이 되돌아와도 다시 늘지 않는다.
- **I4 타당.** 정상 회차는 새 호출 0 ~ 2개다. 잠금 TTL 에 닿는 것은 멈췄던 동기화의 첫 회차뿐이고, 같은 운영 메모(⑦ · OQ-102)에 묶여 있다.
- **I6 타당.** 코드로 풀 일이 아니라 실물 확인 항목이다. 시계 차이는 W1 ② 로도 막히지 않으므로 prod 전 dev 실물 확인은 여전히 필수다.

## 2. 수정이 만든 새 문제 — 없음

**W1 ② `_made_kos_times`**
- 잠금 · tx: `apply` 안에서 `load_world` 와 같은 tx 로 돈다. `_apply_tasks` 가 잡은 방문 잠금(`pg_advisory_xact_lock`)이 commit 까지 유지되므로 잠금 안이다. 같은 방문의 다른 동기화 · 판 조작은 이 사이에 `call.create` 를 쓸 수 없다.
- 비용: 후보가 있는 회차에만 1 쿼리 늘어난다. `ix_event_log_visit_id_type (visit_id, type) WHERE deleted_at IS NULL`(`models/task.py:284-289`)를 타고, `occurred_at >= 오늘 0시` 와 `source` 거름은 남은 행에 적용된다. 방문 하나의 오늘 `call.create` 는 보통 몇 행이라 가볍다.
- 시각 단위 · 시간대:
  - 기록은 KOS 시각 그대로 `isoformat()` 이다. 마이크로초와 `+00:00` 이 남는다.
  - 읽기는 `fromisoformat` 이라 aware 끼리 비교한다. 같은 값이 다시 오면 `<=` 로 같다고 판정된다.
  - 「오늘」 하한은 `today(now)[0]`(UTC aware)과 `occurred_at`(timestamptz) 비교다.
  - 자정 직전 호출을 자정 뒤에 처음 보면 ⑦ 「오늘 아님」이 먼저 거른다.
- 진짜 재호출을 막지 않는가: KOS 시각은 다시 부를 때마다 늘어난다. 그래서 새 호출은 항상 `> made` 이고 막히지 않는다(V2 시험).
- 거름 순서: W1 ② 가 메아리 판정보다 앞에 있어도 둘 다 「만들지 않음」이라 결과는 같다.

**W2 합집합**
- `else` 분기(`:354`)는 그대로다. 시스템 계정이 아닌 직원이 누른 호출은 kind one/all 모두 받는 사람이 **바뀌지 않는다**. `kind=all` 은 분기 밖이다.
- 시스템 계정 분기는 규칙 40 호출에서 대표가 `called_doctor` 의 첫 원장이므로 집합이 같다.
- 시스템 계정으로 DAY 에서 누른 지정 호출: 지정 원장은 반드시 받는다. KOS 옛 `called_doctor` 원장이 덤으로 더 받을 수 있다. be-fix-1 보고의 「스펙 반영 3」이 이 결과를 적었다.

**I1 예외 범위**
- `EmrError` 는 업체 쓰기 계획의 오류만 덮는다. `write_planner` · `plan` 은 HTTP 를 열지 않는다(`factory.py:160-167`).
- DB 예외 등 그 밖의 예외는 그대로 올라가 회차를 rollback 한다. 지시대로다.

## 3. 보고서 「이슈」 — DAY 호출 메아리 시각이 옛 사본으로 되돌아오는 틈

결론: **migration · 새 enum 없이 이미 막혀 있다.** 코드 변경은 필요 없고, 이 성질을 고정할 시험 1개를 권한다(N1).

근거(코드):
- 메아리 창(`policies/kos_calls.py:57-73`)은 **관측 시각이 아니라 KOS 가 찍은 호출 시각 E** 를 op 시각과 비교한다. 조건은 `E >= op.created_at − 30s`, 그리고 (op 이 pending · sent 이거나 `E <= op.updated_at + 30s`)다.
- E 는 KOS 가 그 op 을 받은 시각이라 `created_at ≤ E ≤ 2xx 시각 ≤ 확인 · 실패 시각` 이다.
- `updated_at` 은 `onupdate=func.now()`(`models/_columns.py:56-59`)라 뒤로 가지 않는다. 확인된 op 을 다시 바꾸는 코드도 없다. `_block_later` 는 pending 만, 예약 쓰기 재시도(`services/reservation_writes.py:337-347`)는 failed 만 pending 으로 되돌린다. 그때는 pending 이라 창 안이다. op 을 지우는 코드(`deleted_at` 설정 · DELETE)도 찾지 못했다.
- 그래서 **같은 E 가 몇 분 · 몇 시간 뒤 빈 값 → E 로 다시 와도** `E <= updated_at + 30s` 가 여전히 참이라 메아리로 걸린다. 「메아리 창이 지난 뒤」라는 상황은 같은 E 값에 대해서는 생기지 않는다. 창이 「지나는」 것은 그 뒤 KOS 에서 **새로** 건 시각(E' > updated_at + 30s)뿐이고, 그것은 실제 새 호출이 맞다.
- 예외는 두 가지다.
  - (a) KOS 시계가 DAY 보다 30초 넘게 앞섬(I6). 이때는 첫 메아리부터 이미 중복이다.
  - (b) 보내기 전 판별 오판(I2). 이때 E 는 규칙 40 호출로 만들어져 `kosCalledAt` 에 남으므로 W1 ② 가 막는다.

그래도 이중으로 막고 싶을 때의 방법:
- `event_log.type` 은 enum 도 CHECK 제약도 없는 `String`(`models/task.py:296`)이고 `payload` 는 JSONB 다. 그래서 migration 없이 쓸 수 있다.
- `creatable` 에서 메아리로 판정한 회차에 그 작업의 E 를 기록하면 된다. 예: 새 type `call.kos_echo` · payload `{kosCalledAt: {taskId: E}, source: "kos"}`. `_made_kos_times` 가 `call.create` 와 이 type 을 함께 읽는다.
- 대가: 메아리 회차마다 행이 1개 늘어난다(DAY 호출 1번당 보통 1행). 위 근거로 막는 효과가 (a) 시계 차이 경우에만 있다. 그런데 (a) 에서는 첫 메아리가 이미 새 호출을 만들어 그 E 가 `call.create` 에 남는다. 즉 효과가 사실상 0 이다. **권하지 않는다.**

## 지적

FAIL · WARN 없음.

**N1 [하 · 시험 공백 · 선택] 「DAY 호출 메아리 시각이 오래 뒤 빈 값 → 같은 값으로 돌아와도 0건」 고정 시험** — `tests/day/notifications/test_kos_calls_flow.py`
- 지금 성질(§3)은 `updated_at` 이 뒤로 가지 않는다는 점과 창 비교 기준(KOS 시각)에 기대고 있다. 누가 창 비교를 「관측 시각 `now` 기준」으로 바꾸면 조용히 깨진다.
- 고칠 방향: DAY 호출 → op `confirmed`(`set_call_ops(…, updated_at=E+2초)`) → `detail_round(E)` 0건 → `now` 를 10분 뒤로 → 빈 값 → 다시 E → 0건.

**I-a [정보] `kosCalledAt` 파싱 실패는 회차를 죽인다** — `kos_calls.py:126-129`
- `fromisoformat` · `uuid.UUID` 에 예외 처리가 없다. 이 payload 를 쓰는 곳은 이 모듈 하나(`:277`)라 지금은 안전하다. 나중에 다른 코드가 `call.create` + `source: "kos"` 를 쓰게 되면 그때 감쌀 것.

**I-b [정보] 시스템 계정 DAY 지정 호출의 덤 받는 사람** — `notifications.py:341-353`
- W2 결정대로 지정 원장 + KOS 옛 `called_doctor` 원장이 받는다. 스펙 반영 3(#965)에 들어가면 닫힌다.

**I-c [정보] W4 시험은 `asyncio.sleep(0.5)` 뒤 `not done` 으로 「기다림」을 본다** — `test_kos_calls_races.py:107-108`
- 정상 코드에서는 잠금 때문에 늘 기다리므로 거짓 실패가 없다. 변이(잠금 제거) 판별은 뒤쪽 「호출 = DAY 호출 1개」 단언이 맡는다. 느린 CI 에서 동기화가 0.5초 안에 잠금까지 못 가도 `waited` 는 참이라 깨지지 않는다. 문제없다.

## 사용자가 실물에서 만날 자리

1. 간호사가 KOS 에서 원장을 부르면 10초 안에 원장에게 「원장 호출」 알림 · 푸시가 1번 간다. 같은 호출이 동기화 경로 겹침으로 다시 보여도 더 가지 않는다(W1 ① ② 로 r1 의 「드문 2번」이 닫힘).
2. DAY 에서 누른 호출은 KOS 를 거쳐 돌아와도 알림이 더 가지 않는다. 단 **KOS 시계가 DAY 보다 30초 넘게 어긋나 있으면 두 번 간다**(I6). prod 전에 dev 에서 DAY 호출 1회로 꼭 볼 것(OQ-101).
3. 시스템 계정으로 DAY 에 로그인해 원장 한 명을 지정해 부르면 그 원장이 받는다. KOS 에 앞서 지정돼 있던 원장이 덤으로 같이 받을 수 있다(I-b).
4. KOS 에서 2명을 지정하면 둘 다 받는다. 판 · 앱 이름은 **가장 작은 순번 시술**의 첫 지정 원장 한 명만 보인다. DAY [재호출]은 그 원장에게만 간다(OQ-107 ⓐ ⓑ).
5. KOS 에서 집도의를 정하면 DAY 줄이 「수락」이 된다. DAY 호출 쓰기가 아직 KOS 에 닿기 전이면 한 회차 늦는다.
6. 배포 전 prod worker 가 멈춰 있었다면 첫 회차에 오늘 남은 KOS 「호출」이 한꺼번에 알림으로 갈 수 있다(⑦ · OQ-102 · 운영 메모).
