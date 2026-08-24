---
type: concept
id: template-method-pattern
title: 템플릿 메서드 패턴 (Template Method Pattern)
aliases:
  - 템플릿 메서드 패턴
  - 템플릿 메소드 패턴
  - 템플릿 메서드
  - template method
  - template method pattern
  - 훅 메서드
  - hook method
up:
  - 2024-07-08-Day30
  - 2024-07-09-Day31
  - 2024-07-10-Day32
  - 2024-07-15-Day35
  - 2024-10-14-Day92
tags:
  - 설계
  - 객체지향
  - 디자인패턴
  - 상속
---

# 템플릿 메서드 패턴 (Template Method Pattern)

**일의 순서는 부모가 갖고, 그 순서 안에서 달라지는 단계만 자식이 채우는 구조.** 부모의 메서드가 자식의 메서드를 부르므로 **호출 방향이 위에서 아래로** 간다 — 자식이 부모 코드를 쓰는 보통의 상속과 반대다.

## 정의

부모가 가진 메서드가 두 종류로 갈린다.

| 종류 | 누가 쓰나 | 이 코드에서 |
|---|---|---|
| **템플릿 메서드** — 순서를 담은 완성된 메서드 | 부모가 소유하고 자식은 건드리지 않는다 | `execute()` |
| **추상 메서드(훅)** — 순서 안의 빈 칸 | 부모가 부르고 자식이 채운다 | `processMenu(String)` · `getMenus()` |

필기의 두 줄이 이 갈림이다 — 「수퍼클래스에서 결정되지 못하는 메소드는 추상메소드로 만든다 / 자식클래스에서 추상메소드에 방법을 제시해야한다」. **「결정되지 못한다」는 것이 「비어 있다」가 아니라 「부모가 이 자리에서 무엇을 부를지는 정했고 무엇이 실행될지는 모른다」**는 뜻이다.

그래서 부모는 **자기가 갖지 않은 코드를 전제로 코드를 쓸 수 있다.**

```text
App        →  command.execute()        // 부모의 템플릿 메서드
AbstractCommand.execute()
           →  getMenus()               // 자식이 채운 칸
           →  processMenu(menuName)    // 자식이 채운 칸
```

## 사용 예시

일반화 전의 `UserCommand.execute()` 가 나중에 부모로 올라가는 골격 전체다. **다른 Command 와 다른 것은 두 군데뿐이다.**

```java
@Override
public void execute() {
  printMenus();                                   // menus 를 읽어 찍는다
  while (true) {
    String command = Prompt.input(String.format("메인/%s>", menuTitle));
    if (command.equals("menu")) { printMenus(); continue; }
    else if (command.equals("9")) { break; }
    try {
      int menuNo = Integer.parseInt(command);
      String menuName = getMenuTitle(menuNo);      // menus 의 길이로 검증한다
      if (menuName == null) { System.out.println("유효한 메뉴 번호가 아닙니다."); continue; }
      processMenu(menuName);                       // ← 여기만 Command 마다 다르다
    } catch (NumberFormatException ex) {
      System.out.println("숫자로 메뉴 번호를 입력하세요.");
    }
  }
}
```

일반화 후 자식에는 **채운 칸 두 개만** 남는다.

```java
public class UserCommand extends AbstractCommand {
  @Override
  public void processMenu(String menuName) {       // 부모가 부른다
    switch (menuName) {
      case "등록": this.addUser(); break;
      ...
    }
  }

  @Override
  public String[] getMenus() {                     // 부모가 부른다
    return menus;
  }
}
```

**`AbstractCommand` 의 몸통은 필기에 없다.** 그래도 그 안의 모양은 정해져 있다 — `execute()` 가 자식에서 사라졌고 `getMenus()` 가 추상 메서드로 새로 생겼으므로, **부모의 `execute()` 가 `getMenus()` 를 불러 메뉴를 찍고 번호를 검증한다**고 보지 않으면 `getMenus()` 를 만든 이유가 없다. 일반화 전 `printMenus`·`isValidateMenu`·`getMenuTitle` 이 읽던 `menus` 필드가 부모에는 없으니, 그 세 메서드가 위로 올라가려면 **필드를 읽던 자리를 메서드 호출로 바꿀 수밖에** 없었다.

`menuTitle` 은 그 반대 선택이다. 값이 자식마다 다른데 `super(menuTitle)` 로 **부모에게 주고** 끝냈다 — 추상 메서드로 물어보지 않았다.

