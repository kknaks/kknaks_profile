---
type: concept
id: reflective-annotation-access
title: 리플렉션 애노테이션 읽기 (getAnnotation)
aliases:
  - getAnnotation
  - getAnnotations
  - getDeclaredAnnotations
  - 애노테이션 추출
  - 애노테이션 읽기
up:
  - 2024-08-21-Day60
  - 2024-08-22-Day61
tags:
  - java
  - 리플렉션
  - 메타데이터
  - 실행시점
---

# 리플렉션 애노테이션 읽기 (getAnnotation)

**선언에 붙여 둔 애노테이션을 실행 중에 꺼내 그 프로퍼티 값을 읽는 것.** [[class-metadata]] 노트가 Day21 기준으로 「Day06 의 애노테이션을 읽는 그 누군가」를 예고하고 [[annotation]] 노트가 「누군가 읽어야 효과가 생긴다」로 남겨 둔 자리가, **Day60 에서 두 줄의 코드가 된다** — `clazz.getAnnotation(MyAnnotation.class)` 와 `obj.v1()` → [[class-metadata]] · [[annotation]]

## 정의

```java
Class<?> clazz = MyClass.class;
MyAnnotation obj = clazz.getAnnotation(MyAnnotation.class);

System.out.println(obj.v1());  // 가나다
System.out.println(obj.v2());  // 100
System.out.println(obj.v3());  // 3.14
```

필기가 걸음을 셋으로 적었다 — 「annotation을 설정한다」·「annotation을 사용할 class를 만들고 property를 설정한다」·「클래스를 동적으로 호출하여 property값을 추출한다」.

### 리플렉션 가족 중 유일하게 타입이 살아 있다

| 무엇을 꺼내나 | 돌려주는 것 | 그 값으로 하는 일 |
|---|---|---|
| 메서드 | `Method` (**중개 객체**) | `m.invoke(obj, …)` → 결과는 `Object` |
| 필드 | `Field` (중개 객체) | `f.get(obj)` → `Object` |
| 생성자 | `Constructor` (중개 객체) | `c.newInstance()` → `Object` |
| **애노테이션** | **`MyAnnotation` 그 자체** | `obj.v1()` → **`String`** |

**앞의 셋은 「부르는 도구」를 주고 이쪽은 「값이 담긴 객체」를 준다.** 그래서 캐스팅도 `Object` 도 나오지 않고 `obj.v1()` 이 **컴파일러의 검사를 받는다** — 오타를 내면 실행 시점 예외가 아니라 컴파일 오류다. 이것이 가능한 이유는 선언이 `<A extends Annotation> A getAnnotation(Class<A> annotationClass)` 라서 **인수의 타입이 반환 타입과 묶여 있기** 때문이다. `Class<?>` 로 받은 변수에서 꺼내도 `MyAnnotation` 이 나온다 → [[generics]] · [[class-metadata]]

Day40 의 `loadJson(List<E> list, …, Class<E> elementType)` 이 「목록과 타입 정보가 짝인지 컴파일러가 검사한다」였던 그 문법이, 여기서는 **표준 라이브러리가 리플렉션의 구멍 하나를 메우는 데** 쓰인다 → [[type-erasure]]

### 넷이 갈리는 짝 — 그런데 갈리는 축이 다르다

| 메서드 | 주는 것 |
|---|---|
| `getAnnotation(X.class)` | 그 애노테이션 하나 (없으면 **`null`**) |
| `getAnnotations()` | 붙어 있는 것 전부 (**상속받은 것 포함** — 조건부) |
| `getDeclaredAnnotation(X.class)` | **직접 붙인** 것 하나 |
| `getDeclaredAnnotations()` | 직접 붙인 것 전부 |

