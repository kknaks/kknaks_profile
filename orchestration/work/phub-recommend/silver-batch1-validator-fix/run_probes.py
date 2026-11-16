"""Full CLI tests on local copies, with graph/sidecar IDs and export hashes reconciled."""
from pathlib import Path
import copy, sys, subprocess, os
from collections import Counter
B=Path(__file__).resolve().parent.parent
R=Path(__file__).resolve().parent
M=B/'silver-batch1-migration'
sys.path.insert(0,str(M))
from test_contract import rehash
from transport import load,write,sha
C=B/'silver-batch1-candidate'
base=load(C/'records.json')
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
def replace(v,changes):
    if isinstance(v,str):return changes.get(v,v)
    if isinstance(v,list):return [replace(x,changes) for x in v]
    if isinstance(v,dict):return {k:replace(x,changes) for k,x in v.items()}
    return v

def materialize(out,g=None):
    out.mkdir(exist_ok=False)
    changes={}
    if g is not None:
        g=rehash(g)
        claims={c['id']:c for c in g['claims']}
        changes={a['id']:b['id'] for group in ['scopes','mappings','claims','attachments','decisions'] for a,b in zip(base[group],g[group]) if a['id']!=b['id']}
    for f in C.iterdir():
        if not f.is_file() or f.name in ['validation.json','counterexamples.json','output-manifest.json']:continue
        if f.name=='records.json' and g is not None:write(out/f.name,g)
        elif f.suffix=='.json' and changes:
            v=load(f);changed=replace(v,changes)
            # Reconcile raw export/projection duplicates as well as their graph refs.
            def sync_raw(value):
                if isinstance(value,list):return [sync_raw(x) for x in value]
                if isinstance(value,dict):
                    value={k:sync_raw(x) for k,x in value.items()}
                    if isinstance(value.get('claim_ref'),str) and value['claim_ref'] in claims and 'raw_value' in value:
                        value['raw_value']=copy.deepcopy(claims[value['claim_ref']]['raw_value'])
                    return value
                return value
            changed=sync_raw(changed)
            if changed!=v:write(out/f.name,changed)
            else:(out/f.name).symlink_to(f)
        else:(out/f.name).symlink_to(f)
    manifest=load(C/'output-manifest.json')
    for f in manifest['files']:
        f['sha256']=sha(out/f['file']);f['bytes']=(out/f['file']).stat().st_size
    write(out/'output-manifest.json',manifest)
    return len(changes)

def product(g):return next(p for p in g['products'] if p['line_memberships'])
def scope(g,kind):
    if kind=='product':return g['scopes'][0]
    if kind=='family':return next(s for s in g['scopes'] if len(s['source_refs'])==1 and s['axes']['family']['included'])
    if kind=='membership':
        mid=next(m for m in g['mappings'] if m['purpose']=='membership' and 'legacy' in m)['scope_ref']
        return next(s for s in g['scopes'] if s['id']==mid)
    if kind=='safety_unit':return next(s for s in g['scopes'] if len(s['source_refs'])==2 and s['axes']['unit_procedure']['included'])
    return next(s for s in g['scopes'] if s['statement_qualifiers'])

def excluded(g,kind):
    s=scope(g,kind);axis='family' if kind=='family' else 'unit_procedure' if kind=='safety_unit' else 'product'
    candidates=[r['id'] for r in (g['families'] if axis=='family' else g['registry'] if axis=='unit_procedure' else g['products']) if r['id'].startswith(axis+':') and r['id'] not in s['axes'][axis]['included']]
    s['axes'][axis]['excluded']=[candidates[0]]

