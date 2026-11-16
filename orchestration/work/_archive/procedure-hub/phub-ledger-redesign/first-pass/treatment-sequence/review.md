# treatment-sequence.json — 1차 조사 (읽기용)

> 이 문서는 **원문 대응**과 **잠정 관찰**을 나눠 적는다. 원문 값 표(§2~§8의 「원문 값」)는 build.py 가 원본에서 자동 생성한 것이고, 「잠정 관찰」 절은 직접 읽고 쓴 해석 후보다. 잠정 관찰은 확정 의미·관계가 아니다. 공통 개념 ID·동의어·부위 체계·관계 방향은 정하지 않았다(1차 범위 밖).
> 원문의 임상·법적 주장(간격 일수, 근거 문헌, 금지 사유 등)은 **원장에 적혀 있다는 사실**로만 기록한다. 사실 여부는 검증하지 않았고 외부 자료로 보충하지 않았다.

**상태**: 1차 범위 종료(조건 충족, 코디 확인 전) · **원장 전체 완료 아님** — 미결은 [issues.md](./issues.md).

## 0. 원본과 기록 위치

| 항목 | 값 |
|---|---|
| 원본 | `orchestration/work/phub-recommend/bronze/phub-ledger/treatment-sequence.json` |
| 크기 | 8,964 bytes · 5,208 code points · UTF-8 · BOM 없음 · 개행 0(한 줄) · 백슬래시(이스케이프) 0 · BMP 밖 문자 0 |
| sha256 | `e2f74d41d75a0b4b9d1f6216ccc17402af64bbd455b1c1627395a819ce76cfaf` (작업 시작·build·verify·작업 끝 동일. 원장 폴더 `HASHES.txt` 의 접두 `e2f74d41d75a0b4b` 와도 일치) |
| 구조·값 | [source-map.json](./source-map.json) — 노드 255(전부), 키 출현 142, 필드명 22종 출현 위치, 중복 키 0 |
| 형태소 | [morphology.json](./morphology.json) — 문자열 164 중 분석 155 / 제외 9(사유별), 비문자열 말단 20, 필드명 22, 토큰 1,429 · 오분절 출현 기록 69([segmentation-review.json](./segmentation-review.json)) |
| 복합 표현 | [expressions.json](./expressions.json) — 후보 922(직접 읽기 수동 142 포함) · 알려진 오탐 19(출현별) |
| 미결 | [issues.md](./issues.md) |
| 검증 | [validation.md](./validation.md) · [validation-machine.json](./validation-machine.json) |
| 재현 | [build.py](./build.py) · [verify.py](./verify.py) · 수동 기록: [manual-expressions.json](./manual-expressions.json)(생성기 [manual-expressions-make.py](./manual-expressions-make.py)) · [segmentation-review.json](./segmentation-review.json)(생성기 [segmentation-review-make.py](./segmentation-review-make.py)) · 이 문서의 관찰 원고 [review-notes.md](./review-notes.md) |

구간 기준: 디코딩된 원문 문자열의 Unicode 코드 포인트 `[start,end)`. source-map 의 `span` 은 파일 전체 텍스트 기준(문자열은 따옴표 포함), `value_span` 은 따옴표 제외. morphology·expressions 의 `span` 은 해당 값 문자열 기준(파일 기준 = `value_span[0] + start`). UTF-8 바이트 구간은 `byte_span` 으로 따로 둔다. 이 원장은 이스케이프가 없어 JSON 리터럴 내부 구간과 디코딩 문자열이 같다(검증됨).

## 1. 읽기 범위 (실제로 한 일)

| 구획 | 범위 | 읽기 방식 |
|---|---|---|
| 상위 | `/version` `/updated` `/description` + 다섯 블록의 배열 길이 | 원본 한 줄 전체를 처음부터 끝까지 직접 읽음 |
| principles | `/principles/0` ~ `/principles/12` (13문장) | 1회차 원문 통독, 2회차 값마다 Kiwi 토큰을 원문과 나란히 대조, 3회차 표현 후보·절 분할 대조 |
| sequence_order | `/sequence_order/0` ~ `/10` 각 4필드(order·phase·categories 전 원소·reason) | 같음 |
| incompatible_same_day | `/incompatible_same_day/0` ~ `/8` 각 pair 전 원소·reason | 같음 |
| common_combos | `/common_combos/0` ~ `/7` 각 name·sequence 전 원소·total_time·(note) | 같음 |
| minimum_intervals | `/minimum_intervals/0` ~ `/8` 각 from·to·min_days/min_months·source·reason | 같음 |

- 자동 처리: 구조 열거·Pointer·구간·형태소 분석·regex/keyword 후보·Kiwi 품사 기반 수식 후보·수동 구절의 위치 찾기.
- 직접 처리: 원문 전체 통독, 155개 값의 토큰 1,429개 전체 열람(구두점·조사·어미는 위치만 확인), 규칙 후보 전 범주 열람 후 오탐 판정, 규칙 후보에 덮이지 않은 어절 목록 열람 후 수동 구절 보강, 절 분할 결과 열람 후 분할 규칙 수정(issues A1).
- 한계: 「별도 읽기 검토」는 같은 에이전트가 관점을 바꿔 다시 읽은 것이며 독립 검토자가 아니다.

## 2. 컬럼 구성 표 (자동 생성 — 원본 컬럼명·경로 패턴 그대로)

경로 패턴의 `*` 는 배열 색인. 「출현」은 그 패턴에 실제로 있는 노드 수, 「자료형」은 그 패턴의 실제 노드 자료형(변형이 있으면 행을 나눔). 예시는 첫 출현의 원문 JSON 리터럴과 Pointer.

