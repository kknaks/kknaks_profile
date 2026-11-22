# [mobile] M4 — 통역 드로어 글자를 바뀐 기능(통키 56e43a0)에 맞춤

같은 워크트리 · 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-app-brief.md` 그대로. 최신 커밋 841454c4. ⚠ backend 가 `backend/` F1 작업 중 — 읽기만 · git 읽기만.

## 배경 (사용자 2026-11-20)
통역 기능이 통키 최신으로 바뀌었다(반이중 걷음 · 재생 중에도 들음 · 끼어들기 · 차례 끝 1초 · 멈춤 동작). 드로어의 안내 · 상태 글자 중 **옛 동작을 말하는 것**을 바꾼다. 예: `app/lib/interpret/interpret_widgets.dart:409` 「번역 음성이 나오는 동안은 듣지 않아요」.

## 글자 원천 — 이것만
- **통키 최신 화면 글자**: `git -C /Users/kknaks/git/toy_pr2/interpret-pwa show 56e43a0:front/...`(같은 상태 · 같은 뜻의 글자) · 통키 SPEC `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` 화면 글자 절
- 통키에 같은 뜻 글자가 없으면 **바꾸지 말고 표에 「원천 없음」**(코디가 사용자에게 묻는다). 줄을 지우는 게 맞아 보이면 지우지 말고 표에 「지움 제안」.

## 할 것
1. 드로어 · 통역 바 · 빠른 말하기 등 통역 화면의 모든 글자를 표로: (지금 글자 · 파일:줄 · 0.2.0 동작과 맞나 · 통키 같은 뜻 글자 · 통키 파일:줄 · 바꿈/그대로/원천 없음/지움 제안)
2. 「바꿈」 행만 코드에 반영(통키 글자 그대로). 화면 배치 · 기능은 그대로.
3. 같이: 대리 수락 창(U-6) 제목 「호출할 시술 · N개」 — 바꾸지 말고 위치(파일:줄)만 표에 적어라(사용자 글자 대기).
4. analyze · test · build ios --no-codesign 1회 · 캡처 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/shots/m4-*.png`(드로어 듣는 중 · 재생 중 · 멈춤)

## allowed_paths
`app/lib/interpret/` · 통역 관련 `app/lib/ui/` · `app/lib/core/copy.dart`(통역 글자만) · `app/test/` · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-m4-report.md`(위 표가 본문)

완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 금지.
