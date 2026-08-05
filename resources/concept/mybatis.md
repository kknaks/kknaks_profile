---
type: concept
id: mybatis
title: MyBatis
aliases:
  - MyBatis
  - mybatis
  - 마이바티스
  - mybatis-config.xml
  - 매퍼 XML
  - Mapper XML
  - 매퍼 파일
up:
  - 2024-08-20-Day59
  - 2024-08-21-Day60
  - 2024-08-22-Day61
  - 2024-08-23-Day62
tags:
  - java
  - database
  - 프레임워크
  - SQL
---

# MyBatis

**SQL 문장을 자바 코드 밖(XML)에 두고 id 로 불러 실행하는 [[persistence-framework]] 의 SQL Mapper 쪽 구현.** 하루 전 Day58 이 손으로 만든 세션은 SQL 문자열을 **인수로** 받았는데, MyBatis 는 그 자리에 **문장의 id** 를 받는다 — 그 한 글자 차이가 SQL 을 자바에서 떼어 낸 것이다 → [[sql-session]] · [[jdbc]]

## 정의

층이 넷이고 Day59 가 그 넷을 순서대로 다룬다.

| 층 | 파일·객체 | Day59 의 절 |
|---|---|---|
| 설정 | `mybatis-config.xml` | 「설정파일 준비」 |
| 공장 | `SqlSessionFactoryBuilder` → `SqlSessionFactory` | 「SqlSession 객체 생성」 |
| 실행 | `SqlSession` | 「selectList()」~「delete()」 |
| 문장 | 매퍼 XML (`UserDaoMapper.xml`) | 각 절의 XML 조각 |

**하루 뒤 Day60 이 넷 중 두 층에 살을 붙인다** — 그리고 그 셋이 각각 Day59 가 열어 둔 구멍이다.

| Day60 이 더한 것 | 어느 층 | Day59 가 남긴 무엇을 메우나 |
|---|---|---|
| `<resultMap>`·`<association>`·`<collection>` | 문장 | `user_id as no` 로만 맞추던 대응 → [[result-map]] |
| `<foreach>` | 문장 | 값의 개수가 정해지지 않는 문장 → [[dynamic-sql]] |
| `<typeAliases>` | **설정** | `parameterType="user"` 가 실패한 이유 → [[type-alias]] |

**세 개가 「문장을 자바에서 뺀 다음에 생기는 문제들」이다.** 뺀 SQL 이 결과를 객체로 만들지 못하거나(첫째), 길이가 고정되어 있거나(둘째), 클래스를 짧은 이름으로 못 부르는(셋째) 상태를 각각 푼다.

### 공장 사다리 — 세 객체의 수명이 다르다

필기가 세 줄로 그 순서를 적었다 — 「SqlSession을 인스턴스하기 위해서는 SqlSessionFactory 객체가 필요하다」·「SqlSessionFactory를 인스턴스하기 위해서는 SqlSessionFactoryBuilder 객체가 필요하다」·「SqlSessionFactoryBuilder가 xml파일을 읽어 Factory 객체를 인스턴스해야한다」.

```java
InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(inputStream);
SqlSession sqlSession = sqlSessionFactory.openSession(false);
```

**사다리가 세 칸인 이유는 각 칸의 수명이 다르기 때문이다.**

| 객체 | 몇 개 | 언제까지 |
|---|---|---|
| `SqlSessionFactoryBuilder` | 쓰고 버린다 | XML 을 한 번 읽는 동안만 |
| `SqlSessionFactory` | **앱에 하나** | 프로그램이 사는 동안 |
| `SqlSession` | 작업마다 하나 | **그 작업 하나** — 커밋 경계와 같다 |

Day58 의 세션은 「연결을 누가 만들고 누가 닫는지 정해지지 않았다」는 상태였는데, MyBatis 는 그 질문을 **세 칸으로 나눠** 답한다 → [[sql-session]] · [[xml]]

### 다섯 메서드 — 첫 인수가 SQL 이 아니라 id 다

| 자바 | XML 태그 | 돌려주는 것 |
|---|---|---|
| `sqlSession.selectList("aaa.sql1")` | `<select>` | `List` |
| `sqlSession.selectOne("sql3.findBy", no)` | `<select>` | 객체 하나 (**반드시 1개**) |
| `sqlSession.insert("aaa.sql2", user)` | `<insert>` | 변경된 행 수 |
| `sqlSession.update("UserDao.update", user)` | `<update>` | 변경된 행 수 |
| `sqlSession.delete("UserDao.delete", no)` | `<delete>` | 변경된 행 수 |

필기가 다섯 절에서 같은 첫 줄을 반복한다 — 「java에서는 XML에 태그를 넘기면서 sqlSession의 메서드를 호출한다」. **넘기는 것이 SQL 이 아니라 「그 SQL 을 찾을 이름」**이라는 것이 이 프레임워크의 형태 전부다 → [[dql]] · [[dml]] · [[crud]]

### 값이 오가는 두 방향

필기가 방향마다 걸음을 나눠 적었다.

**들어가는 쪽** (`#{property}` — 「insert()」 절)

