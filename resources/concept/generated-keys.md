---
type: concept
id: generated-keys
title: 자동 생성 키 되받기 (RETURN_GENERATED_KEYS · getGeneratedKeys)
aliases:
  - RETURN_GENERATED_KEYS
  - getGeneratedKeys
  - 자동 생성 키
  - generated keys
  - last_insert_id
  - LAST_INSERT_ID
up:
  - 2024-08-13-Day55
  - 2024-08-16-Day57
  - 2024-08-19-Day58
tags:
  - java
  - database
  - JDBC
  - MySQL
---

# 자동 생성 키 되받기 (RETURN_GENERATED_KEYS · getGeneratedKeys)

**`insert` 를 실행한 뒤, 그 행에 서버가 발급한 키 값을 그 문장으로부터 돌려받는 것.** Day55 의 한 줄이 필요를 말한다 — 「projectNo를 받기위해서 PK가 필요하다」. `auto_increment` 로 번호 발급을 서버에 넘긴 대가로 **넣기 전에는 그 행의 번호를 알 수 없게 되었고**, 자식 행을 넣으려면 그 값이 필요하다 → [[surrogate-key]] · [[foreign-key]]

## 정의

두 단계다. **문장을 실행할 때 「키를 돌려 달라」고 요청하고**, 실행 뒤에 **그 키를 결과 집합으로 읽는다.**

```java
stmt.executeUpdate(sql, Statement.RETURN_GENERATED_KEYS);   // ① 요청
ResultSet keyRS = stmt.getGeneratedKeys();                  // ② 읽기
keyRS.next();
int no = keyRS.getInt(1);
```

| 조각 | 정체 | 값 |
|---|---|---|
| `executeUpdate(String, int)` | `executeUpdate(String)` 의 **오버로드** | — |
| `Statement.RETURN_GENERATED_KEYS` | `Statement` 인터페이스의 `int` **상수** | `1` |
| `Statement.NO_GENERATED_KEYS` | 같은 자리의 반대쪽 상수 (기본값) | `2` |
| `getGeneratedKeys()` | 그 키들을 담은 **`ResultSet`** | 컬럼 하나, 행 하나(대개) |

**돌아오는 것이 값 하나가 아니라 `ResultSet` 이라는 점이 핵심**이다 — 한 문장이 여러 행을 넣을 수 있으므로 키도 여러 개일 수 있고, 그래서 `select` 결과와 같은 방식으로 읽는다. 컬럼 이름은 드라이버가 정하므로(MySQL 은 `GENERATED_KEY`) **인덱스 `1` 로 읽는 것이 유일한 이식 가능한 방법**이다.

`PreparedStatement` 에서는 같은 상수가 **문장을 만들 때** 들어간다 — `con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)`. 요청 시점이 실행에서 준비로 옮겨가는 것뿐이고 읽는 쪽은 같다.

### 사흘 뒤 Day57 — 요청 자리가 앞으로 옮겨간다

Day55 는 `Statement` 판만 썼고, **Day57 이 두 판을 나란히 놓아 이 차이를 드러낸다** → [[prepared-statement]]

| | 플래그를 주는 곳 | 실행 |
|---|---|---|
| `Statement` | `stmt.executeUpdate(쿼리문, Statement.RETURN_GENERATED_KEYS)` | 같은 호출 |
| `PreparedStatement` | `con.prepareStatement(쿼리문, Statement.RETURN_GENERATED_KEYS)` | `stmt.executeUpdate()` — **인수 없음** |

필기가 이유를 한 줄씩 적었다 — 「Statment로 생성된 객체는 쿼리문을 전송(execute)할때 리턴 받는다」·「PreparedStatement로 생성된 객체는 statement를 생성(PrepareStatement)할 리턴 받는다」. **문장이 미리 준비되므로 실행 시점에는 넘길 인수가 없다**는 것이 답이고, 그래서 요청을 준비 쪽으로 올려야 한다. 읽는 네 줄(`getGeneratedKeys` → `next()` → `getInt(1)` → `setNo`)은 두 판에서 **글자 하나 다르지 않다** — 이 개념이 문장 종류에 딸린 것이 아니라는 증거다.

## 사용 예시

Day55 가 프로젝트 등록에 이 형태를 넣는다.

