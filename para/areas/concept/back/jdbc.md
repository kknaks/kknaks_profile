---
type: concept
id: jdbc
title: JDBC (Java Database Connectivity)
aliases:
  - JDBC
  - Java Database Connectivity
  - JDBC 드라이버
  - jdbc driver
  - JDBC-ODBC Bridge
tags:
  - java
  - database
  - 드라이버
  - jvm
up:
  - 2024-08-09-Day53
  - 2024-08-13-Day55
  - 2024-08-14-Day56
  - 2024-08-16-Day57
  - 2024-08-19-Day58
---

# JDBC (Java Database Connectivity)

**자바 코드가 DB 에 접속·질의할 때 부르는 표준 인터페이스 묶음과, 그 인터페이스를 DB 마다 구현해 놓은 드라이버.** Day53 은 이것을 「[[odbc]] 의 기능을 JVM에서 동일하게 구현한 드라이버」 한 줄로 정의한다. **자바 프로그램이 파일 대신 DB 에 데이터를 두게 되는 문턱**이 이 개념이다.

## 정의

이름은 [[odbc]] 를 따라 지었지만 자리가 다르다. **ODBC 가 C 함수 규격이라면 JDBC 는 자바 인터페이스 규격**이고, 규격이 언어의 타입으로 존재한다는 것이 차이의 전부다.

| | ODBC | JDBC |
|---|---|---|
| 규격의 형태 | C 함수 목록 | `java.sql` **인터페이스** 묶음 |
| 규격을 지키는 것 | OS 에 설치한 드라이버 | 클래스패스에 둔 **jar** |
| 어디까지 흡수하나 | DB 판매사 차이 | DB 판매사 차이 **+ OS 차이**([[jvm]] 이 아래를 맡는다) |
| 내 코드가 붙잡는 것 | 함수 이름 | `Connection`·`Statement`·`ResultSet` **타입** |

규격이 인터페이스라서, 내가 쓰는 변수의 타입은 전부 `java.sql` 것이고 실제 객체는 드라이버가 만든 클래스다. **[[polymorphism]] 이 회사 경계를 넘어 쓰이는 자리**다 → [[interface]]

### 드라이버 타입 — Day53 이 Type1 까지 적고 끊겼다

필기는 「Type1 : ODBC-JDBC Bridge Driver」의 두 줄에서 멈춘다. 네 타입은 **자바 코드에서 DB 까지 가는 경로에 무엇을 끼우는가**로 갈린다.

| 타입 | 이름 | 경로 | 지금 |
|---|---|---|---|
| **1** | JDBC-ODBC Bridge | Java → JDBC → **ODBC 드라이버** → Native API → DB | **JDK 8 에서 제거됐다** |
| 2 | Native-API (Thick) | Java → JDBC → 벤더가 준 **C 라이브러리** → DB | 기계마다 그 라이브러리를 설치해야 한다 |
| 3 | Network Protocol | Java → JDBC → **미들웨어 서버** → 각 DB | 드물다 |
| **4** | Thin (순수 자바) | Java → JDBC → **소켓으로 DB 프로토콜 직접** | 표준. `mysql-connector-j` 가 이것 |

Type1 은 「ODBC 를 자바에서 부른다」이므로 Day53 의 정의 한 줄과 정확히 맞물리고, **Type4 는 ODBC 를 아예 거치지 않는다.** 번호가 커질수록 중간에 끼운 것이 사라지고, 마지막에는 드라이버가 **DB 서버와 직접 말하는 자바 코드**만 남는다 — Day45~46 에서 배운 소켓 통신이 그대로 드라이버 안에 들어 있는 것이다 → [[socket]] · [[network-protocol]] · [[port-number]]

**Type1·2 가 「설치」를 요구하고 Type4 가 「의존성 추가」로 끝난다.** 이 한 줄이 왜 Type4 만 살아남았는지의 답이다.

### Day55 — 인터페이스 세 개가 코드로 나타난다

Day53 은 규격과 드라이버 타입까지였고, **`java.sql` 타입이 실제 코드로 보이는 것은 나흘 뒤 Day55 의 DAO 다.** 세 타입이 서로를 만들어 주는 순서로 이어진다.

```java
try (Statement stmt = con.createStatement()) {          // Connection → Statement
  ResultSet rs = stmt.executeQuery("select ...");       // Statement → ResultSet
  while (rs.next()) {                                   // 커서를 한 행씩 옮긴다
    user.setNo(rs.getInt("user_id"));
    user.setName(rs.getString("name"));
  }
}
```

| 타입 | 무엇을 들고 있나 | 어디서 얻나 |
|---|---|---|
| `Connection` | DB 서버와 열린 연결 하나 | `DriverManager.getConnection` |
| `Statement` | 그 연결로 보낼 한 번의 질의 | `con.createStatement()` |
| `ResultSet` | 돌아온 결과 위의 **커서** | `stmt.executeQuery(...)` |

**`ResultSet` 이 결과의 사본이 아니라 커서라는 것**이 이 코드 모양을 정한다 — `while (rs.next())` 로 한 행씩 앞으로 가며 읽고, 다 읽기 전에 연결이나 문장을 닫으면 남은 행을 잃는다. 그리고 **행을 자바 객체로 옮기는 일은 아무도 해 주지 않는다** — `rs.getInt`·`rs.getString` 을 컬럼마다 손으로 적어 `User` 에 담는 코드가 그것이고, 이 반복을 없애겠다고 나오는 것이 나중의 ORM 이다.