1. 「java에서 받은 id를 찾아서 쿼리문을 실행한다」
2. 「파라미터로 받은 User타입에서 getter메서드를 찾는다」
3. 「xml에 작성된 `#{property}`을 `getPorperty()`으로 변환을 한다」
4. 「파라미터로 받은 user에서 `user.getProperty()`를 하여 sql구문을 완성한다」

**나오는 쪽** (`resultType` — 「selectOne()」 절)

1. 「sql 서버에서 받은 table의 컬럼 정보로 property name을 생성한다」
2. 「`resultType`에서 `setProperty(Object obj)`를 호출하여 객체에 정보를 넣는다」
3. 「완성된 객체를 java에 넘겨준다」

**두 방향 모두 리플렉션이다.** 같은 회차 앞부분의 [[reflective-invocation]]·[[reflective-instantiation]]·[[reflective-field-access]] 가 정확히 이 일을 하는 도구이고, `resultType="bitcamp.myapp.vo.User"` 라는 **문자열**이 [[class-loading]] 의 `Class.forName` 에 닿는다 — **한 날에 배운 두 주제가 서로의 안팎인데 필기는 이어 붙이지 않았다.**

들어가는 쪽의 3~4 단계 설명은 정확하지 않다(아래 「경계와 오해」의 첫 항목) → [[prepared-statement]]

## 사용 예시

Day59 가 다섯 메서드를 **자바 한 줄 + XML 한 조각**으로 짝지어 실었다. 조회 두 개가 대비를 보인다.

```java
sqlSession.selectList("aaa.sql1");
```

```xml
<select id="sql1" resultType="bitcamp.myapp.vo.User">
    select
        user_id as no,
        name,
        email
    from
        myapp_users
    order by
        user_id asc
</select>
```

**`user_id as no` 가 이 매핑의 핵심 장치다.** 컬럼 이름과 자바 프로퍼티 이름이 다를 때 SQL 의 별칭으로 맞춘다 — 「쿼리문을 실행해서 나온 테이블을 resultType에서 받아온 User 객체를 생성하고 담는다」가 되려면 컬럼 라벨이 `no` 여야 `setNo` 를 찾을 수 있다 → [[dql]] · [[surrogate-key]]

```java
sqlSession.selectOne("sql3.findBy", no);
```

```xml
<select id="sql3" resultType="bitcamp.myapp.vo.User" parameterType="int">
select
    user_id as no,
    name,
    email,
    tel
from
    myapp_users
where
    user_id = #{ok}
</select>
```

**`#{ok}` 라는 이름이 아무 뜻도 없는데 통한다.** 필기가 이유를 정확히 적었다 — 「primitive 타입의 property name은 없기때문 사용자가 임의로 작성 가능하다」. 파라미터가 하나면 MyBatis 는 이름을 보지 않는다.

변경 쪽은 값이 여러 개 들어가고, SQL 함수 안에도 `#{}` 가 선다.

```java
sqlSession.update("UserDao.update", user);
```

```xml
<update id="update" parameterType="user">
  update myapp_users set
    name=#{name},
    email=#{email},
    pwd=sha1(#{password}),
    tel= #{tel}
  where
    user_id=#{no}
</update>
```

**`pwd=sha1(#{password})` 가 두 가지를 한꺼번에 보인다.** 컬럼 이름은 `pwd` 인데 프로퍼티 이름은 `password` 이므로 **들어가는 쪽에서는 자바 이름을 쓰고**(컬럼 이름은 `=` 왼쪽이 갖는다), 값을 해싱하는 일은 **DB 함수**가 한다 — 자바에서 해시를 계산해 넘기지 않는다 → [[sql-date-function]] · [[database-user]]

그리고 삭제가 가장 짧다.

```java
sqlSession.delete("UserDao.delete", no);
```

```xml
<delete id="delete" parameterType="int">
    delete from myapp_users
    where user_id=#{ok}
</delete>
```

**Day57 의 DAO 메서드 하나가 자바 한 줄 + XML 네 줄이 됐다.** [[sql-session]] 노트가 Day58 기준으로 「남는 것은 SQL 과 값뿐」이라고 적은 자리에서, 이번에는 **SQL 마저 자바에서 빠진다** → [[dao-pattern]]

## 왜 중요한가

**SQL 문장이 자바 파일에서 사라진다.** Day55~58 의 DAO 는 자바 문자열 안에 SQL 이 있어서, 문장을 고치려면 자바 파일을 열고 컴파일을 다시 해야 했고 긴 문장은 `+` 로 이어 붙여 읽기 어려웠다. 매퍼 XML 로 옮기면 문장이 **줄바꿈 그대로** 있고 자바 코드는 id 만 안다 — [[sql-session]] 노트가 「이 회차가 걷어낸 것은 절차이고 SQL 을 자바에서 떼어 내는 일은 아직 남아 있다」고 적은 그 남은 일이 여기서 끝난다 → [[coupling]] · [[encapsulation]]

**그리고 Day57~58 이 손으로 하던 것들이 하나씩 설정 한 줄로 바뀐다.** 연결을 필드로 들고 공유하던 것은 `<dataSource type="POOLED">` 로, `con.setAutoCommit(false)` 는 `openSession(false)` 로, `?` 번호를 사람이 세던 것은 `#{name}` 이라는 **이름**으로 바뀐다. **세 회차에 걸쳐 하나씩 손으로 만든 것이 각각 어느 설정에 대응하는지 알고 쓰는 것**이 이 순서로 배운 값이다 → [[transaction]] · [[prepared-statement]]

