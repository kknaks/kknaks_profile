# Spec Index

규칙: `para/projects/project.md`

> 기능, UX, 정책, acceptance criteria 계약으로 들어가는 map이다. 상세 계약은 `20-spec/` 아래 사용자 기능/정책 묶음 단위의 spec 파일로 둔다.
> 본문은 contract만 다룬다. 구현 진척·work 매핑은 `30-work/README.md`, 결정 로그는 `10-decision/README.md`, 변경 이력은 `log.md`, 리뷰 artifact는 `00-baseline/`, 내부 구조는 `40-architecture/`를 본다.

최종 수정: 2026-09-22

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
| 프로젝트 | SPEC-005 | 아래 Spec List |
| 데스크톱 래퍼 | SPEC-006 | 아래 Spec List |

## Spec List

spec 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다. work 진행률, owner, blocker, PR은 `30-work/README.md`로 보낸다.

| ID | Title | Area | Status | Decision | File |
|---|---|---|---|---|---|
| SPEC-001 | 업무 관리 | 업무 | draft | DEC-001 | [본문](spec-001-work-management.md) |
| SPEC-002 | 답하면 끝나는 목록 | 판단 | draft | DEC-001 | [본문](spec-002-action-item-review.md) |
| SPEC-003 | 업무 생명주기 v2·MyWork UX | 업무·판단 | draft | DEC-002 | [본문](spec-003-task-lifecycle-v2.md) |
| SPEC-004 | 캘린더 시간 배정 | 캘린더 | draft | DEC-003 | [본문](spec-004-calendar-scheduling.md) |
| SPEC-005 | 「프로젝트」 화면 — 재귀 간트·의존선·소속과 참여 (v0.2.0: 생성 모달·상태 변경·체크리스트 읽기 범위) | 프로젝트 | draft | DEC-004 | [본문](spec-005-projects.md) |
| SPEC-006 | 데스크톱 래퍼 — 웹은 그대로 두고, 녹음하는 동안만 잠들지 않는 창 | 데스크톱 | draft | DEC-005 | [본문](spec-006-tauri-wrapper.md) |

> **SPEC-004 는 2루프(v0.3.0)에서 `§1 Scope Out` 한 줄이 뒤집혔다** — 「회의 도메인의 변경 —
> 기간 파라미터 외에는 손대지 않는다」. **회의 생성·시각 변경에 겹침 검증이 붙는다**
> (DEC-003 증보 8 `K22`). 회의 도메인을 읽는 다른 spec 이 생기면 그 사실을 먼저 본다.

## Reading Order

| Area | Spec |
|---|---|
| 업무 → 판단 | SPEC-003의 대체 범위 확인 → 유지되는 SPEC-001·SPEC-002 |

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|
| OQ 목록 | 각 spec의 Open Questions 참조 | 코디·리뷰어 | 검수 후 정리 |

SPEC-006: v0.2.3 사용자 배포 결정 반영(macOS·Windows, Mac Studio, 코드 Releases·프로필 릴리즈 문서). 세부 미결·구현 실측 미완으로 draft 유지.
