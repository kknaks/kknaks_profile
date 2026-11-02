# strong-hajin-attach-read 결과 보고 — 결과 자료 「내용을 읽지 못함 · 본문에 텍스트가 없습니다」 원인 조사

## 상태: done (조사 · read-only, 코드 변경 없음)

워크트리 `strong-hajin-attach-read` (base `origin/main` = `baf7daf`). 아래 `파일:줄`은 모두 이 워크트리 기준.

---

## 0. 결론 먼저

- 화면 문구는 **`failure_reason = "empty_content"` 하나에서만** 나온다. 전체 문장은
  **「내용을 읽지 못함 · 본문에 텍스트가 없습니다 (스캔 이미지 PDF 또는 빈 파일)」**다.
- 사용자가 올린 파일은 **PDF이거나 DOCX/PPTX/XLSX**다. 이미지(png/jpg)·hwp·doc 같은 파일이었다면 `unsupported`로 떨어져
  「검색 미지원 형식」 배지가 뜬다.
  3.1MB 파일이 이 배지를 받으려면 다음 중 하나여야 한다.
  1. **PDF**: 모든 쪽에서 pypdf 텍스트가 비고, `_page_has_images`도 **어느 쪽에서도 이미지를 못 찾은** 경우.
     → 스캔 PDF여도 이미지가 **Form XObject 안에 싸여 있거나** **인라인 이미지**(BI/ID/EI)이거나 글자를 **윤곽선(벡터)으로 바꾼** PDF라면 `needs_ocr`가 아니라 `empty_content`로 떨어진다. 합성 PDF로 실제 확인했다(§6).
  2. **PPTX/DOCX/XLSX**: 텍스트 프레임·문단·셀이 하나도 없는 경우(예: 슬라이드 전체가 그림인 PPTX).
     이 형식에는 이미지 판정이 없어서 무조건 `empty_content`로 가고, 문구는 「스캔 이미지 PDF 또는 빈 파일」이라고 나온다.
- **OCR 경로는 없다**(의도된 계약: "OCR 미도입"). 계약은 "이미지만 있는 PDF → `needs_ocr`, 진짜 빈 것 → `empty`"로 둘을 가르는 것이다.
  그런데 구현에는 **두 군데 어긋남**이 있다.
  - (a) 이미지 판정이 얕아 스캔 PDF를 `empty_content`로 오판한다.
  - (b) `needs_ocr`로 제대로 판정돼도 저장할 때 `status`가 `failed`로 바뀐다. 그래서 FE의 전용 배지 「스캔 문서 · 내용 검색 불가」는 실데이터로는 **절대 안 뜬다**.
- 이 상태가 되면 그 자료는 AX 자료 검색(HTTP·MCP `search_materials`)에서 `unavailable_materials`로만 나온다.
  **재시도 수단은 UI·API 어디에도 없다.**
- 실제 파일 행은 **로컬에 없다**. 로컬 `ax_demo`(+ `ax_demo_*` 4개)의 `attachments`가 0행이거나 해당 크기 행이 없다. 운영에서 올린 것으로 보이며, 운영에는 접근하지 않았다.

---

## 1. 문구는 어디서 만들어지나 (생산 → 표시)

| 단계 | 위치 | 내용 |
|---|---|---|
| 사유 코드 → 문장 | `backend/src/ax_workspace/modules/work/material_extraction.py:41` | `"empty_content": "본문에 텍스트가 없습니다 (스캔 이미지 PDF 또는 빈 파일)"` |
| (참고) 스캔 전용 문장 | `.../modules/work/material_extraction.py:47` | `"needs_ocr": "스캔 문서로 보입니다 — 텍스트 층이 없어 내용을 읽을 수 없습니다 (OCR 미도입)"` |
| 파서 status → 사유 코드 | `backend/src/ax_workspace/platform/material_extraction.py:44-51` | `_PARSER_FAILURES = {"empty": "empty_content", "needs_ocr": "needs_ocr", ...}` |
| 응답 직렬화 | `.../modules/work/material_extraction.py:382-404` `extraction_view()` | `failure_text = FAILURE_REASONS.get(failure_reason)` (`:391`) |
| 업무 자료 목록 응답 | `.../modules/work/materials.py:342` `material_view()` | `"extraction": extraction_view(extraction)` |
| (같은 view를 쓰는 곳) | `modules/work/material_search.py:109` · `modules/work/material_folders.py:146` · `bootstrap/application.py:3442` · `modules/meetings/results.py:191`(타입) | |
| FE 결과 자료 행 | `frontend/src/features/work/WorkModals.tsx:1951` | `<ExtractionStatus extraction={item.extraction ?? null} />` (「결과 자료」 라벨은 `frontend/src/lib/labels.ts:497`) |
| FE 배지 | `frontend/src/features/work/WorkModals.tsx:368-374` | `status`가 completed·queued·running·needs_ocr·purged가 아니면 빨간(`tone="danger"`) 배지를 띄운다. 본문은 `"내용을 읽지 못함"` + `" · " + failure_text`이고, `title`(hover)에 전체 failure_text가 들어간다 |

