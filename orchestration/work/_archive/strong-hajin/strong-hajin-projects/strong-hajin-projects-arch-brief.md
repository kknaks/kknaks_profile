# [architect] SPEC-005 — 「프로젝트」 화면: DEC-004 의 결정 27건을 계약 조문으로 내린다

너는 **strong-hajin `architect` 워커**다. **너는 이 작업의 맥락이 하나도 없다.** 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
  (⚠ `skills.md` 가 말하는 `scripts/lint-pipeline.py` 는 **이 리뉴얼 레포에 없다.** 린트는 건너뛰고 수동 검증만 해라)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-004-projects.md` ← **이번 스펙의 유일한 입력.** 결정 27건(D-01~D-27)·미결 0건
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-004-projects.md` ← 사실·관측(어긋남 ①~⑤·부품 재고·D-1~D-9 대조)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/design-read-projects.md` ← 시안의 틀·부품·색·상호작용·기하
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-be-domain.md` (726줄) · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-fe-structure.md` (500줄) ← 근거 `파일:줄` 의 출처

작업 워크트리: **`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`** (코디 워크트리에 직접 탄다)
⚠ 코디네이터가 같은 워크트리에 있다. **지정한 파일 하나 밖은 건드리지 마라.**

## 1. SSOT — 꼴의 정본은 SPEC-004 다

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-004-calendar-scheduling.md` (1836줄) ← **절 구성·frontmatter·말투를 그대로 따른다**
  `## 1. Context` → `## 2. UX Contract` → `## 3. User Scenario` → `## 4. Interface Contract`
  → `## 5. Implementation Rules` → `## 6. Verification` → `## 7. Open Questions`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/README.md` ← **§ Data / Domain Boundary 를 반드시 읽어라.** SPEC 에 무엇을 두고
  무엇을 안 두는지가 거기 정해져 있다 (읽기만 — 색인 갱신은 코디 몫)
- 이어지는 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`(업무 목록·선행·기한) ·
  `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-003-task-lifecycle-v2.md`(상태·상위/하위·중심 업무)

**기대는 개념** — frontmatter `up:` 은 직전 판과 같은 방식으로 둔다. 없는 개념을 지어내지 마라.

## 2. 산출물 — 파일 **하나**

`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` (id `SPEC-005`, status `draft`, version `0.1.0`)

links 는 `baselines: BASE-004` · `decisions: DEC-004` · `specs: SPEC-001 · SPEC-003 · SPEC-004`.
**`works: []`** 로 둔다 — WORK 역참조는 넣지 않는다(직전 판정 F-2 의 규칙).

## 3. 계약에 담을 것

DEC-004 의 **결정 번호를 각 조문에 달아라** (예: 「… (D-16)」). 근거 없는 조문은 쓰지 마라.

### 3-1. UX Contract (§2)

- **틀** — 3레일. 좌 380px·우 342px(기존 토큰). 헤더는 제목 + `actions`(관리 손잡이, D-22)
- **좌 레일** — 헤더에 「업무」+건수 배지 + 프로젝트 `Select`. 카드는 기존 `scax-inbox-card` 재사용,
  **선택 상태만 추가**(D-21: 클릭 = 선택, 열기는 우 레일의 「업무 열기」). **「분류」는 싣지 않는다**(D-08)
- **요약 스트립** — 5칸. 전체·진행 중·지연·완료·전체 진행률. **전체 진행률 = 완료 업무 수 / 전체 업무 수**(D-04)
- **간트** — **깊이 제한 없는 재귀 트리**(D-16). twisty 는 자식이 있는 모든 깊이에 선다.
  들여쓰기 **깊이당 12px · 최대 5단**(D-18). 행 40px·하루 34px·라벨 200px·바 3종 높이는 시안 그대로.
  바 안 % 는 **체크리스트 기반**(D-01·D-02), **상위 바는 % 를 안 낸다**(D-03),
  **체크리스트가 없으면 % 를 안 그린다**(D-02), `cancelled` 는 배경 `fill-weak`·fill 없음·제목 취소선(D-25)
- **의존선** — 선행→후행 직각 3구간. **접힌 가지에 걸린 선은 접힌 부모 바에 끌어붙인다**(D-17).
  「조용히 사라지는 선」이 **없어야 한다** — 이것이 이 화면의 핵심 인수조건이다
- **우 레일** — 메타(상태·기간·담당·요청·상위) · 관계(선행/후행) · 체크리스트(읽기) · 하위 업무.
  **후행은 클라이언트가 `preceding_task_ids` 를 뒤집어 만든다**(D-07) — 서버 경로가 없다
- **관리 모달** — 참여자 붙이기/떼기 · 참여 이력 · 새 프로젝트(D-05). 여는 손잡이는 헤더 `actions`(D-22)
- **빈 상태** — 프로젝트 0개면 「담당 프로젝트가 없습니다」 하나(D-23). 업무 미선택은 우 레일 `Empty`
- **상태 어휘** — 백엔드 `TaskState` 가 정본, 시안 5종 폐기(D-06). 라벨·톤은 `labels.ts` 표

