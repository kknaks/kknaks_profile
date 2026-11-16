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

<!-- GENERATED:COLUMNS -->

구조 사실(원문 대응):

- 최상위 키 3개, 순서 `version` → `updated` → `comparisons`. 이 원장에는 최상위 `description` 키가 없다.
- `comparisons` = 객체 9개. 키 순서는 두 가지뿐이다: `id, title, subtitle, evidence_notes, procedures`(comparison 0·2·3) / `id, title, subtitle, procedures`(1·4·5·6·7·8). **evidence_notes 는 선택적 키**이며, 없는 6개 객체에는 빈 배열이 아니라 키 자체가 없다.
- `procedures` = 비교군별 4·4·4·5·4·4·4·5·5개, 합계 39개 객체. 키 순서는 두 가지뿐이다: 11키 `name, category, mechanism_simple, pain, downtime, onset, duration, cost_range, best_for, limitations, pih_risk` / 12키(끝에 `asian_skin_note`). **asian_skin_note 는 `/comparisons/3/procedures/0`·`/1` 두 곳에만** 있다.
- 자료형: 노드 533 = object 49(루트 1 + comparison 9 + procedure 39) · array 13(comparisons 1 + evidence_notes 3 + procedures 9) · string 471. **숫자·불리언·null 없음.** 빈 문자열·빈 배열·빈 객체 없음.
- 중복 키 없음(자체 파서와 verify.py 의 `object_pairs_hook` 두 방법으로 확인).

## 3. 항목별 값 — 원문 대응 (원본 컬럼명 그대로, 배열은 원본 순서)

표 칸의 `|` 는 Markdown 때문에 `\|` 로 적었다. 그 외에는 원문 문자 그대로다.

<!-- GENERATED:VALUES -->

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

<!-- GENERATED:SEG -->

## 6. 복합 표현 수집

`category_candidate` 는 탐색 관점 이름이다. 확정 분류가 아니다. regex·keyword 결과는 전수 의미 조사가 아니며, 같은 구간이 여러 범주에 있는 것은 의도된 겹침이다.

<!-- GENERATED:EXPR -->

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
