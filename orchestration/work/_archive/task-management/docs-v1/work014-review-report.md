---
type: review
work: WORK-014
title: "WORK-014 검수 — breadcrumb 링크 · 「←」 · 헤더 순서 세 화면 · 미리보기 CTA · 패널 크기 · 밀도 (+ 013 파일 이름 이관)"
reviewer: reviewer
date: 2026-09-08
scope: "미커밋 변경 22 파일(프론트만) + git mv 둘 + AppShell.test.tsx 신설"
worktree: /Users/kknaks/orca/workspaces/task_management/docs-v1 (kknaksss/docs-v1 · HEAD bfde960)
verdict: "FAIL 0 · WARN 2 · 문서 공백 2"
---

# WORK-014 검수 리포트

**FAIL 0 · WARN 2 · 문서 공백 2.**
`tauri.conf.json` 은 범위 밖이라 보지 않았다. 테스트는 돌리지 않았다(코디 실측 — tsc 0 · vitest 360).

## 0. 축별 판정 한 줄

| 축 | 판정 | 한 줄 |
|---|---|---|
| 2-1 breadcrumb · 「←」 | **PASS** | `trail: readonly Crumb[]` · 앞 칸은 `<Link>` · 마지막은 `href` 를 줘도 `<span>` · `DetailHeaderBar` 가 `AppShell.tsx` 안(새 파일 0) · `router.back(` **0건** · 업무 화면 diff **1 파일 +3/−9** |
| 2-2 헤더 순서 세 화면 | **PASS** | 세 화면 모두 `DetailHeaderBar` → `MeetingBadgeRow` → `<h1>` → 메타이고 **`compareDocumentPosition` 으로 DOM 순서를 단언**한다. 배지 줄이 좌 인라인 셀렉터 · 우 액션을 `items-center` 로 같은 높이에 둔다 · 메타에서 유형·프로젝트가 빠졌다 · 상세 드로어 수정 0 |
| 2-3 CTA · 패널 크기 · 밀도 | **PASS · WARN 1** | CTA 4행 한 표 · 가는 곳 넷 다 하나 · 패널 높이를 `MeetingsScreen` 이 고정하고 본문만 `overflow-y-auto` · `absolute` 0 · 폭 규칙 `MeetingListPanel` 한 자리(`wide: 1440px`) · 트리 컴포넌트 **하나**에 `density` prop. 네 폭 실측만 비었다 |
| 2-4 013 이관 | **PASS** | `git mv` 둘 — `ActionPayloadDrawer.tsx` 는 **import 한 줄**만 바뀌었고 `TaskPayloadDrawer.tsx` 는 **0줄**이다. 옛 이름 잔재 0 |
| 2-5 금지 · 범위 | **PASS** | `fetch(` 0 · `Sheet`/`Dialog` 소유자 각각 하나(`DrawerFrame` · `ConfirmModal`) · `localStorage` 0 · `retry:true` 0 · 012/013 파일(훅 · `linePayload` · `PayloadDrawerParts` · `MeetingStatusBar` · `LineTaskButton`) **수정 0** |
| 2-6 테스트 | **PASS · WARN 1** | AppShell 4 · 헤더 순서 3 · CTA `it.each` 4행 · 패널 크기 · density 2 · static ㉔ 6. **네 폭 캡처가 없다** |

---

## 1. FAIL

**없다.** 브리프가 지목한 FAIL 조건 여덟을 전부 확인했다 — 마지막 외 `<a>` 있음 · `router.back` 0 · 제목이 배지 줄 아래 · 미리보기 전용 트리 0 · 패널 `absolute` 0 · 업무 헤더 순서 불변 · `PageHeader.tsx` 신설 0 · 012/013 범위 수정 0.

---

## 2. PASS — 무엇을 확인했나

### 2-1. breadcrumb · 「←」 (FE §6-3 · MF-7)

