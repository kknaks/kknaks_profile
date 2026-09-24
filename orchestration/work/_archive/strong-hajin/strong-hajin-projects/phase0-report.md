# Phase 0 결과 — `material_*` 계열의 병렬 격리

**상태: done** · 2026-09-22 · strong-hajin `backend` 워커
워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`, 브랜치 `kknaksss/strong-hajin-projects`, 커밋 0건.
기기: Apple 11 core / 18GB. 측정 내내 사용자의 브라우저 E2E 스택이 같은 기기에서 돌았다(착수 시 load average 5.4).

---

## 0. 한 문단 — 원인은 무엇인가

> ⚠ **뒤에 넓혔다** — 이 판이 「자식 «프로세스»」로 적은 기준은 좁았다. 원인의 본질은
> 「**초 단위 실시간 창을 재는데 워커 수가 코어 수에 닿는다**」이고, 그 창을 만드는 동시성이
> 프로세스인지 스레드인지는 본질이 아니다. 현재 기준은 `phase0-fix3-report.md` §0 에 있다:
> **자식 프로세스 «또는» 테스트가 직접 띄운 스레드**.

**원인은 「병렬」이나 「DB·파일 공유」가 아니라, 이 두 파일이 한 테스트 안에서 진짜 자식
인터프리터를 최대 둘 띄우고 그 위에서 초 단위 창을 실시간 시계로 재는데, `-n auto`(= 코어 수 11)가
그 창보다 큰 스케줄 지터를 만든다는 것이다.** 근거는 셋이다. ① `-n auto` 로 그 두 파일만 20건 돌려
28초 만에 재현했고, `test_material_search` 실패에는 **자식 프로세스의 traceback 이 그대로 찍혔다** —
`sqlite3.OperationalError: database is locked`: `material_worker_concurrency=2` 가 claim 한 두 job 이
`asyncio.gather` 로 **자식 둘을 동시에** 띄우고, 둘이 같은 per-test SQLite 파일에서
SELECT(SHARED) → INSERT(RESERVED) 승급을 겹쳐 SQLite 의 교착 회피가 한쪽을 즉시 BUSY 로 튕긴다.
② `test_material_worker_recovery` 의 실패는 **추출 원장은 옳게 `failed`/`time_limit_exceeded` 로
닫혔는데 job 원장만 `running` 에 남았다** — `_time_out()` 이 `MemoryDurableJobQueue.fail()` 을 부를 때
`_fenced()` 가 `lease_expires_at > now` 를 요구하는데, 테스트가 `material_queue_visibility_timeout=3`
으로 줄여 둔 lease 가 그 사이 만료됐다. 상태 기계가 아니라 **fencing 창을 놓친 것**이다.
③ 워커 수를 바꿔 가며 재면 **`-n0`·`-n2`·`-n4` 는 전부 통과하고 `-n auto`(11) 에서만 넘어진다.**

한 줄로: **계약이 다른 값을 내는 것이 아니라, 실시간 시계로 잰 창이 워커 수가 코어 수에 닿는 순간
스케줄 지터에 먹힌다.**

---

## 1단계. 원인 규명 — 검증한 것과 **버린 가설**

### 빠른 재현자를 먼저 만들었다 (28초)

전체 스위트(300~380초) 대신 **그 두 파일만 `-n auto`** 로 돌리면 재현된다.

```
uv run pytest tests/contract/test_material_search.py \
              tests/contract/test_material_worker_recovery.py -n auto --dist worksteal -q
→ 3 failed, 17 passed in 28.22s        # exit 1
  FAILED test_material_worker_recovery::test_stage_timeout_fences_the_late_parser_result
  FAILED test_material_worker_recovery::test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it
  FAILED test_material_search::test_when_a_material_was_registered_is_a_different_question_from_what_it_says
```

**20건만으로 재현된다**는 것 자체가 첫 번째 답이다 — 「계약 테스트가 늘어서」가 아니다.

### 검증 ① 무엇을 두고 다투나 — **자식 둘이 같은 SQLite 파일을 두고 다툰다**

`test_material_search` 실패에 **자식 프로세스의 traceback 이 그대로 붙어 있었다**:

```
ERROR ax_workspace.bootstrap.material_worker: material extraction delivery ended without a result (job fe4ca024…)
RuntimeError: isolated work failed:
  …material_worker.py:312  claimed = self._service(session).claim(job)
  …platform/material_extraction.py:267  self._session.flush()
  sqlite3.OperationalError: database is locked
