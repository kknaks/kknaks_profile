---
type: concept
id: linked-list
title: 연결 리스트 (Linked List)
aliases:
  - 연결 리스트
  - 연결리스트
  - 링크드 리스트
  - LinkedList
  - linked list
  - 단일 연결 리스트
  - 노드
up:
  - 2024-06-25-Day22
  - 2024-06-26-Day23
  - 2024-07-08-Day30
  - 2024-07-10-Day32
tags:
  - java
  - 자료구조
  - 메모리
  - 성능
---

# 연결 리스트 (Linked List)

값 하나와 **다음 것의 주소**를 가진 상자(노드)를 줄줄이 이어 만든 목록. 메모리를 연속으로 잡지 않고 [[object-reference]] 로 순서를 표현하므로, 배열이 크기와 이동 때문에 치르던 비용을 다른 것으로 바꾼다.

## 정의

노드는 필드 두 개다.

```java
//노드의 기본구조
public class Node {
  Object value;
  Node next;

  public Node(Object value) {
    this.value = value;
  }
}
```

**`Node` 안에 `Node` 가 있는 것이 이 구조의 전부다.** 자기와 같은 타입을 필드로 갖는 첫 경험이고, 생성자가 `next` 를 채우지 않으므로 새 노드의 `next` 는 `null` 로 시작한다 → [[class]] · [[default-initialization]]

리스트 쪽은 세 가지를 들고 있다.

| 필드 | 가리키는 것 | 없으면 |
|---|---|---|
| `first` | 첫 노드 | 어디서부터 도는지 알 수 없다 |
| `last` | 마지막 노드 | 추가할 때마다 끝까지 훑어야 한다 |
| `size` | 든 개수 | 범위 검사를 못 한다 |

## 사용 예시

**추가는 「마지막 노드가 새 노드를 가리키게 만들고, 마지막 표시를 옮기는 것」**이다.

```java
public void append(Object value) {
    size++;
    Node newNode = new Node(value);
    //첫 노드의 경우 first와 last의 필드값이 null이다. 
    if (first == null) {
      first = last = newNode;
      return;
    }
    // 이후 노드는 
    last.next = newNode; //추가된 노드의 주소를 넘긴다
    last = newNode; //추가된 노드의 객체의 주소를 넘긴다
}
```

**첫 노드만 특별하다** — 이을 앞이 없으므로 `first` 와 `last` 가 같은 것을 가리킨다. 이 `if` 가 연결 리스트 코드 전체에서 반복되는 패턴이다.

**조회는 처음부터 세면서 간다.**

```java
public Object getValue(int index) {
    if (index < 0 || index >= size) {
      return null;
    }
    Node cursor = first;
    int currentIndex = 0;

    while (cursor != null) {
      if (currentIndex == index) {
        return cursor.value;
      }
      cursor = cursor.next;
      currentIndex++;
    }
    return null;
  }
```

`cursor = cursor.next` 한 줄이 「한 칸 이동」이다. 배열의 `list[index]` 가 계산 한 번이었던 것이 여기서는 **index 번 반복**이 된다 → [[linear-search]] · [[while-loop]]

**삭제는 지울 노드의 앞을 찾아 건너뛰게 만드는 것**이고, 그래서 경우가 갈린다.

```java
size--;
...
if (index == 0) {
  deletedNode = first;
  first = first.next;              // 머리를 한 칸 옮긴다
  if (first == null) {
    last = null;                   // 하나뿐이었다면 last 도 비운다
  }
  return deletedNode.value;
}

while (cursor != null) {
  if (currentIndex == index - 1) {  // 지울 것의 '앞'까지 간다
    break;
  }
  cursor = cursor.next;
  currentIndex++;
}
deletedNode = cursor.next;
cursor.next = cursor.next.next;     // 건너뛰게 잇는다
if (cursor.next == null) {
  last = cursor;                    // 꼬리를 지웠으면 last 를 당긴다
}
```

**`cursor.next = cursor.next.next` 한 줄이 삭제 전부다.** 배열에서는 뒤의 요소를 전부 한 칸 앞으로 당겨야 했던 일이 여기서 대입 한 번이 된다 → [[array-element-removal]]

### 하루 뒤, 껍데기가 채워지고 이름이 바뀐다

전날 메서드만 잘려 나와 있던 것이 다음 회차에 클래스 형태로 나타난다.

```java
public class LinkedList extends AbstractList {
  Node first;
  Node last;

  @Override
  public void add(Object value) { //생략 }

  @Override
  public Object get(int index) { //생략 }

  @Override
  public Object remove(int index) { //생략 }

  ...

  public static class Node {
    Object value;
    Node next;

    public Node(Object value) {
      this.value = value;
    }
  }
}
```

