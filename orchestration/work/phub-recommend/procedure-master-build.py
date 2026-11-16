# 시술 원장 확정안 v3 빌드 — taxonomy-classify-v2 + 사용자 답(1차 · 2차) + 시장가 + 제품 원장 v3 고정본
# 결정론. LLM · 외부 호출 없음. 출력: procedure-master-v3.json · procedure-master-v3.md
import json, re, glob, os, collections

W = os.path.dirname(os.path.abspath(__file__))
SRC = '/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26'
v2 = json.load(open(f'{W}/taxonomy-classify-v2.json'))
ITEMS = v2['items']
BYID = {x['id']: x for x in ITEMS}
A1 = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(f'{W}/gate-answers/classify-v1/*.json')}
A2 = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(f'{W}/gate-answers/classify-v2/answers_v2/*.json')}
MP = json.load(open(f'{SRC}/market-pricing.json'))

# ---------- 제품 원장 v3 고정본 + product-match-build.py 규칙 A ----------
_code = open(f'{W}/product-match-build.py').read()
_code = _code.replace('product-master-draft.json', 'product-master-draft-v3-frozen.json')
_code = _code.split("data={'generated_at'")[0]          # 페이지 데이터 쓰기 전까지만
_ns = {}
exec(_code, _ns)
PM = {p['id']: p for p in _ns['d']['products']}
PM_RULE = {p['id']: p['st'] for p in _ns['prods']}      # 규칙 A 적용 뒤 상태

# ---------- 부위 ----------
TREE = [  # (노드, 상위) — DEC-002 37 + _RESUME 10-27 OQ-206 추가 6
    ('얼굴', None), ('이마(묶음)', '얼굴'), ('이마', '이마(묶음)'), ('미간', '이마(묶음)'), ('관자놀이', '얼굴'),
    ('눈가(묶음)', '얼굴'), ('눈가', '눈가(묶음)'), ('눈밑', '눈가(묶음)'), ('눈꺼풀', '눈가(묶음)'),
    ('코(묶음)', '얼굴'), ('코', '코(묶음)'), ('코끝', '코(묶음)'), ('콧등', '코(묶음)'),
    ('볼(묶음)', '얼굴'), ('볼', '볼(묶음)'), ('광대', '볼(묶음)'),
    ('입가', '얼굴'), ('팔자', '입가'), ('입술', '입가'), ('입꼬리', '입가'), ('잇몸', '입가'),
    ('턱(묶음)', '얼굴'), ('턱끝', '턱(묶음)'), ('턱선', '턱(묶음)'), ('사각턱', '턱(묶음)'), ('턱밑', '턱(묶음)'),
    ('얼굴 전체', '얼굴'), ('목(묶음)', None), ('목', '목(묶음)'), ('승모근', '목(묶음)'), ('두피', None),
    ('바디', None), ('겨드랑이', '바디'), ('팔뚝', '바디'), ('복부', '바디'), ('허벅지', '바디'), ('종아리', '바디'),
    ('전신', '바디'), ('손', '바디'), ('발', '바디'), ('다리', '바디'), ('비키니', '바디'), ('힙', '바디'),
]
ADDED = {'콧등', '손', '발', '다리', '비키니', '힙'}
TREE_NAMES = {n for n, _ in TREE}
NA = '해당 없음'          # 수액 · 성분 주사(DEC-003 OQ-306 처리: 「전신」과 분리)
OUT_OF_TREE = {'옆구리', '등', '브라라인', '엉덩이', '콧망울', '하관', '페이스'}  # _RESUME §1 미결 · v2 where_unmapped
def site_norm(s):
    if not s: return None
    if s in ('(부위 해당 없음)',): return NA
    return s
def site_status(s):
    if s is None: return 'missing'
    if s == NA: return 'not_applicable'
    if s in TREE_NAMES: return 'added' if s in ADDED else 'tree'
    return 'out_of_tree'

# ---------- 계열 ----------
FAM_TERM = {'M1': '보톡스', 'M2': '필러', 'M3': '콜라겐부스터', 'M4': '스킨부스터', 'M5': 'PRP', 'M6': '지방이식',
            'M7': '실리프팅', 'M8': '레이저', 'M9': '리프팅', 'M10': 'EMS', 'M11': '니들RF', 'M12': 'MTS',
            'M13': '플라즈마', 'M14': '냉각지방분해', 'M15': '스킨케어', 'M16': '수액', 'M17': '줄기세포',
            'X1': '지방분해주사', 'X2': '카복시', 'X3': '메조 주사', 'X4': '성장호르몬 주사', 'X5': '태반주사', 'X6': 'RF 지방감소'}
OFFICIAL = {'M1': ('보툴리눔 톡신', 'decided', '_RESUME §2 10-27 「계열 이름 = 공식 일반명(M1 → 보툴리눔 톡신)」')}
# 사용자 1차 답 ③(「무엇을 틀림: 수액치료 아니라 …」)으로 생긴 계열 — 문구는 사용자 답 그대로, 부위 · 기법 낱말만 뗐다
EXTRA = {
    '국소 지방분해주사': ('X1', '국소 주사'), '피하 지방분해주사': ('X1', '피하 주사'), '콜산(CA) 국소 지방분해제': ('X1', '국소 주사'),
    '피하 CO2 가스 주입': ('X2', '피하 주사'), '두피 국소 메조 주사': ('X3', '메조테라피'),
    '성장호르몬 피하주사': ('X4', '피하 주사'), '피하주사용 태반제제': ('X5', '피하 주사'), 'RF 지방감소': ('X6', None),
}
EXTRA_FAM = {
    'X1': ('지방분해주사', ['국소 지방분해주사', '피하 지방분해주사', '콜산(CA) 국소 지방분해제', 'DCA (지방세포파괴)'], 'DCA 7 · 뉴비쥬 · PPC — 1차 답 ③ 「수액치료 아니라 국소/피하 지방분해주사」'),
    'X2': ('CO2 가스(카복시테라피)', ['피하 CO2 가스 주입', '카복시', '카복시테라피'], '카복시테라피 — 1차 답 ③'),
    'X3': ('국소 메조 주사(약물)', ['두피 국소 메조 주사'], '미녹시딜 두피 메조 — 1차 답 ③'),
    'X4': ('성장호르몬', ['성장호르몬 피하주사'], '성장호르몬주사 — 1차 답 ③'),
    'X5': ('태반제제', ['피하주사용 태반제제'], '태반주사멜스몬 — 1차 답 ③'),
    'X6': ('RF 지방감소', ['RF 지방감소'], '트루스컬프트 — 1차 답 ③ 「EMS 아니라 RF 지방감소」'),
}
MOD_SUBS_KEEP = {'M3', 'M4', 'M5', 'M8', 'M9', 'M13', 'M15', 'M16', 'M17'}  # 하위 분류가 재료 · 원리를 가르는 시술군
def parse_what(what, item=None):
    """v2 what → (계열 id, 하위 계열, 성분/재료). 사용자 ③ 계열은 EXTRA."""
    for k, (fid, _) in EXTRA.items():
        if what.startswith(k):
            rest = what[len(k):].strip(' ·')
            return fid, None, rest or None
    if what == '초음파 장비':   # LDM초음파관리 — 1차 답 ③ 「수액치료 아니라 초음파 장비」 → 같은 장비 LDM(M15-4-1)의 자리
        return 'M15', '초음파관리', None
    m = re.match(r'(M\d+)\s+[^·]+?(?:\s·\s(.+))?$', what)
    fid = m.group(1); rest = m.group(2)
    if not rest: return fid, None, None
    parts = [p.strip() for p in rest.split(' · ')]
    sub = parts[0]; ing = parts[1] if len(parts) > 1 else None
    if fid not in MOD_SUBS_KEEP: return fid, None, None
    if fid == 'M5': sub = sub.split(' (')[0]          # 「PRP (혈소판풍부혈장)」 = 「PRP」
    if fid == 'M16' and sub == '지방분해주사 (마케팅명)': sub = '지방분해주사'
    if fid == 'M16' and sub not in ('지방분해주사', 'DCA (지방세포파괴)'):
        # 수액: 하위 분류(미백/항산화 …)는 목적 이름. 성분이 적혀 있으면 성분을 둔다
        return fid, None, sub if sub not in [s['label'] for s in MODS['M16']['subcategories']] else None
    return fid, sub, ing
MODS = {m['id']: m for m in v2['modalities']}

