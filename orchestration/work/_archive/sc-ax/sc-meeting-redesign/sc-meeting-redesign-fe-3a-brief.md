# [frontend] 바퀴 3a — 표시 프리미티브를 새 DS 로 갈아끼운다

너는 **sc-ax `frontend` 워커**다. 바퀴 1·2 를 네가 했으면 그 맥락 그대로다.

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign` (바퀴 2 커밋 `c7a7005` 위)
base `origin/main` → PR `main` (PR 은 코디가 올린다)

## 1. 이 바퀴가 무엇인가

바퀴 9개 중 **③의 앞쪽**이다. ①토큰 ②셸(완료) → **③a 표시 프리미티브** → ③b 폼·오버레이 → ④아이콘 → ⑤업무화면 → ⑥회의화면 → ⑦AX드로어 → ⑧남은7장 → ⑨은퇴.

**여기서 시안 없는 화면 10장이 따라온다.** 화면을 다시 그리는 게 아니라, 그 화면들이 쓰는 **공용 어휘**를 새 것으로 갈면 저절로 새 DS 가 된다. 그게 「DS 가 화면보다 먼저」인 이유다.

③을 a/b 로 나눈 이유: 부품 30종을 한 번에 갈면 검증이 안 된다. **a 는 표시(읽기) 부품**, b 는 폼·오버레이(쓰기) 부품이다.

## 2. SSOT — 먼저 읽을 것 (전부 read-only)

코디 워크트리 `…/work/sc-meeting-redesign/design/` 아래:

- **`handoff/shell/js/scax-ui.jsx`** — 이번에 옮길 부품의 **구현 정본**. `Button`(25줄) `ButtonGroup`(37) `IconButton`(41) `Badge`(52) `Popover`(59) `SegmentedControl`(111) `Tabs`(131) `Chip`(151) `GutterList`(160) `Empty`(176) `StatusNote`(186) `Skeleton`(197) `AgentBubble`(233)
- **`handoff/my-work/css/components.css`**(38KB) — 위 부품들의 **스타일 정본**
- `ds-token-report.md` **§9**(598~658줄) — 우리 부품 ↔ 새 DS 대응표
- `DS-gaps.md` — **새 DS 에 없는 것 24건.** 여기 올라 있는 것은 §3 D-3 대로 손대지 않는다
- `guidelines/*.card.html` — 색·타입·간격 규약. 판단이 갈리면 여기가 기준

현 앱: `src/Popover.tsx` · `src/Empty.tsx` · `src/Skeleton.tsx` · `src/StatusNote.tsx` · `src/ProgressBar.tsx` · `src/Icon.tsx` · `src/styles.css`

## 3. 결정 (코디가 정했다 — 재논의 금지)

| # | 결정 |
|---|---|
| **D-1** | **핸드오프 JSX/CSS 가 구현 정본이다.** `design/components/**` 의 190여 개는 Figma variant 를 굳힌 정적 렌더러라 쓸 수 없다(데이터도 콜백도 안 받는다). 거기서 베끼지 마라 |
| **D-2** | **기존 구조를 따른다.** `src/Button.tsx` 처럼 `src/` 바로 아래. **새 폴더 체계를 만들지 마라.** 이미 있는 파일(`Popover.tsx`·`Empty.tsx`·`Skeleton.tsx`·`StatusNote.tsx`)은 **그 파일 안에서** 내용을 갈아끼운다 — 새 파일을 옆에 만들지 마라 |
| **D-3** | **`DS-gaps.md` 에 오른 것은 손대지 마라.** 이 바퀴 범위에선 `ProgressBar`(G-04) · `EmptyValue`(G-07) 가 해당한다. 새 DS 에 대응이 없어서 사용자 컨펌 대기 중이다. **구 부품을 그대로 둔다** |
| **D-4** | **props 는 우리 것을 지킨다.** 핸드오프의 props 가 우리와 다르면 **우리 호출부를 고치지 말고** 부품 안에서 맞춰라. 소비처가 수십 곳이라 시그니처를 바꾸면 이 바퀴가 화면 바퀴가 된다 |
| **D-5** | **샘플 데이터를 옮기지 마라.** 핸드오프 파일에 `TASK_MODAL_PEOPLE = ['홍길동','박민수','유하람']` 같은 상수가 박혀 있다. **가짜 이름·가짜 파일·가짜 계정은 한 줄도 들어오면 안 된다** |
| **D-6** | 교체한 부품이 쓰던 **구 `styles.css` 구획만** 지운다. 안 판 것은 남긴다. 지운 자리에 사유 주석 한 줄 |
| **D-7** | `AgentBubble` 은 AX 어시스턴트 말풍선이다 — **바퀴 7**(AX 드로어)에서 다룬다. 이번엔 파일만 보고 넘어가라 |
| **D-8** | 아이콘 이름 매핑은 **바퀴 4** 다. 부품이 아이콘을 쓰면 **지금 있는 이름**으로 부르고, 없는 글리프가 필요하면 만들지 말고 보고해라 |

## 4. 구현 단계

1. §2 의 두 정본을 읽고, **부품 13종 각각에 대해 현 앱의 대응을 먼저 표로 정리**해라(있음/없음/이름 다름). 이 표를 보고서에 넣는다.
2. CSS 를 `src/styles/components.css` 로 싣고 `src/styles/index.css` 에 `@import` 추가. **전역 element 규칙이 있으면 바퀴 1·2 와 같은 방식으로 잘라내고 사유를 남긴다.**
3. 부품을 옮긴다(TSX). 있는 파일은 안에서 교체, 없는 것만 새 파일.
4. 소비처가 새 부품으로 도는지 확인하고, 깨진 테스트를 고친다.
5. D-6 으로 구 `styles.css` 구획 정리.

## 5. allowed_paths

- `frontend/`

**`backend/` 는 한 줄도 안 건드린다. 읽는 것까지만이고 고치자는 제안도 쓰지 마라.**

## 6. 검증

```
cd frontend && npx tsc --noEmit     → 0 에러
cd frontend && npx vitest run        → 전체 1회 (이 바퀴도 예외 허용)
```

**전체를 1회 도는 이유**: 공용 부품은 소비처가 전 화면에 퍼져 있어 부분 테스트로 회귀를 못 잡는다. 코디가 허용한다.

> 기준선: 바퀴 2 시점 `41 files · 468 tests` 전부 통과. `src/Checklist.test.tsx` · `src/ActionCenter.test.tsx` 에 flaky 각 1건이 관측됐다(단독 반복에선 통과) — **네가 깬 게 아니다.** 판단이 서면 보고만 하고 넘어가라.

깨진 테스트는 **부품 교체가 원인인 것만** 고쳐라. `querySelector`·`toHaveClass` 로 구 클래스에 묶인 테스트는 새 클래스로 고치는 게 맞다. 원인이 다른 데 있으면 고치지 말고 보고.

자기점검:
- `backend/` 가 diff 에 **안 나오는가**
- **가짜 데이터가 한 줄도 안 들어왔는가**(D-5)
- 부품 **props 시그니처를 안 바꿨는가**(D-4) — 바꿨으면 그 부품과 이유를 보고
- `DS-gaps.md` 항목을 **안 건드렸는가**(D-3)
- 새 폴더를 **안 만들었는가**(D-2)

## 7. 하지 말 것

- 화면 레이아웃을 바꾸지 마라. 바퀴 5·6 이다.
- 시안에 없다는 이유로 기능·부품을 지우지 마라. 남기고 보고해라.
- 커밋·push 하지 마라.
- 대응이 애매한 부품을 **억지로 갈지 마라.** 애매하면 남기고 보고하는 쪽이 옳다.

## 8. 보고

코디(`term_18011a51-e9ec-4cad-9370-1836d3ee8d2d`)에게:

- **부품 13종 대응표** — 갈았다 / 안 갈았다(이유) / 우리에 없어서 새로 만들었다
- `tsc` · **vitest passed/failed** — 고친 테스트 수와 그 이유
- 구 `styles.css` 에서 지운 줄 수
- **props 를 바꾼 부품이 있으면 전건**
- 아이콘이 모자라 못 그린 자리(바퀴 4 입력)
- 막혀서 못 한 것
