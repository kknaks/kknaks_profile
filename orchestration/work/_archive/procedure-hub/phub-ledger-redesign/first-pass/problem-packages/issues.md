# problem-packages.json — 미결·한계 기록

상태 문자: **A** = 에이전트 추출/해석 오류 · **B** = 원문 정보 부족 · **C** = 현재 사용자 결정 필요 · **I** = 원문 내 불일치 · **K** = 알려진 분석 한계 · **P** = 잠정 관찰 · **F** = 후속 의미 조사.
원문 불일치(I)는 C 로 부르지 않는다. 원본 변경 제안은 원본 보존 지시 아래 후속 확인 후보이며 지금 선택 대기로 올리지 않는다.

| 상태 | 건수 |
|---|---|
| A | 0 |
| B | 9 |
| C | 0 |
| I | 10 |
| K | 5 |
| F | 8 |
| P (구획 관찰) | 98 |

A = 0: 빌드 중 발견한 추출 오류는 고친 뒤 재검증했다(validation.md). C = 0: 잔여 항목(B·I·K·F)은 원문 보존·후속 단계로 처리 가능하며 지금 사용자 선택을 요구하는 항목은 없다(영향 검토 후 판단 — 각 항목 영향 칸).

## B

### B-01

- 요약: 'CC' 의 풀이가 원문에 없다.
- 영향: cc 필드의 정보 종류(호소/요청/시술 요구 등)를 원문만으로 확정할 수 없다. 후속 의미 조사에서 다른 원장·사용자 정의 확인.
- 원문 위치: `/description`
- 관련 구획 관찰: OB-S13-06
- 처리 상태: 원문 보존 · 후속 확인

### B-02

- 요약: 같은 combo 블록·alternatives 문장이 부위·세부(cc_detail)가 다른 complaint 들에 글자 그대로 반복된다. 부위별 차이 정보가 원문에 없다.
- 영향: complaint 단위 근거·대안을 부위별로 구분해 쓸 수 없다. 반복을 개별 사실로 셀지 템플릿으로 셀지는 후속 설계 과제.
- 원문 위치: `/problems/0/complaints/0/combos/0`, `/problems/0/complaints/5/combos/0/evidence`
- 관련 구획 관찰: OB-S01-04, OB-S01-08, OB-S03-02, OB-S05-04, OB-S06-02, OB-S08-01, OB-S09-01, OB-S12-01, OB-S13-04, OB-S14-02
- 처리 상태: 원문 보존 · 후속 확인

### B-03

- 요약: 약어 'SMP' 풀이 없음.
- 영향: cc_detail 의미 확정 불가. 풀어 쓰지 않고 보존.
- 원문 위치: `/problems/0/complaints/16/cc_detail`
- 관련 구획 관찰: OB-S01-11, OB-S05-10, OB-S06-10, OB-S08-03, OB-S12-08
- 처리 상태: 원문 보존 · 후속 확인

### B-04

- 요약: products 빈 배열의 뜻(제품 없음/미기재) 원문 정보 없음. 전체 47곳.
- 영향: 빈 products 를 '제품 불필요' 로 해석하면 근거 없는 의미 부여.
- 원문 위치: `/problems/0/complaints/3/procedures/0/products`
- 관련 구획 관찰: OB-S01-12, OB-S14-01
- 처리 상태: 원문 보존 · 후속 확인

### B-05

- 요약: '국문·영문 문헌 일치' 는 서지 정보가 없는 근거 언급.
- 영향: 근거 수준·출처를 확인할 수 없다. 외부 자료로 보충하지 않는다.
- 원문 위치: `/problems/1/complaints/3/combos/2/evidence`
- 관련 구획 관찰: OB-S02-05
- 처리 상태: 원문 보존 · 후속 확인

### B-06

- 요약: '시술 2개월 간격 권장' 에 간격의 앞뒤 시술이 명시되지 않았다(combo 실리프팅 + 리프팅기기 문맥만 있음). 순서도 없다.
- 영향: 간격 규칙의 대상·방향을 확정할 수 없다.
- 원문 위치: `/problems/2/complaints/0/combos/1/evidence`
- 관련 구획 관찰: OB-S03-03
- 처리 상태: 원문 보존 · 후속 확인

