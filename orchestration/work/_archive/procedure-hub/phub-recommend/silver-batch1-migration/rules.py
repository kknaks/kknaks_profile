"""Batch1 source preservation rules. No clinical normalization or approval."""
KEY_NORMALIZE = {
    'onset_duration.peak_effect': 'onset_duration.peak',
    'safety.common_adverse_effects': 'safety.common',
    'safety.serious_adverse_effects': 'safety.serious',
    'safety.common_side_effects': 'safety.common',
}
LANGUAGE = {'한': 'ko', '영': 'en'}
AXES = ['product', 'family', 'site', 'unit_procedure', 'concern', 'target',
        'container', 'site_relation', 'statement_site', 'patient_conditions']

def product_status(row):
    if row.get('merged_into'):
        return 'merged'
    if row.get('moved_to'):
        return 'retired'
    return 'active' if row.get('active') is True else 'pending'

def owner(row, product_ids, units):
    """Only explicit source identity; multi-owner and candidate are not selected."""
    if row['attach']=='단위 시술 후보':
        return None, 'candidate_only'
    if row['attach'].startswith('원문 보관'):
        return None, 'out_of_batch_entity'
    if row.get('product'):
        ref = 'product:'+row['product']
        return (ref, None) if ref in product_ids else (None, 'owner_unresolved')
    refs = row.get('units', [])
    if row['attach']=='단위 시술' and len(refs)==1 and refs[0] in units:
        u = units[refs[0]]
        if any(s.get('id')==row['id'] and s.get('src')=='ledger' and s.get('role')!='후보' for s in u['sources']):
            return 'unit_procedure:'+refs[0], None
    return None, 'owner_unresolved'
