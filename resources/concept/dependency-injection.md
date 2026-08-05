---
type: concept
id: dependency-injection
title: 의존성 주입 (Dependency Injection)
aliases:
  - DI
  - 의존성 주입
  - 의존 주입
  - dependency injection
  - 생성자 주입
  - constructor injection
up:
  - 2024-07-09-Day31
tags:
  - 설계
  - 객체지향
  - 결합도
  - 생성
---

# 의존성 주입 (Dependency Injection)

**어떤 객체가 필요한 다른 객체를 스스로 만들지 않고, 밖에서 만들어 넣어 주는 것.** 필기의 두 줄이 그 전부다 — 「인터페이스를 직접적으로 생성하지 않는다( = 의존객체를 만들지 않는다.) / 외부에서 객체를 생성해서 대입을 받는다」.

## 정의

바뀌는 것은 `new` **한 줄이 어디에 있는가**다.

```java
class Switch {
  Switchable device = new FluoLamp();   // 스스로 만든다 — 주입 아님
}
```

```java
class Switch {
  Switchable device;
  Switch(Switchable device) {           // 밖에서 받는다 — 생성자 주입
    this.device = device;
  }
}
```

받는 경로가 셋이고, 이 회차는 첫 번째만 쓴다.

| 경로 | 형태 | 성질 |
|---|---|---|
| **생성자 주입** | `new Switch(lamp)` | 만들어진 순간부터 완전하다. 바꿀 수 없게 둘 수 있다 |
| 세터 주입 | `sw.setDevice(lamp)` | 나중에 갈아 끼울 수 있다. 넣기 전 상태가 존재한다 |
| 메서드 주입 | `sw.turnOn(lamp)` | 호출마다 다른 것을 줄 수 있다. 들고 있지 않는다 |

**「누가 만드나」와 「누가 쓰나」를 갈라 놓는 것**이 공통이고, 그래서 만드는 책임이 위로 모인다 → [[grasp]]

## 사용 예시

이 회차의 실습이 목록 객체를 주입하는 쪽으로 옮긴다. 하루 전까지는 각 명령이 자기 목록을 스스로 만들었다.

```java
public class UserCommand extends AbstractCommand {
  LinkedList userList = new LinkedList();   // 자기가 만든다
  ...
  public LinkedList getUserList() { return userList; }
}
```

그래서 팀원 목록이 필요한 `ProjectCommand` 는 **다른 명령에게 목록을 얻어 와야** 했다 — `new ProjectCommand("프로젝트", userCommand.getUserList())`. 필기가 그 상태를 「App()의 List와 Command의 List 다른 객체를 참조하여 상호 호환이 불가하였다」로 적었다.

수정은 목록의 소유자를 `App` 으로 올리는 것이다.

```java
ArrayList userList = new ArrayList();
LinkedList projectList = new LinkedList();
LinkedList noticeList = new LinkedList();
ArrayList boardList = new ArrayList();

public App() {
  commandMap.put("회원", new UserCommand("회원", userList));
  commandMap.put("게시판", new BoardCommand("게시판", boardList));
  commandMap.put("공지사항", new BoardCommand("공지사항", noticeList));
  commandMap.put("프로젝트", new ProjectCommand("회원", projectList, userList));
  commandMap.put("도움말", new HelpCommand());
}
//각 Command에서 생성자도 수정
```

**같은 `userList` 인스턴스가 `UserCommand` 와 `ProjectCommand` 에 둘 다 들어간다.** 회원 메뉴에서 등록한 사람이 프로젝트 팀원 목록에서 보이게 되는 것이 이 이동의 목적이고, 「누가 만드나」를 한 곳으로 올린 것이 그것을 가능하게 했다 → [[object-reference]]

그리고 **저장소 종류를 명령 밖에서 고를 수 있게 되었다** — 회원과 게시판은 `ArrayList`, 프로젝트와 공지사항은 `LinkedList` 다. 명령 코드는 어느 쪽이 오는지 모른다(적어도 타입이 `List` 라면. 아래) → [[interface]] · [[dynamic-array]] · [[linked-list]]

## 왜 중요한가

**공유해야 하는 것을 공유할 수 있게 된다.** 이 실습이 실제로 풀려던 문제가 그것이다. 각자 `new` 하면 각자 다른 인스턴스가 생기고, 그러면 「회원 목록」이 프로그램 안에 여러 개 존재한다. **누가 만드는지를 안 정하면 몇 개 있는지도 안 정해진다** → [[instance]]

