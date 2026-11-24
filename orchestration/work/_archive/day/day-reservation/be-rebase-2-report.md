# day-reservation backend rebase 2: origin/dev(#271 · #273) 위로 · migration 0018 ~ 0023

## 상태: done (전체 check.sh 녹색)

브랜치 `kknaksss/day-reservation`, 부모 `b2f28990`(origin/dev). push 하지 않았다. 스택(11040 · .run)과 deploy/*.env는 건드리지 않았다.
Docker는 코디가 지시한 정형 검증 TLC 전용 컨테이너에만 썼다.

| 커밋 | 새 sha | 옛 sha |
|---|---|---|
| 1차 예약 현황 조회 | `a08f1a0b` | `431c081b` |
| 2차 예약 현황 2차 (+ 시험 등록 보충 amend) | `0328b1aa` | `68a37b87` |
| 3차 정형 검증 동기화 (새로 만든 커밋) | `85836b30` (HEAD) | — |

## 충돌 처리
- 1차 커밋
  - `tests/migrations/test_alembic.py`: `HEAD = "0018_reservation_permission"`으로 정했다.
- 2차 커밋
  - `emr/kos/__init__.py`: `class KosAdapter(KosExtReads, KosExtWrites, KosNotices, KosHospitalReads, KosSaleReads, EmrAdapter)`
    - 둘 다 살렸다.
    - 두 쪽 mixin 메서드에 겹치는 이름이 없다. `internal`은 둘 다 같은 시그니처의 Protocol stub일 뿐이다.
  - `services/emr_sync.py`: `ext_delivery`와 `reservation_companions`를 둘 다 import한다.
  - `services/default_permissions.py` docstring: 새 번호를 적었다(view = 0018 · notice = 0021 · companion = 0023).
  - `tests/migrations/test_alembic.py`: `HEAD = "0023_companion_permission"`.
  - `test_reservation_permission_migration.py`: 2차 커밋 쪽(`THIS` 변수)을 살리고 번호를 0018 / PREV `0017_ext_catalog`로 맞췄다.
- 자동 병합된 파일
  - 대상: `common/config.py` · `common/error_codes.py` · `emr/base.py` · `identifiers.py` · `models/__init__.py` · `emr/sync_references.py`
  - origin/dev에 비해 **더하기만** 있다(삭제 0, `models/__init__` docstring 한 줄만 고침). dev 쪽 내용은 그대로 남아 있다.
  - `error_codes.py`: 코드 104개 중 중복은 0개다. taut-check도 통과했다.

## 새 번호 표 (dev `0017_ext_catalog` 뒤에 붙임)
| 옛 | 새 | down_revision |
|---|---|---|
| 0017_reservation_permission | **0018_reservation_permission** (1차 커밋) | 0017_ext_catalog |
| 0018_transaction_status_more | **0019_transaction_status_more** | 0018_reservation_permission |
| 0019_purchase_task_visit_index | **0020_purchase_task_visit_index** | 0019_transaction_status_more |
| 0020_notice_permission | **0021_notice_permission** | 0020_purchase_task_visit_index |
| 0021_companion_tables | **0022_companion_tables** | 0021_notice_permission |
| 0022_companion_permission | **0023_companion_permission** | 0022_companion_tables |

- 바꾼 것: 파일 이름(git mv), revision, down_revision, docstring(Revision ID · Revises)
- 함께 고친 곳
  - migration 시험 5개: 파일 경로 · PREV · THIS · 시험 이름 · docstring
  - `test_alembic` HEAD
  - `default_permissions` docstring
  - `models/purchase.py` · `models/task.py`: 주석의 번호(0020)
- `alembic heads`: **`0023_companion_permission (head)` 하나**다.
- 옛 이름이 남은 곳: 0건. 가장 긴 revision 이름(30자)도 32자 제한 시험을 통과한다.

## 전체 check.sh에서 드러난 기존 실패 6개 (코디 지시로 고침)
첫 전체 실행 결과는 2574 passed · **6 failed**였다. 옛 `68a37b87`을 임시 worktree에 꺼내 돌려도 같은 실패가 나왔다. rebase가 만든 실패가 아니라 2차 커밋이 원래 갖고 있던 문제다.

### (a) 테이블 · 유일 인덱스 등록 빠짐 → 2차 커밋에 amend
- `test_models.py`: `COMPANION_TABLES = {"companion_group", "companion_member"}`를 더했다.
- `test_column_snapshot.py`: 두 테이블의 칸 스냅샷을 더했다.
- `test_constraints.py`: UNIQUE에 `companion_member.visit_id`를 더했다. 실제 PostgreSQL에서 같은 방문을 두 그룹에 넣으면 23505가 나는 사례다.

### (b) 정형 검증 연결 drift → maintain-day-chart-checks 절차로 갱신, 3차 커밋
- 점검 자료: `.local/verification/formal-maintenance-rebase2`(base `59d89325` → HEAD)
- 갱신 전 실행: `verification_formal` · `verification_proof`가 둘 다 `Formal storage coverage drifted: models/task.py`로 거부됐다. 이 거부도 결과로 보존했다(`.local/rebase2-pre-*.log`).
- origin/dev 자체는 연결과 일치(in sync)한다. drift는 우리 변경 3곳뿐이다.
  - `models/task.py`
    - 바뀐 것: `ix_visit_task_visit_id` 부분 인덱스(유일 아님)를 더했다.
    - 판정: **의미에 영향 없음**. 잠금 · 순번 · 이력 쓰기는 그대로다.
  - `emr/sync_references.py`
    - 바뀐 것: `EntityModel` 타입 합에 `Notice`를 더했다.
    - 판정: **의미에 영향 없음**. 차트 칸(CHART_COLUMNS · 가드)은 그대로다.
  - `queries/board.py:load_world`
    - 바뀐 것: 작업 · 호출 · 직원 읽기를 `load_tasks` · `load_calls` · `load_staff`로 그대로 옮겼다(예약 담당의 조회와 같이 쓰려고).
    - 판정: **의미에 영향 없음**. 차트 이력 읽기는 load_world에 남아 있고, 옮긴 읽기도 같은 세션 · 방문 잠금 안에서 돈다.
    - 다만 함수를 나눈 것이라 **연결 범위를 넓혔다**. `verification_binding.REQUIRED_FUNCTIONS`와 `source-map.functions`에 세 함수를 더해, 옮긴 코드가 바뀌면 다시 실패하게 했다.
- 우리 diff에 차트 상태를 새로 쓰는 경로는 없다(chart_log · note · 잠금을 grep으로 확인).
- TLA · Lean 명세는 바꾸지 않았다. 원자 단계가 같기 때문이다.
- 갱신한 것
  - `source_commit` = `0328b1aa`
  - 함수 hash: load_world를 고치고 세 함수를 새로 넣었다.
  - 저장 hash 2개
  - abstraction.Read 설명
- 갱신 뒤 실행 결과
  - TLA+ 8 조합(편집자 2 · 3명 × 초기 이력 0 · 1 × 잠금 유무), 실제 PostgreSQL HTTP 대조 포함:
    - normal은 모두 위반 없음이다. DB 응답은 [200, 409(, 409)]로 chart_conflict가 났다.
    - no-lock은 모두 `NoStaleCommit`을 검출했다. DB 응답은 [200, 200(, 200)]로, 오래된 기준의 저장이 실제로 들어갔다.
  - 상태도를 다시 생성했다: `.local/verification/rebase2-chart-statechart/index.html`
  - Lean
    - normal: 세 정리가 커널 확인을 통과했다. 의존 공리는 `propext`뿐이다.
    - inverted-guard: 세 정리가 모두 unsolvedGoals로 실패했다(검출).
  - 증거 폴더: `.local/verification/rebase2-chart-formal` · `rebase2-chart-proof`
- 분류: **updated**(bug 없음)

## 최종 전체 `./scripts/check.sh` (HEAD `85836b30`): exit 0
- 구조 · Jinja: 584 소스 통과
- ruff 통과 · format 통과 · mypy 583 파일 Success
- taut-audit · taut-check 통과
- frontend: lint · format · CSS 재현 · node 127 pass / 0 fail
- pytest(격리 PG · Redis): **2584 passed, 0 failed**
- 증거: `.local/checks/20261124-113136-53852`

## 코디가 할 것
- push · PR은 코디가 한다. 커밋은 셋이다. 3차 정형 검증 동기화 커밋의 `source_commit`은 `0328b1aa`를 가리키므로, 다시 rebase하면 그 sha를 함께 갱신해야 한다.
- migration 0018 ~ 0023은 deploy의 migrate 단계에서 적용된다.
