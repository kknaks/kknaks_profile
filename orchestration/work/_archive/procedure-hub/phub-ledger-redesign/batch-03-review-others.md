# batch-03 독립 검토 — literature-evidence · problem-packages · problem-combos · pih-risk

- 검토: 독립 Opus 검토 워커(reviewer_doc) · `task_e94c95ab7276` / `ctx_0af2a1122eed` · 2026-11-09
- 기준: [1차 조사 스킬](./ledger-first-pass/SKILL.md)의 산출물 계약·종료 기준(스킬 sha256 `bc443eb1…ae2a`, 발주 기록과 같다), [재개 노트](./_RESUME.md), [발주 기록](./batch-03-dispatches.json)
- 범위: 위 네 원장만 봤다. taxonomy와 다른 원장은 열지 않았다. 원본·결과·스킬·재개 노트·발주 기록·다른 리뷰는 고치지 않았다. 공유 트리에 새로 만든 파일은 이 보고서 하나다. 독립 대조 스크립트는 세션 스크래치패드에만 있다.
- 이 검토는 **1차 수집 계약을 지켰는지**만 본다. 최종 의미 조사, 정규화, 임상·법적 사실 검증, 형태소 전체 정답 판정은 하지 않았다.

## 0. 결론

| 원장 | 판정 | 1차 범위 종료 | 원장 전체 | 반드시 고칠 추출 오류 |
|---|---|---|---|---|
| literature-evidence | **WARN** (기록 보완. 종료를 막지 않음) | 가능 | 완료 아님 | 0 — K-ZHJA 문구가 실제 수집 범위보다 넓게 적혀 있다(§2.1) |
| problem-packages | **PASS** | 가능 | 완료 아님 | 0 |
| problem-combos | **PASS** | 가능 | 완료 아님 | 0 |
| pih-risk | **PASS** (운영 사고 비고 1) | 가능 | 완료 아님 | 0 |

네 원장 모두에서 다음은 **찾지 못했다**: 원문 누락, 원문 변형, 잘못된 Pointer, 잘못된 문자구간·바이트구간, 자료형 변형, 이스케이프 대응 오류, 구획 소유 누락·중복, 형태소 적용·제외 누락, 명시하지 않은 추출 실패. 그래서 종료를 막는 수정 요청은 **0건**이다.

literature-evidence 의 WARN 은 기록 보완 권고다. 중국어·일본어 값의 수식·조건 표현은 사실상 거의 수집되지 않았다. 그런데 issues.md 에는 「직접 읽기·수동 표현·보조 정규식으로 수집했다」고 적혀 있다. 원문 값 자체는 전부 보존·대응돼 있다. 따라서 재조사가 아니라 해당 절의 범위·영향 문구를 고치는 것으로 충분하다(§2.1).

원장 전체 완료는 네 원장 모두 **아니다**. 각 `issues.md` 의 B·I·P·F·K 가 열려 있다. 의미 분해·공통 개념 연결·정규화도 시작하지 않았다.

**지금 필요한 사용자 선택: 0건.** 근거는 §4.

## 1. 검토 방법과 범위 (자동 / 전수 / 표본 구분)

### 1.1 원본 해시와 기존 verify.py 재실행 — 자동, 읽기 전용

| 원장 | 원본 sha256 (발주 기록과 일치) | bytes | `verify.py` 실제 출력 |
|---|---|---|---|
| literature-evidence | `6e179872…2aebfd` | 118,979 | exit 0 · `failure_count` 0 · nodes 2137 · leaves 1726 · segments 18/18 read_direct · morph 적용 137 / 제외 1569 · tokens 3144 · expressions 771(manual 512) · issues 71 · 시작·끝 해시 동일 |
| problem-packages | `e44fa721…08fcb3dc` | 73,526 | exit 0 · `checks=91851 fails=0` · nodes 3656 · 문자열 말단 2366 · 빈 값 48 · sections 15 · tokens 6708 · manual 871 · 시작·끝 해시 동일 |
| problem-combos | `74453c72…5c2cf2262` | 25,026 | exit 0 · 전 항목 PASS (132검사) |
| pih-risk | `cb6e9305…028575c8` | 11,875 | exit 0 · `failure_count` 0 · check_count 11410(77종) · nodes 344 · leaves 288 · tokens 2083 · expressions 310 · 시작·끝 해시 동일 |

