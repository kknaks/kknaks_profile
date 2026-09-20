# Spec Index

규칙: `para/projects/project.md`

> 기능, UX, 정책, acceptance criteria 계약으로 들어가는 map이다. 상세 계약은 `20-spec/` 아래 사용자 기능/정책 묶음 단위의 spec 파일로 둔다.
> 본문은 contract만 다룬다. 구현 진척·work 매핑은 `30-work/README.md`, 결정 로그는 `10-decision/README.md`, 변경 이력은 `log.md`, 리뷰 artifact는 `00-baseline/`, 내부 구조는 `40-architecture/`를 본다.

최종 수정: 2026-09-20

## Data / Domain Boundary

SPEC에는 Product, QA, frontend, 외부 연동자가 알아야 하는 도메인 용어와 API 계약만 둔다.

- SPEC에 둠: 사용자-facing 용어, API request/response에 드러나는 resource/status/enum, 외부 lifecycle, acceptance criteria.
- SPEC에 두지 않음: table schema 전문, column/index/FK, ORM model 전체, repository/service 구조, lock/idempotency 구현 상세.
- 구현 중 DDD 초안은 해당 work의 `Domain / Schema` 섹션에 둔다.
- 실제 schema의 source of truth는 제품 코드와 migration이다.
- 여러 spec/work가 공유하는 장기 domain invariant는 `40-architecture/`에 둔다.

## Scope

### In Scope

- 업무 관리 및 판단 목록 계약 초안. 상세 범위는 각 spec에서 관리한다.

### Out Of Scope

- 코드 실행 계획과 진척은 스펙 검수 후 30-work에서 관리한다.

## Terms

| 용어 | 의미 |
|---|---|
| 용어 정의 | 각 spec의 Context와 Data Contract 참조 |

## Spec Bundle

| 묶음 | 포함 Spec | 파일 |
|---|---|---|
| 업무 | SPEC-003 · SPEC-001 · SPEC-002 | 아래 Spec List |
| 캘린더 | SPEC-004 | 아래 Spec List |

## Spec List

spec 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다. work 진행률, owner, blocker, PR은 `30-work/README.md`로 보낸다.

| ID | Title | Area | Status | Decision | File |
|---|---|---|---|---|---|
| SPEC-001 | 업무 관리 | 업무 | draft | DEC-001 | [본문](spec-001-work-management.md) |
| SPEC-002 | 답하면 끝나는 목록 | 판단 | draft | DEC-001 | [본문](spec-002-action-item-review.md) |
| SPEC-003 | 업무 생명주기 v2·MyWork UX | 업무·판단 | draft | DEC-002 | [본문](spec-003-task-lifecycle-v2.md) |
| SPEC-004 | 캘린더 시간 배정 | 캘린더 | draft | DEC-003 | [본문](spec-004-calendar-scheduling.md) |

## Reading Order

| Area | Spec |
|---|---|
| 업무 → 판단 | SPEC-003의 대체 범위 확인 → 유지되는 SPEC-001·SPEC-002 |

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|
| OQ 목록 | 각 spec의 Open Questions 참조 | 코디·리뷰어 | 검수 후 정리 |
