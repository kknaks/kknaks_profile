# Phase1 독립 코드검수 범위 (아직 발주 전)

코드 /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects 의 Phase1 변경만 읽기전용 검수. 기준 HEAD a1f6791이나 발주 시 재확인한다. 산출물은 /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/review-tauri-p1-report.md 하나. 코드 수정·커밋·push·PR·추가워커 금지.

읽을 것: 코드 AGENTS, /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer 규약, tauri-p1-implementation-brief.md, tauri-p1-url-note.md, tauri-code-review-focus.md, 구현 보고서, WORK-006 Phase1, SPEC-006 §4·5. 사용자 최신 범위 tauri-overnight-execution.md.

Phase1은 탐침·fixture 코드 준비다. 제품화·웹 배선은 Phase3/4이고 실제 설치·최종E2E는 내일. 미실측 자체는 코드 FAIL이 아니지만 미실측을 성공으로 보고하거나 계약과 반대 구현은 FAIL.

핵심: capability remote origin 정확성, 외부 URL 표준 파서, TLS 우회 부재, 명령4·응답 형식, OS 절전 assertion 수명과 Windows 호출 스레드 일관성, acquire/release race·문서 교체·취소 close, Mic 권한 최소화, fixture와 제품 빌드 격리, MIME2경로, 종료 track 정리, 테스트가 구현을 그대로 베끼는지/실제 경합·실패를 보는지, allowed_paths와 잠금파일/ignore 정합.

작업 전후 diff·새파일을 직접 읽고 파일:줄 근거로 PASS/WARN/FAIL 판정. 완료 보고서 수치를 그대로 옮기지 말고 검증 로그/테스트코드와 대조. 이미 실행된 전량 검사는 반복하지 않는다. 필요한 좁은 검증만 허용, 빌드 경합 피하기 위해 writer 완료 뒤 실행. 실패는 현재 Phase와 후속 Phase 책임을 구분하고 범위 밖 개선 요구 금지.

서버 배포/설치/마이크 녹음/OS 설정 변경·신뢰 인증서 설치 없음. 실제 사용자 E2E에서 확인할 자리와 자동검증으로 닫힌 자리를 구분해 보고.
