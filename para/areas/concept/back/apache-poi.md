---
type: concept
id: apache-poi
title: Apache POI (XSSF · HSSF)
aliases:
  - Apache POI
  - POI
  - poi-ooxml
  - XSSF
  - HSSF
  - XSSFWorkbook
  - 엑셀 라이브러리
  - 엑셀 입출력
up:
  - 2024-07-24-Day42
tags:
  - java
  - 입출력
  - 라이브러리
  - 엑셀
---

# Apache POI (XSSF · HSSF)

**엑셀 파일을 바이트가 아니라 「워크북 → 시트 → 행 → 셀」이라는 객체로 열게 해 주는 Java 라이브러리.** Day42 의 한 줄이 범위를 정확히 적었다 — 「Microsoft Excel (.xlsx) 파일을 생성, 수정, 읽기 및 쓰기에 사용되는 Java API」. 이름이 세 개로 갈리는데 층이 다르다 — **라이브러리가 POI**, `.xlsx` 를 다루는 구현이 **XSSF**, `.xls` 쪽이 **HSSF** 다.

## 정의

Day42 가 「주요클래스」로 넷을 세운 것이 그대로 엑셀 화면의 구조다.

| 클래스 | 엑셀에서 보이는 것 | 얻는 방법 |
|---|---|---|
| `XSSFWorkbook` | 파일 하나 | `new XSSFWorkbook()` · `new XSSFWorkbook("data.xlsx")` |
| `XSSFSheet` | 아래쪽 시트 탭 하나 | `workbook.getSheet(이름)` · `createSheet(이름)` |
| `XSSFRow` | 행 하나 | `sheet.getRow(n)` · `createRow(n)` |
| `XSSFCell` | 셀 하나 | `row.getCell(n)` · `createCell(n)` |

**포함 관계가 곧 호출 순서다.** 셀에 닿으려면 워크북 → 시트 → 행을 차례로 지나야 하고, `(3, 5)` 좌표로 한 번에 가는 API 가 없다. 그래서 Day42 의 절차 목록이 다섯 단계·여섯 단계로 늘어선 것이 라이브러리 사정이 아니라 **파일 형식의 구조**다.

### `get` 과 `create` 가 층마다 짝으로 있다

세 층 전부에 같은 짝이 있다 — `getSheet`/`createSheet` · `getRow`/`createRow` · `getCell`/`createCell`.

| | 하는 일 | 없을 때 |
|---|---|---|
| `get…` | 이미 있는 것을 찾는다 | **`null`** (시트는 `null`, 행·셀도 `null`) |
| `create…` | 새로 만든다 | — (있으면 **덮어쓴다**) |

**읽는 쪽과 쓰는 쪽이 이 짝으로 갈린다** — 새 파일을 만드는 경로는 `create` 만 쓰고, 기존 파일을 읽는 경로는 `get` 만 쓴다. Day42 는 §3 에서 이 짝을 정확히 정리해 놓고 §4 의 절차에서 그것을 섞는데, 그 결과가 아래 「경계와 오해」의 `NullPointerException` 이다.

## 사용 예시

Day42 가 세운 절차는 여섯 단계다 — 「WorkBook을 만든다 → Sheet를 만든다 → Row를 선택한다 → Cell을 선택한다 → Cell값에 SetValue를 한다 → 파일을 내보낸다」. 실제로 도는 코드로 옮기면 3·4단계가 `create` 로 바뀌고, 마지막 단계에 필기에 없던 두 줄이 붙는다.

```java
try (XSSFWorkbook workbook = new XSSFWorkbook()) {   // 1. 워크북
  XSSFSheet sheet = workbook.createSheet("회원");      // 2. 시트
  XSSFRow row = sheet.createRow(0);                  // 3. 행 — get 이 아니다
  row.createCell(0).setCellValue("이름");             // 4~5. 셀 + 값
  row.createCell(1).setCellValue(27);

  try (FileOutputStream out = new FileOutputStream("data.xlsx")) {
    workbook.write(out);                             // 6. 여기서야 파일이 생긴다
  }
}
```

읽는 쪽은 「파일명을 가진 WorkBook을 만든다 → Sheet를 선택한다 → …」 순으로, 이쪽은 필기의 「선택」이 맞다.

```java
try (XSSFWorkbook workbook = new XSSFWorkbook("data.xlsx")) {
  XSSFSheet sheet = workbook.getSheet("회원");
  XSSFRow row = sheet.getRow(0);
  String name = row.getCell(0).getStringCellValue();
  int age = (int) row.getCell(1).getNumericCellValue();   // double 로 나온다
}
```

