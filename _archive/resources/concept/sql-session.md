---
type: concept
id: sql-session
title: SqlSession — SQL 실행을 감싼 객체
aliases:
  - SqlSession
  - sqlSession
  - SQL 세션
  - SqlSessionFactory
  - selectList
up:
  - 2024-08-19-Day58
  - 2024-08-20-Day59
  - 2024-08-23-Day62
tags:
  - java
  - database
  - JDBC
  - MyBatis
  - 설계
---

# SqlSession — SQL 실행을 감싼 객체

**연결 하나를 품고 「SQL 문자열 + 값들」을 받아 실행해 주는 객체.** 부르는 쪽은 `PreparedStatement` 를 만들지도 닫지도 않고 `?` 에 값을 채우지도 않는다 — `session.insert(sql, a, b, c)` 한 줄이 그 셋을 대신한다. Day58 이 「Sql 세션 만들기」라는 제목으로 이것을 손으로 만들고, 이름과 메서드 구성을 MyBatis 의 `SqlSession` 에서 그대로 가져왔다 → [[jdbc]] · [[prepared-statement]]

## 정의

메서드 하나가 이 개념의 전부다. **JDBC 코드에서 매번 반복되던 네 단계**(문장 준비 → 값 바인딩 → 실행 → 닫기)가 한 몸에 들어 있다.

```java
public int insert(String sql, Object... values) throws Exception {
  try (PreparedStatement stmt = con.prepareStatement(sql)) {   // ① 준비 + ④ 닫기
    int inparameterIndex = 1;
    for (Object value : values) {
      stmt.setString(inparameterIndex++, value.toString());     // ② 바인딩
    }
    return stmt.executeUpdate();                                // ③ 실행
  }
}
```

| 조각 | 하는 일 | 딸린 개념 |
|---|---|---|
| `con` | 필드로 들고 있는 연결. 메서드마다 받지 않는다 | [[jdbc]] |
| `String sql` | 실행할 문장. **뼈대만 오고 값은 따로 온다** | [[prepared-statement]] |
| `Object... values` | 개수를 부르는 쪽이 정하는 값 목록 | [[varargs]] |
| `inparameterIndex = 1` | `?` 의 번호. Day57 이 배운 「in-parameter」 이름이 그대로 변수명이 됐다 | [[one-based-numbering]] |
| `try (...)` | 문장을 그 호출 안에서 닫는다 | [[try-with-resources]] |
| `return` 값 | `executeUpdate()` 의 **변경된 행 수** | [[dml]] |

### 세 메서드가 한 메서드를 부른다

```java
public int update(String sql, Object... values) throws Exception { return insert(sql, values); }
public int delete(String sql, Object... values) throws Exception { return insert(sql, values); }
```

**본문이 없는 것이 실수가 아니다.** JDBC 에는 `insert`·`update`·`delete` 를 가르는 메서드가 없고 셋 다 `executeUpdate()` 하나로 간다 — 그래서 세 이름이 갈리는 것은 **동작이 아니라 부르는 쪽의 의도**뿐이다. MyBatis 의 `SqlSession` 도 정확히 같은 모양이며(`insert`·`delete` 가 내부적으로 `update` 를 부른다), 다만 **기준 메서드를 `update` 로 잡았다** — 그 차이가 아래 「경계와 오해」의 첫 항목이다 → [[dml]] · [[method]]

`insert(sql, values)` 로 넘길 때 `values` 는 이미 `Object[]` 인데, 가변 인수 자리에 배열을 넘기면 **그 배열이 그대로 전달**되고 원소 하나로 감싸이지 않는다. Day17 의 `inputInt` 가 `input(format, args)` 로 하던 것과 같은 문법이다 → [[varargs]]

### 소제목만 남은 두 자리

Day58 은 「mybatis 구조 살펴보기」와 「selectList 만들기」를 제목만 두고 채우지 않았다. **아래가 그 자리에 들어갈 답이고, 하루 뒤 Day59 가 그 답을 필기 자체로 확인한다**(각 표의 마지막 칸) → [[mybatis]]

#### ① MyBatis 의 구조 — 이 클래스가 놓이는 칸

Day58 이 손으로 만든 것은 MyBatis 네 층 중 **가운데 하나**다.

