# batch-04 독립 검토 — market-pricing · patient-education · post-procedure-timeline · pre-procedure-checklist · treatment-optimization

- 검토: 독립 Opus 검토 워커(reviewer_doc) · `task_a7c05182eefe` / `ctx_74658d7aed89` · 2026-11-09
- 기준: [1차 조사 스킬](./ledger-first-pass/SKILL.md)의 산출물 계약·종료 기준, [재개 노트](./_RESUME.md), [발주 기록](./batch-04-dispatches.json), [검토 브리프](./batch-04-review-brief.md)
- 범위: 위 다섯 원장만 봤다. 다른 원장은 열지 않았다. 원본·결과·스킬·재개 노트·발주 기록·다른 리뷰는 고치지 않았다. 공유 트리에 새로 만든 파일은 이 보고서 하나다. 독립 대조 스크립트는 세션 스크래치패드에만 있다.
- 이 검토는 **1차 수집 계약을 지켰는지**만 본다. 최종 의미 조사, 정규화, 임상·법적 사실 검증, 형태소 전체 정답 판정은 하지 않았다.

## 0. 결론

| 원장 | 판정 | 1차 범위 종료 | 원장 전체 | 반드시 고칠 추출 오류 |
|---|---|---|---|---|
| market-pricing | **PASS** (분류 비고 1) | 가능 | 완료 아님 | 0 |
| patient-education | **PASS** | 가능 | 완료 아님 | 0 |
| post-procedure-timeline | **PASS** (운영 사고 비고 1 · 분류 비고 1) | 가능 | 완료 아님 | 0 |
| pre-procedure-checklist | **WARN** (기록 형식 보완. 종료를 막지 않음) | 가능 | 완료 아님 | 0 — 알려진 오분절 44건에 문자구간이 없다(§2.4) |
| treatment-optimization | **WARN** (분류 보완. 종료를 막지 않음) | 가능 | 완료 아님 | 0 — I-10-1·I-10-2·I-10-4 가 양립할 수 있는 진술을 불일치 후보로 분류했다(§2.5) |

다섯 원장 모두에서 다음은 **찾지 못했다**: 원문 누락, 원문 변형, 잘못된 Pointer, 잘못된 문자구간·바이트구간, 자료형 변형, 키 리터럴 구간 오류, 구획 소유 누락·중복, 형태소 적용·제외 누락, 표현 구간 재현 실패, 분할 문서 행의 원문 불일치. 그래서 **종료를 막는 수정 요청은 0건**이다.

WARN 두 건은 기록 보완 권고다. 재조사는 필요 없다.

- checklist: 오분절 기록에 Pointer·표면형만 있고 구간이 없다. 44건 모두 해당 값 안에서 표면형이 한 번만 나와 위치는 특정된다. 그래서 구간 필드만 채우면 된다.
- treatment-optimization: 불일치로 확정하지는 않았다(「후보」「판정하지 않음」으로 적었다). 다만 I 로 분류해 두면 후속 단계에서 모순으로 읽힐 수 있다. 분류를 P/F 로 옮기거나 「양립 가능, 경계 구간 미정」 비고를 다는 것으로 충분하다.

원장 전체 완료는 다섯 원장 모두 **아니다**. 각 `issues.md` 의 B·I·P·F·K 가 열려 있다. 의미 분해·공통 개념 연결·정규화는 시작하지 않았다.

**지금 필요한 사용자 선택: 0건.** 근거는 §4.

## 1. 검토 방법과 범위 (자동 / 전수 / 표본 구분)

### 1.1 원본 해시와 기존 verify.py 재실행 — 자동, 읽기 전용

작업 디렉토리 `first-pass/` 에서 `python3 <원장>/verify.py` 를 실행했다. 기본 python3 3.14 를 썼고 kiwipiepy 는 없다. 형태소를 다시 분석하지 않고, 기록된 토큰을 원문과 대조했다.

