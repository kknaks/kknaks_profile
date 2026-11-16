"""실버 4단계(기법) 반영 — 결정론. 결정 = _RESUME §2 10-28 「4단계 기법 조사 반영 — 전부 추천대로」 · J1 안 1 · J2 · + 3단계 「표정근」.

입력: step4-decisions.json(결정 — 노드 · 값 사전 · 표현 행선지 · 넘겨받은 것 · technique_hint · 계열 기본 · 초안 대응 · 수정 목록)
      source-map.json(4단계 칸만 고른다) · 원천(결정 source.path)
      step3-decisions.json danger_zone_mapping · step3-sites.json(노드 · deferred · handoff_note — 읽기만)
      step2-families.json(계열 · technique_hint · 4단계 deferred — 읽기만) · procedure-master-v3.json techniques(초안 — 읽기만)
출력: step4-techniques.json · step4-techniques.md · step4-source-fix.md

표현 행은 원천에서 이 스크립트가 만든다(지도 4단계 칸만). 결정 없는 표현 · 결정 없는 넘김 · hint · 계열 · 초안 → open[].
결정 파일에 한 줄을 더하면 닫힌다. 숫자는 이 파일에 적지 않는다.
"""
import argparse
import collections
import json
import re
from pathlib import Path

W = Path(__file__).resolve().parent
AP = argparse.ArgumentParser()
AP.add_argument('--source', help='원천 경로 덮어쓰기(고정 시험용)')
AP.add_argument('--decisions', default=str(W / 'step4-decisions.json'))
AP.add_argument('--out', default=str(W), help='산출 폴더(고정 시험은 임시 폴더)')
ARGS = AP.parse_args()
OUT = Path(ARGS.out)
DEC = json.load(open(ARGS.decisions))
SRC = Path(ARGS.source or DEC['source']['path'])
SMAP = json.load(open(W / DEC['source_map']['file']))
S3D = json.load(open(W / DEC['zone_site']['file']))
S3 = json.load(open(W / 'step3-sites.json'))
S2 = json.load(open(W / 'step2-families.json'))
PM = json.load(open(W / 'procedure-master-v3.json'))


def fail(msg):
    raise SystemExit(f'검사 실패: {msg}')


opened = []


def op(type_, **kw):
    opened.append(dict(type=type_, **kw))