**대신 어긋남이 컴파일에서 잡히지 않는 자리가 셋 늘어난다** — 문장 id, 프로퍼티 이름, 타입 별칭. 셋 다 문자열이라 컴파일러가 보지 않는다. Day59 의 필기 자체가 그 세 자리에서 실제로 어긋나 있다(아래) → [[reflective-invocation]]

**셋이 걸리는 시점은 같지 않다 — Day60 의 `<typeAliases>` 를 알고 나면 갈린다.** 처음에는 「셋 다 실행 시점 예외로만 온다」로 뭉쳤는데, 타입 별칭과 `<resultMap>` id 는 **설정과 매퍼를 읽는 시작 시점**에 해소되므로 어긋나면 프로그램이 아예 뜨지 않는다. 문장 id 는 그 문장을 **부를 때**, 프로퍼티 이름은 부를 때이거나 **아무 일도 안 일어난다**(예외 없이 `null`). **위로 갈수록 이르고 아래로 갈수록 나쁘다** — 배포 전에 반드시 드러나는 것과 그 화면을 써 봐야 아는 것과 데이터를 보고서야 아는 것이다 → [[type-alias]] · [[result-map]]

## 경계와 오해

- **`#{}` 는 문자열 치환이 아니다 — `?` 로 간다** — 이 필기의 가장 큰 오류다. 「xml에 작성된 `#{property}`을 `getPorperty()`으로 변환을 한다」·「`user.getProperty()`를 하여 sql구문을 완성한다」·「완성된 sql구문을 sql서버에 전송한다」는 **`${}` 의 동작**이다. `#{}` 는 파싱될 때 **`?` 로 바뀌어** `PreparedStatement` 가 되고, 값은 `setXXX` 로 따로 간다. 이 차이가 사소하지 않은 이유는 **필기의 설명이 맞다면 MyBatis 를 써도 SQL 삽입에 열려 있게 되기 때문**이다 — 나흘 전 Day57 이 `Statement` 를 버리고 얻은 것이 프레임워크로 옮기면서 되돌아간다는 결론이 나온다. 실제로는 되돌아가지 않았고, `#{}` 를 쓰는 한 값은 문장이 될 수 없다 → [[prepared-statement]] · [[sql-injection]]
- **`${}` 와 `#{}` 를 가르는 것이 이 프레임워크의 첫 보안 규칙이다** — 한 글자 차이인데 하나는 바인딩이고 하나는 **문자열 붙이기**다. `${}` 를 써야 하는 자리가 실제로 있다 — 테이블명·정렬 컬럼처럼 [[prepared-statement]] 의 `?` 가 설 수 없는 곳이다. 그래서 인젝션 위험은 「없어진」 것이 아니라 **`${}` 를 쓰는 자리에 모인** 것이고, 거기서는 허용 목록으로 값을 걸러야 한다. Day58 노트가 「위험이 호출부로 옮겨간다」고 적은 것이 이번에는 **매퍼 XML 로 옮겨간다** → [[sql-injection]]
- **`openSession(false)` 는 autocommit 을 끄는 것이고, 이 필기에는 `commit()` 이 없다** — 그래서 Day59 의 `insert`·`update`·`delete` 예제는 **DB 에 아무것도 남기지 않는다.** 세션을 닫을 때 미확정 트랜잭션이 롤백되기 때문이다. 그리고 이것이 조용한 실패다 — `insert()` 가 **변경된 행 수 1 을 돌려주므로** 부르는 쪽에는 성공으로 보이고, 예외도 로그도 없고, `select` 를 같은 세션에서 하면 자기 변경이 보이기까지 한다([[transaction]] 노트의 「내 트랜잭션 안에서는 내 변경이 보인다」). **화면은 「등록됨」이라 말하고 테이블은 비어 있는 상태**이며, 고칠 곳은 오류가 보이는 자리가 아니라 **작업이 끝나는 자리에 없는 `sqlSession.commit()` 한 줄**이다. Day57 §2.2 가 `con.setAutoCommit(false)` → `con.commit()` 짝을 정확히 썼던 것이 여기서 앞쪽만 옮겨 온 셈이다 → [[transaction]]
- **`openSession()`(인수 없음)도 자동 커밋이 아니다 — JDBC 와 기본값이 반대다** — [[transaction]] 노트의 시작이 「mysql은 autocommit의 기본 값이 true이다」이고 JDBC 연결도 그것을 물려받는데, **MyBatis 의 기본은 `false`** 다. 그래서 「인수를 안 넘겼으니 원래대로겠지」로 읽으면 위 항목의 사고가 **인수를 지운 코드에서도 그대로 난다.** 배운 기본값이 층을 하나 올라가며 뒤집히는 자리다.
- **문장 id 가 이 필기 안에서 세 곳 어긋나 있다** — 문자열이라 컴파일러가 보지 않는다. ① `insert()` 는 자바가 `"aaa.sql2"` 인데 XML 이 `id="slq2"` 로 **철자가 뒤집혀** 있다. ② `selectOne()` 은 자바가 `"sql3.findBy"` 인데 XML 이 `id="sql3"` 이라, MyBatis 는 **네임스페이스 `sql3` 의 `findBy`** 를 찾아 실패한다. ③ 네임스페이스가 한 노트 안에서 `aaa`·`sql3`·`UserDao` 셋으로 갈린다. 셋 다 실행 시점 `BindingException`(「Mapped Statements collection does not contain value for …」)이며, **id 를 문자열로 지목하는 대가가 `getMethod("이름")` 과 똑같다** → [[reflective-invocation]]
- **`<mapper namespace="…">` 루트 태그가 네 XML 조각에 하나도 없다** — 그런데 자바 쪽은 `aaa.sql1`·`UserDao.update` 처럼 **점 앞에 네임스페이스를 붙여** 부른다. 그 네임스페이스는 매퍼 파일의 루트 태그가 정하는 것이라, 조각만 보면 「점 앞이 어디서 오는가」에 답이 없다. 필기가 `<select>`·`<insert>` 만 잘라 실은 결과이고, **id 가 파일 안에서 유일한 것으로는 부족하고 네임스페이스까지 합쳐 전역 유일해야 한다**는 규칙이 그래서 보이지 않는다.
- **`parameterType="user"` 는 별칭 등록이 없으면 실패한다 — 그 등록 문법을 하루 뒤 Day60 이 배운다** — 다른 네 곳은 `bitcamp.myapp.vo.User` 로 정규명을 쓰는데 `<update>` 만 짧은 이름이다. 짧은 이름이 통하려면 설정에 `<typeAliases>` 나 `@Alias` 가 있어야 하고, Day59 의 `mybatis-config.xml` 에는 둘 다 없다 — `Could not resolve type alias 'user'` 로 **XML 을 읽는 순간** 걸린다. 「대문자를 소문자로 쓰면 되는 것」이 아니라 **어딘가에 등록해 두어야 하는 이름**이다. 그리고 같은 회차의 `parameterType="int"` 가 통했던 것은 **`int` 가 MyBatis 의 기본 별칭으로 이미 등록되어 있기 때문**이다 — 같은 자리에 같은 모양으로 적힌 짧은 이름 둘 중 하나만 실패한 이유가 그것이고, Day60 의 「typeAliases」 절이 그 사전을 내가 늘리는 방법이다 → [[type-alias]]
- **`parameterType` 은 사실 적지 않아도 되고, `resultType` 은 없으면 성립하지 않는다** — 비대칭이다. 넘긴 객체의 타입은 MyBatis 가 실행 시점에 알 수 있지만(값이 손에 있다), 결과를 **무엇으로 만들지**는 알 방법이 없다. Day58 노트가 「`insert` 는 값을 보내기만 하므로 타입을 몰라도 되지만 `select` 는 받아서 무언가로 만들어야 하므로 타입 정보를 반드시 밖에서 받아야 한다」고 빈 코드 블록 자리에 적어 둔 예측이 **이번 회차의 XML 문법으로 확인된다** → [[sql-session]] · [[generics]]
- **`setProperty(Object obj)` 라는 메서드는 없다** — 필기의 표현이다. MyBatis 가 하는 일은 ① 기본 생성자로 객체를 만들고 ② 컬럼 라벨에 맞는 **setter 를 찾아 부르거나** ③ setter 가 없으면 **필드에 직접 넣는** 것이다. 그래서 **setter 를 안 만들어도 매핑이 되고**, 반대로 setter 이름이 어긋나면 예외 없이 값이 비어 있다. 세 걸음이 각각 같은 회차 앞부분의 세 절이다 → [[reflective-instantiation]] · [[reflective-field-access]] · [[reflective-invocation]]
- **컬럼 이름과 프로퍼티 이름이 다르면 조용히 비어 있다** — 예외가 아니라 `null`(또는 `0`)이다. `user_id as no` 별칭이 그것을 막는 장치이고, 별칭을 빼면 `getNo()` 가 `0` 을 돌려주는 객체가 목록에 담긴다 — **그 `0` 이 다음 화면에서 조회 조건으로 쓰이면 「없는 번호」가 되어 원인이 두 화면 뒤에서 나타난다.** 방법이 세 가지다: SQL 별칭(Day59 가 쓴 것), `<resultMap>` 으로 대응을 따로 적기, `mapUnderscoreToCamelCase` 설정으로 `user_id ↔ userId` 를 자동 변환하기. **둘째 방법을 하루 뒤 Day60 이 실제로 배우고**, 거기서 이 태그가 이름 맞추기보다 큰 일을 한다는 것이 드러난다 — 조인 결과를 객체 안의 객체·목록으로 접는 것 → [[sql-null]] · [[result-map]]
- **이틀 뒤 Day61 이 `@Param` 과 매퍼 인터페이스를 직접 만든다 — 둘 다 이 프레임워크에 이미 있는 것이다** — 아래 「`#{ok}` 가 통하는 것은 파라미터가 하나일 때뿐이다」 항목이 답으로 든 셋(`@Param("no")`·`Map`·`#{param1}`) 중 **앞의 둘을 Day61 이 손으로 짓는다.** 매개변수가 둘 이상이면 `HashMap<String,Object>` 에 담아 넘기고, 그 키가 될 이름을 얻으려고 `@Retention(RUNTIME)` + `@Target(PARAMETER)` 로 **`@Param` 이라는 이름의 애노테이션을 새로 선언한다** — MyBatis 의 `org.apache.ibatis.annotations.Param` 과 이름도 뜻도 같다. 같은 회차가 DAO 를 인터페이스로 바꾸고 [[dynamic-proxy]] 로 구현체를 만드는 것도 **이 프레임워크의 매퍼 인터페이스와 같은 물건**이다(이 노트가 「잃은 것의 일부를 되찾는 다음 걸음」이라 적어 둔 것). **모르고 다시 만든 것이 손해가 아닌 자리**다 — 프레임워크가 그 애노테이션을 왜 갖고 있는지가 「없으면 무엇이 안 되는가」로 손에 남는다. 다만 직접 만들면 **문장 id 규약도 스스로 정해야** 하고 Day61 은 그 자리를 `"sql.method"` 라는 자리표시자로 비워 두었다 → [[dynamic-proxy]] · [[annotation-target]] · [[annotation-retention]]
- **Day61 의 서버는 접속마다 쓰레드를 붙이면서 `SqlSession` 을 한 벌만 쓴다 — 위 수명 표가 깨지는 자리** — 이 노트의 표가 `SqlSession` 을 「작업마다 하나 — **그 작업 하나**, 커밋 경계와 같다」로 적었는데, Day61 의 DAO 프록시는 `appCtx` 에 한 벌만 등록되어 **모든 접속이 같은 세션을 공유한다.** 세션은 쓰레드 안전하지 않아 동시 호출에서 결과가 섞이고, 더 나쁜 것은 `commit()` 이 **남의 미완성 변경까지 확정한다**는 것이다 — 위 「`commit()` 이 없다」 항목이 「변경이 저장되지 않는다」였는데, 여기서는 반대로 **저장되면 안 되는 것이 저장된다.** 세션의 수명을 「작업 하나」로 적어 둔 이유가 여기서 실물로 드러나고, 답은 **접속(요청)마다 `openSession()`** 이다 → [[thread]] · [[transaction]] · [[connection-lifetime-mismatch]]
- **하루 뒤 Day62 가 그 답을 실행한다 — 그리고 이 프레임워크의 물건을 세 번째로 재발명한다** — 「접속마다 세션」을 얻는 방법으로 고른 것이 **팩토리에 프록시를 씌워 [[thread-local]] 에 세션을 담아 두는 것**이다. 그래서 이 표의 셋째 줄이 「앱에 하나」에서 「쓰레드마다 하나」로 옮겨지는데, **여전히 「작업마다」는 아니다** — `close()` 가 없어 세션이 접속 끝까지 산다. 그리고 이 형태가 프레임워크에 이미 있다 — Spring 연동의 `SqlSessionTemplate` 이 **동적 프록시로 `SqlSession` 을 대리하면서 실제 세션을 현재 트랜잭션에 묶어 두는** 물건이라, Day61 의 도구(`Proxy.newProxyInstance`)와 Day62 의 도구(쓰레드에 묶기)를 합친 것이 그것이다. `@Param` · 매퍼 인터페이스에 이어 **세 번째로 같은 것을 손으로 지은 자리**이고, 여기서도 손해가 아니다 — 「왜 세션을 요청에 묶어 주는 클래스가 따로 있나」의 답이 손에 남는다 → [[proxy-pattern]] · [[dynamic-proxy]] · [[sql-session]]
- **위 수명 표에 네 번째 칸이 있다 — 쓰레드 안전성이고, Day62 의 판단이 그것에 기대고 있다** — 표는 개수와 수명만 적었는데 실제로 셋을 가르는 것이 하나 더 있다: `SqlSessionFactory` 는 **여러 쓰레드가 함께 써도 되고** `SqlSession` 은 **안 된다.** 그래서 Day62 가 대리자를 씌운 자리가 팩토리인 것이 우연이 아니다 — 세션에는 씌울 수 없다(쓰레드마다 달라야 하는 것 자체다). **「앱에 하나」와 「쓰레드가 함께 써도 된다」가 같은 칸에 있다는 것**이 그 회차의 설계가 성립하는 근거인데, 필기는 그 이유를 적지 않는다 → [[thread]] · [[thread-local]]
- **`#{ok}` 가 통하는 것은 파라미터가 하나일 때뿐이다** — 필기의 설명은 맞지만 조건이 빠졌다. 값이 둘 이상이면 이름이 없는 것이 아니라 **이름이 필요해진다** — `#{param1}`·`#{arg0}` 이나 `@Param("no")` 이나 `Map` 이다. 「임의로 써도 된다」로 외우면 조건이 두 개인 조회를 만드는 순간 `There is no getter for property named 'ok'` 를 만난다. 그리고 이 회차의 `delete` 도 같은 `#{ok}` 를 쓰므로 **같은 이름이 두 매퍼에서 각각 다른 컬럼에 붙어 있다** — 뜻 없는 이름이라 읽는 사람에게 아무 도움이 안 되는 자리다.
- **`selectOne` 이 두 행을 받으면 예외다** — 필기의 「리턴된 객체는 반드시 1개여야 한다」가 맞고, 그 실체는 `TooManyResultsException` 이다. 0행이면 예외가 아니라 **`null`** 이므로 두 실패가 다른 모양으로 온다 — 「없음」은 조용하고 「여럿」은 터진다. `where` 조건이 [[primary-key]] 나 [[unique-key]] 가 아닌 컬럼이면 이 메서드를 쓸 수 없다 → [[sql-null]]
- **`insert` 의 반환값은 자동 생성 키가 아니다** — 변경된 행 수다. 키를 되받으려면 `<insert useGeneratedKeys="true" keyProperty="no">` 를 적어야 하고 Day59 에는 없다. **Day57 §2.2 의 등록 화면이 `insert` 로 받은 번호로 팀원을 넣었으므로**, 그 화면을 이 매퍼로 옮기면 `project.getNo()` 가 `0` 인 채로 다음 문장에 들어가 외래키에 걸린다 — [[sql-session]] 노트가 Day58 의 세션에 대해 적은 것과 **같은 구멍이 프레임워크에서도 설정을 적지 않으면 그대로 있다** → [[generated-keys]] · [[foreign-key]]
- **`type="POOLED"` 는 커넥션 풀이다 — 필기가 값만 쓰고 설명하지 않았다** — `UNPOOLED` 는 요청마다 새 연결, `POOLED` 는 만들어 둔 연결을 빌려 주고 되받고, `JNDI` 는 컨테이너가 관리하는 것을 찾아 쓴다. Day55~58 이 `Connection con` 하나를 필드로 들고 모든 화면이 공유하던 자리가 여기서 풀로 바뀌며, **[[transaction]] 노트가 「연결에 남은 설정이 남의 요청으로 넘어간다」고 경고한 구조가 실제로 도입된 것**이다. 다만 MyBatis 의 풀은 연결을 반납할 때 미확정 트랜잭션을 롤백하고 설정을 되돌려 주므로 — Day57 이 `finally` 에서 손으로 하던 `setAutoCommit(true)` 를 프레임워크가 맡는다 → [[connection-lifetime-mismatch]] · [[connection-pool-sizing-formula]]
- **`transactionManager type="JDBC"` 는 「커밋을 `Connection` 에 맡긴다」는 선택이다** — 다른 값 `MANAGED` 는 컨테이너에 맡기고, 그때는 **세션의 `commit()` 이 아무 일도 하지 않는다.** 즉 같은 자바 코드가 설정 한 줄에 따라 커밋을 하기도 안 하기도 하며, 그것이 이 층에서 「트랜잭션이 왜 안 걸리나」의 첫 확인 지점이다 → [[transaction]]
- **`<mappers>` 에 등록하지 않은 매퍼 파일은 없는 것과 같다** — XML 을 만들고 문장을 다 써도 `<mapper resource="…"/>` 한 줄이 없으면 `BindingException` 이고, 메시지는 「그런 문장이 없다」라서 **파일을 만들었다는 사실이 원인 추적을 방해한다.** 그리고 `resource=` 의 경로는 클래스패스 기준이라 소스 디렉토리에 둔 파일이 빌드 결과에 복사되지 않으면 같은 오류가 난다 → [[classpath]] · [[build]]
- **매퍼 XML 에서는 `<` 를 그대로 쓸 수 없다** — `where no < 10` 이 XML 파싱 오류다. `&lt;` 나 `<![CDATA[ … ]]>` 가 필요하다. **SQL 을 자바 문자열에서 XML 로 옮기면서 새로 생긴 제약**이고, Day59 의 문장들에 부등호가 없어서 이 벽에 닿지 않았다 → [[xml]] · [[sql-operator]]
- **MyBatis 의 `SqlSession` ≠ Day58 이 만든 세션** — 이름과 메서드 구성을 Day58 이 그대로 베껴 왔지만 셋이 다르다: ① 첫 인수가 SQL 이 아니라 id 이고, ② `commit`·`rollback`·`close` 가 있고, ③ 연결을 스스로 얻는다(풀에서). 상세는 그쪽 노트가 갖는다 → [[sql-session]]
- **SQL 이 밖으로 나간 대가는 「한 자리에서 읽히지 않는다」다** — Day58 의 세션은 SQL 을 인수로 받았으므로 **호출부만 읽으면 무슨 문장인지 알았다.** 매퍼로 옮기면 호출부에는 `"UserDao.update"` 만 남고 문장을 보려면 XML 을 열어야 하며, 그 사이의 대응이 문자열이다. **얻은 것(분리)과 잃은 것(한눈에 읽힘)이 같은 사건의 앞뒤**이고, 매퍼 인터페이스(`@Mapper`)가 그 문자열을 메서드 이름으로 바꿔 잃은 것의 일부를 되찾는 다음 걸음이다 → [[coupling]] · [[cohesion]]
- **필기는 「Mybatis」로 쓴다** — 공식 표기는 `MyBatis` 다(가운데 `B` 가 대문자). 뜻은 통하지만 문서·검색에서 갈리고, `parameterType="user"` 처럼 **대소문자가 실제로 의미를 갖는 자리가 이 프레임워크에 있어서** 표기를 흘려보는 습관이 그쪽으로 이어진다.
- **필기의 XML 조각에 오타가 하나 더 있다** — `<insert id="slq2" …>` 이고, 자바는 `"aaa.sql2"` 를 부른다(위 id 항목의 ①). 그리고 「SqlSession 객체 생성」 절의 코드 바로 위에 `ㅌ` 한 글자가 남아 있다 — 편집 중에 들어간 것으로 보인다.

