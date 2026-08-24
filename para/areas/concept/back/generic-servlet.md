---
type: concept
id: generic-servlet
title: GenericServlet (추상 서블릿)
aliases:
  - GenericServlet
  - 제네릭 서블릿
  - generic servlet
up:
  - 2024-08-27-Day64
  - 2024-08-28-Day65
  - 2024-09-02-Day68
tags:
  - web
  - java
  - JavaEE
  - 추상화
---

# GenericServlet (추상 서블릿)

**`Servlet` 인터페이스의 다섯 메서드 중 넷을 미리 구현해 두고 `service()` 하나만 남긴 추상 클래스.** Day64 의 정의가 그대로다 — 「서블릿 API에서 제공하는 추상 클래스이다. 이 클래스는 **Servlet** 인터페이스를 구현하고 … 개발자는 **service()** 메서드를 구현하면 된다」 → [[servlet]] · [[servlet-lifecycle]] · [[abstract-class]]

## 정의

Day64 가 역할을 셋 적었는데 **첫째와 셋째가 같은 말**이다.

| Day64 의 역할 | 실제 내용 |
|---|---|
| 「**Servlet 인터페이스 기본 구현 제공** … 개발자가 필요한 메서드만 오버라이드해서 사용」 | 넷을 대신 구현했다 |
| 「**프로토콜 독립적 서블릿 지원** … HTTP와 같은 특정 프로토콜에 종속되지 않고」 | `service` 의 인수가 `ServletRequest`/`ServletResponse` 다 → [[request-response]] |
| 「**필수 메서드 구현**: 개발자는 **service()** 메서드를 구현해서」 | **첫째와 같은 사실** |

주요 메서드로 든 다섯은 `Servlet` 인터페이스와 같은 목록이고(`init`·`service`·`getServletConfig`·`getServletInfo`·`destroy`), **달라진 것은 목록이 아니라 「어느 것을 내가 써야 하나」다.**

| 메서드 | `Servlet` 을 직접 구현할 때 | `GenericServlet` 을 상속할 때 |
|---|---|---|
| `service` | 내가 쓴다 | **내가 쓴다** — 추상으로 남아 있는 유일한 것 |
| `init(ServletConfig)` | 내가 쓰고 `config` 를 필드에 보관해야 한다 | 대신 해 준다 |
| `getServletConfig()` | 보관한 것을 돌려주게 내가 쓴다 | 대신 해 준다 |
| `getServletInfo()` | 내가 쓴다 (빈 문자열이라도) | 대신 해 준다 |
| `destroy()` | 내가 쓴다 (비어 있어도) | 대신 해 준다 |

### Day64 의 앞 절이 이 클래스가 왜 있는지를 이미 보여 주었다

같은 노트의 `UserListServlet` 이 손으로 쓴 것 중 **셋이 이 클래스가 하는 일과 정확히 같다.**

```java
private ServletConfig config;                       // ← GenericServlet 이 갖고 있다

public void init(ServletConfig config) {
  this.config = config;                             // ← GenericServlet 이 한다
  ...
}
public ServletConfig getServletConfig() {
  return this.config;                               // ← GenericServlet 이 한다
}
public String getServletInfo() { return "회원 목록조회"; }
public void destroy() { }                           // ← 빈 구현
```

**즉 이 절은 앞 절의 반복을 지우는 절이다.** 그리고 앞 절의 골격 코드가 `config` 필드를 빠뜨려 컴파일되지 않았던 것(→ [[servlet-lifecycle]])이 **여기서는 빠뜨릴 자리 자체가 없어진다** — 「매번 똑같이 적어야 하는 코드」와 「빠뜨릴 수 있는 코드」가 같은 것이었다 → [[template-method-pattern]]

`GenericServlet` 은 그 위에 편의 메서드도 얹는다 — `getServletContext()`·`getInitParameter(name)`·`log(msg)`. 그러면 `config.getServletContext().getAttribute("userDao")` 가 `getServletContext().getAttribute("userDao")` 로 줄고, **`config` 라는 중간 객체가 부르는 쪽 코드에서 사라진다** → [[servlet-context]]

## 사용 예시

**하루 뒤 회차가 이 클래스를 실제로 상속한다.** Day64 가 코드 없이 설명만 했던 자리에 코드가 온다.

