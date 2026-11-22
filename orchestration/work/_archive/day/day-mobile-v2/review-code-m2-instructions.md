# [reviewer] 코드 검수 — mobile M2(커밋 b91d2fca)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 읽기만(backend 가 `backend/` P3 작업 중 — git 읽기만). 대상 = 커밋 `b91d2fca`.

- 지시 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-m2-instructions.md` · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-m2-report.md` · 캡처 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/shots/m2-*.png`
- 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` U-17 · U-18 · U-19 · U-22 · OQ-A57
- 서버 계약 커밋 `e96b0718`(`routers/api/auth.py` · `routers/api/board.py` · `schemas/`) · 웹 글자 `backend/day/templates/` · `routers/board_messages.py`

## 볼 것
1. 서버 계약과 요청 · 응답 · 오류 갈래가 맞나(기기 선택 · /api/auth/device · quick-start rejected[] · cancel-call · 원장 바꾸기)
2. 서버 값(`canQuickStart` · `canCancelCall` · `canChangeDoctor`)만으로 그리나
3. 글자 원천 — 특히 **원장 변경 창의 「호출할 시술 · 1개」 칸**(원장 바꾸기에 호출 글자가 맞나 · 웹 원장 바꾸기 창 실제 글자 파일:줄) · 캡처 `m2-phone-cancel-call-menu.png` 의 ⋮ 메뉴가 **굵은 검은 테두리**로 보인다 — 앱 기존 메뉴 모양과 같은가(캡처 렌더 탓인가 실제 모양인가)
4. 조작 실패 글자를 웹 `message_of` 규칙으로 모은 변경(OQ-A57) — 기존 조작 회귀
5. `flutter analyze` · 관련 `flutter test` 1회

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-m2-report.md` · FAIL/WARN/PASS · 파일:줄. 수정 · 커밋 금지. 완료 보고는 dispatch preamble 의 worker_done 그대로.
