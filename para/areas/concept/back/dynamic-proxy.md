---
type: concept
id: dynamic-proxy
title: 동적 프록시 (Dynamic Proxy)
aliases:
  - 동적 프록시
  - dynamic proxy
  - JDK 동적 프록시
  - Proxy.newProxyInstance
  - newProxyInstance
  - InvocationHandler
  - java.lang.reflect.Proxy
up:
  - 2024-08-22-Day61
  - 2024-09-26-Day83
  - 2024-08-23-Day62
  - 2025-01-21-Day16
tags:
  - java
  - 리플렉션
  - 실행시점
  - 디자인패턴
---

# 동적 프록시 (Dynamic Proxy)

**인터페이스만 주면 그것을 구현한 클래스를 실행 중에 만들어 주고, 모든 메서드 호출을 `invoke` 하나로 몰아 주는 것.** `Proxy.newProxyInstance` 가 클래스를 만들고 `InvocationHandler` 가 그 몸통을 갖는다. Day61 이 이것으로 **`UserDao`·`BoardDao`·`ProjectDao` 세 구현 클래스를 지웠다** — 인터페이스만 남기고 몸통은 메서드 하나가 됐다 → [[proxy-pattern]] · [[dao-pattern]]

## 정의

만드는 쪽은 인수가 셋이고, 필기가 셋의 역할을 정확히 적었다.

| 인수 | Day61 의 설명 | 왜 필요한가 |
|---|---|---|
| `ClassLoader` | 「클래스를 메모리에 로딩하는 일을 할 객체의 주소를 준다」 | 클래스가 **실행 중에 만들어지므로** 그것을 올릴 로더가 필요하다 → [[class-loading]] |
| `Class[]` | 「자동 생성할 클래스가 구현해야 하는 인터페이스 목록」 | 만들어진 객체의 **타입**이 된다 |
| `InvocationHandler` | 「구현체에서 해야할 일을 설정한다」 | 모든 메서드의 **몸통 하나** |

```java
Proxy.newProxyInstance(
    this.class.getClassLoader(), // 클래스를 메모리에 로딩하는 일을 할 객체
    new Class[] {Interface.class}, // 자동 생성할 클래스가 구현해야 하는 인터페이스 목록
    new InvocationHandler(){
      @Override
      public Object invoke(Object proxy, Method method, Object[] args)        
    }
);
```

받는 쪽은 인수가 셋이다.

| `invoke` 의 인수 | Day61 의 설명 | 실제 값 |
|---|---|---|
| `proxy` | 「실제 객체처럼 메서드를 호출할 수 있도록 대리 역할을 한다」 | **호출된 그 프록시 객체** |
| `method` | 「클라이언트가 호출한 메서드」 | `Method` — 이름·매개변수·리턴 타입을 물을 수 있다 |
| `args` | 「클라이언트가 호출한 메서드의 파라미터 정보」 | 인수 배열, **매개변수가 없으면 `null`** |

**여기서 나오는 것이 Day59 의 리플렉션이 쓰던 것과 같은 `Method` 객체다.** 다른 것은 방향이다 — 그때는 내가 `Method` 를 **찾아서 불렀고**, 여기서는 남이 부른 것이 `Method` 로 **손에 온다** → [[reflective-invocation]]

### 인터페이스만 된다 — 그래서 Dao 가 인터페이스가 되어야 했다

두 번째 인수가 `Class[]` 이지만 거기 들어갈 수 있는 것은 **인터페이스뿐**이다. 클래스를 넣으면 실행 시점에 `IllegalArgumentException` 이다. 그래서 Day61 의 순서가 정해져 있다 — **`UserDao` 를 클래스에서 인터페이스로 바꾸는 것이 이 도구를 쓰는 전제**이고, 그 전까지 Day55~59 의 DAO 는 구현 클래스뿐이었다.

「Dao 인터페이스에는 매개변수가 0~2개가 있다」·「return 타입에 따라 수행하는 메서드가 다르다」 두 줄이 그 인터페이스를 읽어 낸 결과이고, 그것이 곧 `invoke` 가 갈라야 하는 축이 된다 → [[interface]] · [[dao-pattern]]

### 몸통 하나가 메서드 열다섯 개를 대신하는 방법 — 두 축으로 가른다

`invoke` 는 어느 메서드가 불렸는지를 **`method` 에게 물어서** 알아낸다. Day61 이 축을 둘 세웠다.

