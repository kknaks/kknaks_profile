---
type: concept
id: io-stream
title: 입출력 스트림 (I/O Stream)
aliases:
  - 입출력 스트림
  - io stream
  - 바이트 스트림
  - byte stream
  - 표준 출력
  - standard output
  - stdout
  - stderr
  - System.out
  - 파일 스트림
  - FileOutputStream
  - FileInputStream
up:
  - 2024-06-11-Day12
  - 2024-07-18-Day38
  - 2024-07-19-Day39
  - 2024-07-23-Day41
  - 2024-07-30-Day45
tags:
  - java
  - 입출력
  - cli
---

# 입출력 스트림 (I/O Stream)

데이터가 한 방향으로 흐르는 **통로**. 읽는 쪽이 입력 스트림, 쓰는 쪽이 출력 스트림이고, **통로 끝에 무엇이 있든 부르는 메서드는 같다.**

## 정의

이 필기는 통로가 바뀌어도 호출이 그대로임을 이렇게 정리했다.

```java
입력스트림.read(); //return 값으로 1byte를 읽어온다.
//System.in   -> consol키보드 입력으로 부터 읽는다.
//파일입력스트림  -> 파일 입력으로 부터 읽는다.
//소켓입력스트림  -> 네트워크로 부터 읽는다.

출력스트림.println("Hello");
//System.out   -> consol창으로 출력
//파일입력스트림  -> 파일로 출력
//소켓입력스트림  -> 네트워크로 출력
```

프로그램은 시작할 때 **표준 스트림 세 개**를 기본으로 받는다.

| 이름 | Java | 쓰임 |
|---|---|---|
| 표준 입력 (stdin) | `System.in` | 값을 받는다 → [[standard-input]] |
| 표준 출력 (stdout) | `System.out` | 결과를 내보낸다 |
| 표준 오류 (stderr) | `System.err` | 오류를 내보낸다 |

세 통로는 **프로그램 밖에서 갈아 끼울 수 있다.** 키보드 대신 다른 프로그램의 출력을 받을 수 있고, 그것이 파이프다 — 이 필기가 확인한 것이 "파이프라인을 통해 stdout 을 stdin 으로 넘겨 받는 경우"다.

## 사용 예시

Java 코드는 `System.in` 을 읽는 것 하나뿐인데, 실행하는 쪽이 통로를 바꿔 준다.

```bash
java App              # stdin = 키보드
echo "3" | java App   # stdin = 앞 프로그램의 stdout
java App < input.txt  # stdin = 파일
```

**코드를 고치지 않았다.** 프로그램은 "표준 입력에서 읽는다"까지만 알고, 그 끝에 무엇이 붙는지는 실행할 때 정해진다 → [[cli]]

### 다섯 주 뒤, 통로 끝이 실제로 파일이 된다

Day12 가 표로만 적어 둔 「파일입력스트림 → 파일 입력으로 부터 읽는다」를 Day38 이 처음 코드로 쓴다.

```java
    try (FileOutputStream out = new FileOutputStream("user.data")) {
      int userLength = userList.size();
      out.write(userLength >> 8);
      out.write(userLength);
      /* 레코드들을 쓴다 */
    }
```

```java
    try (FileInputStream in = new FileInputStream("user.data")) {
      int userLength = in.read() << 8 | in.read();
      /* 레코드들을 읽는다 */
    }
```

**`read()`·`write()` 가 Day12 에 배운 그대로다.** 새로 배우는 것은 통로를 만드는 방법(생성자에 파일 이름) 과 그것을 닫는 방법뿐이고, 「입출력을 배우는 비용이 한 번으로 끝난다」가 실제로 확인되는 자리다 → [[try-with-resources]]

같은 스트림 계열이지만 통로 끝이 **메모리**인 것도 이 회차에 함께 나온다.

```java
    try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
      out.write(no >> 24);
      /* ... */
      return out.toByteArray();
    }
```

`out.write(...)` 네 줄만 보면 파일에 쓰는 코드와 구별되지 않는다 — **통로 끝을 모르는 것이 이 추상화의 목적이고, 그래서 같은 필드 쌓기 코드를 파일용·메모리용으로 두 벌 쓰지 않는다** → [[byte-array-stream]]

### 하루 뒤 — 통로에 껍데기를 끼우는 것이 이 계열의 조립 방식이라는 것이 드러난다

Day12·Day38 은 「통로 끝이 무엇이든 같은 메서드」를 확인했다. Day39 는 **통로 위에 층을 쌓는 축**을 보여 준다.

