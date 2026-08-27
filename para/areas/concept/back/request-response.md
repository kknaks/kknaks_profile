---
type: concept
id: request-response
title: 요청·응답 객체 (ServletRequest · ServletResponse)
aliases:
  - ServletRequest
  - ServletResponse
  - 요청 객체
  - 응답 객체
  - 요청·응답 객체
up:
  - 2024-08-27-Day64
  - 2024-08-28-Day65
  - 2024-09-06-Day71
tags:
  - web
  - java
  - JavaEE
  - 아키텍처
---

# 요청·응답 객체 (ServletRequest · ServletResponse)

**컨테이너가 요청 하나마다 만들어 `service()` 에 넘겨 주는 두 객체 — 소켓에서 바이트를 읽고 쓰던 일이 「객체에서 꺼내고 객체에 쓰는」 일로 바뀐 자리.** Day64 가 두 매개변수를 이렇게 적었다 — 「`ServletRequest req`: 클라이언트로부터 전달된 요청 데이터를 담고 있는 객체. 요청 파라미터, 헤더 정보 등을 추출할 수 있다」·「`ServletResponse res`: 서버에서 클라이언트로 보낼 응답 데이터를 담는 객체. 응답의 콘텐츠 타입, 출력 스트림 등을 설정할 수 있다」 → [[servlet-lifecycle]] · [[servlet-container]]

## 정의

**둘의 방향이 반대이고, 그래서 할 수 있는 일도 반대다.**

| | `ServletRequest` | `ServletResponse` |
|---|---|---|
| 방향 | 들어온 것 — **읽는다** | 나갈 것 — **쓴다** |
| Day64 가 든 예 | 요청 파라미터 · 헤더 정보 | 콘텐츠 타입 · 출력 스트림 |
| 수명 | 요청 하나 | 요청 하나 |
| 누가 만드나 | **컨테이너** — 내가 `new` 하지 않는다 | **컨테이너** |

**둘 다 인터페이스이고 내가 만들지 않는다는 것이 이 개념의 성격을 정한다** — 「받았으니 내 것」이 성립하지 않고(→ 아래 「경계와 오해」), 시험 코드에서 이 자리를 채우는 것이 따로 문제가 된다 → [[interface]]

### 요청 속성은 서버 안에서만 같은 요청을 따라간다

`ServletRequest`에는 클라이언트가 보낸 파라미터 말고, 서버 컴포넌트가 넣는 속성도 있다.

```java
request.setAttribute("key", value);
Object value = request.getAttribute("key");
```

이 값은 요청 하나에 속하고, `forward`·`include`가 같은 `request` 객체를 넘길 때만 함께 간다. Day71 의 설명처럼 다른 서블릿과 JSP가 꺼낼 수 있는 이유는 **새 요청을 만들지 않기 때문**이다 → [[request-dispatcher]].

### `ServletResponse` 는 두 단계로 쓴다

Day64 의 코드가 그 순서를 정확히 지킨다.

```java
res.setContentType("text/html;charset=UTF-8");   // ① 어떻게 보낼지 정한다
PrintWriter out = res.getWriter();                // ② 쓸 통로를 얻는다
out.println("<!DOCTYPE html>");                   // ③ 쓴다
```

**①과 ②의 순서가 뜻을 갖는다** — `getWriter()` 가 불린 순간 문자 인코딩이 확정되고, 그 뒤의 `setContentType` 은 조용히 무시된다. 필기는 그 이유를 적지 않았다 → [[character-encoding]]

그리고 필기가 골격을 이렇게 남겼다.

```java
ServletResponse.setContentType("MIME타입;문자집합")
```

**한 문자열이 두 가지를 정한다** — 무엇으로 해석할지(MIME 타입)와 어떤 글자 규칙인지(문자집합). Day64 가 실제로 넘긴 값은 `"text/html;charset=UTF-8"` 이다.

## 사용 예시

Day64 의 서블릿이 응답 객체 하나로 HTML 한 장을 만든다.

```java
res.setContentType("text/html;charset=UTF-8");
PrintWriter out = res.getWriter();
out.println("<!DOCTYPE html>");
out.println("<html>");
out.println("<head>");
out.println("    <meta charset='UTF-8'>");
out.println("    <title>Title</title>");
out.println("</head>");
out.println("<body>");

try {
  out.println("<h1>회원 목록</h1>");
  out.println("<table>");
  out.println("    <tr><th>번호</th><th>이름</th><th>이메일</th></tr>");

  for (User user : userDao.list()) {
    out.printf("    <tr><td>%d</td><td>%s</td><td>%s</td></tr>", user.getNo(), user.getName(),
        user.getEmail());
  }
  out.println("</table>");
} catch (Exception e) {
  out.println("목록 조회 중 오류 발생!");
}
out.println("</body>");
out.println("</html>");
```

