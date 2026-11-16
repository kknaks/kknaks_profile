# issues — literature-evidence.json

원본 sha256 `6e179872a9c234491ca62c20899757fca3aa5388833aa6bc4d1ac28a032aebfd`. 구획별 원본 미결은 각 review-part §4 와 issues-index.json. 아래는 같은 원인 묶음과 처리 상태.

## 상태 요약

| 문자 | 뜻 | 건수(구획 기록) | 처리 상태 |
|---|---|---|---|
| A | 에이전트 추출/해석 오류 | 0 열림 | 작업 중 발견·수정 기록은 validation.md §5. 현재 열린 A 없음 |
| B | 원문 정보 부족 | 20 | 열림 — 부족한 정보와 제한되는 활용을 각 항목에 적음. 사용자에게 사실을 묻지 않음 |
| C | 현재 사용자 결정 필요 | 0 | 아래 「사용자 결정 0의 근거」 |
| I | 원문 내 불일치 | 33 | 열림 — 원문 그대로 보존, 원본 변경은 후속 확인 후보(선택 대기 아님) |
| F | 후속 의미 조사 | 17 | 열림 — 2단계(공통 의미·ERD) 과제 |
| K | 알려진 분석 한계 | 1 + 형태소 규칙 18(출현 34) | 기록 완료, 교정 안 함 |

위 건수는 구조화 기록(`issues-index.json`·manual) 기준이다. batch-03 검토 후 덧붙인 문서 기록(K-ZHJA 정정, 맨 아래 K-KOCOND)은 이 건수에 들어 있지 않으며 둘 다 열림이다.

## 같은 원인 묶음

### I-CITE — patient_ko 인용 표지와 citations 불일치
- 모든 진술의 citations 배열은 정확히 1개다. 그런데 patient_ko 끝에 `[1][2][4][5]`·`[3][9]` 같은 표지가 붙은 값이 있고, 그 번호가 가리킬 문헌 목록이 원장 안에 없다. 출현 위치는 expressions.json facet `citation_marker`(정규식 전수)와 각 구획 I 항목.
- 영향: 표지 숫자(SN)를 수량·근거 개수로 쓰면 오류. 이후 단계에서 표지를 근거 연결로 쓰지 못한다.
- 원본 변경 제안(표지 제거 등)은 원본 보존 지시 아래 후속 확인 후보이며 선택 대기로 올리지 않는다.

### I-SCRIPT — 언어 필드의 다른 문자 혼입
- patient_ja 5곳 한글(`伝달`·`ボツ리ヌ`·`狙い通리의`·`HIFU는`·`毛穴의`), patient_ja 1곳 중국어 간체(`视黄醇类`), patient_en 1곳 한글(`natural성분`), patient_zh 1곳 `的同事`(문맥상 다른 글자 후보). expressions.json facet `mixed_script`(정규식)·수동 표현.

### I-LANG — 같은 진술의 언어별 수식·조건·극성 차이
- statement(영어 원 주장)와 patient_ko/en/zh/ja, accuracy_note 사이에 빈도(`드물게`·`rarely`), 가능성(`may`·`수 있습니다`), 경과(`Temporary`·`일시적`), 조건(부위·피부형·pH·사후관리), 비교 대상, 고유명(성분·장비·질환)이 추가·탈락·변형된다. 가장 큰 사례: M16 effects/0 의 불승인·근거 부족 진술이 patient_en/zh/ja 에서 긍정 효과 문장으로 반전, M5 adverse_effects/1 감염 위험이 en/zh/ja 에서 탈락하고 ko 에 「매우 안전」 추가.
- 영향: 언어별 문장을 같은 사실의 번역으로 취급해 수식·조건을 합치면 뜻이 바뀐다. 어느 필드가 기준인지 원문이 밝히지 않는다(source_method 는 statement 를 검증 대상으로 언급).

