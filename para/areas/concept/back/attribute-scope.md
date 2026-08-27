---
type: concept
id: attribute-scope
title: 보관소 범위 (Attribute Scope)
aliases:
  - 보관소
  - 보관소 범위
  - attribute scope
  - pageScope
  - requestScope
  - sessionScope
  - applicationScope
up:
  - 2024-09-10-Day73
  - 2024-09-11-Day74
tags:
  - web
  - jsp
  - servlet
---

# 보관소 범위 (Attribute Scope)

웹 애플리케이션이 값을 담아 두는 네 개의 보관소와, **그중 어디에 담느냐가 그 값의 수명과 공유 범위를 정한다**는 규칙. 좁은 것부터 page → request → session → application 이다.

## 정의

| 보관소 | EL 이름 | 살아 있는 동안 | 누가 본다 |
|---|---|---|---|
| PageContext | `pageScope` | 그 JSP 한 장을 실행하는 동안 | 그 페이지만 |
| ServletRequest | `requestScope` | 요청 하나를 처리하는 동안 | 그 요청에 참여한 서블릿·JSP 전부 → [[request-response]] |
| HttpSession | `sessionScope` | 사용자의 세션이 유지되는 동안 | 그 사용자의 모든 요청 → [[http-session]] |
| ServletContext | `applicationScope` | 애플리케이션이 떠 있는 동안 | 모든 사용자 → [[servlet-context]] |

**보관소 이름을 생략하면 좁은 것부터 순서대로 찾는다.**

```
pageScope → requestScope → sessionScope → applicationScope
```

먼저 찾은 것을 쓰고, 끝까지 못 찾으면 [[expression-language]] 에서는 **빈 문자열**이 나온다.

## 사용 예시

같은 이름 `name` 을 네 보관소에 각각 담아 두면, 어느 것이 나오는지가 갈린다.

```jsp
<%
pageContext.setAttribute("name", "홍길동");
request.setAttribute("name", "임꺽정");
session.setAttribute("name", "유관순");
application.setAttribute("name", "안중근");
%>

${pageScope.name}         <%-- 홍길동 --%>
${requestScope.name}      <%-- 임꺽정 --%>
${sessionScope.name}      <%-- 유관순 --%>
${applicationScope.name}  <%-- 안중근 --%>

${name}                   <%-- 홍길동 — 이름을 생략하면 가장 좁은 것부터 --%>
```

액션 태그의 `scope` 속성도 같은 이름을 받는다.

```jsp
<jsp:useBean id="loginUser" scope="session" class="bitcamp.myapp.vo.User"/>
```

## 왜 중요한가

**어느 보관소에 넣느냐가 곧 「누구에게 보일 것인가」의 결정이다.** 잘못 고르면 두 방향으로 틀어진다.

- **너무 넓게 담으면** — 한 사용자의 데이터가 다른 사용자에게 보인다. 요청 한 번만 쓸 값을 `application` 에 넣으면 그 값은 서버가 살아 있는 내내 남고, 모두가 같은 것을 본다
- **너무 좁게 담으면** — 포워딩 이후에 사라진다. `pageScope` 에 담고 다른 JSP 로 넘기면 그쪽에서는 아무것도 못 꺼낸다 → [[request-dispatcher]]

**생략 검색이 편한 만큼 위험하다.** `${name}` 은 어느 보관소에서 온 값인지 코드에 안 적혀 있으므로, 같은 이름이 두 곳에 있으면 **좁은 쪽이 넓은 쪽을 가린다.** 세션에 담아 둔 값이 어느 페이지에서만 다르게 나온다면 request 나 page 에 같은 이름이 있는지 먼저 본다 → [[field-hiding]] 과 같은 모양의 함정이다.

## 경계와 오해

