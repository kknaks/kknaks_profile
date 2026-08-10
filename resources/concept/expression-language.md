---
type: concept
id: expression-language
title: EL (Expression Language)
aliases:
  - EL
  - Expression Language
  - 표현 언어
  - 표현식 언어
up:
  - 2024-09-10-Day73
  - 2024-09-11-Day74
tags:
  - web
  - jsp
  - 표기법
---

# EL (Expression Language)

`${ ... }` — JSP 에서 **보관소에 저장된 객체의 값을 자바 코드 없이 꺼내는 표기법.** 점과 대괄호로 객체 안을 파고들며, 값을 찾지 못해도 예외를 내지 않는다.

## 정의

문법이 둘이고 서로 섞어 쓸 수 있다.

```jsp
${ 객체명.프로퍼티명.프로퍼티명 }
${ 객체명["프로퍼티명"]["프로퍼티명"] }
```

- **점 표기법** — 객체의 프로퍼티에 접근한다
- **대괄호 표기법** — 배열·컬렉션의 요소, 또는 이름이 식별자로 쓸 수 없는 프로퍼티에 접근한다

접근 대상은 JavaBean 의 프로퍼티, `Map`, `List`, 배열이다.

### 빌트인 객체

선언 없이 바로 쓸 수 있는 이름들이 있다. 자바 코드로 무엇이 되는지가 그대로 대응된다.

| EL | 자바 코드 |
|---|---|
| `${pageContext.servletContext.프로퍼티명}` | `pageContext.getServletContext().get프로퍼티()` |
| `${pageContext.session.프로퍼티명}` | `pageContext.getSession().get프로퍼티()` |
| `${pageContext.request.프로퍼티명}` | `pageContext.getRequest().get프로퍼티()` |
| `${param.파라미터명}` | `request.getParameter("파라미터명")` |
| `${paramValues.파라미터명}` | `request.getParameterValues("파라미터명")` |
| `${header.헤더명}` | `request.getHeader("헤더명")` |
| `${headerValues.헤더명}` | `request.getHeaders("헤더명")` |
| `${cookie.쿠키명.value}` | 그 이름의 쿠키의 값 |
| `${initParam.파라미터명}` | 초기화 파라미터 |

### 연산자

산술(`+ - * /` · `div` · `%`/`mod`), 논리(`&&`/`and`, `||`/`or`, `!`/`not`), 관계(`==`/`eq`, `!=`/`ne`, `>`/`gt`, `>=`/`ge`, `<`/`lt`, `<=`/`le`), 조건(`조건 ? 식1 : 식2`), 그리고 `empty`.

**기호와 낱말이 짝을 이룬다** — `<` 는 HTML 안에서 태그 시작으로 읽히므로 `lt` 라는 대안이 있다.

`empty` 는 값이 없는지 검사한다 — 보관소에 없거나, `null` 이거나, 빈 문자열·빈 컬렉션이면 `true` 다.

## 사용 예시

같은 값을 EL 과 스크립틀릿으로 각각 꺼내면 이렇게 대응된다.

```jsp
<%
pageContext.setAttribute("name", "홍길동");
request.setAttribute("name", "임꺽정");
%>

PageContext 보관소 : ${pageScope.name}
PageContext 보관소 : <%=pageContext.getAttribute("name")%>

ServletRequest 보관소 : ${requestScope.name}
ServletRequest 보관소 : <%=request.getAttribute("name")%>
```

문자열 비교가 특히 다르다.

```jsp
${name == "홍길동" ? "맞다!" : "아니다!"}
```

```java
String a = "홍길동";
String b = new String("홍길동");
a == b        // false — 인스턴스의 주소를 비교
a.equals(b)   // true  — 인스턴스의 값을 비교
```

**EL 의 `==` 는 자바의 `==` 가 아니라 `equals()` 쪽으로 동작한다** → [[string-comparison]] · [[object-equality]]

## 왜 중요한가

**JSP 에서 자바를 걷어내는 두 축 중 하나다**(다른 하나는 [[jsp-action-tag]]). `<%=(User)request.getAttribute("user")%>` 를 쓰려면 캐스팅과 null 검사와 import 가 따라오는데, `${user.name}` 은 그 셋을 다 없앤다.

**값이 없을 때 조용한 것**이 특히 크다. 스크립틀릿은 `null.getName()` 에서 `NullPointerException` 으로 페이지 전체를 죽이지만, EL 은 **빈 문자열을 출력하고 넘어간다.** 화면 하나가 데이터 하나 때문에 통째로 깨지지 않는다.

그 대가로 오류가 조용해진다 — 다음 항목이 그 뒷면이다.

## 경계와 오해