**갈아 끼울 수 있게 된다.** 안에서 `new` 하는 코드는 그 클래스를 바꾸지 않고는 다른 구현을 쓸 수 없다. 밖에서 받으면 부르는 쪽이 고른다 — 그것이 [[dependency-inversion-principle]] 의 두 번째 걸음이고, DIP 가 「인터페이스로 받는다」에서 끝나지 않는 이유다.

**만드는 순서와 쓰는 순서가 분리된다.** 주입하는 구조에서는 프로그램이 시작할 때 필요한 것을 다 만들고 이어 붙이는 구간과 그것을 돌리는 구간이 갈린다. 이 실습의 `App` 생성자가 앞의 것이고 `execute()` 가 뒤의 것이다 — **뒤쪽에 `new` 가 없다는 것이 그 분리가 됐다는 신호**다.

## 경계와 오해

- **의존성 주입 ≠ 의존 역전 원칙** — 필기가 「DIP를 적용하여 외부에서 값을 대입하면 의존성을 탈피 할 수 있다」로 둘을 한 문장에 묶었지만 축이 다르다. DIP 는 **무엇에 기대는가**(추상 대 구체), DI 는 **누가 넣어 주는가**(자기 대 외부)다. 네 조합이 다 존재한다 — `LinkedList projectList` 를 생성자로 받는 이 회차의 코드는 **DI 는 했고 DIP 는 안 한 것**이다(구현 클래스 타입으로 받는다). 반대로 인터페이스 타입 필드를 안에서 `new` 하면 DIP 만 반쪽 한 것이다 → [[dependency-inversion-principle]]
- **필기가 이것을 OCP 라 적었다** — 「App()에서 List를 생성하고 매개변수로 Comman에 넘긴다.(OCP원칙)」. 무엇이 「수정에 닫혔는지」를 세어 보면 답이 없다 — 오히려 `App` 이 목록 넷을 알게 되었으므로 `App` 쪽은 더 열렸다. 이 이동으로 닫힌 것은 없고 **`Command` 가 저장소 종류를 모르게 된 것**이 얻은 것이며, 그것의 이름이 DI 다 → [[open-closed-principle]]
- **주입한다고 의존이 줄지 않는다 — 위로 올라간다** — `UserCommand` 가 `LinkedList` 를 모르게 된 대신 `App` 이 `ArrayList`·`LinkedList`·명령 넷·목록 넷을 다 안다. 이 실습에서 `App` 은 **가장 많이 아는 클래스**가 되었고, 그것이 정상이다 — 의존을 없애는 것이 아니라 **아는 자리를 하나로 모으는 것**이 목적이고, 프레임워크에서 그 자리를 설정이나 컨테이너로 밀어내는 것이 다음 걸음이다 → [[coupling]]
- **「외부」가 한 칸 위일 뿐이다** — `App` 은 여전히 자기 의존을 스스로 `new` 한다. 램프 예제 5단계의 「외부에서 객체를 생성해서 대입을 받는다」를 끝까지 밀면 `App` 도 명령 목록을 받아야 하고, 그러면 그 밖의 누군가가 필요하다. **주입은 사슬이라 어딘가에는 `new` 를 하는 최상단이 있어야 하며**, 그 자리를 어디로 둘지가 결정이다 → [[main-method]]
- **이 회차의 첫 시도가 바로 그 문제로 실패한다** — 2단계의 생성자 코드에 `UserCommand` 가 **두 번** 만들어진다.

  ```java
  commandMap.put("회원", new UserCommand("회원"));          // ① 맵에 든 것
  ...
  UserCommand userCommand = new UserCommand("회원");         // ② 지역 변수
  commandMap.put("프로젝트", new ProjectCommand("회원", userCommand.getUserList()));
  ```

  회원 메뉴에서 등록하는 사람은 ①의 목록에 들어가고 `ProjectCommand` 가 팀원을 찾는 곳은 ②의 목록이다. **②는 맵에 없으므로 영원히 비어 있고**, 팀원 추가는 언제나 「없는 팀원입니다」로 끝난다. 필기가 바로 위에 문제로 적어 둔 「App()의 List와 Command의 List 다른 객체를 참조하여 상호 호환이 불가하였다」를 **고치는 절의 코드에서 다시 만든 것**이고, 4단계에서 `App` 이 목록을 소유하게 되어야 해소된다 → [[instance]] · [[object-reference]]
