---
type: concept
id: spring-framework
title: 스프링 프레임워크 (Spring Framework)
aliases:
  - Spring
  - 스프링
  - Spring Framework
  - spring-webmvc
up:
  - 2024-09-25-Day82
  - 2024-10-18-Day96
tags:
  - java
  - web
  - 프레임워크
---

# 스프링 프레임워크 (Spring Framework)

**애플리케이션의 뼈대를 미리 만들어 두고, 그 안에 우리 클래스를 끼우게 하는 자바 프레임워크.** 객체 생성·연결(IoC)과 웹 요청 처리(MVC)가 두 기둥이다.

## 정의

이 회차에서 스프링을 처음 쓰는 방식이 그 성격을 보여 준다 — **손으로 만들어 둔 것을 하나씩 지우고 그 자리에 스프링 것을 넣는다.**

| 지운 것 (직접 만든 것) | 넣은 것 (스프링) |
|---|---|
| `ApplicationContext` | `AnnotationConfigWebApplicationContext` → [[ioc-container]] |
| `DispatcherServlet` | `DispatcherServlet` → [[dispatcher-servlet]] |
| `CharacterEncodingFilter` | 스프링이 제공하는 같은 이름의 필터 → [[servlet-filter]] |
| 직접 만든 `@Component` 애노테이션 | `org.springframework.stereotype.Component` → [[stereotype-annotation]] |

**이름이 거의 그대로다.** 앞 회차들에서 만든 것과 스프링의 것이 같은 이름·같은 역할이라, 갈아 끼우는 것이 import 문 교체에 가깝다.

버전이 **자바 EE 세대로 갈린다.**

| 스프링 | 기반 |
|---|---|
| 6.x | Jakarta EE 9 (`jakarta.*`) |
| 5.x | Java EE 8 (`javax.*`) |

```gradle
implementation 'org.springframework:spring-webmvc:5.3.39'
```

패키지 이름이 `javax` 냐 `jakarta` 냐가 갈리므로, **버전을 잘못 고르면 서블릿 API 자체가 안 맞는다** → [[java-ee]]

## 왜 중요한가

**「직접 만들어 본 뒤에 갈아 끼운다」는 것이 이 회차의 배치다.** Day61~75 에서 IoC 컨테이너·프론트 컨트롤러·애노테이션 처리를 손으로 만들었고, 여기서 그것들이 통째로 라이브러리로 대체된다. 그래서 스프링의 각 부품이 **무엇을 대신하고 있는지**를 이미 알고 시작한다 → [[dynamic-proxy]] · [[reflective-annotation-access]]

이 순서가 아니면 스프링은 「그냥 되는 것」이 되고, 안 될 때 볼 곳을 모른다.

**프레임워크와 라이브러리의 차이도 여기서 드러난다.** 라이브러리는 내가 부르는 것이고, 프레임워크는 **나를 부르는 것**이다. `@Controller` 를 붙인 메서드를 내가 부르지 않는다 — 스프링이 요청을 받아 그것을 부른다 → [[template-method-pattern]]

## 경계와 오해

- **스프링 = Spring Boot 가 아니다** — 이 회차가 쓰는 것은 스프링 프레임워크이고, `web.xml`·`AppConfig`·`ContextLoaderListener` 를 직접 쓴다. 부트는 그 설정을 자동화한 위층이라 아직 나오지 않았다
- **`@EnableWebMvc` 는 「MVC 를 켜는 스위치」가 아니다** — 필기가 「MVC 와 관련된 여러 설정을 자동으로 적용」이라 적었는데, 정확히는 **기본 설정 묶음을 등록**하는 것이다. 이것 없이도 `DispatcherServlet` 은 돌고, 붙이면 메시지 컨버터·핸들러 매핑 같은 것이 기본값으로 채워진다
- **버전 숫자보다 패키지 접두어가 실제 갈림이다** — 5.x/6.x 라는 숫자보다 `javax.servlet` ↔ `jakarta.servlet` 이 코드에 나타나는 차이다. 톰캣 버전도 여기에 맞춰야 한다 → [[tomcat]]
- **프레임워크를 쓴다고 설계가 좋아지지 않는다** — 갈아 끼운 것은 부품이고, [[service-layer]]·[[mvc-pattern]] 의 배치는 앞 회차에서 이미 정해 둔 것이다. 스프링은 그 배치를 **쉽게 만들 뿐 강제하지 않는다**

## 함께 보는 개념

- [[ioc-container]] — 객체를 만들고 연결하는 기둥
- [[dispatcher-servlet]] — 웹 요청을 받는 기둥
- [[stereotype-annotation]] · [[request-mapping]] — 우리 클래스를 프레임워크에 등록하는 표식
- [[dependency-injection]] — 이 프레임워크가 성립시키는 원리
- [[java-ee]] — `javax`/`jakarta` 가 갈리는 근거
- [[front-controller]] — 스프링이 대신 구현해 주는 패턴
- [[spring-boot]] — 이 프레임워크의 설정을 기본값으로 미는 위층

## 출처

- [[2024-10-18-Day96]] — 삼 주 뒤. **이 노트의 「스프링 = 부트가 아니다」가 뒤집히는 자리**다. `web.xml`·`AppConfig`·`ContextLoaderListener` 를 직접 쓰던 것이 `build.gradle` 의 스타터 몇 줄과 `application.properties` 한 파일이 된다. **Day82~95 에서 손으로 만든 것이 무엇이었는지 알고 나서 그것이 사라지는** 순서라, 「자동으로 된다」가 무엇을 대신하는지가 보인다 → [[spring-boot]]
- [[2024-09-25-Day82]] — 「Spring Framework」 절이 `spring-webmvc:5.3.39` 의존성 한 줄과 **버전-EE 대응(6.x ↔ Jakarta EE 9, 5.x ↔ Java EE 8)**을 적고, 「스프링 프레임워크 적용」이 일곱 걸음에 걸쳐 **직접 만든 클래스를 지우고 스프링 것으로 바꾸는 과정**을 기록한다 — IOC 컨테이너 · Front Controller · Filter · 애노테이션 · Service · PageController · AppConfig 순이다. 「기존 ~ 클래스 삭제」라는 문장이 반복되는 것이 이 회차의 성격을 그대로 보인다. 다만 프레임워크와 라이브러리의 차이, `@EnableWebMvc` 가 실제로 무엇을 등록하는지는 다루지 않았고, 코드에 오타가 여럿 있다(`serSevletContext`, `@EnableWebMVC`, `mb.setViewName`)
