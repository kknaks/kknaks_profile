---
type: concept
id: reflective-invocation
title: 리플렉션 메서드 호출 (Method 와 invoke)
aliases:
  - invoke
  - Method.invoke
  - Method 객체
  - 동적 메서드 호출
  - 메서드 동적 호출
  - getMethod
  - getMethods
  - getDeclaredMethod
  - getDeclaredMethods
up:
  - 2024-08-20-Day59
tags:
  - java
  - 리플렉션
  - 메서드
  - 실행시점
---

# 리플렉션 메서드 호출 (Method 와 invoke)

**메서드를 이름으로 찾아 객체로 손에 들고, 그 객체를 통해 호출하는 것.** `obj.minus(10, 20)` 이 컴파일할 때 정해지는 반면, `m.invoke(obj, 10, 20)` 은 **`m` 이 실행 중에 결정된다.** Day59 가 이것을 세 절에 걸쳐 다룬다 — 찾기(「메소드 정보 추출」) · 부르기(「메서드 호출」) · 시그니처 읽기(「타입정보 추출」) → [[class-metadata]] · [[class-loading]]

## 정의

찾는 메서드가 넷인데, 갈리는 축은 **둘**이다.

| | 상속받은 것 | 접근 범위 | 반환 |
|---|---|---|---|
| `getMethods()` | **포함** | `public` 만 | 목록 |
| `getDeclaredMethods()` | 제외 (이 클래스에 선언한 것만) | **전부** (`private` 까지) | 목록 |
| `getMethod("이름", 타입…)` | **포함** | `public` 만 | 하나 |
| `getDeclaredMethod("이름", 타입…)` | 제외 | **전부** | 하나 |

Day59 가 그 두 축을 각각 코드로 확인했다. 상속 축은 주석 한 줄이다 — 「`getMethods()` : 해당 클래스에 선언된 public 메서드 + 상속받은 Public 메서드」·「Object메서드도 가져온다」. 접근 축은 주석으로 막은 줄에 있다.

```java
// Method m0 = clazz.getMethod("m3"); // public이 아니기 때문에 못 찾는다.
Method m = clazz.getDeclaredMethod("m3"); // OK

// => 단 현재 클래스에 정의된 메서드를 찾는다.
System.out.println(clazz.getDeclaredMethod("toString")); // 예외 발생!
// 상속 받은 메서드는 못찾는다.
```

**표의 대각선이 이 두 줄이다.** `m3` 는 `private` 이라 `getMethod` 로 안 잡히고, `toString` 은 상속받은 것이라 `getDeclaredMethod` 로 안 잡힌다 — 그래서 **상속받은 `private` 메서드는 어느 쪽으로도 나오지 않는다**(애초에 상속되지 않는다) → [[access-modifier]] · [[inheritance]]

### 이름만으로는 메서드를 지목하지 못한다

오버로딩이 있으므로 **파라미터 타입 목록까지** 넘겨야 한다. Day59 가 그 규칙을 코드로 쌓아 올렸다.

```java
// 파라미터가 없는 메서드를 찾을 때는 파라미터의 타입 정보를 넘기지 않는다.
clazz.getMethod("m1");

// 파라미터가 있는 메서드를 찾을 때 그 파라미터의 타입 정보를 넘겨야 한다.
// 타입정보 = 클래스 정보 = Class 객체
Class<?> parameterType = String.class;
Method m = clazz.getMethod("m2", parameterType);
Method m2 = clazz.getMethod("m2", String.class);           // 위와 같다
m = clazz.getMethod("m2", Class.forName("java.lang.String")); // 이것도 같다

// byte,short,int,long,float,double,boolean,char 는 비록 클래스는 아니지만,
// 일반 클래스처럼 타입 정보를 꺼낼 수 있도록 "class"라는 스태틱 변수를 제공한다.
m = clazz.getMethod("m3", String.class, int.class);

// 메서드의 파라미터 순서를 지켜야 한다.
// m = clazz.getMethod("m3", int.class, String.class);   // 못 찾는다
```

**세 표기가 같은 인수라는 것이 이 절의 요점이다** — 변수에 담은 `Class`, 클래스 리터럴, `Class.forName` 의 결과가 전부 「타입 하나」를 가리키는 같은 값이다. 그리고 마지막 두 줄이 **찾는 것도 오버로딩 해석과 같은 규칙을 받는다**는 것을 보인다 → [[class-metadata]] · [[method]] · [[data-type]]

