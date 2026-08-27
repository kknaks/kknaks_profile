---
type: concept
id: switch-statement
title: switch 문
aliases:
  - switch
  - switch 문
  - fall-through
  - 폴스루
up:
  - 2024-06-05-Day09
  - 2024-06-11-Day11
  - 2024-07-09-Day31
tags:
  - java
  - 제어문
  - 문법
---

# switch 문

하나의 값을 여러 `case` 와 견주어 맞는 곳부터 실행하는 조건문. 맞는 `case` 가 없으면 `default` 를 실행한다.

## 정의

```java
switch (식 또는 변수) {
    case 값1:
        // 변수가 값1에 해당하면 실행할 코드
        break;
    case 값2:
        // 변수가 값2에 해당하면 실행할 코드
    case 값3:
        // 값3에 해당하면 실행할 코드
        // case 값2 에 break 가 없어서 값2일 때도 여기까지 실행된다
        break;
    default:
        // 어느 것에도 해당하지 않을 때 실행되는 코드
}
```

**`break` 가 없으면 다음 `case` 로 흘러 내려간다.** 이것을 fall-through 라 한다. `switch` 는 "맞는 `case` 를 실행한다"가 아니라 **"맞는 `case` 로 뛰어들어 `break` 를 만날 때까지 계속한다"** 가 정확한 설명이다.

### 올 수 있는 값이 정해져 있다

| 자리 | 올 수 있는 것 |
|---|---|
| `switch (...)` | 정수 · 문자열 · Enum |
| `case ...` | 리터럴 · `final` 변수 · Enum 상수 |

`case` 에 **일반 변수는 쓸 수 없다.** 컴파일 시점에 값이 확정되는 **이산적인 값**만 온다 → [[literal]]. 그래서 `case` 는 「이 값이면」만 표현할 수 있고 「이 범위면」이나 「이 조건이면」은 표현할 수 없다.

## 사용 예시

메뉴 번호로 분기한다. 각 `case` 마다 `break` 를 둬서 하나만 실행되게 한다.

```java
switch (menuNo) {
    case 1:
        System.out.println("회원");
        break;
    case 2:
        System.out.println("팀");
        break;
    case 6:
        System.out.println("종료합니다.");
        scanner.close();
        break;
    default:
        System.out.println("메뉴 번호가 옳지 않습니다.");
}
```

`default` 가 맨 끝에 있으므로 `break` 를 생략해도 된다 — 흘러 내려갈 곳이 없다.

## 왜 중요한가

**값 하나로 갈리는 분기가 `if-else` 사슬보다 읽힌다.** "이 변수를 보고 있다"가 한 줄로 드러나고, 어떤 값들을 다루는지가 나란히 보인다.

fall-through 는 **의도해서 쓰면 도구, 실수로 두면 버그**다. 여러 값을 같게 처리할 때는 `case` 를 나란히 두는 방식으로 쓰이지만, `break` 를 잊은 것과 생김새가 같아서 구분되지 않는다. 그래서 의도한 fall-through 에는 주석을 남긴다.

### `switch` 를 써야 할 때와 배열로 접어야 할 때

값마다 **하는 일이 다르면** `switch` 가 맞다. 하지만 값마다 하는 일이 같고 **출력할 데이터만 다르면** `case` 를 늘리는 것이 곧 데이터를 코드에 박는 것이 된다.

```java
switch (menuNo) {                              // 이 여섯 개가
    case 1: System.out.println("회원"); break;
    case 2: System.out.println("팀"); break;
    // ... case 6 까지
}

System.out.println(menus[menuNo - 1]);         // 이 한 줄이 된다
```

이 필기의 실습이 그 전환을 그대로 보여 준다 — `case` 여섯 개가 [[array]] 인덱스 접근 한 줄로 접혔고, 메뉴를 추가할 때 고칠 곳이 배열 선언 하나가 됐다. **`switch` 가 길어지면 분기가 아니라 데이터를 적고 있는지 의심할 자리다.**

### 하는 일이 다를 때도 접힌다 — 표에 객체를 담는다

**28일 뒤 회차가 같은 전환을 한 단 위에서 한 번 더 한다.** 그때 접힌 것은 「출력할 문자열」이었고 이번에 접히는 것은 **「실행할 객체」**다.

```java
switch (menuTitle) {                        // 이 다섯 개가
  case "회원": userCommand.execute(); break;
  case "프로젝트": projectCommand.execute(); break;
  case "게시판": boardCommand.execute(); break;
  case "공지사항": noticeCommand.execute(); break;
  case "도움말": helpCommand.execute(); break;
  default:
    System.out.printf("%s 메뉴의 명령을 처리할 수 없습니다.\n", menuTitle);
}
```

```java
Command command = commandMap.get(menuTitle);   // 이 세 줄이 된다
if (command == null) { ... return; }
command.execute();
```

**다섯 `case` 가 하는 일이 이미 같았다** — `execute()` 를 부른다. 다른 것은 어느 변수인가뿐이고, 그렇다면 그 짝(`"회원"` → `userCommand`)이 데이터다. 조건은 앞의 배열 접기와 똑같다 — **모든 갈래가 같은 형태로 접힐 수 있어야 하고**, 갈래마다 인자가 다르거나 문장이 여럿이면 그것을 먼저 객체로 만들어야 한다 → [[dispatch-table]] · [[polymorphism]]

