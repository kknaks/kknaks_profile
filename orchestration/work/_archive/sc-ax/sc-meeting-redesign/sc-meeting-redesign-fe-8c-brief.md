# [frontend] 바퀴 8-C — 병렬 경계에 걸려 미뤄둔 공유 부분을 정리한다

너는 **sc-ax `frontend` 워커**다. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign`
(branch `kknaksss/sc-meeting-redesign`, 머지 커밋 `247860c` 위)

## 0. ★ 먼저 — 이 워크트리에 사용자가 직접 작업 중이다

`git status` 에 **미커밋 5파일**이 있다. **사용자와 다른 클로드 세션이 지금 고치고 있는 것**이다:

```
frontend/src/App.tsx
frontend/src/AppShell.test.tsx
frontend/src/Icon.tsx
frontend/src/SideNav.tsx
frontend/src/styles/shell.css
```

내용은 좌측 내비 `persons` 아이콘을 시안대로 **채움(fill·evenodd·16그리드)** 으로 바꾸는 작업이다.

- **이 다섯 파일의 기존 변경을 되돌리거나 덮지 마라.** `git checkout`·`git restore`·`git stash` 절대 금지
- **커밋하지 마라.** 네 것도, 사용자 것도
- 그중 **`App.tsx` 는 네 §1 작업에 필요하다.** 아래 규칙대로만 만져라
- `Icon.tsx`·`SideNav.tsx`·`shell.css`·`AppShell.test.tsx` 는 **읽기만** 해라

## 1. 제목 줄이 두 개인 화면 다섯을 한 줄로

**증상**: 셸(`AppHeader`)이 제목을 그리는데 화면이 자기 `.page-head` 로 **또** 그린다.

| 화면 | 파일 |
|---|---|
| 캘린더 | `src/CalendarPage.tsx` |
| 조직 | `src/OrgPage.tsx` |
| 관계 탐색 | `src/RelationGraphPage.tsx` |
| 프로젝트 | `src/ProjectPage.tsx` |
| 일일보고 | `src/DailyReportPage.tsx` |

**바퀴 5a(J-2)·6a 가 업무·회의에 한 것과 같은 처리**를 해라 — 화면의 `.page-head` 를 없애고,
제목·액션을 셸 `AppHeader` 로 올린다. **5a 가 만든 seam**(`App.tsx` 의 머리 액션 등록)이 이미 있으니
**새 방식을 발명하지 말고 그것을 그대로 써라.**

**`App.tsx` 규칙**:
- 이 다섯 화면의 머리 배선에 필요한 **최소한만** 고쳐라
- 사용자가 그 파일에 이미 넣은 변경 근처를 건드리게 되면 **멈추고 보고**해라. 합치려 들지 마라
- 그 외 목적으로 `App.tsx` 를 고치지 마라

## 2. `.avatar` 를 구 `styles.css` 밖으로 옮긴다 (DS-gaps G-43)

이름 첫 글자를 원에 넣는 이니셜 아바타다. 새 DS 아바타는 `object-fit:cover` **사진 전제**라
글자를 못 받고 크기 램프도 없다 — **대체품이 없으니 우리가 계속 쓴다.**

- 구 `styles.css:114~119` 의 `.avatar` + `xs`·`sm`·`md`·`lg`·`xl` 5단을 **새 파일로 옮긴다**
- 옮기면서 **값을 `--scax-*` 토큰으로** 바꿔라(색·크기·글자). 기하는 그대로
- 사용처 12곳+ 이 **하나도 안 깨져야 한다**
- 이건 **바퀴 9(구 `styles.css` 삭제) 전에 반드시 닫혀야 하는 항목**이다

## 3. 액션 카드 「속」 폼 CSS 150줄 (바퀴 7 이 남긴 것)

바퀴 7 보고: 「공용 폼 부품(`Select`·`DateField`·`TimeField`)을 같이 건드려야 해서 P-3/P-5 로 미뤘다」.
그 경계가 이제 없다. 옮겨라.

## 4. 공유 클래스 넷 (바퀴 7 이 남긴 것)

`.task-card` · `.drawer-section` · `.revision-diff` · `.inline-reason` —
`WorkViews` · `WorkModals` · `TodayPage` · `RelationGraphPage` 가 **같이 쓴다**.
한 워커의 범위를 넘어서 아무도 못 옮겼다. 새 DS 로 옮겨라.

## 5. `.calendar-*` 전역화 (바퀴 8-B 가 남긴 것)

8-B 가 병렬 규약 때문에 `.calendar-screen` 안에 가둬 뒀다. 그래서 **지금 캘린더 화면과
업무 화면 우측 레일이 서로 다르게 보인다.** 가둔 것을 풀어 둘이 같은 모양이 되게 해라.

## 6. 결정 (재논의 금지)

| # | 내용 |
|---|---|
| **Q-1** | **구 `styles.css` 는 이 바퀴에서도 「지우지」 마라.** 옮긴 뒤 죽은 구획은 **보고만** — 삭제는 바퀴 9 에서 한 번에. 다만 §2 처럼 **옮기는 것**은 해야 한다(옮긴 자리에 사유 주석) |
| **Q-2** | `overrides-transitional.css` 는 이제 **줄여도 된다.** 이 바퀴에서 죽는 규칙이 있으면 지우고 보고해라 |
| **Q-3** | **레일을 새로 만들지 마라.** 사용자가 「시안 있는 두 화면만 레일」로 정했다(선택지 가). 시안 없는 화면은 단일 칸 그대로 |
| **Q-4** | `DS-gaps` ㉯ 항목은 손대지 마라. 새로 나오면 후보로 보고 |
| **Q-5** | **가짜 데이터·가짜 기능 금지.** BE 계약이 없어도 그리되 무엇이 비었는지 보고 |

## 7. allowed_paths

- `frontend/` — 단 §0 의 다섯 파일 중 **`App.tsx` 만** 최소 수정, 나머지 넷은 **읽기 전용**

**`backend/` 는 한 줄도 안 건드린다.**

## 8. 검증

```
cd frontend && npx tsc --noEmit     → 0 에러
cd frontend && npx vitest run        → 전체 1회
```

> 기준선: 머지 `247860c` 시점. **먼저 한 번 돌려 기준선 숫자를 확인하고 시작해라** —
> 사용자의 미커밋 변경이 섞여 있어 기준선이 474 가 아닐 수 있다. 네가 깬 것과 구분하려면 이게 먼저다.

- 클래스 선택자가 깨졌다 → 고친다
- **접근성·텍스트 질의가 깨졌다 → 멈추고 기능이 살아 있는지 먼저 확인**
- **「없음」 단언이 통과로 바뀌는 것** — 이번 세션에서 다섯 번 나왔다. §1 에서 `.page-head` 가 사라지는 자리를 특히 봐라

## 9. 보고

- §1~§5 각각 처리 결과
- **`App.tsx` 에서 네가 고친 줄**과 사용자 변경과 겹쳤는지
- **죽은 구 `styles.css` 구획**(줄 범위 + 근거) — 지우지 말고 보고만
- `overrides-transitional.css` 에서 지운 규칙
- `tsc` · vitest 기준선/최종 · 고친 테스트 · 접근성 질의로 깨진 것과 처리
- **빈 검사가 된 곳**
- `DS-gaps` 후보
