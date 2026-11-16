"""실버 7단계(고민 · 목적 · 추천 조합) 반영 — 결정론(3 · 4 · 5 · 6단계와 같은 구조).

입력: step7-decisions.json(결정 — 고민 트리 갈래 · 대응표 · 목적 · 세션 조합 앵커 · 이름 풀이 사전 · 못 풂 · check · 사용자 판단)
      원천(결정 source.path) taxonomy.problem · problem-packages · problem-combos · combo-recipes · treatment-optimization ·
      procedure-comparison · synergy · treatment-sequence
      step3-sites · step5-units · step6-packages(읽기만)
출력: step7-concerns.json · step7-concerns.md · step7-origin-questions.md · step7-source-fix.md

조사(step7-research · scratchpad step7_build.py · step7_final.py)의 계산을 그대로 옮기고, 조사 스크립트 안에 박혀 있던 표를 결정 파일로 뺐다.
원천 행인데 결정에 없으면 open[], 결정이 가리키는 원천 · 고민 · 목적 · 단위 시술이 없으면 open[] / stale_decisions[].
단위 시술 없는 이름(시술 아님 결정 밖)은 open — 5단계 보강(J7)으로 닫는다. 숫자는 이 파일에 적지 않는다(고정 assert 없음).
"""
import argparse
import collections
import json
import re
from pathlib import Path

W = Path(__file__).resolve().parent
AP = argparse.ArgumentParser()
AP.add_argument('--source', help='원천 경로 덮어쓰기(고정 시험용)')
AP.add_argument('--decisions', default=str(W / 'step7-decisions.json'))
AP.add_argument('--out', default=str(W), help='산출 폴더(고정 시험은 임시 폴더)')
ARGS = AP.parse_args()
OUT = Path(ARGS.out)
DEC = json.load(open(ARGS.decisions))
SRC = Path(ARGS.source or DEC['source']['path'])
J = lambda p: json.load(open(p))
tax = J(SRC / 'taxonomy.json')
pp = J(SRC / 'problem-packages.json')
pc = J(SRC / 'problem-combos.json')
cr = J(SRC / 'combo-recipes.json')
to = J(SRC / 'treatment-optimization.json')
cmp_ = J(SRC / 'procedure-comparison.json')
syn = J(SRC / 'synergy.json')
ts = J(SRC / 'treatment-sequence.json')
s3 = J(W / DEC['canon']['step3'])
s5 = J(W / DEC['canon']['step5'])
s6 = J(W / DEC['canon']['step6'])
UNITS = {u['id']: u for u in s5['units']}
UN = {u['id']: u['name'] for u in s5['units']}
C = collections.Counter

OPEN, STALE = [], []


def op(t, **kw):
    OPEN.append(dict(type=t, **kw))


RES = DEC['resolver']
RENAME = DEC['rename']


def norm(s):
    for a, b in RENAME.items():
        s = s.replace(a, b)
    return re.sub(r'[\s/·,()\-+&]', '', s).lower()


# ───────── 0. 부위 · 단위 시술 찾기 ─────────
CHILD = collections.defaultdict(list)
for n in s3['nodes']:
    if n['parent']:
        CHILD[n['parent']].append(n['name'])


def desc(site):
    out = [site]
    for c in CHILD.get(site, []):
        out += desc(c)
    return out


def want_sites(sites):
    return set(sum([desc(s) if s != '얼굴' else ['얼굴 전체'] for s in sites], []))


def units_at(fams, sites, sub=None):
    """단위 시술 = 계열 ∈ fams 이고 부위가 sites 아래. 얼굴 → 얼굴 전체만(5단계 J2 기본값)."""
    want = want_sites(sites)
    r = [u['id'] for u in s5['units'] if u['key']['family'] in fams and u['key']['site'] in want]
    if sub:
        r = [i for i in r if UNITS[i]['key'].get('sub_family') and sub in UNITS[i]['key']['sub_family']] or r
    return r


def units_of(fams):
    return [u['id'] for u in s5['units'] if u['key']['family'] in fams]


# 부위 올라가기(site_rules.climb · R21 — 사용자 10-29) — 그 부위에 계열 단위 시술이 없으면 3단계 트리 상위 노드 「자신」으로 올라가며 찾고
# (형제 부위 안 넣음 · 묶음은 직접 붙은 단위 시술이 없어 통과), 최상위 영역의 「전체」 노드까지. 영역 경계는 넘지 않음 · 끝까지 없으면 계열만
PARENT = {n['name']: n['parent'] for n in s3['nodes']}
ROOTS = [n['name'] for n in s3['nodes'] if not n['parent']]  # 최상위 영역 — 3단계 트리에서 계산


def region(site):
    if site not in PARENT:
        return None
    while PARENT[site]:
        site = PARENT[site]
    return site


def whole_of(root):
    """최상위 영역의 「전체」 노드 — 「R 전체」 자식이 있으면 그것 · 없으면 R 자신(묶음 아님) · 묶음이면 없음"""
    kid = f'{root} 전체'
    if PARENT.get(kid) == root:
        return kid
    return None if root.endswith('(묶음)') else root


def layers_of(site):
    """앵커 부위 위 층 — 조상 노드 자신(최상위 제외) · 끝 = 최상위 영역의 「전체」 노드"""
    out, a = [], PARENT.get(site)
    while a and PARENT.get(a):
        out.append(a)
        a = PARENT[a]
    root = region(site)
    w = whole_of(root) if root else None
    if w and w != site:
        out.append(w)
    return out


def anchor_regions(sites):
    return {region('얼굴 전체' if s == '얼굴' else s) for s in sites} - {None}


def climb(fams, sites, sub=None, pool=None):
    """층마다 그 노드 자신에 붙은 단위 시술(계열 ∈ fams · pool 이 있으면 그 안) — 처음 찾은 층만. 반환 (units, 층 이름) · 없으면 ([], None)"""
    seen = want_sites(sites)
    chains = [layers_of(s) for s in sites if s in PARENT]
    for k in range(max([len(c) for c in chains] or [0])):
        lay = [c[k] for c in chains if k < len(c) and c[k] not in seen]
        if not lay:
            continue
        seen |= set(lay)
        r = [u['id'] for u in s5['units'] if u['key']['family'] in fams and u['key']['site'] in lay and (pool is None or u['id'] in pool)]
        if sub:
            r = [i for i in r if UNITS[i]['key'].get('sub_family') and sub in UNITS[i]['key']['sub_family']] or r
        if r:
            return r, '/'.join(x for x in dict.fromkeys(lay) if any(UNITS[i]['key']['site'] == x for i in r))
    return [], None


def climb_res(fams, sites, basis, sub=None):
    """sfilter · fam_kw 의 「그 부위 단위 시술 없음」 자리 — 올라가 찾은 층의 단위 시술 · 없으면 계열만(to_units 비움)"""
    us, lay = climb(fams, sites, sub)
    if us:
        return {'status': f'상위 부위로 내림({lay})' + (' · 후보 여럿' if len(us) > 1 else ''), 'units': us, 'families': fams,
                'basis': basis + f' → 계열 {"/".join(fams)} 에 부위 {"/".join(sites)} 단위 시술 없음 · 상위 부위 {lay} 층(R21)', 'flag': None if len(us) == 1 else 'ambiguous', 'site_layer': lay}
    return {'status': '이 부위 단위 시술 없음 · 계열만', 'units': [], 'families': fams,
            'basis': basis + f' → 계열 {"/".join(fams)} 에 부위 {"/".join(sites)} · 상위 부위 · 영역 「전체」 노드까지 단위 시술 없음(R21)', 'flag': 'no_unit_at_site'}


# ───────── 1. 이름 풀이(§3.3.2 — 이름 칸만) ─────────
GENERIC = set(RES['generic_synonyms'])
SYN = collections.defaultdict(set)
for u in s5['units']:
    SYN[norm(u['name'])].add(u['id'])
    for s in u['synonyms']:
        if s.get('type') == '시장가 이름' or s['text'] in GENERIC:
            continue
        SYN[norm(s['text'])].add(u['id'])
for x in RES.get('forced_synonyms') or []:
    SYN[norm(x['text'])] = set(x['units'])
PROD = collections.defaultdict(set)
for p in s5['product_links']:
    us = set(p.get('stored_units') or []) | set(p.get('inherited_candidates') or [])
    if us:
        PROD[norm(p['name'])] |= us
for d in s5['device_name_synonyms']:
    PROD[norm(d['name'])] |= set(d['units'])
FAM_KW = [(x['kw'], x['families'], x['units']) for x in RES['fam_kw']]
for kw, fams, fixed in FAM_KW:
    for i in fixed or []:
        if i not in UNITS:
            op('결정이 가리키는 단위 시술 없음', where=f'resolver.fam_kw {kw}', unit=i)
NO_UNIT = {x['name']: x for x in RES['no_unit']}
EXACT = {x['text']: x for x in RES.get('exact_overrides') or []}
USED_EXACT = set()
for x in EXACT.values():
    for i in x['units']:
        if i not in UNITS:
            op('결정이 가리키는 단위 시술 없음', where=f"resolver.exact_overrides {x['text']}", unit=i)
BRANDS = set(RES['brands'])
GENERIC_KW = {kw.lower() for kw, _, _ in FAM_KW} - {b.lower() for b in BRANDS}
BODY_WORDS = RES['body_words']
SITE_KW = [tuple(x) for x in RES['site_kw']]
AMBIG = set(RES['ambiguous_site_kw'])
SITE_NAMES = {n['name'] for n in s3['nodes']} | {'병변 단위', '전신'}
SITE_FREE = set(DEC['site_rules']['site_free'])  # 부위 무관 특수 부위(5단계 special_sites) — 앵커 부위 검사 · 내림에서 그대로
for k, s in SITE_KW:
    if s not in SITE_NAMES:
        op('결정이 가리키는 부위 없음', where=f'resolver.site_kw {k}', site=s)


def sites_in(text):
    """이름 칸의 부위 낱말. 한 글자 부위는 앞이 한글이 아닐 때만(피코 · 필러볼륨 · 발현 제외) · 「등」(etc.)은 「/」 뒤 또는 「등살」만"""
    out = []
    t = text
    for k, s in SITE_KW:
        if k in AMBIG:
            if k == '등':
                pat = r'(?:(?<=/)|^)등(?![가-힣])|등살'
            else:
                pat = r'(?<![가-힣])' + k + r'(?!륨|그|어|현|상|급|록|면)'
            if re.search(pat, t):
                if s not in out:
                    out.append(s)
                t = re.sub(pat, ' ', t)
        elif k in t:
            if s not in out:
                out.append(s)
            t = t.replace(k, ' ')
    return out


CHECK = DEC['check_flags']


def resolve(name, ctx_sites=None, products=None):
    r = _resolve(name, ctx_sites, products)
    for c in CHECK:
        if r['units'] == [c['unit']] and '스킨' not in name and '모공' not in name:
            r = dict(r, flag='check', basis=r['basis'] + ' — 얼굴 전체 M1 단위 시술은 스킨보톡스(K01a)뿐 · 원천 이름과 같은 시술인지 사람 확인')
    return r


def _resolve(name, ctx_sites=None, products=None):
    """원천 이름 하나 → 단위 시술. 반환 {status, units, family, basis, flag}"""
    n = name.strip()
    nn = norm(n)
    for k, x in NO_UNIT.items():
        why = x['basis']
        if k == '냉동' and nn != '냉동':
            continue
        if why and norm(k) in nn and not (k == 'RF 타이트닝' and '바디' not in n and ctx_sites and not any(s in BODY_WORDS for s in ctx_sites)):
            if k in ('RF 타이트닝',) and not (ctx_sites and any(s in BODY_WORDS + ['바디'] for s in ctx_sites)):
                continue
            st = '시술 아님' if x['kind'] == '시술 아님' else '단위 시술 없음'
            return {'status': st, 'units': [], 'basis': why, 'flag': 'not_procedure' if st == '시술 아님' else 'no_unit'}
    own_sites = sites_in(n)
    sites = own_sites or (ctx_sites or [])

    def sfilter(us, label, basis):
        """이름 · 동의어 · 제품으로 잡은 단위 시술을 앵커 부위로 — 맞는 게 없으면 같은 계열(하위 하나면 그 하위)을 부위로 내림(검수 F2) ·
        그래도 없으면 부위 트리 상위로 올라가 찾고 · 끝까지 없으면 계열만 + no_unit_at_site(R21 · W2 규칙 대체). 부위 무관 특수 부위(해당 없음 · 병변 단위)는 그대로."""
        if not sites:
            return {'status': label if len(us) == 1 else label + ' · 후보 여럿', 'units': us, 'basis': basis, 'flag': None if len(us) == 1 else 'ambiguous'}
        want = want_sites(sites)
        at = [u for u in us if UNITS[u]['key']['site'] in want or UNITS[u]['key']['site'] in SITE_FREE]
        if at:
            return {'status': label if len(at) == 1 else label + ' · 후보 여럿', 'units': at, 'basis': basis + (f' · 부위 {"/".join(sites)}' if len(at) < len(us) else ''), 'flag': None if len(at) == 1 else 'ambiguous'}
        fams = sorted({UNITS[u]['key']['family'] for u in us})
        sub_ = {UNITS[u]['key'].get('sub_family') for u in us}
        at2 = units_at(fams, sites, next(iter(sub_)) if len(sub_) == 1 else None)
        if at2:
            return {'status': '부위로 내림' if len(at2) == 1 else '부위로 내림 · 후보 여럿', 'units': at2, 'basis': basis + f' → 앵커 부위 {"/".join(sites)} 밖이라 계열 {"/".join(fams)} × 부위로 내림', 'flag': None if len(at2) == 1 else 'ambiguous'}
        return climb_res(fams, sites, basis, next(iter(sub_)) if len(sub_) == 1 else None)
    if nn in SYN:
        return sfilter(sorted(SYN[nn]), '이름 일치', '5단계 단위 시술 이름 · 동의어 완전 일치')
    if nn in PROD and len(PROD[nn]) <= 6:
        return sfilter(sorted(PROD[nn]), '제품 이름', '5단계 제품 → 단위 시술(저장 · 상속 후보)')
    for kw, fams, fixed in FAM_KW:
        if kw.lower() in n.lower():
            if fixed is None and fams is None:
                return {'status': '못 풂', 'units': [], 'basis': f'「{kw}」 — 원천 이름만으로 단위 시술을 못 정함', 'flag': 'unresolved'}
            if fixed:
                cand = [u for u in fixed if u in UNITS]
                return sfilter(cand, '이름 일치', f'「{kw}」 → 5단계 단위 시술')
            if sites:
                at = units_at(fams, sites)
                if at:
                    return {'status': '부위로 내림' if len(at) == 1 else '부위로 내림 · 후보 여럿', 'units': at, 'basis': f'계열 {fams[0]} × 부위 {"/".join(sites)}' + ('' if own_sites else '(맥락 부위)'), 'flag': None if len(at) == 1 else 'ambiguous'}
                return climb_res(fams, sites, f'계열 {fams[0]}' + ('' if own_sites else '(맥락 부위)'))
            allf = units_of(fams)
            toks = [t for t in re.split(r'[\s()/,+·]+', n) if len(norm(t)) >= 3 and t.lower() not in GENERIC_KW]
            products = list(products or []) + toks
            if products:
                pu = set()
                for p in list(products) + [t_ for p0 in products for t_ in re.split(r'[()/·,+]', p0) if t_.strip() and t_.strip() != p0]:  # R24 — 괄호 · 「/」 안 낱말까지(「PDL(V빔)」)
                    pu |= PROD.get(norm(p), set()) | SYN.get(norm(p), set())
                    pu |= {i_ for kw_, _, fx_ in FAM_KW if fx_ and kw_.lower() == p.strip().lower() for i_ in fx_}  # 고정 키 낱말(「V빔」 → U5-141)
                    if len(norm(p)) >= 3:
                        for k_, v_ in PROD.items():
                            if k_.startswith(norm(p)):
                                pu |= v_
                nar = [u for u in allf if u in pu]
                if nar:
                    return {'status': '제품으로 좁힘' if len(nar) > 1 else '제품으로 내림', 'units': nar, 'basis': f'계열 {fams[0]} ∩ 원천 제품 {"/".join(products)}', 'flag': None if len(nar) == 1 else 'ambiguous'}
            return {'status': '부위 없음 · 후보 전부' if len(allf) > 1 else '이름 일치', 'units': allf, 'basis': f'계열 {fams[0]} — 원천에 부위 없음', 'flag': 'concern_without_site' if len(allf) > 1 else None}
    return {'status': '못 풂', 'units': [], 'basis': '계열 · 단위 시술 이름 없음', 'flag': 'unresolved'}


def has_kw(x):
    return norm(x) in SYN or any(kw.lower() in x.lower() for kw, _, _ in FAM_KW) or any(norm(k) in norm(x) for k, w in NO_UNIT.items() if w['basis'])


