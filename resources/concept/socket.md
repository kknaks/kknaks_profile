---
type: concept
id: socket
title: 소켓 (Socket)
aliases:
  - 소켓
  - socket
  - 소켓 통신
  - ServerSocket
  - 서버소켓
  - java.net.Socket
up:
  - 2024-07-30-Day45
  - 2024-07-30-Day46
tags:
  - 네트워크
  - java
  - 입출력
  - 통신
---

# 소켓 (Socket)

**두 프로그램 사이에 뚫린 통로의 끝**. 한쪽이 `Socket` 을 만들면 상대의 프로그램까지 이어지고, 그 뒤로는 파일에 쓰던 것과 같은 [[io-stream]] 호출로 데이터가 오간다. Day45 가 「Socket : 입구에 대한 위치」로 적은 것이 이것이다.

## 정의

Day45 는 양쪽이 쓰는 클래스가 **다르다**는 것에서 시작한다.

| 쪽 | 만드는 것 | Day45 의 표현 |
|---|---|---|
| 서버 | `ServerSocket` → 거기서 `Socket` | 「ServerSocket을 생성하고 Socket을 통해 통신」 |
| 클라이언트 | `Socket` 하나 | 「Socket을 생성하여 통신」 |

**서버 쪽만 클래스가 둘인 것이 이 개념의 뼈대다.** `ServerSocket` 은 데이터를 나르지 않고 **연결을 받는 자리**만 맡고, 실제로 읽고 쓰는 것은 그것이 만들어 준 `Socket` 이다.

```java
import java.net.ServerSocket;
// 소켓 설정
ServerSocket serverSocket = new ServerSocket((int) 포트번호,(int) 대기열크기);
System.out.println("서버 실행중...");
// 소켓 접속
Socket socket = serverSocket.accept();
System.out.println("클라이언트 접속");
```

`accept()` 가 **막는다**(blocking). 클라이언트가 붙을 때까지 그 줄에서 멈춰 있고, 붙는 순간 **새 `Socket` 을 돌려준다** — `ServerSocket` 은 닫히지 않고 그대로 남아 다음 `accept()` 를 받을 수 있다. Day45 의 코드가 `accept()` 를 한 번만 부르므로 이 성질은 Day45 에 드러나지 않지만, 「서버」라는 말이 성립하는 근거가 여기다 → [[port-number]]

클라이언트 쪽은 한 줄이다.

```java
Socket socket = new Socket("IP주소",(int) 포트번호);
```

**이 형태에서는 생성자가 곧 접속이다**(같은 날 Day46 이 둘을 가르는 형태를 배운다 — 아래). 객체를 만드는 문법인데 실행되는 동안 네트워크를 타고 상대에게 닿으므로, 이 줄은 시간이 걸리고 실패할 수 있다 — 서버가 안 떠 있으면 `ConnectException` 이 난다. 「어디에」를 정하는 값이 둘 필요하다는 것도 이 줄에 있다 → [[ip-address]] · [[port-number]] · [[exception-handling]]

연결이 생긴 뒤는 이미 배운 것으로 돌아간다.

```text
OutStream -> 랜카드 -> InputStream
```

Day12 가 표로만 적어 둔 「소켓입력스트림 → 네트워크로 부터 읽는다」가 여기서 실물이 된다. **`read()`·`write()` 는 그대로이고 새로 배우는 것은 통로를 만드는 방법뿐**이라는 것이 일곱 주에 걸쳐 확인된 자리다 → [[io-stream]]

### 같은 날 Day46 — 두 줄이 단계로 펼쳐진다

Day45 가 「`ServerSocket` 만들고 `accept()`」 두 줄로 끝낸 것을 Day46 이 순서로 나눈다.

| 단계 | Day46 이 준 것 | 성질 |
|---|---|---|
| 자리 잡기 | 생성자 또는 `bind(new InetSocketAddress(...))` | 바로 끝난다 → [[socket-binding]] |
| 기다리기 | `serverSocket.accept()` | **여기서 막힌다** |
| 상대 확인 | `getRemoteSocketAddress()` → IP·포트 | 연결이 있어야 값이 있다 |
| 닫기 | `serverSocket.close()` | 자리를 내놓는다 |

