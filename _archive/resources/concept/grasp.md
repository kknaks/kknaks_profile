---
type: concept
id: grasp
title: GRASP (책임을 어느 객체에 맡길지 고르는 지침)
aliases:
  - GRASP
  - 책임 할당
  - 책임 할당 패턴
  - General Responsibility Assignment Software Patterns
  - 그래스프
up:
  - 2024-06-20-Day19
  - 2024-07-08-Day30
tags:
  - 설계
  - 객체지향
  - 방법론
  - 유지보수
---

# GRASP (책임을 어느 객체에 맡길지 고르는 지침)

객체지향 설계에서 **「이 일을 누가 해야 하나」를 고르는 아홉 개의 지침 묶음.** 클래스를 어떻게 만드느냐가 아니라 이미 있는 일을 **어느 객체에 붙일 것인가**를 다룬다.

## 정의

| 지침 | 내용 |
|---|---|
| Information Expert (정보 전문가) | 그 일에 필요한 정보를 가진 객체에게 일을 준다 |
| Creator (생성자) | 객체를 만들 책임을, 만들어질 객체와 밀접한 객체에게 준다 |
| Controller (컨트롤러) | 시스템 이벤트를 받아 주요 제어 흐름을 담당하는 자리를 둔다 |
| Low Coupling (낮은 결합도) | 객체 사이 의존을 최소화한다 |
| High Cohesion (높은 응집도) | 한 객체의 책임을 하나의 주제로 결집한다 |
| Polymorphism (다형성) | 타입에 따라 갈리는 처리를 각 타입에게 넘긴다 |
| Pure Fabrication (순수 가공) | 설계 문제를 풀기 위해 도메인에 없는 클래스를 만든다 |
| Indirection (간접화) | 두 객체를 직접 잇지 않고 중간을 둔다 |
| Protected Variations (변화 보호) | 변할 부분을 감싸 외부 영향을 줄인다 |

**첫 번째와 다섯 번째는 사실상 한 방향이다** — 「정보를 가진 쪽에 일을 준다」를 지키면 그 클래스의 메서드들이 자기 필드를 다루는 것으로 모인다 → [[cohesion]]

그리고 넷째와 다섯째는 **서로 당긴다.** 응집도를 높이려 클래스를 쪼개면 클래스 사이 호출이 늘어나 결합이 생긴다. 아홉 개는 체크리스트가 아니라 **저울**이다.

## 사용 예시

이 회차는 아홉 개 중 **High Cohesion 하나**를 실제 코드에 적용했다. 한 클래스가 두 역할을 하고 있던 것을 찾아내는 것이 시작이다.

```java
public class ProjectCommand {
  //데이터보관 필드
  private static final Project[] projects = new Project[MAX_SIZE];
  private static int projectLength = 0;

  //UI처리 메서드
  private static void addProject() {}
  private static void listProject() {}
  ...
  //데이터처리 메서드
  private static Project findByNo(int projectNo) {}
  private static int indexOf(Project project) {}
}
```

필기의 진단이 정확하다 — 「서브메뉴들의 흐름제어 + 데이터보관처리」. 그래서 둘로 갈랐다.

```java
public class ProjectList {        // 데이터를 보관하고 처리한다
  private static final Project[] projects = new Project[MAX_SIZE];
  private static int projectLength = 0;
  private static Project findByNo(int projectNo) {}
  private static int indexOf(Project project) {}
}

public class ProjectCommand {     // 입력받고 순서를 정한다
  public static void excuteProjectCommand(String command){}
  private static void addProject() {}
  ...
}
```

**여기서 이름 붙지 않은 두 번째 지침이 같이 일어났다.** `ProjectList`·`UserList` 는 **도메인에 없는 클래스**다 — 이 프로그램의 도메인은 회원·프로젝트·게시글이고 「회원목록」이라는 것은 현실에 대응물이 없다. 설계 문제를 풀기 위해 만든 것이므로 **Pure Fabrication** 이다. 필기는 High Cohesion 만 이름 붙였지만, 응집도를 올리려는 시도가 **없던 클래스를 하나 만들어 내는 것**으로 끝난 것이 아홉 개가 맞물려 있다는 증거다.

세 번째 자리도 이미 코드에 있다.

```java
public static void executeUserCommand(String command) {      // Controller
  switch (command) {
    case "등록": addUser(); break;
    ...
  }
}
```

명령 문자열을 받아 갈래로 보내는 이 메서드가 컨트롤러이고, 필기는 이것을 「UI처리 메서드」로 부른다 → [[crud]] · [[command-loop]]

### 18일 뒤 같은 지침을 다시 쓰고, 다음 칸을 비워 둔다

리팩터링 회차는 High Cohesion 을 **두 번째로** 적용한다. 옮긴 것이 데이터가 아니라 흐름 제어라 단위가 올라갔고(→ [[cohesion]]), 그 결과 세 Command 에 같은 코드가 생겨 상속으로 되감는다(→ [[generalization]]).

