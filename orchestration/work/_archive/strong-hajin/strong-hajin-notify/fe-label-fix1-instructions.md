# [frontend] 정정 — 「메시지함」 → 「메시지」 **화면에 보이는 것 전부** (사용자 2026-10-10)

앞 지시(`fe-label-instructions.md`)의 「사이드바만 · 화면 제목은 그대로」 를 **뒤집는다.** 사용자: 「여기 메시지함 → 메시지로 다 바꾸라고」.

- **사용자에게 보이는 글자 전부**: 사이드바(`App.tsx:51`) · 화면 머리 제목(`App.tsx:67`) · 레일 제목(`labels.ts` `inboxScreen.title` · `nav`) · 불러오는 중/오류 문구(「메시지함을 불러오는 중」 → 「메시지를 불러오는 중」 등 — 한국어가 자연스럽게) · 설정 안내(「…메시지함에서 사라진다」) · 알림 목록·OS 알림의 가는 곳 글자(「메시지함 · 슬랙」) · 그 밖 `frontend/src` 의 사용자 문구 — **`grep -rn 메시지함 frontend/src` 로 전부 세고** 하나씩 처분(바꿈 / 주석·코드 이름이라 둠)을 리포트에
- **바꾸지 않는다**: 코드 식별자(`inbox` · `InboxPage` 등) · 주석 · 서버(`backend/`) · 셸(`src-tauri`) 문구는 grep 해 보고만(있으면 리포트에 — 코디 판단)
- 시험의 기대 문자열을 같이 맞춘다(grep 으로 전부)
- 검증: 고친 시험 파일만 + `npx tsc --noEmit` · 전체 금지 · 커밋 금지
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-label-report.md` · 완료 보고는 앞 지시와 같은 두 명령
