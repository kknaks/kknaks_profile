# complications.json — 1차 조사 (읽기용)

> **1차 범위: 종료 기준 충족(작성자 자체 판정 · batch-01 독립 묶음 검토 WARN — 1차 종료를 막지 않음 · 코디 확인 전).** **원장 전체 완료 아님** — 열린 미결은 [issues.md](./issues.md)에 있다(원문 부족 B 9 · 잠정 P 4 · 후속 의미 조사 F 9 · 분석 한계 A 4 · 사용자 결정 필요 C 0).
>
> 이 문서는 **원문 값**과 **잠정 관찰**을 다른 칸·다른 절에 나눠 적는다. 표의 「원문 값」 칸은 원장 문자열 그대로다(마크다운 표 때문에 `|` 만 `\|` 로 바꿨는데, 이 원장에는 `|` 가 없다). 「잠정 관찰」은 근거 Pointer 를 붙인 해석 후보이며 확정된 의미·관계가 아니다. 공통 개념 ID·동의어·부위 체계·관계 방향은 정하지 않았다(1차 범위 밖).
> 원문의 임상·법적 주장은 **원장에 그렇게 적혀 있다**는 사실로만 기록했다. 사실 여부는 검증하지 않았고 외부 자료로 보충하지 않았다.

## 상태

| 구분 | 상태 |
|---|---|
| 전수 읽기 | 상위 2키 · 카테고리 10 · 부작용 항목 65 · 모든 값. 작성자가 3회 읽음(§1). 독립 검토자는 없음 |
| 구조·값 수집 | 노드 781/781 · 키 출현 613 · 문자열 628 · 중복 키 0 · 이스케이프 0 |
| 형태소·표현 수집 | Kiwi 0.24.1(cong, 스레드 1) — 분석 531값 9,697토큰 · 제외 97값(사유별) · 필드명 18 · 오분절·오태깅 표시 107출현(57규칙, **교정 아님**) · 표현 후보 5,061(수동 189 포함) |
| 기계 검증 | [validation.md](./validation.md) — verify.py failure 0, 원본 해시 시작·끝 동일, 변이 시험 검출 |
| 읽기 검토 | 작성자 3회차(미포착 어절 열람)로 수식 표지 보강. 독립 읽기 검토 아님 |
| 알려진 분석 오류 | 오분절 107출현 표시(issues A1). 표시하지 않은 토큰의 정확성은 보장하지 않음. 표현 후보의 keyword 오탐은 판정하지 않음(A2). 독립 검토가 찾은 미표시 오분절 2출현(「시술」·「전층」, 미교정)·「삽입 깊이」 구절 후보 한계·같은 구간 57쌍은 issues 「A 보충」에 위치 기록 |
| 열린 미결 | B 9 · P 4 · F 9 · C 0 — [issues.md](./issues.md) |
| 후속 의미 조사 | 시작 안 함 |

## 0. 원본과 기록 위치

| 항목 | 값 |
|---|---|
| 원본 | `orchestration/work/phub-recommend/bronze/phub-ledger/complications.json` |
| 크기 | 58,333 bytes · 33,470 code points · UTF-8 · BOM 없음 · 개행 없는 한 줄 · 이스케이프 0 · BMP 밖 문자 0 |
| sha256 | `7bf0573efa955225f63cc33d96b68a20693ddaac647ee2a0c679c1de32d3d932` (작업 시작·끝 동일) |
| 구조·값 | [source-map.json](./source-map.json) — 노드 781개(전부) · 키 출현 613개 · 필드명 출현 위치 |
| 형태소 | [morphology.json](./morphology.json) — 분석 531값 · 제외 97값 · 필드명 18 · 오분절 규칙 57·출현 107 (규칙 원본 [segmentation-review-rules.json](./segmentation-review-rules.json)) |
| 복합 표현 | [expressions.json](./expressions.json) — 후보 5,061 · 수동 구절 원본 [manual-expressions.json](./manual-expressions.json) |
| 잠정 관찰 | 이 문서 §3·§4 (원본 [manual-observations.json](./manual-observations.json), 68건) |
| 미결 · 검증 | [issues.md](./issues.md) · [validation.md](./validation.md) |
| 재현 | [build.py](./build.py)(`uv run --python 3.12 --with kiwipiepy==0.24.1 python …/build.py`) · [verify.py](./verify.py)(`python3 …/verify.py`) · [build-output.txt](./build-output.txt) |

구간 기준: 디코딩된 원문 문자열의 Unicode 코드 포인트 `[start,end)`. source-map 의 `span` 은 파일 전체 텍스트 기준이고, morphology·expressions 의 `span` 은 그 값 문자열 기준이다(파일 위치 = `file_span_of_text[0] + start`). 바이트 구간은 `byte_span` 에 따로 둔다. 이스케이프가 없어 디코딩 문자열과 JSON 리터럴 안쪽이 글자 단위로 같다(source-map `decoded_equals_literal_inner`). 따옴표 포함 리터럴 구간은 `span`, 따옴표 안쪽은 `value_span` 이다.

## 1. 읽기 범위 (실제로 한 일)

| 회차 | 범위 | 방식 |
|---|---|---|
| 1 | `/severity_levels` 4값 → `/categories/0` ~ `/categories/9` 의 id·name·complications 65항목 전 필드(빈 배열·없는 키 포함) | 카테고리 순서대로 항목별 전 필드를 출력해 위에서 아래로 직접 읽음(0~2 · 3~5 · 6~9 세 구획) |
| 2 | 같은 전체 | 값마다 다시 읽으며 조건·부정·가능성·범위·시간·참조·하위집단·근거 표지를 골라 manual-observations(68) · manual-expressions(189)에 원문 인용으로 적음. build 가 인용이 실제 값 안에 있는지 검사 |
| 3 | 분석 대상 531값 | (a) 의심 품사(NNP 일부·NR·MM·NP·MAJ·MAG 일부·VA/VV 일부·NNB 일부·붙은 SL)와 시간·부정·가능성·용어 낱말의 출현을 원문 어절과 나란히 놓고 하나씩 대조 → 오분절 규칙 57. (b) 표현 후보가 하나도 걸리지 않은 어절 2,331개를 값마다 읽음 → 빠진 수식 표지(필요시·가는·어려워·달리·우선·기존 등)를 keyword 규칙에 보강하고, 남은 어절은 사건·행위·재료·부위 같은 내용어임을 확인 |

- **자동 처리:** 구조 열거 · Pointer · 구간 · 해시 · 형태소 분석 · regex/keyword 후보 추출 · 수동 구절 위치 찾기.
- **직접 읽기:** 위 세 회차. 형태소 9천여 토큰을 하나하나 정답 대조하지는 않았다. 3(a) 범위 밖 토큰의 정확성은 보장하지 않는다.
- **한계:** 「별도 읽기 검토」는 같은 작성자가 관점을 바꿔 다시 읽은 것이다. 독립 검토자가 아니다.

## 2. 구조 — 원문 대응

### 2.1 컬럼 구성 표

최상위 객체의 키는 2개이며 순서는 `severity_levels` → `categories` 다. 숫자·불리언·null·빈 문자열·빈 객체는 없다. 빈 값은 빈 배열(`risk_factors` = [])과 기호 단독 값(`"-"`)뿐이다.

| 원본 컬럼명(경로 패턴) | JSON Pointer 패턴 | 자료형 | 중첩 구조 | 출현 | 원문 예시 | 예시 위치 |
|---|---|---|---|---|---|---|
| `(루트)` | `""`(빈 문자열 = 루트) | object | 키 2개: severity_levels, categories | 1회 | object | `""`(루트) |
| `severity_levels` | `/severity_levels` | object | 키 4개(mild, moderate, severe, critical) | 1회 | object | `/severity_levels` |
| `severity_levels.mild` | `/severity_levels/mild` | string | 스칼라 | 1회 | "경미 — 자연 소실, 경과 관찰" | `/severity_levels/mild` |
| `severity_levels.moderate` | `/severity_levels/moderate` | string | 스칼라 | 1회 | "중등도 — 치료 필요, 클리닉 방문" | `/severity_levels/moderate` |
| `severity_levels.severe` | `/severity_levels/severe` | string | 스칼라 | 1회 | "중증 — 즉시 치료, 후유증 가능" | `/severity_levels/severe` |
| `severity_levels.critical` | `/severity_levels/critical` | string | 스칼라 | 1회 | "위급 — 응급 대응, 비가역적 손상 가능" | `/severity_levels/critical` |
| `categories` | `/categories` | array | 객체 배열 | 1회 | [10개] | `/categories` |
| `categories[].id` | `/categories/\d+/id` | string | 스칼라(코드) | 10회 | "M1" | `/categories/0/id` |
| `categories[].name` | `/categories/\d+/name` | string | 스칼라 | 10회 | "보톡스" | `/categories/0/name` |
| `categories[].complications` | `/categories/\d+/complications` | array | 객체 배열 | 10회 | [7개] | `/categories/0/complications` |
| `categories[].complications[]` | `/categories/\d+/complications/\d+` | object | 부작용 항목 객체 | 65회 | object | `/categories/0/complications/0` |
| `categories[].complications[].name` | `/categories/\d+/complications/\d+/name` | string | 스칼라 | 65/65 항목 | "주사 부위 통증" | `/categories/0/complications/0/name` |
| `categories[].complications[].severity` | `/categories/\d+/complications/\d+/severity` | string | 스칼라 | 65/65 항목 | "mild" | `/categories/0/complications/0/severity` |
| `categories[].complications[].incidence` | `/categories/\d+/complications/\d+/incidence` | string | 스칼라 | 65/65 항목 | "대부분 (일시적)" | `/categories/0/complications/0/incidence` |
| `categories[].complications[].onset` | `/categories/\d+/complications/\d+/onset` | string | 스칼라 | 65/65 항목 | "시술 즉시" | `/categories/0/complications/0/onset` |
| `categories[].complications[].duration` | `/categories/\d+/complications/\d+/duration` | string | 스칼라 | 19/65 항목 | "1-3일 (자연 소실)" | `/categories/0/complications/3/duration` |
| `categories[].complications[].mechanism` | `/categories/\d+/complications/\d+/mechanism` | string | 스칼라 | 65/65 항목 | "바늘 천자 및 약액 주입에 의한 물리적 자극. 부위·용량 무관하게 모든 보톡스 주사에 공통. 손바닥/발바닥·…" | `/categories/0/complications/0/mechanism` |
| `categories[].complications[].risk_factors` | `/categories/\d+/complications/\d+/risk_factors` | array | 문자열 배열 | 65/65 항목 | [] | `/categories/0/complications/0/risk_factors` |
| `categories[].complications[].management` | `/categories/\d+/complications/\d+/management` | string | 스칼라 | 65/65 항목 | "냉각(아이스팩), 미세바늘(32G 이상) 사용, 필요시 표면마취크림. 대부분 수 분 내 소실" | `/categories/0/complications/0/management` |
| `categories[].complications[].prevention` | `/categories/\d+/complications/\d+/prevention` | string | 스칼라 | 65/65 항목 | "가는 바늘, 저속 주입, 냉각·주의분산, 통증 민감 부위는 국소마취/신경차단 고려" | `/categories/0/complications/0/prevention` |
| `categories[].complications[].evidence` | `/categories/\d+/complications/\d+/evidence` | string | 스칼라 | 38/65 항목 | "https://www.goodrx.com/botox/botox-side-effects" | `/categories/0/complications/0/evidence` |
| `categories[].complications[].risk_factors[]` | `/categories/\d+/complications/\d+/risk_factors/\d+` | string | 배열 항목 | 92회 | "이마/미간 부위 시술" | `/categories/0/complications/3/risk_factors/0` |
| `…risk_factors` (빈 배열 변형) | 〃 | array | 길이 0 | 46/65 항목 | [] | `/categories/0/complications/0/risk_factors` |
| `…risk_factors` (항목 있는 변형) | 〃 | array | 길이 4~6 | 19/65 항목 | [4개] | `/categories/0/complications/3/risk_factors` |
| `…duration` (키 없음 변형) | — | (없음) | 선택 필드 | 46/65 항목에 키 자체가 없음 | (키 없음) | 예 `/categories/0/complications/0` |
| `…evidence` (키 없음 변형) | — | (없음) | 선택 필드 | 27/65 항목에 키 자체가 없음 | (키 없음) | 예 `/categories/0/complications/3` |
| `…prevention` (기호 단독 값) | 〃 | string | 스칼라 | 1회 | "-" | `/categories/9/complications/5/prevention` |
| `…evidence` (URL만 변형) | 〃 | string | 스칼라 | 21회 | "https://www.goodrx.com/botox/botox-side-effects…" | `/categories/0/complications/0/evidence` |
| `…evidence` (설명 텍스트 포함 변형) | 〃 | string | 스칼라 | 17회 | "anatomy-danger-zones.json (internal); Complications of Derma…" | `/categories/1/complications/0/evidence` |

### 2.2 항목 객체의 키 순서 변형

필드 순서는 원문 그대로다. `duration` 은 있을 때 `onset` 바로 뒤에, `evidence` 는 있을 때 맨 끝에 온다.

| 키 수 | 키 순서(원문 그대로) | 항목 수 | 위치 |
|---|---|---|---|
| 9 | `name, severity, incidence, onset, mechanism, risk_factors, management, prevention, evidence` | 38 | `/categories/0/complications/0`, `/categories/0/complications/1`, `/categories/0/complications/2`, `/categories/0/complications/5`, `/categories/1/complications/0`, `/categories/1/complications/1`, `/categories/1/complications/2`, `/categories/1/complications/3`, `/categories/2/complications/4`, `/categories/2/complications/5`, `/categories/3/complications/6`, `/categories/3/complications/7`, `/categories/4/complications/1`, `/categories/4/complications/2`, `/categories/5/complications/1`, `/categories/5/complications/2`, `/categories/5/complications/3`, `/categories/5/complications/4`, `/categories/5/complications/5`, `/categories/6/complications/3`, `/categories/6/complications/4`, `/categories/7/complications/2`, `/categories/7/complications/3`, `/categories/7/complications/4`, `/categories/7/complications/5`, `/categories/7/complications/6`, `/categories/8/complications/0`, `/categories/8/complications/1`, `/categories/8/complications/2`, `/categories/8/complications/3`, `/categories/9/complications/0`, `/categories/9/complications/1`, `/categories/9/complications/2`, `/categories/9/complications/3`, `/categories/9/complications/4`, `/categories/9/complications/5`, `/categories/9/complications/6`, `/categories/9/complications/7` |
| 9 | `name, severity, incidence, onset, duration, mechanism, risk_factors, management, prevention` | 19 | `/categories/0/complications/3`, `/categories/0/complications/4`, `/categories/2/complications/0`, `/categories/2/complications/1`, `/categories/2/complications/2`, `/categories/2/complications/3`, `/categories/3/complications/0`, `/categories/3/complications/1`, `/categories/3/complications/2`, `/categories/3/complications/3`, `/categories/3/complications/5`, `/categories/4/complications/0`, `/categories/6/complications/0`, `/categories/6/complications/1`, `/categories/6/complications/2`, `/categories/7/complications/0`, `/categories/9/complications/8`, `/categories/9/complications/10`, `/categories/9/complications/11` |
| 8 | `name, severity, incidence, onset, mechanism, risk_factors, management, prevention` | 8 | `/categories/0/complications/6`, `/categories/1/complications/4`, `/categories/1/complications/5`, `/categories/1/complications/6`, `/categories/3/complications/4`, `/categories/5/complications/0`, `/categories/7/complications/1`, `/categories/9/complications/9` |

### 2.3 형태소 분석 적용·제외

| 대상 | 처리 | 사유 |
|---|---|---|
| `/severity_levels/*` 4 · `categories[].name` 10 · 항목 name·incidence·onset·duration·mechanism·management·prevention · risk_factors 항목 | 분석 | 언어 텍스트 |
| `categories[].id` 10 | 제외 | 코드값(M+숫자) |
| `…/severity` 65 | 제외 | 영문 열거 코드값(`/severity_levels` 키와 같은 문자열) |
| `…/evidence` 중 `; ` 조각이 전부 URL 인 값 21 | 제외 | URL 목록 |
| `…/evidence` 중 설명 텍스트가 섞인 값 17 | 분석 | 텍스트 포함. URL 부분구간은 `url_subspans` 로 따로 표시하고 그 안의 토큰은 `in_url_subspan` |
| `/categories/9/complications/5/prevention` = `"-"` 1 | 제외 | 기호 단독 값(값은 보존, issues B9) |
| 필드명 18종 | 분석(별도) | 영문 식별자. Kiwi 결과와 `_` 분할을 함께 남기며, 뜻은 정하지 않음 |

표현 후보 범주별 수: comparison_contrast 26 · condition_scope 283 · cross_reference 78 · frequency_degree 381 · latin_term 325 · manual.approx_prefix 14 · manual.causal_chain 10 · manual.condition_threshold 16 · manual.cross_reference 24 · manual.evidence_level_marker 15 · manual.frequency_degree_scoped 20 · manual.negated_statement 20 · manual.normal_reaction_statement 10 · manual.population_subgroup 11 · manual.prohibition_contraindication 11 · manual.site_mention_with_scope 11 · manual.time_window_or_sequence 27 · negation 174 · obligation_recommendation 91 · possibility_uncertainty 102 · quantity_unit_time 358 · range 73 · segment.clause 827 · segment.parenthetical 302 · segment.sentence 421 · segment.value 628 · symbol_relation 397 · time_relative 406. 범주는 탐색용 후보일 뿐 분류가 확정된 것이 아니다. 같은 구간이 여러 범주에 겹치는 것은 의도한 것이다. 표현 추출은 원문 문자열에 regex·keyword 를 직접 적용했고 형태소 품사를 쓰지 않았다. 그래서 형태소 오분절이 표현 후보로 옮겨 가지 않는다.

## 3. 전역 잠정 관찰

- **OB-T01** (구조) severity 값 65개는 전부 `/severity_levels` 의 키 4개 중 하나다(mild 38 · moderate 13 · severe 11 · critical 3). 코드 ↔ 정의의 연결은 같은 문자열이라는 구조 사실일 뿐, 각 항목에 이 정의를 적용해 등급을 매겼는지는 원문에 없다. → B1  
  근거: `/severity_levels/mild` 「경미」; `/categories/0/complications/0/severity` 「mild」
- **OB-T02** (잠정) `severity_levels` 정의 한 줄에 여러 축이 섞여 있다 — 경과(자연 소실·후유증·비가역 손상), 필요한 대응(경과 관찰·치료·응급), 장소(클리닉 방문). → B1  
  근거: `/severity_levels/moderate` 「치료 필요, 클리닉 방문」; `/severity_levels/critical` 「비가역적 손상 가능」
- **OB-T03** (구조) 항목 객체 65개는 키 7개(name·severity·incidence·onset·mechanism·management·prevention)를 모두 갖는다. `risk_factors` 도 65개 모두에 있지만 46개는 빈 배열이다. `duration` 은 19개, `evidence` 는 38개에만 있다. 키 순서 변형은 §2.2 표에 있다. → B5  
  근거: `/categories/0/complications/0/risk_factors`
- **OB-T04** (잠정) `incidence` 는 자유 서술이다. 수치(%·범위·분수), 빈도어(흔함·드묾·대부분), 조건·하위집단(부위·기법·제품·피부형·연령), 다른 분모(치료 방문의 %, MAUDE 보고 비율), 지속 기간이 한 문자열에 섞여 있다. 단위·분모·모집단 칸이 따로 없다. → B2  
  근거: `/categories/0/complications/5/incidence` 「치료 방문의 약 14%」; `/categories/6/complications/3/incidence` 「보고 비율이며 실제 발생률은 과소보고로 불명확」; `/categories/3/complications/5/incidence` 「50세 초과에서 최대 16%」