**메서드 이름 셋이 다 바뀌었다** — `append` → `add`, `getValue` → `get`, `delete` → `remove`. 기능이 달라진 것이 아니고 **`List` 인터페이스가 이름을 정했기 때문**이다. 배열 쪽 구현과 같은 이름을 써야 하나로 묶을 수 있으니, 이름을 고를 자유를 내주는 대가로 교체 가능해진다 → [[interface]] · [[method-overriding]]

**Day23 시점에 `size` 는 이 클래스에서 사라졌다.** 배열 쪽과 중복이라 `AbstractList` 의 `protected int size` 로 올라갔고, `size()` 도 거기서 한 번만 구현된다 → [[abstract-class]]

**12일 뒤에 그것이 되돌아온다.** 리팩터링 회차의 `LinkedList` 에 `int size;` 선언이 다시 있고 `size()` 도 다시 재정의되어 있다(배열 쪽도 같다). 부모의 필드는 그대로 있으므로 **한 인스턴스에 `size` 가 두 개**이고, 자식 것만 세어지고 부모 것은 `0` 으로 남는다. 밖에서 보이는 값이 정확해서 드러나지 않는 종류의 되돌림이다 → [[field-hiding]]

그리고 `Node` 가 `LinkedList` **안으로 들어가 중첩 클래스**가 되었다. 전날에는 밖에 홀로 있던 클래스다.

## 왜 중요한가

**같은 회차 3.1 의 배열 장단점 표를 뒤집어 놓은 구조다.** 배열의 단점이던 「삽입·삭제의 비효율성(O(n) 이동)」과 「고정된 크기」를 없애고, 장점이던 「O(1) 인덱스 접근」과 「연속 메모리의 캐시 효율」을 내놓는다.

| | 배열 · [[dynamic-array]] | 연결 리스트 |
|---|---|---|
| index 로 꺼내기 | 계산 한 번 | 앞에서부터 index 번 이동 |
| 중간 삽입·삭제 | 뒤를 전부 당긴다 | 참조 하나를 바꾼다 |
| 크기 | 꽉 차면 옮겨 담는다 | 필요할 때 노드 하나 |
| 메모리 | 값만 | 값 + 다음 주소 |

**「어느 쪽이 빠른가」에 답이 없고 「무엇을 자주 하는가」가 답을 정한다**는 것을 처음 겪는 자리다.

**그리고 `last` 필드가 설계 결정으로 남아 있다.** 없어도 동작하지만 `append` 마다 끝까지 훑어야 하므로 O(n) 이 된다. 필드 하나를 더 들고 다니는 대가로 추가가 O(1) 이 되는 것이고, **자료구조 설계가 「무엇을 미리 기억해 둘까」의 문제**라는 것이 여기서 드러난다 → [[caching]]

## 경계와 오해

