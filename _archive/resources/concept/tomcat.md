---
type: concept
id: tomcat
title: 톰캣 (Tomcat)
aliases:
  - 톰캣
  - tomcat
  - Apache Tomcat
  - Tomcat Embedded
  - 임베디드 톰캣
up:
  - 2024-08-26-Day63
  - 2024-08-27-Day64
tags:
  - web
  - java
  - 서버
  - JavaEE
---

# 톰캣 (Tomcat)

**서블릿 규격의 구현체 — 요청을 받는 부분과 내 클래스를 부르는 부분을 한 프로세스에 함께 가진 서버.** Day63 은 이것을 세 자리에서 부른다(WAS 의 대표 예 · 웹 서버 · Mini Web Server + Web Container + Java App 을 다 가진 것). **세 번째가 실제 모양**이고 앞의 둘은 그 모양 중 어느 부분을 보고 부른 이름이다 → [[servlet-container]] · [[web-server]] · [[web-application-server]]

## 정의

Day63 이 구조를 네 칸으로 적었다.

| 칸 | Day63 의 설명 | 무엇에 해당하나 |
|---|---|---|
| Web Browser | 「유저에게 UI를 출력하는 곳이다. 정적자원을 실행하는 주체이다」 | 톰캣 밖이다 — 클라이언트 |
| **Mini Web Server** | 「정적자원을 관리하는 곳이다」 | 요청을 받아 정적 파일에 답하는 부분 → [[web-server]] |
| **Web Container (Servlet Container)** | 「Servlet을 구축하는 환경이다. Application에 명령을 호출한다」 | 내 클래스를 부르는 부분 → [[servlet-container]] |
| Java App | 「Servlet을 수행하며 동적자원을 관리한다」 | **내가 배치한 서블릿들** → [[servlet]] |

**네 칸 중 톰캣인 것은 가운데 둘이다.** 그래서 「톰캣이 웹 서버인가 WAS 인가」라는 질문에는 **둘 다 안에 있다**가 답이고, 밖에서 어느 쪽으로 쓰는지가 구성에 따라 갈린다 → [[static-and-dynamic-content]]

Day63 이 톰캣의 웹 서버 부분에 조건을 붙였다 — 「tomcat mini web sever는 개발용으로는 적합하나, 성능이 제한된다」·「web server는 NginX와 같은 외부 서버를 혼용해서 사용한다」. **하나로 다 되는데 실무에서는 나눈다**는 것이고, 나누는 이유는 능력이 아니라 자원이다 → [[universal-scalability-law]]

### 실행 방법이 둘이다

| Day63 의 이름 | 무엇을 하나 | 서버 버전이 어디 적히나 |
|---|---|---|
| **간접실행** | 「Tomcat Embedded서버를 통해 서버를 구동하는 방식」 — 톰캣을 **라이브러리로** 내 코드가 켠다 | 내 빌드 파일 |
| **직접실행** | 「.war파일을 tomcat서버 파일에 옮기거나 Eclipse임시폴더로 구동하는 방식」 | **운영 환경에 깔린 것** |

**어느 쪽이든 서블릿을 쓰는 코드는 같고, 다른 것은 「누가 누구를 켜나」다.** 이 갈림이 그대로 뒤에 배울 스프링 부트의 실행 가능한 jar 와 전통적인 war 배포의 차이가 된다 → [[web-application-deployment]] · [[java-ee]]

## 사용 예시

Day63 의 간접실행 코드다. **톰캣을 켜는 일이 자바 코드 스무 줄로 적히는 것**이 이 회차에서 실물로 남은 것이고, 순서와 경로에 뜻이 있는 줄이 넷 있다.

```java
// 톰캣 서버를 구동시키는 객체 준비
Tomcat tomcat = new Tomcat();

// 서버의 포트 번호 설정
tomcat.setPort(8888);

// 톰캣 서버를 실행하는 동안 사용할 임시 폴더 지정
tomcat.setBaseDir("temp");

// 톰캣 서버의 연결 정보를 설정
Connector connector = tomcat.getConnector();
connector.setURIEncoding("UTF-8");

// 톰캣 서버에 배포할 웹 애플리케이션의 환경 정보 준비
StandardContext ctx = (StandardContext) tomcat.addWebapp("/",
    new File("src/main/webapp").getAbsolutePath()
);
ctx.setReloadable(true);

WebResourceRoot resources = new StandardRoot(ctx);
resources.addPreResources(new DirResourceSet(resources,
    "/WEB-INF/classes",                        // 서블릿 클래스 파일의 위치 정보
    new File("bin/main").getAbsolutePath(),    // 실제 경로
    "/"
));
ctx.setResources(resources);

// 톰캣 서버 구동
tomcat.start();
tomcat.getServer().await();
```