### 3-2. Interface Contract (§4)

- **`GET /api/projects/{project_id}` 의 `tasks[]` 확장** — 지금 6필드로는 화면을 못 그린다.
  더할 것과 **각각이 어느 결정 때문인지**를 적어라: 담당(D-08 대체) · 체크리스트 집계(D-01) ·
  하위 집계 · 기한 경과(요약 스트립 「지연」, D-04) · **`_external_state()` 적용**(어긋남 ①)
- **자동 초대**(D-11·D-12) — 업무를 배정·발송할 때 받는 사람이 그 프로젝트에 없으면 `참여`(member)로 붙인다.
  열쇠는 **`task.assign`**(`project.manage` 아님). **이미 붙어 있으면 아무 일도 안 일어난다**(멱등).
  적용되는 표면을 **전부** 적어라 — 요청 발송 · 직접 배정 · 담당 교체 제안까지 `task.assign` 이 지나는 자리를
  `research-be-domain.md` §2-1 의 표면 목록으로 **세어서** 확인하고, 해당하는 것만 계약에 넣어라
- **자동 해제**(D-13~D-15) — 거절·철회 시 **조건 둘을 모두 만족할 때만** 뗀다:
  ① 이 요청이 실제로 새로 붙였을 때 ② 그 사람이 그 프로젝트에 다른 활성 업무를 안 들고 있을 때.
  `end_reason` 으로 닫고 **행을 지우지 않는다**. **수락 뒤 취소·완료로는 떼지 않는다**(D-15)
- **손자 프로젝트 종속**(D-19) — 외부로 드러나는 계약은 「상위를 옮기면 **자손 전체**가 따라간다」다.
  `_require_project_unlocked` 게이트(남은 선행이 있으면 못 옮김)도 **자손 전체**에 걸린다 —
  거절이 어느 오류로 나가는지 적어라
- **에러** — 새로 생기는 거절 갈래를 **기존 오류 어휘와 나란히** 둔다. 기존 다섯 갈래는
  `research-be-domain.md` §D-4 에 이름이 그대로 있다. **이름을 새로 지어내기 전에 기존 것을 먼저 써라**

### 3-3. Verification (§6)

인수조건은 **관측 가능한 문장**으로. 최소한 이 넷은 들어가야 한다:

1. 3층 트리(요청 주고받은 모양)에서 **손자 행이 간트에 선다**
2. 손자에 걸린 **선행/후행 선이 그려진다.** 가지를 접으면 **접힌 부모 바에 붙는다** — 사라지지 않는다
3. 프로젝트 밖 사람에게 업무를 보내면 **그 사람이 프로젝트를 읽게 된다**. 거절하면 **떼어진다**(조건 둘 충족 시)
4. 상위를 다른 프로젝트로 옮기면 **손자까지 따라간다**

## 4. 범위 제약 — 하지 말 것

- **저장 구조를 쓰지 마라** — table schema·column·index·FK·migration 은 **WORK-005 의 Domain/Schema 몫**이다
  (`20-spec/README.md` § Data / Domain Boundary). 예: 「`work_requests` 에 칸 하나」 같은 말은
  **계약이 아니라 구현**이다. 외부로 드러나는 **행동**으로 쓴다
- **Phase·순서·일정·담당을 쓰지 마라** — WORK-005 몫이다
- **결정을 새로 만들지 마라.** DEC-004 에 없는 판단이 필요하면 **§7 Open Questions 로 올린다**
- **WORK 역참조를 넣지 마라** (`works: []`)
- 색인(`20-spec/README.md`)·`log.md` 를 건드리지 마라 — 코디가 갱신한다
- **커밋·push 금지**

## 5. 검증

- 결정 **27건 중 계약에 닿는 것이 모두 조문으로** 내려왔고, 각 조문에 **결정 번호**가 붙어 있다
- 저장 구조(컬럼·인덱스·마이그레이션) 서술이 **0건**이다
- 자동 초대가 적용되는 **표면을 세어서** 적었다 (「주요 경로」 같은 요약 금지)
- 인수조건 §3-3 의 넷이 **관측 가능한 문장**으로 들어 있다
- frontmatter 가 SPEC-004 와 같은 키 구성이고 `works: []` 다
- 소문자 `<…>` 자리표시자가 하나도 없다
- **지정한 파일 하나 밖의 변경이 0건** — `git status --porcelain` 결과를 보고에 적어라

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 과 아래가 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_2705274e-b68b-4cfe-a51b-eeec1e9f8f82 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "architect 완료: SPEC-005" \
  --body "파일 경로·줄 수 / 반영한 결정 번호 범위 / 자동 초대 표면 개수 / 인수조건 수 / Open Questions 수 / git status 결과 / 주의점"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] architect 완료 — SPEC-005 작성. 상세는 인박스." --enter
```

- 막히면 같은 방식으로 물어라:
  `orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a --text "[질문] architect: <질문>" --enter`
