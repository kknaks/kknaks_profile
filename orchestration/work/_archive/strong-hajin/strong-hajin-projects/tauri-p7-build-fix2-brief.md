# WORK-006 Phase 7 최종 WARN/FAIL 보정

대상 코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`

최종 재검수 F-1·W-1·W-2만 처리한다.

1. `verify-shell-build.mjs`에서 실제 구성상 빌드를 막을 수 있는 `unverifiable`(예: .icns 부재)와 호스트 능력상 다른 플랫폼을 이 기기에서 못 굽는 정보(`hostNotes`)를 분리한다. 기본 출력은 두 종류의 건수를 각각 보여준다. `--strict`/`SHELL_STRICT=1`은 구성상 unverifiable만 실패로 승격하고 hostNotes는 정보로 남긴다. macOS에서 .icns를 채우면 strict가 실제로 초록이 될 수 있어야 한다. 기존 7개 검증과 플랫폼 대체 금지 문구는 유지한다.
2. `tauri-p7-build-fix-report.md`의 F-1 문장을 사실대로 고친다: config.rs에 recommended 문장이 없다고 쓰지 말고, 직전 인용 범위가 3612에서 끊겨 3613 권고 줄을 빠뜨렸으며 같은 문장을 schema에서 인용하도록 정정했다고 쓴다.
3. 두 보고서의 검증 명령 예시에 `SHELL_TAG=v0.0.1 SHELL_STRICT=1 make shell-verify` 조합을 한 줄 추가하고, 태그와 strict를 함께 거는 목적을 적는다.

허용 파일: `frontend/scripts/verify-shell-build.mjs`, `Makefile`(필요한 설명만), `tauri-p7-build-report.md`, `tauri-p7-build-fix-report.md`, 보정 보고서 `tauri-p7-build-fix2-report.md`.
실제 설치·Release·태그·push 금지. 기본/strict/태그 조합과 기존 정적 회귀를 실행하고 결과 및 M-10/Windows/D-4 미측정을 기록한다.
