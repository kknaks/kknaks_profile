---
type: concept
id: result-map
title: 결과 매핑 (resultMap)
aliases:
  - resultMap
  - result map
  - 결과 매핑
  - 리설트맵
  - association 옵션
  - collection 옵션
up:
  - 2024-08-21-Day60
tags:
  - database
  - java
  - 매핑
  - 프레임워크
---

# 결과 매핑 (resultMap)

**컬럼과 자바 프로퍼티의 대응을 문장 밖에 따로 선언해 두고, 조인 결과를 「객체 안의 객체」·「객체 안의 목록」으로 조립하는 것.** Day59 는 대응을 맞추는 방법이 하나였다 — `user_id as no` 처럼 **SQL 을 고치는 것**. Day60 은 그 대응을 `<resultMap>` 이라는 **별도 선언**으로 빼내고, 그 순간 되는 일이 하나 늘어난다: **한 문장의 결과가 객체 하나가 아니어도 된다** → [[mybatis]] · [[result-set]]

## 정의

필기의 세 줄이 이 태그가 푸는 문제 셋을 나눠 적었다 — 「데이터베이스의 결과 셋을 Java 객체에 매핑할 때 사용한다」·「sql의 컬럼과 java 객체의 필드값을 매핑 할 수 있다」·「sql의 join 결과를 java에 리턴 할 수 있다」. 뒤의 두 줄이 서로 다른 일이다.

| 태그 | 무엇을 대응시키나 | 없으면 |
|---|---|---|
| `<id property column>` | 컬럼 하나 ↔ 프로퍼티 하나. **그리고 「이 행이 어느 객체인가」의 열쇠** | 아래 「경계와 오해」 첫 항목 |
| `<result property column>` | 컬럼 하나 ↔ 프로퍼티 하나 | 그 프로퍼티가 `null`(또는 `0`)로 남는다 |
| `<association property javaType>` | 컬럼 몇 개 ↔ **프로퍼티 하나가 가리키는 객체** | 조인해 온 컬럼이 갈 곳이 없다 |
| `<collection property ofType>` | 여러 **행** ↔ **프로퍼티 하나가 담는 목록** | 행 수만큼 부모 객체가 생긴다 |

앞의 둘은 「이름이 다른 것을 맞추는」 일이고, 뒤의 둘은 **결과의 모양을 바꾸는** 일이다. 표의 마지막 줄이 이 개념의 값 전부다 — SQL 의 결과는 언제나 **네모난 표**인데 자바 쪽에서 받고 싶은 것은 **나무**다 → [[sql-join]] · [[db-normalization]]

### `<id>` 와 `<result>` 가 갈리는 이유 — 「같은 행인가」의 판정

필기는 둘을 나란히 쓰기만 하고 차이를 적지 않았다. **`<id>` 는 「이 행들이 같은 객체를 말하는가」를 판정하는 컬럼**이다.

`<collection>` 이 붙은 조인은 한 프로젝트에 팀원이 셋이면 **결과가 세 행**으로 온다.

```text
project_id  title      user_id  name
1           웹서비스    11       홍길동
1           웹서비스    12       임꺽정
1           웹서비스    13       유관순
```

MyBatis 는 이 세 행을 훑으면서 **`<id column="project_id">` 값이 같으면 앞에서 만든 프로젝트에 팀원만 더한다.** 그래서 `Project` 하나에 `members` 셋이 담긴다. `<id>` 가 「성능을 위한 표시」처럼 보이는데 실제로는 **접기의 기준**이고, 그것이 없으면 기준이 다른 것으로 대체된다(아래 「경계와 오해」) → [[primary-key]] · [[object-equality]]

### `javaType` 과 `ofType` 이 다른 낱말인 이유

| | 태그 | 타입 속성 | 그 속성이 가리키는 것 |
|---|---|---|---|
| 1:1 | `<association property="writer">` | `javaType="user"` | **프로퍼티의 타입** (`User writer`) |
| 1:N | `<collection property="members">` | `ofType="user"` | **원소의 타입** (`List<User> members`) |

