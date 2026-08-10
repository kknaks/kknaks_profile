---
type: concept
id: jstl-core-tag
title: JSTL Core 태그 (c:)
aliases:
  - Core 태그
  - c:out
  - c:set
  - c:remove
  - c:if
  - c:choose
  - c:forEach
  - c:url
  - c:import
  - c:redirect
  - c:param
up:
  - 2024-09-11-Day74
tags:
  - web
  - jsp
  - jstl
---

# JSTL Core 태그 (c:)

[[jstl]] 의 기본 모듈. **출력 · 변수 · 흐름 제어 · URL** 네 가지 일을 태그로 한다. JSP 에서 스크립틀릿을 걷어내는 데 실제로 쓰이는 것이 대부분 여기 있다.

## 정의

### 출력 — `c:out`

| 속성 | 하는 일 | 기본값 |
|---|---|---|
| `value` | 출력할 값 | `null` |
| `default` | `value` 가 `null`·부재일 때 대신 출력할 값 | `null` |
| `escapeXml` | XML/HTML 이스케이프 여부 | **`true`** |

`default` 는 속성으로도, 태그 본문으로도 줄 수 있다.

```jsp
<c:out value="${null}" default="홍길동"/>
<c:out value="${null}">홍길동</c:out>
```

### 변수 — `c:set` · `c:remove`

| 태그 | 속성 | 하는 일 |
|---|---|---|
| `c:set` | `var` · `value` · `scope` | 보관소에 이름-값을 넣는다 (`scope` 기본 `page`) |
| `c:set` | `target` · `property` · `value` | **객체의 프로퍼티**에 값을 넣는다 |
| `c:remove` | `var` · `scope` | 보관소에서 이름을 지운다 |

`var` 를 쓰면 보관소의 **애트리뷰트**를, `target`/`property` 를 쓰면 **객체 안**을 건드린다 → [[attribute-scope]]

### 흐름 제어 — `c:if` · `c:choose`

```jsp
<c:if test="${userAge >= 18}" var="isAdult">
  성인입니다.
</c:if>
```

- `test` — 참일 때만 본문을 실행한다 (필수)
- `var` — 판정 결과를 보관소에 담아 뒤에서 다시 쓴다

여러 갈래는 `c:choose` 다. `c:when` 을 위에서부터 검사해 **처음 참인 것 하나만** 실행하고, 전부 거짓이면 `c:otherwise` 로 간다 → [[switch-statement]]

### 반복 — `c:forEach`

| 속성 | 하는 일 |
|---|---|
| `items` | 반복할 컬렉션·배열·맵 |
| `var` | 현재 요소를 담을 이름 |
| `begin` · `end` | 시작·끝 인덱스 (첫 인덱스는 0) |
| `step` | 건너뛸 간격 (기본 1) |

### URL — `c:url` · `c:import` · `c:redirect`

셋 다 자식으로 `<c:param name="..." value="..."/>` 을 받아 쿼리 파라미터를 붙인다.

| 태그 | 하는 일 |
|---|---|
| `c:url` | URL **문자열을 만든다**(가지 않는다). `var` 로 담아 두고 쓴다 |
| `c:import` | 다른 리소스를 실행·요청해 **결과를 가져온다**. 외부 URL 도 된다 |
| `c:redirect` | 클라이언트에게 **다시 요청하라고 응답한다** → [[redirect]] |

`c:import` 는 `charEncoding` 으로 가져온 것의 인코딩을, `context` 로 다른 애플리케이션의 컨텍스트 경로를 지정할 수 있다.

## 사용 예시

`c:url` 로 파라미터가 붙은 주소를 만들고, 받는 쪽은 EL 로 읽는다.

```jsp
<%-- ex10 --%>
<c:url value="ex10_sub.jsp" var="url1">
    <c:param name="name" value="홍길동"/>
    <c:param name="age" value="20"/>
    <c:param name="gender" value="woman"/>
</c:url>
<pre>${url1}</pre>
```

```jsp
<%-- ex10_sub --%>
name = ${param.name}<br>
age = ${param.age}<br>
gender = ${param.gender}<br>
```

`<pre>${url1}</pre>` 로 **만들어진 주소를 눈으로 확인하는 것**이 이 실습의 요점이다 — `c:url` 은 가지 않고 문자열만 만든다.

## 왜 중요한가

**HTML 과 짝이 맞는 문법으로 흐름을 적게 된다.** 스크립틀릿으로 반복을 쓰면 자바 블록의 `{`·`}` 가 서로 다른 `<% %>` 에 흩어져 HTML 태그와 교차하는데, `<c:forEach>` 는 여는 태그와 닫는 태그가 HTML 과 같은 규칙으로 중첩된다 — **편집기가 짝을 찾아 준다.**

