# [mobile] M5 — 통역 재생 중 안내 줄 지우기 (사용자 결정)

같은 워크트리 · 브리프 그대로. 최신 커밋 dba35bbd. git 읽기만.

사용자 2026-11-20: `app/lib/interpret/interpret_widgets.dart:409` 「번역 음성이 나오는 동안은 듣지 않아요」 줄을 **지운다**(새 글자 넣지 않음 · 그 자리 레이아웃이 어색해지지 않게만). 「번역 읽는 중」 은 그대로. 대리 수락 창 「호출할 시술 · N개」 그대로.
- 관련 테스트 · 캡처 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/shots/m4-*-drawer-playing.png` 다시 찍기(폰 · 아이패드)
- analyze · test · build ios --no-codesign 1회. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-m5-report.md`. 완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 금지.