```

경로를 코드에서 되짚으면 이렇다.

- `Settings.material_worker_concurrency = 2` → `_claim_jobs(limit=2)` 가 **job 둘을 한 번에** 든다
  (`material_worker.py:236-246`).
- `run_once()` 가 `asyncio.gather(*(self._deliver(job) for job in jobs))` 로 **자식 둘을 동시에** 띄운다
  (`material_worker.py:98`). 자식은 `IsolatedWork` = `multiprocessing.get_context("spawn")` —
  **앱 전체를 다시 import 하는 새 인터프리터**다(`isolated_work.py:32`).
- 자식은 `MaterialExtractionWorker.process()` 안에서 `repository.get()`·`session.get()`(SELECT → SHARED)
  뒤에 `claim()` 이 `MaterialExtractionAttemptRecord` 를 INSERT 하며 `flush()`(→ RESERVED 승급)를 부른다
  (`platform/material_extraction.py:230-268`).
- **둘이 같은 파일에서 SHARED 를 쥔 채 RESERVED 로 올라가려 하면** SQLite 는 교착을 피하려고 한쪽에
  `SQLITE_BUSY` 를 **즉시** 돌려준다 — busy handler 를 거치지 않는 경로다. `make_session_factory` 는
  `create_engine(url, pool_pre_ping=True)` 뿐이라 WAL 도, `busy_timeout` 도 걸려 있지 않다
  (`platform/persistence.py:1996`).

즉 **공유물은 xdist 워커 사이의 무엇이 아니라, 한 테스트 자신의 자식 둘이 나눠 쓰는 per-test SQLite
파일**이다. 실패한 두 테스트(`…registered_is_a_different_question…`, `…searching_without_naming…`)가
모두 **정확히 두 건을 업로드한다**는 것이 이 그림과 맞는다.

### 검증 ② 시간 단언이 무엇을 기다리나 — **실시간 시계에 매달려 있다**

`test_stage_timeout_fences_the_late_parser_result` 의 실패는 값이 「이전 상태」인 것이 아니라
**원장 둘이 갈라진 것**이다:

```
extraction.status == "failed" and failure_reason == "time_limit_exceeded"   ← 통과했다
assert [job["state"] …] == ["failed", "completed"]
E   AssertionError: assert ['running', 'running'] == ['failed', 'completed']
```

`_time_out()` 은 한 트랜잭션에서 둘을 닫는다 — `repository.fail(extraction, "time_limit_exceeded")` 와
`queue.fail(job_id, lease_token)`(`material_worker.py:163-170`). 앞은 성공했고 뒤만 실패했다.
`MemoryDurableJobQueue.fail()` 은 `_fenced()` 를 지나는데 그 조건이
**`lease_expires_at > now`**(`platform/durable_jobs.py:208-219`)다. 테스트가
`material_queue_visibility_timeout=3`·`material_stage_timeout_seconds=1` 로 줄여 뒀으므로
**lease 는 3초짜리**이고, heartbeat 주기는 `visibility/3 = 1초`다(`material_worker.py:122`).
`_handle_with_heartbeat` 의 루프는 `await asyncio.sleep(…0.05…)` 와 `await asyncio.to_thread(…)` 로
돌아가는데, 11 워커 × (자식 최대 2) 로 기계가 넘치면 **한 바퀴가 3초를 넘어간다** — 그러면 timeout 이
도착했을 때 lease 는 이미 죽어 있고, job 원장은 `running` 에 남는다.

같은 파일의 `test_long_parse_heartbeats…` 도 같은 뿌리다: `asyncio.sleep(3.15)` 뒤에 job 이 아직
`running` 이기를 요구하는데, 그 앞에서 **`IsolatedWork.__init__` 가 이벤트 루프를 동기로 막은 채**
새 인터프리터를 spawn 한다. spawn 이 lease(3초)보다 오래 걸리면 첫 heartbeat 가 그 뒤에야 돈다.

**폴링도 sleep 도 아니고 「실시간 시계로 잰 3초 lease」가 기다리는 것**이다. 그래서 흔들린다.

### 검증 ③ 「병렬」인가 「부하」인가 — **둘 다 아니고 「워커 수가 코어 수에 닿는 것」이다**

지시서가 요구한 대로 워커 수를 바꿔 가며, 그리고 부하를 따로 걸어 가며 쟀다.

| 재는 법 | 결과 |
|---|---|
| `-n0`, 무부하 | 20 passed (여러 회차) |
| **`-n0`, CPU 스피너 11개 동시 (load average 13.85, pytest 가 코어 0.88개만 씀, 64s)** | **20 passed · exit 0** |
| `-n2` × 2회 | 20 passed · 20 passed |
| `-n4` × 2회 | 20 passed · 20 passed |
| `-n auto`(11) × 3회 | **3 failed · 1 failed · 0 failed** |

**`-n0` 은 load average 13.85 에서도 초록이었다.** 그러므로 「기계가 바쁘면 흔들린다」는 설명만으로는
부족하다 — 넘어지게 만드는 것은 **동시에 뛰는 파이썬 프로세스의 수**(11 xdist 워커 + 각자가 띄우는
자식 최대 2 = 최대 33)이고, 그것이 이벤트 루프 한 바퀴와 SQLite 트랜잭션 창을 lease 보다 길게 늘인다.

### 같은 파일 안에서 **어느 건이 넘어지는지가 회차마다 바뀌는 이유**

경합 창이지 결정적 실패가 아니기 때문이다. 세 건이 각자 다른 창을 갖고 있고
(`stage_timeout=1s` · `visibility=3s` · 자식 둘의 INSERT 겹침), 그날 그 순간 어느 창이 먼저 먹히는지가
스케줄에 달려 있다. 위 표의 `-n auto` 3회가 3f → 1f → 0f 로 나온 것이 그 자체로 증거다.

### 버린 가설 — **네 개, 근거와 함께**

1. **「xdist 워커들이 DB·파일을 공유한다」 → 버렸다.**
   테스트마다 `tmp_path` 안의 자기 SQLite 파일과 자기 materials 디렉토리를 쓴다
   (`test_material_search.py:_stack`). 공유물이라면 `-n2` 에서도 넘어져야 하는데 `-n2`·`-n4` 는
   4회 전부 초록이었다. 그리고 실제로 찍힌 lock 충돌은 **한 테스트 자신의 자식 둘 사이**였다.

2. **「`pytest-randomly` 의 순서 섞기」 → 버렸다(정정 확인).**
   `uv pip list` 에 `pytest` 8.4.2 와 `pytest-xdist` 3.8.0 뿐이다 — `pytest-randomly` 는 설치돼 있지
   않다. 캘린더 문서의 `-p no:randomly` 는 **무동작**이었고, 그 회차에서 실제로 직렬화한 것은 아무것도
   없다. 직렬화 스위치는 `-n0` 하나뿐이라는 기준선 §0 의 정정이 맞다.

3. **「기계 부하(CPU)가 원인이다」 → 버렸다.**
   `-n0` + CPU 스피너 11개로 load average 13.85 를 만들고 pytest 를 코어 0.88개로 굶겼는데도
   (46s → 64s) **20 passed · exit 0**. 부하 자체로는 재현되지 않는다.

4. **「제품 상태 기계가 틀렸다」 → 버렸다.**
   실패한 단언 바로 앞줄에서 **추출 원장은 옳은 종단 상태로 닫혀 있었다**
   (`failed`/`time_limit_exceeded`). 어긋난 것은 job 원장뿐이고, 그 원인은 fencing 이 요구하는
   lease 만료다. 그리고 `-n0`·`-n2`·`-n4` 에서 같은 코드가 20/20 통과한다.

---

## 2단계. 고른 격리 수단과 이유

**고른 것: 그 계열만 `-n0` 로 갈라 도는 직렬 패스.** 제품 코드는 **한 줄도 건드리지 않았다.**

왜 이것인가:

- 원인이 **「그 두 파일 자신이 프로세스를 띄우고 실시간 창을 잰다」** 이므로, 그 파일들을
  **혼자 뛰게** 하는 것이 원인에 맞는 수단이다. `-n0` 은 5회차 내내, 그리고 부하 아래서도 초록이었다.
- **`--dist loadgroup` + `xdist_group` 은 고르지 않았다 — 다만 이것은 *재지 않은* 기각이다.**
  loadgroup 은 그 파일들끼리 한 워커에 묶어 줄 뿐 **나머지 10 워커는 계속 돈다.** 원인이 파일 간
  경합이 아니라 **기계의 파이썬 프로세스 과잉**이라는 것이 §1 검증 ③ 의 결론이므로, 나머지 10 워커가
  남아 있는 한 듣지 않을 수 있다고 봤다. 한편 같은 검증 ③ 의 「`-n0` 이 load average 13.85 에서도
  초록」이라는 수치는 **반대로 loadgroup 이 먹힐 수도 있다**는 쪽을 가리킨다 — 두 해석이 갈리는
  자리다. **재지 않았으므로 단정하지 않는다.** 고른 이유는 `-n0` 쪽에만 5회차 근거가 있기 때문이다.
  loadgroup 의 장점(명령이 하나로 남는다)이 필요하면 그때 재서 바꾸면 된다.
- **폴링·타임아웃 넉넉히 늘리기는 고르지 않았다.** 그것은 증상 완화이고, 무엇보다
  `visibility_timeout=3` 은 **그 테스트가 증명하려는 대상**이다(짧은 lease 위에서 heartbeat 가 도는가).
  늘리면 계약이 증명하던 것이 사라진다.
- **lease/timeout 을 주입 시계로 바꾸는 근본 수단은 고르지 않았다.** 그것은 `material_worker.py` ·
  `durable_jobs.py` 를 고치는 **제품 코드 변경**이고, 테스트만으로 닫히는 길이 있는데 먼저 손댈 자리가
  아니다. 다만 **원인은 거기에 있다** — 나중에 근본적으로 고칠 자리로 §5 에 남긴다.

### 바꾼 것

| 파일 | 무엇 |
|---|---|
| `Makefile` | `MATERIAL_SERIAL_TESTS` 변수 · `test-material-serial` 타겟 신설. `test`·`test-contract` 가 **두 패스**가 됐다 — 병렬 패스는 `$(addprefix --ignore=,…)` 로 그 둘을 빼고, 이어서 `$(MAKE) test-material-serial` 이 `-n0` 로 돈다 |
| `backend/tests/architecture/test_serial_test_targets.py` | **신규.** 갈라 둔 계약이 조용히 썩지 않게 지킨다 — 목록의 파일이 실재하는지, 직렬 타겟이 `-n0` 인지, 병렬 타겟이 그 둘을 빼고 **그리고 이어 부르는지**, `verify` 가 여전히 `test` 를 지나는지 |
| `backend/tests/contract/test_material_search.py` · `test_material_worker_recovery.py` | **docstring 한 단락씩만.** 왜 이 파일이 갈라져 있는지와, 옮기면 `MATERIAL_SERIAL_TESTS` 도 고쳐야 한다는 것 |
| `README.md` · `AGENTS.md` | 두 패스라는 사실과 이유를 실행 절차의 정본에 적었다 |

**부작용 하나를 같이 막았다.** `PYTEST_ADDOPTS='-k "…"' make test-contract`(`docs/demo-work-seed.md:41`)
처럼 필터를 걸면 직렬 패스가 한 건도 못 고르고 pytest 가 **5**(= 고를 것이 없었다)로 끝난다.
그것은 실패가 아니므로 `test-material-serial` 이 **5 만** 삼킨다. 목록이 실재하는지는 architecture
테스트가 따로 지키므로 이 관용이 진짜 사라짐을 감추지 않는다.
확인: `PYTEST_ADDOPTS='-k "demo_work_seed or reset_demo"' make test-material-serial` → `20 deselected` · **exit 0**.

### 수집 수가 맞는지 — 잃은 것도, 두 번 도는 것도 없다

```
병렬 패스 (--ignore 둘)  : 1542/1659 collected (117 deselected)
직렬 패스 (그 두 파일)    :   20 collected
전체 (가르기 전)          : 1562/1679 collected (117 deselected)     1542 + 20 = 1562 ✓
```

---

## 3단계. `make verify` 의 계약

`verify: test test-scale test-release frontend-test frontend-assets frontend-build` — **그대로 뒀다.**
가른 것은 `test` **안쪽**이므로 `make verify` 는 여전히 한 명령이고, 초록도 한 자리에서 난다.
새 타겟 `test-material-serial` 은 `test`·`test-contract` 가 이어서 부르므로 따로 부를 일은 재측정뿐이다.

