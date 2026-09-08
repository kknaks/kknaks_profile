# WORK-014 Phase 0~3 (frontend) — 완료 보고

브랜치 `kknaksss/docs-v1` · 워크트리 `/Users/kknaks/orca/workspaces/task_management/docs-v1` · **커밋·push 하지 않음**

## 변경 파일 (전부 `app/front/`)

**Phase 0(WORK-013 검수 WARN 2 이관) — 이름을 내용에 맞춘다**
- `components/CreateTaskFromLineDrawer.tsx` → **`ActionPayloadDrawer.tsx`**(git mv · R)
- `components/LinkTaskDrawer.tsx` → **`TaskPayloadDrawer.tsx`**(git mv · R)
- import · `openMeetingDrawers` · `MeetingDetailBody` · `static.test` needle 갱신. **동작 변경 0**(테스트 그대로 통과)

**Phase 1** — `components/shared/AppShell.tsx`(신규 `Crumb` · 링크 breadcrumb · `DetailHeaderBar` · 라우트 상수) ·
`components/shared/AppShell.test.tsx`(신규) · 세 회의 화면 + `features/tasks/components/TaskDetailPage.tsx`

**Phase 2** — `MeetingScheduledPage.tsx` · `MeetingLiveView.tsx` · `MeetingClosedPage.tsx` · `MeetingMetaInline.tsx`(신규 `MeetingBadgeRow` · `MeetingMetaLine` 축소)

**Phase 3** — `MeetingPreviewPanel.tsx` · `MeetingsScreen.tsx` · `AgendaLineTree.tsx`(`TreeDensity`) · `AgendaHeader.tsx` · `LineRow.tsx`

**테스트 6** — `AppShell.test`(신규 4) · `MeetingScheduledPage.test` · `MeetingLiveView.test` · `MeetingClosedPage.test`(헤더 순서 셋) ·
`MeetingPreviewPanel.test`(CTA 4행 + 패널 크기) · `AgendaLineTree.test`(density 2) · `static.test`(㉔ 신설 6)

`src-tauri/tauri.conf.json` 은 **내가 만진 게 아니다** — 디스패치 전부터 modified 였다.

## Phase 1 — breadcrumb 링크 · 「←」

- `Breadcrumb trail` 이 `readonly {label, href?}[]` 가 됐다. **앞 칸은 `<a>`**(hover 밑줄 + `focus-visible:ring`), **마지막은 `href` 를 줘도 `<span>`** 이다
  (자기 자신으로 가는 링크를 두지 않는다). 테스트가 `<a>` 개수와 태그 이름을 함께 단언한다.
- `DetailHeaderBar({trail, backTo})` 를 **같은 파일에** 뒀다(`PageHeader.tsx` 신설 없음). 「←」는 `<Link href={backTo}>` 이고
  **`router.back()` 이 0건**이다(정적 검사 — 주석 제외). 회의록 상세 셋 → `/meetings/` · 업무 상세 → `/tasks/` · **목록 화면은 `backTo` 없음**.
- 업무 상세는 손으로 그린 `<nav>` 를 공용 부품으로 갈아끼운 것뿐이다 — `git diff --stat features/tasks` 가 **1 파일 · +3 / −9**(헤더 순서 · 그 밖 코드 0).

## Phase 2 — 헤더 순서 세 화면

- 세 화면 모두 **① breadcrumb(+「←」) → ② 배지 줄 → ③ 제목 → ④ 메타** 다. DOM 순서를 `compareDocumentPosition` 으로 단언했다
  (`data-header-badges` · `data-header-meta` 표지).
- 배지 줄은 `MeetingBadgeRow` 하나가 그린다 — 좌 [유형 ˅][● 프로젝트 ˅] · 우 그 화면의 액션이 **같은 줄 · 같은 높이**다.
  시작 전 `⋯`+「회의 시작」 · 회의 중 「일시정지/재개」+「회의 종료」 · 종료 후 「삭제」+상태 칩.