`empty_content`를 **만드는 곳**(레포 전체 grep, 테스트 제외):
1. `platform/material_extraction.py:91-92` — text/markdown이 UTF-8로 디코드됐는데 공백뿐일 때
2. `platform/material_extraction.py:115-120` — 문서 파서가 `status="empty"`를 돌려줬을 때(`_PARSER_FAILURES["empty"]`)
3. `platform/native_materials.py:207`, `:232` — 회의록·보고서 같은 **네이티브 개정본**이 비었을 때(업로드 파일과 무관)

FE 문자열 「내용을 읽지 못함」은 `WorkModals.tsx:371` 한 곳뿐이다. 「스캔」이 들어간 FE 문자열은 `WorkModals.tsx:358`(needs_ocr 전용 배지)과 테스트(`Checklist.test.tsx:659-662`)뿐이다.

---

## 2. 어떤 조건에서 이 상태가 되나 — 형식별 추출 경로

### 2.0 흐름
1. 업로드: `modules/work/materials.py:216-241` `attach()` — 25MB 상한(`:225`) → `store_file` → binding.
   같은 트랜잭션에서 `extractions.request(attachment)`(`:238`)를 부르고, `queued`면 `MaterialExtractionJob`을 enqueue한다(`:239-240`).
   회의 자료는 `modules/meetings/materials.py:240-243`으로 같은 방식이다.
2. 워커: `bootstrap/material_worker.py:289-347` `process()` — claim → `MaterialExtractionService.extract(claimed, storage, PypdfTextExtractor)`(`:340`) → `finish()`(`:343`).
3. 추출: `modules/work/material_extraction.py:337-345` — 무결성 sha256 불일치면 `integrity_mismatch`, 아니면 `extractor.extract(...)`. **어떤 예외든 `extractor_error`(transient)** 로 바뀐다(`:344-345`).
4. 분류: `platform/material_extraction.py:62-126` `PypdfTextExtractor._extract`
   - `classify()`(`modules/work/material_extraction.py:148-158`)가 `text`/`markdown`을 고르면 UTF-8로 처리한다(`:87-97`).
   - 그 밖에는 `classify_document()`(`modules/work/document_parsing.py:40-47`, 확장자 우선 → MIME)를 거친다. **docx/docm/xlsx/xlsm/pptx/pptm/pdf만** 받는다.
     나머지(png/jpg/hwp/doc/xls/ppt…)는 `unsupported`(`platform/material_extraction.py:98-100`)로 끝나고, 배지는 「검색 미지원 형식」이다(**이번 배지가 아님**).
5. 판정: `platform/material_extraction.py:115-120` — 파서 status가 ok/partial이 아니거나 chunk가 0이면 `_PARSER_FAILURES`로 사유를 정한다.
   status는 `needs_ocr`/`unsupported`/`too_large`/그 외 `failed`다.
6. 저장: `modules/work/material_extraction.py:347-368` `finish()` → `repository.fail()`(`platform/material_extraction.py:349-363`)이 `status`와 `failure_reason`을 기록한다.

### 2.1 형식별 「텍스트 없음」 분기

