---
type: concept
id: string-comparison
title: 문자열 비교 (== 와 equals)
aliases:
  - 문자열 비교
  - equals
  - string comparison
  - 문자열 풀
  - string interning
  - 인터닝
  - String const pool
  - identityHashCode
up:
  - 2024-06-11-Day11
  - 2024-06-11-Day12
  - 2024-06-18-Day17
  - 2024-06-24-Day21
  - 2024-06-25-Day22
tags:
  - java
  - 문자열
  - 문법
---

# 문자열 비교 (== 와 equals)

`==` 는 **주소**를 비교하고 `.equals()` 는 **내용**을 비교한다. 문자열은 기본 타입이 아니라 인스턴스이므로, `==` 로 비교하면 "내용이 같은가"가 아니라 "같은 인스턴스인가"를 묻게 된다.

## 정의

| 비교 | 묻는 것 | 대상 |
|---|---|---|
| `==` | 두 [[object-reference]] 가 **같은 인스턴스**를 가리키는가 | 모든 타입 |
| `.equals()` | 두 인스턴스의 **내용**이 같은가 | 레퍼런스 타입만 |

기본 타입(`int`·`char`…)은 값을 직접 담으므로 `==` 가 곧 값 비교다. 갈리는 것은 레퍼런스 타입뿐이다.

## 사용 예시

이 필기가 같은 조건을 두 번 다르게 썼다. 먼저 `==` 로 썼고,

```java
for (int i = 0; i < menus.length; i++) {
    if (menus[i] == "종료") {          // 4.2 — 그런데 동작했다
        // 빨간색 볼드로 출력
    }
}
```

뒤에서 `.equals()` 로 고쳤다.

```java
for (String menu : menus){
    if (menu.equals("종료")) {         // 4.4 — 이렇게 바뀌었다
        // 빨간색 볼드로 출력
    }
}
```

**바꾼 이유가 필기에 적혀 있지 않은데, 앞의 코드가 실제로 잘 동작했기 때문이다.** `menus` 를 문자열 리터럴로 채웠고, 같은 내용의 리터럴은 컴파일 시점에 [[constant-pool]] 에 한 번만 들어가 실행 시점에 **같은 인스턴스로 공유**된다(인터닝). 그래서 `menus[i]` 와 `"종료"` 가 진짜로 같은 주소였다.

```java
String[] menus = new String[]{ "회원", ..., "종료" };
System.out.println(menus[5] == "종료");                  // true  — 같은 리터럴, 같은 인스턴스

String typed = keyboard.next();                          // 사용자가 "종료" 를 입력
System.out.println(typed == "종료");                     // false — 런타임에 만들어진 다른 인스턴스
System.out.println(typed.equals("종료"));                // true
```

### 공유된다는 것을 주소로 직접 확인하기

이 필기는 그다음 날 `System.identityHashCode()` 로 **어느 것이 같은 인스턴스인지**를 눈으로 확인했다. 리터럴로 만든 것과 `new` 로 만든 것을 섞어 놓고 주소를 찍는 실험이다.

```java
String s1 = new String("Hello");
String s2 = new String("Hello");
String s3 = "Hello";
String s4 = "Hello";
String[] s5 = new String[] {"Hello", "World"};

System.out.printf("%x\n", System.identityHashCode(s1));
System.out.printf("%x\n", System.identityHashCode(s2));
System.out.printf("%x\n", System.identityHashCode(s3));
System.out.printf("%x\n", System.identityHashCode(s4));
System.out.printf("%x\n", System.identityHashCode(s5[0]));
```

**`s3`·`s4`·`s5[0]` 이 같은 값을 찍고, `s1`·`s2` 는 서로도 다르고 그것들과도 다르다.** 같은 `"Hello"` 라고 썼는데 결과가 갈리는 기준은 **어떻게 만들었는가**다.

| 만드는 방법 | 어디에 생기나 | 같은 글자면 |
|---|---|---|
| 리터럴 `"Hello"` | 문자열 풀 (String const pool) | **공유된다** |
| `new String("Hello")` | 힙에 새로 | 부를 때마다 새 인스턴스 |