- 정확한 해시는 다음과 같다. literature-evidence `6e179872a9c234491ca62c20899757fca3aa5388833aa6bc4d1ac28a032aebfd` · problem-packages `e44fa7216e0eceefde4be368fcdfa623df0834de6989b826f66ba4e408fcb3dc` · problem-combos `74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262` · pih-risk `cb6e9305113d0b47f447eb314ce3bb34d0278bbc8bdf26bc3303d323028575c8`. 실행 전후 `shasum -a 256 -c` 는 4/4 OK 였다.
- 네 결과 폴더 172개 파일의 sha256 을 실행 전후로 비교했다. 정렬 후 diff 는 0 이다. 즉 verify.py 는 아무것도 쓰지 않았다.
- 실행 명령(작업 디렉토리 `first-pass/`): `python3 <원장>/verify.py`. kiwipiepy 가 없는 기본 python3 로 돌렸다. 형태소 재분석은 하지 않고, 기록된 토큰을 원문과 대조했다.

### 1.2 독립 기계 대조 — 전수 (네 원장 모두)

verify.py 를 재사용하지 않았다. 스크래치패드에 원본 텍스트를 한 글자씩 직접 훑는 스캐너를 새로 짰다. 이 스캐너는 중복 키 감지, Pointer, 리터럴 cp 구간, UTF-8 바이트 구간, 키 리터럴 구간, 이스케이프 디코딩 문자 → 파일 cp 대응을 독립적으로 계산한다. 그 결과를 각 원장의 다른 스키마에 맞춰 대조했다.

| 대조 | 방법 | 결과 |
|---|---|---|
| 노드 집합·순서 | 전체 경로(컨테이너·말단·빈 컨테이너)를 source-map `nodes` 와 순서까지 양방향 비교 | 4/4 누락 0 · 불필요 0 · 중복 0 · 순서 일치 |
| 자료형·값 | 말단마다 자료형과 값(파이썬 타입까지) 비교. 문자열은 리터럴 원문·내용 구간(따옴표 제외)·바이트 구간까지 비교 | 4/4 불일치 0 |
| 키 | 키 리터럴 구간·바이트 구간·raw 리터럴, 필드명 출현 목록 | 4/4 불일치 0 (problem-combos 340 · pih-risk 249 · problem-packages 필드 20종 출현 수) |
| 빈 컨테이너 | 빈 배열·빈 객체·빈 문자열 집합 | literature-evidence 빈 배열 20 · problem-packages 48(products 47 + combos 1, `/problems/13/complaints/3/combos`) · problem-combos 0 · pih-risk 0 — 각 기록과 일치 |
| 이스케이프 | literature-evidence 이스케이프 문자열 9개(전부 citations title)의 디코딩 문자별 파일 cp 대응표를 독립 계산해 `decoded_to_file_cp` 와 비교 | 9/9 일치. 이 9개 안의 표현 1건도 파일 cp·바이트 재현 |
| 구획 소유 | 소유 Pointer 합집합 = 전체 노드, 다중 소유 0. 소유 말단 = 말단(problem-packages 는 문자열 말단 + `owned_empty_values` 로 분리) | 4/4 누락·초과·중복 0. 읽기 상태 전 구획 직접 읽음(18 · 15 · 9 · 9) |
| 형태소 적용/제외 | 적용 ∪ 제외 = 대상 말단, 겹침 0, 제외마다 사유. 토큰마다 `value[start:end] == surface`(길이 0 토큰 제외). 파일 cp 를 기록한 원장은 그 값도 비교 | 4/4 불일치 0 · 토큰 3144 / 6708 / 4045 / 2083 · 길이 0 토큰 problem-packages 69 · problem-combos 24 |
| 표현 | 모든 표현(수동·정규식·절/문장)의 `value[span] == text`, 파일 cp·바이트 구간 재현. pih-risk 는 문장 구간 포함 관계와 full_value 도 확인 | 4/4 불일치 0 (771 · 871+1031+27 · 666+388문장 · 310+107) |
| 알려진 오분절 기록 | 기록된 출현 구간의 원문 = 기록 표면형 | 4/4 불일치 0 (literature 34 · packages K-01~05 · combos 81 · pih 51) |
| 분할 문서 원문 대응 | 말단마다 그 구획 review-part 안에 `` `Pointer` `` 가 있는 **같은 행**에 원문 값(JSON 리터럴·`\|` 이스케이프 허용)이 있는지 | 4/4 행 불일치 0 (1726 · 2414 · 370 · 288) |