| 자식마다 다른 것 | 부모가 얻는 방법 | 자식에 남는 것 |
|---|---|---|
| 메뉴 제목 | 생성자 인자 `super(menuTitle)` | 없어야 한다 |
| 메뉴 목록 | 추상 메서드 `getMenus()` | 필드 + 메서드 |
| 메뉴 처리 | 추상 메서드 `processMenu()` | 메서드 |

**두 가지 방법이 한 클래스 안에 나란히 있고, 필기는 왜 갈랐는지 적지 않았다.**

### 7일 뒤, 이 골격이 해체된다

Day35 의 필기가 한 줄로 그것을 적는다 — 「커맨드의 추상클래스의 역할은 menu에서 수행 하므로 더이상 추상클래스가 필요없다」. `AbstractCommand` 가 **삭제된다.**

골격이 없어진 것은 아니다. **사는 곳이 부모 클래스에서 옆 객체로 옮겼다.**

| | Day30~32 | Day35 |
|---|---|---|
| 골격을 가진 것 | `AbstractCommand.execute()` | `MenuGroup.execute()` |
| 골격과 갈래를 잇는 축 | **상속** — 부모가 `this.processMenu()` | **조합** — 노드가 `child.execute()` |
| 갈래를 채우는 것 | 자식 클래스의 재정의 | 트리에 매달린 다른 객체 |
| 갈래를 정하는 시점 | 컴파일 시점(클래스를 쓸 때) | 실행 시점(트리를 조립할 때) |

```java
// MenuGroup.execute() — 골격은 그대로 남았다
menuPath.push(title);
printMenus();
while (true) {
  String command = Prompt.input("%s>", getMenuPathTitle(menuPath));
  /* menu · 0 처리 */
  try {
    int menuNo = Integer.parseInt(command);
    Menu menu = getMenu(menuNo - 1);
    if (menu == null) { /* 안내 */ continue; }
    menu.execute();                    // ← 자식 클래스가 아니라 자식 노드다
  } catch (NumberFormatException ex) { /* 안내 */ }
}
```

**Day30 에 정리한 네 단계(출력·입력·해석·분기) 중 셋이 여전히 한 곳에 있고 분기만 밖에서 온다** — 달라진 것은 그 「밖」이 상속 계층 아래가 아니라 **필드에 담긴 객체**라는 것뿐이다 → [[composite-pattern]]

그리고 `AbstractMenu` 는 이 패턴의 자리를 잇지 **않는다.**

```java
public abstract class AbstractMenu implements Menu {
  protected String title;
  /* 생성자 · equals · hashCode · getTitle */
}
```

`execute()` 를 채우지 않고 추상으로 남기지만 **자식의 무엇도 부르지 않는다.** 물려주는 것이 「순서」가 아니라 `title` 이라는 **상태**이므로, 이 노트가 Day30 에 갈라 둔 두 종류의 추상 클래스 중 `AbstractList` 쪽이다. **추상 클래스가 있다는 것과 템플릿 메서드가 있다는 것이 같지 않다**는 것을 한 회차 안에서 두 클래스로 볼 수 있는 자리다 → [[abstract-class]]

## 왜 중요한가

**「순서」가 재사용 대상이 된다.** 상속으로 물려받는 것이 보통 「기능」인데 여기서 물려받는 것은 **입력을 받고 검증하고 갈래로 보내는 절차**다. 새 메뉴를 하나 더하는 사람은 루프도, `menu` 명령도, `NumberFormatException` 처리도 다시 쓰지 않고 `processMenu` 만 쓴다 → [[command-loop]]

**자식이 순서를 어길 수 없다.** 「숫자 검증을 먼저 하고 그 다음에 처리한다」가 부모 코드 안에 있으므로, 자식이 검증을 빼먹는 방법이 없다. 약속을 인터페이스로만 두면 각 구현이 순서를 스스로 지켜야 하고 **한 곳이 빠뜨려도 컴파일러가 모른다** — 순서를 코드로 못 박는 것은 인터페이스가 할 수 없는 일이다 → [[interface]]

**그리고 이것이 `Command` 인터페이스만으로 안 되는 이유다.** `interface Command { void execute(); }` 에는 몸통을 둘 수 없으니 골격을 담을 곳이 없다. 필기가 인터페이스를 만든 다음 다시 추상 클래스를 만든 것이 그 결과이고, **약속만 있는 곳과 코드가 있는 곳을 둘 다 쓴 것**이다 → [[abstract-class]] · [[interface]]

## 경계와 오해