| 형식 | 위치 | `empty_content`가 되는 조건 |
|---|---|---|
| text/markdown(.txt .csv .log .md, `text/*`) | `platform/material_extraction.py:91-92` | UTF-8 디코드 결과가 `strip()` 후 빈 문자열일 때. UTF-8이 아니면 `not_utf8_text`(`:89-90`) |
| **PDF** | `platform/document_parsers.py:365-426` | 쪽마다 `page.extract_text()`(`:398`)를 부른다. `text.strip()`이 비어 있고(`BlockCollector.add`도 공백 블록을 버린다 — `modules/work/document_parsing.py:187-189`) `_page_has_images(page)`도 False인 쪽만 남으면 **`STATUS_EMPTY`**(`:426`, detail `"no text and no images"`) |
| DOCX | `document_parsers.py:170-210` | 본문 자식 중 **`w:p`·`w:tbl`만** 읽고(`:180-188`), 머리글·바닥글(`:189-208`)을 더해 블록이 0개면 `STATUS_EMPTY`(`:209`). 이미지 판정이 없다. `w:sdt`(콘텐츠 컨트롤)로 감싼 본문은 순회에서 빠진다(코드상 사실). 텍스트 상자(`w:txbxContent`)는 `Paragraph.text`에 안 잡히는 것으로 안다(**추측**: python-docx 동작) |
| PPTX | `document_parsers.py:323-361` | 텍스트 프레임·표·노트만 모은다(`:350-361`). 그림 도형, 차트, SmartArt는 무시한다. 블록이 0개면 `STATUS_EMPTY`(`:347`) → **그림으로만 된 슬라이드 덱은 무조건 `empty_content`** |
| XLSX | `document_parsers.py:236-285` | 비어 있지 않은 셀이 없으면 `STATUS_EMPTY`(`:285`) |

### 2.2 PDF 스캔 판정 기준 (임계값)
- **글자 수 임계값은 없다.** 쪽 단위로 `not text.strip()`(공백 제외 0자)이면 "텍스트 없음"으로 본다(`document_parsers.py:412`).
  즉 쪽번호나 머리글 한 줄만 텍스트 층에 있는 스캔 PDF는 "텍스트 있음"으로 `completed`가 된다(반대 방향의 오판 가능성, §5-d).
- 텍스트 없는 쪽에 대해 `_page_has_images(page)`(`document_parsers.py:502-515`)가 True면 `needs_ocr` 쪽으로, 아니면 그냥 빈 쪽으로 친다. 이 함수는:
  - 그 쪽의 `/Resources` → `/XObject` **최상위 한 단계에서만** `/Subtype /Image`를 찾는다(`:505-512`).
  - **Form XObject 안쪽은 보지 않는다**(`_pdf_content_size`·`_pdf_expansion_size`는 Form을 재귀하지만 이미지 판정에는 쓰이지 않는다).
  - **인라인 이미지(BI…ID…EI)는 리소스에 없으므로** 못 찾는다.
  - 내부에서 **모든 예외를 삼키고 `False`** 를 돌려준다(`:513-514`). 예외는 곧 "이미지 없음"이 된다.
- 최종 분기(`document_parsers.py:417-426`):
  - 블록 ≥ 1 → `ok`, 또는 빠진 쪽이 있으면 `partial`(`:418-421`)
  - 블록 0이고 `image_pages > 0` → `needs_ocr`(`:422-423`)
  - 블록 0이고 디코드 실패 쪽이 있음 → `corrupt`(`:424-425`)
  - 그 밖 → **`empty`**(`:426`)
- 페이지 상한: `ParseBudget.max_pdf_pages` 기본값은 `None`(`modules/work/document_parsing.py:81`)이고, `OfficeDocumentParser()`는 기본 budget으로 생성된다(`platform/material_extraction.py:60`, `document_parsers.py:137`).
  즉 설계 문서의 "PDF 300쪽 상한"(`docs/material-data-management-design.md:57`)은 **현재 걸려 있지 않다**(이번 증상과는 무관).

---

## 3. OCR(이미지 → 텍스트) 경로가 있나
- **없다.** `backend/src`에서 `ocr`/`tesseract`는 사유 코드 문자열과 주석에만 나온다.
  의존성은 `backend/pyproject.toml:13` `pypdf>=6.16.2`(설치 6.16.2)이고 OCR 엔진은 없다.