```java
try (Statement stmt = con.createStatement()) {
  stmt.executeUpdate(sql쿼리문, Statement.RETURN_GENERATED_KEYS);
  ResultSet keyRS = stmt.getGeneratedKeys();
  keyRS.next();
  int projectNo = keyRS.getInt(1);
  project.setNo(projectNo);
}
```

그리고 **되받은 번호를 바로 다음 문장이 값으로 쓴다.** 같은 회차의 Command 쪽 한 줄이 그것이다.

```java
projectDao.insertMembers(project.getNo(), project.getMembers());
```

**두 줄 사이에 이 개념이 서 있다.** `project.setNo(projectNo)` 가 없으면 `getNo()` 는 `0` 이고, 중간 테이블에 `project_id = 0` 인 행을 넣으려다 외래키가 거절한다 — 0번 프로젝트가 없기 때문이다. 등록 화면 하나가 문장 둘로 갈린 뒤 **그 둘을 잇는 값이 서버에서 온다**는 것이 이 코드의 모양이다 → [[foreign-key]] · [[transaction]]

## 왜 중요한가

**번호 발급자가 애플리케이션에서 DB 로 옮겨간 대가를 이것이 치른다.** Day19 의 `user.setNo(User.getSeqNo())` 는 **저장하기 전에** 번호를 알았고, 그래서 그 번호를 다른 곳에 적어 두는 일이 순서 문제를 만들지 않았다. `auto_increment` 는 반대다 — 번호는 `insert` 가 성공한 뒤에만 존재하므로, **부모를 먼저 넣고 키를 되받아야 자식을 넣을 수 있다.** 정규화가 만든 「테이블 두 개」가 코드에서는 **순서가 강제된 문장 두 개**로 나타나는 것이 이 자리다 → [[surrogate-key]] · [[db-normalization]]

**이것을 모르면 방금 넣은 행을 다시 찾는 코드를 쓰게 된다.** `select no from myapp_projects order by no desc limit 1` 같은 것인데, 동시에 다른 사람이 등록하면 **남의 번호를 가져온다.** 되받는 방식은 그럴 수 없다 — 키는 내 문장의 결과이고 내 연결에만 딸려 있다. 「값을 다시 조회해서 알아낸다」와 「실행 결과로 받는다」의 차이가 정확성 문제라는 것을 보여 주는 표본이다 → [[transaction]]

**그리고 「무엇이 서버가 채운 값인가」를 처음 의식하게 된다.** 지금까지 자바 객체의 필드는 전부 내가 넣은 값이었다. `insert` 뒤로는 **객체와 행이 어긋난 상태**가 잠깐 생기고(행에는 번호가 있는데 객체에는 없다), 그것을 맞추는 것이 `setNo` 한 줄이다. 나중에 ORM 이 이 동기화를 대신하겠다고 나오는 이유가 여기에 있다 → [[jdbc]]

## 경계와 오해

