---
sot: here
status: active
---

# Interpret PWA

상담사와 외국인 환자가 기기 하나를 가운데 두고 쓰는 **실시간 통역 PWA** PoC. 한국어 ↔ 외국어 양방향
음성 통역이고, 피부과 시술 용어는 **우리 용어집 시드**(`back/seed/glossary.json` — 처음 한 번 Procedure Hub 에서
가져옴 · DEC-001 D-33)를 Soniox 번역 용어로 넣어 직역을 막는다. cc-prototype 의 통역(sts)에서 떼어 새 레포로 세웠다.
앱 이름 **통키(Tongky)**.

## 코드 위치

| 항목 | 경로 |
|---|---|
| 코드 레포 | `https://github.com/kknaksss/interpret-pwa`(private) · 로컬 `/Users/kknaks/git/toy_pr2/interpret-pwa` (DEC-001 D-01) — `back/`(FastAPI · uv) · `front/`(Next.js PWA) |
| 용어집 정본 | 코드 레포 `back/seed/glossary.json`(시드 PR 로 고친다 → 재배포 · D-33) |
| 배포 | **https://tongky.medisolveai.xyz** — infra `MediSolveAIDev/k8s_infra_mac`(`charts/interpret-pwa` · ns `interpret-pwa-prod` · ArgoCD 수동 sync) · 이미지 `ghcr.io/kknaksss/interpret-pwa-{back,front}:<sha>` (D-26) |
| 시안 | Claude Design 캔버스 「Interpret PWA」 https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd (화면 정본 · D-20) · 로컬 사본 코드 레포 `design/` |

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | BASE-001 raw | — |
| Decision | DEC-001 accepted · D-01 ~ **D-34** | — |
| Spec | SPEC-001 **0.4.1** draft | D-34 구현 뒤 대조 |
| Work | WORK-001 in-progress — WP1 ~ WP10 완료(WP7 건너뜀) · WP11 재배포 완료 · 폰 확인 중 · **WP12(D-34 시작 오버레이 언어 단추) 진행 중** | WP12 → 재배포 · 사용자 폰 확인 · 시드 PR 숙제(zh-Hant 현지명 · 美版/韩版 구어 별칭) |
| 배포 | 4차 — 코드 main `9befd18`(PR #1 ~ #4) · infra PR #25 ~ #28 · 데모 로그인 켬 | WP12 재배포 |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | [입력](00-baseline/README.md) |
| 10-decision | [결정](10-decision/README.md) |
| 20-spec | [스펙](20-spec/README.md) |
| 30-work | [구현 계획](30-work/README.md) |

## 최근 로그

- 2026-10-27: 용어집을 우리 시드로(D-33 · 4차 배포 main 9befd18) · 시작 오버레이 언어 단추(D-34) 진행 중. [전체 이력](log.md)
- 2026-10-26: 제품 착수. 사용자 대화를 BASE-001 로, 대화에서 닫은 것을 DEC-001(proposed)로. 빈 레포 `kknaksss/interpret-pwa` 생성. [전체 이력](log.md)
