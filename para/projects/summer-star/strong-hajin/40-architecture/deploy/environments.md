---
type: architecture
title: Strong Hajin 환경 구성
status: current
created_at: 2026-09-24
updated_at: 2026-10-01
tags: [product/strong-hajin, architecture/deploy]
---

# Strong Hajin 환경 구성

## 환경 현황

| 환경 | 상태 | 구성 |
|---|---|---|
| 로컬 웹 | 사용 가능 | PostgreSQL `54329` · API `8001` · Vite `5176` · 워커 4개 |
| 로컬 Tauri | 사용 가능 | 로컬 웹 전체를 먼저 띄운 뒤 Tauri가 `http://127.0.0.1:5176`을 연다 |
| Mac Studio 운영 | **가동** (2026-10-01) | `https://ax.medisolveai.xyz` — Kubernetes(ns `strong-hajin-prod`) + Argo CD(수동 sync) + Cloudflare Tunnel, 같은 origin에서 `/`, `/api/`, WebSocket을 경로 분기. 시드 4명 |
| 데스크톱 앱 (macOS) | 서명·공증본 전달 | 회사판 `medi-ax`(`app.ax.desktop`) dmg — Developer ID 서명·공증. 개인판 `Strong Hajin` 은 origin 미정 |
| 설치파일 게시 | 미발행 | GitHub Releases 발행 전. dmg 는 직접 전달했다. Windows 는 아직 없다 |
| 릴리즈 문서 | 준비 중 | 이 프로젝트의 `60-release/`에서 버전별 기록 |

## 로컬 구조

`make local-stack`이 PostgreSQL, API, 프론트엔드와 conversation·material·meeting·report 워커를 함께 감독한다. Tauri는 이 스택에 포함되지 않는다. 두 번째 터미널에서 `make tauri-local`을 실행한다. 이 명령은 운영 설정을 바꾸지 않고 임시 Rust 프로젝트에 loopback origin만 넣는다.

실행 원장은 [RUNBOOK-001](../../70-runbook/runbook-001-local-tauri.md)이다. 기계가 읽을 명령과 포트는 `orchestration/config/projects/strong-hajin.json`의 `local_dev`에 둔다.

## 운영 구조

Mac Studio Kubernetes에 프론트엔드와 백엔드를 함께 올렸다(2026-10-01). 배포·재배포 절차는 [RUNBOOK-002](../../70-runbook/runbook-002-production-deploy.md), 결정은 [DEC-007](../../10-decision/decision-007-production-deploy.md)에 있다.

```text
사용자 / medi-ax 앱
  → https://ax.medisolveai.xyz   (Cloudflare → cloudflared → ingress-nginx)
      ├ /                         → front (nginx + SPA)
      ├ /api/* · /health          → back (FastAPI)
      └ /api/meetings/* WebSocket → back

ns strong-hajin-prod: back · front · worker-{conversation,material,meeting,report} · postgres-0 · redis-0
```

세션 쿠키와 WebSocket 인증을 유지하려면 프론트와 API가 같은 HTTPS origin을 써야 한다. Vercel은 현재 구조에 필요하지 않다.

| 항목 | 값 |
|---|---|
| 이미지 | `ghcr.io/kknaksss/strong-hajin-{back,front}:<sha>-arm64` — `deploy/k8s/*.Dockerfile`. 첫 배포 태그 `cdb0f3f-arm64` |
| 차트·앱 | `MediSolveAIDev/k8s_infra_mac` — `charts/strong-hajin` · `charts/datastores/values-strong-hajin.yaml` · Argo `strong-hajin-prod`·`strong-hajin-datastores`(automated 끔) · AppProject `strong-hajin` |
| 시크릿(값은 레포 밖) | `ghcr-pull` · `postgres-secret` · `strong-hajin-secret`(`SONIOX_API_KEY` · `TDL_EMAIL` · `TDL_PASSWORD`) |
| 저장 | postgres PVC 10Gi · redis PVC 2Gi · codex-home PVC · hostPath `/mnt/mac/strong-hajin/{recordings,materials}`(= Mac Studio `~/mediness-data/strong-hajin`) |
| AX | 노드 `/opt/codex`(0.146.0)·`/opt/claude` 읽기 전용 마운트 + Strong Hajin 전용 codex 인증 |

