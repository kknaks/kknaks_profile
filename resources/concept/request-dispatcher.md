---
type: concept
id: request-dispatcher
title: RequestDispatcher (include / forward)
aliases:
  - RequestDispatcher
  - getRequestDispatcher
  - include
  - forward
up:
  - 2024-08-29-Day66
  - 2024-08-30-Day67
tags:
  - web
  - servlet
  - 재사용
---

# RequestDispatcher (include / forward)

한 서블릿이 **다른 서블릿을 불러 같은 응답에 끼워 넣는** 장치. 요청과 응답 객체를 그대로 넘기므로, 불린 쪽이 만든 출력이 부르는 쪽의 출력에 이어 붙는다.

## 정의

경로로 상대를 지목하고 `include` 로 부른다.

```java
req.getRequestDispatcher("/header").include(req, res);
```

**넘기는 것이 `req`·`res` 그 자체**라는 것이 핵심이다. 불린 서블릿은 같은 [[request-parameter]] 를 읽고 같은 출력 스트림에 쓴다 — 새 요청이 아니다.

`include` 와 `forward` 가 갈린다.

| | 하는 일 | 부른 뒤 |
|---|---|---|
| `include` | 상대의 출력을 **끼워 넣는다** | 내 코드가 이어서 쓴다 |
| `forward` | 응답 만들기를 **넘긴다** | 내가 쓴 것은 버려진다 |
| `sendRedirect` | 브라우저에게 **다시 요청하라고 답한다** | 요청이 새로 시작된다 → [[redirect]] |

## 사용 예시

머리말을 서블릿 하나로 만들고, 화면마다 그것을 끼워 넣는다.

```java
@WebServlet("/user/form")
public class UserFormServlet extends GenericServlet {
  @Override
  public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException {
    res.setContentType("text/html;charset=UTF-8");
    PrintWriter out = res.getWriter();

    req.getRequestDispatcher("/header").include(req, res);   // ← 여기까지가 머리말

    out.println("<h1>회원 등록</h1>");
    out.println("<form action='/user/add'>");
    ...
    out.println("</body>");
    out.println("</html>");
  }
}
```

`HeaderServlet` 은 `<!DOCTYPE html>` 부터 `</header>` 까지만 쓰고 **`</body>`·`</html>` 는 쓰지 않는다.** 끼워 넣는 쪽이 그 뒤를 이어 닫는다 — **한 문서를 둘이 나눠 쓰는 형태**다.

## 왜 중요한가

**중복이 서블릿 단위로 접힌다.** Day63~65 의 화면들은 `<!DOCTYPE html>` 부터 `<nav>` 까지 열 몇 줄을 서블릿마다 복사했다. 그것이 한 곳으로 모이고, 메뉴를 고칠 때 고칠 자리가 하나가 된다 → [[cohesion]]

그리고 머리말이 **로그인 상태를 스스로 읽는다.** `HeaderServlet` 안에서 [[http-session]] 을 꺼내 로그인 버튼과 사용자 이름을 갈라 그리므로, 각 화면은 「누가 로그인했나」를 몰라도 된다 — 부르는 쪽이 아무것도 넘기지 않는데 상태가 반영되는 것은 **`req` 를 그대로 넘겼기 때문**이다.

### 하루 뒤 — `forward` 가 처음 쓰이고, JSP 쪽 표기가 하나 더 온다

Day66 은 `include` 만 썼다. Day67 이 **오류 화면으로 넘길 때** `forward` 를 쓴다.

```java
} catch (Exception e) {
  req.setAttribute("exception", e);
  req.getRequestDispatcher("/error.jsp").forward(req, res);
}
```

「넘긴다」가 맞는 자리다 — 오류 화면을 보일 때 앞서 쓴 것은 버려야 한다.

JSP 안에서는 액션 태그로 같은 일을 한다.

```jsp
<jsp:include page="/header.jsp"/>
```

**`req.getRequestDispatcher("/header").include(req, res)` 와 같은 장치다** — 문법만 다르다 → [[jsp]]

