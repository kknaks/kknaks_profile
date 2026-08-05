---
type: concept
id: class-metadata
title: 클래스 정보 객체 (getClass 와 java.lang.Class)
aliases:
  - 클래스 정보
  - Class 객체
  - getClass
  - class metadata
  - 리플렉션
  - reflection
  - 클래스 리터럴
up:
  - 2024-06-24-Day21
  - 2024-07-22-Day40
tags:
  - java
  - jvm
  - 타입
  - 표준라이브러리
---

# 클래스 정보 객체 (getClass 와 java.lang.Class)

실행 중에 **「이 인스턴스는 어떤 클래스인가」를 물어서 객체로 받는 것.** [[object-class]] 의 `getClass()` 가 `Class` 인스턴스를 돌려주고, 그 안에서 이름·원소 타입 같은 정보를 꺼낸다.

## 정의

```java
My obj1 = new My();
// 레퍼런스를 통해서 인스턴스의 클래스 정보를 알아낼 수 있다.
Class classInfo = obj1.getClass();
// 클래스 정보로부터 다양한 값을 꺼낼 수 있다.
System.out.println(classInfo.getName());        // 패키지명 + 바깥 클래스명 + 클래스명
System.out.println(classInfo.getSimpleName());  // 클래스명

//com.eomcs.basic.ex01.Exam0160$My
//My
```

이름을 꺼내는 방법이 둘로 갈린다.

| 메서드 | 결과 | 쓰는 자리 |
|---|---|---|
| `getName()` | `com.eomcs.basic.ex01.Exam0160$My` | 클래스를 유일하게 지목할 때 |
| `getSimpleName()` | `My` | 사람에게 보여 줄 때 |

**기본 타입은 `getClass()` 를 부를 수 없다.** `Object` 의 서브클래스가 아니라 물려받은 메서드가 없기 때문이고, 대신 `타입.class` 라는 문법이 있다.

```java
// Primitive Type은 Object의 서브 클래스가 아니기 때문에 getClass()를 호출할 수 없다.
// 대신 static 변수인 class 를 사용하여 Class 정보를 리턴 받을 수 있다.
Class classInfo = byte.class;
System.out.println(classInfo.getName());          //byte
System.out.println(int.class.getName());          //int
System.out.println(String.class.getName());       // java.lang.String
```

→ [[data-type]]

## 사용 예시

배열에도 클래스가 있고, 이름이 **사람이 쓰는 표기가 아니다.**

```java
String[] obj2 = new String[10];
Class classInfo = obj2.getClass();
System.out.println(classInfo.getName());                  //[Ljava.lang.String;

System.out.println(new byte[10].getClass().getName());     //[B
System.out.println(new int[10].getClass().getName());      //[I
System.out.println(new double[10].getClass().getName());   //[D
System.out.println(new boolean[10].getClass().getName());  //[Z
```

`[` 가 「배열」이고 뒤의 한 글자가 원소 타입이다. **`int[]` 가 `getClass()` 에 답한다는 것은 배열이 `Object` 의 서브클래스라는 뜻**이다 — 원소가 기본 타입이어도 배열 자체는 그렇다 → [[array]]

원소 타입은 따로 물어본다.

```java
// 배열 항목의 타입 정보를 가져온다.
Class compTypeInfo = classInfo.getComponentType();
System.out.println(compTypeInfo.getName());                            //java.lang.String
// [Ljava.lang.String -> java.lang.String -> java.lang.String
System.out.println(new int[10].getClass().getComponentType().getName()); //int
// [I -> int -> int
```

**한 겹을 벗기는 연산**이다. `[I` 에서 `int` 가 나오고, 그 결과는 `byte.class` 로 얻는 것과 같은 `Class` 다 → [[multidimensional-array]]

### 같은 회차의 equals 가 이것을 쓴다

```java
if (getClass() != obj.getClass()) {
  return false;
}
```

「같은 클래스인가」를 `Class` 인스턴스 **두 개를 `==` 로** 비교해서 판정한다. 이것이 성립하는 이유는 아래 「경계와 오해」의 첫 항목이다 → [[object-equality]]

### 한 달 뒤 — 이름을 읽는 것에서 만들고 부르는 것으로