문장을 실행하는 메서드는 **무엇을 돌려받는지에 따라** 갈린다 — `executeQuery` 는 `ResultSet`(조회), `executeUpdate` 는 **바꾼 행 수**(등록·변경·삭제)다. Day55 의 `deleteMembers` 가 `executeUpdate` 의 반환값을 버리는데, 「몇 행을 지웠는가」는 그 값에만 있다. **사흘 뒤 Day57 의 DAO 가 그 값을 `return count > 0` 으로 쓰기 시작한다** → [[dql]] · [[dml]] · [[crud]]

### Day56 — 드라이버를 준비하고, 등록하고, 연결한다

Day55 는 이미 `Connection` 을 들고 있는 상태에서 시작했다. **그 앞의 세 걸음**(jar 를 들이고 → 드라이버를 등록하고 → 연결을 얻는다)을 하루 뒤 Day56 이 소제목으로 세운다. 다만 **본문이 채워진 것은 첫 걸음뿐이고 나머지 둘은 이름만 남았다** — 아래가 그 자리에 들어갈 답이다.

#### ① 준비 — 드라이버는 좌표 한 줄이다

Day56 이 벤더 넷의 좌표를 나란히 적었다. **드라이버가 「받아서 설치하는 것」이 아니라 [[gradle]] 의 `dependencies` 한 줄**이라는 것이 이 목록의 요지다 → [[build]] · [[classpath]]

| DBMS | 좌표 | 이름에 든 것 |
|---|---|---|
| Oracle | `com.oracle.database.jdbc:ojdbc11-production:21.15.0.0` | `11` 은 **대상 자바 11**, `production` 은 여러 jar 를 함께 끌어오는 묶음 |
| MS-SQL | `com.microsoft.sqlserver:mssql-jdbc:12.8.0.jre11` | 버전 끝의 `.jre11` 도 **대상 자바 버전** |
| MySQL | `com.mysql:mysql-connector-j:8.4.0` | `-j` 는 자바용. 그룹이 `com.mysql` 로 바뀐 뒤의 이름 |
| MariaDB | `org.mariadb.jdbc:mariadb-java-client:3.4.1` | MySQL 드라이버와 **별개 구현** |

넷 다 하는 일은 같다 — `java.sql` 인터페이스를 자기 DB 프로토콜로 구현한 위 표의 **Type4** jar 다. **좌표만 갈아 끼우면 되는 것처럼 보이는 것이 이 표의 함정**이고, 그것이 아래 「경계와 오해」의 첫 항목이다.

#### ② 등록 — 다섯 갈래는 사실 셋이 같고 하나가 이긴다

Day56 은 다섯 소제목만 남겼다(`DriverManager.registerDriver` · `new jdbc.Driver경로` · `Class.forName("jdbc.Driver경로")` · `propreties` · `service-provider loading`). 다섯이 하는 일은 **`DriverManager` 가 들고 있는 드라이버 목록에 하나를 넣는 것** 하나이고, 갈리는 것은 **누가 넣는가**와 **벤더 이름이 어디에 박히는가**다.

```java
DriverManager.registerDriver(new com.mysql.cj.jdbc.Driver());  // ① 내가 직접 넣는다
new com.mysql.cj.jdbc.Driver();                                // ② 만들기만 한다
Class.forName("com.mysql.cj.jdbc.Driver");                     // ③ 이름으로 로딩한다
```

```bash
$ java -Djdbc.drivers=com.mysql.cj.jdbc.Driver bitcamp.myapp.App   # ④ 시스템 프로퍼티
```

```text
mysql-connector-j-8.4.0.jar
└── META-INF/services/java.sql.Driver     ← ⑤ 이 파일에 클래스 이름이 적혀 있다
```

| 갈래 | 등록을 **실제로** 하는 것 | 벤더 이름이 박히는 곳 | 지금 |
|---|---|---|---|
| ① `registerDriver` | 내 코드 | **컴파일되는 타입** | 안 쓴다 |
| ② `new ...Driver()` | 그 클래스의 **static 초기화** | **컴파일되는 타입** | 안 쓴다 |
| ③ `Class.forName` | 같은 **static 초기화** | **문자열** | 옛 코드에 남아 있다 |
| ④ `-Djdbc.drivers=` | `DriverManager` 의 static 초기화 | **실행 인자** | 드물다 |
| ⑤ service-provider loading | `ServiceLoader` 가 jar 속 목록을 읽는다 | **jar 안** | **이것. 내 코드는 한 줄도 없다** |

**①②③ 은 같은 장치를 세 거리에서 본 것이다.** 벤더의 `Driver` 클래스 안에는 `static { DriverManager.registerDriver(new Driver()); }` 가 들어 있고, 그 static 블록은 **클래스가 로딩될 때 한 번** 돈다 — 그래서 ② 는 만든 객체를 버려도 등록이 되고(등록된 것은 내가 만든 것이 아니라 static 블록이 만든 다른 인스턴스다), ③ 은 객체를 아예 만들지 않아도 된다 → [[static-member]] · [[class-metadata]]