- 계약상으로도 미도입이다: `docs/material-data-management-design.md:79-81` §6 "OCR 필요 상태 … OCR 도입 여부·엔진은 별도 결정", `docs/material-integrity.md:93` "OCR·embedding … 없음".
- 따라서 이번 파일은 "OCR을 안 탔다"가 아니라 **"OCR 필요(`needs_ocr`)로도 분류되지 못하고 '빈 파일'로 분류됐다"** 가 맞는 설명이다(PDF라면 §2.2의 얕은 이미지 판정, PPTX/DOCX라면 형식별 이미지 판정 부재).

---

## 4. 이 상태가 되면 무엇이 안 되나

- **블록·chunk가 저장되지 않는다**: `repository.fail()`이 chunk·block을 지우고 `chunk_count = char_count = 0`으로 둔다(`platform/material_extraction.py:350-356`).
- **AX 자료 검색에서 빠진다**: `project_material()`이 `completed`(material_id를 지정했으면 `partial`도)만 searchable로 본다(`modules/work/material_search_policy.py:77-81`).
  나머지는 `unavailable_materials`에 `reason: "extraction"`과 `extraction` view(사유 문장 포함)를 붙여 응답한다(`modules/work/material_search.py:111-117`, `:134`).
  이 검색은 HTTP `GET` search(`entrypoints/http.py:2244-2252`)와 MCP 도구 `search_materials`(`entrypoints/mcp.py:1231-1235`, 도구 카탈로그 `modules/ax_execution/tool_catalog.py:406`) 둘 다 쓴다.
  → **AX 대화가 이 파일 내용을 근거로 쓸 수 없다**(목록에는 "읽지 못한 자료"로 보인다).
- 회의록·보고서 생성이 업무 결과 자료의 **추출 텍스트를 직접 읽는 경로는 찾지 못했다**. `material_chunks`·`material_blocks`를 읽는 곳은 검색(`LexicalMaterialRetriever`/chunk index)과 purge(`bootstrap/application.py:3183-3184`)뿐이다.
  회의(`modules/meetings/materials.py`)와 보고서는 같은 추출 파이프라인에 자료를 넣고 상태만 보여 준다.
  (**추측 아님**, grep 기준. 다만 LLM 프롬프트가 원본 바이트를 직접 붙이는 경로는 grep 범위 밖일 수 있다.)
- 파일 자체(열기/다운로드 `task_material_content`, `entrypoints/http.py:2266`)와 완료 보고 첨부는 그대로 된다. 추출 상태와 무관하다.
- **재시도 수단은 없다.**
  - `request()`는 같은 `(attachment_id, integrity_ref, parser_version)`이면 기존 행을 그대로 돌려준다(`platform/material_extraction.py:146-154`). 같은 첨부는 다시 enqueue되지 않는다.
  - 검색 시 백필은 `extraction_status is None`일 때만 걸린다(`material_search_policy.py:76`). 실패 행은 대상이 아니다.
  - 파서 업그레이드 재추출(`request_upgrades`, `:176-197`)은 `UPGRADABLE_PARSER_VERSIONS = {"1","2"}`(`modules/work/material_extraction.py:27`)만 대상이다. 현재 버전 `"3"`의 실패 행은 다시 돌지 않는다.
  - `bootstrap/application.py:3148` `reextract_material()`이 있지만 **`backend/src` 안에서 호출하는 곳이 없다**(HTTP·MCP 미노출).
  - transient 재시도(`extractor_error`, `max_attempts=3`)는 예외 경로에만 있다. `empty_content`는 결정적 결과라 재시도되지 않는다.
  - 같은 파일을 다시 올리면 새 attachment로 새 추출이 걸리지만 **같은 결과**가 나온다.

---

## 5. 의도된 계약대로인가, 오판 자리는

계약(`docs/material-data-management-design.md:81`): "parser는 `needs_ocr`(이미지 있음, 텍스트 없음)와 `empty`를 구분한다. **저장 시 `material_extractions.status=needs_ocr`** 로 두고 UI는 '스캔 문서 — 내용 검색 불가(OCR 미도입)'로 표시."
`docs/material-integrity.md:9`: "읽은 본문이 없으면 설명 가능한 실패로 끝낸다."

