---
type: concept
id: method
title: 메서드 (Method)
aliases:
  - 메서드
  - 메소드
  - method
  - 메서드 추출
  - extract method
  - 메서드 시그니처
  - method signature
up:
  - 2024-06-11-Day12
  - 2024-06-12-Day13
  - 2024-06-25-Day22
  - 2024-07-03-Day28
tags:
  - java
  - 문법
  - 설계
---

# 메서드 (Method)

클래스 안에 **이름을 붙여 묶어 둔 기능 한 덩어리.** 부르면 그 안의 문장이 실행되고, 끝나면 부른 자리로 돌아온다.

## 정의

선언은 네 부분이다.

```java
static String getMenuTitle(int menuNo) { ... }
//     ^반환타입 ^이름      ^매개변수
```

| 부분 | 정하는 것 |
|---|---|
| 반환 타입 | 돌려주는 값의 타입. 돌려줄 것이 없으면 `void` |
| 이름 | 부를 때 쓰는 이름 |
| 매개변수 | 부르는 쪽이 넘긴 값을 받는 자리. 없어도 된다 → [[parameter-and-argument]] |
| 본문 | 실행할 문장 |

이 네 부분은 **두 덩이**로 불린다 — 부르는 쪽이 맞춰야 하는 앞부분과, 그 안에서 실행될 문장을 담은 중괄호 블록이다.

```java
//method signature(fuction prototype)
(static)[return type] method_name(parameter)

//method body
{
	명령문; 
}
```

부르면 그 자리에서 실행이 넘어가고, `return` 을 만나면 부른 자리로 돌아온다. 이 오고 감이 메모리에서 어떻게 일어나는지가 스택 프레임이다 → [[jvm-stack]]

메서드는 두 종류로 갈린다 — 객체 없이 부르는 클래스 메서드와 인스턴스를 만들어야 부를 수 있는 인스턴스 메서드다 → [[static-member]]

이 필기가 정리한 메서드의 값은 셋이다.

```text
중복 코드를 분리하여 유지보수 용이하다.
기능 단위로 명령어로 묶어 코드의 가독성을 향상시킨다.
코드의 재사용률이 올라가여 다른 프로젝트에도 적용하기 용이하다.
```

## 사용 예시

`main` 하나에 다 들어 있던 코드를 네 개로 쪼갠 것이 이 필기의 실습이다.

```java
static void printMenu(){ ... }                       // 출력만 한다 — 돌려줄 것이 없다

static String prompt(){                              // 값을 받아 온다
    System.out.print("> ");
    return keyboard.nextLine();
}

static boolean isValidateMenu(int menuNo){           // 판정한다
    return (menuNo >= 1 && menuNo <= menus.length);
}

static String getMenuTitle(int menuNo){              // 조회한다 — 없으면 null
    return isValidateMenu(menuNo)? menus[menuNo-1] : null;
}
```

**네 개가 각각 다른 종류의 일을 하고, 그것이 반환 타입에 드러난다** — `void`(출력) · `String`(입수) · `boolean`(판정) · `String`(조회). → [[ternary-operator]]

그 결과 `main` 이 이렇게 짧아진다.

```java
command = prompt();
if (command.equals("menu")) {
    printMenu();
} else {
    ...
}
```

## 왜 중요한가

**중복을 없애는 목적은 타이핑을 줄이는 것이 아니라 고칠 자리를 하나로 만드는 것이다.** 이 필기 안에서 그 값이 바로 드러난다 — 중간 버전의 `isValidateMenu` 는 `menuNo <= 6` 으로 숫자를 박아 뒀고, 최종 버전에서는 `menuNo <= menus.length` 로 바뀌었다. 메뉴가 하나 늘 때 고칠 자리가 **한 곳뿐이라서** 고칠 수 있었다. 묶지 않았다면 같은 조건이 코드 여러 군데에 흩어져 있고, 그중 하나를 놓치는 것이 버그가 된다.

두 번째는 **이름이 주석을 대신한다**는 것이다. `menuNo >= 1 && menuNo <= menus.length` 는 무엇을 묻는지 읽어서 해석해야 하지만 `isValidateMenu(menuNo)` 는 이름이 말해 준다. 조건식을 메서드로 뽑는 것은 코드를 줄이는 일이 아니라 **의도에 이름을 붙이는 일**이다.

## 경계와 오해

