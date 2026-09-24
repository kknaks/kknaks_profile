---
title: Tauri local profile implementation report
status: complete
updated: 2026-09-23
---

# 결과

운영 셸 설정을 변경하지 않고 현재 로컬 웹 주소를 Tauri 창으로 여는 반복 명령을 추가했다.

- 실행 명령: `make tauri-local`
- 기본 주소: `http://127.0.0.1:5176`
- 다른 loopback 주소: `TAURI_LOCAL_ORIGIN=http://localhost:5176 make tauri-local`
- 전제: `make local-stack` 또는 별도 Vite/API 서버가 먼저 실행 중이어야 한다.

# 구현

`frontend/scripts/run-tauri-local.mjs`가 실행 시 임시 디렉터리를 만들고 `frontend/src-tauri/`를 복제한다. `target/` 빌드 산출물은 복제하지 않는다. 복제본의 `shell.config.json`에는 입력된 loopback origin을, `capabilities/product-shell.json`에는 같은 origin의 `/*` 패턴을 주입한 뒤 임시 프로젝트에서 `npx tauri dev --no-dev-server`를 실행한다.

Rust의 `include_str!("../shell.config.json")`와 capability 고정 구조를 복제본에 반영하므로 제품 원본을 덮어쓰지 않는다. 외부 주소·자격증명이 들어간 URL은 거부하고 loopback(`127.0.0.1`, `localhost`, `::1`)만 허용한다. SIGINT/SIGTERM 시 자식 프로세스를 종료하고 임시 트리를 삭제한다.

# 검증

- Tauri 실제 실행: 성공
- Rust 빌드: 성공(임시 복제본, macOS)
- 실행 로그: `url=http://127.0.0.1:5176/`, 허용 navigation, page load finished 확인
- `cargo test --all-targets`: 45 passed, 0 failed
- `node --check frontend/scripts/run-tauri-local.mjs`: 성공
- `git diff --check`: 성공
- 종료 후 `strong-hajin-tauri-local-*` 임시 디렉터리 잔존 없음
- 운영 `frontend/src-tauri/shell.config.json` 및 `capabilities/product-shell.json`: 실행 중 수정하지 않음

# 제약

이번 검증은 셸이 로컬 페이지를 실제 창으로 열고 로드하는 것까지다. Windows 실행, 설치파일, 서명, 운영 origin, 로그인, Release는 다루지 않는다. 마이크 권한과 녹음 절전 시나리오는 창을 띄운 뒤 별도 수동 E2E가 필요하다.

Tauri 최초 실행은 임시 Cargo 트리에서 의존성을 다시 컴파일하므로 약 40초가 걸렸다. 반복 실행 때도 임시 트리를 새로 만들기 때문에 같은 빌드 비용이 발생한다.