### B-07

- 요약: alternatives '단계별 접근 추천' 에 단계 내용이 없다(전 원장 반복 위치는 구획 관찰 참조).
- 영향: 대안·순서 정보로 쓸 수 없다.
- 원문 위치: `/problems/3/complaints/0/alternatives/0`
- 관련 구획 관찰: OB-S04-07
- 처리 상태: 원문 보존 · 후속 확인

### B-08

- 요약: '채널' 등 문장 안에서 지시 대상이 정의되지 않은 표현.
- 영향: 기전 진술의 대상을 확정할 수 없다.
- 원문 위치: `/problems/8/complaints/0/combos/0/evidence`
- 관련 구획 관찰: OB-S13-10
- 처리 상태: 원문 보존 · 후속 확인

### B-09

- 요약: 'FDA' 가 문장 성분 없이 나열돼 무엇에 관한 표기인지 알 수 없다.
- 영향: 허가 정보로 해석하면 근거 없는 의미 부여.
- 원문 위치: `/problems/12/complaints/3/cc_detail`
- 관련 구획 관찰: OB-S13-03
- 처리 상태: 원문 보존 · 후속 확인

## I

### I-01

- 요약: procedures.name 'PRP/자가혈' ↔ 같은 complaint 의 combos.combo 'PRP' 표기 불일치(다른 구획에도 반복될 수 있음 — 구획별 관찰 참조).
- 영향: combo 원소를 procedures 항목에 이름으로 잇는 후속 작업에서 문자열 일치가 깨진다. 원본 변경 제안은 후속 확인 후보.
- 원문 위치: `/problems/0/complaints/3/procedures/1/name`, `/problems/0/complaints/3/combos/0/combo/1`
- 관련 구획 관찰: OB-S00-05, OB-S01-05, OB-S04-02, OB-S04-03, OB-S13-01
- 처리 상태: 원문 보존 · 후속 확인

### I-02

- 요약: combo name 이 combo 원소 이름과 다르게 축약된 경우('반영구 단독' ↔ '반영구화장').
- 영향: combo name 을 combo 원소의 조합 표기로 간주할 수 없는 사례.
- 원문 위치: `/problems/0/complaints/13/combos/0/name`, `/problems/0/complaints/13/combos/0/combo/0`
- 관련 구획 관찰: OB-S01-06, OB-S09-09, OB-S10-04, OB-S11-05, OB-S13-08
- 처리 상태: 원문 보존 · 후속 확인

### I-03

- 요약: cc_detail 에 적힌 시술 표현이 같은 complaint 의 procedures 에 없다(바이오스티뮬레이터·실리프팅·스킨부스터·레이저).
- 영향: cc_detail 을 procedures 목록의 요약으로 쓰면 어긋난다. 원본 변경 제안은 후속 확인 후보.
- 원문 위치: `/problems/1/complaints/3/cc_detail`, `/problems/1/complaints/4/cc_detail`, `/problems/1/complaints/5/cc_detail`, `/problems/1/complaints/6/cc_detail`
- 관련 구획 관찰: OB-S02-02, OB-S03-04, OB-S05-04, OB-S06-02, OB-S07-04, OB-S09-03, OB-S09-12, OB-S11-05, OB-S11-06, OB-S12-01, OB-S13-04, OB-S14-05
- 처리 상태: 원문 보존 · 후속 확인

### I-04

- 요약: '팔자주름' complaint(c3) 안에 '목주름' 개선을 말하는 role·combo 가 있고, '목주름' complaint(c5) 에는 그 시술·combo 가 없다.
- 영향: complaint 별 시술 구성을 그대로 쓰면 다른 부위 내용이 섞인다.
- 원문 위치: `/problems/1/complaints/3/procedures/3/role`, `/problems/1/complaints/3/combos/2/reason`, `/problems/1/complaints/5/cc`
- 관련 구획 관찰: OB-S02-03
- 처리 상태: 원문 보존 · 후속 확인