- **OB-T05** (잠정) `onset` 에 발현 시점뿐 아니라 소실·지속·교정 시점이 함께 적힌 값이 있고, `incidence`·`management` 에도 지속·소실 기간이 있다. `duration` 키는 19개 항목에만 있다. 시간의 기준점(시술 후·주입 중 등)이 생략된 값이 많다. → B3  
  근거: `/categories/0/complications/6/onset` 「2-4주 내 자연 소실 또는 보정 주사로 교정」; `/categories/6/complications/4/onset` 「24-72시간 내 대부분 소실」; `/categories/4/complications/0/onset` 「2-6주」
- **OB-T06** (원문 참조) 이 원장에 없는 대상을 가리키는 표현이 있다 — `site_specific`, 「별도 … 항목」, 「부위 특이 항목」, 다른 원장 파일명(taxonomy.json · anatomy-danger-zones.json). 참조 대상은 이 파일 안에 없다. 위치는 expressions.json 의 `manual.cross_reference` 로 모았다. → B4  
  근거: `/categories/0/complications/0/mechanism` 「site_specific에 별도 기재」; `/categories/1/complications/5/incidence` 「별도 상향 항목 참조」; `/categories/2/complications/4/evidence` 「taxonomy.json M3 각 제품 safety.common」
- **OB-T07** (잠정) `risk_factors` 가 빈 배열인 항목도 본문에서 위험을 높이는 조건을 말하는 경우가 있다. 빈 배열이 「위험인자 없음」인지 「안 적음」인지는 원문만으로 정할 수 없다. → B5  
  근거: `/categories/0/complications/1/mechanism` 「혈관이 풍부·표재한 부위(눈가 등)는 현저히 높음」; `/categories/5/complications/0/mechanism` 「골 돌출부(이마·하악연·관자)와 얇은 피부에서 열 축적으로 위험이 상대적으로 높고」
- **OB-T08** (잠정) `evidence` 의 형태가 다양하다: URL 목록, 다른 원장 파일·필드 참조, 논문·기관 문헌 이름, 「clinical-standard」「임상 표준」「임상 통설」 같은 표지. 출처가 항목 안의 어느 주장(빈도·처치 등)을 뒷받침하는지는 나와 있지 않다. 27개 항목에는 evidence 키가 없다. → B6  
  근거: `/categories/4/complications/1/evidence` 「clinical-standard: universal laser thermal response」; `/categories/9/complications/7/evidence` 「임상 표준」; `/categories/6/complications/4/evidence` 「니들RF 임상 통설」
- **OB-T09** (잠정) 기호가 여러 뜻으로 쓰인다. `~` 는 범위(「즉시~수시간」)와 근사(「~87%」, 앞이 공백)로 쓰이고, `/` 는 대안·병기(RF/HIFU)·비율(875/125mg)·횟수 단위(2회/일)·분수(1/455)로, `-` 는 수치 범위(5-10%)와 복합 약물명(아목시실린-클라불란산)으로 쓰인다. `+`·`±`·`→`·`—`·`★` 도 있다. README 의 `+`·`/` 작성 규칙이 이 원장의 기호에도 적용되는지는 확인하지 않았다. → P1  
  근거: `/categories/9/complications/0/incidence` 「~87%」; `/categories/1/complications/5/management` 「875/125mg 2회/일」; `/categories/7/complications/0/incidence` 「1/455」; `/categories/2/complications/3/management` 「★HA 필러와 달리」
- **OB-T10** (잠정) 다른 카테고리에 같거나 비슷한 이름의 사건이 다시 나온다(멍·홍반·부종·감염·PIH·비대칭·통증·감각이상 등). 이름은 같아도 severity 가 다를 수 있다 — PIH 는 M8·M9·M11 에서 moderate, M14 에서 mild 다. 같은 사건인지는 정하지 않았다. → F1  
  근거: `/categories/4/complications/0/severity` 「moderate」; `/categories/7/complications/6/severity` 「mild」; `/categories/7/complications/6/name` 「염증후 색소침착」
- **OB-T11** (잠정) 몇몇 항목은 스스로를 합병증이 아니라 「정상 반응」「예상 경과」「의도된 반응」이라고 적는다. → P2  
  근거: `/categories/5/complications/1/prevention` 「예방 대상이라기보다 예측 가능한 정상 반응」; `/categories/6/complications/4/prevention` 「합병증 아닌 정상 경과」; `/categories/8/complications/2/incidence` 「표재 필링의 의도된 반응」; `/categories/9/complications/0/mechanism` 「정상 반응」
- **OB-T12** (잠정) 항목 이름 하나에 사건 여러 개를 묶은 경우가 있다(괄호·가운뎃점·슬래시로 병기). → P3  
  근거: `/categories/2/complications/4/name` 「부종·압통·멍·홍반」; `/categories/9/complications/10/name` 「공기색전·카테터 관련 감염」; `/categories/7/complications/1/name` 「동상·지방괴사」
- **OB-T13** (잠정) `management`·`prevention` 에는 약물·용량·횟수·기간, 조건부 처치 분기(「…시」「경증/중등도」「유형별」), 금지·금기, 순서가 자유 서술로 들어 있다. 원장에 적힌 주장일 뿐이며 이 조사에서 임상적으로 검증하지 않았다. → F3  
  근거: `/categories/1/complications/4/management` 「유형별 —」; `/categories/2/complications/2/management` 「경증: 경과 관찰 + NSAID. 중등도:」
- **OB-T14** (구조) 항목 이름은 한국어만 쓴 것과 한국어+괄호 영문을 쓴 것이 섞여 있다. 괄호 안에는 영문명 말고 한정어가 들어간 경우도 있다(「기저 위험」「일반 baseline」「수포 포함」). → F1  
  근거: `/categories/1/complications/5/name` 「기저 위험」; `/categories/9/complications/9/name` 「일반 baseline」; `/categories/5/complications/0/name` 「수포 포함」
- **OB-T15** (구조) 세 필드가 겹치는 모양이 규칙적이다. `duration` 이 있는 19항목은 `risk_factors` 가 비지 않은 19항목과 정확히 같고, 이 19항목 중 `evidence` 가 있는 항목은 하나도 없다. `evidence` 가 있는 38항목은 모두 duration 이 없고 risk_factors 가 비었다. 나머지 8항목에는 셋 다 없다. 작성 시기나 방식이 다른 묶음이 섞였을 수 있다는 해석은 잠정이다(원문에 이력 없음). 빈 risk_factors 해석(B5)과 이어진다. → B5  
  근거: `/categories/0/complications/3/duration` 「1-3일」; `/categories/0/complications/0/evidence` 「goodrx」; `/categories/0/complications/6`

## 4. 항목별 값 — 원본 컬럼명 그대로

각 표는 원문 값만 담는다. 「(키 없음)」은 그 항목에 키 자체가 없다는 뜻이고, 「[] (빈 배열)」은 키는 있는데 배열이 비었다는 뜻이다. 배열 항목은 원본 순서를 지키고 행마다 Pointer 를 붙였다. 잠정 관찰은 표 아래 따로 둔다.

### severity_levels

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `mild` | `/severity_levels/mild` | 경미 — 자연 소실, 경과 관찰 |
| `moderate` | `/severity_levels/moderate` | 중등도 — 치료 필요, 클리닉 방문 |
| `severe` | `/severity_levels/severe` | 중증 — 즉시 치료, 후유증 가능 |
| `critical` | `/severity_levels/critical` | 위급 — 응급 대응, 비가역적 손상 가능 |

### `/categories/0` — id `M1` · name 「보톡스」 · complications 7개

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `id` | `/categories/0/id` | M1 |
| `name` | `/categories/0/name` | 보톡스 |

**잠정 관찰 (카테고리)**

- **OB-C00** (구조) 카테고리 id 는 M1, M2, M3, M7, M8, M9, M11, M14, M15, M16 열 개다. 번호가 이어지지 않는다. 빠진 번호의 뜻(다른 원장의 시술군 코드인지)은 이 파일에 없다. → B4  
  근거: `/categories/0/id` 「M1」; `/categories/7/id` 「M14」

#### `/categories/0/complications/0` — 주사 부위 통증

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/0/complications/0/name` | 주사 부위 통증 |
| `severity` | `/categories/0/complications/0/severity` | mild |
| `incidence` | `/categories/0/complications/0/incidence` | 대부분 (일시적) |
| `onset` | `/categories/0/complications/0/onset` | 시술 즉시 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/0/complications/0/mechanism` | 바늘 천자 및 약액 주입에 의한 물리적 자극. 부위·용량 무관하게 모든 보톡스 주사에 공통. 손바닥/발바닥·두피 등 신경분포 밀집 부위는 더 심함(부위별 강도 차이는 site_specific에 별도 기재) |
| `risk_factors` | `/categories/0/complications/0/risk_factors` | [] (빈 배열) |
| `management` | `/categories/0/complications/0/management` | 냉각(아이스팩), 미세바늘(32G 이상) 사용, 필요시 표면마취크림. 대부분 수 분 내 소실 |
| `prevention` | `/categories/0/complications/0/prevention` | 가는 바늘, 저속 주입, 냉각·주의분산, 통증 민감 부위는 국소마취/신경차단 고려 |
| `evidence` | `/categories/0/complications/0/evidence` | https://www.goodrx.com/botox/botox-side-effects |

**잠정 관찰**

- **OB-001** (원문 참조) 부위별 강도 차이를 이 원장 밖의 `site_specific` 으로 넘긴다. `32G 이상` 은 바늘 게이지 수치에 「이상」이 붙은 것으로, 굵기 방향을 원문이 풀어 쓰지 않았다. → B4  
  근거: `/categories/0/complications/0/mechanism` 「부위별 강도 차이는 site_specific에 별도 기재」; `/categories/0/complications/0/management` 「미세바늘(32G 이상)」

#### `/categories/0/complications/1` — 멍 (타박상)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/0/complications/1/name` | 멍 (타박상) |
| `severity` | `/categories/0/complications/1/severity` | mild |
| `incidence` | `/categories/0/complications/1/incidence` | 약 11-25% (부위·기법에 따라) |
| `onset` | `/categories/0/complications/1/onset` | 시술 당일 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/0/complications/1/mechanism` | 바늘이 진피/피하 소혈관을 천자하여 혈관외 출혈. 어느 부위든 발생 가능하나 혈관이 풍부·표재한 부위(눈가 등)는 현저히 높음 |
| `risk_factors` | `/categories/0/complications/1/risk_factors` | [] (빈 배열) |
| `management` | `/categories/0/complications/1/management` | 즉시 압박, 24-48시간 냉찜질 후 온찜질, 아르니카/비타민K 크림. 대부분 7-14일 내 자연 소실. 심하면 레이저(PDL/KTP) |
| `prevention` | `/categories/0/complications/1/prevention` | 시술 전 1주간 항응고·아스피린·NSAID·오메가3·비타민E·음주 자제, 표재 혈관 투과조명(vein finder), 주입 후 즉시 압박 |
| `evidence` | `/categories/0/complications/1/evidence` | https://www.goodrx.com/botox/botox-side-effects; https://www.harleyacademy.com/aesthetic-medicine-articles/periorbital-botox-how-to-treat-crows-feet/ |

**잠정 관찰**

- **OB-002** (잠정) 빈도에 조건 「부위·기법에 따라」가 붙는다. risk_factors 는 비었지만 본문에서 혈관이 많은 부위(눈가 등)가 「현저히 높음」이라고 한다. 처치는 순서가 있고(24-48시간 냉찜질 → 온찜질), 「심하면」에 걸린 조건부 처치도 있다. → F2  
  근거: `/categories/0/complications/1/incidence` 「부위·기법에 따라」; `/categories/0/complications/1/management` 「24-48시간 냉찜질 후 온찜질」; `/categories/0/complications/1/management` 「심하면 레이저(PDL/KTP)」

#### `/categories/0/complications/2` — 주사 부위 홍반·부종

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/0/complications/2/name` | 주사 부위 홍반·부종 |
| `severity` | `/categories/0/complications/2/severity` | mild |
| `incidence` | `/categories/0/complications/2/incidence` | 흔함 (일시적) |
| `onset` | `/categories/0/complications/2/onset` | 시술 직후~수 시간 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/0/complications/2/mechanism` | 주입에 대한 국소 염증/자극 반응 및 약액 볼륨에 의한 팽윤. 부위 무관 공통 반응 |
| `risk_factors` | `/categories/0/complications/2/risk_factors` | [] (빈 배열) |
| `management` | `/categories/0/complications/2/management` | 냉찜질, 대부분 수 시간~1일 내 소실. 지속·확대 시 알레르기/감염 감별 |
| `prevention` | `/categories/0/complications/2/prevention` | 무균 술기, 적정 희석·용량, 시술 후 냉각 |
| `evidence` | `/categories/0/complications/2/evidence` | https://www.medicinenet.com/side_effects_of_botox_onabotulinumtoxina/side-effects.htm |

#### `/categories/0/complications/3` — 두통

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/0/complications/3/name` | 두통 |
| `severity` | `/categories/0/complications/3/severity` | mild |
| `incidence` | `/categories/0/complications/3/incidence` | 5-10% |
| `onset` | `/categories/0/complications/3/onset` | 시술 당일~2일 |
| `duration` | `/categories/0/complications/3/duration` | 1-3일 (자연 소실) |
| `mechanism` | `/categories/0/complications/3/mechanism` | 주사 자체의 물리적 자극, 근육 장력 변화에 따른 보상성 두통, 일시적 근막 긴장 패턴 변화. 만성 편두통 환자에서는 오히려 완화 효과 |
| `risk_factors[0]` | `/categories/0/complications/3/risk_factors/0` | 이마/미간 부위 시술 |
| `risk_factors[1]` | `/categories/0/complications/3/risk_factors/1` | 다량 주입 |
| `risk_factors[2]` | `/categories/0/complications/3/risk_factors/2` | 긴장성 두통 병력 |
| `risk_factors[3]` | `/categories/0/complications/3/risk_factors/3` | 시술 중 과도한 불안 |
| `management` | `/categories/0/complications/3/management` | 아세트아미노펜(타이레놀) 500-1000mg 경구 복용. NSAID(이부프로펜) 사용 가능하나 멍 위험 증가 고려. 대부분 1-3일 내 자연 소실. 지속 시 재진 |
| `prevention` | `/categories/0/complications/3/prevention` | 시술 전 두통 병력 확인, 적정 용량 사용, 시술 중 환자 이완 유도, 시술 후 충분한 수분 섭취 안내 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-003** (잠정) 특정 환자군에서 반대 방향의 효과를 말한다(「만성 편두통 환자에서는 오히려 완화 효과」). 처치 안에 다른 사건(멍)의 위험 증가 경고가 들어 있다. → F2  
  근거: `/categories/0/complications/3/mechanism` 「만성 편두통 환자에서는 오히려 완화 효과」; `/categories/0/complications/3/management` 「멍 위험 증가 고려」

#### `/categories/0/complications/4` — 항체 내성 (면역 저항)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/0/complications/4/name` | 항체 내성 (면역 저항) |
| `severity` | `/categories/0/complications/4/severity` | moderate |
| `incidence` | `/categories/0/complications/4/incidence` | 1-3% (반복 시술 시) |
| `onset` | `/categories/0/complications/4/onset` | 수개월~수년 (누적) |
| `duration` | `/categories/0/complications/4/duration` | 수년에 걸쳐 역가 감소 가능(중단 후 흔히 3-6년 이상 소요) — 완전 영구는 아님. 임상적으로는 즉시 회복이 어려워 다른 혈청형/저단백 제형 전환이 우선 |
| `mechanism` | `/categories/0/complications/4/mechanism` | 반복 주사로 핵심 신경독소(150 kDa)에 대한 중화 항체 형성. 복합 단백질(complexing proteins)은 그 자체는 비중화 표적이지만 면역 자극 보조제로 작용해 중화 항체 생성을 촉진 — 높은 단백질 부하(protein load)일수록 위험 증가 |
| `risk_factors[0]` | `/categories/0/complications/4/risk_factors/0` | 잦은 시술 간격(3개월 미만) |
| `risk_factors[1]` | `/categories/0/complications/4/risk_factors/1` | 1회 고용량 투여(100U 이상) |
| `risk_factors[2]` | `/categories/0/complications/4/risk_factors/2` | 높은 단백질 부하 제형 사용 |
| `risk_factors[3]` | `/categories/0/complications/4/risk_factors/3` | booster 주사 반복 |
| `management` | `/categories/0/complications/4/management` | 다른 혈청형 보톡스로 전환(Type A → Type B)하거나 저단백 제형을 고려. 마이오블록(rimabotulinumtoxinB), 제오민(incobotulinumtoxinA) 시도. 중화 항체 역가 감소에는 흔히 3-6년 이상 소요될 수 있어 3-6개월 휴약만으로 회복을 기대하지 않음 |
| `prevention` | `/categories/0/complications/4/prevention` | 최소 유효 용량 사용, 시술 간격 3개월 이상 유지, 저단백질 부하 제형(제오민 등) 우선 사용, 불필요한 booster 자제, 환자에게 적정 시술 주기 교육 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-004** (잠정) `duration` 칸에 경과·부정·권고가 함께 있다(「완전 영구는 아님」, 「…전환이 우선」). management 에도 부정 기대가 있다(「휴약만으로 회복을 기대하지 않음」). risk_factors 에 수치 문턱(3개월 미만·100U 이상)이 있다. `Type A → Type B` 의 화살표는 전환 방향으로 읽힌다. → F2  
  근거: `/categories/0/complications/4/duration` 「완전 영구는 아님」; `/categories/0/complications/4/management` 「3-6개월 휴약만으로 회복을 기대하지 않음」; `/categories/0/complications/4/risk_factors/0` 「3개월 미만」; `/categories/0/complications/4/management` 「Type A → Type B」

#### `/categories/0/complications/5` — 독감 유사 증상

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/0/complications/5/name` | 독감 유사 증상 |
| `severity` | `/categories/0/complications/5/severity` | mild |
| `incidence` | `/categories/0/complications/5/incidence` | 1.7-20% (치료 방문의 약 14%) |
| `onset` | `/categories/0/complications/5/onset` | 시술 후 수일~1개월 이내 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/0/complications/5/mechanism` | 보톡스 주입 후 발생하는 일과성 전신 면역/염증 반응. 미열·근육통·피로·전신 권태감·상기도감염 유사 증상. 특정 부위와 무관한 전신 반응 |
| `risk_factors` | `/categories/0/complications/5/risk_factors` | [] (빈 배열) |
| `management` | `/categories/0/complications/5/management` | 대증치료(수분 섭취, 안정, 아세트아미노펜). 대부분 경증이며 2주 이내 자연 소실. 지속·악화 또는 호흡·연하 곤란 동반 시 의인성 보툴리즘 감별 위해 즉시 재진 |
| `prevention` | `/categories/0/complications/5/prevention` | 적정 용량 사용, 시술 후 안정 안내. 이전 시술 시 독감 유사 반응 병력 확인 |
| `evidence` | `/categories/0/complications/5/evidence` | https://pubmed.ncbi.nlm.nih.gov/23677449/; https://www.sciencedirect.com/science/article/abs/pii/S0041010111001541 |

**잠정 관찰**

- **OB-005** (잠정) 빈도가 분모가 다른 두 값이다(「1.7-20%」와 「치료 방문의 약 14%」). 처치에서는 조건이 붙으면 다른 질환 감별로 넘어간다(「호흡·연하 곤란 동반 시 의인성 보툴리즘 감별」). → B2  
  근거: `/categories/0/complications/5/incidence` 「1.7-20% (치료 방문의 약 14%)」; `/categories/0/complications/5/management` 「호흡·연하 곤란 동반 시 의인성 보툴리즘 감별 위해 즉시 재진」

