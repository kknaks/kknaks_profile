---
type: concept
id: sql-date-function
title: MySQL 의 날짜 함수와 날짜 리터럴
aliases:
  - SQL 날짜 함수
  - mysql 날짜 함수
  - date_format
  - str_to_date
  - datediff
  - date_add
  - now()
  - curdate
tags:
  - database
  - SQL
  - MySQL
  - 시간
up:
  - 2024-08-07-Day52
---

# MySQL 의 날짜 함수와 날짜 리터럴

**날짜를 서버 쪽에서 읽고·꺼내고·옮기고·재고·모양을 바꾸는 함수들, 그리고 날짜로 인정되는 문자열의 형태.** Day52 의 「날짜 다루기」 절이 이것이고, 자바에서 `java.util.Date` 로 배운 **「저장은 하나, 표시는 여럿」이라는 구분이 서버 쪽에도 그대로 있다** → [[date-time]]

## 정의

함수는 하는 일에 따라 다섯 무리다.

| 무리 | 함수 | Day52 가 적은 것 |
|---|---|---|
| 지금을 읽는다 | `now()` · `curdate()` · `curtime()` | 「현재 날짜 및 시간」·「현재 날짜」·「현재 시간」 |
| 일부를 꺼낸다 | `date(값)` · `time(값)` | 「날짜만 뽑거나 시간만 뽑기」 |
| 옮긴다 | `date_add(값, interval n 단위)` · `date_sub(...)` | 「시,분,초,일,월,년을 추가하거나 빼기」 |
| 잰다 | `datediff(날짜1, 날짜2)` | 「두 날짜 사이의 간격」 |
| 모양을 바꾼다 | `date_format(값, 형식)` · `str_to_date(문자열, 형식)` | 「특정 형식으로 값을 추출」·「문자열을 날짜 값으로」 |

**마지막 무리가 서로 반대 방향**이다 — `date_format` 은 날짜 → 문자열, `str_to_date` 는 문자열 → 날짜다. 그 사이에 **저장 형식은 하나로 고정**되어 있다: Day52 의 마지막 줄이 「날짜 값을 저장할 때 기본 형식은 yyyy-MM-dd이다」다.

### 형식 문자

Day52 의 `date_format` 예제에 나온 것들이다. **월과 분이 헷갈리는 자리**라 함께 세워 둔다.

| 문자 | 뜻 | 예 |
|---|---|---|
| `%Y` / `%y` | 연 4자리 / **2자리** | `2022` / `22` |
| `%m` / `%e` / `%d` | **월**(2자리) / 일(공백 없이) / 일(2자리) | `09` / `7` / `07` |
| `%M` / `%b` | 월 이름 / 줄인 월 이름 | `September` / `Sep` |
| `%W` / `%a` / `%w` | 요일 이름 / 줄인 요일 / 요일 번호(일=0) | `Thursday` / `Thu` / `4` |
| `%H` / `%h` / `%l` / `%p` | 24시간 / 12시간(2자리) / 12시간 / AM·PM | `13` / `01` / `1` / `PM` |
| **`%i`** / `%s` | **분** / 초 | `05` / `45` |

**분이 `%i` 다.** `%m` 은 월이고 `%M` 은 월 이름이라, 자바에서 익힌 「소문자가 분」이라는 감각이 여기서는 통하지 않는다(아래 「경계와 오해」).

## 사용 예시

Day52 는 조건에 날짜를 넣는 것부터 시작한다.

```sql
select * from 테이블명 where 날짜컬럼 = 'yyyy-mm-dd';

select * from test1 where regdt between '2022-11-1' and '2022-12-31';
select * from test1 where regdt >= '2022-11-1' and regdt <= '2022-12-31';
```

**두 줄이 같은 뜻으로 나란히 적혀 있는 것**이 `between` 이 양끝을 포함한다는 것을 보여 준다 → [[sql-operator]]

그다음 함수들을 `from` 없는 조회로 확인한다.

```sql
/* 현재 날짜 및 시간 알아내기 */
select now();

/* 현재 날짜 알아내기 */
select curdate();

/* 현재 시간 알아내기 */
select curtime();
```

```sql
select 날짜컬럼, date(날짜컬럼), time(날짜컬럼) from 테이블명;

date_add(날짜데이터, interval 값 년/월/일/시간/분/초);
date_sub(날짜데이터, interval 값 년/월/일/시간/분/초);

select datediff(curdate(), 'yyyy-mm-dd');
```

형식 변환은 예제마다 결과를 주석으로 남겼다.

```sql
select regdt, date_format(regdt, '%m/%e/%Y') from test1; /* 09/7/2022 */
select regdt, date_format(regdt, '%M/%d/%y') from test1; /* September/07/17 */
select regdt, date_format(regdt, '%W %w %a') from test1; /* Thursday 4 Thu */
select regdt, date_format(regdt, '%M %b') from test1; /* September Sep */
select now(), date_format(now(), '%p %h %H %l'); /* PM 01 13 1 */
select now(), date_format(now(), '%i %s'); /* 05 45 */
```

