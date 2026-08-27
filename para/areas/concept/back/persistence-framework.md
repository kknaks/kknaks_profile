---
type: concept
id: persistence-framework
title: 영속성 프레임워크 (SQL Mapper 와 OR Mapper)
aliases:
  - 영속성 프레임워크
  - Persistence Framework
  - 퍼시스턴스 프레임워크
  - SQL Mapper
  - SQL 매퍼
  - OR Mapper
up:
  - 2024-08-20-Day59
  - 2024-08-21-Day60
  - 2025-01-02-Day03
tags:
  - database
  - 프레임워크
  - 설계
  - java
---

# 영속성 프레임워크 (SQL Mapper 와 OR Mapper)

**자바 객체와 DB 테이블 사이를 오가는 반복 작업을 대신하는 층, 그리고 그 층이 「SQL 을 누가 쓰는가」로 두 갈래로 갈린다는 것.** Day59 가 MyBatis 를 배우기 직전에 이 두 줄을 놓았다 — 「**SQL Mapper** : 개발자가 직접 쿼리문을 만들고 프레임워크에서 결과를 리턴 받는다」·「**OR Mapper** : 쿼리문을 자동으로 생성해서 결과를 리턴 받는다」 → [[jdbc]] · [[dao-pattern]]

## 정의

필기의 두 줄이 가른 축은 하나이고, 나머지 차이는 전부 거기서 나온다.

| | **SQL Mapper** | **OR Mapper (ORM)** |
|---|---|---|
| SQL 문장을 쓰는 주체 | **사람** | **프레임워크** |
| 내가 적는 것 | SQL 과 「결과를 무엇으로 만들지」 | 객체와 테이블의 **대응 규칙** |
| 매핑의 방향 | 결과 → 객체 (**읽는 쪽**) | 양쪽. 객체의 상태 변화가 SQL 이 된다 |
| 대표 구현 | MyBatis · Spring `JdbcTemplate` | JPA/Hibernate · Django ORM · ActiveRecord |
| 강한 곳 | 복잡한 조회·통계·DB 고유 기능 | 단순 CRUD·객체 그래프 저장 |
| 약한 곳 | 문장 수가 늘면 관리할 XML 도 늘어난다 | 생성된 SQL 이 눈에 안 보인다 |

**두 갈래가 걷어내는 반복이 다르다.** SQL Mapper 는 하루 전 Day58 이 손으로 걷어낸 것 — `PreparedStatement` 준비·바인딩·`ResultSet` 읽기 — 을 대신하고, SQL 문장 자체는 그대로 내 것이다. OR Mapper 는 **SQL 문장까지** 대신 쓴다 → [[sql-session]] · [[prepared-statement]] · [[result-set]]

### 표의 「객체 그래프」 칸을 Day60 기준으로 다시 읽는다

위 표가 「객체 그래프 저장」을 OR Mapper 쪽 강점으로만 적었는데, 하루 뒤 Day60 의 `<resultMap>`·`<association>`·`<collection>` 이 **SQL Mapper 로도 객체 그래프를 만드는** 것을 보인다 — 조인 결과의 행 반복을 접어 `Project` 하나에 `List<User>` 를 담는다. 그래서 갈리는 축을 한 낱말 더 좁혀야 한다.

| | SQL Mapper (Day60 확인) | OR Mapper |
|---|---|---|
| 그래프를 **읽어 만드는 것** | **한다** — `<collection>` 이 그 일이다 | 한다 |
| 그래프의 **변경을 문장으로 되돌리는 것** | 안 한다 — `insert`·`update` 를 내가 쓴다 | 한다 |
| 매핑 선언이 쓰이는 방향 | 결과 → 객체 (**한 방향**) | 양방향 |

**「객체 그래프」가 아니라 「객체 그래프의 저장」이 갈림이다.** 필기의 두 줄(「직접 쿼리문을 만들고」/「쿼리문을 자동으로 생성해서」)이 처음부터 그 축을 가리키고 있었고, Day60 은 그 축을 **흐리지 않으면서 겉모습만 닮게** 만든 회차다 → [[result-map]] · [[mybatis]]

### 「영속성」이 가리키는 것