**차이는 「벤더 이름이 컴파일되는가」다.** ① ② 는 `com.mysql.cj.jdbc.Driver` 를 타입으로 적으므로 그 jar 없이는 **컴파일이 안 되고**, DB 를 바꾸면 자바 코드를 고쳐야 한다. ③ 은 같은 이름이 **문자열**이라 설정 파일에서 읽어올 수 있고 — 이것이 Day56 의 「properties 구현」이 원래 향하는 곳이다 — ④ 는 그 문자열을 실행 명령으로 옮긴다. ⑤ 는 이름을 **드라이버가 스스로 신고**하게 해서 내 쪽에서 아예 없앤다.

#### ③ 연결 — URL 의 두 번째 조각이 드라이버를 고른다

Day56 은 「DBMS 연결구조」·「DBMS close」 두 줄만 남겼다. 들어갈 것은 위 Day55 절의 표 첫 줄, `DriverManager.getConnection` 이다.

```java
String url = "jdbc:mysql://localhost:3306/studydb";
try (Connection con = DriverManager.getConnection(url, "study", "1111")) {
  // ...
}
```

| 조각 | 이름 | 하는 일 |
|---|---|---|
| `jdbc:` | 프로토콜 | 이 문자열이 JDBC URL 이라는 표시 |
| `mysql:` | **서브프로토콜** | **어느 드라이버가 이 URL 을 맡는지 고른다** |
| `//localhost:3306/studydb` | 서브네임 | 그 드라이버만 해석하는 주소·포트·DB 이름 |

`getConnection` 은 등록된 드라이버들에게 차례로 「이 URL 네 것이냐」를 묻고 처음 그렇다고 한 드라이버에게 연결을 만들게 한다. **그래서 「등록」이 「연결」 앞에 있는 것이 순서상 필연**이고, 등록이 빠졌을 때의 오류는 접속 실패가 아니라 `No suitable driver found for jdbc:mysql://...` — **DB 가 죽은 것처럼 읽히지 않는 메시지**다 → [[database-user]] · [[port-number]]

「close」는 **얻은 순서의 역순**이다(`ResultSet` → `Statement` → `Connection`). Day55 가 이미 `try (Statement stmt = ...)` 로 문장만 감쌌으므로, 연결까지 같은 괄호로 올리는 것이 이 자리에서 남은 한 걸음이다 → [[try-with-resources]]

### 이틀 뒤 Day57 — 이 API 의 표면이 한 번에 채워진다

Day53 이 규격, Day55 가 DAO 코드, Day56 이 그 앞의 세 걸음이었다. **Day57 은 「1. JDBC 기본 사용법」이라는 제목으로 이 API 를 처음부터 다시 세운다** — 지금까지 흩어져 나온 것이 한 회차 안에서 순서를 갖는다.

| Day57 의 절 | 무엇을 채우나 | 상세를 가진 노트 |
|---|---|---|
| 1.1 SQL문 보내기 | `createStatement` 와 `executeUpdate`/`executeQuery` 의 **반환값**, `insert`·`update`·`delete`·`select` 네 형태 | 이 노트 |
| 1.2 ResultSet 생성 | 커서·`next()`·`getXXX`·컬럼 번호 | [[result-set]] |
| 1.3 Statment의 문제점 | 문자열 조립이 부르는 공격 | [[sql-injection]] |
| 1.3.1 PreparedStatement | 값을 `?` 로 분리하는 문법 | [[prepared-statement]] |
| 1.4 Primary Key return | 자동 생성 키 되받기 | [[generated-keys]] |
| 1.5 AutoCommit옵션 | 커밋 경계를 자바에서 여닫기 | [[transaction]] |

**이 순서가 곧 논증이다.** `Statement` 로 네 문장을 보내는 법을 배우고(1.1) → 결과를 읽고(1.2) → **그 방식이 위험하다는 것을 보고**(1.3) → 대체 문법으로 옮기고(1.3.1) → 서버가 만든 값을 되받고(1.4) → 여러 문장을 한 덩어리로 묶는다(1.5). 「배운 것을 바로 폐기하는」 절(1.3)이 중간에 있는 것이 이 회차의 특징이고, 그래서 **Day55 의 DAO 는 이 회차 기준으로 이미 옛 형태**다.

Day57 이 이 노트 쪽에 더하는 것은 **문장을 보내는 네 형태와 그 반환값**이다.

```java
Statement stmt = con.createStatement();
stmt.exceuteUpdate("insert into 테이블명(컬럼,컬럼...) values(값,값,....) ");   // 변경된 행 수
stmt.exceuteUpdate("update 테이블명 set 컬럼=값 where 조건 ");                  // 변경된 행 수
stmt.exceuteUpdate("delete from 테이블명 where 조건");                          // 변경된 행 수
ResultSet rs = stmt.executeQuery("select 컬럼명 from 테이블명");                 // 커서
```

(필기 전체가 `exceuteUpdate` 로 적혀 있다 — 철자만 오기이고 자리는 맞다.) **셋이 같은 메서드를 부르고 하나만 다르다**는 것이 [[dml]] 과 [[dql]] 의 구분이 API 로 나타난 모양이다. Day57 은 그 이유까지 적었다 — 「select문은 jvm에 반환된 컬럼을 받아와야 하기 때문에 ResultSet 타입으로 가져온다」.

그리고 **`delete` 절에 자바 쪽 순서 문제가 하나 붙는다.**

```java
stmt.exceuteUpdate("delete from 자식_테이블명 where FK조건");
stmt.exceuteUpdate("delete from 부모_테이블명 where 조건");
```