### I-05

- 요약: 같은 combo '레이저 + 스킨부스터' 의 evidence 가 complaint 에 따라 'PIH 예방 임상 근거 제한적'(c0~c2)과 '재생 촉진으로 색소침착 방지'(c3~c7)로 서로 맞지 않는다.
- 영향: evidence 를 combo 단위 근거로 합치면 모순된 주장이 섞인다. 어느 쪽이 옳은지는 임상 판단이므로 이 단계에서 판정하지 않는다.
- 원문 위치: `/problems/4/complaints/0/combos/0/evidence`, `/problems/4/complaints/3/combos/0/evidence`
- 관련 구획 관찰: OB-S05-02
- 처리 상태: 원문 보존 · 후속 확인

### I-06

- 요약: combos.combo 원소가 같은 complaint 의 procedures.name 에 없다('필링' ↔ procedures '메디컬스킨케어').
- 영향: combo 원소를 procedures 로 이을 수 없다. 원본 변경 제안은 후속 확인 후보.
- 원문 위치: `/problems/5/complaints/0/combos/0/combo/1`, `/problems/5/complaints/0/procedures/1/name`
- 관련 구획 관찰: OB-S00-05, OB-S06-01
- 처리 상태: 원문 보존 · 후속 확인

### I-07

- 요약: 한 complaint 안에 같은 procedures.name('스킨부스터')이 role·products 를 달리해 두 번 나온다.
- 영향: name 으로 procedure 를 식별하는 연결은 모호해진다. 배열 순번(Pointer)으로만 구분 가능.
- 원문 위치: `/problems/5/complaints/4/procedures/1`, `/problems/5/complaints/4/procedures/3`
- 관련 구획 관찰: OB-S06-04, OB-S07-01, OB-S11-01
- 처리 상태: 원문 보존 · 후속 확인

### I-08

- 요약: 한 combo 안에서 '영구적 모발 감소' 와 '(반영구)' 와 '완전·영구 제거를 보장하지 않으며' 가 함께 나온다.
- 영향: 효과 지속성 정보를 한 값으로 뽑으면 서로 맞지 않는 정도가 섞인다.
- 원문 위치: `/problems/9/complaints/0/combos/0/reason`, `/problems/9/complaints/0/combos/0/evidence`
- 관련 구획 관찰: OB-S10-01, OB-S13-11
- 처리 상태: 원문 보존 · 후속 확인

### I-09

- 요약: 같은 cc '브이올렛' 의 허가 진술이 두 problem 에서 다르고(FDA 승인 제품 범위), 제품명이 '벨카이라'/'Belkyra' 두 표기로 나온다.
- 영향: 허가 정보를 합치면 서로 맞지 않는다. 사실 판정은 이 단계 범위 밖이며 원본 변경 제안은 후속 확인 후보.
- 원문 위치: `/problems/10/complaints/2/cc_detail`, `/problems/11/complaints/4/cc_detail`
- 관련 구획 관찰: OB-S12-02
- 처리 상태: 원문 보존 · 후속 확인

### I-10

- 요약: cc_detail 'HIFEM' 과 procedures name 'HIFES' 약어 불일치.
- 영향: cc_detail 과 procedure 를 잇지 못한다.
- 원문 위치: `/problems/11/complaints/7/cc_detail`, `/problems/11/complaints/7/procedures/0/name`
- 관련 구획 관찰: OB-S12-04
- 처리 상태: 원문 보존 · 후속 확인

## F

### F-01

- 요약: description 이 taxonomy P1~P14 하위구조를 생성 원천으로 지목한다. problem_id(P1~P14)·category(M코드)·procedures.name·products 가 taxonomy 의 어느 값과 대응하는지는 이 원장만으로 확인할 수 없다.
- 영향: 원장 간 연결(후속 비교 단계). 이번 1차에서는 참조 표현과 위치만 보존.
- 원문 위치: `/description`
- 관련 구획 관찰: OB-S00-01, OB-S00-07, OB-S06-08, OB-S09-04, OB-S13-05
- 처리 상태: 원문 보존 · 후속 확인

