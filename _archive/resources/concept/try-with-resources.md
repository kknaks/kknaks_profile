---
type: concept
id: try-with-resources
title: try-with-resources (자원 자동 닫기)
aliases:
  - try with resources
  - 자원 자동 닫기
  - AutoCloseable
  - Closeable
  - close
  - 자원 반납
up:
  - 2024-07-18-Day38
  - 2024-07-19-Day39
  - 2024-07-23-Day41
  - 2024-08-16-Day57
tags:
  - java
  - 문법
  - 예외
  - 입출력
---

# try-with-resources (자원 자동 닫기)

**`try` 뒤 괄호에 선언한 자원을 블록에서 나갈 때 자동으로 닫아 주는 문법.** 어떤 경로로 나가든 — 정상 종료·`return`·예외 — `close()` 가 불린다.

## 정의

```java
try (자원 out = new 자원()) {
    // 쓴다
}   // 여기서 out.close() 가 불린다
```

- 괄호에 선언한 것은 `AutoCloseable` 을 구현한 타입이어야 한다.
- **`catch` 는 없어도 된다.** 닫는 것과 잡는 것이 별개의 일이기 때문이다.
- `catch`·`finally` 가 있으면 **그것들보다 먼저** 닫힌다.
- 여럿 선언하면 **선언의 역순**으로 닫힌다(나중에 연 것이 먼저 닫힌다 — 감싼 스트림이 안쪽보다 먼저 닫혀야 하기 때문이다).

Day38 의 코드는 이 문법을 네 번 쓰고 그중 두 형태가 다 나온다 — `catch` 가 없는 것과 있는 것.

```java
  public byte[] getBytes() throws IOException {          // catch 없음 → 예외는 밖으로
    try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
      return out.toByteArray();
    }
  }
```

```java
private void saveUser() {
    try (FileOutputStream out = new FileOutputStream("user.data")) {   // catch 있음
      /* 쓴다 */
    } catch (IOException e) {
      System.out.println("회원 정보 저장 중 오류 발생" + e.getMessage());
    }
  }
```

## 사용 예시

**`return` 이 `try` 안에 있는데 닫힌다** — 이 문법의 값이 가장 짧게 드러나는 자리다.

```java
  public byte[] getBytes() throws IOException {
    try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
      //객체의 정보들을 byte로 담는다.
      return out.toByteArray();
    }
  }
```

같은 것을 `finally` 로 쓰면 이렇게 된다.

```java
  public byte[] getBytes() throws IOException {
    ByteArrayOutputStream out = new ByteArrayOutputStream();
    try {
      byte[] result = out.toByteArray();     // 반환값을 임시 변수에 받아 두어야 한다
      return result;
    } finally {
      out.close();                           // 여기서 예외가 나면 위 예외를 덮어쓴다
    }
  }
```

**늘어난 것이 세 줄이 아니라 세 가지다** — 자원 선언이 `try` 밖으로 나가 유효 범위가 넓어지고, 반환값을 담을 변수가 생기고, `close()` 에서 난 예외가 본문의 예외를 지운다 → [[variable-scope]]

`saveUser`·`loadUser` 는 진짜 OS 자원을 다룬다.

```java
    try (FileOutputStream out = new FileOutputStream("user.data")) {
      /* 회원 수와 레코드들을 쓴다 */
    } catch (IOException e) {
      System.out.println("회원 정보 저장 중 오류 발생" + e.getMessage());
    }
```

**쓰다가 예외가 나도 파일은 닫힌다.** `catch` 로 들어올 때는 이미 닫혀 있으므로 `catch` 안에서 정리할 것이 없다 → [[exception-handling]]

### 하루 뒤 — 자원을 겹쳐 쓰는 두 형태가 한 노트에 나란히 있다

Day38 은 자원이 늘 하나였다. Day39 는 통로에 껍데기를 씌우므로 **자원이 둘**이 되고, 필기가 그것을 **두 가지 다른 방법으로** 적었다.