| 축 | 무엇으로 묻나 | 갈라지는 것 |
|---|---|---|
| 매개변수 개수 | `args` (와 `method.getParameters()`) | `sqlSession` 에 넘길 **파라미터의 모양** |
| 리턴 타입 | `method.getReturnType()` | 부를 `sqlSession` **메서드** |

```java
// 0개: null · 1개: args[0] · 2개 이상: Map
// List → selectList · int·void·boolean → insert · 그 밖 → selectOne
```

**두 축이 [[dispatch-table]] 의 「이름으로 고른다」와 같은 일을 「시그니처로」 하는 것**이다. 이름을 키로 쓰면 표를 관리해야 하는데, 시그니처는 **인터페이스 선언에 이미 적혀 있다** — 그래서 표가 필요 없다. 대신 **선언이 조금만 달라도 엉뚱한 쪽으로 간다**(아래 「경계와 오해」) → [[reflective-invocation]]

## 사용 예시

Day61 의 `DaoFactory` 가 이 도구를 실습 프로젝트에 붙인 형태다. **제네릭 메서드 하나가 세 DAO 를 다 만든다.**

```java
//Dao설계
//UserDao, BoardDao, ProjectDao가 있으므로 T로 받는 메서드를 생성
private <T> T createObject(Class<T> daoType){
  return new Proxy.newProxyInstance(
      this.getClass().getClassLoader(),
      new Class[]{daoType},
      this::invoke    
  );
} 

//리턴타입과 매개변수가 같으면 메서드 레퍼런스 사용가능
private Object invoke(Object proxy, Method method, Object[] args){
  //매개변수를 담는다.
  
  //리턴타입에 따라 수행할 메서드를 나눈다.
}
```

**`Class<T> daoType` 하나가 두 곳에 쓰인다** — 프록시가 구현할 인터페이스 목록이 되고, 동시에 반환 타입 `T` 를 정한다. Day40 의 `loadJson(List<E> list, …, Class<E> elementType)` 과 같은 문법이고, 여기서는 **「무엇을 만들지」와 「무엇으로 받을지」가 같은 값에 묶인다** → [[generics]] · [[class-metadata]]

`this::invoke` 가 통하는 이유는 `InvocationHandler` 가 추상 메서드 하나짜리 인터페이스라서다 — 필기의 주석(「리턴타입과 매개변수가 같으면 메서드 레퍼런스 사용가능」)이 그 조건의 절반을 적었다 → [[method-reference]] · [[functional-interface]]

매개변수 쪽은 개수로 갈린다.

```java
Object paramValue = null;
if (args != null){
  if (agrs.length ==1{
    paramValue = args[0];
  } else {
    Parameter[] params = method.getParameters();
    HashMap<String,Object> map = new HashMap<>();
    for (int i = 0; i < args.length; i++){
      Param anno = params.getAnnotation(Param.class);
      map.put(anno, args[i]);
      }
    paramValue = map;
  }
}
```

**`if (args != null)` 이 이 블록에서 가장 정확한 한 줄이다.** 매개변수가 없는 메서드가 불리면 `args` 는 빈 배열이 아니라 **`null`** 이다 — `InvocationHandler` 의 명세가 그렇고, `args.length == 0` 으로 검사하면 `list()` 를 부르는 순간 `NullPointerException` 이다. 나머지 줄에는 오류가 넷 있다(아래) → [[object-reference]]

값이 둘 이상일 때 `Map` 이 필요해지는 이유가 [[mybatis]] 쪽에 있다 — 매퍼 XML 의 `#{no}` 는 **이름으로** 값을 찾는데, `args[0]`·`args[1]` 에는 이름이 없다. 필기가 그 문제를 정확히 적었다 — 「mapper에 사용할 property와 args[n]과 다르기 때문에 Map을 넘긴다 하더라도 get하지 못한다」.

그래서 **애노테이션을 직접 만든다.** 이 필기에서 애노테이션이 장식이 아니라 **일을 하는** 첫 자리다.

```java
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.PARAMETER)
public @interface Param{
  String value();
}

//Dao 적용예시
void updateViewCount(@Param("no") int boardNo, @Param("count") int count)
```

**두 메타 애노테이션이 각각 필요한 이유가 여기서 처음 코드로 갈린다.** `RUNTIME` 이 아니면 `invoke` 가 실행 중에 읽을 수 없고, `PARAMETER` 가 아니면 매개변수 앞에 붙일 수 없다 — [[annotation-target]] 노트가 「두 메타 애노테이션은 직교하는 두 축이고 필기가 둘을 함께 쓴 예를 한 번도 보이지 않았다」고 적어 둔 자리가 **하루 뒤 이 여섯 줄로 채워진다** → [[annotation-retention]] · [[annotation]]

