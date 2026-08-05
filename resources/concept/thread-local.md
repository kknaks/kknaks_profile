---
type: concept
id: thread-local
title: 쓰레드 로컬 (ThreadLocal)
aliases:
  - ThreadLocal
  - thread local
  - 쓰레드 로컬
  - 스레드 로컬
  - 쓰레드별 저장소
  - 쓰레드 지역 변수
up:
  - 2024-08-23-Day62
  - 2024-08-27-Day64
tags:
  - java
  - 동시성
  - 설계
  - 자원관리
---

# 쓰레드 로컬 (ThreadLocal)

**필드 하나가 쓰레드마다 다른 값을 갖게 하는 것 — 공유 자원을 잠그는 대신 공유를 없애는 방법.** Day62 는 이 낱말을 본문에 한 번도 쓰지 않고 코드로만 쓴다(`sqlSessionThreadLocal.get()`·`.set()`). 필기의 설명은 「스레드 별로 같은 SqlSession 객체를 리턴」 한 줄이고, **그것이 이 도구의 정의 전부**다 → [[thread]] · [[sql-session]]

## 정의

메서드가 셋이고 Day62 는 그중 둘만 쓴다.

| 메서드 | 하는 일 | Day62 |
|---|---|---|
| `get()` | **지금 이 쓰레드**의 값을 꺼낸다. 없으면 `null`(초기값을 주지 않았으면) | 쓴다 |
| `set(v)` | 지금 이 쓰레드의 값으로 `v` 를 둔다 | 쓴다 |
| `remove()` | 지금 이 쓰레드의 값을 지운다 | **없다** — 아래 「경계와 오해」의 첫 항목 |

**세 메서드에 「어느 쓰레드」를 넘기는 인수가 없다는 것이 이 도구의 형태다.** 대상은 언제나 부른 쪽 자신이고, 그래서 **남의 값에 닿을 방법이 아예 없다** → [[parameter-and-argument]]

### 값이 어디 사는가 — `ThreadLocal` 객체가 값을 갖지 않는다

이름이 「쓰레드마다 하나 생기는 변수」처럼 읽히지만 저장 구조는 반대로 되어 있다.

| 무엇이 | 몇 개 | 무엇을 갖나 |
|---|---|---|
| `ThreadLocal` 인스턴스 (필드) | **하나** — 모든 쓰레드가 같은 객체를 본다 | 값이 아니라 **키**다 |
| `Thread` 객체 | 쓰레드마다 하나 | 그 쓰레드의 **맵**(`ThreadLocal` → 값) |

**그래서 `get()` 은 「내 `Thread` 객체가 든 맵에서 이 키로 찾기」다.** 성질 셋이 여기서 곧바로 나온다 — ① 값을 넣지 않은 쓰레드에서는 `null` 이고, ② 다른 쓰레드의 맵에 닿는 경로가 없어 **잠금이 필요 없고**, ③ 그 쓰레드가 죽으면 맵도 함께 없어지지만 **살아 있으면 값도 산다** → [[hash-based-collection]] · [[jvm-stack]] · [[garbage-collection]]

선언은 이렇게 생긴다. **Day62 의 필기에는 이 줄이 없다.**

```java
private final ThreadLocal<SqlSession> sqlSessionThreadLocal = new ThreadLocal<>();
```

담을 타입은 제네릭이 받고(`get()` 이 캐스팅 없이 `SqlSession` 을 돌려주는 이유), 이 필드를 **누가 갖는가**가 「몇 개의 키가 있는가」를 정한다 → [[generics]] · [[static-member]]

## 사용 예시

Day62 는 MyBatis 의 `SqlSessionFactory` 를 대리하는 클래스를 하나 세우고, **`openSession(boolean)` 한 메서드 안에서** 이 도구를 쓴다 → [[proxy-pattern]]

