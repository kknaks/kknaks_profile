"""실버 5단계(단위 시술) 반영 — 결정론(3단계 · 4단계와 같은 구조).

입력: step5-decisions.json(결정 — 단위 시술 키 · 원장 521 행선지 · 시장가 · 쁘띠시술 메뉴 · 넘겨받은 것 · 붙는 규칙)
      원천(결정 source.path) taxonomy · market-pricing · pih-risk · procedure-profiles · anatomy-danger-zones
      step1-products · step2-families · step3-sites · step4-techniques · source-map(읽기만)
출력: step5-units.json · step5-units.md · step5-origin-questions.md

행은 원천에서 이 스크립트가 만든다. 원천 행인데 결정에 없으면 open[], 결정이 가리키는 키 · 계열 · 부위 · 기법이 정본에 없으면 open[].
결정 파일에 한 줄 더하면 닫힌다. 숫자는 이 파일에 적지 않는다(고정 assert 없음).
"""
import argparse
import collections
import json
import re
from pathlib import Path

W = Path(__file__).resolve().parent
AP = argparse.ArgumentParser()
AP.add_argument('--source', help='원천 경로 덮어쓰기(고정 시험용)')
AP.add_argument('--decisions', default=str(W / 'step5-decisions.json'))
AP.add_argument('--out', default=str(W), help='산출 폴더(고정 시험은 임시 폴더)')
ARGS = AP.parse_args()
OUT = Path(ARGS.out)
DEC = json.load(open(ARGS.decisions))
SRC = Path(ARGS.source or DEC['source']['path'])
J = lambda p: json.load(open(p))
S1, S2, S3, S4 = (J(W / DEC['canon'][k]) for k in ('step1', 'step2', 'step3', 'step4'))
SMAP = J(W / DEC['canon']['source_map'])
TAX = J(SRC / 'taxonomy.json')
MKT = J(SRC / 'market-pricing.json')
PIH = J(SRC / 'pih-risk.json')
PROF = J(SRC / 'procedure-profiles.json')['profiles']
ZONES = J(SRC / 'anatomy-danger-zones.json')['zones']

OPEN, STALE = [], []


def op(t, **kw):
    OPEN.append(dict(type=t, **kw))


# ───────── 0. 정본 ─────────
PROD = {x['ledger_id']: x for x in S1['items']}
ACTIVE = {k for k, x in PROD.items() if x.get('active')}
FAM = {f['id']: f for f in S2['families']}
PF = {p['ledger_id']: p for p in S2['product_family']}
SITE = {n['name']: n for n in S3['nodes']}
SPECIAL = DEC['special_sites']
TECH = {n['id']: n for n in S4['nodes']}
FDEF = {f['family']: f for f in S4['family_defaults']}


def site_children(name):
    out, todo = [], [name]
    while todo:
        c = todo.pop()
        out.append(c)
        todo += [n['name'] for n in S3['nodes'] if n['parent'] == c]
    return out


def pname(lid):
    return PROD[lid]['2_names']['display_name'] if lid in PROD else lid


# ───────── 1. 단위 시술 키 ─────────
UNITS = {}
KEYS = {}
for u in DEC['units']:
    k = u['key']
    bad = []
    if k['family'] not in FAM:
        bad.append(f"계열 {k['family']} 없음(2단계)")
    elif k.get('sub_family') and k['sub_family'] not in FAM[k['family']]['sub_families']:
        bad.append(f"하위 {k['sub_family']} 가 {k['family']} 칸 아님")
    if k.get('ingredient') and k['family'] != 'M16':
        bad.append('성분 칸은 M16 만')
    if k['site'] not in SITE and k['site'] not in SPECIAL:
        bad.append(f"부위 {k['site']} 없음(3단계 · 특수 부위)")
    elif k['site'].endswith('(묶음)'):
        bad.append('묶음 부위는 키를 만들지 않음(S5)')
    if k['technique'] not in TECH:
        bad.append(f"기법 {k['technique']} 없음(4단계)")
    kt = (k['family'], k.get('sub_family'), k.get('ingredient'), k.get('ingredient_of'), k['site'], k['technique'])
    if kt in KEYS:
        bad.append(f'키 겹침 {KEYS[kt]}')
    if bad:
        op('단위 시술 키 오류', unit=u['id'], reason=' · '.join(bad))
    KEYS[kt] = u['id']
    UNITS[u['id']] = dict(u, sources=[], synonyms=[], candidate_of=[], uses_product=[], purposes=[], route_status=None)
names = collections.Counter(u['name'] for u in UNITS.values())
for n, c in names.items():
    if c > 1:
        op('단위 시술 이름 겹침', name=n)


def units_ok(ids, where):
    good = [i for i in ids if i in UNITS]
    for i in ids:
        if i not in UNITS:
            op('결정이 가리키는 키 없음', where=where, unit=i)
    return good


def resolve(r, where):
    """이름이 부르는 단위 시술 — 계열 · 하위 · 기법 · 묶음 부위 규칙(조회 때 후보)."""
    out = []
    for i, u in UNITS.items():
        k = u['key']
        if k['family'] != r['family']:
            continue
        if 'sub_family' in r and k.get('sub_family') != r['sub_family']:
            continue
        if 'technique' in r and k['technique'] != r['technique']:
            continue
        if 'site_group' in r and k['site'] not in site_children(r['site_group']):
            continue
        out.append(i)
    if not out:
        op('이름이 부르는 단위 시술 없음', where=where, rule=r)
    return sorted(out)


def add_source(ids, src, sid, name, role, extra=None):
    for i in ids:
        UNITS[i]['sources'].append(dict(src=src, id=sid, name=name, role=role, **(extra or {})))
        if role == '후보':
            UNITS[i]['candidate_of'].append(name)
        elif role == '출처':  # J7 G5 — 복합 이름(「사마귀」 냉동/CO2)의 한 갈래: 근거만 · 동의어로 안 붙임
            pass
        elif name and name != UNITS[i]['name']:
            UNITS[i]['synonyms'].append(dict(text=name, type={'ledger': '원장 이름', 'market': '시장가 이름', 'problem_P1': '쁘띠시술 메뉴 이름', 'step1_moved': '1단계 시술 이름', 'handoff': '넘겨받은 이름', 'step7': '7단계 원천 이름'}[src], src=sid))


# ───────── 2. 원장 항목 521 ─────────
LED = {d['id']: d for d in DEC['ledger']}
SRC_LED = [(m['id'], s['id'], i) for m in TAX['modality'] for s in m['subcategories'] for i in s['items']]
DESTS = {'제품', '제품 + 단위 시술', '단위 시술', '6단계 패키지', '다른 단계 이름', '시술 아님(다른 단계)', '값', '시술 아님', '원장님 문의'}
ledger_rows = []
seen = set()
for fam, sub, it in SRC_LED:
    lid = it['id']
    seen.add(lid)
    d = LED.get(lid)
    row = dict(id=lid, name=it['name'], detail=it.get('detail'), source_family=fam, source_sub=sub)
    if d is None:
        op('결정 없는 원장 항목', id=lid, name=it['name'])
        row.update(dest=None)
        ledger_rows.append(row)
        continue
    if d['name'] != it['name']:
        op('원장 항목 이름 바뀜', id=lid, decision=d['name'], source=it['name'])
    if d['dest'] not in DESTS:
        op('원장 행선지 값 밖', id=lid, dest=d['dest'])
    row.update({k: d.get(k) for k in ('dest', 'rule', 'role', 'basis', 'fgroup', 'decided_by', 'to', 'evidence_level', 'origin_question', 'note', 'source_fix')})
    if d['dest'] in ('제품', '제품 + 단위 시술'):
        p = PROD.get(lid)
        if p is None:
            op('원장 「제품」인데 1단계 행 없음', id=lid)
        elif p.get('moved_to'):
            op('원장 「제품」인데 1단계에서 시술 이름으로 빠짐', id=lid)
        else:
            row['product'] = p.get('merged_into') or lid
            row['product_state'] = 'merged' if p.get('merged_into') else ('active' if p.get('active') else 'inactive')
    ids = []
    if d['dest'] in ('단위 시술', '제품 + 단위 시술'):
        ids = units_ok(d['units'], lid)
        if not ids:
            op('원장 「단위 시술」인데 키 없음', id=lid)
    elif d['dest'] == '다른 단계 이름':
        ids = resolve(d['resolve'], lid)
    row['units'] = ids
    if ids:
        add_source(ids, 'ledger', lid, it['name'], d.get('role', '이름'), {'detail': it.get('detail')})
        for i in ids:
            UNITS[i]['purposes'] += d.get('purposes') or []
    for pid in (d.get('uses_product_ids') or []) + ([lid] if d.get('uses_product') else []):
        if pid not in ACTIVE:
            op('저장 uses_product 제품이 1단계 active 아님', id=lid, product=pid)
            continue
        for i in ids:
            UNITS[i]['uses_product'].append(dict(product=pid, basis=f"원장 이름 「{it['name']}」({d['decided_by']})"))
    ledger_rows.append(row)
STALE += [['ledger', k] for k in LED if k not in seen]

# ───────── 3. 쁘띠시술 메뉴(P1) ─────────
P1D = {d['id']: d for d in DEC['problem_P1']}
p1_rows = []
p1_src = [i for p in TAX['problem'] if p['id'] == 'P1' for s in p['subcategories'] for i in s['items']]
for it in p1_src:
    d = P1D.get(it['id'])
    if d is None:
        op('결정 없는 쁘띠시술 메뉴', id=it['id'], name=it['name'])
        continue
    ids = resolve(d['resolve'], it['id']) if 'resolve' in d else units_ok(d['units'], it['id'])
    add_source(ids, 'problem_P1', it['id'], it['name'], d['role'])
    p1_rows.append(dict(id=it['id'], name=it['name'], dest=d['dest'], units=ids, role=d['role'], decided_by=d['decided_by'], note=d.get('note')))
STALE += [['problem_P1', k] for k in P1D if k not in {i['id'] for i in p1_src}]