### F-02

- 요약: 기호 '/'·'+'·'=' 의 의미가 필드마다 다르게 쓰인다(cc_detail·cc_group·procedures.name·reason·alternatives). README 규칙의 적용 범위 확인 필요.
- 영향: 기호만으로 대안/병렬/결과 관계를 확정하지 않는다.
- 원문 위치: `/problems/0/complaints/0/cc_detail`, `/problems/0/complaints/0/combos/0/reason`
- 관련 구획 관찰: OB-S01-02, OB-S01-14, OB-S05-09, OB-S08-02, OB-S08-05, OB-S11-04
- 처리 상태: 원문 보존 · 후속 확인

### F-03

- 요약: cc_group 에 부위 표현과 시술 표현('반영구화장')이 섞여 있다.
- 영향: cc_group 을 부위 축으로 바로 쓰면 오분류.
- 원문 위치: `/problems/0/complaints/13/cc_group`
- 관련 구획 관찰: OB-S01-03, OB-S10-05
- 처리 상태: 원문 보존 · 후속 확인

### F-04

- 요약: alternatives 에 대안·조건부 추가·금지·일정·장기 관리 등 정보 종류가 섞여 있다.
- 영향: alternatives 를 '대체 시술 목록' 으로 해석하면 금지 지시('피할 것')가 대안으로 뒤집힌다.
- 원문 위치: `/problems/0/complaints/1/alternatives/0`, `/problems/0/complaints/3/alternatives/0`, `/problems/0/complaints/5/alternatives/0`, `/problems/0/complaints/13/alternatives/0`
- 관련 구획 관찰: OB-S01-09, OB-S05-08, OB-S08-04, OB-S12-07, OB-S14-08
- 처리 상태: 원문 보존 · 후속 확인

### F-05

- 요약: cc_detail 의 정보 종류가 problem 마다 다르다(부위·목표·기법·시술).
- 영향: cc_detail 을 단일 의미 칸으로 정의하지 못한다. 후속 의미 조사에서 값별 분해 필요.
- 원문 위치: `/problems/0/complaints/0/cc_detail`, `/problems/1/complaints/0/cc_detail`
- 관련 구획 관찰: OB-S02-01, OB-S05-05
- 처리 상태: 원문 보존 · 후속 확인

### F-06

- 요약: combos.evidence 에 근거 진술·기전·순서/간격 지시·시술자 요건 등 정보 종류가 섞여 있다.
- 영향: evidence 를 '근거' 칸으로만 쓰면 일정 지시가 근거로 오분류된다.
- 원문 위치: `/problems/2/complaints/0/combos/0/evidence`, `/problems/2/complaints/0/combos/1/evidence`
- 관련 구획 관찰: OB-S03-03, OB-S11-07, OB-S12-06, OB-S14-06
- 처리 상태: 원문 보존 · 후속 확인

### F-07

- 요약: '쳐짐' / '처짐' 두 표기 공존(problem·cc_group 은 '쳐짐', evidence 는 '처짐').
- 영향: 문자열 일치 기반 연결에서 갈라진다. 표기 통일은 후속 결정 후보이며 지금 원본을 바꾸지 않는다.
- 원문 위치: `/problems/2/problem`, `/problems/1/complaints/3/combos/1/evidence`
- 관련 구획 관찰: OB-S03-01, OB-S07-05
- 처리 상태: 원문 보존 · 후속 확인

### F-08

- 요약: combos 에 올라 있으나 reason·evidence 가 조합 근거를 부정·한정하는 항목('레이저 + 미백주사'). combos 등재의 의미(추천/언급/경고)가 정의돼 있지 않다.
- 영향: combos 를 추천 조합으로 일괄 해석하면 원문의 부정 진술이 뒤집힌다.
- 원문 위치: `/problems/4/complaints/6/combos/1/reason`, `/problems/4/complaints/6/combos/1/evidence`
- 관련 구획 관찰: OB-S05-06
- 처리 상태: 원문 보존 · 후속 확인

