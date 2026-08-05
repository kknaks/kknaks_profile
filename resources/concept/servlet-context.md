---
type: concept
id: servlet-context
title: 서블릿 컨텍스트 (ServletContext)
aliases:
  - ServletContext
  - 서블릿 컨텍스트
  - servlet context
  - ServletContextEvent
up:
  - 2024-08-27-Day64
tags:
  - web
  - java
  - JavaEE
  - 아키텍처
---

# 서블릿 컨텍스트 (ServletContext)

**웹 애플리케이션 하나에 하나씩 있는 공용 저장소 겸 컨테이너와의 창구 — 서블릿이 생성자로 의존을 받을 수 없게 된 자리를 대신 메우는 통로.** Day64 의 정의가 그대로다 — 「웹 애플리케이션 전체에 걸쳐 공유되는 설정과 리소스를 관리하는 객체로, 애플리케이션이 시작될 때 생성되고 종료될 때 소멸된다」 → [[servlet-container]] · [[web-application]]

## 정의

성질이 셋인데 **셋이 서로를 설명한다.**

| 성질 | Day64 의 근거 | 결과 |
|---|---|---|
| **앱마다 하나** | 「웹 애플리케이션 전체에 걸쳐 공유되는」 | 여기 담은 것은 **모든 서블릿·모든 요청·모든 사용자**가 본다 |
| **수명이 앱과 같다** | 「시작될 때 생성되고 종료될 때 소멸된다」 | 부팅에 담아 두면 요청 처리 동안 계속 있다 |
| **컨테이너가 만든다** | 리스너의 `ServletContextEvent` 로 온다 | 내가 `new` 하지 않고 **얻어 오기만** 한다 |

닿는 길이 두 가지다.

| 어디서 | 어떻게 |
|---|---|
| 리스너 | `sce.getServletContext()` — Day64 의 구동원리 4번(「이 객체 안에는 애플리케이션의 `ServletContext`가 포함되어 있다」) → [[servlet-listener]] |
| 서블릿 | `config.getServletContext()` — `init` 이 받은 `ServletConfig` 를 거쳐 → [[servlet-lifecycle]] |

**두 길이 서로 만나는 것이 이 개념이 하는 일 전부다** — 리스너가 넣고 서블릿이 꺼낸다.

## 사용 예시

Day64 의 부팅 코드가 만든 것을 이 자리에 놓는다.

```java
ServletContext ctx = sce.getServletContext();
ctx.setAttribute("userDao", userDao);
ctx.setAttribute("boardDao", boardDao);
ctx.setAttribute("projectDao", projectDao);
ctx.setAttribute("sqlSessionFactory", sqlSessionFactoryProxy);
```

그리고 서블릿이 `init` 에서 꺼낸다.

```java
userDao = (UserDao) config.getServletContext().getAttribute("userDao");
```

**두 줄 사이에 컴파일러가 검사하는 것이 하나도 없다.** 키는 문자열이고 값은 `Object` 로 오간다 — 그것이 이 통로의 편함이면서 아래 「경계와 오해」의 절반이다 → [[type-casting]]

**Day31 의 같은 일과 나란히 놓으면 무엇이 바뀌었는지가 보인다.**

| | Day31 (`App` 생성자) | Day64 (컨텍스트 속성) |
|---|---|---|
| 넣는 쪽 | `new UserCommand("회원", userList)` | `ctx.setAttribute("userDao", userDao)` |
| 받는 쪽 | 생성자 매개변수 | `getAttribute("userDao")` + 캐스팅 |
| 이름이 틀리면 | **컴파일 오류** | `null` → 첫 사용에서 NPE |
| 타입이 틀리면 | **컴파일 오류** | `ClassCastException` |
| 받는 쪽이 안 받으면 | 인수 개수가 안 맞아 컴파일 오류 | 아무 일도 안 일어난다 |

**검사가 전부 실행 시점으로 내려갔다.** 얻은 것은 「컨테이너가 생성자를 못 부르는데도 의존을 전할 수 있다」이고, 그 대가가 이 표의 오른쪽 열이다 → [[dependency-injection]]

## 왜 중요한가

**Day63 에서 답 없이 남은 물음의 답이다.** [[servlet-container]] 노트가 「컨테이너가 클래스를 찾아 만드므로 내 서블릿은 기본 생성자로 만들어진다 … 「의존을 어디서 받나」가 새로 풀어야 하는 문제가 되고, 그것이 프레임워크가 주입을 하는 이유다」로 적어 둔 자리에, **규격이 이미 갖고 있던 답**이 이것이다. 프레임워크가 오기 전 단계의 답이라 형태가 거칠지만(문자열 키·캐스팅) 문제는 정확히 그 문제다 → [[servlet-lifecycle]]

