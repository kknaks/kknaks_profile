---
type: concept
id: hash-based-collection
title: 해시 기반 컬렉션 (HashSet · HashMap)
aliases:
  - 해시 기반 컬렉션
  - 해시셋
  - HashSet
  - 해시맵
  - HashMap
  - hash collection
  - 집합
up:
  - 2024-06-24-Day21
  - 2024-07-09-Day31
tags:
  - java
  - 자료구조
  - 표준라이브러리
  - 성능
---

# 해시 기반 컬렉션 (HashSet · HashMap)

값을 넣을 자리를 **해시코드로 계산해서** 저장하는 컬렉션. `HashSet` 은 중복 없는 집합이고 `HashMap` 은 키에 값을 붙여 두는 표인데, **둘 다 「같은가」의 판정을 내가 만든 클래스에 물어본다.**

## 정의

판정이 두 단계로 일어난다.

| 단계 | 부르는 메서드 | 하는 일 |
|---|---|---|
| 1 | `hashCode()` | 저장할 위치(인덱스)를 계산한다 |
| 2 | `equals()` | 그 위치에 있는 것과 내용을 대조해 확정한다 |

```java
// => 값을 저장할 때 key 객체의 해시코드를 이용하여 저장할 위치(인덱스)를 계산한다.
```

그래서 **두 메서드를 함께 재정의하지 않으면 컬렉션이 제 일을 하지 못한다.** 필기가 그것을 「중복을 검사할때, equals()와 hashCode()가 모두 true일때 중복으로 간주한다」로 적었다 → [[hash-code]] · [[object-equality]]

## 사용 예시

`HashSet` 에 **내용이 똑같은 학생 둘**을 넣는다.

```java
Student s1 = new Student("홍길동", 20, false);
Student s2 = new Student("홍길동", 20, false);
Student s3 = new Student("임꺽정", 21, true);
Student s4 = new Student("유관순", 22, true);

HashSet<Student> set = new HashSet<Student>();
set.add(s1);
set.add(s2);
set.add(s3);
set.add(s4);
```

재정의하기 전에는 **중복이 그대로 남는다.**

```text
홍길동, 20, 실업중
임꺽정, 21, 재직중
홍길동, 20, 실업중
유관순, 22, 재직중
```

`Student` 에 두 메서드를 재정의하면 넷 중 하나가 사라진다.

```java
@Override
public int hashCode() {
  return Objects.hash(age, name, working);
}

@Override
public boolean equals(Object obj) {
  if (this == obj) return true;
  if (obj == null) return false;
  if (getClass() != obj.getClass()) return false;
  Student other = (Student) obj;
  return age == other.age && Objects.equals(name, other.name) && working == other.working;
}
```

```text
홍길동, 20, 실업중
임꺽정, 21, 재직중
유관순, 22, 재직중
```

**`set.add` 를 부르는 코드는 한 글자도 안 바뀌었다.** 바뀐 것은 `Student` 클래스뿐이다 → [[method-overriding]]

### HashMap 은 「키를 다시 만들어도 찾을 수 있는가」로 같은 것을 배운다

```java
MyKey k3 = new MyKey("haha");
map.put(k3, new Student("유관순", 17, true));

System.out.println(map.get(k3));         // 잘 나온다 — 넣을 때 쓴 그 인스턴스다

MyKey k6 = new MyKey("haha");            // 내용은 같고 인스턴스는 새것
System.out.println(map.get(k6));         // 엥? 값을 꺼낼 수가 없다.
```

재정의 전에는 **넣을 때 쓴 인스턴스를 계속 들고 있어야** 값을 꺼낼 수 있다. 그러면 키가 「이름」이 아니라 「그 물건 자체」인 셈이라 표로서 쓸모가 없다. 재정의한 뒤에야 `"haha"` 라는 **내용으로** 꺼낼 수 있게 된다.

### 15일 뒤 — 키를 손볼 필요가 없는 쪽

실습 프로젝트가 메뉴 이름으로 명령 객체를 찾는 표를 만든다.

```java
Map<String, Command> commandMap = new HashMap<>();

commandMap.put("회원", new UserCommand("회원", userList));
commandMap.put("게시판", new BoardCommand("게시판", boardList));
...

Command command = commandMap.get(menuTitle);
```

**`equals`·`hashCode` 이야기가 한 줄도 없는데 잘 돌아간다.** 키가 `String` 이기 때문이다 — 내용 기준 `equals` 와 `hashCode` 가 이미 재정의되어 있고 게다가 값을 바꿀 수 없다. **위의 `MyKey` 예제에서 손으로 만들어 넣어야 했던 조건을 `String` 이 처음부터 갖고 있는 것**이고, 그래서 「같은 내용으로 새로 만든 키로 꺼낼 수 있는가」가 문제조차 되지 않는다.

```java
commandMap.get(menuTitle);        // menuTitle 은 매번 다른 인스턴스일 수 있다
```

