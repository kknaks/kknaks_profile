---
type: content
id: C-004
date: 2026-05-03
duration: '15:09'
speaker: ArjanCodes
kind: study
youtubeId: wYeDGkdMi3g
title:
  en: Replace Boolean Flags with the Policy Pattern in Python
  ko: Python에서 정책 패턴으로 조건문 복잡성 제거하기
summary:
  en: Learn to replace boolean flags and growing conditionals with composable policy objects for cleaner, scalable Python code
  ko: 불린 플래그와 복잡한 조건문을 개별 정책 객체로 분리하여 확장 가능하고 테스트하기 좋은 Python 코드를 만드는 방법
tags:
- '#python'
- '#design-patterns'
- '#policy-pattern'
- '#clean-code'
- '#refactoring'
- '#functional-programming'
---

## 요지

- 정책 패턴은 복잡한 조건문을 개별 정책 클래스 또는 함수로 분리하여 각각 한 가지 규칙만 담당하게 한다.
- 각 정책은 독립적으로 테스트하고 재사용할 수 있으며, 규칙을 추가할 때 기존 코드를 수정하지 않아도 된다.
- 합성(composition)을 통해 여러 정책을 파이프라인처럼 연결하면, 요청이 각 정책을 차례로 통과하며 처리된다.
- 함수형 접근은 클래스보다 더 파이썬스럽고 간결하며, 함수를 일급 객체로 다루어 더 유연한 정책 구성을 가능하게 한다.
- 정책 레지스트리 패턴으로 기능 플래그를 중앙에서 관리하면, 설정 파일만 변경해 동작을 제어할 수 있다.

## 개요

현실의 Python 코드에서 자주 마주치는 패턴이 있다: 불린 플래그 몇 개와 if-else 문 체인으로 이루어진 함수들이다. 처음에는 문제가 없어 보이지만, 규칙이 하나 추가되고 또 다른 규칙이 추가되면서 함수는 급격히 복잡해진다. 이렇게 커진 함수는 확장하기도 어렵고, 테스트하기도 어렵고, 규칙을 재사용하기도 어렵다. 결국 관리 불가능한 스파게티 코드가 되어버린다.

이 문제를 해결하는 방법이 **정책 패턴(Policy Pattern)** 이다. 정책 패턴을 사용하면 복잡한 조건문을 작고 독립적인 정책 단위로 나누고, 이를 필요에 따라 조합하여 사용할 수 있다. 이 접근법은 Python의 함수형 프로그래밍 철학과도 잘 맞아, 코드를 더 읽기 쉽고 유지보수하기 좋게 만들어준다.

## 배경 / 사전 지식

### 불린 플래그와 조건문의 문제
어떤 요청이나 작업이 허용되는지 판단해야 할 때, 보통은 여러 조건을 확인한다. 각 조건을 불린 플래그나 if-else 문으로 구현한다. 예를 들어:
- 사용자가 활성 상태인가?
- 사용자 역할이 충분한가?
- 다중 인증을 통과했는가?
- 감사 로그를 기록해야 하는가?

이런 조건들이 하나의 함수 안에 모두 들어가면, 함수는 점점 커지고 각 조건의 영향 범위를 파악하기 어렵다.

### 데이터클래스 (dataclass)
Python 3.7+의 `dataclasses` 모듈은 데이터를 담는 클래스를 간단히 정의하도록 해준다. 이는 설정, 객체 상태를 저장할 때 유용하다.

### 프로토콜 (Protocol)
`typing.Protocol`은 덕 타이핑을 형식적으로 정의하는 방식이다. 특정 메서드를 가진 모든 객체가 그 프로토콜을 만족한다고 본다. 상속보다 유연하고 Python다운 방식이다.

