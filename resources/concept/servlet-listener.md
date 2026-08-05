---
type: concept
id: servlet-listener
title: 서블릿 리스너 (Servlet Listener)
aliases:
  - 서블릿 리스너
  - servlet listener
  - 웹 리스너
  - ServletContextListener
  - ContextLoaderListener
up:
  - 2024-08-27-Day64
  - 2024-09-02-Day68
tags:
  - web
  - java
  - JavaEE
  - 생명주기
---

# 서블릿 리스너 (Servlet Listener)

**컨테이너 안에서 무언가가 생기거나 없어질 때 통보받는 객체 — `main` 이 없어진 자리에서 「앱이 시작될 때 할 일」을 갖는 곳.** Day64 의 정의가 그대로다 — 「자바 웹 애플리케이션에서 특정 이벤트가 발생할 때 자동으로 실행되는 객체이다」·「**서블릿 컨테이너**에서 발생하는 이벤트에 반응한다」 → [[servlet-container]] · [[web-component]]

## 정의

**요청을 받는 것이 아니라 이벤트를 받는다.** Day64 가 대상을 세 수준으로 적었다 — 「주로 애플리케이션, 세션, 또는 요청 수준의 이벤트」.

| 수준 | 언제 도나 | 규격의 인터페이스 (필기에 없다 — 아래) |
|---|---|---|
| **애플리케이션** | 앱이 뜰 때·질 때, 앱 스코프 속성이 바뀔 때 | `ServletContextListener` · `ServletContextAttributeListener` |
| 세션 | 세션이 만들어질 때·없어질 때, 세션 속성이 바뀔 때 | `HttpSessionListener` · `HttpSessionAttributeListener` |
| 요청 | 요청이 들어올 때·끝날 때 | `ServletRequestListener` · `ServletRequestAttributeListener` |

**Day64 가 실제로 다루는 것은 첫 줄 하나**이고, 소제목이 「리스너의 정의와 **종류**」인데 종류가 하나도 열거되지 않는다. 위 표의 오른쪽 칸이 그 빈 자리를 채운 것이다.

### 하는 일 — Day64 의 셋

| Day64 의 역할 | 어느 수준의 이벤트인가 |
|---|---|
| 「**리소스 초기화 및 해제**: 애플리케이션이 시작되거나 종료될 때, 데이터베이스 연결 풀을 설정하거나 해제」 | 애플리케이션 — **이 회차가 실습한 것** |
| 「**요청 로깅 및 감사**: 들어오는 요청을 기록하거나 … 이벤트를 감시」 | 요청 |
| 「**세션 추적**: 사용자 세션의 수를 추적하거나 세션이 종료되었을 때 로그를 기록」 | 세션 |

### ServletContextListener — 메서드가 둘이다

Day64 가 두 메서드를 짝으로 적었다.

| 메서드 | Day64 의 설명 | 이 회차의 코드에 |
|---|---|---|
| `contextInitialized(ServletContextEvent sce)` | 「웹 애플리케이션이 시작될 때 호출 … 필요한 리소스나 데이터를 초기화」 | **있다** |
| `contextDestroyed(ServletContextEvent sce)` | 「웹 애플리케이션이 종료될 때 호출 … 열려 있는 데이터베이스 연결을 닫거나, 로깅을 남길 때」 | **없다** — 아래 「경계와 오해」 |

인수로 오는 `ServletContextEvent` 는 **`ServletContext` 를 꺼내는 통로**다 — Day64 의 구동원리 4번이 그것을 적었다(「이 객체 안에는 애플리케이션의 `ServletContext`가 포함되어 있다」). 그래서 이 메서드는 「앱 전체가 볼 물건을 놓을 자리」에 닿을 수 있다 → [[servlet-context]]

### 구동원리 — Day64 가 컨테이너의 부팅 순서를 처음 적는다

