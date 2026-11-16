"""실버 2단계(계열) 반영 — 결정론.

입력(고정): step1-products.json · step2-research.json · PROCEDURE-HUB literature-evidence.json
출력: step2-families.json · step2-families.md · step2-origin-questions.md
결정: _RESUME.md §2 2026-10-28 「2단계 계열 조사 반영 — 전부 추천대로」
  (예외: D10 X2 카복시 N2 는 세우지 않음 · 트리필 프로 판단 필요 유지)
  + _RESUME.md §2 2026-10-29 5단계 원칙 · 추가 조사(U1 새 계열 N2~N7 · F8 「계열 밖」 철회 · U8 · U9 새 행) — 결정 파일 step2-step5-decisions.json
  10-29 바꾼 것: 고정 assert(352 행 · 계열 18 · 원장님 문의 3 · 근거 약 9)를 결정 · 입력에서 센 값으로 바꿈
"""
import collections
import json
import re
from pathlib import Path

W = Path(__file__).resolve().parent
LIT_PATH = Path('/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/literature-evidence.json')
TAX_PATH = Path('/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/taxonomy.json')  # 검수 F2·W1: M8 광원은 원천 설명에서

P = json.load(open(W / 'step1-products.json'))
P_ITEMS_BY_ID = {x['ledger_id']: x for x in P['items']}
R = json.load(open(W / 'step2-research.json'))
S5 = json.load(open(W / 'step2-step5-decisions.json'))  # 10-29 5단계 반영(새 계열 · 행 계열 · 새 행)
LIT = json.load(open(LIT_PATH))['categories']
TAX_TEXT = {}  # 원천 항목 id → detail + overview + mechanism
for _m in json.load(open(TAX_PATH))['modality']:
    for _s in _m['subcategories']:
        for _i in _s['items']:
            _e = _i.get('extracted') or {}
            TAX_TEXT[_i['id']] = ' '.join([_i.get('detail') or '', _e.get('overview') or '', _e.get('mechanism') or ''])
    for _p in _m.get('products', []):
        _e = _p.get('extracted') or {}
        TAX_TEXT[_p['id']] = ' '.join([_p.get('name_en') or '', _e.get('overview') or '', _e.get('mechanism') or ''])

DECISION = '_RESUME.md §2 2026-10-28 「2단계 계열 조사(step2-research) 반영 — 전부 추천대로(사용자)」'
ITEMS = {x['ledger_id']: x for x in P['items'] if x.get('active')}
S5_NEW = {x['ledger_id'] for x in S5['new_rows']}
assert set(ITEMS) == {r['ledger_id'] for r in R['rows']} | S5_NEW, set(ITEMS) ^ ({r['ledger_id'] for r in R['rows']} | S5_NEW)

# ───────── 계열 18 ─────────
# 이름: D17 = step2-research 추천 이름. 국내 공식 출처가 확인된 계열 이름은 없음 → M1 외 「공식 출처 미확인」
# 정의: step2-research 정의. M8 · M15 는 D04 · D03 · D09 반영으로 조건부 문구를 확정 문구로.
DEF_OVERRIDE = {
    'M8': '특정 파장의 레이저, 광대역 펄스광(IPL), 협대역 비간섭광(LED)을 피부에 조사해 색소·혈관·모낭·진피를 선택적으로 가열·파괴하거나 광생물조절을 일으키는 시술',
    'M15': '피부 표면에 바르거나 흡수시키는 외용 관리 — 코스메슈티컬·외용 의약품, 화학 박피, 이를 적용하는 기계적 박리·클렌징 기기와 외용제 흡수 보조 기기',
}
NAME_OVERRIDE = {'M8': '레이저·광치료'}  # step2-research M8 name_status 「묶음 D04 를 받으면 「레이저·광치료」」
# 검수 F1(review-step2-report) — 이름
M2_MFDS = {'url': 'https://www.mfds.go.kr/brd/m_550/view.do?seq=200',
           'title': '「성형용 필러」 의료기기 안전성정보 홍보',
           'page': '식품의약품안전처>정책정보>위해정보>의료기기 위해정보>의료기기 안전성서한',
           'checked': '2026-10-28 원문 다시 열어 확인(HTML 제목 · 본문 「성형용 필러로 인한 부작용이 지속적으로 발생」 · 첨부 「의료기기 안전성정보 홍보[성형용 필러].hwp」)'}
M7_ROWS = [r for r in R['rows'] if r['recommended_family'] == 'M7']
M7_ITEMS = collections.Counter()
for _r in M7_ROWS:
    for _it in sorted({(l.get('item') or l.get('item_class') or '').strip() for l in P_ITEMS_BY_ID[_r['ledger_id']]['4_license'].get('licenses', [])} - {''}):
        M7_ITEMS[_it] += 1
M7_FACE = sum(1 for _r in M7_ROWS if any((l.get('item') or l.get('item_class') or '').replace(' ', '') == '안면조직고정용실'
                                          for l in P_ITEMS_BY_ID[_r['ledger_id']]['4_license'].get('licenses', [])))
NAME_FIX = {
    'M2': {'name': '성형용 필러', 'name_status': '국내 공식 출처',
           'basis': f"식약처 {M2_MFDS['title']} — {M2_MFDS['url']} · {M2_MFDS['checked']}",
           'add_synonyms': ['필러'], 'drop_synonyms': ['성형용 필러']},
    'M7': {'name': '실리프팅', 'name_status': f'국내 품목명 있음 · 계열 일부만 해당({M7_FACE}/{len(M7_ROWS)}행) — 공식 일반명 아님',
           'basis': '식약처 품목명(M7 행 허가 item): ' + ' · '.join(f'「{k}」 {v}행' for k, v in sorted(M7_ITEMS.items())),
           'add_synonyms': [], 'drop_synonyms': ['안면조직고정용실(식약처 품목)']},  # 재검수 v2 W-3: 품목명은 name_basis 에만
}
# 검수 W3 — M17 정의 리뷰 문헌 추가(NCBI ESummary 2026-10-28 확인) · 기존 28296617 은 부작용 근거
EXTRA_EVIDENCE = {'M17': [{'pmid': '31247326', 'doi': '10.1016/j.arr.2019.100933',
    'title': 'Adipose-derived cellular and cell-derived regenerative therapies in dermatology and aesthetic rejuvenation.',
    'journal': 'Ageing Res Rev', 'year': '2019', 'role': '정의 근거',
    'quote': 'Cellular and cell-derived components of adipose-derived tissue for the purposes of dermatologic and aesthetic rejuvenation … include micro-fragmented fat (nanofat), the stromal vascular fraction (SVF), adipose-derived mesenchymal stem cells (ASC), and extracellular vesicles (EVs)',
    'verified': 'NCBI ESummary 2026-10-28 (제목·저널·연도 일치)'}]}

DEF_BASIS_NOTE = {
    'M8': 'D04 반영: LED 편입 — PMID 40751922 「LED therapy employs narrow-spectrum, incoherent light for photobiomodulation」 · 원천 M8 영문 「Laser & Light」',
    'M15': 'D03 · D09 반영: 화학 박피 · 기계적 박리·클렌징 · 흡수 보조 기기를 M15 하위로',
    'M16': 'D01 반영: 지방분해주사는 N1 로 나감 · D02: 태반 제제는 계열 밖',
}