### K-ENG / K-ZHJA — 형태소 분석 미적용 언어
- statement·patient_en·name·source_method·scored_by(영어), patient_zh, patient_ja 는 Kiwi(한국어) 적용 범위 밖이라 제외했다. 이 값들의 수식·조건·부정은 직접 읽기·수동 표현·영어 보조 정규식으로만 수집했다. 영어 형태소(품사·기본형)는 없다.
- *정정(batch-03 검토 후 기록 보완, 근거 `../../batch-03-review-others.md` §2.1①):* 위 문장은 **영어 값**(statement 수동 197 · patient_en 수동 92 + en_hedge·en_negation·en_compare·en_condition 보조 정규식)에만 맞는다. **zh/ja 의 수식·조건·부정 표현은 전수 수집하지 않았다.** 실제로 한 것은 다음 세 가지다.
  - 원문 값 보존: `source-map.json` 과 review-part §1 행. patient_zh 119 · patient_ja 119 전부.
  - 제한된 언어 간 차이 관찰: I-LANG · I-SCRIPT.
  - 사례 표시용 수동 표현: patient_zh 3 · patient_ja 12. `expressions.json` 의 patient_ja regex 5 는 `mixed_hangul` 뿐이다. `regex_table` 에 zh/ja 단서 패턴은 없다.
- 리뷰가 단서 정규식(전수 의미 조사 아님)으로 본 결과, 가능·일시·빈도·부정·조건 단서가 zh 119값 중 70값, ja 119값 중 40값에 있다. 그중 표현이 1건이라도 기록된 값은 zh 2 · ja 6 이다. 예: `/categories/M1/adverse_effects/0/patient_zh` 「可能会出现暂时的…」, `/categories/M1/adverse_effects/1/patient_ja` 「…ことがあります」. 보완 워커가 더 좁은 단서 집합으로 다시 세었더니 zh 40값 · ja 30값이었고, 표현이 있는 값은 똑같이 2 · 6 이었다. 단서 집합에 따라 수치가 달라지는 보조 지표다.
- 영향: `expressions.json` 만으로 zh/ja 의 가능성·빈도·일시성·부정·조건을 찾으면 빠진다. 후속 단계에서 zh/ja 문장을 쓰려면 원문 값을 다시 읽어야 한다. 원문 보존만으로 이 미결이 해결되지는 않는다. 열림 상태이며, 이번 보완에서 표현을 추가하지 않았다.

### K-MORPH — 알려진 형태소 오분절(교정 안 함)

