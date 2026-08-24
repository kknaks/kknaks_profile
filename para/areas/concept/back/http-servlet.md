---
type: concept
id: http-servlet
title: HttpServlet (doGet / doPost)
aliases:
  - HttpServlet
  - doGet
  - doPost
up:
  - 2024-09-02-Day68
  - 2024-09-05-Day70
tags:
  - web
  - servlet
  - http
---

# HttpServlet (doGet / doPost)

[[generic-servlet]] 을 상속해 **HTTP 를 다루는 부분까지 채워 둔** 추상 클래스. 상속하면 `service` 대신 `doGet`·`doPost` 를 재정의한다.

## 정의

상속 사슬이 세 칸이다.

| | 무엇을 남기나 | 내가 구현할 것 |
|---|---|---|
| `Servlet` 인터페이스 | 아무것도 안 준다 | 다섯 개 전부 |
| `GenericServlet` | `service(ServletRequest, ServletResponse)` 를 추상으로 | `service` 하나 |
| **`HttpServlet`** | **`doGet`·`doPost` 등을 빈 구현으로** | **필요한 `doXxx` 만** |

이 클래스가 채워 넣은 것이 **캐스팅**이다. 필기가 그 코드를 그대로 인용했다.

```java
public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException {
    HttpServletRequest request;
    HttpServletResponse response;
    try {
        request = (HttpServletRequest) req;
        response = (HttpServletResponse) res;
    } catch (ClassCastException e) {
        throw new ServletException(lStrings.getString("http.non_http"));
    }
    service(request, response);      // ← HTTP 타입을 받는 쪽으로 넘긴다
}
```

**Day65~67 이 서블릿마다 손으로 쓴 `(HttpServletRequest) req` 가 이 한 곳으로 모였다.**
그 뒤 `service(HttpServletRequest, HttpServletResponse)` 가 요청 방식을 보고 `doGet`·`doPost` 중 하나를 부른다.

그래서 재정의할 것이 바뀐다.

- `Servlet` 인터페이스의 `service(ServletRequest, ServletResponse)` 를 재정의하는 것이 **아니고**
- `HttpServlet` 이 더한 `service(HttpServletRequest, HttpServletResponse)` 를 재정의하거나
- 그보다 **`doGet`·`doPost` 를 재정의한다**

### 사흘 뒤 — 분기 코드의 주체를 다시 적는다

Day70 은 `request.getMethod()`의 `GET`·`POST`·`PUT`·`HEAD`를 `switch`로 갈라 각각의
`doXxx`를 부르는 모양을 적었다. 이것이 바로 `HttpServlet`의 HTTP 전용 `service`가 하는
일이다. 컨테이너가 `HttpServlet` 객체를 매개변수로 넘기는 것이 아니다. 컨테이너는
`service(ServletRequest, ServletResponse)`를 호출하고, 그 메서드가 두 객체를 HTTP 타입으로
내린 뒤 **수신자(`this`)의** `service(HttpServletRequest, HttpServletResponse)`로 넘긴다.
그래서 하위 서블릿이 `doGet`을 재정의하면 그 구현이 선택된다.

## 왜 중요한가

**요청 방식을 구별할 자리가 문법으로 생긴다.** Day63~67 은 `GenericServlet` 만 써서 GET·POST 가 같은 `service()` 로 들어왔다 — 그래서 [[http-method]] 표를 배워 두고도 **조회와 변경을 코드에서 가를 수 없었고**, 변경 폼이 GET 으로 제출되는 것이 눈에 걸릴 계기가 없었다. `doGet`·`doPost` 로 갈리면 **어느 쪽에 무엇을 쓸지 정해야** 하고, 그 순간 안전·멱등 이야기가 코드에 닿는다.

그리고 **캐스팅이 사라진다.** 매개변수가 처음부터 `HttpServletRequest` 라 `getSession()`·`getHeader()` 를 바로 부를 수 있다 → [[request-response]] · [[http-session]]

## 경계와 오해

