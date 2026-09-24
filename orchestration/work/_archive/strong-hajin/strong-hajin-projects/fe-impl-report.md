# WORK-005 Phase FE-1 · FE-2 · FE-3 결과 보고

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`, 브랜치
`kknaksss/strong-hajin-projects`. **커밋·push 하지 않았다 — 변경만 남아 있다.**
**`backend/` 는 한 줄도 열지 않았다** — 서버가 실제로 내는 값은 `be-impl-report.md` §6 을 읽었다.

---

## 0. 한 줄

시안대로 **다시 그렸다**. 본문 한 칸의 2컬럼 관리 화면이 **3레일 + 요약 스트립 + 간트 + 의존선 +
업무 상자**가 됐고, 관리 기능은 사라지지 않고 **모달로 옮겨갔다**. 이 판의 가장 어려운 자리
(**접힌 가지에 걸린 의존선**)는 시안의 `if (!a || !b) return` 을 버리고 **닻(anchor) 계산**으로 바꿔
닫았다 — **선이 하나도 사라지지 않는다.**

---

## 1. 착수 전 확인 (FE-1 작업 0) — **한 줄로**

시안 `handoff/projects/css/projects.css` 가 참조하는 `--scax-*` 토큰 중 **저장소에 없는 것은 0개**이고
값도 같다 — `styles/scax.css:6-129` · `product.css:79-80` 을 이름별로 대조했다(조사
`research-fe-structure.md` §2-1 의 전수표와 일치). **고칠 것이 없었고, 값의 정본은 저장소 파일이다.**

⚠ **`node_modules` 가 없는 워크트리였다.** `npm ci` 로 설치한 뒤에야 테스트가 돌았다 —
그래서 **「내 변경 0줄 상태의 프론트 기준선」을 못 찍었다.** 대신 §4 에 「내가 만진 테스트 파일」을
전수로 적었다: 그 셋 밖에서 실패가 나면 내 탓이 아니다(그리고 최종 회차에 그런 실패가 0건이다).

---

## 2. 바꾼/만든 파일과 **각각이 닫는 인수조건**

### 신규 8

| 파일 | 무엇 | 닫는 인수조건 |
|---|---|---|
| **`frontend/src/features/project/projectModel.ts`** (순수) | 재귀 트리 · **닻 계산** · 의존선 · 후행 역산 · 요약 세기 · 축/막대 기하 · 바의 % 규칙. 선례 `workRows.ts`·`calendarModel.ts` | **간트와 트리 6줄** · **의존선 4줄** · **진행률 D-01~D-04** · **핵심 넷 중 3줄** |
| `frontend/src/features/project/projectModel.test.ts` | 위의 순수 규칙 12건 | 위와 같음 (깊이 8층 · 들여쓰기 5단 정지 · 접힘 닻 · 자리 못 찾은 선 · 모수 하나) |
| `frontend/src/features/project/ProjectRail.tsx` | 좌 레일 — 헤더(아이콘 + 「업무」 + 건수 배지) + 프로젝트 `Select`(알약 트리거) + **기존 `scax-inbox-card` 재사용** + 선택 상태 | **좌 레일 3줄**(분류 없음 · 담당 · 클릭 = 선택) · **상태 어휘 3줄** |
| `frontend/src/features/project/ProjectSummaryStrip.tsx` | 요약 스트립 5칸 | **진행률 5줄**(모수 하나 · 지연은 서버 값 · 평균 아님) |
| `frontend/src/features/project/ProjectGantt.tsx` | 간트 축·격자·행·twisty·바 + **의존선 SVG 오버레이** | **간트와 트리 6줄** · **의존선 4줄** · **핵심 넷 중 3줄** |
| `frontend/src/features/project/ProjectTaskPanel.tsx` | 우 레일 — 메타 · 관계(선행/**후행**) · 체크리스트(읽기) · 하위 업무 · 「업무 열기」 | **우 레일 4줄** · **의존선 1줄**(후행 목록) · **진행률 1줄**(미터 「—」) |
| `frontend/src/features/project/ProjectManageModal.tsx` | 관리 모달 — 참여자 붙이기/떼기 · 참여 이력 · 새 프로젝트 | **관리 모달과 빈 상태 6줄** |
| **`frontend/src/styles/projects.css`** | 화면 전용 CSS 한 장 (`.scax-pj-*`) | 위 전부의 생김새 |

### 수정 8

| 파일 | 무엇 | 닫는 인수조건 |
|---|---|---|
| `frontend/src/lib/viewModels.ts` | `ProjectDetail.tasks` 를 **이름 있는 `ProjectTaskRow`** 로 빼고 넓혔다 — `state: string` → **`TaskState`**, `preceding_task_ids` · `assignee` · `checklist_progress` · `span_from`/`span_to` · `overdue_days` 신설. `ProjectPage.tsx:321` 의 억지 캐스팅이 사라졌다 | **I-1~I-6 의 재료** (어긋남 ⑤-6) |
| `frontend/src/lib/labels.ts` | **`projectScreen` 한 블록**(약 70줄). 상태의 «말» 은 여기 없다 — `taskStateLabel`·`taskStateTone` 을 그대로 쓴다 | **상태 어휘 3줄** (라벨·톤이 두 화면에서 같다) |
| `frontend/src/features/project/ProjectPage.tsx` | **재작성.** 3레일 등록 · 선택 축 하나 · 관리 모달 손잡이 · 빈 상태 | **F 좌·우 레일 8줄** · **G 6줄** · 선택 축 1줄 |
| `frontend/src/features/project/ProjectPage.test.tsx` | 7건 → **15건** (§4) | 위 전부의 검사 |
| `frontend/src/App.tsx` | `ProjectPage` 에 `onRegisterRails`·`onRegisterHeaderActions`·`onOpenTask` 를 넘긴다 + 프로젝트를 **`scax-page-scroll--fixed`** 편에 세운다 + **`openTaskInWork` 를 `useCallback` 으로 고정** (§5 ①) | **3레일 1줄** · **D-21 손잡이** |
| `frontend/src/styles/index.css` | `@import "./projects.css"` 한 줄 (선례 `calendar.css`) | — |
| `frontend/src/styles/screens-a.css` | 죽은 `.project-*` 11종 제거 (소비처 0) + 그 자리에 왜 사라졌는지 | — |
| `frontend/src/shell/AppShell.test.tsx` | 스크롤 주인 표에 **「프로젝트」 한 칸** 추가 (§5 ①) | — |

**`src/ds/` 를 한 줄도 안 고쳤다** — `git diff --stat -- frontend/src/ds/` 가 **비어 있다**.
`ds/Empty` 글리프도 `ds/ProgressBar` API 도 `ds/Select` 도 그대로다.

---

## 3. 이 판의 핵심 — **사라지는 선이 하나도 없다** (D-17)

시안 `DepLines` 는 양 끝 좌표를 못 찾으면 `if (!a || !b) return` 으로 **말없이 빠져나간다**
(`projects.v1.jsx:85-106`). 목데이터가 1단계뿐이라 **생길 수 없던 상황**이고, 우리 자료에는 깊이 제한이
없어서 **가지를 접는 순간 그 `return` 이 돈다.** 그대로 옮기면 화면이 「선행 없음」이라고 거짓말한다.

**대신 한 자리에서 닻을 계산한다** — `projectModel.anchorIndex()`:

| 경우 | 시안 | 우리 |
|---|---|---|
| 양 끝이 다 보인다 | 그린다 | 그린다 |
| 한쪽이 **접힌 가지 안** | **말없이 버린다** | **가장 가까운 «서 있는» 조상**(= 접힌 부모 바)에 끌어붙인다 |
| 양 끝이 **같은 접힌 가지 안** | **말없이 버린다** | 그 행이 **건수로 들고 있는다** (`__folded` 배지 + title) |
| 한쪽이 **기간이 없거나 볼 수 없는 업무** | **말없이 버린다** | 머리줄이 **건수로 말한다** (`__legend--warn`) |

검사로 잠갔다 — `ProjectPage.test.tsx` 「가지를 접어도 선이 사라지지 않는다」는
**접기 전후 `.scax-pj-gantt__link` 의 개수가 같다**는 것을 본다(손자가 조부의 형제를 선행으로 가진
4층 트리에서). `projectModel.test.ts` 가 닻의 **값**(접힌 부모 id)까지 본다.

**깊이도 자르지 않았다**: 트리는 재귀이고 8층 사슬에서 행이 여덟 선다. 들여쓰기만 **깊이당 12px ·
5단에서 멈춘다** — `indentFor()` 가 `[0,12,24,36,48,60,60,60]` 을 낸다. **멈추는 것은 들여쓰기이고
행이 아니다.**

**기간 없는 상위의 자식은 사라지지 않는다.** 간트에 서지 않는 업무(정규화 결과 없음)의 자식은
**그 자리로 올라와** 깊이를 유지한다 — 그러지 않으면 손자의 좌표가 없어지고 다시 선이 사라진다.

---

## 4. 테스트 수치 · tsc

| 회차 | 명령 | 파일 | 테스트 | 판정 |
|---|---|---|---|---|
| **1** | `make frontend-test` (Node 20) | 69 passed · **1 failed** | 973 passed · **1 failed** | 실패 1건 — 아래 |
| **2 (최종)** | `make frontend-test` | **70 passed** | **974 passed · 0 failed** | **전부 통과** |
| — | `npx vitest run src/features/project` | 2 | **27 passed** (ProjectPage 15 · projectModel 12) | — |
| — | `npx vitest run src/shell` | 4 | **14 passed** (`AppShell` 포함) | — |
| — | `cd frontend && npx tsc --noEmit` | — | — | **0 에러** (출력 없음) |

**회차 1 의 실패 1건 — 내 것이 아니다.**
`src/features/meetings/MeetingMaterials.test.tsx::이미 볼 수 있는 사람은 고르는 자리에 안 낸다`
(회의 공유 모달에서 「오세림」을 못 찾는다). **이 판이 건드린 코드와 겹치는 자리가 0개**이고
(회의 화면 · `modal meeting-modal-share` · 구 `.modal*` 계열), **브리프가 범위 밖으로 못 박은
자료(material) 쪽**이다. 단독 실행 **15 passed**, 회차 2 에서 **통과** — 병렬 부하에서의 흔들림이다.
**고치지 않았다 — 범위 밖이다.**

⚠ **기준선(내 변경 0줄) 회차는 못 찍었다** — 워크트리에 `node_modules` 가 없어서(§1) 설치한 시점에는
이미 타입 한 파일을 고친 뒤였다. 대신 **내가 만진 테스트 파일 셋을 전수로 밝혀** 귀속을 가능하게 했다.

**내가 만진 테스트 파일은 셋뿐이다** — `features/project/ProjectPage.test.tsx`(수정) ·
`features/project/projectModel.test.ts`(신규) · `shell/AppShell.test.tsx`(**한 줄**, §5 ①).
그 밖의 테스트 파일은 **한 글자도 안 고쳤다.**

### `ProjectPage.test.tsx` — **삭제 0건 · 교체 6건 · 신규 8건** (M-2)

| 옛 검사 | 어디로 갔나 |
|---|---|
| #1 제목 중복 금지 | **살아 있다** — 여기에 「본문 첫 줄이 요약 스트립」과 「`.screens-b-lead` 가 없다」를 더했다 |
| #2 참여자 + 업무 계층 | **둘로 갈라졌다** — 참여자는 **모달 검사**로, 계층은 **간트 `data-depth` 검사**로 |
| #3 `may_manage` 로 관리 UI 감춤 | **머리 `actions` 의 손잡이 렌더 여부**로 |
| #4 「담당자에게만 보입니다」 | **그대로** (본문에 남는 값이다) |
| #5 붙이면 `assignToProject` 호출 | **모달 안에서** (`AutoComplete` 로 고른다) |
| #6 현재 참여자 / 이력 분리 + 사유 종료 | **모달 안에서** |
| #7 프로젝트 전환이 열린 입력을 닫는다 | **`Select` 전환**으로 — 모달까지 함께 닫히는 것을 더 본다 |

**신규 8**: 좌 레일 카드(분류 없음·담당 빈칸·취소도 남음) · 요약 스트립 다섯 수 ·
간트 4층 깊이 · **접힘 의존선** · 바의 % 다섯 규칙 · **`blocked` 배지·바** · 선택 축 + 후행 역산 +
**`getTask` 호출 1회** · 우 레일 미터 「—」 · 프로젝트 0개 빈 상태.

---

## 5. **공유 자산을 건드린 자리** — 셋뿐이고 전부 적는다

### ① `frontend/src/App.tsx` · `frontend/src/shell/AppShell.test.tsx` — **셸의 스크롤 주인 표**

프로젝트가 회의·캘린더와 같은 편(`scax-page-scroll--fixed`)에 섰다. 레일 두 칸과 본문이 칸을 채우고
`.scax-pj-view` 가 자기 안에서 스크롤하기 때문이다 — 바깥이 또 스크롤하면 주인이 둘이 된다.
`AppShell.test.tsx` 의 `fixed` 판정에 **「프로젝트」 한 칸**을 더했다. **다른 화면의 판정은 그대로다.**

> ⚠ **여기서 내가 버그를 하나 만들었다가 잡았다.** 처음에 `onOpenTask` 를 App 에서 **인라인 화살표**로
> 넘겼는데, 레일을 등록하는 화면이 그것을 의존성에 물고 있어서 **「등록 → 셸 상태 변경 → 렌더 →
> 다시 등록」 무한 루프**가 돌았다(`AppShell.test.tsx` 가 통째로 멎는 것으로 드러났다 — `App.tsx:98-102`
> 주석이 예고한 바로 그 함정이다). **App 에서 `useCallback` 으로 고정**하고, 화면 쪽에도
> **`latestOpenTask` ref** 를 둬서 다음 사람이 같은 실수를 해도 안 돌게 막았다(선례 `ds/Modal.tsx`
> 의 `useEscape`). 지금 `AppShell.test.tsx` 는 **365ms** 에 통과한다.

### ② `.scax-inbox-card` — **`[role="button"]` 으로 좁혔다**

시안은 `.scax-inbox-card--selected` 를 **무조건 규칙**으로 둔다. 그대로 쓰면 `role` 이 없는
수신함(`shell/InboxRail.tsx:59`)·캘린더(`features/calendar/ScheduleCard.tsx:43`) 카드에도 새 규칙이 얹힌다.
그래서 hover·focus·selected **네 규칙 전부**를 `.scax-inbox-card[role="button"]` 안으로 넣었다 —
**그 둘은 `role` 이 없어 한 규칙도 안 걸린다.** (확인: `InboxRail.test.tsx` · `CalendarRail.test.tsx` 통과)

### ③ `.scax-gutter-list__header--sub` — **modifier 를 새로 하나 추가**

우리 `.scax-gutter-list__header` 는 `height: 32px` **고정**이라(`components.css:106`) 시안의
`min-height:auto` 한 줄로는 안 풀린다. 이 화면은 제목 줄 아래 셀렉터가 한 줄 더 서야 해서
**`--sub` 에만** `height:auto; flex-direction:column` 을 줬다. **수신함·캘린더 레일은 `--sub` 를
안 쓰므로 그대로다.**

### 건드리지 않은 것 (확인)

- **`src/ds/` 전체** — `git diff --stat` 이 비어 있다. `Empty` 글리프 20px · `ProgressBar` API ·
  `Select` 본체 모두 그대로. 우 레일 미터와 요약 미터는 **화면 전용 클래스**(`.scax-pj-side__*` ·
  `.scax-pj-summary__*`)로 만들었다
- **`AppHeader` 에 슬롯을 더하지 않았다** — 시안 `projects.css:2` 의 `.scax-page-header__title-row`
  한 줄을 **버렸다**(D-25). 그것은 없는 슬롯을 전제한 셸 규칙이다
- **`.screens-b-lead`** — 이 화면에서 **놓기만** 했고 규칙은 안 건드렸다. 조직·관계탐색·보고가
  그대로 쓰고 `OrgPage.test.tsx:249` 도 그대로 통과한다
- **`components.css:692-693` 의 반응형 줄** — 죽은 `.project-layout` 선택자가 남았지만 **안 지웠다.**
  `.dashboard-columns`·`.report-grid` 와 **같은 규칙에 묶여** 있어서, 선택자 하나가 죽은 채 남는 비용이
  홈·보고를 흔드는 비용보다 싸다. (`screens-a.css` 의 같은 줄도 같은 이유로 그대로)
- **사이드바·내비 순서** (D-26) — 안 건드렸다. 어긋남 ⑤-8(시안은 업무 → 프로젝트 → 캘린더, 우리는
  업무 → 캘린더 → 프로젝트)은 **기록만** 한다
- **`api.ts` 밖 `fetch` 0건** · **새 API 함수 0건** — `getTask` 를 import 만 더했다
- **`backend/` · 문서 레포 · 시안 폴더** — 열지도 않았다

---

## 6. DS-gaps — **시안에 없거나 우리와 어긋난 자리 일곱**

저장소에 `DS-gaps.md` 파일이 **없어서**(코드 주석만 그 번호를 가리킨다) 여기에 적는다.

| # | 자리 | 시안 | 우리가 한 것 | 왜 |
|---|---|---|---|---|
| **P-1** | `AppHeader` 의 `titleEnd` 슬롯 | 있다 (`scax-ui.jsx:276-281`) | **안 만들었다.** `projects.css:2` 의 셸 규칙 한 줄을 버렸다 | 5개 화면이 공유하는 셸이다 (D-25) |
| **P-2** | `Empty` 글리프 크기 | 24px | **20px 그대로** | 소비처 29곳이 같이 움직인다 (D-24). **4px 차이가 남는다** |
| **P-3** | 간트 바의 `cancelled` | **색이 정의돼 있지 않다** (목데이터에 취소가 없었다) | `--cancelled` 를 **우리가 더했다** — 배경 `fill-weak` · fill 없음 · 제목 취소선 | 취소된 업무가 **간트에 그대로 선다** (D-23) |
| **P-4** | `DepLines` 의 접힘 처리 | **없다** — `if (!a || !b) return` | **닻 계산으로 대체**(§3) + 삼킨 선 배지 + 자리 못 찾은 선 건수 | 시안 그대로면 **선이 조용히 사라진다** (D-17) |
| **P-5** | 축의 기간·「오늘」 | `{days:30, today:17}` **하드코딩** + legend 「2026년 9월」 | **데이터에서 낸다.** 오늘은 `seoulToday()` 를 화면이 넘긴다 | 목데이터 편의값이다 |
| **P-6** | 상태 라벨 둘 | 「대기」(`not-started`) · 「지연」(`blocked`) | **「시작 전」 · 「막힘」** (`labels.ts` 의 `taskStateLabel`) | 같은 업무가 두 화면에서 다른 이름을 가지면 안 된다. **톤 5종은 한 칸도 안 틀린다** |
| **P-7** | 관리 모달 | **통째로 없다** | 시안 `work-modal.jsx` 의 **어휘만 빌렸다** — `Modal`(`scax-modal*`) · `Field`(`scax-field*`) · `TextField`(`scax-textfield*`) · `AutoComplete`(`scax-autocomplete*`, CSS 는 이미 저장소에 있다). **새 부품 0개 · 필드 늘거나 줄지 않음** | 옮기는 것이지 발명하는 것이 아니다 (M-1) |

---

## 7. 내가 «정한» 자리 — **판단이 필요하면 되돌린다**

1. **요약 스트립의 「전체 진행률」이 업무 0건일 때 「—」다** (0% 가 아니다).
   D-02 의 결(「셀 것이 없으면 말하지 않는다」)을 요약 칸에도 그대로 적용했다. 0% 로 두는 쪽이
   좋으면 `projectModel.summarize()` 의 `percent` 한 줄이다.
2. **상위 바도 fill 은 그린다 — % 텍스트만 안 낸다.** 시안 CSS 가 `--parent .bar-pct{display:none}`
   하나만 두고 fill 은 그대로 두는 것과 같은 뜻으로 읽었다.
3. **접힌 가지 «안쪽» 의 선(양 끝이 같은 행)은 선이 아니라 «셈»으로 낸다.** 자기 자신을 가리키는
   화살표는 뜻이 없어서다. **버리지 않았다** — 그 행의 `__folded` 배지가 건수를 들고 title 이 말한다.
4. **우 레일의 관계 목록은 프로젝트 응답의 `tasks[]` 로 만든다** (업무 상세의 `predecessors` 가 아니라).
   그래야 호출이 안 늘고, **읽을 수 없는 선행은 자리가 남고 건수에 든다**(「볼 수 없는 업무」).
5. **좌 레일 셀렉터에 「새 프로젝트로 추가」 같은 footerAction 을 안 달았다** — 만드는 것은
   관리 모달의 일이다.

---

## 8. 막힌 것 · 안 한 것

- **브라우저 E2E 는 안 돌렸다** — 브리프대로 **내일 사용자가 한다.** 개발 서버를 띄우지 않았고
  사용자 포트·프로세스를 건드리지 않았다.
- **첨부(material) 관련은 범위 밖**이라 손대지 않았다.
- **`make verify` 를 안 돌렸다** — WP 가 「FE-3 에서 한 번」이라 적지만 브리프 §3 이 최종 빌드를
  **코디가 돌린다**고 했고 「같은 검증을 중복 실행하지 마라」가 있어서 `make frontend-test` +
  `npx tsc --noEmit` 까지만 했다.
- **커밋·push·PR 0건.** 워크트리에 변경만 있다.
- **문서 레포·`docs/design/`·시안 폴더 수정 0건.**