**해시 기반 컬렉션을 처음 쓸 때 `String`·`Integer` 를 키로 두면 아무 일도 안 일어나므로, 규약이 있다는 사실 자체를 모르고 지나간다** — 15일 전 회차가 `MyKey` 를 일부러 만들어 그 규약을 드러낸 이유가 여기 있다 → [[immutability]] · [[string-comparison]] · [[wrapper-class]]

값 쪽은 반대로 **내가 만든 타입**이고, 값에는 규약이 없다. 담기는 것이 인터페이스 타입이면 서로 다른 구현이 한 표에 섞여 들어가고, 꺼내서 바로 부를 수 있다 → [[dispatch-table]] · [[polymorphism]]

꺼낸 것을 받는 쪽도 눈여겨볼 자리다.

```java
Object[] list = set.toArray();          // 무엇을 넣었든 Object[] 다
for (Object obj : list) {
  Student student = (Student) obj;        // 그래서 되돌려야 필드에 닿는다
  System.out.printf("%s, %d, %s\n",
      student.name, student.age, student.working ? "재직중" : "실업중");
}
```

→ [[object-class]] · [[type-casting]]

## 왜 중요한가

**라이브러리의 동작이 내 클래스에 달려 있다는 것을 처음 만나는 자리다.** `HashSet` 코드에는 버그가 없고 `Student` 에도 컴파일 오류가 없는데 결과가 틀린다. 원인은 **내가 채워야 하는 빈칸을 비워 둔 것**이고, 그 빈칸이 상속으로 이미 채워져 있어서(기본 `equals`·`hashCode`) 비어 있는 줄도 모른다 → [[object-class]]

**그리고 Day19 의 저장소 문제에 다른 답을 준다.** 그때는 배열에 담고 `for` 로 훑어 찾았고, 중복 검사도 `contain` 을 손으로 썼다. 해시 기반 컬렉션은 **저장·중복 검사·조회를 다 가져가고** 대신 내 클래스에 두 메서드를 요구한다. 「직접 구현할 것」과 「규약을 지킬 것」이 맞바뀐 것이다 → [[linear-search]] · [[crud]]

## 경계와 오해

- **중복 제거는 컬렉션이 아니라 내 클래스가 정한다** — `HashSet` 을 쓰기만 하면 중복이 사라진다고 읽으면 필기의 첫 결과(홍길동이 둘)를 설명할 수 없다. 컬렉션이 가진 것은 **판정을 부르는 구조**이고, 판정 자체는 원소 클래스가 소유한다 → [[object-equality]]
- **`HashSet` 은 순서를 보장하지 않는다** — 필기의 출력이 삽입 순서처럼 보이는 것은 우연이다. 첫 결과에서 `s1` 과 `s2` 가 **붙어 나오지 않고 사이에 임꺽정이 끼어 있는 것**이 그 증거다 — 순서대로 담긴다면 같은 내용인 둘이 이웃해야 한다. 「집합」이라는 말 자체가 순서를 뜻하지 않는다.
- **해시코드가 같으면 같은 키라는 것은 절반이다** — 필기 3.2 의 주석 표현인데, 충돌이 있으므로 `equals` 로 확정해야 한다. 필기 자신이 그 아래에서 「hashCode()의 리턴 값이 다르고, equals() 비교 결과도 false 라면 서로 다른 key」로 **둘을 함께** 적었다. 두 문장이 어긋나 있고 아래쪽이 맞다 → [[hash-code]]
- **넣은 뒤에 필드를 바꾸면 잃어버린다** — `Student` 의 필드가 전부 열려 있으므로 `set` 에 넣은 학생의 `age` 를 바꿀 수 있다. 그러면 해시코드가 변해 **원래 자리를 다시 찾지 못하고**, 꺼낼 수도 지울 수도 없는 원소가 컬렉션 안에 남는다. 키로 쓰는 클래스는 값을 못 바꾸게 닫아야 한다 → [[encapsulation]]
- **제네릭을 썼는데도 `toArray()` 가 `Object[]` 다** — `HashSet<Student>` 로 선언했으니 `Student[]` 가 나올 것으로 읽기 쉽다. `toArray()` 의 선언이 `Object[]` 라서 그렇고, 그래서 꺼낼 때마다 다운캐스팅이 필요하다. Day19 의 `UserList.toArray()` 가 `User[]` 를 돌려준 것과 다른 이유가 여기 있다 — 그쪽은 내가 만든 메서드였다 → [[type-casting]] · [[defensive-copy]]
- **「빠르다」의 조건이 해시 함수에 달려 있다** — 모든 원소가 같은 해시코드를 준다면(예: `return 1;`) 전부 한 자리에 몰려 `equals` 를 처음부터 하나씩 부른다. 그러면 선형 탐색과 같아진다. **자료구조가 성능을 주는 것이 아니라 해시코드가 준다** → [[linear-search]]
- **`Objects.hash` 와 `Objects.equals` 는 다른 일을 한다** — 이름이 비슷하고 같은 클래스에 있어 짝처럼 보이는데, `hash` 는 **여러 값을 하나로 접고** `equals` 는 **두 값을 대조한다.** 인자 개수가 다른 것이 그 차이다.
- **키에 규약이 있는 것과 값에 규약이 있는 것은 다르다** — `equals`·`hashCode` 는 **키**에만 요구된다. 15일 뒤 회차의 `Map<String, Command>` 에서 `Command` 구현들은 두 메서드를 아무것도 재정의하지 않았고 그럴 필요도 없다. 「해시 기반 컬렉션을 쓰면 원소 클래스가 규약을 지켜야 한다」를 `HashMap` 의 값에까지 적용하면 필요 없는 코드를 쓰게 된다 — `HashSet` 쪽은 원소가 곧 키라서 그 구별이 안 보인다 → [[hash-code]]
- **`Map` 을 「분기 대신」 쓰는 것은 자료구조가 아니라 제어 흐름의 결정이다** — 15일 뒤 회차가 문자열 `switch` 다섯 갈래를 `commandMap.get()` 한 줄로 바꾼다. 표에 담기는 것이 **데이터가 아니라 실행할 것**이므로, 「어떤 키가 등록되어 있나」가 곧 「무엇이 실행될 수 있나」다. 자료구조를 고른 것으로 보이지만 **분기 목록의 소유자를 코드에서 데이터로 옮긴 것**이다 → [[dispatch-table]] · [[switch-statement]]
- **표의 순회 순서로 화면을 만들 수 없다** — `HashMap` 은 순서를 기억하지 않으므로 메뉴를 등록 순서대로 찍으려면 `LinkedHashMap` 이나 별도 목록이 필요하다. 15일 뒤 회차가 `String[] mainMenus` 를 계속 들고 있는 실제 이유가 여기인데(필기는 적지 않았다), 그 대가로 **메뉴 이름이 배열과 표의 키 두 곳에 남아** 한쪽만 고치면 조용히 어긋난다 → [[open-closed-principle]]
- **필기 3.1 의 코드 블록은 닫히지 않은 채로 잘려 있다** — `for` 루프와 `main` 의 닫는 중괄호가 없고 주석 블록에서 끝난다. 3.2 의 마지막 블록도 `equals` 중간에서 끊긴다. 실행 결과는 주석으로 남아 있으므로 읽는 데는 지장이 없지만 **그대로는 컴파일되지 않는다.**

