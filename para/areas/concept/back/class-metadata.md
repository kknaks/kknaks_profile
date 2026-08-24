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
  - 2024-08-20-Day59
  - 2024-08-21-Day60
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

이름을 꺼내는 방법이 **넷**이다. Day21 이 앞의 둘을 쓰고, 두 달 뒤 Day59 가 뒤의 둘을 더한다.

| 메서드 | 중첩 클래스에서의 결과 | 쓰는 자리 |
|---|---|---|
| `getName()` | `com.eomcs.basic.ex01.Exam0160$My` | 클래스를 유일하게 지목할 때 — **[[class-loading]] 에 넣는 이름이 이것이다** |
| `getSimpleName()` | `My` | 사람에게 보여 줄 때 |
| `getCanonicalName()` | `com.eomcs.basic.ex01.Exam0160.My` | 소스에 적는 표기. **익명·로컬 클래스에서는 `null`** |
| `getTypeName()` | `com.eomcs.basic.ex01.Exam0160$My` | `getName()` 과 같다 — **배열에서만 갈린다** |

Day59 가 그 넷을 한 코드에서 나란히 찍어 갈림을 보였다 — 「`getCanonicalName()` : "."으로 정규화된 클래스 전체 이름 추출」·「`getTypeName()` : 클래스 타입을 기분으로 전체 이름 추출」(「기분」은 **기준**의 오기다).

```java
class A {}
Class<?> clazz = Class.forName("com.eomcs.reflect.ex02.Exam0110$A");
System.out.println(clazz2.getSimpleName());     // A
System.out.println(clazz2.getName());           // com.eomcs.reflect.ex02.Exam01$A
System.out.println(clazz2.getCanonicalName());  // com.eomcs.reflect.ex02.Exam01.A
System.out.println(clazz2.getTypeName());       // com.eomcs.reflect.ex02.Exam01$A
```

**`$` 와 `.` 이 갈리는 그 한 글자가 로딩에 쓸 수 있는 이름과 못 쓰는 이름을 가른다** → [[class-loading]] · [[nested-class]]

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

**「Day06 의 애노테이션을 읽는 그 누군가」가 하는 일이 이 세 줄이다** — 클래스를 열지 않고 밖에서 구조를 보고 결정한다. 다만 여기서 읽는 것은 인터페이스와 메서드이고 **애노테이션을 실제로 읽는 코드는 아직 나오지 않았다** — 그것이 Day60 이다 → [[annotation]] · [[reflective-annotation-access]]

### 29일 뒤 Day59 — 이 객체가 아는 것을 통째로 훑는다

Day21 은 이름, Day40 은 인터페이스 하나와 메서드 하나였다. **Day59 는 「Reflection API」라는 이름을 붙이고 이 객체가 답할 수 있는 것을 목록으로 만든다.**

| 묻는 것 | 메서드 | 갈리는 짝 |
|---|---|---|
| 이름 | `getSimpleName`·`getName`·`getCanonicalName`·`getTypeName` | 위 「정의」 |
| 부모 | `getSuperclass()` | — |
| 중첩 클래스 | `getClasses()` | `getDeclaredClasses()` |
| 구현 인터페이스 | `getInterfaces()` | — |
| 메서드 | `getMethods()` | `getDeclaredMethods()` → [[reflective-invocation]] |
| 필드 | — | `getDeclaredFields()` → [[reflective-field-access]] |
| 생성자 | `getConstructors()` | `getDeclaredConstructors()` → [[reflective-instantiation]] |
| 지정자 | `getModifiers()` | → [[modifier-flags]] |
| **애노테이션** | `getAnnotation(X.class)`·`getAnnotations()` | `getDeclaredAnnotations()` → [[reflective-annotation-access]] |

**`get*` 과 `getDeclared*` 라는 짝이 자리마다 반복되는 것이 이 API 의 규칙이다** — 앞은 「상속 포함, `public` 만」이고 뒤는 「이 클래스만, 전부」다. Day59 가 그 규칙을 메서드 자리에서만 말로 적었고(「선언된 public 메서드 + 상속받은 Public 메서드」), 중첩 클래스 자리에서는 같은 짝을 코드로만 보인다.

**표의 마지막 줄만 그 규칙을 따르지 않는다 — 그것을 하루 뒤 Day60 이 더한다.** 처음에는 이 짝을 「이 API 의 **유일한** 규칙」이라고 적었는데, 애노테이션 자리에서는 갈리는 축이 다르다(아래 「경계와 오해」) → [[reflective-annotation-access]]