Day21 은 `Class` 로 **이름을 꺼내는 것**까지였다. Day40 은 같은 객체로 **배열을 만들고 메서드를 부른다** — 그리고 그 이유가 새로 생긴다. 제네릭의 타입 파라미터가 실행 시점에 없으므로, **타입을 값으로 들고 다녀야** 하기 때문이다 → [[type-erasure]] · [[generics]]

`Class` 를 **매개변수로 받는 것**이 첫 걸음이다.

```java
  private <E> void loadJson(List<E> list, String filename, Class<E> elementType) { ... }
```

```java
    loadJson(userList, "user.json", User.class);
```

**`User.class` 가 인수 자리에 온다** — Day21 에서 `byte.class`·`String.class` 를 「이름을 꺼내려고」 썼던 그 문법이 여기서는 **넘기는 값**이다. `Class<E>` 라고 적혀 있어서 `loadJson(userList, "user.json", Board.class)` 는 컴파일되지 않는다 → [[generics]]

그리고 셋을 새로 한다.

```java
  // ① 실행 시점의 타입 정보로 배열을 만든다
  static <T> T[] create3(Class<?> type) {
    return (T[]) Array.newInstance(type, 10);
  }
```

```java
  // ② 이 클래스가 무엇을 구현했는지 물어본다
      for (Class<?> type : elementType.getInterfaces()) {
        if (type.equals(InitSeqNo.class)) {
          intintSeqNo(list, elementType);
        }
      }
```

```java
  // ③ 이름으로 메서드를 찾아 부른다
    Method method = elemnetType.getMethod("initSeqNo", int.class);
    method.invoke(null, maxSeqNo);
```

**③ 이 이 노트에서 처음 나오는 「읽기가 아닌 리플렉션」이다.** `getMethod` 의 첫 인수는 메서드 이름 **문자열**이고 뒤는 매개변수 타입 목록(`int.class` — Day21 의 클래스 리터럴이 여기 쓰인다), `invoke` 의 첫 인수 `null` 은 **`static` 메서드라 인스턴스가 필요 없다**는 표시다 → [[static-member]] · [[method]]

**「Day06 의 애노테이션을 읽는 그 누군가」가 하는 일이 이 세 줄이다** — 클래스를 열지 않고 밖에서 구조를 보고 결정한다 → [[annotation]]

## 왜 중요한가

**타입이 컴파일 시점의 이야기에서 실행 시점의 값이 된다.** 변수의 선언 타입은 컴파일러만 아는 것이고, `getClass()` 가 돌려주는 것은 **코드가 들고 다니며 비교하고 넘길 수 있는 객체**다. 그래서 「같은 클래스인지」를 `if` 로 물을 수 있고, 클래스 이름을 문자열로 찍을 수 있다.

**그리고 이 자리에서 프레임워크로 가는 길이 열린다.** 애노테이션을 읽고, 이름으로 클래스를 찾아 인스턴스를 만들고, 필드 목록을 훑는 일이 전부 `Class` 를 통해서 이뤄진다. Day06 에서 「누군가 애노테이션을 읽어야 효과가 생긴다」고 배웠는데, **그 「누군가」가 쓰는 도구**가 여기다 → [[annotation]]

## 경계와 오해

