# WORK-006 Phase 8 W-1 문서/진입점 보정

`Makefile`의 `shell-final-preflight` 주석과 `orchestration/work/strong-hajin-projects/tauri-p8-preflight-fix-report.md`에 자동화 진입점을 명시한다: GNU make는 레시피의 nonzero를 2로 감싸므로 exit 1/2/3 원인을 구분해야 하는 자동화·CI는 `cd frontend && node scripts/verify-final-build.mjs`를 직접 호출하고 종료 코드를 읽는다. Make 타깃은 사람이 보는 편의 진입점으로 남긴다. 실제 관문 동작·설정·제품 코드는 바꾸지 않는다. 보정 보고서 `tauri-p8-w1-fix-report.md`에 검증과 W-2 잔여 우회를 정직하게 기록한다. 실운영/설치/Release 금지.