```java
// 나머지는 원래 SqlSessionFactory에 위임을 한다.
 @Override
public SqlSession openSession(boolean autoCommit) {
  SqlSession sqlSession = sqlSessionThreadLocal.get();

  if (sqlSession == null) {
    sqlSession = original.openSession(autoCommit);
  }

  sqlSessionThreadLocal.set(sqlSession);

  return sqlSession;
}
```

**네 줄이 「없으면 만들고 있으면 그대로」라는 캐시 조회의 최소 형태다** — 다른 것은 키가 사람이 준 값이 아니라 **부른 쪽 쓰레드**라는 것뿐이다 → [[caching]]

### 왜 하필 팩토리에 붙였나 — 세션에는 붙일 수 없다

필기의 절 제목이 「Factory Pattern」인데, 이 절이 실제로 정하는 것은 **세션을 어디서 얻는가**다.

| 후보 | 왜 그 자리가 아닌가 / 인가 |
|---|---|
| `SqlSession` 에 씌운다 | **쓰레드마다 달라야 하는 것 자체**라 대리자를 하나 둘 수 없다 |
| 쓰는 쪽(DAO·Command)이 각자 얻는다 | 얻는 자리가 열다섯 곳으로 흩어진다 — 한 곳이 빠지면 그 화면만 다른 세션이다 |
| **`SqlSessionFactory`** | **앱에 하나**이고 세션을 얻는 **모든 호출이 이 문을 지난다** |

**「앱에 하나 + 모든 호출이 지나간다」가 이 도구를 놓을 자리의 조건**이고, MyBatis 의 수명 표에서 그 조건을 만족하는 칸은 팩토리뿐이다 → [[mybatis]] · [[singleton-pattern]]

그래서 부르는 쪽은 세션을 **필드로 들지 않고 그때그때 얻는다.**

```java
// DaoFactory — 핸들러가 SqlSession 대신 SqlSessionFactory 를 든다
public DaoFactory(SqlSessionFactory sqlSessionFactory) {
  this.sqlSessionFactory = sqlSessionFactory;
}
SqlSession sqlSession = sqlSessionFactory.openSession(false);

// Command — 커밋도 같은 문을 지나 얻은 세션에 한다
sqlSessionFactory.openSession(false).commit();
```

**필드에서 지역 변수로 내려온 것이 이 회차의 전부다.** [[thread]] 노트의 「지역 변수는 안전하고 필드는 안전하지 않다」가 여기서 실제 리팩터링이 되고, **필드에 남은 것(`sqlSessionFactory`)은 쓰레드 안전한 것**이다 → [[dynamic-proxy]] · [[variable-scope]]

### 나흘 뒤 Day64 — 「몇 개 만들 것인가」가 답을 얻고, 「언제 지울 것인가」가 청구서가 된다

Day62(2024-08-23)의 프록시가 **나흘 뒤 웹 컨테이너 위로 올라간다.** 부팅 코드에 처음 실물로 보인다.

```java
SqlSessionFactoryProxy sqlSessionFactoryProxy = new SqlSessionFactoryProxy(sqlSessionFactory);
DaoFactory daoFactory = new DaoFactory(sqlSessionFactoryProxy);
...
ctx.setAttribute("sqlSessionFactory", sqlSessionFactoryProxy);
```

**한쪽 걱정이 해소된다.** 위 「경계와 오해」가 「이 필드를 몇 개 만들 것인지가 코드에 적혀 있지 않고(`static final` 도 아니고 생성자도 필기에 없다), 프록시를 두 벌 만들면 한 쓰레드가 세션을 두 개 갖고 커밋 경계가 갈라진다」고 적었는데 — **Day64 는 그것을 리스너의 `contextInitialized` 한 곳에서 만들어 앱 스코프에 올린다.** `static` 한 글자 없이, 싱글톤 코드 없이, **만드는 자리가 하나뿐이라는 것으로** 개수가 정해졌다 → [[servlet-listener]] · [[servlet-context]] · [[singleton-pattern]]