1. **`Tomcat.start()` → 서블릿 컨테이너 실행** — 「이 컨테이너는 서블릿, JSP, 필터, 리스너 같은 웹 애플리케이션 구성 요소들을 관리한다」 → [[tomcat]]
2. **리스너 탐색** — 「`web.xml`이나 `@WebListener` 어노테이션을 통해 등록된 리스너들을 탐색한다」 → [[annotation]]
3. **인스턴스화 후 `contextInitialized` 호출** — 컨테이너가 클래스를 만든다 → [[reflective-instantiation]]
4. **`ServletContextEvent` 생성·전달**
5. **초기 설정 완료**
6. **애플리케이션 정상 실행** — 「이후 서블릿이나 JSP가 클라이언트 요청을 처리할 준비가 완료된다」

**6번이 이 목록의 값이다** — 리스너가 끝난 다음에 요청 처리가 시작되므로, **서블릿은 리스너가 놓아 둔 것을 이미 있다고 가정해도 된다.** 순서가 이렇게 정해져 있다는 것이 Day64 의 실습이 성립하는 근거다 → [[servlet-lifecycle]]

## 사용 예시

Day64 의 리스너가 **프로젝트 전체의 부팅 코드**다. Day59~62 에서 `main` 이 하던 일이 그대로 이 메서드로 옮겨졌다.

```java
@WebListener
public class ContextLoaderListener implements ServletContextListener {
  @Override
  public void contextInitialized(ServletContextEvent sce) {
    try {
      InputStream inputStream = Resources.getResourceAsStream("config/mybatis-config.xml");
      SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
      SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(inputStream);
      SqlSessionFactoryProxy sqlSessionFactoryProxy = new SqlSessionFactoryProxy(sqlSessionFactory);

      DaoFactory daoFactory = new DaoFactory(sqlSessionFactoryProxy);

      UserDao userDao = daoFactory.createObject(UserDao.class);
      BoardDao boardDao = daoFactory.createObject(BoardDao.class);
      ProjectDao projectDao = daoFactory.createObject(ProjectDao.class);

      ServletContext ctx = sce.getServletContext();
      ctx.setAttribute("userDao", userDao);
      ctx.setAttribute("boardDao", boardDao);
      ctx.setAttribute("projectDao", projectDao);
      ctx.setAttribute("sqlSessionFactory", sqlSessionFactoryProxy);

    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
```

**세 일이 순서대로 있다.**

| 구간 | 하는 일 | 왜 여기여야 하나 |
|---|---|---|
| `Resources.getResourceAsStream` → `build(inputStream)` | 설정을 읽어 팩토리를 만든다 | 요청마다 XML 을 다시 읽을 이유가 없다 → [[mybatis]] · [[xml]] |
| `new SqlSessionFactoryProxy(...)` → `new DaoFactory(...)` → `createObject(...)` | 대리자를 씌우고 DAO 를 만든다 | **앱에 하나여야 하는 것들**이다 → [[proxy-pattern]] · [[thread-local]] · [[dynamic-proxy]] |
| `ctx.setAttribute(...)` 네 줄 | 만든 것을 앱 스코프에 놓는다 | 서블릿이 생성자로 받을 수 없으므로 → [[servlet-context]] · [[dependency-injection]] |

**가운데 구간이 이 노트의 실질이다.** [[thread-local]] 노트가 Day62 를 두고 「이 필드를 몇 개 만들 것인지가 코드에 적혀 있지 않고, 프록시를 두 벌 만들면 한 쓰레드가 세션을 두 개 갖는다」고 걱정한 자리가 **나흘 뒤 여기서 해소된다** — 만드는 지점이 부팅 이벤트 한 곳이므로 앱에 하나가 보장된다. `static` 도 싱글톤 코드도 필요 없이 **자리 하나로** 개수가 정해졌다 → [[singleton-pattern]] · [[instance]]

## 왜 중요한가

**「`main` 이 사라졌는데 시작할 때 할 일은 남아 있다」의 답이다.** [[servlet-container]] 노트가 Day63 을 두고 「내 코드가 시작점을 갖지 않는다」·「생성자에 인수를 줄 수 없어 의존을 어디서 받나가 새로 풀어야 하는 문제가 된다」고 적었는데, 그 두 문제의 답이 같은 것이다 — **컨테이너가 부르는 시작점을 하나 얻고, 거기서 만든 것을 앱 스코프에 둔다** → [[main-method]] · [[servlet-context]]

