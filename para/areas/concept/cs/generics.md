---
type: concept
id: generics
title: 제네릭 (Generics)
aliases:
  - 제네릭
  - 제네릭스
  - generic
  - generics
  - 타입 파라미터
  - 타입 매개변수
  - type parameter
  - 제네릭 메서드
  - generic method
up:
  - 2024-07-22-Day40
tags:
  - java
  - 타입
  - 문법
  - 재사용
---

# 제네릭 (Generics)

**타입을 나중에 정하도록 비워 두고, 쓰는 쪽이 채우게 하는 것.** Day40 의 한 줄이 정의 전부다 — 「결정되지 않은 타입을 파라미터로 처리하고 실제 사용할 때 파라미터를 구체적인 타입으로 대체 시키는 기능」. **값을 매개변수로 올리던 것을 타입에 대해 하는 것**이고, 그래서 [[parameterization]] 의 타입 버전이라 읽으면 정확하다.

## 정의

비워 두는 자리가 두 군데다 — **클래스에 선언하는 것**과 **메서드에 선언하는 것**.

```java
// 클래스의 타입 파라미터 — 인스턴스를 만들 때 정해진다
class Box<T> {
  private T value;
  public T get() { return this.value; }
  public void set(T value) { this.value = value; }
}

// 메서드의 타입 파라미터 — 호출할 때 정해진다 (반환 타입 앞에 <T> 를 적는다)
static <T> T[] reverse2(T[] arr) { ... }
```

채우는 쪽은 타입 인자를 적거나 `<>` 로 비워 컴파일러가 추론하게 한다.

```java
Box<String> box = new Box<>();     // <> — 왼쪽 선언에서 String 을 추론한다
String[] arr = reverse2(new String[] {"a", "b"});   // 인수에서 T = String 을 추론한다
```

| 자리 | 문법 | T 가 정해지는 시점 |
|---|---|---|
| 클래스 | `class Box<T>` | 그 클래스의 **인스턴스를 선언·생성**할 때 |
| 메서드 | `static <T> T[] m(T[] a)` | 그 메서드를 **호출**할 때 (인수·대입 대상에서 추론) |

**두 자리는 서로 독립이다.** Day40 의 `Box<T>` 와 `reverse2` 의 `<T>` 는 글자만 같고 아무 관계가 없다 — `static` 메서드는 애초에 클래스의 타입 파라미터를 쓸 수 없다(아래 「경계와 오해」).

`T`·`E`·`K`·`V` 는 **관례일 뿐 문법이 아니다.** Day40 도 연습 코드에서는 `T` 를, 실습 프로젝트에서는 `E`(element) 를 쓴다.

## 사용 예시

Day40 이 실습 프로젝트에서 얻은 것이 이 개념의 값을 그대로 보여 준다. 필기의 시작이 「유저리스트, 보드리스트, 프로젝트리스트는 모두 동일한 코드를 사용한다. 메서드에 넘기는 매개변수만 차이를 보인다」다 — **같은 메서드가 세 번 복사돼 있었다.**

```java
  private <E> void loadJson(List<E> list, String filename, Class<E> elementType) {
    try (BufferedReader in = new BufferedReader(new FileReader(filename))) {
      StringBuilder strBuilder = new StringBuilder();
      String line;
      while ((line = in.readLine()) != null) {
        strBuilder.append(line);
      }

      list.addAll((List<E>) new GsonBuilder().setDateFormat("yyyy-MM-dd HH:mm:ss").create()
          .fromJson(strBuilder.toString(),
              TypeToken.getParameterized(List.class, elementType).getType()));
      ...
```

```java
  private void loadData() {
    loadJson(userList, "user.json", User.class);
    loadJson(projectList, "porject.json", Project.class);
    loadJson(boardList, "board.json", Board.class);
  }
```

