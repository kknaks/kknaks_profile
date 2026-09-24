# 데모 더미 결과 보고 — 「프로젝트」 화면 E2E

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`,
브랜치 `kknaksss/strong-hajin-projects`. **커밋·push 하지 않았다.**

**고친 파일은 둘뿐이다.**

- `backend/src/ax_workspace/bootstrap/demo_work.py` (+216 / −4)
- `backend/tests/contract/test_demo_work_seed.py` (+106 / −2)

`scenario.py`·`material_*`·프론트·문서 레포는 한 줄도 건드리지 않았다. 기존 시드(업무·캘린더·수신함이
쓰는 12줄)는 **그대로 두고 더하기만** 했다.

---

## 1. 어디를 보면 되나 — 로그인과 프로젝트

`mina@…` / `jiho@…`, 비밀번호는 데모 공용(`scax-demo-1234`). 프로젝트 둘 다 **민아·지호 모두** 읽는다.

| 프로젝트 | `external_key` | 업무 | 참여 |
|---|---|---|---|
| **하반기 제품 개편** | `demo-project-redesign` | **11** | 지호(`lead`·만든 사람) · 민아(`member`) |
| **브랜드 리뉴얼** | `demo-project-brand` | **0 — 비어 있다** | 지호(`lead`) · 민아(`member`) |

> `project_id` 는 reset 마다 새로 난다. 위 표의 `external_key` 로 찾으면 된다.

---

## 2. A~F 대조표 — **어느 업무가 어느 항목인가**

전부 「하반기 제품 개편」 안이다(A-2 만 다른 프로젝트).

| 항목 | 요구 | 실현한 업무 | 화면에서 보이는 것 |
|---|---|---|---|
| **A-1** | 프로젝트 둘 · mina·jiho 둘 다 참여 | **하반기 제품 개편** | 아래 11줄이 전부 여기 |
| **A-2** | **업무가 하나도 없는** 프로젝트 · mina 참여 | **브랜드 리뉴얼** | 빈 본문 · 빈 간트 |
| **B-0** | 3층 트리의 최상위 | **보고서 작성** (mina) | 트리 루트 |
| **B-1** | 1단계 — **요청 발송 → 수락** | **보고서 디자인** (jiho) | 민아→지호 `WorkRequest`, 지호가 수락. `origin.kind == "work_request"` |
| **B-2** | 2단계 = **손자** · 프로젝트는 **상속** | **디자인 시안 조사** (jiho) | 지호가 자기 하위로 쪼갬. `project_id` 를 말하지 않았는데 프로젝트 목록에 있다 |
| **C-1** | 손자에 선행 — **다른 가지** 업무 | **디자인 시안 조사** ← **사용자 리서치 설문** | 보고서 가지를 접으면 **닻이 접힌 부모 바에 붙는다** |
| **C-2** | **같은 접힌 가지 안쪽** · 형제끼리 | **시안 후보 정리** ← **디자인 시안 조사** | 접으면 선이 아니라 **건수**로 |
| **C-3** | 평범한 선 ① 최상위→최상위 | **개편 범위 확정** ← **사용자 리서치 설문** | 보통 의존선 |
| **C-4** | 평범한 선 ② 최상위→최상위 | **경쟁 제품 비교** ← **개편 범위 확정** | 보통 의존선 |
| **D-1** | 체크리스트 **일부 완료** | **디자인 시안 조사** — `{"done": 2, "total": 5}` | 막대에 fill 과 **40%** |
| **D-2** | 체크리스트 **없음** | **시안 후보 정리** — `{"done": 0, "total": 0}` | **% 도 fill 도 안 난다** (0% 가 아니다) |
| **D-3** | 완료된 업무 | **사용자 리서치 설문** — `state: done` | 완료 표시 |
| **D-4** | **하위를 가진 상위** 업무 | **보고서 작성** · **보고서 디자인** | 바가 14px · % 없음 (둘뿐이다) |
| **E-1** | 시작·마감 **다 있다** | **보고서 작성** 외 7줄 | 보통 바 |
| **E-2** | **마감만 있다** | **경쟁 제품 비교** — `start_date: null`, `due_date` 만 | `span_from == span_to == due_date` — **그 날 하루** |
| **E-3** | 기간이 **아예 없다** | **접근성 점검** — `span_from/to` 둘 다 `null` | 간트에 안 서고 **좌 레일에만** |
| **E-4** | **기한이 지났다** | **로그인 화면 개선** — `overdue_days: 3` | **지연 칸에 잡히는 유일한 줄** |
| **F-1** | `open` | **경쟁 제품 비교** · 디자인 시안 조사 · 시안 후보 정리 · 접근성 점검 | |
| **F-2** | `in_progress` | **개편 범위 확정** · 로그인 화면 개선 · 보고서 작성 · 보고서 디자인 | |
| **F-3** | `blocked` (**사유 필수**) | **결제 연동 점검** — 「결제사 테스트 계정 발급을 기다리고 있습니다.」 | |
| **F-4** | `done` | **사용자 리서치 설문** | |
| **F-5** | `cancelled` **하나** | **구형 브라우저 대응** — 사유 「지원 대상에서 빠져 …」 | 취소선 바 · **요약 모수에서 빠진다** (취소는 이 한 줄뿐) |
| **F-6** | **담당 없음** (`assignee: null`) | **접근성 점검** | 화면이 「미정」을 **지어내지 않는** 것을 본다 (`plan_project_work` 로 섰다 — 배정 행이 없다) |

---

## 3. `make reset-demo` — **실제로 돌렸다**

```
cd backend && DATABASE_URL="postgresql+psycopg://ax:ax@localhost:54329/ax_demo" \
  uv run python -m ax_workspace.entrypoints.reset_demo