- **템플릿 메서드 패턴 ≠ 공통 코드를 부모에 올린 것** — 갈리는 것은 **호출 방향**이다. Day30 앞 절의 `AbstractList` 는 `size()` 를 부모에 두었지만 그 메서드는 자식의 무엇도 부르지 않는다 — 자식이 부모 코드를 쓰는 쪽이다. `AbstractCommand.execute()` 는 반대로 **부모가 자식을 부른다.** 한 노트에 두 종류의 추상 클래스가 나란히 있고, 「공통을 올렸다」로만 읽으면 둘이 같은 것으로 보인다 → [[generalization]]

  **그리고 이틀 뒤(Day32) 그 `AbstractList` 도 부르는 쪽으로 넘어간다.** 반복자를 내주는 구현이 부모에 놓이면서다.

  ```java
  public abstract class AbstractList implements List {
    @Override
    public Iterator iterator() {
      return new ListIterator(this);        // 부모가 만든다
    }
  }
  ```

  ```java
  public Object next() { return list.get(cursor++); }   // 자식이 채운 것을 부른다
  ```

  `get(int)` 과 `size()` 는 `ArrayList`·`LinkedList` 가 각자 구현한 것이므로, **부모가 만든 객체가 자식의 코드를 부른다.** 「이 자리에서 무엇을 부를지는 정했고 무엇이 실행될지는 모른다」가 그대로 성립한다 — 이 노트가 Day30 시점에 「자식의 무엇도 부르지 않는다」로 적어 둔 클래스가 이틀 만에 반대편으로 옮겨 간 것이다 → [[iterator-pattern]] · [[abstract-class]]
- **훅이 부모의 메서드에서 불릴 필요는 없다 — 부모가 만든 다른 객체가 부를 수도 있다** — `AbstractCommand` 는 `execute()` 안에서 직접 `processMenu()` 를 불렀지만, `AbstractList` 는 **반복자를 만들어 돌려주고 그 반복자가 나중에** 자식의 `get`·`size` 를 부른다. 호출 방향은 같은데 **호출 시점이 부모의 메서드가 끝난 뒤**로 미뤄진다. 그래서 훅이 불릴 수 없는 시점(생성자 중)을 피하는 문제가 사라지는 대신, **반복자가 만들어진 뒤 컬렉션이 바뀌면 어긋나는** 새 문제가 생긴다 → [[iterator-pattern]] · [[constructor]]
- **골격이 고정된 것은 관습일 뿐 문법이 아니다** — `execute()` 가 `public` 이고 `final` 이 아니므로 자식이 재정의해 순서를 통째로 뒤집을 수 있고, 그러면 검증 없이 처리하는 Command 가 하나 생겨도 컴파일된다. **「자식이 채우는 자리」는 `abstract` 로 강제되는데 「자식이 건드리면 안 되는 자리」는 아무도 막지 않는다** — 막으려면 `final` 이 필요하다 → [[method-overriding]]
- **훅이 값을 돌려주는 것과 일을 하는 것은 다르다** — `getMenus()` 는 부모가 **읽으려고** 부르고 `processMenu()` 는 **시키려고** 부른다. 앞쪽은 자식마다 값이 다를 뿐이므로 생성자 인자로 대체할 수 있고(`menuTitle` 이 실제로 그렇게 되어 있다), 뒤쪽은 동작이 다르므로 대체할 수 없다. **추상 메서드가 필요한 것은 동작이 갈릴 때**이고, 값을 물어보는 훅은 자식에 필드와 메서드를 하나씩 남기는 대가를 치른다 → [[generalization]]
- **`HelpCommand` 는 이 틀 밖에 있다 — 그리고 그것이 옳았다** — Day30 의 필기는 「help커맨드는 인터페이스를 사용하여 직접구현」이라 적었지만 코드에는 `implements Command` 도 `extends AbstractCommand` 도 없었다. 메서드 이름만 `execute()` 로 같았고, `App.processMenu` 가 `case "도움말"` 안에서 직접 출력하므로 **그 시점에는 아무도 쓰지 않는 클래스**였다(같은 문장이 두 곳에 띄어쓰기만 다르게 존재했다 — `"도움말입니다."` / `"도움말 입니다."`).

  **하루 뒤 Day31 이 그것을 매달지 않고 붙인다.**

  ```java
  public class HelpCommand implements Command {
    public void execute(Stack menuPath) {
        System.out.println("도움말입니다!");
    }
  }
  ```

  `extends AbstractCommand` 가 아니라 `implements Command` 다. 그리고 `commandMap.put("도움말", new HelpCommand())` 로 실제로 불리게 되었다. **「메뉴가 서브메뉴를 갖지 않으면 이 패턴에 들어갈 것이 없다」는 진짜 문제의 답이 「약속만 지키고 골격은 안 물려받는다」**였던 것이고, 그것이 인터페이스와 추상 클래스를 겹쳐 쓴 값이다 — 순서를 물려받을 필요가 없는 구현은 골격을 건너뛰고 약속에만 붙는다 → [[interface]] · [[dispatch-table]]

  **그리고 Day35 에서 그 「예외」가 이름을 얻는다.** 컴포짓의 Leaf 가 정확히 「하위 요소를 갖지 않는 것」이므로, `mainMenu.add(new MenuItem("도움말", helpCommand))` 는 **틀을 비켜 간 것이 아니라 틀의 절반**이다. Day30 에 「이 틀에 들어가지 못하는 것이 하나 있다」로 남았던 자리가 두 회차를 거쳐 **「그 하나가 실은 두 종류 중 하나였다」**로 정리된 것이고, 특수 사례가 계속 하나씩 남는 것은 대개 **역할을 하나 덜 세었다는 신호**다 → [[composite-pattern]]
