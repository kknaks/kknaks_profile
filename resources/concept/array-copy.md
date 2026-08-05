---
type: concept
id: array-copy
title: 배열 복사 (Arrays.copyOf · copyOfRange)
aliases:
  - 배열 복사
  - array copy
  - copyOf
  - copyOfRange
  - Arrays.copyOf
  - 범위 복사
  - 반개구간
up:
  - 2024-06-25-Day22
  - 2024-07-22-Day40
tags:
  - java
  - 배열
  - 자료구조
  - 문법
---

# 배열 복사 (Arrays.copyOf · copyOfRange)

배열의 전체나 일부를 **새 배열에 옮겨 담아 돌려주는** 표준 메서드. 배열은 크기를 바꿀 수 없으므로 「늘리기」·「잘라 내기」·「사본 만들기」가 전부 이 한 가지 동작으로 표현된다 → [[array]]

## 정의

```java
Arrays.copyOf(원본, 새길이)            // 앞에서부터 새길이만큼
Arrays.copyOfRange(원본, start, end)   // start 부터 end 앞까지
```

**범위는 반개구간 `[start, end)` 다** — `start` 는 포함하고 `end` 는 포함하지 않는다. 그래서 사본의 길이가 `end - start` 로 딱 나온다.

`copyOf` 는 길이를 마음대로 줄 수 있다.

| 새 길이 | 결과 |
|---|---|
| 원본보다 짧다 | 뒤가 잘린다 |
| 원본과 같다 | 그대로 복사 |
| 원본보다 길다 | 남는 칸이 **기본값**으로 채워진다 → [[default-initialization]] |

## 사용 예시

필기의 예제는 문자열 다섯 개가 든 배열에서 두 칸을 떼어 낸다.

```java
String[] arr = {"101", "제목", "내용", "4", "2021-2-2"};

// 배열에서 특정 범위의 항목을 복사하기
String[] arr2 = Arrays.copyOfRange(arr, 2, 4);
for (String s : arr2) {
  System.out.println(s);
```

**나오는 것은 인덱스 2·3, 즉 `내용` 과 `4` 다.** 「2번부터 4번까지」로 읽으면 세 개가 나올 것 같고, 필기가 적은 `(start,end]` 로 읽으면 `4` 와 `2021-2-2` 가 나올 것 같은데 둘 다 아니다 → 아래 「경계와 오해」

배열을 **한 칸 늘리는** 쪽은 같은 회차의 가변 배열 실습에 나온다.

```java
list = Arrays.copyOf(list, newSize);       // 더 큰 배열을 만들고 옮겨 담는 일을 한 줄로
```

**닷새 전 회차에서 손으로 쓴 것과 같은 일이다.**

```java
User[] arr = new User[userLength];         // 새 배열을 만들고
for (int i = 0; i < arr.length; i++) {
  arr[i] = users[i];                       // 하나씩 옮겨 담아
}
return arr;
```

`new` + `for` 세 줄이 메서드 호출 한 줄이 된 것이고, 그것이 이 메서드가 하는 일 전부다 → [[defensive-copy]] · [[dynamic-array]]

### 한 달 뒤 — 「크기를 바꾸는 수단」이 아니라 「타입을 복제하는 수단」으로 쓰인다

Day40 은 `new T[10]` 이 막혀 있다는 사실을 만나고 이 메서드를 우회로로 고른다.

```java
  // 예2) 견본 배열을 받아서 복제하는 방법을 사용한다.
  static <T> T[] create2(T[] arr) {
    return Arrays.copyOf(arr, 10);
  }
```

```java
    String[] arr1 = create2(new String[0]);
    System.out.println(arr1.length);          // 10
```

**`new String[0]` 은 값이 아니라 타입을 넘기는 수단이다** — 원소가 하나도 없는 배열을 넘기고 길이 10 의 `String[]` 을 받는다. 성립하는 이유는 이 메서드가 **원본의 실행 시점 원소 타입으로 새 배열을 만들기 때문**이다. 만약 `Object[]` 를 돌려줬다면 `String[]` 변수에 대입하는 순간 터진다 → [[generics]] · [[type-erasure]]

그리고 같은 회차가 「줄이는 쪽」도 실험으로 확인한다.

```java
    String[] temp = new String[100];
    String[] arr2 = create2(temp);
    System.out.println(arr2.length);          // 10
    System.out.println(temp == arr2);         // false
```

**`==` 가 `false` 인 것이 이 메서드의 정체 확인이다** — 원본을 자르는 것이 아니라 **새 배열을 만들어 돌려준다.** Day22 의 표에 있던 「원본보다 짧다 → 뒤가 잘린다」가 여기서 실제로 확인된다 → [[object-reference]]

## 왜 중요한가

**배열의 고정 크기를 넘어가는 유일한 방법이 이것이다.** 「배열에 요소를 추가한다」는 동작은 존재하지 않고, 실제로 일어나는 일은 항상 **더 큰 배열을 만들어 옮기는 것**이다. 그래서 이 메서드가 가변 배열의 심장이 되고, 그 위에 `ArrayList` 가 서 있다 → [[dynamic-array]]

**그리고 「복사한다」가 O(n) 이라는 것이 코드에서 사라진다.** 손으로 쓴 `for` 루프는 비용이 눈에 보이지만 `Arrays.copyOf(list, newSize)` 는 한 줄이라 안 보인다. 루프가 메서드 안으로 들어간 것이고 **없어진 것이 아니다.**

## 경계와 오해