```java
@WebServlet("/user/view")
public class UserViewServlet extends GenericServlet {

  private UserDao userDao;

  @Override
  public void init() throws ServletException {
    // 서블릿 컨테이너 ---> init(ServletConfig) ---> init() 호출한다.
    userDao = (UserDao) this.getServletContext().getAttribute("userDao");
  }

  @Override
  public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException {
    res.setContentType("text/html;charset=UTF-8");
    PrintWriter out = res.getWriter();
    ...
  }
}
```

**남긴 것이 둘, 사라진 것이 셋이다.** 재정의한 것은 `init()` 과 `service()` 뿐이고,
`init(ServletConfig)`·`getServletConfig()`·`getServletInfo()`·`destroy()` 는 쓰지 않았다.

그리고 **인수 없는 `init()` 을 골랐다** — 위 「경계와 오해」가 「그쪽을 오버라이드하면
super 를 부를 자리가 없어 잊을 수도 없다」고 적은 그 선택이고, 필기의 주석이
`init(ServletConfig) ---> init()` 순서를 정확히 적어 두었다. `getServletContext()` 가
바로 다음 줄에서 동작하는 것이 **`super.init(config)` 이 이미 불렸다는 증거**다
→ [[servlet-context]] · [[servlet-lifecycle]]

## 왜 중요한가

**「인터페이스를 구현하라」와 「추상 클래스를 상속하라」의 차이가 실물로 갈리는 첫 자리다.** [[interface]]·[[abstract-class]] 를 배울 때의 차이(구현이 있나 없나)가 여기서는 **매 서블릿마다 열 줄 남짓의 차이**로 나타난다. 인터페이스는 「무엇을 채워야 하는가」만 말하고, 추상 클래스는 **「대개 이렇게 채운다」까지 들고 있다** → [[default-method]]

**그리고 이 필기의 다음 걸음이 이 클래스의 자식이다.** `HttpServlet` 이 `GenericServlet` 을 상속해 `service(ServletRequest, ServletResponse)` 를 구현하고, 그 안에서 요청 방식을 보고 `doGet`·`doPost` 로 갈라 준다. 즉 「기본 구현을 얹어 남길 것을 줄인다」가 **한 번 더 반복되는 구조**이고, 그 사슬을 알면 뒤에 나오는 `doGet` 이 어디서 온 것인지가 설명된다 → [[inheritance]] · [[method-overriding]]

### 닷새 뒤 — 「HTTP 가 아닐 때 쓴다」는 오해가 상속 사슬로 풀린다

Day64 노트가 「`HttpServlet` 이 이 클래스를 상속하므로 HTTP 를 쓸 때도 이 클래스를 쓰고 있다」로
짚어 둔 것이 Day68 에서 **필기 자신의 문장으로 확인된다.**

> 「`javax.servlet.GenericServlet` 추상 클래스를 상속 받았다」 — `HttpServlet` 설명 첫 줄

그리고 이 클래스가 추상으로 남긴 `service(ServletRequest, ServletResponse)` 를
`HttpServlet` 이 **구현해 채운다** — 그 안에서 캐스팅을 하고 HTTP 타입을 받는 쪽으로 넘긴다.

```java
public void service(ServletRequest req, ServletResponse res) ... {
    request = (HttpServletRequest) req;      // ← 여기로 모였다
    response = (HttpServletResponse) res;
    service(request, response);
}
```

**즉 이 클래스는 「HTTP 가 아닐 때」가 아니라 「HTTP 를 다루기 전 칸」이다** → [[http-servlet]]

같은 회차가 `init(ServletConfig)` 의 실제 코드도 인용해, 인수 없는 `init()` 이 왜 있는지를
문법으로 보인다.

```java
public void init(ServletConfig config) throws ServletException {
    this.config = config;
    this.init();          // ← 보관한 뒤 인수 없는 쪽을 부른다
}
```

## 경계와 오해

