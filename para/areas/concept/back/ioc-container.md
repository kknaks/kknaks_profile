---
type: concept
id: ioc-container
title: IoC 컨테이너 (ApplicationContext)
aliases:
  - IoC
  - IOC
  - IoC 컨테이너
  - 제어의 역전
  - Inversion of Control
  - ApplicationContext
  - 빈
  - Bean
up:
  - 2024-09-25-Day82
  - 2024-09-29-Day84
  - 2024-10-01-Day86
  - 2024-10-02-Day87
tags:
  - 설계
  - 프레임워크
  - 생성
---

# IoC 컨테이너 (ApplicationContext)

**객체를 대신 만들어 두고, 필요한 곳에 넣어 주는 저장소.** 애플리케이션이 시작될 때 한 번 채워지고, 그 뒤로는 거기서 꺼내 쓴다. 담긴 객체를 **빈(bean)** 이라 부른다.

## 정의

「제어의 역전」이 가리키는 것은 **`new` 를 부르는 주체가 바뀌는 것**이다.

```
[전]  내 코드가 필요한 객체를 만든다        →  new ProjectDao(...)
[후]  컨테이너가 만들어 두고 내 코드에 넣어 준다  →  주입받는다
```

그래서 [[dependency-injection]] 은 이 컨테이너가 하는 **일**이고, IoC 는 그 일이 뒤집어 놓은 **관계**다.

스프링에서 웹용 컨테이너를 세우는 순서가 넷이다.

```java
AnnotationConfigWebApplicationContext iocContainer = new AnnotationConfigWebApplicationContext();
iocContainer.register(AppConfig.class);   // 설정 클래스를 알려 준다
iocContainer.setServletContext(ctx);      // 서블릿 컨텍스트와 잇는다
iocContainer.refresh();                   // 실제로 빈을 만든다
```

**`refresh()` 전에는 아무 객체도 만들어지지 않는다.** 등록과 생성이 갈려 있어서, 설정을 다 모은 뒤 한 번에 조립한다.

빈이 컨테이너에 들어오는 길이 둘이다.

| 방법 | 모양 | 쓰는 곳 |
|---|---|---|
| 스캔 | `@ComponentScan("bitcamp.myapp")` + 클래스에 `@Component` 계열 | **내가 만든 클래스** → [[stereotype-annotation]] |
| 등록 | 설정 클래스의 `@Bean` 메서드 | **남이 만든 클래스** (`MultipartResolver`, `ViewResolver` 등) |

### 컨테이너가 한 종류가 아니다

| 인터페이스 | 로딩 | 성격 |
|---|---|---|
| `BeanFactory` | **지연**(lazy) — 필요할 때 만든다 | 가장 기본. 메모리에 유리하지만 부가 기능이 적다 |
| `AutowireCapableBeanFactory` | — | **이미 만들어진 객체에 주입**할 수 있다. 주로 내부용 |
| `ApplicationContext` | **즉시**(eager) — 시작할 때 다 만든다 | `BeanFactory` 를 확장. AOP·메시지·이벤트·국제화까지 |

**실제로 쓰는 것은 거의 언제나 `ApplicationContext`** 이고, `BeanFactory` 는 그 밑에 깔린 기본형이다.

`ApplicationContext` 도 **설정을 어디서 읽느냐**로 갈린다.

| 구현 | 설정을 읽는 곳 |
|---|---|
| `FileSystemXmlApplicationContext` | 파일 시스템 경로의 XML (`file://...`) |
| `ClassPathXmlApplicationContext` | 클래스패스의 XML → [[classpath]] |
| `AnnotationConfigApplicationContext` | 자바 설정 클래스 → [[java-config]] |
| `AnnotationConfigWebApplicationContext` | 자바 설정 클래스 + 서블릿 환경 |

## 사용 예시

설정 클래스 하나가 컨테이너의 내용을 정한다.

```java
@ComponentScan("bitcamp.myapp")   // 이 패키지 아래를 훑어 표식 붙은 클래스를 담는다
@EnableWebMvc
public class AppConfig {

  @Bean
  public ViewResolver viewResolver() {   // 스프링이 만든 클래스는 손으로 등록한다
    InternalResourceViewResolver vr = new InternalResourceViewResolver();
    vr.setPrefix("/WEB-INF/jsp/");
    vr.setSuffix(".jsp");
    return vr;
  }
}
```