Mediness와는 namespace·Argo 앱·차트·DB/PVC·이미지가 모두 따로다. 공유 리소스 변경은 cloudflared hosts 한 줄과 DNS 레코드 하나뿐이다.

## 해소 기록 — 「아직 배포할 수 없는 이유」 일곱

2026-09-24 에 적어 둔 차단 일곱 가지가 어디서 닫혔는지 남긴다. 닫히지 않은 부분은 아래 「남은 것」으로 옮겼다.

| # | 차단 | 상태 | 어디서 |
|---|---|---|---|
| 1 | 운영 호스트 이름 | 닫힘 — `ax.medisolveai.xyz` | DEC-007 D-03 · DNS route |
| 2 | PRODUCTION 로그인 수단 | 닫힘 — 이메일/비밀번호를 프로파일과 무관하게 연다 | DEC-007 D-01 · 코드 PR #5 |
| 3 | 레지스트리 namespace · 회사 인프라 저장소 사용 범위 | 닫힘 — `ghcr.io/kknaksss` · `MediSolveAIDev/k8s_infra_mac` 에 새 차트·앱 | DEC-007 D-04·D-05 · infra PR #5 |
| 4 | arm64 이미지 · chart/Application · 실제 배포 | 닫힘 — 이미지 `cdb0f3f-arm64`, 파드 8/8, `/` 200 | 코드 PR #5 · infra PR #5·#6 · Argo 수동 sync(2026-10-01) |
| 5 | Tauri 운영 origin · 아이콘 · 서명·공증 · Windows | **macOS 는 닫힘**(origin PR #7 · 아이콘 PR #6 · 두 판 PR #8 · 회사판 공증). Windows 는 남음 | DEC-007 D-09·D-10 |
| 6 | 쿠키 유지 · 원격 IPC · 녹음 절전 방지 실측 | **남음** — 서버 쪽 로그인·STT·회의실·AX 턴은 실측했다. 앱 재시작 후 쿠키 유지(M-5)는 사용자 확인 대기, 원격 IPC·절전 방지 실측 기록은 없다 | `report-infra-deploy.md` §7·§A·§B · `report-fe-flavors.md` §7 |
| 7 | GitHub Releases 발행 | **남음** | — |

세부 설계 근거는 `orchestration/work/_archive/strong-hajin/strong-hajin-projects/tauri-deploy-design.md` 에 있다.

## 남은 것

| 항목 | 상태 |
|---|---|
| 로그인 시도 제한 | 없다 — 운영 로그인에 무차별 대입 방어가 없다(DEC-007 OQ-D7-01) |
| M-5 앱 재시작 후 로그인 유지 | 사용자 확인 대기 — 확인 전에는 최종 관문(preflight)이 막혀 있다 |
| 개인판 origin | 미정 — 개인판은 「서버 주소가 설정되지 않았습니다」 화면 |
| 운영 DB 의 실명 시드 | 실명·회사 메일이 운영 DB 에 있다. 백업·접근 정책 미정(DEC-007 OQ-D7-04) |
| 백업 | 주기·보관 위치 미정 |
| 노드 codex 0.146 | AX 턴은 동작, 기록 필드(observed_model 등)가 빈다. 업그레이드는 mediness 와 공유라 사용자 결정 |
| Argo automated sync | 꺼 둠 — 수동 sync 가 안정적으로 돈 뒤 켠다 |
| TLS 인증서 | Cloudflare 엣지 인증서 만료 2026-11-28 — 자동 갱신 가정, 미확인 |
| Windows 설치파일 · GitHub Releases · `60-release` | 없음 |
| canonical `k8s_infra_mac` 체크아웃의 untracked Strong Hajin 파일 | 머지된 것과 같은 출발본 — 사용자가 정리 |