# 하위 계열(D18) — 계열별 최종 목록
SUBS = {
    'M1': [], 'M6': ['지방 입자 크기(마이크로 · 나노)'], 'M11': [], 'M12': [], 'M14': [], 'M16': [], 'N1': [],
    'M2': ['히알루론산(HA)', '비HA(영구·반영구)'],
    'M3': ['PLLA', 'CaHA', 'PCL', 'PDLLA', 'PDO'],
    'M4': ['히알루론산', '폴리뉴클레오타이드(PN·PDRN)', '콜라겐', '복합 성분(칵테일)', '무세포동종진피(hADM)'],
    'M5': ['혈소판 농축물(PRP·PRF)', '엑소좀'],
    'M7': ['PDO', 'PCL', 'PLCL', 'PLLA'],
    'M8': ['IPL', 'LED', '엔디야그 레이저', '알렉산드라이트 레이저', '반도체 레이저', '탄산가스 레이저', '루비 레이저', 'Er:YAG', 'Er:Glass', '톨륨', 'KTP', 'PDL'],
    'M9': ['HIFU', 'RF', '마이크로웨이브', 'SUPERB 초음파'],
    'M10': ['HIFEM', 'EMS'],
    'M13': ['핫 플라즈마', '콜드 플라즈마'],
    'M15': ['화학 박피', '기계적 박리·클렌징', '외용제', '흡수 보조 기기'],
    'M17': ['배양액·추출물', '세포(SVF)'],
}
STAGE_RE = re.compile(r'([3-7])단계')

def build_family(f):
    fid = f['id']
    ev = []
    for d in f['definition_basis']:
        if d.get('verified'):
            ev.append({'pmid': d['pmid'], 'doi': d.get('doi'), 'title': d['title'], 'journal': d['journal'], 'year': d['year'],
                       'quote': d.get('quote'), 'verified': d['verified']})
        elif 'statement' in d:
            ev.append({'path': d['path'], 'statement': d['statement'], 'pmid': d.get('pmid'), 'doi': d.get('doi'), 'title': d.get('title'),
                       'role': '부작용 근거' if '.adverse_effects[' in d['path'] else '정의 근거'})
        else:
            ev.append({'path': d['path'], 'value': d['value']})
    ev.extend(EXTRA_EVIDENCE.get(fid, []))
    if fid in DEF_BASIS_NOTE:
        ev.append({'decision': DEF_BASIS_NOTE[fid]})
    deferred, subs_src = [], []
    for s in f['sub_families']:
        st = sorted(set(STAGE_RE.findall(s['handling'])))
        if st:
            deferred.append({'source': s['source'], 'deferred_to': ' · '.join(f'{n}단계' for n in st), 'handling': s['handling'], 'basis': s['basis']})
        subs_src.append({'source': s['source'], 'handling': s['handling'], 'basis': s['basis']})
    if fid == 'M8':  # 재검수 v2 W-2 · 결정 「방식은 4단계 기법」
        deferred.append({'source': 'M8 방식(피코초 · 프락셔널 · 롱펄스 · Q스위치 등 — 원천 하위 M8-2 프락셔널 · 피코초 포함)', 'deferred_to': '4단계',
                         'handling': '방식 → 4단계 기법 · 행 technique_hint 에 적힌 말 그대로 표시만',
                         'basis': '_RESUME.md §2 2026-10-28 「2단계 재검수 v2 PASS 뒤 WARN 3 처리 — M8 하위 계열 = 광원 매질 한 축」'})
        subs_src.append({'source': '(재검수 v2 결정)', 'handling': '하위 계열 = 광원 매질 한 축 — 프락셔널 · 피코초 칸 없앰 · 광원 2종은 null + open',
                         'basis': '_RESUME.md §2 2026-10-28 WARN 3 처리'})
    name = NAME_OVERRIDE.get(fid, f['recommended_name'])
    status = '확정(10-27)' if fid == 'M1' else '공식 출처 미확인'
    synonyms = list(f['synonyms'])
    name_basis = f['name_basis'] + ([f'D04 반영 — step2-research M8 「묶음 D04 를 받으면 「레이저·광치료」」'] if fid in NAME_OVERRIDE else [])
    if fid in NAME_FIX:
        fx = NAME_FIX[fid]
        name, status = fx['name'], fx['name_status']
        name_basis = name_basis + ['검수 F1 반영: ' + fx['basis']]
        synonyms = [s_ for s_ in synonyms if s_ not in fx['drop_synonyms']]
        synonyms = list(dict.fromkeys(fx['add_synonyms'] + synonyms))
    return {
        'id': fid,
        'name': name,
        'name_status': status,
        'name_basis': name_basis,
        'literature_name': f['literature_name'],
        'definition': DEF_OVERRIDE.get(fid, f['definition'].replace('(묶음 D03 를 받으면)', '')),
        'literature_evidence': ev,
        'synonyms': synonyms,
        'sub_families': SUBS[fid],
        'sub_family_handling': subs_src,
        'deferred': deferred,
        'new_family': fid == 'N1',
        'note': f.get('note'),
    }

def build_new_family(f):  # 10-29 U1 — 결정 파일 그대로(문헌 · 허가 근거 · 근거 수준)
    return {
        'id': f['id'], 'name': f['name'], 'name_status': f['name_status'], 'name_basis': f['name_basis'],
        'literature_name': f['literature_name'], 'definition': f['definition'],
        'literature_evidence': f['literature_evidence'] + ([{'license': x} for x in f['license_evidence']] if f.get('license_evidence') else []),
        'synonyms': f['synonyms'], 'sub_families': f['sub_families'], 'sub_family_handling': f['sub_family_handling'],
        'deferred': [], 'new_family': True, 'evidence_level': f['evidence_level'], 'decided_by': f['decided_by'],
        **({'surgery': True} if f.get('surgery') else {}),  # 10-29 J7 G7 · G8 — 수술 표시(모발이식 · 지방흡입)
        'note': f"기존 계열에 안 듦: {' · '.join(f'{k} {v}' for k, v in f['fit_existing']['checked'].items())} · 계열 기본 기법(4단계): {f['default_technique']}",
    }

FAMILIES = [build_family(f) for f in R['families']] + [build_new_family(f) for f in S5['new_families']]
for _fn in S5['family_notes']:
    _f = next(f for f in FAMILIES if f['id'] == _fn['family'])
    _f['literature_evidence'].append({'decision': f"{_fn['note']}({_fn['decided_by']})"})
FAM_IDS = [f['id'] for f in FAMILIES]
assert len(FAMILIES) == len(R['families']) + len(S5['new_families']) and len(set(FAM_IDS)) == len(FAM_IDS)
for _f in S5['new_families']:
    SUBS[_f['id']] = _f['sub_families']
FNAME = {f['id']: f['name'] for f in FAMILIES}

