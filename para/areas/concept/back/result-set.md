---
type: concept
id: result-set
title: ResultSet — 커서로 읽는 조회 결과
aliases:
  - ResultSet
  - result set
  - 결과셋
  - 결과 집합
  - rs.next
  - getXXX
  - wasNull
up:
  - 2024-08-16-Day57
tags:
  - java
  - database
  - JDBC
  - 조회
---

# ResultSet — 커서로 읽는 조회 결과

**`select` 의 결과를 담은 객체가 아니라, 그 결과 위에 놓인 커서.** Day57 의 세 줄이 이 개념의 전부를 말한다 — 「select문에 기술된 컬럼으로 구성된 행의 집합이다」·「내부 구조는 다음과 같다」·**「커서가 있는 행의 데이터만 읽을 수 있다」.** 셋째 줄이 첫째 줄을 정정하고 있고, 그 어긋남이 이 노트의 「경계와 오해」 첫 항목이다 → [[jdbc]] · [[dql]]

## 정의

두 축으로 되어 있다. **커서를 옮기는 일**과 **커서가 선 행에서 값을 꺼내는 일**이 서로 다른 메서드다.

```java
Statement stmt = con.createStatement();
ResultSet rs = stmt.executeQuery("select 컬럼명 from 테이블명");
// 커서를 next로 이동(값이 있으면 true, 없으면 false)
if (rs.next()) {
  rs.getXXXX(컬럼 번호);
}
```

| 하는 일 | 메서드 | 돌려주는 것 |
|---|---|---|
| 커서를 **다음 행으로** 옮긴다 | `next()` | 그 자리에 행이 있으면 `true`, 없으면 `false` |
| 그 행의 **한 컬럼**을 읽는다 | `getInt` · `getString` · `getDate` … | 그 컬럼의 값 |

**커서의 출발점이 첫 행이 아니라 「첫 행 앞」**이다. 그래서 `next()` 를 한 번 부르기 전에는 어떤 `getXXX` 도 부를 수 없고, 값을 하나만 읽을 때도 `next()` 가 앞에 필요하다 — [[generated-keys]] 의 `keyRS.next();` 한 줄이 그것이다.

### 타입에 따라 다른 메서드를 부른다

Day57 이 적은 대응이 이것이다. **SQL 타입을 자바 타입으로 옮기는 결정을 내가 메서드 이름으로 한다.**

| 메서드 | 필기가 적은 SQL 타입 | 돌려주는 자바 타입 |
|---|---|---|
| `getInt` | `int`, `number` | `int` |
| `getString` | `char`, `varchar`, `text` | `String` |
| `getDate` / `getTime` | `date`, `time`, `datetime` | `java.sql.Date` / `java.sql.Time` |

메서드 이름이 **자바 쪽 타입**이고 컬럼의 SQL 타입은 그것과 호환되면 된다 — `varchar` 컬럼을 `getInt` 로 읽는 것도 내용이 숫자면 통한다. 즉 이 표는 「반드시 이 짝」이 아니라 **어긋나도 조용히 통하는 자리**이고, 그것이 뒤에 함정을 만든다 → [[sql-data-type]] · [[data-type]] · [[type-casting]]

### 컬럼을 고르는 두 방법

Day57 의 두 줄이 규칙이다 — 「SELECT한 컬럼 순서대로 1~n 까지 구성된다」·「컬럼이름으로 대체 가능하다」.

```java
rs.getInt(1);            // 프로젝션 순서. 1부터
rs.getInt("user_id");    // 컬럼 이름 (또는 as 별칭)
```

**번호는 테이블의 컬럼 순서가 아니라 내가 쓴 `select` 목록의 순서**다. `select name, no` 라고 적으면 `no` 가 2번이다. 그래서 번호로 읽는 코드는 **`select` 목록을 손대는 순간 뜻이 바뀌고**, 이름으로 읽는 코드는 그대로 있다 → [[one-based-numbering]] · [[dql]]

## 사용 예시

Day57 의 실습 DAO 에 **같은 커서를 읽는 두 형태**가 나란히 있다. 갈리는 것은 몇 행을 기대하는가다.

```java
List<Project> list() throws Exception{
  try (PreparedStatement stmt = con.prepareStatement(select 쿼리문);
          ResultSet rs = stmt.executeQuery()) {
    ArrayList<Project> list = new ArrayList<>();
    while (rs.next()) {                       // 여러 행 — 있는 만큼 돈다
      Project project = new Project();
      project.setNo(rs.get(컬럼명));
      list.add(project);
    }
    return list;
  }
}

Project findBy(int no) throws Exception{
  ...
    if (rs.next()) {                          // 한 행 — 있으면 담고 없으면 null
      Project project = new Project();
      project.setNo(rs.get(컬럼명));
      return project;
    }
    return null;
}
```