**그 과정에서 목록의 세 지침이 움직인다.**

| 지침 | 이 회차에서 |
|---|---|
| High Cohesion | 두 번째 적용 — 대상이 필드에서 메뉴로 |
| Pure Fabrication | **회수된다** — `UserList` 가 사라지고 목록이 `LinkedList` 인스턴스로 돌아간다 |
| Polymorphism | **적용될 자리에 도착했는데 적용되지 않는다** |

마지막 줄이 이 회차의 빈칸이다. `Command` 인터페이스를 만들고 `AbstractCommand` 까지 만들었으므로 **네 명령을 한 타입으로 담을 수 있는 상태**인데, `App` 은 여전히 구현 클래스 넷을 각각 필드로 들고 문자열 `switch` 로 갈래를 낸다.

```java
UserCommand userCommand = new UserCommand("회원");
BoardCommand boardCommand = new BoardCommand("게시판");
...
switch (menuTitle) {
  case "회원": userCommand.execute(); break;      // 타입에 따라 갈리는 분기가 남아 있다
  case "게시판": boardCommand.execute(); break;
  ...
}
```

목록의 Polymorphism 이 말하는 것이 정확히 이것이다 — **타입에 따라 갈리는 `switch` 를 각 타입에게 넘기라.** 넘길 대상(`processMenu`)은 이미 각 Command 안에 있으므로 남은 일은 `App` 이 `Command` 배열 하나를 들고 도는 것뿐이었다 → [[polymorphism]] · [[interface]]

## 왜 중요한가

**「그냥 이게 나은 것 같다」와 「응집도 문제다」는 다르게 다뤄진다.** 판단 기준에 이름이 붙으면 남에게 설명할 수 있고, 반박도 같은 축에서 온다. 이름이 없으면 클래스를 쪼갠 이유가 취향으로 남고, 다음 사람이 다시 합쳐도 근거를 댈 수 없다.

**무엇을 보고 쪼갤지가 정해진다.** 이 회차의 실제 작업은 「메서드 목록을 보고 필드를 읽는 것과 화면을 다루는 것을 가르기」였다. 기준이 「파일이 길다」가 아니라 **「무엇을 읽는가」**여서, 어디를 자를지가 세는 일 없이 나왔다 → [[cohesion]]

**그리고 하나를 지키면 다른 하나가 나빠진다는 것을 미리 안다.** 클래스를 둘로 쪼갠 대가로 `UserCommand` 가 `UserList` 라는 이름을 알게 되었다 — 결합이 늘었다. 그것이 나쁜 거래가 아니라는 판단까지가 설계이고, 아홉 개를 나란히 두는 이유가 그 거래를 보이게 하는 것이다.

## 경계와 오해