한 번의 삭제가 **문장 둘**이 되는데, 이것은 JDBC 가 만든 제약이 아니라 [[foreign-key]] 의 기본 동작(`RESTRICT`)이 코드로 나타난 것이다. 그리고 문장이 둘이 된 순간 「앞만 되고 뒤가 안 되는」 경우가 생기므로, 같은 회차 뒤쪽의 1.5 절이 필요해진다 → [[transaction]]

### 사흘 뒤 Day58 — 이 API 를 쓰는 대신 감싸기 시작한다

Day53~57 은 이 API 를 **배우고 쓰는** 회차였다. **Day58 에서 방향이 바뀐다** — 「Sql 세션 만들기」라는 제목으로, 문장을 준비하고 값을 채우고 실행하고 닫는 네 단계를 메서드 하나 뒤로 넣은 클래스를 손으로 만든다 → [[sql-session]]

```java
public int insert(String sql, Object... values) throws Exception { ... }   // 준비·바인딩·실행·닫기
public int update(String sql, Object... values) throws Exception { return insert(sql, values); }
public int delete(String sql, Object... values) throws Exception { return insert(sql, values); }
```

**세 메서드가 한 본문을 공유하는 것이 이 API 의 성질을 그대로 비춘다** — `insert`·`update`·`delete` 를 가르는 호출이 JDBC 에 없고 셋 다 `executeUpdate()` 하나로 가기 때문이다. 위 Day55 절에서 「이 반복을 없애겠다고 나오는 것이 ORM 이다」라고 적은 그 반복 중 **절반**이 이 회차에 사라진다. 남는 절반은 조회 쪽이다 — 행을 자바 객체로 옮기는 일은 세션이 **무엇으로 만들지 알아야** 하므로 「selectList 만들기」가 빈 코드 블록으로 남았고, 그 자리를 메우려면 타입 정보를 밖에서 받아야 한다(MyBatis 의 `resultType`) → [[result-set]] · [[dml]]

그리고 **감싸도 남는 것 셋**이 이 층의 표면이 어디까지인지를 알려 준다: SQL 문자열은 여전히 호출부에 있고, 커밋 경계는 `Connection` 의 메서드이므로 화면 코드가 계속 `con` 을 들고 있어야 하고, 자동 생성 키는 준비 시점 플래그라 감싼 메서드로는 요청할 수 없다 → [[transaction]] · [[generated-keys]] · [[prepared-statement]]

## 왜 중요한가

**저장할 곳이 파일에서 DB 로 옮겨간다.** Day30 무렵부터 실습은 데이터를 `.data`·`.csv`·엑셀로 직접 읽고 썼다. 그 코드가 하던 일 — 형식 정하기, 다 읽어 메모리에 올리기, 바뀔 때마다 전체 다시 쓰기 — 을 JDBC 를 타고 서버에 맡기면 **조건 조회와 부분 수정이 문장 한 줄**이 된다. 파일 저장이 감당하지 못했던 것이 여기서 처음 해결된다 → [[io-stream]] · [[csv]] · [[apache-poi]] · [[dml]] · [[dql]]

**자바 코드가 어느 DB 인지 모르는 상태로 쓰인다.** 컴파일 시점에 내 코드가 아는 것은 `java.sql` 인터페이스뿐이고, 실물 구현은 실행할 때 클래스패스에서 온다. 그래서 **DB 를 바꾸는 일이 「jar 를 바꾸고 접속 URL 을 바꾸는 일」**로 줄어들고 — Day56 이 벤더 넷의 좌표를 **같은 자리에 나란히** 적을 수 있었던 것이 그 증거다 — 반대로 **jar 를 빠뜨리면 컴파일은 되는데 실행에서만 터진다** — 오류를 만나는 시점이 컴파일에서 런타임으로 옮겨간 것이다 → [[classpath]] · [[gradle]] · [[build]] · [[exception-handling]]

**그리고 「등록」이 사라진 것을 모르면 없는 문제를 고치려 든다.** Day56 이 다섯 갈래를 나열한 것은 그 시점에도 예제 코드마다 `Class.forName` 이 한 줄씩 들어 있었기 때문이고, 그 한 줄은 **2006년 JDBC 4.0 이후로 필요 없어졌다.** 그래서 접속이 안 될 때 답이 「등록 코드가 빠졌나」가 아니라 거의 항상 **jar·URL·계정** 셋 중 하나라는 것을 알고 시작하는 것이 이 절의 값이다 → [[jdk]] · [[database-user]]

**그리고 Day51~52 에서 손으로 치던 것이 전부 메서드가 된다.** 접속(`'study'@'%'` 로 로그인하던 것)은 `DriverManager.getConnection`, `set autocommit = false` 는 `connection.setAutoCommit(false)`, `commit`/`rollback` 은 같은 이름의 메서드다. **SQL 을 배운 것이 API 를 배우는 일로 이어진다** — 그 메서드들이 실제로 코드에 나타나는 것은 아흐레 뒤 Day57 이다 → [[database-user]] · [[transaction]]

## 경계와 오해