- **「`executeUpdate()` 의 오버로딩으로 `Statement.RETURN_GENERATED_KEYS` 가 있다」는 두 가지를 한 줄로 겹쳤다** — 오버로드는 **메서드** 쪽 이야기(`executeUpdate(String)` 과 `executeUpdate(String, int)`)이고, `RETURN_GENERATED_KEYS` 는 그 `int` 자리에 넣는 **상수**(값 `1`)다. 상수가 오버로드인 것이 아니라 **오버로드가 상수를 받는 자리를 만든 것**이며, 그래서 반대쪽 값 `NO_GENERATED_KEYS`(`2`)도 같은 자리에 들어갈 수 있다. 겹쳐 읽으면 `PreparedStatement` 쪽에서 막힌다 — 거기서는 **같은 상수를 `con.prepareStatement(sql, RETURN_GENERATED_KEYS)` 로 문장을 만들 때** 넘기고 `executeUpdate()` 는 인수를 받지 않는다. 상수와 오버로드를 갈라 두면 「어느 메서드의 몇 번째 인수인가」가 옮겨져도 같은 것으로 보인다 → [[method]] · [[static-member]]
- **「리턴 받는 시점」이 아니라 「플래그를 주는 시점」이 다른 것이다** — Day57 의 두 줄(「Statment로 생성된 객체는 쿼리문을 전송(execute)할때 리턴 받는다」·「PreparedStatement로 생성된 객체는 statement를 생성(PrepareStatement)할 리턴 받는다」)을 그대로 읽으면 **`prepareStatement` 가 키를 돌려준다**는 말이 된다. 그렇지 않다 — 키는 두 경우 다 **실행 뒤에 `getGeneratedKeys()` 로** 온다. 갈리는 것은 `RETURN_GENERATED_KEYS` 를 **어느 메서드에 넘기는가**뿐이다. 「리턴」이라는 낱말이 요청과 수신을 한 덩어리로 만들어서, `PreparedStatement` 쪽에서 `stmt.executeUpdate(sql, RETURN_GENERATED_KEYS)` 를 다시 쓰려 들게 된다 — 그 호출은 컴파일은 되지만 **`SQLException`** 이다 → [[prepared-statement]] · [[method]]
- **`keyRS.next()` 의 반환값을 버렸다 — 사흘 뒤에도 그대로다** — Day55 의 코드는 `keyRS.next();` 를 홀로 호출하고, **Day57 §2.1 이 그 네 줄을 `PreparedStatement` 판으로 옮길 때도 손대지 않았다.** 키가 없으면 이 호출이 `false` 를 주고, 다음 줄 `keyRS.getInt(1)` 이 **`SQLException`** 을 던진다. 즉 실패가 「키를 못 받았다」로 나타나지 않고 **결과 집합을 잘못 읽었다는 메시지**로 나타나서, 원인(플래그 누락·`auto_increment` 아님)을 메시지에서 읽을 수 없다. `if (keyRS.next())` 로 감싸는 한 줄이 그 간격을 없앤다 → [[exception-handling]]
- **되받을 수 있는 것은 `auto_increment` 컬럼뿐이다** — 이름이 「생성된 키(generated keys)」라서 서버가 채운 값 전부를 받을 것처럼 들리지만, `default now()` 로 채워진 등록일시나 트리거가 넣은 값은 오지 않는다. 그것들이 필요하면 **넣은 뒤 다시 `select`** 해야 한다. 「생성된 값」이 아니라 「생성된 **키**」인 것이 이름 안에 이미 적혀 있다 → [[sql-date-function]]
- **컬럼 이름으로 읽으면 다른 DB 에서 깨진다** — MySQL 이 이 결과에 붙이는 컬럼 이름은 `GENERATED_KEY` 인데 표준이 정한 이름이 아니다. Day55 가 `getInt(1)` 로 **인덱스로 읽은 것이 결과적으로 옳고**, 같은 노트의 `getMembers` 가 `rs.getString("name")` 처럼 이름으로 읽는 것과 **여기서만 규칙이 갈린다** — 내가 적은 `select` 목록의 컬럼은 이름이 내 것이지만, 이 결과의 컬럼은 드라이버가 지은 것이다.
- **플래그 없이도 되는 것처럼 보이는 드라이버가 있다** — JDBC 명세는 키를 요청하지 않은 문장에 대해 `getGeneratedKeys()` 가 무엇을 돌려줄지 **정해 두지 않았다**(드라이버 재량). MySQL Connector/J 는 관대해서 `insert` 뒤에 값을 주는 경우가 있고, 그래서 **플래그를 빼먹은 코드가 MySQL 에서는 돌아가다가 다른 DB 로 옮기면 빈 결과**가 된다. 「돌아가니까 맞다」가 이식성 문제를 덮는 자리이며, [[jdbc]] 가 통일하는 범위 밖에 이런 것들이 남아 있다.
- **여러 행을 넣으면 키가 몇 개 오는지 정해져 있지 않다** — `keyRS.next()` 를 한 번만 부르는 형태는 **한 행을 넣는 `insert`** 에만 맞다. MySQL 은 다중 행 `insert` 에 대해 첫 키부터 연속된 값을 돌려주지만 표준이 요구하는 것은 아니고, 배치 실행에서는 드라이버 설정에 따라 갈린다. `while (keyRS.next())` 로 읽는 형태가 일반형이다 → [[dml]]
- **`last_insert_id()` 는 「남의 번호를 받을 위험」이 없다 — 다른 함정이 있다** — MySQL 함수 `LAST_INSERT_ID()` 로도 같은 값을 얻을 수 있고, 이 값은 **연결(세션)마다 따로 유지**되므로 「동시에 등록하면 섞인다」는 흔한 걱정은 사실이 아니다. 대신 ① 다중 행 `insert` 에서는 **첫 번째** 번호만 주고 ② 그 문장이 트리거를 타서 또 `insert` 를 하면 값이 덮이고 ③ 문장이 하나 더 늘어나므로 왕복이 한 번 더 생긴다. 되받는 쪽은 이 셋에서 자유롭다 → [[transaction]]
- **되받은 번호는 아직 확정된 값이 아니다** — `commit` 전에도 번호는 발급되고, `rollback` 하면 그 행은 사라지지만 **번호는 되돌아가지 않는다.** 「등록 완료 — 3번」이라고 화면에 찍은 뒤 롤백하면 3번은 **존재하지 않는 번호**가 된다. 자동 증가 카운터가 트랜잭션의 대상이 아니라는 성질이 여기서 사용자에게 보이는 값으로 새어 나온다 → [[transaction]] · [[surrogate-key]]
- **「projectNo를 받기위해서 PK가 필요하다」는 이유를 반쯤만 적었다** — 문장이 돌고 있다(번호를 받으려면 번호가 필요하다). 정확히는 **중간 테이블의 행이 부모 키를 값으로 요구하기 때문**이고, 그래서 이 코드는 「PK 가 있어서」가 아니라 **「자식 행을 넣어야 해서」** 필요하다. 자식이 없는 테이블이라면 번호를 되받지 않아도 등록은 끝난다 — 필요를 만드는 것은 `auto_increment` 가 아니라 **관계**다 → [[foreign-key]]
- **`insert` 를 감싸 「행 수」만 돌려주는 순간 이 장치가 통째로 빠진다 — 사흘 뒤 Day58 이 그 형태다** — 그 회차의 세션은 `con.prepareStatement(sql)`(플래그 없음)으로 문장을 만들고 `int` 하나를 돌려주며 [[try-with-resources]] 로 문장을 닫는다. **되받을 자리가 세 번 막힌다**: 플래그를 줄 인수가 없고, 반환형에 키가 들어갈 칸이 없고, `getGeneratedKeys()` 를 부를 문장 객체가 메서드를 나가는 순간 닫혀 있다. 그 결과가 Day57 §2.2 의 등록 화면에서 이렇게 나타난다 — `projectDao.insert(project)` 가 성공하고 `1` 을 돌려주지만 `project.setNo(...)` 는 아무도 부르지 않아 `getNo()` 가 `0` 이고, 다음 줄 `insertMembers(project.getNo(), ...)` 가 **`project_id = 0` 인 행**을 중간 테이블에 넣으려 한다. [[foreign-key]] 가 그것을 거절하므로 예외가 나고 트랜잭션이 롤백된다 — **화면에는 「팀원 테이블의 외래키 위반」이 찍히는데 원인은 그 앞 문장의 키를 감싸는 층이 버린 것**이라, 오류 메시지가 가리키는 문장과 고쳐야 할 문장이 다르다. 외래키가 없는 스키마였다면 더 나쁘다 — `0` 번 프로젝트의 팀원이 조용히 커밋된다. **감싸는 층의 반환형이 「행 수」로 정해진 순간 이 개념이 설계에서 빠지는 것**이고, MyBatis 가 매퍼에 `useGeneratedKeys="true" keyProperty="no"` 라는 별도 설정을 두는 이유가 여기다 → [[sql-session]] · [[transaction]]
- **`RETURNING` 이 더 짧은 길이지만 MySQL 에는 없다** — PostgreSQL·MariaDB 는 `insert ... returning no` 로 **문장 하나가 값을 돌려준다**(조회 결과처럼 읽는다). MySQL 8.x 에는 없어서 JDBC 쪽 장치를 쓰는 것이고, 즉 이 두 단계 코드는 **자바의 방식이 아니라 그 DB 에 없는 문법의 우회**다 → [[dql]]