def comp_one(nm, ctx=None, products=None, purpose=None):
    """원천 조합 칸의 시술 이름 하나 — 「+」 · 「/」 로 나뉜 것은 조각마다 풀고, 괄호 안은 부위 · 제품 · 짧은 대안 목록으로만 쓴다"""
    if nm.strip() in EXACT:
        x = EXACT[nm.strip()]
        USED_EXACT.add(nm.strip())
        return {'status': x['status'], 'units': list(x['units']), 'basis': x['basis'], 'flag': x.get('flag')}
    base = nm.replace('NAD+', 'NAD')
    pieces = [x.strip() for x in re.split(r'\+| or ', base) if x.strip()]
    if len(pieces) > 1 and not all(has_kw(x) for x in pieces):
        pieces = [base]
    us, sts, flags, rs_all = [], [], set(), []
    for pc_ in pieces:
        m = re.match(r'^(.*?)\((.*?)\)(.*)$', pc_)
        main, paren = (m.group(1) + m.group(3), m.group(2)) if m else (pc_, '')
        subs_ = [x for x in main.split('/') if x.strip()]
        if len(subs_) > 1 and all(has_kw(x) for x in subs_):
            rs = [(x, resolve(x, ctx, products)) for x in subs_]
        else:
            pctx = (ctx or []) + sites_in(paren)
            pprod = list(products or []) + [t for t in re.split(r'[/·,\s]+', paren) if t]
            rs = [(main, resolve(main.strip() or pc_, pctx or None, pprod))]
            if rs[0][1]['status'] == '못 풂' and paren:
                r3 = resolve(paren, ctx)
                if r3['status'] != '못 풂':
                    rs = [(pc_, r3)]
            alts = [t for t in paren.split('/') if t.strip()]
            if len(alts) > 1 and all(len(t) <= 12 for t in alts):
                base_f = {UNITS[u]['key']['family'] for u in rs[0][1]['units']}
                for t in alts:
                    if not any(g in t.lower() for g in GENERIC_KW) or any(b.lower() in t.lower() for b in BRANDS):
                        continue
                    r2 = resolve(t)
                    f2 = {UNITS[u]['key']['family'] for u in r2['units']}
                    if r2['units'] and f2 and not (f2 & base_f):
                        rs.append((t, r2))
        if purpose in PURPOSE_CTX:
            pcx = PURPOSE_CTX[purpose]
            rs2 = []
            for x, r in rs:
                hit = next((o for o in pcx['overrides'] if o['contains'] in x), None)
                if hit:
                    rs2.append((x, {'status': hit['status'], 'units': hit['units'], 'basis': hit['basis'], 'flag': hit.get('flag')}))
                else:
                    rs2.append((x, {'status': pcx['default']['status'], 'units': pcx['default']['units'], 'basis': pcx['default']['basis'], 'flag': pcx['default'].get('flag')}))
            rs = rs2
        rs_all += rs
    for x, r in rs_all:
        us += [u for u in r['units'] if u not in us]
        sts.append(f"{x.strip()}→{r['status']}")
        if r.get('flag'):
            flags.add(r['flag'])
    if len(rs_all) == 1:
        r = rs_all[0][1]
        return {'status': r['status'], 'units': us, 'basis': r['basis'], 'flag': r.get('flag'), **{k: r[k] for k in ('families', 'site_layer') if r.get(k)}}
    extra = {}
    lays = [r['site_layer'] for _, r in rs_all if r.get('site_layer')]
    if lays:
        extra['site_layer'] = '/'.join(dict.fromkeys(lays))
    fo = sorted({f for _, r in rs_all if not r['units'] for f in r.get('families') or []})
    if fo:
        extra['families'] = fo
    return {'status': '복합 · 나눠 풂', 'units': us, 'basis': ' · '.join(sts), 'flag': ','.join(sorted(flags)) or None, **extra}


def comp(names, ctx=None, products=None, purpose=None):
    out = []
    for i, nm in enumerate(names):
        m = re.search(r'(\d+)\s*(회|차)', nm)
        cnt_ = m.group(0) if m else None
        base = re.sub(r'\s*\d+\s*(회|차)', '', nm).strip() if m else nm
        x = {'order': i + 1, 'text': nm, 'sessions': cnt_, **comp_one(base, ctx, products, purpose)}
        g = gloss_of(nm)
        if g:
            x['concern_gloss'] = g
        out.append(x)
    return out


def gloss_of(nm):
    """원소 괄호가 고민 · 목적 풀이(「프락셔널(피부결)」)면 그 고민 — 규칙(R12~R17)으로 풀린 것만. 대응표 뒤에 정의된 judge 를 부른다"""
    m = re.search(r'\(([^()]*)\)', nm)
    if not m or 'judge' not in globals():
        return None
    r = judge(m.group(1))
    return r['target'] if r['ok'] and r['target'] else None


PURPOSE_CTX = {x['purpose']: x for x in DEC['purpose_context']}
for x in DEC['purpose_context']:
    for o in x['overrides'] + [x['default']]:
        for i in o['units']:
            if i not in UNITS:
                op('결정이 가리키는 단위 시술 없음', where=f"purpose_context {x['purpose']}", unit=i)
CTX_BY = {(x['source'], x['key']): x for x in DEC['context_by_source']}


def ctx_of(source, key):
    x = CTX_BY.get((source, key))
    return (x.get('sites') or None, x.get('purpose')) if x else (None, None)


# ───────── A. 고민 트리 분해 ─────────
CATD = {x['id']: x for x in DEC['categories']}
SUBD = {x['id']: x for x in DEC['subcategories']}
ITEMD = {x['id']: x for x in DEC['items']}
P1MAP = {r['id']: r for r in s5['problem_P1']}
cats, subs, items = [], [], []
src_cat, src_sub, src_item = set(), set(), set()
for P in tax['problem']:
    src_cat.add(P['id'])
    rule = CATD.get(P['id'])
    if rule is None:
        op('결정 없는 고민 대분류', id=P['id'], name=P['category'])
    verdict, basis = (rule['verdict'], rule['basis']) if rule else (None, '결정 없음')
    name = P['category']
    for a, b in RENAME.items():
        name = name.replace(a, b)
    cats.append({'id': P['id'], 'source_name': P['category'], 'name': name, 'en': P['category_en'], 'verdict': verdict,
                 'basis': basis or ('이름 치환 쳐짐→처짐(SPEC-004 치환표 · 10-27)' if name != P['category'] else '원천 그대로'),
                 'node': verdict not in ('고민 아님(시술 범주)', '고민 아님(기타 묶음)')})
    for S in P['subcategories']:
        src_sub.add(S['id'])
        k = SUBD.get(S['id'])
        if k is None:
            op('결정 없는 고민 중분류', id=S['id'], name=S['label'])
            k = {'kind': None, 'concern': None, 'sites': [], 'purpose': None, 'note': '', 'node': False}
        for s_ in k['sites']:
            if s_ not in SITE_NAMES:
                op('결정이 가리키는 부위 없음', where=S['id'], site=s_)
        subs.append({'id': S['id'], 'parent': P['id'], 'source_label': S['label'], 'kind': k['kind'], 'concern': k['concern'], 'sites': k['sites'], 'purpose': k['purpose'], 'note': k['note'],
                     'node': k['node'], 'top_level': k['node'] and not cats[-1]['node']})
        for I in S['items']:
            src_item.add(I['id'])
            ctx = k['sites']
            d = ITEMD.get(I['id'])
            if d is None:
                op('결정 없는 고민 항목', id=I['id'], name=I['name'])
                continue
            if d['name'] != I['name']:
                op('고민 항목 이름 바뀜', id=I['id'], decision=d['name'], source=I['name'])
            kind = d['kind']
            res = None
            if P['id'] == 'P1':
                m = P1MAP.get(I['id'])
                if m is None:
                    op('쁘띠시술 메뉴가 5단계에 없음', id=I['id'], name=I['name'])
                    continue
                res = {'status': m['dest'], 'units': m['units'], 'basis': f"5단계 problem_P1 {m['decided_by']}" + (f" · {m['note']}" if m.get('note') else ''), 'flag': 'ambiguous' if m['role'] == '후보' and len(m['units']) > 1 else None}
                cpart, isites = None, ctx
            elif kind in ('고민', '부위', '시술 아님'):
                cpart, isites = d.get('concern'), d.get('sites') or []
                if kind == '시술 아님':
                    res = resolve(I['name'] + ' ' + I.get('detail', ''))
                    if res['status'] != '시술 아님':
                        op('시술 아님 항목인데 시술 아님 결정 없음', id=I['id'], name=I['name'])
            else:
                cpart, isites = None, ctx
            if kind == '시술 이름' and res is None:
                txt = I['name']
                own = sites_in(txt) or sites_in(I.get('detail', ''))
                prods = [x for x in re.split(r'[/ ·,]+', I.get('detail', '')) if x]
                res = resolve(txt, own or ctx, prods)
                if res['status'] == '못 풂' and I.get('detail'):
                    res = resolve(I['detail'], own or ctx)
                parts = None
                if ('+' in txt.replace('NAD+', 'NAD')) or I['name'] in DEC['composite_items']:
                    parts = re.split(r'\+', txt) if '+' in txt.replace('NAD+', 'NAD') else re.split(r'[/]', I.get('detail', '').split('.')[0])
                    if all(resolve(x, own or ctx)['status'] == '못 풂' for x in parts) and I['name'] not in DEC['composite_site_split']:
                        parts = None
                if parts:
                    us, sts, pfl = [], [], set()
                    for ptxt in parts:
                        r2 = resolve(ptxt, own or ctx)
                        us += [u for u in r2['units'] if u not in us]
                        sts.append(f"{ptxt.strip()}→{r2['status']}")
                        pfl |= set(filter(None, (r2.get('flag') or '').split(',')))
                    if I['name'] in DEC['composite_site_split']:
                        us, sts = [], []
                        for s_ in DEC['composite_site_split'][I['name']]:
                            us += units_at(['M1'], [s_])
                            sts.append(f'{s_}→부위로 내림')
                    if any('후보' in x or '없음' in x for x in sts):
                        pfl.add('ambiguous')
                    res = {'status': '복합 · 나눠 풂', 'units': us, 'basis': ' · '.join(sts), 'flag': ','.join(sorted(pfl)) or None}  # 재검수 v2 W2 — 조각 플래그 합침
            fams = I.get('modality_ref') or []
            low = None
            if kind in ('고민', '부위'):
                low = {f: units_at([f], isites) if isites else [] for f in fams}
            items.append({'id': I['id'], 'subcategory': S['id'], 'category': P['id'], 'name': I['name'], 'detail': I.get('detail', ''), 'modality_ref': fams,
                          'kind': kind, 'concern': cpart, 'sites': isites, 'resolve': res, 'modality_lowered': low})
STALE += [['categories', k] for k in CATD if k not in src_cat]
STALE += [['subcategories', k] for k in SUBD if k not in src_sub]
STALE += [['items', k] for k in ITEMD if k not in src_item]
# J8 등 원천 밖 고민 항목(결정 이행)
extra_items = []
for x in DEC['extra_concern_items']:
    if x['parent'] is not None and x['parent'] not in {c['id'] for c in cats if c['node']} | {s['id'] for s in subs if s['node']}:  # J10 피부결 = 상위 없음(대분류 급)
        op('결정이 가리키는 고민 노드 없음', where=x['id'], concern=x['parent'])
    for s_ in x['sites']:
        if s_ not in SITE_NAMES:
            op('결정이 가리키는 부위 없음', where=x['id'], site=s_)
    extra_items.append(dict(x, kind='고민(원천 밖 · 결정)'))

PMAP = DEC['purpose_map_from_sub']
SUBX = {x['id']: x for x in subs}
CATX = {x['id']: x for x in cats}


def anchor_of(it):
    if it['kind'] == '고민':
        return it['id']
    S_ = SUBX[it['subcategory']]
    if S_['node']:
        return S_['id']
    if S_['kind'] == '목적':
        return f"목적:{PMAP.get(S_['purpose'], S_['purpose'])}"
    c_ = CATX[it['category']]
    return c_['id'] if c_['node'] else f"(앵커 없음 — {c_['source_name']})"


# 사이트 용어 · 이름 치환 = 고민 동의어(J3 · R1)
for x in DEC['concern_synonyms']:
    n_ = next((c for c in cats + subs if c['id'] == x['id'] and c['node']), None)
    if n_ is None:
        op('결정이 가리키는 고민 노드 없음', where=f"concern_synonyms {x['id']}", concern=x['id'])
        continue
    n_['synonyms'] = x['synonyms']
    n_['synonyms_basis'] = x['basis']

# ───────── B. 고민 대응표 — 규칙(R12~R20 · 10-29 「게이트 → 규칙」) ─────────
CONCERN_IDS = {c['id'] for c in cats if c['node']} | {s['id'] for s in subs if s['node']} | {i['id'] for i in items if i['kind'] == '고민'} | {x['id'] for x in extra_items}
ITEM_IDS = {i['id'] for i in items}
CRU = DEC['concern_rules']
SEPS = CRU['split_separators']
SEV_WORDS = CRU['severity_words']
SEV_CHILD = {x['concern']: x['map'] for x in CRU['severity_children']}
for x in CRU['severity_children']:
    for v in [x['concern']] + list(x['map'].values()):
        if v not in CONCERN_IDS:
            op('결정이 가리키는 고민 노드 없음', where='concern_rules.severity_children', concern=v)
SITE_PARENT = {n['name']: n['parent'] for n in s3['nodes']}
SITE_WORDS = {k: s for k, s in SITE_KW}
SITE_WORDS.update({x: x for x in CRU['extra_site_words']})  # R17 — 3단계 최상위 부위(바디 · 얼굴) · 「전신」은 계통 뜻이라 뺌(3단계 OQ-306)


def site_chain(s):
    out = []
    while s and s not in out:
        out.append(s)
        s = SITE_PARENT.get(s)
    return out


# 고민 노드 부모(트리) — 대분류 ← 중분류 ← 항목
CPARENT = {}
for s in subs:
    if s['node'] and CATX[s['parent']]['node']:
        CPARENT[s['id']] = s['parent']
for it in items:
    if it['kind'] == '고민':
        CPARENT[it['id']] = it['subcategory'] if SUBX[it['subcategory']]['node'] else (it['category'] if CATX[it['category']]['node'] else None)
for x in extra_items:
    CPARENT[x['id']] = x['parent']


def canc(i):
    out = []
    while i and i not in out:
        out.append(i)
        i = CPARENT.get(i)
    return out


def pvars(s):
    """「급성(활성) 여드름」 → 급성 여드름 · 활성 여드름 / 「주름(라인)」 → 주름 · 라인"""
    m = re.match(r'^(.*?)\((.*?)\)(.*)$', s)
    if not m:
        return [s]
    a, b, c = m.groups()
    t = a.split()
    return [a + c, ' '.join(t[:-1] + [b]) + c if t else b + c]


def parts_of(s):
    return [x.strip() for x in re.split('|'.join(re.escape(x) for x in SEPS), s) if x.strip()]


def knorm(x):
    """대응표 낱말 키 — norm 과 같되 묶음 구분자는 「/」로 남긴다(「여드름/흉터」 ≠ 「여드름흉터」 P9-1)"""
    for a, b in RENAME.items():
        x = x.replace(a, b)
    for sp in SEPS:
        x = x.replace(sp, '/')
    return re.sub(r'[\s()\-&]', '', x).lower().strip('/')


LEX = collections.defaultdict(list)  # 정규화 낱말 → [(대상, 등급, 부위)] · 등급 1 완전 · 2 묶음 낱말 · 3 목적 · 4 목적 대상 낱말


def addk(key, tgt, tier, sites, how):
    k = knorm(key)
    if k and (tgt, tier, tuple(sites)) not in [(a, b, c) for a, b, c, _ in LEX[k]]:
        LEX[k].append((tgt, tier, tuple(sites), how))


def add_name(name, tgt, sites, how, whole_tier=1):
    ps = parts_of(name)
    for v in pvars(name):
        addk(v, tgt, whole_tier, sites, how)
    if len(ps) > 1:
        for p in ps:
            for v in pvars(p):
                addk(v, tgt, 2, sites, how + ' 의 낱말(R12)')


NODE_SITES = {}
for c in cats:
    if not c['node']:
        continue
    st = []
    if len(parts_of(c['name'])) == 1:  # 「얼굴윤곽」 = 얼굴 + 윤곽 · 「바디」 = 부위 바디(R17)
        st = [s for s in SITE_PARENT if c['name'].startswith(s) and s != '얼굴 전체'][:1]
        if st and c['name'] != st[0]:
            addk(c['name'][len(st[0]):], c['id'], 1, st, '대분류 이름 − 부위')
    NODE_SITES[c['id']] = st
    add_name(c['name'], c['id'], st, '대분류 이름')
    add_name(c['source_name'], c['id'], st, '대분류 원천 이름')
for s in subs:
    if s['node']:
        NODE_SITES[s['id']] = s['sites']
        add_name(s['source_label'], s['id'], s['sites'], '중분류 이름')
        if s['concern']:
            add_name(s['concern'], s['id'], s['sites'], '중분류 고민 칸')
for it in items:
    if it['kind'] == '고민':
        NODE_SITES[it['id']] = it['sites']
        add_name(it['name'], it['id'], it['sites'], '항목 이름')
        if it['concern']:
            add_name(it['concern'], it['id'], it['sites'], '항목 고민 칸')
for x in extra_items:
    NODE_SITES[x['id']] = x['sites']
    add_name(x['name'], x['id'], x['sites'], '결정 노드 이름')
    for w in x.get('synonyms') or []:
        addk(w, x['id'], 1, x['sites'], '결정 노드 동의어')
for x in DEC['concern_synonyms']:
    if x['id'] in NODE_SITES:
        for w in x['synonyms']:
            addk(w, x['id'], 1, NODE_SITES[x['id']], '고민 동의어(J3 · R1)')
