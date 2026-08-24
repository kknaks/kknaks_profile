---
type: concept
id: wrapper-class
title: 래퍼 클래스 (Wrapper Class)
aliases:
  - 래퍼 클래스
  - 랩퍼 클래스
  - wrapper
  - wrapper class
  - 포장 클래스
  - Integer
  - valueOf
up:
  - 2024-06-25-Day22
tags:
  - java
  - 자료형
  - 문법
---

# 래퍼 클래스 (Wrapper Class)

기본 타입 값 하나를 **객체로 감싸 주는** 여덟 개의 클래스. 기본 타입은 [[object-class]] 의 자손이 아니라서 객체를 요구하는 자리에 갈 수 없고, 그 경계를 넘게 해 주는 것이 이 클래스들이다 → [[data-type]]

## 정의

기본 타입 여덟 개에 **하나씩** 대응한다.

| 기본 타입 | 래퍼 클래스 |
|---|---|
| `byte` | `Byte` |
| `short` | `Short` |
| `int` | **`Integer`** |
| `long` | `Long` |
| `float` | `Float` |
| `double` | `Double` |
| `boolean` | `Boolean` |
| `char` | **`Character`** |

여섯 개는 첫 글자만 대문자로 바뀌고 **`int` → `Integer`, `char` → `Character` 둘만 이름이 다르다.** 실수가 나는 자리가 정확히 그 둘이다.

`valueOf` 로 만든다.

```java
Byte b2 = Byte.valueOf((byte)100);
Short s2 = Short.valueOf((short)20000);
Integer i2 = Integer.valueOf(3000000);
Long l2 = Long.valueOf(60000000000L);
Float f2 = Float.valueOf(3.14f);
Double d2 = Double.valueOf(3.14159);
Boolean bool2 = Boolean.valueOf(true);
Character c2 = Character.valueOf((char)0x41);
```

## 사용 예시

필기가 이 클래스들이 왜 필요한지를 **메서드 세 개를 만들어 보는 것**으로 보여 준다. 기본 타입만으로는 타입마다 하나씩 만들어야 한다.

```java
static void m(long value) { // byte, short, int, long, char
System.out.printf("long value=%s\n", value);
}
static void m(double value) {// float, double
System.out.printf("double value=%s\n", value);
}
static void m(boolean value) {// boolean
System.out.printf("boolean value=%s\n", value);
}
```

**세 개로 줄어든 것도 이미 [[type-promotion]] 덕분이다** — 주석이 그것을 적어 두었다. `byte`·`short`·`int`·`char` 는 `long` 쪽으로 자동 승격되어 첫 번째를 쓰고, `float` 는 `double` 로 승격된다. 그래도 **`boolean` 은 어디로도 승격되지 않으므로 세 번째가 반드시 남는다.**

래퍼로 감싸면 하나가 된다.

```java
Long obj1 = Long.valueOf(l);
Double obj2 = Double.valueOf(d);
Boolean obj3 = Boolean.valueOf(bool);

m(obj1);
m(obj2);
m(obj3);

static void m(Object value) { // 모든 객체를 받을 수 있다.
System.out.printf("wrapper value=%s\n", value);
}
```

**세 개가 하나로 합쳐진 이유는 `Object` 가 참조 타입 전부의 조상이기 때문**이고, 감싸는 순간 그 계층 안으로 들어오는 것이 래퍼가 하는 일 전부다 → [[method]] · [[polymorphism]] · [[type-casting]]

## 왜 중요한가

**「무엇이든 받는다」를 기본 타입에도 적용할 수 있게 된다.** 컬렉션이 `Object` 를 담는 구조라면 `int` 는 넣을 수 없다. 래퍼가 없으면 `HashSet<int>` 같은 것을 쓸 방법이 아예 없고, 타입마다 저장소를 따로 만들어야 한다 → [[hash-based-collection]]

**그리고 기본 타입에 관한 유틸리티가 살 곳이 생긴다.** `Integer.MAX_VALUE`·`Integer.parseInt(...)`·`Character.isDigit(...)` 은 `int` 나 `char` 가 가질 수 없는 것들이다. 두 주 전 회차에서 `int` 의 한계값을 물으려고 `Integer.MAX_VALUE` 를 쓰면서 「기본 타입에는 메서드가 없다」와 어긋나 보였던 것이 여기서 풀린다 — **부르고 있던 것이 `int` 가 아니라 그 짝인 클래스**였다 → [[data-type]] · [[number-parsing]] · [[static-member]]