**그리고 「앱에 하나」를 자리로 보장한다.** 같은 초기화를 서블릿의 `init()` 에서 하면 **서블릿마다 한 벌씩** 생긴다 — 회원 서블릿과 게시판 서블릿이 각자 `SqlSessionFactory` 를 만들고, 그러면 프록시가 두 개이므로 한 쓰레드가 세션을 두 개 갖고 [[transaction]] 경계가 화면마다 갈린다. **리스너는 앱마다 한 번이고 서블릿은 서블릿마다 한 번**이라는 차이가 여기서 값을 만든다 → [[servlet-lifecycle]] · [[sql-session]]

**흐름을 갖지 않는 코드가 순서를 얻는다.** 「리스너 → 서블릿」이 규격이 정한 순서이므로, 서블릿은 자기가 필요한 것이 이미 준비돼 있다고 가정해도 된다. 이 가정이 없으면 모든 서블릿이 「없으면 만들기」를 각자 해야 하고 그것이 곧 여러 벌이 생기는 길이다 → [[caching]]

### 엿새 뒤 — 필기가 스스로 패턴 이름을 붙인다

Day68 의 「Listener 만들기」 절이 한 줄로 정의를 다시 쓴다.

> 「서블릿 컨테이너 또는 서블릿, 세션 등의 객체 상태가 변경되었을 때 보고 받는 **옵저버패턴**이다.」

**Day44 에서 손으로 만든 것이 규격 안에 이미 있었다는 것이 여기서 이름으로 이어진다** →
[[observer-pattern]]

다만 두 가지가 다르다.

| | Day44 의 손으로 만든 옵저버 | 서블릿 리스너 |
|---|---|---|
| 등록 | `registerObserver(this)` 를 코드로 부른다 | **설정 파일이나 애노테이션** → [[web-xml]] |
| 목록 | `List<Observer>` 를 내가 들고 있다 | **컨테이너가 들고 있어 볼 수 없다** |
| 통지 | 내가 `notifyObservers()` 를 부른다 | 컨테이너가 이벤트 시점에 부른다 |

**「등록이 스키마에 박힌다」는 것이 이 형태의 성질이다** — 무엇이 듣고 있는지 코드를 읽어서는
알 수 없고 설정을 봐야 한다.

## 경계와 오해