#### `/categories/0/complications/6` — 안면 비대칭

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/0/complications/6/name` | 안면 비대칭 |
| `severity` | `/categories/0/complications/6/severity` | mild |
| `incidence` | `/categories/0/complications/6/incidence` | 3-8% |
| `onset` | `/categories/0/complications/6/onset` | 7-14일 (2-4주 내 자연 소실 또는 보정 주사로 교정) |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/0/complications/6/mechanism` | 좌우 근육량/활성도 차이, 주입 용량·깊이 비대칭, 기존 해부학적 비대칭의 노출. 어느 부위(이마·미간·눈가·교근 등)에서든 양측 시술 시 발생 가능한 공통 위험이므로 특정 부위에 귀속하지 않음 (미소 특이 비대칭은 입꼬리/perioral의 '비대칭 미소'로 별도 분리) |
| `risk_factors` | `/categories/0/complications/6/risk_factors` | [] (빈 배열) |
| `management` | `/categories/0/complications/6/management` | 2주 후 경과 관찰. 비대칭 확인 시 약한 쪽에 소량(2-5U) 추가 주사. 강한 쪽 재주사는 금지(과교정 위험). 환자에게 2주 이내 재주사 불필요 교육 |
| `prevention` | `/categories/0/complications/6/prevention` | 시술 전 안면 비대칭 사진 기록, 좌우 근육 활성도 개별 평가(찡그리기/눈썹 올리기), 좌우 대칭 주입점 마킹, 한 번에 과량 주입하지 않고 2주 후 터치업 계획 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-006** (원문 참조) `onset` 칸에 소실·교정 경과가 들어 있다. mechanism 은 미소 비대칭을 이 원장에 없는 다른 항목(「입꼬리/perioral의 '비대칭 미소'」)으로 나눴다고 한다. 처치에 금지(「강한 쪽 재주사는 금지」)와 기간 한정 「불필요」가 있다. → B4  
  근거: `/categories/0/complications/6/onset` 「2-4주 내 자연 소실 또는 보정 주사로 교정」; `/categories/0/complications/6/mechanism` 「입꼬리/perioral의 '비대칭 미소'로 별도 분리」; `/categories/0/complications/6/management` 「강한 쪽 재주사는 금지(과교정 위험)」

### `/categories/1` — id `M2` · name 「필러」 · complications 7개

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `id` | `/categories/1/id` | M2 |
| `name` | `/categories/1/name` | 필러 |

#### `/categories/1/complications/0` — 멍 / 반상출혈 (Bruising / Ecchymosis)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/1/complications/0/name` | 멍 / 반상출혈 (Bruising / Ecchymosis) |
| `severity` | `/categories/1/complications/0/severity` | mild |
| `incidence` | `/categories/1/complications/0/incidence` | 19-24% (필러 시술 전반, 부위·기법 무관하게 가장 흔한 부작용군) |
| `onset` | `/categories/1/complications/0/onset` | 즉시~수시간 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/1/complications/0/mechanism` | 니들/캐뉼러가 피부·피하 소혈관(정맥·모세혈관)을 천자하며 혈액이 조직으로 누출. 모든 주입 부위에서 발생하는 기계적 손상으로, 특정 부위 해부학과 무관. |
| `risk_factors` | `/categories/1/complications/0/risk_factors` | [] (빈 배열) |
| `management` | `/categories/1/complications/0/management` | 냉찜질(시술 직후 10-15분), 압박, 아르니카/비타민K 국소도포. 광범위 멍은 585-595nm PDL/IPL로 흡수 촉진. 대개 7-14일 자연 소실. |
| `prevention` | `/categories/1/complications/0/prevention` | 시술 1주 전 항응고제·항혈소판제·오메가3·비타민E·음주 중단(의학적 필요 시 처방의 상의), 캐뉼러 사용으로 혈관 천자 감소, 저속 주입, 시술 후 압박·냉찜질. |
| `evidence` | `/categories/1/complications/0/evidence` | anatomy-danger-zones.json (internal); Complications of Dermal Injectables retrospective study, PMC12817018 (2025) |

**잠정 관찰**

- **OB-007** (원문 참조) evidence 가 다른 원장(anatomy-danger-zones.json)과 문헌을 함께 가리킨다. prevention 의 중단 권고에 예외 조건이 붙어 있다(「의학적 필요 시 처방의 상의」). → B4  
  근거: `/categories/1/complications/0/evidence` 「anatomy-danger-zones.json (internal)」; `/categories/1/complications/0/prevention` 「의학적 필요 시 처방의 상의」

#### `/categories/1/complications/1` — 부종 / 종창 (Swelling / Edema)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/1/complications/1/name` | 부종 / 종창 (Swelling / Edema) |
| `severity` | `/categories/1/complications/1/severity` | mild |
| `incidence` | `/categories/1/complications/1/incidence` | 매우 흔함 (사실상 전 사례에서 경도 발생, 수일 내 소실) |
| `onset` | `/categories/1/complications/1/onset` | 즉시~48시간 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/1/complications/1/mechanism` | 주입 자체의 기계적 조직 확장 + 국소 염증반응 + HA의 친수성으로 인한 수분 유입. 모든 부위 공통이나, 눈밑·입술처럼 조직이 성긴 부위에서는 과다 부종으로 별도 부위특이 항목화(site_specific 참조). |
| `risk_factors` | `/categories/1/complications/1/risk_factors` | [] (빈 배열) |
| `management` | `/categories/1/complications/1/management` | 냉찜질, 두부거상 수면, 저염식. 경도는 3-5일 내 자연 소실. 과도하거나 지연 시 알레르기/염증반응 감별. |
| `prevention` | `/categories/1/complications/1/prevention` | 소량 분산 주입, 과교정 회피, 시술 후 24-48시간 열노출(사우나·격한 운동·음주) 자제. |
| `evidence` | `/categories/1/complications/1/evidence` | anatomy-danger-zones.json (internal) |

**잠정 관찰**

- **OB-008** (원문 참조) 빈도 칸에 정도(「경도」)와 소실 기간이 함께 있다. 눈밑·입술의 과다 부종은 `site_specific` 으로 넘긴다. → B4  
  근거: `/categories/1/complications/1/incidence` 「사실상 전 사례에서 경도 발생, 수일 내 소실」; `/categories/1/complications/1/mechanism` 「별도 부위특이 항목화(site_specific 참조)」

#### `/categories/1/complications/2` — 주사 통증 / 불편감 (Injection Pain / Discomfort)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/1/complications/2/name` | 주사 통증 / 불편감 (Injection Pain / Discomfort) |
| `severity` | `/categories/1/complications/2/severity` | mild |
| `incidence` | `/categories/1/complications/2/incidence` | 흔함 (일시적) |
| `onset` | `/categories/1/complications/2/onset` | 즉시 (주입 중~직후) |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/1/complications/2/mechanism` | 니들/캐뉼러의 조직 관통과 필러 볼륨 주입에 따른 압력·신전 자극. 모든 주입 부위 공통이며 리도카인 함유 필러·국소마취로 완화 가능. |
| `risk_factors` | `/categories/1/complications/2/risk_factors` | [] (빈 배열) |
| `management` | `/categories/1/complications/2/management` | 국소마취 크림(EMLA 등) 선처치, 리도카인 함유 필러 사용, 냉각·진동자극(gate control). 대개 시술 종료 후 수시간 내 소실. |
| `prevention` | `/categories/1/complications/2/prevention` | 리도카인 함유 제품 선택, 마취 선처치, 느린 주입, 세밀한 니들 게이지. |
| `evidence` | `/categories/1/complications/2/evidence` | anatomy-danger-zones.json (internal) |

#### `/categories/1/complications/3` — 홍반 (Erythema / Redness)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/1/complications/3/name` | 홍반 (Erythema / Redness) |
| `severity` | `/categories/1/complications/3/severity` | mild |
| `incidence` | `/categories/1/complications/3/incidence` | 흔함 (일시적, 수시간~수일) |
| `onset` | `/categories/1/complications/3/onset` | 즉시~수시간 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/1/complications/3/mechanism` | 주입 외상에 대한 국소 혈관확장·염증반응. 부위 무관하게 발생하며 대개 자가 소실. 지속·확대되는 홍반은 감염/과민반응/바이오필름 감별 필요. |
| `risk_factors` | `/categories/1/complications/3/risk_factors` | [] (빈 배열) |
| `management` | `/categories/1/complications/3/management` | 냉찜질, 관찰. 48시간 이상 지속·확대 시 감염·지연염증반응 평가. |
| `prevention` | `/categories/1/complications/3/prevention` | 무균 술기, 과도한 조작 최소화. |
| `evidence` | `/categories/1/complications/3/evidence` | anatomy-danger-zones.json (internal) |

**잠정 관찰**

- **OB-009** (잠정) 처치 분기에 지속 시간 문턱이 있다(「48시간 이상 지속·확대 시」). → F3  
  근거: `/categories/1/complications/3/management` 「48시간 이상 지속·확대 시」

#### `/categories/1/complications/4` — 육아종 / 지연성 염증성 결절 (Granuloma / Delayed Inflammatory Nodule)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/1/complications/4/name` | 육아종 / 지연성 염증성 결절 (Granuloma / Delayed Inflammatory Nodule) |
| `severity` | `/categories/1/complications/4/severity` | moderate |
| `incidence` | `/categories/1/complications/4/incidence` | 0.1-1% |
| `onset` | `/categories/1/complications/4/onset` | 수주~수년 (지연성). 평균 지연 합병증 발현 약 16.8개월 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/1/complications/4/mechanism` | 필러에 대한 이물반응·면역 매개 반응. 핵심 트리거가 전신적(바이러스 감염, 인플루엔자 유사 질환, COVID 백신 접종, 치과 시술)이어서 여러 필러 주입 부위에 동시다발로 나타나는 특성 → 부위 특이가 아닌 공통. HA 분해산물·불순물·바이오필름도 관여. 유형: (1) 비감염성 이물 육아종, (2) 감염성/바이오필름 관련, (3) 과민반응성. |
| `risk_factors` | `/categories/1/complications/4/risk_factors` | [] (빈 배열) |
| `management` | `/categories/1/complications/4/management` | 유형별 — (1) 비감염성: 트리암시놀론 10-40mg/mL 병변내 주사 4주 간격 ± 5-FU 혼합. (2) 감염성/바이오필름 의심: 클래리스로마이신 500mg 2회/일 + 시프로플록사신 500mg 2회/일 4-6주, 농양 시 절개배농. (3) HA 필러: 히알루로니다아제 용해. 비HA 필러: 수술적 제거 고려. |
| `prevention` | `/categories/1/complications/4/prevention` | 검증 제품·무균 술기, 과량 주입 자제, 시술 전 면역 상태·최근 백신/감염력 확인, 치과 시술 전후 2주 간격, 정기 추적. |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-010** (잠정) mechanism 의 유형 번호와 management 의 번호가 서로 다른 대상을 가리킨다. mechanism (3) 은 「과민반응성」, management (3) 은 「HA 필러」다. onset 의 「평균 지연 합병증 발현 약 16.8개월」이 이 사건만의 평균인지, 지연 합병증 전체의 평균인지 원문으로 정할 수 없다. → B8  
  근거: `/categories/1/complications/4/mechanism` 「(3) 과민반응성」; `/categories/1/complications/4/management` 「(3) HA 필러」; `/categories/1/complications/4/onset` 「평균 지연 합병증 발현 약 16.8개월」

#### `/categories/1/complications/5` — 감염 (Infection, 기저 위험)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/1/complications/5/name` | 감염 (Infection, 기저 위험) |
| `severity` | `/categories/1/complications/5/severity` | severe |
| `incidence` | `/categories/1/complications/5/incidence` | 0.5-2% (전 부위 기저 위험. 입술 등 점막 인접 부위는 별도 상향 항목 참조) |
| `onset` | `/categories/1/complications/5/onset` | 수일~수주 (급성), 수개월 (지연성/바이오필름) |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/1/complications/5/mechanism` | 주입 시 세균 오염, 혈행성 파급, 필러 표면 바이오필름. 어느 주입 부위든 피부 장벽을 뚫으므로 기저 감염 위험은 공통. 급성: S. aureus, Streptococcus. 지연성: NTM·바이오필름. |
| `risk_factors` | `/categories/1/complications/5/risk_factors` | [] (빈 배열) |
| `management` | `/categories/1/complications/5/management` | 급성: 아목시실린-클라불란산 875/125mg 2회/일 또는 세팔렉신 500mg 4회/일 7-14일. 농양: 절개배농 + 배양. 바이오필름 의심: 클래리스로마이신 + 시프로플록사신 4-6주. HA: 히알루로니다아제 용해 고려. |
| `prevention` | `/categories/1/complications/5/prevention` | 무균 술기(클로르헥시딘 소독), 시술 부위 기존 감염 완치 후 시술, 재시술 부위 주의, 치과 시술 전후 간격 유지. |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-011** (원문 참조) 이름의 「기저 위험」과 incidence 의 「전 부위 기저 위험」은 이 항목이 기본값이고, 부위별 상향 항목이 따로 있다는 뜻으로 읽힌다(잠정). 상향 항목은 이 파일에 없다. onset 은 급성과 지연성 두 갈래다. → B4  
  근거: `/categories/1/complications/5/incidence` 「입술 등 점막 인접 부위는 별도 상향 항목 참조」; `/categories/1/complications/5/onset` 「수개월 (지연성/바이오필름)」

#### `/categories/1/complications/6` — 비대칭 (Asymmetry)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/1/complications/6/name` | 비대칭 (Asymmetry) |
| `severity` | `/categories/1/complications/6/severity` | mild |
| `incidence` | `/categories/1/complications/6/incidence` | 5-10% |
| `onset` | `/categories/1/complications/6/onset` | 즉시~2주 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/1/complications/6/mechanism` | 좌우 불균일한 주입량/깊이, 기존 해부학적 비대칭 노출, 부종의 비대칭 소실, 이차적 필러 이동. 볼륨을 넣는 모든 부위에서 발생 가능한 공통 술기 의존적 부작용. |
| `risk_factors` | `/categories/1/complications/6/risk_factors` | [] (빈 배열) |
| `management` | `/categories/1/complications/6/management` | 2주 후 부종 소실 시점 재평가. 부족한 쪽 소량 touch-up, 과교정 쪽은 히알루로니다아제 부분 용해. 전후 사진 비교. |
| `prevention` | `/categories/1/complications/6/prevention` | 시술 전 정면/좌우 45도 사진, 기존 비대칭 사전 고지, 거울·사진 확인하며 소량 분산 주입, 2주 후 터치업 계획. |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-012** (잠정) mechanism 이 다른 사건(「이차적 필러 이동」)을 원인으로 든다. → F1  
  근거: `/categories/1/complications/6/mechanism` 「이차적 필러 이동」

### `/categories/2` — id `M3` · name 「바이오스티뮬레이터/콜라겐부스터」 · complications 6개

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `id` | `/categories/2/id` | M3 |
| `name` | `/categories/2/name` | 바이오스티뮬레이터/콜라겐부스터 |

#### `/categories/2/complications/0` — 결절 (Nodule)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/2/complications/0/name` | 결절 (Nodule) |
| `severity` | `/categories/2/complications/0/severity` | moderate |
| `incidence` | `/categories/2/complications/0/incidence` | 5-10% (PLLA), 2-5% (CaHA) |
| `onset` | `/categories/2/complications/0/onset` | 수주~수개월 |
| `duration` | `/categories/2/complications/0/duration` | 수개월~영구적 (치료 필요) |
| `mechanism` | `/categories/2/complications/0/mechanism` | 불충분한 희석, 얕은 주입, 부적절한 시술 후 마사지로 인한 바이오스티뮬레이터 입자의 불균일 분포. PLLA 미세결정이 국소 집적되어 촉진 가능한 결절 형성 |
| `risk_factors[0]` | `/categories/2/complications/0/risk_factors/0` | 불충분한 희석(PLLA: 8mL 미만) |
| `risk_factors[1]` | `/categories/2/complications/0/risk_factors/1` | 얕은 주입(진피 내) |
| `risk_factors[2]` | `/categories/2/complications/0/risk_factors/2` | 시술 후 마사지 미시행 |
| `risk_factors[3]` | `/categories/2/complications/0/risk_factors/3` | 입술/눈 주위 얇은 피부에 주입 |
| `risk_factors[4]` | `/categories/2/complications/0/risk_factors/4` | PLLA 재구성 시 라벨 기준보다 불충분한 수화 |
| `management` | `/categories/2/complications/0/management` | 촉진 가능 결절: 생리식염수/희석액 고희석 후 마사지로 분산. 지속성 CaHA 결절: 병변 내 트리암시놀론±5-FU, 필요 시 에너지기기(RF/미세바늘)·기계적 진동을 적용하는 2024 ASJ 구조적 접근법 고려. 티오황산나트륨(STS)은 근거가 제한적이고 효능 논란·괴사/출혈 위험 및 통제된 근거 부족으로 1차 옵션으로 권고하지 않음. 불응성은 수술적 절제 고려 |
| `prevention` | `/categories/2/complications/0/prevention` | PLLA: 적정 희석량(안면 8mL SWFI 이상, 필요 시 리도카인 추가)과 최소 라벨 기준 수화(부족 시 결절 위험), 균질 혼합, 심부(피하지방층/골막 상방) 분산 주입이 결절 예방의 핵심이며 24시간 이상 수화가 필수인 것은 아님. CaHA: 적절한 희석 비율. 얇은 피부 부위(입술, 눈꺼풀) 주입 금지. |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-013** (잠정) 빈도가 제품별로 둘이다(PLLA·CaHA). risk_factors 의 「입술/눈 주위 얇은 피부」와 prevention 의 「얇은 피부 부위(입술, 눈꺼풀) 주입 금지」는 부위 표현이 다르다(눈 주위 ↔ 눈꺼풀). 부정 진술 두 개를 보존한다(「1차 옵션으로 권고하지 않음」, 「24시간 이상 수화가 필수인 것은 아님」). 처치 문장 안에 문헌 언급(「2024 ASJ 구조적 접근법」)이 있다. → F6  
  근거: `/categories/2/complications/0/incidence` 「5-10% (PLLA), 2-5% (CaHA)」; `/categories/2/complications/0/risk_factors/3` 「입술/눈 주위 얇은 피부에 주입」; `/categories/2/complications/0/prevention` 「얇은 피부 부위(입술, 눈꺼풀) 주입 금지」; `/categories/2/complications/0/management` 「1차 옵션으로 권고하지 않음」; `/categories/2/complications/0/prevention` 「24시간 이상 수화가 필수인 것은 아님」