- **W01** `필러` mis_segmentation — 10출현 (예: `/categories/M2/moa/1/patient_ko` [6,8)) — 제품군 명칭 '필러'가 사라지고 어미로 분석됨. '필러가'는 가/VV 까지 동사로 오분석 — 주어·대상 연결 손실
- **W02** `하안면` mis_segmentation — 1출현 (예: `/categories/M1/effects/1/patient_ko` [12,15)) — '하안면'(아래 얼굴)의 '하'가 보조용언으로 분리 — 부위 범위(하부) 손실
- **W03** `거미스마일` wrong_sense_split — 1출현 (예: `/categories/M1/effects/3/patient_ko` [16,21)) — 고민 명칭이 '거미'(동물)+'스마일' 로 분리. 기본형 '거미'를 개념으로 쓰면 오탐
- **W04** `이물` mis_segmentation — 1출현 (예: `/categories/M4/adverse_effects/1/patient_ko` [38,40)) — '이물 반응 육아종'의 '이물'(foreign-body)이 관형사 '이'+'물' — 사건 명칭 손실
- **W05** `가교` mis_segmentation — 1출현 (예: `/categories/M4/effects/2/patient_ko` [4,6)) — '가교'(crosslinked)가 동사 '가-'+'교' — 재질 조건(가교/비가교) 손실
- **W06** `내` mis_segmentation — 1출현 (예: `/categories/M5/moa/0/accuracy_note` [4,5)) — 'PRP 내'(PRP 안의)가 대명사 '나'+'의' — 소속 관계 손실
- **W07** `섬유아세포` mis_segmentation — 2출현 (예: `/categories/M5/moa/0/accuracy_note` [13,18)) — '섬유아세포'가 '섬'+'유아'+'세포' — 세포 명칭 손실, '유아'(infant) 오탐
- **W08a** `실은` mis_segmentation — 2출현 (예: `/categories/M7/moa/5/patient_ko` [2,4)) — '실(thread)+은'이 부사 '실은'(사실은) — 시술 재료 주어 손실
- **W08b** `실로` mis_segmentation — 1출현 (예: `/categories/M7/effects/3/patient_ko` [4,6)) — '실(thread)+로'가 부사 '실로' — 도구 표현 손실
- **W09** `붉은기와` mis_segmentation — 1출현 (예: `/categories/M8/effects/0/patient_ko` [20,24)) — '붉은기+와'가 '붉은'+'기와'(roof tile) — 고민 '붉은기' 손실, 나열 접속 '와' 손실
- **W10** `폴리엘엘락산` oversplit — 1출현 (예: `/categories/M3/moa/3/patient_ko` [0,6)) — 재질명이 5조각 — 재질 명칭 인식 불가
- **W11** `피코초` oversplit — 5출현 (예: `/categories/M8/moa/2/patient_ko` [0,3)) — '피코초'(펄스 시간 단위)가 '피코'+'초' — 장비 명칭 일부가 시간 단위 '초'로 분리, 시간 표현 오탐 가능
- **W12** `외분비` oversplit — 1출현 (예: `/categories/M1/adverse_effects/3/patient_ko` [12,15)) — '외분비'(exocrine)가 '외'+'분비' — 뜻은 남지만 용어 경계 손실
- **W13a** `초음파` oversplit — 2출현 (예: `/categories/M9/moa/0/patient_ko` [6,9)) — 장비 에너지 명칭이 접두사+명사 — 용어 경계 손실
- **W13b** `고주파` oversplit — 1출현 (예: `/categories/M9/effects/0/patient_ko` [0,3)) — 장비 명칭(RF) 경계 손실
- **W14** `미세침술` ambiguous_split — 1출현 (예: `/categories/M12/moa/2/patient_ko` [0,4)) — '미세침술' 경계(미세침+술 / 미세+침술) 모호 — '침술'로 읽으면 다른 시술로 오탐
- **W15** `만드는` mis_tag — 1출현 (예: `/categories/M15/moa/0/patient_ko` [7,13)) — 본용언 '만들다'가 보조용언(VX)으로 태깅 — 품사 기반 필터 시 행위 누락
- **W16** `바르는` mis_tag — 1출현 (예: `/categories/M16/effects/1/accuracy_note` [18,25)) — '(피부에) 바르는'이 형용사 '바르다'(곧다)로 태깅 — 투여 경로(topical) 표현 손실

## 사용자 결정 0의 근거

- 남은 항목은 B(원문 부족)·I(원문 불일치)·F(후속 의미 조사)·K(분석 한계)로, 1차 수집 범위 안에서 사용자가 지금 골라야 바뀌는 결과가 없다. 형태소 도구·제외 범위는 에이전트 판단으로 정해 기록했다.
- I 항목의 원본 수정 여부, 언어 필드 기준 결정, 근접 중복 진술 병합 여부는 2단계 설계 때 영향 검토 후 사용자 확인 대상이 될 수 있다(지금은 선택 대기로 올리지 않음).

## 구획별 B 목록