```java
    try (FileInputStream in0 = new FileInputStream("user.data");
        DataInputStream in = new DataInputStream(in0)) {          // ① 따로 선언
```

```java
    try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("user.data"))) {
                                                                  // ② 한 식에 중첩
```

**①은 「선언의 역순으로 닫힌다」가 실제로 필요해지는 첫 코드다** — `DataInputStream` 이 먼저 닫히고 그 다음 `FileInputStream` 이 닫힌다. 껍데기가 안쪽보다 먼저 닫혀야 껍데기가 들고 있던 것이 통로로 나갈 수 있다.

**②는 안쪽이 새어 나갈 수 있는 형태다.** 괄호에 선언된 것은 `ObjectInputStream` 하나뿐이므로, `new FileInputStream(...)` 은 성공하고 `new ObjectInputStream(...)` 이 예외를 던지면 **이미 열린 파일을 아무도 닫지 않는다.** 그리고 `ObjectInputStream` 의 생성자는 실제로 예외를 던질 수 있다 — 만들 때 파일 앞의 헤더를 읽기 때문에 파일이 비었거나 다른 형식이면 그 자리에서 실패한다. **①과 ②가 같은 노트 안에 있고 둘 다 컴파일되며, 안전한 쪽은 ①뿐이다** → [[decorator-pattern]] · [[data-io-stream]]

### 스무나흘 뒤 Day57 — 괄호가 받을 수 있는 것이 「선언뿐」이라는 것이 구조를 정한다

닫아야 할 것이 파일에서 **DB 연결·문장·결과 커서**로 옮겨 오고(→ [[jdbc]]), Day57 의 DAO 에 **같은 자원 짝이 두 형태로** 나타난다. Day39 의 ①②와 달리 이번에 갈리는 이유는 안전이 아니라 **사이에 낄 문장이 있는가**다.

```java
try (PreparedStatement stmt = con.prepareStatement(select 쿼리문);
        ResultSet rs = stmt.executeQuery()) {          // list() — 값을 넣을 것이 없다
```

```java
try (PreparedStatement stmt = con.prepareStatement(select 쿼리문)) {
  stmt.setInt(1, no);                                  // findBy() — 이 줄이 사이에 와야 한다
  try (ResultSet rs = stmt.executeQuery()) {
```

**`try (...)` 의 괄호는 선언 목록만 받는다.** 그래서 `?` 에 값을 바인딩해야 하는 조회는 `ResultSet` 을 **안쪽 `try` 로 내리는 수밖에 없다** — 중첩이 취향이 아니라 문법의 결과다. 두 형태를 갈라 읽는 기준이 하나 생기는 것이 이 회차의 값이다: **뒤 자원이 앞 자원의 「식」만으로 얻어지면 나란히, 앞 자원에 무엇을 해 준 뒤에 얻어지면 중첩** → [[prepared-statement]] · [[result-set]]

닫히는 순서는 여기서도 역순이고, 그것이 필요한 이유는 Day39 의 껍데기와 같다 — **`ResultSet` 은 자기를 만든 `Statement` 가 살아 있어야 유효하다.** `Statement` 를 먼저 닫으면 남은 행을 읽을 수 없다.

**그리고 이 회차에는 이 문법이 닿지 않는 자원이 하나 있다.** §1.5.3 의 트랜잭션 예제는 `Connection` 을 `try (...)` 에 넣지 않고 `finally` 에서 `con.setAutoCommit(true); con.close();` 로 손수 닫는다. **`close()` 만으로 부족한 것이 있기 때문**이다 — 자동 커밋 설정을 되돌리는 일은 이 문법이 해 주지 않는다 → [[transaction]]

## 왜 중요한가

