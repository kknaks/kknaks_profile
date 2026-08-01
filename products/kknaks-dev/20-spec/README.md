# Spec Index

규칙: `rules/product-doc-pipeline.md`

## Spec 목록

| ID | Title | Status | Decision | Coverage | Work |
|---|---|---|---|---|---|
| KDEV-SPEC-001 | 지식그래프 디렉토리 구조 (4층 + concept) | draft | DEC-001/002/008/010/015 | WORK-013 | WORK-013 (todo) |
| KDEV-SPEC-002 | 그래프 스키마 (노드·layer·식별자·엣지·산출물) | draft | DEC-003/004/010 | WORK-013 | WORK-013 (todo) |
| KDEV-SPEC-003 | 지식 워크플로 (4층 생명주기 · 승인 기반 정제) | draft | DEC-005(개정)/010/011/015 | WORK-013 | WORK-013 (todo) |
| KDEV-SPEC-004 | 그래프 검증 게이트 L1~L6 (층별 판정 · 발행 전 검증) | draft | DEC-006/010/012 | WORK-013·015 | WORK-013·015 (todo) |
| KDEV-SPEC-005 | 지식 열람 표면 — 트리 문서 렌더러와 공개 경계 | draft | DEC-007(대체)/010 | — | (미발주) |
| KDEV-SPEC-006 | 관리자 인증 — 로그인/세션/admin 진입 | implemented | DEC-009 | WORK-011 | WORK-011 (done) |
| KDEV-SPEC-007 | 승인 큐 — 지식 입력 접수와 항목 상태기계 | draft | DEC-011/012/013 | WORK-012·014 | WORK-012·014 (todo) |
| KDEV-SPEC-008 | 게이트 체인 — 파이프라인 정의와 스테이지 계약 | draft | DEC-010/011/016 | WORK-014·015 | WORK-014·015 (todo) |
| KDEV-SPEC-009 | 게이트 피드백과 재생성 — 버전·resume·supersede | draft | DEC-011/012 | WORK-014 | WORK-014 (todo) |
| KDEV-SPEC-010 | Apply Executor — 발행 계획 검증과 원자적 발행 | draft | DEC-010/012/013/016 | WORK-015 | WORK-015 (todo) |
| KDEV-SPEC-011 | 커밋 조사 — 레포 레지스트리와 로컬 git 수집 | draft | DEC-014 | — | (미발주) |
| KDEV-SPEC-012 | 잔디 산출물 — daily·career·concept 계약 | draft | DEC-015 | — | (미발주) |
| KDEV-SPEC-013 | 잔디 승인 게이트 — daily_commit 파이프라인과 발행 | draft (v0.0.2) | DEC-016 | WORK-017 | WORK-017 (in_progress) |

## 읽는 순서

| 묶음 | 문서 | 무엇을 다루나 |
|---|---|---|
| 지식 구조 | SPEC-001 → 002 → 004 → 005 | 어디에 두나 · 어떻게 잇나 · 무엇을 막나 · 어떻게 읽나 |
| 워크플로 | SPEC-003 | 노트가 어떻게 흐르나 (구현체 = 게이트 체인) |
| 승인 파이프라인 | SPEC-007 → 008 → 009 → 010 | 접수 → 체인 → 피드백 → 발행 |
| 잔디 파이프라인 | SPEC-011 → 012 → 013 | 무엇을 조사하나 · 무엇이 되나 · 어떻게 승인·발행되나 |
| 인증 | SPEC-006 | admin 진입 |
