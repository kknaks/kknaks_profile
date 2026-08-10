---
type: concept
id: stereotype-annotation
title: 스테레오타입 애노테이션 (@Component 계열)
aliases:
  - "@Component"
  - "@Service"
  - "@Repository"
  - "@Controller"
  - 스테레오타입
  - stereotype
  - ComponentScan
up:
  - 2024-09-25-Day82
tags:
  - spring
  - 설계
  - 애노테이션
---

# 스테레오타입 애노테이션 (@Component 계열)

**「이 클래스를 컨테이너에 담아라」는 표식.** `@ComponentScan` 이 지정된 패키지를 훑어 이 표식이 붙은 클래스를 찾아 빈으로 만든다.

## 정의

넷이 있고 **하는 일은 같다.**

| 표식 | 붙이는 곳 |
|---|---|
| `@Component` | 특별한 역할이 없는 일반 빈 |
| `@Service` | 업무 로직 층 → [[service-layer]] |
| `@Repository` | 데이터 접근 층 → [[dao-pattern]] |
| `@Controller` | 웹 요청을 받는 층 → [[request-mapping]] |

`@Service`·`@Repository`·`@Controller` 는 **`@Component` 를 붙인 애노테이션**이다. 스캔 입장에서는 넷이 구별되지 않는다 — **차이는 읽는 사람에게 있다** → [[annotation]] · [[annotation-retention]]

다만 몇몇은 스캔 외의 일도 갖는다. `@Controller` 는 요청 매핑의 대상이 되고, `@Repository` 는 예외 변환의 대상이 된다.

## 사용 예시

앞 회차에서 직접 만든 애노테이션을 스프링 것으로 바꾸는 것이 **import 한 줄 교체**다.

```java
// 기존 — 직접 만든 애노테이션
import bitcamp.myapp.annotation.Component;

// 변경 — 스프링 것
import org.springframework.stereotype.Component;
```

```java
@Service
public class ProjectServiceImpl implements ProjectService {
  ...
}
```

## 왜 중요한가

**클래스에 「나는 이 층이다」를 적어 두는 것이 곧 배치의 문서가 된다.** `@Service` 가 붙은 클래스만 모아 보면 업무 로직의 목록이 나오고, `@Repository` 는 저장소에 닿는 것 전부다 — [[mvc-pattern]] 과 [[service-layer]] 에서 정한 층이 **코드에 표시로 남는다.**

그리고 **등록이 선언이 된다.** 설정 파일에 클래스 목록을 적어 두던 방식과 달리, 클래스 자신이 등록 여부를 들고 있어 파일이 두 곳으로 갈리지 않는다 → [[ioc-container]]

## 경계와 오해

- **넷을 구별해 붙여도 스프링은 대개 구별하지 않는다** — `@Service` 대신 `@Component` 를 써도 돈다. **틀린 것을 알려 주지 않으므로** 규율로 지켜야 하고, 반대로 「`@Service` 를 붙였으니 서비스답다」가 되지도 않는다
- **표식을 붙였는데 안 담기면 대개 패키지 문제다** — `@ComponentScan` 이 지정한 패키지 **아래**에 없으면 찾지 않는다 → [[package]]
- **인터페이스에 붙이는 것이 아니라 구현 클래스에 붙인다** — 컨테이너가 만들 수 있는 것은 인스턴스화 가능한 클래스다 → [[interface]] · [[reflective-instantiation]]
- **표식이 있다고 매 요청 새로 만들어지지 않는다** — 기본은 싱글턴이라 하나를 모두가 공유한다. `@Service` 클래스에 필드를 두고 요청 값을 담으면 다른 사용자의 값이 섞인다 → [[singleton-pattern]] · [[thread]]
- **`@Controller` 만 웹과 관계있다** — 나머지 셋은 웹이 아닌 애플리케이션에서도 같은 의미로 쓴다. 스프링 MVC 가 아니어도 IoC 컨테이너는 성립한다

## 함께 보는 개념

- [[ioc-container]] — 이 표식을 읽어 빈을 만드는 것
- [[annotation]] · [[annotation-retention]] — 표식이 실행 시점까지 남는 원리
- [[reflective-annotation-access]] — 스캔이 표식을 읽는 방법
- [[service-layer]] · [[dao-pattern]] — 표식이 가리키는 층
- [[request-mapping]] — `@Controller` 에 이어지는 표식
- [[spring-framework]] — 이 표식을 정의한 곳

## 출처

- [[2024-09-25-Day82]] — 「annotation 교체」 절이 `@ComponentScan("bitcamp.myapp")` 을 설명하면서 **`@Component`, `@Service`, `@Repository`, `@Controller` 를 한 묶음으로 나열**하고, 「Service 클래스 변경」 절이 그 교체가 실제로는 **import 한 줄 바꾸기**(`bitcamp.myapp.annotation.Component` → `org.springframework.stereotype.Component`)임을 코드로 남겼다 — 앞 회차에서 애노테이션을 직접 만들어 리플렉션으로 읽어 봤기 때문에 성립하는 대비다. 다만 넷의 차이가 무엇인지, 빈이 싱글턴이라는 것은 다루지 않았다
