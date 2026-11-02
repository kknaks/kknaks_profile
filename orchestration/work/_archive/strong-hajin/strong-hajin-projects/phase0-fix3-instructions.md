# Phase 0 정정 — 기준이 좁았다: **스레드**도 같은 부류다

**allowed_paths**: `backend/tests/` · `backend/pyproject.toml` · `Makefile`. **제품 코드 0줄.**
커밋·push 금지. 서버·개발서버 금지.

## 무엇이 드러났나 (코디 실측)

`make verify` 를 **두 회차 연속** 돌렸더니 **같은 1건이 두 번 다 실패**했다:

```
verify3: 1 failed / 1446 passed   FAILED test_meeting_rooms.py::test_expired_replay_waits_for_the_live_room_sync_before_recovery
verify4: 1 failed / 1446 passed   같은 건 (gw10)
```
**그 테스트만 단독으로 돌리면 2회 다 통과한다.**

**원인**: 그 테스트는 **`Event`·`Lock` 으로 스레드를 돌리고 «5초짜리 실시간 창»을 잰다**:
```python
assert self.release.wait(5), "the test did not release the room update"
```

**Phase 0 이 정한 기준은 「자식 «프로세스»를 띄운다」였고**, `conftest` 걸개도
`multiprocessing.BaseProcess.start` · `subprocess.Popen` **만** 본다 — **스레드는 안 본다.**
그래서 마커가 안 붙었고 `-n auto`(워커 11)에서 그 창이 스케줄 지터에 먹혔다.

**기준의 «뜻»에는 맞는데 «글자»에서 빠졌다.** Phase 0 리포트가 원인을 이렇게 적었다 —
「**초 단위 실시간 창**을 재는데 워커 수가 코어 수에 닿으면 그 창보다 큰 지터가 생긴다」.
**동시성을 무엇으로 만들었는지(프로세스냐 스레드냐)는 그 원인의 본질이 아니다.**

## 할 일

### 1. 기준을 넓혀라

지금: 「한 테스트가 자기 안에서 **진짜 자식 프로세스**를 띄운다」
→ **「한 테스트가 자기 안에서 «진짜 동시성»(자식 프로세스 «또는» 스레드)을 만들고
그 진행을 «초 단위 실시간 창»으로 잰다」**

**Phase 0 리포트·`AGENTS.md`·`README.md` 의 기준 서술을 그 문장으로 고쳐라.**

### 2. 대상을 **세어서** 찾아라 — 이름 열거가 아니라

코디가 1차로 grep 해 보니 **스레드 + 대기 호출**을 쓰는 계약 테스트가 넷이고 **셋에 마커가 없다**:

| 파일 | 대기 호출 | 마커 |
|---|---|---|
| `tests/contract/test_meeting_rooms.py` | 4 | **없음** ← 이번에 두 번 깨진 곳 |
| `tests/contract/test_conversation_lifecycle.py` | 3 | **없음** ← ⚠ **캘린더 작업의 reference 문서가 원래 지목했던 파일이다** |
| `tests/contract/test_meeting_stream.py` | 3 | **없음** |
| `tests/contract/test_report_worker.py` | 1 | 있음 |

**이 표를 믿지 말고 네가 다시 세어라.** 코디의 grep 은 거칠다(`threading|Thread(|Event()|Lock()`
× `.wait(|sleep(`). **Phase 0 이 «프로세스» 쪽에서 했던 것처럼 실측으로 골라라** —
그 판은 임시 플러그인으로 `BaseProcess.start`·`Popen.__init__` 를 감싸서 **실제로 띄우는 것**을 기록했다.
**스레드도 같은 방식이 가능하다**(`threading.Thread.start` 를 감싼다).
**「실제로 스레드를 띄우고 그 위에서 시간을 재는가」로 걸러라.**

### 3. 걸개도 넓혀라

`tests/conftest.py` 의 걸개가 지금 프로세스만 본다.
**스레드도 보게 하라** — 마커 없이 병렬 패스에서 스레드를 띄우면 **즉시·결정적으로 실패**하고
무엇을 달아야 하는지 말하게. **`-n0`·직접 실행에서는 막지 않는다**(지금과 같다).
⚠ **오탐을 조심하라** — 라이브러리 내부가 스레드를 쓰는 경우(예: httpx·anyio 내부)까지 잡으면
멀쩡한 테스트가 다 빨개진다. **테스트 코드가 «직접» 띄운 것만** 잡히게 하고, 그 판정 방법을 리포트에 적어라

### 4. `test_serial_test_targets.py` 를 새 기준에 맞춰라

지금은 프로세스 기준을 지킨다. **스레드까지 포함한 기준**을 지키게 고쳐라.

## 검증 — **이것이 완료 조건이다**

- **`make verify` 를 «두 회차» 돌려 둘 다 exit 0** 이어야 한다.
  ⚠ 한 회차 초록은 증거가 아니다 — 이 문제는 회차마다 결과가 바뀐다
- 마커를 더한 파일이 **직렬 패스에서 도는지** 확인하고, **수집 수가 맞는지**(잃은 것·두 번 도는 것 0)
- **걸개가 오탐을 안 내는지** — 전체 스위트에서 걸개 때문에 빨개진 것이 0건
- **제품 코드 0줄**

## ⚠ 부하 제약

기계에 다른 작업이 돌 수 있다. **전체 스위트를 반복해서 돌리지 마라** —
대상 파일들만 좁게 재서 기준을 정하고, **전체는 마지막 두 회차만**.
**백그라운드 루프 금지**(`nohup`·`&`·`disown`) — 앞선 판에서 고아가 기계를 먹은 적이 있다.

## 역할·맥락

너는 **strong-hajin `backend` 워커**다. 먼저 읽어라:
- `.../roles/strong-hajin/backend/role.md` (+ 같은 폴더 `.md`) · 코드 레포 `AGENTS.md`
- `phase0-report.md`(원인 규명) · `phase0-followup-report.md`(마커 도입) · `flaky-baseline-projects.md`
- `reference/2026-09-21-strong-hajin-calendar/material-parallel-isolation.md`
  (⚠ 그 문서가 `test_conversation_lifecycle` 을 **원래 지목**했다)

워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
리포트: `orchestration/work/strong-hajin-projects/phase0-fix3-report.md`

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_807867bb-ebda-4775-9019-c8487dcf6ef3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: Phase 0 기준 확장" \
  --body "새 기준 한 문장 / 실측으로 고른 대상 / 걸개 확장과 오탐 방지 / make verify 두 회차 결과 / 수집 수 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] backend 완료 — Phase 0 기준 확장. 상세는 인박스." --enter
```