**`while` 과 `if` 가 그 조회의 계약을 적은 것**이다. `findBy(no)` 는 [[primary-key]] 로 찾으므로 행이 0 또는 1이고, `list()` 는 0 이상이다. 이 판단이 SQL 이 아니라 자바 제어문에 들어 있어서, **`where` 를 빠뜨린 `findBy`** 는 오류 없이 「첫 행」을 돌려준다 → [[if-statement]] · [[while-loop]]

그리고 **커서를 다 읽어 `ArrayList` 에 옮기는 것이 `list()` 의 본체**다. 커서는 `try` 블록을 나가면 닫히므로 밖으로 돌려줄 수 없고, 그래서 이 메서드는 **행을 자바 객체로 옮겨 담는 일**을 반드시 자기 안에서 끝낸다 → [[try-with-resources]] · [[dynamic-array]]

## 왜 중요한가

**조회 결과가 「받아 온 값」이 아니라 「열려 있는 통로」다.** 파일을 읽던 코드에서 결과는 메모리에 올라온 배열이었고 몇 번이든 다시 볼 수 있었다. 커서는 **한 방향으로 한 번**이고, 그것을 들고 있는 동안 문장과 연결이 살아 있어야 한다. 그래서 JDBC 코드의 모양이 「조회해서 담아 두고 닫는다」로 고정된다 — 담아 두지 않으면 나중에 볼 수 없기 때문이다 → [[io-stream]] · [[jdbc]]

**행과 자바 객체를 맞추는 일이 전부 손으로 남는다.** `rs.getInt("no")` → `project.setNo(...)` 를 컬럼마다 적는 것이 이 층의 노동이고, 컬럼을 하나 더 `select` 했어도 **그 줄을 쓰지 않으면 객체는 비어 있다.** 오류가 아니라 빈 필드로 나타나므로 화면에서야 발견된다 — 이 반복과 이 조용한 누락을 없애겠다고 나오는 것이 ORM 이다 → [[default-initialization]] · [[encapsulation]]

**그리고 「몇 행이 오는가」를 코드가 먼저 정해야 한다.** `if (rs.next())` 를 쓴 순간 「많아도 하나」라고 선언한 것이고, `while` 을 쓴 순간 「몇이든」이다. SQL 을 읽지 않고는 어느 쪽이 맞는지 알 수 없어서, **조회와 그 결과를 읽는 코드가 떨어져 있으면 틀리기 시작한다** → [[dql]]

## 경계와 오해