| 줄 | 무엇을 정하나 |
|---|---|
| `setPort(8888)` → `getConnector()` | **이 순서여야 한다** — 아래 「경계와 오해」 |
| `addWebapp("/", …)` | 첫 인수가 **컨텍스트 경로**(URL 의 앞부분), 둘째가 정적 자원이 있는 실제 폴더 → [[web-application-deployment]] |
| `DirResourceSet(…, "/WEB-INF/classes", "bin/main", "/")` | **내 클래스가 어디 있는지** — 여기가 틀리면 서블릿이 하나도 등록되지 않는다 → [[classpath]] |
| `await()` | 서버가 멈출 때까지 `main` 이 끝나지 않는다 → [[main-method]] |

**`main` 이 톰캣을 켜고 기다리는 형태**라 [[socket]] 을 직접 열던 Day61 의 서버와 겉모양이 같다 — `while (true) accept()` 자리에 `await()` 가 있고, **그 루프를 라이브러리가 갖고 있다**는 것만 다르다 → [[client-server-model]]

### 하루 뒤 Day64 — 같은 코드에서 경로 한 줄이 바뀐다

Day64 가 같은 부팅 코드를 다시 싣는데 **딱 한 줄이 다르다.**

| 회차 | `/WEB-INF/classes` 에 붙이는 실제 폴더 | 어느 빌드의 산출물인가 |
|---|---|---|
| Day63 (2024-08-26) | `new File("bin/main")` | **Eclipse · Buildship** |
| **Day64 (2024-08-27)** | `new File("build/classes/java/main")` | **Gradle** |

```java
resources.addPreResources(new DirResourceSet(
    resources, // 루트 웹 애플리케이션 정보
    "/WEB-INF/classes", // 서블릿 클래스 파일의 위치 정보
    new File("build/classes/java/main").getAbsolutePath(), // 서블릿 클래스 파일이 있는 실제 경로
    "/" // 웹 애플리케이션 내부 경로
));
```

**하루 만에 이 줄이 바뀐 것이 Day63 의 부팅이 실제로 안 됐다는 증거로 읽힌다** — 전날 코드로는 서블릿이 하나도 등록되지 않아 화면이 없었고(아래 「경계와 오해」), 이 회차에 처음으로 서블릿을 만들어 열어 보면서 경로를 실행 환경에 맞췄다. 다만 **고쳐진 것은 이 사람의 이 환경뿐이다** — 하드코딩 자체는 그대로이고 어긋나는 방향만 뒤집혔다. 나머지 줄(포트·`temp`·`src/main/webapp`·`setReloadable(true)`·`await()`)은 두 회차가 같다 → [[gradle]] · [[build]] · [[classpath]]

## 왜 중요한가

**서버를 만드는 일이 서버를 고르는 일로 바뀐다.** Day45~62 에서 손으로 세운 것(접속 루프·접속마다 쓰레드·대화 규칙·종료 신호)이 전부 이 제품 안에 있다. 남는 일은 **어디에 무엇을 놓을지 정하는 것**이고, 위 코드의 절반이 정확히 그 일(포트·임시 폴더·문서 루트·클래스 위치)이다 → [[servlet-container]] · [[thread]]

**그리고 「내 프로그램이 곧 프로세스」였던 것이 끝난다.** 직접실행에서는 내 코드에 `main` 이 없고 톰캣의 프로세스 안에 얹힌다. 그러면 여러 앱이 한 프로세스를 나눠 쓰므로 **메모리·쓰레드·클래스 로더가 공유 자원**이 된다 → [[process]] · [[class-loading]]

**대신 무엇이 동작을 정하는지가 코드 밖으로 나간다.** 간접실행에서는 톰캣 버전이 내 빌드 파일에 적히지만, 직접실행에서는 **운영 환경에 깔린 버전**이 정한다 — 같은 war 가 다른 서버에서 다르게 돌 수 있고, 그것이 [[java-ee]] 의 버전 대응표가 실제로 물리는 자리다.

