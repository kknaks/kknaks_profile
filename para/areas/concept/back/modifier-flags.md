---
type: concept
id: modifier-flags
title: 접근 플래그 비트마스크 (getModifiers 와 Modifier)
aliases:
  - getModifiers
  - Modifier
  - access flags
  - 접근 플래그
  - 접근플래그
  - modifier 비트
  - 수정자 비트
up:
  - 2024-08-20-Day59
tags:
  - java
  - 리플렉션
  - 비트연산
  - jvm
---

# 접근 플래그 비트마스크 (getModifiers 와 Modifier)

**`public`·`static`·`final` 같은 지정자들이 클래스 파일 안에서는 정수 하나의 비트로 저장되어 있고, `getModifiers()` 가 그 정수를 그대로 돌려준다는 것.** 「이 메서드는 `public` 인가」를 묻는 일이 결국 **비트 하나가 켜져 있는지 보는 일**이다. Day59 가 「modifier 타입 (public, static, protected)」 절에서 그 정수를 32칸 이진수로 찍어 눈으로 확인한다 → [[bitwise-operator]] · [[access-modifier]]

## 정의

지정자마다 비트 한 칸이 배정돼 있다. `Modifier` 클래스의 상수가 그 값이다.

| 상수 | 값 | 비트 |
|---|---|---|
| `Modifier.PUBLIC` | `0x0001` | 0번 |
| `Modifier.PRIVATE` | `0x0002` | 1번 |
| `Modifier.PROTECTED` | `0x0004` | 2번 |
| `Modifier.STATIC` | `0x0008` | 3번 |
| `Modifier.FINAL` | `0x0010` | 4번 |
| `Modifier.SYNCHRONIZED` | `0x0020` | 5번 |
| `Modifier.NATIVE` | `0x0100` | 8번 |
| `Modifier.ABSTRACT` | `0x0400` | 10번 |

**여러 지정자가 붙은 것은 비트를 함께 켠 것**이라, `public static final` 은 `0x0019` 다. 순서 정보는 없다 — `static public` 과 `public static` 이 같은 정수가 되는 이유가 이것이다 → [[bit-shift]]

읽는 법이 둘이고 Day59 가 둘을 같은 코드 안에 나란히 썼다.

```java
int modifiers = m.getModifiers();

if (Modifier.isPublic(modifiers)) { // (modifiers & Modifier.PUBLIC) == Modifier.PUBLIC)
  System.out.print(" public");
} else if ((modifiers & PROTECTED) != 0) {
  System.out.print(" protected");
}
```

필기가 그 선택을 세 줄로 정리했다 — 「public, static, protected에 할당된 비트와 호출한 객체와 비트 연산(&)을 통해 해당 객체의 modifier타입을 추출한다」·「reflect에 내장된 isModifier()를 통해 modifier타입을 추출한다」·「비트 연산자가 속도 측면에서 유리하고 내장함수가 시인성 측면에서 유리하다」. **마지막 줄이 이 노트의 첫 「경계와 오해」다.**

## 사용 예시

Day59 가 `String` 의 모든 메서드를 훑으며 지정자 비트를 이진수로 찍는다.

```java
public static void main(String[] ok) {
  Class<?> clazz = String.class;

  Method[] methods = clazz.getDeclaredMethods();
  for (Method m : methods) {
    System.out.printf("%s() => ", m.getName());

    int modifiers = m.getModifiers();

    System.out
        .println(String.format("%32s", Integer.toBinaryString(modifiers)).replace(' ', '0'));

    if (Modifier.isPublic(modifiers)) {
      System.out.print(" public");
    } else if ((modifiers & PROTECTED) != 0) {
      System.out.print(" protected");
    } else if ((modifiers & PRIVATE) != 0) {
      System.out.print(" private");
    }

    // if ((modifiers & STATIC) != 0)
    if (Modifier.isStatic(modifiers)) {
      System.out.print(" static");
    }

    if ((modifiers & FINAL) != 0) {
      System.out.print(" final");
    }

    System.out.println();
  }
}
```

**출력 한 줄을 만드는 데 두 걸음이 필요한 것이 눈여겨볼 자리다.**

```java
String.format("%32s", Integer.toBinaryString(modifiers)).replace(' ', '0')
```

`Integer.toBinaryString(9)` 은 `"1001"` 이고 **앞의 0을 버린다.** 그래서 폭을 32로 맞춰 오른쪽 정렬하고(`%32s`), 그때 생긴 공백을 `0` 으로 바꾼다. 32라는 숫자는 `int` 라서 그 이상이 될 수 없다 — **자리 수가 타입에서 나온다** → [[format-string]] · [[twos-complement]]

## 왜 중요한가