- **ResultSet ≠ 행의 집합** — Day57 의 첫 줄(「행의 집합이다」)과 셋째 줄(「커서가 있는 행의 데이터만 읽을 수 있다」)이 서로 다른 것을 말한다. 집합·컬렉션이라면 크기를 묻고(`size()`) 아무 원소나 꺼내고 두 번 훑을 수 있어야 하는데 **셋 다 못 한다.** `ResultSet` 에는 「몇 행인가」를 답하는 메서드가 없고(세려면 다 돌면서 세든가 `select count(*)` 를 따로 보낸다), 지나간 행으로 돌아갈 수 없고, 한 번 끝까지 읽으면 그것으로 끝이다. **결과가 아니라 결과를 읽는 도구**이고, 「집합」이라는 낱말이 [[array]]·`List` 의 감각을 끌고 들어오는 것이 이 개념에서 처음 걸리는 지점이다 → [[dynamic-array]]
- **`rs.get(컬럼명)` 이라는 메서드는 없다** — Day57 §2.1 의 DAO 코드가 `project.setNo(rs.get(컬럼명))` 을 **Statement 판과 PreparedStatement 판에 네 번** 쓴다. `ResultSet` 에 `get(String)` 은 없으므로 이 코드는 실행이 아니라 **컴파일에서 막힌다**(`cannot find symbol`). 소제목 「1.2.1 rs.get(컬럼번호)옵션」도 같은 이름을 쓰고 있어서 필기 안에서 일관되게 잘못 적혀 있고, 본문은 정작 `getInt`·`getString`·`getDate` 를 정확히 나열한다 — **타입마다 메서드가 따로 있다는 것이 이 API 의 핵심인데 그것을 `get` 하나로 줄여 적으면 그 사실이 사라진다.** 옳은 형태는 `project.setNo(rs.getInt("project_id"))` 다.
- **`next()` 는 조회가 아니라 이동이다 — 값을 돌려주지 않는다** — 이름이 「다음」이라서 `Iterator.next()` 처럼 **다음 값을 준다**고 읽기 쉬운데, `ResultSet.next()` 가 주는 것은 `boolean` 하나이고 값은 `getXXX` 로 따로 꺼낸다. 즉 [[iterator-pattern]] 의 `hasNext()` + `next()` 두 메서드가 **여기서는 `next()` 하나에 합쳐져** 있다 — 「있는지 확인」과 「앞으로 이동」이 같은 호출이다. 그래서 `next()` 를 두 번 부르면 한 행을 건너뛰고, 조건문에 두 번 쓰면(`if (rs.next()) ... rs.next()`) 조용히 행이 사라진다. **읽는 것처럼 생긴 호출이 상태를 바꾸는** 표본이다 → [[read-side-effect]]
- **커서(ResultSet) ≠ 커서 객체(Iterator)** — 같은 낱말이지만 이쪽 커서는 **DB 서버가 들고 있을 수도 있는 위치**이고 자바 객체 안의 `int cursor` 가 아니다. 그래서 커서가 유효한 조건이 「컬렉션이 안 바뀌는 것」이 아니라 **「문장과 연결이 열려 있는 것」**이다 → [[iterator-pattern]] · [[socket]]
- **`getInt` 가 `NULL` 을 `0` 으로 준다** — SQL 의 `NULL` 을 `int` 로 받을 방법이 없으므로 드라이버는 `0` 을 준다. 그래서 「값이 0인 행」과 「값이 없는 행」이 자바 쪽에서 **구별되지 않는다.** 구별하려면 값을 읽은 **직후** `rs.wasNull()` 을 묻거나 `getObject` 로 받아 `null` 검사를 한다(`getString` 은 `null` 을 그대로 준다). Day57 의 필기에는 이 갈래가 없고, 「합계가 0이라 안 나온 줄 알았는데 값이 없던 것」이 여기서 시작된다 → [[sql-null]] · [[wrapper-class]] · [[default-initialization]]
- **`getInt : number` 는 MySQL 의 타입이 아니다** — `number` 는 Oracle 의 숫자 타입이고 MySQL 에는 `int`·`bigint`·`decimal` 이 있다. Day57 이 실습에서 쓰는 것은 MySQL 이므로 이 한 줄은 **다른 DB 의 이름이 섞여 들어온 것**이고, `number`(Oracle) 는 소수·큰 수를 다 담는 타입이라 `getInt` 로 읽으면 **소수부가 잘리거나 넘친다** — 그쪽에서는 `getBigDecimal` 이 맞다. 「어느 DB 든 같은 표」로 읽으면 [[jdbc]] 가 통일해 주지 않는 자리(타입 이름)를 통일된 것으로 착각한다 → [[sql-data-type]] · [[floating-point]]
- **컬럼 번호는 「1부터」이고 배열은 0부터다** — `getInt(1)` 이 첫 컬럼이다. 같은 코드 안에서 `String[] arr` 은 `arr[0]` 이 첫 원소이므로, 컬럼을 배열로 옮기는 반복문에서 `-1` 보정이 붙는다. 그리고 `getInt(0)` 은 「첫 컬럼」이 아니라 **오류**다 → [[one-based-numbering]] · [[array]]
- **번호로 읽는 것이 짧지만 `select *` 와 함께 쓰면 깨진다** — 번호가 프로젝션 순서를 따르므로 `select *` 로 읽으면 순서를 **테이블 정의가 정한다.** 누가 `alter table ... add column` 을 중간에 하거나 컬럼 순서를 바꾸면 **쿼리도 자바도 안 바뀌었는데 값이 엉뚱한 필드로 들어간다** — 타입이 같으면 예외도 없다. 이름으로 읽으면 이 사고가 없어서 실무는 이름을 쓰고, 이름이 없는 결과(→ [[generated-keys]] 의 `getGeneratedKeys()`)에서만 번호를 쓴다 → [[ddl]]
- **`as` 별칭을 주면 원래 컬럼 이름으로는 못 읽는다** — `select count(*) as cnt` 를 `rs.getInt("count(*)")` 로 읽을 수 없고 `"cnt"` 여야 한다. 함수·계산식의 결과는 **이름이 없거나 드라이버가 지은 이름**이라서, 별칭이 「보기 좋게」가 아니라 **읽기 위한 필수**가 되는 자리가 여기다 → [[aggregate-function]] · [[dql]]
- **커서를 메서드 밖으로 돌려주면 이미 닫혀 있다** — `ResultSet` 을 `return` 하고 호출한 쪽에서 `next()` 를 돌리는 형태는 [[try-with-resources]] 블록을 나가는 순간 `Statement` 가 닫히고 커서도 함께 무효가 되어 **`Operation not allowed after ResultSet closed`** 로 끝난다. Day57 의 `list()` 가 `ArrayList` 로 옮겨 담아 돌려주는 것이 그래서 우회가 아니라 **정석**이다 — DAO 의 반환 타입이 `List<Project>` 인 이유가 여기에 있다 → [[dynamic-array]]
- **기본 커서는 앞으로만, 한 번만 간다** — JDBC 기본값이 `TYPE_FORWARD_ONLY`·`CONCUR_READ_ONLY` 다. `beforeFirst()`·`absolute(n)` 같은 이동은 `Statement` 를 만들 때 스크롤 가능 타입으로 요청해야 하고, 요청하지 않으면 예외가 난다. 「이미 읽은 결과를 다시 훑자」가 안 되므로 **두 번 볼 것은 자바 컬렉션에 담아 두는 것이 유일한 방법**이다.
- **「커서가 있는 행만 읽는다」가 「한 행씩 서버에서 가져온다」는 뜻은 아니다** — MySQL Connector/J 는 기본적으로 결과 **전체를 클라이언트 메모리로 먼저 받아** 놓고 `next()` 는 그 안에서 위치만 옮긴다. 그래서 「커서라서 메모리를 아낀다」는 기본 설정에서 사실이 아니고, 1000만 행을 `select` 하면 `OutOfMemoryError` 가 **DB 가 아니라 자바 쪽에서** 난다. 진짜 한 행씩 받으려면 `setFetchSize(Integer.MIN_VALUE)`(MySQL) 또는 커서 기반 페치를 켜야 한다 — **커서라는 추상은 「어디까지 읽었나」를 말할 뿐 데이터가 어디 있는지는 말하지 않는다** → [[garbage-collection]] · [[caching]]
- **`if (rs.next())` 를 빼먹으면 「값이 없다」가 「잘못 읽었다」로 나타난다** — 커서가 첫 행 앞에 있는 상태에서 `getInt(1)` 을 부르면 `SQLException` 이고, 메시지는 **결과 집합 위치가 잘못됐다**는 말이라 원인(조건에 맞는 행이 없음)을 가리키지 않는다. [[generated-keys]] 의 `keyRS.next();` 가 반환값을 버리는 것이 같은 자리이고, Day57 §2.1 이 그 코드를 두 판 모두 그대로 옮겨 왔다 → [[exception-handling]]

