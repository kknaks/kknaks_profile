---
type: concept
id: http-session
title: HttpSession (클라이언트 전용 보관소)
aliases:
  - HttpSession
  - 서블릿 세션
  - getSession
  - loginUser
up:
  - 2024-08-28-Day65
  - 2024-08-29-Day66
  - 2024-09-06-Day71
tags:
  - web
  - servlet
  - 상태관리
---

# HttpSession (클라이언트 전용 보관소)

서버가 **클라이언트 한 명당 하나씩** 들고 있는 보관소. 요청이 끝나도 남아 있어서, 요청 하나보다 오래 살아야 하는 값(로그인한 사용자 같은 것)을 여기 둔다.

## 정의

[[request-response]] 의 `ServletRequest` 에는 세션을 얻는 메서드가 없다. **HTTP 쪽 기능이라 형변환을 먼저 해야 한다** → [[type-casting]]

```java
// HTTP 프로토콜 관련 기능을 사용하려면
// 파라미터로 받은 ServletRequest 객체를 원래 타입으로 형변환 해야 한다.
HttpServletRequest httpReq = (HttpServletRequest) req;

HttpSession session = httpReq.getSession();      // 클라이언트 전용 보관소를 알아낸다
session.setAttribute("loginUser", user);         // 보관한다
```

꺼낼 때는 이름으로 찾고 타입을 되돌린다.

```java
User loginUser = (User) ((HttpServletRequest) req).getSession().getAttribute("loginUser");
board.setWriter(loginUser);
```

보관 범위가 셋으로 갈린다 — **누가 보나**가 기준이다.

| 보관소 | 범위 | 수명 |
|---|---|---|
| `ServletRequest` 속성 | 이 요청을 처리하는 컴포넌트들 | 요청 하나 → [[request-parameter]] |
| **`HttpSession`** | **그 클라이언트의 요청 전부** | 유휴 시간 초과·`invalidate()`·앱 종료까지 |
| `ServletContext` 속성 | 모든 클라이언트 | 애플리케이션이 뜬 동안 → [[servlet-context]] |

## 왜 중요한가

**HTTP 는 요청 사이를 기억하지 않는다.** 로그인은 「한 번 확인하고 그 뒤로 계속 그 사람으로 대한다」는 것이라, 요청 하나가 끝나면 사라지는 곳에는 담을 수 없다. 세션이 그 「그 뒤로 계속」을 만드는 자리다.

### 아흐레 뒤 — 브라우저의 쿠키와 서버의 보관소가 한 연결로 보인다

Day65 는 `getSession()`으로 보관소를 얻는 코드만 보였다. Day71 이 그 보관소를 **다음 요청에서 어떻게 다시 찾는지**를 적는다. 서버가 새 세션을 만들면 보통 세션 ID를 쿠키로 보내고, 브라우저가 이후 요청에 그 ID를 다시 보낸다 → [[cookie]].

그러므로 브라우저를 닫는 일이 세션 객체를 직접 지우는 것은 아니다. 보통은 **세션 ID를 담은 세션 쿠키가 사라져** 다음 요청이 기존 보관소를 찾지 못하게 되는 것이고, 서버에 남은 객체의 실제 만료는 컨테이너의 유휴 시간 정책이 정한다. Day71 의 「브라우저 종료 시 삭제」는 쿠키의 보관 방식으로는 맞지만, `HttpSession` 자체의 수명 설명으로는 한 칸이 빠져 있었다.

그래서 이 회차에서 프로그램의 성격이 바뀐다. Day61~62 의 소켓 서버는 **접속이 이어져 있는 동안**이 곧 한 사용자였고, 그래서 `ThreadLocal` 에 세션을 걸어 두는 것이 통했다 → [[thread-local]]. 웹에서는 접속이 요청마다 끊기므로 **연결이 아니라 식별자로 사람을 잇는다.** 같은 문제(사용자별 상태)에 대한 답이 통로에서 보관소로 옮겨간 것이다.

### 하루 뒤 — 버리는 법과 읽는 자리가 온다

Day65 는 담기만 했다. Day66 이 **버리는 법**과 **모든 화면이 읽는 자리**를 더한다.

```java
((HttpServletRequest) req).getSession().invalidate();   // 로그아웃 = 보관소를 버린다
```

그리고 머리말 서블릿이 세션을 스스로 읽어 로그인 버튼과 사용자 이름을 갈라 그린다.

```java
User loginUser = (User) ((HttpServletRequest) req).getSession().getAttribute("loginUser");
if (loginUser == null) {
  out.println("  <a href='/auth/form' class='btn btn-primary'>로그인</a>");
} else {
  out.printf("  <a href='/user/view?no=%d' ...>%s</a>\n", loginUser.getNo(), loginUser.getName());
  out.println("  <a href='/auth/logout' ...>로그아웃</a>");
}
```

**각 화면은 「누가 로그인했나」를 몰라도 된다** — 머리말을 끼우면 상태가 따라온다 → [[request-dispatcher]]

## 경계와 오해

