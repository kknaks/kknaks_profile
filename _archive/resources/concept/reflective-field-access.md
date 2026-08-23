---
type: concept
id: reflective-field-access
title: 리플렉션 필드 접근 (Field 와 setAccessible)
aliases:
  - setAccessible
  - Field 객체
  - getDeclaredField
  - getDeclaredFields
  - 필드 강제 접근
  - 접근 제한 우회
  - 접근제한 우회
up:
  - 2024-08-20-Day59
tags:
  - java
  - 리플렉션
  - 캡슐화
  - 실행시점
---

# 리플렉션 필드 접근 (Field 와 setAccessible)

**필드를 이름으로 찾아 객체로 들고, `private` 이어도 값을 읽고 쓰는 것.** 컴파일러가 막는 `car.maker = "비트자동차"` 를 `makerField.set(car, "비트자동차")` 가 통과한다. Day59 가 이것을 「필드 정보 추출」 한 절로 다루면서 **필기에서 유일하게 물음표를 남겼다** — 코드 주석의 `// 가능해?` → [[class-metadata]] · [[access-modifier]]

## 정의

메서드 넷이 하는 일이 순서대로 하나씩이다.

| 호출 | 하는 일 |
|---|---|
| `clazz.getDeclaredFields()` | 이 클래스에 선언된 필드 **전부**(접근 지정자 무관) |
| `clazz.getDeclaredField("maker")` | 그중 이름으로 하나 |
| `field.setAccessible(true)` | **이 `Field` 객체의 접근 검사를 끈다** |
| `field.set(대상, 값)` / `field.get(대상)` | 값 쓰기 / 읽기 |

Day59 의 네 줄이 그 순서다 — 「`getDeclaredFields()` : 현재클래스의 필드정보 추출한다」·「`getDeclaredField("FeildName")` : 현재클래스에서 FieldName의 필드를 추출한다」·「`fieldName.setAccessible([true|false])` : 필드의 접근을 동적으로 제어한다」·「`setAccessible(true)` : 모든 modifier에 접근가능하다」.

그리고 인용 블록으로 스스로 경고를 달았다 — 「필드에 직접적으로 접근하는 것은 객체지향의 개념에 어긋나는 행위이다」 → [[encapsulation]]

필드 하나에서 꺼낼 수 있는 것은 이름과 타입이다.

```java
Field[] fields = clazz.getDeclaredFields();
for (Field f : fields) {
  System.out.printf("%s:%s\n", f.getName(), f.getType().getName());
}
```

**`f.getType()` 이 `Class` 라는 것이 이 API 의 성질을 보인다** — 필드에서 나온 값이 다시 [[class-metadata]] 의 입력이 되어 타입을 한 겹 더 파고들 수 있다.

## 사용 예시

Day59 가 `Car` 클래스로 `private` 필드에 값을 넣는 것까지 간다. **마지막 주석이 답 없이 남은 물음이다.**

```java
Class<?> clazz = Car.class;

Field[] fields = clazz.getDeclaredFields();
for (Field f : fields) {
  System.out.printf("%s:%s\n", f.getName(), f.getType().getName());
}

Constructor<Car> defaultConst = (Constructor<Car>) clazz.getConstructor();
Car car = defaultConst.newInstance();

// 1) private 필드는 일반적인 방식으로 접근할 수 없다.
//    car.maker = "비트자동차"; // 컴파일 오류!

// 2) 다음과 같이 Reflection API를 사용하면 private 필드에 접근할 수 있다.
Field makerField = clazz.getDeclaredField("maker");

// private modifier로 선언된 필드라 하더라도
// 다음 메서드를 통해 접근 가능하도록 만들 수 있다.
makerField.setAccessible(true);

// private 필드에 값 넣기
// 가능해?
makerField.set(car, "비트자동차");
```

### 「가능해?」의 답