`persistence` 는 **프로세스가 끝나도 남는다**는 뜻이고 DB 에 국한된 말이 아니다. 이 필기가 지나온 것들이 전부 그 축에 있다.

| 방식 | 남기는 곳 | 구조를 아는 주체 |
|---|---|---|
| 파일에 텍스트로 쓰기 | 파일 | 내가 만든 형식 |
| [[serialization]] | 파일 | JVM |
| [[csv]] · [[json]] | 파일 | 형식의 규약 |
| **영속성 프레임워크** | **DB** | **스키마 + 대응 규칙** |

**DB 로 오면서 새로 생긴 것이 「구조를 저장소도 알고 있다」는 것**이다. 파일은 내가 쓴 대로 담기지만 테이블은 컬럼과 타입과 제약을 스스로 갖고 있어서, 자바 쪽 클래스와 그것이 **어긋날 수 있다** — 그 어긋남을 메우는 일이 곧 매핑이고, 이 층이 존재하는 이유다 → [[database-schema]] · [[sql-data-type]]

## 왜 중요한가

**「무엇을 자동으로 하게 할 것인가」의 선택지가 둘이라는 것을 알고 고르게 된다.** JDBC 만 쓰던 코드에서 반복되는 것은 두 종류다 — ① `Statement` 를 준비하고 값을 채우고 커서를 읽는 **절차**, ② `select ... from users where id = ?` 같은 **문장**. Day58 이 ① 을 손으로 걷어냈고 MyBatis 가 그것을 완성하는데, ② 는 여전히 사람이 쓴다. **「프레임워크를 쓰면 SQL 을 안 쓴다」로 뭉치면 MyBatis 를 쓰면서 왜 SQL 을 계속 쓰는지 설명되지 않는다** → [[mybatis]] · [[sql-session]]

**그리고 두 갈래가 각각 대가를 갖는다.** SQL Mapper 는 문장이 눈에 보이니 성능을 예측할 수 있지만 문장 수만큼 관리 대상이 늘어난다. OR Mapper 는 문장이 사라져 코드가 짧아지지만 **무슨 SQL 이 나갔는지 모르는 상태**가 기본값이고, 그것을 알아내려고 결국 SQL 로그를 켠다. **어느 쪽이든 SQL 을 읽을 줄 알아야 한다는 결론이 같다** → [[database-index]]

## 경계와 오해