### 부르기 — 첫 인수가 「누구의 메서드인가」다

```java
m.invoke(대상, 인수…)
```

| 부르는 메서드 | 첫 인수 | Day59 의 표현 |
|---|---|---|
| `static` | **`null`** | 「스태틱 메서드는 인스턴스 생성이 필요 없으므로 바로 호출 할 수 있다」 |
| 인스턴스 | **그 인스턴스** | 「인스턴스 없이 invoke를 호출하면 NullPointException 에러가 발생한다」 |

```java
// static
Class<?> cls = ClassName.class;
Method m = cls.getMethod("methodName", parameterType*);
m.invoke(null, parameter*);
```

```java
// 인스턴스
Class<?> clazz = Exam0320.class;
Method m = clazz.getMethod("minus", int.class, int.class);

// => 인스턴스 메서드를 호출할 때는 반드시 인스턴스 주소를 넘겨야 한다.
Exam0320 obj = new Exam0320();
m.invoke(obj, 10, 20);   // 리플렉션 API를 사용하여 인스턴스 메서드 호출

// => 인스턴스 메서드를 호출하는 일반적인 방식
obj.minus(10, 20);
```

**두 줄을 나란히 놓은 것이 이 절의 값이다.** 아래 줄은 컴파일러가 `minus` 라는 메서드가 있는지 확인하고 인수 타입도 맞춰 주지만, 위 세 줄에서 컴파일러가 검사하는 것은 **`invoke` 라는 메서드가 있는가**뿐이다 → [[static-member]] · [[this-reference]]

### 시그니처를 되읽는 것도 같은 객체가 한다

```java
Method[] methods = clazz.getDeclaredMethods();
for (Method m : methods) {
  Parameter[] parameters = m.getParameters();   // 파라미터 목록
  for (Parameter p : parameters) {
    System.out.printf(" %s : %s\n", p.getName(), p.getType().getName());
  }
  Class<?> returnType = m.getReturnType();      // 리턴 타입
}
```

**여기서 나오는 값이 `getMethod` 에 넣는 값과 같은 종류다** — `p.getType()` 이 `Class` 이고 그것이 곧 `getMethod` 의 뒤 인수 자리에 서는 것이다. 즉 **메서드를 읽어 낸 결과로 다시 메서드를 찾을 수 있다.** 제네릭 반환형은 이 자리에서 따로 물어야 한다 → [[type-erasure]]

## 사용 예시

Day59 의 「메서드 파라미터」 절이 인수를 넘기는 두 형태를 나란히 적었다.

```java
// 파라미터 값을 낱개로 전달하기
m.invoke(null, "홍길동", 100, 90, 80);

// 파라미터 값을 배열에 담아서 전달할 수 있다.
m.invoke(null, new Object[] {"홍길동", 100, 100, 100});
```

**두 줄이 같은 뜻인 이유는 `invoke` 의 선언이 `invoke(Object obj, Object... args)` 라서다.** 위는 컴파일러가 배열을 만들어 주고 아래는 내가 만들어 준 것이며, 가변 인수 자리에 배열을 넘기면 **그 배열이 그대로 전달**된다 — Day17 의 `inputInt(format, args)`, 하루 전 Day58 의 `insert(sql, values)` 와 같은 성질이다 → [[varargs]]

그리고 Day59 가 그 성질의 **함정 쪽**을 두 줄로 적었다 — 「배열의 파라미터인 경우는 배열에 담아서 전달해야한다」·「가변 파라미터의 경우에도 배열에 담아서 전달해야한다」.

```java
// void m(int[] scores) 를 부르고 싶다
int[] scores = {100, 90, 80};
// m.invoke(null, scores);                   // int[] 는 Object[] 가 아니어서 그대로 간다 — 우연히 통한다
// m.invoke(null, new Object[]{"홍길동"});    // 인수 하나짜리로 펼쳐진다

// void m(Object[] values) 를 부르고 싶다면 반드시 감싼다
Object[] values = {"a", "b"};
m.invoke(null, new Object[]{ values });      // 인수 하나 = 그 배열
```

**같은 성질이 Day17·Day58 에서는 이득이었고 여기서는 함정이다.** 앞의 두 회차는 받은 배열을 다음 층으로 **그대로 흘려보내려** 했으므로 펼쳐지는 것이 원하는 동작이었고, `invoke` 에서는 **배열 하나를 값으로 주고 싶은 경우**가 생기므로 같은 규칙이 걸림돌이 된다 → [[varargs]] · [[array]]