**GC 가 대신해 줄 수 없는 일이 이것이다.** Day11 이 「메모리가 아닌 자원(파일 핸들·소켓·DB 커넥션)은 GC 에 맡길 수 없고 `close()` 로 직접 돌려줘야 한다」로 남겨 두고, Day21 의 `finalize()` 가 그 훅처럼 보였지만 **불린다는 보장이 없어** 답이 되지 못했다. 그 자리에 들어오는 것이 이 문법이다 — **회수 시점을 JVM 이 정하는 것과 달리, 블록을 나가는 시점은 코드가 정한다** → [[garbage-collection]] · [[object-class]]

**닫기를 잊을 수 있는 경로가 없어진다.** 손으로 쓰면 출구마다 `close()` 를 두어야 하고, 출구는 `return`·예외·`break` 로 늘어난다. Day31·Day35 의 `push`/`pop` 짝이 정확히 그 문제로 깨졌다 — 예외가 `pop` 을 건너뛰어 경로가 한 칸 깊어진 채 남았고 아무도 알려 주지 않았다. **같은 종류의 문제인데 자원 쪽은 문법이 해결하고 있다**는 것이 대비되는 자리다 → [[stack]]

**「닫아야 한다」가 타입으로 표현된다.** `AutoCloseable` 을 구현했다는 것 자체가 「이건 반납할 것이 있다」는 선언이고, 그러면 `try (...)` 에 넣으라는 신호가 된다. 문서를 읽고 아는 것에서 **타입을 보고 아는 것**으로 옮겨 온 것이다 → [[interface]]

## 경계와 오해

