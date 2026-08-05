---
type: concept
id: jsp
title: JSP (JavaServer Pages)
aliases:
  - JSP
  - JavaServer Pages
  - 스크립틀릿
  - scriptlet
  - 디렉티브
up:
  - 2024-08-30-Day67
tags:
  - web
  - jsp
  - servlet
---

# JSP (JavaServer Pages)

HTML 안에 자바 코드를 끼워 쓰는 서버 측 기술. **컨테이너가 이것을 [[servlet]] 소스로 번역해 컴파일한 뒤 실행한다** — 문법이 다를 뿐 결국 서블릿이다.

## 정의

실행 과정이 네 걸음이다.

1. 클라이언트가 페이지를 요청한다
2. 컨테이너가 그 `.jsp` 를 **서블릿 소스로 변환**한다
3. 컴파일해 `.class` 를 만들고 실행한다
4. 실행 결과인 HTML 을 응답으로 보낸다

**첫 요청에서만 2~3 이 일어난다** — 그 다음부터는 만들어 둔 클래스를 쓴다. 그래서 첫 접속이 느리고 두 번째부터 빠르다.

태그가 다섯 갈래다.

| 태그 | 이름 | 하는 일 |
|---|---|---|
| `<%@ ... %>` | 디렉티브 | 페이지 전역 설정. 컨테이너에게 **어떻게 처리할지** 지시 |
| `<jsp:... />` | 액션 | 다른 페이지를 포함·포워딩하거나 객체와 상호작용 |
| `<% ... %>` | 스크립틀릿 | 자바 코드를 그 자리에 넣는다 |
| `<%= ... %>` | 표현식 | 자바 식을 평가해 **결과를 출력**한다 |
| `<%! ... %>` | 선언 | 메서드·필드를 선언한다 |

`<%@ page %>` 의 속성이 실질적이다.

```jsp
<%@ page
    language="java"
    contentType="text/html;charset=UTF-8"
    pageEncoding="UTF-8"
    trimDirectiveWhitespaces="true"%>
```

- `contentType` — **응답** HTML 의 MIME 타입과 인코딩 → [[character-encoding]]
- `pageEncoding` — **이 JSP 파일 자체**의 인코딩
- `trimDirectiveWhitespaces` — 디렉티브 앞뒤 공백 제거

**둘이 다른 것을 가리킨다** — 하나는 내보낼 것, 하나는 읽어 들일 것이다.

## 사용 예시

서블릿이 데이터를 담고, JSP 가 그것을 꺼내 그린다.

```java
// BoardListServlet
List<Board> list = boardDao.list();
req.setAttribute("list", list);
res.setContentType("text/html;charset=UTF-8");
req.getRequestDispatcher("/board/list.jsp").include(req, res);
```

```jsp
<%@ page import="bitcamp.myapp.vo.Board"%>
<%@ page import="java.util.List"%>
<jsp:include page="/header.jsp"/>

<table>
  <tbody>
<%
List<Board> list = (List<Board>) request.getAttribute("list");
for (Board board : list) {
%>
  <tr>
    <td><%=board.getNo()%></td>
    <td><a href='/board/view?no=<%=board.getNo()%>'><%=board.getTitle()%></a></td>
  </tr>
<%
}
%>
  </tbody>
</table>
```

**`request` 를 선언하지 않았는데 쓴다** — 변환된 서블릿의 `_jspService` 메서드가 그 이름의 매개변수를 갖기 때문이다. `out`·`response`·`session`·`application` 도 같은 방식으로 이미 있다(암시 객체) → [[request-parameter]] · [[http-session]]

선언 태그로 메서드를 만들 수도 있다.

```jsp
<%!
private boolean isMember(List<User> members, User user) {
  for (User member : members) {
    if (member.getNo() == user.getNo()) return true;
  }
  return false;
}
%>
```

## 왜 중요한가

**HTML 이 문자열에서 파일로 돌아온다.** Day63~66 의 서블릿은 `out.println("<tr>")` 을 줄마다 썼다 — 태그가 자바 문자열 안에 있어서 편집기가 도와주지 못하고, 따옴표를 겹쳐 쓰느라 `'` 와 `"` 를 섞어야 했다. JSP 는 그 방향을 뒤집는다 — **HTML 이 바깥이고 자바가 안쪽**이다.

그 뒤집기가 [[mvc-pattern]] 을 가능하게 한다. 화면을 만드는 파일과 데이터를 준비하는 파일이 갈리므로, 디자인을 고치는 사람과 로직을 고치는 사람이 다른 파일을 만진다.