- `MeetingMetaLine` 에서 유형 · 프로젝트를 뺐다 — 「<일시> · <n분>」(+ 시작 전 「예정」). 메타에 유형·프로젝트가 없다는 것도 단언했다.
- 배지 인라인 셀렉터는 **기존 컴포넌트 그대로**(`variant="badge"`/`"chip"`)이고 `PATCH /api/meetings/{id}` 경로도 그대로다.
- 상세 드로어(`MeetingDetailDrawer`)는 이미 배지 줄 → 제목이라 **손대지 않았다**(그 테스트가 그대로 통과 = 회귀 확인).

## Phase 3 — 미리보기 CTA · 크기 · 밀도

- CTA 문구가 **상태 넷 한 표**(`PREVIEW_CTA_LABEL`)에서 나온다 — `scheduled`·`recording` 「회의 입장」 / `generating`·`ended` 「상세보기」,
  **가는 곳은 넷 다 `/meetings/detail?id=`**. `it.each` 로 네 행을 전부 돌고, 문구를 손으로 적은 자리가 없다는 정적 검사도 넣었다.
- 패널 높이를 `MeetingsScreen` 이 고정(`h-[calc(100vh-206px)]` · `min-h-[480px]`)하고 미리보기는 `min-h-0 … overflow-hidden` 상자 안에서
  본문만 `overflow-y-auto` 한다. **빈 상태와 바깥 클래스가 같다**는 것을 테스트가 문자열로 비교한다(내용이 늘어도 상자가 안 커진다).
  `position:absolute` 는 셋 다 0건(주석 제외).
- `AgendaLineTree` 에 `density?: "default"|"compact"` 를 더했다 — **미리보기 전용 트리를 만들지 않았고**(트리 컴포넌트 1),
  가르는 것은 글자 · 여백 · 라벨 폭뿐이다(라벨 34→26 · `text-row-label`→`text-badge` · 줄 padding). 테스트가 **구조 · 배지 · 펼침 수가 같다**는 것과
  클래스만 달라진다는 것을 함께 단언한다.

## 검증

- `npx tsc --noEmit` → **Errors 0**
- `npx vitest run` → **36 files / 360 tests 전부 통과**(0 실패)
- `npx next lint` → **Error 0**
- 정적(직접 grep · 주석 제외) — `router.back(` **0** · 패널 `absolute` **0** · 트리 컴포넌트 **1**(`AgendaLineTree.tsx`) ·
  손으로 그린 breadcrumb `<nav>` **0** · `git diff --stat features/tasks` = +3/−9
- 정적(`static.test.ts` ㉔ 신설 6) — 위 다섯 + 「패널 폭 규칙이 한 자리(좌 400/500 고정 · 화면은 폭 리터럴 0)」

## 미결 · 주의점

- **앱 창 네 폭 실측 미완.** `tauri dev` 창이 **또 흰 화면**이다(WORK-011 · 012 · 013 에 이어 네 번째 · 내 변경과 무관).
  이번에는 창을 1440×900 으로 **크기까지 맞춰** 띄웠는데도(`w014-1440.png`) 여전히 빈 화면이고,
  `MinWidthGuard` 문구조차 없어 **React 앱이 웹뷰에서 아예 마운트되지 않는 상태**로 보인다(`next dev` 는 `/` · `/meetings/` 모두 200).
  기본 브라우저(Whale)로도 열어 봤지만 그 프로세스는 System Events 접근이 거부돼(-10003) 창을 앞으로 못 세웠다.
  → **1280 · 1439 · 1440 · 1920 캡처는 못 만들었다.** 대신 폭·높이 규칙을 정적 검사와 클래스 단언으로 고정했다.
- **회의 중 배지는 표시만**이다(`locked`) — 회의 중 메타 잠금이 기존 동작이라 그대로 뒀다. 시작 전 · 종료 후는 인라인으로 바뀐다.
- **시작 전 제목 · 일시는 표시만**이다 — SPEC-006 U-4 가 「수정 경로는 상세 드로어와 캘린더」라고 못박아 그 화면에 편집을 새로 열지 않았다.
