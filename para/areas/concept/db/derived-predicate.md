---
type: concept
id: derived-predicate
title: 파생 판정 (Derived Predicate)
aliases:
  - 파생 판정
  - derived predicate
  - 파생 축
  - 저장 없는 분류
up:
  - 2026-09-01-task-improve
tags:
  - database
  - 모델링
  - 백엔드
---

# 파생 판정 (Derived Predicate)

**새 개념을 저장하지 않고, 이미 있는 컬럼들의 조합식으로 정의하는 것.** 컬럼·타입·테이블을 늘리는 대신 "이 조건이면 그 개념이다"라는 술어 하나를 둔다.

## 정의

mediness 업무 요청이 사례다. "남에게 요청한 태스크"라는 새 개념이 필요했는데, 요청 테이블도 `is_request` 컬럼도 만들지 않았다:

```
요청 = 비워크플로 task_type ∧ created_by_member_id ≠ assignee_member_id (둘 다 NOT NULL)
```

만든 사람과 담당자 컬럼은 이미 있었으므로, **"만든 사람 ≠ 담당자"라는 사실 자체가 요청**이다. migration 은 조회용 인덱스 1건뿐이었다.

## 왜 저장하지 않나

- **원장 이원화 방지** — `is_request` 를 저장하면 "컬럼과 실제 관계가 어긋난 행"이 생길 수 있다(재배정으로 담당자가 바뀌면?). 파생이면 어긋날 원본이 없다.
- **파급 차단** — 새 타입·컬럼은 그것을 소비하는 모든 자리(워크플로 fanout·필터·화면)에 분기를 강제한다. 파생은 술어를 읽는 자리만 안다.

## 지켜야 성립하는 것

- **술어는 한 곳** — SQL 조각·서비스 판정·화면 판정으로 흩어지면 파생이 세 벌이 된다. mediness 는 repositories 층 한 파일에 두고 grep 테스트로 중복 정의를 막았다.
- **서버가 판정을 내려보낸다** — 화면이 원자료로 재유도하면(예: FE 가 created_by 를 비교) 판정이 두 벌이 된다. 응답에 `is_request` 같은 **계산된 필드**로 싣는다.
- **전제 컬럼의 의미 변화에 취약** — "요청자=담당자" 가정을 깔던 코드가 담당자 분리 후 연쇄로 깨졌다 → [[contract-surface-enumeration]]

관련: [[database-migration]] — 파생으로 풀면 migration 자체가 줄어든다.