| 원장 | 원본 sha256 (발주 기록과 일치) | bytes | `verify.py` 실제 출력 |
|---|---|---|---|
| market-pricing | `601d7e7b4db29731bf15304ff3ec9489ba38838e9f5ba2144c2c181cfd15e477` | 12,214 | exit 0 · checks 11930 · failures 0 · nodes 806 · 말단 648 · segments 18 · morph 적용 262 / 제외 20 · tokens 988 · auto 348 · manual 250 · issues 57 · 시작·끝 해시 동일 |
| patient-education | `6c96520c514b76ef7f93d7f685e53023afe91b05133a9b9ca5db0a95d42d91ac` | 26,551 | exit 0 · checks 34232 · failures 0 · nodes 327 · 말단 240 · segments 18 · 적용 221 / 제외 19 · tokens 4989 · expressions 806 · regex 572 · 오분절 25 · 시작·끝 해시 동일 |
| post-procedure-timeline | `d04c9fe494acd318d656f6dea6d19e33cb944a20440e312ca9bad41309c9742e` | 20,081 | exit 0 · checks 27804(66종) · failure_count 0 · pointers 796 · 말단 558 · segments 11 |
| pre-procedure-checklist | `0de87bff91f721fe685884025d31749017d44da250492b2db9d49109a61e4086` | 14,569 | exit 0 · checks 14697 · failures 0 · nodes 503 · 말단 331 · 적용 165 / 제외 166 · auto 425 · manual 188 · 오분절 44 · info: 수동 표현 없는 분석 대상 값 19 · 시작·끝 해시 동일 |
| treatment-optimization | `07b9ebe0a843280b4eef9487590951932192435ea46284aba425338ab9d9767b` | 22,887 | exit 0 · checks 140 · failures 0 · nodes 691 · 말단 502 · tokens 3025 · expressions 1758 · 시작·끝 해시 동일 |

- 다섯 결과 폴더 194개 파일의 sha256 을 실행 전후로 비교했다. 정렬 후 diff 는 0 이다. verify.py 는 아무것도 쓰지 않았다.
- 원본 5개의 sha256 은 실행 전후 모두 위 값과 같다.

### 1.2 독립 기계 대조 — 전수 (다섯 원장 모두)

verify.py 를 재사용하지 않았다. 스크래치패드에 문자 단위 JSON 스캐너를 새로 짰다. 이 스캐너는 중복 키, Pointer, 리터럴 cp 구간, UTF-8 바이트 구간, 값 cp 구간(따옴표 제외), 키 리터럴 구간을 독립적으로 계산한다. 그 결과를 원장마다 다른 스키마에 맞춰 대조했다.

| 대조 | 방법 | 결과 |
|---|---|---|
| 노드 집합·순서 | 전체 경로(컨테이너·말단·빈 컨테이너)를 source-map `nodes` 와 순서까지 비교 | 5/5 누락 0 · 불필요 0 · 순서 일치 (806 · 327 · 796 · 503 · 691) |
| 자료형·값 | 말단마다 자료형과 값(파이썬 타입까지) 비교. 리터럴 cp·바이트 구간, 문자열 값 cp 구간, 리터럴 원문 비교 | 5/5 불일치 0 |
| 키 | 키 리터럴의 cp·바이트 구간과 순서 | 5/5 불일치 0 (666 · 258 · 307 · 350 · 388) |
| 중복 키·이스케이프 | 스캐너 감지 | 5/5 중복 키 0 · 이스케이프 0 — 각 기록과 일치 |
| 빈 컨테이너 | 빈 배열·객체·빈 문자열·null 집합 | treatment-optimization 빈 배열 11(`/by_concern/*/severity_levels/*/contraindicated_combos`), 나머지 0 — 기록과 일치. 11개 모두 review-part 행에 `[]` 로 있다 |
| 구획 소유 | 소유 Pointer 합집합 = 전체 노드, 다중 소유 0. 소유 말단 = 전체 말단 | 5/5 누락·초과·중복 0. 읽기 상태 전 구획 직접 읽음(18 · 18 · 11 · 6 · 14) |
| 형태소 적용/제외 | 적용 ∪ 제외 = 문자열 말단, 겹침 0, 제외마다 사유. 토큰마다 `value[start:end] == surface`. 파일 cp 를 기록한 원장은 그 값도 비교 | 5/5 불일치 0 · 토큰 988 / 4989 / 3078 / 1511 / 3025 · 길이 0 토큰 market-pricing 2 · patient-education 9 |
| 표현 | 모든 표현(수동·정규식·값 전체·절)의 `value[span] == text`, 파일 cp 재현, `full_value`/`context_value` = 원문 | 5/5 불일치 0 (598 · 1378 · 2291 · 613 · 1758) |
| 표현 중복 | (Pointer, 구간, 출처, 패턴, 원문) 기준 | 5/5 정확 중복 0. treatment-optimization 의 같은 구간 11쌍은 패턴이 다르고 id 가 유일하다(예: `/by_concern/2/severity_levels/2/sequence` [5,7) 「or」 의 R07·R20) — 의도된 겹침 |
| 알려진 오분절 기록 | 기록된 출현 구간의 원문 = 기록 표면형 | 4/5 불일치 0 (21 · 25 · 76 · 77). checklist 44건은 구간이 없어 구간 대조 불가 → §2.4 |
| 분할 문서 원문 대응 | 말단마다 소유 구획 review-part 의 `` `Pointer` `` 가 있는 **같은 행**에 원문 값이 있는지. market-pricing 은 항목당 한 행 표(`name·unit·low·mid·high`)라 122행의 열 6개를 원문과 정확 비교 | 5/5 행 불일치 0 (648 · 240 · 558 · 331 · 502) |