```java
Class<?> superClazz = clazz.getSuperclass();
System.out.println(superClazz.getName());
System.out.println(superClazz.getSuperclass().getName());
```

```java
// public 으로 공개된 중첩 클래스 및 인터페이스 정보를 가져온다.
Class<?>[] nestedList = clazz.getClasses();

// 접근 범위에 상관 없이 모든 중첩 클래스 및 인터페이스 정보를 가져온다.
// => 메서드 안에 정의된 로컬 클래스는 대상이 아니다.
Class<?>[] nestedList2 = clazz.getDeclaredClasses();
```

**`getInterfaces()` 에 대해 Day59 가 한 줄을 더한다** — 「구현한 인터페이스의 수퍼 클래스 정보는 가져오지 않는다」. 한 달 전 Day40 의 `initSeqNo` 복원이 조용히 건너뛰어지던 원인(아래 「경계와 오해」)을 필기가 **뒤늦게 이 자리에서 적은 셈**이다 → [[interface]]

그리고 컬렉션에 담긴 값들의 타입을 알아내는 형태가 나온다.

```java
ArrayList<Object> values = new ArrayList<>();
values.add(100);
values.add(3.14f);
values.add(true);
values.add(new int[] {100, 200, 300});

for (Object value : values) {
   printTypeInfo(value.getClass());
}

private static void printTypeInfo(Class<?> type) {
  if (type.getName().startsWith("[")) {
    System.out.printf("=> %s[]\n", type.getComponentType().getName());
  } else {
    System.out.printf("=> %s\n", type.getName());
  }
}
```

**절 이름이 「Collection 값의 타입」인데 하는 일은 「원소를 꺼내 그 인스턴스의 클래스를 묻는 것」이다.** `ArrayList<Object>` 의 타입 인자는 실행 시점에 없으므로 **꺼내 보는 것이 유일한 길**이고, 그래서 원소가 하나도 없으면 알 방법도 없다 — Day40 이 `Class<E>` 를 매개변수로 받아 우회한 그 벽이다 → [[type-erasure]]

## 왜 중요한가

**타입이 컴파일 시점의 이야기에서 실행 시점의 값이 된다.** 변수의 선언 타입은 컴파일러만 아는 것이고, `getClass()` 가 돌려주는 것은 **코드가 들고 다니며 비교하고 넘길 수 있는 객체**다. 그래서 「같은 클래스인지」를 `if` 로 물을 수 있고, 클래스 이름을 문자열로 찍을 수 있다.

**그리고 이 자리에서 프레임워크로 가는 길이 열린다.** 애노테이션을 읽고, 이름으로 클래스를 찾아 인스턴스를 만들고, 필드 목록을 훑는 일이 전부 `Class` 를 통해서 이뤄진다. Day06 에서 「누군가 애노테이션을 읽어야 효과가 생긴다」고 배웠는데, **그 「누군가」가 쓰는 도구**가 여기다 → [[annotation]]

