---
type: concept
id: xml
title: XML (Extensible Markup Language)
aliases:
  - XML
  - xml
  - 확장 마크업 언어
  - 마크업 언어
  - markup language
  - DTD
  - Document Type Definition
  - 문서 타입 정의
up:
  - 2024-08-20-Day59
  - 2024-10-01-Day86
tags:
  - 데이터형식
  - 설정
  - 파싱
  - 스키마
---

# XML (Extensible Markup Language)

**태그로 값을 감싸 데이터를 나무 구조로 적는 텍스트 형식, 그리고 그 태그를 내가 정의해 쓸 수 있게 한 규약.** Day59 의 세 줄이 그 셋을 짚었다 — 「데이터를 구조화 시켜 저장하는 파일로 데이터 끼리 상관관계를 표현 할 수 있다」·「Markup 언어는 `<tag> value </tag>` tag로 시작해서 끝나는 언어이다」·「XML은 Markup언어의 사용규칙을 준수하여 만들 파일이다」. MyBatis 를 배우기 직전에 이 절이 오는 이유는 **그 프레임워크의 설정과 SQL 이 전부 XML 이기 때문**이다 → [[mybatis]]

## 정의

문법이 다섯 가지로 끝난다.

| 조각 | 모양 | Day59 의 설정 파일에서 |
|---|---|---|
| 선언 | `<?xml version="1.0" encoding="UTF-8" ?>` | 첫 줄 |
| 요소(element) | `<이름>…</이름>` · 빈 것은 `<이름/>` | `<configuration>` · `<properties …/>` |
| 속성(attribute) | `<이름 키="값">` | `resource="jdbc.properties"` |
| 중첩 | 요소 안에 요소 | `configuration > environments > environment > dataSource` |
| 주석 | `<!-- … -->` | 「DBMS 접속정보」 |

**well-formed 규칙이 HTML 보다 엄격하다.** 루트 요소가 하나뿐이어야 하고, 모든 태그가 닫혀야 하고, 겹칠 수 없고, 속성값에 따옴표가 있어야 한다. 하나라도 어긋나면 **파싱 자체가 실패**하고 프로그램이 시작되지 않는다.

### DTD — 「그 태그를 어떻게 써야 하는가」

Day59 가 XML 절보다 **먼저** DTD 를 놓았다 — 「태그 사용규칙을 담은 문서이다」·「XML파일을 만들때 해당 규칙을 통해 작성을 해야한다」.

```xml
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "https://mybatis.org/dtd/mybatis-3-config.dtd">
```

DTD 가 정하는 것은 넷이다 — **어떤 요소가 있는가**, **그 안에 무엇이 들어갈 수 있는가**, **몇 번 · 어떤 순서로**, **어떤 속성이 필수인가**. 그래서 XML 은 두 층의 검사를 받는다.

| 층 | 무엇을 보나 | 어긋나면 |
|---|---|---|
| well-formed | 태그가 닫혔는가, 겹치지 않는가 | 파싱 실패 |
| **valid** (DTD·스키마) | 이 문서가 **이 종류의 문서인가** | 「여기 올 요소가 아니다」 |

**둘째 층이 있다는 것이 XML 을 설정 형식으로 쓰는 이유의 절반이다** — 오타가 「값이 `null` 이더라」가 아니라 **파일을 읽는 순간의 오류**로 나타난다 → [[json]]

## 사용 예시

Day59 의 `mybatis-config.xml` 이 위의 조각을 다 쓴다.

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "https://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!-- DBMS 접속정보 -->
    <properties resource="jdbc.properties"/>

    <!-- SQL문 파일 위치 -->
    <environments default="development-local">

        <!-- 개발하는 동안 사용할 DBMS 접속 정보 -->
        <environment id="development-local">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="${jdbc.driver}"/>
                <property name="url" value="${jdbc.url}"/>
                <property name="username" value="${jdbc.username}"/>
                <property name="password" value="${jdbc.password}"/>
            </dataSource>
        </environment>

    </environments>

    <mappers>
        <mapper resource="UserDaoMapper.xml"/>
        <mapper resource="BoardDaoMapper.xml"/>
    </mappers>