자동 대조로 확인한 것은 **원문 ↔ 기록 대응**뿐이다. 이 대조는 의미 해석의 정답을 보장하지 않는다.

### 1.3 독립 읽기 — 표본 + 단서 정규식 보조

- **직접 원문과 대조해 읽은 범위(표본)**
  - market-pricing: 원문 전체의 `name`·`unit` 122쌍과 루트 4값. `low<mid<high` 122/122, `mid = (low+high)/2` 3/122, unit `1회` 87 을 직접 다시 셌다(P-X-3·review.md 와 일치). review-part-S01 전체를 읽었다.
  - patient-education: 정규식 후보 중 `covered_by_sentence_only` 49건의 원문과 판정 메모를 대조했다.
  - post-procedure-timeline: `/reaction_levels` 전체, `/timelines/0`(botox) 전체, manual/S01.txt 앞부분. 그리고 `/timelines/0/phases/0/normal/0`·`/abnormal/0`·`/caution/0`, `/timelines/3/phases/1/normal/2`, `/timelines/5/phases/1/abnormal/1`, `/timelines/7/phases/1/normal/0`, `/timelines/9/phases/0/normal/3` 의 표현 전부를 읽었다.
  - pre-procedure-checklist: `/universal_checks` 12항목 전체, `/category_specific/0~3` 전체. 수동 표현이 없는 19값 중 6값을 읽었다. 금기·type 관련 기록(B-G-1 · P-S04-4 · P-S05-4 · F-S02-5 · F-G-2 · I-S01-5 · K-S05-6)과 review-part-S05 의 해당 행도 읽었다.
  - treatment-optimization: `/combination_rules` 8개 전체, `/by_concern/0|1|4|6` 의 해당 단계, `/by_age_group/0|1/maintenance`, `/annual_plans/0/schedule`. I-10-1~4·I-11-1 의 근거와 대조했다. `/combination_rules/0/detail`·`/3/*`·`/6/detail`, `/by_concern/0/severity_levels/2/sequence`, `/by_age_group/0/avoid/0` 의 수동 구절도 읽었다.
  - 다섯 원장의 issues.md 는 전문을 읽었다. review.md·validation.md·progress.md 는 상태 표와 범위 주장 부분을 읽었다.
- **단서 정규식 보조(전수 의미 조사 아님)**: 부정·가능성·권고/회피·비교/범위·근사·정도·깊이/두께·속도·지속·후/시/전/내 조건·동일일 단서 정규식을 형태소 적용 값에서 찾았다. 그 구간이 표현 구간 안에 들어가는지만 셌다. 이 수치는 **누락 후보를 찾는 보조 지표**이며 의미 판정이 아니다. 「문장/값 전체」 표현은 따로 빼고 셌다.

