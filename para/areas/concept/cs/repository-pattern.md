---
type: concept
id: repository-pattern
title: 리포지토리 패턴 (Repository Pattern)
aliases:
  - 리포지토리 패턴
  - 저장소 패턴
  - Repository Pattern
  - Repository
  - 리포지터리
up:
  - C-038-separating-controller-service-and-repository-responsibilities
tags:
  - 설계
  - 영속성
  - 데이터 접근
  - 추상화
---

# 리포지토리 패턴 (Repository Pattern)

**도메인 객체의 저장과 조회를 컬렉션을 다루는 것 같은 계약으로 추상화하는 패턴.** 비즈니스 코드는 데이터가 SQL, ORM, 메모리 또는 외부 저장소 중 어디에 어떻게 보관되는지 알지 않고 `save`나 `findById` 같은 도메인 언어로 접근한다.

## 정의

리포지토리는 도메인 또는 서비스가 필요로 하는 저장·조회 연산을 인터페이스로 표현하고, 구체적인 저장 기술은 구현체 안에 감춘다.

```java
interface OrderRepository {
    Order save(Order order);
    Optional<Order> findById(long id);
}
```

서비스는 이 계약에 의존한다. 운영 환경에서는 JPA나 SQL 구현을, 단위 테스트에서는 메모리 구현을 주입할 수 있다.

```text
OrderService → OrderRepository ← JpaOrderRepository
                              ← InMemoryOrderRepository
```

리포지토리의 책임은 다음과 같다.

1. 도메인 객체를 저장하고 식별자로 다시 찾는다.
2. 도메인에 의미 있는 조회 계약을 제공한다.
3. SQL, ORM 세션, 연결과 같은 영속성 세부사항을 구현 안에 가둔다.
4. 저장 결과를 도메인 또는 애플리케이션이 이해하는 타입으로 반환한다.

## 사용 예시

다음 메모리 구현은 DB 없이 서비스를 시험할 때 사용할 수 있다.

```java
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

interface OrderRepository {
    long save(Order order);
    Optional<Order> findById(long id);
}

final class InMemoryOrderRepository implements OrderRepository {
    private final Map<Long, Order> orders = new LinkedHashMap<>();
    private long sequence;

    @Override
    public long save(Order order) {
        long id = ++sequence;
        orders.put(id, order);
        return id;
    }

    @Override
    public Optional<Order> findById(long id) {
        return Optional.ofNullable(orders.get(id));
    }
}
```

서비스는 `InMemoryOrderRepository`라는 이름을 알지 않고 `OrderRepository`만 받는다. 실제 DB 구현으로 교체해도 서비스의 할인이나 주문 정책은 바뀌지 않는다. 쿼리를 최적화하거나 ORM을 바꾸는 변경도 구현체 안에 머문다.

## 왜 중요한가

서비스가 SQL과 ORM API를 직접 다루면 비즈니스 흐름과 저장 기술이 한 코드에 섞인다. 핵심 정책만 시험하려 해도 DB 연결이 필요하고, 저장 기술을 교체하거나 쿼리를 변경할 때 서비스까지 수정해야 한다.

리포지토리 인터페이스를 두면 서비스는 저장 방식과 독립적으로 유스케이스를 표현할 수 있다. 테스트 대역을 주입해 정책과 흐름을 빠르게 단위 테스트할 수 있고, 데이터 접근 예외와 반환형을 애플리케이션 경계에 맞게 통제할 수 있다.

## 경계와 오해

- **Repository ≠ 데이터베이스 그 자체** — 리포지토리는 DB 연결 객체가 아니라 도메인이 저장소에 접근하는 계약이다. 구현은 DB가 아닌 메모리나 외부 API일 수도 있다.
- **Repository ≠ Service** — 리포지토리는 저장·조회만 맡고 할인, 승인 여부, 트랜잭션 유스케이스 같은 업무 판단은 서비스나 도메인이 맡는다 → [[service-layer]].
- **Repository ≠ DAO** — [[dao-pattern]]은 주로 테이블과 데이터 접근 절차를 감싸고, 리포지토리는 도메인 객체의 집합처럼 보이는 계약을 지향한다. 실무에서는 두 이름을 같은 의미로 쓰기도 하므로 이름보다 반환형과 책임을 확인해야 한다.
- **인터페이스 선언만으로 교체 가능성이 생기지는 않는다** — 서비스가 구현체를 직접 생성하면 구체 클래스 의존이 남는다. 외부 조립과 [[dependency-injection]]이 함께 필요하다.
- **모든 쿼리를 범용 메서드 하나로 감추면 좋은 추상화가 아니다** — 문자열 SQL이나 임의 조건 맵을 위 계층에서 받기 시작하면 저장 기술이 다시 새어 나온다. 실제 유스케이스에 의미 있는 조회 계약을 제공한다.
- **리포지토리가 트랜잭션 전체를 결정해서는 안 된다** — 여러 리포지토리를 묶는 작업 단위는 유스케이스를 아는 서비스 계층이 정한다.
- **Spring Data가 구현을 생성해 준다 ≠ 설계 비용이 0이다** — 메서드 이름, 조회 경계, 엔티티 노출 여부와 트랜잭션 위치는 여전히 설계해야 한다.

## 함께 보는 개념

- [[layered-architecture]] — 리포지토리가 영속성 책임을 맡는 대표적인 배치
- [[service-layer]] — 리포지토리들을 조율하고 트랜잭션 경계를 정하는 위 계층
- [[dao-pattern]] — 저장 접근을 감추지만 추상화의 관점이 다른 인접 패턴
- [[dependency-inversion-principle]] — 서비스가 구체 구현 대신 리포지토리 계약에 의존하게 하는 원칙
- [[dependency-injection]] — 운영·테스트 구현을 외부에서 주입하는 수단
- [[transaction]] — 여러 저장 연산을 하나의 작업으로 묶는 경계

## 출처

- [[C-038-separating-controller-service-and-repository-responsibilities]] — 서비스가 저장 위치와 방법을 모른 채 인터페이스의 `save`를 호출하고, 실제 DB 구현과 테스트용 메모리 구현을 교체하는 구조를 설명한다.
