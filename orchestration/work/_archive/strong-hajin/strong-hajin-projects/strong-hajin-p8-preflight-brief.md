# WORK-006 Phase 8 운영 origin 최종 빌드 게이트

## 목표
운영 origin이 아직 결정되지 않은 상태에서 Phase 8의 최종 설정/빌드를 안전하게 준비한다. 실제 origin·도메인·로그인 수단을 발명하거나 placeholder를 최종판으로 굽지 않는다.

## 코드 워크트리
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`

## 허용 경로
- `frontend/scripts/verify-final-build.mjs` (신규)
- `Makefile` (Phase8 preflight 타깃만)
- 보고서: `orchestration/work/strong-hajin-projects/tauri-p8-preflight-report.md`

## 계약
- `capabilities/product-shell.json`의 현재 placeholder/fixture origin은 변경하지 않는다.
- 최종 origin은 `https` 정확한 단일 origin이어야 하며, `.invalid`, wildcard, 경로 포함 origin, 빈 값은 거부한다.
- shell config의 operationalOrigin과 capability remote.urls가 동일해야 한다. 다르면 즉시 실패한다.
- D-4 로그인 수단 미결, 운영 서버 실재 미확인, M-1/M-5 미측정은 통과로 쓰지 않는다.
- 최종 빌드·설치·Release·태그·push는 수행하지 않는다. 이 작업은 preflight gate와 증거 형식만 만든다.

## 구현
1. 현재 두 origin 설정을 읽어 실제 운영값이 들어왔는지 검사하는 preflight 스크립트를 추가한다.
2. `SHELL_OPERATING_ORIGIN`을 선택적 입력으로 받아 두 설정과 정확히 일치할 때만 다음 단계 명령을 안내한다. 입력이 없거나 placeholder면 실패한다.
3. 판 번호·shell_api·origin·소유 아티팩트 식별자를 기록할 manifest 출력 형식을 만들되, 빌드 아티팩트가 없으면 해시를 만들지 않는다.
4. Makefile에 `shell-final-preflight`를 추가한다. 절대 실제 설정 파일을 쓰거나 빌드하지 않는다.
5. 현재 환경에서 preflight가 placeholder/D-4/서버 미실재를 정직하게 차단하는지 검증하고 보고한다.

## 완료 조건
- origin 미결 상태에서 preflight가 0이 아닌 종료로 멈춘다.
- 올바른 https 입력·설정 일치·D-4/서버 확인 전에는 최종판 통과를 내지 않는다.
- 운영 origin이 정해지면 Phase8 후속 워커가 이 gate를 통과한 뒤에만 설정→빌드→검증 순서로 진행할 수 있다.

끝나면 worker_done으로 변경 파일·검증·남은 차단을 보고한다.
