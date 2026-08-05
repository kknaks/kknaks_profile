---
type: concept
id: command-loop
title: 명령 루프와 계층 메뉴
aliases:
  - 명령 루프
  - command loop
  - 메뉴 루프
  - menu loop
  - 서브메뉴
  - submenu
  - 계층 메뉴
  - 모드 루프
up:
  - 2024-06-13-Day14
  - 2024-07-05-Day30
  - 2024-07-08-Day30
  - 2024-07-15-Day35
tags:
  - cli
  - 제어문
  - 설계
  - 사용자경험
---

# 명령 루프와 계층 메뉴

프롬프트를 띄우고 한 줄을 받아 해석해 분기하고 다시 프롬프트로 돌아오는 구조. **메뉴 계층은 이 루프를 한 층 더 쌓아 만들고, 층을 오르내리는 일은 호출과 `return` 이 대신한다.**

## 정의

한 회차가 네 단계다.

1. **출력** — 프롬프트(그리고 필요하면 항목 목록)
2. **입력** — 한 줄을 받는다 → [[standard-input]]
3. **해석** — 특별 명령인가, 번호인가 → [[number-parsing]]
4. **분기** — 실행하고 다시 1로

번호로 해석하기 **전에** 걸러야 하는 특별 명령이 있다.

| 입력 | 뜻 | 하는 일 |
|---|---|---|
| `menu` | 목록을 다시 보여 달라 | 출력하고 `continue` |
| `9` | 이전 층으로 | 이 층의 루프를 `break` |
| 「종료」 항목 | 프로그램 끝 | 최상위 루프를 `break` |
| 그 외 | 항목 번호 | 조회해서 없으면 안내 |

층은 **중첩 `while` 이 아니라 메서드 호출**로 만든다. 상위 루프가 하위 루프를 가진 메서드를 부르고, 하위의 `break` 는 그 메서드를 끝내며 `return` 이 상위 루프의 다음 회차로 돌려보낸다 → [[break-continue]] · [[jvm-stack]]

## 사용 예시

이 필기의 서브메뉴 루프가 그대로 이 구조다.

```java
static void processMenu(String menuTitle, String[] menus) {
    printSubMenu(menuTitle, menus);
    while (true) {
        String command = prompt("메인/" + menuTitle);
        if (command.equals("menu")) {
            printSubMenu(menuTitle, menus);
            continue;
        } else if (command.equals("9")) {   // 이전 메뉴 선택
            break;
        }

        try {
            int menuNo = Integer.parseInt(command);
            String subMenuTitle = getMenuTitle(menuNo, menus);
            if (subMenuTitle == null) {
                System.out.println("유효한 메뉴 번호가 아닙니다.");
            } else {
                System.out.println(subMenuTitle);
            }
        } catch (NumberFormatException ex) {
            System.out.println("숫자로 메뉴 번호를 입력하세요.");
        }
    }
}
```

메인 루프는 그것을 부르기만 한다.

```java
if (menuNo >= 1 && menuNo <= 4) {
    processMenu(menuTitle, subMenus[menuNo - 1]);   // 들어간다 — 돌아오면 다음 회차
} else {
    System.out.println(menuTitle);
}
```

**「이전으로 돌아가기」를 표현하는 코드가 없다.** 서브 루프를 `break` 로 나오면 메서드가 끝나고, 실행은 자연히 메인 루프의 다음 회차로 간다. 층이 [[jvm-stack]] 의 프레임으로 표현되기 때문에 「현재 어느 메뉴에 있는가」를 담는 변수가 필요하지 않다.

프롬프트가 그 위치를 사용자에게 알려 준다 → [[parameterization]]

```text
메인> 1
[회원]
1. 등록a
2. 목록
...
9. 이전
메인/회원> 9
메인>
```

### 25일 뒤, 층이 메서드에서 클래스가 된다

같은 골격이 리팩터링 회차에서 **객체 안으로 들어간다.** 서브메뉴 루프를 가진 `static void processMenu(String, String[])` 가 사라지고, 각 메뉴가 자기 루프를 가진 클래스가 된다.

