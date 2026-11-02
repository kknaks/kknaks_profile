---
type: work
id: WORK-003
title: "참조 읽음 · 프로젝트 선행업무 · 업무 만들기 창 최종 프레임"
status: todo
product: strong-hajin
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 0
created_at: 2026-09-19
updated_at: 2026-09-19
tags:
  - product/strong-hajin
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-001-work-page|BASE-001]]"
  decisions:
    - "[[decision-001-work-page|DEC-001]]"
  specs:
    - "[[spec-001-work-management|SPEC-001]]"
  works:
    - "[[work-001-task-creation|WORK-001]]"
    - "[[work-002-task-lifecycle-v2|WORK-002]]"
  releases: []
  related:
    - "[[spec-003-task-lifecycle-v2|SPEC-003]]"
---

# 참조 읽음 · 프로젝트 선행업무 · 업무 만들기 창 최종 프레임

세 가지를 한 실행 단위로 만든다 — **참조(CC) 참고 업무의 수신함 읽음**(DEC-001 D-19),
**프로젝트 안의 선행업무와 finish-to-start 시작 게이트**(D-20), **업무 만들기 창의 최종
프레임**(D-21). **만들지 않는 것**: 간트 화면 자체, 「안 읽음으로 되돌리기」, `참조 업무` 탭의
읽음 표시, `요청` 갈래의 결재자 저장, 「결재자」로의 문서·필드 전체 개명.

> 1 파일 = 1 work = **빌드 계획**. SPEC 의 외부 계약 본문은 복제하지 않고 절 이름으로 가리킨다.
> **이 문서는 착수 전 계획이다.** 모든 phase 가 `TODO` 이고 코드는 한 줄도 쓰지 않았다.
> **BE 와 FE 는 이 문서가 검수된 뒤 병렬로 발주한다** — Phase 경계가 그 갈래를 이미 가른다.

## Meta

- Baseline: BASE-001
- Covers spec: SPEC-001 §2 U-6(전면 개정)·U-12·U-13·U-14·U-15 · §3 S-11·S-12 ·
  §4 API Contract(수신함·읽음·요청 목록·프로젝트 상세)·Request/Response·Validation·Case Matrix·
  State/Lifecycle·Data Contract · §5 권한·동시성·보존·표면 일치 · §6 인수조건 세 블록
- Depends on work: WORK-001(생성 경로·멱등 키·활성 담당) · WORK-002(v2 요청·수락·하위 관계)
- Parallel work: 없음. **이 work 안에서 BE·FE 두 갈래가 병렬이다**
- Follow-up work: 간트 화면(OQ-K) · `요청` 갈래 결재자(OQ-M) · 낱말 통일(OQ-N) ·
  DEC-002·SPEC-003 본문 갱신(OQ-L)
- External dependency: 없음. 외부 API·credential 을 새로 붙이지 않는다

**착수를 막는 미결이 하나 있다.** **OQ-M**(`요청` 갈래의 결재자)이 열려 있다.
그 하나가 막는 것은 **Phase 3 의 요청 갈래 저장 한 조각**뿐이고, 나머지 전부는 확정 계약 위에
선다. 그 조각은 **화면에 칸을 세우되 저장하지 않고**, 안내 문구로 그 사실을 말한다.

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | todo |
| Progress | 0% |
| Branch/PR | `kknaksss/strong-hajin-work` (기존 브랜치 계속 사용 — 새 워크트리·브랜치를 만들지 않는다) |
| Blocker | 없음 (OQ-M 은 Phase 3 의 한 조각만 gate 한다) |
| Next | WP 검수 → BE·FE 병렬 발주 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위 경계 — 간트 화면·요청 결재자·개명을 끌어오지 않는다 | todo |
| Design | kknaks | 창의 탭 골격과 라벨. **기존 부품**(`Modal`·`SegmentedControl`·`Select`·`TaskPickTable`)만 쓴다 | todo |
| FE | kknaks | 창 프레임 · 조건부 필드 · 읽음 버튼 · 수신함 제거 · API 연결 | todo |
| BE | kknaks | 읽음 영수증·필터 · 선행 표·제약·게이트 · 결재자 저장 · projection 정렬 | todo |
| QA | kknaks | 인수조건 대조 · 권한·동시성·회귀 | todo |
| Ops | kknaks | 로컬 스택 검증. **배포는 이 work 에 없다** | todo |

## Scope

**포함**

