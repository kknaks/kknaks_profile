---
type: concept
id: servlet-lifecycle
title: 서블릿 생명 주기 (Servlet Lifecycle)
aliases:
  - 서블릿 생명주기
  - 서블릿 생명 주기
  - 서블릿 라이프사이클
  - servlet lifecycle
  - servlet life cycle
  - ServletConfig
up:
  - 2024-08-27-Day64
  - 2024-09-02-Day68
  - 2024-09-05-Day70
tags:
  - web
  - java
  - JavaEE
  - 생명주기
---

# 서블릿 생명 주기 (Servlet Lifecycle)

**컨테이너가 서블릿 하나를 「만들고 → 준비시키고 → 요청마다 부르고 → 버리는」 정해진 순서, 그리고 그 순서의 각 단계에 대응하는 메서드 다섯.** Day63 이 「생명 주기는 서블릿 컨테이너에 의해 제어된다」로 사실만 적었고, **Day64 가 그 다섯 메서드를 이름·기능·매개변수로 채운다** → [[servlet]] · [[servlet-container]]

## 정의

`Servlet` 인터페이스의 메서드가 다섯이고, **그중 셋이 생명 주기이고 둘은 조회**다.

| 메서드 | Day64 의 기능 설명 | 몇 번 불리나 |
|---|---|---|
| `init(ServletConfig config)` | 「서블릿이 최초로 로드될 때 호출되는 초기화 메서드 … 인스턴스가 생성된 후 초기화 작업을 수행」 | **한 번** |
| `service(ServletRequest, ServletResponse)` | 「요청을 처리하고, 응답을 생성 … 클라이언트로부터 요청을 받을 때마다 호출」 | **요청마다** (동시에 여러 번) |
| `destroy()` | 「서블릿이 종료되기 전에 호출 … 리소스를 정리하거나, 열린 연결을 닫는」 | **한 번** |
| `getServletConfig()` | 「설정 정보를 담고 있는 `ServletConfig` 객체를 반환 … 컨텍스트나 초기화 파라미터에 접근」 | 조회용 |
| `getServletInfo()` | 「서블릿의 설명, 버전 정보, 저작자 정보를 제공」 | 조회용 |

**시간축으로 세우면 `init` → `service`* → `destroy` 이고, 가운데만 여러 번이다.** 이 비대칭이 이 개념의 실질 전부다 — **한 번 하는 일과 매번 하는 일을 가르는 자리**이기 때문이다.

### 매개변수 셋이 각각 다른 것을 준다

| 매개변수 | Day64 의 설명 | 수명 |
|---|---|---|
| `ServletConfig config` | 「초기화 파라미터와 서블릿 환경에 대한 정보 … 이를 통해 서블릿 컨텍스트에 접근하거나」 | 서블릿과 같다 — **하나** |
| `ServletRequest req` | 「전달된 요청 데이터 … 요청 파라미터, 헤더 정보 등을 추출」 | 요청 하나 → [[request-response]] |
| `ServletResponse res` | 「보낼 응답 데이터 … 콘텐츠 타입, 출력 스트림 등을 설정」 | 요청 하나 → [[request-response]] |

**`ServletConfig` 가 「하나」인 쪽에 있는 것이 중요하다** — 그것을 통해 `ServletContext` 에 닿을 수 있고(`config.getServletContext()`), 리스너가 부팅 때 놓아 둔 물건이 그 안에 있다 → [[servlet-context]] · [[servlet-listener]]

## 사용 예시

Day64 는 골격을 먼저 보인다. **`@Override` 다섯 개가 이 인터페이스의 모양 전부**다.

```java
@WebServlet("/user/list")
public class UserListServlet implements Servlet {
  @Override
  public void init(ServletConfig config) throws ServletException {
    // 서블릿이 작업할 사용할 의존 객체를 준비하는 일을 이 메서드에서 수행한다.
  }

  @Override
  public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException {
    // 웹브라우저에서 이 서블릿을 실행해달라고 요청이 들어오면 이 메서드가 호출된다.
  }

  @Override
  public ServletConfig getServletConfig() {
    return this.config;
  }

  @Override
  public String getServletInfo() {
    return "";
  }

  @Override
  public void destroy() {
    // 서블릿 컨테이너가 종료되기 전에 해제할 자원이 있다면 이 메서드에서 수행한다.
  }
}
```

**주석 다섯 줄이 각 단계의 용도를 정확히 말한다** — 특히 `init` 의 「의존 객체를 준비하는 일」이 이 회차의 실습이 실제로 하는 일이다.