| 원장 | 단서 일치 | 하위 구절(문장·값 전체 제외) 밖 | 읽어 본 판정 |
|---|---|---|---|
| market-pricing | 4 | 0 (수동+자동) | — |
| pre-procedure-checklist | 111 | 0 (수동만으로도 0) | — |
| treatment-optimization | 278 | 수동만 37 · 수동+정규식 6 | 6건 모두 오탐(「미백약」의 약, 「RF/HIFU 시」 는 수동 구절 끝 경계와 단서의 공백 차이, 「다만」 류) |
| post-procedure-timeline | 322 | 수동 하위 구절+자동 19 | 19건 모두 오탐(「징후」의 후, 「완전」의 전 등). 실제 시간·조건 구절(「24-48시간 내」「연하 시」「시술 후」「2) 후」)은 자동 후보와 값 전체 수동 구절에 있다 |
| patient-education | 문장 제외 수동 구절 밖 55 | 문장 기록까지 포함하면 0 | 약 절반은 오탐(「다만」「내 피」「동시에」「운동시켜」). 나머지는 짧은 의문·답변 문장의 부정·가능성·후 조건이다. 작업자가 regex-review 에 `covered_by_sentence_only` 49건으로 **후보별 사유와 함께 공개**했다(§2.2) |

## 2. 원장별 판정

### 2.1 market-pricing — PASS

- 계약: 기계 대조 전부 0 이다. 18구획 직접 읽기와 `items` 122행 표(원본 컬럼명 그대로)가 있고, 잠정 관찰은 원문 표와 분리된 칸에 있다.
- 가격 기준과 원문 부족이 구분돼 있다.
  - 원문 부족(B): 출처·시점·표본(B-X-1), 총액/회당·부가세(B-X-2), mid 의 정의(B-S00-2), 용량·줄 수·샷 수·부위 크기(B-S01-1·S07-2·S09-2·S14-1 등).
  - 잠정(P): currency 적용 범위(P-S00-1), mid 가 산술 중간값이 아님(P-X-3, 직접 재계산 3/122 일치).
  - unit 원문 값 17종의 출현 수는 review.md 에 전부 있다. unit 122값은 자동 후보(num_unit·kw)로 모두 덮인다. 수동 구절은 name 위주(241)이고 unit 은 2건이다. 단위 값은 값 전체가 단위라 수집 누락으로 보지 않는다.
- 수식·조건: `/note` 의 「참고」「에 따라 상이」「정가 아닌」, name 의 「고농도」「집중」「비수술」「이상」「기준」「동시」「양쪽」「소부위」「(시술 후 …)」 가 수동 구절로 있다. 단서 대조 밖은 0 이다.
- **분류 비고(비차단)**: I-S05-1(「(부위당)」+「1회」), I-S07-1(「20줄 이상」+「1회」), I-S08-1(「10cm2」+「1회」), I-S14-1(「1개」+「1부위」)은 서로 모순이라기보다 **가격 분모가 두 축으로 함께 적힌 것**일 수 있다. 예를 들어 부위당·회당은 동시에 성립한다. 작업자는 「후속 확인 후보」로만 두었고 확정하지 않았다. 21개 비교 때 B(분모 정의 부재)·P 와 묶어 다루면 된다.
- 알려진 오분절 21출현은 구간 재현 21/21 이다. 영향(부사·관형사 오탐, 「당」 분모 누락 등)도 적혀 있다.

### 2.2 patient-education — PASS

