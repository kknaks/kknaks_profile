---
type: decision
id: DEC-003
title: "cc PoC 배포 — k8s_infra_mac · ccc.medisolveai.xyz"
status: accepted
product: cc-prototype
feature: cc
created_at: 2026-10-13
updated_at: 2026-10-13
tags:
  - product/cc-prototype
  - feature/cc
  - doc/decision
  - status/accepted
links:
  baselines: []
  decisions:
    - "[[decision-001-feature-lab|DEC-001]]"
    - "[[decision-002-cc-poc|DEC-002]]"
  specs:
    - "[[spec-001-cc-poc|SPEC-001]]"
  works: []
  releases: []
  related: []
---

# cc PoC 배포 — k8s_infra_mac · ccc.medisolveai.xyz

## Decision

| ID | 결정 | 근거 |
|---|---|---|
| D-01 | 배포처 = `k8s_infra_mac`(MediSolveAIDev) 클러스터 — mediness · strong-hajin 과 같은 곳. back · front 둘 다 쿠버네티스 | 사용자 「여기에 배포할 거라서 … 프론트 백엔드 다 쿠버네티스로」 (DEC-001 OQ-001 닫음) |
| D-02 | 도메인 **`ccc.medisolveai.xyz`** — Cloudflare Tunnel → ingress-nginx. `/api` → back, 나머지 → front(같은 출처 — CORS · WS · SSE 단순) | 사용자 「ccc.medisolveai.xyz 로」 |
| D-03 | **접근 제한 없음**(공개) — 시드의 사람 이름 · 이메일을 전부 가짜로 바꾼 뒤 올린다 | 사용자 「접근제한도 문제 없잖아」 · 「이름 이메일만 바꿔」 (DEC-001 OQ-002 닫음) |
| D-04 | 시드 데이터: **직원 이름 · 이메일을 가짜로**(고객 이름은 이미 가짜), JSON 안에 그 직원 이름이 나오면 같이 바꾼다. 그 밖의 글(메모 원문 · 「어시 지민」 같은 표기)은 그대로. DEC-002 D-09 「가짜는 고객명뿐」 → 「사람 이름 · 이메일은 가짜」 | 사용자 「직원 이름 바꾸고 JSON 에서 해당 직원 이름 있으면 바꿔 … 이름 이메일만」 |
| D-05 | 시나리오 · 직원 데이터는 **이미지 · git 에 넣지 않는다**(앱 레포가 public) — 클러스터 Secret 으로 마운트 | 코디(레포 public 확인 2026-10-13) |
| D-06 | 이미지 = GitHub Actions(`kknaksss/cc-prototype`) arm64 → GHCR, 태그 = 커밋 sha. ArgoCD 첫 착지는 수동 sync | strong-hajin 선례 · infra 역할 규칙 |
| D-07 | Soniox 키 · 데이터 Secret · DNS(`cloudflared tunnel route dns`) 는 코디/사용자가 클러스터 밖에서 넣는다(커밋 금지) | infra 규칙 |

## 위험

- 공개 주소라 누구나 통역(Soniox 과금)을 쓸 수 있다 — 시연 뒤 내리거나 접근 제한 추가
