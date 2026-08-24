---
type: concept
id: spring-boot
title: 스프링 부트 (Spring Boot)
aliases:
  - Spring Boot
  - 스프링 부트
  - starter
  - 스타터
  - application.properties
up:
  - 2024-10-18-Day96
tags:
  - spring
  - 프레임워크
  - 빌드
  - 설정
---

# 스프링 부트 (Spring Boot)

**스프링을 쓰기 위해 매번 쓰던 설정을 기본값으로 밀어 넣은 위층.** 설정 클래스 여러 개가 **속성 파일 한 개**가 되고, 서버가 애플리케이션 안으로 들어온다.

## 정의

### 스타터 — 의존성을 묶음으로 가져온다

```groovy
plugins {
    id 'org.springframework.boot' version '2.7.18'
    id 'io.spring.dependency-management' version '1.1.6'
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-jdbc'
    implementation 'org.mybatis.spring.boot:mybatis-spring-boot-starter:2.3.2'
    runtimeOnly   'com.mysql:mysql-connector-j'
    developmentOnly 'org.springframework.boot:spring-boot-devtools'
}
```

**두 가지가 일어난다.**

- `spring-boot-starter-web` 하나가 스프링 MVC · 잭슨 · **내장 톰캣**을 함께 끌고 온다
- `dependency-management` 플러그인이 **버전을 대신 정해 준다** — 그래서 스타터에 버전이 없다 → [[gradle]] · [[build]]

의존성의 **범위**도 갈린다.

| 범위 | 언제 쓰이나 |
|---|---|
| `implementation` | 컴파일·실행 |
| `runtimeOnly` | 실행할 때만 (JDBC 드라이버) → [[jdbc]] |
| `developmentOnly` | 개발 중에만 (devtools) |
| `annotationProcessor` | 컴파일 시점 코드 생성 → [[annotation]] |
| `testImplementation` | 시험 코드 |

### `application.properties` — 설정 클래스를 대체한다

```properties
server.port=8888
server.servlet.context-path=/app

spring.datasource.url=jdbc:mysql://localhost/final_project
spring.datasource.username=root
spring.datasource.password=1111

mybatis.type-aliases-package=project.tripMaker.vo
mybatis.mapper-locations=/mappers/*Mapper.xml

spring.mvc.view.prefix=/WEB-INF/jsp/
spring.mvc.view.suffix=.jsp

spring.servlet.multipart.max-file-size=10MB
```

**앞 회차들에서 `@Bean` 메서드로 쓰던 것이 한 줄씩으로 접힌다.**

| 예전에 쓰던 것 | 부트의 속성 |
|---|---|
| `DataSource` 빈 + `@Value` 넷 → [[data-source]] | `spring.datasource.*` |
| `SqlSessionFactoryBean` 설정 → [[mybatis-spring]] | `mybatis.*` |
| `InternalResourceViewResolver` 빈 → [[view-resolver]] | `spring.mvc.view.*` |
| `MultipartResolver` 빈 → [[multipart-form-data]] | `spring.servlet.multipart.*` |
| `web.xml` · `WebApplicationInitializer` → [[servlet-container-initializer]] | (필요 없음) |

## 왜 중요한가

**「스프링을 쓰기 시작하는 비용」이 사라진다.** 앞 회차들이 컨테이너를 세우고 서블릿을 등록하고 뷰 리졸버를 만드는 데 쓴 코드가 전부 기본값이 된다 — **그 코드를 이미 써 봤기 때문에** 무엇이 자동으로 되고 있는지 알 수 있다는 것이 이 순서의 값이다 → [[spring-framework]]

**그리고 서버가 라이브러리가 된다.** 내장 톰캣이 의존성으로 들어오므로 **WAR 를 만들어 서버에 올리는 대신 JAR 를 실행**한다. 「배포한다」의 뜻이 바뀌는 자리다 → [[tomcat]] · [[web-application-deployment]]

## 경계와 오해

- **자동 설정은 마법이 아니라 조건부 기본값이다** — 「클래스패스에 이것이 있으면 이 빈을 만든다」는 규칙의 묶음이고, **내가 같은 타입 빈을 만들면 그쪽이 이긴다.** 그래서 문제를 만나면 「무엇이 자동으로 등록됐나」를 볼 수 있어야 한다 → [[ioc-container]]
- **`application.properties` 에 비밀번호를 적으면 저장소에 올라간다** — 이 회차의 코드가 `spring.datasource.password=1111` 을 그대로 적었다. Day84 가 스토리지 키를 홈 디렉토리로 뺐던 것과 **기준이 어긋난 자리**다 → [[externalized-configuration]]
- **스타터에 버전을 안 적는 것은 플러그인 덕분이다** — `io.spring.dependency-management` 가 없으면 버전을 못 찾아 빌드가 실패한다. **버전이 없는 것이 아니라 다른 곳에 있다** → [[gradle]]
- **JSP 를 쓰려면 따로 챙겨야 한다** — 부트의 기본 뷰는 Thymeleaf 쪽이라, JSP 를 쓰려면 `tomcat-embed-jasper` 와 JSTL 을 직접 넣어야 한다. 이 회차의 `build.gradle` 이 정확히 그렇게 했다 → [[jsp]] · [[jstl]]
- **`context-path` 를 바꾸면 모든 링크가 영향을 받는다** — `server.servlet.context-path=/app` 은 애플리케이션 전체 앞에 붙는 경로다. 화면에서 주소를 손으로 적었다면 그때 깨진다 → [[url]]
- **부트를 쓴다고 스프링을 몰라도 되는 것은 아니다** — 기본값이 안 맞는 순간 그 밑의 빈·컨테이너·서블릿 구조를 알아야 한다. **감춘 것이지 없앤 것이 아니다**

## 함께 보는 개념

- [[spring-framework]] — 부트가 얹혀 있는 아래층
- [[externalized-configuration]] — 속성 파일이 하던 일의 확장
- [[gradle]] · [[build]] — 스타터와 버전 관리가 놓이는 자리
- [[servlet-container-initializer]] — 부트가 대신해 주는 부팅 코드
- [[tomcat]] — 의존성으로 들어오는 서버
- [[ioc-container]] — 자동 설정이 채우는 곳
- [[web-application-deployment]] — 배포의 뜻이 바뀌는 축

## 출처

- [[2024-10-18-Day96]] — 실습 프로젝트를 부트로 옮기며 **`build.gradle` 전문과 `application.properties` 전문**을 남겼다. 이 두 파일이 이 개념의 전부다 — 스타터 의존성들(`starter-web`·`starter-jdbc`·`mybatis-spring-boot-starter`)과 `implementation`/`runtimeOnly`/`developmentOnly`/`annotationProcessor`/`testImplementation` 다섯 범위가 한 화면에 있고, 속성 파일에는 **DataSource·MyBatis·ViewResolver·multipart 설정이 각각 두세 줄로** 들어 있다. JSP 를 쓰기 위해 `tomcat-embed-jasper` 와 `javax.servlet:jstl` 을 직접 넣은 것도 그대로 남아 있다. 「config 파일 설정하기」 절이 `RootConfig`·`AppConfig`·`WebApplicationInitializer` 를 **목록으로만 적고 그 아래에 속성 파일을 놓은 것**이 이 이행의 요점을 보인다 — 그 클래스들이 하던 일이 속성으로 옮겨 갔다. 다만 「Spring Boot 란?」과 「dao 파일 바꾸기」 절은 제목만 있고 비어 있으며, 자동 설정이 어떻게 동작하는지는 다루지 않았다. `spring.datasource.password` 가 파일에 그대로 적혀 있다