Demo schema reset, My Work fixtures seeded (mina/jiho), and daily-report-generation@1 installed.
exit=0
```

서버·API 프로세스는 **띄우지 않았다** — `reset-demo` 는 DB 작업이다.

---

## 4. 실물 응답 — **들어간 것을 찍었다**

**실제 demo DB**(`ax_demo`)를 계약 테스트 하네스(`TestClient`)로 읽었다. 서버 기동 없음.
민아로 로그인 → `GET /api/projects` → 각 `GET /api/projects/{id}`.

### `GET /api/projects` (민아)

```json
[
  {"project_id": "22520411-…", "name": "하반기 제품 개편", "external_key": "demo-project-redesign",
   "state": "active", "starts_on": "2026-09-01", "ends_on": "2026-11-06", "version": 1},
  {"project_id": "dce6a908-…", "name": "브랜드 리뉴얼",   "external_key": "demo-project-brand",
   "state": "active", "starts_on": "2026-09-29", "ends_on": "2026-12-21", "version": 1}
]
```

### `GET /api/projects/{하반기 제품 개편}` 의 `tasks[]` — 11줄 전부

`reset` 날이 2026-09-22 였을 때의 값이다(날짜는 **전부 `today` 상대값**이라 돌릴 때마다 따라 움직인다).

| title | state | parent | pred | checklist | start~due (원값) | span (정규화) | overdue | assignee |
|---|---|---|---|---|---|---|---|---|
| 사용자 리서치 설문 | `done` | – | – | 0/0 | 2026-09-01~09-08 | 09-01~09-08 | `null` | mina |
| 개편 범위 확정 | `in_progress` | – | 사용자 리서치 설문 | 0/0 | 2026-09-10~09-26 | 09-10~09-26 | `null` | mina |
| 경쟁 제품 비교 | `open` | – | 개편 범위 확정 | 0/0 | **`null`~09-28** | **09-28~09-28** | `null` | mina |
| 로그인 화면 개선 | `in_progress` | – | – | 0/0 | 2026-09-12~09-19 | 09-12~09-19 | **3** | mina |
| 결제 연동 점검 | `blocked` | – | – | 0/0 | 2026-09-18~10-01 | 09-18~10-01 | `null` | mina |
| 구형 브라우저 대응 | `cancelled` | – | – | 0/0 | 2026-09-16~09-24 | 09-16~09-24 | `null` | mina |
| 접근성 점검 | `open` | – | – | 0/0 | **`null`~`null`** | **`null`~`null`** | `null` | **`null`** |
| 보고서 작성 | `in_progress` | – | – | 0/0 | 2026-09-20~10-04 | 09-20~10-04 | `null` | mina |
| 보고서 디자인 | `in_progress` | **보고서 작성** | – | 0/0 | 2026-09-21~10-01 | 09-21~10-01 | `null` | **jiho** |
| 디자인 시안 조사 | `open` | **보고서 디자인** | **사용자 리서치 설문** | **2/5** | 2026-09-22~09-27 | 09-22~09-27 | `null` | jiho |
| 시안 후보 정리 | `open` | **보고서 디자인** | **디자인 시안 조사** | 0/0 | 2026-09-25~09-30 | 09-25~09-30 | `null` | jiho |

`members`: `[("jiho","lead"), ("mina","member")]`

### `GET /api/projects/{브랜드 리뉴얼}`

```json
{"name": "브랜드 리뉴얼", "tasks": [],
 "members": [{"member_id": "jiho", "assignment_kind": "lead"},
             {"member_id": "mina", "assignment_kind": "member"}]}
