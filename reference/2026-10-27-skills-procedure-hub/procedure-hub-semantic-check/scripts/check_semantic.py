"""Procedure Hub 시맨틱 정본(semantic.json) 점검 — 읽기만 · 표준 라이브러리.

하는 일
1. 재생성: semantic-build.py 와 입력(실버 정본 json 8 · step7/8-decisions · step3-lexicon)을 임시 폴더 둘에 복사해 각각 돌린다
   → 두 결과 바이트 같음(결정론) · 정본 semantic.json · .md 와 바이트 같음(낡음 = 실버가 바뀌었는데 재생성 안 함) · build 종료 코드 0(open 0)
2. 입력 판: semantic.json inputs[].sha256 = 지금 입력 파일 sha256 앞 16자리
3. 불변식(errors) — 실버 파일에서 따로 다시 셈
   - 노드 · 엣지 종류 셈: 종류 목록(13 · 21) · 종류마다 count = 실버 재셈 · summary = 목록 길이
   - 사전: norm 중복 없음 · norm = 정규화(expr) · 대상 여럿 ⇔ collision 표시 · mode(하나 · 전부 · 후보) · 후보 ⇔ ambiguous · 대상 id 가 id 대응표 정본 id(또는 none:)
   - id 대응: 실버 개체 전부가 대응표에 있음(빠짐 0) · 대응표에 실버 밖 행 0 · 정본 id 중복 0 · 키가 실버 id 와 다른 것은 결정 고민 노드(J{n}-…) · 목적(PU-nn)뿐 ·
     7단계 엣지 from 의 「목적:{이름}」 · 「J{n}-{한글}」 문자열이 문자열 대응표 또는 실버 id 로 풀림
   - 표시 12 · gate_status 3값: 이름 중복 없음 · 7단계 대응 · 8단계 주장의 gate_status 가 3값 안
   - 상속 9: I1 ~ I9 · 상속 엣지는 끝에 family 가 있음 · 상속 후보 · 끝점 묶음 원소는 저장 엣지 아님 · I5 site_check 셈 = 7단계 재셈 ·
     합병증 = 중대 반응만(B1 — moderate 이상 · 또는 원문 serious T 번호) · 부작용에 moderate 이상 0 · 합병증 gap 계열에 합병증 노드 0 · gap ⊂ 계열 ·
     확인 조건 주장에 「조건 아닌 문장」 섞임 0(B8)
4. --selftest: 정본 사본에 틀린 값을 넣어(대응 행 빠짐 · 겹침 표시 지움 · 없는 대상 id · 종류 셈 · 표시 빠짐 · 모르는 gate 값 · mild 합병증 ·
   상속 엣지 끝 · summary · 입력 판 · 정본 바이트 다름) 각각 errors 로 잡히는지 본다

사용
  python3 check_semantic.py --work orchestration/work/phub-recommend --out <scratchpad>/semantic-check.json
  python3 check_semantic.py --work orchestration/work/phub-recommend --out <scratchpad>/semantic-check.json --selftest
종료 코드: errors 0 (· selftest 전부 잡힘) 이면 0, 아니면 1.
"""
import argparse
import collections
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

sys.dont_write_bytecode = True  # 작업 폴더에 __pycache__ 를 남기지 않는다

SILVER = ['step1-products.json', 'step2-families.json', 'step3-sites.json', 'step4-techniques.json',
          'step5-units.json', 'step6-packages.json', 'step7-concerns.json', 'step8-relations.json']
DECISIONS = ['step7-decisions.json', 'step8-decisions.json', 'step3-lexicon.json',
             'step9-explanations.json']  # 9단계 설명 사실(11-01 · 값 사전 D9-7) — semantic-build 입력(실버 8 풀기와 따로)
OUTPUTS = ['semantic.json', 'semantic.md']
NODE_KINDS = ['product', 'family', 'site', 'technique', 'unit_procedure', 'package', 'concern', 'purpose', 'combo',
              'check_condition', 'complication', 'evidence_statement', 'evidence_source']
