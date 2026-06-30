---
type: work
id: KDEV-WORK-006
title: "contents 잔류 확정 (마이그레이션 철회) + 문서 정정"
status: done
product: kknaks-dev
work_type: doc-correction
owner: "product-curator"
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 100
created_at: 2026-06-30
updated_at: 2026-06-30
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions:
    - "[[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]]"
    - "[[decision-008-contents-retention|KDEV-DEC-008]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
  works:
    - "[[work-005-migrate-notes|KDEV-WORK-005]]"
  releases: []
  related: []
---

# contents 잔류 확정 (마이그레이션 철회) + 문서 정정

원래 WORK-006은 "contents → reference/posts 분기 마이그레이션"이었으나, **코드 현실 조사로 전제가 오판이었음이 드러났다**: `persona/contents/`는 21개 외부자료 노트가 아니라 **live YouTube 요약 전용 파이프라인**이다(C-019~022 최근 실투입, `content_enrich.py` 잡, `/api/contents`·`/contents` FE, youtubeId/day 전용 구조). admin 결정(2026-06-30): **contents는 `algorithms`처럼 잔류**(D-007 병렬, 그래프 무관). 따라서 WORK-006은 마이그레이션이 아니라 **문서 정정**이다. 코드·파일 이동 0.

> 비목표: enforcement(WORK-007), 시각화(WORK-008/009), **/posts 배선**(실데이터 0개 → 연기, 첫 발행물 생길 때 별도 work), 데이터 정제.

## Meta

- Baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Covers/corrects spec: [[spec-001-directory-structure|KDEV-SPEC-001]] (contents 잔류 명시)
- Supersedes(부분): [[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]]의 contents 해체 조항 → 신규 DEC-008
- Depends on work: [[work-005-migrate-notes|KDEV-WORK-005]]
- Follow-up work: WORK-007(enforcement — 이제 004·005만 의존, 006 마이그레이션 없음), (향후) posts 배선 work
- External dependency: 없음

## 근거 (코드 현실)

- contents 22개: C-001=테스트(youtubeId 릭롤), C-002~C-022=`-pending` 스텁(enrich 잡 대기). "21개 외부자료 정리"(DEC-002 L35)는 **실재하지 않음**.
- 전용 파이프라인 강결합: `content_enrich.py`(scan_pending→LLM enrich), `api/routers/contents.py`(`/api/contents`·`/{id}`), FE 9개(`/contents` 목록·상세·landing-preview·topnav), `main_job.py:77` git-diff.
- contents는 현재 지식그래프 `_nodes`에 **미포함**(type=content는 `_build_graph_nodes`에 전달 안 됨) → 잔류해도 그래프 무관(algorithms와 동일).
- C-019~C-022 최근 실투입 = **live**. 해체 시 작동 파이프라인 파손, 이득 ≈ 0.

## Work Summary

| Field | Value |
|---|---|
| Type | doc-correction (마이그레이션 철회) |
| Owner | product-curator (products/ 문서) + admin (PLAN-003 hub) |
| Status | done (products/ 문서) — PLAN-003 hub 정정은 admin 별도 추적 |
| Progress | 100% |
| Branch/PR | feat/knowledge-graph |
| Blocker | - |
| Next | WORK-007 enforcement ON (004·005만 의존) |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| curator | product-curator | DEC-008 신설 + DEC-002 amend + SPEC-001 정정 + 30-work README/log | done |
| admin | admin | PLAN-003 hub(D-006/008/S1/S6) 정정 | done (claude_pr, 비-git 파일) |

> 코드 워커 없음. 순수 문서. C-001 삭제 안 함(test_routers fixture — `/api/contents/C-001`).

## Scope

포함 (문서만):
- **DEC-008 신설**: "contents 잔류(D-007 병렬, live 파이프라인)" 결정 — 근거·OQ 해소.
- **DEC-002 amend**: contents 해체 조항 4곳(L35 전제·L50 reference 종착·L54 C-001 삭제·L66 scope) → DEC-008 포인터로 정정. inbox/reference/permanent/posts 루트 층 코어는 유지.
- **SPEC-001 정정**: §4 디렉토리 레이아웃에 `persona/contents/ # 그래프 무관, 잔류`(algorithms 병렬) 추가. §6 AC의 "notes/contents 재편" → "notes 재편(contents 잔류)".
- **30-work README**: WORK-006 행 재정의(migration→doc-correction), Spec Coverage SPEC-001 `006 contents 잔류 확정`, 의존 메모(007는 004·005만).
- **log.md**: WORK-006 엔트리.

제외:
- 코드·파일 이동·삭제 0 (C-001 포함 무삭제).
- /posts 라우트·loader·FE 배선 → **연기**(실데이터 0, YAGNI. graph 스키마는 post type 선반영돼 있어 첫 발행물 시 별도 work).

## Execution

### Phase 1 — DEC-008 신설 + DEC-002 amend (curator)
- **Status**: DONE
- DEC-008 신설(contents 잔류, 근거=live 파이프라인·algorithms 병렬·그래프 미포함). DEC-002 contents 조항 4곳(L35 전제·L50 reference 종착·L54 C-001 삭제·L66 scope) 정정 + DEC-008 링크. 10-decision/README 인덱스에 DEC-008 추가.

### Phase 2 — SPEC-001 + 30-work + log (curator)
- **Status**: DONE
- SPEC-001 §4(contents 잔류 추가)/§6(AC 정정), version 0.0.2→0.0.3. 30-work README WORK-006 행 재정의·Spec Coverage·의존 흐름(007=004·005). log 엔트리. product_doc_pipeline errors 0.

### Phase 3 — PLAN-003 hub 정정 (admin)
- **Status**: DONE
- D-006/D-008에 ⚠정정 블록(contents 잔류, 오판 명시), S1 구조에 `contents/ 잔류` 추가 + 소멸 리스트 정정, S6 로드맵(notes만 이동·contents 잔류·posts 연기) 정정. (claude_pr hub = 비-git, 파일 수정)

## Pre-deploy Check

- [x] 코드·파일 이동 0 (마이그레이션 아님 — git status 전부 products/kknaks-dev 내부)
- [x] C-001 무삭제(fixture 보존)
- [x] product_doc_pipeline errors 0
- [x] /posts 배선 미착수(연기 — 문서에 명시)

## Rollback

- 문서 정정이라 revert 1회. 코드 영향 0.

## Done Criteria

- [x] DEC-008 신설 + DEC-002 contents 조항 정정(DEC-008 링크)
- [x] SPEC-001 §4/§6에 contents 잔류 반영
- [x] 30-work README WORK-006 재정의 + Spec Coverage, log 엔트리
- [x] PLAN-003 hub 정정(admin)
- [x] pipeline 통과, 코드/파일 무변경 확인

## Open Issues

- /posts 배선(loader 키·라우터·FE) 연기 — 첫 발행물(permanent→글) 생길 때 별도 work. graph는 post type 선반영(준비됨).
- 데이터 정제(Day01·copy·평문 links)는 여전히 후속 별도 work(WORK-005 §Open Issue).

## Related

- Decision: [[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]] (부분 supersede → DEC-008)
- Spec: [[spec-001-directory-structure|KDEV-SPEC-001]]
- Work: [[work-005-migrate-notes|KDEV-WORK-005]]
