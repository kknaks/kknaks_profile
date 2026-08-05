---
type: concept
id: type-erasure
title: 타입 소거 (Type Erasure)
aliases:
  - 타입 소거
  - 타입소거
  - 소거
  - erasure
  - type erasure
  - TypeToken
  - 타입 토큰
  - type token
up:
  - 2024-07-22-Day40
tags:
  - java
  - 타입
  - 컴파일
  - jvm
---

# 타입 소거 (Type Erasure)

**제네릭의 타입 인자는 컴파일할 때만 있고 실행 시점에는 지워진다.** `List<Board>` 와 `List<User>` 는 컴파일러에게는 다른 타입이지만 실행 중에는 **똑같은 `List`** 다. Day40 은 이 말을 하지 않는데, 「배열 만들기」 절의 우회로 넷과 `new TypeToken<List<Board>>() {}` 의 빈 중괄호와 `Class<E> elementType` 매개변수가 **전부 이것을 우회하려고 있는 코드**다.

## 정의

컴파일러가 하는 일은 셋이다.

1. 타입 파라미터를 **상한으로 바꾼다** — `T` 는 `Object`, `<T extends Number>` 의 `T` 는 `Number`
2. 필요한 자리에 **캐스팅을 끼워 넣는다** — 그래서 사람이 안 써도 되는 것이다
3. 다형성이 깨지지 않게 **브리지 메서드**를 만든다

```java
// 내가 쓴 코드
Box<String> box = new Box<>();
box.set("안녕하세요");
String s = box.get();

// 컴파일 결과가 하는 일 (개념적으로)
Box box = new Box();          // 타입 인자가 없다
box.set("안녕하세요");         // set(Object)
String s = (String) box.get(); // 컴파일러가 넣은 캐스팅
```

**「캐스팅에서 자유롭다」의 정체가 이것이다** — 캐스팅이 없어진 것이 아니라 **내가 쓰지 않게 된 것**이다 → [[generics]] · [[type-casting]]

지워지는 것과 남는 것이 갈린다. 이 구분이 없으면 아래 `TypeToken` 트릭이 왜 되는지 설명되지 않는다.

| | 실행 시점에 |
|---|---|
| **인스턴스가 들고 있는 타입 인자** (`new ArrayList<Board>()` 의 `Board`) | **없다** |
| 필드·메서드 시그니처·상위 타입의 제네릭 표기 | **클래스 파일에 메타데이터로 남는다** |
| 배열의 원소 타입 (`new String[10]` 의 `String`) | **있다** — 배열은 소거되지 않는다 |

**마지막 줄이 Day40 「Generic의 사용 — 배열 만들기」의 원인 전체다.** 배열은 실행 시점에 자기 원소 타입을 알아야 하는데(`ArrayStoreException` 을 던지려면 알아야 한다) 제네릭의 `T` 는 그 시점에 없다 → [[array]] · [[class-file-format]]

## 사용 예시

**우회로 1 — 견본 배열을 받아 복제한다.** 타입 정보를 배열이 들고 오게 한다.

```java
  // 예1) 제네릭의 타입 파라미터로 레퍼런스 배열을 생성할 수 없다.
  static <T> T[] create1() {
    T[] arr;
    //    arr = new T[10]; // 컴파일 오류! new 명령어를 사용할 때 제네릭의 타입 파라미터를 사용할 수 없다.
    return null;
  }

  // 예2) 견본 배열을 받아서 복제하는 방법을 사용한다.
  static <T> T[] create2(T[] arr) {
    return Arrays.copyOf(arr, 10);
  }
```

**`create2(new String[0])` 의 빈 배열은 값이 아니라 타입을 넘기는 수단이다.** 원소가 없는데도 인수로 있어야 하는 이유가 그것이다 → [[array-copy]]

**우회로 2 — 타입 정보를 `Class` 로 직접 받는다.**

```java
  // 예3) 배열의 타입 정보를 받아 생성하기
  static <T> T[] create3(Class<?> type) {
    return (T[]) Array.newInstance(type, 10);
  }

  // 예4) 견본 배열에서 타입 정보를 추출하여 배열을 생성하기
  static <T> T[] create4(T[] arr) {
    Class<?> arrayTypeInfo = arr.getClass();               // 예) String[]
    Class<?> arrayItemTypeInfo = arrayTypeInfo.getComponentType(); // 예) String
    return (T[]) Array.newInstance(arrayItemTypeInfo, 10);
  }
```

**`Array.newInstance` 는 실행 시점의 값(`Class`)으로 배열을 만드는 유일한 통로다.** `new` 는 컴파일 시점에 타입이 코드에 적혀 있어야 하고, 그 자리에 `T` 를 쓸 수 없다 → [[class-metadata]]

**우회로 3 — 익명 서브클래스로 타입을 클래스 파일에 박는다.** Day40 이 Gson 을 쓰면서 만나는 형태다.

```java
boardList.addAll(new Gson().fromJson(strBuilder.toString(), new TypeToken<List<Board>>() {
}));
```

