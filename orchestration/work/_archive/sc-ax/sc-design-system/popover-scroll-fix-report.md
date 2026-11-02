# 팝오버 스크롤 버그 결과 보고 — frontend

- 작업일: 2026-09-08 · 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `9b437bc`, 커밋 없음)
- 사용자 보고: 「팝오버들 다 스크롤이 안 되는 것 같다 — 내용이 길면 잘리거나 화면 밖으로 나간다」

## 상태: done

---

## 1. 디자인 v2 의 높이 규정 — **없다**

`docs/design/design-system-v2.dc.html` `14 — OVERLAY` 의 Popover 절은 이것만 정한다:

> 폭 200–400 · 스크림 없음 · 트리거 바로 아래·좌측 정렬, 8px 띄움 · 아래 공간이 모자라면 위로 · shadow-lg · r12

`04`(패딩 8/10)·`06`(r12)·`14`(shadow-lg)를 다 뒤져도 **높이·max-height·스크롤 규정은 없다.**
그래서 브리프 §1 의 지시대로 「뷰포트 안에서 잘리지 않게 max-height + 내부 스크롤」을 규칙으로 삼았고,
그 규칙을 `Popover.tsx` 주석과 `styles.css` 주석에 근거와 함께 적어 두었다.

## 2. 소비처 전수

`grep -rn "Popover" src --include="*.tsx"` — Popover 를 쓰는 곳은 **둘뿐**이다.

| # | 소비처 | 자리 | 내용 |
|---|---|---|---|
| 1 | `MyWorkPage.tsx:357` 상태 필터 칩 | 내 업무 툴바 (앱에서 살아 있는 유일한 소비처) | `popover-item` 7개 |
| 2 | `DatePicker.tsx:173` | **앱에는 마운트되지 않음** — DS 부품으로만 존재 | 헤더(달 이동) + 격자 + 푸터 |
| — | `ds-entry.tsx:5` | `Popover` 를 claude.ai/design 으로 내보낸다 | 내용은 디자인 쪽이 정한다 |

> **브리프가 적은 「조직 화면」에는 Popover 가 없다** — 어제 만든 v3 화면은 Popover 를 쓰지 않는다.
> `DateField`(WorkModals · ActionCenter · DailyReport)는 Popover 가 아니라 브라우저의 `showPicker()` 를 쓴다.
> 즉 「팝오버들 다」의 실체는 **컴포넌트 하나**이고, 고칠 자리도 하나였다.

## 3. 원인

`.popover` 에는 이미 `overflow: auto` 와 `max-height: min(60vh, 420px)` 가 있었다. 그래서 **패널 자체는 스크롤됐다**
(측정: `scrollHeight 1274 / clientHeight 334`, `scrollTop = 200` 이 먹힌다). 진짜 문제는 그 다음이다.

**`max-height` 가 뷰포트 높이만 보고 정해진다 — 트리거가 어디 있는지는 보지 않는다.**

- 트리거가 화면 중간·아래에 있으면 트리거 아래에 남은 자리는 `60vh` 보다 훨씬 작다.
- 그래도 패널은 `60vh`(또는 420) 만큼 자라서 **화면 밖으로 삐져나간다.**
- 삐져나간 부분에는 스크롤 트랙의 아래쪽과 마지막 항목들이 들어 있다 — 사용자 눈에는
  「잘렸고, 스크롤도 안 된다」로 보인다. 스크롤 자리 자체가 화면 밖에 있으니 맞는 말이다.

위로 뒤집는 판단도 같은 병을 앓았다: `anchor.top > 패널높이 + 8` 일 때만 뒤집으므로,
**아래도 좁고 위도 패널만큼은 안 넓은** 흔한 자리에서는 뒤집지 않고 그냥 삐져나갔다.

보조 원인 하나 더: `overscroll-behavior` 가 없어 팝오버 끝까지 내려간 뒤 휠이 뒤 페이지로 넘어갔다 —
「팝오버가 아니라 페이지가 스크롤된다」는 인상을 준다.

## 4. 수정 (Popover.tsx + styles.css 의 popover 규칙에 한정)

**`Popover.tsx`** — 열릴 때 트리거의 지금 자리에서 남은 공간을 재고, 그 값을 인라인 `max-height` 로 준다.

```
GAP 8 (v2 14 의 띄움) · EDGE 8 (뷰포트 가장자리 여유) · MAX 420 (기존 상한 유지) · MIN 160 (항목 서너 개)

spaceBelow = innerHeight - anchor.bottom - GAP - EDGE
spaceAbove = anchor.top - GAP - EDGE
above      = 내용높이 > spaceBelow && spaceAbove > spaceBelow      ← "패널 높이"가 아니라 "어느 쪽이 넓은가"
maxHeight  = clamp(MIN, 열리는 쪽의 남은 자리, MAX)
```

- `useLayoutEffect` 로 첫 그림 전에 잰다(깜빡임 없음).
- `resize` + `scroll`(**capture**) 로 다시 잰다 — capture 라야 드로어 본문 같은 중간 스크롤 컨테이너가 움직일 때도 따라간다.
- 패널에 `tabIndex={-1}` — 안에 누를 것이 없는 내용(긴 글)도 키보드로 스크롤된다. `-1` 이라 탭 순서는 그대로다.
- 바깥 클릭·Esc·포커스 복귀·aria 는 손대지 않았다.

**`styles.css`** (popover 규칙 안에서만, +10줄)

