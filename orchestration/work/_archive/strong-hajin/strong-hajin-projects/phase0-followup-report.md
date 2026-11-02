# Phase 0 후속 결과 — 격리를 **기준**으로 정의했다

**상태: done** · 2026-09-22 · strong-hajin `backend` 워커 · task `task_0b3a05e2ce0b`
워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`, 브랜치 `kknaksss/strong-hajin-projects`, **커밋 0건**.
기기: Apple 11 core / 18GB. 측정 내내 사용자의 브라우저 E2E 가 같은 기기에서 돌았다(load average 2.5~18).
**전체 스위트는 한 번도 돌리지 않았다** — 좁은 집합과 좁은 선택으로만 쟀다. 백그라운드 루프 0건.

---

## 0. 기준 — **한 문장**

> ⚠ **이 문장은 좁았다 — `phase0-fix3-report.md` 가 넓혔다.** 현재 기준은 아래 인용 대신 이것이다:
> **한 테스트가 자기 안에서 진짜 «동시성»을 만들고(자식 «프로세스» — `IsolatedWork` spawn ·
> MCP `stdio_client` · 직접 부른 `subprocess` — «또는» 자기가 직접 띄운 «스레드») 그 진행을
> 초 단위 실시간 창으로 잰다.** 「프로세스」로만 적혀 있던 동안 `test_meeting_rooms` 의
> `test_expired_replay_waits_for_the_live_room_sync_before_recovery`(스레드 둘 · `release.wait(5)`)
> 가 마커 없이 병렬 패스에 남아 `make verify` 두 회차를 다 깼다.
>
> 이 판이 적었던 문장(기록으로 남긴다):
> **한 테스트가 자기 안에서 진짜 자식 프로세스를 띄운다** — 자료·보고서 워커의 `IsolatedWork` spawn,
> MCP `stdio_client`, 직접 부른 `subprocess` — **그리고 그 자식의 진행을 lease·heartbeat·SQLite
> 트랜잭션이라는 초 단위 실시간 창으로 잰다.**

`-n auto`(= 코어 11) 가 되면 「11 xdist 워커 × 각자의 자식」이 그 창보다 큰 스케줄 지터를 만든다.
앞 판의 원인 규명(phase0-report.md §0·§1)과 같은 문장이고, **달라진 것은 「material 파일 둘」이 아니라
「자식을 띄우는가」가 부류를 정의한다는 점**이다.

기계로 셀 수 있게 줄이면 문장의 앞 절이 곧 규칙이다: **자식 프로세스를 띄우면 그 부류다.**
뒤 절(실시간 창)은 왜 흔들리는지의 설명이고, 정적으로 셀 수 없으므로 규칙에 쓰지 않았다 —
그래서 규칙은 의도적으로 **조금 넓다**(예: `git init` 을 띄우는 `test_material_corpus_profile`).
넓은 쪽이 새지 않고, 값은 초 단위다.

### 앞 판 지시서의 단서가 가리킨 곳

`grep -rln "IsolatedWork\|isolated_work\|spawn\|stdio_client\|subprocess" tests/contract/` 이 내는 9개에
깨진 넷 중 셋이 없던 이유: 그 셋은 **`test_material_search._stack` / `test_report_material_search._stack`
을 import 해서** 자료 워커를 세운다. spawn 은 제품 코드(`bootstrap/material_worker.py:124` ·
`bootstrap/report_worker.py:91`) 안에 있고, 테스트는 `worker.run_once()` 한 줄로 그 문을 지난다.
**그래서 이름·grep 으로는 셀 수 없다 — 실행해서 세야 한다.**

### 기준이 깨진 넷 + 앞의 둘을 전부 포함하는가 — 실측으로 확인했다

임시 pytest 플러그인으로 `multiprocessing.BaseProcess.start` 와 `subprocess.Popen.__init__` 를 감싸
**어느 테스트가 실제로 자식을 띄우는지 기록**했다(후보 33파일 · 301건 · `-n2` · 74초).
코디가 적은 깨진 넷과, 기준선이 지목한 앞의 둘에서 실패했던 세 건 — **일곱 모두 기록됐다**:

| 실패한 건 | 띄우는 문 |
|---|---|
| `test_material_search_owners::test_request_comment_and_submission_files_are_searchable_without_a_task` | `multiprocessing:SpawnProcess` |
| `test_report_material_search::test_report_discovery_is_not_limited_to_recent_ui_reports_and_keeps_long_body_tail` | `multiprocessing:SpawnProcess` |
| `test_material_folders::test_personal_and_team_folder_uploads_search_without_tasks_and_open_through_their_owner` | `multiprocessing:SpawnProcess` |
| `test_mcp_action_items::test_stdio_client_runs_the_ledger_and_keeps_it_bound_to_the_server_persona` | `subprocess.Popen` |
| `test_material_search::test_when_a_material_was_registered_is_a_different_question_from_what_it_says` | `multiprocessing:SpawnProcess` |
| `test_material_worker_recovery::test_stage_timeout_fences_the_late_parser_result` | `multiprocessing:SpawnProcess` |
| `test_material_worker_recovery::test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it` | `multiprocessing:SpawnProcess` |

전체 기록은 **25파일 116건**이었다. 그 116건이 지금 마커를 달고 있고, 위 일곱은 `-m serial` 선택에
**7/7** 들어온다.

---

## 1. 목록이 아니라 **마커 + 걸개**로 갔다

세 조각이 함께 닫는다. 목록은 어디에도 없다 — `Makefile` 에 테스트 파일 이름이 한 줄도 없다
(그것 자체를 architecture 테스트가 지킨다).

### ① 마커 — `@pytest.mark.serial`

`pyproject.toml` 의 `markers` 에 기준과 함께 등록했다. 116건 중
**전부 또는 대부분이 자식을 띄우는 파일(14개)은 `pytestmark = pytest.mark.serial`** 로 파일째,
**소수만 띄우는 파일(11개)은 그 테스트에만** 달았다 — `test_mcp_action_items`(5/26) ·
`test_product_operations`(3/21) · `test_meeting_materials`(3/13) · `test_answer_resources`(1/14) 등의
나머지는 병렬 패스에 남는다.

### ② 가르기 — `Makefile` 이 `-m` 으로 (파일 이름 대신)

```make
DEFAULT_DESELECT = not integration and not release and not scale
PARALLEL_MARKERS = $(DEFAULT_DESELECT) and not serial
SERIAL_MARKERS   = serial and $(DEFAULT_DESELECT)