| 층 | 역할 | Day58 의 대응 | 하루 뒤 Day59 에 나온 것 |
|---|---|---|---|
| `mybatis-config.xml` | 접속 정보·타입 별칭·환경 설정 | 없다 (연결을 밖에서 받는다) | **전문이 실린다** — `<dataSource type="POOLED">` 까지 |
| `SqlSessionFactoryBuilder` → `SqlSessionFactory` | 설정을 읽어 세션을 찍어 내는 공장. 앱에 하나 | 없다 | **사다리 세 줄** (아래) |
| **`SqlSession`** | **문장 하나를 실행하고 커밋 경계를 갖는다** | **이 클래스** | `openSession(false)` 로 얻는다 |
| Mapper (XML · 인터페이스) | **SQL 을 자바 밖에 두고 id 로 부른다** | 없다 (SQL 을 인수로 받는다) | **`<select>`·`<insert>`… 조각 다섯** |

**갈리는 지점 하나가 결정적이다.** MyBatis 의 `session.insert("board.add", param)` 이 받는 첫 인수는 SQL 이 아니라 **문장의 id** 이고, SQL 본문은 매퍼에 있다. Day58 의 세션은 SQL 문자열을 그대로 받으므로 **문장은 여전히 자바 코드 안에 있다** — 즉 Day58 이 걷어낸 것은 `PreparedStatement` 를 다루는 절차이고, SQL 을 자바에서 떼어 내는 일은 아직 남아 있다. **하루 뒤 Day59 의 `sqlSession.delete("UserDao.delete", no)` + 매퍼 XML 이 정확히 그 남은 일을 한다** → [[mybatis]] · [[encapsulation]] · [[coupling]]

그리고 **Day58 이 「없다」로 비워 둔 공장 칸이 Day59 에서 세 줄로 채워진다.**

```java
InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(inputStream);
SqlSession sqlSession = sqlSessionFactory.openSession(false);
```

**사다리가 세 칸인 것이 아래 「연결을 누가 만들고 누가 닫는지가 정해지지 않았다」에 대한 답이다** — Builder 는 XML 을 한 번 읽고 버려지고, Factory 는 앱에 하나로 남고, Session 은 작업 하나만큼 산다. Day58 의 세션은 `con` 을 필드로 받았을 뿐 그 수명을 아무도 정하지 않았는데, MyBatis 는 **수명이 다른 셋으로 나눠** 각 칸의 책임을 정한다. 상세는 [[mybatis]] 가 갖는다.

#### ② selectList — 나머지 셋과 격이 다르다

`insert`·`update`·`delete` 가 세 줄로 끝난 뒤 `selectList` 의 코드 블록이 **비어 있는 것**은 우연이 아니다. 조회는 돌려줄 것이 `int` 가 아니라 **행들**이고, 그러려면 세션이 **행을 무엇으로 만들지** 알아야 한다.

```java
// 세션이 타입을 모른 채 돌려줄 수 있는 최대치 — 컬럼 이름 → 값
public List<Map<String, Object>> selectList(String sql, Object... values) throws Exception {
  try (PreparedStatement stmt = con.prepareStatement(sql)) {
    int i = 1;
    for (Object value : values) stmt.setString(i++, value.toString());
    try (ResultSet rs = stmt.executeQuery()) {
      List<Map<String, Object>> rows = new ArrayList<>();
      ResultSetMetaData meta = rs.getMetaData();
      while (rs.next()) {
        Map<String, Object> row = new LinkedHashMap<>();
        for (int c = 1; c <= meta.getColumnCount(); c++) {
          row.put(meta.getColumnLabel(c), rs.getObject(c));
        }
        rows.add(row);
      }
      return rows;
    }
  }
}
```

`insert` 쪽에는 없던 것이 셋 늘어난다 — **커서를 다 읽어 담아야 하고**(문장이 닫히면 커서도 죽는다), **컬럼 이름을 런타임에 알아내야 하고**(`ResultSetMetaData`), **그릇을 골라야 한다.** 그래서 이 자리에서 갈림이 생긴다.

| 돌려주는 것 | 세션이 알아야 하는 것 | 대가 |
|---|---|---|
| `List<Map<String,Object>>` | 없다 | 부르는 쪽이 `row.get("title")` 로 캐스팅하며 쓴다 — 컬럼 이름 오타가 컴파일에서 안 잡힌다 |
| `List<T>` (타입을 인수로 받는다) | **어느 클래스로 만들지** | 리플렉션이 필요하다. MyBatis 의 `resultType` 이 이 인수다 |

**MyBatis 가 `resultType` 을 요구하는 이유가 이 빈 코드 블록 안에 있다.** `insert` 는 값을 보내기만 하므로 타입을 몰라도 되지만, `select` 는 받아서 무언가로 만들어야 하므로 **타입 정보를 반드시 밖에서 받아야 한다** → [[result-set]] · [[generics]] · [[hash-based-collection]] · [[dql]]

