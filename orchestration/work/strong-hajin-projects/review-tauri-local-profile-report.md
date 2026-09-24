---
title: Review — Tauri local profile
status: complete
updated: 2026-09-23
---

# 종합 판정 — FAIL 1 · WARN 1

로컬 Tauri 프로파일은 현재 로컬 스택의 프론트 주소와 맞고, 실제로 임시 Rust 트리를
컴파일해 `http://127.0.0.1:5176/`을 Tauri 창에서 로드했다. 운영 셸 파일은 실행 전후
변경되지 않았고, 외부 origin은 거부된다. 다만 구현이 허용한다고 명시한 `::1` loopback은
Node의 `URL.hostname`이 `[::1]`을 반환하는 환경에서 거부된다. 문서화된 허용 입력과 실제
동작이 어긋나므로 FAIL로 판정한다.

## 1. 검수 범위와 실행 환경

- 코드: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
- 대상: `frontend/scripts/run-tauri-local.mjs`, 루트 `Makefile`의 `tauri-local`,
  `tauri-local-profile-report.md`
- 검수 방식: read-only. 제품 코드·셸 설정·인프라·보고서 원본은 수정하지 않았다.
- 현재 로컬 스택 주소: `http://127.0.0.1:5176` (Makefile의 `E2E_FRONTEND_PORT ?= 5176`)

## 2. 판정표

| 항목 | 판정 | 근거 |
|---|---|---|
| `make tauri-local`이 올바른 작업 디렉터리에서 스크립트를 호출 | PASS | `make -n tauri-local`이 `cd frontend && node scripts/run-tauri-local.mjs`를 출력 |
| 기본 origin이 현재 local-stack 주소와 일치 | PASS | 스크립트 기본값과 Makefile 프론트 포트 모두 `http://127.0.0.1:5176` |
| 실제 Tauri 실행·웹 페이지 로드 | PASS | 직접 실행에서 임시 Rust 트리 컴파일 완료, `Running target/debug/strong-hajin-shell`, `url=http://127.0.0.1:5176/`, `allowed origin`, `load finished` 확인 |
| 운영 `shell.config.json`·`product-shell.json` 보호 | PASS | 복제본에만 origin·remote URL을 기록하는 구현이며, 원본은 실행 후에도 `operationalOrigin: null`, `.invalid` capability를 유지 |
| 임시 트리 정리 | PASS | SIGTERM 종료 뒤 `strong-hajin-tauri-local-*` 임시 디렉터리 잔존 없음 확인 |
| 외부 origin·경로·credential 거부 | PASS | 외부 도메인, 경로, query/hash, credential, `file:` 각각 exit 2로 거부 |
| `localhost`, `127.0.0.1` 허용 | PASS | 기본값 및 `TAURI_LOCAL_ORIGIN=http://localhost:5176` 경로가 검증 규칙에 부합 |
| Rust 회귀 시험 | PASS | `cargo test --all-targets`: 45 passed, 0 failed |
| `::1` 허용 | FAIL | 코드 allowlist는 `::1`을 선언하지만 Node에서 `new URL('http://[::1]:5176').hostname`이 `[::1]`이어서 실제 입력이 exit 2 |

## 3. FAIL

### F-1 — 문서화된 IPv6 loopback `::1`이 실제로 거부됨

`run-tauri-local.mjs:27`은 허용 호스트를 `127.0.0.1`, `localhost`, `::1`로
설명하고 검사한다. 그러나 Node URL 표준 파싱에서 IPv6 loopback URL의 hostname은
`[::1]`이다.

재현:

```text
$ TAURI_LOCAL_ORIGIN=http://[::1]:5176 node frontend/scripts/run-tauri-local.mjs
tauri-local: TAURI_LOCAL_ORIGIN is local-only (use 127.0.0.1, localhost, or ::1)
exit=2
```