**그 코드는 통한다.** `setAccessible(true)` 뒤의 `set` 은 `private` 필드에 값을 넣고, `car` 를 출력하면 `maker` 가 「비트자동차」다. 다만 **통하는 범위에 조건이 셋 있고, 그 셋이 이 개념의 실제 경계다.**

| 대상 | 되나 | 왜 |
|---|---|---|
| 같은 프로젝트 클래스의 `private` 필드 | **된다** | 검사를 끄는 것을 막을 것이 없다 |
| `private static final` 상수 | **안 된다** | `set` 이 `IllegalAccessException`. 게다가 원시·`String` 상수는 컴파일러가 **읽는 쪽에 값을 박아 넣어**(constant folding) 바꿔도 옛 값이 읽힌다 |
| 남의 모듈(JDK 내부 등)의 필드 | **막힌다** | Java 9 의 모듈 시스템이 `InaccessibleObjectException` 을 던진다(Java 17 부터 기본 거부) |

**즉 「가능해?」의 답은 「자바 버전과 대상에 따라 다르다」이고, 필기가 이 코드를 쓴 시점(Java 17 기준의 실습)에도 이미 그렇다.** 자기 코드에는 열려 있고 남의 코드에는 닫혀 있는 것이 지금의 상태다 → [[constant-pool]] · [[immutability]]

## 왜 중요한가

**`private` 필드만 있고 setter 가 없는 클래스를 프레임워크가 채울 수 있는 이유가 이것이다.** JSON 파서·MyBatis 의 `resultType`·JPA 엔티티가 전부 이 통로를 쓴다. Day59 의 필기가 「resultType에서 setProperty(Object obj)를 호출하여 객체에 정보를 넣는다」로 적었는데, 실제로는 **setter 가 있으면 setter, 없으면 이 필드 접근**이다 — 그래서 setter 를 안 만들어도 매핑이 된다 → [[mybatis]] · [[json]] · [[reflective-instantiation]]

**그리고 「캡슐화가 강제인가」의 답이 바뀐다.** `private` 는 **컴파일러의 약속**이고 실행 시점의 담이 아니다. 그것을 알기 전에는 「`private` 니까 아무도 못 본다」를 설계의 근거로 삼게 되는데, 실제로 보장되는 것은 「실수로 만지지 않는다」까지다. 비밀은 `private` 가 지켜 주지 않는다 → [[encapsulation]] · [[access-modifier]]

**대신 클래스의 내부 구조가 계약이 된다.** 필드 이름으로 값을 넣는 코드가 있으면 **필드 이름을 바꾸는 것이 호환성을 깨는 변경**이 된다. 리팩터링 도구가 그 문자열을 따라오지 않으므로, 이름을 바꾼 뒤 컴파일은 되고 실행 중에 값이 `null` 로 남는다 → [[refactoring]] · [[serialization]]

## 경계와 오해

