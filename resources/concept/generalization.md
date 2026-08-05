---
type: concept
id: generalization
title: 일반화 (Generalization)
aliases:
  - 일반화
  - generalization
  - 공통 코드 끌어올리기
  - pull up
  - 수퍼클래스 추출
  - extract superclass
up:
  - 2024-07-08-Day30
tags:
  - 설계
  - 객체지향
  - 리팩터링
  - 상속
---

# 일반화 (Generalization)

**여러 클래스에 똑같이 들어 있는 코드를 공통 수퍼클래스로 끌어올려 한 벌로 만드는 설계 이동.** 상속은 그 이동을 실제로 수행하는 문법이고, 일반화는 **어느 방향으로 옮기는가**다 — 아래(특수)에서 위(일반)로다.

## 정의

필기가 이 이동을 여섯 줄로 적었는데 순서가 그대로 절차다.

| 순서 | 필기의 문장 | 하는 일 |
|---|---|---|
| 1 | 「응집력을 높인 결과 각 Command 클래스에 동일한 코드 생성」 | **관찰** — 중복이 있다는 사실이 먼저다 |
| 2 | 「동일한 코드를 일반화를 통해 하나의 클래스에 넣는다」 | 목표 |
| 3 | 「상속을 사용하여 일반화를 진행한다」 | 수단 → [[inheritance]] |
| 4 | 「수퍼클래스를 추상클래스로 설정하여 직접적인 클래스 사용을 막는다」 | 부모는 반쪽이므로 만들 수 없게 한다 → [[abstract-class]] |
| 5 | 「수퍼클래스에서 결정되지 못하는 메소드는 추상메소드로 만든다」 | 올라갈 수 없는 것에 자리만 남긴다 |
| 6 | 「자식클래스에서 추상메소드에 방법을 제시해야한다」 | 자식이 그 자리를 채운다 → [[method-overriding]] |

**시작이 클래스 그림이 아니라 중복이다.** 부모를 먼저 설계해 놓고 자식을 만드는 것이 아니라, 자식들이 이미 있고 그중 같은 것을 위로 올린다. 그래서 이 작업에는 **부모의 내용을 고민할 필요가 없다** — 무엇이 올라갈지는 세면 나온다.

가르는 기준은 두 개뿐이다.

- **세 자식에게 같은 것** → 부모로 올린다
- **부모가 결정할 수 없는 것** → 부모에 추상 메서드로 자리만 두고 자식이 채운다

## 사용 예시

세 Command 클래스가 응집도 정리 직후 같은 `execute()` 를 갖게 된 상태에서 시작한다. 그 메서드는 「메뉴를 찍고 · 입력을 받고 · 번호로 해석하고 · 갈래로 보내고 · `9` 면 나간다」로, **Command 마다 다른 부분이 두 군데뿐이다.**

```java
public class UserCommand implements Command {

  String menuTitle;
  String[] menus = {"등록", "목록", "조회", "변경", "삭제"};

  @Override
  public void execute() {
    printMenus();
    while (true) {
      String command = Prompt.input(String.format("메인/%s>", menuTitle));
      if (command.equals("menu")) { printMenus(); continue; }
      else if (command.equals("9")) { break; }
      try {
        int menuNo = Integer.parseInt(command);
        String menuName = getMenuTitle(menuNo);
        if (menuName == null) { ... continue; }
        processMenu(menuName);                    // ← 여기가 Command 마다 다르다
      } catch (NumberFormatException ex) { ... }
    }
  }

  private void printMenus() { ... }               // menus 를 읽는다
  private boolean isValidateMenu(int menuNo) { ... }
  private String getMenuTitle(int menuNo) { ... }
}
```

일반화한 뒤 자식에 남은 것은 **네 개**다.

```java
public class UserCommand extends AbstractCommand {

  LinkedList userList = new LinkedList();

  String menuTitle;
  String[] menus = {"등록", "목록", "조회", "변경", "삭제"};

  public UserCommand(String menuTitle) {
    super(menuTitle);                             // 제목은 부모가 갖는다
  }

  @Override
  public void processMenu(String menuName) {      // 갈래로 보내는 일 — 자식마다 다르다
    switch (menuName) {
      case "등록": this.addUser(); break;
      ...
    }
  }

  @Override
  public String[] getMenus() {                    // 부모가 메뉴 목록을 물어보는 창구
    return menus;
  }

  private void addUser() { ... }                  // 실제 기능
  ...
}
```

옮긴 것과 남긴 것을 세면 이 이동의 전부가 보인다.

| 코드 | 어디로 | 왜 |
|---|---|---|
| `execute()` 의 루프 전체 | **부모로** | 세 Command 가 글자까지 같다 |
| `printMenus`·`isValidateMenu`·`getMenuTitle` | **부모로** | 같다 |
| `menuTitle` | **부모로** (`super(menuTitle)`) | 같은 필드, 값만 다르다 |
| `processMenu(String)` | 자식에 남고 부모에 추상 메서드 | 부모가 결정할 수 없다 |
| `getMenus()` | 자식에 남고 부모에 추상 메서드 | 부모가 목록을 모른다 |
| `addUser`·`listUser`… | 자식에만 | 애초에 공통이 아니다 |

