---
type: concept
id: object-class
title: Object 클래스 (java.lang.Object)
aliases:
  - Object 클래스
  - 오브젝트 클래스
  - java.lang.Object
  - 최상위 클래스
  - root class
  - object class
up:
  - 2024-06-24-Day21
tags:
  - java
  - 객체지향
  - 상속
  - 표준라이브러리
---

# Object 클래스 (java.lang.Object)

상속 계층의 **뿌리**. `extends` 를 한 번도 쓰지 않은 클래스도 이미 여기를 상속하고 있고, 그래서 **내가 만든 모든 클래스에 처음부터 메서드 여섯 개가 들어 있다.**

## 정의

컴파일러가 부모를 채워 넣는다.

```java
public class Exam0110 /*extends Object*/ {
  static class My /*extends Object*/ {
  }
}
```

주석으로 적힌 `extends Object` 가 **실제로 거기 있는 것**이다. 아무것도 쓰지 않으면 컴파일러가 자동으로 넣는다 → [[inheritance]]

그래서 어떤 클래스든 아래 여섯 개를 물려받은 상태로 시작한다.

| 메서드 | 하는 일 | 기본 구현이 주는 것 |
|---|---|---|
| `toString()` | 클래스 이름과 해시코드를 리턴 | `패키지명.클래스@16진수해시값` |
| `equals()` | 같은 인스턴스인지 검사 | 주소 비교 (`==` 와 같다) |
| `hashCode()` | 인스턴스를 식별하는 값을 리턴 | 인스턴스마다 다른 `int` |
| `getClass()` | 인스턴스의 클래스 정보를 리턴 | `Class` 인스턴스 |
| `clone()` | 인스턴스를 복제해 리턴 | 필드를 그대로 베낀 새 인스턴스 |
| `finalize()` | 가비지 컬렉터가 회수하기 직전에 호출 | 아무것도 하지 않는다 |

**여섯 개가 다 같은 자격은 아니다.** `toString`·`equals`·`hashCode` 는 재정의하라고 놓인 것이고, `getClass` 는 `final` 이라 재정의할 수 없고, `clone`·`finalize` 는 `protected` 라 밖에서 부를 수조차 없다 → [[access-modifier]]

## 사용 예시

`Object` 레퍼런스에 아무 인스턴스나 담을 수 있다는 것이 곧 상속의 증거다.

```java
Object obj = new My();
// Object의 레퍼런스에 My 인스턴스 주소를 저장할 수 있다는 것은
// My 클래스가 Object 크래스의 서브 클래스임을 증명하는 것이다.
System.out.println(obj instanceof My);      //true
System.out.println(obj instanceof String);  //false
System.out.println(obj instanceof Object);  //true
```

`My` 선언 어디에도 `Object` 라는 글자가 없는데 `instanceof Object` 가 `true` 다 → [[instanceof-operator]]

이 성질이 표준 라이브러리 곳곳에 그대로 쓰인다. 같은 회차의 `HashSet` 실습이 그것을 만난다.

```java
Object[] list = set.toArray();          // 무엇을 넣었든 Object[] 로 나온다
for (Object obj : list) {
  Student student = (Student) obj;       // 그래서 받는 쪽이 되돌려야 한다
  ...
}
```

**「모든 것을 받는 타입」이 있으려면 「모든 것의 조상」이 있어야 한다.** `Object` 가 그 자리다 → [[type-casting]] · [[hash-based-collection]]

## 왜 중요한가

**메서드를 새로 만드는 것이 아니라 이미 있는 것을 다시 쓰는 일이 된다.** 인스턴스 내용을 찍고 싶으면 `print()` 를 만드는 것이 아니라 `toString()` 을 재정의하고, 두 인스턴스를 비교하고 싶으면 `isSame()` 이 아니라 `equals()` 를 재정의한다. **이름을 내가 고르지 않는다는 것이 요점**이고, 그 대가로 `System.out.println(obj)` 와 `HashSet` 같은 남의 코드가 내 클래스를 다룰 수 있게 된다 → [[method-overriding]]

**그리고 「기본값이 있다」가 「쓸 만하다」는 뜻이 아니다.** 상속받은 여섯 개는 전부 동작하지만, `toString()` 은 해시값을 찍고 `equals()` 는 내용을 보지 않는다. 필기의 `Exam0120` 과 `Exam0121` 이 그 차이를 나란히 보여 준다 — **재정의하지 않아도 컴파일되고 실행되기 때문에** 잘못된 결과가 조용히 나온다.

