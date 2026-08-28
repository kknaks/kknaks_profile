# 컨트롤러·서비스·리포지토리를 나누는 이유

> 출처: https://m.youtube.com/watch?v=3OLhaiv0cmQ&pp=ygUh65287Jqw7YSwIOyEnOu5hOyKpCDroIjtj6wg6rWs67O0&ra=m · 개발자 팀 · 10:16 · 2026-06-10

## 요지

- 관심사 분리는 서로 다른 종류의 일을 별도 영역에 배치해 코드가 바뀌는 이유를 하나로 제한하는 설계 원칙이다.
- 계층형 아키텍처에서 컨트롤러는 요청·응답과 검증, 서비스는 비즈니스 흐름과 트랜잭션, 리포지토리는 데이터 접근을 담당한다.
- 의존성은 컨트롤러에서 서비스, 서비스에서 리포지토리로 한 방향으로 흘러야 하며 중간 계층을 건너뛰지 않는다.
- 요청·응답 DTO와 도메인 객체를 구분하면 내부 엔티티 노출과 외부 API 형식에 대한 결합을 막을 수 있다.
- 계층화에는 파일 수와 변환 코드가 늘어나는 비용이 있으므로 단순 CRUD까지 기계적으로 나누기보다 변경과 테스트가 필요한 복잡도에 맞춰 적용해야 한다.

## 개요

한 메서드가 HTTP 요청을 해석하고, 할인 정책을 계산하고, SQL까지 실행한다면 요청 형식·비즈니스 정책·저장 방식 중 어느 하나만 바뀌어도 같은 코드를 수정해야 한다. 웹 서버와 데이터베이스 없이 핵심 규칙만 테스트하거나 다른 진입점에서 같은 규칙을 재사용하기도 어렵다.

관심사 분리(Separation of Concerns)는 이런 서로 다른 변경 이유를 분리한다. 대표적인 구현이 컨트롤러, 서비스, 리포지토리로 구성된 계층형 아키텍처다. 각 계층이 책임과 의존성 경계를 지키면 변경 영향이 국소화되고 단위 테스트와 구현 교체가 쉬워진다.

## 배경 / 사전 지식

관심사는 코드가 해결해야 하는 일의 종류다. 웹 애플리케이션의 대표적인 관심사는 다음과 같다.

- 표현 관심사: HTTP 요청을 읽고 검증하며 적절한 응답 형식과 상태 코드로 변환한다.
- 비즈니스 관심사: 할인, 주문 가능 여부, 재고 차감 순서처럼 업무 규칙과 처리 흐름을 결정한다.
- 영속성 관심사: 데이터를 저장·조회하고 구체적인 데이터베이스 기술과 쿼리를 다룬다.

계층은 같은 성격의 책임을 묶고 서로 다른 책임 사이에 경계를 만든다. 결합도는 한 구성요소가 다른 구성요소의 구체적인 사정을 얼마나 많이 아는지를 뜻한다. 서비스가 SQL이나 HTTP 요청 객체를 직접 알면 표현 또는 저장 기술과 강하게 결합된다. 반대로 인터페이스와 계층 전용 데이터에 의존하면 구체적인 구현을 교체하기 쉽다.

DTO(Data Transfer Object)는 경계 사이에서 데이터를 전달하기 위한 객체다. 엔티티는 보통 영속성 구조와 연결된 내부 모델이고, 도메인 객체는 업무 규칙과 상태를 표현한다. 작은 시스템에서는 하나의 객체가 여러 역할을 겸할 수도 있지만 외부 API와 내부 저장 구조가 서로 다른 속도로 변한다면 역할별 객체를 구분하는 편이 안전하다.

트랜잭션은 여러 데이터 변경을 하나의 작업 단위로 묶는다. 서비스 계층이 트랜잭션 경계를 잡으면 하나의 유스케이스에 포함된 작업을 모두 반영하거나 모두 취소할 수 있다.

## 핵심 개념

### 컨트롤러: 외부와 내부 사이의 통역사

컨트롤러는 요청 DTO를 받고 입력을 검증한 뒤 서비스가 이해할 명령으로 변환한다. 서비스 결과는 응답 DTO와 적절한 HTTP 응답으로 바꾼다. 할인 대상 여부나 주문 가능 여부 같은 업무 판단을 컨트롤러에 넣어서는 안 된다.

