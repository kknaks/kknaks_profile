---
type: concept
id: prepared-statement
title: PreparedStatement (매개변수화 질의)
aliases:
  - PreparedStatement
  - prepareStatement
  - 매개변수화 질의
  - 파라미터 바인딩
  - 바인딩 변수
  - bind parameter
  - in-parameter
  - 플레이스홀더
  - setXXX
up:
  - 2024-08-16-Day57
  - 2024-08-19-Day58
  - 2024-08-20-Day59
tags:
  - java
  - database
  - JDBC
  - 보안
---

# PreparedStatement (매개변수화 질의)

**SQL 문장의 뼈대와 그 안에 들어갈 값을 따로 보내는 문장 객체.** 값이 갈 자리를 `?` 로 비워 두고 문장을 먼저 만든 뒤, `setXXX(위치, 값)` 으로 값을 채운다. Day57 이 이것을 **[[sql-injection]] 의 답으로** 도입한다 — 「보완성을 강화하기 위해 쿼리문에 전송할 값들을 매개변수화하는 방법이다」(원문 표기 「보완성」은 **보안성**의 오기다) → [[jdbc]]

## 정의

`Statement` 와 갈리는 것은 **SQL 이 언제 완성되는가** 하나이고, 나머지 차이는 전부 거기서 나온다.

| | `Statement` | `PreparedStatement` |
|---|---|---|
| 문장을 만드는 메서드 | `con.createStatement()` | `con.prepareStatement(sql)` — **SQL 을 여기서 넘긴다** |
| SQL 이 완성되는 시점 | 내가 문자열을 이어 붙일 때 | **값이 따로 가고 뼈대는 그대로** |
| 값이 문장의 일부인가 | **그렇다** — 그래서 값이 문법을 바꿀 수 있다 | 아니다 — 값은 값 자리로만 간다 |
| 실행 | `executeQuery(sql)` · `executeUpdate(sql)` | `executeQuery()` · `executeUpdate()` — **인수 없음** |
| 같은 문장 반복 | 매번 새 문자열 → 매번 파싱 | 뼈대 한 번 준비, 값만 바꿔 다시 실행 |
| 값의 따옴표·이스케이프 | 내가 챈다 | 드라이버가 한다 |
| 자동 생성 키 요청 자리 | `executeUpdate(sql, RETURN_GENERATED_KEYS)` | **`prepareStatement(sql, RETURN_GENERATED_KEYS)`** |

Day57 이 그 문법을 세 줄로 적었다 — 「statement를 선언할 때 매개변수 값들을 ?으로 표시한다」·「**in-parameter** : ? 값으로 들어갈 타입에 따라 set()으로 설정한다」.

```java
Connection con = DriverManager.getConnection(url, username, password);
PreparedStatement stmt = con.prepareStatement("select 컬럼명 from 테이블명 where 컬럼명= ? ");
stmt.setXXX(1,값);
ResultSet rs = stmt.executQuery(); //쿼리 전송 및 결과 리턴

PreparedStatement stmt = con.prepareStatement("update 테이블명 set 컬럼명=?, 컬럼명=?.. where 조건");
stmt.setXXX(1,값); //첫번째 ?
stmt.setXXX(2,값); //두번째 ?
int count = stmt.executUpdate(); //쿼리 전송 및 결과 리턴
```

**`?` 를 가리키는 것은 이름이 아니라 번호**이고, 그 번호는 **SQL 문자열에 `?` 가 나온 순서**다(1부터). 그래서 `set` 호출은 SQL 텍스트의 순서에 묶여 있고, `where` 절에 조건 하나를 앞에 끼워 넣으면 **뒤의 모든 번호가 밀린다** → [[one-based-numbering]] · [[parameter-and-argument]]

`in-parameter` 라는 이름은 **값이 들어가는 방향**을 말한다(자바 → DB). 반대 방향으로 값을 돌려받는 `out-parameter` 는 저장 프로시저를 부르는 `CallableStatement` 의 것이고, Day57 에는 나오지 않는다.

## 사용 예시

Day57 §2.1 이 실습 DAO 다섯 메서드를 `Statement` 에서 이것으로 옮긴다. **가장 많은 것을 보여 주는 것이 `findBy` 다.**

