---
concept:
- .docx, .xlsx, .pptx 등 X 확장자 파일은 사실 ZIP 압축 파일이며, 확장자를 .zip으로 바꾼 후 압축을 해제하면 내부의 XML
  파일과 폴더 구조를 볼 수 있다.
- XML은 데이터를 계층적으로 구조화해 저장하는 마크업 언어로, HTML과 유사하지만 미리 정해진 태그가 아닌 사용자가 정의한 태그를 사용한다.
- 워드 파일은 document.xml에 글 내용, styles.xml에 스타일과 폰트, media 폴더에 이미지를 저장하므로 코드로 각 부분을 독립적으로
  조작할 수 있다.
- 엑셀은 중복되는 텍스트를 sharedStrings.xml에 한 번만 저장한 후 시트에서 인덱스로 참조해 파일 크기를 크게 줄이는 압축 기법을 사용한다.
- Office 파일의 구조를 이해하면 코드로 문서 일괄 처리, 이미지 추출, 파일 용량 축소, 간단한 암호 해제, 형식 변환 등을 자동화하고 보안을
  강화할 수 있다.
date: 2026-05-14
day: Day 12
duration: '5:02'
enriched_at: '2026-05-14T15:15:11+09:00'
id: C-012
kind: study
speaker: 코딩애플
status: published
summary:
  en: Office files are ZIP archives containing XML data, enabling code-based document
    automation and manipulation.
  ko: .docx, .xlsx, .pptx는 ZIP 파일이고 XML로 저장돼 있어, 코드로 문서를 자동 처리하고 조작할 수 있다.
tags:
- '#office'
- '#xml'
- '#automation'
- '#python'
- '#fileformat'
title:
  en: 'DOCX is ZIP: Understanding Office File Structure and Automation'
  ko: 'DOCX는 ZIP: Office 파일의 내부 구조와 활용'
transcript: true
type: content
youtubeId: ss3rNBhuIhw
---

## 개요

MS Office와 한글, LibreOffice 등의 최신 문서 파일들(.docx, .xlsx, .pptx, .hwpx 등)의 확장자에 붙는 "X"는 무엇을 의미할까요? 이 글을 읽으면 이들 파일의 실체를 알게 되어, 코드를 이용해 문서를 자동으로 처리하고, 손상된 파일을 복구하며, 파일 크기를 줄이고, 심지어 간단한 암호를 해제할 수도 있습니다. 또한 AI와 함께 대량의 문서를 자동화해 처리할 수 있게 되어 업무 효율을 크게 높일 수 있습니다.

## 배경 / 사전 지식

**확장자와 파일 형식의 관계**

파일의 확장자(예: .txt, .jpg, .pdf)는 파일이 어떤 형식으로 저장되었는지를 나타냅니다. 같은 확장자 파일들은 내부적으로 동일한 구조를 가집니다.

**ZIP 압축 파일**

ZIP은 여러 파일과 폴더를 하나의 파일로 압축하는 표준 형식입니다. Windows와 macOS 모두에서 별도의 프로그램 없이 압축 해제가 가능합니다.

**XML 마크업 언어**

XML(eXtensible Markup Language)은 데이터를 계층적으로 정의하고 저장하는 형식입니다. HTML과 유사해 보이지만, HTML은 데이터를 시각적으로 표현하는 데 중점을 두고, XML은 데이터의 구조와 의미를 명확히 하는 데 중점을 둡니다.

예를 들어 "이름이 kim이고 나이가 20"이라는 데이터를 XML로 표현하면:

```xml
<person>
  <name>kim</name>
  <age>20</age>
</person>
```

## 핵심 개념

### "X" 확장자의 정체: ZIP + XML

.docx, .xlsx, .pptx, .hwpx 등 최신 Office 파일들은 사실 **ZIP 압축 파일**입니다. 각 파일을 .zip으로 확장자를 바꾼 후 압축을 해제하면, 내부에 여러 개의 **XML 파일**과 폴더들이 저장되어 있음을 발견할 수 있습니다.

"X"는 "XML"을 의미합니다.

이렇게 설계한 이유는:
- 데이터를 구조화되어 저장할 수 있어 프로그래밍으로 접근하기 쉬움
- ZIP 압축으로 파일 크기를 줄일 수 있음
- 텍스트 기반이어서 버전 관리 시스템과 호환성이 좋음

### 워드 파일(.docx) 구조

Word 문서를 .zip으로 변환해 압축 해제하면 다음과 같은 구조를 볼 수 있습니다:

```
docx-file/
├── word/
│   ├── document.xml      # 실제 글 내용
│   ├── styles.xml        # 폰트, 색상, 단락 스타일 등
│   ├── numbering.xml     # 목록 스타일
│   └── media/            # 이미지, 비디오 등 미디어 파일
├── _rels/
│   └── .rels             # 파일 간 연결 관계
├── [Content_Types].xml   # 파일 형식 정의
└── docProps/             # 문서 속성 (제목, 작성자 등)
```

**document.xml** 내용의 예:

실제 문서에 "안녕하세요"라고 입력하면, document.xml에는 다음과 같이 저장됩니다:

```xml
<w:document>
  <w:body>
    <w:p>
      <w:r>
        <w:t>안녕하세요</w:t>
      </w:r>
    </w:p>
  </w:body>
</w:document>
```

### 엑셀 파일(.xlsx) 구조와 압축 기법

Excel 파일도 마찬가지로 여러 XML 파일로 이루어져 있습니다:

```
xlsx-file/
├── xl/
│   ├── worksheets/
│   │   └── sheet1.xml       # 시트의 실제 데이터
│   ├── sharedStrings.xml    # 중복되는 문자열 저장소
│   ├── workbook.xml         # 시트 목록, 설정 등
│   ├── styles.xml           # 셀 스타일 정의
│   └── media/               # 이미지 등
├── _rels/
└── [Content_Types].xml
```

**엑셀의 똑똑한 압축 기법**

엑셀 파일에서 "제목", "가격", "수량" 같은 텍스트가 여러 번 반복된다면, 매번 같은 문자열을 저장하는 것은 비효율적입니다. 따라서 엑셀은:

1. **sharedStrings.xml**에 모든 고유한 문자열을 저장:
```xml
<sst>
  <si><t>제목</t></si>      <!-- 인덱스 0 -->
  <si><t>가격</t></si>      <!-- 인덱스 1 -->
  <si><t>수량</t></si>      <!-- 인덱스 2 -->
</sst>
```

2. **sheet1.xml**에서는 인덱스만 참조:
```xml
<c><v>0</v></c>  <!-- "제목" 참조 -->
<c><v>1</v></c>  <!-- "가격" 참조 -->
<c><v>2</v></c>  <!-- "수량" 참조 -->
```

이 방식으로 중복 데이터를 제거해 파일 크기를 획기적으로 줄입니다.

## 작동 원리

### 단계 1: 파일 형식 변환

1. 변환하고 싶은 .docx 파일을 준비합니다.
2. 파일의 확장자를 .zip으로 변경합니다.
3. ZIP 파일 매니저(Windows 탐색기, 7-Zip, WinRAR 등)로 압축을 해제합니다.

### 단계 2: 내부 구조 확인