**메서드 셋이 하나가 되고, 달라지던 것이 인수 목록으로 올라왔다.** `List<E> list` 와 `Class<E> elementType` 가 **같은 `E`** 라는 것이 이 시그니처의 핵심이다 — `loadJson(userList, "user.json", Board.class)` 는 컴파일되지 않는다. 목록과 타입 정보가 짝이 맞는지를 **컴파일러가 검사**한다 → [[json]] · [[class-metadata]]

`Class<E>` 를 따로 받는 이유는 실행 시점에 `E` 가 무엇인지 알 방법이 없기 때문이다 → [[type-erasure]]

배열을 다루는 제네릭 메서드는 원소 타입을 몰라도 자리만 바꾼다.

```java
  static <T> T[] reverse2(T[] arr) {
    for (int i = 0; i < arr.length / 2; i++) {
      T temp = arr[i];
      int targetIndex = arr.length - 1 - i;
      arr[i] = arr[targetIndex];
      arr[targetIndex] = temp;
    }
    return arr;
  }
```

**`T temp` 한 줄이 이 메서드가 제네릭인 이유다.** `Object temp` 로도 돌아가지만 그러면 반환 타입이 `Object[]` 가 되어 받는 쪽이 캐스팅해야 한다 → [[array]] · [[type-casting]]

## 왜 중요한가

**같은 코드를 타입마다 복사하지 않아도 된다.** 이 실습에서 `loadJson`·`saveJson` 이 세 벌에서 한 벌로 줄었다. 복사돼 있으면 날짜 형식을 바꿀 때 세 곳을 고쳐야 하고, **한 곳을 빠뜨리는 날 파일 세 개의 형식이 갈린다** → [[refactoring]]

**오류가 실행 시점에서 컴파일 시점으로 옮겨 온다.** 제네릭이 없던 시절의 대안은 `Object` 로 받는 것이었고, 그러면 `List` 에 아무것이나 들어간 뒤 꺼내는 자리에서 `ClassCastException` 이 났다 — **넣은 코드와 터지는 코드가 멀다.** 제네릭은 넣는 자리에서 막는다.

```java
List<String> arr = new ArrayList<>();
arr.add("String");
//arr.add(new Integer(100)) -> 불가능
String s = arr.get(0); // (String으로 캐스팅을 안해도됨)
```

**꺼내는 자리의 캐스팅이 사라진다.** Day39 의 `(List<User>) in.readObject()` 처럼 손으로 쓴 캐스팅은 컴파일러가 검사하지 못하는 약속이었는데, 제네릭은 그 약속을 시그니처에 적어 **검사되는 것으로 바꾼다** → [[serialization]] · [[type-casting]]

## 경계와 오해