컨트롤러를 얇게 유지하면 웹 요청 대신 배치 작업이나 메시지 소비자를 진입점으로 추가하더라도 같은 서비스를 재사용할 수 있다. 비즈니스 정책이 바뀌어도 HTTP 변환 코드에는 영향이 없다.

### 서비스: 유스케이스와 트랜잭션의 경계

서비스는 하나의 업무 흐름을 조율한다. 필요한 도메인 객체를 조회하고, 도메인 규칙을 실행하고, 결과를 저장하며 트랜잭션 범위를 정한다. HTTP 세션이나 요청 객체, 구체적인 SQL을 직접 다루지 않는다.

모든 규칙을 서비스의 조건문으로 작성할 필요는 없다. 주문 금액 계산처럼 특정 도메인 객체가 스스로 지킬 수 있는 불변 조건과 규칙은 도메인 객체에 두고, 서비스는 여러 객체와 저장소가 참여하는 흐름을 조율하면 책임이 더 명확해진다.

### 리포지토리: 데이터 접근의 추상화

리포지토리는 저장과 조회의 계약을 제공한다. 서비스는 `save`나 `findById`가 어떤 SQL, ORM 또는 외부 저장소로 구현되는지 몰라도 된다. 인터페이스 뒤에 실제 DB 구현과 테스트용 메모리 구현을 각각 둘 수 있다.

리포지토리는 데이터 접근 조건을 표현할 수 있지만 할인이나 승인 여부 같은 비즈니스 판단을 맡지 않는다. 저장 기술이나 쿼리가 바뀌는 이유와 업무 정책이 바뀌는 이유를 분리하는 것이 목적이다.

### DTO와 엔티티의 경계

외부 요청은 요청 DTO로 받고 내부에서는 도메인 객체로 처리한 뒤 응답 DTO로 반환한다. 엔티티를 API 응답으로 직접 노출하면 비밀번호나 내부 상태 같은 필드가 뜻하지 않게 직렬화될 수 있다. 테이블 구조 변경이 곧 API 변경으로 이어지고, 지연 로딩 관계나 순환 참조 때문에 직렬화 문제도 생길 수 있다.

DTO는 필요한 필드만 명시하는 허용 목록 역할을 한다. 다만 모든 내부 메서드 호출마다 기계적으로 새 DTO를 만들기보다 외부 API, 애플리케이션, 영속성처럼 변화 주기가 다른 경계에서 변환하는 것이 실용적이다.

### 단방향 의존성

기본 흐름은 `Controller → Service → Repository → Database`이고 응답은 역순으로 돌아온다. 상위 계층은 바로 아래 계층의 계약을 호출하고, 아래 계층은 위 계층을 알지 않는다. 컨트롤러가 서비스를 건너뛰고 리포지토리를 직접 호출하면 비즈니스 경계와 트랜잭션 정책을 우회하게 된다.

구체적인 클래스보다 인터페이스에 의존하면 저장 구현을 교체하거나 테스트 대역을 주입할 수 있다. 의존성 주입은 필요한 협력 객체를 클래스 내부에서 직접 생성하지 않고 외부에서 전달하는 방식이며, 이 단방향 구조를 구성하는 데 유용하다.

### 비용과 적용 기준

계층화는 변경을 격리하고 테스트를 쉽게 하지만 클래스, 파일, 매핑 코드와 간접 호출을 늘린다. 단순한 CRUD 화면에서 각 계층이 아무 판단 없이 같은 데이터를 전달하기만 한다면 추상화 비용이 이점보다 커질 수 있다.

어느 계층에 둘지 판단할 때는 “이 코드가 바뀌는 이유는 무엇인가?”라고 묻는다. 요청·응답 형식 때문에 바뀌면 컨트롤러, 정책과 유스케이스 때문에 바뀌면 서비스나 도메인, 저장 방식 때문에 바뀌면 리포지토리에 둔다.

## 작동 원리

주문 생성 요청은 다음 순서로 처리할 수 있다.

