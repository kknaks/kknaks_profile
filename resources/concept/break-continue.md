---
type: concept
id: break-continue
title: break 와 continue (그리고 라벨)
aliases:
  - break
  - continue
  - 라벨
  - 라벨문
  - label
  - labeled break
up:
  - 2024-06-11-Day11
  - 2024-06-13-Day14
tags:
  - java
  - 제어문
  - 문법
---

# break 와 continue (그리고 라벨)

반복문의 흐름을 중간에 바꾸는 두 문장. `break` 는 반복을 **끝내고**, `continue` 는 이번 회차만 **건너뛴다**. 라벨은 그 대상을 바깥 반복문으로 옮기는 표시다.

## 정의

| 문장 | 하는 일 | 다음에 실행되는 곳 |
|---|---|---|
| `break` | 반복문을 즉시 종료한다 | 반복문 **뒤** |
| `continue` | 남은 문장을 건너뛴다 | 반복문의 **조건식** |

```java
while (조건)
	문장;
   if (조건) break;      // 조건이 참이면 반복문을 종료한다

while (조건)
	문장1;
   if (조건) continue;   // 조건이 참이면 문장2를 수행하지 않고 while문 조건으로 돌아간다
	문장2
```

둘 다 **가장 안쪽 반복문**만 대상으로 한다. 바깥까지 나가려면 반복문에 이름을 붙인다.

```java
// 라벨명: 반복문1 { 반복문2 {break 라벨명;}}
// 라벨 문법:
//      라벨: 문장;
//      라벨: {문장1, 문장2, ...}
```

## 사용 예시

구구단을 돌다 `5 * 5` 에서 이중 루프를 한 번에 빠져나온다.

```java
int x = 2, y = 1;

myloop:
  while (x <= 9) {

    while (y <= 9) {
      System.out.printf("%d * %d = %d\n", x, y, x * y);
      if (x == 5 && y == 5)
        break myloop; // myloop 라벨에 소속된 문장을 나간다.
      y++;
    }

    System.out.println();
    x++;
    y = 1;
  }
```

라벨 없이 `break` 를 쓰면 안쪽 `while` 만 끝나고 `x++` 를 지나 다시 바깥 루프가 돈다.

메뉴 루프에서는 종료 항목을 골랐을 때 `break` 가 루프 자체를 끝내는 신호로 쓰인다.

```java
while (true) {
    menuNo = keyboard.nextInt();
    if (menus[menuNo - 1].equals("종료")) {
        break;          // 종료 메뉴 = 루프 종료 조건
    }
    // ...
}
```

### 층이 둘이면 라벨 대신 메서드로 가른다

서브메뉴를 붙이면서 루프가 두 층이 됐다. 그런데 라벨은 쓰이지 않았다 — 안쪽 루프를 **별도 메서드에 두었기** 때문이다.

```java
static void processMenu(String menuTitle, String[] menus) {
    printSubMenu(menuTitle, menus);
    while (true) {
        String command = prompt("메인/" + menuTitle);
        if (command.equals("menu")) {
            printSubMenu(menuTitle, menus);
            continue;                     // 목록만 다시 보여 주고 이번 회차 끝
        } else if (command.equals("9")) {
            break;                        // 이 루프만 끝난다 = 이전 메뉴로
        }
        // ... 번호 처리
    }
}
```

`break` 로 나오면 메서드가 끝나고 실행은 **부른 자리**, 즉 메인 루프의 다음 회차로 간다. 라벨로 두 층을 다루는 대신 층 하나를 이름 있는 메서드로 옮긴 것이고, 그 덕에 「이전 메뉴로 돌아간다」가 `break` 한 줄이 된다 → [[command-loop]]

`continue` 는 여기서 회차를 건너뛰는 것 이상의 일을 한다. 이것이 없으면 `menu` 라는 입력이 아래의 숫자 해석까지 흘러가 「숫자로 메뉴 번호를 입력하세요」가 출력된다 → [[number-parsing]]

## 왜 중요한가

**중첩 루프에서 "전부 나가기"를 표현할 방법이 라벨뿐이다.** 없으면 플래그 변수를 두고 안쪽에서 세우고 바깥 조건에서 다시 검사해야 한다 — 종료 조건이 두 곳으로 갈라지고, 한 곳만 고치면 조용히 어긋난다.