# ───────── 4. 시장가 ─────────
MD = {d['name']: d for d in DEC['market']}
market_rows = []
mk_src = [(c['id'], i) for c in MKT['categories'] for i in c['items']]
for cat, it in mk_src:
    d = MD.get(it['name'])
    if d is None:
        op('결정 없는 시장가 행', name=it['name'], category=cat)
        continue
    ids = units_ok(d['units'], it['name'])
    if d['kind'] == '시술 1회' and not ids:
        op('시술 1회인데 키 없음', name=it['name'])
    row = dict(name=it['name'], category=cat, unit_raw=it.get('unit'), price=dict(low=it.get('low'), mid=it.get('mid'), high=it.get('high'), currency=MKT.get('currency')),
               kind=d['kind'], units=ids, role=d.get('role', '이름'), product=d['product'], grade=d.get('grade'), spec=d.get('spec'), sessions=d.get('sessions'),
               note=d.get('note'), to=d.get('to'), fgroup=d.get('fgroup'), category_conflict=d.get('category_conflict'), decided_by=d['decided_by'], origin_question=d.get('origin_question'), staff_question=d.get('staff_question'))
    for pid in d['product']:
        if pid not in ACTIVE:
            op('시장가 제품이 1단계 active 아님', name=it['name'], product=pid)
    if ids:
        add_source(ids, 'market', it['name'], it['name'], row['role'])
        for i in ids:
            UNITS[i].setdefault('market', []).append(dict(name=it['name'], price=row['price'], product=d['product'], grade=d.get('grade'), spec=d.get('spec'),
                                                          sessions=d.get('sessions'), role=row['role']))
            if row['role'] == '이름':
                for pid in d['product']:
                    if pid in ACTIVE:
                        UNITS[i]['uses_product'].append(dict(product=pid, basis=f"시장가 이름 「{it['name']}」"))
    market_rows.append(row)
STALE += [['market', k] for k in MD if k not in {i['name'] for _, i in mk_src}]

# 1단계 제품 행 시장가 사본 → 같은 이름 시장가 행의 시술 1회
copies = []
MROW = {r['name']: r for r in market_rows}
for lid, p in PROD.items():
    sp = p.get('5_spec') or {}
    for fld in ('market', 'market_pricing'):
        for c in sp.get(fld) if isinstance(sp.get(fld), list) else []:
            m = MROW.get(c['source_item'])
            if m is None:
                op('1단계 시장가 사본에 같은 이름 시장가 행 없음', product=lid, source_item=c['source_item'])
                continue
            copies.append(dict(product=lid, name=pname(lid), source_item=c['source_item'], to=m['kind'], units=m['units'], product_matches=lid in m['product']))

# ───────── 5. 넘겨받은 것 ─────────
H = DEC['handoffs']
handoff_rows = collections.OrderedDict()
# 1단계 moved_to
hd = {x['id']: x for x in H['step1_moved_to']}
rows = []
for lid, p in PROD.items():
    if not p.get('moved_to'):
        continue
    d = hd.get(lid)
    if d is None:
        op('넘겨받은 것 행선지 없음', source='1단계 moved_to', id=lid, name=pname(lid))
        continue
    ids = units_ok(d['units'], lid)
    add_source(ids, 'step1_moved', lid, p['2_names'].get('ledger_name') or pname(lid), d['role'])
    rows.append(dict(id=lid, name=p['2_names'].get('ledger_name') or pname(lid), units=ids, role=d['role'], decided_by=d['decided_by']))
STALE += [['step1_moved_to', k] for k in hd if not (PROD.get(k) or {}).get('moved_to')]
handoff_rows['1단계 moved_to'] = rows
# 2단계 deferred
hd = {(x['family'], x['source']): x for x in H['step2_deferred']}
rows, s2src = [], set()
for f in S2['families']:
    for d0 in f.get('deferred') or []:
        s2src.add((f['id'], d0['source']))
        d = hd.get((f['id'], d0['source']))
        if d is None:
            op('넘겨받은 것 행선지 없음', source='2단계 deferred', family=f['id'], item=d0['source'])
            continue
        rows.append(dict(family=f['id'], source=d0['source'], deferred_to=d0['deferred_to'], to=d['resolution'], decided_by=d['decided_by']))
STALE += [['step2_deferred', list(k)] for k in hd if k not in s2src]
handoff_rows['2단계 deferred'] = rows
# 3단계 → 5단계
hd = {tuple(x['key']): x for x in H['step3_to5']}
rows, s3src = [], set()
for d0 in S3['deferred']:
    if '5단계' not in d0['stage']:
        continue
    s3src.add(tuple(d0['key']))
    d = hd.get(tuple(d0['key']))
    if d is None:
        op('넘겨받은 것 행선지 없음', source='3단계 deferred', key=d0['key'])
        continue
    rows.append(dict(string=d0['string'], key=d0['key'], to=d['to'], decided_by=d['decided_by']))
STALE += [['step3_to5', list(k)] for k in hd if k not in s3src]
handoff_rows['3단계 → 5단계'] = rows
# 4단계 handoffs · 5단계 표현
hd = {x['id']: x for x in H['step4_handoffs']}
rows = []
for d0 in S4['handoffs']:
    d = hd.get(d0['id'])
    if d is None:
        op('넘겨받은 것 행선지 없음', source='4단계 handoffs', id=d0['id'])
        continue
    rows.append(dict(id=d0['id'], item=d0['item'], to=d['to'], decided_by=d['decided_by']))
STALE += [['step4_handoffs', k] for k in hd if k not in {x['id'] for x in S4['handoffs']}]
hd = {x['text']: x for x in H['step4_expressions']}
s4e = [e for e in S4['expressions'] if e.get('stage') == '5단계']
for e in s4e:
    d = hd.get(e['text'])
    if d is None:
        op('넘겨받은 것 행선지 없음', source='4단계 표현(5단계)', text=e['text'])
        continue
    rows.append(dict(id=e['text'], item=f"{e['text']}({e['key']})", to=d['to'], decided_by=d['decided_by']))
STALE += [['step4_expressions', k] for k in hd if k not in {e['text'] for e in s4e}]
handoff_rows['4단계 → 5단계'] = rows
# 지도 5단계 칸
hd = {(x['file'], x['path']): x for x in H['map_fields']}
rows, msrc = [], set()
for f in SMAP['fields']:
    if not any(d0.get('stage') == '5' for d0 in f['destinations']):
        continue
    msrc.add((f['file'], f['path']))
    d = hd.get((f['file'], f['path']))
    if d is None:
        op('넘겨받은 것 행선지 없음', source='source-map 5단계 칸', file=f['file'], path=f['path'])
        continue
    rows.append(dict(file=f['file'], path=f['path'], status=f['status'], to=d['resolution'], decided_by=d['decided_by']))
STALE += [['map_fields', list(k)] for k in hd if k not in msrc]
handoff_rows['지도 5단계 칸'] = rows

# 7단계가 넘긴 시술 이름(J7 · 10-29 — 고민 트리 · CC 추천 시술 · 최적화 · 비교 원천의 이름 칸)
T7SRC = {'taxonomy.problem': None, 'problem-packages': 'problem-packages.json', 'treatment-optimization': 'treatment-optimization.json', 'procedure-comparison': 'procedure-comparison.json'}
T7TXT = {}
for k, f in T7SRC.items():
    if f:
        T7TXT[k] = json.dumps(J(SRC / f), ensure_ascii=False)
P_ITEMS = {i['id']: i for p in TAX['problem'] for s in p['subcategories'] for i in s['items']}
rows = []
for d in DEC.get('step7_names') or []:
    if d['source'] not in T7SRC:
        op('7단계 이름 원천 값 밖', id=d['id'], source=d['source'])
        continue
    if d['source'] == 'taxonomy.problem':
        it = P_ITEMS.get(d['id'])
        if it is None or it['name'] != d['name']:
            STALE.append(['step7_names', d['id'], d['name']])
            continue
    elif json.dumps(d['name'], ensure_ascii=False) not in T7TXT[d['source']]:
        STALE.append(['step7_names', d['id'], d['name']])
        continue
    ids = units_ok(d['units'], d['id'])
    add_source(ids, 'step7', d['id'], d['name'], d['role'], {'detail': d.get('detail')})
    for i in ids:
        UNITS[i]['purposes'] += d.get('purposes') or []
    rows.append(dict(id=d['id'], source=d['source'], name=d['name'], units=ids, role=d['role'], decided_by=d['decided_by'], origin_question=d.get('origin_question')))
handoff_rows['7단계 → 5단계(J7)'] = rows

# 원천 근거 없는 키
for i, u in UNITS.items():
    if not u['sources']:
        op('원천 근거 없는 키', unit=i, name=u['name'])

# ───────── 6. 쓰는 제품 ─────────
PLR = DEC['product_link_rule']
for x in PLR['extra_stored']:
    if x['product'] not in ACTIVE:
        op('저장 uses_product 제품이 1단계 active 아님', product=x['product'])
    elif x['unit'] not in UNITS:
        op('결정이 가리키는 키 없음', where='extra_stored', unit=x['unit'])
    else:
        UNITS[x['unit']]['uses_product'].append(dict(product=x['product'], basis=x['basis']))
GUARD = {p: g for g in PLR['guards'] for p in g['products']}
for u in UNITS.values():
    seen_p, keep = set(), []
    for up in u['uses_product']:
        g = GUARD.get(up['product'])
        if g and u['key']['technique'] not in g['allowed_techniques']:
            continue
        if up['product'] not in seen_p:
            seen_p.add(up['product'])
            keep.append(dict(up, name=pname(up['product']), recommendable=PROD[up['product']]['4_license']['recommendable']))
    u['uses_product'] = keep
# 장비 이름 동의어 대상 더하기(결정 device_synonym_extra · 사용자 10-30 판단 ③) — 한 장비가 두 매질 키를 내는데 저장 연결이 한쪽만일 때
for x in DEC.get('device_synonym_extra') or []:
    for i in x['units']:
        if i not in UNITS:
            op('결정이 가리키는 단위 시술 없음', where=f"device_synonym_extra {x['product']}", unit=i)
            continue
        if x['product'] not in PROD:
            op('저장 uses_product 제품이 1단계 active 아님', id='device_synonym_extra', product=x['product'])
            continue
        if not any(up['product'] == x['product'] for up in UNITS[i]['uses_product']):
            UNITS[i]['uses_product'].append(dict(product=x['product'], basis=x['basis'], name=pname(x['product']), recommendable=PROD[x['product']]['4_license']['recommendable']))
stored_by_p = collections.defaultdict(list)
for i, u in UNITS.items():
    for up in u['uses_product']:
        stored_by_p[up['product']].append(i)