- **메서드 ≠ 메서드 호출** — 이 필기는 메서드를 "함수를 실행하는 것"이라 적었다. 메서드는 **선언해 둔 코드 덩어리**이고, 실행하는 것은 **호출**이다. 선언은 한 번이고 호출은 여러 번이라는 것이 재사용의 근거이므로, 둘을 같은 것으로 두면 "재사용된다"는 말이 설명되지 않는다. 호출마다 따로 생기는 것은 선언이 아니라 **프레임**이다 → [[jvm-stack]]
- **시그니처 ≠ 선언 전체** — 이 필기는 `(static)[return type] method_name(parameter)` 를 통째로 시그니처라 적었지만, Java 의 시그니처는 **이름 + 매개변수 타입 목록**뿐이다. 반환 타입과 `static` 은 들어가지 않는다. 이 경계가 실제로 갈리는 자리가 오버로딩이다 — 반환 타입만 다른 두 메서드는 시그니처가 같아서 컴파일되지 않는다. "선언 첫 줄 = 시그니처"로 외우면 그 오류 메시지를 읽을 수 없다.
- **같은 이름의 메서드 개수는 「타입이 몇 갈래인가」로 정해진다** — Day13 시점에는 시그니처가 오버로딩의 판정 기준이라는 문법 이야기로 끝났는데, 래퍼 클래스 회차가 **개수를 실제로 세어 보게 만든다.** 기본 타입 여덟 개를 받으려면 세 개(`long`·`double`·`boolean`)가 필요하고, 여덟이 아니라 셋인 것은 자동 승격이 묶어 주기 때문이다. 그리고 그 셋이 `m(Object)` 하나로 줄어드는 것이 오버로딩과 [[polymorphism]] 이 갈리는 지점이다 — **오버로딩은 받을 타입마다 메서드가 늘고, 다형성은 안 는다** → [[type-promotion]] · [[wrapper-class]]
- **오버로딩이 늘어나는 이유가 「타입이 몇 갈래인가」만은 아니다** — 여드레 뒤 회차의 `display(BubbleSort)`·`display(QuickSort)` 는 **하는 일이 똑같은데** 둘로 갈려 있다. 갈린 원인은 받는 데이터의 성질이 아니라 **두 클래스가 같은 기능에 서로 다른 이름을 붙였다는 것**이다 — 한쪽은 `run(values)`, 다른 쪽은 `start(values, 0, values.length - 1)`. 여기서 오버로딩은 문법 기능이 아니라 **남의 API 가 어긋난 것을 호출부가 흡수해 준 자리**이고, 그래서 정렬 클래스가 하나 늘 때마다 `display` 도 하나 늘고 그 클래스의 메서드 이름을 새로 알아야 한다. 「같은 이름으로 부를 수 있어 편하다」로만 읽으면 이 비용이 안 보인다 → [[abstract-class]]
- **오버로딩을 없애는 답이 하나가 아니다** — 래퍼 회차는 `m(Object)` 로 **가장 넓은 타입**을 받아 줄였고, 정렬 회차는 `display(Sorter)` 로 **부모를 직접 만들어** 줄였다. 결과는 둘 다 메서드 하나인데, 뒤쪽은 매개변수 안에서 `sorter.sort(values)` 를 그대로 부를 수 있어 **아래 줄의 대가를 치르지 않는다.** 「다형성으로 오버로딩을 지운다」를 한 가지 방법으로 기억하면 그 차이가 사라진다 → [[polymorphism]]
- **오버로딩을 줄인 대가는 매개변수 안에서 치른다** — `m(Object)` 는 메서드 하나로 끝나지만 그 안에서 무엇이 왔는지 알 수 없다. `printf("%s")` 처럼 타입을 안 물어도 되는 일만 할 수 있고, 값을 꺼내 계산하려면 다운캐스팅이 필요해진다. **「메서드 개수」와 「메서드 안의 복잡도」를 주고받는 것**이지 한쪽이 공짜로 좋아지는 것이 아니다 → [[type-casting]]
- **Java 에 프로토타입 선언은 없다** — 필기가 시그니처에 「fuction prototype」을 병기했는데, C 의 프로토타입은 **본문 없이 선언만 미리 두는 것**이고 Java 에는 그 문법이 없다. 본문 없는 선언이 필요하면 `abstract` 메서드나 인터페이스로 간다 → [[abstract-class]]
- **이름이 반환 타입과 어긋나면 읽는 사람이 틀린다** — `isValidateMenu` 는 `boolean` 을 돌려주는데 이름이 동사(`validate`)라 "검증을 수행한다"로 읽힌다. `boolean` 을 돌려주는 메서드의 관례는 `is` + 상태(`isValidMenu`)다. 이름은 취향이 아니라 **호출부에서 무엇으로 읽히는가**의 문제다 — `if (isValidateMenu(n))` 보다 `if (isValidMenu(n))` 이 문장으로 읽힌다.
- **쪼개는 기준은 길이가 아니다** — "몇 줄이 넘으면 나눈다"가 아니라 **같은 코드가 두 번 나올 때**, 또는 **한 덩어리가 서로 다른 관심사를 하고 있을 때** 나눈다. 길이는 결과지 기준이 아니다.
- **메서드로 뽑았다고 독립적인 것은 아니다** — `printMenu()`·`prompt()` 는 매개변수가 없는데도 동작한다. `menus`·`keyboard` 를 클래스 필드로 올려 뒀기 때문이다. **재사용 가능성은 이름이 아니라 무엇에 의존하는지가 정한다** — 밖의 상태에 의존하는 메서드는 그 상태를 같이 옮기지 않으면 다른 프로젝트로 가져갈 수 없다 → [[static-member]] · [[parameterization]]
- **Java 에 클래스 밖의 함수는 없다** — 모든 메서드는 어떤 클래스에 소속된다. 그래서 이 필기의 네 메서드도 `App` 클래스 안에 있고, `main` 이 `static` 이라 전부 `static` 으로 끌려갔다 → [[main-method]]