1. 컨트롤러가 JSON을 `CreateOrderRequest`로 변환하고 필수값, 자료형, 범위 같은 형식 검증을 수행한다.
2. 컨트롤러가 요청 DTO를 애플리케이션 내부의 `CreateOrderCommand`로 변환해 서비스에 전달한다.
3. 서비스가 트랜잭션을 시작하고 주문 생성 유스케이스를 조율한다.
4. 도메인 객체가 할인과 최종 금액 계산 등 자신의 업무 규칙을 실행한다.
5. 서비스가 `OrderRepository` 인터페이스를 통해 주문을 저장한다.
6. 실제 리포지토리 구현이 ORM이나 SQL을 이용해 데이터베이스에 접근한다.
7. 저장 결과가 서비스로 돌아오면 트랜잭션이 완료된다. 중간에 예외가 발생하면 전체 변경을 취소한다.
8. 컨트롤러가 서비스 결과를 `CreateOrderResponse`로 변환해 클라이언트에 반환한다.

이 구조에서는 할인 정책을 바꿀 때 도메인 규칙을, JSON 필드명을 바꿀 때 요청·응답 DTO와 컨트롤러를, 데이터베이스를 바꿀 때 리포지토리 구현을 중심으로 수정한다. 각 단계는 인접 계층의 공개 계약만 알기 때문에 변경의 파급 범위가 줄어든다.

## 코드 예시

다음 예제는 Java 17 이상에서 하나의 `Main.java` 파일로 실행할 수 있다. 프레임워크 없이도 컨트롤러, 서비스, 도메인, 리포지토리의 책임과 의존 방향을 보여 준다.

```java
import java.util.LinkedHashMap;
import java.util.Map;

record CreateOrderRequest(int amount) {}
record CreateOrderCommand(int amount) {}
record CreateOrderResult(long id, int finalAmount) {}
record CreateOrderResponse(long id, int finalAmount) {}

final class Order {
    private final int finalAmount;

    private Order(int finalAmount) {
        this.finalAmount = finalAmount;
    }

    static Order create(int amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("amount must be non-negative");
        }
        int discount = amount > 10_000 ? 1_000 : 0;
        return new Order(amount - discount);
    }

    int finalAmount() {
        return finalAmount;
    }
}

interface OrderRepository {
    long save(Order order);
    Order findById(long id);
}

final class InMemoryOrderRepository implements OrderRepository {
    private final Map<Long, Order> orders = new LinkedHashMap<>();
    private long sequence = 0;

    @Override
    public long save(Order order) {
        long id = ++sequence;
        orders.put(id, order);
        return id;
    }

    @Override
    public Order findById(long id) {
        Order order = orders.get(id);
        if (order == null) throw new IllegalArgumentException("order not found");
        return order;
    }
}

final class OrderService {
    private final OrderRepository repository;

    OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    CreateOrderResult place(CreateOrderCommand command) {
        Order order = Order.create(command.amount());
        long id = repository.save(order);
        return new CreateOrderResult(id, order.finalAmount());
    }
}

final class OrderController {
    private final OrderService service;

    OrderController(OrderService service) {
        this.service = service;
    }

    CreateOrderResponse create(CreateOrderRequest request) {
        CreateOrderCommand command = new CreateOrderCommand(request.amount());
        CreateOrderResult result = service.place(command);
        return new CreateOrderResponse(result.id(), result.finalAmount());
    }
}

public class Main {
    public static void main(String[] args) {
        OrderRepository repository = new InMemoryOrderRepository();
        OrderService service = new OrderService(repository);
        OrderController controller = new OrderController(service);

        CreateOrderResponse response =
            controller.create(new CreateOrderRequest(15_000));
        System.out.println(response); // id=1, finalAmount=14000
    }
}
```

컴파일과 실행은 `javac Main.java && java Main`으로 할 수 있다. 컨트롤러는 형식 변환만 수행하고, 서비스는 주문 생성 흐름을 조율하며, 할인 규칙은 `Order`가 갖는다. 서비스는 메모리 저장소의 구현 세부사항이 아니라 `OrderRepository` 인터페이스에 의존한다.

