---
doc_no: SCAX-DOC-2
type: map
title: SC-AX Spec
---

# SC-AX Spec

최종 수정: 2026-09-07

SCAX의 사용자-facing 기능·권한·lifecycle 계약과 ubiquitous language로 들어가는 thin map이다. 실행 상태는 [30-work.md](30-work.md), 상위 결정은 [10-decision.md](10-decision.md), 내부 구조와 기술 선택은 [40-architecture/](40-architecture/)가 소유한다.

## 계약 경계

- SPEC은 사용자가 관찰할 수 있는 동작, 권한, 상태 전이, 예외와 확정된 불변조건을 소유한다.
- parser·storage·provider·database·route·model·worker 같은 구현 상세와 QA 실행 상태는 SPEC에 두지 않는다.
- `draft`는 계약이 아직 승인·확정되지 않았다는 뜻이다. 현재 코드에 동작이 있다는 이유만으로 `stable`로 올리지 않는다.
- “현재 제공”과 “아직 제공하지 않음/미결”을 구분하고 후자를 사용 가능한 기능처럼 표현하지 않는다.

## Source precedence

| 우선순위 | 근거 | 쓰임 |
|---:|---|---|
| 1 | 이 정합화에서 사용자가 확정한 결정 | Project·조직 경계와 SPEC 분리 등 최종 계약 |
| 2 | Vault main의 SCAX 상용 시스템 구축·설계·유비쿼터스 랭귀지와 관련 Work Brief | 설계 의도와 용어 |
| 3 | 독립 `ax-workspace` main `0465cbac92dc3a6d65c902803af2246ff45a0091` | 현재 제공 surface와 예외의 판별 근거 |
| 4 | [SCAX-BL-001](00-baseline/SCAX-BL-001-thesc-prototype/README.md) | 과거 baseline과 회귀 비교 |

현재 구현은 계약의 availability를 판별하는 근거지만 제품 결정을 대신하지 않는다. 이 map과 SPEC 001–010은 mediness `a88e995de0dd03fb168f3ffa4ffa6fd3657234e0`에서 한 change unit으로 정합화했다.

## SPEC Bundle

| 묶음 | 포함 SPEC | 파일 |
|---|---|---|
| 업무와 판단 | SCAX-SPEC-001, 002 | [업무 관리](20-spec/spec-001-work-management.md) · [판단 항목 검토](20-spec/spec-002-action-item-review.md) |
| 기록과 회의 | SCAX-SPEC-003, 004 | [업무 기록·일일보고](20-spec/spec-003-work-record-daily-report.md) · [회의·미팅노트](20-spec/spec-004-meeting-note.md) |
| 조직과 자료 | SCAX-SPEC-005, 006 | [조직·사람·권한](20-spec/spec-005-organization-people-access.md) · [자료 검색·출처 계보](20-spec/spec-006-material-search-lineage.md) |
| 일정과 AX | SCAX-SPEC-007, 008 | [일정·캘린더](20-spec/spec-007-calendar-connected-service.md) · [AX 대화·제안](20-spec/spec-008-ax-conversation-suggestion.md) |
| 관계와 Project | SCAX-SPEC-009, 010 | [관계 탐색](20-spec/spec-009-relationship-exploration.md) · [프로젝트 협업·프로젝트 범위 권한](20-spec/spec-010-project-collaboration-access.md) |

## SPEC List

