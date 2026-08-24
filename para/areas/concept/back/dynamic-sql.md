---
type: concept
id: dynamic-sql
title: 동적 SQL (foreach)
aliases:
  - 동적 SQL
  - dynamic sql
  - foreach 태그
  - mybatis foreach
up:
  - 2024-08-21-Day60
tags:
  - database
  - SQL
  - 프레임워크
  - 매퍼
---

# 동적 SQL (foreach)

**문장을 통째로 적어 두는 대신, 넘어온 값에 따라 문장의 일부를 XML 태그로 만들어 내는 것.** Day60 이 그 문법 중 하나(`<foreach>`)를 배운다 — 「mybatis xml에서 반복문을 제어하기 위해 사용하는 문법이다」. **반복되는 것은 실행이 아니라 문장 조각**이고, 그 차이가 이 태그의 전부다 → [[mybatis]] · [[parameterization]]

## 정의

```xml
<foreach collection="members" item="member" separator=",">
    (#{projectNo}, #{member.no})
</foreach>
```

속성 넷이 각각 다른 것을 정한다.

| 속성 | 정하는 것 | 이 예제에서 |
|---|---|---|
| `collection` | **어디서** 반복할 값을 찾을지 (파라미터 안의 이름) | `members` |
| `item` | 한 바퀴의 값에 붙일 **이름** | `member` |
| `separator` | 조각 사이에 끼울 것 | `,` |
| (`open`·`close`·`index`) | 앞뒤로 감쌀 것 · 몇 번째인지 | 쓰지 않았다 |

필기가 걸음을 세 줄로 적었다 — 「java에서 members collection객체를 받는다」·「foreach에서 사용할 변수명을 item에 설정한다」·「해당 결과로 vaule(1,11,12...)와 같이 쿼리문에 전송된다」. 마지막 줄이 결과를 잘못 읽었다(아래 「경계와 오해」 첫 항목).

### 실제로 만들어지는 문장

몸통이 `(#{projectNo}, #{member.no})` 이므로 **한 바퀴가 괄호 한 쌍**이고, `separator=","` 가 그 괄호들 사이에 쉼표를 넣는다. 팀원이 셋이면 문장의 그 자리는 이렇게 된다.

```sql
insert into myapp_project_members (project_id, user_id)
values (?, ?), (?, ?), (?, ?)
```

**`values` 뒤에 행이 셋 붙은 하나의 문장**이다. 물음표가 여섯 개 생기고 값도 여섯 개가 순서대로 바인딩된다 — `#{}` 이므로 문자열로 이어 붙이는 것이 아니다 → [[prepared-statement]]

### 같은 일을 자바 for 문으로 했던 자리

여드레 전 Day55 의 `insertMembers` 가 정확히 이 일을 자바 쪽 반복으로 했다.

```java
public boolean insertMembers(int projectNo, List<User> members) throws Exception {
  try (Statement stmt = con.createStatement()) {
    for (User user : members) {
      stmt.executeUpdate(String.format(
          "insert into myapp_project_members('user_id','project_id')" +
              "values (%d,%d)",
          projectNo,
          user.getNo()
      ));
    }
    return true;
  }
}
```

**두 반복의 결과물이 다르다.**

| | Day55 의 `for` | Day60 의 `<foreach>` |
|---|---|---|
| 반복하는 것 | **문장 실행** | **문장 조각 생성** |
| 서버로 가는 문장 | 팀원 수만큼 (N번) | **1번** |
| 왕복 | N번 | 1번 |
| 하나가 실패하면 | 앞의 것들은 이미 들어갔다 | 문장 하나이므로 **전부 안 들어간다** |

**「같은 결과를 얻는 두 방법」이 아니다** — 뒤쪽은 왕복을 줄이는 것에 더해 **부분 실패라는 상태를 없앤다.** Day57 이 커밋 경계를 화면에 두어 손으로 묶었던 그 덩어리 중 하나가, 여기서는 **문장 하나가 되어 저절로** 묶인다 → [[transaction]] · [[dao-pattern]]

## 사용 예시

Day60 이 실은 조각은 팀원을 넣는 자리다. 문장 전체로 쓰면 이렇게 선다.

```xml
<insert id="insertMembers" parameterType="project">
  insert into myapp_project_members (project_id, user_id)
  values
  <foreach collection="members" item="member" separator=",">
    (#{projectNo}, #{member.no})
  </foreach>
</insert>
```