**`req` 는 한 번도 쓰이지 않는다.** 목록 화면이라 입력이 없어서인데, 그 결과로 **이 회차에서 요청 객체는 시그니처에만 존재한다** — 파라미터를 꺼내는 코드도, 헤더를 읽는 코드도 없다.

**Day45~61 의 서버와 나란히 놓으면 사라진 것이 보인다.**

| Day61 의 소켓 서버 | Day64 의 서블릿 |
|---|---|
| `in.readUTF()` 로 한 줄씩 읽고 뜻을 내가 정한다 | 요청이 **이미 파싱된 객체**로 온다 |
| `out.writeUTF()` + 종료 신호(`GOODBYE`)를 내가 만든다 | `out.println` 만 하고 **끝은 컨테이너가 알린다** |
| 대화 규칙을 문서로 정해야 한다 | HTTP 가 이미 정해 놓았다 |

**내가 안 쓰게 된 것이 상태 줄·헤더·본문 경계·길이 표시·종료 신호 다섯이다.** [[network-protocol]] 노트가 Day61 에 대해 「사람이 정한 셋 중 둘이 맞고 하나가 틀렸다」고 적은 자리가 여기서는 아예 없어졌고, 대신 **HTTP 가 그것을 어떻게 표시하는지를 배워야 한다** → [[socket]] · [[length-prefix-framing]] · [[client-server-model]]

## 왜 중요한가

**대화의 규칙이 내 코드에서 규격으로 옮겨진다.** 소켓 층에서는 「무엇을 주고받을지」가 내 결정이었고 그래서 틀릴 수 있었다. 요청·응답 객체를 쓰면 그 결정이 **없어지는 것이 아니라 남의 것이 된다** — 편해진 만큼 내가 손댈 수 없는 것도 늘어난다 → [[network-protocol]]

**그리고 요청 하나가 두 객체의 수명이 된다.** 「이 값이 언제까지 유효한가」의 답이 「이 요청이 끝날 때까지」로 고정되므로, **어디에 무엇을 담을지가 수명으로 결정된다** — 요청 안에서만 쓸 것은 지역 변수나 요청 속성, 그보다 오래 살 것은 세션이나 앱 스코프다. 이 층이 갈리지 않으면 「필드에 담아 두면 편하다」로 남의 요청과 섞인다 → [[servlet-context]] · [[variable-scope]]

**출력이 스트림이라 되돌릴 수 없다.** 파일에 다 쓰고 나서 고치는 것과 달리, 응답은 쓰기 시작하면 앞부분이 이미 나가 있을 수 있다. 그래서 **정할 것을 먼저 정하고 쓰는 순서**가 규칙이 되고, 그 순서를 어기면 오류가 아니라 「설정이 안 먹는」 형태로 나타난다 → [[io-stream]]

## 경계와 오해

- **`ServletRequest` 에는 HTTP 가 없다 — 하루 뒤 그 어긋남이 코드로 드러난다** — `getMethod()`·`getHeader()`·`getSession()`·`getCookies()`·`getRequestURI()` 는 전부 **`HttpServletRequest`** 의 메서드다. 이 타입에 있는 것은 파라미터·속성·인코딩·입력 스트림처럼 **프로토콜과 무관한 것들**이다. 필기의 설명이 상위 타입에 하위 타입의 능력을 붙여 적은 셈이고, **Day64 의 서블릿은 `req` 를 아예 쓰지 않아 그 어긋남이 드러나지 않았다.** Day65 가 `getSession()` 을 부르려 하는 순간 드러난다 — 이 타입에 없으므로 **손으로 내려야 한다.**

```java
// HTTP 프로토콜 관련 기능을 사용하려면
// 파라미터로 받은 ServletRequest 객체를 원래 타입으로 형변환 해야 한다.
HttpServletRequest httpReq = (HttpServletRequest) req;
HttpSession session = httpReq.getSession();
```

**컨테이너가 넣어 주는 것은 처음부터 `HttpServletRequest` 다** — 선언 타입만 상위였을 뿐이라 이 다운캐스팅은 언제나 성공한다. 즉 이 줄은 **없던 능력을 얻는 것이 아니라 가려져 있던 것을 다시 보는 것**이고, `instanceof` 검사가 없어도 되는 이유가 그것이다 → [[type-casting]] · [[http-session]]

