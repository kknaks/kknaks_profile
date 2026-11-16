# 수동 오분절 검토 기록 생성기. build.py 1회차 morphology.json 을 직접 읽은 결과(spec 목록)를 출현별 기록으로 만든다.
# raw_tokens 는 실제 Kiwi 출력에서 복사하며, build.py 가 매 실행 다시 대조한다. 실행: 이 폴더에서 python3 segmentation-review-make.py
import json
m=json.load(open('morphology.json'))
V={v['pointer']:v for v in m['values']}
HEAT=("meaning-risk","'열'(熱)이 수사 NR(열=10)로, '시술'이 시/NNB+술/NNG 로 분석","열 시술(열을 쓰는 시술 묶음) 표현이 형태소에서 사라지고 NR 이 수량으로 오인될 수 있음")
FILLER=("meaning-risk","'필러'가 필/N*+러/EC 로 분절","시술명 '필러' 출현이 형태소 기준 집계·검색에서 빠짐")
BAKRI=("meaning-risk","'박리성'(ablative) 이 박/N*+리/XSN|NNG+성 으로 쪼개짐","박리성 시술 범위 표현이 형태소에서 사라짐. '비박리성'과의 구분(부정 접두 비)이 형태소만으로는 판단 불가")
NBAKRI=("meaning-risk","'비박리성'이 비/XPN+박/NNG+리/XSN+성/* 로 쪼개짐(비/XPN 자체는 맞음)","부정 접두 '비'는 남지만 '박리' 용어가 사라져 '비박리성 프락셔널' 범위가 형태소로 재구성되지 않음")
CO2=("minor","'CO2'가 CO/SL+2/SN 로 분리","2/SN 이 수량으로 오인될 수 있음. 장비·시술명 'CO2 프락셔널' 표면형은 원문 구간으로 보존")
MCODE=("code-split","카테고리 코드 접두 'Mn-' 이 M/SL+n/SN+-/SO 로 분리","코드 번호가 수사(SN)로 나옴. 형태소는 코드 식별에 쓰지 않는다(원문 값 그대로 보존)")
RANGE=("range-token","숫자 범위 'a-b' 가 단일 W_SERIAL 토큰","범위의 하한·상한이 형태소에서 분리되지 않음. 원문 구간·표현 후보(quantity_unit_time)로 보존")
spec=[
 ("/principles/1","열시술",0,*HEAT),("/principles/1","열시술",1,*HEAT),
 ("/sequence_order/2/reason","열시술",0,*HEAT),("/sequence_order/7/reason","열 시술",0,*HEAT),
 ("/principles/0","진정",0,"tag-only","'진정'(진정 처치)이 NNP 로 태깅","품사만 다름. 고유명사 집계 시 오탐"),
 ("/sequence_order/10/phase","진정",0,"meaning-risk","'진정'(진정 처치)이 부사 MAG(정말로)로 태깅","modifier_phrase 후보 오탐 생성. 처치 단계명이 부사로 읽힘"),
 ("/sequence_order/10/reason","진정",0,"meaning-risk","'진정'이 부사 MAG 로 태깅","modifier_phrase 후보 오탐 생성. 목적(진정) 명사가 부사로 읽힘"),
 ("/principles/5","세럼",0,"meaning-risk","'세럼'이 세/MM+럼/NNG 로 분절","제형명 소실, MM 이 관형 수식으로 오인(modifier_phrase 오탐)"),
 ("/principles/5","이물",0,"meaning-risk","'이물'(異物)이 이/MM(지시)+물/NNG 로 분절","'진피 내 이물 잔류' 위험 원인 표현이 '이 물'로 읽힘, MM 오탐"),
 ("/principles/5","육아종",0,"meaning-risk","'육아종'이 육아/NNG+종/NNG 로 분절(같은 원장 다른 두 출현은 단일 NNG)","부작용명 소실·'육아'(育兒)로 오인"),
 ("/principles/8","유연",0,"meaning-risk","'유연'이 유/NNG+연/NNG 로 분절","'같은 날엔 순서 유연' 의 완화(허용) 수식이 형태소에서 사라짐"),
 ("/principles/9","필러",2,*FILLER),("/principles/11","필러",0,*FILLER),
 ("/principles/11","먼저",0,"tag-only","'먼저'가 NNG 로 태깅(다른 출현은 MAG)","MAG 기반 수식 후보에서 빠짐. 순서 표현은 keyword 규칙으로 보존"),
 ("/sequence_order/5/reason","필러",0,*FILLER),
 ("/sequence_order/5/reason","몰딩",0,"meaning-risk","'몰딩'이 몰/NNG+딩/MAG 로 분절","시술 후 처치(몰딩) 소실, 딩/MAG 수식 후보 오탐"),
 ("/sequence_order/7/reason","필러",0,*FILLER),("/minimum_intervals/6/reason","필러",0,*FILLER),
 ("/sequence_order/4/phase","니들RF",0,"meaning-risk","'니들'이 니/NP(대명사)+들/XSN 로 분절(다른 출현은 니들/NNP)","장비·시술 계열명 소실"),
 ("/sequence_order/9/categories/0","도포",0,"minor","카테고리 이름 '도포'가 도/NNG+포/NNG 로 분절","카테고리 라벨 처치명 소실(코드값 자체는 원문 보존)"),
 ("/sequence_order/9/reason","경피",0,"meaning-risk","'경피'(經皮)가 경/NNG+피/NNG 로 분절","전달 경로 표현 소실"),
 ("/sequence_order/9/reason","코스메슈티컬의",0,"minor","조사 '의'가 분리되지 않은 단일 NNG","제품군명 표면형에 조사가 붙어 집계 불일치"),
 ("/common_combos/7/note","경피",0,"meaning-risk","'경피'가 경/NNG+피/XPN 로 분절","전달 경로 표현 소실"),
 ("/sequence_order/10/reason","항염",0,"minor","'항염'이 항/NNG+염/NNG 로 분절","목적 표현 '항염'이 단일 형태로 남지 않음"),
 ("/incompatible_same_day/3/reason","비박리성",0,*NBAKRI),("/incompatible_same_day/3/reason","박리성",1,*BAKRI),
 ("/incompatible_same_day/7/reason","비박리성",0,*NBAKRI),("/incompatible_same_day/7/reason","박리성",1,*BAKRI),
 ("/minimum_intervals/2/reason","비박리성",0,*NBAKRI),("/minimum_intervals/2/reason","박리성",1,*BAKRI),
 ("/minimum_intervals/3/to","박리성",0,*BAKRI),("/minimum_intervals/3/reason","박리성",0,*BAKRI),("/minimum_intervals/3/reason","비박리성",0,*NBAKRI),
 ("/incompatible_same_day/7/reason","전안면",0,"meaning-risk","'전'(全)이 저/NP+ᆫ/JX('저는')로 분석","적용 범위(전안면) 수식이 대명사로 바뀌어 범위 조건 소실"),
 ("/minimum_intervals/3/reason","전안면",0,"meaning-risk","'전'(全)이 저/NP+ᆫ/JX 로 분석","적용 범위(전안면) 수식 소실 — 이 문장의 '에 한해' 범위 조건 대상"),
 ("/incompatible_same_day/3/reason","전안면",0,"minor","'전'(全)이 관형사 MM 으로 태깅, 안면/NNG 분리","범위 수식은 MM 으로 남지만 '전안면' 단일 표현은 없음"),
 ("/minimum_intervals/2/reason","전안면",0,"minor","'전'(全)이 관형사 MM 으로 태깅, 안면/NNG 분리","범위 수식은 MM 으로 남지만 '전안면' 단일 표현은 없음"),
 ("/minimum_intervals/3/reason","한해",0,"meaning-risk","'(에) 한해'(限해)가 한/MM(하나)+해/NNB(年)로 분석","범위 제한 조건이 '한 해'(1년) 시간 수량으로 오인될 수 있음"),
 ("/sequence_order/1/reason","전",0,"meaning-risk","'30-60분 전'의 '전'(前)이 관형사 MM 으로 태깅","시점 기준(시술 전) 표현이 관형 수식으로 읽힘"),
 ("/common_combos/0/sequence/1","이마",0,"meaning-risk","부위 '이마'가 이/MM+마/NNG 로 분절","부위 표현 소실, MM 오탐"),
 ("/common_combos/5/sequence/2","이마",0,"meaning-risk","부위 '이마'가 이/MM+마/NNG 로 분절","부위 표현 소실, MM 오탐"),
 ("/common_combos/0/sequence/2","팔자",0,"meaning-risk","부위 '팔자'가 팔/VV(팔다)+자/EC 로 분절","부위 표현 소실·동사로 오인"),
 ("/common_combos/5/sequence/0","팔자",0,"meaning-risk","부위 '팔자'가 팔/VV+자/EC 로 분절","부위 표현 소실·동사로 오인"),
 ("/common_combos/5/sequence/1","리쥬란",0,"meaning-risk","제품명 '리쥬란'이 리쥬/NNG+이/VCP(길이0)+란/ETM 으로 분석","제품명 소실. VCP 토큰은 surface 길이 0"),
 ("/incompatible_same_day/4/reason","나중",0,"meaning-risk","'나중'이 나/JC+중/NNG 로 분절","역순 설명의 순서 표지(나중) 소실"),
 ("/incompatible_same_day/4/reason",">",0,"meaning-risk","비교 기호 '>'가 닫는 괄호 SSC 로 태깅","온도 조건 '>55°C'의 초과 비교가 형태소에서 사라짐"),
 ("/minimum_intervals/0/reason",">",0,"meaning-risk","비교 기호 '>'가 SSC 로 태깅","온도 조건 '>55°C'의 초과 비교가 형태소에서 사라짐"),
 ("/minimum_intervals/7/reason","먼저",0,"tag-only","'먼저'가 NNG 로 태깅","MAG 기반 수식 후보에서 빠짐. 순서 표현은 keyword 규칙으로 보존"),
 ("/incompatible_same_day/2/pair/1","비가교",0,"negation-prefix-fused","부정 접두 '비'가 분리되지 않은 단일 NNP '비가교'","부정(비-가교) 성질이 형태소로 드러나지 않음"),
 ("/sequence_order/5/reason","순서든",0,"zero-length","'순서든'에서 이/VCP 가 길이 0 토큰([193,193))","surface 가 빈 문자열인 토큰 존재(Kiwi 복원형). 구간 대조에서 빈 surface 로 기록"),
 ("/incompatible_same_day/0/pair/0","CO2",0,*CO2),("/common_combos/7/sequence/0","CO2",0,*CO2),("/minimum_intervals/5/from","CO2",0,*CO2),
 ("/incompatible_same_day/2/reason","24-72",0,*RANGE),("/sequence_order/1/reason","30-60",0,*RANGE),
 ("/common_combos/0/total_time","60-90",0,*RANGE),("/common_combos/1/total_time","45-60",0,*RANGE),
 ("/common_combos/2/total_time","90-120",0,*RANGE),("/common_combos/5/total_time","60-90",0,*RANGE),
]
for p in ["/sequence_order/0/categories/0","/sequence_order/2/categories/0","/sequence_order/2/categories/1","/sequence_order/2/categories/2","/sequence_order/3/categories/0","/sequence_order/3/categories/1","/sequence_order/3/categories/2","/sequence_order/9/categories/0","/sequence_order/10/categories/0","/sequence_order/10/categories/1"]:
    t=V[p]['text']; spec.append((p,t.split('-')[0]+'-',0,*MCODE))
