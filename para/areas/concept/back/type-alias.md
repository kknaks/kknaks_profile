---
type: concept
id: type-alias
title: 타입 별칭 (typeAliases)
aliases:
  - typeAliases
  - typeAlias
  - 타입 별칭
  - type alias
  - "@Alias"
up:
  - 2024-08-21-Day60
tags:
  - 프레임워크
  - 설정
  - java
  - 매퍼
---

# 타입 별칭 (typeAliases)

**클래스의 정규명(패키지까지 붙은 이름)에 짧은 이름을 붙여 두고 XML 에서 그 짧은 이름으로 가리키는 것.** 필기의 한 줄이 정확하다 — 「java 클래스의 전체 이름(패키지 포함)을 짧게 별칭으로 정의하는 문법이다」. **하루 전 Day59 가 `parameterType="user"` 로 실패한 자리가 여기서 닫힌다** — 짧은 이름은 「소문자로 쓰면 되는 것」이 아니라 **어딘가에 등록해 두어야 하는 이름**이었고, 그 「어딘가」가 이 태그다 → [[mybatis]] · [[xml]]

## 정의

두 가지 방법이 있고 필기가 둘을 나란히 적었다.

```xml
<!--typeAlias로 개별 설정하기-->
<typeAlias type="bitcamp.myapp.vo.User" alias="user"/>

<!--패키지명으로 설정하기-->
<package name="bitcamp.myapp.vo"/>
```

| 방법 | 이름을 누가 정하나 | 대상 |
|---|---|---|
| `<typeAlias type alias>` | **내가** `alias` 에 적는다 | 클래스 하나 |
| `<package name>` | **클래스 이름이 그대로** 별칭이 된다 (`User` → `user`) | 그 패키지의 클래스 전부 |
| `@Alias("user")` (클래스에 붙인다) | 내가 애노테이션에 적는다 | 그 클래스 |

셋째 형태는 필기에 없지만 **같은 회차 후반의 주제가 그것이다** — 설정을 XML 이 아니라 **선언 옆에** 두는 방식이고, 그 문법을 만드는 법이 이 노트의 뒷장에 있다 → [[annotation]] · [[reflective-annotation-access]]

### 별칭이 통하는 자리와 안 통하는 자리

| 자리 | 예 | 별칭 |
|---|---|---|
| `resultType`·`parameterType`·`resultMap` 의 `type` | `resultType="user"` | **통한다** |
| `<association javaType>`·`<collection ofType>` | `ofType="user"` | **통한다** |
| 자바 코드 | `sqlSession.selectOne("…", no)` | 해당 없음 — 별칭은 **XML 안의 이름**이다 |

즉 이 이름은 **매퍼와 설정 파일이 쓰는 어휘**이고, 자바 쪽에는 존재하지 않는다. 같은 클래스가 두 이름을 갖게 되는 것이고, 그 대응을 아는 곳이 설정 파일 한 곳이다 → [[result-map]]

### Day59 는 이미 별칭을 쓰고 있었다 — `parameterType="int"`

MyBatis 는 시작할 때 기본 별칭을 스스로 등록해 둔다.

| 별칭 | 실제 타입 |
|---|---|
| `string` | `java.lang.String` |
| `int`·`integer` | **`java.lang.Integer`** (래퍼) |
| `_int`·`_integer` | `int` (기본형) |
| `map`·`hashmap`·`list`·`arraylist` | 대응하는 컬렉션 |

**그래서 Day59 의 `<delete id="delete" parameterType="int">` 는 등록 없이 통했고 `parameterType="user"` 는 통하지 않았다.** 같은 자리에 같은 모양으로 적힌 짧은 이름 둘 중 하나만 실패한 이유가 이것이며, 필기는 그 차이를 「내가 만든 클래스인가」로도 「등록했는가」로도 적지 않았다. 그리고 밑줄 있는 쪽과 없는 쪽이 **기본형과 래퍼로 갈린다는 것**이 이 표에서 가장 놓치기 쉬운 자리다 → [[wrapper-class]] · [[autoboxing]]

## 사용 예시

필기가 실은 두 줄은 조각이라, 설정 파일에서는 이렇게 선다.

```xml
<configuration>
  <properties resource="jdbc.properties"/>

  <typeAliases>
    <typeAlias type="bitcamp.myapp.vo.User" alias="user"/>
    <package name="bitcamp.myapp.vo"/>
  </typeAliases>

  <environments default="development">
    ...
  </environments>
  <mappers>
    ...
  </mappers>
</configuration>
```

**`<typeAliases>` 라는 감싸는 태그가 있고, 그것이 놓이는 자리도 정해져 있다.** `<properties>` 다음, `<environments>` 앞이다 — Day59 가 「DTD 가 정하는 것」으로 배운 넷 중 **「몇 번 · 어떤 순서로」**가 여기서 실제로 걸린다. 순서를 어기면 값이 무시되는 것이 아니라 **설정 파일을 읽는 순간 파싱 오류**다 → [[xml]]