#### `/categories/2/complications/1` — 육아종 (Granuloma)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/2/complications/1/name` | 육아종 (Granuloma) |
| `severity` | `/categories/2/complications/1/severity` | severe |
| `incidence` | `/categories/2/complications/1/incidence` | 0.5-2% |
| `onset` | `/categories/2/complications/1/onset` | 수개월~수년 (지연성) |
| `duration` | `/categories/2/complications/1/duration` | 수개월~영구적 (적극적 치료 필요) |
| `mechanism` | `/categories/2/complications/1/mechanism` | 바이오스티뮬레이터 입자에 대한 과도한 이물반응(foreign body giant cell reaction). 만성 염증 → 상피양 세포·거대세포 집적 → 육아종 형성. 면역 변화(감염, 예방접종, 스트레스) 시 지연 발현 |
| `risk_factors[0]` | `/categories/2/complications/1/risk_factors/0` | 이물반응 병력 |
| `risk_factors[1]` | `/categories/2/complications/1/risk_factors/1` | 자가면역 질환 |
| `risk_factors[2]` | `/categories/2/complications/1/risk_factors/2` | 면역 상태 변화(감염, 예방접종 후) |
| `risk_factors[3]` | `/categories/2/complications/1/risk_factors/3` | 과량 주입 |
| `risk_factors[4]` | `/categories/2/complications/1/risk_factors/4` | 반복 시술 |
| `management` | `/categories/2/complications/1/management` | 트리암시놀론 20-40mg/mL + 5-FU(50mg/mL) 혼합 병변 내 주사, 4주 간격 3-5회. 항생제 병합(바이오필름 가능성): 클래리스로마이신 500mg 2회/일 4-6주. 미노사이클린 100mg/일 추가 고려. CaHA 국소 집적은 생리식염수/희석액 고희석 후 마사지, 병변 내 트리암시놀론±5-FU, 필요 시 RF/미세바늘·기계적 진동을 고려. STS는 근거 제한적·효능 논란·괴사/출혈 위험과 통제된 근거 부족으로 1차 옵션에서 제외. 불응성은 수술적 제거 |
| `prevention` | `/categories/2/complications/1/prevention` | 이물반응/육아종 병력 환자 시술 금지, 적정 용량·적절한 희석, 시술 전 면역 상태 평가, 예방접종 전후 2주 시술 자제, 정기 추적 관찰(6개월/1년) |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-014** (잠정) 육아종 처치 안에 CaHA 국소 집적(결절 항목 `/categories/2/complications/0` 의 처치와 비슷한 문구)이 들어 있다. 횟수와 간격이 있다(「4주 간격 3-5회」). prevention 에 시술 금지 대상과 기간 조건이 있다. → F3  
  근거: `/categories/2/complications/1/management` 「CaHA 국소 집적은」; `/categories/2/complications/1/management` 「4주 간격 3-5회」; `/categories/2/complications/1/prevention` 「이물반응/육아종 병력 환자 시술 금지」; `/categories/2/complications/1/prevention` 「예방접종 전후 2주 시술 자제」

#### `/categories/2/complications/2` — 이물반응 (Foreign Body Reaction)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/2/complications/2/name` | 이물반응 (Foreign Body Reaction) |
| `severity` | `/categories/2/complications/2/severity` | moderate |
| `incidence` | `/categories/2/complications/2/incidence` | 2-5% |
| `onset` | `/categories/2/complications/2/onset` | 수주~수개월 |
| `duration` | `/categories/2/complications/2/duration` | 수주~수개월 (자연 소실 또는 치료 필요) |
| `mechanism` | `/categories/2/complications/2/mechanism` | 바이오스티뮬레이터 입자를 이물질로 인식한 면역 반응. 대식세포·거대세포 활성화, 국소 염증 반응. 육아종보다 경미한 형태의 염증성 이물반응 |
| `risk_factors[0]` | `/categories/2/complications/2/risk_factors/0` | 면역 반응 민감 체질 |
| `risk_factors[1]` | `/categories/2/complications/2/risk_factors/1` | 과량 주입 |
| `risk_factors[2]` | `/categories/2/complications/2/risk_factors/2` | 얕은 주입층 |
| `risk_factors[3]` | `/categories/2/complications/2/risk_factors/3` | 면역 상태 변화 |
| `management` | `/categories/2/complications/2/management` | 경증: 경과 관찰 + NSAID. 중등도: 경구 프레드니솔론 20-30mg 단기 투여(1-2주 감량). 국소: 트리암시놀론 10mg/mL 병변 내 주사. 지속 시 항생제 추가(바이오필름 배제) |
| `prevention` | `/categories/2/complications/2/prevention` | 적절한 희석 및 주입 깊이, 면역 민감 체질 사전 확인, 시술 부위 무균 유지, 소량씩 분산 주입, 시술 후 마사지 철저 시행 |
| `evidence` | — | (키 없음) |

#### `/categories/2/complications/3` — 혈관폐색/색전 (Vascular Occlusion/Embolism)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/2/complications/3/name` | 혈관폐색/색전 (Vascular Occlusion/Embolism) |
| `severity` | `/categories/2/complications/3/severity` | critical |
| `incidence` | `/categories/2/complications/3/incidence` | 드물지만 피부괴사·실명 등 비가역적 손상 가능 |
| `onset` | `/categories/2/complications/3/onset` | 즉시~수시간 |
| `duration` | `/categories/2/complications/3/duration` | 비가역적 가능 — 즉시 응급 대응 필요 |
| `mechanism` | `/categories/2/complications/3/mechanism` | CaHA/PLLA를 혈관 내 또는 혈관 주변에 볼루스로 주입하여 동맥 색전·혈류 차단 발생. HA 필러와 달리 CaHA/PLLA에는 용해 역전제가 없고 hyaluronidase가 무효 |
| `risk_factors[0]` | `/categories/2/complications/3/risk_factors/0` | 미간·비배부·측두부 등 고위험 부위 |
| `risk_factors[1]` | `/categories/2/complications/3/risk_factors/1` | 고압·대량 볼루스 주입 |
| `risk_factors[2]` | `/categories/2/complications/3/risk_factors/2` | 니들 사용 |
| `risk_factors[3]` | `/categories/2/complications/3/risk_factors/3` | 역행성 주입 |
| `risk_factors[4]` | `/categories/2/complications/3/risk_factors/4` | 해부학적 혈관 변이 |
| `management` | `/categories/2/complications/3/management` | 즉시 시술 중단·응급 전원. 실명 의심 시 즉시 망막안과/응급실 이송, 안구마사지·안압강하 등 응급조치 및 안과 전문의의 전방천자 고려. ★HA 필러와 달리 hyaluronidase는 무효이며 CaHA/PLLA는 용해 역전제가 없음 |
| `prevention` | `/categories/2/complications/3/prevention` | 흡인은 음성 결과가 안전을 보장하지 않는 보조 수단으로만 사용하고, 미세캐뉼라·소량 후진 주입·저압 주입을 적용하며 고위험 부위 심부 볼루스를 회피 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-015** (잠정) `incidence` 칸에 수치가 없고 결과의 심각도(「피부괴사·실명 등 비가역적 손상 가능」)를 적었다. `duration` 칸에는 기간 대신 대응(「즉시 응급 대응 필요」)이 있다. prevention 에는 보조 수단의 한계를 적은 부정문이 있다. → B2  
  근거: `/categories/2/complications/3/incidence` 「드물지만 피부괴사·실명 등 비가역적 손상 가능」; `/categories/2/complications/3/duration` 「즉시 응급 대응 필요」; `/categories/2/complications/3/prevention` 「음성 결과가 안전을 보장하지 않는 보조 수단으로만」

#### `/categories/2/complications/4` — 주사 부위 반응 (부종·압통·멍·홍반)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/2/complications/4/name` | 주사 부위 반응 (부종·압통·멍·홍반) |
| `severity` | `/categories/2/complications/4/severity` | mild |
| `incidence` | `/categories/2/complications/4/incidence` | 대부분(일시적) — 각 제품 안전정보의 최빈 공통 항목 |
| `onset` | `/categories/2/complications/4/onset` | 즉시~수일 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/2/complications/4/mechanism` | 바늘/캐뉼라 삽입에 따른 기계적 조직 손상, 미세혈관 파열(멍), 주입액에 대한 초기 국소 염증·부종. 모든 주입 시술의 공통 초기 반응 |
| `risk_factors` | `/categories/2/complications/4/risk_factors` | [] (빈 배열) |
| `management` | `/categories/2/complications/4/management` | 냉찜질, 대증요법. 멍은 아르니카/레이저(PDL) 고려, 부종은 수일 내 자연 소실. 지속·악화 시 결절·감염 감별 |
| `prevention` | `/categories/2/complications/4/prevention` | 미세 바늘/캐뉼라 사용, 소량 분산 주입, 시술 전 항응고제·NSAID·오메가3·음주 회피, 시술 후 냉찜질 |
| `evidence` | `/categories/2/complications/4/evidence` | taxonomy.json M3 각 제품 safety.common (부종/압통/멍/홍반 반복 등장); Galderma Sculptra IFU |

**잠정 관찰**

- **OB-016** (원문 참조) evidence 가 다른 원장의 필드(「taxonomy.json M3 각 제품 safety.common」)와 제품 IFU 를 가리킨다. → B4  
  근거: `/categories/2/complications/4/evidence` 「taxonomy.json M3 각 제품 safety.common」; `/categories/2/complications/4/evidence` 「Galderma Sculptra IFU」

#### `/categories/2/complications/5` — 감염 및 바이오필름 (Infection / Biofilm)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/2/complications/5/name` | 감염 및 바이오필름 (Infection / Biofilm) |
| `severity` | `/categories/2/complications/5/severity` | severe |
| `incidence` | `/categories/2/complications/5/incidence` | <1% (급성), 지연성 바이오필름은 드물지만 지연 결절·육아종의 원인 |
| `onset` | `/categories/2/complications/5/onset` | 급성: 수일. 바이오필름: 수주~수개월(지연) |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/2/complications/5/mechanism` | 주입 과정 세균 오염 → 급성: 국소 농양/봉와직염. 지연성: 저강도 세균 바이오필름이 입자 표면에 형성되어 만성 염증·지연 결절/육아종을 유발(스테로이드 단독 시 악화). 모든 주입 부위에서 발생 가능한 공통 위험 |
| `risk_factors` | `/categories/2/complications/5/risk_factors` | [] (빈 배열) |
| `management` | `/categories/2/complications/5/management` | 배양 후 경험적 항생제(퀴놀론 + 마크로라이드 조합으로 바이오필름 커버), 농양은 절개배농. ★감염/바이오필름 의심 시 스테로이드 단독 주사 금지(악화). 불응성은 병변 제거 |
| `prevention` | `/categories/2/complications/5/prevention` | 엄격한 무균술, 시술 전 활동성 피부·치과·부비동 감염 배제, 메이크업 제거·소독, 최근 감염/항생제 치료력 확인 |
| `evidence` | `/categories/2/complications/5/evidence` | onlinelibrary.wiley.com/doi/10.1111/jocd.16343 (biostimulator complications, biofilm 관련); PubMed 28247924 (CaHA safety review — biofilm/infection) |

**잠정 관찰**

- **OB-017** (잠정) incidence 가 다른 항목의 원인이 된다고 적는다(「지연 결절·육아종의 원인」 → 같은 카테고리의 결절·육아종 항목). 금지와 그 이유가 짝으로 나온다(「스테로이드 단독 주사 금지(악화)」). → F1  
  근거: `/categories/2/complications/5/incidence` 「지연 결절·육아종의 원인」; `/categories/2/complications/5/management` 「스테로이드 단독 주사 금지(악화)」

### `/categories/3` — id `M7` · name 「실리프팅」 · complications 8개

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `id` | `/categories/3/id` | M7 |
| `name` | `/categories/3/name` | 실리프팅 |

#### `/categories/3/complications/0` — 실 노출 (Thread Exposure)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/3/complications/0/name` | 실 노출 (Thread Exposure) |
| `severity` | `/categories/3/complications/0/severity` | moderate |
| `incidence` | `/categories/3/complications/0/incidence` | 1-3% |
| `onset` | `/categories/3/complications/0/onset` | 수일~수주 |
| `duration` | `/categories/3/complications/0/duration` | 제거 시까지 지속 |
| `mechanism` | `/categories/3/complications/0/mechanism` | 실이 얕은 층에 거치되거나 삽입점 봉합 불량으로 실 끝이 피부 밖으로 돌출. 얇은 피부, 과도한 텐션, 감염에 의한 이차적 노출 |
| `risk_factors[0]` | `/categories/3/complications/0/risk_factors/0` | 얇은 피부 부위 시술 |
| `risk_factors[1]` | `/categories/3/complications/0/risk_factors/1` | 얕은 삽입층 |
| `risk_factors[2]` | `/categories/3/complications/0/risk_factors/2` | 과도한 리프팅 텐션 |
| `risk_factors[3]` | `/categories/3/complications/0/risk_factors/3` | 삽입점 봉합 불량 |
| `risk_factors[4]` | `/categories/3/complications/0/risk_factors/4` | 감염 |
| `management` | `/categories/3/complications/0/management` | 노출 부위 무균 처치. 소독 후 노출된 실 끝을 피부 아래로 재매몰 시도. 불가능 시 노출 부분 절단 또는 실 제거. 감염 동반 시 항생제 투여 + 실 제거. 제거 후 2차 감염 예방 |
| `prevention` | `/categories/3/complications/0/prevention` | 적절한 삽입 깊이(피하지방층~SMAS), 적정 텐션 유지, 삽입점 정확한 봉합, 얇은 피부 부위 시술 시 주의, 시술 후 과도한 안면 운동 자제 교육 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-018** (잠정) `duration` 의 끝이 시간이 아니라 사건으로 정해진다(「제거 시까지 지속」). management 는 조건에 따라 단계가 나뉜다(재매몰 시도 → 불가능 시 절단·제거 → 감염 동반 시 항생제+제거). → F3  
  근거: `/categories/3/complications/0/duration` 「제거 시까지 지속」; `/categories/3/complications/0/management` 「불가능 시 노출 부분 절단 또는 실 제거」

#### `/categories/3/complications/1` — 실 이동 (Thread Migration)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/3/complications/1/name` | 실 이동 (Thread Migration) |
| `severity` | `/categories/3/complications/1/severity` | moderate |
| `incidence` | `/categories/3/complications/1/incidence` | 2-5% |
| `onset` | `/categories/3/complications/1/onset` | 수주~수개월 |
| `duration` | `/categories/3/complications/1/duration` | 재시술 또는 제거 시까지 |
| `mechanism` | `/categories/3/complications/1/mechanism` | 실의 고정점(cog/barb)이 조직에 충분히 앵커링되지 않아 중력/근육 운동에 의해 이동. 부적절한 벡터 설계, 불충분한 cog 거치 |
| `risk_factors[0]` | `/categories/3/complications/1/risk_factors/0` | 부적절한 실 종류 선택 |
| `risk_factors[1]` | `/categories/3/complications/1/risk_factors/1` | 불충분한 cog 거치 |
| `risk_factors[2]` | `/categories/3/complications/1/risk_factors/2` | 과도한 안면 운동(시술 초기) |
| `risk_factors[3]` | `/categories/3/complications/1/risk_factors/3` | 리프팅 벡터 설계 오류 |
| `risk_factors[4]` | `/categories/3/complications/1/risk_factors/4` | 조직 이완이 심한 경우 |
| `management` | `/categories/3/complications/1/management` | 경미한 이동: 경과 관찰(실 흡수 시까지). 미용적 문제: 추가 실 삽입으로 보정 또는 이동된 실 제거. 촉진 가능 시 국소 마취 하 실 제거 |
| `prevention` | `/categories/3/complications/1/prevention` | 적절한 실 종류·길이 선택, 정확한 리프팅 벡터 설계, 충분한 cog 거치 확인, 시술 후 3-4주 격렬한 안면 운동·마사지·치과 시술 자제, 조직 이완 정도에 맞는 실 수 결정 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-019** (잠정) 경과 관찰의 끝도 사건으로 정해진다(「실 흡수 시까지」). prevention 에 시술 뒤 기간 제한이 있다(「시술 후 3-4주」). → F3  
  근거: `/categories/3/complications/1/management` 「경과 관찰(실 흡수 시까지)」; `/categories/3/complications/1/prevention` 「시술 후 3-4주 격렬한 안면 운동·마사지·치과 시술 자제」

#### `/categories/3/complications/2` — 감염

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/3/complications/2/name` | 감염 |
| `severity` | `/categories/3/complications/2/severity` | severe |
| `incidence` | `/categories/3/complications/2/incidence` | 0.5-2% |
| `onset` | `/categories/3/complications/2/onset` | 수일~수주 |
| `duration` | `/categories/3/complications/2/duration` | 치료 기간에 따라 다름 (2-6주) |
| `mechanism` | `/categories/3/complications/2/mechanism` | 시술 중 세균 오염, 비무균 환경, 구강 내 세균의 혈행성 파급. 실 표면에 바이오필름 형성 시 만성 감염으로 이행 |
| `risk_factors[0]` | `/categories/3/complications/2/risk_factors/0` | 비무균 시술 환경 |
| `risk_factors[1]` | `/categories/3/complications/2/risk_factors/1` | 시술 부위 기존 감염 |
| `risk_factors[2]` | `/categories/3/complications/2/risk_factors/2` | 면역저하 |
| `risk_factors[3]` | `/categories/3/complications/2/risk_factors/3` | 구강 위생 불량 |
| `risk_factors[4]` | `/categories/3/complications/2/risk_factors/4` | 시술 직후 치과 시술 |
| `management` | `/categories/3/complications/2/management` | 경험적 항생제(아목시실린-클라불란산 875/125mg 2회/일) 7-14일. 배양검사 시행. 농양 형성 시 절개배농. 항생제 불응 시 실 제거 필수. 바이오필름 의심 시 장기 항생제(클래리스로마이신 + 시프로플록사신 4-6주) |
| `prevention` | `/categories/3/complications/2/prevention` | 무균 술기 철저, 시술 부위 클로르헥시딘 소독, 시술 전 구강 위생 확인, 시술 전후 2주 치과 시술 자제, 예방적 항생제 투여 고려(고위험군) |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-020** (잠정) duration 이 치료에 따라 달라진다고 한다(「치료 기간에 따라 다름 (2-6주)」). prevention 의 예방적 항생제는 대상 조건(고위험군)이 붙은 「고려」다. → F2  
  근거: `/categories/3/complications/2/duration` 「치료 기간에 따라 다름 (2-6주)」; `/categories/3/complications/2/prevention` 「예방적 항생제 투여 고려(고위험군)」

#### `/categories/3/complications/3` — 비대칭

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/3/complications/3/name` | 비대칭 |
| `severity` | `/categories/3/complications/3/severity` | mild |
| `incidence` | `/categories/3/complications/3/incidence` | 5-10% |
| `onset` | `/categories/3/complications/3/onset` | 즉시~2주 |
| `duration` | `/categories/3/complications/3/duration` | 자연 교정(4-8주) 또는 재시술 필요 |
| `mechanism` | `/categories/3/complications/3/mechanism` | 좌우 불균형한 실 배치, 텐션 차이, 편측 부종, 기존 해부학적 비대칭의 노출 |
| `risk_factors[0]` | `/categories/3/complications/3/risk_factors/0` | 기존 안면 비대칭 |
| `risk_factors[1]` | `/categories/3/complications/3/risk_factors/1` | 좌우 불균형 실 배치 |
| `risk_factors[2]` | `/categories/3/complications/3/risk_factors/2` | 편측 부종 |
| `risk_factors[3]` | `/categories/3/complications/3/risk_factors/3` | 한쪽 실 조기 이완 |
| `management` | `/categories/3/complications/3/management` | 2-4주 경과 관찰(부종 소실 후 재평가). 지속적 비대칭: 부족한 쪽 추가 실 삽입 또는 과교정 쪽 실 텐션 조절. 시술 전후 사진 비교 |
| `prevention` | `/categories/3/complications/3/prevention` | 시술 전 안면 비대칭 사진 기록·고지, 좌우 대칭 마킹, 동일 수량·동일 벡터 실 사용, 한쪽씩 교대로 시술하며 대칭 확인 |
| `evidence` | — | (키 없음) |