같은 회차가 응답 쪽에서도 같은 일을 한다 — `((HttpServletResponse) res).setHeader("Refresh", "1;url=/user/list")`. **다운캐스팅이 네 자리에 흩어져 있는 것이 다음 걸음(`HttpServlet`)의 동기**다 → [[generic-servlet]] · [[servlet]]
- **`getWriter()` 와 `getOutputStream()` 은 한 응답에서 둘 중 하나만** — 문자로 쓰는 통로와 바이트로 쓰는 통로를 같은 응답에 겹쳐 열면 `IllegalStateException` 이다. HTML 은 앞쪽, 이미지·파일 내려주기는 뒤쪽이다. 두 개를 다 쓰려 하는 코드는 대개 **한 서블릿이 두 가지 응답을 만들려는 것**이고 자리가 잘못 잡힌 신호다 → [[io-stream]] · [[character-stream]]
- **헤더는 본문보다 먼저 나간다 — 그래서 「먼저 정하고 쓴다」가 규칙이다** — `setContentType`·상태 코드·리다이렉트는 **첫 출력 전에** 해야 하고, 응답이 커밋된 뒤에는 무시된다. Day64 의 코드는 순서가 맞는데 **왜 그 순서인지가 적혀 있지 않아서**, 줄을 옮기면 깨진다는 것을 아무도 모른다. [[tomcat]] 노트의 「`setPort` 와 `getConnector` 의 순서가 뜻을 갖는다」와 **같은 종류의 함정이고 이번에는 요청마다 걸린다** → [[character-encoding]] · [[servlet-filter]]
- **요청 인코딩과 응답 인코딩은 다른 축이다 — 이 회차는 응답만 정했다** — `setContentType(...charset=UTF-8)` 은 **나가는 것**을 정하고, 브라우저가 보낸 파라미터를 한글로 읽으려면 `request.setCharacterEncoding("UTF-8")` 을 **파라미터를 처음 읽기 전에** 불러야 한다. 「인코딩을 UTF-8 로 설정했다」가 한쪽만 한 것이 되는 자리이고, 요청 쪽은 「읽기 전에」라는 시점 제약이 있어 **서블릿마다 첫 줄에 넣게 되는 것**이 곧 필터가 있는 이유다 → [[character-encoding]] · [[servlet-filter]]
- **요청 속성 ≠ 요청 파라미터 — 둘 다 `request`에 있고 이름이 문자열이라 섞인다** — 파라미터는 클라이언트가 보낸 문자열을 `getParameter`로 **읽는** 것이고, 속성은 서버가 객체를 `setAttribute`로 **넣어** 다음 컴포넌트에 건네는 것이다. `forward`에서 남는 것은 같은 요청 객체에 든 속성이지, 브라우저가 새로 보낸 값이 아니다 → [[request-parameter]] · [[request-dispatcher]]
- **요청·응답 객체를 필드에 보관하면 그 요청이 끝난 뒤에 무엇을 만지는지 보장되지 않는다** — 컨테이너는 이 객체를 **재사용하거나 되돌려 놓을 수 있다.** 서블릿 인스턴스는 하나이므로 필드에 담는 순간 다음 요청과 섞이고, 응답을 다 보낸 뒤에 붙들고 있으면 이미 남의 것이 되어 있을 수 있다. 「객체를 받았으니 내 것」이 성립하지 않는 자리다 → [[servlet-lifecycle]] · [[thread]] · [[object-reference]]
- **HTML 을 문자열로 만드는 것이 이 코드의 형태이고 그것이 다음 기술이 나오는 이유다** — `out.println("<html>")` 처럼 태그를 문자열로 적으므로 **컴파일러가 태그 짝을 검사하지 않고**, 화면 구조를 바꾸는 일이 자바 코드를 바꾸는 일이 된다. 게다가 `out.printf("<td>%s</td>", user.getName())` 은 **값을 그대로 태그 사이에 끼워 넣는다** — 이름에 `<` 가 들어 있으면 표가 깨지고, 그 자리에 스크립트를 넣을 수도 있다. [[sql-injection]] 이 「데이터를 문법으로 읽는 자리」에서 생겼던 것과 **같은 형태의 문제가 출력 쪽에서** 반복되고, 답도 같다 — 값과 문법을 섞지 않는다 → [[format-string]] · [[static-and-dynamic-content]]
- **`res.setContentType(...)` 의 인수가 문자열이라 오타가 컴파일에서 안 걸린다** — `"text/html;charset=UTF-8"` 에서 `charset` 을 `charest` 로 적어도 컴파일된다. [[character-encoding]] 노트의 「인코딩을 문자열로 넘기면 오타가 컴파일에서 안 걸린다」가 이 층에서 다시 나타나고, 여기서는 상수를 넘길 타입조차 없다 → [[literal]]
- **두 객체가 인터페이스인 것이 필터가 성립하는 이유다** — 컨테이너가 준 것을 **같은 타입의 래퍼로 감싸 넘길 수 있으므로** 요청·응답을 「고친 것처럼」 만들 수 있다. 「내가 만들지 않는다」가 제약이면서 동시에 이 확장 지점의 근거다 → [[servlet-filter]] · [[decorator-pattern]] · [[polymorphism]]

