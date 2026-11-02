# [writer] BASE-004 · DEC-004 — 「프로젝트」 화면: 시안·조사 2건을 사실로 눕히고, 결정 10건을 근거와 함께 박는다

너는 **strong-hajin `writer` 워커**다. **너는 이 작업의 맥락이 하나도 없다.** 아래를 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/_RESUME.md` ← **이 작업의 정본.** §2 결정표가 DEC-004 의 재료다
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/design-read-projects.md` ← 코디가 시안을 읽고 정리한 것 (틀·부품·색·상호작용 + 요구 사실 D-1~D-9)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-be-domain.md` (726줄) ← 백엔드 조사
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-fe-structure.md` (500줄) ← 프론트 조사

작업 워크트리: **`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`** (코디 워크트리에 직접 탄다 — 너는 별도 워크트리가 없다)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 이 워크트리에는 **코디네이터가 함께 있다.** 지정된 두 파일 밖은 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

**꼴의 정본은 직전 판이다.** frontmatter·절 구성·말투를 여기서 그대로 가져와라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-003-calendar.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-003-calendar.md`
- 색인 규칙: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/README.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/README.md` (**읽기만** — 색인 갱신은 코디 몫)

**내용의 정본**:
- 시안: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/package 2/` (Projects.html · handoff/projects/**)
- 코드 사실: 위 조사 리포트 2건. **리포트의 `파일:줄` 근거를 그대로 물려라.**
- 이미 확정된 상위 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-004-calendar-scheduling.md:1165-1180`
  (「시안 목데이터 어휘와 계약 어휘」 표 — **시안을 계약으로 올리지 않았다는 기록**의 서식 선례다)

**기대는 개념** — `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/areas/concept/` 에서 `single-source-of-truth` 를 확인하고
frontmatter `up:` 에 직전 판과 같은 방식으로 넣어라. 없는 개념을 지어내지 마라.

## 2. 배경 / 무엇을 쓰나

회의·업무 워크스페이스에 「프로젝트」 화면을 만든다. 확정 시안이 있고, 코드 조사 2건이 끝났고,
**사용자와 결정 10건이 닫혔다.** 그것을 문서 두 장으로 눕히는 것이 이번 일이다.

**사용자 원문** (baseline 에 그대로 인용할 것 — 요약하지 마라):

