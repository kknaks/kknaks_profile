---
id: SCAX-SPEC-010
doc_no: SCAX-DOC-13
type: spec
title: 프로젝트 협업·프로젝트 범위 권한
status: draft
owner: TBD
last_updated: 2026-09-07
version: 0.1.0
sources:
  - SCAX-BL-001
---

# SCAX-SPEC-010 프로젝트 협업·프로젝트 범위 권한

조직과 독립된 Project에 lead·member를 배정하고, ProjectAssignment가 열어 준 범위에서 계획·업무·관계 graph를 협업하는 계약이다.

## 1. 핵심 결정

- Project에는 owner organization을 두지 않는다. 조직과 Project는 독립된 분류·권한 축이다.
- `ProjectAssignment`만 Project 접근을 연다.
- ProjectAssignment의 역할은 `lead` 또는 `member`다.
- lead는 Project 안에서 `project.manage`와 `task.assign`으로 계획·배정과 cross-unit member 배정을 수행할 수 있다.
- member는 Project와 그 안의 허용 resource를 read-only로 본다.

## 2. Project와 ProjectAssignment

- Project는 이름, 설명, 상태와 독립 identity를 가진다.
- Project 생성자는 유효한 lead ProjectAssignment를 얻는다.
- lead는 다른 조직 단위의 구성원도 Project member 또는 lead로 추가할 수 있다.
- ProjectAssignment가 시작되면 역할에 맞는 project-scoped grant가 열린다.
- Assignment가 종료되면 그 관계에서 파생된 project-scoped grant도 종료한다.
- 수동으로 별도 부여된 다른 grant까지 함께 회수하지 않는다.
- 같은 조직·team 소속, 대표자 조직 전체 read 권한, graph 노출만으로 Project 접근이 생기지 않는다.

## 3. Project 역할

| 역할 | 허용 범위 | 허용하지 않는 범위 |
|---|---|---|
| lead | Project 조회·수정, member 관리, Project Task 계획, Project 안의 cross-unit 배정 | Project 밖 resource 접근, 다른 사용자의 판단 대리 |
| member | Project와 연결된 허용 Task·관계의 read-only 조회 | Project 수정, member 관리, Task 생성·배정·상태 전이, 판단 대리 |

- member가 Project 밖에서 별도 capability나 TaskAssignment를 가지면 그 관계의 권한은 독립적으로 적용한다.
- Project role은 organization role을 바꾸지 않는다.

## 4. Project Task

- Task의 Project 연결은 선택 사항이다.
- lead는 담당자가 아직 없는 계획 Task를 Project 안에 만들 수 있다.
- 담당자 없는 계획 Task는 Project view에는 보이지만 누구의 My Work에도 나타나지 않는다.
- Project Task의 직접 배정은 [SCAX-SPEC-001](spec-001-work-management.md)의 task-first 수락 계약을 따른다.
- parent Task가 Project에 연결되면 child Task도 같은 Project를 따른다.
- child만 Project에서 분리하거나 다른 Project로 옮길 수 없다.
- ProjectAssignment는 Project 읽기를 열지만 TaskAssignment를 대신하지 않으므로 member에게 수행·상태 전이 권한을 주지 않는다.

## 5. Project is no backdoor

- ProjectAssignment로 얻은 grant는 해당 Project와 그에 명시적으로 연결된 resource에만 적용한다.
- Project member라는 이유로 참여자의 다른 Task, private Meeting, Conversation, 조직 자료를 볼 수 없다.
- Project graph grouping은 이미 허용된 Project member와 Task만 묶어 보여 주며 새 접근 관계를 만들지 않는다.
- Project에서 참조하는 외부 resource는 원래 권한이 없으면 내용 대신 제한된 참조 상태만 표시한다.
- Project 종료 또는 Assignment 종료 후에는 캐시된 목록·검색·graph·inline detail에서도 접근을 다시 거부한다.

## 6. Dataset onboarding 불변조건

- 조직 dataset은 사람 directory와 로그인 계정을 별도로 가져올 수 있으며 login은 선택 사항이다.
- login이 없는 사람도 조직도, Project의 과거·현재 참여 사실과 관계 graph에 존재할 수 있다.
- login이 없는 사람은 WorkRequest 수신자나 실제 TaskAssignment 같은 업무 수행 후보로 제시하지 않는다.
- 서버는 login 없는 사람을 수행자 또는 판단자로 만드는 요청을 거부한다.
- login이 없는 directory member의 ProjectAssignment 자체는 협업 관계 사실로 가져올 수 있지만, 로그인·업무 수행 권한을 암시하지 않는다.

## 7. Functional Rules

1. Project에는 owner organization이 없다.
2. organization과 Project는 독립 축이고 ProjectAssignment만 project access를 연다.
3. lead는 Project 안에서 manage·task assign·cross-unit member assignment를 할 수 있다.
4. member의 Project 권한은 read-only다.
5. Assignment 종료는 그 관계에서 파생된 project-scoped grant를 종료한다.
6. Task의 Project 연결은 optional이고 child는 parent의 Project를 따른다.
7. 담당자 없는 Project Task는 계획에는 보이지만 My Work에는 보이지 않는다.
8. Project는 다른 resource나 조직 권한으로 가는 backdoor가 아니다.
9. Project graph grouping은 허용된 기존 관계만 표현한다.
10. login 없는 사람은 업무 수행·판단 assignment 후보가 아니다.
