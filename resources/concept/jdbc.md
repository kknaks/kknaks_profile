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

## 왜 중요한가

**저장할 곳이 파일에서 DB 로 옮겨간다.** Day30 무렵부터 실습은 데이터를 `.data`·`.csv`·엑셀로 직접 읽고 썼다. 그 코드가 하던 일 — 형식 정하기, 다 읽어 메모리에 올리기, 바뀔 때마다 전체 다시 쓰기 — 을 JDBC 를 타고 서버에 맡기면 **조건 조회와 부분 수정이 문장 한 줄**이 된다. 파일 저장이 감당하지 못했던 것이 여기서 처음 해결된다 → [[io-stream]] · [[csv]] · [[apache-poi]] · [[dml]] · [[dql]]

**자바 코드가 어느 DB 인지 모르는 상태로 쓰인다.** 컴파일 시점에 내 코드가 아는 것은 `java.sql` 인터페이스뿐이고, 실물 구현은 실행할 때 클래스패스에서 온다. 그래서 **DB 를 바꾸는 일이 「jar 를 바꾸고 접속 URL 을 바꾸는 일」**로 줄어들고, 반대로 **jar 를 빠뜨리면 컴파일은 되는데 실행에서만 터진다** — 오류를 만나는 시점이 컴파일에서 런타임으로 옮겨간 것이다 → [[classpath]] · [[gradle]] · [[build]] · [[exception-handling]]

**그리고 Day51~52 에서 손으로 치던 것이 전부 메서드가 된다.** 접속(`'study'@'%'` 로 로그인하던 것)은 `DriverManager.getConnection`, `set autocommit = false` 는 `connection.setAutoCommit(false)`, `commit`/`rollback` 은 같은 이름의 메서드다. **SQL 을 배운 것이 API 를 배우는 일로 이어진다** → [[database-user]] · [[transaction]]

## 경계와 오해

- **「JRE에 기본적으로 포함된 드라이버」는 2024년에 이미 틀린 문장이다** — Type1 브리지(`sun.jdbc.odbc.JdbcOdbcDriver`)는 **JDK 8 에서 제거됐다.** 지금 쓸 수 있는 어떤 JDK 에도 없으므로, 필기대로 Type1 을 시험하면 접속 실패가 아니라 **클래스를 못 찾는 오류**(`ClassNotFoundException`)가 난다. 필기가 「기본 포함」이라 적은 것은 **Type1 의 정의가 아니라 그 시절의 배포 상태**였고, 그 상태가 이미 끝났다. 오늘 자바에서 DB 에 붙는다는 것은 사실상 전부 Type4 다 → [[jdk]]
- **JDBC ≠ ODBC 위에 얹힌 층** — 「ODBC 의 기능을 JVM에서 동일하게 구현」은 **Type1 에만 맞는 설명**이다. 실제로 쓰는 Type4 드라이버는 ODBC 를 거치지 않고 DB 의 통신 규약을 직접 구현한다. 즉 JDBC 는 ODBC 를 감싼 것이 아니라 **같은 문제에 대한 자바의 별도 규격**이고, 두 이름이 닮은 것은 설계를 참고했기 때문이다. 「JDBC 를 쓰려면 ODBC 드라이버를 깔아야 한다」로 읽으면 필요 없는 설치를 찾아 헤맨다.
- **JDBC 는 규격이고 드라이버는 구현이다 — 그런데 필기는 JDBC 를 「드라이버」라 부른다** — 「JVM에서 동일하게 구현한 드라이버」라는 한 줄에 규격과 구현이 겹쳐 있다. 갈라 보면 `java.sql` 인터페이스는 **JDK 에 들어 있고**(그래서 `import java.sql.Connection` 이 항상 된다), 그것을 구현한 드라이버 jar 는 **내가 따로 넣는다.** 「import 가 되는데 실행이 안 되는」 상황이 정확히 이 둘의 간격이다 → [[classpath]]
- **드라이버 「설치」와 「의존성 추가」는 다르다** — ODBC 드라이버는 **OS 에** 설치하고 등록해서 기계를 옮길 때마다 다시 해야 하지만, Type4 JDBC 드라이버는 **빌드 결과물 안에 들어가는 jar 한 개**다. 그래서 「내 컴퓨터에서는 됐는데」가 드라이버 때문에 생기는 일이 거의 없다 — 배포에 함께 실려 가기 때문이다 → [[gradle]] · [[build]] · [[platform-dependency]]
- **JDBC 가 통일하는 것은 접속과 호출이지 SQL 이 아니다** — [[odbc]] 와 같은 한계를 그대로 물려받는다. `Statement` 에 넣는 문자열은 여전히 그 DB 의 방언이고, MySQL 에 붙던 코드가 Oracle 에서 `limit` 하나로 깨진다. 이 층이 흡수하지 않는 것을 나중에 흡수하겠다고 나오는 것이 JPA·ORM 이다 → [[sql-data-type]] · [[sql-date-function]]
- **연결은 객체가 아니라 자원이다** — `Connection` 은 값을 담은 객체처럼 보이지만 실체는 **DB 서버와 열린 소켓 하나**이고, [[garbage-collection]] 이 대신 닫아 주지 않는다. 닫지 않은 연결이 쌓이면 서버 쪽 접속 수 상한에 먼저 부딪혀 **새 접속이 거절된다.** 파일 스트림을 닫아야 했던 것과 같은 규율이 그대로 오고, 그래서 JDBC 코드는 `try-with-resources` 로 쓰인다 → [[try-with-resources]] · [[socket]]
- **접속을 「빠른 것」으로 생각하면 안 된다** — 매 요청마다 `getConnection` 을 부르는 코드는 요청마다 TCP 연결과 인증을 새로 한다. 이것이 뒤에 커넥션 풀이 필요해지는 이유이고, 이 레포에 이미 [[connection-pool-sizing-formula]]·[[connection-lifetime-mismatch]] 로 남아 있는 문제들이 **여기서 만든 연결 하나**를 다루는 이야기다 → [[tcp]]