# ───────── 제품 → 계열 ─────────
OUT = '계열 밖'
OUT_KIND = {  # 계열 밖 사유 종류
    '아큐탄': '의약품(D02)', '라이넥': '의약품(D02)', '멜스몬': '의약품(D02)',
    '미라쥬': '진단 장비(D12)', '3D 메타뷰': '진단 장비(D12)', '마크뷰': '진단 장비(D12)', '스케나': '진단 장비(D12)',
    '헤어셀': '단독 기기 — 17 정의 밖 · 독립 문헌 확인 안 됨(D16 추천)',
}
# 판단 필요 → 계열 밖 으로 확정되는 행(결정: 「헤어셀 = 계열 밖」)
TO_OUT = {'헤어셀'}

def step1_sub(x):
    n = x['family']['name']
    return n.split(' · ', 1)[1].split(' (원천')[0] if ' · ' in n else ''

def lic_items(x):
    return {l.get('item') or l.get('item_class') for l in x['4_license'].get('licenses', []) if (l.get('item') or l.get('item_class'))}

# 하위 계열 — 규칙(원천 하위 이름 · 허가 품목) + 이름별 지정(근거는 step2-research 행 근거·메모)
SUB_BY_NAME = {
    # M3 — 원천 products 설명 「PLLA」
    '신펄': 'PLLA', '글로벨라': 'PLLA',
    # M4
    '릴리이드M': '복합 성분(칵테일)', 'NCTF 필로르가': '복합 성분(칵테일)', '매쿰7': '복합 성분(칵테일)', '사이토케어': '복합 성분(칵테일)',
    '스네일샷': '복합 성분(칵테일)', '밸피엔': '폴리뉴클레오타이드(PN·PDRN)',
    '콜라쥬': '콜라겐', '레티젠': '콜라겐', '미라콜': '콜라겐', '콜라겐핀': '콜라겐',
    # M5
    '셀피아': '혈소판 농축물(PRP·PRF)', '리젠ACR': '혈소판 농축물(PRP·PRF)', '마이셀': '혈소판 농축물(PRP·PRF)',
    'EXOSOME SKIN': '엑소좀', 'ASCE+엑소좀': '엑소좀', '셀엑소좀': '엑소좀', '카탈리스트': '엑소좀', '드원셀': '엑소좀',
    # M8 — D04 LED
    '옴니룩스': 'LED', '힐라이트': 'LED', '아스트로돔': 'LED', '셀라이트': 'LED', '데마루치': 'LED', '바이오프로톤': 'LED', '오메가라이트': 'LED',
    # M9 — 복합 · 옮김 · 현장 기기(D15 「주 = 허가 품목 · 원천 위치 · 설명 첫 원리」)
    '포커스듀얼': 'HIFU', '에브넥': 'RF', '바이캐빈': 'RF', '아폴로': 'RF', '트라이리프트': 'RF', '시크릿맥스': 'RF',
    '트루스컬프트': 'RF', '바넥스': 'RF', '올타이트': 'RF',
    '덴서티 하이': 'RF', '덴서티': 'RF', '세르프': 'RF', '리니어지': 'HIFU', '울핏': 'HIFU', '스텔라듀오': 'HIFU', '울킨': 'HIFU',
    # M10
    '엠스컬프트': 'HIFEM', '엠스컬프트 네오': 'HIFEM', '엠페이스': 'HIFEM',
    '이볼브': 'EMS', '스팀슈어': 'EMS', '바넥스프로': 'EMS', '엔진': 'EMS', '쿨톤': 'EMS',
    # M15
    '밀크필': '기계적 박리·클렌징', '미라필링': '기계적 박리·클렌징', '해초필': '기계적 박리·클렌징', 'ASA필': '기계적 박리·클렌징',
    '미라클필링': '기계적 박리·클렌징', '그린필': '기계적 박리·클렌징', '제네오X': '기계적 박리·클렌징', '힐퓨전 프로': '기계적 박리·클렌징',
    '오투덤': '기계적 박리·클렌징', '라라젯': '기계적 박리·클렌징', '콘투락투벡스': '외용제',
    'LDM': '흡수 보조 기기', '벨라소닉': '흡수 보조 기기', '소노케어': '흡수 보조 기기', '크라이오 멀티마스터': '흡수 보조 기기',
}
SUB_NONE = {  # 하위 계열 null 사유
    '바이리즌': ('open', '라인 — 허가 품목이 HA 필러(the 채움 프리미엄 No. 2)와 PN(PN SKINBOOSTER)으로 갈림 · 품목별 하위는 결정 없음'),
    '소프웨이브': ('open', '원천 하위 「SUPERB 초음파」 — D18 M9 하위(HIFU · RF · 마이크로웨이브)에 해당 근거 없음'),
}
for n in ['리투오', '리투오 파인', '셀르디엠', '쥬브아셀', '아디떼', '도프ECM']:
    SUB_NONE[n] = ('open', 'D07 은 M4 편입만 결정 — M4 하위(HA · PN · 콜라겐 · 복합)에 hADM 하위 없음')
for n in ['큐어젯', '미라젯', '에어젯', '노보젯', '하이쿡스', '더마샤인', '비타인젝터']:
    SUB_NONE[n] = ('n/a', 'D05 「M4 의 제품(기기) — 하위 계열 아님 · 「어떻게」는 4단계 기법」')

SUB_LABEL = {  # 원천(step1 family.name) 하위 이름 → 하위 계열
    'M2': {'국산 HA': '히알루론산(HA)', '수입 HA': '히알루론산(HA)', '비HA 필러': '비HA(영구·반영구)'},
    'M3': {'PLLA (폴리-L-락틱산)': 'PLLA', 'CaHA (칼슘하이드록시아파타이트)': 'CaHA', 'PCL (폴리카프로락톤)': 'PCL',
           'PDLLA (폴리-D,L-락틱산)': 'PDLLA', 'PDO (폴리디옥사논)': 'PDO'},
    'M4': {'HA (물광)': '히알루론산', 'PN/PDRN': '폴리뉴클레오타이드(PN·PDRN)', '콜라겐/신규': '콜라겐'},
    'M9': {'HIFU (초음파)': 'HIFU', 'RF (고주파)': 'RF', '마이크로웨이브': '마이크로웨이브'},
    'M13': {'핫플라즈마': '핫 플라즈마', '콜드플라즈마': '콜드 플라즈마'},
    'M15': {'케미컬필링': '화학 박피', '딥클렌징': '기계적 박리·클렌징', '물리필링(해면체 미세침)': '기계적 박리·클렌징',
            '허벌 필링': '기계적 박리·클렌징'},
    'M17': {'줄기세포배양액': '배양액·추출물', '자가혈유래 줄기세포': '배양액·추출물'},
}

