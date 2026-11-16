"""Independent raw reads + strict structure/references + explicit destructive mutations.
No imports from build.py; source expectations are collected directly from snapshots.
"""
from common import *
from schema import structural,SCHEMA
from project import project
from collections import Counter,defaultdict
import copy,sys
RAW=Path(read(A/'inventory.json')['roots']['raw'])
CACHE={}
def source(file):
 if file not in CACHE:CACHE[file]=read(file)
 return CACHE[file]
def validate(p,graph=None):
 checks=[]
 def ck(name,ok,**detail):checks.append({'check':name,'pass':bool(ok),**detail})
 errs=structural(p);ck('strict_schema',not errs,errors=errs[:20])
 if errs:return checks
 ck('basis',p['basis']=={'file':str(D/'design.json'),'sha256':sha(D/'design.json'),'status':'proposal_only'})
 groups=['snapshots','source_records','entities','scopes','claims','relation_claims','mappings','decisions','resolutions','attachments','notes','cases'];idx={}
 prefixes={'snapshots':'snap','source_records':'src','scopes':'scope','claims':'clm','relation_claims':'rel','mappings':'map','decisions':'dec','resolutions':'res','attachments':'att','notes':'note'}
 for group in groups:
  idx[group]={x['id']:x for x in p[group]};ck('unique_ids',len(idx[group])==len(p[group]),group=group)
 for group,prefix in prefixes.items():
  for x in p[group]:ck('typed_id_format',bool(re.fullmatch(prefix+':[0-9a-f]{64}',x['id'])),group=group)
 allids=[x['id'] for g in groups for x in p[g]];ck('global_id_uniqueness',len(allids)==len(set(allids)))
 sr=idx['source_records'];sn=idx['snapshots'];sc=idx['scopes'];cl=idx['claims'];mp=idx['mappings'];en=idx['entities'];rr=idx['relation_claims'];de=idx['decisions'];rs=idx['resolutions'];at=idx['attachments'];notes=idx['notes'];cases=idx['cases']
 def ref(name,value,group):ck(name,value in idx[group],ref=value,group=group)
 def refs(name,values,group):
  for v in values:ref(name,v,group)
 for s in p['snapshots']:
  for f in s['files']:
   ck('snapshot_hash_bytes',Path(f['file']).is_file() and f['sha256']==sha(f['file']) and f['bytes']==Path(f['file']).stat().st_size,file=f['file'])
  ck('snapshot_identity',len(s['files'])==1 and s['id']=='snap:'+s['files'][0]['sha256'])
  ck('no_fabricated_capture_time',s['captured_at'] is None)
 for r in p['source_records']:
  ref('source_snapshot_ref',r['snapshot_ref'],'snapshots')
  ck('source_file_in_snapshot',r['snapshot_ref'] in sn and r['file'] in [x['file'] for x in sn[r['snapshot_ref']]['files']])
  try:ck('source_raw_exact',digest(r['raw_value'])==digest(get(source(r['file']),r['pointer'])),pointer=r['pointer'],file=r['file'])
  except Exception as e:ck('source_raw_exact',False,error=str(e))
  ck('occurrence_id',r['id']=='src:'+digest([r['snapshot_ref'],r['file'],r['pointer']]))
  ck('no_fabricated_continuity',r['parent_ref'] is None and r['continuity_ref'] is None)
 # An entity must retain its actual existing ID, namespace and existing Silver location.
 expected_entity_roots={'product':('step1-products.json','/items','ledger_id'),'family':('step2-families.json','/families','id'),'site':('step3-sites.json','/nodes','id'),'unit_procedure':('step5-units.json','/units','id'),'concern':('step7-concerns.json','/concerns','id'),'evidence_statement':('step8-relations.json','/evidence/statements','id')}
 for e in p['entities']:
  refs('entity_source_ref',e['source_refs'],'source_records');ck('entity_namespace',e['id']==e['type']+':'+e['native_id'])
  f,root,key=expected_entity_roots[e['type']]
  ck('existing_entity_identity',all(x in sr and sr[x]['file']==str(B/f) and sr[x]['pointer'].startswith(root+'/') and isinstance(sr[x]['raw_value'],dict) and sr[x]['raw_value'].get(key)==e['native_id'] for x in e['source_refs']),entity=e['id'])
 for s in p['scopes']:
  if s['container_scope_ref']:ref('container_scope_ref',s['container_scope_ref'],'scopes')
  for ax in s['axes'].values():refs('axis_source_ref',ax['raw_refs'],'source_records')
  for x in s['statement_qualifiers']+s['conflicts']:ref('qualifier_source_ref',x['source_ref'],'source_records')
 for c in p['claims']:
  refs('claim_source_ref',c['source_refs'],'source_records');ref('claim_scope_ref',c['scope_ref'],'scopes');refs('claim_mapping_refs',c['mapping_refs'],'mappings')
  if c['subject_ref']:ref('claim_subject_ref',c['subject_ref'],'entities')
  ck('claim_immutable_value',len(c['source_refs'])==1 and c['source_refs'][0] in sr and digest(c['raw_value'])==digest(sr[c['source_refs'][0]]['raw_value']),claim=c['id'])
  ck('unreviewed_normalization',c['normalized_value'] is None)
  if c['variant']['of']:ref('variant_ref',c['variant']['of'],'claims')
  ck('no_invented_clinical_approval',c['review_state']!='confirmed' and c['variant']['equivalence']=='unreviewed')
 for m in p['mappings']:
  refs('mapping_source_refs',m['source_refs'],'source_records');ref('mapping_scope_ref',m['scope_ref'],'scopes');refs('mapping_decision_refs',m['decision_refs'],'decisions')
  refs('candidate_targets',[c['target_ref'] for c in m['candidates']],'entities');refs('selected_targets',m['selected_refs'],'entities')
  for c in m['candidates']:ref('candidate_scope',c['scope_ref'],'scopes')
  ck('selection_subset',set(m['selected_refs'])<={c['target_ref'] for c in m['candidates']})
  ck('candidate_not_selected',m['state'] not in ['ambiguous','unresolved','compatible_candidate','excluded'] or not m['selected_refs'])
  ck('null_rule_reason',m['rule'] is not None or bool(m['reason']))
  if m['rule']:
   rf=B/m['rule']['id'];ck('existing_mapping_rule',rf.is_file() and m['rule']['id'] in ['step5-apply.py','step7-apply.py','step9-apply.py'] and m['rule']['code_sha256']==sha(rf) and any(sr[x]['file']==str(B/('step5-units.json' if m['rule']['id']=='step5-apply.py' else 'step7-concerns.json' if m['rule']['id']=='step7-apply.py' else 'step9-explanations.json')) for x in m['source_refs']))
  ck('no_unfounded_selected_state',m['state']!='selected')
 for r in p['relation_claims']:
  ref('relation_claim_ref',r['claim_ref'],'claims');ref('relation_source_ref',r['source_record_ref'],'source_records');ck('relation_arity',r['arity']==len(r['members']))
  for m in r['members']:ref('member_mapping_ref',m['mapping_ref'],'mappings');ref('member_source_ref',m['source_ref'],'source_records')
  ck('singleton_not_pair',r['arity']!=1 or (r['relation_kind']=='single_procedure_attribute' and r['direction']=='not_applicable' and not r['existing_expansions']))
  ck('no_unapproved_pair_derivation',r['parent_claim_ref'] is None and r['derivation'] is None)
  for cond in r['field_conditions'].values():
   ref('field_scope',cond['scope_ref'],'scopes');ref('field_raw',cond['raw_ref'],'source_records')
   for b in cond['options'] or []:ref('branch_scope',b['scope_ref'],'scopes');ref('branch_raw',b['raw_ref'],'source_records')
  for exp in r['existing_expansions']:
   ref('expansion_source',exp['source_record_ref'],'source_records');refs('expansion_origins',exp['source_occurrence_refs'],'source_records')
   if exp['source_record_ref'] in sr:
    v=sr[exp['source_record_ref']]['raw_value'];ck('existing_expansion_values',v['id']==exp['id'] and exp['rule_text']==v['rule'] and exp['lowering_text']==v.get('lowering') and exp['source_index']==str(v['source_index']) and exp['endpoints_raw']=={'a':v['a'],'b':v['b']} and exp['source_arity']==v.get('combo_size',2))
 for n in p['notes']:
  refs('note_claim_refs',n['claim_refs'],'claims');refs('note_sources',n['source_refs'],'source_records');ref('note_record',n['source_record_ref'],'source_records');ref('note_relation_ref',n['relation_ref'],'relation_claims')
  for x in n['existing_claim_refs']:ref('note_existing_ref',x['source_record_ref'],'source_records')
 for a in p['attachments']:
  refs('attachment_claim_refs',a['claim_refs'],'claims');ref('attachment_target',a['target_ref'],'entities');ref('attachment_scope',a['scope_ref'],'scopes')
  ck('attachment_not_approval',a['application_state']=='unknown')
  if a['resolution_ref']:ref('attachment_resolution',a['resolution_ref'],'resolutions')
 for r in p['resolutions']:
  refs('resolution_inputs',r['input_claim_refs'],'claims');refs('resolution_alternatives',r['alternatives'],'claims');ref('resolution_scope',r['scope_ref'],'scopes');ref('resolution_decision',r['policy']['decision_ref'],'decisions');ck('resolution_not_consensus',not r['clinical_consensus']);ck('alternative_subset',set(r['alternatives'])<=set(r['input_claim_refs']))
 for d in p['decisions']:
  refs('decision_sources',d['source_refs'],'source_records');ck('no_fabricated_reviewer',d['authority']['reviewer'] is None)
  ck('existing_rule_decision',d['source_refs'] and all(x in sr and sr[x]['file']==str(B/'step9-decisions.json') for x in d['source_refs']) and d['decided_at']==source(str(B/'step9-decisions.json'))['decided_at'] and d['reason']==source(str(B/'step9-decisions.json'))['decision_ref'])
 # Read every prior evidence locator again; these 42 are a denominator, not new clinical approval.
 design=source(str(D/'design.json'));issues=source(str(A/'issues.json'))['issues']
 ck('42_cases',set(cases)=={x['id'] for x in issues} and len(cases)==42)
 for i in issues:
  cs=cases.get(i['id']);
  if not cs:continue
  for key,values,group in [('source_refs',cs['source_refs'],'source_records'),('silver_refs',cs['silver_refs'],'source_records'),('claim_refs',cs['claim_refs'],'claims'),('relation_refs',cs['relation_refs'],'relation_claims'),('mapping_refs',cs['mapping_refs'],'mappings'),('scope_refs',cs['scope_refs'],'scopes'),('attachment_refs',cs['attachment_refs'],'attachments'),('note_refs',cs['note_refs'],'notes')]:refs('case_'+key,values,group)
  origin=i['origin'] if isinstance(i['origin'],list) else [i['origin']]
  for key,expected in [('source_refs',origin),('silver_refs',[i['silver']])]:
   ck('case_trace_exact',len(cs[key])==len(expected) and {(sr[x]['file'],sr[x]['pointer']) for x in cs[key] if x in sr}=={(x['file'],pointer(x['jsonpath'])) for x in expected},case=i['id'])
   for e in expected:
    ck('prior_evidence_source_rechecked',sha(e['file'])==e['sha256'] and get(source(e['file']),pointer(e['jsonpath']))==e['value'],case=i['id'])
 # Source-only safety extraction, independently discover collision lists by actual row IDs.
 tax=source(str(RAW/'taxonomy.json'));expected_safety={};safety_roots={}
 for ptr,v in walk(tax):
  if isinstance(v,dict) and v.get('id') in ['M1-1-3','auto-2-1774737181584','M7-P-1']:
   safety_roots[v['id']]=ptr
   for field,values in v['extracted']['safety'].items():
    if field.startswith('common'):expected_safety[ptr+'/extracted/safety/'+field]=values
 got_safety={sr[c['source_refs'][0]]['pointer']:c for c in p['claims'] if c['predicate']=='safety.common' and sr.get(c['source_refs'][0],{}).get('pointer') in expected_safety}
 ck('safety_all_fields',len(got_safety)==len(expected_safety)==6)
 safety_leafs=0
 for ptr,val in expected_safety.items():
  c=got_safety.get(ptr);ck('safety_field_value',c is not None and c['raw_value']==val and c['raw_field']=='safety.'+ptr.rsplit('/',1)[1],pointer=ptr)
  for suffix,value in leaves(val):
   ck('safety_leaf_occurrence',sum(r['file']==str(RAW/'taxonomy.json') and r['pointer']==ptr+suffix and r['raw_value']==value for r in sr.values())==1,pointer=ptr+suffix);safety_leafs+=1
 ck('safety_leaf_denominator',safety_leafs==16 and len(set(c['id'] for c in got_safety.values()))==6)
 lost=0
 for ci in ['LOSS-01','LOSS-02','LOSS-03']:
  cs=cases[ci];current=sr[cs['silver_refs'][0]]['raw_value'];original=[cl[x] for x in cs['claim_refs']]
  lost+=sum(v not in current for c in original for v in c['raw_value'])
  ck('surviving_and_lost_values_present',len(original)==2 and any(c['raw_value']==current for c in original) and all(c['predicate']=='safety.common' for c in original),case=ci)
  for c in original:
   ptr=sr[c['source_refs'][0]]['pointer'];modptr='/'+('/'.join(ptr.split('/')[1:3]));family='family:'+get(tax,modptr)['id'];ck('safety_source_family_preserved',sc[c['scope_ref']]['axes']['family']['included']==[family])
 for cid,subject in [('LOSS-01','product:M1-1-3'),('LOSS-02','unit_procedure:U5-016'),('LOSS-03','product:M7-P-1')]:ck('safety_subject_identity',all(cl[x]['subject_ref']==subject for x in cases[cid]['claim_refs']))
 ck('previously_lost_10_recovered_in_pilot',lost==10,leaves=lost)
 same=[c for c in got_safety.values() if c['raw_field']=='safety.common'];ck('same_content_different_occurrence_kept',len(same)==3 and len({digest(x['raw_value']) for x in same})==1 and len({x['source_refs'][0] for x in same})==3 and len({x['id'] for x in same})==3)
 loss2=cases.get('LOSS-02',{});ck('LOSS02_actual_unit_subject',loss2.get('claim_refs') and all(cl[x]['subject_ref']=='unit_procedure:U5-016' for x in loss2['claim_refs']))
 # Duplicate CC correspondence is validated against raw taxonomy ID/parent, never first name-match.
 rawcc=source(str(RAW/'problem-packages.json'));expected_dups={};legacy=defaultdict(list)
 for pi,prob in enumerate(rawcc['problems']):
  for ci,cc in enumerate(prob['complaints']):
   key=prob['problem_id']+':'+cc['cc'];legacy[key].append((f'/problems/{pi}/complaints/{ci}',cc))
 for key,rows in legacy.items():
  if len(rows)>1:expected_dups[key]=rows
 ck('legacy_alias_denominator',len(expected_dups)==2 and len(p['legacy_aliases'])==2)
 rawconcerns={}
 # taxonomy problem groups store IDs independently of Silver correspondence.
 for ptr,v in walk(tax):
  if isinstance(v,dict) and v.get('id') in ['auto-132-1774737181584','auto-139-1774737181584','auto-136-1774737181584','auto-138-1774737181584']:rawconcerns[v['id']]=(ptr,v)
 for alias in p['legacy_aliases']:
  rows=expected_dups.get(alias['alias'],[]);ck('legacy_ambiguous_not_selected',alias['state']=='ambiguous' and not alias['selected_refs'])
  ck('duplicate_occurrences_not_merged',len(alias['targets'])==len(rows)==2 and {sr[x['source_record_ref']]['pointer'] for x in alias['targets'] if x['source_record_ref'] in sr}=={x[0] for x in rows})
  for t in alias['targets']:
   occurrence=sr[t['source_record_ref']];cc=occurrence['raw_value'];native=t['target_ref'].split(':',1)[1];actual=rawconcerns.get(native)
   mappings=[m for m in p['mappings'] if occurrence['id'] in m['source_refs'] and m['purpose']=='identity'];ck('cc_existing_correspondence_rule_retained',len(mappings)==1 and mappings[0]['rule'] is not None and any(sr[x]['pointer'].startswith('/correspondence/') and sr[x]['raw_value'].get('target')==[native] for x in mappings[0]['source_refs'] if sr[x]['file']==str(B/'step7-concerns.json')))
   ck('duplicate_identity_detail',bool(actual) and actual[1]['name']==cc['cc'] and actual[1].get('detail','')==cc.get('cc_detail',''),target=t['target_ref'])
   if actual:
    parent=get(tax,actual[0].rsplit('/items/',1)[0]);ck('cc_group_scope',sc[t['scope_ref']]['axes']['concern']['included']==['concern:'+parent['id']])
 for cid,bad in [('ANCHOR-10','P9-3'),('ANCHOR-11','P9-1')]:
  cs=cases[cid];ck('stretch_correct_group',all(sc[x]['axes']['concern']['included']==['concern:P9-4'] for x in cs['scope_refs']))
  ck('stretch_existing_wrong_link_retained',sr[cs['silver_refs'][0]]['raw_value']['condition']['concern_ids']==[bad])
 # Enumerate combinations from source, independent of audit locators or pilot counts.
 expected_combos={};keys=defaultdict(list);arities=Counter();s8=source(str(B/'step8-relations.json'))
 for pi,prob in enumerate(rawcc['problems']):
  for ci,cc in enumerate(prob['complaints']):
   for ki,combo in enumerate(cc.get('combos',[])):
    ptr=f'/problems/{pi}/complaints/{ci}/combos/{ki}';key=f"{prob['problem_id']}:{cc['cc']}#{ki}";expected_combos[ptr]=(combo,key);keys[key].append(ptr);arities[len(combo['combo'])]+=1
 actual_combos={sr[x['source_record_ref']]['pointer']:x for x in p['relation_claims'] if x['source_record_ref'] in sr and sr[x['source_record_ref']]['file']==str(RAW/'problem-packages.json')}
 ck('combos_full_146',len(expected_combos)==146 and set(expected_combos)==set(actual_combos));ck('source_arity_distribution',dict(arities)=={2:119,1:21,3:6},observed=dict(arities))
 for ptr,(co,key) in expected_combos.items():
  r=actual_combos.get(ptr)
  if not r:continue
  ck('combo_raw_members_and_order',len(co['combo'])==r['arity'] and [sr[m['source_ref']]['raw_value'] for m in r['members']]==co['combo'],pointer=ptr)
  ck('combo_members_unresolved',all(mp[m['mapping_ref']]['state']=='unresolved' and not mp[m['mapping_ref']]['candidates'] and not mp[m['mapping_ref']]['selected_refs'] for m in r['members']))
  exp=[v for v in s8['claims'] if v.get('source')=='problem-packages.complaints[].combos' and v.get('source_index')==key]
  ck('existing_expansions_complete',{v['id'] for v in exp}=={v['id'] for v in r['existing_expansions']})
  for e in r['existing_expansions']:
   ck('duplicate_expansion_not_first_match',e['origin_state']==('exact' if len(keys[key])==1 else 'ambiguous') and {sr[x]['pointer'] for x in e['source_occurrence_refs']}==set(keys[key]),id=e['id'])
   ck('nary_expansion_parent_arity',e['source_arity']==r['arity'])
 # Seven note links fixed to known existing R8 rows and independently checked source members/reason.
 expected_notes={109:('R8-0277','/problems/1/complaints/3/combos/0'),110:('R8-0278','/problems/1/complaints/3/combos/1'),111:('R8-0279','/problems/1/complaints/3/combos/2'),132:('R8-0298','/problems/3/complaints/3/combos/0'),133:('R8-0299','/problems/3/complaints/3/combos/1'),134:('R8-0300','/problems/3/complaints/4/combos/0'),135:('R8-0301','/problems/3/complaints/4/combos/1')}
 ck('note_links_denominator',len(p['notes'])==7)
 for ni,(native,ptr) in expected_notes.items():
  ns=[n for n in p['notes'] if sr[n['source_record_ref']]['pointer']==f'/step8_notes/{ni}'];ck('note_exactly_once',len(ns)==1,note=ni)
  if not ns:continue
  n=ns[0];co=get(rawcc,ptr);ev=n['existing_claim_refs'];ck('note_claim_witness',len(ev)==1 and ev[0]['id']==native and sr[ev[0]['source_record_ref']]['raw_value']['id']==native and sr[ev[0]['source_record_ref']]['raw_value']['reason']==co['reason'] and [sr[x]['pointer'] for x in n['source_refs']]==[ptr] and len(n['claim_refs'])==1 and n['claim_refs']==[rr[n['relation_ref']]['claim_ref']],note=ni)
 # Precise conditional timing: same-day and first must have independent source evidence.
 order=[r for r in p['relation_claims'] if r['relation_kind']=='timing'];ck('timing_once',len(order)==1)
 if order:
  r=order[0];f=r['field_conditions'];ck('field_condition_keys',set(f)=={'same_day','first','days'})
  ck('staff_check_preserved',cl[r['claim_ref']]['review_state']=='staff_check' and s8['claims'][0]['review_status']=='staff_check' and not any(r['claim_ref'] in x['input_claim_refs'] for x in p['resolutions']))
  ck('endpoint_a_M1_b_M2',[mp[x['mapping_ref']]['selected_refs'] for x in r['members']]==[['family:M1'],['family:M2']])
  if set(f)=={'same_day','first','days'}:
   ck('same_day_true_independent',f['same_day']['value'] is True and f['same_day']['options'] is None and sr[f['same_day']['raw_ref']]['pointer']=='/rules/0/interval')
   ck('unknown_site_no_first',f['first']['value'] is None and sc[f['first']['scope_ref']]['axes']['site_relation']['knowledge']=='unknown')
   branches=f['first']['options'] or [];observed={tuple(sc[x['scope_ref']]['axes']['site_relation']['included']):x['value'] for x in branches}
   ck('first_branches_preserved',observed=={('same_site',):'a',('different_site',):'explicit_no_required_order'} and len(branches)==2)
   ck('branch_source_evidence',all(sr[x['raw_ref']]['pointer']=='/rules/0/note' and '동일 부위는 보톡스 먼저' in sr[x['raw_ref']]['raw_value'] and '주입 부위가 다르면 순서 무관' in sr[x['raw_ref']]['raw_value'] for x in branches))
   ck('days_not_invented',f['days']['value'] is None and f['days']['options'] is None)
 # Candidates: preserve eight units and no invented palja application approval.
 for cid,ci,mi in [('CAND-volume',2,0),('CAND-wrinkle',1,1)]:
  cs=cases[cid];m=mp[cs['mapping_refs'][0]];member=get(source(str(B/'step7-concerns.json')),('/combos/72/members/0' if ci==2 else '/combos/71/members/1'))
  ck('comparison_candidate_exact',m['rule'] is not None and m['state']=='ambiguous' and [x['target_ref'] for x in m['candidates']]==['unit_procedure:'+u for u in member['units']] and len(m['candidates'])==8 and not m['selected_refs'])
  ck('comparison_scope_unresolved',sc[m['scope_ref']]['axes']['site']['knowledge']=='unknown' and sc[m['scope_ref']]['container_scope_ref'] in sc)
  ck('comparison_raw_member',cl[cs['claim_refs'][0]]['raw_value']==source(str(RAW/'procedure-comparison.json'))['comparisons'][ci]['procedures'][mi])
 cs=cases['PRODUCT-SCOPE-01'];c=cl[cs['claim_refs'][0]];m=mp[cs['mapping_refs'][0]];existing=source(str(B/'step5-units.json'))['product_links'][243];ov=c['override'];ck('product_compatibility_not_selection',m['rule'] is not None and m['state']=='compatible_candidate' and not m['selected_refs'] and [x['target_ref'] for x in m['candidates']]==['unit_procedure:'+x for x in existing['inherited_candidates']])
 ck('override_M4_scope_metadata',ov is not None and ov['override_of']=='family:M4' and ov['priority']==1 and ov['level']==existing['side_effect_override'][0]['level'] and sc[ov['scope_ref']]['axes']['family']['included']==['family:M4'] and sr[ov['source_record_ref']]['raw_value']==existing and ov['decision_ref'] is None)
 for cid,ix in [('PROJECTION-K8-0028',2),('PROJECTION-K8-0029',3)]:
  cs=cases[cid];v=source(str(B/'step8-relations.json'))['conditions']['not_condition'][ix];c=cl[cs['claim_refs'][0]];s=sc[c['scope_ref']];ck('K8_metadata_preserved',sr[cs['silver_refs'][0]]['raw_value']==v and c['subject_ref']==v['target'] and c['kind']==('preparation' if ix==2 else 'counseling') and s['axes']['patient_conditions']['knowledge']=='not_applicable' and s['axes']['patient_conditions']['included']==[])
 cs=cases['ORIGIN-CC-01'];s=sc[cs['scope_refs'][0]];ck('palja_neck_conflict_unresolved',s['application_state']=='unknown' and s['conflicts'] and s['conflicts'][0]['container']=='팔자주름' and s['conflicts'][0]['statement']=='목주름' and cl[cs['claim_refs'][0]]['review_state']=='source_conflict')
 cs=cases['PATIENT-LANG-01'];variants=[cl[x] for x in cs['claim_refs']];rawlang=source(str(RAW/'literature-evidence.json'))['categories']['M2']['adverse_effects'][2]
 ck('language_variants_all_five',len(variants)==5 and Counter(x['language'] for x in variants)==Counter({'en':2,'ko':1,'zh':1,'ja':1}) and {x['raw_value'] for x in variants}=={rawlang[k] for k in ['statement','patient_ko','patient_en','patient_zh','patient_ja']})
 ck('language_subject_identity',all(x['subject_ref']=='evidence_statement:ST-M2-adverse_effects-03' for x in variants))
 ck('ko_delayed_qualifier_preserved',any(x['language']=='ko' and '몇 개월 후에 지연성' in x['raw_value'] and x['variant']['equivalence']=='unreviewed' for x in variants))
 cs=cases['RESOLUTION-01'];ck('duration_two_claims',len(cs['claim_refs'])==2 and [cl[x]['raw_value'] for x in cs['claim_refs']]==['3-6개월 유지, 정기적 시술로 지속 효과','6-9개월']);ck('only_real_resolution',len(p['resolutions'])==1)
 for cid in cs['claim_refs']:
  c=cl[cid];m=mp[c['mapping_refs'][0]] if c['mapping_refs'] else None;ck('duration_source_identity_mapping',c['subject_ref']=='product:M10-1-1' and m is not None and m['state']=='exact' and m['selected_refs']==['product:M10-1-1'] and any(sr[x]['file']==str(B/'step9-explanations.json') and sr[x]['pointer'].startswith('/records/') and sr[x]['raw_value']['attach']['nodes']==['product:M10-1-1'] and sr[x]['raw_value']['text']==c['raw_value'] for x in m['source_refs']))
 if p['resolutions']:
  r=p['resolutions'][0];slot=source(str(B/'step9-explanations.json'))['node_slots'][280]
  ck('duration_resolution_policy',r['state']=='conservative' and r['input_claim_refs']==cs['claim_refs'] and r['output']['selected_claim_ref']==cs['claim_refs'][0] and r['alternatives']==[cs['claim_refs'][1]] and r['output']['value']==cl[cs['claim_refs'][0]]['raw_value'] and r['policy']['id']=='D9-3' and r['policy']['code_sha256']==sha(B/'step9-apply.py') and sr[r['output']['existing_slot_ref']]['raw_value']==slot and not r['clinical_consensus'])
  ck('resolution_unknown_stays_unknown',r['unknown_branch']=={'conditions':'unknown','clinical_approval':None})
 # Coverage values are tied to independent source counts, not just generated artifacts.
 expected_cov={'raw_files_inventory':len(list(RAW.glob('*.json'))),'case_evidence_rows':42,'safety_collision_rows':3,'safety_original_fields':6,'safety_leaves':16,'previously_lost_leaves':10,'duplicate_cc_occurrences':4,'duplicate_cc_keys':2,'cc_combos':len(expected_combos),'cc_combos_arity':{str(k):v for k,v in sorted(arities.items())},'note_links':7,'comparison_members':2,'language_variants':5,'duration_source_claims':2}
 ck('coverage_denominators',all(p['coverage'][k]==v for k,v in expected_cov.items()))
 if graph is not None:
  ck('projection_matches_records',graph==project(p))
  ck('no_automatic_confirmed_edges',all(x['kind']=='fact_attachment' and x['application_state']=='unknown' for x in graph.get('edges',[])))
  ck('claim_scope_mapping_not_nodes',{x['type'] for x in graph.get('nodes',[])}<={x['id'] for x in design['types'] if x['gold_node']})
 return checks