```java
    try (FileInputStream in0 = new FileInputStream("user.data");
        DataInputStream in = new DataInputStream(in0)) {          // 통로 + 타입 해석 층
```

```java
    try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("user.data"))) {
```

```java
    try (Scanner in = new Scanner(new FileReader("user.csv"))) {  // 통로 + 문자 층 + 파서 층
```

**세 줄 다 안쪽은 파일이고 밖에 씌운 것만 다르다.** 안쪽을 `System.in` 이나 소켓으로 바꿔도 밖의 껍데기는 그대로 쓰이므로, **「통로 종류 × 형식 종류」를 클래스로 다 만들지 않아도 된다** — Day39 가 앞 절에서 배운 데코레이터 패턴이 정확히 이 자리에 쓰여 있고, 필기가 「Data I/O Stream처럼 데코레이터 패턴을 통해」로 스스로 이어 붙였다 → [[decorator-pattern]] · [[data-io-stream]] · [[character-stream]]

그리고 이 회차에 **계열이 하나 더 있다는 것**이 나온다 — `FileReader`·`FileWriter` 는 `InputStream`·`OutputStream` 이 아니라 `Reader`·`Writer` 쪽이다. Day12 의 「1바이트를 읽는다」가 통하지 않는 층이고, 그래서 Day12 때 「문자·줄 단위로 읽어 주는 층이 위에 따로 있다」로 남겨 둔 자리가 여기서 채워진다 → [[character-stream]]

### 나흘 뒤 — 실습으로 쓰던 것을 계열 전체로 훑는다

Day38~Day40 은 회원 목록을 저장하는 실습 안에서 필요한 만큼만 썼다. Day41 은 반대 방향이다 — **`java.io` 를 다섯 무리로 늘어놓고 각 무리의 메서드를 하나씩 짚는다.**

| Day41 의 章 | 무엇을 다루나 | 이 노트와의 관계 |
|---|---|---|
| §1 `java.io.File` | 파일의 **내용이 아니라 존재·속성·목록** | 통로 밖 → [[file-class]] |
| §2 Byte Stream | `FileOutputStream`·`FileInputStream` | **이 노트가 통로라 부르는 것** |
| §3 Character Stream | `FileWriter`·`FileReader` | 별개 계열 → [[character-stream]] |
| §4 Data Stream | `writeInt`·`readUTF` | 타입을 아는 껍데기 → [[data-io-stream]] |
| §5 Buffer Stream | 호출 횟수를 줄이는 껍데기 | → [[buffered-stream]] |

**§1 이 나머지 넷과 층이 다르다는 것이 이 배치에서 드러난다** — `File` 은 바이트를 나르지 않고 「그 파일이 있나·크기가 얼마인가·이 폴더에 뭐가 있나」에만 답한다. 통로를 열기 전에 물을 것이 따로 있다는 것이고, Day38~Day40 의 코드에는 그 층이 아예 없었다(저장 파일이 처음 없는 첫 실행을 다루지 않았다) → [[file-class]]

그리고 **읽기·쓰기 메서드가 세 벌씩이라는 것이 여기서 표로 정리된다.**

| 쓰기 | 읽기 | 단위 |
|---|---|---|
| `write(int)` | `read()` | 1바이트 |
| `write(byte[])` | `read(byte[])` | 배열 전체 |
| `write(byte[], off, len)` | `read(byte[], off, len)` | 배열의 일부 |

Day38 이 세 형태를 섞어 쓰면서도 왜 셋인지는 적지 않았던 자리다. 필기의 예제가 같은 배열로 세 형태를 연달아 보여 준다.

```java
    byte[] bytes = {0x7a, 0x6b, 0x5c, 0x4d, 0x3e, 0x2f, 0x30};
    out.write(0x7a6b5c4d); // 0X4d만 출력(1byte)만 출력한다.
    out.write(bytes);      // 7a 6b 5c 4d 3e 2f 30
    out.write(bytes, 2, 3);// 5c 4d 3e
```

**첫 줄의 주석이 Day38 에서 이 노트가 지적한 것을 필기가 스스로 확인한 자리다** — `write(int)` 가 상위 세 바이트를 말없이 버린다. Day38 은 그것을 「1바이트만 저장할 수 있다」로 적었고, 여기서는 `0x7a6b5c4d` 를 넣어 **버려지는 것을 눈으로 본다** → [[bit-shift]] · [[overflow]]