- **EL 은 지역 변수를 못 읽는다 — 오직 보관소의 값만 꺼낸다** — 필기가 정확히 짚은 자리다. 스크립틀릿에서 `String[] names = new String[]{...}` 를 선언해도 `${names[0]}` 는 아무것도 내놓지 않는다. `pageContext.setAttribute("names", ...)` 로 **보관소에 넣어야** 보인다 → [[attribute-scope]]
- **이름이 틀려도 아무 일도 일어나지 않는다** — 없는 이름은 빈 문자열이다. 오타가 「빈 화면」으로만 나타나고 로그도 남지 않으므로, **디버깅이 예외보다 어렵다.** 값이 안 보일 때 먼저 의심할 것은 문법이 아니라 **이름과 보관소**다
- **`empty` ≠ `null` 검사** — `empty` 는 `null` 뿐 아니라 빈 문자열·빈 컬렉션·빈 배열도 참으로 본다. 「값이 없다」와 「비어 있다」를 구분해야 하면 `empty` 로는 안 된다 → [[sql-null]]
- **`.` 은 콤마가 아니라 점이다** — 필기의 「콤마(.)」는 표기가 어긋난 것이고, 실제로 쓰는 것은 점 표기법(dot notation)이다
- **`${param.x}` 와 `${x}` 는 다르다** — 앞은 요청 **파라미터**(쿼리스트링·폼), 뒤는 보관소의 **애트리뷰트**다. 서로 다른 곳이라 하나가 있다고 다른 하나가 채워지지 않는다 → [[request-parameter]]
- **`${...}` 는 EL 이고 `<%= %>` 는 표현식 태그다** — 둘 다 「값을 출력」하지만 EL 은 자바 문법이 아니고, 볼 수 있는 범위도 좁다(보관소만) → [[jsp-scripting-element]]
- **EL 이 [[ognl]] 은 아니다** — 둘 다 객체 그래프를 문자열로 탐색하는 표기법이지만 서로 다른 명세이고, 쓰이는 곳도 다르다
- **EL 은 이스케이프하지 않는다** — `${board.title}` 은 값을 **그대로** 출력하므로, 값 안의 `<script>` 가 브라우저에서 실행된다. `<c:out value="${board.title}"/>` 는 기본으로 이스케이프한다. **더 짧은 쪽이 안전하지 않은 쪽**이라는 것이 이 표기법에서 가장 값비싼 함정이다 → [[output-escaping]] · [[jstl-core-tag]]
- **출력만이 아니라 태그의 입력이기도 하다** — `${...}` 를 「값을 찍는 문법」으로만 알면 절반이다. [[jstl]] 태그의 속성값이 전부 EL 을 받으므로(`test="${age >= 18}"`, `items="${list}"`, `value="${user}"`), **연산자와 `empty` 는 출력이 아니라 조건을 적기 위해 있다.** Day73 에서 나열로만 보이던 연산자들이 실제로 쓰이는 자리가 그쪽이다

## 함께 보는 개념

- [[attribute-scope]] — EL 이 값을 찾는 곳과 그 순서
- [[ognl]] — 같은 문제를 푸는 다른 표기법
- [[object-graph]] — 점 표기법이 따라가는 구조
- [[jsp-action-tag]] — JSP 에서 자바를 걷어내는 다른 축
- [[jsp-scripting-element]] — EL 이 대체하는 표현식 태그
- [[request-parameter]] · [[cookie]] · [[http-session]] · [[servlet-context]] — 빌트인 객체가 가리키는 것들
- [[jstl]] · [[jstl-core-tag]] — EL 을 속성값으로 받아 쓰는 태그들
- [[output-escaping]] — EL 이 하지 않는 것
- [[page-context]] — 빌트인 객체 `pageContext` 의 실체

## 출처

- [[2024-09-11-Day74]] — 하루 뒤. **EL 이 출력에서 제어로 넘어가는 회차**다. Core 태그의 속성값이 전부 EL 로 채워지고(`test="${userAge >= 18}"`, `items="${itemList}"`, `value="${message}"`), Day73 이 나열로만 보였던 관계·논리 연산자가 여기서 실제로 조건을 적는 데 쓰인다. `ex10` 실습이 `c:param` 으로 만든 주소를 받는 쪽에서 `${param.name}` 으로 읽어, 빌트인 객체 `param` 이 어디서 채워지는지를 한 벌로 보인다. 그리고 **`c:out` 이 이스케이프하는 반면 `${...}` 는 하지 않는다**는 대비가 이 회차에서 처음 생기는데, 필기는 `c:out` 쪽 설명에만 적고 둘을 나란히 놓지 않았다
- [[2024-09-10-Day73]] — 「Expression Language 표기법」 절 전체. 「용어정의」가 점 표기법·대괄호 표기법을 가르고, 「EL에서 사용할 수 있는 빌트인 객체」가 `pageContext`·`param`·`paramValues`·`header`·`headerValues`·`cookie`·`initParam` 을 **대응하는 자바 코드와 나란히** 적어 EL 이 결국 무엇을 부르는지 보인다. 「보관소에서 값 꺼내기」의 실습이 이 개념의 핵심 제약을 실험으로 보여 준다 — 스크립틀릿의 지역 배열은 `${names[0]}` 로 안 나오고, 같은 배열을 `pageContext.setAttribute()` 로 넣으면 나온다. 「EL 연산자」 절이 기호형과 낱말형(`div`·`mod`·`eq`·`lt`)을 짝지어 나열하고, `empty` 와 조건 연산자 예시 끝에 `==` 와 `equals()` 의 차이를 보이는 자바 코드를 붙여 두었다(EL 의 `==` 가 어느 쪽인지는 적지 않았다). 이름이 틀렸을 때 빈 문자열이 나온다는 것은 적혀 있으나 그것이 디버깅에서 갖는 값은 다루지 않았다
