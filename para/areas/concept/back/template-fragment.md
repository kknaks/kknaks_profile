---
type: concept
id: template-fragment
title: 템플릿 조각 (Fragment)
aliases:
  - fragment
  - 조각
  - "th:fragment"
  - "th:replace"
  - 레이아웃 재사용
up:
  - 2024-10-23-Day100
tags:
  - web
  - 템플릿
  - 재사용
---

# 템플릿 조각 (Fragment)

**여러 화면이 함께 쓰는 부분을 한 파일에 두고 이름으로 끼워 넣는 것.** 머리말·꼬리말·메뉴처럼 모든 페이지에 같은 것이 들어가는 자리를 한 곳으로 모은다.

## 정의

**정의하는 쪽**이 이름을 붙이고,

```html
<head data-th-fragment="head">
  <meta charset='UTF-8'>
  <title>Title</title>
  <link href='/css/common.css' rel='stylesheet'>
</head>
```

**쓰는 쪽**이 그 이름으로 부른다.

```html
<head data-th-replace="~{header :: head}"> </head>
```

참조 문법이 세 조각이다.

| 조각 | 뜻 |
|---|---|
| `~` | 템플릿 경로의 **루트** |
| `header` | 파일 이름 (`header.html`) |
| `head` | 그 파일 안에서 `th:fragment` 로 붙인 **조각 이름** |

**`data-th-*` 는 `th:*` 와 같다** — HTML5 의 사용자 정의 속성 규칙(`data-`)을 따르는 표기라, 유효성 검사를 통과하고 편집기도 오류로 보지 않는다 → [[thymeleaf]]

## 왜 중요한가

**「같은 것을 여러 곳에서 쓴다」를 화면 쪽에서 푸는 방법이 이것이다.** 이 레포의 노트들이 같은 문제를 여러 번 만났다.

| 방식 | 시점 | 성격 |
|---|---|---|
| `<%@ include %>` | 번역 | 소스를 붙여 넣는다 → [[jsp-directive]] |
| `<jsp:include>` · `RequestDispatcher.include()` | 실행 | 다른 서블릿/JSP 를 **실행해** 결과를 끼운다 → [[request-dispatcher]] |
| `<c:import>` | 실행 | 외부 URL 까지 가져온다 → [[jstl-core-tag]] |
| `th:replace` | 렌더링 | **같은 엔진 안에서 조각을 찾아 바꿔 넣는다** |

앞의 셋이 **다른 자원을 부르는 것**인 반면, 조각은 **템플릿 하나의 일부를 이름으로 가리키는 것**이다 — 서블릿 호출도 HTTP 요청도 없다.

**그리고 정적으로 열어도 화면이 유지된다.** 조각을 쓰는 쪽의 `<head>` 안에 임시 내용을 넣어 두면 브라우저로 열었을 때 그것이 보이고, 서버를 거치면 진짜 조각으로 바뀐다 → [[thymeleaf]]

## 경계와 오해

- **`replace` 와 `insert` 는 다르다** — `replace` 는 **그 태그 자체를 조각으로 바꾸고**, `insert` 는 태그를 남긴 채 **안에 넣는다.** 필기의 예처럼 `<head data-th-replace=...>` 를 쓰면 바깥 `<head>` 는 사라지고 조각의 `<head>` 가 남으므로 **태그가 중첩되지 않는다** — 여기서 `insert` 를 쓰면 `<head>` 안에 `<head>` 가 생긴다
- **조각 이름은 파일 안에서만 통한다** — 참조가 `파일 :: 조각` 두 부분인 이유다. 파일을 옮기면 그 이름으로 찾던 곳이 전부 깨진다 → [[coupling]]
- **조각도 결국 이름 계약이다** — `~{header :: head}` 는 문자열이라 컴파일러가 검사하지 않는다. 오타는 렌더링 시점에 드러난다
- **재사용의 단위를 정해야 한다** — 머리말 전체를 한 조각으로 두면 페이지마다 다른 `<title>` 을 못 넣는다. 조각에 **매개변수를 넘기는 문법**이 따로 있고, 그것을 안 쓰면 조각이 늘어난다
- **[[jsp]] 의 include 와 비용이 다르다** — 서블릿을 실행하는 것이 아니라 템플릿 트리에서 가져오는 것이라 왕복이 없다. 「같은 include 인데 왜 성능 이야기가 다르냐」의 답이 이것이다

## 함께 보는 개념

- [[thymeleaf]] — 이 문법이 속한 엔진
- [[template-engine]] — 재사용이 이 갈래의 값 중 하나인 이유
- [[request-dispatcher]] · [[jsp-directive]] · [[jstl-core-tag]] — 같은 문제의 앞선 답들
- [[cohesion]] — 공통 부분을 한 곳으로 모으는 축
- [[view-resolver]] — 조각 파일을 찾는 경로의 근거

## 출처

- [[2024-10-23-Day100]] — 「header.html 수정」 절이 **정의하는 쪽과 쓰는 쪽을 한 코드 블록에 나란히** 놓고, 참조 문법 `~{header :: head}` 의 세 부분을 **주석으로 각각 풀어 적었다**(`~` 는 템플릿 경로의 루트 · `header` 는 파일명 · `head` 는 조각명) — 이 주석이 이 개념에서 가장 값진 부분이다. 「헤더 값은 모든 템플릿에서 공통으로 참조하는 값이므로 조각을 만들어서 적용한다」로 이유도 한 줄 적혔다. 같은 노트가 `data-th-*` 표기를 쓰는 것도 눈에 띄고(앞 회차는 `th:*`), 「Project.view 수정」 절은 `data-th-checked="${project.members.contains(user)}"` 로 **이미 선택된 항목을 표시하는** 실전 예를 남겼다. 다만 `replace` 와 `insert` 의 차이, 조각에 값을 넘기는 방법은 다루지 않았다