```sql
select str_to_date('11/22/2022', '%m/%d/%Y');
select str_to_date('2022.2.12', '%Y.%m.%d');
```

그리고 **리터럴 형식이 저장을 막는 것**을 세 `insert` 로 확인한다 — 이 절의 결론이다.

```sql
insert into test1 (title, regdt) values('aaaa', '2022-11-22');

  /* 다음 형식의 문자열을 날짜 값으로 지정할 수 없다.*/
insert into test1 (title, regdt) values('bbbb', '11/22/2022');

/* 특정 형식으로 입력된 날짜를 date 타입의 컬럼 값으로 변환하면 입력할 수 있다.*/
insert into test1 (title, regdt) values('bbbb', str_to_date('11/22/2022', '%m/%d/%Y'));
```

**같은 날짜를 세 번 넣는데 가운데만 거절된다.** 「날짜를 넣는다」가 아니라 **「날짜로 인정되는 표기로 넣는다」**가 규칙이라는 것이 이 세 줄에 다 들어 있다 → [[dml]]

## 왜 중요한가

**날짜 계산을 애플리케이션으로 가져오지 않아도 된다.** 자바 쪽에서는 「하루 더하기」·「그 주 첫째날 구하기」가 `java.util.Date` 만으로는 안 되어 막혔던 자리가 있었다(Day30). `date_add`·`datediff`·`%w` 가 그 일을 문장 안에서 하고, **자리내림(월말·연말)도 서버가 처리한다** → [[date-time]]

**입력 검증이 서버로 옮겨 온다.** `'11/22/2022'` 가 거절되므로 「날짜처럼 생긴 문자열」이 날짜 컬럼에 들어가지 못한다. 자바에서 `String startDate` 로 받으면 `"어제"` 도 들어갔던 것과 갈리고, **형식을 아는 쪽(입력 담당)이 `str_to_date` 로 변환할 책임을 진다** → [[sql-data-type]] · [[number-parsing]]

**대신 함수를 어디에 쓰는지가 성능을 가른다.** `select` 목록에서 쓰는 `date_format` 은 표시 형식일 뿐이지만, **`where` 에서 컬럼을 감싸면 인덱스를 쓸 수 없다.** 같은 함수가 놓이는 자리에 따라 무해하거나 전체 스캔을 만든다 → [[database-index]]

## 경계와 오해