## 경계와 오해

- **`Object` 클래스 ≠ 객체(object)** — 「객체」는 `new` 로 만들어진 것 일반을 가리키는 말이고 `Object` 는 클래스 하나의 **이름**이다. 한국어로 둘 다 「오브젝트」라 읽히므로 「모든 객체는 Object 다」 같은 문장이 두 뜻으로 갈린다. 앞의 것은 층의 이야기, 뒤의 것은 타입의 이야기다 → [[instance]]
- **모든 타입이 `Object` 의 서브클래스는 아니다** — 기본 타입 여덟 개는 아니다. 그래서 `int` 에는 `getClass()` 를 부를 수 없고 `Object` 변수에 담을 수도 없다. 반면 **배열은 서브클래스다** — `new int[10].getClass()` 가 동작한다. 「기본 타입은 아니지만 기본 타입 배열은 그렇다」가 걸리는 지점이다 → [[data-type]] · [[array]]
- **「Object 클래스와 링크된다」는 직접 상속을 뜻하지 않는다** — 필기의 표현인데, 중간에 부모가 있으면 `Object` 는 조부모다. `super_class` 자리에 `java/lang/Object` 가 들어가는 것은 아무것도 `extends` 하지 않았을 때뿐이고, 그래도 계층을 따라 올라가면 항상 `Object` 에 닿는다 → [[inheritance]] · [[class-file-format]]
- **여섯 개가 전부가 아니다** — 필기가 「주요 메서드」로 꼽은 목록이고, `wait`·`notify`·`notifyAll` 같은 것이 더 있다. 「Object 에는 여섯 개가 있다」로 외우면 목록이 닫힌 것으로 읽힌다.
- **`getClass()` 는 재정의할 수 없다** — `final` 이다. 나머지 다섯 개와 나란히 적혀 있어 같은 성질로 보이지만, 이것 하나가 못 바뀐다는 것이 `equals` 에서 `getClass()` 비교를 **믿을 수 있는 근거**다. 재정의할 수 있었다면 「같은 클래스인가」의 답을 상대가 조작할 수 있다 → [[object-equality]] · [[class-metadata]]
- **`finalize()` 가 「해제 직전에 호출된다」는 보장이 아니다** — 회수 시점 자체를 JVM 이 정하므로 **아예 불리지 않고 프로그램이 끝날 수 있다.** 자원 반납을 여기에 걸면 안 되는 이유이고, 그래서 Java 9 부터 폐기 예정으로 표시됐다. 필기의 한 줄을 「소멸자」로 읽으면 어긋난다 → [[garbage-collection]]
- **상속받았다고 코드가 복사된 것은 아니다** — 내 클래스의 `.class` 안에 `toString` 의 바이트코드가 들어가지는 않는다. 재정의하지 않으면 실행될 때 `Object` 의 것이 불린다 → [[inheritance]] · [[bytecode]]

## 함께 보는 개념

- [[inheritance]] — `extends` 없이도 성립하는 관계
- [[method-overriding]] — 물려받은 여섯 개를 쓸 만하게 만드는 일
- [[instanceof-operator]] — 이 상속을 코드로 증명하는 도구
- [[object-equality]] — `equals()` 를 재정의하는 자리
- [[hash-code]] — `hashCode()` 가 돌려주는 값
- [[class-metadata]] — `getClass()` 가 돌려주는 것
- [[object-cloning]] — `clone()` 이 하는 일
- [[garbage-collection]] — `finalize()` 가 걸려 있는 시점
- [[data-type]] — 이 계층 밖에 있는 여덟 개
- [[instance]] — 「객체」라는 말과 갈리는 자리
- [[access-modifier]] — 여섯 개의 자격이 갈리는 기준

## 출처

- [[2024-06-24-Day21]] — `extends` 를 쓰지 않아도 컴파일러가 `Object` 를 상속시킨다는 것을 `/*extends Object*/` 주석과 `instanceof` 로 확인하고, `toString`·`equals`·`hashCode`·`getClass`·`clone`·`finalize` 여섯 메서드를 목록으로 배웠다. 이 회차의 나머지 전부가 그 목록을 하나씩 재정의해 보는 실습이다
