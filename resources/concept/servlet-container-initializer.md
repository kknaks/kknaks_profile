---
type: concept
id: servlet-container-initializer
title: ServletContainerInitializer (코드로 서블릿 등록하기)
aliases:
  - ServletContainerInitializer
  - WebApplicationInitializer
  - AbstractAnnotationConfigDispatcherServletInitializer
  - SPI
  - META-INF/services
up:
  - 2024-10-14-Day92
tags:
  - web
  - spring
  - servlet
  - 프레임워크
---

# ServletContainerInitializer (코드로 서블릿 등록하기)

**서블릿 컨테이너가 시작할 때 라이브러리 안의 클래스를 찾아 불러 주는 규약.** 이 통로가 있어서 [[web-xml]] 없이 자바 코드로 서블릿을 등록할 수 있다.

## 정의

컨테이너가 시작할 때 하는 일이 정해져 있다.

```
1. 서블릿 컨테이너 시작
2. /WEB-INF/lib/*.jar 를 뒤진다
3. 각 jar 의 /META-INF/services/javax.servlet.ServletContainerInitializer 파일을 찾는다
4. 그 파일에 적힌 구현체 클래스 이름을 읽는다
5. 인스턴스를 만들고 onStartup() 을 호출한다
6. 그 구현체가 「보고받고 싶은 타입」을 선언해 두었으면, 해당 클래스들을 찾아 매개변수로 넘긴다
```

**「파일에 클래스 이름을 적어 두면 찾아 준다」는 것이 SPI 방식**이다 — 라이브러리가 자기를 등록하는 표준 통로이고, 서블릿 명세만의 것이 아니다 → [[classpath]] · [[reflective-instantiation]]

스프링은 이 통로에 `SpringServletContainerInitializer` 를 올려 두고, **그것이 다시 우리 클래스를 부른다.**

```
톰캣 → SpringServletContainerInitializer.onStartup(WebApplicationInitializer 구현체 목록)
        → 우리가 만든 WebApplicationInitializer.onStartup(servletContext)
```

### 추상화 사다리

같은 일을 하는 네 단계가 있고, **위로 갈수록 우리가 쓸 코드가 줄어든다.**

| 방식 | 우리가 해야 하는 일 |
|---|---|
| `WebApplicationInitializer` 구현 | 컨테이너 생성 · `refresh()` · `DispatcherServlet` 생성 · `addServlet` · 매핑 **전부** |
| `AbstractContextLoaderInitializer` 상속 | 루트 컨테이너만 돌려주면 `ContextLoaderListener` 등록은 대신 해 준다 |
| `AbstractDispatcherServletInitializer` 상속 | 루트·서블릿 컨테이너와 **URL 매핑**만 돌려준다 |
| `AbstractAnnotationConfigDispatcherServletInitializer` 상속 | **설정 클래스와 매핑만** 돌려준다. 컨테이너 생성 코드가 아예 없다 |

가장 아래 단계의 코드가 이렇다.

```java
public class WebInit extends AbstractAnnotationConfigDispatcherServletInitializer {
  @Override protected Class<?>[] getRootConfigClasses()    { return null; }
  @Override protected Class<?>[] getServletConfigClasses() { return new Class<?>[] {AppConfig.class}; }
  @Override protected String[]   getServletMappings()      { return new String[] {"/app/*"}; }
  @Override protected String     getServletName()          { return "app"; }
}
```

**빈칸을 채우는 형태**로 바뀌었다는 것이 핵심이다 — 순서와 절차는 부모가 갖고 우리는 값만 준다 → [[template-method-pattern]]

## 왜 중요한가

**설정 파일이 사라지고 그 자리를 자바 코드가 받는다.** `web.xml` 에 `<servlet>`·`<servlet-mapping>`·`<listener>` 를 적던 것이 클래스 하나가 되고, **컴파일러의 검사를 받는다** → [[web-xml]] · [[java-config]]

