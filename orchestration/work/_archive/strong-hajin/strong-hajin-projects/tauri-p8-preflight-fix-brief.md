# WORK-006 Phase 8 preflight WARN 보정

대상 코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`

검수 W-1·W-2만 수정한다.

1. `verify-final-build.mjs`에서 `--shell-root`/SHELL_ROOT scratch rehearsal가 evidence로 G5를 충족해도 exit 0을 반환하지 않게 한다. 연습 경로는 manifest/banner에 rehearsal을 표시하고 exit 3 같은 별도 nonzero로 종료해 자동화가 실제 관문 통과로 집계하지 못하게 한다. 실제 root에서 운영 origin·evidence가 모두 갖춰진 경우에만 exit 0을 유지한다. `SHELL_ROOT=/nonexistent` 같은 경로는 raw fs stack 대신 명확한 차단 메시지와 nonzero로 끝낸다.
2. G5 M-5 entry label을 `M-5 — 앱 재시작 후 로그인(쿠키) 유지`로 고친다.
3. 보고서 `tauri-p8-preflight-fix-report.md`에 변경·검증·현재 운영 origin/D-4 미결을 기록한다.

허용 파일: `frontend/scripts/verify-final-build.mjs`, `orchestration/work/strong-hajin-projects/tauri-p8-preflight-fix-report.md`. Makefile/설정/운영 origin/제품 코드는 수정하지 않는다. 실제 운영 배포·설치·Release 금지.