**대신 다른 쪽 청구서가 이 회차에 온다.** 위 「경계와 오해」의 첫 항목이 「쓰레드 풀을 도입하는 순간 이것이 최악의 버그가 된다」로 남겨 둔 것이 **컨테이너가 곧 그 풀**이므로 여기서 실제가 된다.

| Day61·62 (접속마다 `new Thread`) | Day64 (컨테이너 쓰레드) |
|---|---|
| 대화가 끝나면 쓰레드가 죽어 맵도 사라진다 | 쓰레드가 **살아서 다음 요청을 받는다** |
| `remove()` 가 없는 것이 드러나지 않는다 | `get()` 이 **먼저 다녀간 사람의 세션**을 돌려준다 |

**증상까지 세면 이렇다.** 회원 목록 화면을 두 사람이 차례로 열면 두 번째 요청이 같은 쓰레드에 배정될 수 있고, 그러면 첫 번째 사람의 `SqlSession` 을 그대로 쓴다. 그 세션에는 **1차 캐시**가 들어 있으므로 그동안 남이 등록한 회원이 안 보이거나 지운 회원이 계속 보인다 — **화면이 「가끔 옛 데이터를 보여 준다」**로 나타나고, 새로고침하면 다른 쓰레드에 걸려 맞게 나오기도 한다. 그리고 `close()` 가 없으므로 커넥션이 풀로 돌아가지 않는다 — 서로 다른 쓰레드 열 개가 이 화면을 지나가면 MyBatis `POOLED` 의 활성 상한(기본 10)이 차고, 열한 번째는 20초를 기다리다 **먼저 붙어 있던 누군가의 트랜잭션을 강제 롤백**시킨다 → [[connection-lifetime-mismatch]] · [[caching]] · [[transaction]]

**그리고 이번에는 「쓰레드가 곧 죽는다」로 가려질 수도 없다** — 짝이 되는 정리 지점(`contextDestroyed`)도 Day64 의 리스너에 없다 → [[servlet-listener]]

## 왜 중요한가

**잠그지 않고 나눈다.** [[thread]] 노트가 Day48 기준으로 「동기화」 절이 제목만 남았다고 적었는데, 공유 값 문제의 답은 둘이다 — **순서를 정하거나**(`synchronized`) **애초에 나눠 갖거나**. Day62 는 후자를 골랐고, 그러면 대기가 없다. `synchronized` 로 세션을 감쌌다면 접속 100개가 문장 하나씩 줄을 서고, 그것은 성능 문제가 아니라 **트랜잭션이 남의 것과 섞이는 문제를 그대로 남긴다** — 순서를 정해도 커밋 경계는 여전히 하나다 → [[transaction]] · [[universal-scalability-law]]

**시그니처를 하나도 고치지 않고 아래층에 값을 내려보낸다.** 「이 쓰레드의 세션」을 매개변수로 전하려면 Command 인터페이스 → DAO 인터페이스 → 매퍼 호출까지 인수가 하나 늘어야 하고, Day61 이 만든 [[dynamic-proxy]] 는 그 인수를 받을 자리가 없다(`invoke` 는 인터페이스가 선언한 것만 받는다). **그래서 「인수를 늘리지 않고 문맥을 전달하는」 통로가 필요해지고 이 도구가 그 자리다** — 트랜잭션 동기화·요청 컨텍스트·로그 추적 ID 가 프레임워크에서 전부 이렇게 옮겨진다 → [[coupling]] · [[dependency-injection]]

**대신 「보이지 않는 인수」가 생긴다.** `openSession(false)` 를 부르는 코드를 아무리 읽어도 **누가 그 값을 넣었는지**가 안 보이고, 값이 없는 상태로 그 코드에 도달했는지는 실행해 봐야 안다. 매개변수는 컴파일러가 「빠졌다」고 말해 주지만 쓰레드 로컬은 **`null` 로만 말한다** — [[proxy-pattern]] 이 「지금 내가 쥔 것이 무엇인가가 코드에서 사라진다」로 치른 대가와 같은 종류이고, 이 회차는 그 둘을 **한 메서드 안에서** 함께 치른다 → [[encapsulation]]

