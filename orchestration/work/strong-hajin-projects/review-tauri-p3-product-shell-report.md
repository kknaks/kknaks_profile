# WORK-006 Phase 3 제품 셸 검수

## 판정

**조건부 통과 — 저지 0, WARN 4.** Phase 4 웹 배선으로 진행할 수 있다. 운영 주소 확정과 Windows 실기 검증은 이후 단계의 전제로 남긴다.

## 확인한 범위

- `frontend/src-tauri/**`만 Phase 3 변경이며 `frontend/src/**`에는 변경이 없다.
- IPC는 `shell_info`, `wake_guard_acquire`, `wake_guard_release`, `open_external` 네 개로 고정됐다. capability에는 네 권한만 있고 `local:false`와 단일 placeholder remote origin이 있다. 파일·프로세스·범용 셸 권한은 확인되지 않았다.
- 제품 셸에 probe 페이지, `SCAX_PROBE_*`, `loopbackMirror`, fixture 주소를 읽는 경로가 유출되지 않았다.
- 절전 점유는 네이티브 장부와 OS 스레드가 소유한다. TTL·renew·참조계수는 없고, `CloseRequested`와 막힌 navigation에서는 해제하지 않으며 `Destroyed`와 실제 문서 교체에서만 정리한다.
- macOS 재무장 회귀가 실행됐고 Rust 테스트 45건이 통과했다. 프론트 회귀 테스트와 제품 빌드도 구현 보고서의 증거대로 통과했다. Windows 교차 빌드는 소스 오류가 아니라 현재 환경의 `llvm-rc` 부재로 미검증이다.
- M-7의 `on_page_load` 부재 문제는 허용 navigation 시 로드 감시와 OS 신뢰 저장소 기반 TLS preflight로 보완했다. 점유 수명과 로드 감시 타이머는 분리돼 있다.

## WARN

1. 운영 origin은 아직 `.invalid` placeholder라 capability의 최종 보안 경계와 운영 빌드는 Phase 8에서 다시 확인해야 한다.
2. 연결 실패 preflight는 웹뷰가 직접 낸 오류가 아니라 같은 OS 신뢰 저장소를 쓰는 별도 TLS 연결의 결과다. 이 차이는 보고서에 기록돼 있으며 실기 운영판 검증이 필요하다.
3. 15초 로드 감시의 정상 지연·서버 응답 지연 경계는 운영 origin에서 실측하지 않았다. 연결 성공 후 문서가 늦는 경우에는 원인 없이 U-2 화면으로 갈 수 있다.
4. Windows WebView2 마이크 권한과 PowerShell/실기 절전 경로는 이 macOS 환경에서 검증하지 않았다. `llvm-rc`가 설치된 Windows CI 또는 실기에서 별도 확인해야 한다.

## 후속 조건

Phase 4는 셸 API 호출을 실제 마이크가 열린 순간에만 배선하고, `degraded`·호출 실패를 녹음 실패로 바꾸지 않는 계약을 검수한다. 운영 origin을 이 단계에서 발명하거나 capability를 넓히면 안 된다.
