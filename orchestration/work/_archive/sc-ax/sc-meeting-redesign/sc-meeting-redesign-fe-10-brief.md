# [frontend] 바퀴 10 — `src/` 평면 구조를 도메인별로 나눈다 (이동만)

워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign` (커밋 `a65b490` 위, 깨끗함)

## 1. 이 바퀴가 무엇인가 — 그리고 무엇이 아닌가

`src/` 바로 아래에 **91파일**이 평면으로 깔려 있다. 페이지·부품·유틸·테스트가 한 곳에 섞였다.
**파일을 옮겨서 구조를 만든다.**

**이 바퀴가 아닌 것 — 절대 하지 마라:**

| 안 하는 것 | 왜 |
|---|---|
| **`WorkModals.tsx`(2847줄) 분해** | 업무 플로우가 곧 바뀐다. 지금 쪼개면 틀린 경계로 쪼개는 것이다 |
| **부품별 CSS 동거**(`Button.css` 같은 것) | 부품 경계가 안 굳었다. 나중에 |
| **CSS 파일 폴더 나누기** | `styles/` 는 **평면 그대로.** 15파일이 이름으로 구분된다 |
| **코드 내용 수정** | import 경로 말고는 한 줄도 고치지 마라. 리네임·리팩토링·정리 전부 금지 |

**순수 이동 + import 경로 수정.** 그 외는 전부 다음 기회다.

## 2. 목표 구조 (사용자 지정 — 이대로)

```
src/
├── main.tsx · App.tsx · vite-env.d.ts
│
├── ds/                     공용 부품
│   ├── icons/
│   │   ├── Icon.tsx
│   │   └── glyphs.ts       ← path 데이터만 분리 (Icon.tsx 가 커서 가르는 것. 내용 변경 아님)
│   ├── Button.tsx · Badge.tsx · Chip.tsx · SegmentedControl.tsx
│   ├── ProgressBar.tsx · Skeleton.tsx · Empty.tsx · StatusNote.tsx
│   ├── Popover.tsx · Modal.tsx · Select.tsx
│   ├── DateField.tsx · DatePicker.tsx · TimeField.tsx · TimeChip.tsx
│   ├── FormControls.tsx · DropZone.tsx · FileList.tsx
│   ├── GutterList.tsx · MinWidthNotice.tsx
│   └── Avatar.tsx · DataTable.tsx        ← 바퀴 9 가 만든 것
│
├── shell/                  AppShell.tsx · SideNav.tsx · InboxRail.tsx · CalendarRail.tsx
│
├── features/
│   ├── today/      TodayPage.tsx
│   ├── work/       MyWorkPage · WorkViews · WorkModals · useActionDraft.ts
│   ├── meetings/   (이미 폴더 있음 — 그대로)
│   ├── calendar/   CalendarPage.tsx
│   ├── report/     DailyReportPage.tsx
│   ├── project/    ProjectPage.tsx
│   ├── org/        OrgPage.tsx + 기존 org/ 6벌
│   ├── graph/      RelationGraphPage.tsx · GraphCanvas.tsx
│   ├── chat/       (이미 폴더 있음) + Composer.tsx
│   ├── action/     ActionCenter · ActionTaskCard · ActionMeetingCard
│   │               ActionProgressBatchCard · ActionPreview
│   ├── assistant/  AssistantCharacter · AssistantCharacterPicker
│   │               assistantCharacterAssets.ts · assistantPresentation.ts
│   └── auth/       LoginPage.tsx
│
├── lib/            api.ts · labels.ts · viewModels.ts · idempotency.ts
├── styles/         (평면 그대로 — 손대지 마라)
└── assets/         (그대로)
```

**테스트 36개는 짝이 되는 파일 옆에 둔다.** `ds/Button.test.tsx` 처럼.
공용 테스트(`App.test.tsx` 등)는 짝이 있는 곳으로.

**`glyphs.ts` 분리만 예외적으로 「내용을 가르는」 작업이다** — path 데이터 배열을 통째로 옮기는 것뿐이고
로직은 안 건드린다. 애매하면 **Icon.tsx 를 통째로 `ds/icons/` 에 두고 분리는 건너뛰어라.**

## 3. 하는 법

1. `git mv` 로 옮겨라 — 히스토리가 이어진다
2. import 경로는 **`tsc --noEmit` 이 전부 잡아준다.** 에러가 0이 될 때까지 고쳐라
3. **상대 경로가 깊어지면 그대로 둬라.** `tsconfig` 의 path alias(`@/…`) 도입은 이 바퀴가 아니다
4. `vitest` 의 경로·mock 이 깨지면 그것도 고쳐라 (테스트 파일 자체의 단언은 안 바꾼다)

## 4. allowed_paths

- `frontend/src/` — **`backend/` 는 한 줄도 안 건드린다**
- `frontend/src/styles/` 는 **읽기만.** 파일을 옮기지도 고치지도 마라

## 5. 검증

```
cd frontend && npx tsc --noEmit     → 0
cd frontend && npx vitest run        → 전체
cd frontend && npx vite build        → 성공
```

> 기준선: 커밋 `a65b490` 시점 **487 통과.**

**이 바퀴는 「487 그대로」가 유일한 합격선이다.** 이동만 하는 작업이라 테스트가 하나라도
줄거나 늘면 뭔가 잘못된 것이다. 깨진 게 있으면 **경로 문제인지 확인하고 경로만** 고쳐라.

**`git stash` 쓰지 마라.** 다른 세션과 스택을 공유한다. 임시 커밋을 써라.
**최종 커밋은 하지 마라 — 코디가 검증하고 커밋한다.** (임시 커밋은 남겨도 된다, 코디가 합친다)

## 6. 보고

- 옮긴 파일 수 · 최종 트리
- **`git mv` 로 옮겼는지** (히스토리 보존)
- `glyphs.ts` 분리했는지, 안 했으면 왜
- import 경로 고친 파일 수
- `tsc` · `vitest`(487 유지?) · `vite build`
- 옮기다 발견한 것(순환 참조·이상한 의존 등) — **고치지 말고 보고만**