- `max-height: min(60vh, 420px)` 는 **재기 전 한 프레임을 위한 대비책**으로 남겼다(인라인 값이 이긴다).
- `overflow: auto` → `overflow-y: auto; overflow-x: hidden` + **`overscroll-behavior: contain`**(휠이 뒤 페이지로 넘어가지 않는다).
- `align-content: start` — 내용이 짧을 때 grid 가 항목을 세로로 벌리지 않게.
- `.popover:focus { outline: none }` — `tabIndex=-1` 이 만든 포커스 링만 없앤다(항목 포커스 링은 그대로).
- **헤더 고정**: `.popover > .popover-head, .popover > .date-picker-head { position: sticky; top: -8px; ... }`
  — 스크롤해도 달 이동 버튼이 남는다. `.popover-head` 는 앞으로 헤더를 두는 소비처를 위한 이름이다.

소비처 코드는 **한 줄도 고치지 않았다** — 원인이 소비처에 없었다.

## 5. 검증 — 소비처 · 증상 · 수정 후

브라우저 실측(5176, 폭 1440). 「긴 내용」은 `popover-item` 을 37개로 늘려 만들었다.
`화면밖` = 패널이 뷰포트 아래/위로 삐져나간 픽셀. `끝까지` = 스크롤로 마지막 항목까지 닿는가.

| 소비처 / 시나리오 | | 위로 열림 | 패널 높이 | **화면밖(아래/위)** | 스크롤 | 끝까지 |
|---|---|---|---|---|---|---|
| 내 업무 상태 필터 · 실제 7항목 · 900 | 수정 전 | false | 256 | 0 / 0 | — | — |
| | **수정 후** | false | 256 | **0 / 0** | — | — |
| 긴 내용 · 트리거 상단 · 900 | 수정 전 | false | 420 | 0 / 0 | O | O |
| | **수정 후** | false | 420 | **0 / 0** | O | O |
| 긴 내용 · 트리거 중간(아래 좁음) · 560 | 수정 전 | false | 336 | **114 / 0** ← 잘림 | O | O |
| | **수정 후** | **true** | 284 | **0 / 0** | O | O |
| 긴 내용 · 트리거 하단 · 560 | 수정 전 | true | 336 | 0 / 0 | O | O |
| | **수정 후** | true | **420** ← 위 자리를 다 쓴다 | **0 / 0** | O | O |
| 긴 내용 · 위아래 다 좁음 · 400 | 수정 전 | false | 240 | **58 / 0** ← 잘림 | O | O |
| | **수정 후** | false | 174 | **0 / 0** | O | O |

- `overscroll-behavior-y` 는 다섯 경우 모두 `contain` 으로 계산된다.
- **DatePicker 헤더 고정**: 앱에 소비처가 없어 `styles.css` 를 그대로 실은 정적 페이지에서 확인했다 —
  `max-height 200` 에서 `scrollTop 0 → 400` 으로 굴려도 `.date-picker-head` 는 패널 상단에 붙어 있고
  (`headTopOffset 1px` = 테두리), 배경이 불투명해 내용이 비쳐 보이지 않는다.

```
npx tsc --noEmit                                            → 0 에러
npx vitest run src/Popover.test.tsx                         → 12 passed (기존 6 + 신규 6)
  + src/DatePicker.test.tsx · src/DateField.test.tsx · src/MyWorkPage.test.tsx
                                                            → 4 파일 40 passed / 40
styles.css·Popover.tsx diff 에 추가된 hex                    → 0
api.ts · viewModels.ts diff                                  → 없음(불변)
```

신규 테스트 6개: 남은 자리만큼 `max-height` 가 걸려 스크롤 컨테이너가 된다 · 아래가 모자라면 위로 열고 화면 밖으로 넘기지 않는다 ·
위아래가 다 좁으면 넓은 쪽 자리를 그대로 쓴다 · 아무리 좁아도 최소 160 은 지킨다 · 창 크기가 바뀌면 다시 잰다 · 패널이 `tabIndex=-1` 이다.
(jsdom 은 배치를 하지 않아 뷰포트 높이·트리거 자리·내용 높이 셋만 stub 하고 계산식을 검증한다.)

## 6. 변경 파일

| 파일 | 변경 |
|---|---|
| `frontend/src/Popover.tsx` | +73 / -13 — 남은 자리 측정, resize·scroll 재측정, 인라인 max-height, `tabIndex=-1` |
| `frontend/src/styles.css` | +10 / -3 — popover 블록만(overscroll-behavior · overflow 축 분리 · align-content · sticky 헤더 · focus outline) |
| `frontend/src/Popover.test.tsx` | +103 — 신규 6 케이스 + layout stub |

소비처(`MyWorkPage.tsx` · `DatePicker.tsx`) · `api.ts` · `viewModels.ts` · `backend/` · `.design-sync/` · `ds-entry.tsx` — **변경 0**. 커밋·push 없음.

## 7. 미결 · 주의점

- **상한 420 · 하한 160 · 가장자리 여유 8 은 v2 에 근거가 없는 값이다.** 420 은 기존 CSS 값을 그대로 이어받았고,
  160·8 은 내가 정했다. 디자인이 팝오버 높이 규칙을 정하면 그 세 상수만 바꾸면 된다.
- `ds-entry.tsx` 로 나가는 Popover 도 같은 규칙을 받는다. claude.ai/design 쪽 프리뷰가 `max-height` 를 다시
  덮어쓰고 있지 않은지는 디자인 동기화 담당이 한 번 봐 주면 좋겠다(`.design-sync/` 는 내 담당이 아니라 열지 않았다).
- 「팝오버들 **다**」라는 표현과 달리 실제 소비처는 둘이다. 사용자가 다른 화면에서 본 것이 있다면
  그건 Popover 가 아니라 다른 부품(Drawer 본문·`.ax-conversation-list`(max-height 148) 등)일 수 있다 — 알려 주면 그쪽을 본다.
