# batch-03 독립 검토 — taxonomy

- 검토자: Opus 검토 워커 (task_ab74d9d8c1ed / ctx_4902daa50a97), 2026-11-09
- 대상: `first-pass/taxonomy/` (재시작된 새 53구획 S000~S052). 이전에 삭제된 103구획 계획과는 관계가 없다.
- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/taxonomy.json`
- 쓴 파일은 이 보고서 하나다. 독립 검사 스크립트는 세션 scratchpad(`indep.py`, `show.py`)에만 두었다. 원본과 결과 폴더는 읽기만 했다.

## 판정

| 원장 | 판정 | 1차 범위 종료 | 원장 전체 완료 |
|---|---|---|---|
| taxonomy | **WARN** (종료를 막는 추출 오류는 없음) | **가능** | **아님**: B 34 · I 65 · F 47 · K 4가 열려 있음 |

WARN 사유는 하나다. 정규식 자동 후보(`expressions.json` auto)에 수식어·지시어 패턴이 빠져 있다(§3-1). 그런데 `validation.md`는 「나머지 출현은 정규식 후보로 전수 보존」이라고 적어 실제보다 넓게 주장한다. 원문 값·Pointer·형태소 토큰은 전부 보존돼 있어 추출 누락으로 보지 않았고, 종료를 막지 않는 한계로 분류했다. 다만 이 한계가 아직 기록되지 않았으므로 기록하기를 권고한다.

## 1. 반드시 고칠 추출 오류 (종료 차단)

**0건.** 누락·변형·잘못된 Pointer·구간 오류를 찾지 못했다(§2 근거).

## 2. 기계 전수 대조 — 명령과 실제 결과

### 2-1. 기존 verify.py 재실행 (읽기 전용 확인 후)

먼저 `grep`으로 verify.py에 쓰기 호출이 없음을 확인했다(`open()`은 읽기뿐이고, 출력은 stdout의 `json.dumps`).

```
python3 orchestration/work/phub-ledger-redesign/first-pass/taxonomy/verify.py   # 레포 루트
EXIT=0
source_nodes 17593 · source_leaves_or_empty 11931 · duplicate_keys 0 · sections 53 · sections_read 53
morph_applied 10844 · morph_excluded 985 · tokens 98254 · zero_length_tokens 19 · field_names 57
known_seg_flags 2023 · expr_auto 10974 · expr_manual 1073 · issues B34 F47 I65 K4
sha_start = sha_end = 5492d0d4354406477206cb46f1bb735ca684d2d4a218c11d31e7889b20f4e8fe · failure_count 0
shasum -a 256 taxonomy.json → 5492d0d4…f8fe (dispatch 기록 source_sha256 과 같음, 660,679 bytes)
```

### 2-2. 독립 검사 (scratchpad `indep.py`, 결과 폴더의 build·verify 코드 미사용)

원본 바이트를 직접 훑는 스캐너를 따로 작성했다. 이 스캐너가 Pointer·자료형·값·리터럴 바이트 구간·키 구간·중복 키·이스케이프를 독자적으로 만들고, 그 결과를 산출물과 대조했다. **실패 0.**

| 항목 | 독립 결과 | 산출물과 대조 |
|---|---|---|
| 전체 경로 집합 | 17,593 노드 (object 3,265 · array 2,434 · string 11,829 · boolean 48 · null 17 · **number 0**) | source-map 누락 0 · 초과 0, 문서 순서 일치 |
| 자료형·모든 말단 값 | `json.loads` 결과와도 일치 | type·value(타입 포함) 불일치 0 |
| 빈 값 | 59개: 빈 배열 35 · 빈 문자열 22 · 빈 객체 2 | `empty` 표시 불일치 0. review-part에 `""`/`{}`/`[]`로 표기됨(예: S025 `/modality/7/subcategories/5/items/13/detail`·`/extracted`) |
| 바이트·문자 구간 | 모든 노드의 리터럴 바이트 구간, 바이트→코드포인트 변환, 키 리터럴 구간 | 불일치 0 |
| 중복 키 · 이스케이프 | 0 · 0 | 기록과 같음 |
| 구획 소유 합집합 | 53구획 owned_pointers 합집합 = 전체 경로 | 누락 0 · 초과 0 · 중복 소유 0 · section 표기 불일치 0 |
| 구획 파일 실재 | reading·manual·review-part 각 53개 | 누락 0. 모든 manual `state=read`, last_pointer 가 자기 구획 안에 있음 |
| 분할 문서 원문 대응 | 모든 소유 Pointer가 review-part에 있고, 말단 값이 같은 줄에 있음 | 누락 0. review.md 목차에 53개 파트 모두 연결됨 |
| 읽기 렌더 | 비어 있지 않은 문자열 값이 모두 자기 구획 `reading/S###.txt`에 있음 | 누락 0 |
| 형태소 적용/제외 | 문자열 11,829 = 적용 10,844 + 제외 985, 각 정확히 1회 | 토큰 `text[s:e]==surface` 불일치 0, 파트 sha256 일치, **토큰이 덮지 않은 비공백 문자 0** |
| 제외 사유 | id 857 · modality_ref 원소 105 · reclassified_to 1 · 빈 문자열 22 | 모두 사유 있음 |
| 필드명 | 57종, 출현 위치 집합 | 불일치 0 |
| 알려진 오분절 2,023 | 구간이 원문에서 재현됨 | 불일치 0 |
| 표현 auto 10,974 / manual 1,073 | 구간·문장 구간 재현, 구획 표기 | 불일치 0 · (종류, Pointer, 구간, 관점) 중복 0 |
| 관찰·미결 Pointer | 모두 원문에 존재 | 불일치 0. 미결 ID 중복 0, 상태 B34/F47/I65/K4 (A0·C0) |

