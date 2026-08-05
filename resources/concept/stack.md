---
type: concept
id: stack
title: 스택 (Stack)
aliases:
  - stack
  - 스택 자료구조
  - LIFO
  - 후입선출
  - Last In First Out
  - push
  - pop
up:
  - 2024-07-09-Day31
  - 2024-07-15-Day35
  - 2024-07-18-Day38
tags:
  - 자료구조
  - java
  - 알고리즘
  - 설계
---

# 스택 (Stack)

**한쪽 끝에서만 넣고 그 끝에서만 빼는 목록.** 필기의 한 줄이 정의 전부다 — 「스택은 LIFO(Last In, First Out) 구조를 따르며 마지막에 삽입된 요소가 가장 먼저 삭제되는 방식이다. 스택은 마치 한쪽 끝에서만 요소를 넣거나 뺄 수 있다」. **넣고 빼는 자리를 하나로 줄인 것이 이 구조가 하는 일의 전부**이고, 그 제약이 「가장 최근 것」을 공짜로 알려 준다.

## 정의

연산이 셋뿐이다. 자리를 고를 수 없으므로 인덱스를 받는 연산이 없다.

| 연산 | 하는 일 | 이 실습의 이름 |
|---|---|---|
| push | 끝에 하나 넣는다 | `push(Object)` |
| pop | 끝에서 하나 꺼내며 지운다 | `pop()` |
| 비었나 | 꺼낼 것이 있는지 | `isEmpty()` |
| (peek) | 끝을 **지우지 않고** 본다 | **없다** |

`peek` 이 없는 것은 결정이 아니라 빠뜨림에 가깝다 — 없으면 맨 위를 보려고 `pop` 한 뒤 다시 `push` 해야 하고, 그 사이에 값이 사라진 상태가 생긴다.

**어느 끝을 「위」로 삼는지는 구현이 고른다.** 이 실습은 **꼬리**를 위로 삼았다.

```java
public class Stack extends LinkedList {
    //push구현하기
    public void push(Object obj) {
        add(obj);                    // 꼬리에 붙인다
    }
    //pop구현하기
    public Object pop() {
        return remove(size() - 1);   // 꼬리를 뺀다
    }
    //empty구현하기
    public boolean isEmpty() {
        return size() == 0;
    }
}
```

**push·pop 이 열 줄이 아니라 두 줄이다** — 14일 앞선 회차에 만든 `LinkedList` 가 이미 「끝에 붙이기」와 「index 로 지우기」를 갖고 있으므로, 스택은 **어느 자리만 쓸지 정하는 껍데기**가 된다 → [[linked-list]]

## 사용 예시

이 회차의 실습이 스택으로 **메뉴 경로**를 만든다. 메뉴에 들어가면 쌓고 나오면 뺀다.

```java
public class App {
  Stack menuPath = new Stack();

  void execute() {
      menuPath.push("메인");
      /* 생략 */
  }

  void processMenu(String menuTitle) {
      /* 생략 */
      command.execute(menuPath);      // 같은 스택을 내려보낸다
  }
}
```

```java
public void execute(Stack menuPath) {
  menuPath.push(menuTitle);                    // 들어왔다
  printMenus();
  while (true) {
      String command = Prompt.input(...);
      if (command.equals("menu")) { printMenus(); continue; }
      else if (command.equals("9")) {           // 이전 메뉴 선택
          menuPath.pop();                       // 나간다
          break;
      }
      ...
  }
}
```

**메뉴 계층의 오르내림이 push/pop 과 정확히 짝이다.** 26일 앞선 회차에서 메뉴 층을 「중첩 `while` 이 아니라 메서드 호출」로 만들었으므로 **지금 어디 있는지가 호출 스택에만 있고 데이터로는 없었다.** 스택 하나가 그것을 값으로 꺼내 준다 → [[command-loop]] · [[jvm-stack]]

쌓인 것을 이어 붙이면 화면에 찍을 경로가 된다.