# 기법 호환(F1 · 10-29) — 근거 = 4단계 device_attrs(2단계 technique_hint 정리) · 매질 일치 · 계열 기법 하나(코디 답 A)
TC = PLR['technique_compat']
TREQ = {r['technique']: r for r in TC['requires']}
HINT = {h['ledger_id']: h for h in S4['device_attrs']['technique_hints']}
KEY_SUB_FAMS = {u['key']['family'] for u in UNITS.values() if u['key'].get('sub_family')}  # 키에 하위가 있는 계열(J1 안 C)
for t, r in TREQ.items():
    if t not in TECH:
        op('기법 호환 기법이 4단계에 없음', id=t)
    for v in (r.get('pulse_mode_any') or []) + [x for vs in (r.get('pulse_mode_by_medium') or {}).values() for x in vs]:
        if v not in S4['dictionaries']['pulse_mode']:
            op('기법 호환 펄스 값이 4단계 사전 밖', id=t, value=v)
    for v in r.get('modes_any') or []:
        if v not in {m['value'] for m in S4['dictionaries']['modes']}:
            op('기법 호환 가능 방식 값이 4단계 사전 밖', id=t, value=v)
for h in HINT:
    if h not in PROD:
        op('장비 속성 제품이 1단계에 없음', product=h)


def single_tech(fam, tech):
    f = FDEF.get(fam)
    return bool(f) and not f['also'] and f['default'] == tech and not TECH[tech].get('children')


FEV = {e['family']: e for e in TC['family_evidence']}
SPLIT = {f for f in KEY_SUB_FAMS | {f for f, d in FDEF.items() if d['also']}}  # 기법이 갈릴 수 있는 계열(키 하위 · 4단계 also)
for f in sorted(SPLIT):
    ts = sorted({u['key']['technique'] for u in UNITS.values() if u['key']['family'] == f and not single_tech(f, u['key']['technique'])})
    if not ts:
        continue
    if f in FEV:
        for e_t in {t for vs in list((FEV[f].get('sub_family_map') or {}).values()) + list((FEV[f].get('kind_map') or {}).values()) + [FEV[f].get('sub_family_any') or []] for t in vs}:
            if e_t not in TECH:
                op('기법 호환 기법이 4단계에 없음', id=e_t)
        for pid in FEV[f].get('product_map') or {}:
            if pid not in PROD:
                op('기법 호환 제품이 1단계에 없음', product=pid)
        for sb in FEV[f].get('sub_family_map') or {}:
            if sb not in FAM[f]['sub_families']:
                op('기법 호환 하위 계열이 2단계에 없음', id=f, value=sb)
        continue
    for t in ts:
        if t not in TREQ:
            op('기법 호환 결정 없는 기법', id=t)


def tech_ok(h, req, mediums):
    """장비 속성 h 가 기법 조건 req 를 채우나 — None 이면 판단할 조건이 없음."""
    if 'pulse_mode_any' in req:
        allowed = set(req['pulse_mode_any']) | {x for m in mediums for x in (req.get('pulse_mode_by_medium') or {}).get(m, [])}
        return bool(set(h['pulse_mode']) & allowed)
    if 'modes_any' in req:
        return bool(set(h['modes']) & set(req['modes_any']))
    return None


def prod_techs(lid, fam, subs):
    """계열 근거(family_evidence)로 본 이 제품의 기법 — None 이면 근거 없음."""
    e = FEV[fam]
    if lid in (e.get('product_map') or {}):
        return set(e['product_map'][lid]['techniques'])
    sb = [m for f, m in subs if f == fam and m]
    kind = (PROD[lid].get('1_identity') or {}).get('kind') or ''
    out = set()
    for m in sb:
        out |= set((e.get('sub_family_map') or {}).get(m, []))
        out |= set(e.get('sub_family_any') or [])
    if not sb or not e.get('kind_only_without_sub'):
        for w, ts in (e.get('kind_map') or {}).items():
            if (kind == w) if e.get('kind_exact') else (w in kind):
                out = set(ts) if e.get('kind_overrides') else out | set(ts)
    return out or None


PEV = {}  # 제품 출처 근거(v2 F1 · 10-29) — 1단계 detail · 허가 · 원장 detail 이 그 단위 시술(기법 · 목적 「제모」 키)을 채울 때만
for e in TC.get('product_evidence') or []:
    if e['product'] not in PROD:
        op('기법 호환 제품이 1단계에 없음', product=e['product'])
    for i in e['units']:
        if i not in UNITS:
            op('결정이 가리키는 키 없음', where='product_evidence', unit=i)
    PEV.setdefault(e['product'], set()).update(e['units'])
SUB_TECHS = collections.defaultdict(set)
for u in UNITS.values():
    if u['key'].get('sub_family'):
        SUB_TECHS[(u['key']['family'], u['key']['sub_family'])].add(u['key']['technique'])


def tech_conditioned(t, medium):
    """기법 조건이 이 매질 장비를 가르나 — 가능 방식(프락셔널)은 없는 장비가 있어 늘 조건 · 펄스는 사전 전부를 허용하면 조건 아님(엔디야그 K04a)."""
    r = TREQ.get(t) or {}
    if 'modes_any' in r:
        return True
    if 'pulse_mode_any' in r:
        allowed = set(r['pulse_mode_any']) | set((r.get('pulse_mode_by_medium') or {}).get(medium, []))
        return not set(S4['dictionaries']['pulse_mode']) <= allowed
    return False


def medium_decides(f, sub, t):
    """매질 일치가 기법 근거인가(v2 F1) — 그 매질 키 기법이 서로 갈리는 둘 이상(상하위 아님)이거나 기법에 조건이 있으면 아님."""
    ts = SUB_TECHS[(f, sub)]
    split = any(a != b and TECH[a].get('parent') != b and TECH[b].get('parent') != a for a in ts for b in ts)
    return not split and not any(tech_conditioned(x, sub) for x in ts)


def compat(lid, k, subs, i=None):
    """(호환, 사유) — 키 하위 있음 = 매질이 기법을 정하면 매질 일치 · 아니면 기법 근거 / 하위 null = 기법 근거 있어야."""
    f, t = k['family'], k['technique']
    if i in PEV.get(lid, ()):
        return True, None
    if f not in SPLIT or single_tech(f, t):
        return True, None
    sub = k.get('sub_family')
    if f in FEV:
        ts = prod_techs(lid, f, subs)
        if sub:
            if ts is not None:
                return (True, None) if t in ts else (False, f"계열 근거 어긋남({t})")
            if lid in GUARD:  # 4단계 H13 가드 = 제품 기법 출처(도포만)
                return True, None
            return (True, None) if medium_decides(f, sub, t) else (False, f"매질만 · 기법 근거 없음({t})")
        return (True, None) if ts and t in ts else (False, f"기법 근거 없음({t})")
    req = TREQ.get(t)
    h = HINT.get(lid)
    if sub:
        ok = tech_ok(h, req, [sub]) if h and req else None
        if ok is False:
            return False, f"장비 속성 어긋남({t})"
        if ok or medium_decides(f, sub, t):
            return True, None
        return False, f"매질만 · 기법 근거 없음({t})"
    ok = tech_ok(h, req, [m for f2, m in subs if f2 == f]) if h and req else None
    return (True, None) if ok else (False, f"매질 미지정 키 · 기법 근거 없음({t})")


product_links = []
for lid in sorted(ACTIVE):
    pf = PF.get(lid)
    if pf is None:
        op('1단계 active 제품이 2단계에 없음', product=lid)
        continue
    fams = [pf['family']] + list(pf.get('also_families') or [])
    subs = {(pf['family'], pf.get('sub_family'))} | {(a['family'], a['sub_family']) for a in pf.get('also_sub_families') or []}
    cand, tex = [], []
    for i, u in UNITS.items():
        k = u['key']
        if k['family'] not in fams:
            continue
        if k.get('sub_family') and (k['family'], k['sub_family']) not in subs:
            continue
        g = GUARD.get(lid)
        if g and k['technique'] not in g['allowed_techniques']:
            continue
        ok, why = compat(lid, k, subs, i)
        if not ok:
            tex.append(dict(unit=i, reason=why))
            continue
        cand.append(i)
    stored = sorted(set(stored_by_p.get(lid, [])))
    inh = sorted(set(cand) - set(stored))
    tex = [x for x in tex if x['unit'] not in stored]
    if pf['family'] is None:
        link = '원장님 문의(계열 없음)'
    elif pf['family'] == '계열 밖':
        link = '계열 밖(단위 시술 없음)'
    elif stored:
        link = '저장 uses_product'
    elif inh:
        link = '조회 때 상속 후보'
    elif tex:
        link = '계열 has_product 만(기법 호환 단위 시술 없음 — F1)'
    else:
        link = '계열 has_product 만(이 계열 · 하위에 단위 시술 없음)'
    product_links.append(dict(product=lid, name=pname(lid), family=pf['family'], sub_family=pf.get('sub_family'), recommendable=PROD[lid]['4_license']['recommendable'],
                              stored_units=stored, inherited_candidates=inh, technique_excluded=tex, technique_attrs=dict((k, HINT[lid][k]) for k in ('pulse_mode', 'modes', 'ablative')) if lid in HINT else None, guard=GUARD[lid]['basis'] if lid in GUARD else None, link=link))
# 하위 키 상속 근거 셈(v2 F1) — 매질이 기법을 못 정하는 키에 이어진 쌍마다 근거 종류 · 「매질만」 = 0 이어야
SUB_EV = collections.Counter()
for x in product_links:
    pfx = PF[x['product']]
    subs_x = {(pfx['family'], pfx.get('sub_family'))} | {(a['family'], a['sub_family']) for a in pfx.get('also_sub_families') or []}
    for i in x['inherited_candidates']:
        k = UNITS[i]['key']
        if not k.get('sub_family') or k['family'] not in SPLIT or single_tech(k['family'], k['technique']) or medium_decides(k['family'], k['sub_family'], k['technique']):
            continue
        lid = x['product']
        if i in PEV.get(lid, ()):
            SUB_EV['제품 출처'] += 1
        elif k['family'] in FEV and prod_techs(lid, k['family'], subs_x) is not None:
            SUB_EV['계열 근거(종류 · 출처)'] += 1
        elif lid in GUARD:
            SUB_EV['4단계 가드'] += 1
        elif lid in HINT and TREQ.get(k['technique']) and tech_ok(HINT[lid], TREQ[k['technique']], [k['sub_family']]):
            SUB_EV['장비 속성'] += 1
        else:
            SUB_EV['매질만(근거 없음)'] += 1
