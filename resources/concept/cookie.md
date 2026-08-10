---
type: concept
id: cookie
title: 쿠키 (HTTP Cookie)
aliases:
  - Cookie
  - 쿠키
  - HTTP 쿠키
  - 브라우저 쿠키
up:
  - 2024-09-06-Day71
  - 2024-10-16-Day94
tags:
  - web
  - http
  - 상태관리
---

# 쿠키 (HTTP Cookie)

서버가 `Set-Cookie` 응답 헤더로 브라우저에 **이름·값과 전송 조건**을 맡기고, 브라우저가 조건에 맞는 다음 요청의 `Cookie` 헤더로 돌려보내는 작은 상태 조각. 서버는 값을 보관하지 않아도 되지만, 받은 값은 클라이언트가 통제한다 → [[request-response]].

## 정의

왕복은 두 단계다.

1. 서버가 `response.addCookie(cookie)` 를 호출하면 컨테이너가 `Set-Cookie` 헤더를 만든다.
2. 브라우저는 `Domain`·`Path`·`Secure`·만료 조건이 맞는 요청에만 `Cookie: name=value` 를 붙인다. 서버는 `request.getCookies()` 배열에서 찾아 읽는다.

`Cookie` 객체 하나에는 값만 있는 것이 아니다. **어디에, 언제까지 보낼지**도 함께 있다.

| 속성 | 정하는 것 | Day71 예 |
|---|---|---|
| 이름·값 | 브라우저가 보관하고 다시 보낼 짝 | `new Cookie("name", "hong")` |
| `Max-Age` | 보관 기간 | `setMaxAge(30)` |
| `Path` | 같은 호스트에서 보낼 URL 경로의 접두어 | `setPath("/ex10/a")` |
| `Domain` | 보낼 호스트 범위 | 원문에는 없음 |
| `Secure`·`HttpOnly`·`SameSite` | HTTPS 전용 여부·스크립트 접근·교차 사이트 전송 | 원문에는 없음 |

`Max-Age` 를 주지 않은 쿠키는 **세션 쿠키**라 브라우저가 실행 중인 동안만 보관한다. 양수는 그 초 뒤 만료, `0`은 즉시 삭제를 지시한다. 같은 이름이라도 `Path`가 다르면 별개의 쿠키가 공존할 수 있다.

## 사용 예시

Day71 의 기간과 경로 설정을 한 흐름으로 놓으면 이렇다.

```java
Cookie theme = new Cookie("theme", "dark");
theme.setMaxAge(60 * 60 * 24 * 30); // 30일
theme.setPath("/");                // 같은 호스트의 모든 경로(앱 경계·접근 제어가 아님)
theme.setHttpOnly(true);            // JavaScript가 읽지 못하게
theme.setSecure(true);              // HTTPS 요청에만
response.addCookie(theme);          // Set-Cookie 응답 헤더

Cookie[] cookies = request.getCookies(); // Cookie 요청 헤더를 배열로 읽는다
if (cookies != null) {
  for (Cookie cookie : cookies) {
    if ("theme".equals(cookie.getName())) {
      String themeValue = cookie.getValue();
    }
  }
}
```

원문의 한글 값처럼 허용 범위를 넘는 값을 문자로 실어야 하면, **어떤 인코딩으로 넣었는지 아는 쪽에서만** 되돌린다.

```java
String encoded = URLEncoder.encode("홍길동", StandardCharsets.UTF_8);
Cookie name = new Cookie("name", encoded);
response.addCookie(name);

// 이 키가 URL-인코딩됐다는 약속이 있을 때만 한다.
String decoded = URLDecoder.decode(name.getValue(), StandardCharsets.UTF_8);
```

`URLEncoder` 는 폼·쿼리 문자열용 인코딩이라 공백을 `+`로 바꾼다. 쿠키 값을 설계할 때는 값의 형식과 인코딩을 명시하고, 임의의 모든 쿠키에 `URLDecoder`를 적용하지 않는다 → [[url]] · [[character-encoding]].

## 왜 중요한가

HTTP 요청은 각각 독립적이라 브라우저가 **어제와 같은 클라이언트임을 증명할 실마리**가 필요하다. [[http-session]] 은 그 답으로 세션 ID를 쿠키에 싣고, 서버는 그 ID로 자기 메모리의 사용자별 보관소를 다시 찾는다. 따라서 로그인 상태를 브라우저에 통째로 넣지 않고도 다음 요청에서 같은 서버 쪽 세션을 찾을 수 있다.

경로·만료를 명시하지 않으면 동작 범위가 우연히 결정된다. Day71 의 `/ex10/s1` 응답에서 계산되는 기본 `Path` 값은 **`/ex10`**이고, 그 결과 `/ex10/...` 요청과 path-match한다. 원문의 `/ex10/*`는 이 전송 결과를 간단히 적은 표기이지 쿠키 속성에 저장되는 경로 값은 아니다. `Path`를 `/`로 넓히면 편하지만, 의도하지 않은 화면에도 같은 값이 전송된다. **값의 수명과 보내는 범위가 곧 노출 범위**다.

## 경계와 오해

