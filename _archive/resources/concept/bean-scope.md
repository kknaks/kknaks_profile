---
type: concept
id: bean-scope
title: 빈 스코프 (Bean Scope)
aliases:
  - 빈 스코프
  - bean scope
  - prototype
  - singleton 스코프
up:
  - 2024-10-02-Day87
tags:
  - spring
  - 생성
  - 설계
---

# 빈 스코프 (Bean Scope)

**컨테이너가 그 빈을 몇 개 만들고 언제까지 살려 둘지를 정하는 설정.** 기본은 하나만 만들어 모두가 공유하는 `singleton` 이다.

## 정의

| 스코프 | 언제 새로 만드나 |
|---|---|
| **singleton**(기본) | **한 번만.** 컨테이너가 만들어질 때 미리 준비된다 |
| **prototype** | `getBean()` 을 부를 때마다 |
| request | (웹) 요청이 들어올 때마다 → [[request-response]] |
| session | (웹) 세션이 생길 때마다 → [[http-session]] |
| application | (웹) 애플리케이션을 시작할 때 → [[servlet-context]] |
| websocket | (웹) 웹소켓이 연결될 때 |

```xml
<bean id="c1" class="...Car"/>                       <!-- singleton (기본) -->
<bean id="c2" class="...Car" scope="singleton"/>
<bean id="c3" class="...Car" scope="prototype"/>
```

**앞의 둘과 뒤의 넷은 성격이 다르다.** singleton·prototype 은 어디서나 쓰이고, 나머지 넷은 **웹 요청의 수명에 얹힌** 것이라 웹 컨테이너가 있어야 성립한다 → [[attribute-scope]]

## 왜 중요한가

**「이 객체에 상태를 둬도 되는가」의 답이 스코프다.** 싱글턴 빈은 모든 요청이 같은 객체를 만지므로 필드에 요청별 값을 담으면 **다른 사용자의 값이 섞인다.** 그래서 서비스·DAO·컨트롤러는 **상태가 없게** 만든다 → [[thread]] · [[singleton-pattern]]

**그리고 생성 시점이 오류 시점을 정한다.** 싱글턴은 컨테이너가 뜰 때 만들어지므로 설정이 틀리면 **기동에서** 실패하고, prototype 은 `getBean()` 할 때 만들어지므로 **한참 뒤에** 실패한다 → [[ioc-container]]

## 경계와 오해

- **prototype 빈은 컨테이너가 소멸을 관리하지 않는다** — 만들어 주기만 하고 그 뒤로는 놓아 준다. 자원을 여는 빈을 prototype 으로 두면 **닫아 줄 사람이 없다** → [[try-with-resources]] · [[garbage-collection]]
- **싱글턴 빈에 prototype 을 주입하면 한 번만 주입된다** — 싱글턴이 만들어질 때 받은 그 하나를 계속 쓰므로, **prototype 인데 하나만 존재**하게 된다. 「매번 새로 만들어지겠지」가 어긋나는 자리다
- **스프링의 singleton ≠ [[singleton-pattern]]** — 디자인 패턴 쪽은 **JVM 안에 인스턴스가 하나**라는 것이고, 스프링은 **그 컨테이너 안에 이름당 하나**다. 컨테이너가 둘이면 객체도 둘이고, 같은 클래스를 다른 이름으로 두 번 등록하면 객체도 둘이다
- **request/session 스코프 빈을 싱글턴에 주입하면 그대로는 안 된다** — 수명이 짧은 것을 긴 것에 넣는 것이라 프록시가 끼어야 한다. 수명이 다른 것을 잇는 자리에는 항상 무언가가 필요하다 → [[dynamic-proxy]]
- **「메모리 절약」으로 prototype 을 고르는 것은 대개 잘못이다** — 값 객체(VO·DTO)는 애초에 컨테이너에 담지 않고 `new` 로 만든다. 스코프는 **컨테이너가 관리할 만한 협력 객체**에 대한 결정이다

## 함께 보는 개념

- [[ioc-container]] — 스코프를 해석하는 주체
- [[singleton-pattern]] — 이름이 겹치는 인접 개념
- [[bean-definition]] — 스코프를 적는 자리
- [[attribute-scope]] — 웹 스코프 넷과 대응하는 보관소
- [[thread]] — 싱글턴 빈에 상태를 두면 안 되는 이유
- [[instance]] — 몇 개 만들어지는가라는 물음

## 출처

- [[2024-10-02-Day87]] — 「빈 생성 정책」 절이 `scope` 속성의 여섯 값(singleton·prototype·request·session·application·websocket)을 한 줄씩 적고, **「singleton 객체는 IoC 컨테이너가 생성될 때 미리 준비된다 / prototype 객체는 `getBean()` 을 호출할 때 생성된다」**로 **생성 시점의 차이**를 짚었다 — 이것이 이 개념의 뼈대다. XML 예시가 기본값(속성 없음)과 명시(`scope="singleton"`)와 prototype 셋을 나란히 보인다. 다만 싱글턴 빈에 상태를 두면 안 되는 이유, prototype 의 소멸 관리, 웹 스코프 넷이 실제로 어떻게 쓰이는지는 다루지 않았다