# 재검수 v2 W-1~W-3 · _RESUME §2 10-28 「WARN 3 처리」: M8 하위 = 광원 매질 한 축 · 방식(피코초 · 프락셔널 …)은 4단계 기법(technique_hint)
# 매질은 허가 item · 허가 모델명 · 원천 하위 이름 · 원천 설명 어디든 적힌 것. 2종 이상이면 null + open(광원 2종)
M8_WEAK = {'아이콘': '원천 「IPL과 1540nm 레이저 결합」 · 허가 「기타 레이저 수술기」 — 광원 2종(1540nm 매질 표기 없음)(검수 W1 지목)'}
M8_DUAL = {'젠틀맥스 프로 플러스': '원천 설명 「듀얼 파장 레이저」(755nm · 1064nm) — 광원 2종으로 봄(재검수 v2 W-1 · 결정 「듀얼 파장」 사유로 open)'}
# 허가 품목명의 매질 — 적힌 말 그대로(「…수술기」 · 「…조사기」만 뗌)
M8_LIC = [('엔디야그', '엔디야그 레이저'), ('알렉산드라이트', '알렉산드라이트 레이저'), ('반도체', '반도체 레이저'),
          ('탄산가스', '탄산가스 레이저'), ('루비', '루비 레이저'), ('펄스광선', 'IPL')]
# 모델명 · 원천 이름 · 원천 설명의 매질 — 같은 매질은 식약처 품목명 표기로 맞춤(Nd:YAG = 엔디야그 · 다이오드 = 반도체 · CO2 = 탄산가스 · Alexandrite = 알렉산드라이트)
# 품목명 행이 없는 매질(Er:YAG · Er:Glass · 톨륨 · KTP · PDL)은 원문 그대로
M8_TEXT = [(r'Nd:YAG|엔디야그', '엔디야그 레이저'), (r'알렉산드라이트|Alexandrite', '알렉산드라이트 레이저'), (r'다이오드|[Dd]iode', '반도체 레이저'),
           (r'CO2|탄산가스', '탄산가스 레이저'), (r'루비|[Rr]uby', '루비 레이저'), (r'Er:YAG|어븀야그', 'Er:YAG'), (r'Er:Glass|에르븀 ?글래스|에르븀글라스', 'Er:Glass'),
           (r'톨륨|[Tt]hulium', '톨륨'), (r'KTP', 'KTP'), (r'PDL(?! 아님)', 'PDL'), (r'IPL|펄스광', 'IPL')]
# 방식 — 적힌 말 그대로 technique_hint 로(4단계 기법 · 표시만)
M8_TECH = r'피코초|피코나노|[Pp]icosecond|프락셔널|프랙셔널|[Ff]ractional|롱펄스|[Ll]ong ?[Pp]ulse|Q-switched|Q-Switched|큐스위치|나노초|비박리성|박리성|비박피'

def m8_text(x):
    lic = x['4_license'].get('licenses', [])
    items = sorted({(l.get('item') or l.get('item_class') or '') for l in lic} - {''})
    models = ' / '.join(str(l.get(k)) for l in lic for k in ('model', 'models', 'official_name', 'product_names') if l.get(k))
    src_sub = step1_sub(x)
    desc = ' '.join(TAX_TEXT.get(i, '') for i in [x['ledger_id']] + (x.get('taxonomy_product_ids') or []))
    return items, models, src_sub, desc

def m8_technique(x):
    items, models, src_sub, desc = m8_text(x)
    return sorted(set(re.findall(M8_TECH, ' '.join([src_sub, models, desc])))) or None

def m8_light(x, name):
    if name in M8_WEAK:
        return None, M8_WEAK[name]
    if name in M8_DUAL:
        return None, M8_DUAL[name]
    items, models, src_sub, desc = m8_text(x)
    found = {}  # 매질 → 어디에 적혔나
    for it in items:
        for k, lab in M8_LIC:
            if k in it.replace(' ', ''):
                found.setdefault(lab, []).append(f'허가 품목 「{it}」')
    for where, txt in (('허가 모델명', models), ('원천 하위', src_sub), ('원천 설명', desc)):
        for k, lab in M8_TEXT:
            if re.search(k, txt):
                found.setdefault(lab, []).append(where)
    if len(found) == 1:
        lab, wh = next(iter(found.items()))
        return lab, ' · '.join(dict.fromkeys(wh)) + f' — 매질 「{lab}」 하나'
    if len(found) > 1:
        return None, 'D18 M8 매질 못 정함 — 광원 2종(' + ' · '.join(f"{k}: {'/'.join(dict.fromkeys(v))}" for k, v in sorted(found.items())) + ')'
    return None, 'D18 M8 매질 못 정함 — 허가 품목 · 모델명 · 원천 설명에 매질 표기 없음' + (f'(허가 품목 「{" · ".join(items)}」)' if items else '')

def sub_family(fam, x, name):
    if fam is None or fam == OUT:
        return None, None
    if name in SUB_BY_NAME:
        s = SUB_BY_NAME[name]
        assert s in SUBS[fam], (name, fam, s)
        return s, 'step2-research 행 근거 · 메모(이름별 지정)'
    if name in SUB_NONE:
        return None, SUB_NONE[name][1]
    if not SUBS[fam]:
        return None, '이 계열은 하위 계열 없음(D18)'
    lab = step1_sub(x)
    s = SUB_LABEL.get(fam, {}).get(lab)
    if s:
        return s, f'원천 하위 「{lab}」'
    if fam == 'M7':
        if '폴리디옥사논봉합사' in lic_items(x):
            return 'PDO', '허가 품목 「폴리디옥사논봉합사」'
        return None, '재질 출처 없음 — 허가 품목명으로 재질이 안 갈림'
    if fam == 'M17':
        return '배양액·추출물', '원천 설명 「줄기세포 유래 …」(step2-research 행 근거)'
    if fam == 'M8':
        return m8_light(x, name)
    return None, f'원천 하위 「{lab or "없음"}」 — 규칙에 없음'

def step1_code(x):
    m = re.match(r'^(M\d+)\b', x['family']['name'])
    return m.group(1) if m else None

# step2-research 정정: 4행은 research rows[].recommended_family 가 step1 family.code(원장 위치)를 썼으나
# 같은 행 메모가 「1단계 반영된 계열이 맞음」(= family.name 의 계열)이라 추천 본문대로 name 계열을 쓴다.
ERRATA = {}

