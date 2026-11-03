"""Read-only input audit. Writes only siblings of this script; never imports generators."""
import collections
import hashlib
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
WORK = OUT.parent
ROOT = WORK.parents[2]
RAW = Path('/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26')
BACKEND = RAW.parent / 'phub-recommend/backend'
SKILLS = ROOT / 'reference/2026-10-27-skills-procedure-hub'
NAMES = ['products', 'families', 'sites', 'techniques', 'units', 'packages', 'concerns', 'relations', 'explanations']
FILES = [WORK / f'step{i}-{n}.json' for i, n in enumerate(NAMES, 1)]
S = {i: json.loads(p.read_text()) for i, p in enumerate(FILES, 1)}
R = {p.stem: json.loads(p.read_text()) for p in RAW.glob('*.json')}


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def walk(obj, path='$'):
    yield path, obj
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, path + '.' + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f'{path}[{i}]')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def raw_get(file, path):
    # Silver source.path starts with filename, not JSON root.
    tokens = re.findall(r'([^\.\[\]]+)|\[(\d+)\]', path)
    keys = [int(b) if b else a for a, b in tokens]
    if keys and keys[0] == file:
        keys.pop(0)
    obj = R[file]
    for k in keys:
        obj = obj[k]
    return obj


markers = {
    'undetermined': r'미정|미상|못 정|안 정함|미특정|미확인|확인 불가|불명|unknown|undecided',
    'ambiguous': r'ambiguous|모호|후보 여럿',
    'all_candidates': r'후보 전부|inherited_candidates',
    'candidate': r'후보|candidates',
    'family_only': r'계열만',
    'conditional': r'조건부|conditional|by_sub_condition',
    'site_absent': r'부위 없음|부위 못|앵커 부위 없음|concern_without_site|no_unit_at_site',
    'uninterpreted': r'해석 안|못 풂|못 푼|unresolved',
    'origin_question': r'원천 질문|원장님 문의|의료진 확인|staff_check|pending_director',
    'weak_evidence': r'근거 약|근거 없음|출처 없음|근거 제한|확인 필요',
    'conflict_conservative': r'보수|충돌|conflict|conservative|alternatives',
}
compiled = {k: re.compile(v, re.I) for k, v in markers.items()}
hits, field_stats, collections_stats = [], [], []
for i, obj in S.items():
    groups = collections.defaultdict(list)
    for path, value in walk(obj):
        pattern = re.sub(r'\[\d+\]', '[]', path)
        if not isinstance(value, (dict, list)):
            groups[pattern].append((path, value))
            cats = [k for k, rx in compiled.items() if isinstance(value, str) and rx.search(value)]
            if cats:
                hits.append({'stage': i, 'path': path, 'field': pattern, 'value': value, 'markers': cats})
        if isinstance(value, list) and value and all(isinstance(v, dict) for v in value):
            keys = sorted(set().union(*(v.keys() for v in value)))
            fs = {}
            for k in keys:
                present = [v[k] for v in value if k in v]
                fs[k] = {'present': len(present), 'missing': len(value)-len(present),
                         'null': sum(v is None for v in present), 'empty_list': sum(v == [] for v in present),
                         'false': sum(v is False for v in present)}
            collections_stats.append({'stage': i, 'path': path, 'pattern': pattern, 'denominator': len(value), 'fields': fs})
    for path, vals in groups.items():
        counts = {k: sum(isinstance(v, str) and bool(rx.search(v)) for _, v in vals) for k, rx in compiled.items()}
        field_stats.append({'stage': i, 'field': path, 'observations': len(vals), 'null': sum(v is None for _, v in vals),
                            'marker_counts': {k: v for k, v in counts.items() if v}})
dump('uncertainty-hits.json', {'method': 'exhaustive scalar lexical census, overlapping labels; not defect counts; negations and historical prose retained', 'patterns': markers, 'hits': hits})
dump('field-census.json', {'scalar_fields': field_stats, 'record_arrays': collections_stats})

# Direct original text equality. No regenerated Silver used as truth.
checks = []
def check(group, source, target, expected, actual):
    checks.append({'group': group, 'source': source, 'silver': target, 'equal': expected == actual,
                   **({'expected': expected, 'actual': actual} if expected != actual else {})})