| | Day14 | 리팩터링 회차 |
|---|---|---|
| 한 층 | `static` 메서드 하나 | 클래스 하나 (`UserCommand`) |
| 층의 항목 목록 | 매개변수로 받는 `String[] menus` | 그 클래스의 필드 |
| 층으로 들어가기 | `processMenu(title, menus)` | `userCommand.execute()` |
| 층에서 나오기 | `break` → `return` | 그대로 |
| 층의 상태 | 없다 | **그 객체의 필드**(`userList` 등) |

**나가는 방법은 하나도 안 바뀌었다** — `9` 로 `break` 하고 메서드가 끝나며 상위 루프로 돌아간다. 바뀐 것은 **그 층이 자기 데이터를 가질 수 있게 된 것**이고, 그래서 「회원 목록」이 층과 함께 산다 → [[instance]]

그리고 한 단계 더 가서 **루프 자체가 부모로 올라간다.** 네 Command 의 `execute()` 가 글자까지 같았으므로 `AbstractCommand` 에 한 벌만 남고, 각 Command 는 「메뉴 목록」과 「번호를 받았을 때 할 일」만 채운다.

```java
@Override
public void processMenu(String menuName) {    // 부모의 루프가 이것을 부른다
  switch (menuName) {
    case "등록": this.addUser(); break;
    ...
  }
}
```

**이 회차 이후 새 메뉴를 만드는 사람은 루프를 다시 쓰지 않는다.** `menu` 명령도, `9` 도, `NumberFormatException` 처리도 부모에 한 번 있고, 여기 정리된 네 단계 중 **1·2·3 이 부모의 것이고 4(분기)만 자식의 것**이 된다 → [[template-method-pattern]] · [[generalization]]

### 32일 뒤, 루프가 「층」 자체의 것이 된다

Day35 의 컴포짓 리팩터링에서 루프가 상속 계층을 떠나 **트리의 가지**(`MenuGroup`)로 들어간다. 골격은 알아볼 수 있게 그대로다.

```java
@Override
public void execute() {
  menuPath.push(title);
  printMenus();
  while (true) {
    String command = Prompt.input("%s>", getMenuPathTitle(menuPath));
    if (command.equals("menu")) {
      printMenus();
      continue;
    } else if (command.equals("0")) {      // 이전 메뉴 선택
      menuPath.pop();
      return;
    }

    try {
      int menuNo = Integer.parseInt(command);
      Menu menu = getMenu(menuNo - 1);
      if (menu == null) {
        System.out.println("유효한 메뉴 번호가 아닙니다.");
        continue;
      }
      menu.execute();
    } catch (NumberFormatException ex) {
      System.out.println("숫자로 메뉴 번호를 입력하세요.");
    }
  }
}
```

네 단계와 특별 명령 표는 그대로 성립하고, **세 가지가 바뀌었다.**

| | Day14 ~ Day31 | Day35 |
|---|---|---|
| 나가기 입력 | `9` (화면에도 `9. 이전`) | **`0`** (화면에도 `0. 이전`) |
| 나가기 라벨 | 코드에 박힌 「이전」 | `setExitMenuTitle(...)` — 뿌리는 「종료」 |
| 층에서 나오기 | `break` | `return` (루프가 메서드의 전부다) |

**뿌리와 가지가 같은 클래스가 되었으므로 「종료」와 「이전」의 차이가 필드 하나로 줄었다.** Day14 부터 메인 루프와 서브 루프는 구조가 닮았어도 나가기의 뜻이 달라 합칠 수 없었는데, 그 차이가 **코드가 아니라 값**이 된 것이다 — `mainMenu.setExitMenuTitle("종료")` 한 줄이 뿌리를 뿌리로 만든다 → [[composite-pattern]] · [[parameterization]]

## 왜 중요한가

**CLI 에는 화면 상태가 없다.** 지나간 출력은 스크롤로 밀려나므로 사용자가 지금 어디 있는지 아는 단서는 프롬프트 문자열뿐이고, 나가는 길은 매 층이 스스로 제공해야 한다(`9. 이전`). 이 두 가지가 계층 메뉴의 UI 전부다 → [[cli]]