- **드라이버 등록 코드는 2006년부터 필요 없다 — Day56 의 다섯 갈래 중 넷은 이미 유물이다** — JDBC 4.0(Java 6)부터 `DriverManager` 는 첫 사용 시 `ServiceLoader` 로 클래스패스의 jar 들을 훑어 `META-INF/services/java.sql.Driver` 에 적힌 클래스를 **스스로 로딩한다.** 즉 ⑤ service-provider loading 은 「다섯 번째 방법」이 아니라 **①~④ 를 전부 불필요하게 만든 기본 동작**이다. Day56 이 다섯을 나란히 놓은 것은 배우는 순서로는 맞지만 **선택지 다섯 개로 읽으면 틀린다** — 지금 새로 쓰는 코드에 등록 줄을 넣을 이유는 없다. 다만 옛 예제에서 `Class.forName` 을 지웠더니 되는 것을 보고 「지워도 되는 줄」로만 기억하면, **그것이 왜 되는지**(jar 안의 신고 파일)를 모른 채 남아서, 그 파일이 없는 옛 드라이버나 셰이드된 fat jar 에서 갑자기 `No suitable driver` 를 만난다 → [[jdk]] · [[classpath]]
- **`new Driver()` 가 등록하는 것은 내가 만든 그 객체가 아니다** — 「인스턴스를 만들면 등록된다」로 외우면 `new` 가 등록 행위처럼 보인다. 실제로 등록을 하는 것은 그 클래스의 `static` 초기화 블록이고, 그 블록이 **자기가 만든 별개의 인스턴스**를 `DriverManager` 에 넣는다. 내가 만든 객체는 참조도 안 남기고 버려진다. 이 구분이 없으면 ③ `Class.forName` 이 **객체를 하나도 만들지 않는데도** 왜 같은 결과인지 설명되지 않는다 — 등록의 방아쇠는 생성이 아니라 **클래스 로딩**이다 → [[static-member]] · [[class-metadata]]
- **`jdbc.drivers` 시스템 프로퍼티 ≠ 애플리케이션 `.properties` 파일** — Day56 에는 「properties」가 두 군데 나오고 서로 다른 것이다. 「JDBC 드라이버 등록」 아래의 것(원문 표기 `propreties`)은 JVM 실행 인자 `-Djdbc.drivers=...` 로 주는 **시스템 프로퍼티**이고 `DriverManager` 가 읽는다. 「실습프로젝트」 아래의 「properties 구현」은 **내 코드가 읽는 설정 파일**(URL·계정을 소스에서 빼는 것)이다. 둘을 겹쳐 읽으면 「`db.properties` 에 드라이버 이름을 적었는데 등록이 안 된다」에서 막힌다 — 파일에 적은 값은 **내가 꺼내서 쓰지 않으면 아무도 읽지 않는다.**
- **좌표 넷을 다 넣는 것은 「DB 를 안 고르고 두는」 것이 아니다** — Day56 의 목록은 벤더별 좌표의 **참고표**인데, 그대로 `dependencies` 에 붙이면 쓰지 않는 드라이버 세 개가 컴파일·실행 클래스패스와 배포 산출물에 함께 실린다. Oracle 쪽 `ojdbc11-production` 은 특히 단일 jar 가 아니라 **부속 jar 를 여러 개 끌고 오는 묶음 좌표**라서 늘어나는 양이 한 줄처럼 보이지 않는다. 등록이 자동(⑤)이므로 **넣어 둔 드라이버는 전부 등록되고**, URL 서브프로토콜이 겹치는 MySQL/MariaDB 를 함께 두면 `jdbc:mysql:` 을 어느 쪽이 맡을지가 클래스패스 순서에 달린다 — **「일단 다 넣어 두자」가 재현되지 않는 접속 문제로 돌아오는 자리**다 → [[gradle]] · [[build]]
- **`mariadb-java-client` 는 MySQL 드라이버의 다른 이름이 아니다** — MariaDB 가 MySQL 에서 갈라져 나왔고 SQL 도 거의 같아서 「같은 것」으로 묶기 쉽지만, 이 둘은 **별개 회사가 각각 구현한 별개 드라이버**다. 프로토콜 호환 범위 안에서는 서로 붙기도 해서 **한동안 돌아가다가** 인증 플러그인·타임존·`useSSL` 같은 접속 옵션 이름에서 갈린다. 「돌아가니까 맞다」가 또 한 번 덮는 자리다.
- **버전 문자열 끝의 `jre11`·`ojdbc11` 은 DB 버전이 아니다** — `mssql-jdbc:12.8.0.jre11` 의 `12.8.0` 이 드라이버 버전이고 `jre11` 은 **이 jar 가 겨냥한 자바 버전**이며, 같은 드라이버 버전에 `jre8`·`jre11` 이 따로 올라온다. Oracle 의 `ojdbc11` 도 같은 축이다(Oracle DB 11g 가 아니라 **Java 11**). 좌표를 DB 버전에 맞추려 들면 엉뚱한 것을 고른다 — **맞춰야 하는 것은 실행할 JDK** 다 → [[jdk]] · [[platform-dependency]]
- **`mysql:mysql-connector-java` 로 검색하면 멈춘 것이 나온다** — Day56 이 적은 `com.mysql:mysql-connector-j` 가 현재 이름이고, 8.0.31 을 기점으로 그룹과 이름이 함께 바뀌었다. 옛 블로그를 따라 예전 좌표를 쓰면 받아지기는 하는데 **거기서 버전이 더 올라가지 않는다.** 좌표는 라이브러리의 주소이고 **주소가 이사할 수 있다**는 것이 [[gradle]] 의 「좌표를 복사해 온다」에 딸린 조건이다.
- **「JRE에 기본적으로 포함된 드라이버」는 2024년에 이미 틀린 문장이다** — Type1 브리지(`sun.jdbc.odbc.JdbcOdbcDriver`)는 **JDK 8 에서 제거됐다.** 지금 쓸 수 있는 어떤 JDK 에도 없으므로, 필기대로 Type1 을 시험하면 접속 실패가 아니라 **클래스를 못 찾는 오류**(`ClassNotFoundException`)가 난다. 필기가 「기본 포함」이라 적은 것은 **Type1 의 정의가 아니라 그 시절의 배포 상태**였고, 그 상태가 이미 끝났다. 오늘 자바에서 DB 에 붙는다는 것은 사실상 전부 Type4 다 → [[jdk]]
- **JDBC ≠ ODBC 위에 얹힌 층** — 「ODBC 의 기능을 JVM에서 동일하게 구현」은 **Type1 에만 맞는 설명**이다. 실제로 쓰는 Type4 드라이버는 ODBC 를 거치지 않고 DB 의 통신 규약을 직접 구현한다. 즉 JDBC 는 ODBC 를 감싼 것이 아니라 **같은 문제에 대한 자바의 별도 규격**이고, 두 이름이 닮은 것은 설계를 참고했기 때문이다. 「JDBC 를 쓰려면 ODBC 드라이버를 깔아야 한다」로 읽으면 필요 없는 설치를 찾아 헤맨다.
- **JDBC 는 규격이고 드라이버는 구현이다 — 그런데 필기는 JDBC 를 「드라이버」라 부른다** — 「JVM에서 동일하게 구현한 드라이버」라는 한 줄에 규격과 구현이 겹쳐 있다. 갈라 보면 `java.sql` 인터페이스는 **JDK 에 들어 있고**(그래서 `import java.sql.Connection` 이 항상 된다), 그것을 구현한 드라이버 jar 는 **내가 따로 넣는다.** 「import 가 되는데 실행이 안 되는」 상황이 정확히 이 둘의 간격이다 → [[classpath]]
- **드라이버 「설치」와 「의존성 추가」는 다르다** — ODBC 드라이버는 **OS 에** 설치하고 등록해서 기계를 옮길 때마다 다시 해야 하지만, Type4 JDBC 드라이버는 **빌드 결과물 안에 들어가는 jar 한 개**다. 그래서 「내 컴퓨터에서는 됐는데」가 드라이버 때문에 생기는 일이 거의 없다 — 배포에 함께 실려 가기 때문이다 → [[gradle]] · [[build]] · [[platform-dependency]]
- **JDBC 가 통일하는 것은 접속과 호출이지 SQL 이 아니다** — [[odbc]] 와 같은 한계를 그대로 물려받는다. `Statement` 에 넣는 문자열은 여전히 그 DB 의 방언이고, MySQL 에 붙던 코드가 Oracle 에서 `limit` 하나로 깨진다. 이 층이 흡수하지 않는 것을 나중에 흡수하겠다고 나오는 것이 JPA·ORM 이다 → [[sql-data-type]] · [[sql-date-function]]
- **SQL 을 문자열로 조립하는 것이 이 API 의 기본형이고, 그것이 곧 문제가 된다** — Day55 의 DAO 는 `String.format("insert ... values (%d,%d)", ...)` 와 `"where pm.project_id = " + projectNo` 로 질의를 만든다. 넣는 값이 `int` 라 당장은 사고가 나지 않지만, **문자열 값이 오는 순간 두 가지가 함께 온다**: 이름에 `'` 가 하나 있으면 문장이 깨지고(오도철 → 문법 오류), 값 자리에 SQL 을 써 넣으면 그대로 실행된다(SQL 인젝션). 그래서 `Statement` + 문자열 조립은 **연습용 형태**이고, 값을 `?` 로 두고 따로 넣는 `PreparedStatement` 가 실무의 기본이다. 값이 문장의 일부가 되는가 아니면 문장 밖에서 전달되는가의 차이다. **Day55 에는 그 이름이 없고, 사흘 뒤 Day57 이 「Statment의 문제점」이라는 절을 따로 세워 이 위험을 적은 뒤 `PreparedStatement` 로 넘어간다** — 즉 이 항목은 Day55 시점의 지적이었고 그 답이 같은 주 안에 온다 → [[sql-injection]] · [[prepared-statement]] · [[format-string]] · [[literal]]
- **같은 문장을 반복 실행하는데 매번 새로 조립한다** — `insertMembers` 는 팀원마다 SQL 문자열을 만들어 `executeUpdate` 를 부른다. 서버는 그 문자열들을 **서로 다른 문장으로 보고 매번 파싱**하므로, 팀원 열 명이면 파싱도 열 번이다. `PreparedStatement` 는 뼈대를 한 번 준비하고 값만 바꿔 보내므로 이 반복이 사라진다 — **문자열 조립의 대가가 안전 문제만이 아니라 비용에도 있다.** 다만 이 코드가 이미 얻은 것도 있다: `Statement` 를 루프 밖에서 한 번 만들어 재사용하므로 **문장 객체를 팀원마다 만들지는 않는다.** 사흘 뒤 Day57 이 `PreparedStatement` 로 옮기지만 **그 이득까지 얻지는 못한다** — DAO 메서드마다 문장을 새로 준비하고 닫으므로 「한 번 준비하고 여러 번 실행」이 일어나지 않는다. 이 회차가 얻는 것은 안전이고 비용은 그대로다 → [[caching]] · [[prepared-statement]]
- **DAO 가 돌려주는 객체는 「반쯤 채워진」 것일 수 있다** — Day55 의 `getMembers` 는 `select pm.user_id, u.name` 두 컬럼만 읽어 `User` 의 `no`·`name` 만 채운다. 나머지 필드(이메일·연락처)는 `null` 인 채로 화면까지 올라가므로, 팀원 목록을 「이름만」 찍는 지금은 맞지만 **거기서 이메일을 하나 더 찍는 순간 조용히 빈칸**이 된다. 자바 객체는 「완전한 회원」처럼 생겼는데 실제로는 **그 쿼리가 고른 열만큼만 채워진 것**이고, 이 어긋남이 [[generated-keys]] 의 `setNo` 와 같은 축의 문제다 — **행과 객체는 자동으로 맞지 않는다** → [[default-initialization]] · [[dql]]
- **연결은 객체가 아니라 자원이다** — `Connection` 은 값을 담은 객체처럼 보이지만 실체는 **DB 서버와 열린 소켓 하나**이고, [[garbage-collection]] 이 대신 닫아 주지 않는다. 닫지 않은 연결이 쌓이면 서버 쪽 접속 수 상한에 먼저 부딪혀 **새 접속이 거절된다.** 파일 스트림을 닫아야 했던 것과 같은 규율이 그대로 오고, 그래서 JDBC 코드는 `try-with-resources` 로 쓰인다 → [[try-with-resources]] · [[socket]]
- **접속을 「빠른 것」으로 생각하면 안 된다** — 매 요청마다 `getConnection` 을 부르는 코드는 요청마다 TCP 연결과 인증을 새로 한다. 이것이 뒤에 커넥션 풀이 필요해지는 이유이고, 이 레포에 이미 [[connection-pool-sizing-formula]]·[[connection-lifetime-mismatch]] 로 남아 있는 문제들이 **여기서 만든 연결 하나**를 다루는 이야기다 → [[tcp]]

