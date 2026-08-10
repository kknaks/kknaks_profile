---
type: concept
id: declarative-transaction
title: 선언적 트랜잭션 (@Transactional)
aliases:
  - "@Transactional"
  - 선언적 트랜잭션
  - declarative transaction
  - PlatformTransactionManager
  - "@EnableTransactionManagement"
up:
  - 2024-09-26-Day83
  - 2024-09-30-Day85
tags:
  - spring
  - database
  - 트랜잭션
  - 설계
---

# 선언적 트랜잭션 (@Transactional)

**트랜잭션의 경계를 코드가 아니라 표식으로 적는 것.** `commit()`·`rollback()` 을 쓰는 대신 메서드에 `@Transactional` 을 붙이면, 프록시가 그 메서드를 감싸 앞뒤에서 대신 처리한다.

## 정의

세 조각이 맞물려야 동작한다.

| 조각 | 하는 일 |
|---|---|
| `PlatformTransactionManager` | 실제로 커밋·롤백을 거는 것. `DataSourceTransactionManager(ds)` 가 구현 |
| `@EnableTransactionManagement` | **프록시를 자동 생성하게 하는 스위치** |
| `@Transactional` | 어느 메서드가 트랜잭션 단위인지 표시 |

```java
@Bean
public PlatformTransactionManager transactionManager(DataSource ds) {
  return new DataSourceTransactionManager(ds);
}
```

```java
@Transactional
public void add(User user) throws Exception {
  userDao.insert(user);
}
```

동작하는 모양은 이렇다.

```
호출 → [프록시]  트랜잭션 시작
         ↓
      실제 메서드 (userDao.insert ...)
         ↓
       [프록시]  정상 종료면 commit / 예외면 rollback
```

**표식이 코드를 만들지 않는다 — 감싸는 객체를 만든다** → [[dynamic-proxy]] · [[reflective-annotation-access]]

## 왜 중요한가

**업무 로직에서 트랜잭션 코드가 사라진다.** 손으로 쓰면 이런 모양이었다.

```java
con.setAutoCommit(false);
try {
  userDao.insert(user);
  con.commit();
} catch (Exception e) {
  con.rollback();
  throw e;
} finally {
  con.setAutoCommit(true);
}
```

**메서드마다 같은 뼈대가 반복되고, 그중 한 곳에서 `rollback` 을 빠뜨리면 그 자리만 조용히 깨진다.** 표식으로 옮기면 반복이 사라지고, **경계가 어디인지가 한눈에 보인다** → [[transaction]]

그리고 **경계가 [[service-layer]] 에 놓인다는 것이 코드로 드러난다.** Day75 가 「로직과 트랜잭션 제어를 서비스로 분리한다」고 적었던 그 자리에 정확히 이 표식이 붙는다 — 여러 DAO 호출을 하나로 묶는 곳이 서비스이기 때문이다.

## 경계와 오해

- **같은 클래스 안에서 부르면 안 걸린다** — 프록시가 감싸는 것은 **밖에서 들어오는 호출**이다. `this.add()` 처럼 자기 메서드를 직접 부르면 프록시를 지나지 않아 트랜잭션이 시작되지 않는다. **표식은 붙어 있는데 아무 일도 안 일어나고, 오류도 안 난다** → [[dynamic-proxy]]
- **`@EnableTransactionManagement` 를 빠뜨리면 표식이 장식이 된다** — 프록시를 만들 사람이 없으므로 `@Transactional` 이 아무 효과가 없다. **역시 조용하다**
- **트랜잭션 매니저와 DAO 가 같은 `DataSource` 를 봐야 한다** — 매니저가 커넥션에 트랜잭션을 걸어 두는데 DAO 가 다른 커넥션을 쓰면 그 작업은 그 트랜잭션 밖이다 → [[data-source]] · [[mybatis-spring]]
- **기본 롤백 조건은 「모든 예외」가 아니다** — 스프링의 기본은 `RuntimeException`·`Error` 에서만 롤백하고, **검사 예외(`Exception`)에서는 커밋한다.** 필기의 코드가 `throws Exception` 인 것이 정확히 그 조건에 걸리는 모양이다 → [[exception-handling]]
- **표식은 「트랜잭션이 필요하다」는 선언이지 「빨라진다」가 아니다** — 경계를 넓게 잡으면 커넥션과 잠금을 오래 붙들어 동시성이 떨어진다. **범위는 좁을수록 좋다** → [[connection-lifetime-mismatch]]
- **읽기만 하는 메서드에도 붙일 수 있다** — 그때는 최적화 힌트에 가깝다. 다만 「조회니까 안 붙인다」와 「조회도 붙인다」가 팀마다 갈리는 자리다

## 함께 보는 개념

- [[transaction]] — 표식이 대신 긋는 경계
- [[dynamic-proxy]] — 표식이 실제로 동작하는 방식
- [[service-layer]] — 이 표식이 붙는 층
- [[data-source]] — 트랜잭션 매니저가 받는 것
- [[mybatis-spring]] — 같은 커넥션을 공유해야 하는 쪽
- [[annotation]] — 표식이 실행 시점에 읽히는 원리
- [[spring-framework]] — 프록시를 만들어 주는 것
- [[transaction-propagation]] — 이 표식의 범위를 정하는 속성

## 출처

- [[2024-09-30-Day85]] — 나흘 뒤. 표식을 붙이는 것만으로 끝나지 않는다는 것이 드러난다 — **서비스가 서비스를 부르면 트랜잭션이 어떻게 되는가**라는 질문이 「Transjaction Propagation」 절로 나오고, 여섯 정책의 표가 그 답이다. 이 절이 나온 계기가 「기존 사진제거의 문제점」이라는 것도 중요하다: DB 수정과 스토리지 삭제가 따로 놀아 엉뚱한 파일이 지워지는 문제인데, **필기의 해법(같은 트랜잭션으로 묶기)은 DB 쪽만 묶는다** → [[transaction-propagation]] · [[object-storage]]
- [[2024-09-26-Day83]] — 「transjection 설정」 절이 `DataSourceTransactionManager` 를 `PlatformTransactionManager` 타입 빈으로 등록하고, 「transjection 적용」 절이 `@Transactional` 을 서비스 메서드에 붙인 예와 함께 **「`AppConfig` 에 `@EnableTransactionManagement` 를 붙여서 Proxy 클래스를 자동 생성하게 한다」**를 적었다 — **프록시가 만들어진다는 것을 필기가 명시한 것**이 이 개념에서 가장 중요한 문장이다. 앞 회차에서 트랜잭션 프록시를 손으로 만들어 봤기 때문에(→ [[dynamic-proxy]]) 「자동 생성」이 무엇을 대신하는지 알고 읽게 된다. 다만 자기 호출에서 안 걸린다는 것, 검사 예외에서는 기본이 커밋이라는 것은 다루지 않았고, 예시 메서드가 `throws Exception` 이라 그 함정 위에 서 있다
