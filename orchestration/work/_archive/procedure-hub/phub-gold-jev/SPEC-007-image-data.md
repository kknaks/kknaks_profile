---
type: spec
id: SPEC-007
title: "원리 · 방법 그림 데이터 — silver 그림 표 · 라벨 표 → 허브 DB 테이블 2 · 적재 · 그림 파일은 PROCEDURE-HUB 에셋 폴더(출력은 범위 밖)"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.1.0
created_at: 2026-11-17
updated_at: 2026-11-17
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/spec
  - status/draft
links:
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 — 「정정 — 그림은 DB 까지 이번 판 · 출력은 다음 스펙」 :49 · 「그림 결정」 U-4 · U-7 · U-10 :56 · 「서버 시드 방식 · 원천 CSV 자리 · stg gold 진입점은 대기」 :57 · 「concern_site 보강 판정 = 추천」 :51 · 「concern_site 보강은 한 번에」 :58 · 「바인드 마운트」 :66)"
    - "orchestration/work/phub-gold-jev/spec-image-data-instructions.md (「정해진 것」 — 위 _RESUME 행을 코디가 풀어 적은 지시서)"
  sources:
    - "orchestration/work/phub-gold-jev/research-images-v2.md (§0-2 U-1 ~ U-11 · §0-3 N-1 ~ N-3 · §1 · §3 — 103 새 SVG 기준 재셈)"
    - "orchestration/work/phub-gold-jev/research-images.md (§2 silver → gold 경로 · §3-3 해시 · §5-3 바인드 마운트 사실)"
    - "orchestration/work/phub-gold-jev/research-concern-site.md (§4 행 초안 · §5-3 37 키 · §6 추천 7고민 8행)"
    - "orchestration/work/phub-gold-jev/SPEC-003-hub-gold-db.md (0.1.0 — §2 테이블 규칙 R1 ~ R10 · §2-5 빌드 기록 · §3 마이그레이션 · §4 적재 CLI · §5-2 P5)"
    - "reference/2026-11-17-procedure-images/ (README.md · image-assets.csv · image-labels.csv · image-map.csv · image-validation.json · images/ — 미추적 · 읽기만)"
    - "orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/ (gitignore · 로컬 — silver/mechanism.csv · method.csv · drafts/silver-check/{silver-schema.json,silver-check.py} · gold/{silver-supplement.py,gold-build.py,gold-check.py} · notes/vocabulary.csv · glossary.md)"
    - "PROCEDURE-HUB 워크트리 phub-gold-jev (HEAD daa54e3) — backend/app/modules/gold/{silver_contract,medallion_load,inputs,db_inputs,config}.py · backend/app/model/medallion.py · backend/alembic/versions/b202611170001_medallion_tables.py · backend/tests/{test_medallion_model,test_medallion_load,test_medallion_repo,medallion_fixture}.py · .dockerignore · .gitignore"
    - "para/areas/concept/cs/artifact-traceability.md"
  related:
    - "orchestration/work/phub-gold-jev/SPEC-003-hub-gold-db.md"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md"
---

# SPEC-007 — 원리 · 방법 그림 데이터(silver → DB)