- **쿠키 ≠ 세션** — 쿠키는 브라우저가 보관해 보내는 전송 수단이고, `HttpSession`은 서버가 세션 ID를 열쇠로 찾아 주는 보관소다. 세션 ID가 쿠키에 든다는 사실 때문에 둘을 같은 것으로 읽기 쉽다. 쿠키를 지우면 보통 세션을 다시 찾지 못하지만, 서버 쪽 세션 객체가 즉시 사라지는 것은 아니다 → [[http-session]].
- **쿠키 값 ≠ 신뢰할 수 있는 사용자 정보** — 브라우저 소유자는 값·만료·이름을 바꿔 보내거나 아예 만들 수 있다. `role=admin` 같은 권한을 그대로 믿으면 요청 하나로 권한이 바뀐다. 서버가 서명해 검증하거나, 쿠키에는 추측하기 어려운 세션 ID만 두고 권한은 서버에서 찾는다.
- **`Path` ≠ 접근 제어** — `Path="/admin"`은 브라우저가 그 경로에 보낼지를 고르는 규칙일 뿐, 서버의 `/admin` URL을 막지 않는다. 주소를 직접 요청한 사용자를 막는 일은 인증·인가 코드의 몫이다. 보낼 범위와 접근 권한이 모두 URL로 보이므로 섞기 쉽다 → [[servlet-filter]].
- **세션 쿠키 ≠ 반드시 브라우저 종료와 동시에 사라지는 보안 경계** — `Max-Age`가 없다는 것은 영속 저장 지시가 없다는 뜻이다. 브라우저의 세션 복원·정책은 다를 수 있으므로, 민감한 서버 상태의 만료는 `HttpSession` 쪽에서도 정해야 한다.
- **원문의 `new Cookie("name2", "홍길동")`은 일반적인 HTTP 쿠키 값으로 안전하지 않다** — 현대 쿠키 처리기는 허용 문자 밖의 값을 응답에 넣을 때 거부할 수 있다. 원문 주석의 「ISO-8859-1이면 된다」도 충분한 규칙이 아니다. 쿠키 헤더는 임의 Unicode 문자열을 직접 싣는 형식이 아니며, UTF-8 바이트를 URL 인코딩 같은 ASCII 표현으로 바꾸고 **그 키만** 되돌리는 방식이 필요하다. 이 줄을 `response.addCookie(c4)`까지 실행하면 컨테이너 설정에 따라 그 응답 전체가 실패할 수 있다.
- **주석의 조건과 코드의 실행 범위가 다르다** — Day71 은 「값이 URL 인코딩한 값이라면」만 개발자가 디코딩한다고 썼지만, 실제 반복문은 모든 `c.getValue()`에 `URLDecoder.decode(...)`를 호출한다. 일반 값에 `%`가 불완전하게 들어 있으면 `IllegalArgumentException`으로 응답이 끊기고, `+`는 공백으로 바뀐다. 키별 형식을 알고 그 경우에만 디코딩해야 한다.
- **`request.getSesssion()`은 호출할 수 없다** — 마지막 「세션 생성」 설명의 철자가 `s` 하나 더 들어갔다. 이 문장을 코드로 옮기면 메서드를 찾지 못해 컴파일이 멈춘다. 실제 API는 `request.getSession()`이다 → [[http-session]].
- **`getCookies()`가 빈 배열을 준다고 가정하면 안 된다** — 쿠키 헤더가 없으면 `null`이다. Day71 의 `if (cookies != null)` 검사는 맞다. 다만 같은 이름의 쿠키가 여러 경로에서 와도 한 개라고 가정하지 말고, 서버가 기대하는 범위와 키를 명확히 해야 한다.
- **쿠키가 보인다고 JavaScript도 읽을 수 있는 것은 아니다** — `HttpOnly`를 붙이면 스크립트의 `document.cookie`에서 숨기지만 HTTP 요청에는 여전히 실린다. `Secure`는 HTTPS 전송만, `SameSite`는 교차 사이트 전송을 좁힌다. 셋은 서로 대체하지 않으며 원문 코드에는 모두 없다.

## 함께 보는 개념

- [[handler-method-argument]] — `@CookieValue` 로 받는 자리

- [[http-session]] — 쿠키의 세션 ID로 서버 쪽 상태를 다시 찾는 자리
- [[request-response]] — `Set-Cookie`와 `Cookie` 헤더가 오가는 요청·응답
- [[url]] · [[character-encoding]] — 값의 ASCII 표현과 되돌릴 문자집합
- [[servlet-filter]] — 쿠키가 왔다는 사실과 접근 권한을 가르는 자리
- [[web-application-deployment]] — 경로가 실제 배치 컨텍스트와 만나는 자리

## 출처

- [[2024-10-16-Day94]] — 여섯 주 뒤. **꺼내는 코드가 선언이 된다** — 쿠키 배열을 순회하며 이름을 비교하던 것이 `@CookieValue(value="age", defaultValue="0") int age` 한 줄이고, `String → int` 변환까지 해 준다. 보내는 쪽은 여전히 `response.addCookie(new Cookie(...))` 이고, 같은 노트가 **「쿠키의 값이 ASCII 가 아니라면 URL 인코딩 해야만 데이터가 깨지지 않는다. 하지 않으면 `?` 문자로 변환된다」**를 인코딩한 것과 안 한 것을 나란히 보내는 코드로 확인한다 → [[handler-method-argument]] · [[character-encoding]]
- [[2024-09-06-Day71]] — 「Cookie」 절이 응답 헤더로 보낸 값을 브라우저가 지정 URL의 요청 헤더에 다시 싣는 흐름, `response.addCookie`·`request.getCookies()` 코드, 세션 쿠키와 `setMaxAge`, 기본 경로와 `setPath`의 세 예를 적었다. 한글 쿠키 값에는 URL 인코딩을 쓰고 받는 쪽에서 직접 디코딩해야 한다는 주석도 있다. 다만 `new Cookie("name2", "홍길동")`을 이어서 보내는 코드는 현대 쿠키 값 제약을 깨고, 반복문은 모든 값을 무조건 디코딩하며, 마지막 `getSesssion()`은 오타라 호출할 수 없다. 쿠키 값의 신뢰성·`HttpOnly`·`Secure`·`SameSite`와 쿠키와 서버 세션의 구별도 다루지 않았다.
