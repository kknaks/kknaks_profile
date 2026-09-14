# [frontend] 바퀴 11 — `ds/` 를 앱에서 떼어낸다 (문구는 전부 prop 으로)

워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign` (커밋 `3bc74df` 위, 깨끗함)

## 1. 목표 — 규칙 하나

> **`ds/` 안에 사람이 읽는 글자가 하나도 없다.**

바퀴 10 이 `ds/` 폴더를 만들었지만 부품이 아직 앱에 묶여 있다:

- `ds/` → `lib/labels` import **5곳** (`DatePicker` · `Empty` · `TimeField` · `Select` · `MinWidthNotice`)
- `ds/` 안 하드코딩 한국어 **22줄 / 9파일**
  (`DatePicker` · `ProgressBar` · `Popover` · `TimeField` · `FormControls` · `Skeleton` · `FileList` · `Modal` · `Select`)

`api.ts`·`viewModels.ts` 같은 **앱 데이터 의존은 0이다** — 문구만 걸려 있다. 그것만 떼면 된다.

## 2. 하는 법 — 기본값을 두지 마라

**(나) 완전 분리다. 기본값으로 얼버무리지 마라.**

```tsx
// 이렇게 하지 마라 — 부품이 여전히 한국어를 안다
export function Empty({ actionLabel = "다시 시도" }) { … }

// 이렇게 — 부품은 언어를 모른다
export function Empty({ actionLabel }: { actionLabel: string }) { … }
```

**호출부는 `lib/labels` 에서 가져다 넘긴다:**

```tsx
// features/work/MyWorkPage.tsx
import { emptyActionLabel } from "../../lib/labels";
<Empty actionLabel={emptyActionLabel("filter")} />
```

이러면 **문구는 여전히 `lib/labels` 한 곳에 모이고, 부품은 언어를 모른다.** 둘 다 지킨다.

**호출부 62곳** — `Empty` 42 · `Select` 16 · `DatePicker` 2 · `TimeField` 2 · `MinWidthNotice` 0.

## 3. 예외 — 문구가 아닌 것

`DatePicker` 가 `lib/labels` 에서 가져오는 것 중 **문구가 아닌 것**이 있다:

- `seoulToday()` · `weekdayNames` · `formatDate` · `formatMonthLong` · `addDays`

**요일 이름은 문구다** — prop 으로 빼라(`weekdayNames: string[]`).
**시간대·날짜 계산(`seoulToday`·`addDays`·`format*`)은 문구가 아니다** — 이걸 prop 으로 빼면 호출부 2곳이
달력 로직을 들고 있게 된다. 그건 더 나쁘다.

→ **날짜 계산 유틸은 `ds/` 안으로 옮기거나 그대로 둬라.** 어느 쪽이 나은지 네가 판단하고 보고해라.
   기준은 「그 함수가 한국어·서울을 아는가」다. 안다면 문구 취급, 모른다면 유틸 취급.

## 4. 하지 말 것

| | |
|---|---|
| **기본값 prop 금지** | §2. 「안 넘기면 한국어」는 분리가 아니다 |
| **부품 동작·기하 변경 금지** | 시그니처에 문구 prop 이 느는 것 말고는 한 줄도 바꾸지 마라 |
| **`lib/labels.ts` 재작성 금지** | 거기서 가져다 쓰는 것뿐이다. 구조를 바꾸지 마라 |
| **CSS 손대지 마라** | `styles/` 는 읽기만 |
| **`ds/icons/glyphs.tsx`** | `title` 같은 접근성 문구가 있으면 그것도 대상이다. path 데이터는 손대지 마라 |

## 5. allowed_paths

- `frontend/src/` — **`backend/` 는 한 줄도 안 건드린다**

## 6. 검증

```
cd frontend && npx tsc --noEmit     → 0
cd frontend && npx vitest run        → 전체
cd frontend && npx vite build        → 성공
```

> 기준선: 커밋 `3bc74df` 시점 **487 통과.**

**이 바퀴의 진짜 합격선은 이거다:**

```
grep -rn --include='*.tsx' '"[가-힣]' src/ds/ | grep -v '.test.'   →  0줄
grep -rn 'from ".*lib/' src/ds/ | grep -v '.test.'                  →  0줄 (§3 예외 빼고)
```

**둘 다 보고에 실제 출력으로 붙여라.**

깨진 테스트는 **문구가 사라져서 못 찾는 것**일 가능성이 높다. 그건 호출부가 문구를 안 넘겨서다 —
**테스트를 고치지 말고 호출부를 고쳐라.** 접근성 질의(`getByRole(name:)`)가 깨지면 특히 그렇다.

**`git stash` 쓰지 마라.** 임시 커밋을 써라. **최종 커밋은 하지 마라** — 코디가 검증하고 커밋한다.

## 7. 보고

- **위 grep 두 개의 실제 출력**
- 부품별 추가한 prop 전수 (이름·타입)
- 고친 호출부 수
- §3 날짜 유틸을 어느 쪽으로 판단했는지와 근거
- `tsc` · `vitest`(487 유지?) · `vite build`
- 문구를 넘기려다 **호출부에 마땅한 값이 없던 자리**가 있으면 그것 (설계가 어긋난 신호다)
