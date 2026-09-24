# WORK-006 Phase 9 Release 자산 동일성 preflight

## 목표
실제 GitHub Release/태그/배포를 하지 않고, Phase 8이 검증한 설치파일과 Release 대상 자산이 동일한지 검사하는 로컬 preflight를 추가한다.

## 코드 워크트리
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`

## 허용 경로
- `frontend/scripts/verify-release-artifact.mjs` (신규)
- `Makefile` (release-preflight 타깃만)
- 보고서 `orchestration/work/strong-hajin-projects/tauri-p9-release-preflight-report.md`

## 계약
- 태그·GitHub Release·프로필 60-release 문서·push·서명·공증·업데이트는 수행하지 않는다.
- Phase 8 manifest가 없거나 artifacts가 비어 있으면 실패한다. placeholder/임의 해시를 만들지 않는다.
- 입력으로 Phase8 manifest와 candidate artifact directory를 받아 파일 SHA-256, 버전, shell_api, origin 조합을 비교한다.
- candidate는 Phase8 기록과 파일명·해시가 정확히 일치해야 한다. 빌드를 다시 하지 않는다.
- Windows 자산 미검증은 검증됨으로 바꾸지 않고 상태를 기록한다.
- D-4/운영 origin/M-10/Windows 미결을 보고서에서 유지한다.

## 구현·검증
1. JSON manifest schema와 오류 코드를 명확히 한다(입력 없음/manifest 미검증/artifact 누락/hash 불일치/조합 불일치).
2. `make shell-release-preflight`를 추가하되 기본은 dry-run/읽기 전용이다.
3. 정상·누락·해시 불일치·버전/조합 불일치 fixture를 임시 디렉터리에서 실행하고 저장소/Release에 손대지 않는다.
4. 현재 Phase8 artifact가 없으므로 실제 저장소에서 nonzero가 나오는 것을 기록한다.

끝나면 worker_done으로 보고한다.