VERDICT = {'맞음': '맞음', '옮김': '옮김', '여러 계열': '여러', '판단 필요': '판단 필요'}
product_family, out_of_family, open_items = [], [], []
for r in R['rows']:
    lid = r['ledger_id']; x = ITEMS[lid]; name = r['display_name']
    fam = r['recommended_family']
    verdict = VERDICT[r['verdict']]
    basis = r['basis']
    s1 = step1_code(x)
    if r['verdict'] == '맞음' and s1 and fam != s1:
        ERRATA[lid] = {'display_name': name, 'research_field': fam, 'applied': s1, 'research_note': r.get('note'),
                       'tag': 'D03 대상 행 · 조사 정정' if 'D03' in r['bundles'] else '조사 정정'}
        fam = s1
    if name == '트리필 프로':  # D10 예외: 카복시 N2 는 세우지 않음
        basis = basis.split(' — 카복시(X2)')[0] + ' — 결정(10-28): 카복시 N2 는 세우지 않음 · 5단계 카복시테라피에서 재검토 · 판단 필요 유지(약물 주입이면 M4)'
    if name in TO_OUT:
        fam = OUT
        basis = basis + ' → 결정: 헤어셀 = 계열 밖'
    if fam == OUT:
        verdict = '계열 밖'
    if fam is None:
        assert verdict == '판단 필요', name
    sub, sub_basis = sub_family(fam, x, name)
    row = {
        'ledger_id': lid, 'display_name': name,
        'family': fam, 'family_name': FNAME.get(fam, fam),
        'also_families': r['also_families'],
        'sub_family': sub, 'sub_family_basis': sub_basis,
        'technique_hint': m8_technique(x) if fam == 'M8' else None,
        'basis': basis, 'note': r.get('note'),
        'step1_family': x['family']['name'], 'step1_code': s1,
        'verdict': verdict, 'bundles': r['bundles'], 'auto': r['auto'],
        'also_sub_families': [], 'conflict': None, 'evidence_level': None, 'confirm_question': None, 'pending_director': False,
    }
    product_family.append(row)
    if fam == OUT:
        out_of_family.append({'ledger_id': lid, 'display_name': name, 'kind': OUT_KIND[name], 'basis': basis})
    if fam is None:
        open_items.append({'ledger_id': lid, 'display_name': name, 'type': 'family', 'reason': basis, 'question': 'step2-origin-questions.md'})
    elif fam != OUT and sub is None and name in SUB_NONE and SUB_NONE[name][0] == 'open':
        open_items.append({'ledger_id': lid, 'display_name': name, 'type': 'sub_family', 'reason': sub_basis})
    elif fam in ('M7', 'M8') and sub is None:
        open_items.append({'ledger_id': lid, 'display_name': name, 'type': 'sub_family', 'reason': sub_basis})

# ───────── open 40 해결안 반영(_RESUME §2 10-28 「2단계 open 40 해결안 반영」) ─────────
RESOLVE_PATH = W / 'step2-open-resolve.json'
_RES = json.load(open(RESOLVE_PATH))
RESOLVE = {x['ledger_id']: x for x in _RES['rows']}
V4_FIX = _RES.get('v4_fix', [])
OPEN_BEFORE = {o['ledger_id'] for o in open_items}
assert set(RESOLVE) == OPEN_BEFORE, set(RESOLVE) ^ OPEN_BEFORE
DIRECTOR = {  # 원장님 문의 3 — family null 유지 · 1단계 확인 불가 · 추천 제외 그대로
    '알렉스필': '바르는 필링이면 M15 「화학 박피」 · 알렉산드라이트 레이저 시술이면 레이저 시술 이름 → 5단계(시술 이름)',
    '더마큐어': '피글 저온 플라즈마 TS-3 이면 M13 「콜드 플라즈마」',
    '벨르업': '원리(에너지) 확인 후 그 계열 — 지금 출처는 사진 폴더 「2_리프팅」뿐',
}
pending_director = []
for p in product_family:
    rv = RESOLVE.get(p['ledger_id'])
    if not rv:
        continue
    name = p['display_name']
    if name in DIRECTOR:
        assert p['family'] is None
        p['pending_director'] = True
        p['confirm_question'] = rv['ask']
        pending_director.append({'ledger_id': p['ledger_id'], 'display_name': name, 'question': rv['ask'],
                                 'if_confirmed': DIRECTOR[name], 'researched_value': rv['resolve'], 'researched_basis': rv['basis'],
                                 'sources': rv['sources'], 'status': '원장님 문의 · family null · 추천 제외(1단계 확인 불가 그대로)'})
        continue
    res = rv['resolve']
    was_null = p['family'] is None
    p['family'] = res['family']; p['family_name'] = FNAME[res['family']]
    p['also_families'] = res['also_families']
    p['sub_family'] = res['sub_family']; p['also_sub_families'] = res['also_sub_families']
    p['sub_family_basis'] = rv['basis'] + ' · 출처: ' + ' · '.join(rv['sources'])
    p['conflict'] = rv['conflict']
    p['evidence_level'] = rv['level']
    p['confirm_question'] = rv['ask'] if rv['level'] == '약' else None
    p['resolve_rule'] = rv['rule']
    if was_null:
        p['verdict'] = '여러' if p['also_families'] else '옮김'
        p['basis'] = p['basis'] + ' → open 해결안: ' + rv['basis']
        if p['family'] == 'M8':
            p['technique_hint'] = m8_technique(ITEMS[p['ledger_id']])
    if p['sub_family']:
        assert p['sub_family'] in SUBS[p['family']], (name, p['sub_family'])
open_items = []  # 끝 조건: open = 0 (해결 37 · 원장님 문의 3)
assert len(pending_director) == len(DIRECTOR)

# ───────── 10-29 5단계 반영(step2-step5-decisions.json) ─────────
S5_DELTA = []
_pf = {p['ledger_id']: p for p in product_family}
for rf in S5['row_family']:  # F8 · U1 — 「계열 밖」 철회 → 새 계열
    p = _pf[rf['ledger_id']]
    S5_DELTA.append({'ledger_id': p['ledger_id'], 'display_name': p['display_name'], 'before': p['family'], 'after': rf['family'], 'decided_by': rf['decided_by']})
    p['family'] = rf['family']; p['family_name'] = FNAME[rf['family']]; p['sub_family'] = rf['sub_family']
    p['sub_family_basis'] = '이 계열은 하위 계열 없음(10-29 U1)' if not SUBS[rf['family']] else p['sub_family_basis']
    p['verdict'] = rf['verdict']; p['basis'] = p['basis'] + ' → ' + rf['basis']
out_of_family = [o for o in out_of_family if _pf[o['ledger_id']]['family'] == OUT]
for nr in S5['new_rows']:  # U8 · U9 — 1단계 새 active 행
    x = ITEMS[nr['ledger_id']]
    assert nr['sub_family'] is None or nr['sub_family'] in SUBS[nr['family']], nr
    product_family.append({
        'ledger_id': nr['ledger_id'], 'display_name': x['2_names']['display_name'],
        'family': nr['family'], 'family_name': FNAME[nr['family']], 'also_families': [],
        'sub_family': nr['sub_family'], 'sub_family_basis': nr['sub_family_basis'],
        'technique_hint': None, 'basis': nr['basis'], 'note': None,
        'step1_family': x['family']['name'], 'step1_code': step1_code(x),
        'verdict': nr['verdict'], 'bundles': [nr['decided_by']], 'auto': False,
        'also_sub_families': [], 'conflict': None, 'evidence_level': None, 'confirm_question': None, 'pending_director': False,
    })
    S5_DELTA.append({'ledger_id': nr['ledger_id'], 'display_name': x['2_names']['display_name'], 'before': '(새 행 — 1단계 10-29)', 'after': nr['family'] + (f" · {nr['sub_family']}" if nr['sub_family'] else ''), 'decided_by': nr['decided_by']})
for rn in S5['row_notes']:  # U2 — 값은 그대로 · 메모만
    _pf[rn['ledger_id']]['note'] = ((_pf[rn['ledger_id']]['note'] or '') + ' · ' if _pf[rn['ledger_id']]['note'] else '') + f"{rn['note']}({rn['decided_by']})"

