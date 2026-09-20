# Work Index

규칙: `para/projects/project.md`

> 현재 구현, QA, 릴리즈 상태를 추적하는 map이다. 상세 work 실행 본문은 `30-work/` 아래 1 파일 = 1 work로 둔다.
> `Status Board`는 실행 상태의 owning view다. Spec Coverage는 work frontmatter `links.specs`를 spec 중심으로 펼친 derived view다.

최종 수정: 2026-09-21

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
| 1–8 | [WORK-001 업무 생성·즉시 배정](work-001-task-creation.md) | SPEC-001/002의 W1 | review | kknaks | 미산정 | 미정 | `kknaksss/strong-hajin-work` | 사용자 E2E 미수행 | 사용자 E2E 확인 |
| 0–8 | [WORK-002 업무 v2·MyWork 개편](work-002-task-lifecycle-v2.md) | BE·FE 통합 | review | kknaks | 자동검증 완료 | 2026-09-17 목표 | `kknaksss/strong-hajin-work` | 자동검증 완료 · 브라우저 E2E 사용자 수행 · OQ-203·206 해당 경로 답 대기 | Node20 make verify·PG 77건·FE713건 완료 |
| 1–7 | [WORK-003 참조 읽음·선행업무·만들기 창 프레임](work-003-inbox-predecessor-and-create-frame.md) | SPEC-001의 D-19·D-20·D-21 | todo | kknaks | 미산정 | 미정 | `kknaksss/strong-hajin-work` | 없음 (OQ-M은 Phase 3의 한 조각만 gate) | WP 검수 → BE·FE 병렬 발주 |
| BE1–FE2 | [WORK-004 캘린더 시간 배정](work-004-calendar-scheduling.md) | SPEC-004 전절 (BE·FE 직렬) | todo | kknaks | 미산정 | 미정 | `kknaksss/strong-hajin-calendar` | 없음 (WARN-A는 FE-2의 한 줄) | WP 검수 → Phase BE-1 발주 |

## Work List

work 문서를 만들거나 상태, owner, branch, 다음 작업이 바뀌면 이 표를 갱신한다.

| ID | Title | Type | Owner | Status | Progress | File | Covers Spec |
|---|---|---|---|---|---|---|---|
| WORK-001 | 업무 생성·즉시 배정 | new-feature | kknaks | review | 90% | [work-001-task-creation.md](work-001-task-creation.md) | SPEC-001 · SPEC-002 |
| WORK-002 | 업무 v2·MyWork 개편 | new-feature | kknaks | review | 자동검증 완료 | [본문](work-002-task-lifecycle-v2.md) | SPEC-003 · SPEC-001 · SPEC-002 |
| WORK-003 | 참조 읽음·선행업무·만들기 창 프레임 | new-feature | kknaks | todo | 0% | [본문](work-003-inbox-predecessor-and-create-frame.md) | SPEC-001 |
| WORK-004 | 캘린더 시간 배정 | new-feature | kknaks | todo | 0% | [본문](work-004-calendar-scheduling.md) | SPEC-004 |

## Spec Coverage

각 spec이 어느 work에서 구현되며 현재 진척이 어떤지 한눈에 보는 spec-centric view다. Covering Work의 Status를 종합한 derived view다.

| Spec | Covering Work | 구현 상태 |
|---|---|---|
| SPEC-001 | WORK-001 · WORK-002 · WORK-003 | W1 review. W2 미착수. 참조 읽음·선행업무·만들기 창 프레임은 WORK-003 todo |
| SPEC-002 | WORK-001 · WORK-002 | 신규 수락 제거·AX 확인 보존 review. 완료 승인·문의 미착수 |
| SPEC-003 | WORK-002 | 계획·BE·FE 구현 및 자동검증 완료, OQ-203·206 답 대기 |
| SPEC-004 | WORK-004 | 계약 검수 4회 PASS. WP todo — Phase BE-1 발주 대기 |

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
