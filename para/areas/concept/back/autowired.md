---
type: concept
id: autowired
title: 자동 주입 (@Autowired)
aliases:
  - "@Autowired"
  - 자동 주입
  - autowiring
  - "@Qualifier"
  - "@Resource"
up:
  - 2024-10-04-Day88
tags:
  - spring
  - 설계
  - 애노테이션
---

# 자동 주입 (@Autowired)

**어떤 빈을 넣을지 설정에 적지 않고, 「여기에 넣어라」만 표시하면 컨테이너가 타입을 보고 찾아 넣는 것.** `ref="engine"` 이 `@Autowired` 한 줄이 된다.

## 정의

붙일 수 있는 자리가 셋이다.

```java
@Autowired
private Engine engine;                    // 1. 필드

@Autowired
public void setEngine(Engine engine) {    // 2. 세터
  this.engine = engine;
}

public Car(Engine engine) {               // 3. 생성자
  this.engine = engine;
}
```

**생성자는 표식이 없어도 된다** — 기본 생성자가 없으면 컨테이너가 매개변수 있는 생성자를 찾아 부른다.

### 없을 때 어떻게 할 것인가

```java
@Autowired(required = false)   // 못 찾으면 예외 대신 그냥 안 넣는다(null)
```

기본은 `required = true` 라 **없으면 기동이 실패한다.**

### 여럿일 때 어느 것인가

타입만으로는 못 고르므로 이름을 준다.

```java
@Autowired
@Qualifier("dieselEngine")
private Engine engine;
```

자바 표준 애노테이션으로는 한 줄이다.

```java
@Resource(name = "dieselEngine")   // @Autowired + @Qualifier 와 같은 일
```

`@Resource` 는 **스프링이 아니라 자바가 제공**하는 것이라, 프레임워크를 바꿔도 남는다.

## 왜 중요한가

**설정에서 연결선이 사라진다.** XML 시절에는 빈 하나마다 `<property ... ref="...">` 를 적어야 했고, 의존이 늘 때마다 설정도 함께 늘었다. 타입으로 찾게 하면 **연결을 적는 일 자체가 없어진다** → [[bean-definition]] · [[dependency-injection]]

**그리고 자동 주입이 성립하려면 타입이 인터페이스여야 값이 있다.** 구현 클래스로 받으면 갈아 끼울 수 없고, 인터페이스로 받으면 컨테이너에 담긴 구현이 무엇이든 들어온다 → [[interface]] · [[dependency-inversion-principle]]

## 경계와 오해

- **필드 주입은 편하지만 권장되지 않는다** — 필기가 그것을 정확히 적었다: 「인스턴스 변수에 직접 의존 객체를 주입한다는 것은 **캡슐화를 위배**하는 측면이 있기 때문에 "객체지향을 파괴하는 방식"이라는 비난을 받는다」. 실질적인 문제는 **컨테이너 없이는 그 객체를 만들 수 없다**는 것이다 — 시험 코드에서 값을 넣을 방법이 없다 → [[encapsulation]]
- **그래서 생성자 주입이 기본이다** — 만들어진 순간부터 완전하고, `final` 로 둘 수 있고, 컨테이너 없이도 `new Car(engine)` 으로 만들 수 있다 → [[constructor]] · [[immutability]]
- **`required = false` 는 `null` 을 허용하겠다는 선언이다** — 그 필드를 쓰는 모든 자리에서 `null` 검사를 해야 한다. 「없으면 없는 대로」가 정말 맞는지 먼저 따져야 한다 → [[sql-null]]
- **`@Qualifier` 는 이름 계약을 다시 들여온다** — 타입으로 찾게 만들어 놓고 이름을 적는 것이라, 빈 이름을 바꾸면 조용히 깨진다. **구현이 둘로 늘어난 그날부터 생기는 부담**이다 → [[ioc-container]]
- **`@Autowired` 는 스스로 동작하지 않는다** — `AutowiredAnnotationBeanPostProcessor` 가 등록되어야 처리된다. XML 에서는 그 빈을 직접 등록하거나 `<context:annotation-config/>` 를 써야 하고, 안 하면 **표식만 있고 아무 일도 안 일어난다** → [[bean-post-processor]]
- **타입이 같은 빈이 하나뿐일 때만 편하다** — 이 편의는 「후보가 하나」라는 가정 위에 있다. 후보가 없으면 기동 실패, 둘이면 애매해서 실패다. **실패가 기동 시점이라는 것이 그나마 다행이다**

## 함께 보는 개념

- [[dependency-injection]] — 이 표식이 자동화하는 것
- [[bean-post-processor]] — 이 표식을 실제로 처리하는 장치
- [[ioc-container]] — 후보를 고르는 주체
- [[bean-definition]] — 손으로 연결을 적던 쪽
- [[stereotype-annotation]] — 후보가 컨테이너에 들어오는 경로
- [[encapsulation]] — 필드 주입이 위배한다고 지적받는 것
- [[interface]] — 타입 기반 주입이 값을 갖는 조건

## 출처

- [[2024-10-04-Day88]] — 「annotation-config」 절이 **손으로 `ref` 를 적던 XML 에서 `@Autowired` 로 넘어가는 과정**을 단계별로 적었다. 세터·필드·생성자 세 자리를 각각 다루고, **필드 주입에 대해 「캡슐화를 위배하는 측면이 있어 "객체지향을 파괴하는 방식"이라는 비난을 받는다」**고 명시한 것이 이 회차에서 가장 값진 문장이다. `required = false` 의 동작, `@Qualifier` 로 이름을 지정하는 법, **`@Autowired + @Qualifier = @Resource`** 라는 정리, 그리고 `@Resource` 가 스프링이 아니라 자바 제공이라는 구별까지 나온다. 무엇보다 **「`AutowiredAnnotationBeanPostProcessor` 가 생성된 객체에 대해 `@Autowired` 애노테이션을 검사하여 자동 주입하는 일을 한다」**로 그 처리 주체를 짚어, 애노테이션이 마법이 아니라는 것을 보였다. 다만 `@Resource("varName")` 예시는 실제 문법(`name` 속성)과 다르고, 생성자 주입이 왜 권장되는지는 다루지 않았다