`c:url` 의 값은 편의가 아니라 **정확성**이다. 손으로 `"/user/profile?name=" + name` 을 이으면 컨텍스트 경로가 빠지고 특수문자가 인코딩되지 않는다. 배포 이름이 바뀌면 링크가 전부 깨지는 자리이기도 하다 → [[url]] · [[web-application-deployment]]

## 경계와 오해

- **`c:out` 의 `escapeXml` 기본값이 `true` 라는 것이 이 태그의 존재 이유다** — `${title}` 로 그냥 쓰면 값 안의 `<script>` 가 태그로 실행된다. `<c:out value="${title}"/>` 는 그것을 문자로 만든다. **편의 태그가 아니라 안전 장치**다 → [[output-escaping]]
- **`c:if` 에는 else 가 없다** — 반대 경우를 쓰려면 `c:choose`/`c:otherwise` 를 쓰거나 `c:if` 를 두 번 쓴다. 두 번 쓰면 조건이 두 곳에 생겨 한쪽만 고치는 사고가 난다 → [[if-statement]]
- **`c:set` 의 「변수」는 자바 변수가 아니다** — 보관소에 담기는 애트리뷰트다. 그래서 `scope="session"` 을 주면 **요청이 끝나도 남는다.** 화면 안의 임시값이라고 생각하고 세션에 담으면 다음 요청에서 옛 값이 나온다 → [[attribute-scope]]
- **`c:remove` 가 「메모리를 효율적으로 관리」하는 것은 과장이다** — `page` 보관소는 어차피 페이지가 끝나면 사라진다. 이 태그가 실제로 쓸모 있는 곳은 **세션에 남아 있는 값을 지울 때**다 → [[http-session]] · [[garbage-collection]]
- **`c:url` ≠ `c:redirect`** — 앞은 문자열을 만들 뿐 아무 데도 가지 않고, 뒤는 실제로 응답을 보낸다. 「URL 을 다룬다」로 뭉뚱그리면 갈리지 않는다
- **`c:import` ≠ `<jsp:include>` ≠ `<%@ include %>`** — `c:import` 만 **외부 URL 도 가져올 수 있고**, 가져온 것을 `var` 에 **문자열로 담아 둘 수 있다**. 나머지 둘은 같은 애플리케이션 안이고 결과를 그 자리에 바로 쓴다 → [[jsp-action-tag]] · [[jsp-directive]] · [[request-dispatcher]]
- **외부 URL 을 `c:import` 로 가져오는 것은 서버가 나가서 요청하는 것이다** — 브라우저가 아니라 **서버가 클라이언트가 된다.** 그쪽이 느리면 이 페이지가 같이 느려지고, 주소를 사용자 입력에서 받으면 서버가 내부망을 대신 긁어 주는 통로가 된다 → [[client-server-model]]
- **`begin`·`end` 는 인덱스이지 개수가 아니다** — `end="3"` 은 네 개(0·1·2·3)를 돈다. `items` 없이 `begin`/`end` 만 주면 숫자 반복이 된다 → [[one-based-numbering]]

## 함께 보는 개념

- [[jstl]] — 이 태그들이 속한 라이브러리
- [[jstl-format-tag]] — 같은 라이브러리의 형식 지정 모듈
- [[output-escaping]] — `c:out` 이 기본으로 하는 일
- [[expression-language]] — 속성값을 채우는 표기법
- [[attribute-scope]] — `scope` 속성이 가리키는 곳
- [[redirect]] · [[request-dispatcher]] — `c:redirect`·`c:import` 가 감싸는 장치
- [[url]] — `c:url` 이 조립하는 것

## 출처

- [[2024-09-11-Day74]] — 「Core 태그」 절이 `c:out`·`c:set`·`c:remove`·`c:if`·`c:choose`·`c:forEach`·`c:url`·`c:import`·`c:redirect` 아홉 개를 **속성 단위로 타입·기본값·예시까지** 정리했다. `c:out` 의 `escapeXml` 기본값이 `true` 이고 그것이 「HTML 태그가 그대로 출력되는 것을 방지」한다는 것, `c:set`/`c:remove` 의 `scope` 기본값이 `page` 라는 것, `c:forEach` 의 첫 인덱스가 0 이라는 것이 명시돼 있다. `c:out` 의 `default` 를 속성과 본문 두 방식으로 보인 사용예제와, `c:url`+`c:param` 으로 만든 주소를 `<pre>${url1}</pre>` 로 찍어 보고 받는 쪽에서 `${param.name}` 으로 읽는 `ex10` 실습이 실려 있다. 다만 `c:if` 에 else 가 없다는 것, `c:remove` 가 실제로 쓸모 있는 자리, 외부 URL 을 `c:import` 할 때 서버가 클라이언트가 된다는 것은 다루지 않았다
