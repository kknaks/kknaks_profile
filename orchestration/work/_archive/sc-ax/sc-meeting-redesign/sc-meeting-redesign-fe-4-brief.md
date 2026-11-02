# [frontend] 바퀴 4 — 아이콘 세트를 새 DS 로 통합

너는 **sc-ax `frontend` 워커**다. 바퀴 1·2·3a·3c·3b 를 네가 했으면 그 맥락 그대로다.

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign` (바퀴 3b 커밋 `4b7ae91` 위)
base `origin/main` → PR `main` (PR 은 코디가 올린다)

## 1. 이 바퀴가 무엇인가

바퀴 10개 중 **④** — 프리미티브의 마지막이다. 여기까지가 「DS 가 화면보다 먼저」의 끝이고,
다음부터(⑤⑥⑦⑧)는 화면이다.

**지금 `src/Icon.tsx` 안에 그리드 두 벌이 섞여 있다.** 바퀴 2 가 셸이 요구한 24그리드 글리프
6종(`persons`·`square-check`·`document`·`business-bag`·`company`·`left-side`)을 더하면서
16그리드 표와 분리해 뒀고, **「바퀴 4 에서 한 벌로 합친다」고 적어 뒀다.** 그게 이 바퀴다.

## 2. SSOT — 먼저 읽을 것 (전부 read-only)

코디 워크트리 `…/work/sc-meeting-redesign/design/` 아래:

- **`components/icon/icon-data.js`** · **`icon-aliases.js`** — **글리프 정본.** 이 두 파일이 이 바퀴의 전부다
- `components/icon/Icon.jsx` · `Icon.d.ts` — DS 의 부르는 법
- `DS-gaps.md` **G-03 · G-03b** — DS 에 **없는 10종**
- `ds-token-report.md` §9 의 `Icon` 행 — 이름 매핑 초안

현 앱: `src/Icon.tsx` (16그리드 표 + 바퀴 2 가 더한 24그리드 6종)

## 3. 결정 (재논의 금지)

| # | 결정 |
|---|---|
| **H-1** | **DS 세트를 통째로 싣지 마라.** 120 글리프 · 167KB 인데 우리가 쓰는 건 30여 종이다. **실제 쓰는 것만** 가져와라. 이름은 **DS 이름**을 쓴다 |
| **H-2** | **이름은 DS 쪽으로 맞춘다.** 리포트가 준 매핑: `check-square`→`square-check` · `file`→`document` · `refresh`→`reset` · `alert`→`circle-exclamation` · `filter`→`tune` · `list`→`align-justify` 또는 `list-category`. **네가 `icon-data.js` 를 열어 확인하고**, 초안과 다르면 파일 쪽을 따르고 보고해라 |
| **H-3** | **DS 에 없는 살아 있는 5종**(`paperclip` 4 · `arrow-up` 2 · `arrow-down` 2 · `sparkle` 2 · `folder` 2 = 12곳)은 **구 16그리드 path 를 그대로 둔다.** 24그리드로 **다시 그리지 마라 — 발명 금지**(G-03). viewBox 분기는 바퀴 2 가 이미 만들어 놨다. 다만 **굵기·크기가 옆 글리프와 달라 보일 수 있다** — 눈에 띄면 보고해라 |
| **H-4** | **죽은 5종**(`square`·`circle`·`ban`·`pending`·`empty`, 사용처 0)은 **지우지 마라.** G-03b 의 「폐기」는 **제안일 뿐 사용자 컨펌 전**이다. 바퀴 9 몫 |
| **H-5** | **`sparkle` 을 DS 의 `agent`/`ai-review` 로 바꾸지 마라.** 디자이너 확인 대상이다(G-03). 지금은 구 글리프 유지 |
| **H-6** | **`Icon` 의 props 시그니처를 지켜라** — `name`·`size`(12·14·16·20)·`className`·`title`. 소비처가 전 화면에 퍼져 있다. 크기 규칙(16·20 은 stroke 1.5, 14 이하 1.3)도 유지 |
| **H-7** | 그리드가 한 벌로 합쳐지면 **바퀴 2 가 남긴 분리 주석과 `Grid24Name` 타입을 정리해라.** 남길 이유가 있으면(H-3 의 5종) 그 이유로 다시 적어라 |

## 4. allowed_paths

- `frontend/`

**`backend/` 는 한 줄도 안 건드린다. 읽는 것까지만이고 고치자는 제안도 쓰지 마라.**

## 5. 검증

```
cd frontend && npx tsc --noEmit     → 0 에러
cd frontend && npx vitest run        → 전체 1회 (이 바퀴도 예외 허용)
```

> 기준선: 바퀴 3b 시점 `42 files · 469 tests` 전부 통과(3회 연속).

**아이콘은 이름이 바뀌면 타입이 잡아준다** — 그게 이 바퀴가 앞바퀴들보다 안전한 이유다.
`tsc` 가 0 이면 이름 누락은 없다. 대신 **타입이 못 잡는 것**을 따로 봐라:

- `title` 이 사라진 곳 (접근성 이름이 있던 아이콘이 장식으로 바뀌면 조용히 읽히지 않는다)
- `size` 가 바뀐 곳 (같은 줄의 글리프끼리 크기가 어긋난다)
- **글리프 하나가 다른 뜻으로 매핑된 곳** — 예: `list`→`align-justify` 와 `list-category` 중
  어느 쪽이 맞는지는 **그 아이콘이 서 있는 자리**가 정한다. 기계적으로 고르지 마라

자기점검:
- `backend/` 가 diff 에 **안 나오는가**
- **쓰지 않는 글리프를 끌고 오지 않았는가**(H-1) — 최종 글리프 수와 파일 크기를 보고
- H-3 의 5종을 **다시 그리지 않았는가**
- H-4 의 5종을 **안 지웠는가**
- `Icon` props 시그니처가 **그대로인가**

## 6. 보고

코디(`term_18011a51-e9ec-4cad-9370-1836d3ee8d2d`)에게:

- **이름 매핑 전수표** — 구 이름 → 새 이름 (또는 「그대로」·「없어서 구 path 유지」)
- 최종 글리프 수 · `Icon.tsx` 크기 (before/after)
- 리포트 초안과 **달랐던 매핑**과 그 근거
- `title`·`size` 가 바뀐 곳
- 굵기·크기가 옆 글리프와 어긋나 보이는 자리 (H-3 부작용)
- `tsc` · **vitest passed/failed** · 고친 테스트 수
- 막혀서 못 한 것
