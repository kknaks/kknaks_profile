---
type: concept
id: exception-handling
title: 예외 처리 (Exception Handling)
aliases:
  - 예외
  - 예외처리
  - exception
  - try catch
  - InputMismatchException
up:
  - 2024-06-11-Day11
  - 2024-06-11-Day12
  - 2024-06-13-Day14
  - 2024-07-18-Day38
  - 2024-07-19-Day39
  - 2024-08-05-Day48
  - 2024-08-30-Day67
tags:
  - spring
  - java
  - 예외
  - 문법
---

# 예외 처리 (Exception Handling)

실행 중에 생긴 오류로 프로그램이 멈추는 것을 막고, **그 상황에서 할 일을 따로 적는** 문법. 정상 흐름과 오류 흐름을 갈라 쓰는 것이다.

## 정의

```java
try {
    // 정상 코드
} catch (예외타입 ex) {
    // 예외가 발생했을 때 할 일
}
```

`try` 블록에서 예외가 나면 **그 줄에서 멈추고** 바로 `catch` 로 넘어간다. 뒤에 남은 정상 코드는 실행되지 않는다. `catch` 는 선언한 타입과 맞는 예외만 잡는다.

## 사용 예시

`nextInt()` 는 숫자가 아닌 입력에서 `InputMismatchException` 을 던진다 → [[standard-input]]. 그것을 잡아 안내를 출력하고 루프를 계속 돌린다.

```java
Scanner keyboard = new Scanner(System.in);
int menuNo;

while (true){
    System.out.print("> ");
    try{
        menuNo = keyboard.nextInt();
        if (menuNo >= 1 && menuNo <= menus.length){
            if (menus[menuNo - 1].equals("종료")){
                break;
            }
            System.out.printf("%d. %s\n",menuNo, menus[menuNo -1]);
        } else {
            System.out.println("유효한 메뉴 번호가 아닙니다.");
        }
    } catch(InputMismatchException ex){
        System.out.println("숫자로 메뉴 번호를 입력하세요.");
        keyboard.next();          // 키보드 버퍼 초기화
    }
}
```

`catch` 안의 `keyboard.next()` 가 이 예시의 핵심이다. 예외를 잡기만 하고 이 줄이 없으면, 잘못 입력한 문자가 `Scanner` 버퍼에 그대로 남아 다음 회차의 `nextInt()` 가 **같은 예외를 다시** 던진다 — 안내 문구만 무한히 출력되는 루프가 된다.

다만 원본 주석의 「버퍼 초기화」는 정확한 말이 아니다. **`next()` 는 토큰 하나만 비운다** — 잘못 입력한 것이 `abc def` 였다면 `def` 가 남아 다음 회차에서 같은 예외가 또 난다. 줄 전체를 버려야 온전히 정리된다 → [[standard-input]]

### 예외가 나지 않는 방식으로 바꾸는 것도 예외 처리다

다음 회차에서 이 필기는 같은 문제를 **`catch` 를 손대지 않고** 해결했다. 숫자를 직접 읽는 대신 한 줄을 문자열로 받고, 그것을 해석하는 쪽으로 옮긴 것이다.

```java
String command;
while (true){
    System.out.print("> ");
    command = keyboard.nextLine();       // 줄 전체를 읽어 버린다 — 버퍼에 남는 것이 없다
    try{
        if (command.equals("menu")){
            System.out.println("메뉴실행");
        } else {
            int menuNo = Integer.parseInt(command);
            ...
        }
    } catch(NumberFormatException ex){
        System.out.println("숫자로 메뉴 번호를 입력하세요.");
    }                                    // 버퍼를 비우는 줄이 사라졌다
}
```

**`keyboard.next()` 가 없어졌다.** 잘못된 입력이 버퍼에 남지 않으므로 `catch` 가 정리할 상태가 아예 없다 → [[standard-input]] · [[number-parsing]]

### try 의 범위를 좁히면 흐름 제어가 밖으로 나온다

그 다음 실습에서 같은 루프를 서브메뉴용으로 옮겨 쓸 때, `try` 가 감싸는 범위가 줄었다. 초안은 루프 본문 전체를 감쌌다.