- **S01-B1** (S01) `/categories/M1/adverse_effects/0/statement` — 'have been reported' 만 있고 빈도·지속·대상 집단 정보 없음. patient_ko '드물게'의 근거는 원장에 없다.
- **S02-B1** (S02) `/categories/M2/adverse_effects/0/statement`, `/categories/M2/adverse_effects/2/statement` — 'limited'·'rarely' 의 수치·분모·대상 집단 없음. 백분율로 바꾸지 않는다.
- **S03-B1** (S03) `/categories/M3/adverse_effects/0/statement` — 부작용 배열 진술이 임상 사건이 아닌 대식세포 활성화 비교. 빈도·사건명 정보 없음.
- **S03-B2** (S03) `/categories/M3/effects` — effects 빈 배열 — 효과 진술 없음.
- **S04-B1** (S04) `/categories/M4/name` — name 에 있는 polynucleotides·vitamin cocktails 에 대한 진술 없음.
- **S05-B1** (S05) `/categories/M5/adverse_effects/0/statement` — 'most frequently reported' 의 수치·분모 없음. 지속 기간도 없음(patient_ko '일시적'의 근거 없음).
- **S06-B1** (S06) `/categories/M6/moa`, `/categories/M6/adverse_effects`, `/categories/M6/effects` — 진술 0개 — 기전·부작용·효과 근거가 원장에 없다(source_method 상 검증 인용 없는 주장이 제외됐을 가능성은 원문이 개별 확인해 주지 않음).
- **S07-B1** (S07) `/categories/M7/effects/1/statement` — 'superior' 의 비교 기준이 statement 에 없다(제목에만). 동물 모델 결과의 사람 적용 여부도 원문에 없음.
- **S07-B2** (S07) `/categories/M7/adverse_effects/4/statement`, `/categories/M7/adverse_effects/0/statement` — 'Most'·'minor' 의 비율·정도 기준 없음, 지속 기간 없음.
- **S08-B1** (S08) `/categories/M8/name` — IPL 진술 없음.
- **S08-B2** (S08) `/categories/M8/adverse_effects/1/statement`, `/categories/M8/adverse_effects/2/statement`, `/categories/M8/adverse_effects/3/statement` — crusting·oozing 의 빈도·지속 기간 정보 없음.
- **S09-B1** (S09) `/categories/M9/adverse_effects` — 부작용 진술 없음. 깊이 수치 없음.
- **S10-B1** (S10) `/categories/M10/moa`, `/categories/M10/adverse_effects`, `/categories/M10/effects` — 진술 0개. 약어(HIFEM·HIFES·EMS) 풀이도 원장에 없다.
- **S11-B1** (S11) `/categories/M11/moa`, `/categories/M11/adverse_effects`, `/categories/M11/effects` — 진술 0개.
- **S12-B1** (S12) `/categories/M12/adverse_effects/3/statement`, `/categories/M12/adverse_effects/4/statement` — PIH·홍반·부종의 빈도·지속 기간 없음. patient_en 'common'·'temporary' 의 근거는 원장에 없다.
- **S13-B1** (S13) `/categories/M13/moa`, `/categories/M13/adverse_effects`, `/categories/M13/effects` — 진술 0개.
- **S14-B1** (S14) `/categories/M14/moa`, `/categories/M14/adverse_effects`, `/categories/M14/effects` — 진술 0개.
- **S15-B1** (S15) `/categories/M15/effects` — 효과 진술 없음.
- **S16-B1** (S16) `/categories/M16/adverse_effects/0/statement` — 빈도 정보 없음('드물게' 근거 없음).
- **S17-B1** (S17) `/categories/M17/adverse_effects/0/statement`, `/categories/M17/moa`, `/categories/M17/effects` — 빈도 없음. 기전·효과 진술 없음.

## 구획별 I 목록

