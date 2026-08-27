---
type: content
id: C-006
date: 2026-05-03
duration: '2:48'
speaker: 5분개발지식
kind: study
youtubeId: boXNtyeOzuc
title:
  en: Understanding the Observer Pattern
  ko: 옵저버 패턴 이해하기
summary:
  en: A design pattern that automatically notifies multiple observers when a subject's state changes
  ko: 객체의 상태 변화를 자동으로 감지하고 관심 있는 여러 관찰자에게 알리는 디자인 패턴
tags:
- '#design-pattern'
- '#observer'
- '#publisher-subscriber'
- '#solid'
- '#event-driven'
---

## 요지

- 옵저버 패턴은 한 객체(Subject/Publisher)의 상태 변화를 여러 객체(Observer/Subscriber)가 자동으로 감지하고 반응하는 패턴이다.
- Publisher는 subscribers 목록을 관리하고, 상태 변화 시 notify()를 호출하여 모든 subscriber에게 일괄 알림을 보낸다.
- Subscriber는 subscribe()/unsubscribe()로 등록/해제되며, 알림 수신 시 자신의 핸들러(update())를 실행하여 개별 동작을 정의한다.
- 다형성으로 인해 새로운 subscriber 클래스를 추가해도 publisher 코드는 변경될 필요 없으므로 SOLID의 개방-폐쇄 원칙(OCP)을 만족한다.

## 개요

옵저버 패턴(Observer Pattern)은 소프트웨어 디자인 패턴 중 하나로, 한 객체의 상태 변화가 발생할 때 그 변화에 관심 있는 여러 객체들에게 자동으로 알림을 전달하는 방식입니다. 실생활 예시로 이해하면 더 쉬운데, 관심 있는 대상을 주기적으로 직접 확인하는 번거로움 대신, 대상이 변할 때 자동으로 알려주는 방식입니다. 이 패턴은 느슨한 결합(loose coupling)을 유지하면서도 효율적으로 상태 변화를 전파할 수 있어 모던 소프트웨어 개발에서 매우 중요합니다.

## 배경 / 사전 지식

### 용어 정의

- **Subject (또는 Publisher)**: 상태를 관리하고 변화를 발행하는 주체 객체
- **Observer (또는 Subscriber)**: Subject의 상태 변화를 관찰하고 반응하는 객체
- **상태 변화**: Subject의 내부 상태가 어떤 이유로 인해 변하는 것
- **알림 (Notification)**: Subject가 상태 변화를 Observer들에게 전달하는 행위
- **느슨한 결합 (Loose Coupling)**: 두 객체 간 직접적인 의존성을 최소화하는 설계 원칙

### 패턴이 필요한 상황

Observer 패턴이 없다면, Subject의 변화를 감지하려는 객체들이 계속 Subject를 폴링(polling)해야 합니다. 즉, "변경됐나?" "변경됐나?"를 반복적으로 물어봐야 합니다. 이는 불필요한 CPU 사용, 네트워크 요청, 메모리 낭비를 초래합니다.

## 핵심 개념

### Observer 패턴의 기본 구조

Observer 패턴은 다음 세 가지 주요 개념으로 구성됩니다:

#### 1. Publisher (발행자)

Publisher는 상태를 관리하고, 상태 변화 시 Observer들에게 알림을 보내는 객체입니다. Publisher 내부에는 자신에게 등록된 Observer들을 저장하는 목록(보통 배열이나 리스트)을 유지합니다. Publisher는 다음 메서드를 제공합니다:

- `subscribe(observer)`: Observer를 등록
- `unsubscribe(observer)`: Observer를 해제
- `notify()`: 모든 등록된 Observer에게 알림 전송

#### 2. Subscriber (구독자)

Subscriber는 Publisher의 상태 변화에 관심이 있는 객체입니다. Subscriber는 다음 메서드를 구현합니다:

- `update()`: Publisher로부터 알림을 받았을 때 실행되는 메서드

Subscriber는 Publisher에 `subscribe()` 메서드를 호출하여 자신을 등록하고, 더 이상 관심이 없으면 `unsubscribe()`를 호출하여 해제합니다.

#### 3. 이벤트 전파

Publisher의 상태가 변하면, Publisher는 자신의 subscribers 목록을 순회하면서 각 subscriber의 `update()` 메서드를 호출합니다. 이때 필요한 정보(예: 어떤 상태가 변했는지, 새로운 값이 무엇인지)를 인자로 전달할 수 있습니다.

### 실생활 예시: 아파트 매물

아파트 매입을 원하는 구매자들의 입장에서 생각해봅시다:

**Observer 패턴 없는 경우:**
- 구매자가 관심 있는 아파트의 새 매물 여부를 확인하려면 매일 공인중개사를 직접 방문해야 합니다.
- 99%의 방문은 "아직 매물이 없습니다"라는 답변을 받고 돌아옵니다.
- 이는 시간 낭비이고 비효율적입니다.

**Observer 패턴을 적용한 경우:**
- 구매자는 공인중개사에게 "이 아파트에 관심 있으니 새 매물 나오면 알려줘"라고 등록합니다. (subscribe)
- 구매자가 다른 아파트에 입주하면 공인중개사에게 "더 이상 이 아파트는 필요 없어"라고 해제합니다. (unsubscribe)
- 새로운 매물이 나오면 공인중개사는 등록된 모든 구매자에게 자동으로 연락합니다. (notify)

이렇게 하면 구매자는 효율적으로 관심 있는 정보만 받을 수 있고, 공인중개사는 변화가 있을 때만 한 번에 알릴 수 있습니다.

## 작동 원리

Observer 패턴의 동작은 다음과 같은 단계로 진행됩니다:

1. **초기화**: Publisher는 빈 subscribers 목록을 생성합니다.

2. **등록 (Subscribe)**:
   - Observer가 Publisher의 `subscribe(observer)` 메서드를 호출합니다.
   - Publisher는 이 Observer를 자신의 subscribers 목록에 추가합니다.
   - 이 시점부터 이 Observer는 Publisher의 상태 변화 알림을 받을 자격이 생깁니다.

3. **상태 변화**:
   - Publisher의 내부 상태가 변합니다.
   - Publisher는 이 변화를 감지합니다.

4. **알림 전파 (Notify)**:
   - Publisher는 `notify()` 메서드를 호출합니다.
   - `notify()` 메서드는 subscribers 목록의 모든 Observer를 순회합니다.
   - 각 Observer의 `update(eventType, data)` 메서드를 호출합니다.
   - 필요시 상태 변화의 타입(예: "새 매물 추가", "가격 인하")과 상세 정보를 인자로 전달합니다.

5. **개별 반응**:
   - 각 Observer는 자신의 `update()` 메서드에서 받은 알림에 따라 개별적인 로직을 실행합니다.
   - Observer A는 이메일을 발송하고, Observer B는 모바일 앱에 푸시 알림을 보낼 수 있습니다.
   - Observer들은 서로를 알지 못하며 독립적으로 동작합니다.

6. **해제 (Unsubscribe)**:
   - Observer가 더 이상 알림을 받고 싶지 않으면 `unsubscribe(observer)`를 호출합니다.
   - Publisher는 subscribers 목록에서 이 Observer를 제거합니다.
   - 이 이후로 이 Observer는 알림을 받지 않습니다.

## 코드 예시

### Java 예제

```java
import java.util.ArrayList;
import java.util.List;

// 1. Observer 인터페이스 정의
interface Observer {
    void update(String message);
}

// 2. Publisher 클래스 정의
class RealEstateOffice {
    private List<Observer> subscribers = new ArrayList<>();
    private String latestProperty;
    
    // Observer 등록
    public void subscribe(Observer observer) {
        subscribers.add(observer);
    }
    
    // Observer 해제
    public void unsubscribe(Observer observer) {
        subscribers.remove(observer);
    }
    
    // 새 매물 추가 시 모든 Observer에게 알림
    public void setNewProperty(String property) {
        latestProperty = property;
        notifyObservers();
    }
    
    // 모든 Observer에게 알림 전송
    private void notifyObservers() {
        for (Observer observer : subscribers) {
            observer.update(latestProperty);
        }
    }
}

// 3. Observer 구현 - 구매자 1
class Buyer implements Observer {
    private String name;
    
    public Buyer(String name) {
        this.name = name;
    }
    
    @Override
    public void update(String message) {
        System.out.println(name + "님에게 알림: " + message);
    }
}

// 4. Observer 구현 - 구매자 2
class AnotherBuyer implements Observer {
    private String email;
    
    public AnotherBuyer(String email) {
        this.email = email;
    }
    
    @Override
    public void update(String message) {
        System.out.println("이메일로 발송 (" + email + "): " + message);
    }
}

// 5. 사용 예제
public class ObserverDemo {
    public static void main(String[] args) {
        RealEstateOffice office = new RealEstateOffice();
        
        Buyer buyer1 = new Buyer("김철수");
        AnotherBuyer buyer2 = new AnotherBuyer("lee@email.com");
        
        // 구매자들이 등록
        office.subscribe(buyer1);
        office.subscribe(buyer2);
        
        // 새 매물이 나옴 → 모든 등록된 구매자에게 알림
        office.setNewProperty("강남구 래미안 아파트 3000만원");
        // 출력:
        // 김철수님에게 알림: 강남구 래미안 아파트 3000만원
        // 이메일로 발송 (lee@email.com): 강남구 래미안 아파트 3000만원
        
        // 김철수가 이미 다른 아파트에 입주함
        office.unsubscribe(buyer1);
        
        // 새 매물이 또 나옴 → buyer2만 받음
        office.setNewProperty("서초구 아파트 2500만원");
        // 출력:
        // 이메일로 발송 (lee@email.com): 서초구 아파트 2500만원
    }
}
```