**Day42 의 `saveData()` 는 몸통이 비어 있다.** 「실습프로젝트에 적용하기」에서 CSV·JSON 대신 엑셀로 저장하려던 자리이고, 형식만 바뀌었을 뿐 하는 일은 앞 회차들과 같다 → [[csv]] · [[json]] · [[serialization]]

라이브러리를 쓸 수 있게 만드는 것은 좌표 한 줄이다 — Day42 가 `mvnrepository` 에서 찾아 온 것이 `org.apache.poi:poi-ooxml` 이다 → [[gradle]]

## 왜 중요한가

**파일 형식을 몰라도 데이터를 다룰 수 있다.** `.xlsx` 는 XML 파일 여러 개를 담은 ZIP 이고 `.xls` 는 단일 바이너리 형식이다. 직접 읽으려면 두 형식의 명세를 구현해야 하는데, POI 를 쓰면 **보이는 것이 「셀에 무엇이 들었나」뿐**이다. Day38~41 이 스트림으로 바이트를 한 겹씩 벗겨 온 것과 층이 다르고, 「라이브러리를 들인다」가 무엇을 사는 일인지가 여기서 가장 분명하다 → [[binary-io]] · [[io-stream]]

**주고받는 상대가 사람이면 형식이 정해져 버린다.** CSV·JSON 은 프로그램끼리 주고받기 좋지만, 업무에서 「파일로 주세요」는 대개 엑셀이다. 실습 프로젝트의 저장 형식이 Day39 CSV → Day40 JSON → Day42 엑셀로 옮겨 온 것이 그 순서고, **읽는 쪽이 코드에서 사람으로 바뀌면 선택지가 줄어든다.**

**셀 하나가 값 + 타입 + 서식이라 CSV 로 못 담는 것을 담는다.** 시트가 여러 개인 것, 숫자와 문자를 구별하는 것, 날짜에 표시 형식이 붙는 것이 전부 형식 안에 있다. 대가는 파일이 사람이 읽을 수 없게 되는 것이고 — CSV 는 `cat` 으로 열리지만 `.xlsx` 는 열리지 않는다 — **그 대가를 지불하고 사는 것이 구조와 타입**이다 → [[csv]] · [[data-type]]

## 경계와 오해