- **「HTTP 프로토콜을 다루려면 `GenericServlet` 을 상속 받지 말고」가 「`GenericServlet` 은 HTTP 가 아닐 때 쓴다」는 뜻이 아니다** — `HttpServlet` 이 **`GenericServlet` 을 상속한다.** 즉 HTTP 를 쓸 때도 그 클래스를 쓰고 있는 것이고, 갈리는 것은 「어느 층에서 시작하나」다. Day64 노트가 이미 짚어 둔 오해가 이 회차에서 상속 사슬로 확인된다 → [[generic-servlet]] · [[inheritance]]
- **`doGet` 을 재정의하지 않으면 405 가 온다** — 「빈 구현」이 아무 일도 안 하는 것이 아니라 **「지원하지 않는다」고 답한다.** 그래서 GET 으로 들어온 요청에 `doPost` 만 구현해 두면 화면이 안 나오고 오류 코드가 나온다 — 아무 반응이 없는 것보다 낫지만, 「빈 메서드」로 알면 그 405 의 출처를 못 찾는다 → [[method-overriding]]
- **`service(HttpServletRequest, HttpServletResponse)` 를 재정의하면 `doGet`·`doPost` 가 안 불린다** — 그 분기를 하는 것이 바로 그 메서드이므로, 재정의하면서 `super.service(...)` 를 부르지 않으면 사슬이 끊긴다. **둘 중 하나만 골라야 하고** 필기는 둘을 나란히 놓고 어느 쪽을 권하는지 적지 않았다.
- **`doGet`·`doPost` 로 갈라도 폼이 GET 을 보내면 `doGet` 이 불린다** — 문법이 생겼다고 안전이 생기는 것은 아니다. Day66 의 「GET 으로 변경」은 이 클래스를 써도 그대로이고, 고쳐야 할 것은 폼의 `method` 다 → [[html-form]]
- **여덟 개 중 둘만 흔하다** — `doPut`·`doDelete`·`doHead`·`doOptions`·`doTrace` 도 있지만 HTML 폼이 GET·POST 만 보내므로 나머지는 폼으로 닿지 않는다 → [[http-method]]
- **인스턴스가 하나인 것은 그대로다** — 상속 층이 바뀌어도 컨테이너가 클래스마다 인스턴스 하나를 만들어 공유한다. 필기가 같은 회차에서 「클라이언트마다 구분되어야 할 데이터는 서블릿 인스턴스 변수에 보관해서는 안된다」로 그것을 못 박았다 → [[servlet-lifecycle]] · [[thread]]
- **Day70 의 분기 코드는 그대로 컴파일되지 않는다** — `request.getMethod();ßœ`의 뒤 두 글자는 Java 토큰이 아니고, `switch`의 닫는 `}`도 출력되지 않았다. 따라서 컴파일러는 먼저 불법 문자를, 그것을 지워도 파일 끝의 미완성 블록을 보고 멈춘다. 또 `Class HttpServlet extends GenericServlet`·매개변수 선언이 없는 `@Override service(req,res)`는 Java 선언이 아니라 설명용 의사 코드다. 이 조각을 복사해 실행하면 `doGet` 분기 자체를 시험하기도 전에 빌드가 깨진다.
- **`this` ≠ 「Servlet 클래스의 주소」** — `this`는 지금 실행 중인 **객체**다. `HttpServlet`을 상속한 내 서블릿 인스턴스에서 실행 중이면 그 객체를 가리키므로, 오버라이드한 HTTP 전용 `service`가 있으면 동적 디스패치로 그쪽이 선택된다. 클래스를 가리킨다고 읽으면 왜 `doGet` 재정의가 불리는지 설명할 수 없다.

## 함께 보는 개념

- [[generic-servlet]] — 이 클래스의 부모
- [[servlet]] · [[servlet-lifecycle]] — 규격과 생명주기
- [[http-method]] — `doGet`·`doPost` 가 코드로 만드는 구별
- [[request-response]] — 캐스팅이 사라지는 자리
- [[http-session]] — 매개변수 타입 덕에 바로 부를 수 있게 되는 것
- [[inheritance]] · [[method-overriding]] — 세 칸 사슬과 재정의 규칙

## 출처

- [[2024-09-05-Day70]] — 사흘 뒤. 「HttpServlet」 절이 `getMethod()`를 `switch`로 갈라 `doGet`·`doPost`·`doPut`·`doHead`를 부르는 모양과, `HttpServlet extends GenericServlet`에서 일반 요청·응답을 HTTP 타입으로 내려 HTTP 전용 `service`에 넘기는 모양을 적었다. 다만 **「컨테이너가 HttpServlet을 파라미터로 전달한다」는 말은 요청·응답 객체와 서블릿 인스턴스를 섞은 것**이고, 두 코드 조각은 불법 문자·누락된 닫는 중괄호·의사 코드 문법 때문에 그대로는 컴파일되지 않는다
- [[2024-09-02-Day68]] — 「Servlet 만들기」 절이 세 방법을 나란히 놓는다 — 인터페이스 직접 구현, `GenericServlet` 상속, **`HttpServlet` 상속**. 「`javax.servlet.GenericServlet` 추상 클래스를 상속 받았다」로 사슬을 밝히고, `HttpServlet.service` 의 실제 코드를 인용해 **캐스팅과 `ClassCastException` → `ServletException` 변환이 그 안에 있다**는 것을 보인다. 「HTTP 프로토콜을 다루려면 `GenericServlet` 을 상속 받지 말고 `HttpServlet` 을 상속 받아 서블릿 클래스를 만드는 것이 유지보수에 용이하다」가 이 회차의 결론이고, 이어서 `doGet`·`doPost` 를 GET·POST 의 목적·전송 방식·특징(캐싱·크기 제한·멱등성)으로 갈라 정리했다. 다만 `doGet` 을 재정의하지 않으면 405 가 온다는 것, `service(HttpServletRequest, ...)` 를 재정의하면 `doXxx` 분기가 끊긴다는 것, 그리고 **실습 코드는 이 회차에도 `GenericServlet` 을 쓴다**는 것은 다루지 않았다