| 원본 컬럼명 | 경로 패턴 | 자료형 / 중첩 | 출현 | 원문 예시(JSON 리터럴) | 예시 위치 | 비고(구조 사실) |
|---|---|---|---|---|---|---|
| `(루트)` | `(루트)` | object{8} | 1 | `{"version":"1.3","updated":"2026-07-26","description":"동일 세션 시술 조합 순서 …` | `` |  |
| `version` | `/version` | string | 1 | `"1.3"` | `/version` |  |
| `updated` | `/updated` | string | 1 | `"2026-07-26"` | `/updated` |  |
| `description` | `/description` | string | 1 | `"동일 세션 시술 조합 순서 가이드. 안전성과 효과 최적화 기준."` | `/description` |  |
| `principles` | `/principles` | array of string | 1 | `["클렌징 → 마취 → 시술 → 진정 순서 기본","보톡스와 HIFU/RF 열시술은 당일 병행 가능하나, 웬만하면 열시술을 먼…` | `/principles` | 길이 13 |
| `(배열 원소)` | `/principles/*` | string | 13 | `"클렌징 → 마취 → 시술 → 진정 순서 기본"` | `/principles/0` |  |
| `sequence_order` | `/sequence_order` | array of object | 1 | `[{"order":1,"phase":"클렌징/준비","categories":["M15-클렌징"],"reason":"시술 부위 …` | `/sequence_order` | 길이 11 |
| `(배열 원소)` | `/sequence_order/*` | object{4} | 11 | `{"order":1,"phase":"클렌징/준비","categories":["M15-클렌징"],"reason":"시술 부위 청…` | `/sequence_order/0` |  |
| `order` | `/sequence_order/*/order` | integer | 11 | `1` | `/sequence_order/0/order` |  |
| `phase` | `/sequence_order/*/phase` | string | 11 | `"클렌징/준비"` | `/sequence_order/0/phase` |  |
| `categories` | `/sequence_order/*/categories` | array of string | 11 | `["M15-클렌징"]` | `/sequence_order/0/categories` | 길이 1,2,3 |
| `(배열 원소)` | `/sequence_order/*/categories/*` | string | 19 | `"M15-클렌징"` | `/sequence_order/0/categories/0` |  |
| `reason` | `/sequence_order/*/reason` | string | 11 | `"시술 부위 청결, 메이크업 제거"` | `/sequence_order/0/reason` |  |
| `incompatible_same_day` | `/incompatible_same_day` | array of object | 1 | `[{"pair":["CO2 프락셔널","필러"],"reason":"열린 상처에 필러 주입 감염 위험"},{"pair":["심부…` | `/incompatible_same_day` | 길이 9 |
| `(배열 원소)` | `/incompatible_same_day/*` | object{2} | 9 | `{"pair":["CO2 프락셔널","필러"],"reason":"열린 상처에 필러 주입 감염 위험"}` | `/incompatible_same_day/0` |  |
| `pair` | `/incompatible_same_day/*/pair` | array of string | 9 | `["CO2 프락셔널","필러"]` | `/incompatible_same_day/0/pair` | 길이 1,2 |
| `(배열 원소)` | `/incompatible_same_day/*/pair/*` | string | 17 | `"CO2 프락셔널"` | `/incompatible_same_day/0/pair/0` |  |
| `reason` | `/incompatible_same_day/*/reason` | string | 9 | `"열린 상처에 필러 주입 감염 위험"` | `/incompatible_same_day/0/reason` |  |
| `common_combos` | `/common_combos` | array of object | 1 | `[{"name":"동안 기본","sequence":["슈링크 HIFU","보톡스 이마+미간","필러 팔자"],"total_ti…` | `/common_combos` | 길이 8 |
| `(배열 원소)` | `/common_combos/*` | object{3} | 5 | `{"name":"동안 기본","sequence":["슈링크 HIFU","보톡스 이마+미간","필러 팔자"],"total_tim…` | `/common_combos/0` |  |
| `name` | `/common_combos/*/name` | string | 8 | `"동안 기본"` | `/common_combos/0/name` |  |
| `sequence` | `/common_combos/*/sequence` | array of string | 8 | `["슈링크 HIFU","보톡스 이마+미간","필러 팔자"]` | `/common_combos/0/sequence` | 길이 3,4 |
| `(배열 원소)` | `/common_combos/*/sequence/*` | string | 26 | `"슈링크 HIFU"` | `/common_combos/0/sequence/0` |  |
| `total_time` | `/common_combos/*/total_time` | string | 8 | `"60-90분"` | `/common_combos/0/total_time` |  |
| `(배열 원소)` | `/common_combos/*` | object{4} | 3 | `{"name":"보톡스+필러+스킨부스터 원데이","sequence":["필러 팔자+볼","스킨부스터 리쥬란","보톡스 이마+미…` | `/common_combos/5` |  |
| `note` | `/common_combos/*/note` | string | 3 | `"필러 위치 안정화 먼저 → 스킨부스터 → 보톡스 마지막 순서 준수"` | `/common_combos/5/note` | 선택적: 8개 항목 중 3개에만 있음 |
| `minimum_intervals` | `/minimum_intervals` | array of object | 1 | `[{"from":"HA 필러","to":"RF/HIFU","min_days":14,"source":"JCD 2023; ASDS…` | `/minimum_intervals` | 길이 9 |
| `(배열 원소)` | `/minimum_intervals/*` | object{5} | 9 | `{"from":"HA 필러","to":"RF/HIFU","min_days":14,"source":"JCD 2023; ASDS …` | `/minimum_intervals/0` |  |
| `from` | `/minimum_intervals/*/from` | string | 9 | `"HA 필러"` | `/minimum_intervals/0/from` |  |
| `to` | `/minimum_intervals/*/to` | string | 9 | `"RF/HIFU"` | `/minimum_intervals/0/to` |  |
| `min_days` | `/minimum_intervals/*/min_days` | integer | 7 | `14` | `/minimum_intervals/0/min_days` | 선택적: 9개 항목 중 7개에만 있음 |
| `source` | `/minimum_intervals/*/source` | string | 9 | `"JCD 2023; ASDS 2024"` | `/minimum_intervals/0/source` |  |
| `reason` | `/minimum_intervals/*/reason` | string | 9 | `"주입 후 HA가 고온(>55°C) 노출 시 분해/변형 위험. 역순은 같은 날 가능"` | `/minimum_intervals/0/reason` |  |
| `min_months` | `/minimum_intervals/*/min_months` | integer | 2 | `0` | `/minimum_intervals/2/min_months` | 선택적: 9개 항목 중 2개에만 있음 |

### 구조 사실 (원문 대응)

- 최상위 객체 키 8개, 순서 `version` → `updated` → `description` → `principles` → `sequence_order` → `incompatible_same_day` → `common_combos` → `minimum_intervals`.
- `principles` 는 문자열 13개 배열. 나머지 네 블록은 객체 배열(11·9·8·9개).
- `sequence_order` 11개 모두 키 4개 같은 순서(`order, phase, categories, reason`). `order` 값은 배열 순서대로 1~11, 결번·중복 없음. `categories` 길이는 순서대로 1,2,3,3,2,2,1,1,1,1,2.
- `incompatible_same_day` 9개 모두 `pair, reason`. `pair` 길이는 `/incompatible_same_day/4` 만 **1**, 나머지 2.
- `common_combos` 8개 중 `note` 는 `/common_combos/5`·`/6`·`/7` 에만 있다(5개는 키 3개, 3개는 키 4개).
- `minimum_intervals` 9개는 `from, to, (min_days | min_months), source, reason` 순서. `min_days` 7개(14,5,14,14,14,0,14), `min_months` 2개(`/minimum_intervals/2` = 0, `/minimum_intervals/3` = 6). 한 항목에 둘이 함께 있는 경우는 없다.
- null·빈 문자열·빈 배열·빈 객체·실수·불리언 없음. 숫자는 모두 정수(`order` 11, `min_days` 7, `min_months` 2).
- 같은 문자열이 여러 위치에 반복된다(예: `레이저` 5곳, `필러` 4곳, `임상 가이드` 4곳, `이소트레티노인 복용 중` 3곳). 각 출현은 Pointer 별로 따로 기록했다.