**`#{projectNo}` 와 `#{member.no}` 가 같은 괄호 안에 있으면서 오는 곳이 다르다.** 앞은 반복 밖의 값이라 **바퀴마다 같은 값**이 들어가고, 뒤는 `item` 이 가리키는 그 바퀴의 객체에서 `getNo()` 를 불러 꺼낸다. **점이 붙은 `#{member.no}` 는 프로퍼티를 따라 들어가라는 표기**이고, 그것도 Day59·Day60 의 리플렉션이 하는 일이다 → [[reflective-invocation]]

다른 쪽 용도는 조회 조건이다. 「번호 목록에 든 것들을 달라」는 [[prepared-statement]] 의 `?` 로는 쓸 수 없다 — 개수가 정해지지 않으므로.

```xml
<select id="findByNos" resultType="user">
  select * from myapp_users
  where user_id in
  <foreach collection="list" item="no" open="(" close=")" separator=",">
    #{no}
  </foreach>
</select>
```

**`in (?, ?, ?)` 의 물음표 개수를 문자열 조립으로 세던 일이 이 태그로 옮겨진다.** Day56~58 에서 `?` 자리를 사람이 세어 `setInt(1, …)`·`setInt(2, …)` 를 적던 그 노동이 여기서 사라진다 → [[sql-operator]]

## 왜 중요한가

**「문장이 미리 정해져 있다」는 전제가 깨진다.** 매퍼 XML 로 SQL 을 옮기면서 얻은 것은 「문장이 한 자리에 있다」였는데, 값의 개수나 조건의 유무에 따라 문장이 달라져야 하는 경우에는 그 자리에 **문장 하나를 적을 수가 없다.** [[dao-pattern]] 노트가 「조회 조건이 화면마다 다르면 `findByNo`·`findByName`·`findByNameAndDate` … 로 메서드가 불어난다」고 적어 둔 그 자리에 대한 답이 이 문법이고, Day60 은 그중 반복 쪽 하나를 가져온다 → [[mybatis]]

**그리고 왕복 횟수가 코드의 모양에서 문장의 모양으로 옮겨간다.** 자바 for 문 안의 `executeUpdate` 는 **읽어도 몇 번 나가는지 보이지 않는다**(목록 크기가 실행 중에 정해진다). `<foreach>` 로 쓰면 문장이 하나라는 것이 매퍼를 읽는 것으로 확인된다 — **성능에 대한 사실이 코드가 아니라 선언에 적히는 것**이 이 층의 성질이다 → [[database-index]]

**대신 문장을 사람이 다 읽을 수 없게 된다.** 매퍼 파일에 있는 것은 이제 SQL 이 아니라 **SQL 을 만드는 것**이고, 실제로 나간 문장을 보려면 로그를 켜야 한다. [[persistence-framework]] 가 OR Mapper 쪽의 대가로 적어 둔 「생성된 SQL 이 눈에 안 보인다」가 **SQL Mapper 에서도 이 태그를 쓰는 만큼 생긴다** — 갈리는 축이 프레임워크 종류가 아니라 **문장을 사람이 적었는가**였던 것이다.

## 경계와 오해