```java
while (true) {
    String command = prompt("메인/" + menuTitle);
    try {
        if (command.equals("menu")) { ... continue; }
        else if (command.equals("9")) { break; }
        int menuNo = Integer.parseInt(command);       // 예외가 날 수 있는 줄
        ...
    } catch (NumberFormatException ex) { ... }
}
```

최종 코드는 특별 명령 처리를 `try` **앞으로** 내보내고, 숫자 해석과 조회만 남겼다.

```java
while (true) {
    String command = prompt("메인/" + menuTitle);
    if (command.equals("menu")) { ... continue; }     // try 밖
    else if (command.equals("9")) { break; }          // try 밖

    try {
        int menuNo = Integer.parseInt(command);
        String subMenuTitle = getMenuTitle(menuNo, menus);
        ...
    } catch (NumberFormatException ex) {
        System.out.println("숫자로 메뉴 번호를 입력하세요.");
    }
}
```

**`try` 블록에 남은 것이 실제로 예외를 던질 수 있는 코드뿐이다.** `continue`·`break` 가 `try` 안에 있어도 동작은 같지만, 범위가 넓으면 「이 `catch` 가 무엇을 감당하는가」를 읽을 때 블록 전체를 훑어야 한다 → [[command-loop]]

### 다섯 주 뒤 — 안 잡으면 컴파일이 안 되는 예외를 처음 만난다

Day11~Day14 의 예외는 셋 다 잡지 않아도 컴파일되는 것들이었다(`InputMismatchException`·`NumberFormatException`). Day38 의 `IOException` 은 다르다 — **잡거나 던지겠다고 선언하거나, 둘 중 하나를 안 하면 컴파일되지 않는다.**

```java
  public byte[] getBytes() throws IOException {     // 안 잡고 밖으로 넘긴다
    try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
      return out.toByteArray();
    }
  }
```

```java
private void saveUser() {
    try (FileOutputStream out = new FileOutputStream("user.data")) {
      /* 쓴다 */
    } catch (IOException e) {                        // 여기서 잡는다
      System.out.println("회원 정보 저장 중 오류 발생" + e.getMessage());
    }
  }
```

**두 형태가 한 노트 안에 나란히 있다.** `getBytes`·`valueOf` 는 자기 자리에서 할 수 있는 일이 없어 넘기고, `saveUser`·`loadUser` 는 사용자에게 알릴 수 있는 자리라 잡는다 — **어디서 잡을지가 「어디서 났나」가 아니라 「어디서 뭘 할 수 있나」로 정해지는 것**이 여기서 처음 코드로 나타난다.

그리고 `try` 괄호에 자원을 선언한 형태가 처음 나오는데, **`catch` 가 없어도 성립한다**는 것이 위 첫 코드다 → [[try-with-resources]]

### 하루 뒤 — 예외를 「끝을 아는 수단」으로 쓴다

Day39 의 CSV 로딩은 파일 끝을 판정하는 데 **예외를 쓴다.**

```java
      while (true) {
        try {
          String csv = in.nextLine();
          userList.add(User.valueOf(csv));
        } catch (Exception e) {
          break;
        }
      }
```

`Scanner.nextLine()` 은 더 읽을 줄이 없으면 `NoSuchElementException` 을 던지고, 그것을 잡아 루프를 나간다. **`while (in.hasNextLine())` 이라고 쓰면 예외가 필요 없는 자리**인데 예외를 흐름 제어로 쓴 것이고, 대가는 `catch (Exception e)` 로 **모든 것을 같이 잡게 된다**는 것이다 → [[csv]] · [[while-loop]]

같은 노트에 `catch` 가 **처음으로 상태를 되돌리는** 코드도 있다.

```java
        } catch (IOException  | ClassNotFoundException e) {
        System.out.println("회원 정보 로딩 중 오류 발생" + e.getMessage());
        userList = new ArrayList<>();
        }
```

`userList = new ArrayList<>();` 한 줄이 Day11 의 「어떤 상태를 되돌려야 다시 시도할 수 있는가」에 이 파일 층에서 처음 답한 것이다. 그리고 `|` 로 두 예외를 한 `catch` 에 묶는 **멀티 catch** 가 처음 나오는데, 둘을 묶을 수 있는 것은 **할 일이 같아서**다 — 「무엇이 났나」가 아니라 「무엇을 할 것인가」가 `catch` 를 가르는 기준임이 문법으로 나타난 자리다 → [[serialization]]

