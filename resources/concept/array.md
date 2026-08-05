---
type: concept
id: array
title: 배열 (Array)
aliases:
  - 배열
  - array
  - 배열 선언
  - length
up:
  - 2024-06-11-Day11
  - 2024-06-18-Day17
  - 2024-06-24-Day21
  - 2024-06-25-Day22
tags:
  - java
  - 자료구조
  - 메모리
  - 문법
---

# 배열 (Array)

같은 타입의 메모리를 **연속으로 개수만큼** 확보하고, 이름 하나와 인덱스로 다루는 것. 변수 여러 개를 하나로 묶는 첫 번째 도구다.

## 정의

선언 문법은 네 가지 모양으로 나온다.

```java
// - 문법
// 메모리종류[] 메모리이름 = new 메모리종류[개수];
// 데이터타입[] 변수명 = new 데이터타입[개수];
// 데이터타입[] 변수명 = {};
    int[] arr1 = new int[5]; // OK!
    int arr2[] = new int[5]; // OK! C-style.
    int[] arr3 = {1,2,3,4,5};
    int[] arr4 = new int[]{1,2,3,4,5}
```

선언문은 **두 부분**으로 나뉜다.

```java
// arr1
//   - 배열 메모리의 주소를 담는 변수이다.
//   - 이렇게 메모리의 주소를 보관하는 변수를 '레퍼런스'라 부른다.
//
// new int[5]
//   - new 명령은 사용할 메모리를 확보하는 명령이다.
//   - 즉 연속된 5 개의 int 타입 메모리를 준비하라는 명령이다.
//   - 사용할 메모리를 확보한 후 그 메모리의 찾아 갈 수 있도록 시작 주소를 리턴한다.
//   - 이렇게 값을 저장하기 위해 확보된 메모리를 "인스턴스"라 부른다.
```

즉 **변수는 [[object-reference]], `new` 가 만든 것은 [[instance]]** 다. 확보된 원소는 만들어지는 순간 기본값으로 채워진다 → [[default-initialization]]

인덱스는 **0부터** 시작하고, 개수는 `배열.length` 로 읽는다.

## 사용 예시

이 필기의 실습이 배열을 도입한 이유가 그대로 남아 있다. 메뉴가 변수 여섯 개였다.

```java
String menu1 = "1. 회원";
String menu2 = "2. 팀";
String menu3 = "3. 프로젝트";
String menu4 = "4. 게시판";
String menu5 = "5. 도움말";
String menu6 = "6. 종료";
```

배열 하나로 묶었다. 번호를 문자열에서 떼어 낸 것에 주의한다 — 번호는 이제 **인덱스에서 나온다.**

```java
String[] menus = new String[]{
                "회원",
                "팀",
                "프로젝트",
                "게시판",
                "도움말",
                "종료",
        };
```

그러면 유효 범위 검사가 `length` 로 표현된다.

```java
if (menuNo >= 1 && menuNo <= menus.length) {
    System.out.println(menus[menuNo - 1]);
} else {
    System.out.println("메뉴 번호가 옳지 않습니다.");
}
```

### 내용이 늘고 줄면 배열 하나로는 부족하다

메뉴처럼 개수가 고정된 것과 달리, 회원 목록은 등록과 삭제로 개수가 변한다. 그러면 **배열과 「지금 몇 개 들었나」를 따로 들고 다녀야** 한다.

```java
private static final int MAX_SIZE = 10;
private static final User[] users = new User[MAX_SIZE];
private static int userLength = 0;
```

세 줄이 한 세트다.

| 이름 | 뜻 | 바뀌나 |
|---|---|---|
| `MAX_SIZE` | 담을 수 있는 최대 개수 | 아니다 |
| `users.length` | 확보한 칸 수 (= `MAX_SIZE`) | 아니다 |
| `userLength` | **실제로 든 개수** | 등록·삭제마다 |