| ID | 제목 | 영역 | Status | 파일 |
|---|---|---|---|---|
| SCAX-SPEC-001 | 업무 관리 | 업무 수행 | draft | [spec-001-work-management.md](20-spec/spec-001-work-management.md) |
| SCAX-SPEC-002 | 판단 항목 검토 | 사람 판단 | draft | [spec-002-action-item-review.md](20-spec/spec-002-action-item-review.md) |
| SCAX-SPEC-003 | 업무 기록·일일보고 | 기록·보고 | draft | [spec-003-work-record-daily-report.md](20-spec/spec-003-work-record-daily-report.md) |
| SCAX-SPEC-004 | 회의·미팅노트 | 회의 | draft | [spec-004-meeting-note.md](20-spec/spec-004-meeting-note.md) |
| SCAX-SPEC-005 | 조직·사람·권한 | 조직·권한 | draft | [spec-005-organization-people-access.md](20-spec/spec-005-organization-people-access.md) |
| SCAX-SPEC-006 | 자료 검색·출처 계보 | 자료·검색 | draft | [spec-006-material-search-lineage.md](20-spec/spec-006-material-search-lineage.md) |
| SCAX-SPEC-007 | 일정·캘린더 | 일정 | draft | [spec-007-calendar-connected-service.md](20-spec/spec-007-calendar-connected-service.md) |
| SCAX-SPEC-008 | AX 대화·제안 | AX | draft | [spec-008-ax-conversation-suggestion.md](20-spec/spec-008-ax-conversation-suggestion.md) |
| SCAX-SPEC-009 | 관계 탐색 | 관계 graph | draft | [spec-009-relationship-exploration.md](20-spec/spec-009-relationship-exploration.md) |
| SCAX-SPEC-010 | 프로젝트 협업·프로젝트 범위 권한 | Project | draft | [spec-010-project-collaboration-access.md](20-spec/spec-010-project-collaboration-access.md) |

## 제공 범위 요약

| 영역 | 현재 제공 | 아직 제공하지 않음 또는 미결 |
|---|---|---|
| 업무·판단 | self Task, WorkRequest, direct assignment, delivery, version·checklist·subtask·reference | 다단계 subtask, 보편 WorkflowRun |
| 보고 | 개인 draft·편집·제출 history | team status, reminder, resubmit |
| 회의 | privacy, note versions, recording·transcript·refinement·summary·follow-up | live summary, global indicator, consent·retention 정책 |
| 인증·권한 | server session, local dev auth, role·grant, access 관리, Project scope | Google OIDC, 완전한 role-editing UI |
| 자료 | 구조 보존 추출, 권한 검색, locator, purge | embeddings, Drive, 특정 운영 storage, retention |
| 캘린더 | local Task·Meeting projection | Google Calendar |
| AX | 여러 대화, async queue, cancel·retry, tools·actions·resources·graph 답변 | recipient recommendation, profile learning, workflow authoring |
| 관계·Project | 권한 graph, 1-hop 탐색, independent Project와 assignments | generic query builder, inferred edge, graph DB |

## 영역별 읽는 순서

| 목적 | 읽는 순서 |
|---|---|
| 업무 생성·배정·납품 | SCAX-SPEC-001 → 002 → [Work & Decision Model](40-architecture/work-decision-model.md) |
| 보고·회의 근거 | SCAX-SPEC-003 또는 004 → 001 → 006 |
| 조직·Project 권한 | SCAX-SPEC-005 → 010 → [Organization & Access](40-architecture/organization-access.md) |
| 자료와 AX 답변 근거 | SCAX-SPEC-006 → 008 |
| 관계 탐색·mini graph | SCAX-SPEC-009 → 008 → 010 |
| 일정 | SCAX-SPEC-007 → 001 또는 004 |
| 내부 entity·port·기술 선택 | [40-architecture/README.md](40-architecture/README.md)부터 순서대로 |

## Ubiquitous Language

### 업무·판단

| 사용자 용어 | Canonical term | Definition | Aliases to avoid |
|---|---|---|---|
| 업무 | `Task` | 계획·수행·상태·결과를 소유하는 일의 원장 | WorkRequest, Assignment |
| 업무 요청 | `WorkRequest` | 수락 전 타인에게 일을 맡아 달라고 묻는 request-first 원장 | Task, Action |
| 수행자 배정 | `TaskAssignment` | Task 수행 책임의 기간형 사실. direct assignment는 수락 전 pending | WorkRequest, ProjectAssignment |
| 체크리스트 항목 | `ChecklistItem` | Task 안에서 ordered·versioned·archived되는 독립 항목 | Task description, Subtask |
| 하위업무 | `Subtask` | 한 단계 parent를 가진 일반 Task | ChecklistItem, 재귀 tree |
| 업무 참조 | `TaskReference` | 한 Task가 다른 Task를 명시적으로 가리키는 비권한 관계 | inferred edge, dependency |
| 업무 납품 | `TaskDelivery` | request-origin Task의 완료 제출과 requester 판단을 잇는 원장 | Task output, 새 WorkRequest |
| 판단 항목 | `ActionItem` | 원천 종류와 무관하게 같은 판단 질문을 유지하는 canonical projection | effect Action, comment |
| 제출 회차 | `Submission` | 판단 payload와 evidence를 고정한 immutable round | mutable draft, comment |
| 판단 결과 | `ReviewDecision` | 특정 Submission에 대한 공식 immutable 응답 | discussion, reaction |
| 근거 | `Evidence` | Submission에 채택되어 provenance·integrity가 식별되는 판단 자료 | 일반 attachment |