WEAK = [p for p in product_family if p['evidence_level'] == '약']
assert all(p['confirm_question'] for p in WEAK)

assert len(product_family) == len(ITEMS) and {p['ledger_id'] for p in product_family} == set(ITEMS)
assert all(p['family'] in FAM_IDS + [OUT, None] for p in product_family)
assert all(a in FAM_IDS for p in product_family for a in p['also_families'])
assert all(p['pending_director'] for p in product_family if p['family'] is None)

# 검수 W4 — step1 정본 값 불일치(step1 고정 · 기록만)
SOURCE_FIX = [{'ledger_id': 'auto-M11-1775360645191', 'display_name': '셀리뉴', 'field': 'step1-products.json 1_identity.detail',
               'value': ITEMS['auto-M11-1775360645191']['1_identity'].get('detail'),
               'conflict': '원천 설명 「모노폴라 RF 기술을 이용한 비침습적 피부 리프팅」 · 웹(fnnews 2024-01-28 · 비올 IR) 「모노폴라 고주파 ‘CELLINEW’」(review-step2-report W2 · W4)',
               'action': '1단계 원천 수정 후보 — step1 은 고정이라 이번에 고치지 않음'}]
assert SOURCE_FIX[0]['value'], 'detail 비어 있음'

# M8 하위 칸 = 실제로 쓴 매질만(SUBS 순서)
_used8 = {p['sub_family'] for p in product_family if p['family'] == 'M8' and p['sub_family']} | {a['sub_family'] for p in product_family for a in p['also_sub_families'] if a['family'] == 'M8'}
for _f in FAMILIES:
    if _f['id'] == 'M8':
        _f['sub_families'] = [s_ for s_ in SUBS['M8'] if s_ in _used8]

# 10-29 7단계 보강(J7) — 단위 시술 키가 쓰는 하위 계열 · 정의 넓힘(결정 파일 step2-step5-decisions.json · 제품이 안 써도 키가 씀)
S7_DELTA = []
for _f in S5['new_families']:  # J7 G6 · G7 · G8 — 새 계열(제품 행 없음 · 단위 시술 키가 씀)
    if _f['decided_by'].startswith('J7'):
        S7_DELTA.append({'family': _f['id'], 'change': f"새 계열 {_f['name']}" + (' · 수술' if _f.get('surgery') else '') + f" — 기본 기법 {_f['default_technique']}", 'decided_by': _f['decided_by']})
for _a in S5.get('sub_family_additions') or []:
    _f = next(f for f in FAMILIES if f['id'] == _a['family'])
    if _a['sub_family'] not in _f['sub_families']:
        _f['sub_families'] = _f['sub_families'] + [_a['sub_family']]
    SUBS[_a['family']] = list(dict.fromkeys(SUBS[_a['family']] + [_a['sub_family']]))
    _f['sub_family_handling'].append({'source': f"(J7 단위 시술 키) {_a['sub_family']}", 'handling': '하위 계열(단위 시술 키가 씀)', 'basis': f"{_a['basis']}({_a['decided_by']})"})
    _f['literature_evidence'] += [dict(e, role=e.get('role') or '하위 계열 근거') for e in _a.get('literature_evidence') or []]
    S7_DELTA.append({'family': _a['family'], 'change': f"하위 + {_a['sub_family']}", 'decided_by': _a['decided_by']})
for _u in S5.get('definition_updates') or []:
    _f = next(f for f in FAMILIES if f['id'] == _u['family'])
    S7_DELTA.append({'family': _u['family'], 'change': f"정의 넓힘: {_f['definition']} → {_u['definition']}", 'decided_by': _u['decided_by']})
    _f['definition'] = _u['definition']
    _f['literature_evidence'] += [dict(e, role=e.get('role') or '정의 넓힘 근거') for e in _u.get('literature_evidence') or []]
    _f['literature_evidence'].append({'decision': f"{_u['basis']}({_u['decided_by']})"})

# 이번 수정분(재검수 v2 WARN 3) — 직전 산출 고정본과 비교(step2-families.v2.json · 2026-10-28 v2 재검수 대상)
PREV_PATH = W / 'step2-families.v2.json'
PREV = {p['ledger_id']: p for p in json.load(open(PREV_PATH))['product_family']}
delta = [{'ledger_id': p['ledger_id'], 'display_name': p['display_name'], 'family': p['family'],
          'before': PREV[p['ledger_id']]['sub_family'], 'after': p['sub_family'], 'technique_hint': p['technique_hint'],
          'basis': p['sub_family_basis']}
         for p in product_family if p['ledger_id'] in PREV and p['ledger_id'] not in {d['ledger_id'] for d in S5_DELTA}
         and (p['family'], p['sub_family']) != (PREV[p['ledger_id']]['family'], PREV[p['ledger_id']]['sub_family'])]

# 이번 반영분 — 직전 산출 고정본(step2-families.v3.json · open 40 해결안 반영 전)과 비교
PREV3 = {p['ledger_id']: p for p in json.load(open(W / 'step2-families.v3.json'))['product_family']}
def _asf_norm(p):  # v3 고정본은 문자열 · 지금은 {family, sub_family}
    return tuple((a['family'], a['sub_family']) if isinstance(a, dict) else ((a.split(' · ', 1)[0], a.split(' · ', 1)[1]) if ' · ' in a else (p['family'], a)) for a in (p.get('also_sub_families') or []))
def _key(p): return (p['family'], tuple(p['also_families']), p['sub_family'], _asf_norm(p), p['verdict'])
delta3 = [{'ledger_id': p['ledger_id'], 'display_name': p['display_name'],
           'before': {'family': PREV3[p['ledger_id']]['family'], 'sub_family': PREV3[p['ledger_id']]['sub_family'], 'verdict': PREV3[p['ledger_id']]['verdict']},
           'after': {'family': p['family'], 'also_families': p['also_families'], 'sub_family': p['sub_family'], 'also_sub_families': p['also_sub_families'],
                     'verdict': p['verdict'], 'evidence_level': p['evidence_level'], 'pending_director': p['pending_director']}}
          for p in product_family if p['ledger_id'] in PREV3 and p['ledger_id'] not in {d['ledger_id'] for d in S5_DELTA} and _key(p) != _key({**PREV3[p['ledger_id']], 'also_sub_families': PREV3[p['ledger_id']].get('also_sub_families') or []}) or p['pending_director']]

cnt = collections.Counter(p['verdict'] for p in product_family)
by_fam = collections.Counter(p['family'] if p['family'] else '판단 필요(family null)' for p in product_family)
changed = [p for p in product_family if p['family'] != p['step1_code']]

