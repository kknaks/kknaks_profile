---
type: concept
id: externalized-configuration
title: 설정 외부화 (@PropertySource · @Value)
aliases:
  - "@PropertySource"
  - 설정 외부화
  - externalized configuration
  - properties 파일
  - 환경 설정 분리
up:
  - 2024-09-29-Day84
tags:
  - spring
  - 설정
  - 배포
  - 보안
---

# 설정 외부화 (@PropertySource · @Value)

**환경마다 달라지는 값과 비밀로 두어야 하는 값을 코드 밖 파일에 두고, 실행할 때 읽어 넣는 것.** 스프링에서는 `@PropertySource` 가 파일을 지정하고 `@Value` 가 값을 꽂는다.

## 정의

```java
@PropertySource("classpath:config/jdbc.properties")
@PropertySource("file:${user.home}/config/ncp.properties")
public class AppConfig { ... }
```

```properties
ncp.storage.bucketname=bitcamp-bucket96
ncp.accesskey=...
ncp.secretkey=...
```

```java
@Value("${ncp.storage.bucketname}")
private String bucketName;

public NcpObjectStorageService(@Value("${ncp.accesskey}") String accessKey, ...) { ... }
```

**두 접두어가 성격을 가른다.**

| 접두어 | 어디서 읽나 | 무엇을 두나 |
|---|---|---|
| `classpath:` | **빌드 결과물 안** | 환경이 달라도 같은 값 |
| `file:` | 파일 시스템의 절대 경로 | **저장소에 올리면 안 되는 값** |

`file:${user.home}/config/ncp.properties` — **홈 디렉토리**를 가리키므로 그 파일은 프로젝트 폴더 밖에 있고, 실수로 커밋될 수 없다.

주입받는 자리도 둘이다.

- **필드** — `@Value` 를 필드에 붙인다. 객체가 만들어진 **뒤에** 채워진다
- **생성자 매개변수** — 생성자가 끝나기 전에 값이 필요하면 이쪽이어야 한다

필기의 `NcpObjectStorageService` 가 그 구별을 정확히 쓴다 — `bucketName` 은 나중에 쓰니 필드로, 엔드포인트·키는 생성자 안에서 클라이언트를 만드는 데 쓰이니 매개변수로 받는다 → [[dependency-injection]]

## 왜 중요한가

**같은 빌드 결과물을 여러 환경에 올릴 수 있게 된다.** 접속 주소와 계정이 코드에 박혀 있으면 개발·운영이 다른 빌드가 되고, 「운영에 올릴 때 이 줄을 고친다」는 절차가 생긴다 — 그 절차는 언젠가 잊힌다 → [[web-application-deployment]]

**그리고 비밀이 저장소에 남지 않는다.** 액세스 키를 커밋하면 되돌려도 히스토리에 남는다. 이 회차가 `classpath:` 와 `file:${user.home}/...` 를 갈라 쓰는 것이 그 대응이다 → [[git]] · [[remote-repository]]

## 경계와 오해

- **`classpath:` 에 두면 저장소에 올라간다** — DB 접속 정보를 `classpath:config/jdbc.properties` 로 둔 이 회차의 코드는 **비밀이 여전히 프로젝트 안에 있다.** 스토리지 키만 홈으로 뺐고 DB 비밀번호는 안 뺐다 — **같은 노트 안에서 두 기준이 갈린다**
- **파일을 못 찾으면 기동이 실패한다** — `@PropertySource` 가 가리키는 파일이 없으면 컨텍스트가 안 뜬다. 새 개발자가 받은 코드가 「내 컴퓨터에서 안 돈다」가 되는 흔한 자리라, **예시 파일(`.properties.sample`)을 함께 두는 관례**가 여기서 나온다
- **`@Value` 의 이름이 틀려도 컴파일은 된다** — 문자열이라 오타는 기동 시점이나 실행 시점에야 드러난다. 애노테이션이 만드는 계약이 늘 그렇다 → [[annotation]]
- **`${user.home}` 은 스프링이 푸는 것이 아니라 시스템 속성이다** — 자바가 제공하는 값이라 OS 마다 다른 곳을 가리킨다. **환경 차이를 없애려고 쓴 표현이 환경마다 다른 경로가 되는** 자리다 → [[filesystem-path]] · [[platform-dependency]]
- **설정을 뺐다고 안전해지지 않는다** — 서버에 올려둔 그 파일의 권한이 열려 있으면 같은 이야기다. **위치를 옮긴 것과 접근을 막은 것은 다르다**
- **환경 변수와 파일 중 무엇이 맞는지는 상황이 정한다** — 이 회차는 파일만 쓴다. 컨테이너로 배포하면 환경 변수 쪽이 더 자연스러워지고, 스프링은 둘 다 같은 `${...}` 로 읽는다

## 함께 보는 개념

- [[data-source]] — 이 방식으로 접속 정보를 받는 대표 자리
- [[object-storage]] — 액세스 키를 이렇게 빼야 하는 이유
- [[ioc-container]] — 값을 읽어 넣어 주는 주체
- [[dependency-injection]] — 필드 주입과 생성자 주입이 갈리는 축
- [[web-application-deployment]] — 환경마다 값이 달라지는 축
- [[git]] · [[remote-repository]] — 비밀이 남으면 안 되는 곳

## 출처

- [[2024-09-29-Day84]] — 「Spring에 불러오기」가 `@PropertySource("classpath:config/jdvc.properties")` 로 DB 접속 정보를 빼고, 「bucket 생성」이 스토리지 정보를 **`@PropertySource("file:${user.home}/config/ncp.properties")`** 로 뺀다 — **같은 노트에서 `classpath:` 와 `file:` 두 접두어가 나란히 쓰이는 것**이 이 개념의 핵심 대비다(다만 왜 갈라 쓰는지는 적혀 있지 않다). `NcpObjectStorageService` 의 코드가 `@Value` 를 **필드와 생성자 매개변수 두 자리**에 쓰는 예도 함께 보인다. 파일명 `jdvc.properties` 는 `jdbc` 의 오기로 보이고, 예시 클래스에 `@Service` 가 두 번 붙어 있다