def txt(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


# ───────── 1. 원천 → 표현 행(지도 4단계 칸만) ─────────
cells = [f for f in SMAP['fields'] if any(d['stage'] == DEC['source_map']['stage'] for d in f['destinations'])]
LBL = DEC['index_label']


def expand(node, parts, prefix, out):
    """source-map 경로(`zones[].tissue_data.notes` · `{code}.related_techniques`)를 원천 값으로 펼친다. 리스트 값은 한 줄씩."""
    if not parts:
        if isinstance(node, list):
            for v in node:
                out.append((prefix, txt(v)))
        elif node is not None:
            out.append((prefix, txt(node)))
        return
    p, rest = parts[0], parts[1:]
    if p == '{code}':
        for k in node:
            expand(node[k], rest, k, out)
        return
    m = re.fullmatch(r'(\w+)\[\]', p)
    if m:
        name = m.group(1)
        for el in node.get(name, []):
            if LBL[name] not in el:
                fail(f'{name} 원소에 {LBL[name]} 없음')
            expand(el, rest, f"{prefix + '.' if prefix else ''}{name}[{el[LBL[name]]}]", out)
        return
    if isinstance(node, dict) and p in node:
        expand(node[p], rest, f"{prefix + '.' if prefix else ''}{p}", out)


raw = []  # (file, key, text)
for c in cells:
    vals = []
    expand(json.load(open(SRC / c['file'])), c['path'].split('.'), '', vals)
    raw += [(c['file'], k, t) for k, t in vals]
n_lines = len(raw)

# 중복 규칙(extracted ↔ taxonomy)
DD = DEC['dedupe']
tax_lines = collections.defaultdict(set)
for f, k, t in raw:
    if f == DD['against_file'] and k.endswith('.extracted.related_techniques'):
        tax_lines[re.match(r'modality\[(\w+)\]', k).group(1)].add(t)
rows, dup = [], collections.OrderedDict()
for f, k, t in raw:
    if f == DD['file'] and t in tax_lines.get(k.split('.')[0], ()):
        dup.setdefault(k, 0)
        dup[k] += 1
        continue
    rows.append((f, k, t))
cnt = collections.Counter(rows)
rows = list(dict.fromkeys(rows))

# ───────── 2. 기준 목록 ─────────
NODES = {n['id']: n for n in DEC['nodes']}
for n in DEC['nodes']:
    if n['parent'] and (n['parent'] not in NODES or NODES[n['parent']]['parent']):
        fail(f'노드 {n["id"]} 상위 {n["parent"]} — 없거나 2층을 넘음')
if len(NODES) != len(DEC['nodes']):
    fail('노드 id 겹침')
DI = DEC['dictionaries']
LAYERS = set(DI['layer'])
MUSCLES = {m['key']: m for m in DI['target_muscle']}
PULSE, ABL, MODES = set(DI['pulse_mode']), set(DI['ablative']), {m['value']: m for m in DI['modes']}
SITES = {n['name'] for n in S3['nodes']}
FAMS = {f['id']: f for f in S2['families']}
ZONE_SITE = {z['zone']: z['node'] for z in S3D['danger_zone_mapping']}
STAGES = {'2단계', '5단계', '7단계', '8단계', '계열 밖', '시맨틱'}
for m in MUSCLES.values():
    for s in m['sites']:
        if s not in SITES:
            op('값 사전 오류', what=f"대상 근육 {m['key']} 부위 {s} 없음(3단계)")
for m in MODES.values():
    if m['node'] not in NODES:
        op('값 사전 오류', what=f"가능 방식 {m['value']} 노드 {m['node']} 없음")

# ───────── 3. 표현 행선지 ─────────
route = {}
for e in DEC['expressions']:
    k = (e['file'], e['key'], e['text'])
    if k in route:
        fail(f'결정 표현 중복 {k}')
    route[k] = e


def check_expr(e):
    if e['bucket'] == '노드로' and e.get('node') not in NODES:
        return f"노드 {e.get('node')} 없음"
    if e['bucket'] == '넘김' and e.get('stage') not in STAGES:
        return f"넘김 단계 {e.get('stage')}"
    if e.get('node') and e['node'] not in NODES:
        return f"노드 {e['node']} 없음"
    for l in e.get('layers', []):
        if l not in LAYERS:
            return f'층 {l} 사전 밖'
    for m in e.get('muscles', []):
        if m['muscle'] not in MUSCLES:
            return f"대상 근육 {m['muscle']} 사전 밖"
        if any(s not in SITES for s in m['sites']):
            return f"부위 {m['sites']} 없음(3단계)"
    for a in e.get('attach', []):
        if 'muscle' in a and a['muscle'] not in MUSCLES:
            return f"근거 대상 근육 {a['muscle']} 사전 밖"
        if 'layer' in a and (a['layer'] not in LAYERS or a['site'] not in SITES):
            return f"근거 층 {a['layer']}@{a['site']} 사전 · 부위 밖"
    if e.get('layers'):
        z = re.match(r'zones\[(\w+)\]', e['key'])
        if not z or z.group(1) not in ZONE_SITE:
            return '층 값인데 zone → 부위 대응 없음(3단계)'
    return None


expr_rows = []
for f, k, t in rows:
    e = route.get((f, k, t))
    row = dict(file=f, key=k, text=t, count=cnt[(f, k, t)])
    if e is None:
        row.update(bucket='open', destination='open')
        op('결정 없는 표현', file=f, key=k, text=t)
    else:
        row.update({x: e.get(x) for x in ('verdict', 'bucket', 'stage', 'destination', 'node', 'name', 'group', 'layers', 'constraint_text',
                                         'muscles', 'other_parts', 'attach', 'basis', 'note', 'decided_by')})
        bad = check_expr(e)
        if bad:
            row['bucket'] = 'open'
            op('행선지 오류', file=f, key=k, text=t, reason=bad)
    expr_rows.append(row)
for k, n in dup.items():
    expr_rows.append(dict(file=DD['file'], key=k, text=f"({DD['against_file']} modality[{k.split('.')[0]}] 와 {n}줄 같음)", count=n,
                          verdict='중복', bucket='중복', destination=DD['destination'], decided_by=DD['decided_by']))
found = set(rows)
stale = [list(k) for k in route if k not in found]

# ───────── 4. 단위 시술 속성: 부위 × 층(safe_layers) · 대상 근육 · 근거 ─────────
safe_layers = collections.OrderedDict()
for r in expr_rows:
    if r['bucket'] != 'open' and r.get('layers'):
        z = re.match(r'zones\[(\w+)\]', r['key']).group(1)
        safe_layers[ZONE_SITE[z]] = dict(site=ZONE_SITE[z], zone=z, technique='K01', layers=r['layers'], constraint_text=r['constraint_text'],
                                         source_text=r['text'], from_split=None, evidence=[])
for sp in DEC['site_layer_split']:
    g = safe_layers.get(sp['group_site'])
    if ZONE_SITE.get(sp['zone']) != sp['group_site'] or g is None or g['layers'] != sp['group_layers']:
        op('층 나눔 오류', what=f"{sp['zone']} → {sp['group_site']} 묶음 층이 원천 행과 다름")
        continue
    for s in sp['splits']:
        if s['site'] not in SITES or not set(s['layers']) <= set(g['layers']):
            op('층 나눔 오류', what=f"{s['site']} {s['layers']} — 부위 없음 또는 묶음 층 밖")
            continue
        safe_layers[s['site']] = dict(site=s['site'], zone=sp['zone'], technique='K01', layers=s['layers'], constraint_text=s['basis'],
                                      source_text=g['source_text'], from_split=sp['group_site'], evidence=[])
muscle_out = collections.OrderedDict((k, dict(key=k, ko_kma=m['ko_kma'], source_label=m['source_label'], sites=list(m['sites']),
                                              group=m.get('group', False), basis=m['basis'], from_rows=[], evidence=[], handoffs=[]))
                                     for k, m in MUSCLES.items())
for r in expr_rows:
    if r['bucket'] == 'open':
        continue
    for m in r.get('muscles') or []:
        mo = muscle_out[m['muscle']]
        mo['from_rows'].append(dict(key=r['key'], sites=m['sites']))
    for a in r.get('attach') or []:
        ev = dict(key=r['key'], text=r['text'], verdict=r['verdict'])
        if 'muscle' in a:
            muscle_out[a['muscle']]['evidence'].append(ev)
        else:
            tgt = safe_layers.setdefault(a['site'], dict(site=a['site'], zone=None, technique='K01', layers=[], constraint_text=None,
                                                         source_text=None, from_split=None, evidence=[]))
            tgt['evidence'].append(dict(ev, layer=a['layer']))

# ───────── 5. 넘겨받은 것 — 4단계로 보낸 것 전수가 행선지를 갖나 ─────────
s3_def = {tuple(d['key']) for d in S3['deferred'] if '4단계' in d['stage']}
s3_cmp = {(s['normalized'], s['group']) for s in S3['strings'] if any('4단계' in h.get('stage', '') for h in (s['handoff'] or []))} - s3_def
s3_note = {n['name'] for n in S3['nodes'] if n['handoff_note'] and '4단계' in n['handoff_note']}
s3_str = {(s['normalized'], s['group']) for s in S3['strings']}
s2_def = {f['id'] for f in S2['families'] for d in (f.get('deferred') or []) if '4단계' in str(d.get('deferred_to'))}
s2_led = {x['ledger_id'] for x in S2['product_family']}
cov = dict(def_=set(), cmp=set(), note=set(), fam=set())
for h in DEC['handoffs']:
    r = h['source_ref']
    t = r['type']
    ok = True
    if t == 'step3_deferred':
        ok = tuple(r['key']) in s3_def
        cov['def_'].add(tuple(r['key']))
    elif t == 'step3_compound':
        ok = all(tuple(k) in s3_cmp for k in r['keys'])
        cov['cmp'] |= {tuple(k) for k in r['keys']}
    elif t == 'step3_handoff_note':
        ok = r['node'] in s3_note
        cov['note'].add(r['node'])
    elif t == 'step2_deferred':
        ok = r['family'] in s2_def
        cov['fam'].add(r['family'])
    elif t == 'step2_ledger':
        ok = all(i in s2_led for i in r['ledger_ids'])
    elif t == 'step3_string':
        ok = tuple(r['key']) in s3_str
    if not ok:
        op('넘겨받은 것 원천 없음', id=h['id'], item=h['item'])
for k in sorted(s3_def - cov['def_']):
    op('넘겨받은 것 행선지 없음', source='step3 deferred', item=list(k))
for k in sorted(s3_cmp - cov['cmp']):
    op('넘겨받은 것 행선지 없음', source='step3 부위+다른 축', item=list(k))
for k in sorted(s3_note - cov['note']):
    op('넘겨받은 것 행선지 없음', source='step3 handoff_note', item=k)
for k in sorted(s2_def - cov['fam']):
    op('넘겨받은 것 행선지 없음', source='step2 deferred 4단계', item=k)
landmarks = []
for h in DEC['handoffs']:  # 넘김이 값 사전에 닿는 곳(대상 근육 · 주입 지표)
    for m in h.get('muscles', []):
        if m['muscle'] not in muscle_out or any(s not in SITES for s in m['sites']) or not set(m['sites']) <= set(muscle_out[m['muscle']]['sites']):
            op('넘겨받은 것 값 오류', id=h['id'], what=f"대상 근육 {m['muscle']} @ {m['sites']} — 사전 · 부위 밖")
            continue
        muscle_out[m['muscle']]['handoffs'].append(h['id'])
    for lm in h.get('landmarks', []):
        if lm['site'] not in SITES:
            op('넘겨받은 것 값 오류', id=h['id'], what=f"주입 지표 부위 {lm['site']} 없음")
            continue
        landmarks.append(dict(lm, handoff=h['id']))

for m in muscle_out.values():  # 대상 근육 값은 원천 행이나 넘겨받은 것 하나는 있어야 선다
    if not m['from_rows'] and not m['evidence'] and not m['handoffs']:
        op('근거 없는 대상 근육', muscle=m['key'])

# ───────── 6. technique_hint(장비 속성) ─────────
hint_dec = {h['ledger_id']: h for h in DEC['technique_hints']}
hint_src = {x['ledger_id']: x for x in S2['product_family'] if x.get('technique_hint')}
hints = []
for lid in hint_src:
    h = hint_dec.get(lid)
    if h is None:
        op('결정 없는 technique_hint', ledger_id=lid, hint=hint_src[lid]['technique_hint'])
        continue
    bad = None
    if h['hint'] != hint_src[lid]['technique_hint']:
        bad = f"원천 hint {hint_src[lid]['technique_hint']} ≠ 결정 {h['hint']}"
    elif h.get('pulse_scope') and not any(a['sub_family'] in h['pulse_scope'] for a in hint_src[lid].get('also_sub_families') or []):
        bad = f"pulse_scope {h['pulse_scope']} — step2 보조 하위 계열에 없음"
    elif any(p not in PULSE for p in h['pulse_mode']) or any(m not in MODES for m in h['modes']) or any(a['value'] not in ABL for a in h['ablative']):
        bad = '값 사전 밖'
    if bad:
        op('technique_hint 오류', ledger_id=lid, reason=bad)
    hints.append(h)
stale += [['technique_hints', k] for k in hint_dec if k not in hint_src]

# ───────── 7. 계열 기본 기법 ─────────
fd = {f['family']: f for f in DEC['family_defaults']}
for fid in FAMS:
    f = fd.get(fid)
    if f is None:
        op('결정 없는 계열 기본 기법', family=fid)
    elif f['default'] not in NODES or any(a not in NODES for a in f['also']):
        op('계열 기본 기법 오류', family=fid, reason=f"노드 {f['default']} · {f['also']}")
stale += [['family_defaults', k] for k in fd if k not in FAMS]

# ───────── 8. 초안 큰 기법 65 ─────────
dd = {t['id']: t for t in DEC['draft_techniques']}
for t in PM['techniques']:
    d = dd.get(t['id'])
    if d is None:
        op('결정 없는 초안 기법', id=t['id'], name=t['name'])
    elif d['name'] != t['name'] or (d['verdict'] in ('유지', '합침') and d['node'] not in NODES) or d['verdict'] not in ('유지', '합침', '버림'):
        op('초안 기법 오류', id=t['id'], name=t['name'])
stale += [['draft_techniques', k] for k in dd if k not in {t['id'] for t in PM['techniques']}]

# ───────── 9. 노드 ─────────
out_nodes = []
for n in DEC['nodes']:
    i = n['id']
    out_nodes.append(dict(
        id=i, name=n['name'], parent=n['parent'], level='세부' if n['parent'] else '큰',
        medical_name=n['medical_name'], basis=n['basis'],
        children=[c['id'] for c in DEC['nodes'] if c['parent'] == i],
        family_default=[f['family'] for f in DEC['family_defaults'] if f['default'] == i],
        family_also=[f['family'] for f in DEC['family_defaults'] if i in f['also']],
        source_expressions=[dict(key=r['key'], text=r['text'], verdict=r['verdict']) for r in expr_rows if r.get('node') == i and r['bucket'] == '노드로'],
        draft_techniques=[f"{t['id']} {t['name']}" for t in DEC['draft_techniques'] if t['node'] == i and t['verdict'] != '버림'],
        modes=[m['value'] for m in MODES.values() if m['node'] == i]))
has = lambda n: bool(n['source_expressions'] or n['family_default'] or n['family_also'] or n['draft_techniques'])
by_id = {n['id']: n for n in out_nodes}
for n in out_nodes:  # 큰 기법은 세부 기법 근거로도 선다(K12 소수술 ← 서브시전 · 펀치 · 압출)
    if not has(n) and not any(has(by_id[c]) for c in n['children']):
        op('근거 없는 노드', id=n['id'], name=n['name'])

# ───────── 10. 셈 ─────────
bk = collections.Counter(r['bucket'] for r in expr_rows)
summary = dict(
    source=dict(path=str(SRC), cells=len(cells), lines=n_lines, values=len(expr_rows), unique_values=len(rows),
                dup_groups=len(dup), dup_lines=sum(dup.values())),
    nodes=len(out_nodes), nodes_by_level=dict(collections.Counter(n['level'] for n in out_nodes)),
    by_bucket=dict(sorted(bk.items(), key=lambda kv: -kv[1])),
    by_verdict=dict(collections.Counter(r.get('verdict') for r in expr_rows if r['bucket'] != 'open')),
    handoff_by_stage=dict(sorted(collections.Counter(r['stage'] for r in expr_rows if r['bucket'] == '넘김').items(), key=lambda kv: -kv[1])),
    dictionaries={k: len(v) for k, v in DI.items() if k not in ('device_attrs', 'unit_procedure_attrs')},
    safe_layer_sites=len(safe_layers), safe_layer_sites_with_layers=sum(1 for s in safe_layers.values() if s['layers']),
    target_muscles=len(muscle_out), landmarks=len(landmarks),
    handoffs=len(DEC['handoffs']), hints=len(hints), family_defaults=len(fd),
    draft_techniques=dict(collections.Counter(t['verdict'] for t in DEC['draft_techniques'])),
    conflicts=len(DEC['conflicts']), oq_closed=len(DEC['oq_closed']),
    open=len(opened), open_by_type=dict(collections.Counter(o['type'] for o in opened)), stale_decisions=len(stale))
J = dict(version=DEC['version'], decision_ref=DEC['decision_ref'],
         inputs=['step4-decisions.json', f"{DEC['source_map']['file']} 4단계 칸", str(SRC), 'step3-decisions.json danger_zone_mapping', 'step3-sites.json',
                 'step2-families.json', 'procedure-master-v3.json techniques'],
         summary=summary, nodes=out_nodes, dictionaries=DI,
         unit_procedure_attrs=dict(safe_layers=list(safe_layers.values()), target_muscles=list(muscle_out.values()), landmarks=landmarks),
         device_attrs=dict(technique_hints=hints, pulse_by_medium=DEC['pulse_by_medium']),
         family_defaults=DEC['family_defaults'], draft_techniques=DEC['draft_techniques'], handoffs=DEC['handoffs'],
         expressions=expr_rows, conflicts=DEC['conflicts'], user_decisions=DEC['user_decisions'], oq_closed=DEC['oq_closed'],
         not_done=DEC['not_done'], open=opened, stale_decisions=stale)
json.dump(J, open(OUT / 'step4-techniques.json', 'w'), ensure_ascii=False, indent=1)

# ───────── 11. md ─────────
S = summary
L = []
P = L.append
P('---\ntype: silver\nid: step4-techniques\ntitle: "실버 4단계 — 기법 원장"\nproduct: procedure-hub\nfeature: phub-recommend\n'
  f"decision: \"{DEC['decision_ref']}\"\ngenerated_by: step4-apply.py\ndata: step4-techniques.json\n---\n")
P('# 실버 4단계 — 기법 원장\n')
P('## 셈\n')
P(f"- 원천: `{S['source']['path']}` · **지도(`source-map.json`)가 4단계로 정한 칸 {S['source']['cells']}개만** — 줄 {S['source']['lines']} · "
  f"**표현 {S['source']['values']}행**(새 표현 {S['source']['unique_values']} + extracted 중복 묶음 {S['source']['dup_groups']}행 · {S['source']['dup_lines']}줄)")
P(f"- **노드 {S['nodes']}** = " + ' · '.join(f"{k} 기법 {v}" for k, v in S['nodes_by_level'].items()))
P('- **표현 행선지(행)**: ' + ' · '.join(f"{k} {v}" for k, v in S['by_bucket'].items()))
P('  - 넘김 단계별(행): ' + ' · '.join(f"{k} {v}" for k, v in S['handoff_by_stage'].items()))
P('- **값 사전(값)**: ' + ' · '.join(f"{k} {v}" for k, v in S['dictionaries'].items()))
P(f"- 단위 시술 속성: 부위 × 층(safe_layers) **{S['safe_layer_sites']}부위**(층 값 {S['safe_layer_sites_with_layers']} · 근거만 {S['safe_layer_sites'] - S['safe_layer_sites_with_layers']}) · 대상 근육 **{S['target_muscles']}** · 주입 지표 {S['landmarks']}")
P(f"- 넘겨받은 것 **{S['handoffs']}줄** · technique_hint **{S['hints']}행** · 계열 기본 기법 **{S['family_defaults']}** · "
  f"초안 큰 기법 {sum(S['draft_techniques'].values())} = " + ' · '.join(f"{k} {v}" for k, v in S['draft_techniques'].items()))
P(f"- 원천 충돌 {S['conflicts']} · OQ 정리 {S['oq_closed']}")
P(f"- **open {S['open']}**" + (f" — {S['open_by_type']}" if S['open'] else ' — 결정 없는 표현 0 · 행선지 오류 0 · 넘겨받은 것 누락 0 · hint · 계열 · 초안 누락 0') +
  f" · 원천에 없는 결정 {S['stale_decisions']}\n")
P("> 결정 `step4-decisions.json` · 재현 `python3 step4-apply.py`. 원천 칸 값이 바뀌거나 새 값이 들어오면 「결정 없는 표현」으로, step2 · step3 이 4단계로 새로 넘기면 「넘겨받은 것 행선지 없음」으로 open 이 난다 — 결정 한 줄로 닫힌다.\n")
P('## 노드\n')
P('| id | 이름(상담 용어) | 상위 | 의학 용어(속성) | 계열 기본(보조) | 원천 표현(행) | 초안 합침 · 유지 | 근거 |\n|---|---|---|---|---|---|---|---|')
nm = {n['id']: n['name'] for n in out_nodes}
for n in out_nodes:
    fam = ' · '.join(n['family_default'] + [f'({a})' for a in n['family_also']])
    P(f"| {n['id']} | {n['name']} | {nm.get(n['parent'], '—')} | {n['medical_name']} | {fam or '—'} | {len(n['source_expressions'])} | "
      f"{' · '.join(n['draft_techniques']) or '—'} | {n['basis']} |")
P('\n## 값 사전 (속성 · 키 밖)\n')
for k in ('layer', 'pulse_mode', 'ablative', 'tool_form', 'peel_depth'):
    P(f"- **{k}** {len(DI[k])}: " + ' · '.join(DI[k]))
P(f"- **modes**(가능 방식 · 장비 속성) {len(DI['modes'])}: " + ' · '.join(f"{m['value']} → {m['node']}" for m in DI['modes']))
P('- 장비 속성 칸: ' + ' · '.join(DI['device_attrs']))
P('- 단위 시술 속성 칸: ' + ' · '.join(DI['unit_procedure_attrs']) + '\n')
P(f"### 대상 근육 {len(muscle_out)}\n")
P('| 키 | KMA 한글 | 원천 표기 | 부위(3단계 노드) | 원천 행 | 근거 속성 | 넘겨받음 | 근거 |\n|---|---|---|---|---|---|---|---|')
for m in muscle_out.values():
    P(f"| {m['key']}{' (묶음)' if m['group'] else ''} | {m['ko_kma']} | {m['source_label']} | {' · '.join(m['sites'])} | {len(m['from_rows'])} | {len(m['evidence'])} | "
      f"{' · '.join(m['handoffs']) or '—'} | {m['basis']} |")
P('\n## 부위 × 층 — safe_layers (주입 K01 · 키 밖)\n')
P('| 부위(3단계) | zone | 층 | 제약 · 지표(원문) | 근거 속성 |\n|---|---|---|---|---|')
for s in safe_layers.values():
    ev = ' · '.join(f"{e['layer']} ← {e['key'].split('.')[-1]}" for e in s['evidence']) or '—'
    P(f"| {s['site']}{' (← ' + s['from_split'] + ' 나눔)' if s['from_split'] else ''} | {s['zone'] or '—'} | {' · '.join(s['layers']) or '—'} | {s['constraint_text'] or '—'} | {ev} |")
P('\n## 주입 지표 — landmarks (넘겨받은 것)\n')
P('| 부위 | 지표(원문) | 넘김 |\n|---|---|---|')
for lm in landmarks:
    P(f"| {lm['site']} | {lm['text']} | {lm['handoff']} |")
P('\n## 표현 행선지\n')
P('| 파일 | 키 | 원문 | 수 | 판정 | 묶음 | 행선지 |\n|---|---|---|---|---|---|---|')
for r in expr_rows:
    t = r['text'].replace('|', '/').replace('\n', ' ')
    P(f"| {r['file'].replace('.json', '')} | `{r['key']}` | {t[:90]}{'…' if len(t) > 90 else ''} | {r['count']} | {r.get('verdict') or '—'} | {r['bucket']}"
      f"{' · ' + r['stage'] if r.get('stage') else ''} | {r['destination']} |")
P('\n## 넘겨받은 것\n')
P('| id | 출처 | 항목 | 행선지 |\n|---|---|---|---|')
for h in DEC['handoffs']:
    P(f"| {h['id']} | {h['from']} | {h['item']} | {h['destination']} |")
P('\n## technique_hint → 장비 속성\n')
P('| ledger_id | 이름 | 하위 계열 | hint(원천 그대로) | pulse_mode | 펄스 범위 | 가능 방식 | 박피 | 버림 |\n|---|---|---|---|---|---|---|---|---|')
for h in hints:
    P(f"| `{h['ledger_id']}` | {h['name']} | {h['sub_family']} | {' · '.join(h['hint'])} | {' · '.join(h['pulse_mode']) or '—'} | {h.get('pulse_scope') or ('주 하위 계열' if h['pulse_mode'] else '—')} | {' · '.join(h['modes']) or '—'} | "
      f"{' · '.join(a['value'] + '(' + a['basis'] + ')' for a in h['ablative']) or '—'} | {' · '.join(f'{k}: {v}' for k, v in h['dropped'].items()) or '—'} |")
P('\n매질별 펄스 방식: ' + ' · '.join(f"{k} = {'/'.join(v)}" for k, v in DEC['pulse_by_medium'].items()) + '\n')
P('## 계열 기본 기법\n')
P('| 계열 | 기본 | 보조 | 기본 층(원문) | 근거 |\n|---|---|---|---|---|')
for f in DEC['family_defaults']:
    P(f"| {f['family']} {f['family_name']} | {f['default']} {nm[f['default']]} | {' · '.join(a + ' ' + nm[a] for a in f['also']) or '—'} | {f['default_layer']} | {f['basis']} |")
P('\n단위 시술이 원천에서 다른 기법을 부르면(스킨보톡스 · 다한증 = 메조테라피, 성분 주사 = 허가 용법) 5단계에서 덮어쓴다.\n')
P('## 초안 큰 기법 → 새 자리\n')
P('| id | 초안 | 판정 | 새 자리 | 이유 |\n|---|---|---|---|---|')
for t in DEC['draft_techniques']:
    P(f"| {t['id']} | {t['name']} | {t['verdict']} | {(t['node'] + ' ' + nm[t['node']]) if t['node'] else '—'} | {t['reason']} |")
P('\n## 사용자 판단\n')
for u in DEC['user_decisions']:
    P(f"- **{u['id']}** {u['question']} → **{u['decision']}**")
P('\n## 원천 충돌\n')
P('| id | 무엇 | A | B | 해결 |\n|---|---|---|---|---|')
for c in DEC['conflicts']:
    P(f"| {c['id']} | {c['what']} | {c['a']} | {c['b']} | {c['resolve']} |")
P('\n## OQ 정리\n')
for o in DEC['oq_closed']:
    P(f"- **{o['oq']}** {o['q']} → {o['answer']}")
FX = W / 'step4-fixtures' / 'result.json'
if FX.exists() and not ARGS.source and Path(ARGS.decisions) == W / 'step4-decisions.json':
    fx = json.load(open(FX))
    P(f"\n## 고정 시험 — 「결정 빼면 open」 {fx['passed']}/{fx['total']} 통과\n")
    P('`python3 step4-fixture-test.py` — 결정 한 줄을 빼고 돌려 open 이 그 한 줄로 나오는지 본다.\n')
    P('| 사례 | 뺀 결정 | 기대 open | 실제 open | 결과 |\n|---|---|---|---|---|')
    for c in fx['cases']:
        P(f"| {c['id']} | {c['input']} | {' · '.join(c['expect'])} | {' · '.join(c['actual']) or '없음'} | {'PASS' if c['pass'] else 'FAIL'} |")
P('\n## 하지 않은 것\n')
for x in DEC['not_done']:
    P(f"- {x}")
P(f"\n## open {len(opened)}\n")
P('없음.' if not opened else '\n'.join(f"- {o}" for o in opened))
open(OUT / 'step4-techniques.md', 'w').write('\n'.join(L) + '\n')

# ───────── 12. 원천 · 문서 수정 목록(직접 고치지 않음) ─────────
F = DEC['source_fix']
L = ['---\ntype: fix-list\nid: step4-source-fix\ntitle: "4단계 — 문서 · 3단계 정본 · 원천 수정 후보"\ngenerated_by: step4-apply.py\n---\n',
     '# 4단계 — 문서 · 3단계 정본 · 원천 수정 후보\n',
     f"> 결정: {DEC['decision_ref']}. 이 목록만 낸다 — DEC-002.md · step1~3 산출 · 원천은 고치지 않았다.\n",
     f"## DEC 문구 {len(F['dec_text'])}\n", '| # | 대상 | 지금 | 고칠 것 | 이유 | 누가 |', '|---|---|---|---|---|---|']
L += [f"| {i} | {x['target']} | {x['now']} | {x['fix']} | {x['why']} | {x['who']} |" for i, x in enumerate(F['dec_text'], 1)]
L += [f"\n## 3단계 정본 {len(F['step3'])}\n", '| # | 대상 | 고칠 것 | 이유 | 누가 |', '|---|---|---|---|---|']
L += [f"| {i} | {x['target']} | {x['fix']} | {x['why']} | {x['who']} |" for i, x in enumerate(F['step3'], 1)]
L += [f"\n## 원천 수정 후보 {len(F['source_candidates'])}\n", '| # | 파일 | 키 | 지금 | 고칠 것 | 충돌 |', '|---|---|---|---|---|---|']
L += [f"| {i} | `{x['file']}` | {x['path']} | {x['from']} | {x['to']} | {x['why']} |" for i, x in enumerate(F['source_candidates'], 1)]
open(OUT / 'step4-source-fix.md', 'w').write('\n'.join(L) + '\n')
print(json.dumps({k: summary[k] for k in ('nodes', 'by_bucket', 'handoff_by_stage', 'open', 'open_by_type', 'stale_decisions')}, ensure_ascii=False))