### 함수형 프로그래밍의 기초
Python에서는 함수를 일급 객체(first-class object)로 다룬다. 즉, 함수를 변수에 할당하고, 다른 함수의 인자로 전달하고, 함수가 함수를 반환할 수 있다. 이를 활용하면 클래스를 쓰지 않고도 정책 패턴을 구현할 수 있다.

## 핵심 개념

### 정책 패턴이란?
정책 패턴은 어떤 작업을 수행하는 방식을 여러 개의 작은 "정책"으로 분리하는 디자인 패턴이다. 각 정책은:
- **한 가지 책임**: 하나의 규칙 또는 검사만 담당
- **독립적**: 다른 정책과 독립적으로 작동하고 테스트할 수 있음
- **조합 가능**: 여러 정책을 조합하여 복잡한 로직을 구성

예를 들어, 권한 검사 시스템이라면:
- `ActiveUserPolicy`: 사용자가 활성 상태인지 확인
- `RolePolicy`: 사용자 역할이 필요한 권한을 가지는지 확인
- `MFAPolicy`: 다중 인증을 통과했는지 확인
- `AuditPolicy`: 접근 기록을 로그에 남김

이들을 순서대로 적용하면 복잡한 로직이 자동으로 처리된다.

### 전략 패턴 vs 정책 패턴
둘 다 행동을 캡슐화하는 패턴이지만, 의도가 다르다:

**전략 패턴**: "여러 알고리즘 중 하나를 선택"한다. 예를 들어 정렬 알고리즘을 선택하거나, 결제 방식을 선택할 때 사용한다. **하나의 알고리즘만 실행된다.**

**정책 패턴**: "여러 규칙을 조합"한다. 모든 정책이 차례로 적용되어야 한다. 예를 들어 접근 권한 검사에서 모든 조건을 확인해야 하므로, 활성 사용자 정책, 역할 정책, MFA 정책이 **모두 실행된다.**

### OOP 방식 vs 함수형 방식
같은 정책 패턴을 두 가지 방식으로 구현할 수 있다:

**OOP**: 정책을 클래스로 정의하고, 베이스 클래스나 프로토콜로 인터페이스를 정한다. 복잡한 상태를 관리할 때 유용하다.

**함수형**: 정책을 함수로 정의한다. 더 간단하고 Python다운 방식이며, 대부분의 경우 클래스보다 읽기 쉽다.

## 작동 원리

### 1단계: 문제 인식
초기 코드는 권한 검사와 로깅을 하나의 큰 함수에 모두 구현한다:
```python
def process_request(user, request):
    # 여러 조건을 한 함수에 모두 작성
    if not user.is_active:
        raise PermissionError
    if not has_required_role(user):
        raise PermissionError
    # ... 더 많은 조건들
    request.access_granted = True
    audit_log.write(...)
    return request
```
このアプローチの問題:
- 함수가 많은 책임을 가짐
- 규칙을 추가할 때마다 함수를 수정해야 함
- 개별 규칙을 테스트하기 어려움
- 규칙을 다른 곳에서 재사용하기 어려움

### 2단계: OOP 버전으로 리팩토링
각 규칙을 클래스로 분리:
```
BasePolicy (프로토콜)
  ├─ ActiveUserPolicy
  ├─ RolePolicy
  ├─ MFAPolicy
  ├─ AuditPolicy
  └─ GrantAccessPolicy

CompositePolicy (모든 정책 포함)
  └─ apply() → 각 정책을 순서대로 적용
```

각 정책은 `apply(user, request)` 메서드를 가지며, `CompositePolicy`가 이들을 차례로 호출한다.

### 3단계: 함수형 버전으로 간소화
클래스 대신 함수 사용:
```
active_user(user, request) → request
role_required(user, request) → request
mfa_policy(user, request) → request
audit(user, request) → request

함수 조합: active_user | role_required | mfa_policy | audit
```

각 함수가 `request`를 받아서 처리한 후 `request`를 반환하면, 함수들을 파이프라인처럼 연결할 수 있다.

