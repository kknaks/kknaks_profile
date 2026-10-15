# [frontend] 정정 2 — 「메시지」 는 **세 곳만** (사용자 2026-10-10 최종)

사용자가 고른 것은 **세 곳뿐**이다: ① 사이드바 항목(`App.tsx:51`) ② 화면 머리 제목(`App.tsx:67`) ③ 목록 칸(레일) 제목(`labels.ts` `inboxScreen.title`). `inboxScreen.nav` 는 사이드바 이름이면 「메시지」, 쓰는 곳이 없으면 되돌린다(grep 으로 확인).

- **나머지는 「메시지함」 으로 되돌린다**: `loadingList` · `listError` · 설정 안내(`mailRemoveLines` · `slackDisconnectLines` · `roomRemoveLines` · `kakaoRoomRemoveLines` · `kakaoIntro`) · 알림 가는 곳(「메시지함 · 슬랙」 등) · 그 밖 이번에 바꾼 문구 전부
- 시험 기대 문자열도 그에 맞게(세 곳을 단언하는 것만 「메시지」)
- 검증: 고친 시험 파일만 + `npx tsc --noEmit` · 커밋 금지
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-label-report.md` 를 덮어써 최종 세 곳 · 되돌린 곳 목록 · 수치
- 완료 보고는 앞 지시와 같은 두 명령(subject 「frontend 완료: 메시지 세 곳」)
