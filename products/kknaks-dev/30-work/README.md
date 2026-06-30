# Work Index

규칙: `rules/product-doc-pipeline.md`

> 적용 순서 핵심: enforcement(L1~L4 ERROR + 부팅 fail-fast)는 **WORK-007 맨 마지막**에 켠다. 그 전엔 검증기를 report-only로 둬야 라이브 서버가 안 죽는다.

> 마이그레이션 정합: 신규 층(reference/permanent/posts)은 현재 블로그 라우트·loader 키가 **없다** (라우트=about·algorithms·career·contents·notes·projects·print, loader 키=career·projects·notes·contents·daily·algorithms). 마이그레이션 work는 **파일 이동 + 라우트 신설/재배선 + loader 키 추가**를 atomic으로 포함한다 (이동만으로는 블로그에 안 보임).

## 의존 흐름

```
001 빌더+검증기(report) → 002 검증기 정교화(report-only) → 003 지식층 scaffold+규약
  → ┬ 004 projects→products ┐
    ├ 005 notes→reference    ┼→ 007 enforcement ON → 008 /graph → 009 로컬그래프
    └ 006 contents 잔류 확정 ┘  (006=문서정정, 마이그레이션 아님 → 007은 004·005만 의존)
```

## Work 목록

| ID | Title | 담당 | Status | Covers Spec | Depends | File |
|---|---|---|---|---|---|---|
| WORK-001 | 그래프 빌더 수술 + 검증기(report-only) | BE | done | SPEC-002·004 | — | `work-001-graph-builder-validator.md` |
| WORK-002 | 검증기 정교화 (code-fence 스킵·navigational 제외·orphan 범위, report-only) | BE | done | SPEC-002·004 | 001 | `work-002-validator-refinement.md` |
| WORK-003 | 지식층 scaffold + 작성 규약(분류·정제·up·archive + agent.md) | BE/문서 | done | SPEC-001·003 | 002 | `work-003-knowledge-layer-scaffold.md` |
| WORK-004 | projects → products/showcase 재편 (+`/projects` 라우트가 `products/*/showcase.md`를 읽도록 재배선 + loader가 products showcase 노출 + inputs.py) | BE+FE | done | SPEC-001 | 003 | `work-004-migrate-projects.md` |
| WORK-005 | notes → reference 재편 (+ reference 라우트·loader 키 신설/재정의 — `/notes` 유지 vs `/reference` 네이밍은 발주 직전 admin 결정) | BE+FE | done | SPEC-001 | 003 | `work-005-migrate-notes.md` |
| WORK-006 | contents 잔류 확정(마이그레이션 철회)+문서정정 (DEC-008 신설·DEC-002 amend·SPEC-001 정정, 코드 0, /posts 배선 연기) | 문서 | done | SPEC-001 | 003 | `work-006-migrate-contents.md` |
| WORK-007 | 렌더 검증 후 enforcement ON (L1~L4 ERROR+fail-fast+CI) — 검증=build + 모든 라우트 + `/graph` 통과 + showcase·reference 전부 매핑·에러 0 확인 | BE | todo | SPEC-004 | 004·005 | `work-007-enforce-validation.md` |
| WORK-008 | 전역 그래프 /graph (_graph.json API + force-directed) | BE+FE | todo | SPEC-005 | 007 | `work-008-global-graph.md` |
| WORK-009 | 노트별 로컬 그래프 (이웃+백링크) | FE | todo | SPEC-005 | 008 | `work-009-local-graph.md` |

## Spec Coverage

| Spec | Covering Work | 구현 상태 |
|---|---|---|
| SPEC-001 디렉토리 | WORK-003·004·005·006 | 003 scaffold done / 004 projects done / 005 notes done / 006 contents 잔류 확정 |
| SPEC-002 스키마 | WORK-001·002 | 001·002 done |
| SPEC-003 워크플로 | WORK-003 (+강제: 001·007) | 003 규약 문서화 done / 강제 007 todo |
| SPEC-004 검증 | WORK-001·002·007 | 001·002 done / 007 todo |
| SPEC-005 시각화 | WORK-008·009 | todo |