### 4단계: 정책 레지스트리로 확장
설정 파일이나 데이터베이스에 어떤 정책을 사용할지 정의:
```
policies_config = {
    'require_active': True,
    'require_mfa': False,  # 끄고 싶으면 False로
    'log_audit': True
}
```
런타임에 이 설정을 읽어서 필요한 정책만 로드하고 실행한다.

## 코드 예시

### 초기 코드 (문제 있음)
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    name: str
    roles: list[str]
    is_active: bool

@dataclass
class Request:
    user: User
    resource: str
    access_granted: bool = False
    audit_log: list[str] = field(default_factory=list)

def process_request(user: User, request: Request) -> Request:
    # 1. 사용자 활성 여부
    if not user.is_active:
        raise PermissionError(f"User {user.name} is not active")
    
    # 2. 역할 확인
    if "admin" not in user.roles:
        raise PermissionError(f"User {user.name} lacks required role")
    
    # 3. 다중 인증 (예시)
    # ... 더 많은 조건들
    
    # 4. 감사 로그 기록
    request.audit_log.append(f"{datetime.now()} - Access granted to {user.name}")
    
    # 5. 요청 승인
    request.access_granted = True
    return request

# 사용
user = User(name="Alice", roles=["admin"], is_active=True)
request = Request(user=user, resource="admin_panel")
result = process_request(user, request)
print(result)
```
**문제**: 규칙이 한 함수에 모두 묶여있다. 규칙을 추가하면 함수가 더 커진다.

### OOP 버전
```python
from typing import Protocol
from dataclasses import replace

class Policy(Protocol):
    """모든 정책이 따를 인터페이스"""
    def apply(self, user: User, request: Request) -> Request:
        ...

class ActiveUserPolicy:
    def apply(self, user: User, request: Request) -> Request:
        if not user.is_active:
            raise PermissionError(f"User {user.name} is not active")
        return request

class RolePolicy:
    def __init__(self, required_role: str = "admin"):
        self.required_role = required_role
    
    def apply(self, user: User, request: Request) -> Request:
        if self.required_role not in user.roles:
            raise PermissionError(f"User lacks role: {self.required_role}")
        return request

class AuditPolicy:
    def apply(self, user: User, request: Request) -> Request:
        log_entry = f"{datetime.now()} - {user.name} accessed {request.resource}"
        updated_log = request.audit_log + [log_entry]
        return replace(request, audit_log=updated_log)

class GrantAccessPolicy:
    def apply(self, user: User, request: Request) -> Request:
        return replace(request, access_granted=True)

class CompositePolicy:
    """여러 정책을 순서대로 적용"""
    def __init__(self, policies: list[Policy]):
        self.policies = policies
    
    def apply(self, user: User, request: Request) -> Request:
        result = request
        for policy in self.policies:
            result = policy.apply(user, result)
        return result

# 사용
policies = [
    ActiveUserPolicy(),
    RolePolicy(required_role="admin"),
    AuditPolicy(),
    GrantAccessPolicy()
]
composite = CompositePolicy(policies)

user = User(name="Alice", roles=["admin"], is_active=True)
request = Request(user=user, resource="admin_panel")
result = composite.apply(user, request)
print(result)
```
**장점**: 각 정책이 독립적이고, 새로운 정책을 추가하기 쉽다.
**단점**: 클래스가 많아서 코드가 길어진다.

### 함수형 버전 (권장)
```python
from typing import Callable

# 정책을 함수로 정의
def active_user(user: User, request: Request) -> Request:
    if not user.is_active:
        raise PermissionError(f"User {user.name} is not active")
    return request

def role_required(required_role: str = "admin") -> Callable:
    def check_role(user: User, request: Request) -> Request:
        if required_role not in user.roles:
            raise PermissionError(f"User lacks role: {required_role}")
        return request
    return check_role

def audit(user: User, request: Request) -> Request:
    log_entry = f"{datetime.now()} - {user.name} accessed {request.resource}"
    return replace(request, audit_log=request.audit_log + [log_entry])