items = {}
products = {}
for i, m in enumerate(R['taxonomy']['modality']):
    for j, sub in enumerate(m.get('subcategories', [])):
        for k, it in enumerate(sub.get('items', [])):
            items[it['id']] = (it, f'$.modality[{i}].subcategories[{j}].items[{k}]')
    for j, pr in enumerate(m.get('products', [])):
        products[pr['id']] = (pr, f'$.modality[{i}].products[{j}]')
for i, row in enumerate(S[5]['ledger']):
    original, path = items[row['id']]
    for k in ['name', 'detail']:
        check('step5.ledger.'+k, 'taxonomy.json:'+path+'.'+k, f'step5-units.json:$.ledger[{i}].{k}', original.get(k), row.get(k))
for key, source in [('extracted', items), ('taxonomy_products', products)]:
    for i, row in enumerate(S[5][key]):
        original, path = source[row['id']]
        source_text = {}
        ex = original.get('extracted') or {}
        if 'aftercare' in ex:
            source_text['aftercare'] = ex['aftercare']
        for k, v in (ex.get('safety') or {}).items():
            source_text['safety.'+k] = v
        check('step5.'+key+'.source_text', 'taxonomy.json:'+path+'.extracted.{safety,aftercare}', f'step5-units.json:$.{key}[{i}].source_text', source_text, row.get('source_text', {}))

for i, row in enumerate(S[9]['records']):
    src = row['source']
    try:
        val = str(raw_get(src['file'], src['path']))
        check('step9.records.text', src['file']+'.json:'+src['path'], f'step9-explanations.json:$.records[{i}].text', val, row['text'])
    except (KeyError, IndexError, TypeError) as exc:
        checks.append({'group': 'step9.records.text', 'silver': f'$.records[{i}]', 'equal': False, 'error': repr(exc)})

comparison = {v['id']: (i, v) for i, v in enumerate(R['procedure-comparison']['comparisons'])}
for i, c in enumerate(S[7]['combos']):
    if c['source'] != 'procedure-comparison':
        continue
    ri, rc = comparison[c['source_id']]
    for k in ['title', 'subtitle']:
        check('step7.comparison.anchor', f'procedure-comparison.json:$.comparisons[{ri}].{k}', f'step7-concerns.json:$.combos[{i}].anchor.{k}', rc[k], c['anchor'][k])
    for j, m in enumerate(c['members']):
        src = rc['procedures'][j]
        check('step7.comparison.member.name', f'procedure-comparison.json:$.comparisons[{ri}].procedures[{j}].name', f'step7-concerns.json:$.combos[{i}].members[{j}].text', src['name'], m['text'])
        for k, v in m['attrs_text'].items():
            check('step7.comparison.member.attrs', f'procedure-comparison.json:$.comparisons[{ri}].procedures[{j}].{k}', f'step7-concerns.json:$.combos[{i}].members[{j}].attrs_text.{k}', src[k], v)

raw_cb = []
for pi, p in enumerate(R['problem-packages']['problems']):
    for ci, c in enumerate(p['complaints']):
        for bi, cb in enumerate(c.get('combos') or []):
            raw_cb.append((p['problem_id'], c['cc'], cb, f'$.problems[{pi}].complaints[{ci}].combos[{bi}]'))
silver_cb = [(i, n) for i, n in enumerate(S[7]['step8_notes']) if n['source'] == 'problem-packages.complaints[].combos']
assert len(raw_cb) == len(silver_cb)
for (pid, cc, cb, path), (i, row) in zip(raw_cb, silver_cb):
    check('step7.cc_note.text', 'problem-packages.json:'+path, f'step7-concerns.json:$.step8_notes[{i}].text', f"{cb['name']} — {cb.get('reason')} / {cb.get('evidence')}", row['text'])
    check('step7.cc_note.where', 'problem-packages.json:'+path, f'step7-concerns.json:$.step8_notes[{i}].where', f'{pid} {cc}', row['where'])

# Every K8 not_condition and condition category-specific row original text.
for key in ['claims', 'not_condition']:
    for i, c in enumerate(S[8]['conditions'][key]):
        if c['source'] == 'pre-procedure-checklist.category_specific':
            family, idx = c['source_index'].split('#')
            fi, frow = next((j, v) for j, v in enumerate(R['pre-procedure-checklist']['category_specific']) if v['id'] == family)
            original = frow['checks'][int(idx)]
            text = original['label']
            check('step8.category_specific.text', f'pre-procedure-checklist.json:$.category_specific[{fi}].checks[{idx}].label', f'step8-relations.json:$.conditions.{key}[{i}].text', text, c['text'])