```java
private String getMenuTitle(Stack menuPath){
  StringBuilder strBuilder = new StringBuilder();
  for(int i = 0; i < menuPath.size(); i++){
      if (strBuilder.length() > 0){
          strBuilder.append("/");
      }
      strBuilder.append(menuPath.get(i));
  }
  return strBuilder.toString();
}
```

`메인` · `회원` 이 쌓여 있으면 `메인/회원` 이 나오고, 프롬프트가 `메인/회원>` 이 된다. 하루 전까지는 그 문자열이 `String.format("메인/%s>", menuTitle)` 로 **「메인」이 코드에 박혀 있었다** — 층이 세 개가 되면 못 쓰는 방식이었고, 스택이 그 자리를 데이터로 바꾼다 → [[string-builder]] · [[format-string]]

### 6일 뒤, 자작 스택을 버리고 표준을 쓴다

Day35 의 컴포짓 리팩터링에서 같은 `menuPath` 가 **`java.util.Stack<String>`** 이 된다. 자작 `Stack extends LinkedList` 는 사라지고, 경로를 들고 있는 자리도 `App` 에서 **트리의 가지**(`MenuGroup`)로 내려간다.

```java
public class MenuGroup extends AbstractMenu {
  private Stack<String> menuPath;                    // java.util.Stack

  public MenuGroup(String title) {
    super(title);
    this.menuPath = new Stack<>();
  }

  public void setParent(MenuGroup parent) {
    this.parent = parent;
    this.menuPath = parent.menuPath;                 // 부모의 스택을 그대로 쓴다
  }

  @Override
  public void execute() {
    menuPath.push(title);                            // 들어왔다
    printMenus();
    while (true) {
      String command = Prompt.input("%s>", getMenuPathTitle(menuPath));
      /* 생략 */
      } else if (command.equals("0")) {              // 이전 메뉴 선택
        menuPath.pop();                              // 나간다
        return;
      }
      /* 생략 */
    }
  }

  private String getMenuPathTitle(Stack<String> menuPath) {
    StringBuilder strBuilder = new StringBuilder();
    for (String s : menuPath) {                      // 인덱스가 사라졌다
      if (!strBuilder.isEmpty()) {
        strBuilder.append("/");
      }
      strBuilder.append(s);
    }
    return strBuilder.toString();
  }
}
```

세 가지가 바뀌었다. **하나 — 원소 타입이 정해졌다.** `Object` 대신 `String` 이므로 무엇이든 들어가는 문제가 없고 꺼낼 때 `toString()` 에 기대지 않는다. **둘 — 경로를 조립하는 메서드가 한 곳으로 줄었다.** Day31 에 `App` 과 `AbstractCommand` 두 곳에 복사돼 있던 것이 `MenuGroup` 하나에만 있다. **셋 — `for (String s : menuPath)` 로 돈다.** `get(i)` 인덱스 루프가 없어졌고, `strBuilder.length() > 0` 도 `!strBuilder.isEmpty()` 가 되었다 → [[for-loop]] · [[string-builder]]

그런데 **경로를 순회하는 순서가 왜 맞는지는 그대로 설명이 필요하다.** `java.util.Stack` 은 `Vector` 를 상속하고 그 반복자는 **넣은 순서**(아래 → 위)로 돈다. 즉 이 for-each 는 LIFO 순회가 **아니고**, 「메인」부터 나와야 하는 경로 출력에 맞는 것은 그 덕분이다. **스택을 스택 순서로 돌면 `회원/메인` 이 나온다** → [[iterator-pattern]]

### 3일 뒤, 경로를 저장하지 않고 계산한다 — 그리고 처음으로 진짜 스택이 된다

Day38 이 같은 `menuPath` 를 다시 손댄다. **이번에는 필기가 먼저 문제를 적었다** — 「menuGroup이 인스턴스 될 때마다 새로운 Stack을 생성한다」, 「부모의 menuGroup이 있다면 인스턴스된 Stack은 Garbage가 된다」, 「menuPath를 호출하는 메서드는 Stack의 구조로 꺼내는 것이 아니라 List타입으로 탐색을 한다」.