MENU_T = {x['id']: x for x in CRU.get('menu_anchor_targets') or []}  # 쁘띠시술 부위 메뉴(P1-x) — 고민 노드는 아니지만 대응 대상(사용자 10-29)
for i_ in MENU_T:
    if i_ not in SUBX or SUBX[i_]['parent'] != 'P1':
        op('결정이 가리키는 고민 노드 없음', where='concern_rules.menu_anchor_targets', concern=i_)
CWORD = {}  # 낱말 → 대상 여럿(고민 · 쁘띠시술 메뉴 · 목적) — 부위와 관계없이 그대로(사용자 결정 사전)
for x in CRU['concern_words']:
    tg = x.get('targets') or [x['target']]
    bad_ = [t for t in tg if t not in CONCERN_IDS and t not in MENU_T and not (t.startswith('목적:') and t[3:] in {p['name'] for p in DEC['purposes'] if not p['same_as_concern']})]
    if bad_:
        for t in bad_:
            op('결정이 가리키는 고민 노드 없음', where=f"concern_rules.concern_words {x['text']}", concern=t)
        continue
    if len(tg) == 1 and tg[0] in CONCERN_IDS:
        addk(x['text'], tg[0], 1, NODE_SITES.get(tg[0], []), '고민 낱말 결정')
    else:
        CWORD[knorm(x['text'])] = (tg, x)
for k in list(LEX):  # R16 「항X」 → X
    if k.startswith(CRU['anti_prefix']) and len(k) > 2:
        for tgt, tier, st, how in list(LEX[k]):
            addk(k[1:], tgt, 2, st, f'「{k}」의 「항」을 뗀 말(R16)')
# 목적(J4 · R6) — 고민과 같은 말은 그 고민, 아니면 목적 노드
PURP = {p['name']: p for p in DEC['purposes']}
PC = {x['purpose']: x for x in CRU['purpose_concern']}
for x in CRU['purpose_concern']:
    if x['purpose'] not in PURP or PURP[x['purpose']]['same_as_concern']:
        op('결정이 가리키는 목적 없음', where='concern_rules.purpose_concern', purpose=x['purpose'])
for p in DEC['purposes']:
    tgt = p['same_as_concern'] or f"목적:{p['name']}"
    pst = NODE_SITES.get(p['same_as_concern'], []) if p['same_as_concern'] else []  # 고민과 같은 말 = 그 고민의 부위(「윤곽」 = 얼굴)
    keys = set(pvars(p['name'])) | set(re.findall(r'\((.*?)\)', p['name'])) | {a['text'] for a in p['aliases'] if not re.search(r'[/·(]', a['text'])}
    for k in sorted(keys):
        addk(k, tgt, 3, pst, '목적 이름 · 원천 낱말(J4)')
        for vt in CRU['purpose_verb_tails']:
            if knorm(k).endswith(vt) and len(knorm(k)) > len(vt):
                addk(knorm(k)[:-len(vt)], tgt, 4, pst, f'목적 이름의 동사 꼬리 「{vt}」를 뗀 대상 낱말(R16)')
EN = {}  # 영문(정규화) → 한글 원천 말 — 원천 짝(R15)


def en_norm(s):
    s = s.lower().replace('_', ' ').replace('&', ' ').strip()
    s = re.sub(r'^skin\s+', '', s)
    return re.sub(r'\s+', ' ', s)


def add_en(en, ko, basis):
    EN.setdefault(en_norm(en), [])
    if (ko, basis) not in EN[en_norm(en)]:
        EN[en_norm(en)].append((ko, basis))
    ep, kp = [x.strip() for x in en.split('/')], parts_of(ko)
    if len(ep) > 1 and len(ep) == len(kp):
        for a, b in zip(ep, kp):
            add_en(a, b, basis + ' (나눈 짝)')


for c in cats:
    if c['node']:
        add_en(c['en'], c['name'], 'taxonomy category_en')
for c in to['by_concern']:
    add_en(c['concern_en'], c['concern'], '최적화 concern_en')
for c in cmp_['comparisons']:
    add_en(c['id'], c['title'], '비교 id ↔ 제목')
for x in CRU['en_extra']:
    add_en(x['en'], x['to'], x['basis'])
LOAN = {norm(x['text']): x for x in CRU['loanwords']}
UNIT_WORDS = set(SYN) | {norm(kw) for kw, _, _ in FAM_KW}
TAILS = sorted(CRU['tails'] + CRU['state_tails'], key=len, reverse=True)
OUT_KIND = CRU['out_of_tree_purpose_kind']
OUT_PURP = {f"목적:{p['name']}" for p in DEC['purposes'] if OUT_KIND in p['kind']}


def ok(target, rules, sites=(), sev=(), note=None):
    return {'ok': True, 'target': list(dict.fromkeys(target)), 'rules': list(dict.fromkeys(rules)), 'sites': list(dict.fromkeys(sites)), 'severity': list(dict.fromkeys(sev)), 'note': note}


def bad(why, cands=(), rules=()):
    return {'ok': False, 'why': why, 'candidates': list(dict.fromkeys(cands)), 'rules': list(dict.fromkeys(rules))}


def rlabel(tier, how):
    if tier == 1:
        return '완전 일치' if how.endswith('이름') or how.endswith('고민 칸') else how
    return {2: '묶음 이름 낱말(R12)', 3: '목적어 → 목적(R16)', 4: '목적 대상 낱말(R16)'}[tier] if '(R16)' not in how else how


def lookup(key, sites):
    """R13 — 등급 · 부위로 하나를 고른다. 부위가 있으면 그 부위(또는 상위 부위)의 노드 중 가장 가까운 것, 없으면 부위 없는 노드 + 부위 속성"""
    c = LEX.get(key)
    if not c:
        return None
    if sites:
        sc = []
        for tgt, tier, st, how in c:
            ds = [site_chain(s).index(n) for s in sites for n in st if n in site_chain(s)]
            if ds:
                sc.append((min(ds), tier, tgt, how))
        if sc:
            m = min(sc)
            hit = [x for x in sc if x[:2] == m[:2]]
            return ok([x[2] for x in hit], [rlabel(m[1], hit[0][3])] + (['부위 + 고민(R17)'] if m[0] else []), sites, note=hit[0][3])
    free = [(tier, tgt, how) for tgt, tier, st, how in c if not st]
    if free:
        m = min(x[0] for x in free)
        hit = [x for x in free if x[0] == m]
        return ok([x[1] for x in hit], [rlabel(m, hit[0][2])] + (['부위 + 고민(R17) — 그 부위 노드 없음 · 부위 속성'] if sites else []), sites, note=hit[0][2])
    if sites:
        return bad(f'부위 어긋남 — 「{key}」 노드는 {"/".join(sorted({n for _, _, st, _ in c for n in st}))} 에만 있음(부위 {"/".join(sites)})', [x[0] for x in c])
    m = min(x[1] for x in c)
    hit = [x for x in c if x[1] == m]
    return ok([x[0] for x in hit], [rlabel(m, hit[0][3])], [n for x in hit for n in x[2]], note=hit[0][3])


def with_purpose(r, sites):
    """R16 — 목적 노드에 목적 ↔ 고민 대응을 붙인다(고민 낱말을 같은 부위로 내림)"""
    if not r['ok']:
        return r
    tg, rules = list(r['target']), list(r['rules'])
    for t in r['target']:
        if t.startswith('목적:') and t[3:] in PC:
            for w in PC[t[3:]]['concern_words']:
                r2 = lookup(knorm(w), sites)
                if r2 and r2['ok']:
                    tg += r2['target']
            rules.append('목적 ↔ 고민(R16)')
    return dict(r, target=list(dict.fromkeys(tg)), rules=list(dict.fromkeys(rules)))


def apply_sev(r, sev):
    if not r['ok'] or not sev:
        return r
    tg, rules = [], list(r['rules']) + ['중증도(R18)']
    for t in r['target']:
        if t in SEV_CHILD and any(s in SEV_CHILD[t] for s in sev):
            tg.append(SEV_CHILD[t][next(s for s in sev if s in SEV_CHILD[t])])
            rules.append('중증도 → 하위(J12)')
        else:
            tg.append(t)
    return dict(r, target=list(dict.fromkeys(tg)), rules=list(dict.fromkeys(rules)), severity=list(dict.fromkeys(r['severity'] + sev)))


def cres(text, ctx=None, depth=0):
    """원천 고민 낱말 하나 → {ok, target, rules, sites, severity} 또는 {ok False, why, candidates} — R12~R20"""
    ctx = list(ctx or [])
    t = text.strip()
    pre = []
    for a, b in RENAME.items():
        if a in t:
            t = t.replace(a, b)
            pre.append('이름 치환(R1)')
    if depth > 6 or not t:
        return bad('풀 수 없음')

    def done(r, more=()):
        if r['ok']:
            return dict(r, rules=list(dict.fromkeys(pre + list(more) + r['rules'])))
        return dict(r, rules=list(dict.fromkeys(pre + list(more) + r['rules'])))
    k = knorm(t)
    if k in CWORD:  # 0. 사용자 결정 사전(여러 대상 한 묶음)
        return done(ok(CWORD[k][0], ['고민 낱말 결정(사전 · J14)'], ctx, note=CWORD[k][1]['basis']))
    # 1. 완전 · 사전
    r = lookup(k, ctx)
    if r:
        return done(with_purpose(r, ctx))
    if re.fullmatch(r'[A-Za-z_ &/\-]+', t):  # 2. 영문(R15)
        hits = EN.get(en_norm(t), [])
        kos = list(dict.fromkeys(h[0] for h in hits))
        if not kos:
            cands = sorted({ko for e, v in EN.items() for ko, _ in v if en_norm(t) in e.split()})
            cids = [i for ko in cands for i in (cres(ko, ctx, depth + 1).get('target') or [])]
            return done(bad(f'영문 「{t}」 — 원천 짝 · 외래어 사전에 없음' + (f' · 낱말이 여러 원천 짝에 걸림({" / ".join(cands)})' if cands else ''), cids))
        rs = [cres(ko, ctx, depth + 1) for ko in kos]
        if all(x['ok'] for x in rs):
            return done(ok(sum([x['target'] for x in rs], []), sum([x['rules'] for x in rs], []), sum([x['sites'] for x in rs], ctx), sum([x['severity'] for x in rs], [])), ['영문 → 한글(R15)'])
        return done(bad(f'영문 「{t}」 → {" / ".join(kos)} 을 못 풂', sum([x.get('target') or x.get('candidates') or [] for x in rs], [])))
    if norm(t) in LOAN:  # 3. 외래어(R15)
        return done(cres(LOAN[norm(t)]['to'], ctx, depth + 1), ['외래어 → 한글(R15)'])
    if norm(t) in UNIT_WORDS:  # R19
        return {'ok': True, 'target': [], 'rules': pre + ['시술 이름 — 고민 아님(R19)'], 'sites': ctx, 'severity': [], 'note': 'proc'}
    # 4. 괄호 = 풀이 · 하위
    m = re.match(r'^(.*?)\((.*?)\)(.*)$', t)
    if m:
        rm, rp = cres(m.group(1) + m.group(3), ctx, depth + 1), cres(m.group(2), ctx, depth + 1)
        if rm['ok'] and rp['ok'] and rp['target'] and rm['target'] and all(any(a in canc(x) and a != x for a in rm['target']) for x in rp['target']):
            return done(rp, ['괄호 = 하위(R18)'])
        if rm['ok'] and rm['target']:
            return done(rm, ['괄호 = 풀이'])
        if rp['ok'] and rp['target']:
            return done(rp, ['괄호 = 풀이'])
        return done(bad(f'「{t}」 본말 · 괄호 둘 다 못 풂', (rm.get('candidates') or []) + (rp.get('candidates') or [])))
    # 5. 묶음 나눔(R12)
    ps = parts_of(t)
    if len(ps) > 1:
        rs = [cres(p, ctx, depth + 1) for p in ps]
        return done(merge(ps, rs, ctx), ['묶음 나눔(R12)'])
    # 6. 꼬리말 · 머리말(R14)
    for tl in TAILS:
        if t.endswith(tl) and len(t) > len(tl):
            r2 = cres(t[:-len(tl)].strip(), ctx, depth + 1)
            if r2['ok'] and r2['target']:
                return done(r2, [f'꼬리말 「{tl}」 떼기(R14)'])
    for lw in CRU['lead_words']:
        if t.startswith(lw) and len(t) > len(lw):
            r2 = cres(t[len(lw):].strip(), ctx, depth + 1)
            if r2['ok'] and r2['target']:
                return done(r2, [f'머리말 「{lw}」 떼기(R14)'])
    # 7. 공백 나열 · 부위 + 고민 · 중증도(R12 · R17 · R18)
    toks = t.split()
    sev = [x for x in toks if x in SEV_WORDS]
    rest = [x for x in toks if x not in SEV_WORDS]
    st = list(ctx)
    words = []
    for x in rest:
        if x in SITE_WORDS and len(rest) > 1 and not (x == rest[-1] and all(y in SITE_WORDS for y in rest)):
            st.append(SITE_WORDS[x])
        elif x in CRU['lead_words'] and len(rest) > 1:
            continue
        else:
            words.append(x)
    if sev and words:
        r2 = cres(' '.join(words), st, depth + 1)
        return done(apply_sev(r2, sev), ['중증도(R18)'])
    if len(words) > 1:
        rs = [cres(w, st, depth + 1) for w in words]
        return done(merge(words, rs, st), ['공백 나열(R12)'])
    if len(rest) > 1 and words:
        r2 = cres(words[0], st, depth + 1)
        if not r2['ok'] and rest[0] in SITE_WORDS and lookup(knorm(rest[0]), []):  # R17 부위 = 대분류 이름
            return done(lookup(knorm(rest[0]), []), ['부위 = 고민 대분류 이름(R17)'])
        return done(r2, ['부위 + 고민(R17)'])
    # 8. 붙여 쓴 부위 + 말(「바디리프팅」 · 「눈밑꺼짐」)
    own = sites_in(t) + [s_ for w_, s_ in SITE_WORDS.items() if w_ in CRU['extra_site_words'] and t.startswith(w_) and s_ not in sites_in(t)]
    if own:
        rem = t
        for kk, s_ in SITE_KW + [(x, x) for x in CRU['extra_site_words']]:
            if s_ in own and kk in rem:
                rem = rem.replace(kk, ' ', 1) if kk not in AMBIG else re.sub(r'(?<![가-힣])' + kk, ' ', rem, count=1)
        rem = rem.strip()
        if rem and norm(rem) != k:
            r2 = cres(rem, ctx + own, depth + 1)
            if not r2['ok'] and any(lookup(knorm(s_), []) for s_ in own):  # R17 부위 = 대분류 이름(바디 = P12)
                s0 = next(s_ for s_ in own if lookup(knorm(s_), []))
                return done(lookup(knorm(s0), []), ['부위 = 고민 대분류 이름(R17)'])
            return done(r2, ['부위 + 고민(R17)'])
    return done(bad(f'「{t}」 — 고민 · 목적 사전에 없는 낱말'))


def merge(words, rs, sites):
    tg, rules, st, sv, cands, whys = [], [], list(sites), [], [], []
    for w, r in zip(words, rs):
        if r['ok']:
            tg += r['target']
            rules += r['rules']
            st += r['sites']
            sv += r['severity']
            cands += r['target']
        else:
            whys.append(r['why'])
            cands += r['candidates']
    if whys:
        return bad(' · '.join(whys), cands, rules)
    if not tg and rs and all(r.get('note') == 'proc' for r in rs):
        return ok([], rules + ['조각이 전부 시술 이름 — 앵커 없음(R19)'], st, sv, note='proc')
    return ok(tg, rules, st, sv)


def judge(text, ctx=None):
    """대응표 한 행 판정 — 규칙 밖(트리 밖 목적 포함)은 사람 질문(R20)"""
    r = cres(text, ctx)
    if r['ok'] and any(t in OUT_PURP for t in r['target']):  # J9 — 트리 밖 목적 = 목적 노드만 · 고민 대응 없음(사용자 10-29 규칙으로 닫음)
        r = dict(r, rules=r['rules'] + ['트리 밖 목적 = 목적 노드만(J9)'])
    if r['ok'] and not r['target'] and r.get('note') != 'proc':
        return bad('대상 없음', [], r['rules'])
    return r


UNR = {(x['source'], x['text']): x for x in DEC['concern_unresolved']}
USED_UNR = set()
corr = []
PURPOSE_IDS = {f"목적:{p['name']}" for p in DEC['purposes'] if not p['same_as_concern']}


def check_targets(row, where):
    for t in row['target']:
        if t not in CONCERN_IDS and t not in ITEM_IDS and t not in PURPOSE_IDS and t not in MENU_T:
            op('결정이 가리키는 고민 노드 없음', where=where, concern=t)


def add_rule_row(source, field, text, word, extra=None, ctx=None, pre=None):
    r = pre or judge(word, ctx)
    row = {'source': source, 'field': field, 'text': text}
    if r['ok']:
        exact_ = r['rules'] == ['완전 일치']
        row.update({'match': ' + '.join(r['rules']), 'target': r['target'], 'basis': f"규칙 — {' + '.join(r['rules'])}" + (f" · {r['note']}" if r.get('note') and r['note'] != 'proc' and r['note'] not in ' + '.join(r['rules']) else ''),
                    'human_check': False, 'rule_sites': r['sites'], 'severity': r['severity']})
        if (source, word) in UNR:
            STALE.append(['concern_unresolved', [source, word], '규칙으로 풀림'])
    else:
        d = UNR.get((source, word))
        if d is None:
            op('결정 없는 사람 질문(규칙 밖 고민 표현)', source=source, text=word, why=r['why'])
        else:
            USED_UNR.add((source, word))
        row.update({'match': '규칙 밖', 'target': [], 'basis': f"규칙 밖 — {r['why']}", 'human_check': True, 'candidates': r['candidates'],
                    'question': d['question'] if d else None, 'rule_sites': [], 'severity': []})
    if extra:
        row.update(extra)
    check_targets(row, f'{source} {text}')
    corr.append(row)
    return row