등록이 되면 하루 전의 그 문장이 그대로 통한다.

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

**Day59 의 이 문장은 고칠 것이 없었다 — 빠져 있던 것은 설정 파일의 세 줄이었다.** 「어느 파일이 틀렸는가」가 오류 메시지(`Could not resolve type alias 'user'`)에서 곧바로 나오지 않는 종류의 실패이고, 그래서 매퍼를 들여다보며 오타를 찾게 된다 → [[mybatis]]

## 왜 중요한가

**매퍼 XML 에서 패키지 이름이 사라진다.** `resultType="bitcamp.myapp.vo.User"` 가 스무 문장에 반복되면 패키지를 옮기는 일이 스무 곳을 고치는 일이 되고, 그 스무 곳은 **컴파일러가 찾아 주지 않는 문자열**이다. 별칭으로 바꾸면 대응이 **설정 파일 한 줄**에 모이므로 패키지 이동이 그 한 줄을 고치는 일이 된다 — [[refactoring]] 이 문자열 위에서도 가능해지는 유일한 방법이 「이름을 한 곳에 모으는 것」이다 → [[coupling]]

**그리고 틀렸을 때 걸리는 시점이 다른 문자열들보다 이르다.** MyBatis 가 쓰는 문자열 이름이 셋인데 실패 시점이 갈린다.

| 문자열 | 언제 걸리나 | 어떻게 |
|---|---|---|
| **타입 별칭** | **시작할 때** (설정·매퍼를 읽으며) | `Could not resolve type alias` — 프로그램이 아예 안 뜬다 |
| 문장 id | **그 문장을 부를 때** | `BindingException` |
| 프로퍼티 이름 | 부를 때, 또는 **아무 일도 안 일어난다** | 예외 없이 `null` |

**아래로 갈수록 나쁘다** — 시작할 때 걸리는 오류는 배포 전에 반드시 드러나고, 부를 때 걸리는 것은 그 화면을 써 봐야 알며, 마지막은 데이터를 보고서야 안다. 별칭을 쓰는 것이 정규명을 쓰는 것보다 **덜 안전해지는 것이 아니라 더 이른 시점으로 옮겨지는 것**이다 → [[compilation]]

## 경계와 오해

- **별칭은 대소문자를 구분하지 않는다** — MyBatis 가 별칭을 등록할 때 키를 소문자로 낮춰 넣고 찾을 때도 낮춰서 찾는다. 그래서 `type="board"`·`type="Board"`·`type="BOARD"` 가 **전부 같은 것**을 가리킨다. Day59 노트가 「대문자를 소문자로 쓰면 되는 것이 아니라 어딘가에 등록해 두어야 하는 이름이다」라고 적은 것은 그대로 맞고, **거꾸로 등록만 되어 있으면 대소문자는 보지 않는다**는 것이 더해진다. 두 사실이 함께 있어야 「소문자로 쓰면 된다」는 오해가 왜 생기는지가 설명된다 — `<package>` 로 등록하면 `User` 클래스가 `user` 로도 통하므로 **소문자 규칙처럼 보이는 결과**가 나온다.
- **`<package>` 는 같은 단순명이 둘이면 시작을 막는다** — `bitcamp.myapp.vo.Date` 와 다른 패키지의 `Date` 를 함께 등록하면 `The alias 'date' is already mapped to the value '…'` 로 실패한다. 게다가 `date`·`string`·`int` 는 **이미 기본 별칭이 차지하고 있으므로** 내 클래스 이름이 그중 하나와 같으면 그 자체로 부딪힌다. **편해 보이는 쪽(`<package>`)이 이름 충돌을 자동으로 만드는 쪽**이고, 개별 등록은 그 위험이 없는 대신 클래스마다 한 줄이다 → [[package]]
- **`@Alias` 를 쓰면 클래스가 프레임워크를 알게 된다** — XML 로 등록하면 VO 클래스는 MyBatis 를 전혀 모르는 순수한 자바 파일로 남지만, `@Alias("user")` 를 붙이면 **그 클래스가 MyBatis 의 애노테이션을 `import` 한다.** 설정이 짧아지는 대가로 의존 방향이 하나 생기는 것이고, 「설정을 선언 옆에 둔다」가 언제나 이득이 아닌 이유가 여기다 → [[annotation]] · [[coupling]] · [[dependency-inversion-principle]]
- **별칭이 있어도 자바 코드는 정규명·클래스 리터럴을 쓴다** — `sqlSession.selectOne` 의 첫 인수는 문장 id 이고 타입은 제네릭으로 정해지므로 별칭이 나올 자리가 없다. 「짧은 이름을 등록했으니 자바에서도 쓸 수 있다」는 성립하지 않는다 — 별칭은 **XML 파서가 아는 이름**이지 [[class-loading]] 이 아는 이름이 아니다. 정규명은 `Class.forName` 이 요구하는 그 이름이고, 별칭은 그 앞단의 사전 항목이다 → [[class-metadata]]
- **필기의 두 줄에 `<typeAliases>` 감싸는 태그가 없다** — `<typeAlias …/>` 와 `<package …/>` 만 실려 있어 **어디에 넣는 태그인지가 노트에 없다.** Day59 의 매퍼 조각들에 `<mapper namespace="…">` 루트 태그가 없던 것과 같은 종류의 잘림이고, 이 경우는 더 걸리기 쉽다 — `<configuration>` 바로 아래에 `<typeAlias>` 를 놓으면 DTD 검사에서 거절되므로 **설정 파일이 아예 안 읽힌다** → [[xml]]
- **두 방법을 함께 쓰면 개별 등록이 이기지 않는다 — 순서가 정한다** — `<typeAlias alias="user">` 와 `<package>` 를 둘 다 적으면 같은 클래스에 별칭이 둘 생기는 것이고(둘 다 통한다), 같은 **키**에 다른 클래스가 오면 그때 충돌이다. 「개별 설정이 패키지 설정을 덮어쓴다」는 규칙은 없다 — 필기가 둘을 「두가지 방법」으로 나란히 적었을 뿐 함께 쓸 때의 관계는 다루지 않았다.
- **`typeAliases` ≠ `typeHandlers`** — 설정 파일에서 바로 옆에 오는 태그이고 이름이 닮았는데 하는 일이 다르다. 별칭은 **이름을 짧게 부르는 것**이고, 타입 핸들러는 **자바 타입과 JDBC 타입 사이의 변환**(예: `Boolean` ↔ `'Y'`/`'N'`)을 맡는다. 즉 하나는 「무엇이라 부를까」이고 하나는 「어떻게 바꿀까」다. 컬럼 값이 이상하게 들어가는 문제를 별칭에서 찾으면 영원히 못 찾는다 → [[sql-data-type]]
- **별칭은 SQL 의 컬럼 별칭과 아무 관계가 없다** — `user_id as no` 의 `as` 도 「별칭」이고 `<typeAlias>` 도 「별칭」인데, 앞은 **결과 표의 컬럼 라벨**을 바꾸는 SQL 문법이고 뒤는 **자바 클래스를 부르는 이름**을 정하는 설정이다. Day59 가 앞을 쓰고 Day60 이 뒤를 배우는데 같은 낱말이라 한 주제로 묶이기 쉽다 — 그리고 둘 다 「이름이 어긋나면 조용히 비어 있다」는 결과를 공유해서 더 헷갈린다 → [[dql]] · [[result-map]]