- **제어의 역전 ≠ 다형성** — 다형성은 **부르는 쪽이 실제 타입을 모르는 것**이고, 이 패턴은 **부모가 자기 자식을 부르는 것**이다. `AbstractCommand.execute()` 안의 `processMenu()` 는 `this.processMenu()` 이므로 다형성으로 자식 구현이 실행되지만, 패턴이 말하는 것은 그 문법이 아니라 **순서의 소유권이 부모에 있다**는 배치다 → [[polymorphism]]
- **부모가 자식을 부르는 것은 생성 시점과 얽힌다** — 자식의 필드 초기화(`String[] menus = {...}`)는 `super(...)` 가 끝난 **뒤에** 일어난다. 그래서 만약 `AbstractCommand` 의 생성자가 `getMenus()` 를 불렀다면 `null` 을 받는다. 이 코드는 `execute()` 를 나중에 부르므로 무사하지만, **부모에서 훅을 부를 수 있는 시점과 부를 수 없는 시점이 있다** — 상속의 초기화 순서를 모르면 원인을 찾기 어려운 종류의 `null` 이다 → [[constructor]] · [[inheritance]]
- **추상 메서드가 하나뿐이면 이 패턴이 아니라 전략에 가깝다 — 7일 뒤 실제로 그쪽으로 간다** — 갈리는 단계가 하나뿐이면 그 단계를 **따로 객체로 떼어 넘기는 편**이 상속보다 유연하다(자식이 늘 때 클래스가 늘지 않는다). Day31 의 코드는 갈리는 자리가 둘이고 둘 다 부모의 루프 중간에서 불리므로 상속이 맞았지만, **「추상 메서드를 뒀으니 템플릿 메서드」는 아니다.** **Day35 가 그 갈림을 하나로 줄이고 곧바로 객체로 떼어 낸다** — `getMenus()` 가 할 일은 `children` 목록이 가져가고, 남은 하나(`processMenu`)는 `MenuItem` 이 든 `Command` 가 된다. 상속으로 채우던 칸이 **생성자로 넘기는 인자**가 되었으므로 `new MenuItem("등록", new UserAddCommand(userList))` 처럼 **같은 잎 클래스에 다른 갈래를 끼울 수 있다.** 「추상 메서드 하나면 전략」이라는 판단이 회차 하나 뒤에 코드로 확인된 셈이다 → [[interface]] · [[command-pattern]] · [[dependency-injection]]
- **골격에 인자가 늘면 자식과 형제 전부가 같이 바뀐다 — 세 회차에 걸쳐 세 번 바뀐다** — `execute()` → `execute(Stack menuPath)`(Day31) → `execute(String menuName)`(Day35). **세 번 모두 골격이 필요해서 바꿨고 세 번 모두 구현 전부를 고쳐야 했다.** 마지막 것은 특히 허무하게 끝난다 — Day35 뒷부분에서 커맨드를 기능 단위로 쪼개면 갈래를 고를 필요가 없어져 **그 인자를 읽는 구현이 하나도 남지 않는다.** 골격이 요구한 인자가 골격이 사라진 뒤에도 약속에 남아 있는 것이고, 「지금 골격에 필요한 것」을 인터페이스에 적으면 **골격의 수명보다 그 흔적이 오래 산다** → [[command-pattern]]

  Day31 의 경우를 자세히 보면 이렇다. 메뉴 경로를 추적하려고 `execute()` 를 `execute(Stack menuPath)` 로 바꾼다. 인자를 실제로 쓰는 것은 부모의 골격뿐인데(`menuPath.push(menuTitle)` · `menuPath.pop()`), 시그니처는 `Command` 인터페이스에 있으므로 **`HelpCommand`·`HistoryCommand` 처럼 골격을 안 쓰는 구현까지 그 인자를 받는다.** 골격이 필요한 것을 인자로 받으면 그 요구가 **약속을 통해 형제들에게 번진다** — 이 자리에서는 `App` 이 스택을 만들어 넘기는 대신 `AbstractCommand` 가 스택을 필드로 들고 있었다면 시그니처를 안 건드릴 수 있었다 → [[interface-segregation-principle]] · [[stack]]