### 잠정 관찰 (구조)

- 잠정: `description` 은 「동일 세션 시술 조합 순서 가이드」인데 `minimum_intervals` 와 `/principles/9`(별도 세션)는 세션 사이 간격을 다룬다. 원장의 실제 범위가 설명보다 넓다(issues C7).
- 잠정: `categories` 의 값 형태가 셋으로 갈린다 — `Mn-이름`(10), `Mn`(9), 코드 없는 이름(`국소마취`·`연고마취`). `Mn` 이 가리키는 대상은 이 원장 안에 정의가 없다(외부 참조 — issues B7).

## 3. 상위 스칼라 — 원문 값 (자동 생성, 전부)

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `version` | string | 1.3 | `/version` |
| `updated` | string | 2026-07-26 | `/updated` |
| `description` | string | 동일 세션 시술 조합 순서 가이드. 안전성과 효과 최적화 기준. | `/description` |
| `principles` | array[13] of string | (아래 절) | `/principles` |
| `sequence_order` | array[11] of object | (아래 절) | `/sequence_order` |
| `incompatible_same_day` | array[9] of object | (아래 절) | `/incompatible_same_day` |
| `common_combos` | array[8] of object | (아래 절) | `/common_combos` |
| `minimum_intervals` | array[9] of object | (아래 절) | `/minimum_intervals` |

## 4. principles — 원문 값 (자동 생성, 전부)

| 순서 | 원문 값 (`principles[i]`) | Pointer |
|---|---|---|
| 0 | 클렌징 → 마취 → 시술 → 진정 순서 기본 | `/principles/0` |
| 1 | 보톡스와 HIFU/RF 열시술은 당일 병행 가능하나, 웬만하면 열시술을 먼저 시행 | `/principles/1` |
| 2 | HIFU는 보톡스 주입 후 2주 이내 효력 저하 가능성을 고려해 HIFU 선행 또는 2주 이상 간격을 두며, RF·IPL·비침습 레이저는 당일 병행 가능 | `/principles/2` |
| 3 | 레이저/IPL은 필러 주입 전에 (부종 상태에서 레이저 위험) | `/principles/3` |
| 4 | MTS/니들RF 후 약물 도포는 멸균·시술용으로 허가된 성장인자·펩타이드·PRP·ALA 등 의료 제제로 한정. 화장품 분류 엑소좀·배양액의 개방 채널 전달은 미허가·위법 소지와 감염·육아종 위험이 있어 금지 | `/principles/4` |
| 5 | ⚠️ 채널 오픈(MTS/니들RF/프락셔널) 후 도포는 멸균·시술용으로 허가된 의료 제제만 사용. 화장품·코스메슈티컬(비타민C 세럼·비타민E 오일·식물추출물·향료·색소·보습젤 등)의 개방 채널 내 도포 금지 — 진피 내 이물 잔류로 육아종·지연성 과민반응·전신 과민반응 위험 | `/principles/5` |
| 6 | 침습도 높은 시술 먼저, 낮은 시술 나중에 | `/principles/6` |
| 7 | 출혈 위험 시술은 마지막에 | `/principles/7` |
| 8 | 같은 날 필러+보톡스: 필러 먼저(위치 안정화) → 보톡스 나중에 (필러 위치 보존, 전문가 합의 기반 기본값, 같은 날엔 순서 유연) | `/principles/8` |
| 9 | 별도 세션 필러+보톡스: 보톡스 먼저 → 2주 후 필러 (보톡스 효과 안정 후 필러 위치 정밀 결정) | `/principles/9` |
| 10 | HA 필러 → RF/HIFU: 최소 14일 간격 필수 (열에 의한 HA 분해 위험, JCD 2023) | `/principles/10` |
| 11 | RF/HIFU → 필러: 같은 날 가능 (에너지 기기 먼저, 필러 나중에). 역순(필러 주입 후 RF/HIFU)은 주입된 HA가 고열에 노출돼 분해/변형되므로 14일 이상 대기 | `/principles/11` |
| 12 | 필러 → 레이저: 최소 5일 간격 권장 | `/principles/12` |

### 잠정 관찰 (principles)

| Pointer | 관찰(잠정) |
|---|---|
| `/principles/0` | 「클렌징 → 마취 → 시술 → 진정」 4단 순서와 `sequence_order` 의 첫 두 phase·마지막 phase 가 대응해 보인다. 「기본」은 기본값이라는 수식. |
| `/principles/1` · `/principles/2` | 보톡스와 열시술(HIFU/RF)의 당일 병행은 「가능」, 순서는 「웬만하면 열시술 먼저」(선호). `/principles/2` 는 HIFU 에 한해 「HIFU 선행 또는 2주 이상 간격」을 두 선택지로 제시하고, RF·IPL·비침습 레이저는 당일 병행 가능으로 나눈다. 「효력 저하」의 대상(보톡스 효력인지)은 원문에 명시가 없다(issues B4). |
| `/principles/3` | 「레이저/IPL은 필러 주입 전에」 — 같은 세션 안 순서로 읽힌다. 괄호의 「부종 상태」는 필러 주입 뒤 상태로 추정되나 원문에 명시 없음. |
| `/principles/4` · `/principles/5` | 채널을 연 뒤 도포를 허가 의료 제제로 한정하고 화장품 분류 제제를 금지하는 같은 취지 문장이 둘 있다. 채널을 여는 시술 목록이 `/principles/4` 는 MTS/니들RF, `/principles/5` 는 MTS/니들RF/프락셔널로 다르다(issues C8). `/principles/5` 에만 「⚠️」 표지가 있다. |
| `/principles/6` · `/principles/7` | 「침습도 높은 시술」「출혈 위험 시술」의 판정 기준·목록이 원문에 없다(issues B2). |
| `/principles/8` · `/principles/9` | 같은 날은 「필러 먼저 → 보톡스 나중에」이되 「같은 날엔 순서 유연」, 별도 세션은 「보톡스 먼저 → 2주 후 필러」. 조건(같은 날/별도 세션)에 따라 방향이 반대다. |
| `/principles/10` ~ `/principles/12` | 기기·필러 사이 간격 세 규칙. 강도 표현이 `/principles/10` 「필수」, `/principles/12` 「권장」. 같은 내용이 `incompatible_same_day`·`minimum_intervals` 에 다른 강도로 다시 나온다(issues C1). `/principles/11` 은 정방향(RF/HIFU → 필러) 같은 날 가능과 역순 14일 이상 대기를 한 문장에 담는다. |