- **`try (...)` 는 예외를 잡는 문법이 아니다** — `getBytes`·`valueOf` 가 `catch` 없이 쓰고 그래서 선언에 `throws IOException` 이 붙는다. 자원은 닫히고 예외는 **그대로 밖으로 나간다.** 「`try` 를 썼으니 예외는 처리됐다」로 읽으면 왜 `throws` 가 필요한지 설명되지 않는다. **닫기와 잡기는 다른 일이고, `catch` 없는 `try` 가 그것을 문법으로 보여 준다** → [[exception-handling]]
- **닫는 것이 전부 자원 반납은 아니다** — `ByteArrayOutputStream.close()` 는 반납할 OS 자원이 없어 사실상 아무 일도 하지 않는다. Day38 은 같은 문법을 `FileOutputStream`(진짜 반납)과 `ByteArrayOutputStream`(no-op)에 똑같이 붙였고 **문법만 보면 구별되지 않는다.** 그래서 메모리 스트림 쪽에서는 `try (...)` 없이 써도 동작이 같고, 파일 쪽에서는 없으면 핸들이 남는다 → [[byte-array-stream]]
- **자원을 닫는 것과 쓴 것을 되돌리는 것은 다르다** — `new FileOutputStream("user.data")` 는 **여는 순간 기존 파일을 0바이트로 비운다.** 그래서 쓰는 중에 예외가 나면 파일은 정상적으로 닫히지만 **옛 데이터는 이미 없고 새 데이터는 반쪽**인 파일이 남는다. 이 문법은 「닫힘」을 보장할 뿐 **「일관된 상태」를 보장하지 않는다** — 임시 파일에 쓴 뒤 성공하면 이름을 바꾸는 것이 그 문제의 표준 답이다 → [[serialization]]
- **`close()` 중의 예외는 삼켜지지 않고 억눌린다** — 본문에서 예외가 나고 닫는 중에도 예외가 나면, **본문 것이 던져지고 닫기 것은 거기 붙어 나간다**(`getSuppressed()` 로 꺼낸다). `finally { out.close(); }` 로 손으로 쓰면 **뒤에 난 예외가 앞의 것을 덮어써 원인이 사라진다.** 이 문법이 손으로 쓴 `finally` 보다 나은 실질적 이유가 코드 줄 수가 아니라 이것이다.
- **괄호 안의 변수는 다시 대입할 수 없다 — 그리고 나흘 뒤 그 제약이 막았을 사고가 실제로 나온다** — 사실상 `final` 이다. 닫을 대상이 도중에 바뀌면 무엇을 닫을지 정할 수 없기 때문이다. Day41 의 `Charset` 비교 예제가 정확히 그 형태를 손으로 짠다 — `FileWriter out` 에 MS949 스트림을 담아 쓰고, **닫지 않은 채 같은 변수에 UTF-16BE 스트림을 덮어씌운다.** 첫 스트림은 아무도 닫지 않아 인코딩 버퍼의 내용이 나가지 않고, 두 번째 생성자가 같은 파일을 열며 0바이트로 비우고, 그것도 닫히지 않는다. **주석에 적힌 두 결과가 둘 다 나올 수 없고 실행하면 빈 파일 하나가 남는데 예외는 없다.** `try (FileWriter out = …)` 로 썼다면 **재대입 자체가 컴파일 오류**여서 두 스트림을 따로 쓰게 강제됐을 것이다 — 이 제약이 「불편한 규칙」이 아니라 **자원 하나에 이름 하나를 묶어 두는 장치**인 자리 → [[character-stream]] · [[variable]]
- **`close()` 를 마지막 줄에 손으로 적는 것은 이 문법이 아니다 — Day41 이 다시 그 형태로 돌아간다** — Day38·Day39 는 모든 입출력을 `try (…)` 로 감쌌는데, Day41 의 예제는 전부 마지막 줄의 `out.close()`·`in.close()` 다. 강의 노트라 짧게 쓴 것으로 읽히지만 **보장되는 것이 달라진다** — 중간에서 예외가 나면 그 줄까지 도달하지 못해 핸들이 남고, 쓰는 쪽이면 버퍼의 내용까지 유실된다. Day41 의 예제 중 여럿은 `throws Exception` 을 달고 있어 **예외가 실제로 밖으로 나갈 수 있는 상태**이고, 그래서 「닫는 줄이 있다」와 「닫힌다」가 갈리는 것이 이 회차의 코드에 그대로 남아 있다. **문법을 배운 뒤에도 예제는 옛 형태로 쓰이는데, 그 차이가 정상 실행에서는 전혀 보이지 않는다** → [[exception-handling]]
- **괄호는 선언만 받는다 — 「자원을 얻은 뒤 손을 봐야 하는」 경우가 중첩을 만든다** — 자원 목록에는 문장을 끼울 수 없어서, `stmt.setInt(1, no)` 같은 준비가 필요한 코드는 뒤 자원을 **안쪽 `try` 로** 내려야 한다. Day57 의 `findBy` 와 `list` 가 그 차이 하나로 갈린다. 「중첩 `try` 는 서투른 코드」로 읽으면 두 자원을 한 괄호에 밀어 넣으려다 **바인딩할 자리를 잃고** 값 없는 문장을 실행하게 된다(`No value specified for parameter 1`) → [[prepared-statement]]
- **이 문법은 `close()` 만 부른다 — 빌려 온 것의 「상태」는 되돌리지 않는다** — DB 연결처럼 **여러 곳이 돌려 쓰는 자원**에는 닫는 일 말고도 원래대로 돌려놓아야 하는 것이 있다(`setAutoCommit(false)` 를 켠 것). Day57 §1.5.3 이 `Connection` 을 괄호에 넣지 않고 `finally` 에서 다루는 것이 그 이유로 읽히고, 실제로 `try (Connection con = ...)` 로 감싸도 자동 커밋 설정은 그대로 남는다. **자원 반납과 상태 복구가 다른 축**이라는 것이 파일에서는 드러나지 않다가 연결에서 드러난다 → [[transaction]] · [[jdbc]]
- **자원을 얻는 코드가 괄호 안에 있어야 보장된다** — `try { out = new FileOutputStream(...); }` 는 이 문법이 아니고 아무것도 닫아 주지 않는다. 보장은 「`try` 블록 안에서 만들었다」가 아니라 **「괄호에서 만들었다」**에 붙는다.
- **자원을 한 식에 중첩하면 보장이 껍데기 하나에만 붙는다** — `new ObjectInputStream(new FileInputStream(f))` 는 **자원 하나로 세어진다.** 안쪽이 만들어진 뒤 밖의 생성자가 실패하면 안쪽은 닫히지 않는다. 이 문법의 보장은 「`try` 블록 안에서 만들었다」가 아니라 **「괄호에 이름을 붙여 선언했다」**에 붙으므로, 겹칠 때는 Day39 §1 처럼 `;` 로 나눠 선언해야 한다. **줄이 짧은 쪽이 더 안전해 보이는데 반대인 자리** → [[io-stream]]
- **감싼 것을 닫으면 안쪽까지 닫힌다 — 그래서 하나만 선언해도 되는 경우와 헷갈린다** — `Scanner.close()` 는 안쪽 `FileReader` 를, `DataOutputStream.close()` 는 안쪽 `FileOutputStream` 을 닫는다. 그래서 **정상 흐름에서는 껍데기 하나만 `try (...)` 에 넣어도 핸들이 남지 않고**, 위 항목의 문제는 **생성 중에 실패할 때만** 나타난다. 「지금까지 문제없었다」가 이 형태를 안전하다고 말해 주지 않는 이유 → [[standard-input]]
- **`close()` 가 자원 반납이 아니라 데이터 완결인 경우가 있다** — `FileWriter` 는 안에 인코딩 버퍼가 있어 `write()` 가 곧 디스크 쓰기가 아니다. 닫지 않으면 **예외도 없이 빈 파일이나 잘린 파일**이 남는다. Day38 의 `ByteArrayOutputStream` 은 닫아도 할 일이 없었고 `FileOutputStream` 은 핸들을 돌려주는 일이었는데, 여기서는 **닫는 것이 저장 그 자체**다. 같은 문법이 자원 종류마다 다른 무게를 갖는다 → [[character-stream]]
- **닫혔다고 `flush` 가 끝난 것이 확인되는 것은 아니다** — `close()` 가 버퍼를 비우다 실패하면 예외를 던지는데, `catch (IOException)` 이 메시지만 찍는 이 코드에서는 **부른 쪽이 저장 실패를 모른다.** 「자동으로 닫혔다」가 「무사히 저장됐다」와 같은 말이 아닌 자리다 → [[exception-handling]]