**세 번째 줄이 이 노트가 Day31 부터 두 회차에 걸쳐 지적해 온 「쓰기는 스택, 읽기는 목록」이다.** 필기가 그것을 스스로 찾아냈고, 해결 방법이 순회를 고치는 것이 아니라 **스택이 사는 자리를 바꾸는 것**이었다.

```java
  public MenuGroup(String title) {
    super(title);                 // menuPath 필드가 사라졌다
  }

  public void setParent(MenuGroup parent) {
    this.parent = parent;         // 부모의 스택을 물려받는 줄이 사라졌다
  }

  private String getMenuPath() {
    Stack<String> menuPath = new Stack<>();     // 부를 때마다 새로 만든다
    MenuGroup menuGroup = this;
    while (menuGroup != null) {
      menuPath.push(menuGroup.title);           // 나 → 부모 → 조부모 ... 순으로 쌓는다
      menuGroup = menuGroup.parent;
    }
    
    StringBuilder strBuilder = new StringBuilder();
    while (!menuPath.empty()) {
      if (!strBuilder.isEmpty()){
        strBuilder.append("/");
      }
      strBuilder.append(menuPath.pop());        // 꼭대기(= 뿌리)부터 나온다
    }
    return strBuilder.toString();
  }
```

**스택이 필드에서 지역 변수로 내려왔다.** 그 한 줄의 이동이 이 노트에 쌓여 있던 문제 셋을 동시에 없앤다.

| 이전 회차의 문제 | Day38 에서 |
|---|---|
| `setParent` 가 참조를 물려받아 조립 순서에 걸린다 | **참조를 물려받지 않는다** — 쓸 때 부모를 타고 올라간다 |
| `push`/`pop` 짝이 예외 경로에서 깨진다 | **한 메서드 안에서 쌓고 다 비운다** — 짝이 코드 모양으로 닫힌다 |
| 읽기가 `get(i)`·for-each 로 목록처럼 훑는다 | **`push` 와 `pop` 만 쓴다** |

그리고 순서가 맞는 이유가 처음으로 **스택의 성질 그 자체**가 된다. 「나」부터 쌓으면 꼭대기가 뿌리이므로, `pop` 이 뿌리부터 준다 — `메인/회원/소분류`. Day35 는 `Vector` 의 반복자가 아래에서 위로 돌아 주는 덕분에 맞았고, **Day38 은 LIFO 가 순서를 뒤집어 주는 덕분에 맞는다.** 같은 결과에 도달하는 근거가 반대편으로 옮겨 온 것이다 → [[refactoring]] · [[composite-pattern]]

## 왜 중요한가

**「되돌아갈 곳」을 기억하는 문제가 전부 이 모양이다.** 메뉴에서 나가기, 괄호 짝 맞추기, 실행 취소, 메서드 호출과 복귀 — 공통점은 **가장 최근에 들어간 것이 가장 먼저 끝난다**는 것이고, 그 순서가 곧 LIFO 다. 27일 앞선 회차에서 배운 JVM 스택이 같은 규칙으로 프레임을 쌓는다 → [[jvm-stack]] · [[recursion]]

**연산을 줄인 것이 이득이다.** 목록은 아무 자리나 만질 수 있어서 「어디를 만졌나」를 읽는 사람이 추적해야 한다. 스택은 만질 수 있는 자리가 하나뿐이라 **잘못 쓸 방법이 적고**, 코드를 읽을 때 확인할 것이 「짝이 맞나」로 줄어든다.

**자료구조를 고르는 것이 곧 규칙을 못 박는 일**이라는 것을 처음 겪는 자리다. `menuPath` 를 `String` 하나로 두고 이어 붙였다면 나갈 때 뒤에서 잘라야 하고, 그 자르는 코드는 매번 다시 맞아야 한다. 스택은 「마지막 것을 뺀다」를 **자료구조가 알고 있다.**