```java
Project findBy(int no) throws Exception{
  try (PreparedStatement stmt = con.prepareStatement()select 쿼리문){
    stmt.setInt(1,no);
    try(ResultSet rs = stmt.executeQuery()){
      if (rs.next()) {
        Project project = new Project();
        project.setNo(rs.get(컬럼명));
        return project;
      }
      return null;
    }
  }
}
```

**`try` 가 두 겹인 것이 이 문법의 결과다.** 같은 회차의 `list()` 는 자원 둘을 한 괄호에 나란히 선언한다.

```java
try (PreparedStatement stmt = con.prepareStatement(select 쿼리문);
        ResultSet rs = stmt.executeQuery()) {
```

`findBy` 가 그렇게 못 하는 이유는 **`setInt(1,no)` 가 문장 준비와 실행 사이에 들어가야** 하기 때문이다. `try (...)` 의 자원 목록은 선언들만 받으므로 그 사이에 문장을 끼울 수 없고, 그래서 **바인딩할 값이 있으면 `ResultSet` 을 안쪽 `try` 로 내린다.** 값이 없는 조회(`list()`)에서만 한 줄로 붙는다 — 한 노트 안에 두 형태가 나란히 있는 이유가 이것이다 → [[try-with-resources]] · [[result-set]]

그리고 `delete` 가 가장 짧게 갈린다. 문자열을 조립하던 자리가 두 줄로 바뀐다.

```java
boolean delete(int no) throws Exception{
  try (PreparedStatement stmt = con.prepareStatement(delete 쿼리문)) {
    stmt.setInt(1,no);
    int count = stmt.executeUpdate();
    return count > 0;
  }
}
```

**`executeUpdate()` 의 반환값을 처음으로 쓴다.** Day55 의 DAO 는 이 값을 버렸는데, 사흘 뒤 여기서는 `count > 0` 이 곧 「지울 것이 있었는가」의 답이 된다 — 번호가 없는 행을 지우라고 하면 예외가 아니라 **`0` 행 변경**으로 오기 때문이다 → [[dml]] · [[crud]]

### 사흘 뒤 Day58 — 네 줄이 메서드 하나로 접힌다

Day57 의 DAO 는 메서드 다섯 개가 준비·바인딩·실행·닫기를 각각 반복했다. **Day58 은 그 반복을 메서드 하나로 접는다** → [[sql-session]]

```java
public int insert(String sql, Object... values) throws Exception {
  try (PreparedStatement stmt = con.prepareStatement(sql)) {
    int inparameterIndex = 1;
    for (Object value : values) {
      stmt.setString(inparameterIndex++, value.toString());
    }
    return stmt.executeUpdate();
  }
}
```

**이 코드가 이 문법의 두 성질을 정확히 이용한다.** ① `?` 를 가리키는 것이 이름이 아니라 **1부터 세는 번호**라서 값 목록을 `for` 로 돌며 `inparameterIndex++` 로 채울 수 있고(변수명이 Day57 의 「in-parameter」에서 왔다), ② `executeUpdate()` 가 **인수를 받지 않으므로** SQL 을 준비할 때 이미 넘긴 뒤에는 실행 호출이 값과 무관해진다. `Statement` 였다면 문장 문자열을 실행 시점에 완성해야 해서 이런 형태로 접히지 않는다 → [[one-based-numbering]] · [[varargs]]

**그리고 접히면서 `setXXX` 의 XXX 가 하나로 굳는다** — 그 대가가 아래 「경계와 오해」에 있다.

### 다시 하루 뒤 Day59 — `#{}` 가 이 문법으로 내려간다

MyBatis 의 매퍼 XML 에 쓰는 `#{property}` 는 **파싱될 때 `?` 로 바뀐다.** 즉 아래 두 코드가 같은 문장을 만든다 → [[mybatis]]

```xml
<insert id="sql2" parameterType="bitcamp.myapp.vo.User">
    insert into myapp_users(name, email, pwd, tel)
    values (#{name}, #{email}, sha1(#{password}), #{tel})
</insert>
```

