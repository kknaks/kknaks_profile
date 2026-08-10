---
type: concept
id: annotation
title: 애노테이션 (Annotation)
aliases:
  - 애노테이션
  - 어노테이션
  - annotation
  - "@interface"
  - 애노테이션 정의
up:
  - 2024-05-31-Day06
  - 2024-06-24-Day21
  - 2024-07-16-Day36
  - 2024-08-21-Day60
  - 2024-10-21-Day98
tags:
  - java
  - 문법
  - 메타데이터
---

# 애노테이션 (Annotation)

클래스·변수·메서드 선언에 붙이는 표시. 생김새는 [[comment]] 같지만 **컴파일러와 [[jvm]] 이 읽는다** — 무시되지 않는다.

## 정의

`@` 뒤에 이름을 쓰고, 값이 필요하면 프로퍼티로 넘긴다.

```plaintext
@애노테이션명(프로퍼티명=값, 프로퍼티명=값, ...)
```

값이 하나면 그대로, 여럿이면 중괄호로 묶는다.

- `@Override` — 값 없음
- `@SuppressWarnings(value="deprecation")` — 값 하나
- `@SuppressWarnings(value={"unchecked", "deprecation"})` — 값 여럿

### 두 달 반 뒤 Day60 — 만드는 쪽으로 넘어간다

Day06~36 은 **남이 만든 것을 붙이는 쪽**이었다. Day60 이 반대편을 배운다. 선언하는 문법은 `interface` 앞에 `@` 를 붙인 것이다.

```java
public @interface MyAnnotation2 {
  String value(); // 애노테이션의 기본 프로퍼티이다.
}
```

**메서드처럼 선언한 것이 프로퍼티가 된다.** 필기가 그것을 두 줄로 적었다 — 「인터페이스에서 메서드 이름은 property(변수)로 작성한다」·「사용 할 때는 property를 호출하여 사용한다」. 위 「정의」의 `프로퍼티명=값` 이 어디서 오는지가 여기서 채워진다.

| 붙일 때 | 선언에 적은 것 |
|---|---|
| `@MyAnnotation(value="값")` | `String value();` |
| `@MyAnnotation("값2")` | 같은 선언 — **`value` 하나만 줄 때는 이름 생략** |
| `@MyAnnotation2` (값 없이) | `String value() default "홍길동";` |
| `@Myannotation3(value="값", tel="tel")` | `String value(); String tel();` — **둘 이상이면 이름을 다 적는다. 순서는 무관** |

**`default` 가 있으면 선택, 없으면 필수다.** 필기가 주석으로 그 규칙을 적어 두었다 — 「default 값을 지정하지 않으면 필수 프로퍼티가 된다. 즉 애노테이션을 사용할 때 반드시 값을 지정해야 한다」·「default 값이 있으면, 애노테이션을 사용할 때 값을 지정하지 않아도 된다」. 그래서 `@MyAnnotation` 을 값 없이 쓰면 **컴파일 오류**이고 `@MyAnnotation2` 는 통한다 → [[interface]] · [[default-method]]

그리고 **애노테이션을 만드는 순간 두 가지를 더 정해야 한다** — 어디까지 남길지와 어디에 붙게 할지. 둘 다 애노테이션 위에 애노테이션을 붙여 정한다 → [[annotation-retention]] · [[annotation-target]]

## 사용 예시

`@Override` 는 컴파일러에게 재정의 의도를 알린다.

```java
public class Exam0300 {
  public static void main(String[] args) {
    System.out.println("애노테이션");
  }

  @Override
  public String toString() {
    return "Exam12";
  }
}
```

`toString()` 은 원래 `java.lang.Object` 에 있는 메서드다 → [[inheritance]]. `@Override` 를 붙였으니 **정말 부모에 그 메서드가 있는지 컴파일러가 확인**해 준다. 이름을 `toStrng` 으로 잘못 쓰면 재정의가 아니라 새 메서드가 되는데, 애노테이션이 있으면 그 자리에서 컴파일 오류가 난다 → [[method-overriding]]

### 「부모」가 무엇인지는 나중 회차에서 채워진다