test:            pytest -n auto --dist worksteal -m "$(PARALLEL_MARKERS)"  →  $(MAKE) test-serial
test-contract:   pytest tests/contract -n auto … -m "$(PARALLEL_MARKERS)" →  $(MAKE) test-serial SERIAL_PATHS=tests/contract
test-serial:     pytest $(SERIAL_PATHS) -m "$(SERIAL_MARKERS)" -n0        (필터가 다 걸러 5 가 나면 그것만 삼킨다)
```

`test-material-serial` → **`test-serial`** 로 이름을 바꿨다(더 이상 material 만의 일이 아니다).
`-m` 은 `addopts` 를 **덮으므로** 기본 제외(integration·release·scale)를 두 식에 다시 적었다 —
이 함정은 architecture 테스트가 따로 지킨다.

### ③ 걸개 — `tests/conftest.py` (새 테스트가 조용히 새지 않게)

autouse fixture 가 **병렬 패스(xdist 워커) 안에서만** `BaseProcess.start` 와 `Popen.__init__` 를 감싼다.
마커 없는 테스트가 자식을 띄우려 하면 **흔들리는 대신 즉시·결정적으로** 실패하고, 무엇을 달아야
하는지 문장으로 말한다. `-n0`·직접 실행·직렬 패스에서는 아무것도 막지 않는다.

**걸개가 실제로 무는지 세 방향으로 쟀다**(임시 probe 파일, 측정 뒤 삭제):

| 어떻게 | 결과 |
|---|---|
| `-n2`, 마커 없이 `subprocess.run` | **1 failed** — “`subprocess.Popen` 로 자식 프로세스를 띄우는 테스트가 병렬 패스에서 돌았다 … `@pytest.mark.serial` 을 달아라” |
| `-n0`, 마커 없이 | **1 passed** (막지 않는다) |
| `-n2`, 마커 달고 | **1 passed** |

그래서 **새 테스트는 자동으로 옳은 쪽에 선다**: 마커를 달면 직렬 패스가 집어 들고, 안 달고 자식을
띄우면 병렬 패스가 첫 회차에 빨갛게 말한다(흔들림이 아니라 결정적 실패다).

### ④ `test_serial_test_targets.py` — 기준에 맞게 다시 썼다

파일 이름 목록을 지키던 4건을 버리고, **가르기가 성립하는지**를 지키는 8건으로 바꿨다:
마커 등록 · 병렬 패스가 `not serial` 로 빼는가 · 직렬 패스가 `-m serial` 만 `-n0` 로 드는가 ·
**두 식이 기본 제외를 잃지 않는가**(`-m` 이 addopts 를 덮는 함정) · 병렬 타겟이 직렬 패스를 이어
부르는가 · **타겟 recipe 에 `tests/*.py` 이름이 없는가**(목록으로 돌아가면 또 샌다) ·
걸개가 두 문을 다 보는가 · `verify` 가 여전히 `test` 를 지나는가. → **8 passed**.

---

## 2. 좁은 집합 5회 — 격리 전/후

집합은 **깨진 넷 + 앞의 둘**(68건). 앞 판의 28초 재현자를 그 여섯으로 넓힌 것이다.

### 전 (`-n auto --dist worksteal`, 마커 없음) — **5회 중 2회 빨강**

| 회차 | load | 결과 |
|---|---|---|
| 1 | 10.1 | **exit 1** · 1 failed 67 passed (41s) — `test_material_worker_recovery::test_stage_timeout_fences_the_late_parser_result` |
| 2 | 18.5 | exit 0 · 68 passed (43s) |
| 3 | 16.3 | exit 0 · 68 passed (50s) |
| 4 | 18.6 | **exit 1** · 1 failed 67 passed (43s) — 같은 건 |
| 5 | 18.3 | exit 0 · 68 passed (41s) |

(같은 시각 두 파일만 `-n auto` 로 돌린 회차는 **3 failed / 17 passed** 로 앞 판의 28초 재현자를 그대로 재현했다.
여섯 파일로 넓히면 창이 겹치는 빈도가 낮아져 2/5 로 나온다 — 경합 창이지 결정적 실패가 아니라는 §앞판 결론과 같다.)

### 후 — 두 패스를 **각각** 5회, 전부 초록

| 패스 | 선택 | 회차 | 결과 |
|---|---|---|---|
| 병렬 | `-m "… and not serial"` · `-n auto` | 5/5 | **exit 0** · 21 passed (8.6~9.1s) — 걸개 침묵 |
| 직렬 | `-m "serial and …"` · `-n0` | 5/5 | **exit 0** · 47 passed · 21 deselected (101~111s) |

**21 + 47 = 68** — 여섯 파일에서 잃은 것도, 두 번 도는 것도 없다.

## 3. 수집 수 — 잃은 것 0, 두 번 도는 것 0

```
가르기 전 (addopts 그대로) : 1562 / 1679  (117 deselected)
병렬 패스 (-m … not serial): 1435 / 1679  (244 deselected)
직렬 패스 (-m serial …)    :  127 / 1679  (1552 deselected)     1435 + 127 = 1562 ✓
```

직렬 패스 127건은 spawn 116건 + 파일째 마커를 단 파일의 이웃 11건이다.

## 4. 내가 돌린 것 · 남은 것

| 무엇 | 결과 |
|---|---|
| `make test-serial` (직렬 패스 전체, `-n0`) | **127 passed · 1552 deselected · exit 0** · 269s (4:29) |
| `make test-unit` (`tests/unit`+`tests/architecture`) | **380 passed · 1 deselected · exit 0** · 11s |
| `tests/unit`+`tests/architecture` 를 **병렬 선택 · `-n4`** 로 (걸개 활성) | **379 passed · exit 0** — 걸개 침묵 |
| 후보 33파일의 **병렬 선택 · `-n auto`** (걸개 활성) | **174 passed · exit 0** · 22s — 마커 없는 자식 spawn **0건** |
| `PYTEST_ADDOPTS='-k "demo_work_seed or reset_demo"' make test-serial` | 1683 deselected → **exit 0** (5 만 삼킨다) |

**남은 것은 전체 1회다 — 코디에게 넘긴다.** `make verify`(또는 `make test`) 한 번.
부하 제약(사용자 브라우저 E2E · 메모리) 때문에 11 워커 × 12분 을 이 세션에서 돌리지 않았다.

**넘길 때 알아 둘 것:** 혹시 내가 감사하지 않은 파일에 마커 없는 spawn 이 남아 있으면, 그것은
**흔들림이 아니라 결정적 실패**로 나오고 메시지가 고칠 자리를 말한다(마커 한 줄). 그럴 확률은 낮다 —
`tests/` 전체에서 자식으로 가는 문을 이름으로 전수 조사했고(`subprocess`·`multiprocessing`·`Popen`·
`os.fork`·`ProcessPoolExecutor`·`pexpect`·`docker`·`stdio_client`·`IsolatedWork`·두 Worker 클래스),
제품 쪽 spawn 자리는 셋뿐이며(`isolated_work` · `codex_cli`/`claude_cli`/`cli_process`),
그 문을 지나는 테스트 모듈과 **그 helper 를 import 하는 모듈까지** 모두 감사 집합에 들어 있었다.

**직렬 패스가 46초 → 269초로 늘었다**(20건 → 127건). `make verify` 의 임계 경로가 그만큼 늘지만
병렬 패스에서 그 127건(가장 느린 쪽)이 빠지므로 순증은 그보다 작다. 직렬 패스를 `-n2` 로 올리면
반으로 줄 수 있고 앞 판이 `-n2`·`-n4` 를 초록으로 쟀지만, **127건 선택으로는 재지 않았으므로
단정하지 않는다** — `-n0` 쪽에만 근거가 있어서 `-n0` 를 실었다.

## 5. 바꾼 것

| 파일 | 무엇 |
|---|---|
| `Makefile` | `DEFAULT_DESELECT`·`PARALLEL_MARKERS`·`SERIAL_MARKERS` 신설, `test`·`test-contract` 를 `-m` 로 가르고, `test-material-serial` → **`test-serial`**(`SERIAL_PATHS` 로 범위 받음). 파일 이름 목록(`MATERIAL_SERIAL_TESTS`) **삭제** |
| `backend/pyproject.toml` | `serial` 마커 등록(기준을 한 줄로 적었다) |
| `backend/tests/conftest.py` | **걸개 신설** — 병렬 패스에서 마커 없는 자식 spawn 을 즉시 실패시킨다. 기준 문장과 근거 문서를 주석으로 |
| `backend/tests/architecture/test_serial_test_targets.py` | 파일 목록 검사 4건 → **가르기 검사 8건** |
| 테스트 25파일 | `pytestmark = pytest.mark.serial`(14파일) 또는 `@pytest.mark.serial`(11파일, 26건). `test_material_search.py`·`test_material_worker_recovery.py` 의 docstring 을 마커 기준으로 고쳤다 |
| `README.md` · `AGENTS.md` | 두 패스의 정의를 「파일 목록」에서 「기준 + 마커 + 걸개」로 다시 적었다 |

**제품 코드 0줄.** `frontend/` 0건 · `modules/work/projects.py`·`task_projection.py` 0건 ·
`bootstrap/demo_work.py` 0건 · `make reset-demo` 실행 0회 · 서버·API 기동/종료 0회 · 커밋·push 0건.
사용자의 `127.0.0.1:8100`·`localhost:5173` 는 건드리지 않았다.

`git status`: 이 판이 손댄 것은 `Makefile` · `README.md` · `AGENTS.md` · `backend/pyproject.toml` ·
`backend/tests/**`(conftest · architecture 1 · contract 24 · architecture/test_protected_build 1)뿐이고,
나머지 modified/untracked 는 앞 판들의 것이다(`src/**` · `frontend/**` · `docs/**`).

## 6. 남은 자리 (고치지 않았다)

- **근본 원인은 여전히 제품 코드에 있다.** lease·heartbeat 를 실시간 시계 대신 주입 시계로 재면
  이 부류는 병렬에서도 안전해진다(`bootstrap/material_worker.py` · `platform/durable_jobs.py`).
  그때는 그 테스트들의 마커를 떼면 된다 — 마커가 기준을 적어 두었으므로 어디를 떼야 하는지 남는다.
- `platform/persistence.py` 의 SQLite 엔진에 WAL·`busy_timeout` 이 없다(phase0-report §1 검증 ①).
  자식 둘이 같은 per-test 파일에서 부딪히는 자리다. 이것도 제품 코드라 손대지 않았다.
- **integration(PostgreSQL) 쪽 spawn 은 마커를 달지 않았다** — `make test-postgres` 는 xdist 없이
  `-m integration` 으로 돌므로 걸개가 울지 않고 흔들릴 이유도 없다. 누가 그 패스를 병렬로 돌리면
  그때 걸개가 말해 줄 것이다.
