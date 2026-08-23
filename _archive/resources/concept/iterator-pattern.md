---
type: concept
id: iterator-pattern
title: 반복자 패턴 (Iterator Pattern)
aliases:
  - 반복자
  - 반복자 패턴
  - 이터레이터
  - 이터레이터 패턴
  - Iterator
  - Iterator 패턴
  - iterator pattern
  - hasNext
  - 커서 객체
up:
  - 2024-07-10-Day32
tags:
  - 설계
  - 디자인패턴
  - 자료구조
  - 자바
---

# 반복자 패턴 (Iterator Pattern)

**「어디까지 봤나」를 세는 변수를 호출부에서 빼내 객체 하나에 담고, 순회를 그 객체에게 물어보는 것.** 컬렉션이 배열이든 노드 사슬이든 호출부가 쓰는 것은 `hasNext()` · `next()` 두 개뿐이 되고, 컬렉션의 내부 구조는 그 객체 안에서만 쓰인다.

## 정의

세 조각으로 나뉜다.

| 조각 | 이 실습에서 | 하는 일 |
|---|---|---|
| **반복자 약속** | `interface Iterator { boolean hasNext(); Object next(); }` | 순회의 사용 규칙 |
| **반복자 구현** | `class ListIterator implements Iterator` | 커서를 들고 실제로 꺼낸다 |
| **반복자를 내주는 자리** | `List.iterator()` | 컬렉션에게 「하나 만들어 줘」 |

```java
public interface Iterator {
  boolean hasNext();
  Object next();
}
```

**바뀌는 것은 커서가 사는 곳이다.**

| 순회 방법 | 호출부가 알아야 하는 것 | 커서(`i`·`cursor`)가 사는 곳 |
|---|---|---|
| 인덱스 `for` | `size()` · `get(int)` | 호출부 |
| `toArray()` + for-each | 배열이라는 것 | 호출부(문법이 숨긴다) |
| **반복자** | `hasNext()` · `next()` | **반복자 객체** |

`hasNext()` 는 상태를 바꾸지 않고 `next()` 만 커서를 옮긴다 — `list.get(cursor++)` 의 `++` 가 그 한 곳이다. 그래서 `hasNext()` 는 몇 번 불러도 되고, `next()` 를 부르기 전에 물어야 한다 → [[increment-operator]]

## 사용 예시

바꾸기 전의 목록 출력은 **사본 배열을 받아 for-each 로 돌았다.**

```java
//BoardCommand
private void listBoard() {
    System.out.println("번호 제목 작성일 조회수");
    for (Object obj : boardList.toArray()) {
    Board board = (Board) obj;
    System.out.printf("%d %s %tY-%3$tm-%3$td %d\n",
        board.getNo(), board.getTitle(), board.getCreatedDate(), board.getViewCount());
    }
}
```

반복자를 만들고 나면 사본이 사라지고 루프가 `while` 이 된다.

```java
private void listBoard() {
    System.out.println("번호 제목 작성일 조회수");
    Iterator iterator = boardList.iterator();
    while (iterator.hasNext()) {
    Board board = (Board) iterator.next();
    System.out.printf("%d %s %tY-%3$tm-%3$td %d\n", board.getNo(), board.getTitle(),
        board.getCreatedDate(), board.getViewCount());
    }
}
```

구현체는 컬렉션과 커서를 들고 있는 것이 전부다.

```java
public class ListIterator implements Iterator {
  private List list;
  private int cursor;

  public ListIterator(List list) {
    this.list = list;
  }

  @Override
  public boolean hasNext() {
    return cursor < list.size();
  }

  @Override
  public Object next() {
    return list.get(cursor++);
  }
}
```

그리고 **반복자를 내주는 메서드는 자식이 아니라 중간의 추상 클래스에 놓였다.**

```java
// list 인터페이스 변경
public interface List {
  ...
  Iterator iterator();
}

// AbstractList 변경
public abstract class AbstractList implements List {
  @Override
  public Iterator iterator() {
    return new ListIterator(this);
  }
}
```