EDGE_KINDS = ['product_family', 'key_family', 'key_site', 'key_technique', 'child_of', 'concern_related', 'family_technique',
              'uses_product', 'contains', 'treats', 'concern_site', 'anchors_combo', 'combo_component', 'procedure_relation',
              'concern_avoid', 'requires_check', 'has_complication', 'site_caution', 'has_statement', 'cites', 'line_item']
GATE_VALUES = {'자동(완전 일치)', '자동(규칙)', '결정'}
MODES = {'하나', '전부', '후보'}
SERIOUS = {'moderate', 'severe', 'critical'}


RR = None  # semantic.json dictionary.resolve_rules(10-30 품질 M — 문서 = 코드) · 없으면 옛 규칙


def norm(s):
    """semantic-build.py norm 과 같은 뜻 — resolve_rules 가 있으면 그 규칙(NFKC · 악센트 접기 · fold · 공백 제거 · 괄호 지움 · 소문자) · 없으면 공백 제거 · NFKC · 소문자."""
    t = unicodedata.normalize('NFKC', str(s))
    if not RR:
        return re.sub(r'\s+', '', t).lower()
    t = unicodedata.normalize('NFC', ''.join(ch for ch in unicodedata.normalize('NFKD', t) if not unicodedata.combining(ch)))
    for a, b in RR['fold'].items():
        t = t.replace(a, b)
    t = re.sub(r'\s+', '', t)
    t = re.sub('[' + re.escape(RR['strip_chars']) + ']', '', t)
    return t.lower()


def load(work):
    J = lambda f: json.load(open(work / f, encoding='utf-8'))
    return {f: J(f) for f in SILVER + DECISIONS}


# ───────── 실버에서 따로 다시 센 개체 ─────────
def silver_objects(S):
    s1, s2, s3, s4, s5, s6, s7, s8 = [S[f] for f in SILVER]
    cc = s7['concerns']
    con = ([c for c in cc['categories'] if c.get('node')] + [c for c in cc['subcategories'] if c.get('node')]
           + [c for c in cc['items'] if c.get('kind') == '고민'] + cc['extra_items'])
    ev = s8['evidence']
    return {
        'product': [i['ledger_id'] for i in s1['items'] if i.get('active')],
        'family': [x['id'] for x in s2['families']],
        'site': [x['id'] for x in s3['nodes']],
        'technique': [x['id'] for x in s4['nodes']],
        'unit_procedure': [x['id'] for x in s5['units']],
        'package': [x['id'] for x in s6['packages']],
        'concern': [x['id'] for x in con],
        'purpose': [p['name'] for p in s7['purposes'] if p.get('node')],
        'combo': [x['id'] for x in s7['combos']],
        'check_condition': [x['id'] for x in s8['conditions']['nodes']],
        'complication': [x['id'] for x in s8['safety']['complications']],
        'evidence_statement': [x['id'] for x in ev['statements']],
        'evidence_source': [x['id'] for x in ev['literature'] + ev['web'] + ev['guides']],
    }


