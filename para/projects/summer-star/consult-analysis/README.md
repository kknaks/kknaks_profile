---
sot: here
status: active
---

# Consult Analysis

피부과 클리닉 인스타그램 DM(상담) 내보내기를 분석해 **문의 → 예약표 발송 → 예약 회신** 흐름과
고객 구성을 보는 개인 분석 프로젝트. 원본은 Meta 「Download your information」 내보내기다.

규칙: [[para/projects/project|para/projects/project.md]]

## 위치

| 항목 | 경로 |
|---|---|
| 원본 데이터 | `reference/2026-11-16-linky-data/` — **gitignore** (고객 DM · 사진 · 1.8G) |
| 스크립트 | `para/projects/summer-star/consult-analysis/scripts/` (파서 · 적재) |
| 로컬 DB | `para/projects/summer-star/consult-analysis/data/` — SQLite · **gitignore** |

> 이 레포는 PUBLIC 이다. 문서 · 스크립트 · 커밋에 고객 이름 · 메시지 본문 · 사진을 넣지 않는다.
> 수치(건수 · 비율)와 구조만 쓴다.

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | BASE-001 · BASE-002 raw | — |
| Decision | DEC-001 · DEC-002 accepted | — |
| Spec | SPEC-001 0.2.1 accepted | SPEC-002 2층 |
| Work | WORK-001 done (verify 274/274 · 시험 38 · 검수 PASS) | WORK-002 2층 |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | [[para/projects/summer-star/consult-analysis/00-baseline/README\|00-baseline/README.md]] |
| 10-decision | [[para/projects/summer-star/consult-analysis/10-decision/README\|10-decision/README.md]] |
| 20-spec | [[para/projects/summer-star/consult-analysis/20-spec/README\|20-spec/README.md]] |
| 30-work | [[para/projects/summer-star/consult-analysis/30-work/README\|30-work/README.md]] |

<!-- work-links:start -->
## 작업 기록

[[para/projects/summer-star/consult-analysis/work-index|진행 중·완료된 작업 목록]]
<!-- work-links:end -->