**끝의 빈 `{}` 가 장식이 아니다.** `new TypeToken<List<Board>>()` 만으로는 `List<Board>` 라는 정보가 아무 데도 남지 않지만, `{}` 를 붙이면 **`TypeToken<List<Board>>` 를 상속한 익명 클래스**가 생기고 「상위 타입의 제네릭 표기」는 소거되지 않으므로 클래스 파일에 `List<Board>` 가 그대로 적힌다. Gson 은 그것을 `getGenericSuperclass()` 로 읽는다 — **소거의 예외 하나를 이용해 소거를 우회하는 것** → [[anonymous-class]]

**우회로 4 — 타입을 매개변수로 받아 실행 시점에 조립한다.** 제네릭 메서드로 합칠 때 필연적으로 나오는 형태다.

```java
  private <E> void loadJson(List<E> list, String filename, Class<E> elementType) {
      ...
      list.addAll((List<E>) new GsonBuilder().setDateFormat("yyyy-MM-dd HH:mm:ss").create()
          .fromJson(strBuilder.toString(),
              TypeToken.getParameterized(List.class, elementType).getType()));
```

`E` 가 실행 시점에 없으므로 **`new TypeToken<List<E>>() {}` 로는 쓸 수 없다** — 그렇게 쓰면 익명 클래스에 박히는 것이 `List<E>` 라는 「지워진 이름」이라 Gson 이 원소 타입을 알 수 없다. 그래서 `Class<E>` 를 받아 `getParameterized(List.class, elementType)` 로 **타입을 값으로 조립한다.** 필기가 이 줄에 도달한 것이 제네릭을 제대로 쓴 증거이고, 앞의 `Class<E> elementType` 매개변수가 왜 필요한지에 대한 답이다 → [[json]] · [[generics]]

## 왜 중요한가

**제네릭이 「컴파일 시점 검사」에 그치는 이유가 설명된다.** 넣을 때 막아 주는 것이 전부이고, 어떤 경로로든 검사를 우회해서 넣은 값은 실행 중에 아무도 잡지 않는다. `(List<E>)` 같은 unchecked 캐스팅이 경고를 내는 것이 그래서다 — 컴파일러가 「여기서부터는 내가 보증하지 않는다」고 말하는 자리다 → [[type-casting]]

**라이브러리 API 가 왜 `Class` 나 `TypeToken` 을 요구하는지 읽힌다.** Gson·Jackson·Spring 이 `Class<T>` 나 `TypeReference` 를 받는 것은 API 설계 취향이 아니라 **그것 없이는 무엇으로 되돌릴지 알 방법이 없기 때문**이다. 이 사실을 모르면 「왜 이 라이브러리는 이렇게 번거로운가」에서 멈춘다.

**옛 코드와 새 코드가 같은 바이트코드 위에서 섞일 수 있다.** 제네릭은 Java 5 에 들어왔는데 그 전에 쓰인 `List` 를 쓰는 코드가 그대로 돌아간다 — **컴파일 결과가 같기 때문**이다. 그 호환성의 대가가 소거이고, 대가의 흔적이 [[raw-type]] 이다 → [[bytecode]]

## 경계와 오해

