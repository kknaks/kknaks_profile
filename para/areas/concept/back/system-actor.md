---
type: concept
id: system-actor
title: 시스템 행위자 — 사람이 아닌 주체가 보내는 요청 (System Actor)
aliases:
  - system:meeting
  - 시스템 요청자
  - 비인격 주체
up:
  - 2026-09-12-sc-meeting
tags:
  - authorization
  - domain-model
  - actor
---

# 시스템 행위자

어떤 요청을 「그 버튼을 누른 사람」이 아니라 **시스템(또는 자원 자체)**이 보내는 것으로 모델링하는 것. 사람은 `promoted_by`·cc 같은 부가 필드로 남기고, 권한·경계 판정은 시스템 주체 기준으로 한다.

## 정의

1. 요청자 필드에 사람 id 대신 `system:<출처>`(예 `system:meeting`)와 `requester_kind=system` 을 둔다.
2. 사람이 개입한 사실은 별도 열(`promoted_by_member_id`)과 참조(cc)로 남긴다.
3. 조직 경계·역할 권한 검사는 시스템 주체에는 걸지 않는다 — 대신 **출처 자원**(회의 id·안건 id)이 추적 근거다.
4. 화면은 「회의에서 온 요청」으로 보여 주고 사람 이름은 부가 정보다.

## 사용 예시

회의록의 후속 업무를 팀장이 [업무 생성]으로 보내면, 요청자가 팀장이면 「팀장은 요청을 만들 수 있나」·「담당이 다른 조직이면?」 예외가 줄줄이 필요했다(D29·D30). 요청자를 `system:meeting` 으로 두자 예외가 사라지고 SPEC-001 통보 하나(R-48)로 끝났다.

## 왜 중요한가

- 권한 모델을 사람 중심으로만 두면 자동화·파생 요청마다 예외가 쌓인다.
- 「누가 눌렀나」와 「무엇이 근거인가」를 분리하면 감사 추적이 오히려 선명하다.

## 경계와 오해

- 시스템 행위자는 권한 우회 수단이 아니다 — 시스템이 보낼 수 있는 요청의 **종류**는 여전히 정해져 있어야 한다.
- 알림·회신 대상은 시스템이 아니라 `promoted_by`·cc 의 사람이다.

## 함께 보는 개념

- [[field-level-visibility]] · [[defense-in-depth]]

## 출처

- 2026-09-12-sc-meeting §2 · ax-workspace `modules/work/requests.py` · 커밋 d939dae · D40 · SCAX-SPEC-001 §12 R-48