구조 수량을 독립 집계한 결과가 브리프와 같다. modality 17 · subcategories 74 · items 523 · products 59 · problem 14 · problem subcategories 53 · problem items 117(modality_ref 원소 105, 빈 배열 26).

`extracted` 내부도 빠짐없이 들어 있다. 모달리티 17개 층(overview·mechanism·indications{primary,extended}·contraindications{absolute,relative}·safety{common,uncommon,serious}·onset_duration{onset,peak,duration}·aftercare·related_techniques), 항목 523개 층, 제품 59개 층의 변형 키가 모두 경로 집합에 들어 있다. 변형 키는 common_adverse_effects·serious_adverse_effects·long_term·safety/note·safety/contraindications·maintenance·peak_effect·diffusion·common_side_effects·secondary다. 이 키들은 review.md 컬럼 구성 표에 「선택적」 행으로 각각 올라 있다.

**한계:** 이 대조는 원문 대응을 확인한 것이다. 기존 워커가 53구획을 의미까지 다 읽었다는 증명은 아니다. 읽기 수행의 근거는 manual 기록·관찰이 실제로 존재하고 그 내용이 원문과 맞는다는 점이며, 아래 §4 표본에서만 확인했다.

## 3. 비차단 한계 · 분류 보완

### 3-1. 정규식 자동 후보의 패턴 공백 (새 발견, 기록되지 않음 → 기록 권고)

`expressions.json` method.patterns 에 아래 단서가 없다. 그래서 auto 후보와 manual 어느 구간에도 걸리지 않는 출현이 남는다. 계수는 문자열 값 안의 부분 일치 수이며, 「덮임」은 auto·manual 어떤 구간에도 포함되지 않은 것만 셌다.

| 단서 (RESUME §4 관련) | 출현 | 어떤 표현 구간에도 없음 | 비고 |
|---|---|---|---|
| `자제` (회피 지시) | 334 | 298 | 「부정·금지」 패턴에 없음. manual 대표 29건 |
| `깊`(깊이·깊숙이·깊게) | 180 | 77 | 패턴은 `깊은`만 잡음 |
| `얇` (두께) | 6 | 3 | 패턴 없음 |
| `서서히`·`점진` (변화 속도) | 16 · 56 | 13 · 44 | 속도 범주 패턴 없음 |
| `권장`·`주의`·`필요` | 270 · 62 · 83 | 243 · 47 · 49 | 권고 강도 패턴 없음 |
| `심각` | 5 | 4 | 예: `심각한 심폐질환 환자` (`/modality/*/extracted/contraindications/relative/1`) |
| `약 N` (근사) | — | 10 | 예: `색소침착(PIH) - 약 1%` |
| 숫자 범위 + Pa·N 단위 | — | 14 | 예: `G' 200-400 Pa`, `응집력 1.0-1.5 N`. 수량 패턴에 Pa·N이 없음 |
| `시 ` (조건) | 360 | 270 | 조건 패턴에 `시에`만 있음 |

