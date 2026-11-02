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
| Baseline | raw **7건** | BASE-005 는 조사 3건을 사실로 눕혔다 · BASE-007 회의 생성·편집 피드백 정리 |
| Decision | proposed **5건** · accepted 1건 | **DEC-004 결정 39건** · 뒤집힌 것 둘(D-12·D-31) · **DEC-006 결정 20건 · 미결 0건** |
| Spec | **7건** | SPEC-007 **v0.2.0** — 검수 반영·미결 판정 완료 · **열린 미결 1건**(OQ-709) |
| Work | WORK-005·006 구현 진행 · **WORK-007 todo** | Tauri 로컬 셸과 웹 배선 구현 · 운영 배포는 미완료 · WORK-007 은 **BE Phase B-1 발주 대기** |

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

## 운영 개선 목록

운영 화면에서 발견한 버그와 고도화 항목은 [개선 목록](improvements/README.md)에서 상태와
다음 조치를 계속 관리한다. 현재 피드백의 원문은 BASE-007에 보존한다.

## 최근 로그

- 2026-09-28: **업무 상세 재설계** — 확정 시안(`TaskDetail.html` A·B·C)과 조사 셋 위에 BASE-005·DEC-006·SPEC-007·WORK-007 넷. **후행은 저장하지 않고 같은 표를 반대로 읽는다**, 상위 변경을 열고 V-8 파급을 거절한다. 검수 반영으로 **기존 계약 여섯 줄 대체**를 §7.2 에 전수 등록하고 미결 여덟을 닫았다. 코드 미착수. [전체 이력](log.md)
- 2026-09-22: **Phase 0 닫힘**(`make verify` exit 0) · E2E 1차 후 **2루프 계약 개정**(결정 38건 · SPEC v0.2.0). 코드 미착수. [전체 이력](log.md)
- 2026-09-21: 「프로젝트」 화면 — 조사 2건, 결정 27건 확정. 간트 재귀 트리 · 손자 프로젝트 종속 · 배정 시 자동 초대. [전체 이력](log.md)
- 2026-09-15: 업무 페이지 초안 4건 작성, 검수 시작. [전체 이력](log.md)
