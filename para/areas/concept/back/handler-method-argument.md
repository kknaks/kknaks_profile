---
type: concept
id: handler-method-argument
title: 요청 핸들러의 아규먼트
aliases:
  - 요청 핸들러
  - request handler
  - 핸들러 아규먼트
  - "@RequestHeader"
  - "@CookieValue"
  - "@InitBinder"
  - WebDataBinder
up:
  - 2024-10-16-Day94
  - 2025-01-03-Day04_1
tags:
  - spring
  - web
  - mvc
---

# 요청 핸들러의 아규먼트

**컨트롤러 메서드의 매개변수는 우리가 채우지 않는다 — 프론트 컨트롤러가 타입과 표식을 보고 채워 준다.** 그래서 「무엇을 선언할 수 있는가」가 곧 「무엇을 쓸 수 있는가」다.

## 정의

### 표식 없이 타입만으로 들어오는 것

```java
public void handler1(
    ServletRequest request, ServletResponse response,
    HttpServletRequest request2, HttpServletResponse response2,
    HttpSession session,
    Map<String, Object> map,   // 뷰에 넘길 값을 담는 자리
    Model model,               // Map 과 같다 — 둘 중 하나만 받으면 된다
    PrintWriter out            // 응답 출력 스트림
) { }
```

**`ServletContext` 는 예외다** — 매개변수로 못 받고 `@Autowired` 로 주입받아야 한다. 요청마다 달라지는 것이 아니기 때문이다 → [[servlet-context]] · [[autowired]]

### 요청 파라미터 — `@RequestParam`

```java
@RequestParam(value = "name") String name1,
@RequestParam(name  = "name") String name2,   // value 와 name 은 같다
@RequestParam("name")         String name3,   // 속성 이름 생략
String name                                   // 애노테이션 자체 생략 — 이름이 같으면 된다
```

**붙이느냐 마느냐가 필수 여부를 가른다.**

| 선언 | 값이 없으면 |
|---|---|
| `@RequestParam("x") String x` | **예외** (필수) |
| `String x` | `null` (선택) |
| `@RequestParam(value="x", required=false)` | `null` |
| `@RequestParam(value="x", defaultValue="ohora")` | `"ohora"` |

### 도메인 객체로 한 번에 받기

```java
public String handler1(String model, String maker, int capacity, boolean auto, Car car) { ... }
```

값 객체를 선언하면 **인스턴스를 만들어 이름이 같은 프로퍼티에 채워 준다.** 객체 안에 객체가 있으면 `내부객체.프로퍼티명` 으로 지정한다 → [[ognl]]

형변환도 해 준다 — `"100"` → `int`, `"true"`/`"TRUE"`/`"1"` → `boolean`. **못 바꾸면 예외**이고, `boolean` 은 `0`/`1` 외의 숫자에서 터진다 → [[type-casting]]

### 헤더와 쿠키

```java
@RequestHeader("Accept")     String accept,
@RequestHeader("User-Agent") String userAgent,
@CookieValue(value = "age", defaultValue = "0") int age
```

`required`·`defaultValue` 가 `@RequestParam` 과 똑같이 동작한다 → [[http-message]] · [[cookie]]

### 변환기를 끼우기 — `@InitBinder`

기본 변환기가 없는 타입은 등록해야 한다.

```java
@InitBinder
public void initBinder(WebDataBinder binder) {
  binder.registerCustomEditor(java.util.Date.class, new DatePropertyEditor());
  binder.registerCustomEditor(Car.class, new CarPropertyEditor());
}
```

**핸들러를 부르기 전에 매번 불린다** — 아규먼트를 만들기 전에 변환기가 준비돼야 하기 때문이다. 모든 컨트롤러에 적용하려면 `@ControllerAdvice` 클래스로 뺀다 → [[property-editor]]

## 왜 중요한가

**컨트롤러가 서블릿 API 를 안 봐도 되게 만드는 것이 이 규칙의 목적이다.** `request.getParameter("name")` → `String name`, `request.getHeader("Accept")` → `@RequestHeader`, 쿠키 배열 순회 → `@CookieValue`. **꺼내는 코드가 선언으로 바뀐다** → [[request-parameter]]

그 결과 **메서드 시그니처가 곧 그 요청의 명세**가 된다 — 무엇을 받고 무엇이 필수인지가 한 줄에 있다.