**뒤쪽에서 프로퍼티의 타입은 `List` 라서 적을 것이 없다** — 알아야 하는 것은 그 안에 무엇을 넣을지다. `ofType` 은 「of」가 붙은 만큼 「무엇의 목록인가」를 답하고, 그래서 두 태그에 이름이 다른 속성이 붙는다. [[generics]] 의 타입 인자가 실행 시점에 지워지므로 **`List<User>` 라고 적어 둔 것을 프레임워크가 읽을 수 없고**, 그 지워진 정보를 XML 이 다시 대 주는 것이다 → [[type-erasure]] · [[reflective-field-access]]

## 사용 예시

Day60 이 `<association>` 을 게시글과 작성자로 보였다.

```xml
 <resultMap id="BoardMap" type="board">
    <id property="no" column="board_id" />
    <result property="title" column="title" />
    <result property="content" column="content" />
    <result property="createdDate" column="created_date" />
    <result property="viewCount" column="view_count" />

    <association property="writer" javaType="user">
        <id property="no" column="user_id" />
        <result property="name" column="name" />
    </association>
</resultMap>
```

**`<association>` 안이 바깥과 똑같은 문법이다** — `<id>` 와 `<result>` 가 다시 나온다. 즉 이 태그는 새 문법이 아니라 **같은 매핑을 한 겹 안쪽에 두는 장치**이고, `property="writer"` 가 그 겹을 담을 자리를 지목한다. 안쪽 `<id property="no" column="user_id">` 와 바깥 `<id property="no" column="board_id">` 가 **같은 프로퍼티 이름 `no` 를 쓰면서 부딪히지 않는 것**도 겹이 나뉘어 있기 때문이다 → [[variable-scope]]

그리고 `<collection>` 을 프로젝트와 팀원으로 보였다.

```xml
<resultMap id="ProjectMap" type="project">
  <id column="project_id" property="no"/>
  <result column="title" property="title"/>
  <result column="description" property="description"/>
  <result column="start_date" property="startDate"/>
  <result column="end_date" property="endDate"/>

  <collection property="members" ofType="user">
    <id column="user_id" property="no"/>
    <result column="name" property="name"/>
  </collection>
</resultMap>
```

**이것이 Day55 의 `getMembers` 를 없애는 선언이다.** 그때는 프로젝트를 조회하는 문장과 팀원을 조회하는 문장이 따로 있어서 `projectViewCommand` 가 **DAO 를 두 번** 불렀다(`findBy` + `getMembers`). 여기서는 조인 한 문장의 결과가 `project.getMembers()` 까지 채운 객체로 온다 — **화면이 부르는 횟수가 매핑 선언 하나로 줄어든다** → [[dao-pattern]] · [[crud]]

## 왜 중요한가

**매핑을 SQL 에서 떼어 내면 문장과 대응을 따로 고칠 수 있다.** Day59 의 방식(`user_id as no`)은 대응이 **문장 안에** 있어서, 컬럼 이름을 바꾸거나 자바 필드 이름을 바꾸면 **문장을 고쳐야** 했다. 그리고 같은 테이블을 다섯 문장에서 조회하면 별칭도 다섯 곳에 있다. `<resultMap id="…">` 로 빼내면 문장들이 그 id 를 **함께 가리키므로** 대응이 한 곳에 산다 → [[coupling]]

**그리고 「결과가 표다」는 제약이 자바 쪽에서 사라진다.** [[db-normalization]] 이 한 개념을 두 테이블로 갈라 놓았으므로 조회는 반드시 조인이고, 조인 결과는 **부모 컬럼이 반복되는 납작한 표**다. 그것을 그대로 받으면 `List<Row>` 가 되어 「프로젝트 하나와 팀원 셋」이라는 구조가 자바 쪽에 없다. `<collection>` 은 **행의 반복을 객체의 포함 관계로 되돌린다** — 정규화로 잃은 모양을 조회 시점에 복원하는 자리다 → [[sql-join]] · [[foreign-key]]

**대신 조용히 틀리는 자리가 늘어난다.** 컬럼 이름·프로퍼티 이름·타입 별칭이 전부 문자열이고, 어긋나도 대개 예외가 아니라 **비어 있는 객체**로 온다. Day59 가 문장 id 셋을 어긋나게 쓴 것과 같은 종류의 대가이고, 여기서는 그 어긋남이 **화면에 `null` 이 뜨는 것**으로만 드러난다 → [[sql-null]]

