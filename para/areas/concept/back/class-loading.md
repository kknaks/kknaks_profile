---
type: concept
id: class-loading
title: 클래스 로딩 (Class Loading)
aliases:
  - 클래스 로딩
  - 클래스로딩
  - class loading
  - Class.forName
  - forName
  - 동적 로딩
  - 클래스 초기화
  - static 초기화
up:
  - 2024-08-20-Day59
tags:
  - java
  - jvm
  - 실행시점
  - 리플렉션
---

# 클래스 로딩 (Class Loading)

**`.class` 파일을 읽어 그 클래스의 정보를 JVM 안에 세우는 일.** 클래스를 처음 쓰려는 순간 한 번 일어나고, 그때 `static` 변수가 준비되고 `static` 블록이 실행된다. Day59 가 이것을 리플렉션의 첫 절에 두는 이유는 **클래스를 문자열 이름으로 지목하는 유일한 통로**가 여기이기 때문이다 — 「클래스를 동적으로 호출 할 때 필요하다. 주로 라이브러리 개발에 사용된다」 → [[class-metadata]] · [[jvm]]

## 정의

Day59 가 로딩을 일으키는 두 표기를 나란히 적었다.

```java
Class clazz1 = Class.forName("fully qualified class name")
Class clazz2 = classNmae.class;
```

| | `Class.forName("...")` | `타입이름.class` |
|---|---|---|
| 클래스를 지목하는 것 | **문자열** — 실행 중에 바뀔 수 있다 | **타입 이름** — 컴파일할 때 코드에 박힌다 |
| 그 클래스가 없으면 | 실행 시점 `ClassNotFoundException` | **컴파일 오류** |
| `static` 초기화 | **한다** | **하지 않는다** (실제로 쓸 때 한다) |
| 검사 예외 | `throws ClassNotFoundException` | 없다 |

Day59 의 두 줄이 그 차이를 적은 것이다 — 「**forName** : 클래스를 로딩 시 스태틱변수 선언과 스태틱필드 실행」·「**.class** : 클래스 로딩 시 스태틱 미 실행, 실제 클래스 사용시 스태틱변수 선언과 스태틱필드 실행」 → [[static-member]]

### 로딩은 세 걸음이고 필기는 그중 둘을 뭉쳐 부른다

명세는 **loading → linking → initialization** 으로 가른다. 「스태틱 미 실행」이 무슨 뜻인지는 이 구분 없이는 설명되지 않는다.

| 걸음 | 하는 일 | Day59 의 표현 |
|---|---|---|
| loading | `.class` 를 찾아 읽고 `Class` 객체를 만든다 | 「클래스 로딩」 |
| linking | 검증하고 `static` 변수에 **기본값**을 넣는다 | 「스태틱변수 선언」 |
| initialization | `static` 초기화식과 `static` 블록을 **위에서 아래로** 실행한다 | 「스태틱필드 실행」 |

**`.class` 는 앞의 둘까지만 하고 세 번째를 미룬다.** 그래서 `int.class` 처럼 초기화할 것이 아무것도 없는 타입에서는 두 표기의 차이가 드러나지 않는다 → [[class-file-format]] · [[default-initialization]]

### 중첩 클래스는 따로 로딩된다

Day59 가 이것을 별도 절로 뽑았다 — 「상위 클래스를 로딩하는 것과 종속된 클래스를 로딩하는 것은 별개이다」·「종속 클래스는 **패키지.상위클래스$종속클래스**의 경로로 로딩 가능하다」.

```java
Class<?> clazz = Class.forName("com.eomcs.reflect.ex02.Exam0110$A");
```

**바깥 클래스를 로딩해도 안쪽은 로딩되지 않는다.** 중첩 클래스는 별개의 `.class` 파일(`Exam0110$A.class`)이고, 바깥이 그것을 **쓸 때** 그 시점에 로딩된다. Day59 가 그 근거를 「상위 클래스가 종속 클래스를 사용하는 것이지 포함하는 것은 아니기 때문이다」로 적었다 → [[nested-class]] · [[java-compilation-unit]]

## 사용 예시

Day59 가 「.class 를 쓰면 유지보수에 불리하다」의 근거로 든 코드다.