- **S01-I1** (S01) `/categories/M1/moa/1/patient_ko`, `/categories/M1/adverse_effects/3/patient_ko`, `/categories/M1/effects/1/patient_ko`, `/categories/M1/effects/2/patient_ko` — patient_ko 끝의 인용 표지 [1][2][4][5]·[3][9]·[2]·[1][2][3] 가 해당 진술 citations(1개)와 대응하지 않는다. 표지가 가리키는 문헌 목록이 원장 안에 없다(전 구획 공통 패턴, issues.md I-CITE).
- **S01-I2** (S01) `/categories/M1/moa/1/patient_ja`, `/categories/M1/moa/2/patient_ja` — patient_ja 에 한글 혼입('伝달', 'ボツ리ヌ'). 원문 그대로 보존(issues.md I-SCRIPT).
- **S01-I3** (S01) `/categories/M1/adverse_effects/0`, `/categories/M1/adverse_effects/1`, `/categories/M1/adverse_effects/2`, `/categories/M1/moa/2 …` — 같은 진술의 statement·patient_ko·en·zh·ja 사이에 빈도('드물게')·가능성('may')·경과('Temporary')·조건·정도('paralyses'↔'calming') 가 서로 다르다. 어느 언어가 기준인지 원문이 밝히지 않는다(issues.md I-LANG).
- **S02-I1** (S02) `/categories/M2/adverse_effects/2/patient_ko`, `/categories/M2/effects/3/patient_en`, `/categories/M2/moa/2/patient_ko`, `/categories/M2/adverse_effects/1/patient_en` — 언어 간 추가·누락: 지연 발현 '몇 개월 후'·'완벽하게 안전하지는 않지만'(ko 만), 'deeper'(en/ja/zh), '강하게'(ko), 부작용→권고형(en/zh). I-LANG 묶음.
- **S02-I2** (S02) `/categories/M2/moa/1/patient_ko`, `/categories/M2/moa/3/patient_ko`, `/categories/M2/effects/3/patient_ko` — 인용 표지 [1]·[1][5]·[1][2][3] vs citations 1개. I-CITE 묶음.
- **S03-I1** (S03) `/categories/M3/name`, `/categories/M3/moa/2/statement` — 카테고리 name 의 4재질 중 진술 주어는 PLLA 뿐. name 범위와 진술 범위 불일치(원문 그대로).
- **S03-I2** (S03) `/categories/M3/moa/1/patient_ko`, `/categories/M3/moa/2/patient_ko`, `/categories/M3/adverse_effects/0/patient_ko` — 인용 표지 vs citations 1개. I-CITE.
- **S03-I3** (S03) `/categories/M3/moa/1/patient_en`, `/categories/M3/moa/0/patient_en`, `/categories/M3/moa/2/patient_en`, `/categories/M3/moa/3/patient_en` — patient_en/zh/ja 가 고유 기전·재질명을 없애고 염증 반응을 '자연스러운 구조'로 바꿈. I-LANG.
- **S04-I1** (S04) `/categories/M4/name`, `/categories/M4/effects/0/statement`, `/categories/M4/effects/2/statement` — name 의 'non-crosslinked HA' 와 진술의 'cross-linked hyaluronic acid' 가 같은 카테고리 안에 있다. 원문 그대로 보존.
- **S04-I2** (S04) `/categories/M4/adverse_effects/1/patient_en`, `/categories/M4/adverse_effects/1/patient_zh`, `/categories/M4/adverse_effects/1/patient_ja`, `/categories/M4/adverse_effects/0/patient_en …` — patient_en/zh/ja 가 전신·육아종·원인·측정 대상을 빼고 '일시적'·'稀に'를 더함. I-LANG.
- **S04-I3** (S04) `/categories/M4/moa/0/patient_ko`, `/categories/M4/effects/2/patient_ko` — 인용 표지 vs citations 1개. I-CITE.
- **S05-I1** (S05) `/categories/M5/adverse_effects/1/patient_ko`, `/categories/M5/adverse_effects/1/patient_en`, `/categories/M5/adverse_effects/1/patient_zh`, `/categories/M5/adverse_effects/1/patient_ja …` — 감염 위험 진술의 언어별 내용 차이: ko 는 '매우 안전' 추가, en/zh/ja 는 위험 자체 탈락, accuracy_note 는 '실제적으로' 추가. I-LANG(안전 정보 방향이 달라지는 사례).
- **S05-I2** (S05) `/categories/M5/effects/0/patient_en`, `/categories/M5/effects/0/patient_zh` — chronic wounds → dry areas/干燥部位. I-LANG.
- **S05-I3** (S05) `/categories/M5/adverse_effects/0/patient_ko`, `/categories/M5/moa/1/patient_ko` — 'most frequently reported' → '가장 흔하게 발생'(보고 기준이 발생 기준으로), 단정 → '알려져 있습니다'. I-LANG.
- **S07-I1** (S07) `/categories/M7/adverse_effects/2/patient_en`, `/categories/M7/adverse_effects/1/patient_en`, `/categories/M7/effects/1/patient_en`, `/categories/M7/effects/3/patient_en …` — patient_en/zh/ja 가 절대 부정→'typically', 약물명·비교(superior)·3차원 재배치 탈락, zh 만 '暂时' 추가. I-LANG.
- **S07-I2** (S07) `/categories/M7/moa/2/patient_ko`, `/categories/M7/moa/3/patient_ko`, `/categories/M7/adverse_effects/2/patient_ko`, `/categories/M7/effects/5/patient_ko` — 인용 표지 vs citations 1개. I-CITE.
- **S07-I3** (S07) `/categories/M7/moa/6/patient_ko` — '실 모아넣기 시술' — statement 'Thread insertion' 과 대응 불명. 원문 보존, 후속 확인.
- **S08-I1** (S08) `/categories/M8/adverse_effects/0/patient_en`, `/categories/M8/adverse_effects/1/patient_en`, `/categories/M8/adverse_effects/2/patient_en`, `/categories/M8/effects/3/patient_en …` — 언어별 차이: 경과('temporary') 일괄 추가, 비교 대상 탈락, MMP→재생 단백질, hyperpigmentation→기미. I-LANG.
- **S08-I2** (S08) `/categories/M8/moa/2/patient_ja` — patient_ja 한글 혼입 '狙い通리의'. I-SCRIPT.
- **S08-I3** (S08) `/categories/M8/moa/1/patient_ko`, `/categories/M8/moa/2/patient_ko`, `/categories/M8/moa/3/patient_ko`, `/categories/M8/moa/7/patient_ko …` — 인용 표지 vs citations 1개. I-CITE.
- **S08-I4** (S08) `/categories/M8/adverse_effects/0/statement`, `/categories/M8/adverse_effects/4/statement` — 같은 사건(Fractional CO2 → hyperpigmentation 악화)에 경과 '일시적' 이 한쪽에만 있다.
- **S09-I1** (S09) `/categories/M9/moa/0/patient_ja`, `/categories/M9/effects/0/patient_ja` — patient_ja 한글 혼입 'HIFU는'·'毛穴의'. I-SCRIPT.
- **S09-I2** (S09) `/categories/M9/moa/0/citations/0/title`, `/categories/M9/moa/0/statement` — 인용 제목은 'single-dot ultrasound', statement 는 HIFU. 같은 장비인지는 원문이 밝히지 않음(후속 확인, 외부 자료로 채우지 않음).
- **S09-I3** (S09) `/categories/M9/moa/0/patient_ko`, `/categories/M9/effects/0/patient_ko`, `/categories/M9/moa/1/patient_ko` — ko 인용 표지 vs citations 1개(I-CITE), 단독 대비 비교·'표층 전체' 추가(I-LANG).
- **S12-I1** (S12) `/categories/M12/adverse_effects/0/patient_ko`, `/categories/M12/adverse_effects/0/accuracy_note`, `/categories/M12/adverse_effects/0/patient_ja`, `/categories/M12/adverse_effects/1/patient_ko …` — 부작용 조건이 필드별로 다르다(피부형↔자외선·사후관리↔깊이). 위험 조건의 원천이 어느 필드인지 원문이 밝히지 않음. I-LANG(조건 변형 사례).
- **S12-I2** (S12) `/categories/M12/moa/5/patient_en` — patient_en 한글 혼입 'natural성분'. I-SCRIPT.
- **S12-I3** (S12) `/categories/M12/moa/0/patient_ko`, `/categories/M12/moa/5/patient_ko`, `/categories/M12/moa/6/patient_ko`, `/categories/M12/adverse_effects/4/patient_ko …` — 인용 표지 vs citations 1개. I-CITE.
- **S15-I1** (S15) `/categories/M15/moa/0/patient_zh`, `/categories/M15/moa/1/patient_ja`, `/categories/M15/moa/1/patient_ko` — 표기 이상: zh '的同事', ja 안 중국어 간체 '视黄醇类', ko '수명'(turnover). I-SCRIPT/I-LANG.
- **S15-I2** (S15) `/categories/M15/adverse_effects/0/accuracy_note`, `/categories/M15/adverse_effects/0/patient_en`, `/categories/M15/adverse_effects/1/patient_en`, `/categories/M15/moa/4/patient_en` — 조건·비교 변형: low pH ↔ '산성도가 낮아' ↔ 'High-potency', 성분명·비교 집합 탈락. I-LANG.
- **S15-I3** (S15) `/categories/M15/moa/1/patient_ko`, `/categories/M15/adverse_effects/1/patient_ko` — 인용 표지 vs citations 1개. I-CITE.
- **S16-I1** (S16) `/categories/M16/effects/0/patient_en`, `/categories/M16/effects/0/patient_zh`, `/categories/M16/effects/0/patient_ja` — 부정·불승인 진술(effects/0)이 en/zh/ja 에서 긍정 효과 문장으로 반전. 가장 영향 큰 언어 간 불일치 사례. I-LANG.
- **S16-I2** (S16) `/categories/M16/adverse_effects/0/patient_en`, `/categories/M16/adverse_effects/0/accuracy_note`, `/categories/M16/adverse_effects/0/patient_ko`, `/categories/M16/effects/1/patient_ko …` — 중증 사건 탈락·'temporary'·'드물게' 추가, 근거 비교→효과 비교. I-LANG.
- **S17-I1** (S17) `/categories/M17/adverse_effects/0/patient_ko`, `/categories/M17/adverse_effects/0/patient_en`, `/categories/M17/adverse_effects/0/patient_ja` — '드물게'·'まれに'·'잘못 사용할 경우' 추가, 사건 예시 탈락. I-LANG.