```java
// MyBatis 가 실제로 준비하는 것
con.prepareStatement("insert into myapp_users(name, email, pwd, tel) values (?, ?, sha1(?), ?)");
```

**`sha1(#{password})` 가 이 문법의 성질을 하나 더 보인다** — `?` 는 **하나의 값이 올 수 있는 자리**에 서므로 함수의 인수 자리에도 선다. 값을 해싱하는 일은 DB 함수가 하고 자바는 원문을 바인딩만 한다.

그리고 **세 회차에 걸친 문제 하나가 여기서 닫힌다.**

| 회차 | `?` 와 값을 짝짓는 주체 |
|---|---|
| Day57 | 사람이 `setInt(1, no)`·`setString(2, title)` 로 **번호를 센다** |
| Day58 | 세션이 `for` 로 1번부터 채우지만 **`?` 개수와 인수 개수는 아무도 맞춰 주지 않는다** |
| **Day59** | **이름으로 짝짓는다** — `#{name}` 이 몇 번째 `?` 인지는 MyBatis 가 센다 |

`#{ok}` 처럼 뜻 없는 이름도 통하는 것(파라미터가 하나일 때)이 그 증거다. [[sql-session]] 노트가 「`?` 개수와 값 개수를 아무도 맞춰 주지 않는다」·「몇 번째 `?` 에 무엇을 넣는가를 눈으로 확인할 수 없게 됐다」고 적은 구멍이 **이름을 도입함으로써** 메워진다 — **번호가 이름이 되면 순서를 바꿔도 값이 따라온다** → [[one-based-numbering]]

**대신 그 아래에 이 문법의 성질이 그대로 있어서, `${}` 를 쓰는 순간 Day57 이전으로 돌아간다** → [[sql-injection]]

## 왜 중요한가

**값이 문장을 바꿀 수 없게 된다.** 문자열 조립에서는 사용자가 준 글자가 SQL 문법의 일부가 될 수 있었고, 그것이 [[sql-injection]] 이다. `?` 로 넘긴 값은 **값 자리에서 벗어나지 못하므로**, 이름에 `'` 가 있어도(오도철) 문장이 깨지지 않고 `' or 1=1 --` 를 입력해도 그냥 그런 이름을 찾는다. **입력을 검사해서 막는 것이 아니라 구조로 불가능해지는 것**이 이 문법의 값이고, 그래서 이것이 「권장 사항」이 아니라 기본형이다.

**같은 문장을 여러 번 보내는 코드의 비용이 달라진다.** Day55 의 `insertMembers` 는 팀원마다 SQL 문자열을 새로 만들어 보내서 서버가 매번 파싱했다. 뼈대를 한 번 준비하고 값만 바꿔 실행하면 그 반복이 사라진다 — **문자열 조립의 대가가 안전만이 아니라 비용에도 있었다**는 것을 이 문법이 드러낸다 → [[caching]]

**그리고 타입 변환이 코드에서 사라진다.** 문자열 조립에서는 날짜를 `'2024-08-16'` 형태로 맞추고 문자열에 따옴표를 씌우고 숫자는 안 씌우는 일을 **내가 했다.** `setInt`·`setString`·`setDate` 는 그 일을 드라이버에 넘긴다. `String.format("...values('%s')", title)` 같은 줄이 없어지는 것이 코드에서 보이는 가장 큰 변화다 → [[format-string]] · [[date-time]]

## 경계와 오해