- **분이 `%i` 다 — 자바의 「소문자 = 분」 감각이 여기서 깨진다** — `SimpleDateFormat` 은 월이 `MM`, 분이 `mm` 이라 **대소문자로** 갈렸는데, MySQL 은 월이 `%m`, 분이 **`%i`** 로 **글자 자체가 다르다.** 그래서 두 방향의 실수가 성격이 다르다: 자바에서 `"yyyy-mm-dd"` 라고 적으면 월 자리에 분이 들어가 **값이 조용히 망가지지만**(Day40 에서 실제로 그랬다), MySQL 에서 `'%Y-%m-%d'` 라고 적으면 **의도대로 동작한다.** 두 형식 언어를 오갈 때 위험한 방향은 SQL → 자바 쪽이다 → [[date-time]] · [[format-string]]
- **필기의 형식 예제 주석 셋은 같은 행에서 나온 것이 아니다** — `%m/%e/%Y` → `09/7/2022` 는 **2022-09-07** 의 출력이지만, `%y` 는 두 자리 연도이므로 2022 라면 `22` 여야 하는데 주석은 `17` 이고, 2022-09-07 은 **수요일**인데 주석은 `Thursday 4` 다. 「Thursday 4」와 「17」이 함께 맞는 날짜는 **2017-09-07**(목요일)이다. 즉 `test1` 에 행이 여럿 있고 `select ... from test1` 의 결과 중 **주석마다 다른 행을 옮겨 적은 것**이다. 한 행의 결과로 읽으면 `%y` 나 `%W` 가 고장난 것처럼 보이는데, **형식 문자는 정확하고 행이 다르다.**
- **`datediff(a, b)` 는 `a - b` 이고 순서가 부호를 정한다** — 필기는 `datediff(날짜1, 날짜2)` 로만 적었다. 「간격」이라는 말 때문에 절대값으로 읽기 쉽지만 뒤집으면 음수가 나온다. 그리고 **날짜 차이만 세고 시각은 버린다** — 23:59 와 다음 날 00:01 은 2분 차이인데 `datediff` 는 `1` 이다. 「하루가 지났는가」와 「24시간이 지났는가」가 다른 질문이라는 것이 여기서 갈린다 → [[date-time]]
- **`str_to_date` 가 실패하면 예외가 아니라 `NULL` 이다** — 형식이 맞지 않으면 경고와 함께 `NULL` 을 돌려주고, 그 값이 그대로 `insert` 되면(컬럼이 nullable 이면) **잘못된 입력이 조용히 빈 값으로 저장된다.** 자바의 `SimpleDateFormat.parse` 가 `ParseException` 을 던져 흐름을 끊던 것과 정반대다 — 실패가 값으로 돌아오므로 검사하지 않으면 드러나지 않는다 → [[sql-null]] · [[exception-handling]]
- **「지정할 수 없다」도 서버 설정에 딸려 있다** — `values('bbbb', '11/22/2022')` 가 오류인 것은 MySQL 이 **엄격 모드**일 때다. 엄격 모드가 아니면 경고만 내고 `0000-00-00` 을 넣는다. Day51 의 `not null` 실험에서 「오류!」로 적은 것이 같은 설정에 걸려 있었던 것과 같은 축이고, **「제약이 막아 준다」가 서버 설정 하나에 얹혀 있는 자리**다 → [[sql-null]]
- **`between` 을 날짜에 쓰면 끝 경계가 자정이다** — 필기의 `between '2022-11-1' and '2022-12-31'` 은 컬럼이 `datetime` 이면 **2022-12-31 00:00:00 까지만** 잡아 그날 낮의 데이터가 빠진다. `date` 컬럼이면 문제가 없어서, **같은 문장이 컬럼 타입에 따라 맞기도 하고 틀리기도 한다.** 안전한 형태는 `>= '2022-11-01' and < '2023-01-01'` 다 → [[sql-operator]] · [[sql-data-type]]
- **`interval` 로 월을 더하면 자리내림이 일어난다** — `date_add('2022-01-31', interval 1 month)` 는 2022-02-31 이 없으므로 **2022-02-28** 이다. 그래서 「한 달 더하기」를 두 번 한 결과와 「두 달 더하기」의 결과가 다를 수 있다. 자바 쪽에서 「날짜를 필드 뺄셈으로 옮기면 월 경계에서 깨진다」고 남긴 것과 같은 문제이고, **서버 함수를 쓰면 깨지지는 않지만 규칙을 알아야 한다** → [[date-time]]
- **`now()` 와 `sysdate()` 는 다르다** — `now()` 는 **문장이 시작한 시각으로 고정**되어 한 문장 안에서 몇 번 써도 같은 값이고, `sysdate()` 는 호출 시점마다 다시 읽는다. 「등록 시각과 수정 시각을 같은 문장에서 넣었는데 1초 차이가 난다」가 `sysdate()` 쪽에서 생기는 일이다.
- **`curdate()` 의 「오늘」은 서버가 정한다** — 서버·세션의 `time_zone` 설정에 따라 자정의 위치가 달라져서, **자바 쪽에서 만든 시각과 DB 의 `now()` 가 어긋날 수 있다.** `datetime` 타입 자체가 시간대를 담지 않기 때문에 값만 봐서는 드러나지 않는다 → [[sql-data-type]] · [[platform-dependency]]
- **`date_add` 는 컬럼을 바꾸지 않는다** — 새 값을 **돌려주는** 함수이므로 저장된 날짜를 실제로 옮기려면 `update ... set 컬럼 = date_add(컬럼, interval 1 day)` 처럼 써야 한다. `select` 로 확인한 결과가 테이블에 남아 있다고 읽으면 다음 조회에서 원래 값을 보게 된다 → [[dml]]
- **`where date_format(regdt, '%Y') = '2022'` 는 인덱스를 못 쓴다** — 컬럼을 함수로 감싸면 정렬된 값이 아니라 계산 결과를 비교하므로 전체를 훑는다. 「연도로 조회」는 범위 조건(`>= '2022-01-01' and < '2023-01-01'`)으로 적어야 한다. **표시에 쓰는 함수와 조건에 쓰는 함수를 가르는 것**이 이 절에서 얻어야 하는 실무 규칙이다 → [[database-index]]

## 함께 보는 개념

- [[date-time]] — 같은 문제를 자바 쪽에서 다룬 노트(저장과 표시의 분리)
- [[sql-data-type]] — `date`·`time`·`datetime` 이 담는 것
- [[sql-operator]] — `between` 과 날짜 비교
- [[dml]] — 날짜 리터럴이 `insert` 에서 걸러지는 자리
- [[dql]] — `from` 없는 `select now()` 의 형태
- [[sql-null]] — 변환 실패가 값으로 돌아오는 자리
- [[database-index]] — 함수를 `where` 에 쓰면 잃는 것
- [[format-string]] — 형식 언어가 여럿이라는 문제
- [[platform-dependency]] — 서버의 시간대가 결과를 바꾸는 축
- [[exception-handling]] — 실패를 예외로 받던 자바 쪽과의 대비

## 출처

- [[2024-08-07-Day52]] — 「날짜 다루기」 절에서 날짜 조건(`= 'yyyy-mm-dd'`·`between`·`>=/<=`), `now()`·`curdate()`·`curtime()`, `date()`·`time()` 추출, `date_add`·`date_sub`(`interval`), `datediff`, `date_format` 여섯 예제, `str_to_date` 두 예제를 정리하고 **「날짜 값을 저장할 때 기본 형식은 yyyy-MM-dd」**를 세 `insert` 로 확인했다(`'11/22/2022'` 는 거절되고 `str_to_date` 로 감싸면 들어간다). `date_format` 예제의 결과 주석 셋은 서로 다른 행(2022-09-07 과 2017-09-07)에서 옮겨 적혀 있고, 인덱스·시간대·`str_to_date` 실패 시의 동작은 다루지 않았다