## 구획별 F 목록

- **S00-F1** (S00) `/accuracy_summary/rubric` — 점수 구간 설명('뉘앙스 보정' 등)이 진술의 어떤 성질을 평가하는지, 점수가 없는 102개 진술의 상태가 무엇인지는 원문만으로 정해지지 않는다 — 후속 의미 조사.
- **S01-F1** (S01) `/categories/M1/adverse_effects/3` — adverse_effects 배열의 피지·땀 감소 진술의 정보 종류(부작용/기전/효과) 판단 — 후속 의미 조사.
- **S02-F1** (S02) `/categories/M2/adverse_effects/0`, `/categories/M2/adverse_effects/2` — 알레르기 반응에 관한 두 진술(정도 vs 빈도)이 같은 사건을 가리키는지 후속 판단.
- **S03-F1** (S03) `/categories/M3/moa/0`, `/categories/M3/moa/2`, `/categories/M3/moa/1`, `/categories/M3/moa/3` — 중복에 가까운 진술 쌍(moa/0·2, moa/1·3)의 동일성 판단 — 후속.
- **S04-F1** (S04) `/categories/M4/adverse_effects/0` — 효과 일관성 한계 진술이 adverse_effects 에 있음 — 정보 종류 후속 판단.
- **S05-F1** (S05) `/categories/M5/moa/1/citations/0/title`, `/categories/M5/moa/2/citations/0/title` — 암 맥락 문헌이 미용 exosome 기전 진술의 근거로 쓰인 적합성 — 원문 범위 밖 사실 확인이 필요, 후속(외부 자료로 채우지 않음).
- **S07-F1** (S07) `/categories/M7/adverse_effects/1`, `/categories/M7/adverse_effects/3`, `/categories/M7/moa/0`, `/categories/M7/moa/6 …` — 근접 중복 진술 쌍의 동일성·병합 여부 — 후속.
- **S07-F2** (S07) `/categories/M7/moa/5/statement`, `/categories/M7/adverse_effects/5/statement`, `/categories/M7/name` — 'Poly(L-lactide-co-ε-caprolactone)' 가 name 의 PLLA·PCL 중 어디에 해당하는지(또는 별도 재질인지) — 원문 기호만으로 확정하지 않음.
- **S08-F1** (S08) `/categories/M8/effects/0/statement`, `/categories/M8/effects/1/statement`, `/categories/M8/effects/3/statement`, `/categories/M8/effects/4/statement` — 쉼표 없는 나열('erythema texture and height')의 항목 경계 — 후속 의미 판단(ko 해석을 정답으로 쓰지 않음).
- **S08-F2** (S08) `/categories/M8/moa/2/citations/0/title` — postburn scar 문헌 근거 진술들의 적용 범위(화상 흉터 한정 여부) — 후속.
- **S09-F1** (S09) `/categories/M9/moa/2/statement`, `/categories/M9/effects/0/statement` — 병용(보완) 진술이 동시 시행·순서·간격 정보를 담지 않음 — 조합 관계의 종류 구분은 후속.
- **S12-F1** (S12) `/categories/M12/effects/1`, `/categories/M12/effects/7`, `/categories/M12/effects/0`, `/categories/M12/effects/6 …` — 동의어·포함 관계 후보(stretch marks↔striae distensae, acne scars⊃atrophic acne scars, PIH 두 진술) — 후속 의미 조사.
- **S12-F2** (S12) `/categories/M12/adverse_effects/2` — 내약성 진술의 정보 종류(부작용 배열 소속) — 후속.
- **S15-F1** (S15) `/categories/M15/moa/2`, `/categories/M15/moa/3` — moa 배열의 적응증 진술 — 정보 종류 후속 판단.
- **S15-F2** (S15) `/categories/M15/adverse_effects/1` — 성분 병용의 자극 증가 진술이 '함께 피할 관계'인지 '주의 조건'인지 — 후속(원문은 회피를 지시하지 않음).
- **S16-F1** (S16) `/categories/M16/effects/1/statement` — topical vitamin C 진술이 IV 카테고리에 있음 — 대상 시술 연결(M15 등)은 후속, 원문 위치 보존.
- **S16-F2** (S16) `/categories/M16/effects/0` — effects 배열의 '효과 근거 불충분' 진술 — 정보 종류(근거 상태) 후속 판단.