**같은 날 이 이동을 두 번 한다.** 앞 절에서는 `ArrayList`·`LinkedList` 의 공통 `size` 를 `AbstractList` 로 올렸고(→ [[abstract-class]]), 뒤 절에서 세 Command 의 공통 `execute()` 를 `AbstractCommand` 로 올렸다. **한쪽은 필드, 한쪽은 메서드**인데 절차가 같다 — 중복을 세고, 부모를 만들고, 부모를 `abstract` 로 막고, 못 올라간 것을 추상 메서드로 남긴다.

## 왜 중요한가

**고칠 자리의 개수가 자식 수에서 1로 준다.** 「이전 메뉴로 나가는 명령을 `9` 에서 `0` 으로 바꾸자」는 요구가 오면 일반화 전에는 Command 네 곳을 열어야 하고, 후에는 `AbstractCommand` 한 곳이다. 그리고 **하나를 빠뜨렸을 때 아무 오류도 나지 않는다** — 회원 메뉴만 `0` 으로 나가고 게시판은 `9` 로 나가는 프로그램이 컴파일되고 실행된다. 중복이 위험한 이유는 코드가 길어지는 것이 아니라 **어긋난 상태가 정상으로 보인다**는 데 있다.

**응집도를 올리면 반드시 이 작업이 따라온다.** 필기의 첫 줄이 그것을 말한다 — 「응집력을 높인 결과 각 Command 클래스에 동일한 코드 생성」. 한 클래스에 몰려 있던 흐름 제어를 네 클래스로 나누면 그 순간 흐름 제어가 네 벌이 된다. **분리가 중복을 만들고 일반화가 그것을 되감는다** — 리팩터링이 한 단계로 끝나지 않는 이유이고, 여기서 멈추면 나눈 것이 손해로 남는다 → [[cohesion]] · [[refactoring]]

**그리고 부모가 「무엇을 물어볼지」를 정하게 된다.** `getMenus()` 를 추상 메서드로 두는 순간 부모는 「자식은 메뉴 목록을 줄 수 있다」를 전제로 코드를 쓸 수 있다. 올릴 수 없는 것을 **없는 것으로 두지 않고 질문으로 바꾸는 것**이 4~6번 줄이 하는 일이고, 이것이 없으면 공통 코드는 자식마다 다른 변수 이름에 걸려 올라가지 못한다 → [[template-method-pattern]]

## 경계와 오해

