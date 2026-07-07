# 30-work

## WP Map

| WP | Work | 범위 | Covers | 선행 | Status |
|---|---|---|---|---|---|
| WP0 | AXKG-WORK-001 | 모노레포 scaffold + migration + auth + AI 실행 골격 | AXKG-SPEC-008, 011(골격) | — | **done** |
| WP1 | AXKG-WORK-002 | Source Inbox + 수집 adapter + 요약 | AXKG-SPEC-003, 012, 011① | WP0 | todo |
| WP2 | AXKG-WORK-003 | parser + documents/edges 캐시 + retriever + 그래프 뷰 | AXKG-SPEC-005 | WP0 | todo |
| WP3 | AXKG-WORK-004 | 분류·문서화 게이트 + Apply Executor | AXKG-SPEC-001, 002, 004, 011②③ | WP1+WP2 | todo |
| WP4 | AXKG-WORK-005 | Graph RAG Chat | AXKG-SPEC-006, 011④ | WP2 | todo |
| WP5 | AXKG-WORK-006 | 설정 (Provider·Prompts·Templates) | AXKG-SPEC-007, 009, 010 | WP0 | todo |

WP1·WP2는 병렬 가능, WP3는 둘 다 선행 필요, WP4/WP5 병렬 가능.

**FE 공통 기준**: 모든 WP의 FE 화면은 `21-html/` 시안이 기준이다 — 레이아웃·컴포넌트 구조뿐 아니라 **UI 카피(한국어 문구)까지 시안을 따른다.** 영어 placeholder 카피 금지.

## Status Board

| ID | Title | Status | Spec |
|---|---|---|---|
| AXKG-WORK-001 | WP0: 모노레포 scaffold와 실행 골격 | done | AXKG-SPEC-008, AXKG-SPEC-011 |
| AXKG-WORK-002 | WP1: Source Intake — 수신·수집·요약 | todo | AXKG-SPEC-003, AXKG-SPEC-012, AXKG-SPEC-011① |
| AXKG-WORK-003 | WP2: 문서·그래프 코어 | todo | AXKG-SPEC-005 |
| AXKG-WORK-004 | WP3: 승인 게이트 — 분류·문서화·Apply Executor | todo | AXKG-SPEC-001, 002, 004, AXKG-SPEC-011②③ |
| AXKG-WORK-005 | WP4: Graph RAG Chat | todo | AXKG-SPEC-006, AXKG-SPEC-011④ |
| AXKG-WORK-006 | WP5: 설정 | todo | AXKG-SPEC-007, 009, 010 |

## Spec Coverage

| Spec | Covered by | Status |
|---|---|---|
| AXKG-SPEC-003 | AXKG-WORK-002 (WP1) | planned |
| AXKG-SPEC-001 | AXKG-WORK-004 (WP3) | planned |
| AXKG-SPEC-002 | AXKG-WORK-004 (WP3) | planned |
| AXKG-SPEC-004 | AXKG-WORK-004 (WP3) | planned |
| AXKG-SPEC-005 | AXKG-WORK-003 (WP2) | planned |
| AXKG-SPEC-006 | AXKG-WORK-005 (WP4) | planned |
| AXKG-SPEC-007 | AXKG-WORK-006 (WP5) | planned |
| AXKG-SPEC-008 | AXKG-WORK-001 (WP0) | done |
| AXKG-SPEC-009 | AXKG-WORK-006 (WP5) | planned |
| AXKG-SPEC-010 | AXKG-WORK-006 (WP5) | planned |
| AXKG-SPEC-011 | AXKG-WORK-001(골격 done) + 002①·004②③·005④(스테이지 planned) | in-progress |
| AXKG-SPEC-012 | AXKG-WORK-002 (WP1) | planned |