**그리고 스택을 얼마나 오래 들고 있는가가 별개의 결정이라는 것이 Day38 에서 드러난다.** Day31·Day35 는 스택을 **상태로** 들고 있었다 — 지금 어디 있는지가 그 안에 계속 남아 있으므로 들어갈 때와 나올 때 손으로 갱신해야 하고, 갱신을 놓친 상태가 존재할 수 있다. Day38 은 스택을 **계산 수단으로만** 쓴다 — 물어볼 때마다 부모 사슬을 타고 올라가 쌓았다 비우므로 **틀린 상태가 존재할 자리가 없다.** 「무엇을 자료구조로 표현하나」 다음에 오는 물음이 **「그것을 저장하나 계산하나」**이고, 뒤쪽을 고르면 갱신 코드와 그 코드의 버그가 함께 사라진다 → [[refactoring]] · [[caching]]

## 경계와 오해

- **스택 ≠ JVM 스택** — 27일 앞 회차의 스택 메모리는 이 자료구조를 **쓰는 곳**이고 자료구조 자체가 아니다. 그쪽은 메서드 프레임이 쌓이는 메모리 영역이라 내가 `push` 하지 않으며 크기를 넘기면 `StackOverflowError` 가 난다. 같은 낱말이 「규칙」과 「그 규칙으로 동작하는 메모리 영역」 둘을 가리킨다 → [[jvm-stack]]
- **`Stack extends LinkedList` 는 LIFO 를 강제하지 않는다** — 상속했으므로 `add`·`remove(int)`·`get(int)`·`indexOf`·`toArray` 가 전부 함께 열린다. `menuPath.remove(0)` 으로 맨 아래를 뽑아도 컴파일된다. **제약이 이 구조의 값 전부인데 그 제약이 사라진 것**이고, 자료구조를 「가진다」(필드로 목록을 두고 필요한 것만 공개)로 만들면 지킬 수 있었다. `java.util.Stack` 도 `Vector` 를 상속해 같은 문제를 갖고 있고 그것은 표준 라이브러리의 알려진 실수다 → [[inheritance]] · [[interface-segregation-principle]] · [[encapsulation]]
- **그런데 이 실습은 그 구멍을 **쓴다**** — `getMenuTitle` 이 `menuPath.get(i)` 로 아래에서 위로 훑는다. 스택 연산만으로는 안 되는 일이므로(다 `pop` 하면 스택이 비고, 다시 넣으려면 순서가 뒤집힌다) **경로를 찍는 기능이 스택의 제약을 넘어야 성립한다.** 즉 `menuPath` 는 **쓰기는 스택으로 읽기는 목록으로** 쓰이고 있고, 그렇다면 필요한 것은 스택이 아니라 「뒤에서만 넣고 빼는 목록」이다 — 필기가 「for문을 순회하면서 Stack의 배열을 탐색한다」로 적은 문장에 그 어긋남이 그대로 들어 있다 → [[linked-list]]

  **표준으로 갈아탄 Day35 도 이 구멍을 그대로 쓴다.** `for (String s : menuPath)` 는 `Vector` 에서 물려받은 반복자이고 순서도 아래에서 위다 — 인덱스가 안 보이게 됐을 뿐 **여전히 스택 연산이 아닌 것에 기대고 있다.** 자작 클래스의 설계 실수라고 읽으면 표준으로 바꿔서 해결됐다고 착각하게 되는데, `java.util.Stack` 이 `Vector` 를 상속한 것이 같은 실수이므로 **바뀐 것은 그 구멍이 누구 책임인가뿐**이다 → [[inheritance]]

  **Day38 에서 이 항목이 해소된다 — 그리고 해소한 방법이 순회를 고치는 것이 아니었다.** 필기가 「Stack의 구조로 꺼내는 것이 아니라 List타입으로 탐색을 한다」로 문제를 직접 적고, `menuPath` 를 필드에서 지역 변수로 내려 `push` 와 `pop` 만으로 경로를 만든다. **읽기가 목록에서 스택으로 온 것이 아니라, 「저장해 둔 것을 훑는 일」 자체가 「필요할 때 쌓았다 비우는 일」로 바뀌어서** 훑을 대상이 없어졌다. Day31·Day35 두 회차에 걸쳐 「제약이 이 구조의 값 전부인데 그 제약이 사라졌다」로 남아 있던 것이 **여기서 처음으로 스택 연산만 쓰는 코드가 된다** → 「사용 예시」의 Day38 절