Day06 시점에는 `Exam0300` 이 아무것도 `extends` 하지 않았는데 `@Override` 가 통과하는 것이 설명되지 않는다. **`extends` 를 쓰지 않아도 부모가 `java.lang.Object` 라는 것**을 배우는 자리가 뒤에 있고, 거기서 이 예제가 왜 컴파일되는지가 닫힌다 → [[object-class]]

그 회차에서 `@Override` 가 실제로 네 번 쓰이며, 필기가 값을 이렇게 적어 뒀다.

```java
// 개발을 하다 보면 인스턴스의 현재 값을 간단히 확인하고 싶을 경우가 있다.
// 그럴 경우 toString()을 오버라이딩 하라!

//override를 한다고 컴파일러에게 알려주면 오타로 인한 버그를 줄일수 있다.
@Override
public String toString() {
  return "My [name=" + name + ", age=" + age + "]";
}
```

```java
@Override
public boolean equals(Object obj) { ... }        // 매개변수 타입이 Object 여야 한다
```

**두 번째 쪽에서 얻는 것이 오타 방지보다 크다.** `equals(My obj)` 로 편하게 쓰면 이름은 맞는데 매개변수가 달라 **재정의가 아니라 새 메서드**가 되고, 컴파일도 실행도 되면서 `HashSet` 은 계속 부모 것을 부른다. 오타는 눈으로 보이지만 이쪽은 보이지 않으므로, `@Override` 가 잡아 주는 실수 중 **정말 필요한 것은 이쪽**이다 → [[object-equality]]

### 붙는 자리가 선언 하나에서 타입 전체로 넓어진다

Day36 의 `@FunctionalInterface` 는 **인터페이스 선언**에 붙는다.

```java
//함수형 인터페이스 구현
@FunctionalInterface
interface Player{
    void play();
}
```

검사하는 것도 그 선언 하나가 아니라 **타입이 지켜야 하는 조건**이다 — 「이 인터페이스의 추상메서드는 하나뿐이다」. `@Override` 가 「이 메서드는 정말 재정의인가」를 묻는 것과 방향이 같고 범위가 다르다 → [[functional-interface]]

| | `@Override` | `@FunctionalInterface` |
|---|---|---|
| 붙는 곳 | 메서드 선언 | 인터페이스 선언 |
| 검사 내용 | 부모에 그 선언이 있나 | 추상메서드가 하나인가 |
| 안 붙이면 | 재정의는 성립하고 오타를 놓친다 | 람다는 그대로 되고 **나중에 깨질 위치가 옮겨간다** |

**둘 다 없어도 코드는 동작한다는 것이 이 둘의 공통점이다.** Day36 자신이 그 증거를 남겼다 — `Player` 에만 애노테이션을 붙이고 `Intro`·`InterestCalculator` 에는 안 붙였는데 셋 다 람다로 쓴다.

### 붙는 자리의 전체 목록 — 그리고 안 되는 자리 하나

Day60 이 직접 만든 애노테이션 하나를 놓을 수 있는 데 다 놓아 경계를 그렸다.

```java
@MyAnnotation // 클래스 선언에 붙일 수 있다.
public class Exam0110 {

  @MyAnnotation // 필드에 붙일 수 있다.
  static int a;

  @MyAnnotation int b; // 필드 선언 바로 앞에 둘 수 있다.

  @MyAnnotation // 메서드 선언에 붙일 수 있다.
  void m1(
      @MyAnnotation
      int p1, // 파라미터(로컬변수)에 붙일 수 있다.

      @MyAnnotation String p2
      ) {

    @MyAnnotation int local; // 로컬변수 선언에 붙일 수 있다.

    //@MyAnnotation System.out.println("okok"); // 그러나 다른 일반 문장에는 붙일 수 없다.

    for (int i = 0; i < 100; i++) {
      @MyAnnotation int a; // 로컬 변수 선언에 붙일 수 있다.
    }
  }

  @MyAnnotation  // static, non-static 상관없이 메서드 선언에 붙일 수 있다.
  static void m2() {

  }
}
```

**규칙 하나로 줄어든다 — 선언에는 붙고 문장에는 못 붙는다.** 주석으로 막아 둔 `System.out.println("okok")` 이 그 경계선이고, `static` 인지 아닌지는 상관없고 줄을 바꾸든 같은 줄에 두든(`@MyAnnotation int b;`) 상관없다. **애노테이션이 가리키는 것은 코드가 하는 일이 아니라 「이름이 붙은 무엇」**이라는 뜻이다 → [[variable-scope]] · [[static-member]] · [[expression-vs-statement]]

