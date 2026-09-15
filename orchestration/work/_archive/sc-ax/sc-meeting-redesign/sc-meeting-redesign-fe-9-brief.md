# [frontend] 바퀴 9 — 구 DS 를 완전히 없앤다 (흔적 0)

너는 **sc-ax `frontend` 워커**다. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign`
(branch `kknaksss/sc-meeting-redesign`, 커밋 `3f740b9` 위, 워크트리 깨끗함)

## 1. 목표 — 이것 하나다

**구 디자인 시스템의 흔적을 코드에서 0으로 만든다.**

지금까지 아홉 바퀴는 「화면이 안 바뀌게」를 우선해서, 구 규칙을 못 지우고 **옆에 새 걸 얹고
얹은 걸 또 다른 파일로 빼는** 식으로 왔다. 그래서 과도기 파일이 쌓였다. **이 바퀴가 그걸 전부 걷어낸다.**

**사라져야 하는 파일 5개 (합 1706줄)**

```
frontend/src/styles.css                      1340줄
frontend/src/styles/overrides-transitional.css  73줄
frontend/src/styles/avatar.css                  37줄
frontend/src/styles/action-cards.css           202줄
frontend/src/styles/shared-blocks.css           54줄
```

**끝나면 `frontend/src/styles/` 에 남는 것은 두 층뿐이다**

- **DS 원본 복사본** — `fonts` · `fig-tokens` · `fig-typography` · `typography` · `product` · `scax` · `scrollbar` · `shell` · `components` · `workspace`
- **우리 화면 CSS** — `meetings` · `screens-a` · `screens-b` · `ax` · `index`

「예외」·「과도기」·「legacy」 성격의 파일은 **하나도 남기지 마라.**

## 2. 남은 구 클래스 — 마크업 124곳 (코디 실측)

| 클래스 | 곳 | 가는 곳 |
|---|---:|---|
| `.field` | **56** | 새 DS 폼 어휘(`.scax-field` + `.scax-textfield`). 바퀴 8-A 가 이미 세 자리를 그렇게 옮겼다 — **그 방식을 그대로** |
| `.btn`(주로 `.link`) | 22 | `Button` 에 **인라인 텍스트 변형**을 더해 흡수 |
| `.badge`(주로 `outline`) | 15 | `Badge` 에 **outline 톤**을 더해 흡수 |
| `.chip` | 15 | `Chip`·`ChipBar` |
| `.avatar` | 11 | **`Avatar` 부품 신설** — 이니셜 원 + 크기 5단(xs~xl) |
| `.plain-table` | 5 | **`DataTable` 부품 신설** — 열 수에 안 묶인 읽기 표 |

**구 토큰 참조는 이미 0이다.** `--text-primary`·`--graph-*`·`--ai-*`·`--progress-*` 는 `styles.css`
안에서만 정의돼 있고 다른 파일은 아무도 안 본다. 다만 **`GraphCanvas` 는 예외** — §4 를 봐라.

## 3. 결정 — 「없으면 만든다」

지금까지는 **「새 DS 에 없으면 발명 금지, 구 것 두고 `DS-gaps` 에 올려라」**였다.
그건 워커 넷이 병렬로 돌 때 서로 다른 짝퉁을 만들지 않게 하려던 **임시 조치**다. 이제 끝났다.

**이 바퀴의 규칙: 새 DS 에 없으면 네가 새 DS 어휘로 만든다.**

- 값은 **이미 우리 코드에 있다.** 구 `styles.css` 의 값을 그대로 쓰고 **이름만** `--scax-*` / `.scax-*` 로
- 기하·색을 **새로 디자인하지 마라.** 옮기는 것이지 만드는 것이 아니다
- 새 토큰은 **`scax.css` 에** 넣어라 (별도 파일 만들지 마라)
- 새 부품은 `src/` 바로 아래 (`Avatar.tsx` · `DataTable.tsx`)

**`DS-gaps.md` 46건이 그 목록이다.** 코디 워크트리 `…/work/sc-meeting-redesign/design/DS-gaps.md`.
「DS 에 없다」고 적힌 것을 **전부 채워라.** 채운 것은 보고해라 — 그게 다음 단계(`/design-sync` 로
Claude Design 에 올려 DS 자체를 갱신)의 입력이다.

## 4. ★ 유일하게 위험한 곳 — `--graph-*`

`GraphCanvas.tsx:29~36`·`54`·`105~107` 이 `getComputedStyle` 로 **런타임에 CSS 변수를 읽는다.**
이름을 바꾸면 **테스트는 통과하는데 화면에서 색만 사라진다.**

- `--graph-*` 14종을 `--scax-graph-*` 로 옮기려면 **`GraphCanvas.tsx` 의 읽는 쪽도 같이** 고쳐라
- 고친 뒤 **관계 탐색 화면을 실제로 띄워 색이 나오는지 확인**해라. 테스트로는 못 잡는다

## 5. 순서 (권장)

1. `Avatar` · `DataTable` 부품 신설 → `.avatar` 11 · `.plain-table` 5 이관
2. `Button` 인라인 텍스트 변형 · `Badge` outline 톤 추가 → `.btn` 22 · `.badge` 15 이관
3. `.chip` 15 · `.field` 56 이관
4. 구 토큰을 `scax.css` 로 승격 (`--graph-*` 는 §4 대로)
5. `action-cards.css` · `shared-blocks.css` · `avatar.css` 를 화면 CSS 로 흡수
6. `overrides-transitional.css` 의 남은 규칙을 각 화면 CSS 로
7. **파일 5개 삭제** · `index.css` 정리
8. 검증

## 6. allowed_paths

- `frontend/`

**`backend/` 는 한 줄도 안 건드린다.**

## 7. 검증 — 이 바퀴는 눈으로도 봐야 한다

```
cd frontend && npx tsc --noEmit     → 0 에러
cd frontend && npx vitest run        → 전체
cd frontend && npx vite build        → 성공
```

> 기준선: 커밋 `3f740b9` 시점 **486 통과.** 먼저 돌려 확인하고 시작해라.

**테스트는 「클래스가 있는지」만 보지 「그 클래스에 스타일이 붙었는지」는 안 본다.**
그래서 CSS 를 지우는 이 바퀴는 초록이 떠도 화면이 벗겨질 수 있다.

- **`styles.css` 를 지우기 전에** `grep` 으로 그 파일의 모든 셀렉터가 마크업에서 0곳인지 확인해라
- 지운 뒤 **`npm run dev` 로 띄워서 13화면을 눈으로 확인**해라.
  특히 **관계 탐색**(§4) · **조직**(아바타 12곳) · **AX 드로어**(가장 컸다)
- 확신이 안 서는 화면은 **「확인 못 함」으로 적어라. 됐다고 쓰지 마라**

## 8. 보고

- **삭제한 파일 5개** — 각각 몇 줄이었고 어디로 갔는지
- **신설한 부품·토큰 전수** — `DS-gaps` 몇 번을 채웠는지 번호로
- **채우지 못한 gaps 가 있으면 그것과 이유**
- 남은 구 클래스·구 토큰 **grep 결과 0인지**
- `tsc` · `vitest` · `vite build`
- **13화면 눈 확인 결과** (된다 / 안 된다 / 확인 못 함)