- **`?` 는 값 자리에만 쓸 수 있다 — 테이블명·컬럼명·`order by` 방향에는 못 쓴다** — 「매개변수화」라는 말이 「문장의 어느 부분이든 바꿔 끼울 수 있다」로 읽히는데, `?` 가 서는 자리는 **하나의 값이 올 수 있는 자리**뿐이다. `select * from ?`·`order by ?`·`order by no ?` (asc/desc) 는 전부 문법 오류이거나 뜻이 없다(정렬 기준이 「문자열 상수」가 되어 아무 정렬도 안 되는 쪽이 더 나쁘다). 즉 **정렬 컬럼을 사용자가 고르는 화면에는 이 문법이 답을 주지 않고**, 남는 방법은 허용 목록(화이트리스트)으로 골라 문자열에 넣는 것이다 — 인젝션 위험이 그 자리에만 남는다는 것을 알고 다루는 것이 요점이다 → [[sql-injection]]
- **`in (?)` 은 목록으로 펼쳐지지 않는다** — `where no in (?)` 에 `"1,2,3"` 을 넣으면 세 개를 찾는 대신 **`'1,2,3'` 이라는 값 하나**를 찾는다(대개 0행). `?` 하나는 언제나 값 하나이므로, 개수만큼 `?` 를 문자열로 만들어(`in (?,?,?)`) 개수만큼 `set` 해야 한다. **「뼈대는 고정이고 값만 바뀐다」의 예외가 개수가 변하는 목록**이고, 이것이 이 문법을 쓰다가 처음 문자열 조립으로 돌아가게 되는 자리다.
- **`like '%?%'` 는 값 자리가 아니다** — 따옴표 안의 `?` 는 **물음표 글자**이므로 바인딩되지 않고, 「파라미터 개수가 맞지 않는다」로 실패하거나 물음표를 포함한 문자열을 찾는다. `where title like ?` 로 두고 값 쪽에 `"%" + 검색어 + "%"` 를 넣는 것이 옳은 형태다 — **와일드카드는 값의 일부**다. Day57 에는 `like` 가 없지만 이 조합이 실무에서 가장 자주 걸린다 → [[sql-like]]
- **`set` 을 빼먹으면 문장이 실행되지 않는다** — 값이 안 채워진 `?` 가 있으면 `executeQuery()` 가 `No value specified for parameter 1` 로 실패한다. 문자열 조립 시절에는 값이 빠지면 **문법이 깨진 SQL 이 서버까지 가서** 서버의 오류로 나타났는데, 이제 자바 쪽에서 막힌다 — **오류를 만나는 지점이 앞으로 당겨진 것**이고, 실수의 종류가 「이상한 SQL」에서 「빠뜨린 `set`」으로 바뀌어 원인을 읽기 쉬워진다.
- **`Statement.RETURN_GENERATED_KEYS` 를 주는 자리가 옮겨간다** — `Statement` 에서는 `executeUpdate(sql, RETURN_GENERATED_KEYS)` 였는데, 여기서는 **`con.prepareStatement(sql, RETURN_GENERATED_KEYS)`** 다. Day57 이 이것을 정확히 적었다(「PreparedStatement로 생성된 객체는 statement를 생성(PrepareStatement)할 리턴 받는다」 — 문장은 어색하지만 자리는 맞다). 이유는 문장 자체가 **미리 준비되기 때문**이다 — 실행할 때는 넘길 인수가 없으므로 요청을 준비 시점에 해야 한다. 상수는 `Statement` 인터페이스의 것이라 이름이 그대로 `Statement.` 로 시작하는 것도 혼동 지점이다 → [[generated-keys]] · [[static-member]]
- **`executeUpdate(sql)` 을 `PreparedStatement` 에 부르면 예외다** — `PreparedStatement` 는 `Statement` 를 상속하므로 SQL 을 받는 메서드가 **컴파일은 된다.** 그러나 JDBC 명세가 그 호출들을 `SQLException` 으로 규정해서, 급히 SQL 을 끼워 넣으려는 코드가 **런타임에만** 터진다. 상속이 만든 「부를 수 있지만 부르면 안 되는 메서드」의 표본이고, 문장이 이미 정해져 있다는 이 객체의 성질과 어긋나기 때문이다 → [[inheritance]] · [[method-overriding]]
- **안전한 이유는 「특수문자를 이스케이프해서」가 아니다 — 다만 MySQL 기본 설정에서는 그것이기도 하다** — 원리는 **뼈대가 먼저 파싱되어 값이 들어갈 자리가 이미 정해진다**는 것이고(서버측 준비), 그래서 값에 무엇이 있어도 문법으로 해석되지 않는다. 그런데 MySQL Connector/J 는 기본값이 `useServerPrepStmts=false` 라 **드라이버가 클라이언트에서 값을 따옴표로 감싸 문자열을 만들어 보낸다** — 결과는 같지만 경로가 다르다(내가 하던 이스케이프를 드라이버가 정확하게 하는 것). 이 차이가 두 곳에서 드러난다: ① **서버 파싱을 한 번만 한다는 이득이 기본 설정에서는 없다**(`useServerPrepStmts=true`·`cachePrepStmts=true` 를 켜야 한다), ② 그래도 **안전성은 그대로다**(드라이버의 이스케이프는 문자셋을 알고 하므로 내 문자열 조립과 격이 다르다). 「PreparedStatement 는 빠르다」로 외우면 켜지지도 않은 이득을 근거로 삼는다 → [[caching]] · [[character-encoding]]
- **매번 새로 만들면 재사용 이득이 없다 — Day58 에도 그대로다** — Day57 의 DAO 는 메서드마다 `prepareStatement` 를 부르고 [[try-with-resources]] 로 닫는다. 이것이 자원 관리로는 옳지만 **「한 번 준비하고 여러 번 실행」은 일어나지 않는다** — 그 이득은 같은 문장을 반복하는 루프(팀원 열 명을 넣는 `insertMembers`)에서 문장을 **루프 밖에서 한 번** 만들 때 나온다. 필기의 §1.3.1 예제도 같은 변수 이름으로 문장을 두 번 새로 만든다. **사흘 뒤 Day58 이 그 네 줄을 세션 메서드 하나로 접어도 이 상태는 바뀌지 않는다** — 호출마다 준비하고 닫는 규율이 그대로 옮겨 갔기 때문이고, 오히려 문장이 메서드 안에서 태어나 죽으므로 밖에서 재사용할 길이 더 좁아졌다. 즉 **Day57 이 얻은 것은 안전이고, Day58 이 더 얻은 것은 중복 제거이며, 성능은 두 회차 다 아니다** → [[for-loop]] · [[sql-session]]
- **`setString` 으로 숫자 컬럼에 넣어도 대개 돌아간다 — 그리고 인덱스를 못 탄다** — `where no = ?` 에 `setString(1, "3")` 을 하면 MySQL 이 암묵 변환을 해서 결과가 맞게 나온다. 그러나 컬럼과 값의 타입이 다르면 옵티마이저가 **인덱스를 쓰지 못하는 경우**가 생겨 전체 훑기로 바뀐다. 「돌아가니까 맞다」가 성능으로 새는 자리이고, `setXXX` 의 XXX 를 **컬럼 타입에 맞추는 것**이 규율이다 → [[database-index]] · [[type-casting]]
- **`setString(i, value.toString())` 은 위 항목을 규칙으로 굳힌 것이다 — Day58 의 세션이 값을 전부 문자열로 보낸다** — `Object...` 로 받은 값에서는 타입을 알 수 없으니 `toString()` 으로 밀어 `setString` 하나만 부르는데, 세 갈래로 깨진다. ① **`null` 이 오면 DB 에 닿기도 전에 `NullPointerException`** 이다 — `null.toString()` 이므로 SQL 오류가 아니라 자바 오류로 나타나서 원인이 「값이 비어 있다」로 읽히지 않는다. 옳은 형태는 `stmt.setNull(i, java.sql.Types.VARCHAR)` 이다. ② **날짜는 어느 `Date` 인지에 따라 통하거나 깨진다** — `java.sql.Date.toString()` 은 `2024-08-19` 라서 우연히 통하지만 `java.util.Date.toString()` 은 `Mon Aug 19 00:00:00 KST 2024` 이고, MySQL 이 strict 모드면 `Incorrect date value` 로 거절하고 아니면 **`0000-00-00` 을 조용히 저장한다.** ③ `boolean` 은 `"true"` 가 되어 `tinyint(1)` 컬럼에서 거절되거나 `0` 이 된다. **표면상 「전부 문자열이니 일관되다」인데 실제로는 타입마다 다른 결과가 나오고, 그중 일부만 오류로 보인다** — 진짜 답은 갈래를 늘리는 것이 아니라 `stmt.setObject(i, value)` 로 **타입 판단을 드라이버에 되돌려 주는 것**이다 → [[sql-null]] · [[date-time]] · [[sql-data-type]] · [[sql-session]]
- **문장을 감싸는 메서드는 `RETURN_GENERATED_KEYS` 를 넘길 자리를 잃는다** — 이 문법에서 키 요청은 `con.prepareStatement(sql, flag)` 에 들어가는데, Day58 의 세션은 `con.prepareStatement(sql)` 만 부르고 `int` 하나를 돌려주며 문장을 닫는다. 즉 **감싸는 층을 만들면 준비 시점에 주어야 하는 옵션이 전부 그 층의 API 문제로 바뀐다** — 실행 시점 인수라면 호출부에서 더 넘길 수 있었지만, 준비 시점 옵션은 감싼 메서드가 인수로 받아 주지 않으면 도달할 방법이 없다. 요청 자리가 준비로 옮겨간 이 문법의 성질이 여기서 설계 제약으로 나타난다 → [[generated-keys]] · [[sql-session]]
- **`setDate` 가 받는 것은 `java.sql.Date` 다** — `java.util.Date` 를 그대로 넘길 수 없어서(컴파일 오류) `new java.sql.Date(utilDate.getTime())` 변환이 필요하고, 시각까지 넣으려면 `setTimestamp` 다. `setDate` 는 **날짜만** 보내므로 시·분·초가 조용히 잘린다. 이름이 같은 두 클래스가 `java.sql` 과 `java.util` 에 있는 것이 이 API 에서 가장 자주 만나는 import 사고다 → [[date-time]] · [[package]]
- **`stmt.set(?,values)` 라는 메서드는 없다** — Day57 §2.1 의 `insert`·`update` 코드가 `stmt.set(?,values)`·`set(?,project.values)` 로 적혀 있다. 자리를 표시한 의사코드로 읽히지만, 실제로는 **`?` 개수만큼 `setInt`·`setString`·`setDate` 를 번호와 함께** 적어야 하고 그 줄 수가 `insert` 의 컬럼 수만큼 늘어난다 — `PreparedStatement` 로 바꾸는 일의 실제 노동이 정확히 거기에 있는데 필기는 그것을 한 줄로 접었다. `update` 쪽은 `set` 을 `stmt.` 없이 적어 **호출 대상도 빠져 있다.**
- **`con.prepareStatement()select 쿼리문` 은 괄호가 잘못 닫혔다** — Day57 §2.1 `findBy` 의 첫 줄이고, 인수가 괄호 밖으로 나가 컴파일되지 않는다. 같은 블록의 `int count = stmt.executeUpdate()` 두 곳에는 세미콜론이 없고, §1.3.1 의 `executQuery()`·`executUpdate()` 는 `e` 가 빠진 오기다(`executeQuery`·`executeUpdate`). **필기의 코드는 형태를 보여 주는 스케치이지 그대로 옮겨 쓸 수 있는 것이 아니다.**
- **`#{}` ≠ `${}` — 한 글자 차이가 이 문법의 안쪽과 바깥쪽이다** — MyBatis 의 `#{}` 는 `?` 로 바뀌어 이 문법을 그대로 쓰고, `${}` 는 **문자열을 그 자리에 붙여** Day57 이 버린 `Statement` 조립으로 돌아간다. **Day59 의 필기가 `#{}` 를 후자로 설명한다** — 「xml에 작성된 `#{property}`을 `getPorperty()`으로 변환을 한다」·「`user.getProperty()`를 하여 sql구문을 완성한다」·「완성된 sql구문을 sql서버에 전송한다」. 그 설명이 맞다면 **프레임워크로 옮기는 순간 Day57 이 얻은 것이 전부 되돌아간다**(값이 다시 문장의 일부가 된다). 실제로는 되돌아가지 않았고, 필기가 서술한 동작은 `${}` 쪽의 것이다 → [[mybatis]] · [[sql-injection]]
- **`setObject` 가 여기서 답으로 확인된다** — Day58 의 세션이 `Object...` 로 받아 타입을 잃고 `setString` 하나로 몰렸던 자리에서, MyBatis 는 값의 실제 타입을 보고 `setXXX` 를 고르고 모르면 `setObject` 를 부른다(`jdbcType` 을 적어 지정할 수도 있다). **하루 만에 「진짜 답은 `setObject` 다」가 프레임워크의 구현으로 나타난 셈**이고, 그것이 가능한 이유는 MyBatis 가 값을 `Object` 로만 아는 게 아니라 **프로퍼티의 선언 타입까지 리플렉션으로 볼 수 있기 때문**이다 → [[sql-session]] · [[varargs]] · [[reflective-invocation]]
- **`?` 를 쓸 수 없는 자리는 MyBatis 에서도 그대로다** — 위의 「식별자·`in` 목록·`like` 안」 항목이 프레임워크를 써도 유효하다. 테이블명이나 `order by` 컬럼을 바꿔 끼우려면 `#{}` 가 아니라 `${}` 를 써야 하고, **그 자리가 정확히 인젝션이 남는 자리**다. 즉 「`?` 가 설 수 없는 곳」이라는 이 문법의 한계가 프레임워크에서 **문법이 두 개인 이유**로 나타난다 → [[sql-injection]]
- **매퍼 XML 로 옮기면 `<` 를 그대로 쓸 수 없다** — 자바 문자열 안에서는 아무 문제 없던 `where no < 10` 이 XML 에서는 파싱 오류다(`&lt;` 나 `CDATA` 가 필요하다). **문장을 어디에 적는가가 쓸 수 있는 글자를 정한다**는 것이 이 문법의 문제는 아니지만, `PreparedStatement` 를 프레임워크에 맡기며 새로 생기는 제약이라 함께 봐야 한다 → [[xml]] · [[sql-operator]]
- **PreparedStatement ≠ 저장 프로시저** — 「미리 준비한다」는 말이 DB 에 이름을 붙여 저장해 두는 것처럼 들리는데, 이 준비는 **그 연결에서 그 객체가 사는 동안만** 유효하다. 연결이 끊기면 사라지고, 다른 연결에서 쓸 수 없다. DB 안에 남는 것은 `create procedure` 로 만드는 것이고 그것을 부르는 것은 `CallableStatement` 다 → [[socket]]
- **PreparedStatement 로 바꾸는 것이 트랜잭션을 만들어 주지는 않는다** — Day57 은 §2.1 에서 DAO 를 안전하게 바꾸고 §2.2 에서 커밋 경계를 따로 넣는다. **문장 하나의 안전**(값이 문법을 바꾸지 못함)과 **여러 문장의 원자성**은 다른 축이고, 전자를 고쳐도 등록이 절반만 성공하는 문제는 그대로 남는다 → [[transaction]]

