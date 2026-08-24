---
type: concept
id: composite-pattern
title: 컴포짓 패턴 (Composite Pattern)
aliases:
  - 컴포짓 패턴
  - 컴포지트 패턴
  - composite pattern
  - Composite
  - 복합체 패턴
  - 부분-전체 계층
  - part-whole hierarchy
  - 트리 구조 패턴
up:
  - 2024-07-15-Day35
  - 2024-07-18-Day38
tags:
  - 설계
  - 디자인패턴
  - 객체지향
  - 자료구조
---

# 컴포짓 패턴 (Composite Pattern)

**「하나」와 「여럿을 담은 것」에 같은 타입을 주어, 부르는 쪽이 둘을 구별하지 않게 하는 것.** 필기의 한 줄이 정의 전부다 — 「객체들의 트리를 구성하여 부분-전체 계층 구조를 나타내는 패턴이다」. 담는 쪽이 담기는 것과 **같은 약속을 지키기 때문에** 트리의 깊이가 코드에서 사라진다.

## 정의

역할이 셋이고, 필기가 그 셋을 그대로 적었다.

| 역할 | 필기의 설명 | 이 실습에서 |
|---|---|---|
| **Component** | 「단일 객체와 복합 객체가 동일한 방식으로 처리될 수 있도록」 | `interface Menu { void execute(); String getTitle(); }` |
| **Leaf** | 「더이상 하위 요소를 가지지 않는 객체」 | `MenuItem` — 커맨드 하나를 부른다 |
| **Composite** | 「하위 요소들을 관리하고 해당 요소들에게 작업을 전달」 | `MenuGroup` — `List<Menu> children` |

이 구조를 성립시키는 한 줄은 `List<Menu> children` 이다. **담는 통의 원소 타입이 Component 이므로 Leaf 와 Composite 이 같은 통에 들어간다.**

```text
Menu (Component)
 ├── MenuItem   (Leaf)      execute() → command 실행하고 곧 돌아온다
 └── MenuGroup  (Composite) execute() → children 을 보여 주고 하나를 골라 execute()
                              └── children: List<Menu>   ← 다시 Component 다
```

`children` 이 `Menu` 를 담으므로 **재귀가 타입 검사 없이 성립한다** — `MenuGroup.execute()` 안의 `menu.execute()` 는 그것이 잎인지 가지인지 묻지 않는다 → [[polymorphism]] · [[interface]]

여기에 실제 구현은 한 겹이 더 있다. `AbstractMenu` 가 `Menu` 를 구현하면서 `execute()` 는 채우지 않고 **`title` 필드와 `getTitle()`·`equals`·`hashCode` 만** 갖는다. 두 자식이 공유하는 것이 「순서」가 아니라 **「상태」**이므로 골격을 물려주는 추상 클래스와 역할이 다르다 → [[abstract-class]] · [[template-method-pattern]]

## 사용 예시

Composite 쪽이 하는 일은 「목록을 보여 주고 하나를 골라 시킨다」다.

```java
public class MenuGroup extends AbstractMenu {
  private String exitMenuTitle = "이전";
  private MenuGroup parent;
  private Stack<String> menuPath;
  private List<Menu> children = new ArrayList<>();

  @Override
  public void execute() {
    menuPath.push(title);
    printMenus();
    while (true) {
      String command = Prompt.input("%s>", getMenuPathTitle(menuPath));
      if (command.equals("menu")) {
        printMenus();
        continue;
      } else if (command.equals("0")) { // 이전 메뉴 선택
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

        menu.execute();          // ← 잎인지 가지인지 묻지 않는다

      } catch (NumberFormatException ex) {
        System.out.println("숫자로 메뉴 번호를 입력하세요.");
      }
    }
  }

  private void printMenus() {
    System.out.printf("[%s]\n", title);
    int i = 1;
    for (Menu child : children) {
      System.out.printf("%d. %s\n", i++, child.getTitle());
    }
    System.out.printf("0. %s\n", exitMenuTitle);
  }
}
```

**`printMenus()` 가 `getTitle()` 만으로 화면을 만든다.** 그래서 `Menu` 인터페이스에 `execute()` 외에 `getTitle()` 이 필요했던 것이다 — 필기가 「메뉴들의 title을 불러올 규칙이 필요하다」로 적은 자리이고, **Component 의 메서드 목록은 「부르는 쪽이 구별하지 않으려면 무엇을 물어야 하나」로 정해진다.**