# B-1 problem-packages(P id · 이름 직결 — 원천 구조)
for P in pp['problems']:
    corr.append({'source': 'problem-packages', 'field': 'problems[].problem', 'text': P['problem'], 'match': 'P id 직결', 'target': [P['problem_id']], 'basis': 'P id 같음 · 이름 같음', 'human_check': False})
    for c in P['complaints']:
        cands = [x for x in items if x['category'] == P['problem_id'] and x['name'] == c['cc']]
        if len(cands) > 1:
            cands = [x for x in cands if x['detail'] == c['cc_detail'] or c['cc_detail'].startswith(x['detail'].split('.')[0][:4])] or cands
        tgt = [x['id'] for x in cands]
        same_detail = bool(cands) and cands[0]['detail'] == c['cc_detail']
        corr.append({'source': 'problem-packages', 'field': 'complaints[].cc', 'text': f"{c['cc']} [{c['cc_detail']}]", 'cc_group': c['cc_group'],
                     'match': '완전 일치' if tgt else '대응 없음', 'target': tgt,
                     'basis': ('같은 P id · 이름 일치' + ('' if same_detail else ' · detail 다름(원천 detail 이 길어짐 — 안전 문구)')) if tgt else 'taxonomy 항목에 없음',
                     'human_check': not tgt})
        if not tgt:
            op('대응 없는 CC', problem=P['problem_id'], cc=c['cc'])
covered = {t for r in corr if r['field'] == 'complaints[].cc' for t in r['target']}
for it in items:
    if it['id'] not in covered:
        corr.append({'source': 'problem-packages', 'field': '(역방향) taxonomy 항목에 CC 없음', 'text': it['name'], 'match': 'CC 없음', 'target': [it['id']], 'basis': 'problem-packages 에 이 항목의 CC 가 없음 — CC 엣지(③) 없음 · 항목은 그대로', 'human_check': False})
for P in pp['problems']:
    labs = {s['source_label'] for s in subs if s['parent'] == P['problem_id']}
    for g in sorted({c['cc_group'] for c in P['complaints']}):
        if g not in labs:
            op('중분류와 다른 CC 묶음 이름', problem=P['problem_id'], cc_group=g)
# B-2 problem-combos — P1 은 J5(앵커 없음) · 나머지는 이름을 규칙으로(묶음 이름 → 낱말마다)
PCX = {}
for c in pc['combos']:
    if c['problem_id'] == 'P1':
        row = add_rule_row('problem-combos', 'combos[].problem', c['problem'], c['problem'], {'problem_id': c['problem_id']},
                           pre={'ok': True, 'target': [], 'rules': ['J5 — 쁘띠시술 = 고민 앵커 없음(메뉴 이름 원문)'], 'sites': [], 'severity': [], 'note': None})
    else:
        row = add_rule_row('problem-combos', 'combos[].problem', c['problem'], c['problem'], {'problem_id': c['problem_id']})
        if row['target'] and c['problem_id'] not in row['target']:
            op('problem-combos P id 가 규칙 대응에 없음', problem=c['problem_id'], text=c['problem'], target=row['target'])
    PCX[c['problem_id']] = row['target']
# B-3 최적화 고민
OPT = {}
for c in to['by_concern']:
    OPT[c['concern']] = add_rule_row('treatment-optimization', 'by_concern[].concern', c['concern'], c['concern'], {'en': c['concern_en']})['target']
# B-4 synergy target
cnt = C(l.get('target') for l in syn['links'])
for t, n in cnt.items():
    add_rule_row('synergy', 'links[].target', t, t, {'links': n})
# B-5 recipe goal
GOAL = {}
for g in sorted({r['goal'] for r in cr['recipes']}):
    GOAL[g] = add_rule_row('combo-recipes', 'recipes[].goal', g, g, {'recipes': [r['id'] for r in cr['recipes'] if r['goal'] == g]})['target']
# B-6 비교 — 제목
CMPM = {}
for c in cmp_['comparisons']:
    CMPM[c['id']] = add_rule_row('procedure-comparison', 'comparisons[].id · title', f"{c['id']} / {c['title']}", c['title'], {'subtitle': c['subtitle']})['target']
# B-7 연령 주 고민
seen = []
for a in to['by_age_group']:
    for pcn in a['primary_concerns']:
        if pcn in seen:
            continue
        seen.append(pcn)
        add_rule_row('treatment-optimization', 'by_age_group[].primary_concerns', pcn, pcn, {'ages': [x['age'] for x in to['by_age_group'] if pcn in x['primary_concerns']]})
# B-8 3단계 넘김 + 이름 칸 고민 조각 — 원 문자열 먼저(부위 = 3단계 nodes), 안 풀리면 3단계가 적은 조각
S3N = {x['string']: x for x in s3['strings']}


def s3_judge(string, part):
    nodes = (S3N.get(string) or {}).get('nodes') or []
    r = judge(string, nodes)
    if r['ok'] and r['target']:  # 원 문자열이 시술 이름(「다크서클필러」 · 「등살주사」)이면 3단계 조각으로
        return dict(r, rules=['3단계 원 문자열'] + r['rules'])
    r2 = judge(part, nodes)
    rwhy = r.get('why') or '시술 이름 — 고민 아님(R19)'
    return dict(r2, rules=['3단계 조각'] + r2['rules']) if r2['ok'] else dict(r2, why=f"원 문자열 「{string.strip()}」: {rwhy} / 조각 「{part}」: {r2['why']}", candidates=list(dict.fromkeys((r.get('candidates') or []) + r2['candidates'])))


for d0 in s3['deferred']:
    if d0['stage'] != '7단계 고민':
        continue
    add_rule_row('step3 deferred', 'deferred[].string', d0['string'], d0['string'], {'count': d0['count'], 'part': d0['parts'][0]['part']}, pre=s3_judge(d0['string'], d0['parts'][0]['part']))
for x in s3['strings']:
    for h in x.get('handoff') or []:
        if '7' not in str(h.get('stage', '')):
            continue
        add_rule_row('step3 strings handoff', 'strings[].handoff', f"{x['string']} → {h['part']}", f"{x['string']} → {h['part']}", pre=s3_judge(x['string'], h['part']))
# B-9 6단계 메뉴 분류(7단계 넘김)
for npk in s6['non_packages']:
    if not npk['to'].startswith('7단계'):
        continue
    add_rule_row('step6 non_packages', 'menu label', f"{npk['id']} {npk['label']}", npk['label'])
STALE += [['concern_unresolved', list(k)] for k in UNR if k not in USED_UNR and k not in [tuple(s[1]) for s in STALE if s[0] == 'concern_unresolved']]

for r in corr:
    if r['human_check']:
        r['match_class'] = '규칙 밖(사람 질문)'
        r['gate_status'] = '사람 질문(규칙 밖)'
        r['gate_initial'] = list(r.get('candidates') or [])
        r['gate_note'] = 'R20 — 규칙으로 하나로 안 정해짐 · 후보만 적음(추천값 아님)'
    elif r['match'] in ('완전 일치', 'P id 직결', 'CC 없음'):
        r['match_class'] = '완전 일치'
        r['gate_status'] = '자동(완전 일치)'
    else:
        ids = sorted(set(re.findall(r'\b(R\d+|J\d+)\b', r['match'])), key=lambda x: (x[0], int(x[1:])))
        r['match_class'] = '규칙 ' + ' · '.join(ids or ['3단계 원 문자열 = 완전 일치' if '완전 일치' in r['match'] else r['match']])
        r['gate_status'] = '자동(규칙)'

ID2NAMES = collections.defaultdict(set)
for c in cats:
    ID2NAMES[c['id']] |= {norm(c['name']), norm(c['source_name'])}
for s in subs:
    ID2NAMES[s['id']] |= {norm(s['source_label'])} | ({norm(s['concern'])} if s.get('concern') else set())
for it in items + extra_items:
    ID2NAMES[it['id']].add(norm(it['name']))
for p in DEC['purposes']:
    ID2NAMES[f"목적:{p['name']}"].add(norm(p['name']))


def src_word(r):
    t = r['text']
    if r['field'] == 'complaints[].cc':
        return t.split(' [')[0]
    if r['field'] == 'comparisons[].id · title':
        return t.split(' / ', 1)[1]
    if r['source'] == 'step3 strings handoff':
        return t.split(' → ', 1)[1]
    if r['source'] == 'step6 non_packages':
        return t.split(' ', 1)[1]
    return t


# 자동 행 가드(검수 F1 → 규칙판) — 「완전 일치」라고 적힌 자동 행은 원천 말 == 대상 이름이어야 · 규칙 자동 행은 대상이 있어야(J5 · R19 빼고)
for r in corr:
    r['source_word'] = src_word(r)
    r['exact_name'] = bool(r['target']) and all(norm(r['source_word']) in ID2NAMES[t] for t in r['target'])
    if r['gate_status'] == '자동(완전 일치)' and r['source'] not in ('problem-packages',) and r['match'] != 'P id 직결' and not r['exact_name']:
        op('자동 대응인데 원천 말 ≠ 대상 이름', source=r['source'], text=r['text'], target=r['target'], match=r['match'])
    if r['gate_status'] == '자동(규칙)' and not r['target'] and 'J5' not in r['match'] and 'R19' not in r['match']:
        op('규칙 자동 대응인데 대상 없음', source=r['source'], text=r['text'], match=r['match'])


# ───────── C. 목적 ─────────
purposes = []
PNAMES = set()
alias_src = collections.defaultdict(set)
for p in DEC['purposes']:
    s = p['same_as_concern']
    if s and s not in CONCERN_IDS:
        op('결정이 가리키는 고민 노드 없음', where=f"purposes {p['name']}", concern=s)
    PNAMES.add(p['name'])
    for a in p['aliases']:
        alias_src[(a['source'], a['text'])].add(p['name'])
    purposes.append({'name': p['name'], 'from': p['from'], 'same_as_concern': s, 'kind': p['kind'], 'node': s is None, 'aliases': p['aliases']})
expr = set()
for u in s5['units']:
    for p in u['purposes']:
        expr.add(('5단계 purposes', p))
pe = collections.defaultdict(set)
for x in s5['rules']['product_link']['technique_compat']['product_evidence']:
    for e in x['evidence']:
        expr.add(('5단계 목적 키', e['purpose']))
        for uu_ in x['units']:
            for k in DEC['product_evidence_purpose_units']:
                if e['purpose'] == k['purpose'] and uu_ in k['units']:
                    pe[e['purpose']].add(uu_)
for npk in s6['non_packages']:
    if npk['to'].startswith('7단계'):
        expr.add(('6단계 메뉴 분류', npk['label']))
for s in subs:
    if s['purpose']:
        expr.add(('중분류 목적', s['purpose']))
for w in DEC['p1_detail_words']['purpose']:
    expr.add(('P1 detail 목적 낱말', w))
for e in sorted(expr):
    if e not in alias_src:
        op('결정 없는 목적 표현', source=e[0], text=e[1])
STALE += [['purposes.aliases', list(k)] for k in alias_src if k not in expr]
for w, pn in DEC['p1_detail_words']['purpose'].items():
    if pn not in PNAMES:
        op('결정이 가리키는 목적 없음', where=f'p1_detail_words {w}', purpose=pn)
for sp, pn in PMAP.items():
    if pn not in PNAMES:
        op('결정이 가리키는 목적 없음', where=f'purpose_map_from_sub {sp}', purpose=pn)


def purpose_of(source, text):
    return sorted(alias_src.get((source, text), []))


# ───────── C-2. 엣지(원천 구조만) ─────────
edges = []


def E(src, frm, to_units, to_family, basis, status, evidence=None, src_id=None, purpose=None, sites=None, flag=None, site_layer=None):
    edges.append({'source': src, 'source_id': src_id, 'from': frm, 'purpose_nodes': purpose, 'to_units': to_units, 'to_family': to_family, 'lowering': status, 'basis': basis, 'evidence': evidence,
                  'anchor_sites': list(dict.fromkeys(sites or [])), 'resolve_flag': flag, 'site_layer': site_layer,
                  'target_kind': '단위 시술' if to_units else ('계열만' if to_family else '대상 없음')})


for it in items:
    if it['kind'] in ('고민', '부위'):
        frm = anchor_of(it)
        for f in it['modality_ref']:
            us = it['modality_lowered'].get(f) or []
            st = '부위로 내림' if us else ('이 부위 단위 시술 없음 · 계열만' if it['sites'] else '부위 없음 → 계열')
            lay = None
            if not us and it['sites']:  # R21 — 부위 트리 상위로 올라가 찾음 · 없으면 계열만(W2 「후보 전부」 대체)
                us, lay = climb([f], it['sites'])
                if us:
                    st = f'상위 부위로 내림({lay})'
            E('① taxonomy modality_ref', frm, us, f, f"항목 {it['name']} → {f} × 부위 {'/'.join(it['sites']) or '없음'}" + (f' → 상위 부위 {lay} 층(R21)' if lay else ''), st, src_id=it['id'], sites=it['sites'],
              flag='no_unit_at_site' if '계열만' in st else None, site_layer=lay)
    elif it['kind'] == '시술 이름' and it['category'] != 'P1':
        frm = anchor_of(it)
        r = it['resolve']
        st5 = r['status']
        uf5 = sorted({UNITS[u]['key']['family'] for u in r['units']})
        if r['units'] and it['modality_ref'] and not set(uf5) & set(it['modality_ref']):  # 검수 W1 — R7 · O13 같은 표시(CC · 비교와 같게)
            st5 += f" · 계열 코드 어긋남(원천 {'/'.join(it['modality_ref'])} ↔ 단위 시술 {'/'.join(uf5)})"
        E('⑤ taxonomy 항목 = 시술 이름', frm, r['units'], (it['modality_ref'] or r.get('families') or [None])[0], f"항목 이름 「{it['name']}」 → {r['basis']}", st5, src_id=it['id'], sites=(it['sites'] or []) + sites_in(it['name']) + sites_in(it['detail']), flag=r.get('flag'), site_layer=r.get('site_layer'))
    elif it['kind'] == '시술 이름' and it['category'] == 'P1':
        det = it['detail']
        for w, tgt in DEC['p1_detail_words']['concern'].items():
            if w in det:
                E('① P1 detail 고민 낱말', tgt, it['resolve']['units'], None, f"P1 「{it['name']} [{det}]」 — detail 의 고민 낱말", '이름 일치', src_id=it['id'])
        for w, pn in DEC['p1_detail_words']['purpose'].items():
            if w in det:
                E('① P1 detail 목적 낱말', f'목적:{pn}', it['resolve']['units'], None, f"P1 「{it['name']} [{det}]」 — detail 의 목적 낱말", '이름 일치', src_id=it['id'], purpose=[pn])
# ③ CC 추천 시술
for P in pp['problems']:
    for c in P['complaints']:
        cands = [x for x in items if x['category'] == P['problem_id'] and x['name'] == c['cc']]
        if not cands:
            continue
        it = cands[0]
        for pr in c['procedures']:
            fam = pr.get('category')
            sites_ = it['sites'] or SUBD.get(it['subcategory'], {}).get('sites') or []
            r = comp_one(pr['name'], sites_ or None, pr.get('products'))
            fu = set(units_of([fam])) if fam else set()
            in_fam = [u for u in r['units'] if u in fu]
            lay = r.get('site_layer') if r['units'] else None
            if r['status'].startswith('단위 시술 없음') or r['status'] == '시술 아님':
                us, st = [], r['status'] + ' — ' + r['basis']
            elif in_fam:
                us, st = in_fam, r['status']
            elif r['units']:
                us, st = r['units'], r['status'] + f' · 계열 코드 어긋남(원천 {fam} ↔ 단위 시술 ' + '/'.join(sorted({UNITS[u]["key"]["family"] for u in r["units"]})) + ')'
            elif sites_:
                us = units_at([fam], sites_)
                st = '부위로 내림(계열 코드)' if us else '이 부위 단위 시술 없음 · 계열만(계열 코드)'
                if not us:  # R21 — 부위 트리 상위로 올라가 찾음 · 없으면 계열만(W2 「후보 전부」 대체)
                    us, lay = climb([fam], sites_)
                    if us:
                        st = f'상위 부위로 내림({lay} · 계열 코드)'
            else:
                us, st = [], '부위 없음 → 계열(결정 ③)'
            E('③ problem-packages CC 추천 시술', anchor_of(it), us, fam, f"CC {c['cc']} → {pr['name']}({fam})" + (f' → 상위 부위 {lay} 층(R21)' if lay else ''), st, evidence={'name': pr['name'], 'role': pr.get('role'), 'products': pr.get('products')}, src_id=f"{P['problem_id']}:{c['cc']}", sites=sites_ + sites_in(pr['name']), flag='no_unit_at_site' if '계열만' in st else r.get('flag'), site_layer=lay)
