from pathlib import Path
import sys,json,hashlib,copy
from collections import Counter
B=Path(__file__).resolve().parent.parent; R=Path(__file__).resolve().parent
sys.path.insert(0,str(B/'silver-batch1-migration'))
from validate import evaluate,sidecar_checks
from test_contract import rehash
C=R/'execution-copy'
def load(p):return json.loads(Path(p).read_text())
def save(n,v):(R/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def ptr(v,p):
 for k in p.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
G=load(C/'records.json');M=load(C/'input-manifest.json');docs={r['logical_file_key']:load(r['file']) if r['file'].endswith('.json') else Path(r['file']).read_text() for r in M}
S={r['id']:r for r in G['source_records']};claims={r['id']:r for r in G['claims']};p=docs['step1-products.json'];f=docs['step2-families.json'];tax=docs['taxonomy.json'];u=docs['step5-units.json']
checks={};checks['69_manifest_bytes']=all(hashlib.sha256(Path(r['file']).read_bytes()).hexdigest()==r['sha256'] and Path(r['file']).stat().st_size==r['bytes'] for r in M)
checks['63_complete_roots']=len([s for s in S.values() if s['pointer']==''])==63 and all(any(s['logical_file_key']==r['logical_file_key'] and s['domain']==r['domain'] and s['pointer']=='' and canon(s['raw_value'])==canon(docs[r['logical_file_key']]) for s in S.values()) for r in M if r['domain']!='audit-artifact')
checks['all_source_raw_equal']=all(canon(s['raw_value'])==canon(ptr(docs[s['logical_file_key']],s['pointer'])) for s in S.values())
checks['product_native_set']=set(e['id'] for e in G['products'])=={'product:'+r['ledger_id'] for r in p['items']}
checks['membership_active_set']={r['ledger_id'] for r in f['product_family']}=={r['ledger_id'] for r in p['items'] if r['active']}
fields=[];rows=[]
for mi,mod in enumerate(tax['modality']):
 for si,sub in enumerate(mod.get('subcategories',[])):
  rows.extend((f'/modality/{mi}/subcategories/{si}/items/{i}',v) for i,v in enumerate(sub.get('items',[])))
 rows.extend((f'/modality/{mi}/products/{i}',v) for i,v in enumerate(mod.get('products',[])))
def leaf(v):return sum(map(leaf,v.values())) if isinstance(v,dict) else sum(map(leaf,v)) if isinstance(v,list) else 1
for path,row in rows:
 ex=row.get('extracted',{})
 for k,v in ex.get('safety',{}).items():fields.append((path+'/extracted/safety/'+k,v))
 if 'aftercare' in ex:fields.append((path+'/extracted/aftercare',ex['aftercare']))
actual=[c for c in G['claims'] if c['kind'] in ['safety','preparation']]
checks['1394_exact_occurrences']=len(actual)==len(fields)==1394 and all(len([c for c in actual if any(S[x]['logical_file_key']=='taxonomy.json' and S[x]['pointer']==path for x in c['source_refs']) and canon(c['raw_value'])==canon(v)])==1 for path,v in fields)
idx=load(C/'source-row-index.json');safe=[r for r in idx if r['category']=='safety'];notrows=[r for r in safe if r['attachment_state']=='not_created']
notids={x for r in notrows for x in r['claim_refs']};attached={x for a in G['attachments'] for x in a['claim_refs']}
checks['partition']=len(notids)==152 and len(attached)==1242 and not notids&attached and notids|attached=={c['id'] for c in actual}
checks['all_unknown']=all(a['application_state']=='unknown' and a['witness']==[] and a['resolution_ref'] is None for a in G['attachments'])
counts={'products':len(p['items']),'active':sum(r['active'] is True for r in p['items']),'families':len(f['families']),'membership':len(f['product_family']),'family_null':sum(r['family'] is None for r in f['product_family']),'pending_director':sum(bool(r.get('pending_director')) for r in f['product_family']),'safety_rows':len(rows),'safety_fields':len(fields),'scalar_leaves':sum(leaf(v) for _,v in fields),'not_created_rows':dict(Counter(r['attachment_reason'] for r in notrows)),'not_created_fields':dict(Counter(r['attachment_reason'] for r in notrows for _ in r['claim_refs']))}
save('source-direct.json',{'checks':checks,'counts':counts})
save('not-created-source-review.json',[{'native_id':r['native_id'],'raw_pointer':r['raw_pointer'],'reason':r['attachment_reason'],'claim_refs':r['claim_refs'],'source_refs':r['source_refs']} for r in notrows])
probes=[]
def run(name,mutate,detail):
 g=copy.deepcopy(G);before=mutate(g);g=rehash(g);v=evaluate(C,g,check_exports=False)
 probes.append({'name':name,'source_detail':detail,'before':before,'verdict':v['verdict'],'failure_count':v['failure_count'],'normalized_id_failures':sum(d['code']=='NORMALIZED_ID' for d in v['diagnostics']),'codes':dict(Counter(d['code'] for d in v['diagnostics'])),'diagnostics':v['diagnostics'][:5]})
 save('additional-probes.json',probes);print(name,v['verdict'],v['failure_count'],flush=True)
def exclusion(g):
 s=next(s for s in g['scopes'] if s['axes']['product']['included']);before=copy.deepcopy(s)
 other=next(p['id'] for p in g['products'] if p['id'] not in s['axes']['product']['included']);s['axes']['product']['excluded']=[other]
 return before
run('invent_source_scope_exclusion',exclusion,'Inject existing but unsupported product exclusion into source scope; strict refs remain valid')
def qualifiers(g):
 s=next(s for s in g['scopes'] if s['statement_qualifiers']);before=copy.deepcopy(s);s['statement_qualifiers']=[];return before
run('delete_original_statement_qualifiers',qualifiers,'Delete existing raw statement qualifiers while all original sources remain preserved')
def lines(g):
 p=next(p for p in g['products'] if p['line_memberships']);before=copy.deepcopy(p);p['line_memberships']=[];return before
run('delete_explicit_product_line_membership',lines,'Erase an explicitly sourced line membership without altering source roots')
def raw(g):
 c=next(c for c in g['claims'] if c['raw_field']=='safety.common' and isinstance(c['raw_value'],list));before=copy.deepcopy(c);c['raw_value']=['REVIEW_ONLY_INVALID'];return before
run('source_raw_negative_control',raw,'Known raw alteration must be rejected after graph ID recomputation')
