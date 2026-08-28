---
type: concept
id: dispatch-table
title: 분기 테이블 (Dispatch Table)
aliases:
  - 분기 테이블
  - dispatch table
  - 디스패치 테이블
  - 명령 테이블
  - 명령 레지스트리
  - command map
  - 커맨드 맵
  - jump table
  - 점프 테이블
  - 룩업 테이블
  - lookup table
  - 핸들러 맵
up:
  - 2024-07-09-Day31
  - 2024-07-15-Day35
  - 2026-08-28-action-runtime-engine
tags:
  - 설계
  - 제어문
  - 리팩터링
  - 자료구조
---

# 분기 테이블 (Dispatch Table)

**「어느 값이면 어느 코드」의 짝을 자료구조에 담아 두고, 분기를 조회로 바꾸는 것.** `switch` 의 `case` 목록이 `Map` 의 항목이 되고, 갈래를 내는 코드는 **조회 한 줄**로 줄어든다. 늘어나는 것은 데이터이고 코드는 늘지 않는다.

## 정의

세 부분으로 나뉘는 것이 이 구조의 성질을 정한다.

| 부분 | 이 실습에서 | 무엇에 열려 있나 |
|---|---|---|
| **표** | `Map<String, Command> commandMap` | 항목 수 |
| **등록** | `App()` 생성자의 `put` 다섯 줄 | 항목이 늘면 여기가 바뀐다 |
| **조회·실행** | `commandMap.get(menuTitle).execute()` | **아무것도 바뀌지 않는다** |

값 쪽에 담기는 것이 **데이터가 아니라 실행할 것**이라는 점이 이 구조를 특별하게 만든다. 그래서 값의 타입이 인터페이스여야 하고, 조회한 것을 부를 수 있는 것은 다형성이 해 준다 → [[interface]] · [[polymorphism]]

```text
switch:   값 ──▶ 컴파일 시점에 고정된 case 목록 ──▶ 코드 블록
표:       값 ──▶ 실행 중에 채워진 Map          ──▶ 객체의 메서드
```

## 사용 예시

하루 앞 회차의 `App` 은 명령 넷을 각각 필드로 들고 문자열로 갈래를 냈다.

```java
UserCommand userCommand = new UserCommand("회원");
BoardCommand boardCommand = new BoardCommand("게시판");
BoardCommand noticeCommand = new BoardCommand("공지사항");
ProjectCommand projectCommand = new ProjectCommand("프로젝트", userCommand.getUserList());
HelpCommand helpCommand = new HelpCommand();

void processMenu(String menuTitle) {
  switch (menuTitle) {
    case "회원": userCommand.execute(); break;
    case "프로젝트": projectCommand.execute(); break;
    case "게시판": boardCommand.execute(); break;
    case "공지사항": noticeCommand.execute(); break;
    case "도움말": helpCommand.execute(); break;
    default:
      System.out.printf("%s 메뉴의 명령을 처리할 수 없습니다.\n", menuTitle);
  }
}
```

**다섯 `case` 가 하는 일이 같다** — `execute()` 를 부른다. 다른 것은 어느 변수인가뿐이다.

표는 그 짝을 데이터로 옮긴다.

```java
Map<String, Command> commandMap = new HashMap<>();
```

필기가 세 줄로 그 구조를 적었다 — 「String과 Command를 받을 수 있는 Map구조를 선언한다 / String에는 메뉴명을 대입한다 / Command는 인터페이스로 다형성을 이용하여 구현체를 대입한다」.

```java
public App() {
  commandMap.put("회원", new UserCommand("회원", userList));
  commandMap.put("게시판", new BoardCommand("게시판", boardList));
  commandMap.put("공지사항", new BoardCommand("공지사항", noticeList));
  commandMap.put("프로젝트", new ProjectCommand("회원", projectList, userList));
  commandMap.put("도움말", new HelpCommand());
}
```