그리고 이 애노테이션이 메우는 구멍이 [[reflective-invocation]] 에 이미 적혀 있다 — **매개변수 이름은 클래스 파일에서 지워져 `arg0`·`arg1` 로 나온다.** `boardNo`·`count` 라는 이름을 실행 중에 알 방법이 없으므로 **같은 이름을 애노테이션에 한 번 더 적는** 것이 답이고, 그 노트가 「Spring 이 옛날에 `@Param`·`@RequestParam` 으로 이름을 다시 적게 했던 이유가 이것이다」로 예고한 것을 **이틀 뒤 필기가 스스로 재발명했다** → [[class-file-format]] · [[reflective-annotation-access]]

리턴 타입 쪽은 `Class` 객체를 `==` 로 비교한다.

```java
Class<?> returnType = method.getReturnType();

if (returnType == List.class){
  return sqlSession.selectList("sql.method", paramValue);
} else if (returnType == int.class || returnType == void.class || returnType == boolean.class ){
  int count = sqlSession.insert("sql.method", paramValue);
  if (returnType == boolean.class){
    return count > 0;  
  } else if (returnType == void.class){
    return null  
  } else{
    return count;  
  }
} else {
  return sqlSession.selectOne("sql.method", paramValue);
}
```

**`boolean` 을 `count > 0` 으로 접는 것과 `void` 에 `null` 을 돌려주는 것이 DAO 다섯 시그니처를 그대로 흡수하는 장치다** — [[dao-pattern]] 의 `boolean insert(Project)`·`List<Project> list()`·`Project findBy(int)` 세 모양이 이 분기 셋과 1:1 로 맞는다. `void` 에 `null` 을 돌려주는 것도 규칙이다 — `invoke` 의 반환 타입이 `Object` 이므로 「값이 없다」를 `null` 로 말한다 → [[autoboxing]] · [[crud]]

## 왜 중요한가

**구현 클래스를 사람이 쓰지 않게 된다.** DAO 셋 × 메서드 다섯 = 열다섯 개의 몸통이 `invoke` 하나가 되고, 열다섯 개가 전부 같은 모양(문장 id 를 만들고 파라미터를 넘기고 결과를 돌려준다)이었기 때문에 가능하다. **같은 모양의 코드가 여러 파일에 반복되는 것과 「그 모양을 코드로 적는 것」이 갈리는 자리**이고, 새 DAO 를 추가할 때 파일이 하나(인터페이스)만 늘어난다 → [[dao-pattern]] · [[refactoring]]

**MyBatis 의 매퍼 인터페이스가 정확히 이 물건이다.** [[mybatis]] 노트가 「매퍼 인터페이스(`@Mapper`)가 그 문자열을 메서드 이름으로 바꿔 잃은 것의 일부를 되찾는 다음 걸음이다」로 남겨 둔 자리를 **Day61 이 손으로 만든다.** `sqlSession.delete("UserDao.delete", no)` 의 문자열 id 가 `userDao.delete(no)` 라는 **메서드 호출**로 바뀌면 오타가 컴파일에서 걸리고, 그 변환을 하는 것이 프록시다 — 「프레임워크가 어떻게 인터페이스만으로 동작하나」의 답이 이 회차에 있다 → [[sql-session]]

**그리고 「모든 호출을 가로채는」 도구가 손에 들어온다.** 트랜잭션 시작·커밋을 `invoke` 앞뒤에 한 번 적으면 모든 DAO 메서드가 그것을 받는다. Spring 의 `@Transactional` 이 이 위에 서 있고, 두 달 뒤의 필기가 「`@EnableTransactionManagement` 를 붙여서 Proxy 클래스를 자동 생성하게 한다」로 그 이름을 다시 만난다 → [[transaction]] · [[proxy-pattern]]

**대가는 타입이 납작해진다는 것이다.** `invoke` 의 시그니처가 `Object invoke(Object, Method, Object[])` 이므로 **컴파일러가 검사할 것이 없다** — 어떤 인수가 오는지도, 무엇을 돌려줘야 하는지도 `Object` 다. 리턴 타입이 안 맞으면 부르는 쪽에서 `ClassCastException` 이 나고, 그 자리는 프록시를 부른 곳이지 실수한 곳이 아니다 → [[type-casting]] · [[exception-handling]]

## 경계와 오해

