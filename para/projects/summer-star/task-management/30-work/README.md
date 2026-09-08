# Work Index

규칙: `para/projects/project.md`

> 현재 구현, QA, 릴리즈 상태를 추적하는 map이다. 상세 work 실행 본문은 `30-work/` 아래 1 파일 = 1 work로 둔다.
> `Status Board`는 실행 상태의 owning view다. Spec Coverage는 work frontmatter `links.specs`를 spec 중심으로 펼친 derived view다.

최종 수정: 2026-09-08

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
|  |  |  |  |  |  |  |  |  |  |

## Work List

work 문서를 만들거나 상태, owner, branch, 다음 작업이 바뀌면 이 표를 갱신한다.

| ID | Title | Type | Owner | Status | Progress | File | Covers Spec |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## Spec Coverage

각 spec이 어느 work에서 구현되며 현재 진척이 어떤지 한눈에 보는 spec-centric view다. Covering Work의 Status를 종합한 derived view다.

| Spec | Covering Work | 구현 상태 |
|---|---|---|
|  |  |  |

## 1그룹 (2026-09-05 작성)

| ID | Title | Status | Covers spec | Depends | Phase |
|---|---|---|---|---|---|
| WORK-001 | 스캐폴딩 | todo | SPEC-000 | — | 4 |
| WORK-002 | 로그인·세션 | todo | SPEC-001 | WORK-001 | 3 |
| WORK-003 | 업무 설정 | todo | SPEC-002 | WORK-002 | 3 |

## 회의록 재작업 그룹 (2026-09-07 작성 — MF-1 ~ MF-70 · **2026-09-08 MF-71 추가**. WORK-006/007/008 은 옛 설계, 참고만)

| ID | Title | Status | Covers spec | Depends | Phase |
|---|---|---|---|---|---|
| WORK-009 | 회의록 AI — MCP 서버 · 회의별 단명 토큰 · codex allow list | **done**(09-07 밤) | SPEC-007 §4 | WORK-002 · 006 · 007 | 4 |
| WORK-010 | 회의 시작 — `/start` 는 전이만 · 웜스타트는 컨텍스트 없이 백그라운드 | **done**(09-07 밤 · 앱 창 캡처 아침) | SPEC-006 §4 · SPEC-007 §4 | WORK-009 | 2 |
| WORK-011 | 회의 중 — 배치 입력은 발화뿐 · AI 트랙 전량 교체 · 슬래시 5 · 줄 시각 제거 | done | SPEC-007 | WORK-009 · 010 | 4 |
| WORK-012 | 회의 종료 — async 재전사 → 최종 회의록 한 번 · 용어 보정 · payload | done | SPEC-008 §4 | WORK-009 · 011 | 4 |
| WORK-013 | 편집 · 정리 — payload 드로어 둘 · 칩 둘 갈래 · 자리 유지 · 모달 420 · 유형 설명 | done | SPEC-008 U-6~U-10 · SPEC-002 | WORK-012 | 5 |
| WORK-014 | 목록 · 상세 UI — breadcrumb 링크 · 「←」 · 미리보기 패널 · 헤더 순서 | done | SPEC-006 U-1·4·6·8 · SPEC-008 U-3 | — (머지 순서 013 뒤) | 3 |
| WORK-015 | **중간 배치는 AI 혼자 쓴다 — 도구 셋 · 미러 안건 폐기 · 조회 순서 절 삭제**(MF-71) | **done** | SPEC-007 §4 · §5 · §6 · U-4 | WORK-011 · 012(둘 다 done) | 2 |

발주 순서 009 → 010 → 011 → 012 → 013. 014 는 계약상 독립이라 언제든 발주하되 `AgendaLineTree.tsx`·`MeetingClosedPage.tsx` 를 012·013 과 함께 만지므로 **머지는 013 뒤**다. **하나씩 발주 · 검증 · 다음.**

**WORK-015 는 009~014 가 전부 들어간 뒤(코드 HEAD `5c72c25`) 다음에 발주한다.** WORK-011 의 후속이고 **백엔드만**(프론트 0 · 마이그레이션 0)이라 앞의 것들과 겹치지 않는다 — 다만 `meeting_batch_service.py` 와 `integrations/agent.py` 를 만지므로 **다른 코드 워커와 동시에 돌리지 않는다.**

> **스키마 파일 소유** — `ai_schemas/meeting_notes.json`(회의 중·최종 한 벌, MF-52)은 **WORK-011 이 만들고** WORK-012 는 읽기만 한다. `meeting_batch.json` 은 011 이, `meeting_integration.json` 은 012 가 폐기한다.

> **착수 전 선행**: `orchestration/config/projects/task-management.json` 에 `repos.code`(`github.com/kknaks/task_management` clone) 등록. 코드는 이 레포에 만들지 않는다.
