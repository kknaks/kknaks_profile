---
type: concept
id: field-level-visibility
title: 필드 단위 가시성 (부분 자격 응답)
aliases:
  - 필드 가시성
  - 부분 인가 응답
  - null 로 가리기
  - field-level authorization
up:
  - 2026-09-08-sc-design-system
tags:
  - authorization
  - api
  - response-shape
---

# 필드 단위 가시성

한 리소스 안에서 **일부 필드만 자격에 따라 보이는** 경우, 요청 전체를 403 으로 거절하지 않고 응답 필드를 비운다(`null` / 빈 배열). 필드 자체는 남기고 값만 비우므로 화면은 자격이 있든 없든 같은 모양으로 한 번의 요청으로 그린다.

## 정의

1. 리소스의 필드를 **기본 필드**(로그인한 누구나)와 **민감 필드**(자격 보유자만)로 나눈다.
2. 민감 필드는 자격이 없으면 예외를 던지지 않고 값을 비운다. 자격 판정 술어는 한 곳에 두고 읽기·쓰기가 같은 것을 쓴다.
3. 「현재값보다 더 아는 것」(이력·감사 기록·변경 기록)은 별도 엔드포인트로 두고 자격이 없으면 **403**. 부분 응답으로 흘려보내지 않는다.
4. 자격 판정은 서버가 한다. 클라이언트가 응답 값(예: 특정 필드가 null)으로 자격을 역추론하지 않는다.

## 사용 예시

```python
# application layer — 구성원 6축 통합 조회
def member_detail(self, principal, member_id):
    profile = self._repository.member_detail(member_id)          # 기본 축은 항상
    if not (principal.member_id == member_id
            or self._administration.manages_any_of(principal, profile["units"])):
        profile["phone"] = None
        profile["birth_date"] = None
        profile["grants"] = []
        profile["revoked_grants"] = []
    return profile

def member_axis_history(self, principal, member_id, axis):
    if not (self-or-manages): raise AccessAdministrationDenied()   # → 403
```

## 왜 중요한가

화면이 사람 한 명을 그릴 때 「연락처는 못 보지만 소속은 본다」가 흔하다. 요청을 통째로 403 으로 막으면 화면은 필드별로 요청을 쪼개야 하고, 그 순간 자격 규칙이 프론트 코드에 복제된다. 필드를 비우면 규칙은 서버 한 곳에만 있다.

## 경계와 오해

- **null ≠ 없음** — 값이 없어서 null 인지 자격이 없어서 null 인지 응답만으로는 구분이 안 된다. 실데이터에 그 값이 원래 없으면(SC 조직도의 전화 15/165) 「null 이면 자격 없음」 휴리스틱이 바로 무너진다. 구분이 필요하면 별도 신호(예: `visibility` 필드)를 둔다.
- **모든 자격을 비우기로 풀지 않는다** — 이력·변경 기록처럼 존재 자체가 정보인 것은 403 이 맞다.
- **capability 보유 ≠ 범위** — 「관리 capability 가 있으면 값」은 조직 범위를 안 본다. 범위로 좁히려면 판정에 대상의 소속 unit 을 넣어야 한다.

## 함께 보는 개념

- [[api-response-envelope]] — 가능한 행동(`allowed_commands`)을 서버가 응답에 싣는 것과 같은 방향
- [[temporal-table]] — 이력이 별도 엔드포인트가 되는 이유(기간 행이 현재값보다 많은 것을 말한다)

## 출처

- [[2026-09-08-sc-design-system]] — 조직 화면 6축 통합 조회에서 민감 필드 null · 이력 403 으로 가른 결정과, 프론트 휴리스틱이 무너진 경위
