---
type: concept
id: n-plus-one
title: N+1 문제
aliases:
  - N+1
  - N+1 문제
  - 지연 로딩
  - LAZY
  - EAGER
  - default_batch_fetch_size
up:
  - 2025-01-09-Day08
tags:
  - JPA
  - database
  - 성능
---

# N+1 문제

**목록을 한 번 읽었는데, 각 항목의 연관 데이터를 읽느라 질의가 N 번 더 나가는 것.** 코드에는 반복문 하나뿐이라 **보고도 모르는** 종류의 성능 문제다.

## 정의

```java
List<Post> posts = postRepository.findAll();       // 질의 1번
for (Post post : posts) {
    post.getComments().size();                     // 게시글 수만큼 질의 N번
}
```

```sql
select * from post;                    -- 1
select * from comment where post_id=1; -- +1
select * from comment where post_id=2; -- +1
...
```

**지연 로딩 때문에 생긴다** — 연관을 「쓸 때 읽는다」로 미뤄 두었는데, **반복문 안에서 쓰면 반복만큼 읽는다** → [[persistence-context]]

### 고르는 것들

| | 뜻 | 문제 |
|---|---|---|
| `FetchType.LAZY` | 쓸 때 읽는다 | **N+1** |
| `FetchType.EAGER` | 조회할 때 함께 읽는다 | 안 쓸 것도 읽고, 조인이 얽힌다 |

**둘 다 답이 아니라는 것**이 이 문제의 성격이다. 기본은 LAZY 로 두고, **필요할 때 한 번에 가져오는 방법**을 따로 쓴다.

```yaml
spring:
  jpa:
    properties:
      hibernate:
        default_batch_fetch_size: 100
```

이 설정은 N 번을 **`where post_id in (1,2,3,...)` 로 묶어** 질의 수를 `N/100` 로 줄인다.

## 왜 중요한가

**성능 문제가 코드 모양에 안 드러난다.** `posts.forEach(...)` 는 어디에도 SQL 이 없으므로, **로그를 보지 않으면 질의가 몇 번 나가는지 알 수 없다.** 데이터가 적을 때는 티가 안 나고 **운영에서 커진 뒤** 드러나는 전형적인 자리다 → [[transaction]] 의 로그 관찰이 여기서 다시 쓰인다.

**그리고 ORM 을 쓰는 대가가 무엇인지 보여 준다.** SQL 을 직접 쓰면 조인 한 번으로 끝날 것이 **객체로 다루는 편의**의 뒷면에서 N 번이 된다 → [[persistence-framework]] · [[sql-join]]

## 경계와 오해

- **EAGER 로 바꾸는 것은 해결이 아니다** — 목록 조회에서는 여전히 N 번이 나갈 수 있고(구현에 따라), 무엇보다 **안 쓰는 데이터까지 늘 읽는다.** 「기본은 LAZY」가 권장인 이유다
- **`default_batch_fetch_size` 는 줄이는 것이지 없애는 것이 아니다** — `1 + N` 이 `1 + N/100` 이 된다. **크게 줄지만 여전히 여러 번**이다
- **한 번에 가져오려면 조회 방법을 바꿔야 한다** — 조인해서 함께 읽어 오는 질의를 따로 쓰는 것이 근본 해법이다. **설정이 아니라 질의의 문제**다 → [[sql-join]]
- **컬렉션을 여럿 조인하면 행이 곱해진다** — 한 게시글에 댓글 10, 태그 5 를 함께 조인하면 50행이 온다. **그래서 한 번에 다 가져오는 것도 답이 아니다**
- **DTO 로 필요한 것만 뽑는 방식이 대안이다** — 엔티티를 다 채우지 않고 화면이 쓸 값만 조회하면 이 문제 자체가 안 생긴다 → [[dto]]
- **N+1 은 JPA 만의 것이 아니다** — 반복문 안에서 조회하는 모든 코드가 같은 모양이다. MyBatis 에서도 DAO 를 루프에서 부르면 똑같다 → [[mybatis]]

## 함께 보는 개념

- [[persistence-context]] — 지연 로딩이 나오는 곳
- [[persistence-framework]] — 이 문제가 생기는 층
- [[sql-join]] — 한 번에 가져오는 쪽
- [[dto]] — 필요한 것만 뽑는 대안
- [[database-index]] — 늘어난 질의가 더 비싸지는 자리
- [[little-law]] — 질의 수가 처리량이 되는 축

## 출처

- [[2025-01-09-Day08]] — 「N+1 문제」 절이 **목차 형태로만** 남아 있다 — `LAZY` 아래에 「N+1문제 발생」과 `@OneToMany`, `eager` 아래에 `@ManyToOne` 을 적어 **어느 쪽이 문제를 만드는지**는 짚었다. 뒤쪽 낱줄 메모가 실제 대응을 남겼다: 「`default_batch_fetch_size` 100 옵션 추가」와 「`@ManyToOne(fetch = FetchType.LAZY)` 어노테이션 사용」 — **기본을 LAZY 로 두고 배치 크기로 완화한다**는 실무 조합이다. 다만 왜 그 조합인지, 조인으로 한 번에 가져오는 방법은 적히지 않았고, 절 전체가 설명 없이 항목만 있는 상태다