</configuration>
```

**세 자리가 같은 문법의 다른 쓰임이다.** `<properties resource=…/>` 는 **다른 파일을 가리키고**, `<property name= value=/>` 는 **키-값 한 쌍을 담고**, `<environment id=…>` 는 **여러 개 중 하나를 이름으로 고르게 한다**(`default="development-local"` 이 그 선택이다). 개발용·운영용 접속 정보를 나란히 두고 한 줄로 갈아타는 형태가 이 세 번째 쓰임 위에 얹혀 있다.

그리고 매퍼 XML 은 **값이 SQL 문장 자체**다.

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

**태그의 값이 코드인 자리**이고, 그래서 XML 의 문자 제약이 SQL 을 쓰는 데 그대로 걸린다(아래 「경계와 오해」) → [[mybatis]] · [[dql]]

## 왜 중요한가

**프로그램의 결정 일부가 컴파일되지 않는 파일로 옮겨간다.** 접속 정보·드라이버 클래스 이름·SQL 문장이 자바 코드 밖에 있으면 **다시 컴파일하지 않고 바꿀 수 있고**, 개발용과 운영용을 파일로 갈아탈 수 있다. 「이 값을 바꾸려면 코드를 고쳐야 하나」가 이 형식 하나로 갈린다 → [[class-loading]] · [[build]]

**그리고 「구조가 있는 텍스트」의 첫 형식이다.** [[csv]] 는 표 하나만 담을 수 있고 줄과 콤마로는 중첩을 표현할 수 없다. XML 은 요소 안에 요소를 넣어 `environments > environment > dataSource > property` 처럼 **깊이가 있는 설정**을 담는다 — Day59 의 설정 파일이 네 겹인 것이 그 능력을 그대로 쓴 것이다 → [[csv]] · [[json]]

**대신 사람이 쓸 것이 많아진다.** 같은 내용의 JSON 이 절반 길이이고, 여는 태그와 닫는 태그를 짝 맞추는 일이 사람의 몫이다. 통신 형식이 JSON 으로 넘어간 이유가 그 부피이고, **설정에 XML 이 남은 이유는 주석과 스키마 검증**이다 → [[json]]

## 경계와 오해

- **XML ≠ HTML** — 태그를 쓰는 모양이 같아 형제로 보이는데 축이 반대다. HTML 은 **태그 이름이 정해져 있고**(브라우저가 아는 것만) 닫지 않아도 관용되지만, XML 은 **이름을 내가 정하고**(`<mappers>` 는 아무도 모르는 태그다) 하나라도 어긋나면 파싱이 실패한다. 「HTML 처럼 대충 써도 되겠지」로 매퍼 XML 을 쓰면 앱이 시작되지 않는다.
- **DTD 의 URL 을 내려받지 않는다** — `"https://mybatis.org/dtd/mybatis-3-config.dtd"` 가 주소로 적혀 있어 인터넷이 필요해 보이는데, 그 문자열은 **식별자**이고 MyBatis 는 jar 안의 사본을 쓴다(`XMLMapperEntityResolver` 가 그 일을 한다). 그래서 오프라인에서도 돌고, 반대로 **그런 사본을 두지 않은 라이브러리는 매번 남의 서버를 때린다** — 그것이 옛 XML 파싱 코드가 느리거나 방화벽 안에서 멈추던 이유이고, 지금은 외부 엔티티를 아예 끄는 것이 보안 기본값이다(XXE).
- **DTD 는 순서까지 정한다** — `<properties>` → `<environments>` → `<mappers>` 순서가 MyBatis config DTD 에 박혀 있어서, 읽기 좋게 `<mappers>` 를 위로 올리면 **파싱 오류**다. Day59 의 파일이 그 순서인 것은 공식 문서를 옮겨 적었기 때문이지 취향이 아니다. JSON 에는 이런 제약이 없다는 것이 두 형식의 실제 차이 중 하나다.
- **`${jdbc.driver}` 는 XML 문법이 아니다** — XML 파서에게 그것은 그냥 문자 다섯 개 + 이름이다. `${}` 를 읽어 `jdbc.properties` 의 값으로 바꿔 주는 것은 **MyBatis** 이고, 그래서 `<properties resource=…/>` 를 지우면 치환이 일어나지 않고 값이 문자열 그대로 드라이버 이름이 된다. **한 파일 안에 두 문법이 겹쳐 있다는 것**을 모르면 치환이 안 될 때 XML 쪽을 뒤진다 → [[mybatis]]
- **`&` 와 `<` 를 값으로 쓸 수 없다 — 그래서 SQL 이 걸린다** — 둘은 문법 문자라 `&amp;`·`&lt;` 로 쓰거나 `<![CDATA[ … ]]>` 로 감싸야 한다. 매퍼 XML 에서 `where no < 10` 이 **파싱 오류**가 되는 것이 이것이고, 자바 문자열로 SQL 을 쓸 때는 없던 제약이다. 「SQL 을 XML 로 옮기면 그냥 붙여 넣으면 된다」가 처음 깨지는 자리 → [[sql-operator]] · [[mybatis]]
- **주석 안에 `--` 를 둘 수 없다** — `<!-- … -->` 안에 `--` 가 있으면 파싱 오류다. **SQL 의 한 줄 주석이 `--` 라서** 매퍼 XML 에서 SQL 문장을 XML 주석으로 잠시 막으려 하면 걸린다. 두 형식의 주석 문법이 정확히 충돌하는 자리다.
- **DTD ≠ XSD** — DTD 는 「어떤 요소가 어떤 순서로」까지만 정하고 **타입이 거의 없다**(속성은 대개 문자열이다). 그래서 `type="POOLED"` 의 값이 오타여도 XML 검증은 통과하고 MyBatis 가 나중에 걸러 낸다. 요즘 스키마는 XSD·RELAX NG 이고 그쪽은 숫자·열거·범위를 표현한다 — **「스키마가 있으니 잡힌다」의 범위가 스키마 언어마다 다르다.**
- **「데이터 끼리 상관관계를 표현 할 수 있다」의 상관관계는 나무뿐이다** — 필기의 표현인데, XML 이 문법으로 주는 것은 **부모-자식 하나**다. 「이 요소가 저 요소를 참조한다」는 `ID`/`IDREF` 로 흉내내거나 `id="development-local"` ↔ `default="development-local"` 처럼 **값으로 짝을 맞추는 관례**로 만든다 — Day59 의 파일이 실제로 후자다. 그리고 그 짝은 XML 이 검사해 주지 않아서 `default` 를 오타 내면 파싱은 통과하고 실행 중에 환경을 못 찾는다.
- **`encoding="UTF-8"` 은 선언이지 변환이 아니다** — 파일이 실제로 다른 인코딩으로 저장돼 있으면 이 줄이 거짓이 되고, 한글 주석에서 파싱 오류가 난다. 「선언해 두면 UTF-8 이 된다」가 아니라 **「이 파일은 UTF-8 이라고 파서에게 알려 준다」**이고, 선언과 실물이 갈리는 것이 XML 에서 가장 흔한 인코딩 사고다 → [[character-encoding]]
- **속성과 자식 요소 중 어디에 둘지는 문법이 정해 주지 않는다** — 같은 값을 `<property name="url" value="…"/>` 로도 `<url>…</url>` 로도 쓸 수 있고, MyBatis 는 앞을 골랐다. **모델링 선택이 문법에 없다**는 것이 XML 을 읽는 코드가 매번 달라지는 이유이고, 값 하나를 꺼내는 데도 「속성인가 텍스트인가」를 먼저 알아야 한다 — JSON 에는 그 갈래가 없다 → [[json]]
- **DTD 를 XML 절보다 먼저 놓은 순서가 거꾸로다** — 필기의 「사용준비」 절이 DTD → XML → 설정파일 순인데, DTD 는 **XML 을 제약하는 것**이라 XML 이 무엇인지 안 뒤에 와야 한다. 배우는 순서로는 「이 파일을 왜 이렇게 써야 하나」가 먼저 궁금했던 흔적으로 읽히지만, DTD 를 먼저 보면 「태그 사용규칙」이 무엇의 규칙인지가 비어 있다.

## 함께 보는 개념

- [[json]] — 같은 일을 하는 다른 형식. 부피·주석·스키마에서 갈린다
- [[csv]] — 중첩을 담을 수 없는 앞 형식
- [[mybatis]] — 이 형식을 설정과 SQL 에 쓰는 실물
- [[sql-session]] — 그 설정을 읽어 세워지는 객체
- [[class-loading]] — 설정 파일의 클래스 이름 문자열이 닿는 곳
- [[character-encoding]] — `encoding` 선언이 거짓이 될 수 있는 자리
- [[annotation]] — 설정을 다시 코드 안으로 되돌린 반대 방향
- [[build]] — 설정 파일이 어디에 놓여야 읽히는가
- [[serialization]] — 객체를 텍스트로 적는 다른 층
- [[sql-operator]] — `<` 가 XML 에서 걸리는 자리
- [[web-application]] — XML 설정이 가장 많이 쓰였던 층
- [[java-config]] — 같은 설정을 자바로 적는 반대편

## 출처

- [[2024-10-01-Day86]] — 여섯 주 뒤. **네임스페이스와 스키마가 왜 있는지가 나온다.** 스프링 설정 XML 의 `xmlns="http://www.springframework.org/schema/beans"` 와 `xsi:schemaLocation="네임스페이스명 명세서URL"` 을 필기가 **「java의 기본 패키지 처럼 xml의 기본 네임 스페이스」**로 옮긴 것이 정확한 비유다 — `<context:component-scan>` 을 쓰려면 `xmlns:context` 를 따로 선언해야 하고, 태그 이름이 어느 명세의 것인지를 그것이 정한다. 동시에 이 회차는 그 XML 이 자바 클래스로 대체되는 쪽도 나란히 보여 준다 → [[java-config]]
- [[2024-08-20-Day59]] — MyBatis 「사용준비」 절에서 DTD 를 「태그 사용규칙을 담은 문서」로, XML 을 「데이터를 구조화 시켜 저장하는 파일」·「`<tag> value </tag>` tag로 시작해서 끝나는 언어」로 세 줄씩 정의했다. 그리고 `mybatis-config.xml` 전문을 실어 선언·`<!DOCTYPE>`·요소·속성·중첩·주석과 `${}` 치환까지 한 파일에서 다 보이고, 매퍼 XML 에서는 **태그의 값이 SQL 문장**인 쓰임까지 나온다. 다만 well-formed 와 valid 의 두 층 구분, DTD 가 요소의 순서까지 정한다는 것, `&`·`<` 를 값으로 쓸 수 없어 SQL 의 부등호가 걸린다는 것, DTD 의 URL 이 실제로 내려받히지 않는다는 것, `${}` 가 XML 문법이 아니라 MyBatis 의 것이라는 것은 다루지 않았다. 절의 순서가 DTD → XML 이라 제약을 먼저 보고 대상을 나중에 보는 형태다
