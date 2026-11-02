# 리뷰 리포트 — strong-hajin-projects / frontend 루프2 **Phase FE-5** (2026-09-22)

**역할** `@sc-ax-reviewer` · **task-id** `task_031420060ac7` · **워크트리**
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` (브랜치 `kknaksss/strong-hajin-projects`)
**read-only** — 코드·문서 0줄 수정 · 커밋 0건 · 개발 서버 0회.
뮤테이션 **16건**과 probe **2건**은 전부 백업본으로 되돌리고 `cmp` 로 **바이트 동일**을 확인했다
(probe 파일 `ZProbe.test.tsx` 는 삭제 · `git status` 에 남은 흔적 0건).

## 판정: **FAIL** (FAIL 1 · WARN 6)

**계약을 깨뜨린 자리는 딱 하나**다 — 그리고 그것은 **조용하다.** 요청 업무의 「완료」가
완료 보고 모달로 가는 것까지는 맞는데(L-31 참), **그 모달이 서버에 거절당하면 화면 어디에도
아무 말이 안 나온다.** 가져다 쓴 부품의 **유일한 오류 통로를 빈 함수로 막아 놨기 때문**이고,
「부품을 고치지 않고 가져다 쓴다」(D-32)의 반대쪽 실수다.

**그 밖은 실측으로 참이다.** 백엔드가 찍어 준 **열두 자리는 열두 개 다 바르게 처리**됐고
(②·⑥·⑩ 은 뮤테이션으로 빨강 확인), **상태 관문 열 개도 열 개 다 코드에 있다.**
빈 상태 생성 버튼(L-15)·네 칸 모달(L-19)·관리 모달 보존(D-30)·레일 머리 한 줄(L-34)·
`ref`/`data-task-id` 생존(L-46)도 전부 섰다. **앞 판 FAIL(waitFor 없는 비동기 읽기)과
WARN-1(자기참조 단언)은 재발하지 않았다** — 그 자리는 리터럴 + `waitFor` 로 고쳐져 있다.

**WARN 여섯 중 셋은 「§6 의 고백이 충분한가」에 대한 것**이다. §6-2(관문 「아」)는 **정직한 고백이
아니라 더 물 수 있는데 안 문 것**이고 — **12줄짜리 결정적 테스트를 내가 실제로 세워서 증명했다** —
**§6 이 아예 말하지 않은 무관측 갈래가 둘 더 있다**(BE ⑪ 의 다시 읽기 · 완료 보고 뒤 다시 읽기).

---

## 검수 범위

- **대상**: FE-5 가 만진 **아홉 파일**. `git diff` 가 범위를 못 준다(워크트리에 1루프·Phase 0·
  BE-3·FE-4 가 커밋 0건으로 쌓여 있고 `features/project/` 는 통째로 untracked 다) —
  **mtime 으로 갈랐다.** 워커 세션 시작(14:29) 이후 `frontend/src` 에서 바뀐 파일:

  ```
  14:39:30 src/App.tsx                              14:52:19 src/features/project/ProjectCreateModal.tsx
  14:39:46 src/styles/index.css                     14:52:19 src/features/project/ProjectPage.tsx
  14:40:25 src/styles/projects.css                  14:52:19 src/features/project/ProjectRail.tsx
  14:45:57 src/features/project/ProjectPage.test.tsx 14:52:19 src/features/project/ProjectTaskPanel.tsx
                                                    14:52:19 src/lib/labels.ts
  ```
  **정확히 아홉이고 리포트 §1 의 목록과 한 파일도 어긋나지 않는다.**
  `projectModel.ts`(14:19) · `ProjectGantt.tsx`(14:25) 는 **FE-4 의 것**이고 세션 전이다.
- **실행한 검사**: `npx tsc --noEmit` · `make frontend-test` **4회** ·
  `vitest run ProjectPage.test.tsx` **약 20회**(뮤테이션 16 + probe 2 + 기준선) ·
  `git diff --stat` (공유 자산) · `find -newermt` (범위) · CSS 토큰 실값 대조.
- **범위 밖으로 둔 것**: BE-3 · FE-4 · 1루프 · Phase 0 · 루프3 이월 · SPEC 미결(OQ-604 · OQ-607).

---

## 위반 (FAIL)

### [FAIL-1] 완료 보고가 거절되면 **화면이 아무 말도 안 한다** — 가져다 쓴 부품의 유일한 오류 통로를 막았다

- **무엇이**: `frontend/src/features/project/ProjectTaskPanel.tsx:359`
  ```tsx
  <CompletionReportModal ... onError={() => undefined} ... />
  ```
  `CompletionReportModal` 은 **자기 안에 오류를 그리는 자리가 없다.** 보내기가 거절되면
  `WorkModals.tsx:2270` 의 `catch` 가 **`onError(문구)` 로만** 말한다 —
  그 통로를 빈 함수로 받으면 **문구가 갈 곳이 없다.**
- **실측(probe)**: 원본 그대로에 테스트 한 건을 세워 요청 업무의 완료 → 모달 → 요약 입력 →
  「보고 보내기」를 눌렀고 `submitTaskCompletion` 이 `Error("이미 처리된 보고입니다")` 로 거절하게 했다.

  ```
  AssertionError: expected '프로젝트 관리프로젝트9한빛의원 통합 마케팅진행 중한빛 9월 통합 마…'
                  to contain '이미 처리된 보고입니다'
  ```
  **`document.body` 전체에 그 문구가 없다.** 모달은 열린 채로 남고, 사람은 버튼을 눌렀는데
  아무 일도 안 일어난 화면을 본다. (probe 파일은 지웠다.)
- **어느 인수조건과 어긋나나**: SPEC-005 §2.6 ②-**사** — 요청 업무의 완료가 가는 곳이
  「**올바른 경로**」인 완료 보고 모달이라는 계약. 그 경로의 **거절이 관측 불가능하면 경로가
  아니라 막다른 길**이다. 그리고 **D-32 「업무 화면 로직 그대로」** — 선례
  `MyWorkPage.tsx:1115-1116` 은 `onError={onError}` · `onNotice={onNotice}` 를 **그대로 넘긴다.**
  부품을 안 고친 것은 맞지만 **부품의 입력을 무력화한 것은 「그대로」가 아니다.**
  (같은 이유로 `onNotice` 도 안 넘어가 **「완료 보고를 보냈습니다」 확인 문구도 없다.**)
- **수정안 한 줄**: `ProjectPage` 가 이미 쥔 `onError` 를 `ProjectTaskPanel` → `TaskStateValue` 로
  내려 `onError={onError}`(+ 선택적으로 `onNotice`)로 넘긴다 — 전이 실패가 이미 그 통로로 간다.

---

## 경미 (WARN)

### [WARN-1] §6-2 의 「흔들리는 테스트가 된다」는 **사실이 아니다** — 관문 「아」는 12줄로 결정적으로 물린다

- **무엇이**: 워커 리포트 **§6-2**. 「`busy` 가 `ProjectPage` 의 상태이고 레일이 등록 effect 를
  거쳐 다시 그려지므로 보내는 중 프레임을 안정적으로 잡으려면 흔들리는 테스트가 된다」.
- **실측**: 지연 promise 하나 + `waitFor` 로 **결정적인 테스트가 된다.** 내가 세워서 돌렸다.

  ```tsx
  vi.mocked(api.transitionDirectTask).mockImplementation(() => new Promise(...));  // 안 끝난다
  … 완료를 고른다 …
  await waitFor(() => expect(trigger.hasAttribute("disabled")).toBe(true));
  ```
  **원본에서 초록**(51/51) · **`disabled={busy}` 를 뺀 뮤테이션에서 빨강**
  (`AssertionError: expected false to be true`). `waitFor` 가 등록 왕복을 그대로 흡수한다 —
  「보내는 중 프레임을 잡는」 경주가 없다.
- **어긋나는 것**: SPEC 인수조건이 아니라 **리포트 §6 의 신뢰성**이다. §6 은 「정직한 고백」의
  자리인데 이 한 줄은 **못 문 것이 아니라 안 문 것**이고, 그래서 관문 열 중 하나가
  「사용자 2차 E2E 가 유일한 관측자」로 넘어갔다.
- **수정안 한 줄**: 위 세 줄짜리 단언을 `ProjectPage.test.tsx` 에 더한다(관문 「아」가 닫힌다).

### [WARN-2] **BE ⑪ 의 「다시 읽기」에 관측자가 0건**이다 — §6 이 말하지 않았다

- **무엇이**: `ProjectPage.tsx:179-184` — 프로젝트 상세를 못 읽으면 `void reload()` 로
  **목록부터** 다시 읽는다. 리포트 §2-⑪ 이 「이 자리가 ⑪ 을 처리한 자리」라고 적은 바로 그 줄이다.
- **뮤테이션 실측(R13)**: `void reload();` **한 줄을 지워도 50/50 전건 통과.**
  `refreshAfterWrite` 의 `.catch(() => reload())` 도 같다 — 그 갈래를 타는 테스트가 없다.
- **어긋나는 것**: 인수조건이 아니라 **리포트 §3·§6 의 대조표**다. 관문·열두 자리 표는
  「테스트가 무는가 ✅」와 「구현이 있다」를 같은 칸에 적는데, ⑪ 은 **구현만 있고 관측이 없다.**
  §6 「테스트가 못 무는 자리」에 **이 자리가 없다.**
- **수정안 한 줄**: `getProject` 를 한 번 거절시키고 `listProjects` 가 **두 번째로 불리는지**
  재는 단언 하나를 더한다.

### [WARN-3] **완료 보고 뒤 「다시 읽기」에도 관측자가 0건**이다 — 역시 §6 에 없다

- **무엇이**: `ProjectTaskPanel.tsx:364` — `await onChanged?.()`.
  보고는 전이를 안 지나고 상태를 옮기므로 **이 줄이 유일한 다시 읽기**다(③-차의 그 규칙).
- **뮤테이션 실측(R18)**: 그 줄을 지워도 **50/50 전건 통과.** L-31 테스트는 **모달이 뜨는 것까지만**
  재고 그 뒤를 안 따라간다.
- **어긋나는 것**: SPEC §2.6 ③-**차**(「성공하면 다시 읽는다」)의 **완료 보고 쪽 절반**.
  전이 쪽 절반은 L-52 가 양쪽(성공·실패)을 다 문다 — **보고 쪽만 비어 있다.**
- **수정안 한 줄**: probe 와 같은 꼴로 보고를 성공시키고 `getProject` 재호출을 재는 단언 하나.
  **FAIL-1 을 고치는 테스트와 같은 자리**라 한 번에 닫힌다.

### [WARN-4] L-33 의 둘째 단언이 **자기참조**다 — 테스트가 «자기 픽스처»를 단언한다

- **무엇이**: `ProjectPage.test.tsx:940-942`
  ```tsx
  const rows = (await vi.mocked(api.getProject).mock.results[0].value) as {...};
  expect(rows.tasks.filter((row) => "checklist" in row || "description" in row)).toEqual([]);
  ```
  `rows` 는 **이 테스트가 방금 `mockResolvedValue` 로 넣은 그 객체**다. 화면 코드가 무엇을 하든
  이 줄은 **절대 빨강이 되지 않는다** — 재는 것은 픽스처의 모양이지 구현이 아니다.
- **어긋나는 것**: 앞 판 검수가 세운 기준(`review-loop2-fe4-report.md` WARN-1 —
  「기대값을 구현/상수에서 되계산하는 단언은 아무것도 붙들지 않는다」). 리포트 §5 의
  **「자기참조 단언을 반복하지 않았다」는 이 한 줄에서만은 참이 아니다.**
  (같은 테스트의 **첫 절반**(`getTask` 호출 1회 · 대상이 `t-5`)은 진짜다 — M32 가 그것을 문다.
  L-33 의 「선택된 하나에만」은 지켜지고 관측된다.)
- **수정안 한 줄**: 그 줄을 지우거나, 픽스처 대신 **화면이 그린 것**을 재게 바꾼다 —
  예: 상세를 영원히 pending 으로 두고 우 레일에 설명·항목이 **안 그려지는 것**을 잰다.

### [WARN-5] 목이 테스트 사이에 **안 털린다** — `not.toHaveBeenCalled()` 가 선언 순서에 기댄다

- **무엇이**: `ProjectPage.test.tsx:189` 의 모듈 수준 `const noop = vi.fn()` 과
  `vite.config.ts` 에 **`clearMocks` 가 없는 것**. `renderPage` 는 `getProject`·`getTask` 만 털고
  `createProject` 는 안 턴다.
  - `:777` `expect(api.createProject).not.toHaveBeenCalled()` 는 **그 앞의 어느 테스트도
    `createProject` 를 안 불렀다는 사실**에 기댄다(오늘은 참이다 — 순서가 바뀌면 거짓이 된다).
  - `:1113` `expect(noop).toHaveBeenCalledWith("선행 업무가 끝나지 않았습니다")` 는
    **파일 전체에 누적된** `noop` 를 본다. 문구가 유일해서 오늘은 맞다.
- **어긋나는 것**: 규칙 문서가 아니라 **단언의 내구성**이다. 이 판정에 넣지 않는다(오늘은 초록).
- **수정안 한 줄**: `vite.config.ts` 의 `test` 에 `clearMocks: true` 를 넣거나
  `afterEach` 에서 `noop.mockClear()` 한다.

### [WARN-6] 한국어 리터럴 한 개가 `labels.ts` 밖에 있다 — 다만 **선례가 똑같다**

- **무엇이**: `ProjectTaskPanel.tsx:366` — `: "요청자"`.
  근거: `roles/strong-hajin/reviewer/rules.md` frontend 「한국어 문자열이 `labels.ts` 밖에
  흩어지지 않았나」.
- **감경**: 선례 `MyWorkPage.tsx` 의 같은 자리가 **글자 그대로 같다.** 「선례를 그대로 옮긴다」와
  충돌하는 자리라 **위반으로 단정하지 않고 WARN** 으로 남긴다(rules.md 「모호하면 WARN」).

---

## 13항목 결과

| # | 항목 | 결과 | 근거 |
|---|---|---|---|
| 1 | 백엔드 **열두 자리** | **PASS 12/12** | 아래 대조표. ②·⑥·⑩ 은 뮤테이션 빨강으로 확인 |
| 2 | 상태 관문 **열 개** | **구현 10/10** · **관측 8/10** | 아래 대조표. 「라/마」는 겹침(구조), 「아」는 무관측(WARN-1) |
| 3 | 생성 버튼 게이트 = `project.manage` | **PASS** | `App.tsx:538` `has("project.manage")` → `canCreateProjects`. 관리는 `selected?.may_manage` **한 곳뿐**(`ProjectPage.tsx:410`). 섞으면 빨강(R7 2건). 빈 상태 갈래도 선다(`:426-437` · R8 빨강) |
| 4 | 생성 모달 네 칸 · `external_key` 없음 · 거절 네 갈래 | **PASS** | `ProjectCreateModal.tsx` 칸 넷 · 테스트가 `.scax-field` 수를 **리터럴 4** 로 잰다 · ② 는 화면이 막고(`:59`·`:78`) ①③④ 는 **서버 문구 그대로**를 모달 «안»에서 낸다(`:93`) |
| 5 | 관리 모달의 기존 생성 폼 | **PASS — 그대로 있다** | `ProjectManageModal.tsx` **mtime 00:54:34**(FE-5 세션 전) · 테스트가 「새 프로젝트」 region 과 「열기」 버튼을 들고 있다 |
| 6 | 좌 레일 머리 한 줄 + 건수 배지 · FE-4 의 `ref`·`data-task-id` | **PASS** | `ProjectRail.tsx:86-91` 한 줄 · `Badge variant="count"` **기존 부품** · **`:108` 의 `ref={list}` 와 `:133` 의 `data-task-id` 살아 있다** · L-46 회귀 테스트 초록 |
| 7 | 우 레일 블록 순서 | **PASS** | `ProjectTaskPanel.tsx:117 · 164 · 209 · 215` = 메타 → 업무 정보(설명+체크리스트) → 관계 → 하위. 테스트가 **리터럴 배열**로 잰다 |
| 8 | 메타 표 셋 | **PASS(코드·값 기준)** | 정렬선: 세 부품의 좌 padding 이 **전부 `space-200`**(`components.css:36` 배지 · `:45` 트리거 · `projects.css:172` 관계 줄)이고 `:162` 가 **정확히 그 값만큼** 음수 마진 → 계산이 맞다 · 행 높이: `:159` `min-height:28px` + `align-items:center` 통일 · 시인성: **두 자리가 같은 `.scax-pj-rel__item`**(테두리+배경, `:172`)이고 갈라 놓으면 빨강 |
| 9 | 공유 자산 0줄 | **PASS — 내가 직접 확인했다** | `git diff --stat -- src/ds/ components.css shell.css MyWorkPage.tsx WorkModals.tsx api.ts` → **빈 출력.** 더해서 **mtime**: `WorkModals.tsx`·`MyWorkPage.tsx` **09-21 19:33**(FE-5 세션보다 19시간 전) |
| 10 | 테스트가 실제로 무는가 | **뮤테이션 16건 — 13 빨강 · 3 초록** | 아래 「테스트 실측」. 초록 셋 중 **하나만 §6 이 고백**했고 **둘은 안 했다**(WARN-2·3), 고백한 하나도 **틀린 이유**였다(WARN-1) |
| 11 | 앞 판 FAIL 재발 | **재발 없음** | 새 단언의 비동기 읽기는 전부 `waitFor`/`findBy*` 안이다. 앞 판 FAIL-1 자리(`:393`)는 **`await waitFor(... toBe(68))`** 로, WARN-1 자리는 **리터럴 68·578** 로 고쳐져 있다. 다만 **새 자기참조 하나**가 다른 자리에 생겼다(WARN-4) |
| 12 | 범위 | **PASS** | `backend/src`·`backend/tests` 에서 **14:29 이후 바뀐 파일 0개** · `HEAD = e46ce39` **그대로(커밋 0건)** · 루프3 몫 0줄 · 개발 서버 0회(`5173`·`8100` 미기동) |
| 13 | 테스트 수치 재측정 | **PASS(이 판) · 새 흔들림 1건(이 판 밖)** | 아래 「테스트 실측」 |

---

## 백엔드 **열두 자리** 대조표 — 하나씩 실측

| # | 실물이 말한 것 | FE 가 한 것 | 내 검증 | 판정 |
|---|---|---|---|---|
| **①** | `access` 로 체크리스트를 감추지 마라 | `access` 를 읽는 자리는 **드롭다운 게이트 하나뿐**(`ProjectTaskPanel.tsx:312`) | **뮤테이션 R14**(`access==="owner"` 일 때만 항목) → **2건 빨강** | **PASS** |
| **②** | 키의 **«유무»**로 갈라라 (`.length` 는 터진다) | `:102` `detail?.checklist ?? null` — `.length` 직접 접근 **0건** | **R3**(`detail.checklist.length` 로 고침) → **13건 빨강.** `checklist` 키 **없는** 상세로 렌더하는 테스트가 따로 있다 | **PASS** |
| **③** | 미터 재료는 **프로젝트 상세 `tasks[]`** | `taskPercent(row)`·`row.checklist_progress`(`projectModel.ts:71-77` · `:88-89`) — 상세의 집계는 **안 읽는다** | 항목 없는 갈래에서 **`25%`·`1/4`** 를 리터럴로 재는 테스트 초록 | **PASS** |
| **④** | `references` 는 안 열렸다 | `grep -rn references src/features/project/` → **0건** | 내가 직접 grep | **PASS** |
| **⑤** | 리드라고 더 오지 않는다 | 게이트는 `access === "owner"` 하나. `may_manage`·리드 여부를 **안 본다** | `ProjectTaskPanel.tsx` 에 `may_manage` **0회**. `may_manage:true` 인 프로젝트 + `read_only` 업무 → 배지(테스트) | **PASS** |
| **⑥** | 쓰기 네 표면은 404 → 읽기 전용 | 체크리스트는 `li`/`span` 뿐(`:189-199`) | **R10**(`span` → `button`) → **1건 빨강.** 테스트가 `owner` + 역량 있는 세션에서도 `input,button,[role=checkbox]` **0개**를 잰다 | **PASS** |
| **⑦** | `tasks[]` 에 `checklist` 없다 | 상세는 **선택이 바뀔 때만** 한 번(`ProjectPage.tsx:148-170`) | 테스트가 `getTask` **호출 1회**와 대상 `t-5` 를 잰다(진짜 절반). 둘째 절반은 자기참조(**WARN-4**) | **PASS**(관측 절반) |
| **⑧** | `description` 은 네 갈래 전부에 온다 | 설명을 `access` 로 안 가른다(`:168`) | `read_only`+항목 갈래와 프로젝트 «밖» 갈래 **둘 다** 설명을 단언 | **PASS** |
| **⑨** | 초대는 목록 한 줄이 «느는» 것뿐 | 새 플래그를 기다리는 코드 **0건**. 목록은 `listProjects` 하나 | 코드 읽기 | **PASS** |
| **⑩** | 초대돼도 `may_manage` 는 false | 관리 손잡이 판정은 `selected?.may_manage` **한 곳**(`:410`) | **R7**(생성도 `may_manage` 로) → **2건 빨강.** L-16 테스트가 `may_manage:false` + 자격 있음 갈래를 잰다 | **PASS** |
| **⑪** | 거절 뒤 목록을 **다시 읽어라** | `:183` `void reload()` · `:261` `.catch(() => reload())` — **구현은 있다** | **R13**(그 줄 삭제) → **50/50 초록 — 관측자 0건** | **PASS(구현) / WARN-2(관측)** |
| **⑫** | 배정 거절 문구 그대로 · 초대 전용 오류 없다 | 새 오류 갈래 **0건**. 쓰기 둘 다 **서버 문구 그대로** | 생성(L-21 테스트)·전이(거절 테스트) 둘 다 서버 문구를 낸다 | **PASS** |

---

## 상태 관문 **열 개** 대조표 — SPEC §2.6 ①②③ 과 코드를 하나씩

| 관문 | 계약 | 코드 자리 | 내 뮤테이션 | 판정 |
|---|---|---|---|---|
| **가** 세션 역량 `task.self_manage` | 없으면 읽기 배지 | `ProjectTaskPanel.tsx:314` `!canManageOwnTasks` · `App.tsx:539` `has("task.self_manage")` | **R2** 게이트 제거 → **1건 빨강** | **PASS** |
| **나** 접근 값 `owner` | 아니면 배지(수락 전 배정 포함) | `:312` `detail.access === "owner"` | **R1** 제거 → **1건 빨강** | **PASS** |
| **다** 갈 곳이 있나 | 빈 배열이면 배지 | `:313` `allowedTaskTransitions(detail)` — **업무 화면 것 그대로** | 테스트가 `cancelled` · **승인 대기 `done`** · **대비군(승인 축 없는 `done` 은 드롭다운)** 셋을 잰다 | **PASS** |
| **라** 지금 상태를 다시 고름 | 무동작 | `:327` `if (next === detail.state) return;` | **R17**(라만) → **초록** · **R16**(라+마) → **1건 빨강** | **PASS(구현) · 겹침 확인** |
| **마** 허용 전이 밖 | 무동작 | `:328-329` `if (!picked) return;` | 같은 자리 — §6-1 의 설명이 **내 실측과 정확히 일치한다** | **PASS(구현)** |
| **바** 「막힘」 → 사유 프롬프트 | 사유 없이 전이가 안 나간다 | `:330-333` `setBlocking(true)` → `BlockReasonPrompt`(`:371-379`) | **R5**(바로 전송) → **1건 빨강.** 테스트가 **사유 입력 전 호출 0건**을 먼저 잰다 | **PASS** |
| **사** 요청 업무의 「완료」 → 완료 보고 모달 | 전이를 안 보낸다 | `:334-337` `isRequestTask(detail)` → `CompletionReportModal` | **R6**(전이로 보냄) → **1건 빨강.** 대비군(요청 아닌 업무는 그대로 전이)도 있다 | **PASS**(단 **FAIL-1** 이 그 모달의 오류를 삼킨다) |
| **아** 보내는 중 잠금 | 두 번 눌러 두 번 안 나간다 | `:346` `disabled={busy}` + `ProjectPage.tsx:276` `if (busy) return false` | **R12** 제거 → **50/50 초록**. 단 **내 probe 는 그 뮤테이션을 잡는다** | **PASS(구현) / WARN-1(관측)** |
| **자** 회차 동봉 | **업무 상세로 읽은** 회차 | `ProjectPage.tsx:279` `task.version`, `task` 는 `detail`(`ProjectTaskPanel.tsx:338`·`375`) | **R4**(1 로 고정) → **2건 빨강.** 테스트가 **리터럴 7** 로 잰다 — `tasks[]` 픽스처에는 그 키가 아예 없다 | **PASS** |
| **차** 낙관적 갱신 0 + 다시 읽기 | 성공 → 프로젝트 상세 **+** 업무 상세 / 실패 → 문구만 | `ProjectPage.tsx:257-264` · `:275-289` | **R11**(프로젝트 상세 미재조회) → **1건 빨강.** 테스트가 전이 뒤 **좌 레일 카드 텍스트**와 **`--done` 바 클래스**까지 본다. 실패 갈래도 `getProject` **1회**를 리터럴로 잰다 | **PASS(전이) / WARN-3(완료 보고 쪽)** |

> **③-차의 「다시 읽는 범위」**(우 레일만 고치지 않는다)가 **실측으로 참**이다 — R11 이 그것을 붙든다.

---

## 테스트 실측 — **내가 다시 쟀다**

### 수치

| 무엇 | 내 측정 | 워커 주장 | 일치 |
|---|---|---|---|
| `npx tsc --noEmit` (`frontend`) | **exit 0 · 에러 0** | 에러 0 | ✅ |
| `make frontend-test` | **70 파일 · 1010 테스트** | 70 · 1010 | ✅ |
| 그중 `ProjectPage.test.tsx` | **50건 전건 통과** | 50건 | ✅ |
| `projectModel.test.ts` | **13건** (안 건드렸다) | 13건 | ✅ |
| 회차 | **4회** — 3회 `1010 passed` · **1회 `1 failed`(이 판 밖)** | 6회 중 5회 전건 | 같은 모양 |
| **FE-5 파일의 실패** | **4회 + 뮤테이션 20여 회 중 0회** | 0회 | ✅ |

### 뮤테이션 **16건 — 13 빨강 · 3 초록**

모두 원본 파일을 백업하고 하나씩 무력화한 뒤 `ProjectPage.test.tsx` 를 돌렸고,
**매 회차 끝에 백업본을 덮고 `cmp` 로 바이트 동일**을 확인했다.

| 뮤테이션 | 결과 |
|---|---|
| R1 관문 「나」(`access==="owner"`) 제거 | **1건 빨강** |
| R2 관문 「가」(세션 역량) 제거 | **1건 빨강** |
| R3 체크리스트 키가 늘 있다고 믿음(`.length` 직접) | **13건 빨강** |
| R4 회차를 `1` 로 고정 | **2건 빨강** |
| R5 「막힘」을 사유 없이 바로 전송 | **1건 빨강** |
| R6 요청 업무의 「완료」를 전이로 전송 | **1건 빨강** |
| R7 생성 버튼을 `may_manage` 로 판정(두 게이트 혼동) | **2건 빨강** |
| R8 빈 상태 갈래에서 생성 모달 미렌더 | **1건 빨강** |
| R10 체크박스를 누를 수 있게(`span`→`button`) | **1건 빨강** |
| R11 전이 뒤 프로젝트 상세 미재조회 | **1건 빨강** |
| R14 `access` 로 체크리스트 감춤 | **2건 빨강** |
| R15 건수 배지 −1 | **2건 빨강** |
| R16 관문 「라」+「마」 둘 다 제거 | **1건 빨강** |
| **R12 관문 「아」(`disabled={busy}`) 제거** | ⚠ **초록** — 단 **내 probe 는 잡는다**(WARN-1) |
| **R13 프로젝트 못 읽어도 목록 미재조회(BE ⑪)** | ⚠ **초록** — §6 에 고백 없음(WARN-2) |
| **R17 관문 「라」만 제거** | ⚠ **초록** — §6-1 의 설명이 **참이다**(R16 이 빨강) |
| *(§6 밖)* **R18 완료 보고 뒤 `onChanged` 제거** | ⚠ **초록** — §6 에 고백 없음(WARN-3) |

### §6 「테스트가 못 무는 자리」는 정직한 고백인가 — **셋 중 하나만 참**

| §6 의 주장 | 내 판정 |
|---|---|
| **§6-1** 「라」·「마」는 단독으로 안 물린다 — 둘을 함께 빼면 빨강 | **참이다.** R17 초록 · R16 빨강으로 **글자 그대로** 재현됐다. 「버그가 아니고 두 줄이 같은 입력을 덮는 사실」이라는 설명도 맞다 |
| **§6-2** 관문 「아」는 흔들리는 테스트가 되어 못 세웠다 | **거짓이다.** 지연 promise + `waitFor` 로 **결정적**이다 — 원본 초록 · R12 에서 빨강. **더 물 수 있는데 안 문 것**(WARN-1) |
| **§6-3** CSS 여섯은 눈으로만 | **참이다.** jsdom 은 레이아웃을 계산하지 않는다. 다만 **값 계산은 내가 검증했다**(13항목 #8) |
| *(§6 이 말하지 않은 것)* | **둘 더 있다** — BE ⑪ 의 다시 읽기(WARN-2) · 완료 보고 뒤 다시 읽기(WARN-3). **둘 다 뮤테이션 초록** |

### ⚠ 이 판 **밖** 흔들림 — **새 자리 하나를 또 봤다**(코디의 flaky 대장 몫)

```
FAIL src/features/calendar/CalendarPage.test.tsx
  > 캘린더 골격 > 뒤집힌 업무의 띠가 서버가 준 구간대로 선다 — start_date(3/6)부터가 아니다
  AssertionError: expected false to be true   (CalendarPage.test.tsx:129)
