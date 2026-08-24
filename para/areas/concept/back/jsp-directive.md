---
type: concept
id: jsp-directive
title: JSP 지시자 (Directive)
aliases:
  - 지시자
  - 디렉티브
  - directive
  - page 지시자
  - include 지시자
  - taglib
up:
  - 2024-09-10-Day73
  - 2024-09-11-Day74
tags:
  - web
  - jsp
---

# JSP 지시자 (Directive)

`<%@ ... %>` — **번역 시점**에 JSP 엔진에게 「이 파일을 어떻게 서블릿으로 만들지」를 지시하는 문법. 셋뿐이다: `page` · `include` · `taglib`.

## 정의

### `<%@ page %>` — 페이지 전역 설정

| 속성 | 정하는 것 |
|---|---|
| `language` | JSP 안에서 쓸 언어 (기본 `java`) |
| `contentType` | **응답**의 MIME 타입과 문자 인코딩 |
| `pageEncoding` | **이 JSP 파일 자체**의 인코딩 |
| `import` | 번역된 클래스가 임포트할 자바 클래스 |
| `trimDirectiveWhitespaces` | 지시자가 남기는 공백 제거 여부 |
| `buffer` | 응답을 모아 두는 버퍼 크기 (예: `8kb`) |
| `autoFlush` | 버퍼가 차면 자동으로 내보낼지 여부 |
| `errorPage` | 실행 중 오류가 났을 때 대신 실행할 JSP |

### `<%@ include %>` — 파일을 붙여 넣고 번역

지정한 파일의 **내용을 이 자리에 끼워 넣은 뒤** 하나의 서블릿 클래스를 만든다. 붙여 넣기이므로 대상은 **일반 텍스트 파일이면 되고 JSP 일 필요가 없다.**

### `<%@ taglib %>` — 확장 태그 가져오기

외부에 정의된 JSP 확장 태그를 이 페이지에서 쓸 수 있게 등록한다. JSP 명세에 표준으로 추가된 태그 묶음을 [[jstl]] 이라 부른다.

```jsp
<%@ taglib uri="태그 라이브러리 모듈명" prefix="접두어" %>
```

- `uri` — **어느 라이브러리인지 가리키는 이름.** 인터넷 주소처럼 생겼지만 접속하지 않는다
- `prefix` — 이 페이지에서 그 라이브러리를 부를 **접두어.** 선언한 뒤에는 `<접두어:태그명>` 으로 쓴다

**둘 중 이름을 정하는 것은 `uri` 뿐이고, `prefix` 는 이 파일 안에서만 통하는 별명이다.**

## 사용 예시

```jsp
<%@ page
    language="java"
    contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"
    import="java.util.List,java.util.Map,java.util.Set"
    trimDirectiveWhitespaces="true"
    buffer="8kb"
    autoFlush="false"
%>
```

```jsp
<%@ include file="./ex08_header.txt"%>
```

## 왜 중요한가

**지시자는 실행되지 않는다 — 번역을 바꾼다.** 그래서 값을 잘못 주면 코드가 아니라 *만들어지는 클래스* 가 달라지고, 증상이 실행 흐름과 떨어진 곳에서 나타난다.

`contentType` 과 `pageEncoding` 을 헷갈리면 그 자리가 바로 한글 깨짐이다. 하나는 **내보낼 것**(응답 헤더에 실릴 charset), 하나는 **읽어 들일 것**(이 소스 파일을 무슨 인코딩으로 해석할지)이다 → [[character-encoding]]

`autoFlush="false"` 는 버퍼가 차면 자동으로 보내지 않고 **예외를 던지겠다**는 뜻이다. 버퍼를 넘길 만큼 큰 응답에서 갑자기 터지는 이유가 여기 있다.

## 경계와 오해