**하루 뒤 Day59 의 XML 문법이 이 비대칭을 그대로 보인다** — `<select id="sql1" resultType="bitcamp.myapp.vo.User">` 에는 결과 타입이 적혀 있고, `parameterType` 은 **적지 않아도 되는 값**이다(넘긴 객체에서 알 수 있다). 즉 이 빈 코드 블록에서 예측한 「받는 쪽만 타입이 필요하다」가 **문법의 필수/선택 갈림으로 확인된다** → [[mybatis]]

### 사흘 뒤 Day62 — 이 객체가 몇 개여야 하는지가 문제로 나온다

Day58~59 는 세션을 **하나 얻어 쓰는** 코드였고 개수를 물을 일이 없었다. Day61 이 서버를 접속마다 쓰레드로 갈라 놓자 그 질문이 터진다 — Day62 의 첫 절이 그 답을 세 줄로 적었다.

| Day62 가 적은 문제 | 무엇이 세션에 딸려 있어서 생기나 |
|---|---|
| 「하나의 SqlSession을 생성하여 하나의 캐시를 공유한다」 | **1차 캐시**가 세션 범위다 → [[caching]] |
| 「하나의 클라이언트에서 커밋을 하면 전체 캐시가 데이터베이스에 업데이트된다」 | **커밋 경계**가 세션 범위다 → [[transaction]] |
| 「다른 클라이언트에서 오류가 발생해도 롤백되지 않는다」 | 위와 같은 이유 — 되돌릴 범위도 세션이다 |

**세 줄이 전부 「이 객체가 무언가의 범위다」의 결과**이고, 그래서 개수가 성능 문제가 아니라 **정합성 문제**가 된다. 답은 개수를 늘리는 것이고 Day62 가 고른 단위는 **쓰레드**다 → [[thread]] · [[thread-local]]

| 회차 | 세션이 몇 개 | 무엇이 문제인가 |
|---|---|---|
| Day59 | 코드에 하나 (예제) | 개수를 물을 일이 없다 |
| Day61 | **앱에 하나** — `appCtx` 의 DAO 프록시가 필드로 들고 있다 | 접속 수십 개가 캐시와 커밋 경계를 공유한다 |
| Day62 | **쓰레드마다 하나** | 접속끼리는 갈렸다. 다만 「작업마다」는 아니다(아래) |

**MyBatis 의 수명 표(「세션은 작업마다 하나 — 커밋 경계와 같다」)에 한 칸 못 미친다.** 세션을 닫는 코드가 없으므로 한 쓰레드의 세션이 **로그인부터 접속이 끝날 때까지** 살아 있고, 그 사이 화면 열 개를 지나도 같은 세션이다 → [[mybatis]]

## 사용 예시

Day58 이 실제로 적은 것은 `insert` 하나와 그것에 위임하는 둘이다(위 「정의」). **이 세션이 놓이면 Day57 의 DAO 한 메서드가 이렇게 줄어든다.**

```java
// Day57 §2.1 — DAO 가 JDBC 를 직접 다룬다
boolean delete(int no) throws Exception {
  try (PreparedStatement stmt = con.prepareStatement("delete from myapp_projects where project_id=?")) {
    stmt.setInt(1, no);
    int count = stmt.executeUpdate();
    return count > 0;
  }
}

// Day58 의 세션을 쓰면 — 남는 것은 SQL 과 값뿐이다
boolean delete(int no) throws Exception {
  return session.delete("delete from myapp_projects where project_id=?", no) > 0;
}
```

**`Statement`·`PreparedStatement`·`ResultSet` 이라는 낱말이 DAO 에서 사라진다.** 다섯 메서드가 같은 네 단계를 각각 반복하던 것이 한 곳으로 모이고, 그래서 「문장을 닫는 것을 잊었다」·「`setInt` 를 빼먹었다」가 다섯 자리가 아니라 한 자리의 문제가 된다 → [[refactoring]] · [[cohesion]]

다만 **줄어든 것은 `delete` 처럼 값만 보내는 메서드**이고, `insert` 는 자동 생성 키를 되받아야 해서 이 세션으로 옮겨지지 않는다(아래) → [[generated-keys]]

## 왜 중요한가

**JDBC 를 아는 코드가 한 클래스로 줄어든다.** Day55~57 의 DAO 는 메서드 다섯 개가 각각 연결을 알고 문장을 만들고 닫았다. 그 낱말이 한 곳에만 남으면 **드라이버 API 가 바뀌거나 커넥션 풀을 끼울 때 고칠 자리가 한 곳**이 된다. 「같은 코드를 다섯 번 쓰지 않는다」보다 **「이 API 를 아는 코드가 몇 곳인가」** 가 이 층이 실제로 바꾸는 값이다 → [[coupling]] · [[encapsulation]]

