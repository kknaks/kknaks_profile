---
type: concept
id: number-parsing
title: 문자열 → 숫자 변환 (파싱)
aliases:
  - 숫자 파싱
  - parseInt
  - Integer.parseInt
  - NumberFormatException
  - 문자열 숫자 변환
  - number parsing
up:
  - 2024-06-11-Day12
  - 2024-06-18-Day17
tags:
  - java
  - 입출력
  - 예외
---

# 문자열 → 숫자 변환 (파싱)

`"12"` 라는 **글자**를 읽어 `12` 라는 **수**를 만드는 것. 타입을 바꿔 보는 것이 아니라 내용을 해석해 새 값을 만드는 일이라, 실패할 수 있다.

## 정의

```java
int menuNo = Integer.parseInt(command);
```

`Integer` 의 클래스 메서드이므로 객체를 만들지 않고 부른다 → [[static-member]]. 넘긴 문자열이 정수의 모양이 아니면 값을 만들 수 없고, 그때 `NumberFormatException` 을 던진다 → [[exception-handling]]

## 사용 예시

이 필기는 입력을 받는 방식을 바꾸면서 파싱을 들여왔다. 앞의 코드는 숫자를 직접 읽었고,

```java
menuNo = keyboardScanner.nextInt();          // 숫자만 온다는 전제
```

뒤의 코드는 **한 줄을 문자열로 받아 놓고 나중에 해석한다.**

```java
command = keyboard.nextLine();
if (command.equals("menu")) {
    printMenu();                             // 숫자가 아닌 명령
} else {
    int menuNo = Integer.parseInt(command);   // 숫자면 여기서 값이 된다
    ...
}
```

`catch` 도 같이 바뀐다 — `InputMismatchException` 이 아니라 `NumberFormatException` 이다.

```java
} catch (NumberFormatException ex) {
    System.out.println("숫자로 메뉴 번호를 입력하세요.");
}
```

### 파싱을 메서드로 감싸면 `catch` 가 딸려오지 않는다

며칠 뒤 실습 프로젝트는 「숫자를 받는 일」을 유틸리티 메서드로 뽑았다.

```java
public static int inputInt(String format, Object... args) {
  return Integer.parseInt(input(format, args));
}
```

부르는 쪽이 아주 짧아진다 → [[varargs]]

```java
int projectNo = Prompt.inputInt("프로젝트번호?");
int userNo = Prompt.inputInt("추가할 팀원 번호?(종료:0)");
```

**그런데 `try`/`catch` 가 어디에도 없다.** 앞 회차들에서 만들어 둔 `catch (NumberFormatException)` 가 이 프로젝트에는 없어서, 사용자가 번호 자리에 글자를 넣거나 엔터만 치면 **프로그램이 그 자리에서 죽는다.** 검사 예외가 아니라 컴파일러가 아무 말도 하지 않는다 → [[exception-handling]]

같은 프로젝트 안에 두 방식이 섞여 있는 것도 눈에 남는다.

```java
int userNo = Integer.parseInt(Prompt.input("회원번호?"));   // UserCommand — 직접 파싱
int projectNo = Prompt.inputInt("프로젝트번호?");           // ProjectCommand — 감싼 메서드
```

앞은 파싱이 호출부에 보이고 뒤는 `Prompt` 안에 있다. **뒤쪽이 읽기 좋지만, 예외가 어디서 나는지도 같이 숨는다.**

## 왜 중요한가

**입력 통로를 하나로 만들 수 있다.** `nextInt()` 는 "다음에 오는 것은 숫자다"를 전제하지만, 실제 CLI 는 `3` 도 받고 `menu` 도 받는다. 문자열로 받아 두면 **무엇이 왔는지 보고 나서** 숫자로 해석할지 명령으로 볼지 정할 수 있다. 이 필기가 `menu` 명령을 넣을 수 있게 된 것이 그 결과다.

두 번째로, **읽는 단위가 줄이 되면서 입력 버퍼에 남는 것이 없어진다.** `nextInt()` 를 쓰면 개행이 버퍼에 남아 다음 읽기를 망치고, 예외가 나면 잘못된 입력까지 남아 무한 루프가 된다. 줄 단위로 다 읽어 버리는 방식은 그 문제 자체를 없앤다 → [[standard-input]]