SUB_EV['매질만(근거 없음)'] += 0
# 클리닉에서 쓰는 장비 → 시술은 전부 단위 시술(10-29) — 추천 가능 제품이 단위 시술 0 이면 예외 결정(원장 행 원천 질문) 있어야(v2 F1)
for x in product_links:
    if x['recommendable'] and not x['stored_units'] and not x['inherited_candidates'] and x['family'] not in (None, '계열 밖') \
            and not (LED.get(x['product']) or {}).get('origin_question'):
        op('추천 가능 제품인데 단위 시술 0 · 예외 결정 없음', product=x['product'], name=x['name'])
# 장비 · 제품 이름 = 동의어(저장 uses_product)
device_syn = []
for lid, ids in sorted(stored_by_p.items()):
    ids = sorted(set(ids))
    for i in ids:
        UNITS[i]['synonyms'].append(dict(text=pname(lid), type='장비 · 제품 이름(저장 uses_product)' + (' · 모호' if len(ids) > 1 else ''), src=lid))
    device_syn.append(dict(product=lid, name=pname(lid), units=ids, ambiguous=len(ids) > 1))

# ───────── 7. 수액 경로(F5) ─────────
RR = DEC['route_rule']
rx = re.compile(RR['explicit'])
for i, u in UNITS.items():
    if u['key']['family'] != RR['family']:
        continue
    txt = ' '.join(f"{s['name']} {s.get('detail') or ''}" for s in u['sources'])
    u['route_status'] = RR['explicit_status'] if rx.search(txt) else RR['default_status']

# ───────── 8. extracted ─────────
EN = DEC['extracted_rule']['key_normalize']


def flat(e, pre=''):
    out = {}
    for k, v in (e or {}).items():
        kk = f'{pre}{k}'
        if isinstance(v, dict):
            out.update(flat(v, kk + '.'))
        else:
            out[EN.get(kk, kk)] = v
    return out


# J(품질 10-30) — 안전 · 사후관리 원문을 붙는 수준(위 attach)에 그대로 싣는다(키만 두지 않음). 원문 그대로 · 고치지 않음
SAFETY_KEYS = ('safety', 'aftercare')


def safety_text(e):
    return {k: v for k, v in sorted(flat(e).items()) if k.split('.')[0] in SAFETY_KEYS and v} or None


LROW = {r['id']: r for r in ledger_rows}
extracted = []
for fam, sub, it in SRC_LED:
    if not it.get('extracted'):
        continue
    r = LROW[it['id']]
    keys = sorted(flat(it['extracted']))
    if r.get('dest') in ('제품', '제품 + 단위 시술') and r.get('product'):
        pf = PF.get(r['product'], {})
        ks = pf.get('sub_family') if pf.get('family') in KEY_SUB_FAMS else None
        att = dict(attach='제품 × 계열' + (' × 키 하위' if ks else ''), product=r['product'], family=pf.get('family'), sub_family=ks,
                   shown_on=sorted(set(stored_by_p.get(r['product'], [])) | set(r.get('units') or [])))
    elif r.get('units'):
        att = dict(attach='단위 시술' + (' 후보' if r.get('role') == '후보' else ''), units=r['units'])
    else:
        att = dict(attach=f"원문 보관({r.get('dest')})")
    extracted.append(dict(id=it['id'], name=it['name'], keys=keys, **att, source_text=safety_text(it['extracted'])))
tax_products = []
TP = {t: lid for lid, p in PROD.items() for t in (p.get('taxonomy_product_ids') or [])}
TPO = {x['id']: x for x in DEC.get('taxonomy_products') or []}
for m in TAX['modality']:
    for p in m.get('products') or []:
        lid = TP.get(p['id'])
        if lid is None:
            o = TPO.get(p['id'])
            if o is None:
                op('taxonomy 제품이 1단계 행 없음', id=p['id'], name=p.get('name'))
                continue
            ids = units_ok(o['units'], p['id'])
            tax_products.append(dict(id=p['id'], name=p.get('name'), product=None, attach=o['attach'], units=ids, basis=o['basis'], decided_by=o['decided_by'],
                                     keys=sorted(flat(p.get('extracted'))), source_text=safety_text(p.get('extracted'))))
            continue
        tax_products.append(dict(id=p['id'], name=p.get('name'), product=lid, attach='제품 × 계열(taxonomy products extracted)', keys=sorted(flat(p.get('extracted'))), source_text=safety_text(p.get('extracted'))))
STALE += [['taxonomy_products', k] for k in TPO if k not in {p['id'] for m in TAX['modality'] for p in m.get('products') or []} or k in TP]

# 부작용 덮어쓰기 값(골드 빈틈 ① · step5-decisions side_effect_override_rule · 사용자 10-30) — extracted 안전 원문을 붙는 수준(제품 링크 · 단위 시술)에 그대로
SEO = DEC['side_effect_override_rule']
PL_BY = {x['product']: x for x in product_links}
S1ALL = PROD  # 1단계 원장 전부(비활성 포함 · merged_into)
SEO_LOG = collections.Counter()
for src_kind, rows_ in (('taxonomy 항목 extracted', extracted), ('taxonomy products extracted', tax_products)):
    for r in rows_:
        vals = {k[len('safety.'):]: v for k, v in (r.get('source_text') or {}).items() if k.startswith('safety.')}
        if not vals:
            continue
        lvl = r['attach']
        base = dict(source=src_kind, id=r['id'], name=r.get('name'), level=lvl, values=vals)
        if r.get('product') and r['product'] not in PL_BY:
            base['via_merged'] = r['product']
        tgt = r.get('product')
        while tgt and tgt not in PL_BY and (S1ALL.get(tgt) or {}).get('merged_into'):  # 1단계 합침 결정(merged_into)을 따라 활성 제품으로
            tgt = S1ALL[tgt]['merged_into']
        if lvl.startswith('제품 × 계열') and tgt in PL_BY:
            pl = PL_BY[tgt]
            fam_ = r.get('family') or pl['family']
            pl.setdefault('side_effect_override', []).append(dict(base, sub_family=r.get('sub_family'), override_of=f'family:{fam_}' if fam_ else None,
                                                                   priority=SEO['priority'].index('제품 × 계열 × 키 하위' if r.get('sub_family') else '제품 × 계열')))
            SEO_LOG[lvl] += 1
        elif lvl.startswith('단위 시술') and r.get('units'):
            for uid in r['units']:
                u_ = UNITS[uid]
                u_.setdefault('side_effect_override', []).append(dict(base, override_of=f"family:{u_['key']['family']}" if u_['key']['family'] else None,
                                                                      priority=SEO['priority'].index('단위 시술 후보' if '후보' in lvl else '단위 시술')))
            SEO_LOG[lvl] += 1
        elif lvl.startswith('제품 × 계열'):
            op('부작용 덮어쓰기 값 붙는 제품 링크 없음', id=r['id'], product=r.get('product'))
        else:
            SEO_LOG['안 실음(' + lvl + ')'] += 1

# ───────── 9. PIH ─────────
PD = {d['index']: d for d in DEC['pih']}
pih_rows = []
for idx, p in enumerate(PIH['procedures']):
    d = PD.get(idx)
    if d is None or d['name'] != p['name']:
        op('결정 없는 PIH 행', index=idx, name=p['name'])
        continue
    t = d['target']
    if d['attach'] == 'unit':
        ids = [i for i, u in UNITS.items() if all(u['key'].get(k) == v for k, v in t.items())]
    elif d['attach'] in ('family_sub', 'family'):
        ids = [i for i, u in UNITS.items() if all(u['key'].get(k) == v for k, v in t.items())]
    elif d['attach'] == 'product':
        pl = next((x for x in product_links if x['product'] == t['product']), None)
        ids = pl['stored_units'] if pl else []  # 제품 층 — 제품에 붙고, 단위 시술에는 저장 uses_product 로만 보임(S10)
        if pl is None:
            op('PIH 제품이 1단계 active 아님', index=idx, product=t['product'])
        else:
            pl.setdefault('pih', []).append(dict(pih_risk=p.get('pih_risk'), pih_rate=p.get('pih_rate'), condition=d['condition'], source=p['name']))
    else:
        ids = []
        op('PIH 붙는 단위 값 밖', index=idx, attach=d['attach'])
    v = dict(pih_risk=p.get('pih_risk'), pih_rate=p.get('pih_rate'), fitzpatrick_note=p.get('fitzpatrick_note'), condition=d['condition'], source=p['name'],
             attach=d['attach'], target=t)
    for i in sorted(ids):
        UNITS[i].setdefault('pih', []).append(v)
    pih_rows.append(dict(index=idx, name=p['name'], ref=p.get('procedure_ref'), pih_risk=p.get('pih_risk'), pih_rate=p.get('pih_rate'), attach=d['attach'], target=t, condition=d['condition'], units=sorted(ids)))
NA = {f: k for k, fs in DEC['pih_not_applicable'].items() if k != 'decided_by' for f in fs}
for k in NA.values():
    if k not in PIH['notes']:
        op('PIH 해당 없음 원천 칸 없음', note=k)
pih_na, pih_gap = [], []
for i, u in UNITS.items():
    if u.get('pih'):
        continue
    f = u['key']['family']
    if f in NA:
        u['pih_not_applicable'] = dict(note=NA[f], text=PIH['notes'].get(NA[f]))
        pih_na.append(i)
    else:
        via = sorted({x['name'] for x in product_links if x.get('pih') and i in x['inherited_candidates']})
        u['pih_gap'] = '원천 없음(값 없음 표시 · 추정 안 함)' + (f" — 제품 층 PIH 는 쓰는 제품에서: {' · '.join(via)}" if via else '')
        pih_gap.append(i)