반대로 `드물`·`드문`·`매우`·`극히`·`않`·`없`·`금지`·`가능`·`수 있`·`이상`·`이내`·`미만`·`경미`·`심한`·`얕`·`경우`·`%`·`~` 범위는 모두 어떤 구간에 덮여 있다(미덮임 0).

- **영향:** 원문 값·Pointer·형태소 토큰은 전부 남아 있으므로 정보는 사라지지 않았다. 하지만 표현 기록만 보고 회피·깊이·속도·권고 수식을 찾는 후속 작업은 이 출현을 놓친다.
- **권고:** `issues.md`에 K 한 줄을 추가하고 `validation.md`의 「나머지 출현은 정규식 후보로 전수 보존」 문구를 「정규식에 포함된 단서만 보존, 위 공백 있음」으로 바로잡을 것. 같은 원장을 재조사할 필요는 없다.

### 3-2. 기존 기록이 이미 다루는 한계 (위치·영향 기록 확인)

- K: W_SERIAL 숫자 연쇄 1,576 출현, 전문어·브랜드 오분석(GLOBAL-K02, 구획 seg_errors), 길이 0 토큰 19건(kiwi 동작, `morphology.json` span_unit 에 명시).
- B: U+FFFD 손상 `/modality/0/subcategories/0/items/3/extracted/indications/primary/2`(`눈�리 주름(까치발)`, S001-B01). 원래 글자를 추정하지 않은 것까지 확인했다. 빈 extracted 2개(S025-B01), 빈 items 2개(S045-B01), 빈 문자열 22, mfds null 17, 정의 없는 약어, 모집단 없는 비율(GLOBAL-B01).
- 제외 분류 보완(비차단): id 제외 857건 중 `M15-도포`·`M15-팩`(`/modality/14/subcategories/14/id`, `/15/id`)은 한글 단어를 포함한다. 둘 다 S045 관찰에 기록돼 있어 형태소 제외의 영향은 작다.
- 원문에 **number 자료형이 0개**다(용량·기간·%가 모두 문자열 안에 있음). 수치를 쓰려면 문자열에서 분해해야 하는 후속 과제다. 기록은 수량 패턴과 W_SERIAL K로만 간접적으로 되어 있다.
- 비어 있는 products 배열은 7개다(M6·M10·M12·M13·M14·M15·M16). 이 중 6개는 구획 관찰(P) 문장에 「products 빈 배열」로 적혀 있다(S015·S032·S035·S036·S037·S045). **M16(`/modality/15/products`, S049)만 관찰이 없다.** 원문 값은 review-part에 `[]`로 보존돼 있으므로 차단 사유가 아니다.

## 4. 독립 원문 읽기 — **표본** (전체 재독 아님)

원문 JSON을 직접 열고, 해당 Pointer의 manual 표현·auto 후보·관찰·미결과 대조했다. 약 380노드로, 전체 17,593노드의 약 2%다.

| 구획 | 읽은 Pointer | 확인한 것 |
|---|---|---|
| S001 | `/modality/0/subcategories/0/items/1` 전체 (디스포트) | `약 1.5%` 근사·조건(`반복 시술 시`), `수시간 후 가능`, `자제 권장`, `(사우나 등)`, 범위 `2-3일`·`3-4개월`, peak 선택 필드. manual 3·auto 다수가 원문과 같음 |
| S001 | `/modality/0/subcategories/0/items/3/extracted/indications/primary/2` | U+FFFD 보존, B로 기록됨 |
| S003 | `/modality/0/extracted` 전체 (모달리티 층) | 부정 `중추신경에는 영향을 주지 않고`, 가능성 `줄어들 수 있음`, 빈도+부정+주장 `드물게 … (20년간 치명적 부작용 보고 없음)`, 근거 진술 `RCT에서 확인되지 않음`, 다른 단위끼리의 범위 `12시간~4일`. 층마다 문체·구성이 다르다는 관찰과 related_techniques 연결 없음(S003-F02)도 확인 |
| S003 | `/modality/0/products/0` 전체 | `name_en`·`manufacturer`·`country`·`mfds`(불리언). 시술 전 지시가 aftercare 에 있는 점(`1주일 전부터 중단`), 제품/항목 사이의 반대 지시(S003-I01), 제조사 표기 차이(I). duration 칸에 `1개월 완전 효과` 가 섞인 것은 auto 수량으로만 잡혀 있고 관찰은 없다(비차단) |
| S025 | `/modality/7/subcategories/5/items/13`, `/14` | 빈 detail·빈 extracted 표기와 B 기록, LLLT 중복 항목 F(S043-F02) |
| S045 | `/modality/14/subcategories/14`, `/15` | 빈 items 배열, 한글 id 관찰, B 기록 |
| S050 | `/modality/16/subcategories/0/items/0` 전체, `/modality/16/extracted/safety`·`/onset_duration` | `일시적 홍반`, `장기 부작용 평가 불충분(…)`, 속도 `서서히 효과 발현`(manual 수식), `오래 지속될 수 있지만, 재흡수율에 따라 차이`(가능성·조건), 원장에 없는 제품명 `아디포셀` 관찰 |
| S051 | `/problem/0` 앞부분(subcategories 0~5 일부) | problem 항목 키 구성(extracted 없음), modality_ref 원소, detail `콧대/코끝` 등 기호 결합 |
| S052 | `/problem/13` 전체 | `냉동/CO2`·`겨드랑이/손/발`·`308nm`·`영구적`, 빈 modality_ref(미라드라이)와 대응 후보 F(S052-F01), 「M13만 참조되지 않음」을 기계 집계로 명시한 점 |