occ=[]
for i,(p,ph,o,kind,issue,impact) in enumerate(spec):
    s=V[p]['text']; hits=[j for j in range(len(s)) if s.startswith(ph,j)]
    a=hits[o]; b=a+len(ph)
    raw=[[t['form'],t['tag'],t['span']] for t in V[p]['tokens'] if t['span'][0]>=a and t['span'][1]<=b]
    if p=="/sequence_order/5/reason" and ph=="순서든": pass
    occ.append({"id":f"S{i+1:03d}","pointer":p,"phrase":ph,"occurrence_in_value":o,"phrase_span":[a,b],"raw_tokens":raw,"kind":kind,"issue":issue,"impact":impact,"status":"표시됨(교정 아님) — 원시 Kiwi 토큰 유지"})
doc={"method":"build 1회차 Kiwi 출력 1,429토큰을 값별로 원문과 나란히 직접 읽고 찾은 출현을 하나씩 기록. raw_tokens 는 phrase_span 안에 완전히 들어가는 원시 토큰(실제 출력 복사, build.py 가 매 실행 대조). 교정·사용자 사전 적용 없음.",
 "kinds":{"meaning-risk":"의미 표현(시술·부위·제품·수식·조건·순서)이 형태소에서 소실·왜곡","tag-only":"분절은 맞고 품사만 다름","minor":"분절 차이가 있으나 의미 영향 작음","code-split":"코드값 접두 분리","range-token":"숫자 범위 단일 토큰","negation-prefix-fused":"부정 접두 미분리","zero-length":"surface 길이 0 토큰"},
 "scope_limit":"전 토큰을 읽었으나 여기 없는 토큰이 모두 맞다는 보증은 아니다. NNG/NNP 혼용(예: 보톡스·필러가 출현마다 NNG/NNP), 재표면화 재/NNG 등 의미 영향이 작다고 본 품사 차이는 기록하지 않았다.",
 "occurrences":occ}
json.dump(doc,open('segmentation-review.json','w'),ensure_ascii=False,indent=1)
print(len(occ))
for o in occ:
  if not o['raw_tokens'] or o['phrase']=='순서든': print(o['id'],o['pointer'],o['phrase'],o['raw_tokens'])
