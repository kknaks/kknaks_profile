# [reviewer] 코드 검수 — backend P1 통역(커밋 a7868dc6)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 읽기만(다른 워커가 같은 워크트리에서 작업 중 — git 은 읽기만 · stash · checkout 금지). 대상 = **커밋 `a7868dc6`**(`git show a7868dc6`) 하나.

- 브리프(계약 · 범위) `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-be-brief.md` · 워커 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-p1-report.md`
- 스펙(PR 브랜치 정본) `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` §3 「통역 — 0.2.0」 · 통역 서버 절
- 통키 원천 `git -C /Users/kknaks/git/toy_pr2/interpret-pwa show 56e43a0:<path>`(읽기만) · 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/para/projects/summer-star/interpret-pwa/10-decision/`
- 앞 문서 검수 지적(통역) `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-doc-1-report.md` F-3 · F-4 · W-9 ~ W-14

## 볼 것
1. 통키 56e43a0 과 동작이 같은가 — 항목별(v6 · D-67 · context text · TRIM_ORDER · D-71 · 시드 .11 로더 · 빈 원문 · 빈 final 지우기 · TokenGate · ECHO_TAIL · audio_stop · playback_stopped→audio_end · stop 큐 비움 · TTS timestamps/cancel · 바로잡기). 빠진 것 · 다르게 옮긴 것 파일:줄
2. DAY 에 안 맞게 들어온 것(records 계열 · PWA 전용)
3. 세션 정리 — Soniox 두 연결이 모든 경로에서 닫히나(동시 상한 · 조직 TTS 3)
4. 테스트가 동작을 실제로 보나 · `cd backend && uv run pytest -q tests/day/interpret` 1회 · ruff
5. allowed_paths 밖 변경(dtos 2파일은 코디 허용)

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-p1-report.md` · 판정 FAIL/WARN/PASS · 지적마다 파일:줄. 수정 · 커밋 금지. 완료 보고는 dispatch preamble 의 worker_done 그대로.
