---
type: concept
id: socket-binding
title: 소켓 바인딩 (Socket Binding)
aliases:
  - 소켓 바인딩
  - bind
  - socket bind
  - InetSocketAddress
  - 소켓 주소
up:
  - 2024-07-30-Day46
tags:
  - 네트워크
  - 통신
  - java
  - 배포
---

# 소켓 바인딩 (Socket Binding)

**소켓에 「내 쪽 주소」를 붙이는 일.** 서버가 어느 IP·어느 포트로 들어온 접속을 받을지가 여기서 정해진다. Day46 이 「port번호를 직접 바인딩하여 생성」·「특정 IP에만 할당하는 방법」으로 세 가지 형태를 배운 자리다.

## 정의

소켓 하나에 주소가 **둘** 붙는다. 이 짝을 자바에서 `InetSocketAddress`(IP + 포트) 하나로 표현한다.

| 짝 | 무엇인가 | 누가 채우나 |
|---|---|---|
| 로컬 주소 | 내 쪽 IP·포트 | **바인딩** — 서버는 직접 정하고, 클라이언트는 OS 가 붙여 준다 |
| 원격 주소 | 상대 IP·포트 | 클라이언트는 `connect`, 서버는 `accept()` 가 채운다 |

Day46 은 서버 쪽 바인딩을 세 형태로 적는다 — **셋 다 같은 일을 하고 자유도만 다르다.**

```java
ServerSocket serverSocket = new ServerSocket("Port번호");          // 생성자가 바인딩까지 한다

ServerSocket serverSocket = new ServerSocket();                    // 아직 자리가 없는 소켓
serverSocket.bind( new InetSocketAddress("Port번호"));             // 포트만 정한다

ServerSocket serverSocket = new ServerSocket();
serverSocket.bind( new InetSocketAddress("IP주소","Port번호"));    // IP 까지 정한다
```

**첫 줄과 둘째 묶음의 차이는 「바인딩 전에 할 일이 있는가」다.** 기본 생성자로 만든 소켓은 아직 어느 포트도 잡고 있지 않아서, 옵션을 먼저 걸고(`setReuseAddress` 같은) 그 다음 바인딩할 수 있다. 첫 줄은 생성과 바인딩이 한 문장에 붙어 있어 그 틈이 없다.

세 번째가 **이 절에서 가장 실질적인 형태**다. IP 를 적으면 그 주소로 들어온 접속만 받고, 안 적으면 **기계에 있는 모든 주소로 들어온 접속을 받는다**(와일드카드 바인딩, `0.0.0.0`) → [[ip-address]]

클라이언트 쪽은 로컬 주소를 정하지 않고 **원격 주소만 지정한다.** 자기 포트는 OS 가 붙이므로 바인딩이 코드에 나타나지 않는다 → [[port-number]]

```java
Socket socket = new Socket();
socket.connect(new InetAddress.getByName("domainName"),50001);
```

연결이 생긴 뒤 **상대 쪽 짝을 읽는 것**이 `getRemoteSocketAddress()` 다. 돌려주는 타입이 상위 타입 `SocketAddress` 라서 IP·포트를 따로 꺼내려면 `InetSocketAddress` 로 내려 캐스팅한다 → [[type-casting]]

```java
InetSocketAddress isa = (InetSocketAddress) socket.getRemotSocketAddress();
String clientIp = isa.getHostString();
String portNo = isa.getPort();
```

## 왜 중요한가

**「서버는 떠 있고 포트도 맞는데 밖에서 접속이 안 된다」의 원인이 여기다.** 방화벽보다 먼저 볼 곳이 바인딩 주소다 — `127.0.0.1` 로 묶어 두면 같은 기계에서는 되고 다른 기계에서는 **연결 거부**가 난다. 코드도 포트도 안 고쳤는데 접속 가능성이 달라지는 유일한 자리이고, 컨테이너 안에서 서버를 띄울 때 가장 자주 밟는 함정이다(컨테이너 밖에서 보이려면 `0.0.0.0` 이어야 한다) → [[ip-address]]

**포트 충돌이 어느 시점에 드러날지가 바인딩 시점으로 정해진다.** 바인딩은 「이 번호는 내가 쓴다」를 OS 에 등록하는 일이라, 이미 쓰이는 번호면 그 줄에서 `BindException` 이 난다. 생성자로 바인딩하면 **객체를 만드는 문장이 실패**하고, `bind()` 를 따로 부르면 실패 지점이 뒤로 밀린다 — **어디서 터질지를 고르는 것**이 두 형태의 실질적 차이다 → [[exception-handling]] · [[port-number]]