### 17일 뒤 — `catch` 블록이 비어 있는 형태가 처음 나온다

Day48 의 모든 `try` 가 이 모양이다. 쓰레드를 배우는 회차에서 여섯 번 반복된다.

```java
try { Thread.sleep(500); } catch(Exception e) {}
```

Day39 의 `catch (Exception e) { break; }` 는 넓게 잡았어도 **흐름은 정했다.** 여기는 블록 자체가 비어 있어 「없던 일로 하고 계속」이다. 그리고 **이 예외는 오류가 아니라 신호**여서, 삼키는 대가가 앞선 회차들과 종류가 다르다 → [[thread]]

| | 잡은 것 | `catch` 가 해야 할 일 |
|---|---|---|
| Day11 `InputMismatchException` | 사용자가 잘못 입력했다 | 상태를 **되돌린다**(버퍼를 비운다) |
| Day38 `IOException` | 파일이 안 됐다 | 알리거나 **넘긴다** |
| Day48 `InterruptedException` | **누군가 이 쓰레드를 멈추려 한다** | 신호를 **전달한다** |

`InterruptedException` 은 「자는 데 실패했다」가 아니라 「그만하고 나와라」는 요청이고, **던져지는 순간 JVM 이 그 쓰레드의 인터럽트 표시를 지운다.** 그래서 빈 `catch` 는 아무 일도 안 하는 것이 아니라 **표시를 하나 지우고 계속 도는 것**이다. 같은 노트의 「쓰레드 안전종료 - interrupt()메서드 이용」 절이 제목만 남아 있는데, **그 절이 쓸 도구를 이 노트의 나머지 코드가 이미 무력화해 두었다** → [[thread-state]]

`join()` 쪽 빈 `catch` 는 결과까지 망친다.

```java
try {
  sumThread.join();
} catch (InterruptedException e) {

}
System.out.println("1~100 합: " + sumThread.getSum());   // 안 기다렸는데 읽는다
```

**기다림이 중단된 것과 상대가 끝난 것이 같은 다음 줄로 흘러간다** → [[thread-join]]

**예외 처리가 없으면 사용자가 문자 하나만 잘못 넣어도 프로그램이 죽는다.** [[standard-input]] 의 `nextInt()` 가 그 자리다. 잡아서 안내하고 다시 묶는 것이 CLI 프로그램의 기본 형태고, 그래서 예외 처리와 [[while-loop]] 이 짝으로 나온다.

더 값 있는 것은 **예외를 잡는 것과 예외가 남긴 상태를 정리하는 것이 다른 일**이라는 발견이다. `catch` 는 흐름만 돌려놓고 **상태는 되돌려 주지 않는다** — 버퍼는 그대로, `menuNo` 는 갱신되지 않은 채다. 이 필기가 `keyboard.next()` 를 부르며 실제로 만난 것이 그것이고, "잡았으니 해결됐다"로 넘어가면 무한 루프가 된다.

### 오류를 화면으로 넘기는 형태

Day67 이 모든 서블릿을 같은 골격으로 감싼다 — **잡아서 화면에 넘긴다.**

```java
} catch (Exception e) {
  req.setAttribute("exception", e);
  req.getRequestDispatcher("/error.jsp").forward(req, res);
}
```

```jsp
<pre>
<%
Exception e = (Exception) request.getAttribute("exception");
if (e != null) {
    e.printStackTrace(new PrintWriter(out));
}
%>
</pre>
```

**Day61~66 이 `out.println("<p>오류!</p>")` 로 한 줄 찍던 것에서 스택 트레이스 전체로 바뀌었다.** 개발 중에는 이게 훨씬 낫다 — 원인이 화면에 그대로 나온다.

**그리고 그것이 그대로 배포되면 문제가 된다.** 스택 트레이스에는 클래스 이름·파일 경로·SQL 문장·때로는 값까지 들어 있어서, **공격자에게 시스템 구조를 알려 주는 화면**이 된다. 「개발에서 편한 것」과 「사용자에게 보일 것」이 갈리는 자리이고, 필기는 그 구분을 두지 않는다 → [[sql-injection]]

**게다가 이 `forward` 는 자주 실패한다** — `try` 가 JSP `include` 까지 감싸므로, 렌더링 중에 난 예외는 응답이 이미 나간 뒤라 넘길 수 없다 → [[request-dispatcher]]