- **`return new Proxy.newProxyInstance(…)` 는 컴파일되지 않는다 — `new` 뒤에 정적 메서드를 붙일 수 없다** — `newProxyInstance` 는 `Proxy` 의 **정적 메서드**이므로 `Proxy.newProxyInstance(…)` 로 부른다. 그리고 `new` 를 지워도 한 번 더 막힌다 — **반환 타입이 `Object` 라 `T` 로 돌려줄 수 없다.** `return daoType.cast(Proxy.newProxyInstance(…))` 나 `(T)` 캐스팅이 필요하고, 후자는 검사되지 않는 캐스팅 경고가 붙는다. **같은 오류 형태가 [[socket-binding]] 에 이미 있었다** — Day46 의 `new InetAddress.getByName("domainName")` 이고, 23일 뒤 같은 손이 같은 실수를 했다. 그때 적었던 것이 「`new` + 정적 메서드는 **문법 오류**라 이 파일 전체가 컴파일 대상에서 떨어진다」이므로, **이 `DaoFactory` 는 한 줄도 실행되지 않았다** → [[generics]] · [[type-casting]]
- **`this.class` 는 문법이 아니다 — 그리고 같은 노트가 맞는 형태를 갖고 있다** — 첫 코드 블록은 `this.class.getClassLoader()` 이고 `DaoFactory` 블록은 `this.getClass().getClassLoader()` 다. **`.class` 는 타입 이름에만 붙는 리터럴**이므로(`Interface.class` 처럼) 참조 변수에는 못 붙이고, 객체에서 클래스를 얻는 것은 메서드 `getClass()` 다. [[class-metadata]] 가 가르는 두 경로가 여기서 한쪽만 틀린 채 나란히 있다 → [[this-reference]] · [[literal]]
- **`agrs.length ==1{` — 오타와 괄호 누락이 한 줄에 있다** — `args` 의 오기이고 `if (` 의 여는 소괄호가 닫히지 않았다. 오타 쪽은 컴파일러가 「그런 변수 없음」으로 잡아 주지만, 이 줄은 **괄호 때문에 파싱에서 먼저 막힌다** → [[variable-scope]]
- **`params.getAnnotation(Param.class)` 는 배열에 대고 부른 것이다 — 그리고 인덱스가 있는데 안 썼다** — `params` 는 `Parameter[]` 이므로 `getAnnotation` 이 없다(`params[i].getAnnotation(Param.class)` 여야 한다). 루프가 `i` 를 만들어 `args[i]` 에는 쓰면서 `params` 에는 안 쓰는 것이 그 표시다. [[reflective-annotation-access]] 노트가 「읽는 쪽은 클래스만이 아니다 — `Method`·`Field`·`Parameter` 에도 같은 메서드가 있다」고 적어 둔 그 자리인데, **객체를 하나 꺼내는 걸음이 빠졌다** → [[array]]
- **`map.put(anno, args[i])` 는 이 절의 논점을 놓쳤다 — 키가 이름이 아니라 애노테이션 객체다** — `Map<String,Object>` 에 `Param` 을 넣으므로 컴파일도 안 되지만, **뜻으로 틀린 것이 더 크다.** 애노테이션을 만든 이유가 「매개변수 이름을 실행 중에 얻는 것」이고 그 이름은 `anno.value()` — `"no"`·`"count"` — 에 들어 있다. `map.put(anno.value(), args[i])` 라야 매퍼의 `#{no}` 가 값을 찾는다. **한 걸음 앞에서 멈춘 형태**이고, 만약 키가 어떻게든 문자열로 들어갔다면 `@Param(value=no)` 같은 `toString` 이 키가 되어 [[mybatis]] 가 적어 둔 `There is no getter for property named …` 로 온다 → [[hash-based-collection]] · [[reflective-annotation-access]]
- **설명은 「2개」인데 코드는 「1개가 아니면 전부」다 — 이번에는 코드가 맞다** — 필기의 목록이 0개·1개·2개 셋인데 `else` 는 3개 이상도 `Map` 으로 만든다. 매개변수가 셋인 메서드가 생겨도 그대로 도는 형태이므로 **설명이 좁고 코드가 넓다** — 앞의 오류들과 방향이 반대인 자리다.
- **`Object` 의 메서드도 `invoke` 로 온다 — 이 코드에서는 객체를 출력하면 SQL 이 나간다** — 프록시는 `toString()`·`equals()`·`hashCode()` 도 핸들러로 넘긴다. Day61 의 `invoke` 는 그것을 걸러내지 않으므로 결말이 정해진다: `toString()` 은 리턴 타입이 `String` 이라 마지막 `else` 로 가서 **`selectOne` 이 실행되고**, `hashCode()`(`int`)와 `equals()`(`boolean`)는 두 번째 분기로 가서 **`insert` 가 실행된다.** 즉 **디버거로 이 객체를 들여다보거나 `System.out.println(userDao)` 를 한 줄 찍으면 DB 에 쓰기가 나간다.** 컬렉션에 담는 것도(`hashCode`) 같다. 실제 구현에서 `method.getDeclaringClass() == Object.class` 를 먼저 걸러내는 것이 관례인 이유가 이것이고, **이 버그는 기능을 쓸 때가 아니라 로그를 찍을 때 터진다** → [[object-class]] · [[object-equality]] · [[hash-code]] · [[dml]]
- **리턴 타입을 `==` 로 비교하면 `List` 밖에 못 잡는다** — `returnType == List.class` 는 선언이 **정확히 `List`** 일 때만 참이다. `ArrayList<Project> list()` 나 `Collection<Project>` 로 선언한 메서드는 마지막 `else` 로 떨어져 **`selectOne`** 이 되고, 행이 여러 개면 `TooManyResultsException`·하나면 `List` 가 아닌 객체가 `List` 자리에 담겨 `ClassCastException` 이다. 필요한 것은 `List.class.isAssignableFrom(returnType)` 이고, **`==` 로 타입을 비교하는 것과 「이 타입인가」를 묻는 것이 다르다** — [[instanceof-operator]] 가 인스턴스에 대해 하는 일을 `Class` 끼리 하려면 그 메서드다 → [[data-type]]
- **`int`·`void`·`boolean` 을 한 분기에 묶으면 `insert`·`update`·`delete` 가 구별되지 않는다** — 세 문장 모두 「변경된 행 수」를 돌려주므로 **반환 타입만으로는 어느 것인지 알 수 없다.** 그래서 이 코드는 `delete` 를 부르는 자리에서도 `sqlSession.insert(…)` 를 부른다. MyBatis 는 세 메서드를 같은 경로로 처리하므로 대개 동작하지만, **리턴 타입 디스패치의 한계가 정확히 여기서 드러난다** — 문장의 **종류**는 시그니처에 없는 정보이고, 그것을 아는 것은 매퍼 XML 의 태그(`<insert>`/`<delete>`)뿐이다. 축을 하나 더 두려면 메서드 이름을 봐야 하고, 그것이 MyBatis 의 매퍼 인터페이스가 실제로 하는 일이다 → [[dml]] · [[mybatis]]
- **`"sql.method"` 는 자리표시자다 — 그리고 그것이 이 설계의 핵심을 감춘다** — 세 곳에 같은 문자열이 박혀 있으므로 **모든 메서드가 같은 문장 하나를 부르는** 코드다. 실제로는 `method.getDeclaringClass().getName() + "." + method.getName()` 같은 규약이 있어야 하고, **그 규약이 이 도구를 쓰는 값의 절반이다** — 「인터페이스의 메서드 이름 = 매퍼의 문장 id」로 못 박으면 [[mybatis]] 가 지적한 「문장 id 가 문자열이라 컴파일러가 안 본다」가 사라진다. 자리표시자로 남겨 두어 **왜 프록시로 만들면 이득인지가 코드에 안 보인다** → [[refactoring]]
- **`return null` 에 세미콜론이 없다 — 그리고 그 자리는 `void` 분기다** — `void` 메서드에 `null` 을 돌려주는 것은 규칙대로 맞다(`invoke` 가 `Object` 를 돌려주므로 「값 없음」을 그렇게 말한다). 부르는 쪽은 그 값을 볼 수 없다 — 프록시가 만든 메서드의 반환 타입이 `void` 이기 때문이다. 반대로 **반환 타입이 기본형인데 `null` 을 돌려주면 `NullPointerException`** 이고, 박싱을 되돌리는 자리에서 난다 → [[autoboxing]] · [[wrapper-class]]
- **`private Object invoke(…)` 에 `throws Throwable` 이 없다** — 인터페이스의 선언은 `Object invoke(Object, Method, Object[]) throws Throwable` 이다. 더 좁게 던지는 것은 허용되므로 **메서드 레퍼런스로 끼우는 것 자체는 통하지만**, 그 안에서 검사 예외를 던질 수 없다. Day55~59 의 DAO 메서드가 전부 `throws Exception` 이었고 `sqlSession` 도 예외를 던지므로, **몸통을 채우는 순간 이 시그니처가 막힌다** — 시그니처를 좁게 적은 대가가 나중에 온다 → [[exception-handling]] · [[method-reference]]
- **동적 프록시 ≠ 리플렉션 호출 — 방향이 반대다** — 둘 다 `Method` 를 쓰지만 [[reflective-invocation]] 은 **내가 남의 메서드를 이름으로 찾아 부르는** 것이고, 이쪽은 **남이 나를 부른 것을 받는** 것이다. 그래서 Day61 의 `invoke` 안에는 `method.invoke(…)` 가 **없다** — 넘길 안쪽 객체가 없으니 부를 것도 없다. 「`invoke` 라는 이름이 같으니 같은 일」로 읽으면 [[proxy-pattern]] 의 RealSubject 가 어디로 갔는지가 설명되지 않는다.
- **만들어진 객체의 `getClass()` 는 `UserDao` 가 아니다** — `$Proxy0` 같은 이름이 나오고 `instanceof UserDao` 는 참이다. **[[reflective-annotation-access]] 가 「돌려받은 애노테이션 객체는 JVM 이 만든 프록시다」라고 적은 것이 바로 이 클래스다** — `@interface` 가 인터페이스이므로 `getAnnotation` 이 돌려주는 값도 이 도구로 만들어진다. 하루 전 회차에서 「어떻게 `new` 없이 값이 담긴 객체가 오나」로 남았던 것의 답이 이 회차의 문법이다 → [[class-metadata]] · [[interface]]
- **클래스는 못 감싼다 — 그래서 인터페이스가 없으면 이 도구가 아니라 다른 도구를 쓴다** — 두 번째 인수에 클래스를 넣으면 `IllegalArgumentException` 이다. 그래서 인터페이스가 없는 클래스에 프록시를 씌우려면 바이트코드를 만들어 **상속**하는 라이브러리(CGLIB 류)가 필요하고, 그때는 `final` 클래스·`final` 메서드에 막힌다. Spring 이 프록시 방식을 둘 갖고 있는 이유가 이 제약이다 → [[proxy-pattern]] · [[inheritance]] · [[bytecode]]
- **같은 핸들러를 세 DAO 가 공유하면 「내가 어느 DAO 인가」를 `invoke` 가 알아야 한다** — `this::invoke` 는 `DaoFactory` 인스턴스 하나의 메서드이므로 `UserDao`·`BoardDao`·`ProjectDao` 가 **같은 핸들러**를 쓴다. 문장 id 에 네임스페이스를 붙이려면 `method.getDeclaringClass()` 를 물어야 하고, Day61 의 `"sql.method"` 자리표시자가 그 물음을 가리고 있다. **핸들러를 프록시마다 하나씩 만드는 형태**(`createObject` 안에서 람다를 만들어 `daoType` 을 붙잡는 것)가 대안이며, 그러면 각 핸들러가 자기 타입을 안다 → [[variable-scope]]
- **그 공유가 하루 뒤에 한 겹 더 커지고, 그래서 핸들러의 필드가 바뀐다** — Day61 의 핸들러는 세 DAO 만 공유하는 것이 아니라 **서버의 모든 접속이 공유한다**(`appCtx` 에 한 벌). 그 핸들러가 `sqlSession` 을 필드로 들고 있었으므로 접속 수십 개가 세션 하나를 쓰게 되고, Day62 가 그것을 고치는 방법이 **핸들러의 필드를 `SqlSession` 에서 `SqlSessionFactory` 로 바꾸는 것**이다 — `invoke` 가 그때그때 `sqlSessionFactory.openSession(false)` 로 얻으므로 같은 핸들러를 몇 쓰레드가 불러도 각자 자기 세션을 쓴다. **핸들러 하나를 공유해도 되는 조건이 「쓰레드마다 달라야 하는 것을 필드로 들지 않는 것」**이고, 핸들러가 상태를 가지면 그 상태가 **인터페이스의 모든 메서드에 걸친다**는 것이 이 구조의 성질이다 → [[thread]] · [[thread-local]] · [[sql-session]]
- **가로채는 범위가 손으로 쓴 프록시와 반대로 어긋난다** — 이 도구는 `invoke` 하나가 인터페이스의 **모든** 메서드를 받으므로 「어느 메서드를 깜빡 빠뜨렸다」가 구조적으로 불가능한 대신, 위 항목처럼 `toString`·`equals` 까지 받아 버린다. 하루 뒤 Day62 가 손으로 쓴 `SqlSessionFactoryProxy` 는 정확히 반대다 — `openSession(boolean)` 하나만 바꾸고 나머지 여덟 개를 원본에 위임해서, **인수 없는 `openSession()` 으로 들어오면 의도한 동작이 통째로 빠진다.** **만들어 쓰면 너무 많이 받고 손으로 쓰면 너무 적게 받는다** — 어느 쪽이든 「모든 호출이 한 곳을 지난다」는 [[proxy-pattern]] 의 전제가 실제로 지켜지는지 따로 확인해야 한다 → [[method-overriding]] · [[object-class]]
- **`Proxy` 라는 낱말이 세 가지를 가리킨다** — 이 회차 안에서 ① GoF 패턴 이름, ② `java.lang.reflect.Proxy` 클래스, ③ `invoke` 의 첫 인수 `Object proxy`(만들어진 객체 자신)다. 필기의 「proxy : 클라이언트가 메서드를 호출할때 실제 객체처럼 메서드를 호출할 수 있도록 대리 역할을 한다」는 ③ 을 설명하는데 **①·② 의 설명처럼 읽힌다.** 그리고 ③ 은 실무에서 거의 쓰지 않는다 — 그 안에서 자기 다른 메서드를 부르면 **다시 `invoke` 로 들어와** 무한 재귀가 되기 쉬운 인수다.
- **「invoke의 함수가 길기 때문에」로 문장이 끊겨 있다** — 뒷말이 없다. 문맥으로 채우면 「그래서 익명 클래스로 그 자리에 쓰지 않고 별도 메서드로 빼서 메서드 레퍼런스로 넘긴다」다 — 바로 다음 코드 블록이 그 형태이고, 첫 코드 블록의 익명 클래스 판과 대비된다. **끊긴 자리에 들어갈 것이 다음 블록에 이미 있다** → [[anonymous-class]] · [[method-reference]]

