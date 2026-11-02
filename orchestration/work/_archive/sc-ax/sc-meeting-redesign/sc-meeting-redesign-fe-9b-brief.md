# [frontend] 바퀴 9-B — `styles.css` 를 0줄로 만들고 지운다

워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign` (커밋 `0220428` 위, 깨끗함)

## 1. 목표

**`frontend/src/styles.css` 삭제. 구 DS 흔적 0.**

바퀴 9 (가) 가 과도기 파일 넷을 없앴다. 남은 건 이 파일 하나다 — **1312줄 · 190클래스 · 501자리**
+ `input`/`select`/`textarea` 전역 규칙.

네가 보고서 §7 에 정리한 그 목록이 이 바퀴의 작업 목록이다.

## 2. 규칙 — 바퀴 9 (가) 와 같다

**「없으면 새 DS 어휘로 만든다.」** 발명이 아니라 이름 옮기기다:

- 값(색·크기·기하)은 **구 파일에 있던 것 그대로**
- 이름만 `--scax-*` / `.scax-*` / 부품으로
- 새 토큰은 `scax.css`, 새 부품 규칙은 `components.css` — (가) 에서 하던 방식 그대로
- **새 파일을 만들지 마라.** 「예외」·「과도기」·「legacy」 성격 파일은 하나도 안 남는다

`DS-gaps.md`(코디 워크트리 `…/work/sc-meeting-redesign/design/DS-gaps.md`)에서
아직 안 채운 것 — **G-05 나머지 · G-45 textarea · 네가 새로 낸 4건** — 도 여기서 닫아라.

## 3. 특히 조심할 것

| | |
|---|---|
| **`input`·`select`·`textarea` 전역 규칙** | 지우면 **앱 전체 입력칸이 벗겨진다.** 새 DS 의 폼 어휘(`.scax-textfield` 등)로 옮기되, 아직 그 클래스를 안 쓰는 자리가 있으면 **그 자리부터 옮기고** 규칙을 지워라 |
| **화면 통짜 레이아웃** | `login-*` · `graph-*` · `project-*` · `calendar-*` · `timeline-*` · `kanban-*` · `select-*` · `date-picker-*` · `meeting-*` · `org-*` · `report-*` · `discussion-*` · `metric-*` · `gutter-*` · `toast-*` · `popover-*` — **각 화면의 CSS 파일로** 보내라(`screens-a` · `screens-b` · `ax` · `meetings` · `workspace`) |
| **`t-meta` 97 · `sr-only` 21 · `center` 20** 같은 유틸 | 개수가 많다. 새 DS 에 대응이 있으면 그것으로, 없으면 `components.css` 에 유틸 구획을 만들어라 |
| **모달 골격 54자리** | `.modal`·`.modal-backdrop`·`head`·`foot`·`close` — 이미 `Modal` 부품이 있다. 부품 안으로 |

## 4. 마지막 확인 — 지우기 전에

`styles.css` 를 `rm` 하기 **전에** 이걸 해라:

1. 그 파일이 정의하는 **모든 셀렉터**를 뽑아서, `.tsx` 마크업과 다른 CSS 파일에서 **0곳인지** 확인
2. 0이 아닌 게 하나라도 있으면 **지우지 말고 보고**해라
3. 지운 뒤 `vite build` → **번들 CSS 에서** 옮긴 클래스들이 실렸는지 grep

## 5. allowed_paths

- `frontend/` — **`backend/` 는 한 줄도 안 건드린다**

## 6. 검증

```
cd frontend && npx tsc --noEmit     → 0
cd frontend && npx vitest run        → 전체
cd frontend && npx vite build        → 성공
```

> 기준선: 커밋 `0220428` 시점 **487 통과.**

**테스트는 「클래스가 있나」만 보지 「스타일이 붙었나」는 안 본다.** CSS 를 통째로 지우는 바퀴라
초록이 떠도 화면이 벗겨질 수 있다. §4 의 셀렉터 전수 확인이 그래서 필수다.

눈 확인은 **사용자가 한다.** 너는 「확인 못 함」으로 적고 넘어가라 — 그게 정직한 보고다.

## 7. ★ `git stash` 를 쓰지 마라

지난 바퀴에서 맨몸 `git stash` 를 한 번 실행했다(되살렸지만). 이 워크트리의 stash 스택은
**다른 세션과 공유**된다 — 남의 작업을 날릴 수 있다. 작업을 잠시 치워야 하면 **임시 커밋**을 써라.

## 8. 보고

- **`styles.css` 를 지웠는지** — 못 지웠으면 무엇이 남아서인지 전수
- 옮긴 것을 **어느 파일로 보냈는지** 묶음별로
- 채운 `DS-gaps` 번호 · 못 채운 것과 이유
- `tsc` · `vitest` · `vite build`
- **번들 CSS grep 결과**
- 새 파일을 만들었다면 그것과 이유(원칙은 「만들지 마라」)
