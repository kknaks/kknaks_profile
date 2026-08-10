---
type: concept
id: load-on-startup
title: 서블릿 선행 초기화 (load-on-startup)
aliases:
  - load on startup
  - loadOnStartup
  - 서블릿 선행 초기화
  - 서블릿 조기 로딩
up:
  - 2024-09-05-Day70
tags:
  - web
  - servlet
  - 초기화
---

# 서블릿 선행 초기화 (load-on-startup)

서블릿을 첫 요청까지 미루지 않고 **웹 애플리케이션이 시작될 때 인스턴스화하고 `init()`까지 호출하게 하는 설정.** 느린 첫 요청과 늦게 드러나는 초기화 실패를 기동 시점으로 옮긴다 → [[servlet-lifecycle]]

## 정의

애노테이션과 `web.xml` 중 등록 방식을 따라 한 곳에 적는다.

```java
@WebServlet(value = "/ex06/s1", loadOnStartup = 1)
public class ExampleServlet extends HttpServlet { }
```

```xml
<servlet>
  <servlet-name>example</servlet-name>
  <servlet-class>com.example.ExampleServlet</servlet-class>
  <load-on-startup>1</load-on-startup>
</servlet>
```

값이 **0 이상**이면 컨테이너는 앱 기동 중 해당 서블릿을 준비하고, 여럿이면 작은 수부터
초기화한다. 음수(애노테이션의 기본값 `-1`)면 기본 동작대로 첫 요청 때 준비한다. 숫자는
같은 애플리케이션 안의 선행 초기화 순서일 뿐, HTTP 요청의 처리 우선순위가 아니다.

## 왜 중요한가

초기화가 무거운 서블릿은 첫 사용자가 비용을 내지 않는다. 더 중요한 효과는 실패 위치다.
`init()`에서 설정 파일·의존 객체를 읽다 실패하면, 지연 초기화에서는 특정 URL의 첫 요청이
실패하지만 선행 초기화에서는 배포·기동 로그에서 곧 드러난다. **첫 요청 지연과 오류 발견
지연을 줄이는 대신, 기동 시간과 시작 실패의 범위를 늘리는 맞교환**이다.

## 경계와 오해

- **`load-on-startup` ≠ 요청 실행 우선순위** — `1`이 `2`보다 먼저 준비될 뿐, 이후 들어오는 요청을 먼저 처리한다는 뜻은 아니다. 숫자를 작업 큐 우선순위처럼 읽기 쉬워서 Day70의 「객체 실행 우선순위」 표현이 오해를 부른다.
- **선행 초기화 ≠ 클래스 로딩** — 클래스 로딩은 JVM이 `.class` 정보를 읽는 단계이고, 이 설정은 컨테이너가 서블릿을 만들고 `init()`을 부를 시점을 정한다. 둘 다 "시작할 때"라는 말로 묶여도 대상과 주체가 다르다 → [[class-loading]] · [[servlet-container]]
- **선행 초기화 ≠ 모든 오류 검증** — 컨테이너 생성·`init()` 오류는 앞당겨지지만, 요청 파라미터·로그인 상태·DB의 나중 장애처럼 요청이 있어야 드러나는 문제까지 검사하지는 않는다.
- **`loadOnStartup`을 넣었다고 의존 순서가 자동으로 안전해지지는 않는다** — 수치 순서는 서블릿끼리의 초기화 순서일 뿐, 공유 자원의 준비는 리스너·외부 서비스·실패 처리를 별도로 설계해야 한다 → [[servlet-listener]]

## 함께 보는 개념

- [[servlet-lifecycle]] — 앞당겨지는 `init()`과 기본 첫 요청 생성 시점
- [[servlet-container]] — 실제로 서블릿을 만들고 호출하는 주체
- [[web-xml]] — XML로 설정하는 자리
- [[class-loading]] — 이름은 비슷하지만 JVM 쪽의 다른 단계
- [[servlet-listener]] — 앱 시작 때 공유 자원을 준비하는 다른 콜백

## 출처

- [[2024-09-05-Day70]] — 「서블릿의 생성시기」가 기본 첫 요청 생성, 늦은 오류 검증, 첫 호출 지연을 적고, 「load on startup」이 `@WebServlet(..., loadOnStartup = 1)`과 XML `<load-on-startup>1</load-on-startup>` 두 설정 방식을 보인다