# R27 겹친 엣지 합치기(사용자 10-30) — 원천이 갈래(cc_group) 목록을 그 갈래 CC 전부에 복사 → (갈래 앵커 × 원천 시술 · 계열 · 단위 시술 · 앵커 부위) 하나
_m27, _keep = {}, []
R27_GROUPS = []
for e in edges:
    if not e['source'].startswith('③'):
        _keep.append(e)
        continue
    k27 = (e['from'], (e['evidence'] or {}).get('name'), e['to_family'], tuple(e['to_units']), tuple(e['anchor_sites']), e['lowering'])
    cc_ = e['source_id'].split(':', 1)[1]
    if k27 in _m27:
        h = _m27[k27]
        h['source_ids'].append(e['source_id'])
        h['evidence']['ccs'].append(cc_)
        continue
    _m27[k27] = e
    e['source_ids'] = [e['source_id']]
    e['evidence']['ccs'] = [cc_]
    _keep.append(e)
for e in _m27.values():
    lab = (SUBX.get(e['from']) or {}).get('source_label') or (CATX.get(e['from']) or {}).get('name') or next((i['name'] for i in items if i['id'] == e['from']), e['from'])
    tail = e['basis'][e['basis'].find(' → 상위 부위'):] if ' → 상위 부위' in e['basis'] else ''
    e['basis'] = f"갈래 {lab} 추천 시술 {e['evidence']['name']}({e['to_family']}) · CC {' · '.join(e['evidence']['ccs'])}" + tail
    if len(e['source_ids']) > 1:
        R27_GROUPS.append({'from': e['from'], 'group': lab, 'procedure': e['evidence']['name'], 'family': e['to_family'], 'ccs': list(e['evidence']['ccs'])})
edges[:] = _keep
# ② problem-combos(결정: 계열로) — 고민은 대응표 B-2 규칙 대상마다(묶음 이름 → 낱말마다 · R12)
for c in pc['combos']:
    fams = sorted({f for p in c['packages'] for f in p['procedures']})
    for frm in (PCX.get(c['problem_id']) or ['(P1 — 고민 앵커 없음)']):
        for f in fams:
            E('② problem-combos', frm, [], f, '결정대로 계열 단위(SPEC-004 ②)' + (f" · 원천 이름 「{c['problem']}」 → 규칙 대상" if frm != c['problem_id'] else ''), '계열(결정)', src_id=c['problem_id'])
def lev_anchor(concern, level):
    """R18 — 최적화 severity_levels 의 고민 앵커: 주름은 중증도 → 하위(J12) · 다른 고민은 단계 이름 괄호 낱말이 그 고민 아래 노드를 가리키면 그 노드 · 아니면 상위 + severity"""
    anc = OPT.get(concern, [])
    sev = level.split()[0]
    if any(a in SEV_CHILD for a in anc):
        return {'concern': list(dict.fromkeys(SEV_CHILD[a].get(sev, a) if a in SEV_CHILD else a for a in anc)), 'severity': sev, 'rule': '중증도 → 하위(R18 · J12)'}
    sub = {i for i in CONCERN_IDS if any(a in canc(i) for a in anc)}
    m = re.search(r'\((.*)\)', level)
    hits = []
    if m and sub:
        txt = knorm(m.group(1)).replace('/', '')
        keys = sorted({k for k, v in LEX.items() if '/' not in k and any(t_ in sub and tr <= 2 for t_, tr, _, _ in v)}, key=lambda k: (-len(k), k))
        i = 0
        while i < len(txt):
            k = next((k for k in keys if txt.startswith(k, i)), None)
            if not k:
                i += 1
                continue
            r_ = lookup(k, [])  # R13 — 부위 없는 말은 부위 없는 노드 먼저
            hits += [t_ for t_ in (r_['target'] if r_ and r_['ok'] else []) if t_ in sub]
            i += len(k)
    if hits and set(hits) - set(anc):
        return {'concern': list(dict.fromkeys(hits)), 'severity': sev, 'rule': '단계 이름 낱말 → 그 고민 아래 노드(R18)'}
    if hits:
        return {'concern': list(dict.fromkeys(hits)), 'severity': sev, 'rule': '단계 이름 낱말 = 그 고민 — 중증도 하위 없음 · 상위 + severity(R18)'}
    return {'concern': list(anc), 'severity': sev, 'rule': '중증도 하위 없음 — 상위 + severity(R18)'}


# ④ 최적화
for c in to['by_concern']:
    cx, pu = ctx_of('treatment-optimization', c['concern'])
    for s in c['severity_levels']:
        for nm in s['optimal_combo']:
            r = comp_one(nm, cx, purpose=pu)
            E('④ treatment-optimization optimal_combo', f"opt:{c['concern']}", r['units'], None if r['units'] else '/'.join(r.get('families') or []) or None, f"{s['level']} · 「{nm}」 → {r['basis']}", r['status'], evidence={'severity': s['level'], 'evidence_level': s.get('evidence_level')}, src_id=f"{c['concern']}|{s['level']}", sites=(cx or []) + sites_in(nm), flag=r.get('flag'), site_layer=r.get('site_layer'))
            la = lev_anchor(c['concern'], s['level'])
            edges[-1].update(from_concerns=la['concern'], severity=la['severity'], severity_rule=la['rule'])
# ⑧ 결정 노드 → 단위 시술(사용자 결정 — 잇몸미소 → U5-013 잇몸 보톡스)
for x in extra_items:
    for u in x.get('units') or []:
        if u not in UNITS:
            op('결정이 가리키는 단위 시술 없음', where=f"extra_concern_items {x['id']}", unit=u)
            continue
        E('⑧ 결정 노드 → 단위 시술', x['id'], [u], UNITS[u]['key']['family'], f"{x['id']} → {u} {UN[u]} — {x.get('units_basis') or x['basis']}", '단위 시술 직결', src_id=x['id'], sites=x['sites'])
# ⑥ 5단계 purposes · 목적 키
for u in s5['units']:
    for p in u['purposes']:
        E('⑥ 5단계 units[].purposes(원장 용도)', f"목적:{p}", [u['id']], u['key']['family'], f"{u['id']} {u['name']} purposes", '단위 시술 직결', src_id=u['id'], purpose=purpose_of('5단계 purposes', p))
for p, us in pe.items():
    E('⑥ 5단계 목적 키(제품 출처)', f"목적:{p}", sorted(us), 'M8', '5단계 technique_compat.product_evidence', '단위 시술 직결', purpose=purpose_of('5단계 목적 키', p))
# ⑦ 메뉴 분류(6단계 → 7단계 목적 원문)
LED = s5['ledger']
PL = {p['product']: p for p in s5['product_links']}
for npk in s6['non_packages']:
    if not npk['to'].startswith('7단계'):
        continue
    us = set()
    for r in LED:
        if r.get('source_sub') != npk['id']:
            continue
        us |= set(r.get('units') or [])
        if r.get('product') and r['product'] in PL:
            us |= set(PL[r['product']].get('stored_units') or [])
    note7 = ''
    if not us and npk['label'] in pe:
        us = set(pe[npk['label']])
        note7 = f" · 안 항목이 전부 제품 → 5단계 목적 키 「{npk['label']}」(제품 출처) 단위 시술"
    E('⑦ 원장 메뉴 분류(6단계 넘김)', f"목적:{npk['label']}", sorted(us), npk['family'], f"원장 {npk['id']} 안 항목의 단위 시술(저장 연결만 · 상속 후보 제외)" + note7, '단위 시술 직결' if us else '단위 시술 없음(제품만 — 상속 후보는 조회 때)', src_id=npk['id'], purpose=purpose_of('6단계 메뉴 분류', npk['label']))

# 고민 영역(R22 · 사용자 10-30) — 앵커 부위가 없는 엣지 · 추천 조합 구성은 고민의 영역으로 거른다.
# 고민의 영역 = 그 고민(과 하위 고민 · 항목)의 앵커 부위들의 최상위 영역 합집합(3단계 트리에서 계산). 갈래가 「목적」뿐인 중분류(P4-3 전신항노화 등)와 그 항목은 고민이 아니라 넣지 않는다.
# 하위 부위가 하나도 없어 영역을 못 정하는 고민은 손대지 않고 셈만(따로 검수).
CREG = collections.defaultdict(set)
_SUBK = {x['id']: x for x in subs}


def _creg_add(ids, sites_):
    for s_ in sites_:
        r_ = region('얼굴 전체' if s_ == '얼굴' else s_)
        if r_:
            for i_ in ids:
                CREG[i_].add(r_)


for x in subs:
    if x['kind'] != '목적':
        _creg_add([x['id'], x['parent']], x['sites'])
for i in items:
    k_ = _SUBK.get(i['subcategory'])
    if k_ and k_['kind'] != '목적':
        _creg_add([i['id'], i['subcategory'], i['category']], i['sites'])
for x in extra_items:
    _creg_add([x['id']] + ([x['parent']] if x['parent'] else []), x['sites'])


# 판단 ①(사용자 10-30) — 영역 없는 피부 고민의 기본 영역(site_rules.concern_region_default) · R26 튼살 = 바디. 그 노드 · 하위가 영역이 없을 때만 · 위로 올리지 않음
CPAR = {x['id']: x['parent'] for x in subs}
CPAR.update({i['id']: i['subcategory'] for i in items})
CPAR.update({x['id']: x['parent'] for x in extra_items})
CNAME = {x['id']: x['name'] for x in cats}
CNAME.update({x['id']: x['source_label'] for x in subs})
CNAME.update({i['id']: i['name'] for i in items})
CNAME.update({x['id']: x['name'] for x in extra_items})
CDEF = {i_: r_ for r_, ids in DEC['site_rules']['concern_region_default']['regions'].items() for i_ in ids}
for i_ in CDEF:
    if i_ not in CNAME:
        op('결정이 가리키는 고민 노드 없음', where='site_rules.concern_region_default', concern=i_)
CREG_DEFAULT = {}
for i_ in sorted(CNAME):
    if CREG.get(i_):
        continue
    a_ = i_
    while a_ and a_ not in CDEF:
        a_ = CPAR.get(a_)
    if a_:
        CREG_DEFAULT[i_] = CDEF[a_]
for i_, r_ in CREG_DEFAULT.items():
    CREG[i_].add(r_)


def concern_regions(cs):
    return set().union(*[CREG.get(c_, set()) for c_ in cs]) if cs else set()


# R23 용도 낱말 — 고민(과 위 고민) 이름 · 목적 이름 · 목적의 5단계 purposes 별칭
PURP_ALIAS = collections.defaultdict(set)
for p_ in purposes:
    for a_ in p_.get('aliases') or []:
        if a_['source'] == '5단계 purposes':
            PURP_ALIAS[p_['name']].add(a_['text'])


def concern_words(cs):
    w_ = set()
    for c_ in cs:
        if c_.startswith('목적:'):
            names = [c_[3:]] + sorted(PURP_ALIAS.get(c_[3:], ()))
        else:
            names, a_ = [], c_
            while a_:
                if a_ in CNAME:
                    names.append(CNAME[a_])
                a_ = CPAR.get(a_)
        for n_ in names:
            w_ |= {t_ for t_ in re.split(r'[\s/·,()]+', n_) if len(t_) >= 2}
    return w_


SCAR = set(DEC['site_rules']['scar_filler']['concerns'])
SCAR_FAM = DEC['site_rules']['scar_filler']['family']
NARROW_SRC = tuple(DEC['site_rules']['narrow_sources'])


def is_scar(cs):
    cc_ = [c_ for c_ in cs if not c_.startswith('목적:')]
    def up(c_):
        while c_:
            if c_ in SCAR:
                return True
            c_ = CPAR.get(c_)
        return False
    return bool(cc_) and all(up(c_) for c_ in cc_)


def empty_note(keep, cut):
    if keep:
        return ''
    return ' → 계열만' if not any(cut.get(k_) for k_ in ('R22', 'R25', 'R26')) else ' → 이 부위 단위 시술 없음 · 계열만'


def narrow(units, status, cs):
    """앵커 부위 없는 엣지 · 조합 구성 — R23 용도 → R22 고민 영역(+ 판단 ① 기본 영역) → R25 두피 → R26 흉터 필러. 반환 (남김, {규칙: 뺀 것}, 영역, 메모)"""
    u_, cut, notes = list(units), {}, []
    w_ = concern_words(cs)
    if len(u_) > 1 and any(UNITS[x]['purposes'] and not any(any(p_ in t_ for t_ in w_) for p_ in UNITS[x]['purposes']) for x in u_):  # 다른 고민 용도가 박힌 단위 시술이 섞인 여럿
        m_ = [x for x in u_ if any(any(p_ in t_ for t_ in w_) for p_ in UNITS[x]['purposes'])]
        cut['R23'] = [x for x in u_ if x not in m_]
        u_ = m_
        hit = sorted({p_ for x in m_ for p_ in UNITS[x]['purposes'] if any(p_ in t_ for t_ in w_)})
        notes.append(f"용도 「{'/'.join(hit)}」로 좁힘(R23)" if m_ else '고민 · 목적과 맞는 용도 단위 시술 없음(R23)')
    rs = concern_regions(cs)
    if rs:
        o_ = [x for x in u_ if UNITS[x]['key']['site'] not in SITE_FREE and region(UNITS[x]['key']['site']) not in rs]
        if o_:
            cut['R22'] = o_
            u_ = [x for x in u_ if x not in o_]
            notes.append(f"고민 영역({'/'.join(sorted(rs))}) 밖 {len(o_)} 뺌(R22" + (' · 기본 영역 판단 ①)' if any(c_ in CREG_DEFAULT for c_ in cs) else ')'))
    if '두피' not in rs:
        o_ = [x for x in u_ if region(UNITS[x]['key']['site']) == '두피']
        if o_:
            cut['R25'] = o_
            u_ = [x for x in u_ if x not in o_]
            notes.append(f'두피 단위 시술 {len(o_)} 뺌 — 두피 고민 아님(R25)')
    if is_scar(cs):
        o_ = [x for x in u_ if UNITS[x]['key']['family'] == SCAR_FAM]
        if o_:
            cut['R26'] = o_
            u_ = [x for x in u_ if x not in o_]
            notes.append('흉터 필러 단위 시술 없음 → 필러 계열만(R26 · 원천 질문)')
    return u_, cut, rs, notes


def region_cut(units, cs):
    """(남길 단위 시술, 뺀 단위 시술, 영역) — 영역 없으면 (units, [], set())"""
    rs = concern_regions(cs)
    if not rs:
        return list(units), [], rs
    out = [u for u in units if UNITS[u]['key']['site'] not in SITE_FREE and region(UNITS[u]['key']['site']) not in rs]
    return [u for u in units if u not in out], out, rs


SCAR_HITS = []
for e in edges:
    cs = e.get('from_concerns') or [e['from']]
    rs = concern_regions(cs)
    e['concern_regions'] = sorted(rs)
    if e['anchor_sites'] or not e['to_units'] or not e['source'].startswith(NARROW_SRC):
        continue
    keep, cut, rs, notes = narrow(e['to_units'], e['lowering'] + ' ' + e['basis'], cs)
    if not rs:
        e['concern_region_check'] = '고민 영역 없음(R22 · 셈만)' if any(c_ in CREG or c_ in _SUBK or c_ in CATX or c_ in {i['id'] for i in items} for c_ in cs) else '고민 아님(R22 밖)'
    else:
        e['concern_region_check'] = (f"고민 영역 밖 {len(cut['R22'])} 뺌(R22)" if cut.get('R22') else '고민 영역 안(R22)') + (' · 기본 영역(판단 ①)' if any(c_ in CREG_DEFAULT for c_ in cs) else '')
    if cut.get('R22'):
        e['concern_region_dropped'] = cut['R22']
    if cut:
        e['narrow_dropped'] = {k_: v_ for k_, v_ in cut.items() if v_}
        if not e['to_family']:
            fs = sorted({UNITS[u]['key']['family'] for v_ in cut.values() for u in v_})
            e['to_family'] = fs[0] if len(fs) == 1 else '/'.join(fs)
        e['to_units'] = keep
        e['lowering'] += ' · ' + ' · '.join(notes) + empty_note(keep, cut)
        e['target_kind'] = '단위 시술' if keep else ('계열만' if e['to_family'] else '대상 없음')
        if cut.get('R26'):
            SCAR_HITS.append(f"엣지 {e['source'][:1]} {e['from']} · {e['basis'][:60]}")

# 엣지 앵커 부위 검사(검수 F2 같은 성격 전수 · R21) — 단위 시술 부위 ∈ 앵커 부위(또는 하위) 또는 올라간 층(조상 노드 자신 · 영역 「전체」 노드) ·
# 부위 무관 특수 부위는 통과 · 앵커 부위 없음 = 검사 밖. 단위 시술 부위의 최상위 영역 ≠ 앵커 부위의 최상위 영역이면 open(영역 넘음)
for e in edges:
    if not e['anchor_sites'] or not e['to_units']:
        e['site_check'] = '앵커 부위 없음' if not e['anchor_sites'] else ('이 부위 단위 시술 없음 · 계열만' if 'no_unit_at_site' in (e['resolve_flag'] or '') else '단위 시술 없음')
        continue
    want = want_sites(e['anchor_sites'])
    up = {x for s_ in e['anchor_sites'] for x in layers_of(s_)}
    regs = anchor_regions(e['anchor_sites'])
    cross = [u for u in e['to_units'] if UNITS[u]['key']['site'] not in SITE_FREE and region(UNITS[u]['key']['site']) not in regs]
    out_ = [u for u in e['to_units'] if UNITS[u]['key']['site'] not in want | up and UNITS[u]['key']['site'] not in SITE_FREE]
    hi = [u for u in e['to_units'] if UNITS[u]['key']['site'] in up - want]
    e['site_check'] = '영역 넘음' if cross else ('부위 밖' if out_ else (f"상위 부위 {e['site_layer'] or '/'.join(sorted({UNITS[u]['key']['site'] for u in hi}))}" if hi else '부위 안'))
    if cross:
        op('엣지 단위 시술이 앵커 부위의 최상위 영역 밖', source=e['source'], source_id=e['source_id'], sites=e['anchor_sites'], regions=sorted(regs), units=cross)
    elif out_:
        op('엣지 단위 시술이 앵커 부위 밖', source=e['source'], source_id=e['source_id'], sites=e['anchor_sites'], units=out_)
