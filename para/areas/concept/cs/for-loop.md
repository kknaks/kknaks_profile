---
type: concept
id: for-loop
title: for 문
aliases:
  - for
  - for 문
  - for each
  - for-each
  - 향상된 for문
  - enhanced for
up:
  - 2024-06-11-Day11
  - 2024-06-20-Day19
  - 2024-07-10-Day32
tags:
  - java
  - 제어문
  - 문법
---

# for 문

반복에 필요한 세 조각 — **초기화 · 조건 · 증감** — 을 한 줄에 모아 쓰는 반복문. 횟수가 정해진 반복에 맞는다.

## 정의

```java
// for 문의 전형적인 예
for (int i = 1; i <= 5; i++)
  System.out.println(i);
// 실행 순서
// 1) 변수초기화  => int i = 1
// 2) 조건 => i <= 5
// 3) 문장 => System.out.print(i + " ")
// 4) 변수증가문 => i++
// 조건이 참인 동안 2 ~ 4를 반복한다.
```

초기화는 **한 번만** 실행되고, 이후 조건 → 문장 → 증감이 돈다. 증감문이 문장 **뒤**에 실행된다는 것이 [[break-continue]] 의 동작을 정한다.

`for` 안에서 선언한 변수는 그 `for` 안에서만 산다.

```java
// for 문에서 선언한 변수는 그 for 문 안에서만 사용할 수 있다.
//    System.out.println(i); // 컴파일 오류!
```

### 향상된 for 문 (for-each)

배열이나 컬렉션의 요소를 **순서대로 하나씩** 꺼내는 축약 형태다. 인덱스가 없다.

```java
for (String menu : menus) {
    // menu 에 요소가 하나씩 들어온다
}
```

**20일 뒤 회차가 「배열이나 컬렉션」의 정확한 조건을 적는다** — 「진보된 for문에는 배열 또는 Iterable이 가능하다」.

```java
for (변수타입 변수명 : 배열 or Iterable 구현체) {}
```

둘뿐이다. 아무 컬렉션이나 되는 것이 아니라 **`java.lang.Iterable` 을 구현했다고 선언한 것**이어야 한다 → [[iterator-pattern]] · [[interface]]

## 사용 예시

메뉴 배열을 번호와 함께 출력한다. 번호가 필요하므로 인덱스 `for` 를 쓰고 `i + 1` 로 만든다.

```java
for (int i = 0; i < menus.length; i++) {
    if (menus[i] == "종료") {
        System.out.printf("%s%d. %s%s\n", (boldAnsi + redAnsi), (i + 1), menus[i], resetAnsi);
    } else {
        System.out.printf("%d. %s\n", (i + 1), menus[i]);
    }
}
```

같은 출력을 for-each 로 바꾸면 코드가 짧아지는 대신 **번호가 사라진다.**

```java
for (String menu : menus){
    if (menu.equals("종료")) {
        System.out.printf("%s%s%s\n",(boldAnsi+redAnsi),menu,resetAnsi);
    }else {
        System.out.printf("%s\n",menu);
    }
}
```

이 필기의 최종 코드가 정확히 그렇게 됐다 — for-each 로 바꾸면서 `1. 회원` 이 `회원` 이 됐다. **인덱스를 쓰지 않겠다는 선택에 번호 출력까지 딸려 나간 것**이고, 이것이 두 형태를 고르는 기준이다.

## 왜 중요한가

**루프 변수의 생애가 한 줄에 다 보인다.** 어디서 시작해 언제까지 얼마씩 가는지가 헤더에 모여 있어서, 같은 반복을 `while` 로 쓸 때처럼 초기화·증감이 위아래로 흩어지지 않는다. 증감문을 빠뜨려 생기는 무한 루프도 문법이 막아 준다 → [[while-loop]]

그리고 **`length` 를 조건에 쓰면 반복이 데이터 개수와 무관해진다.** 이 필기에서 `println` 여섯 줄과 `case` 여섯 개가 `for` 하나로 줄어든 것이 그 결과다 — 메뉴를 추가해도 고칠 코드가 없다 → [[array]]

## 경계와 오해

- **for-each 는 인덱스를 주지 않는다** — 몇 번째인지 알아야 하는 일(번호 출력, 앞뒤 요소 비교, 특정 위치만 다루기)은 인덱스 `for` 가 맡는다. 위 예시에서 번호가 사라진 것이 그 대가다.
- **「번호를 찍어야 하니 인덱스 `for`」는 조건부다** — Day19 의 목록 출력은 번호를 찍으면서 for-each 를 쓴다. 번호가 데이터의 필드로 들어가 있어서 인덱스로 만들 필요가 없어졌기 때문이다. 대가 없이 바뀐 것이 아니라 **번호를 어디에 두는지를 먼저 바꾼 결과**다 → [[surrogate-key]]
- **for-each 는 「몇 개까지 돌지」를 대상에게 맡긴다** — 인덱스 `for` 는 `i < userLength` 처럼 개수 변수를 조건에 써야 하는데, for-each 는 받은 배열의 길이만큼 돈다. 그래서 **개수 변수를 아는 코드가 줄어들고**, 대신 받은 배열의 길이가 유효 개수와 같아야 한다는 전제가 생긴다 → [[defensive-copy]]