- **Day40 의 `Box<Integer>` 예시는 컴파일되지 않는다 — 출력 주석은 실행된 결과가 아니다** — 「1. Generic의 개념」의 코드가 `Box<Integer> boxInt = new Box<>();` 를 만든 다음 **`boxInt` 가 아니라 `box` 에** `box.set(1);` 을 부른다. `box` 는 `Box<String>` 이므로 `set(String)` 이고, `1` 은 `int`→`Integer` 로 오토박싱돼도 `String` 이 아니다 → **`incompatible types: int cannot be converted to String` 컴파일 오류.** 파일 전체가 컴파일되지 않으므로 앞줄의 `//안녕하세요` 조차 실제로 찍힌 적이 없고, `boxInt` 는 만들어져서 아무도 쓰지 않는다. **이 오류가 바로 이 절이 자랑하려던 성질의 증거다** — 제네릭이 없었다면 `set(Object)` 라서 이 줄이 통과했고, `String s = (String) box.get()` 에서 `ClassCastException` 이 났을 것이다. **막아 주는 것을 보여 주려던 코드가 실제로 막혔다** → [[autoboxing]] · [[type-casting]]
- **제네릭 ≠ `Object` 로 받는 것** — 둘 다 「아무 타입이나 담는다」로 보이지만 검사 시점이 다르다. `Object` 는 담을 때 아무것도 검사하지 않고 꺼낼 때 캐스팅을 요구하며 실패가 실행 중에 난다. 제네릭은 **담을 때 검사하고 꺼낼 때 캐스팅이 없다.** 실행 시점의 바이트코드는 사실 거의 같다 — 컴파일러가 캐스팅을 대신 넣어 주는 것이기 때문이다 → [[type-erasure]]
- **`Box<String>` 은 `Box<Object>` 가 아니다 — 상속이 타입 인자로 전파되지 않는다** — `String extends Object` 인데 `Box<String>` 을 `Box<Object>` 자리에 넣을 수 없다. Day40 이 「컴파일 과정에서 T가 결정되면 바꿀수 없다」로 적은 성질이고, 그 제약을 풀기 위한 문법이 와일드카드다 → [[wildcard-type]] · [[polymorphism]]
- **타입 파라미터에 기본 타입을 넣을 수 없다** — `Box<int>` 는 컴파일되지 않고 `Box<Integer>` 로 써야 한다. Day40 의 예시가 `Box<Integer>` 인 것이 취향이 아니라 문법이다. 그래서 제네릭 컨테이너에 숫자를 담을 때마다 박싱 비용이 붙는다 → [[wrapper-class]] · [[autoboxing]] · [[data-type]]
- **`static` 메서드는 클래스의 타입 파라미터를 쓸 수 없다 — Day40 의 두 `<T>` 가 남남인 이유** — 클래스의 `T` 는 **인스턴스를 만들 때** 정해지는데 `static` 메서드는 인스턴스 없이 불린다. 그래서 `static` 메서드에서 타입을 비우려면 **메서드 자신의 타입 파라미터를 따로 선언**(`static <T> T[] create2(T[] arr)`)해야 하고, 그것이 반환 타입 앞의 `<T>` 다. 이름이 같아서 물려받은 것처럼 보이는데 **가려진 별개 이름**이다 → [[static-member]] · [[variable-scope]]
- **`create3` 의 `<T>` 는 인수와 묶여 있지 않다 — 컴파일되는데 실행에서 터진다** — 필기의 `static <T> T[] create3(Class<?> type)` 는 `T` 가 **매개변수 어디에도 나오지 않는다.** 그래서 컴파일러는 T 를 **대입 대상에서만** 추론하고, `String[] arr = create3(Integer.class);` 가 **경고 없이 컴파일된 다음 실행에서 `ClassCastException`** 을 낸다(`Array.newInstance` 가 만든 `Integer[]` 를 `String[]` 변수에 대입하는 자리에서 터진다). 필기 코드가 `create3(String.class)` 만 불러서 드러나지 않았다. 답은 `Class<T> type` 으로 받아 **인수와 반환 타입을 같은 T 로 묶는 것**이고, 그러면 어긋난 호출이 컴파일 오류가 된다. **제네릭의 값은 「타입 파라미터를 썼다」가 아니라 「어긋날 수 있는 두 자리를 같은 이름으로 묶었다」에서 나온다** — 같은 필기의 `loadJson(List<E>, String, Class<E>)` 는 그것을 제대로 했다 → [[type-erasure]] · [[class-metadata]]
- **제네릭으로 배열을 만들 수 없다** — `new T[10]` 은 컴파일 오류이고, 필기가 그 우회로 넷을 나열한다(`Arrays.copyOf` 로 견본 복제 · `Array.newInstance` 로 타입 정보 받기 · 배열에서 타입 정보 추출). **이유는 배열이 실행 시점에 원소 타입을 들고 있는데 제네릭은 그러지 않기 때문**이고, 그 자리 전체가 [[type-erasure]] 의 이야기다 → [[array-copy]]
- **타입 파라미터가 있어도 여전히 검사되지 않는 캐스팅이 남는다** — `loadJson` 의 `(List<E>)` 와 `create3` 의 `(T[])` 는 컴파일러가 확인할 수 없는 형변환이라 unchecked 경고가 난다. **제네릭을 쓴다는 것이 캐스팅이 없어진다는 뜻은 아니고**, 라이브러리 경계처럼 타입을 잃는 자리에서는 그것이 남는다 → [[type-casting]]
- **제네릭은 문서가 아니라 검사다** — 시그니처에 `<E>` 를 적었다고 그 코드가 안전해지지 않는다. `intintSeqNo(List<E> list, Class<E> elementType)` 는 안에서 `(InitSeqNo) element` 로 캐스팅하고 `getMethod("initSeqNo", int.class)` 로 **이름 문자열**을 찾는다 — 「E 는 `InitSeqNo` 를 구현하고 `static initSeqNo(int)` 를 가진 타입」이라는 진짜 계약은 **타입으로 표현되지 않았고 실행 시점에만 확인된다.** `<E extends InitSeqNo>` 로 앞의 절반은 타입에 올릴 수 있지만, **`static` 메서드의 존재는 인터페이스로 강제할 수 없어서** 나머지 절반은 끝까지 리플렉션에 남는다 → [[interface]] · [[class-metadata]]
- **타입 파라미터 이름이 클래스 이름을 가린다** — `class Box<T>` 안에서 `T` 는 어떤 실제 클래스도 가리키지 않는다. 그런데 `T` 라는 이름의 클래스가 실제로 있다면 그 안에서는 접근할 수 없어진다. `T`·`E` 같은 한 글자 관례가 이 사고를 사실상 없앤 셈이다 → [[variable-scope]]