## 왜 중요한가

**프레임워크가 남의 코드를 부르는 방법이 이것 하나다.** MyBatis 는 `bitcamp.myapp.vo.User` 라는 클래스를 컴파일할 때 몰랐는데도 `#{name}` 을 만나면 `getName()` 을 부른다 — 그 클래스를 `import` 한 적이 없으므로 **이름으로 찾아 부르는 것 말고는 길이 없다.** Day59 의 필기가 「resultType에서 setProperty(Object obj)를 호출하여 객체에 정보를 넣는다」로 적은 것이 이 절의 도구로 하는 일이다 → [[mybatis]] · [[reflective-field-access]]

**그리고 「타입으로 표현할 수 없는 계약」을 쓸 수 있게 된다.** 한 달 전 Day40 이 `getMethod("initSeqNo", int.class)` + `invoke(null, maxSeqNo)` 로 인터페이스가 강제할 수 없는 `static` 메서드를 불렀다. 인터페이스는 인스턴스 메서드만 요구할 수 있으므로, 그 밖의 약속은 **리플렉션으로만 확인하고 부를 수 있다** → [[class-metadata]] · [[interface]]

**대신 호출이 컴파일러의 시야에서 사라진다.** 「이 메서드를 부르는 곳 찾기」가 아무것도 찾지 못하고, 그래서 안 쓰는 것처럼 보이는 메서드가 지워지고, 이름을 바꾸면 실행 중에 터진다. `dispatch` 를 이름으로 하는 다른 방법([[dispatch-table]]·[[command-pattern]])은 **타입을 유지한 채** 같은 일을 하므로, 리플렉션은 그 방법들이 닿지 못하는 자리에만 쓰는 것이 규율이다 → [[refactoring]]

## 경계와 오해