## 5. sequence_order — 원문 값 (자동 생성, 전부)

### `/sequence_order/0` — 키 4개: `order`, `phase`, `categories`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `order` | integer | 1 | `/sequence_order/0/order` |
| `phase` | string | 클렌징/준비 | `/sequence_order/0/phase` |
| `categories[0]` | string | M15-클렌징 | `/sequence_order/0/categories/0` |
| `reason` | string | 시술 부위 청결, 메이크업 제거 | `/sequence_order/0/reason` |

### `/sequence_order/1` — 키 4개: `order`, `phase`, `categories`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `order` | integer | 2 | `/sequence_order/1/order` |
| `phase` | string | 마취 | `/sequence_order/1/phase` |
| `categories[0]` | string | 국소마취 | `/sequence_order/1/categories/0` |
| `categories[1]` | string | 연고마취 | `/sequence_order/1/categories/1` |
| `reason` | string | 시술 30-60분 전 도포 | `/sequence_order/1/reason` |

### `/sequence_order/2` — 키 4개: `order`, `phase`, `categories`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `order` | integer | 3 | `/sequence_order/2/order` |
| `phase` | string | 에너지 기기 | `/sequence_order/2/phase` |
| `categories[0]` | string | M9-HIFU | `/sequence_order/2/categories/0` |
| `categories[1]` | string | M9-RF | `/sequence_order/2/categories/1` |
| `categories[2]` | string | M8-IPL | `/sequence_order/2/categories/2` |
| `reason` | string | 보톡스와 당일 병행 가능하나 웬만하면 열시술 먼저. HIFU는 보톡스 주입 후 2주 이내 효력 저하 가능성을 고려 | `/sequence_order/2/reason` |

### `/sequence_order/3` — 키 4개: `order`, `phase`, `categories`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `order` | integer | 4 | `/sequence_order/3/order` |
| `phase` | string | 레이저 | `/sequence_order/3/phase` |
| `categories[0]` | string | M8-토닝 | `/sequence_order/3/categories/0` |
| `categories[1]` | string | M8-프락셔널 | `/sequence_order/3/categories/1` |
| `categories[2]` | string | M8-혈관 | `/sequence_order/3/categories/2` |
| `reason` | string | 에너지 기기 다음, 주사 전 | `/sequence_order/3/reason` |

### `/sequence_order/4` — 키 4개: `order`, `phase`, `categories`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `order` | integer | 5 | `/sequence_order/4/order` |
| `phase` | string | 니들RF/MTS | `/sequence_order/4/phase` |
| `categories[0]` | string | M11 | `/sequence_order/4/categories/0` |
| `categories[1]` | string | M12 | `/sequence_order/4/categories/1` |
| `reason` | string | 채널 오픈 → 이후 약물 흡수 촉진 | `/sequence_order/4/reason` |

### `/sequence_order/5` — 키 4개: `order`, `phase`, `categories`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `order` | integer | 6 | `/sequence_order/5/order` |
| `phase` | string | 주사-필러 | `/sequence_order/5/phase` |
| `categories[0]` | string | M2 | `/sequence_order/5/categories/0` |
| `categories[1]` | string | M3 | `/sequence_order/5/categories/1` |
| `reason` | string | 같은 날 조합 시 필러 먼저 — 필러는 몰딩/마사지가 필요하고 보톡스 주입 부위는 이후 마사지 시 독소 확산(근육 처짐) 위험이 있어(ASPS 권고), 필러를 먼저 완료해 보톡스 부위를 건드리지 않게 함. 순서 자체의 근거는 전문가 컨센서스(Global Aesthetics Consensus 2016; Derm Surg)로 같은 날이면 어느 순서든 허용되며 RCT 근거는 아님(이론적/합의 수준) | `/sequence_order/5/reason` |

### `/sequence_order/6` — 키 4개: `order`, `phase`, `categories`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `order` | integer | 7 | `/sequence_order/6/order` |
| `phase` | string | 주사-스킨부스터 | `/sequence_order/6/phase` |
| `categories[0]` | string | M4 | `/sequence_order/6/categories/0` |
| `reason` | string | 필러 위치 확정 후 넓은 범위 스킨부스터 | `/sequence_order/6/reason` |

### `/sequence_order/7` — 키 4개: `order`, `phase`, `categories`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `order` | integer | 8 | `/sequence_order/7/order` |
| `phase` | string | 주사-보톡스 | `/sequence_order/7/phase` |
| `categories[0]` | string | M1 | `/sequence_order/7/categories/0` |
| `reason` | string | 같은 날 조합 시 보톡스 마지막 — 단백질 약물이므로 열 시술 뒤에, 필러 위치 확정 후 투여 | `/sequence_order/7/reason` |

### `/sequence_order/8` — 키 4개: `order`, `phase`, `categories`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `order` | integer | 9 | `/sequence_order/8/order` |
| `phase` | string | 주사-PRP/성장인자 | `/sequence_order/8/phase` |
| `categories[0]` | string | M5 | `/sequence_order/8/categories/0` |
| `reason` | string | MTS/니들RF 후 채널 통해 성장인자 흡수 극대화 | `/sequence_order/8/reason` |

### `/sequence_order/9` — 키 4개: `order`, `phase`, `categories`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `order` | integer | 10 | `/sequence_order/9/order` |
| `phase` | string | 약물 도포/침투 | `/sequence_order/9/phase` |
| `categories[0]` | string | M15-도포 | `/sequence_order/9/categories/0` |
| `reason` | string | MTS/니들RF 후 채널을 통한 경피 전달은 멸균·허가 의료 제제(성장인자·펩타이드·PRP·ALA 등)로 한정. 화장품 분류 엑소좀·배양액 및 코스메슈티컬의 채널 내 도포는 미허가·위법 소지와 감염·육아종·과민반응 위험이 있어 금지 | `/sequence_order/9/reason` |