# ---------- 기법 묶음 (원천 표현 → 큰 기법). 큰 기법 이름은 원천 표현 · 사용자 답 문구에서만 고른다 ----------
TECH = collections.OrderedDict([
    ('근육축소', ['근육축소', '교근축소']),
    ('스킨보톡스', ['스킨보톡스']),
    ('네페르티티 리프트', ['네페르티티 리프트']),
    ('토닝', ['토닝', '532nm 포커스 토닝', '포커스 토닝', '피코토닝', '알렉스토닝', '듀얼 토닝', '제네시스토닝']),
    ('박피성 프락셔널', ['박피성']),
    ('비박피성 프락셔널', ['비박피성', '비박리성', '비박피성 피코 프락셀']),
    ('프락셔널', ['프락셔널', '프락셀', '피코슈어 프락셔널', '얕은 박피']),
    ('BBL 시술 프로토콜', ['BBL 시술 프로토콜', 'BBL 여드름 시술 프로토콜']),
    ('일반 레이저 방식', ['루비', 'KTP']),
    ('4단계리프팅', ['4단계리프팅']),
    ('모노폴라', ['모노폴라']),
    ('바이폴라', ['바이폴라', '양극성']),
    ('침습+비침습', ['침습+비침습']),
    ('마이크로웨이브', ['마이크로웨이브', '극초단파']),
    ('캐비테이션', ['캐비테이션']),
    ('석션', ['석션']),
    ('냉각', ['냉각']),
    ('코그', ['코그', '코그(Cog)', 'Cog', '양방향', '단방향']),
    ('모노', ['모노']),
    ('볼륨실', ['볼륨실']),
    ('2방향', ['2방향']), ('다방향', ['다방향']), ('전방향', ['전방향']), ('콘', ['콘']), ('오메가 형태', ['오메가 형태']),
    ('루프형', ['루프형']), ('텐션형', ['텐션형']), ('벌집형', ['벌집형']), ('몰딩 메쉬', ['몰딩 메쉬']),
    ('롤러형', ['롤러형']),
    ('스탬프형', ['스탬프형', '전동 스탬프형']),
    ('전동', ['전자동', '펜타입', '진동형']),
    ('멀티니들', ['멀티니들']),
    ('니들리스', ['니들리스', '공기압 주입', '제트 주입', '공기압 약물주입']),
    ('분사', ['분사']),
    ('초음파 주입', ['초음파 주입']),
    ('이온도입', ['이온도입', '전류 약물침투']),
    ('전기천공', ['전기천공']),
    ('워터제트', ['워터제트', '고압 워터젯', '물 흡인']),
    ('미세박피', ['미세박피']),
    ('중간~심층', ['중간~심층']),
    ('심부필링', ['심부필링']),
    ('CROSS 기법', ['CROSS 기법']),
    ('도포', ['도포', '국소 적용']),
    ('마사지', ['마사지', '림프순환']),
    ('섬유 밴드 절단', ['섬유 밴드 절단']),
    ('압박', ['압박']),
    ('펀치이식', ['펀치이식']),
    ('압출', ['압출']),
    ('광역학치료', ['광역학치료']),
    ('원심분리', ['원심분리']),
    ('미세 지방 주입', ['미세 지방 주입']),
    ('초미세', ['초미세']),
    ('SVF(줄기세포 포함)', ['SVF(줄기세포 포함)']),
    ('메조테라피', ['메조테라피']),
    ('진피 주입', ['진피 주입']),
    ('피하 주사', ['피하주입', '피하']),                      # 「피하」 = 사용자 1차 답 ③ 문구
    ('국소 주사', ['국소']),                                  # 「국소」 = 사용자 1차 답 ③ 문구
    ('병변내 주사', ['병변내 주사']),
    ('정맥 주사', ['IV', '정맥주사']),                         # DEC-003 D-05 문구. 단 수액은 OQ-308 처리로 허가 용법 확인 대기
    ('주입', ['주입', '주사', '두피 주입']),
    # OQ-310 · OQ-311 임시값(첫 선택지 = 기법 축)으로 기법이 된 도구 · 방식명
    ('IPL', ['IPL']), ('BBL스킨타이트', ['BBL스킨타이트']), ('알렉산드라이트', ['알렉산드라이트']),
    ('콜드플라즈마', ['콜드플라즈마']),
])
EXPR2T = {e: t for t, es in TECH.items() for e in es}
TPRI = list(TECH.keys())
def tech_of(exprs):
    ts = [EXPR2T[e] for e in exprs if e in EXPR2T]
    if not ts: return None
    fr = [t for t in ts if t in ('박피성 프락셔널', '비박피성 프락셔널')]
    if fr: return fr[0]
    ts = list(dict.fromkeys(ts))
    return ts[0] if len(ts) == 1 else ts[0]
TECH_ITEM_NAMES = collections.defaultdict(list)   # 큰 기법 ← 원장 항목 이름(기법 kind)

# ---------- 상태 · 답 ----------
def approval_of(x):
    a2 = A2.get(x['id'])
    if a2:
        if a2.get('decision') == 'approve': return 'approved', None
        if a2.get('decision') == 'reject': return 'hold', '2차 반려: ' + (a2.get('reason') or '')
        if a2.get('decision') == 'answer':
            if a2.get('choice') is not None: return 'approved', '2차 답: ' + str(a2['choice'])
            return 'hold', '2차 답(직접 입력): ' + (a2.get('other') or '')
    return {'approved': 'approved', 'regate': 'regate_pending', 'waiting_mfds': 'waiting_mfds', 'question': 'provisional'}[x['status']], None

# ---------- 단위 시술 모음 ----------
UPS = collections.OrderedDict()
def up_add(fam, sub, site, tech, *, item=None, market=None, device=None, approval=None, provisional_q=None,
           how_src=(), ingredient=None, purpose=None, route_status=None, extra_syn=(), uniq=None, note=None, ev=None, product=None):
    site = site_norm(site)
    key = (fam, sub, site, tech, uniq)
    u = UPS.get(key)
    if not u:
        u = UPS[key] = {'family': fam, 'sub_family': sub, 'site': site, 'site_status': site_status(site), 'technique': tech,
                        'ingredient': ingredient, 'route_status': route_status,
                        'source_items': [], 'source_market': [], 'devices': [], 'synonyms': [], 'how_source': [],
                        'purposes': [], 'approvals': [], 'provisional_questions': [], 'notes': [], 'evidence': [], 'product_item_ids': []}
    if item and item not in u['source_items']: u['source_items'].append(item)
    if market and market not in u['source_market']: u['source_market'].append(market)
    if device and device not in u['devices']: u['devices'].append(device)
    for h in how_src:
        if h not in u['how_source']: u['how_source'].append(h)
    for p in (purpose or []):
        if p not in u['purposes']: u['purposes'].append(p)
    if approval: u['approvals'].append(approval)
    if provisional_q and provisional_q not in u['provisional_questions']: u['provisional_questions'].append(provisional_q)
    for s in extra_syn:
        if s and s not in [y['text'] for y in u['synonyms']]: u['synonyms'].append({'text': s, 'type': 'source_expression'})
    if note and note not in u['notes']: u['notes'].append(note)
    if ev and ev not in u['evidence']: u['evidence'].append(ev)
    if product and product not in u['product_item_ids']: u['product_item_ids'].append(product)
    return key
def ev_item(iid):
    x = BYID[iid]
    return {'file': 'taxonomy.json', 'path': f"modality {x['modality']} · {x['subcategory']}", 'item': iid, 'text': x['source_text'].split(' | ')[0]}
def syn(key, text, typ):
    u = UPS[key]
    if text and text not in [y['text'] for y in u['synonyms']]:
        u['synonyms'].append({'text': text, 'type': typ})

LEDGER = []
PROV = []
def dest(t, **kw): return dict(type=t, **kw)