Leaf 쪽은 짧다.

```java
public class MenuItem extends AbstractMenu {
  Command command;

  @Override
  public void execute() {
    if (command != null) {
      command.execute(title);
    } else {
      System.out.println(title);
    }
  }
}
```

트리를 세우는 일은 `add` 한 곳에서 일어난다.

```java
public void add(Menu child) {
  if (child instanceof MenuGroup) {
    ((MenuGroup) child).setParent(this);
  }
  children.add(child);
}
```

그리고 `App` 의 생성자가 그 트리를 조립한다.

```java
MenuGroup mainMenu = new MenuGroup("메인");

MenuGroup userMenu = new MenuGroup("회원");
userMenu.add(new MenuItem("등록", userCommand));
userMenu.add(new MenuItem("목록", userCommand));
/* 조회·변경·삭제 */
mainMenu.add(userMenu);                            // 가지를 넣는다

mainMenu.add(new MenuItem("도움말", helpCommand));   // 잎을 나란히 넣는다
mainMenu.add(new MenuItem("명령내역", historyCommand));

mainMenu.setExitMenuTitle("종료");
```

**마지막 두 줄이 이 패턴의 값을 한눈에 보여 준다.** 「회원」은 서브메뉴를 가진 가지이고 「도움말」은 잎인데, `mainMenu` 는 둘을 **같은 `add` 로 같은 통에 넣는다.** 화면에도 나란히 찍히고 번호도 이어진다 — 「서브메뉴가 있는 메뉴」와 「없는 메뉴」를 두 종류로 다루던 일이 여기서 없어진다.

`App` 은 트리의 뿌리에게 한 번 시키고 끝난다.

```java
void execute() {
    try {
      mainMenu.execute();
    } catch (NumberFormatException ex) { /* 생략 */ }

    System.out.println("종료합니다.");
    Prompt.close();
  }
```

## 왜 중요한가

**깊이가 타입에서 사라진다.** 34일 앞선 회차는 두 층을 `String[][] subMenus` 로 표현했다 — **배열의 차원이 메뉴 깊이였으므로** 세 층은 `String[][][]` 이었다. 6일 앞선 회차는 `Map<String, Command>` 로 한 층을 만들고 각 Command 가 자기 메뉴 목록을 따로 들었다 — 층마다 다른 자료구조였다. `List<Menu>` 는 **한 층과 열 층이 같은 타입**이고, 층을 하나 더하는 일이 `new MenuGroup(...)` 한 줄이 된다 → [[multidimensional-array]] · [[dispatch-table]]

**「서브메뉴가 없는 메뉴」가 예외가 아니게 된다.** 7일 앞선 회차의 「도움말」은 루프를 물려받는 틀(`AbstractCommand`)에 넣을 것이 없어 `App` 의 `switch` 안에 남았고, 하루 뒤에는 `implements Command` 로만 붙었다. **틀에 안 맞는 것이 계속 한 개씩 있었던 셈**이고, 컴포짓은 그것을 예외가 아니라 **Leaf 라는 이름의 정식 역할**로 만든다. 「틀에 안 들어가는 것」이 「이 패턴의 절반」으로 바뀐 것이 이 회차의 이동이다 → [[template-method-pattern]]

**메뉴 구조가 코드에서 데이터로 내려온다.** 층·항목·순서가 전부 `children` 에 담긴 객체들이므로, 메뉴를 바꾸는 일이 **분기를 고치는 일에서 트리를 다르게 조립하는 일**로 바뀐다. 필기의 결론 세 줄이 그것을 「Menu그룹을 나눔으로써 메뉴의 기능과 커맨드의 기능을 분리 하였다」로 적었다.

**타입 검사를 없애는 것이 아니라 한 곳으로 모은다.** 이 코드에서 `instanceof` 가 남은 자리는 `add` 하나뿐이고, 순회하고 실행하는 코드에는 없다. **검사가 「트리를 세울 때」로 밀려나고 「트리를 쓸 때」에서 사라진 것**이 이 패턴이 실제로 사는 이득이다 → [[instanceof-operator]]

## 경계와 오해