**`length` 가 「몇 개 들었나」를 답하지 못하는 것이 여기서 처음 문제가 된다.** 메뉴 실습에서는 배열을 꽉 채워 만들었으니 둘이 같았고, 그래서 `menus.length` 로 범위를 검사할 수 있었다. 늘고 줄어드는 배열에서는 순회도 검사도 `userLength` 를 봐야 하고, `length` 를 보면 아직 `null` 인 칸까지 센다 → [[default-initialization]]

```java
for (int i = 0; i < userLength; i++) {     // users.length 가 아니다
  User user = users[i];
  ...
}
```

추가와 삭제도 그 개수 변수를 같이 손봐야 한다.

```java
users[userLength++] = user;               // 등록 — 넣고 개수를 늘린다
users[--userLength] = null;               // 삭제의 마지막 단계 → [[array-element-removal]]
```

### 장점과 단점이 같은 성질에서 나온다

한 주 뒤 회차가 배열을 정리한 표를 남겼다. **읽는 방법이 있다 — 왼쪽과 오른쪽의 같은 번호가 대개 같은 성질의 양면이다.**

| | 장점 | 단점 |
|---|---|---|
| 1 | **고정된 크기** — 미리 정의하면 메모리 관리가 용이 | **고정된 크기** — 선언 후 크기를 바꿀 수 없어 가변적인 데이터에 부적합 |
| 2 | **빠른 접근** — 인덱스로 O(1) | **메모리 낭비** — 크게 잡으면 남고 작게 잡으면 넘친다 |
| 3 | **연속 할당** — 캐시 효율이 높다 | **삽입·삭제의 비효율** — 다른 요소를 이동해야 해서 O(n) |
| 4 | **간단한 구조** | **타입 제한** — 단일 타입만 담는다 |

**1번은 필기가 같은 말을 양쪽에 적어 둔 것**이고 그것이 오히려 정확하다 — 크기를 못 바꾸는 덕분에 관리가 쉽고, 쉬운 대가로 못 바꾼다. 2번과 3번도 한 뿌리다. **연속으로 잡았으니 시작 주소 + 인덱스 × 크기로 위치를 바로 계산할 수 있고**(장점 2·3), 연속이니 중간에 자리를 만들려면 뒤를 다 밀어야 한다(단점 3) → [[array-element-removal]] · [[data-type]]

그래서 개선 방향이 둘로 갈린다. **고정 크기만 없애려면 배열을 유지한 채 옮겨 담고**, 이동 비용까지 없애려면 **연속 메모리를 포기**해야 한다. 같은 회차의 실습 두 개가 정확히 그 둘이다 → [[dynamic-array]] · [[linked-list]]

「타입 제한」(단점 4)을 피하는 방법도 같은 실습에 나온다 — `Object[]` 로 선언하면 무엇이든 담을 수 있다. 대가는 꺼낼 때의 다운캐스팅이다 → [[object-class]] · [[type-casting]]

## 왜 중요한가

**변수를 개수만큼 늘리는 코드는 개수가 바뀔 때마다 전부 고쳐야 한다.** 이 필기에서 배열을 도입하자 `println` 여섯 줄이 `for` 하나로, `case` 여섯 개가 인덱스 접근 한 줄로 줄었다 → [[for-loop]] · [[switch-statement]]

더 큰 것은 `menus.length` 다. **개수가 코드에 상수로 박히지 않으면 메뉴를 추가해도 고칠 곳이 배열 선언 한 군데다.** 반대로 `menuNo <= 6` 이라고 썼다면 메뉴를 늘릴 때 검증 코드까지 찾아 고쳐야 하고, 하나를 빠뜨리면 조용히 어긋난다.

그리고 배열은 [[instance]]·[[object-reference]]·[[garbage-collection]] 을 처음 만나는 자리다. 클래스를 배우기 전에 `new` 가 하는 일을 배열로 먼저 겪게 된다.

## 경계와 오해