## 함께 보는 개념

- [[sql-injection]] — 이 문법이 답으로 나온 문제
- [[jdbc]] — `Statement` 와 나란히 사는 층
- [[result-set]] — `executeQuery()` 가 돌려주는 커서
- [[generated-keys]] — 요청 자리가 준비 시점으로 옮겨가는 자리
- [[try-with-resources]] — 바인딩 때문에 `try` 가 두 겹이 되는 이유
- [[transaction]] — 같은 회차에서 따로 채워지는 다른 축
- [[dml]] · [[dql]] — `executeUpdate` 와 `executeQuery` 가 각각 맡는 문장
- [[caching]] — 뼈대를 한 번 준비한다는 이득이 실제로 나는 조건
- [[sql-like]] — 와일드카드가 값의 일부가 되는 자리
- [[one-based-numbering]] — `?` 번호가 1부터인 자리
- [[format-string]] — 이 문법이 대신하는 문자열 조립
- [[date-time]] — `setDate`·`setTimestamp` 가 갈리는 자리
- [[database-index]] — 타입을 맞추지 않으면 새는 곳
- [[crud]] — DAO 다섯 메서드가 함께 바뀌는 자리
- [[sql-session]] — 이 문법을 다루는 절차를 한 클래스로 접는 다음 걸음
- [[varargs]] — 그 클래스가 값 목록을 받는 문법
- [[sql-null]] — 값이 `null` 일 때 바인딩이 갈리는 자리
- [[mybatis]] — `#{}` 라는 이름으로 이 문법을 감싼 층
- [[xml]] — 그 문장이 옮겨 간 곳과 거기서 새로 생기는 제약