for x in ITEMS:
    iid = x['id']; kind = x['kind']; q = x['question']
    appr, appr_note = approval_of(x)
    prov = appr == 'provisional'
    opt = q['options'][0] if (prov and q) else None
    fam, sub, ing = parse_what(x['what'])
    tech_item = tech_of(x['how_source'])
    row = {'id': iid, 'name': x['name'], 'modality': x['modality'], 'kind_v2': kind, 'status_v2': x['status'],
           'answer_v1': (A1.get(iid) or {}).get('decision'), 'answer_v2': (A2.get(iid) or {}).get('decision'),
           'approval': appr, 'approval_note': appr_note, 'provisional': prov, 'question': q['oq'] if q else None,
           'applied_option': opt, 'family': fam, 'destinations': [], 'note': ''}
    if prov: PROV.append({'id': iid, 'name': x['name'], 'oq': q['oq'], 'applied': opt, 'options': q['options']})
    D = row['destinations']
    oq = q['oq'] if q else None

    if appr == 'hold':
        D.append(dest('hold', reason=appr_note))
        if kind in ('product', 'device'):
            D.append(dest(kind, product_master_id=iid, match_status=PM.get(iid, {}).get('match', {}).get('status'),
                          match_status_rule_a=PM_RULE.get(iid)))
        LEDGER.append(row); continue

    # --- 임시값 분기(첫 선택지) ---
    if prov and oq == 'OQ-312':          # 동의어로 두고 무엇을 = 성분(성분 확인 전까지 보류)
        D.append(dest('hold', reason='OQ-312 임시값: 마케팅명은 동의어, 「무엇을」 = 성분 — 성분 확인 전까지 보류'))
        LEDGER.append(row); continue
    if prov and oq == 'OQ-309':          # 실 재질 = 「무엇을」(실리프팅) 하위 계열
        D.append(dest('family', family='M7', sub_family=x['name']))
        LEDGER.append(row); continue
    if prov and oq == 'OQ-315':          # 재료(제품 속성)
        D.append(dest('material', material=x['name'], family=fam))
        LEDGER.append(row); continue
    if prov and oq == 'OQ-313':          # 실제 패키지 — 구성 원천 없음
        D.append(dest('package', components=[], components_source='없음(OQ-204) — 구성 원천을 정해야 묶을 수 있다'))
        LEDGER.append(row); continue
    if prov and oq == 'OQ-311' and kind == 'device':   # BBL스킨타이트 — 기법 축
        D.append(dest('technique', technique=x['name']))
        TECH_ITEM_NAMES[x['name']].append(x['name'])
        LEDGER.append(row); continue
    if prov and oq == 'OQ-314' and x['name'] == '쿨미니':   # 본 장비(쿨스컬프팅)의 속성 · 동의어
        k = up_add('M14', None, '턱밑', None, item=iid, device='M14-1-1', approval=appr, provisional_q='OQ-314', ev=ev_item(iid), product=iid)
        syn(k, '쿨미니', 'device_accessory')
        D.append(dest('device_attribute', of_device='M14-1-1', product_master_id=iid))
        D.append(dest('unit_procedure', key=k))
        LEDGER.append(row); continue
    if prov and oq == 'OQ-314' and x['name'] == '엑소좀 두피주사':  # 재료 계열(엑소좀) × 두피
        k = up_add('M4', '엑소좀/성장인자', '두피', '주입', item=iid, approval=appr, provisional_q='OQ-314',
                   how_src=x['how_source'], purpose=x['purpose'], ev=ev_item(iid),
                   note='엑소좀 재료 계열은 M4(ASCE+엑소좀 M4-3-1 · 고민 P13-1 「두피엑소좀(ASCE+)」)에 댔다 — M17 엑소좀과 통합 여부 미정')
        syn(k, x['name'], 'ledger_item')
        D.append(dest('unit_procedure', key=k))
        LEDGER.append(row); continue

    # --- kind 별 ---
    if kind == 'product':
        D.append(dest('product', product_master_id=iid, product_name=PM.get(iid, {}).get('product_name'),
                      products_key=PM.get(iid, {}).get('products_key'),
                      match_status=PM.get(iid, {}).get('match', {}).get('status'), match_status_rule_a=PM_RULE.get(iid)))
    elif kind == 'device':
        D.append(dest('device', product_master_id=iid, match_status=PM.get(iid, {}).get('match', {}).get('status'),
                      match_status_rule_a=PM_RULE.get(iid)))
        for w in x['where']:
            k = up_add(fam, sub, w, tech_item, item=iid, device=iid, approval=appr, how_src=x['how_source'], ev=ev_item(iid), product=iid)
            syn(k, x['name'], 'device')
            D.append(dest('unit_procedure', key=k))
    elif kind in ('other',):
        D.append(dest('not_procedure', reason='약물 · 외용제(kind other) — 시술 아님. 제품/성분 원장 후보'))
    elif kind == 'unclear':
        D.append(dest('hold', reason='판정 불가 — 식약처 원장 대기' if x['status'] == 'waiting_mfds' else '판정 불가'))
    elif kind == 'package':
        comps = []
        for w in x['where']:
            comps.append({'family': fam, 'site': w})
        D.append(dest('package', components=comps,
                      components_source='원천 detail 의 부위만(구성 단위 시술 원천 없음 — OQ-204)' if comps else '없음(OQ-204)'))
        row['_pkg'] = comps
    if kind == 'technique' and not x['unit_procedures']:
        t = tech_item or x['name']
        D.append(dest('technique', technique=t))
        TECH_ITEM_NAMES[t].append(x['name'])
    if kind == 'purpose':
        D.append(dest('purpose', purposes=x['purpose'] or [x['name']]))
    if x['unit_procedures'] and kind in ('unit_procedure', 'technique', 'purpose'):
        for u in x['unit_procedures']:
            f2, s2, ing2 = parse_what(u['what'])
            site = u['where'] or None
            if prov and oq == 'OQ-307' and not site: site = '얼굴 전체'
            how = u['how']
            if how.startswith('('): how = ''
            t = tech_of([how]) if how else None
            if how and not t: t = how
            if prov and oq in ('OQ-310', 'OQ-311') and not t: t = tech_of([x['name']]) or x['name']
            route = None; uniq = None; ingredient = ing2
            if f2 == 'M16' and not site:
                if s2 == '지방분해주사':
                    uniq = iid                        # 성분 미상 · 부위 없음 — 서로 다른 약제를 하나로 합치지 않는다
                else:
                    site = '(부위 해당 없음)'          # 수액 · 성분 주사 = DEC-003 OQ-306 처리(식약처 대기 항목에도 같은 자리)
            if site_norm(site) == NA:
                route = '허가 용법 확인 대기'        # DEC-003 OQ-308 처리
                uniq = iid                            # 수액은 성분마다 다른 시술 — 항목 하나 = 단위 시술 하나
                ingredient = ing2 or x['name']
            if f2 in ('X1', 'X2', 'X4', 'X5') and not t:
                t = EXTRA[[k for k, v in EXTRA.items() if v[0] == f2 and u['what'].startswith(k)][0]][1]
            if f2 == 'X3' and not t: t = '메조테라피'
            if f2 == 'X1':                            # 성분이 단위 시술을 가르면 안 된다 — 성분은 제품 속성
                ingredient = ing2;
            k = up_add(f2, s2, site, t, item=iid, approval=appr, provisional_q=oq if prov else None,
                       how_src=x['how_source'] + ([how] if how and how not in x['how_source'] else []),
                       ingredient=ingredient, purpose=x['purpose'], route_status=route, uniq=uniq, ev=ev_item(iid))
            syn(k, x['name'], 'ledger_item')
            if u['where'] == '' and site == '얼굴 전체' and prov: UPS[k]['notes'].append('OQ-307 임시값 「얼굴 전체」')
            D.append(dest('unit_procedure', key=k))
        if kind == 'technique':
            TECH_ITEM_NAMES[tech_of(x['how_source']) or x['name']].append(x['name'])
    LEDGER.append(row)