## K

### K-03

- 요약: 이름 안의 '+'(리쥬란 HB+, NAD+수액, ASCE+)가 별도 기호 토큰 '+'/SW 로 분리된다. README 의 '+ = 함께' 기호와 표면이 같다.
- 영향: '+' 로 함께 시술을 분해하면 제품·성분명이 쪼개진다.
- 원문 위치: `/problems/0/complaints/5/procedures/1/products/0`, `/problems/0/complaints/9/procedures/1/products/0`, `/problems/3/complaints/0/procedures/0/products/2`, `/problems/3/complaints/5/cc`, `/problems/4/complaints/0/procedures/1/products/1`, `/problems/4/complaints/1/procedures/1/products/1`, `/problems/4/complaints/2/procedures/1/products/1`, `/problems/4/complaints/3/procedures/1/products/1`, `/problems/4/complaints/4/procedures/1/products/1`, `/problems/4/complaints/5/procedures/1/products/1`, `/problems/4/complaints/6/procedures/1/products/1`, `/problems/4/complaints/7/procedures/1/products/1` 외 10곳
- 관련 구획 관찰: OB-S01-10, OB-S04-08, OB-S13-02
- 처리 상태: 한계로 기록(교정하지 않음)

### K-01

- 요약: Kiwi 기본형·품사는 도메인 표준명이 아니다. 같은 제품·시술 문자열의 품사가 문맥에 따라 NNG/NNP 로 흔들린다(예: '보톡스' 단독 NNG, '보톡스 + 스킨부스터' 안에서 NNP; '필러' 단독 NNP).
- 영향: 품사·기본형으로 시술/제품을 분류하면 안 된다. 이름 판단은 원문 값 전체(source-map)를 기준으로 한다.
- 원문 위치: `/problems/0/complaints/0/combos/0/name`, `/problems/0/complaints/2/combos/0/name`, `/problems/0/complaints/4/combos/0/name`, `/problems/0/complaints/5/combos/0/name`, `/problems/0/complaints/7/combos/0/name`, `/problems/0/complaints/8/combos/0/name`, `/problems/0/complaints/9/combos/0/name`, `/problems/0/complaints/10/combos/0/name`, `/problems/0/complaints/11/combos/0/name`, `/problems/1/complaints/0/combos/1/name`, `/problems/1/complaints/1/combos/1/name`, `/problems/1/complaints/2/combos/1/name` 외 7곳
- 처리 상태: 한계로 기록(교정하지 않음)

### K-02

- 요약: 붙여 쓴 복합어·외래 제품명 오분절: 예 '울쎄라'→울쎄/NNG 이/VCP 라/EC, '리쥬란 힐러'→리쥬/NNP 이/VCP 란/ETM, '눈썹반영구'→반영/NNG 구/NNG, '인모드'(단독)→인/NNG 모드/NNG, '컷슬린'→컷/슬/MAG/린, '이중턱'→이/MM 중턱, '튼살'→트/VV ᆫ/ETM 살, '코끝 거상'→거/MM 상, '점 도포'→도/포, '공기압 박리'→박/리/XSN, '쳐짐'→치/VV 어 지/VX ᆷ/EF, '턱선무너짐'·'눈밑꺼짐'→…/VV ᆷ/EF(명사형 어미를 종결어미로), '감광제'→감/광/제, '외용'→외/용, 'MTS두피'→두/MM 피, '필링'(니들RF + 필링 안)→필/링, 문장 속 '필러'→필/NNG 러/EC. 문장 속 '수 있음'의 '음' 도 EF 로 분석된다(가능성 표현 자체는 수/NNB 있/VA 로 보존).
- 영향: 토큰 단위로 이름·부위를 뽑으면 잘못된 조각(이·란·구·모드 등)이 생긴다. 원문 구간과 수동 표현으로 보완했고 교정하지 않았다.
- 원문 위치: `/problems/0/complaints/0/combos/0/evidence`, `/problems/0/complaints/1/cc_detail`, `/problems/0/complaints/2/combos/0/evidence`, `/problems/0/complaints/4/combos/0/evidence`, `/problems/0/complaints/5/procedures/1/products/0`, `/problems/0/complaints/7/combos/0/evidence`, `/problems/0/complaints/8/combos/0/evidence`, `/problems/0/complaints/9/procedures/1/products/0`, `/problems/0/complaints/10/cc_detail`, `/problems/0/complaints/10/combos/0/evidence`, `/problems/0/complaints/11/combos/0/evidence`, `/problems/0/complaints/13/cc` 외 167곳
- 관련 구획 관찰: OB-S01-01, OB-S01-13, OB-S02-09, OB-S03-07
- 처리 상태: 한계로 기록(교정하지 않음)

