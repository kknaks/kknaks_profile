"""Independent closeout runner; writes only beneath this file's directory."""
from pathlib import Path
import sys, json, hashlib, copy, subprocess, os
from collections import Counter
R=Path(__file__).resolve().parent; B=R.parent; C=B/'silver-batch1-candidate'; M=B/'silver-batch1-migration'
sys.path.insert(0,str(M))
from validate import evaluate,sidecar_checks

def load(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(v):return hashlib.sha256(canon(v)).hexdigest()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def replace(v,ids):
 if isinstance(v,str):return ids.get(v,v)
 if isinstance(v,list):return [replace(x,ids) for x in v]
 if isinstance(v,dict):return {k:replace(x,ids) for k,x in v.items()}
 return v
base=load(C/'records.json')
# Positive read-only functions: never run CLI against C.
result=evaluate(C);checks,errors=sidecar_checks(C,base)
write(R/'positive-original.json',{'evaluation':result,'sidecar_checks':checks,'sidecar_errors':errors})
assert result['verdict']=='PASS' and not errors
# Source census independently traverses source_records back to manifest documents.
manifest=load(B/'silver-data-contract-batch1/contract-fix/input-manifest.v2.json')
docs={(x['domain'],x['logical_file_key']):load(x['file']) for x in manifest if x['logical_file_key'] in ['step1-products.json','step2-families.json','step5-units.json','taxonomy.json']}
pdoc=docs['generated-silver','step1-products.json']; fdoc=docs['generated-silver','step2-families.json']; udoc=docs['generated-silver','step5-units.json']
sources={s['id']:s for s in base['source_records']}; product_ids={p['id'] for p in base['products']}; family_ids={f['id'] for f in base['families']}; units={u['id']:u for u in udoc['units']}
counts=Counter(); unknowns=Counter(); assertions=0
for s in base['scopes']:
 refs=[sources[x] for x in s['source_refs']]; owner=None;family=None;qual=[]
 if len(refs)==1:
  src=refs[0];row=src['raw_value'];kind='product' if src['logical_file_key']=='step1-products.json' else 'family'
  owner=kind+':'+row['ledger_id' if kind=='product' else 'id'];counts[kind]+=1
 else:
  assert len(refs)==2 and refs[0]['domain']=='raw21' and refs[1]['logical_file_key']=='step5-units.json'
  row=refs[1]['raw_value'];counts['safety']+=1
  if row['attach']!='단위 시술 후보' and not row['attach'].startswith('원문 보관'):
   if row.get('product') and 'product:'+row['product'] in product_ids:owner='product:'+row['product']
   elif not row.get('product') and row['attach']=='단위 시술' and len(row.get('units',[]))==1:
    uid=row['units'][0]
    if uid in units and any(x.get('src')=='ledger' and x.get('id')==row['id'] and x.get('role')!='후보' for x in units[uid].get('sources',[])):owner='unit_procedure:'+uid
  if 'family:'+str(row.get('family')) in family_ids:family='family:'+row['family']
  qual=[{'axis':'legacy_context','raw':{k:v for k,v in row.items() if k in {'attach','family','sub_family','shown_on','units'}},'source_ref':refs[1]['id'],'operator':None,'value':None,'state':'needs_source'}]
  unknowns['qualifiers_needs_source']+=1
 for axis,values in s['axes'].items():
  included=([owner] if owner and owner.split(':')[0]==axis else [])
  if axis=='family' and family:included=[family]
  assert values=={'knowledge':'explicit' if included else 'not_declared','included':included,'excluded':[],'raw_refs':s['source_refs'],'value_kind':'none' if axis in {'statement_site','patient_conditions'} else 'entity_refs'}
  assertions+=1
 assert s['statement_qualifiers']==qual and s['container_scope_ref'] is None and s['conflicts']==[] and s['application_state']=='unknown'
 unknowns['application_unknown']+=1
# Relational line comparison by edges rather than builder's product-first construction.
expected=set()
for row in pdoc['items']:
 line=row.get('line') or {}; parent=line.get('line_row');owner='product:'+row['ledger_id']
 if parent and 'product:'+parent in product_ids and 'product:'+parent!=owner:expected.add((owner,'product:'+parent,line.get('role')))
for master in pdoc['lines'].values():
 parent='product:'+str(master.get('line_row'))
 if parent not in product_ids:continue
 for item in master.get('items',[]):
  owner='product:'+str(item.get('ledger_id'))
  if owner not in product_ids or owner==parent:continue
  row=next(x for x in pdoc['items'] if 'product:'+x['ledger_id']==owner)
  expected.add((owner,parent,(row.get('line') or {}).get('role','품목')))
actual={(p['id'],e['parent_product_ref'],e['role']) for p in base['products'] for e in p['line_memberships']}
assert expected==actual
unresolved=[m for m in base['mappings'] if m['purpose']=='membership' and any(sources[x]['logical_file_key']=='step1-products.json' and sources[x]['pointer'].endswith('/line') for x in m['source_refs'])]
assert all(m['state']=='unresolved' and not m['selected_refs'] and not m['candidates'] and m['rule'] is None and m['reason'] for m in unresolved)
write(R/'source-direct.json',{'scope_counts':dict(counts),'axis_assertions':assertions,'preserved_unknowns':dict(unknowns),'products_compared':len(base['products']),'line_edges':len(expected),'edges':sorted(expected),'line_unresolved':len(unresolved),'unresolved_ids':[m['id'] for m in unresolved]})

def materialize(name,g):
 out=R/name;out.mkdir(exist_ok=False)
 for group,prefix in [('scopes','scp'),('mappings','map'),('claims','clm'),('decisions','dec'),('attachments','att')]:
  ids={x['id']:prefix+':'+digest([g['record_schema_version'],g['mapping_rule_revision'],{k:v for k,v in x.items() if k not in {'id','type'}}]) for x in g[group]}
  g=replace(g,ids)
 ids={a['id']:b['id'] for group in ['scopes','mappings','claims','decisions','attachments'] for a,b in zip(base[group],g[group]) if a['id']!=b['id']}
 # All changed tests retain record ordering. Erasure of unresolved mapping needs special remapping below.
 for f in C.iterdir():
  if not f.is_file() or f.name in {'validation.json','counterexamples.json','output-manifest.json'}:continue
  if f.name=='records.json':write(out/f.name,g)
  elif f.name=='mapping-ledger.json':
   ledger=replace(load(f),ids);maps={x['id']:x for x in g['mappings']}
   for row in ledger:
    m=maps[row['mapping_ref']]
    for k in ['source_refs','purpose','state','candidates','selected_refs','rule','reason','scope_ref','decision_refs']:row[k]=copy.deepcopy(m.get(k))
   write(out/f.name,ledger)
  elif f.suffix=='.json' and ids:
   v=load(f);v2=replace(v,ids)
   if v2!=v:write(out/f.name,v2)
   else:(out/f.name).symlink_to(f)
  else:(out/f.name).symlink_to(f)
 om=load(C/'output-manifest.json')
 for x in om['files']:x.update(sha256=sha(out/x['file']),bytes=(out/x['file']).stat().st_size)
 write(out/'output-manifest.json',om)
 return out,len(ids)
def scope(g):return next(s for s in g['scopes'] if s['statement_qualifiers'])
def product(g):return next(p for p in g['products'] if p['line_memberships'])
def axis(g):return scope(g)['axes']['site']
cases=[('scope_exclusion','SCOPE_AXIS_SOURCE',lambda g:g['scopes'][0]['axes']['product']['excluded'].append(g['products'][1]['id'])),('qualifier_erasure','SCOPE_QUALIFIER_SOURCE',lambda g:scope(g).__setitem__('statement_qualifiers',[])),('line_erasure','PRODUCT_LINE_SOURCE',lambda g:product(g).__setitem__('line_memberships',[])),('axis_knowledge','SCOPE_AXIS_SOURCE',lambda g:axis(g).__setitem__('knowledge','unknown')),('axis_value_kind','SCOPE_AXIS_SOURCE',lambda g:axis(g).__setitem__('value_kind','source_literals')),('axis_inclusion','SCOPE_AXIS_SOURCE',lambda g:axis(g).update(knowledge='explicit',included=['family:M1'])),('scope_parent','SCOPE_PARENT_SOURCE',lambda g:scope(g).__setitem__('container_scope_ref',g['scopes'][0]['id'])),('scope_conflicts','SCOPE_CONFLICT_SOURCE',lambda g:scope(g)['conflicts'].append({'axis':'site','source_ref':scope(g)['source_refs'][0],'raw':'invented'})),('scope_application','SCOPE_APPLICATION_SOURCE',lambda g:scope(g).__setitem__('application_state','explicit')),('qualifier_axis','SCOPE_QUALIFIER_SOURCE',lambda g:scope(g)['statement_qualifiers'][0].__setitem__('axis','site')),('line_reason_loss','PRODUCT_LINE_SOURCE',lambda g:product(g)['line_memberships'][0].pop('reason')),('line_unresolved_state','PRODUCT_LINE_UNRESOLVED',lambda g:next(m for m in g['mappings'] if m['id']==unresolved[0]['id']).__setitem__('state','exact'))]
results=[]
for name,code,mutate in cases:
 g=copy.deepcopy(base);mutate(g);out,n=materialize('cli-'+name,g)
 proc=subprocess.run([sys.executable,str(M/'validate.py'),'--candidate',str(out),'--independent-source'],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 v=load(out/'validation.json');codes=Counter(d['code'] for d in v['diagnostics'])
 noise={k:n for k,n in codes.items() if k=='NORMALIZED_ID' or k=='OUTPUT_HASH' or k.startswith('SIDECAR') or k.startswith('EXPORT') or k.startswith('MAPPING_LEDGER')}
 ok=proc.returncode==1 and codes[code]>0 and not noise
 results.append({'name':name,'expected_code':code,'passed':ok,'exit_code':proc.returncode,'normalized_ids_remapped':n,'codes':dict(codes),'consistency_noise':noise,'diagnostics':v['diagnostics'],'stderr':proc.stderr})
 write(R/'full-cli-probes.json',results);print(name,ok,dict(codes),flush=True)
assert all(x['passed'] for x in results)