- **「HTTP 외의 프로토콜을 사용하는 서블릿을 만들 때 사용된다」 — 이 회차에서 가장 오해를 만드는 문장이다** — 「HTTP 에 종속되지 않는다」는 맞지만 **「HTTP 가 아닐 때 쓰는 것」이 아니다.** 실제로는 **`HttpServlet` 이 이 클래스를 상속하므로 HTTP 를 쓸 때도 이 클래스를 쓰고 있다.** 그리고 HTTP 아닌 서블릿은 사실상 존재하지 않는다 — 규격이 프로토콜 중립으로 설계되었을 뿐 쓰이는 곳은 웹이다. 이 문장을 그대로 믿으면 「우리는 HTTP 니까 이건 볼 필요 없다」가 되는데, **바로 다음에 배울 것이 이 클래스의 자식**이다 → [[generalization]] · [[inheritance]]
- **GenericServlet ≠ HttpServlet — 요청 방식은 여전히 구별되지 않는다** — 이 클래스는 `service(ServletRequest, ServletResponse)` 를 **추상으로 남긴다.** 즉 상속해도 `doGet`·`doPost` 는 없고, GET·POST 가 같은 메서드로 들어온다. 같은 노트의 컨테이너 절이 「요청에 따라 `doGet()`, `doPost()` 등의 메서드가 실행된다」고 적었지만 **그것은 `HttpServlet` 의 동작**이다. 「추상 클래스를 상속했으니 편해졌다」와 「HTTP 를 다루게 되었다」는 다른 걸음이다 → [[servlet-lifecycle]] · [[request-response]]
- **`init(ServletConfig)` 를 오버라이드하면 `super.init(config)` 를 반드시 불러야 한다 — 그래서 인수 없는 `init()` 이 따로 있다** — 이 클래스가 `config` 를 보관하는 코드는 `init(ServletConfig)` **안에** 있다. 내가 그 메서드를 오버라이드하면서 `super.init(config)` 를 빠뜨리면 보관이 일어나지 않고, 그 뒤 `getServletContext()` 가 **NPE** 다. 초기화는 정상으로 보이고 **처음 컨텍스트를 만질 때** 터지므로 원인이 멀다. 그래서 규격은 **인수 없는 `init()`** 을 하나 더 두었다 — 그쪽을 오버라이드하면 super 를 부를 자리가 없어 잊을 수도 없다. **「같은 이름의 메서드가 둘 있는 이유」가 실수를 구조적으로 없애는 것**이고, 필기의 주요 메서드 목록에는 `init(ServletConfig)` 만 있어 이 갈림이 보이지 않는다 → [[method-overriding]] · [[constructor]]
- **추상 클래스이므로 상속 한 칸을 쓴다** — 자바는 단일 상속이라 이미 다른 클래스를 상속하고 있는 클래스는 이 길로 서블릿이 될 수 없다. `Servlet` 인터페이스를 직접 구현하는 방법이 계속 남아 있는 이유가 그것이고, **「그래도 인터페이스 직접 구현을 배운 것」이 낭비가 아니었던 자리**다 → [[multiple-inheritance]] · [[interface]] · [[abstract-class]]
- **「기본 구현을 제공한다」가 「빈 메서드를 넣어 준다」와 다르다** — `getServletConfig()` 는 빈 구현이 아니라 **계약을 지키는 구현**(보관한 `config` 를 돌려준다)이고, `getServletInfo()` 는 빈 문자열을 돌려주는 진짜 빈 구현이다. 둘을 같은 것으로 읽으면 「어차피 비어 있으니 내가 다시 써도 된다」가 되는데, 앞쪽을 다시 쓰면 위 항목의 사고가 난다 → [[default-initialization]]
- **역할 세 항목 중 둘이 한 사실이다** — 1번(「기본 구현 제공 … 필요한 메서드만 오버라이드」)과 3번(「필수 메서드 구현: 개발자는 service()만」)이 같은 말이다. 실제로 이 클래스가 주는 것은 **둘**이다 — 반복 구현의 제거와 프로토콜 중립. 셋으로 세면 얻은 것이 하나 더 있는 것처럼 읽힌다.
- **「서블릿 프로토콜에 종속되지 않고」의 「서블릿 프로토콜」이라는 것은 없다** — 서블릿은 프로토콜이 아니라 규격이다. 뜻한 것은 **HTTP 에 종속되지 않는다**이고, 같은 문단 앞뒤가 그렇게 적혀 있다. 본문의 표현은 그대로 두었다.
- **Day64 의 이 절에는 코드가 없어 「줄어든다」가 얼마나인지 안 보였다 — 하루 뒤 Day65 가 그 코드를 준다**(위 「사용 예시」) — 앞 절의 열 몇 줄이 `extends GenericServlet` + `service` 하나로 줄어드는 것이 이 절의 값 전부인데, 그 비교가 화면에 없다. 그리고 앞 절 코드의 실제 결함(인수 받는 생성자, 빠진 `config` 필드) 중 **뒤쪽이 이 클래스로 해소되고 앞쪽은 그대로 남는다** — 컨테이너가 기본 생성자로 만든다는 제약은 어느 부모를 상속해도 같다 → [[servlet-lifecycle]]