```java
// className만 변경하면 클래스 로딩 부분의 수정이 없다.
String className;
Class clazz1 = Class.forName(className);

// class가 로딩되는 부분에서 모두 수정해야한다.
className2.class
```

**이 코드가 보이려던 것은 「클래스 이름이 값으로 있으면 코드를 고치지 않고 바꿀 수 있다」다.** 그 말은 맞고, 실제로 그 형태가 나흘 전 [[jdbc]] 회차의 드라이버 등록에 그대로 있었다.

```java
Class.forName("com.mysql.cj.jdbc.Driver");   // Day56 — 벤더 이름이 문자열이다
```

그리고 **이 회차의 MyBatis 설정 파일이 그 문자열을 파일 밖으로 내보낸 결과물**이다.

```xml
<property name="driver" value="${jdbc.driver}"/>
```

`jdbc.properties` 에 적힌 값이 `${jdbc.driver}` 로 들어와 결국 `Class.forName` 에 닿는다 — **자바 코드에 클래스 이름이 한 글자도 없는 상태**이고, DB 를 바꾸는 일이 설정 한 줄이 된다. 「주로 라이브러리 개발에 사용된다」는 첫 줄이 여기서 실물이 된다 → [[mybatis]] · [[xml]]

## 왜 중요한가

**클래스 이름이 문자열이 되면 프로그램이 자기가 모르는 클래스를 쓸 수 있다.** 컴파일할 때 `import` 도 필요 없고 그 jar 가 없어도 컴파일된다. 드라이버·플러그인·`resultType` 이 전부 이 성질에 얹혀 있다 — MyBatis 의 `resultType="bitcamp.myapp.vo.User"` 는 XML 안의 **문자열**이고, MyBatis 는 그 클래스를 컴파일 시점에 몰랐다 → [[mybatis]] · [[reflective-instantiation]]

**그리고 「언제 실행되나」를 물어야 하는 코드가 생긴다.** `static` 블록은 눈에 보이는 호출이 없는데도 실행된다. [[jdbc]] 노트가 「등록의 방아쇠는 생성이 아니라 클래스 로딩」이라고 적은 것이 정확히 이 지점이고, 그것을 모르면 `new Driver()` 로 만든 객체를 버리는데도 등록이 되는 이유를 설명할 수 없다 → [[static-member]]

**대신 컴파일러의 보호가 사라진다.** 문자열 하나 틀리면 실행 중에 `ClassNotFoundException` 이고, IDE 의 이름 바꾸기가 그 문자열을 따라오지 않는다. **컴파일 시점에 정해 두는 것과 실행 시점에 고를 수 있는 것을 맞바꾸는 것**이 이 문법의 전부다 → [[exception-handling]]

## 경계와 오해

