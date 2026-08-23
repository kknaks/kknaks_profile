---
type: concept
id: exception-handler
title: 웹 예외 처리 (@ExceptionHandler · @ControllerAdvice)
aliases:
  - "@ExceptionHandler"
  - "@ControllerAdvice"
  - error-page
  - 웹 예외 처리
up:
  - 2024-10-17-Day95
tags:
  - spring
  - web
  - 예외
---

# 웹 예외 처리 (@ExceptionHandler · @ControllerAdvice)

**요청을 처리하다 예외가 났을 때 무엇을 보여 줄지 정하는 장치.** 가까운 곳부터 차례로 찾아 처리하고, 아무도 안 받으면 컨테이너의 기본 오류 화면이 나온다.

## 정의

**찾는 순서가 넷이다.**

| 순서 | 어디 | 범위 |
|---|---|---|
| 1 | 페이지 컨트롤러의 `@ExceptionHandler` | **그 컨트롤러 안**에서 난 예외 |
| 2 | `@ControllerAdvice` 클래스의 `@ExceptionHandler` | 모든 컨트롤러 |
| 3 | `web.xml` 의 `<error-page>` | 애플리케이션 전체 |
| 4 | 서블릿 컨테이너 | 기본 오류 화면 |

**가까운 쪽이 이긴다** — 컨트롤러 안에 있으면 어드바이스까지 안 간다.

### 컨트롤러 안에서

```java
@ExceptionHandler
public ModelAndView exceptionHandler(Exception ex) {
  ModelAndView mv = new ModelAndView();
  mv.addObject("error", ex);
  mv.setViewName("error6");
  return mv;
}
```

### 전역으로

```java
@ControllerAdvice
public class GlobalControllerAdvice {
  @ExceptionHandler public ModelAndView handle(Exception ex)    { ... }   // 나머지 전부
  @ExceptionHandler public ModelAndView io(IOException ex)      { ... }
  @ExceptionHandler public ModelAndView sql(SQLException ex)    { ... }
}
```

**매개변수 타입이 곧 조건이다** — 던져진 예외를 받을 수 있는 메서드 중 **가장 구체적인 것**이 불린다 → [[exception-handling]] · [[polymorphism]]

### 설정 파일에서

```xml
<error-page>
  <location>/WEB-INF/jsp2/error1.jsp</location>   <!-- JSP 를 직접 실행 -->
</error-page>

<error-page>
  <location>/app2/error</location>                <!-- 컨트롤러를 경유 -->
</error-page>
```

## 왜 중요한가

**오류 화면을 만드는 코드가 정상 흐름에서 빠진다.** 컨트롤러마다 `try-catch` 로 감싸 오류 페이지로 보내던 것을 **표식 하나**로 옮기면, 핸들러 메서드는 성공 경로만 적으면 된다 → [[exception-handling]]

**그리고 예외 종류마다 다른 화면을 줄 수 있다.** `SQLException` 은 「일시적인 문제」, `IllegalArgumentException` 은 「입력을 확인하세요」처럼 갈리는데, **타입으로 고르므로 조건문이 없다** → [[polymorphism]]

**계층이 넷이라는 것도 설계다.** 특별한 처리가 필요한 컨트롤러는 자기 것을 두고, 나머지는 전역이 받고, 스프링이 아예 못 잡은 것(예: 404)은 컨테이너 설정이 받는다 → [[web-xml]]

## 경계와 오해

- **`@ControllerAdvice` 는 `DispatcherServlet` 안에서만 동작한다** — 필터에서 난 예외나 스프링에 닿기 전의 오류는 못 받는다. 그 자리를 `<error-page>` 가 맡는 이유다 → [[servlet-filter]] · [[servlet-container]]
- **예외를 잡으면 트랜잭션은 이미 롤백 표시가 돼 있을 수 있다** — 여기서 화면을 예쁘게 만든다고 그 작업이 되살아나지 않는다 → [[declarative-transaction]]
- **응답이 이미 나가기 시작했으면 오류 화면으로 못 바꾼다** — JSP 를 그리는 중에 난 예외가 그렇다. Day67 에서 `forward` 가 `IllegalStateException` 이 되던 것과 같은 자리다 → [[request-dispatcher]]
- **`@ExceptionHandler` 를 `Exception` 하나로만 두면 정보가 뭉개진다** — 전부 같은 화면으로 가므로 사용자도 개발자도 원인을 모른다. **최소한 로그는 종류별로 남겨야 한다**
- **`<error-page>` 에 컨트롤러 경로를 주면 다시 스프링을 탄다** — 필기의 두 번째 예(`/app2/error`)가 그 방식이다. 화면에 데이터를 채워야 할 때 쓰지만, **그 컨트롤러에서 또 예외가 나면 무한히 도는 위험**이 있다
- **`@ControllerAdvice` 는 예외만의 것이 아니다** — 같은 클래스에 `@InitBinder`·`@ModelAttribute` 를 두어 전역 바인딩·전역 모델도 넣는다 → [[property-editor]] · [[handler-method-argument]]

## 함께 보는 개념

- [[exception-handling]] — 자바 쪽의 같은 문제
- [[handler-interceptor]] — 겹치는 다른 공통 장치
- [[dispatcher-servlet]] — 이 처리를 수행하는 주체
- [[web-xml]] — 세 번째 계층이 설정되는 곳
- [[spring-model]] — 오류 화면에 값을 넘기는 방법
- [[declarative-transaction]] — 예외가 함께 건드리는 것

## 출처

- [[2024-10-17-Day95]] — 「예외 처리하기」 절이 **우선순위를 네 줄로 먼저 세운 것**(페이지 컨트롤러 → `@ControllerAdvice` → `web.xml` → 서블릿 컨테이너)이 이 개념의 뼈대다. 컨트롤러 안의 `@ExceptionHandler` 가 `ModelAndView` 를 돌려주는 예, `@ControllerAdvice` 클래스에 **`Exception`·`IOException`·`SQLException` 세 핸들러를 두고 타입으로 갈리게 한 예**, 그리고 `web.xml` 의 `<error-page>` 를 **JSP 직접 실행**과 **컨트롤러 경유** 두 방식으로 적은 예가 차례로 나온다. 주석의 「`DispatcherServlet` 은 request handler 가 던지는 예외에 따라 그 예외를 받을 수 있는 메서드를 찾아 호출한다」가 동작을 정확히 설명한다. 다만 같은 노트의 「세션다루기」·「JSON 데이터 출력」 절은 **제목만 있고 비어 있다**