**`ArrayList` 와 `LinkedList` 는 한 줄도 바뀌지 않았다.** 약속에 메서드를 하나 더했는데 구현이 깨지지 않은 첫 사례이고, 그 자리를 `AbstractList` 가 대신 채웠기 때문이다 → [[abstract-class]] · [[interface]]

## 왜 중요한가

**순회 코드가 자료구조를 모르게 된다.** 하루 전까지 목록 출력은 「배열로 받아서 돈다」였고 그래서 `toArray()` 가 약속에 있어야 했다. 반복자로 바꾸면 호출부에는 배열도 인덱스도 남지 않는다 — 하루 전 회차가 회원·게시판은 `ArrayList`, 프로젝트·공지사항은 `LinkedList` 로 갈라 놓았는데, **그 갈림이 처음으로 순회 코드에 안 보이게 된 자리**다 → [[dependency-injection]] · [[dynamic-array]] · [[linked-list]]

**사본을 만들지 않고 돌 수 있게 된다.** `toArray()` 로 도는 것은 요소 n 개를 담은 배열을 매번 새로 만드는 일이다. 20일 전 회차에서 그 사본은 **원본 배열을 내주지 않으려는 방어**로 도입됐는데([[defensive-copy]]), 순회에도 같은 메서드를 쓰다 보니 목록을 볼 때마다 배열 하나가 생겼다. 반복자는 **커서 하나만** 만든다 — 목적이 둘이던 메서드에서 순회 쪽이 떨어져 나온 것이다.

**인덱스가 없는 구조까지 같은 규칙으로 묶인다.** 필기 1장이 「리스트, 트리, 해시맵」을 나란히 적은 것이 이 값이다. 트리와 해시맵에는 `get(int)` 가 없으므로 인덱스 `for` 로는 돌 수 없지만, 「다음이 있나 / 다음을 줘」는 어느 구조에서도 말이 된다. **순회를 인덱스에서 떼어낸 것이 자료구조의 종류를 늘릴 수 있게 한다** → [[hash-based-collection]]

**같은 컬렉션을 두 번 겹쳐 돌 수 있다.** 커서가 컬렉션이 아니라 반복자에 있으므로 `iterator()` 를 두 번 불러 반복자를 둘 만들면 서로 방해하지 않는다. 컬렉션이 커서를 필드로 들고 있는 설계였다면 중첩 순회가 곧바로 깨진다 — **커서를 어디에 두는가가 「동시에 몇 번 돌 수 있나」를 정한다** → [[instance]]

## 경계와 오해

