"""Fixed batch field-contract oracles, reconstructed only from immutable input documents.

No builder/rules imports and no candidate values used as expected semantic values.
The contract gate in validate pins the 84-field contract and manifest v2 first.
"""
from collections import defaultdict
from transport import canonical, digest

AXES = ('product', 'family', 'site', 'unit_procedure', 'concern', 'target',
        'container', 'site_relation', 'statement_site', 'patient_conditions')


def source_semantics(g, docs, manifest, collections, eq, check):
    snapshots = {}
    for col in collections:
        members = sorted([[r['logical_file_key'], r['sha256']] for r in manifest if r['domain'] == col['domain']])
        snapshots[col['domain']] = 'snap:' + digest([col['domain'], col['collection'], members])

    def source(key, ptr, domain='generated-silver'):
        return 'src:' + digest([snapshots[domain], key, ptr])

    def normalized(kind, payload):
        prefix = {'scope': 'scp', 'mapping': 'map'}[kind]
        return prefix + ':' + digest([g['record_schema_version'], g['mapping_rule_revision'], payload])

    pdoc = docs['generated-silver', 'step1-products.json']
    fdoc = docs['generated-silver', 'step2-families.json']
    sdoc = docs['generated-silver', 'step5-units.json']
    products = {'product:' + r['ledger_id'] for r in pdoc['items']}
    families = {'family:' + r['id'] for r in fdoc['families']}
    units = {r['id']: r for r in sdoc['units']}
    expected = {}
    entity_scope = {}

    def expect_scope(evidence, owner=None, family=None, context=None):
        axes = {}
        for axis in AXES:
            values = [owner] if owner and owner.split(':', 1)[0] == axis else []
            if axis == 'family' and family:
                values = ['family:' + family]
            axes[axis] = {'knowledge': 'explicit' if values else 'not_declared',
                          'included': values, 'excluded': [], 'raw_refs': evidence,
                          'value_kind': 'none' if axis in ('statement_site', 'patient_conditions') else 'entity_refs'}
        payload = {'axes': axes, 'container_scope_ref': None, 'statement_qualifiers': context or [],
                   'conflicts': [], 'application_state': 'unknown', 'source_refs': evidence}
        sid = normalized('scope', payload)
        expected[tuple(evidence)] = (sid, payload)
        return sid

    for key, rows, group, native, prefix in [
        ('step1-products.json', pdoc['items'], 'items', 'ledger_id', 'product:'),
        ('step2-families.json', fdoc['families'], 'families', 'id', 'family:')]:
        for i, row in enumerate(rows):
            owner = prefix + row[native]
            entity_scope[owner] = expect_scope([source(key, '/' + group + '/' + str(i))], owner)

    current = {(kind, row['id']): (i, row) for kind in ('extracted', 'taxonomy_products') for i, row in enumerate(sdoc[kind])}
    taxonomy = docs['raw21', 'taxonomy.json']
    rawrows = []
    for i, modality in enumerate(taxonomy['modality']):
        for j, sub in enumerate(modality.get('subcategories', [])):
            rawrows.extend((f'/modality/{i}/subcategories/{j}/items/{k}', row, 'extracted') for k, row in enumerate(sub.get('items', [])))
        rawrows.extend((f'/modality/{i}/products/{j}', row, 'taxonomy_products') for j, row in enumerate(modality.get('products', [])))
    for rawptr, rawrow, kind in rawrows:
        i, row = current[kind, rawrow['id']]
        context_ref = source('step5-units.json', '/' + kind + '/' + str(i))
        evidence = [source('taxonomy.json', rawptr, 'raw21'), context_ref]
        owner = None
        # Identity is evidence, not clinical application: candidates and raw-only rows stay unknown.
        if row['attach'] != '단위 시술 후보' and not row['attach'].startswith('원문 보관'):
            if row.get('product'):
                ref = 'product:' + row['product']
                if ref in products:
                    owner = ref
            elif row['attach'] == '단위 시술' and len(row.get('units', [])) == 1:
                uid = row['units'][0]
                if uid in units and any(s.get('id') == row['id'] and s.get('src') == 'ledger' and s.get('role') != '후보' for s in units[uid].get('sources', [])):
                    owner = 'unit_procedure:' + uid
        context = [{'axis': 'legacy_context', 'raw': {k: row[k] for k in ('attach', 'family', 'sub_family', 'shown_on', 'units') if k in row},
                    'source_ref': context_ref, 'state': 'needs_source', 'operator': None, 'value': None}]
        family = row.get('family') if 'family:' + str(row.get('family')) in families else None
        expect_scope(evidence, owner, family, context)

    actual = defaultdict(list)
    for scope in g['scopes']:
        actual[tuple(scope.get('source_refs', []))].append(scope)
    eq(sorted([[list(k), len(v)] for k, v in actual.items()]), sorted([[list(k), 1] for k in expected]),
       'SCOPE_SOURCE_CENSUS', 'records.scopes', 'source_refs', 'Every original product/family/safety scope exactly once; membership reuses its product scope')
    for evidence, (sid, payload) in expected.items():
        matches = actual.get(evidence, [])
        for scope in matches:
            loc = scope['id']
            for axis in AXES:
                eq(scope.get('axes', {}).get(axis), payload['axes'][axis], 'SCOPE_AXIS_SOURCE', loc, 'axes.' + axis)
            for field, code in [('statement_qualifiers', 'SCOPE_QUALIFIER_SOURCE'), ('container_scope_ref', 'SCOPE_PARENT_SOURCE'),
                                ('conflicts', 'SCOPE_CONFLICT_SOURCE'), ('application_state', 'SCOPE_APPLICATION_SOURCE'), ('source_refs', 'SCOPE_SOURCE')]:
                eq(scope.get(field), payload[field], code, loc, field)
    # Exact expected scope IDs also bind membership/identity mappings to original entity scopes.
    for mapping in g['mappings']:
        legacy = mapping.get('legacy')
        if mapping['purpose'] == 'membership' and legacy and 'ledger_id' in legacy:
            owner = 'product:' + legacy['ledger_id']
            eq(mapping.get('scope_ref'), entity_scope.get(owner), 'MEMBERSHIP_SCOPE_SOURCE', mapping['id'], 'scope_ref')

    entities = {r['id']: r for r in g['products']}
    expected_unresolved = []
    for i, row in enumerate(pdoc['items']):
        owner = 'product:' + row['ledger_id']
        ptr = '/items/' + str(i)
        evidence = source('step1-products.json', ptr)
        line = row.get('line')
        memberships = []
        def add(parent, role):
            item = {'parent_product_ref': 'product:' + parent, 'role': role, 'decision_ref': None,
                    'reason': 'Explicit line_row; no separately verified approval decision'}
            if item not in memberships:
                memberships.append(item)
        if line:
            parent = line.get('line_row')
            if parent and 'product:' + parent in products and 'product:' + parent != owner:
                add(parent, line.get('role'))
            else:
                expected_unresolved.append({'source_refs': [source('step1-products.json', ptr + '/line'), source('step1-products.json', '/lines')],
                    'purpose': 'membership', 'state': 'unresolved', 'candidates': [], 'selected_refs': [], 'rule': None,
                    'reason': 'Line string/license number does not establish a parent native ID',
                    'scope_ref': entity_scope[owner], 'decision_refs': []})
        for master in pdoc['lines'].values():
            parent = master.get('line_row')
            if parent and 'product:' + parent in products and 'product:' + parent != owner and any(item.get('ledger_id') == row['ledger_id'] for item in master.get('items', [])):
                add(parent, (line or {}).get('role', '품목'))
        eq(entities.get(owner, {}).get('line_memberships'), memberships, 'PRODUCT_LINE_SOURCE', owner, 'line_memberships',
           'Exact explicit row.line and lines.items ledger_id/line_row relationships, roles and nullable approval reasons')
        # Preserve the existing missing/value field-state distinction even when master ledger gives a parent.
        if 'line' in row:
            value = row['line']
            rawstate = 'null' if value is None else 'empty_array' if value == [] else 'empty_object' if value == {} else 'false' if value is False else 'empty_string' if value == '' else 'value'
            state = {'owner_ref': owner, 'field': 'line_memberships', 'raw_refs': [source('step1-products.json', ptr + '/line')],
                     'state': 'value', 'raw_state': rawstate, 'reason': 'Typed field from original occurrence; historical/clinical status retained'}
        else:
            state = {'owner_ref': owner, 'field': 'line_memberships', 'raw_refs': [evidence], 'state': 'unresolved', 'raw_state': 'missing',
                     'reason': 'Derived transport/ID or later exact membership join; no clinical default'}
        eq([s for s in g['field_states'] if s['owner_ref'] == owner and s['field'] == 'line_memberships'], [state],
           'PRODUCT_LINE_FIELD_STATE', owner, 'field_states.line_memberships')
    # Select by actual source path, rather than a mutable reason label, so erasure/disguise cannot escape the census.
    line_sources = {source('step1-products.json', '/items/' + str(i) + '/line') for i, row in enumerate(pdoc['items']) if row.get('line')}
    actual_unresolved = [m for m in g['mappings'] if m['purpose'] == 'membership' and line_sources.intersection(m['source_refs'])]
    expected_rows = [{'id': normalized('mapping', p), 'type': 'mapping', **p} for p in expected_unresolved]
    eq(sorted(actual_unresolved, key=canonical), sorted(expected_rows, key=canonical), 'PRODUCT_LINE_UNRESOLVED',
       'records.mappings', 'line membership unresolved mappings')