따라서 보고서의 “`::1` 허용”과 구현의 실제 입력 집합이 불일치한다. 수정 시 URL
hostname을 대괄호 포함 형태로 비교하거나 canonical loopback 판정을 별도로 두고,
IPv6 입력을 다시 실행해 임시 트리의 capability URL과 페이지 로드까지 확인해야 한다.

## 4. 직접 확인한 실행 증거

### 4-1. 실제 Tauri 로컬 실행

```text
tauri-local: opening http://127.0.0.1:5176
tauri-local: disposable Rust tree .../strong-hajin-tauri-local-*/src-tauri
Running DevCommand (`cargo run ...`)
Finished `dev` profile
Running `target/debug/strong-hajin-shell`
[shell][boot] ... url=http://127.0.0.1:5176/
[shell][nav] ... allowed origin=http://127.0.0.1:5176
[shell][load] ... finished url=http://127.0.0.1:5176/
```

실행은 약 49초 동안 임시 트리에서 Rust 의존성을 빌드한 뒤 성공했다. 실제 창을 닫는
대신 검수 프로세스에 SIGTERM을 보내 종료·정리를 확인했다. 애플리케이션 수동 조작,
마이크 권한, 녹음 절전 시나리오는 이번 검수에 포함하지 않았다.

### 4-2. 주소 검증

외부 도메인(`https://example.com`), URL 경로, query/hash, credential 포함 URL,
`file:` 및 `localhost.evil`은 모두 exit 2였다. 기본 주소는 local-stack의
`E2E_FRONTEND_PORT=5176`과 일치한다.

### 4-3. Rust 시험

`frontend/src-tauri`에서 다음을 직접 실행했다.

```text
cargo test --all-targets
test result: ok. 45 passed; 0 failed
```

## 5. WARN

### W-1 — 각 실행마다 임시 Rust 의존성 빌드 비용이 큼

`target/`을 복사하지 않고 매번 새 임시 트리를 만들기 때문에 첫 실행과 반복 실행 모두
컴파일 비용이 발생한다. 현재 보고서에는 약 40초로 기록되어 있고, 이번 실행은 약 49초였다.
정확한 기능 실패는 아니며, 로컬 반복 개발에서는 예상 대기 시간으로 안내하면 된다.

## 6. 기존 Makefile 영향과 보호 확인

- `tauri-local`은 `.PHONY`에 등록되어 있다.
- 기존 `local-stack`, `frontend`, `shell-verify`, `shell-final-preflight` 레시피를
  변경하지 않고 새 타깃만 추가했다.
- `make -n tauri-local`은 프론트 디렉터리로 이동한 뒤 스크립트를 실행한다.
- 스크립트는 `src-tauri`를 임시 디렉터리에 복사하고, `target/`은 제외한다.
- 임시 복사본의 `shell.config.json`과 `capabilities/product-shell.json`만 수정한다.
- `npx --prefix frontend --no-install tauri dev --no-dev-server`로 실행하므로
  실행 중 dev server를 새로 만들지 않고 이미 떠 있는 `127.0.0.1:5176`을 사용한다.
- 운영 origin, 로그인, 설치파일, 서명, Release, Windows는 이번 검수의 통과 대상이 아니다.

## 7. 후속 조치

F-1을 먼저 수정하고 다음을 재검증한다.

1. `TAURI_LOCAL_ORIGIN=http://[::1]:5176`이 통과하는지 확인한다.
2. capability의 remote URL이 정규화된 IPv6 origin과 일치하는지 확인한다.
3. IPv6 로컬 서버에서 실제 Tauri navigation/load를 확인한다.
4. `cargo test --all-targets`, 외부 origin 거부, 임시 트리 cleanup, 원본 설정 불변을 반복한다.

F-1은 현재 사용 중인 기본 `127.0.0.1` 경로를 막지는 않지만, 구현이 공개한 허용 범위의
일부가 동작하지 않으므로 수정 전 최종 승인으로 넘기지 않는다.
