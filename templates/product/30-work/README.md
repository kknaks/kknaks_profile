# Work Index

규칙: `rules/product-doc-pipeline.md`

> 현재 구현, QA, 릴리즈 상태를 추적하는 map이다. 상세 work 실행 본문은 `30-work/` 아래 1 파일 = 1 work로 둔다.
> `Status Board`는 실행 상태의 owning view다. Spec Coverage는 work frontmatter `links.specs`를 spec 중심으로 펼친 derived view다.

최종 수정: YYYY-MM-DD

Status 값: `todo`, `in_progress`, `blocked`, `review`, `done`

## Domain / Schema 관리 원칙

- Work는 구현 중 필요한 DDD 초안과 schema 가정을 적는 자리다.
- 실제 table schema, column, index, FK, migration 전문은 제품 코드/migration이 source of truth다.
- `30-work/`에는 aggregate boundary, 상태/invariant, migration 필요 여부, 코드 위치 후보만 적는다.
- 같은 invariant가 여러 work에 반복되거나 onboarding용 도메인 지도가 필요해지면 optional architecture 문서로 승격한다.
- SPEC에는 사용자/프론트/QA/외부 연동에 드러나는 resource, status, enum, API 계약만 환류한다.

## Status Board

| Phase | Work | Scope | Status | Owner | 예상 기간 | 목표 완료 | PR/Branch | Blocker | Next |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [WORK-001 <Work 제목>](work-001-<slug>.md) | SPEC-001 | todo | TBD | TBD | TBD | - | - | 첫 PR 생성 |

## Work List

work 문서를 만들거나 상태, owner, branch, 다음 작업이 바뀌면 이 표를 갱신한다.

| ID | Title | Type | Owner | Status | Progress | File | Covers Spec |
|---|---|---|---|---|---|---|---|
| WORK-001 | <Work 제목> | new-feature | TBD | todo | 0% | [work-001-<slug>.md](work-001-<slug>.md) | SPEC-001 |

## Spec Coverage

각 spec이 어느 work에서 구현되며 현재 진척이 어떤지 한눈에 보는 spec-centric view다. Covering Work의 Status를 종합한 derived view다.

| Spec | Covering Work | 구현 상태 |
|---|---|---|
| SPEC-001 | WORK-001 | todo |

## Release Gate

### Scope

- [ ] 릴리즈 대상 spec이 정해졌다.
- [ ] 포함/제외 범위가 decision/spec과 맞다.

### Code

- [ ] 연결된 제품 PR이 merge됐다.
- [ ] 필요한 migration/환경변수/외부 설정이 반영됐다.

### Spec

- [ ] 필요한 `20-spec/README.md` / `20-spec/` 변경이 리뷰됐다.
- [ ] blocker open question이 없다.

### Baseline / UX

- [ ] 필요한 baseline artifact가 연결됐다.
- [ ] Known UX issue는 Product/Design이 승인했다.

### QA

- [ ] 필요한 QA case가 실행됐다.
- [ ] blocking fail이 없다.

### Approval

- [ ] Product
- [ ] QA
- [ ] Tech Lead
- [ ] 범위, 벤더 경로, 정책, 비용, 일정, 고객 약속이 바뀐 경우 Decision Owner