### `/sequence_order/10` — 키 4개: `order`, `phase`, `categories`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `order` | integer | 11 | `/sequence_order/10/order` |
| `phase` | string | 진정/마무리 | `/sequence_order/10/phase` |
| `categories[0]` | string | M15-LED | `/sequence_order/10/categories/0` |
| `categories[1]` | string | M15-팩 | `/sequence_order/10/categories/1` |
| `reason` | string | 항염, 진정, 재생 촉진 | `/sequence_order/10/reason` |


### 잠정 관찰 (sequence_order)

| Pointer | 관찰(잠정) |
|---|---|
| `/sequence_order/2` | `categories` 에 `M9-HIFU`·`M9-RF`·`M8-IPL` 이 함께 있다. `M8` 은 `/sequence_order/3`(레이저)에도 `M8-토닝`·`M8-프락셔널`·`M8-혈관` 으로 나온다 — 같은 코드 접두가 두 phase 에 걸친 구조 사실. 코드 체계 해석은 하지 않았다. |
| `/sequence_order/2/reason` | 「…가능성을 고려」로 끝나며 그 결과 행동(선행 또는 간격)은 `/principles/2` 에만 있다(issues B4). |
| `/sequence_order/3/reason` | 「에너지 기기 다음, 주사 전」 — 다른 phase 이름으로 앞뒤를 정한다. phase 이름이 순서 관계의 참조 대상으로 쓰인다. |
| `/sequence_order/5` ~ `/sequence_order/8` | phase 이름이 모두 「주사-」 접두. 주사 묶음 안의 순서가 필러(6) → 스킨부스터(7) → 보톡스(8) → PRP/성장인자(9). |
| `/sequence_order/5/reason` | 같은 날 필러 먼저의 이유(몰딩/마사지, 독소 확산 위험, ASPS 권고)와 근거 수준(전문가 컨센서스, RCT 근거 아님), 완화(「같은 날이면 어느 순서든 허용」)가 한 값에 함께 있다. |
| `/sequence_order/7/reason` | 「보톡스 마지막」이지만 order 8 이고 뒤에 PRP(9)·약물 도포(10)·진정(11)이 있다. 「마지막」이 주사 묶음 안에서인지 원문만으로 정할 수 없다(issues C3). |
| `/sequence_order/9/reason` | `/principles/4` 와 같은 제한을 경피 전달 관점으로 다시 적고, 위험 목록에 「과민반응」이 더해졌다. |
| `/sequence_order/1/categories` · `/sequence_order/4~8/categories` | 마취 phase 의 두 값만 코드가 없다. 니들RF/MTS(M11·M12), 필러(M2·M3)처럼 `phase` 이름의 두 요소와 두 코드의 대응은 이 원장에 적혀 있지 않다. |

## 6. incompatible_same_day — 원문 값 (자동 생성, 전부)

### `/incompatible_same_day/0` — 키 2개: `pair`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `pair[0]` | string | CO2 프락셔널 | `/incompatible_same_day/0/pair/0` |
| `pair[1]` | string | 필러 | `/incompatible_same_day/0/pair/1` |
| `reason` | string | 열린 상처에 필러 주입 감염 위험 | `/incompatible_same_day/0/reason` |

### `/incompatible_same_day/1` — 키 2개: `pair`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `pair[0]` | string | 심부 필링(페놀) | `/incompatible_same_day/1/pair/0` |
| `pair[1]` | string | 레이저 | `/incompatible_same_day/1/pair/1` |
| `reason` | string | 이중 피부 손상 | `/incompatible_same_day/1/reason` |

### `/incompatible_same_day/2` — 키 2개: `pair`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `pair[0]` | string | PDO실 | `/incompatible_same_day/2/pair/0` |
| `pair[1]` | string | 비가교HA | `/incompatible_same_day/2/pair/1` |
| `reason` | string | HA가 PDO를 24-72시간 내 분해 가능 (in vitro 연구). 실제 임상에서는 병용 시술되는 경우가 많고 in vivo 재현성은 아직 검증 중 — 같은 부위 즉시 병용은 보수적으로 피함 | `/incompatible_same_day/2/reason` |

### `/incompatible_same_day/3` — 키 2개: `pair`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `pair[0]` | string | 이소트레티노인 복용 중 | `/incompatible_same_day/3/pair/0` |
| `pair[1]` | string | 프락셔널/필링 | `/incompatible_same_day/3/pair/1` |
| `reason` | string | 활성 복용 중에는 의사 판단이 필요. 비박리성 프락셔널·얕은 필링은 중단 후 0~2개월 내에도 개별 위험평가 하에 고려 가능하며, 6개월 대기는 전안면 박리성 재표면화·기계적 박피에 한정 | `/incompatible_same_day/3/reason` |

### `/incompatible_same_day/4` — 키 2개: `pair`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `pair[0]` | string | HA 필러 주입 후 RF/HIFU | `/incompatible_same_day/4/pair/0` |
| `reason` | string | 주입 후 HA가 고온(>55°C) 노출 시 분해/변형 위험 — 최소 14일 간격 권장. 역순(RF/HIFU 먼저 → 필러 나중)은 같은 날 가능. ASDS 2024 Filler Complication Guidelines; JCD 2023 | `/incompatible_same_day/4/reason` |

### `/incompatible_same_day/5` — 키 2개: `pair`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `pair[0]` | string | HA 필러 | `/incompatible_same_day/5/pair/0` |
| `pair[1]` | string | 레이저 | `/incompatible_same_day/5/pair/1` |
| `reason` | string | 부종/열 상호작용 — 최소 5일 간격 필요 | `/incompatible_same_day/5/reason` |

### `/incompatible_same_day/6` — 키 2개: `pair`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `pair[0]` | string | 심부 필링(TCA 50%+/페놀) | `/incompatible_same_day/6/pair/0` |
| `pair[1]` | string | 모든 시술 | `/incompatible_same_day/6/pair/1` |
| `reason` | string | 피부 장벽 완전 파괴 상태 — 충분한 회복 후에만 다른 시술 가능 | `/incompatible_same_day/6/reason` |

### `/incompatible_same_day/7` — 키 2개: `pair`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `pair[0]` | string | 이소트레티노인 복용 중 | `/incompatible_same_day/7/pair/0` |
| `pair[1]` | string | 프락셔널 레이저 | `/incompatible_same_day/7/pair/1` |
| `reason` | string | 비박리성 얕은 프락셔널은 중단 후 0~2개월 내에도 의사 판단 하에 고려 가능. 전안면 박리성 재표면화는 중단 후 6개월 대기 | `/incompatible_same_day/7/reason` |

