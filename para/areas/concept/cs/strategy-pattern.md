---
type: concept
id: strategy-pattern
title: 전략 패턴 (Strategy Pattern)
aliases:
  - 전략 패턴
  - 전략패턴
  - 스트래티지 패턴
up:
  - C-036-design-patterns-for-spring-boot
tags:
  - 디자인패턴
  - 행동패턴
  - 다형성
  - 객체지향
---

# 전략 패턴 (Strategy Pattern)

**서로 교체할 수 있는 알고리즘들을 공통 인터페이스 뒤의 별도 객체로 분리하고, 사용하는 쪽이 필요한 구현을 선택하거나 주입받게 하는 행동 디자인 패턴.** 알고리즘이 늘어날 때 호출부의 조건문을 계속 수정하지 않고 새 전략을 추가할 수 있게 한다.

## 정의

전략 패턴은 세 역할로 구성된다.

| 역할 | 책임 |
|---|---|
| Strategy | 교체 가능한 알고리즘들이 지킬 공통 연산을 선언한다 |
| Concrete Strategy | 각 알고리즘을 독립적으로 구현한다 |
| Context | 구체적인 알고리즘 대신 Strategy를 보유하고 작업을 위임한다 |

최소 골격은 다음과 같다.

```java
interface Strategy {
    Result execute(Input input);
}

final class ConcreteStrategy implements Strategy {
    @Override
    public Result execute(Input input) {
        return new Result(input);
    }
}

final class Context {
    private final Strategy strategy;

    Context(Strategy strategy) {
        this.strategy = strategy;
    }

    Result run(Input input) {
        return strategy.execute(input);
    }
}

record Input(String value) {}
record Result(Input input) {}
```

`Context`는 어떤 구체 클래스가 작업하는지 알지 않고 `Strategy` 계약에만 의존한다. 전략의 선택은 생성자 인자, 설정, 팩토리 또는 의존성 주입 컨테이너처럼 컨텍스트 바깥의 조립 지점으로 이동한다.

## 사용 예시

고객 유형마다 할인 계산식이 달라지는 경우 각 계산식을 전략으로 분리할 수 있다.

```java
import java.util.Map;

interface DiscountStrategy {
    int apply(int price);
}

final class RegularDiscount implements DiscountStrategy {
    @Override
    public int apply(int price) {
        return price;
    }
}

final class VipDiscount implements DiscountStrategy {
    @Override
    public int apply(int price) {
        return (int) (price * 0.8);
    }
}

final class PriceCalculator {
    private final Map<String, DiscountStrategy> strategies;

    PriceCalculator(Map<String, DiscountStrategy> strategies) {
        this.strategies = Map.copyOf(strategies);
    }

    int calculate(String customerType, int price) {
        DiscountStrategy strategy = strategies.get(customerType);
        if (strategy == null) {
            throw new IllegalArgumentException(
                "Unknown customer type: " + customerType
            );
        }
        return strategy.apply(price);
    }
}

public class Main {
    public static void main(String[] args) {
        PriceCalculator calculator = new PriceCalculator(Map.of(
            "regular", new RegularDiscount(),
            "vip", new VipDiscount()
        ));

        System.out.println(calculator.calculate("regular", 10_000)); // 10000
        System.out.println(calculator.calculate("vip", 10_000));     // 8000
    }
}
```

`PriceCalculator`는 할인 공식을 직접 구현하지 않고 선택한 `DiscountStrategy`에 계산을 위임한다. 새 할인 정책은 인터페이스 구현과 등록 항목을 추가해 확장할 수 있으며, 기존 계산 흐름은 유지된다.

스프링에서는 각 전략 구현을 빈으로 등록하고 `Map<String, DiscountStrategy>`를 생성자로 주입받아 같은 구조를 만들 수 있다. 전략 빈을 기본 싱글톤 스코프로 공유한다면 요청별 데이터를 필드에 보관하지 않는 무상태 객체로 설계해야 한다.

## 왜 중요한가

알고리즘별 분기가 하나의 거대한 조건문에 모이면 정책을 추가할 때마다 기존 코드를 수정해야 하고, 서로 다른 정책의 테스트도 얽힌다. 전략 패턴은 각 정책을 독립된 단위로 분리해 추가·교체·테스트할 수 있게 한다.

호출자는 구체 구현이 아니라 공통 계약을 알기 때문에 [[coupling]]의 대상을 구현 클래스에서 인터페이스로 옮길 수 있다. 새 구현을 추가하면서 기존 컨텍스트를 바꾸지 않을 수 있다는 점에서는 [[open-closed-principle]]과도 연결된다.

## 경계와 오해

- **전략 패턴 ≠ 조건문 제거 자체** — 어떤 전략을 선택하는 판단은 조립 지점이나 팩토리에 남는다. 핵심은 선택 이후의 알고리즘 구현과 사용 코드를 분리하는 것이다.
- **전략 패턴 ≠ 상태 패턴** — 전략은 대개 외부에서 목적에 맞는 알고리즘을 선택한다. 상태 패턴은 객체의 내부 상태가 바뀜에 따라 행동 객체가 전환되는 구조다.
- **인터페이스 사용 ≠ 자동으로 전략 패턴** — 구현들이 동일한 알고리즘 역할로 교체될 수 있고 컨텍스트가 그 계약에 작업을 위임해야 한다.
- **전략 클래스가 많을수록 항상 좋지는 않다** — 분기가 작고 변경 가능성이 낮다면 클래스 증가와 조립 비용이 얻는 유연성보다 클 수 있다.
- **전략 선택 키를 구현 곳곳에 흩뜨리면 결합이 되살아난다** — 문자열이나 타입에 따른 선택은 한 조립 지점에 모으고, 알 수 없는 키는 명시적으로 처리한다.
- **공유 전략의 변경 가능한 필드는 동시성 문제를 만든다** — 특히 싱글톤 빈으로 관리할 때 입력과 중간 결과는 메서드 인자와 지역 변수로 다룬다.

## 함께 보는 개념

- [[design-pattern]] — 전략 패턴이 속하는 더 큰 개념
- [[coupling]] — 구현 대신 전략 인터페이스에 의존해 조절하는 설계 축
- [[polymorphism]] — 같은 전략 계약으로 서로 다른 알고리즘을 실행하게 하는 성질
- [[dependency-inversion-principle]] — 상위 정책이 구체 구현보다 추상화에 의존하도록 하는 원칙
- [[open-closed-principle]] — 기존 컨텍스트 수정 없이 전략을 추가하려는 방향
- [[singleton-pattern]] — 스프링에서 전략 빈을 공유할 때 구분해야 하는 객체 생성 패턴

## 출처

- [[C-036-design-patterns-for-spring-boot]] — 할인 정책을 `DiscountStrategy` 구현으로 분리하고 맵으로 조립하는 Java 예제를 통해 전략 교체와 스프링 의존성 주입 적용 방법을 보여 준다.