- **(a) 오판 — PDF 이미지 판정이 얕다** (`document_parsers.py:502-515`)
  최상위 `/XObject`의 `/Image`만 본다. 스캔·복합기 PDF에 흔한 다음 모양은 이미지가 있어도 False가 되어 **`empty_content`(「빈 파일」)** 로 떨어진다.
  - Form XObject로 감싼 이미지(일부 스캐너, PDF 편집기가 쪽을 재포장한 경우, "PDF로 인쇄"가 만드는 구조)
  - 인라인 이미지
  §6에서 실측했다. "스캔인데 빈 파일이라고 말하는" 오판이다.
- **(b) 예외를 삼켜 같은 사유로 떨어뜨리는 곳** — `_page_has_images`의 `except Exception: return False`(`document_parsers.py:513-514`)
  리소스를 읽다 난 오류가 "이미지 없음"이 되고, 결국 `empty_content`로 합쳐진다.
  (참고로 쪽 디코드 예외(`:408-411`)는 `decode_failed`로 따로 남아 전부 실패면 `corrupt`가 되므로 이쪽은 섞이지 않는다.
  `MaterialExtractionService.extract`의 포괄 except(`modules/work/material_extraction.py:344-345`)와 `parse()`의 포괄 except(`document_parsers.py:162-163`)는 각각 `extractor_error`·`corrupt_document`로 가므로 `empty_content`와 섞이지 않는다.)
- **(c) 계약 위반 — `needs_ocr`가 저장 단계에서 `failed`로 바뀐다**
  `finish()`가 `status = outcome.status if outcome.status in {"failed","unsupported","too_large"} else "failed"`로 처리한다(`modules/work/material_extraction.py:366`).
  `needs_ocr`는 이 집합에 없으므로 DB에는 `status="failed", failure_reason="needs_ocr"`로 남는다.
  FE는 `status === "needs_ocr"`(`WorkModals.tsx:354`)로만 전용 배지를 고르므로, 실데이터의 스캔 PDF도 빨간 「내용을 읽지 못함 · 스캔 문서로 보입니다 — …」로 뜬다.
  FE 테스트(`Checklist.test.tsx:659`)는 `status: "needs_ocr"`를 직접 주입해서 이 어긋남을 못 잡는다.
  `docs/domain-model.md:135`도 lifecycle을 `queued/running/completed/partial/failed`로만 적고 있어 문서끼리도 갈린다.
  **이번 화면(empty_content)의 직접 원인은 아니지만**, (a)를 고쳐 `needs_ocr`로 분류돼도 화면은 여전히 빨간 「읽지 못함」이 된다.
- **(d) 문구 자체의 범위 문제**
  `empty_content` 문장은 「스캔 이미지 PDF 또는 빈 파일」이라고 PDF를 전제한다.
  하지만 PPTX/DOCX/XLSX/텍스트 파일도 같은 코드를 쓴다(§2.1). 그림만 있는 PPTX에 "스캔 이미지 PDF 또는 빈 파일"이라고 보여 주게 된다.
  또 스캔 판정은 "이미지 판정"이 맡고 있어서 `empty`의 의미가 이미 "이미지도 없음"인데(`document_parsing.py:53`), 문장은 스캔일 수도 있다고 말한다. 판정과 문장이 서로 엇갈린다.
- **(e) 반대 방향 오판(참고)**
  텍스트 임계값이 0자라서, 텍스트 층에 쪽번호 정도만 있는 스캔 PDF는 `completed`(내용 검색 가능)로 표시되지만 실제로는 검색에 거의 걸리지 않는다. 이번 증상과는 반대다.
- **(f) 텍스트는 있는데 「텍스트 없음」이 되는 경우** (**추측**)
  ToUnicode가 없거나 Type3 폰트를 쓰는 PDF는 pypdf가 깨진 글자를 내는 일이 대부분이다. 완전히 빈 문자열을 내는 경우는 드물다고 본다.
  따라서 "텍스트 PDF인데 `extract_text`가 예외를 냈고 그게 empty로 둔갑"하는 경로는 코드상 없다(예외는 `decode_failed` → `corrupt`).
  남는 가능성은 글자를 **윤곽선으로 변환한 PDF**(디자인 툴 출력)다. 사람 눈에는 글자지만 텍스트 층도 이미지도 없어 `empty_content`가 된다(§6 E).

---

