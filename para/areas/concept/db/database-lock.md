---
type: concept
id: database-lock
title: 데이터베이스 락 (읽기락 · 쓰기락)
aliases:
  - 락
  - lock
  - 공유락
  - 배타락
  - FOR UPDATE
  - LOCK IN SHARE MODE
  - 비관적 락
up:
  - 2025-01-07-Day06
  - 2025-01-08-Day07
tags:
  - database
  - 동시성
  - 트랜잭션
---

# 데이터베이스 락 (읽기락 · 쓰기락)

**여러 트랜잭션이 같은 데이터를 동시에 만질 때 순서를 강제하는 장치.** 먼저 잡은 쪽이 놓을 때까지 뒤엣것이 기다린다.

## 정의

두 종류가 있고, **무엇을 막는지**가 다르다.

| | 거는 법 (SQL) | 읽기 | 쓰기 |
|---|---|---|---|
| **읽기락**(공유) | `SELECT ... LOCK IN SHARE MODE` | 된다 | **막힌다** |
| **쓰기락**(배타) | `SELECT ... FOR UPDATE` | 막힌다 | 막힌다 |

```sql
START TRANSACTION;
SELECT * FROM post WHERE id = 1 LOCK IN SHARE MODE;   -- 읽기락

-- 다른 세션에서
SELECT * FROM post WHERE id = 1;      -- 된다
UPDATE post SET username = '홍길순' WHERE id = 1;   -- 대기한다
```

**락은 트랜잭션이 끝날 때 풀린다** — `COMMIT`(또는 롤백)이 곧 해제 시점이다 → [[transaction]]

### JPA 에서 거는 법

```java
@Lock(LockModeType.PESSIMISTIC_READ)    // LOCK IN SHARE MODE
@Lock(LockModeType.PESSIMISTIC_WRITE)   // FOR UPDATE
```

리포지토리 메서드에 붙이면 그 조회가 락을 잡고, **서비스의 `@Transactional` 이 끝날 때 풀린다** → [[declarative-transaction]]

```
트랜잭션 A (락 획득) ──── 작업 ────▶ 종료(락 해제)
트랜잭션 B (락 시도) ─── 대기 ──────────────▶ 실행
```

기다리는 데는 **한도가 있다** — 타임아웃까지 못 잡으면 예외가 난다.

## 왜 중요한가

**「읽고 → 판단하고 → 쓰기」 사이에 남이 끼어드는 문제를 막는다.** 재고를 읽어 1 을 빼고 저장하는 코드가 둘이 동시에 돌면 **하나가 사라진다**(갱신 분실). 읽을 때 쓰기락을 잡으면 그 사이가 보호된다 → [[transaction]]

**그리고 락의 범위와 시간이 곧 동시성이다.** 락을 오래 잡으면 뒤엣것들이 전부 기다리므로, **트랜잭션이 짧아야 한다**는 원칙이 여기서 나온다 → [[connection-lifetime-mismatch]] · [[little-law]]

## 경계와 오해

- **`Thread.sleep(10000)` 을 트랜잭션 안에 두는 것은 실험용이다** — 필기가 락을 관찰하려고 쓴 방법인데, **실제 코드에서는 그것이 곧 장애**다. 락을 잡은 채 오래 머무는 모든 것(외부 API 호출·파일 업로드)이 같은 모양이다 → [[object-storage]]
- **락은 데드락을 만든다** — A 가 1번을 잡고 2번을 기다리는데 B 가 2번을 잡고 1번을 기다리면 둘 다 못 간다. **여러 행을 잠글 때 순서를 정해 두는 것**이 흔한 예방책이다
- **비관적 락이 유일한 답은 아니다** — 여기서 배우는 것은 **먼저 잠그는 방식**(비관적)이다. 충돌이 드물면 버전 컬럼으로 **나중에 확인하는 방식**(낙관적)이 처리량에서 낫다 → [[optimistic-lock]]
- **읽기락은 「읽기만 하니 안전하다」가 아니다** — 두 트랜잭션이 각자 읽기락을 잡고 서로 쓰기를 시도하면 **데드락**이 된다. 공유락이 겹쳐 잡히기 때문이다
- **락은 행 단위가 아닐 수 있다** — 조건에 인덱스가 없으면 더 넓은 범위가 잠긴다. **어떤 질의로 잠갔는지가 무엇이 잠기는지를 정한다** → [[database-index]]
- **`autocommit` 이 켜져 있으면 락을 유지할 수 없다** — 문장 하나가 곧 트랜잭션이라 바로 풀린다. 실험에서 `SET autocommit = 0` 이나 `START TRANSACTION` 을 먼저 하는 이유다 → [[transaction]]

## 함께 보는 개념

- [[transaction]] — 락이 유지되는 단위
- [[declarative-transaction]] — JPA 에서 그 단위를 긋는 표식
- [[transaction-propagation]] — 트랜잭션이 합쳐지면 락도 함께 간다
- [[database-index]] — 잠기는 범위를 정하는 것
- [[thread]] — 동시에 도는 것들
- [[connection-pool-sizing-formula]] — 대기가 길어질 때 드러나는 자리
- [[optimistic-lock]] — 잠그지 않고 확인만 하는 반대편

## 출처

- [[2025-01-08-Day07]] — 하루 뒤. **이 방식에 「비관적」이라는 이름이 붙는다** — 짝이 되는 낙관적 락이 나오면서다. 「데이터 접근 시 락을 걸고 데이터를 읽음 / 락 권한을 가진 트랜잭션이 끝나기 전까지 다른 트랜잭션은 대기 상태에 남는다」로 이 방식의 성질을 다시 정리했고, 그 대비로 **대기가 없는 대신 실패가 있는** 쪽이 놓인다. 「JPA 에서만 통용되는 개념으로 DB 에서는 낙관적락을 직접적인 지원은 없다」는 한 줄이 **둘이 서로 다른 층의 장치**라는 것도 짚는다 → [[optimistic-lock]]
- [[2025-01-07-Day06]] — 「락」 절이 **SQL 과 JPA 양쪽에서 같은 것을 걸어 본다.** 읽기락은 `LOCK IN SHARE MODE` 로 걸고 **조회는 되고 `UPDATE` 는 막히는 것**을 스크린샷으로 확인했고, 쓰기락은 `SET autocommit = 0` → `SELECT ... FOR UPDATE` → `UPDATE` → `COMMIT` 순서로 **잠그고 푸는 전 과정**을 적었다. 스프링 쪽은 `@Lock(LockModeType.PESSIMISTIC_READ/WRITE)` 를 리포지토리에 붙이고 **여덟 단계로 흐름을 적어** 락이 `@Transactional` 의 시작·종료와 함께 잡히고 풀린다는 것을 짚었다 — `Thread.sleep(10000)` 으로 락을 붙들어 두 번째 트랜잭션이 대기하는 것을 눈으로 본 것이 이 실험의 요점이다. 「타임아웃(기본 값)까지 대기 후 락을 획득하지 못하면 예외 발생」도 적혀 있다. 다만 데드락과 낙관적 락은 다루지 않았고, 「락의 개념」 세 줄 중 둘째·셋째가 같은 문장의 반복이다