**검증 방법도 바뀐다.** `nextInt()` 는 스캐너가 검증을 해 주지만, 파싱은 "해 보고 실패하면 예외"다. 즉 검증 지점이 **입력을 읽는 자리에서 값을 쓰는 자리로** 옮겨 온다.

## 경계와 오해

- **파싱 ≠ 캐스팅** — `(int) "12"` 는 컴파일 오류다. 캐스팅은 이미 수인 값을 다른 수 타입으로 보거나 참조의 타입을 바꾸는 것이고([[type-casting]] · [[type-promotion]]), 파싱은 **글자를 해석해 새 값을 만드는 것**이다. 그래서 캐스팅은 실패해도 컴파일 시점에 드러나는 반면 파싱은 실행 시점에 터진다.
- **`NumberFormatException` 은 검사 예외가 아니다** — `try`/`catch` 를 강제하지 않으므로 감싸지 않아도 컴파일된다. 잊으면 사용자가 글자를 하나 넣는 순간 프로그램이 죽는다.
- **예외를 흐름 제어로 쓰는 것이다** — "숫자인가"를 묻는 방법이 "변환해 보고 실패를 잡는 것"이라, 정상 입력에서도 예외가 자주 나는 구조가 된다. 작은 CLI 에서는 관용이지만, 예외 하나마다 스택 트레이스가 만들어지므로 잦은 경로에서는 미리 검사하는 쪽이 낫다.
- **앞뒤 공백을 허용하지 않는다** — `Integer.parseInt(" 12")` 는 예외다. `nextInt()` 는 공백을 건너뛰고 읽으므로 통과했던 입력이 `nextLine()` + `parseInt()` 로 바꾸면 실패한다. **입력을 읽는 방법을 바꾸면 허용되는 입력의 모양도 바뀐다.**
- **빈 문자열도 실패한다** — 사용자가 엔터만 치면 `""` 이고 예외다. 이 필기의 코드에서는 "숫자로 메뉴 번호를 입력하세요"가 출력된다 — 의도한 메시지는 아니지만 죽지는 않는다.
- **`Integer.parseInt` 와 `Integer.valueOf` 는 돌려주는 것이 다르다** — 앞은 `int`, 뒤는 `Integer` 객체다. 이름이 닮아서 섞이지만 반환 타입이 갈린다.
- **감싼 메서드는 실패를 안 다루면 실패를 감춘다** — `inputInt` 는 「숫자를 받아 주는 메서드」로 읽히지만 실패 처리는 없다. 파싱을 뽑아 올리는 것과 예외 처리를 뽑아 올리는 것은 **따로 결정해야 하는 일**이고, 앞만 하면 부르는 쪽 어디에도 `catch` 가 없는 코드가 된다. 이 필기가 며칠 전에 만들어 둔 `catch` 가 새 프로젝트에서 사라진 것이 그 결과다 → [[method]]
- **번호 입력에서 가장 흔한 잘못은 글자가 아니라 엔터다** — 빈 문자열도 `NumberFormatException` 이다. 「숫자가 아닌 것을 넣는 사람은 드물다」로 넘기면, 아무것도 안 누른 사용자에게 프로그램이 죽는 것이 설명되지 않는다.

## 함께 보는 개념

- [[standard-input]] — 파싱할 문자열을 받아 오는 곳
- [[exception-handling]] — 실패를 다루는 방법
- [[type-casting]] — 「변환」이라 불리지만 다른 일
- [[static-member]] — 객체 없이 부르는 클래스 메서드의 예
- [[string-comparison]] — 같은 문자열 입력을 값으로 비교하는 자리
- [[varargs]] — 파싱을 감싼 메서드가 인수를 받는 문법
- [[method]] — 감싸는 것과 감싼 것의 책임
- [[one-based-numbering]] — 파싱한 번호를 검사하는 다음 단계

## 출처

- [[2024-06-11-Day12]] — `nextInt()` 대신 한 줄을 문자열로 받아 `Integer.parseInt` 로 해석하도록 실습 코드를 바꾸며, 잡아야 하는 예외가 `InputMismatchException` 에서 `NumberFormatException` 으로 바뀐다는 것을 배웠다
- [[2024-06-18-Day17]] — 파싱을 `Prompt.inputInt(String, Object...)` 로 감싸 호출부를 짧게 만드는 것을 실습으로 배웠다. 그 과정에서 앞 회차들의 `try`/`catch` 가 사라져 번호 자리에 숫자가 아닌 입력이 오면 프로그램이 죽는 상태가 된 자리이기도 하다