## 함께 보는 개념

- [[exception-handling]] — `catch`·`finally` 와 순서가 정해지는 짝
- [[garbage-collection]] — 이 문법이 메우는 구멍이 왜 생기는지
- [[object-class]] — 답이 되지 못한 앞의 훅(`finalize()`)
- [[io-stream]] — 닫아야 하는 것들이 사는 층
- [[byte-array-stream]] — 닫아도 할 일이 없는 쪽
- [[serialization]] — 닫힘만으로는 지켜지지 않는 것
- [[stack]] — 같은 「짝 맞추기」 문제가 문법 없이 남은 자리
- [[interface]] — `AutoCloseable` 이 신호가 되는 방식
- [[variable-scope]] — 자원 변수가 사는 범위가 좁아지는 이득
- [[decorator-pattern]] — 자원이 겹쳐지는 구조와 닫는 순서의 이유
- [[data-io-stream]] — 통로와 껍데기를 나란히 선언하는 예
- [[character-stream]] — 닫기가 저장 완결이 되는 자리
- [[buffered-stream]] — 닫지 않으면 데이터가 남아 있는 또 한 겹
- [[variable]] — 자원 변수에 재대입이 막히는 자리
- [[jdbc]] · [[result-set]] · [[prepared-statement]] — 닫아야 할 것이 파일에서 DB 로 옮겨 온 자리
- [[transaction]] — 닫는 것만으로는 되돌려지지 않는 설정

## 출처