## 출처

- [[2024-08-16-Day57]] — 「1.3 Statment의 문제점」에서 문자열 조립의 위험을 세운 직후 「1.3.1 PreparedStatement 생성」으로 이 문법을 도입한다. 세 줄(「매개변수화하는 방법」·「?으로 표시한다」·「**in-parameter** : ? 값으로 들어갈 타입에 따라 set()으로 설정한다」)과 `select`·`update` 두 예제가 문법 골격이고, 「1.4 Primary Key return」이 **자동 생성 키 요청이 `prepareStatement` 쪽으로 옮겨간다**는 것을 따로 적었다. 실습 §2.1 은 DAO 다섯 메서드(`insert`·`list`·`findBy`·`update`·`delete`)의 `Statement` 판과 `PreparedStatement` 판을 **나란히 놓아** 무엇이 바뀌는지 보여 주고, 그중 `findBy` 가 `setInt` 때문에 `try` 를 두 겹으로 쓰게 되는 자리, `delete` 가 `executeUpdate()` 의 반환값을 `count > 0` 으로 쓰는 자리가 이 회차의 값이다. 다만 「보완성」은 보안성의 오기이고, 코드에는 실제로 없는 `stmt.set(?,values)`·`rs.get(컬럼명)` 이 쓰이며 `con.prepareStatement()select 쿼리문` 은 괄호가 잘못 닫혔고 `executQuery`·`executUpdate` 는 `e` 가 빠졌다. `?` 를 쓸 수 없는 자리(식별자·`in` 목록·`like` 안), 문장을 재사용해야 준비 이득이 난다는 것, MySQL 드라이버가 기본적으로 클라이언트에서 준비한다는 것은 필기에 없다
- [[2024-08-19-Day58]] — 사흘 뒤. 이 문법을 **다루는 절차를 메서드 하나로 접은** 회차다. `insert(String sql, Object... values)` 안에서 `con.prepareStatement(sql)` → `for` 로 `?` 를 1번부터 채우기 → `executeUpdate()` 까지가 한 몸이 되고, 그것이 가능한 근거가 이 문법의 두 성질(번호로 가리키는 `?`, 인수 없는 `executeUpdate()`)이다. 변수명 `inparameterIndex` 가 Day57 의 「in-parameter」를 그대로 옮긴 것이라 두 회차가 이어지는 것이 이름에서 보인다. 다만 값을 전부 `value.toString()` + `setString` 으로 보내 **Day57 이 얻은 「타입 변환이 코드에서 사라진다」를 되돌렸고**(`null`·`java.util.Date`·`boolean` 에서 각각 다르게 깨진다), `con.prepareStatement(sql)` 만 부르므로 [[generated-keys]] 요청을 넘길 자리가 사라졌다. `setObject` 도, 문장을 재사용하는 형태도 필기에 없다 → [[sql-session]]
- [[2024-08-20-Day59]] — 다시 하루 뒤. 이 문법이 **`#{property}` 라는 이름 아래로 내려간다** — MyBatis 의 매퍼 XML 에 쓰는 `#{}` 는 파싱될 때 `?` 로 바뀌고 값은 `setXXX` 로 따로 가므로, `values (#{name}, #{email}, sha1(#{password}), #{tel})` 가 곧 `values (?, ?, sha1(?), ?)` 다. **`?` 를 가리키는 것이 번호에서 이름으로 바뀌는 것**이 이 회차가 이 문법에 더한 것이고, 그래서 Day57 이 사람에게 맡겼던 번호 세기와 Day58 이 아무도 맞춰 주지 않게 만든 개수 일치가 함께 없어진다(`#{ok}` 처럼 파라미터가 하나면 이름조차 아무래도 좋다). 다만 **필기는 `#{}` 를 「getter 를 불러 sql구문을 완성한다」로 설명해 `${}` 의 동작으로 적었고**, 그 설명대로면 프레임워크로 옮기는 순간 Day57 이 얻은 안전이 되돌아간다는 결론이 나온다. `${}` 라는 다른 표기가 실제로 있다는 것, MyBatis 가 값의 타입을 보고 `setXXX` 를 고르거나 `setObject` 로 넘긴다는 것, 매퍼 XML 에서는 `<` 를 그대로 쓸 수 없다는 것은 필기에 없다 → [[mybatis]] · [[sql-injection]]
