# [frontend] 바퀴 12 — `origin/main` 을 따라잡는다 (머지 충돌 해소)

워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign`
**지금 머지 충돌 상태다.** 코디가 `git merge origin/main` 을 실행해 두었다. 네가 마저 푼다.

## 1. 상황

우리 브랜치는 `0a8a04b` 에서 갈라져 바퀴 1~11 로 **디자인 시스템을 통째로 갈았다**.
그 사이 `origin/main` 이 `94ec26d` 까지 앞서갔고, **frontend 49파일 1845줄**이 들어왔다.

부딪히는 이유가 둘이다:
- **우리가 파일을 옮겼다**(바퀴 10 이 `src/` 를 도메인 구조로) — main 은 옛 평면 위치에 새 파일을 넣었다
- **우리가 CSS 를 갈아엎었다** — main 은 구 `styles.css` 를 고쳤는데 우리는 지웠다

## 2. 원칙 — 이것만 지키면 된다

| # | 원칙 |
|---|---|
| **M-1** | **양쪽을 다 살린다.** main 의 새 기능도, 우리의 DS 교체도 둘 다 결과에 있어야 한다. 어느 한쪽을 버리는 해소는 오답이다 |
| **M-2** | **구조는 우리 것.** main 이 `src/` 평면에 넣은 새 파일은 **우리 도메인 구조로 옮겨라**(`features/…` · `ds/` · `lib/`). 바퀴 10 의 트리를 되돌리지 마라 |
| **M-3** | **CSS 는 우리 것.** `frontend/src/styles.css` 는 **삭제 상태를 유지**한다(`git rm`). 다만 **main 이 그 파일에 넣은 변경 45줄은 버리지 말고** 우리 새 CSS 파일(`styles/*.css`) 중 맞는 자리로 옮겨라 |
| **M-4** | **문구는 prop 으로.** main 이 새로 넣은 코드가 `ds/` 부품을 쓰면서 문구를 안 넘기면 바퀴 11 규칙이 깨진다. 호출부에서 넘기게 고쳐라 |
| **M-5** | **구 클래스를 다시 들이지 마라.** main 의 새 코드가 `.btn`·`.field`·`.badge` 같은 구 클래스를 쓰면 **새 DS 부품·`.scax-*` 로 바꿔서** 들여라 |

## 3. 충돌 파일 (15)

**내용 충돌 11** — 양쪽 변경을 합쳐라:
```
App.tsx
features/action/ActionCenter.tsx · ActionMeetingCard.tsx · ActionTaskCard.tsx
features/auth/LoginPage.tsx
features/chat/AssistantMarkdown.tsx · MessageList.tsx
features/meetings/BookingModal.tsx · MeetingList.test.tsx
features/report/DailyReportPage.tsx
features/work/WorkModals.tsx
```

**위치 충돌 3** — main 이 `src/chat/` 에 넣었는데 우리는 `features/chat/` 이다. 후자로:
```
features/chat/answerElements.ts
features/chat/useConversations.test.tsx
features/chat/AssistantMarkdown.test.tsx
```

**삭제 vs 수정 1** — M-3 대로:
```
frontend/src/styles.css     ← 지운 채로 두고, main 의 45줄은 새 CSS 로 옮긴다
```

## 4. main 이 새로 넣은 파일 — 우리 구조로 옮겨라

`src/` 평면에 들어와 있다. 무엇인지 읽고 맞는 도메인으로:
```
BrowserInteractionPage.tsx(+test) · BrowserRecordingPage.tsx
CommandConfirmationForm.tsx(+test) · browserOperationGuard.ts
liveTranscription.ts(+test) · DailyReportPage.test.tsx
```
`DailyReportPage.test.tsx` 는 짝이 `features/report/` 에 있다. 나머지는 네가 판단하고 보고해라.

**이 화면들도 새 DS 로 갈아야 한다**(M-5). main 은 구 DS 기준으로 썼다.

## 5. allowed_paths

- `frontend/` — **`backend/` 는 한 줄도 안 건드린다.** main 이 가져온 backend 변경은 그대로 받는다

## 6. 검증

```
cd frontend && npx tsc --noEmit     → 0
cd frontend && npx vitest run        → 전체
cd frontend && npx vite build        → 성공
```

> 기준선이 둘이다 — 우리 쪽 **487**, main 쪽은 새 테스트가 붙었다.
> **합친 뒤 숫자는 487보다 커야 정상이다.** 작아지면 main 의 테스트를 잃은 것이다.
> `git show origin/main:frontend/...` 로 main 의 테스트 파일 수를 세어 확인해라.

**특히 확인할 것:**
- `grep -rn --include='*.tsx' '"[가-힣]' src/ds/ | grep -v '.test.'` → **0** (바퀴 11 규칙이 안 깨졌나)
- 구 클래스 `.btn`·`.field`·`.badge`·`.chip`·`.avatar` 가 마크업에 **0곳**
- `frontend/src/styles.css` 가 **없는지**

## 7. 하지 말 것

- **`git merge --abort` 하지 마라.** 풀어라
- **`git stash` 금지.** 임시 커밋을 써라
- **최종 커밋 하지 마라** — 코디가 검증하고 커밋한다. 임시 커밋은 남겨도 된다
- 막히면 **혼자 오래 붙들지 말고 보고**해라. 어느 쪽을 살릴지 애매하면 물어라

## 8. 보고

- 충돌 15건 각각 **어떻게 풀었는지** (어느 쪽을 살렸나, 합쳤나)
- main 의 새 파일을 **어디로 옮겼는지**
- **`styles.css` 45줄이 어디로 갔는지**
- main 의 새 코드에서 **구 클래스를 새 DS 로 바꾼 자리**
- `tsc` · `vitest`(487보다 큰가) · `vite build`
- 판단이 애매했던 자리