Day59 가 메서드·필드·생성자·중첩 클래스 자리에서 본 `get*`/`getDeclared*` 짝이 여기서도 나오는데 **뜻이 같지 않다.** 다른 자리에서는 「상속 포함 + `public` 만」 대 「이 클래스만 + 전부」였는데, 애노테이션에는 **접근 지정자라는 것이 없으므로** 그 축이 사라진다. 그리고 남은 상속 축조차 조건부다 — 부모 클래스의 애노테이션이 `getAnnotations()` 에 나오는 것은 **그 애노테이션이 `@Inherited` 로 선언되었을 때만**이고, 인터페이스에서는 아예 물려받지 않는다 → [[inheritance]] · [[access-modifier]]

### `default` 값은 사용 자리에 저장되어 있지 않다

`@MyAnnotation` 만 적었는데 `obj.v1()` 이 「가나다」를 준다. 필기는 「annotation에 default 설정이 되어있다면 설정을 하지 않아도 된다」로 결과만 적었다. **그 값이 어디서 오는가** — `MyClass.class` 안에는 「`MyAnnotation` 이 붙어 있다」는 사실만 있고 값은 없다. 값은 **`MyAnnotation.class` 쪽에 기본값으로 저장**되어 있고, 읽는 시점에 그것으로 채워진다.

그래서 결과가 하나 따라온다 — **애노테이션의 `default` 값을 바꾸고 그 애노테이션만 다시 컴파일하면, 그것을 쓰는 코드를 다시 컴파일하지 않아도 새 값이 나온다.** 값을 명시해 적어 둔 자리는 반대로 그 클래스 파일에 박혀 있어 바뀌지 않는다. **「기본값에 맡긴 것」과 「값을 적은 것」이 나중에 다르게 움직인다** → [[class-file-format]] · [[compilation]]

## 사용 예시

Day60 의 「배열 property 추출」 절이 프로퍼티가 배열일 때를 보인다.

```java
@Retention(RetentionPolicy.RUNTIME)
public @interface MyAnnotation3 {
  // 배열 값이 한 개일 경우 중괄호를 생략할 수 있다.
  String[] v1() default "가나다";
  int[] v2() default 100;
  float[] v3() default 3.14f;
}
```

```java
@MyAnnotation3(
    // 배열 값을 지정할 때 중괄호를 사용한다.
    v1 = {"홍길동", "임꺽정", "유관순"},
    v2 = {1000, 2000, 3000, 4000, 5000},
    v3 = {1.12f, 2.23f, 3, 34f})
public class MyClass4 {
}
```

```java
Class<?> clazz = MyClass4.class;
MyAnnotation3 obj = clazz.getAnnotation(MyAnnotation3.class);

printValues(obj.v1());
printValues(obj.v2());
printValues(obj.v3());
```

**`printValues` 가 셋으로 오버로딩된 것이 우연이 아니다.** `String[]`·`int[]`·`float[]` 을 하나로 받을 방법이 없다 — `Object[]` 로 받으면 `int[]` 와 `float[]` 이 들어가지 않고([[array]] 의 기본형 배열은 `Object[]` 가 아니다), `Object...` 로 받으면 `int[]` 가 **인수 하나**로 들어가 원소가 펼쳐지지 않는다. Day59 의 `invoke` 에서 「배열을 감싸야 한다」로 만난 그 성질이 **여기서는 메서드를 세 개 쓰게 만드는 이유**로 나타난다 → [[varargs]] · [[method]]

출력이 `1.12,2.23,3.0,34.0,` 인 것도 이 절이 남긴 것이다 — `v3` 의 세 번째 값 `3` 은 `int` 리터럴인데 배열이 `float[]` 이라 **`3.0` 으로 승격**되어 담긴다 → [[type-promotion]] · [[floating-point]]

## 왜 중요한가