- **`setAccessible(true)` 는 필드의 지정자를 바꾸지 않는다** — 「모든 modifier에 접근가능하다」는 필기의 표현이 필드가 `public` 이 된 것처럼 읽힌다. 바뀌는 것은 **이 `Field` 객체 하나가 접근 검사를 건너뛴다**는 사실뿐이고, 다른 코드의 `car.maker` 는 여전히 컴파일 오류이며 [[modifier-flags]] 로 물어보면 그대로 `private` 이다. **객체에 붙은 스위치이지 클래스에 한 일이 아니다.**
- **`fieldName.setAccessible(...)` 이라는 표기가 대상을 흐린다** — 부르는 대상은 필드의 **이름**이 아니라 `Field` 객체다. 필기의 다음 줄이 `makerField.setAccessible(true)` 로 옳게 쓰고 있으므로 설명 줄의 이름만 어긋난 것인데, 「이름을 가지고 무언가 한다」로 읽으면 문자열을 넘기는 메서드를 찾게 된다.
- **`getFields()` 는 다른 것을 준다 — 필기가 그쪽을 다루지 않았다** — 메서드 쪽의 `getMethods()`/`getDeclaredMethods()` 와 **정확히 같은 두 축**이다. `getFields()` 는 상속받은 것까지 포함하되 `public` 만, `getDeclaredFields()` 는 이 클래스에 선언한 것만이되 전부다. 그래서 **부모의 `private` 필드는 어느 쪽으로도 나오지 않고**, 상속 계층 전체를 훑으려면 `getSuperclass()` 로 올라가며 `getDeclaredFields()` 를 반복해야 한다. 「필드 목록을 가져왔다」로 끝내면 부모의 상태가 통째로 빠진다 → [[reflective-invocation]] · [[inheritance]] · [[class-metadata]]
- **`set` 은 타입 검사를 실행 시점으로 옮긴다** — `makerField.set(car, 100)` 은 **컴파일된다**(둘째 인수가 `Object` 다). 실행 중에 `IllegalArgumentException` 이고, 기본형 필드에 `null` 을 넣으면 같은 예외다. 원래 `car.maker = 100;` 이 컴파일 오류로 잡히던 것이 여기서는 실행 시점으로 밀린다 — **리플렉션은 검사를 없애는 것이 아니라 늦추는 것**이다 → [[type-casting]] · [[exception-handling]]
- **필드 목록의 순서는 보장되지 않는다** — 명세가 「정렬되지 않으며 특정 순서가 아니다」로 못 박았다. 필기의 예제는 순서를 쓰지 않아 문제가 없지만, 이 목록으로 CSV 헤더나 화면 항목을 만들면 **컴파일러나 JVM 을 바꿨을 때 열 순서가 달라진다.** 「소스에 쓴 순서대로 나오더라」는 관찰은 보장이 아니다 → [[csv]] · [[reflective-invocation]]
- **컴파일러가 만든 필드가 목록에 섞인다** — 소스에 없는데 나오는 것들이 있다. 인스턴스 중첩 클래스의 **`this$0`**(바깥 인스턴스 주소), `enum` 의 `$VALUES`, 커버리지 도구가 끼운 `$jacocoData` 같은 것이다. [[nested-class]] 회차가 `B2 this$0;` 를 주석으로 펼쳐 적었던 그 필드가 **여기서는 실제 목록에 나타난다** — 그래서 「선언한 필드 전부」를 훑는 코드는 `f.isSynthetic()` 으로 걸러야 하고, 걸르지 않으면 직렬화 결과에 정체 불명의 항목이 하나 붙는다 → [[nested-class]] · [[serialization]]
- **`clazz.getConstructor()` 를 `Constructor<Car>` 로 캐스팅한 것은 unchecked 다** — `Class<?> clazz = Car.class;` 로 받았기 때문에 `getConstructor()` 가 `Constructor<?>` 를 돌려주고 캐스팅이 필요해졌다. **`Class<Car> clazz = Car.class;` 로 받으면 `Constructor<Car>` 가 그대로 와 캐스팅이 사라진다** — 한 달 전 Day40 이 raw `Class` 를 `Class<E>` 로 고쳐 쓰며 배운 것이 여기서 다시 걸린 자리다 → [[generics]] · [[raw-type]] · [[reflective-instantiation]]
- **경고와 실제 쓰임이 갈린다 — 응용 코드에서는 옳고 프레임워크에서는 유일한 길이다** — 「객체지향의 개념에 어긋나는 행위」라는 인용은 **내가 내 클래스의 필드를 밖에서 만지는 경우**를 말하며 그 자리에서는 정확하다. 그러나 남의 클래스를 미리 알지 못한 채 채워야 하는 층(매퍼·직렬화기·DI 컨테이너)에서는 이것이 대안 없는 도구다. **「하면 안 되는 일」과 「프레임워크가 하는 일」을 한 문장으로 묶으면 MyBatis 가 어떻게 도는지 설명할 수 없다** → [[mybatis]] · [[dependency-injection]]
- **읽는 쪽(`get`)도 같은 벽을 받는다** — 필기는 `set` 만 썼는데 `get` 도 `setAccessible(true)` 없이는 `IllegalAccessException` 이다. 테스트가 `private` 상태를 확인하려고 이 통로를 쓰는 것이 흔한데, **그 순간 테스트가 구현 세부에 묶인다** — 필드 이름을 바꾸면 테스트가 깨진다.
- **`setAccessible` 은 성능 비용이 있고 그것을 줄이는 방법이 이 API 의 모양을 정한다** — 접근 검사를 매 호출마다 하지 않도록 **`Field` 객체를 캐시해 두고 재사용**하는 것이 프레임워크의 기본 형태다. 필기처럼 매번 `getDeclaredField` 를 부르면 이름 조회가 반복된다. MyBatis 의 `Reflector` 가 클래스마다 필드·메서드 목록을 한 번 읽어 들고 있는 것이 그 이유다 → [[caching]] · [[mybatis]]
- **`final` 필드는 「되기도 하고 안 되기도 한다」가 아니라 갈림이 정해져 있다** — `static final` 은 안 된다. 인스턴스 `final` 은 예전에 `setAccessible(true)` 로 뚫렸지만 `record` 와 hidden class 는 처음부터 막혀 있고 버전이 올라가며 좁아지고 있다. **「리플렉션이면 다 된다」로 외우면 `final` 을 불변의 근거로 쓰는 설계가 흔들린다** — 실제로 흔들리지 않는 이유는 리플렉션이 막혔기 때문이 아니라 이 좁힘이 계속되고 있기 때문이다 → [[immutability]]

