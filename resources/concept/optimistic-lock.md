---
type: concept
id: optimistic-lock
title: 낙관적 락 (@Version)
aliases:
  - 낙관적 락
  - optimistic lock
  - "@Version"
  - OptimisticLockException
up:
  - 2025-01-08-Day07
tags:
  - database
  - 동시성
  - JPA
---

# 낙관적 락 (@Version)

**잠그지 않고 읽되, 저장할 때 「내가 읽은 뒤로 남이 고쳤나」를 확인하는 방식.** 충돌이 드물다고 **낙관**하고, 실제로 났을 때만 되돌린다.

## 정의

엔티티에 버전 필드를 둔다.

```java
@Entity
public class Post {
    ...
    @Version
    private Long version;
}
```

- 처음 저장될 때 버전이 시작되고
- **수정될 때마다 자동으로 증가**하며
- 커밋 시점에 **읽을 때의 버전과 지금 DB 의 버전을 비교**한다

```sql
UPDATE post SET username = ?, version = 3 WHERE id = 1 AND version = 2
```

**`WHERE` 에 버전이 들어간다** — 그 사이 남이 고쳐 버전이 올라갔으면 **0행이 바뀌고**, JPA 가 그것을 보고 `OptimisticLockException` 을 던진다.

비관적 방식과 나란히 놓으면 이렇다.

| | 비관적 락 | 낙관적 락 |
|---|---|---|
| 언제 막나 | **읽을 때 미리** 잠근다 | 안 잠근다 |
| 충돌을 어떻게 아나 | 애초에 못 들어온다 | **커밋할 때** 버전으로 안다 |
| 기다림 | 뒤엣것이 **대기** | 대기 없음 |
| 충돌 시 | (없음) | **예외 — 되돌리고 다시 해야 한다** |
| 어울리는 곳 | 충돌이 잦다 | 충돌이 드물다 |

**낙관적 락은 DB 기능이 아니다** — 필기가 짚은 대로 「JPA 에서만 통용되는 개념으로 DB 에서는 직접적인 지원이 없다」. 버전 비교를 **`UPDATE` 조건으로 흉내내는 것**이다 → [[persistence-framework]]

## 왜 중요한가

**기다리지 않는다는 것이 처리량을 바꾼다.** 비관적 락은 뒤에 온 요청이 전부 대기하므로 **동시성이 락 유지 시간에 갇힌다.** 충돌이 실제로는 드문 상황(같은 글을 동시에 고치는 일)에서는 **막지 않고 확인만 하는 쪽**이 훨씬 많이 처리한다 → [[database-lock]] · [[little-law]]

**대신 실패를 다뤄야 한다.** 락 방식에서는 성공이 보장되지만, 여기서는 **예외가 정상 흐름의 일부**다 — 재시도하거나 사용자에게 「누군가 먼저 수정했습니다」를 보여 줘야 한다 → [[exception-handling]]

## 경계와 오해

- **낙관적 락이 「더 나은 락」이 아니다** — 충돌이 잦으면 **재시도가 계속 실패**해 오히려 나빠진다. 고르는 기준은 성능 자체가 아니라 **충돌 빈도**다
- **예외가 나면 그 트랜잭션은 끝이다** — 되돌아가므로 **처음부터 다시 읽어** 다시 시도해야 한다. 「예외를 잡고 계속」이 안 되는 종류다 → [[declarative-transaction]]
- **DB 마다 예외 이름이 다르게 나온다** — 필기가 확인한 대로 MariaDB 에서는 `JpaSystemException`/`GenericJDBCException` 으로 감싸여 온다. **`OptimisticLockException` 만 잡으면 못 잡는 경우가 있다** → [[exception-handling]]
- **버전 컬럼은 애플리케이션이 관리한다** — DB 에서 직접 `UPDATE` 하면 버전이 안 올라가고, 그러면 **낙관적 락이 그 변경을 못 본다.** 실험에서 DBeaver 로 버전을 손으로 바꿔 충돌을 만든 것이 역으로 그 사실을 보인다
- **읽기만 하는 트랜잭션은 버전을 안 올린다** — 충돌 감지는 **쓰기**에 대한 것이다. 읽은 값이 낡았는지 알고 싶으면 다른 장치가 필요하다
- **`Thread.sleep` 은 실험 장치다** — 두 트랜잭션이 겹치는 창을 인위로 벌린 것이고, 실제 코드에 들어가면 그 자체가 문제다 → [[database-lock]]

## 함께 보는 개념

- [[database-lock]] — 먼저 잠그는 반대편
- [[transaction]] — 충돌 검사가 일어나는 경계
- [[declarative-transaction]] — 예외가 롤백으로 이어지는 자리
- [[persistence-framework]] — 이 기능을 제공하는 층
- [[exception-handling]] — 충돌이 예외로 오는 것
- [[functional-dependency]] — 데이터 정합성이라는 같은 목적

## 출처

- [[2025-01-08-Day07]] — 「낙관적 락, 비관적 락」 절이 둘을 나란히 정의하고, **「JPA 에서만 통용되는 개념으로 DB 에서는 낙관적락을 직접적인 지원은 없다」**는 첫 줄이 이 개념의 성격을 정확히 짚었다. 구현은 `@Version` 필드 하나이고, 「엔티티가 수정될 때마다 버전이 자동으로 증가한다 / 트랜잭션 충돌 시 `OptimisticLockException` 이 발생한다」로 동작을 적었다. **충돌을 실제로 만들어 본 방법**이 이 회차의 값이다 — 요청을 보내 `Thread.sleep(10_000)` 으로 트랜잭션을 붙들어 둔 사이에 **DBeaver 로 버전을 직접 수정**해 예외를 일으켰고, MariaDB 에서는 `JpaSystemException`/`GenericJDBCException` 으로 나타난다는 것까지 확인했다. 다만 충돌 후 재시도를 어떻게 할지는 다루지 않았고, 「JUnitTest」 절은 제목만 있다