- 계약: 기계 대조 전부 0 이다. 문장 231 · 하위 구절 575 · 정규식 후보 572 가 있다. observations.json 은 원문과 분리된 잠정 관찰이다.
- 수식·부정: 문장 기록 밖 하위 구절로 덮이지 않은 정규식 후보 49건을 `covered_by_sentence_only` 등으로 **후보마다 사유와 함께** issues.md 표에 공개했다(「않」「없」「수 있」「후」「맞으면」 등). 대부분 「…않나요?」「…생길 수 있나요?」 같은 짧은 의문·답변 문장이다. 문장 전체가 단서 하나를 담는 구조라 사유가 맞다고 본다.
- 작업 중 수식·부정·조건 신호 141건을 대조해 구절 27건을 보충했다(validation.md). 수치·빈도·근사 구절 49건도 보충했다(issues 요약 A ①). 그리고 「전수 정답을 보장하지 않는다」고 적었다. 과장 문구는 없다.
- **비차단 한계(새 기록 권고 아님, 참고)**: `covered_by_sentence_only` 중 몇 개는 짧은 문장이 아니라 단서 절(「다만 주사 부위에 일시적 붓기나 멍은 있을 수 있어요」 `/categories/4/common_concerns/0/a`)이 문장 일부다. 원문과 문장 구간이 보존돼 있고 판정이 공개돼 있어 1차 종료를 막지 않는다. 의미 조사 때 문장 안 단서 절을 다시 나누면 된다.
- I 1(「써마지은」)은 표기 이상이며 원본 보존이다. 응급 징후 부족을 B 로 둔 것도 원문 부족과 해석 과제를 섞지 않은 처리다.

### 2.3 post-procedure-timeline — PASS (운영 사고 비고 · 분류 비고)

- 계약: 기계 대조 전부 0 이다. 값 전체 558 · 수동 586 · 자동 1147 이 있다. 수동 586 중 542 는 값 전체와 같은 문자열이다. 원문 값이 「경미한 멍」「약간의 따끔함/화끈감」 같은 짧은 구절이라 그렇다. 긴 값은 manual/S*.txt 에 하위 구절로 나뉘어 있다(예: `/timelines/0/phases/0/normal/0` → 「주사 부위」「작은 돌기/발적」「(15-60분 내 소실)」).
- 따라서 validation.md 의 「모든 문자열 말단 558개에 수동 구절 ≥1」 은 **사실이지만 하위 수식 구절 수집의 근거는 아니다**. 값 안의 정도·속도·경과·비교·조건은 자동 후보(P-DEGREE 98 · P-COURSE 256 · P-SPEED 22 · P-COMPARE 37 · P-COND-SI 8 · P-AFTER 23 · P-NUMUNIT 27 …)로 잡혀 있다. method.auto 와 G-K3 은 「정규식 일치분뿐, 전수 아님」 이라고 밝혔다. 과장으로 판정하지 않는다.
- 시간 역할·조건: 기간(`period`)과 값 속 시간의 기준 시점 부재(G-B2·S00-Q2·S01-Q1·S04-Q2), 경계일 포함 여부(S01-Q2), 기간 표기 방식 차이(G-I1·S02-Q3), 값 시점이 소속 기간을 벗어나는 사례(G-I2), 등급·기간·사건·조치 분리(G-F1)가 기록돼 있다. 빈도 어휘를 백분율로 바꾸지 않았다(G-B3).
- **분류 비고(비차단)**: G-I1·S02-Q3(시술마다 기간 경계 방식이 다름)와 S04-Q1(「수주」 / 「1-3개월」 이 다른 기간에 있음)은 서로 다른 시술·기간의 진술이라 양립할 수 있다. 작업자는 「후속 확인 후보」로만 두었다. 확정하지 않았으므로 비고로 둔다.
- 오분절 76출현은 구간 재현 76/76 이다. 규칙 서명 밖 토큰 정확성은 보장하지 않는다고 적었다(G-K1).
- **운영 사고(계약 위반 비고, 현재 데이터 검증과 분리)**: validation.md §64 에 작업자가 허용 경로 밖 `/Users/kknaks/orca/workspaces/kknaks_profile/scratch_dummy` 에 임시 파일을 만들고 같은 명령에서 지웠다고 **스스로 기록**했다. 이 검토 시점에 그 경로는 없다(`ls`: No such file or directory). 과거 내용과 다른 파일 무변경은 독립적으로 증명할 수 없다. 범위 밖이라 더 조사하지 않았다. 이 사고는 현재 결과 데이터의 원문 대응(§1.2 전부 0)에 영향이 없다. 발주 계약(작업 범위 밖 파일 생성 금지) 위반으로 기록한다.