자동 대조로 확인한 것은 **원문 ↔ 기록 대응**뿐이다. 이 대조는 의미 해석의 정답을 보장하지 않는다.

### 1.3 독립 읽기 — 표본 + 단서 정규식 보조

- **직접 원문과 대조해 읽은 범위(표본)**
  - problem-combos: `/combos/7` 전체, `/combos/2/packages/1`, `/combos/1/packages/2`. review-part-S8 전체(원문 표·잠정 관찰·수동 표현·미결)와 대조했다.
  - pih-risk: `/risk_levels` 전체, 26행의 `pih_risk`·`pih_rate` 전부, `/notes` 전체, `/procedures/13` 전체. I1·I2·B2 와 「나머지 24행 범위 안」 주장을 직접 대조했다.
  - literature-evidence: `/categories/M16/effects/0`·`/categories/M5/adverse_effects/1` 의 statement·accuracy_note·patient_ko/en/zh/ja·citations. review-part-S16 의 관찰·미결도 읽었다.
  - problem-packages: issues I-05·I-09·I-10·F-08 원문(`/problems/4/complaints/0|3|6/combos/*`, `/problems/10/complaints/2/cc_detail`, `/problems/11/complaints/4|7/*`), 빈 combos(`/problems/13/complaints/3/combos`)와 S14 기록.
  - 네 원장의 issues.md · review.md 는 전문을 읽었다. literature-evidence 는 validation.md 도 전문, 나머지는 progress.md 를 읽었다.
- **단서 정규식 보조(전수 의미 조사 아님)**: 한국어 수식·조건·부정 단서(`않|없|금지|피하|불가|아닌|제한적|부족|드물|가능|수 있|주의|권장|이상|이내|간격|경우|시술 후|… 시`)와 zh/ja 단서(`可能|暂时|罕见|极少|…` / `可能|まれ|一時|ない|場合|ことがあ|…`)를 원문 값에서 찾았다. 그 구간이 수동 표현 안에 들어가는지만 셌다. 이 수치는 **누락 후보를 찾는 보조 지표**이며 의미 판정이 아니다.

| 원장 | 단서 일치 | 수동 표현 밖 | 수동 표현 밖을 읽어 본 판정 |
|---|---|---|---|
| problem-combos | 80 | 0 | — |
| pih-risk | 56 | 0 | — |
| problem-packages | 175 | 21 | 21건 모두 오탐(`서브시전`·`볼륨 충전` 의 글자 일치) |
| literature-evidence (patient_ko·accuracy_note) | 64 | 8 | 1건 오탐. 7건은 실제 조건·시점 구절이 수동 표현에 없음(§2.1 ③) |
| literature-evidence patient_zh | 119값 중 70값 일치 | 그중 표현이 1건이라도 있는 값 2 | §2.1 ① |
| literature-evidence patient_ja | 119값 중 40값 일치 | 그중 표현이 1건이라도 있는 값 6 | §2.1 ① |

## 2. 원장별 판정

### 2.1 literature-evidence — WARN (1차 종료 가능, 기록 보완 권고)