**프레임워크가 설정 파일 없이 동작하는 방법이 이것이다.** MyBatis 의 `mybatis-config.xml` 이 하던 일 — 「이 클래스를 이렇게 취급하라」 — 을 클래스 선언 옆에 적어 두고 실행 중에 읽으면 XML 이 사라진다. 같은 노트의 `<typeAliases>` 를 `@Alias("user")` 로 대신할 수 있는 근거가 이 두 줄의 코드이고, **한 회차의 앞부분(MyBatis 설정)과 뒷부분(애노테이션)이 서로의 대안이라는 것을 필기는 잇지 않았다** → [[type-alias]] · [[xml]]

**그리고 「타입으로 표현할 수 없는 계약」을 적는 두 번째 방법이 열린다.** [[reflective-invocation]] 노트가 인터페이스로 강제할 수 없는 `static` 메서드를 이름 문자열로 부른 사례를 적었는데, 그 방식은 **약속이 코드 어디에도 안 보인다**(문자열이 호출하는 쪽에만 있다). 애노테이션으로 하면 약속이 **약속을 지켜야 하는 클래스 위에** 적히고, 이름이 아니라 **타입**으로 지목되므로 오타가 컴파일에서 걸린다 — 리플렉션 셋 중 이것만 문자열을 쓰지 않는다 → [[interface]] · [[annotation]]

**대신 「붙였는데 아무 일도 안 일어난다」가 새로 생긴다.** 애노테이션은 스스로 동작하지 않으므로, 읽는 코드가 그 자리를 훑지 않으면 붙인 것이 그냥 없다. 그리고 실패가 예외가 아니라 `null` 이나 「해당 없음」이라서 **어느 쪽이 문제인지**(안 붙였나 · 보존 정책이 아닌가 · 읽는 쪽이 안 훑나) 를 코드에서 갈라내야 한다 → [[annotation-retention]]

## 경계와 오해