### 2.4 pre-procedure-checklist — WARN (기록 형식 보완, 1차 종료 가능)

- 계약: 기계 대조 전부 0 이다. 제외 166 은 `type` 135 · `id` 29 · version · updated 다. 모두 코드값이고 사유가 있다. 언어 텍스트 165값은 전부 분석 대상이다.
- **기록 보완 필요(비차단)**: 알려진 오분절 44건(`morphology.json` 의 `known_errors` 와 레코드별 `known_errors`)에 **Pointer·표면형·원시 토큰·영향만 있고 문자구간이 없다**. 스킬 3단계는 「출현 위치(Pointer·구간)」를 요구한다. 직접 확인한 결과는 다음과 같다.
  - 44건 모두 해당 값에서 표면형이 정확히 1번 나온다. 그래서 위치는 Pointer+표면형으로 특정된다.
  - 원시 토큰 서명 44/44 가 실제 토큰 열에 있다. 따라서 추출 오류가 아니라 기록 형식 누락이다. 같은 값에 같은 표면형이 두 번 나오는 일이 생기면 모호해지므로 `span` 을 채워 두는 것을 권고한다.
- **금기 확정 여부**: 작업자는 확인 항목을 금기로 확정하지 않았다.
  - F-G-2 「확인 항목을 금기 관계로 일괄 확정하지 않는다」.
  - B-G-1 「type 6종의 뜻·판정 기준 없음」.
  - P-S05-4 「검사 행위 문구에 absolute_contraindication — type 이 다른 축일 가능성, 확정하지 않음」.
  - review-part-S02 는 `/category_specific/1/checks/8/label` 을 「금기 관계로 읽으면 안 되는 예」로 들었다.
  - 원문 `type` 값 `absolute_contraindication`(22)·`relative_contraindication`(1)은 원장의 구조적 사실로 보존돼 있다. 원문 안 「금기」 명시어는 1회(`/category_specific/15/checks/3/label`)이고 K-S05-6 에 형태소 깨짐 영향과 함께 기록돼 있다.
- 수식·조건: 이소트레티노인(`/universal_checks/6/description`)의 「최소 6개월」「12개월 대기 원칙」「조기 시행 고려 가능」「반드시 확인」, 헤르페스의 「시술 3일 전부터」, 필러 비행의 「이동시키지는 않으나」「(미용상)」 등이 수동 표현에 있다. 단서 대조 밖은 0 이다. A-S04-6(이소트레티노인 구절 누락)은 발견·수정·재검증됐다.
- 수동 표현이 없는 19값(verify info)은 「알레르기 병력」「자가면역질환 여부」 같은 짧은 명사구다. 수식·조건 단서가 없어 비차단이다. 「여부」 의 확인 행위 성격은 F-G-2 범위에서 다루면 된다.
- I-S01-5(absolute_contraindication vs 「대부분의 시술 불가」)는 type 정의가 없어 「확정 못 함」으로 둔 후보다. 적절하다.

### 2.5 treatment-optimization — WARN (분류 보완, 1차 종료 가능)

- 계약: 기계 대조 전부 0 이다. 수동 413(값 전체 141 · 하위 구절 272) · 정규식 1114 · 절 231 이 있다. 수식·부정 토큰 206개 점검표에 미검토 0 이다. 미덮임 어절 163 은 검토 목록으로 공개돼 있다. K-06 은 「별도 읽기 검토는 같은 에이전트」라고 스스로 밝혔다.
- 효과 보완·동일일·순서·간격·회피가 원문대로 구절로 수집돼 있다. 표본 확인 결과:
  - `/combination_rules/0/detail`: 「당일 시술 가능하나」「웬만하면 열시술을 먼저 시행」「2주 이내 효력을 감소시킬 수 있어」「2주 이상 간격을 둔다」「필러 후 HIFU를 4주 이상 간격 권장하거나 HIFU를 먼저 시행한다」「당일 병행 가능하므로」「동일한 절대 규칙으로 취급하지 않음」.
  - `/by_concern/0/severity_levels/2/sequence`: 「HIFU/RF 먼저」「보톡스(같은날 가능)」「2주 후 필러」.
  - `/combination_rules/6/detail`: 「레이저 제모 후 2주 내 동일 부위 필링/프락셔널 금지」.
  - 단서 대조에서 수동+정규식 밖의 6건은 모두 오탐이다.
  - 기준 시점 부재(B-01-1·B-02-1·B-03-1·B-06-2), 「동시」 범위(B-02-2), 출력 수치 기준(B-05-1)을 원문 부족으로 남겼다. F-G4·F-G5 는 조건을 떼면 충돌처럼 읽힌다는 점을 적었다.