## 경계와 오해

- **`remove()` 가 없다 — 이 회차에서는 커넥션 누출로, 쓰레드 풀에서는 남의 세션으로 나타난다** — 이 코드에는 `sqlSession.close()` 도 `remove()` 도 없다. ① 세션을 닫지 않으므로 빌린 연결이 **풀로 돌아가지 않는다.** MyBatis 의 `POOLED` 데이터소스는 기본 설정에서 활성 연결 10개가 상한이고 20초를 넘겨 붙들린 연결은 **강제로 회수해 롤백**하므로, 접속 열 개가 다녀간 뒤의 열한 번째 로그인은 20초를 기다리다 붙고 **그때 먼저 붙어 있던 누군가의 트랜잭션이 되돌려진다.** 원인(닫지 않은 세션)과 증상(남의 작업이 사라짐)이 다른 접속에서 나타난다. ② 값을 지우지 않는 쪽은 **이 회차 구조에서는 드러나지 않는다** — Day61 의 서버가 접속마다 `new Thread` 를 만들고 대화가 끝나면 그 쓰레드가 죽으므로 맵도 함께 사라진다. **쓰레드 풀을 도입하는 순간 이것이 최악의 버그가 된다** — 재사용된 쓰레드의 `get()` 이 **먼저 다녀간 클라이언트의 세션**을 돌려주고, 그 세션에는 그 사람의 미확정 트랜잭션과 1차 캐시가 들어 있다. 즉 **이 코드는 「쓰레드가 곧 죽는다」에 기대어 맞고 있고**, [[thread]] 노트가 「쓰레드 풀이 이 회차에 없다」고 적어 둔 것이 여기서는 **결함을 가려 주는 쪽으로** 작용한다 → [[connection-lifetime-mismatch]] · [[try-with-resources]] · [[transaction]]
- **누출의 방향이 직관과 반대다 — 값이 쓰레드를 붙잡는 것이 아니라 쓰레드가 값을 붙잡는다** — 「`ThreadLocal` 변수를 안 쓰면 정리되겠지」로 읽히는데, 맵의 키(`ThreadLocal` 객체)는 약하게 참조되고 **값은 강하게** 참조된다. 그래서 `ThreadLocal` 필드를 버려도 값은 그 쓰레드가 사는 동안 남는다. 정리 시점을 정하는 것은 **`remove()` 를 부르는 코드**뿐이고, 그것이 「작업이 끝나는 자리」에 있어야 한다 — 그 자리가 바로 세션을 닫아야 하는 자리와 같다 → [[garbage-collection]] · [[object-reference]]
- **쓰레드 로컬 ≠ 동기화** — 둘 다 「공유 값이 깨지는 것」을 막지만 방법이 반대다. `synchronized` 는 **하나의 값을 여럿이 순서대로** 쓰게 하고, 이 도구는 **값을 여러 개로 나눠** 순서 문제를 없앤다. 그래서 이 도구로는 **합계·카운터처럼 진짜로 하나여야 하는 값을 다룰 수 없고**(쓰레드마다 자기 합계를 갖게 되어 아무 뜻이 없다), 반대로 세션·연결처럼 **원래 하나일 이유가 없던 것**에만 맞는다. 「쓰레드 로컬을 쓰면 동시성 문제가 사라진다」로 외우면 공유해야 하는 값에 붙이게 된다 → [[thread]]
- **쓰레드 로컬 ≠ 쓰레드마다 필드가 생기는 것** — 필드는 여전히 하나다(위 표). 이 구별이 값을 갖는 이유가 둘이다 — ① 그래서 `remove()` 가 필요하고(필드가 사라지는 것이 아니므로), ② **`ThreadLocal` 객체가 키이므로 그 객체를 두 개 만들면 칸이 두 개**다. Day62 의 이 필드는 프록시의 인스턴스 필드로 보이는데, 프록시를 두 벌 만들면 **한 쓰레드가 세션을 두 개 갖고 커밋 경계가 갈라진다.** 「앱에 하나만 만든다」는 전제가 코드에 적혀 있지 않고(`static final` 도 아니고 생성자도 필기에 없다), 그 전제가 깨지는 것을 컴파일러도 실행도 알려 주지 않는다. **나흘 뒤 Day64 가 이 자리를 닫는다** — 프록시를 만드는 코드가 리스너의 부팅 이벤트 한 곳으로 옮겨져 앱에 하나가 자리로 보장된다(위 「나흘 뒤 Day64」) → [[static-member]] · [[singleton-pattern]] · [[servlet-listener]]
- **캐시가 맞으면 `autoCommit` 인수가 버려진다 — 인수를 받는 메서드가 인수를 무시한다** — 두 번째 호출부터는 `original.openSession(autoCommit)` 을 부르지 않으므로 **그 쓰레드에서 처음 부른 값이 끝까지 이긴다.** 이 프로젝트는 모든 자리가 `false` 라 지금은 드러나지 않지만, 어느 화면이 `openSession(true)` 를 먼저 부르면 그 뒤의 `openSession(false)` 가 **자동 커밋 세션을 돌려주고** 거기서의 `rollback()` 은 되돌릴 것이 없다. 값을 캐시하는 메서드가 인수를 받으면 **「인수는 처음 한 번만 뜻이 있다」는 규칙이 시그니처에 안 보인다** → [[transaction]] · [[caching]]
- **첫 `get()` 이 `null` 이라는 것에 기대고 있다 — 그리고 초기값 람다로는 이 자리를 대신할 수 없다** — `ThreadLocal.withInitial(() -> …)` 을 쓰면 `if (sqlSession == null)` 이 사라진다. 그런데 여기서는 못 쓴다 — **초기값을 만드는 람다는 인수를 받을 수 없어서** `autoCommit` 을 넘길 방법이 없다. 즉 이 `if` 는 게으름이 아니라 **인수를 받는 생성을 지연시키는 유일한 형태**다. 대신 `null` 을 「없음」으로 쓰는 대가는 그대로 남는다 — 값으로 `null` 을 넣어 두는 것과 넣지 않은 것이 구별되지 않는다 → [[sql-null]] · [[immutability]]
- **자식 쓰레드는 이 값을 못 본다 — 작업을 다른 쓰레드에 넘기면 세션이 갈라진다** — 맵이 `Thread` 객체에 딸려 있으므로 접속 처리 중에 `new Thread` 를 만들어 DB 작업을 넘기면 그쪽 `get()` 은 `null` 이고 **새 세션이 열린다.** 두 세션이 서로의 미확정 변경을 못 보므로(`REPEATABLE READ`), 부모가 커밋하기 전에 자식이 조회하면 없는 데이터가 되고 커밋도 각각이다. `InheritableThreadLocal` 이 그 자리를 위한 것이지만 **쓰레드 풀에서는 「그 쓰레드가 처음 만들어질 때의 부모」를 물려받아** 더 위험하다 → [[transaction]] · [[thread-state]]
- **전제가 둘인데 하나만 참이다 — 「요청 하나가 한 쓰레드에서 끝난다」와 「쓰레드 하나가 요청 하나로 끝난다」는 다른 문장이다** — 이 도구가 값을 갖는 조건이 앞쪽이고, 이 도구가 **안전한** 조건이 뒤쪽이다.

  | 문장 | Day61·62 (접속마다 `new Thread`) | Day64 (컨테이너) |
  |---|---|---|
  | 요청 하나가 한 쓰레드에서 끝난다 | 참 | **참** — 그래서 세션을 쓰레드에 묶는 것이 여전히 맞다 |
  | 쓰레드 하나가 요청 하나로 끝난다 | 참 | **거짓** — 그래서 `remove()` 없이는 남의 세션이 온다 |

  **두 문장을 한 전제로 뭉쳐 두면 Day62 의 코드가 웹에서 왜 깨지는지 설명되지 않는다** — 「요청마다 쓰레드가 하나니까 괜찮다」는 앞줄만 읽은 것이다. 그리고 앞줄도 영원하지 않다 — 비동기·논블로킹으로 작업을 큐에 넣고 다른 쓰레드가 이어받는 구조로 바꾸면 **같은 코드가 조용히 남의 세션을 집거나 세션을 잃는다.** 「쓰레드에 묶는다」는 것이 편리한 만큼 **실행 모델을 고정한다** → [[queue]] · [[socket]] · [[servlet-lifecycle]]
