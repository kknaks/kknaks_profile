---
id: SCAX-SPEC-005
doc_no: SCAX-DOC-8
type: spec
title: 조직·사람·권한
status: draft
owner: TBD
last_updated: 2026-09-07
version: 0.2.0
sources:
  - SCAX-BL-001
---

# SCAX-SPEC-005 조직·사람·권한

실제 서버 session과 generic Principal을 기준으로 조직·사람을 탐색하고, versioned capability·role·grant를 조직 축과 Project 축에 적용하는 계약이다.

> Project 자체와 ProjectAssignment lifecycle은 [SCAX-SPEC-010](spec-010-project-collaboration-access.md)이 소유한다. 내부 권한 합성은 [Organization & Access](../40-architecture/organization-access.md)가 소유한다.

## 1. 인증과 Principal

### 현재 제공 범위

- 개발 환경에서는 email·password로 실제 서버 session을 만들고 session cookie로 사용자를 식별한다.
- 비밀번호 원문은 저장하거나 응답하지 않는다.
- 운영 환경에서는 local login과 provider 목록 route 자체를 노출하지 않는다.
- 모든 사용자 표면은 특정 로그인 방식에 종속되지 않는 `Principal`을 사용한다.
- logout, session 만료, 계정 또는 grant 변경 후에는 이전 권한을 계속 사용할 수 없다.

### 아직 제공하지 않는 범위

- Google OIDC 로그인은 현재 제공하지 않는다.
- 외부 identity provider 선택과 계정 연결 UX는 별도 계약이 필요하다.

## 2. 조직과 사람

- 재직, 계정, 조직 소속, 보직, 직급, 직무는 서로 다른 사실이며 각각의 기간을 보존한다.
- 계정이 없는 사람도 조직 directory와 과거 관계에는 남을 수 있다.
- 이름·조직·직무로 사람을 찾을 수 있지만, 결과 field는 현재 Principal의 권한에 맞게 제한한다.
- 클라이언트가 보낸 사용자 식별 header나 화면 persona는 서버 session의 Principal을 바꾸지 못한다.

## 3. Capability·Role·Grant

- 권한은 capability와 적용 scope의 조합으로 평가한다.
- capability와 표준 role catalog, grant 변경은 version을 가지며 알 수 없는 capability를 role에 넣을 수 없다.
- role의 capability 구성을 변경할 때 기대 version이 다르면 충돌로 거부한다.
- `StandardGrantRule`은 업무·조직·Project 관계에 따라 필요한 표준 grant를 만들고 회수한다.
- 관리자가 customization한 role은 표준 규칙의 재실행으로 덮어쓰지 않는다.
- grant는 organization scope 또는 project scope를 가질 수 있으며 두 축을 섞어 암묵적으로 확장하지 않는다.

## 4. 대표자와 조직 전체 조회

- 대표자 성격의 조직 전체 reader는 허용된 조직 자료와 private Meeting을 포함한 read-only projection을 볼 수 있다.
- 조직 전체 읽기 권한은 다른 사람의 Task를 수행·전이하거나 판단을 대신할 권한이 아니다.
- 다른 사람의 private AX conversation은 조직 전체 reader에게도 열리지 않는다.
- 사용자 대리(impersonation)는 제공하지 않는다.
- 조직 전체 reader라는 이유만으로 Project에 접근할 수 없다. Project 접근은 유효한 ProjectAssignment만 연다.

## 5. Access 관리 UI

### 현재 제공 범위

- 권한 있는 관리자는 role·capability catalog와 현재 grant를 조회할 수 있다.
- 사용자에게 role을 grant하거나 revoke할 수 있다.
- 변경 결과와 현재 scope를 다시 조회할 수 있다.

### 부분 제공 범위

- role capability 편집 command와 version 충돌 보호는 존재하지만, role 편집 UI는 모든 관리 흐름을 완결하지 않는다.
- UI가 제공하지 않는 기능을 사용 가능한 관리 기능처럼 표시하지 않는다.

## 6. Project scope와 보호 규칙

- ProjectAssignment만 해당 Project 읽기 권한을 연다.
- Project lead의 관리 권한과 member의 read-only 권한은 [SCAX-SPEC-010](spec-010-project-collaboration-access.md)을 따른다.
- ProjectAssignment 종료 시 그 관계에서 파생된 project-scoped grant도 종료한다.
- 조직 role이나 관계 탐색 결과는 Project assignment를 대신하지 않는다.
- Project 권한으로 Project 밖 사람·자료·Task 접근을 열 수 없다.

## 7. Functional Rules

1. 서버 session이 Principal의 정본이며 클라이언트가 Principal을 선택할 수 없다.
2. 운영 환경은 local authentication route를 노출하지 않는다.
3. capability·role·grant는 version과 scope를 명시한다.
4. StandardGrantRule은 관리자 customization을 덮어쓰지 않는다.
5. organization과 Project는 독립 권한 축이다.
6. 대표자 조직 전체 권한은 read-only이며 impersonation·판단·타인 업무 수행을 허용하지 않는다.
7. 조직 전체 reader도 ProjectAssignment 없이 Project에 접근할 수 없다.
8. ProjectAssignment만 project access를 열고 종료 시 파생 grant도 종료한다.
9. Google OIDC와 완전한 role-editing UI를 현재 제공 범위로 표시하지 않는다.