- **`{1,2,3}` 축약은 선언과 동시에만 쓴다** — 이 필기에 `arr3` 과 `arr4` 두 형태가 나란히 있는데, 둘 다 필요한 이유가 여기다. 이미 선언된 변수에는 `arr = {1,2,3};` 을 쓸 수 없고 `arr = new int[]{1,2,3};` 이어야 한다. 메서드 인자로 넘길 때도 `new int[]{...}` 형태만 통한다.
- **배열은 크기가 고정이다** — `new` 할 때 정해지고 늘릴 수 없다. "요소를 추가"하려면 더 큰 배열을 새로 만들어 옮겨야 한다. 그 불편을 감춘 것이 `ArrayList` 이고, 한 주 뒤 회차에서 그것을 직접 만들어 본다 → [[dynamic-array]] · [[array-copy]]
- **옮겨 담는 것을 손으로 쓸 필요는 없다** — Day17·Day19 까지는 `new` + `for` 로 복사 루프를 직접 썼는데, 표준 라이브러리에 `Arrays.copyOf`·`Arrays.copyOfRange` 가 있다. **루프가 없어진 것이 아니라 메서드 안으로 들어간 것**이라 O(n) 비용은 그대로다 → [[array-copy]] · [[defensive-copy]]
- **`length` ≠ 든 개수** — `length` 는 **확보한 칸 수**다. 배열을 꽉 채워 쓰는 동안은 둘이 같아서 구분이 필요 없지만, 늘고 줄어드는 목록에서는 개수를 담는 변수를 따로 둬야 한다. 이 짝을 지키지 않으면 `null` 인 칸이 목록에 나오거나 삭제한 것이 계속 세어진다 → [[array-element-removal]]
- **최대 크기를 정한 것과 그것을 검사하는 것은 다르다** — `MAX_SIZE` 를 선언해도 `users[userLength++] = user` 는 그 값을 보지 않는다. 11번째 등록에서 `ArrayIndexOutOfBoundsException` 이 나고, **상수를 뽑아 둔 것이 검사를 대신해 주지 않는다** → [[crud]]
- **`length` 는 필드고 `length()` 는 메서드다** — 배열은 `menus.length`, 문자열은 `menu.length()`. 한 코드에 둘이 같이 나오면 헷갈린다.
- **`int[] arr` 과 `int arr[]` 은 같다** — C 스타일도 허용되지만, 타입이 이름 쪽으로 흩어져 읽히기 어렵다. `int[] a, b;` 는 둘 다 배열인데 `int a[], b;` 는 `b` 만 `int` 다.
- **배열 변수는 배열이 아니다** — 주소를 담고 있을 뿐이다. 그래서 `b = a` 는 배열을 복사하지 않고, `b[0]` 을 바꾸면 `a[0]` 도 바뀐다 → [[object-reference]]
- **인덱스 검사는 실행 시점에 한다** — 범위를 넘으면 컴파일이 아니라 실행 중에 `ArrayIndexOutOfBoundsException` 이 난다. `menuNo - 1` 처럼 계산해 넣는 자리가 특히 위험하다.
- **배열 원소끼리 `==` 로 비교할 때 타입을 본다** — `int[]` 는 값이 비교되지만 `String[]` 은 주소가 비교된다. 이 필기가 `menus[i] == "종료"` 로 시작해 `.equals()` 로 고친 이유다 → [[string-comparison]]
- **배열도 클래스를 갖는다 — `int[]` 조차 그렇다** — `new int[10].getClass().getName()` 이 `[I` 를 돌려준다. 즉 배열은 [[object-class]] 의 서브클래스이고 `toString`·`equals`·`hashCode` 도 갖고 있다. **원소가 기본 타입인 것과 배열 자체가 무엇인가는 다른 층**이라서, 「`int` 는 객체가 아니니 `int[]` 도 아니겠지」가 여기서 깨진다 → [[data-type]] · [[class-metadata]]
- **배열의 타입 이름은 `String[]` 이 아니다** — `getName()` 이 `[Ljava.lang.String;` 를 돌려주고 기본 타입 배열은 `[B`·`[I`·`[Z` 처럼 한 글자로 줄어든다. JVM 내부 표기라 사람이 쓰는 표기와 다른 것이고, 이름을 찍어 보다 처음 만나면 깨진 문자열로 읽힌다 → [[class-file-format]]
- **`length` 는 원소 타입을 알려 주지 않는다** — 배열이 스스로 답하는 것은 칸 수뿐이고, 「무엇이 들어가는 배열인가」는 `getClass().getComponentType()` 으로 따로 물어야 한다. `Object[]` 로 받은 배열에서 원래 타입을 되찾을 때 필요한 것이 그것이다 → [[class-metadata]] · [[type-casting]]
- **`Object[]` 는 아무 배열이나 받는 타입이 아니다** — `Object` 가 모든 참조 타입의 조상이므로 `Object[]` 변수에 `String[]` 을 담을 수는 있지만, `int[]` 는 `Object` 이면서 `Object[]` 는 아니다(원소가 `Object` 가 아니다). `HashSet.toArray()` 가 `Object[]` 를 돌려주고 꺼낼 때마다 다운캐스팅이 필요한 것도 이 층의 이야기다 → [[hash-based-collection]]

