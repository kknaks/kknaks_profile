# [frontend] 바퀴 3b — 폼·오버레이 프리미티브를 새 DS 로

너는 **sc-ax `frontend` 워커**다. 바퀴 1·2·3a·3c 를 네가 했으면 그 맥락 그대로다.

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign` (바퀴 3c 커밋 `36ba1d5` 위)
base `origin/main` → PR `main` (PR 은 코디가 올린다)

## 1. 이 바퀴가 무엇인가

바퀴 10개 중 **③b** — 프리미티브의 마지막 조각이다.
①토큰 ②셸 ③a표시 ③c클래스이관(전부 완료) → **③b 폼·오버레이** → ④아이콘 → ⑤업무화면 → ⑥회의화면 → ⑦AX드로어 → ⑧남은7장 → ⑨은퇴.

3a 가 **읽는** 부품이었다면 3b 는 **쓰는** 부품이다 — 폼·모달·드로어·토스트.
여기까지 끝나면 공용 어휘가 한 벌로 갖춰지고, 남은 건 화면뿐이다.

## 2. SSOT — 먼저 읽을 것 (전부 read-only)

코디 워크트리 `…/work/sc-meeting-redesign/design/` 아래:

- **`handoff/shell/js/work-modal.jsx`** — 구현 정본. `Modal`(14줄) `Field`(36) `TextField`(51) `DateField`(61) `Composer`(72) `AutoComplete`(83) `Checklist`(120) `DropZone`(147) `Toast`(178)
- **`handoff/my-work/css/components.css`** — 이미 앱에 실려 있다(`src/styles/components.css`). 폼·오버레이 클래스가 여기 있다
- **`handoff/meetings/css/workspace.css`** — `.scax-drawer*` · `.scax-modal--sm/--md` · `.scax-field-row` · `.scax-time-chip`
- `components/datetime/DateField.d.ts` · `DatePicker.d.ts` · `TimeField.d.ts` — **새 DS 와 1:1 인 3종**의 props 정본
- `ds-token-report.md` §9 · `DS-gaps.md` — 대응 관계와 없는 것

현 앱: `src/Modal.tsx`(Drawer·ConfirmModal·Toast) · `src/FormControls.tsx`(Checkbox·FieldMessage) · `src/Select.tsx` · `src/DateField.tsx` · `src/DatePicker.tsx` · `src/TimeField.tsx` · `src/Composer.tsx` · `src/DropZone.tsx` · `src/FileList.tsx` · `src/Checklist*`(WorkModals 안) · `src/styles/overrides-transitional.css`

## 3. 결정 — `DS-gaps` 취급을 여기서 정밀화한다

바퀴 3a 의 「gaps 항목은 손대지 마라」는 **너무 뭉뚱그린 규칙**이었다. 두 종류를 가른다.

| 종류 | 무엇 | 이 바퀴에서 |
|---|---|---|
| **㉮ 껍데기는 DS·핸드오프에 있다** — 부품으로만 안 올라간 것 | G-10 `Drawer`(`.scax-drawer` 있음) · G-11 `ConfirmModal`(`.scax-modal--sm` 있음) · G-12 `TimeChip`(`.scax-time-chip` 있음) · G-13 `Toast`(핸드오프에 구현 있음) | **간다.** 사다리 ② — **껍데기는 DS 규약, 안의 구성은 우리 것.** 사용자 컨펌은 「DS 에 부품으로 올릴지」에 대한 것이지 우리가 쓸 수 있느냐가 아니다 |
| **㉯ 기하·값 자체가 없다** | G-04 `ProgressBar` · G-05 `FieldMessage` 톤 · G-07 `EmptyValue` · G-08 `TimeRangeField` · G-09 `MultiSelect` · G-28 링크버튼 · G-29 테두리배지 | **손대지 마라.** 구 부품을 그대로 둔다. **발명 금지** |

그 밖 결정:

| # | 결정 |
|---|---|
| **F-1** | **`Drawer` 폭은 사이즈 variant 로 연다** — `.scax-drawer` 골격(오른쪽 슬라이드·head/body/foot·오버레이 32%)을 쓰되 `--sm`(520) / `--lg`(840) 두 단. 업무 상세 드로어는 폼이 두 열이라 520 으로는 좁다. 지금 840 을 쓰던 6곳은 **`--lg` 로 간다**(화면 그대로) |
| **F-2** | **`DateField`·`DatePicker`·`TimeField` 3종은 새 DS 와 1:1** 이다(§9). `.d.ts` 를 props 정본으로 보고 갈아끼워라 |
| **F-3** | **props 는 우리 것을 지킨다**(3a·3c 와 같다). 다르면 호출부가 아니라 부품 안에서 맞춘다. 넓힌 것은 전건 보고 |
| **F-4** | **`Select` 는 props 가 다르다**(§9). 우리 `Select` 는 `options`·`searchable`·`footerAction`·`trigger` 를 받는다 — **이 시그니처를 지켜라.** 네이티브 `<select>` 로 되돌리지 마라(구 DS 때 7곳을 갈아낸 이력이 있다) |
| **F-5** | **샘플 데이터 금지.** `work-modal.jsx` 에 `TASK_MODAL_PEOPLE = ['홍길동','박민수','유하람']` · `TASK_MODAL_FILES` 가 박혀 있다. **가짜 이름·파일이 한 줄도 들어오면 안 된다** |
| **F-6** | `work-modal.jsx` 의 **`TaskCreateModal` 은 화면 조립물**이라 이 바퀴가 아니다(바퀴 5). 프리미티브만 가져와라 |
| **F-7** | **`overrides-transitional.css` 를 줄여라.** `Checklist` 를 새로 그리면 거기 「→ 바퀴 3b 또는 5」로 달린 규칙 2줄이 죽는다. 죽었으면 **지우고** 보고해라. 못 지우면 왜인지 |
| **F-8** | 아이콘 이름은 지금 있는 것을 쓴다. 모자라면 만들지 말고 보고(바퀴 4 입력) |

## 4. allowed_paths

- `frontend/`

**`backend/` 는 한 줄도 안 건드린다. 읽는 것까지만이고 고치자는 제안도 쓰지 마라.**

## 5. 검증

```
cd frontend && npx tsc --noEmit     → 0 에러
cd frontend && npx vitest run        → 전체 1회 (이 바퀴도 예외 허용)
```

> 기준선: 바퀴 3c 시점 `41 files · 468 tests` 전부 통과(3회 연속).

**폼은 접근성이 곧 기능이다.** 3c 와 같은 감사를 하되 대상이 다르다 —
`label`·`aria-label`·`aria-describedby`·`id`/`htmlFor` 짝·`required`·`disabled`·`onChange` 가
옮기는 과정에서 **사라진 곳이 없는지** `git diff` 로 훑고 건수를 보고해라.

깨진 테스트는 이관이 원인인 것만 고쳐라.
**`getByLabelText`·`getByRole("textbox"|"combobox"|"dialog")` 가 깨졌다면 테스트가 아니라 네 이관이 틀린 것이다** — 코드를 고쳐라.

자기점검:
- `backend/` 가 diff 에 **안 나오는가**
- **㉯ 항목(G-04·05·07·08·09·28·29)을 안 건드렸는가**
- **가짜 데이터가 한 줄도 안 들어왔는가**(F-5)
- `Select` 시그니처를 **안 바꿨는가**(F-4) · 네이티브 `<select>` 로 되돌린 곳이 없는가
- `overrides-transitional.css` 가 **줄었는가**(F-7)

## 6. 하지 말 것

- 화면 레이아웃·모달 내용 구성을 바꾸지 마라. 바퀴 5·6 이다.
- 시안에 없다는 이유로 필드·기능을 지우지 마라. 남기고 보고.
- 커밋·push 하지 마라.

## 7. 보고

코디(`term_18011a51-e9ec-4cad-9370-1836d3ee8d2d`)에게:

- **부품별 대응표** — 갈았다 / 남겼다(어느 종류 ㉮㉯ 이고 왜) / 새로 만들었다
- `tsc` · **vitest passed/failed** · 고친 테스트 수와 이유
- **접근성 속성 감사 결과** (각 속성 before/after 건수)
- 구 `styles.css` 지운 줄 수 · **`overrides-transitional.css` 에서 지운 규칙**
- 넓힌 prop 전건
- 아이콘이 모자라 못 그린 자리 (바퀴 4 입력)
- 막혀서 못 한 것