- **`getAnnotation` 이 `null` 을 주는 경우가 셋이고 전부 예외가 아니다** — ① 안 붙였다, ② 붙였지만 [[annotation-retention]] 이 `RUNTIME` 이 아니다(**기본값이 `CLASS` 이므로 안 적으면 이쪽**), ③ 부모에 붙어 있고 그 애노테이션이 `@Inherited` 가 아니다. 셋 다 조용하고, 필기의 예제는 곧바로 `obj.v1()` 을 부르므로 **바로 `NullPointerException`** 이다 — 그 메시지에 애노테이션 이름이 없어서 원인이 애노테이션이라는 것부터 알아내야 한다. 값을 읽기 전에 `isAnnotationPresent(X.class)` 로 묻거나 `null` 검사를 하는 형태가 필요한데 필기에는 없다 → [[exception-handling]] · [[object-reference]]
- **돌려받은 `obj` 는 내가 만든 인스턴스가 아니다 — JVM 이 만든 프록시다. 그 프록시를 만드는 문법을 하루 뒤 배운다** — `@interface` 는 인터페이스이므로 `new MyAnnotation()` 이 불가능한데 값이 담긴 객체가 온다. `obj.getClass()` 를 찍으면 `MyAnnotation` 이 아니라 `$Proxy1` 같은 이름이고, `obj instanceof MyAnnotation` 은 참이다. [[class-metadata]] 노트의 「`getClass()` 로 진짜 타입을 안다」가 여기서는 **선언 타입과 다른 답**을 주는 자리이며, `equals`·`hashCode`·`toString` 은 애노테이션 규약대로 그 프록시가 구현한다. **Day61 이 `Proxy.newProxyInstance` + `InvocationHandler` 를 배우면서 그 `$Proxy1` 이 어떻게 만들어지는지가 손에 들어온다** — 「인터페이스만 주면 구현체가 실행 중에 생긴다」가 그 문법이고, 그래서 `@interface` 가 인터페이스라는 사실 하나로 이 반환값이 설명된다. 두 회차가 하루 차이인데 필기는 잇지 않는다 → [[dynamic-proxy]] · [[anonymous-class]] · [[interface]] · [[object-equality]]
- **배열 프로퍼티는 부를 때마다 새 배열을 준다** — `obj.v1()` 을 두 번 부르면 서로 다른 배열이고, 하나를 고쳐도 다음 호출에 영향이 없다. 애노테이션의 값은 **바뀌지 않아야** 하는데 배열은 원소를 바꿀 수 있으므로, 프록시가 **복사해서** 내주기 때문이다. 그래서 `obj.v1() == obj.v1()` 은 거짓이고, 큰 배열을 반복문 조건에서 매번 부르면 그만큼 복사가 일어난다 → [[defensive-copy]] · [[immutability]] · [[array-copy]]
- **`getAnnotations()` 와 `getDeclaredAnnotations()` 의 차이가 다른 자리들과 다르다 — 시점을 박아 두면** Day59 기준으로 [[class-metadata]] 가 「`get*` 과 `getDeclared*` 라는 짝이 자리마다 반복되는 것이 이 API 의 유일한 규칙」이라고 적었는데, **Day60 에서 그 규칙이 처음 어긋난다.** 애노테이션에는 접근 지정자가 없어 「`public` 만」이라는 축이 없고, 상속 축은 `@Inherited` 가 있을 때만 살아난다. **짝의 모양이 같으니 뜻도 같을 것이라고 읽으면 여기서 처음 틀린다** → [[inheritance]]
- **애노테이션 프로퍼티에 아무 타입이나 쓸 수 없다** — 필기가 `String`·`int`·`float` 과 그 배열만 써서 이 벽에 닿지 않았다. 쓸 수 있는 것은 **기본형·`String`·`Class`·열거 타입·다른 애노테이션, 그리고 그것들의 배열**뿐이고, `Date` 나 내가 만든 클래스는 컴파일 오류다. **그리고 `null` 을 기본값으로 줄 수 없다** — 「값이 없음」을 표현하려면 `""` 나 특별한 상수를 약속으로 정해야 한다. 이유는 애노테이션 값이 **클래스 파일에 상수로 박히기** 때문이고, 그래서 이 문법은 「설정」까지만 담을 수 있다 → [[literal]] · [[constant-pool]] · [[data-type]]
- **같은 애노테이션을 한 자리에 두 번 붙이려면 `getAnnotation` 으로는 못 읽는다** — 기본적으로 한 번만 붙일 수 있고, `@Repeatable` 로 선언하면 두 번 붙을 수 있는데 그때는 **컴파일러가 묶음 애노테이션으로 감싸므로** `getAnnotation(X.class)` 이 `null` 이다. `getAnnotationsByType(X.class)` 를 써야 한다. **「붙였는데 `null` 이다」의 네 번째 원인**이고, 세 원인과 달리 이것은 붙인 개수가 정한다.
- **읽는 쪽은 클래스만이 아니다 — Day60 에서는 두 절이 만나지 않았고, 하루 뒤 Day61 에서 만난다** — Day60 의 필기는 `Class` 에서만 꺼낸다(`clazz.getAnnotation`). 같은 메서드가 `Method`·`Field`·`Constructor`·`Parameter` 에도 있다 — 넷 다 같은 인터페이스를 구현하기 때문이다. **`@Target` 으로 메서드나 필드에 붙게 만들었다면 읽는 쪽도 그 객체에서 꺼내야 하는데**, Day60 은 `@Target` 을 따로 배우고 읽기는 클래스에서만 해서 그 조합이 나오지 않았다. **Day61 이 `@Target(ElementType.PARAMETER)` 로 애노테이션을 만들고 `method.getParameters()` 로 매개변수를 꺼내 거기서 읽으려 한다** — 두 절이 처음 만나는 자리다. 다만 마지막 걸음에서 어긋난다: `params.getAnnotation(Param.class)` 로 **배열 자체에 대고** 불렀다(`params[i].getAnnotation(…)` 이어야 한다). **읽는 대상이 클래스에서 매개변수로 내려가면 「그 하나를 꺼내는」 걸음이 하나 더 필요하다**는 것이 그 실수의 내용이고, 프레임워크가 하는 「클래스의 필드를 전부 훑어 각 필드에 묻는」 형태가 정확히 그 걸음이다 → [[reflective-field-access]] · [[annotation-target]] · [[dynamic-proxy]]
- **애노테이션을 읽는 것과 그 값을 쓰는 것은 두 걸음이다 — Day61 이 첫 걸음에서 멈췄다** — `getAnnotation` 이 돌려주는 것은 **애노테이션 객체**이고 내가 필요한 것은 대개 그 안의 프로퍼티다. Day61 은 `map.put(anno, args[i])` 로 **객체 자체를 Map 의 키로** 넣었는데, 필요한 것은 `anno.value()` — `"no"`·`"count"` 라는 문자열이다. Day60 의 예제가 `obj.v1()` 까지 정확히 갔던 것과 대비되는 자리이고, **애노테이션을 만든 목적(이름을 얻는 것)이 그 한 번의 호출에 들어 있다.** 이 노트가 「리플렉션 가족 중 유일하게 타입이 살아 있다」로 적은 이득 — `obj.v1()` 이 컴파일러의 검사를 받는다 — 이 여기서는 **아예 부르지 않아서** 쓰이지 않는다 → [[hash-based-collection]] · [[dynamic-proxy]]
- **필기 안에서 `MyAnnotation3` 이 두 번 다르게 선언된다** — 앞의 「property」 절에서는 `String value(); String tel();` 이고 배열 절에서는 `String[] v1(); int[] v2(); float[] v3();` 이다. 같은 이름의 애노테이션이 노트 안에서 두 모양을 가지므로 **어느 쪽을 가리키는지 결정되지 않는다.** `MyClass4` 도 `@Target` 절과 이 절에 각각 다른 내용으로 나온다 — 예제를 절마다 새로 만들면서 이름을 돌려 쓴 자리다.
- **`printValues` 는 마지막 값 뒤에도 쉼표를 찍는다** — `System.out.print(value + ",")` 이므로 `홍길동,임꺽정,유관순,` 이 된다. 필기의 기대 출력도 그렇게 적혀 있어 의도한 것으로 보이지만, [[dynamic-sql]] 의 `separator` 가 **사이에만** 넣는 것과 대비되는 자리다 — 「사이에 넣기」와 「뒤에 붙이기」는 다르고, 문자열을 이어 붙일 때 언제나 갈리는 지점이다 → [[string-builder]]
- **`@Retention(RetentionPolicy.RUNTIME)` 이 없으면 이 절 전체가 성립하지 않는다** — 필기의 두 예제는 그것을 붙였지만 **왜 붙였는지 적지 않았다.** 이 노트의 내용 전부가 그 한 줄을 전제하며, 그것이 「리플렉션으로 읽는다」는 말의 실제 조건이다 → [[annotation-retention]]

