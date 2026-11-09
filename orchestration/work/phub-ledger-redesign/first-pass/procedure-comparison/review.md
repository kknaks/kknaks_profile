# procedure-comparison.json — 1차 조사 (읽기용)

> **상태: 1차 수집 범위 종료(코디 확인 전) · 원장 전체 완료 아님.** 원문 부족 B 9묶음, 후속 의미 조사 F 7묶음, 알려진 형태소·표현 한계(A1~A4)가 열려 있고 사용자 선택 대기는 0건이다. 이 표시는 batch-01 묶음 검토 §3.2 형식 비고에 따라 §7 의 상태를 맨 위에 올린 것이며, 의미 조사·정규화 완료가 아니다. 상세는 [§7 상태](#7-상태).

> 원문 대응(§2·§3)과 잠정 관찰(§4)을 나눠 적는다. 「잠정」은 원문을 근거로 한 해석 후보일 뿐 확정된 의미·관계가 아니다. 공통 개념 ID·동의어 병합·부위 체계·관계 방향은 정하지 않았다(1차 범위 밖).
> 원문의 임상 주장(효과·위험·RR·근거수준·가격)은 **원장에 그렇게 적혀 있다는 사실**로만 기록한다. 사실 여부는 검증하지 않았고 외부 자료로 보충하지 않았다.
> 이 파일은 `build.py` 가 `review-template.md`(손으로 쓴 부분)에 원문 표(§2·§3·§5·§6)를 채워 만든다. 원문 표는 원본에서 직접 생성하므로 손으로 옮겨 적다 생기는 오기는 없다.

## 0. 원본과 기록 위치

| 항목 | 값 |
|---|---|
| 원본 | `orchestration/work/phub-recommend/bronze/phub-ledger/procedure-comparison.json` |
| 크기 | 18,002 bytes · 12,088 code points · UTF-8 · BOM 없음 · 개행 0(한 줄) · 백슬래시 이스케이프 0 · BMP 밖 문자 0 |
| sha256 | `eba7ae5af919ef77ff52cb07b2f6117b458751319f530f38cf30c61e94989571` (작업 시작·끝 동일, `HASHES.txt` 의 앞 16자리 `eba7ae5af919ef77` 와 일치) |
| 구조·값 | [source-map.json](./source-map.json) — 노드 533개 전부(포인터·자료형·리터럴·코드포인트/바이트 구간·문맥), 키 출현 473개, 경로 패턴·선택적 키·키 순서 |
| 형태소 | [morphology.json](./morphology.json) — 텍스트 값 343개 분석(2,127 토큰), 제외 128개(사유별), 필드명 16개, 기계 표시 442건, 직접 확인 오분절 52출현 |
| 복합 표현 | [expressions.json](./expressions.json) — 후보 2,181건(직접 판정 48건 포함), 미포착 어절 목록 |
| 미결 | [issues.md](./issues.md) |
| 검증 | [validation.md](./validation.md) · [validation-machine.json](./validation-machine.json) |
| 재현 | [build.py](./build.py) · [verify.py](./verify.py) · [make-segmentation-review.py](./make-segmentation-review.py) + 수동 기록 [manual-expressions.json](./manual-expressions.json) · [segmentation-signatures.json](./segmentation-signatures.json) → [segmentation-review.json](./segmentation-review.json) · [expression-review.json](./expression-review.json) · 직접 대조 열람본 [tokens-readable.txt](./tokens-readable.txt) |

구간 기준: 모두 디코딩된 문자열의 Unicode 코드 포인트 `[start,end)`.
- source-map `span` = 파일 전체 텍스트에서 JSON 리터럴(문자열이면 따옴표 포함) 구간. `value_span` = 따옴표 안쪽. `byte_span`·`value_byte_span` = 같은 구간의 UTF-8 바이트 위치.
- morphology·expressions 의 `span` = 그 값 문자열 기준. 파일 기준으로 바꾸려면 `file_span_of_text[0] + start`.
- 이 원장은 이스케이프가 0건이라 **디코딩 문자열 = 리터럴 안쪽**이다. 노드마다 `decoded_equals_literal_interior` 로 남겼다(전부 true).

## 1. 읽기 범위 (실제로 한 일)

| 구획 | 범위 | 읽기 방식 |
|---|---|---|
| 최상위 | `/version` `/updated` `/comparisons`(배열 9) | 원본 한 줄 전체를 직접 읽음 |
| comparison[0]~[8] | `/comparisons/0` ~ `/comparisons/8` 각 id·title·subtitle·evidence_notes(있는 3개)·procedures 전 항목 | 1회차: 원본 전체를 위에서 아래로 직접 읽음(39개 시술 × 11~12필드, evidence_notes 11문장). 2회차: `tokens-readable.txt` 에서 343개 값의 원문과 Kiwi 토큰을 나란히 전부 대조하며 오분절 서명 39종을 적음. 3회차: 표현 후보에 덮이지 않은 어절 목록을 읽고 수동 표현을 보충, regex·manual 후보의 오탐·부분일치를 판정 |

- 자동 처리: 구조 열거·포인터·구간·자료형, Kiwi 형태소 분석, regex·keyword 후보 추출, 수동 목록 문자열의 전 값 부분문자열 검색, 서명의 전 값 출현 펼치기, 원문 값 표 생성.
- 직접 처리: 원문 전체 읽기, 토큰 2,127개 전체 열람(구두점·조사·어미는 위치만 확인), 오분절 39서명 확정(52출현), 수동 표현 331개 선정, 후보 48건 판정, §4 잠정 관찰과 issues.md 작성.
- 한계: 「별도 읽기 검토」는 같은 에이전트가 관점을 바꿔 다시 읽은 것이며 독립 검토자가 아니다. NNP 태그 110건(보통명사를 고유명사로 태깅한 것으로 보이는 것 다수)은 출현마다 판정하지 않았다 — `auto_flags` 에 출현별 위치만 남겼다(→ issues A2).

## 2. 컬럼 구성 표 — 원문 대응

경로 패턴의 `*` 는 배열 인덱스. 원문 예시는 패턴의 첫 출현이다.

| 원본 컬럼명 / JSON 경로 패턴 | 자료형·중첩 | 출현 수 | 원문 예시 | 예시 위치(Pointer) | 비고(구조 사실) |
|---|---|---|---|---|---|
| `(root)` | object×1 | 1 | "<object length 3>" | `(빈 문자열 = 루트)` |  |
| `/version` | string×1 | 1 | "1.3" | `/version` |  |
| `/updated` | string×1 | 1 | "2026-07-26" | `/updated` |  |
| `/comparisons` | array×1 | 1 | "<array length 9>" | `/comparisons` |  |
| `/comparisons/*` | object×9 | 9 | "<object length 5>" | `/comparisons/0` |  |
| `/comparisons/*/id` | string×9 | 9 | "lifting" | `/comparisons/0/id` |  |
| `/comparisons/*/title` | string×9 | 9 | "리프팅 비교" | `/comparisons/0/title` |  |
| `/comparisons/*/subtitle` | string×9 | 9 | "처짐/탄력 개선을 위한 시술 비교" | `/comparisons/0/subtitle` |  |
| `/comparisons/*/evidence_notes` | array×3 | 3 | "<array length 4>" | `/comparisons/0/evidence_notes` | 선택적 키: 3개 객체에만 있음, 6개에 없음 |
| `/comparisons/*/evidence_notes/*` | string×11 | 11 | "실리프팅: 즉각적 효과가 가장 뚜렷하지만 3-7일 다운타임. 실+RF/HIFU 조합 시 만족도 향상 경향이 보고되나, 근거는 후향적 관찰연구 수준(대조군 부재)" | `/comparisons/0/evidence_notes/0` |  |
| `/comparisons/*/procedures` | array×9 | 9 | "<array length 4>" | `/comparisons/0/procedures` |  |
| `/comparisons/*/procedures/*` | object×39 | 39 | "<object length 11>" | `/comparisons/0/procedures/0` |  |
| `/comparisons/*/procedures/*/name` | string×39 | 39 | "울쎄라 (HIFU)" | `/comparisons/0/procedures/0/name` |  |
| `/comparisons/*/procedures/*/category` | string×39 | 39 | "M9" | `/comparisons/0/procedures/0/category` |  |
| `/comparisons/*/procedures/*/mechanism_simple` | string×39 | 39 | "초음파로 SMAS층 열응고" | `/comparisons/0/procedures/0/mechanism_simple` |  |
| `/comparisons/*/procedures/*/pain` | string×39 | 39 | "★★★★☆" | `/comparisons/0/procedures/0/pain` |  |
| `/comparisons/*/procedures/*/downtime` | string×39 | 39 | "거의 없음" | `/comparisons/0/procedures/0/downtime` |  |
| `/comparisons/*/procedures/*/onset` | string×39 | 39 | "즉시 + 3개월 점진" | `/comparisons/0/procedures/0/onset` |  |
| `/comparisons/*/procedures/*/duration` | string×39 | 39 | "6-12개월" | `/comparisons/0/procedures/0/duration` |  |
| `/comparisons/*/procedures/*/cost_range` | string×39 | 39 | "100-400만원" | `/comparisons/0/procedures/0/cost_range` |  |
| `/comparisons/*/procedures/*/best_for` | string×39 | 39 | "중등도 처짐, 비수술 원하는 경우" | `/comparisons/0/procedures/0/best_for` |  |
| `/comparisons/*/procedures/*/limitations` | string×39 | 39 | "심한 처짐은 효과 제한" | `/comparisons/0/procedures/0/limitations` |  |
| `/comparisons/*/procedures/*/pih_risk` | string×39 | 39 | "very_low" | `/comparisons/0/procedures/0/pih_risk` |  |
| `/comparisons/*/procedures/*/asian_skin_note` | string×2 | 2 | "표피 우회 → PIH 최저. 아시아 피부 1차 선택" | `/comparisons/3/procedures/0/asian_skin_note` | 선택적 키: 2개 객체에만 있음, 37개에 없음 |

구조 사실(원문 대응):

- 최상위 키 3개, 순서 `version` → `updated` → `comparisons`. 이 원장에는 최상위 `description` 키가 없다.
- `comparisons` = 객체 9개. 키 순서는 두 가지뿐이다: `id, title, subtitle, evidence_notes, procedures`(comparison 0·2·3) / `id, title, subtitle, procedures`(1·4·5·6·7·8). **evidence_notes 는 선택적 키**이며, 없는 6개 객체에는 빈 배열이 아니라 키 자체가 없다.
- `procedures` = 비교군별 4·4·4·5·4·4·4·5·5개, 합계 39개 객체. 키 순서는 두 가지뿐이다: 11키 `name, category, mechanism_simple, pain, downtime, onset, duration, cost_range, best_for, limitations, pih_risk` / 12키(끝에 `asian_skin_note`). **asian_skin_note 는 `/comparisons/3/procedures/0`·`/1` 두 곳에만** 있다.
- 자료형: 노드 533 = object 49(루트 1 + comparison 9 + procedure 39) · array 13(comparisons 1 + evidence_notes 3 + procedures 9) · string 471. **숫자·불리언·null 없음.** 빈 문자열·빈 배열·빈 객체 없음.
- 중복 키 없음(자체 파서와 verify.py 의 `object_pairs_hook` 두 방법으로 확인).

## 3. 항목별 값 — 원문 대응 (원본 컬럼명 그대로, 배열은 원본 순서)

표 칸의 `|` 는 Markdown 때문에 `\|` 로 적었다. 그 외에는 원문 문자 그대로다.

### 3.0 최상위 `(root)`

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| version | 1.3 | `/version` |
| updated | 2026-07-26 | `/updated` |
| comparisons | <array length 9> | `/comparisons` |

### 3.1 `/comparisons/0` — id `lifting`

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| id | lifting | `/comparisons/0/id` |
| title | 리프팅 비교 | `/comparisons/0/title` |
| subtitle | 처짐/탄력 개선을 위한 시술 비교 | `/comparisons/0/subtitle` |
| evidence_notes | <array length 4> | `/comparisons/0/evidence_notes` |
| procedures | <array length 4> | `/comparisons/0/procedures` |

**evidence_notes** (`/comparisons/0/evidence_notes`, 원본 순서)

| # | 원문 값 | Pointer |
|---|---|---|
| 0 | 실리프팅: 즉각적 효과가 가장 뚜렷하지만 3-7일 다운타임. 실+RF/HIFU 조합 시 만족도 향상 경향이 보고되나, 근거는 후향적 관찰연구 수준(대조군 부재) | `/comparisons/0/evidence_notes/0` |
| 1 | HIFU: 깊은 리프팅(SMAS층 도달), 2-3개월 점진적 효과. 심한 처짐은 효과 제한적 | `/comparisons/0/evidence_notes/1` |
| 2 | RF: 안전성 가장 높지만 리프팅 효과 가장 약함. 피부결+타이트닝에 더 적합 | `/comparisons/0/evidence_notes/2` |
| 3 | 조합 고려: 실리프팅(즉각적 물리적 리프팅)과 HIFU/RF(콜라겐 리모델링·장기 유지)는 상보적 기전으로 효과 지속이 기대되나, 현재 근거는 후향적 연구(근거수준 III) 위주로 RCT는 부족 | `/comparisons/0/evidence_notes/3` |

**procedures/0** (`/comparisons/0/procedures/0`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 울쎄라 (HIFU) | `/comparisons/0/procedures/0/name` |
| category | M9 | `/comparisons/0/procedures/0/category` |
| mechanism_simple | 초음파로 SMAS층 열응고 | `/comparisons/0/procedures/0/mechanism_simple` |
| pain | ★★★★☆ | `/comparisons/0/procedures/0/pain` |
| downtime | 거의 없음 | `/comparisons/0/procedures/0/downtime` |
| onset | 즉시 + 3개월 점진 | `/comparisons/0/procedures/0/onset` |
| duration | 6-12개월 | `/comparisons/0/procedures/0/duration` |
| cost_range | 100-400만원 | `/comparisons/0/procedures/0/cost_range` |
| best_for | 중등도 처짐, 비수술 원하는 경우 | `/comparisons/0/procedures/0/best_for` |
| limitations | 심한 처짐은 효과 제한 | `/comparisons/0/procedures/0/limitations` |
| pih_risk | very_low | `/comparisons/0/procedures/0/pih_risk` |

**procedures/1** (`/comparisons/0/procedures/1`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 써마지FLX (RF) | `/comparisons/0/procedures/1/name` |
| category | M9 | `/comparisons/0/procedures/1/category` |
| mechanism_simple | 고주파로 콜라겐 수축+재생 | `/comparisons/0/procedures/1/mechanism_simple` |
| pain | ★★★☆☆ | `/comparisons/0/procedures/1/pain` |
| downtime | 거의 없음 | `/comparisons/0/procedures/1/downtime` |
| onset | 즉시 + 2-3개월 | `/comparisons/0/procedures/1/onset` |
| duration | 6-12개월 | `/comparisons/0/procedures/1/duration` |
| cost_range | 80-400만원 | `/comparisons/0/procedures/1/cost_range` |
| best_for | 피부 탄력, 타이트닝 | `/comparisons/0/procedures/1/best_for` |
| limitations | 지방위축 위험 (반복 시) | `/comparisons/0/procedures/1/limitations` |
| pih_risk | very_low | `/comparisons/0/procedures/1/pih_risk` |

**procedures/2** (`/comparisons/0/procedures/2`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 실리프팅 (PDO코그) | `/comparisons/0/procedures/2/name` |
| category | M7 | `/comparisons/0/procedures/2/category` |
| mechanism_simple | 실로 물리적 당김 + 콜라겐 유도 | `/comparisons/0/procedures/2/mechanism_simple` |
| pain | ★★★☆☆ | `/comparisons/0/procedures/2/pain` |
| downtime | 3-7일 부종/멍 | `/comparisons/0/procedures/2/downtime` |
| onset | 즉시 | `/comparisons/0/procedures/2/onset` |
| duration | 12-18개월 | `/comparisons/0/procedures/2/duration` |
| cost_range | 50-200만원 | `/comparisons/0/procedures/2/cost_range` |
| best_for | 즉각적 리프팅 효과 | `/comparisons/0/procedures/2/best_for` |
| limitations | 실 이탈, 비대칭 가능 | `/comparisons/0/procedures/2/limitations` |
| pih_risk | none | `/comparisons/0/procedures/2/pih_risk` |

**procedures/3** (`/comparisons/0/procedures/3`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 인모드FX (RF마이크로니들) | `/comparisons/0/procedures/3/name` |
| category | M11 | `/comparisons/0/procedures/3/category` |
| mechanism_simple | RF 니들로 진피 수축 + 재생 | `/comparisons/0/procedures/3/mechanism_simple` |
| pain | ★★★☆☆ | `/comparisons/0/procedures/3/pain` |
| downtime | 2-3일 붉은기 | `/comparisons/0/procedures/3/downtime` |
| onset | 2-4주 | `/comparisons/0/procedures/3/onset` |
| duration | 6-12개월 | `/comparisons/0/procedures/3/duration` |
| cost_range | 30-80만원 | `/comparisons/0/procedures/3/cost_range` |
| best_for | 초기 탄력 저하, 모공 | `/comparisons/0/procedures/3/best_for` |
| limitations | 강력한 리프팅은 어려움 | `/comparisons/0/procedures/3/limitations` |
| pih_risk | low | `/comparisons/0/procedures/3/pih_risk` |

### 3.2 `/comparisons/1` — id `wrinkle`

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| id | wrinkle | `/comparisons/1/id` |
| title | 주름 개선 비교 | `/comparisons/1/title` |
| subtitle | 이마/미간/눈가 주름 치료 비교 | `/comparisons/1/subtitle` |
| procedures | <array length 4> | `/comparisons/1/procedures` |

**evidence_notes** — 이 비교군 객체에는 키 자체가 없다(빈 배열 아님).


**procedures/0** (`/comparisons/1/procedures/0`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 보톡스 (보툴리눔톡신) | `/comparisons/1/procedures/0/name` |
| category | M1 | `/comparisons/1/procedures/0/category` |
| mechanism_simple | 근육 수축 차단으로 표정주름 완화 | `/comparisons/1/procedures/0/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/1/procedures/0/pain` |
| downtime | 없음 | `/comparisons/1/procedures/0/downtime` |
| onset | 3-7일 | `/comparisons/1/procedures/0/onset` |
| duration | 3-6개월 | `/comparisons/1/procedures/0/duration` |
| cost_range | 5-30만원 | `/comparisons/1/procedures/0/cost_range` |
| best_for | 표정주름 (이마, 미간, 눈가) | `/comparisons/1/procedures/0/best_for` |
| limitations | 정적 주름에는 효과 제한 | `/comparisons/1/procedures/0/limitations` |
| pih_risk | none | `/comparisons/1/procedures/0/pih_risk` |

**procedures/1** (`/comparisons/1/procedures/1`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 히알루론산 필러 | `/comparisons/1/procedures/1/name` |
| category | M2 | `/comparisons/1/procedures/1/category` |
| mechanism_simple | 필러로 주름 골 채움 | `/comparisons/1/procedures/1/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/1/procedures/1/pain` |
| downtime | 1-2일 부종 | `/comparisons/1/procedures/1/downtime` |
| onset | 즉시 | `/comparisons/1/procedures/1/onset` |
| duration | 6-18개월 | `/comparisons/1/procedures/1/duration` |
| cost_range | 20-80만원 | `/comparisons/1/procedures/1/cost_range` |
| best_for | 팔자, 마리오넷, 정적 주름 | `/comparisons/1/procedures/1/best_for` |
| limitations | 필러 이동, 뭉침 가능. 드물지만 혈관 폐색 시 피부괴사·실명 위험(응급 히알루로니다제 처치 필요) | `/comparisons/1/procedures/1/limitations` |
| pih_risk | none | `/comparisons/1/procedures/1/pih_risk` |

**procedures/2** (`/comparisons/1/procedures/2`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 프락셀 (프랙셔널 레이저) | `/comparisons/1/procedures/2/name` |
| category | M8 | `/comparisons/1/procedures/2/category` |
| mechanism_simple | 미세 열 기둥으로 콜라겐 리모델링 | `/comparisons/1/procedures/2/mechanism_simple` |
| pain | ★★★☆☆ | `/comparisons/1/procedures/2/pain` |
| downtime | 3-5일 각질/붉은기 | `/comparisons/1/procedures/2/downtime` |
| onset | 2-4주 | `/comparisons/1/procedures/2/onset` |
| duration | 12-24개월 | `/comparisons/1/procedures/2/duration` |
| cost_range | 20-50만원 | `/comparisons/1/procedures/2/cost_range` |
| best_for | 잔주름, 피부 텍스처 | `/comparisons/1/procedures/2/best_for` |
| limitations | 깊은 주름은 여러 회 필요 | `/comparisons/1/procedures/2/limitations` |
| pih_risk | moderate | `/comparisons/1/procedures/2/pih_risk` |

**procedures/3** (`/comparisons/1/procedures/3`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 리쥬란 (PN주사) | `/comparisons/1/procedures/3/name` |
| category | M4 | `/comparisons/1/procedures/3/category` |
| mechanism_simple | 폴리뉴클레오타이드로 진피 재생 | `/comparisons/1/procedures/3/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/1/procedures/3/pain` |
| downtime | 1-2일 잔뾰루지 | `/comparisons/1/procedures/3/downtime` |
| onset | 2-4주 | `/comparisons/1/procedures/3/onset` |
| duration | 6-12개월 | `/comparisons/1/procedures/3/duration` |
| cost_range | 15-40만원 | `/comparisons/1/procedures/3/cost_range` |
| best_for | 눈밑 잔주름, 피부 탄력 | `/comparisons/1/procedures/3/best_for` |
| limitations | 깊은 주름에는 단독 효과 부족 | `/comparisons/1/procedures/3/limitations` |
| pih_risk | none | `/comparisons/1/procedures/3/pih_risk` |

### 3.3 `/comparisons/2` — id `volume`

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| id | volume | `/comparisons/2/id` |
| title | 볼륨 회복 비교 | `/comparisons/2/title` |
| subtitle | 볼/관자/이마 볼륨 충전 비교 | `/comparisons/2/subtitle` |
| evidence_notes | <array length 3> | `/comparisons/2/evidence_notes` |
| procedures | <array length 4> | `/comparisons/2/procedures` |

**evidence_notes** (`/comparisons/2/evidence_notes`, 원본 순서)

| # | 원문 값 | Pointer |
|---|---|---|
| 0 | 바이오스티뮬레이터: 18-24개월+ 지속, 연간 비용 최저, 자연스러운 결과. 즉각 효과는 없지만 장기적으로 가장 경제적 | `/comparisons/2/evidence_notes/0` |
| 1 | HA 필러: 즉각적이지만 6-18개월 지속, 유지비용 높음. 가역적(히알루로니다아제로 용해 가능)이 최대 장점 | `/comparisons/2/evidence_notes/1` |
| 2 | 지방이식: 생착 부분 영구적이나 흡수율 변동(30-70%), 수술적 위험(마취, 감염, 지방색전증). 대량 볼륨 복원에 유리 | `/comparisons/2/evidence_notes/2` |

**procedures/0** (`/comparisons/2/procedures/0`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 히알루론산 필러 | `/comparisons/2/procedures/0/name` |
| category | M2 | `/comparisons/2/procedures/0/category` |
| mechanism_simple | HA 겔로 즉각 볼륨 충전 | `/comparisons/2/procedures/0/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/2/procedures/0/pain` |
| downtime | 1-3일 부종 | `/comparisons/2/procedures/0/downtime` |
| onset | 즉시 | `/comparisons/2/procedures/0/onset` |
| duration | 6-18개월 | `/comparisons/2/procedures/0/duration` |
| cost_range | 30-100만원 | `/comparisons/2/procedures/0/cost_range` |
| best_for | 즉각적 볼륨, 정밀 조각 | `/comparisons/2/procedures/0/best_for` |
| limitations | 반복 시술 필요, 필러 이동. 드물지만 혈관 폐색 시 피부괴사·실명 위험(응급 히알루로니다제 처치 필요) | `/comparisons/2/procedures/0/limitations` |
| pih_risk | none | `/comparisons/2/procedures/0/pih_risk` |

**procedures/1** (`/comparisons/2/procedures/1`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 스컬트라 (PLLA) | `/comparisons/2/procedures/1/name` |
| category | M3 | `/comparisons/2/procedures/1/category` |
| mechanism_simple | PLLA로 자가 콜라겐 생성 유도 | `/comparisons/2/procedures/1/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/2/procedures/1/pain` |
| downtime | 1-2일 부종 | `/comparisons/2/procedures/1/downtime` |
| onset | 1-3개월 점진 | `/comparisons/2/procedures/1/onset` |
| duration | 18-24개월 | `/comparisons/2/procedures/1/duration` |
| cost_range | 30-80만원/바이알 | `/comparisons/2/procedures/1/cost_range` |
| best_for | 전체적 볼륨 회복, 자연스러움 | `/comparisons/2/procedures/1/best_for` |
| limitations | 즉각 효과 없음, 결절 가능 | `/comparisons/2/procedures/1/limitations` |
| pih_risk | none | `/comparisons/2/procedures/1/pih_risk` |

**procedures/2** (`/comparisons/2/procedures/2`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 엘란쎄 (PCL) | `/comparisons/2/procedures/2/name` |
| category | M3 | `/comparisons/2/procedures/2/category` |
| mechanism_simple | PCL 마이크로스피어 + CMC 겔 | `/comparisons/2/procedures/2/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/2/procedures/2/pain` |
| downtime | 1-3일 부종 | `/comparisons/2/procedures/2/downtime` |
| onset | 즉시 + 점진적 | `/comparisons/2/procedures/2/onset` |
| duration | 12-48개월 (타입별) | `/comparisons/2/procedures/2/duration` |
| cost_range | 30-70만원/시린지 | `/comparisons/2/procedures/2/cost_range` |
| best_for | 즉각+장기 볼륨, 콜라겐 유도 | `/comparisons/2/procedures/2/best_for` |
| limitations | 녹지 않아 교정 어려움 | `/comparisons/2/procedures/2/limitations` |
| pih_risk | none | `/comparisons/2/procedures/2/pih_risk` |

**procedures/3** (`/comparisons/2/procedures/3`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 자가지방이식 | `/comparisons/2/procedures/3/name` |
| category | M6 | `/comparisons/2/procedures/3/category` |
| mechanism_simple | 본인 지방 채취 후 이식 | `/comparisons/2/procedures/3/mechanism_simple` |
| pain | ★★★☆☆ | `/comparisons/2/procedures/3/pain` |
| downtime | 7-14일 부종/멍 | `/comparisons/2/procedures/3/downtime` |
| onset | 2-3개월 (생착 후) | `/comparisons/2/procedures/3/onset` |
| duration | 반영구 (생착분) | `/comparisons/2/procedures/3/duration` |
| cost_range | 100-400만원 | `/comparisons/2/procedures/3/cost_range` |
| best_for | 대량 볼륨, 자연스러움, 반영구 | `/comparisons/2/procedures/3/best_for` |
| limitations | 생착률 변동 (30-70%), 채취부 통증 | `/comparisons/2/procedures/3/limitations` |
| pih_risk | none | `/comparisons/2/procedures/3/pih_risk` |

### 3.4 `/comparisons/3` — id `skin_texture`

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| id | skin_texture | `/comparisons/3/id` |
| title | 피부결 개선 비교 | `/comparisons/3/title` |
| subtitle | 모공/흉터/피부톤 개선 비교 (Asian skin 특화) | `/comparisons/3/subtitle` |
| evidence_notes | <array length 4> | `/comparisons/3/evidence_notes` |
| procedures | <array length 5> | `/comparisons/3/procedures` |

**evidence_notes** (`/comparisons/3/evidence_notes`, 원본 순서)

| # | 원문 값 | Pointer |
|---|---|---|
| 0 | 니들RF: 아시아 피부(Fitz III-V)에서 PIH 발생률 가장 낮음 — 표피를 우회하여 진피에 직접 RF 전달. 다운타임 1-3일 | `/comparisons/3/evidence_notes/0` |
| 1 | CO2 프랙셔널: 깊은 흉터(아이스픽, 박스카)에 최강 효과지만 PIH 위험 높음 (RR 4.44). 아시아 피부에서 특히 주의. 5-7일 다운타임 | `/comparisons/3/evidence_notes/1` |
| 2 | 케미컬 필: 표면 효과 위주, 반복 필요. 깊은 필링(TCA 50%+)은 아시아 피부에서 PIH 위험 현저히 높음 | `/comparisons/3/evidence_notes/2` |
| 3 | 아시아 피부 원칙: 표피 열 손상 최소화가 핵심 — 니들RF > 피코 프랙셔널 > CO2 프랙셔널 순 안전 | `/comparisons/3/evidence_notes/3` |

**procedures/0** (`/comparisons/3/procedures/0`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 마이크로니들RF (시크릿/인모드) | `/comparisons/3/procedures/0/name` |
| category | M11 | `/comparisons/3/procedures/0/category` |
| mechanism_simple | RF 니들로 진피 콜라겐 리모델링 | `/comparisons/3/procedures/0/mechanism_simple` |
| pain | ★★★☆☆ | `/comparisons/3/procedures/0/pain` |
| downtime | 1-3일 붉은기 | `/comparisons/3/procedures/0/downtime` |
| onset | 2-4주 | `/comparisons/3/procedures/0/onset` |
| duration | 12-18개월 | `/comparisons/3/procedures/0/duration` |
| cost_range | 20-60만원 | `/comparisons/3/procedures/0/cost_range` |
| best_for | 모공, 여드름 흉터, 탄력 | `/comparisons/3/procedures/0/best_for` |
| limitations | 깊은 박스카 흉터는 제한적 | `/comparisons/3/procedures/0/limitations` |
| pih_risk | low | `/comparisons/3/procedures/0/pih_risk` |
| asian_skin_note | 표피 우회 → PIH 최저. 아시아 피부 1차 선택 | `/comparisons/3/procedures/0/asian_skin_note` |

**procedures/1** (`/comparisons/3/procedures/1`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | CO2 프랙셔널 레이저 | `/comparisons/3/procedures/1/name` |
| category | M8 | `/comparisons/3/procedures/1/category` |
| mechanism_simple | CO2로 미세 열기둥 + 피부 재생 | `/comparisons/3/procedures/1/mechanism_simple` |
| pain | ★★★★☆ | `/comparisons/3/procedures/1/pain` |
| downtime | 5-7일 각질/붉은기 | `/comparisons/3/procedures/1/downtime` |
| onset | 2-4주 | `/comparisons/3/procedures/1/onset` |
| duration | 12-24개월 | `/comparisons/3/procedures/1/duration` |
| cost_range | 20-50만원 | `/comparisons/3/procedures/1/cost_range` |
| best_for | 깊은 흉터, 모공, 피부 재생 | `/comparisons/3/procedures/1/best_for` |
| limitations | PIH 위험 높음 (RR 4.44), 긴 다운타임 | `/comparisons/3/procedures/1/limitations` |
| pih_risk | high | `/comparisons/3/procedures/1/pih_risk` |
| asian_skin_note | 아시아 피부 PIH 위험 가장 높음. 저밀도/저에너지 세팅 + 사전 미백 권장 | `/comparisons/3/procedures/1/asian_skin_note` |

**procedures/2** (`/comparisons/3/procedures/2`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | MTS (더마펜/더마스탬프) | `/comparisons/3/procedures/2/name` |
| category | M12 | `/comparisons/3/procedures/2/category` |
| mechanism_simple | 미세침으로 콜라겐 유도 요법 | `/comparisons/3/procedures/2/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/3/procedures/2/pain` |
| downtime | 1-2일 붉은기 | `/comparisons/3/procedures/2/downtime` |
| onset | 2-4주 | `/comparisons/3/procedures/2/onset` |
| duration | 6-12개월 | `/comparisons/3/procedures/2/duration` |
| cost_range | 5-20만원 | `/comparisons/3/procedures/2/cost_range` |
| best_for | 피부결, 모공, 약물 침투 | `/comparisons/3/procedures/2/best_for` |
| limitations | 깊은 흉터에는 효과 제한 | `/comparisons/3/procedures/2/limitations` |
| pih_risk | low | `/comparisons/3/procedures/2/pih_risk` |

**procedures/3** (`/comparisons/3/procedures/3`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 피코 프랙셔널 | `/comparisons/3/procedures/3/name` |
| category | M8 | `/comparisons/3/procedures/3/category` |
| mechanism_simple | 피코초 레이저로 LIOB 생성 → 콜라겐 유도 | `/comparisons/3/procedures/3/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/3/procedures/3/pain` |
| downtime | 1-2일 경미 붉은기 | `/comparisons/3/procedures/3/downtime` |
| onset | 2-4주 | `/comparisons/3/procedures/3/onset` |
| duration | 6-12개월 | `/comparisons/3/procedures/3/duration` |
| cost_range | 10-30만원 | `/comparisons/3/procedures/3/cost_range` |
| best_for | 모공, 피부톤, 가벼운 흉터 | `/comparisons/3/procedures/3/best_for` |
| limitations | 깊은 흉터는 여러 회 필요 | `/comparisons/3/procedures/3/limitations` |
| pih_risk | low | `/comparisons/3/procedures/3/pih_risk` |

**procedures/4** (`/comparisons/3/procedures/4`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 실리콘피부관리 (아쿠아필/하이드라) | `/comparisons/3/procedures/4/name` |
| category | M15 | `/comparisons/3/procedures/4/category` |
| mechanism_simple | 흡입+필링으로 모공 세정 + 보습 | `/comparisons/3/procedures/4/mechanism_simple` |
| pain | ★☆☆☆☆ | `/comparisons/3/procedures/4/pain` |
| downtime | 없음 | `/comparisons/3/procedures/4/downtime` |
| onset | 즉시 | `/comparisons/3/procedures/4/onset` |
| duration | 2-4주 | `/comparisons/3/procedures/4/duration` |
| cost_range | 5-15만원 | `/comparisons/3/procedures/4/cost_range` |
| best_for | 모공 관리, 피지 제거, 유지관리 | `/comparisons/3/procedures/4/best_for` |
| limitations | 구조적 개선은 안 됨 | `/comparisons/3/procedures/4/limitations` |
| pih_risk | very_low | `/comparisons/3/procedures/4/pih_risk` |

### 3.5 `/comparisons/4` — id `pigment`

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| id | pigment | `/comparisons/4/id` |
| title | 색소 치료 비교 | `/comparisons/4/title` |
| subtitle | 기미/주근깨/잡티 치료 비교 | `/comparisons/4/subtitle` |
| procedures | <array length 4> | `/comparisons/4/procedures` |

**evidence_notes** — 이 비교군 객체에는 키 자체가 없다(빈 배열 아님).


**procedures/0** (`/comparisons/4/procedures/0`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 피코토닝 | `/comparisons/4/procedures/0/name` |
| category | M8 | `/comparisons/4/procedures/0/category` |
| mechanism_simple | 피코초 레이저로 색소 미세 파괴 | `/comparisons/4/procedures/0/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/4/procedures/0/pain` |
| downtime | 거의 없음 | `/comparisons/4/procedures/0/downtime` |
| onset | 3-5회 후 점진 | `/comparisons/4/procedures/0/onset` |
| duration | 6-12개월 | `/comparisons/4/procedures/0/duration` |
| cost_range | 5-15만원/회 | `/comparisons/4/procedures/0/cost_range` |
| best_for | 기미, 칙칙한 피부톤 | `/comparisons/4/procedures/0/best_for` |
| limitations | 다회 치료 필요, 재발 가능 | `/comparisons/4/procedures/0/limitations` |
| pih_risk | low | `/comparisons/4/procedures/0/pih_risk` |

**procedures/1** (`/comparisons/4/procedures/1`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | Q-스위치 Nd:YAG | `/comparisons/4/procedures/1/name` |
| category | M8 | `/comparisons/4/procedures/1/category` |
| mechanism_simple | 나노초 레이저로 색소 선택적 파괴 | `/comparisons/4/procedures/1/mechanism_simple` |
| pain | ★★★☆☆ | `/comparisons/4/procedures/1/pain` |
| downtime | 3-7일 딱지 | `/comparisons/4/procedures/1/downtime` |
| onset | 1-2주 | `/comparisons/4/procedures/1/onset` |
| duration | 장기 지속되나 재발 가능(특히 주근깨는 자외선·유전 영향으로 재발률 높음). 일광흑자는 상대적으로 지속적이며 유지에는 평생 자외선 차단 필수 | `/comparisons/4/procedures/1/duration` |
| cost_range | 5-20만원/회 | `/comparisons/4/procedures/1/cost_range` |
| best_for | 주근깨, 잡티, 오타모반 | `/comparisons/4/procedures/1/best_for` |
| limitations | 기미에는 효과 제한, PIH 위험 | `/comparisons/4/procedures/1/limitations` |
| pih_risk | moderate | `/comparisons/4/procedures/1/pih_risk` |

**procedures/2** (`/comparisons/4/procedures/2`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | IPL (광선치료) | `/comparisons/4/procedures/2/name` |
| category | M9 | `/comparisons/4/procedures/2/category` |
| mechanism_simple | 광대역 빛으로 멜라닌 + 혈관 타겟 | `/comparisons/4/procedures/2/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/4/procedures/2/pain` |
| downtime | 1-3일 미세 딱지 | `/comparisons/4/procedures/2/downtime` |
| onset | 1-2주 | `/comparisons/4/procedures/2/onset` |
| duration | 6-12개월 | `/comparisons/4/procedures/2/duration` |
| cost_range | 10-30만원 | `/comparisons/4/procedures/2/cost_range` |
| best_for | 잡티, 홍조, 피부톤 균일화 | `/comparisons/4/procedures/2/best_for` |
| limitations | 깊은 색소는 어려움 | `/comparisons/4/procedures/2/limitations` |
| pih_risk | low | `/comparisons/4/procedures/2/pih_risk` |

**procedures/3** (`/comparisons/4/procedures/3`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 레이저토닝 (저출력 Nd:YAG) | `/comparisons/4/procedures/3/name` |
| category | M8 | `/comparisons/4/procedures/3/category` |
| mechanism_simple | 저에너지 반복 조사로 기미 멜라닌 분해 | `/comparisons/4/procedures/3/mechanism_simple` |
| pain | ★☆☆☆☆ | `/comparisons/4/procedures/3/pain` |
| downtime | 거의 없음 | `/comparisons/4/procedures/3/downtime` |
| onset | 5-10회 후 점진 | `/comparisons/4/procedures/3/onset` |
| duration | 유지치료 필요 | `/comparisons/4/procedures/3/duration` |
| cost_range | 3-10만원/회 | `/comparisons/4/procedures/3/cost_range` |
| best_for | 기미 유지관리, 피부톤 | `/comparisons/4/procedures/3/best_for` |
| limitations | 탈색 위험 (과다 시), 단독 효과 느림 | `/comparisons/4/procedures/3/limitations` |
| pih_risk | low | `/comparisons/4/procedures/3/pih_risk` |

### 3.6 `/comparisons/5` — id `hair_removal`

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| id | hair_removal | `/comparisons/5/id` |
| title | 제모 비교 | `/comparisons/5/title` |
| subtitle | 레이저 제모 장비 비교 | `/comparisons/5/subtitle` |
| procedures | <array length 4> | `/comparisons/5/procedures` |

**evidence_notes** — 이 비교군 객체에는 키 자체가 없다(빈 배열 아님).


**procedures/0** (`/comparisons/5/procedures/0`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 알렉산드라이트 (755nm) | `/comparisons/5/procedures/0/name` |
| category | M8 | `/comparisons/5/procedures/0/category` |
| mechanism_simple | 755nm 멜라닌 선택적 흡수 → 모낭 파괴 | `/comparisons/5/procedures/0/mechanism_simple` |
| pain | ★★★☆☆ | `/comparisons/5/procedures/0/pain` |
| downtime | 1-2일 붉은기 | `/comparisons/5/procedures/0/downtime` |
| onset | 3-5회 (2-4주 간격) | `/comparisons/5/procedures/0/onset` |
| duration | 영구 감모 (80-90%) | `/comparisons/5/procedures/0/duration` |
| cost_range | 5-30만원/부위 | `/comparisons/5/procedures/0/cost_range` |
| best_for | 밝은 피부 + 굵은 모발 | `/comparisons/5/procedures/0/best_for` |
| limitations | 어두운 피부 화상 위험 | `/comparisons/5/procedures/0/limitations` |
| pih_risk | moderate | `/comparisons/5/procedures/0/pih_risk` |

**procedures/1** (`/comparisons/5/procedures/1`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 다이오드 (808nm/810nm) | `/comparisons/5/procedures/1/name` |
| category | M8 | `/comparisons/5/procedures/1/category` |
| mechanism_simple | 808nm 멜라닌 흡수 + 깊은 침투 | `/comparisons/5/procedures/1/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/5/procedures/1/pain` |
| downtime | 거의 없음 | `/comparisons/5/procedures/1/downtime` |
| onset | 4-6회 (4-6주 간격) | `/comparisons/5/procedures/1/onset` |
| duration | 영구 감모 (80-90%) | `/comparisons/5/procedures/1/duration` |
| cost_range | 3-20만원/부위 | `/comparisons/5/procedures/1/cost_range` |
| best_for | 다양한 피부톤, 대면적 | `/comparisons/5/procedures/1/best_for` |
| limitations | 밝은 모발 효과 제한 | `/comparisons/5/procedures/1/limitations` |
| pih_risk | low | `/comparisons/5/procedures/1/pih_risk` |

**procedures/2** (`/comparisons/5/procedures/2`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | Nd:YAG (1064nm) | `/comparisons/5/procedures/2/name` |
| category | M8 | `/comparisons/5/procedures/2/category` |
| mechanism_simple | 1064nm 깊은 침투 + 낮은 멜라닌 의존 | `/comparisons/5/procedures/2/mechanism_simple` |
| pain | ★★★☆☆ | `/comparisons/5/procedures/2/pain` |
| downtime | 거의 없음 | `/comparisons/5/procedures/2/downtime` |
| onset | 5-8회 (4-6주 간격) | `/comparisons/5/procedures/2/onset` |
| duration | 영구 감모 (70-85%) | `/comparisons/5/procedures/2/duration` |
| cost_range | 5-25만원/부위 | `/comparisons/5/procedures/2/cost_range` |
| best_for | 어두운 피부 (Fitz IV-VI) | `/comparisons/5/procedures/2/best_for` |
| limitations | 밝은 모발은 효과 낮음, 더 많은 회차 | `/comparisons/5/procedures/2/limitations` |
| pih_risk | low | `/comparisons/5/procedures/2/pih_risk` |

**procedures/3** (`/comparisons/5/procedures/3`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | IPL 제모 | `/comparisons/5/procedures/3/name` |
| category | M9 | `/comparisons/5/procedures/3/category` |
| mechanism_simple | 광대역 빛으로 멜라닌 타겟 → 모낭 약화 | `/comparisons/5/procedures/3/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/5/procedures/3/pain` |
| downtime | 거의 없음 | `/comparisons/5/procedures/3/downtime` |
| onset | 6-10회 (3-4주 간격) | `/comparisons/5/procedures/3/onset` |
| duration | 반영구 (60-80%) | `/comparisons/5/procedures/3/duration` |
| cost_range | 3-15만원/부위 | `/comparisons/5/procedures/3/cost_range` |
| best_for | 넓은 부위, 경제적 | `/comparisons/5/procedures/3/best_for` |
| limitations | 레이저 대비 효과 약함, 어두운 피부 주의 | `/comparisons/5/procedures/3/limitations` |
| pih_risk | low | `/comparisons/5/procedures/3/pih_risk` |

### 3.7 `/comparisons/6` — id `body_contouring`

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| id | body_contouring | `/comparisons/6/id` |
| title | 바디 컨투어링 비교 | `/comparisons/6/title` |
| subtitle | 비수술 체형 관리 비교 | `/comparisons/6/subtitle` |
| procedures | <array length 4> | `/comparisons/6/procedures` |

**evidence_notes** — 이 비교군 객체에는 키 자체가 없다(빈 배열 아님).


**procedures/0** (`/comparisons/6/procedures/0`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 쿨스컬프팅 (냉동지방분해) | `/comparisons/6/procedures/0/name` |
| category | M14 | `/comparisons/6/procedures/0/category` |
| mechanism_simple | 냉각으로 지방세포 선택적 사멸 | `/comparisons/6/procedures/0/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/6/procedures/0/pain` |
| downtime | 거의 없음 (멍 가능) | `/comparisons/6/procedures/0/downtime` |
| onset | 2-3개월 | `/comparisons/6/procedures/0/onset` |
| duration | 영구 (사멸 지방) | `/comparisons/6/procedures/0/duration` |
| cost_range | 30-80만원/부위 | `/comparisons/6/procedures/0/cost_range` |
| best_for | 국소 지방 (복부, 러브핸들) | `/comparisons/6/procedures/0/best_for` |
| limitations | 체중 감량은 아님, PAH 위험 | `/comparisons/6/procedures/0/limitations` |
| pih_risk | none | `/comparisons/6/procedures/0/pih_risk` |

**procedures/1** (`/comparisons/6/procedures/1`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 리포셀 (HIFU 지방) | `/comparisons/6/procedures/1/name` |
| category | M10 | `/comparisons/6/procedures/1/category` |
| mechanism_simple | 고강도 초음파로 지방세포 파괴 | `/comparisons/6/procedures/1/mechanism_simple` |
| pain | ★★★☆☆ | `/comparisons/6/procedures/1/pain` |
| downtime | 1-3일 부종/멍 | `/comparisons/6/procedures/1/downtime` |
| onset | 4-12주 | `/comparisons/6/procedures/1/onset` |
| duration | 영구 (사멸 지방) | `/comparisons/6/procedures/1/duration` |
| cost_range | 50-150만원/부위 | `/comparisons/6/procedures/1/cost_range` |
| best_for | 복부, 팔뚝, 허벅지 | `/comparisons/6/procedures/1/best_for` |
| limitations | 시술 시간 길고 통증 있음 | `/comparisons/6/procedures/1/limitations` |
| pih_risk | none | `/comparisons/6/procedures/1/pih_risk` |

**procedures/2** (`/comparisons/6/procedures/2`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 스컬프슈어 (레이저 지방분해) | `/comparisons/6/procedures/2/name` |
| category | M8 | `/comparisons/6/procedures/2/category` |
| mechanism_simple | 1060nm 레이저로 지방세포 열파괴 | `/comparisons/6/procedures/2/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/6/procedures/2/pain` |
| downtime | 거의 없음 | `/comparisons/6/procedures/2/downtime` |
| onset | 6-12주 | `/comparisons/6/procedures/2/onset` |
| duration | 영구 (사멸 지방) | `/comparisons/6/procedures/2/duration` |
| cost_range | 30-70만원/부위 | `/comparisons/6/procedures/2/cost_range` |
| best_for | 복부, 옆구리 소량 지방 | `/comparisons/6/procedures/2/best_for` |
| limitations | 대량 지방에는 효과 제한 | `/comparisons/6/procedures/2/limitations` |
| pih_risk | very_low | `/comparisons/6/procedures/2/pih_risk` |

**procedures/3** (`/comparisons/6/procedures/3`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 바넬라 (고주파 바디) | `/comparisons/6/procedures/3/name` |
| category | M9 | `/comparisons/6/procedures/3/category` |
| mechanism_simple | RF로 지방 감소 + 피부 타이트닝 | `/comparisons/6/procedures/3/mechanism_simple` |
| pain | ★☆☆☆☆ | `/comparisons/6/procedures/3/pain` |
| downtime | 없음 | `/comparisons/6/procedures/3/downtime` |
| onset | 4-6회 후 점진 | `/comparisons/6/procedures/3/onset` |
| duration | 6-12개월 | `/comparisons/6/procedures/3/duration` |
| cost_range | 10-30만원/회 | `/comparisons/6/procedures/3/cost_range` |
| best_for | 셀룰라이트, 피부 탄력 | `/comparisons/6/procedures/3/best_for` |
| limitations | 지방 감소 효과는 약한 편 | `/comparisons/6/procedures/3/limitations` |
| pih_risk | none | `/comparisons/6/procedures/3/pih_risk` |

### 3.8 `/comparisons/7` — id `acne`

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| id | acne | `/comparisons/7/id` |
| title | 여드름 치료 비교 | `/comparisons/7/title` |
| subtitle | 여드름 치료 시술 비교 | `/comparisons/7/subtitle` |
| procedures | <array length 5> | `/comparisons/7/procedures` |

**evidence_notes** — 이 비교군 객체에는 키 자체가 없다(빈 배열 아님).


**procedures/0** (`/comparisons/7/procedures/0`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 아그네스 (RF 니들 피지선) | `/comparisons/7/procedures/0/name` |
| category | M11 | `/comparisons/7/procedures/0/category` |
| mechanism_simple | RF 니들로 피지선 선택적 파괴 | `/comparisons/7/procedures/0/mechanism_simple` |
| pain | ★★★☆☆ | `/comparisons/7/procedures/0/pain` |
| downtime | 3-5일 부종/붉은기 | `/comparisons/7/procedures/0/downtime` |
| onset | 1-3회 후 | `/comparisons/7/procedures/0/onset` |
| duration | 영구 (파괴된 피지선) | `/comparisons/7/procedures/0/duration` |
| cost_range | 20-50만원/회 | `/comparisons/7/procedures/0/cost_range` |
| best_for | 재발성 여드름, 피지선 과다 | `/comparisons/7/procedures/0/best_for` |
| limitations | 전체 얼굴 시 시간/비용 높음 | `/comparisons/7/procedures/0/limitations` |
| pih_risk | low | `/comparisons/7/procedures/0/pih_risk` |

**procedures/1** (`/comparisons/7/procedures/1`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | PDT (광역동치료) | `/comparisons/7/procedures/1/name` |
| category | M8 | `/comparisons/7/procedures/1/category` |
| mechanism_simple | 감광제 도포 후 광조사 → 피지선 억제 | `/comparisons/7/procedures/1/mechanism_simple` |
| pain | ★★★★☆ | `/comparisons/7/procedures/1/pain` |
| downtime | 3-7일 각질/붉은기 | `/comparisons/7/procedures/1/downtime` |
| onset | 1-3회 후 | `/comparisons/7/procedures/1/onset` |
| duration | 6-12개월 | `/comparisons/7/procedures/1/duration` |
| cost_range | 15-40만원/회 | `/comparisons/7/procedures/1/cost_range` |
| best_for | 중증 염증성 여드름 | `/comparisons/7/procedures/1/best_for` |
| limitations | 자외선 차단 필수, 통증 강함 | `/comparisons/7/procedures/1/limitations` |
| pih_risk | moderate | `/comparisons/7/procedures/1/pih_risk` |

**procedures/2** (`/comparisons/7/procedures/2`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 살리실릭 필링 | `/comparisons/7/procedures/2/name` |
| category | M15 | `/comparisons/7/procedures/2/category` |
| mechanism_simple | BHA로 모공 내 피지/각질 용해 | `/comparisons/7/procedures/2/mechanism_simple` |
| pain | ★☆☆☆☆ | `/comparisons/7/procedures/2/pain` |
| downtime | 1-2일 경미 각질 | `/comparisons/7/procedures/2/downtime` |
| onset | 2-3회 후 점진 | `/comparisons/7/procedures/2/onset` |
| duration | 유지치료 필요 | `/comparisons/7/procedures/2/duration` |
| cost_range | 3-10만원/회 | `/comparisons/7/procedures/2/cost_range` |
| best_for | 블랙헤드, 경미 여드름 | `/comparisons/7/procedures/2/best_for` |
| limitations | 중증 여드름엔 단독 효과 부족 | `/comparisons/7/procedures/2/limitations` |
| pih_risk | very_low | `/comparisons/7/procedures/2/pih_risk` |

**procedures/3** (`/comparisons/7/procedures/3`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 압출+스킨스케일링 | `/comparisons/7/procedures/3/name` |
| category | M15 | `/comparisons/7/procedures/3/category` |
| mechanism_simple | 면포 물리적 제거 + 아쿠아필 세정 | `/comparisons/7/procedures/3/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/7/procedures/3/pain` |
| downtime | 1일 붉은기 | `/comparisons/7/procedures/3/downtime` |
| onset | 즉시 | `/comparisons/7/procedures/3/onset` |
| duration | 2-4주 | `/comparisons/7/procedures/3/duration` |
| cost_range | 3-10만원 | `/comparisons/7/procedures/3/cost_range` |
| best_for | 면포, 화이트/블랙헤드 | `/comparisons/7/procedures/3/best_for` |
| limitations | 흉터 위험, 재발 빠름 | `/comparisons/7/procedures/3/limitations` |
| pih_risk | low | `/comparisons/7/procedures/3/pih_risk` |

**procedures/4** (`/comparisons/7/procedures/4`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 제네시스 (Nd:YAG 롱펄스) | `/comparisons/7/procedures/4/name` |
| category | M8 | `/comparisons/7/procedures/4/category` |
| mechanism_simple | 1064nm 롱펄스로 진피 가열 → 피지 억제 | `/comparisons/7/procedures/4/mechanism_simple` |
| pain | ★☆☆☆☆ | `/comparisons/7/procedures/4/pain` |
| downtime | 없음 | `/comparisons/7/procedures/4/downtime` |
| onset | 3-5회 후 점진 | `/comparisons/7/procedures/4/onset` |
| duration | 3-6개월 | `/comparisons/7/procedures/4/duration` |
| cost_range | 5-15만원/회 | `/comparisons/7/procedures/4/cost_range` |
| best_for | 홍조성 여드름, 여드름 자국 | `/comparisons/7/procedures/4/best_for` |
| limitations | 활성 여드름 단독치료 어려움 | `/comparisons/7/procedures/4/limitations` |
| pih_risk | very_low | `/comparisons/7/procedures/4/pih_risk` |

### 3.9 `/comparisons/8` — id `rejuvenation`

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| id | rejuvenation | `/comparisons/8/id` |
| title | 피부 재생 비교 | `/comparisons/8/title` |
| subtitle | 스킨부스터/PRP/줄기세포 비교 | `/comparisons/8/subtitle` |
| procedures | <array length 5> | `/comparisons/8/procedures` |

**evidence_notes** — 이 비교군 객체에는 키 자체가 없다(빈 배열 아님).


**procedures/0** (`/comparisons/8/procedures/0`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 스킨부스터 (쥬베룩/리쥬란) | `/comparisons/8/procedures/0/name` |
| category | M4 | `/comparisons/8/procedures/0/category` |
| mechanism_simple | 리쥬란=PN(폴리뉴클레오타이드), 쥬베룩=PDLLA 콜라겐 바이오스티뮬레이터+HA | `/comparisons/8/procedures/0/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/8/procedures/0/pain` |
| downtime | 1-2일 잔뾰루지 | `/comparisons/8/procedures/0/downtime` |
| onset | 2-4주 | `/comparisons/8/procedures/0/onset` |
| duration | 리쥬란 약 6개월 / 쥬베룩 약 12-18개월 | `/comparisons/8/procedures/0/duration` |
| cost_range | 15-40만원 | `/comparisons/8/procedures/0/cost_range` |
| best_for | 피부 질감, 수분, 잔주름 | `/comparisons/8/procedures/0/best_for` |
| limitations | 볼륨이나 리프팅은 안 됨 | `/comparisons/8/procedures/0/limitations` |
| pih_risk | none | `/comparisons/8/procedures/0/pih_risk` |

**procedures/1** (`/comparisons/8/procedures/1`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | PRP (자가혈 재생) | `/comparisons/8/procedures/1/name` |
| category | M5 | `/comparisons/8/procedures/1/category` |
| mechanism_simple | 자가 혈소판 성장인자로 재생 촉진 | `/comparisons/8/procedures/1/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/8/procedures/1/pain` |
| downtime | 1-2일 붉은기 | `/comparisons/8/procedures/1/downtime` |
| onset | 2-4주 | `/comparisons/8/procedures/1/onset` |
| duration | 6-12개월 | `/comparisons/8/procedures/1/duration` |
| cost_range | 15-40만원 | `/comparisons/8/procedures/1/cost_range` |
| best_for | 탈모, 피부재생, 상처치유 | `/comparisons/8/procedures/1/best_for` |
| limitations | 개인차 큼 (혈소판 농도 의존) | `/comparisons/8/procedures/1/limitations` |
| pih_risk | none | `/comparisons/8/procedures/1/pih_risk` |

**procedures/2** (`/comparisons/8/procedures/2`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 엑소좀 (줄기세포 유래) | `/comparisons/8/procedures/2/name` |
| category | M17 | `/comparisons/8/procedures/2/category` |
| mechanism_simple | 줄기세포 엑소좀으로 세포 신호 전달 → 재생 | `/comparisons/8/procedures/2/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/8/procedures/2/pain` |
| downtime | 1일 붉은기 | `/comparisons/8/procedures/2/downtime` |
| onset | 2-4주 | `/comparisons/8/procedures/2/onset` |
| duration | 6-12개월 | `/comparisons/8/procedures/2/duration` |
| cost_range | 30-100만원 | `/comparisons/8/procedures/2/cost_range` |
| best_for | 고급 재생, 항노화 | `/comparisons/8/procedures/2/best_for` |
| limitations | 근거 아직 제한적, 가격 높음 | `/comparisons/8/procedures/2/limitations` |
| pih_risk | none | `/comparisons/8/procedures/2/pih_risk` |

**procedures/3** (`/comparisons/8/procedures/3`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 물광주사 (메소테라피) | `/comparisons/8/procedures/3/name` |
| category | M4 | `/comparisons/8/procedures/3/category` |
| mechanism_simple | HA+비타민 칵테일 진피 직접 주입 | `/comparisons/8/procedures/3/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/8/procedures/3/pain` |
| downtime | 1-2일 잔뾰루지 | `/comparisons/8/procedures/3/downtime` |
| onset | 즉시 + 2주 | `/comparisons/8/procedures/3/onset` |
| duration | 2-4개월 | `/comparisons/8/procedures/3/duration` |
| cost_range | 10-30만원 | `/comparisons/8/procedures/3/cost_range` |
| best_for | 수분 광채, 즉각 윤기 | `/comparisons/8/procedures/3/best_for` |
| limitations | 유지기간 짧음, 반복 필요 | `/comparisons/8/procedures/3/limitations` |
| pih_risk | none | `/comparisons/8/procedures/3/pih_risk` |

**procedures/4** (`/comparisons/8/procedures/4`)

| 원본 컬럼명 | 원문 값 | Pointer |
|---|---|---|
| name | 바이오스티뮬레이터 (쥬베룩볼륨) | `/comparisons/8/procedures/4/name` |
| category | M3 | `/comparisons/8/procedures/4/category` |
| mechanism_simple | PDLLA로 콜라겐 네오제네시스 유도 | `/comparisons/8/procedures/4/mechanism_simple` |
| pain | ★★☆☆☆ | `/comparisons/8/procedures/4/pain` |
| downtime | 1-3일 부종 | `/comparisons/8/procedures/4/downtime` |
| onset | 1-3개월 점진 | `/comparisons/8/procedures/4/onset` |
| duration | 18-24개월 | `/comparisons/8/procedures/4/duration` |
| cost_range | 30-80만원/바이알 | `/comparisons/8/procedures/4/cost_range` |
| best_for | 콜라겐 재생, 피부탄력, 장기 개선 | `/comparisons/8/procedures/4/best_for` |
| limitations | 즉각 효과 없음, 결절 가능 | `/comparisons/8/procedures/4/limitations` |
| pih_risk | none | `/comparisons/8/procedures/4/pih_risk` |

## 4. 잠정 관찰 (원문 칸과 분리)

모든 항목은 근거 위치를 붙인 **관찰·해석 후보**다. 「→ Bn/Pn/Fn」은 issues.md 번호.

### 4.1 원장 전체

| 관찰 | 근거 위치 | 상태 |
|---|---|---|
| `pain` 은 모두 5글자 ★/☆ 기호열이며 ★ 개수는 1~4다(★5개 없음). 척도 정의·측정 주체·조건이 원장에 없다. ★ 개수를 수치 통증 점수로 확정하지 않는다 | `/comparisons/*/procedures/*/pain` 39개 | 원문 부족 → B1 |
| `pih_risk` 코드는 `none`16 · `very_low`6 · `low`12 · `moderate`4 · `high`1. 순서·기준(발생률인지 등급인지)이 원장에 없다. `none` 이 「위험 없음」인지 「해당 없음/평가 안 함」인지 구분 불가 | `/comparisons/*/procedures/*/pih_risk` | 원문 부족 → B2 |
| `category`(Mxx) 코드의 정의가 이 원장에 없다. 출현 코드: M1·M2·M3·M4·M5·M6·M7·M8·M9·M10·M11·M12·M14·M15·M17(M13·M16 없음). 같은 코드에 기전이 다른 항목이 함께 있다(예: M8 에 프락셀·피코토닝·Q-스위치·제모 레이저·PDT·스컬프슈어·제네시스, M9 에 울쎄라(HIFU)·써마지(RF)·IPL·바넬라(RF 바디)). 의미는 다른 원장 대조 후속 과제 | `/comparisons/*/procedures/*/category` | 후속 F1 |
| 필드의 내용 종류가 섞여 있다. `onset` 에 시간(2-4주)·회차(3-5회 후 점진)·회차+간격(3-5회 (2-4주 간격))이, `duration` 에 기간·영구/반영구+괄호 한정·백분율(영구 감모 (80-90%))·관리 지시(유지치료 필요)·긴 서술(Q-스위치)이 함께 있다 | `onset` 39 · `duration` 39 | 후속 F2 |
| `cost_range` 는 모두 「N-M만원」 꼴이며 단위 기준이 `/회`8 · `/부위`7 · `/바이알`2 · `/시린지`1 · 표기 없음 21이다. 표기 없는 21개가 무엇을 기준으로 한 가격인지 원장에 없다. 가격 시점·지역도 없다 | `cost_range` 39 | 원문 부족 → B3 |
| `downtime` 은 「없음」「거의 없음」「N-M일 + 증상」꼴이다. 「거의 없음 (멍 가능)」처럼 부정과 가능성이 함께 있다. 증상 사이 `/` 가 둘 중 하나인지 함께인지 원문만으로 정할 수 없다(예: 「3-7일 부종/멍」) | `downtime` | 후속 F3 |
| 기호 `/` 의 쓰임이 여러 가지다: 부위 나열(이마/미간/눈가), 대안 제품(시크릿/인모드), 단위 기준(만원/회), 제품별 값 구분(리쥬란 약 6개월 / 쥬베룩 약 12-18개월), 파장 병기(808nm/810nm), 측정 항목 나열(시간/비용). README 작성 규칙은 `/` = 대안이라고 하지만 이 원장의 모든 쓰임에 맞지 않는다. `+` 도 시술 결합(실+RF/HIFU) 외에 단계(즉시 + 3개월 점진)·대상 조건(밝은 피부 + 굵은 모발)·하한(18-24개월+, 50%+)으로 쓰인다 | `symbol_relation` 후보 전부 | 후속 F3 |
| 같은 이름 「히알루론산 필러」가 두 비교군에 있고 값이 다르다: downtime 1-2일 부종 vs 1-3일 부종, cost_range 20-80만원 vs 30-100만원, mechanism_simple·best_for·limitations 도 다르다(limitations 뒤 문장은 동일). 하나로 합치지 않는다 | `/comparisons/1/procedures/1` · `/comparisons/2/procedures/0` | 후속 F4 |
| 이름 일부가 다른 항목과 겹친다: 리쥬란 (PN주사)(`/1/procedures/3`, duration 6-12개월) ↔ 스킨부스터 (쥬베룩/리쥬란)(`/8/procedures/0`, duration 「리쥬란 약 6개월」), 인모드FX (RF마이크로니들)(`/0/procedures/3`) ↔ 마이크로니들RF (시크릿/인모드)(`/3/procedures/0`), 쥬베룩(`/8/procedures/0`) ↔ 쥬베룩볼륨(`/8/procedures/4`), IPL (광선치료)(`/4/procedures/2`) ↔ IPL 제모(`/5/procedures/3`), Nd:YAG 계열 4곳. 같은 대상인지 정하지 않는다 | 각 name | 후속 F4 |
| 원문 안 약어 풀이가 없다(HIFU·RF·SMAS·PIH·PAH·LIOB·PLLA·PCL·CMC·PDLLA·BHA·TCA·PDT·IPL·MTS·PRP·HA·RCT·RR·Fitz 등). PN 만 `/comparisons/8/procedures/0/mechanism_simple` 에 「PN(폴리뉴클레오타이드)」로 병기됐다. 풀이를 채우지 않았다 | `abbreviation_or_code_in_text` 후보 | 원문 부족 → B4 |

### 4.2 비교군별

| 비교군 | 관찰 | 근거 위치 | 상태 |
|---|---|---|---|
| lifting | evidence_notes 는 「머리말: 서술」 형식이며 머리말(실리프팅·HIFU·RF·조합 고려)이 procedures 의 name 과 문자열이 다르다(울쎄라 (HIFU)·써마지FLX (RF)·실리프팅 (PDO코그)). 어느 항목을 가리키는지는 잠정 | `/comparisons/0/evidence_notes/0..3` | 후속 F5 |
| lifting | HIFU 서술 「2-3개월 점진적 효과」 ↔ 울쎄라 onset 「즉시 + 3개월 점진」: 숫자가 다르다. 같은 대상이라는 전제 없이 불일치 후보로만 기록 | `/comparisons/0/evidence_notes/1` · `/comparisons/0/procedures/0/onset` | 후속 F5 |
| lifting | 「실+RF/HIFU 조합 시 만족도 향상 경향이 보고되나, 근거는 후향적 관찰연구 수준(대조군 부재)」「상보적 기전으로 효과 지속이 기대되나 … RCT는 부족」: 조합 관계·근거 수준·가능성(경향·기대)이 한 문장에 있다. 조합의 의미(보완 효과)와 같은 날 시행 가능 여부는 원문에 없다 | `/comparisons/0/evidence_notes/0` · `/3` | 후속 F6 |
| lifting | 「근거수준 III」의 등급 체계가 원장에 없다 | `/comparisons/0/evidence_notes/3` | 원문 부족 → B5 |
| lifting | 「RF: 안전성 가장 높지만 리프팅 효과 가장 약함」: 최상급 비교의 범위(이 비교군 4개 안인지)가 명시되지 않았다 | `/comparisons/0/evidence_notes/2` | 원문 부족 → B6 |
| lifting | 써마지 「지방위축 위험 (반복 시)」: 조건(반복 시)이 위험에 붙어 있다. 반복의 횟수·간격 기준 없음 | `/comparisons/0/procedures/1/limitations` | 원문 부족 → B6 |
| wrinkle | 보톡스 best_for 「표정주름 (이마, 미간, 눈가)」: 괄호가 부위 예시인지 한정인지 원문만으로 판단 불가. subtitle 「이마/미간/눈가 주름 치료 비교」와 겹친다 | `/comparisons/1/procedures/0/best_for` · `/comparisons/1/subtitle` | 후속 F7 |
| wrinkle·volume | 「드물지만 혈관 폐색 시 피부괴사·실명 위험(응급 히알루로니다제 처치 필요)」가 두 필러 항목에 글자 그대로 반복된다. 「드물지만」의 수식 대상이 「혈관 폐색」(사건 빈도)인지 「피부괴사·실명」(결과 빈도)인지 원문만으로 정할 수 없다. 빈도를 백분율로 바꾸지 않는다 | `/comparisons/1/procedures/1/limitations` · `/comparisons/2/procedures/0/limitations` | 후속 F6 |
| wrinkle·volume | 철자 변이: 「히알루로니다제」(procedures 2곳) ↔ 「히알루로니다아제」(`/comparisons/2/evidence_notes/1`). 같은 물질인지 확정하지 않는다 | 해당 Pointer | 후속 F4 |
| volume | 「지방이식: … 흡수율 변동(30-70%)」 ↔ 자가지방이식 limitations 「생착률 변동 (30-70%)」: 같은 수치에 서로 반대 방향일 수 있는 두 지표(흡수율·생착률)가 붙어 있다. 원장 내부 불일치 후보 — 어느 쪽이 맞는지 정하지 않음 | `/comparisons/2/evidence_notes/2` · `/comparisons/2/procedures/3/limitations` | 원문 부족 → B7 |
| volume | 바이오스티뮬레이터 「18-24개월+ 지속, 연간 비용 최저 … 장기적으로 가장 경제적」: 비용 비교의 계산 근거가 원장에 없다. 「바이오스티뮬레이터」는 이 비교군 name 에 없는 계열명이다(스컬트라 (PLLA)·엘란쎄 (PCL)이 category M3) | `/comparisons/2/evidence_notes/0` | 원문 부족 → B6 · 후속 F5 |
| volume | 엘란쎄 duration 「12-48개월 (타입별)」: 타입 목록·타입별 값이 원장에 없다 | `/comparisons/2/procedures/2/duration` | 원문 부족 → B8 |
| volume | 자가지방이식 duration 「반영구 (생착분)」, onset 「2-3개월 (생착 후)」: 괄호가 적용 대상(생착된 부분)·기준 시점(생착 후)을 한정한다 | `/comparisons/2/procedures/3/duration` · `/onset` | 후속 F2 |
| skin_texture | subtitle 「(Asian skin 특화)」인데 asian_skin_note 는 5개 중 2개 항목에만 있다 | `/comparisons/3/subtitle` · `/comparisons/3/procedures/0..1` | 구조 사실 |
| skin_texture | 「니들RF > 피코 프랙셔널 > CO2 프랙셔널 순 안전」: `>` 의 방향은 문장 끝 「순 안전」으로 보아 왼쪽이 더 안전으로 읽히나 잠정. 순서 관계에 MTS·실리콘피부관리 항목은 없다 | `/comparisons/3/evidence_notes/3` | 후속 F6 |
| skin_texture | 「PIH 위험 높음 (RR 4.44)」이 evidence_notes 와 CO2 limitations 두 곳에 있다. RR 의 비교 대상·대상 집단·출처가 원장에 없다. 보고 수치를 환자 발생률로 바꾸지 않는다 | `/comparisons/3/evidence_notes/1` · `/comparisons/3/procedures/1/limitations` | 원문 부족 → B5 |
| skin_texture | 「케미컬 필: … 깊은 필링(TCA 50%+)」은 이 비교군 procedures 에 대응 항목 이름이 없다(살리실릭 필링은 acne 비교군) | `/comparisons/3/evidence_notes/2` | 후속 F5 |
| skin_texture | 실리콘피부관리 (아쿠아필/하이드라): 「실리콘」이 원문 그대로다. 오기인지 원장만으로 판단할 수 없다 — 고치지 않았다 | `/comparisons/3/procedures/4/name` | 원문 부족 → B9 |
| skin_texture | CO2 asian_skin_note 「저밀도/저에너지 세팅 + 사전 미백 권장」: 권장(필요성)·시점(사전)·조건(세팅)이 함께 있다. 수치 기준 없음 | `/comparisons/3/procedures/1/asian_skin_note` | 원문 부족 → B6 |
| pigment | Q-스위치 duration 이 기간 값이 아니라 지속·재발·대상별 차이(주근깨·일광흑자)·관리 지시(평생 자외선 차단 필수)를 담은 두 문장이다. 「일광흑자」는 best_for(주근깨, 잡티, 오타모반)에 없는 대상이다 | `/comparisons/4/procedures/1/duration` | 후속 F2 |
| pigment | 레이저토닝 「탈색 위험 (과다 시)」: 무엇이 과다한지(회차·출력 등) 생략됐다. 수식 대상을 채우지 않는다 | `/comparisons/4/procedures/3/limitations` | 원문 부족 → B6 |
| hair_removal | duration 「영구 감모 (80-90%)」「반영구 (60-80%)」: 백분율이 무엇의 비율인지(감모율·만족 비율 등)와 기준 시점이 원장에 없다 | `/comparisons/5/procedures/*/duration` | 원문 부족 → B8 |
| hair_removal | onset 이 회차+간격(「3-5회 (2-4주 간격)」)이다. 효과 시작 시점인지 필요 회차인지 필드명과 값의 종류가 다르다 | `/comparisons/5/procedures/*/onset` | 후속 F2 |
| hair_removal | 대상 조건: 「밝은 피부 + 굵은 모발」, 「어두운 피부 (Fitz IV-VI)」, 「어두운 피부 화상 위험」, 「밝은 모발 효과 제한」. 피부 유형 체계(Fitz)는 약어로만 있다 | 해당 best_for·limitations | 후속 F7 · B4 |
| body_contouring | 쿨스컬프팅 「체중 감량은 아님, PAH 위험」: 부정(아님)과 약어 위험이 한 칸. PAH 풀이 없음 | `/comparisons/6/procedures/0/limitations` | B4 |
| body_contouring | 「영구 (사멸 지방)」 3곳: 영구가 「사멸된 지방」에 한정된다는 괄호 | `/comparisons/6/procedures/0..2/duration` | 후속 F2 |
| acne | 아그네스 limitations 「전체 얼굴 시 시간/비용 높음」: 조건(전체 얼굴 시)이 부위 범위다. 「시간/비용」은 두 항목 나열로 보임(잠정) | `/comparisons/7/procedures/0/limitations` | 후속 F3 |
| acne | PDT category M8, 살리실릭 필링·압출+스킨스케일링 M15: Mxx 정의 없음 | 각 category | F1 |
| rejuvenation | 스킨부스터 mechanism_simple 은 `=` 로 제품별 정의(리쥬란=PN…, 쥬베룩=PDLLA…+HA)를 나란히 둔다. duration 도 제품별 값이다. 한 항목 안에 두 제품의 값이 함께 있다 | `/comparisons/8/procedures/0` | 후속 F4 |
| rejuvenation | 엑소좀 「근거 아직 제한적, 가격 높음」: 근거 상태 서술. 시간 표현 「아직」 | `/comparisons/8/procedures/2/limitations` | 후속 F6 |
| rejuvenation | PRP 「개인차 큼 (혈소판 농도 의존)」: 변동 요인이 괄호로 붙어 있다 | `/comparisons/8/procedures/1/limitations` | 후속 F6 |

### 4.3 수식·조건·부정의 보존 확인 (원문 → 수집 위치)

형태소만으로 사라지거나 오탐이 되는 곳을 원문 구간으로 보존했는지 확인한 목록이다. 구절은 모두 `expressions.json` 에 manual(직접 읽기) 후보로 있다.

| 유형 | 원문 구절(예, 전체는 manual-expressions.json) | 형태소만으로의 위험 |
|---|---|---|
| 빈도 | 드물지만 혈관 폐색 시 피부괴사·실명 위험(…) | 「드물」VA 만 남으면 무엇의 빈도인지 끊김 |
| 조건 | 혈관 폐색 시 · (반복 시) · (과다 시) · 전체 얼굴 시 · 조합 시 | 「시」NNB 로 남고, 「즉시」도 regex 상 「…시」 로 잡힘(오탐 9건 판정) |
| 부정 | 즉각 효과 없음 · 구조적 개선은 안 됨 · 체중 감량은 아님 · 녹지 않아 교정 어려움 · 대조군 부재 · RCT는 부족 | 「RCT는」 이 RCT+늘다 로 분석(S01) |
| 가능성 | 비대칭 가능 · 뭉침 가능 · 재발 가능 · 멍 가능 · 경향 · 기대되나 | 「가능」 이 NNG/XR 로 출현마다 다름(S38) |
| 정도·비교 | 가장 뚜렷 · 가장 약함 · 최강 · 현저히 높음 · 더 적합 · 레이저 대비 · 더 많은 회차 · > … 순 안전 | `>` 가 SSC(닫는 괄호)로 태깅(S16) · 비교 기준 생략 다수(B6) |
| 범위·수량 | 3-7일 · 30-70% · 18-24개월+ · TCA 50%+ · Fitz III-V · 808nm/810nm | 「N-M」 이 W_SERIAL 한 토큰 · 「%+」 하한 표지 결합(S39) · 로마숫자 범위 분절 |
| 시간 | 즉시 + 3개월 점진 · 2-3개월 (생착 후) · 3-5회 (2-4주 간격) · 평생 · 아직 | 즉각(S06)·즉시(S07)·점진(S08)·생착(S11)·반영구(S12) 분절 |
| 반대 의미 | 항노화 · 비수술 · 비대칭 | 「항」 독립 명사(S26) — 노화만 떼면 의미 역전. 「비」는 XPN 으로 보존됨 |

## 5. 형태소 분석 — 설정과 알려진 오분절

- 분석기: kiwipiepy **0.24.1**, `Kiwi(num_workers=1, model_type='cong')`, `tokenize()` 옵션 전부 기본값, 내장 기본 사전, 사용자 사전 없음, 오타 교정 없음. 품사 체계 Kiwi(세종 기반 + SL/SH/SN/W_*). `lemma` 는 Kiwi 가 준 값 그대로이며 도메인 표준명이 아니다. 실행: `uv run --python 3.12 --with kiwipiepy==0.24.1`.
- 적용: 텍스트 값 343개(title 9·subtitle 9·evidence_notes 11·name 39·mechanism_simple 39·downtime 39·onset 39·duration 39·cost_range 39·best_for 39·limitations 39·asian_skin_note 2).
- 제외 128개(원문 보존, `excluded_values` 에 사유·위치): `/version` 1(버전 문자열) · `/updated` 1(ISO 날짜) · `/comparisons/*/id` 9(snake_case 식별자) · `category` 39(Mxx 코드) · `pih_risk` 39(snake_case 등급 코드) · `pain` 39(★/☆ 기호열). 제외 규칙은 경로 패턴과 값 형태가 둘 다 맞아야 적용되며, 형태가 어긋나는 값이 나오면 build 가 실패한다.
- 필드명 16개는 값과 따로 `field_names` 에 기록했다. 영문 snake_case 식별자라 Kiwi 결과는 SL 분절일 뿐이며, 규칙 분할(`identifier_parts_rule_based`)을 따로 붙였다(형태소 분석 아님).
- 길이 0 토큰 2개(서술격 조사 복원, `/comparisons/3/evidence_notes/1` [33,33] · `/comparisons/7/procedures/0/best_for` [14,14]) — surface 가 빈 문자열이다.
- 아래는 원문 대조로 확인한 오분절·오태깅이다. **교정하지 않았다** — 원시 토큰을 그대로 두고 출현별로 표시했다. 서명은 모든 값에서 같은 토큰열을 찾아 펼쳤다.

| 서명 | 원문 구절 | 원시 토큰 | 종류 | 영향 | 출현(Pointer [구간]) |
|---|---|---|---|---|---|
| S01 | RCT는 | RCT/SL 늘/VV ᆫ/ETM | mis_segmentation_meaning_risk | 원문에 없는 '늘다(증가)' 용언이 생기고 주제 표지가 사라진다. 'RCT는 부족'의 부족 대상 연결이 토큰만으로는 끊긴다 | `/comparisons/0/evidence_notes/3` [101, 105] |
| S02 | 실로 | 실로/MAG | mis_segmentation_meaning_risk | 도구·재료 '실'이 명사 목록에서 빠지고, 수식어 후보(modifier_phrase)가 오탐으로 생긴다 | `/comparisons/0/procedures/2/mechanism_simple` [0, 2] |
| S03 | 필러 | 필/NNG 러/EC | mis_segmentation_meaning_risk | 제품·시술 계열 명칭 '필러'가 토큰에서 사라진다(같은 문자열의 다른 출현은 NNP 로 정상 분절 — 출현마다 다름) | `/comparisons/1/procedures/1/name` [6, 8]<br>`/comparisons/2/procedures/0/name` [6, 8] |
| S04 | 필러 | 피/XPN ᆯ러/EC | mis_segmentation_meaning_risk | '필러 이동'의 이동 주체가 토큰에서 사라진다 | `/comparisons/2/procedures/0/limitations` [10, 12] |
| S05 | 잔뾰루지 | 자/NNG ᆫ/ETM 뾰루지/NNG | mis_segmentation_meaning_risk | 크기 수식 '잔'이 형태로 남지 않고 '자다/자' 계열 가짜 형태가 생긴다 | `/comparisons/1/procedures/3/downtime` [5, 9]<br>`/comparisons/8/procedures/0/downtime` [5, 9]<br>`/comparisons/8/procedures/3/downtime` [5, 9] |
| S06 | 즉각 | 즉/MAJ 각/MM | mis_segmentation_meaning_risk | 시점 표현 '즉각(효과 발현 시점)'이 사라지고 '각(各)' 범위 수식이 오탐으로 생긴다 | `/comparisons/2/procedures/0/mechanism_simple` [6, 8] |
| S07 | 즉시 | 즉/MAG 시/NNG | mis_segmentation_meaning_risk | 시점 '즉시'가 사라지고 '시'가 조건 표지(…시)와 같은 형태로 남아 조건 오탐 위험 | `/comparisons/2/procedures/2/onset` [0, 2] |
| S08 | 점진 | 점/NNG 진/NNG | term_split | 변화 속도 표현 '점진'이 토큰에서 사라진다 | `/comparisons/2/procedures/1/onset` [6, 8]<br>`/comparisons/8/procedures/4/onset` [6, 8] |
| S09 | 겔 | 것/NNB 이/VCP ᆯ/ETM | mis_segmentation_meaning_risk | 제형 '겔'이 사라지고 원문에 없는 의존명사·서술격 조사가 생긴다 | `/comparisons/2/procedures/2/mechanism_simple` [18, 19] |
| S10 | 겔로 | 겔로/NNG | mis_tag_minor | 제형 '겔'과 도구 관계 조사가 분리되지 않는다 | `/comparisons/2/procedures/0/mechanism_simple` [3, 5] |
| S11 | 생착 | 생/XPN 착/NNG | term_split | 기준 시점 '생착 후'의 '생착'이 토큰에서 사라진다 | `/comparisons/2/evidence_notes/2` [6, 8]<br>`/comparisons/2/procedures/3/onset` [7, 9] |
| S12 | 반영구 | 반영/NNG 구/NNG | mis_segmentation_meaning_risk | 지속 특성 '반영구'가 사라지고 무관한 '반영'이 생긴다(같은 문자열의 다른 출현은 반/XPN+영구 로 정상) | `/comparisons/2/procedures/3/duration` [0, 3] |
| S13 | 채취부 | 채취/NNG 부/XPN | mis_tag_minor | 통증 발생 위치(채취 부위) 표지가 접두사로 남는다 | `/comparisons/2/procedures/3/limitations` [17, 20] |
| S14 | CO2 | CO/SL 2/SN | term_split | 장비·레이저 명칭이 쪼개지고 숫자 '2'가 수량처럼 남는다 | `/comparisons/3/evidence_notes/1` [0, 3]<br>`/comparisons/3/evidence_notes/3` [46, 49]<br>`/comparisons/3/procedures/1/name` [0, 3]<br>`/comparisons/3/procedures/1/mechanism_simple` [0, 3] |
| S15 | 효과지만 | 이/VCP | zero_length_token | surface 가 빈 문자열인 토큰이다. 원문 구간 재현 검사는 빈 구간을 허용해야 한다. 같은 원장의 다른 길이 0 토큰('과다' 안 이/VCP)은 S23 에 포함 | `/comparisons/3/evidence_notes/1` [31, 35] |
| S16 | > | >/SSC | mis_segmentation_meaning_risk | '니들RF > 피코 프랙셔널 > CO2 프랙셔널 순 안전'의 순서 관계가 괄호 닫힘으로 보인다 | `/comparisons/3/evidence_notes/3` [34, 35]<br>`/comparisons/3/evidence_notes/3` [44, 45] |
| S17 | 피코 | 피/NNG 코/NNG | mis_segmentation_meaning_risk | 장비 명칭이 사라지고 신체 부위 단어와 같은 형태 '코'가 생겨 부위 오탐 위험 | `/comparisons/3/evidence_notes/3` [36, 38] |
| S18 | 마이크로니들RF | 마이크로니/NNG 들/XSN | mis_segmentation_meaning_risk | 명칭이 깨지고 원문에 없는 복수 표지가 생긴다 | `/comparisons/3/procedures/0/name` [0, 8] |
| S19 | 다회 | 다/MAG 회/NNG | mis_segmentation_meaning_risk | 회차 수식 '다회'가 '다(모두)' 부사로 바뀌어 범위 오탐 위험 | `/comparisons/4/procedures/0/limitations` [0, 2] |
| S20 | 타겟 | 타/VV 게/EC ᆺ/Z_CODA | mis_segmentation_meaning_risk | 작용 대상 관계어 '타겟'이 사라지고 원문에 없는 용언이 생긴다(같은 문자열 다른 출현은 NNG 로 정상) | `/comparisons/4/procedures/2/mechanism_simple` [17, 19] |
| S21 | 감모 | 감/NNG 모/NNG | term_split | '영구 감모'가 '영구'만 남아 영구 제거로 오독될 위험 | `/comparisons/5/procedures/0/duration` [3, 5]<br>`/comparisons/5/procedures/1/duration` [3, 5]<br>`/comparisons/5/procedures/2/duration` [3, 5] |
| S22 | 복부 | 복/NNG 부/NNG | term_split | 부위 명칭이 토큰에서 사라진다(다른 출현은 NNG 한 토큰으로 정상) | `/comparisons/6/procedures/0/best_for` [7, 9] |
| S23 | 과다 | 과/NNG 이/VCP 다/EF | mis_segmentation_meaning_risk | 정도 표현 '과다'가 사라지고 원문에 없는 종결 서술이 생긴다 | `/comparisons/7/procedures/0/best_for` [13, 15] |
| S24 | 재발 | 재/XPN 발/NNG | mis_segmentation_meaning_risk | 경과 표현 '재발'이 사라지고 신체 부위 단어와 같은 형태 '발'이 생겨 부위 오탐 위험 | `/comparisons/7/procedures/3/limitations` [7, 9] |
| S25 | 리쥬란 | 리쥬/NNP 란/JX | mis_segmentation_meaning_risk | 제품별 지속기간 대응(리쥬란 약 6개월)의 제품명이 깨진다 | `/comparisons/8/procedures/0/duration` [0, 3] |
| S26 | 항노화 | 항/NNG 노화/NNG | mis_segmentation_meaning_risk | '노화'만 따로 쓰면 의미가 뒤집힌다(항노화 → 노화) | `/comparisons/8/procedures/2/best_for` [7, 10] |
| S27 | 중등도 | 중등/NNG 도/JX | mis_segmentation_meaning_risk | 처짐 정도 수식이 사라지고 원문에 없는 첨가 의미 '도'가 생긴다 | `/comparisons/0/procedures/0/best_for` [0, 3] |
| S28 | 필: | 필/NNB | mis_tag_minor | 시술 계열 명칭이 의존명사로 남는다 | `/comparisons/3/evidence_notes/2` [4, 6] |
| S29 | 인모드FX | 인/NNG 모드/NNG | term_split | 제품명 대조 시 '인모드'(다른 출현은 NNG 한 토큰)와 형태가 달라진다 | `/comparisons/0/procedures/3/name` [0, 5] |
| S30 | 박스카 | 박스/NNG 카/NNG | term_split | 흉터 유형 명칭이 출현마다 형태가 다르다(다른 출현은 한 토큰) | `/comparisons/3/procedures/0/limitations` [3, 6] |
| S31 | 각질 | 각/NNG 질/XSN | term_split | 증상 명칭이 출현마다 형태가 다르다(다른 출현은 NNG 한 토큰) | `/comparisons/7/procedures/2/downtime` [8, 10] |
| S32 | 롱펄스 | 롱/NNG 펄스/NNG | term_split | 장비 방식 명칭이 출현마다 다르다(이름 필드 출현은 NNP 한 토큰) | `/comparisons/7/procedures/4/mechanism_simple` [7, 10] |
| S33 | 아쿠아필 | 아쿠아/NNP 필/NNG | term_split | 제품·시술명이 출현마다 다르다(다른 출현은 NNG 한 토큰) | `/comparisons/7/procedures/3/mechanism_simple` [12, 16] |
| S34 | 마이크로스피어 | 마이크로/NNG 스피어/NNP | term_split | 재질 형태 명칭이 쪼개진다 | `/comparisons/2/procedures/2/mechanism_simple` [4, 11] |
| S35 | 빛으로 | 빛으로/NNP | mis_tag_minor | 작용 수단 '빛'과 도구 관계 조사가 분리되지 않는다 | `/comparisons/4/procedures/2/mechanism_simple` [4, 7]<br>`/comparisons/5/procedures/3/mechanism_simple` [4, 7] |
| S36 | 초음파 | 초/XPN 음파/NNG | term_split | 에너지원 명칭이 쪼개진다 | `/comparisons/0/procedures/0/mechanism_simple` [0, 3]<br>`/comparisons/6/procedures/1/mechanism_simple` [4, 7] |
| S37 | 당김 | 당김/NNP | mis_tag_minor | 작용(당기다) 서술이 고유명사로 남는다 | `/comparisons/0/procedures/2/mechanism_simple` [7, 9] |
| S38 | 가능 | 가능/XR | mis_tag_minor | 가능성 표현의 품사가 출현마다 다르다 — 품사로 가능성 후보를 고르면 누락 | `/comparisons/4/procedures/0/limitations` [13, 15] |
| S39 | %+ | %+/SW | mis_tag_minor | '50%+'의 하한(이상) 표지가 단위 기호와 분리되지 않는다 | `/comparisons/3/evidence_notes/2` [36, 38] |

## 6. 복합 표현 수집

`category_candidate` 는 탐색 관점 이름이다. 확정 분류가 아니다. regex·keyword 결과는 전수 의미 조사가 아니며, 같은 구간이 여러 범주에 있는 것은 의도된 겹침이다.

| category_candidate | 건수 | 방법 |
|---|---|---|
| abbreviation_or_code_in_text | 65 | manual |
| condition_scope | 47 | keyword |
| context_phrase.condition_risk | 5 | manual |
| context_phrase.degree_comparison | 31 | manual |
| context_phrase.evidence | 8 | manual |
| context_phrase.frequency_condition_risk | 6 | manual |
| context_phrase.mechanism | 15 | manual |
| context_phrase.necessity | 15 | manual |
| context_phrase.negation_limit | 24 | manual |
| context_phrase.possibility | 9 | manual |
| context_phrase.target_population | 10 | manual |
| context_phrase.timing_course | 37 | manual |
| evidence_statement | 18 | keyword |
| frequency_degree_comparison | 108 | keyword |
| latin_term | 79 | regex |
| modifier_phrase | 131 | Kiwi 품사 MAG 포함 어절+다음 어절, Kiwi 품사 MAJ 포함 어절+다음 어절, Kiwi 품사 MM 포함 어절+다음 어절, Kiwi 품사 VA 포함 어절+다음 어절, Kiwi 품사 VA-I 포함 어절+다음 어절, Kiwi 품사 VCN 포함 어절+다음 어절, Kiwi 품사 XR 포함 어절+다음 어절 |
| necessity_recommendation | 23 | keyword |
| negation_limit | 40 | keyword |
| parenthetical | 70 | regex |
| possibility_risk | 25 | keyword |
| quantity_range_unit | 158 | regex |
| reference_to_other_item_candidate | 33 | manual |
| segment.colon_head | 11 | 첫 ':' 앞 머리말 |
| segment.comma_part | 130 | 괄호 밖 ',' 기준 분할 |
| segment.sentence | 29 | regex 문장분할: '. ' 뒤 경계 |
| segment.value | 343 | 값 전체 |
| symbol_relation | 246 | regex |
| term_candidate.adverse_or_downtime_event | 65 | manual |
| term_candidate.anatomy_or_target | 65 | manual |
| term_candidate.concern_or_indication | 70 | manual |
| term_candidate.mechanism_action | 93 | manual |
| term_candidate.mechanism_agent_or_substance | 71 | manual |
| timing_course | 101 | keyword |
| **합계** | **2181** | 완전 중복 제거 0건 |

직접 판정(expression-review.json): false_positive 32, partial_match 3, partial_match_ok 13. 오분절 표시 토큰에서 파생된 modifier_phrase 6건(표시만, 삭제 안 함). 어떤 표현 후보(segment.* 제외)에도 덮이지 않은 어절 81개 — expressions.json `uncovered_eojeol`.

미포착 어절은 비교·시술·치료·피부·효과 같은 일반 명사, 제목 낱말, 형태소 서명으로 이미 표시한 낱말(필러·타겟 등)이다. 목록을 직접 읽고 남겼다.

## 7. 상태

**1차 범위 종료: 예(아래 기준 충족).** **원장 전체 완료: 아님** — 원문 부족 B 9묶음, 후속 의미 조사 F 7묶음, 형태소 한계 A 3이 열려 있다.

| 구분 | 상태 |
|---|---|
| 전수 읽기 | 최상위 3키 + comparison 9개 + procedures 39개 + evidence_notes 11문장 전부. 원문 통독 1회 + 토큰 대조 1회 + 미포착·후보 판정 1회 |
| 구조·값 수집 | 노드 533/533 · 키 473 · 중복 키 0 · 선택적 키 2종(evidence_notes·asian_skin_note) · 빈 값 0 |
| 형태소·표현 수집 | Kiwi 0.24.1(cong, 1스레드) 343값 2,127토큰 · 제외 128(사유 6종) · 필드명 16 · 확인 오분절 39서명 52출현(표시, 교정 아님) · NNP 110건 미판정(A2) · 표현 후보 2,181(직접 판정 48) |
| 기계 검증 | build.py 내부 검사 + 독립 verify.py 통과, 변이 시험 검출 — [validation.md](./validation.md) |
| 읽기 검토 | §4 잠정 관찰·§4.3 보존 확인. 같은 에이전트 재독(독립 검토 아님) |
| 알려진 분석 오류 | §5 표 52출현 + NNP 110 미판정 + 길이 0 토큰 2 |
| 열린 미결 | B 9묶음 · C(사용자 결정 필요) 0 · 잠정 해석은 §4 표의 「잠정」 표시 |
| 후속 의미 조사 | F1~F7. 시작 안 함 |