- 참조 읽음 — 영수증 · 멱등 읽음 명령 · 수신함 `reference` 갈래 필터 · 뱃지 · `참조 업무` 탭 존치
- 선행업무 — 표·제약 · 생성/수정 payload · 순환·프로젝트 검증 · finish-to-start 게이트 ·
  프로젝트 상세 업무 줄의 선행 배열
- 결재자 — **`업무` 갈래**의 `approver_id` 저장·조회
- 만들기 창 — 갈래 토글·제목 · 왼쪽 탭 넷 · 갈래별 기본 정보 · `업무 연결` 탭 ·
  참고 업무 UI 내림 · 낡은 안내 문구 정정
- 표면 정렬 — REST · MCP · AX projection
- 회귀 — unit · contract · PostgreSQL 통합 · FE · 브라우저 journey

**제외**

| 제외 | 어디로 |
|---|---|
| 간트/타임라인 **화면** | OQ-K. 이 work 는 **데이터**(선행 배열)까지 |
| 「안 읽음으로 되돌리기」 | OQ-I. 만들지 않는다 |
| `참조 업무` 탭의 읽음/미읽음 **표시** | OQ-J. 탭은 그대로 두고 표시를 더하지 않는다 |
| `요청` 갈래의 결재자 **저장·조회** | OQ-M. 칸만 세우고 저장하지 않는다 |
| 「결재자」로의 문서·필드 **개명** | OQ-N. 라벨 매핑으로 둔다 |
| 참고 업무의 **입력 필드·저장 모델·명령 삭제** | 하지 않는다. **UI 만 창에서 내린다** |
| 업무 요청 **수락·거절 흐름** 변경 | 하지 않는다. 읽음은 CC 참고 갈래만 접는다 |
| 기존 데이터 전환·backfill·migration | DEC-001 D-17 면제 |
| DEC-002·SPEC-003 본문 갱신 | OQ-L. 다음 발주 |

## Code Surface