## 함께 보는 개념

- [[class-metadata]] — 필드를 꺼내는 출발점
- [[reflective-invocation]] — 같은 두 축(`get*`/`getDeclared*`)이 메서드에 적용되는 자리
- [[reflective-instantiation]] — 채울 객체를 먼저 만드는 걸음
- [[access-modifier]] — 이 API 가 통과하는 규칙
- [[encapsulation]] — 「막힌다」의 실제 강도
- [[modifier-flags]] — 필드의 지정자를 되읽는 방법
- [[nested-class]] — `this$0` 이 목록에 나타나는 이유
- [[mybatis]] — 이 통로로 객체를 채우는 실물
- [[json]] · [[serialization]] — 같은 통로를 쓰는 다른 층
- [[immutability]] · [[constant-pool]] — `final` 이 이 통로에 저항하는 자리
- [[generics]] · [[raw-type]] — `Class<?>` 로 받아 캐스팅이 생긴 자리
- [[caching]] — `Field` 객체를 들고 있어야 하는 이유
- [[dependency-injection]] — 남의 객체에 값을 넣는 다른 이름
- [[type-casting]] · [[exception-handling]] — 검사가 실행 시점으로 밀린 결과

## 출처

- [[2024-08-20-Day59]] — 「필드 정보 추출」 절에서 `getDeclaredFields()` 로 필드 이름과 타입을 훑고, `getDeclaredField("maker")` + `setAccessible(true)` + `set(car, "비트자동차")` 로 **`private` 필드에 밖에서 값을 넣는 것**까지 갔다. 「필드에 직접적으로 접근하는 것은 객체지향의 개념에 어긋나는 행위이다」라는 경고를 인용 블록으로 함께 달았다. **코드 마지막 주석 `// 가능해?` 가 이 필기에서 답 없이 남은 물음**이고 답은 「된다, 단 `static final` 과 남의 모듈은 아니다」다. 다만 `getFields()` 와의 갈림(상속 포함 여부)·상속 계층을 올라가며 훑어야 한다는 것·목록 순서가 보장되지 않는다는 것·`this$0` 같은 합성 필드가 섞인다는 것·`set` 의 타입 검사가 실행 시점으로 밀린다는 것은 다루지 않았고, `Class<?>` 로 받아 `(Constructor<Car>)` unchecked 캐스팅이 생긴 자리도 그대로 남아 있다
