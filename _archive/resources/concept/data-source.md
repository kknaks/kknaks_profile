---
type: concept
id: data-source
title: DataSource
aliases:
  - DataSource
  - 데이터소스
  - DriverManagerDataSource
  - "@Value"
up:
  - 2024-09-26-Day83
  - 2024-09-29-Day84
tags:
  - database
  - java
  - spring
  - 설정
---

# DataSource

**커넥션을 얻는 방법을 감싼 인터페이스.** 쓰는 쪽은 `getConnection()` 만 알고, 그것이 매번 새로 만든 것인지 풀에서 꺼낸 것인지 모른다.

## 정의

`DriverManager.getConnection(url, user, pw)` 을 직접 부르던 자리를 대신한다 → [[jdbc]]

```java
@Bean
public DataSource dataSource(
    @Value("${jdbc.driver}") String jdbcDriver,
    @Value("${jdbc.url}") String jdbcUrl,
    @Value("${jdbc.username}") String jdbcUsername,
    @Value("${jdbc.password}") String jdbcPassword) {
  DriverManagerDataSource ds = new DriverManagerDataSource();
  ds.setDriverClassName(jdbcDriver);
  ds.setUrl(jdbcUrl);
  ds.setUsername(jdbcUsername);
  ds.setPassword(jdbcPassword);
  return ds;
}
```

**두 가지가 한 자리에서 일어난다.**

1. **접속 정보가 코드 밖으로 나간다** — `${jdbc.url}` 은 설정 파일의 값을 가리키고, `@Value` 가 그 값을 매개변수로 넣어 준다 → [[ioc-container]]
2. **커넥션 획득이 인터페이스 뒤로 숨는다** — `DataSource` 타입으로 받는 쪽은 구현이 무엇인지 모른다 → [[interface]]

## 왜 중요한가

**커넥션을 얻는 전략을 갈아 끼울 수 있게 된다.** `DriverManagerDataSource` 는 부를 때마다 새로 연결하지만, 커넥션 풀 구현으로 바꾸면 미리 만들어 둔 것을 빌려 준다 — **쓰는 코드는 한 줄도 안 바뀐다.** 연결을 만드는 비용이 요청마다 드는 것과 안 드는 것의 차이라 실전에서는 거의 항상 풀을 쓴다 → [[connection-pool-sizing-formula]] · [[little-law]]

**그리고 접속 정보가 소스에서 빠진다.** 계정과 비밀번호가 코드에 박혀 있으면 저장소에 그대로 올라가고, 개발·운영 환경마다 코드를 고쳐야 한다. 설정 파일로 빼면 **같은 빌드 결과물을 여러 환경에 올릴 수 있다** → [[web-application-deployment]]

## 경계와 오해

- **`DriverManagerDataSource` 는 풀이 아니다** — 이름이 `DataSource` 라 풀처럼 보이지만 **매번 새 연결을 연다.** 실습·시험용이고, 운영에 그대로 쓰면 부하가 늘 때 연결 수립 비용과 DB 의 최대 연결 수에서 먼저 막힌다 → [[connection-lifetime-mismatch]]
- **`@Value` 로 들어오는 것은 전부 문자열이다** — `${jdbc.url}` 이 없으면 값이 안 채워지는 게 아니라 **`"${jdbc.url}"` 이라는 글자 그대로** 들어가거나 기동이 실패한다. 오타가 조용히 넘어가는 자리다
- **설정 파일로 뺐다고 비밀이 지켜지지 않는다** — 파일이 저장소에 함께 올라가면 위치만 옮긴 것이다. **저장소 밖에 두는 것**까지 가야 의미가 있다
- **`DataSource` 를 쓰는 쪽은 커넥션을 반드시 닫아야 한다** — 풀에서는 「닫기」가 실제 종료가 아니라 **반납**이다. 안 닫으면 풀이 말라 애플리케이션 전체가 멈춘다 → [[try-with-resources]]
- **트랜잭션 관리자도 이것을 받는다** — 같은 `DataSource` 를 트랜잭션 매니저가 받아 커넥션 단위로 커밋·롤백을 건다. **둘이 다른 DataSource 를 보면 트랜잭션이 안 걸린다** → [[declarative-transaction]]

## 함께 보는 개념

- [[jdbc]] — 이 인터페이스가 감싸는 것
- [[connection-pool-sizing-formula]] — 풀 구현으로 바꿀 때의 문제
- [[ioc-container]] — 이것을 빈으로 만들고 값을 넣어 주는 곳
- [[declarative-transaction]] — 같은 DataSource 를 공유해야 하는 쪽
- [[mybatis-spring]] — 이것을 받아 세션 팩토리를 만드는 쪽
- [[web-application-deployment]] — 환경마다 값이 갈리는 축
- [[externalized-configuration]] — 접속 정보를 파일로 빼는 방법

## 출처

- [[2024-09-29-Day84]] — 사흘 뒤. 같은 `dataSource` 빈이 그대로 다시 나오는데 **읽어 오는 곳이 바뀐다** — `mybatis-config.xml` 이 아니라 `@PropertySource("classpath:config/jdvc.properties")` 가 가리키는 파일이다. 그리고 접속 대상이 로컬 MySQL 에서 **NCP 에 띄운 서버**로 옮겨 가면서, 「접속 정보가 환경마다 다르다」가 실제 문제가 되는 자리다 → [[externalized-configuration]]
- [[2024-09-26-Day83]] — 「dataSource 메서드 생성」 절이 `config.xml` 의 `${jdbc.driver}`·`${jdbc.url}`·`${jdbc.username}`·`${jdbc.password}` 네 값을 `@Value` 로 받아 `DriverManagerDataSource` 를 세우는 `@Bean` 메서드를 그대로 실었다 — **MyBatis 설정 파일에 있던 접속 정보가 스프링 빈의 매개변수로 옮겨 오는 자리**다. 앞 회차들에서 `mybatis-config.xml` 이 들고 있던 것을 스프링이 대신 읽게 되는 이행이라, 이후 `SqlSessionFactoryBean`·`DataSourceTransactionManager` 가 모두 이 하나의 빈을 받아 간다. 다만 `DriverManagerDataSource` 가 커넥션 풀이 아니라는 것, `@Value` 의 값이 없을 때 무슨 일이 나는지는 다루지 않았다
