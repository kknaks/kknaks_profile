---
type: concept
id: role-based-entity
title: 역할 기반 엔티티 (도메인마다 다른 관점)
aliases:
  - 역할 기반 엔티티
  - 모듈 분리
  - Author 엔티티
up:
  - 2025-02-19-Day32
tags:
  - 설계
  - 도메인
  - 결합도
---

# 역할 기반 엔티티 (도메인마다 다른 관점)

**같은 테이블을 도메인마다 자기에게 필요한 만큼만 보는 엔티티로 따로 정의하는 것.** 회원 테이블을 게시글 모듈에서는 「작성자」로만 본다.

## 정의

게시글은 회원의 모든 것이 필요하지 않다 — **글쓴이라는 역할**만 필요하다.

```java
// post 모듈 안에서
public class Post extends BaseEntity {
  private String title;
  private String content;

  @ManyToOne
  private Author author;        // Member 가 아니라 Author
}
```

```java
@Entity
@Table(name = "member")         // 테이블은 같다
public class Author extends BaseEntity {
  @Column(name = "nickname")
  private String writer;        // 필요한 컬럼만
}
```

**테이블은 하나인데 엔티티가 둘**이다 — `member` 테이블을 회원 모듈은 `Member` 로, 게시글 모듈은 `Author` 로 본다 → [[persistence-context]] · [[data-modeling]]

### 로직도 따라간다

게시글 수를 세는 일을 게시글 서비스가 회원 서비스를 불러 처리하면 종속이 생긴다. **그 로직을 `Author` 안으로 옮기면** 게시글 모듈은 회원 모듈을 몰라도 된다.

```java
@Table(name = "member")
public class Author extends BaseEntity {
  @Column(columnDefinition = "BIGINT default 0")
  @Setter(PRIVATE)
  private long postsCount;

  public void increasePostsCount() { postsCount++; }   // 데이터 옆에 동작을 둔다
}
```

→ [[encapsulation]] · [[cohesion]]

## 왜 중요한가

**모듈을 나누려면 「무엇을 아는가」를 줄여야 한다.** 게시글 모듈이 `Member` 전체를 알면 회원 모듈이 바뀔 때마다 함께 흔들린다. **필요한 만큼만 보는 타입**을 두면 그 연결이 가늘어진다 → [[coupling]] · [[interface-segregation-principle]]

**그리고 이것이 마이크로서비스로 가는 준비 단계다.** 나중에 프로세스를 나눌 때 **이미 서로 조금만 알고 있으면** 자를 자리가 분명하다 → [[microservice-architecture]]

## 경계와 오해

- **필기가 그 한계를 스스로 적었다** — 「복잡한 엔티티를 다른 도메인에서 사용할 때 복잡도가 증가하고 유지보수가 난해해진다」. 같은 테이블을 보는 엔티티가 셋·넷으로 늘면 **어느 것이 진짜인지** 흐려진다
- **쓰기가 여러 곳에서 일어나면 위험하다** — `Member` 와 `Author` 가 같은 행을 각자 고치면 **영속성 컨텍스트가 둘을 다른 객체로 본다.** 읽기 관점을 나누는 것과 쓰기 주체를 나누는 것은 다른 문제다 → [[persistence-context]] · [[optimistic-lock]]
- **테이블 하나에 매달려 있다는 사실은 그대로다** — 진짜로 분리하려면 **데이터도 나눠야** 하는데, 이 방법은 아직 한 DB 안이다. **구조상의 준비이지 분리 자체는 아니다** → [[microservice-architecture]]
- **`@Table(name="member")` 로 이름을 맞추는 것이 전부라 조용히 깨진다** — 회원 모듈이 컬럼 이름을 바꾸면 **컴파일은 되고 실행에서 터진다** → [[database-schema]]
- **역할 이름이 도메인 용어여야 한다** — `Author`·`Reviewer`·`Buyer` 처럼 **그 맥락에서 부르는 이름**일 때 값이 있다. `MemberForPost` 같은 이름이면 관점이 아니라 우회에 가깝다

## 함께 보는 개념

- [[application-event]] — 같은 회차의 다른 분리 방법
- [[coupling]] · [[cohesion]] — 나누는 이유를 재는 축
- [[microservice-architecture]] — 이 준비가 향하는 곳
- [[dto]] — 필요한 것만 담는다는 같은 발상
- [[persistence-context]] — 같은 행을 두 엔티티로 볼 때의 문제
- [[data-modeling]] — 테이블과 엔티티가 1:1 이 아니라는 것

## 출처

- [[2025-02-19-Day32]] — 「역할 기반 엔티티로 종속성 분리하기」 절이 **전환의 두 번째·세 번째 단계**(모듈 → 종속성 분리)를 코드로 보인다. `Post` 가 `Member` 대신 **`Author`** 를 참조하고, 그 `Author` 는 `@Table(name="member")` 로 같은 테이블을 가리키되 `nickname` 하나만 갖는다. 이어서 게시글 수 증가 로직을 `Author.increasePostsCount()` 로 옮겨 **게시글 서비스가 회원 서비스를 부르지 않게** 만든다. 무엇보다 **「역할 기반 엔티티 설계의 한계」 절을 스스로 붙인 것**이 이 노트의 값이다 — 「복잡한 엔티티를 다른 도메인에서 사용할 때 복잡도가 증가하고 유지보수가 난해해진다」로 이 방법의 상한을 적어 두고, 그다음 절에서 스프링 이벤트로 넘어간다 → [[application-event]]