def qualifier(g,field,value):scope(g,'safety')['statement_qualifiers'][0][field]=value
cases=[('scope_exclusion','SCOPE_AXIS_SOURCE',lambda g:excluded(g,'product')),
       ('qualifier_erasure','SCOPE_QUALIFIER_SOURCE',lambda g:scope(g,'safety').__setitem__('statement_qualifiers',[])),
       ('line_erasure','PRODUCT_LINE_SOURCE',lambda g:product(g).__setitem__('line_memberships',[])),
       ('line_role','PRODUCT_LINE_SOURCE',lambda g:product(g)['line_memberships'][0].__setitem__('role','변조')),
       ('line_partial_field_loss','PRODUCT_LINE_SOURCE',lambda g:product(g)['line_memberships'][0].pop('reason')),
       ('line_parent','PRODUCT_LINE_SOURCE',lambda g:product(g)['line_memberships'][0].__setitem__('parent_product_ref',g['products'][0]['id'])),
       ('line_extra','PRODUCT_LINE_SOURCE',lambda g:g['products'][0]['line_memberships'].append(copy.deepcopy(product(g)['line_memberships'][0]))),
       ('line_source_fieldstate','PRODUCT_LINE_FIELD_STATE',lambda g:next(s for s in g['field_states'] if s['owner_ref']==product(g)['id'] and s['field']=='line_memberships').__setitem__('raw_refs',g['products'][0]['source_refs'])),
       ('qualifier_raw','SCOPE_QUALIFIER_SOURCE',lambda g:qualifier(g,'raw',{'attach':'발명'})),
       ('qualifier_source','SCOPE_QUALIFIER_SOURCE',lambda g:qualifier(g,'source_ref',g['scopes'][0]['source_refs'][0])),
       ('qualifier_state','SCOPE_QUALIFIER_SOURCE',lambda g:qualifier(g,'state','unreviewed')),
       ('qualifier_operator_value','SCOPE_QUALIFIER_SOURCE',lambda g:scope(g,'safety')['statement_qualifiers'][0].update(operator='=',value='invented')),
       ('qualifier_addition','SCOPE_QUALIFIER_SOURCE',lambda g:scope(g,'safety')['statement_qualifiers'].append(copy.deepcopy(scope(g,'safety')['statement_qualifiers'][0]))),
       ('axis_raw_refs','SCOPE_AXIS_SOURCE',lambda g:scope(g,'safety')['axes']['site'].__setitem__('raw_refs',g['scopes'][0]['source_refs'])),
       ('scope_source_refs','SCOPE_SOURCE_CENSUS',lambda g:scope(g,'safety').__setitem__('source_refs',g['scopes'][0]['source_refs'])),
       ('raw_value_control','SAFETY_RAW',lambda g:next(c for c in g['claims'] if c['kind']=='safety').__setitem__('raw_value',['변조']))]
for kind in ('family','membership','safety_unit'):
    cases.append((kind+'_excluded','SCOPE_AXIS_SOURCE',lambda g,k=kind:excluded(g,k)))
for kind in ('product','family'):
    cases.append((kind+'_qualifier_addition','SCOPE_QUALIFIER_SOURCE',lambda g,k=kind:scope(g,k)['statement_qualifiers'].append(copy.deepcopy(scope(g,'safety')['statement_qualifiers'][0]))))
if '--raw-only' in sys.argv:
    cases=[c for c in cases if c[0]=='raw_value_control']
    prior=load(R/'full-cli-probes.json')
    write(R/'raw-control-initial-harness.json',next(r for r in prior if r['name']=='raw_value_control'))
    import shutil
    shutil.rmtree(R/'cli-raw_value_control')
    results=[r for r in prior if r['name']!='raw_value_control']
else:
    results=[]
positive=R/'positive-copy'
if not positive.exists():materialize(positive)
proc=subprocess.run([sys.executable,str(M/'validate.py'),'--candidate',str(positive),'--independent-source'],capture_output=True,text=True,env=env)
write(R/'positive-cli.json',{'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'validation':load(positive/'validation.json')})
assert proc.returncode==0,proc.stdout
for name,code,fn in cases:
    g=copy.deepcopy(base);fn(g);out=R/('cli-'+name);changed=materialize(out,g)
    proc=subprocess.run([sys.executable,str(M/'validate.py'),'--candidate',str(out),'--independent-source'],capture_output=True,text=True,env=env)
    result=load(out/'validation.json');codes=Counter(d['code'] for d in result['diagnostics'])
    passed=proc.returncode==1 and codes[code]>0 and codes['NORMALIZED_ID']==0 and codes['OUTPUT_HASH']==0 and not any(k.startswith('SIDECAR') or k in ['MAPPING_LEDGER_RAW','MAPPING_LEDGER_CLAIMS','EXPORT_DEEP_EQUAL'] for k in codes)
    row={'name':name,'passed':passed,'expected_code':code,'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'normalized_ids_remapped':changed,'diagnostic_codes':dict(codes),'diagnostics':result['diagnostics']}
    results.append(row);write(R/'full-cli-probes.json',results);print(name,'PASS' if passed else 'FAIL',dict(codes),flush=True)
assert all(r['passed'] for r in results)