**계약 충족**
- 기계 대조 전수 통과. 18구획 전부 직접 읽음 상태다. 진술 119개의 statement·citations 8키·점수·patient_ko/en/zh/ja·added_at 이 모두 review-part 행에 있다.
- 형태소 적용 범위를 정직하게 적었다. 적용은 patient_ko 119 · accuracy_note 17 · rubric 1 = 137값이다. 제외 1569 는 사유별로 기록했다(id_code 460 · bibliographic 357 · en_text 257 · zh_text 119 · ja_text 119 · version_date 104 · ratio 5 · non_string 148). validation.md §4 「검토하지 않은 것」에 「영어·중국어·일본어 형태소」가 명시돼 있다. **전 언어 형태소 분석 완료라는 과장은 없다.**
- 서지(authors·title·journal)·식별자(pmid·doi·pmc·oa_url)는 원문 수집(source-map·review 행)과 형태소 제외를 구분했다. 제외를 「의미 없음」으로 처리한 문구는 없다.
- 영어 statement(수동 197)·patient_en(수동 92)은 수동 표현과 영어 보조 정규식(en_hedge·en_negation·en_compare·en_condition)으로 수식·조건을 모았다.
- 언어별 극성·조건 차이(I-LANG)는 원문 근거가 있다. `/categories/M16/effects/0` 은 statement 가 불승인·근거 부족을 말하고, patient_ko 는 부정을 유지한다. 반면 patient_en/zh/ja 는 wellness 긍정문이다. `/categories/M5/adverse_effects/1` 은 ko 가 「본인의 혈액을 활용하면 매우 안전」을 덧붙이고, en/zh/ja 에는 감염 위험이 없다. 둘 다 I 로 기록했고 어느 쪽이 맞는지 판정하지 않았다.
- C 0 의 근거와 B 20 · I 33 · F 17 의 처리 상태·영향을 issues.md 에 적었다.

**기록 보완 권고 (종료 차단 아님)**
1. **K-ZHJA 문구가 실제보다 넓다.** issues.md 「K-ENG / K-ZHJA」는 zh/ja 값의 수식·조건·부정을 「직접 읽기·수동 표현·영어 보조 정규식으로만 수집했다」고 적었다. 실제는 다르다.
   - 정규식 표에 zh/ja 단서 패턴이 없다(`mixed_hangul` 만 있음).
   - 수동 표현은 patient_zh 3 · patient_ja 12 뿐이고, 대부분 I-SCRIPT·I-LANG 사례 표시용이다.
   - 단서 정규식 보조로 보면 zh 70값·ja 40값에 가능·일시·빈도·부정·조건 단서가 있다. 그중 표현이 있는 값은 2·6 이다. 예: `/categories/M1/adverse_effects/0/patient_zh` 「可能会出现暂时的…」, `/categories/M1/adverse_effects/1/patient_ja` 「…ことがあります」.
   - **고칠 내용**: zh/ja 는 원문 값 보존(source-map·review 행)과 언어 간 차이 관찰(I-LANG·I-SCRIPT)만 했고, 수식·조건 표현의 전수 수집은 하지 않았다고 정정한다. 영향도 덧붙인다: expressions.json 으로 zh/ja 의 가능성·빈도·일시성을 찾으면 빠진다. 후속에 zh/ja 문장을 쓰려면 원문 값을 다시 읽어야 한다.
   - 재조사는 요구하지 않는다. statement(영어 원 주장)와 patient_ko 는 수집돼 있고, zh/ja 는 원문이 전부 보존돼 있기 때문이다.
2. **한국어 조건·시점 구절 7건이 수동 표현에 없다.** 원문 값·형태소 토큰은 있고, 수동 표현만 없다.
   - `/categories/M1/adverse_effects/0/accuracy_note` 「안구 주위 시술 후」
   - `/categories/M5/effects/0/accuracy_note` 「시술 후 상처 치유」
   - `/categories/M8/moa/6/patient_ko` 「CO2 리프레싱 시」
   - `/categories/M8/adverse_effects/1/patient_ko` 「레이저 시술 시 딱지가 생깁니다」
   - `/categories/M8/adverse_effects/2/patient_ko` 「레이저 시술 시 피부에서 진물이」
   - `/categories/M12/adverse_effects/3/patient_ko` 「마이크로니들링 시술 후 피부가 자극받아」
   - `/categories/M12/adverse_effects/4/patient_ko` 「마이크로니들링 시술 후 피부가 붉어지고」
   - 한국어 보조 정규식에 「후·시」 조건 패턴이 없어서 정규식 대조 단계(validation §4-3)에서도 잡히지 않았다. 한계 목록에 위치를 추가하는 정도로 충분하다.