- **그 실패가 이미 다른 이유로 가려져 있다** — 하루 앞 회차에서 `indexOf` 가 `equals` 대신 `==` 로 비교하게 되어 목록 조회가 전부 실패하는 상태다. 그래서 위 인스턴스 두 개 문제를 고쳐도 팀원 추가는 여전히 「없는 팀원입니다」다. **죽은 기능 위에 새 단절이 얹혀 증상이 같아진 것**이고, 증상으로 원인을 찾을 수 없는 상태를 만든다 → [[object-equality]]
- **주입한 것을 그대로 들고 있으면 밖에서도 만질 수 있다** — `App` 이 만든 `userList` 를 두 명령에 넘기는 것은 **공유가 목적**이라 맞지만, 같은 참조를 넘기는 것과 사본을 넘기는 것은 다른 결정이다. 공유가 목적이 아닌 값을 이렇게 넘기면 한쪽의 변경이 다른 쪽에 새어 나간다 → [[defensive-copy]] · [[call-by-value]]
- **넘기는 타입을 구현 클래스로 쓰면 주입의 이득이 반쪽이 된다** — 이 코드는 `ArrayList userList` · `LinkedList projectList` 를 그 타입 그대로 넘긴다. 13일 앞 회차에 `List` 인터페이스를 만들어 두었으므로 `List` 로 받으면 저장소를 바꿀 때 명령 코드가 안 바뀌는데, 지금은 `UserCommand` 의 생성자 시그니처에 `ArrayList` 가 박힌다. 게시글 목록이 `ArrayList` 에서 `LinkedList` 로 바뀌는 날 명령 클래스를 고쳐야 한다 → [[interface]]
- **`ProjectCommand` 에 넘긴 제목이 「회원」이다** — 4단계 코드가 `new ProjectCommand("회원", projectList, userList)` 다. 맵의 키는 「프로젝트」인데 객체가 들고 있는 제목은 「회원」이므로, 프로젝트 메뉴에 들어가면 화면에 `[회원]` 이 찍히고 같은 노트 뒤쪽에서 만드는 경로 표시도 `메인/회원` 이 된다. **같은 사실(메뉴 이름)이 맵의 키와 생성자 인자 두 곳에 적혀 어긋난 것**이고, 컴파일러는 두 문자열이 같아야 한다는 것을 모른다 → [[dispatch-table]]

## 함께 보는 개념

- [[dependency-inversion-principle]] — 주입이 두 번째 걸음으로 들어가는 원칙
- [[solid-principles]] — 이 이동이 놓인 원칙 묶음
- [[open-closed-principle]] — 필기가 이 이동에 잘못 붙인 이름
- [[constructor]] — 주입을 받는 자리
- [[instance]] — 몇 개 만들어지는지가 결정되는 문제
- [[object-reference]] — 같은 목록을 나눠 갖는다는 것의 실제 내용
- [[interface]] — 무엇으로 받을지를 정하는 축
- [[coupling]] — 의존이 옮겨 간 것을 세는 축
- [[dispatch-table]] — 이 회차가 명령을 등록하는 자리
- [[defensive-copy]] — 공유가 목적이 아닐 때의 반대 선택
- [[grasp]] — 「만들 책임을 누가 갖나」(Creator)를 다루는 쪽
- [[main-method]] — 주입 사슬의 최상단이 놓이는 자리

## 출처

- [[2024-07-09-Day31]] — 램프/스위치 예제 5단계에서 「인터페이스를 직접적으로 생성하지 않는다( = 의존객체를 만들지 않는다) / 외부에서 객체를 생성해서 대입을 받는다」로 이 개념을 배우고, 실습에서 각 `Command` 가 스스로 만들던 목록을 `App` 이 만들어 생성자로 넘기는 쪽으로 옮겼다(「App()에서 List를 생성하고 매개변수로 Comman에 넘긴다」). 그 과정에서 2단계 코드가 `UserCommand` 를 두 번 만들어 `ProjectCommand` 가 맵에 없는 인스턴스의 목록을 받는 상태를 만들고, 4단계에서 `App` 이 목록을 소유하며 해소된다. 넘기는 타입이 `List` 가 아니라 `ArrayList`·`LinkedList` 구현 클래스이고, `ProjectCommand` 의 제목 인자가 「회원」으로 잘못 들어가 있다. 필기는 이 이동을 DIP 와 「(OCP원칙)」 두 이름으로 부르며 DI 라는 이름은 쓰지 않았다
