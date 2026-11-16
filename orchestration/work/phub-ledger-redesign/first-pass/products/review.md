# products.json — 1차 조사 (읽기용)

> 이 문서는 생성물이다(build.py). 원문 값 칸과 잠정 관찰 칸을 분리했다. 잠정 관찰은 확정 데이터가 아니다.

## 0. 원본과 상태

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/products.json`
- 크기 8322 바이트 · 6666 코드 포인트 · UTF-8 · BOM 없음 · 한 줄 · 이스케이프 0
- sha256 (빌드 시작/끝 동일): `090955cccd35468ace2882024f0e0f216d3ebdb58b38d77693c0cf402338b854`
- 노드 415 · 키 352 · 중복 키 0 · 빈 값 0
- 형태소: 적용 225값 / 558토큰 · 제외 72값 · 필드명 352출현 제외
- 표현 후보: 701건 (값 구획 297 · 문장 8 · 정규식 248 · 수동 148)
- 상태 보고는 `validation.md` 맨 위, 미결은 `issues.md`.

## 1. 최상위 구성

| 원본 키 | 자료형 | 원문 값 / 구성 | Pointer |
|---|---|---|---|
| `version` | string | "1.2" | `/version` |
| `updated` | string | "2026-07-26" | `/updated` |
| `description` | string | "미용시술 제품-제조사 매핑 (유통사 아닌 제조사 기준)" | `/description` |
| `botulinum_toxin` | object | object { category_id, products }; products 11개 | `/botulinum_toxin` |
| `filler_ha` | object | object { category_id, products }; products 7개 | `/filler_ha` |
| `biostimulator` | object | object { category_id, products }; products 6개 | `/biostimulator` |
| `skin_booster` | object | object { category_id, products }; products 5개 | `/skin_booster` |
| `thread_lift` | object | object { category_id, products }; products 5개 | `/thread_lift` |
| `energy_device` | object | object { category_id, products }; products 18개 | `/energy_device` |
| `prp_exosome` | object | object { category_id, products }; products 5개 | `/prp_exosome` |
| `stem_cell` | object | object { category_id, products }; products 2개 | `/stem_cell` |

## 2. 컬럼 구성 표

깊이 2 이상 경로의 첫 `*` 는 최상위 섹션 키(8개), 그 뒤 `*` 는 배열 인덱스. 출현 수는 실제 노드 수. 예시는 첫 출현. 변형·선택 필드·자리표시를 따로 행으로 둔다.

| 원본 컬럼명 / 경로 패턴 | 자료형 · 중첩 | 출현 | 원문 예시 | 예시 위치 | 변형·선택 여부 |
|---|---|---|---|---|---|
| `/version` | string | 1 | "1.2" | `/version` |  |
| `/updated` | string | 1 | "2026-07-26" | `/updated` |  |
| `/description` | string | 1 | "미용시술 제품-제조사 매핑 (유통사 아닌 제조사 기준)" | `/description` |  |
| `/botulinum_toxin` | object | 1 | {category_id, products} | `/botulinum_toxin` |  |
| `/*/category_id` | string | 7 | "M1" | `/botulinum_toxin/category_id` | string: botulinum_toxin, filler_ha, biostimulator, skin_booster, thread_lift, prp_exosome, stem_cell |
| `/*/products` | array of object | 8 | [object × 11] | `/botulinum_toxin/products` |  |
| `/*/products/*` | object | 59 | {name, name_en, manufacturer, country, mfds} | `/botulinum_toxin/products/0` |  |
| `/*/products/*/name` | string · products 배열 항목 object 안 | 59 | "보톡스" | `/botulinum_toxin/products/0/name` | 항목 59/59; botulinum_toxin 11, filler_ha 7, biostimulator 6, skin_booster 5, thread_lift 5, energy_device 18, prp_exosome 5, stem_cell 2 |
| `/*/products/*/name_en` | string · products 배열 항목 object 안 | 59 | "Botox" | `/botulinum_toxin/products/0/name_en` | 항목 59/59; botulinum_toxin 11, filler_ha 7, biostimulator 6, skin_booster 5, thread_lift 5, energy_device 18, prp_exosome 5, stem_cell 2 |
| `/*/products/*/manufacturer` | string · products 배열 항목 object 안 | 59 | "앨러간/애브비" | `/botulinum_toxin/products/0/manufacturer` | 항목 59/59; botulinum_toxin 11, filler_ha 7, biostimulator 6, skin_booster 5, thread_lift 5, energy_device 18, prp_exosome 5, stem_cell 2 |
| `/*/products/*/country` | string · products 배열 항목 object 안 | 59 | "US" | `/botulinum_toxin/products/0/country` | 항목 59/59; botulinum_toxin 11, filler_ha 7, biostimulator 6, skin_booster 5, thread_lift 5, energy_device 18, prp_exosome 5, stem_cell 2 |
| `/*/products/*/mfds` | boolean · products 배열 항목 object 안 | 41 | true | `/botulinum_toxin/products/0/mfds` | 선택 필드 — 항목 41/59; botulinum_toxin 11, filler_ha 7, biostimulator 6, skin_booster 5, thread_lift 5, prp_exosome 5, stem_cell 2 |
| `/*/products/*/note` | string · products 배열 항목 object 안 | 5 | "휴젤 보툴렉스의 수출용 브랜드명(미국·중국·유럽 등)" | `/botulinum_toxin/products/10/note` | 선택 필드 — 항목 5/59; botulinum_toxin 1, skin_booster 2, prp_exosome 2 |
| `/filler_ha` | object | 1 | {category_id, products} | `/filler_ha` |  |
| `/biostimulator` | object | 1 | {category_id, products} | `/biostimulator` |  |
| `/*/products/*/ingredient` | string · products 배열 항목 object 안 | 9 | "PLLA" | `/biostimulator/products/0/ingredient` | 선택 필드 — 항목 9/59; biostimulator 6, skin_booster 3 |
| `/skin_booster` | object | 1 | {category_id, products} | `/skin_booster` |  |
| `/thread_lift` | object | 1 | {category_id, products} | `/thread_lift` |  |
| `/*/products/*/material` | string · products 배열 항목 object 안 | 5 | "PDO" | `/thread_lift/products/0/material` | 선택 필드 — 항목 5/59; thread_lift 5 |
| `/energy_device` | object | 1 | {category_id, products} | `/energy_device` |  |
| `/*/category_id` | array | 1 | ["M8", "M9", "M11"] | `/energy_device/category_id` | array: energy_device |
| `/*/category_id/*` | string · category_id 배열 원소 | 3 | "M8" | `/energy_device/category_id/0` |  |
| `/*/products/*/type` | string · products 배열 항목 object 안 | 25 | "HIFU" | `/energy_device/products/0/type` | 선택 필드 — 항목 25/59; energy_device 18, prp_exosome 5, stem_cell 2 |
| `/prp_exosome` | object | 1 | {category_id, products} | `/prp_exosome` |  |
| `/*/products/*/legal_warning` | string · products 배열 항목 object 안 | 2 | "국내 의료기관의 주사(injection) 용도 사용은 의료법·화장품법 위반 소지가 있으며 식약처가 반복 경고·단속한 사안입니다. 시술 표기·광고 시 '주입'이 아닌 '도포(MTS·니들RF 후 경피 전달)'로만 표현해야 합니다" | `/prp_exosome/products/3/legal_warning` | 선택 필드 — 항목 2/59; prp_exosome 2 |
| `/*/products/*/regulatory_status` | string · products 배열 항목 object 안 | 2 | "화장품 허가만 받은 제품 — 식약처의 주사·주입 용도 허가 없음" | `/prp_exosome/products/3/regulatory_status` | 선택 필드 — 항목 2/59; prp_exosome 2 |
| `/stem_cell` | object | 1 | {category_id, products} | `/stem_cell` |  |
| `/*/products/*/manufacturer` = `"-"` | string 자리표시 | 1 | "-" | `/skin_booster/products/3/manufacturer` | 값 변형(자리표시) |
| `/*/products/*/country` = `"-"` | string 자리표시 | 1 | "-" | `/skin_booster/products/3/country` | 값 변형(자리표시) |
| `/*/products/*/mfds` = `true` | boolean | 35 | true | `/botulinum_toxin/products/0/mfds` 외 | 값 분포 |
| `/*/products/*/mfds` = `false` | boolean | 6 | false | `/skin_booster/products/3/mfds` 외 | 값 분포 |
| `/*/products/*/mfds` 키 없음 | — | 18 | (키 없음) | `/energy_device/products/0` … `/energy_device/products/17` | 선택 필드 부재 |
| `/*/products/*` 키 구성 {name, name_en, manufacturer, country, mfds} | object 변형 | 17 | (키 순서 그대로) | `/botulinum_toxin/products/0`, `/botulinum_toxin/products/1`, `/botulinum_toxin/products/2` 외 14 | 항목 키 구성 변형 |
| `/*/products/*` 키 구성 {name, name_en, manufacturer, country, mfds, note} | object 변형 | 3 | (키 순서 그대로) | `/botulinum_toxin/products/10`, `/skin_booster/products/3`, `/skin_booster/products/4` | 항목 키 구성 변형 |
| `/*/products/*` 키 구성 {name, name_en, manufacturer, country, mfds, ingredient} | object 변형 | 9 | (키 순서 그대로) | `/biostimulator/products/0`, `/biostimulator/products/1`, `/biostimulator/products/2` 외 6 | 항목 키 구성 변형 |
| `/*/products/*` 키 구성 {name, name_en, manufacturer, country, mfds, material} | object 변형 | 5 | (키 순서 그대로) | `/thread_lift/products/0`, `/thread_lift/products/1`, `/thread_lift/products/2` 외 2 | 항목 키 구성 변형 |
| `/*/products/*` 키 구성 {name, name_en, manufacturer, country, type} | object 변형 | 18 | (키 순서 그대로) | `/energy_device/products/0`, `/energy_device/products/1`, `/energy_device/products/2` 외 15 | 항목 키 구성 변형 |
| `/*/products/*` 키 구성 {name, name_en, manufacturer, country, mfds, type} | object 변형 | 5 | (키 순서 그대로) | `/prp_exosome/products/0`, `/prp_exosome/products/1`, `/prp_exosome/products/2` 외 2 | 항목 키 구성 변형 |
| `/*/products/*` 키 구성 {name, name_en, manufacturer, country, mfds, type, note, legal_warning, regulatory_status} | object 변형 | 2 | (키 순서 그대로) | `/prp_exosome/products/3`, `/prp_exosome/products/4` | 항목 키 구성 변형 |
| 빈 문자열·빈 배열·빈 객체·null | — | 0 | (없음) | — | 원본에 0건 |

## 3. 항목별 값 (원본 컬럼명 그대로, 원본 순서)

원문 값 칸은 JSON 리터럴 그대로다(문자열은 따옴표 포함). 관찰은 §4 에만 적는다.

### `botulinum_toxin` — category_id "M1" (`/botulinum_toxin/category_id`) · products 11개

| 항목 | 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | `category_id` | "M1" | `/botulinum_toxin/category_id` |
| **0** | `name` | "보톡스" | `/botulinum_toxin/products/0/name` |
|  | `name_en` | "Botox" | `/botulinum_toxin/products/0/name_en` |
|  | `manufacturer` | "앨러간/애브비" | `/botulinum_toxin/products/0/manufacturer` |
|  | `country` | "US" | `/botulinum_toxin/products/0/country` |
|  | `mfds` | true | `/botulinum_toxin/products/0/mfds` |
| **1** | `name` | "디스포트" | `/botulinum_toxin/products/1/name` |
|  | `name_en` | "Dysport" | `/botulinum_toxin/products/1/name_en` |
|  | `manufacturer` | "입센" | `/botulinum_toxin/products/1/manufacturer` |
|  | `country` | "FR" | `/botulinum_toxin/products/1/country` |
|  | `mfds` | true | `/botulinum_toxin/products/1/mfds` |
| **2** | `name` | "제오민" | `/botulinum_toxin/products/2/name` |
|  | `name_en` | "Xeomin" | `/botulinum_toxin/products/2/name_en` |
|  | `manufacturer` | "멀츠" | `/botulinum_toxin/products/2/manufacturer` |
|  | `country` | "DE" | `/botulinum_toxin/products/2/country` |
|  | `mfds` | true | `/botulinum_toxin/products/2/mfds` |
| **3** | `name` | "보툴렉스" | `/botulinum_toxin/products/3/name` |
|  | `name_en` | "Botulax" | `/botulinum_toxin/products/3/name_en` |
|  | `manufacturer` | "휴젤" | `/botulinum_toxin/products/3/manufacturer` |
|  | `country` | "KR" | `/botulinum_toxin/products/3/country` |
|  | `mfds` | true | `/botulinum_toxin/products/3/mfds` |
| **4** | `name` | "나보타" | `/botulinum_toxin/products/4/name` |
|  | `name_en` | "Nabota" | `/botulinum_toxin/products/4/name_en` |
|  | `manufacturer` | "대웅제약" | `/botulinum_toxin/products/4/manufacturer` |
|  | `country` | "KR" | `/botulinum_toxin/products/4/country` |
|  | `mfds` | true | `/botulinum_toxin/products/4/mfds` |
| **5** | `name` | "메디톡신" | `/botulinum_toxin/products/5/name` |
|  | `name_en` | "Meditoxin" | `/botulinum_toxin/products/5/name_en` |
|  | `manufacturer` | "메디톡스" | `/botulinum_toxin/products/5/manufacturer` |
|  | `country` | "KR" | `/botulinum_toxin/products/5/country` |
|  | `mfds` | true | `/botulinum_toxin/products/5/mfds` |
| **6** | `name` | "리즈톡스" | `/botulinum_toxin/products/6/name` |
|  | `name_en` | "Liztox" | `/botulinum_toxin/products/6/name_en` |
|  | `manufacturer` | "휴온스바이오파마" | `/botulinum_toxin/products/6/manufacturer` |
|  | `country` | "KR" | `/botulinum_toxin/products/6/country` |
|  | `mfds` | true | `/botulinum_toxin/products/6/mfds` |
| **7** | `name` | "더톡신" | `/botulinum_toxin/products/7/name` |
|  | `name_en` | "The Toxin" | `/botulinum_toxin/products/7/name_en` |
|  | `manufacturer` | "제테마" | `/botulinum_toxin/products/7/manufacturer` |
|  | `country` | "KR" | `/botulinum_toxin/products/7/country` |
|  | `mfds` | true | `/botulinum_toxin/products/7/mfds` |
| **8** | `name` | "티엠버스" | `/botulinum_toxin/products/8/name` |
|  | `name_en` | "Timbus" | `/botulinum_toxin/products/8/name_en` |
|  | `manufacturer` | "종근당바이오" | `/botulinum_toxin/products/8/manufacturer` |
|  | `country` | "KR" | `/botulinum_toxin/products/8/country` |
|  | `mfds` | true | `/botulinum_toxin/products/8/mfds` |
| **9** | `name` | "뉴럭스" | `/botulinum_toxin/products/9/name` |
|  | `name_en` | "NEWLUX" | `/botulinum_toxin/products/9/name_en` |
|  | `manufacturer` | "뉴메코(Newmeco, 메디톡스 계열)" | `/botulinum_toxin/products/9/manufacturer` |
|  | `country` | "KR" | `/botulinum_toxin/products/9/country` |
|  | `mfds` | true | `/botulinum_toxin/products/9/mfds` |
| **10** | `name` | "레티보" | `/botulinum_toxin/products/10/name` |
|  | `name_en` | "Letybo" | `/botulinum_toxin/products/10/name_en` |
|  | `manufacturer` | "휴젤" | `/botulinum_toxin/products/10/manufacturer` |
|  | `country` | "KR" | `/botulinum_toxin/products/10/country` |
|  | `mfds` | true | `/botulinum_toxin/products/10/mfds` |
|  | `note` | "휴젤 보툴렉스의 수출용 브랜드명(미국·중국·유럽 등)" | `/botulinum_toxin/products/10/note` |

### `filler_ha` — category_id "M2" (`/filler_ha/category_id`) · products 7개

| 항목 | 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | `category_id` | "M2" | `/filler_ha/category_id` |
| **0** | `name` | "쥬비덤" | `/filler_ha/products/0/name` |
|  | `name_en` | "Juvéderm" | `/filler_ha/products/0/name_en` |
|  | `manufacturer` | "앨러간/애브비" | `/filler_ha/products/0/manufacturer` |
|  | `country` | "US" | `/filler_ha/products/0/country` |
|  | `mfds` | true | `/filler_ha/products/0/mfds` |
| **1** | `name` | "레스틸렌" | `/filler_ha/products/1/name` |
|  | `name_en` | "Restylane" | `/filler_ha/products/1/name_en` |
|  | `manufacturer` | "갈더마" | `/filler_ha/products/1/manufacturer` |
|  | `country` | "SE" | `/filler_ha/products/1/country` |
|  | `mfds` | true | `/filler_ha/products/1/mfds` |
| **2** | `name` | "이브아르" | `/filler_ha/products/2/name` |
|  | `name_en` | "Yvoire" | `/filler_ha/products/2/name_en` |
|  | `manufacturer` | "LG화학" | `/filler_ha/products/2/manufacturer` |
|  | `country` | "KR" | `/filler_ha/products/2/country` |
|  | `mfds` | true | `/filler_ha/products/2/mfds` |
| **3** | `name` | "벨로테로" | `/filler_ha/products/3/name` |
|  | `name_en` | "Belotero" | `/filler_ha/products/3/name_en` |
|  | `manufacturer` | "멀츠" | `/filler_ha/products/3/manufacturer` |
|  | `country` | "DE" | `/filler_ha/products/3/country` |
|  | `mfds` | true | `/filler_ha/products/3/mfds` |
| **4** | `name` | "엘라비에" | `/filler_ha/products/4/name` |
|  | `name_en` | "Elravie" | `/filler_ha/products/4/name_en` |
|  | `manufacturer` | "휴메딕스" | `/filler_ha/products/4/manufacturer` |
|  | `country` | "KR" | `/filler_ha/products/4/country` |
|  | `mfds` | true | `/filler_ha/products/4/mfds` |
| **5** | `name` | "채움" | `/filler_ha/products/5/name` |
|  | `name_en` | "Chaeum" | `/filler_ha/products/5/name_en` |
|  | `manufacturer` | "휴젤" | `/filler_ha/products/5/manufacturer` |
|  | `country` | "KR" | `/filler_ha/products/5/country` |
|  | `mfds` | true | `/filler_ha/products/5/mfds` |
| **6** | `name` | "더채움" | `/filler_ha/products/6/name` |
|  | `name_en` | "The Chaeum" | `/filler_ha/products/6/name_en` |
|  | `manufacturer` | "휴젤" | `/filler_ha/products/6/manufacturer` |
|  | `country` | "KR" | `/filler_ha/products/6/country` |
|  | `mfds` | true | `/filler_ha/products/6/mfds` |

### `biostimulator` — category_id "M3" (`/biostimulator/category_id`) · products 6개

| 항목 | 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | `category_id` | "M3" | `/biostimulator/category_id` |
| **0** | `name` | "스컬트라" | `/biostimulator/products/0/name` |
|  | `name_en` | "Sculptra" | `/biostimulator/products/0/name_en` |
|  | `manufacturer` | "갈더마" | `/biostimulator/products/0/manufacturer` |
|  | `country` | "FR" | `/biostimulator/products/0/country` |
|  | `mfds` | true | `/biostimulator/products/0/mfds` |
|  | `ingredient` | "PLLA" | `/biostimulator/products/0/ingredient` |
| **1** | `name` | "엘란쎄" | `/biostimulator/products/1/name` |
|  | `name_en` | "Ellansé" | `/biostimulator/products/1/name_en` |
|  | `manufacturer` | "싱클레어" | `/biostimulator/products/1/manufacturer` |
|  | `country` | "NL" | `/biostimulator/products/1/country` |
|  | `mfds` | true | `/biostimulator/products/1/mfds` |
|  | `ingredient` | "PCL" | `/biostimulator/products/1/ingredient` |
| **2** | `name` | "래디어스" | `/biostimulator/products/2/name` |
|  | `name_en` | "Radiesse" | `/biostimulator/products/2/name_en` |
|  | `manufacturer` | "멀츠" | `/biostimulator/products/2/manufacturer` |
|  | `country` | "DE" | `/biostimulator/products/2/country` |
|  | `mfds` | true | `/biostimulator/products/2/mfds` |
|  | `ingredient` | "CaHA" | `/biostimulator/products/2/ingredient` |
| **3** | `name` | "쥬베룩" | `/biostimulator/products/3/name` |
|  | `name_en` | "Juvelook" | `/biostimulator/products/3/name_en` |
|  | `manufacturer` | "바임(VAIM/바임글로벌)" | `/biostimulator/products/3/manufacturer` |
|  | `country` | "KR" | `/biostimulator/products/3/country` |
|  | `mfds` | true | `/biostimulator/products/3/mfds` |
|  | `ingredient` | "PDLLA+HA" | `/biostimulator/products/3/ingredient` |
| **4** | `name` | "쥬베룩볼륨" | `/biostimulator/products/4/name` |
|  | `name_en` | "Juvelook Volume" | `/biostimulator/products/4/name_en` |
|  | `manufacturer` | "바임(VAIM/바임글로벌)" | `/biostimulator/products/4/manufacturer` |
|  | `country` | "KR" | `/biostimulator/products/4/country` |
|  | `mfds` | true | `/biostimulator/products/4/mfds` |
|  | `ingredient` | "PDLLA+HA" | `/biostimulator/products/4/ingredient` |
| **5** | `name` | "글로벨라" | `/biostimulator/products/5/name` |
|  | `name_en` | "Glovella" | `/biostimulator/products/5/name_en` |
|  | `manufacturer` | "에이씨피바이오" | `/biostimulator/products/5/manufacturer` |
|  | `country` | "KR" | `/biostimulator/products/5/country` |
|  | `mfds` | true | `/biostimulator/products/5/mfds` |
|  | `ingredient` | "PDLLA+HA" | `/biostimulator/products/5/ingredient` |

### `skin_booster` — category_id "M4" (`/skin_booster/category_id`) · products 5개

| 항목 | 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | `category_id` | "M4" | `/skin_booster/category_id` |
| **0** | `name` | "리쥬란 힐러" | `/skin_booster/products/0/name` |
|  | `name_en` | "Rejuran Healer" | `/skin_booster/products/0/name_en` |
|  | `manufacturer` | "파마리서치" | `/skin_booster/products/0/manufacturer` |
|  | `country` | "KR" | `/skin_booster/products/0/country` |
|  | `mfds` | true | `/skin_booster/products/0/mfds` |
|  | `ingredient` | "PN/PDRN" | `/skin_booster/products/0/ingredient` |
| **1** | `name` | "리쥬란 HB+" | `/skin_booster/products/1/name` |
|  | `name_en` | "Rejuran HB+" | `/skin_booster/products/1/name_en` |
|  | `manufacturer` | "파마리서치" | `/skin_booster/products/1/manufacturer` |
|  | `country` | "KR" | `/skin_booster/products/1/country` |
|  | `mfds` | true | `/skin_booster/products/1/mfds` |
|  | `ingredient` | "PN+HA" | `/skin_booster/products/1/ingredient` |
| **2** | `name` | "리쥬란아이" | `/skin_booster/products/2/name` |
|  | `name_en` | "Rejuran i" | `/skin_booster/products/2/name_en` |
|  | `manufacturer` | "파마리서치" | `/skin_booster/products/2/manufacturer` |
|  | `country` | "KR" | `/skin_booster/products/2/country` |
|  | `mfds` | true | `/skin_booster/products/2/mfds` |
|  | `ingredient` | "PN" | `/skin_booster/products/2/ingredient` |
| **3** | `name` | "스킨보톡스" | `/skin_booster/products/3/name` |
|  | `name_en` | "Skin Botox" | `/skin_booster/products/3/name_en` |
|  | `manufacturer` | "-" | `/skin_booster/products/3/manufacturer` |
|  | `country` | "-" | `/skin_booster/products/3/country` |
|  | `mfds` | false | `/skin_booster/products/3/mfds` |
|  | `note` | "보톡스 희석 피내주사법 (별도 제품 아님)" | `/skin_booster/products/3/note` |
| **4** | `name` | "벨피엔" | `/skin_booster/products/4/name` |
|  | `name_en` | "Belpien" | `/skin_booster/products/4/name_en` |
|  | `manufacturer` | "휴메딕스" | `/skin_booster/products/4/manufacturer` |
|  | `country` | "KR" | `/skin_booster/products/4/country` |
|  | `mfds` | false | `/skin_booster/products/4/mfds` |
|  | `note` | "2026 하반기 출시 예정, PN+HA 복합" | `/skin_booster/products/4/note` |

### `thread_lift` — category_id "M7" (`/thread_lift/category_id`) · products 5개

| 항목 | 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | `category_id` | "M7" | `/thread_lift/category_id` |
| **0** | `name` | "민트리프트" | `/thread_lift/products/0/name` |
|  | `name_en` | "Mint Lift" | `/thread_lift/products/0/name_en` |
|  | `manufacturer` | "한스바이오메드" | `/thread_lift/products/0/manufacturer` |
|  | `country` | "KR" | `/thread_lift/products/0/country` |
|  | `mfds` | true | `/thread_lift/products/0/mfds` |
|  | `material` | "PDO" | `/thread_lift/products/0/material` |
| **1** | `name` | "테스리프트" | `/thread_lift/products/1/name` |
|  | `name_en` | "TESSLift" | `/thread_lift/products/1/name_en` |
|  | `manufacturer` | "리젠바이오텍" | `/thread_lift/products/1/manufacturer` |
|  | `country` | "KR" | `/thread_lift/products/1/country` |
|  | `mfds` | true | `/thread_lift/products/1/mfds` |
|  | `material` | "PDO+PCL" | `/thread_lift/products/1/material` |
| **2** | `name` | "실루엣소프트" | `/thread_lift/products/2/name` |
|  | `name_en` | "Silhouette Soft" | `/thread_lift/products/2/name_en` |
|  | `manufacturer` | "싱클레어" | `/thread_lift/products/2/manufacturer` |
|  | `country` | "NL" | `/thread_lift/products/2/country` |
|  | `mfds` | true | `/thread_lift/products/2/mfds` |
|  | `material` | "PLLA" | `/thread_lift/products/2/material` |
| **3** | `name` | "에버라인" | `/thread_lift/products/3/name` |
|  | `name_en` | "Everline" | `/thread_lift/products/3/name_en` |
|  | `manufacturer` | "KL글로벌" | `/thread_lift/products/3/manufacturer` |
|  | `country` | "KR" | `/thread_lift/products/3/country` |
|  | `mfds` | true | `/thread_lift/products/3/mfds` |
|  | `material` | "PDO" | `/thread_lift/products/3/material` |
| **4** | `name` | "미라클" | `/thread_lift/products/4/name` |
|  | `name_en` | "Miracle Thread" | `/thread_lift/products/4/name_en` |
|  | `manufacturer` | "메디텍" | `/thread_lift/products/4/manufacturer` |
|  | `country` | "KR" | `/thread_lift/products/4/country` |
|  | `mfds` | true | `/thread_lift/products/4/mfds` |
|  | `material` | "PDO" | `/thread_lift/products/4/material` |

### `energy_device` — category_id ["M8", "M9", "M11"] (`/energy_device/category_id`) · products 18개

| 항목 | 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | `category_id` | ["M8", "M9", "M11"] | `/energy_device/category_id` |
| (묶음) | `category_id` [0] | "M8" | `/energy_device/category_id/0` |
| (묶음) | `category_id` [1] | "M9" | `/energy_device/category_id/1` |
| (묶음) | `category_id` [2] | "M11" | `/energy_device/category_id/2` |
| **0** | `name` | "울쎄라" | `/energy_device/products/0/name` |
|  | `name_en` | "Ultherapy" | `/energy_device/products/0/name_en` |
|  | `manufacturer` | "멀츠" | `/energy_device/products/0/manufacturer` |
|  | `country` | "US" | `/energy_device/products/0/country` |
|  | `type` | "HIFU" | `/energy_device/products/0/type` |
| **1** | `name` | "써마지FLX" | `/energy_device/products/1/name` |
|  | `name_en` | "Thermage FLX" | `/energy_device/products/1/name_en` |
|  | `manufacturer` | "솔타메디컬" | `/energy_device/products/1/manufacturer` |
|  | `country` | "US" | `/energy_device/products/1/country` |
|  | `type` | "RF" | `/energy_device/products/1/type` |
| **2** | `name` | "슈링크유니버스" | `/energy_device/products/2/name` |
|  | `name_en` | "Shurink Universe" | `/energy_device/products/2/name_en` |
|  | `manufacturer` | "클래시스" | `/energy_device/products/2/manufacturer` |
|  | `country` | "KR" | `/energy_device/products/2/country` |
|  | `type` | "HIFU" | `/energy_device/products/2/type` |
| **3** | `name` | "올리지오" | `/energy_device/products/3/name` |
|  | `name_en` | "Oligio" | `/energy_device/products/3/name_en` |
|  | `manufacturer` | "클래시스" | `/energy_device/products/3/manufacturer` |
|  | `country` | "KR" | `/energy_device/products/3/country` |
|  | `type` | "RF" | `/energy_device/products/3/type` |
| **4** | `name` | "볼뉴머" | `/energy_device/products/4/name` |
|  | `name_en` | "Volnewmer" | `/energy_device/products/4/name_en` |
|  | `manufacturer` | "클래시스(Classys)" | `/energy_device/products/4/manufacturer` |
|  | `country` | "KR" | `/energy_device/products/4/country` |
|  | `type` | "모노폴라 RF" | `/energy_device/products/4/type` |
| **5** | `name` | "더블로골드" | `/energy_device/products/5/name` |
|  | `name_en` | "Doublo Gold" | `/energy_device/products/5/name_en` |
|  | `manufacturer` | "하이로닉" | `/energy_device/products/5/manufacturer` |
|  | `country` | "KR" | `/energy_device/products/5/country` |
|  | `type` | "HIFU" | `/energy_device/products/5/type` |
| **6** | `name` | "인모드" | `/energy_device/products/6/name` |
|  | `name_en` | "InMode" | `/energy_device/products/6/name_en` |
|  | `manufacturer` | "인모드" | `/energy_device/products/6/manufacturer` |
|  | `country` | "IL" | `/energy_device/products/6/country` |
|  | `type` | "RF+EMS" | `/energy_device/products/6/type` |
| **7** | `name` | "포텐자" | `/energy_device/products/7/name` |
|  | `name_en` | "Potenza" | `/energy_device/products/7/name_en` |
|  | `manufacturer` | "사이노슈어" | `/energy_device/products/7/manufacturer` |
|  | `country` | "US" | `/energy_device/products/7/country` |
|  | `type` | "니들RF" | `/energy_device/products/7/type` |
| **8** | `name` | "인트라셀" | `/energy_device/products/8/name` |
|  | `name_en` | "INTRACELL" | `/energy_device/products/8/name_en` |
|  | `manufacturer` | "제이시스메디칼" | `/energy_device/products/8/manufacturer` |
|  | `country` | "KR" | `/energy_device/products/8/country` |
|  | `type` | "니들RF" | `/energy_device/products/8/type` |
| **9** | `name` | "시크릿" | `/energy_device/products/9/name` |
|  | `name_en` | "Secret RF" | `/energy_device/products/9/name_en` |
|  | `manufacturer` | "아이닉" | `/energy_device/products/9/manufacturer` |
|  | `country` | "KR" | `/energy_device/products/9/country` |
|  | `type` | "니들RF" | `/energy_device/products/9/type` |
| **10** | `name` | "제니스" | `/energy_device/products/10/name` |
|  | `name_en` | "AGNES" | `/energy_device/products/10/name_en` |
|  | `manufacturer` | "고우리엔티" | `/energy_device/products/10/manufacturer` |
|  | `country` | "KR" | `/energy_device/products/10/country` |
|  | `type` | "니들RF" | `/energy_device/products/10/type` |
| **11** | `name` | "피코슈어" | `/energy_device/products/11/name` |
|  | `name_en` | "PicoSure" | `/energy_device/products/11/name_en` |
|  | `manufacturer` | "사이노슈어" | `/energy_device/products/11/manufacturer` |
|  | `country` | "US" | `/energy_device/products/11/country` |
|  | `type` | "피코레이저" | `/energy_device/products/11/type` |
| **12** | `name` | "피코웨이" | `/energy_device/products/12/name` |
|  | `name_en` | "PicoWay" | `/energy_device/products/12/name_en` |
|  | `manufacturer` | "캔델라" | `/energy_device/products/12/manufacturer` |
|  | `country` | "US" | `/energy_device/products/12/country` |
|  | `type` | "피코레이저" | `/energy_device/products/12/type` |
| **13** | `name` | "클라리티2" | `/energy_device/products/13/name` |
|  | `name_en` | "Clarity II" | `/energy_device/products/13/name_en` |
|  | `manufacturer` | "루트로닉" | `/energy_device/products/13/manufacturer` |
|  | `country` | "KR" | `/energy_device/products/13/country` |
|  | `type` | "Nd:YAG+알렉산드라이트" | `/energy_device/products/13/type` |
| **14** | `name` | "엑셀V" | `/energy_device/products/14/name` |
|  | `name_en` | "Excel V" | `/energy_device/products/14/name_en` |
|  | `manufacturer` | "큐테라" | `/energy_device/products/14/manufacturer` |
|  | `country` | "US" | `/energy_device/products/14/country` |
|  | `type` | "혈관레이저" | `/energy_device/products/14/type` |
| **15** | `name` | "프락셀" | `/energy_device/products/15/name` |
|  | `name_en` | "Fraxel" | `/energy_device/products/15/name_en` |
|  | `manufacturer` | "솔타메디컬" | `/energy_device/products/15/manufacturer` |
|  | `country` | "US" | `/energy_device/products/15/country` |
|  | `type` | "프락셔널" | `/energy_device/products/15/type` |
| **16** | `name` | "레블라이트" | `/energy_device/products/16/name` |
|  | `name_en` | "RevLite" | `/energy_device/products/16/name_en` |
|  | `manufacturer` | "사이노슈어" | `/energy_device/products/16/manufacturer` |
|  | `country` | "US" | `/energy_device/products/16/country` |
|  | `type` | "Nd:YAG" | `/energy_device/products/16/type` |
| **17** | `name` | "LDM" | `/energy_device/products/17/name` |
|  | `name_en` | "LDM-MED" | `/energy_device/products/17/name_en` |
|  | `manufacturer` | "제이시스메디칼" | `/energy_device/products/17/manufacturer` |
|  | `country` | "KR" | `/energy_device/products/17/country` |
|  | `type` | "초음파" | `/energy_device/products/17/type` |

### `prp_exosome` — category_id "M5" (`/prp_exosome/category_id`) · products 5개

| 항목 | 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | `category_id` | "M5" | `/prp_exosome/category_id` |
| **0** | `name` | "셀피아" | `/prp_exosome/products/0/name` |
|  | `name_en` | "Cellpia" | `/prp_exosome/products/0/name_en` |
|  | `manufacturer` | "CGBio" | `/prp_exosome/products/0/manufacturer` |
|  | `country` | "KR" | `/prp_exosome/products/0/country` |
|  | `mfds` | true | `/prp_exosome/products/0/mfds` |
|  | `type` | "PRP키트" | `/prp_exosome/products/0/type` |
| **1** | `name` | "리젠ACR" | `/prp_exosome/products/1/name` |
|  | `name_en` | "RegenACR" | `/prp_exosome/products/1/name_en` |
|  | `manufacturer` | "리젠바이오텍" | `/prp_exosome/products/1/manufacturer` |
|  | `country` | "KR" | `/prp_exosome/products/1/country` |
|  | `mfds` | true | `/prp_exosome/products/1/mfds` |
|  | `type` | "PRP키트" | `/prp_exosome/products/1/type` |
| **2** | `name` | "마이셀" | `/prp_exosome/products/2/name` |
|  | `name_en` | "Mycell" | `/prp_exosome/products/2/name_en` |
|  | `manufacturer` | "한스바이오메드" | `/prp_exosome/products/2/manufacturer` |
|  | `country` | "KR" | `/prp_exosome/products/2/country` |
|  | `mfds` | true | `/prp_exosome/products/2/mfds` |
|  | `type` | "PRP키트" | `/prp_exosome/products/2/type` |
| **3** | `name` | "ASCEplus" | `/prp_exosome/products/3/name` |
|  | `name_en` | "ASCE+" | `/prp_exosome/products/3/name_en` |
|  | `manufacturer` | "엑소코바이오" | `/prp_exosome/products/3/manufacturer` |
|  | `country` | "KR" | `/prp_exosome/products/3/country` |
|  | `mfds` | false | `/prp_exosome/products/3/mfds` |
|  | `type` | "엑소좀" | `/prp_exosome/products/3/type` |
|  | `note` | "화장품 허가. 주사/주입 사용 금지" | `/prp_exosome/products/3/note` |
|  | `legal_warning` | "국내 의료기관의 주사(injection) 용도 사용은 의료법·화장품법 위반 소지가 있으며 식약처가 반복 경고·단속한 사안입니다. 시술 표기·광고 시 '주입'이 아닌 '도포(MTS·니들RF 후 경피 전달)'로만 표현해야 합니다" | `/prp_exosome/products/3/legal_warning` |
|  | `regulatory_status` | "화장품 허가만 받은 제품 — 식약처의 주사·주입 용도 허가 없음" | `/prp_exosome/products/3/regulatory_status` |
| **4** | `name` | "EXOSOME SKIN" | `/prp_exosome/products/4/name` |
|  | `name_en` | "ExoSCRT" | `/prp_exosome/products/4/name_en` |
|  | `manufacturer` | "엑소스템텍" | `/prp_exosome/products/4/manufacturer` |
|  | `country` | "KR" | `/prp_exosome/products/4/country` |
|  | `mfds` | false | `/prp_exosome/products/4/mfds` |
|  | `type` | "엑소좀" | `/prp_exosome/products/4/type` |
|  | `note` | "화장품 허가. 주사/주입 사용 금지" | `/prp_exosome/products/4/note` |
|  | `legal_warning` | "국내 의료기관의 주사(injection) 용도 사용은 의료법·화장품법 위반 소지가 있으며 식약처가 반복 경고·단속한 사안입니다. 시술 표기·광고 시 '주입'이 아닌 '도포(MTS·니들RF 후 경피 전달)'로만 표현해야 합니다" | `/prp_exosome/products/4/legal_warning` |
|  | `regulatory_status` | "화장품 허가만 받은 제품 — 식약처의 주사·주입 용도 허가 없음" | `/prp_exosome/products/4/regulatory_status` |

### `stem_cell` — category_id "M17" (`/stem_cell/category_id`) · products 2개

| 항목 | 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | `category_id` | "M17" | `/stem_cell/category_id` |
| **0** | `name` | "큐어스킨" | `/stem_cell/products/0/name` |
|  | `name_en` | "CureSkin" | `/stem_cell/products/0/name_en` |
|  | `manufacturer` | "바이오솔루션" | `/stem_cell/products/0/manufacturer` |
|  | `country` | "KR" | `/stem_cell/products/0/country` |
|  | `mfds` | false | `/stem_cell/products/0/mfds` |
|  | `type` | "성장인자" | `/stem_cell/products/0/type` |
| **1** | `name` | "에스에프" | `/stem_cell/products/1/name` |
|  | `name_en` | "SF Injection" | `/stem_cell/products/1/name_en` |
|  | `manufacturer` | "에이치앤바이오" | `/stem_cell/products/1/manufacturer` |
|  | `country` | "KR" | `/stem_cell/products/1/country` |
|  | `mfds` | false | `/stem_cell/products/1/mfds` |
|  | `type` | "줄기세포배양액" | `/stem_cell/products/1/type` |

## 4. 잠정 관찰 (원문 값과 분리)

상태: `잠정`=근거 있는 관찰이나 확정 아님 · `후속`=후속 의미 조사/연결 과제 · `원문부족`=원문에 정보가 없음. 자세한 처리는 issues.md.

| id | 관찰 | 근거 Pointer | 상태 | issues |
|---|---|---|---|---|
| O01 | 최상위는 메타 3키(version·updated·description) 다음 분류 묶음 8키. 묶음 키는 영문 snake_case 이고 한국어 이름 칸이 없다. 묶음의 뜻은 키 이름과 category_id 코드로만 드러난다. | `/version`<br>`/updated`<br>`/description`<br>`/botulinum_toxin`<br>`/stem_cell` | 잠정 | F1 |
| O02 | description 은 manufacturer 칸이 '유통사 아닌 제조사 기준' 이라고 파일 수준에서 선언한다. 각 항목의 manufacturer 값이 이 기준을 따르는지는 원문으로 확인할 수 없다. | `/description` | 원문부족 | B5 |
| O03 | category_id 는 7개 묶음에서 string(M1·M2·M3·M4·M7·M5·M17), energy_device 에서만 array [M8,M9,M11] 이다. 파일 순서는 코드 숫자 순이 아니다(M7 다음 M8~ 다음 M5). 코드의 뜻은 이 파일에 없다. | `/botulinum_toxin/category_id`<br>`/thread_lift/category_id`<br>`/energy_device/category_id`<br>`/prp_exosome/category_id`<br>`/stem_cell/category_id` | 원문부족 | B2 |
| O04 | energy_device 의 18개 항목 각각이 M8·M9·M11 중 어느 코드에 속하는지 항목 단위 표시가 없다. | `/energy_device/category_id`<br>`/energy_device/products` | 원문부족 | B2 |
| O05 | 파일에 나오지 않는 코드: M6·M10·M12~M16. 다른 원장에 있는지 이 조사는 열지 않았다. | `/botulinum_toxin/category_id`<br>`/stem_cell/category_id` | 후속 | F1 |
| O06 | mfds 는 boolean. 키 이름 외에 뜻(무엇의 허가·신고 여부인지)을 설명하는 원문이 없다. energy_device 18항목은 mfds 키 자체가 없다 — '키 없음' 과 false 는 다른 상태로 보존한다. | `/botulinum_toxin/products/0/mfds`<br>`/skin_booster/products/3/mfds`<br>`/energy_device/products/0` | 원문부족 | B1 |
| O07 | 스킨보톡스 항목: note 가 '보톡스 희석 피내주사법 (별도 제품 아님)' 이고 manufacturer·country 가 '-', mfds false. products 배열 안에 있으나 스스로 제품이 아니라고 서술한다. 항목의 종류(제품/기법)는 후속에서 정한다. | `/skin_booster/products/3/name`<br>`/skin_booster/products/3/note`<br>`/skin_booster/products/3/manufacturer`<br>`/skin_booster/products/3/country`<br>`/skin_booster/products/3/mfds` | 잠정 | P1 |
| O08 | '-' 자리표시 2건(스킨보톡스 manufacturer·country). '해당 없음' 인지 '미상' 인지 원문에 없다. | `/skin_booster/products/3/manufacturer`<br>`/skin_booster/products/3/country` | 원문부족 | B3 |
| O09 | 벨피엔 note '2026 하반기 출시 예정, PN+HA 복합' — 예정 상태. 파일 updated 는 2026-07-26. 현재 출시 여부·상태 갱신 시점은 원문에 없다. 다른 항목은 ingredient 칸에 성분을 두는데 벨피엔은 note 안에 'PN+HA 복합' 을 둔다(ingredient 키 없음). | `/skin_booster/products/4/note`<br>`/skin_booster/products/4/mfds`<br>`/updated`<br>`/skin_booster/products/4` | 원문부족 | B4 |
| O10 | 레티보 note '휴젤 보툴렉스의 수출용 브랜드명(미국·중국·유럽 등)' 은 같은 묶음의 보툴렉스(manufacturer 휴젤)를 가리키는 말로 읽힌다. 두 항목은 별도 항목으로 있고 mfds 는 둘 다 true. 관계는 확정하지 않는다. | `/botulinum_toxin/products/10/note`<br>`/botulinum_toxin/products/3/name`<br>`/botulinum_toxin/products/10/mfds`<br>`/botulinum_toxin/products/3/mfds` | 후속 | F2 |
| O11 | 뉴럭스 manufacturer '뉴메코(Newmeco, 메디톡스 계열)' — 괄호 안에 로마자명과 계열 표현이 함께 있다. '메디톡스' 는 메디톡신 항목의 manufacturer 값과 같은 문자열이다. | `/botulinum_toxin/products/9/manufacturer`<br>`/botulinum_toxin/products/5/manufacturer` | 후속 | F2 |
| O12 | 스킨보톡스 note '보톡스 희석' 의 '보톡스' 는 /botulinum_toxin/products/0/name 과 같은 문자열이다. | `/skin_booster/products/3/note`<br>`/botulinum_toxin/products/0/name` | 후속 | F2 |
| O13 | 같은 제조사로 보이는 값의 표기 변형: '클래시스'(2회) vs '클래시스(Classys)'(1회), '바임(VAIM/바임글로벌)'(2회). 괄호·'/' 의 역할이 원문에 정의되어 있지 않다. README 의 '/'·'+' 규칙은 시술 이름 작성 규칙이다. | `/energy_device/products/2/manufacturer`<br>`/energy_device/products/3/manufacturer`<br>`/energy_device/products/4/manufacturer`<br>`/biostimulator/products/3/manufacturer` | 후속 | F3 |
| O14 | manufacturer '앨러간/애브비' 2회 — '/' 가 대안·병기·인수 관계 중 무엇인지 원문에 없다. | `/botulinum_toxin/products/0/manufacturer`<br>`/filler_ha/products/0/manufacturer` | 원문부족 | B6 |
| O15 | 같은 manufacturer 문자열이 여러 항목에 나온다(값 그대로 셈): 멀츠 4항목·4묶음, 휴젤 4항목·2묶음(레티보 note 본문에도 1회), 사이노슈어 3·1묶음, 파마리서치 3·1묶음, 앨러간/애브비 2·2묶음, 갈더마 2·2묶음, 휴메딕스 2·2묶음, 싱클레어 2·2묶음, 한스바이오메드 2·2묶음, 리젠바이오텍 2·2묶음, 바임(VAIM/바임글로벌) 2·1묶음, 솔타메디컬 2·1묶음, 클래시스 2·1묶음(+ '클래시스(Classys)' 1), 제이시스메디칼 2·1묶음. 문자열 일치일 뿐 동일 개체로 확정하지 않는다. | `/botulinum_toxin/products/2/manufacturer`<br>`/filler_ha/products/3/manufacturer`<br>`/biostimulator/products/2/manufacturer`<br>`/energy_device/products/0/manufacturer` | 후속 | F3 |
| O16 | country 가 같은 manufacturer 문자열에 대해 항목마다 다르다: 멀츠 DE(제오민·벨로테로·래디어스) vs US(울쎄라), 갈더마 SE(레스틸렌) vs FR(스컬트라). country 가 제품·제조사·생산지 중 무엇의 국가인지 원문에 없다. 외부 확인은 하지 않았다. | `/botulinum_toxin/products/2/country`<br>`/energy_device/products/0/country`<br>`/filler_ha/products/1/country`<br>`/biostimulator/products/0/country` | 원문부족 | B7 |
| O17 | name 과 name_en 이 음역·번역으로 바로 대응하지 않는 항목: 제니스/AGNES, EXOSOME SKIN/ExoSCRT, ASCEplus/ASCE+, LDM/LDM-MED, 미라클/Miracle Thread, 시크릿/Secret RF, 리쥬란아이/Rejuran i, 에스에프/SF Injection, 클라리티2/Clarity II. 어느 쪽이 맞는지 원문만으로 정할 수 없다. | `/energy_device/products/10/name`<br>`/energy_device/products/10/name_en`<br>`/prp_exosome/products/4/name`<br>`/prp_exosome/products/4/name_en`<br>`/prp_exosome/products/3/name`<br>`/energy_device/products/17/name`<br>`/thread_lift/products/4/name_en`<br>`/energy_device/products/9/name_en`<br>`/skin_booster/products/2/name_en`<br>`/stem_cell/products/1/name_en`<br>`/energy_device/products/13/name_en` | 후속 | F4 |
| O18 | name 칸이 한글이 아닌 항목: ASCEplus, EXOSOME SKIN, LDM. | `/prp_exosome/products/3/name`<br>`/prp_exosome/products/4/name`<br>`/energy_device/products/17/name` | 잠정 | F4 |
| O19 | type 키는 묶음마다 담는 말의 종류가 다르다: energy_device 는 방식·매질(HIFU·RF·니들RF·피코레이저·Nd:YAG+알렉산드라이트·초음파 등), prp_exosome 은 형태(PRP키트·엑소좀), stem_cell 은 구성물(성장인자·줄기세포배양액). 같은 키 이름이 같은 정보 종류라는 근거는 없다. | `/energy_device/products/0/type`<br>`/energy_device/products/13/type`<br>`/prp_exosome/products/0/type`<br>`/prp_exosome/products/3/type`<br>`/stem_cell/products/0/type` | 잠정 | P2 |
| O20 | 성분·재질은 묶음에 따라 다른 키에 있다: biostimulator·skin_booster 는 ingredient, thread_lift 는 material. 값 안의 '+'(PDLLA+HA·PN+HA·PDO+PCL)와 '/'(PN/PDRN)의 뜻(혼합·대안·병기)은 원문에 없다. | `/biostimulator/products/3/ingredient`<br>`/skin_booster/products/0/ingredient`<br>`/skin_booster/products/1/ingredient`<br>`/thread_lift/products/1/material` | 후속 | F5 |
| O21 | 이름 끝 '+' 는 연산자로 볼 피연산자가 없다: '리쥬란 HB+'·'Rejuran HB+'·'ASCE+'. ASCEplus 는 '+' 를 'plus' 로 적은 것으로 보이나 확정하지 않는다. | `/skin_booster/products/1/name`<br>`/skin_booster/products/1/name_en`<br>`/prp_exosome/products/3/name_en`<br>`/prp_exosome/products/3/name` | 잠정 | F4 |
| O22 | 이름 계열로 보이는 항목군: 리쥬란 힐러·리쥬란 HB+·리쥬란아이, 쥬베룩·쥬베룩볼륨, 채움·더채움, 보톡스·스킨보톡스. 항목 사이의 제품군·변형 관계는 원문에 표시되어 있지 않다. | `/skin_booster/products/0/name`<br>`/skin_booster/products/1/name`<br>`/skin_booster/products/2/name`<br>`/biostimulator/products/3/name`<br>`/biostimulator/products/4/name`<br>`/filler_ha/products/5/name`<br>`/filler_ha/products/6/name` | 후속 | F6 |
| O23 | ASCEplus·EXOSOME SKIN 두 항목은 note·legal_warning·regulatory_status 세 값이 글자 단위로 같다. 이 세 키는 파일에서 이 두 항목에만 있다(note 는 다른 항목에도 있음). 법령·식약처 관련 서술은 원장의 서술이며 사실 확인하지 않았다. | `/prp_exosome/products/3/note`<br>`/prp_exosome/products/4/note`<br>`/prp_exosome/products/3/legal_warning`<br>`/prp_exosome/products/4/legal_warning`<br>`/prp_exosome/products/3/regulatory_status`<br>`/prp_exosome/products/4/regulatory_status` | 후속 | F7 |
| O24 | ASCEplus·EXOSOME SKIN 두 항목은 note·legal_warning·regulatory_status 세 값이 글자 단위로 같다. legal_warning·regulatory_status 키는 파일 전체에서 이 두 항목에만 있다(note 는 5항목). 법령·식약처 관련 서술은 원장의 서술이며 사실 확인하지 않았다. | `/prp_exosome/products/3/legal_warning` | 후속 | F7 |
| O25 | note '화장품 허가. 주사/주입 사용 금지' 와 regulatory_status '화장품 허가만 받은 제품 — 식약처의 주사·주입 용도 허가 없음' 은 같은 항목 안에서 '주사/주입'(슬래시)·'주사·주입'(가운뎃점) 으로 다르게 나열한다. | `/prp_exosome/products/3/note`<br>`/prp_exosome/products/3/regulatory_status` | 잠정 | F7 |
| O26 | stem_cell 묶음 항목의 type 은 '성장인자'·'줄기세포배양액' 이다. 묶음 키 'stem_cell' 과 type 값이 같은 정보 종류인지 원문에 없다. 두 항목 모두 mfds false 이고 note 가 없다. | `/stem_cell`<br>`/stem_cell/products/0/type`<br>`/stem_cell/products/1/type`<br>`/stem_cell/products/0/mfds` | 잠정 | P2 |
| O27 | 항목 59개의 키 구성은 묶음마다 다르다(§2 컬럼 구성 표의 '선택 필드'·'키 구성' 행). 모든 항목에 공통인 키는 name·name_en·manufacturer·country 4개다. mfds 41·type 25·ingredient 9·note 5·material 5·legal_warning 2·regulatory_status 2. | `/botulinum_toxin/products/0`<br>`/energy_device/products/0`<br>`/prp_exosome/products/3` | 잠정 |  |
| O28 | 인모드 항목은 name 과 manufacturer 가 같은 문자열 '인모드' 이다(name_en 'InMode'). 제품명·제조사명이 같은 것인지 원문 서술은 없다. | `/energy_device/products/6/name`<br>`/energy_device/products/6/manufacturer`<br>`/energy_device/products/6/name_en` | 잠정 | F3 |

## 5. 구조화 기록으로 가는 길

- 노드·키·구간·문맥: `source-map.json` (`nodes[].pointer` 로 찾기)
- 형태소: `morphology.json` `values[]`(적용) · `excluded_values[]`(제외 사유) · `field_names`(필드명 제외) · `segmentation_review`(알려진 오분절·오태깅, 출현별)
- 복합 표현: `expressions.json` (`manual.*` 는 직접 읽기, `regex.*` 는 보조 후보)
- 읽기 범위·검증: `validation.md` · 미결: `issues.md`