## 경계와 오해

- **「HTML 코드와 Java 코드를 분리하여 사용할 수 있어 유지보수가 용이하다」 — 이것이 이 회차에서 가장 오해를 만드는 문장이다** — JSP 가 하는 일은 **섞는 것**이다. 필기의 `list.jsp` 자체가 `<% for %>` 와 `<%= %>` 로 자바와 HTML 을 한 파일에 겹쳐 놓았다. 분리를 만드는 것은 JSP 문법이 아니라 **서블릿이 데이터를 담고 JSP 가 그리기만 하는 배치**, 즉 [[mvc-pattern]] 이다. 문법의 공로로 읽으면 「JSP 를 쓰면 자동으로 깔끔해진다」가 되는데, 스크립틀릿을 많이 쓰면 서블릿보다 더 읽기 어려워진다.
- **JSP ≠ 서블릿과 다른 것** — 「Java Servlet 의 확장」이라는 필기의 표현이 정확하다. 변환된 결과가 서블릿이므로 **생명주기·인스턴스 공유·쓰레드 문제가 똑같이 적용된다** → [[servlet-lifecycle]]
- **`<%! %>` 로 선언한 것은 서블릿의 멤버가 된다 — 인스턴스가 하나다** — 컨테이너가 JSP 당 인스턴스 하나를 만들어 모든 요청이 공유하므로, 선언 태그에 **필드를 두면 쓰레드 안전하지 않다.** 필기의 `isMember` 는 상태가 없어 괜찮지만, 그 이유가 적혀 있지 않다 → [[thread]] · [[servlet-container]]
- **스크립틀릿 안의 변수는 지역 변수, 선언 태그 안의 것은 필드다** — 같은 파일에 있고 생김새가 비슷한데 사는 곳이 다르다 → [[variable-scope]]
- **`<%= %>` 뒤에 세미콜론을 붙이면 안 된다** — 식이지 문장이 아니다. 변환될 때 `out.print(...)` 안에 그대로 들어가므로 세미콜론이 있으면 문법 오류가 된다 → [[expression-vs-statement]]
- **캐스팅이 검사받지 않는다** — `(List<Board>) request.getAttribute("list")` 는 이름만 맞으면 컴파일된다. 서블릿이 담은 이름과 JSP 가 꺼내는 이름이 어긋나면 `null` 이고, 다른 타입이면 실행 시점에 터진다. **문자열로 이어진 계약**이다 → [[generics]] · [[type-erasure]]
- **첫 요청이 느린 것이 「JSP 가 느리다」는 뜻은 아니다** — 변환·컴파일은 한 번이다. 다만 배포 직후 첫 사용자가 그 비용을 낸다.

## 함께 보는 개념

- [[servlet]] · [[servlet-lifecycle]] — 변환된 결과가 되는 것
- [[mvc-pattern]] — 분리를 실제로 만드는 배치
- [[template-engine]] — JSP 가 속한 도구 갈래
- [[request-dispatcher]] — 서블릿과 JSP 를 잇는 장치
- [[character-encoding]] — `contentType`·`pageEncoding` 이 갈리는 축
- [[static-and-dynamic-content]] — 정적 HTML 과의 경계

## 출처

- [[2024-08-30-Day67]] — 「JSP(JavaServer Pages)」 절이 정의·특징·실행 과정(요청 → 서블릿 변환 → `.class` 생성 → 응답)을 정리하고, 「JSP태그의 종류」가 디렉티브와 액션 태그를 가른다. `<%@ page %>` 의 `language`·`contentType`·`pageEncoding`·`trimDirectiveWhitespaces` 를 한 줄씩 설명하고 **`contentType` 과 `pageEncoding` 이 각각 응답과 파일 쪽이라는 것을 정확히 적었다.** `<% %>`·`<%= %>`·`<%! %>` 세 태그와 `<%@ page import %>` 가 실습 코드에 전부 나오며, `list.jsp`·`view.jsp`·`form.jsp`·`error.jsp` 네 파일이 실려 있다. 다만 「HTML 코드와 Java 코드를 분리하여 사용할 수 있어」는 JSP 문법이 아니라 MVC2 배치의 공로이고, 같은 노트의 JSP 파일들이 스크립틀릿으로 둘을 섞어 놓아 스스로 반증한다. 선언 태그가 서블릿의 멤버가 되어 인스턴스를 공유한다는 것, 암시 객체(`request`·`out`)가 어디서 오는지, 첫 요청만 변환된다는 것은 다루지 않았다