## 함께 보는 개념

- [[odbc]] — 이름과 설계를 물려준 앞선 표준. Day53 의 바로 앞 절
- [[jvm]] · [[jdk]] — 규격이 어디에 들어 있고 무엇이 OS 차이를 흡수하는가
- [[interface]] · [[polymorphism]] — 규격만 붙잡고 구현을 런타임에 받는 문법
- [[classpath]] · [[gradle]] · [[build]] — 드라이버 jar 가 실행 시점에 발견되게 하는 자리
- [[static-member]] · [[class-metadata]] — 드라이버 등록의 방아쇠가 클래스 로딩인 이유
- [[database-user]] — 연결에 넘기는 계정. 등록 다음에 오는 관문
- [[socket]] · [[network-protocol]] · [[port-number]] · [[tcp]] — Type4 드라이버 안에 들어 있는 것
- [[transaction]] — `setAutoCommit(false)` 로 옮겨 오는 Day52 의 실험
- [[dml]] · [[dql]] · [[ddl]] — 드라이버를 타고 서버로 보내는 문장들
- [[sql-join]] — 질의 횟수를 줄이는 쪽이 SQL 에 있다는 것을 보여 주는 문법
- [[result-set]] — `executeQuery` 가 돌려주는 커서. 결과를 읽는 쪽
- [[prepared-statement]] — 값을 문장에서 떼어 내는 문장 객체
- [[sql-injection]] — 문자열 조립이 부르는 문제. 위 문법이 답인 이유
- [[generated-keys]] — `insert` 뒤에 서버가 만든 값을 되받는 API
- [[try-with-resources]] — 연결·문장·결과를 닫는 규율
- [[connection-pool-sizing-formula]] · [[connection-lifetime-mismatch]] — 이 연결을 재사용할 때 생기는 문제
- [[io-stream]] · [[csv]] · [[apache-poi]] — DB 로 넘어가기 전에 저장을 맡고 있던 것들
- [[client-server-model]] — 프로그램이 DB 서버의 클라이언트가 된다는 사실
- [[crud]] — 등록·조회·변경·삭제 화면이 이제 SQL 로 내려가는 자리
- [[sql-session]] — 이 API 를 감싸는 층. MyBatis 의 첫 칸을 손으로 만든 것
- [[varargs]] — 그 층이 값 목록을 받는 문법