- **연결 리스트 ≠ 메모리를 아끼는 구조** — 노드마다 `next` 참조와 객체 헤더가 붙으므로 같은 개수를 담는 데 배열보다 **더** 쓴다. 「필요할 때만 만든다」는 것은 미리 잡아 두지 않는다는 뜻이고 총량이 적다는 뜻이 아니다.
- **단일 연결이라 뒤로 갈 수 없다** — `delete` 가 `index - 1` 까지 가는 이유다. 지울 노드를 손에 들고 있어도 그 앞을 모르면 지울 수 없다. 「삭제가 O(1)」이라는 말은 **앞 노드를 이미 알고 있을 때**만 참이고, 인덱스로 지우면 찾는 데 O(n) 이 든다 → [[linear-search]]
- **`getValue` 가 「없음」과 「값이 null」을 구별하지 못한다** — 범위를 벗어나도 `null`, 찾은 값이 `null` 이어도 `null` 이다. 닷새 전 회차의 `findByNo` 가 못 찾을 때 `null` 을 준 것과 같은 형태이고, `Object` 를 담는 구조에서는 값 자체가 `null` 일 수 있어 더 아프다 → [[defensive-copy]]
- **`indexOf` 가 주소를 비교한다 — 그래서 아무것도 찾지 못한다** — 12일 뒤 회차에서 이 클래스의 `indexOf` 가 드러나는데 `cursor.value == value` 다. 그 회차의 Command 들은 `userList.indexOf(new User(userNo))` 로 조회하므로 **넘기는 객체가 목록에 든 어떤 것과도 주소가 같지 않고**, 조회·변경·삭제가 전부 「없는 회원입니다」로 끝난다. 훑는 코드는 맞는데 **비교 한 줄이 검색 전체를 무효로 만든다** → [[object-equality]] · [[linear-search]]
- **`remove` 는 개수를 먼저 줄이고 나중에 사슬을 끊는다 — 12일 뒤 코드에서 확인된다** — `size--` 가 범위 검사 직후, 노드를 찾기 **전에** 있다. 여기서는 앞의 `index` 검사가 통과했으면 반드시 지울 노드가 있으므로 결과가 맞지만, **개수와 사슬이 잠깐 어긋난 상태**가 존재하고 그 사이에 예외가 나면 `size` 만 줄어든 목록이 남는다 → [[array-element-removal]]
- **`size` 를 실제 작업보다 먼저 고친다** — `append` 와 `delete` 모두 첫 줄에서 `size++`·`size--` 를 한다. 이 코드에서는 앞에서 범위를 검사했으니 문제가 없지만, **중간에서 실패해 빠져나가면 개수만 어긋난 상태가 남는다.** 세는 것과 고치는 것 중 무엇을 먼저 할지는 판단이고, 이 필기는 세는 쪽을 먼저 택했다.
- **필드 선언과 클래스 껍데기가 Day22 필기에는 없다 — 답은 하루 뒤에 나온다** — 그날은 메서드만 잘려 나와 `first`·`last`·`size` 를 어떻게 선언했는지 알 수 없었는데, 다음 회차의 클래스 형태가 그것을 보여 준다. `Node first;`·`Node last;` 는 **접근 지정자가 없고**(package-private) `size` 는 부모의 `protected` 다. **셋 다 닫혀 있지 않다** — 같은 패키지의 다른 클래스가 `list.first.next` 로 사슬을 직접 끊을 수 있고, `Node` 의 필드도 마찬가지다 → [[access-modifier]] · [[encapsulation]]
- **`Node` 가 `static` 중첩 클래스인 것은 결정이다** — `static` 을 빼면 노드마다 **바깥 `LinkedList` 인스턴스를 가리키는 숨은 참조**가 붙어, 노드를 만들려면 리스트가 있어야 하고 노드 하나의 크기도 늘어난다. 노드는 바깥의 상태를 하나도 쓰지 않으므로 `static` 이 맞고, **「값 + 다음 주소」뿐이라는 이 구조의 성질을 지키는 것이 그 한 단어**다. 필기는 코드만 보여 주고 이 차이를 적지 않았다 → [[class]] · [[static-member]]
- **그런데 `public static class Node` 는 밖으로 열려 있다** — `LinkedList.Node` 로 밖에서 만들 수도, 받아 갈 수도 있다. `List` 인터페이스로 받으면 구현을 모르게 되는데 노드 타입은 그대로 노출되어 있어, **감추기가 한쪽에서만 되어 있다** → [[interface]] · [[encapsulation]]
- **공통 약속이 이 구조에 없던 비용을 요구한다** — `Object[] toArray()` 는 배열 구현에서는 `System.arraycopy` 한 번이지만, 연결 리스트에서는 처음부터 끝까지 훑으며 새 배열에 담아야 한다. 인터페이스로 묶을 때 **어느 구현에는 자연스럽고 어느 구현에는 억지인 메서드**가 생기고, 그 대가는 「하나로 묶어서 관리하는 것이 편리하다」에 적히지 않는다 → [[interface]] · [[array-copy]]
- **`while (cursor != null)` 이 실제 종료 조건이 아니다** — 두 루프 모두 `break` 나 `return` 으로 빠져나가고, 조건이 참인 채로 루프가 끝나는 일은 앞의 범위 검사 덕분에 생기지 않는다. **조건이 안전망으로만 남아 있는 형태**라 읽는 사람이 종료 이유를 조건에서 찾으면 어긋난다 → [[while-loop]]
- **`Object value` 는 무엇이든 담지만 꺼낼 때 되돌려야 한다** — 담는 순간 타입 정보가 사라지고, 넣은 것이 무엇인지는 코드를 쓴 사람만 안다 → [[type-casting]] · [[object-class]]
- **인덱스로 도는 반복자를 붙이면 순회가 O(n²) 이 된다** — 이틀 뒤 회차가 `AbstractList` 에 반복자를 하나 만들고 그 `next()` 를 `list.get(cursor++)` 로 쓴다. 배열 쪽에서는 순회가 O(n) 인데, 이 구조에서는 `get(index)` 가 매번 `first` 부터 `index` 칸을 걸으므로 **걸음 수가 `1 + 2 + ... + n`** 이 된다. 위 표의 「index 로 꺼내기 = index 번 이동」 한 줄이 순회 전체에 곱해지는 것이다.

  이 구조에 맞는 반복자는 `Node cursor` 를 들고 `cursor = cursor.next` 로 걷는 것이고, 그러면 `getValue` 가 하던 훑기를 **한 번만** 하게 되어 O(n) 이다. 즉 **반복자 패턴이 이 자료구조에 주려던 이득이 정확히 이것인데**, 반복자를 만드는 자리를 부모 한 곳에 두고 `get(int)` 에 기댄 코드가 그것을 놓쳤다. 「어느 쪽이 빠른가에 답이 없고 무엇을 자주 하는가가 답을 정한다」에서, **순회를 자주 하는 쪽이 이 구조를 골랐다면 반복자를 자기가 줘야 한다** → [[iterator-pattern]] · [[template-method-pattern]]