## 6. 실제 기록 · 실측

### 6.1 DB (SELECT만, `PGOPTIONS=-c default_transaction_read_only=on`)
- `postgresql://ax:ax@127.0.0.1:54329/ax_demo`(Makefile `DATABASE_URL` 자격증명): `select count(*) from attachments` → **0행**. `material_extractions`도 0행.
- `ax_demo_inbox`·`ax_demo_polish`·`ax_demo_polish2`·`ax_demo_polish3`에서 2.9~3.4MB 첨부 또는 `failure_reason='empty_content'`를 조회했고 **모두 0행**이다.
- → **로컬에 없음.** 운영에서 올린 파일로 보인다. 운영 DB와 서버에는 접근하지 않았다.
  운영에서 확인할 쿼리는 이렇다(코디/운영 담당용):
  ```sql
  select a.name, a.content_type, a.size_bytes, a.created_at, e.status, e.failure_reason, e.extractor,
         e.parser_version, e.page_count, e.warnings, e.coverage
  from attachments a join material_extractions e on e.attachment_id = a.id and e.superseded_at is null
  where a.created_at::date = '2026-10-13' and a.size_bytes between 3000000 and 3300000;
  ```
  `extractor`가 `pdf`/`pptx`/`docx`/`xlsx`/`text`인지 보면 §2.1의 어느 줄인지 바로 갈린다. PDF면 `page_count`가 채워져 있고 `coverage.reason="no text and no images"`일 것이다.

### 6.2 추출 함수 실측 (합성 PDF, 메모리 안 · 레포/DB 무변경)
스크래치 스크립트로 1×1 이미지 PDF 다섯 종을 만들어 **운영과 같은 `PypdfTextExtractor().extract()`** 에 넣었다(pypdf 6.16.2).

| 케이스 | 결과 |
|---|---|
| A. 쪽 리소스에 직접 Image XObject | `needs_ocr / needs_ocr` ✅ 계약대로 |
| B. **Image를 Form XObject로 감쌈** | **`failed / empty_content`** ❌ 스캔인데 빈 파일 |
| C. **인라인 이미지(BI/ID/EI)** | **`failed / empty_content`** ❌ |
| D. Image 리소스를 Pages 노드에서 상속 | `needs_ocr / needs_ocr` ✅ |
| E. 윤곽선(벡터 path)만, 이미지 없음 | `failed / empty_content` (계약상 empty, 사람 눈엔 글자) |

(이 표의 `needs_ocr`는 `extract()` 출력이다. `finish()`를 거치면 §5-c대로 DB status는 `failed`가 된다.)
`git status`는 실행 전후 모두 clean이다(`uv run`이 만든 `backend/.venv`는 gitignore 대상).

---

## 원인 한 줄 요약
업로드 파일(PDF 또는 Office)에서 텍스트 층이 0자로 나왔고, 이미지 판정이 최상위 Image XObject만 보거나(PDF) 아예 없어서(PPTX/DOCX/XLSX) 「OCR 필요」가 아니라 `empty_content`(「본문에 텍스트가 없습니다 (스캔 이미지 PDF 또는 빈 파일)」)로 분류됐다. OCR 경로와 재추출 수단이 없어 이 상태가 영구히 남고, 그 자료는 AX 자료 검색에서 빠진다.

## 고친다면 선택지 (결정하지 않음)
1. **이미지 판정 강화(PDF)**: `_page_has_images`가 Form XObject를 재귀로 보고(기존 `_pdf_expansion_size`의 순회·한도 재사용), 콘텐츠 스트림의 인라인 이미지(`BI`)도 보게 한다. 예외를 삼켜 False로 만드는 대신 `missing_units`에 `image_probe_failed`를 남긴다.
   대안으로 "텍스트 0자 + 쪽 콘텐츠가 비어 있지 않음"이면 보수적으로 `needs_ocr`로 분류할 수 있다(벡터 윤곽선 PDF도 "읽을 수 없음"으로 잡히지만 오탐도 생긴다).
2. **`needs_ocr` 저장 계약 복구**: `finish()`의 허용 status 집합에 `needs_ocr`를 넣는다(`modules/work/material_extraction.py:366`). 이와 함께 DB status 값 범위, `docs/domain-model.md:135`, FE 테스트를 실제 저장값 기준으로 맞춘다.
   또는 FE가 `failure_reason === "needs_ocr"`로도 전용 배지를 고르게 하는 FE 쪽 대안이 있다.