그리고 살을 붙인 것이 회원 목록 화면이다.

```java
@WebServlet("/user/list")
public class UserListServlet implements Servlet {
  private ServletConfig config;
  private UserDao userDao;

  public UserListServlet(UserDao userDao) {   // ← 이 줄이 이 서블릿을 뜨지 못하게 한다
    this.userDao = userDao;
  }

  @Override
  public void init(ServletConfig config) throws ServletException {
    this.config = config;
    userDao = (UserDao) config.getServletContext().getAttribute("userDao");
  }

  @Override
  public void service(ServletRequest req, ServletResponse res)
      throws ServletException, IOException {

    res.setContentType("text/html;charset=UTF-8");
    PrintWriter out = res.getWriter();
    ...
    try {
      for (User user : userDao.list()) {
        out.printf("    <tr><td>%d</td><td>%s</td><td>%s</td></tr>", user.getNo(), user.getName(),
            user.getEmail());
      }
    } catch (Exception e) {
      out.println("목록 조회 중 오류 발생!");
    }
  }

  @Override
  public ServletConfig getServletConfig() { return this.config; }

  @Override
  public String getServletInfo() { return "회원 목록조회"; }

  @Override
  public void destroy() { }
}
```

**세 줄이 「한 번」과 「매번」의 경계를 보여 준다.**

| 어디에 | 무엇이 | 왜 그 자리인가 |
|---|---|---|
| 필드 | `config` · `userDao` | 요청마다 다시 얻을 이유가 없다 |
| `init` | 컨텍스트에서 DAO 를 꺼내 필드에 담기 | **한 번** — 요청마다 하면 문자열 조회가 매번 돈다 |
| `service` 지역 변수 | `PrintWriter out` | **요청마다 다른 것** — 필드에 두면 남의 화면에 쓴다 |

**마지막 줄이 이 구조에서 가장 값비싼 규칙이다.** 서블릿 인스턴스는 하나이고 여러 쓰레드가 같은 `service` 에 동시에 들어오므로, **요청별 값을 필드에 담으면 남의 요청 값을 보게 된다.** 이 코드는 `out` 을 지역 변수로 두어 맞았고, 필기는 그 이유를 적지 않았다 → [[thread]] · [[variable-scope]]

## 왜 중요한가

**초기화를 어디에 두느냐가 「몇 벌 생기는가」를 정한다.** 같은 준비를 생성자에 두면 컨테이너가 만들 때, `init` 에 두면 서블릿마다 한 번, 리스너에 두면 앱마다 한 번이다. Day64 가 **DAO 를 리스너에서 만들고 서블릿의 `init` 에서 꺼내 쓰는** 형태를 고른 것이 정확히 이 계산이다 — 만드는 것은 앱에 하나, 꺼내는 것은 서블릿마다 하나 → [[servlet-listener]] · [[instance]]

**그리고 `main` 이 없는 코드에 「준비 구간」이 생긴다.** [[dependency-injection]] 노트가 Day31 을 두고 「만드는 순서와 쓰는 순서가 분리된다 … 뒤쪽에 `new` 가 없다는 것이 그 분리가 됐다는 신호」라고 적었는데, 웹에서는 그 분리가 **내 선택이 아니라 규격**이다. `service` 안에 `new` 가 없어야 하는 이유가 설계 취향이 아니라 **요청마다 도는 자리**이기 때문이다.

**대신 실패의 시점이 셋으로 갈린다.** 클래스를 만들 수 없어 실패하는 것 · `init` 에서 실패하는 것 · `service` 에서 실패하는 것이 **다 다른 증상**이고, 셋 중 앞의 둘은 로그를 보지 않으면 「요청하면 500」으로만 보인다. 아래 첫 두 항목이 이 회차 코드에서 실제로 그 둘이다 → [[exception-handling]]

### 엿새 뒤 — 구동 과정이 일곱 걸음으로 적힌다

Day64 는 메서드 다섯의 기능을 적었다. Day68 이 **컨테이너가 그것을 부르는 순서**를 적는다.

1. 클라이언트 요청 수신
2. 컨테이너가 URL 로 **어느 서블릿인지 결정** (`web.xml` 또는 `@WebServlet`) → [[web-xml]]
3. 인스턴스 **생성 또는 재사용** — 첫 요청이면 로드·생성, 그 뒤로는 재사용
4. 새로 생성됐으면 `init()` — **한 번만**
5. `service()` — 요청마다
6. 응답 전송
7. 컨테이너 종료·서블릿 제거 시 `destroy()`