읽는 쪽도 세 형태가 나란히 있고, **스트림이 위치를 기억한다는 것**이 그 자리에서 보인다.

```java
    // test.text = 7a 6b 5c 4d 3e 2f 30
    int b = in.read(); // 7a
    in.read(buf,0,2);  // 6b 5c
    in.read(buf);      // 4d 3e 2f 30 
```

**세 호출이 이어서 읽는다.** 어디서부터 읽을지를 인자로 주지 않는데도 앞의 것을 다시 읽지 않는 것이 「통로」라는 말의 실질이고, 파일을 배열처럼 인덱스로 다루는 것과 갈리는 자리다 → [[byte-array-stream]]

### 일주일 뒤 — 표의 세 번째 줄이 실물이 된다

Day12 의 표에 「소켓입력스트림 → 네트워크로 부터 읽는다」가 있었다. Day45 가 그 통로를 만든다.

```text
OutStream -> 랜카드 -> InputStream
```

**필기가 데이터의 흐름을 스트림 두 개로 그린 것이 정확하다** — 소켓은 통로가 아니라 통로 **두 개**를 가진 물건이고, 내가 쓴 출력 스트림이 상대의 입력 스트림으로 이어진다. 아래 「스트림은 한 방향이다」가 여기서 코드로 확인되는 자리다 → [[socket]]

그런데 **Day45 에는 그 스트림을 꺼내는 코드가 없다.** `getInputStream()`·`getOutputStream()` 없이 연결까지만 만들고 끝나므로, 이 노트에 대해 그 회차가 더하는 것은 새 메서드가 아니라 **통로 끝의 종류 하나**다. 그리고 그 종류가 앞의 세 종류(콘솔·파일·메모리)와 갈리는 자리가 아래 세 항목에 있다 — **호출은 같은데 성질이 다른 첫 통로**다.

## 왜 중요한가

**입출력을 배우는 비용이 한 번으로 끝난다.** 콘솔·파일·네트워크가 각각 다른 방법을 요구한다면 세 번 배워야 하지만, 전부 스트림이라 `read()`·`write()` 를 아는 것으로 통한다. Day45 에서 소켓을 다룰 때 새로 배운 것은 실제로 **통로를 만드는 방법**뿐이었고 읽고 쓰는 방법은 그대로였다 → [[client-server-model]] · [[socket]]

**다만 「그대로다」는 호출에 대해서만 참이다.** Day12~Day41 의 통로는 넷 다 「끝이 있고, 요청한 만큼 읽히고, 다시 열면 처음부터 읽을 수 있는」 것이었다. 소켓은 셋 다 아니다 — 아래 「소켓 스트림」 항목이 그 목록이고, **호출이 같다는 것이 성질까지 같다는 뜻은 아니라는 것**이 이 회차에서 처음 실제 통로로 드러난다.

그리고 이 구조가 **프로그램을 조립할 수 있게 만든다.** 각 프로그램이 stdin 에서 읽어 stdout 으로 내보내기만 하면, 파이프로 이어 붙이는 것만으로 새 도구가 된다. CLI 도구들이 작게 유지되는 이유가 이것이고, 반대로 화면에 직접 그리는 프로그램은 이렇게 이어 붙일 수 없다.

## 경계와 오해