- **`Class` 인스턴스는 클래스마다 하나다** — 인스턴스마다 하나가 아니다. `My` 를 백 개 만들어도 `getClass()` 는 전부 같은 것을 돌려준다. 그래서 `equals` 의 `getClass() != obj.getClass()` 가 **`equals` 가 아니라 `==` 로** 비교해도 맞다. 「참조 타입은 `==` 로 비교하면 안 된다」의 예외처럼 보이는데, 여기서는 **정말로 같은 인스턴스인지**를 묻는 것이 맞는 질문이다 → [[object-reference]] · [[string-comparison]]
- **`getClass()` 는 재정의할 수 없다** — `final` 이다. 필기가 `toString`·`equals`·`hashCode` 와 나란히 놓아 같은 성질로 보이지만, 이것 하나가 못 바뀌는 덕분에 「같은 클래스인가」의 답을 상대가 조작할 수 없다. `equals` 안에서 신뢰할 수 있는 근거가 그것이다 → [[object-class]] · [[method-overriding]]
- **`byte.class` 는 「static 변수」가 아니다** — 필기의 표현인데 필드가 아니라 **클래스 리터럴**이라는 문법이다. `byte` 라는 타입에 `class` 라는 멤버가 있는 것이 아니므로 「필드니까 다른 필드도 있겠지」로 읽으면 어긋난다 → [[literal]]
- **`getName()` ≠ `getSimpleName()`** — `$` 가 붙은 쪽이 중첩 클래스를 나타내는 표기다. `Exam0160$My` 를 「Exam0160 의 My」로 읽어야 하고, 이 이름이 실제 `.class` 파일명(`Exam0160$My.class`)이기도 하다 → [[java-compilation-unit]]
- **`[Ljava.lang.String;` 은 사람이 쓰는 타입 이름이 아니다** — JVM 내부 표기(디스크립터)이고 `.class` 파일 안에 타입을 적어 두는 그 형식이다. `String[]` 이라고 찍히지 않는 것이 버그가 아니다. `[B`·`[I`·`[Z` 처럼 기본 타입은 한 글자로 줄고, 이름 끝의 `;` 도 표기의 일부다 → [[class-file-format]] · [[bytecode]]
- **`getComponentType()` 은 배열이 아니면 `null` 이다** — `String.class.getComponentType()` 은 예외가 아니라 `null` 을 준다. 「원소 타입을 준다」로만 외우면 `null` 검사를 빼먹는다 → [[object-reference]]
- **`Class classInfo` 는 raw type 이다 — 한 달 뒤 필기가 스스로 고친다** — Day21 은 전부 `Class classInfo` 로 쓰는데 그것은 타입 인자를 안 적은 상태이고 컴파일 경고가 난다. **Day40 에서는 `Class<?> type`·`Class<E> elementType` 로 바뀌어 있다** — 제네릭을 배우고 나서야 「그때 안 적었던 것」이 무엇인지 보이는 자리다. 동작은 같지만 `Class<E>` 쪽은 **목록과 타입 정보가 짝인지 컴파일러가 검사한다** → [[raw-type]] · [[generics]]
- **`getInterfaces()` 는 직접 구현한 것만 준다 — 상속받은 인터페이스는 빠진다** — Day40 의 `for (Class<?> type : elementType.getInterfaces())` 는 `Board` 가 `implements InitSeqNo` 라고 **직접 적었을 때만** 참이다. 부모 클래스가 구현하고 `Board` 가 그것을 상속했다면 목록에 없고, **조건문이 거짓이 되어 번호 발급기 복원이 조용히 건너뛰어진다** — 예외도 메시지도 없고 다음 등록에서 번호가 겹치는 것으로만 드러난다. 상속을 포함해 판정하려면 `InitSeqNo.class.isAssignableFrom(elementType)` 이나 `instanceof` 를 쓴다. **「구현했는가」와 「직접 적었는가」가 다른 질문** → [[interface]] · [[inheritance]] · [[instanceof-operator]] · [[surrogate-key]]
- **`getMethod` 는 이름을 문자열로 받으므로 컴파일러의 검사 밖이다** — `getMethod("initSeqNo", int.class)` 의 `"initSeqNo"` 를 IDE 의 이름 바꾸기가 따라오지 않고, 오타나 시그니처 불일치는 **실행 시점 `NoSuchMethodException`** 이다. 게다가 `getMethod` 는 `public` 만 찾는다(`getDeclaredMethod` 가 그 밖까지 본다). Day40 의 코드에서는 그 예외가 `loadJson` 의 `catch (Exception e)` 에 잡히므로 **데이터는 로딩된 채로 번호 복원만 실패한다** → [[exception-handling]] · [[access-modifier]]
- **인터페이스는 `static` 메서드의 존재를 강제할 수 없다 — 그래서 이 계약이 리플렉션에 남는다** — `InitSeqNo` 인터페이스가 요구할 수 있는 것은 인스턴스 메서드(`getNo()`)뿐이고, `static initSeqNo(int)` 는 **구현 클래스가 우연히 갖고 있기를 바라는 약속**이다. 타입으로 표현할 수 없는 계약이 있을 때 리플렉션이 그 자리를 메우고, **대가는 위반이 컴파일 시점에 안 잡힌다는 것**이다 → [[interface]] · [[static-member]]
- **`Array.newInstance` 로 만든 배열의 타입은 인수가 정하고, `(T[])` 캐스팅은 아무것도 검사하지 않는다** — `create3(Class<?> type)` 는 `T` 가 인수와 묶여 있지 않아 `String[] arr = create3(Integer.class);` 가 컴파일된 다음 **대입하는 줄에서** `ClassCastException` 을 낸다. `Class<T> type` 으로 받는 것이 답이다 — **리플렉션으로 타입을 넘기는 순간 타입 검사를 스스로 다시 세워야 한다** → [[type-erasure]] · [[generics]]
- **`type.equals(InitSeqNo.class)` 는 `==` 와 결과가 같다** — `Class` 는 `equals` 를 재정의하지 않으므로 동일성 비교다. 위의 「`Class` 인스턴스는 클래스마다 하나」가 그것을 성립시킨다 → [[object-equality]]
- **필기의 「getComponetType()」은 오기다** — 주석 줄에만 그렇게 적혀 있고 실제 코드는 `getComponentType()` 이다.
- **필기 4.1 코드 블록은 클래스를 닫지 않은 채로 잘려 있다** — `main` 의 닫는 중괄호와 클래스의 닫는 중괄호가 없다.