## 왜 중요한가

**애플리케이션의 객체 그래프가 한 곳에서 정해진다.** 클래스마다 `new` 를 흩어 두면 무엇이 무엇을 쓰는지 코드를 다 읽어야 알 수 있지만, 컨테이너를 쓰면 **설정 클래스와 표식만 보면 된다** → [[object-graph]] · [[coupling]]

그리고 **바꿔 끼우는 것이 코드 수정이 아니라 설정 변경이 된다.** 같은 인터페이스의 다른 구현으로 바꿀 때 쓰는 쪽은 그대로다 → [[dependency-inversion-principle]]

**이 회차의 값은 그것을 이미 만들어 봤다는 데 있다.** 앞 회차에서 직접 만든 `ApplicationContext` 가 하던 일 — 패키지를 훑고, 애노테이션을 읽고, 리플렉션으로 객체를 만들어 맵에 담는 것 — 이 그대로 스프링 것으로 대체된다. **안이 보이는 채로 갈아 끼운다** → [[reflective-annotation-access]] · [[reflective-instantiation]]

## 경계와 오해

- **IoC ≠ DI** — IoC 는 「제어가 뒤집혔다」는 **관계**의 이름이고, DI 는 그것을 이루는 **방법** 중 하나다. 프레임워크가 내 코드를 부르는 것도 IoC 다 → [[dependency-injection]] · [[template-method-pattern]]
- **빈은 기본이 싱글턴이다** — 이름 하나에 객체 하나가 만들어져 모두가 공유한다. 그래서 **빈에 요청별 상태를 두면 안 된다** — 여러 요청이 같은 필드를 만진다 → [[singleton-pattern]] · [[thread]]
- **`@ComponentScan` 은 패키지를 훑는 것이지 클래스를 아는 게 아니다** — 지정한 패키지 **바깥**에 있는 클래스는 표식을 붙여도 안 담긴다. 「분명히 `@Service` 를 붙였는데 없다」의 대부분이 이 자리다
- **`@Bean` 과 `@Component` 는 대상이 다르다** — 내 소스를 고칠 수 있으면 표식을 붙이고(스캔), 라이브러리 클래스처럼 고칠 수 없으면 `@Bean` 메서드로 만들어 등록한다. **둘 다 되는 경우에 아무거나 쓰는 것이 혼란을 만든다**
- **컨테이너가 있다고 `new` 가 사라지지 않는다** — 값 객체(VO·DTO)는 여전히 `new` 로 만든다. 컨테이너에 담을 것은 **수명이 길고 상태가 없는 협력 객체**다
- **같은 타입 빈이 둘이면 주입이 애매해진다** — 인터페이스 하나에 구현이 둘이면 「어느 것을 넣을지」를 정해 줘야 한다. `@Primary` 로 기본을 정하거나, `@Service("name")` 으로 이름을 붙이고 받는 쪽에서 `@Qualifier("name")` 로 고른다. **구현이 하나일 때는 안 보이다가 둘이 되는 날 기동이 실패한다**
- **즉시 로딩이 기본이라는 것이 값이다** — `ApplicationContext` 는 시작할 때 빈을 다 만들므로, **설정이 틀렸으면 첫 요청이 아니라 기동에서 실패한다.** 지연 로딩이 「메모리 효율」로 적히지만 그 대가가 **오류를 나중에 만나는 것**이라, 서버 애플리케이션에서는 대개 즉시 쪽이 맞다
- **빈 설정 파일이라고 빈이 0개가 아니다** — 자바 설정으로 컨테이너를 세우면 애노테이션을 처리할 **컨테이너 자신의 부품들**이 먼저 등록된다. Day86 이 XML(0개)과 `AppConfig`(기본 개수)를 실행 결과로 대조한 자리다 → [[java-config]]
- **웹 애플리케이션에는 컨테이너가 둘일 수 있다** — 루트 컨테이너와 서블릿용 컨테이너가 부모-자식으로 갈리는 구성이 흔하다. 이 회차는 하나만 쓰지만, 「빈이 안 보인다」의 원인이 되는 자리다 → [[dispatcher-servlet]]

## 함께 보는 개념