- **분류 보완 필요(비차단)** — 수치 차를 「원문 내 불일치 후보」로 분류한 세 건:
  - **I-10-1** `/combination_rules/0/detail` 「필러 후 HIFU를 4주 이상 간격 권장」 vs `/combination_rules/1/detail` 「HA 필러 주입 후 14일 이내 RF/HIFU 시 필러 용해 위험」·`/by_concern/0/severity_levels/2/contraindicated_combos/0` 「HA 필러 후 14일 이내 RF/HIFU 금지」. 하나는 **금지 하한(14일 이내 금지)**, 하나는 **권장 간격(4주 이상)** 이다. 함께 성립한다. 남는 미결은 14일~4주 구간을 어떻게 다룰지와 RF 포함 범위다(F 또는 B).
  - **I-10-2** `/combination_rules/3/rule` 「프락셔널 후 당일 필러 금지」 vs `/combination_rules/3/detail` 「최소 4주 간격」. 4주 간격은 당일 금지를 포함한다. 제목이 더 좁은 금지를 적은 것이라 모순이 아니다. 남는 미결은 금지 범위가 당일인지 4주인지, 즉 제목과 상세의 범위 차이다(P).
  - **I-10-4** `/combination_rules/6/detail` 「2주 내 동일 부위 … 금지」 vs `/by_concern/6/severity_levels/2/contraindicated_combos/0` 「제모 부위 필링/프락셔널 동시 금지」. 동시는 2주 내에 포함된다. 함께 성립한다.
  - 작업자는 세 건 모두 「후보」로 적고 판정하지 않았다. 그래서 모순으로 **확정한 것은 아니다**. 그러나 I 버킷에 두면 21개 비교 때 원문 충돌로 묶일 위험이 있다. P/F 로 옮기거나 각 항목에 「양립 가능(금지 하한 vs 권장 간격), 경계 구간 미정」 비고를 붙이는 것을 권고한다.
  - 나머지 I 는 후보로 유지하는 것이 맞다: I-10-3 「저출력 토닝**만** 권장」 vs 「저출력 IPL(병용 보조)」, I-05-1 경로 「경구+주사」 vs 「경구+국소」, I-03-1·I-04-1·I-06-1·I-07-1 필드 간 항목 차이, I-11-1·I-12-1 plan vs maintenance 빈도. 원문 문맥에 실제 긴장이 있다.
- 오분절 77출현은 구간 재현 77/77 이다. A-01~04 는 발견·수정·재검증 이력이 있다.

## 3. 반드시 고칠 추출 오류

**0건.** 원문 누락·변형·Pointer·구간 오류를 다섯 원장 어디서도 찾지 못했다.

권고(비차단, 1차 종료를 막지 않음):

| # | 원장 | 위치 | 권고 |
|---|---|---|---|
| R1 | pre-procedure-checklist | `morphology.json` `known_errors` 44건 | 각 출현에 값 기준 `span` [start,end) 을 추가한다(현재 44/44 가 값 안에서 유일해 위치는 특정된다) |
| R2 | treatment-optimization | issues I-10-1 · I-10-2 · I-10-4 | I → P/F 로 옮기거나 「양립 가능, 경계 구간 미정」 비고를 붙인다. 원문 수정 제안 아님 |
| R3 | market-pricing · post-procedure-timeline | I-S05-1 · I-S07-1 · I-S08-1 · I-S14-1 / G-I1 · S02-Q3 · S04-Q1 | 21개 비교 때 「기준 축이 두 개 적힌 것」과 「실제 충돌」을 나눠 다룬다. 지금 고칠 필요는 없다 |

