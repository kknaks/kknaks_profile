# WORK-006 Phase 7 검수 WARN 보정

대상 코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`

검수 WARN 3건만 닫는다.

1. `frontend/scripts/verify-shell-build.mjs`와 `Makefile`에 strict build 검증 경로를 추가한다. 기본 `make shell-verify`는 현재처럼 정적 검증을 하되 `.icns` 같은 `unverifiable` 항목 수를 명확히 출력하고, `SHELL_STRICT=1 make shell-verify`(또는 동등한 명시적 플래그)는 unverifiable을 실패로 승격해 “문제 0건=빌드 가능” 오독을 막는다. 기존 양 플랫폼·원격 origin·권한 검증은 유지한다. 운영 주소/아이콘을 발명하지 않는다.
2. `tauri-p7-build-report.md`에 Tauri 상류가 config version 관리를 권고하지만, 이번 Phase에서는 허용 경로와 값 선택 미결을 이유로 Cargo.toml 단일 출처를 택했고 Phase8에서 판 번호 정책을 재검토한다는 사실을 추가한다.
3. 같은 보고서의 작성 시각 자리표시를 실제 현재 KST 시각으로 바꾼다.

허용 파일: 위 스크립트, Makefile, `tauri-p7-build-report.md`, 보정 보고서 `tauri-p7-build-fix-report.md`.
실제 설치·빌드·Release·태그·push는 하지 않는다. 기존 검증을 재실행하고 결과와 미측정(M-10/Windows/D-4)을 기록한다.
