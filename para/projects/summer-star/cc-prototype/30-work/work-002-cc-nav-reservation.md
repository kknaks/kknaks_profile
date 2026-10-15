---
type: work
id: WORK-002
title: "cc 2차 구현 — 공통 헤더 · 기기별 현황판 · 예약관리 데모"
status: in-progress
product: cc-prototype
feature: cc
work_type: new-feature
owner: kknaks
progress: 100
created_at: 2026-10-14
updated_at: 2026-10-15
tags:
  - product/cc-prototype
  - feature/cc
  - doc/work
  - status/in-progress
links:
  baselines: []
  decisions:
    - "[[decision-004-cc-nav-reservation|DEC-004]]"
  specs:
    - "[[spec-002-cc-nav-reservation|SPEC-002]]"
  works:
    - "[[work-001-cc-poc|WORK-001]]"
  releases: []
  related: []
---

# cc 2차 구현 — 공통 헤더 · 기기별 현황판 · 예약관리 데모

SPEC-002 를 2026-10-16(금) 시연 전까지 넣는다.

> 1 파일 = 1 work = **빌드 계획**. 계약은 SPEC-002 를 참조만 한다.

## Meta

- Covers spec: SPEC-002
- 코드 레포: `kknaksss/cc-prototype` — 범위 `cc/front`(WP1 · WP2), `cc/back` + `cc/front`(WP4)
- slug: `cc-nav-resv` · 워커: frontend(WP1 · WP2 · WP3 시안) · backend(WP4)

## Work Packages

| WP | 내용 | 계약 | 워커 | 상태 |
|---|---|---|---|---|
| WP1 | 공통 헤더 + `/reservations` 빈 페이지 + 직군 가드 해제 | SPEC-002 §1 | frontend | 완료 |
| WP2 | 기기별 현황판 — 폰 = Aside 폭 전체(D-19) | SPEC-002 §2 | frontend | 완료 |
| WP3 | 예약관리 시안 — claude design 「Ceramique 예약관리 v1」 | DEC-004 D-10 ~ D-17 | frontend(DesignSync) | 완료 |
| WP4 | 예약관리 구현 | SPEC-002 §3 | backend · frontend | 완료 |
| fix1 ~ fix5 | E2E batch-1 ~ 5 · 기획자 피드백(BASE-007) 반영 · 시술 후보 정정 | SPEC-002 §3.3 · §4 · §5 | backend · frontend | 완료 |
| 배포 | 코드 `kknaksss/cc-prototype#2`(main 339293e) · infra `MediSolveAIDev/k8s_infra_mac#20` · 시나리오 Secret 갱신 · 배포 DB 재시드 — https://ccc.medisolveai.xyz | DEC-003 | 코디 | 완료(2026-10-15) |

## 검증

- WP 마다 `cc/front` 에서 `npx tsc --noEmit` · `npm run lint` · `npm run build`
- 완료는 사용자 표면에서 — 데스크톱 · 탭 · 폰 폭으로 화면 확인