## 경계와 오해

- **`<id>` 를 빼도 대개 접히지만, 빠지는 순간 「두 부모가 하나로 합쳐지는」 경로가 열린다** — MyBatis 는 행을 접을 때 `<id>` 로 지정한 컬럼들로 열쇠를 만들고, **`<id>` 가 하나도 없으면 그 자리에 매핑된 컬럼 전부**를 쓴다. 그래서 제목·설명·날짜가 우연히 똑같은 프로젝트가 둘 있으면 **한 프로젝트에 팀원 여섯 명이 담기고 다른 하나는 결과에서 사라진다.** 행 수가 맞지 않는 것이 예외로 오지 않으므로 「가끔 팀원이 두 배로 나온다」로만 보이고, 원인은 데이터가 겹칠 때만 나타나 재현이 어렵다. **`<id>` 는 성능 힌트가 아니라 동일성 정의**이고, 그 자리에 오는 컬럼은 [[primary-key]] 여야 한다 → [[object-equality]] · [[hash-code]]
- **`resultMap` ≠ `resultType`** — Day59 가 쓴 `resultType` 은 「이 클래스로 만들어라, 대응은 이름이 같은 것끼리 알아서」이고, `resultMap` 은 「대응을 내가 적어 둔 그 선언대로 하라」다. **한 `<select>` 에 둘을 함께 적을 수 없다**(둘 중 하나만). 그래서 「`resultType` 을 쓰다가 조인이 필요해졌다」는 곧 **속성 이름을 바꿔 다는 일**이고, 필기에는 그 `<select resultMap="BoardMap">` 줄이 없다(아래 항목) → [[mybatis]]
- **필기에 `<resultMap>` 을 문장에 붙이는 줄과 조인 SQL 이 없다** — 실린 것은 `<resultMap>` 두 개뿐이고, 그것을 **누가 쓰는지**(`<select id="…" resultMap="BoardMap">`)와 **어떤 조인이 이 컬럼들을 만들어 내는지**가 둘 다 빠져 있다. 결과 화면은 이미지 링크로만 남아 있어 문서에서는 확인할 수 없다. 즉 이 절만 읽으면 **매핑 선언이 어디에 연결되는지 알 수 없다** — `<resultMap>` 은 `<mapper>` 안에 문장들과 나란히 두고 문장이 id 로 가리키는 것이다.
- **`type="board"`·`javaType="user"`·`ofType="user"` 는 별칭이라 등록되어 있어야 한다** — 정규명(`bitcamp.myapp.vo.Board`)이 아니므로 `<typeAliases>` 나 `@Alias` 가 필요하고, 없으면 `Could not resolve type alias 'board'` 로 **매퍼 XML 을 읽는 순간** 실패한다. **그 등록 문법이 같은 회차의 마지막 절(「typeAliases」)에 있는데 필기가 두 절을 잇지 않았다** — 앞 절의 XML 이 뒤 절의 설정을 이미 전제하고 있다 → [[type-alias]]
- **컬럼 라벨이 겹치면 어느 겹으로 갈지 정해지지 않는다** — `<association>` 안의 `<result property="name" column="name"/>` 은 결과 표에 `name` 이라는 라벨이 **하나뿐일 때만** 뜻이 분명하다. 게시글에도 `title` 이, 회원에도 `title` 이 있는 두 테이블을 조인하면 같은 라벨이 둘이 되고, MyBatis 가 보는 것은 **테이블이 아니라 라벨**이라 안쪽과 바깥쪽이 같은 값을 집는다. 답이 둘이다 — SQL 에서 `u.name as writer_name` 처럼 라벨을 갈라 주거나, `<association columnPrefix="u_">` 로 접두사를 걷어내며 읽게 하는 것. **정규화된 테이블끼리는 `name`·`title`·`no` 가 겹치는 것이 오히려 정상**이라 이 벽은 예제를 조금만 키우면 바로 닿는다 → [[dql]]
- **`<collection>` 이 붙은 문장에는 `limit` 을 걸 수 없다** — `limit 10` 이 자르는 것은 **행**이고 접히기 전의 행이므로, 팀원이 셋인 프로젝트 열 개를 요청하면 **프로젝트 세 개와 잘린 목록**이 온다. 「열 개를 달라고 했는데 세 개가 온다」가 버그처럼 보이지만 SQL 은 정확히 시킨 일을 했다. 페이징이 필요하면 부모 키를 먼저 뽑고(`limit` 은 그 문장에) 그 키들로 조인을 다시 하는 두 문장이 된다 — **행과 객체의 개수가 다른 순간부터 「몇 개」라는 말이 두 뜻을 갖는다** → [[dql]] · [[aggregate-function]]
- **`<collection>` 을 만드는 방법이 둘이고 성능이 정반대다** — 필기가 쓴 것은 **중첩 `<collection>`**(조인 한 문장으로 다 가져와 접는다)이다. 다른 형태는 `<collection property="members" select="findMembers" column="project_id"/>` 로 **부모 행마다 문장을 하나 더 보내는** 것이고, 목록 100건을 그리면 문장이 101번 나간다(N+1). [[persistence-framework]] 노트가 「생성된 SQL 이 눈에 안 보인다」의 예로 적어 둔 그 현상이 **SQL Mapper 에서도 설정 한 줄로 생긴다** — 자동 생성만의 문제가 아니다 → [[database-index]]
- **`inner join` 으로 조인하면 팀원 없는 프로젝트가 목록에서 사라진다** — `<collection>` 자체는 「없으면 빈 목록」을 만들 준비가 되어 있는데, 결과 표에 행이 아예 오지 않으면 부모도 없다. `left join` 이어야 하고, 그때 팀원 쪽 컬럼은 전부 `null` 로 온다 — MyBatis 는 **`<id>` 컬럼이 `null` 이면 그 원소를 만들지 않으므로** 빈 목록이 된다. 즉 `<id>` 가 여기서 두 번째 일을 한다. `<id>` 가 없고 `<result>` 만 있으면 **이름이 `null` 인 유령 팀원 하나**가 목록에 들어갈 수 있다 → [[sql-join]] · [[sql-null]]
- **`<association>` 이 있어도 조인하지 않으면 그 프로퍼티는 `null` 이다** — 매핑 선언은 「이 컬럼이 오면 여기 담아라」이지 「가져와라」가 아니다. `select * from myapp_boards` 에 `BoardMap` 을 붙이면 `writer` 가 `null` 이고 예외는 없다. **선언과 조회는 별개**이며, 그 구분이 흐려지는 것이 다음 층(OR Mapper)에서 「필요할 때 알아서 가져오는」 동작을 만나면 더 커진다 → [[persistence-framework]]
- **매핑은 읽는 쪽 한 방향이다 — `<resultMap>` 은 `insert` 에 쓰이지 않는다** — 이름이 `resultMap` 인 그대로 결과 전용이고, 값을 넣는 쪽은 `#{property}` 가 각자 알아서 한다. 그래서 컬럼 이름과 프로퍼티 이름의 대응을 **양쪽에 각각 적어야 하고**, 한쪽만 고치면 조회는 되는데 저장이 안 되는(또는 반대인) 상태가 된다. **이 비대칭이 SQL Mapper 와 OR Mapper 를 가르는 그 방향 차이의 실물**이다 → [[persistence-framework]] · [[dml]]
- **「collection 으로 join된 객체 삽입하기」의 「삽입」은 `insert` 가 아니다** — 소제목이 그렇게 읽히는데 실제로 하는 일은 **조회 결과를 객체 안에 넣는 것**이다. 바로 다음 절(「forEach 사용하기」)이 정말로 `insert` 문을 만드는 절이라 두 소제목이 붙어 있으면서 낱말이 겹친다 → [[dynamic-sql]]
- **`writer`·`members` 를 채우는 것도 setter 나 필드다** — `<association property="writer">` 가 통하려면 `Board` 에 `setWriter(User)` 나 `writer` 필드가 있어야 하고, `<collection property="members">` 는 `List<User> members` 가 있어야 한다(MyBatis 가 `ArrayList` 를 만들어 넣는다). 이름이 어긋나면 조용히 비어 있다 — Day59 의 「`setProperty(Object obj)` 라는 메서드는 없다」 항목과 **똑같은 도구가 한 겹 안쪽에서 한 번 더 쓰이는 것**이다 → [[reflective-field-access]] · [[reflective-instantiation]]
- **`<resultMap>` 의 `id` 는 문장 id 와 같은 이름 공간에 있지 않다** — `<select id="sql1">` 과 `<resultMap id="BoardMap">` 이 같은 파일에 있어도 서로 부딪히지 않지만, **`<resultMap>` 끼리는 네임스페이스 안에서 유일해야** 하고 다른 매퍼의 것을 쓰려면 `resultMap="다른네임스페이스.BoardMap"` 처럼 점 앞을 붙인다. Day59 의 매퍼 조각들에 `<mapper namespace="…">` 루트 태그가 없던 것이 여기서 한 번 더 걸린다 — **가리킬 이름이 어디서 오는지가 정해지지 않은 상태** → [[mybatis]] · [[xml]]