- **꼬리를 위로 삼은 탓에 `pop` 이 O(n) 이 되었다** — 이 `LinkedList` 는 단일 연결이고 `last` 만 들고 있다. `add` 는 `last` 덕분에 O(1) 인데, `remove(size() - 1)` 은 **지울 노드의 앞까지 걸어가야** 하므로 원소 수에 비례한다. 머리를 위로 삼아 `push` 를 앞에 넣고 `pop` 을 `remove(0)` 으로 했다면 **둘 다 O(1)** 이었다. 같은 노트의 `Queue` 가 `poll()` 에 `remove(0)` 을 쓰고 있으므로 그 방법을 몰랐던 것도 아니다. 메뉴 경로는 깊이가 둘셋이라 체감되지 않지만, **어느 끝을 위로 삼는지가 성능 결정**이라는 것이 여기서 갈린다 → [[linked-list]]
- **자작 `pop()` 은 비어 있을 때 조용히 `null` 을 준다 — 표준은 던진다** — Day31 의 구현은 `size()` 가 0 이면 `remove(-1)` 이 되고, `LinkedList.remove` 는 음수 인덱스에 `null` 을 돌려준다. 그래서 짝이 안 맞아 한 번 더 `pop` 해도 예외가 없고 **경로가 조용히 비는** 쪽으로 간다. `isEmpty()` 를 만들어 두고 `pop()` 안에서 쓰지 않은 것이고, 그 코드에서 `isEmpty()` 를 부르는 곳은 없다. **Day35 가 `java.util.Stack` 으로 갈아타면서 이 자리의 성질이 뒤집힌다** — 표준 `pop()` 은 빈 스택에서 `EmptyStackException` 을 던지므로 짝이 안 맞으면 **조용히 지나가는 대신 그 자리에서 터진다.** 같은 코드가 더 안전해진 것이 아니라 **증상이 「경로가 비어 보인다」에서 「프로그램이 죽는다」로 바뀐 것**이고, 어느 쪽이 나은지는 「짝을 못 맞춘 것을 언제 알고 싶은가」가 정한다 → [[exception-handling]]

  **Day38 이후로는 이 축 자체가 사라진다.** 스택이 `getMenuPath()` 안의 지역 변수이므로 **빈 스택에서 `pop` 이 불릴 경로가 없다** — `while (!menuPath.empty())` 가 조건으로 막고 있고, 그 스택은 메서드가 끝나면 버려진다. 「자작이 조용하고 표준이 던진다」는 비교는 **스택을 오래 들고 있을 때만 의미가 있는 물음**이었다.