## 구획별 K 목록

- **S00-K1** (S00) `/source_method`, `/accuracy_summary/scored_by` — 영어 텍스트는 Kiwi 적용 제외(K-ENG). 직접 읽기·수동 표현으로만 수식·부정을 수집했다.

## batch-03 검토 후 기록 보완 (2026-11-09)

근거: `../../batch-03-review-others.md` §2.1②·§3 R2. 이 절은 문서 기록이다. `issues-index.json`·`manual/*.json`·`expressions.json` 에는 들어 있지 않으며, 위 「상태 요약」 K 건수(1 + 18규칙)에도 포함되지 않는다. 이 파일은 `build.py` 가 생성하므로 rebuild 하면 이 절과 위 K-ZHJA 정정이 사라진다.

### K-KOCOND — 한국어 조건·시점 구절 7건이 수동 표현에 없음

원문 값과 형태소 토큰은 있고 수동 표현만 없다. 한국어 보조 정규식(`ko_possibility`·`ko_negation`·`ko_degree`)에 「후·시」 조건 패턴이 없어서 validation §4-3 대조 단계에서도 걸리지 않았다. 구간은 디코딩된 값 문자열의 코드포인트 `[start,end)` 이다. 원문 값에서 문자열 검색으로 기계 계산했고 일치 횟수는 각 1회다. 조건이 무엇에 걸리는지는 정하지 않았다.