def source8(c):
    src, idx = c['source'], c['source_index']
    file = src.split('.')[0]
    obj = R[file]
    if src == 'contraindications.rules':
        r = obj['rules'][idx]
        return file, f'$.rules[{idx}]', f"{r['from']}↔{r['to']} {r['interval']}", {'reason': r['note']}
    if src == 'synergy.links':
        r = obj['links'][idx]
        return file, f'$.links[{idx}]', f"{r['from']} {r['type']} {r['to']} · {r.get('timing') or ''}", {'reason': r.get('reason'), 'target': r.get('target')}
    if src.startswith('treatment-sequence.'):
        coll = src.split('.')[1]
        r = obj[coll][idx]
        path = f'$.{coll}[{idx}]'
        if coll == 'incompatible_same_day':
            return file, path, ' ↔ '.join(r['pair']), {'reason' if c['id'].startswith('R8') else 'detail': r['reason']}
        if coll == 'minimum_intervals':
            if c['id'].startswith('K8'):
                return file, path, ' ↔ '.join([r['from'], r['to']]), {'detail': r['reason']}
            return file, path, f"{r['from']} → {r['to']}", {'reason': r['reason'], 'min_days': r.get('min_days'), 'min_months': r.get('min_months')}
        return file, path, r['note'] if coll == 'common_combos' else r, {}
    if src == 'treatment-optimization.combination_rules':
        r = obj['combination_rules'][idx]
        # Depending on parsed clause, generator uses the title or detail verbatim.
        return file, f'$.combination_rules[{idx}]', r['rule'] if c['text'] == r['rule'] else r['detail'], {'evidence_text': r['evidence']}
    if src.startswith('treatment-optimization.by_concern.'):
        ix = [int(x) for x in str(idx).split('.')]
        r = obj['by_concern'][ix[0]]['severity_levels'][ix[1]]
        path = f'$.by_concern[{ix[0]}].severity_levels[{ix[1]}]'
        if src.endswith('.sequence'):
            return file, path+'.sequence', r['sequence'], {}
        return file, path+f'.contraindicated_combos[{ix[2]}]', r['contraindicated_combos'][ix[2]], {}
    if src == 'treatment-optimization.by_age_group.avoid':
        age, ix = idx.split('#')
        ai, r = next((j, r) for j, r in enumerate(obj['by_age_group']) if r['age'] == age)
        return file, f'$.by_age_group[{ai}].avoid[{ix}]', r['avoid'][int(ix)], {}
    if src == 'problem-combos.riskBenefit':
        pi, bi, r = next((pi, bi, r) for pi, p in enumerate(obj['combos']) for bi, r in enumerate(p['packages']) if r['id'] == idx)
        return file, f'$.combos[{pi}].packages[{bi}].riskBenefit', r['riskBenefit'], {}
    if src.startswith('problem-packages.'):
        key, ix = idx.rsplit('#', 1)
        pid, cc = key.split(':', 1)
        coll = 'combos' if src.endswith('.combos') else 'alternatives'
        matches = [(pi, ci, r) for pi, p in enumerate(obj['problems']) if p['problem_id'] == pid for ci, r in enumerate(p['complaints']) if r['cc'] == cc and int(ix) < len(r.get(coll) or [])]
        # Legacy locator is non-unique for repeated CC labels. Content selection is
        # audit-only; ambiguity is explicitly recorded below, not repaired in source.
        good = [(pi, ci, r) for pi, ci, r in matches if (r[coll][int(ix)]['name'] if coll == 'combos' else r[coll][int(ix)]) == c['text']]
        pi, ci, r = (good or matches)[0]
        val = r[coll][int(ix)]
        return file, f'$.problems[{pi}].complaints[{ci}].{coll}[{ix}]', val['name'] if coll == 'combos' else val, {'reason': val['reason'], 'evidence_text': val.get('evidence')} if coll == 'combos' else {}
    if src.startswith('pre-procedure-checklist.'):
        if src.endswith('.universal_checks'):
            j, r = next((j, r) for j, r in enumerate(obj['universal_checks']) if r['id'] == idx)
            return file, f'$.universal_checks[{j}]', r['label'], {'detail': r['description'], 'grade_original': r['type']}
        fam, ix = idx.split('#')
        j, r = next((j, r) for j, r in enumerate(obj['category_specific']) if r['id'] == fam)
        r = r['checks'][int(ix)]
        return file, f'$.category_specific[{j}].checks[{ix}]', r['label'], {'grade_original': r['type']}
    if src == 'consent-checklist.contraindications':
        fam, ix = idx.split('#')
        j, r = next((j, r) for j, r in enumerate(obj['categories']) if r['id'] == fam)
        return file, f'$.categories[{j}].contraindications[{ix}]', r['contraindications'][int(ix)], {}
    if src.startswith('taxonomy.'):
        rid, ix = idx.split('#')
        ix = int(ix)
        if '.modality[].extracted.' in src:
            mi, r = next((j, r) for j, r in enumerate(obj['modality']) if r['id'] == rid)
            grade = src.rsplit('.', 1)[-1]
            return file, f'$.modality[{mi}].extracted.contraindications.{grade}[{ix}]', r['extracted']['contraindications'][grade][ix], {}
        r, p = (products if '.products[]' in src else items)[rid]
        return file, p+f'.extracted.safety.contraindications[{ix}]', r['extracted']['safety']['contraindications'][ix], {}
    raise ValueError(src)