def safe_validate(p,graph=None):
 try:return validate(p,graph)
 except Exception as e:return [{'check':'rejected_invalid_references_or_values','pass':False,'error':type(e).__name__+': '+str(e)}]
def mutation_tests(p):
 tests=[]
 assert all(x['pass'] for x in safe_validate(copy.deepcopy(p),project(p))), 'Positive control failed before mutations'
 def test(name,mut):
  changed=copy.deepcopy(p);mut(changed);results=safe_validate(changed,project(changed));fails=[x['check'] for x in results if not x['pass']];tests.append({'mutation':name,'rejected':bool(fails),'failed_checks':list(dict.fromkeys(fails))[:12]})
 def case(p,cid):return next(x for x in p['cases'] if x['id']==cid)
 def item(p,g,rid):return next(x for x in p[g] if x['id']==rid)
 def cc(p,cid):return item(p,'claims',case(p,cid)['claim_refs'][0])
 test('alias_merge_overwrites_original_list',lambda p:cc(p,'LOSS-01').update(raw_value=['시술 부위 발적','일시적 부종']))
 test('drop_whole_alias_source_claim',lambda p:p['claims'].remove(cc(p,'LOSS-03')))
 test('same_name_first_match_wrong_scope',lambda p:item(p,'scopes',case(p,'ANCHOR-10')['scope_refs'][0])['axes']['concern'].update(included=['concern:P9-3']))
 test('collapse_duplicate_legacy_occurrence',lambda p:p['legacy_aliases'][0]['targets'].pop())
 test('duplicate_legacy_auto_selection',lambda p:p['legacy_aliases'][0].update(selected_refs=[p['legacy_aliases'][0]['targets'][0]['target_ref']]))
 test('singleton_promoted_to_pair',lambda p:next(r for r in p['relation_claims'] if r['arity']==1).update(relation_kind='source_combo',direction='symmetric'))
 test('nary_member_deleted',lambda p:next(r for r in p['relation_claims'] if r['arity']==3)['members'].pop())
 test('note_claim_reference_deleted',lambda p:p['notes'][0].update(claim_refs=[]))
 test('note_wrong_R8',lambda p:p['notes'][0]['existing_claim_refs'][0].update(id='R8-0001'))
 def timing(p):return next(x for x in p['relation_claims'] if x['relation_kind']=='timing')
 test('first_condition_deleted',lambda p:timing(p)['field_conditions'].pop('first'))
 test('first_unconditional_a',lambda p:timing(p)['field_conditions']['first'].update(value='a',options=None))
 test('explicit_no_order_conflated_with_not_declared',lambda p:timing(p)['field_conditions']['first']['options'][1].update(value='not_declared'))
 test('same_site_endpoint_swap',lambda p:timing(p)['members'].reverse())
 test('candidate_promoted_to_selected',lambda p:item(p,'mappings',case(p,'CAND-volume')['mapping_refs'][0]).update(state='selected',selected_refs=['unit_procedure:U5-082']))
 test('product_M4_override_extended_to_M2',lambda p:item(p,'scopes',case(p,'PRODUCT-SCOPE-01')['scope_refs'][0])['axes']['family'].update(included=['family:M2']))
 test('staff_check_promoted_to_confirmed',lambda p:cc(p,'SCOPE-ORDER-01').update(review_state='confirmed'))
 test('palja_neck_conflict_erased',lambda p:item(p,'scopes',case(p,'ORIGIN-CC-01')['scope_refs'][0]).update(conflicts=[],application_state='explicit'))
 test('ko_qualifier_omitted',lambda p:next(c for c in p['claims'] if c['language']=='ko').update(raw_value='알레르기 반응은 드뭅니다.'))
 test('duration_alternative_erased',lambda p:p['resolutions'][0].update(alternatives=[]))
 test('policy_promoted_to_clinical_consensus',lambda p:p['resolutions'][0].update(clinical_consensus=True))
 test('wrong_source_hash',lambda p:p['snapshots'][0]['files'][0].update(sha256='0'*64))
 test('wrong_source_pointer',lambda p:p['source_records'][0].update(pointer='/no_such_field'))
 test('existing_mapping_rule_dropped',lambda p:item(p,'mappings',case(p,'CAND-volume')['mapping_refs'][0]).update(rule=None))
 test('unknown_extra_field',lambda p:p['mappings'][0].update(approval=True))
 test('invalid_enum',lambda p:p['scopes'][0].update(application_state='approved'))
 test('null_instead_of_empty_selected_list',lambda p:p['mappings'][0].update(selected_refs=None))
 test('missing_required_raw_field',lambda p:p['claims'][0].pop('raw_field'))
 test('identity_from_name',lambda p:p['entities'][0].update(id='product:코어톡스'))
 test('duration_fake_reviewer',lambda p:p['decisions'][0]['authority'].update(reviewer='invented reviewer'))
 test('ambiguous_expansion_first_match',lambda p:next(e for r in p['relation_claims'] for e in r['existing_expansions'] if e['origin_state']=='ambiguous').update(origin_state='exact'))
 g=project(p);g['edges'].append({'id':'bad','kind':'procedure_pair','from':'unit_procedure:U5-082','to':'unit_procedure:U5-018','application_state':'explicit'});failed=[x['check'] for x in safe_validate(p,g) if not x['pass']];tests.append({'mutation':'automatic_confirmed_graph_edge','rejected':bool(failed),'failed_checks':failed})
 return tests