## 함께 보는 개념

- [[static-member]] — 메서드의 두 종류와 `static` 이 강제하는 것
- [[main-method]] — 프로그램이 가장 먼저 부르는 메서드
- [[conditional-flattening]] — 메서드로 뽑은 뒤 남은 조건문을 정리하는 단계
- [[method-overriding]] — 상속에서 같은 이름의 메서드를 다시 정의하는 것
- [[ternary-operator]] — 반환값을 한 줄로 고르는 방법
- [[array]] — `menus.length` 로 판정 기준을 삼는 자리
- [[parameter-and-argument]] — 선언과 호출이 값을 주고받는 자리
- [[parameterization]] — 감춰진 의존을 매개변수로 올려 다른 맥락에서도 부를 수 있게 하는 것
- [[call-by-value]] — 그 값이 어떻게 넘어가는가
- [[jvm-stack]] — 호출과 `return` 이 메모리에서 하는 일
- [[recursion]] — 메서드가 자기 자신을 부르는 형태
- [[polymorphism]] — 오버로딩과 갈리는 자리
- [[wrapper-class]] — 메서드 셋이 하나로 줄어든 예
- [[type-promotion]] — 오버로딩 개수를 줄여 주는 규칙
- [[type-casting]] — 하나로 줄인 대가를 치르는 자리
- [[abstract-class]] — 오버로딩을 부모 하나로 접는 다른 답

## 출처

- [[2024-06-11-Day12]] — `main` 한 덩어리였던 실습 코드를 `printMenu()`·`prompt()`·`isValidateMenu()`·`getMenuTitle()` 네 메서드로 뽑으며 메서드의 선언 형식과 중복 제거·가독성·재사용이라는 값을 배웠다
- [[2024-06-12-Day13]] — 선언이 시그니처와 본문으로 불린다는 것, 호출과 `return` 이 스택 프레임의 생성·삭제라는 것을 배웠다. 시그니처를 선언 첫 줄 전체로 적은 것은 이 필기의 표기다
- [[2024-06-25-Day22]] — 래퍼 클래스를 배우는 자리에서 같은 이름의 메서드 `m(long)`·`m(double)`·`m(boolean)` 세 개를 만들어 보고, 래퍼로 감싸면 `m(Object)` 하나로 줄어드는 것을 확인했다. 「wrapper 클래스를 사용하지 않으면 primitive type에 대해 각각 메서드를 만들어야한다」가 오버로딩의 비용을 개수로 보여 준 자리이고, 주석의 `// byte, short, int, long, char` 가 세 개로 줄어든 이유를 담고 있다
- [[2024-07-03-Day28]] — 추상 클래스를 배우는 출발점이 오버로딩 두 개다. `display(BubbleSort)`·`display(QuickSort)` 가 「기능은 같지만 sorter.run()과 sorter.start()의 메서드명과 매개변수가 다르다」는 이유로 갈려 있고, 공통 부모를 만들어 `display(Sorter)` 하나로 접는다. **오버로딩이 데이터 타입 때문이 아니라 남의 메서드 이름 때문에 늘어난 예**이고, 여드레 전 `m(Object)` 와 달리 매개변수 안에서 그 메서드를 그대로 부를 수 있다