source8_rows = []
for coll, rows in [('claims', S[8]['claims']), ('conditions.claims', S[8]['conditions']['claims']), ('conditions.not_condition', S[8]['conditions']['not_condition'])]:
    for i, c in enumerate(rows):
        file, path, text, extra = source8(c)
        check('step8.'+coll+'.original_text', file+'.json:'+path, f'step8-relations.json:$.{coll}[{i}].text', text, c['text'])
        for k, v in extra.items():
            check('step8.'+coll+'.original_fields', file+'.json:'+path, f'step8-relations.json:$.{coll}[{i}].{k}', v, c.get(k))
        source8_rows.append({'id': c['id'], 'silver_path': f'$.{coll}[{i}]', 'source_file': str(RAW/(file+'.json')), 'source_path': path})
        if c['source'].startswith('problem-packages.'):
            key, ix = c['source_index'].rsplit('#', 1)
            pid, cc = key.split(':', 1)
            raw_coll = 'combos' if c['source'].endswith('.combos') else 'alternatives'
            matches = [f'$.problems[{pi}].complaints[{ci}].{raw_coll}[{ix}]' for pi, p in enumerate(R['problem-packages']['problems']) if p['problem_id'] == pid for ci, r in enumerate(p['complaints']) if r['cc'] == cc and int(ix)<len(r.get(raw_coll) or [])]
            if len(matches) > 1:
                source8_rows[-1]['legacy_locator_candidates'] = matches
                source8_rows[-1]['audit_content_match_not_canonical_identity'] = True
dump('step8-origin-locators.json', source8_rows)

# Report all key collisions before normalization, separately from benign renames.
normalization = json.loads((WORK/'step5-decisions.json').read_text())['extracted_rule']['key_normalize']
collisions = []
for coll, rows, source in [('extracted', S[5]['extracted'], items), ('taxonomy_products', S[5]['taxonomy_products'], products)]:
    for i, row in enumerate(rows):
        orig, path = source[row['id']]
        buckets = collections.defaultdict(list)
        for p, v in walk(orig.get('extracted') or {}):
            if isinstance(v, dict) or re.search(r'\[\d+\]', p):
                continue
            p = p.removeprefix('$.')
            if p == '$':
                continue
            buckets[normalization.get(p, p)].append({'source_field': p, 'value': v})
        for normalized, origins in buckets.items():
            if len(origins) > 1:
                collisions.append({'record_id': row['id'], 'raw_file': str(RAW/'taxonomy.json'), 'raw_path': path+'.extracted', 'silver_path': f'$.{coll}[{i}].source_text', 'normalized_key': normalized, 'sources': origins, 'current': (row.get('source_text') or {}).get(normalized), 'lost_original_leaves': [v for o in origins for v in (o['value'] if isinstance(o['value'],list) else [o['value']]) if v not in ((row.get('source_text') or {}).get(normalized) or [])]})
dump('normalization-collisions.json', collisions)

