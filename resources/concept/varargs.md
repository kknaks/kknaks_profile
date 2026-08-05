---
type: concept
id: varargs
title: 가변 인수 (Varargs)
aliases:
  - 가변 인수
  - 가변인자
  - varargs
  - variable arguments
  - 가변 길이 매개변수
up:
  - 2024-06-18-Day17
tags:
  - java
  - 메서드
  - 문법
  - 재사용
---

# 가변 인수 (Varargs)

매개변수 타입 뒤에 `...` 을 붙여 **인수를 몇 개 넘겨도 받게** 하는 문법. 넘기는 개수를 부르는 쪽이 정하고, 받는 쪽에서 그것은 **배열 하나**다.

## 정의

```java
public static String input(String format, Object... args) {
  System.out.printf(format + " ", args);      // 본문에서 args 는 Object[] 다
  return keyboardScanner.nextLine();
}
```

- **선언에서는 `...`, 본문에서는 배열**이다. 컴파일러가 호출부의 남은 인수를 모아 배열을 만들어 넘긴다.
- **마지막 매개변수여야 한다.** 뒤에 다른 매개변수가 오면 어디서 끝나는지 정할 방법이 없다.
- **인수를 하나도 안 넘겨도 된다.** 그때 `args.length == 0` 이고 `null` 이 아니다.

| 호출 | 넘어가는 `args` |
|---|---|
| `input("이름?")` | 길이 0 배열 |
| `input("이름(%s):", name)` | `{name}` |
| `input("메인/%s>", title)` | `{title}` |

타입을 `Object` 로 잡으면 무엇이든 받는다 — 필기가 「Object 자료형은 모든 데이터 타입을 받는다」고 적은 자리다. 기본 타입도 박싱되어 들어간다 → [[data-type]]

## 사용 예시

이 필기는 여러 클래스가 함께 쓰는 입력 메서드를 `util` 패키지의 `Prompt` 로 옮기면서 가변 인수를 붙였다 → [[package]]

```java
package bitcamp.myapp2.util;

public class Prompt {
  static Scanner keyboardScanner = new Scanner(System.in);

  public static String input(String format, Object... args) {
    System.out.printf(format + " ", args);
    return keyboardScanner.nextLine();
  }

  public static int inputInt(String format, Object... args) {
    return Integer.parseInt(input(format, args));      // args 를 그대로 다시 넘긴다
  }
}
```

필기가 값이 흘러가는 과정을 손으로 풀어 뒀다.

```text
input("메인/%s>", menutitle)
  format = "메인/%s>",  menutitle = mainMenuse[0] = "회원"
-> System.out.printf(format + " ", args) = System.out.printf("메인/%s>" + " ", "회원");
=> "메인/회원> "
```

그 결과 **묻기만 하는 자리와 현재 값을 보여 주는 자리가 같은 메서드 하나**로 처리된다.

```java
user.setName(Prompt.input("이름?"));                        // 등록 — 인수 없음
user.setName(Prompt.input("이름(%s):", user.getName()));    // 변경 — 현재 값을 끼워 넣는다
```

`inputInt` 의 `input(format, args)` 가 이 문법의 두 번째 얼굴이다. **이미 `Object[]` 가 된 `args` 를 가변 인수 자리에 다시 넘기면 그 배열이 그대로 전달된다** — 원소 하나로 감싸이지 않는다. 그래서 `inputInt("추가할 팀원 번호?(종료:0)")` 와 `inputInt("프로젝트(%s)?", title)` 가 둘 다 통한다.

## 왜 중요한가

**개수가 달라지는 인수를 오버로딩 없이 하나로 받는다.** 가변 인수가 없으면 `input(String)`·`input(String, Object)`·`input(String, Object, Object)` … 를 필요한 만큼 만들어야 하고, 그것들이 전부 같은 본문을 복사해 갖는다. 고칠 자리가 개수만큼 늘어나는 것이다 → [[method]]