**「예/아니오 여러 개」를 정수 하나에 담는 형태를 처음 실물로 본다.** 클래스 파일의 `access_flags` 가 그렇고, 파일 권한(`chmod 644`)·이벤트 마스크·정규식 플래그(`Pattern.CASE_INSENSITIVE`)가 전부 같은 모양이다. Day10·Day38 에서 배운 `&`·`|` 가 **연습 문제가 아니라 남이 만든 API 의 규약**으로 나타나는 자리다 → [[bitwise-operator]] · [[class-file-format]]

**그리고 리플렉션으로 무언가를 판정하려면 이 값이 필요하다.** 「`static` 메서드면 `invoke(null, …)` 로 부른다」를 코드로 쓰려면 `Modifier.isStatic(m.getModifiers())` 를 물어야 하고, 「setter 만 골라 부른다」·「`transient` 필드는 직렬화에서 빼자」도 전부 이 정수를 읽는 일이다 — **필드·메서드 목록을 훑는 코드는 예외 없이 이 물음을 갖는다** → [[reflective-invocation]] · [[reflective-field-access]] · [[serialization]]

## 경계와 오해

- **「비트 연산자가 속도 측면에서 유리하다」는 성립하지 않는다** — `Modifier.isPublic(int mod)` 의 본문은 **`return (mod & PUBLIC) != 0;` 한 줄**이다. 즉 손으로 쓴 비트 연산과 **같은 연산을 그대로 감싼 것**이고, `static` 메서드라 JIT 가 인라인해서 기계어에서는 구별이 없어진다. 따라서 이 자리는 「시인성 대 속도」의 저울이 아니라 **한쪽이 이유 없이 읽기 어려운 것**이다. 「저수준이 빠르다」는 감각이 표준 라이브러리의 얇은 래퍼에 적용되면 이렇게 어긋난다 → [[bytecode]]
- **`& 마스크 != 0` 과 `& 마스크 == 마스크` 는 단일 비트에서만 같다** — 필기가 주석에 `(modifiers & Modifier.PUBLIC) == Modifier.PUBLIC` 형태를 적었고 `PUBLIC` 은 비트가 하나라 결과가 같다. 그러나 여러 비트를 묶은 마스크에서는 **`!= 0` 은 「하나라도 켜짐」, `== 마스크` 는 「전부 켜짐」**으로 갈린다. 두 표기를 같은 것으로 외우면 마스크를 합쳐 쓰는 첫 순간에 어긋난다 → [[bitwise-operator]]
- **`else if` 로 이어 놓은 것이 맞는 이유는 비트가 배타적이기 때문이 아니다** — 접근 지정자 셋을 `else if` 로 이었는데 결과는 맞다. 다만 근거는 **자바 문법이 셋 중 하나만 허용한다**는 것이고 비트 구조 자체는 셋을 동시에 켜는 것을 막지 않는다(클래스 파일을 직접 만들면 가능하고 검증기가 거부한다). 그리고 **package-private 은 셋이 전부 0** 이라 아무것도 찍히지 않아 **출력이 빈칸**이다 — `String` 의 메서드에는 실제로 그런 것이 있어서 이 코드가 돌면 이름만 있고 지정자가 없는 줄이 나온다. 「4가지 중 하나」로 배운 [[access-modifier]] 의 네 번째가 **비트로는 「없음」**이라는 것이 여기서 드러난다.
- **`PROTECTED`·`PRIVATE`·`FINAL` 이 클래스명 없이 쓰여 있다** — `Modifier.PROTECTED` 를 `import static` 하지 않으면 컴파일되지 않는다. 같은 코드 안에서 `Modifier.isPublic`·`Modifier.isStatic` 은 한정해 쓰고 상수만 벗겨 놓아 **두 표기가 섞여 있고**, 그대로 옮겨 쓰면 `cannot find symbol` 이다 → [[static-member]] · [[package]]
- **소제목의 「public, static, protected」가 담기는 것의 일부다** — `getModifiers()` 에는 `final`·`synchronized`·`native`·`abstract`·`strictfp`(메서드), `transient`·`volatile`(필드), `interface`·`enum`(클래스)까지 들어 있다. 필기가 셋만 적었지만 코드는 `final` 도 검사하므로 스스로 넷을 다룬다. **`String` 의 메서드에는 `native` 가 실제로 있어서**(`intern()`) 이진수 출력에 8번 비트가 켜진 줄이 나오는데, 이 코드는 그 비트를 해석하지 않아 화면에 아무 말도 남지 않는다 → [[platform-dependency]]
- **소스에 안 쓴 플래그가 나타난다** — 인터페이스의 메서드는 `public abstract` 가 암묵으로 붙고, `enum` 상수는 `public static final` 이고, 중첩 인터페이스는 `static` 이다. **`getModifiers()` 는 「내가 쓴 것」이 아니라 「컴파일된 결과」를 준다** — [[nested-class]] 회차가 「중첩 인터페이스에는 `static` 을 쓸 필요가 없다 — 언제나 `static` 이다」로 적은 것이 이 정수에서 확인된다 → [[interface]]
- **`Modifier.toString(int)` 이 이미 있다** — 필기가 `if` 다섯 개로 조립한 출력을 한 줄로 만들어 주고, 순서까지 자바 언어 명세의 관례대로 맞춰 준다(`public static final`). **「표준 라이브러리에 이미 있는가」를 묻지 않고 손으로 만든 자리**이고, 손으로 만든 대가가 위의 「빈칸 출력」과 「해석하지 않은 `native`」다.
- **`Modifier.isPublic(clazz.getModifiers())` 와 「밖에서 쓸 수 있는가」는 다른 질문이다** — 플래그는 **그 선언 하나**의 것이라, `public` 중첩 클래스가 `private` 바깥 클래스 안에 있으면 플래그는 `public` 인데 밖에서는 쓸 수 없다. 「실제로 접근 가능한가」는 [[reflective-field-access]] 처럼 시도해 보거나 `canAccess` 로 물어야 한다 → [[nested-class]]
- **클래스의 플래그와 멤버의 플래그가 다른 집합이다** — 클래스에는 `ACC_SUPER`·`ACC_INTERFACE`·`ACC_ENUM` 같은 것이 있고 `static`·`final` 의 뜻도 다르다([[nested-class]] 노트의 첫 항목 — 클래스의 `static` 은 「바깥 인스턴스 참조가 없다」). `Modifier.classModifiers()`·`methodModifiers()` 로 각 자리에 올 수 있는 마스크를 물을 수 있는데, 필기는 메서드만 훑어 이 구분에 닿지 않았다 → [[static-member]]
- **음수가 되지 않는 이유가 우연이다** — 32비트를 다 쓰지 않고 아래쪽 비트만 쓰므로 최상위 비트가 켜지지 않아 `getModifiers()` 는 항상 양수다. 그래서 `Integer.toBinaryString` 이 보수 표기를 내지 않고 필기의 32칸 출력이 앞부분이 전부 0 으로 나온다. **`int` 를 플래그 그릇으로 쓰면 32칸이 상한**이고, 그것이 부족해지는 API 는 `long` 이나 `EnumSet` 으로 간다 → [[twos-complement]] · [[overflow]]

