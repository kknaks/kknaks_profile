# 이관 01 — `concept` 366 → `areas/concept/<영역>/`

`_archive/resources/concept/` 의 366 건(`README.md` 제외)을 아홉 영역에 배정한다.
**분류 완료 — 갈림 0.** `결정` 칸이 비어 있으면 `추천` 이 그대로 확정된 것이고, 굵게 적힌 것은 사람이 정한 것이다.

- 판정 기준: `para/areas/area.md`
- 파일 stem 을 바꾸지 않는다 — 본문 `[[wikilink]]` 11,326 개와 `up:` 149 개가 전부 stem 기반이다
- `git mv` 를 쓰지 않는다. `_archive/` 는 그대로 두고 복사한다
- `up:` 은 한 줄도 건드리지 않는다. 149 개 stem 이 전부 `resources/source/` 를 가리키고, 그 층은 이관 02 에서 다룬다

## 최종 분포

| 영역 | 건수 |
|---|---|
| `cs` | 169 |
| `back` | 137 |
| `db` | 28 |
| `infra` | 24 |
| `ai` | 4 |
| `front` | 2 |
| `qa` | 1 |
| `pm` | 1 |
| `design` | 0 |
| **합** | **366** |

`design` 이 0 이다. 「디자인 패턴」이 전부 `cs` 로 갔고(GoF 는 소프트웨어 설계), UI/UX 개념은 아직 쌓인 것이 없다.

## 정한 선 — 네 개

워커 10 개가 366 건을 훑어 갈림 63 건을 냈고, 파일 하나씩이 아니라 **선을 긋고 묶음으로** 정했다.

### 1. `cs` ↔ `back` (38 건)

> **개념이 언어를 바꿔도 남으면 `cs`. 필기가 자바로 쓰인 것은 근거가 아니다.**

63 중 38 이 이 경계였고 전부 같은 모양이었다 — 개념 자체는 언어 무관인데 필기가 자바 문법으로
쓰여 있다. **33 건이 `cs` 로 갔다.**

예외 5 건만 `back` 에 남겼다. **예제가 자바인 게 아니라 개념이 자바 밖에 없는 것들**이다.

| 파일 | 왜 |
|---|---|
| `functional-interface` | 자바가 람다를 기존 타입 체계에 얹으려고 만든 우회. 파이썬·JS 엔 없다 |
| `object-class` | `java.lang.Object` 와 그 메서드 여섯. 클래스 이름이 곧 대상 |
| `ognl` | 특정 표현 언어. 개념이 아니라 제품명 |
| `package` | 네임스페이스라는 일반 개념은 따로 있다. 이건 자바 패키지 문법 |
| `raw-type` | 자바 제네릭이 소거 방식이라 생긴 하위 호환 상태 |

### 2. `infra` = 서버 · 빌드 · 배포 · 형상관리

`build` · `gradle` · `npm` · `web-application-deployment` · `cold-start` · `message-broker` ·
`git` · `staging-area` · `remote-repository` 가 여기로 왔다.

**⚠ `para/areas/area.md` 를 고쳐야 한다.** 지금 정의가 「배포·운영 — 컨테이너·오케스트레이션·
CI/CD·모니터링」이라 **형상관리와 빌드가 안 들어간다.** 정본에 안 적으면 다음에 같은 판단을 또 한다.

`back` 에 남긴 것 둘:

| 파일 | 왜 |
|---|---|
| `distributed-session` | 서버 다중화는 계기일 뿐 개념은 「세션을 어디에 담나」. `attribute-scope` 와 한 갈래 |
| `terminal-state-ttl` | 서버·빌드·배포 어디도 아니다. 큐 키에 TTL 을 언제 거느냐는 앱이 정하는 규칙 |

### 3. `db` = 순수 SQL · DB 엔진만

`back` ↔ `db` 5 건이 **전부 `back`** 으로 갔다. 넷은 본문이 스스로 답을 적어 뒀다 — `[[jdbc]]` 로 끝난다.

| 파일 | 본문이 말하는 것 |
|---|---|
| `odbc` | 「여기서부터는 프로그램이 DB 에 접속하는 이야기」 |
| `prepared-statement` | `setXXX(위치, 값)` 으로 값을 채운다 → `[[jdbc]]` |
| `sql-injection` | 「원인은 문장을 문자열 이어 붙이기로 만든 것」 → `[[jdbc]]` |
| `optimistic-lock` | 「**잠그지 않고** 읽되」 — DB 락이 아니라 `@Version` 을 앱이 확인 |
| `pagination` | 「몇 번째부터 몇 개」를 계산하는 것은 앱 |

`area.md` 는 「락 → `db`」라고 적어 뒀지만 **낙관적 락은 DB 락을 안 쓴다.** 이미 `db` 에 있는
`database-lock`(「동시에 만지는 트랜잭션의 순서를 강제하는 장치」)과 다른 물건이다.

### 4. 단발 5 건

| 파일 | 결정 | 왜 |
|---|---|---|
| `gamification` | `pm` | `design` 은 화면 얘기다. 이건 「무엇으로 다시 열게 만드나」 |
| `javascript-type` | `cs` | 동적 타이핑은 언어 무관. 선 1 을 그대로 적용 |
| `mrtr` | `ai` | 출처와 유일한 사례가 MCP 스펙. AI 맥락 밖에 쓰인 적이 없다 |
| `output-escaping` | `back` | 치환이 일어나는 자리가 서버 (JSP `c:out`) |
| `surrogate-key` | `db` | `primary-key` · `unique-key` · `foreign-key` 와 키 계열로 모인다 |

## 남은 일

- [ ] `para/areas/area.md` 의 `infra` 정의를 넓힌다 (형상관리·빌드)
- [ ] 366 건을 `para/areas/concept/<영역>/` 로 복사한다
- [ ] 옵시디언에서 `_archive/` 를 제외한다 — 복사하면 같은 vault 안에 stem 이 둘이 된다.
      `.obsidian/` 은 gitignore 라 머신마다 따로 해야 한다

---

## 표