# Repeated CC names: preserve distinct original row/group/detail and compare
# correspondence's own correct item mapping against emitted edge anchor.
duplicate_cc = []
cc_groups = collections.defaultdict(list)
for pi, p in enumerate(R['problem-packages']['problems']):
    for ci, c in enumerate(p['complaints']):
        cc_groups[(p['problem_id'], c['cc'])].append((pi, ci, c))
for (pid, cc), rows in cc_groups.items():
    if len(rows) < 2:
        continue
    for pi, ci, c in rows:
        correspondence = [x for x in S[7]['correspondence'] if x['source'] == 'problem-packages' and x['field'] == 'complaints[].cc' and x['text'] == f"{cc} [{c['cc_detail']}]" and x.get('cc_group') == c['cc_group']]
        nodes = [x for x in S[7]['concerns']['items'] if correspondence and x['id'] in correspondence[0]['target']]
        duplicate_cc.append({'raw_file': str(RAW/'problem-packages.json'), 'raw_path': f'$.problems[{pi}].complaints[{ci}]', 'original': c,
                             'legacy_key': f'{pid}:{cc}', 'correspondence_targets': correspondence[0]['target'] if correspondence else [],
                             'correspondence_item_parent': [x['subcategory'] for x in nodes],
                             'emitted_claims': [{'id': x['id'], 'condition': x.get('condition'), 'source_index': x['source_index']} for x in S[8]['claims'] if x['source'].startswith('problem-packages.') and str(x['source_index']).startswith(f'{pid}:{cc}#')]})
dump('duplicate-cc-evidence.json', duplicate_cc)

# Decision data has its own exhaustive scalar census; separate historical policy prose.
decision_hits = []
for p in sorted(WORK.glob('step*-decisions.json')):
    for path, value in walk(json.loads(p.read_text())):
        cats = [k for k, rx in compiled.items() if isinstance(value, str) and rx.search(value)]
        if cats:
            decision_hits.append({'file': p.name, 'path': path, 'field': re.sub(r'\[\d+\]', '[]', path), 'value': value, 'markers': cats})
dump('decision-uncertainty-hits.json', {'method': 'exhaustive lexical scan; historical prose and rules are not pending issue counts', 'hits': decision_hits})

def counts(rows, field):
    return dict(collections.Counter(str(r.get(field)) for r in rows))

stage_metrics = {str(i): {'denominators': {k: len(v) for k, v in s.items() if isinstance(v, list)}, 'existing_summary': s['summary']} for i, s in S.items()}
stage_metrics['1']['recount'] = {'active': sum(r['active'] for r in S[1]['items']), 'open_entries': len(S[1]['open']), 'rows_with_open': sum(bool(r.get('open')) for r in S[1]['items']), 'active_license_status': counts([r['4_license'] for r in S[1]['items'] if r['active']], 'status')}
stage_metrics['2']['recount'] = {'verdict': counts(S[2]['product_family'], 'verdict'), 'family_null': sum(r['family'] is None for r in S[2]['product_family']), 'weak': sum(r.get('evidence_level') == '약' for r in S[2]['product_family']), 'conflict_nonempty': sum(bool(r.get('conflict')) for r in S[2]['product_family'])}
stage_metrics['3']['recount'] = {'weak_strings': sum(r.get('weak') is True for r in S[3]['strings']), 'anatomical_level': counts([r['anatomical_name'] for r in S[3]['nodes']], 'level'), 'doctor_questions': len(S[3]['doctor_questions'])}
stage_metrics['4']['recount'] = {'expression_verdict': counts(S[4]['expressions'], 'verdict'), 'conflicts': len(S[4]['conflicts']), 'not_done': len(S[4]['not_done'])}
stage_metrics['5']['recount'] = {'ledger_role': counts(S[5]['ledger'], 'role'), 'market_role': counts(S[5]['market'], 'role'), 'menu_role': counts(S[5]['problem_P1'], 'role'), 'extracted_attach': counts(S[5]['extracted'], 'attach'), 'inheritance_pairs': sum(len(r['inherited_candidates']) for r in S[5]['product_links']), 'stored_pairs': sum(len(r['stored_units']) for r in S[5]['product_links']), 'link_status': counts(S[5]['product_links'], 'link'), 'raw_normalization_collisions': len(collisions)}
stage_metrics['6']['recount'] = {'slots': len(S[6]['slots']), 'contains_weak': sum(r.get('evidence_level') == '약' for r in S[6]['contains']), 'questions': len(S[6]['origin_questions'])}
stage_metrics['7']['recount'] = {'edge_flags': counts(S[7]['edges'], 'resolve_flag'), 'family_only': sum(r['target_kind']=='계열만' for r in S[7]['edges']), 'edge_target_kind': counts(S[7]['edges'], 'target_kind'), 'correspondence_gate_status': counts(S[7]['correspondence'], 'gate_status'), 'combo_member_flags': {k: counts([m for c in S[7]['combos'] for m in c.get(k,[])], 'flag') for k in ['components','members','upgrade']}, 'source_combo_arity': dict(collections.Counter(len(cb['combo']) for _,_,cb,_ in raw_cb)), 'note_rows_without_exact_locator': sum('source_index' not in r and 'source_path' not in r for r in S[7]['step8_notes'])}
stage_metrics['8']['recount'] = {'claims_gate_status': counts(S[8]['claims'], 'gate_status'), 'claims_review_status': counts(S[8]['claims'], 'review_status'), 'claims_resolved_true': sum(r.get('resolved') is True for r in S[8]['claims']), 'claim_endpoint_levels': dict(collections.Counter(v['level'] for c in S[8]['claims'] for _,v in walk(c) if isinstance(v,dict) and 'level' in v and 'via' in v)), 'edge_review_status': counts(S[8]['edges'], 'review_status'), 'edge_resolved_status': counts([r['resolved'] for r in S[8]['edges']], 'status'), 'condition_resolved_status': counts(S[8]['conditions']['resolved'], 'status'), 'source_locator_ambiguous_rows': sum('legacy_locator_candidates' in r for r in source8_rows)}
stage_metrics['9']['recount'] = {'record_status': counts(S[9]['records'], 'status'), 'attach_status': counts([r['attach'] for r in S[9]['records']], 'status'), 'node_slot_class': counts(S[9]['node_slots'], 'class'), 'alternatives': sum(len(r.get('alternatives',[])) for r in S[9]['node_slots']), 'resolved_by': counts([r for r in S[9]['node_slots'] if 'resolved_by' in r], 'resolved_by')}
dump('stage-metrics.json', stage_metrics)