| 검사 | 결과 |
|---|---|
| `trail` 타입 | `Breadcrumb({ trail }: { trail: readonly Crumb[] })` · `Crumb = {label, href?}`(`AppShell.tsx:22-25`) |
| 앞 칸 = `<a>` | `last \|\| !crumb.href` 일 때만 `<span>`, 그 밖은 `<Link>`(`:52-62`). **마지막은 `href` 를 줘도 `<span>`** — 「자기 자신으로 가는 링크를 두지 않는다」 |
| hover/focus | `hover:text-fg-meta hover:underline focus-visible:ring-2 focus-visible:ring-primary` |
| Tab 도달 · focus 표시 | `AppShell.test.tsx:36` — `userEvent.tab()` → `toHaveFocus()` + 클래스에 `focus-visible:ring-2` |
| `<a>` 개수 단언 | `:23` 이 `links.map(textContent) === ["홈","회의록"]` · `toHaveLength(2)` · 마지막 `tagName === "SPAN"` 을 함께 본다(FE §6-3 「마지막 항목 외 `<a>` 0건이면 반려」의 반대 방향 증명) |
| `DetailHeaderBar` 위치 | **`AppShell.tsx:100-117`** — `PageHeader.tsx` 같은 새 파일이 없다(`components/shared/` 목록 확인) |
| 「←」 | `<Link href={backTo} aria-label="뒤로">`(`:104-110`) · `router.back(` 이 소스 전체에 **0건**(히트는 주석·테스트 이름뿐) |
| 부모 라우트 | 회의록 상세 셋 → `MEETINGS_ROUTE`(`/meetings/`) · 업무 상세 → `TASKS_ROUTE`(`/tasks/`) · **목록 화면은 `backTo` 를 안 넘긴다**(`TRAIL` 상수에 `backTo` 개념이 없고 `AppShell.test.tsx:61` 이 「←」 부재를 단언) |
| 업무 화면 | `git diff --stat -M features/tasks` = **1 파일 · +3 / −9** — 손으로 그린 `<nav>` 를 공용 부품으로 갈아끼운 것뿐이고 헤더 순서 · 그 밖 코드 변화 0 |

### 2-2. 헤더 순서 세 화면 (MF-8 · SPEC-006 U-4 · SPEC-007 U-1 · SPEC-008 U-3)

세 화면의 소스 순서가 같다 —

| 화면 | ① | ② | ③ | ④ |
|---|---|---|---|---|
| `MeetingScheduledPage.tsx` | `:105` DetailHeaderBar | `:109` MeetingBadgeRow | `:134` `<h1>` | `:136` `data-header-meta` |
| `MeetingLiveView.tsx` | `:245` | `:249` | `:284` | `:286` |
| `MeetingClosedPage.tsx` | `:41` | `:45` | `:64` `MeetingTitleInline` | `:65` `MeetingMetaLine` |

- **DOM 순서 단언이 세 화면 전부에 있다** — `compareDocumentPosition(...) === Node.DOCUMENT_POSITION_FOLLOWING` 를 badges→title, title→meta 두 번씩. 표지는 `data-header-badges` · `data-header-meta`.
- **배지 줄은 `MeetingBadgeRow` 하나**(`MeetingMetaInline.tsx`) — 좌측이 `MeetingWorkTypeInline variant="badge"` + `MeetingProjectInline variant="chip"` 로 **기존 컴포넌트 그대로**이고 배치만 옮겼다. 우측 `actions` 슬롯이 `flex items-center` 안에 있어 **배지와 같은 높이**다. 화면별 우측 — 시작 전 `⋯`+「회의 시작」 · 회의 중 「일시정지/재개」+「회의 종료」 · 종료 후 「삭제」+`MeetingStatusChip`.
- **`MeetingMetaLine` 에서 유형·프로젝트가 빠졌다** — docstring 이 「배지 줄(②)로 올라갔다(MF-8)」로 명시하고, 세 테스트가 「메타에 유형 · 프로젝트가 없다」를 함께 단언한다. 시작 전 「예정」은 `suffix` prop 으로 붙인다.
- breadcrumb 마지막 칸이 **회의 제목**이다 — SPEC-006 U-4 「breadcrumb 「홈 › 회의록 › \<제목\>」」 · SPEC-007 U-1(「회의 중」은 정정)과 맞다. 옛 「시작 전」 문자열이 사라졌다.
- **`MeetingDetailDrawer` 는 수정 0** — 변경 목록에 없다(이미 배지 줄 → 제목 순서라 손댈 것이 없었고, 그 테스트가 그대로 통과하는 것이 회귀 증거다).

### 2-3. 미리보기 CTA · 패널 크기 · 밀도 (MF-5 · 6 · SPEC-006 U-6 · U-8)

