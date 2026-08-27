---
type: concept
id: jwt
title: JWT (JSON Web Token)
aliases:
  - JWT
  - JSON Web Token
  - 액세스 토큰
  - 리프레시 토큰
  - 클레임
up:
  - 2025-01-10-Day09
tags:
  - 보안
  - 인증
  - web
---

# JWT (JSON Web Token)

**정보를 담고 서명해 둔 문자열.** 서버가 저장해 두지 않아도, **서명을 확인하는 것만으로** 그 안의 값이 위조되지 않았음을 안다.

## 정의

세 조각이 점으로 이어져 있다.

| 조각 | 무엇 |
|---|---|
| **헤더** | 토큰 유형(JWT)과 서명 알고리즘(HS512 등) |
| **페이로드** | **클레임** — 담을 정보(사용자 id 등)와 만료 시각 |
| **서명** | 헤더+페이로드를 **비밀 키로** 서명한 값 |

```java
Jwts.builder()
    .setHeaderParam("typ", "JWT")
    .claim("body", Ut.json.toStr(claims))       // 담을 정보
    .setExpiration(accessTokenExpiresIn)        // 만료 시각
    .signWith(getSecretKey(), SignatureAlgorithm.HS512)
    .compact();
```

검증은 같은 키로 서명을 다시 맞춰 보는 것이다.

```java
Jwts.parserBuilder()
    .setSigningKey(getSecretKey())
    .build()
    .parseClaimsJws(token);      // 위조·만료면 여기서 예외
```

비밀 키는 **설정 파일에 두고 코드 밖에서 온다** → [[externalized-configuration]]

```yaml
custom:
  jwt:
    secret: [어려운 문자열]
  accessToken:
    expirationSeconds: "#{60 * 10}"
```

### 액세스 토큰과 리프레시 토큰

수명이 다른 둘을 함께 쓴다.

- **액세스 토큰** — 짧다(분 단위). 매 요청에 실려 간다
- **리프레시 토큰** — 길다. **액세스가 만료됐을 때 새로 발급**받는 데만 쓴다

## 왜 중요한가

**서버가 세션을 안 들고 있어도 된다.** [[http-session]] 방식은 서버 메모리에 「누가 로그인했는지」를 두므로, 서버가 여러 대면 그 정보를 공유해야 한다. 토큰은 **필요한 정보를 클라이언트가 들고 다니고 서버는 확인만** 하므로 그 문제가 사라진다 → [[distributed-processing]] · [[microservice-architecture]]

그래서 설정에 `SessionCreationPolicy.STATELESS` 가 함께 나온다 — **세션을 아예 만들지 않겠다**는 선언이다.

## 경계와 오해

- **JWT 는 암호화가 아니라 서명이다** — 페이로드는 Base64 로 인코딩됐을 뿐 **누구나 열어 읽을 수 있다.** 비밀번호나 개인정보를 담으면 안 된다. 서명이 보장하는 것은 **「바뀌지 않았다」이지 「안 보인다」가 아니다** → [[character-encoding]]
- **서버가 토큰을 취소할 수 없다** — 저장하지 않으니 **로그아웃해도 그 토큰은 만료 전까지 유효**하다. 그래서 액세스 토큰을 짧게 두고, 정말 막아야 하면 결국 서버에 목록을 둔다 — **무상태의 이점을 되돌리는 지점**이다
- **탈취되면 그것으로 끝이다** — 토큰 하나가 곧 신분증이다. 쿠키에 담을 때 `HttpOnly`(자바스크립트 접근 차단)·`Secure`(HTTPS 만)를 켜는 이유가 그것이고, 필기의 코드가 정확히 그렇게 한다 → [[cookie]] · [[output-escaping]]
- **필기의 코드는 쿠키를 두 번 추가한다** — 옵션 없는 `new Cookie("accessToken", token)` 을 먼저 넣고 옵션 붙인 것을 또 넣는다. **앞엣것이 보호 없는 쿠키**라 그대로 두면 `HttpOnly` 를 켠 의미가 없다
- **비밀 키가 새면 전부 위조된다** — 서명이 그 키 하나에 걸려 있다. 저장소에 올라가면 **모든 사용자로 로그인할 수 있는 열쇠**가 공개되는 것이다 → [[externalized-configuration]]
- **만료 시간을 숨기는 것은 보안이 아니다** — 필기가 「사용자가 토큰 만료시간을 알지 못하게 한다」고 적었는데, **만료 시각은 페이로드에 그대로 들어 있어 누구나 본다.** 설정을 파일로 뺀 이유는 환경마다 바꾸기 위해서다

## 함께 보는 개념

- [[http-session]] — 서버가 상태를 들고 있던 방식
- [[cookie]] — 토큰을 실어 나르는 그릇
- [[spring-security]] — 이 토큰을 검사하는 자리
- [[externalized-configuration]] — 비밀 키를 두는 곳
- [[json]] — 클레임이 담기는 형식
- [[rest-api]] — 무상태 통신이 전제되는 곳

## 출처

- [[2025-01-10-Day09]] — 「JWT」 절이 **세 조각의 역할을 먼저 정의하고 그대로 만든다.** `jjwt` 의존성 셋(api/impl/jackson), `application.yml` 의 `secret`·`expirationSeconds`, JSON↔Map 유틸(`Ut`), 그리고 `Jwts.builder()` 로 발급하고 `Jwts.parserBuilder()` 로 검증하는 코드가 이어진다. 비밀 키를 **Base64 로 인코딩한 뒤 `Keys.hmacShaKeyFor` 로 만들고 캐시**하는 처리까지 남아 있다. 발급한 토큰을 쿠키로 내보내며 **`setHttpOnly(true)`·`setSecure(true)`·`setMaxAge`** 를 켜는 것, 검증 실패 시 리프레시 토큰으로 새 액세스 토큰을 발급하는 흐름, 로그아웃에서 토큰을 지우는 것까지 한 벌이다. 다만 페이로드가 **암호화되지 않는다**는 것은 다루지 않았고, 「토큰 시간 설정을 숨겨서 사용자가 토큰 만료시간을 알지 못하게 한다」는 설명은 사실과 다르다
