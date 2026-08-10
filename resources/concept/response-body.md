---
type: concept
id: response-body
title: 리턴값으로 응답 만들기 (@ResponseBody · ResponseEntity)
aliases:
  - "@ResponseBody"
  - HttpEntity
  - ResponseEntity
  - HttpHeaders
up:
  - 2024-10-16-Day94
tags:
  - spring
  - web
  - mvc
---

# 리턴값으로 응답 만들기 (@ResponseBody · ResponseEntity)

**컨트롤러 메서드가 돌려준 값이 「뷰 이름」인지 「응답 본문」인지를 가르는 규칙.** 기본은 뷰 이름이고, 표식이나 타입으로 그것을 뒤집는다.

## 정의

| 리턴 모양 | 무엇으로 해석되나 |
|---|---|
| `String` (표식 없음) | **뷰 이름** → [[view-resolver]] |
| `String` + `@ResponseBody` | **응답 본문 그 자체** |
| `HttpEntity<String>` | 본문 (+ 헤더). **표식이 필요 없다** — 타입으로 안다 |
| `ResponseEntity<String>` | 본문 + 헤더 + **상태 코드** |
| `ModelAndView` | 모델 + 뷰 이름 → [[spring-model]] |

### 콘텐트 타입을 정하는 자리

```java
@GetMapping(value = "h2", produces = "text/html;charset=UTF-8")
@ResponseBody
public String handler2() { return "<h1>abc가각간</h1>"; }
```

**`response.setContentType(...)` 을 메서드 안에서 불러 봐야 소용없다** — 필기가 코드로 확인한 자리다. 이미 스프링이 리턴값을 변환하는 경로에 들어와 있어서, **선언(`produces`)이나 헤더 객체로** 정해야 한다.

```java
HttpHeaders headers = new HttpHeaders();
headers.add("Content-Type", "text/html;charset=UTF-8");
headers.add("BIT-OK", "ohora");

return new ResponseEntity<>("<h1>abc가각간</h1>", headers, HttpStatus.OK);
```

## 왜 중요한가

**같은 컨트롤러 문법으로 화면과 데이터를 둘 다 낼 수 있다.** 표식 하나로 「HTML 을 그리는 요청」과 「값을 돌려주는 요청」이 갈리므로, 웹 페이지와 API 가 같은 클래스에 살 수 있다 — `@RestController` 는 **모든 메서드에 `@ResponseBody` 를 붙인 것**과 같다 → [[stereotype-annotation]] · [[json]]

**그리고 응답의 세 부분을 코드에서 다 만질 수 있게 된다.** 본문·헤더·상태 코드가 `ResponseEntity` 하나에 모이므로, 서블릿의 `response` 객체를 안 꺼내도 된다 → [[request-response]] · [[http-message]]

## 경계와 오해

- **`@ResponseBody` 를 빼먹으면 404 가 난다** — 돌려준 문자열이 뷰 이름으로 해석돼 그런 파일을 찾기 때문이다. **오류 메시지가 원인과 멀다** → [[view-resolver]]
- **한글이 깨지는 자리가 셋인데 답은 하나다** — `produces` 에 charset 을 적거나 헤더에 직접 넣는다. 메서드 안의 `setContentType` 은 **이미 늦다** → [[character-encoding]]
- **`HttpEntity` 와 `ResponseEntity` 는 상속 관계다** — 뒤엣것이 상태 코드를 더한 것이라, **상태 코드를 정할 일이 없으면 앞엣것으로 충분**하다. 다만 실무에서는 대개 `ResponseEntity` 를 쓴다 → [[http-method]]
- **리턴 타입이 `String` 이 아니면 변환기가 개입한다** — 객체를 돌려주면 메시지 컨버터가 JSON 등으로 바꾼다. 이 회차는 문자열만 다루지만, **그 자리에 컨버터가 있다**는 것이 다음 단계다 → [[json]]
- **`void` 를 돌려주면서 `PrintWriter` 로 직접 쓰는 방식도 된다** — 같은 노트의 아규먼트 절이 그 방법을 쓴다. **응답을 만드는 길이 둘**이므로 한 메서드에서 섞으면 안 된다 → [[handler-method-argument]]

## 함께 보는 개념

- [[handler-method-argument]] — 반대편(입력)의 규칙
- [[view-resolver]] — 표식이 없을 때 리턴값이 가는 곳
- [[spring-model]] — 뷰와 함께 값을 넘기는 방법
- [[request-response]] · [[http-message]] — 응답의 세 부분
- [[character-encoding]] — charset 을 정하는 자리
- [[json]] — 객체를 돌려줄 때 개입하는 변환

## 출처

- [[2024-10-16-Day94]] — 「요청핸들러의 리턴값」 절이 `@ResponseBody` 부터 `ResponseEntity` 까지 **일곱 개의 핸들러를 한 클래스에 나란히** 놓아 차이를 보인다. 그중 `handler3` 이 **`response.setContentType(...)` 을 불러 봐야 소용없다**는 것을 주석으로 확인한 자리가 특히 값지다 — 왜 `produces` 를 써야 하는지를 실패로 보였다. `HttpEntity` 는 「리턴 타입으로 콘텐트임을 알 수 있기 때문에 `@ResponseBody` 를 붙이지 않아도 된다」고 정확히 적었고, `HttpHeaders` 로 `Content-Type` 과 커스텀 헤더(`BIT-OK`)를 넣는 것, `HttpStatus.OK` 로 상태 코드를 정하는 것까지 이어진다. 이어지는 「view 컴포넌트(JSP) 쪽에 데이터 전달하기」 절은 같은 값을 `ServletRequest`·`Map`·`Model`·`ModelAndView` 네 방식으로 담아 보인다 → [[spring-model]]
