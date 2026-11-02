# WORK-006 Phase 8 preflight 최종 재검수

대상: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects/frontend/scripts/verify-final-build.mjs`, `orchestration/work/strong-hajin-projects/tauri-p8-preflight-fix-report.md`

W-1/W-2 보정을 독립 검수하고 `orchestration/work/strong-hajin-projects/review-tauri-p8-final-report.md`만 작성한다.

- scratch `--shell-root` rehearsal + evidence는 exit 0이 아닌 별도 코드로 끝나고 manifest/banner에 rehearsal이 남는가.
- SHELL_ROOT가 존재하지 않으면 친절한 차단 메시지와 nonzero인가.
- 실제 root에서 아직 운영 origin/D-4/evidence가 없으면 기존처럼 차단되는가.
- M-5가 앱 재시작 후 쿠키/로그인 유지로 설명되는가.
- 설정/Makefile/제품/인프라/Release는 무변경이고 Phase7 회귀와 미측정 표기가 유지되는가.

실제 운영 배포·설치·Release·태그·push 금지. FAIL/WARN/PASS 분리.