- **객체의 트리 ≠ 클래스의 트리** — 이 코드에는 트리가 **둘** 있고 방향이 다르다. `MenuGroup`·`MenuItem` 이 `AbstractMenu` 를 상속하는 것은 **클래스 사이의 트리**이고 컴파일 시점에 고정된다. 컴포짓이 말하는 트리는 `children` 이 만드는 **인스턴스 사이의 트리**이고 실행 중에 조립된다. `extends` 로 트리를 그렸다고 컴포짓이 되지 않는다 — 필요한 것은 **자기와 같은 타입을 담는 필드**다 → [[inheritance]] · [[instance]]
- **투명성과 안전성 중 하나를 골라야 한다 — 이 코드는 안전성을 골랐다** — `add`·`remove`·`getMenu`·`countMenu` 를 `Menu` 인터페이스가 아니라 `MenuGroup` 에만 두었다. 그래서 `MenuItem.add(...)` 라는 말이 안 되는 호출이 애초에 컴파일되지 않는다(안전). 대가는 **호출부가 가지와 잎을 구별해야 하는 자리가 하나 남는다**는 것이고 그게 `add` 안의 `instanceof` 다. 반대로 그 넷을 Component 에 올리면(투명) 호출부는 완전히 균일해지지만 잎이 「담을 수 없다」를 실행 중에 알려야 한다. **어느 쪽도 공짜가 아니고, 균일함을 어디까지 밀지가 이 패턴의 유일한 설계 결정이다** → [[interface-segregation-principle]]
- **필기가 「root menuGroup」과 「tree menuGroup」을 두 종류로 갈라 적었지만 클래스는 하나다** — 둘의 차이는 `parent` 가 `null` 인가뿐이고, 뿌리를 특별한 타입으로 만들지 않는 것이 바로 컴포짓이 하는 일이다. 두 종류로 읽으면 왜 `MenuGroup` 이 하나인지 설명되지 않고, **뿌리인지 가지인지를 정하는 것도 자기 자신이 아니라 「누가 나를 `add` 했는가」**다.
- **`menuPath` 공유가 `add` 순서에 걸린다 — 세 층을 만들면 그 자리에서 깨진다** — 생성자가 `this.menuPath = new Stack<>()` 로 자기 스택을 만들고, `setParent` 가 그것을 **부모의 스택으로 바꿔치운다.** `setParent` 는 `add` 될 때 한 번만 불리므로 **자식이 부모에게 붙는 시점에 부모가 이미 뿌리에 붙어 있어야** 스택 하나가 트리 전체에 퍼진다. `App` 의 조립 순서는 아래에서 위다.

  ```java
  MenuGroup sub = new MenuGroup("소분류");   // 자기 스택 S2
  userMenu.add(sub);                        // sub.menuPath = userMenu 의 S1
  mainMenu.add(userMenu);                   // userMenu.menuPath = S0  ← sub 은 여전히 S1
  ```

  실행하면 「메인」과 「회원」은 `S0` 에 쌓이고 「소분류」는 `S1` 에 쌓인다. 프롬프트가 `메인/회원/소분류>` 가 아니라 **`소분류>`** 로 나온다. 예외도 오류도 없고 **빵 부스러기 경로만 조용히 조상을 잃는다.** 두 줄의 순서를 바꾸면(부모를 먼저 붙이고 자식을 나중에) 정상 동작하며, **어느 쪽도 컴파일러가 보지 못한다.** 필기가 「tree는 parent가 필요하여 부모의 parent와 menuPath를 가져오는 메서드가 필요하다」로 세 층을 명시적으로 계획해 두었는데 이 코드는 두 층까지만 맞는다 — 참조를 물려주는 방식이 아니라 **쓸 때 부모를 타고 올라가 뿌리의 스택을 찾는 방식**이었다면 순서와 무관해진다 → [[stack]] · [[object-reference]]

  **Day38 이 정확히 그 방식으로 고친다.** `menuPath` 필드와 생성자의 `new Stack<>()` 이 사라지고 `setParent` 는 `this.parent = parent;` 한 줄만 남으며, 경로는 `getMenuPath()` 가 `this` 에서 `parent` 를 타고 올라가 그때그때 만든다. 필기가 적은 문제는 스택 하나가 낭비된다는 쪽이었지만(「인스턴스된 Stack은 Garbage가 된다」) **같은 변경이 조립 순서 의존까지 함께 없앤다** — 물려받을 참조가 없으므로 언제 붙었는지가 상관없어진다. 세 층이 이제 실제로 동작한다 → [[stack]] · [[refactoring]]
