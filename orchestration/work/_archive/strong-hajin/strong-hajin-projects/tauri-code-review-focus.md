# WORK-006 코드 검수 공통 기준

사용자 야간 지시: 구현→검수→수정 직렬. 문서 품질 검수 반복이 아니라 실제 코드 계약·안전성·회귀를 확인한다. 실기 미수행은 내일 사용자 설치 E2E로 남긴다. 미실측을 자동 통과로 간주하지 않는다.

## Phase1 우선 검수

- remote HTTPS origin 하나 + 최소4 커맨드 권한. 로컬 다른 origin/프레임/외부 navigation에서 OS 기능 호출을 넓혀주지 않는다.
- TLS 검증 무력화·키체인/전역 신뢰 자동설치·인증서 개인키 추적 없음.
- 자동 idle system sleep만 억제, 화면/수동 sleep 보존. macOS assertion 수명·Windows SetThreadExecutionState thread 수명 확인. async command 임의 스레드 이동으로 assertion 잃는 경로 검수.
- TTL/renew 없음, session key 중복/late release/acquire/문서세대 경계 및 close 취소 보존. 탐침 단계와 Phase3 추가 구현을 구분하되 반대 구조를 깔지 않는다.
- MIME 경로2·mic 오류·명시적 녹음 종료/장치 해제·IPC 실패 표시. 제품 라우트/빌드에 fixture 유출 없음.
- 변경 Rust 실제 검사, tsc·FE suite 결과 원문과 범위 확인. Windows 실행 미확인과 cross compile 통과 구분.
- 범위 밖 지적은 해당 Phase에 명시된 후속 작업인지 먼저 확인. 구현 필수 계약 위반은 FAIL, 장비 부재 자체는 FAIL 아님.

검수 리포트에는 실제 파일:줄 근거, 최소 수정, 사용자 실물에서 만날 문제, 미검증 경계를 적는다. 리뷰어는 코드 수정하지 않는다.

## Phase6 운영 인증 사전 코드 관찰

2026-09-22 read-only: settings.py local_login_enabled는 PRODUCTION이 아니면 true이며 docstring은 production 외부 provider 전제를 갖는다. create_app은 developer_auth_enabled 아래 앱 service/session store와159 라우트를 함께 등록한다. 따라서 단순 dedent만으로 실제 로그인까지 생기지 않는다. auth/providers에는 개발 demo 계정/비밀번호 안내도 있으므로 운영에서 제외해야 한다. 향후6a/6b는 개발 persona 헤더·demo shortcut을 운영에 노출하지 않으면서 기존 password 검증·권한 의미와 cookie 세션을 유지하는 명시적 운영 구성 및 테스트를 설계해야 한다. 외부 provider를 구현했다고 주장하거나 production 이름만 바꿔 개발 모드를 쓰지 않는다.

## Phase1 작성 중 관찰(완성 전 코드이므로 최종본에서 재확인)

- lib.rs on_page_load Started에서 clear_window 호출. 탐침 로그 목적과 실제 문서 교체 완료 보장을 구분해야 함. 요청 시작만으로 이전 문서 정상 녹음 점유를 해제하는지 확인.
- guard.rs generation은 초기 버전에서 로그 전용이었다. 늦은 acquire 뒤 잔존0/이전 문서 명령 격리는 최종 Phase1과 Phase3 책임을 구분해 검수. 아직 미작성인 단계를 Phase1 전체 실패로 확대하지 않되 구현 방향이 기존 계약과 반대면 수정 필요.
- power.rs는 OS 호출 전용 스레드를 사용하고 thread identity 테스트를 작성 중. Windows thread-bound 문제의 올바른 방향인지 최종본 확인.
- 코디 자체 URL 파서 제거 지시 tauri-p1-url-note.md 전달 후 표준 url crate 및 정규화 테스트 반영을 워커 화면에서 확인. 최종 코드 검수에서 확인.

## Phase1 Rust 종료 교착 수정 증거(워커 보고, 독립 검수에서 확인)

cargo PID90477·test PID91208 CPU0 장기대기를 코디가 관측. power.rs 테스트의 sender clone 생존→Drop join→rx.recv 미종료를 코디가 지적, 워커 sample stack으로 확정. Op::Shutdown 명시 사건 및 송신자 사본 생존 종료·스레드 부재 실패 회귀시험 추가. 워커 cargo test21 passed 보고. 정리한 두 PID는 이 작업의 대기 프로세스뿐. 독립 검수는 최신 Drop/Shutdown과 회귀시험이 이 경로를 실제로 검사하는지 확인.