## 함께 보는 개념

- [[servlet]] — 이 클래스가 구현하는 규격
- [[servlet-lifecycle]] — 이 클래스가 대신 채워 주는 메서드들
- [[request-response]] — `service` 가 받는 두 타입이 HTTP 중립인 자리
- [[servlet-context]] — 편의 메서드로 짧아지는 접근 경로
- [[abstract-class]] · [[interface]] — 두 길의 차이가 실물로 갈리는 자리
- [[template-method-pattern]] — 「골격은 부모, 빈칸은 자식」의 이름
- [[inheritance]] · [[method-overriding]] — `HttpServlet` 으로 이어지는 사슬
- [[multiple-inheritance]] — 상속 한 칸을 쓰는 대가
- [[generalization]] — 프로토콜 중립이 뜻하는 것
- [[default-method]] — 인터페이스가 기본 구현을 갖는 다른 방법
- [[servlet-container]] — 어느 부모를 상속해도 그대로인 제약(기본 생성자)

## 출처

- [[2024-09-02-Day68]] — 닷새 뒤. 「`GenericServlet` 상속 받기」 절이 「`service()` 메서드만 남겨두고 나머지 메서드들은 모두 구현하였다」로 이 클래스의 역할을 한 줄로 정리하고, `init(ServletConfig)` 가 `config` 를 보관한 뒤 인수 없는 `init()` 을 부르는 **실제 코드를 인용한다** — Day64 노트가 추론으로 적었던 것이 소스로 확인되는 자리다. 그리고 바로 다음 절이 `HttpServlet` 이 이 클래스를 상속한다는 것을 밝혀, **「HTTP 가 아닐 때 쓰는 것」이라는 Day64 의 문장이 왜 오해인지가 사슬로 드러난다** → [[http-servlet]]
- [[2024-08-28-Day65]] — 하루 뒤. **이 클래스를 실제로 상속한 첫 코드**다. `UserViewServlet extends GenericServlet` 이 `init()`(인수 없는 쪽)과 `service()` 둘만 재정의하고 나머지 넷을 물려받는데, Day64 가 「필요한 메서드만 오버라이드」로 설명만 하고 코드로 보이지 못한 자리를 이 회차가 채운다. 다만 이 회차도 `doGet`/`doPost` 는 쓰지 않는다 — GET·POST 가 같은 `service()` 로 들어오고, 로그인 폼이 `method` 없이 GET 으로 제출되는 것과 겹쳐 **요청 방식을 구별할 자리가 아예 없다** → [[html-form]]
- [[2024-08-27-Day64]] — 「GenericServlet 활용 > GenericServlet이란?」 절이 이 개념이다. 「서블릿 API에서 제공하는 추상 클래스 … **Servlet** 인터페이스를 구현하고, HTTP 외의 프로토콜을 사용하는 서블릿을 만들 때 사용된다」로 정의하고, 역할 셋(기본 구현 제공 / 프로토콜 독립 / 개발자는 `service()` 만)과 주요 메서드 다섯(`init`·`service`·`getServletConfig`·`getServletInfo`·`destroy`)을 적었다. **코드가 없다** — 그래서 같은 노트 앞 절의 `UserListServlet` 이 손으로 쓴 `config` 필드·`init` 의 보관·`getServletConfig()` 의 반환·빈 `destroy()` 가 정확히 이 클래스가 하는 일이라는 대비가 화면에 없고, `extends GenericServlet` 이 실제로 어떤 모양인지도 나오지 않는다. 「HTTP 외의 프로토콜을 사용하는 서블릿을 만들 때」라는 설명은 **`HttpServlet` 이 이 클래스를 상속한다**는 사실과 합치면 오해를 만들고, 이 클래스를 상속해도 `doGet`·`doPost` 는 없다는 것, `init(ServletConfig)` 를 오버라이드할 때 `super.init(config)` 를 불러야 한다는 것(그래서 인수 없는 `init()` 이 따로 있다는 것), 추상 클래스라 단일 상속 한 칸을 쓴다는 것도 다루지 않았다. 역할 1번과 3번은 같은 사실을 두 번 적은 것이다
