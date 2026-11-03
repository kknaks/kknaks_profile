#!/usr/bin/env python3
"""실버 연결 구조 페이지 데이터 — 시맨틱 정본(semantic.json) 기준으로 실버 1~8단계를 노드 · 엣지로 펼친다(읽기 전용 · 결정론).

python3 silver-graph-build.py  →  silver-graph.html 의 <script id="data"> 를 다시 채운다.
노드 종류 · 엣지 종류 · 표시 · 용어 · 사전 · 정본 id 는 semantic.json 에서 읽는다(여기서 목록을 짓지 않음).
실버 칸 → 정본 엣지 종류 대응은 semantic.json edge_kinds[].page(그 페이지의 옛 엣지 키) 를 따른다.
끝점 묶음은 노드가 아니다(U3 · B3) — 후보마다 선을 긋고 「후보 여럿」 표시 · 「모든 시술」 · 해석 안 됨 끝은 상대 노드의 「대상 노드 없는 엣지」로.
실버 · 시맨틱 json 은 읽기만 한다(고치지 않음).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, 'silver-graph.html')
J = lambda f: json.load(open(os.path.join(HERE, f), encoding='utf-8'))

S1, S2, S3, S4 = J('step1-products.json'), J('step2-families.json'), J('step3-sites.json'), J('step4-techniques.json')
S5, S6, S7, S8 = J('step5-units.json'), J('step6-packages.json'), J('step7-concerns.json'), J('step8-relations.json')
SEM = J('semantic.json')

# ───────── 정본에서 읽는 것
GLOSS = {g['term']: g['definition'] for g in SEM['glossary']}
SK = SEM['node_kinds']                       # 13
KIND_IDX = {k['kind']: i for i, k in enumerate(SK)}
SE = SEM['edge_kinds']                       # 21
SE_IDX = {e['kind']: i for i, e in enumerate(SE)}
# 표시 12 — 한 글자 코드(페이지 안에서만 · 정본 이름은 flag)
FLAG_CODE = {'conflict': 'c', 'conditional': 's', 'candidates': 'm', 'weak': 'w', 'question': 'q', 'not_recommended': 'x',
             'gap': 'g', 'default_value': 'd', 'unresolved': 'u', 'not_procedure': 'n', 'by_sub_condition': 'b', 'license_unconfirmed': 'l'}
SFL = SEM['reading']['flags']
if sorted(f['flag'] for f in SFL) != sorted(FLAG_CODE):
    sys.exit(f"semantic.json 표시가 페이지 코드표와 다름: {[f['flag'] for f in SFL]}")
FLAGS = {FLAG_CODE[f['flag']]: {'flag': f['flag'], 'ko': f['ko'], 'read': f['read'], 'n': f['count'], 'gloss': GLOSS.get(f['ko'].split('(')[0].strip(), '')} for f in SFL}
GATE = SEM['reading']['gate_status']
G_AUTO, G_DEC = '자동(규칙)', '결정'
# 정본 id — (종류, 실버 id) → 정본 id
CANON = {(m['kind'], m['silver_id']): m['canonical'] for m in SEM['ids']['map']}
# 페이지 옛 키 → 정본 엣지 종류(semantic edge_kinds[].page)
PAGE2SE = {}
for e in SE:
    for p in e['page'] + [e['kind']]:   # 페이지 키가 없는 새 종류(line_item)는 정본 이름 그대로
        PAGE2SE[p] = e['kind']
OLD2KIND = {'prod': 'product', 'fam': 'family', 'site': 'site', 'tech': 'technique', 'unit': 'unit_procedure', 'pkg': 'package', 'con': 'concern',
            'pur': 'purpose', 'combo': 'combo', 'cond': 'check_condition', 'cx': 'complication', 'stmt': 'evidence_statement', 'ev': 'evidence_source'}
if sorted(OLD2KIND.values()) != sorted(KIND_IDX):
    sys.exit('semantic.json 노드 종류가 페이지 대응표와 다름')
GRADE3 = SEM['reading']['labels']['grade3']

nodes = {}      # nid -> dict
order = []      # 넣은 순서(결정론)


def add_node(kind, raw, name, aliases=(), info=(), detail=(), flags='', gate=G_AUTO):
    nid = f'{kind}:{raw}'
    if nid in nodes:
        n = nodes[nid]
        n['flags'] = ''.join(sorted(set(n['flags']) | set(flags)))
        for a in aliases:
            if a and a not in n['aliases']:
                n['aliases'].append(a)
        return nid
    nodes[nid] = {'kind': kind, 'raw': raw, 'name': name or raw, 'aliases': [a for a in dict.fromkeys(a for a in aliases if a and a != name)],
                  'info': [x for x in info if x], 'detail': [x for x in detail if x], 'flags': ''.join(sorted(set(flags))), 'gate': gate}
    order.append(nid)
    return nid


def flag(nid, f):
    if nid in nodes:
        nodes[nid]['flags'] = ''.join(sorted(set(nodes[nid]['flags']) | set(f)))


def gate_of(rec):
    """B12 — gate_status 칸이 있으면 그대로 · decided_by 가 있으면 「결정」 · 나머지 「자동(규칙)」."""
    if rec.get('gate_status'):
        return rec['gate_status']
    if rec.get('decided_by'):
        return G_DEC
    return G_AUTO


edges = {}      # (page키, a, b) -> dict
loose = []      # 대상 노드 없는 엣지(끝 「모든 시술」 · 해석 안 됨 · 행선지 없는 원장 항목)


def add_edge(pk, a, b, label='', detail=(), flags='', gate=G_AUTO):
    if pk not in PAGE2SE:
        sys.exit(f'정본 엣지 종류 없는 페이지 키: {pk}')
    if a not in nodes or b not in nodes:
        return False
    k = (pk, a, b)
    e = edges.get(k)
    if e is None:
        e = edges[k] = {'label': [], 'detail': [], 'flags': set(), 'gate': set()}
    if label and label not in e['label']:
        e['label'].append(label)
    for d in detail:
        if d and d not in e['detail']:
            e['detail'].append(d)
    e['flags'] |= set(flags)
    e['gate'].add(gate)
    return True


def add_loose(pk, nid, direction, other, label='', detail=(), flags='', gate=G_AUTO):
    if nid in nodes:
        loose.append({'pk': pk, 'n': nid, 'dir': direction, 'other': other, 'label': label, 'detail': [d for d in detail if d], 'flags': ''.join(sorted(set(flags))), 'gate': gate})


def short(s, n=160):
    s = re.sub(r'\s+', ' ', str(s or '')).strip()
    return s if len(s) <= n else s[:n - 1] + '…'


# ───────── 1단계 제품 · 2단계 계열
pf = {r['ledger_id']: r for r in S2['product_family']}
for it in S1['items']:
    if not it.get('active'):
        continue
    nm = it['2_names']
    lic = it.get('4_license') or {}
    f = ''
    if lic.get('recommendable') is False:
        f += 'x'
    if lic.get('status') == '허가번호 미확인':
        f += 'l'
    if it.get('open'):
        f += 'q'
    info = [f"허가 {lic.get('status')}" if lic.get('status') else '', f"{(it.get('1_identity') or {}).get('kind') or ''}",
            '추천 제외' if lic.get('recommendable') is False else '추천 가능']
    detail = [f"허가 이유: {short(lic.get('reason'))}" if lic.get('reason') else '']
    detail += [f"사람 확인 메모: {short(it['gate'])}" if it.get('gate') else '']
    detail += [f"열린 것: {short(json.dumps(o, ensure_ascii=False))}" for o in (it.get('open') or [])]
    add_node('prod', it['ledger_id'], nm.get('display_name'), [s['name'] for s in nm.get('search_names') or []], info, detail, f, gate_of(it))

for fa in S2['families']:
    add_node('fam', fa['id'], fa['name'], fa.get('synonyms') or [], [fa.get('literature_name') or '', f"하위 계열: {' · '.join(fa['sub_families'])}" if fa.get('sub_families') else ''],
             [f"정의: {short(fa.get('definition'), 400)}", f"이름 상태: {fa.get('name_status')}"], '', gate_of(fa))

for r in S2['product_family']:
    a = f"prod:{r['ledger_id']}"
    f = ''
    if r.get('evidence_level') in ('약', '중'):
        f += 'w'
    if r.get('conflict'):
        f += 'c'
    if r.get('pending_director') or r.get('confirm_question'):
        f += 'q'
    det = [f"판정: {r.get('verdict')}", f"근거: {short(r.get('basis'), 300)}", f"하위 계열: {r['sub_family']}" if r.get('sub_family') else '',
           f"충돌: {short(json.dumps(r['conflict'], ensure_ascii=False))}" if r.get('conflict') else '',
           f"확인 질문: {short(r['confirm_question'])}" if r.get('confirm_question') else '']
    if r.get('family'):
        add_edge('prod_fam', a, f"fam:{r['family']}", '주' + (f" · {r['sub_family']}" if r.get('sub_family') else ''), det, f, gate_of(r))
    for af in r.get('also_families') or []:
        add_edge('prod_fam_also', a, f"fam:{af}", '보조', det, f, gate_of(r))
    flag(a, f)
for r in S2.get('pending_director') or []:
    flag(f"prod:{r['ledger_id']}", 'q')

# 1단계 라인 → 품목(정본 line_item · ledger_id 있는 품목만)
for ln, v in S1['lines'].items():
    for it in v.get('items') or []:
        if it.get('ledger_id') and v.get('line_row'):
            add_edge('line_item', f"prod:{v['line_row']}", f"prod:{it['ledger_id']}", f"라인 「{ln}」",
                     [f"결정 {v.get('decision')}" if v.get('decision') else '', f"허가번호 {it.get('license_no')}" if it.get('license_no') else ''],
                     '', G_DEC if v.get('decision') else G_AUTO)

# ───────── 3단계 부위
site_by_name = {}
for n in S3['nodes']:
    an = n.get('anatomical_name') or {}
    f = 'w' if (n.get('weak_strings') or any(s.get('weak') for s in n.get('synonyms') or []) or an.get('level') == '약') else ''
    add_node('site', n['id'], n['name'], [s['text'] for s in n.get('synonyms') or []],
             [f"해부학 이름 {an.get('ko')} · {an.get('en')} (근거 {an.get('level')})" if an else '', f"위험지대 {n['danger_zone']['zone']}" if n.get('danger_zone') else ''],
             [f"위험지대 대응: {n['danger_zone'].get('relation')} — {short(n['danger_zone'].get('basis'))}" if n.get('danger_zone') else '', n.get('note') or ''], f, gate_of(n))
    site_by_name[n['name']] = f"site:{n['id']}"
for n in S3['nodes']:
    if n.get('parent') in site_by_name:
        add_edge('site_parent', f"site:{n['id']}", site_by_name[n['parent']], '상위 부위')
for q in S3.get('doctor_questions') or []:
    flag(f"site:{q['id']}", 'q')

# ───────── 4단계 기법
for n in S4['nodes']:
    add_node('tech', n['id'], n['name'], [n.get('medical_name')] + [s['text'] for s in n.get('source_expressions') or [] if len(s.get('text', '')) < 30],
             [f"{n.get('level')} · {n.get('medical_name') or ''}"], [f"근거: {short(n.get('basis'), 300)}"], '', gate_of(n))
for n in S4['nodes']:
    if n.get('parent'):
        add_edge('tech_parent', f"tech:{n['id']}", f"tech:{n['parent']}", '상위 기법')
for r in S4['family_defaults']:
    det = [f"기본 층: {r.get('default_layer')}" if r.get('default_layer') else '', f"근거: {short(r.get('basis'), 300)}"]
    if r.get('default'):
        add_edge('fam_tech', f"fam:{r['family']}", f"tech:{r['default']}", '기본', det, 'd', gate_of(r))
    for t in r.get('also') or []:
        add_edge('fam_tech_also', f"fam:{r['family']}", f"tech:{t}", '함께', det, '', gate_of(r))

# ───────── 5단계 단위 시술
market_by_unit = {}
for m in S5['market']:
    for u in m.get('units') or []:
        market_by_unit.setdefault(u, []).append(f"시장가 「{m['name']}」 {m.get('price') or ''} {m.get('sessions') or ''}".strip())
pih_by_unit = {}
for p in S5['pih']:
    for u in p.get('units') or []:
        pih_by_unit.setdefault(u, []).append(f"PIH {p.get('pih_risk')} {p.get('pih_rate') or ''} — {p.get('name')}")
gap_units = set(S5.get('pih_gap_units') or [])
for u in S5['units']:
    k = u['key']
    f = ''
    if u.get('evidence_level') in ('약', '중'):
        f += 'w'
    if u['id'] in gap_units:
        f += 'g'
    if (u.get('route_status') and '미확인' in u['route_status']) or '기본값' in str(u.get('site_basis') or ''):
        f += 'd'
    if u.get('candidate_of') or any(s.get('ambiguous') for s in u.get('synonyms') or []):
        f += 'm'
    info = [f"{k.get('family')} × {k.get('site')} × {k.get('technique')}" + (f" · 하위 {k['sub_family']}" if k.get('sub_family') else '') + (f" · 성분 {k['ingredient']}" if k.get('ingredient') else ''),
            f"부위 근거: {u['site_basis']}" if u.get('site_basis') else '', f"경로: {u['route_status']}" if u.get('route_status') else '', 'PIH 정보 없음(gap)' if u['id'] in gap_units else '']
    detail = [f"결정: {short(u['decided_by'], 200)}" if u.get('decided_by') else '']
    detail += [f"메모: {short(x, 300)}" for x in u.get('notes') or []] + market_by_unit.get(u['id'], []) + pih_by_unit.get(u['id'], [])
    detail += [f"용도(원장): {' · '.join(u['purposes'])}" if u.get('purposes') else '']
    detail += [f"{a}: {short(json.dumps(v, ensure_ascii=False))}" for a, v in (u.get('step4_attrs') or {}).items()]
    add_node('unit', u['id'], u['name'], [s['text'] for s in u.get('synonyms') or []] + (u.get('candidate_of') or []), info, detail, f, gate_of(u))
for u in S5['units']:
    a, k = f"unit:{u['id']}", u['key']
    g = gate_of(u)
    add_edge('unit_fam', a, f"fam:{k['family']}", ' · '.join(x for x in [k.get('sub_family') and f"하위 {k['sub_family']}", k.get('ingredient') and f"성분 {k['ingredient']}"] if x), [], '', g)
    if k.get('site') in site_by_name:
        add_edge('unit_site', a, site_by_name[k['site']], u.get('site_basis') or '', [], 'd' if '기본값' in str(u.get('site_basis') or '') else '', g)
    if k.get('technique'):
        add_edge('unit_tech', a, f"tech:{k['technique']}", '', [], '', g)
    for p in u.get('uses_product') or []:
        add_edge('unit_prod', a, f"prod:{p['product']}", '', [f"근거: {short(p.get('basis'))}"], '' if p.get('recommendable', True) else 'x', g)
for q in S5.get('origin_questions') or []:
    for nid in (f"unit:{q['id']}", f"prod:{q['id']}"):
        flag(nid, 'q')
for q in S5.get('staff_questions') or []:
    flag(f"unit:{q['id']}", 'q')

# ───────── 6단계 패키지
for p in S6['packages']:
    f = '' if p.get('recommendable', True) else 'x'
    add_node('pkg', p['id'], p['name'], [s['text'] for s in p.get('synonyms') or []],
             [f"{p.get('kind')} · {p.get('shape') or ''}", '추천 제외' if not p.get('recommendable', True) else ''],
             [f"원문: {p.get('detail_raw')}" if p.get('detail_raw') else '', f"같은 날: {p.get('same_day_raw')}"] + [f"메모: {short(x, 300)}" for x in p.get('notes') or []], f, gate_of(p))
for c in S6['contains']:
    f = 'w' if c.get('evidence_level') in ('약', '중') else ''
    f += 'q' if c.get('origin_question') else ''
    add_edge('pkg_unit', f"pkg:{c['package']}", f"unit:{c['unit']}", f"확정 · {c['order']}번" + (f" · {c['sessions']}회" if c.get('sessions') else ''),
             [f"원문: {c.get('text')} — {short(c.get('basis'))}"], f, gate_of(c))
for s in S6['slots']:
    for u in s.get('candidates') or []:
        add_edge('pkg_slot', f"pkg:{s['package']}", f"unit:{u}", f"슬롯 후보 · {s['order']}번",
                 [f"원문: {s.get('text')} — {short(s.get('basis'))}", f"원천 질문 {s['origin_question']}" if s.get('origin_question') else ''], 'm' + ('q' if s.get('origin_question') else ''), gate_of(s))
    flag(f"pkg:{s['package']}", 'q' if s.get('origin_question') else '')
for q in S6.get('origin_questions') or []:
    for p in q.get('packages') or []:
        flag(f"pkg:{p}", 'q')

# ───────── 7단계 고민 · 목적 · 추천 조합
CC = S7['concerns']
con_ids = set()
for c in CC['categories']:
    if c.get('node'):
        add_node('con', c['id'], c['name'], [c.get('en'), c.get('source_name')], [c.get('verdict')], [short(c.get('basis'), 300)], '', gate_of(c))
        con_ids.add(c['id'])
for c in CC['subcategories']:
    if c.get('node'):
        add_node('con', c['id'], c.get('concern') or c['source_label'], [c['source_label']], [f"{c.get('kind')}" + (f" · 부위 {' · '.join(c['sites'])}" if c.get('sites') else '')], [c.get('note')], '', gate_of(c))
        con_ids.add(c['id'])
for c in CC['items']:
    if c.get('kind') == '고민':
        add_node('con', c['id'], c['name'], [c.get('detail')], [f"고민 항목 · {c.get('concern') or ''}" + (f" · 부위 {' · '.join(c['sites'])}" if c.get('sites') else '')], [], '', gate_of(c))
        con_ids.add(c['id'])
for c in CC['extra_items']:
    add_node('con', c['id'], c['name'], [], [c.get('kind')], [short(c.get('basis'), 400), f"결정: {c.get('decided_by')}"], '', gate_of(c))
    con_ids.add(c['id'])
for c in CC['subcategories']:
    if c.get('node') and c.get('parent') in con_ids:
        add_edge('con_parent(상위)', f"con:{c['id']}", f"con:{c['parent']}", '상위 고민')
for c in CC['items']:
    if c.get('kind') == '고민':
        par = c['subcategory'] if c['subcategory'] in con_ids else c['category']
        add_edge('con_parent(상위)', f"con:{c['id']}", f"con:{par}", '상위 고민')
for c in CC['extra_items']:
    if c.get('parent') in con_ids:
        add_edge('con_parent(상위)', f"con:{c['id']}", f"con:{c['parent']}", '상위 고민')
    for r in c.get('related') or []:
        add_edge('con_parent(관련)', f"con:{c['id']}", f"con:{r}", '관련(상위 없음)', [], '', gate_of(c))
for c in CC['subcategories'] + CC['items'] + CC['extra_items']:
    if f"con:{c['id']}" in nodes:
        for s in c.get('sites') or []:
            if s in site_by_name:
                add_edge('con_site', f"con:{c['id']}", site_by_name[s])

pur_map = {}
for p in S7['purposes']:
    if p.get('node'):
        pur_map[p['name']] = add_node('pur', p['name'], p['name'], [a['text'] for a in p.get('aliases') or []], [p.get('kind')], [f"나온 곳: {' · '.join(p.get('from') or [])}"], '', gate_of(p))
    elif p.get('same_as_concern') and f"con:{p['same_as_concern']}" in nodes:
        pur_map[p['name']] = f"con:{p['same_as_concern']}"
        nodes[pur_map[p['name']]]['aliases'].append(p['name'])
# 원천 표현 대응(correspondence) = 고민 · 목적의 검색 이름(gate_status 는 상세에)
for r in S7['correspondence']:
    for t in r.get('target') or []:
        nid = f"con:{t}" if f"con:{t}" in nodes else pur_map.get(t)
        if nid and r.get('text') and r['text'] not in nodes[nid]['aliases'] and r['text'] != nodes[nid]['name']:
            nodes[nid]['aliases'].append(r['text'])
            nodes[nid]['detail'].append(f"원천 표현 「{short(r['text'], 40)}」 [{r.get('source')}] — {r.get('gate_status')}")


def from_nodes(e):
    fr = e['from']
    if fr.startswith('목적:'):
        n = pur_map.get(fr[3:])
        return [n] if n else []
    if e.get('from_concerns'):
        return [f"con:{c}" for c in e['from_concerns'] if f"con:{c}" in nodes]
    if f"con:{fr}" in nodes:
        return [f"con:{fr}"]
    return []


no_anchor = 0
for e in S7['edges']:
    fs = from_nodes(e)
    if not fs:
        no_anchor += 1
        continue
    rf = e.get('resolve_flag') or ''
    f = ''
    if 'ambiguous' in rf:
        f += 'm'
    if 'no_unit_at_site' in rf:
        f += 'g'
    if 'unresolved' in rf:
        f += 'u'
    if 'not_procedure' in rf:
        f += 'n'
    det = [f"[{e['source']}] {short(e.get('basis'), 300)}", f"내림: {e.get('lowering')} · {e.get('site_check')}",
           f"고민 영역: {e['concern_region_check']}" if e.get('concern_region_check') else '', f"중증도: {e['severity']}" if e.get('severity') else '',
           f"풀이 표시: {rf}" if rf else '']
    for fr in fs:
        if e['target_kind'] == '단위 시술':
            for u in e['to_units']:
                add_edge('con_unit', fr, f"unit:{u}", e['source'][:1], det, f, gate_of(e))
        elif e['target_kind'] == '계열만' and e.get('to_family'):
            add_edge('con_fam', fr, f"fam:{e['to_family']}", e['source'][:1] + ' · 계열만', det, f, gate_of(e))
        else:
            add_loose('con_unit', fr, 'out', f"「{short(e.get('from') or '', 30)}」 대상 단위 시술 없음({e['target_kind']})", e['source'][:1], det, f, gate_of(e))

SSM = SEM['ids']['silver_string_map']   # 「목적:{이름}」 → 정본 id


def anchor_node(cid):
    if cid.startswith('목적:') and cid in SSM:
        k, v = SSM[cid].split(':', 1)
        sid = next(m_sid for (m_k, m_sid), m_c in CANON.items() if m_c == SSM[cid])
        return f"pur:{sid}" if k == 'purpose' else f"con:{sid}"
    return f"con:{cid}"


oq7_where = {w for q in S7.get('origin_questions') or [] for w in q.get('where') or []}
for c in S7['combos']:
    f = 'q' if c['id'] in oq7_where or c.get('source_id') in oq7_where else ''
    if (c.get('sales_copy') or {}).get('default_response') is False:
        pass  # 영업 문구만 기본 응답 제외 — 조합 자체는 추천
    info = [c.get('kind'), f"가격 {c['price']}" if c.get('price') else '', f"등급 {c.get('tier_label_site')}" if c.get('tier_label_site') else '']
    det = [f"제품: {' · '.join(c.get('products_text') or [])}" if c.get('products_text') else '']
    eff = c.get('effect') or {}
    det += [f"{k}: {short(v, 300)}" for k, v in eff.items() if isinstance(v, str)]
    if (c.get('sales_copy') or {}).get('default_response') is False:
        det.append('영업 문구 — 기본 응답 제외(보관)')
    add_node('combo', c['id'], c['name'], [], info, det, f, gate_of(c))
    a = c.get('anchor') or {}
    cs = a.get('concerns') or (a.get('concern') if isinstance(a.get('concern'), list) else ([a['concern']] if a.get('concern') else []))
    for cid in cs:
        add_edge('con_combo', anchor_node(cid), f"combo:{c['id']}", c.get('kind'))
    for i, (fld, comp) in enumerate((f_, x) for f_ in ('components', 'members', 'upgrade') for x in c.get(f_) or []):  # 구성 칸 셋(골드 빈틈 ② · 10-30)
        cf = ''
        if comp.get('flag') in ('ambiguous', 'concern_without_site') or (comp.get('status') or '').find('후보') >= 0:
            cf += 'm'
        for u in comp.get('units') or []:
            add_edge('combo_unit', f"combo:{c['id']}", f"unit:{u}", ('' if fld == 'components' else {'members': '비교 ', 'upgrade': '업그레이드 '}[fld]) + f"{comp.get('order') or i + 1}번",
                     [f"원문: {comp.get('text') or comp.get('family_name') or ''} — {comp.get('status')} · {short(comp.get('basis'))}"], cf)

# ───────── 8단계 관계 · 확인 조건 · 안전 · 근거
CL = {c['id']: c for c in S8['claims']}
unit_name = {u['id']: u['name'] for u in S5['units']}
EKIND_KO = {'unit_procedure': 'unit', 'family': 'fam'}

q8_claims = {}
for q in S8.get('origin_questions') or []:
    for r in q.get('refs') or []:
        q8_claims.setdefault(r, []).append(q['id'])
guide_by_claim = {}
for x in S8['evidence']['guides']:
    for c in x.get('used_by') or []:
        guide_by_claim.setdefault(c, []).append(f"{x['id']} {x['label']}")


def ends(ep):
    """endpoints.a|b → ([(노드 id, 후보?)], 한정어 문구, 노드 없는 끝 문구)."""
    k = ep['kind']
    qual = ' · '.join(f"{a} {v}" for a, v in (ep.get('qualifier') or {}).items() if v)
    if k == '단위 시술':
        return [(f"unit:{ep['id']}", False)], qual, ''
    if k in ('계열', '계열 + 조건'):
        return [(f"fam:{ep['id']}", False)], qual, ''
    if ep.get('candidates'):
        return [(f"{EKIND_KO[c['kind']]}:{c['id']}", True) for c in ep['candidates']], qual, ''
    return [], qual, k


def claim_lines(cids):
    out = []
    for cid in cids:
        c = CL[cid]
        iv = c.get('interval') or {}
        first = ''
        if iv.get('first') in ('a', 'b') and isinstance(c.get(iv['first']), dict):
            first = c[iv['first']].get('text') or ''
        days = iv.get('days')
        ds = ''
        if days:
            ds = f"{days[0]:g}~{days[1]:g}일" if days[0] != days[1] else f"{days[0]:g}일"
            ds += ' 이상' if iv.get('open_high') else ''
        sd = {True: '같은 날 가능', False: '같은 날 불가'}.get(iv.get('same_day'), '')
        cond = iv.get('condition')
        cs = (cond.get('source_label') if isinstance(cond, dict) else str(cond)) if cond else ''
        opts = ''
        if iv.get('by_sub_condition'):
            opts = '하위 조건별: ' + ' / '.join(
                f"{o.get('sub_condition')} — " + ' '.join(x for x in [
                    (f"{o['days'][0]:g}~{o['days'][1]:g}일" if o.get('days') else ''), {True: '같은 날 가능', False: '같은 날 불가'}.get(o.get('same_day'), ''),
                    (f"먼저 {o['first']}" if o.get('first') else '')] if x) for o in iv.get('options') or [])
        parts = [c['kind'], f"먼저 「{short(first, 40)}」" if first else '', ds, sd, opts, f"조건 {short(cs, 60)}" if cs else '', c.get('level_site') or '',
                 c.get('review_label') or '', f"원천 질문 {','.join(q8_claims[cid])}" if cid in q8_claims else '',
                 '시술 아님' if c.get('not_procedure') else '', '못 풂' if c.get('resolved') is False else '', c.get('gate_status') or '']
        out.append(f"{cid} · " + ' · '.join(p for p in parts if p) + f" ‖ 원문 [{c['source']}] {short(c['text'], 260)}")
        if cid in guide_by_claim:
            out.append(f"{cid} 출처(가이드): " + ' · '.join(guide_by_claim[cid]))
    return out


def resolved_line(r):
    """앱이 읽는 값(10-30 · edges[].resolved) 한 줄."""
    if not r:
        return ''
    sdl = {True: '같은 날 가능', False: '같은 날 불가'}
    def one(o):
        d = o.get('days')
        return ' '.join(x for x in [(f"먼저 끝 {o['first']}" if o.get('first') else ''), (f"{d[0]:g}~{d[1]:g}일" if d and d[0] != d[1] else f"{d[0]:g}일" if d else '') + (' 이상' if d and o.get('open_high') else ''),
                                     sdl.get(o.get('same_day'), '')] if x)
    parts = [f"앱 값(resolved · {r['status']}{' · ' + '·'.join(r['rules']) if r['rules'] else ''})", one(r) or '값 없음',
             '순서 단정 안 함(의료진 확인)' if r['field_status'].get('first', '').find('의료진') >= 0 and r.get('first') is None else '']
    if r.get('by_direction') and len({v['same_day'] for v in r['by_direction'].values() if v['same_day'] is not None}) > 1:
        parts.append('방향별 같은 날: ' + ' / '.join(f"끝 {k} 먼저 {sdl.get(v['same_day'], '정보 없음')}" for k, v in r['by_direction'].items()))
    if r.get('options'):
        parts.append('하위 조건별: ' + ' / '.join(f"{'·'.join(map(str, o['sub_condition'].values()))} — {one(o) or '정보 없음'}" for o in r['options']))
    return ' · '.join(p for p in parts if p)


for e in S8['edges']:
    A, qa, la = ends(e['endpoints']['a'])
    B, qb, lb = ends(e['endpoints']['b'])
    cl = [CL[c] for c in e['claims']]
    f = 'c' if e.get('review_status') in ('conservative', 'staff_check') else ''  # 10-30 충돌 하나로 — 보수적 선택 · 의료진 확인만 표시
    f += 's' if e.get('conditional_claims') else ''
    f += 'q' if any(c in q8_claims for c in e['claims']) or e['id'] in q8_claims else ''
    f += 'b' if any((c.get('interval') or {}).get('by_sub_condition') for c in cl) else ''
    f += 'n' if any(c.get('not_procedure') for c in cl) else ''
    f += 'u' if any(c.get('resolved') is False for c in cl) else ''
    gates = sorted({c.get('gate_status') or G_AUTO for c in cl})
    head = f"{e['id']} · 끝 a {e['endpoints']['a']['kind']}" + (f"({qa})" if qa else '') + f" · 끝 b {e['endpoints']['b']['kind']}" + (f"({qb})" if qb else '') + (' · 자기 쌍' if e.get('self_pair') else '')
    cand = []
    for side, L in (('a', A), ('b', B)):
        if any(c for _, c in L):
            cand.append(f"끝 {side} 후보 {len(L)}: " + ' · '.join(nodes[n]['name'] if n in nodes else n for n, _ in L))
    det = [head] + cand + [resolved_line(e.get('resolved'))] + claim_lines(e['claims'])
    lab = ' · '.join(e['kinds'])
    for g in gates:
        if A and B:
            for a, ca in A:
                for b, cb in B:
                    add_edge('rel', a, b, lab + (' · 후보' if (ca or cb) else ''), det, f + ('m' if (ca or cb) else ''), g)
        elif A or B:
            L, other = (A, lb) if A else (B, la)
            for n, c in L:
                add_loose('rel', n, 'out' if A else 'in', f"「{other}」", lab, det, f + ('m' if c else ''), g)

for v in S8['avoid_edges']:
    t = v['to']
    f = 's' if (v.get('scope_conditional') or v.get('default_apply') is False) else ''
    f += 'q' if v['id'] in q8_claims else ''
    det = [f"{v['id']} · {v.get('scope') or ''} · 기본 적용 {'함' if v.get('default_apply') else '안 함'} · 원래 등급 {v.get('grade_original')}",
           f"원문 [{v['source']}] {short(v['text'], 300)}", f"고민 근거: {v.get('concern_basis')}"]
    if t.get('units'):
        tg = [f"unit:{u}" for u in t['units']]
        if len(tg) > 1:
            f += 'm'
            det.append(f"후보 {len(tg)}: " + ' · '.join(unit_name.get(u, u) for u in t['units']))
    else:
        tg = [f"fam:{x}" for x in t.get('families') or []]
    for c in v.get('from_concerns') or []:
        for x in tg:
            add_edge('avoid', f"con:{c}", x, v.get('qualifier') or v.get('label'), det, f, gate_of(v))

CN = S8['conditions']
for n in CN['nodes']:
    add_node('cond', n['id'], n['name'], [x for x in n.get('match_pattern', '').split('|')], [f"원천 {' · '.join(n.get('sources') or [])} · 주장 {n.get('n_claims')}"], [], '', gate_of(n))
for w in CN.get('wait_conflicts') or []:
    flag(f"cond:{w['condition']}", 'c' + ('q' if w['id'] in q8_claims else ''))
xk_claims, xk_q = {}, set()
for g in CN.get('grade_conflicts') or []:
    for c in g['claims']:
        xk_claims.setdefault(c[0], []).append(g['id'])
        if g['id'] in q8_claims:
            xk_q.add(c[0])
prod_ids = {n['raw'] for n in nodes.values() if n['kind'] == 'prod'}


def cond_target(t):
    """확인 조건 주장 대상 → ([(노드 id, 후보?)], 노드 없는 대상 문구)."""
    if isinstance(t, list):
        xs = [(x.replace('product:', 'prod:') if x.startswith('product:') else f"unit:{x}") for x in t]
        return [(x, len(xs) > 1) for x in xs], ''
    if isinstance(t, str):
        if t.startswith('family:'):
            return [(f"fam:{t[7:]}", False)], ''
        if t.startswith('ledger:'):
            lid = t[7:]
            return ([(f"prod:{lid}", False)], '') if lid in prod_ids else ([], f"원장 항목 {lid}(행선지 없음)")
        return [], ('모든 시술' if t.startswith('모든 시술') else t)
    us = t.get('units') or []
    if us:
        return [(f"unit:{u}", len(us) > 1) for u in us], ''
    if t.get('level') == '모든 시술':
        return [], '모든 시술'
    if t.get('families'):
        return [(f"fam:{x}", len(t['families']) > 1) for x in t['families']], ''
    return [], f"「{t.get('text')}」(해석 안 됨)"


for c in CN['claims']:
    f = 'c' if c['id'] in xk_claims else ''
    f += 's' if c.get('scope_conditional') else ''
    f += 'q' if c['id'] in q8_claims or c['id'] in xk_q else ''
    tg, lo = cond_target(c['target'])
    if lo and ('해석 안 됨' in lo or '행선지 없음' in lo):
        f += 'u'
    if any(x for _, x in tg):
        f += 'm'
    det = [f"{c['id']} · {c.get('kind')} · 원래 등급 {c.get('grade_original')} → {c.get('grade3')}" + (f" · 등급 충돌 {','.join(xk_claims[c['id']])} → 기본값(더 엄격 · R2) " + ' · '.join(f"{k} {v}" for k, v in (c.get('grade3_resolved') or {}).items()) if c['id'] in xk_claims else ''),
           f"원문 [{c['source']}] {short(c['text'], 300)}", f"자리: {c['where']}" if c.get('where') else '',
           f"대상 후보 {len(tg)}: " + ' · '.join(nodes[x]['name'] if x in nodes else x for x, _ in tg) if any(x for _, x in tg) else '']
    for cn in c.get('conditions') or []:
        for x, _ in tg:
            add_edge('cond', x, f"cond:{cn}", c.get('grade3'), det, f, gate_of(c))
        if lo:
            add_loose('cond', f"cond:{cn}", 'in', lo, c.get('grade3'), det, f, gate_of(c))

SF = S8['safety']
for x in SF['complications']:
    add_node('cx', x['id'], x['name'], [], [f"{x.get('family')} · {x.get('severity_site') or x.get('severity')} · {x.get('incidence') or ''}"],
             [f"기전: {short(x.get('mechanism'), 300)}", f"대처: {short(x.get('management'), 300)}", f"예방: {short(x.get('prevention'), 300)}",
              f"원천: {x.get('source')}" if x.get('source') else ''], '', gate_of(x))
for x in SF['complications']:
    add_edge('fam_cx', f"fam:{x['family']}", f"cx:{x['id']}", x.get('severity_site') or '', [], '', gate_of(x))
# 부작용 = 계열 속성(U2 · B1) — 노드 아님 · 계열 상세에
se_by_fam = {}
for x in SF.get('side_effects') or []:
    se_by_fam.setdefault(x['family'], []).append(x)
for fm, xs in se_by_fam.items():
    if f"fam:{fm}" in nodes:
        nodes[f"fam:{fm}"]['info'].append(f"부작용(흔한 예상 반응 · 계열 속성) {len(xs)}")
        nodes[f"fam:{fm}"]['detail'] += [f"부작용 {x['id']} {x['name']} · {x.get('severity_site') or x.get('severity')} · {x.get('incidence') or ''}" for x in xs]
for fm in SF.get('complication_gap_families') or []:
    flag(f"fam:{fm}", 'g')
    nodes.get(f"fam:{fm}", {'info': []})['info'].append('합병증 정보 없음(gap · 없음 = 안전 아님)')
for fm in SF.get('side_effect_gap_families') or []:
    flag(f"fam:{fm}", 'g')
    nodes.get(f"fam:{fm}", {'info': []})['info'].append('부작용 정보 없음(gap)')
for fm in (SF.get('complication_mild_only_families') or {}).get('families') or []:
    nodes.get(f"fam:{fm}", {'info': []})['info'].append('중대 반응 없음(원천 — 전부 경미 → 부작용으로)')
for x in SF['site_caution']:
    det = [f"{x['id']} · 위험도 {x.get('danger_level')} ({x.get('danger_color')}) · 부위 대응 {x.get('site_mapping')}"]
    det += [f"혈관 {v['name']} · 깊이 {v.get('depth_mm')}mm — {short(v.get('danger'), 120)}" for v in x.get('vessels') or []]
    f = 's' if '확인' in (x.get('site_mapping') or '') else ''
    if x.get('site') in site_by_name:
        add_edge('site_caution', site_by_name[x['site']], f"fam:{x['family']}", f"위험도 {x.get('danger_level')}", det, f, gate_of(x))
# 계열 원문 속성(엣지 아님) — 상세에만
for x in SF.get('timelines') or []:
    at = x.get('attach', '')
    if at.startswith('family:') and f"fam:{at[7:]}" in nodes:
        nodes[f"fam:{at[7:]}"]['detail'].append(f"경과 타임라인 「{x['name']}」 {len(x.get('phases') or [])}단계")
for x in S8.get('profile_attrs') or []:
    if f"fam:{x['family']}" in nodes:
        nodes[f"fam:{x['family']}"]['detail'] += [f"운영 메모: {short(n, 200)}" for n in x.get('practicalNotes') or []]
for x in S8.get('attrs') or []:
    at = x.get('attach', '')
    if at.startswith('family:') and f"fam:{at[7:]}" in nodes:
        nodes[f"fam:{at[7:]}"]['detail'].append(f"안전 원문: {short(x.get('rule_title') or x.get('text'), 200)}")

EVD = S8['evidence']
STMT_CLASS = {r['statement']: r['class'] for r in SEM['statements']['table']}
for x in EVD['literature']:
    add_node('ev', x['id'], short(x.get('title'), 90), [x.get('pmid'), x.get('doi')], [f"문헌 · {x.get('journal')} {x.get('year')}"], [f"PMID {x.get('pmid')}" if x.get('pmid') else ''])
for x in EVD['web']:
    add_node('ev', x['id'], short(x['urls'][0] if x.get('urls') else x.get('url'), 90), [], ['웹' + (' · 주소 여럿' if x.get('multi_url') else '')], x.get('urls') or [])
for x in EVD['guides']:
    add_node('ev', x['id'], x['label'], [], [x.get('kind')], [f"쓰인 관계 주장 {len(x.get('used_by') or [])}"], 'q' if x['id'] in q8_claims else '')
for x in EVD['statements']:
    add_node('stmt', x['id'], short((x.get('patient') or {}).get('ko') or x['statement'], 90), [],
             [f"{x.get('family')} · 칸 {x.get('field')} · 갈래(B2) {STMT_CLASS.get(x['id'], '')} · 정확도 {x.get('accuracy_score')}"],
             [f"원문: {short(x['statement'], 300)}", f"검토: {short(x.get('accuracy_note'), 200)}"], 'w' if (x.get('accuracy_score') or 100) < 70 else '')
for x in EVD['statements']:
    add_edge('fam_stmt', f"fam:{x['family']}", f"stmt:{x['id']}", f"{x.get('field')} · {STMT_CLASS.get(x['id'], '')}")
    for v in x.get('evidence') or []:
        add_edge('stmt_ev', f"stmt:{x['id']}", f"ev:{v}")
for x in SF['complications']:
    for v in x.get('evidence') or []:
        add_edge('cx_ev', f"cx:{x['id']}", f"ev:{v}")

# ───────── 정본 id · 사전 표현
canon_of = {}
miss = []
for nid in order:
    n = nodes[nid]
    k = OLD2KIND[n['kind']]
    c = CANON.get((k, n['raw']))
    if not c:
        miss.append(nid)
        c = f"{k}:{n['raw']}"
    canon_of[nid] = c
if miss:
    sys.exit(f"정본 id 대응 없는 노드 {len(miss)}: {miss[:5]}")
by_canon = {c: nid for nid, c in canon_of.items()}
dict_n = {}
for x in SEM['dictionary']['expressions']:
    for t in x['targets']:
        nid = by_canon.get(t['id'])
        if not nid:
            continue
        n = nodes[nid]
        dict_n[nid] = dict_n.get(nid, 0) + 1
        tag = x['expr'] + (f" ({x['mode']})" if x['mode'] != '하나' else '')
        if x['expr'] != n['name'] and x['expr'] not in n['aliases'] and tag not in n['aliases']:
            n['aliases'].append(tag)

# ───────── 묶기
nid_list = order
idx = {n: i for i, n in enumerate(nid_list)}
ek_list = [e['kind'] for e in SE]
E = []
for (pk, a, b) in sorted(edges, key=lambda k: (SE_IDX[PAGE2SE[k[0]]], idx[k[1]], idx[k[2]], k[0])):
    e = edges[(pk, a, b)]
    se = SE[SE_IDX[PAGE2SE[pk]]]
    inh = 1 if se['inherit'] and (nodes[a]['kind'] == 'fam' or nodes[b]['kind'] == 'fam') and se['kind'] != 'key_family' else 0
    E.append([SE_IDX[se['kind']], idx[a], idx[b], ''.join(sorted(e['flags'])), ' · '.join(e['label']), e['detail'], ' · '.join(sorted(e['gate'])), inh])
LOOSE = [[SE_IDX[PAGE2SE[x['pk']]], idx[x['n']], x['dir'], x['other'], x['flags'], x['label'] or '', x['detail'], x['gate']] for x in loose]
KN = [OLD2KIND[nodes[n]['kind']] for n in nid_list]
N = []
for nid in nid_list:
    n = nodes[nid]
    N.append([KIND_IDX[OLD2KIND[n['kind']]], n['raw'], n['name'], [a for a in n['aliases'] if a][:60], n['flags'], n['info'], n['detail'], canon_of[nid], n['gate'], dict_n.get(nid, 0)])
kmeta = []
for i, k in enumerate(SK):
    got = sum(1 for n in N if n[0] == i)
    kmeta.append({'k': k['kind'], 'label': k['name'], 'meaning': k['meaning'], 'gloss': GLOSS.get(k['name'], ''), 'src': f"{k['canon']} {k['path']}",
                  'id': k['canonical_id'], 'n': got, 'canon_n': k['count']})
    if got != k['count']:
        sys.exit(f"노드 셈이 정본과 다름: {k['kind']} 페이지 {got} · 정본 {k['count']}")
ek_meta = []
for j, se in enumerate(SE):
    es = [x for x in E if x[0] == j]
    ls = [x for x in LOOSE if x[0] == j]
    fk = sorted({x[0] for x in [N[e[1]] for e in es]} | {N[x[1]][0] for x in ls if x[2] == 'out'})
    tk = sorted({x[0] for x in [N[e[2]] for e in es]} | {N[x[1]][0] for x in ls if x[2] == 'in'})
    ek_meta.append({'k': se['kind'], 'label': se['name'], 'meaning': se['meaning'], 'gloss': GLOSS.get(se['name'], ''), 'src': f"{se['canon']} {se['path']}",
                    'inherit': se['inherit'], 'attrs': se['attrs'], 'canon_n': se['count'], 'n': len(es), 'loose': len(ls),
                    'from': [SK[i]['kind'] for i in fk], 'to': [SK[i]['kind'] for i in tk], 'frm_txt': se['frm'], 'to_txt': se['to']})
examples = []
for kind, name in [('concern', '기미'), ('concern', '처짐'), ('concern', '피부결'), ('unit_procedure', '얼굴 전체 토닝'), ('family', '성형용 필러')]:
    hit = next((i for i, n in enumerate(N) if SK[n[0]]['kind'] == kind and n[2] == name), None)
    if hit is None:
        sys.exit(f'예시 시작점 없음: {kind} {name}')
    examples.append({'label': f"{SK[KIND_IDX[kind]]['name']} 「{name}」", 'i': hit})
DATA = {
    'version': 'silver-graph v2 (semantic)',
    'semantic': {'version': SEM['version'], 'decision_ref': SEM['decision_ref'], 'summary': {k: v for k, v in SEM['summary'].items() if not isinstance(v, dict)}},
    'inputs': {f: v['version'] for f, v in SEM['inputs'].items()},
    'flags': FLAGS, 'gate': {'values': GATE['values'], 'rule': GATE['rule']}, 'kinds': kmeta, 'ekinds': ek_meta, 'nodes': N, 'edges': E, 'loose': LOOSE, 'examples': examples,
    'attrs_not_nodes': [{'what': x['what'], 'where': x['where'], 'n': x['count'], 'rule': x['rule']} for x in SEM['attributes_not_nodes']],
    'not_edges': SEM['not_edges'],
    'inheritance': [{'id': x['id'], 'name': x['name'], 'rule': x['rule']} for x in SEM['inheritance']],
    'notes': [f"7단계 고민 → 시술 엣지 중 앵커(고민 · 목적 노드) 없는 원천 행 {no_anchor} — 그림 밖(쁘띠시술 등 · step7 J5)",
              '끝점 묶음(단위 시술 후보 · 계열 묶음)은 노드가 아니다(U3 · B3) — 후보마다 선을 긋고 「후보 여럿」 표시 · 같은 기록이면 상세 첫 줄 id 가 같다',
              '끝이 「모든 시술」 · 해석 안 됨 · 행선지 없는 원장 항목인 엣지는 상대 노드의 「대상 노드 없는 엣지」로 보여 준다',
              '정본 셈 = semantic.json 의 기록 셈 · 선 = 페이지가 그은 선(후보 · 끝점 쌍마다 하나 · 같은 쌍은 하나로 합침)',
              '부작용(흔한 예상 반응)은 계열 속성(U2 · B1) — 계열 상세에 · 합병증만 노드',
              '원천 표현 대응(step7 correspondence)과 사전 표현(semantic.json dictionary)은 검색 이름으로 넣음',
              '계열 원문 속성(경과 타임라인 · 운영 메모 · 안전 원문)은 계열 상세에만 — 파생 엣지 안 만듦',
              f"단위 시술 부위 「해당 없음」 · 「병변 단위」 {sum(1 for u in S5['units'] if u['key']['site'] not in site_by_name)}개는 부위 노드가 없어 부위 엣지 없음(step5 rules.special_sites)",
              '계열 단위 엣지는 「계열에서 상속」으로만 보여 줌 — 단위 시술에 펼치는 건 골드 일(B7)'],
}

if __name__ == '__main__':
    js = json.dumps(DATA, ensure_ascii=False, separators=(',', ':'), sort_keys=False).replace('</', '<\\/').replace('�', '\\ufffd')
    h = open(HTML, encoding='utf-8').read()
    pre, rest = h.split('<script id="data" type="application/json">', 1)
    _, post = rest.split('</script>', 1)
    open(HTML, 'w', encoding='utf-8').write(pre + '<script id="data" type="application/json">' + js + '</script>' + post)
    print(f"노드 종류 {len(kmeta)} · 엣지 종류 {len(ek_meta)} · 표시 {len(FLAGS)} · 노드 {len(N)} · 선 {len(E)} · 노드 없는 끝 {len(LOOSE)} · 데이터 {len(js.encode()):,} B")
    for k in kmeta:
        print(' ', k['k'], k['label'], k['n'], '정본', k['canon_n'])
    for k in ek_meta:
        print(' ', k['k'], k['label'], '정본', k['canon_n'], '선', k['n'], '끝 없음', k['loose'], k['from'], '→', k['to'], '(상속)' if k['inherit'] else '')