**Day60 에서 그 문장이 두 줄의 코드로 닫힌다.** `clazz.getAnnotation(MyAnnotation.class)` 로 표시를 꺼내고 `obj.v1()` 로 값을 읽는 것 — Day21 에서 「읽는 주체가 있으면 주석이 아니다」로 갈라 둔 그 주체가 **내가 쓴 코드**가 되는 자리다. 그리고 이 갈래만 **중개 객체가 아니라 애노테이션 타입 자체를 돌려주므로** 반환값에 캐스팅이 없다 → [[reflective-annotation-access]] · [[generics]]

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
- **`getName()` 과 `getTypeName()` 은 배열에서만 갈린다 — 그런데 Day59 의 배열 절이 `getName()` 만 써서 그것을 스스로 보이지 못했다** — 중첩 클래스에서는 둘 다 `Exam01$A` 라 같아 보이는데, `Date[].class.getName()` 은 `[Ljava.sql.Date;` 이고 `getTypeName()` 은 **`java.sql.Date[]`** 다. 즉 「배열의 타입 및 값의 타입」 절이 디스크립터 표기를 읽어 내려고 `getComponentType()` 을 부르는 그 노동이 **`getTypeName()` 한 번으로 끝난다.** 같은 필기의 두 절이 각각 한 메서드씩 쓰면서 서로를 대신할 수 있다는 것을 놓친 자리다.
- **`getCanonicalName()` 이 준 이름으로는 클래스를 로딩할 수 없다** — 중첩 클래스의 정규명은 `...Exam01.A`(점)이고 [[class-loading]] 이 요구하는 이름은 `...Exam01$A`(달러)다. **Day59 가 같은 코드에서 `forName("…$A")` 로 로딩하고 바로 아래에서 정규명을 출력하면서 이 대비를 말하지 않았다** — 사람에게 보여 줄 이름과 기계에 넣을 이름이 갈리며, 후자는 `getName()` 이다.
- **필기의 「익명클래스의 경우」 항목이 두 사실을 한 문장에 섞었다** — 「익명클래스의 경우 CanonicalName은 null 이지만 TypeName,Name은 $n으로 표시된다」의 앞은 맞고(익명·로컬 클래스는 정규명이 없다), 뒤는 익명 클래스의 이름이 `Exam01$1`·`$2` 처럼 **번호**라는 뜻이면 맞다. 그런데 **붙어 있는 예시의 `A` 는 익명 클래스가 아니라 중첩 클래스**이고 그 이름은 번호가 아니라 `$A` 다. 로컬 클래스는 또 달라서 `$1A` 형태이고 정규명도 `null` 이다 — **세 종류(중첩·로컬·익명)가 각각 다른데 한 항목이 되어 있다** → [[nested-class]] · [[anonymous-class]]
- **`superClazz.getSuperclass().getName()` 은 부모가 `Object` 이면 터진다** — Day59 의 「수퍼클래스 정보」 코드가 두 단을 연달아 부르는데, `Object` 의 부모는 `null` 이라 그 줄이 `NullPointerException` 이다. 그리고 `null` 을 돌려주는 경우가 셋 더 있다 — **인터페이스**(`List.class.getSuperclass()`), **기본 타입**(`int.class`), `Object` 자신. 배열은 예외적으로 `Object` 를 준다. **상속 사슬을 훑으려면 `while (c != null)` 이어야 하고**, 두 줄 연달아 부르는 형태는 「부모가 하나 더 있다」는 가정을 코드에 박아 넣은 것이다 → [[inheritance]] · [[object-class]]
- **`getClasses()` 도 상속을 포함한다 — 필기가 메서드 쪽에서만 그것을 짚었다** — 「Class.forName으로 호출한 class에 중첩된 class 정보를 리턴한다」로 적혀 있어 **이 클래스에 선언한 것만** 주는 것처럼 읽히는데, `getMethods()` 와 같은 규칙이라 **부모의 `public` 중첩 클래스도 목록에 들어온다.** 같은 짝(`get*`/`getDeclared*`)이 자리마다 같은 뜻이라는 것을 알면 이 오해가 생기지 않는다 → [[reflective-invocation]]
- **`get*`/`getDeclared*` 짝의 뜻이 애노테이션 자리에서 처음 어긋난다 — Day60 기준으로** — 다른 자리들에서는 축이 둘이었다(상속 포함 여부 · `public` 만인지). 애노테이션에는 **접근 지정자라는 것이 아예 없으므로** 둘째 축이 사라지고, 남은 상속 축조차 조건부다 — 부모 클래스의 애노테이션이 `getAnnotations()` 에 나오는 것은 그 애노테이션이 `@Inherited` 로 선언되었을 때뿐이고 인터페이스에서는 물려받지 않는다. **모양이 같은 짝이니 뜻도 같을 것이라고 읽으면 여기서 처음 틀리며**, 그래서 위 표의 규칙은 「자리마다 반복되지만 자리마다 같은 뜻은 아니다」로 고쳐 읽어야 한다 → [[reflective-annotation-access]] · [[inheritance]] · [[access-modifier]]
- **`getDeclaredClasses()` 가 빼는 것은 로컬 클래스만이 아니다** — 필기가 「클래스 안에 선언 메소드에 정의된 로컬 클래스는 대상이 아니다」로 적었는데 **익명 클래스도 빠진다.** 둘 다 「멤버」가 아니기 때문이고, 그래서 [[nested-class]] 의 네 종류 중 **멤버 클래스 둘만** 이 목록에 나온다 → [[anonymous-class]]
- **`getComponentType()` 대신 `isArray()` 가 있다** — Day59 의 `printTypeInfo` 가 `type.getName().startsWith("[")` 로 배열을 판정한다. 결과는 맞지만 **디스크립터 표기의 첫 글자에 기대는 것**이고, `Class.isArray()` 가 같은 답을 준다. 「문자열의 모양으로 타입을 판정한다」는 형태가 남으면 표기가 바뀌는 날 조용히 깨진다.
- **`values.add(100)` 이 `java.lang.Integer` 로 찍히는 것은 오토박싱이다** — Day59 의 컬렉션 예제가 기본 타입 리터럴을 담는데, 출력은 `int` 가 아니라 `Integer`·`Long`·`Float`·`Boolean`·`Character` 다. **`int.class` 와 `Integer.class` 는 서로 다른 `Class` 인스턴스**이므로, 위 「기본 타입은 `getClass()` 를 부를 수 없다」와 이 결과를 함께 보면 「담긴 순간 다른 타입이 됐다」는 사실이 드러난다 → [[autoboxing]] · [[wrapper-class]]
- **출력이 `java.sql.Date` 인 것은 `import` 가 정한 결과다** — Day59 의 배열 예제가 `Date` 를 쓰고 `java.sql.Date` 로 찍힌다. 리플렉션이 보는 것은 **컴파일된 실제 타입**이라, `java.util.Date` 를 `import` 했다면 같은 코드가 다른 이름을 찍는다. 이름이 같은 두 클래스가 두 패키지에 있는 것이 이 API 에서 결과를 갈라 놓는 자리다 → [[package]] · [[prepared-statement]]
- **필기의 「getComponetType()」은 오기다** — 주석 줄에만 그렇게 적혀 있고 실제 코드는 `getComponentType()` 이다.
- **필기 4.1 코드 블록은 클래스를 닫지 않은 채로 잘려 있다** — `main` 의 닫는 중괄호와 클래스의 닫는 중괄호가 없다.
- **Day59 의 이름 예제는 `clazz` 를 선언하고 `clazz2` 를 쓴다 — 그리고 클래스 이름이 두 값으로 갈려 있다** — `Class<?> clazz = Class.forName("…Exam0110$A");` 인데 출력 줄은 전부 `clazz2.` 라 컴파일되지 않고, 인수는 `Exam0110$A` 인데 주석의 기대 출력은 `Exam01$A` 다. **어느 쪽이 맞는지 필기 안에서 결정되지 않는다.** 컬렉션 예제도 `main` 과 클래스의 닫는 중괄호가 없이 잘려 있다.
- **필기의 「배열은 ```[b``` 처럼」은 소문자가 오기다** — `byte[]` 의 디스크립터는 **`[B`** 이고 소문자 `b` 인 디스크립터는 존재하지 않는다. 위의 `[B`·`[I`·`[Z` 항목과 같은 표기다.

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
- [[class-loading]] — 이 객체를 문자열 이름으로 얻는 통로
- [[reflective-invocation]] · [[reflective-field-access]] · [[reflective-instantiation]] · [[reflective-annotation-access]] — 이 객체에서 갈라져 나오는 네 갈래
- [[modifier-flags]] — 이 객체가 지정자를 정수로 돌려주는 자리
- [[autoboxing]] · [[wrapper-class]] — 담긴 순간 타입이 바뀌는 자리
- [[mybatis]] — 이 객체 위에 서 있는 프레임워크

