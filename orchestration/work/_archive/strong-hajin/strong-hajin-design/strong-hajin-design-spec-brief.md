# [writer] 업무 상세 재설계 — BASELINE-005 · DECISION-006 · SPEC-007

너는 **strong-hajin `writer` 워커**다. 역할 문서를 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인` (코디 워크트리 — 직접 탄다)

## 0. 무엇을 만드나

문서 **셋**을 쓴다. 이 순서로, 앞 문서를 근거로 삼아.

```
para/projects/summer-star/strong-hajin/00-baseline/baseline-005-task-detail.md
para/projects/summer-star/strong-hajin/10-decision/decision-006-task-detail.md
para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md
```

**이 셋 말고 아무 파일도 건드리지 마라.** index·log·README 수정 금지. 커밋·push 금지.

## 1. 먼저 읽을 것 — 전부 절대경로

### 조사 리포트 셋 (이번 판의 사실 근거)

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/work/strong-hajin-design/spec-survey-report.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/work/strong-hajin-design/be-survey-report.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/work/strong-hajin-design/fe-survey-report.md`

### 확정 시안 — **이것이 화면의 정본이다**

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/reference/2026-09-10-sc-meeting/package 2/TaskDetail.html`

A(기본) · B(시작 막힘) · C(연결 편집) 세 상태가 들어 있다. **시안과 다르게 쓰지 마라.**
시안에 없는 것을 스펙이 요구하면 그것은 Open Question 이다.

### 기존 계약

- `.../20-spec/spec-001-work-management.md` — 선행 계약의 SoT (v0.3.0)
- `.../20-spec/spec-003-task-lifecycle-v2.md` — 중심 업무 판정 §5 · V-6/V-7/V-8 · L-11
- `.../20-spec/spec-005-projects.md` — 프로젝트 화면의 후행 역산 (§502)
- `.../10-decision/decision-004-projects.md` — D-07
- `.../30-work/work-003-*` 가 있으면 그 상태 (README 상 todo·0%)

## 2. 사용자가 확정한 것 — **전부 결정이다. 다시 묻지 마라**

이 목록이 `decision-006` 의 알맹이다. 각 항목에 **왜**를 붙여 쓴다.

### 화면 구조

1. 업무 상세는 **네 덩어리**다 — `업무 메타` · `업무 정보` · `연관 업무` · `자료`
2. 세 덩어리 제목(`업무 정보`·`연관 업무`·`자료`)은 **같은 레벨**이다
3. `업무 정보` 는 **1열** — 업무 내용, 그 아래 체크리스트 (체크리스트가 길어질 자리라 옆에 두지 않는다)
4. `연관 업무` 는 **2열**이고 짝이 정해져 있다
   ```
   상위 업무 | 프로젝트
   하위 업무 | 선행 업무
   참고 업무 | 후행 업무
   ```
5. `자료` 는 **2열** — `참고 자료` | `결과 자료`. **「산출물」 표기를 「결과 자료」로 바꾼다**
6. 목록은 **3행이 기본**이고 넘으면 **칸 안에서** 스크롤한다. 머리(제목·셈·단추)는 스크롤 밖에 고정
7. `업무 메타` 는 제목·상태·담당·기한·시작·결재·참조를 **한 줄로** 압축한다

### 관계

8. **후행은 저장하지 않는다.** `task_predecessors` 의 같은 줄을 반대쪽에서 읽는 것이다.
   B 가 A 를 선행으로 고르면 A 의 후행에 B 가 **자동으로** 선다. 새 표·새 쓰기 경로가 없다
9. 후행에 필요한 것은 셋뿐 — **역방향 조회 · `predecessor_task_id` 인덱스 · 상세 응답 필드**
10. **못 읽는 후행은 건수만** 보여준다. 제목·담당자·기한을 내지 않는다
11. **선행은 시작을 막고 하위는 완료를 막는다.** 화면에서도 문구를 갈라 쓴다.
    `WORK_PREDECESSORS_UNFINISHED` 와 `WORK_CHILDREN_UNFINISHED` 를 합치지 않는다

### 편집

12. `연관 업무` 에 **연결 편집** 입구를 둔다. 같은 2열 자리에서 고친다
13. 칸마다 조작이 다르다
    | 칸 | 조작 |
    |---|---|
    | 상위 업무 · 프로젝트 | 셀렉터 (「없음」 포함) |
    | 하위 · 선행 · 참고 | 기존 항목에 **해제** · 아래에 **추가** 셀렉터 |
    | 후행 | **해제**만. 추가 자리 없음 |
14. 「추가」는 **글자로 「추가」를 쓰고 파란색**이다 — 셀렉터만 두면 추가인지 모른다
15. **유효성은 서버가 판정한다.** 화면이 미리 막지 않는다. 고를 수 있게 두고 저장할 때 거절을 받아 보여준다
16. 비공개 후행은 해제 단추를 주지 않는다

### 계약을 여는 결정 둘

17. **상위 업무를 나중에 바꿀 수 있다.** 지금 `TaskEditFields` 에 `parent_task_id` 가 없어서 못 한다.
    이 스펙이 그 칸을 연다. 검증은 기존 `parent_for()` 를 그대로 쓴다
    (읽기 권한 · 순환 · 끝난 업무 · 중심 업무 판정)
18. **상위를 옮길 때 그 업무의 하위가 V-8 을 어기게 되면 거절한다.**
    SPEC-003 §5 가 `EU-8` 로 미뤄 둔 자리를 **이 범위에서 닫는다** — 「소급 재배치를 만들지 않는다」는
    그대로 두고, 대신 **어긋나게 만드는 이동을 막는다.** 화면이 V-8 위반 트리를 그리게 두지 않기 위해서다.
    새 오류 코드가 필요하면 제안하고 근거를 붙여라
19. **후행 해제는 즉시 반영한다.** 제안(`proposal`)으로 보내지 않는다.
    후행 해제는 **상대 업무의 선행 목록에서 나를 빼는 일**이다 — 권한 규칙을 이 스펙이 정한다
20. **알림은 이번 스펙 밖이다.** 「후행이 해제되면 상대 담당자에게 알림이 가야 한다」는 사실만
    스펙에 **자리로 표시**하고, 알림 종류·문구·전달은 **정하지 않는다.**
    `modules/notifications.py` 가 이미 있다는 것만 적고 구현 범위에서 제외한다

## 3. 반드시 다뤄야 할 알려진 결함

`baseline-005` 에 **지금 무엇이 깨져 있는지**로 적는다. 근거는 조사 리포트에 다 있다.

1. 상세 조회가 `predecessors` 를 버린다 — effect 가 `checklist`·`references`·`delivery`·`children`·`parent`
   **다섯만** 채운다. 그리는 쪽은 `task` prop 을 읽는데 목록에서 열면 그것이 목록 투영이다.
   그래서 **선행 구획과 시작 게이트가 통째로 안 선다**
2. 후행을 내주는 경로가 백엔드에 **0건**이다 (`successor` 식별자 0회)
3. 업무 상세가 `project_id` 를 **한 글자도 그리지 않는다**
4. `RelationGraph` 엣지 7종에 선행이 없다 — 서버가 내면 `kind` 문자열이 날것으로 뜬다
5. 생성 모달에서 넷(상위·프로젝트·참고·선행)을 나란히 고르는데 만든 뒤 대접이 제각각이다

## 4. 문서별 요구

### BASELINE-005 — 지금 어떻게 도는가

조사 리포트 셋을 **접는다.** 관계 여섯(상위·하위·선행·후행·참고·프로젝트)마다
`스펙 / 서버 저장 / 서버 읽기 / 서버 수정 / 화면 표시 / 화면 수정` 여섯 칸 표를 만든다.
**모든 칸에 `파일:줄`.** 조사 리포트를 인용하되 리포트 경로가 아니라 **원본 파일:줄**을 적어라.

### DECISION-006 — 무엇을 정했나

§2 의 스무 항목을 결정으로 쓴다. 형식은 `10-decision/` 의 기존 문서를 따른다.
**각 결정에 「왜」를 붙인다.** 사용자 지시인 것은 「사용자 확정 2026-09-28」로 근거를 적는다.
뒤집힌 결정은 없다.

### SPEC-007 — 무엇을 만드나

기존 `20-spec/` 문서의 구조를 따른다. 최소한 이것들:

- 화면 구조 (네 덩어리 · 2열 짝 · 3행 스크롤) — **시안이 정본**
- 관계 여섯의 읽기·쓰기 계약. 필드 이름·shape 까지
- 후행: 역방향 조회 · 인덱스 · 응답 필드 · **권한 필터**(못 읽는 후행은 건수만)
- 상위 변경: 입력 칸 · 검증 순서 · **V-8 위반 시 거절** · 오류 코드
- 후행 해제: 누가 할 수 있나 · 무엇이 바뀌나 · **알림은 범위 밖 표시**
- 선행 배선 복구: 상세 조회가 `predecessors` 를 채우는 것
- 오류 코드 표 (기존 것 + 새로 제안하는 것)
- Acceptance — 화면 A·B·C 각각에서 무엇이 참이어야 하나

## 5. 하지 말 것

- **시안과 다르게 쓰지 마라.** 다르게 쓰고 싶으면 Open Question 으로 남긴다
- 알림을 설계하지 마라 (§2-20)
- 소급 재배치를 설계하지 마라 (EU-8 은 「거절」로만 닫는다)
- 코드를 고치지 마라. 여기는 문서 워크트리다
- `_archive/` 에서 끌어오지 마라
- 정하지 못한 것을 정하지 마라 — Open Questions 로 남긴다
- 다른 문서(index·log·README·기존 spec)를 고치지 마라

## 6. 검증

- 세 문서의 모든 주장에 근거(`파일:줄` 또는 「사용자 확정 2026-09-28」)가 붙었나
- 시안과 어긋나는 서술이 없나
- 기존 계약(SPEC-001·003·005)과 충돌하는 자리를 **고치지 않고** Open Question 으로 남겼나
- 선행=시작 / 하위=완료 를 섞어 쓴 문장이 없나

## 7. 완료 보고 — **문구 변경 금지**

> ⚠ 핸들은 dispatch preamble 의 값을 믿어라. 아래는 브리프 작성 시점 값이라 오래됐을 수 있다.

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer 문서 3종 완료: <한 줄>" \
  --body "세 문서 경로 / 핵심 결정 / Open Questions / 기존 계약과 충돌한 자리"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] writer 문서 3종 완료 — <한 줄>. baseline-005·decision-006·spec-007" --enter
```

막히면: `orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 --text "[질문] writer: <질문>" --enter`
