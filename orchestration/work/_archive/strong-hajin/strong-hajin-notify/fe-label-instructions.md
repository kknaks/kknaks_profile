# [frontend] 사이드바 「메시지함」 → 「메시지」 (사용자 지시 2026-10-10)

작업 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify` — **브랜치 `kknaksss/strong-hajin-notify-label`(origin/main `3321504` 기준) 로 이미 바꿔 두었다.**

- **사이드바 항목 이름만** `메시지함` → `메시지` — `frontend/src/App.tsx:51` (`navigation` 의 `inbox`)
- **바꾸지 않는다**: 화면 머리 제목(`App.tsx:67` · `labels.ts` `inboxScreen.title`)· 레일 제목 · 그 밖 문구 — 사용자는 사이드바만 말했다. `labels.ts` `inboxScreen.nav` 가 사이드바에 쓰이는지 grep 으로 확인하고, 쓰이면 그것만 같이
- 사이드바 이름을 단언하는 시험(`App.test.tsx` · `AppShell.test.tsx` · `InboxPage.test.tsx` 등 — **grep 으로 전부**)을 맞춘다. 화면 제목을 단언하는 것은 그대로
- 검증: 고친 시험 파일만 `npx vitest run <파일들> --no-file-parallelism` + `npx tsc --noEmit` · 전체 금지
- 커밋 금지 · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-label-report.md`(바꾼 곳 · grep 수 · 시험 수치)
- 완료 보고 앞 브리프 §7 두 명령 — subject 「frontend 완료: 사이드바 메시지」 · text 「[worker_done] frontend 사이드바 메시지 완료 — <한 줄>」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
