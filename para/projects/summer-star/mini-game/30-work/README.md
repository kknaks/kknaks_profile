# Work Index

규칙: `para/projects/project.md`

> 현재 구현, QA, 릴리즈 상태를 추적하는 map이다. 첫 작업은 프론트 게임 구현부터 시작한다.

최종 수정: 2026-07-14

Status 값: `todo`, `in_progress`, `blocked`, `review`, `done`

## Domain / Schema 관리 원칙

- Work는 구현 중 필요한 DDD 초안과 schema 가정을 적는 자리다.
- 실제 Supabase schema/RLS는 후속 work 또는 architecture에서 확정한다.
- 이번 work는 `/Users/kknaks/git/toy_pr2/lunch_game` 프론트 레포의 모바일 게임 구현을 우선한다.

## Status Board

| Phase | Work | Scope | Status | Owner | 예상 기간 | 목표 완료 | PR/Branch | Blocker | Next |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [WORK-001 Front yut gauge MVP](work-001-front-yut-gauge-mvp.md) | SPEC-001, SPEC-002 | done | TBD | TBD | 2026-07-14 | - | Supabase env는 실제 저장 work 전 필요 | Supabase persistence work 작성 |

## Work List

| ID | Title | Type | Owner | Status | Progress | File | Covers Spec |
|---|---|---|---|---|---|---|---|
| WORK-001 | Front yut gauge MVP | new-feature | TBD | done | 100% | [work-001-front-yut-gauge-mvp.md](work-001-front-yut-gauge-mvp.md) | SPEC-001, SPEC-002 |

## Spec Coverage

| Spec | Covering Work | 구현 상태 |
|---|---|---|
| SPEC-001 | WORK-001 | done |
| SPEC-002 | WORK-001 | done |

## Release Gate

### Scope

- [x] 릴리즈 대상 spec이 정해졌다.
- [x] 포함/제외 범위가 decision/spec과 맞다.

### Code

- [x] 연결된 제품 구현이 로컬 트리에 반영됐다.
- [ ] 필요한 migration/환경변수/외부 설정이 반영됐다.

### Spec

- [x] 필요한 `20-spec/README.md` / `20-spec/` 변경이 작성됐다.
- [x] blocker open question이 없다.

### Baseline / UX

- [x] 필요한 baseline artifact가 연결됐다.
- [ ] Known UX issue는 Product/Design이 승인했다.

### QA

- [x] `npm run build`가 통과했다.
- [x] blocking fail이 없다.

### Approval

- [ ] Product
- [ ] QA
- [ ] Tech Lead
