---
type: concept
id: jsp-action-tag
title: JSP 액션 태그 (Action Tag)
aliases:
  - 액션 태그
  - action tag
  - jsp:useBean
  - jsp:setProperty
  - jsp:include
  - jsp:forward
up:
  - 2024-09-10-Day73
tags:
  - web
  - jsp
---

# JSP 액션 태그 (Action Tag)

`<jsp:... />` — JSP 가 기본으로 제공하는 전용 태그. 지시자와 달리 **실행 시점에** 동작하며, 보관소의 객체를 꺼내거나 다른 페이지로 실행을 넘긴다.

## 정의

네 가지가 자주 쓰인다.

### `jsp:useBean` — 보관소에서 꺼내거나, 없으면 만든다

```jsp
<jsp:useBean scope="보관소명" id="객체명" class="클래스명" type="레퍼런스타입"/>
```

- `scope` — 찾을(또는 저장할) 보관소. 기본값은 `page`
- `id` — 그 보관소에서 쓸 이름
- `class` — **못 찾았을 때** 새로 만들 클래스
- `type` — 꺼낸 객체를 담을 레퍼런스 타입

**「꺼내기」와 「만들기」가 한 태그에 들어 있다.** 있으면 꺼내고 없으면 만들어 넣는다.

### `jsp:setProperty` — 꺼낸 객체의 프로퍼티에 값을 넣는다

```jsp
<jsp:setProperty name="beanName" property="propertyName" value="value"/>
```

- `name` — `jsp:useBean` 의 `id`
- `property` — 값을 넣을 프로퍼티 이름
- `value` — 넣을 값

`property="*"` 를 주면 **요청 파라미터 전부를 같은 이름의 프로퍼티에 자동으로 매핑한다.**

### `jsp:include` / `jsp:forward` — 실행을 넘긴다

| 태그 | 제어권 | 결과 |
|---|---|---|
| `jsp:include` | **되돌아온다** | 위임한 페이지의 실행 결과를 이 자리에 포함 |
| `jsp:forward` | 되돌아오지 않는다 | 화면 전체를 다른 페이지가 그린다 |

둘 다 `page` 속성에 지정하는 URL 은 **서블릿이거나 JSP 여야 한다.**

## 사용 예시

세션에 담긴 로그인 사용자를 꺼내고, 없으면 새로 만들어 요청 파라미터로 채운다.

```jsp
<jsp:useBean id="loginUser" scope="session" class="bitcamp.myapp.vo.User"/>
<jsp:setProperty name="loginUser" property="*"/>

<jsp:include page="/header.jsp"/>
안녕하세요, ${loginUser.name}님
```

## 왜 중요한가

**액션 태그는 스크립틀릿을 지우기 위한 문법이다.** 같은 일을 자바로 쓰면 이렇다.

```jsp
<%
User loginUser = (User) session.getAttribute("loginUser");
if (loginUser == null) {
  loginUser = new User();
  session.setAttribute("loginUser", loginUser);
}
%>
```

여덟 줄이 한 줄이 되고, **캐스팅과 null 검사가 태그 안으로 들어간다.** [[expression-language]] 가 「꺼내 출력하기」에서 자바를 걷어내는 것과 같은 방향이고, 둘이 합쳐지면 JSP 에 `<% %>` 가 거의 남지 않는다 → [[mvc-pattern]]

## 경계와 오해

- **`<jsp:include>` ≠ `<%@ include %>`** — 앞은 **실행 시점**에 다른 서블릿/JSP 를 돌려 결과를 받아 오고, 뒤는 **번역 시점**에 소스를 붙여 넣는다. 그래서 `<jsp:include>` 의 대상은 반드시 실행 가능한 서블릿/JSP 이고, `<%@ include %>` 의 대상은 텍스트 파일이면 된다 → [[jsp-directive]] · [[request-dispatcher]]
- **`jsp:forward` ≠ [[redirect]]** — 포워드는 **서버 안에서** 실행을 넘기므로 브라우저는 아무것도 모르고 주소도 그대로다. 리다이렉트는 응답을 돌려주고 브라우저가 **다시 요청**한다 → [[request-dispatcher]]
- **`class` 는 「생성할 것」이지 「기대하는 타입」이 아니다** — 보관소에서 찾으면 `class` 는 아예 쓰이지 않는다. 꺼낸 객체가 엉뚱한 타입이어도 이 속성이 막아 주지 않는다
- **`property="*"` 는 이름이 맞아야만 동작한다** — 요청 파라미터 이름과 프로퍼티 이름이 **문자열로 맞물리는 계약**이라, 오타가 나면 조용히 채워지지 않는다. 컴파일러가 잡아 주지 않는다 → [[request-parameter]]
- **`property="*"` 가 매핑하는 「프로퍼티」는 필드가 아니라 `setXxx()` 메서드다** — 자바빈 규약을 따르는 setter 가 있어야 하고, 없으면 필드가 public 이어도 채워지지 않는다. 필기가 「자바빈의 동일한 이름을 가진 속성」이라고만 적고 규약 자체는 다루지 않은 자리다 → [[encapsulation]]
- **액션 태그는 JSTL 이 아니다** — 액션 태그는 JSP 명세에 **기본 내장**된 것이라 `taglib` 선언 없이 바로 쓰고, 확장 태그는 선언이 필요하다 → [[jsp-directive]]

## 함께 보는 개념

- [[jsp]] — 액션 태그가 속한 기술
- [[jsp-directive]] — 번역 시점에 작용하는 갈래
- [[jsp-scripting-element]] — 액션 태그가 대체하려는 자바 코드
- [[attribute-scope]] — `scope` 속성이 가리키는 네 보관소
- [[expression-language]] — 꺼낸 객체를 출력하는 짝
- [[request-dispatcher]] — include·forward 의 자바 API

## 출처

- [[2024-09-10-Day73]] — 「action tage(Directive element)」 절이 `jsp:useBean`·`jsp:setProperty`·`jsp:include`·`jsp:forward` 를 속성 단위로 정리했다. `useBean` 에서 **「보관소에 저장된 객체를 꺼낼 때도 사용한다」**와 `class` 가 「찾을 수 없을 때 생성할 클래스」라는 것을 명시해 이 태그의 이중 성격을 짚었고, `scope` 의 기본값이 `page` 라는 것도 적었다. `setProperty` 의 `property="*"` 자동 매핑, include 와 forward 의 제어권 차이(되돌아온다/되돌아오지 않는다)가 한 줄씩 나온다. 다만 자바빈 규약(setter 기반 프로퍼티)과 forward 가 리다이렉트와 어떻게 다른지는 다루지 않았고, 절 제목이 「Directive element」로 되어 있으나 액션 태그는 지시자가 아니다
