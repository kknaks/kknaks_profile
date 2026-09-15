# [frontend] 바퀴 5b — 업무 화면: 좌·우 레일 두 칸을 신설한다

너는 **sc-ax `frontend` 워커**다. 바퀴 5a 커밋 `15f5301` 위에서 이어간다.
작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign`

## 1. 이 바퀴가 무엇인가

바퀴 5 의 나머지 — **없던 칸 두 개를 만든다.** 5a 가 머리·본문을 시안대로 다시 그렸고,
지금 `AppBody` 는 본문만 있다. 시안은 세 칸이다.

| 칸 | 폭 | 내용 |
|---|---|---|
| 좌 레일 | **380 고정** | 수신함 — `GutterList`(제목 + count 배지 + 분류 `SegmentedControl`) 안에 카드 N장 |
| 본문 | min 640 | 5a 가 했다 |
| 우 레일 | **342 고정** | 캘린더 — 오늘/주간/월간 `SegmentedControl` + 근무 시간 + 일정 항목 N |

**레이아웃은 시안이 정본이고, 로직·데이터는 우리 것이다.**

## 2. SSOT (전부 read-only)

- **`ds-token-report.md` §8-A** — 「좌 레일」·「판단할 것의 자리」·「우 레일」·「칸별 상태」 네 행이 명세다
- **`MyWork.html`** · **`handoff/my-work/js/my-work.v2.jsx`** — `InboxCard` · `CalendarRail` · `AgendaItem` 의 시안 정본
- `handoff/my-work/css/components.css` — 이미 앱에 실려 있다
- `handoff/shell/js/scax-ui.jsx` 의 `GutterList` — **레일 목록용** 부품(우리 `src/GutterList.tsx` 와 이름만 같은 다른 것 — G-26)

현 앱: `src/MyWorkPage.tsx`(5a 가 바꿔 놓음) · `src/ActionTaskCard.tsx` · `src/ActionMeetingCard.tsx` · `src/WorkViews.tsx`(`TaskCalendar`) · `src/viewModels.ts` · `src/styles/overrides-transitional.css`

## 3. 결정 (재논의 금지)

| # | 결정 |
|---|---|
| **K-1** | **[L-4] 좌 레일은 우리 `actionItems` 를 시안 `InboxCard` 모양으로 그린다.** 데이터 모양이 다르니 **프론트에 어댑터**를 둔다. **`backend/` 무변경.** 시안이 요구하는데 **우리 데이터에 없는 필드는 그리지 않는다** — 빈 값·가짜 값 발명 금지 |
| **K-2** | **「판단이 필요한 업무」 패널을 본문 위에서 좌 레일로 옮긴다.** 5a 가 본문에 남겨 뒀다. 같은 데이터가 두 자리에 있으면 안 된다 — **옮기는 것이지 복제가 아니다** |
| **K-3** | **우 레일 캘린더는 우리 `TaskCalendar`(`WorkViews.tsx`)와 우리 `tasks` 로 채운다.** 새 데이터 원천을 만들지 마라. 별도 화면 `CalendarPage.tsx` 는 **이 바퀴에서 안 건드린다**(바퀴 8) |
| **K-4** | **「근무 시간」은 계약이 있을 때만.** 시안에 있지만 우리에게 그 데이터가 없으면 **J-1 대로 안 그린다.** 확인하고 보고해라 |
| **K-5** | **칸별 상태 4종**(default / empty / loading / error)을 레일 두 칸에 각각 그린다. 부품은 이미 있다 — `Skeleton` · `Empty` · `StatusNote`. **새로 만들지 마라** |
| **K-6** | **레일은 `AppBody` 의 `railLeft`·`railRight` 슬롯으로 넘긴다.** 레일을 안 넘기면 그 칸이 렌더되지 않는 구조다(셸 규약). 본문 안에 레일을 직접 그리지 마라 |
| **K-7** | **`overrides-transitional.css` 를 줄여라.** 「→ 바퀴 5」 규칙 여섯 중 **판단 카드(ActionTaskCard 6줄 · 진행일괄 · 활동기록)**가 이 바퀴에서 다시 그려진다. 죽은 것은 **지우고**, 못 지운 것은 **왜인지** |
| **K-8** | `DS-gaps` ㉯ 항목(G-04·05·07·08·09·26·28·29·30)은 **손대지 마라** |

## 4. allowed_paths

- `frontend/`

**`backend/` 는 한 줄도 안 건드린다. 읽는 것까지만이고 고치자는 제안도 쓰지 마라.**

## 5. 검증

```
cd frontend && npx tsc --noEmit     → 0 에러
cd frontend && npx vitest run        → 전체 1회
```

> 기준선: 바퀴 5a 시점 **`42 files · 472 tests` 전부 통과.**

5a 에서 배운 것을 그대로 적용해라 — **깨진 테스트의 종류로 네 작업을 판정한다:**

- 클래스 선택자 → 고친다
- **접근성·텍스트 질의** → **멈추고**, 기능이 살아 있는지 먼저 확인. 없앴으면 되살려라
- **「없음」 단언이 통과로 바뀜** → 조용한 구멍이다. 반드시 확인

**K-2 의 이동은 특히 위험하다** — 판단 카드가 본문에서 사라지고 레일에 나타나는 것이라,
그 카드를 찾던 테스트가 **자리만 바뀌었는데 「기능이 사라졌다」로 읽힐 수 있다.**
반대로 **본문에 남아 중복**되어도 테스트는 통과한다. 둘 다 확인해라.

자기점검:
- `backend/` 가 diff 에 **안 나오는가**
- **가짜 값·빈 값을 발명하지 않았는가**(K-1·K-4)
- 판단 카드가 **한 자리에만** 있는가(K-2)
- 레일을 `railLeft`/`railRight` 슬롯으로 넘겼는가(K-6)
- 새 데이터 원천을 만들지 않았는가(K-3)

## 6. 보고

코디(`term_18011a51-e9ec-4cad-9370-1836d3ee8d2d`)에게:

- **§8-A 레일 관련 4건 처리 결과**
- **K-1 어댑터가 버린 시안 필드 / 우리에게만 있는 필드** 전수
- **J-1 로 안 그린 것**(근무 시간 등)과 근거 → 백엔드 태스크 입력
- `tsc` · **vitest passed/failed** · 고친 테스트 수 · 접근성 질의로 깨진 것과 처리
- `overrides-transitional.css` 지운 규칙 / 못 지운 규칙과 이유
- 막혀서 못 한 것
