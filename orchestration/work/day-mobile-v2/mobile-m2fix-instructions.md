# [mobile] M2 고침 — 검수 FAIL 1 · WARN 3

같은 워크트리 · 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-app-brief.md` 그대로. 커밋됨 M3 (최신). ⚠ backend 가 `backend/` F1 작업 중 — 읽기만 · git 읽기만.

검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-m2-report.md`:
1. **FAIL** 원장 변경 창 「호출할 시술 · 1개」 — 웹에 없는 칸 → 지움(`app/lib/ui/room_screen.dart:528` procs 비움 · 웹 `ui.html:406` single 레이아웃과 같게)
2. WARN 바로 시작 `rejected[]` — 웹처럼 코드를 중복 없이 **여러 장** 토스트(웹 `backend/day/routers/board.py:628`) · 앱 토스트 칸이 하나면 웹 순서대로 차례로 보이게
3. WARN 캡처 하네스 — `debugDisableShadows` 로 메뉴가 검은 테두리로 찍힘 → 하네스에서 그림자 켜고 `shots/m2-*.png` 다시 찍기(덮어쓰기)
4. WARN 호출 취소 ⋮ 에 덧붙인 `state=='called'` 조건 → 서버 `canCancelCall` 만

검증 analyze · test · build ios --no-codesign 각 1회. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-m2fix-report.md`. 완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 금지.