- **필기의 「Factory Pattern」은 GoF 의 팩토리 패턴이 아니다** — 절 제목이 그렇게 붙어 있지만 세 줄의 내용은 「쓰레드당 하나의 SqlSession 을 갖게 만든다」·「고유의 SqlSession 이 있는지 확인 후 할당한다」·「그외 기능은 위임한다」 — **객체를 어떻게 만들지의 규칙이 아니라 이미 있는 팩토리를 세션의 유일한 출입구로 쓰는 이야기**다. 마지막 줄(위임)은 아예 프록시의 정의다. 「SqlSessionFactory 를 만들어서」라는 표현도 정확하지 않다 — 팩토리는 Day59 부터 이미 있었고 이 회차가 만든 것은 **그 앞에 세우는 대리자**다 → [[proxy-pattern]]
- **「그외 다른 기능은 기존의 SqlSession에게 위임한다」의 대상이 틀렸다** — 위임을 받는 것은 `SqlSession` 이 아니라 **원래의 `SqlSessionFactory`**(`original`)다. 코드의 주석은 「나머지는 원래 SqlSessionFactory에 위임을 한다」로 맞게 적혀 있어서 **본문과 주석이 다른 말을 한다** — 대리자가 씌워진 층이 팩토리라는 것을 문장 쪽에서는 놓친 것이고, 두 객체의 이름이 앞부분을 공유해서 눈에 안 걸린다 → [[sql-session]]
- **`sqlSessionThreadLocal` 의 선언과 `original` 의 선언·생성자가 필기에 없다** — 그래서 세 가지가 안 보인다: 담는 타입, 그 필드를 **누가 갖는가**(위의 「키가 둘이 된다」), 그리고 **원래 팩토리를 어디서 받는가.** Day61 의 클라이언트에서 `GOODBYE` 상수 선언이 빠져 있던 것과 같은 자리이고, **프록시가 성립하는 조건(같은 타입을 구현하고 원본을 품는다)이 코드 조각에서 확인되지 않는다** → [[proxy-pattern]] · [[interface]]