- **MyBatis 는 ORM 이 아니다 — 필기의 두 줄이 그것을 정확히 가른다** — 「MyBatis ORM」이라는 말이 흔하고 MyBatis 가 결과를 객체로 만들어 주니 그렇게 보이는데, MyBatis 자신이 스스로를 **SQL Mapper** 라 부른다. 갈리는 지점은 방향이다: MyBatis 의 `resultType` 은 **조회 결과를 객체로 만드는** 한 방향이고, ORM 의 매핑은 **객체를 고치면 그것이 `update` 문장이 되는** 반대 방향까지 포함한다. 「매핑을 하니 ORM」으로 읽으면 「그런데 왜 `update` 문을 내가 쓰지?」가 설명되지 않는다 → [[mybatis]]
- **Day60 을 지나면 이 구별이 더 어려워진다 — 그래서 판정 기준을 방향으로 못 박아 둔다** — Day59 시점에는 근거를 「`resultType` 은 클래스 하나를 만들 뿐이다」로 댈 수 있었다. Day60 의 `<resultMap>` 은 **객체 안에 객체와 목록을 채운 그래프**를 만들고 매핑 규칙을 별도 선언으로 빼내므로, ORM 의 매핑 파일과 **모양이 닮는다.** 그래도 판정은 바뀌지 않는다 — 그 선언은 `insert`·`update` 에 쓰이지 않고(이름이 `resultMap` 인 그대로다), 팀원 목록을 고쳐도 문장이 저절로 나가지 않아 Day55 처럼 `deleteMembers` + `insertMembers` 를 내가 부른다. **기준은 「무엇을 만들어 주는가」가 아니라 「내가 문장을 쓰는가」다** → [[result-map]] · [[dml]] · [[crud]]
- **「쿼리문을 자동으로 생성해서」가 「SQL 을 몰라도 된다」는 아니다** — 생성된 문장을 보지 않으면 목록 하나를 그리며 문장이 101 번 나가는 것(N+1)이나 필요 없는 컬럼을 전부 긁어오는 것을 알 수 없다. **자동 생성은 「쓰지 않아도 된다」이지 「읽지 않아도 된다」가 아니다** → [[sql-join]] · [[dql]]
- **SQL Mapper 도 JDBC 를 없애지 않는다 — 감싼다** — MyBatis 밑에는 여전히 `Connection`·`PreparedStatement`·`ResultSet` 이 있고, 예외도 결국 그쪽에서 온다. 하루 전 Day58 이 손으로 만든 층이 바로 이 자리이며, **프레임워크를 쓴다는 것은 그 층을 남이 만들어 준 것을 쓴다는 뜻**이다. 그래서 JDBC 를 모르면 MyBatis 의 오류 메시지를 읽을 수 없다 → [[jdbc]] · [[sql-session]]
- **두 갈래는 배타적이지 않다** — 한 프로젝트에서 JPA 로 CRUD 를 하고 복잡한 통계 조회만 MyBatis 나 `JdbcTemplate` 로 하는 형태가 흔하다. 「우리는 ORM 을 쓴다」가 전부를 정하는 결정이 아니다.
- **OR Mapper 의 R 은 Relational 이다** — 「Object Return」이 아니고 「Object Relation」도 아니다. **객체 모델과 관계 모델을 잇는다**는 뜻이며, 그 두 모델이 다르다는 것(상속·다형성이 테이블에 없고, 컬렉션과 외래키가 대응하지 않는다)이 ORM 이 어려운 이유 전체다 → [[inheritance]] · [[foreign-key]]
- **필기의 두 줄이 대칭이 아니다** — SQL Mapper 쪽에만 「개발자가 직접」이라는 주체가 있고 OR Mapper 쪽은 「쿼리문을 자동으로 생성해서」로 주체가 비어 있다. 채우면 **「프레임워크가 객체와 테이블의 대응 규칙에서 쿼리를 만든다」**이고, 그러면 곧바로 다음 질문이 나온다 — **그 대응 규칙을 어디에 적는가.** 그것이 애노테이션(`@Entity`·`@Column`)이나 XML 이고, **ORM 을 쓰는 일의 실제 노동이 SQL 을 쓰는 것에서 대응 규칙을 쓰는 것으로 옮겨간 것**이다. 「쓸 일이 없어진다」가 아니라 「쓸 것이 바뀐다」다 → [[annotation]] · [[xml]]
- **이 층이 없어도 프로그램은 돈다 — 없앤 것은 반복이지 기능이 아니다** — Day55~57 의 DAO 가 JDBC 만으로 CRUD 다섯 개를 다 했다. 프레임워크가 더해 주는 것은 새 능력이 아니라 **같은 것을 적게 쓰는 방법**이고, 그래서 「이 반복이 실제로 아픈가」를 묻지 않고 도입하면 배울 것만 늘어난다 → [[refactoring]]
- **매핑이 리플렉션 위에 서 있다** — 두 갈래 모두 자기가 컴파일할 때 모르던 클래스를 만들고 채워야 하므로 [[class-loading]]·[[reflective-instantiation]]·[[reflective-field-access]] 를 쓴다. **같은 회차의 앞 절(Reflection API)이 뒤 절(MyBatis)의 구현 원리라는 것을 필기는 잇지 않았다** — 두 주제가 한 날에 온 것이 우연처럼 적혀 있다.
- **「영속성」을 「DB 에 저장」으로 읽으면 층이 좁아진다** — 파일·직렬화도 영속성이고, 반대로 DB 를 쓴다고 영속적인 것도 아니다(임시 테이블·인메모리 DB). 이 층이 다루는 것은 **저장소가 관계형 DB 일 때의 매핑**이라 이름보다 좁다 → [[serialization]]

## 함께 보는 개념

- [[osiv]] — JPA 를 웹에서 쓸 때 따라오는 설정