**서버가 클라이언트를 식별할 수 있게 된다.** `getRemoteSocketAddress()` 로 상대 IP·포트를 읽을 수 있으므로 접속 로그를 남기거나 특정 주소를 막는 것이 가능해진다. Day45 가 「서버는 클라이언트의 포트를 알 필요가 없다」로 넘어갔던 값을 **꺼내 볼 수 있게 되는 자리**다.

## 경계와 오해

- **bind ≠ connect** — 둘 다 「주소를 정한다」로 읽히지만 **정하는 쪽이 반대**다. `bind` 는 **내 주소**를, `connect` 는 **상대 주소**를 정한다. 그래서 서버는 상대를 모른 채 바인딩만 하고 기다릴 수 있고, 클라이언트는 자기 주소를 모른 채 접속할 수 있다. 이름이 비슷한 `InetSocketAddress` 를 양쪽에 다 넘기기 때문에 코드만 보면 구별이 안 되고, **`bind` 인지 `connect` 인지가 유일한 구분**이다.
- **바인딩(소켓) ≠ 바인딩(그 밖의 모든 바인딩)** — 자바·프레임워크에서 「바인딩」은 값과 이름을 잇는 일을 통틀어 부른다(데이터 바인딩, 메서드 바인딩, 파라미터 바인딩). 여기서는 **소켓과 로컬 주소**를 잇는 것만 뜻한다. 낱말이 같아서 검색이 엉키는 자리이므로, 이 노트를 가리킬 때는 `[[socket-binding]]` 으로 건다 → [[polymorphism]]
- **`new ServerSocket("Port번호")` 는 컴파일되지 않는다 — 원본 코드의 실제 결함이다** — `ServerSocket` 에 문자열 하나를 받는 생성자가 없다(`()`·`(int)`·`(int,int)`·`(int,int,InetAddress)` 뿐이다). 같은 이유로 `new InetSocketAddress("Port번호")` 도 없고(`(int)`·`(String,int)`·`(InetAddress,int)` 뿐이다), `new InetSocketAddress("IP주소","Port번호")` 는 두 번째가 `int` 여야 한다. 그리고 클라이언트 쪽 `new Socket("IP","Port")` 도 두 번째 인자가 `int` 다. **네 줄이 같은 습관에서 나왔다** — 인자 자리에 값이 아니라 값의 **설명**을 적은 것이고, Day45 가 `(int) 포트번호` 로 하던 것의 다음 형태다. 다만 결과가 다르다: `(int) 포트번호` 는 변수를 선언하면 컴파일될 수 있었지만 **문자열 리터럴은 어떤 선언으로도 살릴 수 없다** — 타입이 애초에 다르다 → [[socket]] · [[data-type]]
- **세 형태를 한 블록에 적어서 그 자체로도 컴파일되지 않는다** — `ServerSocket serverSocket` 이 같은 블록에 세 번 선언돼 있다. 「이렇게도 되고 저렇게도 된다」를 나열한 것이지 이어지는 코드가 아니므로 **복사해 붙이면 「이미 정의된 변수」에서 먼저 막힌다** → [[variable-scope]]
- **`socket.connect(new InetAddress.getByName("domainName"),50001)` 은 세 군데가 틀렸다** — (1) `new` 뒤에 정적 메서드 호출을 붙일 수 없다(**문법 오류**라 이 파일 전체가 컴파일 대상에서 떨어진다). (2) `connect` 는 `SocketAddress` 를 받는데 `InetAddress` 는 그 타입이 아니다 — **바로 위 `bind` 에서 쓴 `InetSocketAddress` 를 `InetAddress` 로 잘못 옮겨 적은 것**이고, 두 클래스 이름이 다섯 글자만 다르다. (3) `connect` 의 두 번째 인자는 **포트가 아니라 타임아웃 밀리초**다. 그래서 「,50001」을 포트로 읽고 고치면 **포트 없이 50초를 기다리는 코드**가 된다 — 컴파일은 통과하고 동작만 이상해지는, 더 찾기 어려운 형태로 옮겨 간다. 맞는 형태는 `socket.connect(new InetSocketAddress("domainName", 50001))` 이다 → [[domain-name-system]] · [[parameter-and-argument]]
- **같은 절의 도메인 생성자 한 줄은 유일하게 맞는 코드다** — `new Socket(InetAddress.getByName("domainName"),50001)` 은 `Socket(InetAddress,int)` 생성자에 정확히 맞는다. **다섯 조각 중 하나만 컴파일된다**는 것이 이 절의 상태이고, 맞는 줄이 하필 가장 낯선 형태라는 것도 겹친다. 단 `getByName` 이 `UnknownHostException` 을 던지므로 `try` 없이는 여전히 막힌다 → [[exception-handling]]
- **`getRemotSocketAddress` 와 `String portNo = isa.getPort();`** — 앞은 `getRemoteSocketAddress` 의 오타이고 **메서드 이름 오타는 컴파일러가 잡는다.** 뒤는 `int` 를 `String` 변수에 대입한 것이라 역시 컴파일 에러다 — 「포트 번호」를 사람이 부르는 이름 그대로 문자열로 받은 것이고, 바로 위 `getHostString()` 이 실제로 문자열을 돌려주기 때문에 **두 줄이 나란히 있어서 더 자연스러워 보인다.** 숫자를 문자열로 받는 습관은 값에 `"8888 "` 같은 것이 섞여도 안 걸리게 만든다 → [[data-type]] · [[number-parsing]]
- **와일드카드 바인딩 ≠ 아무나 들어올 수 있음** — IP 를 안 적으면 「모든 주소로 받는다」이지만 **그것이 접근 허용을 뜻하지는 않는다.** 바깥에서 닿는지는 라우팅·NAT·방화벽이 따로 정한다. 반대로 특정 IP 로 묶는 것은 **접근 제어가 아니라 도달 경로 제한**이다 — 그 주소로 오는 요청은 누구든 받는다 → [[computer-network]]
- **바인딩은 연결을 받는 것이 아니다** — `bind` 는 자리를 잡는 것까지이고, 실제로 들어온 연결을 꺼내는 것은 `accept()` 다. Day46 이 「ServerSocket을 생성하면 client Socket의 연결을 수락하기 전까지 블로킹이 된다」로 적어 **생성·바인딩 단계에서 멈춘다고 배운 것은 틀렸다** — 생성과 바인딩은 바로 끝나고 막히는 것은 `accept()` 다 → [[socket]]
- **클라이언트도 바인딩할 수 있다** — 코드에 안 나타나는 것은 필요가 없기 때문이고 금지된 것이 아니다. `Socket` 도 `bind()` 를 갖고 있어 나가는 쪽 IP·포트를 고정할 수 있다(주소가 여러 개인 기계에서 어느 회선으로 나갈지 정할 때). **「서버만 바인딩한다」는 관례이지 규칙이 아니다** → [[port-number]]

