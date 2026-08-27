---
type: concept
id: bean-definition
title: 빈 정의 (bean 태그)
aliases:
  - bean 태그
  - 빈 정의
  - bean definition
  - constructor-arg
  - "ref 속성"
  - getBean
up:
  - 2024-10-02-Day87
tags:
  - spring
  - 설정
  - xml
---

# 빈 정의 (bean 태그)

**컨테이너에게 「이 클래스로 객체를 만들고, 이 이름으로 부르고, 이 값들을 넣어라」를 적는 선언.** XML 에서는 `<bean>` 태그 하나가 그 전부를 담는다.

## 정의

### 이름 — `id` 와 `name`

```xml
<bean id="c1" class="com.eomcs.spring.ioc.ex02.Car"/>            <!-- 이름 -->
<bean id="c2" name="c3" class="...Car"/>                          <!-- 이름 + 별명 -->
<bean name="c4" class="...Car"/>                                  <!-- name 만 주면 그것이 이름 -->
<bean id="c5" name="c51 c52 c53" class="...Car"/>                 <!-- 별명 여럿 -->
<bean name="c91 c92 c93" class="...Car"/>                         <!-- 첫 별명이 이름이 된다 -->
```

- **별명 구분자는 공백·콤마(`,`)·세미콜론(`;`) 셋뿐이다.** `c81:c82:c83` 은 나뉘지 않고 통째로 하나가 된다
- `id="c11 c12 c13"` 도 **쪼개지지 않는다** — `id` 는 문자열 하나다
- 꺼낼 때는 `getBean("이름")` 이나 `getBean("별명")` 둘 다 되고, 별명 목록은 `getAliases("이름")` 으로 본다(없으면 `null`)

이름을 아예 안 주면 **익명 빈**이 된다.

```xml
<bean class="...Car"/>   <!-- 이름: "...Car#0" — 그리고 클래스명 별명이 이것에만 붙는다 -->
<bean class="...Car"/>   <!-- "...Car#1" -->
```

이름 대신 **타입으로** 꺼낼 수도 있다(`getBean(Car.class)`). 다만 **같은 타입 빈이 둘 이상이면 그 방법은 실패한다** → [[ioc-container]]

### 생성자로 넣기 — `<constructor-arg>`

```xml
<bean id="c1" class="...Car">
  <constructor-arg index="0" type="java.lang.String" value="소나타"/>
  <constructor-arg index="1" type="int" value="2024"/>
</bean>
```

- 아무 것도 안 주면 **기본 생성자**가 불린다
- `type` 을 안 주면 컨테이너가 고르는데 **String 이 우선**이라 의도와 다른 생성자가 잡힐 수 있다
- `index` 로 순서를 못 박을 수 있다
- 값은 **문자열로 적고 컨테이너가 형변환**한다. 못 하면 예외다 → [[type-casting]] · [[number-parsing]]

### 세터로 넣기 — `<property>`

```xml
<bean id="c1" class="...Car">
  <property name="model" value="소나타"/>
  <property name="year" value="2024"/>
  <property name="engine" ref="e1"/>      <!-- 값이 아니라 다른 빈 -->
</bean>
```

**`value` 는 값, `ref` 는 다른 빈**이다 — 이 한 글자 차이가 [[dependency-injection]] 이다.

**선언 순서는 상관없다.** `ref="e1"` 을 만났을 때 `e1` 이 아직 안 만들어졌으면 그때 찾아 만든다.

속성 축약형도 있다(네임스페이스 선언이 필요하다).

```xml
<bean id="c1" class="...Car" c:model="소나타" c:_0="2024"/>   <!-- 생성자 -->
<bean id="c2" class="...Car" p:model="소나타" p:year="2024"/>  <!-- 세터 -->
```

### 컬렉션 넣기

```xml
<property name="engines">
  <list><bean class="...Engine"/><bean class="...Engine"/></list>
</property>

<property name="options">
  <map>
    <entry key="color" value="red"/>
    <entry key="engine" value-ref="e1"/>
  </map>
</property>

<property name="settings">
  <props><prop key="url">jdbc:...</prop></props>
</property>
```

`<array>`·`<list>`·`<map>`·`<props>` 가 각각 배열·리스트·맵·`Properties` 다 → [[array]] · [[hash-based-collection]]