3. 필드명(키)은 전부 형태소 제외했다(영어 snake_case·Mxx 코드). 사유는 기록돼 있다. 다른 원장은 필드명에 Kiwi 를 적용했으나 SL 한 덩어리로만 나왔다. 사유가 명시돼 있어 문제는 아니고, 형식 차이 비고로만 남긴다.

**분류 보완 권고 (선택)**
- `S09-I2`(인용 제목 single-dot ultrasound ↔ statement HIFU)와 `S07-I3`(「실 모아넣기 시술」 ↔ Thread insertion 대응 불명)은 값끼리 모순인 사례가 아니다. 「같은 대상인지 원문이 밝히지 않는다」는 판단 미결이다. batch-02 검토와 같은 기준이면 F(또는 B)가 맞다.

### 2.2 problem-packages — PASS (1차 종료 가능)

- 기계 대조 전수 통과. 문자열 말단 2366(언어 텍스트 적용 2096 + 제외 270: version·updated·problem_id 14·category 254)과 빈 배열 48(products 47·combos 1)을 따로 소유·기록했다. 15구획 모두 직접 읽기 done 이다.
- 독립 읽기 표본에서 미결 주장이 원문과 맞았다.
  - I-05: 같은 combo 의 evidence 가 「PIH 예방 효과의 임상 근거는 제한적」 ↔ 「재생 촉진으로 색소침착 방지」로 맞지 않는다.
  - F-08: 「레이저 + 미백주사」 reason·evidence 가 근거 부족·시너지 배제·안전성 경고를 담는다.
  - I-09: Kybella/벨카이라 ↔ Kybella·Belkyra 국가별 허가 구분.
  - I-10: HIFEM ↔ HIFES.
  - B-04·OB-S14-01: 빈 products 47·빈 combos 1 의 뜻이 원문에 없다.
  - 「영구적 모발 감소」·「보장하지 않으며」 같은 부정·한정, 「제한적」·「부족」·「피할 것」은 수동 표현 안에 있다(단서 보조 175 중 실제 누락 0).
- 이름·코드·기호 불일치(I-01·I-02·I-06·I-07·I-10)와 후속 개념 연결(F-01 taxonomy 대응, F-02 기호 의미)을 구분해 적었다. 원본 변경 제안은 선택 대기로 올리지 않았다.
- K-01~K-05 는 위치·원시 토큰·영향을 함께 기록했고, 교정하지 않았다고 명시했다.
- 남은 미결: B 9 · I 10 · F 8 · K 5 · P 98 · C 0 · A 0.

### 2.3 problem-combos — PASS (1차 종료 가능)

- 기계 대조 전수 통과. 문자열 말단 370 중 적용 249 · 제외 121 이다. 제외는 ID·tier 코드·M코드뿐이고, tierLabel 은 적용했다. 필드명 340 출현, 9구획 직접 읽음.
- 직접 읽은 `/combos/7` 은 원문 값 전부, 「드물게 피하지방 위축」, 「(수술 대체가 아닌 보완적 프로그램)」, 「선택한 에너지 시술(HIFU 또는 RF)→보톡스→필러 순서」, 「일시 감소 가능 → 단단한 음식 주의」가 수동 표현으로 보존됐다. 「드물게」를 백분율로 바꾸지 않았다.
- 미결 주장 I-PC-15(텍스트는 HIFU 또는 RF, procedures 는 `M9`·`M1`·`M2`)와 I-PC-04(procedures 순서 M9·M1·M2·M4 ≠ name 순서)를 원문과 대조해 확인했다. 원문 내 이름·코드·가격·기호 불일치(I-PC-07·10·11·15·16)와 후속 연결(F: M코드 정의, products 분해, 출처 없는 수치)을 나눴다.
- K 81 출현은 `known_missegmentations` 에 원시 토큰·영향과 함께 있다. 「목록(TERMS) 밖 오분절은 빠졌을 수 있다」고 한계를 적었다. 정규식 오탐(「동안 조합」·「세안 제한」)도 남겼다.
- 남은 미결: B 5 · F 6 · I 5 · P 1 · K 81출현 · C 0 · A 0(작업 중 2건 수정).