#### `/categories/3/complications/4` — 구형구축 (Capsular Contracture-like Reaction / 섬유성 결절)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/3/complications/4/name` | 구형구축 (Capsular Contracture-like Reaction / 섬유성 결절) |
| `severity` | `/categories/3/complications/4/severity` | moderate |
| `incidence` | `/categories/3/complications/4/incidence` | 0.5-2% |
| `onset` | `/categories/3/complications/4/onset` | 수주~수개월 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/3/complications/4/mechanism` | 드문 중증 섬유성 캡슐 형성으로 실 주변 조직이 수축·경화. 실의 이물반응에 의한 과도한 콜라겐 생성과 국소 섬유성 캡슐 형성. 이물반응 기전으로 부위 무관. |
| `risk_factors` | `/categories/3/complications/4/risk_factors` | [] (빈 배열) |
| `management` | `/categories/3/complications/4/management` | 경미한 당김: 트리암시놀론 10-20mg/mL 국소 주사로 섬유화 완화, 4주 간격. 딤플링: 서브시전(subcision) + 필러 보충. 심한 경우: 실 제거 + 항섬유화 치료. 고주파/초음파 기기를 이용한 실 주변 조직 이완. |
| `prevention` | `/categories/3/complications/4/prevention` | 적정 실 수 사용(과도한 삽입 자제), 적절한 텐션(과도한 당김 금지), 켈로이드 체질 사전 확인, 시술 간 최소 6개월 간격, 시술 부위 마사지 교육. |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-021** (잠정) mechanism 의 「드문 중증 섬유성 캡슐 형성」과 severity `moderate`·incidence 「0.5-2%」를 원문 그대로 나란히 둔다. 서로 맞는지는 판단하지 않았다. 이름이 한국어 「구형구축」, 영문 「Capsular Contracture-like Reaction」, 「섬유성 결절」 셋을 같이 쓴다. → P4  
  근거: `/categories/3/complications/4/mechanism` 「드문 중증 섬유성 캡슐 형성」; `/categories/3/complications/4/severity` 「moderate」; `/categories/3/complications/4/name` 「Capsular Contracture-like Reaction / 섬유성 결절」

#### `/categories/3/complications/5` — 피부 딤플링/주름짐 (Skin Dimpling/Puckering)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/3/complications/5/name` | 피부 딤플링/주름짐 (Skin Dimpling/Puckering) |
| `severity` | `/categories/3/complications/5/severity` | mild |
| `incidence` | `/categories/3/complications/5/incidence` | 약 7-10%(50세 초과에서 최대 16%) |
| `onset` | `/categories/3/complications/5/onset` | 즉시 |
| `duration` | `/categories/3/complications/5/duration` | 대부분 수주 내 자연 소실 |
| `mechanism` | `/categories/3/complications/5/mechanism` | 표재성 barb/cog 거치 또는 과도한 텐션으로 진피가 당겨져 함몰·주름짐 발생 |
| `risk_factors[0]` | `/categories/3/complications/5/risk_factors/0` | 표재성 실 거치 |
| `risk_factors[1]` | `/categories/3/complications/5/risk_factors/1` | 과도한 텐션 |
| `risk_factors[2]` | `/categories/3/complications/5/risk_factors/2` | 얇은 피부 |
| `risk_factors[3]` | `/categories/3/complications/5/risk_factors/3` | 고령 |
| `risk_factors[4]` | `/categories/3/complications/5/risk_factors/4` | 부적절한 벡터 |
| `management` | `/categories/3/complications/5/management` | 대부분 수주 내 자연 소실. 지속 시 마사지·서브시전(subcision) 및 텐션 조절 고려 |
| `prevention` | `/categories/3/complications/5/prevention` | 적정 삽입 깊이와 텐션을 유지하고 표재성 barb 거치를 피함 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-022** (잠정) 하위집단 최대값이 있다(「50세 초과에서 최대 16%」). risk_factors 의 「고령」과 같은 축으로 보이지만(잠정), 기준 나이가 같은지는 원문에 없다. → F6  
  근거: `/categories/3/complications/5/incidence` 「50세 초과에서 최대 16%」; `/categories/3/complications/5/risk_factors/3` 「고령」