# ---------- 시장가 → 단위 시술 (이름에 부위가 적힌 줄만) ----------
# (시장가 항목 이름, 계열, 하위 계열, 부위들, 기법, 연결 원장 항목, 장비, 등급/제품 메모)
MARKET = [
    ('이마 주름 (수입)', 'M1', None, ['이마'], None, None, None, '등급 수입'), ('이마 주름 (국산)', 'M1', None, ['이마'], None, None, None, '등급 국산'),
    ('미간 주름 (수입)', 'M1', None, ['미간'], None, None, None, '등급 수입'), ('미간 주름 (국산)', 'M1', None, ['미간'], None, None, None, '등급 국산'),
    ('눈가 주름 (수입)', 'M1', None, ['눈가'], None, None, None, '등급 수입'), ('눈가 주름 (국산)', 'M1', None, ['눈가'], None, None, None, '등급 국산'),
    ('사각턱 (수입)', 'M1', None, ['사각턱'], '근육축소', 'M1-3-2', None, '등급 수입'), ('사각턱 (국산)', 'M1', None, ['사각턱'], '근육축소', 'M1-3-2', None, '등급 국산'),
    ('승모근', 'M1', None, ['승모근'], None, 'M1-3-3', None, None), ('목주름 (네페르티티)', 'M1', None, ['목'], None, None, None, '「네페르티티」'),
    ('팔자주름 (HA 1cc)', 'M2', None, ['팔자'], None, None, None, 'HA 1cc'), ('입술 볼륨 (HA 1cc)', 'M2', None, ['입술'], None, None, None, 'HA 1cc'),
    ('코 필러 (HA 1cc)', 'M2', None, ['코'], None, None, None, 'HA 1cc'), ('턱 끝 볼륨 (HA 1cc)', 'M2', None, ['턱끝'], None, None, None, 'HA 1cc'),
    ('이마 볼륨 (HA 2cc)', 'M2', None, ['이마'], None, None, None, 'HA 2cc'), ('볼 볼륨 (HA 1cc)', 'M2', None, ['볼'], None, None, None, 'HA 1cc'),
    ('눈밑 꺼짐 (HA 1cc)', 'M2', None, ['눈밑'], None, None, None, 'HA 1cc'), ('관자놀이 (HA 2cc)', 'M2', None, ['관자놀이'], None, None, None, 'HA 2cc'),
    ('스킨부스터 물광주사 (전체얼굴)', 'M4', 'HA (물광)', ['얼굴 전체'], None, None, None, None),
    ('엑소좀 (전체얼굴)', 'M4', '엑소좀/성장인자', ['얼굴 전체'], None, None, None, 'OQ-314 임시값(재료 계열 엑소좀)'),
    ('엑소좀 (두피)', 'M4', '엑소좀/성장인자', ['두피'], '주입', None, None, 'OQ-314 임시값(재료 계열 엑소좀)'),
    ('PRP (전체얼굴)', 'M5', 'PRP', ['얼굴 전체'], None, None, None, 'PRP 항목(M5-1-1)은 2차 반려(확인 필요) — 시장가 줄만 근거'),
    ('PRP (두피)', 'M5', 'PRP', ['두피'], None, None, None, None),
    ('이마 지방이식', 'M6', None, ['이마'], None, None, None, None), ('볼 지방이식', 'M6', None, ['볼'], None, None, None, None),
    ('눈밑 지방이식', 'M6', None, ['눈밑'], None, None, None, None), ('풀페이스 지방이식', 'M6', None, ['얼굴 전체'], None, None, None, None),
    ('관자놀이 지방이식', 'M6', None, ['관자놀이'], None, None, None, None), ('턱 끝 지방이식', 'M6', None, ['턱끝'], None, None, None, None),
    ('나노 지방이식 (전체얼굴)', 'M6', None, ['얼굴 전체'], '초미세', 'M6-2-1', None, None),
    ('코 실리프팅', 'M7', None, ['코'], None, None, None, None), ('풀페이스 실리프팅 (20줄 이상)', 'M7', None, ['얼굴 전체'], None, None, None, '20줄 이상'),
    ('목 실리프팅', 'M7', None, ['목'], None, None, None, None),
    ('피코토닝 (전체얼굴)', 'M8', '색소/토닝', ['얼굴 전체'], '토닝', 'M8-1-2', None, None),
    ('피코프락셀 (전체얼굴)', 'M8', '프락셔널', ['얼굴 전체'], '비박피성 프락셔널', 'M8-2-5', None, None),
    ('CO2 프락셔널 (전체얼굴)', 'M8', '프락셔널', ['얼굴 전체'], '박피성 프락셔널', 'M8-2-1', None, None),
    ('IPL (전체얼굴)', 'M8', 'IPL', ['얼굴 전체'], 'IPL', 'M8-3-1', None, 'OQ-311 임시값(IPL = 기법)'),
    ('레이저 제모 (겨드랑이)', 'M8', '제모', ['겨드랑이'], None, None, None, None), ('레이저 제모 (전신)', 'M8', '제모', ['전신'], None, None, None, '전신 = 몸 표면(OQ-306 처리)'),
    ('울쎄라 (풀페이스)', 'M9', 'HIFU (초음파)', ['얼굴 전체'], None, None, 'M9-1-1', None), ('울쎄라 (턱라인)', 'M9', 'HIFU (초음파)', ['턱선'], None, None, 'M9-1-1', '턱라인 = 턱선'),
    ('슈링크 유니버스 (풀페이스)', 'M9', 'HIFU (초음파)', ['얼굴 전체'], None, None, 'M9-1-4', None), ('슈링크 유니버스 (턱라인)', 'M9', 'HIFU (초음파)', ['턱선'], None, None, 'M9-1-4', '턱라인 = 턱선'),
    ('더블로골드 (풀페이스)', 'M9', 'HIFU (초음파)', ['얼굴 전체'], None, None, 'M9-1-6', None),
    ('써마지 FLX (풀페이스 900샷)', 'M9', 'RF (고주파)', ['얼굴 전체'], '모노폴라', None, 'M9-2-1', '900샷'),
    ('써마지 FLX (눈가 450샷)', 'M9', 'RF (고주파)', ['눈가'], '모노폴라', None, 'M9-2-1', '450샷'),
    ('인모드 (풀페이스)', 'M9', 'RF (고주파)', ['얼굴 전체'], '바이폴라', None, 'M9-2-5', None),
    ('이모드 (복부)', 'M10', None, ['복부'], None, None, None, '장비 「이모드」 원장에 없음'), ('이모드 (힙)', 'M10', None, ['힙'], None, None, None, '장비 「이모드」 원장에 없음'),
    ('이모드 (복부+힙 동시)', 'M10', None, ['복부', '힙'], None, None, None, '두 부위 동시 — 패키지 후보'),
    ('EMS 바디 (팔뚝/허벅지)', 'M10', None, ['팔뚝', '허벅지'], None, None, None, None),
    ('시크릿 (전체얼굴)', 'M11', None, ['얼굴 전체'], None, None, None, '「시크릿」 ≠ 원장 「시크릿RF」 표기 — 자동 연결 안 함'),
    ('인피니 (전체얼굴)', 'M11', None, ['얼굴 전체'], None, None, 'auto-M11-1775364775143', None),
    ('모피어스8 (전체얼굴)', 'M11', None, ['얼굴 전체'], None, None, None, '「모피어스8」 ≠ 원장 「모르페우스8」 표기 — 자동 연결 안 함'),
    ('포텐자 (전체얼굴)', 'M11', None, ['얼굴 전체'], None, None, 'M11-1-1', None),
    ('니들RF (목주름)', 'M11', None, ['목'], None, None, None, None),
    ('MTS (전체얼굴)', 'M12', None, ['얼굴 전체'], None, None, None, None), ('더마펜4 (전체얼굴)', 'M12', None, ['얼굴 전체'], None, None, 'auto-M12-1775363026852', None),
    ('MTS (두피 탈모)', 'M12', None, ['두피'], None, None, None, None),
    ('플라즈마 리프팅 (전체얼굴)', 'M13', None, ['얼굴 전체'], None, None, None, None), ('플라즈마 (눈가 주름)', 'M13', None, ['눈가'], None, None, None, None),
    ('플라즈마 (눈꺼풀 처짐 비수술)', 'M13', None, ['눈꺼풀'], None, None, None, None),
    ('쿨스컬프팅 (복부 1부위)', 'M14', None, ['복부'], None, None, 'M14-1-1', '1부위'), ('쿨스컬프팅 (턱밑 이중턱)', 'M14', None, ['턱밑'], None, None, 'M14-1-1', '1부위'),
    ('쿨스컬프팅 (허벅지 안쪽 양쪽)', 'M14', None, ['허벅지'], None, None, 'M14-1-1', '양쪽'), ('쿨스컬프팅 (팔뚝 양쪽)', 'M14', None, ['팔뚝'], None, None, 'M14-1-1', '양쪽'),
    ('아쿠아필 (전체얼굴)', 'M15', '딥클렌징', ['얼굴 전체'], '워터제트', None, 'M15-2-1', None),
    ('LED 광선치료 (전체얼굴)', 'M15', '광치료(LED)', ['얼굴 전체'], None, None, None, None),
    ('줄기세포 배양액 주입 (전체얼굴)', 'M17', None, ['얼굴 전체'], '주입', None, None, '재료 줄기세포배양액(OQ-315 임시값 = 제품 속성)'),
    ('줄기세포 엑소좀 (전체얼굴)', 'M17', None, ['얼굴 전체'], None, None, None, '재료 줄기세포유래 엑소좀(OQ-315 임시값 = 제품 속성)'),
    ('줄기세포 두피치료 (탈모)', 'M17', None, ['두피'], None, None, None, None),
]
MARKET_SKIPPED = []
_mnames = {r[0] for r in MARKET}
for c in MP['categories']:
    for i in c['items']:
        if i['name'] not in _mnames: MARKET_SKIPPED.append(f"{c['id']} {i['name']}")
# 원천에 그대로 있는지 확인
_all_market = {i['name'] for c in MP['categories'] for i in c['items']}
assert _mnames <= _all_market, _mnames - _all_market
for (mname, fam, sub, sites, tech, link, devid, memo) in MARKET:
    for s in sites:
        appr = 'provisional' if memo and '임시값' in memo else 'source_only'
        if tech is None:
            # 시장가는 기법을 적지 않는다 — 같은 계열 · 하위 계열 · 부위의 단위 시술이 하나뿐이면 거기에 붙인다
            same = [k for k in UPS if k[0] == fam and k[1] == sub and k[2] == s]
            if len(same) == 1: tech = same[0][3]
        k = up_add(fam, sub, s, tech, market=mname, device=devid, approval=appr, product=devid,
                   ev={'file': 'market-pricing.json', 'path': f'categories {fam}', 'item': mname, 'text': mname},
                   provisional_q=re.search(r'OQ-\d+', memo).group(0) if memo and '임시값' in memo else None,
                   note=memo if memo and ('표기' in memo or '원장에 없음' in memo or '패키지' in memo or '반려' in memo) else None)
        if link:
            UPS[k]['source_items'].append(link) if link not in UPS[k]['source_items'] else None
            syn(k, BYID[link]['name'], 'ledger_item')
        if devid: syn(k, BYID[devid]['name'], 'device')
        base = re.sub(r'\s*\(.*?\)', '', mname).strip()
        syn(k, base, 'market')
        if '시크릿' in mname or '모피어스' in mname or '이모드' in mname: syn(k, base, 'device_name_unlinked')

# ---------- 적응증 · 고민 트리 → 계열 × 부위 (SPEC-004 R-1) ----------
# 부위는 트리 노드 이름(과 DEC-002 가 그 부위 근거로 센 표현)이 낱말로 나올 때만 잡는다
SITE_ALIAS = {'전체얼굴': '얼굴 전체', '전체 얼굴': '얼굴 전체', '얼굴 전체': '얼굴 전체', '풀페이스': '얼굴 전체',
              '턱 선': '턱선', '턱라인': '턱선', '턱 라인': '턱선', '턱 끝': '턱끝',
              '이중턱': '턱밑', '애교': '눈밑', '다크서클': '눈밑'}       # 이중턱 · 애교 · 다크서클 = DEC-002 노드별 원천 근거의 표현
SITE_WORDS = sorted([n for n in TREE_NAMES if '(' not in n and n not in ('얼굴', '바디', '입가')] + list(SITE_ALIAS) + ['입가'],
                    key=len, reverse=True)
OK_SUFFIX = ('주름', '필러', '볼륨', '라인', '꺼짐', '처짐', '쳐짐', '탄력', '리프팅', '실리프팅', '축소', '보톡스', '지방', '살', '뼈',
             '부위', '윤곽', '모양', '거상', '연장', '함몰', '이완', '과', '와', '의', '을', '를', '이', '도', '등', '쪽')