## 함께 보는 개념

- [[proxy-pattern]] — 이 도구가 실행 중에 만들어 내는 역할
- [[thread-local]] — 핸들러가 상태를 들지 않게 만드는 하루 뒤의 답
- [[dao-pattern]] — Day61 이 이것으로 구현 클래스를 지운 층
- [[mybatis]] — 매퍼 인터페이스가 이 도구로 만들어진다
- [[reflective-invocation]] — 같은 `Method` 객체를 반대 방향으로 쓰는 쪽
- [[reflective-annotation-access]] — 애노테이션 객체가 이 도구로 만들어진다는 자리
- [[annotation]] · [[annotation-retention]] · [[annotation-target]] — `@Param` 을 만드는 데 필요한 셋
- [[method-reference]] · [[functional-interface]] — `this::invoke` 가 성립하는 근거
- [[class-loading]] · [[class-metadata]] — 첫 인수와 두 번째 인수가 닿는 곳
- [[generics]] — `Class<T>` 하나로 타입과 반환형을 묶는 문법
- [[dispatch-table]] — 이름으로 고르는 사촌
- [[interface]] — 이 도구가 요구하는 유일한 조건
- [[object-class]] · [[object-equality]] · [[hash-code]] — 걸러내지 않으면 함께 가로채지는 것들
- [[declarative-transaction]] — 프레임워크가 같은 일을 자동으로 하는 자리
- [[aop]] — 이 장치에 이름과 문법을 붙인 것
- [[transaction]] — 호출을 가로채 앞뒤에 붙이는 대표적인 일
- [[exception-handling]] — `throws Throwable` 이 있는 이유
- [[type-casting]] — `Object` 로 납작해진 반환값을 되돌리는 자리