- **Java 8 의 Stream API 와 다른 것이다** — `list.stream().filter(...)` 의 스트림은 **컬렉션의 원소를 흘려보내는 처리 파이프라인**이고, 여기서 말하는 스트림은 **바이트가 흐르는 입출력 통로**다. 이름만 같고 상속 관계도 없다. 검색할 때 섞여 나오는 대표적인 자리다.
- **`read()` 가 읽는 1바이트는 한 문자가 아니다** — 한글은 UTF-8 에서 3바이트라 한 번의 `read()` 로 못 읽는다. 그래서 문자·줄 단위로 읽어 주는 층(`Reader`·`Scanner`)이 위에 따로 있다 → [[character-encoding]] · [[standard-input]] · [[character-stream]]
- **`Reader`·`Writer` 는 이 노트의 스트림을 상속하지 않는다 — 이름만 「스트림」인 별개 계열이다** — Day39 의 `FileReader` 는 `InputStream` 이 아니라 `Reader` 의 자식이라 `read()` 가 돌려주는 것이 **바이트가 아니라 `char`**(0~65535)다. 두 계열을 잇는 것은 상속이 아니라 **변환 껍데기**(`InputStreamReader`·`OutputStreamWriter`)이고, 그 껍데기가 인코딩을 적용하는 자리다. 「스트림이면 다 같은 것」으로 읽으면 `FileInputStream` 을 `Scanner` 에 넣을 수 있는 이유와 `FileReader` 를 `DataInputStream` 에 넣을 수 없는 이유가 설명되지 않는다 → [[character-stream]] · [[character-encoding]]
- **껍데기를 씌우면 「닫을 것」이 여러 개가 되고 순서가 생긴다** — 안쪽만 닫으면 껍데기가 들고 있던 것이 나가지 않고, 껍데기를 닫으면 안쪽까지 닫힌다. Day39 는 `try (FileInputStream in0 = …; DataInputStream in = …)` 로 둘을 선언해 **역순으로**(껍데기 먼저) 닫게 했다. 통로가 한 겹일 때는 없던 문제이고, 조립 가능한 구조가 치르는 비용이다 → [[try-with-resources]] · [[decorator-pattern]]
- **`read()` 의 반환 타입은 `byte` 가 아니라 `int` 다** — 0~255 의 값과 "더 읽을 것이 없다"(`-1`)를 한 타입으로 구별해야 하기 때문이다. 스트림의 끝을 값으로 알린다.
- **`write(int)` 도 `int` 를 받지만 이유가 반대다** — Day38 의 필기가 「write(int) int 타입을 받지만 1바이트만 읽고 저장할 수 있다」로 정확히 적었다. `read()` 의 `int` 는 **표현할 값의 범위를 늘리려고** 있고, `write(int)` 의 `int` 는 **넘어온 값을 잘라 버리려고** 있다. 그래서 `out.write(no >> 24)` 처럼 상위 비트가 남아 있는 값을 넘겨도 되고, 반대로 `out.write(300)` 은 예외 없이 `44` 를 쓴다. **한쪽은 넓혀서 정보를 지키고 다른 쪽은 말없이 버린다** — 같은 타입이 반대 일을 하는 자리다 → [[bit-shift]] · [[overflow]]
- **`read(byte[])` 가 요청한 만큼 읽어 준다는 보장은 없다** — Day38 의 `in.read(bytes)` 는 반환값을 버리는데, 그 반환값이 **실제로 읽은 개수**다. 로컬 파일에서는 대개 다 채워지므로 이 코드가 동작하지만 **명세상 보장이 아니고**, 통로를 네트워크로 바꾸면 짧게 읽히는 일이 흔하다. 「통로 끝이 무엇이든 부르는 메서드가 같다」는 이 노트의 출발점이 **호출이 같다는 뜻이지 성질까지 같다는 뜻은 아니라는 것**이 여기서 갈린다. 다 채우는 것을 보장하려면 반환값을 세며 반복하거나 `readNBytes`·`DataInputStream.readFully` 를 쓴다. 같은 회차의 `ByteArrayInputStream` 쪽에서는 배열이 이미 메모리에 있어 이 위험이 없다 — **두 줄이 똑같이 생겼는데 안전한 이유가 다르다** → [[byte-array-stream]] · [[serialization]]
- **버퍼를 감싸지 않으면 `read()` 한 번이 시스템 호출 한 번이다 — 나흘 뒤 Day41 이 그 겹을 배운다** — `FileInputStream` 을 그대로 쓰면 `no` 하나를 읽는 데 `read()` 를 4번 부르고 회원 한 명에 십수 번이다. Day38·Day39 는 그 겹을 쓰지 않고, Day40 이 `BufferedReader` 를 끼우지만 그것은 「줄 단위로 읽으려고」였다. **Day41 §5 가 처음으로 「호출 횟수를 줄이려고 겹을 끼운다」를 목적으로 설명한다** — 그래서 Day38 의 코드에 빠진 것이 이 노트의 추측이 아니라 **같은 필기 안의 뒤 회차가 답을 갖고 있는 자리**가 된다. **「바이너리라 빠르다」와 「통로에 몇 번 접근하나」는 다른 축**이고, 뒤쪽이 대개 더 크게 영향을 준다 → [[buffered-stream]] · [[binary-io]] · [[caching]]
- **통로를 열기 전에 물을 것이 따로 있다 — 그 층이 Day38~Day40 코드에는 없다** — `new FileInputStream("user.data")` 는 파일이 없으면 `FileNotFoundException` 이므로, **첫 실행에서 저장 파일이 없는 것이 정상인데 예외 경로로 들어온다.** Day41 §1 의 `File.exists()`·`isFile()` 이 그 판단을 예외 없이 하게 해 주는 층이고, 스트림에는 그것이 없다. **통로는 「열고 흐르게 하는 것」까지만 알고 「그 끝에 무엇이 있나」는 다른 클래스가 안다** → [[file-class]] · [[exception-handling]]
- **`new FileOutputStream(name)` 은 여는 순간 파일을 비운다** — 이어 쓰려면 두 번째 인자로 `true` 를 줘야 한다. **통로를 만드는 일이 이미 데이터를 지우는 일**이라 「열기만 했다」가 안전한 동작이 아니다 → [[try-with-resources]]
- **스트림은 바이트만 알고 타입 규칙은 모른다** — `int` 를 4바이트로 쪼개는 것도, 상위 바이트를 먼저 보내는 것도 스트림이 정해 주지 않는다. Day38 이 그것을 손으로 짠 것이고, 표준에서 그 층을 맡는 것은 `DataOutputStream`·`DataInputStream` 이다. **「통로」와 「통로에 흘려보낼 형식」이 다른 층**이라는 것이 `println` 이 `PrintStream` 의 메서드인 것과 같은 구조다 → [[binary-io]] · [[serialization]]
- **stdout 과 stderr 은 둘 다 화면에 보이지만 다른 통로다** — 파이프와 리다이렉션이 넘기는 것은 stdout 뿐이라, 오류를 stderr 로 내보내면 데이터에 섞이지 않는다. `System.out.println` 으로 오류를 찍으면 다음 프로그램이 그것을 데이터로 받는다.
- **스트림은 한 방향이다** — 입력 스트림으로 쓸 수 없고 출력 스트림에서 읽을 수 없다. 양방향으로 보이는 소켓도 실제로는 입력용과 출력용 스트림 두 개이고, **Day45 의 「OutStream -> 랜카드 -> InputStream」이 그 두 개를 그린 것**이다. 그래서 내 출력 스트림에 쓴 것을 내 입력 스트림에서 읽을 수 없다 → [[socket]]
- **소켓 스트림은 이 노트의 다른 통로들과 성질이 셋 다르다** — 호출은 같으므로 코드만 보면 구별되지 않는데, (1) `read(byte[])` 가 요청한 만큼 안 채우는 것이 **정상**이고, (2) 끝이 없어서 「읽을 것 없음」이 `-1` 대신 **막힘**으로 나타나고, (3) 흘러간 바이트를 다시 읽을 수 없다. 파일 통로에서 「대개 되니까」로 넘어갔던 것들이 여기서 전부 실제 문제가 된다 — **같은 코드가 통로를 바꾸는 것만으로 깨지는 첫 자리**이고, 그래서 「어디까지가 한 메시지인가」를 보내는 쪽이 알려 줘야 한다 → [[socket]] · [[length-prefix-framing]] · [[network-protocol]]
- **`println` 은 스트림의 메서드가 아니라 그것을 감싼 것의 메서드다** — `System.out` 은 `PrintStream` 인스턴스이고 `println` 은 거기에 있다. 통로 자체는 바이트만 알고, 문자열·숫자를 바이트로 바꾸는 일은 감싸는 쪽이 한다 → [[static-member]]