identity_sets = {
    'taxonomy.modality.items.name': [(x['name'], {'id': x['id'], 'path': p}) for x,p in items.values()],
    'taxonomy.modality.products.name': [(x['name'], {'id': x['id'], 'path': p}) for x,p in products.values()],
    'market-pricing.items.name': [(x['name'], {'category': c['id'], 'path': f'$.categories[{ci}].items[{xi}]'}) for ci,c in enumerate(R['market-pricing']['categories']) for xi,x in enumerate(c['items'])],
    'problem-packages.PID+CC': [(f"{p['problem_id']}:{c['cc']}", {'path': f'$.problems[{pi}].complaints[{ci}]', 'detail': c['cc_detail'], 'group': c['cc_group']}) for pi,p in enumerate(R['problem-packages']['problems']) for ci,c in enumerate(p['complaints'])],
    'step1.active.display_name': [(x['2_names']['display_name'], {'id': x['ledger_id']}) for x in S[1]['items'] if x['active']],
    'step3.nodes.name': [(x['name'], {'id': x['id']}) for x in S[3]['nodes']],
    'step4.nodes.name': [(x['name'], {'id': x['id']}) for x in S[4]['nodes']],
    'step5.units.name': [(x['name'], {'id': x['id']}) for x in S[5]['units']],
    'step9.CC2.text': [(x['text'], {'targets': x['target'], 'group': x.get('cc_group')}) for x in S[7]['correspondence'] if x['field']=='complaints[].cc'],
}
identity_report = {}
for name, rows in identity_sets.items():
    grouped = collections.defaultdict(list)
    for key, row in rows:
        grouped[key].append(row)
    duplicate = {key: vals for key,vals in grouped.items() if len(vals)>1}
    identity_report[name] = {'denominator': len(rows), 'distinct_keys': len(grouped), 'duplicate_keys': len(duplicate), 'affected_rows': sum(len(v) for v in duplicate.values()), 'duplicates': duplicate}
identity_report['normalization_call_sites'] = ['step5-apply.py:flat at 613-621 (same dictionary overwrite used for every non-dict leaf)', 'step5-apply.py:safety_text at 628-629 -> extracted/source_text and taxonomy_products/source_text', 'step5-apply.py:638,662,664 -> keys inventory', 'step5-apply.py:674-699 -> side_effect_override values copied from already-normalized source_text', 'Gold build.py:842-890 -> source_text and override facts consume losses; no generator executed']
dump('identity-collisions.json', identity_report)

