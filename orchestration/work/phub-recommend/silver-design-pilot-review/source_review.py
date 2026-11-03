"""Independent JSON reads and denominators; no pilot builder/validator imports."""
import json, hashlib
from pathlib import Path
from collections import Counter,defaultdict
R=Path(__file__).resolve().parent;B=R.parent
def read(p):return json.loads(Path(p).read_text())
raw=Path(read(B/'silver-origin-structure-audit/inventory.json')['roots']['raw'])
inventory=[]
for f in sorted(raw.glob('*.json')):
 x=read(f);inventory.append({'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'type':type(x).__name__,'root_keys':list(x) if isinstance(x,dict) else None})
def get(x,p):
 for k in p.strip('/').split('/') if p else []:x=x[int(k)] if isinstance(x,list) else x[k.replace('~1','/').replace('~0','~')]
 return x
def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():yield from walk(v,p+'/'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from walk(v,p+'/'+str(i))
tax=read(raw/'taxonomy.json');cc=read(raw/'problem-packages.json');p=read(B/'silver-design-pilot/pilot.json')
sr={x['id']:x for x in p['source_records']};cl={x['id']:x for x in p['claims']};sc={x['id']:x for x in p['scopes']};mp={x['id']:x for x in p['mappings']}
out={'raw_inventory':inventory,'checks':[]}
def ck(name,ok,**e):out['checks'].append({'check':name,'pass':bool(ok),**e})
ck('21_raw_read',len(inventory)==21)
safety=[];leafcount=0;lost=0
for ptr,x in walk(tax):
 if isinstance(x,dict) and x.get('id') in ['M1-1-3','auto-2-1774737181584','M7-P-1']:
  fields={k:v for k,v in x['extracted']['safety'].items() if k.startswith('common')};leafcount+=sum(map(len,fields.values()))
  for field,val in fields.items():
   pointer=ptr+'/extracted/safety/'+field
   found=[c for c in p['claims'] if any(sr[r]['file']==str(raw/'taxonomy.json') and sr[r]['pointer']==pointer for r in c['source_refs'])]
   ck('safety_original_list',len(found)==1 and found[0]['raw_value']==val,pointer=pointer,value=val)
   for i,vv in enumerate(val):ck('safety_leaf',sum(s['file']==str(raw/'taxonomy.json') and s['pointer']==pointer+'/'+str(i) and s['raw_value']==vv for s in sr.values())==1,pointer=pointer+'/'+str(i))
  lost+=sum(len(v) for k,v in fields.items() if k!='common');safety.append({'id':x['id'],'pointer':ptr,'fields':fields})
ck('safety_denominators',len(safety)==3 and leafcount==16 and lost==10,rows=safety,leaves=leafcount,lost=lost)
legacy=defaultdict(list);combos=[]
for pi,prob in enumerate(cc['problems']):
 for ci,row in enumerate(prob['complaints']):
  ptr=f'/problems/{pi}/complaints/{ci}';legacy[prob['problem_id']+':'+row['cc']].append((ptr,row))
  for ki,co in enumerate(row.get('combos',[])):combos.append((ptr+f'/combos/{ki}',co))
dups={k:v for k,v in legacy.items() if len(v)>1}
ck('duplicate_denominator',len(dups)==2 and sum(map(len,dups.values()))==4,duplicates=dups)
ck('combo_denominator',len(combos)==146 and Counter(len(x['combo']) for _,x in combos)=={1:21,2:119,3:6})
relations={sr[x['source_record_ref']]['pointer']:x for x in p['relation_claims'] if sr[x['source_record_ref']]['file']==str(raw/'problem-packages.json')}
for ptr,x in combos:
 r=relations[ptr]
 ck('all_combo_content_order',len(x['combo'])==r['arity'] and [sr[y['source_ref']]['raw_value'] for y in r['members']]==x['combo'] and cl[r['claim_ref']]['raw_value']==x,pointer=ptr)
 if r['arity']==1:ck('singleton_no_pair',r['relation_kind']=='single_procedure_attribute' and not r['existing_expansions'],pointer=ptr)
s7=read(B/'step7-concerns.json');s8=read(B/'step8-relations.json');s5=read(B/'step5-units.json')
notes=[]
for n in p['notes']:
 origin=sr[n['source_refs'][0]];co=get(cc,origin['pointer']);existing=sr[n['existing_claim_refs'][0]['source_record_ref']]['raw_value'];note=sr[n['source_record_ref']]['raw_value']
 notes.append({'pointer':origin['pointer'],'existing_id':existing['id'],'note_pointer':sr[n['source_record_ref']]['pointer'],'note':note})
 ck('note_actual_reason_and_parent',existing['reason']==co['reason'] and cl[n['claim_refs'][0]]['raw_value']==co)
ck('note_seven_ids',sorted(x['existing_id'] for x in notes)==['R8-0277','R8-0278','R8-0279','R8-0298','R8-0299','R8-0300','R8-0301'],notes=notes)
ck('LOSS02_existing_unit',s5['extracted'][25]['units']==['U5-016'] and s5['extracted'][25]['attach']=='단위 시술',row=s5['extracted'][25])
correct=[]
for native in ['auto-138-1774737181584','auto-139-1774737181584']:
 found=[(pt,x) for pt,x in walk(tax) if isinstance(x,dict) and x.get('id')==native];pt,x=found[0];parent=get(tax,pt.rsplit('/items/',1)[0]);correct.append({'native':native,'parent':parent['id'],'name':x['name']});ck('stretch_raw_parent',parent['id']=='P9-4')
out['stretch_correct_targets']=correct;out['stretch_existing_wrong']=[x for x in s8['claims'] if x['id'] in ['R8-0366','R8-0367']]
out['timing_raw']=read(raw/'contraindications.json')['rules'][0]
out['comparison_sources']=[read(raw/'procedure-comparison.json')['comparisons'][i] for i in [1,2]]
out['product_override']=s5['product_links'][243]
out['K8_existing']=s8['conditions']['not_condition'][2:4]
out['conflict_raw']=cc['problems'][1]['complaints'][3]
out['language_raw']=read(raw/'literature-evidence.json')['categories']['M2']['adverse_effects'][2]
out['duration_raw']=[tax['modality'][9]['subcategories'][0]['items'][i]['extracted']['onset_duration']['duration'] for i in [0,1]]
out['duration_decision']=read(B/'step9-decisions.json')['conflict_resolution']
for r in p['source_records']:
 actual=get(read(r['file']),r['pointer']);ck('all_source_type_fidelity',type(actual)==type(r['raw_value']) and json.dumps(actual,sort_keys=True,ensure_ascii=False)==json.dumps(r['raw_value'],sort_keys=True,ensure_ascii=False),file=r['file'],pointer=r['pointer'])
out['passed']=sum(x['pass'] for x in out['checks']);out['failed']=sum(not x['pass'] for x in out['checks'])
(R/'independent-source.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':out['passed'],'failed':out['failed']}))