## 경계와 오해

- **「인스턴스 변수를 활용할 수 없다」는 표현이 어긋난다** — 필기의 문장인데 「인스턴스 변수」는 클래스가 갖는 **필드**를 뜻하는 용어다. 여기서 말하려던 것은 `int` 값을 **참조 변수에 담을 수 없고 그것에 메서드를 부를 수 없다**는 것이다. 용어를 그대로 받으면 「기본 타입에는 필드를 못 만든다」로 읽혀 엉뚱한 결론이 된다 → [[static-member]] · [[method]]
- **래퍼 인스턴스도 불변이다** — `Integer` 의 값을 나중에 바꿀 수 없다. 「객체로 감쌌으니 안에 든 값을 고칠 수 있겠지」가 안 되고, `m(obj1)` 안에서 값을 바꿔 밖으로 내보내는 것도 불가능하다 → [[immutability]] · [[call-by-value]]
- **`valueOf` 와 `new Integer(...)` 가 같지 않다** — `valueOf` 는 작은 값(`-128`~`127`)에 대해 **미리 만들어 둔 인스턴스를 재사용**하고 `new` 는 부를 때마다 새로 만든다. 그래서 `Integer.valueOf(100) == Integer.valueOf(100)` 은 `true`, `Integer.valueOf(1000) == Integer.valueOf(1000)` 은 `false` 다. **같은 회차 1.1 의 문자열 풀과 정확히 같은 구조의 함정**이고, 값이 작을 때만 `==` 가 맞는 답을 내므로 테스트를 통과한다 → [[string-comparison]] · [[caching]]
- **래퍼끼리는 `==` 가 아니라 `equals`** — 위 항목의 결론이다. 래퍼는 참조 타입이므로 `==` 는 주소를 묻는다. 필기가 `valueOf` 만 쓰고 `==` 비교를 하지 않은 덕분에 이 함정을 만나지 않았다 → [[object-equality]]
- **`Integer` 와 `int` 는 다른 타입이다** — 자동으로 오갈 수 있어서 같아 보이지만, `Integer` 는 `null` 일 수 있고 `int` 는 될 수 없다. 그 차이가 실제로 드러나는 자리가 언박싱이다 → [[autoboxing]]
- **여덟 개 밖에는 래퍼가 없다** — `String` 은 래퍼 클래스가 아니다. 처음부터 참조 타입이라 감쌀 대상이 아니다 → [[data-type]]
- **감싸는 것이 무료가 아니다** — 값 하나를 담기 위해 인스턴스가 생기고 주소를 한 번 더 따라가야 한다. 기본 타입을 쓸 수 있는 자리에서 굳이 래퍼를 쓸 이유는 없다 → [[garbage-collection]]

## 함께 보는 개념

- [[autoboxing]] — 이 변환을 컴파일러가 대신 해 주는 것
- [[data-type]] — 기본 타입과 참조 타입의 경계
- [[object-class]] — 감싸는 순간 들어가게 되는 계층
- [[type-promotion]] — 오버로딩을 세 개로 줄여 주던 규칙
- [[method]] — 세 개가 하나로 합쳐지는 자리
- [[polymorphism]] — `Object` 로 받는 것의 이름
- [[type-casting]] — `Object` 로 받은 것을 되돌리는 일
- [[number-parsing]] — 래퍼가 제공하는 대표 유틸리티
- [[immutability]] — 래퍼 인스턴스의 성질
- [[object-equality]] — `==` 로 비교하면 안 되는 이유
- [[hash-based-collection]] — 기본 타입을 담으려면 래퍼가 필요한 곳

## 출처

- [[2024-06-25-Day22]] — 「primitive type은 객체가 아니므로 인스턴스 변수를 활용할수 없다 / 이를 해결하기 위해 wrapper를 활용」으로 여덟 클래스와 `valueOf` 를 배웠다. `m(long)`·`m(double)`·`m(boolean)` 세 개로 나눠야 하던 메서드가 래퍼로 감싸면 `m(Object)` 하나가 된다는 것이 이 회차가 래퍼의 값을 보여 주는 방식이다
