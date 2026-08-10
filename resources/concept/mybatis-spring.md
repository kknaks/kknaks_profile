---
type: concept
id: mybatis-spring
title: MyBatis-Spring 연동
aliases:
  - mybatis-spring
  - SqlSessionFactoryBean
  - SqlSessionTemplate
  - "@MapperScan"
  - getMapper
up:
  - 2024-09-26-Day83
tags:
  - spring
  - database
  - MyBatis
---

# MyBatis-Spring 연동

**MyBatis 의 설정과 객체 생성을 스프링 컨테이너에 넘기는 연결 라이브러리.** `mybatis-config.xml` 과 손으로 만든 팩토리가 하던 일이 `@Bean` 메서드로 옮겨 온다.

```groovy
implementation 'org.mybatis:mybatis-spring:2.1.2'
```

## 정의

세 단계로 쌓인다.

### 1. `SqlSessionFactoryBean` — 설정을 코드로 옮긴다

```java
@Bean
public SqlSessionFactory sqlSessionFactory(DataSource ds) throws Exception {
  SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
  factoryBean.setDataSource(ds);
  factoryBean.setTypeAliasesPackage("bitcamp.myapp.vo");
  factoryBean.setMapperLocations(appCtx.getResources("classpath:mappers/*Mapper.xml"));
  return factoryBean.getObject();
}
```

`mybatis-config.xml` 의 `<environment>`·`<typeAliases>`·`<mappers>` 세 자리가 각각 위의 세 메서드가 된다 → [[mybatis]] · [[type-alias]] · [[data-source]]

### 2. `SqlSessionTemplate` — 세션을 대신 열고 닫는다

```java
@Bean
public SqlSessionTemplate sqlSessionTemplate(SqlSessionFactory sqlSessionFactory) {
  return new SqlSessionTemplate(sqlSessionFactory);
}
```

`SqlSession` 을 직접 열고 닫던 것을 대신하며, **진행 중인 트랜잭션이 있으면 그 커넥션을 따라간다** → [[sql-session]] · [[declarative-transaction]]

### 3. `getMapper` — 인터페이스만으로 DAO 를 얻는다

```java
@Bean
public UserDao createUserDao(SqlSessionTemplate sqlSessionTemplate) {
  return sqlSessionTemplate.getMapper(UserDao.class);
}
```

`UserDao` 는 **인터페이스뿐이고 구현 클래스가 없다.** 매퍼 XML 의 `namespace` 를 그 인터페이스의 **풀 패키지 이름**으로 맞춰 두면, MyBatis 가 그 둘을 이어 구현체를 만들어 준다 → [[dynamic-proxy]] · [[dao-pattern]]

```xml
<mapper namespace="bitcamp.myapp.dao.BoardDao">
```

이 `@Bean` 메서드들을 DAO 마다 쓰는 것도 지겨워지면 한 줄로 줄인다.

```java
@MapperScan("bitcamp.myapp.dao")
```

## 왜 중요한가

**설정 파일이 하나 사라진다.** 접속 정보·타입 별칭·매퍼 위치가 전부 `AppConfig` 로 모이면, **설정이 두 언어(XML·자바)로 갈려 있던 것이 하나가 된다.** 어느 파일을 봐야 하는지 헤매지 않는다 → [[ioc-container]]

**그리고 트랜잭션이 MyBatis 를 관통한다.** `SqlSessionTemplate` 이 스프링의 트랜잭션 커넥션을 따라가기 때문에, 서비스에 `@Transactional` 을 붙이면 **그 안의 여러 DAO 호출이 한 트랜잭션이 된다.** 이 연결 라이브러리가 실제로 하는 가장 중요한 일이 이것이다 → [[transaction]]

## 경계와 오해

- **`namespace` 를 풀 패키지 이름으로 바꾸는 것이 필수 조건이다** — `getMapper(UserDao.class)` 가 매퍼를 찾는 열쇠가 그 이름이다. 예전처럼 `namespace="UserDao"` 로 두면 **매퍼를 못 찾아 실행 시점에 터진다** → [[mybatis]]
- **`@Param` 의 패키지가 바뀐다** — 직접 만들어 쓰던 애노테이션을 MyBatis 것으로 교체해야 한다. `@Component` 교체와 같은 종류의 이행이다 → [[stereotype-annotation]]
- **`SqlSessionTemplate` 은 스레드에 안전하다** — 하나를 만들어 모든 DAO 가 공유한다. `SqlSession` 을 그렇게 쓰면 안 되는 것과 반대라 헷갈리는 자리다 → [[sql-session]] · [[thread]]
- **`@MapperScan` 은 편의이지 다른 기능이 아니다** — `@Bean` 으로 하나씩 등록한 것과 결과가 같다. 다만 **어떤 인터페이스가 DAO 로 등록됐는지가 코드에서 안 보이게 된다** → [[ioc-container]]
- **`SqlSessionFactoryBean` 과 `SqlSessionFactory` 는 다른 타입이다** — 앞은 **뒤를 만들어 주는 것**이라 `getObject()` 로 꺼내야 한다. 필기의 코드가 그 호출을 정확히 하고 있다
- **`appCtx` 가 어디서 오는지가 이 코드에 없다** — 매퍼 위치를 읽으려면 애플리케이션 컨텍스트가 필요한데, 필기의 조각에는 그 필드 선언이 빠져 있다

## 함께 보는 개념

- [[mybatis]] — 이 연동이 감싸는 대상
- [[sql-session]] — `SqlSessionTemplate` 이 대신하는 것
- [[data-source]] — 팩토리가 받는 접속 통로
- [[declarative-transaction]] — 같은 커넥션을 공유하는 짝
- [[dao-pattern]] — 인터페이스만 남는 층
- [[dynamic-proxy]] — 구현 없는 인터페이스가 동작하는 원리
- [[ioc-container]] — 이 모든 것을 담는 곳

## 출처

- [[2024-09-26-Day83]] — 「MyBatis Spring」 절 전체가 `mybatis-spring:2.1.2` 의존성부터 `@MapperScan` 까지 **설정 이행의 전 과정**을 코드로 남겼다. `SqlSessionFactoryBean` 에 `setDataSource`·`setTypeAliasesPackage`·`setMapperLocations` 세 줄이 붙는 것이 `mybatis-config.xml` 의 세 자리와 그대로 대응하고, 「Dao 생성」 절이 **「Mapper에 UserDao에 대한 정보는 풀 패키지 명으로 작성한다」**와 `<mapper namespace="bitcamp.myapp.dao.BoardDao">` 예를 적어 인터페이스와 XML 을 잇는 열쇠를 짚었다. `getMapper(UserDao.class)` 를 DAO 마다 `@Bean` 으로 쓴 뒤 마지막 절에서 `@MapperScan("bitcamp.myapp.dao")` 한 줄로 줄이는 순서까지 나온다. 다만 `SqlSessionTemplate` 이 트랜잭션 커넥션을 따라간다는 것 — 이 라이브러리를 쓰는 가장 큰 이유 — 은 적혀 있지 않고, `appCtx` 의 출처도 코드에 없다
