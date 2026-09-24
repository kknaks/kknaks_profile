# WORK-006 Phase 7 독립 검수

대상 코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
대상 구현 보고서: `orchestration/work/strong-hajin-projects/tauri-p7-build-report.md`

현재 Phase 7 변경을 코드·설정·보고서 기준으로 독립 검수하고, 아래 항목을 PASS/FAIL/WARN으로 분리해 보고서 한 파일만 작성하라:
`orchestration/work/strong-hajin-projects/review-tauri-p7-build-report.md`

검수:
- tauri.conf.json에서 버전 단일 출처(Cargo.toml 0.0.1)와 기존 식별자/원격 문서 계약이 보존되는가.
- `make shell-verify`가 버전 불일치, 양 플랫폼 타깃, 아이콘, 권한 경계를 실제로 검증하고 실패를 숨기지 않는가.
- `make shell-build-fixture`가 기본 dry-run이며 fixture origin 두 주소가 없을 때 중단하고 운영 주소를 발명하지 않는가.
- 허용 경로 밖 코드/인프라/Release/태그/서명/CI 변경이 없는가.
- 기록된 cargo check/test/clippy/tsc/frontend 수치가 현재 diff와 일치하는가.
- Windows 실기·M-10·설치파일 생성 미검증을 통과로 쓰지 않았는가.
- D-4 로그인 미결이 유지되는가.

실제 설치·운영 배포·태그·push는 하지 말고, 보고서만 작성한다.