## 함께 보는 개념

- [[multidimensional-array]] — 원소가 다시 배열인 경우
- [[object-reference]] — 배열 변수가 담는 것
- [[instance]] — `new` 가 만드는 것
- [[default-initialization]] — 확보된 원소가 채워지는 값
- [[garbage-collection]] — 가리키는 것이 없어진 배열의 운명
- [[for-loop]] — 배열을 도는 짝
- [[command-line-arguments]] — `String[] args` 로 처음 만나는 배열
- [[data-type]] — 원소 하나의 크기와 해석 방법
- [[call-by-value]] — 배열을 메서드에 넘겼을 때 내용이 바뀌는 이유
- [[array-element-removal]] — 중간 요소를 지울 때 해야 하는 일
- [[one-based-numbering]] — 인덱스와 화면 번호를 잇는 자리
- [[crud]] — 배열이 저장소로 쓰이는 구조
- [[object-class]] — 배열도 상속하고 있는 조상
- [[class-metadata]] — 배열의 타입과 원소 타입을 묻는 도구
- [[hash-based-collection]] — 배열을 감춘 저장소
- [[array-copy]] — 늘리고 잘라 내는 표준 도구
- [[dynamic-array]] — 고정 크기를 감춘 구조
- [[linked-list]] — 연속 메모리를 포기한 구조

## 출처

- [[2024-06-11-Day11]] — 배열의 네 가지 선언 형태와 `new` 가 연속 메모리를 확보해 시작 주소를 리턴한다는 것, 그리고 실습에서 메뉴 변수 여섯 개를 배열 하나로 묶어 `length` 로 범위를 검사하는 것을 배웠다
- [[2024-06-18-Day17]] — 등록·삭제로 개수가 변하는 목록을 담으면서 `MAX_SIZE` 로 고정한 배열과 실제 개수를 담는 변수(`userLength`·`memberSize`)를 짝으로 들고 다니는 것을 실습으로 배웠다. 순회와 범위 검사가 `length` 가 아니라 그 개수 변수를 보게 되는 것이 이 회차의 차이다
- [[2024-06-24-Day21]] — 배열에 `getClass()` 를 불러 `[Ljava.lang.String;`·`[B`·`[I` 같은 JVM 표기의 타입 이름을 얻고, 원소 타입은 `getComponentType()` 으로 따로 물어야 한다는 것을 배웠다. `int[]` 도 `getClass()` 에 답하므로 **기본 타입 배열조차 `Object` 의 서브클래스**라는 것이 이 자리에서 드러난다
- [[2024-06-25-Day22]] — 배열의 장단점을 네 항목씩 표로 정리했다(고정 크기 · O(1) 접근 · 연속 메모리 · 단일 타입). 「고정된 크기」가 장점과 단점 양쪽에 적혀 있는 것이 그 표의 핵심이고, 이어지는 실습이 그 단점을 각각 다르게 푼다 — 옮겨 담아 크기를 늘리는 가변 배열과, 연속 메모리를 버린 연결 리스트다. `Arrays.copyOfRange`·`Arrays.copyOf` 로 복사를 표준 메서드에 맡기게 되는 것도 이 회차다