- **`remove` 는 `add` 의 반대가 아니다** — `add` 는 `children` 에 넣고 **부모를 세우는 두 가지 일**을 하는데, `remove` 는 `children.remove(child)` 만 한다. 떼어낸 `MenuGroup` 은 여전히 옛 부모를 `parent` 로 들고 옛 부모의 `menuPath` 를 공유한다. 그 상태로 다른 곳에 다시 붙이면 `setParent` 가 덮어 주니 살아나지만, **붙이지 않고 버리면 트리에서 빠진 노드가 트리를 붙들고 있는다** → [[garbage-collection]] · [[defensive-copy]]

  **Day38 이후에도 이 항목은 남는다 — 다만 남은 것이 하나로 줄었다.** 스택 공유가 사라졌으므로 「옛 부모의 `menuPath` 를 공유한다」는 없어지지만 `parent` 참조는 그대로 남고, 이제 그 필드가 **실제로 읽히므로** 떼어낸 노드의 경로가 옛 조상을 그대로 말한다. **문제의 절반이 없어진 대신 남은 절반은 증상이 눈에 보이는 쪽으로 옮겨 갔다** → [[object-reference]]
- **설계한 연산의 절반이 안 쓰인다 — `parent` 는 3일 뒤에 처음 읽힌다** — 필기는 「addMenu()·removeMenu()·getMenu()·countMenu()가 필요하다」로 넷을 적었고 구현은 `add`·`remove`·`getMenu`·`countMenu` 로 이름이 갈렸다. 실제로 프로그램이 부르는 것은 `add` 와 `getMenu` 둘뿐이다. **Day35 시점의 `parent` 필드는 `setParent` 가 저장만 하고 읽는 코드가 없다** — 「부모로 돌아가기」는 `return` 이 하고 있으므로(호출 스택) 필드가 할 일이 없었다. **Day38 에서 그 필드가 쓰인다** — `getMenuPath()` 의 `menuGroup = menuGroup.parent` 가 사슬을 거슬러 올라가고, `while (menuGroup != null)` 의 종료 조건이 「뿌리의 `parent` 는 `null`」이라는 성질을 그대로 쓴다. **트리를 아래로 내려가는 링크(`children`)만 쓰던 코드가 위로 올라가는 링크를 처음 쓰는 자리**이고, 두 방향 링크를 다 갖는 것이 그때 비용을 회수한다. 나머지(`countMenu`·`remove`)는 여전히 안 쓰인다 → [[jvm-stack]] · [[method]]
- **`execute()` 하나가 두 가지 수명을 덮는다** — `MenuItem.execute()` 는 커맨드 하나를 실행하고 곧 돌아오지만 `MenuGroup.execute()` 는 사용자가 `0` 을 누를 때까지 **돌아오지 않는다.** 균일하게 부를 수 있게 된 대가로 **호출부가 「이게 금방 끝나는 일인지 층에 들어가는 일인지」를 알 수 없게 됐다.** Day14 에서 「루프가 있는 메서드의 이름이 한 번의 처리처럼 읽힌다」로 걸렸던 것이 이제 **인터페이스 수준으로 올라간 것**이고, 이름을 바꿔서 해결할 수 없는 자리다 → [[command-loop]] · [[method]]
- **같은 일을 하는 방법이 둘이 되었다** — `MenuItem` 에는 `command` 없이 제목만 받는 생성자가 있고 `execute()` 는 `command == null` 이면 제목을 찍는다. 그러면 「아무 동작 없는 메뉴」를 만드는 길이 **커맨드 없는 `MenuItem`** 과 **아무것도 안 하는 `Command` 구현** 두 가지가 된다. 실제 `App` 은 모든 항목에 커맨드를 주므로 그 생성자와 `else` 가지는 쓰이지 않는다 → [[constructor]]
- **트리는 데이터가 되었지만 트리를 만드는 코드는 그대로 `App` 에 있다** — 층·항목·순서가 객체가 되었으므로 **파일이나 설정에서 읽어 조립할 수 있게 된 것**이 이 구조가 연 문이다. 이 회차는 그것을 쓰지 않고 생성자 안에 스물몇 줄로 박아 두었다. 「데이터로 내려왔다」와 「밖에서 온다」는 다른 단계이고, 6일 전 회차의 표에서도 등록 코드가 생성자에 남아 있던 것과 같은 자리다 → [[dispatch-table]] · [[open-closed-principle]]
- **깊이가 열렸으므로 재귀 종료를 자료구조가 보장한다** — `execute()` 가 자식의 `execute()` 를 부르므로 호출이 층만큼 쌓인다. 끝나는 이유는 **잎에 도달하면 더 부르지 않는다**는 것뿐이고, 사이클이 없다는 보장은 자료구조에 없다. `groupA.add(groupB); groupB.add(groupA);` 는 컴파일되고 실행되며 사용자가 계속 들어가면 스택이 자란다 — **트리라고 부르는 것은 약속이지 강제가 아니다** → [[recursion]] · [[jvm-stack]]