**그리고 「어떻게 스프링이 시작되는가」의 답이 여기 있다.** 스프링 부트에서도 그 시작점만 다를 뿐 구조는 같다 — 프레임워크가 컨테이너의 규약에 자기를 끼워 넣고, 다시 우리 클래스를 부른다. **부르는 쪽이 계속 위에 있다** → [[ioc-container]]

## 경계와 오해

- **`onStartup()` 을 오버라이딩하면 반드시 `super.onStartup()` 을 불러야 한다** — 필기가 두 번 강조한 자리다. 부모가 하던 등록 절차가 통째로 그 안에 있어서, 안 부르면 **서블릿이 아예 등록되지 않는다** → [[method-overriding]]
- **`getServletName()` 을 안 고치면 이름이 `"dispatcher"` 로 고정이다** — `DispatcherServlet` 을 **둘 이상 등록할 때는 반드시 다르게** 해야 한다. 하나만 쓸 때는 드러나지 않는 제약이다
- **`createRootApplicationContext()` 가 `null` 이면 `ContextLoaderListener` 가 안 생긴다** — 「비어 있는 컨테이너가 생긴다」가 아니라 **리스너 자체를 만들지 않는다.** 루트 컨테이너를 쓰지 않겠다는 선언이다 → [[context-hierarchy]]
- **`iocContainer.scan("bitcamp")` 을 쓰려면 설정 클래스에 `@Configuration` 이 필요하다** — 클래스를 직접 `register` 할 때는 없어도 되지만, 패키지를 훑게 하면 무엇이 설정 클래스인지 알려 줄 표식이 있어야 한다 → [[java-config]]
- **SPI 파일 이름이 곧 인터페이스의 전체 이름이다** — `/META-INF/services/javax.servlet.ServletContainerInitializer` 라는 **경로 자체가 계약**이다. 오타가 나면 아무 일도 안 일어나고 오류도 없다(필기의 본문에도 `SerlvetContainerInitializer` 로 잘못 적혀 있다)
- **`setLoadOnStartup(1)` 은 여전히 필요하다** — 등록 방식이 코드로 바뀌었을 뿐, 서블릿을 미리 만들지 말지는 같은 결정이다 → [[load-on-startup]]

## 함께 보는 개념

- [[web-xml]] — 이 방식이 대체하는 설정 파일
- [[dispatcher-servlet]] — 등록 대상
- [[context-hierarchy]] — 루트·서블릿 컨테이너의 관계
- [[template-method-pattern]] — 추상 클래스들이 취하는 형태
- [[servlet-container]] — 이 규약을 실행하는 주체
- [[java-config]] — 설정 클래스를 넘기는 자리
- [[load-on-startup]] — 등록할 때 함께 정하는 것

## 출처

- [[2024-10-14-Day92]] — 「Servlet 등록」 절이 **같은 일을 다섯 단계로 다시 쓰며 추상화가 올라가는 과정**을 전부 코드로 남겼다. 첫 절이 컨테이너의 부팅 순서 여섯 걸음(`/WEB-INF/lib/*.jar` → `/META-INF/services/...` → 구현체 인스턴스 → `onStartup()`)을 적어 **어떻게 라이브러리 코드가 불려지는지**를 밝히고, 이어 스프링이 그 자리에 `SpringServletContainerInitializer` 를 두고 다시 `WebApplicationInitializer` 를 부르는 두 단계 구조를 보인다. 그 다음 `AbstractContextLoaderInitializer` → `AbstractDispatcherServletInitializer` → `AbstractAnnotationConfigDispatcherServletInitializer` 로 가며 **직접 쓰던 코드가 오버라이드 메서드 넷으로 줄어드는 것**이 나란히 놓여 있다. 주석으로 「원래의 메서드를 반드시 호출해줘야 한다」·「여러 개의 DispatcherServlet 을 등록할 것이라면 반드시 이름을 다르게」 같은 실전 주의가 붙어 있는 것도 이 노트의 값이다. 다만 SPI 라는 이름은 나오지 않고, 본문의 파일 경로는 `SerlvetContainerInitializer`·`/META-INF/service/` 로 두 군데 오기가 있다
