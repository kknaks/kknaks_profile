#!/usr/bin/env python3
"""허브 데이터 품질 측정(1차 10-30 · 2차 10-30 품질 수정 뒤) — 결정론 · LLM 없음 · 읽기 전용(실버 · 시맨틱 · 브론즈 수정 없음).

2차 측정 변경(문항 · 정답 · 채점 식은 그대로 — quality-eval-set.json 은 1차와 바이트 같음):
  · resolve = semantic.json dictionary.resolve_rules 그대로(문서 = 코드 · 품질 M · G · H)
  · I-01 경로 = R32 층 표시(U-1 ② · 엣지 layer 「상위」) · R28 CC 슬롯(코디 10-30 · 골드 도구 입력 후보) — 「CC 없음」 값과 나란히
  · 부위 무관 특수 부위(병변 단위 · 해당 없음 — 7단계 site_free)는 부위 층 거르기에서 통과
  · 같이 · 간격 = 8단계 reading_contract 대로(by_direction · options 「순서」 · 조건부 주장은 질의가 조건 낱말을 말할 때)
  · 안전 묶음에 gap 상태(G13 · 8단계 safety.unit_gaps) · M4 구조 = 8단계 row_landing(규칙으로 원문만 싣는 행 표시) · 4자 미만 실버 원문은 완전 같음으로 대조
  · --inputs <폴더> 로 다른 판(1차 실버)을 같은 2차 측정으로 잴 수 있음(--out 에 씀)

산출: quality-eval-set.json(문항 · 정답 · 근거) · quality-report.json · quality-report.md
두 번 실행해 cmp 로 같은지 본다(시각 · 난수 없음 — 표본은 고정 시드).

측정
  M1 질문 세트 정답률 — 골드 조사(gold-research) 탐색 경로 P-01~P-11 을 지금 실버 · 시맨틱 위에서 흉내
  M2 말 → 노드 찾기 — 시맨틱 사전(T1 resolve 꼴: 완전 → 낱말 나눔 → 접두)
  M3 엣지 표본 검수 — 엣지 종류 21 × 고정 시드 표본 ↔ 원천 브론즈
  M4 안전 누락 — 원천 안전 문장 → 실버 전수(원천 → 실버 방향) · 안전 정보 0 단위 시술
"""
import json, os, re, random, unicodedata, collections, hashlib

W = os.path.dirname(os.path.abspath(__file__))
import sys as _sys
_ARGV = _sys.argv[1:]
INP = _ARGV[_ARGV.index('--inputs') + 1] if '--inputs' in _ARGV else W  # 실버 · 시맨틱 입력 폴더(없는 파일은 W)
OUTD = _ARGV[_ARGV.index('--out') + 1] if '--out' in _ARGV else W
B = '/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26'
SAMPLE = os.path.join(W, '../../../reference/2026-10-30-chatry-sample/S3p-Scenario.dc.html')
SEED = 20261030
PER_KIND = 20