**다만 이 `forward` 는 자주 실패한다.** `try` 가 `include(...)` 까지 감싸고 있어서, JSP 가 그리는 중에 예외가 나면 **응답이 이미 나가기 시작한 뒤**다. 그 상태에서 `forward` 는 버릴 수 없어 `IllegalStateException` 이 되고, 사용자는 반쯤 그려진 화면과 그 뒤에 붙은 오류를 함께 본다 — **오류 화면이 정작 필요한 경우에 못 나온다** → [[exception-handling]]

## 경계와 오해

- **`include` ≠ 새 요청** — 브라우저는 이 일이 있었는지 모른다. 주소창도 바뀌지 않고 요청 횟수도 하나다. 「서블릿을 부른다」로 읽으면 두 번 왕복하는 것처럼 오해한다.
- **`include` 로 불린 쪽은 응답 헤더를 바꿀 수 없다** — 상태 코드·`setContentType`·`sendRedirect` 가 무시된다. 이미 본문이 나가기 시작했기 때문이다. 그래서 이 필기가 「`setHeader("Refresh", ...)` 이 필요한 부분은 추가한다」고 적은 것은 **끼워 넣는 쪽**의 일이다.
- **`setContentType` 은 `include` 앞에 두어야 한다** — 인코딩은 첫 출력 전에 정해져야 하는데, 머리말이 먼저 쓰기 시작하면 늦는다. 이 필기의 서블릿들이 `setContentType` → `getWriter()` → `include` 순서인 것이 그 때문이다 → [[character-encoding]]
- **`forward` 를 쓰면 앞서 쓴 것이 버려진다** — 버퍼가 이미 나갔으면 버릴 수 없어 예외가 된다. `include` 와 바꿔 쓸 수 있는 것이 아니다.
- **경로는 컨텍스트 안의 것이다** — `"/header"` 는 서블릿 매핑이고 파일 경로가 아니다. 같은 애플리케이션 밖은 부를 수 없다.
- **HTML 태그가 두 파일에 걸쳐 열리고 닫힌다** — `HeaderServlet` 이 `<body>` 를 열고 부르는 쪽이 닫으므로, **한쪽만 보면 문서가 깨져 보인다.** 끼워 넣는 것을 잊으면 `</body>` 만 있는 응답이 나가고 브라우저가 조용히 고쳐 그려서 알아차리기 어렵다.

## 함께 보는 개념

- [[redirect]] — 브라우저를 다시 보내는 쪽
- [[http-session]] — 머리말이 스스로 읽는 상태
- [[servlet]] · [[servlet-container]] — 부르는 주체와 불리는 대상
- [[request-parameter]] — 넘겨진 `req` 가 그대로 들고 있는 것
- [[static-and-dynamic-content]] — 정적 파일이던 것이 서블릿이 되는 자리
- [[cohesion]] — 중복을 한 곳으로 모으는 축

## 출처

- [[2024-08-30-Day67]] — 하루 뒤. `forward` 가 처음 쓰이고(오류 화면), JSP 쪽 표기 `<jsp:include page="..."/>` 가 같은 장치라는 것이 드러난다. 서블릿이 데이터를 `setAttribute` 로 담고 JSP 를 `include` 하는 형태가 회차 전체의 골격이 된다. 다만 `try` 가 `include` 까지 감싸고 있어 **JSP 렌더링 중에 난 예외는 `forward` 로 넘길 수 없다**(응답이 이미 나갔다)는 것은 다루지 않았다
- [[2024-08-29-Day66]] — 「HeaderServlet 만들기」 절이 「중복된 코드 head 를 servlet 클래스로 만든다」로 시작하고 `req.getRequestDispatcher("/header").include(req, res)` 로 부른다. 그 서블릿이 `<!DOCTYPE html>` 부터 `</header>` 까지만 쓰고 로그인 여부에 따라 버튼을 갈라 그리는 것까지가 한 벌이다. 이어지는 「동적으로 HTML관리하기」에서 `form.html`·`index.html` 이 서블릿이 되면서 그 둘도 같은 한 줄로 머리말을 끼운다. 다만 `include` 로 불린 쪽이 응답 헤더를 바꿀 수 없다는 것, `forward` 와의 차이, `setContentType` 이 `include` 앞이어야 하는 이유는 다루지 않았다