HANGUL = re.compile(r'[가-힣]')
REJECTED = []
def find_sites(text, ctx):
    found = []; t = text
    i = 0
    while i < len(t):
        hit = None
        for w in SITE_WORDS:
            if t.startswith(w, i):
                hit = w; break
        if not hit: i += 1; continue
        prev = t[i-1] if i else ' '
        nxt = t[i+len(hit):i+len(hit)+4]
        site = SITE_ALIAS.get(hit, hit)
        if HANGUL.match(prev) and hit not in SITE_ALIAS:
            REJECTED.append({**ctx, 'word': hit, 'reason': '앞 글자가 붙어 있음(다른 낱말의 일부)', 'context': t[max(0,i-6):i+len(hit)+6]})
        elif nxt and HANGUL.match(nxt[0]) and not nxt.startswith(OK_SUFFIX):
            REJECTED.append({**ctx, 'word': hit, 'reason': '뒤 글자가 붙어 있음(다른 낱말의 일부)', 'context': t[max(0,i-6):i+len(hit)+6]})
        else:
            if site not in found: found.append(site)
        i += len(hit)
    return found
def same_keys(fam, sub, site, strict_sub=True):
    return [k for k in UPS if k[0] == fam and k[2] == site and k[4] is None and (k[1] == sub if strict_sub else True)]
INDICATION_UPS = collections.Counter(); PROBLEM_UPS = collections.Counter()
HOLD_IDS = {r['id'] for r in LEDGER if r['approval'] == 'hold'}
for x in ITEMS:
    if x['kind'] not in ('product', 'device') or x['id'] in HOLD_IDS: continue
    st = x['source_text']; j = st.find('적응증:')
    if j < 0: continue
    ind = st[j+4:].strip()
    fam, sub, _ = parse_what(x['what'])
    tech = tech_of(x['how_source']) if x['kind'] == 'device' else None
    for site in find_sites(ind, {'source': 'indication', 'item': x['id'], 'name': x['name'], 'family': fam}):
        ev = {'file': 'taxonomy.json', 'path': f"modality {x['modality']} · {x['subcategory']} · extracted.indications", 'item': x['id'], 'text': f"{x['name']} 적응증: {ind}"}
        r0 = next(r for r in LEDGER if r['id'] == x['id'])
        ap_i = {'waiting_mfds': 'waiting_mfds', 'provisional': 'provisional'}.get(r0['approval'], 'source_only')
        ks = same_keys(fam, sub, site)
        if tech: ks = [k for k in ks if k[3] == tech]        # 장비 기법이 있으면 같은 기법의 단위 시술에만
        if not ks:
            ks = [up_add(fam, sub, site, tech, approval=ap_i, ev=ev, product=x['id'])]; INDICATION_UPS[fam] += 1
        for k in ks:
            up_add(*k[:4], uniq=k[4], ev=ev, product=x['id'], approval=ap_i,
                   provisional_q=r0['question'] if ap_i == 'provisional' else None)
            if x['kind'] == 'device': syn(k, x['name'], 'device')   # 제품 이름은 동의어가 아니라 product_item_ids 로만(제품은 별도 노드)
        for k in ks:
            r = next(r for r in LEDGER if r['id'] == x['id'])
            if not any(d.get('key') == k for d in r['destinations']):
                r['destinations'].append(dest('unit_procedure', key=k, via='indication'))
TAX = json.load(open(f'{SRC}/taxonomy.json'))
for P in TAX['problem']:
    for sc in P['subcategories']:
        lab_sites = find_sites(sc['label'], {'source': 'problem_label', 'item': sc['id'], 'name': sc['label']})
        for it in sc.get('items', []):
            refs = it.get('modality_ref') or []
            text = it['name'] + ' ' + (it.get('detail') or '')
            ctx = {'source': 'problem_item', 'item': it['id'], 'name': it['name'], 'label': f"{sc['id']} {sc['label']}"}
            sites = find_sites(text, ctx)
            if not sites:
                for ls in lab_sites:
                    for fam in refs:
                        REJECTED.append({**ctx, 'family': fam, 'word': ls, 'reason': '하위 라벨에만 있는 부위 — 항목 이름 · detail 에 없음 → 만들지 않음'})
                continue
            for fam in refs:
                for site in sites:
                    ev = {'file': 'taxonomy.json', 'path': f"problem {P['id']} · {sc['id']} 「{sc['label']}」", 'item': it['id'], 'text': f"{it['name']} ({it.get('detail') or ''}) modality_ref {refs}"}
                    ks = same_keys(fam, None, site, strict_sub=False)
                    if not ks:
                        ks = [up_add(fam, None, site, None, approval='source_only', ev=ev)]; PROBLEM_UPS[fam] += 1
                    for k in ks:
                        up_add(*k[:4], uniq=k[4], ev=ev, approval='source_only', purpose=None)
                        syn(k, it['name'], 'problem_tree')

# 장비 행에 시장가 연결 표시
for row in LEDGER:
    for k, u in UPS.items():
        if row['id'] in u['devices'] and not any(d.get('key') == k for d in row['destinations']):
            row['destinations'].append(dest('unit_procedure', key=k, via='market'))
        if row['id'] in u['source_items'] and u['source_market'] and not any(d.get('key') == k for d in row['destinations']):
            row['destinations'].append(dest('unit_procedure', key=k, via='market'))

# ---------- 패키지 구성 후보를 단위 시술에 대 본다 ----------
for row in LEDGER:
    for dd in row['destinations']:
        if dd['type'] == 'package' and dd.get('components'):
            for c in dd['components']:
                hits = [k for k, u in UPS.items() if u['family'] == c['family'] and u['site'] == c['site']]
                c['unit_procedure_keys'] = hits

# ---------- 단위 시술 approval 합치기 · id · 이름 ----------
RANK = ['approved', 'regate_pending', 'source_only', 'provisional', 'waiting_mfds', 'hold']
SUB_TERM = {('M8', '제모'): '레이저 제모', ('M8', '혈관'): '혈관레이저', ('M8', 'IPL'): 'IPL', ('M8', '피코초(Picosecond)'): '피코레이저',
            ('M9', 'HIFU (초음파)'): 'HIFU 리프팅', ('M9', 'RF (고주파)'): '고주파 리프팅', ('M9', '마이크로웨이브'): '마이크로웨이브 리프팅',
            ('M9', '복합 에너지'): '복합 에너지 리프팅', ('M9', 'SUPERB 초음파'): 'SUPERB 초음파 리프팅',
            ('M4', 'HA (물광)'): '물광주사', ('M4', 'PN/PDRN'): 'PN 스킨부스터', ('M4', '엑소좀/성장인자'): '엑소좀',
            ('M5', 'PRF'): 'PRF', ('M5', 'CGF'): 'CGF', ('M5', 'PRP'): 'PRP',
            ('M15', '케미컬필링'): '필링', ('M15', '딥클렌징'): '딥클렌징', ('M15', '광치료(LED)'): 'LED', ('M15', '탈모(비수술)'): '탈모 관리',
            ('M15', '흉터 전용'): '흉터 치료', ('M15', '여드름 전용'): '여드름 치료', ('M15', '물리박피(결정 분사)'): '크리스탈필',
            ('M15', '이온토포레시스'): '이온토포레시스', ('M15', '주입장비'): '약물 주입', ('M15', '초음파관리'): '초음파 관리',
            ('M16', '지방분해주사'): '지방분해주사'}
TECH_IN_NAME = {'M8', 'M12', 'M13', 'M15', 'M7', 'M6'}
out_ups = []
fam_counter = collections.Counter()
for k, u in UPS.items():
    fam = u['family']; fam_counter[fam] += 1
    u['id'] = f"UP-{fam}-{fam_counter[fam]:03d}"
    ap = sorted(set(u['approvals']), key=RANK.index)
    # 사용자 승인 · 재판정 값이 하나라도 있으면 그 값을 쓴다. 시장가만 근거면 market
    u['approval'] = ap[0] if ap else 'source_only'
    u['provisional'] = bool(u['provisional_questions']) and u['approval'] in ('provisional',)
    if u['approval'] == 'source_only' and u['provisional_questions']: u['provisional'] = True
    del u['approvals']
    term = SUB_TERM.get((fam, u['sub_family'])) or FAM_TERM[fam]
    if fam in TECH_IN_NAME and u['technique'] and fam != 'M6':
        term = u['technique'] if fam in ('M8', 'M12', 'M13') else f"{term}({u['technique']})"
    if fam == 'M6' and u['technique']: term = f"지방이식({u['technique']})"
    if u['site'] == NA or k[4]:
        name = BYID[u['source_items'][0]]['name']
    elif u['site'] is None:
        name = term + ' — 부위 원천 없음'
    else:
        name = f"{u['site']} {term}"
    u['name'] = name
    u['name_status'] = '조합(상담 용어 검수 필요)'
    u['key'] = ' × '.join(str(v) for v in [fam, u['sub_family'] or '-', u['site'] or '부위 없음', u['technique'] or '기법 없음'])
    if u['technique']:
        for e in TECH.get(u['technique'], []):
            if e in u['how_source'] and e != u['technique']:
                syn(k, e, 'technique_expression')
    out_ups.append(u)