## 함께 보는 개념

- [[socket]] — 바인딩된 자리에서 연결을 꺼내는 클래스
- [[ip-address]] — 어느 주소로 받을지가 이 값으로 정해진다
- [[port-number]] — 바인딩이 등록하는 번호
- [[tcp]] — 바인딩 → 대기 → 수락 순서를 정하는 프로토콜
- [[domain-name-system]] — 접속 쪽에서 이름을 주소로 바꾸는 단계
- [[client-server-model]] — 바인딩하는 쪽과 접속하는 쪽이 갈리는 구조
- [[type-casting]] — `SocketAddress` 를 내려 캐스팅하는 자리
- [[exception-handling]] — 자리 잡기 실패가 드러나는 방식

## 출처

- [[2024-07-30-Day46]] — 「TCP서버를 개발 하려면 ServerSocket과 Socket이 필요하다」 아래에 바인딩 세 형태(생성자 직접 바인딩 · 기본 생성 후 `bind` · 특정 IP 지정)를 코드로 적고, `getRemotSocketAddress()` 로 접속한 클라이언트의 IP·포트를 읽는 것과 `close()` 를 배웠다. 클라이언트 쪽은 IP+포트 · 도메인 · `connect` 세 형태를 적었다. 다만 **인자 자리에 값이 아니라 「Port번호」·「IP주소」 같은 설명 문자열을 적어 놓아 대부분이 컴파일되지 않고**(문자열 하나를 받는 `ServerSocket`·`InetSocketAddress` 생성자는 없다), `socket.connect(new InetAddress.getByName(...),50001)` 은 `new` + 정적 메서드라는 문법 오류에 타입·인자 의미까지 어긋나 있다. 「ServerSocket을 생성하면 …블로킹이 된다」도 막히는 지점을 `accept()` 가 아니라 생성으로 잘못 잡았고, 와일드카드 바인딩과 특정 IP 바인딩이 **무엇을 달라지게 하는지**는 다루지 않았다