**그리고 「앱에 하나」를 언어가 아니라 자리로 보장한다.** 지금까지 하나임을 보장하는 방법은 `static` 이나 싱글톤 코드였다. 컨텍스트 속성은 **컨테이너가 앱마다 하나만 만드는 객체 안에** 담기므로, 코드에 `static` 이 한 글자도 없이 개수가 정해진다. [[thread-local]] 노트가 Day62 를 두고 「이 필드를 몇 개 만들 것인지가 코드에 적혀 있지 않다」고 걱정한 것이 나흘 뒤 이 자리로 해소된다 → [[singleton-pattern]] · [[static-member]] · [[instance]]

**여러 앱을 한 서버에 얹으면서도 서로를 못 보게 하는 경계다.** 컨텍스트가 앱마다 따로이므로 같은 톰캣 안의 다른 앱이 내 `"userDao"` 를 볼 수 없다. 「전역」처럼 쓰면서 **격리는 앱 단위**인 것이 이 저장소의 성격이다 → [[process]] · [[web-application-deployment]]

## 경계와 오해

- **`ServletContext` ≠ `ServletConfig`** — 이름이 비슷하고 한쪽에서 다른 쪽으로 가는 메서드(`config.getServletContext()`)가 있어 섞인다. **`Config` 는 서블릿마다 하나**(그 서블릿의 초기화 파라미터), **`Context` 는 앱마다 하나**(앱 전체의 파라미터와 속성)다. 그래서 초기화 파라미터도 두 층에 따로 있고, 「설정을 읽었는데 값이 없다」의 절반이 **다른 층에서 읽은 것**이다 → [[servlet-lifecycle]]
- **`ServletContext` ≠ 세션 — 그런데 API 가 똑같아서 잘못된 층에 담아도 컴파일된다** — 둘 다 `setAttribute(String, Object)`·`getAttribute(String)` 을 갖는다. 다른 것은 **범위와 수명**이다: 컨텍스트는 앱 전체·모든 사용자, 세션은 사용자 한 명. 그래서 로그인 사용자를 컨텍스트에 담으면 **한 사람이 로그인하면 전원이 그 사람으로 로그인된다** — 개발자 혼자 시험할 때는 정상으로 보이고, 사람이 둘이 되는 순간 드러난다. Day61 이 `prompt.setAttribute("loginUser", loginUser)` 로 상태를 연결에 붙였던 것과 **이름이 같다는 것**이 이 함정을 크게 만든다. 「무엇을 어느 범위에 담을 것인가」가 API 로 구별되지 않으므로 사람이 정해야 한다 → [[client-server-model]] · [[caching]]
- **키가 문자열이라 넣는 쪽과 꺼내는 쪽이 어긋난 것을 아무도 말해 주지 않는다** — 리스너가 `"userDao"` 로 넣고 서블릿이 `"userDAO"` 로 꺼내면 `getAttribute` 가 **`null` 을 돌려주고 그 자리에서는 아무 일도 없다.** 터지는 곳은 `userDao.list()` 를 부르는 `service` 안이고, 그때는 「목록 조회 중 오류 발생!」 한 줄로 덮인다(→ [[servlet-lifecycle]]). Day31 의 `commandMap` 키가 만들던 문제와 같은 형태이고, 대개의 답은 **키를 상수로 뽑는 것**이다 — 이 코드에는 그것이 없다 → [[literal]] · [[dispatch-table]]
- **`getAttribute` 가 `Object` 를 돌려주므로 타입 검사도 실행 시점이다** — `(UserDao)` 캐스팅이 그 증거다. 엉뚱한 것을 담아도 컴파일되고, 꺼내는 쪽에서 `ClassCastException` 이 난다. 제네릭이 이 자리를 도와주지 못하는 것은 **규격이 자바 5 이전 API** 이기 때문이고, 그래서 프레임워크의 주입은 이 통로를 쓰지 않는다 → [[type-casting]] · [[generics]] · [[raw-type]]
- **`"sqlSessionFactory"` 라는 이름에 든 것이 원본이 아니라 프록시다** — 값은 `SqlSessionFactoryProxy` 이고, 그것이 의도다(프록시를 거치지 않으면 쓰레드마다 세션이 갈리지 않는다). 그런데 **이름도 타입도 그 사실을 말하지 않는다** — 꺼내는 쪽은 `SqlSessionFactory` 로 받고 이름은 원본처럼 읽힌다. [[proxy-pattern]] 노트가 「이 프록시는 갈아 끼울 수 없다 — 빼면 컴파일은 되고 커밋만 조용히 사라진다」고 적은 위험이, 여기서 **부팅 코드 한 줄 + 문자열 키 뒤로 옮겨졌다.** 좁혀진 것은 좋고 눈에 덜 띄는 자리로 간 것은 나쁘다 → [[proxy-pattern]] · [[thread-local]]
- **컨텍스트 속성은 모든 쓰레드가 함께 보는 값이다 — 요청 처리 중에 넣으면 공유 변수를 쓰는 것과 같다** — 이 코드가 안전한 이유는 **부팅에 한 번만 넣고 그 뒤로 읽기만 하기 때문**이고, 규격이 막아 주는 것이 아니다. `service` 안에서 `setAttribute` 를 부르면 그 순간 남의 요청이 보는 값을 바꾼다 — 「앱 전체가 공유한다」의 다른 면이다 → [[thread]] · [[read-side-effect]]
- **「설정과 리소스를 관리하는 객체」는 절반이다 — 실제로는 컨테이너에게 묻는 창구다** — 속성 저장 말고도 `getRealPath`(웹 자원의 실제 경로) · `getResourceAsStream`(앱 안의 파일 읽기) · `log`(컨테이너 로그에 쓰기) · `getInitParameter`(앱 단위 파라미터) 가 이 객체에 있다. 즉 「내가 담은 것을 보관해 주는 곳」이면서 **「컨테이너에게 물어볼 것이 있을 때 가는 곳」**이고, 뒤쪽이 필기에 없다 → [[filesystem-path]] · [[servlet-container]]
- **컨텍스트가 소멸할 때 담긴 것을 정리해 주지는 않는다** — 「종료될 때 소멸된다」는 컨텍스트 객체의 이야기이고, 그 안에 든 `SqlSessionFactory` 가 들고 있는 커넥션 풀은 **누군가 닫아 주어야** 한다. 그 자리가 `contextDestroyed` 이고 Day64 의 리스너에는 없다 → [[servlet-listener]] · [[connection-lifetime-mismatch]] · [[garbage-collection]]
- **「애플리케이션 전체」가 톰캣 전체는 아니다 — 컨텍스트 경로마다 하나다** — 같은 서버에 앱을 둘 올리면 컨텍스트도 둘이고 속성도 따로다. 그러면 DB 커넥션 풀도 앱 수만큼 생긴다는 뜻이라, 「전역이니 하나뿐」으로 세면 연결 수 계산이 틀린다 → [[web-application-deployment]] · [[connection-pool-sizing-formula]]