## 함께 보는 개념

- [[type-erasure]] — 이 문법이 실행 시점에 남기지 않는 것
- [[wildcard-type]] — `Box<String>` ≠ `Box<Object>` 를 우회하는 문법
- [[raw-type]] — 타입 인자를 안 적었을 때 남는 옛 문법
- [[parameterization]] — 같은 일을 값에 대해 하는 리팩터링
- [[type-casting]] — 제네릭이 없애는 것과 여전히 남는 것
- [[wrapper-class]] — 기본 타입을 타입 인자로 쓰기 위한 통로
- [[autoboxing]] — 그 변환이 자동으로 일어나는 자리
- [[array]] — 제네릭과 규칙이 다른 컨테이너
- [[array-copy]] — 제네릭 배열을 만드는 우회로
- [[class-metadata]] — 실행 시점에 타입을 넘기는 방법
- [[json]] — 이 실습에서 제네릭을 쓴 대상
- [[dynamic-array]] — `List<E>` 가 구현되는 자료구조
- [[refactoring]] — 세 벌을 한 벌로 만든 동작
- [[method]] — 타입 파라미터가 붙는 자리

## 출처

- [[2024-07-22-Day40]] — 「결정되지 않은 타입을 파라미터로 처리하고 실제 사용할 때 구체적인 타입으로 대체」로 정의하고, `Box<T>`(클래스 타입 파라미터)와 `static <T> T[] reverse2(T[])`(메서드 타입 파라미터)를 나란히 보여 준다. 특징으로 「다루는 타입을 제한할 수 있다」·「캐스팅에서 자유롭다」를 들고 `List<String>` 에 `Integer` 를 넣지 못하는 예를 적었다. 「배열 만들기」 절이 `new T[10]` 이 불가능한 것과 우회로 넷(`Arrays.copyOf` · `Array.newInstance` · `getComponentType`)을 보여 주는데, `create3(Class<?> type)` 는 T 를 인수와 묶지 않아 실행 시점 `ClassCastException` 이 가능한 형태다. 실습 프로젝트에서는 세 벌로 복사돼 있던 저장·로딩을 `<E> loadJson(List<E>, String, Class<E>)`·`<E> saveJson(List<E>, String)` 한 벌로 합친다. 「1. Generic의 개념」 코드는 `Box<Integer>` 를 만들고 `Box<String>` 에 `1` 을 넣어 **컴파일되지 않는다**
