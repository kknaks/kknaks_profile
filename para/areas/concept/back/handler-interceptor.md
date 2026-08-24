---
type: concept
id: handler-interceptor
title: 인터셉터 (HandlerInterceptor)
aliases:
  - 인터셉터
  - HandlerInterceptor
  - preHandle
  - postHandle
  - afterCompletion
  - WebMvcConfigurer
up:
  - 2024-10-17-Day95
tags:
  - spring
  - web
  - mvc
---

# 인터셉터 (HandlerInterceptor)

**프론트 컨트롤러와 페이지 컨트롤러 사이에 코드를 끼워 넣는 장치.** 요청 처리의 앞·뒤·끝 세 지점에 걸 수 있다.

## 정의

메서드 셋이 각각 다른 시점이다.

| 메서드 | 언제 |
|---|---|
| `preHandle` | 핸들러를 **부르기 전**. `false` 를 돌려주면 **거기서 끝난다** |
| `postHandle` | 핸들러가 리턴한 **직후** (뷰 실행 전). `ModelAndView` 를 받아 손댈 수 있다 |
| `afterCompletion` | **JSP 까지 실행한 뒤.** 예외 객체를 받는다 |

```java
public class Interceptor1 implements HandlerInterceptor {
  @Override
  public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
    return true;   // false 면 다음 인터셉터도 핸들러도 실행하지 않는다
  }

  @Override
  public void postHandle(HttpServletRequest req, HttpServletResponse res,
                         Object handler, ModelAndView mv) { }

  @Override
  public void afterCompletion(HttpServletRequest req, HttpServletResponse res,
                              Object handler, Exception ex) { }
}
```

### 어디에 걸 것인가

```java
@ComponentScan("bitcamp.app2")
public class App2Config implements WebMvcConfigurer {
  @Override
  public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(new Interceptor1());                       // 모든 요청

    registry.addInterceptor(new Interceptor2())
            .addPathPatterns("/c04_1/*");                              // 바로 아래만

    registry.addInterceptor(new Interceptor3())
            .addPathPatterns("/c04_1/**");                             // 모든 하위 경로

    registry.addInterceptor(new Interceptor4())
            .addPathPatterns("/c04_1/**")
            .excludePathPatterns("/c04_1/a/**");                       // 빼면서 걸기
  }
}
```

**`*` 는 한 단계, `**` 는 모든 깊이**다 → [[sql-like]] 의 와일드카드와 같은 종류의 구별이다.

## 왜 중요한가

**모든 요청에 공통인 일을 컨트롤러 밖에 둘 수 있다.** 로그인 확인·권한 검사·로깅·실행 시간 측정이 컨트롤러마다 반복되던 것을 한 곳으로 모은다 — [[front-controller]] 가 얻으려던 것을 **경로 단위로 골라서** 얻는 형태다.

**`preHandle` 이 `false` 를 돌려줄 수 있다는 것이 핵심**이다. 로그인 안 한 요청을 여기서 끊고 로그인 화면으로 보내면, 컨트롤러는 **로그인 여부를 아예 모르는 채로** 쓸 수 있다 → [[http-session]] · [[redirect]]

## 경계와 오해

- **인터셉터 ≠ [[servlet-filter]]** — 필터는 **서블릿 컨테이너**의 것이라 `DispatcherServlet` 보다 바깥이고, 인터셉터는 **스프링**의 것이라 그 안쪽이다. 그래서 인터셉터는 어느 핸들러가 불릴지(`Object handler`)를 알고 스프링 빈을 주입받을 수 있지만, 필터는 요청이 스프링에 닿기도 전에 걸린다. **인코딩 설정처럼 컨테이너 수준의 일은 필터**가 맞다
- **`postHandle` 은 예외가 나면 안 불린다** — 정리 작업을 여기 두면 실패 경로에서 빠진다. **반드시 실행돼야 하는 것은 `afterCompletion`** 이다 → [[exception-handling]] · [[try-with-resources]]
- **`preHandle` 이 `false` 를 돌려줄 때는 응답을 직접 만들어야 한다** — 「막았다」는 신호일 뿐 아무것도 안 보내면 빈 응답이 나간다. 리다이렉트나 오류 응답을 여기서 써야 한다
- **등록 순서가 실행 순서다** — `preHandle` 은 등록 순서대로, `postHandle`·`afterCompletion` 은 **역순**으로 불린다. 감싸는 구조라서 그렇다
- **`WebMvcConfigurer` 는 설정 클래스가 구현한다** — 인터셉터가 스프링 빈이 아니어도 `new` 로 등록할 수 있지만, 빈을 주입받아야 한다면 빈으로 만들어 넣어야 한다 → [[java-config]] · [[ioc-container]]
- **`@ControllerAdvice` 와 겹치는 자리가 있다** — 둘 다 「여러 컨트롤러에 공통」인데, 인터셉터는 **요청 흐름의 앞뒤**를 잡고 어드바이스는 **예외·바인딩·모델**을 잡는다 → [[exception-handler]]

## 함께 보는 개념

- [[dispatcher-servlet]] — 인터셉터를 부르는 주체
- [[servlet-filter]] — 한 겹 바깥의 같은 성격 장치
- [[front-controller]] — 공통 처리를 한 곳에 두려는 배치
- [[exception-handler]] — 겹치는 다른 공통 장치
- [[java-config]] — 인터셉터를 등록하는 자리
- [[http-session]] — 인터셉터가 흔히 검사하는 것

## 출처

- [[2024-10-17-Day95]] — 「인터셉터」 절이 **「프론트 컨트롤러와 페이지 컨트롤러 사이에 코드를 삽입하는 기술」**이라는 한 줄 정의로 시작해 위치를 정확히 짚었다. `addInterceptors` 안에 **네 가지 등록 방식**(전체 · `/c04_1/*` · `/c04_1/**` · `**` 에서 특정 경로 제외)을 주석과 함께 나란히 놓아 `*` 와 `**` 의 차이를 보였다. 구현 쪽은 `preHandle`·`postHandle`·`afterCompletion` 세 메서드에 각각 **언제 불리는지**를 주석으로 달았고, **「다음 인터셉터나 페이지 컨트롤러를 계속 실행하고 싶다면 `true`, 여기서 요청 처리를 완료하고 싶다면 `false`」**로 반환값의 의미까지 적었다. 다만 필터와의 차이, `postHandle` 이 예외 시 건너뛰어진다는 것, 등록 순서와 실행 순서의 관계는 다루지 않았다