## 출처

- [[2025-01-21-Day16]] — **이 장치가 무엇이었는지 이름이 붙는다.** 손으로 만든 프록시(Day61)와 `@Transactional` 의 자동 프록시(Day83)가 하던 일이 **AOP** 라는 이름으로 정리되고, `@Aspect`·`@Around`·포인트컷이라는 문법이 나온다 — 「무엇을 끼울지」(어드바이스)와 「어디에 끼울지」(포인트컷)를 갈라 적는 형태다. 이 회차의 `ResponseAspect` 가 모든 `@RestController` 메서드의 반환값을 가로채 상태 코드를 설정하는데, **프록시가 메서드를 감싼다**는 원리가 그대로 쓰인다 → [[aop]]
- [[2024-09-26-Day83]] — 다섯 주 뒤. **손으로 만든 프록시가 프레임워크의 것으로 대체된다.** 「`AppConfig` 에 `@EnableTransactionManagement` 를 붙여서 **Proxy 클래스를 자동 생성**하게 한다」는 한 줄이 그 이행을 그대로 적었고, 같은 노트의 `getMapper(UserDao.class)` 도 **구현 클래스 없는 인터페이스**에서 객체를 얻는다 — 이 회차에 프록시가 두 군데 쓰이는데 둘 다 「자동」이라 안이 안 보인다. 직접 만들어 본 것이 그 안을 아는 근거가 되는 자리다 → [[declarative-transaction]] · [[mybatis-spring]]
- [[2024-08-22-Day61]] — 「호출하기」(`newProxyInstance`·`InvocationHandler`·「method 값 호출하기, args 호출하기」)와 「Dao객체 만들기」 절들이 이 개념이다. `Proxy.newProxyInstance` 의 세 인수(클래스로더 · 구현할 인터페이스 목록 · 호출 관리자)와 `invoke` 의 세 인수(`proxy`·`method`·`args`)를 각각 한 줄씩 정확히 적고, 그것으로 `UserDao`·`BoardDao`·`ProjectDao` 를 **제네릭 메서드 `<T> T createObject(Class<T> daoType)` 하나로 만드는** 형태를 세웠다. `invoke` 는 축이 둘이다 — 매개변수 개수(0개는 `null`·1개는 `args[0]`·2개 이상은 `Map`)와 리턴 타입(`List`→`selectList`, `int`·`void`·`boolean`→`insert`, 그 밖→`selectOne`)이고, `boolean` 을 `count > 0` 으로 접고 `void` 에 `null` 을 돌려주는 것으로 DAO 다섯 시그니처를 흡수한다. 매퍼의 `#{property}` 가 이름으로 값을 찾는데 `args[n]` 에는 이름이 없다는 문제를 짚고 **`@Retention(RUNTIME)` + `@Target(ElementType.PARAMETER)` 로 `@Param` 을 직접 만들어** `void updateViewCount(@Param("no") int boardNo, @Param("count") int count)` 에 붙였다 — 이 필기에서 애노테이션이 처음 일을 하는 자리이고 두 메타 애노테이션이 함께 쓰인 첫 예다. 다만 **코드는 한 줄도 실행되지 않는다** — `return new Proxy.newProxyInstance(…)` 가 정적 메서드에 `new` 를 붙인 문법 오류이고(반환형도 `Object` 라 `T` 로 못 돌려준다), `this.class.getClassLoader()`·`agrs.length ==1{`·`params.getAnnotation(…)`(배열에 대고 호출)·`map.put(anno, args[i])`(키가 이름이 아니라 애노테이션 객체 — **애노테이션을 만든 이유인 `anno.value()` 를 꺼내지 않았다**)·세미콜론 없는 `return null` 이 이어진다. 문장 id 는 `"sql.method"` 자리표시자로 남아 **메서드 이름이 곧 문장 id 가 되는 규약**이 코드에 없고, `Object` 의 `toString`·`equals`·`hashCode` 를 걸러내지 않아 **객체를 출력하는 것만으로 `selectOne`·`insert` 가 실행되는** 상태다. `returnType == List.class` 의 `==` 비교가 `ArrayList` 선언을 놓치는 것, `insert`·`update`·`delete` 가 반환 타입으로 구별되지 않는 것, 인터페이스만 감쌀 수 있다는 제약, `throws Throwable` 누락도 다루지 않았다. 「invoke의 함수가 길기 때문에」로 문장 하나가 끊겨 있다
- [[2024-08-23-Day62]] — 하루 뒤. 이 도구 자체는 다시 나오지 않지만 **핸들러가 고쳐진다** — 「DaoFactory 클래스 변경」 절이 `SqlSession` 필드를 버리고 생성자로 `SqlSessionFactory` 를 받아 `invoke` 안에서 `sqlSessionFactory.openSession(false)` 로 세션을 얻게 바꾼다. 접속마다 쓰레드가 붙는 서버에서 **핸들러 한 벌을 모든 쓰레드가 공유하므로**, 핸들러가 세션을 필드로 들면 그것이 곧 공유 자원이 된다는 것이 이 변경의 이유다(→ [[thread-local]]). 같은 회차가 `SqlSessionFactory` 에는 **손으로 쓴** 프록시를 세우는데, 그쪽은 오버로드 여덟 개 중 하나만 가로채서 이 도구와 **가로채는 범위가 반대로 어긋난다** — 이 노트의 「`Object` 의 메서드도 `invoke` 로 온다」와 짝이 되는 자리다 → [[proxy-pattern]]