def grant_access(user: User, request: Request) -> Request:
    return replace(request, access_granted=True)

# 정책 파이프라인
def apply_policies(policies: list[Callable], user: User, request: Request) -> Request:
    result = request
    for policy in policies:
        result = policy(user, result)
    return result

# 사용
policies = [
    active_user,
    role_required("admin"),
    audit,
    grant_access
]

user = User(name="Alice", roles=["admin"], is_active=True)
request = Request(user=user, resource="admin_panel")
result = apply_policies(policies, user, request)
print(result)
```
**장점**: 간결하고 읽기 쉽고, Python다운 방식이다.
**특징**: `replace()`는 dataclass의 메서드로, 불변성을 유지하면서 특정 필드만 변경한다.

### 정책 레지스트리 패턴
```python
from dataclasses import dataclass
import json

@dataclass
class PolicyConfig:
    require_active: bool = True
    require_role: str = "admin"
    require_mfa: bool = False
    log_audit: bool = True

class PolicyRegistry:
    def __init__(self, config: PolicyConfig):
        self.config = config
        self.policies = []
        self._build_policies()
    
    def _build_policies(self):
        """설정에 따라 동적으로 정책 구성"""
        if self.config.require_active:
            self.policies.append(active_user)
        if self.config.require_role:
            self.policies.append(role_required(self.config.require_role))
        if self.config.log_audit:
            self.policies.append(audit)
        self.policies.append(grant_access)
    
    def apply(self, user: User, request: Request) -> Request:
        return apply_policies(self.policies, user, request)

# 설정 파일에서 읽기 (예: config.json)
config_dict = {
    "require_active": True,
    "require_role": "admin",
    "require_mfa": False,
    "log_audit": True
}
config = PolicyConfig(**config_dict)
registry = PolicyRegistry(config)

user = User(name="Alice", roles=["admin"], is_active=True)
request = Request(user=user, resource="admin_panel")
result = registry.apply(user, request)
print(result)
```
**이점**: 설정 파일만 바꾸면 동작을 쉽게 제어할 수 있다. 코드를 수정할 필요가 없다.

## 함정·실수

### 1. 과도한 추상화
**실수**: 모든 작은 로직도 정책으로 만들려고 한다.
```python
# 너무 많은 정책
policies = [
    check_user_exists,
    check_is_active,
    check_role,
    check_mfa,
    check_ip_whitelist,
    check_time_window,
    log_access,
    update_last_access_time,
    grant_access
]
```
**해결**: 관련 있는 정책들을 묶는다. 예를 들어 모든 인증 관련 검사를 하나의 `AuthenticationPolicy`로 묶을 수 있다.

### 2. 클래스 오버엔지니어링
**실수**: 함수로 충분한데도 클래스를 만든다.
```python
# 불필요하게 복잡
class CheckActiveUserPolicy:
    def apply(self, user, request):
        if not user.is_active:
            raise PermissionError()
        return request
```
**해결**: 함수형 버전을 사용한다. 간단하고 Python다운 방식이다.

### 3. 상태 관리 부주의
**실수**: `request` 객체를 직접 수정한다.
```python
def audit(user, request):
    request.audit_log.append(...)  # 원본을 수정! 부작용 발생
    return request
```
**해결**: `replace()`를 사용하여 새 객체를 생성한다.
```python
def audit(user, request):
    return replace(request, audit_log=request.audit_log + [...])
```

### 4. 정책 순서 무시
**실수**: 정책의 순서가 중요한데 임의로 배치한다.
```python
# 잘못된 순서: 접근 허용 후에 활성 여부 확인
policies = [grant_access, active_user]  # 논리적으로 말이 안 됨
```
**해결**: 논리적 순서를 고려한다. 보통은 검증 → 로그 → 실행 순서가 맞다.

### 5. 정책에서 부작용(Side Effects) 혼합
**실수**: 검증과 부작용이 섞여 있다.
```python
def role_policy(user, request):
    if role not in user.roles:
        raise PermissionError()
    # 검증 후 바로 부작용 수행
    send_notification_email(user)  # 이건 별도 정책이어야 함
    return request