- **`contextDestroyed` 가 없다 — 그리고 `setReloadable(true)` 때문에 그 부재가 개발 중에 바로 걸린다** — Day64 는 이 메서드의 용도를 「열려 있는 데이터베이스 연결을 닫거나」로 정확히 적어 두고 **코드에는 넣지 않았다.** 끝까지 따라가면 이렇게 된다: 클래스 파일이 바뀌면 톰캣이 컨텍스트를 다시 시작하는데(Day63 의 `ctx.setReloadable(true)`), 그때 컨테이너는 `contextDestroyed` → `contextInitialized` 를 부른다. 정리 코드가 없으므로 **옛 `SqlSessionFactory` 가 들고 있던 커넥션 풀이 회수되지 않은 채 새 풀이 또 생긴다.** 저장을 몇 번 하면 DB 쪽 연결 수만 늘어나고, MyBatis `POOLED` 의 활성 상한(기본 10)과 MySQL 의 `max_connections` 가 순서대로 걸린다. **증상이 「코드를 여러 번 고친 뒤부터 화면이 멈춘다」라서 방금 고친 코드를 의심하게 된다** — 원인은 그 코드가 아니라 재시작 횟수다 → [[connection-lifetime-mismatch]] · [[tomcat]] · [[try-with-resources]]
- **`catch (Exception e) { e.printStackTrace(); }` 가 기동 실패를 요청 실패로 미룬다 — 이 회차에서 가장 비싼 세 줄이다** — 규격은 `contextInitialized` 가 예외를 던지면 컨테이너가 그 애플리케이션을 **기동 실패로 처리**하게 되어 있다. 즉 「설정이 잘못됐으면 서버가 안 뜬다」는 장치가 이미 있는데, 이 코드는 예외를 삼켜서 **그 장치를 껐다.** `config/mybatis-config.xml` 을 못 찾거나 DB 정보가 틀리면 스택트레이스만 콘솔에 찍히고 `contextInitialized` 는 **정상 종료**하며, 컨테이너는 앱이 떴다고 보고 요청을 받기 시작한다. 그러면 `ctx.setAttribute` 가 한 줄도 실행되지 않았으므로 서블릿의 `init()` 에서 `getAttribute("userDao")` 가 `null` 이고, **첫 요청에서 `NullPointerException` → 500** 이 난다. **원인(부팅 시점 설정 오류)과 증상(요청 시점 NPE)이 다른 시각·다른 화면에서 나타나는** 형태이고, 로그를 안 보고 있으면 유일한 단서가 사라져 있다 → [[exception-handling]] · [[servlet-context]]
- **리스너 ≠ 필터 — 흐름 위에 있는가로 갈린다** — 둘 다 「서블릿 밖에서 도는 코드」라 섞이는데, 필터는 **요청이 지나가는 길 위에** 있어서 요청을 막을 수도 바꿔서 넘길 수도 있다. 리스너는 **통보만 받는다** — 이벤트를 취소하거나 요청을 가로챌 방법이 없다. Day64 가 역할에 「요청 로깅 및 감사」를 리스너 쪽에 적었는데, **요청을 기록하는 일은 대개 필터의 자리**이고 요청 리스너는 「요청이 시작·종료했다」는 두 시점만 안다 → [[servlet-filter]] · [[observer-pattern]]
- **`@WebListener` 만으로는 여러 리스너의 순서를 정할 수 없다** — 어노테이션으로 등록한 것들 사이의 호출 순서는 규격이 보장하지 않고, `web.xml` 에 적으면 **문서에 적힌 순서**가 순서다. 이 코드는 리스너가 하나뿐이라 걸리지 않지만, 「DB 초기화가 끝난 뒤에 캐시를 채운다」처럼 리스너 사이에 의존이 생기는 순간 **어노테이션만으로는 표현할 수 없는 요구**가 된다. 그래서 어노테이션이 `web.xml` 을 완전히 대체하지 않는다 → [[xml]] · [[annotation]]
- **`ServletContextListener` 는 「앱마다 한 번」이 아니라 「컨텍스트마다 한 번」이다** — 같은 톰캣에 앱을 둘 올리면 리스너가 각각 돌고 각자의 `ServletContext` 에 넣는다. 그래서 「전역」이라 읽으면 톰캣 전체로 착각하고, DB 연결이 앱 수만큼 늘어난다는 것도 놓친다 → [[servlet-context]] · [[process]]
- **초기화 순서에 대한 보장이 어디까지인가를 필기가 적지 않았다** — 규격이 정하는 것은 **리스너의 `contextInitialized` 가 서블릿·필터의 초기화보다 먼저**라는 것까지다. 리스너와 리스너 사이(위 항목), 서블릿과 서블릿 사이는 정해져 있지 않다. Day64 의 구동원리 6번(「이후 서블릿이나 JSP가 … 준비가 완료된다」)은 그 보장을 정확히 말한 것이지만, **그 이상까지 순서가 정해져 있다고 읽으면** 뒤에 리스너가 늘었을 때 조용히 깨진다.
- **리스너가 만든 것을 리스너가 갖고 있지 않다** — 이 코드는 지역 변수로 만들고 컨텍스트 속성에 넣은 뒤 아무것도 필드에 남기지 않는다. 그래서 `contextDestroyed` 를 나중에 채우려면 **속성에서 다시 꺼내야** 한다(`sce.getServletContext().getAttribute(...)`). 만든 곳과 정리할 곳이 같은 클래스인데도 서로 문자열 키를 거쳐야 하는 형태이고, 이것이 「넣어 주는 것」이 아니라 「놓아 두는 것」의 대가다 → [[variable-scope]] · [[dependency-injection]]
- **「데이터베이스 연결 풀을 설정하거나 해제」가 실제로 하는 일과 반쯤 다르다** — 이 코드는 풀을 직접 만들지 않는다. MyBatis 설정 파일(`mybatis-config.xml`)이 데이터소스를 정하고, 풀은 **첫 커넥션 요청 때** 그 설정에 따라 채워진다. 그래서 리스너가 하는 일은 「풀을 만든다」가 아니라 **「풀을 만들 준비를 한 객체를 만들어 앱 스코프에 둔다」**이고, 실제로 DB 에 붙는 시점은 첫 요청이다. 「앱이 뜰 때 DB 연결을 확인했다」로 읽으면 **DB 가 죽어 있어도 서버가 정상으로 뜬다**는 사실을 놓친다 → [[mybatis]] · [[jdbc]]
- **필기의 첫 줄에 낱말이 겹쳐 있다** — 「리스너는 는 자바 웹 애플리케이션에서…」. 내용은 그대로 두었다.