- [[mybatis]] — 이 갈래 중 SQL Mapper 쪽의 실물
- [[result-map]] — SQL Mapper 가 그래프를 「읽어 만드는」 자리
- [[dynamic-sql]] — 문장을 사람이 적는다는 것의 경계가 흐려지는 자리
- [[sql-session]] — 그 층을 손으로 만들어 본 앞 걸음
- [[jdbc]] — 두 갈래가 공통으로 깔고 있는 층
- [[dao-pattern]] — 이 층이 놓이면 얇아지는 자리
- [[xml]] · [[annotation]] — 대응 규칙을 적는 두 형식
- [[reflective-instantiation]] · [[reflective-field-access]] — 매핑을 실제로 수행하는 도구
- [[class-loading]] — 클래스 이름이 문자열로 오는 통로
- [[result-set]] · [[prepared-statement]] — 걷어내지는 반복의 실체
- [[database-schema]] · [[sql-data-type]] — 자바 쪽과 어긋날 수 있는 상대편
- [[foreign-key]] · [[sql-join]] · [[inheritance]] — 두 모델이 대응하지 않는 자리들
- [[serialization]] · [[csv]] · [[json]] — 같은 영속성 축의 다른 형식들
- [[transaction]] — 이 층이 경계를 어디에 두는가
- [[coupling]] · [[encapsulation]] — 「무엇을 감췄나」를 묻는 축
- [[refactoring]] — 반복을 걷어내는 일의 이름

## 출처

- [[2025-01-02-Day03]] — 넉 달 뒤. **이 노트가 갈라 둔 두 갈래 중 OR Mapper 쪽으로 실제로 넘어간다** — MyBatis 가 아니라 JPA/Hibernate 를 쓰고, `@Entity`·`@MappedSuperclass`·`@GeneratedValue(strategy = IDENTITY)` 로 클래스가 테이블에 대응하며, `@CreatedDate`·`@LastModifiedDate` 와 Auditing 이 생성·수정 시각을 자동으로 채운다. **SQL 을 사람이 쓰지 않는다**는 그 갈림이 코드로 확인되는 자리이고, 동시에 그 대가도 처음 나온다 — 영속성 컨텍스트를 언제까지 열어 둘 것인가(OSIV), 그리고 `default_batch_fetch_size` 가 필요한 N+1 문제 → [[osiv]]
- [[2024-08-20-Day59]] — MyBatis 를 배우기 직전 「Persistence Framework」 절에서 **SQL Mapper 와 OR Mapper 두 줄**로 이 갈래를 세웠다. 「개발자가 직접 쿼리문을 만들고 프레임워크에서 결과를 리턴 받는다」/「쿼리문을 자동으로 생성해서 결과를 리턴 받는다」가 이 개념의 축(SQL 을 누가 쓰는가)을 정확히 가른 두 문장이고, 그 뒤 절 전체가 앞쪽(MyBatis)의 실습이다. 다만 두 줄 중 뒤쪽에는 주체가 비어 있어 「대응 규칙을 어디에 적는가」라는 다음 질문으로 이어지지 않고, OR Mapper 의 구현체 이름·두 갈래를 섞어 쓰는 형태·MyBatis 가 스스로를 ORM 이라 부르지 않는다는 것은 나오지 않는다. 같은 회차 앞부분의 Reflection API 가 이 층의 구현 원리라는 연결도 적혀 있지 않다
- [[2024-08-21-Day60]] — 하루 뒤. **SQL Mapper 쪽이 겉모습에서 OR Mapper 에 가까워지는 회차**이고, 그래서 이 노트의 갈림 기준이 시험받는다. 「resultMap」 절의 `<association>`·`<collection>` 이 조인 결과를 **객체 안의 객체·객체 안의 목록**으로 접어 그래프를 조립하고, 매핑 규칙이 문장에서 빠져 별도 선언이 되므로 ORM 의 매핑 파일과 모양이 닮는다 — 그런데 그 선언은 조회에만 쓰이고 변경 문장은 여전히 사람이 쓴다. 그래서 위 표의 「객체 그래프 저장」이라는 칸을 **「그래프를 읽어 만드는 것」과 「그래프의 변경을 문장으로 되돌리는 것」으로 쪼개야** 하고, 갈림은 뒤쪽에만 남는다. 「typeAliases」 절과 같은 노트 후반의 애노테이션 절들은 이 노트가 「대응 규칙을 어디에 적는가」로 남겨 둔 질문의 두 답(XML · 애노테이션)이 **한 회차 안에 나란히 놓인 자리**이기도 하다 → [[result-map]] · [[type-alias]] · [[annotation]]
