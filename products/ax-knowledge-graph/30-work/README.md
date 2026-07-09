# 30-work

## WP Map

| WP | Work | 범위 | Covers | 선행 | Status |
|---|---|---|---|---|---|
| WP0 | AXKG-WORK-001 | 모노레포 scaffold + migration + auth + AI 실행 골격 | AXKG-SPEC-008, 011(골격) | — | **done** |
| WP1 | AXKG-WORK-002 | Source Inbox + 수집 adapter + 요약 | AXKG-SPEC-003, 012, 011① | WP0 | **done** (코드 완료 기준·라이브 잔여 있음) |
| WP2 | AXKG-WORK-003 | parser + documents/edges 캐시 + retriever + 그래프 뷰 | AXKG-SPEC-005 | WP0 | **in-progress** (P1~3 BE done, P4 그래프 뷰 FE 잔여) |
| WP3 | AXKG-WORK-004 | 분류·문서화 게이트 + Apply Executor | AXKG-SPEC-001, 002, 004, 011②③ | WP1+WP2 | **in-progress** (P1 분류 게이트 done·라이브, P2 문서화 게이트 발주, 분류 게이트 FE 선착수) |
| WP4 | AXKG-WORK-005 | Graph RAG Chat | AXKG-SPEC-006, 011④ | WP2 | **done** (P1~3 코드 done·라이브 e2e 완료 2026-07-09) |
| WP5 | AXKG-WORK-006 | 설정 (Provider·Prompts·Templates) | AXKG-SPEC-007, 009, 010 | WP0 | **done** |

WP1·WP2는 병렬 가능, WP3는 둘 다 선행 필요, WP4/WP5 병렬 가능.

**FE 공통 기준**: 모든 WP의 FE 화면은 `21-html/` 시안이 기준이다 — 레이아웃·컴포넌트 구조뿐 아니라 **UI 카피(한국어 문구)까지 시안을 따른다.** 영어 placeholder 카피 금지.

## Status Board

| ID | Title | Status | Spec |
|---|---|---|---|
| AXKG-WORK-001 | WP0: 모노레포 scaffold와 실행 골격 | done | AXKG-SPEC-008, AXKG-SPEC-011 |
| AXKG-WORK-002 | WP1: Source Intake — 수신·수집·요약 | done | AXKG-SPEC-003, AXKG-SPEC-012, AXKG-SPEC-011① |
| AXKG-WORK-003 | WP2: 문서·그래프 코어 | in-progress | AXKG-SPEC-005 |
| AXKG-WORK-004 | WP3: 승인 게이트 — 분류·문서화·Apply Executor | in-progress | AXKG-SPEC-001, 002, 004, AXKG-SPEC-011②③ |
| AXKG-WORK-005 | WP4: Graph RAG Chat | done | AXKG-SPEC-006, AXKG-SPEC-011④ |
| AXKG-WORK-006 | WP5: 설정 | done | AXKG-SPEC-007, 009, 010 |

## Spec Coverage

| Spec | Covered by | Status |
|---|---|---|
| AXKG-SPEC-003 | AXKG-WORK-002 (WP1) | done |
| AXKG-SPEC-001 | AXKG-WORK-004 (WP3) | in-progress (분류 게이트 done, 문서화·재분류 잔여) |
| AXKG-SPEC-002 | AXKG-WORK-004 (WP3) | in-progress (게이트 공통·버전·분류 done, 문서화 게이트 잔여) |
| AXKG-SPEC-004 | AXKG-WORK-004 (WP3) | in-progress (문서화 게이트 Phase 2 발주) |
| AXKG-SPEC-005 | AXKG-WORK-003 (WP2) | in-progress (BE 계약 done, U-2 그래프 뷰 FE 잔여) |
| AXKG-SPEC-006 | AXKG-WORK-005 (WP4) | done (세션/run API + chat 배선 + FE 패널, 라이브 e2e 완료 2026-07-09) |
| AXKG-SPEC-007 | AXKG-WORK-006 (WP5) | done (AI Provider 설정 API) |
| AXKG-SPEC-008 | AXKG-WORK-001 (WP0) | done |
| AXKG-SPEC-009 | AXKG-WORK-006 (WP5) | done (Prompts API — 버전/롤백/스키마 검증) |
| AXKG-SPEC-010 | AXKG-WORK-006 (WP5) | done (Templates API — 버전/롤백) |
| AXKG-SPEC-011 | AXKG-WORK-001(골격 done) + 002①(done) + 004②(done)·004③(in-progress)·005④(done) | in-progress (004③ 잔여) |
| AXKG-SPEC-012 | AXKG-WORK-002 (WP1) | done |