### `/incompatible_same_day/8` — 키 2개: `pair`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `pair[0]` | string | 이소트레티노인 복용 중 | `/incompatible_same_day/8/pair/0` |
| `pair[1]` | string | 케미컬 필링 | `/incompatible_same_day/8/pair/1` |
| `reason` | string | 얕은 필링은 중단 후 0~2개월 내에도 의사 판단 하에 고려 가능. 심부 필링·기계적 박피는 중단 후 6개월 대기 | `/incompatible_same_day/8/reason` |


### 잠정 관찰 (incompatible_same_day)

| Pointer | 관찰(잠정) |
|---|---|
| 블록 전체 | 이름은 「같은 날 불가」이지만 내용은 섞여 있다: 같은 날 회피(`/0`·`/1`·`/2`), 복용 상태와 중단 후 기간(`/3`·`/7`·`/8`), 방향 있는 간격 규칙(`/4`·`/5`), 모든 시술 대상(`/6`). `/4` 의 reason 은 「역순…같은 날 가능」까지 말한다(issues C2). |
| `/incompatible_same_day/2` | 원문이 스스로 근거 수준(in vitro)·반대 사실(실제 임상에서 병용 많음)·불확실성(in vivo 검증 중)·범위(같은 부위 즉시)·강도(보수적으로 피함)를 모두 담는다. |
| `/incompatible_same_day/3` · `/7` · `/8` | `pair[0]` 이 시술이 아닌 「이소트레티노인 복용 중」. reason 은 복용 중이 아니라 **중단 후** 0~2개월·6개월을 말한다. 상대 표현이 「프락셔널/필링」「프락셔널 레이저」「케미컬 필링」으로 겹치며 갈린다(issues C5). |
| `/incompatible_same_day/4` | `pair` 원소가 1개이고 그 안에 순서(「HA 필러 주입 후 RF/HIFU」)가 문자열로 들어 있다. |
| `/incompatible_same_day/5` | pair 는 방향이 없는데 reason 은 「최소 5일 간격 필요」. `/principles/3`(레이저 먼저 같은 세션)과 `/minimum_intervals/1`(HA 필러 → 레이저 5일)을 함께 보면 방향에 따라 다른 규칙일 수 있으나 이 항목만으로는 정할 수 없다(issues B6). |
| `/incompatible_same_day/6/pair/0` | 「TCA 50%+」의 「+」는 README 의 「+ = 함께」가 아니라 「이상」으로 읽힌다(잠정, issues B9). |

## 7. common_combos — 원문 값 (자동 생성, 전부)

### `/common_combos/0` — 키 3개: `name`, `sequence`, `total_time`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `name` | string | 동안 기본 | `/common_combos/0/name` |
| `sequence[0]` | string | 슈링크 HIFU | `/common_combos/0/sequence/0` |
| `sequence[1]` | string | 보톡스 이마+미간 | `/common_combos/0/sequence/1` |
| `sequence[2]` | string | 필러 팔자 | `/common_combos/0/sequence/2` |
| `total_time` | string | 60-90분 | `/common_combos/0/total_time` |

### `/common_combos/1` — 키 3개: `name`, `sequence`, `total_time`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `name` | string | 피부결 개선 | `/common_combos/1/name` |
| `sequence[0]` | string | IPL | `/common_combos/1/sequence/0` |
| `sequence[1]` | string | 레이저토닝 | `/common_combos/1/sequence/1` |
| `sequence[2]` | string | 스킨부스터 | `/common_combos/1/sequence/2` |
| `total_time` | string | 45-60분 | `/common_combos/1/total_time` |

### `/common_combos/2` — 키 3개: `name`, `sequence`, `total_time`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `name` | string | 리프팅 풀코스 | `/common_combos/2/name` |
| `sequence[0]` | string | 울쎄라 HIFU | `/common_combos/2/sequence/0` |
| `sequence[1]` | string | 보톡스 턱선 | `/common_combos/2/sequence/1` |
| `sequence[2]` | string | 필러 볼+턱 | `/common_combos/2/sequence/2` |
| `sequence[3]` | string | 스킨부스터 | `/common_combos/2/sequence/3` |
| `total_time` | string | 90-120분 | `/common_combos/2/total_time` |

### `/common_combos/3` — 키 3개: `name`, `sequence`, `total_time`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `name` | string | 여드름 집중 | `/common_combos/3/name` |
| `sequence[0]` | string | MTS(미세채널 오픈) | `/common_combos/3/sequence/0` |
| `sequence[1]` | string | ALA 도포·배양 | `/common_combos/3/sequence/1` |
| `sequence[2]` | string | 광조사(PDT) | `/common_combos/3/sequence/2` |
| `sequence[3]` | string | 진정팩 | `/common_combos/3/sequence/3` |
| `total_time` | string | 60분 | `/common_combos/3/total_time` |

### `/common_combos/4` — 키 3개: `name`, `sequence`, `total_time`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `name` | string | 색소 집중 | `/common_combos/4/name` |
| `sequence[0]` | string | 피코토닝 | `/common_combos/4/sequence/0` |
| `sequence[1]` | string | IPL | `/common_combos/4/sequence/1` |
| `sequence[2]` | string | 비타민C 이온토포레시스 | `/common_combos/4/sequence/2` |
| `total_time` | string | 45분 | `/common_combos/4/total_time` |

### `/common_combos/5` — 키 4개: `name`, `sequence`, `total_time`, `note`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `name` | string | 보톡스+필러+스킨부스터 원데이 | `/common_combos/5/name` |
| `sequence[0]` | string | 필러 팔자+볼 | `/common_combos/5/sequence/0` |
| `sequence[1]` | string | 스킨부스터 리쥬란 | `/common_combos/5/sequence/1` |
| `sequence[2]` | string | 보톡스 이마+미간 | `/common_combos/5/sequence/2` |
| `total_time` | string | 60-90분 | `/common_combos/5/total_time` |
| `note` | string | 필러 위치 안정화 먼저 → 스킨부스터 → 보톡스 마지막 순서 준수 | `/common_combos/5/note` |

### `/common_combos/6` — 키 4개: `name`, `sequence`, `total_time`, `note`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `name` | string | 리프팅 + 피부결 | `/common_combos/6/name` |
| `sequence[0]` | string | HIFU 울쎄라 | `/common_combos/6/sequence/0` |
| `sequence[1]` | string | 토닝 | `/common_combos/6/sequence/1` |
| `sequence[2]` | string | 스킨부스터 | `/common_combos/6/sequence/2` |
| `total_time` | string | 90분 | `/common_combos/6/total_time` |
| `note` | string | 에너지 기기(HIFU) 먼저 → 레이저 토닝 → 스킨부스터 마지막 | `/common_combos/6/note` |

