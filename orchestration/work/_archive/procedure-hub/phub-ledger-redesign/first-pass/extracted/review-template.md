# extracted.json — 1차 조사 (읽기용)

> **1차 범위: 종료 기준 충족(작성자 자체 판정 · 독립 검토 전 · 코디 확인 전).** **원장 전체 완료 아님** — 열린 미결은 [issues.md](./issues.md)에 있다(원문 부족 B 10 · 원문 내 불일치 I 13 · 잠정 P 4 · 후속 의미 조사 F 11 · 알려진 분석 한계 K 5 · 에이전트 오류 A 3(해결) · 사용자 결정 필요 C 0).
>
> 이 문서는 상태·전체 컬럼 구성·구획 목차를 갖는다. **모든 값은 구획별 `review-part-*.md`** 에 원본 컬럼명·JSON Pointer·자료형·원문 값으로 실려 있고, 잠정 관찰은 각 파일의 별도 절에 있다. 원문 칸과 관찰 칸을 섞지 않는다. 원문의 임상·법적 주장은 **원장에 그렇게 적혀 있다**는 사실로만 기록했다. 사실 여부는 검증하지 않았고 외부 자료로 보충하지 않았다. 공통 개념 ID·동의어·부위 체계·관계 방향은 정하지 않았다(1차 범위 밖).

## 상태

| 구분 | 상태 |
|---|---|
| 1차 범위 종료 | **충족(자체 판정)** — 전 구획 직접 읽기·구조/값 대응·형태소·표현 수집·기계 검증 통과. 독립 읽기 검토는 받지 않았다 |
| 원장 전체 완료 | **아님** — B·I·P·F 미결과 의미 분해·정규화가 남아 있다 |
| 전수 읽기 | 구획 18개(S00 루트 + 항목 17) 전부 직접 읽음. 항목마다 3회(통독 · 값별 표지 기록 · 형태소 대조). [coverage.json](./coverage.json) · [reading-log.json](./reading-log.json) |
| 구조·값 수집 | 노드 {{NODES}} 전부 · 키 출현 {{KEYOCC}} (서로 다른 키 {{DKEYS}}) · {{BYTYPE}} · 말단 {{LEAVES}} · 빈 값 {{EMPTY}}(null) · 중복 키 0 · 이스케이프 0 |
| 형태소·표현 수집 | Kiwi 0.24.1(cong, 스레드 1, 사용자 사전 없음) — 분석 {{ANALYZED}}값 {{TOKENS}}토큰 · 제외 {{EXCLUDED}} 말단(사유별) · 필드명 {{FIELDN}} · 알려진 오분절·오태깅 표시 {{SEGMARKS}}출현(**교정 아님**) · 표현 후보 {{EXPRS}}(수동 {{MANUALEXPR}} 포함) |
| 기계 검증 | [validation.md](./validation.md) — verify.py 실패 0 · 원본 해시 시작·끝 동일 · 변이 시험 검출 |
| 읽기 검토 | 작성자 3회차까지. 독립 검토자 아님 |
| 알려진 분석 오류 | issues K1~K5 (형태소 표시 {{SEGMARKS}}출현 · NNP 과다 태깅 미표시 · 규칙 후보 오탐 미판정 등) |
| 열린 미결 | B 10 · I 13 · P 4 · F 11 · C 0 — [issues.md](./issues.md) |
| 후속 의미 조사 | 시작 안 함 |
| 마지막 읽은 위치 | {{LASTREAD}} |

## 0. 원본과 기록 위치

| 항목 | 값 |
|---|---|
| 원본 | `orchestration/work/phub-recommend/bronze/phub-ledger/extracted.json` (읽기 전용) |
| 크기 | {{BYTES}} bytes · {{CP}} code points · UTF-8 · BOM 없음 · 개행 없는 한 줄 · 이스케이프 0 · BMP 밖 문자 0 · `\|` 0 |
| sha256 | `{{SHA}}` (작업 시작·끝 동일) |
| 구조·값 | [source-map.json](./source-map.json) — 모든 노드(Pointer·자료형·값·리터럴·코드 포인트/바이트 구간·키 구간·문맥 참조·구획) · 필드명 출현 위치 |
| 구획 대응 | [coverage.json](./coverage.json) — 구획별 소유 Pointer 집합·말단·문맥 참조·읽기 상태·review 파일 |
| 형태소 | [morphology.json](./morphology.json) — 분석·제외·필드명·알려진 오분절 표시(원본 [segmentation-review.json](./segmentation-review.json)) |
| 복합 표현 | [expressions.json](./expressions.json) — 규칙 후보 + 수동 구절(원본 [manual-expressions.json](./manual-expressions.json)) |
| 잠정 관찰 | 각 `review-part-*.md` §2 (원본 [manual-observations.json](./manual-observations.json), {{OBS}}건) |
| 미결 · 검증 | [issues.md](./issues.md) · [validation.md](./validation.md) |
| 재현 | [build.py](./build.py)(`uv run --python 3.12 --with kiwipiepy==0.24.1 python …/build.py`) · [verify.py](./verify.py)(`python3 …/verify.py`) |

