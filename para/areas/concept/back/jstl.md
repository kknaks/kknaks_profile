---
type: concept
id: jstl
title: JSTL (JSP Standard Tag Library)
aliases:
  - JSTL
  - JSP Standard Tag Library
  - JavaServer Pages Standard Tag Library
  - 표준 태그 라이브러리
  - 커스텀 태그
up:
  - 2024-09-11-Day74
tags:
  - web
  - jsp
  - 표준
---

# JSTL (JSP Standard Tag Library)

JSP 에서 **자바 코드로 하던 일을 태그로 하게 만든 표준 라이브러리.** 조건·반복·URL 처리·형식 지정을 `<c:if>`·`<c:forEach>` 같은 태그로 적는다.

## 정의

**규격과 구현이 갈려 있다.**

- **JSTL API** — 기본 클래스와 인터페이스, 즉 **규격**
- **JSTL 구현체** — 그 규격에 맞춰 실제로 동작을 만든 것

그래서 라이브러리를 넣을 때 두 개의 jar 가 필요하다 — 자바 표준이 흔히 취하는 모양이다 → [[interface]] · [[java-ee]]

쓰려면 페이지마다 **가져오겠다고 선언**한다.

```jsp
<%@ taglib uri="태그 라이브러리 모듈명" prefix="접두어" %>
```

- `uri` — 어느 라이브러리인지 가리키는 경로
- `prefix` — 이 페이지에서 그 라이브러리를 부를 **접두어**

선언한 뒤에는 접두어로 태그를 쓴다.

```jsp
<접두어:태그명 속성="값" ...> ... </접두어:태그명>
```

모듈(Area)이 여럿이고, 접두어는 관례적으로 이렇게 붙는다.

| 모듈 | 접두어 | 하는 일 |
|---|---|---|
| Core | `c` | 출력·변수·조건·반복·URL → [[jstl-core-tag]] |
| Formatting / I18N | `fmt` | 날짜·숫자 형식, 다국어 → [[jstl-format-tag]] |
| XML | `x` | XML 처리 → [[xml]] |
| SQL | `sql` | 데이터베이스 접근 |
| Functions | `fn` | 문자열 함수 |

## 사용 예시

Core 모듈을 `c` 로 가져와 쓰는 형태.

```jsp
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>

<c:forEach items="${boardList}" var="board">
  <tr>
    <td>${board.no}</td>
    <td><c:out value="${board.title}"/></td>
  </tr>
</c:forEach>
```

## 왜 중요한가

**JSP 에서 `<% %>` 가 사라지는 마지막 조각이다.** [[expression-language]] 가 「값을 꺼내 출력하기」를, [[jsp-action-tag]] 가 「객체 다루기」를 자바 없이 하게 만들었지만, **조건과 반복은 여전히 스크립틀릿이었다.**

```jsp
<%
for (Board board : list) {
%>
  <tr><td><%=board.getTitle()%></td></tr>
<%
}
%>
```

이 모양의 문제는 **여는 괄호와 닫는 괄호가 서로 다른 스크립틀릿에 있다**는 것이다. HTML 태그와 자바 블록이 서로 교차해서 열리고 닫히므로, 편집기가 어느 쪽도 제대로 짝지어 주지 못한다. JSTL 은 반복을 **태그로** 만들어 그 교차를 없앤다 — `<c:forEach>` 는 열고 닫는 자리가 HTML 태그와 같은 규칙을 따른다.

그리고 **표준이라는 것이 값이다.** 접두어와 태그 이름이 프로젝트마다 다르면 배우는 비용이 매번 든다 → [[template-engine]]

## 경계와 오해

- **JSTL ≠ JSP 문법** — 액션 태그(`<jsp:... />`)는 JSP 명세에 **내장**돼 `taglib` 선언 없이 바로 쓰지만, JSTL 은 **외부 라이브러리**라 jar 를 넣고 선언해야 한다. 생김새가 같아 헷갈리는 자리다 → [[jsp-action-tag]] · [[jsp-directive]]
- **접두어는 관례이지 규칙이 아니다** — `prefix="c"` 는 바꿀 수 있다. 태그를 결정하는 것은 `uri` 이고, 접두어는 **이 페이지 안에서만 통하는 별명**이다. 남의 코드에서 `<c:if>` 를 보고 Core 라고 단정하기 전에 위쪽 `taglib` 선언을 봐야 한다
- **「유지보수가 쉬운 코드」는 태그가 주는 게 아니다** — 필기의 표현이지만, `<c:if>` 를 겹겹이 쌓으면 스크립틀릿보다 읽기 어려워진다. 태그가 주는 것은 **HTML 과 짝이 맞는 문법**이고, 로직을 화면에서 걷어내는 것은 여전히 [[mvc-pattern]] 의 일이다
- **JSTL 의 SQL 모듈은 있지만 쓰지 않는다** — 화면에서 직접 DB 에 붙는 것이라 계층 분리를 정면으로 깬다. 「제공된다」와 「써도 된다」가 다른 자리다 → [[dao-pattern]]
- **`uri` 는 인터넷 주소가 아니다** — `http://java.sun.com/jsp/jstl/core` 는 **이름**이지 접속할 곳이 아니다. 네트워크가 없어도 동작하고, 그 주소를 브라우저로 열 필요도 없다 → [[url]]

## 함께 보는 개념

- [[jstl-core-tag]] · [[jstl-format-tag]] — 이 라이브러리의 두 모듈
- [[expression-language]] — JSTL 태그의 속성값을 채우는 표기법
- [[jsp-directive]] — `taglib` 으로 가져오는 자리
- [[jsp-action-tag]] — 선언 없이 쓰는 내장 태그
- [[page-context]] — JSTL 태그가 값을 넣고 꺼내는 통로
- [[template-engine]] — JSTL 이 완성하는 갈래

## 출처

- [[2024-09-11-Day74]] — 「JSTL의 개념」 절이 정의와 **구성요소를 API 와 구현체로 가른 것**, `<%@ taglib uri="..." prefix="..."%>` 선언 문법과 `<접두어:태그명 속성="값">` 사용 문법을 적었다. 앞 회차(Day73)의 「Tablib」 절이 이름만 소개하고 넘어간 자리를 여기서 채운다. 모듈이 여럿이라는 것은 이미지로만 있고, 본문이 실제로 다루는 것은 Core 와 fmt 둘이다. 다만 접두어가 페이지 안에서만 통하는 별명이라는 것, `uri` 가 접속 주소가 아니라 이름이라는 것은 다루지 않았다