## 출처

- [[2024-08-09-Day53]] — JDBC 를 「ODBC 의 기능을 JVM에서 동일하게 구현한 드라이버」로 정의하고, 드라이버 타입 중 **Type1(ODBC-JDBC Bridge)** 만 「JRE에 기본적으로 포함된 드라이버」·「ODBC API를 호출(C함수)」 두 줄로 적은 뒤 끊긴다. 그래서 Type2~4 와 「지금 쓰는 것은 Type4」라는 결론은 이 노트가 채운다. 「JRE 에 기본 포함」은 JDK 8 에서 제거되어 이미 성립하지 않고, Day52 의 `commit`/`rollback` 이 어떻게 메서드로 오는지도 필기에는 없다
- [[2024-08-13-Day55]] — **`java.sql` 타입이 실제 코드로 처음 보이는 회차**다. `con.createStatement()` → `executeUpdate`/`executeQuery` → `ResultSet` 순회 → `rs.getInt`·`rs.getString` 으로 자바 객체에 담기까지가 실습 프로젝트의 DAO 세 메서드(`insertMembers`·`getMembers`·`deleteMembers`)에 들어 있고, 전부 `try (Statement stmt = ...)` 로 감싸여 있다. Day53 이 규격과 드라이버 타입만 다룬 뒤 **그 인터페이스를 손으로 쓰는 자리**가 여기다. 다만 질의를 `String.format` 과 문자열 결합으로 조립하므로 `PreparedStatement` 가 왜 필요한지가 드러나지 않고(필기에 그 이름이 없다), `executeUpdate` 의 반환값(영향받은 행 수)은 버려지며, `getMembers` 는 두 컬럼만 채운 `User` 를 돌려준다. 연결을 어디서 얻어 오는지(`DriverManager`)와 `setAutoCommit` 은 이 노트에 나오지 않는다 — **그 앞 단계는 하루 뒤 [[2024-08-14-Day56]] 가 소제목으로 세운다**
- [[2024-08-14-Day56]] — Day55 다음 날. **드라이버를 들이고 등록하고 연결하는 세 걸음의 목차**인데 본문이 채워진 것은 첫 걸음뿐이다. 「JDBC 드라이버 준비」가 벤더 넷의 `dependencies` 좌표(`ojdbc11-production`·`mssql-jdbc:12.8.0.jre11`·`mysql-connector-j:8.4.0`·`mariadb-java-client:3.4.1`)와 IntelliJ·Eclipse 두 갈래의 IDE 반영까지 적어 **드라이버가 「설치」가 아니라 좌표 한 줄이라는 것**을 실물로 보여 준다. 반면 「JDBC 드라이버 등록」의 다섯 소제목(`DriverManager.registerDriver`·`new jdbc.Driver경로`·`Class.forName("jdbc.Driver경로")`·`propreties`·`service-provider loading`)과 「DBMS에 연결하기」의 두 줄(`DBMS 연결구조`·`DBMS close`)은 **이름만 있고 본문이 비어 있어**, 다섯이 사실 같은 장치의 세 거리 + 실행 인자 + 자동이라는 것, 그중 ⑤ 만 남았다는 것, URL 서브프로토콜이 드라이버를 고른다는 것은 전부 이 노트가 채운다. 앞부분 「실습프로젝트」(properties 구현 · 로그인 기능 · 게시글에 사용자 정보 추가)도 소제목만 남아 있고, 그중 「properties 구현」은 등록 쪽 `propreties` 와 **이름만 같고 다른 것**이다. 파일 이름을 또 「gradle.build」로, 태스크를 「esclipse」로 적었다 → [[gradle]]
- [[2024-08-16-Day57]] — 이틀 뒤. **「1. JDBC 기본 사용법」이라는 제목으로 이 API 의 표면을 처음부터 끝까지 훑은 회차**다. `createStatement` → `executeUpdate`(변경된 행 수) / `executeQuery`(`ResultSet`) 의 갈림을 반환값과 함께 세우고, `insert`·`update`·`delete`·`select` 네 형태를 각각 코드 두 줄로 적은 뒤, 외래키가 걸린 자식을 먼저 지우는 순서까지 붙였다. 이어서 [[result-set]](커서·`getXXX`·컬럼 번호) → [[sql-injection]](「Statment의 문제점」) → [[prepared-statement]] → [[generated-keys]] → [[transaction]] 으로 **문제와 답을 붙여 놓은 순서**가 이 회차의 값이고, 실습 §2.1 이 Day55 의 DAO 다섯 메서드를 `Statement` 판과 `PreparedStatement` 판으로 나란히 보여 준다. 여기서 `executeUpdate` 의 반환값이 처음으로 `count > 0` 으로 쓰인다. 다만 `exceuteUpdate`·`executQuery` 같은 철자 오기가 코드 전반에 있고, 실제로 없는 메서드(`rs.get(컬럼명)`·`stmt.set(?,values)`)가 DAO 코드에 남았으며, 문장을 메서드마다 새로 준비해 재사용 이득은 아직 얻지 않는다. 연결을 얻는 코드(`DriverManager.getConnection`)는 §1.5.3 의 트랜잭션 예제에만 나오고 그 예제는 `con` 을 `try` 안에서 선언해 `catch`·`finally` 에서 쓸 수 없는 상태다 → [[transaction]]
- [[2024-08-19-Day58]] — 사흘 뒤. **이 API 를 쓰는 회차에서 감싸는 회차로 방향이 바뀐 자리**다. 「Sql 세션 만들기」 아래 `insert(String sql, Object... values)` 한 메서드가 준비·바인딩·실행·닫기 네 단계를 품고, `update`·`delete` 가 `return insert(sql, values)` 로 위임한다 — **셋을 가르는 호출이 이 API 에 없다는 사실**이 코드 모양으로 드러난 것이다. 다만 필기는 소제목 여섯 개 중 둘(「mybatis 구조 살펴보기」·「selectList 만들기」)을 빈 채로 남겼고, 「insert문 만들기」 블록에 `update`·`delete` 가 이미 들어 있어 뒤의 두 절이 같은 코드를 다시 싣는다. 조회를 감싸는 일이 왜 등록보다 어려운지, 감싸도 남는 것(SQL 문자열·커밋 경계·자동 생성 키)이 무엇인지는 [[sql-session]] 이 갖는다