## 경계와 오해

- **예외를 잡는 것이 고치는 것은 아니다** — 원인이 남아 있으면 다음 회차에 같은 예외가 다시 난다. 위 예시에서 버퍼를 비우지 않으면 정확히 그렇게 된다. `catch` 블록에서 물어야 하는 것은 "무엇을 출력할까"가 아니라 **"어떤 상태를 되돌려야 다시 시도할 수 있는가"** 다.
- **`try` 블록은 중간에서 끊긴다** — 예외 뒤의 코드는 건너뛴다. 위 코드에서 `nextInt()` 가 실패하면 `menuNo` 는 이전 값 그대로 `catch` 로 간다. `try` 안의 여러 줄이 다 실행됐다고 가정하면 안 된다.
- **`catch` 는 타입이 맞아야 잡는다** — `InputMismatchException` 을 잡아도 다른 예외는 그대로 올라가 프로그램을 멈춘다. 반대로 `Exception` 으로 다 잡으면 예상하지 않은 오류까지 삼켜서 문제를 감춘다.
- **예외 ≠ 컴파일 오류** — 문법은 완전한데 실행 중에 난다. `NullPointerException`([[object-reference]])·`ArrayIndexOutOfBoundsException`([[array]])도 그쪽이다.
- **예외를 안 던지는 오류가 더 무섭다** — 정수 [[overflow]] 는 예외 없이 값만 틀린다. 예외가 나는 것은 **알려 주는 쪽**이고, 조용히 어긋나는 것보다 다루기 쉽다.
- **어떤 예외가 나는지는 「입력이 잘못됐다」가 아니라 「어떻게 읽었는가」가 정한다** — 같은 잘못된 입력인데 `nextInt()` 는 `InputMismatchException`, `Integer.parseInt()` 는 `NumberFormatException` 이다. **읽는 방법만 바꾸고 `catch` 타입을 그대로 두면 예외가 잡히지 않아 프로그램이 죽는다** — 컴파일은 그대로 되므로 실행해 봐야 안다 → [[number-parsing]]
- **더 나은 해결은 `catch` 를 잘 쓰는 것이 아니라 `catch` 가 감당할 상태를 줄이는 것이다** — 이 필기는 하루 사이에 두 답을 만났다. 먼저 `catch` 안에서 버퍼를 비웠고, 다음에는 **버퍼에 남지 않는 입력 방식으로 바꿨다.** 뒤쪽이 나은 이유는 예외를 안 쓰기 때문이 아니라 **정리해야 할 상태가 없어져서** 잊을 수 있는 단계가 사라졌기 때문이다.
- **`try` 로 감싸는 범위가 넓으면 어디서 났는지 흐려진다** — 위 예시는 루프 본문 전체를 감쌌는데, 잡고 싶은 것은 `nextInt()` 한 줄의 실패다. 범위가 넓을수록 `catch` 가 감당해야 하는 상태의 종류가 늘어난다. 서브메뉴 실습에서 실제로 좁혀 보면 예외와 무관한 분기가 `try` 밖으로 나온다 → 「사용 예시」
- **`try` 를 좁히는 것은 성능이 아니라 읽기의 문제다** — `try` 블록에 들어가는 것 자체에 비용이 있는 것이 아니다. 좁혀서 얻는 것은 **`catch` 가 책임지는 범위가 코드 모양으로 드러난다**는 것뿐이고, 그것이 「잡았으니 됐다」로 넘어가지 않게 막아 준다.
- **체크 예외 ≠ 잡아야 하는 예외** — `IOException` 을 「반드시 잡아야 하는 것」으로 외우면 Day38 의 `getBytes()` 가 설명되지 않는다. 컴파일러가 요구하는 것은 **잡기 또는 `throws` 선언**이고, 둘 다 정당한 답이다. 잡는 쪽을 고르는 기준은 「그 자리에서 되돌릴 것이 있는가」이며, 아무것도 못 하는 자리에서 잡으면 **호출한 쪽이 실패를 모르게 만드는 것**이 된다 → [[method]]
- **`catch` 에 적은 타입이 실제로 날 예외를 다 덮는다는 보장은 없다 — Day38 이 그 반례다** — `loadUser` 는 `catch (IOException e)` 로 「로딩 중 오류」를 찍고 넘어가게 짜였는데, 파일이 중간에서 잘리면 `in.read()` 가 `-1` 을 주고 길이가 `-1` 이 되어 `new byte[-1]` → `NegativeArraySizeException`, 안쪽에서는 `in.read(buffer, 0, -1)` → `IndexOutOfBoundsException` 이 난다. **둘 다 `RuntimeException` 이라 이 `catch` 를 통과해 프로그램을 죽인다.** Day12 의 「읽는 방법만 바꾸고 `catch` 타입을 그대로 두면 잡히지 않는다」와 같은 종류인데, 이번에는 **읽는 방법이 아니라 입력이 깨졌을 때** 갈린다 — 정상 입력만으로 시험하면 절대 드러나지 않는다 → [[length-prefix-framing]] · [[serialization]]
- **잡아서 찍고 넘어가면 부른 쪽은 실패를 모른다 — 그리고 이번에는 되돌릴 상태가 디스크에 있다** — `saveUser` 의 `catch` 는 메시지만 찍으므로 호출부는 저장이 됐다고 여기고 계속 돈다. 게다가 `new FileOutputStream("user.data")` 는 여는 순간 기존 파일을 비우므로 **옛 데이터도 없고 새 데이터도 반쪽인 파일**이 남고, 다음 실행의 `loadUser` 가 그것을 읽으려 한다. Day11 의 「어떤 상태를 되돌려야 다시 시도할 수 있는가」가 같은 물음인데, 답이 `keyboard.next()` 한 줄이었던 자리와 달리 **여기서는 프로그램 밖의 파일을 되돌려야 한다** — 임시 파일에 쓰고 성공하면 이름을 바꾸는 것이 그 답이다 → [[try-with-resources]] · [[serialization]]
- **예외를 흐름 제어로 쓰면 「끝났다」와 「틀렸다」가 한 갈래가 된다 — Day39 가 그 값을 치른다** — `catch (Exception e) { break; }` 는 파일 끝(`NoSuchElementException`)에서 나오려고 쓴 것인데, **`Integer.parseInt` 실패(`NumberFormatException`)·조각 부족(`ArrayIndexOutOfBoundsException`)도 같은 문으로 들어와 똑같이 `break`** 한다. 중간 한 줄이 깨지면 **거기서 읽기를 멈추고 뒤의 회원들을 조용히 버리며 메시지도 남기지 않는다.** 그리고 다음 저장이 그 잘린 목록으로 파일을 덮어써 **손실이 확정된다** — 「읽기 오류」가 「데이터 삭제」가 되는 경로다. Day11 의 「`Exception` 으로 다 잡으면 문제를 감춘다」가 **감추는 것으로 끝나지 않고 지우는 데까지 간 사례**이고, `while (in.hasNextLine())` 로 끝을 판정하면 이 갈래가 애초에 생기지 않는다 → [[csv]] · [[number-parsing]] · [[array]]
- **예외가 「제대로」 잡히게 된 것이 더 조용한 손실을 만들 수도 있다** — Day38 의 잘린 파일은 `RuntimeException` 으로 프로그램을 죽여서 **최소한 저장을 못 하게 막았다.** Day39 의 `readInt`·`readUTF` 는 `EOFException`(=`IOException`)을 던지므로 기존 `catch` 에 얌전히 걸리는데, **그 전까지 `userList.add(user)` 한 회원들은 목록에 남아** 프로그램이 반쪽 목록으로 계속 돌고 다음 저장이 그것을 확정한다. **「예외가 잡힌다」가 「상태가 온전하다」와 다르다** — 되읽기는 임시 목록에 담고 끝까지 성공했을 때만 넘겨야 한다 → [[data-io-stream]] · [[serialization]]
- **예외를 삼키는 것은 「아무 일도 안 하는 것」이 아니다 — 상태를 하나 지운다** — 빈 `catch` 는 코드가 없으니 부작용도 없어 보이는데, `InterruptedException` 은 **잡히는 순간 인터럽트 표시가 지워진다.** 즉 이 빈 블록은 「멈춰라」는 요청을 **없애 버린다.** 결과가 「멈추라고 했는데 안 멈추는 프로그램」이고, 종료 버튼이 안 듣는 서버가 이렇게 만들어진다. Day11 의 「잡는 것이 고치는 것은 아니다」와 방향이 반대다 — 여기서는 잡는 것이 **원래 있던 정보를 지운다** → [[thread]] · [[thread-state]]
- **처음으로 되돌릴 것이 아니라 「넘길 것」이 있는 예외다** — Day11 부터 `catch` 에서 물어 온 것이 「어떤 상태를 되돌려야 다시 시도할 수 있는가」였는데, 이 예외의 답은 되돌리기가 아니라 **전달**이다. 잡은 자리에서 끝낼 수 없으면 다시 던지거나, 못 던지는 자리라면 `Thread.currentThread().interrupt()` 로 표시를 다시 세워 **위층이 볼 수 있게** 남긴다. 「잡았으니 끝」이 이 예외에서는 **다른 코드의 기능을 없애는 일**이 된다.
- **잡을 것이 하나뿐인데 `Exception` 으로 잡았다** — `Thread.sleep()` 이 던지는 체크 예외는 `InterruptedException` 하나다. 넓게 잡아 이득이 없고, 대신 `run()` 안에서 난 다른 실행 시점 예외까지 같은 문으로 들어올 수 있다. Day39 의 「`Exception` 으로 다 잡으면 감춘다」가 여기서는 **감춘 것을 기록조차 안 하는 형태**로 나타난다 — 블록이 비어 있어 `e` 를 쓰는 곳이 없다.
- **정상 상태가 오류 메시지를 내는 자리가 생겼다** — 첫 실행에는 `user.data` 가 없어 `FileNotFoundException` 이 나고 그것도 `IOException` 이라 같은 `catch` 로 들어와 「회원 정보 로딩 중 오류 발생」을 찍는다. **「파일이 아직 없다」와 「파일이 깨졌다」가 한 `catch` 에 묶여 있어서** 사용자에게도 같은 화면이고 코드에도 구별이 없다. 타입 하나로 잡는 범위를 정하는 것의 한계이고, `Exception` 으로 다 잡는 것과 같은 성질의 문제가 한 단계 좁은 자리에서 나타난 것이다.