## 경계와 오해

- **클래스 폴더가 하드코딩되어 있어 「어느 빌드 도구로 실행하나」가 코드에 박힌다 — Day63 은 Gradle 에서 전 요청 404, Day64 는 Eclipse 에서 전 요청 404** — 서블릿은 `/WEB-INF/classes` 에 있는 클래스를 컨테이너가 훑어서 등록하는데, 이 코드는 그 자리에 붙일 실제 폴더를 상대 경로 문자열로 적는다. 그 문자열이 **하루 만에 뒤집혔다.**

  | | `/WEB-INF/classes` 에 붙인 것 | 클래스가 실제로 생기는 곳 | 결과 |
  |---|---|---|---|
  | Day63 (2024-08-26) | `bin/main` | Gradle 로 빌드하면 `build/classes/java/main` | **Gradle 실행에서 404** |
  | Day64 (2024-08-27) | `build/classes/java/main` | Eclipse·Buildship 로 빌드하면 `bin/main` | **Eclipse 실행에서 404** |

  **즉 고쳐진 것이 아니라 어긋나는 방향이 바뀐 것이다.** 어느 쪽이든 증상은 같다 — 컨테이너가 보는 폴더가 **빈 폴더이거나 아예 없어서** 등록할 서블릿이 없고, `tomcat.start()` 는 **성공하고**, 8888 포트도 **열리고**, 예외도 로그도 나지 않고, 모든 요청이 **404** 다. 「서버는 떴는데 화면이 없다」의 원인이 코드 한 줄의 상대 경로이고, **실패가 예외가 아니라 「없음」으로 나타나므로** 찾을 단서가 없다.

  Day64 의 값은 **그 자리가 실행 환경에 물려 있다는 것을 코드가 드러냈다**는 데 있다 — 하루 만에 이 줄만 바뀐 것이 전날 부팅이 실제로 되지 않았다는 흔적이다. 근본 답은 문자열을 고치는 것이 아니라 **빌드가 알려 주게 하거나 두 경로를 다 등록하는 것**이고, Day63 이 갈라 둔 「간접실행/직접실행」에 **「어느 IDE·빌드로 실행하나」라는 축이 하나 더** 붙는다. `new File("src/main/webapp")` 도 같은 부류이며 이쪽은 두 회차가 같다 — 빌드 산출물이 아니라 **소스 트리를 그대로 문서 루트로** 쓰므로 개발 중에는 편하지만 배포물과 다른 곳을 본다 → [[classpath]] · [[gradle]] · [[build]] · [[filesystem-path]] · [[web-application-deployment]]
