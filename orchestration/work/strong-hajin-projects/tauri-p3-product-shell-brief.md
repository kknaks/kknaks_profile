# WORK-006 Phase 3 발주 — 제품 Tauri 셸

## 목표

Phase 1 탐침을 제품 셸로 흡수한다. Phase 2의 M-7 관측(HTTPS/TLS 실패에서 page-load 이벤트 없음)을 설계 입력으로 삼아 연결 실패 화면(U-2)을 구현한다. M-1은 아직 미측정이므로 이 Phase에서 최종 통과로 닫지 않는다.

## 범위

- 코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
- 허용: `frontend/src-tauri/**`, 필요한 Tauri 설정/`frontend/package.json`만.
- 금지: `frontend/src/**`, `App.tsx`, `features/**`, `api.ts`, `microphone.ts`, `backend/**`, SPEC/WP/index/log.
- 출력: `orchestration/work/strong-hajin-projects/tauri-p3-product-shell-report.md`.
- 커밋/push/PR/Release/운영 배포 금지.

## 계약 불변식

1. 웹에 노출하는 커맨드는 정확히 넷(`shell_info`, `wake_guard_acquire`, `wake_guard_release`, `open_external`)이다. 파일·프로세스·범용 셸·open_path 권한을 추가하지 않는다.
2. 커맨드 capability origin과 네비게이션 허용 목록을 분리한다. 운영 origin은 미정이므로 기존 fixture 값을 제품 운영값으로 승격하지 말고 설정 자리만 둔다.
3. 점유 해제는 CloseRequested·막힌 navigation 요청이 아니라 Destroyed·실제 document replacement 같은 완료 사건에서만 한다. 네이티브 소유·TTL/renew/refcount 없음·Op::Shutdown을 보존한다.
4. 같은 세션 재요청은 중복 점유를 만들지 않고, OS assertion이 사라졌다면 재무장한다. macOS assertion id 캐시 no-op(W-4)와 Windows engage 실패 후 release(W-5)를 반드시 해결하거나 코드 보고서에 차단으로 올린다.
5. 늦은 acquire/release 경합 후 최종 잔존 0을 보장한다. 선택 수단을 코드 주석과 테스트로 남긴다.
6. U-2: page-load 훅만으로 TLS 실패를 감지할 수 없다는 M-7 결과를 반영해 별도 로딩/연결 실패 신호를 구현한다. 수단이 없으면 조용히 제거하지 말고 Phase 3 BLOCKED 보고를 낸다.
7. `open_external`은 http/https만 허용하고 앱 창·두 번째 웹뷰를 만들지 않는다. incognito를 켜지 않아 쿠키 저장소를 보존한다.

## 구현 요구

- 탐침 전용 `src/dev`, `probe.html`, loopbackMirror, `SCAX_PROBE_*` 손잡이를 제품 셸에 복사하지 않는다.
- 제품 식별자·아이콘·번들 target은 기존 Phase1 자리를 검토해 결정하되 운영 주소나 서명 신원을 발명하지 않는다.
- macOS와 Windows 조건부 코드를 각각 읽고, 가능한 범위에서 `cargo check --all-targets`, clippy, frontend tsc/test를 실행한다. Windows가 컴파일 불가하면 그 사실을 명시한다.
- 제품 셸이 외부 운영 origin을 열기 전에도 fixture에서 설정·권한 경계를 정적으로 검증한다. M-1 최종 측정은 별도 기록으로 남긴다.

## 완료 보고

보고서에 변경 파일 목록, 커맨드/권한 수, U-2 감지 수단, 수명 정리 경계, W-4/W-5 처리, 테스트 명령과 결과, 미검증 OS 축을 적는다. AC-T12~T18, T20~T23, T25, T31, T33~T34 15건의 증거 위치를 매핑한다.