primary_sets = {
    'raw.taxonomy.modality.items.id': [x['id'] for m in R['taxonomy']['modality'] for sub in m.get('subcategories',[]) for x in sub.get('items',[])],
    'raw.taxonomy.modality.products.id': [x['id'] for m in R['taxonomy']['modality'] for x in m.get('products',[])],
    'step1.items.ledger_id': [x['ledger_id'] for x in S[1]['items']],
    'step2.families.id': [x['id'] for x in S[2]['families']],
    'step2.product_family.ledger_id': [x['ledger_id'] for x in S[2]['product_family']],
    'step3.nodes.id': [x['id'] for x in S[3]['nodes']],
    'step4.nodes.id': [x['id'] for x in S[4]['nodes']],
    'step5.units.id': [x['id'] for x in S[5]['units']],
    'step6.packages.id': [x['id'] for x in S[6]['packages']],
    'step7.combos.id': [x['id'] for x in S[7]['combos']],
    'step8.claims.id': [x['id'] for x in S[8]['claims']],
    'step8.conditions.all_claims.id': [x['id'] for k in ['claims','not_condition'] for x in S[8]['conditions'][k]],
    'step8.edges.id': [x['id'] for x in S[8]['edges']],
    'step9.records.id': [x['id'] for x in S[9]['records']],
}
primary_report = {k:{'denominator':len(v),'distinct_ids':len(set(v)),'duplicates':{a:n for a,n in collections.Counter(v).items() if n>1}} for k,v in primary_sets.items()}
manifest_entries = [{'file':p.name,'sha256':sha(p)} for p in sorted(RAW.glob('*.json'))]
digest = lambda obj: hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
snapshot_id = 'snap:'+digest(manifest_entries)
occurrences = []
for ci in [4,8,10,11]:
    pointer = f'/problems/8/complaints/{ci}'
    inputs = {'snapshot':snapshot_id,'file':'problem-packages.json','pointer':pointer}
    c = R['problem-packages']['problems'][8]['complaints'][ci]
    occurrences.append({'proposed_source_record_id':'sr:'+digest(inputs),'inputs':inputs,'legacy_alias':'P9:'+c['cc'],'raw_group':c['cc_group'],'raw_detail':c['cc_detail']})
dump('id-design.json', {'status':'design_examples_only_no_IDs_written_to_sources','primary_id_uniqueness':primary_report,'snapshot_algorithm':'sha256 UTF8 canonical JSON sorted [{file,sha256}] for full raw snapshot, sort_keys=True, separators=(comma,colon), ensure_ascii=False','example_snapshot_id':snapshot_id,'source_record_algorithm':'sha256 canonical JSON {snapshot,file,pointer}; immutable occurrence, not cross-version continuity','actual_collision_examples':occurrences,'legacy_alias_policy':'alias -> set of target IDs; never first-match; mappings require snapshot/scope/decision validation','identity_is_not_semantic_approval':True})

probe_sets={
    'step1.items':S[1]['items'], 'step2.product_family':S[2]['product_family'],
    'step3.strings':S[3]['strings'], 'step4.expressions':S[4]['expressions'],
    'step5.ledger':S[5]['ledger'], 'step5.units':S[5]['units'], 'step5.product_links':S[5]['product_links'],
    'step5.extracted':S[5]['extracted'],'step5.taxonomy_products':S[5]['taxonomy_products'],
    'step6.contains':S[6]['contains'],'step6.slots':S[6]['slots'],
    'step7.correspondence':S[7]['correspondence'],'step7.edges':S[7]['edges'],'step7.step8_notes':S[7]['step8_notes'],
    'step7.combo_members':[m for c in S[7]['combos'] for k in ['components','members','upgrade'] for m in c.get(k,[])],
    'step8.claims':S[8]['claims'],'step8.condition_claims':S[8]['conditions']['claims']+S[8]['conditions']['not_condition'],
    'step9.records':S[9]['records'],
}
probe_fields=['source','source_id','source_ids','source_index','file','key','source.file','source.path','source.record','source.sha256','source_refs','source_record_id','snapshot_ref','version','scope','scope_conditional','condition','conditions','anchor_sites','target','target_level','role','flag','flags','resolve_flag','status','attach.status','attach.flags','rule','decided_by','basis','review_status']
probe=[]
for label,rows in probe_sets.items():
    fields={}
    for path in probe_fields:
        vals=[]
        missing=0
        for row in rows:
            val=row
            for part in path.split('.'):
                if not isinstance(val,dict) or part not in val:
                    missing+=1
                    break
                val=val[part]
            else:
                vals.append(val)
        fields[path]={'present':len(vals),'missing':missing,'null':sum(v is None for v in vals),'empty_list':sum(v==[] for v in vals),'false':sum(v is False for v in vals)}
    probe.append({'collection':label,'denominator':len(rows),'fields':fields})