### Python 예제

```python
from abc import ABC, abstractmethod

# 1. Observer 추상 클래스
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

# 2. Publisher 클래스
class RealEstateOffice:
    def __init__(self):
        self._subscribers = []
        self._latest_property = None
    
    def subscribe(self, observer):
        """Observer 등록"""
        if observer not in self._subscribers:
            self._subscribers.append(observer)
    
    def unsubscribe(self, observer):
        """Observer 해제"""
        self._subscribers.remove(observer)
    
    def set_new_property(self, property_info):
        """새 매물 추가 및 알림"""
        self._latest_property = property_info
        self._notify_observers()
    
    def _notify_observers(self):
        """모든 Observer에게 알림 전송"""
        for observer in self._subscribers:
            observer.update(self._latest_property)

# 3. Observer 구현 - 구매자
class Buyer(Observer):
    def __init__(self, name):
        self.name = name
    
    def update(self, message):
        print(f"{self.name}님에게 알림: {message}")

# 4. Observer 구현 - 이메일 발송
class EmailNotifier(Observer):
    def __init__(self, email):
        self.email = email
    
    def update(self, message):
        print(f"이메일로 발송 ({self.email}): {message}")

# 5. 사용 예제
office = RealEstateOffice()

buyer1 = Buyer("김철수")
email_notifier = EmailNotifier("lee@email.com")

# 구매자들이 등록
office.subscribe(buyer1)
office.subscribe(email_notifier)

# 새 매물이 나옴 → 모든 등록된 Observer에게 알림
office.set_new_property("강남구 래미안 아파트 3000만원")
# 출력:
# 김철수님에게 알림: 강남구 래미안 아파트 3000만원
# 이메일로 발송 (lee@email.com): 강남구 래미안 아파트 3000만원

# 김철수가 더 이상 관심 없음
office.unsubscribe(buyer1)

# 새 매물이 또 나옴 → EmailNotifier만 받음
office.set_new_property("서초구 아파트 2500만원")
# 출력:
# 이메일로 발송 (lee@email.com): 서초구 아파트 2500만원
```

### 코드 해설

위 예제에서:

- **`Observer` 인터페이스**: 모든 Observer가 구현해야 하는 계약입니다. `update()` 메서드 하나만 정의하면 됩니다.
- **`RealEstateOffice` (Publisher)**: `_subscribers` 리스트로 Observer들을 관리합니다. `subscribe()`, `unsubscribe()`, `_notify_observers()`를 통해 Observer들과 상호작용합니다.
- **`Buyer`, `EmailNotifier` (구체적 Observer)**: 각각 다른 방식으로 알림을 처리합니다. Publisher는 이들이 어떻게 반응할지 알 필요가 없습니다.
- **다형성**: Publisher는 Observer 인터페이스만 알면 됩니다. 새로운 Observer 클래스(예: `SMSNotifier`)를 추가해도 Publisher 코드는 변경되지 않습니다.

## 함정·실수

### 1. 메모리 누수 (Memory Leak)

**흔한 실수:**
```java
// 잘못된 예
Observer observer = new Buyer("김철수");
office.subscribe(observer);
observer = null;  // 로컬 변수만 null이 됨
// observer는 여전히 office의 subscribers 목록에 남음!
```

**해결법:**
- Observer를 더 이상 사용하지 않을 때는 반드시 `unsubscribe()`를 호출해야 합니다.
- 특히 Observer가 장시간 메모리에 남을 가능성이 있다면 더욱 중요합니다.
- 일부 언어/프레임워크는 약한 참조(weak reference)를 사용하여 이 문제를 완화할 수 있습니다.

### 2. 순환 참조와 무한 루프

**흔한 실수:**
```java
// 잘못된 예
class Buyer implements Observer {
    private RealEstateOffice office;
    
    public void update(String message) {
        // Observer가 다시 Publisher의 메서드를 호출
        office.setNewProperty(message);  // 무한 루프 발생!
    }
}
```

