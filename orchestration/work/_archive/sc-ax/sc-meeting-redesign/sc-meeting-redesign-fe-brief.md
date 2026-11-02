# [frontend] 바퀴 1 — 새 DS 토큰을 앱에 싣는다

너는 **sc-ax `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/roles/sc-ax/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리는 너 혼자 쓴다. 다만 **코디 워크트리의 `design/` 폴더에 다른 워커가 파일을 계속 쓰고 있다** — 거기는 read-only 로만 봐라.

## 1. 배경 — 어디쯤인가

디자이너가 새 디자인 시스템(`TheSC AX Design System`)을 세웠고, **목표는 구 DS 의 은퇴**다.
전체는 **바퀴 9개**로 간다: **① 토큰** → ② 셸 → ③ 프리미티브 → ④ 아이콘 → ⑤ 업무화면 → ⑥ 회의화면 → ⑦ AX드로어 → ⑧ 남은 7장 → ⑨ 은퇴.

**너는 바퀴 1 이다.** 다음 여덟 바퀴가 참조할 토큰을 깔아 두는 것뿐이고, **화면은 하나도 안 바뀐다.**
아직 아무 코드도 `--scax-*` 를 참조하지 않으므로 이 바퀴에서 깨질 테스트는 **0건**이어야 한다. 그게 검증 기준이다.

## 2. SSOT — 먼저 읽을 것 (전부 read-only)

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-redesign/design/ds-token-report.md`
  - **§3 충돌표**(365~409줄) · **§4 판정**(410~424줄) · **§5 폰트**(425~441줄) ← 이 바퀴의 근거 전부
- `…/design/tokens/` — 실을 원본 7벌 (`fig-tokens.css` · `product.css` · `scax.css` · `typography.css` · `fig-typography.css` · `scrollbar.css` · `fonts.css`)
- 현 앱: `frontend/src/styles.css` · `frontend/src/main.tsx` · `frontend/index.html`

리포트의 숫자를 **믿지 말고 한 번 확인해라** — 토큰 이름 교집합이 정말 0인지 네 손으로 세라. 다르면 멈추고 보고한다.

## 3. 결정 (코디가 정했다 — 이대로 간다, 재논의 금지)

| # | 결정 |
|---|---|
| D1 | **스코프 격리 안 한다.** 토큰 이름이 안 겹치므로(새 569 : 구 65, 교집합 0) `:root` 에 그대로 얹는다 |
| D2 | **전역 element 규칙만 잘라낸다.** `product.css` 의 `a` · `a:hover` 규칙을 **지우고** 싣는다. 구 `styles.css` 의 링크 색이 이겨야 한다 |
| D3 | **`scrollbar.css` 는 싣지 않는다.** `*{scrollbar-width:none}` 이 앱 전체에서 스크롤 막대를 없앤다 — 구 화면은 막대가 보이는 전제로 그려졌다. 바퀴 8 까지 보류. 파일은 옮겨 두되 `index.css` 에서 `@import` 하지 않고 **주석으로 이유를 남긴다** |
| D4 | **폰트는 로컬 동봉.** `fonts.css` 의 jsDelivr 원격 URL 을 쓰지 않는다 — 사내망·오프라인에서 글꼴이 깨진다. woff2 2벌을 받아 `frontend/public/fonts/` 에 두고 `src:url("/fonts/…")` 로 바꾼다 (Pretendard = OFL, 동봉 가능) |
| D5 | **글꼴 가족은 DS 값 그대로** — `--font-ui: "Pretendard JP"` 를 고치지 마라. DS 가 정본이다 |
| D6 | **구 `frontend/src/styles.css` 는 한 줄도 건드리지 않는다.** 바퀴 9 에서 통째로 지운다. 지금은 둘이 같이 실린다 |
| D7 | 새 자리는 `frontend/src/styles/` — DS 토큰 원본을 그대로 두고 `index.css` 한 벌이 `@import` 로 묶는다. `main.tsx` 가 구 `styles.css` **다음에** 이 한 줄을 더 import 한다 |

## 4. 구현 단계

1. `frontend/src/styles/` 를 만들고 `design/tokens/` 의 **6벌**(`scrollbar.css` 포함해 7벌 다 복사하되 §D3 대로 `scrollbar.css` 는 import 하지 않는다)을 복사해 넣는다. **내용을 다시 쓰지 마라 — 복사다.** 손대는 곳은 D2(`product.css` 의 `a` 2규칙 삭제)와 D4(`fonts.css` 의 url) **둘뿐**이고, 지운 자리엔 `/* 바퀴 1: … 이유 */` 주석을 남긴다.
2. 폰트 woff2 2벌을 받아 `frontend/public/fonts/` 에 둔다 — `PretendardJPVariable.woff2` · `PretendardVariable.woff2` (`fonts.css` 의 원래 URL 이 출처다). 받은 파일 크기를 보고에 적는다.
3. `frontend/src/styles/index.css` 를 쓴다 — `@import` 목록 + 각 줄에 그 파일이 무엇인지 한 줄 주석 + `scrollbar.css` 를 왜 뺐는지.
4. `frontend/src/main.tsx` 에 import 한 줄 추가 (**구 `styles.css` 다음**).
5. 확인 — 개발 서버를 띄우지 말고, `npx tsc --noEmit` 과 vitest 로만 본다(§6).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `frontend/`

**`backend/` 는 한 줄도 건드리지 않는다. 읽는 것까지만이고, 고치자는 제안도 쓰지 마라.** 백엔드는 다음 태스크다.

## 6. 검증 — 이 바퀴의 합격선

```
cd frontend && npx tsc --noEmit          → 네가 만진 파일 0 에러
cd frontend && npx vitest run             → 이 바퀴는 예외적으로 전체를 1회 돌린다
```

**이 바퀴는 「전체 스위트 1회」가 허용된다.** 이유: 토큰만 얹었으므로 **테스트는 이전과 똑같이 통과해야 한다**(기준선 확보). 하나라도 새로 깨지면 그건 D1~D3 중 뭔가가 새는 것이다 — 고치지 말고 **어느 테스트가 왜 깨졌는지 보고**해라.

자기점검:
- 구 `styles.css` 가 `git diff` 에 **안 나오는가** (D6)
- `design/` 폴더(코디 워크트리)를 **안 고쳤는가**
- `tokens/*.css` 를 복사하면서 **값을 다시 타이핑하지 않았는가** — diff 로 원본과 대조해라
- `a`/`a:hover` 삭제 말고 **다른 element 규칙을 더 지우지 않았는가**

## 7. 하지 말 것

- 화면·컴포넌트를 고치지 마라. 이 바퀴는 **CSS 를 싣는 것뿐**이다.
- `--scax-*` 를 어디에도 **쓰지 마라**. 참조는 바퀴 2 부터다.
- 구 토큰을 새 것으로 바꾸지 마라. 둘은 같이 산다.
- 커밋·push 하지 마라. 코디가 검증하고 커밋한다.
- **새 폴더 체계를 발명하지 마라.** 만드는 건 `src/styles/` 하나뿐이다.

## 8. 보고

코디(`term_18011a51-e9ec-4cad-9370-1836d3ee8d2d`)에게:

- 네가 직접 센 **토큰 이름 교집합 수** (리포트는 0이라고 했다 — 맞나)
- 만든 파일 목록 + 폰트 woff2 2벌의 바이트
- `tsc` 결과 · **vitest 전체 결과 (passed/failed 수)** — 실패가 있으면 파일명과 사유
- D2·D3·D4 로 원본에서 손댄 자리 (파일:줄, 정확히 몇 줄)
- 막혀서 못 한 것이 있으면 그것