**층을 호출로 만들면 상태 변수가 사라진다.** 한 루프에 `currentMenu` 같은 변수를 두고 처리하면 모든 분기가 그 변수를 검사해야 하고, 어디서 값을 바꾸는지가 코드 전체에 흩어진다. 호출로 층을 만들면 각 루프가 **자기 층의 항목만** 알면 되고, 복귀 지점은 호출한 자리라는 것이 언어가 보장한다.

**해석 순서가 곧 명령 체계다.** `menu`·`9` 를 숫자 해석보다 먼저 처리하기 때문에 그것들이 항목 번호와 충돌하지 않는다. 순서를 뒤집으면 `menu` 가 `Integer.parseInt` 에서 예외로 떨어져 「숫자로 입력하세요」가 뜬다 — 기능이 사라지는 것이 아니라 **엉뚱한 메시지로 바뀐다** → [[exception-handling]]

## 경계와 오해

- **`9` 는 메뉴 번호가 아니다 — 32일 뒤 `0` 으로 바뀌면서 충돌 가능성이 사라진다** — `printSubMenu` 가 `9. 이전` 을 항목처럼 출력하지만 배열에는 없다. 번호 검증(1 ~ `menus.length`)에 걸리지 않도록 **파싱 전에 문자열로 비교해** 걸러 낸다. 즉 화면의 번호 체계와 배열 인덱스는 다른 체계이고, **항목이 아홉 개를 넘기면 이 번호가 충돌한다.** Day35 가 그 자리를 `0` 으로 옮긴다 — 항목 번호는 `int i = 1` 에서 시작해 위로만 가므로 **`0` 은 어떤 항목 수에도 비지 않는 번호**다. 「비어 있을 것 같은 큰 수를 고른다」에서 「구조적으로 절대 안 겹치는 수를 고른다」로 바뀐 것이고, 항목이 열 개를 넘는 메뉴가 실제로 생기기 전에 고쳐진 셈이다 → [[multidimensional-array]] · [[one-based-numbering]]
- **「서브메뉴 번호가 null」인 것이 아니다** — 필기의 의사코드가 그렇게 적었지만 `int` 는 `null` 이 될 수 없다. `null` 인 것은 `getMenuTitle` 의 **반환값**이고, 그것이 「그런 번호는 없다」의 신호다. 번호와 조회 결과를 같은 것으로 읽으면 왜 `subMenuTitle == null` 로 검사하는지가 설명되지 않는다 → [[conditional-flattening]]
- **`continue` 는 흐름 제어가 아니라 오분류 방지로 쓰였다** — `menu` 를 처리한 뒤 `continue` 를 빼면 아래로 흘러가 `Integer.parseInt("menu")` 가 예외를 던지고 「숫자로 메뉴 번호를 입력하세요」가 출력된다. 목록은 이미 나왔으니 동작은 되지만 **메시지가 거짓말을 한다** → [[break-continue]]
- **`try` 가 파싱만 감싸지 않고 실행까지 감싼다 — 그래서 남의 예외가 이 루프의 메시지로 나온다** — `catch (NumberFormatException)` 이 노리는 것은 `Integer.parseInt(command)` 하나인데, `try` 블록 안에 **고른 것을 실행하는 줄까지** 들어 있다. Day31 의 `AbstractCommand.execute` 부터 이 모양이고 Day35 의 `MenuGroup.execute` 도 `menu.execute()` 를 감싼 채다. 명령이 자기 입력을 숫자로 읽다가(`Prompt.inputInt("회원번호?")`) 던지는 `NumberFormatException` 이 **여기까지 올라와 「숫자로 메뉴 번호를 입력하세요」로 안내된다.** 사용자가 잘못 넣은 것은 회원번호인데 메뉴 번호를 지적받는 것이고, 예외 종류가 같아서 **구별할 방법이 없다.** 파싱 줄만 감싸거나 파싱을 `try` 밖으로 빼면 풀리는 자리이며, Day35 에서는 감싼 것이 **트리 전체**여서 범위가 더 넓어졌다 → [[exception-handling]] · [[number-parsing]]
- **그리고 그 catch 가 위층에 하나 더 있는데 그쪽은 절대 실행되지 않는다** — Day35 의 `App.execute()` 는 `mainMenu.execute()` 를 `try`/`catch (NumberFormatException)` 로 감싼다. 그런데 `MenuGroup.execute()` 가 자기 루프 안에서 그 예외를 **전부 잡아 삼키므로** 밖으로 나오는 것이 없다. 루프를 아래로 옮기면서 위층의 방어가 죽은 코드가 된 것이고, **없어져야 할 것이 남는 쪽이라 아무 증상도 없다** → [[exception-handling]] · [[refactoring]]
- **같은 `break` 가 층마다 다른 뜻이다** — 메인 루프의 `break` 는 프로그램 종료이고 서브 루프의 `break` 는 이전 메뉴로다. 그래서 **서브메뉴에서 「종료」를 고르게 만들 수는 없다** — `break` 는 자기 층만 끝내므로 종료 신호를 상위로 올려 보내는 방법(반환값·예외)이 따로 필요하다. 이 프로그램은 서브에 종료 항목을 두지 않아 문제가 드러나지 않았다. **Day35 의 `setExitMenuTitle` 이 이것을 푼 것처럼 보이지만 아니다** — 라벨만 바꿀 수 있게 된 것이고 동작은 여전히 `return` 하나다. 뿌리에서 `return` 하면 `App.execute()` 로 돌아가 프로그램이 끝나므로 「종료」가 맞고, 가지에서는 부모 루프로 돌아가므로 「이전」이 맞다 — **같은 코드가 위치에 따라 다른 뜻이 되는 성질은 그대로이고, 이름을 그 위치에 맞게 붙일 수 있게 된 것뿐**이다. 중간 층에서 프로그램을 끝내는 일은 여전히 못 한다 → [[composite-pattern]]
- **목록을 언제 그리는가는 화면에 상태가 있는가로 정해진다** — 이 필기는 `printSubMenu` 를 루프 **앞**에 두어 진입할 때 한 번만 출력한다. 그래서 회차마다 목록이 안 보이고 `menu` 명령이 필요해졌고, 서브에서 `9` 로 나왔을 때 메인 메뉴가 다시 뜨지 않는 것도 같은 이유다. **22일 뒤 팀 프로젝트에서 이것이 취향 문제가 아니게 된다** — 그쪽 메인 화면은 메뉴와 함께 「당일 날짜와 당일 달성률 및 전체 누적 달성률」과 오늘 할 일 4가지의 체크 표시를 같이 띄우고, 명령들이 바로 그 값을 바꾼다. 명령을 처리한 뒤 다시 그리지 않으면 **화면이 이전 회차의 상태를 보여 주므로** 회차마다 출력하는 것 외에 선택이 없고, 그러면 `menu` 명령 자체가 필요 없어진다. 진입 시 한 번만 그려도 되는 것은 **메뉴가 고정 텍스트일 때뿐**이다 → [[gamification]]
- **루프를 끝내는 것이 사용자의 명령만은 아니다** — 이 필기의 종료는 전부 사용자가 고른 것이다(「종료」 항목 · `9`). 22일 뒤 프로젝트는 「누적달성률 20%미만 시 프로그램 종료」를 두는데, **아무 명령도 「종료」가 아니면서 명령을 처리한 결과로 루프가 끝난다.** 그러면 종료 검사가 놓일 자리가 달라진다 — 분기 안이 아니라 **회차의 끝**에 한 번 있어야 어느 명령이 상태를 바꾸든 같은 곳에서 걸린다. 「종료 = 메뉴 항목 하나」로 굳으면 그 검사를 명령마다 복사하고 하나를 빠뜨리게 된다 → [[gamification]]
- **루프의 한 회차와 도메인의 한 단위는 다르다** — 그 프로젝트의 「일과종료」는 명령 한 번이 하루를 넘긴다(「저장된 ToDoList 객체를 ArrayList에 추가」하고 「새로운 ToDoList 객체생성 및 날짜 조정」). 루프는 입력 한 번을 한 회차로 도는데 도메인은 하루를 단위로 세므로, **「지금 며칠인가」를 루프가 상태로 들고 있어야** 화면과 판정이 같은 날을 본다. 이 필기의 루프는 회차마다 남기는 상태가 없어 그 문제가 없었다 → [[date-time]]
- **층을 무한히 만들 수 있으면 스택이 쌓인다** — 「들어가기」가 호출이고 「나가기」가 `return` 이므로, 사용자가 계속 더 깊이 들어갈 수 있는 구조라면 프레임이 계속 쌓여 스택 오버플로가 가능하다. 메뉴 깊이가 둘로 고정되어 있어 문제되지 않는 것이다 → [[recursion]]
- **메인 루프와 서브 루프는 같은 코드가 아니다** — 구조가 닮아서 하나로 합치고 싶어지지만, 메인은 「종료」와 서브 진입을 갖고 서브는 「이전」을 갖는다. 이 필기가 공유한 것은 루프가 아니라 **그 안에서 쓰는 메서드**(`prompt`·`getMenuTitle`)다 → [[parameterization]]
- **층을 클래스로 만들어도 층이 아닌 메뉴가 생긴다** — 리팩터링 회차의 「도움말」은 서브메뉴가 없어서 들어갈 층이 없고, `App` 의 `switch` 안에서 한 줄 출력으로 끝난다. `HelpCommand` 클래스를 만들어 두고도 그렇다. **모든 메뉴가 「진입」인 것은 아니라는 사실**이 층을 객체로 만드는 순간 예외로 드러나는 것이고, 그것을 「명령」과 「진입」으로 갈라 두지 않으면 한쪽이 틀에서 빠진다 → [[template-method-pattern]]
- **루프가 부모로 올라가면 자식만 읽어서는 흐름을 알 수 없다** — 자식에 남은 `processMenu` 는 언제 불리는지, `9` 를 누르면 무엇이 끝나는지 자기 코드에 없다. 층 구조가 **호출 스택에서 상속 계층으로 한 겹 더 옮겨진 것**이고, 읽는 비용이 그만큼 늘어난다. 그 대가로 얻는 것은 「루프를 네 번 쓰지 않는다」다 → [[generalization]]
- **루프가 있는 메서드의 이름은 한 번의 처리처럼 읽힌다 — 32일 뒤 그것이 인터페이스로 올라간다** — `processMenu` 는 「메뉴 하나를 처리한다」로 읽히지만 실제로는 사용자가 나갈 때까지 돌아오지 않는다. 부르는 쪽에서 이것이 **한 층 진입**이라는 것이 이름에 드러나지 않는다. Day14 필기가 1.2 에서 `processSubmenu` 라 적었다가 최종 코드에서 `processMenu` 로 바꾼 자리이기도 하다. **Day35 에서는 이름을 고쳐서 해결할 수 없게 된다** — `Menu.execute()` 하나가 `MenuItem` 의 「금방 끝나는 일」과 `MenuGroup` 의 「층에 들어가 머무는 일」을 동시에 뜻하고, 호출부(`menu.execute()`)는 어느 쪽인지 **알 수 없어야 하는 것이 이 구조의 목적**이다. 균일하게 부를 수 있게 된 대가로 수명의 차이가 타입에서 지워진 것이다 → [[method]] · [[composite-pattern]]