- **`invoke` 의 반환값이 필기에 한 번도 나오지 않는다** — 예제가 전부 `m.invoke(obj, 10, 20);` 로 끝나므로 `minus` 가 계산한 값이 어디로도 가지 않는다. `invoke` 는 **`Object` 를 돌려준다** — `void` 면 `null`, 기본형이면 박싱된 값(`Integer`)이다. 즉 `int` 를 받으려면 `(int) m.invoke(...)` 로 되돌려야 하고, 그 캐스팅은 실행 시점에만 검사된다. **「호출했다」와 「결과를 받았다」가 갈리는 자리**이고, 리플렉션으로 무언가를 얻으려면 반드시 이쪽이 필요하다 → [[autoboxing]] · [[type-casting]]
- **`NullPointException` 은 오기이고, 그 예외가 나는 것은 맞다** — `NullPointerException` 이다. 인스턴스 메서드에 `invoke(null, …)` 을 하면 실제로 그것이 난다(호출할 대상이 없다) → [[exception-handling]]
- **대칭이 아니다 — `static` 메서드에 인스턴스를 넘겨도 통한다** — 필기는 「스태틱은 인스턴스가 필요 없다」·「인스턴스는 필요하다」를 짝처럼 적었지만, `static` 쪽은 **첫 인수를 무시한다.** `m.invoke(obj, …)` 로 `static` 메서드를 불러도 정상 동작한다. 그래서 「대상 인수가 `null` 인가」로 `static` 여부를 판정할 수 없고, 알고 싶으면 [[modifier-flags]] 를 물어야 한다.
- **부른 메서드가 던진 예외가 그대로 오지 않는다** — `InvocationTargetException` 에 감싸여 오고 진짜 원인은 `getCause()` 다. 그래서 `catch (SQLException e)` 로 잡으려 해도 안 잡히고, 스택트레이스가 한 겹 늘어 원인 줄이 아래로 밀린다. **리플렉션을 한 층 끼우면 예외의 타입이 바뀐다**는 것이 프레임워크 스택트레이스가 길어지는 이유이며, 「이 예외를 누가 던졌나」를 읽는 법이 달라진다 → [[exception-handling]]
- **`getMethod` 는 문자열을 받으므로 컴파일러 검사 밖이다 — 그리고 실패하는 방식이 셋이다** — 이름 오타·시그니처 불일치·접근 범위 미달이 전부 `NoSuchMethodException` 하나로 오므로, 메시지만 보면 「이름이 틀렸나 `private` 인가」를 구별할 수 없다. 필기의 `getDeclaredMethod("toString")` 이 그 셋 중 「이 클래스에 선언되지 않았다」 경우다. **`getDeclaredMethod` 로 다시 찾아 보면 갈린다**는 것이 실무의 진단법이고, 그때 나오면 접근 범위 문제였다는 뜻이다 → [[access-modifier]]
- **찾는 것과 부르는 것은 다른 벽이다** — `getDeclaredMethod("m3")` 로 `private` 메서드를 **찾을 수는 있어도** 그대로 `invoke` 하면 `IllegalAccessException` 이다. `m.setAccessible(true)` 가 필요하다. **Day59 는 `m3` 를 찾아 이름만 찍고 `invoke` 는 하지 않아서 이 벽에 닿지 않았다** — 같은 회차의 필드 절에서는 `setAccessible(true)` 를 쓰는데 메서드 절에서는 나오지 않는 비대칭이 그래서 생긴다 → [[reflective-field-access]] · [[encapsulation]]
- **가변 인수 메서드는 배열 타입으로 찾는다** — `void m(int... a)` 를 찾을 때는 `getMethod("m", int[].class)` 다. 선언의 `...` 는 컴파일 뒤에 배열이므로 시그니처에는 `...` 라는 것이 없다. 필기는 호출 쪽만 적고(「가변 파라미터의 경우에도 배열에 담아서 전달해야한다」) 찾는 쪽은 다루지 않았다 → [[varargs]]
- **`invoke(obj, null)` 은 「인수 없음」으로 읽힌다** — `null` 이 `Object[]` 로 해석되기 때문이다. 인수 하나로 `null` 을 넘기려면 `new Object[]{null}` 이어야 한다. [[varargs]] 노트가 「인수 하나로 `null` 을 넘기면 배열 자체가 `null` 이 된다」고 적은 것과 같은 문법인데, `invoke` 쪽에서는 그것이 오히려 **통하는 형태**(인수 없는 메서드 호출)라서 실수가 오류로 드러나지 않는다.
- **`getMethods()` 에 `Object` 의 메서드가 섞이는 것을 필기가 짚었다 — 그래서 목록을 쓰는 목적이 갈린다** — 「이 클래스가 무엇을 하는가」를 보려면 `getDeclaredMethods()` 이고, 「이 객체에 무엇을 부를 수 있는가」를 보려면 `getMethods()` 다. 앞의 것으로 화면을 만들면 상속받은 기능이 빠지고, 뒤의 것으로 만들면 `wait`·`notify`·`hashCode` 가 끼어든다 → [[object-class]] · [[inheritance]]
- **목록의 순서는 보장되지 않는다** — `getDeclaredMethods()` 가 소스의 선언 순서를 준다는 보장이 명세에 없다. 필기의 예제들은 순서를 쓰지 않으므로 문제가 없지만, 이 목록으로 화면 항목이나 파일 헤더를 만들면 **컴파일러나 JVM 을 바꿨을 때 순서가 달라진다** → [[reflective-field-access]]
- **파라미터 「이름」은 기본적으로 지워져 있다** — `p.getName()` 이 `name`·`age` 가 아니라 **`arg0`·`arg1`** 을 찍는다. 컴파일 옵션 `-parameters` 를 켜야 이름이 클래스 파일에 남는다. 필기의 「파라미터 타입」 예제 출력이 그 형태가 되며, **타입은 남고 이름만 지워지는 것**이라 [[type-erasure]] 와는 다른 축인데 증상이 닮았다. Spring 이 옛날에 `@Param`·`@RequestParam` 으로 이름을 다시 적게 했던 이유가 이것이다 → [[class-file-format]] · [[mybatis]]
- **`.class` 로 시작하는 코드는 「동적」이 아니다** — 이 절의 예제는 전부 `Exam0110.class`·`Exam0320.class` 로 클래스를 컴파일 시점에 적는다. 즉 메서드 이름만 문자열이고 클래스는 고정이라 **반쯤만 동적이다.** 진짜 동적 호출은 클래스 이름과 메서드 이름이 둘 다 밖에서 오는 것이고, 그 첫 칸이 같은 회차의 [[class-loading]] 절이다 — **두 절이 이어지는데 필기는 이어 붙이지 않았다.**
- **`getMethods()` 예제의 중괄호가 어긋나 있다** — `Class<?> clazz = Exam0110.class;` 다음 `for` 문이 끝난 뒤 `}` 가 하나 더 있어 그대로는 컴파일되지 않는다. 코드를 메서드 안에서 잘라 붙인 자리다.
- **`m2` 를 찾는 세 줄이 같은 결과라 셋 다 필요한 것처럼 읽힌다** — 필기가 `parameterType` 변수·`String.class`·`Class.forName("java.lang.String")` 을 차례로 쓰고 매번 이름을 출력한다. 셋은 **같은 것을 보이는 세 표기**이고, 실제 코드에 셋을 함께 쓸 이유는 없다. 특히 세 번째는 `String.class` 로 될 일을 검사 예외까지 달고 하는 것이라 **문자열로 지목해야 하는 이유가 없을 때는 쓰지 않는다** → [[class-loading]]
- **`getMethod` 는 브리지 메서드도 준다** — 제네릭 클래스를 상속·구현하면 컴파일러가 시그니처를 맞추는 메서드를 몰래 만들고, 그것이 목록에 섞여 **같은 이름이 두 번** 나온다. `m.isBridge()`·`m.isSynthetic()` 으로 걸러야 하며, Day59 의 예제 클래스들은 제네릭이 아니라 그 현상을 만나지 않는다 → [[type-erasure]] · [[generics]]