### `/common_combos/7` — 키 4개: `name`, `sequence`, `total_time`, `note`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `name` | string | 흉터 집중 | `/common_combos/7/name` |
| `sequence[0]` | string | 프락셔널 CO2 | `/common_combos/7/sequence/0` |
| `sequence[1]` | string | MTS | `/common_combos/7/sequence/1` |
| `sequence[2]` | string | PRP 도포 | `/common_combos/7/sequence/2` |
| `total_time` | string | 60분 | `/common_combos/7/total_time` |
| `note` | string | 프락셔널+MTS 채널 오픈 후 PRP 성장인자 경피 침투 극대화 | `/common_combos/7/note` |


### 잠정 관찰 (common_combos)

| Pointer | 관찰(잠정) |
|---|---|
| 블록 전체 | `sequence` 배열 순서가 시행 순서라는 말은 원문에 없다. `note` 가 있는 3개(`/5`·`/6`·`/7`)만 순서를 문장으로 말한다(issues B5). |
| `/common_combos/0` · `/2` | 배열 순서가 HIFU → 보톡스 → 필러(…→ 스킨부스터)인데 `sequence_order` 는 필러(6) → 스킨부스터(7) → 보톡스(8). 배열이 시행 순서라면 `/principles/8` 의 같은 날 기본 순서와 다르다. 다만 `/principles/8` 이 같은 날 순서를 유연하다고도 하므로 충돌인지 정할 수 없다(issues C4). |
| `/common_combos/4` | 피코토닝(레이저) → IPL 순서. `sequence_order` 는 IPL(3) → 레이저(4). 같은 조건부 관찰(issues C4). |
| `/common_combos/5/note` | 「순서 준수」 — 같은 원장의 「같은 날엔 순서 유연」(`/principles/8`)보다 강한 표현(issues C3). |
| 이름 표면형 | 「울쎄라 HIFU」(`/2/sequence/0`)·「HIFU 울쎄라」(`/6/sequence/0`), 「레이저토닝」(`/1/sequence/1`)·「토닝」(`/6/sequence/1`)·「레이저 토닝」(`/6/note`), 「프락셔널 CO2」(`/7/sequence/0`)·「CO2 프락셔널」(`/incompatible_same_day/0/pair/0`). 같은 대상인지 정하지 않았다(issues C6). |
| 부위 표현 | 「보톡스 이마+미간」「필러 팔자」「보톡스 턱선」「필러 볼+턱」「필러 팔자+볼」 — 시술·부위가 한 문자열에 붙어 있다. 분리는 후속. |

## 8. minimum_intervals — 원문 값 (자동 생성, 전부)

### `/minimum_intervals/0` — 키 5개: `from`, `to`, `min_days`, `source`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `from` | string | HA 필러 | `/minimum_intervals/0/from` |
| `to` | string | RF/HIFU | `/minimum_intervals/0/to` |
| `min_days` | integer | 14 | `/minimum_intervals/0/min_days` |
| `source` | string | JCD 2023; ASDS 2024 | `/minimum_intervals/0/source` |
| `reason` | string | 주입 후 HA가 고온(>55°C) 노출 시 분해/변형 위험. 역순은 같은 날 가능 | `/minimum_intervals/0/reason` |

### `/minimum_intervals/1` — 키 5개: `from`, `to`, `min_days`, `source`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `from` | string | HA 필러 | `/minimum_intervals/1/from` |
| `to` | string | 레이저 | `/minimum_intervals/1/to` |
| `min_days` | integer | 5 | `/minimum_intervals/1/min_days` |
| `source` | string | 임상 가이드 | `/minimum_intervals/1/source` |
| `reason` | string | 부종/열 상호작용 | `/minimum_intervals/1/reason` |

### `/minimum_intervals/2` — 키 5개: `from`, `to`, `min_months`, `source`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `from` | string | 이소트레티노인 | `/minimum_intervals/2/from` |
| `to` | string | 프락셔널/얕은 필링 | `/minimum_intervals/2/to` |
| `min_months` | integer | 0 | `/minimum_intervals/2/min_months` |
| `source` | string | ASDS 2017 consensus; AAD 2024 | `/minimum_intervals/2/source` |
| `reason` | string | 비박리성 프락셔널·얕은 필링은 6개월 일률 대기 근거가 부족하며 중단 후 0~2개월 범위에서 의사 판단. 6개월 대기는 전안면 박리성 재표면화·기계적 박피에 한정 | `/minimum_intervals/2/reason` |

### `/minimum_intervals/3` — 키 5개: `from`, `to`, `min_months`, `source`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `from` | string | 이소트레티노인 | `/minimum_intervals/3/from` |
| `to` | string | 박리성(ablative) 레이저/심부 필링 | `/minimum_intervals/3/to` |
| `min_months` | integer | 6 | `/minimum_intervals/3/min_months` |
| `source` | string | AAD 2024; ASDS 2017 consensus | `/minimum_intervals/3/source` |
| `reason` | string | 전안면 박리성 재표면화·기계적 박피에 한해 중단 후 6개월 대기. 국소 부위·비박리성 시술에는 적용하지 않음 | `/minimum_intervals/3/reason` |

### `/minimum_intervals/4` — 키 5개: `from`, `to`, `min_days`, `source`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `from` | string | 심부 필링 | `/minimum_intervals/4/from` |
| `to` | string | 레이저 | `/minimum_intervals/4/to` |
| `min_days` | integer | 14 | `/minimum_intervals/4/min_days` |
| `source` | string | 임상 가이드 | `/minimum_intervals/4/source` |
| `reason` | string | 피부 장벽 회복 필요 | `/minimum_intervals/4/reason` |

### `/minimum_intervals/5` — 키 5개: `from`, `to`, `min_days`, `source`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `from` | string | 프락셔널 CO2 | `/minimum_intervals/5/from` |
| `to` | string | 필러 | `/minimum_intervals/5/to` |
| `min_days` | integer | 14 | `/minimum_intervals/5/min_days` |
| `source` | string | 피부 회복 | `/minimum_intervals/5/source` |
| `reason` | string | 열린 상처 회복 후 주입 안전성 확보 | `/minimum_intervals/5/reason` |

### `/minimum_intervals/6` — 키 5개: `from`, `to`, `min_days`, `source`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `from` | string | 보톡스 | `/minimum_intervals/6/from` |
| `to` | string | 필러 (별도 세션) | `/minimum_intervals/6/to` |
| `min_days` | integer | 14 | `/minimum_intervals/6/min_days` |
| `source` | string | PRS 논문 | `/minimum_intervals/6/source` |
| `reason` | string | 보톡스 효과 안정화 후 필러 위치 정밀 결정 | `/minimum_intervals/6/reason` |