## 함께 보는 개념

- [[odbc]] — 이름과 설계를 물려준 앞선 표준. Day53 의 바로 앞 절
- [[jvm]] · [[jdk]] — 규격이 어디에 들어 있고 무엇이 OS 차이를 흡수하는가
- [[interface]] · [[polymorphism]] — 규격만 붙잡고 구현을 런타임에 받는 문법
- [[classpath]] · [[gradle]] · [[build]] — 드라이버 jar 가 실행 시점에 발견되게 하는 자리
- [[socket]] · [[network-protocol]] · [[port-number]] · [[tcp]] — Type4 드라이버 안에 들어 있는 것
- [[transaction]] — `setAutoCommit(false)` 로 옮겨 오는 Day52 의 실험
- [[dml]] · [[dql]] · [[ddl]] — 드라이버를 타고 서버로 보내는 문장들
- [[try-with-resources]] — 연결·문장·결과를 닫는 규율
- [[connection-pool-sizing-formula]] · [[connection-lifetime-mismatch]] — 이 연결을 재사용할 때 생기는 문제
- [[io-stream]] · [[csv]] · [[apache-poi]] — DB 로 넘어가기 전에 저장을 맡고 있던 것들
- [[client-server-model]] — 프로그램이 DB 서버의 클라이언트가 된다는 사실
- [[crud]] — 등록·조회·변경·삭제 화면이 이제 SQL 로 내려가는 자리

## 출처

- [[2024-08-09-Day53]] — JDBC 를 「ODBC 의 기능을 JVM에서 동일하게 구현한 드라이버」로 정의하고, 드라이버 타입 중 **Type1(ODBC-JDBC Bridge)** 만 「JRE에 기본적으로 포함된 드라이버」·「ODBC API를 호출(C함수)」 두 줄로 적은 뒤 끊긴다. 그래서 Type2~4 와 「지금 쓰는 것은 Type4」라는 결론은 이 노트가 채운다. 「JRE 에 기본 포함」은 JDK 8 에서 제거되어 이미 성립하지 않고, Day52 의 `commit`/`rollback` 이 어떻게 메서드로 오는지도 필기에는 없다