**네 단계 중 막히는 것이 하나뿐이라는 것이 이 표의 내용이다.** Day46 은 그 하나를 잘못 짚어 「ServerSocket을 생성하면 …블로킹이 된다」로 적었다 → 아래 「경계와 오해」

클라이언트 쪽에서 새로 나온 것은 **생성과 접속을 가를 수 있다**는 것이다.

```java
Socket socket = new Socket();
socket.connect(...);            // 접속을 나중에
```

Day45 의 한 줄짜리 생성자는 이것을 붙여 놓은 편의 형태이고, 가르면 **접속 전에 옵션을 걸거나 타임아웃을 줄 수 있다.** 그래서 「생성자가 곧 접속」은 규칙이 아니라 **그 형태의 성질**이었다. Day46 의 `connect` 호출은 그대로는 컴파일되지 않는다 → [[socket-binding]]

접속이 실패하는 방식도 이름을 얻는다 — Day46 의 「연결 요청 시 두가지 예외가 발생 할 수 있다. UnknownHostException/ IOException」이다. **이름 쪽 실패와 붙는 쪽 실패**의 구별이고, 도메인으로 접속할 때 앞의 것이 나온다 → [[domain-name-system]] · [[exception-handling]]

## 사용 예시

Day45 의 두 조각을 각각 쓰이는 형태로 놓으면 이렇다. 서버는 받을 자리를 만들고 기다린다.

```java
ServerSocket serverSocket = new ServerSocket(8888, 10);
Socket socket = serverSocket.accept();   // 여기서 멈춘다
```

클라이언트는 그 자리를 찾아 붙는다.

```java
Socket socket = new Socket("127.0.0.1", 8888);
```

**두 코드에서 같아야 하는 값은 포트 번호 하나이고, 클라이언트만 IP 를 안다.** 서버는 자기 IP 를 코드에 쓰지 않는다 — 어느 주소로 들어오든 그 포트로 온 것을 받는다. 「서버측 포트 번호는 App에서 설정한다」와 「클라이언트측 포트 번호는 운영체제가 저장한다」가 갈리는 이유가 이 비대칭이다 → [[port-number]]

Day45 의 코드에 **없는 것이 셋**인데, 그 셋이 소켓을 실제로 쓸 때 반드시 나온다.

```java
try (Socket socket = new Socket("127.0.0.1", 8888);
     DataInputStream in = new DataInputStream(socket.getInputStream());
     DataOutputStream out = new DataOutputStream(socket.getOutputStream())) {
  out.writeUTF("명령");
  out.flush();
  String result = in.readUTF();
}
```

(1) **스트림을 꺼내는 두 메서드** — 소켓은 통로 자체가 아니라 통로 **두 개**(읽기·쓰기)를 갖고 있고 그것을 `getInputStream()`·`getOutputStream()` 으로 꺼낸다. (2) **껍데기** — 바이트만 흐르므로 문자열·숫자를 실으려면 Day39·Day41 에 배운 층을 씌운다 → [[data-io-stream]] · [[decorator-pattern]]. (3) **닫기** — `Socket` 은 `Closeable` 이라 `try-with-resources` 에 들어간다 → [[try-with-resources]]

## 왜 중요한가

**프로그램을 두 조각으로 자를 수 있게 된다.** 지금까지 실습이 한 프로세스 안에서 메서드를 부르던 것을, 이 두 클래스로 「부르는 쪽」과 「하는 쪽」을 다른 컴퓨터에 둘 수 있다. Day45 가 myApp 을 메뉴 쪽과 데이터 쪽으로 가른 것이 그것이고, Day01 에 정의로만 배운 클라이언트/서버가 여기서 처음 **문법**을 얻는다 → [[client-server-model]]