```java
void processMenu(String menuTitle) {
  Command command = commandMap.get(menuTitle);
  if (command == null) {
    System.out.printf("%s 메뉴의 명령을 처리할 수 없습니다.\n", menuTitle);
    return;
  }
  command.execute();
}
```

**필드 다섯 개와 `case` 다섯 개가 표 하나와 세 줄로 줄었다.** 그리고 `switch` 의 `default:` 가 `null` 검사로 자리를 옮겼다 — **같은 안전망이 문법에서 조회 결과로 내려온 것**이다 → [[switch-statement]] · [[hash-based-collection]]

### 6일 뒤, 표가 목록으로 되돌아간다

Day35 의 컴포짓 리팩터링에서 `Map<String, Command> commandMap` 이 **사라진다.** 대신 각 메뉴가 자기 자식 목록을 든다.

```java
public class MenuGroup extends AbstractMenu {
  private List<Menu> children = new ArrayList<>();

  public void add(Menu child) { /* 생략 */ children.add(child); }

  public Menu getMenu(int index) {
    if (index < 0 || index >= children.size()) {
      return null;
    }
    return children.get(index);
  }
}
```

```java
int menuNo = Integer.parseInt(command);
Menu menu = getMenu(menuNo - 1);      // 키가 아니라 번호로 찾는다
if (menu == null) {
  System.out.println("유효한 메뉴 번호가 아닙니다.");
  continue;
}
menu.execute();
```

**표의 세 부분이 그대로 있고 「키」만 바뀌었다.**

| 부분 | Day31 | Day35 |
|---|---|---|
| 표 | `Map<String, Command>` | `List<Menu> children` |
| 등록 | `commandMap.put("회원", ...)` | `mainMenu.add(new MenuItem("등록", ...))` |
| 조회 | `commandMap.get(menuTitle)` | `children.get(menuNo - 1)` |
| 열쇠 | **메뉴 이름(문자열)** | **화면에 찍힌 번호(정수)** |

즉 이것은 표를 버린 것이 아니라 **문자열 키 표에서 순서 있는 목록으로 되돌아간 것**이고, 34일 전 Day11 의 `menus[menuNo - 1]` 과 같은 모양이다. 다른 것은 담긴 것이 문자열이 아니라 **실행할 객체**라는 점뿐이다 — 「표에 담는 것이 데이터인가 할 일인가」 축에서는 앞으로 가고 「키가 이름인가 위치인가」 축에서는 뒤로 온 셈이다 → [[array]] · [[composite-pattern]]

## 왜 중요한가

**갈래가 늘어도 갈래를 내는 코드가 안 자란다.** 28일 앞선 회차가 이미 같은 이동을 한 번 했다 — `case` 여섯 개로 메뉴 이름을 찍던 것을 `menus[menuNo - 1]` 한 줄로 접었고, 메뉴를 더하는 일이 배열 선언 하나를 고치는 일이 되었다. 그때 표에 담은 것이 **문자열**이었고 이번에는 **객체**다. 같은 발상이 「출력할 데이터가 다를 때」에서 「할 일이 다를 때」로 올라온 것이다 → [[array]] · [[switch-statement]]

**다형성을 실제로 쓰게 되는 마지막 한 칸이다.** 하루 앞 회차는 `Command` 인터페이스와 `AbstractCommand` 를 만들어 다형성의 두 전제를 다 갖췄는데도 `App` 이 구현 클래스를 들고 `switch` 로 갈랐다. **다형성이 이득을 주는 것은 「호출부가 타입을 모를 때」**이고, 표에 담는 순간 호출부에서 구현 클래스 이름이 전부 사라진다 → [[polymorphism]] · [[dependency-inversion-principle]]

**갈래를 실행 중에 바꿀 수 있게 된다.** `case` 목록은 컴파일 시점에 고정이지만 표는 실행 중에 `put`·`remove` 할 수 있다. 이 실습은 쓰지 않지만, 「설정 파일을 읽어 명령을 등록한다」·「플러그인을 나중에 끼운다」가 가능해지는 것이 이 차이의 값이다.

