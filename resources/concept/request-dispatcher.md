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
  - 2024-09-05-Day70
  - 2024-09-10-Day73
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

Day70 은 같은 세 칸을 「기존 `res` 결과를 남겨 두는 `include` / 최종 대상으로 넘기는
`forward`」로 다시 갈랐다. 정확히는 `forward`가 **아직 전송되지 않은 호출자 쪽 버퍼**를
비우고 대상에게 응답 생성을 맡기는 것이며, `req`·`res` 객체 자체는 여전히 같은 것이다.
`include`는 대상의 **본문 출력**을 그 버퍼에 덧붙인다.

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
- **`forward` ≠ `res` 객체를 새것으로 바꾸는 일** — Day70 은 `req,res`를 전달한다고 적어 두고도 「기존과 앞으로 담길 값을 무시한다」고 썼다. 실제로 같은 객체를 넘기되, 아직 커밋되지 않은 호출자 버퍼만 비우고 대상의 출력을 최종 응답으로 삼는다. 호출자가 `forward` 뒤에 계속 응답을 쓰면 소유권이 흐려지므로 바로 `return`해 흐름을 끝내는 것이 안전하다.
- **`getRequestDispacher`는 호출할 수 없다** — 원문의 철자가 `Dispatcher`의 `t`를 빠뜨렸다. 그 코드 그대로면 메서드를 찾지 못해 컴파일이 멈추고, `include`·`forward`의 차이를 실행으로 확인할 수 없다.
- **「include」라는 이름이 셋이고 시점이 다르다** — Day73 이 「RequestDispatcher의 include()와 다르다」고만 적고 넘어간 자리다.

  | | 시점 | 무엇을 합치나 | 대상 |
  |---|---|---|---|
  | `<%@ include %>` | **번역** | 소스를 붙여 넣어 **한 개** 클래스가 된다 | 텍스트 파일이면 된다 → [[jsp-directive]] |
  | `<jsp:include>` | 실행 | 대상을 실행한 **결과**를 끼운다 | 서블릿/JSP → [[jsp-action-tag]] |
  | `RequestDispatcher.include()` | 실행 | 같은 일을 자바 코드로 | 서블릿/JSP |

  아래 둘은 같은 장치이고, 맨 위만 **다른 종류**다. 번역 시점에 붙여 넣으므로 포함되는 쪽의 변수가 포함하는 쪽과 같은 메서드에 살고, 이름이 겹치면 컴파일 오류가 난다 — 실행 시점 포함에서는 없는 일이다.

## 함께 보는 개념

- [[redirect]] — 브라우저를 다시 보내는 쪽
- [[http-session]] — 머리말이 스스로 읽는 상태
- [[servlet]] · [[servlet-container]] — 부르는 주체와 불리는 대상
- [[request-parameter]] — 넘겨진 `req` 가 그대로 들고 있는 것
- [[static-and-dynamic-content]] — 정적 파일이던 것이 서블릿이 되는 자리
- [[cohesion]] — 중복을 한 곳으로 모으는 축
- [[jsp-action-tag]] — JSP 문법으로 같은 일을 하는 표기
- [[jsp-directive]] — 이름만 같고 시점이 다른 `<%@ include %>`

## 출처

- [[2024-09-10-Day73]] — 「Include(Directive element)」 절이 `<%@ include %>` 를 「지정한 파일을 JSP로 **포함시킨 후에** 자바 서블릿 클래스를 생성한다」로 적어 **번역 시점 포함**임을 짚고, 「일반 텍스트 파일이면 된다. JSP 파일일 필요가 없다」로 그 결과까지 보인다. 그리고 「RequestDispatcher의 include()와 다르다」고 명시했다 — **다르다는 것만 적고 무엇이 다른지는 적지 않은 자리**라 위 표가 그것을 채운다. 같은 노트의 액션 태그 절이 `jsp:include`(제어권이 되돌아온다)와 `jsp:forward`(되돌아오지 않는다)를 가르는데, 이는 Day67 에서 자바 API 로 본 구별과 같은 것이다
- [[2024-09-05-Day70]] — 「include와 forward」 절이 `getRequestDispatcher(...)`로 위임 객체를 얻어 `forward(req, res)`·`include(req, res)`를 고르는 두 예시를 적었다. `forward`는 앞서 쓴 미커밋 버퍼를 버리고 최종 대상의 결과를 쓰며, `include`는 여러 서블릿의 본문을 합친다는 구별을 보인다. 다만 원문 코드의 `getRequestDispacher`는 오타라 컴파일되지 않고, 「앞으로 담기는 값도 무시한다」는 설명은 같은 `res` 객체와 대상의 출력을 혼동한다
- [[2024-08-30-Day67]] — 하루 뒤. `forward` 가 처음 쓰이고(오류 화면), JSP 쪽 표기 `<jsp:include page="..."/>` 가 같은 장치라는 것이 드러난다. 서블릿이 데이터를 `setAttribute` 로 담고 JSP 를 `include` 하는 형태가 회차 전체의 골격이 된다. 다만 `try` 가 `include` 까지 감싸고 있어 **JSP 렌더링 중에 난 예외는 `forward` 로 넘길 수 없다**(응답이 이미 나갔다)는 것은 다루지 않았다
- [[2024-08-29-Day66]] — 「HeaderServlet 만들기」 절이 「중복된 코드 head 를 servlet 클래스로 만든다」로 시작하고 `req.getRequestDispatcher("/header").include(req, res)` 로 부른다. 그 서블릿이 `<!DOCTYPE html>` 부터 `</header>` 까지만 쓰고 로그인 여부에 따라 버튼을 갈라 그리는 것까지가 한 벌이다. 이어지는 「동적으로 HTML관리하기」에서 `form.html`·`index.html` 이 서블릿이 되면서 그 둘도 같은 한 줄로 머리말을 끼운다. 다만 `include` 로 불린 쪽이 응답 헤더를 바꿀 수 없다는 것, `forward` 와의 차이, `setContentType` 이 `include` 앞이어야 하는 이유는 다루지 않았다
