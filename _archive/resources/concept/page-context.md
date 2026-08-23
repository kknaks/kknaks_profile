---
type: concept
id: page-context
title: PageContext
aliases:
  - PageContext
  - pageContext
  - JspWriter
up:
  - 2024-09-11-Day74
tags:
  - web
  - jsp
  - servlet
---

# PageContext

JSP 페이지 하나의 **실행 상태를 담고 있는 객체.** 페이지 범위의 보관소이면서, 동시에 `request`·`response`·`session`·`application`·`out` 으로 가는 **입구**다.

## 정의

JSP 엔진이 페이지마다 하나씩 만들어 주고, 페이지가 끝나면 버린다. 하는 일이 다섯 갈래다.

1. **속성 관리** — page 범위의 애트리뷰트를 넣고 꺼낸다 → [[attribute-scope]]
2. **페이지 요소 관리** — `request`·`response`·`session`·`application` 에 접근하게 해 준다
3. **출력 관리** — `JspWriter`(암시 객체 `out`)로 응답 본문을 쓴다
4. **에러 처리** — 페이지에서 난 예외를 처리하고 전파한다 → [[exception-handling]]
5. **forward · include 관리** — 다른 자원으로 요청을 넘기거나 결과를 포함한다 → [[request-dispatcher]]

**한 객체가 「보관소 하나」와 「나머지 전부로 가는 통로」를 겸한다**는 것이 이 클래스의 성격이다.

```jsp
${pageContext.request.contextPath}
${pageContext.session.id}
```

[[expression-language]] 의 빌트인 객체 중 `pageContext` 만 이 통로 역할을 하고, 나머지(`param`·`header`·`cookie`)는 값을 담은 맵이다.

## 왜 중요한가

**JSP 의 암시 객체들이 어디서 오는지에 대한 답이다.** `request`·`out`·`session` 을 선언 없이 쓸 수 있는 이유는 번역된 서블릿의 `_jspService()` 가 이것들을 지역 변수로 만들어 두기 때문이고, **그 값들을 한 곳에 모아 들고 있는 것이 `PageContext`** 다 → [[jsp-scripting-element]]

EL 에서 실질적으로 쓰는 곳은 컨텍스트 경로다.

```jsp
<a href="${pageContext.request.contextPath}/board/list">목록</a>
```

배포 이름이 바뀌어도 링크가 안 깨진다 — 주소를 손으로 적지 않는다는 점에서 `c:url` 과 같은 문제를 푼다 → [[jstl-core-tag]] · [[web-application-deployment]]

그리고 **JSTL 태그가 값을 넣고 꺼내는 통로가 이것이다.** `<c:set>` 이 어느 보관소에 넣을지, `<c:out>` 이 어디로 출력할지를 태그 구현체가 `PageContext` 를 통해 정한다 → [[jstl]]

## 경계와 오해

- **PageContext ≠ ServletContext** — 이름이 닮았지만 **정반대**다. 하나는 페이지 하나가 실행되는 동안만 살고, 하나는 애플리케이션이 떠 있는 내내 산다. EL 에서 `pageScope` 와 `applicationScope` 로 갈리는 것이 이 둘이다 → [[servlet-context]]
- **네 보관소 중 하나인 동시에 네 보관소 전부로 가는 문이다** — `${pageScope.name}` 은 이 객체 **안**을 보는 것이고, `${pageContext.session.id}` 는 이 객체를 **거쳐** 다른 곳을 보는 것이다. 같은 이름이 두 역할을 하므로 읽을 때 갈라야 한다
- **보관소 이름을 생략한 검색은 `PageContext` 가 한다** — `${name}` 이 page → request → session → application 순으로 찾는 그 동작이 이 객체의 기능이다. 자바로는 `pageContext.findAttribute("name")` 이다 → [[attribute-scope]]
- **서블릿에는 없다** — 손으로 짠 서블릿에는 `PageContext` 가 없고 `page` 범위 보관소도 없다. JSP 로 번역될 때 생기는 것이라, 서블릿에서 JSP 로 넘길 값은 최소한 `request` 에 담아야 한다 → [[servlet]]
- **`JspWriter` 는 `PrintWriter` 가 아니다** — 버퍼를 두고 동작하며 `<%@ page buffer %>`·`autoFlush` 의 영향을 받는다. 서블릿의 `response.getWriter()` 와 섞어 쓰면 출력 순서가 뒤엉킨다 → [[jsp-directive]] · [[io-stream]]

## 함께 보는 개념

- [[attribute-scope]] — 이 객체가 관리하는 보관소와 검색 순서
- [[expression-language]] — `pageContext` 를 빌트인 객체로 노출하는 표기법
- [[jstl]] — 태그 구현체가 이 객체를 통해 동작한다
- [[jsp-scripting-element]] — 암시 객체가 만들어지는 자리
- [[servlet-context]] — 이름이 닮은 반대편
- [[request-dispatcher]] — forward·include 기능이 위임하는 곳

## 출처

- [[2024-09-11-Day74]] — 「PageContext」 절이 이 클래스를 「페이지의 실행 상태와 관련된 정보를 **캡슐화**한다」로 정의하고 주요기능 다섯(속성 관리 · JSP 페이지 요소 관리 · 출력 관리 · 에러 처리 · forward/include 관리)을 나열했다. 앞 회차(Day73)가 보관소 넷 중 하나로만 스쳐 간 것을 **객체로서** 다시 본 자리이고, 「`request`, `response`, `session`, `application` 과 같은 객체에 대한 접근을 제공한다」는 두 번째 기능이 이 클래스의 통로 역할을 짚는다. 다만 `${pageContext.request.contextPath}` 같은 실제 쓰임, ServletContext 와 이름이 닮은 것에서 오는 혼동, 서블릿에는 이 객체가 없다는 것은 다루지 않았다