if __name__=='__main__':
 p=read(O/'pilot.json');g=read(O/'graph-projection.json');checks=safe_validate(p,g)
 for f in read(O/'inputs-start.json'):
  checks.append({'check':'input_start_end_hash','pass':Path(f['file']).is_file() and sha(f['file'])==f['sha256'] and Path(f['file']).stat().st_size==f['bytes'],'file':f['file']})
 mutations=mutation_tests(p);checks.append({'check':'schema_artifact_matches_declarative_contract','pass':read(O/'schema.json')==SCHEMA});end=[{'file':x['file'],'sha256':sha(x['file']),'bytes':Path(x['file']).stat().st_size} for x in read(O/'inputs-start.json')];write('inputs-end.json',end)
 out={'scope':'Pilot source fidelity, referential and conditional integrity only; no clinical or full-migration approval','passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'mutations_rejected':sum(x['rejected'] for x in mutations),'mutation_total':len(mutations),'checks':checks,'mutations':mutations,'coverage':p['coverage']};write('validation.json',out)
 print(json.dumps({k:out[k] for k in ['passed','failed','mutations_rejected','mutation_total']}));print(json.dumps([x for x in checks if not x['pass']],ensure_ascii=False));sys.exit(bool(out['failed'] or out['mutations_rejected']!=len(mutations)))