**[[parameterization]] 의 다음 칸이다.** Day14 에서 `prompt()` 가 `prompt(String title)` 이 되며 「무엇을 물을지」를 부르는 쪽이 정하게 됐고, 여기서는 **그 문구에 값을 몇 개 끼워 넣을지까지** 부르는 쪽이 정한다. 호출부가 고를 수 있는 범위가 한 단계 더 넓어졌다.

그리고 **받은 것을 손대지 않고 흘려보낼 수 있다.** `printf` 가 같은 문법으로 만들어져 있어서 `Prompt.input` 은 형식 문자열과 인수를 해석하는 일을 다시 만들 필요가 없다 — 그대로 넘기면 된다. 가변 인수는 「많이 받기」보다 **한 층을 그냥 통과시키기**에 값이 있다.

## 경계와 오해

- **`Object... args` ≠ 인수 여러 개** — 넘어가는 것은 **배열 한 개**다. 호출마다 배열이 새로 만들어지므로 아주 잦은 경로에서는 그 생성 비용이 드러난다. 「문법 설탕이라 공짜」로 읽으면 설명되지 않는다 → [[array]]
- **`...` 는 마지막에만 온다** — `input(Object... args, String format)` 은 컴파일 오류다. 그래서 형식 문자열이 앞에 오는 `printf(format, args)` 모양이 사실상 강제된다.
- **배열을 넘기면 펼쳐지지 않는다** — `Object[]` 를 가변 인수 자리에 넘기면 **그 배열이 곧 `args`** 다. `inputInt` 가 동작하는 근거이고, 반대로 배열 하나를 「원소 한 개」로 넘기고 싶으면 `new Object[]{arr}` 로 감싸야 한다.
- **형식 문자열과 인수 개수가 맞는지 컴파일러가 보지 않는다** — `input("이름(%s):")` 은 컴파일되고 실행 중에 `MissingFormatArgumentException` 이 난다. 가변 인수는 개수를 자유롭게 해 주는 대신 **개수 검사를 실행 시점으로 옮긴다** → [[exception-handling]]
- **`format + " "` 은 형식 문자열을 손댄 것이다** — 프롬프트 뒤에 공백을 붙이려고 이어 붙였는데, 이 자리에 오는 문자열은 **형식으로 해석된다.** 부르는 쪽이 `%` 가 든 문장을 넘기면 값이 아니라 형식 지시자로 읽힌다. 값은 반드시 `args` 로 보내야 한다.
- **`Object` 로 받는 것은 타입 검사를 포기하는 것이다** — 무엇이든 받으므로 `%d` 자리에 `String` 을 넘겨도 컴파일된다. 안 맞으면 실행 중에 `IllegalFormatConversionException` 이다 → [[type-casting]]
- **감싼 메서드가 실패 지점을 감춘다** — `inputInt` 는 `Integer.parseInt` 를 품고 있는데 예외를 다루지 않는다. 부르는 쪽에서는 「숫자를 받아 주는 편한 메서드」로 보이지만 숫자가 아닌 입력에 그대로 죽는다. 가변 인수와는 별개의 문제이면서, **얇은 위임 메서드를 만들 때 같이 봐야 하는 자리**다 → [[number-parsing]]

## 함께 보는 개념

- [[parameter-and-argument]] — 받는 자리와 넘기는 값
- [[parameterization]] — 호출부가 정할 범위를 넓히는 앞 단계
- [[array]] — 가변 인수의 실체
- [[method]] — 이 문법이 붙는 자리
- [[number-parsing]] — `inputInt` 가 감싸는 일
- [[package]] — `Prompt` 가 `util` 로 간 이유
- [[static-member]] — `Prompt` 의 멤버가 전부 `static` 인 것

## 출처

- [[2024-06-18-Day17]] — 여러 클래스가 쓰는 입력 메서드를 `util.Prompt` 로 옮기면서 `input(String format, Object... args)` 로 만들고, 받은 `args` 를 `printf` 에 그대로 흘려보내 프롬프트 문구와 끼워 넣을 값을 부르는 쪽이 정하게 하는 것을 실습으로 배웠다. `inputInt` 가 `input(format, args)` 로 배열을 그대로 다시 넘기는 것도 이 자리다
