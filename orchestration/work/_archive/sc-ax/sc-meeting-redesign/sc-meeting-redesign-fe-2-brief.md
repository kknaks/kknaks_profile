# [frontend] 바퀴 2 — 셸을 새 DS 로 갈아탄다

너는 **sc-ax `frontend` 워커**다. 바퀴 1(토큰)을 네가 했다면 그 맥락을 그대로 쓴다. 처음이면 역할 문서부터:

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/roles/sc-ax/frontend/role.md` (+ `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign` (바퀴 1 커밋 `1ff3e51` 위에서 시작)
base `origin/main` → PR `main` (PR 은 코디가 올린다)

## 1. 이 바퀴가 무엇인가

바퀴 9개 중 **②** 다. ①토큰(완료) → **②셸** → ③프리미티브 → ④아이콘 → ⑤업무화면 → ⑥회의화면 → ⑦AX드로어 → ⑧남은7장 → ⑨은퇴.

**이 바퀴는 13화면이 한 번에 흔들리는 바퀴다.** 틀을 갈면 페이지 10장 + 오버레이 3개가 전부 영향을 받는다.
그 흔들림을 **부품 교체(바퀴 3) 전에** 겪어야 원인이 안 섞인다 — 그래서 여기 있다.

구 `.thesc-shell` · `.rail` · `.canvas` · `.canvas-topbar` 를 **새 DS 의 `AppShell` / `AppHeader` / `AppBody` / `SideNav`** 로 갈아탄다.

## 2. SSOT — 먼저 읽을 것 (전부 read-only)

코디 워크트리 `…/orchestration/work/sc-meeting-redesign/design/` 아래:

- **`ds-token-report.md` §6**(442~462줄) — 셸 넷이 무엇을 받고 어떤 클래스를 쓰나. **클래스 어휘 목록이 거기 있다.**
- `ds-token-report.md` §3-1(394~409줄) · §4(410~424줄) — element 리셋 처리
- `ds-token-report.md` §10(659~684줄) — 화면 13개 전수표. **네 스크롤 점검 목록이다.**
- `components/shell/AppShell.jsx` · `AppShell.d.ts` · `SideNav.jsx` · `SideNav.d.ts` · `shell.css`
- `handoff/shell/js/nav.js` — 메뉴 목록의 **시안 예시**(정본 아님, §3 D-F 참조)
- `MyWork.html` · `MeetingWorkspace.html` — 셸을 실제로 어떻게 쓰는지 보는 용례

현 앱: `frontend/src/App.tsx` (특히 `28~48` surface 정의 · `332` 로그인 분기 · `414~430` breadcrumb · `456~513` 화면 전환) · `frontend/src/styles.css` `101~160`

## 3. 결정 (코디가 정했다 — 이대로 간다, 재논의 금지)

| # | 결정 |
|---|---|
| **D-A** | **breadcrumb 줄은 이 바퀴에서 지우지 않는다.** 최종 결정은 「삭제」지만 실행은 **바퀴 6**이다. 지금 지우면 회의 상세에서 목록으로 돌아갈 길이 바퀴 6까지 사라진다(`App.tsx:414~430` 의 `closeMeeting` 이 유일 경로). `AppHeader` 가 `breadcrumb` prop 을 받으니 **과도기엔 그대로 넘겨라** |
| **D-B** | **`min-width:1542px` · `height:100vh` · `overflow:hidden` 은 시안대로 적용한다.** 대신 **화면마다 본문이 자기 스크롤 컨테이너를 갖게 만든다** — 이게 이 바퀴의 진짜 일이고 합격선이다(§6) |
| **D-C** | **`MinWidthNotice` 는 건드리지 마라.** 프로덕션 사용처가 0곳이라 이미 안 뜬다. 파일 삭제는 바퀴 9 |
| **D-D** | **구 `styles.css` 의 shell 구획(`101~139`, 39줄)을 지운다.** `.page-surface`·`.page-head`(`140~160`)는 페이지가 아직 쓰므로 **남긴다.** 지운 자리에 `/* 바퀴 2: … */` 한 줄 |
| **D-E** | **`shell.css` 의 맨 위 element 리셋 7줄을 잘라내고** `src/styles/shell.css` 로 싣는다(바퀴 1 의 `product.css` 와 같은 처리, 같은 꼴의 사유 주석). `.scax-*` 클래스 규칙만 남긴다 |
| **D-F** | **메뉴 목록은 우리 것이 정본.** `nav.js` 의 `NAV_MAIN` 8종은 시안 예시다. 우리 `ProductSurface` 8종(`App.tsx:28~48`)이 정본 — **순서·아이콘·그룹 나눔·접기 동작은 시안**을 따르되, **시안에 있고 우리에 없는 메뉴(수신함·진행 현황·자료)는 만들지 마라.** 갈 화면이 없다 |
| **D-G** | AX 채팅 드로어·액션 센터·어시스턴트 모달은 **이 바퀴에서 안 건드린다**(바퀴 7). 셸 위에 얹힌 채로 계속 뜨기만 하면 된다 |
| **D-H** | 프리미티브(`Button`·`Badge`·`Select`…)는 **바퀴 3** 이다. 셸이 요구하는 최소한만 손대고, 눈에 거슬려도 지금 갈지 마라 |

## 4. 구현 단계

1. `design/components/shell/` 의 `AppShell.jsx` · `SideNav.jsx` 를 `frontend/src/` 의 **기존 구조 안**으로 옮긴다(TSX 로). **새 폴더 체계를 만들지 마라** — `src/AppShell.tsx` · `src/SideNav.tsx` 꼴이면 된다. `.d.ts` 가 props 정본이다.
2. `shell.css` 를 D-E 대로 `src/styles/shell.css` 로 싣고 `src/styles/index.css` 에 `@import` 추가.
3. `App.tsx` 를 갈아탄다 — `.thesc-shell`/`.rail`/`.canvas`/`.canvas-topbar` → `AppShell`/`SideNav`/`AppHeader`/`AppBody`. surface 전환 로직은 **그대로 둔다**(로직은 우리 것).
4. **스크롤 경계를 화면마다 잡는다** (§6 의 목록 13개 전부).
5. D-D 로 구 `styles.css` shell 구획 삭제.
6. 검증(§6).

## 5. allowed_paths

- `frontend/`

**`backend/` 는 한 줄도 안 건드린다. 읽는 것까지만이고 고치자는 제안도 쓰지 마라.**

## 6. 검증 — 합격선

```
cd frontend && npx tsc --noEmit          → 0 에러
cd frontend && npx vitest run             → 전체 1회 (이 바퀴도 예외로 허용)
```

**전체 스위트를 1회 돌리는 이유**: 셸은 전역이라 부분 테스트로는 회귀를 못 잡는다. 사용자 방침의 예외로 코디가 허용한다. **깨진 것은 고쳐라** — 단 셸 교체가 원인인 것만. 원인이 다른 데 있으면 고치지 말고 보고해라.

> 기준선: 바퀴 1 시점 `40 files · 467 tests` 전부 통과. `src/Checklist.test.tsx` 에 flaky 1건이 있다(단독 3회 중 1회 재현) — **이건 네가 깬 게 아니다.**

**스크롤 점검 — 13개 전부 한 줄씩 보고해라.** `overflow:hidden` 인 셸 안에서 내용이 길 때 **잘리지 않고 스크롤되는가**:

`LoginPage` · `TodayPage` · `CalendarPage` · `MeetingListPage` · `MeetingDetailPage` · `MyWorkPage` · `DailyReportPage` · `ProjectPage` · `OrgPage` · `RelationGraphPage` · `ChatDrawer` · `ActionCenter` · `AssistantCharacterPicker`

테스트로 잡히는 게 아니니 **코드를 읽어서 판단하고**, 확신이 안 서는 화면은 「확인 못 함」으로 적어라 — **된다고 쓰지 마라.**

자기점검:
- `backend/` 가 `git diff` 에 **안 나오는가**
- `design/` 폴더(코디 워크트리)를 **안 고쳤는가**
- surface 전환·권한 판단(envelope) 로직을 **안 바꿨는가** — 레이아웃만 바꾼다
- `nav.js` 에 있다는 이유로 **없는 메뉴를 만들지 않았는가**
- breadcrumb 을 **살려 뒀는가**(D-A)

## 7. 하지 말 것

- 프리미티브·아이콘·화면 내용을 갈지 마라. 바퀴 3~6 이다.
- 시안에 없다는 이유로 **기능을 지우지 마라.** 자리가 애매하면 남기고 보고해라.
- 커밋·push 하지 마라. 코디가 검증하고 커밋한다.
- 빈 값·가짜 메뉴·가짜 사용자 정보를 만들지 마라. `SideNav` 의 `user`·`version` 은 우리 데이터에서 오거나, 없으면 안 그린다.

## 8. 보고

코디(`term_18011a51-e9ec-4cad-9370-1836d3ee8d2d`)에게:

- `tsc` 결과 · **vitest passed/failed** — 깨진 것은 파일명·원인·고쳤는지
- **스크롤 점검 13줄** (된다 / 안 된다 / 확인 못 함)
- 구 `styles.css` 에서 실제로 지운 줄 수
- D-F 로 **안 만든 메뉴**가 무엇인지
- 시안과 달라진 자리가 있으면 그것과 이유
- 막혀서 못 한 것