경로 접두어: `$W` = 이 폴더 · `$I` = `reference/2026-11-17-procedure-images`(그림 시드 · 읽기만) · `$SM` = `orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬) · `$H` = PROCEDURE-HUB 워크트리 `phub-gold-jev`.
「조사 1」 = `$W/research-images.md` · 「조사 2」 = `$W/research-images-v2.md` · 「보강 조사」 = `$W/research-concern-site.md` · 「지시서」 = `$W/spec-image-data-instructions.md` · 「재셈」 = 이 워커가 시드 · silver · 허브 코드를 읽어 다시 센 값(부록 B).
이 문서에는 표 · 칸 이름 · 코드 꼴 · 셈만 있다 — 그림의 글자(라벨 문장) · 사전 설명 문장 · 접속 값은 없다.

## 0. 요약

| 무엇 | 이 스펙이 정하는 것 |
|---|---|
| 목표 | **그림을 데이터로 올려 두는 데까지** — silver 에 그림 표 · 라벨 표를 더하고, 허브 DB 에 테이블 둘을 만들어 싣고, 그림 파일 103 을 PROCEDURE-HUB 레포 에셋 폴더에 둔다 |
| silver | 새 표 **2** — `concept_image`(103행 · 코드 1 = 그림 1) · `concept_image_label`(787행 · 한국어 · 언어는 칸) → silver 57 → **59** |
| 시드 → silver | 시드 CSV 둘을 읽어 silver CSV 둘을 짓는 스크립트 하나(전례 `silver-supplement.py`) · 시드 14칸 가운데 골라 싣는다 |
| DB | 테이블 74 → **76**(`s_concept_image` · `s_concept_image_label`) · SPEC-003 규칙 그대로(문자열 · 빈칸 NULL · `load_seq` · FK) · alembic revision 1 추가 |
| 해시 | 두 표는 이번 판 `kind = silver` — **`gold_hash` · `aux_hash` 의 식 · 파일 수는 그대로**. 그림 바이트는 표의 `sha256` 칸이 장마다 든다 · 묶음 해시 칸은 두지 않는다 |
| 그림 파일 | 대표 SVG 103 만 허브 레포 에셋 폴더로(별칭 83 · 미리보기 · legacy-source 는 안 옮김) · 이미지(Docker)에는 안 실린다 |
| gold | **넣지 않는다**(제안 — U7-1) · gold 15표 · `gold_hash` 불변 |
| 재빌드 | concern_site 보강(7고민 8행)과 **한 번에** — 순서 · 해시 · 37 키 대조는 §8 |
| 범위 밖 | 허브 도구 · 정적 서빙 · 바인드 마운트 실행 · 앱 화면 — §9 「다음 스펙이 읽을 자리」 |

## 1. 목적 · 범위

### 1-1. 목적

원리(`mechanism` 54) · 방법(`method` 49) 사전 103 코드에 그림이 한 장씩 생겼다(조사 2 §1). 이 그림을 **silver 의 표로 올리고 허브 DB 까지 싣는다**(_RESUME §2 11-17 :49 「그림은 DB 까지 이번 판 · 출력은 다음 스펙」). 내보내는 일(도구 · 서빙 · 화면)은 다음 스펙이다.

### 1-2. 정해진 것(다시 묻지 않는다)

| # | 정해진 것 | 근거 | 이 문서에서 |
|---|---|---|---|
| G-1 | 이번 판 = **데이터만**(silver 표 · DB 테이블 · 적재 · 그림 파일 자리). 허브 도구 · 정적 서빙 · 바인드 마운트 실행 · 앱 화면은 다음 스펙 | _RESUME §2 :49 · 지시서 「범위 밖」 | §1-3 · §9 |
| G-2 | 담는 꼴 = **새 silver 표**(그림 한 장 = 한 행) + **라벨 표** | _RESUME §2 :56 「나머지(새 그림 표 …)는 추천대로」 · 「라벨 DB 는 둠」 · 조사 2 U-1 추천 (b) | §2 |
| G-3 | 코드 1 = 그림 1 · 대표 SVG 103 · 라벨 787 | 조사 2 §1-1 · §1-3 · 재셈 ①② | §2-2 · §2-3 |
| G-4 | **의료 검수 게이트 없음** — 그림은 노출한다 · 문제가 있으면 그림만 바꾼다(판 값 · sha 로 교체 추적). 검수 값 칸은 둔다(값 「검수 전」) | _RESUME §2 :56 U-4 · 지시서 | §2-2 · §2-4 |
| G-5 | **한국어만** 쓴다 · 라벨 표는 두되 언어 칸을 둔다(이번엔 ko) | _RESUME §2 :56 U-7 · 지시서 | §2-3 |
| G-6 | 그림은 **공개 가능** · **PROCEDURE-HUB 레포 에셋 폴더가 원천** · 거기서 바인드 마운트(실행은 다음) · legacy-source(옛 JPG)는 안 옮김 | _RESUME §2 :56 U-10 · :66 | §7 |
| G-7 | 시드 칸은 **골라서** 싣는다 · `kind` 값은 표 이름(`mechanism` / `method`) · 판 값 · sha256 을 싣는다 | 조사 2 N-1 추천 (b) · 지시서 | §2-4 |
| G-8 | 별칭은 싣지 않는다 · 서빙 대상은 **대표 103 만** | 조사 2 U-2 (a) · N-2 추천 (a) · `$I/README.md:22` 「DB 에는 코드별 대표 `svg_path` 한 개를 반입」 | §2-4 · §7 |
| G-9 | 그림 판 값은 **표의 칸으로만**(빌드 기록 · `health` 에 따로 두지 않는다) | 조사 2 N-3 추천 (a) | §6 |
| G-10 | DB 테이블은 **SPEC-003 꼴**(`s_*` · 문자열 · 빈칸 NULL · FK) | 지시서 · SPEC-003 §2-1 R1 ~ R10 | §4 |
| G-11 | concern_site 보강(7고민 8행)과 **같은 재빌드 한 번** | _RESUME §2 :49 · :51 · :58 · 지시서 | §8 |
| G-12 | 서버 시드 방식 · 원천 CSV 자리 · stg gold 진입점은 **대기**(그림까지 넣은 뒤 한 번에) | _RESUME §2 :57 | §9 N7-5 |

### 1-3. 범위 · 범위 밖

| 이 스펙에서 만든다 | 범위 밖(§9) |
|---|---|
| silver 표 2 의 정의 · 시드 → silver 스크립트 · silver-check 보탬 | 허브 도구(코드 → 그림 행) · 응답 계약(SPEC-001 다음 판) |
| 허브 계약 상수 · alembic revision 1 · 적재기 보탬 · 시험 | 정적 서빙 · 바인드 마운트 실행 · 그림 폴더 env 를 허브 서버가 읽는 것 |
| 그림 파일 103 을 허브 레포 에셋 폴더에 두는 자리 · 대조 | 앱 화면(그림 자리 · 인라인 넣기 · id 겹침 처리 — 조사 2 §6) |
| 재빌드 순서(보강과 묶음) | 라벨로 SVG 글자를 가는 코드(다국어) · 영어 라벨 싣기 |

- **허브가 읽는 범위는 안 바뀐다**(SPEC-003 §5-2 P5 — gold 15 + silver 보조 5표 + 원장 확인). 새 두 표는 「올려 두기만」 하는 silver 다(SPEC-003 D-1). SPEC-001 의 도구 9 · 응답은 그대로다.
- 그림의 의료 내용이 맞는지는 이 스펙이 보지 않는다 — 시드가 「의료 검수 전 원리 개념도」 다(`$I/README.md:40`).

## 2. silver 표

### 2-1. 공통

| # | 규칙 | 근거 |
|---|---|---|
| S1 | 표 둘은 silver 의 다른 표와 같은 꼴 — UTF-8 BOM · 줄 끝 `\n` · 헤더 = 스키마 · 키 `id` · 키 형식 정규식 | `silver-check.py:263-277`(F1 ~ F3) · `:293`(F4 · F5) · 재셈 ⑥(`concern_site.csv` BOM 있음 · CRLF 0) |
| S2 | **새 층 「⑤ 매체」**(제안 — O7-1). 그림은 원장의 말이 아니라 사전 행에 붙는 매체다 — 원장 근거(`source_ref`) 규칙의 대상이 아니다 | 지금 층은 ① 사전 · ② 조합 · ③ 관계 · ④ 상품 넷(`silver-schema.json` `layers`) · ① ~ ④ 의 키 있는 표는 전부 「행 근거 ≥ 1」 검사를 받는다(`silver-check.py:453-474` D4 · D5 · C7 · E1 · O1) — 그림 행에는 가리킬 원장 자리가 없다 |
| S3 | 되짚기는 `source_ref` 가 아니라 **표 안의 값**으로 — `sha256`(그림 바이트) · `artwork_version`(판) · 시드 파일(§3) | `artifact-traceability` — 행이 원천으로 되짚혀야 한다. 그림의 원천은 그림 파일과 시드다 |
| S4 | 사전(`mechanism` · `method`)은 **고치지 않는다** — 칸 0 추가 · 행 0 변경 | 조사 2 §3-2 「검수 상태가 바뀔 때마다 사전 CSV 가 바뀐다」 를 피한다 · G-2 |

### 2-2. `concept_image` — 그림 한 장 = 한 행

| 칸 | 값 | 뜻 | 시드에서 |
|---|---|---|---|
| `id` | `CIM-0001` ~ `CIM-0103` | 행 id · 키 · 형식 `CIM-\d{4}` | 지음 — (`target_table`, `target_code`) 오름차순으로 번호(원리 54 → 방법 49) |
| `target_table` | `mechanism` 54 · `method` 49 | 붙는 사전 표(다형 참조 · 고정 값 칸) | `kind` 「원리」 → `mechanism` · 「방법」 → `method` |
| `target_code` | `MEC-…` 54 · `MET-…` 49 | 붙는 사전 행의 코드 | `code` 그대로 |
| `svg_path` | `images/mechanism/<CODE>.svg` 54 · `images/method/<CODE>.svg` 49 | 대표 그림의 경로 — **에셋 폴더(§7) 기준 상대 경로** | `svg_path` 그대로 |
| `sha256` | 64자 | 그 파일 바이트의 sha256 | `sha256` 그대로 |
| `artwork_version` | `2026-11-17-native-svg-v1` 103 | 그림 판 | `artwork_version` 그대로 |
| `medical_review` | `검수 전` 103 | 의료 검수 상태(고정 값 칸 · **게이트 아님** — G-4) | `review` 한 글자에서 의료 검수 쪽만(§2-4) |

- 키 `id` · **유일 (`target_table`, `target_code`)** — 코드 1 = 그림 1 을 표가 지킨다(재셈 ① 103 / 103 유일).
- 다형 참조 (`target_table`, `target_code`) → `mechanism` · `method` 둘. FK 는 걸지 않는다(silver 전례 15칸 — SPEC-003 §2-7). 깨진 참조 0(재셈 ① — 시드 103 코드 = silver 사전 103 코드 · 빠짐 0 · 남음 0).
- 접두어 `CIM` · `CIL`(§2-3)은 지금 silver 키 접두어 55종과 겹치지 않는다(재셈 ⑦).
- 행 수 103 · 빈칸 0.

### 2-3. `concept_image_label` — 그림 안 글자 하나 = 한 행(언어마다)

| 칸 | 값 | 뜻 | 시드에서 |
|---|---|---|---|
| `id` | `CIL-0001` ~ `CIL-0787` | 행 id · 키 · 형식 `CIL-\d{4}` | 지음 — (`image_id`, 시드의 행 순서) 순으로 번호 |
| `image_id` | `CIM-…` | 그 그림 행(FK → `concept_image`) | `code` → 그 코드의 `concept_image.id` |
| `element_id` | `label-*` 581 · `diagram-title` 103 · `diagram-desc` 103 | SVG 안 글자 요소의 id | `element_id` 그대로 |
| `i18n_key` | 787 유일 | 번역 키(SVG 의 `data-i18n`) | `i18n_key` 그대로 |
| `lang` | `ko` 787 | 언어(고정 값 칸 — 값 묶음은 `statement_translation.lang` 과 같은 「번역 언어」) | 지음 — 이번 판은 `ko` 만(G-5) |
| `text` | 글자 | 그 요소의 글자 | `ko` 칸 그대로 |

- 키 `id` · **유일 (`image_id`, `element_id`, `lang`)** · FK `image_id` → `concept_image.id`.
- 행 수 **787**(103 그림 · 그림마다 5 ~ 10행 — 재셈 ②) · 빈칸 0 · `;` · 줄바꿈 · NUL · 앞뒤 공백이 든 글자 0(재셈 ②).
- 언어를 **칸이 아니라 행**으로 둔다 — 시드는 `ko` · `en` 두 칸이지만(조사 2 §3-4 「언어를 더하면 칸이 는다 — 계약 · 마이그레이션이 언어마다」), 행으로 두면 언어가 늘어도 표 꼴이 그대로다. 영어를 싣게 되면 같은 `element_id` 에 `lang = en` 행 787 이 더해질 뿐이다(O7-4).
- 좌표 넷(`x` · `y` · `font_size` · `text_anchor`)은 싣지 않는다 — 위치의 원천은 SVG 다(`$I/README.md:9` 「좌표 · 크기 · 정렬 열은 SVG 에서 추출했으며 위치 변경의 원천은 SVG」).

### 2-4. 시드 칸 → 싣는 것 / 안 싣는 것

**`image-assets.csv` 14칸**(조사 2 §3-3 · 재셈 ①)

| 시드 칸 | 값(103행) | 처리 | 이유 |
|---|---|---|---|
| `code` | MEC 54 · MET 49 | **실음** → `target_code` | 열쇠 |
| `kind` | 「원리」 54 · 「방법」 49 | **실음(값 바꿈)** → `target_table` = `mechanism` / `method` | silver 다형 참조는 표 이름을 쓴다(G-7). 코드 접두어와 `kind` 가 어긋난 행 0(재셈 ①) |
| `svg_path` | 꼴 일치 103 | **실음** | 폴더 ↔ 표 대조의 열쇠 |
| `sha256` | 실제 파일과 일치 103 | **실음** | 그림 바이트의 지문 — 교체 추적(G-4) |
| `artwork_version` | 한 값 | **실음** | 판(G-7 · G-9) |
| `review` | 「구조·한영 렌더 확인 / 의료 검수 전」 한 값 | **쪼개 실음** → `medical_review` = `검수 전` | 한 글자에 두 사실이 섞여 있다. 의료 검수 쪽만 칸으로 · 구조 검사 쪽은 `image-validation.json` 이 묶음 전체로 든다(13 항목 `true`) |
| `name_ko` | 사전 이름 | 안 실음 | 사전과 겹친다(원천 둘) |
| `stage` | 1 · 2 · 3(37 · 33 · 33) | 안 실음 | 제작 이력 — 소비자가 쓸 일이 조사에 없다 |
| `alias_paths` | 69행에 목록(83 파일) | 안 실음 | G-8 · 한 칸에 목록 · 별칭은 대표와 같은 바이트다 |
| `width` · `height` · `background` | 1200 · 800 · transparent(한 값씩) | 안 실음 | 103행이 한 값 — 규격이다(§7-3 에 규격으로 적는다) |
| `text_count` | 5 ~ 10 | 안 실음 | 라벨 행 수와 같다(파생 — 어긋남 0) |
| `production_status` | `complete` 한 값 | 안 실음 | 제작 상태 — 시드에 들어온 것은 전부 완료다 |

**`image-labels.csv` 10칸**: `code`(→ `image_id`) · `element_id` · `i18n_key` · `ko`(→ `text` · `lang = ko`) 를 싣는다. `svg_path`(그림 행과 같은 값 — 재셈 ②) · 좌표 넷 · `en` 은 싣지 않는다.

**`image-map.csv` 는 싣지 않는다** — 103 코드의 보유 현황 · 조사 메모 표다. MEC-070 의 `메모` 에 제작 전 조사 글(옛 사진의 라이선스)이 남아 있어, 실으면 지금 그림에 표기가 필요한 것처럼 읽힌다(조사 2 U-6 꼬리 ②).

- 스크립트는 「안 실음」 칸의 값이 위 표와 달라지면(예: `review` 에 새 글자 · `production_status` ≠ `complete` · `width` ≠ 1200) **멈춘다**(§3 K4) — 한 값이라 안 실은 칸에 다른 값이 생기면 「담을 칸 없는 값」 이 되기 때문이다.
- `medical_review` 의 값 목록은 지금 `검수 전` 하나다. 다른 값(통과 · 반려 …)과 검수자 · 날짜 칸은 **정하지 않는다** — 검수 절차가 생길 때 정한다(O7-3 · G-4).

## 3. 시드 → silver 스크립트

| 항목 | 정한 것 | 근거 |
|---|---|---|
| 자리 · 이름 | `$SM/gold/silver-image.py`(이름 제안) — `silver-supplement.py` 옆 | 전례가 그 자리다(silver 보강을 스크립트로 다시 쓰기 — 조사 2 N-1 위험 칸) |
| 입력 | 시드 폴더(인자 또는 env · 기본 = `$I`) 의 `image-assets.csv` · `image-labels.csv` · `images/` + `$SM/silver/mechanism.csv` · `method.csv`(대조만) | G-7 |
| 출력 | `$SM/silver/concept_image.csv` · `concept_image_label.csv` — 이 둘만 쓴다. 다른 silver 파일의 바이트는 그대로 | S4 |
| 재현 | 다시 돌려도 **같은 바이트** · 인자로 다른 폴더를 주면 그 폴더에만 쓴다(검사가 임시 폴더에 돌려 대조) | `silver-supplement.py:4-6` 「다시 돌려도 같은 바이트」 · `gold-check.py:105-113` A3 |
| 꼴 | BOM · `\n` · 헤더 = §2-2 · §2-3 의 칸 순서 | S1 |

스크립트가 쓰기 전에 보는 것(하나라도 어긋나면 쓰지 않고 끝):

| # | 검사 |
|---|---|
| K1 | 시드 그림 표의 코드 집합 = `mechanism.code` ∪ `method.code`(103 · 빠짐 0 · 남음 0) · 코드 중복 0 |
| K2 | `kind` 가 「원리」 이면 코드가 `mechanism` 에 · 「방법」 이면 `method` 에 있다 |
| K3 | `svg_path` = `images/<mechanism\|method>/<code>.svg` 꼴 · 그 파일이 있다 · 파일 바이트의 sha256 = `sha256` 칸 |
| K4 | 「안 실음」 칸이 §2-4 의 값 그대로다(`review` 한 값 · `production_status` = `complete` · 1200 · 800 · transparent · `text_count` = 그 코드의 라벨 행 수) |
| K5 | 라벨 표의 코드 집합 = 그림 표의 코드 집합 · `svg_path` 가 그 코드의 대표 경로 · (`code`, `element_id`) 유일 · `i18n_key` 유일 · `ko` 빈칸 0 |
| K6 | 실을 글자에 `;` · 줄바꿈 · NUL 0 |

- 스크립트는 그림 파일을 **읽기만** 한다(sha256 대조). 옮기는 일은 §7 이다.
- 시드 CSV 의 오래 둘 자리(프로필 `reference/` · 허브 레포 · 그 밖)는 이 스펙이 정하지 않는다(G-12 · §9 N7-5). 이번 판은 `$I` 를 읽는다.

## 4. silver-check · 문서 · 값 목록 보탬

silver 표가 둘 늘면 아래가 **함께** 간다(하나라도 빠지면 검사가 FAIL 한다 — 그것이 맞는 동작이다).

| 무엇 | 보탤 것 | 근거 |
|---|---|---|
| `silver-schema.json` | `layers` 에 「⑤」 · `tables` 에 두 표(`layer` · `what` · `key` = `id` · `id_pattern` · `columns[]` — `concept_image.target_table` · `medical_review` · `concept_image_label.lang` 은 `vocab: true` · `image_id` 는 `fk: concept_image` · `concept_image.poly` = (`target_table`, `target_code`, [`mechanism`, `method`])) | 표 · 칸 · FK 정의는 스키마 한 벌이다(`silver-check.py:5-6`) · F1 이 「표 목록 ≠ 스키마」 를 FAIL 로 본다(`:264-265`) |
| `silver-check.py` | ① 층 ⑤ 의 표는 「행 근거 ≥ 1」 검사(D4 · D5 · C7 · E1 · O1)의 대상이 아니다 ② 새 검사 I1 ~ I5(아래) ③ 부정 시험(깨뜨린 사본)에 I 마다 하나 | `:453-474` — 지금 식은 ① ~ ④ 밖의 키 있는 표를 D5 로 보낸다(`:473` 끝 갈래) · `:1195` 부정 시험 전례 |
| `notes/silver-erd.md` · `silver-tables.md` | `--write-docs` 로 다시 쓴다(손으로 고치지 않는다) | `:1080` · `:1111` · G1 「문서 = 스키마」(`:898`) |
| `notes/vocabulary.csv` | `glossary-build.py` 로 다시 뽑는다 — 「표 이름」 묶음에 `concept_image.target_table` · 「번역 언어」 묶음에 `concept_image_label.lang` · 새 묶음 「그림 검수 상태」(`concept_image.medical_review` · 값 `검수 전`) | V3 「고정 값 칸 ⊆ 값 목록」(`silver-check.py:808-829`) · 조사 2 §3-2 「고정 값 검사」 행 |
| `notes/glossary.md` | 표 둘 · 접두어 `CIM-` · `CIL-` 의 줄 | 용어집에 표 · 접두어가 한 줄씩 있다(`glossary.md:28,30`) |
| `gold-check.py` A1 | silver 표 목록의 기대값에 새 두 파일(지금 = 고치기 전 사본 + `product_procedure` + `external_code`) | `gold-check.py:91-94` — 안 고치면 A1 이 FAIL 한다 |

새 검사(silver-check):

| # | 검사 | 등급 |
|---|---|---|
| I1 | `concept_image` 의 (`target_table`, `target_code`) 유일 · 가리킨 사전 행이 있다(R2 와 같은 식) | FAIL |
| I2 | **사전 103 코드 전부에 그림 행이 하나씩** — `mechanism` ∪ `method` 의 코드 집합 = `concept_image.target_code` 집합 | FAIL(사전에 코드가 늘면 그림이 따라와야 한다 — O7-5) |
| I3 | `svg_path` = `images/<target_table>/<target_code>.svg` · `sha256` 은 소문자 16진 64자 · `artwork_version` 빈칸 0 | FAIL |
| I4 | `concept_image_label` — (`image_id`, `element_id`, `lang`) 유일 · 그림마다 `diagram-title` · `diagram-desc` 가 언어마다 하나씩 · `text` 빈칸 0 | FAIL |
| I5 | 스크립트 재현 — `silver-image.py` 를 임시 폴더에 돌린 두 파일 = 지금 두 파일(바이트) | FAIL(시드 폴더가 없으면 건너뛰고 그렇게 적는다) |

- silver-check 는 그림 **파일**을 열지 않는다 — 파일 ↔ 표 대조는 스크립트 K3(짓는 때)와 적재기 V13(싣는 때 — §5-3)이 한다.
- `silver_sha256`(`check-stats.json` — silver 폴더 전체 해시 `:1188-1192`)은 파일이 늘어 **바뀐다**(§8).

## 5. gold

**넣지 않는다**(제안 — U7-1). gold 15표 · `gold-build.py` · `gold_hash` 는 이 스펙으로 안 바뀐다.

| 물음 | 사실 | 판단 |
|---|---|---|
| 원리 그림은 gold 행에서 닿나 | 닿는다 — `g_profile.mechanism_code`(401행 · 51 코드) = `concept_image.target_code`(조사 1 §2-2 · §2-4) | gold 에 그림 칸이 없어도 코드 한 번의 찾기다 |
| 방법 그림은 | gold 에 방법 **코드가 없다** — `g_profile.methods` 는 이름을 ` · ` 로 이은 글자(159행 · 39 이름). 이름 → 코드는 `g_entry` 의 method 입구(131행 · 이름 중복 0)로 닿는다(조사 1 §2-2) | 이름 맞춤으로 닿는다 — 허브가 속성 조회에서 이미 쓰는 길이다 |
| gold 에 넣으면 | `g_profile` 에 칸(`method_codes` · 그림 경로 …)이 늘어 헤더 27 → · `gold_hash` · 헤더 계약 · gold-check · 37 답 키가 함께 바뀐다(조사 1 §2-4 · §3-2) | 값이 얻는 것은 「방법 코드를 행 옆에」 하나인데 바뀌는 것은 gold 전체 판이다 |
| gold 가 안 가리키는 코드 | 어느 시술도 안 가리키는 원리 3 · 어느 케이스 · 제품도 안 가리키는 방법 10 — 그림은 있고 gold 행으로는 안 닿는 코드 13(조사 1 §2-1) | gold 에 넣어도 이 13 은 못 싣는다 — 그림 표가 silver 에 따로 있어야 103 이 다 산다 |

- 방법 코드를 gold 행에 둘지는 **출력 스펙이 응답 꼴을 정할 때** 다시 본다(§9 N7-2). 그때도 그림 표는 silver 에 그대로 있고 gold 는 코드만 든다.

## 6. DB · 적재 · 해시

### 6-1. 테이블

SPEC-003 §2-1 R1 ~ R10 을 그대로 따른다 — 여기에는 **늘어나는 것만** 적는다.

| 테이블 | 행 | CSV 칸 | PK | 유일 제약 | FK 칸(→ 대상) | 다형 칸 |
|---|---:|---:|---|---|---|---|
| `s_concept_image` | 103 | 7 | `id` | (`target_table`, `target_code`) | — | `target_table` |
| `s_concept_image_label` | 787 | 6 | `id` | (`image_id`, `element_id`, `lang`) | `image_id` → `s_concept_image` | — |

| 셈 | SPEC-003(지금) | 이 스펙 뒤 | 늘어난 것 |
|---|---:|---:|---|
| 테이블 | 74 | **76** | silver 57 → 59 |
| CSV 칸 | 665 | 678 | 7 + 6 |
| `load_seq` | 72 | 74 | 2 |
| 테이블 칸 | 749 | 764 | 13 + 2 |
| FK | 82 | **83** | `image_id` 1(silver 80 → 81) |
| 다형 칸 | silver 15(14표) | 16(15표) | `concept_image.target_table` |
| 유일 제약 | 3 | **5** | 2 |
| 직접 지은 인덱스 | 30 | 30 | 0 — 유일 제약의 앞 칸이 색인 노릇을 한다(SPEC-003 §2-8 `g_profile` · `g_evidence` 와 같은 꼴) |
| 빌드 기록 행 | 74 | **76** | 두 CSV(`kind = silver`) |
| `public` 테이블 | 241 | 243 | |

- 칸은 전부 `TEXT` · 빈칸 = NULL(R2 · R3) — 두 표는 빈칸이 0 이라 NULL 도 0 이다. NOT NULL 은 PK · 유일 제약 칸에만(R6) → `s_concept_image` 의 `id` · `target_table` · `target_code` · `s_concept_image_label` 의 `id` · `image_id` · `element_id` · `lang`.
- 이름 — `fk_s_concept_image_label_image_id_s_concept_image` 49자 · `uq_s_concept_image__target_table_target_code` 44자 · `uq_s_concept_image_label__image_id_element_id_lang` 50자(≤ 63 · 재셈 ⑦). 기존 167 · 지금 74 와 겹치는 이름 0(재셈 ⑦ — 기존에 `concept` 가 든 이름은 `catalog_procedure_concept` 하나이고 접두어 `s_` 가 아니다).
- FK 는 `DEFERRABLE INITIALLY DEFERRED`(SPEC-003 §2-6 — WORK-010 에서 확인된 꼴 · `$H/backend/app/model/medallion.py:27`).
- 기존 167 로 가는 FK 0 · gold → 새 표 FK 0(R10).

### 6-2. 계약 상수 · 모델 · 마이그레이션

| 무엇 | 정한 것 | 근거 |
|---|---|---|
| 계약 상수 | `silver_contract.py` 의 `SILVER_HEADERS` · `SILVER_KEY` 에 두 표 · `SILVER_FK` 에 `concept_image_label.image_id` · `SILVER_POLY` 에 `concept_image.target_table` | 모델 · 적재기 · 시험이 이 상수 하나를 읽는다(`$H/backend/app/modules/gold/silver_contract.py:1-6` · `model/medallion.py:84-106`) |
| 모델 | `SILVER_UNIQUES` 에 두 표의 유일 묶음 — 그 밖의 모델 코드는 상수에서 기계로 지어지므로 손대지 않는다 | `model/medallion.py:49` |
| 마이그레이션 | **새 revision 1**(id 제안 `b202611170002` · `down_revision = b202611170001`) — 테이블 2 · FK 1 · 유일 제약 2 를 만든다(schema 만). 풀어 쓴 고정본 · 앱 상수 import 0 | SPEC-003 §3-2 「표가 바뀌면 계약 상수 + 새 revision 이 함께」 · `b202611170001` 은 그 시점의 고정본이라 고치지 않는다(`model/medallion.py:5`) |
| downgrade | 두 테이블을 지운다(라벨 → 그림 순) | 허브 관례 |
| 깨지지 않는 조건 | SPEC-003 §3-3 C1 ~ C7 그대로 — `alembic check` · SQLite `create_all` · 이름 길이 · `ruff` | |

- revision id 는 옛 브랜치 3개(`b202610260001` · `b202610300001` · `b202610310001`)와 겹치지 않는다(SPEC-003 D-9). 구현 날이 바뀌면 그날 값으로 짓는다(O7-6).
- 허브 HEAD 는 지금 `daa54e3`(DB 판)이다. 이 스펙의 구현은 **진행 중인 0.7.x 구현이 끝난 HEAD 위**에서 한다(_RESUME §2 :58 「코드 구현 끝난 뒤」) — 0.7.x 는 새 입력 · 새 테이블이 없으므로(조사 2 §4) revision 줄은 겹치지 않는다.

### 6-3. 적재기

| 무엇 | 정한 것 | 근거 |
|---|---|---|
| 싣는 법 | 지금 그대로 — 두 표는 silver 폴더의 CSV 로 들어와 `kind = silver` 로 실린다. 적재기 본문은 계약 상수를 따라가므로 **표를 가리는 코드는 0** | `medallion_load.py:106-134`(specs 를 돌며 읽는다) |
| V2 · V3 · V5 | 그대로 — 두 CSV 가 없으면 V2 · 계약에 없는 CSV 가 있으면 V3 · 헤더가 다르면 V5 로 exit 2. **계약 상수 · 마이그레이션이 CSV 보다 먼저** 가야 한다(순서 §8) | `:116-121` · `:130` |
| V6 · V7 | 그대로 — PK · 유일 묶음 2 · FK `image_id` 가 새로 검사에 든다 | `:174-203` |
| V10 | 다형 칸이 15 → 16 — `s_concept_image.target_table` 의 못 찾은 수가 요약에 한 줄 는다(기대 0) | `:206-219` |
| **V13(새)** | 그림 폴더 env `GOLD_IMAGE_DIR`(새 · 이름 제안)이 있으면 — `s_concept_image` 행마다 `<폴더>/<svg_path>` 파일이 있고 sha256 = `sha256` 칸 · 폴더의 `images/**/*.svg` 가 표의 경로 103 과 정확히 같다(더 있는 파일 0). 어긋나면 exit 2(DB 에 쓴 것 0). env 가 없으면 **건너뛰고 요약에 그렇게 찍는다**(막지 않는다) | 조사 1 §5-3 ⑤ 「폴더 ↔ 표 대조는 누가 세지 않으면 모른다 — 셀 자리는 적재기」 · 조사 2 N-2 위험 칸 「표의 `sha256` 대조가 그 틈을 메운다」 |
| 요약 | `image_files 103 checked` 또는 `image_files unchecked(GOLD_IMAGE_DIR 없음)` 한 줄 · 글자 값은 찍지 않는다 | `medallion_load.py:10`(출력에는 이름 · 수 · 해시만) |
| 박힌 수 | 적재기 · 시험에 「74」 · 「57」 · 「52」 · 「72」 · 「15」 로 박힌 자리를 **grep 으로 전부** 찾아 고친다(부록 B ⑧ 이 지금 찾은 목록 — 목록이 아니라 grep 이 기준이다) | `medallion_load.py:68,380` · `tests/test_medallion_{model,load,repo}.py` · `tests/medallion_fixture.py` |
| `LOADER_VERSION` | 올린다(`load_medallion 0.2.0` 제안) | `:36` — 빌드 기록에 판으로 남는다 |

- `GOLD_IMAGE_DIR` 는 **적재기만** 읽는다. 허브 서버(`gold_main`)는 이 env 를 읽지 않고 그림을 내지 않는다 — 다음 스펙이다(G-1).
- DB 판 repository 의 읽는 범위(P5)는 그대로다 — 새 두 표를 읽지 않는다(`db_inputs.py:7` 의 「나머지 silver 52표」 가 54표가 된다).

### 6-4. 해시

| 물음 | 정한 것 | 근거 |
|---|---|---|
| 그림 표가 `aux` 에 드나 | **이번 판은 안 든다** — 두 표는 `kind = silver`(제안 — U7-2). `aux_hash` 의 식 · 파일 6 은 그대로 · `health.files[]` 는 22줄 그대로 | `aux` 는 「허브가 읽는 보조 입력」 이다(SPEC-003 §2-5 · `inputs.py:129-178`). 이번 판에 허브는 그림 표를 읽지 않는다(§1-3) — 안 읽는 표를 `aux` 에 넣으면 응답이 안 바뀌는데 build 값 · cursor 만 바뀐다 |
| 다음 스펙에서는 | 허브 도구가 그림 행을 **응답으로 내는 판**에서 두 표(또는 그림 표)를 `aux` 로 올린다 — 그때 `aux` 6 → 7(또는 8) · `health.files[]` 가 는다 | 조사 1 §3-3 「`aux` 로 넣지 않으면 응답은 바뀌는데 build 값은 같은 판이 생긴다」 · 조사 2 §3-2 해시 행 |
| 그림 파일 묶음 해시를 어디에 | **따로 두지 않는다.** 장마다의 지문은 `s_concept_image.sha256`(103행) · 그 CSV 한 파일의 sha256 은 빌드 기록 한 줄(`concept_image.csv` · `kind = silver`)이다. 그림 한 장이 바뀌면 → 시드 `sha256` → silver CSV 바이트 → 빌드 기록의 그 줄이 차례로 바뀐다 | 조사 1 §5-3 ⑤ 요약 (가) · G-9. 묶음 해시 칸을 더하면 빌드 기록의 판 값이 넷 → 다섯이 되고 SPEC-003 §2-5 · F3 이 함께 바뀐다 |
| 그림 판 | `s_concept_image.artwork_version` 칸으로만 | G-9 |
| `gold_hash` | 이 스펙으로 **안 바뀐다**(gold 불변 — §5) | |

- 그림을 바꾸는 절차(G-4 「문제 있으면 그림만 바꿈」)는 그래서 한 줄기다 — 에셋 폴더의 파일 교체 → 시드의 `sha256`(· 판을 올리면 `artwork_version`) → `silver-image.py` → silver-check → 적재(V13 이 폴더와 표를 대조). 사전 · gold 는 안 바뀐다.

## 7. 그림 파일 — PROCEDURE-HUB 에셋 폴더

### 7-1. 자리

| 항목 | 정한 것(제안 — U7-3) | 근거 |
|---|---|---|
| 폴더 | 허브 레포 루트의 `assets/procedure-images/`(이름 제안) — 그 아래 `images/mechanism/<CODE>.svg` 54 · `images/method/<CODE>.svg` 49 | G-6 「PROCEDURE-HUB 레포 에셋 폴더가 원천」. `svg_path` 값(`images/…`)이 이 폴더 기준 상대 경로 그대로다 — 값을 바꾸지 않는다 |
| 이미지(Docker)에 안 실림 | 루트 `assets/` 는 build context 에 들지 않는다 — `.dockerignore` 가 `**` 로 전부 막고 `backend/` 의 몇 자리만 연다 | `$H/.dockerignore`(전문 14줄) · 조사 1 §5-3 ④. **`backend/app/` 아래에 두면 한 줄도 안 고치고 이미지에 실린다** — 그 자리는 피한다(G-6 은 바인드 마운트다) |
| 함께 두는 것 | `README.md` 하나 — 판 값 · 규격(§7-3) · 「의료 검수 전 원리 개념도」 · 파일 수 103 · 대조 방법(V13) | `$I/README.md:40` |
| 안 옮기는 것 | 별칭 83 · `previews/` · `legacy-source/` · 제작 지시(`codex-prompts.*`) · `media-coverage-survey.md` · `image-map.csv` · `.gitkeep` · `.DS_Store` | G-6 · G-8 · 조사 2 N-2 「통째면 옛 JPG · 미리보기 · 제작 지시가 정적 경로로 나간다」 |
| 시드 CSV 둘 | **이번 판에 옮기지 않는다** — 원천 CSV 자리는 대기다 | G-12 |

- 크기: 대표 103 = **6,886,445 바이트**(재셈 ① · 조사 2 §1-1 과 같다).
- 허브 레포 `.gitignore` 는 `.DS_Store` 를 이미 막는다(`$H/.gitignore`) — 그림 폴더를 막는 줄은 없다.
- 프로필 레포의 `$I` 는 지금 **미추적이고 gitignore 에 없다**(재셈 ⑨). 이 스펙은 `$I` 를 커밋 대상으로 만들지 않는다 — 마감 때 미추적 파일을 함께 넣는 관례와 부딪히는 자리다(O7-7 · `legacy-source/` 의 옛 사진은 저작자 · 출처 주소가 그 폴더에 없다 — 조사 2 U-10).

### 7-2. 옮긴 뒤 대조

| # | 대조 | 누가 |
|---|---|---|
| A1 | 에셋 폴더의 SVG = 103 · 이름 = `(MEC\|MET)-\d{3}\.svg` · `mechanism/` 54 · `method/` 49 · 그 밖의 파일 0(README 제외) | 허브 시험(CI 에서 돈다 — 레포 안 파일만 본다) |
| A2 | 파일마다 sha256 = `concept_image.sha256` | 적재기 V13(로컬 실물 — silver CSV 가 있어야 한다) |
| A3 | 103 파일에 `<script` · `<image` · `<style` · `<foreignObject` · 바깥 주소 참조 0(이름공간 선언 `xmlns` 는 뺀다) · `viewBox="0 0 1200 800"` 103 | 허브 시험(A1 과 같은 자리) — 재셈 ③ 이 지금 값(전부 0 · 103) |

- A3 은 **다음 스펙이 SVG 를 화면에 넣을 때 기대는 바닥**이다(조사 2 §6-2 「인라인의 안전 — 적재 때 다시 검사하지 않으면 보장 없음」). 지금 걸어 두면 그림이 바뀔 때 CI 가 본다.

### 7-3. 규격(표에 안 실은 한 값들)

1200 × 800 · 배경 투명 · native vector(래스터 · 스크립트 · 외부 참조 없음) · 글자는 `<text>`(윤곽선 아님) · 루트 `lang="ko"` · 글자 요소마다 `id` 와 `data-i18n`(`$I/README.md:30` · 조사 2 §1-2). 이 값들은 §2-4 에서 「안 실음」 으로 둔 칸의 값이다 — 에셋 폴더 README 에 적어 둔다.

## 8. 재빌드 한 번 — concern_site 보강과 묶음

둘은 **같은 재빌드 한 번**에 들어간다(G-11). 보강의 내용(7고민 8행 · 근거 경로)은 보강 조사 §4 · §6 이 정본이고 여기에 다시 적지 않는다.

### 8-1. 순서

| # | 단계 | 무엇 | 실패하면 |
|---|---|---|---|
| 1 | 사본 | 지금 `$SM/silver` 를 `$SM/archive/` 에 사본으로(전례 — `archive/silver-before-*` 21 폴더) | — |
| 2 | 보강 | `concern_site.csv` 에 8행(95 → 103 · `CSI-0099` 부터) · `source_ref.csv` 에 그 근거 행 | — |
| 3 | 그림 | `silver-image.py` → `concept_image.csv` 103 · `concept_image_label.csv` 787 | K1 ~ K6 에서 멈춤 |
| 4 | 스키마 · 값 목록 · 문서 | §4 의 여섯(스키마 · silver-check · `--write-docs` · vocabulary · glossary · gold-check A1) — 보강 쪽 A1 목록(덧붙인 `source_ref` 행 · `concern_site` 변경)도 여기서 | — |
| 5 | silver-check | PASS(WARN 0) · I1 ~ I5 | 멈춤 — silver 를 고친다 |
| 6 | gold | `gold-build.py` → `gold-check.py` PASS · **`gold_hash` 가 지금 값과 같은지** 본다 | 다르면 멈춤 — 왜 바뀌었는지부터(아래) |
| 7 | 허브 스키마 | 계약 상수 · 모델 · 새 revision(§6-2) → 로컬 DB 에 `alembic upgrade head` · `alembic check` | 멈춤 |
| 8 | 그림 파일 | 대표 103 을 허브 에셋 폴더로(§7) · A1 · A3 | 멈춤 |
| 9 | 적재 | `--dry-run`(V1 ~ V13 · 요약) → 적재 | exit 2 = DB 그대로 · exit 3 = 롤백 |
| 10 | 허브 | 재시작 → `health` 의 `gold_hash` · `aux_hash` 확인 | — |
| 11 | 대조 | 앱 37 키 대조 (나) | — |

- **7 이 9 보다 먼저다** — 계약에 없는 CSV 가 silver 폴더에 있으면 적재기 V3 이 exit 2 로 막는다(SPEC-003 §4-3). 3 을 한 뒤 7 을 하기 전에는 **지금 떠 있는 허브 · 적재기로 다시 싣지 않는다**.
- 2 와 3 은 서로 다른 파일을 쓴다(보강 = `concern_site` · `source_ref` / 그림 = 새 두 파일) — 순서를 바꿔도 결과 바이트가 같다. 사본(1)은 둘보다 앞이어야 한다.
- 떠 있는 CSV 판 허브(`GOLD_REPOSITORY=csv`)는 silver 폴더에서 보조 5 파일만 이름으로 읽는다(`inputs.py:129-161`) — 새 두 CSV 가 폴더에 생겨도 CSV 판은 그대로 뜬다.

### 8-2. 해시 · 37 키 — 무엇이 바뀌나

| 값 | 바뀌나 | 왜 |
|---|---|---|
| `gold_hash` | **안 바뀐다(기대)** | gold 는 그림 표를 안 읽는다(§5) · `gold-build.py` 는 `concern_site` 도 안 읽는다(재셈 ⑤ — 본문에 그 표 이름 0). 6 에서 실제로 확인한다 — 다르면 보강의 `source_ref` 덧붙임이 gold 근거(`g_evidence`)에 닿았다는 뜻이라 멈춘다 |
| `aux_hash` | **바뀐다** | 보강 때문이다 — `concern_site.csv` · `source_ref.csv` 가 보조 입력이다(SPEC-003 §2-5). **그림 때문에는 안 바뀐다**(§6-4) |
| `GOLD_EXPECTED_HASH` | 그대로 | `gold_hash` 만 대조한다(`inputs.py:179-183`) |
| silver 폴더 전체 해시(`check-stats.json`) | 바뀐다 | 파일 2 추가 + 보강 2 파일 |
| 빌드 기록 | 74 → 76행 · `built_at` · `loader_version` · `aux_hash` 값 | |
| 37 답 키의 **행** | **안 바뀐다(기대)** | 37 문항 가운데 부위를 건 고민 조회 0(보강 조사 §5-3) · 그림 표는 도구가 안 읽는다 |
| 37 답 키의 `build.aux_hash` | 바뀐다 | 위 `aux_hash` — 대조는 「`aux_hash` 를 빼고 같다」 로 보고, 기준 키를 다시 뽑는 일은 보강 쪽 WORK 가 한다 |

- 그림만 따로 보면 **응답에 닿는 값은 하나도 안 바뀐다** — `gold_hash` · `aux_hash` · 도구 응답 · 37 키 전부 그대로다. 묶어서 한 번에 가는 까닭은 재적재 · 재시작 · 대조가 한 번이면 되기 때문이다(_RESUME §2 :58).

## 9. 다음 스펙이 읽을 자리

이번에 만들지 않는다. 정해진 것은 「정해짐」 으로, 나머지는 남은 질문으로 적는다.

| # | 무엇 | 지금 아는 것 | 이 스펙이 남겨 두는 것 |
|---|---|---|---|
| N7-1 | **허브 도구** — 코드 → 그림 행 | 방향은 정해짐: 새 도구 하나(_RESUME §2 :56 「새 도구」 · 조사 1 U-8 (b)). 도구 9 → 10 · 기존 응답 불변 | `s_concept_image` 7칸이 응답 행의 재료다(코드 · 경로 · sha256 · 판 · 검수 상태). 그때 두 표를 `aux` 로 올린다(§6-4) · DB 판 읽는 범위 P5 에 더한다 |
| N7-2 | 방법 그림을 행 옆에 붙이는 길 | gold 에 방법 코드가 없다(§5) — 이름 → `g_entry` 로 맞추나 · `g_profile` 에 코드 칸을 더하나 | 그림 표는 어느 쪽에도 그대로 쓰인다 |
| N7-3 | **정적 서빙 · 바인드 마운트** | 방향은 정해짐: 에셋 폴더를 읽기 전용으로 마운트 · 로컬 = 레포 폴더 경로 · 서버 = VM 디렉터리(_RESUME §2 :56 · :66). 허브에 정적 서빙 코드 0 · stg 서빙 컨테이너는 「기존 mounts 없음」 을 확인한다(조사 1 §5-3 ① ③) | 에셋 폴더(§7-1)가 마운트의 원본 · `svg_path` 가 그 폴더 기준 상대 경로 · A3 이 안전 바닥 · `GOLD_IMAGE_DIR` 이름을 서버 env 로 이어 쓸 수 있다 |
| N7-4 | **앱 화면** — 그림 자리 · 넣는 법 | 방향은 정해짐: 원리 · 방법을 물은 턴에만(_RESUME §2 :56 「물은 턴에만 화면」). 인라인이면 id 54종이 파일 사이에 겹친다 · 참조되는 겹친 정의 13종은 글자가 같다 · `<img>` 면 화면 폰트가 안 먹는다(조사 2 §6-2) | `s_concept_image_label` 의 `element_id` · `i18n_key` 가 글자 요소를 지목한다 · `medical_review` 는 값으로만 있다(게이트 아님 — G-4) |
| N7-5 | 원천 CSV · 시드 CSV 의 자리 · 서버 시드 방식 · stg gold 진입점 | 대기(G-12) — 코디 추천은 「원천 CSV 를 허브 레포로 · VM 디렉터리 + 일회성 적재 컨테이너」(_RESUME §2 :57) | 시드 → silver 스크립트가 시드 폴더를 인자로 받는다(§3) — 자리가 정해지면 인자만 바뀐다 |
| N7-6 | 다국어 그림 | 이번엔 한국어만(G-5). 시드에 영어 초안 787 이 있다 · silver 번역 표는 4 언어다(조사 2 U-7) | 라벨 표가 언어를 행으로 든다(§2-3) — 영어는 행 추가 · 표 꼴 불변 |
| N7-7 | 의료 검수 절차 | 게이트 없음(G-4). 검수자 · 날짜 · 값 목록은 원천 어디에도 없다(조사 2 §1-4) | `medical_review` 칸 하나(값 `검수 전`) |

## 10. 시험 · 완료 조건

번호는 SPEC-003 의 `DT` · `DE` 와 겹치지 않게 `IT`(허브 단위 · 합성 · SQLite — CI) · `IE`(로컬 실물)로 단다. **그 WP 의 시험만** 돌리고 전체 검증은 끝에 한 번이다.

### 10-1. silver 쪽(로컬 — `$SM`)

| # | 시험 | 기대 |
|---|---|---|
| IS1 | `silver-image.py` | 두 파일 생성 · 103 · 787행 · 다시 돌려 같은 바이트 · 다른 silver 57 파일 바이트 불변 |
| IS2 | 깨뜨린 시드(K1 ~ K6 을 하나씩 — 레포 밖 임시 폴더) | 쓰지 않고 끝 |
| IS3 | silver-check | PASS · WARN 0 · I1 ~ I5 · 부정 시험에서 I 마다 FAIL · 문서(`silver-erd.md` · `silver-tables.md`) = 스키마 |
| IS4 | gold-check | PASS · `gold_hash` 불변(§8-2) |

### 10-2. 허브 단위(IT)

| # | 시험 | 기대 |
|---|---|---|
| IT1 | 모델 = 계약 | 새 테이블 2 · 합 76 · silver 59 · 칸 764 · FK 83 · 유일 제약 5 · 인덱스 30 · 이름 길이 ≤ 63 · 중복 0(SPEC-003 DT1 의 수가 §6-1 로 바뀐다) |
| IT2 | SQLite · revision | `create_all` 성공 · 새 revision 의 `down_revision` = `b202611170001` · 헤드 하나 · 옛 3 id 와 다름 · 새 revision 파일에 `create_table` 2 · 지연 FK 1 |
| IT3 | 적재(합성) | 합성 fixture 에 두 표(가짜 코드 · 가짜 글자)를 더해 SQLite 에 싣는다 → 행 수 · `load_seq` · 되읽기 대조 · 빌드 기록 76행(`silver` 52 → 54) |
| IT4 | 적재 검사 실패 | 두 표에서 — CSV 빠짐(V2) · 헤더 바뀜(V5) · 유일 묶음 중복(V6) · 없는 `image_id`(V7) → exit 2 · DB 에 쓴 것 0 |
| IT5 | V13 | 합성 그림 폴더로 — 일치 = 통과 · 한 파일 바이트 바꿈 · 한 파일 빠짐 · 표에 없는 SVG 하나 더 → 각각 exit 2 · env 없음 = 건너뛰고 요약에 `unchecked` |
| IT6 | 읽는 범위 불변 | DB 판 repository 가 새 두 표를 읽지 않는다(SPEC-003 DT15 그대로) · `health.files[]` 22줄 · 도구 9 응답이 이 변경 전과 같다(기존 합성 도구 시험 통과) |
| IT7 | 에셋 폴더 | §7-2 A1 · A3 |

- fixture 에 실제 라벨 글자 · 실제 그림을 넣지 않는다(SPEC-003 §7-1 끝 줄과 같다).

### 10-3. 로컬 실물(IE)

| # | 시험 | 기대 |
|---|---|---|
| IE1 | 빈 DB | 새 빈 PostgreSQL 에 `alembic upgrade head` → `alembic check` 통과 · `public` 243 · `downgrade -1` → `upgrade head` 다시 됨 |
| IE2 | dry-run | 74표 통과 · `s_concept_image` 103 · `s_concept_image_label` 787 · `poly_unresolved s_concept_image.target_table 0` · `image_files 103 checked` · `gold_hash` = 지금 값 |
| IE3 | 적재 | exit 0 · 76 테이블 · 되읽기 대조 차이 0 · FK 위반 0 · 빌드 기록 76행 |
| IE4 | SQL 한 줄 대조 | `s_concept_image` 의 `target_code` 집합 = `s_mechanism.code` ∪ `s_method.code`(103) · 라벨이 없는 그림 0 · 그림이 없는 라벨 0 |
| IE5 | 허브 | DB 판 재시작 → `health` 의 `gold_hash` 불변 · `aux_hash` = 보강 뒤 값 · `files[]` 22줄 |
| IE6 | **37 키 대조 (나)** | 행 37 / 37 같음(`build.aux_hash` 만 다름 — §8-2) |

### 10-4. 완료 조건

1. IS1 ~ IS4 · IT1 ~ IT7 통과 · `ruff` · 기존 시험 전부 통과.
2. IE1 ~ IE6 통과.
3. 허브 레포에 silver CSV · 시드 CSV · dump · 접속 값이 들어가지 않았다(공개 금지 grep) · 에셋 폴더에는 SVG 103 + README 만.
4. 재셈이 맞는다 — 103 · 787 · sha256 103 일치(부록 B ① ②).

허브 브랜치의 push · PR · 머지 · 로컬 DB · 서버 띄우기는 완료 조건이 아니다 — 코디네이터 · 별도 승인이다(SPEC-003 §6 · §7-3).

## 11. 열린 것

### 11-1. WORK 전 사용자 결정(셋)

「추천으로」 한 마디면 본문 그대로 닫힌다. §1-2 의 「정해진 것」 은 여기 다시 올리지 않았다.

| # | 정할 것 | 선택지 | 추천 | 근거 · 셈 |
|---|---|---|---|---|
| **U7-1** | **gold 에 그림을 넣나** | (a) 안 넣는다 — gold 15표 · `gold_hash` 불변(본문) (b) `g_profile` 에 방법 코드 칸(`method_codes`)만 더한다 (c) 그림 경로까지 gold 행에 | **(a)** | 원리는 `g_profile.mechanism_code` 로 이미 닿고(401행 · 51 코드) 방법은 이름 → `g_entry` 로 닿는다(§5). (b) · (c) 는 `gold_hash` · 헤더 계약 · gold-check · 37 답 키가 함께 바뀌고, gold 가 안 가리키는 코드 13 은 어차피 못 싣는다. 방법 코드를 행 옆에 둘지는 출력 스펙이 응답 꼴을 정할 때(N7-2) |
| **U7-2** | **그림 표를 이번 판에 `aux`(허브 보조 입력)로 올리나** | (a) 이번엔 `silver` — `aux_hash` 식 · `health.files[]` 22줄 그대로 · 도구 스펙에서 올린다(본문) (b) 지금 `aux` 로 — `aux` 6 → 8 · `health` 24줄 · DB 판 읽는 범위에 두 표 | **(a)** | 이번 판에 허브는 그림을 읽지도 내지도 않는다(G-1). (b) 는 응답이 안 바뀌는데 `aux_hash` · cursor 의 build 값 · `health` 시험 5곳(22 를 박은 자리 — 부록 B ⑧)이 바뀌고, 그 값은 도구 스펙에서 어차피 한 번 더 바뀐다 |
| **U7-3** | **에셋 폴더의 자리 · 이름** | (a) 허브 레포 루트 `assets/procedure-images/images/{mechanism,method}/`(본문) (b) `backend/` 아래(예: `backend/assets/…`) (c) `docs/assets/` 아래 | **(a)** | 루트 `assets/` 는 `.dockerignore` 가 막아 이미지에 안 실리고(G-6), `svg_path` 값이 그대로 상대 경로가 된다. (b) 도 지금 `.dockerignore` 로는 안 실리지만 `backend/app/` 과 한 폴더 차이라 실수로 실리기 쉽다. (c) 는 문서 사이트(mkdocs) 폴더라 문서 빌드에 딸려 나간다 |

### 11-2. 열린 것

「추천」 은 이 워커의 추천이고 결정이 아니다.

| # | 열린 것 | 선택지 | 추천 | 상태 |
|---|---|---|---|---|
| O7-1 | 새 두 표의 **층** · 원장 근거 규칙 | (a) 새 층 「⑤ 매체」 — 행 근거 검사 대상 아님(본문) (b) 층 ① 에 두고 그림 행마다 `source_ref` 에 「사용자 제공」 근거 한 줄(값 목록에 자리만 열려 있고 지금 0행 — `vocabulary.csv:277`) | **(a)** — (b) 는 `source_ref` 에 103(라벨까지면 890)행이 늘고 `aux_hash` 가 그림 때문에도 바뀌며, 「사용자 …」 근거를 해석하는 식(S1)을 처음 쓰게 된다. 그림의 되짚기는 sha256 · 판 값이 이미 한다(S3) | 구현 때 정함(본문 = (a)) |
| O7-2 | 그림 표의 **키** | (a) `id`(`CIM-…`) + 유일 (`target_table`, `target_code`)(본문 — silver 다형 표 전례) (b) 사전 코드를 그대로 키로(`code` = `MEC-…` / `MET-…`) · 라벨은 `image_code` | **(a)** — silver 의 다형 표는 전부 `id` + (`target_table`, `target_code`) 꼴이고 허브 계약 · silver-check 가 그 꼴을 안다. (b) 는 지어낸 id 가 없어 더 짧지만 키 형식 정규식이 두 접두어를 받아야 하고 `code` 가 「자기 코드」 가 아닌 첫 표가 된다 | 구현 때 정함 |
| O7-3 | `medical_review` 의 값 목록 · 검수자 · 날짜 칸 | 지금은 `검수 전` 하나 · 칸 추가 없음(본문) / 값 셋(검수 전 · 통과 · 반려) + 칸 | 본문 — 검수 절차가 없다(G-4 · 조사 2 U-4 「원천 질문」). 값이 생기면 값 목록 한 줄 · 칸이 필요하면 표 변경(새 revision) | 검수 절차가 생길 때 |
| O7-4 | 영어 라벨 787 을 지금 싣나 | 안 싣는다(본문 — `ko` 787) / `lang = en` 787 도 싣는다(1,574행) | 안 싣는다 — 「한국어만」(G-5) · 시드가 「영어 초안」 이라 적었다(`$I/README.md:28`). 표 꼴은 그대로라 뒤에 행만 더한다 | 다국어 범위가 열릴 때 |
| O7-5 | I2(사전 103 코드 전부에 그림 하나)를 FAIL 로 두나 | FAIL(본문) / WARN | FAIL — 지금 103 / 103 이고 「코드 1 = 그림 1」 이 정해진 꼴이다(G-3). 사전에 코드가 늘어 그림이 아직 없을 때는 그때 WARN 으로 내릴지 정한다 | 구현 때 정함 |
| O7-6 | 이름 — 표 `concept_image` · `concept_image_label` · 접두어 `CIM` · `CIL` · 칸 `medical_review` · 스크립트 `silver-image.py` · env `GOLD_IMAGE_DIR` · revision id `b202611170002` · 에셋 폴더 `assets/procedure-images` · `LOADER_VERSION` | 본문 제안 / 다른 이름 | 본문 그대로 — silver 표 57 · 접두어 55 · 허브 테이블 241 · 옛 revision 3 과 겹침 0(재셈 ⑦). `concept_image` 는 조사 1 §3-2 의 이름 제안이다 | 구현 때 정함 |
| O7-7 | 프로필 레포의 `$I`(미추적 · gitignore 아님 · 18MB) | (a) 원천이 허브 에셋 폴더로 간 뒤 프로필에서는 gitignore (b) 프로필에도 커밋(공개 가능 — G-6) (c) 지운다 | 코디 판단 — 이 스펙의 allowed_paths 밖이다. 사실만: `legacy-source/` 의 옛 사진은 CC BY-SA 4.0 인데 저작자 · 출처 주소가 그 폴더에 없다(조사 2 U-10) · 별칭 83 · 미리보기까지 통째면 18MB 다 | 마감 전 코디 |
| O7-8 | V13 을 env 없을 때 건너뛰나 | 건너뛰고 찍는다(본문) / env 필수 — 없으면 exit 2 | 본문 — CI 의 합성 적재(IT3)와 그림 폴더 없는 환경에서 적재기가 그대로 돈다. 실물 절차(§8-1 9)에서는 env 를 준다(IE2 가 `checked` 를 본다) | 구현 때 정함 |

## 부록 A. 결정 → 본문

| 결정 행 | 문서:줄 | 본문 |
|---|---|---|
| 그림은 DB 까지 이번 판 · 출력은 다음 스펙 · 재빌드 한 번 | `$W/_RESUME.md:49` | §1-2 G-1 · G-11 · §8 · §9 |
| U-4 검수 게이트 없음 · 판 값 · sha 로 교체 추적 | `$W/_RESUME.md:56` | G-4 · §2-2 `medical_review` · §6-4 끝 |
| U-7 한국어만 · 라벨 DB 는 둠 | `$W/_RESUME.md:56` | G-5 · §2-3 |
| U-10 공개 가능 · PROCEDURE-HUB 에셋 폴더가 원천 · 바인드 마운트 · legacy-source 안 옮김 | `$W/_RESUME.md:56` | G-6 · §7 · N7-3 |
| 나머지 추천대로(새 그림 표 · 시드 칸 골라서 · 대표 103 만 · 새 도구 · 물은 턴에만) | `$W/_RESUME.md:56` · `$W/research-images-v2.md:25,26,43,44,45` | G-2 · G-7 · G-8 · G-9 · N7-1 · N7-4 |
| 서버 시드 방식 · 원천 CSV 자리 · stg 진입점은 대기 | `$W/_RESUME.md:57` | G-12 · N7-5 |
| concern_site 보강 판정 = 추천(7고민 8행 · 95 → 103) | `$W/_RESUME.md:51` · `$W/research-concern-site.md:228` | §8-1 2 |
| 보강은 한 번에 · 코드 구현 끝난 뒤 | `$W/_RESUME.md:58` | §6-2 끝 · §8 |
| 바인드 마운트 방향 | `$W/_RESUME.md:66` | G-6 · N7-3 |
| DB 테이블은 SPEC-003 꼴 | `$W/spec-image-data-instructions.md:13` · `$W/SPEC-003-hub-gold-db.md:94-105` | G-10 · §6-1 |

## 부록 B. 재셈

이 워커가 `python3`(표준 라이브러리 `csv` · `hashlib` · `json` · `re`) · `grep` · `git`(읽기)으로 다시 센 것이다. CSV 는 `utf-8-sig` · `newline=''` 로 읽었다. 스크립트는 세션 임시 폴더에만 두었다. DB · 서버 · docker 를 띄우지 않았고 `.env` 를 열지 않았으며 외부 호출 0 이다.

| # | 무엇 | 결과 |
|---|---|---|
| ① | 시드 그림 표 | `image-assets.csv` **103행**(「원리」 54 · 「방법」 49) · 코드 집합 = `mechanism.code` 54 ∪ `method.code` 49(빠짐 0 · 남음 0) · `kind` ↔ 코드 접두어 어긋남 0 · `svg_path` 꼴 일치 103 · **sha256 일치 103 / 103** · 대표 103 = 6,886,445 바이트 · `review` · `artwork_version` · `production_status` · `width` · `height` · `background` 각 한 값 · `stage` 37 · 33 · 33 · 별칭 든 행 69(파일 83) |
| ② | 시드 라벨 표 | `image-labels.csv` **787행** · 코드 103 · `text_count` 합 787 = 코드별 행 수(어긋남 0 · 5 ~ 10) · `i18n_key` 787 유일 · (`code`, `element_id`) 787 유일 · `label-*` 581 + `diagram-title` 103 + `diagram-desc` 103 · `ko` 빈칸 0 · `en` 빈칸 0 · `svg_path` = 그 코드의 대표 경로 787 · `ko` 에 `;` · 줄바꿈 · NUL · 앞뒤 공백 0 · 가장 긴 `ko` 82자 |
| ③ | 대표 SVG 103 | `<script` · `<image` · `<style` · `<foreignObject` · `https://` 0 · `http://` 는 103(전부 이름공간 선언 한 줄) · `viewBox="0 0 1200 800"` 103 · `lang="ko"` 103 |
| ④ | 시드 폴더 | `images/` = `.svg` 186 · `.gitkeep` 2 · `.DS_Store` 1 · 대표 이름(`(MEC\|MET)-\d{3}.svg`) 103 · `image-map.csv` 103행 · `image-validation.json` 의 수(103 · 83 · 186 · 787)와 같다 |
| ⑤ | silver · gold 스크립트 | silver CSV 57 · 66,936행 · `gold-build.py` 본문에 `concern_site` 0 · `gold-check.py:91-94` 가 silver 표 목록을 고정 기대값과 견준다 · `silver-check.py:473` 이 ① ~ ④ 밖 키 있는 표를 D5 로 보낸다 · 스키마 `layers` 넷 |
| ⑥ | silver 파일 꼴 | `concern_site.csv` BOM 있음 · CRLF 0 · 95행 · 끝 id `CSI-0098` |
| ⑦ | 이름 | silver 키 접두어 55종에 `CIM` · `CIL` 없음 · silver 표 57 에 `concept` · `image` 든 이름 0 · 허브 모델에 `concept` 든 테이블 1(`catalog_procedure_concept`) · 새 제약 이름 최대 50자 |
| ⑧ | 허브에 수가 박힌 자리(grep) | `silver_contract.py:1`(57) · `:154`(80) · `model/medallion.py:1,3,9,59,85`(74 · 72 · 82 · 57) · `medallion_load.py:1,68,380`(74) · `db_inputs.py:7`(52) · `scripts/load_medallion.py:2`(74) · `tests/test_medallion_model.py:42,44,49,60,92,98,134,174-176,183,188` · `tests/test_medallion_load.py:86,87,146,153,154,299` · `tests/test_medallion_repo.py:265` · `tests/medallion_fixture.py:1,5,86,129` · (`health.files` 22 를 박은 5곳 `test_gold_load.py:85,146` · `test_gold_holes.py:68` · `test_gold_rest.py:38` · `test_gold_tools_synthetic.py:331` · `test_medallion_repo.py:79` 은 U7-2 (a) 면 그대로) |
| ⑨ | git | 허브 HEAD `daa54e3` · 작업 트리 깨끗 · versions 3 파일(끝 `b202611170001`) · 프로필 `$I` 는 미추적 · `git check-ignore` 불일치 |

## 변경 기록

### 0.1.0 — 2026-11-17 · 초안

- 지시서 「정해진 것」 을 G-1 ~ G-12 로 풀었다 — silver 표 2(103 · 787) · 시드 → silver 스크립트 · silver-check 보탬 · DB 테이블 2(74 → 76) · 적재기 V13 · 해시(그림 표는 이번 판 `silver`) · 에셋 폴더 · 재빌드 순서 11단계 · 다음 스펙이 읽을 자리 7.
- 이 워커가 본문에 「제안」 으로 정한 것: gold 에 안 넣음(U7-1) · 이번 판 `kind = silver`(U7-2) · 에셋 폴더 자리(U7-3) · 새 층 ⑤(O7-1) · 키 `id` + 유일 묶음(O7-2) · 라벨의 언어를 행으로 · 이름들(O7-6).