# 이름 겹침 → 기법/하위 계열을 괄호로
cnt = collections.Counter(u['name'] for u in out_ups)
for u in out_ups:
    if cnt[u['name']] > 1:
        grp = [v for v in out_ups if v['name'] == u['name']]
        if len({v['technique'] for v in grp}) > 1: tag = u['technique'] or '기법 없음'
        else: tag = u['sub_family'] or '하위 계열 없음'
        u['_tag'] = tag
for u in out_ups:
    if u.get('_tag'):
        u['name'] = f"{u['name']} ({u.pop('_tag')})"
cnt = collections.Counter(u['name'] for u in out_ups)
assert max(cnt.values()) == 1, [n for n, c in cnt.items() if c > 1]
KEY2ID = {k: u['id'] for k, u in UPS.items()}
for row in LEDGER:
    for dd in row['destinations']:
        if dd['type'] == 'unit_procedure':
            k = dd.pop('key'); dd['unit_procedure_id'] = KEY2ID[k]; dd['name'] = UPS[k]['name']
        if dd['type'] == 'package':
            for c in dd.get('components', []):
                c['unit_procedure_ids'] = [KEY2ID[k] for k in c.pop('unit_procedure_keys', [])]
    row.pop('_pkg', None)
for u in out_ups:
    u['source_items'] = list(dict.fromkeys(u['source_items']))
    u['product_item_ids'] = list(dict.fromkeys(u['product_item_ids'] + u['devices']))

# ---------- 계열 목록 ----------
families = []
for mid, m in MODS.items():
    name, st, basis = OFFICIAL.get(mid, (m['name'], 'source_name_provisional', '원천 시술군 이름 — 공식 일반명 미정'))
    syns = list(dict.fromkeys([s.strip() for s in m['name'].split('/')] + [FAM_TERM[mid]] + ([m['name_en']] if m.get('name_en') else [])))
    if mid == 'M1': syns = ['보톡스', '톡신', 'Botulinum Toxin']
    syns = [s for s in syns if s != name]
    subs = [{'label': s['label'], 'source': s['id'], 'count': s['count']} for s in m['subcategories']]
    if mid == 'M7':
        subs += [{'label': r['name'], 'source': r['id'], 'count': 1, 'provisional': 'OQ-309'} for r in LEDGER if r['applied_option'] and r['question'] == 'OQ-309']
    families.append({'id': mid, 'name': name, 'name_status': st, 'name_basis': basis, 'source_name': m['name'],
                     'official_name_candidate_en': m.get('name_en'), 'synonyms': syns, 'consult_term': FAM_TERM[mid],
                     'group': m.get('group'), 'sub_families': subs, 'source_item_count': m['item_count']})
for fid, (name, syns, basis) in EXTRA_FAM.items():
    families.append({'id': fid, 'name': name, 'name_status': 'user_answer_v1', 'name_basis': basis, 'source_name': None,
                     'official_name_candidate_en': None, 'synonyms': syns, 'consult_term': FAM_TERM[fid], 'group': None,
                     'sub_families': [], 'source_item_count': sum(1 for r in LEDGER if r['family'] == fid)})
for f in families:
    f['unit_procedure_count'] = sum(1 for u in out_ups if u['family'] == f['id'])
    f['ledger_item_count'] = sum(1 for r in LEDGER if r['family'] == f['id'])

# ---------- 기법 묶음표 ----------
all_expr = collections.Counter(h for x in ITEMS for h in x['how_source'])
techniques = []
for i, (t, es) in enumerate(TECH.items(), 1):
    used = [u['id'] for u in out_ups if u['technique'] == t]
    techniques.append({'id': f'T{i:02d}', 'name': t, 'source_expressions': es,
                       'source_expression_counts': {e: all_expr.get(e, 0) for e in es},
                       'ledger_items_as_technique': list(dict.fromkeys(TECH_ITEM_NAMES.get(t, []))),
                       'unit_procedure_count': len(used),
                       'provisional': t in ('IPL', 'BBL스킨타이트', '알렉산드라이트', '콜드플라즈마', '코그', '모노', '볼륨실', '롤러형', '스탬프형')})
unmapped_expr = sorted(e for e in all_expr if e not in EXPR2T)
assert not unmapped_expr, unmapped_expr

# ---------- 요약 ----------
dest_counter = collections.Counter()
for r in LEDGER:
    for t in dict.fromkeys(d['type'] for d in r['destinations']): dest_counter[t] += 1