## 함께 보는 개념

- [[mybatis]] — 이 별칭이 쓰이는 층
- [[result-map]] — `type`·`javaType`·`ofType` 이 이 이름을 받는 자리
- [[dynamic-sql]] — `parameterType` 이 이 이름을 받는 자리
- [[xml]] — DTD 가 태그의 자리와 순서를 정하는 것
- [[annotation]] · [[reflective-annotation-access]] — 같은 등록을 선언 옆에서 하는 방법
- [[class-loading]] · [[class-metadata]] — 정규명이 실제로 필요한 자리
- [[package]] — 별칭이 걷어내는 것
- [[wrapper-class]] · [[autoboxing]] — `int` 와 `_int` 가 갈리는 축
- [[sql-data-type]] — 타입 핸들러가 맡는 다른 축
- [[coupling]] · [[refactoring]] — 이름을 한 곳에 모으는 값
- [[compilation]] — 문자열이 늦게 걸린다는 것의 기준선
- [[dql]] — 같은 낱말을 쓰는 SQL 쪽 별칭

## 출처

- [[2024-08-21-Day60]] — 「typeAliases」 절이 이 개념이다. 「java 클래스의 전체 이름(패키지 포함)을 짧게 별칭으로 정의하는 문법이다」로 정의하고 `<typeAlias type="bitcamp.myapp.vo.User" alias="user"/>`(개별)와 `<package name="bitcamp.myapp.vo"/>`(패키지 단위) 두 방법을 나란히 실었다. **하루 전 Day59 가 `parameterType="user"` 로 실패한 자리**가 여기서 닫히는데, 필기는 두 회차를 잇지 않았고 같은 노트 앞부분의 `type="board"`·`javaType="user"`·`ofType="user"` 가 이 등록을 이미 전제하고 있다는 것도 적지 않았다. 실린 것이 태그 두 줄뿐이라 **감싸는 `<typeAliases>` 와 그것이 `<configuration>` 안에서 놓이는 자리가 빠져 있고**, 별칭이 대소문자를 구분하지 않는다는 것·`int`·`string` 같은 기본 별칭이 이미 등록되어 있어 Day59 의 `parameterType="int"` 는 그래서 통했다는 것·`<package>` 가 같은 단순명 둘을 만나면 시작 자체가 막힌다는 것·`@Alias` 로 같은 등록을 애노테이션으로 할 수 있다는 것은 다루지 않았다