## 함께 보는 개념

- [[while-loop]] — 이 루프의 골격
- [[break-continue]] — 층을 나가고 회차를 건너뛰는 문법
- [[standard-input]] — 한 줄을 받는 쪽
- [[number-parsing]] — 명령을 번호로 해석하는 쪽
- [[exception-handling]] — 숫자가 아닌 입력을 감당하는 자리
- [[jvm-stack]] — 메뉴 층이 실제로 쌓이는 곳
- [[recursion]] — 들어가기와 나오기가 같은 모양인 구조
- [[cli]] — 이 UI 가 성립하는 환경
- [[multidimensional-array]] — 층마다 다른 항목 목록을 담는 자료구조
- [[parameterization]] — 두 층이 같은 메서드를 쓰게 만드는 방법
- [[string-comparison]] — 특별 명령을 걸러 낼 때 쓰는 비교
- [[gamification]] — 화면에 상태가 생기고 종료가 조건이 되는 쪽
- [[date-time]] — 회차가 아니라 하루를 단위로 세는 쪽
- [[template-method-pattern]] — 이 루프가 부모로 올라간 뒤의 구조
- [[generalization]] — 네 벌이던 루프를 한 벌로 만드는 이동
- [[instance]] — 층이 자기 데이터를 갖게 되는 조건
- [[composite-pattern]] — 루프가 트리의 가지로 들어간 뒤의 구조
- [[command-pattern]] — 루프를 빼앗긴 뒤 커맨드에 남은 것
- [[one-based-numbering]] — 나가기 번호를 `0` 으로 옮길 수 있는 근거
- [[number-parsing]] — 같은 예외가 층을 넘나드는 자리