```

### 기존 화면이 안 깨졌다 — 같은 하네스로 확인

| | `/api/my-work` | `/api/tasks?include_closed=true` | `/api/work-requests` | `/api/work-requests/inbox` | `/api/action-items` | `/api/projects` |
|---|---|---|---|---|---|---|
| **mina** | 11 | 22 | 8 | 3 | 2 | 2 |
| **jiho** | 5 | 16 | 8 | 2 | 3 | 2 |

전부 200. 업무 원장 전체는 **12 → 23줄**(기존 12 + 프로젝트 11).

---

## 5. 테스트

| 무엇 | 명령 | 결과 |
|---|---|---|
| 데모 시드 계약 | `make test-contract-serial FILES=tests/contract/test_demo_work_seed.py` | **4 passed** (3.83s) |
| 도메인·구조·운영 대장 drift | `make test-unit` | **372 passed**, 1 deselected (10.43s) |

`test_demo_work_seed.py` 에 더한 것:

- 기존 두 단언을 **바꿨다**: 업무 수 `12 → 23`, 민아가 보낸 요청 집합에 **「보고서 디자인」 추가**
  (3층 트리의 1단계가 실제 요청이라 여기 뜨는 것이 맞다)
- **새 테스트 1건** `test_reset_demo_seeds_every_hard_spot_of_the_project_screen` —
  A~F 를 **한 함수에서 전부** 단언한다. 트리 세 칸 · 의존선 네 변 · 체크리스트 두 수 ·
  정규화 기간 네 갈래 · `overdue_days` 가 온 줄이 **하나뿐** · 상태 다섯 · `assignee: null` 이
  **하나뿐**. 빠지면 화면의 그 자리가 빈 채로 뜨는데 사람이 눌러 보기 전에는 아무도 모른다

---

## 6. 판단한 자리 · 알아 둘 것

- **프로젝트는 지호가 만든다.** 민아는 `member` 역할이라 `project.manage` 가 없어 만들 수 없다
  (`catalog.py` 의 `member` 템플릿). 만든 사람은 `lead` 로 자동으로 붙고, 민아는 `member` 로 붙인다.
- **만든 직후 principal 을 다시 읽는다.** 프로젝트 범위 grant 는 생성 시점에 생기는데 손에 든
  principal 은 그 전에 읽은 것이라, 다시 읽지 않으면 바로 다음 「사람 붙이기」가 **거절된다**
  (`ProjectAccessDenied`). 실제로 한 번 막혔고 그래서 `_seed_demo_projects` 에 한 줄로 남겼다.
- **손자는 `project_id` 를 말하지 않는다.** 하위는 상위를 따르므로(`project_for(parent=…)`)
  **상속으로** 들어간다 — 지시서가 확인하라고 한 자리이고, 실물 응답과 테스트로 둘 다 확인했다.
- **취소에도 사유가 필요하다.** `blocked` 만 사유를 요구하는 줄 알았으나 `cancelled` 도 요구한다
  (`lifecycle.py:160`). `ProjectWork.reason` 한 칸이 두 전이를 함께 맡는다.
- **선행 게이트를 피해 순서를 짰다.** 끝나지 않은 선행이 있으면 `open → in_progress` 가 막히므로
  (`TaskPredecessorGate`), 선행이 `done` 인 줄만 진행 중으로 올렸다. 「경쟁 제품 비교」·「시안 후보
  정리」가 `open` 인 것은 **그래서**이고, 화면의 `open` 표본 역할도 함께 한다.
- **지연 칸에 잡히는 줄은 하나로 맞췄다**(「로그인 화면 개선」). `overdue_days` 는 끝난 업무에
  오지 않으므로(완료·취소·승인 대기) 기한 지난 줄을 여럿 두면 지연 칸이 뭉개진다.
- **`reset-demo` 는 매번 DB 를 드롭한다.** `external_key` 중복을 걱정할 자리가 아니고,
  계약 테스트가 `main([])` 을 두 번 도는 것도 그래서 통과한다.

## 7. 하지 않은 것

- 커밋·push·PR — **하지 않았다.** 워크트리에 변경만 있다
- `scenario.py` 확장 — **하지 않았다.** `Ask` 에 `parent`·`project` 를 더하면 지시서의 「그 밖은
  건드리지 마라」를 깬다. 그래서 프로젝트 더미는 `demo_work.py` 안에서 application 명령을 직접 부른다
- `material_*` · 프론트 · 문서 레포 · 서버 기동 — 전부 손대지 않았다
