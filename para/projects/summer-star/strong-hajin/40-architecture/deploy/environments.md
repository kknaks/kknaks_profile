---
type: architecture
title: Strong Hajin 환경 구성
status: current
created_at: 2026-09-24
updated_at: 2026-09-24
tags: [product/strong-hajin, architecture/deploy]
---

# Strong Hajin 환경 구성

## 환경 현황

| 환경 | 상태 | 구성 |
|---|---|---|
| 로컬 웹 | 사용 가능 | PostgreSQL `54329` · API `8001` · Vite `5176` · 워커 4개 |
| 로컬 Tauri | 사용 가능 | 로컬 웹 전체를 먼저 띄운 뒤 Tauri가 `http://127.0.0.1:5176`을 연다 |
| Mac Studio 운영 | 설계 중 | Kubernetes + Argo CD + Cloudflare Tunnel, 같은 origin에서 `/`, `/api/`, WebSocket을 경로 분기 |
| 설치파일 배포 | 준비 중 | macOS·Windows 설치파일을 Strong_hajin 코드 저장소의 GitHub Releases에서 배포 |
| 릴리즈 문서 | 준비 중 | 이 프로젝트의 `60-release/`에서 버전별 기록 |

## 로컬 구조

`make local-stack`이 PostgreSQL, API, 프론트엔드와 conversation·material·meeting·report 워커를 함께 감독한다. Tauri는 이 스택에 포함되지 않는다. 두 번째 터미널에서 `make tauri-local`을 실행한다. 이 명령은 운영 설정을 바꾸지 않고 임시 Rust 프로젝트에 loopback origin만 넣는다.

실행 원장은 [RUNBOOK-001](../../70-runbook/runbook-001-local-tauri.md)이다. 기계가 읽을 명령과 포트는 `orchestration/config/projects/strong-hajin.json`의 `local_dev`에 둔다.

## 운영 구조

목표는 Mac Studio Kubernetes에 프론트엔드와 백엔드를 함께 올리는 것이다.

```text
사용자 / Tauri
  → https://<운영 호스트>
      ├ /              → frontend nginx
      ├ /api/*         → FastAPI
      └ WebSocket 경로 → FastAPI

FastAPI → PostgreSQL + conversation/material/meeting/report workers
```

세션 쿠키와 WebSocket 인증을 유지하려면 프론트와 API가 같은 HTTPS origin을 써야 한다. Vercel은 현재 구조에 필요하지 않다.

GitOps 대상은 `/Users/kknaks/git/harness_works/k8s_infra_mac`이며 Mediness의 서버 접속 방식만 참고한다. Strong Hajin은 별도 namespace, Argo CD Application, chart, DB/PVC와 이미지 태그를 사용한다. 공유 Mediness 리소스는 수정하지 않는다.

## 아직 배포할 수 없는 이유

운영 배포는 아직 완료되지 않았다.

1. 운영 호스트 이름 확정
2. PRODUCTION 로그인 수단 확정 — 현재 API 라우트는 등록되지만 세션을 발급할 로그인 경로가 없다
3. 컨테이너 레지스트리 namespace 및 회사 인프라 저장소 사용 범위 확정
4. arm64 백엔드·프론트 이미지, Strong Hajin chart/Application 작성과 실제 배포
5. Tauri 운영 origin 반영, macOS 아이콘·서명·공증, Windows 빌드·서명 준비
6. 운영 서버에서 쿠키 유지, 원격 문서 IPC, 녹음·절전 방지 실측
7. 검증된 설치파일을 코드 저장소 GitHub Releases에 발행

세부 설계 근거는 `orchestration/work/strong-hajin-projects/tauri-deploy-design.md`에 있다. 반복 가능한 실제 배포 명령은 구현이 끝난 뒤 `70-runbook/`에 별도 런북으로 확정한다.

