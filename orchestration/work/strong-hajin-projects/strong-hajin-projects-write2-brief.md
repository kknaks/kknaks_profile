# [writer] BASE-004 · DEC-004 **개정** — 검수 뒤 나온 결정 17건을 반영하고 미결 9건을 닫는다

너는 **strong-hajin `writer` 워커**다. **너는 이 작업의 맥락이 하나도 없다.**
**이미 존재하는 문서 둘을 고치는 일**이다 — 새로 쓰지 마라.

먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/_RESUME.md` ← **이 작업의 정본.** §2 결정표가 이번 개정의 유일한 재료다
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-004-projects.md` (474줄) ← 고칠 문서 ①
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-004-projects.md` (407줄) ← 고칠 문서 ②
- 배경이 필요하면: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/design-read-projects.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-be-domain.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-fe-structure.md`

작업 워크트리: **`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`** (코디 워크트리에 직접 탄다)
⚠ 코디네이터가 같은 워크트리에 있다. **지정된 두 파일 밖은 건드리지 마라.**

## 1. 무엇이 달라졌나

직전 판(BASE-004·DEC-004)은 **검수를 통과했다.** 그 뒤 사용자와 대화하면서
**미결 9건이 전부 닫혔고**, 파는 과정에서 **새 사실 셋과 새 결정 여럿**이 나왔다.
`_RESUME.md` §2 표가 그 전부이고 **지금 27행**이다. 직전 판에 들어간 10건 외의
**나머지 17건이 이번에 더할 것**이다.

**가장 큰 뒤집기 하나를 명시하라** — 직전 판은 미결 #1(손자 업무)을 열어 두었는데,
이제 **「간트는 깊이 제한 없이 재귀 트리로 그린다」**로 닫혔다. 그 과정에서
**코디네이터가 먼저 제안했던 「중심+직속 하위 2단계만」이 철회됐다.**
뒤집힌 판단은 **지우지 말고 철회로 기록하라** — 왜 그렇게 갔는지가 사라지면 같은 논의를 다시 한다.

## 2. 산출물 — 기존 파일 **둘을 고친다** (새 파일 금지)

### (1) `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-004-projects.md` — 주 개정

- **`## Decision` → `### 채택`** 에 신규 결정을 **D-11 부터 이어 붙인다.**
  기존 D-01~D-10 의 번호·본문은 **건드리지 마라** (이미 인용되고 있다).
  `_RESUME` §2 의 각 행에 대해 **무엇을 정했나 / 왜 / 근거(`파일:줄` 또는 사용자 원문)** 를 단다.
- **사용자 결정 / 코디 판단**을 계속 갈라 적는다 — §2 의 「근거」 열이 그것을 구분해 뒀다.
- **`## Open Questions` 절을 「닫힘」으로 바꾼다.** 9건을 지우지 말고 **각 건에 결론과 근거를 단다**
  (어느 결정 번호로 닫혔는지 가리킨다). 「미결 0건」이 되어야 한다.
- **철회 기록**: 「중심+직속 하위 2단계」 제안이 왜 섰고 왜 철회됐는지를 `### 기각` 또는
  별도 한 절에 남긴다. 철회 근거는 **선행에 깊이 제한이 없다**는 사실이다
  (`application.py:1116-1158` — 같은 프로젝트·읽기·자기자신·중복·순환만 본다).
- **`## Scope`** 갱신 — In Scope 에 새로 들어온 넷을 더한다:
  손자 프로젝트 종속 수정 · 자동 초대 · 자동 해제 · 간트 재귀.
  Out Of Scope 는 그대로 두되 사이드바(내비 순서)를 명시적으로 넣는다.
- **`## Resulting Spec`** — 「미결 9건을 닫은 뒤 발주한다」를 **「닫혔다. SPEC-005 발주 가능」**으로.

### (2) `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-004-projects.md` — 사실 보강

**결정을 쓰지 마라. 사실만 더한다.**