# ───────── 10. 운영 정보 ─────────
AN = DEC['anesthesia_dict']
PROFILE = {p['id']: p for p in PROF}
ops_gap = collections.Counter()
for i, u in UNITS.items():
    p = PROFILE.get(u['key']['family'])
    if p is None:
        u['ops'] = None
        ops_gap[u['key']['family']] += 1
        continue
    if p.get('needsAnesthesia') not in AN:
        op('마취 값 사전 밖', family=u['key']['family'], value=p.get('needsAnesthesia'))
    u['ops'] = dict(inherit=f"계열 {u['key']['family']} 운영 속성(procedure-profiles)", needsAnesthesia=p.get('needsAnesthesia'), anesthesia_ko=AN.get(p.get('needsAnesthesia')),
                    position=p.get('position'), needsCleansing=p.get('needsCleansing'), prepTime=p.get('prepTime'), durationMin=p.get('durationMin'), durationMax=p.get('durationMax'),
                    prepNotes=p.get('prepNotes'))

# ───────── 11. 4단계 속성 · 위험 부위 용량 ─────────


def rule_units(r):
    out = []
    for i, u in UNITS.items():
        k = u['key']
        if k['family'] not in r['families']:
            continue
        if 'technique' in r and k['technique'] != r['technique']:
            continue
        if 'sites' in r and k['site'] not in r['sites']:
            continue
        if 'site_or_children' in r and k['site'] not in site_children(r['site_or_children']):
            continue
        out.append(i)
    return sorted(out)


AD = DEC['step4_attrs']
UPA = S4['unit_procedure_attrs']
attr_rows = []
src_attrs = [('safe_layers', x['site'], x) for x in UPA['safe_layers']] + [('target_muscles', x['key'], x) for x in UPA['target_muscles']] + \
            [('landmarks', x['site'], x) for x in UPA['landmarks']]
dmap = {(d['attr'], d.get('site') or d.get('muscle')): d for d in AD if d['attr'] in ('safe_layers', 'target_muscles', 'landmarks')}
for attr, key, x in src_attrs:
    d = dmap.get((attr, key))
    if d is None:
        op('결정 없는 4단계 속성', attr=attr, key=key)
        continue
    ids = rule_units(d['rule'])
    val = x.get('layers') if attr == 'safe_layers' else (x.get('ko_kma') if attr == 'target_muscles' else x.get('text'))
    for i in ids:
        UNITS[i].setdefault('step4_attrs', {}).setdefault(attr, []).append(dict(key=key, value=val, constraint=x.get('constraint_text')))
    attr_rows.append(dict(attr=attr, key=key, value=val, constraint=x.get('constraint_text'), units=ids,
                          dest=None if ids else '8단계 site_caution 원문(붙을 단위 시술 없음)', decided_by=d['decided_by']))
STALE += [['step4_attrs', list(k)] for k in dmap if k not in {(a, k_) for a, k_, _ in src_attrs}]
for d in AD:
    if d['attr'] not in ('tool_form', 'peel_depth'):
        continue
    if d['attr'] not in S4['dictionaries']:
        op('4단계 사전 칸 없음', attr=d['attr'])
        continue
    ids = rule_units(d['rule'])
    for i in ids:
        UNITS[i].setdefault('step4_attrs', {}).setdefault(d['attr'], []).append(dict(key=d['attr'], value=d['value']))
    attr_rows.append(dict(attr=d['attr'], key=d['attr'], value=d['value'], constraint=None, units=ids, dest=None if ids else '8단계', decided_by=d['decided_by']))
DZ = {d['zone']: d for d in DEC['dose_range']}
dose_rows = []
for z in ZONES:
    dr = (z.get('botox_specific') or {}).get('dose_range')
    if not dr:
        continue
    d = DZ.get(z['id'])
    if d is None:
        op('결정 없는 위험 부위 용량', zone=z['id'])
        continue
    ids = rule_units(dict(d['rule'], sites=d['sites']))
    have = {UNITS[i]['key']['site'] for i in ids}
    for i in ids:
        UNITS[i].setdefault('dose_range_text', []).append(dict(zone=z['id'], text=dr))
    dose_rows.append(dict(zone=z['id'], dose_range_text=dr, sites=d['sites'], units=ids, no_unit_sites=[s for s in d['sites'] if s not in have]))
STALE += [['dose_range', k] for k in DZ if k not in {z['id'] for z in ZONES if (z.get('botox_specific') or {}).get('dose_range')}]

# ───────── 12. 셈 ─────────
for u in UNITS.values():
    u['purposes'] = sorted(set(u['purposes']))
    seen_s, syn = set(), []
    for s in u['synonyms']:
        if s['text'] not in seen_s:
            seen_s.add(s['text']); syn.append(s)
    u['synonyms'] = syn
    u['candidate_of'] = sorted(set(u['candidate_of']))
SYN_UNITS = collections.defaultdict(set)
for i, u in UNITS.items():
    for x in u['synonyms']:
        SYN_UNITS[x['text']].add(i)
synonym_multi_unit = {t: sorted(v) for t, v in sorted(SYN_UNITS.items()) if len(v) > 1}
for u in UNITS.values():
    for x in u['synonyms']:
        if x['text'] in synonym_multi_unit:
            x['ambiguous'] = True
# 결정으로 모호 표시(검수 W3) — 7단계 원천 이름이 질환 · 고민 이름인 동의어(키 하나여도)
AMB7 = {(d['id'], d['name']): d['ambiguous_reason'] for d in DEC.get('step7_names') or [] if d.get('ambiguous')}
for u in UNITS.values():
    for x in u['synonyms']:
        if x['type'] == '7단계 원천 이름' and (x['src'], x['text']) in AMB7:
            x['ambiguous'] = True
            x['ambiguous_reason'] = AMB7[(x['src'], x['text'])]
LDEST = collections.Counter(r['dest'] for r in ledger_rows)
PROC_DEST = ('단위 시술', '제품 + 단위 시술', '다른 단계 이름')
NOT_PROC = ('시술 아님', '값', '시술 아님(다른 단계)')
proc_rows = [r for r in ledger_rows if r['dest'] in PROC_DEST]
proc_no_unit = [r for r in proc_rows if not r.get('units')]
for r in proc_no_unit:
    op('시술인데 단위 시술 없음', id=r['id'], name=r['name'])
count_521 = dict(
    total=len(ledger_rows),
    products=sum(1 for r in ledger_rows if r['dest'] == '제품'),
    procedures=len(proc_rows), procedures_with_unit=len(proc_rows) - len(proc_no_unit),
    procedures_by_dest={k: LDEST[k] for k in PROC_DEST},
    procedures_candidate=sum(1 for r in proc_rows if r.get('role') == '후보'),
    package_6=LDEST['6단계 패키지'],
    not_procedure={k: LDEST[k] for k in NOT_PROC},
    pending_director=LDEST['원장님 문의'],
    no_decision=LDEST[None],
)
count_521['check'] = sum([count_521['products'], count_521['procedures'], count_521['package_6'], sum(count_521['not_procedure'].values()),
                          count_521['pending_director'], count_521['no_decision']]) == count_521['total']
by_family = collections.Counter(u['key']['family'] for u in UNITS.values())
summary = dict(
    source=str(SRC), units=len(UNITS), units_by_family=dict(sorted(by_family.items(), key=lambda kv: (kv[0][0], int(kv[0][1:])))),
    ledger_521=count_521, ledger_by_dest=dict(LDEST.most_common()),
    problem_P1=len(p1_rows), market=dict(total=len(market_rows), by_kind=dict(collections.Counter(r['kind'] for r in market_rows))),
    step1_market_copies=len(copies),
    uses_product_stored=sum(len(u['uses_product']) for u in UNITS.values()), products_with_stored=len(stored_by_p),
    product_links=dict(collections.Counter(x['link'] for x in product_links)),
    extracted=dict(collections.Counter(x['attach'] for x in extracted)), taxonomy_products=len(tax_products),
    side_effect_override=dict(rows=dict(sorted(SEO_LOG.items())), product_links=sum(len(x.get('side_effect_override') or []) for x in product_links),
                              units=sum(len(u.get('side_effect_override') or []) for u in UNITS.values()), rule=SEO['rule']),
    pih=dict(rows=len(pih_rows), units_with_pih=sum(1 for u in UNITS.values() if u.get('pih')), not_applicable=len(pih_na), gap=len(pih_gap)),
    ops=dict(families=len(PROFILE), units_inherit=sum(1 for u in UNITS.values() if u['ops']), gap_by_family=dict(ops_gap)),
    step4_attrs=dict(rows=len(attr_rows), linked=sum(1 for r in attr_rows if r['units']), to_stage8=sum(1 for r in attr_rows if not r['units'])),
    dose_range=dict(zones=len(dose_rows), unit_links=sum(len(r['units']) for r in dose_rows), no_unit_sites=sorted({s for r in dose_rows for s in r['no_unit_sites']})),
    handoffs={k: len(v) for k, v in handoff_rows.items()},
    device_name_synonyms=len(device_syn), synonym_multi_unit=len(synonym_multi_unit),
    open=len(OPEN), open_by_type=dict(collections.Counter(o['type'] for o in OPEN)), stale_decisions=len(STALE),
)

# 원천 질문
OQ = []
for r in ledger_rows:
    if r.get('origin_question'):
        OQ.append(dict(kind='원장 항목', id=r['id'], name=r['name'], question=r['origin_question'], now=', '.join(f"{i} {UNITS[i]['name']}" for i in r.get('units') or []),
                       evidence_level=r.get('evidence_level'), source_fix=r.get('source_fix')))
for r in market_rows:
    if r.get('origin_question'):
        OQ.append(dict(kind='시장가', id=r['name'], name=r['name'], question=r['origin_question'], now=', '.join(f"{i} {UNITS[i]['name']}" for i in r['units'])))
for r in handoff_rows['7단계 → 5단계(J7)']:  # J7 G10 — 7단계 원천 이름의 원천 질문
    if r.get('origin_question'):
        OQ.append(dict(kind='7단계 원천 이름', id=f"{r['source']} {r['id']}", name=r['name'], question=r['origin_question'], now=', '.join(f"{i} {UNITS[i]['name']}" for i in r['units']) + (' · 후보' if r['role'] == '후보' else '')))
EMODE = [r for r in market_rows if (r.get('grade') or '').startswith('이모드')]
if EMODE:
    OQ.append(dict(kind='시장가', id=' · '.join(r['name'] for r in EMODE), name='이모드', question='「이모드」는 어떤 장비인가요? 「인모드 바디」와 같은 것인가요? (MFDS 이모드 · E-MOD 0 · 원천이 인모드를 M9 다른 행으로 따로 가짐)',
                   now=', '.join(sorted({f"{i} {UNITS[i]['name']}" for r in EMODE for i in r['units']}))))