```java
for (User user : UserList.toArray()) {                      // 개수 변수를 모른다
  System.out.printf("%d %s %s\n", user.getNo(), user.getName(), user.getEmail());
}
```
- **`Iterable` 을 구현하지 않으면 반복자를 만들어도 for-each 를 쓸 수 없다** — 20일 뒤 회차가 「직접적으로 Iterable의 구현체를 생성하여도 가능하다」까지 적고도 **자기가 만든 `List` 를 `Iterable` 로 만들지 않았다.** 그 회차가 손으로 만든 것은 `Iterator` 였고, 그래서 목록 출력이 `for (Object obj : boardList.toArray())` 에서 **`while (iterator.hasNext())` 로 되돌아간다.** 두 타입의 역할이 다르다 — `Iterable` 은 컬렉션이 「반복자를 줄 수 있다」고 선언하는 자리이고 `Iterator` 는 그 반복자다. **문법이 요구하는 것은 앞쪽**이고, 뒤쪽만 만들면 문법에 끼워지지 않는다 → [[iterator-pattern]]
- **그 회차가 for-each 와 사본의 관계를 드러낸다** — `toArray()` 로 도는 형태는 **for-each 를 쓰려고 배열을 매번 새로 만드는 것**이었다(아래 「개수 변수를 모른다」 코드가 그 형태다). 사본을 없애려니 for-each 를 잃었고, 둘을 동시에 얻는 길이 `Iterable` 이다. for-each 가 대상에게 맡기는 것이 「몇 개까지 도나」에서 **「어떻게 도나」까지** 넓어지는 것이 그 인터페이스의 값이다 → [[iterator-pattern]] · [[defensive-copy]]
- **for-each 로 배열 요소를 바꿀 수 없다** — 루프 변수에 값이 **복사**되므로 `menu = "x"` 는 배열에 반영되지 않는다. 요소를 고치려면 `menus[i] = ...` 여야 한다 → [[object-reference]]
- **세 자리는 모두 생략할 수 있다** — `for (;;)` 는 `while (true)` 와 같다. 조건 자리를 비우면 참으로 본다.
- **루프 변수의 스코프는 헤더에서 선언했을 때만 좁다** — 루프가 끝난 뒤 그 값을 써야 하면 `for` 밖에서 선언한다. 그러면 스코프가 넓어지는 대가를 치른다 → [[variable]]
- **`i <= length` 는 범위를 벗어난다** — 인덱스는 0부터이므로 `i < menus.length` 다. `<=` 로 쓰면 마지막 회차에서 `ArrayIndexOutOfBoundsException` 이 난다.
- **증감이 `i++` 여야 할 이유는 없다** — `i += 2`, `i--` 등 자유롭다. 다만 헤더의 세 조각이 서로 맞지 않으면(`i--` 인데 조건이 `i < n`) 무한 루프가 된다.

## 함께 보는 개념

- [[while-loop]] — 횟수가 아니라 조건으로 도는 반복
- [[break-continue]] — `continue` 가 증감문을 거쳐 조건으로 가는 자리
- [[array]] — for-each 와 `length` 가 맞물리는 대상
- [[increment-operator]] — 증감문에 쓰는 `i++`
- [[variable]] — 루프 변수의 선언 위치와 스코프
- [[do-while-loop]] — 최소 한 번 실행이 필요한 반복
- [[surrogate-key]] — 번호 출력과 for-each 가 같이 갈 수 있게 된 이유
- [[defensive-copy]] — for-each 에 넘길 배열을 만들어 주는 쪽
- [[linear-search]] — 인덱스 `for` 가 남아야 하는 자리
- [[iterator-pattern]] — for-each 가 실제로 쓰는 구조
- [[interface]] — `Iterable` 이라는 조건이 놓인 자리

## 출처

- [[2024-06-11-Day11]] — `for` 의 실행 순서 네 단계(초기화 → 조건 → 문장 → 증감)와 루프 변수의 스코프, 그리고 실습에서 메뉴 출력을 인덱스 `for` 로 쓴 뒤 for-each 로 바꾸는 것을 배웠다
- [[2024-06-20-Day19]] — 목록 출력이 `for (User user : UserList.toArray())` 로 바뀌며 **번호를 찍으면서도 for-each 를 쓰는** 형태가 나왔다. 번호가 데이터의 필드가 되고 목록이 사본으로 넘어온 두 변경이 겹쳐야 가능한 것이고, 같은 회차의 탐색·삭제 루프는 인덱스가 필요해 인덱스 `for` 로 남았다
- [[2024-07-10-Day32]] — for-each 의 **대상 조건**을 처음 문법으로 적은 회차다 — 「배열 또는 Iterable 구현체」. 같은 노트가 반복자 패턴을 손으로 만들면서 자기 `List` 를 `Iterable` 로 만들지 않아, Day19 이후 줄곧 for-each 였던 목록 출력이 `while (iterator.hasNext())` 로 되돌아간다. **for-each 를 쓸 수 있게 하는 것은 반복자가 아니라 그것을 내주겠다는 선언**이라는 것이 그 대비로 드러나고, `toArray()` 사본이 실은 for-each 를 쓰기 위한 값이었다는 것도 여기서 보인다
