# Phase 0 후속 — 격리 목록이 좁다. **기준**을 찾아라

## 지금까지 (앞 판이 한 것 — 읽고 이어라)

`orchestration/work/strong-hajin-projects/phase0-report.md` (201줄). **원인 규명은 성공했다**:

> 그 파일들은 **한 테스트 안에서 진짜 자식 인터프리터를 최대 둘 띄우고 초 단위 lease 창을
> 실시간 시계로 잰다.** `-n auto`(= 코어 11) 가 되면 그 창보다 스케줄 지터가 커진다.
> `-n0`·`-n2`·`-n4` 는 전부 통과한다. 버린 가설 넷도 근거와 함께 그 리포트에 있다.

앞 판은 **`test_material_search.py` · `test_material_worker_recovery.py` 둘만** 직렬 패스로 갈랐다
(`Makefile` 의 `MATERIAL_SERIAL_TESTS`, `test-material-serial` 타겟, `tests/architecture/test_serial_test_targets.py`).

**앞 판의 터미널이 죽어서 최종 검증을 못 적었다. 코디가 대신 쟀고, 결과는 이렇다.**

## 무엇이 남았나 — `make verify` 가 **exit 2** 다

코디 실측 (2026-09-22, 12분 44초): **4 failed / 1538 passed**.
**깨진 넷은 격리한 두 파일이 아니라 같은 부류의 «다른» 파일들이다:**

```
FAILED tests/contract/test_material_search_owners.py::test_request_comment_and_submission_files_are_searchable_without_a_task
FAILED tests/contract/test_report_material_search.py::test_report_discovery_is_not_limited_to_recent_ui_reports_and_keeps_long_body_tail
FAILED tests/contract/test_material_folders.py::test_personal_and_team_folder_uploads_search_without_tasks_and_open_through_their_owner
FAILED tests/contract/test_mcp_action_items.py::test_stdio_client_runs_the_ledger_and_keeps_it_bound_to_the_server_persona
```

`test_material_search_owners` 는 **reference 문서가 원래 지목했던 파일**이다
(`reference/2026-09-21-strong-hajin-calendar/material-parallel-isolation.md` — 그 문서는
`test_material_search_owners` · `test_material_action_evidence` · `test_conversation_lifecycle` 도 든다).

## 할 일 — **파일을 하나씩 더하지 마라. 기준을 찾아라**

목록에 한 줄씩 추가하는 식으로는 **또 새는 것이 나온다.** 그래서:

1. **무엇이 이 넷(+앞의 둘)을 같은 부류로 만드나** — 기준을 한 문장으로 정의하라.
   후보: 자식 인터프리터를 띄운다 / material 워커 경로를 탄다 / `stdio` 로 프로세스를 연다 /
   초 단위 실시간 창을 잰다. **참고**: `grep -rln "IsolatedWork\|isolated_work\|spawn\|stdio_client\|subprocess" tests/contract/`
   는 **9개**를 내는데, 깨진 넷 중 **셋은 거기 없다** — 직접 spawn 하지 않고도 같은 경로를 탄다.
   그 사실이 기준을 좁히는 단서다
2. **그 기준으로 목록을 정의하라.** 이름 열거가 아니라 **마커**가 맞다면 마커로 가라
   (예: `@pytest.mark.serial` 을 그 부류에 붙이고 `-m`/`--deselect` 로 가른다).
   그러면 **새 테스트가 생겨도 자동으로 옳은 쪽에 선다**
3. **`test_serial_test_targets.py` 를 그 기준에 맞게 고쳐라** — 지금은 파일 이름 목록을 지킨다.
   마커로 가면 「마커 붙은 것이 병렬 패스에서 빠지는가」를 지켜야 한다

## ⚠ 부하 제약 — **이번엔 이게 규칙이다**

**사용자가 같은 기계에서 브라우저 E2E 를 하고 있고, 메모리가 빡빡하다.**
앞 판이 남긴 고아 프로세스(`rounds.sh` 가 `make test` 를 무한 반복)가 기계를 먹어서 코디가 죽였다.

- **전체 스위트(`make test`·`make test-contract`·`make verify`)를 반복해서 돌리지 마라.**
  한 번 돌리는 데 12분이고 xdist 워커 11개가 뜬다
- **앞 판이 만든 28초 재현자를 써라** — 깨진 넷 + 앞의 둘만 `-n auto` 로 돌리면 재현된다.
  기준 찾기와 검증을 **그 좁은 집합**에서 해라
- **백그라운드 루프를 만들지 마라.** `for` 루프로 회차를 돌릴 거면 **전경에서** 돌려서
  네가 죽으면 같이 죽게 하라. `nohup`·`&`·`disown` 금지
- **최종 확인 1회만** 전체를 돌려라 — 그것도 **코디에게 맡겨도 된다.**
  「목록/마커를 이렇게 바꿨다, 전체 확인은 코디가 해 달라」로 보고해도 된다
- 측정 전에 `sysctl -n vm.loadavg` 로 부하를 보고, **높으면 기다려라**

## 하지 말 것

- **제품 코드를 건드리지 마라** (앞 판도 안 건드렸다). 테스트 인프라·Makefile·마커까지다
- **「프로젝트」 화면 코드 금지** — `frontend/`, `modules/work/projects.py`, `task_projection.py`.
  **사용자가 그걸로 E2E 중**이다
- **`bootstrap/demo_work.py` 금지 · `make reset-demo` 금지** — 사용자의 데모 DB 가 날아간다
- **서버·API 를 띄우거나 죽이지 마라.** `127.0.0.1:8100`(API) · `localhost:5173`(FE) 는 사용자 것이다
- **커밋·push 금지**

## 검증

- 기준을 **한 문장으로** 적고, 그 기준이 **깨진 넷과 앞의 둘을 전부 포함**하는지 보여라
- **좁은 집합에서 격리 전/후를 각각 5회** 재라 (28초짜리면 5회가 3분이다)
- 전체 1회는 **코디에게 넘겨도 된다** — 넘기면 그렇게 적어라
- 수집 수가 맞는지(잃은 것·두 번 도는 것 0) 확인하라

## 역할·맥락

너는 **strong-hajin `backend` 워커**다. 먼저 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `.md`)
- 코드 레포 `AGENTS.md` · `phase0-report.md` · `flaky-baseline-projects.md`

워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
리포트: `orchestration/work/strong-hajin-projects/phase0-followup-report.md`

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_6828802a-6aa8-4b66-bddc-db3ca8707a3a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: Phase 0 후속" \
  --body "기준 한 문장 / 목록 또는 마커 / 좁은 집합 5회 결과 / 전체 1회를 코디에게 넘기나 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] backend 완료 — Phase 0 후속. 상세는 인박스." --enter
```