| 검사 | 결과 |
|---|---|
| CTA 4행 | `PREVIEW_CTA_LABEL: Record<MeetingDetail["status"], string>`(`MeetingPreviewPanel.tsx:57-62`) — `scheduled`·`recording` 「회의 입장」 / `generating`·`ended` 「상세보기」. 화면은 `PREVIEW_CTA_LABEL[meeting.status]`(`:113`) 하나만 읽는다 |
| 가는 곳 하나 | `meetingDetailHref(id)`(`:50`) = `/meetings/detail/?id=${id}` — 넷 다 같다. 정적 ㉔ 가 문구 리터럴이 각각 **2번씩만**(표 안) 나오는 것까지 센다 |
| 패널 높이 고정 | `MeetingsScreen.tsx` — `h-[calc(100vh-206px)] min-h-[480px] min-w-0 flex-1` |
| 본문만 스크롤 | `MeetingPreviewPanel.tsx:86` 바깥 상자 `min-h-0 min-w-0 flex-1 … overflow-hidden` · `:119` 본문 `min-h-0 flex-1 … overflow-y-auto` |
| 빈 상태와 같은 상자 | 테스트가 **클래스 문자열을 비교**해 「패널 바깥 크기가 내용에 따라 변하지 않는다」를 단언 |
| `position:absolute` | **0건** — `MeetingPreviewPanel.tsx:84` 의 히트는 「그렇게 배치하지 않는다」는 주석이다. 정적 ㉔ 가 목록·미리보기·상세 셋을 검사 |
| 폭 규칙 한 자리 | `MeetingListPanel.tsx:73` `w-[400px] shrink-0 … wide:w-[500px]` **하나**. `tailwind.config.ts:17 wide: "1440px"` → 1280~1439 = 400 · ≥1440 = 500 ✓. 우측은 `min-w-0 flex-1` 로 남는 폭. 정적 ㉔ 가 `MeetingsScreen` 에 폭 리터럴이 **0**임을 함께 잠근다 |
| 트리 하나 | `features/meetings/components/` 의 트리 파일이 `AgendaLineTree.tsx` **하나**. 미리보기는 `density="compact"` 로 같은 컴포넌트를 부른다(`:175-178`) |
| density 가 가르는 것 | `AgendaLineTree.tsx:45` `TreeDensity` · `AgendaHeader`·`LineRow` 로 내려간다. diff 를 줄 단위로 보면 **전부 클래스 스왑**이다 — 라벨 폭 34→26 · `text-row-label`→`text-badge` · `text-body`→`text-meta` · padding/gap. **구조 · 배지 · 펼침 규칙을 가르는 분기가 0** 이고 테스트가 「구조 · 배지 · 펼침 수가 같다」를 단언한다 |
| 미리보기 읽기 전용 | `AgendaLineTree` 를 읽기 전용 prop 으로 부른다(기존 동작 유지) |

### 2-4. 013 이관 — 파일 이름 둘 (동작 0)

`git diff HEAD -M` 이 rename 을 잡는다 —

```
{CreateTaskFromLineDrawer.tsx => ActionPayloadDrawer.tsx} | 2 +-      ← import 한 줄
{LinkTaskDrawer.tsx => TaskPayloadDrawer.tsx}             | 0        ← 0줄
```

`ActionPayloadDrawer.tsx` 의 유일한 변경은 `import { TaskDrawerHeader } from ".../LinkTaskDrawer"` → `".../TaskPayloadDrawer"` 한 줄이다. **동작 변경 0** ✓. 옛 이름(`CreateTaskFromLineDrawer` · `LinkTaskDrawer`)이 소스 전체에 **0건**이고 `openMeetingDrawers` · `MeetingDetailBody` · static needle 이 함께 갱신됐다. WORK-013 검수 W-2 가 닫혔다.

### 2-5. 금지 · 범위

- `fetch(` 직접 **0**(히트는 전부 `.refetch()`) · `localStorage` **0** · `retry: true` **0**
- `Sheet` 직접 import = `components/shared/DrawerFrame.tsx:33` **하나** · `Dialog` = `components/shared/ConfirmModal.tsx:33` **하나**(FE §6-1 · WORK-013 이 세운 상태 그대로)
- **012/013 범위 수정 0** — `hooks/` · `linePayload.ts` · `PayloadDrawerParts.tsx` · `MeetingStatusBar.tsx` · `LineTaskButton.tsx` 가 변경 목록에 없다. `LineRow` · `AgendaHeader` · `MeetingDetailBody` 는 바뀌었지만 **density 클래스와 import rename 뿐**이다(줄 버튼 · 편집 · 카운트 값 로직 0)