## 함께 보는 개념

- [[sql-session]] — 이 프레임워크의 세션을 하루 전에 손으로 만든 자리
- [[result-map]] · [[dynamic-sql]] · [[type-alias]] — 하루 뒤 매퍼와 설정에 더해지는 셋
- [[persistence-framework]] — 이것이 SQL Mapper 쪽이라는 분류
- [[dao-pattern]] — 이 층이 놓이면 얇아지는 클래스
- [[dynamic-proxy]] — 매퍼 인터페이스를 성립시키는 문법
- [[thread]] — 세션을 공유하면 깨지는 자리
- [[thread-local]] · [[proxy-pattern]] — 세션을 쓰레드에 묶는 방법
- [[caching]] — 세션에 딸린 1차 캐시
- [[xml]] — 설정과 문장을 담는 형식
- [[prepared-statement]] — `#{}` 가 실제로 내려가는 자리
- [[sql-injection]] — `${}` 를 쓰면 되돌아가는 위험
- [[transaction]] — `openSession(false)` 가 여는 것
- [[jdbc]] — 이 층 밑에 그대로 있는 API
- [[result-set]] · [[dql]] · [[dml]] · [[crud]] — 다섯 메서드가 맡는 문장들
- [[generated-keys]] — 설정 없이는 여전히 못 되받는 값
- [[class-loading]] — `resultType` 문자열이 클래스가 되는 통로
- [[reflective-instantiation]] · [[reflective-field-access]] · [[reflective-invocation]] — 매핑을 실제로 수행하는 셋
- [[sql-null]] — 이름이 어긋났을 때 조용히 남는 값
- [[connection-lifetime-mismatch]] · [[connection-pool-sizing-formula]] — `type="POOLED"` 가 여는 축
- [[coupling]] · [[cohesion]] · [[encapsulation]] — 무엇이 분리되고 무엇이 흩어졌나
- [[classpath]] · [[build]] — 설정과 매퍼 파일이 읽히는 조건

