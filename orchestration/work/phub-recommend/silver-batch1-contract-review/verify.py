"""Read-only independent contract review; writes only adjacent results/."""
from pathlib import Path
import collections
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
RESULTS = HERE / 'results'
CACHE = {}

def read(path):
    path = Path(path)
    if path not in CACHE:
        CACHE[path] = json.loads(path.read_text())
    return CACHE[path]

def ptr(path, pointer):
    value = read(path)
    assert pointer == '' or pointer.startswith('/'), pointer
    for part in pointer.split('/')[1:]:
        key = part.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def leaves(value):
    if isinstance(value, dict):
        return sum(map(leaves, value.values()))
    if isinstance(value, list):
        return sum(map(leaves, value))
    return 1

def dump(name, value):
    (RESULTS / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

contract = read(BASE / 'silver-data-contract-batch1/field-contract.json')
coverage = read(BASE / 'silver-pilot-closeout-review/coverage.json')
manifest = read(BASE / 'silver-data-contract-batch1/results/input-manifest.json')
errors = []
manifest_rows = []
for row in manifest:
    actual = sha(row['file'])
    manifest_rows.append({**row, 'actual_sha256': actual,
                          'actual_bytes': Path(row['file']).stat().st_size,
                          'matches': actual == row['sha256'] and Path(row['file']).stat().st_size == row['bytes']})
assert len({(r['domain'], r['logical_file_key']) for r in manifest}) == len(manifest)
rawfiles = {Path(r['file']) for r in manifest if r['domain'] == 'raw21'}
rawroot = next(iter(rawfiles)).parent
raw_actual = {p for p in rawroot.rglob('*') if p.is_file() and not p.name.startswith('.')}
dump('manifest.json', {'files': manifest_rows, 'domains': dict(collections.Counter(r['domain'] for r in manifest)),
     'raw_manifest_count': len(rawfiles), 'raw_actual_count': len(raw_actual),
     'raw_membership_equal': rawfiles == raw_actual,
     'generated_source_kinds': dict(collections.Counter(r.get('source_kind') for r in manifest if r['domain'] == 'generated-silver'))})

baseline = {r['proposed']: r for r in coverage['fields']}
baseline_checks = collections.Counter()
for row in baseline.values():
    for group in ['origin_current_paths', 'evidence']:
        for loc in row.get(group, []):
            value = ptr(loc['file'], loc['pointer'])
            if 'value_type' in loc:
                assert type(value).__name__ == loc['value_type']
            baseline_checks[group] += 1
assert len(baseline) == 247
assert len(contract['fields']) == 84 and len(contract['excluded_fields']) == 163
assert {r['proposed'] for r in contract['fields']} | {r['proposed'] for r in contract['excluded_fields']} == set(baseline)
field_results = []
for row in contract['fields']:
    assert row['baseline_coverage_status'] == baseline[row['proposed']]['coverage_status'] if 'coverage_status' in baseline[row['proposed']] else row['baseline_coverage_status'] == baseline[row['proposed']]['status']
    assert row['proposed_contract'] == baseline[row['proposed']]['proposed_contract']
    counts = collections.Counter()
    checked = 0
    for loc in row.get('exact_current_locators', []):
        value = ptr(loc['file'], loc['pointer'])
        counts[type(value).__name__] += 1
        checked += 1
    for loc in row.get('origin_current_paths', []):
        ptr(loc['file'], loc['pointer'])
    field_results.append({'field': row['proposed'], 'baseline_status': row['baseline_coverage_status'],
                          'batch_status': row['batch_status'], 'proposed_type': row['proposed_contract']['type'],
                          'required': row['proposed_contract']['required'], 'empty_unknown': row['proposed_contract']['empty_unknown'],
                          'actual_locator_count': checked, 'actual_value_types': dict(counts),
                          'transform': row['transform'], 'source_selectors': row.get('source_selectors'), 'oracle': row['oracle']})
for row in contract['excluded_fields']:
    assert row['baseline_status'] == baseline[row['proposed']].get('coverage_status', baseline[row['proposed']].get('status'))
dump('fields.json', field_results)
canonical = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
generated = sorted([[r['logical_file_key'], r['sha256']] for r in manifest if r['domain'] == 'generated-silver'])
changed = [list(r) for r in generated]
for row in changed:
    if row[0] == 'silver-entity-graph-design/design.json':
        row[1] = '0' * 64
snapshot = lambda rows: 'snap:' + hashlib.sha256(canonical(['generated-silver', 'procedure-hub/generated-silver', rows]).encode()).hexdigest()
occurrence = lambda snap: 'src:' + hashlib.sha256(canonical([snap, 'step1-products.json', '/items/0/4_license']).encode()).hexdigest()
dump('identity-proof.json', {'method': 'DATA-001 section 2 formulas, hypothetical design hash edit in memory only',
     'before_snapshot': snapshot(generated), 'after_snapshot': snapshot(changed),
     'before_license_occurrence': occurrence(snapshot(generated)), 'after_license_occurrence': occurrence(snapshot(changed)),
     'design_only_changes_unrelated_source_ref': occurrence(snapshot(generated)) != occurrence(snapshot(changed)),
     'baseline_locator_checks': dict(baseline_checks)})

products = read(BASE / 'step1-products.json')['items']
families = read(BASE / 'step2-families.json')
step5 = read(BASE / 'step5-units.json')
taxonomy = read(rawroot / 'taxonomy.json')
source_rows = []
for mi, modality in enumerate(taxonomy['modality']):
    for si, sub in enumerate(modality.get('subcategories', [])):
        for ii, item in enumerate(sub.get('items', [])):
            source_rows.append((f'/modality/{mi}/subcategories/{si}/items/{ii}', item, 'extracted'))
    for pi, product in enumerate(modality.get('products', [])):
        source_rows.append((f'/modality/{mi}/products/{pi}', product, 'taxonomy_products'))
assert len(source_rows) == 580
source_by_id = {row['id']: (pointer, row, group) for pointer, row, group in source_rows}
assert len(source_by_id) == 580
rules = step5['rules']['extracted']['key_normalize']
actual_fields = []
collisions = []
rename_counts = collections.Counter()
for pointer, row, group in source_rows:
    extracted = row.get('extracted', {})
    fields = [('safety.' + k, v, '/safety/' + k.replace('~', '~0').replace('/', '~1'))
              for k, v in extracted.get('safety', {}).items()]
    if 'aftercare' in extracted:
        fields.append(('aftercare', extracted['aftercare'], '/aftercare'))
    normalized = {}
    by_predicate = collections.defaultdict(list)
    for field, value, suffix in fields:
        pred = rules.get(field, field)
        if pred != field:
            rename_counts[(field, pred)] += 1
        record = {'legacy_id': row['id'], 'raw_pointer': pointer + '/extracted' + suffix,
                  'raw_field': field, 'raw_value': value, 'normalized_predicate': pred, 'leaf_count': leaves(value)}
        actual_fields.append(record)
        by_predicate[pred].append(record)
        normalized[pred] = value
    current = next(x for x in step5[group] if x['id'] == row['id'])
    assert current['source_text'] == normalized, row['id']
    for pred, rows in by_predicate.items():
        if len(rows) > 1:
            collisions.append({'id': row['id'], 'predicate': pred, 'fields': rows,
                               'before_leaf_count': leaves(normalized[pred]),
                               'after_leaf_count': sum(x['leaf_count'] for x in rows)})
oracle = read(BASE / 'silver-data-contract-batch1/results/safety-field-oracle.json')
actual_map = {r['raw_pointer']: r for r in actual_fields}
assert len(actual_fields) == len(oracle) == 1394
assert sum(r['leaf_count'] for r in actual_fields) == 4170
assert set(actual_map) == {r['raw_pointer'] for r in oracle}
for row in oracle:
    actual = actual_map[row['raw_pointer']]
    for key in actual:
        assert actual[key] == row[key], (row['raw_pointer'], key)
    assert ptr(row['raw_file'], row['raw_pointer']) == row['raw_value']
locators = read(BASE / 'silver-data-contract-batch1/results/safety-origin-locators.json')
assert len(locators) == 580
for row in locators:
    raw = ptr(row['raw_file'], row['raw_pointer'])
    current = ptr(row['current_file'], row['current_pointer'])
    assert raw['id'] == current['id'] == row['legacy_id']
    assert raw.get('extracted', {}).get('safety') == row['raw_safety']
    assert raw.get('extracted', {}).get('aftercare') == row['raw_aftercare']
overrides = []
for group in ['units', 'product_links']:
    for i, owner in enumerate(step5[group]):
        for j, value in enumerate(owner.get('side_effect_override', [])):
            overrides.append({'pointer': f'/{group}/{i}/side_effect_override/{j}', 'value': value})
inventory = read(BASE / 'silver-data-contract-batch1/results/override-inventory.json')
assert {r['pointer']: r['value'] for r in overrides} == {r['pointer']: r['value'] for r in inventory}
collision_ids = {r['id'] for r in collisions}
dump('safety.json', {'rows': len(source_rows), 'groups': dict(collections.Counter(g for _, _, g in source_rows)),
     'fields': len(actual_fields), 'scalar_leaves': sum(r['leaf_count'] for r in actual_fields),
     'raw_oracle_exact': True, 'all_current_source_text_equals_last_write_projection': True,
     'normal_renames': [{'from': a, 'to': b, 'count': n} for (a, b), n in rename_counts.items()],
     'collisions': collisions, 'override_count': len(overrides),
     'override_groups': dict(collections.Counter(r['pointer'].split('/')[1] for r in overrides)),
     'collision_override_occurrences': [r for r in overrides if r['value']['id'] in collision_ids],
     'ownerless_or_candidate_rows': [{'pointer': '/' + group + '/' + str(next(i for i,x in enumerate(step5[group]) if x['id']==row['id'])),
                                      'id': row['id'], 'attach': row['attach'], 'units': row.get('units'),
                                      'safety_fields': len([r for r in actual_fields if r['legacy_id']==row['id']])}
                                     for group in ['extracted','taxonomy_products'] for row in step5[group]
                                     if row['attach'].startswith('원문 보관') or row['attach']=='단위 시술 후보']})
active = {x['ledger_id'] for x in products if x['active']}
assert active == {x['ledger_id'] for x in families['product_family']}
assert len({x['ledger_id'] for x in products}) == 395
assert len({x['id'] for x in families['families']}) == 27
tech = read(BASE / 'step4-techniques.json')
node_ids = {x['id'] for x in tech['nodes']}
for default in tech['family_defaults']:
    assert default['family'] in {x['id'] for x in families['families']}
    for target in [default['default']] + default['also']:
        assert target in node_ids, target
dump('census.json', {'products': len(products), 'active': len(active), 'inactive': len(products)-len(active),
     'families': len(families['families']), 'product_family': len(families['product_family']),
     'active_mapping_id_sets_equal': True, 'family_null': sum(x['family'] is None for x in families['product_family']),
     'pending_director': sum(bool(x.get('pending_director')) for x in families['product_family']),
     'family_defaults_reachable': len(tech['family_defaults']),
     'baseline': coverage['summary']['by_status'], 'scope': dict(collections.Counter(r['proposed'].split('.')[0] for r in contract['fields'])),
     'unresolved_baseline': [r['proposed'] for r in coverage['fields'] if r.get('coverage_status', r.get('status')) == '의미미확정']})
links = []
for doc in [BASE/'DATA-001.md', BASE/'WORK-013.md']:
    for target in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
        if not target.startswith(('http:', 'https:')):
            links.append({'document': doc.name, 'target': target, 'exists': (doc.parent / target.split('#')[0]).exists()})
dump('links.json', links)
start = read(RESULTS / 'protected-start.json')
changes = [r['file'] for r in start if not Path(r['file']).is_file() or
           sha(r['file']) != r['sha256'] or Path(r['file']).stat().st_size != r['bytes']]
end = [{'file': r['file'], 'bytes': Path(r['file']).stat().st_size, 'sha256': sha(r['file'])}
       for r in start if Path(r['file']).is_file()]
dump('protected-end.json', end)
dump('verification.json', {'independent_assertions': 'PASS', 'protected_files': len(start),
     'protected_changes': changes, 'start_manifest_sha256': sha(RESULTS/'protected-start.json'),
     'end_manifest_sha256': sha(RESULTS/'protected-end.json'),
     'review_script_sha256': sha(__file__), 'input_manifest_mismatches': [r['logical_file_key'] for r in manifest_rows if not r['matches']],
     'broken_links': [r for r in links if not r['exists']],
     'contract_verdict': 'FAIL; see report.md for interpretation; assertions validate evidence, not contract closure'})
print(json.dumps({'independent_assertions': 'PASS', 'protected_changes': changes,
                  'input_mismatches': [r['logical_file_key'] for r in manifest_rows if not r['matches']]}, ensure_ascii=False))