## 함께 보는 개념

- [[surrogate-key]] — 번호를 애플리케이션이 발급하던 시절과 갈리는 자리
- [[primary-key]] — 되받는 값이 무엇인가
- [[foreign-key]] — 그 값을 요구하는 자식 행
- [[jdbc]] — 이 API 가 사는 층
- [[prepared-statement]] — 플래그 자리가 준비 시점으로 옮겨가는 쪽
- [[result-set]] — 되받는 것이 값이 아니라 커서인 이유
- [[transaction]] — 되받은 번호가 확정되지 않은 상태
- [[dml]] — 키를 만드는 문장
- [[db-normalization]] — 등록이 문장 둘이 된 이유
- [[exception-handling]] — 키를 못 받았을 때 드러나는 방식
- [[crud]] — 등록 화면이 두 문장으로 갈리는 자리
- [[method]] — 오버로드와 상수를 가르는 문법 축
- [[sql-session]] — 감싸는 층의 반환형이 이 장치를 밀어내는 자리
- [[try-with-resources]] — 문장이 닫히면 키를 읽을 대상이 사라진다

## 출처

- [[2024-08-13-Day55]] — 「RETURN_GENERATED_KEYS 생성」 세 줄과 코드 여섯 줄로 이 개념이 등장한다. 「projectNo를 받기위해서 PK가 필요하다」·「Statement.executeUpdate()의 오버로딩으로 Statement.RETURN_GENERATED_KEYS가 있다」·「statement에서 Pk를 리턴받고 변수에 할당을 한 다음 project객체에 대입한다」이고, 마지막 줄이 **객체와 행을 다시 맞추는 일**을 정확히 적었다. 되받은 값은 같은 회차의 `projectDao.insertMembers(project.getNo(), ...)` 가 곧바로 쓴다. 다만 두 번째 줄은 오버로드(`executeUpdate(String,int)`)와 상수(`RETURN_GENERATED_KEYS`)를 한 줄에 겹쳐 적었고, 코드의 `keyRS.next()` 는 반환값을 검사하지 않아 키가 없는 경우가 엉뚱한 예외로 나타난다. `getInt(1)` 로 인덱스로 읽은 것은 결과적으로 이식성 있는 형태다
- [[2024-08-16-Day57]] — 사흘 뒤. 「1.4 Primary Key return」이 같은 장치를 다시 세우면서 **`PreparedStatement` 판을 나란히 추가한다** — 플래그가 `executeUpdate` 에서 `prepareStatement` 로 올라가고, 읽는 네 줄은 그대로다. 「자동생성된 PK값을 리턴받을 수 있다」·「Statement.RETURN_GENERATED_KEYS로 ResultSet에 생성한다」에 이어 두 문장 종류의 차이를 각각 한 줄로 적은 것이 이 회차가 더한 것이고, 실습 §2.2 가 되받은 번호를 쓰는 두 문장(`insert` → `insertMembers`)을 **수동 커밋으로 감싸** [[transaction]] 과 이어 붙인다. 다만 두 줄 모두 「리턴 받는다」로 적어 **요청 시점과 수신 시점을 겹쳐** 놓았고(키는 언제나 실행 뒤에 온다), 「statement를 생성(PrepareStatement)할 리턴 받는다」는 조사가 빠져 문장이 끊긴다. `keyRS.next()` 의 반환값을 검사하지 않는 코드도 두 판 모두 그대로 옮겨 왔다
- [[2024-08-19-Day58]] — 사흘 뒤. 이 개념이 **나오지 않는 것이 자료**인 회차다. JDBC 호출을 세션 클래스로 감싸면서 `insert(String sql, Object... values)` 가 `con.prepareStatement(sql)` 로 플래그 없이 문장을 만들고 `int`(변경된 행 수) 하나를 돌려주며 문장을 닫으므로, **Day55·Day57 이 두 회차에 걸쳐 세운 「플래그 → 실행 → `getGeneratedKeys()`」 경로가 이 통로에는 존재하지 않는다.** 필기는 그것을 문제로 적지 않았고 `insert` 를 예외로 두는 언급도 없다 — 그래서 이 노트의 「경계와 오해」가 그 누락이 Day57 §2.2 의 등록 화면에서 무엇을 깨는지(`getNo()` 가 `0` 인 채로 중간 테이블에 들어가 외래키가 거절한다)를 따라간다. 「insert문 만들기」 코드 블록이 `update`·`delete` 까지 담고 뒤의 두 절이 같은 코드를 다시 실은 붙여넣기 중복도 이 회차의 상태다 → [[sql-session]]