for e in edges:  # R22 가드 — 고민 영역이 계산되는 고민인데 단위 시술이 영역 밖이면 open
    rs = set(e['concern_regions'])
    if rs:
        bad22 = [u for u in e["to_units"] if UNITS[u]['key']['site'] not in SITE_FREE and region(UNITS[u]['key']['site']) not in rs]
        if bad22:
            op('엣지 단위 시술이 고민 영역 밖', source=e['source'], source_id=e['source_id'], regions=sorted(rs), units=bad22)

# ───────── D. 추천 조합 ─────────
combos = []
FAM_NAME = {m['id']: m.get('category') or m.get('name') for m in tax['modality']}
TIER = DEC['tier_label_site']
for c in pc['combos']:
    for p in c['packages']:
        prods = [x.strip() for x in re.split(r'\+| or |/|또는|\(|\)', ' '.join(p['products'])) if x.strip()]
        parts = []
        name_parts = [x.strip() for x in re.split(r'\+', re.sub(r'\(.*?\)', '', p['name'])) if x.strip()]
        for f in p['procedures']:
            hit = []
            for npt in name_parts:
                r_ = resolve(re.sub(r'^(수입|국산)\s*', '', npt))
                fu = [u for u in r_['units'] if UNITS[u]['key']['family'] == f]
                if fu and len(fu) < len(units_of([f])):
                    hit.append((npt, fu))
            if hit:
                us = sorted({u for _, fu in hit for u in fu})
                parts.append({'family': f, 'family_name': FAM_NAME.get(f), 'status': '이름으로 내림' if len(us) == 1 else '이름으로 좁힘 · 후보 여럿', 'units': us, 'basis': '패키지 이름 조각 ' + ' · '.join(f'「{a}」' for a, _ in hit), 'flag': None if len(us) == 1 else 'ambiguous'})
                continue
            pu = set()
            for x in prods:
                pu |= PROD.get(norm(x), set()) | SYN.get(norm(x), set())
            allf = units_of([f])
            nar = [u for u in allf if u in pu]
            if nar and len(nar) < len(allf):
                parts.append({'family': f, 'family_name': FAM_NAME.get(f), 'status': '제품으로 좁힘' if len(nar) > 1 else '제품으로 내림', 'units': nar, 'basis': '원천 제품 칸 이름 → 5단계 제품 연결', 'flag': 'ambiguous' if len(nar) > 1 else None})
            else:
                parts.append({'family': f, 'family_name': FAM_NAME.get(f), 'status': '후보 전부', 'units': allf, 'basis': '고민(대분류)에 부위 없음 · 이름 · 제품으로 못 좁힘', 'flag': 'concern_without_site'})
        if p['tier'] not in TIER:
            op('결정 없는 추천 조합 등급', combo=p['id'], tier=p['tier'])
        combos.append({'id': f"RC-PC-{p['id']}", 'kind': '고민 패키지(사이트 「추천 패키지」)', 'source': 'problem-combos', 'source_id': p['id'],
                       'anchor': {'concern': c['problem_id'] if c['problem_id'] != 'P1' else None, 'concerns': PCX.get(c['problem_id']) or [], 'source_label': c['problem'], 'note': DEC['p1_combo_anchor_note'] if c['problem_id'] == 'P1' else None},
                       'name': p['name'], 'tier': p['tier'], 'tier_label_source': p['tierLabel'], 'tier_label_site': TIER.get(p['tier']),
                       'components': parts, 'product_tier': p['productTier'], 'products_text': p['products'], 'price': p['priceRange'],
                       'effect': {'expectedResult': p['expectedResult'], 'clinicalRationale': p['clinicalRationale'], 'riskBenefit': p['riskBenefit']},
                       'sales_copy': {'kind': '영업 문구', 'default_response': False, 'salesPitch': p['salesPitch'], 'upsellHook': p['upsellHook'], 'site_shows_as': '「상담 안내」 탭 · 「추가 제안」'}})
def name_narrow(f, texts):
    """R24 — 이름 조각(「+」로 나눔)을 풀어 계열 f 단위 시술이 일부만 잡히면 그것(problem-combos 패키지 이름 조각과 같은 방식)"""
    hit = []
    for npt in texts:
        r_ = resolve(re.sub(r'^(수입|국산)\s*', '', npt))
        fu = [u for u in r_['units'] if UNITS[u]['key']['family'] == f]
        if fu and len(fu) < len(units_of([f])):
            hit.append((npt, fu))
    return hit


for r in cr['recipes']:
    parts = []
    rparts = [x.strip() for x in re.split(r'\+', re.sub(r'\(.*?\)', '', r['subtitle'] or '')) + re.split(r'\+', re.sub(r'\(.*?\)', '', r['name'])) if x.strip()]
    # R24(사용자 10-30) — 이름 · subtitle 로 못 좁히면 레시피 설명 문장 칸(recipe_text_fields — analogy 「X = …」의 X · patientExplanation 괄호 · 낱말)
    tparts = []
    for fld in DEC['site_rules']['recipe_text_fields']:
        t_ = r.get(fld) or ''
        if fld == 'analogy':
            tparts += [x.split('=')[0].strip() for x in re.split(r'[,，]', t_) if '=' in x]
        else:
            tparts += re.findall(r'\(([^()]*)\)', t_) + [w for w in re.split(r'[\s,.·()]+', t_) if re.fullmatch(r'[A-Za-z][A-Za-z0-9+]*', w)]
    tparts = [x for x in dict.fromkeys(y.strip() for x in tparts for y in x.split('/')) if x]
    for f in r['procedures']:
        hit = name_narrow(f, rparts)
        src_ = '레시피 이름 · subtitle 조각 '
        if not hit:
            hit = name_narrow(f, tparts)
            src_ = '레시피 설명(analogy · patientExplanation) 낱말 '
        if hit:
            us = sorted({u for _, fu in hit for u in fu})
            parts.append({'family': f, 'family_name': FAM_NAME.get(f), 'status': '이름으로 내림(R24)' if len(us) == 1 else '이름으로 좁힘 · 후보 여럿(R24)', 'units': us, 'basis': src_ + ' · '.join(f'「{a}」' for a, _ in hit), 'flag': None if len(us) == 1 else 'ambiguous'})
        else:
            parts.append({'family': f, 'family_name': FAM_NAME.get(f), 'status': '후보 전부', 'units': units_of([f]), 'basis': '레시피에 부위 · 제품 없음 · 이름 조각으로 못 좁힘', 'flag': 'concern_without_site'})
    rpurp = sorted({t_ for x in re.split(r'\+', r['name']) if x.strip() for j_ in [judge(x.strip())] if j_['ok'] for t_ in (j_['target'] or []) if t_.startswith('목적:')})  # 레시피 이름 조각의 목적어(R16 · 10-30 「재생」 = 목적)
    combos.append({'id': f"RC-RE-{r['id']}", 'kind': '목적 레시피', 'source': 'combo-recipes', 'source_id': r['id'], 'anchor': {'goal': r['goal'], 'concern': GOAL.get(r['goal'], []), 'via': '고민 대응표 B-5(규칙)', 'purposes': rpurp, 'purposes_via': '레시피 이름 조각 → 목적(R12 · R14 · R16)'},
                   'name': r['name'], 'subtitle': r['subtitle'], 'tier': r['intensity'], 'components': parts, 'price': None,
                   'effect': {'expectedResults': r['expectedResults'], 'repeatCycle': r['repeatCycle']},
                   'consult_copy': {'kind': '상담 문구', 'default_response': True, 'patientExplanation': r.get('patientExplanation'), 'analogy': r.get('analogy')},
                   'follow_up': r.get('followUp')})
for i, c in enumerate(ts['common_combos']):  # 세션 조합 앵커 = 이름을 대응표 규칙으로(R12~R19) · 못 풀면 앵커 없음(이유 기록)
    a_ = judge(c['name'])
    combos.append({'id': f"RC-SQ-{i+1:02d}", 'kind': '세션 조합(순서)', 'source': 'treatment-sequence.common_combos', 'source_id': c['name'],
                   'anchor': {'concern': a_['target'] if a_['ok'] else [], 'via': ('규칙 — ' + ' + '.join(a_['rules'])) if a_['ok'] and a_['target'] else ('앵커 없음 — ' + (a_.get('why') or ' + '.join(a_['rules'])))},
                   'name': c['name'], 'components': comp(c['sequence']), 'total_time': c['total_time'], 'note_8': c.get('note'), 'price': None})
for c in to['by_concern']:
    cx, pu = ctx_of('treatment-optimization', c['concern'])
    for s in c['severity_levels']:
        combos.append({'id': f"RC-OP-{c['concern_en'].split()[0][:6]}-{s['level'].split()[0]}", 'kind': '중증도 조합', 'source': 'treatment-optimization.by_concern', 'source_id': f"{c['concern']}|{s['level']}",
                       'anchor': {'opt_concern': c['concern'], 'concern': lev_anchor(c['concern'], s['level'])['concern'], 'opt_concern_targets': OPT.get(c['concern'], []), 'severity': s['level'], 'severity_rule': lev_anchor(c['concern'], s['level'])['rule']}, 'name': f"{c['concern']} · {s['level']}",
                       'components': comp(s['optimal_combo'], cx, purpose=pu), 'sessions': s['expected_sessions'], 'duration': s.get('total_duration'), 'evidence_level': s.get('evidence_level'),
                       'rationale': s.get('rationale'), 'sequence_text_8': s.get('sequence'), 'caveats': s.get('caveats'), 'price': None})
for a in to['annual_plans']:
    sched = [{'month': m['month'], 'items': comp(m['procedures'])} for m in a['schedule']]
    combos.append({'id': f"RC-AN-{a['age_group']}", 'kind': '연간 플랜', 'source': 'treatment-optimization.annual_plans', 'source_id': a['plan_name'], 'anchor': {'age_group': a['age_group'], 'focus': a['focus']},
                   'name': a['plan_name'], 'price': a['annual_budget_range'], 'schedule': sched})
for a in to['by_age_group']:
    combos.append({'id': f"RC-AG-{a['age']}", 'kind': '연령 플랜', 'source': 'treatment-optimization.by_age_group', 'source_id': a['age'], 'anchor': {'age_group': a['age'], 'primary_concerns': a['primary_concerns']},
                   'name': f"{a['age']} 연령 플랜", 'components': comp(a['recommended_base']), 'upgrade': comp(a.get('upgrade') or []), 'avoid_text': a.get('avoid'), 'maintenance': a['maintenance'], 'annual_focus': a['annual_focus'], 'note': a.get('note'), 'price': None})
for c in cmp_['comparisons']:
    cx, pu = ctx_of('procedure-comparison', c['id'])
    mem = []
    for i, p in enumerate(c['procedures']):
        r = comp_one(p['name'], cx, purpose=pu)
        unit_fams = {UNITS[u]['key']['family'] for u in r['units']}
        mem.append({'order': i + 1, 'text': p['name'], 'source_family': p['category'], **r, 'family_mismatch': bool(r['units']) and p['category'] not in unit_fams,
                    'attrs_text': {k: p.get(k) for k in ['mechanism_simple', 'pain', 'downtime', 'onset', 'duration', 'cost_range', 'best_for', 'limitations', 'asian_skin_note', 'pih_risk'] if p.get(k) is not None}})
    combos.append({'id': f"RC-CP-{c['id']}", 'kind': '비교', 'source': 'procedure-comparison', 'source_id': c['id'], 'anchor': {'concern': CMPM.get(c['id'], []), 'title': c['title'], 'subtitle': c['subtitle']},
                   'name': c['title'], 'members': mem, 'evidence_notes': c.get('evidence_notes')})
KSN = DEC['combo_kind_site_names']
for c in combos:
    if c['kind'] not in KSN:
        op('결정 없는 추천 조합 종류(사이트 이름)', kind=c['kind'])
    c['site_names'] = KSN.get(c['kind'], [])
STALE += [['combo_kind_site_names', k] for k in KSN if k not in {c['kind'] for c in combos}]
STALE += [['context_by_source', list(k)] for k in CTX_BY if k not in {('treatment-optimization', c['concern']) for c in to['by_concern']} | {('procedure-comparison', c['id']) for c in cmp_['comparisons']}]

# ───────── E. 8단계 메모 ─────────
s8 = []
for c in to['by_concern']:
    for s in c['severity_levels']:
        for x in s.get('contraindicated_combos') or []:
            s8.append({'kind': '금기 · 간격', 'source': 'treatment-optimization.contraindicated_combos', 'where': f"{c['concern']} · {s['level']}", 'text': x})
        if s.get('sequence'):
            s8.append({'kind': '순서', 'source': 'treatment-optimization.sequence', 'where': f"{c['concern']} · {s['level']}", 'text': s['sequence'] if isinstance(s['sequence'], str) else json.dumps(s['sequence'], ensure_ascii=False)})
for r in to['combination_rules']:
    s8.append({'kind': '규칙(순서 · 간격 · 금기)', 'source': 'treatment-optimization.combination_rules', 'where': r['rule'], 'text': r['detail'], 'priority': r.get('priority')})
for c in ts['common_combos']:
    if c.get('note'):
        s8.append({'kind': '순서', 'source': 'treatment-sequence.common_combos.note', 'where': c['name'], 'text': c['note']})
for r in cr['recipes']:
    for f in r.get('followUp') or []:
        s8.append({'kind': '후속 간격(원문 속성으로도 둠)', 'source': 'combo-recipes.followUp', 'where': r['id'], 'text': f"{f['week']}주 · {f['action']}"})
S8RE = DEC['step8_patterns']
for P in pp['problems']:
    for c in P['complaints']:
        for cb in c.get('combos') or []:
            s8.append({'kind': '시너지(쌍 주장)', 'source': 'problem-packages.complaints[].combos', 'where': f"{P['problem_id']} {c['cc']}", 'text': f"{cb['name']} — {cb.get('reason')} / {cb.get('evidence')}"})
        for al in c.get('alternatives') or []:
            if re.search(S8RE['alternatives'], al):
                s8.append({'kind': '간격 · 금기(대안 칸에 섞임)', 'source': 'problem-packages.complaints[].alternatives', 'where': f"{P['problem_id']} {c['cc']}", 'text': al})
for c in pc['combos']:
    for p in c['packages']:
        if re.search(S8RE['riskBenefit'], p['riskBenefit']):
            s8.append({'kind': '순서 · 간격(위험 대비 효과 문장)', 'source': 'problem-combos.riskBenefit', 'where': p['id'], 'text': p['riskBenefit']})

# ───────── F. 빈자리 · 못 풂 · check · 계열 어긋남 ─────────
gaps = collections.OrderedDict()
notproc = collections.OrderedDict()


def gap(name, status, basis, where):
    tgt = notproc if status == '시술 아님' else gaps
    tgt.setdefault(basis, {'basis': basis, 'names': [], 'where': []})
    if name not in tgt[basis]['names']:
        tgt[basis]['names'].append(name)
    if where not in tgt[basis]['where']:
        tgt[basis]['where'].append(where)


def is_gap(st):
    return st.startswith('단위 시술 없음') or st.startswith('시술 아님')


def scan(name, r, where):
    if r is None:
        return
    if is_gap(r['status']):
        gap(name, '시술 아님' if r['status'].startswith('시술 아님') else '단위 시술 없음', r['basis'], where)
    if r['status'] == '복합 · 나눠 풂':
        for part in r['basis'].split(' · '):
            if part.endswith('→단위 시술 없음'):
                gap(f"{name} [{part.split('→')[0]}]", '단위 시술 없음', part, where)


for i in items:
    scan(i['name'], i['resolve'], 'taxonomy 항목')
for e in edges:
    if not is_gap(e['lowering']) or e['source'][0] == '⑦':
        continue
    st = '시술 아님' if e['lowering'].startswith('시술 아님') else '단위 시술 없음'
    if e['source'][0] == '③':
        gap(f"{e['source_id'].split(':')[1]}→{e['evidence']['name']}", st, e['lowering'].split(' — ', 1)[-1], e['source'])
        continue
    gap(e['basis'].split('「')[-1].split('」')[0] if '「' in e['basis'] else e['basis'], st, e['lowering'].split(' — ', 1)[-1] if ' — ' in e['lowering'] else e['basis'].split('→')[-1].strip(), e['source'])


def comp_iter(c):
    for x in (c.get('components') or []) + (c.get('members') or []) + (c.get('upgrade') or []):
        if 'text' in x:
            yield x
    for m in c.get('schedule') or []:
        for x in m['items']:
            yield x


for c in combos:
    for x in comp_iter(c):
        scan(x['text'], x, c['kind'])
for g in gaps.values():
    op('단위 시술 없는 이름', names=g['names'], basis=g['basis'])