- **push/pop 의 짝을 아무도 강제하지 않는다 — Day38 이 그 짝을 없앤다** — `AbstractCommand.execute` 는 들어올 때 `push` 하고 「9」로 나갈 때 `pop` 한다. 짝이 맞는 것은 **그 메서드에 다른 출구가 없기 때문**이고, 나중에 `return` 하나가 늘면 경로가 한 칸씩 깊어진 채로 남는다. 증상은 프롬프트가 `메인/회원/회원>` 처럼 자라는 것뿐이라 오래 눈에 안 띈다. `try/finally` 로 짝을 묶는 것이 이 문제의 표준 답이다. **Day35 는 그 위험을 실제로 하나 늘린다** — `MenuGroup.execute` 의 `try` 블록이 `menu.execute()` 를 감싸고 있어서, 자식 트리 어딘가에서 던진 `NumberFormatException` 이 **자식의 `pop` 을 건너뛴 채** 부모의 `catch` 로 잡힌다. 짝이 깨지고도 프로그램은 계속 돈다 → [[exception-handling]] · [[composite-pattern]]

  **Day38 의 답은 `try/finally` 가 아니었다.** 짝을 묶는 대신 **스택을 오래 살려 두지 않는 쪽**으로 갔다 — 한 메서드 안에서 쌓고 그 안에서 다 비우므로 예외가 어디서 나든 남는 상태가 없다. 「짝을 지키는 방법」이 아니라 **「짝이 코드 한 곳에 다 보이게 만드는 방법」**이고, 같은 문제의 자원 쪽 버전에는 문법이 따로 있다 → [[try-with-resources]]
- **`HelpCommand` 는 `menuPath` 를 받고 아무것도 하지 않는다** — 서브메뉴가 없으니 쌓을 것이 없어 맞는 동작인데, **인터페이스가 그 인자를 요구한다.** 「이 명령은 경로를 만지지 않는다」가 타입으로 표현되지 않아서, 받고 안 쓰는 것과 받고 쓰는 것을 읽는 사람이 하나하나 확인해야 한다 → [[interface-segregation-principle]]
- **경로를 만드는 메서드가 두 클래스에 복사됐다 — 6일 뒤에 한 벌로 줄어든다** — Day31 의 필기가 「menuPath 호출이 필요한 App, AbstractCommand에 적용한다」로 적었다. **하루 전 회차가 공통 코드를 부모로 올리는 일에 절 하나를 쓴 다음 날에 같은 메서드를 두 벌 만든 것**이고, 두 클래스에 공통 부모가 없어서 올릴 곳이 없다는 것이 실제 이유였다. Day35 가 그것을 해결하는 방식이 「부모로 올린다」가 **아니라는 것**이 볼 만한 자리다 — 경로를 쓰는 주체가 `App` 과 커맨드 둘에서 **`MenuGroup` 하나로 줄었기** 때문에 복사할 대상 자체가 없어졌다. 커맨드는 이제 경로를 모른다. **중복을 없앤 것은 일반화가 아니라 책임의 재배치였다** → [[generalization]] · [[refactoring]] · [[composite-pattern]]
- **`getMenuTitle` 이 한 클래스 안에서 두 가지를 뜻하게 됐다** — `AbstractCommand` 에는 「번호로 메뉴 이름을 얻는」 `getMenuTitle(int)` 가 이미 있고 거기에 「스택으로 경로 문자열을 얻는」 `getMenuTitle(Stack)` 이 붙었다. 오버로딩이라 컴파일은 되지만 **이름이 같을 이유가 없는 두 일**이다 → [[method]]
- **`Stack` 이라는 이름이 `java.util.Stack` 과 겹친다 — Day35 는 겹치기를 그만두고 표준을 쓴다** — 13일 앞 회차의 `List` 가 `java.util.List` 와 겹쳤던 것과 같은 자리다. Day31 의 노트에서 `Map` 과 `HashMap` 은 표준 것을 그대로 쓰고 `Stack`·`Queue` 는 직접 만들어 **한 파일 안에 표준 컬렉션과 자작 컬렉션이 섞였다.** Day35 의 `MenuGroup` 은 `import java.util.Stack;` 을 적고 자작 클래스를 버린다 — **직접 만들어 배우는 단계와 만든 것을 계속 쓰는 단계가 갈리는 자리**이고, 자작 `List` 계열(`ArrayList`·`LinkedList`)도 같은 회차에 `java.util` 쪽으로 바뀐다 → [[package]] · [[hash-based-collection]]
- **저장을 계산으로 바꾸는 것이 공짜는 아니다 — 대가가 반복 계산으로 옮겨 갔다** — Day38 의 `getMenuPath()` 는 `Prompt.input("%s>", getMenuPath())` 자리에서 **키 입력마다** 불리고, 부를 때마다 스택을 새로 만들어 층 수만큼 `push` 하고 다시 그만큼 `pop` 한다. 메뉴 깊이가 둘셋이라 눈에 안 띄지만, **Day35 는 문자열 조립만 했고 Day38 은 조립 전에 사슬을 거슬러 올라가는 일까지 한다.** 정확성을 얻고 반복 계산을 냈으며, 이 크기에서는 맞는 교환이다 — **「저장할까 계산할까」의 답이 자료 크기에 달려 있다**는 것이 여기서 처음 보이는 형태다 → [[caching]]
- **`empty()` 와 `isEmpty()` 가 같은 클래스에 둘 다 있다** — Day38 은 `while (!menuPath.empty())` 로 `Stack` 자신의 `empty()` 를, 바로 아랫줄에서는 `!strBuilder.isEmpty()` 로 `StringBuilder` 의 `isEmpty()` 를 쓴다. `java.util.Stack` 에는 자기 `empty()` 와 `Vector` 에서 물려받은 `isEmpty()` 가 **둘 다 있고 하는 일이 같다** — `empty()` 는 `Collection` 인터페이스가 생기기 전의 이름이고 지금은 남아 있는 흔적이다. Day31 의 자작 스택이 `isEmpty()` 라고 이름 붙였던 것과 갈리는 자리이고, **표준 라이브러리에서 같은 일을 하는 이름이 둘인 것은 대개 역사이지 구별이 아니다** → [[inheritance]] · [[method]]
- **`Object` 를 담으므로 무엇이든 들어간다 — Day35 에서 그 구멍만은 닫힌다** — Day31 의 `menuPath` 에 문자열만 넣는다는 것은 코드를 쓴 사람만 아는 약속이고, 꺼낼 때는 `append(Object)` 가 `toString()` 을 불러 주므로 형변환 없이 지나간다. 숫자를 잘못 넣어도 아무 일이 없다. Day35 의 `Stack<String>` 은 **넣는 쪽에서 컴파일러가 막고** 꺼낸 것이 곧 `String` 이라 `for (String s : menuPath)` 가 캐스팅 없이 성립한다. 순회를 추상화해도 타입은 추상화되지 않던 자리를 메우는 것이 이 표기다 → [[type-casting]] · [[object-class]]