**입출력을 다시 배우지 않아도 된다.** 소켓이 돌려주는 것이 `InputStream`·`OutputStream` 이므로 파일에 쓰던 코드가 그대로 통한다 — 저장 대상이 파일에서 상대 프로그램으로 바뀌는데 `write()` 호출은 한 글자도 안 바뀐다. 대가는 아래 「경계와 오해」의 성질 차이이고, **호출이 같다는 것이 성질까지 같다는 뜻은 아니다** → [[io-stream]]

**두 값만 알면 남의 프로그램에 말을 걸 수 있다.** IP 와 포트라는 두 숫자가 「어느 기계의 어느 프로그램」을 가리키므로, 상대의 언어·OS 를 몰라도 통신이 성립한다. 그 대신 **무엇을 보낼지에 대한 약속을 사람이 정해야** 하고 그것이 프로토콜이다 → [[network-protocol]]

## 경계와 오해

- **`ServerSocket` ≠ `Socket`** — 이름이 비슷해서 「서버용 소켓」으로 읽히는데 **하는 일이 다르다.** `ServerSocket` 은 읽기·쓰기 메서드가 없다(`getInputStream()` 이 아예 없다) — 연결을 **듣고 받는** 것만 한다. 데이터가 흐르는 것은 `accept()` 가 돌려준 `Socket` 쪽이고, 상속 관계도 없다. Day45 의 필기가 「ServerSocker : 서버에서 받을 입구 생성」·「Socket : 입구에 대한 위치」로 둘을 갈라 적은 것이 정확하다.
- **대기열크기 ≠ 클라이언트 최대 접속수** — Day45 가 「대기열크기 : 클라이언트 최대 접속수」로 적은 것은 **틀렸다.** 두 번째 인자(backlog)는 **아직 `accept()` 되지 않고 줄 서 있는 연결의 최대 개수**다. `accept()` 로 받아 낸 연결은 그 줄에서 빠지므로, 대기열이 10 이어도 **동시에 붙어 있는 클라이언트는 10 을 넘을 수 있다.** 반대로 서버가 `accept()` 를 부르지 않고 딴 일을 하고 있으면 11번째 접속은 대기열이 차서 거절되는데, 이때 **접속 수가 아니라 「받아 내는 속도」가 부족한 것**이다. 대기열은 처리 능력을 늘려 주지 않고 **도착이 몰리는 순간의 편차만 흡수한다** → [[queue]] · [[little-law]]
- **소켓 ≠ 포트** — 포트는 **번호**(약속된 식별자)이고 소켓은 **객체**(연결의 끝)다. 그래서 **한 포트 위에 소켓이 여러 개** 생긴다 — 서버 포트 8888 하나에 클라이언트 셋이 붙으면 `accept()` 가 `Socket` 셋을 돌려준다. 이 셋을 구별하는 것은 서버 포트가 아니라 **상대의 IP 와 상대의 포트**다. 「포트 = 연결」로 읽으면 웹 서버가 80 하나로 수천 명을 받는 것이 설명되지 않는다 → [[port-number]]
- **`import java.net.ServerSocket;` 만 있어서 두 조각 다 컴파일되지 않는다 — 원본 코드의 실제 결함이다** — 서버 조각은 `Socket socket = serverSocket.accept();` 를 쓰는데 `Socket` 을 import 하지 않았고, 클라이언트 조각은 `Socket` 만 만드는데 **import 는 `ServerSocket`** 이다. 두 조각에 **똑같은 import 한 줄**이 적혀 있는 것이 원인을 말해 준다 — 앞 조각을 복사해 뒤를 만들었고 클래스 이름만 안 고쳤다. 명령 클래스를 복사해 늘리던 CRUD 실습에서 「골격을 복사하면 `import` 도 따라온다」로 이미 나온 자리이고, 그쪽은 컴파일이 막혀 최종 코드에서 고쳐졌다 — **여기는 고쳐지지 않은 채로 남은 형태다.** 필요한 것은 `import java.net.Socket;` 이고 둘 다 쓰는 조각은 두 줄(또는 `java.net.*`)이다 → [[package]] · [[crud]]
- **`(int) 포트번호` 는 캐스팅이 아니라 타입 표기로 쓴 것이다** — 자바에서 `(int) x` 는 「x 를 int 로 바꿔라」인데 여기서는 「이 자리에 int 를 넣어라」의 뜻으로 적혀 있다. 헷갈리는 이유는 **그대로도 컴파일될 수 있다는 것**이다 — 자바 식별자는 유니코드를 허용하므로 `int 포트번호 = 8888;` 이 합법이고, 그러면 `(int) 포트번호` 는 아무 일도 안 하는 캐스팅이 된다. **문법으로 읽어도 통하고 설명으로 읽어도 통해서** 나중에 이 줄을 코드로 복사하면 「선언한 적 없는 변수」에서 막힌다 → [[type-casting]] · [[parameter-and-argument]]
- **소켓 스트림은 파일 스트림과 호출만 같고 성질이 다르다** — 셋이 갈린다. (1) `read(byte[])` 가 **요청한 만큼 안 채운다** — 로컬 파일에서는 대개 다 채워지지만 네트워크는 패킷 단위로 도착하므로 짧게 읽히는 것이 정상이다. (2) **끝이 없다** — 파일은 다 읽으면 `-1` 인데 소켓은 상대가 아직 안 보낸 것과 끝난 것이 같은 「읽을 것 없음」으로 보이고, `read()` 는 `-1` 을 주지 않고 **막는다.** (3) **되돌아가지 못한다** — 파일은 다시 열어 처음부터 읽을 수 있지만 흘러간 바이트는 사라진다. 그래서 「어디까지가 한 메시지인가」를 보내는 쪽이 알려 줘야 하고, Day38 이 파일에 손으로 만든 길이 접두사 형식이 정확히 그 답이다 → [[length-prefix-framing]] · [[io-stream]] · [[binary-io]]
- **`accept()` 가 막힌다는 것은 그 스레드가 다른 일을 못 한다는 뜻이다** — Day45 의 서버는 `accept()` 한 번 → 통신 → 끝이므로 **클라이언트 하나를 받고 프로그램이 죽는다.** 「서버」가 되려면 `while(true)` 안에서 `accept()` 를 돌려야 하고, 그러면 **한 클라이언트와 대화하는 동안 다음 클라이언트를 받지 못한다**는 다음 문제가 바로 나온다(그 답이 접속마다 스레드를 주는 것이다). Day45 의 「대기열크기」가 왜 필요한 값인지도 여기서 드러난다 — 서버가 앞 손님을 상대하는 사이에 온 접속이 줄을 선다.
- **막히는 것은 생성이 아니라 `accept()` 다 — Day46 이 잘못 배운 자리다** — Day46 은 「ServerSocket을 생성하면 client Socket의 연결을 수락하기 전까지 블로킹이 된다」로 적었는데, **생성(과 바인딩)은 자리를 잡고 바로 돌아온다.** 멈추는 것은 그 다음 줄 `accept()` 다. 두 문장이 붙어 있어 결과가 같아 보이지만 갈리는 지점이 있다 — 포트가 이미 쓰이고 있으면 **생성에서 `BindException` 이 나고 `accept()` 까지 가지 못한다.** 「생성이 막힌다」로 배우면 그 예외를 「접속을 기다리다 실패한 것」으로 읽게 된다. 순서를 정확히 쓰면 **자리 잡기(즉시) → 듣기(즉시) → 수락(막힘)** 이다 → [[socket-binding]] · [[exception-handling]]
- **서버가 닫을 것은 하나가 아니라 둘이다** — Day46 은 「연결이 종료되면 serverSocket을 close 해야한다」로 `serverSocket.close()` 만 적는데, `accept()` 가 돌려준 `Socket` 도 각각 닫아야 한다. **`ServerSocket` 을 닫는 것은 새 접속을 안 받겠다는 뜻이고 이미 붙은 연결을 끊는 것이 아니다.** 연결마다 생기는 `Socket` 을 놓치면 접속이 늘 때마다 자원이 쌓이고, 서버는 오래 도는 프로그램이라 **그 누수가 실행 중에 드러난다** → [[try-with-resources]]
- **같은 문장이 클라이언트 절에도 복사돼 주체가 어긋나 있다** — Day46 의 TCP클라이언트 절도 「연결이 종료되면 serverSocket을 close 해야한다」로 적혀 있고 코드는 `socket.close()` 다. **클라이언트에는 `serverSocket` 이 존재하지 않는다** — 앞 절을 복사해 코드만 고친 흔적이고, 같은 노트에서 `import` 를 안 고쳐 남은 Day45 의 자리와 같은 종류다. 설명 문장은 컴파일되지 않으므로 **이 어긋남은 나중에 이 필기를 읽는 사람만 걸린다.**
- **`UnknownHostException` 과 `IOException` 은 나란한 둘이 아니다** — Day46 이 「두가지 예외」로 적어 형제처럼 보이는데 **`UnknownHostException` 이 `IOException` 의 하위 타입**이다(`ConnectException` 도 그렇다). 그래서 순서를 반대로 쓰면 컴파일이 막힌다 — `catch (IOException)` 을 먼저 두면 뒤의 `catch (UnknownHostException)` 은 「이미 잡힌 예외」가 된다. **넓은 것을 먼저 잡으면 좁은 것을 구별할 기회가 없어진다**는 것이 이 관계의 실질이고, 「두 가지」로 외우면 그 순서가 왜 강제되는지가 설명되지 않는다 → [[exception-handling]] · [[inheritance]]
- **소켓을 닫지 않으면 포트가 바로 풀리지 않는다** — Day45 의 코드에는 `close()` 가 없고 **Day46 이 같은 날 그 한 줄을 채운다**(「연결이 종료되면 serverSocket을 close 해야한다」). 프로그램이 죽으면 OS 가 정리하지만, `ServerSocket` 이 쓰던 포트는 TCP 규칙상 잠깐 잠겨 있어(`TIME_WAIT`) 곧바로 다시 띄우면 「Address already in use」가 난다. **파일을 안 닫으면 내 데이터가 안 나가는 것과 달리, 소켓을 안 닫으면 다음 실행이 막힌다** → [[try-with-resources]] · [[port-number]]
- **한 소켓에서 두 스트림이 나오지만 방향은 여전히 하나씩이다** — 소켓이 양방향으로 보이는 것은 `getInputStream()` 과 `getOutputStream()` 이 **각각 다른 통로**를 주기 때문이다. 「소켓 = 양방향 스트림」으로 읽으면 내가 쓴 것을 내가 읽을 수 있다고 오해하게 되는데, 내 출력 스트림에 쓴 것은 **상대의 입력 스트림**으로 간다. 그리고 양쪽이 서로 「먼저 읽기」를 하면 둘 다 영원히 멈춘다 — 누가 먼저 말하는지도 약속에 들어가야 한다 → [[io-stream]] · [[network-protocol]]
- **`OutStream` 은 `OutputStream` 의 오기다** — Day45 의 「OutStream -> 랜카드 -> InputStream」에서 왼쪽만 줄어 있다. 그리고 **가운데의 「랜카드」는 실제 경로의 요약**이다 — 사이에 OS 의 TCP 스택·라우터·상대 OS 가 있고, 그 층들이 있기 때문에 위의 「짧게 읽힌다」·「메시지 경계가 없다」가 생긴다. **한 화살표로 그리면 그 층들이 만드는 문제가 안 보인다** → [[network-protocol]]
- **`ServerSocker`·`Socker`(Day45)·`getRemotSocketAddress`(Day46) — 필기의 오타이고, 이런 오타는 컴파일러가 잡는다** — 클래스 이름과 메서드 이름은 컴파일 시점에 해석되므로 코드에 저렇게 쓰면 바로 막힌다. Day44 의 `DisplyElement` 는 **선언과 사용이 같은 오타라서** 컴파일을 통과하고 살아남았다 — **잡히는 오타와 살아남는 오타를 가르는 것은 철자가 아니라 그 이름을 내가 선언했는가**다. Day46 의 「accept()을 통해 Sokcet을 연결 할 수 있다」는 **설명 문장 쪽 오타라 아무도 잡지 않는다** — 셋을 한 줄에 놓으면 컴파일러가 지켜 주는 범위가 어디까지인지가 보인다 → [[observer-pattern]]