### 기록·회의·자료·AX

| 사용자 용어 | Canonical term | Definition | Aliases to avoid |
|---|---|---|---|
| 일일보고 | `DailyReport` | 특정 보고일의 근거를 사람이 편집하고 version으로 제출한 개인 보고 | 현재 dashboard |
| 회의 노트 | `MeetingNote` | 한 Meeting에 누적되는 immutable note versions | transcript, summary |
| 후속업무 후보 | `MeetingActionItem` | self Task 또는 WorkRequest로 승격하기 전의 회의 제안 | ActionItem, Task |
| 자료 | `Material` | 파일·링크와 구조 보존 추출·검색·출처를 잇는 resource | TaskReference, storage object |
| 답변 자료 참조 | `AnswerResourceReference` | AX 답변의 canonical resource ID·version·locator·표시 순서 | 복사된 citation text |
| 대화 | `Conversation` | 여러 Turn과 Conversation별 queue·draft를 묶는 사용자 대화 | 단일 chat session |
| 대화 응답 | `Turn` | 비동기로 실행되어 partial/final 또는 실패·취소가 되는 한 응답 | Conversation |

### 조직·Project·관계

| 사용자 용어 | Canonical term | Definition | Aliases to avoid |
|---|---|---|---|
| 역할·권한 | `Role` / `AccessGrant` | capability template과 Principal·기간·scope에 실제 발급된 권한 | 보직, 조직도 추정 권한 |
| 프로젝트 | `Project` | owner organization 없이 조직과 독립된 협업·권한 축 | team, organization |
| 프로젝트 배정 | `ProjectAssignment` | 사람과 Project를 lead/member로 잇고 project access를 여는 관계 | TaskAssignment, Membership |
| 관계 graph | `RelationshipGraph` | canonical resource 사이의 권한 있는 명시적 edge projection | inferred social graph, graph DB |
| 관계 이동 기록 | `TraversalReceipt` | AX가 관계 답변에서 실제로 따른 node·edge 순서 | 숨은 reasoning |

`WorkflowRun`은 개인 일일보고 draft 생성 같은 제한된 내부 orchestration에 사용할 수 있지만, WorkRequest·TaskAssignment·ActionItem의 보편 invariant가 아니다. effect 실행용 `Action`과 사람 판단용 `ActionItem`을 혼용하지 않는다.

## Open Questions

| ID | 상태 | 항목 | 현재 경계 |
|---|---|---|---|
| SCAX-OQ-001 | 미구현 | 팀 보고 현황·reminder·resubmit | 개인 일일보고만 현재 계약에 포함 |
| SCAX-OQ-002 | 미결 | 녹음 consent·retention과 global indicator | 값과 UX를 추정하지 않음 |
| SCAX-OQ-003 | 미구현 | Google OIDC·Google Calendar·Drive | local 기능과 분리 |
| SCAX-OQ-004 | 미구현 | embedding 검색 | 현재 text 검색 계약만 유지 |
| SCAX-OQ-005 | 미구현 | 수신자 추천·개인 profile 학습·workflow authoring | AX 현재 기능처럼 표시하지 않음 |
| SCAX-OQ-006 | 미결 | 운영 object storage와 자료 retention | architecture/운영 결정 전 특정 provider를 약속하지 않음 |
