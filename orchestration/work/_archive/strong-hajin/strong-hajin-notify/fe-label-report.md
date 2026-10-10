# 「메시지함」 → 「메시지」 — 최종: **세 곳만** (사용자 2026-10-10 · 정정 2)

## 상태: done (커밋 없음)

- 브랜치 `kknaksss/strong-hajin-notify-label`(기준 `3321504`)
- 진행: 첫 지시(사이드바만) → 정정 1(화면 전부) → **정정 2(세 곳만 · 나머지는 되돌림)** — 이 리포트는 정정 2 기준으로 덮어썼다

## 최종 — 「메시지」 세 곳 (제품 diff 3줄)

| # | 자리 | 앞 → 뒤 |
|---|---|---|
| ① | 사이드바 항목 `frontend/src/App.tsx:51`(`navigation` 의 `inbox`) | 「메시지함」 → **「메시지」** |
| ② | 화면 머리 제목 `frontend/src/App.tsx:67`(`surfaceLabel.inbox`) | 「메시지함」 → **「메시지」** |
| ③ | 목록 칸(레일) 제목 `frontend/src/lib/labels.ts` `inboxScreen.title` — 레일 제목 글자와 그 칸의 `aria-label`(`MessageRail.tsx:165,169`) | 「메시지함」 → **「메시지」** |

`inboxScreen.nav` 는 쓰는 곳이 없다(grep `inboxScreen.nav` · `copy.nav` = 0). 지시대로 **「메시지함」 으로 되돌렸다**.

## 되돌린 곳 — 정정 1에서 바꿨다가 「메시지함」 으로

| 자리(`labels.ts`) | 지금 글자 |
|---|---|
| `inboxScreen.nav` | 「메시지함」 |
| `loadingList` | 「메시지함을 불러오는 중」 |
| `listError` | 「메시지함을 불러오지 못했습니다」 |
| `mailRemoveLines` · `slackDisconnectLines` · `roomRemoveLines` · `kakaoRoomRemoveLines` | 「…메시지함에서 사라진다.」 |
| `kakaoIntro` | 「…메시지함에서 보내지는 않는다.」 |
| 알림 가는 곳 `destinationOf`(둘) + 그 주석 | 「메시지함 · 슬랙/메일/카톡」(OS 알림 공유 글자도 그대로) |

`labels.ts` 의 diff 는 이제 `title` 한 줄뿐이다.

## 시험 — 세 곳을 단언하는 것만 「메시지」

| 파일 | 「메시지」 로 둔 단언 | 되돌린 단언 |
|---|---|---|
| `App.test.tsx` | 사이드바 단추 2 · 머리 제목 1 · 사이드바 점 `dotOf("메시지")` 3 | — |
| `shell/AppShell.test.tsx` | 화면 목록 · 사이드바 순서 · fixed 판정(사이드바 이름) 3 | — |
| `features/inbox/InboxPage.test.tsx` | 레일 region 이름 「메시지」(③의 `aria-label`) 1 | 오류 「메시지함을 불러오지 못했습니다」 |
| `features/notifications/NotificationsPage.test.tsx` | — | 가는 곳 「메시지함 · 슬랙」(원래대로 · diff 없음) |
| `lib/notificationLabels.test.ts` | — | 가는 곳 「메시지함 · 슬랙/카톡」(원래대로 · diff 없음) |

## 수치

| | 값 |
|---|---|
| `grep -rn 메시지함 frontend/src` | 처음 **75** → 지금 **62**. 줄어든 13은 위 세 곳 + 그것을 단언하는 시험 줄(10)이다 |
| 바뀐 파일 | 5(`App.tsx` · `labels.ts` · `App.test.tsx` · `AppShell.test.tsx` · `InboxPage.test.tsx`) · 13줄 |
| 서버 · 셸 | 손대지 않음(backend 의 「메시지함」 18줄은 전부 주석 · docstring · src-tauri 0) |

## 검증

| 명령 | 결과 |
|---|---|
| `cd frontend && npx vitest run src/App.test.tsx src/shell/AppShell.test.tsx src/features/inbox/InboxPage.test.tsx src/features/notifications/NotificationsPage.test.tsx src/lib/notificationLabels.test.ts --no-file-parallelism` | **exit 0** · 5 files · **118 passed** · 0 failed |
| `npx tsc --noEmit` | **0 오류** |