압축 해제된 폴더를 열면:
- **word/** 또는 **xl/** 폴더에 핵심 데이터 파일(XML)들이 있음
- **media/** 폴더에 이미지, 비디오 등이 있음
- XML 파일들은 코드 에디터(VS Code 등)로 열어 볼 수 있음

### 단계 3: 데이터 추출 및 수정

**워드 문서에서 텍스트만 추출:**
- document.xml 파일을 VS Code 등의 에디터로 열기
- `<w:t>` 태그 안의 내용만 추출
- AI에 붙여 넣어 요약, 번역 등 처리

**엑셀 파일에서 데이터 추출:**
- sheet1.xml에서 필요한 셀 값 추출
- sharedStrings.xml과 대조하여 실제 문자열 획득

**이미지 추출:**
- media/ 폴더의 이미지를 그대로 복사
- 원본 품질의 이미지를 손쉽게 획득

### 단계 4: 파일 재구성

1. XML 파일 수정
2. 수정된 폴더를 다시 ZIP으로 압축
3. 확장자를 .docx 또는 .xlsx로 변경
4. Office에서 정상적으로 열림

## 코드 예시

### Python으로 DOCX 파일에서 텍스트 추출

**방법 1: 저수준 접근 (ZIP + XML 직접 처리)**

```python
import zipfile
import xml.etree.ElementTree as ET

# DOCX 파일을 ZIP으로 읽기
with zipfile.ZipFile('document.docx', 'r') as zip_ref:
    # document.xml 추출
    xml_content = zip_ref.read('word/document.xml')

# XML 파싱
root = ET.fromstring(xml_content)

# Word XML의 네임스페이스 정의
namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# 모든 텍스트 추출
text_elements = root.findall('.//w:t', namespace)
full_text = ''.join([elem.text for elem in text_elements if elem.text])

print(full_text)
```

**방법 2: 고수준 라이브러리 사용 (권장)**

```python
from docx import Document

# DOCX 파일 열기
doc = Document('document.docx')

# 모든 단락의 텍스트 추출
for paragraph in doc.paragraphs:
    print(paragraph.text)

# 표의 데이터 추출
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text, end=' ')
```

설치: `pip install python-docx`

### Python으로 XLSX 파일 처리

**엑셀 데이터 추출:**

```python
from openpyxl import load_workbook

# 엑셀 파일 로드
wb = load_workbook('spreadsheet.xlsx')
ws = wb.active

# 모든 셀 데이터 반복
for row in ws.iter_rows(values_only=True):
    print(row)

# 특정 셀 접근
cell_value = ws['A1'].value
print(f"A1 값: {cell_value}")
```

설치: `pip install openpyxl`

**시트 암호 해제:**

```python
from openpyxl import load_workbook
import zipfile
import xml.etree.ElementTree as ET

# 엑셀 파일을 ZIP으로 처리
with zipfile.ZipFile('protected.xlsx', 'r') as zip_ref:
    # 각 시트의 XML 파일 수정
    with zipfile.ZipFile('unprotected.xlsx', 'w') as zip_out:
        for item in zip_ref.infolist():
            content = zip_ref.read(item.filename)
            
            # 시트 XML에서 보호 설정 제거
            if item.filename.startswith('xl/worksheets/sheet'):
                tree = ET.fromstring(content)
                # sheetProtection 태그 찾아서 제거
                for elem in tree.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheetProtection'):
                    tree.remove(elem)
                content = ET.tostring(tree)
            
            zip_out.writestr(item, content)
```

**주의:** 파일 전체가 암호화되어 있으면 이 방법으로 해제할 수 없습니다. 시트 단위의 보호만 해제 가능합니다.

### 대량 문서 처리: 1만 개 워드 파일에서 총액 추출

```python
import os
from docx import Document
from pathlib import Path

# 문서 폴더 경로
documents_folder = './documents/'
total_amount = 0

# 모든 DOCX 파일 순회
for docx_file in Path(documents_folder).glob('*.docx'):
    try:
        doc = Document(docx_file)
        
        # 문서의 모든 테이블에서 금액 찾기
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text = cell.text.strip()
                    # 숫자만 추출 (예: "10,000원" → 10000)
                    if text and text[0].isdigit():
                        try:
                            amount = int(''.join(c for c in text if c.isdigit()))
                            total_amount += amount
                        except ValueError:
                            pass
    except Exception as e:
        print(f"Error processing {docx_file}: {e}")

print(f"총액: {total_amount:,}")
```

## 함정·실수

### 1. 암호화된 파일은 처리 불가

**실수:** DOCX/XLSX 파일이 "Encrypt as OLE object" 또는 "Password protect" 옵션으로 완전히 암호화되어 있으면, ZIP으로 변환해도 내용이 암호화되어 있어 열 수 없습니다.

**회피법:** 
- 파일을 Office에서 열어 원본 암호를 입력한 후 다시 저장할 때 암호 없이 저장
- 파일 전체의 암호화 VS 시트/문서 보호 구분 (시트 보호만 제거 가능)

### 2. 인터넷의 출처 불명의 문서 파일 위험

**실수:** ZIP 파일 구조이므로 악의적인 실행 파일(.exe, 스크립트 등)을 media 폴더에 숨겨 넣을 수 있습니다. 파일을 열 때 악성 코드가 실행될 수 있습니다.

**회피법:**
- 신뢰할 수 없는 출처의 파일은 먼저 압축을 해제해서 내용 검토
- XML 파일만 추출해 AI로 분석
- 최신 Office 버전 사용 (보안 패치 포함)

### 3. 파일 수정 후 손상 위험

**실수:** XML을 직접 수정할 때 태그를 잘못 닫거나 인코딩을 변경하면 파일이 열리지 않을 수 있습니다.

**회피법:**
- 원본 파일 백업 후 수정
- XML 검증 도구 사용 (온라인 XML validator)
- 가능하면 공식 라이브러리(python-docx, openpyxl) 사용

### 4. 중복된 문자열 인덱싱 실수 (엑셀)

**실수:** sharedStrings.xml의 인덱스가 변경되었는데 시트의 참조를 업데이트하지 않으면 데이터가 뒤바뀝니다.

**회피법:**
- XML을 직접 수정하지 말고 openpyxl 등 라이브러리 사용
- 라이브러리가 자동으로 인덱스 관리

### 5. 이미지 추출 시 품질 손실 없음을 모르는 경우

**실수:** "DOCX에 포함된 이미지는 압축되어 있을 거야" 라고 가정

**사실:** DOCX/PPTX에 포함된 이미지는 원본 파일이 그대로 저장되므로, media 폴더에서 추출한 이미지는 100% 원본 품질입니다.

### 6. 매우 큰 문서 파일의 처리 시간

**실수:** 이미지가 많은 대용량 PPT(1GB 이상)를 메모리에 한 번에 로드

**회피법:**
- ZIP 파일을 스트림 방식으로 처리
- media 폴더의 이미지만 선택적으로 처리

## 베스트 프랙티스

### 1. 정식 라이브러리 사용

XML을 직접 다루는 것보다 설계된 라이브러리를 사용하세요:

**Python:**
- `python-docx`: DOCX 파일 조작
- `openpyxl`: XLSX 파일 조작
- `python-pptx`: PPTX 파일 조작

이들 라이브러리는 내부 XML 복잡성을 숨기고 직관적인 API를 제공합니다.

### 2. 파일 처리 전 백업

```python
import shutil

# 원본 백업
shutil.copy('important_document.docx', 'important_document_backup.docx')
```

### 3. 대량 처리 시 자동화의 이점 극대화

파일 1개를 수정하는 데 2분이 걸리는데, 1000개면 2000분(33시간)이 필요합니다. 이런 반복 작업은:
- Python 스크립트로 자동화 → 수분 내 완료
- 휴먼 에러 제거
- 일관된 품질 보장

### 4. 직접 형식 변환기 개발의 이점

온라인 변환 사이트 대신 직접 코드를 작성하면:

```python
# 예: DOCX → CSV 추출
def docx_to_csv(docx_path, csv_path):
    from docx import Document
    import csv
    
    doc = Document(docx_path)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for table in doc.tables:
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                writer.writerow(row_data)
```

**장점:**
- **보안:** 문서를 외부 서버로 보내지 않음
- **대량 처리:** 수천 개 파일도 순간에 처리
- **커스터마이징:** 특정 형식으로만 데이터 추출 가능

### 5. AI와 함께 자동화

구조화된 데이터(XML)는 AI 분석에 최적입니다:

```python
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from docx import Document

client = Anthropic()

# DOCX에서 텍스트 추출
doc = Document('document.docx')
text = '\n'.join([p.text for p in doc.paragraphs])

# Claude API로 분석
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": f"다음 문서를 분석해서 주요 내용을 3줄로 정리해주세요:\n\n{text}"
        }
    ]
)

print(response.content[0].text)
```

### 6. HWPX 활용

공공기관이 HWP에서 HWPX로 변경한 이유:
- HWP: 바이너리 형식 → 코드 접근 어려움
- HWPX: ZIP + XML 형식 → 코드 접근 용이

HWPX 처리도 DOCX와 동일한 원리입니다:

```python
import zipfile
import xml.etree.ElementTree as ET

# HWPX 파일 열기
with zipfile.ZipFile('document.hwpx', 'r') as zip_ref:
    # 한글의 경우 'Contents/section0.xml' 등에 본문이 저장
    xml_content = zip_ref.read('Contents/section0.xml')
    # 이후 XML 파싱은 동일
```

## 참고

**영상에서 언급된 자료:**
- [W3C XML Datamodel](https://www.w3.org/XML/Datamodel.html) — XML의 공식 명세
- Tenor — 영상에서 사용된 GIF 출처
- 네이버 스포츠 (메이플스토리 커뮤니티) — 게임 커뮤니티 언급

**추가 학습 자료:**
- [Office Open XML 공식 표준](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/) — DOCX, XLSX, PPTX의 정식 명세
- [python-docx 공식 문서](https://python-docx.readthedocs.io/) — Python DOCX 라이브러리
- [openpyxl 공식 문서](https://openpyxl.readthedocs.io/) — Python XLSX 라이브러리
- [LibreOffice 문서](https://www.libreoffice.org/) — 오픈소스 Office 대안

**핵심 교훈:**
파일 확장자의 "X"가 XML을 의미한다는 단순한 사실로부터, 문서 자동화, 보안 강화, 대량 처리 등 무한한 가능성이 펼쳐집니다. Office 파일의 구조를 이해하면 더 이상 마우스로 수동 작업하지 않아도 됩니다.