**그리고 프레임워크가 하는 일이 무엇인지 알게 된다.** MyBatis·JdbcTemplate 을 먼저 배우면 「설정을 이렇게 하면 된다」로 남지만, 같은 것을 손으로 만들어 보면 그 API 의 생김새가 전부 이유를 갖는다 — `insert`/`update`/`delete` 가 왜 셋인데 하는 일은 같은지, `selectList` 가 왜 `resultType` 을 요구하는지, `SqlSession` 이 왜 `commit()` 을 갖는지. **Day58 은 라이브러리를 쓴 회차가 아니라 라이브러리의 첫 칸을 재현한 회차다** → [[template-method-pattern]]

**대신 무엇이 감춰지지 않았는지도 드러난다.** SQL 문자열은 여전히 DAO 에 있고, 커밋 경계는 여전히 `Connection` 에 있고, 자동 생성 키는 이 통로로 나올 수 없다. **감싸는 층을 만들면 「감싸지 못한 것」이 목록으로 남는다** — 그 목록이 다음에 무엇을 배워야 하는지를 가리킨다 → [[transaction]] · [[generated-keys]]

## 경계와 오해

- **기준 메서드가 `insert` 인 것은 거꾸로다** — 셋 중 하나에 본문을 두고 둘이 위임하는 형태는 옳은데, **본문을 가진 것이 `insert`** 라서 셋 중 가장 특별한 것이 기준이 됐다. `insert` 만 자동 생성 키를 되받아야 하고(`RETURN_GENERATED_KEYS`), 그 요청은 `con.prepareStatement(sql, flag)` 에 들어가므로 **머지않아 `insert` 의 본문이 달라진다.** 그때 `update`·`delete` 는 키를 요청하는 문장으로 실행되게 되거나 위임을 끊어야 한다. MyBatis 가 `update` 를 기준으로 잡은 이유가 이것이다 — **변하지 않을 쪽을 기준으로 둔다** → [[generated-keys]] · [[method]]
- **세 이름은 검사를 하지 않는다 — `session.delete("insert into ...")` 가 통한다** — 셋이 같은 본문이므로 어느 이름으로 무슨 문장을 보내도 실행된다. 메서드 이름은 **읽는 사람에게 하는 말**이고 컴파일러나 드라이버는 그것을 보지 않는다. 그래서 이름을 셋으로 나눈 값은 「막아 준다」가 아니라 **「호출부를 읽으면 무슨 문장인지 안다」** 뿐이다. 하나로 합쳐 `execute(sql, values)` 하나만 두는 설계도 성립하고, 그때 잃는 것이 정확히 그 가독성이다.
- **값을 전부 `setString` 으로 보낸다 — 그 대가는 [[prepared-statement]] 쪽에 있다** — `Object...` 로 받은 순간 세션이 아는 타입은 `Object` 뿐이라 `setInt`·`setDate` 를 고를 근거가 없고, 그래서 `value.toString()` + `setString` 이 유일한 길이 된다. **가변 인수가 개수를 자유롭게 해 준 대가로 타입을 잃은 것**이고, 이것이 이 설계의 가장 큰 구멍이다(`null` 이 오면 그 자리에서 죽고, 날짜는 어떤 `Date` 인지에 따라 통하거나 깨진다). 진짜 답은 `setObject(i, value)` 로 드라이버에게 타입 판단을 넘기는 것이다 → [[varargs]] · [[prepared-statement]] · [[sql-null]] · [[date-time]]
- **`?` 개수와 값 개수를 아무도 맞춰 주지 않는다** — 값이 많으면 `setString` 이 `Parameter index out of range` 로, 적으면 `executeUpdate()` 가 `No value specified for parameter N` 으로 실패한다. **세션을 만들면서 없어진 것 중 하나가 「몇 번째 `?` 에 무엇을 넣는가」를 눈으로 확인할 수 있던 것**이고, 이제 SQL 의 `?` 개수와 호출부의 인수 개수를 사람이 세어 맞춘다. 오류는 컴파일이 아니라 실행에서만 온다 → [[varargs]] · [[exception-handling]]
- **문장 재사용 이득은 여기서도 나지 않는다** — `try-with-resources` 가 호출마다 문장을 준비하고 닫으므로, 같은 SQL 을 팀원 열 명에게 반복해도 준비가 열 번이다. Day57 의 DAO 와 같은 상태이며 **세션이 그것을 고친 것이 아니다.** 문장 캐시는 세션이 SQL 문자열을 키로 `PreparedStatement` 를 들고 있어야 나는 이득이고(MyBatis 의 `cachePrepStmts` 계열이 그 자리), 그러려면 「호출이 끝나면 닫는다」는 이 코드의 규율을 포기해야 한다 — **자원 안전과 재사용이 부딪히는 자리** → [[try-with-resources]] · [[caching]]
- **자동 생성 키는 이 통로로 나올 수 없다** — 반환형이 `int`(변경된 행 수)이고 문장이 메서드 안에서 닫히므로, 부르는 쪽에서 `getGeneratedKeys()` 를 부를 대상이 남지 않는다. Day57 §2.2 의 등록 화면은 `insert` 뒤에 받은 번호로 팀원을 넣었으므로, **그 화면을 이 세션으로 옮기면 `project.getNo()` 가 `0` 인 채로 다음 문장에 들어간다** → [[generated-keys]]
- **SqlSession ≠ 커넥션, ≠ DB 세션** — 이름의 「세션」이 [[transaction]] 노트가 말하는 「접속 하나」와 겹쳐 읽히는데 층이 다르다. DB 세션은 서버가 관리하는 접속이고 `autocommit` 같은 설정이 거기에 딸린다. `SqlSession` 은 **그 접속을 쓰는 자바 쪽 객체**이며, 하나의 연결 위에 세션 객체를 여러 개 만들 수도 있다. 웹의 HTTP 세션(사용자 로그인 상태)과는 이름만 같고 아무 관계가 없다 → [[jdbc]]
- **「하나의 연결 위에 세션 여러 개」는 이 프레임워크에서는 성립하지 않는다 — 그래서 Day62 의 세션 수가 곧 연결 수다** — 위 항목이 개념 층에서 적은 말인데, MyBatis 의 세션은 **첫 문장을 실행할 때 풀에서 연결 하나를 빌려 자기 것으로 붙들고 `close()` 까지 놓지 않는다**(커밋으로도 안 놓는다). 그래서 「쓰레드마다 하나」는 곧 **「접속마다 연결 하나」**이고, `<dataSource type="POOLED">` 의 기본 활성 상한이 10개이므로 **열한 번째 접속부터 풀에서 기다린다.** [[thread]] 노트가 「접속 100명이면 쓰레드 100개」라고 적은 자리에서 이번에는 **연결 100개가 필요해지는 것**이고, 쓰레드 수의 상한이 없는 것과 연결 수의 상한이 있는 것이 여기서 부딪힌다 — 세션의 단위를 「접속」이 아니라 「작업」으로 잡아야 하는 실무적 이유가 이것이다 → [[connection-pool-sizing-formula]] · [[universal-scalability-law]]
- **Day59 의 「`commit()` 이 없다」가 Day62 에서는 「`close()` 가 없다」로 옮겨간다** — 세 회차가 같은 짝의 다른 쪽을 빼먹는다. Day59 는 경계를 열고 커밋하지 않아 **아무것도 저장되지 않았고**, Day62 는 커밋·롤백을 제자리에 넣었지만 **세션을 닫지 않는다.** 닫지 않으면 ① 연결이 풀로 돌아가지 않고(위 항목), ② 마지막 작업 뒤의 미확정 변경이 되돌려지는 시점이 사라지고, ③ [[thread-local]] 의 값도 남는다. **`openSession` 을 부르는 자리를 열다섯 곳으로 흩어 놓으면 닫을 자리가 어디인지 아무도 답할 수 없게 된다**는 것이 이 구조의 대가다 — 「얻는 곳」을 프록시로 한 곳에 모았는데 「놓는 곳」은 모으지 않았다 → [[try-with-resources]] · [[proxy-pattern]]
- **세션이 「작업」이 아니라 「접속」 단위가 되면 대화 내내 같은 과거를 본다** — Day62 의 세션은 로그인부터 종료까지 하나이므로 **1차 캐시와 트랜잭션 스냅샷이 그 대화 전체에 걸린다.** 목록을 조회한 뒤 다른 클라이언트가 글을 등록해도, 같은 문장을 다시 부르면 캐시가 답하고([[caching]]) 캐시가 비워진 뒤라도 열려 있는 트랜잭션의 스냅샷이 답한다([[transaction]] 의 REPEATABLE READ 항목). **읽기만 하는 사용자는 화면을 새로 그려도 데이터가 갱신되지 않는 것**이고, 원인이 두 층에 하나씩 있어서 한쪽을 껐다고 사라지지 않는다. Day61 의 공유 세션이 「남의 변경이 섞이는」 문제였다면 이쪽은 **「남의 변경이 안 보이는」 문제**이며, 둘 사이의 자리가 「작업마다 하나」다 → [[mybatis]] · [[dql]]
- **커밋 경계는 Day58 의 이 객체에 없고, 하루 뒤 MyBatis 에는 있는데 필기가 그것을 쓰지 않는다** — Day58 의 세션에는 `commit()`·`rollback()` 이 없어서 Day57 §2.2 가 하던 `con.setAutoCommit(false)` → `con.commit()` 는 여전히 화면 코드가 `Connection` 을 직접 들고 해야 한다. 즉 **DAO 에서는 JDBC 가 사라졌지만 Command 에는 남아 있다.** MyBatis 의 `SqlSession` 이 `commit`·`rollback`·`close` 를 갖는 것은 장식이 아니라 이 구멍을 메우는 것이고, 문장 실행과 커밋 경계가 **같은 객체에 있어야 「이 세션의 작업 묶음」이 성립**하기 때문이다. **그런데 Day59 는 `openSession(false)` 로 경계를 열어 놓고 `commit()` 을 한 번도 부르지 않는다** — 그래서 그 회차의 `insert`·`update`·`delete` 예제는 세션이 닫힐 때 롤백되어 **DB 에 아무것도 남지 않으면서 반환값은 1 이다.** Day58 기준으로는 「구멍이 있다」였고 Day59 기준으로는 「도구가 왔는데 반쪽만 썼다」다 → [[transaction]] · [[mybatis]]
- **`openSession(false)` 의 인수는 autocommit 이고, 그 기본값이 JDBC 와 반대다** — Day57 이 `con.setAutoCommit(false)` 로 명시해야 했던 것을 MyBatis 는 **세션을 얻는 자리의 인수 하나**로 받는다. 그리고 인수를 생략한 `openSession()` 도 `false` 다 — [[transaction]] 노트가 시작하는 「mysql은 autocommit의 기본 값이 true이다」가 이 층에서 뒤집히므로, **「기본값이니 자동 커밋이겠지」로 읽으면 인수를 지운 코드에서도 위 항목의 사고가 그대로 난다.** 커밋 경계를 갖는 객체가 생긴 대가로 **경계를 닫는 책임도 그 객체를 쓰는 쪽에 생긴 것**이다 → [[transaction]]
- **MyBatis 의 `SqlSession` 은 이 클래스와 이름만 같다 — 갈리는 것이 셋이다** — Day58 이 이름과 메서드 구성을 그대로 베껴 왔지만, ① 첫 인수가 SQL 이 아니라 **문장의 id** 이고, ② `commit`·`rollback`·`close` 를 갖고, ③ 연결을 밖에서 받지 않고 **풀에서 스스로 얻는다**. 그래서 「같은 것을 손으로 만들었다」는 정확히 **한 층의 절반**이고, 남은 절반이 하루 뒤 회차에 나온다 → [[mybatis]]
- **기준 메서드 문제는 Day59 로도 확인되지 않는다** — 아래 첫 항목이 「MyBatis 가 `update` 를 기준으로 잡았다」고 적었는데, Day59 의 필기는 다섯 메서드를 **부르는 쪽만** 보이고 그 안이 어떻게 위임되는지는 다루지 않는다. 즉 그 판단의 근거는 여전히 이 노트 밖(MyBatis 소스)에 있고, **필기만으로는 세 이름이 왜 셋인지 알 수 없는 상태가 두 회차 연속**이다 → [[mybatis]]
- **연결을 누가 만들고 누가 닫는지가 정해지지 않았다** — `con` 은 필드인데 이 코드에는 생성자도 `close()` 도 없다. 밖에서 만든 연결을 받는 형태라면(그것이 [[dependency-injection]] 의 가장 단순한 꼴이다) **닫는 책임도 밖에 있고**, 세션이 만든다면 세션이 `AutoCloseable` 이어야 한다. 둘 다 아닌 상태가 「연결이 안 닫혀 쌓이는」 문제가 시작되는 자리다 → [[jdbc]] · [[try-with-resources]]
- **감싼 것은 절차이고 SQL 은 아니다** — 필기의 제목이 「JDBC 캡슐화」·「sql구문 캡슐화」인데, 실제로 감춰진 것은 **`PreparedStatement` 를 다루는 절차**다. SQL 문자열은 호출부에 그대로 있고 오히려 **인수로 올라가 더 눈에 띈다.** 「SQL 을 감춘다」는 매퍼 파일이나 ORM 이 하는 다음 걸음이고, 두 가지를 한 낱말로 묶어 두면 이 회차가 무엇을 끝냈고 무엇을 남겼는지가 흐려진다 → [[encapsulation]]
- **인젝션 위험은 줄지 않고 옮겨간다 — 하루 뒤에 한 번 더 옮겨간다** — 세션이 `PreparedStatement` 를 쓰니 안전해 보이지만, **문자열 조립을 하는 자리는 호출부**로 옮겨졌을 뿐이다. `session.update("update x set title='" + t + "'")` 는 이 세션을 통해서도 그대로 실행된다. 값 자리를 `?` 로 두는 판단은 여전히 SQL 을 쓰는 사람이 하고, 세션은 **그것을 강제하지 못한다.** Day59 에서는 그 자리가 다시 **매퍼 XML** 로 옮겨가고, 거기서는 `#{}`(안전)와 `${}`(문자열 치환)가 **한 글자 차이**로 나란히 있다 — 감싸는 층을 하나 더 얹어도 「어느 표기를 썼나」는 끝까지 사람의 판단이다 → [[sql-injection]] · [[mybatis]]
- **연결을 필드로 들고 있는 것의 대가가 Day59 에서 설정으로 바뀐다** — 아래 「연결을 누가 만들고 누가 닫는지가 정해지지 않았다」의 답이 하루 뒤 `<dataSource type="POOLED">` 로 온다. 연결을 만들고 빌려 주고 되받고 상태를 되돌리는 일이 전부 그 한 줄 뒤로 들어가며, Day57 이 `finally` 에서 손으로 하던 `setAutoCommit(true)` 도 거기서 사라진다 — **정하지 못했던 책임이 코드가 아니라 설정 값으로 정해진 것**이다 → [[mybatis]] · [[connection-lifetime-mismatch]]
- **`throws Exception` 이 그대로 올라온다** — 세션이 예외를 다루지 않고 밀어 올리므로 DAO 도 `throws Exception` 이고 화면도 `catch (Exception e)` 다. 감싸는 층을 만들면서 **예외만은 감싸지 않은 상태**이고, 그래서 「SQL 오류인지 연결 오류인지 프로그램 버그인지」가 호출부에서 구별되지 않는다. Spring 의 `JdbcTemplate` 이 검사 예외를 런타임 예외로 바꿔 던지는 것이 이 자리에 대한 답이다 → [[exception-handling]]
- **행 수를 `boolean` 으로 접으면 정보가 사라진다** — `session.delete(...) > 0` 형태는 「지웠다/못 지웠다」만 남기므로, 조건에 맞는 행이 **여럿 지워진 경우**를 알 수 없다. `where` 를 빠뜨린 `update` 가 전체 행을 고쳐도 `true` 다. 반환값을 `int` 로 준 세션의 결정이 옳고, 그것을 접는 것은 호출부의 선택이다 → [[dml]]