- **「객체를 인스턴스 하는 것이 클래스 로딩이며」는 반대다** — Day59 의 문장인데 인스턴스화는 로딩이 아니다. `new` 가 로딩을 **일으키는 계기**이고(그 클래스가 아직 로딩되지 않았다면), 로딩이 끝난 뒤에 인스턴스가 만들어진다. 둘이 같은 것이라면 ① 인스턴스를 하나도 만들지 않는 `Class.forName` 이 왜 `static` 블록을 돌리는지, ② 인스턴스를 백 개 만들어도 `static` 블록이 왜 한 번만 도는지 둘 다 설명되지 않는다. **같은 필기의 「생성자 정보 추출」 절이 스스로 반증한다** — 「객체를 생성하기 위해서는 클래스호출, 생성자 호출, 인스턴스호출 순으로 이루어진다」로 **세 걸음**을 적었으니 첫 걸음과 셋째 걸음은 같은 것이 아니다 → [[reflective-instantiation]] · [[instance]]
- **뒷문장(「레퍼런스를 선언하는 것과는 다르다」)은 맞고 이유가 다르다** — `My obj;` 가 로딩을 일으키지 않는 것은 배열이어서가 아니라 **타입 이름을 쓰는 일에는 실행이 없기 때문**이다. [[nested-class]] 회차가 `static` 메서드에서 `X obj;` 는 되고 `this.new X()` 만 막히는 것으로 같은 구별을 이미 보였다 — **「이름을 쓴다」와 「대상을 만든다」는 다른 일**이다 → [[variable]]
- **「유지보수에 불리하다」가 거꾸로다** — 유지보수의 보호를 받는 쪽은 `.class` 다. 클래스 이름을 바꾸면 IDE 의 이름 바꾸기가 `Exam01.class` 는 따라 고치고 **`"com.eomcs...Exam01"` 문자열은 건드리지 않는다.** 패키지를 옮기기만 해도 `forName` 쪽은 조용히 깨지고 그 사실을 실행해 봐야 안다. `forName` 이 이기는 자리는 유지보수가 아니라 **컴파일 시점에 어느 클래스인지 모를 때** 하나다 — 필기가 든 예(`String className`)가 실제로 그 경우이므로 **예는 맞고 붙인 이름이 틀렸다.**
- **`Class clazz2 = classNmae.class;` 는 컴파일되지 않는다 — 오타 때문만이 아니다** — `classNmae` 는 `className` 의 오기이지만, 오타를 고쳐도 **변수에는 `.class` 를 붙일 수 없다.** `.class` 는 필드가 아니라 **타입 이름 뒤에만 서는 클래스 리터럴**이고, 아래 예시의 `className2.class` 도 같은 형태다. 두 줄이 보이려던 것은 「여기에 타입 이름을 직접 적어야 한다」이므로 뜻은 통하지만 코드로는 성립하지 않는다 → [[literal]] · [[class-metadata]]
- **「스태틱변수 선언」과 「스태틱필드 실행」이라는 일은 없다** — 선언은 컴파일 시점의 일이고, 필드는 실행되지 않는다. 실행 시점에 일어나는 것은 **기본값 할당**(linking)과 **초기화식·`static` 블록 실행**(initialization)이다. 낱말이 어긋난 것뿐이라 뜻은 통하지만, 그 구분이 없으면 `.class` 가 「아무 일도 안 한다」로 읽힌다 — 실제로는 로딩까지 다 하고 초기화만 미룬다 → [[static-member]] · [[default-initialization]]
- **`Class.forName` 도 초기화를 건너뛸 수 있다** — 세 인수 오버로드가 있다. `Class.forName("...", false, loader)` 는 로딩만 하고 `static` 블록을 돌리지 않아서, **클래스를 훑어보기만 하는 도구**(애노테이션 스캐너, IDE)가 남의 `static` 블록을 실행시키지 않고 구조를 볼 수 있다. 두 표기의 차이가 「메서드냐 리터럴이냐」가 아니라 **인수**에 있다는 것이 이 오버로드로 드러난다 → [[annotation]]
- **로딩은 클래스마다 한 번이라 `static` 블록도 한 번이다** — `Class.forName` 을 열 번 불러도 초기화는 첫 번째에만 일어나고 나머지는 이미 만들어진 같은 `Class` 인스턴스를 돌려받는다. 필기가 「forName : 로딩 시 스태틱 실행」만 적어 부를 때마다 도는 것처럼 읽히는데, 그렇다면 [[jdbc]] 의 드라이버가 호출 수만큼 등록될 것이다. 「[[class-metadata]] 의 `Class` 인스턴스는 클래스마다 하나」와 같은 사실의 다른 면이다 → [[singleton-pattern]]
- **`getCanonicalName()` 이 준 이름을 `Class.forName` 에 넣으면 실패한다** — 중첩 클래스에서 정규명은 `...Exam01.A`(점)이고 로딩에 필요한 이름은 `...Exam01$A`(달러)다. **Day59 가 같은 절에서 네 이름을 나란히 찍어 놓고 이 함정을 말하지 않았다** — 위 예제가 `forName` 인수로 `$` 를 쓰고 바로 아래에서 `getCanonicalName()` 의 `.` 표기를 출력한다. 사람에게 보여 줄 이름과 로딩에 쓰는 이름이 갈리며, 로딩에 써야 하는 것은 **`getName()`** 이다 → [[class-metadata]]
- **클래스 로딩 ≠ ClassLoader** — 「로딩」이라는 낱말이 그 일을 하는 객체(`ClassLoader`)와 겹쳐 읽히는데, Day59 가 다룬 것은 **로딩이라는 사건**이고 그 사건을 누가 어떤 순서로 수행하는지(부트스트랩 → 플랫폼 → 애플리케이션의 위임 모델, 같은 이름이 로더마다 다른 클래스가 될 수 있다는 것)는 이 회차에 나오지 않는다. `Class.forName(name)` 이 **부르는 쪽의 로더**를 쓰는 것도 그 층의 이야기이고, 웹 컨테이너에서 같은 클래스가 두 번 로딩되어 `ClassCastException` 이 나는 사고가 거기서 생긴다 → [[classpath]] · [[jvm]]
- **`ClassNotFoundException` 과 `NoClassDefFoundError` 는 다른 신호다** — 앞은 「이름으로 찾았는데 없다」(리플렉션 쪽의 검사 예외)이고, 뒤는 「컴파일할 때는 있었는데 실행할 때 없다」(에러이지 예외가 아니다). 같은 「클래스가 없다」인데 **어느 표기로 지목했는지가 예외 종류를 정한다** — 그래서 스택트레이스만 보고도 그 자리가 `forName` 인지 `new` 인지 알 수 있다 → [[exception-handling]] · [[classpath]]
- **로딩되는 것은 소스가 아니라 `.class` 다** — 그래서 `.java` 파일이 있어도 컴파일하지 않으면 로딩되지 않고, 반대로 소스 없이 `.class` 만 있어도 로딩된다. 「클래스를 동적으로 호출한다」가 「소스를 읽어 실행한다」로 읽히면 인터프리터와 섞인다 → [[compilation]] · [[bytecode]] · [[interpreter]]
- **`Class.forName` 은 인스턴스를 만들지 않는다** — 첫 절의 제목이 「클래스로딩」인데 필기의 다른 문장이 「객체를 인스턴스 하는 것」이라 두 일이 겹쳐 읽힌다. `forName` 이 돌려주는 것은 **그 클래스에 대한 정보 객체**이고, 그 클래스의 인스턴스를 만들려면 생성자를 따로 골라야 한다 → [[reflective-instantiation]]