summary = {
    'families': len(families), 'families_from_modality': len(MODS), 'families_from_user_answer': len(EXTRA_FAM),
    'unit_procedures': len(out_ups),
    'unit_procedures_by_family': {f['id']: f['unit_procedure_count'] for f in families},
    'unit_procedures_by_site': dict(collections.Counter(u['site'] or '(부위 원천 없음)' for u in out_ups).most_common()),
    'unit_procedures_by_site_status': dict(collections.Counter(u['site_status'] for u in out_ups)),
    'unit_procedures_by_approval': dict(collections.Counter(u['approval'] for u in out_ups)),
    'unit_procedures_provisional': sum(1 for u in out_ups if u['provisional']),
    'techniques': len(techniques), 'source_technique_expressions': len(all_expr),
    'ledger_items': len(LEDGER), 'ledger_by_destination': dict(dest_counter),
    'ledger_by_approval': dict(collections.Counter(r['approval'] for r in LEDGER)),
    'provisional_items': len(PROV), 'provisional_by_oq': dict(collections.Counter(p['oq'] for p in PROV)),
    'answers_v2_applied': len(A2), 'unit_procedures_created_from_indication': dict(INDICATION_UPS), 'unit_procedures_created_from_problem_tree': dict(PROBLEM_UPS), 'rejected_site_hits': len(REJECTED), 'market_rows_used': len(MARKET), 'market_rows_skipped': len(MARKET_SKIPPED),
}
out = {
    'version': 3, 'generated_at': '2026-10-27', 'source_snapshot': 'phub-stg-2026-10-26',
    'basis': ['DEC-002', 'DEC-003', '_RESUME §2 2026-10-27', 'taxonomy-classify-v2.json',
              'gate-answers/classify-v1 (521) · classify-v2/answers_v2 (17, 2차 우선)',
              'product-master-draft-v3-frozen.json + product-match-build.py 규칙 A', 'market-pricing.json'],
    'rules': {
        'unit_procedure': '무엇을(계열 · 하위 계열) × 어디에(부위) × 어떻게(큰 기법). 같은 키는 하나로 합치고 원장 이름 · 장비 이름 · 시장가 이름 · 기법 원천 표현을 동의어로 둔다',
        'answers': '2차 답 > 1차 답(v2 에 반영) > v2 판정. 2차 「reject」 · 「answer + 직접 입력(확인 필요)」 = 보류(hold)',
        'provisional': '답 없는 question = 각 질문의 첫 선택지를 임시값으로(provisional: true)',
        'approval': 'approved 사용자 승인 / regate_pending 재판정값(1차 답 반영) · 2차 답 없음 / market 시장가 줄만 근거 / provisional 임시값 / waiting_mfds 식약처 대기 / hold 보류',
        'site': 'v2 where(원천 name · detail) + 시장가 이름의 괄호 · 앞말에 적힌 부위만. 트리 밖 이름은 out_of_tree 로 두고 트리에 넣지 않는다. 수액 = 「해당 없음」 + 경로 「허가 용법 확인 대기」',
        'technique': '기법 = v2 단위 시술 how(없으면 비움). 장비 · 시장가에서 만든 단위 시술은 장비 how_source 묶음. 큰 기법 이름은 원천 표현 · 사용자 답 문구에서만',
        'name': '이름 = 「부위 + 상담 용어」 조합(name_status 조합). 수액은 원장 이름 그대로',
        'family_name': 'M1 만 공식 일반명 확정(보툴리눔 톡신). 나머지 16 은 원천 시술군 이름 임시 — 공식 일반명 미정',
    },
    'summary': summary,
    'site_tree': [{'name': n, 'parent': p, 'added_oq206': n in ADDED} for n, p in TREE],
    'site_special': [{'name': NA, 'meaning': '수액 · 성분 주사 — 부위 해당 없음(DEC-003 OQ-306 처리)'}],
    'site_out_of_tree': sorted(OUT_OF_TREE),
    'families': families, 'techniques': techniques, 'unit_procedures': out_ups,
    'ledger_map': LEDGER, 'provisional': PROV,
    'market_rows': [{'name': r[0], 'family': r[1], 'sub_family': r[2], 'sites': r[3], 'technique': r[4], 'item': r[5], 'device': r[6], 'memo': r[7]} for r in MARKET],
    'market_rows_skipped': MARKET_SKIPPED,
    'rejected_combinations': REJECTED,
}
json.dump(out, open(f'{W}/procedure-master-v3.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))

# ======================= md =======================
UPI = {u['id']: u for u in out_ups}
FAMN = {f['id']: f['name'] for f in families}
APL = {'approved': '승인', 'regate_pending': '재판정값(2차 답 없음)', 'source_only': '원천 근거만(승인 전)', 'provisional': '임시값',
       'waiting_mfds': '식약처 대기', 'hold': '보류'}
DTL = {'unit_procedure': '단위 시술', 'product': '제품', 'device': '장비', 'package': '패키지', 'purpose': '목적(고민 엣지 후보)',
       'not_procedure': '시술 아님', 'hold': '보류', 'technique': '기법', 'family': '계열(하위)', 'material': '재료(제품 속성)',
       'device_attribute': '장비 속성'}
def evtext(u):
    out = []
    for e in u['evidence']:
        if e['file'] == 'market-pricing.json': out.append(f"시장가 「{e['item']}」")
        elif 'indications' in e['path']: out.append(f"적응증 {e['item']}")
        elif e['path'].startswith('problem'): out.append(f"고민 {e['path'].split(' · ')[1].split(' ')[0]} {e['item']}")
        else: out.append(f"taxonomy {e['item']}")
    return ' · '.join(out[:6]) + (f" 외 {len(out)-6}" if len(out) > 6 else '')
def esc(s): return str(s if s is not None else '').replace('|', '\\|').replace('\n', ' ')
def dtext(dd):
    t = dd['type']
    if t == 'unit_procedure': return f"단위 시술 {dd['unit_procedure_id']} 「{dd['name']}」" + (' (시장가)' if dd.get('via') else '')
    if t in ('product', 'device'):
        st = dd.get('match_status_rule_a') or dd.get('match_status') or '-'
        return f"{DTL[t]} `{dd['product_master_id']}` ({st})" + (f" 「{dd['product_name']}」" if dd.get('product_name') else '')
    if t == 'package':
        cs = dd.get('components') or []
        if not cs: return '패키지 — 구성 없음(OQ-204)'
        return '패키지 — 구성 후보 ' + ', '.join(f"{c['site']}→{'/'.join(c['unit_procedure_ids']) or '단위 시술 없음'}" for c in cs)
    if t == 'purpose': return '목적 ' + '·'.join(dd['purposes'])
    if t == 'technique': return f"기법 「{dd['technique']}」"
    if t == 'family': return f"계열 {dd['family']} 하위 「{dd['sub_family']}」"
    if t == 'material': return f"재료 「{dd['material']}」"
    if t == 'device_attribute': return f"장비 속성(of `{dd['of_device']}`)"
    if t == 'hold': return '보류 — ' + esc(dd.get('reason'))
    return DTL.get(t, t) + (' — ' + dd['reason'] if dd.get('reason') else '')
S = summary
L = []
L.append('---\ntype: research\nproduct: procedure-hub\nfeature: phub-recommend\ncreated_at: 2026-10-27\n'
         'basis: DEC-002 · DEC-003 · _RESUME §2 2026-10-27 · taxonomy-classify-v2 · gate-answers(1차 521 · 2차 17)\n'
         'source_snapshot: phub-stg-2026-10-26\n---\n')
L.append('# 시술 원장 확정안 v3 — 분류표 v3(단위 시술 목록)\n')
L.append('> 정본은 `procedure-master-v3.json`(빌드 `procedure-master-build.py`, 결정론 · 외부 호출 없음)이다. 이 문서는 같은 데이터를 표로 옮긴 것이다.')
L.append('> 판정 우선순위: **2차 답 > 1차 답(v2 에 반영된 값) > v2 판정**. 답이 없는 question 은 첫 선택지를 임시값으로 넣고 `provisional: true` 로 표시했다.')
L.append('> 제품 · 장비는 `product-master-draft-v3-frozen.json` 의 같은 id 행이고, 괄호 안 상태는 `product-match-build.py` 규칙 A 를 적용한 값이다(4차 원본은 읽지 않았다).\n')
L.append('## 0. 한눈에\n')
L.append('| 항목 | 수 |\n|---|---|')
L.append(f"| 계열(무엇을) | **{S['families']}** = 시술군 {S['families_from_modality']} + 사용자 1차 답 ③으로 생긴 계열 {S['families_from_user_answer']} |")
L.append(f"| 단위 시술 | **{S['unit_procedures']}** |")
L.append(f"| 큰 기법 | {S['techniques']} (원천 기법 표현 {S['source_technique_expressions']}종을 묶음) |")
L.append(f"| 원장 항목 | {S['ledger_items']} — 전부 행선지 있음 |")
L.append(f"| 임시값(답 없는 question) | {S['provisional_items']} 항목 · 임시값이 걸린 단위 시술 {S['unit_procedures_provisional']} |")
L.append(f"| 2차 답 적용 | {S['answers_v2_applied']} |")
L.append(f"| 적응증 · 고민 트리로 새로 세운 단위 시술(SPEC-004 R-1) | 적응증 {sum(S['unit_procedures_created_from_indication'].values())} · 고민 트리 {sum(S['unit_procedures_created_from_problem_tree'].values())} — 계열별 §0 표 · 근거 없는 조합(만들지 않음) {S['rejected_site_hits']} 건은 §6-1 |")
L.append(f"| 시장가 줄 | 단위 시술 근거로 씀 {S['market_rows_used']} · 안 씀 {S['market_rows_skipped']}(부위가 이름에 없음 — §7) |\n")
L.append('### 단위 시술 — 판정 상태별\n')
L.append('| 상태 | 뜻 | 수 |\n|---|---|---|')
for k in RANK:
    if k in S['unit_procedures_by_approval']:
        L.append(f"| `{k}` | {APL[k]} | {S['unit_procedures_by_approval'][k]} |")
L.append('\n상태는 그 단위 시술을 받치는 근거 가운데 가장 확정된 것이다(승인 > 재판정값 > 시장가 > 임시값 > 식약처 대기 > 보류).\n')
L.append('### 단위 시술 — 계열별\n')
L.append('| 계열 id | 계열 이름 | 이름 상태 | 단위 시술 | 원장 항목 |\n|---|---|---|---|---|')
for f in families:
    L.append(f"| {f['id']} | {f['name']} | {f['name_status']} | {f['unit_procedure_count']} | {f['ledger_item_count']} |")
L.append('\n### 단위 시술 — 부위별\n')
L.append('| 부위 | 상태 | 단위 시술 |\n|---|---|---|')
for s_, n in S['unit_procedures_by_site'].items():
    st = site_status(None if s_ == '(부위 원천 없음)' else s_)
    L.append(f"| {s_} | {st} | {n} |")
L.append('\n- `tree` DEC-002 부위 트리 · `added` OQ-206 추가분(콧등 · 손 · 발 · 다리 · 비키니 · 힙) · `not_applicable` 수액(부위 해당 없음) · `out_of_tree` 트리 밖(사용자 결정 대기) · `missing` 원천에 부위 없음')
L.append(f"- 부위 원천 없음 {S['unit_procedures_by_site_status'].get('missing', 0)} 은 v2 단위 시술(사용자 승인 포함)이 부위를 비워 둔 것이다. 부위를 만들어 넣지 않았다\n")
L.append('### 임시값 목록 (답 없는 question — 첫 선택지 적용)\n')
L.append('| OQ | 항목 | 적용한 값(첫 선택지) | 다른 선택지 |\n|---|---|---|---|')
for p_ in sorted(PROV, key=lambda p: (p['oq'], p['id'])):
    L.append(f"| {p_['oq']} | `{p_['id']}` {esc(p_['name'])} | {esc(p_['applied'])} | {esc(' / '.join(p_['options'][1:]))} |")
L.append(f"\n- question 63 가운데 4건은 2차 답(직접 입력 「확인 필요」)이 있어 임시값 대신 **보류**로 두었다: HArmonyCa · 꿀광주사 · 아기주사 · 벨벳주사. 그래서 임시값은 {len(PROV)} 이다")
L.append('- M1-3-8 의 OQ-316(잇몸미소 = 잇몸?)은 2차 답이 「승인」이라 임시값이 아니라 확정(잇몸)으로 넣었다\n')

L.append('## 1. 계열(무엇을)\n')
L.append('| id | 이름 | 이름 상태 · 근거 | 동의어 | 하위 계열(원천 하위 분류) |\n|---|---|---|---|---|')
for f in families:
    subs = ' · '.join(s['label'] + (f"(임시 {s['provisional']})" if s.get('provisional') else '') for s in f['sub_families']) or '-'
    L.append(f"| {f['id']} | **{f['name']}** | {f['name_status']} — {esc(f['name_basis'])} | {esc(' · '.join(f['synonyms']))} | {esc(subs)} |")
L.append('\n- **M1 만 공식 일반명이 확정**(보툴리눔 톡신)이다. 나머지 16 은 원천 시술군 이름을 임시로 쓴다(`source_name_provisional`). 공식 일반명 후보로 원천 영문명(`official_name_candidate_en`)을 함께 둔다 — 확정은 사용자')
L.append('- X1~X6 은 사용자 1차 답 ③(「무엇을 틀림: 수액치료 아니라 …」)의 문구로 세운 계열이다. 「국소 / 피하」 는 계열이 아니라 기법(국소 주사 · 피하 주사)으로 뗐다')
L.append('- 「LDM초음파관리」(1차 답 ③ 「수액치료 아니라 초음파 장비」)는 새 계열을 세우지 않고 같은 장비 LDM(M15-4-1)이 있는 M15 · 초음파관리에 댔다\n')

L.append('## 2. 기법(어떻게) — 묶음표\n')
L.append('큰 기법 이름은 원천 표현 또는 사용자 답 문구에서만 골랐다. 원천 표현은 그 기법의 동의어다. 「임시」 = OQ-310/311 첫 선택지(기법 축)로 기법이 된 것.\n')
L.append('| id | 큰 기법 | 원천 표현(원장 등장 수) | 기법으로 들어온 원장 항목 | 단위 시술 |\n|---|---|---|---|---|')
for t in techniques:
    ex = ' · '.join(f"{e}({c})" for e, c in t['source_expression_counts'].items())
    L.append(f"| {t['id']} | {t['name']}{' (임시)' if t['provisional'] else ''} | {esc(ex)} | {esc(' · '.join(t['ledger_items_as_technique']))} | {t['unit_procedure_count']} |")
L.append('\n- 프락셔널은 원천에 「박피성 / 비박피성(비박리성)」이 적힌 경우 둘로 나눴다(안전이 다르다 — DEC-002 D-05 ②). 적히지 않은 것은 「프락셔널」')
L.append('- 필링 깊이(중간~심층 · 심부필링)는 v2 단위 시술이 기법을 비워 두어 기법으로 쓰지 않고 `how_source` 속성으로만 남겼다(§8)\n')

L.append('## 3. 단위 시술\n')
L.append('이름은 「부위 + 상담 용어」 조합이다(`name_status: 조합` — 상담 용어 검수 필요). 수액은 원장 이름을 그대로 쓴다. 이름이 겹치면 괄호에 기법이나 하위 계열을 붙였다.\n')
for f in families:
    us = [u for u in out_ups if u['family'] == f['id']]
    if not us: continue
    L.append(f"### {f['id']} {f['name']} — {len(us)}\n")
    L.append('| id | 이름 | 하위 계열 | 부위 | 기법 | 상태 | 동의어(원장 · 장비 · 시장가 · 고민 · 표현) | 원천 항목 id | product_item_ids | 근거(파일 · 항목) |\n|---|---|---|---|---|---|---|---|---|---|')
    for u in us:
        sy = ' · '.join(f"{y['text']}" + ('[장비]' if y['type'] in ('device', 'device_accessory') else '[미연결 장비명]' if y['type'] == 'device_name_unlinked' else '') for y in u['synonyms'])
        stt = APL[u['approval']] + (' · 임시 ' + '/'.join(u['provisional_questions']) if u['provisional_questions'] else '')
        L.append(f"| {u['id']} | **{esc(u['name'])}** | {esc(u['sub_family'] or '-')} | {esc(u['site'] or '(원천 없음)')}{' ⚠트리 밖' if u['site_status']=='out_of_tree' else ''} | "
                 f"{esc(u['technique'] or '-')} | {stt} | {esc(sy)} | {esc(', '.join(u['source_items']))} | {esc(', '.join(u['product_item_ids']))} | {esc(evtext(u))} |")
    L.append('')
L.append('## 4. 원장 항목 521 → 어디로 갔나\n')
L.append('| 행선지 | 항목 수 |\n|---|---|')
for t, n in sorted(S['ledger_by_destination'].items(), key=lambda x: -x[1]):
    L.append(f"| {DTL.get(t, t)} | {n} |")
L.append('\n한 항목이 여러 행선지를 가질 수 있다(예: 목적 이름 「주름」 = 목적 + 단위 시술 다섯). 판정 상태별 항목 수: ' +
         ' · '.join(f"{APL[k]} {v}" for k, v in S['ledger_by_approval'].items()) + '\n')
for mid in list(MODS):
    rows = [r for r in LEDGER if r['modality'] == mid]
    L.append(f"### {mid} {MODS[mid]['name']} — {len(rows)}\n")
    L.append('| id | 이름 | v2 kind · status | 답 1차/2차 | 상태 | 어디로 |\n|---|---|---|---|---|---|')
    for r in rows:
        ans = f"{r['answer_v1'] or '-'} / {r['answer_v2'] or '-'}"
        stt = APL[r['approval']] + (f" ({r['question']} 임시)" if r['provisional'] else '')
        L.append(f"| `{r['id']}` | {esc(r['name'])} | {r['kind_v2']} · {r['status_v2']} | {ans} | {stt} | {esc('<br>'.join(dtext(d) for d in r['destinations']))} |")
    L.append('')
L.append('## 5. 보류(hold) — 다음 단계로 가지 않는 것\n')
L.append('| id | 이름 | 사유 |\n|---|---|---|')
for r in LEDGER:
    for dd in r['destinations']:
        if dd['type'] == 'hold':
            L.append(f"| `{r['id']}` | {esc(r['name'])} | {esc(dd.get('reason'))} |")
L.append('\n## 6. 트리 밖 부위 · 미연결 장비명\n')
L.append('- 트리 밖 부위(트리에 넣지 않음 — `_RESUME` §1 미결 「옆구리 · 등 · 브라라인 · 엉덩이」): ' +
         ', '.join(f"{u['id']} 「{u['name']}」" for u in out_ups if u['site_status'] == 'out_of_tree') + ' · 원천에만 있는 표현: ' + ' · '.join(sorted(OUT_OF_TREE)))
L.append('- 시장가에 장비 이름이 있지만 원장 항목 이름과 글자가 달라 자동 연결하지 않은 것: 「시크릿」(원장 시크릿RF) · 「모피어스8」(원장 모르페우스8) · 「이모드」(원장에 없음) · 「제네시스 (전체얼굴)」(원장 제네시스토닝 — 단위 시술로도 안 씀)\n')
L.append('### 6-1. 근거 없어 만들지 않은 조합(SPEC-004 R-1)\n')
L.append('부위 이름이 글자로는 보였지만 다른 낱말의 일부(「까치발」의 발 · 「볼륨」의 볼 · 「손상」의 손 …)였거나, 고민 트리 하위 라벨에만 있고 항목 이름 · detail 에는 없는 부위다. 단위 시술을 만들지 않았다. 「필러 × 턱선」은 적응증 근거(더채움 「턱선 정의」 · 아띠에르 · 아말리안 · 하모니카)가 있어 세웠다(UP-M2 「턱선 필러」).\n')
L.append('| 원천 | 항목 | 계열 | 낱말 | 앞뒤 | 사유 |\n|---|---|---|---|---|---|')
for r in REJECTED:
    L.append(f"| {r['source']} | `{r['item']}` {esc(r.get('name'))} | {r.get('family') or '-'} | {r['word']} | {esc(r.get('context', r.get('label', '')))} | {r['reason']} |")
L.append('')
L.append('## 7. 시장가에서 쓰지 않은 줄\n')
L.append('이름에 부위가 없거나(제품 · 규격만, 목적만, 콤보) 원장과 이어지지 않는 줄이다. 규격 · 가격은 제품 원장 `specs` 와 그래프 빌드가 맡는다.\n')
L.append(', '.join(MARKET_SKIPPED) + '\n')
L.append('## 8. 정하지 않은 것(사용자)\n')
L.append('1. **계열 공식 일반명 16개**(M2~M17) — 지금은 원천 이름 임시. 후보는 원천 영문명')
L.append('2. **임시값 59** — §0 목록. 답이 오면 첫 선택지 대신 그 값으로 다시 빌드한다(`procedure-master-build.py`)')
L.append('3. **M16 「지방분해주사(마케팅명)」 10 ↔ X1 지방분해주사** — 1차 답 ③ 은 DCA 제품을 「수액치료 아님」으로 옮겼는데, 마케팅명 주사 10 은 v2 그대로 M16 아래에 있다(성분 미상 — OQ-312). 합칠지')
L.append('4. **원천 근거만(승인 전) 단위 시술** — 시장가 · 적응증 · 고민 트리로 세운 것은 사용자 승인을 거치지 않았다(`source_only`). 적응증 문장은 taxonomy `extracted.indications`(원천 추출문)라 부위가 넓게 적힌 장비가 많다(예: 울쎄라피프라임 팔뚝/허벅지) — 그래프에 넣기 전 게이트 여부')
L.append('5. **부위 원천 없음 단위 시술 25** — v2 가 부위를 비워 둔 기법형 단위 시술(토닝 · 프락셔널 · IPL · 실 구조 · MTS 도구 · 지방이식 기법 등). 부위를 붙일 원천이 생기기 전에는 「시술 ↔ 부위 가능 엣지」를 만들 수 없다')
L.append('6. **수액 경로** — 「해당 없음」 + 경로 「허가 용법 확인 대기」(DEC-003 OQ-308 처리). 원천에 「IV」 · 「정맥주사」가 있는 2건(백옥 · 나드)도 같은 대기')
L.append('7. **필링 깊이**(중간~심층 · 심부필링)를 기법으로 가를지 — 지금은 「얼굴 전체 필링」 하나에 합쳐져 있다')
L.append('8. **엑소좀 재료 계열** — OQ-314 임시값 「재료 계열(엑소좀) × 두피」를 M4 엑소좀/성장인자에 댔다. M17 엑소좀과 합칠지')
L.append('9. **단위 시술 이름(상담 용어)** — 전부 조합 이름이다. 검수 필요')
open(f'{W}/procedure-master-v3.md', 'w').write('\n'.join(L) + '\n')
print('md lines', len(L))