`default:` 도 자리를 옮긴다. 「어느 `case` 에도 안 걸림」이 「조회 결과가 `null`」이 되어, **같은 안전망이 문법에서 값 검사로 내려온다** → [[object-reference]]

## 경계와 오해

- **`break` 는 `case` 를 끝내는 것이 아니라 `switch` 를 빠져나오는 것이다** — 그래서 없으면 다음 `case` 의 코드까지 실행된다. `case` 가 블록이 아니라 **뛰어들 지점(label)** 이기 때문이다.
- **`switch` 안의 `break` 와 루프의 `break` 는 대상이 다르다** — 루프 안의 `switch` 에서 `break` 를 쓰면 `switch` 만 빠져나오고 루프는 계속 돈다. 루프를 끝내려면 라벨을 쓰거나 조건을 따로 둔다 → [[break-continue]]
- **`case` 에는 상수만 온다** — 리터럴·`final` 변수·Enum 상수만 가능하고 일반 변수는 안 된다. 범위나 조건식도 쓸 수 없어서 그런 분기는 [[if-statement]] 로 간다.
- **`switch` 는 반복문이 아니다** — 이 필기는 `switch` 를 「2. 반복문」 절 아래에 넣었다. 값으로 갈리는 **조건문**이고, `break` 키워드를 반복문과 공유하는 것 때문에 더 헷갈린다. 반복을 만드는 것은 `while`·`do~while`·`for` 뿐이다 → [[while-loop]]
- **`default` 는 맨 끝에 있어야 하는 것이 아니다** — 관례로 끝에 두지만 중간에 둘 수도 있고, 그 경우 `break` 가 필요하다.
- **문자열 `switch` 는 내용을 비교한다** — `if` 로 같은 분기를 쓸 때는 `==` 가 아니라 `.equals()` 를 써야 하는데, `switch (문자열)` 은 그 처리를 해 준다 → [[string-comparison]]. `HashMap` 의 키 조회도 같은 것을 해 주므로 표로 접을 때 이 성질은 잃지 않는다 → [[hash-based-collection]]
- **`case` 목록이 사라지면 다루는 값이 한눈에 안 보인다** — `switch` 를 읽으면 이 값이 무엇들일 수 있는지가 나란히 드러난다. 표로 접으면 그 목록이 **등록하는 코드**로 흩어지고, 등록이 여러 곳에서 일어나면 전부 찾아야 한다. 표로 바꾸는 것이 공짜가 아닌 첫 번째 자리다 → [[dispatch-table]]
- **오타가 걸리는 시점이 뒤로 밀린다** — `case "회웜":` 은 컴파일은 되지만 그 자리에서 눈에 띄고 다른 `case` 들과 나란히 놓여 비교된다. `put("회웜", ...)` 는 **눌러 봐야** 안다. 그리고 증상이 「없는 메뉴」와 같아서 오타와 미등록이 구별되지 않는다 — `case` 를 enum 으로 쓰면 컴파일 시점으로 되찾을 수 있고 표의 키도 그렇다 → [[literal]]

## 함께 보는 개념

- [[if-statement]] — 조건식·범위로 갈리는 쪽
- [[do-while-loop]] · [[while-loop]] — 분기를 감싸는 반복
- [[break-continue]] — 같은 `break` 키워드가 다른 대상을 갖는 곳
- [[array]] — 긴 `switch` 를 접는 방향(값이 데이터일 때)
- [[dispatch-table]] — 긴 `switch` 를 접는 방향(값이 실행할 것일 때)
- [[hash-based-collection]] — 문자열 키로 표를 만드는 자료구조
- [[polymorphism]] — 갈래를 타입에게 넘기는 쪽
- [[standard-input]] — 분기할 값을 받는 곳

## 출처

- [[2024-06-05-Day09]] — `case`·`default` 구조와, `break` 가 없으면 다음 `case` 도 실행된다는 것을 배웠다
- [[2024-06-11-Day11]] — `switch` 조건에 정수·문자열·Enum 이 오고 `case` 에는 리터럴·`final` 변수·Enum 만 온다는 것(이산적인 값), 그리고 실습에서 `case` 여섯 개를 배열 인덱스 접근으로 접는 것을 배웠다
- [[2024-07-09-Day31]] — **28일 전 Day11 의 「`switch` → 배열」 전환이 「`switch` → 표」로 한 단 올라간 자리다.** 실습 프로젝트의 `App.processMenu` 에서 다섯 `case` 가 전부 `execute()` 를 부르고 있었으므로 그 짝(메뉴명 → 명령 객체)을 `Map<String, Command>` 에 담아 조회 세 줄로 접었다. 접히는 조건이 같다 — 갈래들이 이미 같은 형태였다는 것. `default:` 는 `commandMap.get()` 의 `null` 검사로 옮겨졌고, 그 대가로 다루는 값의 목록이 코드에서 사라지고 키 오타가 실행 시점으로 밀린다
