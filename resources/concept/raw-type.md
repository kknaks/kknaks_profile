---
type: concept
id: raw-type
title: 원시 타입 (Raw Type)
aliases:
  - 원시 타입
  - 원시타입
  - raw type
  - rawtype
  - 로우 타입
  - 다이아몬드 연산자
  - diamond operator
up:
  - 2024-07-22-Day40
tags:
  - java
  - 타입
  - 문법
  - 호환성
---

# 원시 타입 (Raw Type)

**제네릭 클래스를 타입 인자 없이 쓴 것.** `ArrayList<String> list` 가 아니라 `ArrayList list` 라고 쓴 그 상태다. 문법 오류가 아니고 경고만 나는데, 그 이유는 하나뿐이다 — **제네릭이 Java 5 에 들어왔고 그 전에 쓰인 코드가 그대로 컴파일돼야 했기 때문**이다. 즉 이것은 기능이 아니라 **남겨 둔 문**이다 → [[generics]] · [[type-erasure]]

> 이름이 헷갈리는 자리다. Java 에서 「primitive type」도 **원시 타입**으로 번역되는데 그것은 `int`·`double` 같은 기본 타입이고, 여기서 말하는 raw type 은 **타입 인자를 지운 제네릭 타입**이다. 둘은 아무 관계가 없다 → [[data-type]]

## 정의

Day40 은 참조 선언 세 가지를 나란히 놓아 raw type 의 자리를 잡는다. **선언에 무엇을 적었는지가 두 가지를 동시에 정한다** — 어떤 객체를 대입할 수 있는지, 그리고 어떤 값을 넣을 수 있는지.

| 선언 | 대입할 수 있는 객체 | `add(...)` 할 수 있는 것 | 검사 |
|---|---|---|---|
| `ArrayList list` (raw) | 전부 (`<String>`·`<Member>`·…) | **전부** | **없다** (경고만) |
| `ArrayList<?> list` | 전부 | **없다** (`null` 만) | 있다 → [[wildcard-type]] |
| `ArrayList<Object> list` | `<Object>` 로 만든 것만 | 전부 | 있다 |

**raw 와 `<Object>` 가 「아무거나 넣을 수 있다」에서 같아 보이는데 대입 규칙이 반대다.** `ArrayList<Object>` 는 `new ArrayList<String>()` 을 거부하고, raw 는 다 받는다. 그래서 raw 는 「`Object` 로 쓰는 것」이 아니라 **「검사를 끄는 것」**이다.

필기가 그 성질을 자기 말로 적었다.

```text
레퍼런스를 선언 하지 않으면 원시타입 그대로 사용하여,
모든 타입에 대한 객체를 생성할 수 있고, 메서드 파라미터에 모든 타입을 사용할 수 있다.
```

## 사용 예시

```java
    // 레퍼런스를 선언할 때 제네릭 타입을 지정하지 않으면
    // 객체 생성시 어떤 제네릭 타입을 지정하더라도 상관없다.
    ArrayList list1;
    list1 = new ArrayList<Member>(); // OK

    //=> 레퍼런스를 선언할 때 제네릭 타입을 지정하지 않으면
    //   ArrayList 객체를 생성할 때 지정한 제네릭 타입은 무시된다.
    list1.add(new String());
    list1.add(new Integer(100));
    list1.add(new java.util.Date());
    list1.add(new Member("홍길동", 20));
```

**`new ArrayList<Member>()` 로 만든 목록에 `String`·`Integer`·`Date` 가 들어간다.** 컴파일러는 unchecked 경고만 내고 통과시킨다. 이 목록을 나중에 `List<Member>` 로 받아 `for (Member m : list)` 를 돌리면 **첫 원소에서 `ClassCastException`** 이고, 터지는 자리는 넣은 코드가 아니라 **읽는 코드**다 → [[type-casting]] · [[exception-handling]]

그리고 같은 필기가 반대쪽을 옳게 잡아 두었다.

```java
    ArrayList<Object> list1;
    //    list1 = new ArrayList(); // 이렇게 사용하지 말고, 명확히 제네릭의 타입을 지정하라.
    list1 = new ArrayList<Object>();
    list1 = new ArrayList<>();
```

**`new ArrayList<>()` 와 `new ArrayList()` 는 다르다** — 앞은 타입 인자를 컴파일러가 채우는 것이고 뒤가 raw 다 → 아래 「경계와 오해」

## 왜 중요한가

**경고를 무시하면 제네릭을 쓴 값이 0 이 된다.** 목록 선언 한 줄에서 `<Member>` 를 빼먹으면 그 목록에 대한 검사가 전부 사라지고, 남는 것은 **캐스팅을 손으로 쓰던 Java 5 이전의 코드**다. 컴파일이 되기 때문에 **테스트가 없으면 그 사실이 드러나지 않는다** — 실패는 나중에, 다른 파일에서 나타난다.

**옛 코드와 새 코드를 섞을 수 있게 한다.** 제네릭 이전 라이브러리를 부르는 코드가 컴파일되는 이유이고, 실무에서 오래된 프로젝트를 만질 때 unchecked 경고가 잔뜩 뜨는 이유다. **경고를 「소음」으로 볼지 「아직 안 옮긴 코드의 목록」으로 볼지가 갈리는 자리** → [[compilation]]

**같은 문법이 두 시대를 가리키는 것을 알게 된다.** Day21 필기의 `Class classInfo = obj1.getClass();` 도 raw type 이었다 — 그때는 「그냥 쓰는 방법」으로 보였지만 Day40 을 지난 뒤에는 **`Class<?>` 를 안 적은 상태**로 읽힌다. Day40 의 `create3(Class<?> type)`·`getInterfaces()` 가 `Class<?>` 를 쓰는 것이 그 교정이다 → [[class-metadata]]

