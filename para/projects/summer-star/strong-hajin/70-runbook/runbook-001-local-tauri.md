---
type: runbook
id: RUNBOOK-001
title: 로컬 웹과 Tauri 실행
status: active
created_at: 2026-09-24
updated_at: 2026-09-24
tags: [product/strong-hajin, doc/runbook, status/active]
links:
  baselines: []
  decisions: ["[[decision-005-tauri-wrapper]]"]
  specs: ["[[spec-006-tauri-wrapper]]"]
  works: ["[[work-006-tauri-wrapper]]"]
  releases: []
---

# RUNBOOK-001 — 로컬 웹과 Tauri 실행

## 목적

로컬 웹과 Tauri 앱을 같은 데이터와 API로 띄워 기능·디자인을 확인한다. 다음 세션은 이 문서만으로 재현한다.

## 작업 위치

현재 변경을 확인할 때는 해당 Strong_hajin 코드 워크트리 루트에서 실행한다. 병합된 `main`을 확인할 때는 프로젝트 설정의 `repos.code.canonical_path`를 사용하되 최신 `origin/main` 반영 여부를 먼저 확인한다.

## 최초 1회 준비

```bash
make install
make frontend-install
make postgres-up
make reset-demo
```

`make reset-demo`는 로컬 데모 데이터를 지우고 다시 만든다. 기존 데이터를 유지해야 하면 실행하지 않는다. 코드보다 스키마만 뒤처졌다면 `make sync-demo-schema`를 쓴다.

## 매일 실행

터미널 1:

```bash
make local-stack
```

`SCAX local stack ready`와 API `http://127.0.0.1:8001`, frontend `http://127.0.0.1:5176` 표시를 확인한다.

터미널 2:

```bash
make tauri-local
```

Tauri만 먼저 실행하면 흰 화면이나 연결 실패 화면이 나올 수 있다. 반드시 스택 준비 완료 후 실행한다.

## 확인

```bash
curl -fsS http://127.0.0.1:8001/api/auth/providers
curl -fsS http://127.0.0.1:5176/
```

브라우저와 Tauri는 같은 프론트와 API를 사용한다. 레이아웃·드래그앤드롭 차이는 WebView 조건으로 분리해서 확인한다.

## 종료

- Tauri: 앱 종료 또는 해당 터미널 `Ctrl+C`
- 웹 스택: `make local-stack` 터미널에서 `Ctrl+C`
- PostgreSQL까지 내릴 때만 `make postgres-down`

## 문제 해결

| 증상 | 확인·조치 |
|---|---|
| Tauri가 흰 화면 | `local-stack ready`와 `curl http://127.0.0.1:5176/` 확인 후 Tauri 재실행 |
| 스키마 부족으로 중단 | 데이터 유지 시 `make sync-demo-schema`; 버려도 되는 데모면 `make reset-demo` |
| AX 답변이 pending | conversation worker 로그 확인 |
| 자료·회의·보고가 queued | material/meeting/report worker 로그 확인 |
| 녹음 기능 없음 | `~/.config/soniox/env`와 macOS 마이크 권한 확인. 키 값은 문서나 로그에 적지 않는다 |
| 회의실 예약 기능 없음 | `~/.config/theconnect/env` 확인. 없어도 나머지 회의 기능은 동작한다 |
| 백엔드 변경이 안 보임 | 실행 중인 스택을 종료하고 다시 띄운다 |

## 운영 배포

아직 실행 가능한 운영 배포 런북은 없다. 현재 상태와 차단 항목은 [환경 구성](../40-architecture/deploy/environments.md)에 기록한다. 운영 주소·로그인·이미지·차트가 확정되고 Mac Studio에 실제 배포한 뒤 이 폴더에 `RUNBOOK-002`로 배포·검증·롤백 명령을 고정한다.