## 함께 보는 개념

- [[jdbc]] — 이 객체가 감싸는 API 층
- [[prepared-statement]] — 세션 안에서 만들어지고 닫히는 문장 객체
- [[varargs]] — 값 목록을 받는 문법. 타입을 잃는 대가까지
- [[encapsulation]] — 「무엇을 감췄나」를 묻는 축
- [[generated-keys]] — 이 통로로 나오지 못하는 값
- [[transaction]] — 아직 이 객체에 없는 커밋 경계
- [[thread]] · [[thread-local]] — 이 객체가 몇 개여야 하는지를 정하는 축
- [[proxy-pattern]] — 세션을 얻는 자리를 한 곳으로 모은 구조
- [[caching]] — 세션에 딸려 있는 1차 캐시
- [[result-set]] · [[dql]] — `selectList` 가 어려운 이유
- [[dml]] — 세 메서드가 하나로 합쳐지는 근거
- [[try-with-resources]] — 자원 안전과 문장 재사용이 부딪히는 자리
- [[coupling]] · [[cohesion]] — JDBC 를 아는 곳을 줄인다는 것의 이름
- [[refactoring]] — 다섯 메서드의 반복을 한 곳으로 모으는 일
- [[generics]] · [[hash-based-collection]] — 조회 결과를 무엇에 담을지의 갈림
- [[dependency-injection]] — 연결을 밖에서 받는 형태
- [[template-method-pattern]] — 변하는 곳만 인수로 받고 절차를 고정하는 같은 꼴
- [[sql-injection]] — 세션이 강제해 주지 않는 것
- [[exception-handling]] — `throws Exception` 이 그대로 올라오는 자리
- [[crud]] — 이 세션 위에 다시 세워지는 DAO 메서드들
- [[mybatis]] — 이 클래스가 흉내낸 원본. 빈 두 소제목의 답이 실제로 나오는 자리
- [[persistence-framework]] — 이 층이 속하는 갈래(SQL Mapper)
- [[dao-pattern]] — 이 세션을 부르는 위쪽 층
- [[xml]] — SQL 이 옮겨 가는 곳