def silver_edge_counts(S):
    """엣지 종류마다 실버 칸에서 다시 셈 — 셈 정의는 semantic.json edge_kinds[].path 와 같다."""
    s1, s2, s3, s4, s5, s6, s7, s8 = [S[f] for f in SILVER]
    units = s5['units']
    special = s5['rules']['special_sites']
    cc = s7['concerns']
    con_sub = [c for c in cc['subcategories'] if c.get('node')]
    con_item = [c for c in cc['items'] if c.get('kind') == '고민']
    con_all = [c for c in cc['categories'] if c.get('node')] + con_sub + con_item + cc['extra_items']
    sf, ev = s8['safety'], s8['evidence']

    def anchors(c):
        a = c.get('anchor') or {}
        if a.get('concerns'):
            return a['concerns']
        x = a.get('concern')
        return [x] if isinstance(x, str) else (x or [])
    return {
        'product_family': sum(1 for r in s2['product_family'] if r.get('family')) + sum(len(r.get('also_families') or []) for r in s2['product_family']),
        'key_family': len(units),
        'key_site': sum(1 for u in units if u['key']['site'] not in special),
        'key_technique': sum(1 for u in units if u['key']['technique']),
        'child_of': (sum(1 for n in s3['nodes'] if n.get('parent')) + sum(1 for n in s4['nodes'] if n.get('parent'))
                     + sum(1 for c in con_sub if c.get('parent')) + len(con_item) + sum(1 for c in cc['extra_items'] if c.get('parent'))),
        'concern_related': sum(len(c.get('related') or []) for c in cc['extra_items']),
        'family_technique': sum(1 for r in s4['family_defaults'] if r.get('default')) + sum(len(r.get('also') or []) for r in s4['family_defaults']),
        'uses_product': sum(len(u.get('uses_product') or []) for u in units),
        'contains': len(s6['contains']) + sum(len(s.get('candidates') or []) for s in s6['slots']),
        'treats': len(s7['edges']),
        'concern_site': sum(len(c.get('sites') or []) for c in con_all),
        'anchors_combo': sum(len(anchors(c)) for c in s7['combos']),
        'combo_component': sum(len(x.get('units') or []) for c in s7['combos'] for f_ in ('components', 'members', 'upgrade') for x in c.get(f_) or []),  # 구성 칸 셋(10-30 골드 빈틈 ②)
        'procedure_relation': len(s8['edges']),
        'concern_avoid': len(s8['avoid_edges']),
        'requires_check': sum(len(k['conditions']) for k in s8['conditions']['claims']),
        'has_complication': len(sf['complications']),
        'site_caution': len(sf['site_caution']),
        'has_statement': len(ev['statements']),
        'cites': sum(len(x.get('evidence') or []) for x in ev['statements']) + sum(len(x.get('evidence') or []) for x in sf['complications']),
        'line_item': sum(1 for v in s1['lines'].values() for it in v.get('items') or [] if it.get('ledger_id')),
    }


