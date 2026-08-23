---
type: concept
id: web-xml
title: web.xml (배포 설명자)
aliases:
  - web.xml
  - 배포 설명자
  - deployment descriptor
  - WebServlet
up:
  - 2024-09-02-Day68
  - 2024-10-14-Day92
tags:
  - web
  - servlet
  - 설정
---

# web.xml (배포 설명자)

**어떤 클래스를 어떤 URL 로 부를지 적어 두는 설정 파일.** `WEB-INF` 안에 있고, 컨테이너가 애플리케이션을 띄울 때 이것을 읽는다 → [[web-application-deployment]]

## 정의

등록과 매핑이 **두 단계**다. 별명을 붙이고, 그 별명에 URL 을 잇는다.

```xml
<servlet>
    <servlet-name>s01</servlet-name>                        <!-- 별명 -->
    <servlet-class>com.eomcs.web.ex01.Servlet01</servlet-class>
</servlet>

<servlet-mapping>
    <servlet-name>s01</servlet-name>                        <!-- 그 별명에 -->
    <url-pattern>/ex01/first</url-pattern>                  <!-- URL 을 잇는다 -->
</servlet-mapping>
```

[[web-component]] 셋 모두 같은 형태다.

| 컴포넌트 | 등록 태그 | 매핑 태그 |
|---|---|---|
| 서블릿 | `<servlet>` | `<servlet-mapping>` |
| 필터 | `<filter>` | `<filter-mapping>` (`/ex02/*` 처럼 패턴) |
| 리스너 | `<listener>` | **없다** — 이벤트를 받는 것이라 URL 이 필요 없다 |

애노테이션으로 하면 두 단계가 한 줄로 접힌다.

```java
@WebServlet("/ex01/s2")                                     // 기본형
@WebServlet(value="/ex01/s2")                               // 같은 것
@WebServlet(urlPatterns="/ex01/s2")                         // 같은 것
@WebServlet(urlPatterns = {"/ex01/s2", "/ex01/ss2", "/ex01/sss2"})   // 여러 URL
```

**`value` 를 생략할 수 있는 것은 애노테이션의 일반 규칙**이다 — 프로퍼티가 하나면 이름을 안 쓴다 → [[annotation]]

## 왜 중요한가

**「별명 → URL」 두 단계가 애노테이션의 한 줄로 접힌 이유가 보인다.** XML 쪽은 클래스와 URL 을 **각각 다른 자리에** 적으므로 별명이 그 둘을 잇는 못이 필요했다. 애노테이션은 클래스 선언 옆에 붙으니 잇는 못이 필요 없다 — 대신 **URL 을 알려면 클래스를 열어야** 한다.

그래서 둘이 갈리는 것은 문법이 아니라 **어디를 보면 전체가 보이나**다.

| | XML | 애노테이션 |
|---|---|---|
| 전체 URL 목록 | **한 파일에서 다 보인다** | 클래스를 다 열어야 한다 |
| 클래스의 URL | 별명을 따라가야 한다 | **선언 옆에 있다** |
| 고칠 때 | 배포물의 XML 만 고치면 된다 | **다시 컴파일해야 한다** |

## 경계와 오해

- **`web.xml` 이 있어야 하는 것은 아니다** — 서블릿 3.0 부터 애노테이션만으로 된다. `metadata-complete="false"` 가 그 스위치인데, **`true` 로 두면 애노테이션을 무시하고 XML 만 읽는다.** 필기가 그 속성을 코드에 적어 두었지만 뜻은 설명하지 않았다 — 「XML 을 썼는데 `@WebServlet` 이 안 먹는다」의 원인이 여기다.
- **별명은 컨테이너 안에서만 쓰인다** — `s01` 은 URL 이 아니고 클라이언트가 볼 수 없다. 두 태그를 잇기 위한 이름이다.
- **필터의 URL 패턴은 서블릿과 뜻이 다르다** — 서블릿 매핑은 「이 URL 을 처리할 하나」를 고르고, 필터 매핑은 「이 패턴에 걸리는 요청 전부」에 끼어든다. `/ex02/*` 처럼 별표를 쓰는 것이 흔한 이유다 → [[servlet-filter]]
- **리스너에 매핑이 없는 것이 규칙의 예외처럼 보이지만 아니다** — 리스너는 요청이 아니라 **생명주기 이벤트**를 받는다. URL 로 불릴 일이 없으니 이을 것도 없다 → [[servlet-listener]]
- **XML 과 애노테이션을 같은 서블릿에 둘 다 쓰면 충돌한다** — 같은 URL 을 두 곳에서 주장하면 기동이 실패하거나 한쪽이 조용히 이긴다. 섞어 쓸 수는 있지만 **같은 것을 두 번 적지 않는다**가 기준이다.
- **`WEB-INF` 안이라 브라우저가 못 본다** — 설정 파일이 노출되면 클래스 이름과 구조가 그대로 새므로, 그 폴더가 공개되지 않는 것이 규격이다 → [[web-application-deployment]]

## 함께 보는 개념

- [[servlet-container-initializer]] — 이 파일을 자바 코드가 대신하는 방법

- [[servlet]] · [[servlet-filter]] · [[servlet-listener]] — 등록 대상 셋
- [[web-component]] — 그 셋을 묶는 이름
- [[annotation]] — `@WebServlet` 이 속한 문법
- [[servlet-container]] — 이 파일을 읽는 주체
- [[web-application-deployment]] — `WEB-INF` 의 위치와 뜻
- [[xml]] — 이 파일의 형식

## 출처

- [[2024-10-14-Day92]] — 여섯 주 뒤. **이 파일이 없어도 되는 이유가 나온다.** 서블릿 컨테이너가 시작할 때 `/WEB-INF/lib/*.jar` 의 `/META-INF/services/javax.servlet.ServletContainerInitializer` 를 읽어 구현체를 부르는 통로가 있고, 스프링이 거기에 자기를 올려 두었기 때문에 **`<servlet>`·`<servlet-mapping>`·`<listener>` 를 자바 클래스로 적을 수 있다.** Day68 이 「등록할 class 파일의 별명과 URL Path」로 정리했던 두 단계가 `getServletName()` 과 `getServletMappings()` 두 메서드가 되고, `<load-on-startup>` 은 `registration.setLoadOnStartup(1)` 이 된다 — **결정은 그대로이고 적는 곳만 바뀐다** → [[servlet-container-initializer]]
- [[2024-09-02-Day68]] — 「Servlet 등록하기」 절이 두 방법을 갈라 놓는다. `web.xml` 을 「서블릿의 배포 설명자(deployment descriptor) 파일」로 정의하고 `WEB-INF` 안에 있다는 것, **「등록할 class 파일의 별명과 패키지명을 등록하고, 해당 별명에 대한 URL Path 를 설정한다」로 두 단계 구조를 정확히 적었다.** 리스너·서블릿·필터 셋의 태그가 다 들어 있는 전문이 실려 있고, `@WebServlet` 쪽은 `value`·`urlPatterns`·기본형·배열까지 네 표기를 나란히 보였다. 다만 `metadata-complete` 의 뜻, 둘을 섞을 때의 충돌, 리스너에 매핑이 없는 이유는 다루지 않았다