## 함께 보는 개념

- [[annotation]] — 읽히는 대상
- [[annotation-retention]] — 읽을 수 있게 하는 조건
- [[annotation-target]] — 어디에 붙었는지가 어디서 읽어야 하는지를 정한다
- [[class-metadata]] — 이 메서드가 달려 있는 객체
- [[reflective-invocation]] · [[reflective-field-access]] · [[reflective-instantiation]] — 같은 가족의 나머지 셋
- [[generics]] · [[type-erasure]] — 타입이 살아 있는 이유
- [[defensive-copy]] · [[immutability]] — 배열을 복사해 주는 이유
- [[varargs]] · [[array]] — 오버로딩 셋이 필요한 이유
- [[type-promotion]] · [[floating-point]] — `3` 이 `3.0` 이 되는 자리
- [[constant-pool]] · [[class-file-format]] — 값이 저장되는 곳
- [[interface]] · [[anonymous-class]] — 프록시가 그 타입인 이유
- [[exception-handling]] — `null` 이 예외로 바뀌는 지점
- [[type-alias]] · [[xml]] — 이 도구가 대신할 수 있는 설정
- [[mybatis]] — 이 도구 위에 서 있는 프레임워크
- [[dynamic-proxy]] — 돌려받은 애노테이션 객체를 만들어 내는 문법