### 2.4 pih-risk — PASS (1차 종료 가능, 운영 사고 비고)

- 이 결과는 원래 워커의 최종 산출물이다(재시작 대상 아님). 결과 파일 시각은 13:28~13:45, 재시작 기록은 13:38~13:39 이다.
- 기계 대조 전수 통과. 노드 344 · 말단 288 · 키 249 · 형태소 레코드 537(값 288 + 필드명 249, 적용 448 · 제외 89, 제외는 version·updated·category·procedure_ref·pih_risk 코드와 열거·ID 키) · 표현 310 · 정규식 107 · 오분절 51 출현이다. 모두 완전 파싱되고 값·구간이 원문과 대응한다.
- 원문 대조:
  - `/risk_levels` 는 「< 1%」·「1-5%」·「5-15%」·「15-30%」·「> 30%」이다. `/procedures/5` 는 high ↔ 「10-20%」(I1), `/procedures/12` 는 very_low ↔ 「~1%」(I2)이다.
  - 나머지 24행은 등급 범위 안에 있다. `/procedures/0` 「~5%」는 low 상한과 맞닿는다(B2 경계).
  - B1(분모·기간·출처 부족)과 B8(「어두운 피부」 기준은 13번 「IV+」만)도 원문대로다.
  - 「드물게」·「과도한」·「적절한」은 수치로 바꾸지 않고 B4 로 남겼다.
- **운영 사고 비고**: issues.md A1 에 워커가 `pkill -f cat -u <사용자>` 를 실행한 사실이 적혀 있다. 「같은 사용자의 다른 cat 프로세스가 함께 종료됐을 수 있다(확인 불가)」고 피해 범위를 미확인으로 남겼다. 이 검토도 다른 프로세스에 피해가 없었다고 추정하지 않는다. 다만 이번 검토 시점의 세 재시작 원장 결과는 독립 대조를 전부 통과했다. pih-risk 산출물도 기계적으로 정상이다. 따라서 이 사고를 근거로 데이터 실패를 판정하거나 사용자 선택을 만들지 않는다.
- **분류 보완 권고 (선택)**: I3(`/notes/M17` 「표피 손상 최소로 PIH 해당 없음」의 근거 강도)은 두 값이 서로 맞지 않는 사례가 아니다. 에이전트가 문장 근거의 강도를 해석한 것이다. P 또는 F 가 맞다.
- 남은 미결: B 8 · I 3 · P 2 · F 7 · K 3묶음(51출현) · C 0.

## 3. 반드시 고칠 추출 오류

**0건.** 네 원장 모두 Pointer·구간·값·자료형·소유·적용/제외에 고칠 추출 오류가 없다.

비차단 보완은 다음과 같다. 재조사·rebuild 없이 해당 원장 `issues.md` 에 문구를 더하는 수준이다.

| # | 원장 | 위치 | 보완 |
|---|---|---|---|
| R1 | literature-evidence | `issues.md` 「K-ENG / K-ZHJA」 | zh/ja 수식·조건 표현을 전수 수집하지 않았다고 정정. 실제 수집 범위(수동 zh 3·ja 12, zh/ja 정규식 없음)와 영향을 명시(§2.1 ①) |
| R2 | literature-evidence | 위 7개 Pointer | 한국어 조건·시점 구절의 수동 표현 누락을 한계로 위치 기록(§2.1 ②) |
| R3 | literature-evidence · pih-risk | S09-I2 · S07-I3 · pih I3 | I → F/P 재분류 권고(선택) |

## 4. 미결 처리 상태와 「사용자 선택 0」 근거