이 예제의 `@MyAnnotation` 이 다섯 자리에 다 붙는 것은 자유롭게 만들었기 때문이 아니라 **붙는 자리를 제한하지 않았기 때문**이다 — 그 제한을 적는 문법이 같은 노트의 뒷부분에 따로 있다 → [[annotation-target]]

## 왜 중요한가

**의도를 코드에 적어 두면 기계가 검사해 준다.** 주석으로 "이건 재정의다"라고 써 두면 아무도 확인하지 않지만, `@Override` 로 쓰면 컴파일러가 확인한다. 검사받는 설명과 검사받지 않는 설명의 차이가 이것이다.

**그리고 검사받을 값이 있는 자리는 「틀려도 동작하는」 자리다.** 재정의를 놓치면 오류가 나지 않고 상속받은 기본 구현이 조용히 실행된다. `@Override` 는 그 조용함을 깨는 장치이고, 그래서 **재정의에는 붙이고 새 메서드에는 붙일 수 없다**는 비대칭이 생긴다.

그리고 이 방식이 Java 프레임워크의 기본 문법이 된다. 설정을 별도 파일에 쓰지 않고 **선언 옆에 붙여 두면 프레임워크가 읽어 동작을 정하는** 구조가 여기서 출발한다.

**만들 수 있게 되면 그 「검사받는 설명」을 내가 정의할 수 있다.** Day06~36 에서는 컴파일러가 아는 애노테이션(`@Override`·`@FunctionalInterface`)만 쓸 수 있었으므로 검사받을 수 있는 것도 그 둘이 아는 것뿐이었다. `@interface` 를 쓸 수 있게 되면 **내 프로그램이 읽을 표시를 내가 만들고**, 그것을 읽는 코드를 내가 쓴다. 그 순간 필요해지는 것이 「어디까지 남기나」와 「어디에 붙나」와 「어떻게 읽나」 셋이고, Day60 의 나머지 절들이 정확히 그 셋이다 → [[annotation-retention]] · [[annotation-target]] · [[reflective-annotation-access]]

**그래서 이 문법이 XML 설정과 경쟁 관계에 놓인다.** 같은 회차 앞부분의 MyBatis 설정이 「이 클래스를 `user` 라 부르라」를 XML 에 적었는데, 애노테이션으로 하면 그 말이 클래스 선언 위에 온다. **설정이 파일 한 곳에 모이는 것**과 **설정이 대상 옆에 붙는 것**의 갈림이고, 어느 쪽이 나은지가 정해져 있지 않다 — 전자는 한눈에 보이고 후자는 대상과 어긋날 수 없다 → [[type-alias]] · [[xml]]

## 경계와 오해