### K-04

- 요약: 숫자·로마자·단위 혼합 표기 분리: 'CO2'→CO/SL 2/SN, '1064nm'→1064/SN nm/SL, 'Nd:YAG'→Nd/SL :/SP YAG/SL, '클라리티2'→클라리티/NNG 2/SN, '5-FU'→5/SN -/SO FU/SL, '532+1064nm'→532/SN +/SW 1064/SN nm/SL.
- 영향: 장비·제품·수치 단위를 토큰에서 다시 붙여야 한다. '532+1064nm' 의 단위는 뒤 수치에만 붙어 있어 앞 수치 단위를 토큰으로 판단할 수 없다.
- 원문 위치: `/problems/4/complaints/0/cc_detail`, `/problems/4/complaints/0/combos/0/evidence`, `/problems/4/complaints/1/combos/0/evidence`, `/problems/4/complaints/2/combos/0/evidence`, `/problems/6/complaints/4/cc`, `/problems/7/complaints/0/cc_detail`, `/problems/7/complaints/3/cc_detail`, `/problems/8/complaints/3/cc`, `/problems/8/complaints/6/procedures/0/products/0`, `/problems/8/complaints/6/combos/0/name`, `/problems/8/complaints/6/combos/0/evidence`, `/problems/8/complaints/7/procedures/0/products/0` 외 15곳
- 관련 구획 관찰: OB-S05-12, OB-S07-07, OB-S10-06
- 처리 상태: 한계로 기록(교정하지 않음)

### K-05

- 요약: 기호·한 글자 로마자 결합 오분석: '↓'→SW, '±'→SL(로마자 품사), 'V빔'→V/SL 비/VV ᆷ/EF(용언으로 분석), 'PDL(V빔)'→… 비/VV ᆷ/ETN.
- 영향: 감소 기호(↓)·선택 병용(±)의 뜻은 토큰에 없다. 'V빔' 은 용언으로 잘못 분석돼 동사 검색 시 오탐.
- 원문 위치: `/problems/5/complaints/4/cc_detail`, `/problems/6/complaints/0/cc_detail`, `/problems/7/complaints/0/cc`, `/problems/8/complaints/6/procedures/0/products/0`, `/problems/8/complaints/6/procedures/1/products/0`, `/problems/8/complaints/6/combos/0/name`, `/problems/8/complaints/6/combos/0/evidence`, `/problems/8/complaints/7/cc_detail`, `/problems/8/complaints/7/procedures/0/products/0`, `/problems/8/complaints/7/procedures/1/products/0`, `/problems/8/complaints/7/combos/0/name`, `/problems/8/complaints/7/combos/0/evidence`
- 관련 구획 관찰: OB-S06-05, OB-S09-08
- 처리 상태: 한계로 기록(교정하지 않음)

## 1차에서 검토하지 않은 것

- 공통 개념 ID·동의어 병합·상하 관계·관계 방향·적용 조건: 미검토(후속 단계).
- 다른 원장(taxonomy 등)과의 대응: 미검토(F-01).
- 임상·법적 진술의 사실 여부: 판정하지 않음(원문 보존만).