## 출처

- [[2024-06-24-Day21]] — `getClass()` 로 `Class` 인스턴스를 받아 `getName()`·`getSimpleName()` 으로 이름을 꺼내고, 기본 타입은 `Object` 의 서브클래스가 아니라 `byte.class` 형태를 써야 한다는 것, 배열의 클래스 이름이 `[Ljava.lang.String;`·`[B` 형태로 나오고 원소 타입은 `getComponentType()` 으로 얻는다는 것을 배웠다. 같은 회차의 `equals` 재정의가 `getClass() != obj.getClass()` 로 이 객체를 쓴다
- [[2024-07-22-Day40]] — `Class` 가 **읽는 대상에서 넘기고 부리는 값**이 된다. 제네릭 메서드 `loadJson(List<E> list, String filename, Class<E> elementType)` 가 `User.class`·`Board.class` 를 인수로 받고, `Array.newInstance(type, 10)` 로 실행 시점 타입 정보로 배열을 만들며, `getComponentType()` 으로 견본 배열에서 원소 타입을 꺼낸다. `elementType.getInterfaces()` 로 구현 인터페이스를 확인하고 `getMethod("initSeqNo", int.class)` + `invoke(null, maxSeqNo)` 로 **이름으로 찾은 `static` 메서드를 호출**한다 — 이 노트에서 처음 나오는 「읽기가 아닌 리플렉션」이다. Day21 의 raw `Class` 가 여기서는 `Class<?>`·`Class<E>` 로 적혀 있다. 필기는 `getInterfaces()` 가 직접 구현한 인터페이스만 준다는 것과 `getMethod` 가 실행 시점에만 검증된다는 것은 다루지 않았다
- [[2024-08-20-Day59]] — 29일 뒤. 「Reflection API」라는 이름이 붙고 **이 객체가 답할 수 있는 것이 목록이 된다.** 이름을 꺼내는 방법이 넷으로 늘고(`getCanonicalName`·`getTypeName` 이 여기서 추가된다), `getSuperclass()` 로 부모를, `getClasses()`/`getDeclaredClasses()` 로 중첩 클래스를, `getInterfaces()` 로 구현 인터페이스를 꺼내며, 메서드·필드·생성자·지정자로 갈라지는 절들이 뒤따른다 — **`get*` 과 `getDeclared*` 라는 짝이 자리마다 반복된다는 것이 이 회차에서 보이는 규칙**이고, 필기가 그것을 메서드 자리에서만 말로 적었다. `getInterfaces()` 에 대한 「구현한 인터페이스의 수퍼 클래스 정보는 가져오지 않는다」 한 줄은 Day40 의 `initSeqNo` 복원이 조용히 건너뛰어질 수 있던 원인을 뒤늦게 짚은 자리다. 컬렉션에 담긴 값들의 타입은 **원소를 꺼내 `value.getClass()`** 로만 알 수 있다는 것도 이 회차의 것이다. 다만 이름 예제가 `clazz` 를 선언하고 `clazz2` 를 써서 컴파일되지 않고 클래스 이름이 `Exam0110$A`/`Exam01$A` 두 값으로 갈리며, 「익명클래스」 항목의 예시가 실제로는 중첩 클래스이고, `superClazz.getSuperclass().getName()` 은 부모가 `Object` 이면 `NullPointerException` 이며, `getName()` 과 `getTypeName()` 이 배열에서만 갈린다는 것과 `isArray()` 의 존재는 다루지 않았다 → [[class-loading]] · [[reflective-invocation]] · [[reflective-field-access]] · [[reflective-instantiation]] · [[modifier-flags]]
- [[2024-08-21-Day60]] — 하루 뒤. **이 객체가 답하는 것에 애노테이션이 더해지고, 그 갈래만 다른 셋과 다르게 생겼다.** 「property 추출」 절이 `clazz.getAnnotation(MyAnnotation.class)` 로 클래스에 붙은 애노테이션을 꺼내 `obj.v1()`·`obj.v2()`·`obj.v3()` 로 프로퍼티 값을 읽는데, 돌려받는 것이 `Method`·`Field`·`Constructor` 같은 **중개 객체가 아니라 애노테이션 타입 그 자체**라 캐스팅도 `Object` 도 나오지 않는다 — Day40 의 `Class<E> elementType` 이 보였던 「인수와 반환을 제네릭으로 묶는」 형태를 표준 API 가 쓴 자리다. Day21 이 「읽는 주체가 있으면 주석이 아니다」로 갈라 두고 Day40 이 「애노테이션을 읽는 그 누군가」로 예고한 코드가 **여기서 실제로 나온다.** 그리고 `getAnnotations()`/`getDeclaredAnnotations()` 는 Day59 에서 본 짝과 모양이 같으면서 **갈리는 축이 다르다**(접근 지정자 축이 없고 상속은 `@Inherited` 조건부) — 그래서 「짝이 자리마다 같은 뜻」이라는 읽기가 이 자리에서 처음 깨진다. 다만 필기는 `Class` 에서만 꺼내고 `Method`·`Field` 에서도 같은 메서드를 쓸 수 있다는 것·`null` 이 오는 경우들·돌려받은 객체가 프록시라는 것은 다루지 않았다 → [[reflective-annotation-access]] · [[annotation-retention]] · [[annotation-target]]