s3n = s3['nodes']
site_gap_names = []
for i in items:
    if i['category'] == 'P10':
        for st in i['sites']:
            if not any(u['key']['family'] == 'M8' and u['key']['site'] == st for u in s5['units']) and st not in site_gap_names:
                site_gap_names.append(st)
for st in site_gap_names:
    op('제모 부위 단위 시술 없음', site=st)

UOK = {x['text']: x for x in DEC['unresolved_ok']}
unresolved = []
for e in edges:
    if e['lowering'] == '못 풂':
        unresolved.append({'where': '엣지', 'src': e['source'], 'text': e['basis']})
for c in combos:
    for x in (c.get('components') or []) + (c.get('members') or []):
        if 'text' in x and x.get('status') == '못 풂':
            unresolved.append({'where': '추천 조합', 'src': c['id'], 'text': x['text']})
for u in unresolved:
    d = next((v for k, v in UOK.items() if k in u['text']), None)
    if d is None:
        op('이름으로 못 푼 원소 · 결정 없음', where=u['src'], text=u['text'])
    else:
        u['decision'] = d['basis']
STALE += [['unresolved_ok', k] for k in UOK if not any(k in u['text'] for u in unresolved)]
check_flags = []


def walk(o, where):
    if isinstance(o, dict):
        if isinstance(o.get('flag'), str) and 'check' in o['flag']:
            check_flags.append({'where': where, 'text': o.get('text') or o.get('basis')})
        for v in o.values():
            walk(v, where)
    elif isinstance(o, list):
        for v in o:
            walk(v, where)


for c in combos:
    walk(c, c['id'])
for e in edges:
    for ck in CHECK:
        if e['to_units'] == [ck['unit']] and '스킨' not in e['basis'] and '모공' not in e['basis']:
            check_flags.append({'where': e['source'], 'text': e['basis']})
mism_cmp = [{'combo': c['id'], 'name': m['text'], 'source_family': m['source_family'], 'units': list(m['units']), 'unit_families': sorted({UNITS[u]['key']['family'] for u in m['units']})} for c in combos if c['kind'] == '비교' for m in c['members'] if m.get('family_mismatch')]
mism_cc = [{'from': e['from'], 'basis': e['basis'], 'lowering': e['lowering'], 'units': e['to_units']} for e in edges if '계열 코드 어긋남' in e['lowering'] and e['source'][0] == '③']
mism_item = [{'from': e['from'], 'basis': e['basis'], 'lowering': e['lowering'], 'units': e['to_units'], 'source_family': e['to_family']} for e in edges if '계열 코드 어긋남' in e['lowering'] and e['source'][0] == '⑤']

STALE += [['resolver.exact_overrides', k] for k in EXACT if k not in USED_EXACT]
# 사용자 판단 · 규칙 — 결정 행이 있어야
for jid in DEC['required_judgements']:
    if jid not in {j['id'] for j in DEC['judgements']}:
        op('사용자 판단 결정 없음', id=jid)

# 추천 조합 구성 — R22 고민 영역으로 거름 · 가드
def combo_concerns(c):
    a = c.get('anchor') or {}
    cs = a.get('concerns') or a.get('concern') or []
    return [cs] if isinstance(cs, str) else list(cs)


def combo_parts(c):
    for x in (c.get('components') or []) + (c.get('members') or []) + (c.get('upgrade') or []):
        yield x
    for m in c.get('schedule') or []:
        yield from m['items']


VOL_M2 = DEC['site_rules']['many_fillers']
for c in combos:
    cs = combo_concerns(c)
    rs = concern_regions(cs)
    c['concern_regions'] = sorted(rs)
    for x in combo_parts(c):
        if not x.get('units'):
            continue
        keep, cut, rs, notes = narrow(x['units'], (x.get('status') or '') + ' ' + (x.get('basis') or ''), cs)
        if not rs:
            x['concern_region_check'] = '고민 영역 없음(R22 · 셈만)' if cs else '고민 앵커 없음(R22 밖)'
        else:
            x['concern_region_check'] = (f"고민 영역 밖 {len(cut['R22'])} 뺌(R22)" if cut.get('R22') else '고민 영역 안(R22)') + (' · 기본 영역(판단 ①)' if any(c_ in CREG_DEFAULT for c_ in cs) else '')
        if cut.get('R22'):
            x['concern_region_dropped'] = cut['R22']
        if cut:
            x['narrow_dropped'] = {k_: v_ for k_, v_ in cut.items() if v_}
            x['units'] = keep
            x['status'] = (x.get('status') or '') + ' · ' + ' · '.join(notes) + empty_note(keep, cut)
            if cut.get('R26'):
                SCAR_HITS.append(f"추천 조합 {c['id']} · {x.get('text') or x.get('family')}")
        fu_ = {UNITS[u]['key']['family'] for u in x['units']}
        if x['units'] and fu_ == {VOL_M2['family']} and len(x['units']) > 1 and '후보 전부' in (x.get('status') or ''):  # 판단 ②
            x['status'] += ' · ' + VOL_M2['label']
            x['flag'] = 'ambiguous'
    for x in combo_parts(c):
        bad22 = [u for u in x.get('units') or [] if rs and UNITS[u]['key']['site'] not in SITE_FREE and region(UNITS[u]['key']['site']) not in rs]
        if bad22:
            op('추천 조합 단위 시술이 고민 영역 밖', combo=c['id'], regions=sorted(rs), units=bad22)
        b25 = [u for u in x.get('units') or [] if '두피' not in rs and region(UNITS[u]['key']['site']) == '두피']
        if b25:
            op('추천 조합 두피 단위 시술이 두피 고민 밖(R25)', combo=c['id'], units=b25)
        if is_scar(cs) and any(UNITS[u]['key']['family'] == SCAR_FAM for u in x.get('units') or []):
            op('흉터 고민에 필러 단위 시술(R26)', combo=c['id'], units=[u for u in x['units'] if UNITS[u]['key']['family'] == SCAR_FAM])
for e in edges:  # R25 · R26 가드(앵커 부위 없는 엣지)
    if e['anchor_sites'] or not e['source'].startswith(NARROW_SRC):
        continue
    cs = e.get('from_concerns') or [e['from']]
    rs = set(e['concern_regions'])
    b25 = [u for u in e['to_units'] if '두피' not in rs and region(UNITS[u]['key']['site']) == '두피']
    if b25:
        op('엣지 두피 단위 시술이 두피 고민 밖(R25)', source=e['source'], source_id=e['source_id'], units=b25)
    if is_scar(cs) and any(UNITS[u]['key']['family'] == SCAR_FAM for u in e['to_units']):
        op('흉터 고민에 필러 단위 시술(R26)', source=e['source'], source_id=e['source_id'], units=[u for u in e['to_units'] if UNITS[u]['key']['family'] == SCAR_FAM])

# ───────── 셈 · 출력 ─────────
cat_nodes = [c for c in cats if c['node']]
sub_nodes = [s for s in subs if s['node']]
item_nodes = [i for i in items if i['kind'] == '고민'] + extra_items
purpose_nodes = [p for p in purposes if p['node']]
human = [r for r in corr if r.get('human_check')]
# J10 피부결 등 결정 노드 — 원천 어디에 붙었나(대응표 · 엣지 · 추천 조합 · 원소 풀이)
for x in extra_items:
    i_ = x['id']
    x['links'] = {
        'correspondence': [f"{r['source']} 「{r['text']}」" for r in corr if i_ in r['target']],
        'edges': [f"{e['source']} {e['source_id']} → {e['to_family'] or '/'.join(e['to_units'][:3])}" for e in edges if e['from'] == i_ or i_ in (e.get('from_concerns') or [])],
        'combos': [c['id'] for c in combos if i_ in (lambda a: (a.get('concern') if isinstance(a.get('concern'), list) else [a.get('concern')]) + (a.get('concerns') or []))(c['anchor'])],
        'glosses': sorted({f"{c['id']} {x_['text']}" for c in combos for x_ in comp_iter(c) if i_ in (x_.get('concern_gloss') or [])}),
    }
    x['links_count'] = {k: len(v) for k, v in x['links'].items()}
concern_unres = [{'source': r['source'], 'text': r['text'], 'why': r['basis'], 'candidates': r.get('candidates') or [], 'question': r.get('question')} for r in human]
summary = {
    'concern_nodes': {'category': len(cat_nodes), 'subcategory': len(sub_nodes), 'item': len(item_nodes), 'item_from_decision': len(extra_items), 'total': len(cat_nodes) + len(sub_nodes) + len(item_nodes)},
    'taxonomy_layers': {'category': len(cats), 'subcategory': len(subs), 'item': len(items), 'item_kind': dict(C(i['kind'] for i in items)), 'subcategory_kind': dict(C(s['kind'] for s in subs))},
    'correspondence': {'rows': len(corr), 'by_source': dict(C(r['source'] for r in corr)), 'by_class': dict(C(r['match_class'] for r in corr)), 'human_check': len(human), 'gate_status': dict(C(r['gate_status'] for r in corr)),
                       'auto': sum(1 for r in corr if not r.get('human_check')), 'auto_exact': sum(1 for r in corr if r['gate_status'] == '자동(완전 일치)'), 'auto_rule': sum(1 for r in corr if r['gate_status'] == '자동(규칙)')},
    'decision_nodes': {x['id']: x['links_count'] for x in extra_items},
    'purposes': {'expressions': len(purposes), 'nodes': len(purpose_nodes), 'folded_into_concern': len(purposes) - len(purpose_nodes)},
    'edges': {'total': len(edges), 'by_source': dict(C(e['source'] for e in edges)), 'to_units': sum(1 for e in edges if e['target_kind'] == '단위 시술'), 'family_only': sum(1 for e in edges if e['target_kind'] == '계열만'),
              'no_target': sum(1 for e in edges if e['target_kind'] == '대상 없음'), 'unit_pairs': sum(len(e['to_units']) for e in edges), 'site_check': dict(C(e['site_check'] for e in edges)),
              'narrow': {k_: {'edges': sum(1 for e in edges if (e.get('narrow_dropped') or {}).get(k_)), 'units_cut': sum(len((e.get('narrow_dropped') or {}).get(k_) or []) for e in edges)} for k_ in ('R23', 'R22', 'R25', 'R26')},
              'merged_r27': {'edges': len(R27_GROUPS), 'cc_rows': sum(len(g['ccs']) for g in R27_GROUPS)},
              'concern_region': {'edges_cut': sum(1 for e in edges if e.get('concern_region_dropped')), 'units_cut': sum(len(e.get('concern_region_dropped') or []) for e in edges),
                                 'no_region_untouched': sum(1 for e in edges if e.get('concern_region_check') == '고민 영역 없음(R22 · 셈만)')}},
    'combos': {'total': len(combos), 'by_kind': dict(C(c['kind'] for c in combos)), 'sales_copy_default_excluded': sum(1 for c in combos if c.get('sales_copy'))},
    'step8_notes': {'total': len(s8), 'by_kind': dict(C(x['kind'] for x in s8))},
    'unit_gaps': len(gaps), 'not_procedure_names': len(notproc), 'p10_site_gaps': site_gap_names, 'unresolved': len(unresolved), 'check_flags': len(check_flags),
    'family_mismatch': {'comparison': len(mism_cmp), 'cc': len(mism_cc), 'taxonomy_item': len(mism_item)},
    'open': len(OPEN), 'open_by_type': dict(C(o['type'] for o in OPEN)), 'stale': len(STALE),
}
OQ = [{'id': f'Q7-{i+1:02d}', 'to': ck['to'], 'question': ck['question'], 'where': sorted({f['where'] for f in check_flags}), 'count': len(check_flags)} for i, ck in enumerate(CHECK)]
OQ += [{'id': f'Q7-{len(OQ)+i+1:02d}', 'to': x['origin_question']['to'], 'question': x['origin_question']['question'], 'where': x['origin_question']['where'], 'count': 1}
       for i, x in enumerate(v for v in EXACT.values() if v.get('origin_question'))]  # J7 G10 — 이름 결정에 걸린 원천 질문
OQ += [{'id': f'Q7-{len(OQ)+i+1:02d}', 'to': '사람(규칙 밖 고민 표현 · R20)', 'question': r.get('question') or f"고민 대응 「{r['text']}」({r['source']}) — 규칙 밖", 'where': [r['source']], 'count': 1,
        'text': r['text'], 'why': r['basis'], 'candidates': r.get('candidates') or []} for i, r in enumerate(human)]
SF = DEC['site_rules']['scar_filler']['origin_question']
if SCAR_HITS:  # R26 — 흉터 필러 단위 시술(원천 질문)
    OQ.append({'id': f'Q7-{len(OQ)+1:02d}', 'to': SF['to'], 'question': SF['question'], 'where': sorted(set(SCAR_HITS)), 'count': len(SCAR_HITS)})
fix_r27 = [dict(kind='갈래 목록 복사(R27)', from_=g['from'], basis=f"갈래 {g['group']} 추천 시술 {g['procedure']}({g['family']}) 이 CC {len(g['ccs'])}개({' · '.join(g['ccs'])})에 같은 목록으로 복사 — CC 별 목록이 원래 의도였는지", units=[], source_family=g['family']) for g in R27_GROUPS]
for f_ in fix_r27:
    f_['from'] = f_.pop('from_')
fix = [dict(kind='계열 코드 어긋남(비교)', **m) for m in mism_cmp] + [dict(kind='계열 코드 어긋남(CC)', **m) for m in mism_cc] + [dict(kind='계열 코드 어긋남(taxonomy 항목)', **m) for m in mism_item] + fix_r27
out = {
    'version': 'step7-concerns v1 (2026-10-29)', 'generated_by': 'step7-apply.py(결정론)', 'decision_ref': DEC['decision_ref'],
    'inputs': {'source': str(SRC), 'decisions': Path(ARGS.decisions).name, 'canon': DEC['canon']},
    'site_terms': DEC['site_terms'], 'rules': DEC['rules'], 'judgements': DEC['judgements'], 'summary': summary,
    'concerns': {'categories': cats, 'subcategories': subs, 'items': items, 'extra_items': extra_items},
    'correspondence': corr, 'purposes': purposes, 'edges': edges, 'combos': combos, 'step8_notes': s8,
    'unit_gaps': list(gaps.values()), 'not_procedure': list(notproc.values()), 'unresolved': unresolved, 'concern_unresolved': concern_unres, 'check_flags': check_flags,
    'origin_questions': OQ, 'source_fix_candidates': fix, 'open': OPEN, 'stale_decisions': STALE,
}
OUT.mkdir(parents=True, exist_ok=True)
json.dump(out, open(OUT / 'step7-concerns.json', 'w'), ensure_ascii=False, indent=1)

# ───────── md ─────────
L = []
A = L.append


def uu(us, n=6):
    if not us:
        return '—'
    s = ' · '.join(f'{u} {UN.get(u, "")}' for u in us[:n])
    return s + (f' 외 {len(us) - n}' if len(us) > n else '')


def sid(x):
    return x.replace('-1774737181584', '')


sm = summary
fx = W / 'step7-fixtures' / 'result.json'
fxr = json.load(open(fx)) if fx.exists() else None
A('---\ntitle: 실버 7단계 반영 — 고민 · 목적 · 추천 조합\ndate: 2026-10-29\nauthor: researcher(step7-apply.py)\ndecision: ' + DEC['decision_ref'] + '\ndata: step7-concerns.json\n---\n')
A('# 실버 7단계 반영 — 고민 · 목적 · 추천 조합\n')
A(f"> **셈** — 고민 노드 {sm['concern_nodes']['total']}(대분류 {sm['concern_nodes']['category']} · 중분류 {sm['concern_nodes']['subcategory']} · 항목 {sm['concern_nodes']['item']} — 결정으로 더한 항목 {sm['concern_nodes']['item_from_decision']}) · "
  f"대응 {sm['correspondence']['rows']}행(자동 {sm['correspondence']['auto']} = 완전 일치 {sm['correspondence']['auto_exact']} · 규칙 {sm['correspondence']['auto_rule']} / 규칙 밖 사람 질문 {sm['correspondence']['human_check']}) · 목적 노드 {sm['purposes']['nodes']}(목적 표현 {sm['purposes']['expressions']} · 고민에 붙임 {sm['purposes']['folded_into_concern']}) · "
  f"엣지 {sm['edges']['total']}(단위 시술 {sm['edges']['to_units']} · 계열만 {sm['edges']['family_only']} · 대상 없음 {sm['edges']['no_target']} · 단위 시술 쌍 {sm['edges']['unit_pairs']} · 앵커 부위 밖 {sm['edges']['site_check'].get('부위 밖', 0)} · 영역 넘음 {sm['edges']['site_check'].get('영역 넘음', 0)} · "
  f"부위 올라가기(R21) 상위 층 {sum(v for k, v in sm['edges']['site_check'].items() if k.startswith('상위 부위'))} · 이 부위 단위 시술 없음 · 계열만 {sm['edges']['site_check'].get('이 부위 단위 시술 없음 · 계열만', 0)}) · "
  f"고민 영역(R22) 엣지 뺌 {sm['edges']['concern_region']['edges_cut']}(단위 시술 {sm['edges']['concern_region']['units_cut']}) · 영역 없어 손 안 댐 {sm['edges']['concern_region']['no_region_untouched']} · "
  f"추천 조합 구성 뺌 {sum(1 for c in combos for x in combo_parts(c) if x.get('concern_region_dropped'))}(단위 시술 {sum(len(x.get('concern_region_dropped') or []) for c in combos for x in combo_parts(c))}) · 영역 없어 손 안 댐 {sum(1 for c in combos for x in combo_parts(c) if x.get('concern_region_check') == '고민 영역 없음(R22 · 셈만)')} · "
  f"좁힘 엣지(R23 용도 {sm['edges']['narrow']['R23']['edges']} · R25 두피 {sm['edges']['narrow']['R25']['edges']} · R26 흉터 필러 {sm['edges']['narrow']['R26']['edges']}) · 겹친 ③ 합침(R27) {sm['edges']['merged_r27']['edges']}엣지 ← CC {sm['edges']['merged_r27']['cc_rows']}행 · "
  f"좁힘 조합 구성(R23 {sum(1 for c in combos for x in combo_parts(c) if (x.get('narrow_dropped') or {}).get('R23'))} · R25 {sum(1 for c in combos for x in combo_parts(c) if (x.get('narrow_dropped') or {}).get('R25'))} · R26 {sum(1 for c in combos for x in combo_parts(c) if (x.get('narrow_dropped') or {}).get('R26'))} · 이름 조각 R24 {sum(1 for c in combos for x in combo_parts(c) if 'R24' in (x.get('status') or ''))} · 필러 후보 여럿 판단 ② {sum(1 for c in combos for x in combo_parts(c) if '판단 ②' in (x.get('status') or ''))}) · "
  f"추천 조합 {sm['combos']['total']}(영업 문구 기본 제외 {sm['combos']['sales_copy_default_excluded']}) · 8단계 메모 {sm['step8_notes']['total']} · "
  f"단위 시술 없는 이름 {sm['unit_gaps']} · 시술 아님 {sm['not_procedure_names']}묶음 · 못 풂 {sm['unresolved']} · check {sm['check_flags']} · 원천 수정 후보 {len(fix)} · 원천 질문 {len(OQ)} · "
  f"**open {sm['open']} · stale {sm['stale']}**" + (f" · 고정 시험 {fxr['passed']}/{fxr['total']}" if fxr else ''))