## 함께 보는 개념

- [[queue]] — 반대 순서의 짝
- [[linked-list]] — 이 스택이 상속한 구현
- [[jvm-stack]] — 같은 규칙으로 동작하는 메모리 영역
- [[command-loop]] — 스택이 값으로 만들어 준 「지금 어디인가」
- [[recursion]] — 같은 규칙이 호출로 나타나는 자리
- [[interface-segregation-principle]] — 상속으로 만든 대가를 재는 원칙
- [[encapsulation]] — 제약을 지키려면 필요한 것
- [[string-builder]] — 경로 문자열을 만드는 도구
- [[inheritance]] — 이 구현이 고른 수단
- [[generalization]] — 복사된 경로 메서드가 걸리는 자리
- [[package]] — 표준 라이브러리와 이름이 겹치는 문제
- [[composite-pattern]] — 스택이 트리의 가지로 내려간 뒤의 구조
- [[iterator-pattern]] — 스택을 아래에서 위로 돌게 해 주는 것
- [[for-loop]] — 인덱스 루프가 for-each 로 바뀐 자리
- [[exception-handling]] — 짝이 깨졌을 때 알게 되는 방법이 갈리는 축
- [[refactoring]] — 필드를 지역 변수로 내린 변경의 성격
- [[caching]] — 저장할까 계산할까의 축
- [[garbage-collection]] — 만들자마자 버려지던 스택이 사라진 자리
- [[try-with-resources]] — 같은 「짝 맞추기」 문제에 문법이 있는 쪽