배열 안에 든 리터럴(`s5[0]`)까지 공유된다는 것이 Day11 실습의 `menus[i] == "종료"` 가 동작한 이유다 — 배열은 `new` 로 만들었지만 **그 안에 담긴 문자열은 리터럴**이라 풀의 것을 가리키고 있었다.

### 두 갈래가 고정된 것이 아니다 — `intern()`

Day12 시점에는 「리터럴은 풀, `new` 는 힙」으로 두 갈래가 나뉜 채 끝났다. 그 둘을 잇는 통로가 `intern()` 이다. **힙에 있는 인스턴스를 옮기는 것이 아니라, 같은 글자를 가진 풀의 인스턴스 주소를 받아 오는 것**이다.

```java
String s1 = new String("Hello");  // Heap 영역에 String 인스턴스를 생성한다.
String s2 = s1.intern();
String s3 = "Hello";

System.out.println(s1 == s2); //false   ← s1 은 여전히 힙의 것
System.out.println(s2 == s3); //true    ← s2 와 s3 은 풀의 같은 것
```

그리고 **`==` 가 여전히 `false` 라는 것이 이 메서드의 성질을 말해 준다.** `s1` 은 아무 영향을 받지 않았고, 풀 쪽 주소를 담은 변수가 하나 늘었을 뿐이다 → [[immutability]]

같은 회차가 `instanceof` 로 「둘이 결국 같은 종류」라는 것도 확인한다.

```java
System.out.println(s1 == s2);  //false — 다른 인스턴스
System.out.println(s1 instanceof String); //true
System.out.println(s2 instanceof String); //true
```

**「풀에 있는 것」과 「힙에 있는 것」은 타입이 다른 것이 아니다.** 어디에 놓였느냐만 다르고 둘 다 `String` 인스턴스다 → [[instanceof-operator]] · [[instance]]

### `String.equals()` 가 내용을 비교하는 이유는 문법이 아니다

`String` 이 특별해서가 아니라 **`String` 클래스가 `equals()` 를 재정의해 두었기** 때문이다. 그 사실을 확인하는 자리가 직접 클래스를 만들어 같은 일을 해 보는 회차다 — 필기가 「대표적으로 String.equals()가 Override를 활용한 경우이다」라고 못박았다.

```java
static class My {
    String name;
    int age;

    @Override
    public boolean equals(Object obj) {
      if (this == obj)          return true;
      if (obj == null)          return false;
      if (getClass() != obj.getClass()) return false;
      My other = (My) obj;
      return age == other.age && Objects.equals(name, other.name);
    }
  }
```

재정의 전에는 `obj1.equals(obj2)` 가 `false` 였고 후에는 `true` 다. 내용이 같은데도 `false` 였던 그 상태가 **`String` 이 재정의를 하지 않았다면 `"Hello".equals("Hello")` 도 그렇게 나올 상태**다 → [[object-equality]] · [[method-overriding]]

필드 비교에 `Objects.equals(name, other.name)` 를 쓴 것도 눈여겨볼 자리다. `name` 이 `null` 일 수 있으므로 `name.equals(...)` 를 그대로 쓰면 터진다 — 아래 「경계와 오해」의 `null` 항목이 여기서 표준 유틸로 해결된다.

## 왜 중요한가

**`==` 가 "동작하는" 경우가 있어서 위험하다.** 리터럴만 다루는 동안은 `==` 로도 맞는 결과가 나오므로, 잘못 쓴 것이 테스트를 통과한다. 그러다 값의 출처가 바뀌는 날 — 키보드 입력, 파일, DB, 네트워크 — 같은 코드가 조용히 `false` 가 된다. **동작했다는 것이 맞다는 뜻이 아닌** 대표적인 자리다.