### `/minimum_intervals/7` — 키 5개: `from`, `to`, `min_days`, `source`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `from` | string | RF/HIFU | `/minimum_intervals/7/from` |
| `to` | string | 필러 | `/minimum_intervals/7/to` |
| `min_days` | integer | 0 | `/minimum_intervals/7/min_days` |
| `source` | string | 임상 가이드 | `/minimum_intervals/7/source` |
| `reason` | string | 같은 날 가능 — 에너지 기기 먼저, 필러 나중에 | `/minimum_intervals/7/reason` |

### `/minimum_intervals/8` — 키 5개: `from`, `to`, `min_days`, `source`, `reason`

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `from` | string | 필러 | `/minimum_intervals/8/from` |
| `to` | string | 필러 (동일 부위 재시술) | `/minimum_intervals/8/to` |
| `min_days` | integer | 14 | `/minimum_intervals/8/min_days` |
| `source` | string | 임상 가이드 | `/minimum_intervals/8/source` |
| `reason` | string | 부종 해소 후 정확한 평가 가능 | `/minimum_intervals/8/reason` |


### 잠정 관찰 (minimum_intervals)

| Pointer | 관찰(잠정) |
|---|---|
| 블록 전체 | `from` → `to` 는 방향 있는 쌍으로 보인다(필드명 기준 잠정). 숫자 칸은 `min_days` 또는 `min_months`. |
| `/minimum_intervals/2` | `min_months` = 0 이고 reason 은 「중단 후 0~2개월 범위에서 의사 판단」. 0 이 하한인지, 대기 없음인지 원문만으로 정할 수 없다(issues B1). 잠정 해석: reason 의 「0~2개월 범위」로 보아 0 은 그 범위의 **하한일 수 있다**(확정 아님). 숫자 칸만 단독으로 쓰면 「대기 0개월(=즉시 가능)」로 읽힐 위험이 있어 reason 과 함께 읽어야 한다. |
| `/minimum_intervals/3` | reason 이 적용 범위를 「전안면 박리성 재표면화·기계적 박피에 한해」로 좁히고 「국소 부위·비박리성 시술에는 적용하지 않음」으로 제외한다. `to` 는 「박리성(ablative) 레이저/심부 필링」. |
| `/minimum_intervals/7` | `min_days` = 0, reason 「같은 날 가능」 — 최소 간격 블록 안의 같은 날 허용. `/minimum_intervals/0` 과 from/to 가 뒤바뀐 쌍. |
| `/minimum_intervals/6` | `to` = 「필러 (별도 세션)」 — 세션 조건이 대상 문자열 안 괄호에 있다. `/principles/9` 는 「2주 후」, 여기는 `min_days` 14(최소). |
| `/minimum_intervals/8` | `from`·`to` 가 같은 「필러」이고 `to` 괄호에 「동일 부위 재시술」. |
| `source` | 문헌 표기(JCD·ASDS·AAD·PRS)와 비특정 표현(「임상 가이드」 4곳), 출처가 아닌 문구(「피부 회복」, `/minimum_intervals/5/source`)가 섞여 있다(issues B8). |

## 9. 형태소·표현 수집 요약

- 분석기: Kiwi(kiwipiepy 0.24.1 / kiwipiepy_model 0.24.0), `Kiwi(num_workers=1, model_type='cong')`, 사용자 사전 없음, tokenize 기본 옵션, 원문 정규화 없음. 기본형은 Kiwi `Token.lemma` 그대로.
- 제외 9: `/version`(버전 문자열), `/updated`(날짜), 한글 없는 카테고리 코드 7(`M11` `M12` `M2` `M3` `M4` `M1` `M5`). 비문자열 말단 20(정수)은 리터럴만 보존. 필드명 22종은 값과 따로 분석(영문 snake_case → Kiwi SL + underscore 규칙 분할).
- 알려진 오분절 69출현(교정 안 함, 원시 토큰 유지): 의미 영향 큰 것 — 「열시술/열 시술」→ 열/NR(수사) 4출현, 「필러」→ 필+러/EC 5출현, 「박리성·비박리성」 분절 9출현, 「전안면」→ 저/NP+ᆫ 2출현, 「(에) 한해」→ 한/MM+해/NNB(1년) 1출현, 「>」→ SSC 2출현, 부위 「이마」「팔자」 4출현, 「진정」→ MAG 2출현, 「육아종」「이물」「세럼」「몰딩」「니들」「경피」「리쥬란」「나중」「유연」 각 출현. 전체 목록·영향은 [segmentation-review.json](./segmentation-review.json), 요약은 issues A2.
- 표현 후보 922: 값 전체 155 · 절 분할 · regex/keyword 13규칙 · Kiwi 품사(MAG/MM/VCN/VX/MAJ) 수식 구절 · 직접 읽기 수동 142. 알려진 오탐 19(부분일치 8 · 범주 불일치 3 · 오태깅 유래 8)는 지우지 않고 [manual-expressions.json](./manual-expressions.json) `known_false_positives` 에 출현별로 둔다. 규칙 후보는 탐색 보조이며 전수 의미 해석이 아니다.

## 10. 상태

| 항목 | 상태 |
|---|---|
| **1차 범위 종료** | 종료 조건 충족(아래 전 항목) — 코디 확인 전 |
| **원장 전체 완료** | **아님** — 원문 부족 B 10 · 원문 내 불일치 C 8 · 후속 의미 조사 D 8 열림 |
| 전수 읽기 | 상위 3 + 5블록 전 항목 전 필드, 3회 통독(같은 에이전트) |
| 구조·값 수집 | 노드 255/255 · 키 142 · 중복 키 0 · 말단 184(문자열 164 + 정수 20) |
| 형태소·표현 수집 | 분석 155 / 제외 9 / 비문자열 20 · 토큰 1,429 · 오분절 기록 69 · 표현 922(수동 142, 오탐 19 표시) |
| 기계 검증 | build 내장 12검사 + 독립 verify.py 32검사 통과, 변이 시험 검출(validation.md) |
| 읽기 검토 | 같은 에이전트 별도 관점 재독 — 수식·조건·부정·오분절 영향 대조(validation.md §3). 독립 검토 없음 |
| 알려진 분석 오류 | 오분절 69(표시, 교정 아님) · 표현 오탐 19(표시) |
| 열린 미결 | B 10 · C 8 · D 8 · 사용자 선택 대기 0(issues E) |
| 후속 의미 조사 | 시작 안 함 |