- **`setPort` 와 `getConnector` 의 순서가 뜻을 갖는다 — 바꿔 쓰면 8888 이 조용히 무시된다** — `getConnector()` 는 「가져오는」 이름인데 **없으면 만든다.** 그 만들어지는 시점에 포트가 정해지므로, `getConnector()` 를 먼저 부르면 기본값 8080 으로 커넥터가 생기고 뒤에 온 `setPort(8888)` 는 **이미 만들어진 것에 반영되지 않는다.** 오류도 경고도 없고 서버는 8080 에서 정상으로 뜬다. 위 코드의 순서는 맞는데 **왜 그 순서인지가 주석에 없어서**, 줄을 옮기면 깨진다는 것을 아무도 모른다 → [[method]]
- **톰캣 ≠ 웹 서버, 톰캣 ≠ WAS — 같은 노트가 세 자리에서 부른다** — 비교 표의 「대표적인 예」에서는 WAS, 구조 절에서는 「`Tomcat` 같은 웹 서버가 이 역할을 수행한 후, 요청을 WAS로 넘겨 처리한다」로 웹 서버, Tomcat 절에서는 둘을 다 가진 것. **②가 틀렸다** — 톰캣은 WAS 로 넘기는 쪽이 아니라 넘겨받는 쪽이다. 두 이름이 다 붙는 이유는 정말로 두 부분을 갖고 있어서이고, 그래서 「무엇을 포함하나」와 「어느 자리에 서나」를 갈라야 그림의 화살표가 방향을 갖는다 → [[web-application-server]] · [[web-server]]
- **톰캣 ≠ Java EE 전체** — Day63 의 버전 표에서 톰캣 열이 채워지는 것은 Servlet·JSP·EL 이고 **EJB 는 비어 있다.** 그래서 WebLogic·WebSphere 와 같은 줄에 놓이지만 크기가 다르고, 「WAS 를 톰캣으로 배웠다」가 「Java EE 를 배웠다」가 아니다 → [[java-ee]]
- **`setReloadable(true)` 는 개발용이고, 다시 뜰 때 메모리에 있던 것이 다 사라진다** — 클래스 파일이 바뀌면 컨텍스트를 다시 시작하므로 편한데, 그때 **세션·쓰레드에 매달린 값·캐시가 함께 없어진다.** 사흘 전 Day62 가 쓰레드마다 매달아 둔 `SqlSession` 이 그런 값이고, 반납되지 않은 연결이 있다면 그것도 이 시점에 정리되지 않는다. **하루 뒤 Day64 에서 이것이 실제 비용이 된다** — 그 회차의 리스너가 `contextInitialized` 에서 `SqlSessionFactory` 와 커넥션 풀을 만들면서 `contextDestroyed` 를 비워 두었으므로, **저장할 때마다 옛 풀이 회수되지 않은 채 새 풀이 하나 더 생긴다** → [[servlet-listener]] · [[thread-local]] · [[connection-lifetime-mismatch]]
- **`setBaseDir("temp")` 는 상대 경로다** — 실행을 어느 디렉토리에서 시작했는지에 따라 다른 폴더가 되고, 그 폴더에 컨텍스트 압축 해제본과 컴파일 결과가 쌓인다. 정리하는 코드가 없으므로 **옛 산출물이 남아 있는 상태로 다시 뜰 수 있다** → [[filesystem-path]]
- **종료 코드가 없다** — `await()` 뒤에 `System.out.println("서버 종료!")` 만 있고 `tomcat.stop()`·`destroy()` 도, 종료 신호를 받아 정리하는 장치도 없다. 프로세스를 강제로 끊으면 세션과 임시 폴더가 그대로 남는다. [[thread]] 노트가 Day61 을 두고 「참조가 없어 `join()`·`interrupt()` 를 부를 상대가 없다 — 특정 접속을 끊을 수도, 종료를 기다릴 수도 없다」고 적은 문제가 **여기서는 라이브러리 안으로 들어갔을 뿐 답해지지 않았다** → [[thread-join]] · [[exception-handling]]
- **`main` 이 `throws Exception` 이다** — 기동 실패(포트 사용 중·경로 없음)가 스택트레이스로 끝나고 「무엇을 확인하라」는 메시지가 없다. 서버는 사람이 아니라 스크립트가 켜는 것이므로 **종료 코드와 메시지가 그 자체로 인터페이스**인데 그 자리가 비어 있다 → [[exception-handling]]
- **「Mini Web Server 는 성능이 제한된다」의 내용이 필기에 없다** — 실제로 갈리는 것은 정적 파일을 많이 보낼 때 쓰레드를 잡는다는 것, TLS 를 끝내는 일과 느린 연결을 붙들고 있는 일이 앞단의 몫이라는 것이다. 「성능」 한 낱말로 두면 **왜 앞에 하나를 더 두는지**가 취향처럼 보인다 → [[web-server]] · [[little-law]]

## 함께 보는 개념

- [[servlet-container]] — 톰캣의 가운데 부분
- [[servlet-listener]] — 톰캣이 기동할 때 내 코드를 처음 부르는 자리
- [[web-component]] — 톰캣이 찾아서 등록하는 부품들
- [[web-server]] — 톰캣이 안에 갖고 있고 실무에서는 앞에 따로 두는 것
- [[web-application-server]] — 톰캣이 대표 예로 불리는 자리
- [[servlet]] — 톰캣이 찾아서 부르는 내 클래스
- [[java-ee]] — 톰캣이 구현하는 범위를 정하는 명세
- [[web-application-deployment]] — 간접실행·직접실행이 갈리는 자리
- [[classpath]] · [[class-loading]] · [[build]] · [[gradle]] — 클래스 위치가 어긋나는 자리
- [[main-method]] · [[process]] — 실행의 단위가 바뀌는 자리
- [[socket]] · [[client-server-model]] — 손으로 만들던 서버와 같은 모양인 부분
- [[thread]] · [[thread-local]] — 톰캣 위에서 다시 문제가 되는 것
- [[universal-scalability-law]] · [[little-law]] — 앞에 웹 서버를 두는 이유를 세는 축
- [[filesystem-path]] — 상대 경로가 동작을 정하는 자리
- [[character-encoding]] — `setURIEncoding` 이 정하는 것