## 함께 보는 개념

- [[jdbc]] — 이 커서가 사는 층. `Connection` → `Statement` → `ResultSet` 의 마지막
- [[prepared-statement]] — 같은 커서를 얻는 다른 문장 객체
- [[generated-keys]] — 이름 없는 컬럼 하나뿐인 특수한 `ResultSet`
- [[dql]] — 커서가 무엇을 담는지 정하는 `select`
- [[try-with-resources]] — 커서를 닫는 규율. `list()` 가 담아 돌려주는 이유
- [[iterator-pattern]] · [[read-side-effect]] — `next()` 가 이동과 확인을 겸하는 모양
- [[one-based-numbering]] — 컬럼 번호가 1부터인 자리
- [[sql-null]] · [[wrapper-class]] — `NULL` 이 `0` 으로 오는 문제
- [[sql-data-type]] · [[data-type]] — 메서드 이름이 정하는 타입 대응
- [[dynamic-array]] — 커서를 옮겨 담는 그릇
- [[crud]] — `findBy` 와 `list` 가 `if` 와 `while` 로 갈리는 자리
- [[default-initialization]] — 읽지 않은 컬럼이 조용히 비어 있는 이유

## 출처

- [[2024-08-16-Day57]] — 「1.2 ResultSet 생성」 세 줄과 코드로 이 개념이 등장한다. 「select문에 기술된 컬럼으로 구성된 행의 집합」·「커서가 있는 행의 데이터만 읽을 수 있다」와 `if(rs.next()){ rs.getXXXX(컬럼 번호) }` 가 커서·이동·읽기의 세 조각을 정확히 세우고, 이어지는 「1.2.1」이 타입별 메서드 세 갈래(`getInt`·`getString`·`getDate`/`getTime`)와 컬럼 번호 규칙(「SELECT한 컬럼 순서대로 1~n」·「컬럼이름으로 대체 가능」)을 적었다. 실습 DAO 에서는 `while (rs.next())` 로 목록을, `if (rs.next())` 로 단건을 읽는 두 형태가 나란히 나온다. 다만 「행의 집합」이라는 첫 줄은 셋째 줄과 어긋나고(집합이 아니라 커서다), 소제목과 DAO 코드가 실제로 없는 메서드 `rs.get(컬럼명)` 을 네 번 쓰며, `getInt` 의 대응 타입에 MySQL 에 없는 Oracle 타입 `number` 가 섞여 있다. `NULL` 을 읽었을 때(`wasNull`)와 커서가 앞으로만 간다는 성질은 필기에 없다