> 「시안은 레이아웃 색 위치 등을 보려고 만든거고 상태값 논리구조는 이미 우리 있는 구조를 정본으로 할거야」
> 「그래서 일단 시안 구조를 탐색하고 → 우리 프론트/백 워커 보내서 조사를 할거야」
> 「프론트는 거의 다시 그린다고 보면돼」
> 「b가 메인인데 a도 해야 하잖아 … b를 하는데 어차피 검증에서 걸리니까 a까지 하고 갈거라고」
>   (a = `material_*` 계약 테스트의 병렬 경합. 재료는 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-21-strong-hajin-calendar/material-parallel-isolation.md`)
> D-3 진행률: 「체크리스트로 계산하자」
> 관리 기능: 「별도 모달로 옮긴다」

## 3. 산출물 — 파일 **정확히 둘**

### (1) `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-004-projects.md`  (id `BASE-004`, status `raw`)

**사실만 눕힌다. 판단·결정·설계를 쓰지 마라.** 들어갈 것:

- **입력** — 확정 시안(무엇을 어디에 어떤 색으로: `design-read-projects.md` §1~§7 을 물려라) · 위 사용자 원문
- **화면이 요구하는 사실 D-1~D-9** 와 **우리 코드의 실제 모양** 대조표
  (BE 리포트 §1 · FE 리포트 §3-4 를 합친다. **판정·근거 `파일:줄` 을 유지**)
- **부품 재고** — 있다 13 / 다르다 4 / 없다 2 (FE §2). **새로 만들 것이 사실상 간트·의존선 둘**이라는 관측
- **조사가 드러낸 어긋남** — BE §5 의 6건, FE §6 의 7건 중 **이 화면에 닿는 것**만 골라 적는다.
  특히 ① 프로젝트 상세 `tasks[].state` 가 `_external_state()` 를 안 지나 `completion_submitted` 가 새는 것
  ② `tasks_in()` 이 done·cancelled 를 안 거르고 페이징이 없는 것
- **전제를 뒤집은 것** — SPEC-001 U-3:200 이 「진행률은 쓰지 않는다」고 **의식적으로 배제**했고,
  시안은 그 결정을 모른 채 네 자리에서 % 를 그린다는 사실 (BASE-003 의 「조사가 뒤집은 전제」 절과 같은 자리)

### (2) `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-004-projects.md`  (id `DEC-004`, status `proposed`)

**`_RESUME.md` §2 의 결정 10건을 근거와 함께 옮긴다. 새 결정을 만들지 마라.**

- 각 결정에 **무엇을 정했나 / 왜 / 근거(`파일:줄` 또는 사용자 원문)** 를 단다
- **사용자 결정과 코디 기본값을 구분해 표시하라** — §2 표의 「근거」 열이 그것을 갈라 적어 뒀다.
  코디 기본값 셋(체크리스트 없는 업무의 %, 상위 바의 %, 전체 진행률의 분모)은 **「코디 기본값 — 사용자 정정 가능」**으로 명시
- **시안을 계약으로 올리지 않은 목록**을 SPEC-004:1165-1180 의 표 서식으로 만든다
  (시안 목데이터 → 우리 계약 → 근거). `status` 5종 · `progress` · `group`(분류) · `task_dependencies` 이름 등
- **결정이 낳는 변경의 윤곽**만 적는다 (계약 조문은 SPEC-005 몫):
  프로젝트 상세 `tasks[]` 확장 · 버그 ① 수정 · 3레일 전환 · 간트/의존선 신설 · 관리 모달 분리

## 4. 미결 — **추측으로 메우지 마라.** 아래는 아직 안 정해졌다

DEC-004 의 「미결 사항」 절에 **질문 형태로** 남긴다. 답을 지어내면 반려다.

1. **손자 업무(2단계 초과)를 간트에 어떻게 그리나** — 시안은 1단계만 그리는데 저장 깊이는 무제한이고
   (BE §D-5), 프로젝트 상세 `tasks[]` 는 깊이와 무관하게 **평평한 배열**로 손자까지 싣는다
2. **좌 레일 카드 클릭의 뜻** — 시안은 「선택」, 우리 업무 화면은 「드로어 열기」(FE §4-1). 같은 부품이 다른 뜻이 된다
3. **관리 모달을 여는 손잡이가 어디에 서나** — 헤더? 셀렉터 옆? (시안에 자리가 없다)
4. **읽을 수 있는 프로젝트가 0개인 사용자**의 화면 (BE §4 — 정상 상태인데 시안에 그 상태가 없다)
5. **`cancelled` 간트 바 색** — 시안 CSS 에 정의가 없다 (`projects.css` 에 `--cancelled` 없음)
6. **`Empty` 글리프 20px ↔ 시안 24px** — 고치면 소비처 29곳이 함께 움직인다 (FE §4-3 C)
7. **`AppHeader` 에 `titleEnd` 슬롯을 더할지** — 더하면 5개 화면이 공유하는 셸이 움직인다
8. **내비 순서** — 시안은 업무→프로젝트→캘린더, 우리는 업무→캘린더→프로젝트 (FE §1-3)
9. **버그 ②(`tasks_in()` 필터·페이징)를 이번 범위에 넣을지** — 코디는 범위 밖으로 제안했고 사용자 확인 전이다

## 5. allowed_paths — 이 밖은 건드리지 마라

- **쓰는 파일은 위 둘뿐이다.** 색인(`00-baseline/README.md` · `10-decision/README.md`)과
  `log.md` 는 **건드리지 마라** — 코디가 갱신한다.
- 조사 리포트·시안·기존 spec/WP 는 **읽기 전용**이다.
- **커밋·push 금지.**

## 6. 단계

1. 역할 문서 · `_RESUME.md` · 리포트 3건 읽기
2. 직전 판(baseline-003 · decision-003)의 frontmatter·절 구성 확인
3. BASE-004 작성 → DEC-004 작성 (links 를 서로 걸고, SPEC-004·SPEC-001 을 related 로)
4. 자기 검증(§8) → 완료 보고

## 7. 범위 제약 — 하지 말 것

- **결정을 만들지 마라.** §2 에 없는 결정은 §4 의 미결로 간다.
- **계약 조문(필드·에러코드·엔드포인트)을 쓰지 마라** — SPEC-005 의 몫이다. DEC 는 윤곽까지다.
- **구현 계획·Phase·일정을 쓰지 마라** — WORK-005 의 몫이다.
- 조사 리포트를 **요약하지 마라.** 이 화면에 닿는 사실을 **근거와 함께 옮겨라**.
- 코드를 고치지 마라. 색인·로그를 고치지 마라.

## 8. 검증

- 두 문서의 frontmatter 가 직전 판과 **같은 키 구성**이고 `links` 가 서로를 가리킨다
- 결정 10건이 **하나도 빠지지 않았다**. 사용자 결정 / 코디 기본값이 구분돼 있다
- 모든 사실에 **근거(`파일:줄` 또는 사용자 원문)** 가 붙어 있다
- §4 의 미결 9건이 **질문 그대로** 남아 있다 (답이 적혀 있으면 실패다)
- 소문자 `<…>` 자리표시자가 **하나도 남지 않았다**
- 지정한 두 파일 **밖의 변경이 0건**이다 — `git status --porcelain` 으로 확인해 보고에 적어라

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이라 오래됐을 수 있다. preamble 과 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_0928f39c-7725-469b-8d49-9e3856e1665b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "writer 완료: BASE-004 · DEC-004" \
  --body "쓴 파일 2개 경로 / 결정 10건 반영 여부 / 미결 9건 유지 여부 / git status 결과 / 미결·주의점"

# (2) 직접 주입
orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] writer 완료 — BASE-004·DEC-004 작성. 상세는 인박스." --enter
```

- 막히면 30분 이상 헤매지 말고 같은 방식으로 물어라:
  `orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a --text "[질문] writer: <질문>" --enter`
