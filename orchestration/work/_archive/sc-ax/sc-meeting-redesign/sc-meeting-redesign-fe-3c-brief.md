# [frontend] 바퀴 3c — 구 CSS 클래스를 새 DS 부품으로 이관한다

너는 **sc-ax `frontend` 워커**다. 바퀴 1·2·3a 를 네가 했으면 그 맥락 그대로다.

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign` (바퀴 3a 커밋 `fbe5801` 위)
base `origin/main` → PR `main` (PR 은 코디가 올린다)

## 1. 이 바퀴가 무엇인가

바퀴 10개 중 **③c** 다. ①토큰 ②셸 ③a표시프리미티브(전부 완료) → **③c 클래스 이관** → ③b 폼·오버레이 → ④아이콘 → ⑤업무화면 → ⑥회의화면 → ⑦AX드로어 → ⑧남은7장 → ⑨은퇴.

바퀴 3a 에서 **부품 7종을 만들었는데 소비처가 0** 이다. 우리 앱에서 그것들은 React 부품이 아니라
**맨 CSS 클래스**로 호출부마다 인라인으로 박혀 있었기 때문이다. 이 바퀴가 그 연결을 잇는다.

**이 바퀴 하나로 시안 없는 화면 10장이 새 DS 가 된다.** 그게 「DS 가 화면보다 먼저」의 결말이다.

**범위 (코디 실측, 2026-09-13)**

| 구 클래스 | 사용처 | 갈 곳 |
|---|---:|---|
| `.btn` (+`.primary`·`.link`·`.ghost`·`.sm` 등 변형) | **225** (35파일) | `src/Button.tsx` 의 `Button` · `ButtonGroup` · `IconButton` |
| `.badge` (+ tone 변형) | **33** | `src/Badge.tsx` |
| `.chip` | **18** | `src/Chip.tsx` · `ChipBar` |
| `.page-tabs` | **1** | `src/SegmentedControl.tsx` 의 `Tabs` |

합 **277곳**. 테스트 제외 프로덕션 기준이다.

## 2. 먼저 할 일 — 매핑표를 만들고 **승인을 받아라** (게이트)

277곳을 고친 뒤에 매핑이 틀렸다고 판명되면 되돌릴 방법이 없다. **이관 전에 표부터 만든다.**

1. `.btn` 의 **실제로 쓰이는 변형 조합 전수**를 세라 (`.btn` 단독 / `.btn.primary` / `.btn.link` / `.btn.ghost` / `.btn.sm` / 조합 …). 조합마다 **건수**를 적는다.
2. 각 조합 → `Button` 의 `variant` / `tone` / `size` **매핑 제안**. 아이콘만 있는 버튼은 `IconButton`, 붙어 있는 버튼 묶음은 `ButtonGroup`.
3. `.badge` · `.chip` 도 같은 꼴로.
4. **대응이 없는 조합**은 별도로 모아라 — 억지로 끼워 맞추지 마라.
5. 테스트가 구 클래스에 묶인 곳(`querySelector`·`toHaveClass`·`className`) 건수.

표가 되면 **`decision_gate` 로 코디에게 보내고 답을 기다려라.** 답이 오면 그때 이관한다.

> **런타임이 끊겨 답을 못 받으면**: 그때는 **건수가 가장 많은 조합(대개 `.btn` 단독·`.btn.primary`)만 빼고** 나머지를 먼저 이관하고, 큰 것은 남긴 채 보고해라. 되돌릴 양을 작게 유지하는 쪽으로 판단한다.

## 3. SSOT (전부 read-only)

- `frontend/src/Button.tsx` · `Badge.tsx` · `Chip.tsx` · `SegmentedControl.tsx` — 바퀴 3a 가 만든 **부품 정본**
- `frontend/src/styles/components.css` — 새 클래스(`.scax-btn*` 등)의 스타일 정본
- `…/design/handoff/my-work/js/my-work.v2.jsx` · `…/handoff/shell/js/scax-ui.jsx` — 시안이 부품을 **어떻게 부르는지**의 용례
- `…/design/guidelines/*.card.html` — 판단이 갈리면 여기가 기준
- `frontend/src/styles.css` — 구 `.btn`·`.badge`·`.chip` 정의(지울 대상)

## 4. 결정 (재논의 금지)

| # | 결정 |
|---|---|
| **E-1** | **레이아웃을 바꾸지 마라.** 이 바퀴는 「같은 자리의 같은 것」을 새 부품으로 부르는 것뿐이다. 버튼이 서는 자리·순서·개수는 그대로다. 화면 재설계는 바퀴 5·6 |
| **E-2** | **동작을 바꾸지 마라.** `onClick`·`disabled`·`type`·`aria-*`·`title` 을 전부 옮겨라. 특히 **접근성 이름이 사라지면 테스트가 조용히 통과하면서 화면이 망가진다** |
| **E-3** | 부품에 없는 prop 이 필요하면 **부품을 넓혀라**(호출부를 비틀지 말고). 넓힌 것은 전건 보고 |
| **E-4** | **기능을 지우지 마라.** 새 부품으로 표현이 안 되는 버튼이 있으면 **구 클래스인 채로 남기고 보고**해라. 억지 이관 금지 |
| **E-5** | 이관이 끝난 클래스만 구 `styles.css` 에서 지운다. 한 곳이라도 남아 있으면 지우지 마라. 지운 자리에 사유 주석 |
| **E-6** | 아이콘 이름은 **지금 있는 것**을 쓴다. 없는 글리프가 필요하면 만들지 말고 보고(바퀴 4 입력) |
| **E-7** | **가짜 라벨·가짜 데이터 금지.** 핸드오프 용례의 문구를 우리 화면에 옮기지 마라 — 우리 문구를 그대로 쓴다 |

## 5. allowed_paths

- `frontend/`

**`backend/` 는 한 줄도 안 건드린다. 읽는 것까지만이고 고치자는 제안도 쓰지 마라.**

## 6. 검증

```
cd frontend && npx tsc --noEmit     → 0 에러
cd frontend && npx vitest run        → 전체 1회 (이 바퀴도 예외 허용)
```

> 기준선: 바퀴 3a 시점 `41 files · 468 tests` 전부 통과. `ActionCenter.test.tsx` · `Checklist.test.tsx` 에 flaky 각 1건 관측(단독 반복 통과) — **네가 깬 게 아니다.**

깨진 테스트는 **이관이 원인인 것만** 고쳐라. 구 클래스 선택자를 새 이름으로 바꾸는 건 맞다.
**단, 접근성 질의(`getByRole`·`getByLabelText`)가 깨졌다면 그건 테스트가 아니라 네 이관이 틀린 것이다** — 테스트를 고치지 말고 코드를 고쳐라.

자기점검:
- `backend/` 가 diff 에 **안 나오는가**
- 남은 구 클래스 사용처가 **0인가** (아니면 어느 것이 왜 남았는가)
- `onClick`·`disabled`·`aria-*`·`title` 을 **빠뜨린 곳이 없는가**
- 넓힌 prop 이 있으면 **전건 적었는가**

## 7. 보고

코디(`term_18011a51-e9ec-4cad-9370-1836d3ee8d2d`)에게:

- **승인받은 매핑표대로 갔는지**, 벗어난 곳이 있으면 그것과 이유
- 이관 건수 (`.btn` N / `.badge` N / `.chip` N / `.page-tabs` N) · **남긴 곳과 이유**
- `tsc` · **vitest passed/failed** · 고친 테스트 수
- 구 `styles.css` 에서 지운 줄 수
- 넓힌 prop 전건
- 아이콘이 모자라 못 그린 자리 (바퀴 4 입력)
- 막혀서 못 한 것
