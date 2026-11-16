"""Independent read-only source checks; writes only this contract-fix/results directory.
No builder, previous verifier, or validator is imported or executed.
"""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
RESULTS = HERE / 'results'
CACHE = {}
def read(p):
    p = Path(p)
    if p not in CACHE:
        CACHE[p] = json.loads(p.read_text())
    return CACHE[p]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canonical(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
def digest(v): return hashlib.sha256(canonical(v).encode()).hexdigest()
def dump(n, v): (RESULTS/n).write_text(json.dumps(v, ensure_ascii=False, indent=2)+'\n')
def ptr(p, pointer):
    v = read(p)
    for k in pointer.split('/')[1:]:
        k = k.replace('~1', '/').replace('~0', '~')
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v
def leaves(v):
    if isinstance(v, dict): return sum(leaves(x) for x in v.values())
    if isinstance(v, list): return sum(leaves(x) for x in v)
    return 1

manifest = read(HERE/'input-manifest.v2.json')
cols = read(HERE/'collections.json')
previous = read(HERE/'input-manifest.previous.json')
assert len(manifest) == len(previous) == 69
assert (HERE/'input-manifest.previous.json').read_bytes() == (HERE.parent/'results/input-manifest.json').read_bytes()
assert len({(r['domain'],r['logical_file_key']) for r in manifest}) == 69
checks = []
for row in manifest:
    p = Path(row['file'])
    assert sha(p) == row['sha256'] and p.stat().st_size == row['bytes'], p
    assert p != BASE/'_RESUME.md'
    assert row['collection'] == 'procedure-hub/'+row['domain']
    if p.suffix == '.json':
        value = read(p)
    else: value = None
    present = isinstance(value, dict) and 'version' in value
    raw_version = value['version'] if present else None
    meta = row['meta']
    assert meta['version_state'] == (('null' if raw_version is None else 'value') if present else 'missing')
    assert type(meta['source_version_raw']) == type(raw_version) and meta['source_version_raw'] == raw_version
    assert meta['source_version_type'] == (type(raw_version).__name__ if present else None)
    assert meta['version_pointer'] == ('/version' if present else None)
    if not present: assert meta['version_reason']
    checks.append({'file':str(p),'matches':True,'meta':meta})
expected = {'raw21':21,'generated-silver':18,'research-artifact':11,'decision-artifact':13,'audit-artifact':6}
assert dict(collections.Counter(r['domain'] for r in manifest)) == expected
for col in cols:
    assert sorted(col['members']) == sorted(r['logical_file_key'] for r in manifest if r['domain']==col['domain'])
    assert len(col['members']) == col['count'] == expected[col['domain']]
    assert col['source_version'] is None and col['source_version_reason']
    assert col['semantic_source'] == (col['domain'] != 'audit-artifact')
raw = [r for r in manifest if r['domain']=='raw21']
root = Path(raw[0]['file']).parent
assert {Path(r['file']) for r in raw} == {p for p in root.rglob('*') if p.is_file() and not p.name.startswith('.')}
# Previous identities are preserved for every member except explicit frozen log replacement.
old_by_key = {r['logical_file_key']:r for r in previous}
for row in manifest:
    if row['logical_file_key'].startswith('frozen-inputs/'): continue
    old = old_by_key[row['logical_file_key']]
    assert row['sha256']==old['sha256'] and row['bytes']==old['bytes']
    assert row['meta']['source_kind']==old['source_kind']
# Missing/null/int/string file version distinctions also tested when not all occur in inputs.
for obj,state,kind in [({},'missing',None),({'version':None},'null','NoneType'),({'version':1},'value','int'),({'version':'v1'},'value','str')]:
    present='version' in obj; v=obj.get('version')
    assert (('null' if v is None else 'value') if present else 'missing')==state
    assert (type(v).__name__ if present else None)==kind
dump('manifest.json',{'files':checks,'counts':expected,'P0_input_hashes_pass':True,'file_version_positive':['missing','null','int','str'],'actual_version_states':dict(collections.Counter(r['meta']['version_state'] for r in manifest))})

recon = read(HERE/'reconciliation.json')
frozen = Path(recon['current_snapshot']['file'])
assert sha(frozen)==recon['current_snapshot']['sha256']
assert recon['previous_original_bytes_available'] is False
assert recon['previous_expected']==previous[0]
lines=frozen.read_text().splitlines()
for cite in recon['resume_citations']:
    assert ptr(BASE/'step2-families.json',cite['current_pointer'])==cite['current_value']
    for line in cite['snapshot_lines']:
        assert lines[line['line']-1]==line['text'] and cite['snapshot_anchor'] in line['text']
families=read(BASE/'step2-families.json')
for row,fam in zip(recon['family_name_basis'],families['families']):
    for key in ['id','name','name_basis','literature_evidence']:
        assert row[key]==fam.get(key,[])
assert len(recon['family_name_basis'])==27
assert ptr(root/'literature-evidence.json','/categories/M1/name')==families['families'][0]['literature_name']
for item in recon['M1_independent_current_source_ATC']:
    assert ptr(BASE/'step1-products.json',item['pointer'])==item['value']
for item in recon['family_source_corroboration']:
    assert ptr(item['source_file'],item['source_pointer']) == item['source_value']
    current=ptr(BASE/'step2-families.json',item['current_pointer'])
    if item['compared_field']=='literature_name': assert item['source_value']==current['literature_name']
    elif item['compared_field']=='name': assert item['source_value']==current['name']
    else:
        assert item['source_value']['name']==current['name']
        assert item['source_value']['name_basis']==current['name_basis']
assert len(recon['family_source_corroboration'])==27
dump('reconciliation.json',{'citation_count':len(recon['resume_citations']),'family_basis_count':27,'M1_raw_literature_and_license_ATC':True,'all_27_family_source_corroborations':True,'old_bytes_recovered':False,'approved_current_snapshot_sha256':sha(frozen)})

# Identity proofs use the documented formula on in-memory copies, never source mutation.
def snap(rows,domain):
    selected=sorted([[r['logical_file_key'],r['sha256']] for r in rows if r['domain']==domain])
    return 'snap:'+digest([domain,'procedure-hub/'+domain,selected])
def occurrence(rows): return 'src:'+digest([snap(rows,'generated-silver'),'step1-products.json','/items/0/4_license'])
def claim_id(rows):
    payload={'source_refs':[occurrence(rows)],'subject_ref':'product:test-fixture','predicate':'license','raw_value':{'fixture':True}}
    return 'claim:'+digest(['batch1-schema/2','batch1-source-preservation/2',payload])
audit_only=copy.deepcopy(manifest)
for r in audit_only:
    if r['domain']=='audit-artifact': r['sha256']='0'*64
source_change=copy.deepcopy(manifest)
next(r for r in source_change if r['logical_file_key']=='step1-products.json')['sha256']='1'*64
assert snap(manifest,'audit-artifact')!=snap(audit_only,'audit-artifact')
assert occurrence(manifest)==occurrence(audit_only) and claim_id(manifest)==claim_id(audit_only)
assert occurrence(manifest)!=occurrence(source_change) and claim_id(manifest)!=claim_id(source_change)
dump('identity-proof.json',{'method':'Memory-only documented formula tests; synthetic normalized payload explicitly retains source_refs; no candidate implementation claimed','before':{'occurrence':occurrence(manifest),'claim':claim_id(manifest)},'audit_only':{'occurrence':occurrence(audit_only),'claim':claim_id(audit_only)},'source_change':{'occurrence':occurrence(source_change),'claim':claim_id(source_change)},'audit_only_invariant':True,'source_change_propagates':True})

# Full source census and safety field reconstruction independent of stored oracle.
products=read(BASE/'step1-products.json')['items']
assert len({x['ledger_id'] for x in products})==395
active={x['ledger_id'] for x in products if x['active']}
assert len(active)==354 and len(families['families'])==27
assert active=={x['ledger_id'] for x in families['product_family']}
taxonomy=read(root/'taxonomy.json'); step5=read(BASE/'step5-units.json')
rows=[]
for mi,mod in enumerate(taxonomy['modality']):
    for si,sub in enumerate(mod.get('subcategories',[])):
        for ii,r in enumerate(sub.get('items',[])): rows.append((f'/modality/{mi}/subcategories/{si}/items/{ii}',r,'extracted'))
    for pi,r in enumerate(mod.get('products',[])): rows.append((f'/modality/{mi}/products/{pi}',r,'taxonomy_products'))
assert len(rows)==580
actual=[]; excluded=[]; fields_by_row={}
for pointer,row,group in rows:
    ext=row.get('extracted',{})
    vals=[('safety.'+k,v,'/safety/'+k.replace('~','~0').replace('/','~1')) for k,v in ext.get('safety',{}).items()]
    if 'aftercare' in ext: vals.append(('aftercare',ext['aftercare'],'/aftercare'))
    curr_index=next(i for i,r in enumerate(step5[group]) if r['id']==row['id'])
    curr=step5[group][curr_index]
    is_excluded=curr['attach'].startswith('원문 보관') or curr['attach']=='단위 시술 후보'
    records=[]
    for field,value,suffix in vals:
        record={'legacy_id':row['id'],'raw_pointer':pointer+'/extracted'+suffix,'raw_field':field,'raw_value':value,'normalized_predicate':step5['rules']['extracted']['key_normalize'].get(field,field),'leaf_count':leaves(value)}
        records.append(record);actual.append(record)
    fields_by_row[row['id']]=records
    if is_excluded:
        excluded.append({'legacy_id':row['id'],'current_pointer':f'/{group}/{curr_index}','raw_pointer':pointer,'attach':curr['attach'],'raw_candidates':curr.get('units'),'field_pointers':[r['raw_pointer'] for r in records],'field_count':len(records),'attachment_state':'not_created','attachment_reason':'candidate_only' if curr['attach']=='단위 시술 후보' else 'out_of_batch_entity','claim_preservation_required':True})
assert len(actual)==1394 and sum(r['leaf_count'] for r in actual)==4170
oracle=read(HERE.parent/'results/safety-field-oracle.json')
assert len(oracle)==1394
actual_by_ptr={r['raw_pointer']:r for r in actual}
for row in oracle:
    assert all(actual_by_ptr[row['raw_pointer']][k]==row[k] for k in actual_by_ptr[row['raw_pointer']])
assert len(excluded)==56 and sum(r['field_count'] for r in excluded)==132
assert sum(r['attachment_reason']=='candidate_only' for r in excluded)==19
assert sum(r['attachment_reason']=='out_of_batch_entity' for r in excluded)==37
assert len({p for r in excluded for p in r['field_pointers']})==132
# No owner assignment is inferred here; remaining set still needs builder owner verification.
dump('safety.json',{'rows':580,'fields':1394,'scalar_leaves':4170,'raw_oracle_exact':True,'candidate_rows':19,'preservation_only_rows':37,'required_not_created_fields':132,'remaining_rows_needing_owner_verification':524,'remaining_fields_needing_owner_verification':1262,'excluded_rows':excluded,'coverage_equation':'all_raw_fields = eligible_fields disjoint-union not_created_fields; all preserve raw; eligible attachments>=1; not_created attachments=0','candidate_implementation_executed':False})

contract=read(HERE.parent/'field-contract.json'); coverage=read(BASE/'silver-pilot-closeout-review/coverage.json')
baseline={r['proposed']:r for r in coverage['fields']}
assert len(baseline)==247 and len(contract['fields'])==84 and len(contract['excluded_fields'])==163
assert {r['proposed'] for r in contract['fields']+contract['excluded_fields']}==set(baseline)
locators=0
for field in contract['fields']:
    orig=baseline[field['proposed']]
    assert field['baseline_coverage_status']==orig.get('coverage_status',orig.get('status'))
    assert field['proposed_contract']==orig['proposed_contract']
    for loc in field.get('exact_current_locators', []): ptr(loc['file'],loc['pointer']);locators+=1
for field in contract['excluded_fields']:
    assert field['baseline_status']==baseline[field['proposed']].get('coverage_status',baseline[field['proposed']].get('status'))
for filename in ['DATA-001.md','WORK-013.md']:
    text=(BASE/filename).read_text()
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if not target.startswith(('http:','https:')):
            assert (BASE/target.split('#')[0]).exists(),target
assert contract['input_manifest']=='contract-fix/input-manifest.v2.json'
assert 'results/input-manifest.json' not in (BASE/'WORK-013.md').read_text()
for name in ['snapshot.source_kind','snapshot.source_version','snapshot.files','claim.subject_ref','attachment.claim_refs','attachment.target_ref','attachment.rule']:
    transform=next(f['transform'] for f in contract['fields'] if f['proposed']==name)
    assert transform in (BASE/'DATA-001.md').read_text(),name
for item in read(HERE/'evidence-manifest.json'):
    assert sha(HERE/item['file'])==item['sha256'] and (HERE/item['file']).stat().st_size==item['bytes']
allowed={BASE/'DATA-001.md',BASE/'WORK-013.md',HERE.parent/'field-contract.json'}
protected=read(RESULTS/'protected-start.json')
changes=[]
for r in protected:
    p=Path(r['file'])
    if sha(p)!=r['sha256'] or p.stat().st_size!=r['bytes']: changes.append(str(p))
assert set(changes)=={str(p) for p in allowed}
dump('protected-end.json',[{'file':r['file'],'sha256':sha(r['file']),'bytes':Path(r['file']).stat().st_size,'authorized_contract_change':Path(r['file']) in allowed} for r in protected])
dump('verification.json',{'contract_fix_verdict':'PASS','CR-H1':'closed by approved frozen current snapshot + explicit missing historical bytes + source/context reconciliation','CR-H2':'closed by fixed separate audit membership and formula counterexamples','CR-H3':'closed by separate preservation and attachment denominators + actual 56/132 positive census','CR-M1':'closed by collection role/null version and original file metadata','fields':84,'baseline':247,'out_of_scope_new_implementation':0,'exact_locator_checks':locators,'protected_files_checked':len(protected),'changed_files':changes,'unauthorized_changes':0,'candidate_P0_hash_gate_ready':True,'candidate_P1_to_P5':'not implemented; separate worker required'})
print('PASS: 69 input hashes; collections 21/18/11/13/6; 580/1394/4170 safety; 56/132 unattachable; 84/247 baseline; source_refs-retaining identity proofs; protected inputs unchanged')