def validate(sem, S, work_hashes):
    errors = []

    def err(t, **kw):
        errors.append(dict(type=t, **kw))

    s7, s8 = S['step7-concerns.json'], S['step8-relations.json']
    report = {}

    # 0. 입력 판
    for f, v in (sem.get('inputs') or {}).items():
        if f in work_hashes and v.get('sha256') != work_hashes[f]:
            err('입력 판 다름 — 실버가 바뀌었는데 재생성 안 함', file=f, semantic=v.get('sha256'), now=work_hashes[f])

    # 1. 노드 종류
    objs = silver_objects(S)
    nk = {n['kind']: n for n in sem['node_kinds']}
    if [n['kind'] for n in sem['node_kinds']] != NODE_KINDS:
        err('노드 종류 목록 다름', got=[n['kind'] for n in sem['node_kinds']], want=NODE_KINDS)
    for k in NODE_KINDS:
        if k in nk and nk[k]['count'] != len(objs[k]):
            err('노드 종류 셈 ≠ 실버 재셈', kind=k, semantic=nk[k]['count'], silver=len(objs[k]))
    report['node_kinds'] = {k: len(v) for k, v in objs.items()}

    # 2. 엣지 종류
    ec = silver_edge_counts(S)
    ek = {e['kind']: e for e in sem['edge_kinds']}
    if [e['kind'] for e in sem['edge_kinds']] != EDGE_KINDS:
        err('엣지 종류 목록 다름', got=[e['kind'] for e in sem['edge_kinds']], want=EDGE_KINDS)
    for k in EDGE_KINDS:
        if k in ek and ek[k]['count'] != ec[k]:
            err('엣지 종류 셈 ≠ 실버 재셈', kind=k, semantic=ek[k]['count'], silver=ec[k])
    report['edge_kinds'] = ec

    # 3. id 대응
    idmap = sem['ids']['map']
    canon = [m['canonical'] for m in idmap]
    for c, n in collections.Counter(canon).items():
        if n > 1:
            err('정본 id 중복', canonical=c, n=n)
    have = collections.defaultdict(set)
    for m in idmap:
        have[m['kind']].add(str(m['silver_id']))
        key = m['canonical'].split(':', 1)[1]
        if key != str(m['silver_id']):
            ok = (m['kind'] == 'concern' and re.fullmatch(r'J\d+', key) and str(m['silver_id']).startswith(key + '-')) or \
                 (m['kind'] == 'purpose' and re.fullmatch(r'PU-\d{2}', key))
            if not ok:
                err('정본 키가 실버 id 와 다름(허용 밖)', silver_id=m['silver_id'], canonical=m['canonical'])
    missing, extra = [], []
    for k, ids in objs.items():
        missing += [(k, i) for i in ids if str(i) not in have[k]]
        extra += [(k, i) for i in have[k] if i not in {str(x) for x in ids}]
    for k, i in missing:
        err('id 대응 빠짐 — 실버 개체가 대응표에 없음', kind=k, silver_id=i)
    for k, i in extra:
        err('id 대응표에 실버 밖 행', kind=k, silver_id=i)
    smap = sem['ids']['silver_string_map']
    unmapped = sorted({e['from'] for e in s7['edges'] if isinstance(e.get('from'), str)
                       and (e['from'].startswith('목적:') or re.match(r'J\d+-', e['from']))
                       and e['from'] not in smap and e['from'] not in have['concern']})
    for f in unmapped:
        err('7단계 엣지 from 문자열이 대응표에 없음(문자열 대응 · 실버 id 둘 다)', form=f)
    for f, c in smap.items():
        if c not in set(canon):
            err('문자열 대응 → 없는 정본 id', form=f, canonical=c)
    report['id_map'] = dict(rows=len(idmap), missing=len(missing), extra=len(extra), key_differs=sum(1 for m in idmap if m['canonical'].split(':', 1)[1] != str(m['silver_id'])))

    # 4. 사전
    global RR
    RR = sem['dictionary'].get('resolve_rules')
    exprs = sem['dictionary']['expressions']
    cset = set(canon)
    for n, c in collections.Counter(x['norm'] for x in exprs).items():
        if c > 1:
            err('사전 norm 중복 — 표현 행은 norm 하나에 하나', norm=n, n=c)
    coll = 0
    for x in exprs:
        tids = {t['id'] for t in x['targets']}
        if x['norm'] != norm(x['expr']):
            err('사전 norm ≠ 정규화(expr)', expr=x['expr'], norm=x['norm'])
        if not tids:
            err('사전 대상 없음', expr=x['expr'])
        multi = len(tids) > 1
        coll += multi
        if multi and not x.get('collision'):
            err('사전 겹침인데 collision 표시 없음', expr=x['expr'], targets=sorted(tids))
        if not multi and x.get('collision'):
            err('사전 대상 하나인데 collision 표시', expr=x['expr'])
        if x.get('mode') not in MODES or (multi and x['mode'] == '하나') or (not multi and x['mode'] != '하나'):
            err('사전 mode 어긋남', expr=x['expr'], mode=x.get('mode'), targets=len(tids))
        if bool(x.get('ambiguous')) != (x.get('mode') == '후보'):
            err('사전 후보 ⇔ ambiguous 어긋남', expr=x['expr'])
        for t in tids:
            if not (t in cset or t.startswith('none:') or t == 'scope:모든 시술'):  # scope = 와일드카드 범위(G16 · 10-30 품질 L)
                err('사전 대상 id 가 대응표에 없음', expr=x['expr'], target=t)
    report['dictionary'] = dict(expressions=len(exprs), collisions=coll, targets=sum(len(x['targets']) for x in exprs))

    # 5. 표시 · gate_status
    flags = sem['reading']['flags']
    fn = [f['flag'] for f in flags]
    if len(fn) != 12 or len(set(fn)) != len(fn):
        err('표시 12 아님 · 중복', flags=fn)
    for f in flags:
        if not f.get('fields') or not f.get('read') or not isinstance(f.get('count'), int):
            err('표시 칸 빠짐(fields · read · count)', flag=f.get('flag'))
    gv = {g['value'] for g in sem['reading']['gate_status']['values']}
    if gv != GATE_VALUES:
        err('gate_status 값 ≠ 3값', got=sorted(gv))
    bad_gate = collections.Counter(x.get('gate_status') for x in s7['correspondence'] if x.get('gate_status') not in GATE_VALUES)
    bad_gate += collections.Counter(c.get('gate_status') for c in s8['claims'] if c.get('gate_status') not in GATE_VALUES)
    for v, n in bad_gate.items():
        err('실버 gate_status 가 3값 밖', value=v, n=n)

    # 6. 상속 규칙 · 안전 분리
    inh = sem['inheritance']
    if [i['id'] for i in inh] != [f'I{n}' for n in range(1, 10)]:
        err('상속 규칙 I1 ~ I9 아님', got=[i['id'] for i in inh])
    for i in inh:
        if not i.get('rule') or not i.get('fields'):
            err('상속 규칙 칸 빠짐(rule · fields)', id=i.get('id'))
    for e in sem['edge_kinds']:
        if e['inherit'] and 'family' not in f"{e['frm']} {e['to']}":
            err('상속 엣지인데 끝에 계열 없음(I1)', kind=e['kind'])
    if {x['page'] for x in sem.get('not_edges') or []} != {'prod_unit_inh', 'set_member'}:
        err('저장 엣지 아님 목록 다름(B7 · B3 — 상속 후보 · 끝점 묶음 원소)', got=[x['page'] for x in sem.get('not_edges') or []])
    i5 = next((i for i in inh if i['id'] == 'I5'), None)
    sc = dict(collections.Counter(e.get('site_check') for e in s7['edges']))
    if i5 and (i5.get('count') or {}).get('site_check') != sc:
        err('I5 site_check 셈 ≠ 7단계 재셈', semantic=(i5.get('count') or {}).get('site_check'), silver=sc)
    sf = s8['safety']
    for c in sf['complications']:
        if not (c.get('severity') in SERIOUS or re.search(r'-T\d+$', c['id'])):
            err('합병증에 중대 반응 아닌 것(B1)', id=c['id'], severity=c.get('severity'))
    for x in sf['side_effects']:
        if x.get('severity') in SERIOUS:
            err('부작용에 moderate 이상(B1)', id=x.get('id'), severity=x['severity'])
    fam_ids = set(objs['family'])
    cx_fams = {c['family'] for c in sf['complications']}
    for g in sf['complication_gap_families']:
        if g not in fam_ids:
            err('합병증 gap 계열이 계열 목록에 없음(I9)', family=g)
        if g in cx_fams:
            err('합병증 gap 계열에 합병증 노드 있음(I9)', family=g)
    for k in s8['conditions']['claims']:
        if str(k.get('kind', '')).endswith('항목') and k.get('kind') != '사람 조건':
            err('확인 조건 주장에 조건 아닌 문장(B8)', kind=k.get('kind'), id=k.get('id'))
    report['safety'] = dict(complications=len(sf['complications']), side_effects=len(sf['side_effects']),
                            complication_gap=len(sf['complication_gap_families']), not_condition=len(s8['conditions'].get('not_condition') or []))

    # 7. summary
    sm = sem['summary']
    want = dict(node_kinds=len(sem['node_kinds']), edge_kinds=len(sem['edge_kinds']), glossary=len(sem['glossary']), flags=len(flags),
                gate_values=len(gv), inherit_rules=len(inh), dictionary_expressions=len(exprs), dictionary_collisions=coll,
                id_map=len(idmap), complications=len(sf['complications']), side_effects=len(sf['side_effects']),
                complication_gap_families=len(sf['complication_gap_families']), open=len(sem.get('open') or []))
    for k, v in want.items():
        if sm.get(k) != v:
            err('summary 불일치', key=k, summary=sm.get(k), recount=v)
    if sem.get('open'):
        err('정본 open 있음', n=len(sem['open']))
    return errors, report