## 경계와 오해

- **애노테이션을 안 붙이면 선택 항목이 된다** — 필기가 정확히 짚은 자리다. 「이름이 같으면 생략해도 된다」와 「생략하면 값이 없어도 넘어간다」가 **같은 생략의 두 얼굴**이라, 필수인 파라미터에 애노테이션을 빼면 오류가 `null` 로 미뤄진다
- **`Map` 과 `Model` 을 둘 다 받을 이유는 없다** — 같은 것을 가리킨다 → [[spring-model]]
- **도메인 객체 바인딩은 이름이 맞는 것만 채운다** — 안 맞는 필드는 조용히 `null` 이고, 반대로 **클라이언트가 보내면 안 되는 필드까지 채워질 수 있다.** 등록 폼에서 `role` 같은 필드가 함께 채워지는 사고가 여기서 난다
- **`@InitBinder` 는 요청마다 실행된다** — 캐시되지 않으므로 무거운 일을 넣으면 안 된다. 필기가 「request handler 의 아규먼트 개수만큼」이라 적었는데 정확히는 **핸들러 호출 전에 한 번**이다
- **매개변수 이름 생략은 컴파일 옵션에 기댄다** — `.class` 에 이름이 남지 않으면 `@RequestParam` 없이는 못 찾는다 → [[bytecode]]
- **쿠키 값이 ASCII 가 아니면 URL 인코딩해야 한다** — 안 하면 `?` 로 바뀐다. 이것은 스프링이 아니라 쿠키 명세의 제약이다 → [[cookie]] · [[character-encoding]]

## 함께 보는 개념

- [[request-mapping]] — 어느 핸들러가 불릴지의 규칙
- [[response-body]] — 반대편(리턴값)의 규칙
- [[request-parameter]] — 이 표식들이 감싸는 서블릿 API
- [[property-editor]] — 문자열을 타입으로 바꾸는 장치
- [[spring-model]] — 뷰에 값을 넘기는 아규먼트
- [[cookie]] · [[http-message]] — 헤더·쿠키를 받는 자리
- [[ognl]] — 중첩 객체의 프로퍼티를 가리키는 표기
- [[dto]] — `@RequestBody` 로 받는 그릇

## 출처

- [[2025-01-03-Day04_1]] — 두 달 뒤. **REST 로 오면서 아규먼트 두 개가 더 쓰인다** — 경로의 일부를 받는 `@PathVariable("id")` 와 **본문 JSON 을 객체로 받는 `@RequestBody`** 다. 앞 회차의 `@RequestParam` 이 쿼리스트링·폼을 받았다면 이쪽은 **본문 전체를 객체 하나로** 매핑하는 것이라, 「이름이 같은 프로퍼티에 채운다」는 규칙이 JSON 필드로 옮겨 간다. 필기가 부딪힌 기본 생성자 문제도 그 과정에서 나온다 → [[dto]] · [[json]]
- [[2024-10-16-Day94]] — 「요청핸들러의 아규먼트」 절이 **받을 수 있는 타입 목록**(`ServletRequest`·`HttpSession`·`Map`·`Model`·`PrintWriter`)부터 시작해 `ServletContext` 만 예외라는 것까지 코드 주석으로 남겼다. `@RequestParam` 은 `value`/`name`/생략 세 표기와 **`required`·`defaultValue` 의 조합을 네 줄로 나란히** 보이고, 「애노테이션을 붙이면 필수 항목, 붙이지 않으면 선택 항목」이라는 대비를 주석에 적었다 — 이 회차에서 가장 실전적인 관찰이다. 도메인 객체 바인딩에서는 **`boolean` 변환 규칙(`1`→true, `0`→false, 그 외 숫자는 예외)**까지 적혀 있고, `@InitBinder` + `WebDataBinder.registerCustomEditor` 로 `Date` 와 `Car`(콤마 구분 문자열)를 변환하는 에디터 둘을 실제로 구현했다. `@ControllerAdvice` 로 그것을 전역화하는 절도 이어진다. `@RequestHeader` 로 `User-Agent` 를 받아 브라우저를 판별하는 예제, `@CookieValue` 로 쿠키를 받으며 **URL 인코딩이 필요한 이유**를 주석에 적은 예제가 함께 있다. 다만 `handler2` 의 `originBytes` 는 선언되지 않은 변수다