## 함께 보는 개념

- [[exception-handler]] — 웹에서 이 처리를 표식으로 옮긴 장치

- [[standard-input]] — 예외를 던지는 `nextInt()` 가 있는 곳
- [[while-loop]] — 잡고 다시 시도하는 흐름을 만드는 짝
- [[object-reference]] — `NullPointerException` 이 나는 자리
- [[array]] — 인덱스 범위 예외가 나는 자리
- [[overflow]] — 예외 없이 값만 틀리는 대비되는 경우
- [[number-parsing]] — `NumberFormatException` 을 던지는 쪽
- [[command-loop]] — `try` 가 감싸는 범위를 고르게 되는 자리
- [[try-with-resources]] — 자원을 닫는 일이 `catch` 와 갈리는 문법
- [[serialization]] — 되돌릴 상태가 디스크에 있는 경우
- [[length-prefix-framing]] — 깨진 입력이 예상 밖 예외를 던지는 자리
- [[csv]] — 끝 판정을 예외에 맡긴 형식
- [[data-io-stream]] — 스트림 끝을 예외로 알리는 층
- [[thread]] — 예외가 오류가 아니라 신호로 오는 자리
- [[thread-join]] — 빈 `catch` 가 결과를 망치는 경로

## 출처

- [[2024-10-17-Day95]] — **`try-catch` 가 표식으로 바뀌는 자리.** 스프링 MVC 에서는 컨트롤러를 감싸는 대신 `@ExceptionHandler` 를 붙인 메서드를 두면 되고, 던져진 예외 타입에 맞는 메서드가 선택된다 — **catch 절의 타입 매칭이 메서드 선택으로 옮겨간 형태**다. 그리고 처리 주체가 넷으로 계층을 이룬다(페이지 컨트롤러 → `@ControllerAdvice` → `web.xml` → 서블릿 컨테이너) → [[exception-handler]]
- [[2024-06-11-Day11]] — `try` / `catch` 구조와 `nextInt()` 의 `InputMismatchException` 을 잡는 것, 그리고 `catch` 에서 `keyboard.next()` 로 키보드 버퍼를 비워야 같은 예외가 반복되지 않는다는 것을 실습으로 배웠다
- [[2024-06-11-Day12]] — 입력을 줄 단위로 받고 `Integer.parseInt` 로 해석하도록 바꾸면서 잡는 예외가 `NumberFormatException` 으로 바뀌고 `catch` 에서 버퍼를 비우는 줄이 필요 없어진다는 것을 배웠다
- [[2024-06-13-Day14]] — 서브메뉴 루프를 만들면서 `try` 가 루프 본문 전체를 감싸던 초안을 특별 명령 처리(`menu`·`9`)를 밖으로 내보내고 숫자 해석과 조회만 남기도록 좁혔다
- [[2024-07-18-Day38]] — 파일 입출력 실습에서 **잡거나 선언하지 않으면 컴파일되지 않는 예외(`IOException`)를 처음 만난다.** `getBytes`·`valueOf` 는 `throws IOException` 으로 넘기고 `saveUser`·`loadUser` 는 `catch (IOException e)` 로 잡아 메시지를 찍는데, **두 답이 한 노트 안에 나란히 있어 「어디서 잡을지」가 「어디서 뭘 할 수 있나」로 정해지는 것**이 드러난다. `try` 괄호에 자원을 선언하는 형태도 이 회차가 처음이고 `catch` 없이 쓰는 예가 함께 있다. 다만 그 `catch` 가 실패를 부른 쪽에 전달하지 않고, 첫 실행의 `FileNotFoundException` 이 오류 메시지로 나오며, 파일이 깨졌을 때 나는 `NegativeArraySizeException`·`IndexOutOfBoundsException` 은 `IOException` 이 아니라 이 `catch` 를 통과한다 — 필기는 이 셋을 다루지 않았다
- [[2024-08-30-Day67]] — 서블릿 전체가 `try` / `catch (Exception e)` 로 감싸이고, `catch` 가 예외를 요청 속성에 담아 `error.jsp` 로 `forward` 한다. `error.jsp` 는 `e.printStackTrace(new PrintWriter(out))` 로 스택 트레이스를 화면에 그대로 찍는다 — 개발 중에는 유용하지만 배포되면 시스템 구조가 노출된다. 그리고 `try` 가 `include` 까지 감싸고 있어 **렌더링 중에 난 예외는 그 `forward` 자체가 실패한다**
- [[2024-08-05-Day48]] — **`catch` 블록이 비어 있는 형태가 처음 나온다** — `try { Thread.sleep(500); } catch(Exception e) {}` 가 여섯 번, `join()` 쪽 `catch (InterruptedException e) { }` 가 한 번이다. 그리고 잡히는 것이 오류가 아니라 **「멈춰라」는 신호**여서 삼킨 대가가 앞선 회차들과 종류가 다르다 — `InterruptedException` 은 던져질 때 인터럽트 표시가 지워지므로 **빈 `catch` 는 신호를 없애고 계속 돈다.** 같은 노트의 「쓰레드 안전종료 - interrupt()메서드 이용」 절이 제목만 남아 있는데, 그 절이 쓸 도구가 나머지 코드에서 이미 무력화돼 있다. `join()` 쪽 빈 블록은 **기다림이 중단됐는데 결과를 읽는** 경로를 만든다. 필기는 「실행 대기 중에 메서드가 호출되면 InerruptedException이 발생한다」로 **누가 왜 던지는지**를 흐리게 적었고, 잡은 뒤에 무엇을 해야 하는지는 다루지 않았다
- [[2024-07-19-Day39]] — 예외의 쓰임이 셋 늘어난다. ① **흐름 제어** — CSV 로딩이 `while (true)` 안에서 `catch (Exception e) { break; }` 로 파일 끝을 판정해, 형식 오류까지 같은 문으로 들어와 뒤의 회원을 조용히 버린다. ② **멀티 catch** — `catch (IOException | ClassNotFoundException e)` 로 두 예외를 묶고, 그 `catch` 가 `userList = new ArrayList<>()` 로 **처음으로 상태를 되돌린다.** ③ **끝을 알리는 방식의 변화** — `readInt`·`readUTF` 가 부족한 입력에서 `EOFException` 을 던져 Day38 의 `RuntimeException` 경로가 없어지는데, 잡힌 뒤에도 반쪽 목록이 남아 다음 저장이 그것을 확정한다. 필기는 예외를 쓰기만 하고 이 셋 중 어느 것도 설명하지 않았다