```

- **4회 중 1회.** **FE-5 가 만진 파일과 닿지 않는다** — `CalendarPage.test.tsx` **mtime 09-21 19:33**
  (FE-5 세션보다 19시간 전 · 루프2 가 한 줄도 안 건드렸다).
- **원인이 앞 판 FAIL 과 «같은 부류»다**: `:125` 가 `await waitFor(() => expect(getCalendar).toHaveBeenCalled())`
  로 **API 호출만** 기다리고, `:127-129` 가 **그 promise 가 그려 낸 DOM 을 동기로 읽는다.**
  부하가 걸리면 띠가 아직 안 붙은 프레임을 잡는다. **`covered` 계산 전체를 `waitFor` 안에 넣으면 닫힌다.**
- 검수·FE-4·FE-5 가 세어 둔 자리(`task checklist`×2 · `task checklist span/null` ·
  `adjustment and resubmission` · `product surfaces` · `MeetingMaterials` · `ActionCenter` ·
  `CreateWork` 멱등 키)에 **없던 자리**다.
- 지시서가 적어 둔 기존 흔들림 넷(`task checklist`(2) · `task checklist span/null` ·
  `adjustment and resubmission` · `product surfaces`)은 **내 4회에서 한 번도 안 났다.**

---

## 눈으로만 확인되는 것 — 사용자 2차 E2E 가 볼 자리

**워커 §6-3 의 여섯에 내가 둘을 더한다.** jsdom 은 CSS 를 적용도 계산도 안 한다.

| # | 무엇 | 내가 코드로 확인한 데까지 |
|---|---|---|
| 1 | **L-37** 제목·소제목이 **읽히는가** | 선언은 있다 — `projects.css:136`·`:145` 둘 다 `ink-strong` |
| 2 | **L-38** 값의 좌측 정렬선이 **하나로 보이는가** | **값 계산은 맞다** — 배지·트리거·관계 줄의 좌 padding 이 **전부 `space-200`** 이고 `:162` 가 그만큼 음수 마진. 실제 x 는 레이아웃이 낸다 |
| 3 | **L-39** 행 높이 28px 이 **넉넉한가** | `min-height:28px` + `align-items:center` 로 통일됐다. 배지 22 · 트리거 26 을 담는다 |
| 4 | **L-40** 두 자리가 hover 없이 **눈에 띄는가** | **같은 부품인 것**은 뮤테이션으로 붙들린다. 테두리(`--scax-color-line`)·배경(`surface`)의 대비는 눈이다. 읽을 수 없는 선행의 **점선** 대비도 눈이다 |
| 5 | 생성 모달의 **날짜 두 칸이 나란히 서는가** | `grid-template-columns:1fr 1fr` · 모달 `size="md"` |
| 6 | 좌 레일 머리 한 줄이 **32px 안에서 안 넘치는가** | 셀렉터 `max-width:60%`. 긴 이름의 말줄임 자리는 눈이다 |
| **7** | **FAIL-1 의 실물** — 요청 업무의 완료 보고를 **서버가 거절하는** 장면 | **테스트로 이미 잡았다**(probe). E2E 는 「고친 뒤에 문구가 뜨는가」를 본다 |
| **8** | **관문 「아」의 실물** — 전이 중 트리거가 **회색으로 잠기는가** | 구현은 있고(WARN-1) **테스트로도 잡힌다.** 눈은 「잠긴 것이 보이는가」만 본다 |

---

## 기존 부채 (이번 판정 제외)

- `CalendarPage.test.tsx:125-129` 의 비동기 읽기(위 § 참조) — **루프2 가 안 건드린 파일**이다.
- 워커 §7 이 올린 `CreateWork.test.tsx` 의 멱등 키 흔들림 — 내 4회에서는 **안 났다**.
- SPEC 미결 **OQ-604**(항목 안 오는 갈래의 문구) · **OQ-607**(`external_key` 칸) —
  워커의 §4 잠정 정정(「이 프로젝트에 참여한 사람에게 보입니다」)은 **D-29 이후 참인 문장**이고
  `labels.ts` 한 줄이다. **판정에 넣지 않는다.**

## 확인한 것 (PASS 근거) — rules.md 체크리스트 전수

- **envelope**: 권한 판정은 **세션 역량 둘 + `access` + `may_manage`** 뿐이다.
  `kind`·`status` 로 권한을 추론하는 코드 **0건**.
- **호출 자리**: `grep -rn "fetch(" src/features/project/` → **0건**. 새 API 래퍼 0개.
- **재사용**: `Modal`·`DateField`·`Button`·`Badge`·`Select`·`Empty`·`Skeleton`·`StatusNote` ·
  `WorkModals` 의 `allowedTaskTransitions`·`BlockReasonPrompt`·`CompletionReportModal` ·
  `workRows` 의 `isRequestTask` — **전부 가져다 썼고 그 파일들은 diff 0줄**이다.
- **카피·스타일**: 한국어 문자열은 `labels.ts` 의 `projectScreen` 에 모여 있다(예외 1건 — WARN-6).
  `projects.css` 에 **hex 리터럴 0건**.
- **테스트**: `ProjectPage.test.tsx` **50건** 옆자리에 있다. 뮤테이션 16건 중 13건이 빨강 —
  **빈 단언·목만 검사하는 테스트는 없다**(자기참조 1건은 WARN-4).
- **allowed_paths**: 이탈 **0건**. 아홉 파일 전부 WORK-005 FE-5 §Code Surface 안이다.