## 출처

- [[2024-08-19-Day58]] — 「Sql 세션 만들기」라는 제목 아래 `insert(String sql, Object... values)` 한 메서드로 이 개념이 등장한다. `con.prepareStatement(sql)` → `for` 로 `?` 를 1번부터 채우기 → `executeUpdate()` 반환까지가 [[jdbc]] 네 단계를 한 몸에 넣은 형태이고, `update`·`delete` 가 `return insert(sql, values)` 한 줄로 위임하는 것이 **셋이 같은 `executeUpdate` 로 간다**는 사실을 코드로 드러낸다. 변수명 `inparameterIndex` 는 사흘 전 Day57 이 배운 「in-parameter」를 그대로 옮긴 것이다. 다만 값을 전부 `value.toString()` + `setString` 으로 보내 타입 정보를 버렸고, 문장이 메서드 안에서 닫혀 [[generated-keys]] 를 되받을 길이 없으며, `commit`/`rollback` 이 없어 커밋 경계는 여전히 `Connection` 쪽에 남는다. **「mybatis 구조 살펴보기」와 「selectList 만들기」는 소제목과 빈 코드 블록만 있어** MyBatis 네 층 중 이 클래스가 어느 칸인지, 조회가 왜 `resultType` 을 요구하는지는 이 노트가 채웠다. 「insert문 만들기」의 코드 블록에 `update`·`delete` 가 이미 들어 있고 뒤의 두 절이 같은 코드를 다시 싣는 붙여넣기 중복도 그대로 남아 있다
- [[2024-08-20-Day59]] — 하루 뒤. **Day58 이 흉내낸 원본이 실제로 나오고, 이 노트가 빈 소제목 자리에 채워 둔 답이 필기로 확인된다.** 「mybatis 구조 살펴보기」에 넣은 네 층 표의 「없다」 칸 셋이 각각 `mybatis-config.xml` 전문·`SqlSessionFactoryBuilder` → `SqlSessionFactory` → `openSession(false)` 사다리·매퍼 XML 조각 다섯으로 채워지고, 「selectList 만들기」에 적어 둔 「조회만 타입 정보를 밖에서 받아야 한다」는 예측이 **`resultType` 은 필수이고 `parameterType` 은 선택**이라는 XML 문법의 비대칭으로 나타난다. 첫 인수가 SQL 이 아니라 문장 id 라는 갈림도 `sqlSession.delete("UserDao.delete", no)` 로 그대로 보인다. 다만 **`openSession(false)` 로 커밋 경계를 열고 `commit()` 을 부르지 않아** 이 노트가 「구멍」이라 부른 자리가 「도구가 왔는데 반쪽만 쓴」 상태로 남고, 세 이름(`insert`·`update`·`delete`) 중 무엇이 기준 메서드인지는 부르는 쪽만 보여 두 회차 연속 확인되지 않는다 → [[mybatis]]
- [[2024-08-23-Day62]] — 사흘 뒤. **이 객체가 몇 개여야 하는지가 처음 문제로 나오는 회차**다. 「MultiTread의 문제점」 세 줄(캐시를 공유한다 · 한 클라이언트의 커밋이 전체를 확정한다 · 남의 오류에 롤백되지 않는다)이 전날 Day61 의 구조에서 실제로 걸린 것이고, 셋 다 **캐시와 커밋 경계가 이 객체의 범위**라는 한 사실에서 나온다. 답으로 `SqlSessionFactory` 에 프록시를 씌워 [[thread-local]] 로 **쓰레드마다 같은 세션**을 돌려주게 하고, `DaoFactory` 와 Command 구현체가 `SqlSession` 필드를 버리고 팩토리를 받아 `openSession(false)` 로 그때그때 얻는 형태로 바꾼다 — 「각자 고유의 캐시를 가지기 때문에 다른 클라이언트의 작업이 현재 클라이언트의 작업에 영향을 미치지 않는다」가 그 결과다. **다만 「작업마다 하나」에는 한 칸 못 미친다** — `close()` 가 어디에도 없어 세션이 로그인부터 접속 종료까지 살아 있고, 그래서 ① 빌린 연결이 풀로 돌아가지 않아 활성 상한(기본 10)에 닿고, ② 1차 캐시와 트랜잭션 스냅샷이 대화 전체에 걸려 **남의 변경이 보이지 않는** 반대쪽 문제가 생긴다. Day59 가 「경계를 열고 커밋하지 않은 회차」였다면 Day62 는 **「커밋은 넣고 닫지 않은 회차」**다. 세션이 쓰레드 안전하지 않다는 것도, 팩토리는 안전해서 공유해도 된다는 비대칭도 필기에는 없다 — 프록시를 팩토리에 씌운 판단이 그 비대칭에 기대고 있는데 이유가 적혀 있지 않다