표본에서 원문 인용은 모두 원문과 같았다. 잠정 관찰(P)·불일치(I)·부족(B)·후속(F)이 원문 칸과 분리되어 있었고, 수식·조건·부정·가능성·범위 문구가 manual 또는 auto 구간에 남아 있었다. 원문 부족(B)을 에이전트 해석 과제로 혼동한 사례는 없었다. 다만 표본 밖 49구획의 의미 읽기 품질은 이 검토로 보증하지 않는다.

## 5. 미결 처리 상태

- A(에이전트 오류) 0 · **C(현재 사용자 결정) 0**. 원본 변경 후보(빈 modality_ref 보강, 중복 문장, 제조사 표기 등)는 F/I로 분류돼 있고, 원본 보존 지시와 맞는다. 원문 안의 불일치(I 65)와 사용자 결정(C)이 섞이지 않았다.
- B 34 · I 65 · F 47 · K 4는 열린 상태로 남아 있으며, 해결된 것으로 세지 않았다. 각 항목에 Pointer·영향이 있다(기계 확인: Pointer 유효, ID 중복 0).
- **지금 필요한 사용자 선택: 0건.** §3-1은 기록 보완 권고이며 선택 사항이 아니다.

## 6. 결과 · 컬럼표 접근 경로

- 목차·컬럼 구성 표: `first-pass/taxonomy/review.md` (경로 패턴·자료형·중첩·선택적·빈 값·예시 Pointer)
- 구획별 원문 값·관찰·표현·오분절·미결: `first-pass/taxonomy/review-part-S000.md` ~ `review-part-S052.md`
- 검증 서술·명령: `first-pass/taxonomy/validation.md` · 미결 전체 목록: `first-pass/taxonomy/issues.md`
- 구조화 기록: `source-map.json` · `coverage.json` · `morphology.json`(+`morphology/S###.json`) · `expressions.json` · `manual/S###.json`·`GLOBAL.json`
- 재검증: 레포 루트에서 `python3 orchestration/work/phub-ledger-redesign/first-pass/taxonomy/verify.py`

## 7. 상태 요약 (스킬 형식)

| 구분 | 상태 |
|---|---|
| 1차 범위 종료 | 가능 (WARN: §3-1 기록 보완 권고) |
| 원장 전체 완료 | 아님 |
| 전수 읽기 | 53/53 기록 있음. 이 검토에서 실제로 재독한 것은 표본 약 2% |
| 구조·값 수집 | 독립 대조 실패 0 |
| 형태소·표현 수집 | 적용/제외 전수 대응. auto 패턴 공백은 §3-1 |
| 기계 검증 | verify.py EXIT 0 / 독립 검사 실패 0 / 원본 해시 불변 |
| 읽기 검토 | 표본 PASS |
| 알려진 분석 오류 | K 4 묶음 (W_SERIAL 등 2,023 표시) |
| 열린 미결 | B 34 · I 65 · F 47 · K 4 (C 0) |
| 후속 의미 조사 | 남음 (F, 수치 문자열 분해, 개체·축 분해) |