| 구분 | 파일명 | 내용 | 추천 | 결정 |
|---|---|---|---|---|
| 1 | `abstract-class.md` | 공통 멤버만 모아 두고 인스턴스는 못 만들게 막아 자식이 완성하게 강제하는 상속 골격 | cs |  |
| 2 | `access-modifier.md` | 클래스·멤버를 어디서 쓸 수 있는지 네 등급으로 나눠 캡슐화 경계를 긋는 키워드 | cs / back? | **cs** |
| 3 | `aggregate-function.md` | 여러 행을 값 하나로 접는 SQL 함수. NULL 은 세지 않는다 | db |  |
| 4 | `ai-agent.md` | 모델이 문장만 내놓는 데서 그치지 않고 툴을 호출해 실제 동작을 일으키게 만드는 구조 | ai |  |
| 5 | `annotation-retention.md` | 직접 만든 애노테이션이 소스·클래스파일·실행중 메모리 중 어디까지 살아남을지 정하는 선언 | back |  |
| 6 | `annotation-target.md` | 직접 만든 애노테이션을 붙일 수 있는 선언 종류를 제한해 컴파일 단계에서 걸러내는 장치 | back |  |
| 7 | `annotation.md` | 선언에 붙이는 표시인데 주석과 달리 컴파일러와 JVM 이 읽어 동작에 반영한다 | back |  |
| 8 | `anonymous-class.md` | 클래스 선언과 인스턴스 생성을 한 식으로 합쳐 그 자리에서 한 번만 쓰는 구현을 만드는 문법 | cs / back? | **cs** |
| 9 | `ansi-escape-code.md` | 터미널이 글자로 찍지 않고 명령으로 해석하는 제어 문자열. 색과 스타일을 바꾼다 | cs |  |
| 10 | `aop.md` | 여기저기 흩어진 공통 처리를 한 곳에 모으고 적용 지점을 조건으로 적어 호출부 앞뒤에 끼워 넣는 것 | back |  |
| 11 | `apache-poi.md` | 엑셀 파일을 바이트가 아니라 워크북·시트·행·셀 객체로 다루게 해 주는 자바 라이브러리 | back |  |
| 12 | `api-documentation.md` | 코드에 붙인 애노테이션에서 API 명세와 시험 화면을 자동으로 뽑아내는 방식 | back |  |
| 13 | `api-response-envelope.md` | 모든 API 응답을 결과코드·메시지·데이터라는 같은 껍데기로 감싸 모양을 고정하는 설계 | back |  |
| 14 | `application-event.md` | 무슨 일이 일어났다만 알리고 처리는 듣는 쪽이 정하게 해 호출부가 상대를 모르게 만드는 장치 | back |  |
| 15 | `application-layer.md` | HTTP·SMTP 처럼 사람이 쓰는 서비스가 사는 네트워크 최상위 층과 프로토콜별 포트 | cs |  |
| 16 | `array-copy.md` | 크기를 못 바꾸는 배열에서 늘리기·자르기·사본 만들기를 새 배열 반환 하나로 처리하는 방법 | cs / back? | **cs** |
| 17 | `array-element-removal.md` | 고정 크기 배열의 중간 요소를 뒤를 당기고 개수를 줄이고 끝칸을 비우는 세 단계로 지우는 것 | cs |  |
| 18 | `array.md` | 같은 타입 메모리를 연속으로 확보해 이름 하나와 인덱스로 다루는 첫 묶음 도구 | cs |  |
| 19 | `async-io.md` | 워커가 응답을 기다리는 동안에도 붙들려 있는지 여부. 붙들리면 워커 수가 동시 처리 상한이 된다 | cs / back? | **cs** |
| 20 | `attribute-scope.md` | 웹에서 값을 담는 네 보관소. 어디에 담느냐가 그 값의 수명과 공유 범위를 정한다 | back |  |
| 21 | `autoboxing.md` | 기본 타입과 래퍼 타입 사이 변환 호출을 컴파일러가 코드에 몰래 끼워 넣어 주는 것 | back |  |
| 22 | `autowired.md` | 넣을 빈을 설정에 적지 않고 표시만 하면 컨테이너가 타입을 보고 찾아 넣는 주입 방식 | back |  |
| 23 | `bean-definition.md` | 컨테이너에 어떤 클래스로 무슨 이름의 객체를 만들고 무엇을 넣을지 적는 선언 | back |  |
| 24 | `bean-post-processor.md` | 컨테이너가 빈을 만든 직후 끼어들어 손대는 확장점. 스프링 애노테이션이 도는 실제 이유 | back |  |
| 25 | `bean-scope.md` | 컨테이너가 빈을 몇 개 만들고 언제까지 살릴지 정하는 설정. 기본은 공유되는 하나 | back |  |
| 26 | `binary-io.md` | 값을 사람이 읽는 문자로 바꾸지 않고 타입별 비트 표현 그대로 주고받는 입출력 | back |  |
| 27 | `bit-shift.md` | 비트를 좌우로 옮기는 연산자. 한 칸이 2를 곱하거나 나누는 것과 같다 | cs |  |
| 28 | `bitwise-operator.md` | 두 값을 비트 자리마다 독립적으로 맞대어 AND·OR·XOR·NOT 하는 연산자 | cs |  |
| 29 | `breadth-first-search.md` | 가까운 것부터 한 겹씩 넓혀 가는 큐 기반 탐색. 처음 닿은 순간이 최단 거리다 | cs |  |
| 30 | `break-continue.md` | 반복을 끝내거나 이번 회차만 건너뛰는 두 문장과 그 대상을 바깥 반복문으로 옮기는 라벨 | cs |  |
| 31 | `brute-force.md` | 가능한 경우를 빠짐없이 다 해 보는 것. 상한이 작으면 이걸로 끝나는 기본값 | cs |  |
| 32 | `buffered-stream.md` | 1바이트씩 부르는 코드는 그대로 두고 실제 통로에는 덩어리로 내보내 시스템콜 횟수를 줄이는 껍데기 | back |  |
| 33 | `build.md` | 소스에서 배포 산출물이 나오기까지의 컴파일·의존성·테스트 단계 전체와 그걸 명령으로 묶는 도구 | back / infra? | **infra** |
| 34 | `byte-array-stream.md` | 통로의 끝이 파일이나 네트워크가 아니라 메모리 바이트 배열인 스트림 | back |  |
| 35 | `bytecode.md` | 기계어까지 내리지 않고 중간 형태로만 컴파일해 실행은 환경별 가상머신에 맡기는 하이브리드 실행 모델 | back |  |
| 36 | `caching.md` | 자주 읽는 데이터를 고속 저장소에 복사해 두고 원본 대신 거기서 꺼내 응답을 앞당기는 것 | cs / back? | **cs** |
| 37 | `call-by-value.md` | 호출 시 인수의 값이 복사되어 넘어가는 방식. 레퍼런스면 주소가 복사된다 | cs |  |
| 38 | `cgi.md` | 웹 서버가 외부 프로그램을 실행해 그 출력을 응답으로 돌려주는 규약 | back |  |
| 39 | `change-data-capture.md` | DB가 남기는 binlog를 읽어 변경을 스트림으로 따라가는 동기화 방식 | db |  |
| 40 | `character-encoding.md` | 글자를 바이트로 바꾸는 규칙. 쓴 쪽과 읽는 쪽이 같아야 안 깨진다 | cs |  |
| 41 | `character-stream.md` | 바이트 대신 char가 흐르는 Java Reader/Writer 계열과 인코딩 변환층 | back |  |
| 42 | `ci-cd.md` | 푸시 한 번으로 빌드부터 배포까지 잇는 GitHub Actions 자동화 절차 | infra |  |
| 43 | `class-file-format.md` | JVM이 읽는 .class 파일의 바이트 배치 규격과 매직넘버 순서 | back |  |
| 44 | `class-loading.md` | .class를 읽어 JVM 안에 클래스를 세우고 static을 초기화하는 시점 | back |  |
| 45 | `class-metadata.md` | 실행 중에 인스턴스의 타입 정보를 객체로 받아 다루는 리플렉션 진입점 | back |  |
| 46 | `class.md` | 메서드를 묶고 새 데이터 타입을 정의하는 객체지향의 기본 단위 | cs |  |
| 47 | `classpath.md` | JVM에 .class 파일이 어디 있는지 알려주는 탐색 경로 옵션 | back |  |
| 48 | `cli.md` | 글자로 한 줄씩 명령을 입력해 컴퓨터를 부리는 방식. GUI와 대비된다 | cs |  |
| 49 | `client-server-model.md` | 요청하는 쪽과 응답하는 쪽으로 나뉘어 통신해야 도는 애플리케이션 구조 | cs |  |
| 50 | `cohesion.md` | 데이터에 대한 판단과 조작을 그 데이터를 가진 클래스 안에 두는 정도 | cs |  |
| 51 | `cold-start.md` | 준비된 상태 없이 시작한 실행이 준비 비용부터 다시 치르는 문제 | infra / back? | **infra** |
| 52 | `command-line-arguments.md` | 실행 명령 뒤에 붙여 프로그램 밖에서 넘겨 주는 값 | cs / back? | **cs** |
| 53 | `command-loop.md` | 입력을 받아 해석·분기하고 다시 프롬프트로 돌아오는 대화형 실행 구조 | cs |  |
| 54 | `command-pattern.md` | 할 일 하나를 객체로 만들어 실행을 값처럼 담고 바꿔 끼우는 패턴 | cs |  |
| 55 | `comment.md` | 컴파일 때 무시되는 설명문. 여러 줄·한 줄 문법과 javadoc의 갈래 | cs |  |
| 56 | `compilation.md` | 사람이 쓴 소스를 기계가 실행할 수 있는 코드로 변환하는 단계 | cs |  |
| 57 | `composite-pattern.md` | 하나와 여럿에 같은 타입을 주어 트리의 깊이를 부르는 쪽에서 지우는 패턴 | cs |  |
| 58 | `computer-network.md` | 여러 컴퓨터를 회선으로 이어 데이터를 주고받게 한 것. LAN과 WAN | cs |  |
| 59 | `conditional-flattening.md` | 중첩 if를 가드절·조기 반환으로 펴서 읽을 때 쌓을 층을 없애기 | cs |  |
| 60 | `connection-lifetime-mismatch.md` | 풀의 커넥션 수명이 중간 계층 유휴 타임아웃보다 길어 죽은 연결을 재사용하는 장애 | back |  |
| 61 | `connection-pool-sizing-formula.md` | 커넥션 풀 최대 크기 시작점을 코어 수로 계산하는 경험칙 | back |  |
| 62 | `constant-pool.md` | .class 안에서 이름·문자열·참조를 한 번만 두고 인덱스로 가리키는 표 | back |  |
| 63 | `constructor.md` | new 될 때 실행되어 인스턴스의 초기 상태를 갖춰 주는 것 | cs |  |
| 64 | `container.md` | 한 커널 위에서 게스트 OS 없이 격리돼 도는 프로세스 실행 단위 | infra |  |
| 65 | `context-hierarchy.md` | 스프링 IoC 컨테이너를 루트와 서블릿별 자식으로 나눠 빈을 공유하는 구조 | back |  |
| 66 | `cookie.md` | 서버가 헤더로 브라우저에 맡기고 다음 요청에 되돌려받는 상태 조각 | cs / back? | **cs** |
| 67 | `coupling.md` | 한 코드가 다른 코드에 대해 알아야 하는 것의 양. 변경 전파의 크기 | cs |  |
| 68 | `crud.md` | 데이터 한 종류를 다루면 반드시 생기는 등록·조회·변경·삭제 연산 묶음 | cs |  |
| 69 | `csv.md` | 값 사이에 약속한 구분자를 끼워 경계를 표시하는 텍스트 데이터 형식 | cs |  |
| 70 | `dao-pattern.md` | 저장소에 닿는 코드를 한 층에 모아 부르는 쪽에 SQL을 감추는 패턴 | back / cs? | **cs** |
| 71 | `data-io-stream.md` | 바이트 스트림을 감싸 int·문자열 같은 타입 단위로 읽고 쓰게 하는 층 | back |  |
| 72 | `data-link-layer.md` | 같은 망 안에서 MAC 주소로 받을 상대를 지목해 프레임을 보내는 계층 | cs |  |
| 73 | `data-modeling.md` | 무엇을 저장할지 엔티티와 관계로 그려 중복 없는 표 구조를 만드는 일 | db |  |
| 74 | `data-pipeline.md` | 한 저장소를 주기적으로 읽어 다듬고 다른 저장소로 옮기는 장치 | infra |  |
| 75 | `data-source.md` | 커넥션 획득 방법을 감싼 인터페이스 — 직접 생성인지 풀인지 숨긴다 | back |  |
| 76 | `data-type.md` | 변수가 잡을 메모리의 크기와 해석 방법을 정하는 것 | cs |  |
| 77 | `database-index.md` | 검색 조건 컬럼을 미리 정렬해 따로 들고 조회를 빠르게 하는 구조 | db |  |
| 78 | `database-lock.md` | 같은 데이터를 동시에 만지는 트랜잭션의 순서를 강제하는 장치 | db |  |
| 79 | `database-migration.md` | 돌고 있는 DB를 계속 바뀌는 채로 다른 곳으로 옮기는 일 | db / infra? | **db** |
| 80 | `database-schema.md` | 테이블을 담는 이름공간과 그 인코딩·정렬 기본값 | db |  |
| 81 | `database-user.md` | 접속 자격과 접속 후 권한을 따로 정하는 계정 체계 | db |  |
| 82 | `date-time.md` | 시각을 문자열이 아니라 전용 타입으로 담고 표시할 때 형식을 입히는 것 | back |  |
| 83 | `db-normalization.md` | 중복을 없애려고 테이블을 논리 단위로 쪼개고 외래키로 잇는 설계 원칙 | db |  |
| 84 | `ddl.md` | 값이 아니라 값이 들어갈 틀(DB 객체)을 만들고 고치는 SQL 부류 | db |  |
| 85 | `declarative-transaction.md` | 트랜잭션 경계를 코드 대신 애너테이션 표식으로 적고 프록시가 처리하는 것 | back |  |
| 86 | `decorator-pattern.md` | 같은 타입의 객체를 품고 앞뒤에 기능을 끼워 넣어 겹겹이 확장하는 패턴 | cs |  |
| 87 | `default-initialization.md` | new로 확보한 메모리는 타입별 기본값으로 자동 채워지고 지역변수는 아니다 | back |  |
| 88 | `default-method.md` | 인터페이스가 몸통을 미리 구현해 두어 구현체가 안 채워도 되게 하는 문법 | back |  |
| 89 | `defensive-copy.md` | 내부 저장소를 원본 대신 사본으로 내줘 밖에서 못 흔들게 하는 것 | cs |  |
| 90 | `dependency-injection.md` | 필요한 객체를 스스로 만들지 않고 밖에서 만들어 넣어 주는 것 | cs |  |
| 91 | `dependency-inversion-principle.md` | 고수준과 저수준이 서로가 아니라 같은 추상에 기대게 만드는 원칙 | cs |  |
| 92 | `depth-first-search.md` | 갈 수 있는 데까지 들어갔다 막히면 되돌아 나오는 그래프 탐색 | cs |  |
| 93 | `dispatch-table.md` | 값과 코드의 짝을 자료구조에 담아 분기를 조회로 바꾸는 기법 | cs |  |
| 94 | `dispatcher-servlet.md` | 모든 요청을 받아 처리할 컨트롤러·메서드를 고르는 프론트 컨트롤러 | back |  |
| 95 | `distributed-processing.md` | 데이터와 처리를 여러 노드에 나눠 처리량을 올리고 일관성을 내주는 방식 | db / infra? | **infra** |
| 96 | `distributed-session.md` | 서버가 여러 대가 되면 깨지는 메모리 세션을 외부 저장소로 빼는 것 | back / infra? | **back** |
| 97 | `divide-and-conquer.md` | 문제를 절반씩 쪼개 각각 풀고 합쳐 로그 시간으로 줄이는 기법 | cs |  |
| 98 | `dml.md` | 틀이 아니라 그 안에 든 값을 넣고 고치고 지우는 SQL 부류 | db |  |
| 99 | `do-while-loop.md` | 몸통을 먼저 한 번 실행한 뒤 조건을 판단하는 반복문 | cs |  |
| 100 | `domain-name-system.md` | 이름을 IP 주소로 바꿔 주는 조회 체계 | cs |  |
| 101 | `dql.md` | 테이블에서 원하는 행과 컬럼을 골라 읽어 오는 select 계열 SQL | db |  |
| 102 | `dto.md` | 계층 경계를 넘을 때 값을 담아 나르는 전용 객체 | cs / back? | **cs** |
| 103 | `dynamic-array.md` | 고정 배열이 꽉 차면 더 큰 배열로 옮겨 담아 무한히 늘어나 보이게 한 구조 | cs |  |
| 104 | `dynamic-proxy.md` | 인터페이스만으로 실행 중에 구현체를 만들고 호출을 한 곳으로 모으는 것 | back |  |
| 105 | `dynamic-sql.md` | 넘어온 값에 따라 SQL 문장 조각을 XML 태그로 만들어 내는 것 | back |  |
| 106 | `elasticsearch.md` | 모든 단어를 미리 색인해 두고 색인만 뒤지는 검색 전용 저장소 | db / infra? | **db** |
| 107 | `encapsulation.md` | 필드를 닫고 메서드로만 읽고 쓰게 해 상태 변경 지점을 한곳으로 모으는 것 | cs |  |
| 108 | `endianness.md` | 여러 바이트 값을 어느 쪽 바이트부터 늘어놓는지의 규칙 | cs |  |
| 109 | `exception-handler.md` | 요청 처리 중 난 예외를 어디서 잡아 무엇을 보여 줄지 정하는 장치 | back |  |
| 110 | `exception-handling.md` | 실행 중 오류로 멈추는 것을 막고 오류 흐름을 따로 적는 문법 | cs / back? | **cs** |
| 111 | `expression-language.md` | JSP에서 보관소의 값을 자바 코드 없이 꺼내는 표기법 | back |  |
| 112 | `expression-vs-statement.md` | 값을 돌려주는 문장만 표현식이라는 포함관계. 값이 필요한 자리에 무엇이 올 수 있는지를 정한다 | cs |  |
| 113 | `externalized-configuration.md` | 환경마다 다르거나 비밀인 값을 코드 밖 파일에 두고 실행 시 주입하는 것 | back |  |
| 114 | `factory-bean.md` | 생성자로 못 만드는 객체를 메서드 호출 결과로 스프링 컨테이너에 담는 법 | back |  |
| 115 | `field-hiding.md` | 자식이 부모와 같은 이름의 필드를 선언하면 둘 다 남고 선언 타입이 어느 쪽을 볼지 정한다 | cs |  |
| 116 | `file-class.md` | 파일 내용이 아니라 존재·속성·목록을 다루는 자바 표준 객체 | back |  |
| 117 | `filesystem-path.md` | 같은 파일을 가리키는 이름이 여럿인 이유와 절대·상대·정규의 차이 | cs |  |
| 118 | `floating-point.md` | 실수를 부호·지수·가수로 쪼개 저장하는 방식과 그 오차의 근거 | cs |  |
| 119 | `for-loop.md` | 초기화·조건·증감 세 조각을 한 줄에 모은 반복 구문의 실행 순서 | cs |  |
| 120 | `foreign-key.md` | 한 테이블의 값이 다른 테이블의 실재하는 행을 가리키도록 양방향으로 검사하는 제약 | db |  |
| 121 | `format-string.md` | 출력 틀을 문자열로 적고 값을 따로 넘겨 자리표를 채우는 방식 | cs |  |
| 122 | `front-controller.md` | 모든 요청을 한 진입점이 받아 공통 처리 후 알맞은 처리기로 분배하는 배치 | cs / back? | **cs** |
| 123 | `functional-dependency.md` | A가 정해지면 B도 하나로 정해지는 관계. 정규화가 떼어낼 대상을 찾는 잣대 | db |  |
| 124 | `functional-interface.md` | 추상메서드가 하나뿐인 인터페이스. 람다가 채울 자리를 컴파일러가 특정하는 근거 | cs / back? | **back** |
| 125 | `functional-programming.md` | 데이터를 가진 쪽에 처리 방법을 넘겨 같은 데이터에서 다른 결과를 내는 방식 | cs |  |
| 126 | `gamification.md` | 게임이 아닌 일에 재화·진행도·보상·실패조건을 붙여 다시 열게 만드는 설계 | pm / design? | **pm** |
| 127 | `garbage-collection.md` | 아무도 가리키지 않게 된 인스턴스의 메모리를 런타임이 알아서 회수하는 것 | back |  |
| 128 | `generalization.md` | 여러 클래스에 중복된 코드를 공통 수퍼클래스로 끌어올리는 설계 이동 | cs |  |
| 129 | `generated-keys.md` | insert 뒤 서버가 발급한 auto_increment 값을 그 문장으로부터 되받는 법 | back |  |
| 130 | `generic-servlet.md` | Servlet 인터페이스의 다섯 중 넷을 미리 구현하고 service만 남긴 추상 클래스 | back |  |
| 131 | `generics.md` | 타입을 비워 두고 쓰는 쪽이 채우게 하는 것. 매개변수화를 타입에 적용한 것 | cs |  |
| 132 | `git.md` | 변경마다 식별자를 붙여 어느 시점으로든 되돌아갈 수 있게 하는 형상관리 도구 | infra / cs? | **infra** |
| 133 | `gradle.md` | 컴파일·테스트·산출물 묶기를 태스크로 나눠 명령 하나로 부르는 빌드 도구 | back / infra? | **infra** |
| 134 | `grasp.md` | 「이 일을 누가 해야 하나」를 고르는 객체 책임 할당 지침 아홉 개 | cs |  |
| 135 | `greedy-algorithm.md` | 지금 가장 좋아 보이는 것을 고르고 되돌아보지 않는 풀이. 정렬 기준이 전부다 | cs |  |
| 136 | `grid-traversal.md` | 2차원 배열에서 인접 칸으로 옮겨 다니는 방향 배열과 경계 검사의 정형 | cs |  |
| 137 | `handler-interceptor.md` | 요청 처리의 앞·뒤·끝 세 지점에 공통 코드를 끼워 넣는 스프링 장치 | back |  |
| 138 | `handler-method-argument.md` | 컨트롤러 메서드의 매개변수를 프레임워크가 타입과 표식을 보고 채워 주는 규칙 | back |  |
| 139 | `hash-based-collection.md` | 넣을 자리를 해시로 계산해 저장하는 컬렉션. 같음 판정을 두 단계로 묻는다 | cs / back? | **cs** |
| 140 | `hash-code.md` | 인스턴스를 정수 하나로 요약해 같음 비교를 먼저 걸러 내고 위치 계산에 쓰는 값 | cs / back? | **cs** |
| 141 | `html-form.md` | 사용자 입력에 이름표를 달아 한 URL로 묶어 보내는 브라우저 표준 장치 | front |  |
| 142 | `http-message.md` | 요청과 응답이 선 위로 오갈 때의 형식 — 시작 줄·헤더·빈 줄·본문 | cs |  |
| 143 | `http-method.md` | 요청이 무엇을 하려는지 밝히는 이름. 안전성과 멱등성 두 축으로 갈린다 | cs |  |
| 144 | `http-servlet.md` | GenericServlet을 상속해 HTTP 캐스팅까지 채워 doGet·doPost만 재정의하게 한 클래스 | back |  |
| 145 | `http-session.md` | 서버가 클라이언트 한 명당 하나씩 들고 요청보다 오래 살아야 할 값을 담는 보관소 | back |  |
| 146 | `human-in-the-loop.md` | 자동화를 위험한 자리에서 멈춰 사람 승인을 기다렸다가 그 지점부터 재개하는 것 | ai |  |
| 147 | `idempotency.md` | 같은 요청이 몇 번 와도 한 번 온 것과 결과가 같게 만드는 성질. 재시도의 전제 | cs |  |
| 148 | `identifying-relationship.md` | 부모 키를 자식 기본키에 넣는지 외래키로만 두는지의 선택과 그 종속 강도 | db |  |
| 149 | `if-statement.md` | 조건을 순서대로 따져 첫 참인 가지만 실행하는 분기 제어 | cs / back? | **cs** |
| 150 | `immutability.md` | 만든 뒤 못 바꾸는 객체 — 변경 메서드가 새 인스턴스를 돌려준다 | cs |  |
| 151 | `increment-operator.md` | 1 증감 연산에서 전위·후위에 따라 값 사용 시점이 갈리는 규칙 | cs / back? | **cs** |
| 152 | `infrastructure-as-code.md` | 서버·네트워크를 클릭 대신 파일로 선언해 만드는 방식 (Terraform) | infra |  |
| 153 | `inheritance.md` | 부모 클래스의 멤버를 자식이 물려받는 관계와 생성자 호출 순서 | cs |  |
| 154 | `instance.md` | new 로 확보된 메모리 덩어리와 그 시작 주소를 다루는 개념 | cs |  |
| 155 | `instanceof-operator.md` | 선언 타입이 아닌 실제 들어 있는 인스턴스의 타입을 묻는 검사 | cs / back? | **cs** |
| 156 | `interface-segregation-principle.md` | 약속을 쓰는 쪽 기준으로 잘라 안 쓰는 메서드 의존을 없애는 원칙 | cs |  |
| 157 | `interface.md` | 무엇을 할 수 있는지만 정하고 구현은 비워 둔 타입 | cs |  |
| 158 | `interpreter.md` | 소스를 한 줄씩 변환해 그때그때 실행하는 방식과 그 대가 | cs |  |
| 159 | `io-bound-vs-cpu-bound.md` | 기다려서 느린 일과 계산해서 느린 일을 갈라 처방을 다르게 하기 | cs |  |
| 160 | `io-stream.md` | 통로 끝이 무엇이든 같은 메서드로 읽고 쓰는 단방향 데이터 통로 | back |  |
| 161 | `ioc-container.md` | 객체를 대신 만들어 두고 필요한 곳에 넣어 주는 스프링 저장소 | back |  |
| 162 | `ip-address.md` | 네트워크에서 기계 하나를 가리키는 번호, 포트와 짝을 이룸 | cs |  |
| 163 | `iterator-pattern.md` | 순회 위치를 별도 객체에 담아 컬렉션 내부 구조를 감추는 패턴 | cs |  |
| 164 | `java-compilation-unit.md` | 소스 하나가 들어가고 클래스마다 class 파일 하나가 나오는 단위 | back |  |
| 165 | `java-config.md` | 스프링 설정을 XML 대신 자바 클래스에 애노테이션으로 적는 방식 | back |  |
| 166 | `java-ee.md` | 기업용 기술을 인터페이스 규격으로 적어 둔 명세 문서 묶음 | back |  |
| 167 | `javadoc.md` | 선언 앞 주석에서 HTML API 문서를 뽑아내는 도구와 태그 문법 | back |  |
| 168 | `javascript-type.md` | 변수가 아니라 값에 타입이 붙는 구조와 typeof 의 함정 | front / cs? | **cs** |
| 169 | `jdbc.md` | 자바가 DB 에 접속·질의할 때 부르는 표준 인터페이스와 드라이버 | back |  |
| 170 | `jdk.md` | 실행에 필요한 꾸러미와 개발까지 되는 꾸러미의 포함 관계 | back |  |
| 171 | `json.md` | 값마다 이름을 붙여 중첩까지 표현하는 텍스트 데이터 형식 | cs |  |
| 172 | `jsp-action-tag.md` | 실행 시점에 보관소 객체를 꺼내거나 실행을 넘기는 jsp 전용 태그 | back |  |
| 173 | `jsp-directive.md` | 번역 시점에 이 파일을 어떻게 서블릿으로 만들지 지시하는 문법 | back |  |
| 174 | `jsp-scripting-element.md` | JSP 각 조각이 번역된 서블릿의 어느 자리에 놓이는지 정하는 문법 | back |  |
| 175 | `jsp.md` | HTML 에 자바를 섞어 쓰고 컨테이너가 서블릿으로 번역해 실행 | back |  |
| 176 | `jstl-core-tag.md` | 출력·변수·흐름 제어·URL 을 태그로 처리하는 JSTL 기본 모듈 | back |  |
| 177 | `jstl-format-tag.md` | 날짜·숫자를 문자열과 오가게 바꾸는 JSTL 형식 지정 모듈 | back |  |
| 178 | `jstl.md` | JSP 의 자바 코드를 태그로 대체하는 표준 태그 라이브러리 | back |  |
| 179 | `jvm-stack.md` | 메서드 호출마다 프레임을 쌓고 끝나면 버리는 스택 메모리 영역 | back |  |
| 180 | `jvm.md` | 바이트코드를 OS 위에서 실행해 한 번 짜서 어디서나 돌게 하는 층 | back |  |
| 181 | `jwt.md` | 정보를 담고 서명해 서버 저장 없이 위조 여부를 확인하는 토큰 | back |  |
| 182 | `kubernetes-workload.md` | 버전 전환·개수 유지·실행을 나눠 맡은 세 층의 배포 리소스 | infra |  |
| 183 | `kubernetes.md` | 컨테이너를 여러 서버에 걸쳐 자동 배포·확장·관리하는 플랫폼 | infra |  |
| 184 | `lambda-expression.md` | 매개변수와 처리만 남긴 식이 함수형 인터페이스 구현체로 변환됨 | cs / back? | **cs** |
| 185 | `length-prefix-framing.md` | 가변 길이 데이터 앞에 길이를 적어 바이트 경계를 정하는 규칙 | cs |  |
| 186 | `linear-search.md` | 앞에서부터 하나씩 비교해 찾고 만나면 멈추는 탐색 | cs |  |
| 187 | `linked-list.md` | 노드가 다음 노드 주소를 들고 줄줄이 이어진 목록 | cs |  |
| 188 | `literal.md` | 코드에 직접 적은 값, 표기 방식이 그 값의 타입을 정한다 | cs / back? | **cs** |
| 189 | `little-law.md` | 처리량 = 동시 처리 수 ÷ 처리 시간 이라는 큐잉이론 공식 | cs / infra? | **infra** |
| 190 | `load-balancer.md` | 여러 서버에 요청을 나눠 보내 부하를 분산하는 장치 | infra |  |
| 191 | `load-on-startup.md` | 서블릿을 첫 요청이 아닌 앱 기동 때 미리 초기화하는 설정 | back |  |
| 192 | `lombok.md` | 애노테이션 프로세서로 getter·setter 를 컴파일 때 생성 | back |  |
| 193 | `mac-address.md` | 랜카드마다 박힌 48비트 장치 고유번호와 ARP 조회 | cs |  |
| 194 | `main-method.md` | JVM 이 실행 시 찾아 부르는 고정 형식의 프로그램 진입점 | back |  |
| 195 | `message-broker.md` | 송수신 사이에 저장소를 둬 비동기로 주고받는 발행-구독 | infra / back? | **infra** |
| 196 | `method-overriding.md` | 자식이 부모 메서드를 같은 선언부로 다시 정의하는 것 | cs |  |
| 197 | `method-reference.md` | 기존 메서드 하나를 함수형 인터페이스 구현으로 쓰는 :: 표기 | back |  |
| 198 | `method.md` | 이름 붙여 묶어 둔 기능 한 덩어리와 그 선언 네 부분 | cs |  |
| 199 | `metric-type.md` | 지표를 Counter·Gauge·Histogram 으로 나눠 읽는 법을 정함 | infra |  |
| 200 | `microservice-architecture.md` | 배포 단위를 하나로 둘지 작은 서비스 여럿으로 쪼갤지의 선택 | cs / infra? | **infra** |
| 201 | `modifier-flags.md` | public·static 지정자가 정수 비트로 저장되고 리플렉션이 읽음 | back |  |
| 202 | `monitoring.md` | 수집·저장·시각화·알림으로 돌아가는 것을 밖에서 보는 일 | infra |  |
| 203 | `mrtr.md` | 서버가 역호출 대신 정보 필요 응답을 주고 재요청받는 패턴 | cs / ai? | **ai** |
| 204 | `multidimensional-array.md` | 원소가 다시 배열인 배열, 즉 배열의 배열 구조 | cs |  |
| 205 | `multipart-form-data.md` | 파일 바이트와 문자열을 경계로 나눠 한 요청에 싣는 본문 형식 | back |  |
| 206 | `multiple-inheritance.md` | 상위 타입을 둘 이상 갖는 것과 자바가 클래스에만 막은 이유 | cs |  |
| 207 | `mvc-pattern.md` | 화면·데이터·흐름 제어를 셋으로 갈라 두는 배치 | cs / back? | **cs** |
| 208 | `mybatis-spring.md` | MyBatis 설정과 객체 생성을 스프링 컨테이너에 넘기는 연동 | back |  |
| 209 | `mybatis.md` | SQL 을 XML 로 빼고 id 로 불러 실행하는 SQL 매퍼 | back |  |
| 210 | `n-plus-one.md` | 목록 조회 뒤 연관 데이터를 항목마다 다시 질의하는 문제 | back |  |
| 211 | `nested-class.md` | 클래스 안의 클래스, 바깥 인스턴스 참조 유무로 넷이 갈림 | cs |  |
| 212 | `network-layer.md` | 라우터가 다른 망까지 가는 경로를 정하는 계층 | cs |  |
| 213 | `network-protocol.md` | 통신하는 두 쪽이 같이 지켜야 하는 규칙과 그 층위 | cs |  |
| 214 | `newline-character.md` | 줄 끝을 나타내는 제어 문자가 OS 마다 다른 것 | cs |  |
| 215 | `npm.md` | 자바스크립트 의존성·개발서버·번들을 Node 위에서 다루는 도구 | front | **infra** |
| 216 | `number-parsing.md` | 글자로 된 숫자를 해석해 수 값으로 만드는 일과 그 실패 | cs |  |
| 217 | `object-class.md` | 모든 클래스가 물려받는 상속 계층의 뿌리와 기본 메서드 여섯 | cs / back? | **back** |
| 218 | `object-cloning.md` | 같은 내용의 새 인스턴스를 만드는 일과 얕은·깊은 복사 | cs |  |
| 219 | `object-equality.md` | 같은 인스턴스인가와 내용이 같은가를 갈라 다루는 것 | cs |  |
| 220 | `object-graph.md` | 객체가 객체를 참조해 만들어지는 관계의 그래프 | cs |  |
| 221 | `object-reference.md` | 값 대신 인스턴스의 메모리 주소를 담는 변수 | cs |  |
| 222 | `object-storage.md` | 파일을 경로가 아닌 키로 찾는 객체로 저장하고 HTTP 로 접근 | infra |  |
| 223 | `observer-pattern.md` | 상태가 바뀐 객체가 등록된 구독자들에게 자동으로 알리는 GoF 패턴 | cs |  |
| 224 | `odbc.md` | DB 종류가 달라도 같은 함수로 접속하게 만든 드라이버 표준 API | back / db? | **back** |
| 225 | `ognl.md` | 점으로 이은 문자열 경로로 객체 안의 값을 읽고 쓰는 표현 언어 | back / cs? | **back** |
| 226 | `one-based-numbering.md` | 사람이 보는 1부터의 번호와 0부터의 배열 인덱스 사이 변환과 범위 검사 | cs |  |
| 227 | `open-closed-principle.md` | 기능을 더할 때 기존 파일을 열지 않아도 되게 만드는 설계 원칙 | cs |  |
| 228 | `operator.md` | 값을 계산하고 비교하는 문법 기호들과 그 계산 순서 | cs / back? | **cs** |
| 229 | `optimistic-lock.md` | 잠그지 않고 읽되 저장 시점에 버전 컬럼으로 충돌을 확인하는 방식 | back / db? | **back** |
| 230 | `osi-model.md` | 통신을 일곱 층으로 나누고 내려가며 헤더를 붙이는 구조 | cs |  |
| 231 | `osiv.md` | 영속성 컨텍스트를 요청이 끝날 때까지 열어 두고 커넥션을 붙드는 패턴 | back |  |
| 232 | `output-escaping.md` | 값을 문서에 꽂을 때 문법 문자로 읽히지 않게 치환해 XSS 를 막는 것 | back / front? | **back** |
| 233 | `overflow.md` | 연산 결과가 타입 범위를 넘어 비트가 버려지고 값이 조용히 뒤바뀌는 현상 | cs |  |
| 234 | `package.md` | 클래스를 폴더 구조와 대응시켜 묶고 이름을 구분하는 문법 | back / cs? | **back** |
| 235 | `page-context.md` | JSP 페이지 하나의 실행 상태와 다른 보관소들로 가는 입구를 겸하는 객체 | back |  |
| 236 | `pagination.md` | 전체를 한 번에 안 보내고 시작 행과 개수로 끊어 가져오는 것 | db / back? | **back** |
| 237 | `parameter-and-argument.md` | 값을 받는 선언 쪽 자리와 실제로 넘기는 호출 쪽 값의 구분 | cs |  |
| 238 | `parameterization.md` | 메서드에 박아 둔 값을 매개변수로 올려 부르는 쪽이 고르게 하는 리팩터링 | cs |  |
| 239 | `performance-testing.md` | 얼마나 견디는지 재는 것 정상 성능 확인과 무너지는 지점 찾기 | qa |  |
| 240 | `persistence-context.md` | 엔티티를 DB 에 보내기 전까지 들고 캐시와 변경 감지를 하는 메모리 공간 | back |  |
| 241 | `persistence-framework.md` | 객체와 테이블 사이 반복을 대신하는 층 SQL 을 사람이 쓰나 기계가 쓰나로 갈림 | back |  |
| 242 | `physical-layer.md` | 비트를 실제 전기 신호로 바꿔 케이블에 실어 보내는 층 | cs |  |
| 243 | `platform-dependency.md` | 컴파일 결과물이 특정 CPU 와 OS 를 향해 만들어져 옮겨지지 않는 성질 | cs |  |
| 244 | `polling.md` | 새 것이 있는지 클라이언트가 주기적으로 물어 실시간처럼 보이게 하는 방식 | cs / back? | **cs** |
| 245 | `polymorphism.md` | 같은 선언으로 실제 인스턴스 타입에 따라 다른 동작이 나오는 성질 | cs |  |
| 246 | `port-number.md` | 한 기계 안에서 어느 프로그램이 받을지를 가르는 번호 | cs |  |
| 247 | `prefix-sum.md` | 구간 합을 매번 다시 더하지 않고 빠진 값만 빼고 들어온 값만 더하는 기법 | cs |  |
| 248 | `prepared-statement.md` | SQL 뼈대와 값을 따로 보내 인젝션을 막는 JDBC 문장 객체 | back / db? | **back** |
| 249 | `primary-key.md` | 행을 구분하려 고른 컬럼 그리고 슈퍼키 후보키 대체키로 갈리는 층 | db |  |
| 250 | `priority-queue.md` | 넣은 순서와 무관하게 가장 우선인 것이 먼저 나오는 힙 기반 자료구조 | cs |  |
| 251 | `process.md` | 실행 중인 프로그램 하나 OS 가 메모리와 자원을 묶어 주는 격리 단위 | cs |  |
| 252 | `property-editor.md` | 설정 파일의 문자열을 자바 타입으로 바꿔 주는 스프링 변환기 | back |  |
| 253 | `proxy-pattern.md` | 같은 타입의 대리자를 쥐게 해 실제 객체로 가는 길을 한 곳에 모으는 패턴 | cs |  |
| 254 | `queue.md` | 한쪽으로 넣고 반대쪽으로 빼서 가장 오래된 것이 먼저 나오는 자료구조 | cs |  |
| 255 | `raw-type.md` | 제네릭 클래스를 타입 인자 없이 써서 검사가 사라진 하위 호환용 상태 | back / cs? | **back** |
| 256 | `read-side-effect.md` | 읽기라 이름 붙인 연산이 실제로 데이터를 고칠 때 생기는 문제 | cs |  |
| 257 | `recursion.md` | 메서드가 자기 자신을 다시 불러 스택에 같은 프레임이 쌓이는 방식 | cs |  |
| 258 | `redirect.md` | 응답 대신 다른 주소로 다시 요청하라고 답해 요청이 두 번 일어나게 하는 것 | back |  |
| 259 | `refactoring.md` | 동작은 그대로 두고 구조만 바꿔 다음에 고칠 비용을 줄이는 작업 | cs |  |
| 260 | `reflective-annotation-access.md` | 선언에 붙은 애노테이션을 실행 중에 꺼내 값을 읽는 자바 API | back |  |
| 261 | `reflective-field-access.md` | 필드를 이름으로 찾아 private 이어도 값을 읽고 쓰는 자바 API | back |  |
| 262 | `reflective-instantiation.md` | new 없이 실행 중에 고른 생성자로 인스턴스를 만드는 자바 API | back |  |
| 263 | `reflective-invocation.md` | 메서드를 이름으로 찾아 Method 객체로 호출하는 자바 API | back |  |
| 264 | `remote-procedure-call.md` | 다른 컴퓨터의 객체 호출을 지역 호출처럼 보이게 하는 통신 구조 | cs |  |
| 265 | `remote-repository.md` | 호스팅서버에 둔 git 저장소와 clone·push·pull 로 주고받기 | infra / cs? | **infra** |
| 266 | `request-dispatcher.md` | 한 서블릿이 다른 서블릿을 불러 같은 응답에 끼워 넣는 장치 | back |  |
| 267 | `request-mapping.md` | URL·HTTP 메서드와 컨트롤러 메서드를 잇는 스프링 표식 | back |  |
| 268 | `request-parameter.md` | 클라이언트가 실어 보낸 이름=값 쌍을 서블릿이 꺼내는 통로 | back |  |
| 269 | `request-response.md` | 컨테이너가 요청마다 만들어 넘기는 입력·출력 두 객체 | back |  |
| 270 | `response-body.md` | 컨트롤러 리턴값을 뷰 이름이 아닌 응답 본문으로 해석시키는 규칙 | back |  |
| 271 | `rest-api.md` | URL 은 자원을 가리키고 행위는 HTTP 메서드가 맡는 API 설계 방식 | back / cs? | **cs** |
| 272 | `result-map.md` | 컬럼과 자바 프로퍼티 대응을 따로 선언해 조인 결과를 객체로 조립 | back |  |
| 273 | `result-set.md` | 조회 결과 위에 놓인 커서로 한 행씩 옮겨 가며 값을 꺼내는 것 | back |  |
| 274 | `reverse-proxy.md` | 바깥 요청을 먼저 받아 도메인·SSL 을 정리하고 내부로 넘기는 서버 | infra |  |
| 275 | `role-based-entity.md` | 같은 테이블을 도메인마다 필요한 만큼만 보는 엔티티로 쪼개기 | cs / back? | **cs** |
| 276 | `script-loading.md` | 브라우저가 script 태그를 만나면 멈추고 실행하는 순서와 배치 문제 | front |  |
| 277 | `search-index.md` | 원본과 별도로 두어 키워드로 문서를 빨리 찾게 하는 색인 구조 | db |  |
| 278 | `semaphore.md` | 허가증 N 장으로 동시에 도는 작업 수에 상한을 두는 장치 | cs |  |
| 279 | `serialization.md` | 참조로 얽힌 객체를 파일·네트워크가 받는 바이트 한 줄로 펴는 것 | cs |  |
| 280 | `server-sent-events.md` | 연결을 열어 둔 채 서버가 클라이언트로만 계속 밀어 보내는 통신 | cs / back? | **cs** |
| 281 | `service-layer.md` | 업무 로직과 트랜잭션 제어를 컨트롤러에서 떼어 낸 계층 | cs |  |
| 282 | `servlet-container-initializer.md` | 컨테이너 시작 때 jar 안의 클래스를 찾아 불러 주는 등록 규약 | back |  |
| 283 | `servlet-container.md` | 서블릿을 만들고 부르고 정리하며 흐름을 대신 갖는 실행 환경 | back |  |
| 284 | `servlet-context.md` | 앱마다 하나씩 있는 공용 저장소 겸 컨테이너와의 창구 객체 | back |  |
| 285 | `servlet-filter.md` | 요청이 서블릿에 닿기 전과 응답이 나가기 전에 끼어드는 부품 | back |  |
| 286 | `servlet-lifecycle.md` | 컨테이너가 서블릿을 만들고 준비시키고 부르고 버리는 정해진 순서 | back |  |
| 287 | `servlet-listener.md` | 컨테이너 안에서 생기고 없어지는 이벤트를 통보받는 객체 | back |  |
| 288 | `servlet.md` | HTTP 요청 하나를 받아 응답 하나를 만드는 서버 측 자바 컴포넌트 | back |  |
| 289 | `short-circuit-evaluation.md` | 앞의 값으로 결과가 정해지면 뒤를 계산하지 않는 논리 연산 규칙 | cs |  |
| 290 | `simulation.md` | 특별한 알고리즘 없이 문제가 시키는 절차를 그대로 옮기는 풀이 유형 | cs |  |
| 291 | `singleton-pattern.md` | 생성자를 닫고 입구를 하나만 두어 인스턴스를 하나로 묶는 설계 | cs |  |
| 292 | `socket-binding.md` | 소켓에 내 쪽 IP·포트를 붙여 어디로 온 접속을 받을지 정하는 일 | cs |  |
| 293 | `socket.md` | 두 프로그램 사이에 뚫린 통로의 끝, 스트림으로 데이터가 오간다 | cs |  |
| 294 | `solid-principles.md` | 나중에 고치기 쉬운 구조인지를 재는 객체지향 설계 기준 다섯 | cs |  |
| 295 | `sorting.md` | 순서를 만드는 것, 실제로 정할 것은 비교 함수의 기준뿐 | cs |  |
| 296 | `spring-boot.md` | 스프링 설정을 기본값으로 밀어 넣고 서버까지 품은 위층 | back |  |
| 297 | `spring-framework.md` | 애플리케이션 뼈대를 미리 만들어 두고 그 안에 내 클래스를 끼우게 하는 자바 프레임워크 | back |  |
| 298 | `spring-model.md` | 컨트롤러가 뷰에게 값을 넘기는 통로. request.setAttribute 자리를 대신한다 | back |  |
| 299 | `spring-security.md` | 모든 요청 앞에 필터를 세워 누구인가(인증)와 해도 되는가(인가)를 검사 | back |  |
| 300 | `sql-data-type.md` | 컬럼 하나가 어떤 값을 얼마만큼 담을 수 있는지 서버에 선언해 두는 것 | db |  |
| 301 | `sql-date-function.md` | 날짜를 서버 쪽에서 읽고 꺼내고 옮기고 재고 형식을 바꾸는 함수들 | db |  |
| 302 | `sql-injection.md` | 입력 문자열이 SQL 문장의 일부로 파싱되어 의도 밖 문장이 실행되는 것 | back / db? | **back** |
| 303 | `sql-join.md` | 여러 테이블의 행을 짝지어 한 행으로 잇는 것. 쪼갠 테이블을 다시 붙인다 | db |  |
| 304 | `sql-like.md` | 문자열을 정확히 같은가가 아니라 이런 모양인가로 비교하는 연산자 | db |  |
| 305 | `sql-null.md` | 컬럼마다 값 없음을 허용할지와 값을 생략하면 무엇이 들어갈지를 정하는 것 | db |  |
| 306 | `sql-operator.md` | where 조건 하나를 만들어 내는 비교·논리·범위 기호들 | db |  |
| 307 | `sql-session.md` | 연결 하나를 품고 SQL 문자열과 값을 받아 실행해 주는 객체. JDBC 반복을 감춘다 | back |  |
| 308 | `sql-set-operation.md` | 조회 결과 두 개를 위아래로 합치거나 서로 빼서 하나로 만드는 것 | db |  |
| 309 | `stack.md` | 한쪽 끝에서만 넣고 빼는 목록. 가장 최근 것을 공짜로 알려 준다 | cs |  |
| 310 | `staging-area.md` | 다음 커밋에 담을 파일을 미리 등록해 두는 중간 자리 | infra / cs? | **infra** |
| 311 | `standard-input.md` | 프로그램이 사용자에게서 값을 받는 기본 통로. 바이트라 감싸야 타입이 읽힌다 | back / cs? | **cs** |
| 312 | `stateless-protocol.md` | 세션을 두지 않고 요청마다 필요한 정보를 스스로 담아 독립 처리하는 통신 규약 | cs |  |
| 313 | `static-and-dynamic-content.md` | 응답이 파일로 이미 있는가 요청받고 나서 만들어지는가. 웹서버와 WAS를 가른다 | cs / back? | **cs** |
| 314 | `static-member.md` | 멤버가 클래스에 붙느냐 인스턴스에 붙느냐. 부르는 법과 닿는 상태가 갈린다 | cs |  |
| 315 | `stereotype-annotation.md` | 이 클래스를 컨테이너에 담으라는 표식. 스캔이 훑어 빈으로 만든다 | back |  |
| 316 | `string-builder.md` | 문자열을 새로 만들지 않고 그 자리에서 고쳐 쓰는 가변 버퍼 | back |  |
| 317 | `string-comparison.md` | ==는 주소를 equals는 내용을 비교한다. 문자열 풀이 그 차이를 흐린다 | back |  |
| 318 | `string-manipulation.md` | 자르고 찾고 뒤집는 몇 개의 연산으로 대부분의 문자열 문제를 끝내는 법 | cs |  |
| 319 | `subnet.md` | IP 주소를 어느 망인가와 그 안의 몇 번인가로 가르는 선을 긋는 문제 | cs |  |
| 320 | `surrogate-key.md` | 몇 번째인가가 아니라 몇 번인가를 데이터가 필드로 들고 있게 하는 것 | cs / db? | **db** |
| 321 | `switch-statement.md` | 값 하나를 여러 후보와 견주어 맞는 곳부터 실행하는 조건문 | cs |  |
| 322 | `tcp.md` | 바이트를 보낸 순서대로 빠짐없이 상대에게 넘겨 주는 연결형 전송 프로토콜 | cs |  |
| 323 | `template-engine.md` | 틀과 데이터를 합쳐 문서를 만들어 주는 도구. 코드와 화면을 가른다 | back |  |
| 324 | `template-fragment.md` | 여러 화면이 함께 쓰는 부분을 한 파일에 두고 이름으로 끼워 넣는 것 | back |  |
| 325 | `template-method-pattern.md` | 일의 순서는 부모가 갖고 달라지는 단계만 자식이 채우게 하는 구조 | cs |  |
| 326 | `terminal-state-ttl.md` | 진행 중인 큐 키에는 만료를 안 걸고 작업이 끝난 시점에만 TTL을 주는 방식 | back / infra? | **back** |
| 327 | `ternary-operator.md` | 조건에 따라 두 값 중 하나를 골라 돌려주는 표현식 | cs |  |
| 328 | `this-reference.md` | 인스턴스 메서드에 컴파일러가 숨겨 넘기는 대상 인스턴스의 주소 | cs |  |
| 329 | `thread-join.md` | 다른 흐름이 끝날 때까지 지금 흐름을 세워 그 결과를 안전하게 읽는 것 | cs / back? | **cs** |
| 330 | `thread-local.md` | 필드 하나가 흐름마다 다른 값을 갖게 해 잠그는 대신 공유를 없애는 것 | back / cs? | **cs** |
| 331 | `thread-state.md` | 만들어진 실행 흐름이 끝날 때까지 지나가는 단계. start는 실행이 아니라 대기줄 | cs |  |
| 332 | `thread.md` | 한 프로그램 안에서 따로 흐르는 실행 흐름 하나. 흐름을 여럿으로 늘린다 | cs |  |
| 333 | `thymeleaf.md` | HTML 파일 그대로가 템플릿인 엔진. 브라우저로 열어도 화면이 보인다 | back |  |
| 334 | `time-complexity.md` | 입력 크기 대비 연산 증가율. 제약을 보고 쓸 알고리즘을 고르는 기준 | cs |  |
| 335 | `tomcat.md` | 서블릿 규격 구현체. 웹서버와 웹컨테이너를 한 프로세스에 가진 WAS | back |  |
| 336 | `transaction-propagation.md` | 트랜잭션 메서드가 다른 트랜잭션 안에서 불릴 때의 합류·분리 규칙 | back |  |
| 337 | `transaction.md` | 여러 문장을 전부 되거나 전부 안 되게 묶는 단위와 autocommit 경계 설정 | db |  |
| 338 | `transport-layer.md` | 끝에서 끝까지 온전한 도착을 책임지고 포트로 프로그램을 식별하는 층 | cs |  |
| 339 | `try-with-resources.md` | 블록을 어떤 경로로 나가든 선언한 자원의 close 를 자동 호출하는 문법 | back |  |
| 340 | `twos-complement.md` | 음수를 비트로 저장하는 방식. 1의 보수에 1을 더해 0 중복과 덧셈 문제를 해결 | cs |  |
| 341 | `type-alias.md` | 패키지 포함 정규 클래스명에 짧은 별칭을 등록해 XML 에서 그 이름으로 가리킴 | back |  |
| 342 | `type-casting.md` | 상속 관계에서 참조 변수 타입을 부모·자식 쪽으로 바꾸는 업다운 캐스팅 | cs / back? | **cs** |
| 343 | `type-erasure.md` | 제네릭 타입 인자가 컴파일 후 지워져 런타임에는 구분이 사라지는 것 | back |  |
| 344 | `type-promotion.md` | 산술 연산 시 피연산자 타입을 자동으로 맞추는 규칙. 정수 최소 단위는 int | back |  |
| 345 | `unicode.md` | 전세계 문자에 번호를 매긴 표준과 그 번호를 바이트로 담는 UTF 인코딩 | cs |  |
| 346 | `unique-key.md` | 기본키가 아니면서 값 중복을 막아야 하는 컬럼에 거는 유일성 제약 | db |  |
| 347 | `universal-scalability-law.md` | 동시 처리 단위를 늘릴수록 경쟁·일관성 비용으로 처리량이 꺾이는 모델 | cs / back? | **cs** |
| 348 | `url.md` | 자원을 위치로 가리키는 URL 과 이름으로 가리키는 URN 을 묶는 상위 식별자 | cs |  |
| 349 | `varargs.md` | 점 셋으로 인수 개수를 호출 쪽이 정하게 하고 받는 쪽은 배열로 받는 문법 | back |  |
| 350 | `variable-scope.md` | 같은 이름이 여러 층에 있을 때 가장 가까운 층을 고르는 이름 해석 순서 | cs / back? | **cs** |
| 351 | `variable.md` | 값을 담을 메모리를 타입과 이름으로 확보하는 선언, 그리고 값을 넣는 할당 | cs |  |
| 352 | `view-resolver.md` | 컨트롤러가 돌려준 뷰 이름에 접두·접미사를 붙여 실제 화면 파일로 바꾸는 것 | back |  |
| 353 | `web-application-deployment.md` | 코드를 실행하는 게 아니라 돌고 있는 서버가 찾아갈 자리에 war 를 놓는 일 | back / infra? | **infra** |
| 354 | `web-application-server.md` | 요청을 받아 내 코드를 실행해 동적 응답을 만드는 서버. 실행 주인이 서버로 넘어감 | back |  |
| 355 | `web-application.md` | 설치 없이 브라우저 위에서 통신으로 쓰는 비설치형 클라이언트 서버 소프트웨어 | cs |  |
| 356 | `web-component.md` | 컨테이너가 직접 생성해 호출하는 서버측 부품 묶음. 리스너 필터 서블릿 셋 | back |  |
| 357 | `web-server.md` | 요청을 받아 이미 파일로 있는 정적 자원을 그대로 내보내는 프로그램 | cs / back? | **cs** |
| 358 | `web-xml.md` | 어떤 클래스를 어떤 URL 로 부를지 적어 컨테이너가 기동 때 읽는 설정 파일 | back |  |
| 359 | `websocket.md` | 연결을 열어 두고 양쪽이 아무 때나 보내는 양방향 통신과 그 위의 메시징 규약 | back / cs? | **cs** |
| 360 | `while-loop.md` | 조건을 먼저 검사하고 참인 동안 반복하는 제어문. 거짓이면 한 번도 안 돈다 | cs |  |
| 361 | `wildcard-type.md` | 제네릭이 상속을 타지 않는 벽을 뚫으려 타입 인자 자리에 범위를 적는 문법 | back |  |
| 362 | `wireless-lan.md` | 전파로 통신하는 LAN 과 유선 구간을 이어 주는 액세스 포인트 | cs |  |
| 363 | `workflow-orchestration.md` | 작업을 함수 호출이 아니라 단계로 선언해 이음매와 상태를 밖에 드러내는 것 | ai |  |
| 364 | `wrapper-class.md` | 기본 타입 값 하나를 객체로 감싸 객체를 요구하는 자리에 넣게 해 주는 클래스 | back |  |
| 365 | `xml.md` | 태그로 값을 감싸 데이터를 나무 구조로 적고 태그를 직접 정의하는 텍스트 형식 | cs |  |
| 366 | `zero-downtime-deployment.md` | 새 버전을 옆에 띄워 두고 준비되면 트래픽만 돌려 빈 시간을 없애는 배포 | infra |  |