## 함께 보는 개념

- [[class-metadata]] — 로딩의 결과로 손에 들어오는 객체
- [[static-member]] — 로딩이 방아쇠를 당기는 것
- [[reflective-instantiation]] — 로딩 다음 걸음
- [[reflective-invocation]] — 이름으로 찾은 클래스에서 메서드를 부르는 자리
- [[jdbc]] — 이 문법이 실제로 쓰이던 첫 자리(드라이버 등록)
- [[mybatis]] — 클래스 이름이 XML 문자열로 옮겨간 결과
- [[nested-class]] — `$` 표기와 별개 로딩
- [[classpath]] — 그 이름을 어디서 찾는가
- [[class-file-format]] · [[bytecode]] — 로딩되는 실물
- [[jvm]] — 로딩을 수행하는 주체
- [[literal]] — `.class` 의 정체
- [[default-initialization]] — linking 이 넣는 기본값
- [[exception-handling]] — 문자열로 지목한 대가
- [[compilation]] — 로딩 앞에 있어야 하는 일
- [[annotation]] — 초기화 없이 클래스를 훑는 도구들이 사는 자리

## 출처

- [[2024-08-20-Day59]] — 「Reflection API」의 첫 절이 「클래스로딩」이고, `Class.forName("패키지를 포함한 전체 클래스명")` 과 `타입.class` 두 표기를 나란히 놓아 **`forName` 은 `static` 을 실행하고 `.class` 는 실제로 쓸 때까지 미룬다**는 차이를 적었다. 중첩 클래스는 바깥과 별개로 로딩되며 `패키지.상위클래스$종속클래스` 경로로 지목한다는 것, 그리고 클래스 이름이 문자열이면 그 변수만 바꿔 로딩 대상을 갈아탈 수 있다는 것(`String className` 예제)이 이 회차의 값이다. 다만 「객체를 인스턴스 하는 것이 클래스 로딩이며」는 로딩과 인스턴스화를 뒤바꾼 것이고, 「.class 는 유지보수에 불리하다」는 IDE·컴파일러의 보호를 받는 쪽이 `.class` 라는 점에서 거꾸로이며, `classNmae.class`·`className2.class` 는 변수에 클래스 리터럴을 붙여 컴파일되지 않는다. loading·linking·initialization 세 걸음, `Class.forName(name, false, loader)` 오버로드, 로딩이 클래스마다 한 번뿐이라는 것, `getCanonicalName()` 의 점 표기를 `forName` 에 넣을 수 없다는 것은 필기에 없다