## 함께 보는 개념

- [[io-stream]] — 연결 뒤로 흐르는 것과 그것을 읽는 호출
- [[tcp]] — 이 두 클래스가 쓰는 전송 프로토콜
- [[socket-binding]] — 연결을 받을 자리를 정하는 단계
- [[domain-name-system]] — 이름으로 접속할 때 앞에 끼는 조회
- [[port-number]] — 소켓이 붙을 자리를 가리키는 숫자
- [[ip-address]] — 그 자리가 있는 기계를 가리키는 값
- [[network-protocol]] — 통로가 뚫린 뒤 무엇을 보낼지의 약속
- [[client-server-model]] — 이 두 클래스가 문법으로 실현하는 구조
- [[remote-procedure-call]] — 이 통로를 메서드 호출처럼 보이게 감싸는 층
- [[length-prefix-framing]] — 「어디까지가 한 메시지인가」의 답
- [[data-io-stream]] · [[decorator-pattern]] — 소켓 스트림에 씌우는 층
- [[try-with-resources]] — 소켓을 닫는 문법
- [[queue]] — 대기열크기가 가리키는 자료구조
- [[exception-handling]] — 생성자가 실패할 수 있다는 성질
- [[package]] — `java.net` 을 import 해야 하는 자리

## 출처