- **세션 ≠ 로그인** — 세션은 값을 담는 상자일 뿐이고, 「로그인했다」는 것은 **그 상자에 사용자를 넣어 두기로 한 약속**이다. 그래서 이 필기처럼 `loginUser` 라는 이름을 정하는 순간부터 **모든 서블릿이 그 이름을 알아야** 한다 — 오타 하나가 「로그인 안 한 사람」으로 조용히 처리된다.
- **`getSession()` 은 없으면 만든다** — 조회처럼 보이지만 부작용이 있다. 로그인하지 않은 사람이 아무 페이지만 열어도 세션이 생기고 서버 메모리를 차지한다. 만들지 않고 확인만 하려면 `getSession(false)` 로 물어 `null` 을 받아야 한다 → [[read-side-effect]]
- **꺼낼 때 캐스팅이 검사받지 않는다** — `(User) getAttribute("loginUser")` 는 이름이 맞기만 하면 컴파일된다. 다른 타입을 같은 이름으로 넣어 두었으면 **실행 시점에 `ClassCastException`** 이다. 상자가 `Object` 를 담는 대가다 → [[type-casting]] · [[generics]]
- **이 필기의 로그인 폼에는 `method` 가 없다** — 기본값이 `GET` 이므로 암호가 URL 에 실린다. 세션에 잘 담아도 **담기 전에 이미 샌다** → [[html-form]] · [[url]]
- **Day66 이 권한 검사를 처음 넣는데 그 조건이 깨져 있다** — Day65 에 없던 검사가 게시글 변경에 붙었지만, `loginUser == null || loginUser.getNo() > 10 && ...` 가 연산자 우선순위 때문에 **번호 10 이하 회원에게 남의 글 변경을 허용한다.** 「검사가 없다」에서 「검사가 있는데 틀렸다」로 옮겨간 것이고, 뒤쪽이 더 위험하다 — 있으니 안심하게 된다 → [[operator]]
- **로그인 확인이 어디에도 없다** — `BoardAddServlet` 이 `loginUser` 를 꺼내 바로 `setWriter` 에 넣는다. 로그인하지 않은 사람이 그 URL 을 직접 열면 `loginUser` 가 `null` 이고, 그 `null` 이 글쓴이로 저장되거나 그 앞에서 터진다. **「세션에 있으면 로그인한 것」과 「없으면 막는다」는 다른 일**이고 뒤쪽이 빠져 있다 → [[servlet-filter]]
- **세션은 서버 메모리에 있다** — 서버를 여러 대로 늘리면 두 번째 요청이 다른 서버로 갈 수 있고 그 서버에는 그 세션이 없다. 「로그인이 자꾸 풀린다」의 원인이 여기다.
- **브라우저 종료 ≠ 서버 세션 무효화** — 종료하면 보통 세션 ID 쿠키가 사라져 기존 세션을 못 찾게 되지만, 서버가 그 객체를 즉시 지우는 것은 아니다. 쿠키의 `Max-Age`와 서버의 세션 유휴 시간은 다른 시계다 → [[cookie]].

## 함께 보는 개념

- [[request-parameter]] — 클라이언트가 보낸 값(요청과 함께 사라진다)
- [[servlet-context]] — 모두가 공유하는 보관소
- [[request-response]] — 형변환을 해야 하는 이유
- [[html-form]] · [[url]] — 로그인 값이 실려 오는 경로
- [[thread-local]] — 소켓 시절에 같은 문제를 풀던 자리
- [[servlet-filter]] — 로그인 확인을 한 곳에 두는 장치
- [[cookie]] — 이 보관소를 다시 찾게 하는 세션 ID의 운반자
- [[spring-model]] — 세션을 직접 만지지 않고 같은 일을 하는 쪽

## 출처

- [[2024-09-06-Day71]] — 아흐레 뒤. 「Web 보관소」가 `HttpSession`을 사용자별 저장소로 다시 정의하고 `request.getSession().setAttribute(...)` 예를 보인다. 이어 「세션 생성」이 클라이언트마다 고유 번호를 발급해 **쿠키에 보관하고 다음 요청마다 보낸다**고 적어, Day65 에서 답 없이 남은 「다음 요청이 같은 보관소를 어떻게 찾나」를 닫는다. 다만 브라우저 종료가 세션 객체 자체의 즉시 삭제라고 읽히는 부분은 쿠키와 서버 쪽 수명을 섞은 것이다
- [[2024-08-29-Day66]] — 하루 뒤. `invalidate()` 로 **버리는 법**이 오고, `HeaderServlet` 이 세션을 읽어 로그인 상태를 그리면서 **모든 화면이 공유하는 읽기 자리**가 생긴다. 게시글 변경에 권한 검사도 처음 붙지만 그 조건식이 연산자 우선순위 때문에 의도와 다르게 동작한다
- [[2024-08-28-Day65]] — 로그인 서블릿에서 `(HttpServletRequest) req` 로 형변환한 뒤 `getSession()` 으로 「클라이언트 전용 보관소」를 얻고 `setAttribute("loginUser", user)` 로 담았다. `BoardAddServlet` 이 `getAttribute("loginUser")` 로 꺼내 글쓴이로 넣는 것까지가 한 벌이다. 필기가 「클라이언트 전용 보관소」라는 말로 범위를 정확히 짚었지만, 세션이 없을 때 막는 코드와 폼의 `method="POST"` 는 둘 다 없다