out = {
    'version': 'step2-families v1', 'generated_by': 'step2-apply.py',
    'inputs': ['step1-products.json', 'step2-research.json', 'step2-step5-decisions.json(10-29 새 계열 · 행 계열 · 새 행)', str(LIT_PATH), str(TAX_PATH), 'step2-open-resolve.json(open 40 해결안)',
               'step2-families.v2.json · step2-families.v3.json(수정분 비교용 고정본)'],
    'decision': DECISION,
    'rules': [f"계열 {len(FAMILIES)} = M1~M17 + " + ' · '.join(f"{f['id']} 「{f['name']}」" for f in FAMILIES if f['id'].startswith('N')) + ' — 10-28 카복시 N2 를 세우지 않던 D10 예외는 10-29 U1 로 철회(N2 세움)',
              '판정: 맞음 / 옮김 / 여러(주 + also_families) / 계열 밖 / 판단 필요(family null)',
              '하위 계열 = D18 · 3·4·5·6단계로 넘기는 것은 families[].deferred 표시만'],
    'summary': {'families': len(FAMILIES), 'rows': len(product_family), 'verdicts': dict(cnt),
                'by_family': dict(by_fam), 'changed_rows': len(changed), 'open': len(open_items),
                'pending_director': len(pending_director), 'evidence_weak': len(WEAK), 'conflicts': sum(1 for p in product_family if p['conflict']),
                'this_apply_changed_rows': len(delta3),
                'out_of_family': len(out_of_family), 'step5_delta': len(S5_DELTA), 'step7_delta': len(S7_DELTA)},
    'step5_delta': S5_DELTA,
    'step7_delta': S7_DELTA,
    'v4_fix': V4_FIX,
    'v3_delta': delta3,
    'v2_delta': delta,
    'research_errata': ERRATA,
    'source_fix_candidates': SOURCE_FIX,
    'families': FAMILIES, 'product_family': product_family, 'out_of_family': out_of_family, 'open': open_items,
    'pending_director': pending_director,
}
(W / 'step2-families.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')

# ───────── md ─────────
def asf_txt(p_):
    return ' · '.join(a['sub_family'] if a['family'] == p_['family'] else f"{a['family']} {a['sub_family']}" for a in (p_.get('also_sub_families') or []))
def fl(c):
    return '—(null)' if c is None else (c if c == OUT else f'{c} {FNAME[c]}')
def sk(c):
    if c in FAM_IDS: return FAM_IDS.index(c)
    return 100 if c == OUT else 101
L = []; A = L.append
A('# 실버 2단계 계열 원장 — step2-families')
A('')
A(f'> `step2-apply.py` 생성(결정론) · 입력 step1-products.json · step2-research.json · literature-evidence.json · step2-step5-decisions.json · 결정 {DECISION} + _RESUME §2 2026-10-29(U1 · F8 · U2 · U8 · U9). 데이터 `step2-families.json`')
A('')
A(f'## 0. 10-29 5단계 반영 — 새 계열 {len(S5["new_families"])} · 바뀐 행 {len(S5_DELTA)} (step2-step5-decisions.json)')
A('')
A(f'계열 {len(FAMILIES)} = 기존 {len(R["families"])} + ' + ' · '.join(f"{f['id']} {f['name']}(근거 {f['evidence_level']})" for f in S5['new_families']))
A('')
A('| ledger_id | 이름 | 전 | 후 | 결정 |')
A('|---|---|---|---|---|')
for d_ in S5_DELTA:
    A(f"| `{d_['ledger_id']}` | {d_['display_name']} | {d_['before']} | {d_['after']} | {d_['decided_by']} |")
A('')
if S7_DELTA:
    A(f'## 0-1. 10-29 7단계 보강(J7) — 계열 · 하위 · 정의 {len(S7_DELTA)} (step2-step5-decisions.json)')
    A('')
    A('| 계열 | 바뀐 것 | 결정 |')
    A('|---|---|---|')
    for d_ in S7_DELTA:
        A(f"| {d_['family']} | {d_['change']} | {d_['decided_by']} |")
    A('')
A('## 1. 계열별 행 수 (주 계열 기준)')
A('')
A('| 계열 | 이름 | 행 | 그중 여러(보조 계열 있음) |')
A('|---|---|---|---|')
for c in sorted({p['family'] for p in product_family}, key=sk):
    rs = [p for p in product_family if p['family'] == c]
    A(f"| {c or '판단 필요'} | {FNAME.get(c, '' if c else 'family null')} | {len(rs)} | {sum(1 for p in rs if p['also_families'])} |")
A(f'| **합** | | **{len(product_family)}** | |')
A('')
zero = [f['id'] for f in FAMILIES if not any(p['family'] == f['id'] for p in product_family)]
A(f"제품 행 0 계열: {' · '.join(f'{z} {FNAME[z]}' for z in zero)} (시술·수액 계열 — 제품 원장에 해당 행 없음)")
A('')
A('## 2. 판정 셈')
A('')
A('| 판정 | 행 |')
A('|---|---|')
for v in ['맞음', '옮김', '여러', '계열 밖', '판단 필요']:
    A(f'| {v} | {cnt[v]} |')
A(f'| **합** | **{sum(cnt.values())}** |')
A('')
A(f'open {len(open_items)}건 · 원장님 문의(pending_director) {len(pending_director)}행 · 근거 약(evidence_level 약) {len(WEAK)}행 · 허가 ↔ 원천 충돌 기록 {sum(1 for p in product_family if p["conflict"])}행 (§6)')
A('')
A(f'### 최종 검수 v4 수정(review-step2-v4-report) — {len(V4_FIX)}행(해결안 step2-open-resolve.json v4_fix)')
A('')
A('보조 값 전수 기준: 근거가 (a) 원천 설명의 파장 숫자뿐 (b) 이 제품에 연결 안 된 허가(수출용 · 다른 품목) 이면 보조에서 뺌 · also_sub_families = {family, sub_family} 객체(W2)')
A('')
for f_ in V4_FIX:
    A(f"- `{f_['ledger_id']}` {ITEMS[f_['ledger_id']]['2_names']['display_name']}: {f_['fix']}")
A('')
A(f'### 이번 반영(open 40 해결안 · _RESUME §2 10-28) — 바뀐 행 {len(delta3)}')
A('')
A('| ledger_id | 이름 | 전(v3) | 후 | 근거 수준 |')
A('|---|---|---|---|---|')
for d_ in delta3:
    b_, a_ = d_['before'], d_['after']
    after = '원장님 문의(family null)' if a_['pending_director'] else (f"{a_['family']}" + (f"+{'·'.join(a_['also_families'])}" if a_['also_families'] else '') + f" · {a_['sub_family'] or '하위 없음'}" + (f" + 보조 {asf_txt(a_)}" if a_['also_sub_families'] else '') + f" ({a_['verdict']})")
    A(f"| `{d_['ledger_id']}` | {d_['display_name']} | {b_['family'] or 'null'} · {b_['sub_family'] or 'null'} ({b_['verdict']}) | {after} | {a_['evidence_level'] or '—'} |")
