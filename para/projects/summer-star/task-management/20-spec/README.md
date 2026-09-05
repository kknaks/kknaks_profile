# Spec Index

규칙: `para/projects/project.md`

> 기능, UX, 정책, acceptance criteria 계약으로 들어가는 map이다. 상세 계약은 `20-spec/` 아래 사용자 기능/정책 묶음 단위의 spec 파일로 둔다.
> 본문은 contract만 다룬다. 구현 진척·work 매핑은 `30-work/README.md`, 결정 로그는 `10-decision/README.md`, 변경 이력은 `log.md`, 리뷰 artifact는 `00-baseline/`, 내부 구조는 `40-architecture/`를 본다.

최종 수정: 2026-09-01

## Data / Domain Boundary

SPEC에는 Product, QA, frontend, 외부 연동자가 알아야 하는 도메인 용어와 API 계약만 둔다.

- SPEC에 둠: 사용자-facing 용어, API request/response에 드러나는 resource/status/enum, 외부 lifecycle, acceptance criteria.
- SPEC에 두지 않음: table schema 전문, column/index/FK, ORM model 전체, repository/service 구조, lock/idempotency 구현 상세.
- 구현 중 DDD 초안은 해당 work의 `Domain / Schema` 섹션에 둔다.
- 실제 schema의 source of truth는 제품 코드와 migration이다.
- 여러 spec/work가 공유하는 장기 domain invariant는 `40-architecture/`에 둔다.

## Scope

### In Scope

- 미정 — decision 뒤에 채운다

### Out Of Scope

- 미정

## Terms

| 용어 | 의미 |
|---|---|
|  |  |

## Spec Bundle

| 묶음 | 포함 Spec | 파일 |
|---|---|---|
|  |  |  |

## Spec List

spec 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다. work 진행률, owner, blocker, PR은 `30-work/README.md`로 보낸다.

| ID | Title | Area | Status | Decision | File |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Reading Order

| Area | Spec |
|---|---|
|  |  |

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
|  |  |  |  |

## Spec 목록 (2026-09-05 v1 12건 초안 완비)

| ID | Title | Status | Decision | E2E 검증 |
|---|---|---|---|---|
| SPEC-000 | 스캐폴딩·기동 | draft | — | 앱 창이 뜨고 백엔드에 붙는다 |
| SPEC-001 | 로그인·세션 | draft | DEC-001 | 로그인하고 앱을 껐다 켜도 유지된다 |
| SPEC-002 | 업무 설정(유형·프로젝트) | draft | DEC-001 | 유형·프로젝트를 만든다 |
| SPEC-003 | 내 업무 — 생성·상세·편집 | draft | DEC-002 | 업무를 만들고 열어서 고친다 |
| SPEC-004 | 내 업무 — 상태·완료 게이트·뷰 | draft | DEC-002 | 완료까지 보내고 리스트↔칸반을 오간다 |
| SPEC-005 | 문서함 | draft | DEC-004 | md 를 올리고 고치고 업무에 연결한다 |
| SPEC-006 | 회의록 — 생성·시작 전 | draft | DEC-003 | 회의를 만들고 안건을 적고 시작한다 |
| SPEC-007 | 회의록 — 회의 중(STT·AI 배치) | draft | DEC-003 | 말하면 스크립트가 쌓이고 AI 탭이 찬다 |
| SPEC-008 | 회의록 — 종료·통합·편집 | draft | DEC-003 | 통합본이 나오고 액션에서 업무가 생성된다 |
| SPEC-009 | 캘린더 | draft | DEC-005 | 일정을 끌어 옮기고 겹치는 자리엔 안 놓인다 |
| SPEC-010 | 개인 설정 | draft | DEC-001 | 프로필·경력이 자동 저장되고 v2 는 안내만 |
| SPEC-011 | 메시지함(v1 UI 만) | draft | DEC-006 | 메뉴로 들어가면 화면이 보이고 안내가 뜬다 |