SQ = [dict(kind='시장가', id=r['name'], name=r['name'], question=r['staff_question'], now=r.get('to') or r['kind']) for r in market_rows if r.get('staff_question')]
summary['origin_questions'] = len(OQ)
summary['staff_questions'] = len(SQ)

J_OUT = dict(
    version='step5-units v1', generated_by='step5-apply.py', decision_ref=DEC['decision_ref'],
    inputs=['step5-decisions.json', str(SRC) + ' (taxonomy · market-pricing · pih-risk · procedure-profiles · anatomy-danger-zones)', 'step1-products.json', 'step2-families.json',
            'step3-sites.json', 'step4-techniques.json', 'source-map.json 5단계 칸'],
    rules=dict(key=DEC['key_rule'], special_sites=SPECIAL, name=DEC['name_rules'], product_link=PLR, extracted=DEC['extracted_rule'], market=DEC['market_rule'], route=RR,
               pih_not_applicable=DEC['pih_not_applicable'], anesthesia=AN, not_this_stage=DEC['not_this_stage']),
    summary=summary,
    units=[dict(id=i, **{k: v for k, v in u.items() if k != 'id'}) for i, u in UNITS.items()],
    ledger=ledger_rows, problem_P1=p1_rows, market=market_rows, step1_market_copies=copies,
    product_links=product_links, device_name_synonyms=device_syn, synonym_multi_unit=synonym_multi_unit, extracted=extracted, taxonomy_products=tax_products,
    pih=pih_rows, pih_not_applicable_units=pih_na, pih_gap_units=pih_gap, step4_attrs=attr_rows, dose_range=dose_rows,
    handoffs=handoff_rows, origin_questions=OQ, staff_questions=SQ, open=OPEN, stale_decisions=STALE,
)
json.dump(J_OUT, open(OUT / 'step5-units.json', 'w'), ensure_ascii=False, indent=1)
open(OUT / 'step5-units.json', 'a').write('\n')

# ───────── 13. md ─────────
L = []
P = L.append
esc = lambda x: str(x if x is not None else '').replace('|', '／').replace('\n', ' ')
FN = {f['id']: f['name'] for f in S2['families']}
TN = {n['id']: n['name'] for n in S4['nodes']}


def kfmt(k):
    s = FN.get(k['family'], k['family'])
    if k.get('sub_family'):
        s += f" · {k['sub_family']}"
    if k.get('ingredient'):
        s += f" · 성분 {k['ingredient']}" + (f"({k['ingredient_of']})" if k.get('ingredient_of') else '')
    return f"{k['family']} {s} × {k['site']} × {k['technique']} {TN.get(k['technique'], '')}"


c = count_521
P('---\ntype: silver\nid: step5-units\ntitle: "실버 5단계 — 단위 시술 원장"\nproduct: procedure-hub\nfeature: phub-recommend\n'
  f"decision: \"{DEC['decision_ref']}\"\ngenerated_by: step5-apply.py\ndata: step5-units.json\n---\n")
P('# 실버 5단계 — 단위 시술 원장\n')
P(f"> 결정 `step5-decisions.json` · 재현 `python3 step5-apply.py` · 고정 시험 `python3 step5-fixture-test.py`. 원천에 새 원장 항목 · 시장가 · 메뉴 · PIH 행이 오거나 앞 단계가 5단계로 새로 넘기면 「결정 없는 …」 open 이 난다 — 결정 한 줄로 닫힌다.\n")
P('## 원장 521 셈 — 시술인 것은 전부 단위 시술\n')
P('| 무엇 | 행 | 단위 시술 |')
P('|---|---|---|')
P(f"| **원장 항목** | **{c['total']}** | |")
P(f"| 시술 — 단위 시술 키가 있음 | **{c['procedures']}** | **{c['procedures_with_unit']} / {c['procedures']}** (이름 {c['procedures'] - c['procedures_candidate']} · 후보 동의어 {c['procedures_candidate']}) |")
for k, v in c['procedures_by_dest'].items():
    P(f"| ㄴ {k} | {v} | |")
P(f"| 제품(1단계 제품 행 — 단위 시술에 「쓰는 제품」으로 붙음) | {c['products']} | §4 |")
P(f"| 6단계 패키지(병원 메뉴 묶음 — 구성 단위 시술은 6단계) | {c['package_6']} | |")
P(f"| 원장님 문의(2단계 그대로 · 답 오면 그 행만) | {c['pending_director']} | |")
for k, v in c['not_procedure'].items():
    lab = {'시술 아님': '시술 아님 — 처방약(아큐탄)', '값': '시술 아님 — 성분 값(M15 외용제 성분 · 사후관리 권장 제품 · F9)', '시술 아님(다른 단계)': '시술 아님 — 8단계 확인 조건 약물(이소트레티노인 · 스피로노락톤)'}[k]
    P(f"| {lab} | {v} | |")
P(f"| 결정 없음 | {c['no_decision']} | |")
P(f"\n셈 맞음: {'예' if c['check'] else '**아니오**'} · 시술인데 단위 시술 없음 **{len(proc_no_unit)}** · open **{len(OPEN)}** · 낡은 결정 **{len(STALE)}**\n")
REC0 = [x for x in product_links if x['recommendable'] and not x['stored_units'] and not x['inherited_candidates']]
REC0_DIAG = [x for x in REC0 if x['family'] == '계열 밖']
PEV_U = collections.Counter(i for x in product_links for i in x['inherited_candidates'] if i in PEV.get(x['product'], ()))
P(f"제품 출처로 이은 목적 키(코디 10-29 추가 · `technique_compat.product_evidence` · 문구 · 필드 기록) — 제품 {len(PEV)} · 쌍 {sum(PEV_U.values())}: " + ' · '.join(f"{i} {UNITS[i]['name']} {n}" for i, n in sorted(PEV_U.items())) +
  f" · 출처 문구가 있어도 뺀 것 {len(TC.get('product_evidence_excluded') or [])}: " + ' · '.join(f"{x['name']}({x['reason'].split(' — ')[-1]})" for x in TC.get('product_evidence_excluded') or []) + '\n')
P(f"상속 후보 **{sum(len(x['inherited_candidates']) for x in product_links)}쌍**(v2 검수 1203 → F1 하위 키 20쌍 빠짐 · 제품 출처 목적 키 더함 — step5-fix4) · 하위 키 중 매질이 기법을 못 정하는 키(알렉산드라이트 · 탄산가스 · Er:YAG · M5 엑소좀)에 이어진 쌍 "
  f"{sum(v for k, v in SUB_EV.items() if k != '매질만(근거 없음)')} = " + ' · '.join(f"{k} {v}" for k, v in SUB_EV.items() if k != '매질만(근거 없음)') + f" · **기법 근거 없는 쌍 {SUB_EV['매질만(근거 없음)']}**\n")
REC0_OQ = [x for x in REC0 if x['family'] != '계열 밖']
P(f"추천 가능 제품 {sum(1 for x in product_links if x['recommendable'])} 중 이어지는 단위 시술 0 = **{len(REC0)}** — 진단 장비(계열 밖) {len(REC0_DIAG)}: " + (' · '.join(x['name'] for x in REC0_DIAG) or '없음') +
  (f" · **예외(원천 질문 · 출처로 시술 방식 안 닫힘) {len(REC0_OQ)}: " + ' · '.join(x['name'] for x in REC0_OQ) + '**' if REC0_OQ else ' — 진단 장비만') + '\n')
s = summary
P(f"단위 시술 키 **{s['units']}** — " + ' · '.join(f"{k} {v}" for k, v in s['units_by_family'].items()))
P(f"\n시장가 {s['market']['total']}(" + ' · '.join(f"{k} {v}" for k, v in s['market']['by_kind'].items()) + f") · 쁘띠시술 메뉴 {s['problem_P1']} · 저장 uses_product {s['uses_product_stored']}(제품 {s['products_with_stored']}) · "
  f"PIH {s['pih']['rows']}행(붙은 키 {s['pih']['units_with_pih']} · 해당 없음 {s['pih']['not_applicable']} · 원천 없음 {s['pih']['gap']}) · 운영 상속 {s['ops']['units_inherit']}(원천 없음 " + ' · '.join(f"{k} {v}" for k, v in s['ops']['gap_by_family'].items()) + ')'
  f" · 4단계 속성 {s['step4_attrs']['rows']}(붙음 {s['step4_attrs']['linked']} · 8단계로 {s['step4_attrs']['to_stage8']}) · 원천 질문 {s['origin_questions']}\n")
if OPEN:
    P('## open\n')
    for o in OPEN:
        P(f"- {esc(json.dumps(o, ensure_ascii=False))}")
    P('')
if STALE:
    P('## 낡은 결정\n')
    for x in STALE:
        P(f"- {esc(x)}")
    P('')