구간 기준: 디코딩된 원문 문자열의 Unicode 코드 포인트 `[start,end)`. source-map 의 `span` 은 파일 전체 텍스트 기준(따옴표 포함 리터럴), `value_span` 은 따옴표 안쪽, `byte_span` 은 UTF-8 바이트다. morphology·expressions 의 `span` 은 그 값 문자열 기준이다(파일 위치 = `value_span[0] + start`). 이스케이프가 없어 디코딩 문자열과 리터럴 안쪽이 글자 단위로 같다(`decoded_equals_literal_inner`).

## 1. 읽기 범위와 구획

**구획 분할:** 원장은 최상위 객체 하나에 시술 항목 17개다. 항목 하나가 1,256~2,165자로 한 번에 전부 읽을 수 있어 **항목 하나 = 구획 하나**로 정했다(문장 중간 자르기 없음). S00 은 루트 객체 노드만 소유하고, 항목 구획은 루트를 문맥으로 참조만 한다. 각 항목의 `name`·`procedure_id` 는 그 구획이 소유하면서 구획 안 모든 값의 문맥으로 참조한다.

| 회차 | 범위 | 방식 |
|---|---|---|
| 1 | 전 구획 | 항목 객체를 키 순서대로 출력해 2~3개 항목씩 순차로 위에서 아래로 읽음(묶음 6회) |
| 2 | 전 구획 | 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조·하위 유형·근거 표지를 원문 인용으로 기록(수동 표현 {{MANUALEXPR}} · 관찰 {{OBS}}) |
| 3 | 분석 대상 전부 | 의심 품사(NNP·NR·MM·NP·MAJ·XR·SW·W_SERIAL·불규칙 활용 태그 등) 전 출현과 전문어·부위어·부작용어·부정/가능성 표지 약 170개 낱말의 모든 출현을 원문 어절과 대조 → 오분절 규칙 20 · 출현 {{SEGMARKS}} |

- **자동 처리:** 구조 열거 · Pointer · 구간 · 해시 · 형태소 분석 · regex/keyword 후보 · 수동 인용 위치 찾기 · coverage 생성.
- **직접 읽기:** 위 세 회차. 3회차 범위 밖 토큰의 정확성은 보장하지 않는다.
- **한계:** 「별도 읽기 검토」는 같은 작성자가 관점을 바꿔 다시 읽은 것이다.

### 구획 목차

| 구획 | 항목 | 소유 Pointer | 노드 수 | 직접 읽기 | 값·관찰 위치 |
|---|---|---|---|---|---|
{{TOC}}

### S00 루트

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 |
|---|---|---|---|---|
| 1 | (루트) | `""` | object | (object · 17) — 키: M10, M11, M12, M13, M14, M15, M16, M17, M1, M2, M3, M4, M5, M6, M7, M8, M9 |

## 2. 구조 — 원문 대응

### 2.1 컬럼 구성 표

`<항목 키>` 는 최상위 키(M1~M17)다. 「출현」은 노드 수, 「항목」은 그 경로가 있는 항목이다. 원문 예시가 길면 80자에서 끊었고 전체 값은 구획 파일에 있다.

| 원본 컬럼명(경로 패턴) | JSON Pointer 패턴 | 자료형 | 중첩 구조 | 출현 | 항목 | 원문 예시 | 예시 위치 |
|---|---|---|---|---|---|---|---|
{{COLROWS}}

### 2.2 객체 키 구성 변형

| 경로 패턴 | 키 수 | 키(원문 순서) | 객체 수 | Pointer |
|---|---|---|---|---|
{{KSROWS}}

### 2.3 형태소 분석 적용·제외

| 대상 | 처리 | 사유 |
|---|---|---|
| name · overview · mechanism · source · safety/* · aftercare/* · indications/* · onset_duration/* · contraindications/* · related_techniques/* | 분석 | 언어 텍스트 |
| name_en 17 | 분석(원시 결과만) | 영문 시술명. Kiwi 는 SL 토큰을 준다 — 영어 형태 분석이 아니다(K4) |
| procedure_id 17 | 제외 | 코드값(Mxx-영문 대문자) |
| extracted_at 17 · updated 1 | 제외 | 날짜값 |
| guardrail_version 17 | 제외 | 버전 문자열 |
| source_type 17 | 제외 | 열거 코드값(kr/general/us) |
| safety/serious = null 2 | 제외 | 문자열 아님(값 보존) |
| 필드명 | 분석(별도) | 영문 식별자·항목 키. Kiwi 결과와 `_` 분할을 함께 남기며 뜻은 정하지 않음 |

표현 후보 범주별 수: {{CATS}}. 범주는 탐색용 후보이며 분류가 확정된 것이 아니다. 같은 구간이 여러 범주에 겹치는 것은 의도했고, 같은 (Pointer, 구간, 범주) 중복 생성은 0 이다. 규칙은 원문 문자열에 직접 적용했고 형태소 품사를 쓰지 않았다(형태소 오분절이 표현 후보로 옮겨 가지 않는다). `cross_reference_name` 은 이 원장 `/Mx/name` 값·약칭과 같은 문자열일 뿐 관계 확정이 아니다.

## 3. 전역 잠정 관찰 (원문과 분리)

분류 문자: 구조 = 원장 구조 사실 · P 잠정 · B 원문 정보 부족 · F 후속 의미 조사 · I 원문 내 불일치 · K 분석 한계. 항목별 관찰은 각 구획 파일 §2 에 있다.

{{GLOBALOBS}}