- **필기가 만들어지는 문장을 잘못 읽었다 — 쉼표로 이어지는 것은 값이 아니라 괄호다** — 「예제의 결과 user_id가 ","로 구분되어 담긴다」·「해당 결과로 vaule(1,11,12...)와 같이 쿼리문에 전송된다」는 **한 괄호 안에 프로젝트 번호와 회원 번호들이 나란히 들어간다**는 뜻인데, `separator` 가 끼어드는 자리는 **몸통 사이**이고 몸통 자체가 `(#{projectNo}, #{member.no})` 라는 괄호 한 쌍이다. 실제 결과는 `(1,11),(1,12),(1,13)` 이다. 이 오해가 실제로 무엇을 깨는가 — **필기대로 믿고 `values` 뒤를 `(#{projectNo}, <foreach …>#{member.no}</foreach>)` 처럼 괄호를 밖에 두면** 값 네 개가 컬럼 두 개짜리 한 행에 들어가 `Column count doesn't match value count at row 1` 이 되고, 「foreach 가 잘못됐나」를 보게 되지만 틀린 것은 **괄호의 위치**다. 즉 「무엇이 반복되는가」를 값으로 읽으면 태그를 놓는 자리가 어긋난다 → [[dml]]
- **`collection="members"` 라는 이름이 자바 변수 이름과 같아서 통하는 것이 아니다** — 이 이름은 **넘긴 파라미터 안에서 찾는 이름**이다. `project` 객체를 넘겼고 그것에 `getMembers()` 가 있으면 `members` 가 맞고, `Map` 을 넘겼으면 그 키여야 한다. 그런데 **`List` 를 그대로 넘겼으면 이름이 `list`** 이고(배열이면 `array`), 그때 `collection="members"` 는 `Parameter 'members' not found. Available parameters are [collection, list]` 로 실패한다. Day55 의 `insertMembers(int projectNo, List<User> members)` 처럼 **인수가 둘인 메서드를 그대로 옮기면 이름이 `param1`·`param2`(또는 `arg0`·`arg1`)** 가 되어 `members` 도 `list` 도 아니다 — 이름을 살리려면 `@Param("members")` 를 붙이거나 객체·`Map` 으로 묶어 넘겨야 한다. **필기의 「java에서 members collection객체를 받는다」가 그 조건을 적지 않았고**, 이것이 이 태그에서 가장 자주 나는 오류다. 파라미터 이름이 `arg0` 으로 지워지는 것은 [[reflective-invocation]] 노트가 적어 둔 그 소거와 같은 원인이다
- **`<foreach>` ≠ 자바의 향상된 for 문** — 이름과 모양이 같아 같은 것으로 읽히는데, 반복하는 주체와 결과물이 다르다. 자바의 것은 **JVM 이 몸통을 N번 실행**하고, 이것은 **MyBatis 가 문자열 조각을 N개 이어 붙인 뒤 그 문장을 한 번 실행**한다. 그래서 몸통 안에 「이전 바퀴의 결과를 쓰는」 코드를 넣을 수 없고, `break` 도 조건 분기도 없다 — 분기가 필요하면 `<if>` 를 그 안에 겹쳐 넣는 별개 문법이다 → [[for-loop]]
- **빈 목록이면 문장이 깨진다** — 팀원을 하나도 고르지 않으면 `<foreach>` 가 아무것도 만들지 않아 `insert into … values` 로 끝나는 문장이 서버로 가고 문법 오류가 된다. `in ()` 쪽도 같다. **자바 for 문은 0번 돌면 아무 일도 안 일어나는 것이 정상 동작이었는데**, 문장 조각을 만드는 반복은 **0번이 곧 잘못된 문장**이다 — 「반복이 0번일 때」의 뜻이 뒤집히는 자리이고, 그래서 부르는 쪽이 목록이 비었는지 먼저 봐야 한다(또는 `<if test="members != null and members.size() > 0">` 로 감싼다) → [[sql-null]]
- **목록이 크면 문장 하나가 감당 못 하게 커진다** — 왕복을 1번으로 줄인 대가다. 값이 수만 개면 문장 길이가 MySQL 의 `max_allowed_packet` 을 넘고, 넘지 않아도 `?` 개수가 매번 달라져 **[[prepared-statement]] 의 재사용이 안 된다**(개수가 달라지면 다른 문장이다). 그래서 실무에서는 1000건씩 잘라 여러 번 보내는 형태가 되고, **그러면 다시 부분 실패가 생기므로 트랜잭션 경계를 밖에 둬야 한다** — 위 표의 「전부 안 들어간다」가 조건부라는 것 → [[transaction]]
- **`#{}` 는 여기서도 바인딩이고 `${}` 는 아니다** — 반복으로 만들어지는 것은 **문장의 구조**이고 값은 여전히 물음표로 간다. 그런데 `<foreach>` 는 「정렬 컬럼 목록」처럼 값이 아닌 것을 반복하는 데도 쓸 수 있고, 그때는 `${}` 여야 한다 — **거기서 인젝션이 열린다.** Day59 노트가 「위험이 `${}` 를 쓰는 자리에 모인다」고 적은 그 자리가 동적 SQL 을 쓰기 시작하면 **늘어난다** → [[sql-injection]]
- **Day55 의 컬럼 순서 문제를 이 조각으로는 검증할 수 없다** — Day60 의 몸통은 `(#{projectNo}, #{member.no})` 로 **프로젝트 번호가 먼저**인데, `insert into` 의 컬럼 목록이 이 절에 없다. Day55 의 자바 판은 컬럼을 `('user_id','project_id')` 로 적고 값을 `(projectNo, user.getNo())` 순서로 넘겨 **두 값이 뒤바뀌어 있었다**([[foreign-key]] 노트의 항목). 옮기면서 그 순서가 맞춰졌는지 아닌지는 **문장의 앞부분이 없으므로 판정되지 않는다** — 그리고 두 컬럼이 둘 다 정수라 **뒤바뀌어도 타입 오류가 나지 않는다**(외래키가 걸려 있어 없는 번호일 때만 걸린다) → [[foreign-key]]
- **`<foreach>` 는 동적 SQL 의 하나일 뿐이다 — 예측된 나머지는 아직 안 왔다** — [[dao-pattern]] 노트가 메서드 폭증의 답으로 `<if>`·`<where>` 를 적었는데 Day60 이 가져온 것은 반복 쪽 하나다. 조건 쪽(`<if>`·`<choose>`·`<where>`·`<set>`·`<trim>`)은 이 회차에 없고, 그래서 **「조회 조건이 화면마다 다르다」는 문제는 여기서 아직 안 풀린다** — 풀린 것은 「값의 개수가 정해지지 않는다」쪽이다.
- **`open`·`close`·`index` 를 안 써서 `in (…)` 형태가 나오지 않았다** — 필기의 예제는 몸통에 괄호를 직접 적는 방식이라 `open="("`·`close=")"` 가 필요 없었다. 그래서 이 태그의 **가장 흔한 용도**(`where id in (…)`)가 노트에 없고, `index` 로 몇 번째인지 받는 것도 나오지 않는다.