## 함께 보는 개념

- [[standard-input]] — 세 통로 중 입력 쪽과 그것을 읽는 도구
- [[cli]] — 통로를 갈아 끼우는 환경
- [[character-encoding]] — 바이트와 문자가 1:1 이 아닌 이유
- [[client-server-model]] — 통로가 네트워크가 되는 경우
- [[socket]] — 그 통로를 만드는 클래스와 그것이 주는 두 스트림
- [[network-protocol]] — 흘려보낼 것의 순서와 경계를 정하는 약속
- [[static-member]] — `System.out.println` 의 호출이 두 층인 이유
- [[byte-array-stream]] — 통로 끝이 메모리인 경우
- [[binary-io]] — 통로에 흘려보낼 형식을 정하는 층
- [[serialization]] — 그 형식을 객체 단위로 정하는 작업
- [[try-with-resources]] — 통로를 닫는 문법
- [[bit-shift]] — `write(int)` 에 1바이트씩 넘기는 도구
- [[decorator-pattern]] — 통로에 층을 쌓는 구조
- [[data-io-stream]] — 타입을 아는 껍데기
- [[character-stream]] — 문자가 흐르는 다른 계열
- [[buffered-stream]] — 통로에 몇 번 접근하나를 줄이는 껍데기
- [[file-class]] — 통로를 열기 전에 파일을 묻는 층