A('')
if OPEN:
    A('## open\n\n| 종류 | 내용 |\n|---|---|')
    for o in OPEN:
        A(f"| {o['type']} | {json.dumps({k: v for k, v in o.items() if k != 'type'}, ensure_ascii=False)[:200]} |")
    A('')
if STALE:
    A('## stale 결정\n\n' + '\n'.join(f'- {json.dumps(s, ensure_ascii=False)}' for s in STALE) + '\n')
A('## ① 규칙 · 사용자 판단(결정 파일)\n\n| id | 규칙 | 근거 |\n|---|---|---|')
for r in DEC['rules']:
    A(f"| {r['id']} | {r['rule']} | {r['basis']} |")
A('\n추천 조합 종류 ↔ 사이트 이름(동의어): ' + ' · '.join(f"{k} = {' / '.join(v) or '—'}" for k, v in DEC['combo_kind_site_names'].items()))
A('\n| id | 판단 | 결정 | 결정 출처 |\n|---|---|---|---|')
for j in DEC['judgements']:
    A(f"| {j['id']} | {j['question']} | {j['decision']} | {j['decided_by']} |")
A('\n> 사이트 용어(화면 코드) = 동의어: ' + ' / '.join(f'**{k}** {v}' for k, v in DEC['site_terms'].items()))
A('\n## ② 셈 상세\n')
A(f"- 고민 트리 원천 {len(cats)} · {len(subs)} · {len(items)} — 항목 갈래 " + ' · '.join(f'{k} {v}' for k, v in sm['taxonomy_layers']['item_kind'].items()) + ' / 중분류 갈래 ' + ' · '.join(f'{k} {v}' for k, v in sm['taxonomy_layers']['subcategory_kind'].items()))
A('- 대응 원천별 ' + ' · '.join(f'{k} {v}' for k, v in sm['correspondence']['by_source'].items()) + ' / 일치 갈래 ' + ' · '.join(f'{k} {v}' for k, v in sm['correspondence']['by_class'].items()) + ' / 게이트 ' + ' · '.join(f'{k} {v}' for k, v in sm['correspondence']['gate_status'].items()))
A('- 엣지 원천별 ' + ' · '.join(f'{k} {v}' for k, v in sm['edges']['by_source'].items()))
A('- 추천 조합 ' + ' · '.join(f'{k} {v}' for k, v in sm['combos']['by_kind'].items()))
A('- 8단계 메모 ' + ' · '.join(f'{k} {v}' for k, v in sm['step8_notes']['by_kind'].items()))

A('\n## A. 고민 노드\n\n### A-1. 대분류\n\n| id | 원천 | 노드 이름 | 판정 | 근거 |\n|---|---|---|---|---|')
for c in cats:
    A(f"| {c['id']} | {c['source_name']} ({c['en']}) | {c['name'] if c['node'] else '—'}{(' (동의어 ' + ' · '.join(c['synonyms']) + ')') if c.get('synonyms') else ''} | {c['verdict']} | {c['basis']} |")
A('\n### A-2. 중분류\n\n| id | 원천 이름 | 갈래 | 고민 | 부위 | 목적 | 노드 | 메모 |\n|---|---|---|---|---|---|---|---|')
for s in subs:
    A(f"| {s['id']} | {s['source_label']} | {s['kind']} | {s['concern'] or '—'} | {' · '.join(s['sites']) or '—'} | {s['purpose'] or '—'} | {('○ 최상위' if s['top_level'] else '○') if s['node'] else '—'} | {s['note']} |")
A('\n### A-3. 항목\n\n| id | 중분류 | 이름 [detail] | 갈래 | 고민 · 부위 | 단위 시술 | 풀이 |\n|---|---|---|---|---|---|---|')
for i in items:
    det = i['detail'].split('.')[0][:30]
    if i['resolve']:
        A(f"| {sid(i['id'])} | {i['subcategory']} | {i['name']} [{det}] | {i['kind']} | {' · '.join(i['sites']) or '—'} | {uu(i['resolve']['units'])} | {i['resolve']['status']} — {i['resolve']['basis'][:80]} |")
    else:
        low = ' / '.join(f"{f}: {uu(v, 3) if v else '그 부위 없음'}" for f, v in (i['modality_lowered'] or {}).items())
        A(f"| {sid(i['id'])} | {i['subcategory']} | {i['name']} [{det}] | {i['kind']} | {i['concern'] or '—'} @ {' · '.join(i['sites']) or '—'} | {low} | modality_ref 부위로 내림 |")
for x in extra_items:
    A(f"| {x['id']} | {x['parent'] or '— (대분류 급)'} | {x['name']} | {x['kind']} | {x['name']} @ {' · '.join(x['sites']) or '—'} | — | {x['basis']} · 붙은 곳 " + ' · '.join(f'{k} {v}' for k, v in x['links_count'].items()) + ' |')
for x in extra_items:
    if x.get('related'):
        A(f"\n**{x['id']} 붙은 곳**(related {' · '.join(x['related'])}): 대응 — " + ' / '.join(x['links']['correspondence']) + ' · 추천 조합 — ' + ' · '.join(x['links']['combos']) + ' · 원소 풀이 — ' + ' · '.join(x['links']['glosses']) + f" · 엣지 {len(x['links']['edges'])}")

A('\n## B. 고민 대응표 — 규칙(R12~R20)\n')
A('규칙으로 하나로 정해지면 자동(human_check false · match_class 에 규칙 id) · 안 정해지는 것만 사람 질문(결정 concern_unresolved — 없으면 open).\n')
A('### B-0. 규칙 밖 — 사람 질문\n\n| 원천 | 표현 | 왜 안 정해지나 | 후보 | 질문 |\n|---|---|---|---|---|')
for r in human:
    A(f"| {r['source']} | {r['text']} | {r['basis'].replace('규칙 밖 — ', '')} | {' · '.join(sid(t) for t in r.get('candidates') or []) or '—'} | {r.get('question') or '—'} |")
A('\n### B-1. 전체\n\n| 원천 | 칸 | 표현 | 일치 | 규칙 | → 고민 | 부위 · 중증도 | 게이트 |\n|---|---|---|---|---|---|---|---|')
for r in corr:
    A(f"| {r['source']} | {r['field']} | {r['text']} | {r['match_class']} | {r['match']} | {' · '.join(sid(t) for t in r['target']) or '—'} | {' · '.join((r.get('rule_sites') or []) + (r.get('severity') or [])) or '—'} | {r['gate_status']} |")

A('\n## C. 목적\n\n### C-1. 목적 표현 → 노드 · 고민에 붙임\n\n| 목적 | 원천 표현 | 원천 낱말(대조 키) | 같은 말 고민 | 갈래 | 노드 |\n|---|---|---|---|---|---|')
for p in purposes:
    A(f"| {p['name']} | {' · '.join(p['from'])} | {' · '.join(a['source'] + ' 「' + a['text'] + '」' for a in p['aliases']) or '—'} | {p['same_as_concern'] or '—'} | {p['kind']} | {'○' if p['node'] else '고민에 붙임'} |")
A('\n### C-2. 엣지 — 원천별 · 대상\n\n| 원천 | 엣지 | 단위 시술 | 계열만 | 대상 없음 |\n|---|---|---|---|---|')
for src, n in C(e['source'] for e in edges).items():
    es = [e for e in edges if e['source'] == src]
    A(f"| {src} | {n} | {sum(1 for e in es if e['target_kind'] == '단위 시술')} | {sum(1 for e in es if e['target_kind'] == '계열만')} | {sum(1 for e in es if e['target_kind'] == '대상 없음')} |")
A('\n내림 상태: ' + ' · '.join(f'{k} {v}' for k, v in C(e['lowering'].split(' — ')[0].split(' · 계열 코드')[0] for e in edges).most_common()))
A('\n목적 · 메뉴 분류 엣지(⑥ · ⑦):\n\n| from | 목적 노드 | 단위 시술 | 원천 |\n|---|---|---|---|')
for e in edges:
    if e['source'][0] in '⑥⑦':
        A(f"| {e['from']} | {' · '.join(e['purpose_nodes'] or []) or '—'} | {uu(e['to_units'], 8)} | {e['source']} · {e['basis'][:60]} |")
A('\n엣지 전체는 json `edges[]` — from · purpose_nodes · to_units · to_family · target_kind · lowering · basis · evidence.')

A('\n## D. 추천 조합\n\n| id | 종류 | 고민 앵커 | 이름 | 등급 | 가격 | 구성(단위 시술) |\n|---|---|---|---|---|---|---|')
for c in combos:
    anc = c['anchor']
    a_ = anc.get('concern') or anc.get('age_group') or anc.get('goal') or '—'
    if isinstance(a_, list):
        a_ = ' · '.join(a_) or '—'
    if c['kind'] == '연간 플랜':
        comp_ = f"12개월 · 원소 {sum(len(m['items']) for m in c['schedule'])}(월별 원문 + 내림 — json)"
    elif c['kind'] == '비교':
        comp_ = ' / '.join(f"{m['text']} → {uu(m['units'], 2)}" for m in c['members'])
    elif c['kind'] in ('고민 패키지(사이트 「추천 패키지」)', '목적 레시피'):
        comp_ = ' / '.join(f"{p['family']} {p['status']}({len(p['units'])})" for p in c['components'])
    else:
        comp_ = ' / '.join(f"{x['text']} → {uu(x['units'], 2)}" for x in c['components'])
    tier = c.get('tier_label_site') or c.get('tier') or (anc.get('severity') or '').split(' ')[0] or '—'
    A(f"| {c['id']} | {c['kind']} | {a_} | {c['name']} | {tier} | {c.get('price') or '—'} | {comp_} |")
A('\n- 고민 패키지의 영업 문구(salesPitch · upsellHook)는 json `sales_copy`(kind 영업 문구 · default_response false — 보관 · 기본 응답 제외) · 기대 효과 · 임상 근거 · 위험 대비 효과는 `effect` 원문')
A('- 레시피의 환자 설명 · 비유는 `consult_copy`(상담 문구 · 기본 포함) · 후속 일정 `follow_up` 원문')
A('- 중증도 조합의 sequence · rationale · caveats · 회차 · 기간 · 근거 수준 = 원문 속성 · 비교 구성원 칸 = `attrs_text` 원문(단위 시술 속성과 합치지 않음 — B12)')

A('\n## E. 8단계 메모(표시만)\n\n| 갈래 | 수 | 원천 |\n|---|---|---|')
for k, v in C(x['kind'] for x in s8).items():
    A(f"| {k} | {v} | {' · '.join(sorted({x['source'] for x in s8 if x['kind'] == k}))} |")
A('\n전체 행은 json `step8_notes[]`(where · text 원문).')

A('\n## F. 빈자리 · 시술 아님 · 못 풂 · check · 원천 수정 후보\n\n| 갈래 | 이름 | 사유 | 나온 곳 |\n|---|---|---|---|')
for g in gaps.values():
    A(f"| 단위 시술 없음(open) | {' · '.join(g['names'][:8])} | {g['basis']} | {' · '.join(g['where'])} |")
for g in notproc.values():
    A(f"| 시술 아님(5단계 선례 · 엣지 없음) | {' · '.join(g['names'][:8])} | {g['basis']} | {' · '.join(g['where'])} |")
for st in site_gap_names:
    A(f"| 제모 부위 단위 시술 없음(open) | {st} | — | taxonomy P10 |")
for u in unresolved:
    A(f"| 못 풂(표시) | {u['text'][:60]} | {u.get('decision') or '결정 없음'} | {u['where']} {u['src']} |")
for f in check_flags:
    A(f"| check(의료진 질문) | {str(f['text'])[:70]} | 얼굴 전체 M1 = 스킨보톡스뿐 | {f['where']} |")
A(f"| 원천 수정 후보 | 계열 코드 어긋남 {len(fix)}(비교 {len(mism_cmp)} · CC {len(mism_cc)} · taxonomy 항목 {len(mism_item)}) | {DEC['source_fix_rule']['rule']} | step7-source-fix.md |")
if fxr:
    A('\n## 고정 시험(결정 빼면 open)\n\n| id | 입력 | 기대 | 결과 |\n|---|---|---|---|')
    for c in fxr['cases']:
        A(f"| {c['id']} | {c['input']} | {' · '.join(c['expect']) or 'open 0'} | {'PASS' if c['pass'] else 'FAIL'} |")
A('\n## 남은 것(기록만)\n\n' + '\n'.join(f"- **{x['id']}** {x['text']} — {x['basis']}" for x in DEC.get('remaining') or []) + '\n')
A('\n## 지킨 것\n\n- 원천(stg 2026-10-26) · 1~6단계 정본은 읽기만 · 결정 = step7-decisions.json · 숫자는 json `summary` 에서\n- 추정 금지 — 이름 · 부위 · 제품 칸에 없는 단위 시술은 내리지 않는다. 앵커 부위에 없으면 부위 트리 상위 노드 자신 → 영역 「전체」 노드까지만 올라가고(R21 · 영역 경계 안 넘음) · 끝까지 없으면 계열만 + 「이 부위 단위 시술 없음」 · 앵커 부위 자체가 없으면 「후보 전부 + 표시」 뒤 고민 영역(R22)으로 거름 · 영역 못 정하는 고민은 손 안 댐\n- 결정 없는 원천 행 · 표현 · 단위 시술 없는 이름 = open')
open(OUT / 'step7-concerns.md', 'w').write('\n'.join(L) + '\n')

Q = ['---\ntitle: 실버 7단계 원천 질문\ndate: 2026-10-29\ndata: step7-concerns.json origin_questions\n---\n', '# 실버 7단계 원천 질문\n',
     f'- 질문 {len(OQ)} = 의료진 {len(CHECK)} · 원천(병원 · 이름 결정) {sum(1 for v in EXACT.values() if v.get("origin_question"))} · 규칙 밖 고민 표현(사람 질문 · R20) {len(human)} — 대응표는 규칙(R12~R19)으로 닫고 규칙으로 하나로 안 정해지는 것만 여기(후보는 추천값 아님)\n', '| id | 누구 | 질문 | 나온 곳 |', '|---|---|---|---|']
for q in OQ:
    Q.append(f"| {q['id']} | {q['to']} | {q['question']} | {' · '.join(q['where'])[:80]} |")
open(OUT / 'step7-origin-questions.md', 'w').write('\n'.join(Q) + '\n')
F = ['---\ntitle: 실버 7단계 원천 수정 후보\ndate: 2026-10-29\ndata: step7-concerns.json source_fix_candidates\n---\n', '# 실버 7단계 원천 수정 후보 — 계열 코드 어긋남 · 갈래 목록 복사(R27)\n',
     f"{DEC['source_fix_rule']['rule']}\n", '| 갈래 | 어디 | 원천 이름 · 근거 | 원천 계열 | 단위 시술 |', '|---|---|---|---|---|']
for f in fix:
    if f['kind'].endswith('(비교)'):
        F.append(f"| {f['kind']} | {f['combo']} | {f['name']} | {f['source_family']} | {uu(f['units'], 4)} ({'/'.join(f['unit_families'])}) |")
    else:
        F.append(f"| {f['kind']} | {sid(f['from'])} | {f['basis']} | {f.get('source_family') or '—'} | {uu(f['units'], 4)} |")
open(OUT / 'step7-source-fix.md', 'w').write('\n'.join(F) + '\n')
print(json.dumps(dict(concerns=summary['concern_nodes']['total'], correspondence=len(corr), human=len(human), purposes=summary['purposes']['nodes'], edges=len(edges),
                      combos=len(combos), step8=len(s8), open=len(OPEN), open_by_type=summary['open_by_type'], stale=len(STALE)), ensure_ascii=False))