---

## 3. WARN

### W-1. 네 폭 실측 캡처가 없다 — 「둘 다 화면 안이다」는 아직 아무도 확인하지 않았다

- **빠진 검증**: WP Phase 3 — 「**1280 · 1439 · 1440 · 1920 네 폭에서 패널이 화면 안에 있다(수동 확인 캡처)**」 · SPEC-006 U-6.
- **원인**: `tauri dev` 창이 또 흰 화면이다(WORK-011 · 012 · 013 에 이어 **네 번째**). 이번에는 창을 1440×900 으로 맞춰 띄웠는데도 `MinWidthGuard` 문구조차 없어 **React 앱이 웹뷰에 마운트되지 않은 상태**로 보인다(`next dev` 는 200). 워커 변경과 무관한 환경 문제다.
- **무엇으로 대체됐나(그리고 무엇이 안 됐나)** —
  | 대체된 것 | 못 한 것 |
  |---|---|
  | 좌 폭 규칙이 `MeetingListPanel.tsx:73` 한 자리(`w-[400px] … wide:w-[500px]`)이고 `wide = 1440px` 라는 **클래스 문자열** 단언 | 그 클래스가 실제로 **1280 에서 400, 1440 에서 500** 으로 계산되는지 |
  | 우측이 `min-w-0 flex-1` 이라는 문자열 단언 | 좌 500 + gap + 우가 **1440 안에 들어가는지**(합계 검증) |
  | 패널 상자 클래스가 빈 상태와 같다는 문자열 비교 | `h-[calc(100vh-206px)]` 가 실제 뷰포트에서 **넘치지 않는지** |
- **jsdom 은 레이아웃을 계산하지 않는다** — 지금 있는 단언으로는 원리상 확인할 수 없는 항목이라, 테스트를 더 쓴다고 닫히지 않는다. **앱 창(또는 브라우저) 실측이 유일한 길**이고, 네 번 연속 막힌 tauri 웹뷰 자체가 먼저 풀려야 한다.

### W-2. `/tasks/` 목록에서 breadcrumb 「홈」이 **자기 페이지를 가리키는 `<a>`** 다

- **자리**: `AppShell.tsx` — `HOME_ROUTE = "/tasks/"` · `TASKS_ROUTE = "/tasks/"`(같은 값) · `TRAIL["/tasks/"] = [HOME_CRUMB, { label: "내 업무" }]`
- **무엇이 일어나나**: `/tasks/` 화면에서 `HOME_CRUMB` 은 마지막 칸이 아니므로 `<a href="/tasks/">홈</a>` 으로 렌더된다 — **눌러도 지금 그 페이지**다. `Breadcrumb` 자신의 규칙(「자기 자신으로 가는 링크를 두지 않는다」 — 마지막 칸을 `<span>` 으로 만드는 이유)과 결이 어긋난다.
- `/meetings/` 쪽은 문제가 없다(「홈」 → `/tasks/` 는 다른 화면).
- **의도된 임시 상태다** — 코드가 「홈은 아직 `/tasks/` 다(첫 화면 · SPEC-001 U-1)」로 이유를 적어 두었다. 홈 화면이 생길 때까지 남는 자리이고 **뿌리는 D-2** 다.

---

## 4. 문서 공백

| # | 자리 | 무엇이 비었나 |
|---|---|---|
| **D-1** | `frontend/README.md` §6-3 | 부품 이름을 **`AppShell` 의 `PageHeader`(S-02)** 로 두 번 적었고 강제 칸도 「`PageHeader` 의 `backTo` prop」이다. 그런데 WP §Internal Interface 와 코드는 **`DetailHeaderBar`** 다. 코드는 WP 를 따랐고 새 파일도 만들지 않아 브리프의 FAIL 조건을 피했지만, **아키텍처 문서와 이름이 다르다.** 어느 쪽으로 맞출지가 정해져 있지 않다(§6-3 을 고치든 부품을 개명하든) |
| **D-2** | `frontend/README.md` §6-3 breadcrumb 행 · SPEC-001 U-1 | **「홈」이 가리킬 라우트가 없다.** 첫 화면이 `/tasks/` 라 `HOME_ROUTE` 가 거기 물려 있고, 그 결과 `/tasks/` 에서 「홈」이 자기 페이지 링크가 된다(W-2). 홈 화면을 만들지 · 「홈」 칸을 목록에서 뺄지 · 그 칸만 링크를 안 걸지가 어느 문서에도 없다 |