- [[dependency-injection]] — 이 컨테이너가 하는 일
- [[spring-framework]] — 이 컨테이너를 제공하는 것
- [[stereotype-annotation]] — 스캔이 찾는 표식
- [[dispatcher-servlet]] — 이 컨테이너를 받아 쓰는 서블릿
- [[singleton-pattern]] — 빈의 기본 수명
- [[reflective-instantiation]] — 컨테이너가 객체를 만드는 방법
- [[dependency-inversion-principle]] — 이 배치가 성립시키는 원칙
- [[externalized-configuration]] — 빈에 넣을 값을 파일에서 읽는 자리
- [[java-config]] — 이 컨테이너에 무엇을 담을지 적는 방식
- [[bean-definition]] · [[bean-scope]] · [[factory-bean]] — 빈 하나를 어떻게 적는가

## 출처

- [[2024-10-02-Day87]] — 하루 뒤. **컨테이너에 담기는 빈 하나를 끝까지 파고든 회차**다. 이름(`id`/`name`/별명/익명)·스코프·생성자·세터·참조·컬렉션·팩토리가 XML 예시로 차례로 나오고, 그중 몇 가지가 이 노트의 빈 곳을 채운다 — 「singleton 객체는 IoC 컨테이너가 생성될 때 미리 준비된다」가 즉시 로딩의 실제 모양이고, `getBean(변수.class)` 가 **같은 타입 빈이 여럿이면 실패한다**는 것이 `@Qualifier` 가 필요한 이유의 XML 판이다 → [[bean-definition]] · [[bean-scope]] · [[factory-bean]]
- [[2024-10-01-Day86]] — 사흘 뒤. **컨테이너를 실습이 아니라 개념으로 다시 본다.** 「IOC Cotainer의 종류」가 `BeanFactory`(지연 로딩) · `AutowireCapableBeanFactory` · `ApplicationContext`(즉시 로딩)를 장단점과 함께 갈랐고, 「ApplicationCeontext 종류」가 설정을 읽는 곳에 따라 네 구현을 나열해 **Day82 에서 쓴 `AnnotationConfigWebApplicationContext` 가 그중 하나였다는 것**을 자리매김한다. 「DI컨테이너, IOC컨테이너, Bean컨테이너의 관계」 절이 세 이름이 같은 것을 가리킨다고 정리한 것도 이 노트의 몫이다. 다만 「IoC의 상속관계」 절은 제목만 있고 비어 있다 → [[java-config]]
- [[2024-09-29-Day84]] — 나흘 뒤. 같은 컨테이너에 **설정 파일을 붙이는 자리**(`@PropertySource`)와 **구현이 둘일 때 고르는 법**이 더해진다. 필기가 「하나의 구현체의 여러개의 Service를 사용하려면 `@Primary` 를 지정하거나 구현체 `Service("name")` 과 컨트롤러에 `Qualifier("name")` 을 설정 해야한다」로 짚은 자리인데, 이 회차의 스토리지 서비스는 구현이 하나뿐이라 **문제가 드러나기 전에 답만 적힌 상태**다 → [[externalized-configuration]]
- [[2024-09-25-Day82]] — 「IOC 컨테이너 교체」 절이 직접 만든 `ApplicationContext` 를 지우고 `AnnotationConfigWebApplicationContext` 를 세우는 네 줄(`register` → `setServletContext` → `refresh`)을 그대로 남겼다 — **등록과 생성이 갈려 있다는 것**이 이 코드에 드러난다. 「annotation 교체」 절이 `@ComponentScan("bitcamp.myapp")` 을 「패키지 내에 있는 모든 클래스에서 `@Component`, `@Service`, `@Repository`, `@Controller` 와 같은 애노테이션이 붙은 클래스들을 자동으로 스캔하고 빈으로 등록」으로 설명하고, 「AppConfig 클래스 변경」이 `@Bean` 메서드로 `MultipartResolver`·`ViewResolver` 를 등록하는 두 예를 보인다 — **스캔과 등록 두 길이 한 노트에 나란히 있다.** 다만 빈이 싱글턴이라는 것, IoC 와 DI 의 관계, `refresh()` 가 하는 일은 설명되지 않았고 코드에 `serSevletContext` 오타가 있다