| Pointer | 리뷰 인용 구절 [start,end) | 조건·시점 단서 [start,end) | 기존 표현과의 겹침 | 상태 |
|---|---|---|---|---|
| `/categories/M1/adverse_effects/0/accuracy_note` | `안구 주위 시술 후` [0,10) | `시술 후` [6,10) | 없음 | 누락(열림) |
| `/categories/M5/effects/0/accuracy_note` | `시술 후 상처 치유` [8,18) | `시술 후` [8,12) | 없음 | 누락(열림) |
| `/categories/M8/moa/6/patient_ko` | `CO2 리프레싱 시` [4,14) | `리프레싱 시` [8,14) | regex number_unit `2 ` [6,8)만 | 누락(열림) |
| `/categories/M8/adverse_effects/1/patient_ko` | `레이저 시술 시 딱지가 생깁니다` [3,20) | `시술 시` [7,11) | manual `딱지가 생깁니다` [12,20) — 조건부 [3,11) 은 없음 | 누락(열림) |
| `/categories/M8/adverse_effects/2/patient_ko` | `레이저 시술 시 피부에서 진물이` [4,21) | `시술 시` [8,12) | 없음 | 누락(열림) |
| `/categories/M12/adverse_effects/3/patient_ko` | `마이크로니들링 시술 후 피부가 자극받아` [0,21) | `시술 후` [8,12) | 없음 | 누락(열림) |
| `/categories/M12/adverse_effects/4/patient_ko` | `마이크로니들링 시술 후 피부가 붉어지고` [0,21) | `시술 후` [8,12) | manual `피부가 붉어지고 부을 수 있습니다` [13,31) — 조건부 [0,12) 는 없음 | 누락(열림) |

- 영향: 표현 기록만 보면 이 부작용·효과 진술의 발생 조건이나 기준 시점(시술 중/후)이 빠진다. 시간의 역할(발현·회복 등)이나 적용 조건을 연결하는 후속 단계에서는 이 7개 값의 원문을 다시 읽어야 한다. 같은 원인(「후·시」 패턴 없음)으로 다른 값에도 같은 누락이 있을 수 있다. 위 7건은 리뷰 표본·단서 보조로 찾은 것이며 전수 목록이 아니다.
- 이번 보완에서는 `expressions.json` 에 추가하지 않았다. 의미도 확정하지 않았다.