| 원장 | B | I | F | P | K | C | 처리 상태 확인 |
|---|---|---|---|---|---|---|---|
| literature-evidence | 20 | 33 | 17 | (관찰 다수) | 1 + 18규칙 34출현 | 0 | 각 B 에 부족 정보·제한 활용, I 에 원문 보존·후속 확인 후보, F 에 2단계 과제를 적음 |
| problem-packages | 9 | 10 | 8 | 98 | 5 | 0 | 각 항목에 영향·처리 상태 칸 |
| problem-combos | 5 | 5 | 6 | 1 | 81출현 | 0 | 표 한 행마다 영향 |
| pih-risk | 8 | 3 | 7 | 2 | 3묶음 51출현 | 0 | 「C 0 의 근거」 절이 B·I·F·도구 선택을 각각 검토 |

- 네 원장 모두 C 를 원문 내 불일치 I 와 구분했다. 원본 수정 여부는 원본 보존 지시가 이미 있으므로 다시 묻지 않았다. 원문 부족 B 를 사용자 추측으로 채우게 하지 않았다.
- 이번 검토에서도 지금 사용자가 골라야 1차 결과가 바뀌는 항목은 없었다. 언어 필드 중 어느 것을 기준으로 할지, 근접 중복 진술 병합, 원문 불일치의 원본 확인은 모두 2단계 설계나 원장 간 비교에서 다룬다. 그때 영향을 검토한 뒤 사용자 확인 대상이 될 수 있다. 따라서 **현재 사용자 선택 대기는 0건**이다.
- C 0 은 미결이 없다는 뜻이 아니다. 위 B·I·F·P·K 는 모두 열려 있다.

## 5. 관찰 (판정에 반영하지 않음)

- 재시작한 세 원장의 결과 파일 시각은 13:41~13:58 이고, 재시작 기록은 13:39 이다. 따라서 삭제 전 중간 기록 파일이 남아 쓰였을 흔적은 없다. 다만 시각만으로 읽기의 깊이를 판정하지는 않았다. 읽기 품질은 §1.3 표본으로만 판단했다.

## 6. 결과·컬럼표 접근 경로

| 원장 | 읽기 시작점(컬럼 구성 표 포함) | 구획 문서 | 구조화 기록 | 미결 · 검증 |
|---|---|---|---|---|
| literature-evidence | [review.md](./first-pass/literature-evidence/review.md) §컬럼 구성 표 | `review-part-S00.md`~`S17.md` | source-map.json · coverage.json · morphology.json · expressions.json · issues-index.json · regex-review.json · segmentation-review.json | [issues.md](./first-pass/literature-evidence/issues.md) · [validation.md](./first-pass/literature-evidence/validation.md) |
| problem-packages | [review.md](./first-pass/problem-packages/review.md) §컬럼 구성 | `review-part-S00.md`~`S14.md` | source-map.json · coverage.json · morphology.json · expressions.json · cue-review.json | [issues.md](./first-pass/problem-packages/issues.md) · [validation.md](./first-pass/problem-packages/validation.md) |
| problem-combos | [review.md](./first-pass/problem-combos/review.md) §컬럼 구성 표 | `review-part-S0.md`~`S8.md` | source-map.json · coverage.json · morphology.json · expressions.json | [issues.md](./first-pass/problem-combos/issues.md) · [validation.md](./first-pass/problem-combos/validation.md) |
| pih-risk | [review.md](./first-pass/pih-risk/review.md) §컬럼 구성 표 · §대조 | `review-part-S0.md`~`S8.md` | source-map.json · coverage.json · morphology.json · expressions.json · validation-machine.json | [issues.md](./first-pass/pih-risk/issues.md) · [validation.md](./first-pass/pih-risk/validation.md) |

## 7. 이 검토가 하지 않은 것

- 의미 관계(정보 종류·수식 대상·관계 방향·조건 범위)의 정답 판정, 공통 개념 연결, 정규화
- 형태소 재분석과 서명 밖 토큰의 정확성 판정(kiwipiepy 미설치 환경. 기록된 토큰과 원문의 대응만 확인)
- 임상·법적 사실 검증과 인용 문헌 내용 대조(외부 자료 미사용)
- 비표본 구획의 수동 관찰 전문 정독. 기계 대조와 단서 보조로만 덮었다
- pkill 사고가 다른 프로세스에 끼친 영향 확인