## 함께 보는 개념

- [[servlet-context]] — 리스너가 만든 것을 놓는 자리
- [[servlet-container]] — 이 객체를 찾아 부르는 쪽
- [[web-component]] — 이 개념이 속한 셋
- [[servlet-lifecycle]] — 「앱마다 한 번」과 「서블릿마다 한 번」이 갈리는 축
- [[servlet-filter]] — 요청 흐름 위에 서는 쪽
- [[main-method]] — 이 메서드가 대신 서는 자리
- [[dependency-injection]] — 만든 것을 어떻게 전하나
- [[proxy-pattern]] · [[thread-local]] · [[dynamic-proxy]] — 이 부팅 코드가 조립하는 것들
- [[mybatis]] · [[sql-session]] — 초기화 대상
- [[singleton-pattern]] · [[instance]] — 「앱에 하나」가 자리로 정해지는 방식
- [[connection-lifetime-mismatch]] — 정리하지 않은 것이 쌓이는 문제
- [[exception-handling]] — 삼킨 예외가 미루는 실패
- [[observer-pattern]] — 「이벤트가 오면 불린다」의 일반형
- [[annotation]] · [[xml]] — 등록하는 두 방식
- [[tomcat]] — 이 순서를 실제로 도는 서버

## 출처

- [[2024-09-02-Day68]] — 엿새 뒤. 「Listener 만들기」 절이 리스너를 **「객체 상태가 변경되었을 때 보고 받는 옵저버패턴이다」**로 정의해, Day44 에서 손으로 만든 패턴이 규격 안에 이미 있다는 것을 이름으로 잇는다. `web.xml` 의 `<listener>` 태그가 **매핑 없이 등록만 있는** 것도 같은 회차에 나오는데, 이벤트를 받는 것이라 URL 이 필요 없다는 이유는 적혀 있지 않다. 리스너 구현 코드는 이 회차에도 없다
- [[2024-08-27-Day64]] — 「리스너」 절과 「Web Component의 활용 > ServletContextListener」 절이 이 개념이다. 「특정 이벤트가 발생할 때 자동으로 실행되는 객체」·「서블릿 컨테이너에서 발생하는 이벤트에 반응한다」·「주로 애플리케이션, 세션, 또는 요청 수준의 이벤트를 처리」로 정의하고 역할을 셋(리소스 초기화·해제 / 요청 로깅·감사 / 세션 추적) 적었으며, `ServletContextListener` 의 `contextInitialized`·`contextDestroyed` 를 짝으로 설명하고 구동원리를 여섯 단계(`Tomcat.start()` → 컨테이너 실행 → `web.xml`·`@WebListener` 탐색 → 인스턴스화와 `contextInitialized` 호출 → `ServletContextEvent` 전달 → 초기 설정 완료 → 요청 처리 준비)로 적었다. **실습 코드가 프로젝트의 부팅 코드 전체**다 — `mybatis-config.xml` 을 읽어 `SqlSessionFactory` 를 만들고 `SqlSessionFactoryProxy` 를 씌워 `DaoFactory` 에 넘긴 뒤 DAO 셋을 만들어 `ServletContext` 속성 네 개로 올린다. 다만 **소제목이 「정의와 종류」인데 종류가 열거되지 않고**(세 수준의 인터페이스 이름이 없다), **`contextDestroyed` 가 코드에 없어** 정리 없이 재시작될 때 커넥션 풀이 겹치며, `catch (Exception e) { e.printStackTrace(); }` 가 초기화 실패를 삼켜 **기동은 성공하고 첫 요청이 NPE 로 죽는** 형태를 만든다. 여러 리스너의 순서 문제, 컨텍스트마다 한 번이라는 것, 「연결 풀을 설정한다」가 실제로는 첫 요청에 채워진다는 것도 다루지 않았다