- **POI ≠ `poi` — 아티팩트를 잘못 고르면 `XSSFWorkbook` 이 안 잡힌다** — `org.apache.poi:poi` 는 HSSF(`.xls`)까지고, `.xlsx` 를 다루려면 **`poi-ooxml`** 이어야 한다(이것이 `poi` 를 다시 끌어온다). 필기가 「apachi-poi를 검색하여」로 적고 링크한 좌표가 `org.apache.poi:poi-ooxml` 인 것이 그 이유이며, **검색어와 좌표가 다른 자리**다. 라이브러리 이름으로 검색해서 나온 첫 결과를 넣는 습관이 여기서 처음 걸린다 → [[gradle]]
- **`.xls` 는 「2007 이하」가 아니라 2003 이하다** — Excel 2007 이 이미 `.xlsx`(Office Open XML)를 기본으로 쓰기 시작했으므로 한 세대 어긋난 표기다. 그리고 실제로 갈리는 기준은 **버전이 아니라 확장자**다 — 파일이 `.xls` 면 HSSF, `.xlsx` 면 XSSF 이고, 둘을 다 받아야 하는 프로그램은 `WorkbookFactory.create(file)` 로 판단을 라이브러리에 넘긴다. 「엑셀 버전」으로 외우면 옛 파일을 받은 날 어느 클래스를 쓸지 결정하지 못한다.
- **`getValue`·`SetValue` 라는 메서드는 없다 — 그리고 없는 이유가 셀에 타입이 있기 때문이다** — 쓰는 쪽은 `setCellValue(...)` 하나가 오버로딩으로 문자열·숫자·불린·날짜를 받는데, **읽는 쪽은 하나로 합칠 수 없다** — `getStringCellValue()`·`getNumericCellValue()`·`getBooleanCellValue()` 로 갈라져 있고, 숫자 셀에 문자 getter 를 쓰면 `IllegalStateException` 이다. 「Cell값에 getValue를 한다」로 절차를 외우면 **바로 그 한 단계에서 멈춘다** — 읽기 전에 `getCell(i).getCellType()` 을 봐야 하고, 그것이 CSV 를 읽을 때는 없던 일이다(CSV 는 전부 문자열이고 타입은 내가 붙였다) → [[data-type]] · [[number-parsing]]
- **엑셀에는 정수 타입이 없다 — 숫자는 전부 `double` 이다** — `getNumericCellValue()` 의 반환형이 `double` 인 것은 POI 의 취향이 아니라 **파일 형식이 그렇다.** 나이 `27` 을 넣고 읽으면 `27.0` 이고 `(int)` 로 되돌리는 것은 내 코드의 일이다. 날짜도 숫자다 — 1900년 기준의 일수에 표시 형식이 붙은 것이라, 서식을 잃으면 `45000` 같은 값이 남는다. **「셀에 27을 넣었다」와 「27이라는 정수가 저장됐다」가 다른 자리** → [[floating-point]] · [[type-casting]] · [[date-time]]
- **「Row를 선택한다」로는 새 파일을 못 만든다 — 필기의 6단계가 여기서 어긋난다** — 「만들고 저장하기」의 3·4단계가 「Row를 **선택**한다」·「Cell을 **선택**한다」인데, 방금 `createSheet` 한 시트에는 행이 하나도 없으므로 `getRow(0)` 은 **`null`** 을 준다. 다음 단계인 「Cell값에 SetValue」에서 `NullPointerException` 이 나고 **파일은 만들어지지 않는다.** 필기가 §3 에서 `get`/`create` 를 짝으로 정리해 두고도 §4 의 절차에서 「선택」으로 뭉갠 결과이며, 「불러오기」쪽 절차는 같은 낱말이 맞다 — **두 절차가 다섯 단계까지 똑같이 생겨서 낱말 하나 차이가 안 보이는 것**이 이 실수의 조건이다 → [[default-initialization]] · [[exception-handling]]
- **`getRow`·`getCell` 의 `null` 과 「빈 셀」은 다른 것이다** — 한 번도 값을 넣지 않은 셀은 파일에 아예 없어서 `getCell(3)` 이 `null` 이고, 값을 넣었다 지운 셀은 존재하며 타입이 `BLANK` 다. **「비어 있다」가 두 가지**라서, 열이 들쭉날쭉한 표를 읽는 코드는 `null` 검사 없이 한 바퀴도 못 돈다. `row.getCell(i, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)` 가 둘을 하나로 눌러 주는 장치이고, **이 구분이 있는 이유는 엑셀 파일이 안 쓴 셀을 저장하지 않기 때문**이다(그래서 100만 행짜리 시트가 몇 KB 일 수 있다).
- **`createRow` 는 「없으면 만든다」가 아니다** — 이미 행이 있는 자리에 `createRow(0)` 을 부르면 **그 행이 지워지고 새 빈 행으로 바뀐다.** 기존 파일을 열어 한 칸만 고치려고 `createRow` 를 쓰면 그 행의 나머지 셀이 예외 없이 사라지고, 저장한 뒤에야 드러난다. 고치는 경로는 `getRow` 로 받아 `null` 일 때만 `createRow` 하는 것이고 — **이름이 `getOrCreate` 가 아니라는 것을 확인해야 하는 자리**다. 「만들기」와 「수정하기」가 같은 메서드로 되지 않는 것이 `get`/`create` 짝의 값이자 함정이다 → [[read-side-effect]]
- **워크북을 만든 것과 파일이 생긴 것은 다르다** — `new XSSFWorkbook()` 은 메모리 안의 객체일 뿐이고, 디스크에 파일이 나타나는 것은 `workbook.write(out)` 한 줄뿐이다. 필기의 6단계 「파일을 내보낸다」가 그것인데 코드가 없고 `saveData()` 도 비어 있다. **`write` 를 빼면 예외도 없이 아무 일도 일어나지 않는다** — 셀을 다 채우고 프로그램이 정상 종료하는데 파일이 없는 모양이라, 버퍼 스트림에서 `flush` 를 잊는 것과 증상이 같다 → [[buffered-stream]] · [[try-with-resources]]
- **`new XSSFWorkbook("data.xlsx")` 는 그 파일을 잡고 있다** — 필기의 설명(「해당 파일의 내용을 메모리에 로드한다」)대로 읽어 들이지만 파일 핸들과 임시 자원이 남으므로 `close()` 가 필요하다. 그래서 **읽어서 고쳐 같은 경로로 저장하는 왕복이 순서에 민감하다** — 읽은 워크북을 닫기 전에 그 파일을 열어 쓰면 원본을 깎아 놓고 쓰게 되는 경우가 있다. `Workbook` 이 `Closeable` 인 것이 그 표시다 → [[try-with-resources]]
- **XSSF 는 문서 전체를 메모리에 올린다 — 그래서 행 수에 상한이 생긴다** — 「메모리에 로드한다」의 대가다. 수십만 행을 만들면 `OutOfMemoryError` 이고, 그때 쓰는 것이 **쓰기 전용 스트리밍 구현 `SXSSFWorkbook`**(최근 몇 행만 메모리에 두고 나머지는 임시 파일로 흘린다)이다. **Day41 이 「한 번에 얼마나 들고 있나」로 배운 축이 여기서는 클래스 선택으로 올라온다** — 시트 상한 자체도 형식마다 달라 `.xls` 는 65,536행, `.xlsx` 는 1,048,576행이다 → [[buffered-stream]]
- **`Row`·`Cell` 로 받은 것은 오타가 아니라 더 나은 쪽이다** — 필기가 §3 에서 `XSSFSheet`(과 오타 `XSSFSHeet`)를 쓰다가 행·열에서는 `Row row = sheet.getRow(...)`·`Cell cell = row.getCell(...)` 로 적었다. 이쪽은 `org.apache.poi.ss.usermodel` 의 **인터페이스**이고, 그 타입으로 받아 두면 같은 코드가 HSSF(`.xls`)에도 그대로 돈다. **구현 클래스로 받으면 형식에 묶이고 인터페이스로 받으면 안 묶인다** — 표기가 섞인 것이 우연이지만 고를 이유는 분명하다 → [[interface]] · [[polymorphism]]
- **`Row row = sheet.getRow(int a);` 는 코드가 아니라 서명 표기다** — 인수 자리에 `int a` 를 적으면 컴파일되지 않는다. 필기 §3 전체가 「어떤 메서드가 있나」를 적은 표라서 그대로 붙여 쓸 수 없고, 그 자리에 들어갈 것은 **0부터 시작하는 인덱스**다 — 엑셀 화면의 행 번호는 1부터인데 `getRow(0)` 이 첫 행이므로 **화면과 코드가 한 칸 어긋난다** → [[one-based-numbering]]

