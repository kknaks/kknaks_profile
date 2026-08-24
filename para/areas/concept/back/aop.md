---
type: concept
id: aop
title: AOP (관점 지향 프로그래밍)
aliases:
  - AOP
  - Aspect
  - "@Aspect"
  - "@Around"
  - 포인트컷
  - 횡단 관심사
up:
  - 2025-01-21-Day16
tags:
  - spring
  - 설계
  - 프레임워크
---

# AOP (관점 지향 프로그래밍)

**여기저기 흩어져 반복되는 공통 처리를 한 곳에 모으고, 「어디에 적용할지」를 조건으로 적는 것.** 부르는 코드를 고치지 않고 **앞뒤에 끼어든다.**

## 정의

문제는 **한 가지 관심사가 여러 메서드에 흩어지는 것**이다.

```java
// 모든 컨트롤러가 같은 두 줄을 반복한다
RsData<List<Post>> rsData = RsData.of("S-1", "성공", posts);
response.setStatus(rsData.getStatusCode());   // ← 이 줄이 어디에나 있다
return rsData;
```

그 줄을 걷어내고 **한 클래스로 옮긴다.**

```java
@Aspect
@Component
@RequiredArgsConstructor
public class ResponseAspect {
  private final HttpServletResponse response;

  @Around("""
      within(@org.springframework.web.bind.annotation.RestController *)
      && (@annotation(...GetMapping) || @annotation(...PostMapping) || ...)
      """)                                        // ← 어디에 적용할지 (포인트컷)
  public Object handleResponse(ProceedingJoinPoint joinPoint) throws Throwable {
    Object proceed = joinPoint.proceed();         // ← 원래 메서드 실행

    if (proceed instanceof RsData<?> rsData) {
      response.setStatus(rsData.getStatusCode()); // ← 공통 처리
    }
    return proceed;
  }
}
```

낱말 셋이 뼈대다.

| 낱말 | 무엇 |
|---|---|
| **어드바이스**(advice) | 끼워 넣을 **동작**. `@Around` 는 앞뒤 모두 |
| **포인트컷**(pointcut) | **어디에** 끼울지의 조건 (`within`·`@annotation` 등) |
| **조인포인트**(join point) | 실제로 끼어든 **그 자리**. `proceed()` 로 원래 것을 부른다 |

**`proceed()` 를 부르지 않으면 원래 메서드가 안 돈다** — 막을 수도 있다는 뜻이다 → [[handler-interceptor]] 의 `preHandle` 과 같은 구조다.

## 왜 중요한가

**이미 여러 번 만난 장치의 이름이 여기서 붙는다.** `@Transactional` 이 트랜잭션을 앞뒤로 감싸던 것, 프록시가 메서드를 가로채던 것 — 전부 이 방식이었다 → [[declarative-transaction]] · [[dynamic-proxy]]

**그리고 「어디에」를 조건으로 적는다는 것이 핵심이다.** 인터셉터는 **URL 패턴**으로 범위를 정하지만, AOP 는 **애노테이션·패키지·클래스·메서드 시그니처**로 정한다 — 웹이 아닌 곳에도 걸 수 있다 → [[handler-interceptor]]

**공통 관심사가 업무 코드에서 빠지면 읽기 쉬워진다.** 컨트롤러가 「무엇을 돌려줄지」만 적고 상태 코드는 신경 쓰지 않는 것이 그 결과다 → [[api-response-envelope]] · [[cohesion]]

## 경계와 오해

- **프록시를 통해서만 걸린다** — 같은 클래스 안에서 `this.method()` 로 부르면 **끼어들지 않는다.** `@Transactional` 의 자기 호출 함정과 **정확히 같은 원인**이다 → [[dynamic-proxy]] · [[declarative-transaction]]
- **코드에 안 보이는 동작이 생긴다** — 컨트롤러만 읽으면 상태 코드가 어디서 정해지는지 알 수 없다. **편해지는 만큼 추적이 어려워지고**, 그것이 이 방식의 대가다
- **포인트컷이 틀리면 조용히 아무 데도 안 걸린다** — 오류가 아니라 **아무 일도 안 일어나는 것**으로 나타난다. 필기의 표현식이 긴 이유도 그만큼 정확히 겨눠야 하기 때문이다
- **`@Around` 는 `proceed()` 를 반드시 불러야 한다** — 잊으면 원래 메서드가 안 돌고, **예외도 안 난다**
- **모든 공통 처리를 AOP 로 할 필요는 없다** — 웹 요청 앞뒤라면 인터셉터가, 컨테이너 수준이면 필터가 더 맞다. **셋이 걸리는 지점이 다르다** → [[servlet-filter]] · [[handler-interceptor]]
- **관점을 남발하면 흐름이 사라진다** — 로깅·인증·트랜잭션·응답 가공이 전부 보이지 않는 곳에서 일어나면, **코드를 읽어도 무슨 일이 나는지 모른다**

## 함께 보는 개념

- [[dynamic-proxy]] — AOP 가 실제로 동작하는 방식
- [[declarative-transaction]] — 같은 장치로 만들어진 대표 기능
- [[handler-interceptor]] · [[servlet-filter]] — 겹치는 다른 층의 장치
- [[bean-post-processor]] — 프록시가 끼워지는 지점
- [[api-response-envelope]] — 이 회차가 AOP 로 자동화한 대상
- [[cohesion]] — 흩어진 관심사를 모으는 축

## 출처

- [[2025-01-21-Day16]] — 「참고. AOP를 이용한 Response 수정」 절이 **문제를 먼저 코드로 보인 것**이 좋다 — 컨트롤러마다 `response.setStatus(rsData.getStatusCode())` 를 반복하는 「기존 코드」와, 그 줄이 사라진 「AOP 를 이용한 코드」를 나란히 놓았다. 그다음 `ResponseAspect` 전문이 나오는데 **포인트컷 표현식이 특히 구체적이다** — `within(@RestController *)` 로 클래스를 좁히고 `@annotation(GetMapping) || ...` 으로 매핑 애노테이션이 붙은 메서드만, 또는 `@ResponseBody` 가 붙은 것을 잡는다. `@Around` 안에서 `joinPoint.proceed()` 로 원래 메서드를 부르고 반환값이 `RsData` 일 때만 상태 코드를 설정한 뒤 **그대로 돌려주어 메시지 컨버터로 넘기는** 흐름이 주석으로 세 단계로 적혀 있다. 다만 자기 호출에서는 안 걸린다는 것, 포인트컷이 틀렸을 때 조용하다는 것은 다루지 않았다