- **`java.util.LinkedList` 와 같은 이름이지만 구조가 다르다** — 표준 라이브러리 쪽은 앞뒤로 다 갈 수 있는 이중 연결이다. 이 실습은 `next` 만 있는 단일 연결이고, 그래서 뒤에서부터 세는 최적화가 불가능하다.

## 함께 보는 개념

- [[object-reference]] — 순서를 표현하는 수단
- [[array]] — 장단점이 반대인 구조
- [[dynamic-array]] — 같은 문제를 배열로 푼 쪽
- [[array-element-removal]] — 배열에서 삭제가 비싼 이유
- [[linear-search]] — 조회가 훑기가 되는 자리
- [[while-loop]] — 커서를 옮기는 반복
- [[class]] — 자기 타입을 필드로 갖는 클래스
- [[default-initialization]] — `next` 가 `null` 로 시작하는 근거
- [[type-casting]] — 꺼낸 값을 되돌리는 일
- [[object-class]] — 무엇이든 담게 해 주는 타입
- [[encapsulation]] — 노드 필드가 열려 있는 문제
- [[caching]] — `last` 를 들고 있는 판단
- [[recursion]] — 자기 참조 구조를 도는 다른 방법
- [[interface]] — 메서드 이름을 정해 주는 약속
- [[abstract-class]] — `size` 가 올라간 중간 층
- [[static-member]] — `Node` 가 `static` 인 이유
- [[field-hiding]] — `size` 가 다시 선언된 자리
- [[object-equality]] — `indexOf` 의 비교 기준
- [[iterator-pattern]] — 순회를 이 구조에서 떼어내는 방법
- [[nested-class]] — `Node` 가 이 클래스 안에 사는 문법

## 출처

- [[2024-06-25-Day22]] — 「LinkedList의 구조는 Node에 다음 Node의 레퍼런스를 가지게 함으로서 객체간에 연결을 하는 구조이다」로 시작해 `Node` 클래스, `append`·`getValue`·`delete` 를 직접 구현했다. 삭제의 세 경우(머리·중간·꼬리)를 나눠 적은 것과 `last` 를 필드로 들고 있는 것이 이 실습에서 배운 핵심이고, 앞선 3.1 의 배열 장단점 표와 3.2 의 가변 배열이 이 구조의 대조군이다
- [[2024-06-26-Day23]] — 이 구조가 `List` 인터페이스의 구현이 되면서 클래스 껍데기가 드러난다. 메서드 이름이 `append`·`getValue`·`delete` 에서 `add`·`get`·`remove` 로 바뀌고, 중복되던 `size` 는 `AbstractList` 로 올라가고, `Node` 는 `public static class` 로 `LinkedList` 안에 들어왔다. 전날 알 수 없었던 `first`·`last` 의 접근 지정자가 여기서 확인된다 — 없다
- [[2024-07-08-Day30]] — 리팩터링 회차에 이 클래스가 **전체 코드로 다시 나오면서** Day23 에 `//생략` 이던 `indexOf`·`remove`·`toArray` 가 드러난다. `indexOf` 가 `cursor.value == value` 로 주소를 비교하므로 그 회차의 조회 코드(`indexOf(new User(userNo))`)는 아무것도 찾지 못하고, `remove` 는 노드를 찾기 전에 `size--` 를 한다. 그리고 Day23 에 부모로 올려 없앴던 `int size;` 선언과 `size()` 재정의가 **다시 이 클래스에 들어와** `AbstractList.size` 가 죽었다. 실습 프로젝트의 회원·프로젝트·게시글 목록이 전부 이 클래스의 인스턴스가 되어, 이 구조가 배열 대신 저장소로 쓰이기 시작한 자리이기도 하다
- [[2024-07-10-Day32]] — 이 클래스의 코드가 **중첩 클래스의 예시로** 다시 인용되며 `public static class Node` 에 이름이 붙는다(Day23 에 이미 그 문법이었다). 새로 생긴 것은 순회 쪽이다 — `AbstractList` 에 반복자가 하나 만들어지는데 `next()` 가 `list.get(cursor++)` 이라 **이 구조에서는 순회가 O(n²)** 이 된다. 반복자를 부모 한 곳에만 두어 「자기 구조에 맞게 걷는 반복자」를 줄 여지를 쓰지 않은 것이고, `Node cursor` 를 따라 걸으면 O(n) 이 될 일이다. 인용된 코드에 `int size;` 선언이 여전히 남아 있어 Day30 의 필드 은닉도 그대로다