## 함께 보는 개념

- [[csv]] — 같은 「표를 파일로」인데 타입과 서식이 없는 쪽
- [[json]] — 실습 프로젝트가 이 형식 바로 전에 쓰던 저장 형식
- [[serialization]] — 객체를 파일로 내보내는 일 전체
- [[binary-io]] — POI 가 대신 처리해 주는 아래층
- [[io-stream]] — `workbook.write(out)` 이 붙는 자리
- [[gradle]] — 좌표 한 줄로 이 라이브러리를 들이는 방법
- [[data-type]] — 셀에 타입이 있어서 getter 가 갈리는 이유
- [[floating-point]] — 엑셀의 모든 숫자가 이것인 이유
- [[date-time]] — 날짜가 숫자 + 서식으로 저장되는 쪽
- [[one-based-numbering]] — 화면의 행 번호와 인덱스가 어긋나는 자리
- [[try-with-resources]] — 워크북과 출력 스트림을 닫는 자리
- [[buffered-stream]] — 「한 번에 얼마나 들고 있나」가 같은 문제인 곳
- [[interface]] — `Row`·`Cell` 로 받으면 형식에 묶이지 않는 이유

## 출처

- [[2024-07-24-Day42]] — 「Microsoft Excel (.xlsx) 파일을 생성, 수정, 읽기 및 쓰기에 사용되는 Java API」로 범위를 적고 `XSSFWorkbook`·`XSSFSheet`·`XSSFRow`·`XSSFCell` 네 클래스와 `getSheet`/`createSheet`·`getRow`/`createRow`·`getCell`/`createCell` 세 짝을 정리했다. `mvnrepository` 에서 `org.apache.poi:poi-ooxml` 좌표를 찾아 `build.gradle` 에 넣고 IDE 설정을 새로 고치는 절차까지 적었다. 다만 「2007이하버전(.xls)은 HSSF」는 한 세대 어긋난 표기이고, 「만들고 저장하기」 절차의 3·4단계가 `create` 여야 하는데 「선택한다」로 적혀 **그대로 따르면 `getRow(0)` 이 `null` 이라 저장에 이르지 못한다.** 「Cell값에 SetValue/getValue」는 존재하지 않는 이름이며 실제로는 `setCellValue` 와 타입별 getter 로 갈린다. 「파일을 내보낸다」에 해당하는 `workbook.write(...)` 코드는 없고, 실습 프로젝트에 적용하는 `saveData()` 는 몸통이 빈 채로 남았다
