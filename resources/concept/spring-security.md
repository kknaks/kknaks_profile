---
type: concept
id: spring-security
title: Spring Security (인증과 인가)
aliases:
  - Spring Security
  - SecurityFilterChain
  - SecurityContext
  - 인증
  - 인가
  - authentication
  - authorization
up:
  - 2025-01-10-Day09
tags:
  - spring
  - 보안
  - web
---

# Spring Security (인증과 인가)

**모든 요청 앞에 필터를 세워 「누구인가」와 「할 수 있는가」를 검사하는 프레임워크.** 두 물음이 다르다는 것이 이 층의 출발점이다.

## 정의

| | 묻는 것 | 예 |
|---|---|---|
| **인증**(authentication) | **누구인가** | 토큰이 유효한가, 비밀번호가 맞는가 |
| **인가**(authorization) | **이것을 해도 되는가** | 이 글을 지울 권한이 있는가 |

**인증이 먼저이고 인가가 뒤**다 — 누구인지 모르면 권한을 따질 수 없다.

### 필터체인으로 규칙을 적는다

```java
@Bean
SecurityFilterChain apiFilterChain(HttpSecurity http) throws Exception {
  http
    .securityMatcher("/api/**")                      // 이 체인이 맡을 범위
    .authorizeHttpRequests(auth -> auth
      .requestMatchers(HttpMethod.GET,  "/api/*/articles").permitAll()
      .requestMatchers(HttpMethod.POST, "/api/*/members/login").permitAll()
      .anyRequest().authenticated())                 // 나머지는 인증 필요
    .csrf(csrf -> csrf.disable())
    .httpBasic(basic -> basic.disable())
    .formLogin(form -> form.disable())
    .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
  return http.build();
}
```

**끄는 것이 켜는 것만큼 많다** — 폼 로그인·HTTP Basic·CSRF·세션을 전부 끈다. API 서버는 **브라우저 폼이 아니라 토큰으로 인증**하기 때문이다 → [[jwt]] · [[rest-api]]

### 인증 결과를 어디에 두나

```java
SecurityUser securityUser = memberService.getUserFromAccessToken(accessToken);
SecurityContextHolder.getContext().setAuthentication(securityUser.genAuthentication());
```

`SecurityContext` 에 심어 두면 **그 요청을 처리하는 동안 어디서나 꺼내 쓸 수 있다** — 쓰레드에 매인 저장소라 요청마다 격리된다 → [[thread-local]]

## 왜 중요한가

**보안 검사가 업무 코드에서 빠진다.** 컨트롤러마다 「로그인했나」를 확인하던 것을 필터가 대신하므로, **핸들러는 이미 인증된 요청만 받는다** → [[servlet-filter]] · [[handler-interceptor]]

**그리고 규칙이 한 곳에 모인다.** 어떤 경로가 열려 있고 어떤 것이 막혀 있는지가 설정 클래스 하나에 있어, **빠뜨린 곳을 눈으로 찾을 수 있다** — 「모든 요청에 대해」를 코드로 보증하는 [[front-controller]] 의 논리와 같다.

## 경계와 오해

- **필터는 스프링 MVC 보다 바깥이다** — `DispatcherServlet` 에 닿기 전에 걸리므로, 여기서 막힌 요청은 **컨트롤러도 인터셉터도 예외 처리도 못 본다.** 401/403 응답 모양이 애플리케이션의 것과 달라지는 이유다 → [[exception-handler]]
- **`permitAll()` 은 「검사 안 함」이지 「인증 없음」이 아니다** — 토큰이 있으면 여전히 읽히고 컨텍스트에 심긴다. **없어도 통과시킬 뿐**이다
- **`csrf.disable()` 은 조건부로만 안전하다** — 토큰을 **쿠키**에 담으면 브라우저가 자동으로 붙여 보내므로 CSRF 의 표적이 그대로 남는다. 「무상태니까 CSRF 는 무관하다」는 **헤더로 토큰을 보낼 때의 이야기**다 → [[cookie]]
- **경로 패턴의 순서가 규칙이다** — 위에서부터 처음 맞는 것이 적용되므로, `anyRequest()` 를 위에 두면 아래가 죽는다
- **`securityMatcher` 로 체인을 나눌 수 있다** — API 용과 화면용 규칙이 다를 때 체인을 둘 두는 구성이고, 필기가 `/api/**` 에만 거는 것이 그것이다. **어느 체인이 잡았는지**가 디버깅의 첫 질문이 된다
- **인증과 인가를 한 낱말로 부르면 헷갈린다** — 한국어로 둘 다 「권한」처럼 읽히지만, **401(누구인지 모름)과 403(권한 없음)** 은 다른 답이다 → [[http-message]]

## 함께 보는 개념

- [[jwt]] — 이 층이 검사하는 자격 증명
- [[servlet-filter]] — 필터체인이 얹혀 있는 장치
- [[thread-local]] — `SecurityContext` 가 요청별로 격리되는 원리
- [[http-session]] — 끄기로 선택한 반대편 방식
- [[handler-interceptor]] — 한 겹 안쪽의 공통 처리
- [[rest-api]] — 무상태 정책이 맞아떨어지는 배치

## 출처

- [[2025-01-10-Day09]] — 「apiFilter 생성하기」 절이 `SecurityFilterChain` 빈 하나로 **범위·허용 규칙·끌 것들**을 적는 모양을 보인다 — `securityMatcher("/api/**")` 로 범위를 좁히고, GET 조회와 로그인만 `permitAll()` 하고 나머지는 `authenticated()`, 그리고 CSRF·HTTP Basic·폼 로그인·세션을 차례로 끈다. **「기본적으로 securityConfig 는 모든 url 에 대해 허용했기 때문에 api 로 들어오는 요청은 필터링이 필요하다」**는 한 줄이 이 체인을 왜 따로 두는지 설명한다. 「토큰을 활용하여 인가처리하기」 절이 흐름을 두 단계로 적었다 — 필터가 쿠키에서 토큰을 꺼내 검증하고, 유효하면 `SecurityContextHolder.getContext().setAuthentication(...)` 으로 심는다. 유효하지 않으면 리프레시 토큰으로 재발급하는 분기까지 있다 → [[jwt]]