3. **Office 형식의 「그림만 있음」 구분**: PPTX picture shape, DOCX `w:drawing`, XLSX 이미지가 있으면 `needs_ocr`(또는 새 사유 "그림만 있음") 쪽으로 보낸다. DOCX `w:sdt`·텍스트 상자 본문도 읽게 한다.
4. **문구만 정정(최소)**: `empty_content` 문장을 형식 중립으로 바꾼다(예: "읽을 수 있는 텍스트가 없습니다 — 그림·스캔으로만 된 문서이거나 빈 파일"). 판정은 그대로 두고 오해만 줄인다.
5. **재시도 수단**: 숨은 `reextract_material`(`bootstrap/application.py:3148`)을 권한 있는 명령으로 노출하거나, 판정 로직을 바꿀 때 `PARSER_VERSION`을 올리고 `"3"`을 `UPGRADABLE_PARSER_VERSIONS`에 넣어 기존 `empty_content`/`needs_ocr` 행을 백필 재추출한다.
6. **OCR 도입**: 설계 문서 §6의 별도 결정 사항(엔진·비용·개인정보). 1~3이 선행되어야 OCR 대상이 정확히 골라진다.

## 다른 팀 영향
- FE: 전용 `needs_ocr` 배지(`WorkModals.tsx:354-361`)가 실데이터로는 도달하지 못한다(§5-c). 어느 쪽을 고칠지는 결정이 필요하다.
- planner: `docs/domain-model.md:135` lifecycle 목록과 설계 문서 §6(`status=needs_ocr`)이 서로 갈리고 구현은 후자를 따르지 않는다. SPEC 정본 확인이 필요하다.

## 이슈/블로커
- 실제 파일과 DB 행은 운영에만 있다. 형식(PDF vs PPTX 등)은 §6.1 쿼리로 운영에서 확인해야 확정된다.

---

## 7. 추가 조사 — 실제 파일 `~/Downloads/세라미크_명동_본사_인터뷰.pdf` (read-only)

방법: 원본 경로를 그대로 열어 읽기만 했다(복사·수정·이동 없음). 실행 전후 크기 3,239,552 bytes와 mtime(Oct 13 09:20)이 같다.
워크트리 backend venv(pypdf 6.16.2)에서 스크래치 스크립트로 돌렸다. 레포·DB는 바꾸지 않았다.

### 7.1 운영과 같은 `PypdfTextExtractor().extract()` 결과
`status=failed · failure_reason=empty_content · page_count=14 · char_count=0 · warnings=() · coverage={'complete': False, 'reason': 'no text and no images'}`
→ 화면의 배지와 정확히 같다. (워커 경로의 `finish()`도 `failed`/`empty_content`를 그대로 저장한다 — `modules/work/material_extraction.py:366-367`.)

### 7.2 쪽별 `page.extract_text()` 글자 수
| 쪽 | 1–11 | 12 | 13–14 |
|---|---|---|---|
| len / strip 후 | 0 / 0 | **3 / 0** (`'  \n'`, 공백뿐) | 0 / 0 |

### 7.3 쪽별 리소스 구조 (Form XObject는 재귀로 확인)
| 항목 | 결과 |
|---|---|
| 최상위 `/XObject`의 Image | **14쪽 모두 0** |
| Form XObject 안의 Image | **0** (Form은 9쪽 3개, 10쪽 2개, 12쪽 1개만 있고 그 안에도 Image 없음) |
| 인라인 이미지 `BI` | **0** |
| `/Font` 리소스 | **12쪽에만 1개**(`/G1` Type0 `AAAAAB+font…`, ToUnicode 있음). 나머지 13쪽은 **0** |
| 텍스트 연산자 `BT`/`Tj`/`TJ` | **12쪽만 BT 2 · Tj 2**(공백 글리프). 나머지 13쪽은 **0** |
| 경로 연산자 | 쪽마다 `m`(moveto) 859~2,250개, `f`(fill) 284~839개, 곡선 `c` 다수(1쪽 249개). 콘텐츠 스트림은 쪽당 0.36~0.88MB |
| `_page_has_images()` | 14쪽 모두 **False** |