- **GRASP ≠ 디자인 패턴(GoF)** — 둘 다 「패턴」이라 부르지만 답의 모양이 다르다. GoF 는 **구조의 이름**(Strategy·Observer)을 주고 클래스 도식으로 답하며, GRASP 는 **질문**을 준다(「이 정보를 누가 갖고 있나」). GRASP 를 적용해도 만들어지는 클래스 모양은 매번 다르다.
- **GRASP 의 Creator 는 자바의 생성자가 아니다** — 필기가 「Creator (생성자)」로 번역해 두었는데 이 지침은 **누가 `new` 를 부를 책임을 갖는가**이고, `constructor` 문법과는 다른 층의 이야기다. 이 코드에서 Creator 는 `new User()` 를 부르는 `UserCommand.addUser` 다 → [[constructor]]
- **Polymorphism 이 목록에 있는 것은 문법 이야기가 아니다** — 「다형성을 쓰라」가 아니라 **타입에 따라 갈리는 `if`·`switch` 를 각 타입에게 넘기라**는 배치 지침이다. 문법을 아는 것과 그것을 책임 분배로 쓰는 것은 따로 배워야 한다 → [[polymorphism]]
- **아홉 개를 다 적용하는 것이 목표가 아니다** — 이 회차는 하나를 적용했고 그것만으로 클래스가 두 개로 갈렸다. 나머지 여덟 개는 **이름만 아는 상태**이고, 그중 Pure Fabrication 은 이름을 모르는 채로 실행됐다.
- **Low Coupling 은 이 회차에서 오히려 늘었다** — `UserCommand` 가 `UserList.add`·`toArray`·`findByNo`·`delete` 를 클래스 이름으로 직접 부른다. 목록에는 「의존성을 최소화」라고 적혀 있지만 실제 코드는 반대로 갔고, **그 대가를 치를 만했는지는 이 회차에서 판단되지 않았다.** 판단할 도구가 보름 뒤에 온다 — 인터페이스 회차가 「호출자가 무엇을 아는가」로 이 축을 세는 법을 준다 → [[static-member]] · [[coupling]]
- **클래스를 쪼개면 접근 지정자를 다시 정해야 한다** — 필기 「High Cohesion」 절의 `ProjectList` 초안은 `findByNo`·`indexOf` 를 `private static` 으로 그대로 옮겨 두었는데, 그러면 `ProjectCommand` 에서 부를 수 없어 분리한 의미가 사라진다. 「클래스 분리하기」 절의 `UserList` 에서는 `public static` 이 되었다. **한 클래스 안에서의 `private` 은 쪼개는 순간 뜻이 바뀐다** → [[access-modifier]]
- **필기의 영문 이름이 틀렸다** — `General Responsibility Assignment SofeWare Patters` 로 적혀 있는데 `Software Patterns` 다. 약어를 만드는 원문이라 찾아볼 때 걸린다.
- **Generalization 은 이 목록에 없다** — 18일 뒤 회차가 「리팩토링: GRASP의 High Cohesion」 다음 절을 「리팩토링: 상속의 Generalization 적용」으로 두어 **열 번째 지침처럼** 읽히는데, 아홉 개에 그런 항목은 없다. Generalization 은 **UML 에서 상속 관계를 부르는 이름**이고, 그래서 그 절이 UML 다이어그램과 짝인 것이다. 「GRASP 를 계속 적용하는 중」으로 읽으면 이 목록에 없는 것을 찾게 된다 → [[generalization]]
- **아홉 개는 순서가 없지만 서로를 불러온다** — 이 필기의 두 회차가 그것을 보여 준다. High Cohesion 을 적용하니 Pure Fabrication 이 딸려 왔고(Day19), 다시 적용하니 중복이 생겨 상속이 필요해졌고(Day30), 그 결과 Polymorphism 을 적용할 조건이 갖춰졌다. **하나를 고르는 것이 다음 후보를 정한다** — 체크리스트로 훑는 것과 다른 쓰임이다 → [[refactoring]]
- **적용 조건이 갖춰진 것과 적용한 것은 다르다** — Day30 은 `Command` 인터페이스와 `AbstractCommand` 를 만들어 네 명령을 한 타입으로 다룰 수 있게 해 놓고도 `App` 의 `switch` 를 남겼다. **지침을 「알고 있다」와 「그 자리에서 떠올린다」 사이의 거리**가 여기서 보이고, 그것이 목록을 외우는 것으로 줄지 않는다는 것도 같이 보인다 → [[polymorphism]]
- **책임을 옮기는 것과 코드를 옮기는 것은 다르다** — 메서드를 다른 클래스에 복사해 넣으면 코드는 옮겨졌지만, **그 규칙이 틀렸을 때 고칠 자리가 어디인가**가 바뀌는 것이 책임 이동이다. 이 회차에서 회원 목록의 규칙(어떻게 세고 어떻게 지우나)의 소유자가 `UserList` 가 되었다 → [[cohesion]]

## 함께 보는 개념

- [[cohesion]] — 아홉 개 중 이 회차가 실제로 적용한 것
- [[class]] — 책임이 붙는 단위
- [[method]] — 옮겨지는 대상
- [[package]] — 갈라진 클래스를 묶는 상위 단위
- [[polymorphism]] — 목록에 있는 또 다른 배치 지침
- [[constructor]] — Creator 와 혼동되는 문법
- [[access-modifier]] — 쪼갠 뒤 다시 정해야 하는 것
- [[encapsulation]] — 변화 보호가 기대는 장치
- [[crud]] — 컨트롤러가 갈래로 보내는 대상
- [[generalization]] — 이 목록 밖에서 이어 붙은 UML 쪽 이름
- [[refactoring]] — 지침이 하나씩 불려 나오는 작업의 단위
- [[interface]] — Polymorphism 을 적용할 조건을 만드는 장치

## 출처

- [[2024-06-20-Day19]] — GRASP 아홉 개 지침을 한 줄씩 정리하고, 그중 High Cohesion 을 실습 프로젝트에 적용해 `ProjectCommand`·`UserCommand` 를 데이터 보관 클래스(`ProjectList`·`UserList`)와 UI 처리 클래스로 갈랐다. 그 과정에서 도메인에 없는 목록 클래스를 만든 것이 Pure Fabrication 이라는 것, 그리고 `private` 이던 탐색 메서드를 `public` 으로 열어야 했던 것도 이 자리에서 나왔다
- [[2024-07-08-Day30]] — High Cohesion 을 **두 번째로** 적용해 `App` 의 서브메뉴 흐름을 각 `Command` 로 옮기고, 그 결과 생긴 중복을 상속으로 되감았다. Day19 가 만든 Pure Fabrication(`UserList`)은 범용 자료구조가 생기면서 회수되고, **Polymorphism 은 적용 조건이 다 갖춰진 상태로 비어 남는다** — `Command` 인터페이스와 `AbstractCommand` 가 있는데 `App` 은 구현 클래스 넷을 필드로 들고 문자열 `switch` 로 갈래를 낸다. 필기가 다음 절 제목을 「상속의 Generalization」으로 붙여 아홉 개에 없는 항목이 목록에 이어지는 것처럼 보이게 만든 자리이기도 하다