`continue` 의 값은 **들여쓰기를 줄이는 것**이다. "이 경우는 건너뛴다"를 앞에서 걸러 내면 뒤 코드가 `else` 블록 안으로 들어가지 않는다. 다만 그 대가로 **루프의 끝이 여러 곳이 된다** — 어디서 다음 회차로 넘어가는지 읽으려면 본문을 훑어야 한다.

## 경계와 오해

- **`continue` 는 루프의 처음이 아니라 조건식으로 간다** — 그래서 `for` 에서는 증감문을 **거치고** 조건을 본다. 반대로 `while` 에서 증감을 본문 끝에 뒀다면 `continue` 가 그것을 건너뛰어 **무한 루프**가 된다. `for` 와 `while` 에서 `continue` 의 안전도가 다른 이유다.
- **`switch` 안의 `break` 와 반복문의 `break` 는 대상이 다르다** — 반복문 안 `switch` 에서 `break` 를 쓰면 `switch` 만 나오고 루프는 계속 돈다. 루프까지 끝내려면 라벨을 쓰거나 조건을 따로 둔다 → [[switch-statement]]
- **`continue` 는 `switch` 에 없다** — `switch` 는 반복이 아니므로 건너뛸 다음 회차가 없다. `switch` 안의 `continue` 는 그것을 감싼 반복문을 대상으로 한다.
- **라벨은 goto 가 아니다** — 라벨이 가리키는 곳으로 뛰어가는 것이 아니라 **그 문장을 나가거나 그 문장의 다음 회차로 가는** 것뿐이다. 뒤로 돌아갈 수 없다. Java 는 `goto` 를 예약어로만 남겨 두고 문법에서 뺐다.
- **라벨은 반복문 전용이 아니다** — 문법상 아무 문장에나 붙일 수 있고 블록에 붙여 `break 라벨;` 로 블록을 빠져나올 수도 있다. 다만 실무에서 그렇게 쓰는 코드는 드물다.
- **`break` 가 많은 루프는 `while (true)` 와 다르지 않다** — 종료 조건이 조건식에서 본문으로 옮겨 간 상태다. 나쁜 것은 아니지만, 조건식만 읽고 루프의 끝을 짐작할 수 없다는 뜻이다 → [[while-loop]]
- **메서드로 가르는 것은 라벨의 대안이지만 같은 것은 아니다** — 안쪽 루프를 메서드로 옮기면 `break` 가 그 층만 끝내고 `return` 이 바깥의 다음 회차로 돌려보낸다. 라벨보다 이름이 붙어 읽히는 대신, **두 층을 한 번에 나가는 것은 여전히 안 된다.** 바깥까지 끝내려면 반환값이나 예외로 신호를 올려 보내야 한다 → [[method]]
- **같은 `break` 가 층마다 다른 뜻이 된다** — 메뉴 프로그램에서 메인 루프의 `break` 는 프로그램 종료이고 서브 루프의 `break` 는 이전 메뉴로다. 문법은 하나인데 의미는 그 루프가 무엇을 반복하는지가 정한다 → [[command-loop]]

## 함께 보는 개념

- [[while-loop]] — `break`·`continue` 가 가장 많이 쓰이는 자리
- [[for-loop]] — `continue` 가 증감문을 거치는 쪽
- [[do-while-loop]] — 조건식이 뒤에 있어 `continue` 가 아래로 내려간다
- [[switch-statement]] — 같은 `break` 키워드가 다른 대상을 갖는 곳
- [[if-statement]] — `break`·`continue` 를 거는 판단
- [[command-loop]] — 층마다 `break` 의 뜻이 달라지는 구조
- [[method]] — 안쪽 루프를 옮겨 층을 가르는 수단

## 출처

- [[2024-06-11-Day11]] — `break`·`continue` 가 반복 흐름을 바꾸는 방식과, 라벨(`myloop:`)을 붙여 `break myloop;` 로 이중 루프를 한 번에 빠져나오는 것을 구구단 예제로 배웠다
- [[2024-06-13-Day14]] — 서브메뉴 루프에서 `break` 가 「이전 메뉴로」, `continue` 가 「목록 다시 출력」이 되는 것을 배웠다. 루프 층을 메서드로 갈라 라벨 없이 두 층을 다룬 자리다