## 출처

- [[2024-08-26-Day63]] — 「Tomcat 설치 및 구동」·「Tomcat 서버 구조」·「Tomcat 서버 실행」·「웹애플리케이션 + 톰캣서버 배치」 절이 이 개념이다. 구조를 「Web Brower / Mini Web Server / Web Container(Servlet Container) / Java App」 네 칸으로 적어 **웹 서버 부분과 컨테이너 부분이 한 제품 안에 있다는 것**을 보여 주고, 「tomcat mini web sever는 개발용으로는 적합하나, 성능이 제한된다」·「web server는 NginX와 같은 외부 서버를 혼용해서 사용한다」로 실무 구성을 한 줄씩 적었다. 실행 방법을 간접실행(Tomcat Embedded)과 직접실행(war 또는 Eclipse 임시 폴더)으로 갈랐고, **간접실행 코드 스무 줄이 이 회차에서 남은 유일한 코드**다 — `new Tomcat()` → `setPort(8888)` → `setBaseDir("temp")` → `getConnector().setURIEncoding("UTF-8")` → `addWebapp("/", src/main/webapp)` → `setReloadable(true)` → `DirResourceSet` 로 `/WEB-INF/classes` 를 `bin/main` 에 붙이기 → `start()` → `getServer().await()`. 다만 그 코드에 **경로가 IDE 산출물(`bin/main`)로 하드코딩되어 있어** Gradle 로 실행하면 서블릿이 하나도 등록되지 않은 서버가 오류 없이 뜨고 모든 요청이 404 가 되며, `setPort` 를 `getConnector` 앞에 두어야 한다는 것·종료 처리가 없다는 것·`setReloadable(true)` 가 재시작마다 메모리 상태를 지운다는 것은 필기에 없다. 「Java App : Servlet을 수행하며」라는 칸은 같은 노트의 서블릿 절(「서블릿은 서블릿 컨테이너 안에서 실행됩니다」)과 층수가 어긋나고, 구조 절에서는 톰캣을 「WAS로 넘기는 웹 서버」로 적어 대표 예 표와 반대 자리에 놓았다. 버전 표의 톰캣 열은 Java EE 8 · 톰캣 8.5/9.x 에서 끝나 **`jakarta.*` 로 바뀌는 톰캣 10 경계 앞에서 멈춘다**(→ [[java-ee]])
- [[2024-08-27-Day64]] — 하루 뒤. 같은 간접실행 코드를 「서블릿 컨테이너의 동작 원리」 절에 다시 싣는데 **`/WEB-INF/classes` 에 붙이는 실제 경로가 `bin/main` 에서 `build/classes/java/main` 으로 바뀌었다** — 하드코딩은 그대로이고 어긋나는 방향만 Gradle 쪽에서 Eclipse 쪽으로 뒤집힌 것이며, 하루 만에 이 줄만 바뀐 것이 전날 코드로는 서블릿이 등록되지 않아 화면이 없었다는 흔적이다(위 「경계와 오해」 첫 항목). 주석이 더 자세해졌고(「컨텍스트 경로(웹 애플리케이션 경로)」·「정적 웹 자원의 경로」·「동적 웹 자원의 경로」) 나머지 줄은 두 회차가 같다. 그리고 이 회차는 **톰캣이 기동한 뒤 내 코드가 처음 불리는 지점을 실제로 쓴다** — 리스너 구동원리 절이 `Tomcat.start()` → 컨테이너 실행 → 리스너 탐색 → `contextInitialized` 순서를 적고, 그 메서드에서 MyBatis 팩토리와 DAO 를 만들어 [[servlet-context]] 에 올린다. 다만 짝이 되는 `contextDestroyed` 를 비워 두어 **`setReloadable(true)` 로 컨텍스트가 다시 뜰 때마다 커넥션 풀이 정리되지 않고 겹친다**(→ [[servlet-listener]]). 종료 처리·`setPort` 순서·`setBaseDir` 상대 경로에 대해서는 이 회차에도 아무 언급이 없다