그리고 이 구분은 문자열만의 이야기가 아니다. 레퍼런스 타입은 전부 그렇다 — `==` 는 항상 주소를 묻는다. 문자열이 유독 함정인 이유는 **리터럴로 쓸 수 있어서 기본 타입처럼 보이기** 때문이다.

## 경계와 오해

- **`==` 가 틀린 것이 아니라 다른 것을 묻는다** — 주소 비교로서는 정확히 동작한다. 묻고 싶었던 것이 내용이었을 뿐이고, 그래서 컴파일러가 막아 주지 않는다.
- **인터닝은 컴파일 시점 상수에만 적용된다** — 리터럴과 `final` 상수로 만든 문자열은 공유되지만, 런타임에 이어 붙이거나(`"종" + var`) `new String("종료")` 로 만든 것은 새 인스턴스다. 그래서 같은 글자인데 `==` 가 `false` 가 된다 → [[instance]]
- **`.equals()` 는 `null` 을 안전하게 다루지 않는다** — `menu.equals("종료")` 에서 `menu` 가 `null` 이면 `NullPointerException` 이다. Day11 시점에는 `"종료".equals(menu)` 로 **왼쪽에 리터럴을 두는 관용구**가 답이었고(그 실습은 배열을 리터럴로 채워 `null` 이 없었다), Day21 에서 **양쪽 다 `null` 일 수 있는 필드**를 비교하게 되면서 `Objects.equals(a, b)` 로 옮겨간다. 관용구는 한쪽이 확실히 `null` 이 아닐 때만 쓸 수 있으므로 **필드끼리 비교하는 자리에서는 쓸 수 없다** → [[object-reference]] · [[object-equality]]
- **기본 타입에 `.equals()` 는 없다** — `int` 는 `==` 가 맞다. 규칙이 "항상 equals" 가 아니라 "레퍼런스 타입이면 equals" 다.
- **`.equals()` 의 동작은 타입이 정한다** — 내용 비교는 `String` 이 그렇게 구현해 둔 것이다. 직접 만든 클래스는 재정의하지 않으면 `.equals()` 도 주소를 비교한다 → [[method-overriding]] · [[object-equality]]
- **「문자열은 `equals`, 기본 타입은 `==`」로 외우면 세 번째 경우를 놓친다** — Day12 시점에는 규칙이 「레퍼런스 타입이면 `equals`」로 닫힌 것처럼 보였다. 그런데 그 규칙이 성립하려면 **그 레퍼런스 타입이 `equals` 를 재정의해 두었어야** 한다. Day21 의 `My` 처럼 재정의하지 않은 클래스는 레퍼런스 타입인데도 `equals` 가 `==` 와 똑같이 답한다. 정확한 형태는 「내용 비교를 원하면 그 타입이 `equals` 를 재정의해 두었는지 확인한다」다 → [[object-class]]
- **`String.hashCode()` 도 같은 이유로 재정의된 것이다** — 같은 문자열이면 같은 해시값을 준다는 성질이 문자열의 본성이 아니라 `String` 클래스가 그렇게 구현해 둔 결과다. Day21 의 첫 `hashCode()` 재정의가 `String.format(...).hashCode()` 로 그 성질을 **빌려 쓴다** → [[hash-code]]
- **`==` 로 비교한 코드는 `switch` 에서는 통한다** — `switch (문자열)` 은 내부적으로 내용 비교로 동작한다. 같은 문자열 분기를 `if` 로 쓸 때만 이 함정이 있다 → [[switch-statement]]
- **`equalsIgnoreCase` 는 대소문자만 무시한다** — `str.equalsIgnoreCase("y")` 는 `Y` 와 `y` 를 같게 보지만 `yes`·` y `·`ㅛ` 는 전부 다르다. 사용자에게 한 글자를 받는 자리에서 이것을 「관대한 비교」로 읽으면 공백 하나에 「유지합니다」로 넘어가는 이유가 설명되지 않는다. 관용의 범위를 넓히려면 `trim()` 처럼 **비교 전에 값을 다듬는** 단계가 따로 필요하다.
- **내용 비교라고 해서 「같은 것」을 판정한 것은 아니다** — 이 필기는 팀원 중복을 `user.getName().equals(member.getName())` 으로 판정한다. 문자열 비교로는 정확한데 **동명이인이면 다른 사람을 같은 팀원으로 본다.** `equals` 가 답하는 것은 「이 두 문자열이 같은가」이고 「이 두 사람이 같은 사람인가」는 아니다 — 동일성 판정에 무엇을 쓸지는 도메인이 정할 일이고, 그것을 정하지 않으면 이름이 그 역할을 떠맡는다 → [[cohesion]]
- **문자열 풀(String const pool) ≠ `.class` 파일의 상수 풀** — 이름이 거의 같아서 한 가지로 읽히지만 층이 다르다. `.class` 의 상수 풀은 **파일 안에 리터럴의 글자를 담아 두는 표**이고, 문자열 풀은 **실행 중에 그 리터럴로 만든 인스턴스를 모아 두고 재사용하는 곳**이다. 이 필기의 「String const pool」은 뒤쪽, 즉 실행 시점의 것이다 → [[constant-pool]]
- **`new String("Hello")` 는 풀을 쓰지 않는다** — 리터럴을 넘겼는데도 새 인스턴스가 만들어진다. 그래서 같은 글자인 `s1` 과 `s2` 가 `==` 로 `false` 이고, 문자열을 `new` 로 만드는 것이 권장되지 않는 이유다. `new` 가 하는 일 자체는 그대로다 → [[instance]]
- **`identityHashCode` 는 주소가 아니다** — 인스턴스를 구별하는 값이라 "같은가 다른가"를 보는 데는 쓸 수 있지만 메모리 주소 자체는 아니다. 실행마다 값이 달라진다.
- **`intern()` 이 풀에 새로 만드는 경우는 이 예제에 없다** — 필기는 「String pool에 없으면 풀에 만들고 그 주소를 리턴한다」를 규칙으로 적고 `s1.intern()` 에 「String pool에 Hello를 생성」이라고 주석을 달았는데, `new String("Hello")` 의 **인수가 이미 리터럴**이라 그 클래스가 로드되는 시점에 `"Hello"` 는 풀에 들어가 있다. 그래서 `intern()` 은 찾기만 하고 만들지 않는다. **필기가 `intern()` 을 먼저 부른 Case 1 과 리터럴 대입을 먼저 한 Case 2 를 나눠 놓고 결과가 똑같이 나온 것이 그 증거**다 — 순서가 결과를 바꿨다면 둘 중 하나가 「만드는 쪽」이었을 것이다. 규칙 자체는 맞고, **런타임에 만들어진 문자열**(`sc.next()`·`"종" + var` 의 결과)에 부를 때 비로소 풀에 새로 들어간다 → [[constant-pool]] · [[literal]]
- **`==` 를 맞추기 위해 `intern()` 을 쓰는 것은 순서가 뒤바뀐 것이다** — 내용을 비교하고 싶으면 `equals` 를 쓰면 된다. `intern()` 은 같은 글자를 여러 벌 들고 있을 때 **메모리를 아끼려고** 쓰는 것이고, 그 부수 효과로 `==` 가 통하게 되는 것이다. 「`==` 로 비교하려면 인터닝하면 된다」로 배우면 풀에 문자열이 무한히 쌓이는 코드를 쓰게 된다 → [[caching]] · [[garbage-collection]]
- **`String` 을 만드는 방법이 리터럴과 `new String(문자열)` 둘만 있는 것은 아니다** — `new String(char[])` 와 `new String(byte[], "euc-kr")` 처럼 배열에서 만드는 생성자가 있고, 이쪽은 **애초에 리터럴이 없으므로 무조건 힙**이다. 「같은 글자면 공유될 수도 있다」는 이야기가 아예 성립하지 않는 만드는 법이 따로 있다 → [[character-encoding]] · [[array]]
- **`String` 은 기본 타입이 아니다** — 이 필기가 명시적으로 정리한 것이다. 기본 타입은 여덟 개(`byte`·`short`·`int`·`long`·`float`·`double`·`char`·`boolean`)뿐이고, `String` 은 배열과 마찬가지로 레퍼런스다. 리터럴로 쓸 수 있어 기본 타입처럼 보이는 것이 이 함정의 뿌리다 → [[data-type]] · [[object-reference]]