## 경계와 오해

- **`new ArrayList()` ≠ `new ArrayList<>()`** — 빈 꺾쇠(다이아몬드 연산자)는 **타입 인자를 생략한 것이 아니라 추론하게 맡긴 것**이다. `List<String> a = new ArrayList<>();` 의 오른쪽은 `ArrayList<String>` 이고 raw 가 아니다. 반면 `new ArrayList()` 는 raw 라서 대입하는 순간 unchecked 경고가 난다. **두 글자 차이로 검사가 켜졌다 꺼진다** → [[generics]]
- **「객체 생성 시 지정한 제네릭 타입은 무시된다」는 반만 맞다** — 필기의 이 문장은 결과는 맞지만 원인이 어긋나 있다. **애초에 객체는 타입 인자를 들고 있지 않다** — `new ArrayList<Member>()` 로 만든 것과 `new ArrayList<String>()` 로 만든 것은 실행 시점에 완전히 같은 객체다([[type-erasure]]). 무시하는 주체는 「객체」가 아니라 **컴파일러의 검사**이고, 그 검사는 **참조의 선언 타입**으로 이뤄진다. 그래서 같은 객체를 raw 참조로 보면 검사가 없고 `List<Member>` 참조로 보면 검사가 있다 — **타입은 객체에 붙어 있지 않고 그것을 보는 눈에 붙어 있다.**
- **raw 참조를 쓰면 그 타입의 제네릭이 전부 함께 지워진다** — 관계없는 멤버까지 그렇다. `ArrayList list; Iterator it = list.iterator();` 의 `it` 은 `Iterator<Member>` 가 아니라 **raw `Iterator`** 이고, `it.next()` 의 반환 타입도 `Object` 가 된다. **한 줄의 raw 가 그 줄 아래로 전파된다** → [[iterator-pattern]]
- **raw type ≠ `<Object>`** — 위 표의 대입 규칙이 반대다. 「아무거나 담고 싶으면 `<Object>`」가 답이고, 그러면 꺼낼 때 `Object` 라는 것이 **타입에 적혀 있어** 캐스팅을 잊지 않는다. raw 는 그 사실조차 감춘다.
- **raw type ≠ `<?>`** — 대입은 둘 다 자유롭지만 `add` 는 raw 가 전부 허용, `<?>` 가 전부 거부다. **정확히 반대편**이고, 필기의 두 절을 「타입을 안 적은 두 방법」으로 뭉치면 거꾸로 이해한다 → [[wildcard-type]]
- **컴파일 오류가 아니라 경고다 — 그것이 위험의 전부다** — 오류라면 고치고 지나갔을 것이다. 경고는 빌드를 막지 않아 **몇 년을 남는다.** `-Xlint:unchecked` 로 자세히 보고 `-Werror` 로 오류로 승격하는 것이 정공법이고, `@SuppressWarnings("unchecked")` 는 「검사가 없는 것을 내가 보증한다」는 선언이라 **그 자리에 왜 안전한지 주석이 필요하다** → [[annotation]]
- **`new Integer(100)` 은 Java 9 부터 권장되지 않는다** — 필기 코드에 그대로 있는데 지금은 `Integer.valueOf(100)` 이나 오토박싱(`list.add(100)`)을 쓴다. 생성자는 매번 새 객체를 만들고 `valueOf` 는 작은 값을 캐시하기 때문이다. raw type 과 함께 **제네릭 이전 스타일이 한 줄에 두 개 겹쳐 있는** 자리다 → [[autoboxing]] · [[wrapper-class]]
- **필기의 `list1` 이 두 절에서 다른 타입이다** — 「원시타입」절의 `ArrayList list1` 과 「Object로 선언」절의 `ArrayList<Object> list1` 이 같은 이름이다. 두 절이 각각 별개 예시라 그런 것이고, 이어 붙이면 컴파일되지 않는다 → [[variable-scope]]

## 함께 보는 개념

- [[generics]] — 타입 인자를 적었을 때 얻는 것
- [[wildcard-type]] — 「모른다」를 타입으로 적는 반대편 선택
- [[type-erasure]] — raw type 이 남아 있을 수 있는 이유
- [[type-casting]] — raw 로 담은 것을 꺼낼 때 다시 필요해지는 것
- [[class-metadata]] — `Class` 를 raw 로 쓰던 옛 필기와의 연결
- [[autoboxing]] — 같은 코드에 겹쳐 있는 옛 스타일
- [[wrapper-class]] — `new Integer(100)` 이 만드는 것
- [[compilation]] — 경고와 오류가 갈리는 자리
- [[annotation]] — `@SuppressWarnings` 로 경고를 끄는 통로
- [[iterator-pattern]] — raw 가 전파되는 대표적 자리
- [[data-type]] — 이름이 겹치는 「기본 타입」쪽

## 출처

- [[2024-07-22-Day40]] — 「파라미터 타입 레퍼런스」절에서 `ArrayList list1`(raw) · `ArrayList<?> list2` · `ArrayList<Object> list1` 세 가지를 나란히 놓고 각각 어떤 객체를 대입할 수 있고 `add` 가 통과하는지를 컴파일 오류 주석으로 비교한다. raw 로 선언하면 「객체 생성 시 지정한 제네릭 타입은 무시된다」고 적고 `new ArrayList<Member>()` 에 `String`·`Integer`·`Date` 를 넣는 코드를 보여 준다 — **검사가 사라진다는 사실은 정확히 봤고, 그것이 객체가 아니라 참조의 선언 타입 때문이라는 것은 다루지 않았다.** `// 이렇게 사용하지 말고, 명확히 제네릭의 타입을 지정하라` 주석으로 raw 를 쓰지 말라는 결론까지 적어 두었다
