# Database Architecture Index

규칙: `rules/product-doc-pipeline.md`

> ERD, 테이블 목록, 도메인 데이터 구조를 관리한다. migration/schema 전문은 두지 않는다.

| ID | Title | Status | File | 연결 spec |
|---|---|---|---|---|
| ARCH-002 | AI Queue State Tables | draft | [database-001-ai-queue-state.md](database-001-ai-queue-state.md) | SPEC-004, SPEC-005, SPEC-007 |
| ARCH-003 | Core Domain Tables | draft | [database-002-core-domain-tables.md](database-002-core-domain-tables.md) | SPEC-001~007 |

읽는 순서: ARCH-003(도메인 원장) → ARCH-002(AI job 상태).