스프링에서는 `OrderController`에 `@RestController`, 서비스에 `@Service`와 `@Transactional`, 실제 리포지토리 구현에 `@Repository`를 적용할 수 있다. 요청 DTO에는 Bean Validation의 `@Valid`, `@PositiveOrZero` 등을 사용한다. 이 애너테이션들은 책임 분리를 대신하지 않으며, 각 책임을 프레임워크의 실행 과정에 연결한다.

## 함정·실수

- 뚱뚱한 컨트롤러: 컨트롤러에서 할인, 권한, 주문 상태 같은 정책을 판단하면 다른 진입점에서 재사용하기 어렵다. 형식 변환과 입력 검증을 제외한 업무 판단은 서비스나 도메인으로 옮긴다.
- 전달만 하는 서비스: 서비스가 리포지토리 호출을 그대로 중계할 뿐 유스케이스나 트랜잭션 경계가 없다면 계층의 가치가 낮다. 필요한 경계인지 검토하고, 핵심 규칙은 적절한 도메인 객체에 둔다.
- 거대한 서비스: 모든 규칙을 서비스 메서드에 쌓으면 데이터만 가진 빈약한 도메인 모델이 된다. 객체가 스스로 지킬 수 있는 불변 조건과 계산 규칙은 도메인에 배치한다.
- 엔티티 직접 노출: 내부 필드 유출, API와 스키마의 결합, 지연 로딩 및 순환 참조 문제가 발생할 수 있다. 명시적인 응답 DTO로 필요한 값만 반환한다.
- 계층 누수: 서비스가 `HttpServletRequest`를 받거나 컨트롤러가 SQL을 알면 기술 관심사가 안쪽으로 침투한다. 계층에 맞는 명령, 결과, 인터페이스를 사용한다.
- 계층 건너뛰기: 컨트롤러가 리포지토리를 직접 호출하면 서비스의 정책과 트랜잭션을 우회한다. 조회처럼 별도의 단순 경로가 필요하다면 우연한 우회가 아니라 명시적인 조회 유스케이스로 설계한다.
- 양방향 의존: 리포지토리가 서비스나 컨트롤러를 참조하면 순환 의존과 변경 전파가 생긴다. 아래 계층은 위 계층을 모르게 한다.
- 과도한 계층화: 변화 가능성이 거의 없는 단순 CRUD에도 일률적으로 객체와 변환 단계를 추가하면 보일러플레이트만 늘어난다. 실제 복잡도와 테스트 요구를 기준으로 경계를 선택한다.
- 검증의 혼동: 문자열 형식이나 필수값 검사는 입력 경계에서 처리하되, “주문을 취소할 수 있는가” 같은 업무 유효성은 서비스 또는 도메인에서 검사한다.

## 베스트 프랙티스

- 코드의 위치는 기술 이름보다 변경 이유를 기준으로 정한다.
- 컨트롤러는 요청·응답 변환과 형식 검증에 집중하고 업무 규칙을 포함하지 않는다.
- 서비스 메서드는 하나의 유스케이스를 표현하고 그 유스케이스에 맞는 트랜잭션 경계를 설정한다.
- 도메인 객체가 스스로 지킬 수 있는 상태 규칙과 불변 조건은 도메인에 둔다.
- 서비스는 구체적인 DB 클래스가 아니라 리포지토리 인터페이스에 의존하고 생성자 주입을 사용한다.
- 외부 경계에는 요청·응답 DTO를 두고 엔티티와 민감한 내부 필드를 직접 노출하지 않는다.
- 단위 테스트에서는 가짜 리포지토리로 서비스와 도메인 규칙을 검증하고, 별도의 통합 테스트에서 실제 DB 매핑과 트랜잭션을 확인한다.
- 계층 사이의 공개 계약을 작게 유지하고 프레임워크 전용 타입이 애플리케이션 핵심부로 퍼지지 않게 한다.
- 단순 CRUD는 더 작은 구조로 시작하되 정책, 트랜잭션, 재사용 또는 독립 테스트의 필요가 생기면 경계를 분리한다.
- 계층을 추가했을 때 변경 격리와 테스트 가능성이 실제로 개선되는지 검토하고 의미 없는 전달 계층은 합치거나 제거한다.

## 참고

(영상 내 명시 없음)
