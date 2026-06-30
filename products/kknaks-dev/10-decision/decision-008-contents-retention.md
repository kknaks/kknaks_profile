---
type: decision
id: KDEV-DEC-008
title: "contents 잔류 — YouTube 요약 파이프라인은 그래프 무관(algorithms 병렬)"
status: accepted
product: kknaks-dev
created_at: 2026-06-30
updated_at: 2026-06-30
tags:
  - product/kknaks-dev
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions:
    - "[[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
  works: []
  releases: []
  related: []
---

# contents 잔류 — YouTube 요약 파이프라인은 그래프 무관 (ADR-008)

`persona/contents/`를 지식 파이프라인(reference/posts)으로 해체하려던 DEC-002 조항을 철회하고, `persona/algorithms/`처럼 **그래프 무관 잔류**로 확정한다. 코드 현실 조사 결과 contents는 외부자료 정리가 아니라 live YouTube 요약 전용 파이프라인이었다.

> [[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]]의 contents 해체 조항(L35 전제·L54 C-001 삭제)을 부분 supersede한다. DEC-002 코어(inbox/reference/permanent/posts 루트 층)는 유지.

## Context

- 관련 baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- DEC-002 L35는 `persona/contents/` 22개 중 21개를 "외부 자료 정리(참고노트)"로 전제하고 reference 종착·C-001 삭제를 결정했다. **이 전제가 코드 현실과 불일치**한다.
- 코드 현실 조사(2026-06-30, admin):
  - 파일 실태: C-001=테스트 픽스처(`/api/contents/C-001`), C-002~C-022=`-pending` 스텁(enrich 잡 대기). "21개 외부자료 정리"는 실재하지 않음.
  - 전용 파이프라인 강결합: `app/back/service/jobs/content_enrich.py`(scan_pending→LLM enrich), `api/routers/contents.py`(`/api/contents`·`/{id}`), FE `/contents`(목록·상세·landing-preview·topnav), `main_job.py` git-diff 추적.
  - type=content는 별도 dict 키(`contents`)로 로드되어 `_build_graph_nodes`에 **전달되지 않음** → 지식그래프 노드 아님(`persona_loader.py`: contents/career/daily는 persona-내부 enrich 비대상).
  - C-019~C-022 최근 실투입 = **live**.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 해체(DEC-002 원안) | contents→reference/posts 마이그레이션 | 파이프라인 일원화 명분 | 작동 중인 YouTube 요약 파이프라인 파손, 외부자료 전제가 허위 | 기각 |
| **잔류(algorithms 병렬)** | type=content 유지, 그래프 비대상, 코드 무변경 | live 파이프라인 보존, 이동 0·리스크 0 | 루트 지식층과 분리된 채 공존 | **채택** |

## Decision

- 채택:
  - `persona/contents/` **잔류** — `persona/algorithms/`와 동일 클래스(그래프 무관, 개인 배치 산출물).
  - `type=content` 유지, 지식그래프 노드 **비대상**(현 코드 그대로).
  - **C-001 유지**(test_routers fixture — `/api/contents/C-001`). DEC-002 L54 "C-001 삭제" 철회.
  - 코드·파일 이동·삭제 **0**.
- 기각: contents→reference/posts 해체 마이그레이션(DEC-002 contents 조항).

## Rationale

- 판단 기준: 문서가 코드 현실을 따른다(spec grounding 원칙). DEC-002의 "외부자료 21개" 전제는 grep으로 반증됨.
- 대안 대비 이유: 해체 시 작동 중인 파이프라인(잡·라우터·FE 9개)이 파손되고 얻는 이득 ≈ 0. algorithms를 잔류로 둔 DEC-002 L53과 동일 논리.
- 리스크: 없음(코드 무변경). 잔류라 enforcement(WORK-007) L5 orphan 대상도 아님(type=content는 지식 노드 아님).

## Scope

- In: contents 잔류 확정 + DEC-002 contents 조항 정정 + SPEC-001 디렉토리 레이아웃 반영.
- Out: `/posts` 라우트·loader·FE 배선 → **연기**(실 발행물 0개, YAGNI). graph 스키마는 post type 선반영돼 있어 첫 발행물 시 별도 work.
- 영향을 받는 spec: [[spec-001-directory-structure|KDEV-SPEC-001]] (contents 잔류 명시).

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 첫 발행물(permanent→글) 생길 때 `/posts` 배선 | | 별도 work |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-001-directory-structure|KDEV-SPEC-001]] | update | §4 디렉토리 레이아웃에 contents 잔류(algorithms 병렬) 반영 |