**커널 규모에서는 이 구조가 불변식이 된다.** 2년 뒤 회사 워크플로 엔진([[2026-08-28-action-runtime-engine]])에서 같은 구조를 다시 만났다 — 결재 커널이 도메인 타입마다 다르게 처리해야 할 모든 결정을 「커널에 `type ==` 값 비교 분기 0개, 전부 레지스트리 조회」로 계약화했고, 이 불변식은 grep 으로 검증 가능하다. 표의 값은 「정책 데이터 + 핸들러 포인터」 묶음이라 Day31 의 `Command` 객체가 확장된 모양이고, 새 타입 등록 = 레지스트리 항목 추가일 뿐 커널은 편집하지 않는다 — [[open-closed-principle]] 이 「원칙」에서 「grep 0건이라는 검사 가능한 계약」으로 내려온 것이다. 단 전부 표로 가지는 않는다: 도메인 상황을 판단하는 분기(「선점됐나」)는 핸들러 **안에** 남는 것이 정상이고, 금지되는 것은 커널이 타입을 알아보는 것뿐이다.

## 경계와 오해

- **분기가 없어진 것이 아니라 자리가 바뀐 것이다** — 「어느 명령인가」를 고르는 일은 그대로 있고 `HashMap` 의 해시 계산으로 옮겼다. 얻은 것은 그 일이 **한 곳에서만 일어난다**는 것이고, 잃은 것은 갈래 목록이 코드에 나란히 보이지 않는다는 것이다. `switch` 는 읽으면 다루는 값이 전부 보이는데 표는 **등록하는 코드를 다 찾아야** 안다 → [[switch-statement]]
- **키의 오타를 컴파일러가 못 본다** — `case "회원":` 을 `case "회웜":` 으로 쓰면 그 자리에서 보이지만, `put("회웜", ...)` 는 컴파일된다. 그리고 조회가 `null` 을 돌려주므로 「처리할 수 없습니다」가 나올 뿐이라 **오타와 「없는 메뉴」가 같은 증상**이 된다. 문자열을 키로 쓴 대가이고, enum 을 키로 쓰면 되찾을 수 있다 → [[literal]]
- **같은 사실을 두 곳에 적게 된다 — 이 회차가 실제로 어긋났다** — 메뉴 이름이 **맵의 키**와 **명령의 생성자 인자** 두 곳에 들어간다.

  ```java
  commandMap.put("프로젝트", new ProjectCommand("회원", projectList, userList));
  ```

  키는 「프로젝트」이고 객체가 들고 있는 제목은 「회원」이다. 갈래는 제대로 나지만 화면에는 `[회원]` 이 찍히고 경로 표시도 `메인/회원` 이 된다. **컴파일러는 두 문자열이 같아야 한다는 것을 모른다** — 표 구조에서 가장 자주 생기는 어긋남이고, 명령이 자기 제목을 들고 있다면 `put(cmd.getTitle(), cmd)` 로 한 곳으로 줄일 수 있다 → [[dependency-injection]]

  **Day35 는 이 어긋남을 두 단계에 걸쳐 없앤다.** 앞부분에서는 위험이 그대로 남는다 — `new MenuItem("등록", userCommand)` 의 `"등록"` 이 `UserCommand.execute` 안의 `case "등록":` 과 짝이어야 하므로, 키가 맵에서 트리의 잎으로 옮겨졌을 뿐이다. 뒷부분에서 커맨드를 기능 하나씩 쪼개면 **그 문자열을 읽는 코드가 화면 출력밖에 남지 않는다.** 문자열 키 표의 근본 위험이 사라지는 조건이 「키를 잘 관리하기」가 아니라 **「키로 갈래를 고르지 않게 만들기」**였던 것이다 → [[command-pattern]]
