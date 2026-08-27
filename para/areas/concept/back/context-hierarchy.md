---
type: concept
id: context-hierarchy
title: 루트 컨테이너와 서블릿 컨테이너 (Context Hierarchy)
aliases:
  - 루트 컨테이너
  - RootConfig
  - ContextLoaderListener
  - context hierarchy
up:
  - 2024-10-14-Day92
tags:
  - spring
  - web
  - 설계
---

# 루트 컨테이너와 서블릿 컨테이너 (Context Hierarchy)

**스프링 웹 애플리케이션의 IoC 컨테이너는 하나가 아니라 부모-자식 둘 이상일 수 있다.** 공유할 것은 부모에, 그 서블릿만의 것은 자식에 둔다.

## 정의

```
        [루트 컨테이너]          ← ContextLoaderListener 가 만든다
         서비스 · DAO · DataSource
            ↑            ↑
    [app 컨테이너]  [admin 컨테이너]   ← DispatcherServlet 마다 하나씩
     app 컨트롤러      admin 컨트롤러
```

**자식은 부모의 빈을 볼 수 있고, 부모는 자식의 빈을 볼 수 없다.**

`DispatcherServlet` 을 둘 등록하는 구성이 이 구조를 필요하게 만든다.

```java
// app 쪽 — 루트 설정을 여기서 정한다
@Override protected Class<?>[] getRootConfigClasses()    { return new Class<?>[] {RootConfig.class}; }
@Override protected Class<?>[] getServletConfigClasses() { return new Class<?>[] {AppConfig.class}; }
@Override protected String[]   getServletMappings()      { return new String[] {"/app/*"}; }

// admin 쪽 — 루트는 이미 만들어졌으므로 null
@Override protected Class<?>[] getRootConfigClasses()    { return null; }
@Override protected Class<?>[] getServletConfigClasses() { return new Class<?>[] {AdminConfig.class}; }
@Override protected String[]   getServletMappings()      { return new String[] {"/admin/*"}; }
```

**스캔 범위를 갈라 두는 것이 짝을 이룬다.**

```java
@ComponentScan(value = "bitcamp",
    excludeFilters = @Filter(type = FilterType.REGEX, pattern = "bitcamp.web.*"))
public class RootConfig {}        // 웹 계층을 뺀 나머지 전부

@ComponentScan("bitcamp.web.app")   public class AppConfig {}
@ComponentScan("bitcamp.web.admin") public class AdminConfig {}
```

**루트에서 `bitcamp.web.*` 을 빼는 것이 이 구성의 핵심**이다 — 안 빼면 컨트롤러가 양쪽에 두 번 만들어진다 → [[stereotype-annotation]]

## 왜 중요한가

**공유와 격리를 동시에 얻는다.** 서비스·DAO·`DataSource` 는 앱과 관리자가 같은 것을 써야 하고, 컨트롤러와 뷰 설정은 서로 달라야 한다. 컨테이너를 하나만 두면 둘 중 하나를 포기해야 한다 → [[ioc-container]]

**그리고 「빈이 안 보인다」의 대부분이 이 구조에서 나온다.** 컨트롤러(자식)가 서비스(부모)를 주입받는 것은 되지만 그 반대는 안 된다. **방향이 한쪽뿐**이라는 것을 모르면 원인을 못 찾는다 → [[autowired]]

## 경계와 오해

- **루트 컨테이너는 필수가 아니다** — `getRootConfigClasses()` 가 `null` 이면 `ContextLoaderListener` 자체를 안 만든다. `DispatcherServlet` 하나만 쓰는 애플리케이션은 **자식 컨테이너 하나로 충분**하고, 실제로 대부분 그렇게 쓴다 → [[servlet-container-initializer]]
- **같은 클래스가 양쪽에 스캔되면 빈이 둘이 된다** — 오류가 아니라 **조용히 둘**이다. 싱글턴이라고 믿은 서비스가 둘이면 캐시나 상태가 갈린다 → [[bean-scope]]
- **부모가 자식을 못 본다는 것이 제약이 된다** — 루트에 있는 무언가가 컨트롤러를 참조해야 하는 설계라면 그 구조가 틀린 것이다. **의존 방향이 곧 계층 방향**이어야 한다 → [[coupling]]
- **`ContextLoaderListener` 는 서블릿이 아니라 리스너다** — 애플리케이션이 시작·종료될 때 불리는 것이라, 요청과 무관하게 컨테이너를 세우고 닫는다 → [[servlet-listener]] · [[servlet-context]]
- **웹 계층을 스캔에서 빼는 것은 규칙이 아니라 우리가 세우는 규약이다** — 패키지 이름(`bitcamp.web.*`)에 기대므로, 패키지를 옮기면 **필터가 조용히 안 맞게 된다** → [[package]]

## 함께 보는 개념

- [[ioc-container]] — 이 계층을 이루는 단위
- [[dispatcher-servlet]] — 자식 컨테이너를 받는 것
- [[servlet-container-initializer]] — 이 계층을 설정하는 자리
- [[servlet-listener]] — 루트 컨테이너를 세우는 장치
- [[autowired]] — 주입이 계층을 따라 가능한지의 문제
- [[stereotype-annotation]] — 스캔 범위를 가르는 표식

## 출처

- [[2024-10-14-Day92]] — 「1 ContextLoaderListener & 2 DispatcherServlet 설정하기」 절이 이 구조를 **실제로 필요하게 만드는 상황**과 함께 보인다 — `/app/*` 과 `/admin/*` 두 진입점을 두고, 「`ContextLoaderListener` 는 Servlet Container 에서 공용으로 사용하기 때문에 **하나의 Servlet 에서만** `getRootConfigClasses` 를 설정한다」로 규칙을 적었다. `RootConfig` 가 `@ComponentScan(value="bitcamp", excludeFilters = @Filter(REGEX, "bitcamp.web.*"))` 로 웹 계층을 빼고, `AppConfig`·`AdminConfig` 가 각각 자기 패키지만 스캔하는 **세 설정 클래스의 조합**이 코드로 남아 있다. 앞선 절들의 `createRootApplicationContext()` 가 `null` 을 돌려주며 「그러면 `ContextLoaderListener` 를 생성하지 않는다」고 적은 주석도 이 개념의 일부다. 다만 부모-자식 사이에 **주입 방향이 한쪽뿐**이라는 것과, 같은 클래스가 양쪽에 스캔될 때 빈이 둘이 된다는 것은 다루지 않았다