## 함께 보는 개념

- [[thread]] — 이 값이 딸리는 단위
- [[sql-session]] — Day62 가 쓰레드마다 나눈 대상
- [[servlet-listener]] — 이 프록시를 앱에 하나로 만들어 주는 자리
- [[servlet-context]] — 그 하나가 담기는 곳
- [[servlet-container]] — `remove()` 부재가 실제 버그가 되는 실행 환경
- [[servlet-lifecycle]] — 「요청 하나 = 쓰레드 하나」가 성립하는 층
- [[proxy-pattern]] — 이 도구를 놓을 자리를 만든 구조
- [[transaction]] — 쓰레드마다 나눈 결과로 갈라지는 커밋 경계
- [[caching]] — 「없으면 만들고 있으면 그대로」의 같은 모양
- [[mybatis]] — 세 객체의 수명 표가 이 판단의 근거
- [[dynamic-proxy]] — 인수를 늘릴 수 없어 이 통로가 필요해지는 층
- [[static-member]] — 「필드는 하나」가 갖는 뜻
- [[garbage-collection]] · [[object-reference]] — 값이 언제까지 사는가
- [[jvm-stack]] — 쓰레드마다 따로 있는 다른 것
- [[hash-based-collection]] — 값이 실제로 담기는 자료구조
- [[connection-lifetime-mismatch]] — 반납되지 않은 연결이 만드는 문제
- [[variable-scope]] — 필드에서 지역 변수로 내려오는 리팩터링
- [[queue]] — 실행 모델을 바꾸면 이 전제가 깨지는 자리
- [[dependency-injection]] — 인수로 전하는 쪽의 대안