**3번이 이 목록의 핵심이다** — 「생성 또는 재사용」이라 적혀 있고, 이어지는 절이 그 뜻을 못 박는다.

> 「서블릿 인스턴스는 오직 클래스 마다 한 개만 생성된다.」
> 「클라이언트마다 구분되어야 할 데이터는 서블릿 인스턴스 변수에 보관해서는 안된다.」
> 「인스턴스는 모든 클라이언트가 공유하기 때문에 config 와 같은 공유하는 데이터만 필드에 사용해야한다.」

**Day64 노트가 「인스턴스 1개 공유 사실(필기에 없음)」이라고 적어 둔 자리가 여기서 채워진다.**
그리고 그 규칙이 Day63~67 실습의 `private UserDao userDao;` 를 정당화한다 — DAO 는
클라이언트마다 다를 것이 없으므로 필드에 두어도 된다 → [[thread]] · [[servlet-context]]

## 경계와 오해

- **`public UserListServlet(UserDao userDao)` 하나 때문에 이 서블릿은 절대 뜨지 않는다 — 컴파일도 되고 서버도 정상 기동한다** — 컨테이너는 `@WebServlet` 으로 찾은 클래스를 **인수 없는 생성자로** 만든다. 자바는 생성자를 하나라도 명시하면 기본 생성자를 만들어 주지 않으므로 이 클래스에는 no-arg 생성자가 **없다.** 그러면 컨테이너의 인스턴스화가 실패하고(`InstantiationException`/`NoSuchMethodException`), 톰캣은 그것을 `ServletException` 으로 감싸 **`/user/list` 요청에 500** 을 낸다. 끝까지 세면 이렇다 — 컴파일 통과, `tomcat.start()` 성공, 다른 URL 정상, **이 화면만 500**, 그리고 원인은 목록 코드가 아니라 **쓰이지 않는 생성자**다. 더 나쁜 것은 **그 생성자가 필요조차 없다**는 점이다 — `init()` 이 이미 같은 `userDao` 를 컨텍스트에서 꺼내므로 생성자를 지우면 그 자리에서 고쳐진다. 즉 **한 필드를 두 경로로 채우려 한 코드가 남아 그중 절대 실행되지 않는 쪽이 클래스 전체를 막는다.** [[servlet-container]] 노트가 Day63 을 두고 「생성자에 인수를 줄 수 없다」고 적어 둔 것이 **하루 뒤 코드에 그대로 남아 있는** 형태다 → [[constructor]] · [[dependency-injection]] · [[reflective-instantiation]]
- **골격 코드의 `return this.config;` 는 그 자체로 컴파일되지 않는다** — 「서블릿의 구조는 다음과 같다」로 제시된 첫 코드에는 **`config` 필드 선언이 없고** `init` 이 받은 매개변수를 저장하지도 않는다. 두 번째 코드에서 `private ServletConfig config;` 가 생기며 해결되지만, 첫 코드를 그대로 옮겨 적으면 「기호를 찾을 수 없다」로 막힌다. **골격에서 빠진 것이 문법이 아니라 「받은 것을 보관해야 한다」는 계약**이라 눈에 안 걸린다 → [[variable-scope]]
- **`init` 의 `config` 를 저장하지 않으면 `getServletConfig()` 가 `null` 을 돌려준다 — 그리고 이것은 의례가 아니라 규격이다** — `getServletConfig()` 는 「`init` 에서 받은 그 객체를 돌려주어야 한다」가 계약이다. 저장을 잊으면 컴파일도 되고 요청도 처리되지만, **컨텍스트에 닿는 길이 끊긴다**(`getServletConfig().getServletContext()` 가 NPE). 두 번째 코드의 `this.config = config;` 한 줄이 그 계약을 지킨 것이고, **모든 서블릿이 똑같이 적어야 하는 줄**이라는 것이 다음 절(`GenericServlet`)이 존재하는 이유다 → [[generic-servlet]]
- **`init` 이 언제 도는지는 정해져 있지 않다 — 기본은 「첫 요청」이다** — 필기의 「서블릿이 최초로 **로드**될 때」와 컨테이너 절의 「웹 애플리케이션이 시작되면 … 서블릿을 로드하고 인스턴스화한다」가 서로 다른 시점을 가리키는데, **규격의 기본값은 첫 요청**이고 기동 시점에 만드는 것은 `loadOnStartup` 을 준 경우다. 그래서 「서버는 떴는데 첫 요청만 느리다」가 정상 동작이고, `init` 안의 오류는 **기동 로그가 아니라 첫 요청에서** 드러난다. 다만 어느 쪽이든 **리스너보다는 늦다** — 컨테이너가 리스너를 먼저 돌리므로 `getAttribute("userDao")` 가 준비돼 있다는 이 코드의 가정은 성립한다 → [[servlet-listener]] · [[load-on-startup]] · [[class-loading]]
- **`service()` 는 요청 방식을 구별하지 않는다 — 필기의 설명과 필기의 코드가 다른 층이다** — 같은 노트의 컨테이너 절이 「`service()` 메서드가 호출되며, 요청에 따라 `doGet()`, `doPost()` 등의 메서드가 실행된다」고 적고 서블릿 역할 절도 「`GET`, `POST`, `PUT`, `DELETE` 등의 HTTP 메서드를 지원한다」고 적었지만, **`Servlet` 인터페이스에는 `doGet`·`doPost` 가 없다.** 그 갈라 주는 일은 `HttpServlet.service()` 가 하고, 이 회차의 코드는 인터페이스를 직접 구현했으므로 **GET·POST·DELETE 어느 것으로 와도 같은 목록을 돌려준다.** 즉 「지원한다」는 이 코드에 대해 참이 아니고, 조회 화면이 DELETE 로도 열린다 → [[generic-servlet]] · [[servlet]]
- **예외를 응답 본문에 적고 200 으로 끝낸다 — 실패가 성공으로 보고된다** — `catch (Exception e) { out.println("목록 조회 중 오류 발생!"); }` 인데 그 앞에서 이미 `<html><body>` 와 `<h1>` 을 내보냈다. 코드가 상태 코드를 건드리지 않으므로 응답은 **200 OK** 이고, 브라우저·모니터링·검색엔진 모두 이 요청을 성공으로 센다. 게다가 `e` 를 **어디에도 남기지 않아** 무엇이 터졌는지 알 방법이 없다(연결 실패인지 SQL 오류인지 `userDao` 가 `null` 인지). 뒤늦게 `sendError` 로 바꾸려 해도 출력이 이미 버퍼를 넘겼으면 그때는 불가능하다. [[servlet-container]] 노트가 「컨테이너가 예외를 삼켜 500 응답으로 바꾼다」고 적은 그 장치를, **이 코드는 예외를 먼저 잡아서 쓰지 않기로 한 것**이다 → [[exception-handling]] · [[request-response]]
- **`destroy()` 가 비어 있다** — 리스너의 `contextDestroyed` 가 없는 것과 같은 자리다. 이 서블릿은 자기가 만든 자원이 없어 지금은 문제가 없지만, `init` 에서 무언가를 열기 시작하면 **닫을 자리가 준비돼 있는데 비어 있는** 상태가 된다 → [[servlet-listener]] · [[connection-lifetime-mismatch]]
- **`init` 에서 채운 필드는 안전하고 `service` 에서 채우는 필드는 안전하지 않다 — 이 규칙이 필기에 없다** — `userDao`·`config` 는 `init` 에서 한 번 담고 그 뒤 읽기만 하므로 여러 쓰레드가 함께 봐도 된다(DAO 자체가 상태를 갖지 않는 한). 반면 요청에서 온 값을 필드에 담으면 그 순간 남의 요청과 섞인다. **두 종류의 필드가 문법으로 구별되지 않으므로**(둘 다 그냥 `private`), 규칙을 모르면 「필드에 담는 게 편하다」로 같은 자리에 담게 된다. Day61 의 서버가 `SqlSession` 하나를 모든 접속이 공유해 커밋 경계가 섞였던 것과 같은 형태의 사고다 → [[thread]] · [[thread-local]] · [[immutability]]
- **다섯 메서드 중 둘은 생명 주기가 아니다** — `getServletConfig()`·`getServletInfo()` 는 컨테이너가 필요할 때 묻는 **조회 메서드**다. 「생명 주기 메서드가 다섯」으로 외우면 `getServletInfo()` 가 언제 도는지를 찾게 되는데, 필기가 정확히 적었다 — 「서블릿 컨테이너 관리 화면에서 서블릿을 정보를 출력할 때」다. 즉 **대부분의 경우 한 번도 불리지 않는다** → [[method]]
- **`@WebServlet("/user/list")` 의 문자열이 코드와 URL 을 잇는 유일한 끈이다** — 컴파일러는 이 문자열을 검사하지 않고, 두 서블릿이 같은 패턴을 쓰면 **기동 시점에 충돌**한다. Day31 의 `commandMap.put("회원", …)` 이 문자열 키로 명령을 찾던 자리가 여기서는 어노테이션으로 올라간 것이고, 검사 시점만 실행 → 기동으로 조금 앞당겨졌다 → [[annotation]] · [[dispatch-table]]

