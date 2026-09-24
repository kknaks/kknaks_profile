---
sot: here
status: active
---

# Strong Hajin

개인 프로젝트로 이어가는 회의·업무 워크스페이스. 현재 업무 페이지 요구사항과 스펙 초안을 검수 중이다.

## 코드 레포

| 항목 | 경로 |
|---|---|
| Remote | `https://github.com/kknaks/Strong_hajin.git` |
| Local clone | `/Users/kknaks/git/toy_pr2/Strong_hajin` |
| 문서 SoT | `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin` |

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | raw 4건 | BASE-004 는 조사 2건을 사실로 눕혔다 |
| Decision | proposed 4건 · accepted 1건 | **DEC-004 결정 39건** · 뒤집힌 것 둘(D-12·D-31) |
| Spec | **6건** | SPEC-005 **v0.2.0** — 2루프 계약 반영·검수 통과 · **미결 4건**(OQ-604~607) |
| Work | WORK-005·006 구현 진행 | Tauri 로컬 셸과 웹 배선 구현 · 운영 배포는 미완료 |

데스크톱 래핑: [DEC-005](10-decision/decision-005-tauri-wrapper.md) 방향 확정. [SPEC-006](20-spec/spec-006-tauri-wrapper.md) v0.2.3: macOS·Windows, Mac Studio FE·BE, 코드 Releases 설치파일·프로필 릴리즈 문서 확정. [WORK-006](30-work/work-006-tauri-wrapper.md)에 따라 로컬 Tauri 셸·웹 배선·빌드 관문까지 구현했다. 로컬 실행은 [RUNBOOK-001](70-runbook/runbook-001-local-tauri.md), 환경별 현재 상태는 [환경 구성](40-architecture/deploy/environments.md)을 따른다. 운영 주소·PRODUCTION 로그인·인프라 배포와 설치파일 발행은 아직 완료되지 않았다.

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | [입력](00-baseline/README.md) |
| 10-decision | [결정](10-decision/README.md) |
| 20-spec | [스펙](20-spec/README.md) |
| 30-work | [구현 계획](30-work/README.md) |
| 40-architecture | [환경과 배포 구조](40-architecture/README.md) |
| 70-runbook | [반복 실행 절차](70-runbook/README.md) |

## 최근 로그

- 2026-09-22: **Phase 0 닫힘**(`make verify` exit 0) · E2E 1차 후 **2루프 계약 개정**(결정 38건 · SPEC v0.2.0). 코드 미착수. [전체 이력](log.md)
- 2026-09-21: 「프로젝트」 화면 — 조사 2건, 결정 27건 확정. 간트 재귀 트리 · 손자 프로젝트 종속 · 배정 시 자동 초대. [전체 이력](log.md)
- 2026-09-15: 업무 페이지 초안 4건 작성, 검수 시작. [전체 이력](log.md)