## 함께 보는 개념

- [[servlet-listener]] — 여기에 물건을 놓는 쪽
- [[servlet-lifecycle]] — 여기서 물건을 꺼내는 쪽
- [[servlet-container]] — 이 객체를 만들고 관리하는 쪽
- [[web-component]] — 이 저장소를 함께 쓰는 부품들
- [[dependency-injection]] — 이 통로가 대신 서는 자리
- [[web-application]] — 이 객체 하나가 대응하는 단위
- [[proxy-pattern]] · [[thread-local]] — 이 자리에 담긴 것의 실체
- [[singleton-pattern]] · [[static-member]] · [[instance]] — 「하나임」을 보장하는 다른 방법들
- [[type-casting]] · [[generics]] · [[raw-type]] — `Object` 로 오가는 대가
- [[literal]] · [[dispatch-table]] — 문자열 키가 만드는 문제
- [[thread]] · [[read-side-effect]] — 공유 값으로서의 성질
- [[client-server-model]] — 「누구인지」를 어디에 담을지의 문제
- [[connection-lifetime-mismatch]] — 담긴 것을 정리하지 않을 때
- [[web-application-deployment]] — 이 경계가 앱 단위인 것의 결과
- [[filesystem-path]] — 컨테이너에게 실제 경로를 묻는 자리

## 출처

- [[2024-08-27-Day64]] — 「ServletContextListener」 절의 두 번째 줄이 이 개념의 정의다 — 「`ServletContext`는 웹 애플리케이션 전체에 걸쳐 공유되는 설정과 리소스를 관리하는 객체로, 애플리케이션이 시작될 때 생성되고 종료될 때 소멸된다」. 실습 코드가 이 객체를 **두 방향으로** 쓴다 — 리스너에서 `sce.getServletContext()` 로 얻어 `setAttribute` 네 번(`userDao`·`boardDao`·`projectDao`·`sqlSessionFactory`)으로 부팅 산출물을 올리고, 서블릿의 `init` 에서 `config.getServletContext().getAttribute("userDao")` 로 꺼내 캐스팅한다. 구동원리 4번이 `ServletContextEvent` 안에 이 객체가 들어 있다는 것을 적었다. 다만 **`ServletConfig` 와의 구별**, **세션과 API 가 같아서 생기는 스코프 혼동**, 키가 문자열이고 값이 `Object` 라 검사가 전부 실행 시점으로 내려간다는 것, `"sqlSessionFactory"` 라는 이름에 실제로는 프록시가 담긴다는 것, 요청 처리 중에 `setAttribute` 를 부르면 공유 값이 바뀐다는 것, 이 객체가 속성 저장 말고도 `getRealPath`·`getResourceAsStream`·`log` 같은 컨테이너 창구라는 것은 다루지 않았다