- **메뉴 목록이 표 밖에 또 있다 — 6일 뒤에 한 벌로 합쳐진다** — Day31 에는 `String[] mainMenus` 가 화면 출력용으로 남아 있고 `commandMap` 의 키가 갈래용이었다. 메뉴를 하나 더할 때 **두 곳을 고쳐야 하며 한쪽만 고치면 조용히 어긋났다** — 배열에만 넣으면 눌렀을 때 「처리할 수 없습니다」, 맵에만 넣으면 화면에 안 보이는 명령이 된다. **Day35 의 `children` 은 그 둘을 겸한다** — `printMenus()` 가 그 목록을 돌며 `getTitle()` 로 화면을 만들고, 번호 조회도 같은 목록에서 한다. 메뉴를 더하는 일이 `add` 한 줄이 되고 **화면과 갈래가 어긋날 방법이 없어진다** → [[open-closed-principle]] · [[composite-pattern]]
- **`HashMap` 은 순서를 기억하지 않는다 — 그래서 6일 뒤의 답이 목록이었다** — 메뉴를 화면에 찍는 일이 `commandMap` 으로 넘어가려면 순서가 필요한데 `HashMap` 의 순회 순서는 보장이 없다. **표로 화면까지 만들려면 자료구조를 `LinkedHashMap` 이나 목록으로 바꿔야 하고**, Day31 이 배열을 따로 남긴 이유가 실은 여기에 있다(필기는 이유를 적지 않았다). Day35 가 고른 것은 `LinkedHashMap` 이 아니라 `ArrayList` 이고, **화면에 번호를 찍는 순간 이미 순서가 열쇠였다**는 것을 인정한 셈이다 — 이름으로 찾을 이유가 없었다면 이름을 키로 쓸 이유도 없었다 → [[hash-based-collection]] · [[dynamic-array]]
- **표를 쓸 수 있는 조건이 있다** — 모든 `case` 가 **같은 시그니처의 같은 호출**로 접혀야 한다. 하루 앞 회차의 `switch` 는 다섯 줄이 전부 `execute()` 였기 때문에 접혔고, `case` 마다 인자가 다르거나 여러 문장이 있으면 그것을 먼저 객체로 만들어야 한다. **표는 리팩터링의 결과이지 시작이 아니다** — 명령 객체를 만드는 일(하루 전)이 먼저였다 → [[refactoring]] · [[template-method-pattern]]
- **표에 담긴 값이 상태를 갖는다** — `case` 안의 코드는 상태가 없지만 `commandMap` 의 값은 목록을 든 객체다. 그래서 같은 클래스의 인스턴스를 둘 담을 수 있고 실제로 그렇게 한다 — 「게시판」과 「공지사항」이 둘 다 `BoardCommand` 이고 목록만 다르다. **`switch` 로는 표현할 수 없던 것**이며, 갈리는 것이 타입이 아니라 값일 때 클래스를 늘리지 않는 길이다 → [[instance]]
- **분기 테이블 ≠ 커맨드 패턴 — 6일 뒤가 그것을 증명한다** — Day31 은 둘을 같은 절에서 하지만 다른 것이다. 커맨드 패턴은 **할 일을 객체로 만드는 것**(하루 앞 회차의 `interface Command`)이고, 표는 **그 객체를 키로 찾는 것**이다. 명령 객체 없이 표만 쓰는 경우도(값이 문자열인 28일 전의 `menus[]`) 표 없이 명령 객체만 쓰는 경우도(하루 전의 `switch`) 있다. **Day35 가 `Map` 을 버리고도 커맨드는 남는다** — 오히려 기능 하나당 클래스 하나까지 더 잘게 쪼개진다. 두 개념이 한 절에 같이 있었을 뿐 서로 의존하지 않는다는 것이 그렇게 확인된다 → [[command-pattern]]
- **키가 사용자 입력이면 표가 곧 권한 경계가 된다** — 이 코드는 사용자가 고른 메뉴 이름을 그대로 조회 키로 쓴다. 실습에서는 메뉴 번호로 얻은 이름이라 안전하지만, **입력이 곧 실행할 것을 고르는 구조**라는 성질은 남는다. 표에 넣지 않은 것은 절대 실행되지 않는다는 것이 이 구조의 안전 근거이고, 반대로 표에 실수로 넣은 것은 곧바로 호출 가능해진다 → [[standard-input]]

