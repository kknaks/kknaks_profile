---
type: concept
id: layered-architecture
title: 계층형 아키텍처 (Layered Architecture)
aliases:
  - 계층형 아키텍처
  - 계층 아키텍처
  - 레이어드 아키텍처
  - Layered Architecture
  - n-tier architecture
up:
  - C-038-separating-controller-service-and-repository-responsibilities
tags:
  - 아키텍처
  - 계층
  - 의존성
  - 책임 분리
---

# 계층형 아키텍처 (Layered Architecture)

**성격이 비슷한 책임을 수평 계층으로 묶고 계층 사이의 호출과 의존 방향을 제한하는 아키텍처.** 웹 애플리케이션에서는 흔히 컨트롤러, 서비스, 리포지토리 계층으로 표현·비즈니스·영속성 관심사를 나눈다.

## 정의

기본적인 요청 흐름은 다음과 같다.

```text
Client → Controller → Service → Repository → Database
Client ← Controller ← Service ← Repository ← Database
```

각 계층은 고유한 책임을 갖는다.

| 계층 | 해야 하는 일 | 경계 밖의 일 |
|---|---|---|
| Controller | 요청·응답 변환, 형식 검증, 상태 코드 결정 | 업무 정책 판단, SQL 실행 |
| Service | 유스케이스 조율, 비즈니스 흐름, 트랜잭션 경계 | HTTP 객체 처리, 구체적인 SQL 실행 |
| Repository | 도메인 객체 저장·조회, 저장소 접근 추상화 | 화면 형식 결정, 비즈니스 정책 판단 |

일반적인 규칙은 다음과 같다.

1. 상위 계층은 바로 아래 계층의 공개 계약을 통해 요청한다.
2. 아래 계층은 위 계층의 타입과 기술을 알지 않는다.
3. 컨트롤러가 서비스 계층을 건너뛰어 저장소를 직접 호출하지 않는다.
4. 정책 코드는 구체적인 저장 구현보다 인터페이스 같은 추상화에 의존한다.
5. 외부 형식과 내부 모델의 변화 주기가 다르면 [[dto]]로 경계를 만든다.

## 사용 예시

주문 생성 유스케이스는 다음과 같이 배치할 수 있다.

```java
record CreateOrderRequest(int amount) {}
record CreateOrderResult(long id, int finalAmount) {}

interface OrderRepository {
    long save(Order order);
}

final class OrderService {
    private final OrderRepository repository;

    OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    CreateOrderResult place(int amount) {
        Order order = Order.create(amount);
        long id = repository.save(order);
        return new CreateOrderResult(id, order.finalAmount());
    }
}

final class OrderController {
    private final OrderService service;

    OrderController(OrderService service) {
        this.service = service;
    }

    CreateOrderResult create(CreateOrderRequest request) {
        return service.place(request.amount());
    }
}
```

컨트롤러는 요청을 내부 호출로 변환하고, 서비스는 주문 생성 흐름을 조율하며, 리포지토리는 저장을 담당한다. 할인 정책이 바뀌면 `Order`를, HTTP 형식이 바뀌면 컨트롤러와 요청 DTO를, 저장 기술이 바뀌면 리포지토리 구현을 중심으로 수정한다.

## 왜 중요한가

계층을 지키면 서로 다른 변경이 한 파일에 모이지 않는다. 서비스가 HTTP를 모르므로 같은 유스케이스를 배치나 메시지 소비자에서도 호출할 수 있고, 리포지토리 인터페이스에 테스트 대역을 넣어 데이터베이스 없이 업무 흐름을 시험할 수 있다.

서비스가 트랜잭션 경계를 소유하면 여러 저장 작업을 하나의 유스케이스 단위로 묶을 수 있다. 아래 계층이 위 계층을 모르는 단방향 의존성은 순환 의존을 막고 내부 정책이 특정 표현 기술에 묶이는 것을 방지한다.

## 경계와 오해

- **계층형 아키텍처 ≠ 물리적 다중 티어** — 논리 계층은 같은 프로세스에서 실행될 수 있다. 웹 서버와 DB 서버처럼 배포 위치를 나누는 티어와 책임을 나누는 레이어는 구별해야 한다.
- **응답이 역방향으로 돌아온다 ≠ 아래 계층이 위 계층에 의존한다** — 반환값은 호출 스택을 거슬러 오지만, 리포지토리가 컨트롤러 타입을 참조할 필요는 없다.
- **항상 바로 아래 계층만 호출해야 한다는 규칙은 절대 법칙이 아니다** — 단순 조회를 별도 경로로 최적화하는 구조도 있다. 다만 우연히 계층을 우회하지 말고 별도의 계약과 책임으로 명시해야 한다.
- **얇은 서비스 ≠ 무조건 잘못된 서비스** — 단순 조회에서는 서비스가 얇을 수 있다. 반대로 조율할 책임이 있는데도 컨트롤러가 여러 리포지토리를 직접 부른다면 계층 경계가 무너진 것이다 → [[service-layer]].
- **엔티티를 모든 계층의 공용 객체로 쓰면 경계가 사라질 수 있다** — 특히 외부 응답에 영속성 엔티티를 직접 노출하면 내부 스키마와 API가 결합된다 → [[dto]].
- **계층 수가 많을수록 좋은 것이 아니다** — 계층마다 변환과 간접 호출 비용이 생긴다. 변경 가능성과 독립 테스트 필요가 작은 기능은 단순한 구조가 낫다.

## 함께 보는 개념

- [[separation-of-concerns]] — 계층으로 구현하려는 상위 설계 원칙
- [[service-layer]] — 업무 흐름과 트랜잭션 경계를 맡는 가운데 계층
- [[repository-pattern]] — 저장소 접근을 도메인 친화적인 계약으로 감추는 아래 계층
- [[dto]] — 외부 표현과 내부 모델 사이의 데이터 경계
- [[dependency-inversion-principle]] — 구체적인 아래층 구현 대신 추상화에 의존하게 하는 원칙
- [[coupling]] — 계층 분리가 줄이려는 변경 전파의 축

## 출처

- [[C-038-separating-controller-service-and-repository-responsibilities]] — 컨트롤러·서비스·리포지토리의 책임, 단방향 의존성, 계층 건너뛰기 금지와 계층화의 비용을 주문 생성 예제로 설명한다.