- **Iterator ≠ Iterable — 이 회차가 그 둘을 이어 붙이지 못했다** — 같은 노트 4장이 「진보된 for문에는 배열 또는 Iterable이 가능하다 / 직접적으로 Iterable의 구현체를 생성하여도 가능하다」로 for-each 의 조건을 적는데, **이 실습이 만든 것은 `Iterator` 이고 `List` 는 `java.lang.Iterable` 을 구현하지 않는다.** 그래서 `for (Object obj : boardList)` 는 컴파일되지 않고, 순회 코드가 for-each 에서 `while` 로 되돌아갔다. 두 타입의 역할이 다르다 — **`Iterable` 은 「반복자를 줄 수 있다」는 컬렉션 쪽 표시**(하나, 컬렉션 자신)이고 **`Iterator` 는 「지금 도는 중인 커서」**(순회마다 새로 생긴다)다. `List extends Iterable` 한 줄과 메서드 이름을 `java.util.Iterator` 규격에 맞추는 것이 남은 일이었고, 필기는 반복자를 만든 절과 for-each 를 배운 절을 **연결하지 않은 채로 끝냈다** → [[for-loop]]
- **직접 만든 `Iterator` ≠ `java.util.Iterator`** — 이름도 메서드 이름도 같지만 다른 타입이라 표준 문법·라이브러리에 끼워지지 않는다. 표준 쪽에는 `remove()` 가 하나 더 있고, for-each 가 실제로 부르는 것은 `java.lang.Iterable.iterator()` 가 돌려주는 `java.util.Iterator` 다. 14일 전 회차가 `bitcamp.myapp2.util.List` 를 만들며 같은 이름 문제를 한 번 겪었고 **이번이 두 번째**다 — 표준과 같은 이름으로 만드는 것은 배우는 데 좋고 끼워 쓰는 데 나쁘다 → [[package]]
- **`ListIterator` 도 표준에 이미 있는 이름이다** — `java.util.ListIterator` 는 `previous()`·`add()`·`set()` 을 가진 **양방향** 반복자다. 이 실습의 것은 앞으로만 가므로 같은 이름으로 좁은 것을 만든 셈이다.
- **연결 리스트에서 이 반복자는 O(n²) 이다** — `next()` 가 `list.get(cursor++)` 이고 `LinkedList.get(index)` 는 매번 `first` 부터 `index` 칸 걸어간다. 요소 n 개를 다 돌면 걸음 수가 `1 + 2 + ... + n` 이 된다. **「자료구조에 맞는 순회」를 얻는 것이 이 패턴의 값인데 인덱스 조회에 기대는 순간 그 절반을 잃는다** — 연결 리스트의 반복자라면 `Node cursor` 를 들고 `cursor = cursor.next` 로 걸어야 하고, 그러면 전체가 O(n) 이다. 반복자를 만드는 자리를 `AbstractList` **한 곳에만** 둔 것이 그 길을 닫았다. 구조마다 다른 반복자를 줄 수 있다는 것이 `iterator()` 를 메서드로 둔 이유인데, 이 코드는 그 여지를 쓰지 않는다 → [[linked-list]] · [[template-method-pattern]]
- **`toArray()` 가 약속에서 사라지지 않았다** — `List` 에 `iterator()` 를 더했지만 `Object[] toArray()` 는 그대로 있다. 순회 경로가 둘이 되었고 구현 클래스는 둘 다 채워야 하며, 연결 리스트에서 `toArray()` 는 전체를 훑어 새 배열에 담는 일이다. **더한 절만 있고 뺀 절이 없는 리팩터링**이고, 남은 쪽을 지우려면 방어용 사본이 필요했던 자리를 따로 처리해야 한다 → [[interface-segregation-principle]] · [[refactoring]]
- **필기의 「객체 안에 실질적인 조회 코드를 숨긴다」에서 숨겨진 것은 없다** — `get(int)` 와 `size()` 는 여전히 `List` 의 `public` 메서드이고, 밖에서 인덱스로 도는 길이 그대로 열려 있다. 실제로 일어난 것은 **감춘 것이 아니라 경로를 하나 더 만든 것**이다. 진짜로 감추려면 `get`·`size` 를 약속에서 빼야 하는데, 그것들은 조회 기능 자체로도 쓰이고 있어서 뺄 수 없다 → [[encapsulation]]
- **반복 중에 컬렉션을 고치면 조용히 어긋난다** — 표준 컬렉션은 변경 횟수를 세어 `ConcurrentModificationException` 을 던지지만(fail-fast) 이 반복자는 그런 장치가 없다. 순회 도중 커서 앞의 요소를 지우면 뒤가 한 칸씩 당겨지므로 **커서가 가리키던 요소를 건너뛴다.** 반대로 추가하면 같은 요소를 두 번 볼 수 있다. 이 회차의 코드는 목록 출력에서만 반복자를 쓰므로 드러나지 않지만, 「순회하면서 조건에 맞는 것을 지운다」를 쓰는 날 바로 걸린다 → [[array-element-removal]]
- **`remove()` 가 없어서 순회 중 삭제는 인덱스로 되돌아가야 한다** — 표준 `Iterator.remove()` 가 있는 이유가 위 문제다. 반복자가 커서를 아니까 지운 뒤 커서를 맞춰 줄 수 있다. 이 실습의 반복자는 **읽기 전용**이고, 그래서 인덱스 `for` 가 완전히 대체되지는 않는다 → [[linear-search]]
- **반복자 패턴 ≠ 반복문을 없애는 것** — `while (iterator.hasNext())` 는 여전히 반복문이다. 없어진 것은 **인덱스 변수와 범위 조건**이고, `i < list.size()` 를 잘못 써서 범위를 넘는 종류의 실수가 사라진 것이 얻은 것이다 → [[while-loop]] · [[for-loop]]
- **반복자를 필드로 들고 있으면 커서가 남는다** — `Iterator iterator = boardList.iterator();` 가 메서드 안의 지역 변수인 것이 중요하다. 필드로 올리면 목록을 두 번째로 볼 때 커서가 끝에 있어 아무것도 찍히지 않는다. **반복자는 한 번 쓰고 버리는 것**이고, 다시 돌려면 새로 얻어야 한다 → [[variable]]
- **`next()` 의 반환 타입이 `Object` 라 캐스팅이 남는다** — `Board board = (Board) iterator.next();`. `toArray()` 로 돌 때와 똑같이 형변환이 필요하고, 순회를 추상화해도 **타입은 추상화되지 않았다.** 이 자리를 없애는 것이 제네릭이 하는 일이다 → [[type-casting]] · [[object-class]]
- **`hasNext()` 가 「다음 것이 있나」가 아니라 「아직 안 준 것이 있나」다** — `cursor < list.size()` 이고 `cursor` 는 **다음에 줄 위치**다. 「현재 위치」로 읽으면 마지막 요소에서 `hasNext()` 가 왜 참인지 설명되지 않는다 → [[one-based-numbering]]
- **반복자를 만드는 일이 `new` 를 호출부에서 없애지 않는다 — 옮긴다** — `boardList.iterator()` 안에서 `new ListIterator(this)` 가 매번 일어난다. 호출부가 구현 클래스 이름을 모르게 된 것이 얻은 것이고([[dependency-inversion-principle]]), 만드는 책임은 컬렉션이 가졌다 — 「자기 것을 아는 쪽이 만든다」의 한 예다 → [[grasp]]

