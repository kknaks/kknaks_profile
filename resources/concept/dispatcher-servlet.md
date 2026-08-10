---
type: concept
id: dispatcher-servlet
title: DispatcherServlet
aliases:
  - DispatcherServlet
  - 디스패처 서블릿
  - HandlerMapping
up:
  - 2024-09-25-Day82
tags:
  - web
  - spring
  - 프레임워크
---

# DispatcherServlet

**스프링 MVC 의 프론트 컨트롤러.** 모든 요청을 받아 어느 컨트롤러의 어느 메서드가 처리할지 고르고, 결과를 뷰로 넘긴다.

## 정의

앞 회차에서 손으로 만든 프론트 컨트롤러와 하는 일이 같다 → [[front-controller]]

1. 요청을 받는다 (단일 진입점)
2. 요청 정보를 보고 **컨트롤러를 고른다**
3. 그 컨트롤러의 **실행할 메서드를 고른다**
4. 메서드를 부르고, 돌려받은 뷰 이름으로 화면을 정한다 → [[view-resolver]]

세우는 방법은 컨테이너를 넘겨 주는 것뿐이다.

```java
DispatcherServlet dispatcherServlet = new DispatcherServlet(iocContainer);
```

**컨테이너를 받는다는 것이 핵심이다** — 어느 클래스가 컨트롤러인지, 어떤 URL 을 맡는지는 전부 그 컨테이너에 담긴 빈에서 읽는다 → [[ioc-container]] · [[request-mapping]]

## 왜 중요한가

**요청 하나가 어디를 거치는지가 여기서 정해진다.** 스프링 웹에서 「왜 이 메서드가 안 불리지」·「왜 404 가 뜨지」의 답은 거의 항상 이 서블릿의 단계 중 하나다 — 매핑을 못 찾았거나, 파라미터를 못 만들었거나, 뷰 이름을 못 풀었거나.

그리고 **공통 처리를 넣을 자리를 제공한다.** 모든 요청이 여기를 지나므로 인증·로깅·예외 처리를 한 곳에서 걸 수 있다 — 손으로 만들 때 얻으려던 것과 같다 → [[servlet-filter]]

## 경계와 오해

- **이름이 [[request-dispatcher]] 와 겹치지만 다른 것이다** — `RequestDispatcher` 는 서블릿 API 의 위임 도구이고, `DispatcherServlet` 은 **스프링이 만든 서블릿 하나**다. Day75 필기가 프론트 컨트롤러의 분배 역할을 「Request Dispatcher 라고도 한다」고 적은 것이 이 혼동의 출발점이다
- **매핑을 못 찾은 것과 뷰를 못 찾은 것은 다른 실패다** — 앞은 「그 URL 을 맡는 메서드가 없다」이고 뒤는 「메서드는 돌았는데 화면 파일이 없다」다. 둘 다 404 로 보일 수 있어 구별이 필요하다 → [[view-resolver]]
- **컨테이너를 받는다는 것은 그 컨테이너 밖의 빈은 안 보인다는 뜻이다** — 컨트롤러를 담은 컨테이너와 이 서블릿이 받은 컨테이너가 다르면, 분명히 등록한 컨트롤러가 매핑되지 않는다 → [[ioc-container]]
- **서블릿이므로 컨테이너가 관리하는 생명주기를 갖는다** — 스프링 것이라고 특별하지 않다. 서블릿 하나가 모든 요청을 쓰레드로 받는 그 구조 그대로다 → [[servlet-lifecycle]] · [[thread]]

## 함께 보는 개념

- [[front-controller]] — 이것이 구현하는 패턴
- [[spring-framework]] — 이것을 제공하는 것
- [[ioc-container]] — 컨트롤러를 어디서 찾는지의 근거
- [[request-mapping]] — 어느 메서드를 고를지의 근거
- [[view-resolver]] — 돌려받은 이름을 화면으로 바꾸는 쪽
- [[request-dispatcher]] — 이름이 겹치는 서블릿 API

## 출처

- [[2024-09-25-Day82]] — 「Front Controller 교체」 절이 직접 만든 `DispatcherServlet` 클래스를 지우고 스프링 것으로 바꾸며, **「클라이언트 요청이 들어오면 pageController에서 controller를 선택 후 requestHandler를 통해 실행할 메서드 선택」**이라는 한 줄로 이 서블릿의 두 단계(컨트롤러 고르기 → 메서드 고르기)를 적었다. `new DispatcherServlet(iocContainer)` 로 **컨테이너를 넘겨 세운다**는 것이 코드에 남아 있다. 클래스 이름이 앞 회차에서 손으로 만든 것과 같아서, 교체가 이름 그대로 일어난 자리다. 다만 매핑 실패와 뷰 해석 실패의 구별, 컨테이너가 둘일 때의 문제는 다루지 않았다