## 출처

- [[2024-08-20-Day59]] — 「MyBatis」 절 전체가 이 개념이다. `mybatis-config.xml` 전문(`<properties>`·`<environments>`·`<transactionManager type="JDBC">`·`<dataSource type="POOLED">`·`<mappers>`)을 실어 설정 층을 세우고, `SqlSessionFactoryBuilder` → `SqlSessionFactory` → `openSession(false)` 사다리 세 줄로 세션을 얻고, `selectList`·`insert`·`selectOne`·`update`·`delete` 다섯 절에서 **자바 한 줄과 매퍼 XML 한 조각을 짝지어** 실었다. 「java에서는 XML에 태그를 넘기면서 sqlSession의 메서드를 호출한다」가 다섯 절에 반복되고, 「Dao 기능분리」 절이 「Mybatis를 사용해서 JDBC API의 역할을 이전하고 소스에서는 자바코드만 작성한다」로 이 층의 목적을 적었다. `user_id as no` 로 컬럼 라벨을 프로퍼티 이름에 맞추는 것, `pwd=sha1(#{password})` 로 컬럼명과 프로퍼티명이 갈리는 것, 파라미터가 하나면 `#{ok}` 처럼 이름을 아무렇게나 써도 되는 것, `selectOne` 의 결과가 반드시 하나여야 한다는 것이 이 회차에서 실제로 확인한 규칙들이다. 다만 **`#{}` 를 「getter 를 불러 sql구문을 완성한다」로 설명해 `${}` 의 동작으로 적었고**(실제로는 `?` + `PreparedStatement`), `openSession(false)` 로 autocommit 을 껐는데 **`commit()` 이 어디에도 없어 변경이 저장되지 않으며**, 문장 id 가 `slq2`·`sql3.findBy` 두 곳에서 어긋나고 네임스페이스가 `aaa`·`sql3`·`UserDao` 로 갈리며, `parameterType="user"` 는 등록되지 않은 별칭이고, `<mapper namespace="…">` 루트 태그·`useGeneratedKeys`·`<resultMap>`·`${}` 는 나오지 않는다. 「SqlSession 객체 생성」 절 코드 위에 `ㅌ` 한 글자가 남아 있다
- [[2024-08-21-Day60]] — 하루 뒤. **Day59 가 열어 둔 구멍 셋을 각각 메우는 회차**다. 「resultMap」 절이 컬럼과 프로퍼티의 대응을 문장 밖으로 빼내고 `<association javaType>`·`<collection ofType>` 으로 조인 결과를 객체 안의 객체·목록으로 접는 형태를 보이며(→ [[result-map]]), 「forEach 사용하기」 절이 `<foreach collection item separator>` 로 값의 개수가 정해지지 않은 문장을 만드는 법을 보이고(→ [[dynamic-sql]]), 「typeAliases」 절이 `<typeAlias type alias>`·`<package name>` 으로 **전날 `parameterType="user"` 가 실패한 이유**를 닫는다(→ [[type-alias]]). 그래서 이 회차를 지나면 이 프레임워크의 네 층 중 설정과 문장 두 층이 채워지고, **문자열 이름들이 걸리는 시점이 갈린다는 것**(별칭·`<resultMap>` id 는 시작할 때, 문장 id·프로퍼티 이름은 부를 때)도 여기서 보인다. 다만 세 절 모두 조각만 실려 있어 `<select resultMap="…">` 로 매핑을 문장에 붙이는 줄·`insert into` 의 컬럼 목록·감싸는 `<typeAliases>` 태그가 전부 빠져 있고, `<foreach>` 가 만드는 문장을 「vaule(1,11,12...)와 같이」로 잘못 읽었다. 같은 노트 후반의 애노테이션 절들이 이 설정을 XML 없이 적는 다른 길(`@Alias`·매퍼 인터페이스)의 문법인데 두 주제가 이어지지 않는다 → [[annotation]] · [[reflective-annotation-access]]
- [[2024-08-22-Day61]] — 이틀 더 뒤. 이 프레임워크를 **직접 확장해 보는 회차**다. DAO 를 인터페이스로 두고 [[dynamic-proxy]] 로 구현체를 만들어 `sqlSession.selectList`·`insert`·`selectOne` 을 **메서드 시그니처로 골라 부르게** 하는데, 그것이 MyBatis 자신의 매퍼 인터페이스와 같은 물건이다 — 이 노트가 「매퍼 인터페이스가 문자열 id 를 메서드 이름으로 바꿔 잃은 것의 일부를 되찾는 다음 걸음」이라 적어 둔 그 걸음을 **프레임워크 기능이 아니라 손으로** 밟았다. 매개변수가 둘 이상일 때 `#{property}` 가 이름으로 값을 찾는다는 것을 짚고(「mapper에 사용할 property와 args[n]과 다르기 때문에 Map을 넘긴다 하더라도 get하지 못한다」) **`@Param` 애노테이션을 직접 선언해** `void updateViewCount(@Param("no") int boardNo, @Param("count") int count)` 에 붙이는데, 이것 역시 MyBatis 에 이미 있는 애노테이션과 이름·뜻이 같다. 다만 문장 id 규약을 `"sql.method"` 자리표시자로 비워 두어 **메서드 이름이 곧 문장 id 가 되는 규칙**이 코드에 없고, `anno.value()` 를 꺼내지 않아 Map 의 키가 이름이 되지 않으며(→ [[dynamic-proxy]]), `insert`·`update`·`delete` 를 반환 타입만으로 갈라 셋을 구별하지 못한다. 같은 노트 후반의 멀티쓰레드 서버와 합치면 **모든 접속이 `SqlSession` 하나를 공유하는 구조**가 되어 이 노트의 수명 표(「세션은 작업마다 하나」)가 깨지는데, 두 절이 이어지지 않아 필기에는 그 충돌이 없다
- [[2024-08-23-Day62]] — 하루 더 뒤. **깨진 수명 표를 되돌리는 회차**다. 전날의 공유 세션 문제를 「하나의 SqlSession을 생성하여 하나의 캐시를 공유한다」·「하나의 클라이언트에서 커밋을 하면 전체 캐시가 데이터베이스에 업데이트된다」로 적고, `SqlSessionFactory` 에 GoF 프록시(`SqlSessionFactoryProxy`)를 씌워 `openSession(boolean)` 이 [[thread-local]] 에 담아 둔 세션을 돌려주게 한다 — 이 표의 「세션은 작업마다 하나」가 「앱에 하나」에서 **「쓰레드마다 하나」**로 한 칸 옮겨진다. 프록시를 세션이 아니라 팩토리에 씌운 것은 **팩토리가 앱에 하나이면서 쓰레드가 함께 써도 되는 유일한 칸**이기 때문인데 필기는 그 이유를 적지 않고, 「SqlSessionFactory를 만들어서」라는 표현도 정확하지 않다(팩토리는 Day59 부터 있었고 새로 만든 것은 그 앞의 대리자다). 그리고 이 형태가 프레임워크에 이미 있다 — Spring 연동의 `SqlSessionTemplate` 이 같은 일을 동적 프록시로 하므로, `@Param`·매퍼 인터페이스에 이어 **세 번째 재발명**이다. 남은 것은 `close()` 다 — 세션을 닫지 않아 `<dataSource type="POOLED">` 에서 빌린 연결이 반납되지 않고(기본 활성 상한 10), 1차 캐시와 트랜잭션 스냅샷이 접속 전체에 걸려 **남의 변경이 보이지 않는** 반대쪽 문제가 생긴다. `openSession` 의 오버로드가 여덟 개인데 하나만 가로챈 것도 다루지 않는다 → [[sql-session]] · [[transaction]] · [[caching]]
