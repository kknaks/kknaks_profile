---
id: SCAX-ORGANIZATION-ACCESS
type: architecture
title: SCAX Organization & Access
status: draft
owner: architecture
last_updated: 2026-09-07
---

# SCAX Organization & Access

SCAX의 generic Principal과 organization/project scope authorization을 정의한다. 사용자 표면은 [SCAX-SPEC-005](../20-spec/spec-005-organization-people-access.md)와 [SCAX-SPEC-010](../20-spec/spec-010-project-collaboration-access.md)이 소유한다.

## 1. Identity와 session

- inbound HTTP와 MCP는 인증 adapter에서 `Principal`을 얻고 같은 application authorization을 사용한다.
- 개발 local email/password는 real server session을 만들며 운영 구성에서는 local auth route가 등록되지 않는다.
- session은 account/member 연결을 해석하지만 domain service가 특정 login provider에 의존하지 않는다.
- Google OIDC는 현재 adapter로 제공되지 않는다.
- account가 없는 Member는 directory 사실로 존재할 수 있으나 interactive Principal이나 업무 판단자가 아니다.

## 2. 독립된 조직 사실

`EmploymentPeriod`, `Membership`, `PositionDefinition`/`Appointment`, `GradeAssignment`, `JobAssignment`, account link는 독립 원장이다. 한 관계에서 다른 관계나 capability를 추론하지 않는다.

## 3. Authorization input

`authorize(Principal, capability, resource, purpose)`는 다음을 함께 평가한다.

1. 유효한 session과 Member/account 상태
2. versioned Role의 capability 집합
3. 현재 유효한 AccessGrant
4. organization 또는 project scope
5. TaskAssignment, Meeting participant/share, resource binding 같은 직접 관계
6. action-specific subject state와 version

목록·검색·graph·AX resource도 같은 판정을 사용하고 숨긴 resource의 수를 별도 side channel로 노출하지 않는다.

## 4. Role catalog와 StandardGrantRule

- CapabilityDefinition과 RoleDefinition은 catalog version을 가지며 grant 변경도 versioned state로 보호한다.
- role customization은 expected version으로 동시성을 보호한다.
- StandardGrantRule은 self work, organization reader, ProjectAssignment 같은 source relation에서 표준 grant를 reconcile한다.
- source relation과 derived grant를 연결해 종료 시 해당 grant만 회수한다.
- 관리자가 customization한 role definition을 catalog reconcile이 덮어쓰지 않는다.

## 5. Organization과 Project scope

- organization scope와 project scope는 독립 축이다.
- 대표자 organization-wide read grant는 조직 resource를 넓게 읽을 수 있지만 타인의 command·decision·Conversation 권한을 주지 않는다.
- Project에는 owner organization을 두지 않는다.
- ProjectAssignment만 Project 접근을 열고 lead/member에 맞는 project-scoped grant를 파생한다.
- organization-wide reader, 같은 Membership, Project graph edge는 ProjectAssignment를 대신하지 않는다.
- ProjectAssignment 종료는 파생 grant를 끝내며 다른 독립 grant에는 영향을 주지 않는다.

## 6. Projection rules

- private Meeting outsider는 busy-only projection을 받는다.
- Project outsider는 Project 또는 연결 Task의 존재를 볼 수 없다.
- member Project role은 read-only이며 별도 TaskAssignment 없이는 수행 command를 받지 않는다.
- AnswerResourceReference와 graph node는 표시할 때마다 재인가한다.
- 권한 상실은 캐시·search·inline peek에도 즉시 같은 결과를 내야 한다.

## 7. Invariants

1. 인증 adapter가 Principal을 만들고 client header가 이를 대체하지 못한다.
2. Role은 template, AccessGrant는 scope와 기간을 가진 실제 권한이다.
3. organization-wide read는 impersonation이나 decision 권한이 아니다.
4. Project access는 오직 유효한 ProjectAssignment에서 열린다.
5. 권한 판정은 query와 command 양쪽의 application boundary에서 시행한다.