P('## 10-29 결정 반영 — 바뀐 것\n')
P('| 결정 | 무엇 | 반영 |')
P('|---|---|---|')
for dk, what, how in [
    ('J1 안 C', '키 = 계열 × [하위 · 성분] × 부위 × 기법', 'M5 · M8 · M9 · M13 하위 · M16 성분만 키 — 재질 · 성분 차이는 제품 속성'),
    ('J2', '부위 이름 없는 얼굴 계열 = 얼굴 전체', 'site_basis 「기본값」 표시'),
    ('F1 · U1', '카복시 · 반영구 화장 = 단위 시술', 'N2 바디 카복시테라피(보정 · 기본값) · N3 반영구 4(눈썹 · 눈꺼풀 · 입술 · 두피 × K13)'),
    ('F2 · U1 · U4', '소수술 4 = 단위 시술', 'N4 × 얼굴 전체 × K12a · K12b · K12c + N4 × 병변 단위 × K01(스테로이드 병변 내 주사)'),
    ('F3', '병변 단위 시장가 3', '특수 부위 「병변 단위」 — M8 병변 레이저 · M13 병변 플라즈마'),
    ('F4 · research2', '사파이어 · 에이팩 · MPE · 이모드 · 수소토닝', '사파이어 → 얼굴 전체 레이저 · 에이팩 → 얼굴 전체 MTS(근거 약) · MPE → 얼굴 전체 줄기세포(근거 약) · 이모드 → 복부 · 힙 EMS(등급 「이모드(미확인)」) · 수소토닝 → 얼굴 전체 박리 관리(장비 듀오 하이드로젠 저장 uses_product · U8) — 전부 원천 질문'),
    ('U9', '파셀라 메디컬 경락', 'M9 RF × 얼굴 전체 × K05(얼굴 전체 고주파 리프팅) 동의어 + 1단계 새 행 「파셀라」 저장 uses_product'),
    ('F5', '근거 약 4 · 수액 경로', 'CPR · ACR → 얼굴 전체 PRP · SVF → 얼굴 전체 지방이식 + 「SVF 보강」 · 셀룰라이트 → 허벅지 지방분해주사(근거 약 + 질문) · M16 route_status'),
    ('F6', '부위 없는 몸 · 지방분해 메뉴', '후보 동의어 — V라인 · 다빼 · 아큐 = N1 얼굴 쪽 5 · 팻킬 · GPC · PPC = N1 전부 · 쿨미니 = M14 5 · 이모드 4회 = 복부 · 힙 회차 4'),
    ('F7', 'HP주사 · 크라이오셀', '감초 수액(+ 원천 수정 후보) · 얼굴 전체 냉각 진정 관리'),
    ('F8 · U1', '태반 2 · 성장호르몬 · 헤어셀', 'N5 태반주사(라이넥 · 멜스몬 저장) · N6 성장호르몬주사(U5 — 소마트로핀 1단계 행 없음) · N7 두피 전자기장 치료(헤어셀 저장)'),
    ('F9', '버림 17', 'M15 외용제 성분 값 · 사후관리 권장 제품(버림 0)'),
    ('U7', '성분 미상 수액 4', 'M16 × 해당 없음 × 정맥 · 성분 「미상」 키 4(원천 이름으로 가름) + 원천 질문'),
    ('보정 프로락틴', '프로락틴주사', 'M4 × 두피 × 주입 = 두피 스킨부스터 동의어 · 성분 미상 + 원천 질문'),
    ('10-29 원칙', '루비레이저 · KTP레이저(원장 항목)', 'M8 루비 · KTP × 얼굴 전체 × K04 키 2 — 같은 매질 키가 없어 세움(J1 안 C · J2 · S4)'),
    ('검수 F1', '제품 → 단위 시술 상속에 기법 호환', f"상속 후보 {sum(len(x['inherited_candidates']) for x in product_links)}쌍 · 기법으로 뺀 것 {sum(len(x['technique_excluded']) for x in product_links)}쌍(제품 {sum(1 for x in product_links if x['technique_excluded'])}) — 매질 미지정 키는 장비 속성(펄스 · 가능 방식) 근거 있는 제품만 · 하위 있는 키는 매질 일치 + 장비 속성 어긋나면 뺌 · 계열 기법 하나(M9 · M13)는 계열 기본이 근거 · PIH 「제품 층 PIH 는 쓰는 제품에서」 재생성(§4-1)"),
    ('검수 W1', '온다 · 소프웨이브 쓸 단위 시술', 'M9 마이크로웨이브 · SUPERB 초음파 × 얼굴 전체 × K05 키 2(U5-139 · U5-140 · 부위 기본값) · 원장 장비 행 = 제품 + 단위 시술 · 쓰는 제품 = 그 장비(저장 uses_product)'),
    ('검수 W2', '「진정관리 (시술 후 재생팩)」', 'U5-034 얼굴 전체 필링의 후보 동의어로 낮춤(이름 그대로)'),
    ('F1 확장(step5-fix3)', '기법 갈리는 계열 전부(M4 · M5 · M15 · M17 · N4)', '계열 근거(§4-1 family_evidence) — M15 하위 계열 → K09 · K11 · K10 · M4 성분 하위 = K01a · 주입 기기(장비) = K01c · M5 · M17 화장품 = K09 · M17 의약품 = K01 · 노바스템 = K01(병원 페이지 「주입」 출처) · 근거 없으면 상속 안 함'),
    ('재검수 v2 F1(step5-fix4)', '하위 키 안 기법 근거 · M5 확인 불가 · 단위 시술 0 이 된 추천 제품', '매질의 키 기법이 갈리거나(상하위 아님) 조건(K04b 프락셔널 · 사전 일부 K04a 펄스)이 있으면 매질 일치는 근거 아님 — 장비 속성 · 계열 근거 · 가드 · 제품 출처가 채울 때만(엔디야그 = 매질로 충분). 빠진 20쌍 = 젠틀맥스 프로 플러스 · 젠틀맥스 프로 · 젠틀레이즈 · 스플렌더 X → U5-024 · U5-026 / 스마트사이드 → U5-028 · SP 다이나미스 · 포토나스타발브 → U5-029 / 셀엑소좀 · 카탈리스트 · 드원셀 → U5-019 · U5-040 · U5-142. 제품 출처(1단계 detail · evidence · 원장 행 · taxonomy products 문구)가 목적을 채우면 0 이 아니어도 잇기(코디 추가) — 「제모 · 체모」 → 겨드랑이 · 전신 레이저 제모(U5-100 · U5-101) · 「문신 · 점 제거」 → 병변 레이저(U5-131) · 리팟(제모 표기 오기) · 슬렌더엑스(확인 불가) 뺌 · 셀엑소좀 · 카탈리스트 · 드원셀 · 스마트사이드 = 예외 + 원천 질문(출처로 방식 안 닫힘) · 추천 가능 제품이 단위 시술 0 인데 예외 결정이 없으면 open'),
    ('step5-fix3', '단위 시술 없는 추천 제품', 'U5-141 얼굴 전체 PDL 레이저(브이빔 · 브이빔 퍼펙타 · 목적 혈관 = 7단계) · U5-142 얼굴 전체 엑소좀 도포(ASCE+엑소좀 · U5 가드) · U5-143 얼굴 전체 줄기세포 도포(AAPE · 코디 답 ①) — 원장 제품 행 = 제품 + 단위 시술 · 미라셀 = 예외 + 원천 질문(코디 답 ②)'),
]:
    P(f"| {dk} | {esc(what)} | {esc(how)} |")
P('')
P(f"## 1. 단위 시술 키 — {len(UNITS)}\n")
P('동의어 끝 * = 여러 키를 부르는 이름(모호 · §11)\n')
P('| id | 이름 | 키 | 부위 근거 | 동의어 | 후보로 부르는 이름 | 쓰는 제품(저장) | 결정 |')
P('|---|---|---|---|---|---|---|---|')
for i, u in UNITS.items():
    P(f"| {i} | **{esc(u['name'])}** | {esc(kfmt(u['key']))} | {esc(u['site_basis'])} | {esc(' · '.join(x['text'] + ('*' if x.get('ambiguous') else '') for x in u['synonyms']))} | {esc(' · '.join(u['candidate_of']))} | "
      f"{esc(' · '.join(x['name'] + ('' if x['recommendable'] else '(추천 제외)') for x in u['uses_product']))} | {esc(u['decided_by'])}{' · 근거 ' + u['evidence_level'] if u.get('evidence_level') else ''} |")
P('')
P('### 1-1. 붙는 것 — 키마다(시장가 시술 1회 · PIH · 운영 · 4단계 속성 · 경로 · 목적)\n')
P('| id | 이름 | 시장가 시술 1회 | PIH | 운영(계열 상속) | 4단계 속성 · 용량 | 수액 경로 | 7단계 목적 |')
P('|---|---|---|---|---|---|---|---|')
for i, u in UNITS.items():
    mk = ' · '.join(f"{m['name']} {m['price']['low']:,}~{m['price']['high']:,}" + (f"({m['grade']})" if m.get('grade') else '') + (f" ×{m['sessions']}회" if m.get('sessions') else '') + (' 후보' if m['role'] == '후보' else '')
                    for m in u.get('market', []) if m['price'].get('low') is not None)
    ph = ' / '.join(f"{p['pih_risk']} {p['pih_rate'] or ''}" + (f"({p['condition']})" if p['condition'] else '') for p in u.get('pih', [])) or \
        (f"해당 없음({u['pih_not_applicable']['note']})" if u.get('pih_not_applicable') else u.get('pih_gap', ''))
    o = u['ops']
    ops = f"마취 {o['anesthesia_ko']} · {o['durationMin']}~{o['durationMax']}분 · 준비 {o['prepTime']}분" if o else '원천 없음'
    at = ' · '.join(f"{a} " + '/'.join(str(x['value']) for x in v) for a, v in (u.get('step4_attrs') or {}).items())
    at += (' · 용량 ' + ' / '.join(x['text'] for x in u['dose_range_text'])) if u.get('dose_range_text') else ''
    at += (' · ' + ' · '.join(f"{a} {v}" for a, v in u['attrs'].items())) if u['attrs'] else ''
    P(f"| {i} | {esc(u['name'])} | {esc(mk)} | {esc(ph)} | {esc(ops)} | {esc(at)} | {esc(u['route_status'] or '')} | {esc(' · '.join(u['purposes']))} |")
P('')
P(f"## 2. 원장 521 행선지\n")
P('| 행선지 | 행 |')
P('|---|---|')
for k, v in LDEST.most_common():
    P(f"| {k} | {v} |")
P('')
P('### 2-1. 제품이 아닌 행\n')
P('| id | 이름 | detail | 행선지 | 단위 시술 | 결정 · 근거 |')
P('|---|---|---|---|---|---|')
for r in ledger_rows:
    if r['dest'] == '제품':
        continue
    us = ' · '.join(f"{i} {UNITS[i]['name']}" for i in r.get('units') or [])
    P(f"| `{r['id']}` | {esc(r['name'])} | {esc(r['detail'])} | {esc(r['dest'])}{' · 후보' if r.get('role') == '후보' and us else ''} | {esc(us or r.get('to'))} | {esc(r.get('decided_by'))} — {esc(r.get('basis'))} |")
P('')
P('### 2-2. 쁘띠시술 메뉴(문제 트리 P1)\n')
P('| id | 이름 | 행선지 | 단위 시술 | 결정 |')
P('|---|---|---|---|---|')
for r in p1_rows:
    P(f"| `{r['id']}` | {esc(r['name'])} | {esc(r['dest'])} | {esc(' · '.join(f'{i} ' + UNITS[i]['name'] for i in r['units']))} | {esc(r['decided_by'])} |")