## 함께 보는 개념

- [[mybatis]] — 이 태그가 사는 층
- [[result-map]] — 같은 회차에서 결과를 조립하는 쪽
- [[type-alias]] — `parameterType="project"` 가 통하기 위한 등록
- [[prepared-statement]] — `#{}` 가 만드는 물음표
- [[sql-injection]] — `${}` 로 반복할 때 열리는 위험
- [[transaction]] — 문장이 하나가 되면서 저절로 묶이는 것
- [[dao-pattern]] — 메서드 폭증의 답으로 예고된 자리
- [[for-loop]] — 이름이 같지만 반복 주체가 다른 문법
- [[reflective-invocation]] — `#{member.no}` 가 getter 에 닿는 통로
- [[dml]] · [[sql-operator]] — 이 태그가 만드는 문장들
- [[foreign-key]] — 값의 순서가 뒤바뀌어도 조용한 자리
- [[parameterization]] — 「달라지는 것을 밖에서 받는다」의 일반형
- [[persistence-framework]] — 생성된 문장이 안 보이게 되는 대가
- [[xml]] — 이 태그가 사는 형식

## 출처

- [[2024-08-21-Day60]] — 「forEach 사용하기」 절이 이 개념이다. 「mybatis xml에서 반복문을 제어하기 위해 사용하는 문법이다」로 정의하고 `<foreach collection="members" item="member" separator=",">(#{projectNo}, #{member.no})</foreach>` 한 조각을 실었으며, 「java에서 members collection객체를 받는다」·「foreach에서 사용할 변수명을 item에 설정한다」로 두 속성의 역할을 적었다. **여드레 전 Day55 가 자바 `for` 안에서 `executeUpdate` 를 팀원 수만큼 부르던 `insertMembers` 가 이 태그로는 문장 하나가 된다** — 왕복이 N번에서 1번으로 줄고 부분 실패가 사라지는 자리인데 필기는 그 대비를 적지 않았다. 그리고 만들어지는 문장을 「user_id가 ","로 구분되어 담긴다」·「vaule(1,11,12...)와 같이」로 적어 **쉼표로 이어지는 것이 값이라고 읽었다** — 실제로는 `(1,11),(1,12),(1,13)` 처럼 괄호 단위로 이어진다. `collection` 의 이름이 파라미터 안에서 찾는 이름이라는 조건(`List` 를 그대로 넘기면 `list`), 빈 목록이면 문장이 깨지는 것, `open`·`close` 로 `in (…)` 을 만드는 흔한 용도, 조건 쪽 문법(`<if>`·`<where>`)은 이 회차에 없다. 문장의 앞부분(`insert into … 컬럼 목록`)이 실려 있지 않아 Day55 에서 컬럼과 값의 순서가 뒤바뀌어 있던 것이 고쳐졌는지는 확인할 수 없다