```
**해결**: 검증만 수행하는 정책과 부작용을 수행하는 정책을 분리한다.

## 베스트 프랙티스

### 1. 함수형 접근 선호
대부분의 경우 함수형 구현이 클래스형보다 낫다:
- 더 간단하고 읽기 쉽다
- Python의 철학에 부합한다
- 테스트하기 쉽다

클래스는 정책이 복잡한 상태를 관리해야 할 때만 사용한다.

### 2. 정책은 순수 함수로
각 정책은 부작용이 없어야 한다:
```python
# 좋음: 순수 함수
def active_user(user, request):
    if not user.is_active:
        raise PermissionError()
    return request  # 명시적으로 반환

# 나쁨: 부작용
def active_user(user, request):
    if not user.is_active:
        send_email(user)  # 부작용!
        return request
```

### 3. 정책 레지스트리 활용
설정 파일이나 환경 변수로 정책을 제어하면, 배포 시에 코드를 건드릴 필요가 없다:
```python
require_mfa = os.getenv("REQUIRE_MFA", "true").lower() == "true"
policies = [...]
if require_mfa:
    policies.append(mfa_policy)
```

### 4. 정책의 책임은 명확하게
각 정책의 이름과 구현이 일치해야 한다:
- `ActiveUserPolicy`: 사용자 활성 여부만 확인
- `RolePolicy`: 역할만 확인
- `AuditPolicy`: 감사 로그만 기록

한 정책이 여러 가지를 하면, 나중에 분리하기 어렵다.

### 5. 테스트 용이성
정책 패턴의 큰 장점은 각 정책을 독립적으로 테스트할 수 있다는 것이다:
```python
def test_active_user_policy():
    user = User(name="Bob", roles=[], is_active=False)
    request = Request(user=user, resource="test")
    
    with pytest.raises(PermissionError):
        active_user(user, request)

def test_role_policy():
    user = User(name="Charlie", roles=["user"], is_active=True)
    request = Request(user=user, resource="test")
    
    with pytest.raises(PermissionError):
        role_required("admin")(user, request)
```

### 6. 정책 파이프라인 추상화
정책을 적용하는 방식을 더 유연하게 만들 수 있다:
```python
from functools import reduce

def pipe(user, request, *policies):
    """여러 정책을 순서대로 적용"""
    return reduce(lambda req, policy: policy(user, req), policies, request)

# 사용
result = pipe(user, request, active_user, role_required("admin"), audit)
```

### 7. 정책 조건부 포함
설정에 따라 정책을 동적으로 포함한다:
```python
def create_policies(config):
    policies = []
    if config.auth_required:
        policies.append(active_user)
    if config.role_required:
        policies.append(role_required(config.required_role))
    if config.audit_enabled:
        policies.append(audit)
    return policies
```

## 참고

- **GitHub 저장소**: https://git.arjan.codes/2026/policy — 영상에서 사용한 모든 코드 예제
- **ArjanCodes 강좌**: https://www.arjancodes.com/courses — 더 깊이 있는 소프트웨어 설계 강좌
- **Discord 커뮤니티**: https://discord.arjan.codes — ArjanCodes 커뮤니티에서 질문과 피드백
- **Python typing.Protocol**: https://docs.python.org/3/library/typing.html#typing.Protocol — 프로토콜에 대한 공식 문서
- **dataclasses 모듈**: https://docs.python.org/3/library/dataclasses.html — 데이터클래스 사용법
- **Software Design Mastery**: https://arjan.codes/mastery — 심화 소프트웨어 설계 마스터 프로그램 대기 목록