#### `/categories/3/complications/6` — 통증·당김감 (Pain / Tightness)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/3/complications/6/name` | 통증·당김감 (Pain / Tightness) |
| `severity` | `/categories/3/complications/6/severity` | mild |
| `incidence` | `/categories/3/complications/6/incidence` | 매우 흔함 (거의 전례에서 일시적) |
| `onset` | `/categories/3/complications/6/onset` | 즉시~수일 (당김감은 1-2주 지속) |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/3/complications/6/mechanism` | 실 삽입 경로의 조직 손상, barb의 조직 견인·앵커링에 의한 긴장감. 표정·저작·개구 시 실이 당겨지며 발생. 실 거치 부위와 무관하게 공통 발생하며 흡수·조직 순응과 함께 감소. |
| `risk_factors` | `/categories/3/complications/6/risk_factors` | [] (빈 배열) |
| `management` | `/categories/3/complications/6/management` | 경구 진통제(아세트아미노펜), 냉찜질, 표정·저작 제한. 통증이 국소적으로 심하거나 발적·열감 동반 시 감염/신경 자극 감별. |
| `prevention` | `/categories/3/complications/6/prevention` | 적정 텐션·삽입 깊이 준수, 과도한 barb 견인 회피, 시술 후 2-3주 심한 표정·저작·마사지 자제 교육. |
| `evidence` | `/categories/3/complications/6/evidence` | https://onlinelibrary.wiley.com/doi/full/10.1111/jocd.16745; https://www.hmpgloballearningnetwork.com/site/thederm/aesthetics-corner/polydioxanone-thread-lift-complications |

**잠정 관찰**

- **OB-023** (잠정) onset 칸에 하위 증상(당김감)의 지속 기간이 있다. → B3  
  근거: `/categories/3/complications/6/onset` 「당김감은 1-2주 지속」

#### `/categories/3/complications/7` — 부종·멍(혈종) (Edema / Bruising / Hematoma)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/3/complications/7/name` | 부종·멍(혈종) (Edema / Bruising / Hematoma) |
| `severity` | `/categories/3/complications/7/severity` | mild |
| `incidence` | `/categories/3/complications/7/incidence` | 멍 흔함(수일~2주), 유의 혈종은 드묾 |
| `onset` | `/categories/3/complications/7/onset` | 즉시~48시간 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/3/complications/7/mechanism` | 삽입 바늘·캐뉼라가 진피~피하 소혈관을 손상시켜 반상출혈·부종 발생. 어느 부위든 혈관을 지나므로 공통. (단, 관자·측두의 천측두동정맥 등 명명 혈관 손상에 의한 국소 혈종은 부위 특이 항목으로 별도 분류.) |
| `risk_factors` | `/categories/3/complications/7/risk_factors` | [] (빈 배열) |
| `management` | `/categories/3/complications/7/management` | 냉찜질·압박, 항응고·항혈소판제 사전 중단(가능 시). 확장성 혈종은 흡인·압박, 필요 시 배액. 멍은 대개 1-2주 내 소실. |
| `prevention` | `/categories/3/complications/7/prevention` | 시술 전 항응고제·음주·비타민E 중단, 캐뉼라 사용으로 혈관 손상 최소화, 사전 도플러로 혈관 회피. |
| `evidence` | `/categories/3/complications/7/evidence` | https://onlinelibrary.wiley.com/doi/full/10.1111/jocd.16745; https://www.newswise.com/articles/facial-thread-lifting-complications-causes-and-prevention |

**잠정 관찰**

- **OB-024** (원문 참조) incidence 가 두 사건에 각각 빈도를 준다(멍 흔함 · 유의 혈종 드묾). 명명 혈관 손상에 의한 국소 혈종은 「부위 특이 항목」으로 넘긴다. 이 원장 안에는 그런 항목이 없다. → B4  
  근거: `/categories/3/complications/7/incidence` 「멍 흔함(수일~2주), 유의 혈종은 드묾」; `/categories/3/complications/7/mechanism` 「부위 특이 항목으로 별도 분류」

### `/categories/4` — id `M8` · name 「레이저」 · complications 3개

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `id` | `/categories/4/id` | M8 |
| `name` | `/categories/4/name` | 레이저 |

#### `/categories/4/complications/0` — PIH (시술 후 과색소침착)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/4/complications/0/name` | PIH (시술 후 과색소침착) |
| `severity` | `/categories/4/complications/0/severity` | moderate |
| `incidence` | `/categories/4/complications/0/incidence` | 10-50% (CO2 레이저 시 최대 50%, Fitzpatrick IV-VI에서 높음) |
| `onset` | `/categories/4/complications/0/onset` | 2-6주 |
| `duration` | `/categories/4/complications/0/duration` | 3-12개월 (치료 시 단축 가능) |
| `mechanism` | `/categories/4/complications/0/mechanism` | 레이저 열손상 후 염증 반응으로 멜라닌세포 활성화. 표피 손상 → 염증성 사이토카인 → 멜라닌 과생성. 진피 내 멜라닌 침착(melanophage) 시 장기 지속. 동아시아인(Fitzpatrick III-IV) 특히 고위험 |
| `risk_factors[0]` | `/categories/4/complications/0/risk_factors/0` | Fitzpatrick III-VI 피부 |
| `risk_factors[1]` | `/categories/4/complications/0/risk_factors/1` | CO2/Er:YAG 절삭 레이저 |
| `risk_factors[2]` | `/categories/4/complications/0/risk_factors/2` | 높은 에너지 설정 |
| `risk_factors[3]` | `/categories/4/complications/0/risk_factors/3` | 시술 후 자외선 노출 |
| `risk_factors[4]` | `/categories/4/complications/0/risk_factors/4` | 시술 전 피부 염증 존재 |
| `risk_factors[5]` | `/categories/4/complications/0/risk_factors/5` | 부적절한 사후 관리 |
| `management` | `/categories/4/complications/0/management` | 하이드로퀴논 4% 크림 + 트레티노인 0.025-0.05% + 하이드로코르티손 1% (Kligman's formula) 2-3개월. 트라넥사믹산 경구 250mg 2회/일 또는 국소 도포. 아젤라산 15-20% 크림. 비타민C 세럼 병용. 광범위 자외선 차단제(SPF 50+) 필수. 치료 불응 시 저출력 1064nm Nd:YAG 레이저 토닝 |
| `prevention` | `/categories/4/complications/0/prevention` | Fitzpatrick 피부 타입 평가 필수, 고위험군 시술 전 2-4주 하이드로퀴논 전처치, 적정 에너지 파라미터 설정, 시술 후 4-6주 철저한 자외선 차단(SPF 50+, 물리적 차단 병용), 여름철 절삭 레이저 자제 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-025** (잠정) 피부형 범위가 칸마다 다르다 — incidence 「Fitzpatrick IV-VI에서 높음」, mechanism 「동아시아인(Fitzpatrick III-IV) 특히 고위험」, risk_factors 「Fitzpatrick III-VI 피부」. prevention 에 계절 조건이 있다(「여름철 절삭 레이저 자제」). → F6  
  근거: `/categories/4/complications/0/incidence` 「Fitzpatrick IV-VI에서 높음」; `/categories/4/complications/0/mechanism` 「동아시아인(Fitzpatrick III-IV) 특히 고위험」; `/categories/4/complications/0/risk_factors/0` 「Fitzpatrick III-VI 피부」; `/categories/4/complications/0/prevention` 「여름철 절삭 레이저 자제」

#### `/categories/4/complications/1` — 홍반 (Erythema)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/4/complications/1/name` | 홍반 (Erythema) |
| `severity` | `/categories/4/complications/1/severity` | mild |
| `incidence` | `/categories/4/complications/1/incidence` | 거의 전례(일과성). 비박피 토닝/IPL 수시간~2-3일, 박피성 프락셔널/CO2 수일~수주 |
| `onset` | `/categories/4/complications/1/onset` | 즉시 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/4/complications/1/mechanism` | 레이저·광에너지의 조직 흡수로 발생한 열이 진피 혈관 확장과 경미한 염증 반응을 유발. 파장·적응증·부위와 무관하게 에너지가 조직에 흡수되는 모든 레이저 시술의 공통 즉각 반응. 박피 깊이·에너지·밀도가 클수록 강도·지속기간 증가 |
| `risk_factors` | `/categories/4/complications/1/risk_factors` | [] (빈 배열) |
| `management` | `/categories/4/complications/1/management` | 냉찜질/냉각, 진정 보습(판테놀·시카), 필요시 저강도 국소 스테로이드 단기. 물리적 자외선 차단. 대개 자연 소실이므로 경과 관찰 |
| `prevention` | `/categories/4/complications/1/prevention` | 적정 에너지·냉각 병행, 다중 패스 시 열축적(thermal stacking) 최소화, 시술 직후 자극·열 노출(사우나·운동) 회피 |
| `evidence` | `/categories/4/complications/1/evidence` | clinical-standard: universal laser thermal response |

**잠정 관찰**

- **OB-026** (잠정) incidence 칸에 시술 방식에 따른 지속 기간이 들어 있다(비박피 토닝/IPL ↔ 박피성 프락셔널/CO2). evidence 는 문헌이 아니라 「clinical-standard」 표지다. → B3  
  근거: `/categories/4/complications/1/incidence` 「비박피 토닝/IPL 수시간~2-3일, 박피성 프락셔널/CO2 수일~수주」; `/categories/4/complications/1/evidence` 「clinical-standard」

#### `/categories/4/complications/2` — 부종 (Edema)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/4/complications/2/name` | 부종 (Edema) |
| `severity` | `/categories/4/complications/2/severity` | mild |
| `incidence` | `/categories/4/complications/2/incidence` | 흔함(일과성). 안와주위·구주위 등 피부가 얇고 성긴 부위에서 특히 현저하나 발생 자체는 부위 무관 |
| `onset` | `/categories/4/complications/2/onset` | 즉시~24시간 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/4/complications/2/mechanism` | 열손상에 의한 혈관 투과성 증가로 간질액 저류. 모든 레이저 시술에서 공통으로 나타나는 급성 염증성 반응. 다만 눈꺼풀·입술 등 성긴 결합조직 부위에서 더 눈에 띄게 나타남 |
| `risk_factors` | `/categories/4/complications/2/risk_factors` | [] (빈 배열) |
| `management` | `/categories/4/complications/2/management` | 냉찜질, 시술 당일 머리 높여 수면(안면부), 필요시 단기 항히스타민. 광범위·지속 부종 시 단기 경구 스테로이드 고려. 대개 1-3일 내 소실 |
| `prevention` | `/categories/4/complications/2/prevention` | 냉각 병행, 과도한 중첩 조사 자제, 시술 후 24시간 열 노출·음주 회피, 안면부는 취침 시 상체 거상 |
| `evidence` | `/categories/4/complications/2/evidence` | clinical-standard: universal laser thermal response |

**잠정 관찰**

- **OB-027** (잠정) 「부위 무관」이라고 하면서 두드러지는 부위를 함께 적는다(「안와주위·구주위 …특히 현저하나 발생 자체는 부위 무관」). 발생과 정도를 나눠 말한 것으로 읽힌다(잠정). → F8  
  근거: `/categories/4/complications/2/incidence` 「발생 자체는 부위 무관」; `/categories/4/complications/2/mechanism` 「눈꺼풀·입술 등 성긴 결합조직 부위에서 더 눈에 띄게 나타남」

### `/categories/5` — id `M9` · name 「기기 리프팅」 · complications 6개

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `id` | `/categories/5/id` | M9 |
| `name` | `/categories/5/name` | 기기 리프팅 |

#### `/categories/5/complications/0` — 화상 (수포 포함)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/5/complications/0/name` | 화상 (수포 포함) |
| `severity` | `/categories/5/complications/0/severity` | severe |
| `incidence` | `/categories/5/complications/0/incidence` | 0.5-2% |
| `onset` | `/categories/5/complications/0/onset` | 즉시~수시간 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/5/complications/0/mechanism` | RF/HIFU 에너지의 과도한 열 축적, 커플링 불량, 장비 오작동. 피부 표면(RF) 또는 심부 조직(HIFU) 열손상. 에너지·커플링·세팅 문제로 조사되는 모든 부위에서 발생 가능해 특정 부위 특이가 아님(부위 무관 공통). 다만 골 돌출부(이마·하악연·관자)와 얇은 피부에서 열 축적으로 위험이 상대적으로 높고, RF는 표면 화상·HIFU는 심부 화상 양상. 너무 높은 에너지에서 수포(물집) 동반 |
| `risk_factors` | `/categories/5/complications/0/risk_factors` | [] (빈 배열) |
| `management` | `/categories/5/complications/0/management` | 즉시 냉각. 표재성 화상: 습윤 드레싱, 항생제 연고. 심부 화상: 경과 관찰 + 항염 치료. 수포 형성 시 무균 배액. 반흔/PIH 예방 병행 |
| `prevention` | `/categories/5/complications/0/prevention` | 파라미터 점진적 상승(저에너지부터), 커플링 확인, 환자 통증 피드백 즉시 반영, 금속 임플란트 부위 회피, 장비 정기 점검·캘리브레이션 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-028** (잠정) 「부위 무관 공통」이라고 하면서 위험이 높은 부위(골 돌출부·얇은 피부)를 든다. 기기에 따라 양상이 다르고(RF 표면 ↔ HIFU 심부), 에너지 조건이 붙은 하위 사건(수포)이 있다. risk_factors 는 비었다. → F8  
  근거: `/categories/5/complications/0/mechanism` 「부위 무관 공통」; `/categories/5/complications/0/mechanism` 「RF는 표면 화상·HIFU는 심부 화상 양상」; `/categories/5/complications/0/mechanism` 「너무 높은 에너지에서 수포(물집) 동반」

#### `/categories/5/complications/1` — 홍반 (시술 직후 빨개짐)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/5/complications/1/name` | 홍반 (시술 직후 빨개짐) |
| `severity` | `/categories/5/complications/1/severity` | mild |
| `incidence` | `/categories/5/complications/1/incidence` | 거의 전례(시술 직후 일시적). 대부분 수 시간~수일 내 자연 소실 |
| `onset` | `/categories/5/complications/1/onset` | 즉시 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/5/complications/1/mechanism` | HIFU/RF 열에너지에 대한 진피 혈관 확장 및 국소 염증 반응. 부위·기기 무관하게 조사 직후 나타나는 정상 반응 |
| `risk_factors` | `/categories/5/complications/1/risk_factors` | [] (빈 배열) |
| `management` | `/categories/5/complications/1/management` | 냉찜질·보습·진정 스킨케어. 특별 치료 불필요, 수시간~수일 관찰. 정상 경과로 안내 |
| `prevention` | `/categories/5/complications/1/prevention` | 적절한 에너지·쿨링, 시술 직후 냉각. 예방 대상이라기보다 예측 가능한 정상 반응 |
| `evidence` | `/categories/5/complications/1/evidence` | taxonomy.json M9 safety.common (홍반); HIFU esthetic complications review, Appl Sci 2025 (mdpi.com/2076-3417/15/9/4958) |

#### `/categories/5/complications/2` — 부종 (붓기)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/5/complications/2/name` | 부종 (붓기) |
| `severity` | `/categories/5/complications/2/severity` | mild |
| `incidence` | `/categories/5/complications/2/incidence` | 흔함. 경우에 따라 2~3일 지속 |
| `onset` | `/categories/5/complications/2/onset` | 즉시~수시간 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/5/complications/2/mechanism` | 열자극에 의한 미세혈관 투과성 증가와 간질 부종. SMAS/진피 가열 후 조직 반응으로 부위 무관 발생 |
| `risk_factors` | `/categories/5/complications/2/risk_factors` | [] (빈 배열) |
| `management` | `/categories/5/complications/2/management` | 냉찜질, 두상 거상 수면. 대부분 2-3일 내 소실, 지속 시 경구 항염제 |
| `prevention` | `/categories/5/complications/2/prevention` | 과도한 중첩 조사 회피, 시술 후 냉각·보습 |
| `evidence` | `/categories/5/complications/2/evidence` | taxonomy.json M9 safety.common (부종); HIFU esthetic complications review, Appl Sci 2025 |

**잠정 관찰**

- **OB-029** (잠정) incidence 칸에 지속 기간이 조건 「경우에 따라」와 함께 있다. 범위 기호가 같은 원장 안에서 `~`(2~3일)와 `-`(2-3일)로 섞여 쓰인다. → P1  
  근거: `/categories/5/complications/2/incidence` 「경우에 따라 2~3일 지속」; `/categories/5/complications/2/management` 「2-3일 내 소실」

#### `/categories/5/complications/3` — 통증·열감 (시술 중/후)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/5/complications/3/name` | 통증·열감 (시술 중/후) |
| `severity` | `/categories/5/complications/3/severity` | mild |
| `incidence` | `/categories/5/complications/3/incidence` | 시술 중 흔함(특히 HIFU 골막 자극 시). 시술 후 압통 수일 |
| `onset` | `/categories/5/complications/3/onset` | 시술 중~수일 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/5/complications/3/mechanism` | 집속초음파/고주파 심부열에 의한 통각 및 골막 자극(골 돌출부에서 강함), 시술 후 근막 부종성 압통. 조사 부위 전반에서 발생하는 공통 반응 |
| `risk_factors` | `/categories/5/complications/3/risk_factors` | [] (빈 배열) |
| `management` | `/categories/5/complications/3/management` | 시술 중 에너지 조절·표면마취/송풍냉각, 시술 후 아세트아미노펜. 대부분 수일 내 완화 |
| `prevention` | `/categories/5/complications/3/prevention` | 점진적 에너지 상승, 골막 근접 부위(이마·하악연) 에너지 감량, 쿨링 |
| `evidence` | `/categories/5/complications/3/evidence` | taxonomy.json M9 safety.common (따끔거림); HIFU esthetic complications review, Appl Sci 2025 |

**잠정 관찰**

- **OB-030** (잠정) incidence 가 시술 중과 시술 후 두 시점으로 나뉜다(「시술 중 흔함」, 「시술 후 압통 수일」). → B3  
  근거: `/categories/5/complications/3/incidence` 「시술 중 흔함(특히 HIFU 골막 자극 시). 시술 후 압통 수일」

#### `/categories/5/complications/4` — 일시적 감각이상 (따끔거림·저림·감각둔화)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/5/complications/4/name` | 일시적 감각이상 (따끔거림·저림·감각둔화) |
| `severity` | `/categories/5/complications/4/severity` | mild |
| `incidence` | `/categories/5/complications/4/incidence` | 흔함(일시적). 수일~수주 내 회복 |
| `onset` | `/categories/5/complications/4/onset` | 즉시~수일 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/5/complications/4/mechanism` | 표재 감각신경 종말의 일시적 열자극에 의한 가역적 신경실조. 운동신경 손상(부위 특이 신경손상)과 달리 부위 무관하게 흔히 나타나는 경한 감각 변화 |
| `risk_factors` | `/categories/5/complications/4/risk_factors` | [] (빈 배열) |
| `management` | `/categories/5/complications/4/management` | 경과 관찰, 대부분 자연 회복. 비타민B군 보조. 단, 4주 이상 지속하거나 운동마비(입꼬리·눈썹 비대칭)를 동반하면 부위 특이 신경손상으로 감별 필요 |
| `prevention` | `/categories/5/complications/4/prevention` | 과도 중첩·고에너지 회피, 적절한 카트리지 깊이 |
| `evidence` | `/categories/5/complications/4/evidence` | taxonomy.json M9 safety.common (일시적 감각 둔화); HIFU esthetic complications review, Appl Sci 2025 |

**잠정 관찰**

- **OB-031** (원문 참조) 처치에 다른 사건으로 넘기는 문턱이 있다(「4주 이상 지속하거나 운동마비 … 동반하면 부위 특이 신경손상으로 감별」). 그 항목은 이 원장에 없다. → B4  
  근거: `/categories/5/complications/4/management` 「4주 이상 지속하거나 운동마비(입꼬리·눈썹 비대칭)를 동반하면 부위 특이 신경손상으로 감별 필요」

#### `/categories/5/complications/5` — 색소침착 (염증후 과색소침착, PIH)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/5/complications/5/name` | 색소침착 (염증후 과색소침착, PIH) |
| `severity` | `/categories/5/complications/5/severity` | moderate |
| `incidence` | `/categories/5/complications/5/incidence` | 짙은 피부형(Fitzpatrick IV-VI)·과도 에너지에서 증가. 대개 일시적, 수주~수개월 |
| `onset` | `/categories/5/complications/5/onset` | 수일~수주 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/5/complications/5/mechanism` | 열자극 염증 후 멜라닌세포 활성화. 발생은 부위보다 피부타입·자외선 노출 요인이 지배적이어서 특정 부위 특이가 아닌 공통 위험으로 분류 |
| `risk_factors` | `/categories/5/complications/5/risk_factors` | [] (빈 배열) |
| `management` | `/categories/5/complications/5/management` | 엄격한 자외선 차단, 미백제(하이드로퀴논·트라넥삼산·비타민C), 필요시 저에너지 토닝. 대부분 가역적 |
| `prevention` | `/categories/5/complications/5/prevention` | 짙은 피부형 에너지 감량, 시술 전후 자외선 차단·선크림 필수, 활동성 염증·태닝 상태 회피 |
| `evidence` | `/categories/5/complications/5/evidence` | taxonomy.json M9 safety.uncommon (색소침착); HIFU esthetic complications review, Appl Sci 2025 |

**잠정 관찰**

- **OB-032** (잠정) incidence 칸에 수치가 없다. 증가 조건(피부형·과도 에너지)과 지속 기간만 있다. evidence 가 다른 원장의 `safety.uncommon` 을 가리킨다. → B2  
  근거: `/categories/5/complications/5/incidence` 「짙은 피부형(Fitzpatrick IV-VI)·과도 에너지에서 증가」; `/categories/5/complications/5/evidence` 「taxonomy.json M9 safety.uncommon」

### `/categories/6` — id `M11` · name 「니들RF」 · complications 5개

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `id` | `/categories/6/id` | M11 |
| `name` | `/categories/6/name` | 니들RF |

#### `/categories/6/complications/0` — 반흔 (Scarring)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/6/complications/0/name` | 반흔 (Scarring) |
| `severity` | `/categories/6/complications/0/severity` | severe |
| `incidence` | `/categories/6/complications/0/incidence` | 0.5-2% |
| `onset` | `/categories/6/complications/0/onset` | 수주~수개월 |
| `duration` | `/categories/6/complications/0/duration` | 영구적 (치료로 개선 가능) |
| `mechanism` | `/categories/6/complications/0/mechanism` | 니들에 의한 물리적 손상 + RF 열에너지의 복합 작용으로 과도한 진피 손상. 비정상적 창상 치유 반응으로 비후성/위축성 반흔 형성 |
| `risk_factors[0]` | `/categories/6/complications/0/risk_factors/0` | 높은 에너지/깊이 설정 |
| `risk_factors[1]` | `/categories/6/complications/0/risk_factors/1` | 켈로이드 체질 |
| `risk_factors[2]` | `/categories/6/complications/0/risk_factors/2` | 동일 부위 반복 조사 |
| `risk_factors[3]` | `/categories/6/complications/0/risk_factors/3` | 감염 합병 |
| `risk_factors[4]` | `/categories/6/complications/0/risk_factors/4` | 시술 직후 자극적 외용제 사용 |
| `management` | `/categories/6/complications/0/management` | 비후성 반흔: 트리암시놀론 10-40mg/mL 병변 내 주사 4주 간격, 실리콘 시트. 위축성 반흔: 프랙셔널 레이저, 서브시전, TCA CROSS. PDL(595nm) 레이저로 반흔 홍조 개선. 방사선 치료(켈로이드, 불응성) |
| `prevention` | `/categories/6/complications/0/prevention` | 켈로이드/비후성 반흔 병력 확인. 2017 ASDS 합의상 니들RF는 이소트레티노인 병용/최근 복용 환자에서도 안전하게 시행 가능하며 관례적 6개월 대기는 근거 부족으로 더 이상 권고되지 않음. test spot 선행, 보수적 에너지/깊이 시작, 시술 후 습윤 관리, 자극 외용제(레티노이드, AHA) 시술 전후 1주 중단 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-033** (잠정) prevention 에 문헌 합의를 근거로 한 「더 이상 권고되지 않음」이 있다(관례적 6개월 대기). 원장에 적힌 주장으로만 보존한다. duration 은 「영구적」에 「치료로 개선 가능」이 함께 붙는다. → F7  
  근거: `/categories/6/complications/0/prevention` 「관례적 6개월 대기는 근거 부족으로 더 이상 권고되지 않음」; `/categories/6/complications/0/duration` 「영구적 (치료로 개선 가능)」

#### `/categories/6/complications/1` — PIH (시술 후 과색소침착)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/6/complications/1/name` | PIH (시술 후 과색소침착) |
| `severity` | `/categories/6/complications/1/severity` | moderate |
| `incidence` | `/categories/6/complications/1/incidence` | 5-20% (Fitzpatrick III-V) |
| `onset` | `/categories/6/complications/1/onset` | 2-4주 |
| `duration` | `/categories/6/complications/1/duration` | 2-6개월 |
| `mechanism` | `/categories/6/complications/1/mechanism` | 니들 + RF 열에 의한 표피/진피 염증 반응 → 멜라닌세포 활성화 → 멜라닌 과생성. 동아시아인(Fitzpatrick III-IV)에서 높은 빈도 |
| `risk_factors[0]` | `/categories/6/complications/1/risk_factors/0` | Fitzpatrick III-VI 피부 |
| `risk_factors[1]` | `/categories/6/complications/1/risk_factors/1` | 높은 에너지 설정 |
| `risk_factors[2]` | `/categories/6/complications/1/risk_factors/2` | 시술 후 자외선 노출 |
| `risk_factors[3]` | `/categories/6/complications/1/risk_factors/3` | 시술 전후 부적절한 스킨케어 |
| `risk_factors[4]` | `/categories/6/complications/1/risk_factors/4` | 절연 코팅 불량 팁(비절연 니들) |
| `management` | `/categories/6/complications/1/management` | 자외선 차단제(SPF 50+) 필수. 하이드로퀴논 4% + 트레티노인 크림 2-3개월. 트라넥사믹산 경구/국소. 비타민C 세럼. 불응성: 저출력 1064nm Nd:YAG 레이저 토닝 |
| `prevention` | `/categories/6/complications/1/prevention` | Fitzpatrick 피부 타입 평가, 고위험군 시술 전 2주 하이드로퀴논 전처치, 절연 팁(insulated needle) 사용(표피 보호), 보수적 에너지 설정, 시술 후 4-6주 철저한 자외선 차단 |
| `evidence` | — | (키 없음) |

#### `/categories/6/complications/2` — 감염

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/6/complications/2/name` | 감염 |
| `severity` | `/categories/6/complications/2/severity` | severe |
| `incidence` | `/categories/6/complications/2/incidence` | 0.5-1% |
| `onset` | `/categories/6/complications/2/onset` | 수일~수주 |
| `duration` | `/categories/6/complications/2/duration` | 2-4주 (치료 시) |
| `mechanism` | `/categories/6/complications/2/mechanism` | 다수의 미세 천공을 통한 세균 침입. 비무균 환경, 시술 전후 오염된 외용제 사용. 드물게 NTM(비결핵항산균) 감염 보고 |
| `risk_factors[0]` | `/categories/6/complications/2/risk_factors/0` | 비무균 시술 환경 |
| `risk_factors[1]` | `/categories/6/complications/2/risk_factors/1` | 시술 직후 비멸균 외용제 도포 |
| `risk_factors[2]` | `/categories/6/complications/2/risk_factors/2` | 면역저하 |
| `risk_factors[3]` | `/categories/6/complications/2/risk_factors/3` | 기존 피부 감염 |
| `risk_factors[4]` | `/categories/6/complications/2/risk_factors/4` | 여드름 활성기 시술 |
| `management` | `/categories/6/complications/2/management` | 경험적 항생제(세팔렉신 500mg 4회/일 또는 독시사이클린 100mg 2회/일) 7-14일. 배양검사 시행. 농양 시 절개배농. NTM 의심 시 항산균 배양 + 클래리스로마이신 기반 치료 |
| `prevention` | `/categories/6/complications/2/prevention` | 무균 술기 철저, 시술 부위 클로르헥시딘 소독, 시술 직후 멸균 외용제만 사용, 여드름 활성기/피부 감염 시 시술 연기, 시술 후 24시간 자극적 화장 자제 교육 |
| `evidence` | — | (키 없음) |

#### `/categories/6/complications/3` — 화상 (열손상, Thermal Burn)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/6/complications/3/name` | 화상 (열손상, Thermal Burn) |
| `severity` | `/categories/6/complications/3/severity` | severe |
| `incidence` | `/categories/6/complications/3/incidence` | MAUDE 보고 합병증의 약 6.3%(14/224 events, 2013–2025.10) — 보고 비율이며 실제 발생률은 과소보고로 불명확. 경증 표재 화상은 이보다 흔함 |
| `onset` | `/categories/6/complications/3/onset` | 즉시~수시간(급성 수포·미란·중증 홍반), 이차 반흔·색소변화는 수주~수개월 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/6/complications/3/mechanism` | RF 열에너지가 표피/유두진피에 과도 전달되어 응고 괴사 발생. (1) 짧은 니들+고출력+다중 패스(stacking)로 표피 과열, (2) 니들 절연 손상·부분 노출로 니들 채널을 따라 선상·격자상(grid) 화상, (3) 굴곡·골 돌출부에서 불균일 접촉/아크·핫스팟. 조사 부위 어디서나 발생하는 부위 무관 공통 합병증(FDA는 안면·목·복부 등 다부위 보고) |
| `risk_factors` | `/categories/6/complications/3/risk_factors` | [] (빈 배열) |
| `management` | `/categories/6/complications/3/management` | 즉시 냉각 및 시술 중단, 비점착 드레싱, 장벽 손상 시 국소 항생제, 철저한 광차단(PIH 예방). 비후성 염증반응/초기 비후성 반흔에 국소·병변내 스테로이드. 심부 진피화상은 창상관리, 드물게 외과적 debridement. 후유 색소변화는 색소조절제·후기 분획레이저/IPL, 반흔은 실리콘·스테로이드·반흔 재건 |
| `prevention` | `/categories/6/complications/3/prevention` | 보수적 에너지·펄스폭, 시술 전 니들 절연 팁 무결성 확인, '짧은 니들+고출력' 조합 회피, 패스 간 충분한 냉각·간격 유지, 균일한 피부 접촉 확보, 얇은 부위(관자·안와주위·목) 저에너지, test spot 선행 |
| `evidence` | `/categories/6/complications/3/evidence` | FDA RF Microneedling Safety Communication (2025-10-15) — burns superficial to deep dermal, 일부 debridement/수술 필요; MAUDE 분석 (PubMed 41886649): 114 reports/224 events 중 burns 14건(6.3%) |

**잠정 관찰**

- **OB-034** (잠정) incidence 는 발생률이 아니라 보고 비율이라고 스스로 밝히고, 「이보다」로 앞의 수치를 다시 가리킨다. 날짜 범위에 en dash(2013–2025.10)를 쓴다. evidence 에 같은 수치의 다른 표기가 있다(14/224 events ↔ 114 reports/224 events 중 burns 14건). onset 은 급성과 이차 두 단계다. → F7  
  근거: `/categories/6/complications/3/incidence` 「보고 비율이며 실제 발생률은 과소보고로 불명확」; `/categories/6/complications/3/incidence` 「경증 표재 화상은 이보다 흔함」; `/categories/6/complications/3/evidence` 「114 reports/224 events 중 burns 14건(6.3%)」; `/categories/6/complications/3/onset` 「이차 반흔·색소변화는 수주~수개월」

#### `/categories/6/complications/4` — 일시적 홍반·부종 (Transient Erythema/Edema)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/6/complications/4/name` | 일시적 홍반·부종 (Transient Erythema/Edema) |
| `severity` | `/categories/6/complications/4/severity` | mild |
| `incidence` | `/categories/6/complications/4/incidence` | 거의 보편적(대부분 환자) — 예상되는 정상 회복 반응 |
| `onset` | `/categories/6/complications/4/onset` | 즉시 발생, 24-72시간 내 대부분 소실 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/6/complications/4/mechanism` | 니들의 물리적 미세손상 + RF 열에 의한 정상 급성 염증 반응(혈관확장·모세혈관 투과성 증가). 모든 조사 부위에서 동일하게 나타나는 부위 무관 공통 반응 |
| `risk_factors` | `/categories/6/complications/4/risk_factors` | [] (빈 배열) |
| `management` | `/categories/6/complications/4/management` | 냉찜질, 진정 스킨케어, 광차단으로 자연 회복. 부종 심하면 시술 당일 두부 거상·냉찜질 |
| `prevention` | `/categories/6/complications/4/prevention` | 적정 에너지·패스 수 조절, 시술 직후 냉각·보습, 자극 외용제 회피. 시술 전 예상 경과로 사전 고지(합병증 아닌 정상 경과) |
| `evidence` | `/categories/6/complications/4/evidence` | taxonomy.json M11 extracted.safety.common (일시적 홍반·부종·딱지); 니들RF 임상 통설 — 예상 회복 반응 |

### `/categories/7` — id `M14` · name 「크라이오리포라이시스」 · complications 7개

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `id` | `/categories/7/id` | M14 |
| `name` | `/categories/7/name` | 크라이오리포라이시스 |

#### `/categories/7/complications/0` — PAH (역설적 지방 증식, Paradoxical Adipose Hyperplasia)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/7/complications/0/name` | PAH (역설적 지방 증식, Paradoxical Adipose Hyperplasia) |
| `severity` | `/categories/7/complications/0/severity` | severe |
| `incidence` | `/categories/7/complications/0/incidence` | 통합 추정 약 0.2%(1/455, 2025 systematic review), 독립 연구에서 0.05-0.91%까지 보고하며 과소보고 가능성 높음. 제조사(Allergan 2024) 추정치는 0.033%(1/3000); 신세대 기기에서 발생률 감소 경향 |
| `onset` | `/categories/7/complications/0/onset` | 2-6개월 |
| `duration` | `/categories/7/complications/0/duration` | 영구적 (자연 소실 없음) |
| `mechanism` | `/categories/7/complications/0/mechanism` | 냉각에 의해 지방세포가 파괴되지 않고 오히려 비대·증식하는 역설적 반응. 정확한 기전 불명이나 cold-induced adipogenesis 가설: 냉각 자극이 지방전구세포를 자극하여 분화·증식 유도. 시술 부위가 주변보다 단단하게 융기 |
| `risk_factors[0]` | `/categories/7/complications/0/risk_factors/0` | 남성 |
| `risk_factors[1]` | `/categories/7/complications/0/risk_factors/1` | 히스패닉 인종 |
| `risk_factors[2]` | `/categories/7/complications/0/risk_factors/2` | 높은 BMI 가능 인자(근거 불확실) |
| `risk_factors[3]` | `/categories/7/complications/0/risk_factors/3` | 복부 시술 |
| `risk_factors[4]` | `/categories/7/complications/0/risk_factors/4` | 대형 어플리케이터/핸드피스(넓은 치료 면적) 사용 |
| `risk_factors[5]` | `/categories/7/complications/0/risk_factors/5` | 유전적 소인(가족력) |
| `management` | `/categories/7/complications/0/management` | 경과 관찰로 소실되지 않음(영구적). 지방흡입술이 유일한 근치적 치료. 추가 크라이오 시술은 PAH 악화 가능 — 금기. 지방흡입 시기: PAH 확진 후 최소 6-9개월 이후(조직 안정화 후). 비침습적 대안: DCA 주사(디옥시콜산) 시도 보고 있으나 효과 제한적 |
| `prevention` | `/categories/7/complications/0/prevention` | 시술 전 PAH 위험 고지(특히 남성), 가족력/개인 기왕력 확인, 발생 시 조기 인지를 위한 시술 후 사진 기록, 의심 증상(시술 부위 경결/융기) 발생 시 즉시 내원 교육. 현재 완전한 예방법은 없음 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-035** (잠정) 빈도 추정치가 출처별로 여럿이다(통합 추정·독립 연구·제조사). risk_factors 한 항목에 근거 수준 한정어가 있다(「가능 인자(근거 불확실)」). 처치의 「금기」, 시기 문턱(「최소 6-9개월 이후」), prevention 의 「현재 완전한 예방법은 없음」을 보존한다. → F7  
  근거: `/categories/7/complications/0/incidence` 「제조사(Allergan 2024) 추정치는 0.033%(1/3000)」; `/categories/7/complications/0/risk_factors/2` 「높은 BMI 가능 인자(근거 불확실)」; `/categories/7/complications/0/management` 「추가 크라이오 시술은 PAH 악화 가능 — 금기」; `/categories/7/complications/0/prevention` 「현재 완전한 예방법은 없음」

#### `/categories/7/complications/1` — 피부 괴사 (Skin Necrosis / 동상·지방괴사, Frostbite·Fat Necrosis)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/7/complications/1/name` | 피부 괴사 (Skin Necrosis / 동상·지방괴사, Frostbite·Fat Necrosis) |
| `severity` | `/categories/7/complications/1/severity` | critical |
| `incidence` | `/categories/7/complications/1/incidence` | 극히 드묾 (<0.01%). 어느 치료 부위에서도 발생 가능(복부 전층 지방괴사 증례, 사지·체부 동상 증례 보고) |
| `onset` | `/categories/7/complications/1/onset` | 수일~수주 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/7/complications/1/mechanism` | 과도한 냉각 또는 흡입 압력에 의한 피부 혈류 차단 → 허혈성 괴사(동상). 진공 흡입에 의한 모세혈관 파열·혈종 후 이차 손상. 한랭 두드러기 환자의 과도 반응. 냉각손상은 어플리케이터가 접촉하는 모든 부위에서 발생 가능해 부위 무관 공통 |
| `risk_factors` | `/categories/7/complications/1/risk_factors` | [] (빈 배열) |
| `management` | `/categories/7/complications/1/management` | 즉시 시술 중단, 서서히 재가온(급격한 가온 금지). 괴사 부위: 습윤 드레싱, 항생제 연고, 2차 감염 예방. 광범위 시 성형외과 협진(피부이식 가능). 치유 후 반흔 관리 |
| `prevention` | `/categories/7/complications/1/prevention` | 한랭 두드러기·한랭글로불린혈증·발작성 한랭혈색소뇨증은 절대 금기 확인, Raynaud는 상대 금기로 개별 평가. 적절 어플리케이터 크기, 시술 중 피부 주기 확인, 장비 점검, 냉각 프로토콜(젤 패드 포함) 준수 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-036** (잠정) 금기에 등급이 있다(「절대 금기」 ↔ 「상대 금기로 개별 평가」). 처치에 금지가 있다(「급격한 가온 금지」). incidence 에 사례가 난 부위(복부·사지·체부)가 함께 적혀 있다. → F3  
  근거: `/categories/7/complications/1/prevention` 「절대 금기 확인, Raynaud는 상대 금기로 개별 평가」; `/categories/7/complications/1/management` 「급격한 가온 금지」; `/categories/7/complications/1/incidence` 「복부 전층 지방괴사 증례, 사지·체부 동상 증례 보고」

#### `/categories/7/complications/2` — 일시적 감각저하·저림 (Transient Hypoesthesia / Paresthesia)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/7/complications/2/name` | 일시적 감각저하·저림 (Transient Hypoesthesia / Paresthesia) |
| `severity` | `/categories/7/complications/2/severity` | mild |
| `incidence` | `/categories/7/complications/2/incidence` | 매우 흔함 — 시술 후 가장 흔한 부작용군의 하나(대부분의 환자에서 일시적으로 경험) |
| `onset` | `/categories/7/complications/2/onset` | 시술 직후 발생, 대개 2주 이내 소실(일부 4-8주까지) |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/7/complications/2/mechanism` | 냉각과 진공 흡입에 의한 표재 감각신경의 일시적 전도 차단(냉각성 neuropraxia). 지방·피부 냉각 시 감각신경도 함께 냉각되어 발생. 어느 치료 부위든 공통 |
| `risk_factors` | `/categories/7/complications/2/risk_factors` | [] (빈 배열) |
| `management` | `/categories/7/complications/2/management` | 대부분 자연 회복, 경과관찰. 드물게 지속·통증 동반 시 가바펜틴 등 고려 |
| `prevention` | `/categories/7/complications/2/prevention` | 냉각·흡입 시간 프로토콜 준수, 과냉각 회피 |
| `evidence` | `/categories/7/complications/2/evidence` | https://onlinelibrary.wiley.com/doi/10.1111/jocd.16000 |

**잠정 관찰**

- **OB-037** (잠정) onset 칸에 소실 기간과 일부 예외(「일부 4-8주까지」)가 있다. → B3  
  근거: `/categories/7/complications/2/onset` 「대개 2주 이내 소실(일부 4-8주까지)」

#### `/categories/7/complications/3` — 일시적 홍반·부종 (Erythema / Edema)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/7/complications/3/name` | 일시적 홍반·부종 (Erythema / Edema) |
| `severity` | `/categories/7/complications/3/severity` | mild |
| `incidence` | `/categories/7/complications/3/incidence` | 매우 흔함(거의 모든 환자), 자연 소실 |
| `onset` | `/categories/7/complications/3/onset` | 시술 직후~수시간, 소실 수시간~수일 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/7/complications/3/mechanism` | 냉각 및 재가온(재관류) 과정의 혈관 반응·경미한 염증 반응. 어플리케이터 접촉 부위 어디든 공통 |
| `risk_factors` | `/categories/7/complications/3/risk_factors` | [] (빈 배열) |
| `management` | `/categories/7/complications/3/management` | 냉찜질, 경과관찰. 특별 처치 불필요 |
| `prevention` | `/categories/7/complications/3/prevention` | 프로토콜 준수 |
| `evidence` | `/categories/7/complications/3/evidence` | https://onlinelibrary.wiley.com/doi/10.1111/jocd.16000 |

#### `/categories/7/complications/4` — 멍·타박상 (Bruising)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/7/complications/4/name` | 멍·타박상 (Bruising) |
| `severity` | `/categories/7/complications/4/severity` | mild |
| `incidence` | `/categories/7/complications/4/incidence` | 흔함 |
| `onset` | `/categories/7/complications/4/onset` | 시술 직후~수일, 소실 1-2주 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/7/complications/4/mechanism` | 진공 흡입 어플리케이터에 의한 모세혈관 파열. 흡입식 컵을 적용하는 모든 부위에서 공통 발생 |
| `risk_factors` | `/categories/7/complications/4/risk_factors` | [] (빈 배열) |
| `management` | `/categories/7/complications/4/management` | 경과관찰, 대개 자연 소실. 필요시 아르니카·비타민K 국소 |
| `prevention` | `/categories/7/complications/4/prevention` | 항응고·항혈소판제 복용력 확인, 과도한 흡입 압력 회피 |
| `evidence` | `/categories/7/complications/4/evidence` | https://onlinelibrary.wiley.com/doi/10.1111/jocd.16000 |

#### `/categories/7/complications/5` — 통증·불편감 및 지연성 통증 (Procedural Pain & Late-Onset Pain, LOP)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/7/complications/5/name` | 통증·불편감 및 지연성 통증 (Procedural Pain & Late-Onset Pain, LOP) |
| `severity` | `/categories/7/complications/5/severity` | moderate |
| `incidence` | `/categories/7/complications/5/incidence` | 시술 중 당김·냉감 불편감은 흔함. 지연성 통증(LOP)은 소수에서 보고(넓은 치료면적·복부에서 다소 빈도↑이나 부위 전반에 발생) |
| `onset` | `/categories/7/complications/5/onset` | 시술 중~직후; 지연성 통증은 시술 3-4일 후 발현, 대개 2주 내 자연 소실 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/7/complications/5/mechanism` | 진공 흡입에 의한 조직 당김·냉감, 재관류 및 신경 자극. 지연성 신경병성 통증은 감각신경의 일시적 자극/신경병증으로 추정. 어느 부위든 발생하는 공통 현상 |
| `risk_factors` | `/categories/7/complications/5/risk_factors` | [] (빈 배열) |
| `management` | `/categories/7/complications/5/management` | NSAIDs, 경과관찰. 중증 지연성 통증에는 가바펜틴/프레가발린 고려 |
| `prevention` | `/categories/7/complications/5/prevention` | 시술 전 통증 가능성 고지, 프로토콜 준수 |
| `evidence` | `/categories/7/complications/5/evidence` | https://onlinelibrary.wiley.com/doi/10.1111/jocd.16000 |

**잠정 관찰**

- **OB-038** (잠정) 같은 항목 안에 하위 사건 두 개(시술 중 통증 · 지연성 통증 LOP)가 있고, 시점이 각각 다르다. mechanism 의 「추정」은 근거 수준 표지다. → P3  
  근거: `/categories/7/complications/5/onset` 「지연성 통증은 시술 3-4일 후 발현, 대개 2주 내 자연 소실」; `/categories/7/complications/5/mechanism` 「신경병증으로 추정」

#### `/categories/7/complications/6` — 염증후 색소침착 (Post-inflammatory Hyperpigmentation, PIH)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/7/complications/6/name` | 염증후 색소침착 (Post-inflammatory Hyperpigmentation, PIH) |
| `severity` | `/categories/7/complications/6/severity` | mild |
| `incidence` | `/categories/7/complications/6/incidence` | 드묾. Fitzpatrick IV-VI(진한 피부톤)에서 상대적으로 높음 |
| `onset` | `/categories/7/complications/6/onset` | 수주 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/7/complications/6/mechanism` | 냉각·염증 반응 후 멜라닌세포 활성화. 피부톤 관련 위험으로 치료 부위 무관 공통 |
| `risk_factors` | `/categories/7/complications/6/risk_factors` | [] (빈 배열) |
| `management` | `/categories/7/complications/6/management` | 자외선 차단, 미백제(하이드로퀴논 등), 대개 수개월에 걸쳐 자연 호전 |
| `prevention` | `/categories/7/complications/6/prevention` | 진한 피부톤 환자 사전 고지, 시술 후 철저한 광차단 |
| `evidence` | `/categories/7/complications/6/evidence` | https://onlinelibrary.wiley.com/doi/10.1111/jocd.16000 |

### `/categories/8` — id `M15` · name 「메디컬스킨케어」 · complications 4개

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `id` | `/categories/8/id` | M15 |
| `name` | `/categories/8/name` | 메디컬스킨케어 |

**잠정 관찰 (카테고리)**

- **OB-C08** (잠정) 카테고리 이름은 「메디컬스킨케어」인데 항목 4개는 모두 필링(산 도포)을 말한다. 카테고리 밖의 다른 스킨케어 시술이 있는지는 이 원장으로 알 수 없다. → B7  
  근거: `/categories/8/complications/0/mechanism` 「산 도포에 의한」; `/categories/8/complications/1/mechanism` 「모든 필링에 공통」

#### `/categories/8/complications/0` — 일시적 홍반 (Transient erythema)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/8/complications/0/name` | 일시적 홍반 (Transient erythema) |
| `severity` | `/categories/8/complications/0/severity` | mild |
| `incidence` | `/categories/8/complications/0/incidence` | 약 15% (표재), 사실상 전 필링에서 경도 발생 |
| `onset` | `/categories/8/complications/0/onset` | 즉시~수시간 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/8/complications/0/mechanism` | 산 도포에 의한 각질층 용해 및 표피 자극으로 혈관 확장·경도 염증 반응. 필링 깊이와 무관하게 모든 제제에서 나타나는 기본 반응. |
| `risk_factors` | `/categories/8/complications/0/risk_factors` | [] (빈 배열) |
| `management` | `/categories/8/complications/0/management` | 냉찜질, 보습, 진정 크림(판테놀/센텔라). 대개 처치 없이 소실. 표재는 수시간~72시간, 중~심부는 별도 지속성 홍반 항목 참조. |
| `prevention` | `/categories/8/complications/0/prevention` | 적정 농도·작용시간 준수, 시술 후 물리적 자극 금지, 보습 강화 |
| `evidence` | `/categories/8/complications/0/evidence` | https://www.tandfonline.com/doi/full/10.2147/CCID.S34029; https://www.theplasticsfella.com/chemical-peels/ |

**잠정 관찰**

- **OB-039** (원문 참조) 처치에서 중~심부 필링은 「별도 지속성 홍반 항목」으로 넘긴다. 이 원장에는 그 항목이 없다. 빈도에 깊이 조건(표재)이 붙어 있다. → B4  
  근거: `/categories/8/complications/0/management` 「중~심부는 별도 지속성 홍반 항목 참조」; `/categories/8/complications/0/incidence` 「약 15% (표재)」

#### `/categories/8/complications/1` — 자극감·작열감 (Stinging/burning)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/8/complications/1/name` | 자극감·작열감 (Stinging/burning) |
| `severity` | `/categories/8/complications/1/severity` | mild |
| `incidence` | `/categories/8/complications/1/incidence` | 매우 흔함 (도포 중 대부분) |
| `onset` | `/categories/8/complications/1/onset` | 도포 즉시 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/8/complications/1/mechanism` | 산성 제제가 유리 신경종말을 자극. 농도·pH가 낮을수록, 장벽이 손상된 피부일수록 강함. 제제 특성상 모든 필링에 공통. |
| `risk_factors` | `/categories/8/complications/1/risk_factors` | [] (빈 배열) |
| `management` | `/categories/8/complications/1/management` | 냉풍/냉찜질로 완화, 중화 또는 세척으로 종료. 조절 불가능한 통증은 과도 침투 신호이므로 즉시 중단. |
| `prevention` | `/categories/8/complications/1/prevention` | test spot, 도포 전 장벽 상태 평가, 민감피부는 저농도/단시간부터 |
| `evidence` | `/categories/8/complications/1/evidence` | https://www.tandfonline.com/doi/full/10.2147/CCID.S34029 |

**잠정 관찰**

- **OB-040** (잠정) 처치에 신호 해석과 중단 지시가 있다(「조절 불가능한 통증은 과도 침투 신호이므로 즉시 중단」). → F3  
  근거: `/categories/8/complications/1/management` 「조절 불가능한 통증은 과도 침투 신호이므로 즉시 중단」

#### `/categories/8/complications/2` — 건조·낙설(각질 박리) (Dryness/desquamation)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/8/complications/2/name` | 건조·낙설(각질 박리) (Dryness/desquamation) |
| `severity` | `/categories/8/complications/2/severity` | mild |
| `incidence` | `/categories/8/complications/2/incidence` | 흔함 (표재 필링의 의도된 반응) |
| `onset` | `/categories/8/complications/2/onset` | 1-3일 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/8/complications/2/mechanism` | 각질세포간 결합 용해로 인한 각질층 탈락 및 경표피 수분손실(TEWL) 증가. 재상피화·턴오버 촉진 과정의 일부. |
| `risk_factors` | `/categories/8/complications/2/risk_factors` | [] (빈 배열) |
| `management` | `/categories/8/complications/2/management` | 보습제 도포, 물리적으로 각질을 뜯지 않도록 교육, 온화한 세안 |
| `prevention` | `/categories/8/complications/2/prevention` | 시술 후 보습·자외선차단, 레티노이드/산 제품 병용 일시 중단 |
| `evidence` | `/categories/8/complications/2/evidence` | https://www.tandfonline.com/doi/full/10.2147/CCID.S34029; https://www.theplasticsfella.com/chemical-peels/ |

#### `/categories/8/complications/3` — 소양감 (Pruritus)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/8/complications/3/name` | 소양감 (Pruritus) |
| `severity` | `/categories/8/complications/3/severity` | mild |
| `incidence` | `/categories/8/complications/3/incidence` | 흔함 |
| `onset` | `/categories/8/complications/3/onset` | 시술 직후~재상피화기 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/8/complications/3/mechanism` | 각질 박리·건조 및 창상 치유 과정에서 히스타민/신경펩타이드 매개 가려움. 깊이 무관하게 발생하나 중~심부에서 더 강할 수 있음. |
| `risk_factors` | `/categories/8/complications/3/risk_factors` | [] (빈 배열) |
| `management` | `/categories/8/complications/3/management` | 보습, 필요 시 경구 항히스타민제, 긁힘 방지(2차 감염·색소침착 예방) |
| `prevention` | `/categories/8/complications/3/prevention` | 충분한 보습, 장벽 회복 지원 |
| `evidence` | `/categories/8/complications/3/evidence` | https://www.theplasticsfella.com/chemical-peels/ |

### `/categories/9` — id `M16` · name 「수액치료」 · complications 12개

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `id` | `/categories/9/id` | M16 |
| `name` | `/categories/9/name` | 수액치료 |

**잠정 관찰 (카테고리)**

- **OB-C09** (잠정) 카테고리 이름은 「수액치료」인데, complications 0~5 는 DCA(디옥시콜산)를 주입하는 지방분해 주사로 읽히고(출처가 KYBELLA·턱밑·바디), 6~11 은 정맥 주사·수액 이야기다. 카테고리 안에서 항목이 어느 시술에 해당하는지는 원문에 없다. → B7  
  근거: `/categories/9/complications/0/mechanism` 「DCA의 지방세포막 직접 파괴」; `/categories/9/complications/0/evidence` 「KYBELLA」; `/categories/9/complications/6/mechanism` 「모든 정맥/근육 주사에 공통」

#### `/categories/9/complications/0` — 부종·종창

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/0/name` | 부종·종창 |
| `severity` | `/categories/9/complications/0/severity` | mild |
| `incidence` | `/categories/9/complications/0/incidence` | 매우 흔함 (턱밑 임상 ~87%, 거의 필발) |
| `onset` | `/categories/9/complications/0/onset` | 주사 직후~24시간, 1-2주 지속(대용량 바디는 더 길게) |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/9/complications/0/mechanism` | DCA의 지방세포막 직접 파괴(cytolysis)로 유리된 지방·세포 잔해에 대한 예측된 국소 염증·대식세포 침윤 반응. 주입 조직이면 부위와 무관하게 발생하는 정상 반응. |
| `risk_factors` | `/categories/9/complications/0/risk_factors` | [] (빈 배열) |
| `management` | `/categories/9/complications/0/management` | 냉찜질, 안면부는 상체 거상, 압박. 대부분 1-2주 자연 소실. 통증 동반 시 NSAIDs. |
| `prevention` | `/categories/9/complications/0/prevention` | 예상 반응임을 사전 고지, 용량 분할·세션 간격 준수. CA(콜산, 뉴비쥬)는 계면활성이 낮아 부종이 상대적으로 경미하다는 보고. |
| `evidence` | `/categories/9/complications/0/evidence` | https://www.rxabbvie.com/content/dam/rxabbvie/pdf/20180205-KYBELLA-USPI-73179US10.pdf; https://hcp.mykybella.com/safety-profile |

**잠정 관찰**

- **OB-041** (잠정) 빈도에 부위(턱밑)와 근사 표기(~87%)가 있다. 비교 주장 하나가 다른 제품(CA·뉴비쥬)에 관한 것이다(「부종이 상대적으로 경미하다는 보고」). → F9  
  근거: `/categories/9/complications/0/incidence` 「턱밑 임상 ~87%」; `/categories/9/complications/0/prevention` 「CA(콜산, 뉴비쥬)는 계면활성이 낮아 부종이 상대적으로 경미하다는 보고」

#### `/categories/9/complications/1` — 통증·압통

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/1/name` | 통증·압통 |
| `severity` | `/categories/9/complications/1/severity` | mild |
| `incidence` | `/categories/9/complications/1/incidence` | 흔함 (~70%) |
| `onset` | `/categories/9/complications/1/onset` | 주사 시~시술 후 수일 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/9/complications/1/mechanism` | 주입 자체 + DCA 세포용해에 의한 국소 조직 자극·염증. 모든 주입 부위 공통. |
| `risk_factors` | `/categories/9/complications/1/risk_factors` | [] (빈 배열) |
| `management` | `/categories/9/complications/1/management` | 냉찜질, 경구 진통제. 시술 중 리도카인 혼합·국소마취로 통증 경감. |
| `prevention` | `/categories/9/complications/1/prevention` | 리도카인 혼합, 느린 주입, 부위당 용량 조절. |
| `evidence` | `/categories/9/complications/1/evidence` | https://www.rxabbvie.com/content/dam/rxabbvie/pdf/20180205-KYBELLA-USPI-73179US10.pdf |

#### `/categories/9/complications/2` — 멍·혈종

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/2/name` | 멍·혈종 |
| `severity` | `/categories/9/complications/2/severity` | mild |
| `incidence` | `/categories/9/complications/2/incidence` | 흔함 (~72%) |
| `onset` | `/categories/9/complications/2/onset` | 주사 직후~수일, 1-2주 내 소실 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/9/complications/2/mechanism` | 주삿바늘에 의한 소혈관 손상. 부위 무관 공통. 항응고·항혈소판제, 음주, 오메가3 복용 시 증가. |
| `risk_factors` | `/categories/9/complications/2/risk_factors` | [] (빈 배열) |
| `management` | `/categories/9/complications/2/management` | 냉찜질·압박, 시간 경과 소실. 필요 시 혈관 레이저. |
| `prevention` | `/categories/9/complications/2/prevention` | 시술 전 항응고·항혈소판제·오메가3·음주력 확인, 가는 바늘, 정확한 층 주입. |
| `evidence` | `/categories/9/complications/2/evidence` | https://reference.medscape.com/drug/kybella-deoxycholic-acid-999993 |

#### `/categories/9/complications/3` — 감각이상·저림 (표재 감각신경, 가역적)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/3/name` | 감각이상·저림 (표재 감각신경, 가역적) |
| `severity` | `/categories/9/complications/3/severity` | mild |
| `incidence` | `/categories/9/complications/3/incidence` | 흔함 (턱밑 ~66%; 바디는 평균 18.6일 지속 보고) |
| `onset` | `/categories/9/complications/3/onset` | 주사 후~수일, 대부분 수주 내 회복 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/9/complications/3/mechanism` | 국소 피부감각신경 분지의 일시적 부종성 압박·자극. 운동신경 손상(하악변연신경 등)과 별개인 표재 감각 변화로 모든 주입 부위 공통이며 대부분 가역적. |
| `risk_factors` | `/categories/9/complications/3/risk_factors` | [] (빈 배열) |
| `management` | `/categories/9/complications/3/management` | 경과 관찰, 대부분 수주 내 자연 회복. 지속 시 비타민B군 보조. |
| `prevention` | `/categories/9/complications/3/prevention` | 적정 깊이·용량, 표재 감각신경 밀집부 과주입 회피. (운동신경 손상은 부위별 특이 항목 참조) |
| `evidence` | `/categories/9/complications/3/evidence` | https://www.rxabbvie.com/content/dam/rxabbvie/pdf/20180205-KYBELLA-USPI-73179US10.pdf; https://pmc.ncbi.nlm.nih.gov/articles/PMC5943074/ |

**잠정 관찰**

- **OB-042** (원문 참조) incidence 칸에 다른 부위의 지속 기간이 있다(「바디는 평균 18.6일 지속 보고」). 운동신경 손상은 「부위별 특이 항목」으로 넘긴다(이 원장에 없음). → B4  
  근거: `/categories/9/complications/3/incidence` 「바디는 평균 18.6일 지속 보고」; `/categories/9/complications/3/prevention` 「운동신경 손상은 부위별 특이 항목 참조」

#### `/categories/9/complications/4` — 경결·딱딱함(일시적 섬유화)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/4/name` | 경결·딱딱함(일시적 섬유화) |
| `severity` | `/categories/9/complications/4/severity` | mild |
| `incidence` | `/categories/9/complications/4/incidence` | 흔함 (~23-30%) |
| `onset` | `/categories/9/complications/4/onset` | 1-2주경 촉지, 수주~수개월 내 소실 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/9/complications/4/mechanism` | 염증 후 일시적 섬유화·조직 경화로 만져지는 딱딱함. 치유 과정의 정상 반응, 부위 무관. (바디의 지속·대형 결절/파열은 별도 특이 항목) |
| `risk_factors` | `/categories/9/complications/4/risk_factors` | [] (빈 배열) |
| `management` | `/categories/9/complications/4/management` | 급성 부종 소실 후 온찜질·부드러운 마사지, 대부분 수개월 내 소실. |
| `prevention` | `/categories/9/complications/4/prevention` | 용량 분할, 동일 지점 과밀 주입 회피, 균등 분산. |
| `evidence` | `/categories/9/complications/4/evidence` | https://hcp.mykybella.com/safety-profile |

**잠정 관찰**

- **OB-043** (원문 참조) 바디 부위의 다른 사건(지속·대형 결절/파열)을 「별도 특이 항목」으로 넘긴다(이 원장에 없음). → B4  
  근거: `/categories/9/complications/4/mechanism` 「바디의 지속·대형 결절/파열은 별도 특이 항목」

#### `/categories/9/complications/5` — 홍반·발적·가려움

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/5/name` | 홍반·발적·가려움 |
| `severity` | `/categories/9/complications/5/severity` | mild |
| `incidence` | `/categories/9/complications/5/incidence` | 흔함 (홍반 ~27%) |
| `onset` | `/categories/9/complications/5/onset` | 주사 직후~수일 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/9/complications/5/mechanism` | 국소 염증성 혈관 확장 및 히스타민 매개 소양감. 부위 무관. |
| `risk_factors` | `/categories/9/complications/5/risk_factors` | [] (빈 배열) |
| `management` | `/categories/9/complications/5/management` | 냉찜질, 가려움 시 항히스타민제, 자연 소실. |
| `prevention` | `/categories/9/complications/5/prevention` | - |
| `evidence` | `/categories/9/complications/5/evidence` | https://www.rxabbvie.com/content/dam/rxabbvie/pdf/20180205-KYBELLA-USPI-73179US10.pdf |

**잠정 관찰**

- **OB-044** (원문 부족) prevention 값이 기호 「-」 하나다. 「없음」인지 「미작성」인지 원문으로 정할 수 없다. 형태소 분석에서는 기호 단독 값으로 제외했다. → B9  
  근거: `/categories/9/complications/5/prevention` 「-」

#### `/categories/9/complications/6` — 주사부위 반응 (통증·발적·멍·경결)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/6/name` | 주사부위 반응 (통증·발적·멍·경결) |
| `severity` | `/categories/9/complications/6/severity` | mild |
| `incidence` | `/categories/9/complications/6/incidence` | 매우 흔함 (경미, 대부분 수시간~수일 내 소실) |
| `onset` | `/categories/9/complications/6/onset` | 천자~주입 중~직후 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/9/complications/6/mechanism` | 바늘 천자·카테터 유치에 의한 국소 조직 자극과 소혈관 손상(반상출혈), 주입액의 물리적 자극. 투여 성분·적응증과 무관하게 모든 정맥/근육 주사에 공통. |
| `risk_factors` | `/categories/9/complications/6/risk_factors` | [] (빈 배열) |
| `management` | `/categories/9/complications/6/management` | 국소 냉찜질과 압박으로 대부분 자연 소실, 멍은 수일 내 흡수. 통증 지속 시 소염진통제. |
| `prevention` | `/categories/9/complications/6/prevention` | 적절한 정맥 선택과 무외상 천자, 주입 후 충분한 압박 지혈, 관절 근처 거치 회피. |
| `evidence` | `/categories/9/complications/6/evidence` | taxonomy M16 safety.common (전 제제 공통 기재); 임상 표준 주사 시술 공통 |

**잠정 관찰**

- **OB-050** (잠정) evidence 가 다른 원장의 필드와 「임상 표준」 표지를 함께 쓴다. → B6  
  근거: `/categories/9/complications/6/evidence` 「taxonomy M16 safety.common (전 제제 공통 기재)」

#### `/categories/9/complications/7` — 혈관미주신경성 반응·실신 (vasovagal)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/7/name` | 혈관미주신경성 반응·실신 (vasovagal) |
| `severity` | `/categories/9/complications/7/severity` | moderate |
| `incidence` | `/categories/9/complications/7/incidence` | 바늘·주사 시술 전반에서 흔함 (수%) |
| `onset` | `/categories/9/complications/7/onset` | 천자 중~주입 초기 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/9/complications/7/mechanism` | 통증·불안·바늘 공포에 의한 미주신경 항진 → 서맥·말초혈관 확장·혈압저하 → 뇌관류 저하로 전실신/실신. 주입 성분과 무관하게 모든 주사 시술에 공통. |
| `risk_factors` | `/categories/9/complications/7/risk_factors` | [] (빈 배열) |
| `management` | `/categories/9/complications/7/management` | 즉시 앙와위·다리 거상(Trendelenburg), 활력징후 확인, 수분 공급. 대부분 수분 내 회복. 서맥·저혈압 지속 시 관찰 연장. |
| `prevention` | `/categories/9/complications/7/prevention` | 공복·탈수 회피, 앙와위 시술, 사전 설명으로 불안 완화, 시술 중·후 관찰. |
| `evidence` | `/categories/9/complications/7/evidence` | 임상 표준 (needle-related vasovagal syncope, 주사 시술 공통) |

**잠정 관찰**

- **OB-049** (잠정) 빈도가 괄호 속 「수%」다. 숫자 자리에 「수」를 쓴 근사 표기다. → B2  
  근거: `/categories/9/complications/7/incidence` 「(수%)」

#### `/categories/9/complications/8` — 정맥염·혈관외유출(extravasation)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/8/name` | 정맥염·혈관외유출(extravasation) |
| `severity` | `/categories/9/complications/8/severity` | moderate |
| `incidence` | `/categories/9/complications/8/incidence` | 말초 IV에서 3-20% 보고 |
| `onset` | `/categories/9/complications/8/onset` | 주입 중~48시간 |
| `duration` | `/categories/9/complications/8/duration` | 수일~수주 |
| `mechanism` | `/categories/9/complications/8/mechanism` | 고삼투압·고농도·자극성 용액(고농도 비타민C·칼슘·마그네슘 등)이 혈관 내피 자극 또는 혈관외로 유출. 국소 부종·작열감·홍반·경화, 심하면 피부 괴사 |
| `risk_factors[0]` | `/categories/9/complications/8/risk_factors/0` | 고삼투압 용액 |
| `risk_factors[1]` | `/categories/9/complications/8/risk_factors/1` | 소구경 말초 IV |
| `risk_factors[2]` | `/categories/9/complications/8/risk_factors/2` | 관절 근처 거치 |
| `risk_factors[3]` | `/categories/9/complications/8/risk_factors/3` | 장시간 주입 |
| `risk_factors[4]` | `/categories/9/complications/8/risk_factors/4` | 환자 움직임 |
| `management` | `/categories/9/complications/8/management` | 즉시 주입 중단(카테터는 유지해 잔량 흡인 후 제거). 국소 냉찜질(자극성 용액) 또는 온찜질(혈관수축제)—성분별 프로토콜 확인. 고위험 유출(칼슘 글루코네이트 등) 시 국소 주사 해독제(hyaluronidase) 고려, 성형외과 협진 |
| `prevention` | `/categories/9/complications/8/prevention` | 큰 혈관 사용, 중심정맥 고려(고자극성·장기 투여 시), 주입 속도 조절, 주입 중 15-30분마다 유출 확인, 관절 부위 회피 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-045** (잠정) 처치에 성분 조건별 대안이 괄호 안에 있다(냉찜질(자극성 용액) 또는 온찜질(혈관수축제)). 앞뒤 공백 없는 `—` 뒤에 지시가 이어진다. → F3  
  근거: `/categories/9/complications/8/management` 「국소 냉찜질(자극성 용액) 또는 온찜질(혈관수축제)—성분별 프로토콜 확인」

#### `/categories/9/complications/9` — 아나필락시스·즉시형 과민반응 (일반 baseline)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/9/name` | 아나필락시스·즉시형 과민반응 (일반 baseline) |
| `severity` | `/categories/9/complications/9/severity` | critical |
| `incidence` | `/categories/9/complications/9/incidence` | 드묾. 모든 주입 성분이 baseline 위험을 가지며, 태반·단백가수분해물·글루타치온·보존제 제제에서 특히 보고 |
| `onset` | `/categories/9/complications/9/onset` | 주입 중~30분 |
| `duration` | — | (키 없음) |
| `mechanism` | `/categories/9/complications/9/mechanism` | IgE 매개 즉시형 과민반응 또는 직접 비만세포 탈과립. 어떤 정맥 투여 제제든 baseline 위험이 있어 전 시술 공통으로 응급 대비가 필요하며, 특정 고위험 성분(글루타치온·태반단백·알파리포산·티아민)에서 위험이 현저히 상승(성분별은 site_specific 참조). |
| `risk_factors` | `/categories/9/complications/9/risk_factors` | [] (빈 배열) |
| `management` | `/categories/9/complications/9/management` | 즉시 투여 중단, 에피네프린 0.3-0.5mg IM(대퇴부 전외측), 기도 확보·산소, 항히스타민제, 하이드로코르티손 100-200mg IV, 119 이송. 이원성(biphasic) 반응 대비 4-6시간 관찰. |
| `prevention` | `/categories/9/complications/9/prevention` | 시술 전 알러지·아나필락시스 병력 확인, 첫 투여 시 속도 1/2 감속·초기 15분 밀착 관찰, 에피네프린 자동주사기·소생 장비 상비, 신규 성분은 소량 선행 투여. |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-046** (원문 참조) 이름의 「일반 baseline」과 mechanism 의 「성분별은 site_specific 참조」는 성분별 항목이 따로 있다는 뜻으로 읽힌다(잠정). 그 항목은 이 원장에 없다. prevention 에 분수 「1/2」(속도 감속)가 있다. → B4  
  근거: `/categories/9/complications/9/mechanism` 「성분별은 site_specific 참조」; `/categories/9/complications/9/prevention` 「첫 투여 시 속도 1/2 감속」

#### `/categories/9/complications/10` — 공기색전·카테터 관련 감염

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/10/name` | 공기색전·카테터 관련 감염 |
| `severity` | `/categories/9/complications/10/severity` | severe |
| `incidence` | `/categories/9/complications/10/incidence` | 드물지만 치명적 가능 |
| `onset` | `/categories/9/complications/10/onset` | 주입 중(공기색전) / 24-72시간(감염) |
| `duration` | `/categories/9/complications/10/duration` | 즉시 치료 필요 |
| `mechanism` | `/categories/9/complications/10/mechanism` | 공기색전: 공기 50mL 이상이 정맥 내 유입 시 폐순환 장애. 감염: 무균술기 위반 시 정맥염·균혈증·패혈증. 반복 시술 시 카테터 관련 혈류감염 |
| `risk_factors[0]` | `/categories/9/complications/10/risk_factors/0` | 개방형 수액 세트 |
| `risk_factors[1]` | `/categories/9/complications/10/risk_factors/1` | 중심정맥관 |
| `risk_factors[2]` | `/categories/9/complications/10/risk_factors/2` | 손 위생 불량·무균술기 위반 |
| `risk_factors[3]` | `/categories/9/complications/10/risk_factors/3` | 면역저하 |
| `management` | `/categories/9/complications/10/management` | 공기색전 의심 시 좌측 와위·Trendelenburg 자세, 산소 100%, 응급실. 감염 의심 시 혈액배양 2쌍, 경험적 항생제(세파졸린±반코마이신), 카테터 제거 및 첨단 배양 |
| `prevention` | `/categories/9/complications/10/prevention` | 폐쇄형 IV 세트 사용, 공기 제거 철저, 손 위생·알코올 소독·멸균 장갑, 접근부 클로르헥시딘 2% 알코올 소독, 같은 부위 24-72시간 이상 카테터 거치 금지 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-047** (잠정) 사건 두 개를 한 항목에 묶었고, onset 도 `/` 로 사건마다 나눴다. mechanism 에 양의 문턱이 있다(「공기 50mL 이상」). → P3  
  근거: `/categories/9/complications/10/onset` 「주입 중(공기색전) / 24-72시간(감염)」; `/categories/9/complications/10/mechanism` 「공기 50mL 이상이 정맥 내 유입 시」

#### `/categories/9/complications/11` — 수분·전해질 과부하 (심부전·신부전)

| 원본 컬럼명 | Pointer | 원문 값 |
|---|---|---|
| `name` | `/categories/9/complications/11/name` | 수분·전해질 과부하 (심부전·신부전) |
| `severity` | `/categories/9/complications/11/severity` | severe |
| `incidence` | `/categories/9/complications/11/incidence` | 기저 심부전·신부전 환자에 한해 임상적으로 의미 |
| `onset` | `/categories/9/complications/11/onset` | 주입 중~수 시간 |
| `duration` | `/categories/9/complications/11/duration` | 이뇨·입원 치료 필요 가능 |
| `mechanism` | `/categories/9/complications/11/mechanism` | 단시간 대량 수액 투여가 전부하를 급격히 증가시켜 폐울혈·폐부종 유발. 신부전에서는 칼륨·마그네슘·인 배설 저하로 부정맥 위험 |
| `risk_factors[0]` | `/categories/9/complications/11/risk_factors/0` | 심부전(EF 감소) |
| `risk_factors[1]` | `/categories/9/complications/11/risk_factors/1` | 만성 신부전(eGFR<30) |
| `risk_factors[2]` | `/categories/9/complications/11/risk_factors/2` | 고령·체중 저체중 |
| `risk_factors[3]` | `/categories/9/complications/11/risk_factors/3` | 빠른 주입 속도 |
| `risk_factors[4]` | `/categories/9/complications/11/risk_factors/4` | 고장성 용액 |
| `management` | `/categories/9/complications/11/management` | 주입 중단, 상체 거상, 산소·이뇨제(furosemide), 필요 시 중환자 모니터링, 심전도·산소포화도 감시 |
| `prevention` | `/categories/9/complications/11/prevention` | 시술 전 심폐·신기능 문진 및 검사, 용량·속도 보수적 설정(고위험군 100-125mL/h), 고장성 성분 희석, 증상 발생 즉시 중단 |
| `evidence` | — | (키 없음) |

**잠정 관찰**

- **OB-048** (잠정) 빈도 칸이 모집단 한정이다(「기저 심부전·신부전 환자에 한해 임상적으로 의미」). 수치 문턱(eGFR<30, 100-125mL/h)이 있다. → F6  
  근거: `/categories/9/complications/11/incidence` 「기저 심부전·신부전 환자에 한해 임상적으로 의미」; `/categories/9/complications/11/risk_factors/1` 「eGFR<30」; `/categories/9/complications/11/prevention` 「고위험군 100-125mL/h」