## 함께 보는 개념

- [[object-class]] — `getClass()` 가 물려 내려오는 곳
- [[object-equality]] — 「같은 클래스인가」를 쓰는 자리
- [[instanceof-operator]] — 같은 질문의 다른 답 방식
- [[data-type]] — `getClass()` 를 부를 수 없는 여덟 개
- [[array]] — 배열도 클래스를 갖는다는 것
- [[multidimensional-array]] — `getComponentType()` 이 한 겹씩 벗기는 구조
- [[class-file-format]] — `[Ljava.lang.String;` 표기가 사는 곳
- [[annotation]] — `Class` 를 통해 읽히는 것
- [[java-compilation-unit]] — `$` 가 붙은 이름과 파일의 관계
- [[literal]] — `byte.class` 의 정체
- [[jvm]] — 이 정보를 들고 있는 주체
- [[type-erasure]] — 타입을 값으로 들고 다녀야 하는 이유
- [[generics]] — `Class<E>` 로 타입 정보와 목록을 묶는 자리
- [[raw-type]] — `Class` 를 그냥 쓰던 옛 표기
- [[json]] — 리플렉션이 실제 일을 하게 된 실습

## 출처

- [[2024-06-24-Day21]] — `getClass()` 로 `Class` 인스턴스를 받아 `getName()`·`getSimpleName()` 으로 이름을 꺼내고, 기본 타입은 `Object` 의 서브클래스가 아니라 `byte.class` 형태를 써야 한다는 것, 배열의 클래스 이름이 `[Ljava.lang.String;`·`[B` 형태로 나오고 원소 타입은 `getComponentType()` 으로 얻는다는 것을 배웠다. 같은 회차의 `equals` 재정의가 `getClass() != obj.getClass()` 로 이 객체를 쓴다
- [[2024-07-22-Day40]] — `Class` 가 **읽는 대상에서 넘기고 부리는 값**이 된다. 제네릭 메서드 `loadJson(List<E> list, String filename, Class<E> elementType)` 가 `User.class`·`Board.class` 를 인수로 받고, `Array.newInstance(type, 10)` 로 실행 시점 타입 정보로 배열을 만들며, `getComponentType()` 으로 견본 배열에서 원소 타입을 꺼낸다. `elementType.getInterfaces()` 로 구현 인터페이스를 확인하고 `getMethod("initSeqNo", int.class)` + `invoke(null, maxSeqNo)` 로 **이름으로 찾은 `static` 메서드를 호출**한다 — 이 노트에서 처음 나오는 「읽기가 아닌 리플렉션」이다. Day21 의 raw `Class` 가 여기서는 `Class<?>`·`Class<E>` 로 적혀 있다. 필기는 `getInterfaces()` 가 직접 구현한 인터페이스만 준다는 것과 `getMethod` 가 실행 시점에만 검증된다는 것은 다루지 않았다