## 함께 보는 개념

- [[hash-code]] — 위치를 계산하는 재료
- [[object-equality]] — 위치에서 확정하는 판정
- [[object-class]] — 두 메서드가 물려 내려오는 곳
- [[method-overriding]] — 컬렉션에 내 규칙을 넣는 방법
- [[linear-search]] — 이 구조가 대체하는 조회 방식
- [[type-casting]] — `Object[]` 로 나온 것을 되돌리는 일
- [[array]] — 안쪽에서 자리를 세는 저장소
- [[crud]] — 손으로 만들던 저장소 연산
- [[defensive-copy]] — 목록을 사본으로 내주는 같은 발상
- [[search-index]] — 같은 아이디어의 저장소 층
- [[encapsulation]] — 키의 값을 잠가야 하는 이유
- [[immutability]] — `String` 키가 규약을 저절로 만족하는 근거
- [[dispatch-table]] — 값에 실행할 것을 담는 쓰임
- [[switch-statement]] — 표가 대체하는 제어 흐름
- [[polymorphism]] — 여러 구현이 한 표에 섞여도 되는 이유

## 출처

- [[2024-06-24-Day21]] — `HashSet` 에 내용이 같은 `Student` 둘을 넣어도 `equals`·`hashCode` 를 재정의하기 전에는 중복이 남고, 재정의하면 하나로 합쳐지는 것을 실습했다. `HashMap` 에서는 같은 내용으로 새로 만든 키(`k6`)로 값을 꺼낼 수 없다가 재정의 후 꺼낼 수 있게 되는 것으로 같은 규약을 배웠다. 「값을 저장할 때 key 객체의 해시코드를 이용하여 저장할 위치를 계산한다」와 「중복을 검사할때 equals()와 hashCode()가 모두 true일때 중복으로 간주한다」도 이 자리다
- [[2024-07-09-Day31]] — `HashMap` 을 **분기 대신** 쓰는 첫 자리다. 실습 프로젝트의 `App` 이 `Map<String, Command> commandMap` 에 {메뉴명 → 명령 객체}를 담아 문자열 `switch` 다섯 갈래를 `commandMap.get(menuTitle)` 조회로 바꿨다(「put메서드를 이용하여 {Key : 메뉴명, Value : 구현체}를 대입한다」). 15일 전 회차가 `MyKey` 로 힘들게 드러낸 `equals`·`hashCode` 규약이 여기서는 **한 줄도 나오지 않는데 잘 돌아간다** — 키가 `String` 이라 내용 기준 비교와 불변성을 이미 갖고 있기 때문이고, 값에는 애초에 그 규약이 요구되지 않는다. 순서를 기억하지 않는 성질 때문에 메뉴 이름이 `mainMenus` 배열에 한 벌 더 남았다
