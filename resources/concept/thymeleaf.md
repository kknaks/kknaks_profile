---
type: concept
id: thymeleaf
title: Thymeleaf
aliases:
  - Thymeleaf
  - 타임리프
  - "th:text"
  - "th:each"
  - 내추럴 템플릿
up:
  - 2024-10-22-Day99
tags:
  - web
  - spring
  - 템플릿
---

# Thymeleaf

**HTML 파일 그대로가 템플릿인 엔진.** 서버를 안 거치고 브라우저로 열어도 화면이 보이고, 서버를 거치면 그 자리에 실제 데이터가 채워진다.

## 정의

문법이 **속성**으로 들어간다 — 태그를 새로 만들지 않는다.

```html
<p th:text="${user.name}">User Name</p>
```

- **브라우저로 그냥 열면** — `User Name` 이 보인다 (`th:text` 는 모르는 속성이라 무시된다)
- **서버를 거치면** — 본문이 `${user.name}` 의 값으로 **대체된다**

이것을 **내추럴 템플릿**이라 부르고, [[jsp]] 의 `<% %>` 와 갈리는 가장 큰 차이다.

### 표현식 네 종류

| 표기 | 무엇을 가리키나 |
|---|---|
| `${...}` | 모델에 담긴 데이터 → [[spring-model]] |
| `#{...}` | 메시지 파일(`messages.properties`)의 키 — 다국어 |
| `@{...}` | **URL** — 컨텍스트 경로를 붙여 준다 → [[url]] |
| `*{...}` | **선택된 객체**의 필드 (`th:object` 로 정한 폼 대상) |

```html
<p  th:text="#{welcome.message}">Welcome, Guest!</p>
<a  th:href="@{/user/profile}">Profile</a>
<input type="text" th:field="*{name}" />
```

### 값 만들기

```html
<p th:text="'Hello, ' + ${name} + '!'"></p>     <!-- 문자열 결합 -->
<p th:text="|The name is ${name}|"></p>          <!-- 리터럴 대체 — 더 짧다 -->
```

리터럴은 텍스트(`'...'`)·숫자·불리언·`null`·**토큰**(따옴표 없는 낱말)이 있다.

### 조건과 반복

```html
<p th:text="${user.active} ? 'Active' : 'Inactive'"></p>   <!-- 삼항 -->
<p th:text="${user.name} ?: 'Anonymous'"></p>              <!-- 엘비스: 없으면 기본값 -->

<li th:each="item : ${items}" th:text="${item.name}">Item Name</li>

<p th:if="${user.active}">Active User</p>
<p th:unless="${user.active}">Inactive User</p>
```

**`th:if` 와 `th:unless` 가 짝**이다 — else 가 없는 [[jstl-core-tag]] 의 `c:if` 와 갈리는 자리다.

## 왜 중요한가

**디자이너와 개발자가 같은 파일을 볼 수 있다.** JSP 파일은 브라우저로 열면 `<% %>` 가 그대로 보이거나 깨지지만, Thymeleaf 파일은 **정적 화면으로 열린다** — 필기가 「웹 디자이너가 데이터를 삽입하지 않아도 전체적인 레이아웃을 확인할 수 있다」로 적은 것이 그것이다 → [[template-engine]]

**그리고 표현식이 문법으로 갈려 있다.** EL 은 `${...}` 하나로 값·URL·메시지를 전부 다루지만, Thymeleaf 는 **기호로 종류를 구분**한다 — `@{/board/list}` 를 보면 그것이 URL 이라는 것이 읽는 즉시 보이고, 컨텍스트 경로 처리도 엔진이 맡는다 → [[expression-language]] · [[jstl-core-tag]]

## 경계와 오해

- **`th:text` 는 태그의 「본문을 대체」한다** — 원래 있던 글자는 개발용 자리표시자이고 실행 시에는 사라진다. **그 자리에 진짜 문구를 넣어 두면 화면에서 없어진다**
- **`th:text` 는 이스케이프한다** — HTML 을 그대로 넣으려면 `th:utext` 를 써야 한다. **기본이 안전한 쪽**이라는 설계가 `c:out` 과 같다 → [[output-escaping]]
- **엘비스 연산자는 `null` 만 보는 것이 아니다** — 필기가 「`null` 또는 `false` 일 경우」라 적었는데, 정확히는 **`null` 이거나 비어 있을 때**다(빈 문자열 포함). `false` 를 그대로 쓰면 기본값이 나오는지 헷갈릴 수 있는 자리다
- **`*{...}` 는 `th:object` 가 있어야 한다** — 선택 변수 표현식은 「지금 다루는 객체」를 전제하므로, 폼 태그에 대상을 정해 두지 않으면 못 쓴다
- **표현 언어는 SpringEL 이다** — `${...}` 안의 문법이 JSP 의 EL 이 아니라 스프링 표현 언어라, 메서드 호출 같은 것이 더 된다. **문법이 비슷해 같은 것으로 착각하기 쉽다** → [[ognl]]
- **정적으로 열린다는 것이 「그대로 배포해도 된다」는 뜻은 아니다** — 반복(`th:each`)은 정적 화면에서 한 줄만 보이므로, 목록의 실제 모양은 서버를 거쳐야 안다

## 함께 보는 개념

- [[template-engine]] — 이 도구가 속한 갈래
- [[jsp]] — 대체 대상이 되는 앞 세대
- [[expression-language]] · [[jstl-core-tag]] — 문법을 비교할 짝
- [[spring-model]] — `${...}` 가 읽는 곳
- [[view-resolver]] — 이 템플릿을 고르는 자리
- [[output-escaping]] — `th:text` 가 기본으로 하는 일
- [[spring-boot]] — 스타터로 이 엔진을 가져오는 환경

## 출처

- [[2024-10-22-Day99]] — 「Thymeleaf」 절이 **왜 이 엔진이 다른지**를 두 줄로 짚었다: 「기본 형식이 `.html` 이기 때문에 별도의 엔진 없이도 웹에서 실행할 수 있다 / 웹 디자이너가 데이터를 삽입하지 않아도 전체적인 레이아웃을 확인할 수 있다」. 문법 쪽은 **표현식 네 종류(`${}`·`#{}`·`@{}`·`*{}`)를 각각 예제와 함께** 정리한 것이 핵심이고, 리터럴 다섯 갈래·문자열 결합과 `|...|` 리터럴 대체·삼항과 엘비스 연산자·`th:each`·`th:if`/`th:unless` 까지 이어진다. 각 항목이 「기본 텍스트가 보이고 값이 있으면 대체된다」는 예시로 설명돼, 내추럴 템플릿의 성질이 문법 설명 안에 녹아 있다. 다만 `th:text` 와 `th:utext` 의 이스케이프 차이, `*{...}` 가 `th:object` 를 전제한다는 것, 표현 언어가 SpringEL 이라는 것은 다루지 않았다