## 출처

- [[2024-08-21-Day60]] — 「property 추출」 절의 두 소절(「property 값 추출」·「배열 property 추출」)이 이 개념이다. `@Retention(RetentionPolicy.RUNTIME)` 으로 선언한 애노테이션을 클래스에 붙이고 `clazz.getAnnotation(MyAnnotation.class)` 로 꺼내 `obj.v1()`·`obj.v2()`·`obj.v3()` 로 프로퍼티 값을 읽는 것을 코드로 보였고, **반환값이 애노테이션 타입 그 자체라 캐스팅 없이 프로퍼티를 부른다**는 것이 이 회차에서 확인되는 형태다. 배열 프로퍼티는 선언에서 값 하나면 중괄호를 생략할 수 있고(`String[] v1() default "가나다"`) 지정할 때는 중괄호를 쓴다는 것, 그리고 `String[]`·`int[]`·`float[]` 을 받는 `printValues` 를 **셋으로 오버로딩**해야 한다는 것도 여기서 나온다. 「default 설정이 되어있다면 설정을 하지 않아도 된다」로 결과는 적었지만 **그 기본값이 애노테이션 타입 쪽에 저장되어 읽는 시점에 채워진다는 것**은 비어 있고, `@Retention(RUNTIME)` 을 왜 붙였는지도 적혀 있지 않다. `getAnnotation` 이 `null` 을 주는 경우들·돌려받은 객체가 프록시라는 것·배열이 매번 복사되어 오는 것·`getAnnotations()`/`getDeclaredAnnotations()` 의 축이 다른 리플렉션 자리들과 다르다는 것·`Method`·`Field` 에서도 같은 메서드를 쓸 수 있다는 것은 다루지 않았다. `MyAnnotation3` 과 `MyClass4` 가 노트 안에서 각각 두 번 다른 내용으로 선언된다
- [[2024-08-22-Day61]] — 하루 뒤. **Day60 이 각각 배운 세 절(`@Retention`·`@Target`·애노테이션 읽기)이 처음 한 코드에서 만난다.** `@Retention(RetentionPolicy.RUNTIME)` + `@Target(ElementType.PARAMETER)` 로 `@Param` 을 선언해 DAO 메서드의 매개변수에 붙이고, `method.getParameters()` 로 매개변수 목록을 꺼내 거기서 애노테이션을 읽어 `Map` 의 키로 쓰려 한다 — **읽는 대상이 클래스가 아닌 첫 사례**이고, Day60 의 「읽기는 클래스에서만」이 여기서 벗어난다. 목적도 분명하다: 매개변수 이름이 클래스 파일에서 지워져 `arg0` 이 되므로(→ [[reflective-invocation]]) **이름을 애노테이션에 한 번 더 적어 실행 중에 되찾는** 것이다. 다만 마지막 두 걸음이 어긋난다 — `params.getAnnotation(Param.class)` 는 **배열에 대고** 부른 것이고(`params[i]` 가 빠졌다), `map.put(anno, args[i])` 는 **애노테이션 객체를 키로** 넣어 정작 필요한 `anno.value()` 를 꺼내지 않는다. 그리고 같은 회차의 `Proxy.newProxyInstance` 가 **Day60 이 「돌려받은 애노테이션 객체는 JVM 이 만든 프록시다」로 남긴 물음의 답**인데(그 프록시를 만드는 문법이다) 두 주제가 이어지지 않는다 → [[dynamic-proxy]]
