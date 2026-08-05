---
type: concept
id: reflective-instantiation
title: 리플렉션 객체 생성 (Constructor 와 newInstance)
aliases:
  - newInstance
  - Constructor 객체
  - getConstructor
  - getConstructors
  - 동적 객체 생성
  - 기본 생성자 요구
up:
  - 2024-08-20-Day59
tags:
  - java
  - 리플렉션
  - 생성자
  - 실행시점
---

# 리플렉션 객체 생성 (Constructor 와 newInstance)

**`new` 를 쓰지 않고, 실행 중에 고른 클래스에서 실행 중에 고른 생성자로 인스턴스를 만드는 것.** `new Exam03(200)` 은 클래스와 생성자가 코드에 박히지만, `clazz.getConstructor(int.class).newInstance(200)` 은 **둘 다 값이다.** Day59 가 그 순서를 한 줄로 적었다 — 「객체를 생성하기 위해서는 클래스호출, 생성자 호출, 인스턴스호출 순으로 이루어진다」 → [[class-loading]] · [[class-metadata]]

## 정의

세 걸음이고, 필기의 그 한 줄이 정확히 셋을 가른다.

| 걸음 | 코드 | 손에 들어오는 것 |
|---|---|---|
| ① 클래스 | `Class<?> clazz = Exam03.class;` 또는 `Class.forName("...")` | `Class` — 아직 인스턴스는 없다 |
| ② 생성자 | `Constructor<?> c = clazz.getConstructor(int.class);` | `Constructor` — 여전히 인스턴스는 없다 |
| ③ 인스턴스 | `Exam03 obj = (Exam03) c.newInstance(200);` | 객체 |

생성자를 고르는 규칙은 메서드를 고르는 규칙과 같다 — **파라미터 타입 목록**이 생성자를 지목한다. 이름이 없는 대신 그것만으로 구분되므로, 인수 없는 생성자는 `getConstructor()` 다 → [[reflective-invocation]] · [[constructor]]

목록으로 훑을 수도 있다.

```java
Constructor<?>[] list = clazz.getConstructors();
for (Constructor<?> c : list) {
  System.out.printf("%s(%d)\n", c.getName(), c.getParameterCount());
}
```

Day59 가 이 코드로 확인한 대상은 생성자 셋을 가진 클래스다.

```java
public Exam01() {}
public Exam01(int i) {}
public Exam01(String s, int i) {}
```

**출력은 `Exam01(0)`·`Exam01(1)`·`Exam01(2)` 다** — 이름이 셋 다 같고 개수만 다르다. 생성자를 구분하는 것이 이름이 아니라는 사실이 출력에 그대로 드러난다.

## 사용 예시

Day59 의 「생성자 호출」 예제가 **기본 생성자가 없을 때 무엇이 깨지는지**를 보인다.

```java
public class Exam03 {
  int value;

  public Exam03(int i) {
    this.value = i;
  }

  public void print() {
    System.out.printf("value=%d\n", this.value);
  }

  public static void main(String[] args) throws Exception {
    Class<?> clazz = Exam03.class;

    // newInstance()는 객체를 생성한 후 기본 생성자를 호출한다.
    // Exam03은 기본 생성자가 없기 때문에 실행 오류가 발생한다!
    //    Exam03 obj0 = (Exam03) clazz.newInstance(); // 실행 오류!

    // 해결=> 생성자를 준비한다.
    Constructor<?> c = clazz.getConstructor(int.class);

    // 생성자 객체를 통해 인스턴스를 생성해야 한다.
    Exam03 obj = (Exam03) c.newInstance(200);
    obj.print();
  }
}
```

**주석으로 막은 줄과 살아 있는 줄이 각각 다른 메서드다** — 위는 `Class.newInstance()`(기본 생성자 고정), 아래는 `Constructor.newInstance(…)`(고른 생성자). 이름이 같아서 한 메서드로 보이는데 사는 클래스가 다르다(아래 「경계와 오해」).

그리고 같은 회차의 필드 절이 이 셋 중 ②③ 을 실제로 쓴다 — **객체를 만들고 나서 필드를 채우는 형태**다.

```java
Constructor<Car> defaultConst = (Constructor<Car>) clazz.getConstructor();
Car car = defaultConst.newInstance();
// ... setAccessible(true) 후 private 필드에 값 넣기
```

**이 두 줄과 필드 절의 세 줄을 합치면 매퍼가 하는 일 전체다** → [[reflective-field-access]]

## 왜 중요한가

**프레임워크가 기본 생성자를 요구하는 이유가 여기서 설명된다.** MyBatis 의 `resultType="bitcamp.myapp.vo.User"` 는 XML 안의 **문자열**이므로 MyBatis 는 그 클래스를 컴파일할 때 몰랐고, 어떤 인수를 어떤 순서로 넘겨야 하는지 알 방법도 없다. **아무것도 모른 채 만들 수 있는 유일한 생성자가 인수 없는 것**이라, 프레임워크들이 그것을 요구한다 — JPA 엔티티·Jackson·Gson 이 전부 같은 이유다. Day59 의 주석(「기본 생성자가 없기 때문에 실행 오류」)이 그 규칙의 근거를 코드로 보여 준다 → [[mybatis]] · [[json]] · [[class-loading]]