## 출처

- [[2024-06-13-Day14]] — 메인 메뉴 루프 안에서 서브메뉴 루프를 가진 메서드를 불러 계층을 만들고, `9` 로 `break` 해서 이전 층으로 돌아오며 프롬프트에 `메인/회원> ` 처럼 위치를 표시하는 것을 실습으로 배웠다
- [[2024-07-05-Day30]] — 같은 골격을 팀 토이 프로젝트에 쓰면서 **이 필기가 선택이라 여겼던 것들이 조건으로 바뀐 자리**다. 메인 화면이 메뉴와 함께 날짜·달성률·체크 표시를 띄우므로 회차마다 다시 그려야 하고, 「누적달성률 20%미만 시 프로그램 종료」로 **사용자 명령이 아닌 조건이 루프를 끝내며**, 「일과종료」 명령 하나가 도메인의 하루를 넘긴다. 메뉴를 「CURD」라 부른 것은 이름의 오적용이다(→ [[crud]])
- [[2024-07-08-Day30]] — 같은 골격이 **메서드에서 클래스로, 다시 부모 클래스로** 옮겨 간다. 서브메뉴 루프를 가진 `static` 메서드가 `UserCommand`·`ProjectCommand`·`BoardCommand` 의 `execute()` 가 되면서 층이 자기 데이터(`userList` 등)를 갖게 되고, 그 네 `execute()` 가 글자까지 같아 `AbstractCommand` 로 올라간다. 그 뒤 각 Command 에 남는 것은 「메뉴 목록」과 「번호를 받았을 때 할 일」뿐이다 — 여기 정리한 네 단계 중 **출력·입력·해석이 부모의 것이 되고 분기만 자식의 것**이 된다. 서브메뉴가 없는 「도움말」이 이 틀에 들어가지 못해 `App` 의 `switch` 안에 남은 것도 이 회차다
- [[2024-07-15-Day35]] — 같은 루프가 **상속 계층을 떠나 트리의 가지(`MenuGroup.execute()`)로 들어간다.** 네 단계와 특별 명령 표는 그대로이고 셋이 바뀐다 — 나가기 입력이 `9` 에서 **`0`** 으로 옮겨 항목 번호(1부터)와 구조적으로 안 겹치게 되고, 「이전」/「종료」가 `setExitMenuTitle` 로 **값**이 되어 뿌리와 가지가 한 클래스로 합쳐지고, 층에서 나오기가 `break` 에서 `return` 이 된다(루프가 메서드의 전부다). 「중간 층에서 프로그램 종료」는 여전히 못 하며 라벨만 위치에 맞게 붙일 수 있게 된 것이다. 이 회차에 드러나는 예외 처리 문제 둘이 있다 — `try` 가 `menu.execute()` 까지 감싸서 **트리 아래 어디서 난 `NumberFormatException` 도 「숫자로 메뉴 번호를 입력하세요」로 안내되고**(명령이 회원번호를 파싱하다 던진 것까지), 루프가 내려간 탓에 `App.execute()` 의 같은 `catch` 는 **도달할 수 없는 코드**가 되었다. 그리고 `Menu.execute()` 하나가 잎의 「한 번의 처리」와 가지의 「층 진입」을 겸하게 되어 Day14 의 이름 문제가 인터페이스 수준으로 올라간다
