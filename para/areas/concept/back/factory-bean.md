---
type: concept
id: factory-bean
title: 팩토리로 빈 만들기 (factory-method · FactoryBean)
aliases:
  - FactoryBean
  - factory-method
  - factory-bean
  - 팩토리 메서드
up:
  - 2024-10-02-Day87
tags:
  - spring
  - 생성
  - 설계
---

# 팩토리로 빈 만들기 (factory-method · FactoryBean)

**생성자로 만들 수 없는 객체를 컨테이너에 담는 방법.** 「이 클래스를 `new` 해라」가 아니라 「이 메서드를 불러서 나온 것을 담아라」로 적는다.

## 정의

세 가지 형태가 있다.

### 1. 정적 팩토리 메서드 — `factory-method`

```xml
<bean id="date" class="java.sql.Date" factory-method="valueOf">
  <constructor-arg value="2024-03-11"/>
</bean>
```

`new java.sql.Date(...)` 가 아니라 `java.sql.Date.valueOf("2024-03-11")` 이 불린다. **`class` 는 만들 것이 아니라 메서드를 가진 클래스**이고, 담기는 것은 그 **반환값**이다 → [[date-time]]

### 2. 인스턴스 팩토리 메서드 — `factory-bean` + `factory-method`

```xml
<bean id="carFactory" class="...CarFactory"/>

<bean id="c1" factory-bean="carFactory" factory-method="create">
  <constructor-arg value="소나타"/>
</bean>
```

**팩토리 객체를 먼저 빈으로 만들고**, 그 객체의 메서드를 불러 나온 것을 다시 빈으로 담는다. `class` 속성이 아예 없다는 것이 눈에 띄는 차이다.

### 3. `FactoryBean` 인터페이스 구현

```java
public class CarFactory implements FactoryBean<Car> {
  private String varName;               // 세터로 값을 받는다

  @Override
  public Car getObject() throws Exception { ... }     // 만들어 돌려줄 객체

  @Override
  public Class<?> getObjectType() { return Car.class; }  // 그 객체의 타입
}
```

```xml
<bean id="c1" class="...CarFactory">
  <property name="varName" value="소나타"/>
</bean>
```

**여기서 반전이 일어난다** — `class` 는 팩토리인데 `getBean("c1")` 이 돌려주는 것은 **`Car`** 다. 컨테이너가 이 인터페이스를 알아보고 `getObject()` 를 대신 불러 준다.

## 왜 중요한가

**「생성자로 만들 수 있는 것」만 컨테이너에 담을 수 있다면 담을 수 없는 것이 너무 많다.** 생성자가 `private` 인 클래스, 정적 메서드로만 만드는 클래스, 만드는 데 여러 단계가 필요한 객체가 전부 그렇다 → [[singleton-pattern]] · [[constructor]]

`SqlSessionFactoryBean` 이 정확히 세 번째 형태다 — 이름에 `FactoryBean` 이 붙어 있고, 등록하면 `SqlSessionFactory` 가 담긴다. **Day83 에서 `factoryBean.getObject()` 를 손으로 부른 그 메서드**가 이 인터페이스의 것이다 → [[mybatis-spring]]

## 경계와 오해

- **`FactoryBean` 을 등록하면 담기는 것은 팩토리가 아니다** — `getBean("c1")` 이 `CarFactory` 가 아니라 `Car` 를 돌려준다. **팩토리 자체가 필요하면 `getBean("&c1")` 처럼 `&` 를 붙여야 한다**
- **`FactoryBean` ≠ `BeanFactory`** — 이름이 뒤집혀 있을 뿐인데 완전히 다르다. `BeanFactory` 는 **컨테이너**이고 `FactoryBean` 은 **빈 하나를 만드는 도구**다 → [[ioc-container]]
- **`factory-method` 를 쓰면 `class` 의 의미가 바뀐다** — 보통은 「만들 클래스」인데 여기서는 「메서드를 가진 클래스」다. 담기는 것은 반환 타입이라 **`class` 만 보고 타입을 짐작하면 틀린다**
- **팩토리 메서드도 생성자와 같은 형변환 규칙을 받는다** — `<constructor-arg>` 로 넘긴 문자열이 매개변수 타입으로 변환되고, 안 되면 예외다 → [[bean-definition]]
- **[[java-config]] 에서는 이 셋이 전부 `@Bean` 메서드 하나로 접힌다** — `@Bean public Date date() { return Date.valueOf("2024-03-11"); }` 면 끝이다. **XML 이 문법을 세 개 필요로 했던 이유가 「자바 코드를 쓸 수 없어서」**라는 것이 여기서 드러난다

## 함께 보는 개념

- [[bean-definition]] — 이 방식이 놓이는 태그
- [[ioc-container]] — 팩토리를 알아보는 주체
- [[java-config]] — 같은 일을 메서드 하나로 접는 쪽
- [[mybatis-spring]] — `FactoryBean` 이 실제로 쓰인 자리
- [[singleton-pattern]] — 생성자가 막혀 있는 대표 사례
- [[constructor]] — 이 방식이 우회하는 것

## 출처

- [[2024-10-02-Day87]] — 「팩토리 메서드를 통해 객체 만들기」 절이 세 형태를 순서대로 보인다. **정적 메서드**의 예로 `<bean id="date" class="java.sql.Date" factory-method="valueOf">` 를 든 것이 좋은 선택이다 — `java.sql.Date` 는 생성자가 deprecated 라 실제로 팩토리가 필요한 클래스다. **인스턴스 메서드** 쪽은 `factory-bean` + `factory-method` 조합으로 팩토리 객체를 먼저 만든다는 것을, **`FactoryBean` 구현** 쪽은 `getObject()`·`getObjectType()` 두 오버라이드로 「객체 정보와 클래스명을 리턴한다」는 것을 적었다. 다만 `FactoryBean` 을 등록했을 때 `getBean()` 이 팩토리가 아니라 **만들어진 객체**를 돌려준다는 반전 — 이 인터페이스의 핵심 — 은 명시되지 않았고, `BeanFactory` 와 이름이 뒤집혀 있다는 주의도 없다