- **골격이 자식의 메서드가 아닌 것도 부른다** — Day31 의 `AbstractCommand.execute` 는 `Prompt.input(...)` 과 `menuPath.push/pop` 을 부른다. 추상 메서드로 물어보는 것(자식이 채우는 칸)과 **부모가 직접 아는 협력자**가 한 메서드에 섞여 있고, 그래서 「부모가 무엇에 의존하나」가 추상 메서드 목록에 다 나오지 않는다 → [[static-member]] · [[coupling]]
- **패턴 이름이 필기에 없다** — 필기는 이 구조를 「상속의 Generalization 적용」으로만 부른다. 이름 없이 만들어졌고 실제로 동작하지만, **이름이 없으면 「부모의 `execute()` 를 자식이 재정의해도 되나」 같은 물음이 판단으로 남는다.** 패턴 이름은 구조에 딸린 규칙(골격은 `final`, 훅만 열린다)을 같이 데려온다 → [[singleton-pattern]]

## 함께 보는 개념

- [[generalization]] — 이 구조가 만들어지는 이동
- [[abstract-class]] — 골격과 빈 칸을 함께 담는 그릇
- [[method-overriding]] — 자식이 빈 칸을 채우는 문법
- [[inheritance]] — 부모/자식 관계의 문법
- [[command-loop]] — 여기서 부모가 소유하게 된 순서의 내용
- [[interface]] — 순서를 담을 수 없는 쪽
- [[polymorphism]] — 훅 호출이 자식 구현에 닿게 만드는 성질
- [[constructor]] — 훅을 부를 수 없는 시점이 생기는 이유
- [[singleton-pattern]] — 이름 붙은 구조가 규칙을 데려오는 다른 예
- [[dispatch-table]] — 이 골격을 가진 객체들을 한 통에 담는 구조
- [[interface-segregation-principle]] — 골격의 인자가 형제들에게 번지는 것을 재는 원칙
- [[stack]] — 골격이 새로 받게 된 협력자
- [[iterator-pattern]] — 부모가 만든 객체가 자식을 부르는 변형
- [[servlet-container-initializer]] — 프레임워크가 이 형태로 설정을 받는 자리
- [[nested-class]] — 그 객체를 부모 안에 두는 방법
- [[composite-pattern]] — 골격이 상속에서 조합으로 옮겨 간 뒤의 구조
- [[command-pattern]] — 훅이 객체가 된 결과
- [[dependency-injection]] — 갈래를 생성자로 넘기게 되는 자리

## 출처