---

## 5. WP 검증 항목 ↔ 테스트 대응표

**Phase 1 — breadcrumb 링크 · 「←」**

| 검증 항목 | 테스트 |
|---|---|
| 「홈」·「회의록」이 링크 · 마지막만 아님 · `<a>` 개수 | `AppShell.test.tsx:23` |
| `href` 를 준 마지막 칸도 링크 아님 | `:36` |
| **Tab 으로 닿고 focus 표시** | `:36`(`userEvent.tab()` + `toHaveFocus()` + ring 클래스) — **`Enter` 이동은 jsdom 이 못 본다**(`<a href>` 라 브라우저 기본 동작) |
| 「←」가 `/meetings/` 로 · `router.back()` 아님 | `:51` + 정적 ㉔ 1 |
| 목록 화면에 「←」 없음 | `:61` |
| 업무 화면 그 밖 코드 불변 | `git diff --stat -M features/tasks` = 1 파일 +3/−9 |

**Phase 2 — 헤더 순서**

| 검증 항목 | 테스트 |
|---|---|
| 세 화면 ①→②→③→④ DOM 순서 | `MeetingScheduledPage.test` · `MeetingLiveView.test` · `MeetingClosedPage.test` 각 1건(`compareDocumentPosition`) |
| 메타에 유형·프로젝트 없음 | 같은 세 건이 함께 단언 |
| 배지 줄 우측 액션 · 같은 높이 | `MeetingBadgeRow` 의 `items-center` + 세 화면 테스트가 버튼을 찾는다 |
| 배지 인라인 편집(기존 동작) | 기존 테스트 유지 |
| 상세 드로어 불변 | `MeetingDetailDrawer.test` 무수정 통과(회귀 확인) |

**Phase 3 — CTA · 크기 · 밀도**

| 검증 항목 | 테스트 |
|---|---|
| CTA 4행 | `MeetingPreviewPanel.test` `it.each` 네 행 + 정적 ㉔ 6 |
| 패널 바깥 크기 불변 · 본문만 스크롤 | 같은 파일 1건(클래스 문자열 비교) |
| **네 폭에서 화면 안** | **없음 — W-1** |
| 같은 컴포넌트 · 글자만 작다 | `AgendaLineTree.test` 2건 + 정적 ㉔ 4 |
| `position:absolute` 0 | 정적 ㉔ 3 |
| 미리보기 읽기 전용 | 기존 테스트 유지 |

**Phase 0 — 이름 이관**: `git diff -M` 이 rename 을 잡고 변경 줄이 1과 0이며 기존 테스트가 무수정 통과 — 그것이 「동작 0」의 증거다.

---

## 6. 요약

**공용 부품 하나로 정리됐다.** `Breadcrumb` 이 `Crumb[]` 를 받아 앞 칸을 `<Link>` 로 그리고 마지막은 `href` 를 줘도 `<span>` 으로 두며, `DetailHeaderBar` 가 같은 파일에 앉아 「←」를 **부모 라우트 `<a>`** 로 낸다 — `router.back(` 이 0건이라 새 탭·딥링크에서도 갈 곳이 있다. 세 회의 화면이 ①breadcrumb → ②배지 줄 → ③제목 → ④메타로 맞춰졌고 **DOM 순서를 `compareDocumentPosition` 으로** 단언한다(업무 헤더는 손대지 않았고 diff 가 +3/−9 다). 미리보기 CTA 는 상태 넷 한 표에서 나오고 가는 곳이 하나이며, 패널은 `absolute` 없이 흐름 배치로 높이를 고정하고 본문만 스크롤한다. **트리는 하나**이고 `density` 가 가르는 것은 클래스뿐이다. WORK-013 검수 W-2 로 올린 파일 이름 둘이 `git mv` 로 옮겨졌고 **변경 줄이 1과 0**이다.

남은 둘 중 **W-1 이 실질적이다** — 네 폭 실측은 jsdom 으로 대신할 수 없는 항목인데 tauri 웹뷰가 네 번째로 막혀 있다. 폭·높이 **규칙**은 정적 검사가 잠갔지만 **결과**는 아직 아무도 보지 못했다. **W-2** 는 홈 화면이 없어서 생긴 임시 상태이고 뿌리가 문서(D-2)에 있다. 커밋을 막을 무게는 없다.
