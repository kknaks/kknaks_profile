---
type: concept
id: application-event
title: 애플리케이션 이벤트 (@EventListener)
aliases:
  - ApplicationEvent
  - ApplicationEventPublisher
  - "@EventListener"
  - "@Async"
  - 스프링 이벤트
up:
  - 2025-02-19-Day32
  - 2025-02-20-Day33
tags:
  - spring
  - 설계
  - 결합도
---

# 애플리케이션 이벤트 (@EventListener)

**「무슨 일이 일어났다」를 알리기만 하고, 그것으로 무엇을 할지는 듣는 쪽이 정한다.** 부르는 쪽이 상대를 모르게 만드는 장치다.

## 정의

**전**: 게시글을 쓰면 알림 서비스를 직접 부른다.

```java
private void firePostCreateEvent(Post post) {
  notiService.postCreated(post);      // PostService 가 NotiService 를 안다
}
```

**후**: 사건만 발행한다.

```java
private final ApplicationEventPublisher eventPublisher;

public RsData<Post> write(Author author, String title, String content) {
  ...
  eventPublisher.publishEvent(new PostCreatedEvent(this, post));   // 누가 듣는지 모른다
  return RsData.of(post);
}
```

```java
@Getter
public class PostCreatedEvent extends ApplicationEvent {
  private final Post post;
  public PostCreatedEvent(Object source, Post post) { super(source); this.post = post; }
}
```

```java
@Component
@RequiredArgsConstructor
public class NotiEventListener {
  private final NotiService notiService;

  @EventListener
  public void listenPost(PostCreatedEvent event) {     // 듣는 쪽이 자기를 등록한다
    notiService.postCreated(event.getPost());
  }
}
```

**의존의 방향이 뒤집힌다** — 알림 모듈이 게시글 모듈을 알고, 게시글 모듈은 알림을 모른다 → [[dependency-inversion-principle]] · [[observer-pattern]]

### 비동기로 돌리기

```java
@EnableAsync            // 설정 클래스에
@Async                  // 리스너 메서드에
```

붙이면 **발행한 쪽이 기다리지 않는다** → [[thread]]

## 왜 중요한가

**새 기능을 더할 때 기존 코드를 안 고친다.** 게시글이 생겼을 때 통계도 올리고 검색 색인도 넣고 싶으면 **리스너를 하나씩 더하면 된다** — `PostService` 는 그대로다 → [[open-closed-principle]]

**그리고 마이크로서비스로 가는 중간 다리다.** 이 회차가 적은 전환 순서가 그 지도다.

```
서비스 → 모듈 → 종속성 분리 → 마이크로서비스
```

같은 프로세스 안의 이벤트를 [[message-broker]] 의 토픽으로 바꾸면 **코드 구조는 그대로 두고 프로세스만 나눌 수 있다** — 발행하는 쪽은 어차피 누가 듣는지 몰랐기 때문이다 → [[microservice-architecture]]

## 경계와 오해

- **기본은 동기다** — `publishEvent` 가 리스너를 **그 자리에서 부르고 기다린다.** 「이벤트라서 비동기」가 아니고, 비동기로 하려면 `@Async` 를 붙여야 한다
- **동기 이벤트는 같은 트랜잭션 안에서 돈다** — 리스너에서 예외가 나면 **발행한 쪽까지 롤백**된다. 알림 실패가 게시글 저장을 되돌리는 것이 맞는지 따져야 한다 → [[declarative-transaction]]
- **비동기로 바꾸면 트랜잭션이 갈린다** — 다른 쓰레드라 **커밋 전의 데이터를 못 볼 수도 있다.** 커밋 이후에 부르는 별도 장치(`@TransactionalEventListener`)가 그래서 있다 → [[transaction]]
- **흐름이 코드에서 사라진다** — `publishEvent` 만 보고는 무슨 일이 일어나는지 모른다. **리스너를 다 찾아봐야** 하므로, AOP 와 같은 종류의 대가를 치른다 → [[aop]]
- **이벤트 클래스가 도메인 객체를 그대로 담으면 결합이 남는다** — `PostCreatedEvent` 가 `Post` 엔티티를 통째로 들고 있으면 알림 모듈이 여전히 게시글 엔티티를 안다. **필요한 값만 담는 것**이 다음 걸음이다 → [[dto]]
- **순서를 보장하지 않는다** — 리스너가 여럿이면 실행 순서는 정해져 있지 않다. 순서가 중요하면 **그것 자체가 잘못된 설계 신호**인 경우가 많다

## 함께 보는 개념

- [[observer-pattern]] — 이 구조의 원형
- [[message-broker]] — 프로세스를 넘어서는 같은 방식
- [[microservice-architecture]] — 이 분리가 향하는 곳
- [[dependency-inversion-principle]] — 의존 방향이 뒤집히는 원리
- [[declarative-transaction]] — 이벤트가 트랜잭션과 얽히는 자리
- [[aop]] — 흐름이 코드에서 사라진다는 같은 대가
- [[role-based-entity]] — 같은 회차의 다른 분리 방법

## 출처

- [[2025-02-20-Day33]] — 하루 뒤. **이 장치와 메시지 브로커가 같은 자리에 나란히 놓인다** — `PostService.write()` 안에서 스프링 이벤트를 발행한 바로 다음 줄에 `kafkaTemplate.send(...)` 가 있고, 리스너 클래스에도 `@EventListener` 와 `@KafkaListener` 가 함께 있다. **한 프로세스 안에서 끊어 둔 결합을 프로세스 밖으로 옮기는 것이 얼마나 짧은 거리인지**가 이 대비로 드러난다 — 발행하는 쪽 코드는 거의 그대로다 → [[message-broker]]
- [[2025-02-19-Day32]] — 「스프링 이벤트」 절이 **전후 코드를 나란히** 놓았다 — `PostService` 가 `notiService.postCreated(post)` 를 직접 부르던 것이 `eventPublisher.publishEvent(new PostCreatedEvent(this, post))` 가 되고, 알림 쪽에 `@EventListener` 를 붙인 `NotiEventListener` 가 생긴다. `PostCreatedEvent` 를 **`global/event` 패키지**에 두어 어느 모듈에도 속하지 않게 한 것도 의도가 분명하다. 마지막에 `@EnableAsync`+`@Async` 로 비동기 처리를 붙이는 방법이 인용으로 붙어 있다. 이 절 전체가 **「모놀리식 → 마이크로서비스」 전환의 세 번째 단계(종속성 분리)** 로 자리매김돼 있는 것이 이 노트의 구성이다 → [[microservice-architecture]]