## 함께 보는 개념

- [[servlet]] — 이 주기를 갖는 대상
- [[servlet-container]] — 이 순서를 실제로 부르는 쪽
- [[generic-servlet]] — 다섯 중 넷을 대신 구현해 주는 추상 클래스
- [[request-response]] — `service` 가 받는 두 객체
- [[servlet-context]] — `init` 이 의존을 꺼내는 자리
- [[servlet-listener]] — 「앱마다 한 번」쪽 초기화
- [[constructor]] — 컨테이너가 인수를 줄 수 없는 자리
- [[dependency-injection]] — 의존을 어떻게 받나
- [[thread]] · [[thread-local]] — `service` 가 동시에 여러 번 도는 데서 오는 문제
- [[variable-scope]] — 필드와 지역 변수를 가르는 규칙
- [[exception-handling]] — 실패가 어느 시점·어느 형태로 나타나나
- [[class-loading]] — `init` 시점이 정해지는 층
- [[reflective-instantiation]] — 컨테이너가 클래스를 만드는 방식
- [[annotation]] · [[dispatch-table]] — URL 과 클래스를 잇는 방식
- [[instance]] — 「몇 벌 생기나」를 세는 축
- [[method]] — 조회 메서드와 콜백을 가르는 축

## 출처

- [[2024-09-05-Day70]] — 사흘 뒤. 「Load On Startup」 절이 기본 생성 시점을 「컨테이너가 최초 요청했을 때」로 적고, 늦은 오류 검증·첫 호출 지연을 이유로 `@WebServlet(loadOnStartup = 1)`과 `web.xml`의 `<load-on-startup>1</load-on-startup>`을 보였다. **기동 우선순위라는 표현은 같은 애플리케이션 안에서 선행 초기화할 서블릿의 순서를 뜻할 뿐, 요청 처리 우선순위는 아니다** → [[load-on-startup]]
- [[2024-09-02-Day68]] — 엿새 뒤. 「Servlet의 구동과정」 절이 컨테이너의 일곱 걸음을 적고, 3번에서 **「인스턴스 생성 또는 재사용」**을 명시한다. 이어지는 「서블릿 인스턴스와 클래스의 관계」가 「인스턴스는 오직 클래스 마다 한 개」·「클라이언트마다 구분되어야 할 데이터는 인스턴스 변수에 보관해서는 안된다」·「`config` 와 같은 공유하는 데이터만 필드에 사용해야한다」로 그 규칙을 못 박는다 — **Day64 노트가 「필기에 없다」고 적어 둔 사실이 채워진 자리**다
- [[2024-08-27-Day64]] — 「서블릿으로 리스트 만들기」·「서블릿 구현체의 메서드」 두 절이 이 개념이다. `implements Servlet` 골격 코드로 `@Override` 다섯 개(각 메서드의 용도를 주석으로)를 보이고, 이어 다섯 메서드를 **기능과 매개변수**로 하나씩 적었다 — `init(ServletConfig)`, `service(ServletRequest, ServletResponse)`, `getServletConfig()`, `getServletInfo()`, `destroy()`. 그리고 `UserListServlet` 실물로 `init` 에서 `config.getServletContext().getAttribute("userDao")` 로 DAO 를 받아 `service` 에서 `out.println` 으로 HTML 표를 그리는 코드를 실었다. 다만 **그 코드에 인수를 받는 생성자가 남아 있어 컨테이너가 클래스를 인스턴스화할 수 없고**(그 URL 만 500), 골격 코드는 `config` 필드가 없어 `return this.config;` 가 컴파일되지 않으며, `catch` 절이 예외를 응답 본문에 적고 200 으로 끝낸다. `init` 이 실제로 도는 시점(기본은 첫 요청), 인스턴스가 하나이고 `service` 가 동시에 여러 번 돈다는 것, 그래서 필드에 무엇을 담아도 되는지, `getServletConfig()` 가 `init` 의 인수를 돌려주어야 한다는 계약, `destroy()` 를 왜 채워야 하는지는 다루지 않았다. 같은 노트의 다른 절이 「요청에 따라 `doGet()`, `doPost()` 등이 실행된다」·「`GET`, `POST`, `PUT`, `DELETE` 등을 지원한다」고 적었지만 **`Servlet` 인터페이스에는 그 메서드가 없어** 이 코드에서는 일어나지 않는다