def L(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def SL(name):
    p_ = os.path.join(INP, name)
    return L(p_ if os.path.exists(p_) else os.path.join(W, name))


def BL(name):
    return L(os.path.join(B, name))


# ───────────────────────── 입력 ─────────────────────────
SEM = SL('semantic.json')
P1 = SL('step1-products.json')
F2 = SL('step2-families.json')
S3 = SL('step3-sites.json')
T4 = SL('step4-techniques.json')
U5 = SL('step5-units.json')
G6 = SL('step6-packages.json')
C7 = SL('step7-concerns.json')
R8 = SL('step8-relations.json')
GOLD = SL('gold-research.json')

b_tax = BL('taxonomy.json')
b_pp = BL('problem-packages.json')
b_pc = BL('problem-combos.json')
b_mp = BL('market-pricing.json')
b_prod = BL('products.json')
b_pe = BL('patient-education.json')
b_pf = BL('procedure-profiles.json')
b_cmp = BL('procedure-comparison.json')
b_cx = BL('complications.json')
b_ci = BL('contraindications.json')
b_ts = BL('treatment-sequence.json')
b_to = BL('treatment-optimization.json')
b_cc = BL('consent-checklist.json')
b_pre = BL('pre-procedure-checklist.json')
b_syn = BL('synergy.json')
b_az = BL('anatomy-danger-zones.json')
b_tl = BL('post-procedure-timeline.json')
b_pih = BL('pih-risk.json')
b_ext = BL('extracted.json')
b_lit = BL('literature-evidence.json')
b_cr = BL('combo-recipes.json')

INPUT_SHA = {}
for n in ['semantic.json', 'step1-products.json', 'step2-families.json', 'step3-sites.json', 'step4-techniques.json',
          'step5-units.json', 'step6-packages.json', 'step7-concerns.json', 'step8-relations.json', 'gold-research.json']:
    INPUT_SHA[n] = hashlib.sha256(open(os.path.join(INP, n) if os.path.exists(os.path.join(INP, n)) else os.path.join(W, n), 'rb').read()).hexdigest()[:16]


# ───────────────────────── 공통 ─────────────────────────
RR = SEM['dictionary'].get('resolve_rules')  # 2차: 사전 찾기 규칙(문서 = semantic-build.py 코드 · 품질 M) — 없으면 1차 규칙


def norm(s):
    """사전 정규화 — semantic.json dictionary.resolve_rules 그대로(2차). 칸이 없으면 1차(NFKC · 공백 제거 · 전부 소문자)."""
    t = unicodedata.normalize('NFKC', str(s or ''))
    if not RR:
        return re.sub(r'\s+', '', t).lower()
    t = unicodedata.normalize('NFC', ''.join(ch for ch in unicodedata.normalize('NFKD', t) if not unicodedata.combining(ch)))
    for a, b in RR['fold'].items():
        t = t.replace(a, b)
    t = re.sub(r'\s+', '', t)
    t = re.sub('[' + re.escape(RR['strip_chars']) + ']', '', t)
    return t.lower()


def fold_accents(s):
    return unicodedata.normalize('NFC', ''.join(ch for ch in unicodedata.normalize('NFKD', s) if not unicodedata.combining(ch)))


def tnorm(s):
    """원문 대조용(M4) — 공백 · 문장 부호 제거 · 소문자."""
    s = unicodedata.normalize('NFC', str(s or ''))
    return re.sub(r'[\s\.,·•\-–—_/\\()\[\]{}「」『』"\'`:;!?~※→←↔+*%]', '', s).lower()


UNITS = {u['id']: u for u in U5['units']}
SITES = {n['name']: n for n in S3['nodes']}
SITE_BY_ID = {n['id']: n for n in S3['nodes']}
FAM_NAME = {f['id']: f['name'] for f in F2['families']}
PRODUCTS = {it['ledger_id']: it for it in P1['items']}
PF_ROWS = collections.defaultdict(list)
for r in F2['product_family']:
    PF_ROWS[r['ledger_id']].append(r)
TECH = {n['id']: n for n in T4['nodes']}
CANON = {m['canonical']: m for m in SEM['ids']['map']}
SILVER2CANON = {}
for m in SEM['ids']['map']:
    SILVER2CANON.setdefault(m['silver_id'], m['canonical'])
PACKAGES = {p['id']: p for p in G6['packages']}


def site_chain(name):
    """부위 이름 → [자기, 부모, …] 이름."""
    out = []
    n = SITES.get(name)
    while n:
        out.append(n['name'])
        n = SITES.get(n['parent']) if n['parent'] else None
    return out


def region(name):
    ch = site_chain(name)
    return ch[-1] if ch else None  # 얼굴 · 목(묶음) · 두피 · 바디 · None(해당 없음 · 병변 단위)


def site_rel(unit_site, want_sites):
    """단위 시술 부위 ↔ 원천이 말한 부위. 반환: 부위 안 · 상위 · 하위 · 얼굴 전체 · 다른 부위(같은 영역) · 다른 영역 · 부위 없음."""
    if not want_sites:
        return '원천 부위 없음'
    if unit_site in ('해당 없음', '병변 단위', None):
        return '부위 없음(단위 시술)'
    best = None
    order = ['부위 안', '하위', '상위', '얼굴 전체', '다른 부위(같은 영역)', '다른 영역']
    for w in want_sites:
        w = w if w in SITES else None
        if not w:
            continue
        uc, wc = site_chain(unit_site), site_chain(w)
        if unit_site == w:
            r = '부위 안'
        elif w in uc:
            r = '하위'
        elif unit_site in wc:
            r = '상위'
        elif unit_site == '얼굴 전체' and region(w) == '얼굴':
            r = '얼굴 전체'
        elif region(unit_site) == region(w):
            r = '다른 부위(같은 영역)'
        else:
            r = '다른 영역'
        if best is None or order.index(r) < order.index(best):
            best = r
    return best or '원천 부위 없음'


SITE_OK = {'부위 안', '하위', '상위', '얼굴 전체', '원천 부위 없음', '부위 없음(단위 시술)'}
SITE_NAMES_BY_LEN = sorted([n for n in SITES if '(묶음)' not in n], key=lambda x: -len(x))
SITE_ALIASES = {}
for n in S3['nodes']:
    for syn in n.get('synonyms') or []:
        if syn.get('weak'):
            continue
        SITE_ALIASES.setdefault(syn['text'], n['name'])


ONE_CHAR_RULE = {  # 한 글자 부위 이름은 다른 낱말 속에 잘 섞인다 — 규칙으로만 인정
    '볼': r'볼(?!륨|류)', '등': r'(?:(?<=[/,(])|^)등(?=$|[\s/,)])|등(?=\s*(?:여드름|드름|라인|살))', '발': r'(?<![가-힣])발(?![가-힣])',
    '손': r'(?<![가-힣])손(?![가-힣상])|손등|손바닥', '목': r'목(?!적|표|록|소리)', '코': r'코(?!그|팅|어|스)', '팔': r'팔(?![자뚝])', '힙': r'힙',
}


def sites_in_text(text):
    """원천 문장에서 부위 이름 · 강한 동의어 찾기(3단계 부위 이름표 = 낱말표로만 씀). 긴 이름 먼저 · 한 글자는 규칙(ONE_CHAR_RULE)."""
    t = text or ''
    found = []
    keys = set(SITE_NAMES_BY_LEN) | {k for k in SITE_ALIASES if len(k) >= 2}
    for k in sorted(keys, key=lambda x: (-len(x), x)):
        nm = k if k in SITES else SITE_ALIASES.get(k, k)
        if len(k) == 1:
            pat = ONE_CHAR_RULE.get(k)
            if not pat or not re.search(pat, t):
                continue
            t = re.sub(pat, ' ', t)
        else:
            if k not in t:
                continue
            t = t.replace(k, ' ')
        if nm not in found and nm != '얼굴':
            found.append(nm)
    return found


# ───────────────────────── 시맨틱 사전 · resolve(T1 흉내) ─────────────────────────
DICT = {}
for e in SEM['dictionary']['expressions']:
    DICT.setdefault(e['norm'], e)
DICT_KEYS = sorted(DICT)


def resolve(text):
    """골드 T1 resolve: norm 완전 일치 → 띄어쓰기 · 구분자로 나눠 낱말마다 완전 → 접두 일치(부분 일치 표시)."""
    q = norm(text)
    if q not in DICT and fold_accents(q) in DICT:  # 문서상 악센트 접기(v4 F-B) — 질의 쪽에서
        q = fold_accents(q)
    if q in DICT:
        return {'mode': '완전', 'spans': [{'span': text, 'match': '완전', 'targets': DICT[q]['targets']}], 'unmatched': []}
    toks = [t for t in re.split(RR['split'] if RR else r'[\s/·,()\[\]+]+', text or '') if t]
    spans, unmatched = [], []
    if len(toks) > 1:
        for t in toks:
            n = norm(t)
            if n in DICT:
                spans.append({'span': t, 'match': '낱말', 'targets': DICT[n]['targets']})
            else:
                unmatched.append(t)
        if spans:
            return {'mode': '낱말', 'spans': spans, 'unmatched': unmatched}
    # 끝말 떼기(2차 · 품질 H) — 질의 끝 「주사 · 시술」을 떼고 완전
    for tl in (RR or {}).get('tails') or []:
        if q.endswith(tl) and len(q) - len(tl) >= 2 and q[:-len(tl)] in DICT:
            return {'mode': '끝말', 'spans': [{'span': text, 'match': '끝말', 'targets': DICT[q[:-len(tl)]]['targets']}], 'unmatched': []}
    # 접두 일치 — 질의가 사전 표현의 앞부분(2자 이상) · 2차: 대상 계열 · 고민 대분류가 하나로 모일 때만(품질 G)
    if len(q) >= ((RR or {}).get('prefix_min') or 2):
        hits = [k for k in DICT_KEYS if k.startswith(q)]
        if hits:
            tg = []
            for k in hits[:30]:
                for t in DICT[k]['targets']:
                    if t not in tg:
                        tg.append(t)
            if RR and len(prefix_groups(tg)) != 1:
                return {'mode': '없음', 'spans': [], 'unmatched': [text], 'prefix_rejected': len(prefix_groups(tg))}
            return {'mode': '접두', 'spans': [{'span': text, 'match': '접두', 'targets': tg}], 'unmatched': []}
    return {'mode': '없음', 'spans': [], 'unmatched': toks or [text]}


def prefix_groups(tg):
    """접두 일치 대상 묶음 — 계열 코드 · 고민 대분류 · 그 밖 종류:id(품질 G)."""
    g = set()
    for t in tg:
        fs = target_families(t['id'])
        if fs:
            g |= {'family:' + f for f in fs}
        elif t['id'].startswith('concern:'):
            g.add('concern:' + str(target_concern_root(t['id'])))
        else:
            g.add(t['id'])
    return g


def all_targets(res):
    out = []
    for s in res['spans']:
        for t in s['targets']:
            if t['id'] not in [o['id'] for o in out]:
                out.append(t)
    return out


def target_families(tid):
    """정본 id → 계열 집합(정답 비교용)."""
    kind, _, key = tid.partition(':')
    if kind == 'family':
        return {key}
    if kind == 'unit_procedure':
        u = UNITS.get(key)
        return {u['key']['family']} if u and u['key']['family'] else set()
    if kind == 'product':
        fs = set()
        for r in PF_ROWS.get(key, []):
            if r.get('family'):
                fs.add(r['family'])
            fs |= set(r.get('also_families') or [])
        return fs
    if kind == 'package':
        p = PACKAGES.get(key)
        return {p['source_family']} if p and p.get('source_family') else set()
    return set()


def target_concern_root(tid):
    kind, _, key = tid.partition(':')
    if kind != 'concern':
        return None
    m = re.match(r'(P\d+)', key)
    if m:
        return m.group(1)
    for it in C7['concerns']['items']:
        if it['id'] == key:
            return it['category']
    for it in C7['concerns']['extra_items']:
        if it['id'] == key:
            return it.get('parent') and re.match(r'(P\d+)', it['parent']).group(1) if it.get('parent') else 'J'
    return None


# ───────────────────────── 고민 트리 · treats ─────────────────────────
CONCERN_NODES = {}
for c in C7['concerns']['categories']:
    if c.get('node'):
        CONCERN_NODES[c['id']] = {'id': c['id'], 'parent': None, 'sites': [], 'name': c['name']}
for c in C7['concerns']['subcategories']:
    if c.get('node'):
        CONCERN_NODES[c['id']] = {'id': c['id'], 'parent': c['parent'], 'sites': c.get('sites') or [], 'name': c.get('concern') or c.get('source_label')}
for c in C7['concerns']['items']:
    if c.get('kind') == '고민':
        CONCERN_NODES[c['id']] = {'id': c['id'], 'parent': c['subcategory'], 'sites': c.get('sites') or [], 'name': c['name']}
for c in C7['concerns']['extra_items']:
    CONCERN_NODES[c['id']] = {'id': c['id'], 'parent': c.get('parent'), 'sites': c.get('sites') or [], 'name': c['name']}


def anchor_concerns(cb):
    anc = cb.get('anchor') or {}
    out = list(anc.get('concerns') or [])
    c = anc.get('concern')
    for x in (c if isinstance(c, list) else [c]):
        if x and x not in out:
            out.append(x)
    return out


def concern_desc(cid):
    out = {cid}
    changed = True
    while changed:
        changed = False
        for k, v in CONCERN_NODES.items():
            if v['parent'] in out and k not in out:
                out.add(k)
                changed = True
    return out


TREATS = C7['edges']


LAYER_DATA = any('layer' in e for e in TREATS)  # 2차: 7단계 R32 층 표시가 있으면 U-1 ② = 데이터의 layer 「상위」를 같이 낸다
CC_DATA = any('ccs' in e for e in TREATS)


ITEM_CAT = {it['id']: it['category'] for it in C7['concerns']['items']}


def edge_root(e):
    """엣지의 원천 문제(P{n}) — ③ source_id 「P:cc」 · ①⑤ 항목 id → 항목 대분류"""
    sid = str(e.get('source_id') or '')
    if e['source'].startswith('③'):
        return sid.split(':', 1)[0]
    return ITEM_CAT.get(sid)


def recommend(concerns, site=None, face_layer=False, cc=None, roots=None):
    """골드 P-01 흉내: 고민 + 하위 → treats → 부위 층 거르기(R21: 부위 · 하위 → 상위 묶음 → [얼굴 전체 = U-1 옵션]).
    2차: face_layer='data' 면 엣지 layer 「상위」(R32 · U-1 ②)만 얼굴 전체 층으로 · cc 가 있으면 R28(그 CC 가 든 엣지만 · 하나도 없으면 CC 없이)."""
    cs = set()
    for c in concerns:
        cs |= concern_desc(c)
    units, fam_only = collections.OrderedDict(), []
    pool = [e for e in TREATS if e['from'] in cs]
    if cc and CC_DATA:  # R28 — 같은 원천 문제 안에서 그 CC 가 든 엣지(출발 노드가 고민 · 목적 · 앵커 없음이어도)
        hit = [e for e in TREATS if cc in (e.get('ccs') or []) and (not roots or edge_root(e) in roots)]
        if hit:
            pool = hit
    by_cc = bool(cc and CC_DATA and pool and all(cc in (e.get('ccs') or []) for e in pool))
    for e in pool:
        if e['target_kind'] == '계열만':
            if e['to_family'] and e['to_family'] not in fam_only:
                fam_only.append(e['to_family'])
            continue
        for uid in e['to_units']:
            units.setdefault(uid, []).append(e)
    if site:
        keep = collections.OrderedDict()
        for uid, es in units.items():
            us = UNITS[uid]['key']['site']
            # R28 CC 엣지면 질의 부위 + 그 CC 원천 부위 낱말(엣지 앵커 · R29)로 거름 — 같은 원천 문구라서
            rel = site_rel(us, [site] + ([a for e in es for a in e.get('anchor_sites') or [] if a in SITES] if by_cc else []))
            if rel in ('부위 안', '하위', '상위') or (face_layer and rel == '부위 없음(단위 시술)') or (face_layer is True and rel == '얼굴 전체') or (face_layer == 'data' and rel == '얼굴 전체' and any(e.get('layer') == '상위' for e in es)):
                keep[uid] = es
        units = keep
    return list(units), fam_only


# ───────────────────────── 시술 ↔ 시술 주장(P-07) ─────────────────────────
CLAIMS = {c['id']: c for c in R8['claims']}


def endpoint_units(ep):
    k = ep['kind']
    if k == '단위 시술':
        return {ep['id']}
    if k in ('계열', '계열 + 조건'):
        fam = ep['id']
        us = {u for u, x in UNITS.items() if x['key']['family'] == fam}
        q = ep.get('qualifier') or {}
        if isinstance(q, dict) and q.get('sub'):
            us = {u for u in us if UNITS[u]['key']['sub_family'] == q['sub']}
        return us
    if k in ('단위 시술 후보', '계열 묶음'):
        out = set()
        for c in ep['candidates']:
            if c['kind'] == 'unit_procedure':
                out.add(c['id'])
            elif c['kind'] == 'family':
                out |= {u for u, x in UNITS.items() if x['key']['family'] == c['id']}
        return out
    if k == '모든 시술':
        return set(UNITS)
    return set()


EDGE_UNITS = []
for e in R8['edges']:
    EDGE_UNITS.append((e, endpoint_units(e['endpoints']['a']), endpoint_units(e['endpoints']['b'])))


def cond_stated(c, qtext):
    """2차: 조건부 주장(끝점 scope 「조건부 — 단위 시술 미특정」 · default_apply false)은 질의가 그 끝점 조건 낱말(qualifier)을 말할 때 켠다
    — reading_contract 「조회 옵션으로만」의 조회 옵션 = 질의에 조건이 있음(예: 「심부 필링(TCA 50%+/페놀)」 → qualifier 「심부 · TCA 50%+/페놀」)."""
    if not qtext:
        return False
    qn = norm(qtext)
    for side in ('a', 'b'):
        ep_ = c.get(side) or {}
        if ep_.get('default_apply') is False or '조건부' in str(ep_.get('scope') or ''):
            toks = [t for t in re.split(r'[\s·/,()]+', ep_.get('qualifier') or '') if len(norm(t)) >= 2]
            if toks and any(norm(t) in qn for t in toks):
                return True
    return False


def pair_claims(ua, ub, include_conditional=False, qtext=None):
    out = []
    for e, A, Bs in EDGE_UNITS:
        if ((ua in A and ub in Bs) or (ub in A and ua in Bs)) and (ua != ub or e.get('self_pair') or e['endpoints']['a'] == e['endpoints']['b']):
            for cid in e['claims']:
                if not include_conditional and cid in e.get('conditional_claims', []) and not cond_stated(CLAIMS[cid], qtext):
                    continue
                c = CLAIMS[cid]
                flip = not (ua in A and ub in Bs)
                out.append((c, flip))
    return out


# 충돌 판: 8단계에 충돌 해소 칸(resolution_rule · alternatives · resolved{…})이 생기면 그 값으로 센다.
# 지금 판의 claims[].resolved 는 bool(끝점 풀림) — dict 일 때만 해소 값으로 본다.
def _has_resolution(o):
    return isinstance(o, dict) and ('resolution_rule' in o or isinstance(o.get('resolved'), dict))


CONFLICT_BOARD = ('해소 판(resolved 기준)' if any(_has_resolution(x) for x in R8['claims'] + R8['edges'] + R8.get('conflicts', []))
                  else '지금 판(충돌 그대로 · resolved 칸 없음)')
EDGE_RES = {e['id']: e for e in R8['edges'] if _has_resolution(e)}
USE_RES = bool(EDGE_RES)  # main() 이 지금 판(raw) · 해소 판 둘 다 돌린다


def claim_interval(c):
    iv = dict(c.get('interval') or {})
    if isinstance(c.get('resolved'), dict):
        iv.update({k: v for k, v in c['resolved'].items() if k in ('days', 'same_day', 'first', 'options')})
    return iv


def pair_summary(ua, ub, qtext=None):
    cl = pair_claims(ua, ub, qtext=qtext)
    sd, days, first, kinds = set(), [], set(), set()
    # 해소 판: 쌍에 걸린 엣지에 resolved dict 가 있으면 그 값 하나로
    if USE_RES and EDGE_RES:
        for e, A, Bs in EDGE_UNITS:
            if e['id'] in EDGE_RES and ((ua in A and ub in Bs) or (ub in A and ua in Bs)) and isinstance(e.get('resolved'), dict):
                rv = e['resolved']
                # 2차: reading_contract 대로 — 겉 same_day 가 null 이면 by_direction(질문 순서 = 앞 시술 먼저) · 그다음 options 의 「순서」 조건 값(품질 O)
                dkey = 'a' if ua in A else 'b'
                if rv.get('same_day') is not None:
                    sd.add(rv['same_day'])
                elif (rv.get('by_direction') or {}).get(dkey, {}).get('same_day') is not None:
                    sd.add(rv['by_direction'][dkey]['same_day'])
                else:
                    ov = [o for o in rv.get('options') or [] if o.get('field') == 'same_day' and o.get('same_day') is not None and (o.get('sub_condition') or {}).get('순서') == dkey]
                    for o in ov:
                        sd.add(o['same_day'])
                if rv.get('days'):
                    days.append(rv['days'])
                if rv.get('first') in ('a', 'b'):
                    first.add(rv['first'] if (ua in A) else ('b' if rv['first'] == 'a' else 'a'))
        if sd or days or first:
            return {'n': len(cl), 'same_day': sorted(sd, key=str), 'days': days, 'first': sorted(first), 'kinds': [], 'ids': [c['id'] for c, _ in cl], 'board': 'resolved'}
    for c, flip in cl:
        iv = claim_interval(c)
        kinds.add(c['kind'])
        if iv.get('same_day') is not None:
            sd.add(iv['same_day'])
        if iv.get('days'):
            days.append(iv['days'])
        if iv.get('first') in ('a', 'b'):
            f = iv['first']
            if flip:
                f = 'b' if f == 'a' else 'a'
            first.add(f)
        for o in iv.get('options') or []:
            if o.get('same_day') is not None:
                sd.add(o['same_day'])
            if o.get('days'):
                days.append(o['days'])
    return {'n': len(cl), 'same_day': sorted(sd, key=str), 'days': days, 'first': sorted(first), 'kinds': sorted(kinds),
            'ids': [c['id'] for c, _ in cl]}


# ───────────────────────── 안전 묶음(G13) ─────────────────────────
COND_NODES = {n['id']: n for n in R8['conditions']['nodes']}


def unit_products(uid):
    return [p['product'] for p in UNITS[uid].get('uses_product') or []]


def cond_target(c):
    """확인 조건 주장 대상 → (계열 집합, 단위 시술 집합, 제품 집합). target 꼴 = str · dict · list."""
    t = c.get('target')
    fams, units, prods = set(), set(), set()
    for x in (t if isinstance(t, list) else [t]):
        if isinstance(x, str):
            k, _, v = x.partition(':')
            if k == 'family':
                fams.add(v)
            elif k in ('unit', 'units'):
                units |= set(v.split(','))
            elif k == 'product':
                prods.add(v)
        elif isinstance(x, dict):
            if x.get('units'):
                units |= set(x['units'])
            else:
                fams |= set(x.get('families') or [])
    return fams, units, prods


def unit_checks(uid):
    u = UNITS[uid]
    fam = u['key']['family']
    prods = set(unit_products(uid))
    out = []
    for c in R8['conditions']['claims']:
        if c.get('target_level') in ('공통', '모든 시술'):
            continue  # 전역은 따로(G16)
        f, us, ps = cond_target(c)
        if fam in f or uid in us or (ps & prods):
            out.append(c)
    return out


def unit_safety(uid):
    u = UNITS[uid]
    fam = u['key']['family']
    site = u['key']['site']
    sf = R8['safety']
    d = {
        'complications': [x for x in sf['complications'] if x['family'] == fam],
        'side_effects': [x for x in sf['side_effects'] if x.get('attach') == f'family:{fam}'],
        'checks': unit_checks(uid),
        'site_caution': [x for x in sf['site_caution'] if x['family'] == fam and (x['site'] == site or site in site_chain(x['site']) or x['site'] in site_chain(site))],
        'timelines': [x for x in sf['timelines'] if (x.get('attach') == f'family:{fam}' and not x.get('units')) or uid in (x.get('units') or [])],
        'pih': [x for x in sf['pih'] if uid in (x.get('units') or [])],
        'family_text': list((sf['family_text'].get(fam) or {}).keys()),
        'forbid_relations': [],
        'gap': [g for g in sf.get('unit_gaps') or [] if g['unit'] == uid],  # 2차: G13 「gap 상태」 — 「정보 없음(gap)」을 명시해 내면 안전 묶음을 낸 것(없음 = 안전 아님)
    }
    for e, A, Bs in EDGE_UNITS:
        if uid in A or uid in Bs:
            if any(k in ('간격 금기', '조합 금기', '같은 날 불가') for k in e['kinds']) and not (e['endpoints']['a']['kind'] == '모든 시술'):
                d['forbid_relations'].append(e['id'])
    return d


# ───────────────────────── 샘플 낱말 ─────────────────────────
def sample_texts():
    t = open(SAMPLE, encoding='utf-8').read()
    t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
    return t


SAMPLE_RAW = sample_texts()


def in_sample(s):
    return s in SAMPLE_RAW


# ═════════════════════════ 문항 세트(M1) ═════════════════════════
def bronze_ref(file, path, text):
    return {'file': file, 'path': path, 'text': text}


def build_eval_set():
    Q = []

    def add(**kw):
        kw['id'] = f"Q{len(Q) + 1:03d}"
        Q.append(kw)

    # ── I-01 고민 × 부위: 샘플 3 ──
    sample_concerns = [
        ('이마 주름', '이마', 'P2', 3),
        ('팔자', '팔자', 'P2', 4),
        ('턱선 처짐', '턱선', 'P3', 5),
    ]
    for text, site, prob, step in sample_concerns:
        assert in_sample(text)
        ev, fams = [], set()
        for p in b_pp['problems']:
            if p['problem_id'] != prob:
                continue
            for i, cpl in enumerate(p['complaints']):
                blob = ' '.join([cpl['cc'], cpl.get('cc_detail') or '', cpl.get('cc_group') or ''])
                if site in blob or (site == '팔자' and '팔자' in blob):
                    for pr in cpl['procedures']:
                        fams.add(pr['category'])
                    ev.append(bronze_ref('problem-packages.json', f"problems[{prob}].complaints[{i}]", f"{cpl['cc']} · {cpl.get('cc_group')} → " + ' · '.join(f"{x['name']}({x['category']})" for x in cpl['procedures'])))
        add(intent='I-01', origin=f'샘플 {step}단계', text=text, slots={'concern_text': text, 'site': site},
            answer={'families': sorted(fams), 'site': site, 'must_not': '다른 부위 · 다른 영역 단위 시술'} if fams else None,
            answer_state='정답 있음' if fams else '정답 미정', evidence=ev)

    # ── I-01 고민 × 부위: 원천 사이트 「고민 선택 → 주요 호소(CC) → 효과 시술」 · 갈래마다 cc_group 다른 것 최대 2 ──
    for p in b_pp['problems']:
        seen = []
        for i, cpl in enumerate(p['complaints']):
            g = cpl.get('cc_group') or cpl['cc']
            if g in seen:
                continue
            seen.append(g)
            if len(seen) > 2:
                break
            fams = sorted({x['category'] for x in cpl['procedures'] if x.get('category')})
            subs = {f: sorted(source_subs(cpl['procedures'], f, cpl['cc'])) for f in fams if source_subs(cpl['procedures'], f, cpl['cc'])}
            add(intent='I-01', origin='원천 problem-packages(사이트 고민별 시술 추천)', text=f"{p['problem']} · {cpl['cc']}",
                slots={'concern_text': p['problem'], 'cc': cpl['cc'], 'cc_group': g, 'cc_detail': cpl.get('cc_detail')},
                answer={'families': fams, 'sub_families': subs, 'site_words': sites_in_text(' '.join([cpl['cc'], g, cpl.get('cc_detail') or ''])),
                        'must_not': '다른 부위 · 다른 영역 단위 시술'},
                answer_state='정답 있음',
                evidence=[bronze_ref('problem-packages.json', f"problems[{p['problem_id']}].complaints[{i}]",
                                     f"{cpl['cc']} [{g}] → " + ' · '.join(f"{x['name']}({x['category']}, {x.get('role')})" for x in cpl['procedures']))])

    # ── I-02 시술 설명: 샘플 소프웨이브 + patient-education 계열 8 ──
    pe9 = next(x for x in b_pe['categories'] if x['id'] == 'M9')
    add(intent='I-02', origin='샘플 7단계', text='소프웨이브', slots={'procedure': '소프웨이브'},
        answer={'families': ['M9'], 'must_show': [pe9['simple_explanation']]}, answer_state='정답 있음',
        evidence=[bronze_ref('taxonomy.json', 'modality[M9] 소프웨이브 원장 행(5단계 U5-140 근거)', '소프웨이브 · 초음파 1.5mm · 민감부위 적합'),
                  bronze_ref('patient-education.json', 'categories[M9].simple_explanation', pe9['simple_explanation'])])
    for c in b_pe['categories'][:17:2]:
        add(intent='I-02', origin='원천 patient-education', text=c['name'], slots={'procedure': c['name']},
            answer={'families': [c['id']], 'must_show': [c['simple_explanation']]}, answer_state='정답 있음',
            evidence=[bronze_ref('patient-education.json', f"categories[{c['id']}].simple_explanation", c['simple_explanation'])])

    # ── I-03 주의 · 사후관리: 샘플 사우나(M9) + procedure-profiles aftercare ──
    pf9 = next(x for x in b_pf['profiles'] if x['id'] == 'M9')
    ult = next(i for s in next(m for m in b_tax['modality'] if m['id'] == 'M9')['subcategories'] for i in s['items'] if i['id'] == 'M9-1-1')
    add(intent='I-03', origin='샘플 8단계', text='소프웨이브 · 사우나', slots={'procedure': '소프웨이브', 'topic': 'aftercare'},
        answer={'families': ['M9'], 'must_show': [x for x in pf9['aftercare'] if '사우나' in x],
                'note': '샘플 「시술 후 2주 사우나」는 원천에 없음 — 원천은 「당일」(procedure-profiles) · 「24시간」(taxonomy 울쎄라 aftercare)'},
        answer_state='정답 있음(원천 2갈래 · 의료진 확인)',
        evidence=[bronze_ref('procedure-profiles.json', 'profiles[M9].aftercare', ' / '.join(pf9['aftercare'])),
                  bronze_ref('taxonomy.json', 'modality[M9].items[M9-1-1].extracted.aftercare[0]', ult['extracted']['aftercare'][0])])
    for pid in ['M1', 'M2', 'M7', 'M8', 'M4', 'M11']:
        pf = next(x for x in b_pf['profiles'] if x['id'] == pid)
        add(intent='I-03', origin='원천 procedure-profiles', text=f"{pf['name']} · 사후관리", slots={'procedure': pf['name'], 'topic': 'aftercare'},
            answer={'families': [pid], 'must_show': pf.get('aftercare') or []}, answer_state='정답 있음' if pf.get('aftercare') else '정답 미정',
            evidence=[bronze_ref('procedure-profiles.json', f'profiles[{pid}].aftercare', ' / '.join(pf.get('aftercare') or []))])

    # ── I-04 부작용 · 합병증: complications.json 계열 10 ──
    for cat in b_cx['categories']:
        add(intent='I-04', origin='원천 complications', text=f"{cat['name']} · 부작용", slots={'procedure': cat['name']},
            answer={'families': [cat['id']], 'must_show': [x['name'] for x in cat['complications']]}, answer_state='정답 있음',
            evidence=[bronze_ref('complications.json', f"categories[{cat['id']}].complications[].name", ' · '.join(f"{x['name']}({x['severity']})" for x in cat['complications']))])

    # ── I-05 회복 · 지속: 샘플 M9 + patient-education 4 ──
    for c in [pe9] + [x for x in b_pe['categories'] if x['id'] in ('M1', 'M2', 'M7', 'M8')]:
        add(intent='I-05', origin='샘플 6단계' if c is pe9 else '원천 patient-education', text=f"{c['name']} · 회복", slots={'procedure': c['name']},
            answer={'families': [c['id']], 'must_show': [c['downtime'], c['duration_simple']]}, answer_state='정답 있음',
            evidence=[bronze_ref('patient-education.json', f"categories[{c['id']}].downtime · duration_simple", f"{c['downtime']} / {c['duration_simple']}")])

    # ── I-06 비교: 샘플 Ulthera ↔ Sofwave + procedure-comparison 첫 두 시술 ──
    add(intent='I-06', origin='샘플 10단계(조합 A ↔ B)', text='Ulthera ↔ Sofwave', slots={'procedures': ['Ulthera', 'Sofwave']},
        answer={'families_each': [['M9'], ['M9']]}, answer_state='정답 있음',
        evidence=[bronze_ref('procedure-comparison.json', 'comparisons[lifting].procedures[0]', '울쎄라 (HIFU) · M9'),
                  bronze_ref('taxonomy.json', '원장 소프웨이브 행', '소프웨이브 · 초음파 1.5mm')])
    for cmpx in b_cmp['comparisons'][:6]:
        a, b2 = cmpx['procedures'][0], cmpx['procedures'][1]
        add(intent='I-06', origin='원천 procedure-comparison', text=f"{a['name']} ↔ {b2['name']}", slots={'procedures': [a['name'], b2['name']]},
            answer={'families_each': [[a['category']], [b2['category']]]}, answer_state='정답 있음',
            evidence=[bronze_ref('procedure-comparison.json', f"comparisons[{cmpx['id']}].procedures[0:2]", f"{a['name']}({a['category']}) ↔ {b2['name']}({b2['category']})")])

    # ── I-07 같이 · 순서 · 간격 ──
    # 샘플 조합 A 쌍 3 — 원천 contraindications.rules 계열 쌍
    def ci_rule(f1, f2):
        for i, r in enumerate(b_ci['rules']):
            if {r['from'], r['to']} == {f1, f2}:
                return i, r
        return None, None
    for (na, fa), (nb, fb) in [(('소프웨이브', 'M9'), ('팔자 필러', 'M2')), (('소프웨이브', 'M9'), ('이마 보톡스', 'M1')), (('팔자 필러', 'M2'), ('이마 보톡스', 'M1'))]:
        i, r = ci_rule(fa, fb)
        ans = None
        if r:
            ans = {'same_day': True if '가능' in (r.get('interval') or '') or r['level'] == 'safe' else (False if r['level'] in ('forbid', 'contraindicated') else None),
                   'text': f"{r['from_name']}↔{r['to_name']} {r['level']} · {r['interval']} · {r['note']}"}
        add(intent='I-07', origin='샘플 10단계 조합 A', text=f'{na} + {nb} 같은 날', slots={'procedures': [na, nb], 'same_day': True},
            answer=ans, answer_state='정답 있음' if ans else '정답 미정',
            evidence=[bronze_ref('contraindications.json', f'rules[{i}]', ans['text'])] if ans else [])
    # incompatible_same_day 9
    for i, x in enumerate(b_ts['incompatible_same_day']):
        pair = list(x['pair'])
        split_note = None
        if len(pair) == 1 and ' 주입 후 ' in pair[0]:  # 규칙: 「A 주입 후 B」 → [A, B](원문 한 칸)
            pair = pair[0].split(' 주입 후 ')
            split_note = '원문 한 칸 「A 주입 후 B」 → 규칙으로 나눔'
        ev = [bronze_ref('treatment-sequence.json', f'incompatible_same_day[{i}]', f"{x['pair']} — {x['reason']}")]
        if '복용' in pair[0]:  # 사람 조건 × 시술 — 확인 조건 쪽(I-09)
            add(intent='I-09', origin='원천 treatment-sequence.incompatible_same_day(사람 조건)', text=f"{pair[0]} · {pair[1]}",
                slots={'condition_text': pair[0], 'procedure': pair[1], 'source': 'treatment-sequence.incompatible_same_day', 'source_index': i},
                answer={'condition_present': True, 'text': x['reason']}, answer_state='정답 있음(등급은 원문 「의사 판단」 — 등급 채점 안 함)', evidence=ev)
            continue
        add(intent='I-07', origin='원천 treatment-sequence.incompatible_same_day', text=f"{pair[0]} + {pair[1]} 같은 날",
            slots={'procedures': pair, 'same_day': True, 'split_note': split_note},
            answer={'same_day': False, 'text': x['reason']}, answer_state='정답 있음', evidence=ev)
    # minimum_intervals 9
    for i, x in enumerate(b_ts['minimum_intervals']):
        md = x['min_days'] if 'min_days' in x else x.get('min_months', 0) * 30
        unit_txt = f"{x['min_days']}일" if 'min_days' in x else f"{x.get('min_months')}개월"
        ev = [bronze_ref('treatment-sequence.json', f'minimum_intervals[{i}]', f"{x['from']} → {x['to']} {unit_txt} · {x['reason']}")]
        if x['from'] == '이소트레티노인':  # 약 복용 = 사람 조건 → 확인 조건(I-09)
            add(intent='I-09', origin='원천 treatment-sequence.minimum_intervals(사람 조건)', text=f"{x['from']} · {x['to']}",
                slots={'condition_text': x['from'], 'procedure': x['to'], 'source': 'treatment-sequence.minimum_intervals', 'source_index': i},
                answer={'condition_present': True, 'text': x['reason']}, answer_state='정답 있음(등급 채점 안 함)', evidence=ev)
            continue
        to = re.sub(r'\s*\((별도 세션|동일 부위 재시술)\)', '', x['to'])  # 규칙: 괄호 수식 떼기(원문 보관)
        ans = {'same_day': True, 'first': 'a', 'text': x['reason']} if md == 0 else {'min_days': md, 'first': 'a', 'text': x['reason']}
        add(intent='I-07', origin='원천 treatment-sequence.minimum_intervals', text=f"{x['from']} → {x['to']} 간격",
            slots={'procedures': [x['from'], to], 'self_pair': to == x['from']}, answer=ans, answer_state='정답 있음', evidence=ev)

    # ── I-08 이전 시술 뒤: 샘플 6주 전 보톡스 → 소프웨이브 ──
    i, r = ci_rule('M1', 'M9')
    add(intent='I-08', origin='샘플 공통 칸(六週前施打過肉毒)', text='6주 전 보톡스 → 소프웨이브', slots={'prior': '보톡스', 'procedure': '소프웨이브', 'elapsed_days': 42},
        answer={'ok': True, 'text': f"{r['from_name']}↔{r['to_name']} {r['level']} · {r['interval']} · {r['note']}"} if r else None,
        answer_state='정답 있음' if r else '정답 미정',
        evidence=[bronze_ref('contraindications.json', f'rules[{i}]', f"{r['from']}↔{r['to']} {r['interval']}")] if r else [])

    # ── I-09 확인 조건: pre-procedure-checklist absolute_contraindication(계열마다 첫 1) + 샘플 통증 민감 ──
    n = 0
    for cat in b_pre['category_specific']:
        for j, ch in enumerate(cat['checks']):
            if ch['type'] == 'absolute_contraindication':
                add(intent='I-09', origin='원천 pre-procedure-checklist', text=f"{cat['name']} · {ch['label']}", slots={'procedure': cat['name'], 'condition_text': ch['label']},
                    answer={'families': [cat['id']], 'grade3': '금기', 'condition_text': ch['label']}, answer_state='정답 있음',
                    evidence=[bronze_ref('pre-procedure-checklist.json', f"category_specific[{cat['id']}].checks[{j}]", f"{ch['label']} ({ch['type']})")])
                n += 1
                break
        if n >= 8:
            break
    add(intent='I-09', origin='샘플 공통 칸(對疼痛較敏感)', text='소프웨이브 · 통증 민감', slots={'procedure': '소프웨이브', 'condition_text': '통증 민감'},
        answer={'families': ['M9'], 'must_show': [pe9['pain_level']], 'note': '확인 조건 노드 아님 — 원천은 통증 · 마취 칸'}, answer_state='정답 있음',
        evidence=[bronze_ref('patient-education.json', 'categories[M9].pain_level', pe9['pain_level']),
                  bronze_ref('procedure-profiles.json', 'profiles[M9].needsAnesthesia', pf9['needsAnesthesia'])])

    # ── I-10 용량 · 제품: 샘플 Voluma 2cc · 원천 products.json 필러 ──
    fl = b_prod['filler_ha']['products']
    vol = [p for p in fl if 'oluma' in (p.get('name_en') or '') or '볼루마' in p['name']]
    add(intent='I-10', origin='샘플 9단계(Juvéderm Voluma 2cc)', text='Voluma', slots={'product': 'Voluma', 'amount': '2cc'},
        answer={'families': ['M2'], 'product_in_source': bool(vol)} if vol else None, answer_state='정답 있음' if vol else '정답 미정(원천 품목 없음)',
        evidence=[bronze_ref('products.json', 'filler_ha.products[].name', ' · '.join(p['name'] for p in fl))])
    for p in fl[:3]:
        add(intent='I-10', origin='원천 products.json filler_ha', text=p['name'], slots={'product': p['name']},
            answer={'families': ['M2']}, answer_state='정답 있음',
            evidence=[bronze_ref('products.json', 'filler_ha.products[]', f"{p['name']} · {p.get('name_en')} · {p.get('manufacturer')}")])

    # ── I-11 추천 조합: problem-combos 고민 갈래 ──
    for c in b_pc['combos'][:6]:
        fams = sorted({f for pk in c['packages'] for f in pk['procedures']})
        add(intent='I-11', origin='원천 problem-combos', text=f"{c['problem']} · 추천 조합", slots={'concern_text': c['problem']},
            answer={'n_packages': len(c['packages']), 'families': fams}, answer_state='정답 있음',
            evidence=[bronze_ref('problem-combos.json', f"combos[{c['problem_id']}].packages[]", ' / '.join(f"{pk['name']}({'+'.join(pk['procedures'])})" for pk in c['packages']))])

    # ── I-12 가격 — 연결 층(이번 범위 밖) · 문항 0
    return Q


# 계열 옮김 표(원천 계열 코드 → 실버 계열) — 2단계 제품 계열 옮김 · 5단계 단위 시술 계열 결정. 정답(원천 코드)과 실버 계열을 비교할 때 쓴다.
MOVE_SRC = collections.defaultdict(set)  # (원천 계열, 실버 계열) → 어디서 왔나(리포트 · 3차)


def _move_pairs():
    """계열 옮김 표(3차 · 골드 전 정리 10-30) — 손 표가 아니라 단계 산출 · 결정 파일에서 읽는다.
    ① 2단계 product_family(원장 코드 ≠ 판정 계열) ② 2단계 결정 step2-step5-decisions row_family · new_rows(원장 코드 → 계열)
    ③ 5단계 결정 원장 행선지 ledger[].units(원장 원천 계열 → 단위 시술 계열) ④ 5단계 정본 단위 시술 원천 계열(unit_source_fams)
    ⑤ 7단계 결정 resolver.fam_kw — 원천 이름(problem-packages 추천 시술 · taxonomy 고민 항목)에 낱말이 들면 (원천 category · modality → fam_kw 계열 · 고정 단위 시술 계열)"""
    def add(a, b, why):
        if a and b and a != b:
            MOVE_SRC[(a, b)].add(why)
    for r in F2['product_family']:
        if r.get('family') and r.get('step1_code') and r['family'] != r['step1_code'] and r.get('verdict') != '맞음':
            add(r['step1_code'], r['family'], '2단계 product_family')
    D2 = SL('step2-step5-decisions.json')
    for r in (D2.get('row_family') or []) + (D2.get('new_rows') or []):
        m_ = re.match(r'(M\d+|N\d+)', str(r.get('ledger_id') or ''))
        if m_:
            add(m_.group(1), r.get('family'), '2단계 결정 row_family · new_rows')
    D5 = SL('step5-decisions.json')
    UK = {u['id']: u['key']['family'] for u in D5['units']}
    LF = {l['id']: l.get('source_family') for l in U5['ledger']}
    for l in D5['ledger']:
        for uid in l.get('units') or []:
            add(LF.get(l['id']), UK.get(uid), '5단계 결정 원장 행선지')
    for u in U5['units']:
        for f in unit_source_fams(u):
            add(f, u['key']['family'], '5단계 단위 시술 원천 계열')
    D7 = SL('step7-decisions.json')
    kws = []
    for x in D7['resolver']['fam_kw']:
        tf = set(x.get('families') or []) | {UK[i] for i in x.get('units') or [] if i in UK}
        if tf:
            kws.append((x['kw'], tf))
    names = [(pr['name'], pr.get('category')) for p_ in b_pp['problems'] for c in p_['complaints'] for pr in c['procedures']]
    names += [(it['name'], f) for p_ in b_tax['problem'] for s_ in p_['subcategories'] for it in s_['items'] for f in it.get('modality_ref') or []]
    for nm, cat in names:
        for kw, tf in kws:
            if kw.lower() in (nm or '').lower():
                for f in tf:
                    add(cat, f, '7단계 결정 fam_kw 「' + kw + '」')
    return set(MOVE_SRC)


MOVE_PAIRS = None


def fam_hit(exp, got):
    """정답 계열(원천 코드) 중 맞은 것 · 그중 옮김 표로 맞은 것."""
    global MOVE_PAIRS
    if MOVE_PAIRS is None:
        MOVE_PAIRS = _move_pairs()
    hit, via = set(), set()
    for x in exp:
        if x in got:
            hit.add(x)
        elif any((x, y) in MOVE_PAIRS for y in got):
            hit.add(x)
            via.add(x)
    return hit, via


# ═════════════════════════ M1 실행 ═════════════════════════
def resolve_procedure(text):
    """시술 말 → 단위 시술 · 제품 · 계열 후보(P-02 첫 단계)."""
    res = resolve(text)
    tg = all_targets(res)
    tg = [t for t in tg if t['id'].split(':')[0] in ('unit_procedure', 'product', 'family', 'package', 'scope')]
    return res, tg


def fams_of(tg):
    out = set()
    for t in tg:
        out |= target_families(t['id'])
    return out


def units_of(tg):
    """후보 → 단위 시술(제품이면 쓰는 단위 시술 · 계열이면 그 계열 전부)."""
    out = []
    for t in tg:
        k, _, key = t['id'].partition(':')
        if k == 'unit_procedure':
            out.append(key)
        elif k == 'scope':  # 「모든 시술」(G16 와일드카드) — 모든 단위 시술
            out += sorted(UNITS)
        elif k == 'product':
            for u in UNITS.values():
                if key in unit_products(u['id']):
                    out.append(u['id'])
            for pl in U5['product_links']:
                if pl.get('product') == key:
                    for x in (pl.get('units') or []) + [c.get('unit') for c in (pl.get('inherited_candidates') or []) if isinstance(c, dict)]:
                        if x:
                            out.append(x)
    seen = []
    for u in out:
        if u not in seen:
            seen.append(u)
    return seen


def silver_text_for_family(fam):
    """계열에 닿는 실버 원문(family_text · 근거 문장 · 부작용 · 합병증 · 타임라인 · 확인 조건)."""
    sf = R8['safety']
    out = []
    def walk(o):
        if isinstance(o, str):
            out.append(o)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(sf['family_text'].get(fam) or {})
    walk([x for x in sf['side_effects'] if x.get('attach') == f'family:{fam}'])
    walk([x for x in sf['complications'] if x['family'] == fam])
    walk([x for x in sf['timelines'] if x.get('attach') == f'family:{fam}'])
    walk([x for x in R8['evidence']['statements'] if x['family'] == fam])
    return out


def contains_text(haystack_list, needle):
    n = tnorm(needle)
    if not n:
        return True
    return any(n in tnorm(h) for h in haystack_list)


I01_MODES = {'v1': '1차 경로(부위 층만 · CC 없음)', 'nocc': 'CC 없음(R32 층 표시 · U-1 ②)', 'cc': 'CC 슬롯(R28 · 골드 도구 입력 후보 cc?) + R32'}


def run_m1(Q, i01_mode='cc'):
    rows = []
    for q in Q:
        it = q['intent']
        a = q['answer']
        r = {'id': q['id'], 'intent': it, 'text': q['text'], 'answer_state': q['answer_state']}
        if a is None:
            r.update(status='정답 미정', recall=None, precision=None, safety_missing=[], why=['원천 근거 없음 — 채점 안 함'])
            rows.append(r)
            continue
        why, safety_missing = [], []
        recall = precision = None
        if it == 'I-01':
            sl = q['slots']
            parts = [sl['concern_text']] + ([sl['cc_group']] if sl.get('cc_group') else []) + ([sl['cc']] if sl.get('cc') else [])
            concerns, site, direct_units = [], sl.get('site'), []
            roots = set()
            res_log = []
            for ptxt in parts:
                res = resolve(ptxt)
                res_log.append({'text': ptxt, 'mode': res['mode'], 'targets': [t['id'] for t in all_targets(res)][:8], 'unmatched': res['unmatched']})
                for t in all_targets(res):
                    k, _, key = t['id'].partition(':')
                    if ptxt == sl['concern_text']:  # 질의 고민 말의 원천 문제(P) — R28 CC 찾기 범위
                        if k == 'concern' and target_concern_root(t['id']):
                            roots.add(target_concern_root(t['id']))
                        elif (t.get('qualifier') or {}).get('taxonomy_entry'):
                            roots.add(re.match(r'(P\d+)', t['qualifier']['taxonomy_entry']).group(1))
                    if k == 'concern' and key not in concerns:
                        concerns.append(key)
                    elif k == 'site' and not site:
                        site = SITE_BY_ID.get(key, {}).get('name')
                    elif k == 'unit_procedure':
                        direct_units.append(key)
            r['resolve'] = res_log
            # 골드 P-01: 가장 구체적인 고민만(조상 · 자손이 같이 잡히면 자손) · 고민 노드에 부위 1개면 그 부위 · 부위만 있으면 그 부위 고민
            concerns = [c for c in concerns if not any(c != d and d in concern_desc(c) for d in concerns)]
            if not site:
                ss = {x for c in concerns for x in CONCERN_NODES.get(c, {}).get('sites') or []}
                if len(ss) == 1:
                    site = next(iter(ss))
            if site and not concerns:
                concerns = [k for k, v in CONCERN_NODES.items() if any(site_rel(site, [x]) in ('부위 안', '상위') or x == site for x in v['sites'])]
                r['concerns_from_site'] = concerns
            fl = False if (i01_mode == 'v1' or not LAYER_DATA) else 'data'
            got_units, fam_only = recommend(concerns, site, face_layer=fl, cc=sl.get('cc') if i01_mode == 'cc' else None, roots=roots)
            got_face, _ = recommend(concerns, site, face_layer=True, cc=sl.get('cc') if i01_mode == 'cc' else None, roots=roots)
            r['i01_mode'] = I01_MODES[i01_mode]
            if not concerns:  # 고민을 못 찾았을 때만 시술 말로 잡힌 단위 시술을 답으로
                got_units = list(dict.fromkeys(got_units + direct_units))
            r['direct_units_ignored'] = direct_units if concerns else []
            gf_face = {UNITS[u]['key']['family'] for u in got_face} | set(fam_only)
            r['recall_with_face_layer'] = (len(fam_hit(set(a['families']), gf_face)[0]) / len(a['families'])) if a['families'] else None
            fw = []
            for u in got_face:
                se = (a.get('sub_families') or {}).get(UNITS[u]['key']['family'])
                if se and UNITS[u]['key'].get('sub_family') and UNITS[u]['key']['sub_family'] not in se:
                    fw.append(f"{UNITS[u]['name']}(원천 하위 {se})")
            r['face_layer_wrong_sub'] = fw
            r['got'] = {'concerns': concerns, 'site': site, 'units': got_units, 'family_only': fam_only, 'units_with_face_layer': got_face}
            exp = set(a['families'])
            got_f = {UNITS[u]['key']['family'] for u in got_units} | set(fam_only)
            hit, via = fam_hit(exp, got_f)
            recall = len(hit) / len(exp) if exp else None
            if via:
                why.append('계열 옮김 표로 맞음 ' + ','.join(sorted(via)))
            want_sites = [a['site']] if a.get('site') else a.get('site_words') or []
            bad, ok = [], 0
            for u in got_units:
                fam = UNITS[u]['key']['family']
                rel = site_rel(UNITS[u]['key']['site'], want_sites)
                sub_ok = True
                subs_exp = (a.get('sub_families') or {}).get(fam)
                if subs_exp and UNITS[u]['key'].get('sub_family') and UNITS[u]['key']['sub_family'] not in subs_exp:
                    sub_ok = False
                if fam_hit(exp, {fam})[0] and rel in SITE_OK and sub_ok:
                    ok += 1
                elif fam_hit(exp, {fam})[0] and rel in SITE_OK:
                    bad.append({'unit': u, 'name': UNITS[u]['name'], 'family': fam, 'site': UNITS[u]['key']['site'], 'why': f"하위 계열 밖(원천 제품 하위 {subs_exp})"})
                else:
                    bad.append({'unit': u, 'name': UNITS[u]['name'], 'family': fam, 'site': UNITS[u]['key']['site'],
                                'why': ('계열 밖' if not fam_hit(exp, {fam})[0] else '') + ('' if rel in SITE_OK else (' · ' if not fam_hit(exp, {fam})[0] else '') + rel)})
            precision = ok / len(got_units) if got_units else None
            r['wrong_units'] = bad
            if not concerns:
                why.append('고민 노드 못 찾음(resolve)')
            miss = sorted(exp - hit)
            if miss:
                why.append('빠진 계열 ' + ','.join(miss))
            if bad:
                kinds = collections.Counter(b['why'] for b in bad)
                why.append('틀린 단위 시술 ' + ' · '.join(f'{k} {v}' for k, v in kinds.items()))
            if not got_units and not fam_only:
                why.append('결과 0')
            # 안전: 나온 단위 시술마다 안전 묶음이 하나라도 있는가
            for u in got_units:
                s = unit_safety(u)
                if not any(s[k] for k in ('complications', 'side_effects', 'checks', 'site_caution', 'timelines', 'forbid_relations', 'gap')):
                    safety_missing.append(f'{u} 안전 정보 0')
        elif it == 'I-09' and a.get('condition_present'):
            sl = q['slots']
            hit = [c for c in R8['conditions']['claims'] + R8['claims'] if c['source'] == sl['source'] and str(c['source_index']).split('.')[0] == str(sl['source_index'])]
            nc = [c for c in R8['conditions']['not_condition'] if c['source'] == sl['source'] and str(c['source_index']).split('.')[0] == str(sl['source_index'])]
            r['checks_hit'] = [(c['id'], c.get('grade3') or c.get('kind'), c.get('conditions')) for c in hit]
            recall = 1.0 if hit else 0.0
            precision = None
            if not hit:
                safety_missing.append(f"원천 금기 행이 실버 주장 · 조건에 없음{' (not_condition 에만)' if nc else ''}: {q['text']}")
        elif it in ('I-02', 'I-03', 'I-04', 'I-05', 'I-09', 'I-10'):
            ptxt = q['slots'].get('procedure') or q['slots'].get('product')
            res, tg = resolve_procedure(ptxt)
            gf = fams_of(tg)
            exp = set(a.get('families') or [])
            r['resolve'] = {'mode': res['mode'], 'targets': [t['id'] for t in tg][:10], 'families': sorted(gf)}
            hit, via = fam_hit(exp, gf)
            recall = len(hit) / len(exp) if exp else None
            precision = (sum(1 for t in tg if fam_hit(exp, target_families(t['id']))[0]) / len(tg)) if tg else None
            if via:
                why.append('계열 옮김 표로 맞음 ' + ','.join(sorted(via)))
            if not tg:
                why.append(f'시술 말 「{ptxt}」 못 찾음(resolve {res["mode"]})')
            elif not hit:
                why.append(f'다른 계열로 찾음 {sorted(gf)}')
            fam = sorted(exp)[0] if exp else None
            texts = silver_text_for_family(fam) if fam else []
            if it == 'I-04':
                names_cx = {x['name'] for x in R8['safety']['complications'] if x['family'] == fam} | {x['name'] for x in R8['safety']['side_effects'] if x.get('attach') == f'family:{fam}'}
                for nm in a['must_show']:
                    if nm not in names_cx:
                        safety_missing.append(nm)
            elif it == 'I-09' and a.get('grade3'):
                pat_hit = []
                for c in R8['conditions']['claims']:
                    tf = fam in cond_target(c)[0]
                    if tf and tnorm(a['condition_text'])[:12] in tnorm(c['text']):
                        pat_hit.append(c)
                r['checks_hit'] = [(c['id'], c['grade3'], c['conditions']) for c in pat_hit]
                if not pat_hit:
                    safety_missing.append(f"확인 조건 없음: {a['condition_text']}")
                elif not any(c['grade3'] == '금기' for c in pat_hit):
                    safety_missing.append(f"등급 다름(금기 아님): {a['condition_text']} → {[c['grade3'] for c in pat_hit]}")
            else:
                for m in a.get('must_show') or []:
                    if not contains_text(texts, m):
                        safety_missing.append(m) if it in ('I-03',) else why.append(f'카드 칸 원문 없음: {m[:40]}')
            if it == 'I-03' and a.get('note'):
                why.append(a['note'])
        elif it == 'I-06':
            gfs, okn = [], 0
            for ptxt, expf in zip(q['slots']['procedures'], a['families_each']):
                res, tg = resolve_procedure(ptxt)
                gf = fams_of(tg)
                gfs.append({'text': ptxt, 'mode': res['mode'], 'families': sorted(gf), 'n': len(tg)})
                if fam_hit(set(expf), gf)[0]:
                    okn += 1
                else:
                    why.append(f'「{ptxt}」 ' + ('못 찾음' if not tg else f'다른 계열 {sorted(gf)}'))
            r['resolve'] = gfs
            recall = okn / 2
            precision = recall
        elif it in ('I-07', 'I-08'):
            names = q['slots']['procedures'] if it == 'I-07' else [q['slots']['prior'], q['slots']['procedure']]
            us = []
            rl = []
            for ptxt in names:
                res, tg = resolve_procedure(ptxt)
                uu = units_of(tg)
                if not uu:  # 계열만 찾았으면 계열 대표 단위 시술 전부
                    for f in fams_of(tg):
                        uu += [u for u, x in UNITS.items() if x['key']['family'] == f]
                rl.append({'text': ptxt, 'mode': res['mode'], 'targets': [t['id'] for t in tg][:6], 'n_units': len(uu)})
                us.append(uu)
            r['resolve'] = rl
            if not us[0] or not us[1]:
                why.append('시술 말 못 찾음 — ' + ', '.join(x['text'] for x in rl if x['n_units'] == 0))
                recall, precision = 0.0, None
                if a.get('same_day') is False or a.get('min_days'):
                    safety_missing.append(f"금기 · 간격 못 냄: {q['text']}")
            else:
                # 대표 쌍 = 첫 후보끼리(결정론) + 모든 쌍에서 주장 있는 비율
                agg = {'same_day': set(), 'days': [], 'n': 0, 'first': set()}
                pairs_with = 0
                tot = 0
                for ua in us[0][:12]:
                    for ub in us[1][:12]:
                        if ua == ub and not q['slots'].get('self_pair'):
                            continue
                        tot += 1
                        s = pair_summary(ua, ub, q['text'])
                        if s['n']:
                            pairs_with += 1
                        agg['same_day'] |= set(s['same_day'])
                        agg['days'] += s['days']
                        agg['n'] += s['n']
                        agg['first'] |= set(s['first'])
                r['got'] = {'pairs': tot, 'pairs_with_claims': pairs_with, 'same_day': sorted(agg['same_day'], key=str),
                            'days': sorted({tuple(d) for d in agg['days']})[:10], 'first': sorted(agg['first']), 'claims': agg['n']}
                ok = None
                if a.get('same_day') is None and not a.get('min_days'):
                    ok = agg['n'] > 0
                    why.append(f"원천 간격 · 주의 주장({a['text'][:40]}) → 실버 주장 {agg['n']} · days {sorted({tuple(d) for d in agg['days']})[:4]}")
                    if not ok:
                        safety_missing.append(f"간격 · 주의 못 냄: {q['text']}")
                if 'same_day' in a and a['same_day'] is not None:
                    ok = a['same_day'] in agg['same_day']
                    if agg['same_day'] == {a['same_day']}:
                        ok_text = '일치'
                    elif ok:
                        ok_text = '충돌(양쪽 값)'
                    else:
                        ok_text = '없음' if not agg['same_day'] else '반대 값만'
                    why.append(f"same_day 기대 {a['same_day']} → {ok_text}")
                    if a['same_day'] is False and not ok:
                        safety_missing.append(f"같은 날 불가 못 냄: {q['text']}")
                if a.get('min_days'):
                    lows = [d[0] for d in agg['days'] if d and d[0] is not None]
                    ok = any(lo >= a['min_days'] for lo in lows)
                    why.append(f"간격 기대 ≥{a['min_days']}일 → 하한 {sorted(set(lows))[:6] or '없음'}")
                    r['interval_values'] = {'source': a['min_days'], 'silver_lows': sorted(set(lows))}
                    if not ok:
                        safety_missing.append(f"최소 간격 못 냄: {q['text']}")
                if it == 'I-08':
                    lows = [d[0] for d in agg['days'] if d and d[0] is not None]
                    prior_ok = (not lows) or min(lows) <= q['slots']['elapsed_days']
                    ok = prior_ok == a['ok']
                    why.append(f"경과 {q['slots']['elapsed_days']}일 · 간격 하한 {sorted(set(lows)) or '없음'} → {'가능' if prior_ok else '불가'}")
                recall = 1.0 if ok else 0.0
                precision = (pairs_with / tot) if tot else None
        elif it == 'I-11':
            res = resolve(q['slots']['concern_text'])
            cs = [t['id'].split(':', 1)[1] for t in all_targets(res) if t['id'].startswith('concern:')]
            got = []
            for cb in C7['combos']:
                acs = set(anchor_concerns(cb))
                if any(acs & concern_desc(c) for c in cs):
                    got.append(cb)
            gf = {comp['family'] for cb in got for comp in cb.get('components', []) if comp.get('family')}
            exp = set(a['families'])
            hit, _ = fam_hit(exp, gf)
            recall = len(hit) / len(exp) if exp else None
            precision = (sum(1 for g in gf if fam_hit(exp, {g})[0]) / len(gf)) if gf else None
            r['got'] = {'concerns': cs, 'combos': [cb['id'] for cb in got][:20], 'families': sorted(gf)}
            if not cs:
                why.append(f"고민 말 「{q['slots']['concern_text']}」 고민 노드 못 찾음")
            if not got:
                why.append('조합 0')
        r.update(recall=recall, precision=precision, safety_missing=safety_missing, why=why)
        if it in ('I-07', 'I-08'):  # 쌍 정밀도 = 후보 쌍 중 주장 있는 비율(참고) — 맞음 판정은 값으로만
            r['status'] = '맞음' if (recall == 1.0 and not safety_missing) else '틀림'
        else:
            r['status'] = '맞음' if (recall == 1.0 and (precision is None or precision >= 0.999) and not safety_missing) else '틀림'
        rows.append(r)
    return rows


# ═════════════════════════ M2 말 → 노드 ═════════════════════════
def word_list():
    """(말, 출처, 기대) — 기대 = 원천이 그 말을 둔 자리(계열 · 고민 갈래 · 부위 · 정답 미정)."""
    W_ = []

    def add(text, origin, expect, variant=None):
        if not text:
            return
        W_.append({'text': text, 'origin': origin, 'expect': expect, 'variant': variant})

    # 샘플(한국어 · 영문 낱말 — 실명 제외)
    samp = [('이마 주름', {'concern_root': 'P2', 'site': '이마'}), ('팔자', {'site': '팔자'}), ('턱선 처짐', {'concern_root': 'P3', 'site': '턱선'}),
            ('이마', {'site': '이마'}), ('턱선', {'site': '턱선'}), ('소프웨이브', {'families': ['M9']}), ('Sofwave', {'families': ['M9']}),
            ('Ulthera', {'families': ['M9']}), ('Voluma', {'families': ['M2']}), ('Juvéderm Voluma', {'families': ['M2']}), ('Shrink', {'families': ['M9']}),
            ('필러', {'families': ['M2']}), ('리프팅', {'families': ['M9', 'M7']}), ('초음파', {'families': ['M9']}), ('모공', {'concern_root': 'P7'}),
            ('눈물고랑', None), ('밝기', None), ('피지', {'concern_root': 'P6'})]
    for t, e in samp:
        add(t, '샘플', e)
    # 원천 taxonomy 시술 항목 이름 · 제품 이름(계열 = modality id)
    for m in b_tax['modality']:
        for s in m['subcategories']:
            for it in s['items']:
                add(it['name'], 'taxonomy 시술 항목', {'families': [m['id']]})
        for p in m.get('products') or []:
            add(p['name'], 'taxonomy 제품', {'families': [m['id']]})
    # taxonomy 고민 갈래 · 항목
    for p in b_tax['problem']:
        add(p['category'], 'taxonomy 고민 대분류', {'concern_root': p['id']})
        for s in p['subcategories']:
            sc = next((x for x in C7['concerns']['subcategories'] if x['id'] == s['id']), {})
            site_ok = (not sc.get('node')) and '부위' in (sc.get('kind') or '')  # 7단계 결정: 이 갈래는 고민이 아니라 부위
            add(s['label'], 'taxonomy 고민 갈래', {'concern_root': p['id'], 'site_ok': site_ok})
    # 시장가 이름
    for c in b_mp['categories']:
        for it in c['items']:
            add(it['name'], '시장가', {'families': [c['id']]})
    # problem-packages CC
    for p in b_pp['problems']:
        for cpl in p['complaints']:
            add(cpl['cc'], 'problem-packages CC', {'families': sorted({x['category'] for x in cpl['procedures']}), 'concern_root': p['problem_id']})
    # products.json
    for grp, v in b_prod.items():
        if isinstance(v, dict) and 'products' in v:
            for p in v['products']:
                cid = v['category_id']
                add(p['name'], 'products.json', {'families': cid if isinstance(cid, list) else [cid]})
    # patient-education 환자용 이름
    for c in b_pe['categories']:
        add(c['patient_name'], 'patient-education 환자용 이름', {'families': [c['id']]})
    # 원장 이름(5단계 ledger)
    for l in U5['ledger']:
        add(l['name'], '원장 이름', {'families': [l['source_family']]} if l.get('source_family') else None)
    # 중복 제거(같은 말 · 같은 출처)
    seen, out = set(), []
    for w in W_:
        k = (w['text'], w['origin'])
        if k in seen:
            continue
        seen.add(k)
        out.append(w)
    # 규칙 변형(표시) — V1 처짐→쳐짐 · V2 영문 대문자 · V3 괄호 풀기 · V4 끝 「주사」「시술」 떼기
    var = []
    for w in out:
        t = w['text']
        if '처짐' in t:
            var.append({**w, 'text': t.replace('처짐', '쳐짐'), 'variant': 'V1 처짐→쳐짐'})
        if re.match(r'^[A-Za-z]', t) and t.upper() != t:
            var.append({**w, 'text': t.upper(), 'variant': 'V2 영문 대문자'})
        if '(' in t and ')' in t:
            var.append({**w, 'text': re.sub(r'\s*\(([^)]*)\)', r' \1', t).strip(), 'variant': 'V3 괄호 풀기'})
        m = re.match(r'^(.{2,})(주사|시술)$', t)
        if m:
            var.append({**w, 'text': m.group(1), 'variant': 'V4 끝 주사·시술 떼기'})
        if ' ' in t:
            var.append({**w, 'text': t.replace(' ', ''), 'variant': 'V0 띄어쓰기 붙임(정규화 흡수 확인)'})
    seen2 = set((w['text'], w['origin']) for w in out)
    for v in var:
        k = (v['text'], v['origin'] + '|' + v['variant'])
        if k in seen2:
            continue
        seen2.add(k)
        out.append(v)
    return out


def judge_target(t, exp):
    if exp is None:
        return None
    tid = t['id']
    k, _, key = tid.partition(':')
    if exp.get('families') and target_families(tid) & set(exp['families']):
        return True
    if exp.get('families') and fam_hit(set(exp['families']), target_families(tid))[0]:
        return '옮김'
    if exp.get('families') and k == 'technique':
        fams = {d['family'] for d in T4['family_defaults'] if key in [d['default']] + (d.get('also') or []) or (TECH.get(key, {}).get('parent') in [d['default']] + (d.get('also') or []))}
        if fams & set(exp['families']):
            return True
    if exp.get('concern_root') and k == 'concern' and target_concern_root(tid) == exp['concern_root']:
        return True
    if exp.get('site') and k == 'site' and SITE_BY_ID.get(key, {}).get('name') == exp['site']:
        return True
    if exp.get('site') and k == 'unit_procedure' and UNITS.get(key, {}).get('key', {}).get('site') == exp['site']:
        return True
    if exp.get('site_ok') and k == 'site':
        return '옮김'
    if exp.get('concern_root') and k in ('purpose',):
        return None  # 목적 노드 — 판정 보류
    return False


def run_m2():
    rows = []
    for w in word_list():
        res = resolve(w['text'])
        tg = all_targets(res)
        verdicts = [judge_target(t, w['expect']) for t in tg]
        if res['mode'] == '없음':
            st = '못 찾음'
        elif w['expect'] is None:
            st = '찾음(정답 미정)'
        elif not any(v for v in verdicts):
            st = '틀리게 찾음' if all(v is False for v in verdicts) else '판정 보류'
        elif len(tg) > 1:
            st = '후보 여럿(정답 포함)'
        elif verdicts[0] == '옮김':
            st = '찾음(계열 옮김 결정)'
        else:
            st = '찾음'
        rows.append({'text': w['text'], 'origin': w['origin'], 'variant': w['variant'], 'mode': res['mode'], 'status': st,
                     'targets': [t['id'] for t in tg][:8], 'n_targets': len(tg), 'unmatched': res['unmatched'], 'expect': w['expect']})
    return rows


# ═════════════════════════ M3 엣지 표본 ═════════════════════════
def all_text(o):
    out = []
    def walk(x):
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(o)
    return ' '.join(out)


TAX_ITEM = {}
for m in b_tax['modality']:
    for s in m['subcategories']:
        for it in s['items']:
            TAX_ITEM[it['id']] = (m['id'], s, it)
    for p in m.get('products') or []:
        TAX_ITEM[p['id']] = (m['id'], None, p)
TAX_ITEM_AUTO = {}
for p in b_tax['problem']:
    for s in p['subcategories']:
        for it in s['items']:
            TAX_ITEM_AUTO[it['id']] = (p['id'], s, it)


def edge_rows():
    K = collections.OrderedDict()
    K['product_family'] = [{'product': r['ledger_id'], 'family': f, 'role': '주' if f == r['family'] else '보조', 'row': r}
                           for r in F2['product_family'] for f in ([r['family']] if r['family'] else []) + (r.get('also_families') or [])]
    K['key_family'] = [{'unit': u['id'], 'v': u['key']['family']} for u in U5['units'] if u['key']['family']]
    K['key_site'] = [{'unit': u['id'], 'v': u['key']['site']} for u in U5['units'] if u['key']['site'] not in (None, '해당 없음', '병변 단위')]
    K['key_technique'] = [{'unit': u['id'], 'v': u['key']['technique']} for u in U5['units'] if u['key']['technique']]
    K['child_of'] = ([{'kind': 'site', 'a': n['name'], 'b': n['parent']} for n in S3['nodes'] if n['parent']] +
                     [{'kind': 'technique', 'a': n['id'], 'b': n['parent']} for n in T4['nodes'] if n['parent']] +
                     [{'kind': 'concern', 'a': k, 'b': v['parent']} for k, v in CONCERN_NODES.items() if v['parent']])
    K['concern_related'] = [{'a': c['id'], 'b': r, 'row': c} for c in C7['concerns']['extra_items'] for r in c.get('related') or []]
    K['family_technique'] = [{'family': d['family'], 'tech': t} for d in T4['family_defaults'] for t in [d['default']] + (d.get('also') or []) if t]
    K['uses_product'] = [{'unit': u['id'], 'product': p['product'], 'p': p} for u in U5['units'] for p in u.get('uses_product') or []]
    K['contains'] = [{'package': c['package'], 'unit': c['unit'], 'c': c} for c in G6['contains'] if c.get('unit')] + \
                    [{'package': s['package'], 'unit': x, 'c': s} for s in G6['slots'] for x in s.get('candidates') or []]
    K['treats'] = [{'e': e, 'unit': u} for e in C7['edges'] for u in (e['to_units'] or [None]) if e['target_kind'] != '대상 없음']
    K['concern_site'] = [{'concern': k, 'site': s} for k, v in CONCERN_NODES.items() for s in v['sites']]
    K['anchors_combo'] = [{'combo': cb, 'concern': c} for cb in C7['combos'] for c in anchor_concerns(cb)]
    K['combo_component'] = [{'combo': cb, 'comp': comp, 'unit': u, 'field': f_} for cb in C7['combos'] for f_ in ('components', 'members', 'upgrade') for comp in cb.get(f_) or [] for u in comp.get('units') or []]  # 3차: 구성 칸 셋(골드 빈틈 ②)
    K['procedure_relation'] = [{'e': e} for e in R8['edges']]
    K['concern_avoid'] = [{'e': e} for e in R8['avoid_edges']]
    K['requires_check'] = [{'c': c, 'cond': k} for c in R8['conditions']['claims'] for k in c.get('conditions') or []]
    K['has_complication'] = [{'x': x} for x in R8['safety']['complications']]
    K['site_caution'] = [{'x': x} for x in R8['safety']['site_caution']]
    K['has_statement'] = [{'x': x} for x in R8['evidence']['statements']]
    K['cites'] = [{'from': x['id'], 'to': ev, 'x': x} for x in R8['evidence']['statements'] + R8['safety']['complications'] for ev in x.get('evidence') or []]
    K['line_item'] = [{'line': ln, 'item': it} for ln, v in P1['lines'].items() for it in v['items'] if it.get('ledger_id')]
    return K


def unit_source_text(u):
    parts = [u['name']]
    for s in u.get('sources') or []:
        parts += [s.get('name') or '', s.get('detail') or '', s.get('id') or '']
    for m in u.get('market') or []:
        parts.append(m['name'])
    return ' '.join(parts)


def unit_source_fams(u):
    fs = set()
    for s in u.get('sources') or []:
        if s['src'] == 'ledger':
            l = next((x for x in U5['ledger'] if x['id'] == s['id']), None)
            if l and l.get('source_family'):
                fs.add(l['source_family'])
            m = re.match(r'(M\d+)', s['id'])
            if m:
                fs.add(m.group(1))
        elif s['src'] == 'market':
            mk = next((x for x in U5['market'] if x['name'] == s['id']), None)
            if mk:
                fs.add(mk['category'])
        elif s['src'] in ('taxonomy', 'problem'):
            if s['id'] in TAX_ITEM:
                fs.add(TAX_ITEM[s['id']][0])
            elif s['id'] in TAX_ITEM_AUTO:
                fs |= set(TAX_ITEM_AUTO[s['id']][2].get('modality_ref') or [])
    return fs


def _sub_by_name():
    m = collections.defaultdict(set)
    for r in F2['product_family']:
        subs = [(r['family'], r['sub_family'])] if r.get('sub_family') else []
        subs += [(x['family'], x['sub_family']) if isinstance(x, dict) else (r['family'], x) for x in r.get('also_sub_families') or []]
        if not subs:
            continue
        it = PRODUCTS.get(r['ledger_id']) or {}
        names = {r.get('display_name')} | {x['name'] for x in (it.get('2_names') or {}).get('search_names') or []}
        for n in names:
            if n:
                for fs in subs:
                    m[norm(n)].add(fs)
    return m


SUB_BY_NAME = _sub_by_name()


def source_subs(procs, fam, cc=None):
    """원천 CC procedures[] 중 그 계열 행의 제품 이름(+ CC 이름) → 하위 계열 집합(2단계 판정). 제품 이름이 없거나 하위가 없으면 빈 집합."""
    out = set()
    for f, sub in SUB_BY_NAME.get(norm(cc or ''), set()):
        if f == fam:
            out.add(sub)
    for pr in procs or []:
        if pr.get('category') != fam:
            continue
        for n in pr.get('products') or []:
            for f, sub in SUB_BY_NAME.get(norm(n), set()):
                if f == fam:
                    out.add(sub)
    return out


def moved_ok(src_fams, silver_fams, units=(), basis=''):
    """원천 계열 코드 ≠ 실버 계열인데 단계 결정으로 옮긴 것인가(2단계 계열 옮김 · N 계열 신설 · 5단계 단위 시술 결정 · 원천 수정 후보)."""
    silver_fams = set(silver_fams or [])
    if any(str(f).startswith('N') for f in silver_fams):
        return '계열 신설(N · 2단계 결정)'
    if '원천 수정 후보' in (basis or ''):
        return '원천 코드 = 원천 수정 후보(결정)'
    for u in units or []:
        x = UNITS.get(u)
        if x and x['key']['family'] in silver_fams and (set(src_fams) & unit_source_fams(x)):
            return '단위 시술 계열을 원천에서 옮김(5단계 결정)'
    for f in silver_fams:
        for rows in PF_ROWS.values():
            for r in rows:
                if r['family'] == f and r.get('step1_code') in src_fams and r.get('verdict') != '맞음':
                    return '제품 계열 옮김(2단계 결정)'
    return None


def find_source_record(src, sid):
    """step7 treats source · source_id → 원천 레코드 원문."""
    if src.startswith('③'):
        pid, _, cc = sid.partition(':')
        for p in b_pp['problems']:
            if p['problem_id'] == pid:
                for cpl in p['complaints']:
                    if cpl['cc'] == cc:
                        return {'families': {x['category'] for x in cpl['procedures']}, 'procs': cpl['procedures'], 'text': all_text(cpl), 'sites_text': ' '.join([cpl['cc'], cpl.get('cc_group') or '', cpl.get('cc_detail') or ''])}
    if src.startswith('②'):
        for c in b_pc['combos']:
            if c['problem_id'] == sid:
                return {'families': {f for pk in c['packages'] for f in pk['procedures']}, 'text': all_text(c), 'sites_text': ''}
    if src.startswith('⑤') or src.startswith('① taxonomy') or src.startswith('① P1'):
        if sid in TAX_ITEM_AUTO:
            pid, s, it = TAX_ITEM_AUTO[sid]
            return {'families': set(it.get('modality_ref') or []), 'text': all_text(it) + ' ' + s['label'], 'sites_text': ' '.join([it['name'], it.get('detail') or '', s['label']])}
    if src.startswith('④'):
        return {'families': None, 'text': all_text(b_to['by_concern']), 'sites_text': ''}
    return None


def check_edge(kind, r):
    """반환 (판정, 꼴, 근거). 판정 ∈ 맞음 · 틀림 · 결정 근거(원천 직접 근거 없음)."""
    if kind == 'product_family':
        it = PRODUCTS.get(r['product'])
        src = (it or {}).get('family', {}).get('code') if it else None
        row = r['row']
        if r['role'] == '보조':
            return ('결정 근거', '보조 계열(2단계 결정)', row.get('basis'))
        if src == r['family']:
            return ('맞음', '원장 계열 = 판정', f'원장 {src}')
        decided = set(F2.get('research_errata', {})) | {x.get('ledger_id') for k in ('v4_fix', 'v3_delta', 'v2_delta', 'step5_delta', 'step7_delta') for x in F2.get(k, []) if isinstance(x, dict)}
        if r['family'] == '계열 밖' or r['product'] in decided:
            return ('결정 근거', '계열 밖 · 2단계 정정 기록(research_errata · delta)', f"원장 {src} → {r['family']}")
        if row.get('verdict') in ('옮김', '여러') and row.get('basis'):
            return ('결정 근거', '원장과 다른 계열로 옮김(2단계 결정)', f"원장 {src} → {r['family']} · {row['basis'][:80]}")
        return ('틀림', '원장 계열 ≠ 판정 · 근거 없음', f'원장 {src} ↔ {r["family"]}')
    if kind == 'key_family':
        u = UNITS[r['unit']]
        fs = unit_source_fams(u)
        if not fs:
            return ('결정 근거', '원천 계열 코드 없음(결정으로 세운 단위 시술)', u.get('decided_by'))
        if r['v'] in fs:
            return ('맞음', '원천 계열 코드 일치', ','.join(sorted(fs)))
        mv = moved_ok(fs, {r['v']}, [r['unit']], '')
        if mv or u.get('decided_by'):
            return ('결정 근거', mv or '단위 시술 계열 결정(decided_by)', f"원천 {','.join(sorted(fs))} → {r['v']} · {u.get('decided_by') or ''}"[:160])
        return ('틀림', '원천 계열 코드와 다름', f"{','.join(sorted(fs))} ↔ {r['v']}")
    if kind == 'key_site':
        u = UNITS[r['unit']]
        st = unit_source_text(u)
        if '기본값' in (u.get('site_basis') or ''):
            return ('결정 근거', '부위 기본값(원천 부위 없음)', u['site_basis'][:80])
        names = [r['v']] + [s['text'] for s in (SITES.get(r['v']) or {}).get('synonyms') or [] if not s.get('weak')]
        if any(n and n in st for n in names):
            return ('맞음', '원천 이름 · detail 에 부위 있음', r['v'])
        found = sites_in_text(st)
        if found and r['v'] not in found:
            return ('틀림', '원천 문구의 부위와 다름', f"원천 {found} ↔ {r['v']}")
        return ('결정 근거', '원천 문구에 부위 낱말 없음(맥락 · 결정)', (u.get('site_basis') or '')[:80])
    if kind == 'key_technique':
        u = UNITS[r['unit']]
        fam = u['key']['family']
        fd = next((d for d in T4['family_defaults'] if d['family'] == fam), None)
        allowed = set()
        if fd:
            allowed = {fd['default']} | set(fd.get('also') or [])
        tparent = TECH.get(r['v'], {}).get('parent')
        if r['v'] in allowed or tparent in allowed:
            return ('맞음', '계열 기본 · 허용 기법(하위 포함)', f"{fam} {sorted(allowed)}")
        return ('결정 근거', '계열 기본 기법 밖 — 단위 시술에서 덮어씀(4 · 5단계 결정)', f"{fam} {sorted(allowed)} ↔ {r['v']}")
    if kind == 'child_of':
        if r['kind'] == 'concern':
            ra, rb = re.match(r'(P\d+)', r['a']), re.match(r'(P\d+)', r['b'] or '')
            if ra and rb:
                return ('맞음', '원천 problem 갈래 id 일치', r['a']) if ra.group(1) == rb.group(1) else ('틀림', '원천 갈래와 다른 상위', f"{r['a']} → {r['b']}")
            if r['a'] in TAX_ITEM_AUTO:
                pid, s, it = TAX_ITEM_AUTO[r['a']]
                return ('맞음', '원천 갈래 일치', s['id']) if s['id'] == r['b'] else ('틀림', '원천 갈래와 다른 상위', f"{s['id']} ↔ {r['b']}")
            return ('결정 근거', '원천 밖 고민(결정 J)', r['a'])
        if r['kind'] == 'site':
            return ('결정 근거', '부위 트리 = 사용자 확정(10-27) · 원천 트리 없음', f"{r['a']} → {r['b']}")
        return ('결정 근거', '기법 트리 = 4단계 결정', f"{r['a']} → {r['b']}")
    if kind == 'concern_related':
        return ('결정 근거', '원천 밖 고민 관련(J10 결정)', r['row']['basis'][:80])
    if kind == 'family_technique':
        prof = next((p for p in b_pf['profiles'] if p['id'] == r['family']), None)
        med = (TECH.get(r['tech']) or {}).get('medical_name') or ''
        mech = ' '.join(prof.get('mechanism') or []) if prof else ''
        words = re.findall(r'[a-z]+', med.lower())
        if prof and any(w in mech.lower() for w in words if len(w) > 3):
            return ('맞음', 'procedure-profiles mechanism 일치', f"{mech} ~ {med}")
        return ('결정 근거', 'mechanism 낱말 직접 일치 없음(4단계 결정)', f"{mech or '프로필 없음'} ~ {med}")
    if kind == 'uses_product':
        u = UNITS[r['unit']]
        it = PRODUCTS.get(r['product']) or {}
        names = [it.get('2_names', {}).get('display_name'), it.get('2_names', {}).get('ledger_name')] + [s['name'] for s in it.get('2_names', {}).get('search_names') or []]
        st = unit_source_text(u)
        if any(n and n in st for n in names):
            return ('맞음', '단위 시술 원천 이름에 제품 이름', r['product'])
        pf = target_families('product:' + r['product'])
        if u['key']['family'] in pf:
            return ('결정 근거', '이름 직접 근거 없음 · 계열 일치', r['p'].get('basis'))
        return ('틀림', '제품 계열 ≠ 단위 시술 계열', f"{sorted(pf)} ↔ {u['key']['family']}")
    if kind == 'contains':
        p = PACKAGES.get(r['package']) or {}
        u = UNITS.get(r['unit'])
        if not u:
            return ('틀림', '없는 단위 시술', r['unit'])
        src_txt = all_text(p.get('description')) + ' ' + (p.get('detail_raw') or '') + ' ' + p.get('name', '') + ' ' + (r['c'].get('basis') or '')
        site_ok = u['key']['site'] in src_txt or any(s in src_txt for s in sites_in_text(u['name']))
        fam_ok = (p.get('source_family') == u['key']['family']) or (u['key']['family'] and FAM_NAME.get(u['key']['family'], '') in src_txt)
        if site_ok and fam_ok:
            return ('맞음', '원장 detail 부위 · 계열 일치', r['c'].get('basis'))
        ws = sites_in_text(src_txt)
        if ws and site_rel(u['key']['site'], ws) == '다른 영역':
            return ('틀림', '패키지 원문 부위와 다른 영역', f"{ws} ↔ {u['key']['site']} {u['name']}")
        return ('결정 근거', '원장 detail 에 계열 · 부위 직접 열거 없음(6단계 구성 결정)', f"{p.get('source_family')} · {u['name']} · {r['c'].get('basis')}"[:160])
    if kind == 'treats':
        e = r['e']
        rec = find_source_record(e['source'], e['source_id'])
        u = UNITS.get(r['unit']) if r['unit'] else None
        fam = u['key']['family'] if u else e['to_family']
        if rec is None:
            if e['source'].startswith('⑥') or e['source'].startswith('⑦') or e['source'].startswith('⑧'):
                return ('결정 근거', '원장 용도 · 메뉴 · 결정 노드(원천 고민 칸 아님)', e['basis'][:80])
            return ('결정 근거', '원천 레코드 못 찾음(대조 불가)', f"{e['source']} {e['source_id']}")
        if rec['families'] is not None and rec['families'] and fam not in rec['families']:
            mv = moved_ok(rec['families'], {fam}, [r['unit']] if r['unit'] else [], e.get('basis'))
            if mv:
                return ('결정 근거', mv, f"원천 {sorted(rec['families'])} → {fam}")
            return ('틀림', '원천 추천 시술 계열에 없음', f"원천 {sorted(rec['families'])} ↔ {fam}")
        if u and u['key'].get('sub_family'):
            subs = source_subs(rec.get('procs'), fam, e['source_id'].partition(':')[2] if e['source'].startswith('③') else None)
            if subs and u['key']['sub_family'] not in subs:
                return ('틀림', '원천 제품의 하위 계열 밖(같은 계열 다른 하위)', f"원천 제품 하위 {sorted(subs)} ↔ {u['key']['sub_family']} {u['name']}")
            if not subs and e['site_check'] == '상위 부위 얼굴 전체':
                return ('결정 근거', '하위 계열 원천 미지정 — 계열 전부(얼굴 전체 층)로 펼침', f"{u['key']['sub_family']} {u['name']} ← {e['source'][:2]}{e['source_id']}")
        if u:
            want = sites_in_text(rec['sites_text']) or [s for s in e.get('anchor_sites') or [] if s in SITES and '(묶음)' not in s]
            rel = site_rel(u['key']['site'], want)
            segs = [g for g in re.split(r'[/,]', rec['sites_text'].split(' ')[0]) if g]
            if rel in ('다른 영역', '다른 부위(같은 영역)') and any(not sites_in_text(g) for g in segs):
                return ('결정 근거', '원천 낱말 일부가 부위 이름 아님(낱말 → 부위 풀이 결정)', f"원천 「{rec['sites_text'][:40]}」 ↔ {u['key']['site']} {u['name']}")
            if rel == '다른 영역':
                return ('틀림', '원천 부위와 다른 영역(얼굴 ↔ 바디 등)', f"원천 {want} ↔ {u['key']['site']} {u['name']}")
            if rel == '다른 부위(같은 영역)':
                return ('틀림', '원천 부위와 다른 부위', f"원천 {want} ↔ {u['key']['site']} {u['name']}")
            if rel == '얼굴 전체':
                return ('결정 근거', '얼굴 전체 층(R21 · U-1 판단 대상)', f"원천 {want} ↔ 얼굴 전체 {u['name']}")
            if rel == '원천 부위 없음' and region(u['key']['site']) not in (None, '얼굴') and e['from'] not in ('opt',) and not str(e['from']).startswith('목적'):
                cn = CONCERN_NODES.get(e['from'])
                cr = {region(s.replace('(묶음)', '')) or region(s) for s in (cn or {}).get('sites') or []}
                if cr and region(u['key']['site']) not in cr:
                    return ('틀림', '고민 영역과 다른 영역', f"고민 {cn['sites']} ↔ {u['key']['site']} {u['name']}")
        return ('맞음', '원천 계열 · 부위 일치', f"{e['source']} {e['source_id']}")
    if kind == 'concern_site':
        cn = CONCERN_NODES[r['concern']]
        src = None
        for s in C7['concerns']['subcategories']:
            if s['id'] == r['concern']:
                src = s['source_label']
        if r['concern'] in TAX_ITEM_AUTO:
            src = TAX_ITEM_AUTO[r['concern']][2]['name'] + ' ' + (TAX_ITEM_AUTO[r['concern']][2].get('detail') or '') + ' ' + TAX_ITEM_AUTO[r['concern']][1]['label']
        if not src:
            return ('결정 근거', '원천 밖 고민(결정)', r['concern'])
        nm = r['site'].replace('(묶음)', '')
        names = [nm] + [s['text'] for s in (SITES.get(r['site']) or SITES.get(nm) or {}).get('synonyms') or [] if not s.get('weak')]
        if any(n in src for n in names):
            return ('맞음', '원천 갈래 이름에 부위', src)
        ws = sites_in_text(src)
        segs = [g for g in re.split(r'[/,\s]', src) if g]
        if ws and not any(not sites_in_text(g) for g in segs):
            return ('틀림', '원천 갈래 이름의 부위와 다름', f"{src} ({ws}) ↔ {r['site']}")
        return ('결정 근거', '원천 낱말 → 부위 풀이(7단계 결정 · 해부 동의어)', f"{src} ↔ {r['site']}")
    if kind == 'anchors_combo':
        cb = r['combo']
        sid = cb.get('source_id') or ''
        root = target_concern_root('concern:' + r['concern'])
        if cb['source'] == 'problem-combos':
            if sid.startswith(root or '?'):
                return ('맞음', '원천 problem id 일치', sid)
            anc = cb.get('anchor') or {}
            if anc.get('note') or anc.get('basis') or anc.get('source_label'):
                return ('결정 근거', '원천 problem 과 다른 고민에 앵커(7단계 앵커 결정)', f"{sid} → {r['concern']} · {(anc.get('note') or anc.get('basis') or anc.get('source_label'))}"[:160])
            return ('틀림', '원천 problem 과 다른 고민', f"{sid} ↔ {r['concern']}")
        lab = (cb.get('anchor') or {}).get('source_label') or ''
        cn = CONCERN_NODES.get(r['concern'], {}).get('name') or ''
        if cn and (cn in lab or any(w in lab for w in re.split(r'[/· ]', cn) if len(w) > 1)):
            return ('맞음', '원천 라벨에 고민 이름', lab)
        return ('결정 근거', '원천 라벨 ↔ 고민 이름 직접 일치 없음(7단계 대응)', f"{lab} ↔ {cn}")
    if kind == 'combo_component':
        cb, comp, uid = r['combo'], r['comp'], r['unit']
        u = UNITS[uid]
        if comp.get('family') and u['key']['family'] != comp['family']:
            return ('틀림', '구성 계열 ≠ 단위 시술 계열', f"{comp['family']} ↔ {u['key']['family']}")
        anc = cb.get('anchor') or {}
        acs = anchor_concerns(cb)
        want = []
        for c in acs:
            want += [s for s in (CONCERN_NODES.get(c) or {}).get('sites') or [] if '(묶음)' not in s]
        want += sites_in_text(anc.get('source_label') or '')
        rel = site_rel(u['key']['site'], want)
        if rel in ('다른 영역', '다른 부위(같은 영역)'):
            return ('틀림', f'조합 고민 부위와 {rel}', f"{want} ↔ {u['key']['site']} {u['name']}")
        return ('맞음', '구성 계열 · 부위 일치', f"{cb['id']} {comp.get('family')}")
    if kind == 'procedure_relation':
        e = r['e']
        bad = []
        for cid in e['claims']:
            c = CLAIMS[cid]
            if c['source'] == 'contraindications.rules':
                rr = b_ci['rules'][c['source_index']]
                fa, fb = set(c['a'].get('families') or []), set(c['b'].get('families') or [])
                miss = {rr['from'], rr['to']} - (fa | fb)
                if miss and not moved_ok(miss, (fa | fb) - {rr['from'], rr['to']} or (fa | fb), list(c['a'].get('units') or []) + list(c['b'].get('units') or []), (c['a'].get('basis') or '') + (c['b'].get('basis') or '')):
                    bad.append(f"{cid} 원천 {rr['from']}↔{rr['to']} ↔ 실버 {sorted(fa)}↔{sorted(fb)}")
            elif c['source'] == 'synergy.links':
                rr = b_syn['links'][c['source_index']]
                fa, fb = set(c['a'].get('families') or []), set(c['b'].get('families') or [])
                miss = {rr['from_category'], rr['to_category']} - (fa | fb)
                if miss and not moved_ok(miss, (fa | fb) - {rr['from_category'], rr['to_category']} or (fa | fb), list(c['a'].get('units') or []) + list(c['b'].get('units') or []), (c['a'].get('basis') or '') + (c['b'].get('basis') or '')):
                    bad.append(f"{cid} 원천 {rr['from_category']}↔{rr['to_category']} ↔ 실버 {sorted(fa)}↔{sorted(fb)}")
            elif c['source'] != 'problem-packages.complaints[].combos':  # CC 조합은 끝점 = procedures[] 이름(주장 원문과 다른 칸)
                for side in ('a', 'b'):
                    t = (c[side] or {}).get('text') or ''
                    if t and tnorm(t)[:6] not in tnorm(c['text']):
                        bad.append(f"{cid} 끝점 원문 「{t}」 이 주장 원문에 없음")
            # 부위 대조: 원문에 부위 낱말이 있고 끝점 단위 시술 부위가 다르면
            for side in ('a', 'b'):
                t = (c[side] or {}).get('text') or ''
                ws = sites_in_text(t)
                for uid in (c[side] or {}).get('units') or []:
                    if ws and site_rel(UNITS[uid]['key']['site'], ws) in ('다른 영역', '다른 부위(같은 영역)'):
                        bad.append(f"{cid} 끝점 「{t}」 부위 {ws} ↔ {UNITS[uid]['name']}")
        if bad:
            return ('틀림', '원천 계열 · 끝점 · 부위 불일치', ' | '.join(bad[:3]))
        return ('맞음', '원천 from · to · 끝점 일치', ','.join(e['claims'][:3]))
    if kind == 'concern_avoid':
        e = r['e']
        cn = [CONCERN_NODES.get(c, {}).get('name', c) for c in e['from_concerns']]
        ok_c = any(w in e['text'] + ' ' + (e.get('concern_basis') or '') for n in cn for w in re.split(r'[/· ]', n or '') if len(w) > 1)
        ok_t = (e['to'].get('text') or '') in e['text']
        if ok_c and ok_t:
            return ('맞음', '원문에 고민 · 대상 낱말', e['text'][:60])
        return ('틀림', '원문에 고민 또는 대상 낱말 없음', f"{cn} · {e['to'].get('text')} ↔ {e['text'][:60]}")
    if kind == 'requires_check':
        c = r['c']
        node = COND_NODES.get(r['cond'])
        if not node:
            return ('틀림', '없는 확인 조건 노드', r['cond'])
        if any(re.search(node['match_pattern'], str(c.get(k) or '')) for k in ('text', 'detail', 'where', 'age')):
            # 대상 계열 ↔ 원천 계열 코드
            m = re.match(r'(M\d+)', str(c.get('source_index') or ''))
            tf = cond_target(c)[0]
            if m and tf and m.group(1) not in tf:
                return ('틀림', '원천 계열과 다른 대상', f"원천 {m.group(1)} ↔ {sorted(tf)}")
            return ('맞음', '원문이 조건 패턴과 일치', node['name'])
        return ('틀림', '원문에 조건 낱말 없음(패턴 불일치)', f"{node['name']} /{node['match_pattern']}/ ↔ {c['text'][:60]}")
    if kind == 'has_complication':
        x = r['x']
        if re.search(r'거의 없음|매우 안전|연구가 아직|충분하지 않', x['name']):
            return ('틀림', '합병증 아님(안심 · 근거 한계 문장이 합병증 노드로)', f"{x['id']} 「{x['name'][:50]}」 ← {x.get('source')}")
        if 'taxonomy' in str(x.get('source')):
            m = next((m for m in b_tax['modality'] if m['id'] == x['family']), None)
            ser = ((m or {}).get('extracted') or {}).get('safety', {}).get('serious') or []
            return ('맞음', '원천 taxonomy serious 칸에 같은 문장', x['family']) if x['name'] in ser else ('틀림', '원천 taxonomy serious 칸에 없음', x['id'])
        cat = next((c for c in b_cx['categories'] if c['id'] == x['family']), None)
        if cat and any(cc['name'] == x['name'] for cc in cat['complications']):
            return ('맞음', '원천 계열 칸에 같은 이름', x['family'])
        other = [c['id'] for c in b_cx['categories'] if any(cc['name'] == x['name'] for cc in c['complications'])]
        return ('틀림', '원천 계열 칸에 없음', f"{x['family']} ↔ 원천 {other}")
    if kind == 'site_caution':
        x = r['x']
        z = next((z for z in b_az['zones'] if z['id'] == x['zone']), None)
        if not z:
            return ('틀림', '없는 위험지대', x['zone'])
        key = {'M1': 'botox_specific', 'M2': 'filler_specific'}.get(x['family'])
        site_ok = x['site'] in z['name_ko'] or x.get('site_mapping') == '같음'
        if key and z.get(key) and site_ok:
            return ('맞음', f'원천 {key} 칸 · 부위 일치', z['name_ko'])
        if site_ok:
            return ('결정 근거', '원천 계열 칸(botox/filler_specific) 밖 계열', f"{z['name_ko']} ↔ {x['family']}")
        return ('결정 근거', f"부위 대응 {x.get('site_mapping')}", f"{z['name_ko']} ↔ {x['site']}")
    if kind == 'has_statement':
        x = r['x']
        cat = b_lit['categories'].get(x['family']) or {}
        if any(isinstance(s, dict) and s.get('statement') == x['statement'] for s in cat.get(x['field']) or []):
            return ('맞음', '문헌 같은 계열 · 칸', x['family'])
        other = [k for k, v in b_lit['categories'].items() for f in ('moa', 'adverse_effects', 'effects') for s in v.get(f) or [] if isinstance(s, dict) and s.get('statement') == x['statement']]
        return ('틀림', '문헌 계열 · 칸 다름', f"{x['family']}.{x['field']} ↔ 원천 {other}")
    if kind == 'cites':
        ids = {e['id'] for e in R8['evidence']['literature'] + R8['evidence']['web'] + R8['evidence']['guides']}
        return ('맞음', '출처 노드 있음', r['to']) if r['to'] in ids else ('틀림', '없는 출처 id', r['to'])
    if kind == 'line_item':
        ln = P1['lines'][r['line']]
        it = PRODUCTS.get(r['item']['ledger_id'])
        if not it:
            return ('틀림', '없는 제품 행', r['item']['ledger_id'])
        fa, fb = target_families('product:' + ln['line_row']), target_families('product:' + r['item']['ledger_id'])
        lic = {re.sub(r'\s', '', l.get('license_no') or '') for l in (it.get('4_license') or {}).get('licenses') or []}
        if r['item'].get('license_no') and re.sub(r'\s', '', r['item']['license_no']) not in lic:
            return ('틀림', '품목 허가 번호가 제품 행 허가에 없음', f"{r['item']['license_no']} ↔ {sorted(lic)}")
        if fa and fb and not (fa & fb):
            return ('틀림', '라인 ↔ 품목 계열 다름', f"{sorted(fa)} ↔ {sorted(fb)}")
        return ('맞음' if r['item'].get('license_no') else '결정 근거', '허가 번호 · 계열 일치' if r['item'].get('license_no') else '허가 번호 없음 · 계열 일치(결정 ' + str(ln.get('decision')) + ')', r['item']['name'])
    return ('결정 근거', '검사기 없음', kind)


def run_m3():
    K = edge_rows()
    out = collections.OrderedDict()
    sem_counts = {e['kind']: e['count'] for e in SEM['edge_kinds']}
    for kind in [e['kind'] for e in SEM['edge_kinds']]:
        rows = K.get(kind, [])
        rnd = random.Random(f'{SEED}:{kind}')
        idx = list(range(len(rows)))
        pick = sorted(rnd.sample(idx, min(PER_KIND, len(idx)))) if rows else []
        checked = []
        for i in pick:
            v, form, ev = check_edge(kind, rows[i])
            checked.append({'i': i, 'verdict': v, 'form': form, 'evidence': str(ev)[:240], 'row': brief_row(kind, rows[i])})
        # 전수(treats · combo_component · procedure_relation · concern_avoid 는 전부도 같이 셈 — 오연결 잡기)
        full = None
        if kind in ('treats', 'combo_component', 'procedure_relation', 'concern_avoid', 'requires_check', 'has_complication', 'has_statement', 'cites', 'key_family', 'key_site', 'product_family'):
            cnt = collections.Counter()
            forms = collections.Counter()
            wrong = []
            for i, rr in enumerate(rows):
                v, form, ev = check_edge(kind, rr)
                cnt[v] += 1
                if v == '틀림':
                    forms[form] += 1
                    wrong.append({'i': i, 'form': form, 'evidence': str(ev)[:240], 'row': brief_row(kind, rr)})
            full = {'n': len(rows), 'verdicts': dict(cnt), 'wrong_forms': dict(forms), 'wrong': wrong}
        c = collections.Counter(x['verdict'] for x in checked)
        out[kind] = {'rows': len(rows), 'semantic_count': sem_counts.get(kind), 'sample': len(pick), 'verdicts': dict(c),
                     'error_rate': round(c['틀림'] / len(pick), 3) if pick else None,
                     'forms': dict(collections.Counter(x['form'] for x in checked if x['verdict'] == '틀림')),
                     'checked': checked, 'full': full}
    return out


def brief_row(kind, r):
    if kind == 'treats':
        e = r['e']
        u = UNITS.get(r['unit']) if r['unit'] else None
        return f"{e['from']} → {r['unit'] or e['to_family']}{(' ' + u['name']) if u else ''} [{e['source'][:2]}{e['source_id']}]"
    if kind == 'combo_component':
        return f"{r['combo']['id']} → {r['unit']} {UNITS[r['unit']]['name']}"
    if kind == 'procedure_relation':
        return f"{r['e']['id']} {r['e']['a']} ↔ {r['e']['b']} {r['e']['kinds']}"
    if kind == 'concern_avoid':
        return f"{r['e']['id']} {r['e']['from_concerns']} → {r['e']['to'].get('text')}"
    if kind == 'requires_check':
        return f"{r['c']['id']} {r['c'].get('target') if isinstance(r['c'].get('target'), str) else (r['c'].get('target') or {}).get('families')} → {r['cond']}"
    if kind in ('has_complication', 'site_caution', 'has_statement'):
        return r['x']['id']
    if kind == 'anchors_combo':
        return f"{r['concern']} → {r['combo']['id']}"
    if kind == 'product_family':
        return f"{r['product']} → {r['family']} ({r['role']})"
    return ' · '.join(f'{k}={v}' for k, v in r.items() if isinstance(v, (str, int)) and k not in ('row',))[:160]


# ═════════════════════════ M4 안전 누락 ═════════════════════════
def silver_corpus():
    texts = []
    for d in (U5, G6, C7, R8):
        def walk(x):
            if isinstance(x, str):
                texts.append(x)
            elif isinstance(x, dict):
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(d)
    blob = '\n'.join(tnorm(t) for t in texts if len(t) >= 4)
    short = {tnorm(t) for t in texts if len(t) < 4}  # 2차: 4자 미만 실버 문자열은 blob 에서 빠져 있어 「완전 같음」으로만 대조(1차는 실버에 있어도 없음으로 셈 — 예 「간독성」)
    return blob, short


def run_m4():
    blob, short = silver_corpus()
    items = []

    def add(group, path, text, family=None, structured=None):
        if not text or not isinstance(text, str):
            return
        n = tnorm(text)
        present = n in blob or n in short
        items.append({'group': group, 'path': path, 'family': family, 'text': text, 'in_silver_text': present, 'structured': structured})

    # 1. 금기 · 확인 조건
    cond_src = collections.defaultdict(set)
    for c in R8['conditions']['claims'] + R8['conditions']['not_condition']:
        cond_src[c['source']].add(tnorm(c['text']))
    for cat in b_cc['categories']:
        for i, t in enumerate(cat['contraindications']):
            add('금기(consent contraindications)', f"consent-checklist[{cat['id']}].contraindications[{i}]", t, cat['id'],
                structured=tnorm(t) in cond_src['consent-checklist.contraindications'])
        for i, t in enumerate(cat['emergency_signs']):
            add('응급 징후(consent emergency_signs)', f"consent-checklist[{cat['id']}].emergency_signs[{i}]", t, cat['id'])
        for i, t in enumerate(cat['mandatory_disclosures']):
            add('필수 고지(consent mandatory_disclosures)', f"consent-checklist[{cat['id']}].mandatory_disclosures[{i}]", t, cat['id'])
    for i, ch in enumerate(b_pre['universal_checks']):
        add('확인 조건(pre universal)', f'pre-procedure-checklist.universal_checks[{i}]', ch['description'] if False else ch['label'], None,
            structured=any(tnorm(ch['label']) in s for s in cond_src['pre-procedure-checklist.universal_checks'] | cond_src.get('pre-procedure-checklist.universal_checks', set())))
    for cat in b_pre['category_specific']:
        for j, ch in enumerate(cat['checks']):
            add(f"확인 조건(pre {ch['type']})", f"pre-procedure-checklist[{cat['id']}].checks[{j}]", ch['label'], cat['id'],
                structured=tnorm(ch['label']) in cond_src['pre-procedure-checklist.category_specific'])
    # 2. 시술 ↔ 시술 금기 · 간격
    claim_idx = collections.defaultdict(set)
    for c in R8['claims']:
        claim_idx[c['source']].add(str(c['source_index']))
    for c in R8['conditions']['claims']:
        claim_idx[c['source']].add(str(c['source_index']).split('.')[0])
    for i, r in enumerate(b_ci['rules']):
        add('시술↔시술 금기 · 간격(contraindications.rules)', f'contraindications.rules[{i}]', f"{r['from_name']}↔{r['to_name']} {r['level']} {r['interval']} {r['note']}", r['from'],
            structured=str(i) in claim_idx['contraindications.rules'])
        items[-1]['in_silver_text'] = tnorm(r['note']) in blob
    for i, x in enumerate(b_ts['incompatible_same_day']):
        add('같은 날 불가(treatment-sequence)', f'treatment-sequence.incompatible_same_day[{i}]', x['reason'], None,
            structured=str(i) in claim_idx['treatment-sequence.incompatible_same_day'])
    for i, x in enumerate(b_ts['minimum_intervals']):
        add('최소 간격(treatment-sequence)', f'treatment-sequence.minimum_intervals[{i}]', x['reason'], None,
            structured=str(i) in claim_idx['treatment-sequence.minimum_intervals'])
    for i, x in enumerate(b_ts['principles']):
        add('순서 원칙(treatment-sequence.principles)', f'treatment-sequence.principles[{i}]', x, None,
            structured=str(i) in claim_idx['treatment-sequence.principles'])
    for i, x in enumerate(b_to['combination_rules']):
        add('조합 규칙(treatment-optimization.combination_rules)', f'treatment-optimization.combination_rules[{i}]', x['detail'], None,
            structured=str(i) in claim_idx['treatment-optimization.combination_rules'] or any(a['source_index'] == i for a in R8['avoid_edges'] if a['source'] == 'treatment-optimization.combination_rules'))
        items[-1]['text'] = f"{x['rule']} — {x['detail']}"
        items[-1]['in_silver_text'] = tnorm(x['detail']) in blob
    for gi, g in enumerate(b_to['by_age_group']):
        for j, t in enumerate(g.get('avoid') or []):
            add('연령대 피함(by_age_group.avoid)', f'treatment-optimization.by_age_group[{gi}].avoid[{j}]', t, None)
    for ci_, c in enumerate(b_to['by_concern']):
        for si, sv in enumerate(c['severity_levels']):
            for j, t in enumerate(sv.get('contraindicated_combos') or []):
                add('고민별 금기 조합(by_concern.contraindicated_combos)', f'treatment-optimization.by_concern[{ci_}].severity_levels[{si}].contraindicated_combos[{j}]', t, None)
    # 3. 합병증 · 부작용
    cx_names = {(x['family'], x['name']) for x in R8['safety']['complications']} | {(x['family'], x['name']) for x in R8['safety']['side_effects']}
    for cat in b_cx['categories']:
        for j, x in enumerate(cat['complications']):
            add(f"합병증 · 부작용(complications {x['severity']})", f"complications[{cat['id']}][{j}]", x['name'], cat['id'], structured=(cat['id'], x['name']) in cx_names)
    # 4. 경과 · PIH · 위험지대
    for t in b_tl['timelines']:
        for p in t['phases']:
            for lvl in ('emergency', 'caution'):
                for j, s in enumerate(p.get(lvl) or []):
                    add(f'타임라인 {lvl}', f"post-procedure-timeline[{t['id']}].{p['period']}.{lvl}[{j}]", s, t['category'])
    for i, p in enumerate(b_pih['procedures']):
        add('PIH(pih-risk)', f'pih-risk.procedures[{i}]', p['prevention'], p['category'], structured=any(x['index'] == i for x in R8['safety']['pih']))
    for z in b_az['zones']:
        for k in ('botox_specific', 'filler_specific'):
            v = z.get(k) or {}
            for kk in ('key_warning', 'primary_risk'):
                if v.get(kk):
                    add(f'위험지대({k}.{kk})', f"anatomy-danger-zones[{z['id']}].{k}.{kk}", v[kk], 'M1' if k.startswith('botox') else 'M2',
                        structured=any(sc['zone'] == z['id'] and sc['family'] == ('M1' if k.startswith('botox') else 'M2') for sc in R8['safety']['site_caution']))
    # 5. 시술 설명 속 안전(extracted · taxonomy)
    for fam, v in b_ext.items():
        for lvl in ('serious', 'uncommon', 'common'):
            for j, s in enumerate((v.get('safety') or {}).get(lvl) or []):
                add(f'extracted.json safety.{lvl}', f'extracted[{fam}].safety.{lvl}[{j}]', s, fam)
        for j, s in enumerate(v.get('aftercare') or []):
            add('extracted.json aftercare', f'extracted[{fam}].aftercare[{j}]', s, fam)
    for m in b_tax['modality']:
        for s in m['subcategories']:
            for it in s['items']:
                ex = it.get('extracted') or {}
                for j, t in enumerate((ex.get('safety') or {}).get('serious') or []):
                    add('taxonomy 항목 safety.serious', f"taxonomy[{it['id']}].safety.serious[{j}]", t, m['id'])
                for j, t in enumerate((ex.get('safety') or {}).get('contraindications') or []):
                    add('taxonomy 항목 safety.contraindications', f"taxonomy[{it['id']}].safety.contraindications[{j}]", t if isinstance(t, str) else json.dumps(t, ensure_ascii=False), m['id'])
    for p in b_pf['profiles']:
        for j, t in enumerate(p.get('aftercare') or []):
            add('procedure-profiles aftercare', f"procedure-profiles[{p['id']}].aftercare[{j}]", t, p['id'])
        for j, t in enumerate(p.get('practicalNotes') or []):
            add('procedure-profiles practicalNotes', f"procedure-profiles[{p['id']}].practicalNotes[{j}]", t, p['id'])

    # 2차(품질 I): 8단계 원천 행 착지표(row_landing) — 쌍 없는 원칙 · 계열 원문 · 순위로 「원문만」 싣는 행은 규칙으로 안 싣는 이유가 명시된 것(구조 누락 아님)
    LAND = {(x['source'], str(x['index'])): x['how'] for x in R8.get('row_landing') or []}
    for it in items:
        m_ = re.match(r'^(.*)\[(\d+)\]$', it['path'])
        if it['structured'] is False and m_ and LAND.get((m_.group(1), m_.group(2)), '').startswith('원문만'):
            it['structured'] = '규칙(원문만)'
    by_group = collections.OrderedDict()
    for it in items:
        g = by_group.setdefault(it['group'], {'n': 0, 'missing_text': 0, 'structured_n': 0, 'structured_missing': 0})
        g['n'] += 1
        if not it['in_silver_text']:
            g['missing_text'] += 1
        if it['structured'] is not None:
            g['structured_n'] += 1
            if not it['structured']:
                g['structured_missing'] += 1
    missing = [it for it in items if not it['in_silver_text'] or it['structured'] is False]

    # 단위 시술 안전 0
    zero, per = [], {}
    for uid, u in UNITS.items():
        s = unit_safety(uid)
        cnt = {k: len(v) for k, v in s.items()}
        per[uid] = cnt
        if not any(cnt[k] for k in ('complications', 'side_effects', 'checks', 'site_caution', 'timelines', 'pih', 'forbid_relations')):
            zero.append({'unit': uid, 'name': u['name'], 'family': u['key']['family'], 'family_text': cnt['family_text']})
    no_cx = [uid for uid, c in per.items() if not c['complications'] and not c['side_effects']]
    no_check = [uid for uid, c in per.items() if not c['checks']]
    return {'items': items, 'by_group': by_group, 'missing': missing, 'units_zero_safety': zero,
            'units_no_side_or_complication': len(no_cx), 'units_no_checks': len(no_check), 'units_total': len(UNITS),
            'global_checks': sum(1 for c in R8['conditions']['claims'] if c.get('target_level') in ('공통', '모든 시술'))}


# ═════════════════════════ 원인 묶음 ═════════════════════════
def causes(m1, m2, m3, m4, raw_diff=None):
    C = []

    def add(cid, title, rule, stage, count, examples):
        C.append({'id': cid, 'title': title, 'fix_rule': rule, 'stage': stage, 'count': count, 'examples': examples[:6]})

    # A 얼굴 전체 층 · 다른 부위
    tr = m3['treats']['full']
    wrong_site = [w for w in tr['wrong'] if w['form'].startswith('원천 부위') or '영역' in w['form']]
    add('A', 'treats 부위 판정 — 원천 부위와 다른 부위 · 다른 영역 단위 시술이 붙음',
        '원천 문구(cc · cc_group · cc_detail · 항목 이름)에 부위 낱말이 있으면 그 부위 · 하위 · 상위 묶음 단위 시술만. 같은 영역 다른 부위 · 다른 영역은 붙이지 않고 계열만',
        '7단계 R21 · R25(site_check) — 「앵커 부위 없음」 갈래', len(wrong_site), [w['row'] + ' — ' + w['evidence'] for w in wrong_site])
    face = sum(1 for x in m3['treats']['checked'] if '얼굴 전체' in x['form'])
    face_full = sum(1 for e in C7['edges'] if e['site_check'] == '상위 부위 얼굴 전체')
    add('B', '얼굴 전체 층(U-1) — 부위 고민에 「얼굴 전체 ○○」가 같이 나옴',
        'U-1 결정 하나: 부위가 있는 질의에 얼굴 전체 단위 시술을 낼지(낸다면 「상위 층」 표시) — 샘플 턱선 처짐 → 소프웨이브는 이 층에서만 나옴',
        '골드 U-1 · 7단계 R21', face_full, [f"표본 얼굴 전체 판정 {face}"])
    tf = [w for w in tr['wrong'] if w['form'] == '원천 추천 시술 계열에 없음']
    add('C', 'treats 계열 — 원천 추천 시술 계열에 없는 계열의 단위 시술', '원천 procedures[].category · modality_ref 밖 계열은 엣지 만들지 않음', '7단계 ③ · ⑤ 갈래',
        len(tf), [w['row'] + ' — ' + w['evidence'] for w in tf])
    cc = m3['combo_component']['full']
    add('D', '추천 조합 구성 — 조합 고민 부위와 다른 부위 단위 시술', '조합 앵커 고민의 부위(sites)로 구성 단위 시술을 거름(R22 를 부위까지)', '7단계 R22 · combos',
        len(cc['wrong']), [w['row'] + ' — ' + w['evidence'] for w in cc['wrong']])
    pr = m3['procedure_relation']['full']
    add('E', '시술 ↔ 시술 끝점 — 원문 끝점 낱말 · 부위와 실버 끝점 불일치', '끝점 원문에 부위 낱말이 있으면 그 부위 단위 시술만 · 원문 낱말이 주장 원문에 없으면 풀이 재확인',
        '8단계 resolver(끝점 풀이 · site_climb)', len(pr['wrong']), [w['row'] + ' — ' + w['evidence'] for w in pr['wrong']])
    # 사전
    nf = [r for r in m2 if r['status'] == '못 찾음' and not r['variant']]
    add('F', '사전 — 원천 · 샘플 말이 사전에 없음(완전 · 낱말 · 접두 모두 실패)', '원천 이름 칸(시장가 · CC · 환자용 이름 · products.json · 샘플 영문)을 사전 출처에 넣고, 괄호 · 「/」 나눔을 낱말 나눔 규칙에',
        '시맨틱 사전(dictionary sources) · 1 · 5단계 검색 이름', len(nf), [f"{r['text']}({r['origin']})" for r in nf])
    wf = [r for r in m2 if r['status'] == '틀리게 찾음' and not r['variant']]
    add('G', '사전 — 다른 계열 · 고민으로 찾음', '틀리게 찾은 말마다 사전 행의 대상을 원천 자리(계열 코드 · 고민 갈래)와 대조 — 접두 일치는 대상 계열이 하나일 때만', '시맨틱 사전 · resolve 접두 규칙',
        len(wf), [f"{r['text']}({r['origin']}) → {r['targets'][:3]}" for r in wf])
    sub_wrong = [w for w in tr['wrong'] if '하위' in w['form']]
    sub_dec = sum(1 for i, rr in enumerate(edge_rows()['treats']) if check_edge('treats', rr)[1].startswith('하위 계열 원천 미지정'))
    fl = [x for r in m1 for x in r.get('face_layer_wrong_sub') or []]
    add('N', '하위 계열 섞임 — 「리프팅기기(울쎄라 · 올리지오)」 추천이 같은 계열 다른 하위(마이크로웨이브 · SUPERB 등)까지 펼쳐짐(사용자 지적 「이중턱 → 마이크로웨이브」의 원인)',
        '원천 CC 행의 제품 이름 → 2단계 하위 계열로 단위 시술 하위를 거름. 원천이 하위를 안 정하면 계열만(얼굴 전체 층에서 하위 전부로 펼치지 않음)',
        '7단계 ③ lowering(얼굴 전체 층 R21) · 5단계 하위 키(J1 안 C)', len(sub_wrong) + sub_dec,
        [w['row'] + ' — ' + w['evidence'] for w in sub_wrong] + [f'하위 원천 미지정인데 얼굴 전체 층으로 펼친 treats {sub_dec}'] + [f'I-01 얼굴 전체 층 하위 밖 {len(fl)}: ' + ' · '.join(fl[:4])])
    add('M', '정규화 문서 ≠ 코드', 'semantic.json dictionary.summary.normalize(「영문으로 시작하면 소문자 · 악센트 제거」) ↔ semantic-build.py norm()(NFKC · 전부 소문자 · 악센트 안 접음) — 골드 resolve 가 문서대로 짜면 「니들RF」 같은 한글+영문 말이 전부 못 찾음', '시맨틱 normalize(문서 · 코드 한 줄로 맞춤)',
        1, ['니들RF → 사전 norm 「니들rf」 · 문서 규칙이면 「니들RF」', 'Juvéderm → 사전은 악센트 그대로'])
    vf = [r for r in m2 if r['variant'] and r['status'] in ('못 찾음', '틀리게 찾음') and not r['variant'].startswith('V0')]
    add('H', '사전 — 규칙 변형(쳐짐 · 대문자 · 괄호 · 끝말) 못 찾음', '정규화에 V1 「쳐짐→처짐」 접기(10-27 은 원천 수정 결정 — 입력 쪽은 열려 있음) · V3 괄호 → 낱말 나눔 · V4 끝 「주사 · 시술」 꼬리 규칙', '시맨틱 normalize · interpret_rules tails',
        len(vf), [f"{r['text']} [{r['variant']}]" for r in vf])
    # 안전
    sm = [x for x in m4['missing'] if x['structured'] is False]
    add('I', '안전 — 원천 구조 칸이 실버 주장 · 노드로 안 올라옴', '원천 안전 칸 행 → 주장 · 조건 · 합병증 행 1:1 셈 assert(빠진 index 목록을 단계 산출에 남김)', '8단계 claims · conditions · safety',
        len(sm), [f"{x['path']} {x['text'][:50]}" for x in sm])
    tm = [x for x in m4['missing'] if not x['in_silver_text'] and x['structured'] is None]
    add('J', '안전 — 원문이 실버에 없음(extracted · taxonomy 안전 칸 · 타임라인 등)', '골드 G9 처럼 브론즈 원문을 싣는 칸을 실버 attach 표에 명시(값 없이 키만 있는 칸)', '5단계 extracted attach · 8단계 family_text',
        len(tm), [f"{x['path']} {x['text'][:50]}" for x in tm])
    z = m4['units_zero_safety']
    add('K', '안전 정보 0 단위 시술', '계열이 안전 원천 밖(M10 · M12 · M13 · M17 · N 계열 등)이면 「정보 없음(gap)」 상태를 단위 시술에 명시', '8단계 gap · 골드 G10',
        len(z), [f"{x['unit']} {x['name']}({x['family']})" for x in z])
    # M1 의도별
    rq = [r for r in m1 if r['status'] == '틀림' and r['intent'] in ('I-07', 'I-08')]
    add('L', '같이 · 간격 질문 — 시술 말을 못 풀거나 주장이 원천 값과 다름', '원천 쌍 이름(「CO2 프락셔널」「HA 필러」「RF/HIFU」)을 사전 · 낱말 나눔으로 · same_day 충돌은 G14 쌍 요약으로', '시맨틱 사전 · 8단계 끝점',
        len(rq), [f"{r['id']} {r['text']} — {'; '.join(r['why'])[:120]}" for r in rq])
    lost = [d for d in (raw_diff or []) if d['raw'] == '맞음' and d['resolved'] == '틀림']
    add('O', '충돌 해소 판에서 같은 날 값이 사라짐 — 순서에 따라 갈리는 원천(「HA 필러 → RF/HIFU 같은 날 불가 · 역순은 같은 날 가능」)이 해소 뒤 same_day 「정보 없음」',
        '방향(first)별 same_day 를 따로 남김(by_direction) — 한 값으로 접을 수 없으면 options[] 로(G15 와 같은 꼴)', '8단계 충돌 해소(conflict_resolution · edges[].resolved)',
        len(lost), [f"{d['id']} raw {d['raw_why'][:1]} → resolved {d['resolved_why'][:1]}" for d in lost])
    return [c for c in C if c['count']]


# ═════════════════════════ 실행 · 리포트 ═════════════════════════
def pct(a, b):
    return round(100.0 * a / b, 1) if b else None


def main():
    global USE_RES
    Q = build_eval_set()
    USE_RES = False
    m1_raw = run_m1(Q)
    USE_RES = bool(EDGE_RES)
    m1 = run_m1(Q, 'cc')
    m1_nocc = run_m1(Q, 'nocc')
    m1_v1 = run_m1(Q, 'v1')

    def board_stats(rows):
        out = {}
        for it in ('I-07', 'I-08'):
            rr = [r for r in rows if r['intent'] == it and r['recall'] is not None]
            out[it] = {'n': len(rr), 'right': sum(r['status'] == '맞음' for r in rr), 'recall': round(sum(r['recall'] for r in rr) / len(rr), 3) if rr else None,
                       'safety_missing': sum(len(r['safety_missing']) for r in rr)}
        return out
    boards = {'raw(충돌 그대로 · claims[].interval)': board_stats(m1_raw)}
    if EDGE_RES:
        boards['resolved(edges[].resolved)'] = board_stats(m1)
    m2 = run_m2()
    m3 = run_m3()
    m4 = run_m4()
    raw_diff = [{'id': a['id'], 'raw': a['status'], 'resolved': b['status'], 'raw_why': a['why'][:2], 'resolved_why': b['why'][:2]} for a, b in zip(m1_raw, m1) if a['status'] != b['status'] or a['why'] != b['why']]
    cz = causes(m1, m2, m3, m4, raw_diff if EDGE_RES else [])

    scored = [r for r in m1 if r['recall'] is not None]
    rec = round(sum(r['recall'] for r in scored) / len(scored), 3) if scored else None
    pr_ = [r for r in m1 if r['precision'] is not None]
    prec = round(sum(r['precision'] for r in pr_) / len(pr_), 3) if pr_ else None
    smiss = sum(len(r['safety_missing']) for r in m1)
    i01 = [r for r in m1 if r['intent'] == 'I-01' and r['recall'] is not None]
    i01_face = [r['recall_with_face_layer'] for r in i01 if r.get('recall_with_face_layer') is not None]
    by_int = collections.OrderedDict()
    for r in m1:
        d = by_int.setdefault(r['intent'], {'n': 0, 'scored': 0, 'right': 0, 'recall': [], 'precision': [], 'safety_missing': 0, 'undecided': 0})
        d['n'] += 1
        if r['recall'] is None:
            d['undecided'] += 1
        else:
            d['scored'] += 1
            d['recall'].append(r['recall'])
        if r['precision'] is not None:
            d['precision'].append(r['precision'])
        d['right'] += r['status'] == '맞음'
        d['safety_missing'] += len(r['safety_missing'])
    for d in by_int.values():
        d['recall'] = round(sum(d['recall']) / len(d['recall']), 3) if d['recall'] else None
        d['precision'] = round(sum(d['precision']) / len(d['precision']), 3) if d['precision'] else None

    base = [r for r in m2 if not r['variant']]
    m2c = collections.Counter(r['status'] for r in base)
    m2v = collections.Counter(r['status'] for r in m2 if r['variant'])
    m2_by_origin = collections.OrderedDict()
    for r in base:
        d = m2_by_origin.setdefault(r['origin'], collections.Counter())
        d[r['status']] += 1
    m2_by_var = collections.OrderedDict()
    for r in m2:
        if r['variant']:
            m2_by_var.setdefault(r['variant'], collections.Counter())[r['status']] += 1
    found = m2c['찾음'] + m2c['후보 여럿(정답 포함)'] + m2c['찾음(정답 미정)'] + m2c['찾음(계열 옮김 결정)']
    judged = sum(v for k, v in m2c.items())

    sample_total = sum(v['sample'] for v in m3.values())
    sample_wrong = sum(v['verdicts'].get('틀림', 0) for v in m3.values())

    zero = m4['units_zero_safety']
    miss_n = len(m4['missing'])

    headline = {
        'M1': {'questions': len(Q), 'scored': len(scored), 'undecided': len(Q) - len(scored), 'right': sum(1 for r in m1 if r['status'] == '맞음'),
               'recall': rec, 'precision': prec, 'safety_missing': smiss,
               'i01_recall': round(sum(r['recall'] for r in i01) / len(i01), 3) if i01 else None,
               'i01_recall_with_face_layer': round(sum(i01_face) / len(i01_face), 3) if i01_face else None},
        'M2': {'words': len(base), 'variants': len(m2) - len(base), 'found_pct': pct(found, judged), 'status': dict(m2c),
               'variant_status': dict(m2v), 'not_found_pct': pct(m2c['못 찾음'], judged), 'wrong_pct': pct(m2c['틀리게 찾음'], judged),
               'multi_pct': pct(m2c['후보 여럿(정답 포함)'], judged)},
        'M3': {'kinds': len(m3), 'sampled': sample_total, 'wrong': sample_wrong, 'error_rate_pct': pct(sample_wrong, sample_total),
               'decision_based': sum(v['verdicts'].get('결정 근거', 0) for v in m3.values())},
        'M4': {'source_items': len(m4['items']), 'missing': miss_n,
               'missing_structured': sum(1 for x in m4['missing'] if x['structured'] is False),
               'missing_text_only': sum(1 for x in m4['missing'] if not x['in_silver_text']),
               'units_zero_safety': len(zero), 'units_total': m4['units_total']},
        'causes': len(cz),
    }
    staff = staff_questions(m1, m4)
    headline['staff_questions'] = len(staff)
    # 목표 판정(사용자 승인 10-30) — 의료진 질문 · 정답 미정 문항은 1차 목록(고정)으로 뺌
    goal = {}
    for mode, rows in (('cc', m1), ('nocc', m1_nocc), ('v1', m1_v1)):
        goal[mode] = goal_stats(rows) | {'path': I01_MODES[mode]}
    for mode in goal:
        goal[mode].update(m2_found_pct=headline['M2']['found_pct'], m3_error_pct=headline['M3']['error_rate_pct'], m4_missing=headline['M4']['missing'])
        goal[mode]['pass'] = goal_pass(goal[mode])
    headline['goal'] = goal
    rep = {'version': 'quality-eval v3', 'goal_excluded': sorted(GOAL_EXCLUDE), 'v1_compare': v1_compare(), 'generated_by': 'quality-eval.py', 'seed': SEED, 'conflict_board': CONFLICT_BOARD, 'boards': boards,
           'm1_raw_diff': raw_diff, 'per_kind': PER_KIND, 'inputs_sha256': INPUT_SHA,
           'headline': headline, 'by_intent': by_int, 'causes': cz, 'staff_questions': staff,
           'm1': m1, 'm2': {'rows': m2, 'by_origin': {k: dict(v) for k, v in m2_by_origin.items()}, 'by_variant': {k: dict(v) for k, v in m2_by_var.items()}},
           'm3': m3, 'm4': {k: v for k, v in m4.items() if k != 'items'} | {'items_n': len(m4['items'])}}
    with open(os.path.join(OUTD, 'quality-eval-set.json'), 'w', encoding='utf-8') as f:
        json.dump({'version': 'quality-eval-set v1', 'generated_by': 'quality-eval.py build_eval_set()',
                   'rule': '문항 = 샘플(S3p 11단계) · 원천 브론즈에 있는 말만 · 정답은 원천 칸 근거(없으면 「정답 미정」) · 가상 문장 없음',
                   'intents': [i['id'] for i in GOLD.get('intents', [])] if isinstance(GOLD.get('intents'), list) else None,
                   'n': len(Q), 'questions': Q}, f, ensure_ascii=False, indent=1, sort_keys=False)
    with open(os.path.join(OUTD, 'quality-report.json'), 'w', encoding='utf-8') as f:
        json.dump(rep, f, ensure_ascii=False, indent=1, default=lambda o: sorted(o) if isinstance(o, set) else str(o))
    write_md(rep, m2_by_origin, m2_by_var)


_V1 = os.path.join(W, 'quality-v1', 'quality-report.json')
GOAL_EXCLUDE = set()
if os.path.exists(_V1):  # 1차 의료진 질문 5 + 정답 미정 1 — 목표 계산에서 뺌(브리프 · 고정 목록)
    _v1r = L(_V1)
    GOAL_EXCLUDE = {re.search(r'Q\d+', s_['from']).group(0) for s_ in _v1r['staff_questions']} | {r_['id'] for r_ in _v1r['m1'] if r_['recall'] is None}
GOALS = [('recall', '질문 세트 재현율(전체)', 0.95, '>='), ('precision', '질문 세트 정밀도(전체)', 0.95, '>='), ('i01_recall', 'I-01 재현율', 0.95, '>='),
         ('i01_precision', 'I-01 정밀도', 0.95, '>='), ('safety_missing', '문항 안전 누락', 0, '=='), ('m4_missing', '원천 안전 원문 실버 누락(M4)', 0, '=='),
         ('m2_found_pct', '말 → 노드 찾기(%)', 97, '>='), ('m3_error_pct', '엣지 표본 오류율(%)', 1, '<=')]


def goal_stats(rows):
    sc = [r for r in rows if r['recall'] is not None and r['id'] not in GOAL_EXCLUDE]
    pr = [r for r in sc if r['precision'] is not None]
    i1 = [r for r in sc if r['intent'] == 'I-01']
    i1p = [r for r in i1 if r['precision'] is not None]
    rd = lambda xs, k: round(sum(x[k] for x in xs) / len(xs), 3) if xs else None
    return {'scored': len(sc), 'right': sum(r['status'] == '맞음' for r in sc), 'recall': rd(sc, 'recall'), 'precision': rd(pr, 'precision'),
            'i01_recall': rd(i1, 'recall'), 'i01_precision': rd(i1p, 'precision'), 'safety_missing': sum(len(r['safety_missing']) for r in sc),
            'wrong': [r['id'] for r in sc if r['status'] != '맞음']}


def goal_pass(g):
    out = {}
    for k, _, t, op_ in GOALS:
        v = g.get(k)
        out[k] = v is not None and ((v >= t) if op_ == '>=' else (v == t) if op_ == '==' else (v <= t))
    out['n_pass'] = sum(out.values())
    return out


def v1_compare():
    """1차 리포트(quality-v1) 값 — 1차 정의 그대로 + 목표 기준(의료진 · 정답 미정 뺌)으로 다시 셈."""
    if not os.path.exists(_V1):
        return None
    h1 = _v1r['headline']
    g = goal_stats(_v1r['m1'])
    g.update(m2_found_pct=h1['M2']['found_pct'], m3_error_pct=h1['M3']['error_rate_pct'], m4_missing=h1['M4']['missing'])
    g['pass'] = goal_pass(g)
    return {'headline': h1, 'goal': g}


def staff_questions(m1, m4):
    S = []
    for r in m1:
        if r['intent'] == 'I-03' and '2갈래' in r['answer_state']:
            S.append({'q': '소프웨이브(M9) 시술 후 사우나는 언제부터? 원천 「당일 피하기」(procedure-profiles) · 「24시간 고온 환경 회피」(taxonomy 울쎄라) · 샘플 「2주」 — 어느 값을 상담 정답으로?', 'from': r['id']})
        if r['intent'] == 'I-07' and r.get('got') and len(r['got'].get('same_day') or []) > 1:
            S.append({'q': f"「{r['text']}」 — 원천 주장이 같은 날 가능 · 불가 양쪽(충돌). 상담 정답은?", 'from': r['id']})
    for r in m1:
        iv = r.get('interval_values')
        if iv and iv['silver_lows'] and iv['source'] not in iv['silver_lows']:
            S.append({'q': f"「{r['text']}」 — 원천 treatment-sequence {iv['source']}일 · 실버(다른 원천 주장) 하한 {iv['silver_lows']}일. 상담 정답 간격은?", 'from': r['id']})
        if r['intent'] == 'I-07' and r['status'] == '틀림' and any('반대 값만' in w for w in r['why']) and r.get('got'):
            S.append({'q': f"「{r['text']}」 — 원천 treatment-sequence 「같은 날 불가」 ↔ 다른 원천 주장(실버) same_day {r['got'].get('same_day')}. 원천끼리 갈림 — 같은 날 가능 여부 정답은?", 'from': r['id']})
    for r in m1:
        if r['intent'] == 'I-10' and r['answer_state'].startswith('정답 미정'):
            S.append({'q': '샘플 「Juvéderm Voluma 2cc」 — 원천 products.json 필러 품목에 볼루마 없음. 팔자에 볼루마(볼 · 광대용 제형)를 쓰는 것이 상담 정답인가, 다른 쥬비덤 품목인가?', 'from': r['id']})
    return S


CTRL = os.path.join(W, 'quality-v1', 'v1-data-v2-eval.json')  # 1차 실버를 2차 측정으로 잰 값(대조 · python3 quality-eval.py --inputs quality-v1/inputs --out <폴더> 결과의 goal)

FIXES = [  # 원인 → 고친 단계 · 규칙 · 고정 시험(셈은 리포트 만들 때 실버에서 다시 셈)
    ('A', '7단계 R29 원천 부위 낱말', '① ③ ⑤ 엣지 원천 문구(cc · cc_group · cc_detail · 항목 이름)의 3단계 부위 낱말로 앵커 부위를 바꿈 — 결정으로만 붙은 부위(「불독살 → 턱선」)는 앵커 아님', 'step7 QA'),
    ('B', '7단계 R32 층 표시(U-1 ②)', '엣지 layer = 부위 · 상위(R21 로 올라간 층) · null — 부위 고민에 상위 층을 같이 내고 「상위」 표시', 'step7 QB'),
    ('C', '7단계 R30 원천 계열 밖 금지', '③ procedures[].category · ① modality_ref · ⑤ modality_ref ∪ 같은 이름 CC 계열 밖 단위 시술을 뺌 — 계열 옮김 결정(원장 · 시장가 원천 계열 · fam_kw 낱말)과 원천 이름이 바로 가리키는 시술은 둠', 'step7 QC'),
    ('E', '8단계 끝점 부위 낱말', '끝점 원문에 부위 낱말이 하나면 그 부위를 site_hint 로 풀이(resolver.endpoint_site_word)', 'step8 QE'),
    ('F', '시맨틱 사전 출처', '원장 이름(5단계 행선지) · 시장가 이름 · 환자용 이름 · 원천 CC 이름(→ CC 앵커) · 고민 갈래 이름(→ 노드 · 가까운 앵커)', 'semantic F1~F5'),
    ('G', '시맨틱 접두 규칙', '접두 일치는 대상 계열 · 고민 대분류가 하나로 모일 때만(resolve_rules.prefix_rule)', 'semantic G1 · G2'),
    ('H', '시맨틱 정규화', '「쳐짐 → 처짐」 접기 · 괄호 지움 · 끝말(주사 · 시술) 떼기', 'semantic H1~H3'),
    ('I', '8단계 원천 행 착지표', 'row_landing — 원천 행마다 주장 · 조건 · 피함 id 또는 「원문만(규칙)」 · 빠진 행 open(이미 있던 1:1 가드를 산출로)', 'step8 QI'),
    ('J', '5단계 · 8단계 안전 원문', '5단계 extracted 행 source_text(taxonomy 항목 safety · aftercare 원문 그대로) · 8단계 family_text 「사후관리(extracted.json aftercare)」', 'step5 QJ · step8 QJ'),
    ('K', '8단계 안전 상태', 'safety.unit_safety_status(칸마다 값 있음 · 해당 없음 · gap) · unit_gaps(모든 칸 gap 단위 시술 — G10 「없음 = 안전」 아님)', 'step8 QK'),
    ('L', '시맨틱 쌍 이름 · 와일드카드', '「모든 시술」 = scope:모든 시술(G16) · 쌍 이름은 F · H 로 찾음 · 조건부 주장은 질의가 조건 낱말을 말할 때(reading_contract 조회 옵션)', 'semantic L1 · L2'),
    ('M', '시맨틱 정규화 문서 = 코드', 'semantic.json dictionary.resolve_rules = semantic-build.py RESOLVE_RULES(측정 · 스킬이 이 칸을 읽음)', 'semantic M1~M3'),
    ('N', '7단계 R31 원천 제품 → 하위', '③ 원천 제품 이름(+ CC · 항목 이름 · 5단계 장비 이름 동의어)의 2단계 하위 밖 단위 시술을 뺌 · 하위를 안 정하고 올라간 층 하위가 둘 이상이면 계열만', 'step7 QN · S1'),
    ('O', '8단계 by_direction 읽기', '방향별 same_day 는 8단계에 이미 있음(E8-0077 a=False · b=True) — 측정이 reading_contract 대로 by_direction · options 「순서」를 읽게 고침', 'step8 QO'),
    ('3차 ①', '측정 계열 옮김 표', '손 표 대신 2단계 product_family · 2단계 결정 row_family · new_rows · 5단계 결정 원장 행선지 · 5단계 단위 시술 원천 계열 · 7단계 결정 fam_kw(원천 추천 시술 · 고민 항목 이름에 낱말)에서 읽음 — Q020(M8 → N4 「서브시전」) · Q025(M14 → N1 「지방분해」)', 'gold-prep G1a~G1d'),
    ('3차 ②', '2단계 다파장 하위', 'M8 · 원천 「…nm」 파장 둘 이상 · 주 · 보조 하위에 빠진 매질(10-30 ⑤ 넓힘) → 파장마다 원천 문장 근거가 가장 많은 매질을 보조로(532 → KTP · 755 → 알렉산드라이트 · 595 → PDL …) · 반도체 · IPL · LED 주 하위는 안 건드림 — 14행(엑셀 V = 엔디야그 + KTP) · 사용자 판단 ③(엑셀 V 동의어 U5-138 KTP)과 맞물림', 'gold-prep G2a~G2e'),
    ('3차 ③', '5단계 부작용 덮어쓰기 값', 'extracted 안전 원문(safety.*)을 붙는 수준 그대로 — 제품 × 계열(× 키 하위) → product_links[].side_effect_override · 단위 시술(후보) → units[].side_effect_override · override_of = 계열 · 1단계 합침(merged_into) 따라 활성 제품으로', 'step5 QG1a · QG1b'),
    ('3차 ④', '7단계 · 시맨틱 조합 구성', 'combo_component 셈 = components · members · upgrade(구성 칸 이름 그대로) — 462 → 581', 'step7 QG2 · gold-prep G4'),
    ('R28', '7단계 R28 CC 단위(코디 10-30)', '③ · ① 엣지 ccs[] · ⑤ cc_named[] — 질의 CC 가 원천 CC 면 같은 원천 문제 안 그 CC 엣지만(골드 도구 입력 후보 cc?)', 'step7 Q28'),
]

NOTES_ANSWER = [  # 정답이 원천 · 결정과 다르게 보이는 것 — 고치지 않고 보고(브리프) · 3차(골드 전 정리) 기준
    ('Q106', 'I-11 쁘띠시술 추천 조합 — 7단계 J5 「쁘띠시술 = 고민 앵커 없음(메뉴)」이라 고민 → 조합 경로로 못 찾음(골드 판단 몫)'),
    ('Q108 · Q109 · Q110', 'I-11 추천 조합 — 정답 = problem-combos 패키지 계열만 · 허브는 같은 고민 앵커의 조합 7종 출처(레시피 · 순서 · 최적화 · 비교 …)를 다 냄 → 정밀도 < 1(재현율 1.0). 정답 범위 ↔ 허브 응답 범위 차이(골드 판단 몫)'),
    ('정답 sub_families(문항 파일)', '정답의 하위 계열은 「원천 제품 이름 → 2단계 하위」 규칙으로 만든다 — 3차 2단계 결정(다파장 보조 KTP · 10-30 ⑤ 넓힘 포함)으로 Q012 · Q013 · Q018 · Q019 · Q022 · Q023 · Q031 의 정답 하위에 KTP 가 더해짐(문항 · 슬롯 · 의도 · 정답의 다른 칸 · 채점 식은 1차와 같음 — gold-prep-fixture-test G1d). 1번(옮김 표)만 반영했을 때는 문항 파일 바이트 같음 확인'),
    ('2단계 다파장 · 규칙 밖', '주 하위가 반도체 레이저 · IPL(셀렉V · 트리니티 · 소프라노 티타늄)이면 파장이 매질을 안 가리켜 안 건드림 — 10-30 ⑤ 로 「보조가 이미 있어도 빠진 매질은 더함」으로 넓혀 노블린 · 클라리티2 · 아포지 엘리트 플러스 · 디스커버리 피코에 KTP(step2-families.json multi_wavelength.seen)'),
    ('정답 site_words', 'I-01 정답의 부위 낱말 표(sites_in_text)가 「피코레이저」의 「코」를 부위로 잡음(Q013 · Q031 site_words [코]) — 점수엔 영향 없음. 7단계 R29 는 「앞이 한글이면 코 · 목 안 잡음」으로 고쳐 씀'),
]


def write_v2_head(rep, a):
    h = rep['headline']
    g = h['goal']
    v1 = rep['v1_compare']['goal']
    ctrl = L(CTRL)['goal']['cc'] if os.path.exists(CTRL) else None
    _v2p = os.path.join(W, 'quality-v2', 'inputs', 'quality-report.json')
    v2 = L(_v2p)['headline']['goal'] if os.path.exists(_v2p) else None
    a('# 허브 데이터 품질 측정 3차 — 골드 전 정리 뒤(2차 = 원인 14 고친 뒤)')
    a('')
    a(f"정본 `quality-report.json`(v3) · 문항 `quality-eval-set.json`(문항 · 슬롯 · 정답 규칙 · 채점 식은 1차 그대로 — 정답 하위 5문항만 2단계 결정으로 바뀜 · §0-3) · 스크립트 `quality-eval.py` · 1차 보관 `quality-v1/` · 2차 보관 `quality-v2/inputs/`(2차 리포트 · 입력 실버) · 시드 {rep['seed']} · 두 번 실행 cmp 같음 · 2026-10-30")
    a('')
    a(f"목표 계산에서 뺀 문항(브리프 — 1차 의료진 질문 5 · 정답 미정 1, 고정): {' · '.join(rep['goal_excluded'])}")
    a('')
    a('## 0. 목표 판정 — 1차 → 최종')
    a('')
    a('| 지표 | 목표 | 1차 | 1차 실버 × 2차 측정(대조) | 2차 · CC 슬롯 | 최종 · CC 없음 | 최종 · CC 슬롯(R28) |')
    a('|---|---|---|---|---|---|---|')
    ok = lambda x, k: '✅' if x['pass'][k] else '❌'
    for k, nm, t, op_ in GOALS:
        tt = {'>=': '≥', '==': '=', '<=': '≤'}[op_] + str(t)
        a(f"| {nm} | {tt} | {v1[k]} {ok(v1, k)} | {ctrl[k] if ctrl else '—'} | {v2['cc'][k] if v2 else '—'} | {g['nocc'][k]} {ok(g['nocc'], k)} | {g['cc'][k]} {ok(g['cc'], k)} |")
    six = lambda x: sum([x['pass']['recall'] and x['pass']['precision'], x['pass']['i01_recall'] and x['pass']['i01_precision'], x['pass']['safety_missing'], x['pass']['m4_missing'], x['pass']['m2_found_pct'], x['pass']['m3_error_pct']])
    a(f"| **목표 달성(6)** | | **{six(v1)}/6** | {six(ctrl) if ctrl else '—'}/6 | {six(v2['cc']) if v2 else '—'}/6 | **{six(g['nocc'])}/6** | **{six(g['cc'])}/6** |")
    a(f"| 맞은 문항(채점 {g['cc']['scored']}) | | {v1['right']} | {ctrl['right'] if ctrl else '—'} | {v2['cc']['right'] if v2 else '—'} | {g['nocc']['right']} | {g['cc']['right']} |")
    a('')
    a('읽는 법: 「CC 슬롯」 = R28(질의의 원천 CC 로 그 CC 엣지만 · 코디 10-30 「① cc 슬롯 추가 · 1차 방식 값과 나란히」 · 골드 도구 입력 후보 — 골드 판단 때 확정). 「CC 없음」 = 고민 노드 엣지 전부(1차와 같은 경로) + R32 층 표시. '
      '「1차 실버 × 2차 측정」 = 1차 입력 실버를 이 판 측정 스크립트로 잰 값 — 측정 변경만으로는 거의 안 움직이고 개선은 데이터 수정에서 나옴을 보이는 대조.')
    a('')
    a('### 0-1. 2차 측정 변경(문항 · 정답 · 채점 식은 그대로)')
    a('')
    for t_ in ['resolve = semantic.json dictionary.resolve_rules 그대로(정규화 · 낱말 나눔 · 끝말 · 접두 규칙 — 문서 = 코드)',
               'I-01 경로 = 엣지 layer 「상위」(R32 · U-1 ②)를 얼굴 전체 층으로 · CC 슬롯(R28) — CC 없음 값 나란히',
               '부위 무관 특수 부위(병변 단위 · 해당 없음 — 7단계 site_free)는 부위 층 거르기 통과(1차는 「점제거 → 병변 레이저」를 걸렀음)',
               '같이 · 간격 = 8단계 reading_contract(겉 same_day null 이면 by_direction · options 「순서」 · 조건부 주장은 질의가 조건 낱말(「심부 · 페놀」)을 말할 때)',
               '안전 묶음에 gap 상태(G13 · safety.unit_gaps) · M4 구조 = row_landing(「원문만(규칙)」 행은 안 싣는 이유가 규칙으로 명시된 것) · 4자 미만 실버 원문은 완전 같음 대조(1차는 「간독성」을 있어도 없음으로 셈)',
               '(3차) 계열 옮김 표 = 2 · 5 · 7단계 결정 파일에서(§0-2 3차 ①) · combo_component 엣지 표본 = 구성 칸 셋(components · members · upgrade)']:
        a(f'- {t_}')
    a('')
    a('### 0-2. 원인별 고침')
    a('')
    a('| 원인 | 고친 곳 | 규칙 | 고정 시험 |')
    a('|---|---|---|---|')
    for cid, where, rule, fx in FIXES:
        a(f'| {cid} | {where} | {rule} | {fx} |')
    a('')
    a('### 0-3. 남은 것(CC 슬롯 경로에서 틀린 문항 · 정답과 결정이 다른 것 — 고치지 않고 보고)')
    a('')
    a(f"틀린 문항(목표 계산 안): {' · '.join(g['cc']['wrong']) or '없음'}")
    a('')
    for k_, t_ in NOTES_ANSWER:
        a(f'- **{k_}** — {t_}')
    a('')
    a('의료진 질문(목표 계산 밖) — 1차 5문항 그대로: ' + ' · '.join(rep['goal_excluded']) + ' (아래 §2)')
    a('')


def write_md(rep, m2_by_origin, m2_by_var):
    h = rep['headline']
    L_ = []
    a = L_.append
    if rep.get('version') in ('quality-eval v2', 'quality-eval v3') and rep.get('v1_compare'):
        write_v2_head(rep, a)
        a('---')
        a('')
        a('# 상세 — 2차 판(경로 = CC 슬롯 R28 + R32 층 표시) · 아래 형식은 1차와 같음')
    else:
        a('# 허브 데이터 품질 측정 1차 — 정답 세트 · 결정론 측정')
    a('')
    a(f"정본 `quality-report.json` · 문항 `quality-eval-set.json` · 스크립트 `quality-eval.py`(결정론 · LLM 없음 · 시드 {rep['seed']} · 두 번 실행 cmp 같음) · 실버 · 시맨틱 · 브론즈 수정 없음 · 2026-10-30")
    a('')
    a(f"**충돌 판**: {rep['conflict_board']} — step8-relations sha256 {rep['inputs_sha256']['step8-relations.json']}. 8단계에 충돌 해소 칸(resolution_rule · resolved{{…}})이 생기면 `python3 quality-eval.py` 다시 실행 → 같이 · 간격(I-07 · I-08) 지표가 해소 값 기준으로 바뀜(스크립트가 칸 유무를 보고 자동 전환)")
    a('')
    a('| 판 | I-07 맞음/채점 · 재현율 · 안전 누락 | I-08 맞음/채점 · 재현율 |')
    a('|---|---|---|')
    for bn, bs in rep['boards'].items():
        a(f"| {bn} | {bs['I-07']['right']}/{bs['I-07']['n']} · {bs['I-07']['recall']} · {bs['I-07']['safety_missing']} | {bs['I-08']['right']}/{bs['I-08']['n']} · {bs['I-08']['recall']} |")
    a('')
    a(f"아래 표 · 원인 · 문항별은 **{rep['conflict_board']}** 기준. 판 사이 달라진 문항 {len(rep['m1_raw_diff'])}: " + '; '.join(f"{d['id']} {d['raw']}→{d['resolved']}" for d in rep['m1_raw_diff'][:12]))
    a('')
    a('## 0. 지표 한 표')
    a('')
    a('| 측정 | 지표 | 값 |')
    a('|---|---|---|')
    m1 = h['M1']
    a(f"| M1 질문 세트 | 문항 · 채점 · 정답 미정 | {m1['questions']} · {m1['scored']} · {m1['undecided']} |")
    a(f"| | 완전히 맞은 문항 | {m1['right']} / {m1['scored']} |")
    a(f"| | 재현율(문항 평균) · 정밀도(문항 평균) | {m1['recall']} · {m1['precision']} |")
    a(f"| | 안전 누락(문항에 나와야 할 안전 항목이 안 나옴) | {m1['safety_missing']} |")
    a(f"| | I-01 재현율 — 부위 층만 · 얼굴 전체 층(U-1) 넣으면 | {m1['i01_recall']} · {m1['i01_recall_with_face_layer']} |")
    m2 = h['M2']
    a(f"| M2 말 → 노드 | 말 · 규칙 변형 | {m2['words']} · {m2['variants']} |")
    a(f"| | 찾음(정답 포함 · 후보 여럿 포함) | {m2['found_pct']}% |")
    a(f"| | 못 찾음 · 틀리게 찾음 · 후보 여럿 | {m2['not_found_pct']}% · {m2['wrong_pct']}% · {m2['multi_pct']}% |")
    m3 = h['M3']
    a(f"| M3 엣지 표본 | 종류 · 표본 · 틀림 | {m3['kinds']} · {m3['sampled']} · {m3['wrong']} |")
    a(f"| | 오류율(표본) · 결정 근거(원천 직접 근거 없음) | {m3['error_rate_pct']}% · {m3['decision_based']} |")
    m4 = h['M4']
    a(f"| M4 안전 누락 | 원천 안전 항목 · 실버에 없음(원문 · 구조) | {m4['source_items']} · {m4['missing']} (구조 {m4['missing_structured']} · 원문 {m4['missing_text_only']}) |")
    a(f"| | 안전 정보 0 단위 시술 | {m4['units_zero_safety']} / {m4['units_total']} |")
    a(f"| 정리 | 원인 묶음 · 의료진 질문 | {h['causes']} · {h['staff_questions']} |")
    a('')
    a('읽는 법: 재현율 = 원천 정답(계열 · 값) 중 나온 비율 · 정밀도 = 나온 것 중 원천 계열 · 부위와 맞는 비율. 「결정 근거」 = 원천에 직접 근거가 없고 단계 결정으로 세운 것(오류로 세지 않음 · 따로 셈). 원천 → 실버 방향(M4)은 원문 대조(공백 · 부호 무시 부분 문자열) + 구조 칸 index 대조.')
    a('')
    a('## 1. 원인별 묶음(같은 원인 = 규칙 하나)')
    a('')
    a('| id | 원인 | 셈 | 고칠 규칙 | 고칠 단계 결정 | 예 |')
    a('|---|---|---|---|---|---|')
    for c in rep['causes']:
        ex = ' / '.join(e.replace('|', '¦') for e in c['examples'][:3])
        a(f"| {c['id']} | {c['title']} | {c['count']} | {c['fix_rule']} | {c['stage']} | {ex[:300]} |")
    a('')
    a('## 2. 의료진에게 물을 것(정답이 갈리는 문항만)')
    a('')
    for i, s in enumerate(rep['staff_questions'], 1):
        a(f"{i}. {s['q']} ({s['from']})")
    a('')
    a('## 3. M1 질문 세트 — 의도별')
    a('')
    a('| 의도 | 문항 | 채점 | 맞음 | 재현율 | 정밀도 | 안전 누락 | 정답 미정 |')
    a('|---|---|---|---|---|---|---|---|')
    for k, d in rep['by_intent'].items():
        a(f"| {k} | {d['n']} | {d['scored']} | {d['right']} | {d['recall']} | {d['precision']} | {d['safety_missing']} | {d['undecided']} |")
    a('| I-12 가격 | 0 | — | — | — | — | — | 연결 층(범위 밖) |')
    a('')
    a('### 3-1. 문항별(틀림 · 정답 미정)')
    a('')
    a('| 문항 | 의도 | 말(원천 · 샘플) | 재현율 | 정밀도 | 틀린 이유 | 안전 누락 |')
    a('|---|---|---|---|---|---|---|')
    for r in rep['m1']:
        if r['status'] == '맞음':
            continue
        why = '; '.join(r['why']).replace('|', '¦')[:220]
        sm = '; '.join(r['safety_missing']).replace('|', '¦')[:160]
        a(f"| {r['id']} | {r['intent']} | {r['text'][:40]} | {r['recall'] if r['recall'] is None else round(r['recall'], 2)} | {r['precision'] if r['precision'] is None else round(r['precision'], 2)} | {why} | {sm} |")
    a('')
    a('### 3-2. I-01 틀린 단위 시술(오연결)')
    a('')
    a('| 문항 | 말 | 단위 시술 | 부위 | 왜 |')
    a('|---|---|---|---|---|')
    for r in rep['m1']:
        for b in r.get('wrong_units') or []:
            a(f"| {r['id']} | {r['text'][:30]} | {b['unit']} {b['name']} | {b['site']} | {b['why']} |")
    a('')
    a('## 4. M2 말 → 노드')
    a('')
    a('| 출처 | 말 | 찾음 | 찾음(계열 옮김 결정) | 후보 여럿(정답 포함) | 찾음(정답 미정) | 틀리게 찾음 | 판정 보류 | 못 찾음 |')
    a('|---|---|---|---|---|---|---|---|---|')
    for k, d in m2_by_origin.items():
        a(f"| {k} | {sum(d.values())} | {d['찾음']} | {d['찾음(계열 옮김 결정)']} | {d['후보 여럿(정답 포함)']} | {d['찾음(정답 미정)']} | {d['틀리게 찾음']} | {d['판정 보류']} | {d['못 찾음']} |")
    a('')
    a('규칙 변형(표시 — 원천 말에 규칙만 적용, 새 말 지어내지 않음)')
    a('')
    a('| 변형 | 찾음 | 후보 여럿 | 틀리게 | 보류 | 못 찾음 |')
    a('|---|---|---|---|---|---|')
    for k, d in m2_by_var.items():
        a(f"| {k} | {d['찾음']} | {d['후보 여럿(정답 포함)']} | {d['틀리게 찾음']} | {d['판정 보류']} | {d['못 찾음']} |")
    a('')
    a('### 4-1. 못 찾은 말(원천 · 샘플)')
    a('')
    nf = [r for r in rep['m2']['rows'] if r['status'] == '못 찾음' and not r['variant']]
    by = collections.OrderedDict()
    for r in nf:
        by.setdefault(r['origin'], []).append(r['text'])
    for k, v in by.items():
        a(f"- **{k}** ({len(v)}): " + ' · '.join(v))
    a('')
    a('### 4-2. 틀리게 찾은 말')
    a('')
    a('| 말 | 출처 | 방식 | 찾은 대상 | 기대 |')
    a('|---|---|---|---|---|')
    for r in rep['m2']['rows']:
        if r['status'] == '틀리게 찾음':
            a(f"| {r['text']} | {r['origin']}{(' · ' + r['variant']) if r['variant'] else ''} | {r['mode']} | {', '.join(r['targets'][:3])} | {json.dumps(r['expect'], ensure_ascii=False)} |")
    a('')
    a('## 5. M3 엣지 표본 검수(종류 21 · 고정 시드 · 종류당 20 또는 전부)')
    a('')
    a('| 종류 | 행 | 표본 | 맞음 | 틀림 | 결정 근거 | 오류율 | 오류 꼴 | 전수(틀림/행) |')
    a('|---|---|---|---|---|---|---|---|---|')
    for k, v in rep['m3'].items():
        full = f"{v['full']['verdicts'].get('틀림', 0)}/{v['full']['n']}" if v['full'] else '—'
        forms = '; '.join(f'{f} {n}' for f, n in v['forms'].items())
        a(f"| {k} | {v['rows']} | {v['sample']} | {v['verdicts'].get('맞음', 0)} | {v['verdicts'].get('틀림', 0)} | {v['verdicts'].get('결정 근거', 0)} | {v['error_rate']} | {forms} | {full} |")
    a('')
    a('### 5-1. 전수 틀림(오연결 잡기 — treats · 조합 구성 · 관계 · 확인 조건 등)')
    a('')
    for k, v in rep['m3'].items():
        if v['full'] and v['full']['wrong']:
            a(f"**{k}** — 꼴: " + '; '.join(f'{f} {n}' for f, n in v['full']['wrong_forms'].items()))
            a('')
            for w in v['full']['wrong'][:40]:
                a(f"- {w['row']} — {w['evidence']}")
            if len(v['full']['wrong']) > 40:
                a(f"- … 외 {len(v['full']['wrong']) - 40} (json)")
            a('')
    a('## 6. M4 안전 누락(원천 → 실버 전수)')
    a('')
    a('| 원천 칸 | 항목 | 원문 없음 | 구조 대조 항목 | 구조 없음 |')
    a('|---|---|---|---|---|')
    for k, d in rep['m4']['by_group'].items():
        a(f"| {k} | {d['n']} | {d['missing_text']} | {d['structured_n']} | {d['structured_missing']} |")
    a('')
    a(f"- 단위 시술 {rep['m4']['units_total']} 중 안전 정보 0(합병증 · 부작용 · 확인 조건 · 위험지대 · 타임라인 · PIH · 금기류 관계 모두 없음, 전역 확인 조건 {rep['m4']['global_checks']} 제외): **{len(rep['m4']['units_zero_safety'])}**")
    a(f"- 부작용 · 합병증 둘 다 없음 {rep['m4']['units_no_side_or_complication']} · 확인 조건(전역 제외) 없음 {rep['m4']['units_no_checks']}")
    a('')
    a('안전 정보 0 단위 시술: ' + ' · '.join(f"{x['unit']} {x['name']}({x['family']})" for x in rep['m4']['units_zero_safety']))
    a('')
    a('### 6-1. 빠진 항목(앞 60)')
    a('')
    for x in rep['m4']['missing'][:60]:
        tag = '구조 없음' if x['structured'] is False else '원문 없음'
        a(f"- [{tag}] {x['path']} — {x['text'][:90]}")
    if len(rep['m4']['missing']) > 60:
        a(f"- … 외 {len(rep['m4']['missing']) - 60} (json `m4.missing`)")
    a('')
    a('## 7. 한계(이 측정이 못 본 것)')
    a('')
    a('- 정답은 원천 칸 기준 — 원천 자체가 틀린 것은 못 잡는다(원천 수정 후보는 각 단계 source_fix 쪽). 문헌 근거는 문헌 칸(literature-evidence)과 같은 계열 · 칸인지만 봄')
    a('- I-01 은 질의를 원천 말(고민 갈래 · CC)로만 넣는다 — Jev 슬롯 추출 품질은 안 봄. 정답 부위는 채점에만 쓰고 질의에 주지 않음(샘플 3 문항은 부위를 줌)')
    a('- 「결정 근거」는 원천 직접 근거가 없고 단계 결정으로 세운 엣지 — 오류율에서 빼고 따로 셈. 결정 자체가 맞는지는 이 측정 밖')
    a('- M4 원문 대조는 공백 · 부호 무시 부분 문자열 — 원천 문장을 고쳐 실은 것(쳐짐→처짐 등)은 「원문 없음」으로 셀 수 있음')
    a('- KOS 연결 · 가격(I-12)은 범위 밖(기록만)')
    open(os.path.join(OUTD, 'quality-report.md'), 'w', encoding='utf-8').write('\n'.join(L_) + '\n')


if __name__ == '__main__':
    main()
