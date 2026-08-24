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
  - 2024-08-19-Day58
  - 2024-08-20-Day59
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

### 두 달 뒤 Day58 — 같은 문법이 SQL 값 목록을 받는다

Day17 이 화면에 찍을 값들을 받았고, **Day58 은 `?` 에 채울 값들을 받는다** → [[sql-session]]

```java
public int insert(String sql, Object... values) throws Exception {
  try (PreparedStatement stmt = con.prepareStatement(sql)) {
    int inparameterIndex = 1;
    for (Object value : values) {
      stmt.setString(inparameterIndex++, value.toString());
    }
    return stmt.executeUpdate();
  }
}

public int update(String sql, Object... values) throws Exception {
  return insert(sql, values);          // Day17 의 inputInt 와 같은 통과
}
```

두 회차가 이 문법의 **두 얼굴을 각각 하나씩** 쓴다. `update` 는 받은 배열을 손대지 않고 **흘려보내고**(`inputInt` 와 같은 자리), `insert` 는 그것을 **`for` 로 하나씩 꺼내 쓴다** — 후자에서 「본문에서 `args` 는 배열이다」가 코드로 보인다.

그리고 **여기서 이 문법의 대가가 처음 값을 매긴다.** 개수를 자유롭게 얻은 대신 세션이 아는 타입은 `Object` 뿐이고, `PreparedStatement` 는 타입마다 `setInt`·`setDate` 가 따로 있으므로 **고를 근거가 없어 `setString` 하나로 몰린다.** Day17 에서는 `printf` 가 형식 문자열로 타입을 알려 받았기 때문에 이 문제가 드러나지 않았다 → [[prepared-statement]]

### 하루 뒤 Day59 — 같은 성질이 처음 함정으로 나타난다

`Method.invoke` 의 선언이 **`invoke(Object obj, Object... args)`** 다. 그래서 리플렉션으로 메서드를 부르는 일이 이 문법 위에 서 있고, Day59 가 두 형태를 나란히 적었다 → [[reflective-invocation]]

```java
// 파라미터 값을 낱개로 전달하기
m.invoke(null, "홍길동", 100, 90, 80);

// 파라미터 값을 배열에 담아서 전달할 수 있다.
m.invoke(null, new Object[] {"홍길동", 100, 100, 100});
```

**「배열을 넘기면 펼쳐지지 않는다」의 세 번째 사례이고, 앞의 둘과 뜻이 다르다.** Day17 의 `inputInt(format, args)` 와 Day58 의 `insert(sql, values)` 는 **받은 배열을 다음 층으로 그냥 통과시키려** 했으므로 펼쳐지는 것이 원하는 동작이었다. `invoke` 에서는 그것이 **인수 목록 자체**가 되므로, 배열 하나를 값 하나로 주고 싶은 순간 같은 규칙이 걸림돌이 된다 — Day59 가 그 답을 두 줄로 적었다: 「배열의 파라미터인 경우는 배열에 담아서 전달해야한다」·「가변 파라미터의 경우에도 배열에 담아서 전달해야한다」.

```java
// void m(Object[] values) 를 부르고 싶다면 한 겹 더 감싼다
m.invoke(null, new Object[]{ values });   // 인수 하나 = 그 배열
```

**같은 문법이 이 필기에서 세 번 쓰이는데 두 번은 이득이고 한 번은 함정이다** — 「흘려보내기 좋다」와 「값 하나로 주기 어렵다」는 한 성질의 앞뒤다.

## 왜 중요한가

**개수가 달라지는 인수를 오버로딩 없이 하나로 받는다.** 가변 인수가 없으면 `input(String)`·`input(String, Object)`·`input(String, Object, Object)` … 를 필요한 만큼 만들어야 하고, 그것들이 전부 같은 본문을 복사해 갖는다. 고칠 자리가 개수만큼 늘어나는 것이다 → [[method]]

**[[parameterization]] 의 다음 칸이다.** Day14 에서 `prompt()` 가 `prompt(String title)` 이 되며 「무엇을 물을지」를 부르는 쪽이 정하게 됐고, 여기서는 **그 문구에 값을 몇 개 끼워 넣을지까지** 부르는 쪽이 정한다. 호출부가 고를 수 있는 범위가 한 단계 더 넓어졌다.

그리고 **받은 것을 손대지 않고 흘려보낼 수 있다.** `printf` 가 같은 문법으로 만들어져 있어서 `Prompt.input` 은 형식 문자열과 인수를 해석하는 일을 다시 만들 필요가 없다 — 그대로 넘기면 된다. 가변 인수는 「많이 받기」보다 **한 층을 그냥 통과시키기**에 값이 있다.