- **필기의 `(start,end]` 는 뒤집혀 있다** — 실제는 `[start, end)` 로 **앞을 포함하고 뒤를 제외**한다. 필기대로면 `copyOfRange(arr, 2, 4)` 가 `4`·`2021-2-2` 를 줄 텐데 실제로는 `내용`·`4` 가 나온다. Java 의 범위 메서드는 `substring`·`replace(start,end,..)` 까지 전부 이 규칙이라 하나를 뒤집어 외우면 전부 한 칸씩 어긋난다. **길이가 `end - start` 로 나오는 것이 반개구간의 값**이다 → [[one-based-numbering]] · [[string-builder]]
- **「String복사하기」라는 제목과 하는 일이 다르다** — 복사되는 것은 **문자열이 든 배열**이고 문자열 하나가 아니다. `String` 은 불변이라 복사할 이유 자체가 없다 → [[immutability]]
- **새로 만들어지는 것은 배열뿐이다 (얕은 복사)** — 칸에 든 것은 **같은 인스턴스의 주소**다. `String[]` 에서는 원소가 불변이라 차이가 안 드러나지만, `User[]` 였다면 사본의 원소를 고치는 것이 원본의 회원을 고친다. 닷새 전 회차의 「방어적 복사 ≠ 깊은 복사」가 표준 메서드로 옮겨 와도 그대로 남는다 → [[defensive-copy]] · [[object-reference]]
- **`b = a` 는 복사가 아니다** — 배열 변수는 주소를 담을 뿐이므로 대입은 같은 배열을 가리키는 이름을 하나 더 만든다. 복사를 원하면 이 메서드를 불러야 하고, **문법으로는 둘이 구별되지 않는다** → [[array]] · [[call-by-value]]
- **원본은 건드리지 않는다** — `copyOf` 는 원본을 그대로 두고 새 배열을 돌려준다. 그래서 `list = Arrays.copyOf(list, newSize)` 처럼 **결과를 다시 받아야** 의미가 있다. 받지 않으면 새 배열이 생겨서 바로 버려진다 → [[immutability]]
- **`length` 로 잘못 부르는 것을 컴파일러가 막지 못한다** — `copyOfRange(arr, 2, arr.length)` 는 되지만 `copyOfRange(arr, 2, arr.length + 1)` 은 실행 시점에 `ArrayIndexOutOfBoundsException` 이다. 반면 `copyOf(arr, arr.length + 1)` 은 정상이고 뒤가 `null` 이 된다 — **같은 「범위를 넘김」이 한쪽은 예외, 한쪽은 기본값**이다 → [[default-initialization]] · [[exception-handling]]

- **`copyOf` 는 `Object[]` 를 돌려주지 않는다 — 그래서 제네릭 배열의 우회로가 된다** — 안에서 원본의 `getClass().getComponentType()` 을 보고 그 타입의 배열을 만든다. `String[]` 을 넘기면 `String[]` 이 나오므로 `T[]` 로 받아도 실제 타입이 맞다. **직접 `(T[]) new Object[10]` 을 만들어 돌려주면 컴파일은 되고 대입하는 자리에서 `ClassCastException`** 이 나는데, 이것이 제네릭 배열의 고전적 함정이고 이 메서드를 쓰면 걸리지 않는다 → [[type-erasure]] · [[class-metadata]]
- **견본 배열의 내용은 쓰이지 않는다** — `create2(new String[0])` 처럼 빈 배열을 넘기는 것이 관용구다. **인수가 값이 아니라 타입 정보로 쓰이는 자리**라서, 「왜 빈 배열을 만들어 넘기나」를 값의 관점으로 읽으면 이해되지 않는다 → [[generics]]

## 함께 보는 개념

- [[array]] — 크기를 바꿀 수 없는 대상
- [[generics]] — 이 메서드를 배열 생성 우회로로 쓰는 자리
- [[type-erasure]] — `new T[10]` 이 막혀 있는 이유
- [[class-metadata]] — 원소 타입을 실행 시점에 알아내는 통로
- [[dynamic-array]] — 이 메서드로 크기 제약을 넘는 구조
- [[defensive-copy]] — 손으로 쓴 같은 일
- [[object-reference]] — 칸에 든 것이 무엇인가
- [[immutability]] — 사본이 필요 없어지는 조건
- [[default-initialization]] — 늘린 칸을 채우는 값
- [[array-element-removal]] — 배열을 줄이는 다른 방법
- [[one-based-numbering]] — 범위를 세는 기준이 어긋나는 자리
- [[call-by-value]] — 대입과 복사가 갈리는 이유

## 출처

- [[2024-06-25-Day22]] — 「String을 복사하는 메서드는 Arrays.copyOfRange(args[], start,end)」로 배열의 일부를 떼어 내는 것을 배웠고, 같은 회차 3.2 의 가변 배열 실습에서 `Arrays.copyOf(list, newSize)` 로 배열을 늘리는 쪽까지 나온다. 범위를 「(start,end\]」로 적은 것은 이 필기의 오류다
- [[2024-07-22-Day40]] — 제네릭으로 배열을 만들 수 없다는 것을 만나고 「견본 배열을 받아서 복제하는 방법」으로 이 메서드를 우회로로 쓴다(`static <T> T[] create2(T[] arr) { return Arrays.copyOf(arr, 10); }`). `create2(new String[0])` 처럼 **빈 배열을 타입 정보로 넘기는** 관용구가 여기서 나오고, 원본보다 큰 배열(`new String[100]`)을 넘겨 길이 10 이 나오고 `temp == arr2` 가 `false` 인 것까지 확인한다 — 「copyOf() 그래도 새 크기에 맞춰 새 배열을 생성한다」가 그 주석이다. 이 메서드가 원본의 실행 시점 원소 타입을 그대로 쓴다는 것(그래서 이 우회로가 성립한다는 것)은 다루지 않았다