- **애노테이션 ≠ 주석** — 이름과 생김새 때문에 주석으로 묶기 쉽지만, 주석의 정의는 "컴파일 시 무시된다"이고 애노테이션은 무시되지 않는다. 옛 필기가 애노테이션을 주석의 한 종류로 분류하면서 동시에 "컴파일러나 JVM 에서 사용할 주석"이라 적었는데, 그 두 문장은 함께 성립할 수 없다. **읽는 주체가 있으면 주석이 아니다.**
- **그 분류 오류가 82일 뒤에도 그대로 반복된다** — Day60 의 「annotation 정의」가 다시 「클래스, 필드, 메서드, 로컬 변수 선언에 붙이는 특별한 주석이다」·「다른 주석과 달리 컴파일이나 실행할 때 추출할 수 있다」로 시작한다. 두 문장 중 뒤쪽이 앞쪽을 부정하는 구조까지 Day06 과 같다. **그런데 같은 회차가 애노테이션을 직접 만들고 `getAnnotation` 으로 값을 꺼내 출력하기까지 한다** — 즉 「추출할 수 있는 주석」이라는 표현이 남아 있는 채로 그것을 읽는 코드를 쓴 상태다. 세 회차 걸쳐 남은 이 낱말이 실제로 방해가 되는 자리는 **`SOURCE` 정책**이다: 그것만이 정말로 「컴파일할 때 제거되는」 것이고 나머지 둘은 아니므로, 「주석이니까 컴파일하면 사라지겠지」로 읽으면 기본값이 `CLASS` 라는 사실과 어긋난다 → [[comment]] · [[annotation-retention]]
- **애노테이션이 코드를 바꾸는 것은 아니다** — 스스로 동작하지 않는다. 누군가(컴파일러·프레임워크)가 그것을 읽고 무엇을 할지 정해야 효과가 생긴다. 그래서 아무도 안 읽는 애노테이션은 정말 아무 일도 하지 않는다.
- **읽는 시점이 애노테이션마다 다르다** — `@Override` 는 컴파일할 때만 쓰이고 실행 시점에는 남지 않는다. 실행 중에 읽히는 것도 따로 있다.
- **`@Override` 는 오버라이딩을 만들지 않는다** — 붙이면 재정의가 되는 것이 아니라, **이미 재정의인지 검사**할 뿐이다. 반대로 안 붙여도 선언부가 맞으면 재정의는 성립한다. 「이 애노테이션이 동작을 정한다」로 읽으면 애노테이션이 코드를 바꾸지 않는다는 위 항목과 어긋난다 → [[method-overriding]]
- **`@FunctionalInterface` 도 무엇을 만들어 주지 않는다 — 오류가 날 위치를 바꾼다** — `@Override` 가 오버라이딩을 만들지 않는 것과 같은 자리다. 붙였다고 함수형 인터페이스가 되는 것이 아니고(조건은 추상메서드가 하나인 것), 안 붙였다고 람다를 못 쓰는 것도 아니다. 바뀌는 것은 **약속을 깨는 변경이 어디서 걸리는가**다 — 붙였으면 추상메서드를 하나 더 넣는 순간 그 인터페이스 파일에서 오류가 나고, 안 붙였으면 인터페이스는 통과하고 **그것을 람다로 쓴 자리 전부**가 깨진다. 필기가 「이러한 인터페이스를 함수형 인터페이스라고 부르며, 어노테이션은 @FunctionalInterface라고 한다」로 둘을 한 문장에 묶어 애노테이션이 조건처럼 읽히는데, **같은 노트가 애노테이션 없는 함수형 인터페이스를 둘 쓴다** → [[functional-interface]] · [[lambda-expression]]
- **애노테이션을 붙일 수 없는 자리도 있다 — 람다 몸통이 그렇다** — 람다는 추상메서드를 채우지만 `@Override` 를 붙일 문법 자리가 없다(이름도 반환 타입도 없는 식이다). 같은 일을 익명 클래스로 쓰면 `@Override` 가 붙는다. **「재정의에는 애노테이션을 붙인다」는 습관이 통하지 않는 첫 문법**이고, 그 검사를 여기서는 컴파일러가 대입되는 타입으로 대신한다 → [[lambda-expression]] · [[anonymous-class]]
- **실행 중에 읽는 쪽이 쓰는 도구가 따로 있다** — 애노테이션을 「누군가 읽어야 효과가 생긴다」고 하는데, 그 읽는 경로가 `Class` 객체다. 프레임워크가 설정을 선언 옆에 붙여 두고 동작하는 구조의 나머지 절반이 그것이다 → [[class-metadata]] · [[reflective-annotation-access]]
- **「읽는 시점이 애노테이션마다 다르다」가 Day60 에서 선언 문법이 된다** — Day06 기준으로는 관찰이었다(`@Override` 는 실행 시점에 남지 않는다). Day60 의 `@Retention` 은 **내가 만드는 애노테이션에 대해 그것을 정하는** 자리이고, 기본값이 「실행 중에 안 보인다」쪽이라는 것이 만드는 사람에게는 함정이 된다 → [[annotation-retention]]
- **`@interface` 는 `interface` 의 한 종류인데 할 수 있는 일이 훨씬 적다** — `implements` 로 구현하지 않고, `extends` 로 상속하지도 못한다(암묵적으로 `java.lang.annotation.Annotation` 을 상속한 상태로 고정이다). 그래서 **공통 프로퍼티를 부모 애노테이션에 모아 두는 형태가 불가능**하고, 비슷한 애노테이션 다섯 개가 같은 프로퍼티를 각각 다시 선언한다. 이름이 `interface` 라서 [[inheritance]]·[[interface]] 에서 배운 것이 그대로 통할 것 같은데 그 두 축이 다 막혀 있다.
- **프로퍼티는 「메서드처럼 선언한다」이지 메서드가 아니다** — 몸통(`{ … }`)을 쓸 수 없고, 매개변수를 받을 수 없고, `throws` 를 붙일 수 없다. 값을 계산해서 돌려주는 것이 아니라 **붙일 때 적어 둔 상수를 되읽는 것**이기 때문이다. 「인터페이스니까 추상 메서드다」로 읽으면 구현할 곳을 찾게 되는데, 구현하는 주체는 컴파일러와 JVM 이다 → [[method]] · [[abstract-class]]
- **`value` 이름을 생략할 수 있는 조건은 「프로퍼티가 하나」가 아니다** — 필기가 「property가 여러개 일 경우 키와 값을 정확하게 명시해야한다」로 적었는데, 정확히는 **값을 하나만 지정하고 그것이 `value` 일 때** 생략할 수 있다. 프로퍼티가 둘이어도 나머지에 `default` 가 있으면 `@MyAnnotation3("값")` 이 통한다. 「여러 개면 무조건 이름을 다 쓴다」로 외우면 `@RequestMapping("/users")` 처럼 프로퍼티가 열 개인데 이름 없이 쓰는 형태를 만났을 때 설명되지 않는다.
- **「순서는 상관없다」가 생성자와 갈리는 지점이다** — 프로퍼티는 이름으로 지목하므로 `@Myannotation3(tel="tel", value="값")` 이 통한다. 위치로 짝지어지는 [[constructor]] 인수와 정반대이고, 그래서 **프로퍼티를 나중에 추가해도 기존 사용처가 깨지지 않는다** — 단, `default` 를 함께 주었을 때만이다. `default` 없는 프로퍼티를 추가하면 **그 애노테이션을 쓰던 모든 자리가 한꺼번에 컴파일 오류**가 된다. 라이브러리 쪽 애노테이션에 프로퍼티가 늘어날 때 `default` 가 거의 항상 붙어 있는 이유가 이것이다 → [[parameter-and-argument]]
- **애노테이션을 만들었다고 아무 일도 일어나지 않는다 — 위의 「스스로 동작하지 않는다」가 만드는 쪽에서 더 크다** — 붙이는 쪽은 최소한 컴파일러가 아는 애노테이션을 쓰지만, 내가 만든 것은 **아는 주체가 하나도 없는 상태로 태어난다.** 읽는 코드를 쓰기 전까지는 붙여도 붙이지 않아도 프로그램이 똑같이 동작하고, 그것이 정상이다 → [[reflective-annotation-access]]