### 7.4 메타데이터
`/Producer = macOS Version 15.6.1 (Build 24G90) Quartz PDFContext` · `/Creator = Claude` · `/Author = admin` · `/Title = 세라미크_명동_본사_인터뷰` · `CreationDate = D:20261013002003Z` · PDF 1.3.
→ macOS 인쇄 파이프라인(Quartz)에서 만든 PDF다. Creator가 "Claude"이므로 Claude 앱(웹뷰)에서 HTML을 「PDF로 저장/인쇄」한 것으로 보인다.
Quartz는 보통 폰트를 임베드하는데, 이 파일에서 글자가 경로로 그려진 이유는 **추측**이다. 웹폰트나 웹뷰 렌더링 경로가 글리프를 윤곽선으로 내보냈을 가능성이 있다.

### 7.5 결론
- **텍스트 층이 없는 이유 = 벡터 윤곽선이다.**
  14쪽 중 13쪽에는 폰트 리소스와 텍스트 연산자가 아예 없다. 글자 모양이 수백~수천 개의 채움 경로(`m`/`l`/`c` + `f`)로 그려져 있다.
  래스터화 문제가 아니다(이미지 0개, 재귀 확인). 우리 추출기 문제도 아니다(꺼낼 텍스트 자체가 없다. 12쪽 유일한 텍스트도 공백 2글자).
  pypdf가 아닌 다른 텍스트 추출기를 써도 결과는 같을 것이다(**추측**이지만 근거는 `BT` 0개).
- **우리 코드가 탄 정확한 분기**
  1. `document_parsers.py:398`: 14쪽 모두 `extract_text()`가 공백뿐이다.
  2. `:412`: `_page_has_images()`가 모두 False라서 `image_pages`가 늘지 않는다. 디코드 예외가 없으므로 `missing`도 비어 있다.
  3. `:415` `collector.add()`: `strip()` 후 빈 문자열이라 블록이 0개다(`modules/work/document_parsing.py:187-189`).
  4. `:418`(`collector.count == 0`) → `:422`(`image_pages == 0`) → `:424`(`missing` 비어 있음)를 모두 통과해 **`:426` `STATUS_EMPTY`, detail `"no text and no images"`** 에 도달한다.
  5. `platform/material_extraction.py:115-118`: `_PARSER_FAILURES["empty"] = "empty_content"`, status `failed`.
  6. FE `WorkModals.tsx:368-374`: 「내용을 읽지 못함 · 본문에 텍스트가 없습니다 (스캔 이미지 PDF 또는 빈 파일)」.
- **§5 가설 중 맞은 것은 (f)/§6.2 E(윤곽선 PDF)** 다. (a) Form·인라인 이미지 누락은 이 파일과 **무관**하다(이미지가 정말 0개).
  판정 자체는 현재 계약("텍스트도 이미지도 없음 = empty")에 따르면 **정확하다**. 틀린 것은 **문구**다. 사용자에게 "스캔 이미지 PDF 또는 빈 파일"이라고 말하지만, 실제로는 글자가 그림(벡터)으로 그려져 사람 눈에는 멀쩡한 문서다.
- **선택지 재평가 (결정 안 함)**
  - §선택지 1(이미지 판정 강화)은 이 파일에 **효과가 없다**.
  - 효과가 있는 것은 셋이다.
    - §4 문구 정정: 예) "텍스트 층이 없습니다 — 글자가 그림·윤곽선으로 저장된 PDF이거나 스캔·빈 파일입니다. 원본(HTML/문서)을 올리거나 텍스트를 선택할 수 있는 PDF로 다시 저장하세요."
    - "텍스트 0 + 경로 그리기 연산 다수"를 `needs_ocr` 계열(새 사유, 예: `outlined_text`)로 구분하는 판정 추가.
    - §6 OCR 도입: 페이지를 래스터화한 뒤 OCR하면 읽힌다.
  - 사용자 쪽 우회는 원본 HTML 자체(현재 `text/html`은 `text` 추출기로 UTF-8 텍스트 처리 — `modules/work/material_extraction.py:156`)나 텍스트가 살아 있는 PDF를 올리는 것이다.