## 출처

- [[2024-08-23-Day62]] — 「코드 수정 > SqlSessionFactory 생성」 절의 여덟 줄이 이 개념이다. `sqlSessionThreadLocal.get()` 이 `null` 이면 `original.openSession(autoCommit)` 으로 만들고 `set()` 으로 넣어 둔 뒤 돌려주는 형태로, **쓰레드마다 같은 `SqlSession` 을 받게 하는 것**이 목적이며 필기의 표현은 「스레드 별로 같은 SqlSession 객체를 리턴」이다. 앞 절(「Factory Pattern」)이 그 판단의 이유를 적었다 — 「SqlSessionFactory를 만들어서 쓰레드당 하나의 SqlSession를 갖게 만든다」·「클라이언트가 접속 후 명령을 수행할때 고유의 SqlSession이 있는지 확인 후 할당한다」·「각자 고유의 캐시를 가지기 때문에 다른 클라이언트의 작업이 현재 클라이언트의 작업에 영향을 미치지 않는다」. 뒤이어 `DaoFactory` 와 Command 구현체가 `SqlSession` 필드를 버리고 `SqlSessionFactory` 를 받아 **그때그때 `openSession(false)` 로 얻어 쓰는** 형태로 바뀐다. 다만 **`ThreadLocal` 이라는 낱말도, 그 필드의 선언도, `original` 의 선언과 생성자도 필기에 없고**, `remove()` 와 `sqlSession.close()` 가 어디에도 없어 연결이 풀로 돌아가지 않는다. 캐시가 맞은 경로에서 `autoCommit` 인수가 버려지는 것, 자식 쓰레드가 이 값을 못 보는 것, 이 필드를 몇 개 만들 것인지도 다루지 않았다. 「그외 다른 기능은 기존의 SqlSession에게 위임한다」는 위임 대상을 잘못 적은 것으로, 같은 코드의 주석은 「원래 SqlSessionFactory에 위임을 한다」로 맞게 되어 있다
- [[2024-08-27-Day64]] — 나흘 뒤. 이 도구를 새로 설명하지는 않고 **그것을 담은 프록시를 웹 컨테이너 위에 올린다** — 리스너의 `contextInitialized` 에 `new SqlSessionFactoryProxy(sqlSessionFactory)` 가 처음 실물로 나오고(Day62 에는 생성자도 `original` 선언도 필기에 없었다), `new DaoFactory(sqlSessionFactoryProxy)` 로 DAO 셋을 만들어 `ServletContext` 속성으로 올린다. 그래서 이 회차가 이 개념에 더하는 것이 둘이다 — ① **「이 필드를 몇 개 만드나」가 답을 얻는다**(만드는 자리가 부팅 이벤트 하나이므로 앱에 하나가 자리로 보장된다), ② **`remove()` 가 없는 것이 처음으로 실제 버그가 된다**(컨테이너 쓰레드는 요청이 끝나도 죽지 않으므로 재사용된 쓰레드의 `get()` 이 먼저 다녀간 사람의 세션과 1차 캐시를 돌려준다). 필기는 둘 중 어느 것도 적지 않았다 — `ThreadLocal` 이라는 낱말도, 세션을 닫는 코드도, 리스너의 `contextDestroyed` 도 이 회차에 없다