**해결법:**
- Observer의 `update()` 메서드 내에서 Publisher의 상태를 변경하는 메서드를 호출하지 않도록 주의합니다.
- 필요하다면 이를 명시적으로 디자인하고 방지 로직을 추가합니다.

### 3. 이벤트 타입 구분 부재

**흔한 실수:**
```java
// 부족한 예
public void notifyObservers() {
    for (Observer observer : subscribers) {
        observer.update("뭔가 변했습니다");  // 무엇이 변했는지 모름!
    }
}
```

**해결법:**
- Publisher는 알림 시 이벤트 타입이나 상태 정보를 전달해야 합니다.
- Observer는 받은 정보를 바탕으로 필요한 작업만 수행할 수 있습니다.

```java
// 개선된 예
public void notifyObservers(EventType eventType, Object data) {
    for (Observer observer : subscribers) {
        observer.update(eventType, data);
    }
}
```

### 4. 동기 vs 비동기 처리

**흔한 실수:**
```java
// Publisher의 notify()가 모든 Observer의 update()가 완료될 때까지 대기
// Observer가 느리면 전체 시스템이 느려짐
```

**해결법:**
- 성능이 중요한 경우 Observer의 `update()` 메서드를 별도 스레드에서 실행합니다.
- 또는 메시지 큐를 사용하여 비동기로 처리합니다.

## 베스트 프랙티스

### 1. SOLID 원칙 준수

**개방-폐쇄 원칙 (Open/Closed Principle)**
- Publisher는 새로운 Observer 추가에 개방되어 있습니다 (확장 가능).
- 기존 Publisher 코드는 수정되지 않습니다 (변경에 폐쇄).

**의존성 역전 원칙 (Dependency Inversion Principle)**
- Publisher는 구체적인 Observer 클래스에 의존하지 않고, Observer 인터페이스에만 의존합니다.

### 2. 이벤트 정보 전달

```java
// 구조화된 이벤트 객체 사용
class PropertyEvent {
    public enum Type { ADDED, REMOVED, PRICE_CHANGED }
    
    private Type type;
    private String address;
    private int price;
    
    public PropertyEvent(Type type, String address, int price) {
        this.type = type;
        this.address = address;
        this.price = price;
    }
    
    // getter들...
}

// Observer 인터페이스
interface PropertyObserver {
    void onPropertyEvent(PropertyEvent event);
}
```

이렇게 하면 필요한 정보를 명확하게 전달할 수 있고, Observer는 이벤트 타입을 쉽게 구분할 수 있습니다.

### 3. Publisher-Subscriber 별칭 용어

일부 컨텍스트에서는 Observer 패턴을 다음과 같이 부릅니다:
- **Subject** = Publisher (상태를 발행하는 주체)
- **Observer** = Subscriber (변화를 구독하는 관찰자)

이 용어들은 같은 개념을 다르게 부르는 것입니다.

### 4. 약한 참조 (Weak Reference) 고려

언어가 지원하는 경우, 메모리 누수를 방지하기 위해 observers 목록을 약한 참조로 저장할 수 있습니다.

```java
// Java 예시
private List<WeakReference<Observer>> subscribers = new ArrayList<>();
```

### 5. 이벤트 필터링

Observer가 관심 있는 특정 이벤트만 수신하도록 선택할 수 있게 합니다.

```java
public void subscribe(Observer observer, EventType eventType) {
    // 특정 이벤트 타입만 구독
}
```

### 6. 프레임워크 및 라이브러리 활용

많은 언어와 프레임워크에서 Observer 패턴을 기본으로 제공합니다:
- **Java**: `java.util.Observer`, Spring의 이벤트 메커니즘
- **JavaScript**: DOM 이벤트 시스템, RxJS
- **Python**: `asyncio.Event`, Django의 시그널
- **C++**: Boost.Signals2

이러한 기존 구현을 활용하면 더 안정적이고 검증된 코드를 작성할 수 있습니다.

## 참고

(영상 내 명시 없음)

### 관련 개념
- **Pub-Sub 패턴 (Publisher-Subscriber)**: Observer 패턴의 확장으로, 중앙 메시지 브로커를 통해 Publisher와 Subscriber가 완전히 분리됩니다.
- **MVC/MVVM**: View가 Model의 변화를 관찰하는 Observer 패턴의 적용 사례입니다.
- **Event-Driven Architecture**: Observer 패턴을 시스템 전체에 확대한 아키텍처입니다.
- **Reactive Programming**: RxJS, Reactor 등의 라이브러리에서 Observer 패턴 기반의 리액티브 프로그래밍을 제공합니다.