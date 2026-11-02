# 리뷰 리포트 — strong-hajin-projects / frontend (FE-1~FE-3) · 2026-09-22

## 판정: **FAIL (1) · WARN (7)**

**한 줄.** 이 판의 핵심(**사라지는 의존선 없음** · **깊이 제한 없는 재귀 간트** · **진행률 넷** ·
**BE 응답을 바르게 읽는 것** · **공유 자산 격리**)은 **코드로 확인했고 전부 참이다** —
시안의 `if (!a || !b) return` 은 옮겨지지 않았고 `anchorIndex()` 가 그 자리를 닫았다.
FAIL 은 **딱 하나**이고 화면의 논리가 아니라 **레일 등록 시점**이다: 프로젝트가 0개인 사람에게
「네 칸이 각각 비는」 순간이 실제로 생기고, 그 때문에 **이번 판이 새로 쓴 테스트가 흔들린다**
(격리 11회 중 2회 실패 — 내가 직접 잼).

---

## 검수 범위

- 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`, 브랜치 `kknaksss/strong-hajin-projects`
- `frontend/` **수정 8 · 신규 8** (`git diff --stat -- frontend/` = 749+/361-, untracked 8개)
- **`backend/` 는 이번 검수 범위 밖**(다른 워커 몫) — 다만 §2-10 의 「FE 가 backend 를 안 건드렸나」는 확인했다
- 실행한 것: `make frontend-test` **2회**, `npx vitest run src/features/project/ProjectPage.test.tsx` **11회**,
  `npx vitest run src/features/action/ActionCenter.test.tsx` 3회, `cd frontend && npx tsc --noEmit`,
  `git diff/status`, grep 전수(공유 자산 · `fetch` · `may_manage` · `.scax-inbox-card` · `.screens-b-lead`)
- **개발 서버는 띄우지 않았다.** 코드도 한 줄 안 고쳤다 — 산출물은 이 파일 하나다

---

## 위반 (FAIL)

### [FAIL-1] 프로젝트가 0개인 사람에게 **3레일이 먼저 서고 나서** 빈 상태가 덮는다 — D-22 위반 + 새 테스트가 흔들린다

- **무엇이** — `ProjectPage.tsx:219` 의 `noProjects = projects !== null && projects.length === 0` 는
  **첫 렌더에서 반드시 거짓**이다(`projects` 초기값이 `null`). 그래서 `:226-272` 의 등록 effect 가
  **마운트 시점에 좌·우 레일을 셸에 꽂는다** — 좌 레일은 `Skeleton`(`ProjectRail.tsx:47`),
  우 레일은 「업무를 선택하세요」 `Empty`(`ProjectTaskPanel.tsx:52`). `listProjects()` 가 `[]` 로
  돌아온 **뒤에야** `onRegisterRails({})` 로 지워진다.
- **파일:줄** — `frontend/src/features/project/ProjectPage.tsx:219` · `:226-231`
- **어느 계약과 어긋나나** — SPEC-005 §2.8 / §6 인수조건
  「읽을 수 있는 프로젝트가 0개인 사람에게 **「담당 프로젝트가 없습니다」 한 문장**이 뜬다 —
  **네 칸이 각각 비지 않는다**」 (D-22). 지금은 **네 칸이 각각 비는 프레임이 실재한다** —
  사용자가 「고장인가」를 묻게 되는 바로 그 자리다.
- **증거 (실측)** — 이번 판이 새로 쓴 검사
  `ProjectPage.test.tsx:433` 「읽을 수 있는 프로젝트가 0개면 화면 전체를 한 문장이 덮는다」가
  **`rail-left` 가 남아 있어** 실패한다. 실패 DOM 에 `scax-gutter-list__header--sub` + `scax-skeleton`
  이 그대로 찍힌다(= 로딩 단계 등록물). **격리 11회 중 2회 실패**, 전체 스위트 2회 중 1회 실패.
  FE 리포트 §4 의 「회차 2(최종) 974 passed · 0 failed」는 **한 번 초록이었을 뿐**이고 안정이 아니다.
- **수정안 한 줄** — 등록 effect 를 `if (!onRegisterRails) return; if (projects === null || noProjects) { onRegisterRails({}); return; }`
  로 바꿔 **프로젝트 목록을 알기 전에는 레일을 세우지 않는다** (= 빈 상태 판정을 첫 렌더로 끌어온다).

---

## 경미 (WARN)

### [WARN-1] 빈 상태 섹션의 `aria-label` 이 「프로젝트 관리」다
- `ProjectPage.tsx:289` — `aria-label={projectScreen.manage}`. 그 화면은 **관리 모달이 아니라
  「담당 프로젝트가 없습니다」 한 문장**이다. 보조기술에 잘못된 이름이 나간다.
- 근거: SPEC-005 §2.8. **수정안**: `projectScreen.noProjectsTitle` 로 바꾼다.

### [WARN-2] **접힌 가지 «안쪽»** 의 선은 선이 아니라 **셈**으로 난다 — 인수조건 문구와 글자 그대로는 어긋난다
- `projectModel.ts:298-310`(`internal`) · `ProjectGantt.tsx:252`(`!link.internal` 로 걸러 안 그린다) ·
  `ProjectGantt.tsx:215-219`(`__folded` 배지로 건수만).
- SPEC §6 「가지를 접으면 … **접힌 상태에서 선의 개수가 줄지 않는다**」는 **선의 개수**를 말한다.
  양 끝이 같은 행으로 접힌 선은 `.scax-pj-gantt__link` 가 **줄어든다**.
- **다만 「조용히 사라지는 선」은 아니다** — 건수 배지 + `title` 이 그 사실을 말하고,
  FE 리포트 §7-3 이 **스스로 「내가 정한 자리」로 올려 두었다**(자기 화살표는 뜻이 없다).
- **판단 요청**: 계약 문구를 「선 + 셈의 합이 줄지 않는다」로 정정할지, 자기-루프 선을 그릴지.
  **근거 불충분이라 FAIL 로 세지 않았다.**

### [WARN-3] 모수가 0 일 때 전체 진행률이 **「—」** 다 (0% 가 아니라)
- `projectModel.ts:159`(`percent: counted.length === 0 ? null : …`) · `ProjectSummaryStrip.tsx:39`.
- D-04 는 「완료 ÷ 전체」만 정했고 **분모 0 을 정한 적이 없다.** FE 가 D-02 의 결을 끌어다 썼고
  자기 리포트 §7-1 에 적어 두었다. **되돌리려면 한 줄**이다 — 코디 판단 자리.

### [WARN-4] 담당 없음을 **좌 레일은 빈칸**으로, **우 레일은 「—」** 로 낸다
- 좌 레일 `projectModel.ts:186`(`meta: []`) ↔ 우 레일 `ProjectTaskPanel.tsx:93-95`(`"—"`).
- 「미정」을 지어낸 것은 **아니므로 I-1 위반은 아니다.** 다만 같은 사실을 두 칸이 다르게 말한다.
  SPEC §2.6 은 우 레일 메타의 빈 칸 표기를 정하지 않았다 — **표기 통일 권고**에 그친다.

### [WARN-5] 하위가 **전부 기간 없는** 업무면 twisty 가 서지만 눌러도 아무 것도 안 움직인다
- `projectModel.ts:224-232` — `hasChildren` 은 **트리의 자식 수**(기간 유무 무관)로 정해지는데,
  행으로 서는 것은 `hasSpan` 인 것뿐이다. 접어도 사라질 행이 없다.
- SPEC §2.4 「twisty 는 **자식이 있는** 모든 깊이에 선다」는 지킨다 — **죽은 손잡이**가 생길 뿐이다.

### [WARN-6] 「상위이면서 하위」인 바의 높이가 **18px** 이다 (14px 이 아니라)
- `projects.css:104`(`--parent{height:14px}`) 다음에 `:106`(`--child{height:18px}`) 이 와서
  **둘 다 붙은 중간 깊이 바는 `--child` 가 이긴다.**
- 시안도 그 교차를 정의한 적이 없어 **규칙 출처가 없다** — 기록만 남긴다.

### [WARN-7] 강조된 의존선의 **화살촉 색이 안 바뀐다**
- `ProjectGantt.tsx:266-271` 의 `<marker>` 가 `fill="currentColor"` 인데, SVG marker 의 내용은
  **참조하는 `<path>` 가 아니라 `<marker>` 자신의 문맥**에서 상속한다. 그래서
  `projects.css:75` 의 `.scax-pj-gantt__link--on{color:accent}` 가 화살촉에 닿지 않는다 —
  **선(stroke)만 accent 로 굵어지고 촉은 `ink-assistive` 로 남는다.**
- SPEC §2.5 「선택된 업무에 닿는 선만 `accent` 1.6px」의 **선 부분은 참**이다. 시각 흠.
  **수정안**: `--on` 전용 marker 를 하나 더 두거나 `marker`에 `fill="context-stroke"` 를 쓴다.

---

## §2 — 브리프가 못 박은 10개 항목, 하나씩

| # | 항목 | 결과 | 근거 |
|---|---|---|---|
| **1** | **사라지는 의존선이 없는가** | **PASS** | 시안의 `if (!a || !b) return` 이 **코드에 없다.** `projectModel.ts:265-281 anchorIndex()` 가 **자리 없는 업무를 가장 가까운 «서 있는» 조상으로** 접고(`resolve()`), `depLinks()`(`:291-311`)가 `fromRowId/toRowId` 로 그 닻을 싣는다. 접힌 부모 바에 실제로 붙는 것을 **값으로** 검사한다 — `projectModel.test.ts:86` `expect(foldedLinks.find(l=>l.fromTaskId==="d2")?.fromRowId).toBe("d0")`. 화면 쪽은 `ProjectPage.test.tsx:282-296` 이 **4층 트리 + 손자가 조부의 형제를 선행으로 가진 모양**에서 접기 전후 `.scax-pj-gantt__link` 개수가 **1 → 1** 임을 본다. **테스트가 정확히 그것을 겨눈다.** (가지 «안쪽» 선은 WARN-2) |
| **2** | 간트가 깊이 제한 없는 재귀인가 | **PASS** | `buildTaskTree()`(`projectModel.ts:85-101`) 재귀 · `ganttRows()`(`:236-260`) 재귀. **8층 사슬에서 행 8개 · depth `[0..7]`** — `projectModel.test.ts:48-52`. 화면에서도 **증손자 t-4 가 `data-depth="3"`** 으로 선다(`ProjectPage.test.tsx:268-272`). **2단계에서 끊기는 자리가 0곳**이다 |
| **3** | 들여쓰기 예산 · 나머지 기하 | **PASS** | `GANTT = {day:34,row:40,label:200,indent:12,maxIndentDepth:5}`(`projectModel.ts:20-29`). `indentFor()` 가 `[0,12,24,36,48,60,60,60]`(`test:55`) — **멈추는 것은 들여쓰기이고 행이 아니다**(같은 파일 8층 검사). 바 22/14/18 = `projects.css:89,104,106`. 레일 380/342 = `scax.css:119-120`→`product.css:79-80`, **`AppShell.tsx` 무변경**이라 그대로 |
| **4** | 진행률 넷 | **PASS** | ① 체크리스트 기반 `taskPercent()`(`projectModel.ts:69-75`) ② **`total==0` → `null`** 이고 JSX 가 `percent !== null` 일 때만 fill·% 를 낸다(`ProjectGantt.tsx:223,225`) — **0% 가 없다** ③ 상위 바는 `!hasChildren` 조건으로 % 텍스트 없음(`:225`) + CSS 이중 잠금(`projects.css:105`) ④ `cancelled` → `null` + `--cancelled` 배경 + `__row--cancelled` 취소선(`projects.css:99-100`). `done` 은 체크리스트 없어도 100%. 다섯 규칙 전부 `ProjectPage.test.tsx:298-320` 이 **바 단위로** 검사 |
| **5** | **BE 응답을 바르게 읽는가** | **PASS** | · `assignee: null` → 좌 레일은 **칸 자체를 안 만든다**(`projectModel.ts:186` `meta: []`, 검사 `test:239` `meta-sep` 0개), **「미정」 문자열이 저장소 전체에 0건**(grep) · 간트가 **`span_*` 만** 읽는다(`ganttAxis`·`barGeometry` `:212-233`), 원값 `start_date/due_date` 는 **카드의 말**(`taskWhen()`)에만 닿는다 — **클라이언트 정규화 0건** · `overdue_days` 는 **값이 온 업무만** 센다(`:157`, 검사 `test:150-157` 이 「완료+기한 지남+`null`」을 안 세는 것을 본다) · `blocked` 는 `BAR_STATUS`(`:33-39`)·`taskStateLabel/Tone` 으로 **배지 「막힘/danger」 + 바 `--blocked`** 까지 그린다(`test:322-334`). 떨어뜨리는 자리 0곳 |
| **6** | 요약 스트립 모수 | **PASS** | `summarize()` 가 `counted = tasks.filter(state !== "cancelled")` **하나**로 `total` 과 `percent` 분모를 함께 만든다(`:152-160`) — 한쪽만 빼는 자리가 없다. **「취소 2 · 완료 8 → 8/8/100%」** 를 `projectModel.test.ts:141-148` 이 직접 잰다. 좌 레일 배지(9)와 「전체 업무」(8)가 **다른 것을 센다**는 것도 화면 검사가 잡는다(`test:253-255`) |
| **7** | 공유 자산 | **PASS** | · `.scax-inbox-card` 4규칙 전부 **`[role="button"]` 안**(`projects.css:35-38`) — 수신함 `InboxRail.tsx:59`·캘린더 `ScheduleCard.tsx:44` 에 **`role` 속성이 0건**(grep)이라 안 걸린다 ✔ · **`git diff --stat -- frontend/src/ds/` 가 비어 있다** → `Empty` 29곳·`ProgressBar`·`Select` 무사 · `AppShell.tsx` 무변경 → **`titleEnd` 슬롯 안 생김**(5화면 무사, D-25) · `screens-b.css` 무변경 → `.screens-b-lead` 규칙 그대로, **`OrgPage.test.tsx:249` 통과**(전체 초록 회차에서 확인) · `components.css` 무변경 → `:692-693` 반응형 줄 그대로. **`--sub` modifier 소비처는 `ProjectRail.tsx:66` 한 곳뿐** |
| **8** | 후행은 클라이언트 역산인가 | **PASS** | `successorIndex()`(`projectModel.ts:127-137`)가 `preceding_task_ids` 를 뒤집는다. `api.ts` **무변경**(새 함수 0개), 프로젝트 화면이 부르는 것은 `listProjects·getProject·participation-history·createProject·assignToProject·releaseFromProject·getMemberDirectory·getTask` 여덟뿐이고 **후행 경로가 없다.** 검사가 「후행 목록이 우 레일에 난다」까지 본다(`test:344-348`) |
| **9** | `api.ts` 밖 fetch · 모달이 이동인가 | **PASS** | `grep -rn "fetch(" frontend/src` 에서 `lib/api.ts`·테스트 밖 **0건**. 모달은 `git show HEAD:…/ProjectPage.tsx:206-306` 과 대조해 **필드 다섯(이름·붙일 구성원·참여/담당·종료 사유)이 늘지도 줄지도 않았다** — `ds/Select` 자리만 시안 어휘 `AutoComplete` 로 갈았고(`components.css:308-313` 에 CSS 가 **이미 있다**), `ds/Select` 본체는 안 고쳤다. `may_manage` 를 읽는 자리는 **`ProjectPage.tsx:278` 한 곳뿐**(grep 전수) |
| **10** | 범위 | **PASS** | FE 가 만든 `backend/` 파일 0건(현재 backend 변경 17건은 `be-impl-report.md §8` 의 목록과 **정확히 일치** = BE 워커 몫) · **커밋 0건**(`git log` 머리가 `e46ce39` 그대로, 브랜치가 앞서 있지 않다) · **개발 서버 0건**(5173/4173 LISTEN 없음; 8000 은 이 판과 무관한 Docker) |

---

## 테스트 — **내가 잰 수치**

| 명령 | 회차 | 결과 |
|---|---|---|
| `make frontend-test` | 1 | **Test Files 2 failed / 68 passed (70)** · **Tests 2 failed / 972 passed (974)** |
| `make frontend-test` | 2 | **70 passed (70)** · **974 passed (974)** · 11.45s |
| `npx vitest run src/features/project/ProjectPage.test.tsx` | **11회** | **9 pass · 2 fail** — 실패는 **매번 같은 한 건** |
| `npx vitest run src/features/action/ActionCenter.test.tsx` | 3회 | **14 passed · 3/3** |
| `cd frontend && npx tsc --noEmit` | 1 | **exit 0 · 에러 0** |

### 실패 둘을 **귀속**해 가른다

| 실패 | 파일 | 이번 판 것인가 | 근거 |
|---|---|---|---|
| 「읽을 수 있는 프로젝트가 0개면 …」 | **`features/project/ProjectPage.test.tsx:437`** | **이번 판 것이다** | 이 판이 **새로 쓴** 검사이고, 이 판이 새로 쓴 등록 effect 가 원인이다 → **FAIL-1**. 격리 실행에서도 **2/11 로 재현**된다 |
| 「confirms an unchanged AX proposal …」 | `features/action/ActionCenter.test.tsx:187` | **아니다** | `git diff --stat -- frontend/src/features/action/ frontend/src/lib/api.ts` 가 **비어 있다**(이 판이 한 글자도 안 건드렸다). **단독 3회 전부 통과** → 병렬 부하 흔들림(기존 부채) |

> FE 리포트 §4 의 「최종 974 passed · 0 failed」는 **거짓이 아니라 한 회차의 사실**이다.
> 다만 **그 회차만으로 초록을 선언하면 FAIL-1 이 숨는다** — 실제로 2회 중 1회는 빨갛다.

---

## 시안 대비 눈에 띄는 차이

FE 리포트 §6 의 **DS-gaps 일곱(P-1~P-7)** 을 코드로 대조했다 — **일곱 다 실재하고 기록대로다.**
그 밖에 내가 새로 센 것:

1. **`.scax-pj-gantt__bar--progress` 규칙이 없다** — 기본 `.scax-pj-gantt__bar` 가 `accent-20`,
   fill 이 `accent` 라 **`in_progress` 가 시안과 같은 값으로 선다.** 규칙을 안 쓴 것이지 빠뜨린 것이 아니다
   (`projects.css:89-90`). **차이 아님**으로 닫는다.
2. **legend 의 「2026년 9월」이 데이터의 축 범위로 바뀌었다** — `ganttRange(from,to)`(`labels.ts`) +
   `ProjectGantt.tsx:66`. 시안의 고정 문구는 목데이터용이었다(DEC-003 §J 선례). **계약대로다.**
3. **`__legend--warn` 이 `danger` 색으로 머리줄에 붙는다** — 시안에 없는 자리(P-4 의 부산물).
   기간 없는 업무에 선행이 하나라도 걸리면 **항상** 빨간 문구가 선다. 계약(「왜 없는지가 드러나야 한다」)은
   지키지만 **상시 경고로 읽힐 수 있다** — 눈으로 볼 때 확인할 자리다(E2E 사용자 몫).
4. **사이드바 순서 어긋남 ⑤-8**(시안 업무 → 프로젝트 → 캘린더 / 우리 업무 → 캘린더 → 프로젝트) —
   **D-26 대로 안 건드렸다.** 기록만.

---

## 기존 부채 (이번 판정 제외)

- `features/action/ActionCenter.test.tsx` 의 병렬 부하 흔들림 (위 표 참조). 이 판 밖이다.
- `components.css:692-693` 에 죽은 `.project-layout` 선택자가 남아 있다 —
  `.dashboard-columns`·`.report-grid` 와 같은 규칙이라 **일부러 안 지운 것**이고 FE 리포트가 그 이유를 적었다.
  **동의한다.**

---

## 재발주 시 확인할 것 — **한 줄짜리 하나**

- [ ] `ProjectPage.tsx:226` 등록 effect 가 **`projects === null` 일 때도 레일을 안 세운다.**
- [ ] `ProjectPage.test.tsx` 「프로젝트 0개」 검사를 **격리로 10회 연속** 돌려 초록인지 본다
      (지금은 2/11 로 빨갛다). 1회 초록은 통과 근거가 아니다.
- [ ] WARN-1(`aria-label`)은 같은 파일 한 줄이라 함께 고치는 것이 싸다.
- [ ] WARN-2·WARN-3 은 **코드가 아니라 계약 판단** — 코디네이터가 정한다.
