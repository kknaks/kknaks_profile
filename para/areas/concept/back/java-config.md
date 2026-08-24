---
type: concept
id: java-config
title: Java Config (설정을 자바 클래스로 적기)
aliases:
  - Java Config
  - JavaConfig
  - 자바 설정
  - AppConfig
  - "@Bean"
up:
  - 2024-10-01-Day86
  - 2024-10-02-Day87
  - 2024-10-04-Day88
tags:
  - spring
  - 설정
  - 프레임워크
---

# Java Config (설정을 자바 클래스로 적기)

**스프링 설정을 XML 파일이 아니라 자바 클래스에 애노테이션으로 적는 방식.** 같은 것을 두 언어로 적을 수 있고, 무엇이 달라지는지가 이 개념의 몸통이다.

## 정의

세 자리가 정확히 대응한다.

| 하는 일 | XML | Java Config |
|---|---|---|
| 컨테이너 세우기 | `new ClassPathXmlApplicationContext("...xml")` | `new AnnotationConfigApplicationContext(AppConfig.class)` |
| 객체 하나 등록 | `<bean id="c1" class="...Car"/>` | `@Bean public Car c1() { return new Car(); }` |
| 패키지 훑기 | `<context:component-scan base-package="..."/>` | `@ComponentScan("...")` |

**빈의 이름이 어디서 오는지가 갈린다.**

- XML — `id` 속성에 적은 문자열
- Java Config — **메서드 이름**이 곧 빈 이름이다

```java
@Bean
public Car c1() {   // ← 빈 이름이 "c1"
  return new Car();
}
```

## 왜 중요한가

**설정이 컴파일러의 검사를 받게 된다.** XML 의 `class="com.eomcs.spring.ioc.ex01.Car"` 는 문자열이라 오타가 나도 빌드가 되고 **기동할 때** 터진다. `new Car()` 는 클래스 이름이 틀리면 **컴파일이 안 된다** — 리팩터링으로 클래스 이름을 바꿔도 따라온다 → [[refactoring]]

**그리고 설정에 로직을 쓸 수 있다.** 조건에 따라 다른 구현을 돌려주거나, 값을 계산해 넣는 것이 그냥 자바 코드다. XML 에서는 그런 것을 하려면 문법이 하나씩 더 필요했다.

**설정 파일이 하나 줄어든다는 것도 실질적이다.** 이 실습 프로젝트에서 `mybatis-config.xml` 과 `web.xml` 이 차례로 사라지고 `AppConfig` 로 모이는 흐름이 그것이다 → [[mybatis-spring]] · [[web-xml]]

## 경계와 오해

- **`AnnotationConfigApplicationContext` 는 빈 설정 클래스로도 빈을 몇 개 만든다** — 필기가 잡아낸 자리다: 비어 있는 XML 은 빈이 **0개**인데 비어 있는 `AppConfig` 는 **기본 개수**가 잡힌다. 애노테이션 처리를 위해 컨테이너가 **자기 부품을 먼저 등록**하기 때문이고, 「내가 만든 것만 들어 있다」로 읽으면 안 되는 이유다
- **메서드 이름이 계약이 된다** — 빈 이름이 메서드 이름이므로, 이름을 바꾸면 **그 이름으로 찾던 곳이 깨진다.** 컴파일러가 잡아 주는 범위 밖이라 XML 의 `id` 와 같은 종류의 위험이 이름만 옮겨 남는다
- **XML 이 틀린 방식은 아니다** — 설정을 코드와 **완전히 분리해 두는 것**이 목적이면 XML 쪽이 맞다. 다시 컴파일하지 않고 바꿀 수 있다는 것이 그 방식의 값이다
- **`@Bean` 과 `@Component` 는 여전히 갈린다** — Java Config 로 옮겨도 「내 클래스는 스캔, 남의 클래스는 등록」이라는 기준은 그대로다 → [[ioc-container]] · [[stereotype-annotation]]
- **XML 의 네임스페이스가 왜 필요한지는 알아 둘 값이 있다** — `<context:component-scan>` 을 쓰려면 `xmlns:context` 와 `schemaLocation` 을 함께 선언해야 한다. **태그 이름이 어느 명세의 것인지**를 밝히는 장치이고, 자바의 패키지와 같은 역할이다 → [[xml]] · [[package]]

## 함께 보는 개념

- [[ioc-container]] — 이 설정이 채우는 대상
- [[stereotype-annotation]] — 스캔 쪽 표식
- [[xml]] — 반대편 설정 언어
- [[annotation]] — 설정을 코드에 붙이는 장치
- [[externalized-configuration]] — 값만 따로 빼는 세 번째 자리
- [[web-xml]] — 웹 쪽에서 같은 이행이 일어난 자리
- [[classpath]] — XML 설정을 찾는 경로의 근거
- [[bean-definition]] — XML 쪽 문법의 전모
- [[factory-bean]] — XML 이 문법 셋을 쓰던 자리
- [[autowired]] — 설정에서 연결선을 지우는 표식
- [[bean-post-processor]] — `@Configuration` 을 처리하는 장치

## 출처

- [[2024-10-04-Day88]] — 이틀 뒤. **`@Configuration` 이 왜 필요한지가 나온다** — `AnnotationConfigApplicationContext` 에 클래스를 넘길 때는 없어도 되지만 **패키지 이름을 넘기면** 그 클래스를 설정으로 알아보게 하려고 이 표식이 필요하고, 그때는 같은 패키지의 `@Component` 들도 함께 등록된다. `@Bean("이름")` 으로 빈 이름을 직접 주는 법(생략하면 메서드 이름), `@ComponentScan(basePackages = {...}, excludeFilters = ...)` 의 세 가지 사용법, 그리고 `@PropertySource` 로 읽은 값을 **`Environment` 주입 · 필드 `@Value` · 매개변수 `@Value`** 세 방식으로 꺼내는 예제가 함께 실렸다 → [[autowired]] · [[externalized-configuration]]
- [[2024-10-02-Day87]] — 하루 뒤. **XML 쪽을 끝까지 밀어 본 회차**라 이 노트의 비교표가 실물로 채워진다. 별명 구분자, `type` 생략 시 String 우선, `value`/`ref` 의 갈림, `c:`·`p:` 네임스페이스 축약, 팩토리 세 형태 — **전부 XML 이 자바 코드를 쓸 수 없어서 필요해진 문법**이고, Java Config 에서는 `@Bean` 메서드 본문의 평범한 자바 한 줄로 접힌다. 그 대비를 보고 나면 왜 설정이 자바로 옮겨 갔는지가 설명된다 → [[bean-definition]] · [[factory-bean]]
- [[2024-10-01-Day86]] — 「XML파일과 AppConfig.java파일」 절이 **같은 일을 두 방식으로 나란히 적어** 비교한다 — 빈 등록(`<bean id="c1" class="...Car"/>` ↔ `@Bean public Car c1()`), 컴포넌트 스캔(`<context:component-scan base-package="...">` ↔ `@ComponentScan("...")`), 그리고 컨테이너 생성 코드까지. **「XML파일은 0개의 Bean을 생성하지만 AppConfig는 기본 갯수의 Bean을 생성한다」**는 관찰이 이 노트에서 가장 값진 한 줄이고, 실행 결과 스크린샷 둘이 그 근거로 붙어 있다. 「자바 클래스로 설정 정보를 다루는 것을 'Java Config' 라 부른다」로 이름도 명시했다. 다만 예시의 `AppConfig` 에는 `@Configuration` 이 붙어 있지 않고, 빈 이름이 메서드 이름이라는 것의 함의(이름을 바꾸면 깨진다)는 다루지 않았다