## 함께 보는 개념

- [[object-reference]] — `==` 가 실제로 비교하는 것
- [[constant-pool]] — 리터럴이 한 번만 저장되는 곳
- [[instance]] — 같은 글자라도 다른 인스턴스일 수 있다는 것
- [[literal]] — 문자열을 코드에 적는 표기
- [[if-statement]] — 이 비교가 쓰이는 자리
- [[array]] — 배열 원소를 비교할 때 갈리는 자리
- [[data-type]] — `String` 이 기본 타입이 아닌 이유
- [[cohesion]] — 동일성 판정 규칙이 어느 클래스에 사는가
- [[method-overriding]] — 직접 만든 클래스의 `equals` 를 정하는 자리
- [[object-equality]] — 「같다」의 두 뜻을 일반화한 자리
- [[hash-code]] — `String` 이 함께 재정의해 둔 짝
- [[object-class]] — 재정의하지 않았을 때의 기본 동작이 사는 곳
- [[immutability]] — 공유가 안전한 이유
- [[instanceof-operator]] — 풀과 힙의 것이 같은 타입임을 확인하는 수단
- [[character-encoding]] — 배열에서 문자열을 만드는 쪽
- [[wrapper-class]] — 같은 「작은 값은 재사용」 함정이 반복되는 자리