P('')
P(f"## 3. 시장가 {len(market_rows)} → 시술 1회\n")
P('| 이름 | 종류 | 단위 시술 | 제품 | 등급 | 규격 | 하~상 | 결정 |')
P('|---|---|---|---|---|---|---|---|')
for r in market_rows:
    us = ' · '.join(f"{i} {UNITS[i]['name']}" for i in r['units'])
    P(f"| {esc(r['name'])} | {r['kind']}{' · 후보' if r['role'] == '후보' else ''} | {esc(us or r.get('to'))} | {esc(' · '.join(pname(p) for p in r['product']))} | {esc(r['grade'])} | {esc((r['spec'] or {}).get('raw'))}{' · ' + str(r['sessions']) + '회' if r['sessions'] else ''} | "
      f"{r['price']['low']:,}~{r['price']['high']:,} | {esc(r['decided_by'])} |")
P('')
P(f"1단계 제품 행 시장가 사본 {len(copies)} → 같은 이름 시장가 행의 행선지로 옮김(S9) — " + ' / '.join(
    f"{to} {len(xs)}: " + ' · '.join(f"{x['name']}「{x['source_item']}」" for x in xs)
    for to, xs in ((t, [x for x in copies if x['to'] == t]) for t in dict.fromkeys(x['to'] for x in copies))) + '\n')
P(f"## 4. 쓰는 제품 — 1단계 active {len(product_links)}\n")
P(' · '.join(f"{k} {v}" for k, v in s['product_links'].items()) + f" · 가드 {', '.join(sorted(GUARD))}(도포 K09 만)\n")
P('| 제품 | 계열 · 하위 | 저장 uses_product | 상속 후보 수 | 기법으로 뺀 수 | 연결 |')
P('|---|---|---|---|---|---|')
for x in product_links:
    P(f"| {esc(x['name'])}(`{x['product']}`){'' if x['recommendable'] else ' · 추천 제외'} | {x['family']} · {x['sub_family'] or '—'} | {esc(' · '.join(x['stored_units']))} | {len(x['inherited_candidates'])} | {len(x['technique_excluded']) or ''} | {x['link']} |")
P('')
P('### 4-1. 기법 호환(F1) — 매질 미지정 · 장비 속성 어긋남으로 뺀 상속\n')
P(f"규칙: {esc(TC['sub_null'])} / {esc(TC['sub_keyed'])} / {esc(TC['single_technique_family'])}\n")
P('| 기법 | 조건 | 근거 |')
P('|---|---|---|')
for r in TC['requires']:
    cond = ('펄스 ' + ' · '.join(r['pulse_mode_any']) + ''.join(f" (+ {m} {' · '.join(v)})" for m, v in (r.get('pulse_mode_by_medium') or {}).items())) if 'pulse_mode_any' in r else \
        ('가능 방식 ' + ' · '.join(r['modes_any'])) if 'modes_any' in r else '근거 없음 — 매질 미지정 키 상속 안 함'
    P(f"| {r['technique']} {TN.get(r['technique'], '')} | {esc(cond)} | {esc(r['basis'])} |")
P('')
EXU = collections.Counter(e['unit'] for x in product_links for e in x['technique_excluded'])
P('| 계열 | 근거(제품 → 기법) | 근거 문장 |')
P('|---|---|---|')
for e in TC['family_evidence']:
    ev = ' · '.join([f"하위 {k} → {'/'.join(v)}" for k, v in (e.get('sub_family_map') or {}).items()] + ([f"성분 하위 있음 → {'/'.join(e['sub_family_any'])}"] if e.get('sub_family_any') else []) +
                    [f"1단계 종류 「{k}」 → {'/'.join(v)}" for k, v in (e.get('kind_map') or {}).items()] + [f"{pname(k)} → {'/'.join(v['techniques'])}" for k, v in (e.get('product_map') or {}).items()]) or '근거 없음 — 상속 안 함'
    P(f"| {e['family']} | {esc(ev)} | {esc(e['basis'])}{'' if not e.get('product_map') else ' · ' + esc(' / '.join(v['basis'] for v in e['product_map'].values()))} |")
P('')
P('| 단위 시술 | 뺀 제품 수 | 남은 상속 후보(매질 일치 · 장비 속성 근거) |')
P('|---|---|---|')
for i, n in sorted(EXU.items()):
    keep = [x['name'] for x in product_links if i in x['inherited_candidates']]
    P(f"| {i} {esc(UNITS[i]['name'])} | {n} | {esc(' · '.join(keep)) or '없음'} |")
P('')
P(f"## 5. extracted 붙임 — 원장 {len(extracted)} · taxonomy 제품 {len(tax_products)}\n")
P(' · '.join(f"{k} {v}" for k, v in s['extracted'].items()) + ' · 키 정규화 ' + ' · '.join(f"{a} → {b}" for a, b in EN.items()) + ' · 적응증 = 7단계 근거만 · 부작용 = complications 결정론 일치만(8단계)\n')
P(f"## 6. PIH {len(pih_rows)}행\n")
P('| 원천 이름 | ref | 위험 | 발생률 | 붙는 단위 | 조건 | 단위 시술 |')
P('|---|---|---|---|---|---|---|')
for r in pih_rows:
    P(f"| {esc(r['name'])} | {r['ref']} | {r['pih_risk']} | {esc(r['pih_rate'])} | {r['attach']} {esc(json.dumps(r['target'], ensure_ascii=False))} | {esc(r['condition'])} | {esc(' · '.join(r['units']))} |")
P(f"\n해당 없음(원천 notes) 키 {len(pih_na)} · 원천 없음(값 없음 표시) 키 {len(pih_gap)}: " + ' · '.join(f"{i} {UNITS[i]['name']}" for i in pih_gap) + '\n')
P(f"## 7. 운영 정보 — 계열 {len(PROFILE)} 상속\n")
P('마취 값 사전: ' + ' · '.join(f"{k} = {v}" for k, v in AN.items()) + f" · 원천 없음 계열: " + ' · '.join(f"{k}({v}키)" for k, v in ops_gap.items()) + '\n')
P(f"## 8. 4단계 속성 {len(attr_rows)} · 위험 부위 용량 {len(dose_rows)}\n")
P('| 속성 | 부위 · 근육 | 값 | 단위 시술 | 행선지 |')
P('|---|---|---|---|---|')
for r in attr_rows:
    P(f"| {r['attr']} | {esc(r['key'])} | {esc(r['value'])} | {esc(' · '.join(r['units']))} | {esc(r['dest'] or '단위 시술 속성')} |")
P('')
P('| zone | 용량 원문 | 부위 | 단위 시술 | 단위 시술 없는 부위(8단계) |')
P('|---|---|---|---|---|')
for r in dose_rows:
    P(f"| {r['zone']} | {esc(r['dose_range_text'])} | {' · '.join(r['sites'])} | {' · '.join(r['units'])} | {' · '.join(r['no_unit_sites'])} |")
P('')
P('## 9. 넘겨받은 것\n')
for k, rows in handoff_rows.items():
    P(f"### {k} — {len(rows)}\n")
    for r in rows:
        if 'units' in r:
            P(f"- `{r['id']}` {esc(r['name'])} → {esc(' · '.join(f'{i} ' + UNITS[i]['name'] for i in r['units']))}{' (후보)' if r['role'] == '후보' else ''} — {esc(r['decided_by'])}")
        else:
            lab = r.get('item') or r.get('source') or r.get('string') or f"{r.get('file')} {r.get('path')}"
            P(f"- {esc(lab)} → {esc(r['to'])} — {esc(r['decided_by'])}")
    P('')
P(f"## 10. 원천 질문 {len(OQ)} · 의료진 질문 {len(SQ)} — `step5-origin-questions.md`\n")
P(f"## 11. 장비 · 제품 이름 동의어 {len(device_syn)}(저장 uses_product) · 여러 키를 부르는 동의어 {len(synonym_multi_unit)}(모호 — 조회 때 후보 전부)\n")
P(' · '.join(f"{x['name']} → {' · '.join(x['units'])}{' (모호)' if x['ambiguous'] else ''}" for x in device_syn) + '\n')
P(' · '.join(f"「{t}」 → {' · '.join(v)}" for t, v in synonym_multi_unit.items()) + '\n')
FX = W / 'step5-fixtures' / 'result.json'
if FX.exists() and OUT == W:
    fx = J(FX)
    P(f"## 12. 고정 시험 — {fx['passed']}/{fx['total']}\n")
    P('| 사례 | 입력 | 기대 open | 실제 | 결과 |')
    P('|---|---|---|---|---|')
    for x in fx['cases']:
        P(f"| {x['id']} | {esc(x['input'])} | {esc(' · '.join(x['expect']))} | {esc(' · '.join(x['actual']))} | {'PASS' if x['pass'] else 'FAIL'} |")
    P('')
open(OUT / 'step5-units.md', 'w').write('\n'.join(L) + '\n')

Q = ['# 5단계 원천(병원)에 물을 것 (2026-10-29)', '',
     '`step5-apply.py` 생성. 1 · 2단계 질문(`step1-origin-questions.md` · `step2-origin-questions.md`)은 건드리지 않음. 답이 오면 그 행만 다시 판정한다. 지금 값은 넣어 두었다(결정대로).', '',
     f'질문 {len(OQ)}', '']
for q in OQ:
    Q.append(f"- {q['question']} — `{q['id']}` · 지금: {q['now']}" + (f" · 근거 {q['evidence_level']}" if q.get('evidence_level') else '') + (f" · 원천 수정 후보: {q['source_fix']}" if q.get('source_fix') else ''))
if SQ:
    Q += ['', f'## 의료진 질문 {len(SQ)} — 시술 범위', '']
    for q in SQ:
        Q.append(f"- {q['question']} — `{q['id']}`({q['kind']}) · 지금: {q['now']}")
pdl = [p for p in S2.get('pending_director') or []]
if pdl:
    Q += ['', f'## 참고 — 2단계 원장님 문의 {len(pdl)}(5단계는 답 오기 전까지 단위 시술 없음)', '']
    for p in pdl:
        Q.append(f"- {p['question']} — `{p['ledger_id']}` {p['display_name']}")
open(OUT / 'step5-origin-questions.md', 'w').write('\n'.join(Q) + '\n')
print(json.dumps(dict(units=len(UNITS), ledger_521=count_521, open=len(OPEN), open_by_type=summary['open_by_type'], stale=len(STALE)), ensure_ascii=False))