**그리고 「어느 구현을 쓸지」를 설정으로 옮길 수 있다.** 클래스 이름이 문자열이고 생성이 리플렉션이면 자바 코드는 인터페이스만 알면 되고, 어느 구현체를 만들지는 설정 파일이 정한다. Day56 의 드라이버 등록에서 시작해 이 회차의 `mybatis-config.xml` 까지 같은 장치다 → [[dependency-injection]] · [[interface]] · [[xml]]

**대신 「이 클래스가 어디서 만들어지나」를 코드에서 찾을 수 없게 된다.** `new User()` 를 검색해도 아무것도 나오지 않는데 객체는 만들어져 있다. 생성자에 넣어 둔 검증이나 로그가 도는 것도 이 경로로는 눈에 안 보인다 → [[refactoring]]

## 경계와 오해

- **`clazz.newInstance()` ≠ `constructor.newInstance()`** — 이름이 같고 사는 클래스가 다르다. 앞은 `Class` 의 메서드로 **기본 생성자만** 부르고, 뒤는 `Constructor` 의 메서드로 **그 생성자**를 부른다. 필기가 앞의 것이 실행 오류라는 사실은 정확히 짚었지만 둘이 다른 클래스의 메서드라는 것은 적지 않아서, 「인수를 넘기면 되는 건가」로 읽히기 쉽다. 그리고 **`Class.newInstance()` 는 Java 9 부터 deprecated 다** — 생성자가 던진 검사 예외를 `throws` 선언 없이 그대로 흘려보내서 컴파일러의 예외 검사를 우회하기 때문이고, 권장 대체가 정확히 `clazz.getDeclaredConstructor().newInstance()` 다 → [[exception-handling]]
- **`c.getName()` 은 생성자 이름이 아니라 클래스 이름이다** — 필기 코드가 `c.getName()` 을 찍어 `Exam01` 이 나오므로 「생성자 이름 = 클래스 이름이라 맞다」로 읽히는데, `Constructor.getName()` 은 **언제나** 선언 클래스의 이름을 돌려준다(생성자에는 이름이 없다). `Method.getName()` 과 같은 뜻으로 읽으면 어긋나며, 실제로 이 출력에서 셋을 구분해 주는 것은 이름이 아니라 `getParameterCount()` 다 → [[reflective-invocation]]
- **`getParameterCount()` 는 「메서드의 파라미터 갯수」가 아니다** — 필기의 설명 줄인데, 이 코드에서 부른 대상은 생성자다. `Method` 와 `Constructor` 의 공통 부모(`Executable`)에 있는 메서드라 양쪽에서 쓸 수 있고, 그래서 설명이 틀린 것은 아니지만 **이 절에서 세고 있는 것은 생성자의 파라미터**다.
- **`getConstructors()` 는 `public` 만 준다 — 그리고 그 사실이 싱글톤을 뚫는 구멍이다** — 전부 보려면 `getDeclaredConstructors()` 이고, `private` 생성자를 부르려면 `setAccessible(true)` 다. 즉 **생성자를 `private` 로 감춘 싱글톤도 리플렉션으로는 인스턴스가 둘이 된다** — 「생성자를 막았으니 하나뿐이다」가 실행 시점의 보장이 아니라는 뜻이고, `enum` 싱글톤이 권장되는 이유가 이것이다(JVM 이 `enum` 의 리플렉션 생성을 거부한다) → [[singleton-pattern]] · [[reflective-field-access]] · [[access-modifier]]
- **기본 생성자는 「없으면 만들어진다」가 아니다** — 생성자를 하나라도 직접 쓰면 컴파일러가 넣어 주던 것이 사라진다. `Exam03` 이 `Exam03(int)` 를 쓴 순간 인수 없는 생성자가 없어졌고, 그것이 `clazz.newInstance()` 가 실패한 이유 전체다. 필기는 결과만 적고 그 규칙은 적지 않았다 → [[constructor]]
- **생성자 목록의 순서는 보장되지 않는다** — 명세가 「특정 순서가 아니다」로 못 박았다. 「인수가 적은 것부터 나오겠지」로 골라 쓰면 JVM 을 바꿨을 때 다른 생성자가 잡힌다. 고르려면 파라미터 타입으로 지목하는 것이 유일한 방법이다.
- **생성자 안에서 터진 예외는 `InvocationTargetException` 으로 감싸여 온다** — `newInstance` 는 이 밖에도 `NoSuchMethodException`(그런 생성자가 없다)·`InstantiationException`(추상 클래스나 인터페이스다)·`IllegalAccessException`(접근 범위) 네 갈래를 던지고, 필기는 `main` 에 `throws Exception` 을 달아 넷을 뭉쳐 넘긴다. **원인마다 고칠 곳이 다른데 한 이름으로 올라오면 진단이 늦는다** → [[exception-handling]] · [[abstract-class]]
- **`(Exam03) c.newInstance(200)` 의 캐스팅은 받는 타입 때문에 생겼다** — `Class<?>` 에서 얻은 `Constructor<?>` 는 `Object` 를 돌려주므로 캐스팅이 필요하다. `Class<Exam03> clazz = Exam03.class;` 로 받으면 `Constructor<Exam03>` 이 오고 캐스팅이 사라진다. 같은 회차의 필드 절이 `(Constructor<Car>)` unchecked 캐스팅으로 같은 자리에서 걸렸다 — **`Class` 를 raw 나 `?` 로 받는 습관이 리플렉션 코드 전체에 캐스팅을 뿌린다** → [[generics]] · [[raw-type]] · [[type-casting]]
- **배열은 이 통로로 만들 수 없다** — 배열에는 생성자가 없어서 `Array.newInstance(원소타입, 길이)` 를 쓴다. 한 달 전 Day40 이 `new T[10]` 이 안 되는 것을 그 메서드로 우회한 자리가 그것이고, **같은 「실행 시점 타입으로 만든다」인데 API 가 갈린다** → [[type-erasure]] · [[array]]
- **로딩만으로는 인스턴스가 생기지 않는다 — 이 절이 같은 회차의 오류를 반증한다** — 첫 절이 「객체를 인스턴스 하는 것이 클래스 로딩이며」라고 적었는데, 여기서 세 걸음을 나열한 것이 그것과 부딪힌다. ① 이 로딩이고 ③ 이 인스턴스화이므로 **둘은 같은 걸음이 아니다.** 한 필기 안에 답이 들어 있는 자리다 → [[class-loading]] · [[instance]]
- **「클래스호출」·「인스턴스호출」이라는 말은 없다** — 필기의 표현인데 클래스는 호출되지 않고(로딩된다) 인스턴스도 호출되지 않는다(생성된다). 호출되는 것은 생성자 하나뿐이다. 낱말이 어긋난 것이지만, **세 걸음을 갈랐다는 점에서는 이 문장이 그 절의 가장 정확한 한 줄이다.**
- **인수 없는 생성자를 요구하는 것과 「그 객체가 쓸 수 있는 상태인가」는 다르다** — 필수 값을 생성자로 받던 클래스를 프레임워크에 맞추려고 빈 생성자를 추가하면, **불완전한 객체가 만들어질 수 있는 통로**가 하나 열린다. 그래서 그 생성자를 `protected` 로 좁히거나(JPA 의 관례) 매퍼가 필드를 채운 뒤에만 쓰이도록 두는 규율이 붙는다 — **프레임워크의 요구가 도메인 클래스의 설계를 바꾸는 자리**다 → [[encapsulation]] · [[reflective-field-access]]