## 출처

- [[2024-07-09-Day31]] — 「LIFO(Last In, First Out)」와 「한쪽 끝에서만 요소를 넣거나 뺄 수 있다」로 개념을 배우고, 14일 전에 만든 `LinkedList` 를 상속해 `push`(= `add`) · `pop`(= `remove(size()-1)`) · `isEmpty` 세 개만 얹어 구현했다. 실습에서는 `App` 의 `menuPath` 필드로 메뉴 경로를 쌓아 `execute()` 에서 「메인」을 push 하고, `AbstractCommand.execute(Stack)` 이 들어올 때 제목을 push 하고 「9」로 나갈 때 pop 하며, `StringBuilder` 로 이어 붙여 `메인/회원>` 프롬프트를 만든다. `peek` 이 없고 `pop()` 이 빈 스택에서 조용히 `null` 을 주며, 상속 때문에 목록 연산이 전부 노출된 상태에서 **경로 출력이 실제로 그 `get(i)` 에 의존한다** — 쓰기는 스택, 읽기는 목록으로 쓰인 셈이다. 꼬리를 위로 삼아 `pop` 이 O(n) 이 된 것과 경로 조립 메서드가 `App`·`AbstractCommand` 두 곳에 복사된 것도 이 회차다
- [[2024-07-15-Day35]] — 같은 `menuPath` 가 **자작 스택을 버리고 `java.util.Stack<String>` 이 되고, 사는 자리가 `App` 에서 트리의 가지(`MenuGroup`)로 내려간다.** 원소 타입이 정해져 `Object` 구멍이 닫히고, 두 곳에 복사돼 있던 경로 조립 메서드가 `getMenuPathTitle` 하나로 줄고(커맨드는 이제 경로를 모른다), `get(i)` 인덱스 루프가 `for (String s : menuPath)` 로 바뀌며 `length() > 0` 이 `!isEmpty()` 가 된다. **그 for-each 가 아래에서 위로 도는 것은 `java.util.Stack` 이 `Vector` 를 상속했기 때문**이므로 Day31 의 「쓰기는 스택 읽기는 목록」이 표준으로 갈아탄 뒤에도 그대로다. 반대로 성질이 뒤집힌 자리가 하나 있다 — 표준 `pop()` 은 빈 스택에서 `EmptyStackException` 을 던지므로 짝이 안 맞을 때 조용히 넘어가지 않는다. 그리고 `setParent` 가 부모의 스택 참조를 복사하는 방식이라 **세 층에서는 조립 순서에 따라 자식이 옛 스택에 쌓아 경로가 끊긴다**(→ [[composite-pattern]])
- [[2024-07-18-Day38]] — **필기가 스스로 세 가지 문제를 적고(「인스턴스 될 때마다 새로운 Stack을 생성한다」·「부모의 menuGroup이 있다면 인스턴스된 Stack은 Garbage가 된다」·「Stack의 구조로 꺼내는 것이 아니라 List타입으로 탐색을 한다」) `menuPath` 를 필드에서 지역 변수로 내린다.** 생성자의 `new Stack<>()` 과 `setParent` 의 참조 복사가 함께 사라지고, `getMenuPath()` 가 `this` 에서 `parent` 를 타고 `null` 까지 올라가며 `push` 한 뒤 `while (!menuPath.empty())` 로 `pop` 해 경로를 만든다. 이 회차가 이 노트의 세 항목을 동시에 닫는다 — **조립 순서 의존이 없어지고, push/pop 짝이 한 메서드 안에서 닫히고, 처음으로 스택 연산만으로 읽는다.** 순서가 맞는 근거도 `Vector` 반복자에서 **LIFO 그 자체**로 옮겨 왔다. 대가는 프롬프트를 찍을 때마다 사슬을 거슬러 올라가는 반복 계산이고, 같은 클래스의 `empty()` 와 `isEmpty()` 를 한 메서드 안에서 나란히 쓴 것도 이 코드다