## 함께 보는 개념

- [[lombok]] — 애노테이션이 컴파일 시점에 코드를 만드는 사례

- [[comment]] — 생김새가 비슷하지만 무시되는 쪽
- [[method-overriding]] — `@Override` 가 검사해 주는 것
- [[javadoc]] — 별도 도구가 읽는 주석 (컴파일러가 읽는 애노테이션과 갈린다)
- [[object-class]] — `@Override` 가 참조할 부모가 언제나 있는 이유
- [[object-equality]] — 매개변수 타입 사고를 잡아 주는 자리
- [[class-metadata]] — 실행 중에 애노테이션을 읽는 경로
- [[functional-interface]] — `@FunctionalInterface` 가 검사하는 조건
- [[lambda-expression]] — 애노테이션을 붙일 자리가 없어지는 문법
- [[annotation-retention]] — 만들 때 정하는 「어디까지 남기나」
- [[annotation-target]] — 만들 때 정하는 「어디에 붙나」
- [[reflective-annotation-access]] — 붙여 둔 것을 실제로 읽는 쪽
- [[interface]] · [[abstract-class]] — `@interface` 가 속하면서 대부분 못 하는 것
- [[constructor]] · [[parameter-and-argument]] — 이름으로 지목하는 것과 순서로 짝짓는 것
- [[expression-vs-statement]] — 애노테이션이 붙을 수 없는 자리의 기준
- [[type-alias]] · [[xml]] — 같은 설정을 파일에 적는 경쟁 방식

## 출처

