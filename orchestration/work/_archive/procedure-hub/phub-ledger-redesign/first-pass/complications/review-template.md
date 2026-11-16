# complications.json — 1차 조사 (읽기용)

> **1차 범위: 종료 기준 충족(작성자 자체 판정 · batch-01 독립 묶음 검토 WARN — 1차 종료를 막지 않음 · 코디 확인 전).** **원장 전체 완료 아님** — 열린 미결은 [issues.md](./issues.md)에 있다(원문 부족 B 9 · 잠정 P 4 · 후속 의미 조사 F 9 · 분석 한계 A 4 · 사용자 결정 필요 C 0).
>
> 이 문서는 **원문 값**과 **잠정 관찰**을 다른 칸·다른 절에 나눠 적는다. 표의 「원문 값」 칸은 원장 문자열 그대로다(마크다운 표 때문에 `|` 만 `\|` 로 바꿨는데, 이 원장에는 `|` 가 없다). 「잠정 관찰」은 근거 Pointer 를 붙인 해석 후보이며 확정된 의미·관계가 아니다. 공통 개념 ID·동의어·부위 체계·관계 방향은 정하지 않았다(1차 범위 밖).
> 원문의 임상·법적 주장은 **원장에 그렇게 적혀 있다**는 사실로만 기록했다. 사실 여부는 검증하지 않았고 외부 자료로 보충하지 않았다.

## 상태

| 구분 | 상태 |
|---|---|
| 전수 읽기 | 상위 2키 · 카테고리 10 · 부작용 항목 65 · 모든 값. 작성자가 3회 읽음(§1). 독립 검토자는 없음 |
| 구조·값 수집 | 노드 {{NODES}}/{{NODES}} · 키 출현 {{KEYS}} · 문자열 {{NSTR}} · 중복 키 0 · 이스케이프 0 |
| 형태소·표현 수집 | Kiwi 0.24.1(cong, 스레드 1) — 분석 {{NVAL}}값 {{NTOK}}토큰 · 제외 {{NEXC}}값(사유별) · 필드명 18 · 오분절·오태깅 표시 {{NSEG}}출현(57규칙, **교정 아님**) · 표현 후보 {{NEXPR}}(수동 {{NMAN}} 포함) |
| 기계 검증 | [validation.md](./validation.md) — verify.py failure 0, 원본 해시 시작·끝 동일, 변이 시험 검출 |
| 읽기 검토 | 작성자 3회차(미포착 어절 열람)로 수식 표지 보강. 독립 읽기 검토 아님 |
| 알려진 분석 오류 | 오분절 {{NSEG}}출현 표시(issues A1). 표시하지 않은 토큰의 정확성은 보장하지 않음. 표현 후보의 keyword 오탐은 판정하지 않음(A2). 독립 검토가 찾은 미표시 오분절 2출현(「시술」·「전층」, 미교정)·「삽입 깊이」 구절 후보 한계·같은 구간 57쌍은 issues 「A 보충」에 위치 기록 |
| 열린 미결 | B 9 · P 4 · F 9 · C 0 — [issues.md](./issues.md) |
| 후속 의미 조사 | 시작 안 함 |

## 0. 원본과 기록 위치

| 항목 | 값 |
|---|---|
| 원본 | `orchestration/work/phub-recommend/bronze/phub-ledger/complications.json` |
| 크기 | {{BYTES}} bytes · {{CP}} code points · UTF-8 · BOM 없음 · 개행 없는 한 줄 · 이스케이프 0 · BMP 밖 문자 0 |
| sha256 | `{{SHA}}` (작업 시작·끝 동일) |
| 구조·값 | [source-map.json](./source-map.json) — 노드 {{NODES}}개(전부) · 키 출현 {{KEYS}}개 · 필드명 출현 위치 |
| 형태소 | [morphology.json](./morphology.json) — 분석 {{NVAL}}값 · 제외 {{NEXC}}값 · 필드명 18 · 오분절 규칙 57·출현 {{NSEG}} (규칙 원본 [segmentation-review-rules.json](./segmentation-review-rules.json)) |
| 복합 표현 | [expressions.json](./expressions.json) — 후보 {{NEXPR}} · 수동 구절 원본 [manual-expressions.json](./manual-expressions.json) |
| 잠정 관찰 | 이 문서 §3·§4 (원본 [manual-observations.json](./manual-observations.json), {{NOBS}}건) |
| 미결 · 검증 | [issues.md](./issues.md) · [validation.md](./validation.md) |
| 재현 | [build.py](./build.py)(`uv run --python 3.12 --with kiwipiepy==0.24.1 python …/build.py`) · [verify.py](./verify.py)(`python3 …/verify.py`) · [build-output.txt](./build-output.txt) |

