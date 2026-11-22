# [mobile] P5 — 앱 통역 클라이언트를 서버 P1(통키 56e43a0)에 맞춤 (DAY 직원 앱 0.2.0)

같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-app-brief.md` 의 역할 · 규칙 · 검증 · 금지 그대로. M1 은 커밋 `e7853088`, 서버 P1 은 `a7868dc6`. ⚠ backend 워커가 같은 워크트리 `backend/` 에서 P2 작업 중 — `backend/` 읽기만 · git 읽기만(커밋은 코디).

## 정본
- 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` §3 「통역 — 0.2.0」 · U-15 통역 드로어(반이중 걷음 줄) · OQ-A61(닫힘 — `playback_stopped` = [멈춤] · 재생 지우기만 · 출력 구간 안일 때)
- 서버 사실: 커밋 `a7868dc6`(`git show a7868dc6` · `backend/day/services/interpret/session.py` 등) · 서버 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-p1-report.md`
- 통키 클라이언트 원천(읽기만): `git -C /Users/kknaks/git/toy_pr2/interpret-pwa show 56e43a0:front/lib/interpret.ts` — PCM 버리기 · 재생 구간(+400ms 판정용) · `audio_stop` · `playback_stopped`
- 검수 지적 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-doc-1-report.md` W-12 · W-13

## 할 것
1. `app/lib/interpret/interpret_client.dart` 등: **반이중 걷음**(재생 중에도 마이크 보냄) · 서버 `audio_stop` 오면 재생 멈춤(id 보지 않음) · 멈춤 · 닫기 · 오류 · `audio_stop` 모든 경로에서 다음 `audio_start` 까지 PCM 버림 · `playback_stopped` 는 [멈춤] · 재생 지우기 때만(출력 구간 안) · 서버 `audio_end` 응답 처리 · 빈 final caption 지우기 프레임(같은 id 말풍선 지움)
2. 화면 · 글자는 바꾸지 마라(드로어 모양 그대로 · 새 글자 금지).
3. 테스트(클라이언트 상태 · 프레임 처리).
4. 실물: 로컬 서버가 없으면 목 WS 로. iOS 시뮬레이터 마이크 실호출은 pending 가능.

## allowed_paths
- `app/lib/interpret/` · 통역 관련 `app/lib/ui/` 파일(필요할 때만) · `app/test/`
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-p5-report.md`

완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 · push · PR 금지.
