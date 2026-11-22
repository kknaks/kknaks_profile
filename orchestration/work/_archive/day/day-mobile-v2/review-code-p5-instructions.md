# [reviewer] 코드 검수 — mobile P5 앱 통역(커밋 bb8412de)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 읽기만(backend 워커가 같은 워크트리 `backend/` 작업 중 — git 읽기만). 대상 = 커밋 `bb8412de` 하나.

- 지시 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-p5-instructions.md` · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-p5-report.md`
- 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` §3 「통역 — 0.2.0」 · U-15 · OQ-A61
- 서버 사실 커밋 `a7868dc6`(`backend/day/services/interpret/session.py`) · 서버 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-p1-report.md`
- 통키 클라이언트 `git -C /Users/kknaks/git/toy_pr2/interpret-pwa show 56e43a0:front/lib/interpret.ts` · `front/lib/output.ts`

## 볼 것
1. 서버 프로토콜과 프레임 단위로 맞나(`audio_stop` · `playback_stopped` → `audio_end` · 빈 final · PCM 버리기 경로 전부) · 통키 front 와 같은 동작인가
2. 재생 중 마이크 송신 — 메아리 판정은 서버 몫이니 앱이 막지 않는가 · 상태 경합(멈춤 직후 audio_start · 다시 연결)
3. allowed_paths 밖 `app/lib/state/interpret_controller.dart` 3줄 — 필요한가 · 부작용
4. 테스트 · `flutter analyze` · 관련 `flutter test` 1회

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-p5-report.md` · FAIL/WARN/PASS · 파일:줄. 수정 · 커밋 금지. 완료 보고는 dispatch preamble 의 worker_done 그대로.