- **소거 ≠ 제네릭 정보가 전부 사라진다** — 「실행 시점에 타입이 없다」는 **인스턴스**에 대한 말이다. `List<Board> boardList;` 라는 **필드 선언**의 제네릭 표기는 클래스 파일의 시그니처 속성에 남고, 그래서 리플렉션으로 `getGenericType()` 을 읽을 수 있다. `TypeToken` 이 성립하는 것도 「상위 타입의 제네릭 표기가 남는다」는 이 예외 덕분이다. **둘을 뭉치면 「TypeToken 이 왜 되는가」와 「왜 `new TypeToken<List<E>>(){}` 는 안 되는가」를 둘 다 설명할 수 없다** → [[class-file-format]]
- **배열과 제네릭은 정반대다 — 그래서 섞으면 어긋난다** — 배열은 실행 시점에 원소 타입을 들고 있고(실체화), 제네릭은 안 들고 있다(소거). 그래서 `new T[10]` 이 불가능하고, `List<String>[]` 같은 배열도 만들 수 없다. Day40 이 「배열에 제네릭 적용하기」에서 만난 벽 전체가 이 한 문장이다.
- **`(T[])` 캐스팅은 실행 시점에 아무것도 검사하지 않는다 — 터지는 곳은 호출부다** — `create3` 안의 `(T[])` 는 소거 후 `(Object[])` 이거나 아예 사라진다. 실제 검사는 **컴파일러가 호출부에 끼워 넣은 캐스팅**에서 일어난다 — `String[] arr = create3(Integer.class);` 는 `create3` 안에서는 조용히 지나가고 **대입하는 줄에서 `ClassCastException`** 이다. **오류 메시지가 원인 코드를 가리키지 않는 대표적 형태**이고, 이런 값이 검사 없이 흘러 다니는 상태를 heap pollution 이라 부른다 → [[type-casting]] · [[exception-handling]]
- **`instanceof List<String>` 은 쓸 수 없다** — 실행 시점에 확인할 대상이 없으므로 컴파일 오류다. `instanceof List` 나 `instanceof List<?>` 만 된다. 「타입을 물어볼 수 있다」는 감각이 제네릭에서는 절반만 성립한다 → [[instanceof-operator]]
- **`List<String>.class` 도 없다** — `List.class` 하나뿐이고 `List<String>` 과 `List<Integer>` 가 **같은 `Class` 인스턴스**를 공유한다. Day21 에서 「`Class` 인스턴스는 클래스마다 하나」로 배운 것이 여기서 「타입 인자는 그 하나를 늘리지 않는다」로 이어진다 → [[class-metadata]]
- **타입 인자만 다른 오버로딩은 불가능하다** — `void m(List<String>)` 과 `void m(List<Integer>)` 는 소거 후 시그니처가 같아 **컴파일 오류**다. 오버로딩이 「매개변수 타입이 다르면 된다」로 외워져 있으면 여기서 어긋난다 → [[method]]
- **`static` 필드는 타입 인자마다 따로 있지 않다** — `Box<String>` 과 `Box<Integer>` 가 같은 `static` 필드를 공유한다. 클래스는 하나뿐이기 때문이고, 그래서 타입 파라미터를 `static` 필드 타입으로 쓸 수도 없다 → [[static-member]]
- **`new TypeToken<List<Board>>()` 에서 `{}` 를 지우면 컴파일되지 않는다** — Gson 의 `TypeToken` 은 추상 클래스라 직접 인스턴스화할 수 없고, 그 「불편함」이 실수 방지 장치다. 반대로 **`{}` 가 있는데 타입 인자에 타입 변수(`E`)를 넣으면 컴파일은 되고 결과만 틀린다** — 그 경우는 `getParameterized` 를 써야 한다. 오류가 나는 쪽보다 **컴파일되는 쪽이 위험하다** → [[anonymous-class]]
- **소거는 성능 최적화가 아니라 호환성 결정이다** — 「지우면 빠르니까」가 아니라 **제네릭 이전에 쓰인 클래스 파일과 같은 형태를 유지해야 했기 때문**이다. C# 은 다른 선택(실체화 제네릭)을 해서 `List<int>` 가 박싱 없이 돌아가고 `typeof(List<int>)` 도 된다. **같은 문법으로 보이는 기능이 언어마다 다른 것이 이 지점** → [[wrapper-class]] · [[platform-dependency]]
- **필기의 「컴파일 과정에서 T가 결정되면 바꿀수 없다」는 맞지만 이유가 소거와 반대편이다** — `Box<String>` 을 `Box<Object>` 에 대입할 수 없는 것은 정보가 지워져서가 아니라 **컴파일러가 정보를 엄격하게 쓰기 때문**이다. 소거는 실행 시점의 이야기이고 그 규칙은 컴파일 시점의 이야기다 → [[wildcard-type]]

## 함께 보는 개념

- [[generics]] — 이 소거의 대상이 되는 문법
- [[raw-type]] — 소거를 전제로 남아 있는 옛 문법
- [[wildcard-type]] — 컴파일 시점 규칙 쪽의 이야기
- [[class-metadata]] — 타입을 실행 시점의 값으로 넘기는 통로
- [[anonymous-class]] — `TypeToken` 트릭이 쓰는 문법
- [[array]] — 소거되지 않는 반대편 컨테이너
- [[array-copy]] — 제네릭 배열을 만드는 우회로
- [[type-casting]] — 컴파일러가 몰래 넣는 것과 사람이 쓰는 것
- [[instanceof-operator]] — 제네릭에는 물어볼 수 없는 검사
- [[bytecode]] — 소거된 결과가 사는 곳
- [[class-file-format]] — 지워지지 않고 남는 시그니처가 적히는 자리
- [[json]] — `TypeToken` 이 실제로 필요해진 자리
- [[serialization]] — `(List<User>) readObject()` 가 검사되지 않던 자리

## 출처

- [[2024-07-22-Day40]] — 소거라는 이름은 나오지 않지만 그 결과가 세 곳에 나타난다. 「배열 만들기」 절이 `new T[10]` 이 컴파일 오류인 것과 우회로 넷(`Arrays.copyOf` 로 견본 복제 · `Array.newInstance(Class, 10)` · `getComponentType()` 으로 원소 타입 추출)을 보여 주고, `(T[])` unchecked 캐스팅을 그대로 둔다. Gson 쪽에서는 `new TypeToken<List<Board>>() {}` 의 익명 서브클래스로 원소 타입을 넘기고, 제네릭 메서드로 합친 `loadJson` 에서는 `E` 가 실행 시점에 없어 `TypeToken.getParameterized(List.class, elementType)` 와 `Class<E> elementType` 매개변수로 갈아탄다 — **타입을 컴파일 시점 표기에서 실행 시점 값으로 옮기는 이행이 한 노트 안에서 일어난다**
