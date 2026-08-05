---
type: concept
id: redirect
title: 리다이렉트 (sendRedirect)
aliases:
  - 리다이렉트
  - sendRedirect
  - redirect
up:
  - 2024-08-29-Day66
tags:
  - web
  - servlet
  - http
---

# 리다이렉트 (sendRedirect)

서버가 응답 대신 **「저 주소로 다시 요청해라」고 답하는** 것. 브라우저가 그 말을 듣고 새 요청을 보내므로, 요청이 **두 번** 일어난다.

## 정의

```java
((HttpServletResponse) res).sendRedirect("/");
```

[[request-dispatcher]] 와 갈리는 지점이 요청 횟수다.

| | 요청 횟수 | 주소창 | 앞서 쓴 출력 |
|---|---|---|---|
| `include` | 1 | 그대로 | 남는다 |
| `forward` | 1 | 그대로 | 버려진다 |
| **`sendRedirect`** | **2** | **바뀐다** | **버려진다** |

필기가 그 「버려진다」를 이렇게 적었다 — **「기존 버퍼에 있던 res 을 삭제하고 버퍼에 새롭게 담고 리턴한다」.** 정확히는 응답 본문 버퍼를 비우고 상태 코드 302 와 `Location` 헤더만 남긴다.

## 사용 예시

로그아웃은 세션을 버린 뒤 첫 화면으로 보낸다.

```java
@WebServlet("/auth/logout")
public class LogoutServlet extends GenericServlet {
  @Override
  public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException {
    ((HttpServletRequest) req).getSession().invalidate();   // 보관소를 버린다
    ((HttpServletResponse) res).sendRedirect("/");          // 첫 화면으로 다시 보낸다
  }
}
```

**이 서블릿은 HTML 을 한 줄도 쓰지 않는다.** `setContentType` 도 `getWriter()` 도 없다 — 보낼 본문이 없기 때문이다 → [[http-session]]

같은 회차의 다른 자리는 같은 일을 다르게 한다.

```java
((HttpServletResponse) res).setHeader("Refresh", "1;url=/project/list");
```

`Refresh` 는 **본문을 보여 준 뒤 1초 후에 옮기는** 것이라 「변경 했습니다」를 읽을 시간을 준다. 리다이렉트는 즉시 옮긴다 — **둘은 같은 목적의 다른 도구**이고, 이 필기는 상황에 따라 갈라 썼다.

## 왜 중요한가

**주소창이 결과 화면의 주소가 된다.** 등록·변경을 처리한 URL 에 그대로 머무르면 새로고침이 그 처리를 다시 실행한다. 처리 뒤 목록으로 리다이렉트하면 새로고침이 목록 조회가 되므로 그 문제가 사라진다 → [[http-method]]

그리고 **응답을 버릴 수 있다는 것**이 실질적이다. 로그아웃처럼 「할 일은 했고 보여 줄 것은 다른 화면」인 경우, 화면을 만들지 않고 넘길 수 있다.

## 경계와 오해

- **리다이렉트는 서버가 옮기는 것이 아니라 브라우저에게 부탁하는 것이다** — 브라우저가 따르지 않으면 아무 일도 안 난다. 그래서 `sendRedirect` 뒤의 코드는 **계속 실행된다** — 메서드가 끝나는 것이 아니므로 `return` 을 따로 써야 한다.
- **본문을 이미 보냈으면 실패한다** — 버퍼가 나간 뒤에는 되돌릴 수 없어 `IllegalStateException` 이다. 그래서 `include` 로 머리말을 끼운 다음에는 리다이렉트할 수 없고, 이 필기의 `LogoutServlet` 이 머리말을 끼우지 않는 것이 그 때문이다 → [[request-dispatcher]]
- **`Refresh` 헤더는 표준 HTTP 가 아니다** — 브라우저가 관행으로 지원하는 것이고, 「1초 뒤 이동」이라 사용자가 그 사이 다른 곳을 누르면 갈리는 결과가 된다. 같은 회차가 둘을 섞어 쓰는데 **어느 쪽을 언제 쓰는지 기준은 적혀 있지 않다.**
- **리다이렉트하면 요청 속성이 사라진다** — 새 요청이므로 `setAttribute` 로 담은 것은 넘어가지 않는다. 넘기려면 [[http-session]] 이나 쿼리 스트링을 써야 한다. `forward` 와 갈리는 실질적 차이가 이것이다.
- **`invalidate()` 뒤에 세션을 다시 쓰면 예외다** — 버린 뒤에 `setAttribute` 를 부르면 `IllegalStateException` 이다. 이 필기는 버린 직후 리다이렉트만 하므로 걸리지 않는다.
- **`sendRedirect("/")` 의 `/` 는 서버 루트다** — 컨텍스트 경로가 붙는 배치에서는 애플리케이션 밖을 가리키게 된다 → [[web-application-deployment]]

## 함께 보는 개념

- [[request-dispatcher]] — 같은 요청 안에서 합치는 쪽
- [[http-session]] — 로그아웃이 버리는 것, 그리고 리다이렉트를 넘어 값을 나르는 곳
- [[http-method]] — 처리 뒤 리다이렉트가 필요한 이유
- [[url]] — `Location` 에 담기는 것
- [[request-response]] — 형변환을 해야 부를 수 있는 자리

## 출처

- [[2024-08-29-Day66]] — 「LoginOutServlet만들기」 절이 「Session 을 초기화 한다」·「sendRedirect 을 통해 기존 버퍼에 있던 res 을 삭제하고 버퍼에 새롭게 담고 리턴한다」로 두 줄을 적고, `getSession().invalidate()` + `sendRedirect("/")` 두 문장뿐인 서블릿을 보인다. 같은 회차의 변경·삭제 처리는 `setHeader("Refresh", "1;url=...")` 를 쓰는데, 두 방법을 언제 갈라 쓰는지는 적혀 있지 않다. `sendRedirect` 뒤 코드가 계속 실행된다는 것, 본문을 보낸 뒤에는 못 쓴다는 것, 요청 속성이 넘어가지 않는다는 것도 다루지 않았다