- [[2024-07-18-Day38]] — 파일 입출력 실습의 네 메서드가 모두 `try (자원)` 형태로 짜였다. `getBytes`·`valueOf` 는 `catch` 없이 쓰고 `throws IOException` 을 선언에 붙여 **닫기와 잡기가 갈리는 형태**를 보여 주고, `saveUser`·`loadUser` 는 `catch (IOException)` 을 달아 메시지를 찍는다. `getBytes` 가 `return out.toByteArray();` 를 `try` 안에서 하는 것이 이 문법의 값을 그대로 드러낸다. 필기는 이 문법을 설명하지 않고 **쓰기만 했다** — 반납할 것이 없는 `ByteArrayOutputStream` 과 진짜 파일 스트림에 같은 문법이 붙어 있고, `FileOutputStream` 이 열자마자 파일을 비우므로 「닫힘 보장」이 「저장 성공」과 다르다는 것도 이 코드에 그대로 남아 있다
- [[2024-07-19-Day39]] — 통로에 껍데기를 씌우면서 **자원이 둘이 되는 경우가 처음 나오고, 두 형태가 한 노트에 함께 있다.** §1 은 `try (FileInputStream in0 = …; DataInputStream in = new DataInputStream(in0))` 로 나눠 선언해 「선언의 역순으로 닫힌다」가 실제로 쓰이고, §2·§3 은 `new ObjectInputStream(new FileInputStream(...))`·`new Scanner(new FileReader(...))` 처럼 한 식에 중첩해 **밖의 생성자가 실패하면 안쪽이 닫히지 않는 형태**가 된다. §3 의 `FileWriter` 는 닫는 것이 곧 저장 완결이라 이 문법의 무게가 또 다르다. 필기는 세 형태를 쓰기만 하고 차이를 적지 않았다
- [[2024-07-23-Day41]] — 이 문법을 **쓰지 않는다** — 예제 전부가 마지막 줄의 `out.close()`·`in.close()` 이고 `try (…)` 가 한 번도 나오지 않아, Day38·Day39 가 일관되게 쓰던 형태에서 뒤로 간다. 여러 예제가 `throws Exception` 을 달고 있어 예외가 실제로 밖으로 나갈 수 있으므로 **「닫는 줄이 있다」와 「닫힌다」가 갈리는 상태**다. 그리고 `Charset` 비교 예제가 **`FileWriter` 변수에 두 번째 스트림을 재대입**해 첫 것을 닫지 않고 같은 파일을 다시 열어 비우는데, 이 문법의 「괄호 안의 변수는 재대입할 수 없다」 제약이 **그 코드를 컴파일 단계에서 막았을 형태**다. 주석에 적힌 두 관찰 결과는 둘 다 나올 수 없고 실행하면 빈 파일이 남으며 예외는 없다. §5 의 버퍼 스트림 예제도 `in.close()` 를 마지막 줄에 두고, 쓰는 쪽 버퍼와 `flush()` 는 다루지 않았다
- [[2024-08-16-Day57]] — Day41 에서 스무나흘 뒤, **닫아야 하는 것이 파일에서 DB 연결·문장·커서로 바뀐 회차**다. 실습 DAO 다섯 메서드가 전부 `try (Statement …)` 또는 `try (PreparedStatement …)` 로 감싸여 있고, `list()` 는 `PreparedStatement` 와 `ResultSet` 을 **한 괄호에 `;` 로 나란히** 선언하는 반면 `findBy()` 는 `stmt.setInt(1,no)` 가 사이에 들어가야 해서 **`ResultSet` 을 안쪽 `try` 로 내린다** — 괄호가 선언만 받는다는 제약이 코드 구조를 정하는 것을 보여 주는 자리다. 반대로 §1.5.3 의 트랜잭션 예제는 `Connection` 을 이 문법에 넣지 않고 `finally` 에서 `setAutoCommit(true)` 와 `close()` 를 손수 부르는데, 자동 커밋 설정 복구는 `close()` 가 해 주지 않기 때문이다(다만 그 예제는 `con` 을 `try` 안에서 선언해 `finally` 에서 볼 수 없는 상태다). 필기는 두 형태의 차이를 설명하지 않고 코드로만 남겼다