## 출처

- [[2024-06-11-Day12]] — `입력스트림.read()` 가 1바이트를 돌려준다는 것, 콘솔·파일·소켓이 같은 호출로 다뤄진다는 것, 표준 입출력이 세 통로로 제공되며 파이프로 stdout 을 stdin 으로 넘길 수 있다는 것을 배웠다
- [[2024-07-18-Day38]] — Day12 가 표로만 적어 둔 「파일입력스트림」을 처음 코드로 쓴다 — `FileOutputStream("user.data")` 와 `FileInputStream("user.data")` 로 통로를 만들고 `read()`·`write()` 는 그대로 쓴다. 같은 회차에 통로 끝이 메모리인 `ByteArrayOutputStream`·`ByteArrayInputStream` 도 나와 **같은 호출이 세 종류의 끝에 붙는 것**이 한 노트 안에서 확인된다. 「write(int) int 타입을 받지만 1바이트만 읽고 저장할 수 있다」로 `write` 가 상위 비트를 버린다는 것을 배웠고, 반대로 `in.read(bytes)` 의 반환값을 무시하고 `BufferedInputStream` 으로 감싸지 않은 것과 바이트 순서·타입 규칙을 손으로 짠 것이 이 코드에 그대로 남아 있다
- [[2024-07-19-Day39]] — 통로에 **껍데기를 씌우는 축**이 나온다 — `new DataInputStream(in0)`·`new ObjectInputStream(new FileInputStream(...))`·`new Scanner(new FileReader(...))` 세 형태가 한 노트에 있고, 필기가 「Data I/O Stream처럼 데코레이터 패턴을 통해 File I/O Stream으로 내보낼 수 있다」로 앞 절의 패턴과 직접 이어 붙였다. Day12 가 「문자·줄 단위로 읽어 주는 층이 위에 따로 있다」로 남겨 둔 자리에 `Reader`·`Writer` 계열이 들어오는데, 그것이 `InputStream` 의 하위가 아니라 **별개 계열**이라는 것은 필기에 적히지 않았다. `BufferedInputStream`·`BufferedWriter` 를 끼우지 않은 것은 Day38 과 같다
- [[2024-07-23-Day41]] — 실습 안에서 필요한 만큼만 쓰던 것을 **계열 전체의 강의로 다시 훑는다** — `java.io.File` · Byte Stream · Character Stream · Data Stream · Buffer Stream 다섯 무리를 순서대로 놓아 **어느 것이 통로이고 어느 것이 껍데기인지, 그리고 `File` 은 아예 다른 층인지**가 배치로 드러난다. `write(int)`·`write(byte[])`·`write(byte[], off, len)` 세 형태를 같은 배열로 연달아 보여 주고, `out.write(0x7a6b5c4d)` 의 주석에 「0X4d만 출력」이라 적어 **Day38 에서 지적된 상위 바이트 버림을 눈으로 확인한다.** 읽는 쪽 세 호출이 이어서 읽히는 것도 주석에 남아 스트림이 위치를 기억한다는 것이 보인다. §5 에서 처음으로 **버퍼를 「호출 횟수를 줄이려고」 끼우는 것**이 목적으로 설명되어 Day38·Day39 에 빠져 있던 겹의 답이 같은 필기 안에서 채워진다. 다만 클래스 이름을 `BufferedFileInputStream`·`DataFileOutputStream` 으로 적고 껍데기를 「상속받아 사용한다」로 설명해 **위임 구조를 상속으로 읽었다**
- [[2024-07-30-Day45]] — Day12 의 표에 적혀 있던 「소켓입력스트림 → 네트워크로 부터 읽는다」가 **실제 통로**가 된다. 「실제 데이터 전송은 OutStream -> 랜카드 -> InputStream으로 이루어진다」로 소켓이 스트림 **두 개**를 갖는 것을 그림으로 잡았고(이 노트의 「스트림은 한 방향이다」가 코드로 확인되는 자리다), 통로를 만드는 방법만 새로 배우고 읽고 쓰는 방법은 그대로라는 이 노트의 예측이 여기서 확인된다. 다만 **확인되는 것은 호출까지**다 — 짧게 읽히는 것·끝이 없는 것·되돌아가지 못하는 것이 파일 통로와 갈리는데 그 셋은 필기에 없다. 그리고 이 회차에는 `getInputStream()`·`getOutputStream()` 을 부르는 코드가 아예 없어 **통로를 연 것까지가 전부**다