dump('provenance-coverage.json',{'method':'literal existing-field presence probes, not schema errors; indirect lineage can exist in other fields or file-level metadata; exact field spelling matters','collections':probe})

dump('direct-comparisons.json', {'method': 'original snapshot vs stored Silver fields; text equality, not clinical validation or complete semantic review', 'summary': dict(collections.Counter(c['group'] for c in checks)), 'failed': sum(not c['equal'] for c in checks), 'checks': checks})

# Stable file-level lineage and integrity.
paths = set(RAW.glob('*.json')) | set(WORK.glob('step*.json')) | set(WORK.glob('step*-apply.py'))
paths |= {WORK / 'semantic.json', WORK / 'semantic-build.py', WORK / 'source-map.json'}
paths |= set(SKILLS.glob('*/SKILL.md')) | set(SKILLS.glob('*/references/*.md')) | {SKILLS/'README.md'}
paths |= {BACKEND/'raw-manifest.json', BACKEND/'app/modules/raw/config.py', BACKEND/'app/modules/gold/inputs.py', BACKEND/'app/modules/gold/build.py', BACKEND/'app/modules/gold/tools.py', BACKEND/'app/modules/gold/facts.py', BACKEND/'scripts/gold_ingest.py', BACKEND/'scripts/gold_build.py'}
manifest = json.loads((BACKEND/'raw-manifest.json').read_text())
guards = []
for f in manifest['files']:
    p = RAW/f['name']
    guards.append({'file': str(p), 'bytes_match': p.stat().st_size == f['bytes'], 'sha16_match': sha(p)[:16] == f['sha16']})
sem = json.loads((WORK/'semantic.json').read_text())
sem_guards = [{'file': k, 'expected': v['sha256'], 'actual': sha(WORK/k)[:16], 'equal': v['sha256'] == sha(WORK/k)[:16]} for k, v in sem['inputs'].items()]
denom = {i: {k: len(v) for k, v in s.items() if isinstance(v, list)} for i, s in S.items()}
inv = {'scope': '2026-11-03 current on-disk artifacts; migration authority and active DB build not verified',
       'roots': {'silver': str(WORK), 'raw': str(RAW), 'skills': str(SKILLS), 'backend': str(BACKEND)},
       'authority': 'Coordinator explicitly approved these existing files as audit baseline; separate migrated canonical location unconfirmed',
       'lineage': ['raw 21 snapshot -> step decisions/research + step apply -> step1..9 Silver', 'step1..9 + step3 lexicon + step7/8 decisions -> semantic-build -> semantic.json', 'gold_ingest --from-dir explicit 13 files -> DB source snapshots -> gold_build latest snapshots -> gold facts/edges; no DB operations in audit'],
       'raw_manifest_checks': guards, 'semantic_input_checks': sem_guards,
       'stage_denominators': denom,
       'direct_comparison_groups': dict(collections.Counter(c['group'] for c in checks)),
       'files': [{'file': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p), 'role': 'raw' if p.parent == RAW else 'skill' if SKILLS in p.parents else 'consumer' if BACKEND in p.parents else 'silver_or_decision_or_generator'} for p in sorted(paths) if p.exists()]}
dump('inventory.json', inv)
print(json.dumps({'checks': len(checks), 'failed': sum(not c['equal'] for c in checks), 'marker_hits': len(hits), 'scalar_fields': len(field_stats), 'record_arrays': len(collections_stats), 'files': len(inv['files']), 'raw_manifest_pass': sum(g['bytes_match'] and g['sha16_match'] for g in guards), 'semantic_hash_pass': sum(g['equal'] for g in sem_guards)}, ensure_ascii=False))
