# [backend] WORK-005 검수 수정 — statusCounts · unfilteredTotal · 상세 overdueDays

너는 **task-management `backend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**네 Phase 1·2 는 검수를 잘 통과했다** — 게이트 단일화 4종, 낙관적 갱신 방향, 마이그레이션 `0003` 모두 PASS.
**FAIL 2건은 전부 프론트 쪽**이다. 여기서는 **그 수정을 가능하게 하는 응답 필드**를 만든다.

## 1. 왜 부르나

검수 FAIL-2 — **칸반이 리스트 페이지 크기(12)를 물려받아 그 달 앞 12건만 그린다.**
그리고 완료 컬럼의 「8월 12」가 **월 기준이 아니라 받아온 카드 수**다.

**SPEC 에 칸반 데이터 범위 규격이 없어서 생긴 일이고, 코디가 정했다**(2026-09-06).
그 결정에 **응답 필드 둘이 필요하다.**

## 2. SSOT

- `para/projects/summer-star/task-management/20-spec/spec-004-tasks-status-views.md`
  — **§2 U-2 「데이터 범위」 절**(신설) · **§4 Request/Response 의 `statusCounts`·`unfilteredTotal` 표**(신설) · `typeCounts` 규칙
- `.../20-spec/spec-003-tasks-crud.md` — **§4 상세 응답의 `isOverdue`·`overdueDays`**(신설)
- `.../40-architecture/backend/README.md` — §3 규칙 7 · §12

## 3. 무엇을 만드나

### (1) `statusCounts` — 상태별 총계

```
{ "todo": n, "inProgress": n, "done": n, "cancelled": n }
```

**`typeCounts` 와 같은 결이다** — 기간·유형·프로젝트 필터는 **반영하고**, **상태 필터 자신은 반영하지 않는다.**
(상태 필터를 걸었다고 다른 컬럼 수가 0이 되면 칸반 완료 컬럼의 「8월 12」가 흔들린다.)

**`items` 를 세서 만들지 마라.** 상한에 걸리면 두 수가 갈린다 — 그게 이 필드를 만드는 이유다.
`typeCounts` 를 만든 방식(집계 쿼리)을 그대로 따라라.

**`typeCounts` 와 달리 네 키를 항상 담는다** — 0건 상태도 `0` 으로 낸다. 칸반은 컬럼이 **항상 넷**이라
행이 없으면 화면이 또 메워야 한다. (`typeCounts` 는 유형이 동적이라 사정이 다르다.)

### (2) `unfilteredTotal` — 기간만 적용한 총계

U-9 의 「유형·상태 필터를 지우면 **n건이** 보입니다」의 `n` 이다.
**기간만** 적용하고 유형·상태·프로젝트 필터는 **전부 뺀다.**

### (3) `size` 상한 500

칸반이 그 달 전체를 한 번에 받는다(U-2 「데이터 범위」). **`size` 최대값을 500 으로 열어라.**
지금 상한이 그보다 작으면 422 가 나서 칸반이 못 받는다. **상한을 없애지는 마라** — 500 이 선이다.

### (4) 상세 응답에 `isOverdue`·`overdueDays`

**문서 공백 G-1** — SPEC-004 U-10 이 「상세: 헤더 기한 옆에 같은 문구」를 요구하는데 SPEC-003 상세 계약에
`overdueDays` 가 없어 상세가 「n일 지남」을 못 그렸다. **SPEC-003 §4 에 추가했다.**

**목록과 같은 파생 규칙**이다 — 저장하지 않고 조회 시 계산한다(T-4). 목록에 쓴 계산을 재사용해라.

## 4. allowed_paths

- `app/back/` — 전부

**`app/front/` 을 건드리지 마라**(FE 워커가 같은 워크트리에서 FAIL 2건을 고치는 중이다).
문서 레포도 **읽기 전용**이다. **커밋·push·PR 하지 마라.**

## 5. 검증

```
cd app/back && pytest
```

**curl 로 실물 확인** — 수치로 보고해라:

1. `statusCounts` 네 키가 **항상** 오는가(0건 상태도 `0`)
2. **상태 필터를 걸어도 `statusCounts` 가 안 바뀌는가.** 유형 필터를 걸면 **바뀌는가**(typeCounts 와 반대 축)
3. `statusCounts.done` 이 **`items` 안의 완료 수와 다른** 상황을 만들어 확인해라 — `size` 를 작게 줘서
   완료 업무가 페이지 밖으로 밀려도 `done` 이 그대로인가. **이게 이 필드의 존재 이유다**
4. `unfilteredTotal` 이 **유형·상태 필터를 걸어도 안 바뀌고**, **기간을 바꾸면 바뀌는가**
5. `size=500` 이 **200** 인가. `size=501` 은 **422** 인가
6. 상세 응답에 `isOverdue`·`overdueDays` 가 오는가 — 기한이 어제인 진행중 업무가 `true`/`1`,
   **완료로 보내면 `false`** 인가(목록과 같은 규칙)

계층 자기점검도 붙여라 — `except Exception` 0 · service 의 fastapi/schemas/models import 0 ·
router 의 models/repository import 0 · repository 의 ORM 반환 0 · `commit()` 0.
**새 쿼리 파라미터를 만들면 `Query(alias=...)` 를 잊지 마라**(§3 규칙 7).

**dev DB 기존 행은 지우지 마라.**

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 6. 질문하는 법 — **`orca orchestration ask` 를 쓰지 마라**

```bash
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[질문] backend: <질문>" --enter
```

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

**커밋·push·PR 하지 마라.**