- **일반화 ≠ 상속** — 상속은 `extends` 라는 문법이고 일반화는 **그것을 쓰는 이유 중 하나**다. 닷새 앞선 회차의 `Sorter` 는 자식에게 물려줄 코드가 하나도 없는 부모였다(추상 메서드 하나뿐) — 상속을 썼지만 일반화한 것이 없고, 목적은 [[polymorphism]] 이었다. 이번 `AbstractCommand` 는 반대로 **물려줄 코드가 목적**이다. 같은 `extends` 가 두 이유로 쓰이므로 「상속을 썼다」로는 무엇을 한 것인지 알 수 없다 → [[inheritance]]
- **Generalization 은 GRASP 지침이 아니다** — 필기가 「리팩토링: GRASP의 High Cohesion」 바로 다음에 「리팩토링: 상속의 Generalization 적용」을 두어 **열 번째 지침처럼** 읽히는데, GRASP 아홉 개에 Generalization 은 없다. 이 말은 **UML 에서 상속 관계를 부르는 이름**(속이 빈 삼각형 화살표)이고, 그래서 앞 절의 UML 다이어그램과 짝이다. 굳이 GRASP 에서 이어지는 지침을 찾으면 Polymorphism 과 Protected Variations 쪽이다 → [[grasp]]
- **같은 코드 ≠ 같은 이유** — 올릴 것을 「글자가 같은 것」으로 고르면, 우연히 같았던 코드가 한쪽만 바뀌어야 하는 날 부모를 다시 쪼개야 한다. 세 Command 의 `menus` 가 그 시험대다 — `{"등록","목록","조회","변경","삭제"}` 세 개가 완전히 같은데 **이것이 규칙인지 우연인지 필기가 묻지 않았다.** 「모든 메뉴는 CRUD 다섯 개를 갖는다」면 부모로 올라가야 하고, 「지금은 셋이 같을 뿐」이면 남아야 한다. **판단이 필요한 자리를 세는 것으로 대신할 수 없다** → [[crud]]
- **일반화를 선언하고 정작 중복이 남았다** — 자식 셋에 `String menuTitle;` 과 `String[] menus` 가 그대로 있다. `menuTitle` 은 `super(menuTitle)` 로 부모에 넘겼는데 **자식의 필드 선언은 지워지지 않았고**, 그래서 그 필드는 영원히 `null` 이다. 올린 것은 `execute()` 계열이고 필드 중복은 손대지 못했다 → [[field-hiding]]
- **부모 필드를 자식이 다시 선언하면 일반화가 무효가 된다** — 같은 노트 앞 절의 `AbstractList.size` 가 그 실물이다. `protected int size` 를 올려놓고 `ArrayList` 가 `private int size` 를, `LinkedList` 가 `int size` 를 또 선언했다. 코드는 돌아가는데 **끌어올린 것이 아무도 쓰지 않는 필드가 되었다** — 일반화의 성공 여부는 「부모에 코드가 생겼나」가 아니라 **「자식에서 없어졌나」**로 확인해야 한다 → [[field-hiding]] · [[abstract-class]]
- **「부모가 결정할 수 없는 것」과 「자식마다 값이 다른 것」은 다르다** — 필기는 둘 다 추상 메서드로 처리했지만 갈라야 한다. `processMenu` 는 **동작**이 다르므로 추상 메서드가 맞고, `getMenus()` 는 **값**이 다를 뿐이므로 `menuTitle` 처럼 **생성자 매개변수**로 충분했다. 그렇게 했다면 자식에서 `menus` 배열과 `getMenus()` 가 같이 사라진다. **값을 추상 메서드로 받으면 자식마다 필드 하나와 메서드 하나가 계속 남는다.**
- **일반화 ≠ 클래스 분리** — 18일 앞선 회차는 `UserCommand` 를 `UserList` + `UserCommand` 로 **옆으로** 갈랐고(역할이 둘이라서), 이번에는 세 Command 의 공통을 **위로** 올렸다(같은 것이 세 벌이라서). 둘 다 「중복·혼재를 없앤다」로 뭉치면 방향이 안 보이고, 그러면 「클래스를 쪼갤까 부모를 만들까」를 고를 근거가 없어진다. 판정 기준은 **한 클래스 안에 두 주제가 있는가**(→ 분리) 대 **여러 클래스에 한 코드가 있는가**(→ 일반화)다 → [[cohesion]]
- **일반화하면 흐름의 주인이 부모로 넘어간다** — `execute()` 가 부모로 올라간 뒤 자식의 `processMenu` 는 **자기가 부르는 코드가 아니라 불리는 코드**가 된다. 코드를 옮기는 일로 시작했는데 **제어의 방향이 뒤집힌 것**이고, 그래서 자식만 읽으면 언제 실행되는지 알 수 없다 → [[template-method-pattern]]
- **추상 메서드로 열어 둔 자리는 `public` 이 된다** — 자식의 `processMenu` 는 일반화 전에 `private` 이었는데 부모가 부를 수 있어야 하므로 `public` 이 되었다(오버라이딩은 접근을 좁힐 수 없다). **부모로 코드를 올린 대가로 자식의 내부 메서드가 외부에 열린다** — 응집도를 올릴 때 `private` 을 `public` 으로 열어야 했던 것과 같은 종류의 대가다 → [[method-overriding]] · [[access-modifier]]
- **부모가 하나뿐이라는 것이 제약으로 돌아온다** — `extends` 는 하나만 쓸 수 있으므로, 이 자식들이 나중에 다른 공통 코드 묶음에도 속해야 하면 그쪽은 일반화로 풀 수 없다. 공통 **약속**은 여러 개 붙을 수 있지만 공통 **코드**는 한 줄기뿐이다 → [[multiple-inheritance]] · [[interface]]

## 함께 보는 개념

- [[inheritance]] — 이 이동을 실행하는 문법
- [[abstract-class]] — 올라간 코드가 사는 곳이자 직접 생성을 막는 장치
- [[template-method-pattern]] — 일반화의 결과로 생기는 부모/자식 역할 구조
- [[refactoring]] — 이 이동이 놓인 작업의 단위
- [[cohesion]] — 이 이동을 필요하게 만든 앞 단계
- [[grasp]] — 필기가 이것을 이어 붙인 지침 묶음
- [[field-hiding]] — 일반화를 조용히 무효로 만드는 실수
- [[method-overriding]] — 자식이 자리를 채우는 방법
- [[polymorphism]] — 상속을 쓰는 또 다른 이유
- [[interface]] — 코드가 아니라 약속만 올릴 때의 선택
- [[crud]] — 세 자식의 메뉴가 같았던 이유

## 출처

- [[2024-07-08-Day30]] — 「리팩토링: 상속의 Generalization 적용」 절이 이 이동의 절차를 여섯 줄로 적고 실습으로 수행한다. 응집도 정리로 세 Command 에 같은 `execute()` 가 생긴 것을 관찰한 뒤 그것을 `AbstractCommand` 로 올리고, 부모가 결정할 수 없는 `processMenu`·`getMenus` 를 추상 메서드로 남겨 자식이 채우게 했다. 같은 노트 앞 절의 `List`/`AbstractList` 도 같은 절차의 필드 버전이다. 다만 자식 셋에 `String menuTitle;` 과 `String[] menus` 가 그대로 남아 **끌어올리기가 절반에서 멈췄고**, `menuTitle` 은 부모에도 있어 자식 쪽이 죽은 필드가 되었다