## 출처

- [[2024-06-11-Day11]] — 실습에서 메뉴를 `menus[i] == "종료"` 로 비교했다가 `menu.equals("종료")` 로 바꾸는 것을 배웠다. 리터럴로 채운 배열이어서 `==` 도 동작했다는 사실은 필기에 적히지 않았다
- [[2024-06-11-Day12]] — `String` 이 기본 타입이 아니라 레퍼런스라는 것, 리터럴은 문자열 풀에 생기고 `new String()` 은 힙에 새로 생긴다는 것을 `System.identityHashCode()` 로 직접 확인했다. Day11 의 `==` 가 동작한 이유가 여기서 설명된다
- [[2024-06-18-Day17]] — 팀원 중복 검사를 `user.getName().equals(member.getName())` 으로, 삭제 확인을 `str.equalsIgnoreCase("y")` 로 쓰면서 `equals` 계열이 실제 판정에 들어가는 것을 실습으로 배웠다. 이름으로 사람의 동일성을 판정하게 된 것도 이 자리다
- [[2024-06-24-Day21]] — 직접 만든 클래스의 `equals` 를 재정의해 보며 **`String.equals()` 가 내용을 비교하는 것도 재정의의 결과**라는 것을 확인했다(「대표적으로 String.equals()가 Override를 활용한 경우이다」). 필드 비교에 `Objects.equals(name, other.name)` 를 쓰면서 Day11 의 `"종료".equals(menu)` 관용구가 표준 유틸로 옮겨가고, `String.format(...).hashCode()` 로 문자열의 해시 성질을 빌려 쓰는 것도 이 자리다
- [[2024-06-25-Day22]] — Day12 에서 실험으로 확인한 「리터럴은 풀, `new` 는 힙」이 여기서 문장으로 정리되고(「new String()으로 생성한 객체는 Heap영역에 보관된다」·「""으로 할당된 문자열은 String pool에 생성된다」), `intern()` 으로 힙의 것에서 풀의 주소를 얻는 통로가 더해진다. `instanceof String` 을 양쪽에 불러 「근본적으로 두 방식 모두 String 객체의 인스턴스이다」를 확인한 것도 이 자리다. `intern()` 이 풀에 「생성」한다고 적었지만 이 예제에서는 인수가 리터럴이라 이미 풀에 있고 찾기만 한다