- [[2024-10-21-Day98]] — **애노테이션이 읽히는 세 번째 시점이 나온다.** 지금까지는 실행 중에 리플렉션으로 읽는 것(`RUNTIME`)만 봤는데, Lombok 은 **컴파일 중간**에 애노테이션 프로세서가 읽어 **소스에 없던 메서드를 `.class` 에 넣는다.** 필기가 「gradle 의 `compileOnly`/`annotationProcessor` 설정으로 작업하는 중간 컴파일 과정이 있고 그 과정에서 Lombok 이 메서드들을 추가해 준다」로 그 구조를 짚었다 → [[lombok]] · [[annotation-retention]]
- [[2024-05-31-Day06]] — `@애노테이션명(프로퍼티명=값)` 문법과 `@Override`·`@SuppressWarnings` 예시, 그리고 컴파일러나 JVM 이 사용한다는 성질을 배웠다
- [[2024-06-24-Day21]] — `toString`·`equals`·`hashCode`·`clone` 을 재정의하며 `@Override` 를 실제로 네 번 쓰고, 「override를 한다고 컴파일러에게 알려주면 오타로 인한 버그를 줄일수 있다」를 필기에 남겼다. Day06 예제가 아무것도 `extends` 하지 않고도 `@Override public String toString()` 이 통과한 이유(암묵 `Object` 상속)가 이 회차에서 채워지고, 오타보다 큰 값이 **매개변수 타입을 틀린 `equals`** 를 잡는 데 있다는 것도 여기서 드러난다
- [[2024-07-16-Day36]] — `@FunctionalInterface` 가 나오면서 애노테이션이 붙는 자리가 **메서드 선언에서 타입 선언으로** 넓어진다. 검사 대상도 「이 선언이 재정의인가」에서 「이 인터페이스의 추상메서드가 하나인가」로 바뀌지만 성질은 같다 — 붙여도 아무것도 만들어 주지 않고, 조건이 깨질 때 **오류가 날 위치만 옮긴다.** 필기는 「어노테이션은 @FunctionalInterface라고 한다」로 애노테이션을 함수형 인터페이스의 조건처럼 적었는데, **같은 회차가 애노테이션 없는 `Intro`·`InterestCalculator` 를 람다로 쓴다.** 그리고 같은 장에서 람다 몸통에는 `@Override` 를 붙일 자리가 아예 없어지는 것도 보인다 — 익명 클래스 버전에는 붙어 있던 것이 람다 버전에서 사라진다
- [[2024-08-21-Day60]] — 82일 뒤, **붙이는 쪽에서 만드는 쪽으로 넘어가는 회차**다. 「annotation 정의」·「annotation 사용」·「annotation property 정의」·「property」 네 절이 `public @interface MyAnnotation { String value(); }` 라는 선언 문법과 프로퍼티 규칙을 세운다 — 「인터페이스에서 메서드 이름은 property(변수)로 작성한다」, `default` 가 없으면 필수·있으면 선택, 값 하나면 `value` 이름 생략 가능(`@MyAnnotation("값2")`), 둘 이상이면 이름을 다 적고 **순서는 무관**. 「annotation 사용」 절의 `Exam0110` 예제가 클래스·필드·메서드·매개변수·지역 변수 다섯 자리에 같은 애노테이션을 붙여 보이고 **일반 문장에는 붙일 수 없다**는 것을 주석으로 막아 표시해, 「선언에 붙는다」는 규칙이 코드로 확인된다. 같은 회차의 나머지 절들이 만드는 쪽에 필요한 셋을 이어 다룬다 → [[annotation-retention]] · [[annotation-target]] · [[reflective-annotation-access]]. 다만 정의가 다시 「특별한 주석이다」로 시작해 **Day06 의 분류 오류가 그대로 반복되고**, `@interface` 가 상속·구현이 안 된다는 것·프로퍼티에 쓸 수 있는 타입이 제한된다는 것·`default` 없는 프로퍼티를 나중에 추가하면 기존 사용처가 전부 깨진다는 것은 다루지 않았다. 「property 정의」 절과 「property」 절이 같은 내용을 두 번 다루면서 예제 애노테이션 이름(`MyAnnotation`·`MyAnnotation2`·`MyAnnotation3`)이 절마다 다른 선언으로 재사용된다
