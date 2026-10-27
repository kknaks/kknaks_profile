---
sot: here
status: active
---

# Interpret PWA

상담사와 외국인 환자가 기기 하나를 가운데 두고 쓰는 **실시간 통역 PWA** PoC. 한국어 ↔ 외국어 양방향
음성 통역이고, 피부과 시술 용어는 **우리 용어집 시드**(`back/seed/glossary.json` — 처음 한 번 Procedure Hub 에서
가져옴 · DEC-001 D-33 · 대만 현지명 반영 D-35)를 Soniox 번역 용어로 넣어 직역을 막는다. 용어집은 back 안에서만 쓰고
밖으로는 통역에 필요한 최소 정보만 낸다(D-37). 「자동 듣기 / 누르고 말하기」 모드가 있다(D-36). cc-prototype 의 통역(sts)에서 떼어 새 레포로 세웠다.
앱 이름 **통키(Tongky)**.

## 코드 위치

| 항목 | 경로 |
|---|---|
| 코드 레포 | `https://github.com/kknaksss/interpret-pwa`(private) · 로컬 `/Users/kknaks/git/toy_pr2/interpret-pwa` (DEC-001 D-01) — `back/`(FastAPI · uv) · `front/`(Next.js PWA) |
| 용어집 정본 | 코드 레포 `back/seed/glossary.json`(시드 PR 로 고친다 → 재배포 · D-33 · 화면 메뉴 없음 — D-37) |
| 배포 | **https://tongky.medisolveai.xyz** — infra `MediSolveAIDev/k8s_infra_mac`(`charts/interpret-pwa` · ns `interpret-pwa-prod` · ArgoCD 수동 sync) · 이미지 `ghcr.io/kknaksss/interpret-pwa-{back,front}:<sha>` (D-26) |
| 시안 | Claude Design 캔버스 「Interpret PWA」 https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd (화면 정본 · D-20) · 로컬 사본 코드 레포 `design/` |

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | BASE-001 raw | — |
| Decision | DEC-001 accepted · D-01 ~ **D-37**(D-13 · D-32 뒤집힘) | — |
| Spec | SPEC-001 **0.5.0** draft — 최종 배포본 fe8475e 와 대조 | — |
| Work | WORK-001 in-progress — WP1 ~ **WP15** 완료(WP7 건너뜀) · 운영 장애(TTS keepalive) 수정 포함 | 사람 목소리 E2E(SPEC OQ-017) |
| 배포 | **8차** — 코드 main `fe8475e`(PR #1 ~ #8 · back · front 같은 sha) · infra PR #25 ~ #33(#31 제외) · 데모 로그인 켬 | 데모 끝나면 끄기(OQ-008) · 시드 숙제(대만명 못 찾은 80 — OQ-016) |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | [입력](00-baseline/README.md) |
| 10-decision | [결정](10-decision/README.md) |
| 20-spec | [스펙](20-spec/README.md) |
| 30-work | [구현 계획](30-work/README.md) |

## 최근 로그

- 2026-10-27: D-34 ~ D-37 배포(PR #5 ~ #8 · 최종 fe8475e) — 시작 오버레이 언어 단추 · 대만 현지명 시드 + `s2tw` · **운영 끊김(TTS keepalive `{}`) 수정** · 누르고 말하기 · 용어집 API · 메뉴 삭제(최소 노출). SPEC 0.5.0. [전체 이력](log.md)
- 2026-10-27: 용어집을 우리 시드로(D-33 · 4차 배포 main 9befd18). [전체 이력](log.md)
- 2026-10-26: 제품 착수. 사용자 대화를 BASE-001 로, 대화에서 닫은 것을 DEC-001(proposed)로. 빈 레포 `kknaksss/interpret-pwa` 생성. [전체 이력](log.md)