- [[2024-10-14-Day92]] — 석 달 뒤. **프레임워크가 이 패턴으로 설정을 받는다는 것이 드러난다.** `WebApplicationInitializer` 를 직접 구현하면 컨테이너 생성·서블릿 등록·매핑을 전부 우리가 쓰지만, `AbstractAnnotationConfigDispatcherServletInitializer` 를 상속하면 **순서와 절차는 부모가 갖고 우리는 `getRootConfigClasses()`·`getServletConfigClasses()`·`getServletMappings()` 세 값만 돌려준다.** 같은 노트가 「`onStartup()` 을 오버라이딩했으면 **원래의 메서드를 반드시 호출해줘야 한다**」고 두 번 적은 것도 이 패턴의 전형적인 함정이다 → [[servlet-container-initializer]] · [[method-overriding]]
- [[2024-07-08-Day30]] — 세 Command 의 `execute()` 를 `AbstractCommand` 로 올리고 `processMenu`·`getMenus` 를 추상 메서드로 남겨 이 구조를 만들었다. 필기는 패턴 이름을 쓰지 않고 「수퍼클래스에서 결정되지 못하는 메소드는 추상메소드로 만든다」로만 적었다. `AbstractCommand` 의 코드 자체는 노트에 없지만, 일반화 전 `execute()` 가 `menus` 필드를 세 메서드에서 읽고 있었고 그것이 부모로 올라가며 `getMenus()` 가 생겼다는 것에서 호출 방향이 드러난다. 값이 다른 `menuTitle` 은 추상 메서드가 아니라 `super(menuTitle)` 로 처리해 두 방법이 한 클래스에 나란히 있으며, `HelpCommand` 는 이 틀에 들어가지 못하고 `App` 의 `switch` 안에서 직접 출력되는 쪽으로 남았다
- [[2024-07-09-Day31]] — 이 구조가 하루 만에 두 가지로 검증된다. 하나 — 전날 틀 밖에 있던 `HelpCommand` 가 `extends AbstractCommand` 가 아니라 **`implements Command` 로** 들어와 `commandMap` 에 등록된다. 「서브메뉴가 없어 골격에 넣을 것이 없는 명령」의 답이 「약속만 지키고 골격은 안 물려받는다」였고, 인터페이스와 추상 클래스를 둘 다 둔 이유가 여기서 값을 낸다. 둘 — 메뉴 경로를 쌓기 위해 `execute()` 가 `execute(Stack menuPath)` 로 바뀌면서 부모의 골격이 `menuPath.push(menuTitle)` 로 시작하고 「9」에서 `menuPath.pop()` 으로 나가게 되었는데, **인자를 쓰지 않는 형제 구현들까지 시그니처가 번졌다.** 그리고 경로를 문자열로 조립하는 `getMenuTitle(Stack)` 이 `AbstractCommand` 와 `App` 두 곳에 복사되어, 골격을 부모로 올린 다음 날에 공통 부모가 없는 두 클래스 사이 중복이 새로 생겼다
- [[2024-07-10-Day32]] — **Day30 시점에 「자식의 무엇도 부르지 않는다」로 갈라 두었던 `AbstractList` 가 이 회차에 부르는 쪽으로 넘어간다.** 반복자를 내주는 `iterator()` 가 부모에 놓이고 그 반복자의 `next()` 가 `list.get(cursor++)` 로 자식 구현을 부르기 때문이다. 다만 훅이 부모의 메서드 안에서 불리지 않고 **부모가 만들어 돌려준 객체가 나중에** 부르는 형태라, 「생성자에서 훅을 부르면 `null` 을 받는다」 같은 시점 문제는 없어지고 대신 「반복자를 만든 뒤 컬렉션이 바뀌면 어긋난다」가 새로 생긴다. 그리고 이 회차는 `iterator()` 를 `AbstractList` **한 곳에만** 두어 자식이 자기 구조에 맞는 반복자를 줄 여지를 쓰지 않았다 — 연결 리스트에서 순회가 O(n²) 이 되는 것이 그 대가다
- [[2024-07-15-Day35]] — **`AbstractCommand` 가 삭제된다** — 「커맨드의 추상클래스의 역할은 menu에서 수행 하므로 더이상 추상클래스가 필요없다」. 골격 자체는 `MenuGroup.execute()` 로 살아남지만 갈래를 잇는 축이 **상속에서 조합으로** 바뀐다(`this.processMenu()` → `child.execute()`), 그래서 갈래가 정해지는 시점이 컴파일에서 트리 조립으로 내려온다. 이 노트가 Day31 시점에 「갈리는 단계가 하나뿐이면 객체로 떼어 넘기는 편이 유연하다」로 적어 둔 판단이 그대로 실행된 자리다 — `getMenus()` 는 `children` 이 흡수하고 `processMenu` 는 `MenuItem` 이 든 `Command` 가 된다. 같은 회차의 `AbstractMenu` 는 `execute()` 를 추상으로 남기면서도 **자식의 무엇도 부르지 않고 `title` 이라는 상태만 물려주므로 이 패턴이 아니다** — 추상 클래스와 템플릿 메서드가 같지 않다는 것을 한 노트 안의 두 클래스로 볼 수 있다. Day30 부터 계속 틀 밖에 남던 「도움말」은 **Leaf 라는 정식 역할**을 얻고, 세 회차에 걸쳐 세 번 바뀐 `execute` 의 시그니처는 마지막에 **아무 구현도 읽지 않는 인자**로 남는다