- Repo / module: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`,
  branch `kknaksss/strong-hajin-work`, base `origin/main`
- 아래는 **후보**다. 착수할 때 같은 검색을 다시 돌려 표면을 다시 센다 — **목록 밖에서 실패가 난다.**
  특히 수신함을 내는 입구와 상태를 바꾸는 입구는 **grep 으로 전수**하고 시작한다.

### BE allowed paths

| 경로 후보 | 역할 |
|---|---|
| `backend/src/ax_workspace/platform/persistence.py` | 읽음 영수증 표 · 선행 표 · 제약. **스키마 SoT 는 모델 metadata** |
| `backend/src/ax_workspace/platform/work_tasks.py` | 영속 — 영수증 읽기/쓰기, 선행 행, 프로젝트 업무 조회 |
| `backend/src/ax_workspace/modules/work/requests.py` | 수신함 `inbox()` 의 `reference` 갈래 필터 · 읽음 명령 |
| `backend/src/ax_workspace/modules/work/request_commands.py` · `request_results.py` · `request_errors.py` | 읽음 명령 입력·영수증 투영·오류 |
| `backend/src/ax_workspace/modules/work/task_creation.py` | 공통 생성 payload — `preceding_task_ids` · `approver_id` |
| `backend/src/ax_workspace/modules/work/task_commands.py` | 수정 payload — 선행 배열 전체 교체 |
| `backend/src/ax_workspace/modules/work/application.py` | 선행 검증(자기·중복·순환·프로젝트) · 투영 · 프로젝트 변경 거부 |
| `backend/src/ax_workspace/modules/work/lifecycle.py` | **시작 게이트** — 전이 판정이 모이는 자리 |
| `backend/src/ax_workspace/modules/work/errors.py` | 새 오류 클래스 넷 + 읽음 권한 하나 |
| `backend/src/ax_workspace/modules/work/projects.py` · `project_results.py` | 프로젝트 상세 업무 줄에 선행 배열 |
| `backend/src/ax_workspace/modules/work/task_results.py` | 업무 투영에 선행·결재자 |
| `backend/src/ax_workspace/bootstrap/application.py` | 위 application 조립 |
| `backend/src/ax_workspace/entrypoints/http.py` | REST — 읽음 라우트 · 오류→상태 매핑 |
| `backend/src/ax_workspace/entrypoints/mcp.py` · `modules/ax_execution/tool_catalog.py` | MCP 수신함 projection · **도구 설명 문구** · 생성 도구 인자 |
| `backend/src/ax_workspace/platform/actions.py` | AX 제안 필드 목록 |
| `backend/tests/unit/` · `tests/contract/` · `tests/integration/postgres/` | 회귀 |

### FE allowed paths

| 경로 후보 | 역할 |
|---|---|
| `frontend/src/features/work/WorkModals.tsx` | 만들기 창 — 토글·탭·갈래별 필드·참고 업무 내림·선행/결재자 전송 |
| `frontend/src/shell/InboxRail.tsx` | 수신함 카드 `[읽음]` · 목록 제거 · 뱃지 |
| `frontend/src/features/work/requestInbox.ts` | 수신함 항목 조립 |
| `frontend/src/features/work/MyWorkPage.tsx` | `참조 업무` 탭 존치 · 목록 갱신 |
| `frontend/src/features/work/WorkTables.tsx` | `CcTaskTable` · 선행 표시 |
| `frontend/src/lib/api.ts` · `viewModels.ts` · `labels.ts` | 호출·타입·문구 |
| `frontend/src/features/work/*.test.tsx` · `frontend/e2e/` | 회귀 |

- **Domain / schema note**: **새 표 둘**(읽음 영수증 · 선행)과 **제약 셋**(영수증 유일성 ·
  선행 활성 유일성 · 자기참조 금지)이 생긴다. 실제 schema 의 SoT 는 **모델 metadata** 이고,
  그것을 데이터베이스에 세우는 자리는 `reset_demo` 하나다 — **이 레포에 migration 도구는 없다**
  (WORK-001 § 스키마를 어디에 세우나 가 그 사실의 원장이다). **기존 데이터 전환·backfill 은
  하지 않는다.**

## Domain / Schema

| Entity | 역할 |
|---|---|
| 읽음 영수증 | (요청 · 사람) → 읽은 시각. **행을 지우지 않고**, 한 사람의 읽음이 남의 목록을 바꾸지 않는다 |
| 선행 관계 | (업무 · 선행 업무) 활성/닫힘. **상위·참고와 다른 세 번째 관계** |
| Task | `approver_id` 에 **이제 값이 들어온다**(`업무` 갈래). 열은 WORK-001 이 이미 만들었다 |

**상태 / invariant**

1. **읽음은 사용자별이다.** (요청 · 사람) 한 쌍에 DB 유일성이 선다. 같은 사람의 동시 두 번이
   행 하나를 만들고 둘 다 성공한다.
2. **읽음은 요청 행의 회차를 올리지 않는다.** 남의 낙관적 잠금을 흔들지 않는다.
3. **읽음은 CC 관계를 지우지 않는다.** 관계가 남아야 그 사람이 왜 이 업무를 아는지가 남는다.
4. **읽음 필터는 수신함 `reference` 갈래 하나에만 걸린다.** 요청 목록·업무 조회에는 없다.
5. **한 업무의 같은 선행 관계는 활성 행 하나.** 부분 unique 로 DB 가 답한다.
6. **자기 자신은 선행이 될 수 없다.** DB CHECK 으로 막는다.
7. **순환은 application 이 활성 행만 따라 걸으며** 막는다 — DB 가 못 한다.
   **검사와 저장이 한 덩어리**다.
8. **선행은 같은 프로젝트 안에서만** 선다. 선행이 있으면 프로젝트는 필수이고,
   **남은 선행이 있는 업무의 프로젝트는 바꿀 수 없다.**
9. **시작 게이트는 finish-to-start 하나다.** 미완(취소 아닌) 선행이 있으면 시작과
   `시작 전 → 완료` 직행을 둘 다 막는다. **판정과 전이가 한 덩어리**다.
10. **게이트는 시작 시점 판정이다.** 시작한 뒤 선행이 다시 열려도 후행을 되돌리지 않는다.
11. **미완 하위가 완료를 막는 기존 규칙은 그대로다.** 선행과 다른 축이고 **오류 코드도 다르다.**

**스키마를 어디에 세우나** — WORK-001 § 스키마를 어디에 세우나 와 같다. 새로 들이지 않는다.

- 새 표·제약을 **모델 metadata 에만** 더한다. 스키마 소유는 `reset_demo` 그대로다.
- DB 수준 유일성·CHECK 은 **이 work 전용 빈 격리 테스트 데이터베이스**에서 검증한다
  (`make test-postgres`, `POSTGRES_TEST_URL` — `DATABASE_URL` 과 반드시 다르다).
- `sync-demo-schema` 가 **제약을 만들 수 있다고 적지 않는다** — 못 한다.
- **실제 사용자 데이터가 든 데이터베이스를 reset 하지 않는다.**

**SPEC 에 환류해야 하는 외부 변경**: 구현 중 외부에 드러나는 resource/status/enum 이 SPEC 과
달라지면 **코드를 맞추지 말고 SPEC 개정을 먼저 올린다.**

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| FE Phase 4~6 | BE 가 내는 읽음 영수증 · 수신함 필터 · 선행 배열 · 결재자 투영 | **계약은 SPEC-001 이 이미 고정**했으므로 FE 는 BE 완료를 기다리지 않고 착수한다. 붙이는 시점만 순서가 있다 |
| 간트 화면(후속) | 프로젝트 상세 업무 줄의 선행 배열 | **새 조회를 만들지 않는다.** 화면 자리는 OQ-K |
| `요청` 결재자(후속) | `approver_id` 저장 경로 | 업무 갈래가 먼저 서고, OQ-M 이 닫히면 요청 갈래가 같은 자리를 쓴다 |

**BE·FE 병렬 규칙** — 두 갈래가 **같은 파일을 만지지 않는다.** 위 allowed paths 표가 그
경계이고, 한쪽이 상대 표의 파일을 고쳐야 하면 **먼저 코디네이터에게 올린다.**

## Internal Interface Contract

SPEC 의 외부 API 계약을 복제하지 않는다. 여기 고정하는 것은 **후속이 의존하는 내부 입출력**뿐이다.

**읽음 판정 (application 내부)**

- 입력: 행위자 · 요청 식별자
- 판정 순서: ① 그 요청을 읽을 수 있는가(아니면 **없는 것과 같은 말**) → ② 그 요청의 **CC 참조자인가**
  (아니면 권한 거절) → ③ 영수증이 이미 있으면 **그것을 그대로 돌려준다**
- 출력: 요청 식별자 · 읽음 여부 · 읽은 시각
- **요청 행을 수정하지 않는다** — 회차도 상태도 그대로다

**선행 판정 (application 내부)**

- 입력: 업무 · 선행 후보 배열(전체 교체) · 행위자 · 회차
- 판정: 자기 자신 → 중복 → 프로젝트 일치 → 순환 순으로 가르고 **각각 다른 오류**를 낸다
- 출력: 활성 선행 배열 + 오른 회차 + 진행 기록 한 줄
- **검사와 저장이 한 transaction** 이다

**시작 게이트 (전이 판정 안)**

- 입력: 업무 · 목표 상태 · 미리 계산한 **막는 선행 목록**
- 목표가 `진행 중` 이거나 (`시작 전` 에서의) `완료` 면 막는 선행이 있는지 본다
- 거절은 **막는 선행의 이름을 함께** 싣는다 — 미완 하위 거절이 이미 그 모양이다

## Execution

각 Phase 의 상태는 `TODO / IN_PROGRESS / DONE / BLOCKED / SUPERSEDED` 중 하나로 갱신한다.
Phase 별 `검증` + `완료 증거` 가 완료 조건이다.

> **Phase 1~3 은 BE, Phase 4~6 은 FE, Phase 7 은 공통이다.** 두 갈래는 WP 검수 뒤 **병렬 발주**한다.

### Phase 1 — BE · 참조 읽음

- **Status**: TODO
- **allowed paths**: BE 표의 `persistence.py` · `work_tasks.py` · `requests.py` ·
  `request_commands.py` · `request_results.py` · `request_errors.py` · `errors.py` ·
  `bootstrap/application.py` · `entrypoints/http.py` · `entrypoints/mcp.py` ·
  `modules/ax_execution/tool_catalog.py` · `tests/`
- **의존성**: 없음. **첫 BE 단계다**
- **설명**: 읽음이라는 사실을 사용자별로 세우고, 수신함의 참고 갈래에서만 접는다.
- **작업**:
  - [ ] 읽음 영수증 표와 `(요청, 사람)` 유일성을 **모델 metadata** 에 더한다
  - [ ] 읽음 명령을 요청 자원 아래 하위 명령으로 세운다 — **멱등**, 본문 없음, 회차 없음
  - [ ] 권한: **그 요청의 CC 참조자만.** 아니면 403, 없거나 못 읽으면 404(같은 말)
  - [ ] 수신함 조회의 `reference` 갈래에 **미읽음 필터**. `work` 갈래는 손대지 않는다
  - [ ] 요청 목록 조회·업무 조회에 **필터를 걸지 않았음**을 명시적으로 확인한다
  - [ ] MCP 수신함 도구가 **같은 projection** 을 쓰고, 도구 설명의
        「처리된 것까지 포함해」 문구를 함께 고친다
  - [ ] **읽음 명령을 MCP·AX 에 내지 않는다**
- **검증**:
  - [ ] 수신함을 내는 입구를 **grep 으로 전수**하고 필터가 닿은 곳·안 닿은 곳을 목록으로 남긴다
  - [ ] 같은 항목 두 번 읽음 → `200` · `read_at` 첫 값 그대로
  - [ ] 같은 사람 **동시 두 번** → 행 하나
  - [ ] 참조자 A 의 읽음이 참조자 B 의 수신함·뱃지를 **바꾸지 않는다**
  - [ ] 읽음 뒤에도 CC 관계가 남고 `참조 업무` 탭에서 읽힌다
  - [ ] 읽음이 요청 행의 **회차를 올리지 않는다**
  - [ ] 업무 요청 `pending`/`negotiating` 의 수락·거절 흐름이 **그대로다**
  - [ ] `cd backend && uv run pytest tests/unit tests/contract -k "inbox or request"`
  - [ ] `make test-unit` · `make test-contract`
  - [ ] `make test-postgres` (유일성 제약 — `POSTGRES_TEST_URL` ≠ `DATABASE_URL`)
- **완료 증거**: 미작성

### Phase 2 — BE · 선행업무와 시작 게이트

- **Status**: TODO
- **allowed paths**: BE 표의 `persistence.py` · `work_tasks.py` · `task_creation.py` ·
  `task_commands.py` · `application.py` · `lifecycle.py` · `errors.py` · `projects.py` ·
  `project_results.py` · `task_results.py` · `bootstrap/application.py` ·
  `entrypoints/http.py` · `entrypoints/mcp.py` · `platform/actions.py` · `tests/`
- **의존성**: 없음 — Phase 1 과 **파일이 거의 겹치지 않는다**. `persistence.py`·`errors.py`·
  `http.py`·`bootstrap/application.py` 만 공유하므로 **한 사람이 순서대로** 가거나 충돌을 먼저 푼다
- **설명**: 업무와 업무를 잇는 세 번째 관계를 세우고, 시작을 막는 규칙 하나를 건다.
- **작업**:
  - [ ] 선행 표 · 부분 unique(활성) · 자기참조 CHECK 을 **모델 metadata** 에 더한다
  - [ ] 공통 생성 payload 와 수정 payload 에 **선행 배열**. 수정은 **전체 교체**,
        **생략하면 안 건드린다**, 빈 배열은 「전부 뗀다」
  - [ ] 검증 넷을 **각각 다른 오류**로 가른다 — 프로젝트 미선택 · 프로젝트 불일치 ·
        자기 자신 · 중복 · 순환
  - [ ] **순환 검사와 저장을 한 transaction** 에 둔다
  - [ ] 선행 변경이 **회차를 올리고 진행 기록에 남는다**
  - [ ] 해제는 **행을 지우지 않고 닫는다**
  - [ ] **남은 선행이 있는 업무의 프로젝트 변경을 거부**한다. 하위가 상위를 따라 옮기는 경로에도 건다
  - [ ] 시작 게이트를 **전이 판정 한 자리**에 건다 — 시작과 `시작 전 → 완료` 직행 둘 다,
        **같은 오류 코드**로. 취소된 선행은 막지 않는다
  - [ ] 거절 본문에 **막는 선행의 이름**을 싣는다
  - [ ] 업무 조회 투영과 **프로젝트 상세 업무 줄**에 선행 배열을 낸다. **새 조회를 만들지 않는다**
  - [ ] 볼 수 없는 선행은 **제목 없이 건수만** 낸다
  - [ ] REST · MCP 생성 도구 · AX 제안 필드가 **같은 배열**을 받는다
- **검증**:
  - [ ] 상태를 바꾸는 입구를 **grep 으로 전수**하고 게이트가 시작과 직행 **둘에만** 걸렸음을 확인
  - [ ] 자기 자신 · 중복 · 순환 · 프로젝트 불일치 · 프로젝트 미선택 각각 **다른 오류**
  - [ ] 미완 선행 → 시작 409, `시작 전` 에서의 완료도 409, **같은 코드**
  - [ ] 취소된 선행은 막지 않는다. 전부 완료/취소면 시작이 열린다
  - [ ] 시작 뒤 선행이 다시 열려도 **후행이 되돌아가지 않는다**
  - [ ] **미완 하위의 완료 거절과 오류 코드가 다르다**
  - [ ] 같은 관계 **동시 두 번** → 행 하나
  - [ ] `make test-unit` · `make test-contract`
  - [ ] `make test-postgres` (부분 unique · CHECK)
- **완료 증거**: 미작성

### Phase 3 — BE · 결재자 저장과 projection 정렬

- **Status**: TODO
- **allowed paths**: `task_creation.py` · `task_commands.py` · `application.py` ·
  `task_results.py` · `entrypoints/http.py` · `entrypoints/mcp.py` · `platform/actions.py` · `tests/`
- **의존성**: Phase 2 와 **같은 파일을 만진다.** Phase 2 뒤에 간다
- **설명**: WORK-001 이 열만 만들어 둔 결재자에 값을 넣는다 — **`업무` 갈래만.**
- **작업**:
  - [ ] `업무` 생성·수정 payload 가 `approver_id` 를 **받아 저장**한다
  - [ ] 검증은 D-9 그대로 — 0..1 · 재직 중 · **담당자 본인 불가** · `승인 대기` 뒤 변경 불가
  - [ ] 업무 조회 투영이 결재자를 낸다
  - [ ] **`요청` 갈래는 `approver_id` 필드를 열지 않는다** — OQ-M.
        보내면 **`extra='forbid'` 로 422** 다(요청 생성 입력이 이미 그 설정을 상속한다).
        받아서 무시하는 API 를 만들지 않고, **거절 경로를 새로 만들지도 않는다** —
        미개방이 이미 기본 동작이다.
  - [ ] `업무` 갈래 생성이 **담당자 인자 없이** 와도 현재 사용자를 담당자로 기록하는지 확인하고
        회귀로 못 박는다(현행 동작으로 보이나 **계약으로 고정된 적이 없다**)
  - [ ] 참조자가 **두 갈래 모두** 저장되는지 확인하고 회귀로 못 박는다
  - [ ] 요청 생성이 **시작일**을 받는지 확인하고 회귀로 못 박는다
- **검증**:
  - [ ] 결재자가 저장되고 조회에서 읽힌다. 담당자 본인 지정이 거절된다
  - [ ] `승인 대기` 뒤 결재자 변경이 거절된다
  - [ ] `요청` 갈래에 `approver_id` 를 실어 보내면 **422** 다(필드 미개방). 조용히 무시되지 않는다
  - [ ] 담당자 인자 없는 `업무` 생성이 현재 사용자를 담당자로 세운다
  - [ ] `make test-unit` · `make test-contract`
- **완료 증거**: 미작성
- **Gate**: **OQ-M 이 닫히기 전에는 `요청` 갈래의 `approver_id` 필드를 열지 않는다.** OQ-M 자체는 열린 채로 둔다 — 답이 오면 이 한 줄만 바뀐다.

### Phase 4 — FE · 만들기 창 최종 프레임

- **Status**: TODO
- **allowed paths**: FE 표의 `WorkModals.tsx` · `lib/api.ts` · `viewModels.ts` · `labels.ts` ·
  `features/work/*.test.tsx`
- **의존성**: 없음 — **계약은 SPEC-001 §2 U-6 이 이미 고정**했다. BE 를 기다리지 않는다
- **설명**: 창의 골격과 갈래별 필드를 확정 프레임에 맞춘다.
- **작업**:
  - [ ] 갈래 토글과 제목(`새 업무 추가` / `새 업무 요청`)을 확인·유지한다
  - [ ] 선택 탭 이름을 **`업무 연결`** 로 고친다
  - [ ] `업무 연결` 탭에서 **`참고 업무` fieldset 을 내린다.** 상세의 자리는 그대로 둔다
  - [ ] `요청` 갈래에 **`시작일`** 칸을 세우고 **보낸다**
  - [ ] 참조자 안내의 **「내 업무로 만들면 함께 저장되지 않습니다」를 고친다** — 저장된다
  - [ ] 결재자를 **실제로 보낸다**(`업무` 갈래). 안내 문구를 걷는다.
        **`요청` 갈래에서는 결재자를 보내지 않는다** — 서버가 필드를 열지 않아 보내면 422 다.
        칸은 세우되 **아직 저장되지 않는다고 말한다**(OQ-M)
  - [ ] 선행 업무를 **실제로 보낸다.** 「아직 저장되지 않습니다」를 걷는다
  - [ ] 프로젝트 미선택 시 선행 비활성 + 안내를 유지한다
  - [ ] 선행 후보를 **고른 프로젝트의 업무**로 거르고 **자기 자신·이미 고른 것**을 뺀다
  - [ ] `업무` 갈래에 담당자 칸을 **세우지 않는다**(현행 유지 확인)
  - [ ] 체크리스트·자료 탭은 현행 동작 유지. **붙일 수 없는 갈래에서 고른 파일을 조용히 버리지 않는다**
- **검증**:
  - [ ] 탭을 옮겼다 돌아와도 값이 남는다
  - [ ] 선택 탭 셋을 하나도 안 채워도 만들어진다
  - [ ] 고른 값이 **조용히 버려지지 않는다** — 보내지 않는 값은 화면이 그 사실을 말한다
  - [ ] `make frontend-test`
- **완료 증거**: 미작성

### Phase 5 — FE · 수신함 읽음과 참조 업무 탭

- **Status**: TODO
- **allowed paths**: `shell/InboxRail.tsx` · `features/work/requestInbox.ts` ·
  `features/work/MyWorkPage.tsx` · `features/work/WorkTables.tsx` · `lib/api.ts` · 관련 test
- **의존성**: 없음 (계약 고정). 실제 붙이기는 Phase 1 뒤
- **설명**: 읽으면 수신함에서만 사라지게 한다.
- **작업**:
  - [ ] 참고 카드에 `[읽음]` 을 세운다. **참조자에게만** 그린다
  - [ ] **카드를 여는 것**도 같은 읽음 명령을 부른다
  - [ ] 읽으면 그 카드를 목록에서 빼고 **뱃지를 줄인다**
  - [ ] 뱃지는 **필터가 걸린 수신함 건수**를 그대로 쓴다
  - [ ] `참조 업무` 탭은 **요청 목록에서 계속 읽는다** — 읽음 필터를 붙이지 않는다
  - [ ] 업무 요청 카드에는 `[읽음]` 을 **세우지 않는다**
- **검증**:
  - [ ] 읽은 항목이 수신함에서 사라지고 `참조 업무` 탭에는 남는다
  - [ ] 연타해도 한 번만 처리된다
  - [ ] `make frontend-test`
- **완료 증거**: 미작성

### Phase 6 — FE · 선행 표시와 시작 거절

- **Status**: TODO
- **allowed paths**: `features/work/WorkTables.tsx` · `features/work/WorkModals.tsx` ·
  `features/work/MyWorkPage.tsx` · `labels.ts` · 관련 test
- **의존성**: Phase 4 뒤(같은 파일)
- **설명**: 막혔다는 사실과 **무엇이 막는지**를 화면이 말하게 한다.
- **작업**:
  - [ ] 상세 `값` 구획에 `선행업무` 줄. 비면 줄이 없다. 끝나지 않은 선행을 **눈에 띄게**
  - [ ] 볼 수 없는 선행은 **제목 없이 건수만**
  - [ ] 미완 선행이 있으면 `[시작]` 과 (`시작 전` 의) `[완료]` 를 **비활성**으로 두고
        **막는 선행 이름**을 그 옆에 낸다
  - [ ] 프로젝트 변경 거절 문구를 프로젝트 필드 옆에 낸다
  - [ ] 회차 충돌이면 지금 값으로 다시 읽되 **쓰던 입력은 남긴다**
- **검증**:
  - [ ] 버튼이 **누르기 전에** 막힌다. 눌린 뒤 거절도 같은 문장을 낸다
  - [ ] 취소된 선행은 버튼을 막지 않는다
  - [ ] `make frontend-test`
- **완료 증거**: 미작성

### Phase 7 — 공통 · 회귀와 표면 정렬

- **Status**: TODO
- **allowed paths**: `backend/tests/**` · `frontend/src/**/*.test.tsx` · `frontend/e2e/**`
- **의존성**: Phase 1~6
- **설명**: 계약이 표면마다 같은지, 그리고 바꾸지 않기로 한 것이 정말 안 바뀌었는지 본다.
- **작업**:
  - [ ] 화면·REST·MCP·AX 가 **같은 수신함 projection** 을 쓴다
  - [ ] 생성 표면 전부(REST·MCP·AX 제안·회의 후속 승격)가 **같은 선행 배열**을 받는다
  - [ ] 관계 셋(상위·참고·선행)을 섞지 않았음을 test 로 남긴다 —
        참고를 달아도 시작이 막히지 않고, 선행을 달아도 하위 완료 규칙이 안 바뀐다
  - [ ] 참고 업무의 **계약·데이터가 살아 있음**을 test 로 남긴다
  - [ ] 새 DB 제약을 **빈 격리 데이터베이스**에서 검증한다
- **검증**:
  - [ ] `make verify` (= `test` · `test-scale` · `test-release` · `frontend-test` ·
        `frontend-assets` · `frontend-build`)
  - [ ] `make test-postgres`
  - [ ] 브라우저 journey — `make local-stack` 을 띄운 뒤
        `make e2e-work-request` · `make e2e-work-relations` · `make e2e-task-lifecycle`
  - [ ] **사용자 E2E 는 사용자가 직접 수행한다**(WORK-001·WORK-002 와 같은 규칙)
- **완료 증거**: 미작성

> **워커는 사용자의 포트·프로세스를 건드리지 않는다.** `local-stack` 과 e2e 가 필요하면
> 코디네이터에게 올린다. 기존 사용자 데이터베이스를 reset 하지 않는다.

## Pre-deploy Check

- [ ] 기존 서비스 영향 없음 — 업무 요청 수락·거절, 미완 하위 완료 규칙, 참고 업무 계약이 그대로다
- [ ] credential·env 신규 노출 없음 — 외부 API 를 붙이지 않았다
- [ ] 응답에 비공개 필드 없음 — **볼 수 없는 선행의 제목이 새지 않는다**(건수만)
- [ ] 읽음 영수증이 **다른 사람의 읽음 여부를 노출하지 않는다**
- [ ] 새 DB 제약이 **실사용 데이터베이스에 적용되지 않았다**(이 work 범위 밖)

## Rollback

- migration downgrade 는 **없다**(도구가 없다). 되돌리기는 **코드·모델 되돌림 + 일회용 환경 교체**다.
- 부분 revert 영향: 읽음(Phase 1·5)과 선행(Phase 2·6)은 **서로 독립**이라 한쪽만 되돌릴 수 있다.
  창 프레임(Phase 4)은 선행·결재자 전송을 포함하므로 **Phase 2·3 보다 먼저 되돌린다.**
- 되돌려도 **CC 관계·참고 업무 데이터는 손대지 않았으므로** 복구할 것이 없다.

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] SPEC-001 §6 의 인수조건 세 블록(참조 읽음 · 프로젝트 선행업무 · 만들기 창 프레임)이 전부 체크된다.
- [ ] `make verify` · `make test-postgres` 가 통과한다.
- [ ] 기존 계약 삭제·약화가 **0건**이다 — 참고 업무 · 수락·거절 · 미완 하위 규칙.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다. **문서 쪽은 2026-09-19
      리뷰 수정에서 닫았다**(Status Board · Work List · Spec Coverage · log 줄).
      구현이 끝나면 **상태·진척만** 다시 갱신한다.

## Open Issues

- **OQ-M** — `요청` 갈래의 결재자. **Phase 3 의 한 조각을 gate** 한다. 답 전에는 만들지 않는다.
- **OQ-K** · **OQ-I** · **OQ-J** · **OQ-N** — 이 work 밖이고 착수를 막지 않는다.
- **OQ-L** — DEC-002·SPEC-003 본문 갱신. 다음 발주.
- ~~`30-work/README.md` 의 index 에 WORK-003 행이 없다~~ — **2026-09-19 리뷰 수정에서 닫았다.**
  구현이 진행되면 그 표의 **Status·Progress·Next 를 같은 커밋에서** 움직인다.
- 결재자 검증 「`승인 대기` 뒤 변경 불가」는 **완료 승인 경로가 서 있어야 의미가 있다**.
  그 경로의 현황은 WORK-002 가 갖는다 — 착수 때 실제 상태를 다시 확인한다.

## Related

- SPEC: (frontmatter `links.specs` 참조)
- Work: (frontmatter `links.works` 참조)
- Decision: DEC-001 § D-19 · D-20 · D-21 · § 구현 WP