## 경계와 오해

- **`Object... args` ≠ 인수 여러 개** — 넘어가는 것은 **배열 한 개**다. 호출마다 배열이 새로 만들어지므로 아주 잦은 경로에서는 그 생성 비용이 드러난다. 「문법 설탕이라 공짜」로 읽으면 설명되지 않는다 → [[array]]
- **`...` 는 마지막에만 온다** — `input(Object... args, String format)` 은 컴파일 오류다. 그래서 형식 문자열이 앞에 오는 `printf(format, args)` 모양이 사실상 강제된다.
- **배열을 넘기면 펼쳐지지 않는다** — `Object[]` 를 가변 인수 자리에 넘기면 **그 배열이 곧 `args`** 다. Day17 의 `inputInt(format, args)` 와 Day58 의 `insert(sql, values)` 가 둘 다 이 성질로 동작하고, 반대로 배열 하나를 「원소 한 개」로 넘기고 싶으면 `new Object[]{arr}` 로 감싸야 한다. **얇은 위임 메서드가 한 줄로 써지는 이유가 이것**이고, 이 성질이 없다면 두 코드는 배열을 풀어 다시 넘기는 반복문을 각각 가져야 했다.
- **`Object...` 로 받으면 개수만 자유롭고 타입은 사라진다** — 받는 쪽이 아는 것은 「`Object` 몇 개」이므로 **원소마다 다른 처리를 하려면 다시 타입을 알아내야 한다.** Day58 의 세션이 그 자리에서 걸려 값을 전부 `value.toString()` + `setString` 으로 보내고, 그 결과 숫자·날짜·`null` 이 전부 문자열로 DB 에 간다. 답은 `instanceof` 로 갈래를 만드는 것이 아니라 **타입 판단을 아는 쪽으로 넘기는 것**이다(`stmt.setObject(i, value)`). 「무엇이든 받는다」가 「무엇이든 다룰 수 있다」로 읽히는 자리다 → [[instanceof-operator]] · [[prepared-statement]]
- **인수 하나로 `null` 을 넘기면 배열 자체가 `null` 이 된다** — `insert(sql, null)` 은 「값 하나가 `null`」이 아니라 **`values == null`** 로 넘어가고(컴파일러가 `null` 을 배열로 해석한다), 그다음 `for (Object v : values)` 가 `NullPointerException` 이다. 「인수를 안 넘기면 길이 0 배열」이라는 성질과 어긋나 보이는 예외이며, 값 하나를 `null` 로 보내려면 `insert(sql, (Object) null)` 로 캐스팅해야 한다 → [[type-casting]]
- **형식 문자열과 인수 개수가 맞는지 컴파일러가 보지 않는다** — `input("이름(%s):")` 은 컴파일되고 실행 중에 `MissingFormatArgumentException` 이 난다. 가변 인수는 개수를 자유롭게 해 주는 대신 **개수 검사를 실행 시점으로 옮긴다** → [[exception-handling]]
- **`format + " "` 은 형식 문자열을 손댄 것이다** — 프롬프트 뒤에 공백을 붙이려고 이어 붙였는데, 이 자리에 오는 문자열은 **형식으로 해석된다.** 부르는 쪽이 `%` 가 든 문장을 넘기면 값이 아니라 형식 지시자로 읽힌다. 값은 반드시 `args` 로 보내야 한다.
- **`Object` 로 받는 것은 타입 검사를 포기하는 것이다** — 무엇이든 받으므로 `%d` 자리에 `String` 을 넘겨도 컴파일된다. 안 맞으면 실행 중에 `IllegalFormatConversionException` 이다 → [[type-casting]]
- **`invoke(obj, null)` 은 「인수 없음」으로 읽히고, 그래서 실수가 오류로 드러나지 않는다** — `null` 이 `Object[]` 로 해석되므로 위의 「인수 하나로 `null` 을 넘기면 배열 자체가 `null` 이 된다」와 같은 문법인데, `invoke` 쪽에서는 그것이 **인수 없는 메서드를 부르는 정상 형태**가 된다. 즉 값 하나로 `null` 을 넘기려던 코드가 예외 없이 **다른 메서드 호출**이 되어 `NoSuchMethodException` 이나 「왜 값이 안 들어갔나」로 나타난다. 값 하나를 `null` 로 주려면 `new Object[]{null}` 이다 → [[reflective-invocation]]
- **가변 인수 메서드를 리플렉션으로 찾을 때는 배열 타입으로 찾는다** — `void m(int... a)` 는 컴파일 뒤에 `void m(int[] a)` 이므로 `getMethod("m", int[].class)` 다. 시그니처에 `...` 라는 것은 남지 않는다 — **「선언에서는 `...`, 본문에서는 배열」이라는 이 문법의 첫 성질이 클래스 파일에서도 그대로**여서, 리플렉션 쪽에서는 `...` 를 쓴 메서드와 배열을 쓴 메서드가 구별되지 않는다(`m.isVarArgs()` 로만 갈린다). Day59 는 호출 쪽만 적고 찾는 쪽은 다루지 않았다 → [[reflective-invocation]] · [[class-file-format]]
- **감싼 메서드가 실패 지점을 감춘다** — `inputInt` 는 `Integer.parseInt` 를 품고 있는데 예외를 다루지 않는다. 부르는 쪽에서는 「숫자를 받아 주는 편한 메서드」로 보이지만 숫자가 아닌 입력에 그대로 죽는다. 가변 인수와는 별개의 문제이면서, **얇은 위임 메서드를 만들 때 같이 봐야 하는 자리**다 → [[number-parsing]]

