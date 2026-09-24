# Phase 0 — `material_*` 계열의 병렬 격리 (원인 규명 → 수단 → `make verify` 계약)

**이것은 조사가 절반이다. 원인이 아직 규명되지 않았다** — 「다음에 볼 자리」는 **가설**이지 답이 아니다.
가설을 검증하지 않고 수단부터 적용하지 마라.

## 읽을 것 — 순서대로

1. `orchestration/work/strong-hajin-projects/flaky-baseline-projects.md`
   ← **이번 판의 기준선.** 회차 0~4 수치와 들고 난 파일이 있다. **§0 의 정정을 반드시 읽어라**
2. `reference/2026-09-21-strong-hajin-calendar/material-parallel-isolation.md`
   ← 캘린더 작업의 관측. **⚠ 그 문서가 「`-p no:randomly` 직렬로 44 passed」라고 적는데
   이 저장소에 `pytest-randomly` 가 설치돼 있지 않다. 그 플래그는 무동작이었다.**
   **그러므로 그 문서의 「직렬 증명」은 전제를 다시 재야 한다** — 실제로 직렬화한 것이
   무엇이었는지(아마 `-n0` 이거나, 아니면 아무것도 아니었다)부터 확인하라
3. `orchestration/work/_archive/strong-hajin/strong-hajin-calendar/flaky-baseline-evidence.md`
   (있으면) · `review-be-report.md` · `be-fix-report.md` 의 테스트 수치 절

## 관측 (지금까지 쌓인 것)

| 회차 | 결과 | 상황 |
|---|---|---|
| 캘린더 착수 전 | 1078 / **2f** | 이 문제는 **그 작업 전부터 있었다** |
| 이번 판 착수 전 | 1158 / **2f** | `test_material_worker_recovery.py` |
| 이번 판 최종 | 1183 / **1f** | 기준선 밖 실패 0 |
| BE 재수정 회차 | 1181 / **4f** | `test_material_search` 가 **처음 들었다**. 스위트 **283s→384s**, **FE 워커가 동시에 돌았다** |

- **실패 단언이 전부 「워커가 아직 안 갔다」류의 시간 단언**이다 (`['failed','running']` vs `['failed','completed']`)
- **그 파일들만 `-n0` 로 돌리면 통과한다** (5 passed / 20 passed — 회차마다 확인됨)
- **부하가 오르면 흔들리는 범위가 넓어진다**는 정황이 이번에 하나 더 쌓였다

## 할 일 — 세 단계. **순서를 지켜라**

### 1단계. 원인 규명 — **무엇을 두고 다투는가**

가설들을 **하나씩 검증**하고 **버린 가설도 기록**하라.

- **무엇이 공유되나** — 파일? DB? **시계?** `durable_jobs` 원장과 lease 시각이 후보다
- **정말 「병렬」이 원인인가, 「부하」가 원인인가** — `-n2`·`-n4`·`-n auto` 로 **워커 수를 바꿔 가며** 재라.
  워커 수가 아니라 기계 부하에 반응하면 **격리 수단이 달라진다**
- **시간 단언이 무엇을 기다리나** — 폴링인가 sleep 인가 타임아웃인가.
  **실시간 시계에 매달려 있으면** 그것이 원인이다
- 같은 파일 안에서 **어느 건이 넘어지는지가 회차마다 바뀌는** 이유

**이 단계의 산출물은 「원인은 X 다, 근거는 Y」 한 문단**이다. 못 찾으면 **「못 찾았다 + 이렇게 찾아봤다」**로 적어라. 지어내지 마라.

### 2단계. 격리 수단 — **원인에 맞는 것으로**

규명된 원인에 따라 고른다. **원인 없이 고르지 마라.**

- `pytest-xdist` 의 `--dist loadgroup` + `@pytest.mark.xdist_group` 으로 그 계열을 **한 워커에 묶기**
- 그 계열만 **직렬 마커**
- **lease/timeout 을 실시간이 아니라 주입 시계로** 바꾸기 ← 근본 수단이지만 제품 코드를 건드린다
- 단언이 기다리는 **폴링 간격·타임아웃을 넉넉하게** ← 증상 완화지 치료는 아니다. 이걸 고를 거면 그렇게 적어라

**제품 코드를 건드릴 거면 먼저 그 사실을 리포트에 적고, 테스트만으로 닫히는 길이 있는지 먼저 보라.**

### 3단계. `make verify` 의 계약

지금 `verify` 는 `test test-scale test-release frontend-test frontend-assets frontend-build` 를 묶고
**한 명령이 전부를 돌린다.** 그 계열이 흔들리면 **초록을 못 본다.**

- 그 계열만 갈라 도는 타겟이 필요한지 판단하고, 필요하면 **만들어라**
- `make verify` 가 **exit 0 를 낼 수 있게** 되는 것이 이 Phase 의 완료 조건이다
- 이미 있는 `test-contract-serial`(`Makefile:49-50`)을 보라 — 이번 판이 만든 타겟이다

## 검증

- **`make verify` 가 exit 0** — 이것이 완료 조건이다. 못 하면 **왜 못 했는지**와 **어디까지 갔는지**
- 격리 전/후를 **같은 방식으로 여러 회차** 재서 비교하라. **1회 초록은 증거가 아니다** —
  이 문제는 회차마다 결과가 바뀐다. **최소 5회** 돌려 전부 초록인 것을 보여라
- 제품 코드를 건드렸으면 **그 변경이 실제 동작을 바꾸지 않는다**는 근거를 대라

## 하지 말 것

- **「프로젝트」 화면 관련 코드를 건드리지 마라** — `frontend/`, `modules/work/projects.py`,
  `task_projection.py` 등. **사용자가 지금 그걸로 브라우저 E2E 중**이다
- **`bootstrap/demo_work.py` 를 건드리지 마라** — 방금 넣은 데모 데이터가 거기 있다
- **`make reset-demo` 를 돌리지 마라** — 사용자의 데모 DB 가 날아간다
- **서버·API 를 띄우지 마라.** 사용자 포트·프로세스 금지
- **커밋·push 금지**

## 역할·맥락

너는 **strong-hajin `backend` 워커**다. 먼저 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `.md`)
- 코드 레포 `AGENTS.md`

워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
리포트: `orchestration/work/strong-hajin-projects/phase0-report.md`

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_2b88657d-8e86-4743-b205-8dd7b461da2d \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: Phase 0 material 격리" \
  --body "원인(근거) / 버린 가설 / 고른 수단과 이유 / make verify exit / 회차별 수치 / 제품 코드 변경 유무 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] backend 완료 — Phase 0. 상세는 인박스." --enter
```