def regen(work):
    """semantic-build.py 를 임시 폴더 둘에서 돌려 결정론 · 낡음을 본다. 작업 폴더는 건드리지 않는다."""
    res, outs = [], []
    for _ in range(2):
        d = Path(tempfile.mkdtemp(prefix='semchk-'))
        for f in SILVER + DECISIONS + ['semantic-build.py']:
            shutil.copy2(work / f, d / f)
        p = subprocess.run([sys.executable, '-B', str(d / 'semantic-build.py')], capture_output=True, text=True)
        res.append(p.returncode)
        outs.append({f: (d / f).read_bytes() for f in OUTPUTS if (d / f).exists()})
        shutil.rmtree(d, ignore_errors=True)
    return res, outs


def regen_errors(res, outs, canon_bytes):
    errors = []
    if any(r != 0 for r in res):
        errors.append(dict(type='semantic-build 종료 코드 ≠ 0(open 있음)', codes=res))
    for f in OUTPUTS:
        a, b = outs[0].get(f), outs[1].get(f)
        if a is None or a != b:
            errors.append(dict(type='결정론 아님 — 두 번 실행 바이트 다름', file=f))
        elif a != canon_bytes.get(f):
            errors.append(dict(type='정본 낡음 — 재생성 결과와 바이트 다름', file=f))
    return errors