- **네 보관소는 크기가 아니라 수명이 다르다** — 「더 큰 저장소」가 아니라 **언제 없어지는가**가 다르다. 담긴 값의 개수나 용량 제한과는 무관하다
- **`page` 가 기본값이다** — `<jsp:useBean>` 에서 `scope` 를 생략하면 `page` 다. 그 페이지 안에서만 살아 있으므로, 포워딩 대상에서 안 보인다고 놀랄 자리다 → [[jsp-action-tag]]
- **애트리뷰트 ≠ 파라미터** — 보관소에 담는 값(애트리뷰트)은 **서버가 넣은 것**이고, 파라미터는 **클라이언트가 보낸 것**이다. `${param.x}` 는 이 네 보관소를 아예 보지 않는다 → [[request-parameter]]
- **[[redirect]] 는 request 보관소를 건너뛴다** — 리다이렉트는 브라우저가 **새 요청**을 보내는 것이라 앞 요청의 `requestScope` 는 그 시점에 이미 사라졌다. 리다이렉트 너머로 값을 넘기려면 최소한 세션이 필요하다
- **`applicationScope` 는 쓰레드 안전하지 않다** — 모든 요청이 같은 곳을 만지므로, 값을 바꾸는 코드가 있으면 동기화가 필요하다 → [[thread]]
- **PageContext 라는 객체 자체는 이 개념보다 넓다** — 여기서는 보관소의 하나로만 다룬다. 그 객체는 보관소이면서 나머지 셋으로 가는 통로이기도 하다 → [[page-context]]
- **담는 문법이 셋인데 전부 같은 곳을 만진다** — 스크립틀릿의 `session.setAttribute("x", v)`, 액션 태그의 `<jsp:useBean scope="session">`, JSTL 의 `<c:set var="x" scope="session">` 이 모두 같은 보관소에 같은 이름으로 넣는다. **문법이 달라도 이름이 겹치면 서로 덮어쓴다** → [[jstl-core-tag]] · [[jsp-action-tag]]
- **`<c:set>` 의 「변수」는 지역 변수가 아니라 애트리뷰트다** — `scope` 를 생략하면 `page` 라 페이지가 끝나면 사라지지만, `session` 을 주면 **다음 요청에도 남는다.** 화면 안의 임시 계산값이라고 생각하고 넓은 보관소에 담는 것이 이 개념에서 가장 흔한 사고다

## 함께 보는 개념

- [[expression-language]] — 이 순서로 값을 찾는 표기법
- [[jsp-action-tag]] — `scope` 속성으로 보관소를 지정한다
- [[servlet-context]] · [[http-session]] · [[request-response]] — 네 보관소 중 셋
- [[request-dispatcher]] — request 보관소가 유지되는 경계
- [[redirect]] — request 보관소가 끊기는 경계
- [[variable-scope]] — 자바 안에서 같은 물음을 다루는 개념
- [[page-context]] — 보관소이면서 나머지로 가는 통로인 객체
- [[jstl-core-tag]] — `c:set`·`c:remove` 로 보관소를 다루는 태그

## 출처

- [[2024-09-11-Day74]] — 하루 뒤. **같은 보관소를 태그로 다루는 회차**다. 「c:set」이 `var`·`value`·`scope` 로 값을 넣고 「c:remove」가 `var`·`scope` 로 지우며, 둘 다 `page`·`request`·`session`·`application` 을 받고 **기본값이 `page`** 라는 것을 명시했다. 「PageContext」 절이 「페이지 범위(Page scope)의 속성을 설정하고 가져오는 기능」을 첫 번째 기능으로 적어, Day73 이 EL 쪽에서 본 보관소를 **객체 쪽에서** 다시 본다. 다만 `<c:set scope="session">` 이 요청을 넘어 남는다는 것과, 「c:remove 로 메모리를 효율적으로 관리한다」가 `page` 보관소에서는 별 의미가 없다는 것은 다루지 않았다
- [[2024-09-10-Day73]] — 「보관소에서 값 꺼내기」 절이 **보관소 이름을 생략했을 때의 검색 순서**(`pageScope → requestScope → sessionScope → applicationScope`)와 못 찾으면 빈 문자열을 리턴한다는 규칙을 적었다. 같은 이름 `name` 을 네 보관소에 모두 담아 놓고 EL 과 스크립틀릿으로 각각 꺼내 보이는 실습이 이 개념의 뼈대다. 「jsp:useBean」 절이 보관소 넷을 `ServletContext, HttpSession, ServletRequest, PageContext` 로 나열하고 `scope` 의 기본값이 `page` 라고 명시했다. 다만 좁은 보관소가 넓은 보관소를 가린다는 것과, 어느 것을 골라야 하는지의 기준은 다루지 않았다