- **「조사가 드러낸 어긋남」 절에 두 건을 추가**한다 (이미 있는 ①②와 나란히):
  - **손자의 `project_id` 가 「만든 순서」에 따라 갈린다** — 생성 때는 상속되는데
    (`application.py:365-367` `project_for`: parent 있으면 부모 것을 그대로 반환)
    **옮길 때는 직속 하위만 갱신한다** (`application.py:532-536` + `work_tasks.py:475-482`
    `children_of` 는 `WHERE parent_task_id == task_id`). 하위는 자기 프로젝트를 직접 못 바꾸므로
    (`application.py:522-524`) **손자는 영영 프로젝트 밖에 남는다**
  - **배정·발송이 「받는 사람이 그 프로젝트를 읽을 수 있나」를 안 본다** — `project_for` 의 parent
    경로가 `readable_project_ids` 검사를 건너뛴다. 조직 축에서 온 후보는 프로젝트 밖 사람일 수 있고
    (`projects.py:281-296` `assignable_members` 주석이 프로젝트 축 후보는 멤버뿐이라고 적는다),
    그러면 그 사람은 **자기가 하는 일의 프로젝트를 못 읽는다**
- **「관측」에 요청 업무의 트리 모양을 사실로 적는다** — 사용자 원문 그대로 인용:

  > 「나 / 보고서작성 (상위) / |-보고서 디자인 업무요청 (하위 , 디자이너요청)
  >  디자이너 / 보고서 디자인 업무요청(수락) / |- 디자인 시안 조사(하위)」

  그리고 이것이 **설계대로 되는 모양**이라는 근거: `_is_central_task`(`application.py:457-469`) —
  「부모를 든 사람 ≠ 이 업무를 든 사람이면 중심 업무」, 주석이 「다른 사람이 수락한 요청 업무는
  그 사람의 새 중심 업무이고, 그래서 자기 직속 하위와 하위 요청을 가질 수 있다」(정책 V-7·P-3).
  → **요청을 주고받으면 3층이 예외가 아니라 기본값이다.**
- **선행에 깊이 제한이 없다는 사실**과, 그래서 2단계로 자르면 시안 `DepLines` 의
  `if (!a || !b) return`(`projects.v1.jsx:85-106`)로 **의존선이 조용히 사라진다**는 관측.
- **요청 발송 시 프로젝트가 이미 상속된다는 사실**(사용자 질문으로 확인된 것):
  `requests.py:371-375` 가 `project_for` 를 그대로 지나고, 주석이 「하위 요청은 묻지 않고 상위를 따른다」.
  그리고 **수락은 새 업무를 만들지 않는다** — `requests.py:457-458` 주석
  「같은 업무의 담당이 확정된다 — 새 업무가 생기지 않는다」.

## 3. allowed_paths

- **쓰는 파일은 위 둘뿐이다.** 색인(`README.md` 둘)·`log.md` 는 **건드리지 마라** — 코디가 갱신한다.
- 조사 리포트·시안·다른 spec/WP 는 읽기 전용. **커밋·push 금지.**

## 4. 범위 제약 — 하지 말 것

- **§2 에 없는 결정을 만들지 마라.**
- **계약 조문(필드명·에러코드·엔드포인트 시그니처)을 쓰지 마라** — SPEC-005 몫이다. 윤곽까지다.
- **Phase·일정·구현 순서를 쓰지 마라** — WORK-005 몫이다.
- 기존 D-01~D-10 의 번호와 본문을 **바꾸지 마라.** 다른 절이 그 번호를 가리킨다.
- 문서를 **새로 쓰지 마라.** 기존 파일을 고치는 일이다.

## 5. 검증

- `_RESUME` §2 의 **27행이 모두** 두 문서 어딘가에 반영돼 있다 (기존 10 + 신규 17).
- `## Open Questions` 가 **미결 0건**이고, 9건 각각에 **닫은 결정 번호와 근거**가 달려 있다.
- 「중심+직속 2단계」 **철회가 기록**돼 있다.
- BASE-004 의 어긋남이 **4건**이다 (기존 2 + 신규 2).
- 사용자 원문(요청 트리 그림)이 **인용 그대로** 들어 있다.
- 모든 신규 문장에 **근거(`파일:줄` 또는 사용자 원문)** 가 붙어 있다.
- `updated_at` 을 `2026-09-21` 로 두고 frontmatter 나머지 키는 그대로.
- **지정한 두 파일 밖의 변경이 0건** — `git status --porcelain` 결과를 보고에 적어라.

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 과 아래가 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_6e5b7cfe-820e-4b81-8189-1346a4fcb3a3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "writer 완료: BASE-004 · DEC-004 개정" \
  --body "반영한 신규 결정 수 / Open Questions 닫힘 여부 / 철회 기록 위치 / 어긋남 4건 여부 / git status 결과 / 미결·주의점"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] writer 완료 — BASE-004·DEC-004 개정. 상세는 인박스." --enter
```

- 막히면 같은 방식으로 물어라:
  `orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a --text "[질문] writer: <질문>" --enter`
