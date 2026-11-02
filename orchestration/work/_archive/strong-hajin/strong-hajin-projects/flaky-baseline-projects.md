# 흔들리는 테스트 기준선 — strong-hajin-projects / backend

> **내일 Phase 0 의 입력이다.** WORK-005 Phase BE-1 작업 0 이 이름 지은 그 파일이고,
> 수치의 원천은 `be-impl-report.md` §1·§2(회차 0·1·2) · `review-be-report.md` 테스트 실측(회차 3) ·
> BE 재수정 판의 재측정(회차 4, 2026-09-22)이다.
>
> 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`,
> 브랜치 `kknaksss/strong-hajin-projects`, base `e46ce39`. **커밋 0건** — 변경은 워크트리에만 있다.

## 0. 먼저 — 직렬화 플래그에 대한 정정

**`-p no:randomly` 를 쓴 회차는 한 번도 없다.** 이 저장소에 `pytest-randomly` 가 **설치돼 있지 않아**
그 플래그는 **무동작**이다(pytest 가 모르는 플러그인을 끄라는 요청은 조용히 지나간다).

**직렬화는 전부 `-n0` 였다** — `pytest-xdist` 의 `-n auto --dist worksteal` 를 끄는 스위치다.
`Makefile` 의 `test-contract-serial` 타겟도 `-n0` 하나만 쓴다(`Makefile:46-50`).

⚠ **reference 문서가 「`-p no:randomly` 로 직렬 증명을 했다」고 적었다면 그 전제는 다시 재야 한다** —
그 플래그로는 아무것도 직렬화되지 않았고, 실제로 격리를 만든 것은 `-n0` 뿐이다.

## 1. 회차별 수치 — `make test-contract` (병렬 `-n auto --dist worksteal`, 11 workers)

| 회차 | 언제 · 누가 | collected | passed | failed | 소요 | exit |
|---|---|---|---|---|---|---|
| **0** | 착수 전 (BE 기준선) | 1160 | 1158 | **2** | 301.88s | 2 |
| **1** | BE-1·BE-2 구현 뒤 (BE) | 1184 | 1182 | **2** | — | 2 |
| **2** | BE 최종 (BE) | 1184 | 1183 | **1** | — | 2 |
| **3** | 검수 재측정 (리뷰어) | 1184 | 1183 | **1** | 283.32s | 2 |
| **4** | **BE 재수정 뒤 (이번 판)** | **1185** | **1181** | **4** | **384.32s** | 2 |

- 회차 4 의 collected 가 하나 는 것은 **이번 판이 더한 계약 테스트 1건**
  (`test_the_cancel_assignment_surface_lands_in_the_one_method`) 때문이다.
- `make test-unit` 은 **369 → 372 passed · exit 0**(이번 판이 더한 단위 테스트 3건,
  `tests/unit/test_project_auto_join_flag.py`).

## 2. 회차마다 **어느 파일의 어느 건**이 넘어졌나

| 회차 | 실패한 파일 | 실패한 **건** |
|---|---|---|
| **0** | `test_material_worker_recovery.py` | `test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it` · `test_stage_timeout_fences_the_late_parser_result` |
| **1** | `test_material_worker_recovery.py` | `test_stage_timeout_fences_the_late_parser_result` |
| **1** | `test_task_fields_and_materials.py` | `test_start_sets_a_missing_start_date_to_the_seoul_business_day` — **BE 가 만든 실패였고 회차 2 전에 고쳤다** |
| **2** | `test_material_worker_recovery.py` | `test_stage_timeout_fences_the_late_parser_result` |
| **3** | `test_material_worker_recovery.py` | `test_stage_timeout_fences_the_late_parser_result` |
| **4** | `test_material_worker_recovery.py` | `test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it` · `test_stage_timeout_fences_the_late_parser_result` |
| **4** | **`test_material_search.py`** ← **회차 4 에 처음 든 파일** | `test_searching_without_naming_the_work_finds_what_this_person_may_read` · `test_when_a_material_was_registered_is_a_different_question_from_what_it_says` |

**회차 1 의 `test_task_fields_and_materials.py` 한 건만이 코드 변경이 만든 실패였다**:
상태 투영을 순수 모듈 `work/task_projection.py` 로 내리면서 그 테스트가 얼려 둔 시계
(`work_application.datetime`)가 안 닿게 됐다. 그 테스트가 `task_projection.datetime` 도 함께 얼리도록
한 줄 더해 회차 2에서 통과했다. **그 뒤로 재발 없다.**

### 회차 4 에서 흔들림이 **두 파일로 넓어졌다 — 감추지 않고 적는다**

회차 4 의 실패 넷은 **전부 「자료 파싱 워커가 아직 안 갔다」는 단언**이다:

```
test_material_search.py       : assert set() == {'남견적.md'}     # 색인이 아직 안 섰다
test_material_search.py       : assert set() == {'8월정리.md'}    # 같은 모양
test_material_worker_recovery : assert ('queued' == 'running')
test_material_worker_recovery : assert ['running','running'] == ['failed','completed']
```

**넷 다 상태 기계가 틀린 것이 아니라 아직 진행하지 않은 것**이다 — 값이 「다른 상태」가 아니라
**「이전 상태」**로 나온다. 같은 회차의 소요가 **283.32s → 384.32s 로 36% 늘었고**, 이때 같은 기기에서
**FE 워커가 동시에 돌고 있었다.** 부하가 커질수록 흔들리는 파일이 늘어나는 모양과 일치한다
(단정이 아니라 관측이다).

## 3. 직렬로 돌리면 통과한다 — **병렬에서만 넘어진다**

```
$ make test-contract-serial FILES="tests/contract/test_material_search.py tests/contract/test_material_worker_recovery.py"
   → cd backend && uv run pytest <두 파일> -n0
