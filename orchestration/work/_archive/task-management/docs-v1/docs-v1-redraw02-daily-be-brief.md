# [backend] 업무 일정 4필드 + 「오늘 업무」 조회

너는 **task-management `backend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

> ⚠ **프론트 워커가 같은 워크트리에서 `app/front/` 를 동시에 고친다.**
> 너는 **`app/back/` 만** 건드린다. `app/front/` 를 열지도 고치지도 마라. `git status` 에 `app/front/` 가 뜨면 잘못한 것이다.
> **포트 3000 을 쓰지 마라** — 사용자가 그 주소로 화면을 보고 있다.

---

## 0. 왜 바꾸나 — 두 개가 한꺼번에 바뀐다

### ① 일정 필드가 1개에서 4개로 (정정 **A-4 번복**)

정정 A-4 가 `startDate`/`endDate` 를 `due_date` 하나로 합쳤는데 **2026-09-06 사용자 확정으로 번복됐다.**
업무는 **계획 기간**을 갖고, 실적 2개가 더해져 **일정 필드는 4개**다.

### ② 조회 단위가 월에서 일로

**「내 업무」는 오늘 업무다.** 기본 진입이 「이번 달」이 아니라 **「오늘 하루」**다.

**읽어야 할 문서** (절대경로 · read-only):
```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/10-decision/decision-002-my-tasks.md
    §「2026-09-06 일정 필드 4개 확정 — A-4 번복」
    §「2026-09-06 조회 단위 전환 — 월 → 일」
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/40-architecture/database/domains/task.md   T-1 · T-1-c · T-1-d
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/40-architecture/database/README.md          §3 schedule 파생
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/20-spec/spec-003-tasks-crud.md              §Scope · §4
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/20-spec/spec-004-tasks-status-views.md      §4 「GET /api/tasks 의 기간 조회 규칙 — 4종」
```

---

## 1. P1 — 일정 4필드

| 컬럼 | 타입 | 뜻 | 누가 쓰나 |
|---|---|---|---|
| **`start_date`** | `DATE NULL` | **계획 시작** | 사용자 (신설) |
| `due_date` | `DATE NULL` | **계획 종료 = 기한** | 사용자 (기존) |
| **`started_at`** | `TIMESTAMPTZ NULL` | **실적 시작** — `in_progress` 전이 시각 | 시스템 (신설) |
| **`completed_at`** | `TIMESTAMPTZ NULL` | **실적 종료** — `done` 전이 시각 | 시스템 (신설) |

- **마이그레이션 리비전을 추가**한다. 기존 행은 전부 `NULL` 로 둔다(과거 데이터를 추측해 채우지 마라)
- **검증** — 둘 다 있으면 `start_date ≤ due_date`. 한쪽만 있어도 된다. CHECK 로 강제해라
- **`startedAt`·`completedAt` 은 요청으로 받지 않는다.** `TaskUpdateDTO` 에 넣지 마라 — 일반 PATCH 로 오면 **422** 여야 한다(`backend/README` §10 의 `status` 와 같은 방식)
- **실적은 상태 전이 시점에 서비스가 쓴다.** 전이 로그(`task_log`)와 **같은 트랜잭션**이어야 로그와 컬럼이 갈리지 않는다(ERD T-1-c)
- **실행취소**(`POST /status/undo`)가 전이를 되돌릴 때 **실적 컬럼도 함께 되돌려야 한다.** 로그만 지우고 컬럼을 남기면 어긋난다
- 응답에 `startDate`·`startedAt`·`completedAt` 추가(SPEC-003 §4 Data Contract)

> **`cancelledAt` 은 지금 로그에서 파생한다**(WORK-005). 그대로 둘지 컬럼으로 올릴지는 네가 판단하고 **이유를 보고에 적어라.** R-4 가 취소도 실적 시각으로 거르므로 매번 로그를 되짚게 되면 승격이 낫다.

## 2. P2 — 조회 규칙 4종

지금 `repository/task_repository.py` 의 `_period_filter` 가 「기한이 범위 안 **또는** 기한 없으면 생성일 기준 달」이다.
**T-1-a(「기한 없는 업무는 생성일 기준 달에 속한다」)는 폐기됐다.** 새 규칙:

| # | 무엇 | 조건 |
|---|---|---|
| **R-1** | 계획 기간이 범위에 걸침 | `start_date ≤ to` **AND** `due_date ≥ from`. **한쪽이 `NULL` 이면 있는 쪽만으로 판단** |
| **R-2** | 기한 없음 | `due_date IS NULL` **AND 미완료** → **범위와 무관하게 항상** |
| **R-3** | 지연 | `due_date < from` **AND 미완료** → 포함 |
| **R-4** | 완료 · 취소 | **`completed_at`**(취소는 취소 전이 시각)이 범위 안일 때만. **`due_date` 로 거르지 않는다** |

- **「미완료」는 `todo`·`in_progress`** 다. 정의를 **코드 한 곳**에 두고 문자열을 흩지 마라
- **지연 판정은 `derive_overdue()` 를 재사용해라**(WORK-005). 두 번째 구현을 만들지 마라
- `statusCounts` · `unfilteredTotal` · scope별 `total` 도 **같은 규칙으로** 센다

### ⚠ 끝 경계 — 이번에 반드시 닫아라

지금은 `< to`(열림)다. 프론트가 **`from = to = 오늘`** 을 보내므로 **열려 있으면 오늘 업무가 하나도 안 나온다.**
WORK-005 검수 FAIL-① 이 이 어긋남이었고(말일 업무가 통째로 사라짐), **일 단위가 되면 매일 터진다.**

## 3. P3 — `schedule` 파생

계획 기간 기준으로 다시 정의됐다(ERD T-1-d · `database/README` §3). **실적은 캘린더에 쓰지 않는다.**

| 업무가 가진 것 | `schedule` |
|---|---|
| `start_date` + `due_date` | **기간 일정** — `is_all_day=true`, 여러 날 |
| `due_date` 만 | 종일 일정 **하루** |
| `start_date` 만 | 시작일 하루의 종일 일정 |
| `due_date` + 시간 | 시간 일정 — `is_all_day=false` |
| 둘 다 없음 | **`schedule` 을 만들지 않는다** |

**`schedule` 쓰기 표면은 없다**(SPEC-009 · BE-10). 업무 저장의 파생으로만 갱신된다.

---

## 4. 범위

| 경로 | |
|---|---|
| `app/back/` | 전부 |
| `app/front/` | **금지 — 프론트 워커가 동시 작업 중** |
| 문서 레포 | **읽기 전용** |

**쿼리 파라미터 이름·타입(`from`·`to`)은 바꾸지 마라.** 규칙만 바뀐다.

## 5. 검증

```bash
cd app/back && uv run pytest -q <네가 만들거나 고친 테스트만>   # 전체 스위트 금지, 1회만
```

계층 자기점검 — ORM 이 repository 를 넘지 않는가 · schema/dto 를 섞지 않았는가 · `except Exception` 을 쓰지 않았는가

**테스트로 고정할 것 9개** (하나라도 빠지면 미완이다)
1. `from = to = 오늘` → **오늘 기한 업무가 나온다**(끝 경계)
2. `start 09.04 ~ due 09.08` 업무가 **09.06 조회에 나온다**(R-1 걸침)
3. `start` 만 있는 업무가 그 날 조회에 나온다 (R-1 한쪽 NULL)
4. 기한 없는 **미완료** 업무가 **어떤 범위로 조회해도** 나온다 (R-2)
5. 기한 없는 **완료** 업무는 **완료한 날** 범위에서만 나온다 (R-2 + R-4)
6. 어제 기한 · 미완료 → 오늘 조회에 나온다 (R-3)
7. 어제 기한 · **어제 완료** → 오늘 조회에 **안 나온다** (R-4)
8. 어제 기한 · **오늘 완료** → **오늘 조회에 나온다** (R-4 — 사용자 확정 규칙의 핵심)
9. `start_date > due_date` 로 저장 시도 → **거부**된다

## 6. 지킬 것

1. **`app/back/` 만 건드린다**
2. **`derive_overdue()` 재사용.** 지연 판정 두 벌 금지
3. **실행취소가 실적 컬럼도 되돌리는지** 반드시 확인해라
4. **정한 적 없는 것은 물어라** — `orca terminal send`. `orca orchestration ask` 는 답이 안 닿는다
5. **커밋·push 하지 마라**

## 7. Done Criteria

- [ ] 마이그레이션 리비전 추가 — `start_date`·`started_at`·`completed_at`, CHECK `start_date ≤ due_date`
- [ ] `startedAt`·`completedAt` 이 일반 PATCH 로 오면 **422**
- [ ] 실적 컬럼이 **전이 로그와 같은 트랜잭션**에서 쓰이고, **실행취소가 함께 되돌린다**
- [ ] R-1~R-4 반영, `_period_filter` 가 단일 진입점으로 남는다
- [ ] **끝 경계가 닫혀** `from = to = 오늘` 이 오늘 업무를 낸다
- [ ] `statusCounts`·`unfilteredTotal`·scope별 `total` 이 같은 규칙을 쓴다
- [ ] `schedule` 파생 5경우 반영
- [ ] 지연 판정이 `derive_overdue()` 하나를 지난다(정적 검사로 호출처 증명)
- [ ] 테스트 9개 통과
- [ ] `git status` 에 `app/front/` **0건**

---

## 8. 질문하는 법 — **`orca orchestration ask` 를 쓰지 마라**

```bash
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[질문] backend: <질문>" --enter
```

## 9. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 / 마이그레이션 리비전 / R-1~R-4 구현 / 끝 경계 처리 / 실적 컬럼과 실행취소 / cancelledAt 판단과 이유 / schedule 파생 / statusCounts 파급 / pytest 결과 / app/front diff 0줄 근거 / 코디가 정해야 할 자리"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