- **`<%@ include %>` ≠ `<jsp:include>` ≠ `RequestDispatcher.include()`** — 필기가 「RequestDispatcher의 include()와 다르다」고만 적고 넘어간 자리다. 셋의 시점이 다르다.
  - `<%@ include %>` — **번역 시점.** 소스를 붙여 넣어 **한 개의** 서블릿이 된다. 대상은 텍스트 파일이면 된다
  - `<jsp:include>` — **실행 시점.** 다른 서블릿/JSP 를 실행하고 그 **결과**를 받아 온다 → [[jsp-action-tag]]
  - `RequestDispatcher.include()` — 자바 코드에서 같은 일을 하는 API → [[request-dispatcher]]
  
  붙여 넣기라서 `<%@ include %>` 대상 파일 안의 변수는 포함하는 쪽과 **같은 메서드에 살고**, 이름이 겹치면 컴파일 오류가 난다. 실행 시점 포함에서는 그런 일이 없다.
- **지시자는 페이지 어디에 써도 페이지 전체에 걸린다** — `<%@ page %>` 는 파일 맨 위에 쓰는 관습이 있을 뿐, 위치가 효력 범위를 정하지 않는다. [[jsp-scripting-element]] 의 선언 태그와 같은 성질이다
- **`import` 는 여러 번 써도 되고 쉼표로 이어 써도 된다** — 필기의 예시가 `import` 속성을 세 줄 겹쳐 썼다. `page` 지시자의 속성 중 **중복이 허용되는 것은 `import` 뿐**이고 나머지는 한 번만 쓸 수 있다
- **`errorPage` 는 오류를 없애지 않는다** — 대신 보여 줄 화면을 정할 뿐이고, 예외는 여전히 발생했다. 로그와 응답 화면을 분리하는 장치이지 [[exception-handling]] 을 대신하지 않는다
- **`taglib` 은 태그를 정의하지 않는다** — 이미 정의된 것을 **가져오는** 선언이다. 라이브러리 jar 가 없으면 선언만으로는 아무 일도 안 되고 번역 시점에 터진다 → [[jstl]]
- **`taglib` 은 페이지마다 다시 써야 한다** — 한 번 선언하면 애플리케이션 전체에 걸리는 설정이 아니다. `<%@ include %>` 로 붙여 넣는 머리말 파일에 선언을 두면 **붙여 넣어진 페이지에는 걸리지만** 실행 시점 포함(`<jsp:include>`)으로 가져온 페이지에는 안 걸린다 — 번역 시점과 실행 시점의 차이가 여기서도 갈린다

## 함께 보는 개념

- [[jsp]] — 지시자가 속한 기술
- [[jsp-scripting-element]] — 번역 결과의 「어느 자리」를 정하는 다른 갈래
- [[jsp-action-tag]] — 실행 시점에 작용하는 태그
- [[jstl]] — `taglib` 으로 가져오는 표준 라이브러리
- [[character-encoding]] — `contentType`·`pageEncoding` 이 갈리는 축
- [[request-dispatcher]] — 실행 시점 포함·위임의 자바 API
- [[template-engine]] — 번역을 수행하는 도구 갈래

## 출처

- [[2024-09-11-Day74]] — 하루 뒤. Day73 의 「Tablib」 절이 이름만 남기고 넘어간 자리를 「JSTL 태그 라이브러리 구조 및 사용」이 채운다 — `<%@ taglib uri="..." prefix="..."%>` 선언 문법과 두 속성의 역할(`uri` 는 참조 경로, `prefix` 는 페이지에서 쓸 접두어), 그리고 선언 이후의 `<접두어:태그명 속성="값">` 사용 문법이 나온다. 이 회차 전체가 그 선언으로 가져온 태그들을 다루므로, `taglib` 이 실제로 무엇을 여는 문인지가 여기서 드러난다 → [[jstl]]
- [[2024-09-10-Day73]] — 「Page(Directive element)」 절이 `language`·`contentType`·`pageEncoding`·`import`·`trimDirectiveWhitespaces`·`buffer`·`autoFlush` 를 한 줄씩 설명하고 전부 쓴 예시를 실었다. `buffer`·`autoFlush` 는 앞 회차(Day67)에 없던 항목이다. 「Include(Directive element)」가 **「일반 텍스트 파일이면 된다. JSP 파일일 필요가 없다」**고 적어 번역 시점 포함이라는 성질을 정확히 짚었고, 「RequestDispatcher의 include()와 다르다」로 구분해야 할 자리를 남겼다(무엇이 다른지는 적지 않았다). 「Tablib」 절은 JSTL 이라는 이름만 소개하고 넘어간다. `errorPage` 는 별도 절로 한 줄 나온다