## 함께 보는 개념

- [[parameter-and-argument]] — 받는 자리와 넘기는 값
- [[parameterization]] — 호출부가 정할 범위를 넓히는 앞 단계
- [[array]] — 가변 인수의 실체
- [[method]] — 이 문법이 붙는 자리
- [[number-parsing]] — `inputInt` 가 감싸는 일
- [[package]] — `Prompt` 가 `util` 로 간 이유
- [[static-member]] — `Prompt` 의 멤버가 전부 `static` 인 것
- [[sql-session]] — 같은 문법으로 SQL 값 목록을 받는 쪽
- [[prepared-statement]] — 타입을 잃은 값이 도착하는 곳
- [[instanceof-operator]] — `Object` 로 받은 것의 타입을 되찾으려 할 때 손이 가는 문법
- [[reflective-invocation]] — 이 문법 위에 서 있는 `invoke`. 같은 성질이 함정이 되는 자리

## 출처

- [[2024-06-18-Day17]] — 여러 클래스가 쓰는 입력 메서드를 `util.Prompt` 로 옮기면서 `input(String format, Object... args)` 로 만들고, 받은 `args` 를 `printf` 에 그대로 흘려보내 프롬프트 문구와 끼워 넣을 값을 부르는 쪽이 정하게 하는 것을 실습으로 배웠다. `inputInt` 가 `input(format, args)` 로 배열을 그대로 다시 넘기는 것도 이 자리다
- [[2024-08-19-Day58]] — 두 달 뒤. 같은 문법이 **SQL 의 `?` 에 채울 값 목록**을 받는 자리에 다시 나타난다. `insert(String sql, Object... values)` 는 받은 배열을 `for` 로 하나씩 꺼내 바인딩하고, `update`·`delete` 는 `return insert(sql, values)` 한 줄로 배열을 그대로 흘려보낸다 — Day17 의 `inputInt` 와 같은 통과이며, **꺼내 쓰는 쪽과 흘려보내는 쪽이 한 클래스 안에 나란히** 있는 첫 예다. 동시에 이 회차가 이 문법의 대가를 드러낸다: `Object` 로 받았으므로 `setInt`·`setDate` 를 고를 근거가 없어 값을 전부 `value.toString()` + `setString` 으로 보낸다. 필기는 그것을 문제로 적지 않았고 `setObject` 도 나오지 않는다 → [[sql-session]]
- [[2024-08-20-Day59]] — 하루 뒤. 리플렉션의 `Method.invoke(Object obj, Object... args)` 가 이 문법으로 만들어져 있어서, 「메서드 파라미터」 절이 `m.invoke(null, "홍길동", 100, 90, 80)` 과 `m.invoke(null, new Object[] {"홍길동", 100, 100, 100})` 을 **같은 뜻으로** 나란히 적는다 — 「배열을 넘기면 펼쳐지지 않는다」의 세 번째 사례다. 그런데 여기서는 그 성질이 **처음 함정 쪽으로 나타난다**: 배열 하나를 값 하나로 넘기려면 한 겹 더 감싸야 하고, 필기가 그것을 「배열의 파라미터인 경우는 배열에 담아서 전달해야한다」·「가변 파라미터의 경우에도 배열에 담아서 전달해야한다」 두 줄로 적었다(이유는 적지 않았다). Day17·Day58 이 이 성질로 **얇은 위임 메서드를 한 줄로** 쓴 것과 정확히 반대 방향의 쓰임이다. `invoke(obj, null)` 이 「인수 없음」으로 읽히는 것과 가변 인수 메서드를 `int[].class` 로 찾아야 하는 것은 다루지 않았다 → [[reflective-invocation]]
