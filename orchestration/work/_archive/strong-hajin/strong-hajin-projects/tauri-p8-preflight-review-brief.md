# WORK-006 Phase 8 preflight 독립 검수

대상 코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
대상 보고서: `orchestration/work/strong-hajin-projects/tauri-p8-preflight-report.md`

`verify-final-build.mjs`와 Makefile 변경을 read-only 검수하고 `orchestration/work/strong-hajin-projects/review-tauri-p8-preflight-report.md` 한 파일만 작성한다.

확인:
- 운영 origin 미결/placeholder에서 nonzero로 차단되는가.
- https 단일 origin, wildcard/path/query/localhost/IP/.invalid/빈값 거부가 실제 동작하는가.
- shell.config operationalOrigin과 capability remote.urls 불일치가 차단되는가.
- D-4·운영 서버 실재·M-1/M-5는 정적 검증으로 통과시키지 않고 evidence가 있을 때만 attested로 기록되는가.
- `--shell-root` scratch rehearsal가 실제 repo 설정을 변경하지 않는가.
- Phase7 shell-verify 회귀, 허용 경로, Release/설치/태그/push 부재를 확인한다.
- 최종 origin 없는 상태를 Phase8 완료/최종 아티팩트 생성으로 과장하지 않았는가.

FAIL/WARN/PASS 분리. 실제 운영 배포·설치·Release는 하지 않는다.
