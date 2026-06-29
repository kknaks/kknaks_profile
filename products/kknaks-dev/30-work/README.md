# Work Index

규칙: `rules/product-doc-pipeline.md`

> 적용 순서 핵심: enforcement(L1~L4 ERROR + 부팅 fail-fast)는 **WORK-007 맨 마지막**에 켠다. 그 전엔 검증기를 report-only로 둬야 라이브 서버가 안 죽는다.

## 의존 흐름

```
001 빌더+검증기(report) → 002 데이터정리 → 003 지식층 scaffold+규약
  → ┬ 004 projects→products ┐
    ├ 005 notes→reference    ┼→ 007 enforcement ON → 008 /graph → 009 로컬그래프
    └ 006 contents→ref/posts ┘
```

## Work 목록

| ID | Title | 담당 | Status | Covers Spec | Depends | File |
|---|---|---|---|---|---|---|
| WORK-001 | 그래프 빌더 수술 + 검증기(report-only) | BE | todo | SPEC-002·004 | — | `work-001-graph-builder-validator.md` |
| WORK-002 | report-only 실행 → 데이터 정리(충돌3·링크정규화) | BE | todo | SPEC-002·004 | 001 | `work-002-data-cleanup.md` |
| WORK-003 | 지식층 scaffold + 작성 규약(분류·정제·up·archive + agent.md) | BE/문서 | todo | SPEC-001·003 | 002 | `work-003-knowledge-layer-scaffold.md` |
| WORK-004 | projects → products/showcase 재편 (+라우트·inputs.py) | BE+FE | todo | SPEC-001 | 003 | `work-004-migrate-projects.md` |
| WORK-005 | notes → reference 재편 (+라우트·loader) | BE+FE | todo | SPEC-001 | 003 | `work-005-migrate-notes.md` |
| WORK-006 | contents → reference/posts 재편 (C-001 폐기 +라우트) | BE+FE | todo | SPEC-001·003 | 003 | `work-006-migrate-contents.md` |
| WORK-007 | 렌더 검증 후 enforcement ON (L1~L4 ERROR+fail-fast+CI) | BE | todo | SPEC-004 | 004·005·006 | `work-007-enforce-validation.md` |
| WORK-008 | 전역 그래프 /graph (_graph.json API + force-directed) | BE+FE | todo | SPEC-005 | 007 | `work-008-global-graph.md` |
| WORK-009 | 노트별 로컬 그래프 (이웃+백링크) | FE | todo | SPEC-005 | 008 | `work-009-local-graph.md` |

## Spec Coverage

| Spec | Covering Work | 구현 상태 |
|---|---|---|
| SPEC-001 디렉토리 | WORK-003·004·005·006 | todo |
| SPEC-002 스키마 | WORK-001·002 | todo |
| SPEC-003 워크플로 | WORK-003 (+강제: 001·007) | todo |
| SPEC-004 검증 | WORK-001·007 | todo |
| SPEC-005 시각화 | WORK-008·009 | todo |
