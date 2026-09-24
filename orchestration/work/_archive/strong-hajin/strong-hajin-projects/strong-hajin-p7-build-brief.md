# WORK-006 Phase 7 — fixture 판 빌드 구성

## 목표
WORK-006 Phase 7의 코드 구현을 수행한다. 운영 주소·Release·실제 사용자 설치는 건드리지 않고, macOS·Windows 양쪽 지원을 보존하는 fixture origin 빌드 절차와 판 번호 일관성 검증을 코드에 마련한다.

## 코드 워크트리
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`

## 허용 경로
- `frontend/src-tauri/tauri.conf.json`
- `Makefile`
- 필요한 빌드·검증 스크립트는 `frontend/scripts/` 아래 신규 파일만
- 보고서: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/tauri-p7-build-report.md`

## 계약
- macOS·Windows 지원을 유지한다. Windows 실기/빌드 환경이 없으면 검증 불가로 기록하고 macOS 결과로 대체하지 않는다.
- 운영 origin, 도메인, 서명 신원, CI 러너, 최소 OS 버전은 발명하지 않는다. 미정은 placeholder/측정 대기로 명시한다.
- 코드 태그·tauri.conf version·shell_info app_version이 같은 판 번호를 검증할 수 있어야 한다. 기존 버전/식별자는 함부로 바꾸지 말고, 변경 필요 시 근거를 기록한다.
- fixture 판은 Release 발행 대상이 아니다. 운영 배포·GitHub Release·서명·공증·자동업데이트는 하지 않는다.
- M-10 실기(재설치·판 올림 쿠키 유지)는 사용자 설치가 필요하므로 미측정으로 남긴다. 테스트/정적 검증을 실기 통과로 쓰지 않는다.
- Phase 6b D-4 로그인 수단 미결은 그대로 유지한다.

## 구현
1. 현재 Tauri 설정과 Makefile을 읽고, 기존 제품 셸(`shell-noop`/원격 문서 로딩) 계약을 보존한다.
2. 양 플랫폼 bundle target/아이콘/버전 검증을 자동화할 수 있는 최소 Make 타깃 또는 스크립트를 추가한다. 명령은 실제 환경에서 안전하게 재실행 가능해야 하며, Windows 전용 명령을 macOS에서 성공했다고 표시하지 않는다.
3. fixture origin 판 두 개를 위한 버전 주입/검증 절차를 문서화한다. 실제 fixture URL/운영 주소는 placeholder로 둔다.
4. 빌드 가능한 범위에서 정적 검사와 설정 검증을 실행한다. 설치파일을 사용자 기기에 설치하지 않는다.

## 검증
- JSON/schema 또는 Tauri 설정 검증, Make/스크립트 dry-run, 기존 프론트·Rust 회귀검사를 실행한다.
- 결과에 실제 빌드 여부, Windows 환경 부재 여부, M-10 미측정을 구분한다.
- 변경 파일·수치·미결을 보고서에 좌표와 함께 기록한다.

## 금지
- 운영 서버 변경, 인프라 레포 변경, Release/태그/push, 비밀값 조회, 사용자 기기 설치
- 로그인/권한 구현 변경
- 확인하지 않은 macOS·Windows 설치 성공 주장

끝나면 worker_done으로 보고서를 남긴다.