구간 기준: 디코딩된 원문 문자열의 Unicode 코드 포인트 `[start,end)`. source-map 의 `span` 은 파일 전체 텍스트 기준이고, morphology·expressions 의 `span` 은 그 값 문자열 기준이다(파일 위치 = `file_span_of_text[0] + start`). 바이트 구간은 `byte_span` 에 따로 둔다. 이스케이프가 없어 디코딩 문자열과 JSON 리터럴 안쪽이 글자 단위로 같다(source-map `decoded_equals_literal_inner`). 따옴표 포함 리터럴 구간은 `span`, 따옴표 안쪽은 `value_span` 이다.

## 1. 읽기 범위 (실제로 한 일)

| 회차 | 범위 | 방식 |
|---|---|---|
| 1 | `/severity_levels` 4값 → `/categories/0` ~ `/categories/9` 의 id·name·complications 65항목 전 필드(빈 배열·없는 키 포함) | 카테고리 순서대로 항목별 전 필드를 출력해 위에서 아래로 직접 읽음(0~2 · 3~5 · 6~9 세 구획) |
| 2 | 같은 전체 | 값마다 다시 읽으며 조건·부정·가능성·범위·시간·참조·하위집단·근거 표지를 골라 manual-observations({{NOBS}}) · manual-expressions(189)에 원문 인용으로 적음. build 가 인용이 실제 값 안에 있는지 검사 |
| 3 | 분석 대상 531값 | (a) 의심 품사(NNP 일부·NR·MM·NP·MAJ·MAG 일부·VA/VV 일부·NNB 일부·붙은 SL)와 시간·부정·가능성·용어 낱말의 출현을 원문 어절과 나란히 놓고 하나씩 대조 → 오분절 규칙 57. (b) 표현 후보가 하나도 걸리지 않은 어절 2,331개를 값마다 읽음 → 빠진 수식 표지(필요시·가는·어려워·달리·우선·기존 등)를 keyword 규칙에 보강하고, 남은 어절은 사건·행위·재료·부위 같은 내용어임을 확인 |

- **자동 처리:** 구조 열거 · Pointer · 구간 · 해시 · 형태소 분석 · regex/keyword 후보 추출 · 수동 구절 위치 찾기.
- **직접 읽기:** 위 세 회차. 형태소 9천여 토큰을 하나하나 정답 대조하지는 않았다. 3(a) 범위 밖 토큰의 정확성은 보장하지 않는다.
- **한계:** 「별도 읽기 검토」는 같은 작성자가 관점을 바꿔 다시 읽은 것이다. 독립 검토자가 아니다.

## 2. 구조 — 원문 대응

### 2.1 컬럼 구성 표

최상위 객체의 키는 2개이며 순서는 `severity_levels` → `categories` 다. 숫자·불리언·null·빈 문자열·빈 객체는 없다. 빈 값은 빈 배열(`risk_factors` = [])과 기호 단독 값(`"-"`)뿐이다.

{{COLUMN_TABLE}}

### 2.2 항목 객체의 키 순서 변형

필드 순서는 원문 그대로다. `duration` 은 있을 때 `onset` 바로 뒤에, `evidence` 는 있을 때 맨 끝에 온다.

{{ORDER_TABLE}}

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

표현 후보 범주별 수: {{EXPR_COUNTS}}. 범주는 탐색용 후보일 뿐 분류가 확정된 것이 아니다. 같은 구간이 여러 범주에 겹치는 것은 의도한 것이다. 표현 추출은 원문 문자열에 regex·keyword 를 직접 적용했고 형태소 품사를 쓰지 않았다. 그래서 형태소 오분절이 표현 후보로 옮겨 가지 않는다.

## 3. 전역 잠정 관찰

{{TOP_OBS}}

## 4. 항목별 값 — 원본 컬럼명 그대로

각 표는 원문 값만 담는다. 「(키 없음)」은 그 항목에 키 자체가 없다는 뜻이고, 「[] (빈 배열)」은 키는 있는데 배열이 비었다는 뜻이다. 배열 항목은 원본 순서를 지키고 행마다 Pointer 를 붙였다. 잠정 관찰은 표 아래 따로 둔다.

{{ITEMS}}