## 함께 보는 개념

- [[class-metadata]] — 메서드를 꺼내는 출발점
- [[class-loading]] — 클래스 쪽을 문자열로 지목하는 짝
- [[reflective-field-access]] — 같은 규칙(`get*`/`getDeclared*`)이 필드에 적용되는 자리
- [[reflective-instantiation]] — 생성자에 적용되는 자리
- [[modifier-flags]] — 찾은 메서드가 `static` 인지 묻는 방법
- [[varargs]] — `invoke` 의 인수가 받는 문법
- [[method]] · [[method-overriding]] — 이름 하나가 여럿을 가리킬 수 있는 이유
- [[access-modifier]] — 찾을 수 있는 범위를 정하는 것
- [[exception-handling]] — 예외가 한 겹 감싸이는 자리
- [[static-member]] — 첫 인수가 `null` 이 되는 근거
- [[annotation]] — 「무엇을 부를지」를 표시하는 짝 문법
- [[dispatch-table]] · [[command-pattern]] — 타입을 지키면서 이름으로 고르는 다른 답
- [[type-erasure]] — 제네릭 시그니처를 되읽는 자리
- [[mybatis]] — 이 도구로 남의 클래스의 getter 를 부르는 실물
- [[object-class]] — `getMethods()` 에 섞여 오는 것들의 출처

## 출처

- [[2024-08-20-Day59]] — 「메소드 정보 추출」·「메서드 호출」·「타입정보 추출」 세 절이 이 개념을 이룬다. `getMethods()`/`getDeclaredMethods()`/`getMethod()`/`getDeclaredMethod()` 넷을 코드로 갈라 **상속 포함 여부와 접근 범위가 서로 다른 두 축**이라는 것을 보였고(`getMethod("m3")` 는 `private` 이라 못 찾고 `getDeclaredMethod("toString")` 은 상속이라 못 찾는다), 오버로딩 때문에 파라미터 타입 목록을 순서까지 맞춰 넘겨야 한다는 것을 `getMethod("m3", String.class, int.class)` 와 주석으로 막은 반대 순서로 확인했다. 호출은 `static` 이면 `invoke(null, …)`·인스턴스면 `invoke(obj, …)` 로 갈리고, `m.invoke(obj, 10, 20)` 과 `obj.minus(10, 20)` 을 나란히 놓아 같은 일의 두 경로를 보였다. 인수를 낱개로 넘기는 것과 `new Object[]{…}` 로 담아 넘기는 것이 같다는 것, 배열·가변 파라미터는 감싸야 한다는 것도 이 회차의 것이다. 다만 예제가 `invoke` 의 반환값을 한 번도 쓰지 않아 결과를 받는 형태가 나오지 않고, `private` 메서드는 찾기만 하고 `invoke` 하지 않아 `setAccessible` 이 필요한 벽에 닿지 않으며, `InvocationTargetException`·`getMethods()` 예제의 남는 중괄호·파라미터 이름이 `arg0` 으로 지워진다는 것·`static` 쪽이 첫 인수를 무시한다는 비대칭은 다루지 않았다