## 함께 보는 개념

- [[servlet-lifecycle]] — 이 두 객체가 인수로 오는 자리
- [[servlet]] · [[generic-servlet]] — HTTP 전용 타입으로 좁혀지기 전 단계
- [[servlet-container]] — 이 객체를 만들어 넘기는 쪽
- [[servlet-filter]] — 이 객체를 감싸서 바꾸는 자리
- [[character-encoding]] — `setContentType` 이 정하는 축
- [[io-stream]] · [[character-stream]] — 출력 통로의 성질
- [[socket]] · [[network-protocol]] · [[client-server-model]] — 이 객체가 대신하게 된 층
- [[length-prefix-framing]] — 손으로 만들던 경계 표시
- [[servlet-context]] — 요청보다 오래 사는 것을 담는 자리
- [[variable-scope]] — 수명으로 담을 곳을 정하는 축
- [[sql-injection]] · [[format-string]] — 값과 문법을 섞는 같은 형태의 문제
- [[static-and-dynamic-content]] — 코드로 HTML 을 만드는 것의 성질
- [[decorator-pattern]] · [[polymorphism]] — 래퍼로 감쌀 수 있는 근거
- [[object-reference]] — 「받은 객체가 내 것이 아니다」

## 출처

- [[2024-09-06-Day71]] — 열흘 뒤. 「Web 보관소」가 `ServletRequest`를 요청마다 새로 생성되는 저장소로 두고 `request.setAttribute("key", "value")`·`getAttribute("key")` 예와 `forward`·`include` 뒤에도 꺼낼 수 있다는 점을 적었다. 다만 세 `String value = ...` 줄을 한 코드 블록에 그대로 두면 같은 지역 변수 선언이 겹치고 각 줄 끝 세미콜론도 없어 컴파일되지 않는다. 세 저장소의 **사용법 비교**로 읽어야 하며, 실제로는 보관소별로 한 줄씩 따로 써야 한다
- [[2024-08-28-Day65]] — 하루 뒤. Day64 가 「`req` 가 코드에서 한 번도 쓰이지 않는다」로 남긴 자리가 채워지고, **그 순간 상위 타입의 한계가 드러난다.** 로그인 서블릿이 「HTTP 프로토콜 관련 기능을 사용하려면 파라미터로 받은 `ServletRequest` 객체를 원래 타입으로 형변환 해야 한다」는 주석과 함께 `(HttpServletRequest) req` 를 쓰고, 응답 쪽도 `((HttpServletResponse) res).setHeader("Refresh", ...)` 로 같은 캐스팅을 두 자리에서 한다. 필기의 「즉 req 레퍼런스는 실제 `HttpServletRequest` 객체를 가리키고 있다」가 그 캐스팅이 안전한 이유를 정확히 적은 문장이다. 다만 그 캐스팅이 반복된다는 것 자체가 `HttpServlet` 을 쓸 이유라는 연결은 이 회차에 없다
- [[2024-08-27-Day64]] — 「서블릿 구현체의 메서드」 절의 `service` 항목이 두 타입을 정의한다 — 「`ServletRequest req`: 클라이언트로부터 전달된 요청 데이터를 담고 있는 객체. 요청 파라미터, 헤더 정보 등을 추출할 수 있다」·「`ServletResponse res`: 서버에서 클라이언트로 보낼 응답 데이터를 담는 객체. 응답의 콘텐츠 타입, 출력 스트림 등을 설정할 수 있다」. 그리고 「문자열 출력시 글자 깨짐」 절이 `ServletResponse.setContentType("MIME타입;문자집합")` 골격을 남기고, `UserListServlet` 의 `service` 가 `setContentType("text/html;charset=UTF-8")` → `getWriter()` → `out.println`/`out.printf` 로 HTML 한 장을 만든다. 다만 **`req` 는 코드에서 한 번도 쓰이지 않고**, 「헤더 정보를 추출할 수 있다」는 실제로 `HttpServletRequest` 의 능력이라 이 타입에는 해당하지 않는다. `setContentType` 을 `getWriter()` 앞에 두어야 하는 이유, `getWriter()`/`getOutputStream()` 을 겹쳐 쓸 수 없다는 것, 요청 쪽 인코딩(`setCharacterEncoding`)은 따로 정해야 한다는 것, 이 객체를 필드에 보관하면 안 되는 이유, 값을 태그 사이에 그대로 끼워 넣는 것의 위험은 다루지 않았다