## 함께 보는 개념

- [[interface]] — Component 를 담는 약속
- [[polymorphism]] — 잎과 가지를 구별하지 않게 만드는 성질
- [[abstract-class]] — 두 자식이 상태를 공유하는 자리
- [[command-pattern]] — 잎이 실행하는 것
- [[command-loop]] — Composite 안으로 들어간 루프
- [[dispatch-table]] — 이 구조가 대체한 앞 단계
- [[template-method-pattern]] — 이 회차에 해체된 앞 구조
- [[stack]] — 트리의 현재 위치를 값으로 들고 있는 협력자
- [[instanceof-operator]] — 트리를 세울 때 한 번 남은 검사
- [[recursion]] — 깊이가 열린 뒤의 호출 모양
- [[object-equality]] — 트리에서 노드를 찾고 지우는 판정
- [[interface-segregation-principle]] — 투명성과 안전성을 재는 원칙
- [[multidimensional-array]] — 깊이를 타입으로 표현하던 앞 방법
- [[open-closed-principle]] — 트리 조립이 코드에 남은 것을 재는 원칙
- [[refactoring]] — 3일 뒤 경로 계산을 고친 변경의 성격

## 출처

- [[2024-07-15-Day35]] — 「객체들의 트리를 구성하여 부분-전체 계층 구조를 나타내는 패턴」이라는 정의와 Component·Leaf·Composite 세 역할을 배우고, 실습 프로젝트의 메뉴를 `interface Menu`(`execute()`·`getTitle()`) → `AbstractMenu`(title·equals·hashCode) → `MenuGroup`(`List<Menu> children`) · `MenuItem`(`Command`) 로 다시 세웠다. `mainMenu.add(userMenu)` 와 `mainMenu.add(new MenuItem("도움말", helpCommand))` 가 나란히 놓이면서 **「서브메뉴 없는 메뉴」가 예외에서 Leaf 로 승격**되고, 메뉴 깊이가 `String[][]`·`Map` 같은 타입에서 빠져나와 `children` 이라는 데이터가 된다. `add`·`remove`·`getMenu`·`countMenu` 를 `MenuGroup` 에만 두어 안전성을 골랐고 그 대가로 `add` 안에 `instanceof MenuGroup` 이 하나 남았으며, `remove` 가 `parent` 를 되돌리지 않고 `parent` 필드는 저장만 되며 `countMenu`·`remove` 는 호출되지 않는다. **`setParent` 가 부모의 `menuPath` 참조를 복사하는 방식이라 세 층에서는 조립 순서에 따라 경로가 조용히 끊긴다**
- [[2024-07-18-Day38]] — 같은 트리에서 **경로를 들고 다니는 방식만 바꾼다.** `MenuGroup` 의 `menuPath` 필드와 생성자의 `new Stack<>()` 이 사라지고 `setParent` 가 `this.parent = parent;` 한 줄로 줄며, `getMenuPath()` 가 `while (menuGroup != null) { menuPath.push(menuGroup.title); menuGroup = menuGroup.parent; }` 로 사슬을 거슬러 올라가 그때그때 경로를 만든다. **Day35 에 저장만 되고 읽히지 않던 `parent` 필드가 여기서 처음 쓰이고**, 조립 순서에 따라 세 층에서 경로가 끊기던 문제가 함께 사라진다. 필기가 적은 이유는 「인스턴스된 Stack은 Garbage가 된다」쪽이었지 순서 의존 쪽이 아니었다 — **낭비를 고친 변경이 버그도 고쳤고, 필기는 그 사실을 모른다.** `add`·`getMenu` 외의 연산(`remove`·`countMenu`)은 이 회차에도 쓰이지 않는다