## 함께 보는 개념

- [[mybatis]] — 이 태그가 사는 층
- [[type-alias]] — `type="board"` 가 통하기 위한 등록
- [[dynamic-sql]] — 같은 회차에서 문장을 만드는 쪽
- [[result-set]] — 접히기 전의 납작한 표
- [[sql-join]] — 그 표를 만드는 문장
- [[db-normalization]] — 객체의 모양을 깨 놓은 쪽
- [[primary-key]] · [[foreign-key]] — `<id>` 자리에 와야 하는 것
- [[object-equality]] · [[hash-code]] — 「같은 행인가」를 판정하는 일반형
- [[reflective-field-access]] · [[reflective-instantiation]] — 매핑을 실제로 수행하는 도구
- [[type-erasure]] · [[generics]] — `ofType` 이 필요한 이유
- [[sql-null]] — 어긋난 이름이 남기는 값
- [[dao-pattern]] — 호출 횟수가 줄어드는 자리
- [[persistence-framework]] — 이 매핑이 한 방향이라는 것의 뜻
- [[dql]] · [[dml]] — 조회와 변경에서 매핑이 갈리는 자리
- [[xml]] — 이 선언이 사는 형식

## 출처

- [[2024-08-21-Day60]] — 「resultMap」 절과 그 아래 「association 옵션」·「collection 으로 join된 객체 삽입하기」 두 소절이 이 개념이다. 「데이터베이스의 결과 셋을 Java 객체에 매핑」·「sql의 컬럼과 java 객체의 필드값을 매핑」·「sql의 join 결과를 java에 리턴」 세 줄로 하는 일을 나누고, `<id>`·`<result>` 로 컬럼과 프로퍼티를 짝지은 뒤 `<association property="writer" javaType="user">` 로 1:1 을, `<collection property="members" ofType="user">` 로 1:N 을 각각 XML 로 실었다 — **두 태그 안이 바깥과 같은 문법이라는 것**과 1:1 은 `javaType`·1:N 은 `ofType` 이라는 것이 이 회차에서 확인되는 형태다. 하루 전 Day59 가 `user_id as no` 라는 SQL 별칭으로만 맞추던 대응이 여기서 별도 선언으로 빠지고, Day55 의 `findBy` + `getMembers` 두 번 호출이 조인 한 문장으로 접힐 길이 열린다. 다만 **`<id>` 와 `<result>` 의 차이를 적지 않았고**(접기의 기준이라는 것), **`<select resultMap="BoardMap">` 로 문장에 붙이는 줄과 실제 조인 SQL 이 둘 다 없어** 이 선언이 어디에 연결되는지 노트만으로는 알 수 없다. `type="board"`·`javaType="user"` 가 등록된 별칭을 전제하는데 그 등록은 같은 노트의 마지막 절에 따로 있고, 컬럼 라벨 충돌·`left join` 이 필요한 이유·`limit` 이 행을 자른다는 것·중첩 대신 `select` 속성을 쓰면 N+1 이 되는 것은 다루지 않았다. 결과 화면은 GitHub 이미지 링크로만 남아 있다