## 함께 보는 개념

- [[class-loading]] — 첫 걸음. 클래스를 문자열로 지목하는 자리
- [[class-metadata]] — 생성자를 꺼내는 출발점
- [[reflective-invocation]] — 같은 규칙으로 메서드를 고르는 짝
- [[reflective-field-access]] — 만든 객체를 채우는 다음 걸음
- [[constructor]] — 기본 생성자가 사라지는 규칙
- [[singleton-pattern]] — `private` 생성자가 이 통로로 뚫리는 자리
- [[dependency-injection]] — 「어느 구현을 만들지」를 밖으로 옮기는 이름
- [[mybatis]] · [[json]] — 이 통로로 객체를 만드는 실물
- [[type-erasure]] · [[array]] — 배열은 다른 API 로 만들어야 하는 이유
- [[generics]] · [[raw-type]] — 캐스팅이 생기고 사라지는 자리
- [[exception-handling]] — 네 갈래 실패가 한 이름으로 올라오는 자리
- [[abstract-class]] · [[interface]] — 만들 수 없는 대상
- [[instance]] — 로딩과 갈리는 걸음
- [[access-modifier]] — `getConstructors()` 가 걸러 내는 것

## 출처

- [[2024-08-20-Day59]] — 「생성자 정보 추출」 절에서 `getConstructors()` + `getParameterCount()` 로 생성자 셋을 훑고, 「생성자 호출」에서 **기본 생성자가 없는 클래스에 `clazz.newInstance()` 를 부르면 실행 오류**라는 것과 `getConstructor(int.class)` 로 생성자를 골라 `c.newInstance(200)` 하는 해법을 코드로 보였다. 「객체를 생성하기 위해서는 클래스호출, 생성자 호출, 인스턴스호출 순으로 이루어진다」는 한 줄이 로딩·생성자 선택·인스턴스화를 셋으로 가른 것이고, 그것이 같은 필기 첫 절의 「객체를 인스턴스 하는 것이 클래스 로딩이며」를 스스로 반증한다. 같은 회차의 필드 절이 `clazz.getConstructor()` + `newInstance()` 로 `Car` 를 만든 뒤 `private` 필드를 채우므로 **객체를 만들고 채우는 두 걸음이 한 노트 안에 다 있다.** 다만 `Class.newInstance()` 와 `Constructor.newInstance()` 가 다른 클래스의 메서드라는 것·전자가 deprecated 라는 것·`c.getName()` 이 클래스 이름이라는 것·`getConstructors()` 가 `public` 만 준다는 것·`InvocationTargetException` 은 다루지 않았다