## 4. 미결 처리 상태와 사용자 선택

| 원장 | A | B | C | I | P | F | K |
|---|---|---|---|---|---|---|---|
| market-pricing | 0 | 30 | 0 | 4 | 12 | 7 | 4 (오분절 21출현) |
| patient-education | 0 남음 | 36 | 0 | 1 | 42 | 10 | 26 (오분절 25) |
| post-procedure-timeline | 1 (해결) | 21 | 0 | 4 | 6 | 4 | 3 (오분절 76) |
| pre-procedure-checklist | 1 (fixed) | 15 | 0 | 있음(I-S01-5 등) | 있음 | 있음 | 오분절 44 |
| treatment-optimization | 4 (수정) | 26 | 0 | 12 | 108 | 14 | 6 (오분절 77) |

- **C = 0 근거**: 다섯 원장 모두 issues.md 에서 잔여 B·I·P·F·K 의 성격과 영향을 검토하고 C 0 을 판단했다. 나도 같은 결론이다.
  - B 는 원문에 없는 기준·출처·기준 시점이다. 사용자 추측으로 채울 대상이 아니다.
  - I 는 원본 보존 지시가 이미 있다. 원본 수정 여부를 다시 고르게 하지 않는다. 후속 확인 후보로 둔다.
  - P·F 는 21개 비교 뒤 설계 단계 과제다.
  - K 의 도구 설정은 에이전트 판단 범위다.
  - R1·R2 는 기록·분류 보완이라 사용자 선택이 아니다.
- 원문 부족과 에이전트 해석 과제를 섞은 사례는 찾지 못했다. 예: timeline 「거의 필발」 은 B 로 두고 오기 판단을 하지 않았다. checklist 「x2」 도 B 로 두고 뜻을 채우지 않았다.

## 5. 결과·컬럼표 접근 경로

| 원장 | 읽기용 목차 | 컬럼 구성·항목별 값 | 미결 | 검증 |
|---|---|---|---|---|
| market-pricing | [review.md](./first-pass/market-pricing/review.md) | review-part-S00~S17.md(`items` 122행 표) · review.md 컬럼 표·unit 변형 표 | [issues.md](./first-pass/market-pricing/issues.md) | [validation.md](./first-pass/market-pricing/validation.md) · verify.py |
| patient-education | [review.md](./first-pass/patient-education/review.md) | review-part-S00~S17.md · observations.json | [issues.md](./first-pass/patient-education/issues.md) | [validation.md](./first-pass/patient-education/validation.md) · verify.py |
| post-procedure-timeline | [review.md](./first-pass/post-procedure-timeline/review.md) | review-part-S00~S10.md · review.md 「컬럼 구성」 | [issues.md](./first-pass/post-procedure-timeline/issues.md) | [validation.md](./first-pass/post-procedure-timeline/validation.md) · verify.py |
| pre-procedure-checklist | [review.md](./first-pass/pre-procedure-checklist/review.md) | review-part-S00~S05.md | [issues.md](./first-pass/pre-procedure-checklist/issues.md) | [validation.md](./first-pass/pre-procedure-checklist/validation.md) · verify.py |
| treatment-optimization | [review.md](./first-pass/treatment-optimization/review.md) | review-part-1~4.md | [issues.md](./first-pass/treatment-optimization/issues.md) | [validation.md](./first-pass/treatment-optimization/validation.md) · verify.py · mutation-test.py |

구조화 기록은 각 폴더의 `source-map.json` · `morphology.json` · `expressions.json` · `coverage.json` 이다.

## 6. 이 검토가 하지 않은 것

- 형태소 재분석(kiwipiepy 미설치 환경). 기록 토큰의 원문 재현만 확인했다.
- 모든 값의 의미 재독. §1.3 표본과 단서 정규식 보조만 했다. 단서 수치는 전수 의미 조사가 아니다.
- 임상·가격·법적 사실 검증, 원장 간 연결, timeline 운영 사고의 과거 파일 내용 조사.
