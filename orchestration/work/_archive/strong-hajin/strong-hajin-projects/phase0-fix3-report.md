# Phase 0 정정 결과 — 기준을 「프로세스」에서 「동시성」으로 넓혔다

**상태: done** · 2026-09-22 · strong-hajin `backend` 워커 · task `task_fd310bb11d9b`
워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`, 브랜치 `kknaksss/strong-hajin-projects`, **커밋 0건**.
기기: Apple 11 core / 18GB (load average 4.9~11.1). **제품 코드 0줄.** 백그라운드 루프 0건.
전체 스위트는 **실측 1회 + 완료 조건 2회, 모두 3회**만 돌렸다.

---

## 0. 기준 — **한 문장** (이것이 새 정본이다)

> **한 테스트가 자기 안에서 «진짜 동시성»을 만들고 — 자식 «프로세스»(자료·보고서 워커의
> `IsolatedWork` spawn · MCP `stdio_client` · 직접 부른 `subprocess`) «또는» 자기가 직접 띄운
> «스레드» — 그 진행을 «초 단위 실시간 창»으로 잰다.**

`-n auto`(= 코어 11) 가 되면 「워커 수 × 각자가 만든 동시성」이 그 창보다 큰 스케줄 지터를 만든다.
**무엇으로 동시성을 만들었는지는 원인의 본질이 아니다** — Phase 0 리포트가 이미 그렇게 적었고
(「초 단위 실시간 창을 재는데 워커 수가 코어 수에 닿으면 그 창보다 큰 지터가 생긴다」), 그 판이
기준을 「자식 프로세스」라는 **글자**로 좁혔을 뿐이다.

그 좁음이 낸 값이 이번 실패다: `test_meeting_rooms.py::test_expired_replay_waits_for_the_live_room_sync_before_recovery`
는 `Event`·`Lock` 으로 스레드 둘을 돌리고 `release.wait(5)`·`entered.wait(2)`·`first_done.wait(5)` 로
초 단위 창을 재는데, 기준이 프로세스였으므로 마커가 안 붙었고 `conftest` 걸개도 프로세스만 봐서
**조용히 병렬 패스에 남아 `make verify` 두 회차를 다 깼다**(단독으로 돌리면 통과한다).

**이 문장을 적은 곳**: `AGENTS.md` 「테스트」 · `README.md` 「검증」 · `Makefile` 가르기 주석 ·
`backend/pyproject.toml` 의 `serial` 마커 설명 · `backend/tests/conftest.py` 걸개 주석 ·
`backend/tests/architecture/test_serial_test_targets.py` docstring.
`phase0-report.md` §0 과 `phase0-followup-report.md` §0 에는 **정정 표시와 새 문장으로 가는 포인터**를
달았다(옛 문장은 기록으로 남겼다 — 그 판이 무엇을 재고 무엇을 적었는지가 근거이기 때문이다).

---

## 1. 대상을 **세어서** 찾았다 — 이름 열거가 아니라

코디의 grep 표(`test_meeting_rooms` 4 · `test_conversation_lifecycle` 3 · `test_meeting_stream` 3 ·
`test_report_worker` 1)를 **믿지 않고 다시 쟀다.** Phase 0 이 `BaseProcess.start`·`Popen.__init__` 를
감쌌던 것과 같은 방식으로, **임시 pytest 플러그인이 `threading.Thread.start` 와
`ThreadPoolExecutor.submit` 을 감싸 호출 스택째 기록**했다(측정 뒤 삭제).

### 두 번 쟀다

| 언제 | 범위 | 결과 |
|---|---|---|
| 좁게 | 후보 6파일 111건 · `-n2` · 40.6s | 스레드 기동 **683회** — 테스트 직접 **3회** |
| 넓게 | **병렬 선택 전체** 1447건 · `-n auto` · 436s | 기동 **11,788회** — 테스트 직접 **5회** |

넓은 판이 필요했던 이유: 스레드는 프로세스와 달리 **라이브러리 내부가 늘 쓴다.** 오탐을 막으려면
「멀쩡한 쪽이 실제로 어떻게 생겼는지」를 알아야 했다.

### 11,788회의 정체 — **테스트가 직접 만든 것은 5회뿐이다**

| 누가 띄우나 | 회수 | 무엇 |
|---|---:|---|
| **라이브러리 내부** | **11,598** | anyio 11,405(`TestClient` 의 blocking portal 5,627 · `run_sync_in_worker_thread` 의 worker thread 5,778) · asyncio 기본 executor 와 `concurrent.futures` 내부 193 |
| **제품 백그라운드** | **185** | `modules/meetings/batch_service.py` 의 `_spawn` 157 · `_arm_timer` 의 `threading.Timer` 28 |
| **테스트 코드가 직접** | **5** | 아래 3건 |

### 고른 셋 — 둘 다(동시성 + 초 단위 창)를 만족한다

| 건 | 무엇으로 동시성을 만드나 | 무엇을 초 단위로 재나 |
|---|---|---|
| `test_meeting_rooms::test_expired_replay_waits_for_the_live_room_sync_before_recovery` | `Thread` 둘(`approve`·`replay`) + `Event`·`Lock` | `release.wait(5)` · `entered.wait(2)` · `first_done.wait(5)` · `replay_done.wait(5)` |
| `test_conversation_lifecycle::test_cancelling_a_turn_keeps_what_was_said_and_ignores_what_came_after` | `Thread(target=lambda: asyncio.run(worker.run_once()))` | `release.wait(timeout=10)` · `running.join(timeout=15)` · 50×0.1s 폴링 |
| `test_material_integrity::test_pdf_warnings_do_not_contaminate_another_workers_document` | `ThreadPoolExecutor(max_workers=2)` + `Barrier` | `barrier.wait(timeout=5)` ×2 |

**코디의 표와 갈린 지점 둘 — 실측이 갈랐다.**

- **`test_meeting_stream`(3) 은 들어오지 않았다.** 그 파일이 쓰는 `Event`·`wait`·`sleep` 은 전부
  **`asyncio` 쪽**(`asyncio.Event` · `asyncio.sleep`)이고 스레드가 아니다. 이 파일에서 실제로 도는
  스레드는 **제품이 띄우는 회의 배치 백그라운드**(`batch_service._spawn`)이고, 테스트는 그것을
  기다리지 않는다. 같은 스레드를 띄우는 테스트가 **14파일 126건**인데 그 126건은 이번 실측 회차에서
  **전부 초록**이었다(기준선 5회차에도 한 번도 든 적이 없다). 그래서 넣지 않았다 — 근거 없이 넣으면
  직렬 패스만 무거워진다.
- **`test_conversation_lifecycle` 은 3건이 아니라 1건이다.** 나머지 둘은
  `time.sleep(1.1)` 폴링(재시도 backoff)으로, **동시성을 만들지 않는다.** 그 파일이 기준선에서
  흔들렸던 이유는 스레드를 쓰는 그 1건이다 — reference 문서가 이 파일을 지목한 것은 맞았고,
  **파일이 아니라 그 안의 한 건**이 부류에 든다.
- **`test_material_integrity`(단위 테스트)가 새로 들어왔다.** grep 표에 없던 건이다 —
  `threading` 을 import 하지 않고 `concurrent.futures` 로 스레드를 만든다. **이름으로는 셀 수 없고,
  실행해서 세야 한다**는 Phase 0 의 교훈이 스레드에서도 같았다.

---

## 2. 걸개를 넓혔다 — 그리고 **오탐을 어떻게 막았는지**

`backend/tests/conftest.py` 의 autouse 걸개가 이제 **문 넷**을 본다(병렬 패스 = xdist 워커 안에서만,
`serial` 마커가 없을 때만):

| 문 | 판정 |
|---|---|
| `multiprocessing.BaseProcess.start` | 무조건 (전과 같다) |
| `subprocess.Popen.__init__` | 무조건 (전과 같다) |
| **`threading.Thread.start`** | **테스트 코드가 직접 띄웠을 때만** |
| **`concurrent.futures.ThreadPoolExecutor.submit`** | **테스트 코드가 직접 불렀을 때만** |

### 「테스트 코드가 직접」의 판정 방법 — **두 가지 중 하나면 문다**

1. **`start()`/`submit()` 을 부른 «바로 그» 프레임**(`sys._getframe`)의 파일이 `backend/tests/` 안인가
2. 그 스레드가 **실행할 함수**(`Thread._target` · `type(self).run` · `submit(fn)`)가 `backend/tests/` 안에 정의됐는가

**왜 「바로 그 프레임」인가**: 스택 전체를 보면 `TestClient` 를 쓰는 **모든** 테스트가 걸린다
(테스트 → TestClient → anyio → `Thread.start`). anyio·asyncio 내부는 1·2 어느 쪽도 아니므로 조용하다.
제품이 스스로 띄우는 백그라운드 스레드(`batch_service`)도 1·2 어느 쪽도 아니라 잡히지 않는다 — §1 의
근거로 의도한 경계다.

⚠ **측정 중에 실제로 밟은 함정 하나**: 처음엔 「호출자 프레임」을 `sys._getframe(depth)` 로 잡았는데
그 프레임이 **걸개 자신**(= `backend/tests/conftest.py`, 즉 `tests/` 안)이라 **모든 스레드가 걸렸다**
— probe 에서 `TestClient` 와 `asyncio.to_thread` 가 빨갛게 나와 바로 드러났고, 헬퍼가 자기 프레임
한 칸을 더하도록 고쳤다. 이 함정을 주석에 남겼다.

### 걸개를 **다섯 방향으로 쟀다** (임시 probe 파일, 측정 뒤 삭제)

| 어떻게 | 결과 |
|---|---|
| `-n2`, 마커 없이 테스트가 `Thread.start` | **1 failed** — 「threading.Thread 로 **스레드를 띄우는** 테스트가 병렬 패스에서 돌았다 … `@pytest.mark.serial` 을 달아라」 |
| `-n2`, 마커 없이 테스트가 `ThreadPoolExecutor.submit` | **1 failed** (같은 문장) |
| `-n2`, 마커 달고 스레드 | **1 passed** |
| `-n2`, `TestClient` 로 요청 (anyio blocking portal) | **1 passed** — **오탐 없음** |
| `-n2`, `asyncio.to_thread` (asyncio 기본 executor) | **1 passed** — **오탐 없음** |
| `-n0`, 마커 없이 전부 | **5 passed** — 직렬·단독 실행은 막지 않는다 (전과 같다) |

**전체 스위트에서 걸개 때문에 빨개진 것 0건** — `make verify` 두 회차의 병렬 패스 1445건이 모두
초록이다(§4).

---

## 3. `test_serial_test_targets.py` 를 새 기준에 맞췄다

8건 → **9건**. 고친 것과 더한 것:

- `test_the_serial_marker_is_registered_with_the_widened_reason` — 마커 설명에
  `child process` **와** `thread` **와** `wall clock` 이 모두 있어야 한다. 「프로세스」로만 적힌 기준이
  이번 실패를 만들었으므로, **그 좁아짐 자체를 테스트가 막는다.**
- `test_the_runtime_guard_watches_every_door_into_real_concurrency` — 문 둘 → **넷**
  (`BaseProcess.start` · `Popen.__init__` · `Thread.start` · `ThreadPoolExecutor.submit`).
- **신규** `test_the_thread_door_only_bites_what_the_test_itself_started` — 걸개가 판정 둘
  (`_called_from_test_code` · `_defined_in_test_code`)과 `_TESTS_ROOT` 경계를 갖고 있는지, 그리고
  스레드 문이 **「바로 그 프레임」(`_called_from_test_code(1)`)** 을 보는지. 누가 이걸 「스택 전체」로
  바꾸면 TestClient 쓰는 테스트가 다 빨개지는데, **그 회귀를 이 테스트가 먼저 잡는다.**

나머지 6건(가르기·기본 제외·이어 부르기·파일 이름 금지·`verify` 경로)은 그대로다. → **9 passed**.

---

## 4. 검증 — **`make verify` 두 회차 연속 exit 0**

| 회차 | 병렬 패스 | 직렬 패스 | scale | release | frontend | **exit** |
|---|---|---|---|---|---|---|
| **1** | **1445 passed** (242.2s) | **130 passed** · 1562 deselected (290.3s) | 13 passed | 1 passed | 1016 passed (70 files) · assets · build | **0** |
| **2** | **1445 passed** (290.5s) | **130 passed** · 1562 deselected (263.9s) | 13 passed | 1 passed | 1016 passed (70 files) · assets · build | **0** |

깨졌던 `test_expired_replay_waits_for_the_live_room_sync_before_recovery` 는 두 회차 모두
**직렬 패스에서 통과**했다.

### 수집 수 — 잃은 것 0, 두 번 도는 것 0

```
가르기 전 (addopts 그대로)      : 1575 / 1692  (117 deselected)
병렬 패스 (-m "… and not serial"): 1445 / 1692  (247 deselected)
직렬 패스 (-m "serial and …")    :  130 / 1692  (1562 deselected)    1445 + 130 = 1575 ✓
```

앞 판 대비 **직렬 127 → 130(+3), 병렬 1448 → 1445(−3)** — 옮긴 셋이 정확히 그 셋이고 총합은 그대로다.
(총합이 앞 판의 1562 에서 1575 로 는 것은 그 사이 다른 판이 더한 13건이다.)

직렬 패스 시간은 앞 판의 269s(127건)에서 **264~290s(130건)** 로 — 더한 셋 중 둘이 초 단위 창을
실제로 기다리는 계약인데도 회차 간 편차(±13%) 안에 있다.

---

## 5. 바꾼 것 — **제품 코드 0줄**

| 파일 | 무엇 |
|---|---|
| `backend/tests/conftest.py` | 걸개에 **스레드 문 둘** 추가 + 「테스트 코드가 직접」 판정 헬퍼 둘 · 기준 문장과 오탐 방지 근거를 주석에 |
| `backend/pyproject.toml` | `serial` 마커 설명을 넓힌 기준으로 |
| `backend/tests/architecture/test_serial_test_targets.py` | 8건 → 9건 (§3) |
| `backend/tests/contract/test_meeting_rooms.py` | `@pytest.mark.serial` 1건 + 왜인지 두 줄 |
| `backend/tests/contract/test_conversation_lifecycle.py` | `@pytest.mark.serial` 1건 + `import pytest` |
| `backend/tests/unit/test_material_integrity.py` | `@pytest.mark.serial` 1건 |
| `Makefile` | 가르기 주석의 기준 문장 (타겟·변수는 그대로) |
| `README.md` · `AGENTS.md` | 기준 서술 + 스레드 문의 오탐 방지 설명 |
| `phase0-report.md` · `phase0-followup-report.md` | §0 에 정정 표시와 새 기준으로 가는 포인터 |

`src/**` 0줄 · `frontend/**` 0줄 · `make reset-demo` 0회 · 서버 기동 0회 · 커밋·push 0건.
임시 probe(측정 플러그인 · probe 테스트 파일)는 **모두 지웠다** — `git status` 에 남은 것이 없다.

---

## 6. 손대지 않았지만 **드러난 것** (보고만 한다)

### ① 프로세스 걸개는 **백그라운드 스레드에서 못 문다**

`test_meeting_stream` 의 여러 건이 병렬 패스에서 이 경고를 낸다:

```
PytestUnhandledThreadExceptionWarning: Exception in thread Thread-5 (_guarded)
  …/platform/cli_process.py:96 in subprocess_runner → subprocess.Popen(…)
  …/tests/conftest.py:86 in popen → _refuse("subprocess.Popen")
  Failed: subprocess.Popen 로 **자식 프로세스를 띄우는** 테스트가 병렬 패스에서 돌았다 …
```

즉 **제품의 회의 배치 백그라운드 스레드가 실제로 `subprocess.Popen` 까지 간다.** 걸개는 옳게 물었지만
`pytest.fail` 이 **메인 스레드가 아니라서** 경고로 삼켜지고 테스트는 통과한다(테스트가 그 배치를
기다리지 않으므로 결과가 바뀌지 않는다).

**두 가지를 뜻한다.** ⓐ 걸개는 메인 스레드에서 부른 것만 결정적으로 실패시킬 수 있다.
ⓑ **`-n0`·직렬 패스·단독 실행에서는 걸개가 꺼져 있으므로 그 `Popen` 이 실제로 실행된다** —
`shutil.which("codex"/"claude")` 로 바이너리를 찾아 CLI 를 띄우려 한다(없으면 `ProviderUnavailable`
이 로그로 접힌다). 이 기기에 그 CLI 가 있으면 테스트가 진짜 외부 CLI 를 부르는 자리다.

**고치지 않은 이유**: ⓐ를 고치려면(스레드의 위반을 모아 teardown 에서 실패시키기) 지금 초록인
126건이 **전부 빨개진다** — 완료 조건(`make verify` 두 회차 exit 0)과 정면으로 부딪힌다.
ⓑ는 **제품 코드와 테스트 하네스의 배선**(회의 배치 provider 를 fake 로 주입하지 않는다) 문제이고
이번 판의 allowed_paths·「제품 코드 0줄」 밖이다. **다음 판의 후보로 남긴다.**

### ② 제품 백그라운드 스레드는 기준의 «뜻»에는 들어간다

`batch_service._spawn` 이 띄우는 스레드를 **테스트가 기다리고 초 단위로 재기 시작하면** 그 테스트는
부류에 든다. 지금은 아무도 기다리지 않아 넣지 않았다(§1). 걸개는 그 경우를 **잡지 못하므로**,
그때는 사람이 마커를 달아야 한다 — 기준 문장이 그 판단의 근거로 남아 있다.

### ③ 앞 판이 남긴 것은 그대로다

lease·heartbeat 를 주입 시계로 바꾸는 근본 수정, SQLite 엔진의 WAL·`busy_timeout` —
둘 다 제품 코드라 이번에도 손대지 않았다(`phase0-followup-report.md` §6).