프로퍼티 안에서 **이름 없는 임시 빈**을 만들어 바로 넣을 수도 있다. 다만 **그렇게 만든 것은 다른 빈이 `ref` 로 가져다 쓸 수 없다** — 그 자리에만 존재한다.

## 왜 중요한가

**객체 그래프 전체가 선언으로 적힌다.** 어떤 객체가 어떤 값을 갖고 누구를 참조하는지가 `new` 코드를 읽지 않고도 한 파일에서 보인다 → [[object-graph]]

**그리고 이름이 계약이 된다.** `ref="e1"` 은 `id="e1"` 을 가리키는 문자열이라, **컴파일러가 검사하지 않는 연결**이다. 오타는 기동할 때 「그런 빈 없다」로 나타난다 — [[java-config]] 가 이 문제의 절반을 푸는 이유다.

## 경계와 오해

- **`id` 하나에 공백을 넣어도 별명이 되지 않는다** — `id="c11 c12 c13"` 은 **공백을 포함한 이름 하나**다. 별명을 여럿 주려면 `name` 을 써야 한다. 필기가 이 둘을 예시로 나란히 놓아 구별한다
- **`type` 을 생략하면 String 이 이긴다** — 생성자가 `(String)` 과 `(int)` 로 오버로딩돼 있으면 `<value>0000</value>` 은 String 쪽으로 간다. **숫자처럼 생겼다고 숫자로 가지 않는다** → [[method]]
- **자동 형변환은 되는 것과 안 되는 것이 있다** — `"2024"` → `int` 는 되고 `"소나타"` → `int` 는 예외다. 설정이 틀렸다는 것을 **기동에서** 알려 준다는 점은 오히려 다행이다
- **`value` 와 `ref` 를 헷갈리면 문자열이 들어간다** — `value="e1"` 은 「`e1` 이라는 글자」이지 그 빈이 아니다. 타입이 맞으면 **오류 없이 잘못된 값**이 들어간다
- **임시 빈은 재사용할 수 없다** — 프로퍼티 안에 `id` 를 적어도 컨테이너에 등록되지 않는다. 두 곳에서 같은 것을 쓰려면 밖에 따로 선언해야 한다
- **이 문법 전체가 XML 전용은 아니다** — 같은 결정(이름·스코프·생성자·세터·참조)을 [[java-config]] 에서는 메서드와 반환값으로 적는다. **문법이 아니라 결정을 배우는 절**이다

## 함께 보는 개념

- [[ioc-container]] — 이 선언을 읽는 주체
- [[bean-scope]] — 같은 태그의 `scope` 속성
- [[factory-bean]] — 생성자 대신 팩토리로 만드는 방법
- [[java-config]] — 같은 선언을 자바로 적는 쪽
- [[dependency-injection]] — `ref` 가 하는 일
- [[xml]] — 네임스페이스(`c:`·`p:`)가 필요한 이유
- [[type-casting]] — 문자열이 타입으로 바뀌는 자리

## 출처

- [[2024-10-02-Day87]] — 「bean 태그 사용법」부터 「다양한 타입의 의존객체 주입하기」까지가 이 개념의 전부다. **`id`/`name`/별명의 규칙을 예시 아홉 줄로 훑어** 공백·콤마·세미콜론만 구분자가 되고 콜론은 안 된다는 것, `id` 는 통째로 하나라는 것, `name` 만 주면 첫 별명이 이름이 된다는 것을 각각 짚었다. 익명 빈의 이름이 `FQName#index` 이고 **0번에만 클래스명 별명이 붙는다**는 관찰도 남아 있다. `<constructor-arg>` 절이 **타입을 안 주면 String 이 우선 적용된다**는 것과 `index`·`type` 으로 못 박는 법을, `<property>` 절이 `value`(값)와 `ref`(다른 빈)의 갈림과 **선언 순서가 상관없다**는 것을, 컬렉션 절이 `<array>`·`<list>`·`<map>`/`<entry>`·`<props>` 를 다룬다. 프로퍼티 안의 임시 빈이 **다른 곳에서 `ref` 로 못 쓰인다**는 제약도 주석으로 적혀 있다. 다만 예시가 대부분 `FQName`·`VarName` 같은 자리표시자라 실제 클래스와 이어 보기는 어렵고, `<map>` 예시에는 `<map>` 태그 자체가 빠져 있다