20 passed, 2 warnings in 46.00s          # exit 0
```

(`test_material_search.py` 15건 + `test_material_worker_recovery.py` 5건.)
검수 회차(3)도 `test_material_worker_recovery.py` 만 `-n0` 로 **5 passed · exit 0** 이었다.

**`-n0` 하나가 실효 스위치다.** 같은 파일들이 `-n auto --dist worksteal` 아래에서만 넘어지고,
직렬에서는 전부 통과하며 exit 0 이다.

→ **진단: 자료 파싱 워커의 진행을 기다리는 테스트들이 병렬 부하에서 시간 창을 놓친다.**
업무·프로젝트 경로와 공유하는 것은 DB 파일이 아니라 **프로세스 시간**이다.

## 4. 이번 판(회차 4)이 만든 실패 — **0건**

근거 넷:

1. **실패한 파일이 전부 `material_*` 계열이다.** 이번 재수정이 바꾼 여섯 파일 중
   material 경로에 닿는 것이 **0건**이다:
   `modules/work/projects.py` · `modules/work/assignments.py` · `modules/work/requests.py` ·
   `modules/work/project_results.py` · `tests/contract/test_project_membership_follows_work.py` ·
   `tests/unit/test_project_auto_join_flag.py`.
2. **직렬 격리가 통과한다** — §3, 20 passed · exit 0. 코드가 깨졌다면 직렬에서도 넘어진다.
3. **실패 단언이 전부 「아직 진행 안 함」이다** — §2. 계약이 다른 값을 내는 것이 아니라
   워커가 이전 상태에 머물러 있다.
4. **이번 판이 닿은 계약을 직렬로 다시 돌렸다** —
   `test_projects.py` · `test_project_membership_follows_work.py` · `test_project_commands.py` ·
   `test_task_assignments.py` · `test_task_predecessors.py` · `test_task_fields_and_materials.py` ·
   `test_action_center.py` → **125 passed · exit 0**(77.21s).
   그리고 `make test-unit` **372 passed · exit 0**, `make test-postgres` **103 passed · 1571 deselected · exit 0**(159.54s).

## 5. Phase 0 가 받아야 할 것

- **흔들리는 것은 「자료 파싱 워커의 진행을 기다리는 계약 테스트」다.** 오늘까지 관측된 파일은 둘:
  `tests/contract/test_material_worker_recovery.py`(5회차 내내) ·
  `tests/contract/test_material_search.py`(회차 4 에 처음). **부하가 커지면 더 늘 수 있다.**
- **병렬에서만 넘어진다.** `-n0` 이면 전부 통과하고 exit 0 이다.
- **`-p no:randomly` 는 쓰지 마라** — 미설치라 무동작이다. 직렬화 스위치는 `-n0` 뿐이고
  `make test-contract-serial FILES="…"` 이 그것을 감싼다.
- **기기 부하를 같이 기록해라.** 회차 3(283s, 실패 1) 과 회차 4(384s, 실패 4) 의 차이가 그것이다 —
  다른 워커가 같은 기기에서 도는지가 수치를 바꾼다.
- **「기준선 그대로」의 판정 기준**: `make test-contract` 의 실패가 **전부 `material_*` 파일 안**이고
  **그 파일들을 `-n0` 로 돌리면 exit 0** 이면 기준선이다. 그 밖의 파일이 한 건이라도 뜨면 새 실패다.