- [[2024-07-30-Day45]] — 「클라이언트 : Socket을 생성하여 통신 / 서버 : ServerSocket을 생성하고 Socket을 통해 통신」으로 양쪽이 쓰는 클래스가 다른 것을 배우고, `new ServerSocket(포트번호, 대기열크기)` → `serverSocket.accept()` → `new Socket("IP주소", 포트번호)` 세 줄을 코드로 적었다. 「실제 데이터 전송은 OutStream -> 랜카드 -> InputStream으로 이루어진다」로 Day12 의 「소켓입력스트림」이 실물이 되는 자리이기도 하다. 다만 **「대기열크기 : 클라이언트 최대 접속수」는 잘못 배운 것**이고(대기열은 아직 `accept()` 되지 않은 연결의 줄이다), 두 코드 조각 모두 `import java.net.ServerSocket;` 한 줄만 갖고 있어 **그대로는 컴파일되지 않는다**(클라이언트 조각은 `Socket` 을, 서버 조각은 `Socket` 을 import 하지 않았다). `getInputStream()`·`getOutputStream()`·`close()`·`accept()` 반복이 전부 빠져 있어 **연결을 만드는 것까지만 다룬 회차**이고, `(int) 포트번호` 는 캐스팅 문법을 타입 표기로 쓴 것이다. `ServerSocker`·`Socker` 오타와 `OutStream` 표기도 그대로 남아 있다
- [[2024-07-30-Day46]] — 같은 날 Day45 의 두 줄을 **단계로 펼친다.** 서버 쪽은 바인딩 세 형태 → `accept()` → `getRemotSocketAddress()` 로 상대 IP·포트 확인 → `close()` 이고, 클라이언트 쪽은 IP+포트 · 도메인 · `new Socket()` 후 `connect()` 세 형태와 「연결 요청 시 두가지 예외 UnknownHostException/ IOException」이다. Day45 에 없던 `close()` 가 여기서 채워지고, 「생성자가 곧 접속」이 규칙이 아니라 형태의 성질이었다는 것도 `connect()` 로 드러난다. 다만 **막히는 지점을 「ServerSocket을 생성하면 …블로킹이 된다」로 잘못 짚었고**(막히는 것은 `accept()` 다), 닫아야 할 것을 `serverSocket` 하나로만 적었으며(`accept()` 가 준 `Socket` 이 남는다), TCP클라이언트 절의 close 설명은 앞 절에서 복사돼 **클라이언트에 없는 `serverSocket` 을 가리킨다.** 「두가지 예외」도 실제로는 상하 관계다. 여전히 `getInputStream()`·`getOutputStream()` 과 실제 송수신은 나오지 않아 **두 회차 모두 통로를 만드는 것까지**다