## 함께 보는 개념

- [[switch-statement]] — 이 구조가 대체하는 문법
- [[hash-based-collection]] — 표를 담는 자료구조
- [[polymorphism]] — 조회한 것을 부를 수 있게 하는 성질
- [[interface]] — 값의 타입이 되는 약속
- [[array]] — 같은 발상의 앞 단계(값이 데이터일 때)
- [[dependency-inversion-principle]] — 호출부에서 구현 이름이 사라지는 원칙
- [[open-closed-principle]] — 조회 코드가 닫히고 등록 코드가 열린 결과
- [[dependency-injection]] — 표를 채우는 자리에서 함께 일어나는 일
- [[command-loop]] — 이 표를 쓰는 흐름
- [[instance]] — 같은 클래스를 두 항목으로 담는 선택
- [[refactoring]] — 표로 접기 전에 필요한 준비
- [[template-method-pattern]] — 표의 값들이 공통 골격을 갖는 구조
- [[composite-pattern]] — 표가 트리의 자식 목록으로 바뀐 뒤의 구조
- [[command-pattern]] — 표와 짝이지만 표에 의존하지 않는 쪽
- [[dynamic-array]] — 순서를 지키는 표를 담는 자료구조

## 출처

- [[2024-07-09-Day31]] — 하루 전 회차의 `App.processMenu` 문자열 `switch` 다섯 갈래를 `Map<String, Command> commandMap` 조회로 접었다. 「String에는 메뉴명을 대입한다 / Command는 인터페이스로 다형성을 이용하여 구현체를 대입한다 / put메서드를 이용하여 {Key : 메뉴명, Value : 구현체}를 대입한다」가 이 구조를 세우는 세 줄이고, `switch` 의 `default:` 는 `get()` 결과의 `null` 검사로 옮겨졌다. 등록이 `App` 의 생성자에 남아 명령 추가 시 `App` 을 고쳐야 하는 상태이며, `put("프로젝트", new ProjectCommand("회원", ...))` 로 **키와 객체가 든 제목이 어긋난 것**과 `mainMenus` 배열이 메뉴 이름을 따로 또 들고 있는 중복은 필기에 적히지 않았다
- [[2026-08-28-action-runtime-engine]] — 워크플로 결재 커널의 Definition-Driven Dispatch. 「커널에 타입 값 비교 분기 grep 0건」 불변식, 표의 값 = 정책 데이터 + 핸들러 포인터, 미등록 키는 조용한 fallback 없이 명시 에러, 「도메인 상황 분기는 핸들러에 남는 게 정상」이라는 경계가 여기서 왔다
- [[2024-07-15-Day35]] — **표가 없어지고 순서 있는 목록으로 되돌아간다.** `Map<String, Command> commandMap` 이 `List<Menu> children` 이 되고 조회가 `children.get(menuNo - 1)` 이 되므로 열쇠가 **메뉴 이름에서 화면에 찍힌 번호**로 바뀐다. Day31 이 남긴 문제 둘이 이 이동으로 함께 풀린다 — 화면용 `mainMenus` 배열과 갈래용 맵 키의 이중 관리가 `children` 한 벌로 합쳐지고(`printMenus()` 가 같은 목록을 돈다), `HashMap` 의 순서 미보장 때문에 배열을 남겨야 했던 이유도 사라진다. 문자열 키의 근본 위험은 앞부분까지 남아 있다가(잎의 제목과 커맨드 안 `case` 가 짝이어야 한다) **커맨드를 기능 단위로 쪼개면서 없어진다** — 키로 갈래를 고르지 않게 되어서다. 그리고 `Map` 을 버렸는데도 커맨드 객체는 남아 **표와 커맨드 패턴이 서로 독립이라는 것이 확인된다**(→ [[command-pattern]]). 등록 코드가 여전히 `App` 의 생성자에 스물몇 줄로 박혀 있는 것은 그대로다