def tampers(sem, S):
    """(이름, 기대 오류 type, 바꾸는 함수) — 정본 · 실버 사본에만."""
    def t_map_drop(m, s): m['ids']['map'] = [r for r in m['ids']['map'] if r['silver_id'] != 'U5-020']
    def t_coll(m, s): next(x for x in m['dictionary']['expressions'] if x.get('collision'))['collision'] = None
    def t_target(m, s): m['dictionary']['expressions'][0]['targets'].append(dict(id='unit_procedure:U5-999', qualifier=None, reasons=['주입']))
    def t_node(m, s): next(n for n in m['node_kinds'] if n['kind'] == 'concern')['count'] += 1
    def t_edge(m, s): s['step7-concerns.json']['edges'].pop()
    def t_flag(m, s): m['reading']['flags'].pop()
    def t_gate(m, s): s['step7-concerns.json']['correspondence'][0]['gate_status'] = '확인 대기'
    def t_mild(m, s): s['step8-relations.json']['safety']['complications'][0]['severity'] = 'mild'
    def t_inh(m, s): next(e for e in m['edge_kinds'] if e['kind'] == 'key_site')['inherit'] = True
    def t_summary(m, s): m['summary']['dictionary_expressions'] += 1
    def t_input(m, s): m['inputs']['step7-concerns.json']['sha256'] = '0' * 16
    def t_purpose(m, s): s['step7-concerns.json']['edges'][0]['from'] = '목적:없는 목적'
    def t_gap(m, s):
        f = s['step8-relations.json']['safety']['complications'][0]['family']
        s['step8-relations.json']['safety']['complication_gap_families'].append(f)
    return [
        ('id 대응 행 하나 빼기(U5-020)', 'id 대응 빠짐 — 실버 개체가 대응표에 없음', t_map_drop),
        ('겹침 행 collision 지우기', '사전 겹침인데 collision 표시 없음', t_coll),
        ('사전 대상에 없는 단위 시술', '사전 대상 id 가 대응표에 없음', t_target),
        ('고민 노드 셈 +1', '노드 종류 셈 ≠ 실버 재셈', t_node),
        ('7단계 엣지 하나 빼기(시맨틱 안 바꿈)', '엣지 종류 셈 ≠ 실버 재셈', t_edge),
        ('표시 하나 빼기', '표시 12 아님 · 중복', t_flag),
        ('7단계 대응 gate_status 「확인 대기」', '실버 gate_status 가 3값 밖', t_gate),
        ('합병증 severity mild', '합병증에 중대 반응 아닌 것(B1)', t_mild),
        ('계열 없는 엣지에 상속 표시', '상속 엣지인데 끝에 계열 없음(I1)', t_inh),
        ('summary 사전 표현 +1', 'summary 불일치', t_summary),
        ('입력 판 sha 바꾸기', '입력 판 다름 — 실버가 바뀌었는데 재생성 안 함', t_input),
        ('7단계 엣지 from 「목적:없는 목적」', '7단계 엣지 from 문자열이 대응표에 없음(문자열 대응 · 실버 id 둘 다)', t_purpose),
        ('합병증 있는 계열을 gap 에', '합병증 gap 계열에 합병증 노드 있음(I9)', t_gap),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True, help='orchestration/work/phub-recommend')
    ap.add_argument('--out', required=True, help='결과 json 경로(scratchpad)')
    ap.add_argument('--selftest', action='store_true', help='틀린 값을 넣어 잡히는지')
    a = ap.parse_args()
    work = Path(a.work).resolve()
    sem = json.load(open(work / 'semantic.json', encoding='utf-8'))
    S = load(work)
    hashes = {f: hashlib.sha256((work / f).read_bytes()).hexdigest()[:16] for f in SILVER + DECISIONS}
    canon_bytes = {f: (work / f).read_bytes() for f in OUTPUTS}

    res, outs = regen(work)
    errors = regen_errors(res, outs, canon_bytes)
    inv, report = validate(sem, S, hashes)
    errors += inv

    selftest = []
    if a.selftest:
        for name, want, fn in tampers(sem, S):
            m, s = copy.deepcopy(sem), copy.deepcopy(S)
            fn(m, s)
            got = {e['type'] for e in validate(m, s, hashes)[0]}
            selftest.append(dict(tamper=name, expect=want, caught=want in got, got=sorted(got)))
        # 정본 바이트가 재생성과 다르면 잡히나(한 바이트 더함)
        fake = dict(canon_bytes)
        fake['semantic.json'] = canon_bytes['semantic.json'] + b' '
        got = {e['type'] for e in regen_errors(res, outs, fake)}
        want = '정본 낡음 — 재생성 결과와 바이트 다름'
        selftest.append(dict(tamper='정본 semantic.json 바이트 다름', expect=want, caught=want in got, got=sorted(got)))
        # 두 번 실행 결과가 다르면 잡히나
        o2 = [dict(outs[0]), dict(outs[1])]
        o2[1]['semantic.md'] = (o2[1].get('semantic.md') or b'') + b'x'
        got = {e['type'] for e in regen_errors(res, o2, canon_bytes)}
        want = '결정론 아님 — 두 번 실행 바이트 다름'
        selftest.append(dict(tamper='두 번 실행 결과 다름', expect=want, caught=want in got, got=sorted(got)))

    out = dict(work=str(work), build_exit=res, inputs=hashes, report=report, errors=errors, selftest=selftest,
               summary=dict(errors=len(errors), selftest_caught=sum(x['caught'] for x in selftest), selftest_total=len(selftest)))
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    st = (f" · selftest {sum(x['caught'] for x in selftest)}/{len(selftest)} 잡힘" if selftest else '')
    r = report
    print(f"노드 종류 {len(r['node_kinds'])} · 엣지 종류 {len(r['edge_kinds'])} · 사전 표현 {r['dictionary']['expressions']}(겹침 {r['dictionary']['collisions']})"
          f" · id 대응 {r['id_map']['rows']}(빠짐 {r['id_map']['missing']}) · 합병증 {r['safety']['complications']} · 부작용 {r['safety']['side_effects']}"
          f" · gap {r['safety']['complication_gap']} · build {res} · errors {len(errors)}{st} → {a.out}")
    bad = errors or (selftest and not all(x['caught'] for x in selftest))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