## 함께 보는 개념

- [[bitwise-operator]] — `&` 로 비트를 확인하는 문법
- [[bit-shift]] — 비트 자리를 정하는 연산
- [[access-modifier]] — 이 정수가 표현하는 문법
- [[class-file-format]] · [[bytecode]] — 이 정수가 실제로 저장되는 자리
- [[reflective-invocation]] — `static` 여부를 물어야 하는 자리
- [[reflective-field-access]] — 필드의 지정자를 되읽는 자리
- [[class-metadata]] — 이 값을 꺼내는 출발점
- [[static-member]] — 같은 키워드가 자리마다 다른 뜻을 갖는 축
- [[nested-class]] — 암묵 플래그가 붙는 대표 자리
- [[interface]] — 안 쓴 `public abstract` 가 나타나는 곳
- [[format-string]] — 32칸 0채움 출력을 만드는 문법
- [[twos-complement]] · [[overflow]] — 32칸이 상한인 이유
- [[serialization]] — `transient` 비트를 읽는 다른 층
- [[annotation]] — 같은 「선언에 붙는 메타데이터」인데 개수가 고정되지 않은 형태

## 출처

- [[2024-08-20-Day59]] — 「타입정보 추출」의 마지막 절 「modifier 타입 (public, static, protected)」에서 `m.getModifiers()` 가 돌려주는 정수를 `String.format("%32s", Integer.toBinaryString(modifiers)).replace(' ', '0')` 로 **32칸 이진수로 찍어** 지정자가 비트라는 것을 눈으로 확인했다. 읽는 법이 두 가지(`(modifiers & PROTECTED) != 0` 와 `Modifier.isStatic(modifiers)`)라는 것을 같은 코드에 나란히 쓰고 「비트 연산자가 속도 측면에서 유리하고 내장함수가 시인성 측면에서 유리하다」로 저울을 세웠다 — **그 저울이 이 노트가 뒤집는 첫 항목**이며, `Modifier.isPublic` 의 본문이 같은 비트 연산 한 줄이라 속도 차이가 없다. 그 밖에 `PROTECTED`·`PRIVATE`·`FINAL` 이 `Modifier.` 없이 쓰여 그대로는 컴파일되지 않고, package-private 메서드에서는 출력이 빈칸이 되며, `native`·`abstract` 같은 다른 비트와 `Modifier.toString(int)` 의 존재는 다루지 않았다