A('')
A(f'step2-research 정정 {len(ERRATA)}행 — research 의 recommended_family 가 step1 원장 위치 코드를 썼으나 같은 행 메모(「1단계 반영된 계열이 맞음」)대로 반영: ' + ' · '.join(f"{e['display_name']} {e['research_field']}→{e['applied']}" for e in ERRATA.values()))
A('')
m8 = [p for p in product_family if p['family'] == 'M8']
A(f"검수 수정(review-step2-report): F1 이름 M2 「{FNAME['M2']}」(국내 공식 출처 · 원문 재확인) · M7 「{FNAME['M7']}」 유지(품목명 {M7_FACE}/{len(M7_ROWS)}행만 해당 — 품목명은 name_basis 에만) · F2 · W1 M8 하위 {sum(1 for p in m8 if p['sub_family'])}/{len(m8)}행 채움 · null {sum(1 for p in m8 if not p['sub_family'])}행은 open · W3 M17 정의 근거 PMID 31247326 추가(28296617 = 부작용 근거) · W2 소노퀸 「D03 대상 행 · 조사 정정」 · W4 원천 수정 후보 {len(SOURCE_FIX)}건: " + ' · '.join(f"{c['display_name']} {c['field']} 「{c['value']}」" for c in SOURCE_FIX))
A('')
dual = [p for p in product_family if p['family'] == 'M8' and not p['sub_family'] and '광원 2종' in (p['sub_family_basis'] or '')]
A(f'### 이번 수정분(재검수 v2 WARN 3 · _RESUME §2 10-28) — 하위 계열 바뀐 {len(delta)}행')
A('')
A(f"M8 하위 = 광원 매질 한 축(피코초 · 프락셔널 칸 없앰 → 방식은 행 `technique_hint` + 4단계) · 광원 2종 {len(dual)}행 null + open · M7 품목명은 synonyms 에서 빼고 name_basis 에만(동의어: {' · '.join(FAMILIES[6]['synonyms'])})")
A('')
A('| ledger_id | 이름 | 전(v2) | 후 | technique_hint | 근거 |')
A('|---|---|---|---|---|---|')
for d_ in delta:
    A(f"| `{d_['ledger_id']}` | {d_['display_name']} | {d_['before'] or '—'} | {d_['after'] or '— (open)'} | {' · '.join(d_['technique_hint'] or [])} | {(d_['basis'] or '').replace('|', '/')} |")
A('')
A(f'## 3. 전후 바뀐 행 — {len(changed)}행 (step1 계열 → 2단계 주 계열)')
A('')
A('| ledger_id | 이름 | step1 | 2단계 | 판정 | 근거 |')
A('|---|---|---|---|---|---|')
for p in sorted(changed, key=lambda p: (sk(p['family']), p['display_name'])):
    A(f"| `{p['ledger_id']}` | {p['display_name']} | {p['step1_family']} | {fl(p['family'])} | {p['verdict']} | {(p['basis'] or '').replace('|', '/')} |")
A('')
A(f'## 4. 계열 {len(FAMILIES)}')
A('')
for f in FAMILIES:
    A(f"### {f['id']} {f['name']}" + (' — 새 계열' if f['new_family'] else ''))
    A('')
    A(f"- name_status: {f['name_status']} · 문헌 이름: {f['literature_name']}" + (f" · 근거 수준: {f['evidence_level']} · 결정: {f['decided_by']}" if f.get('evidence_level') else ''))
    A(f"- 정의: {f['definition']}")
    pm = [f"PMID {e['pmid']}" + (f" (DOI {e['doi']})" if e.get('doi') else '') for e in f['literature_evidence'] if e.get('pmid')]
    A(f"- 문헌 근거: {' · '.join(dict.fromkeys(pm)) or '—'}")
    for e in f['literature_evidence']:
        if e.get('decision'): A(f"- 반영: {e['decision']}")
    A(f"- 동의어: {' · '.join(f['synonyms'])}")
    A(f"- 하위 계열: {' · '.join(f['sub_families']) or '없음'}")
    if f['deferred']:
        A('- 넘김(표시만): ' + ' / '.join(f"{d['source']} → {d['deferred_to']}" for d in f['deferred']))
    if f['note']: A(f"- 메모: {f['note']}")
    A('')
A('## 5. 계열 밖 — ' + f'{len(out_of_family)}행')
A('')
for o in out_of_family:
    A(f"- {o['display_name']}(`{o['ledger_id']}`) — {o['kind']}")
A('')
A(f'## 6. open {len(open_items)} · 원장님 문의 {len(pending_director)} · 근거 약 {len(WEAK)}')
A('')
A('**원장님 문의(family null · 추천 제외 그대로)**')
A('')
for o in pending_director:
    A(f"- {o['display_name']}(`{o['ledger_id']}`) — 질문: {o['question']} · 확인되면: {o['if_confirmed']}")
A('')
A('**근거 약(값은 넣음 · 확인 질문)**')
A('')
for p in WEAK:
    A(f"- {p['display_name']}(`{p['ledger_id']}`) — {p['family']} · {p['sub_family']}" + (f" + 보조 {asf_txt(p)}" if p['also_sub_families'] else '') + f" — 확인: {p['confirm_question']}")
A('')
A('**허가 ↔ 원천 충돌 기록**')
A('')
for p in product_family:
    if p['conflict']:
        A(f"- {p['display_name']}(`{p['ledger_id']}`) — {p['conflict']}")
A('')
A(f'## 7. 제품 → 계열 {len(product_family)}행')
A('')
for c in sorted({p['family'] for p in product_family}, key=sk):
    rs = [p for p in product_family if p['family'] == c]
    A(f"### {fl(c) if c else '판단 필요(family null)'} — {len(rs)}행")
    A('')
    A('| ledger_id | 이름 | 하위 계열 | 보조 하위 | 보조 계열 | 판정 | 근거 수준 | step1 |')
    A('|---|---|---|---|---|---|---|---|')
    for p in rs:
        A(f"| `{p['ledger_id']}` | {p['display_name']} | {p['sub_family'] or '—'} | {asf_txt(p)} | {' · '.join(p['also_families'])} | {p['verdict']}{' · 원장님 문의' if p['pending_director'] else ''} | {p['evidence_level'] or ''} | {p['step1_family']} |")
    A('')
(W / 'step2-families.md').write_text('\n'.join(L) + '\n')

Q = ['# 2단계 원천(병원)에 물을 것 (2026-10-28)', '',
     '`step2-apply.py` 생성. 1단계 질문(`step1-origin-questions.md`)은 건드리지 않음. 답이 오면 그 행만 다시 판정한다.', '',
     f'## 원장님 문의 {len(pending_director)} — 정체 미확인(family null · 추천 제외 그대로)', '']
for o in pending_director:
    Q.append(f"- {o['question']} — `{o['ledger_id']}` · 확인되면: {o['if_confirmed']}")
Q += ['', f'## 근거 약 확인 {len(WEAK)} — 값은 넣어 둠(evidence_level 약)', '']
for p_ in WEAK:
    Q.append(f"- {p_['confirm_question']} — `{p_['ledger_id']}` · 지금 값: {p_['family']} · {p_['sub_family']}" + (f" + 보조 {asf_txt(p_)}" if p_['also_sub_families'] else ''))
(W / 'step2-origin-questions.md').write_text('\n'.join(Q) + '\n')
print(dict(cnt), 'open', len(open_items), 'pending', len(pending_director), 'weak', len(WEAK), 'delta3', len(delta3), 'changed', len(changed), 'zero', zero)
