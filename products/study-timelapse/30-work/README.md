# Work Index

규칙: `rules/product-doc-pipeline.md`

> study-timelapse의 현재 구현, QA, 릴리즈 상태를 추적하는 map이다. 상세 work 실행 본문은 `30-work/` 아래 1 파일 = 1 work로 둔다.
> `Status Board`는 실행 상태의 owning view다. Spec Coverage는 work frontmatter `links.specs`를 spec 중심으로 펼친 derived view다.

최종 수정: 2026-06-21

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
| 1 | [STL-WORK-001 English app copy audit](work-001-english-app-copy-audit.md) | STL-SPEC-001·002·008·009·010·012 | done | kknaks | 0.5d | 2026-06-20 | TBD | - | 후속 work 선정 |
| 2 | [STL-WORK-002 Mobile Apple Sign-In integration](work-002-mobile-apple-sign-in.md) | STL-SPEC-009·008 | todo | kknaks | 1d | TBD | TBD | Apple capability / bundle id 확인 필요 | Apple capability / bundle id / Expo dependency 확인 |
| 3 | [STL-WORK-003 Session stats persistence and timezone fix](work-003-session-stats-persistence-timezone.md) | STL-SPEC-003·005·010·012·013 | todo | kknaks | 1d | TBD | TBD | 날짜 기준 결정 필요 | Asia/Seoul 자정 경계 재현 테스트 작성 |

## Work List

work 문서를 만들거나 상태, owner, branch, 다음 작업이 바뀌면 이 표를 갱신한다.

| ID | Title | Type | Owner | Status | Progress | File | Covers Spec |
|---|---|---|---|---|---|---|---|
| STL-WORK-001 | English app copy audit | polish | kknaks | done | 100% | [work-001-english-app-copy-audit.md](work-001-english-app-copy-audit.md) | STL-SPEC-001·002·008·009·010·012 |
| STL-WORK-002 | Mobile Apple Sign-In integration | new-feature | kknaks | todo | 0% | [work-002-mobile-apple-sign-in.md](work-002-mobile-apple-sign-in.md) | STL-SPEC-009·008 |
| STL-WORK-003 | Session stats persistence and timezone fix | bugfix | kknaks | todo | 0% | [work-003-session-stats-persistence-timezone.md](work-003-session-stats-persistence-timezone.md) | STL-SPEC-003·005·010·012·013 |

## Spec Coverage

각 spec이 어느 work에서 구현되며 현재 진척이 어떤지 한눈에 보는 spec-centric view다. Covering Work의 Status를 종합한 derived view다.

| Spec | Covering Work | 구현 상태 |
|---|---|---|
| STL-SPEC-001 | STL-WORK-001 | done |
| STL-SPEC-002 | STL-WORK-001 | done |
| STL-SPEC-003 | STL-WORK-003 | todo |
| STL-SPEC-005 | STL-WORK-003 | todo |
| STL-SPEC-008 | STL-WORK-001, STL-WORK-002 | todo |
| STL-SPEC-009 | STL-WORK-001, STL-WORK-002 | todo |
| STL-SPEC-010 | STL-WORK-001, STL-WORK-003 | todo |
| STL-SPEC-012 | STL-WORK-001, STL-WORK-003 | todo |
| STL-SPEC-013 | STL-WORK-003 | todo |
| STL-SPEC-004 | — (이관 전 구현) | implemented |
| STL-SPEC-006 | — (이관 전 구현) | in_dev |
| STL-SPEC-007 | — (이관 전 구현) | implemented |

> `— (이관 전 구현)` 은 **이 레포에 WP 문서가 없는** spec 이다. 2026-06-09 medi_docs
> 이관이 「계약 표면만(구현 본문 제외)」 옮겼기 때문에 구현을 담은 work 문서가 없다
> (`log.md` 2026-06-09). 추적을 빠뜨린 것이 아니므로 소급 WP 를 만들지 않는다.
> `product_doc_pipeline.py` 는 이 둘을 「커버하는 work 없음」 warning 으로 계속 보고한다.

## Release Gate

### Scope

- [ ] 릴리즈 대상 spec/work가 정해졌다.
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