## 함께 보는 개념

- [[interface]] — 순회의 사용 규칙을 담는 약속
- [[for-loop]] — 이 패턴이 대체하는 순회 방법, 그리고 `Iterable` 이 필요한 이유
- [[abstract-class]] — 반복자를 내주는 구현이 놓인 자리
- [[template-method-pattern]] — 부모가 만든 반복자가 자식의 메서드를 부르는 구조
- [[nested-class]] — 반복자를 컬렉션 안으로 넣는 네 가지 방법
- [[anonymous-class]] — 반복자에서 이름까지 없앤 형태
- [[linked-list]] — 인덱스 조회에 기대면 손해를 보는 구조
- [[dynamic-array]] — 같은 반복자가 문제없이 도는 구조
- [[encapsulation]] — 「내부 구조를 감춘다」가 어디까지 됐는지 재는 축
- [[defensive-copy]] — `toArray()` 가 원래 하던 일
- [[polymorphism]] — 같은 `Iterator` 타입으로 다른 순회를 받는 성질
- [[while-loop]] — 반복자와 짝을 이루는 반복문
- [[type-casting]] — `Object` 를 되돌리는 남은 일
- [[interface-segregation-principle]] — `toArray()` 가 약속에 남은 것을 재는 원칙
- [[refactoring]] — 더한 절과 뺀 절이 갈린 작업
- [[hash-based-collection]] — 인덱스가 없어 반복자가 필요한 구조

## 출처

- [[2024-07-10-Day32]] — 「컬렉션의 내부 구조를 노출하지 않고 그 요소들에 순차적으로 접근」이라는 정의에서 출발해 `interface Iterator { hasNext(); next(); }` 와 `ListIterator` 를 직접 만들고, `List` 에 `iterator()` 를 더해 `BoardCommand.listBoard()` 의 `for (Object obj : boardList.toArray())` 를 `while (iterator.hasNext())` 로 바꿨다. 반복자를 내주는 구현을 `AbstractList` 한 곳에 두어 자식 클래스가 하나도 바뀌지 않은 것이 이 회차의 값이고, 같은 노트 4장에서 for-each 의 조건이 `Iterable` 이라는 것을 배우면서도 **자기가 만든 `List` 를 `Iterable` 로 만들지 않아** for-each 로 돌아가지 못한 것이 빠진 한 걸음이다. `next()` 가 `list.get(cursor++)` 이라 연결 리스트에서는 순회가 O(n²) 이고, `toArray()` 는 약속에서 지워지지 않았으며 `remove()` 와 반복 중 변경 검사는 없다
