"""Independent source/typed-contract checks; never imports the builder or identity.py."""
from common import *
from ref_contract import REFS, ATTACHMENT_RULE

def inspect(p):
 out=[]
 def ck(name,ok,**detail):out.append({'check':name,'pass':bool(ok),**detail})
 idx={g:{r['id']:r for r in rows if 'id' in r} for g,rows in p.items() if isinstance(rows,list)}
 def paths(obj,parts,path):
  if not parts:
   if obj is not None:yield path,obj
   return
  if obj is None:return
  head,*tail=parts
  if head=='*':
   for key,val in (enumerate(obj) if isinstance(obj,list) else obj.items()):yield from paths(val,tail,path+'/'+str(key))
  elif head in obj:yield from paths(obj[head],tail,path+'/'+head)
 for group,fields in REFS.items():
  for i,r in enumerate(p[group]):
   for field,target_type in fields.items():
    for path,target in paths(r,field.split('.'),'/'+group+'/'+str(i)):
     ck('typed_ref',target in idx[target_type],path=path,target=target,target_type=target_type,reason='reachable' if target in idx[target_type] else 'wrong_type_or_missing')
 for i,s in enumerate(p['scopes']):
  for name,ax in s['axes'].items():
   if ax['value_kind']=='entity_refs':
    for field in ['included','excluded']:
     for j,target in enumerate(ax[field]):
      ck('typed_ref',target in idx['entities'],path=f'/scopes/{i}/axes/{name}/{field}/{j}',target=target,target_type='entities',reason='reachable' if target in idx['entities'] else 'wrong_type_or_missing')
      ck('axis_entity_namespace',name=='target' or target.split(':')[0]==name,path=f'/scopes/{i}/axes/{name}',target=target)
 # Detect cycles even when a rehashed malformed graph also contains missing refs.
 for scope_record in p['scopes']:
  seen=set();node=scope_record['id']
  while node in idx['scopes'] and node not in seen:
   seen.add(node);node=idx['scopes'][node]['container_scope_ref']
  ck('scope_parent_acyclic',node not in seen,scope=scope_record['id'])
 # No dependent lookup after missing refs: diagnostics remain structured and complete.
 if any(not x['pass'] for x in out):return out
 sr=idx['source_records'];sc=idx['scopes'];cl=idx['claims'];mp=idx['mappings'];rr=idx['relation_claims']
 files_cache={}
 def source_file(file):
  if file not in files_cache:files_cache[file]=read(file)
  return files_cache[file]
 def raw(r):return get(source_file(r['file']),r['pointer'])
 # State invariants apply to every declared axis, including future pilot axes.
 owners={sid:[] for sid in sc}
 for group in ['claims','mappings']:
  for record in p[group]:owners[record['scope_ref']].extend(record['source_refs'])
 comparison_members={}
 for claim_record in p['claims']:
  origin=sr[claim_record['source_refs'][0]]
  if origin['logical_file_key']=='procedure-comparison.json' and '/procedures/' in origin['pointer']:
   comparison_members[claim_record['scope_ref']]=origin
 for sid,scope_record in sc.items():
  axes=scope_record['axes'];parent=scope_record['container_scope_ref']
  for name,axis in axes.items():
   included=axis['included'];excluded=axis['excluded'];state=axis['knowledge']
   expected_state='not_applicable' if name=='patient_conditions' else 'unknown' if name in ['site','statement_site'] or (name=='site_relation' and not included) else 'explicit'
   ck('scope_axis_source_knowledge',state==expected_state,scope=sid,axis=name)
   evidence=axis['raw_refs']+owners[sid]
   ck('scope_axis_disjoint',not set(included)&set(excluded),scope=sid,axis=name)
   # cc and cc_group are positional source roles; three real rows repeat the literal.
   source_roles=False
   if name=='container' and len(axis['raw_refs'])==1:
    origin=sr[axis['raw_refs'][0]];value=raw(origin)
    source_roles=origin['logical_file_key']=='problem-packages.json' and isinstance(value,dict) and 'cc' in value and included==[value['cc'],value.get('cc_group','')]
   ck('scope_axis_unique', (len(included)==len(set(included)) or source_roles) and len(excluded)==len(set(excluded)),scope=sid,axis=name)
   ck('scope_axis_knowledge_values',bool(evidence) and (bool(included or excluded) if state=='explicit' else not (included or excluded) if state in ['not_declared','not_applicable'] else True),scope=sid,axis=name)
  if sid in comparison_members:
   origin=comparison_members[sid];root=origin['pointer'].rsplit('/procedures/',1)[0]
   context=sc.get(parent,{});context_axes=context.get('axes',{})
   roots=[r['id'] for r in sr.values() if r['snapshot_ref']==origin['snapshot_ref'] and r['logical_file_key']==origin['logical_file_key'] and r['pointer']==root]
   expected={'container':{'knowledge':'explicit','included':[get(source_file(origin['file']),root)['subtitle']],'excluded':[],'raw_refs':roots,'value_kind':'source_literals'}}
   ck('scope_parent_source_context',parent!=sid and context.get('container_scope_ref') is None and context_axes==expected and context.get('application_state')=='unknown',scope=sid)
   ck('comparison_axis_source_state',axes=={'site':{'knowledge':'unknown','included':[],'excluded':[],'raw_refs':[origin['id']],'value_kind':'entity_refs'}},scope=sid)
  else:ck('scope_parent_source_context',parent is None,scope=sid)
 # Frozen declared fingerprints, independent of values emitted by build.py.
 ck('attachment_rule_declaration',read(O/'ref-contract.json').get('attachment_rule')==ATTACHMENT_RULE)
 for key,file in [('implementation_sha256','build.py'),('contract_sha256','contract.md')]:
  ck('attachment_rule_fingerprint',ATTACHMENT_RULE[key]==sha(O/file),file=file)
 for s in p['snapshots']:
  expected_kind={'raw21':'raw_snapshot','generated-silver':'generated','decision-artifact':'decision'}[s['domain']]
  ck('snapshot_domain_kind',s['source_kind']==expected_kind and s['collection']=='procedure-hub/'+s['domain'])
  manifest=sorted([[f['logical_file_key'],sha(f['file'])] for f in s['files']])
  ck('collection_snapshot_id',s['id']=='snap:'+digest([s['domain'],s['collection'],manifest]))
  ck('logical_file_unique',len({f['logical_file_key'] for f in s['files']})==len(s['files']))
  if s['domain']=='raw21':
   root=Path(read(A/'inventory.json')['roots']['raw'])
   ck('raw21_full_manifest',manifest==sorted([[str(f.relative_to(root)),sha(f)] for f in root.rglob('*.json')]) and len(manifest)==21)
 for r in p['source_records']:
  val=raw(r);native=str(val.get('id',val.get('ledger_id'))) if isinstance(val,dict) and (val.get('id') or val.get('ledger_id')) else None
  ck('source_native_id',r['native_id']==native,source=r['id'])
  snap=idx['snapshots'][r['snapshot_ref']]
  ck('source_logical_locator',any(f['logical_file_key']==r['logical_file_key'] and f['file']==r['file'] for f in snap['files']))
  ck('occurrence_id_v2',r['id']=='src:'+digest([r['snapshot_ref'],r['logical_file_key'],r['pointer']]))
 for group in ['scopes','mappings','claims','relation_claims','notes','decisions','resolutions','attachments']:
  for r in p[group]:
   expected=r['id'].split(':')[0]+':'+digest([p['schema_version'],p['mapping_rule_revision'],{k:v for k,v in r.items() if k!='id'}])
   ck('normalized_revision_id',r['id']==expected,group=group,record=r['id'])
 for c in p['claims']:
  origin=sr[c['source_refs'][0]];ptr=origin['pointer'];val=raw(origin);scope=sc[c['scope_ref']]
  if 'literature-evidence.json'==origin['logical_file_key']:
   ck('language_scope_family',scope['axes']=={'family':{'knowledge':'explicit','included':['family:'+ptr.split('/')[2]],'excluded':[],'raw_refs':[],'value_kind':'entity_refs'}} and ptr.split('/')[2]=='M2' and scope['container_scope_ref'] is None and scope['application_state']=='unknown')
   ck('language_predicate',c['predicate']==('statement' if ptr.endswith('/statement') else 'patient_explanation'))
   parents=[x['id'] for x in p['claims'] if sr[x['source_refs'][0]]['logical_file_key']==origin['logical_file_key'] and sr[x['source_refs'][0]]['pointer']==ptr.rsplit('/',1)[0]+'/statement']
   ck('language_variant_parent',c['variant']['of']==(None if ptr.endswith('/statement') else parents[0]))
   ck('language_raw_field',c['raw_field']=='/'+ptr.rsplit('/',1)[1])
  if c['override']:
   ov=c['override'];ck('override_claim_predicate',ov['predicate']==c['predicate'] and all(cl[x]['predicate']==ov['predicate'] for x in ov['claim_refs']))
   ck('override_scope_matches_claim',ov['scope_ref']==c['scope_ref'])
 # Source-specific scope rules cover all non-combo fixture kinds too.
 for c in p['claims']:
  origin=sr[c['source_refs'][0]];scope=sc[c['scope_ref']];key=origin['logical_file_key'];ptr=origin['pointer']
  if key=='procedure-comparison.json':
   parent=get(source_file(origin['file']),ptr.rsplit('/procedures/',1)[0]);container=sc.get(scope['container_scope_ref'],{})
   ck('comparison_context_literal',container.get('axes',{}).get('container',{}).get('included')==[parent['subtitle']] and container.get('application_state')=='unknown')
   ck('comparison_member_unknown_scope',scope['application_state']=='unknown' and scope['axes'].get('site',{}).get('knowledge')=='unknown')
   ck('comparison_predicate',c['predicate']=='comparison_member' and c['kind']=='recommendation')
  elif key=='taxonomy.json' and '/extracted/safety/' in ptr:
   ck('safety_scope_explicit_source',scope['application_state']=='explicit' and scope['axes'].get('family',{}).get('knowledge')=='explicit')
  elif c['predicate']=='onset_duration.duration':
   ck('duration_source_scope',scope['axes'].get('product',{}).get('included')==['product:M10-1-1'] and scope['application_state']=='unknown')
  if key=='problem-packages.json' and '/combos/' in ptr:
   ck('combo_predicate_source',c['predicate']=='combo_source_statement' and c['kind']=='recommendation')
  if c['kind'] in ['preparation','counseling']:
   ck('K8_scope_not_patient_approval',scope['application_state']=='not_applicable' and c['predicate']==c['kind'])
 for r in p['relation_claims']:
  source=sr[r['source_record_ref']];ptr=source['pointer']
  ck('relation_claim_same_source',r['source_record_ref'] in cl[r['claim_ref']]['source_refs'])
  if source['logical_file_key']=='problem-packages.json':
   container=get(source_file(source['file']),ptr.rsplit('/combos/',1)[0]);scope=sc[cl[r['claim_ref']]['scope_ref']]
   ck('combo_container_scope',scope['axes'].get('container',{}).get('included')==[container['cc'],container.get('cc_group','')] and scope['axes'].get('container',{}).get('knowledge')=='explicit')
   roots=[x['id'] for x in sr.values() if x['snapshot_ref']==source['snapshot_ref'] and x['logical_file_key']==source['logical_file_key'] and x['pointer']==ptr.rsplit('/combos/',1)[0]]
   expected_axes={'container':{'knowledge':'explicit','included':[container['cc'],container.get('cc_group','')],'excluded':[],'raw_refs':roots,'value_kind':'source_literals'},'statement_site':{'knowledge':'unknown','included':[],'excluded':[],'raw_refs':[source['id']],'value_kind':'none'}}
   ck('combo_scope_source_axes',scope['axes']==expected_axes and scope['container_scope_ref'] is None)
   ck('combo_unknown_scope_preserved',scope['application_state']=='unknown' and scope['axes'].get('statement_site',{}).get('knowledge')=='unknown')
   ck('combo_direction_unpromoted',r['direction']==('not_applicable' if r['arity']==1 else 'unknown'))
   ck('combo_interval_not_invented',r['interval']==dict(raw=None,min=None,max=None,unit=None,open_high=None,repeat=None))
  elif r['relation_kind']=='timing':
   val=raw(source)
   ck('timing_interval_no_numeric_invention',r['interval']==dict(raw=val['interval'],min=None,max=None,unit=None,open_high=None,repeat=None))
   ck('timing_direction_unknown',r['direction']=='unknown')
   ck('timing_conditional_scope',all(sc[condition['scope_ref']]['application_state']=='conditional' and all(sc[branch['scope_ref']]['application_state']=='conditional' for branch in condition['options'] or []) for condition in r['field_conditions'].values()))
 for m in p['mappings']:
  if m['rule']:
   rule=m['rule'];file={'step5-apply.py':'step5-units.json','step7-apply.py':'step7-concerns.json','step9-apply.py':'step9-explanations.json'}.get(rule['id'])
   ck('mapping_rule_id_version_hash',file is not None and rule['version']==read(B/file)['version'] and rule['code_sha256']==sha(B/rule['id']))
  sources=[sr[x] for x in m['source_refs']]
  correspondence=[r for r in sources if r['logical_file_key']=='step7-concerns.json' and r['pointer'].startswith('/correspondence/')]
  duration=[r for r in sources if r['logical_file_key']=='step9-explanations.json' and r['pointer'].startswith('/records/')]
  endpoint=[r for r in sources if r['logical_file_key']=='contraindications.json' and r['pointer'] in ['/rules/0/from','/rules/0/to']]
  expected=None
  if correspondence:expected=['concern:'+x for x in raw(correspondence[0])['target']]
  if duration:expected=raw(duration[0])['attach']['nodes']
  if endpoint:expected=['family:'+raw(endpoint[0])]
  if expected is not None:ck('exact_identity_selection_preserved',m['purpose']=='identity' and m['state']=='exact' and m['selected_refs']==expected,mapping=m['id'])
 for d in p['decisions']:
  val=raw(sr[d['source_refs'][0]])
  targets=[c['id'] for c in p['claims'] if c['predicate']=='onset_duration.duration']
  ck('decision_authority_source',d['authority']=={'kind':'approved_rule','reviewer':None} and d['status']=='approved' and d['supersedes']==[] and d['target_refs']==targets and d['reason']==val['decision_ref'] and d['decided_at']==val['decided_at'])
 for resolution in p['resolutions']:
  decision=idx['decisions'][resolution['policy']['decision_ref']]
  origin=sr[decision['source_refs'][0]];value=raw(origin)
  ck('resolution_policy_exact_source_version',origin['logical_file_key']=='step9-decisions.json' and resolution['policy']=={'id':'D9-3','version':str(value['version']),'code_sha256':sha(B/'step9-apply.py'),'decision_ref':decision['id']})
 for a in p['attachments']:
  ck('attachment_declared_rule',a['rule']=={'id':ATTACHMENT_RULE['id'],'version':ATTACHMENT_RULE['version']})
  ck('attachment_rule_source_application',a['application_state']=='unknown' and a['witness']==[] and all(cl[x]['subject_ref']==a['target_ref'] and cl[x]['scope_ref']==a['scope_ref'] for x in a['claim_refs']))
  expected_res=[r['id'] for r in p['resolutions'] if r['scope_ref']==a['scope_ref'] and r['input_claim_refs']==a['claim_refs']]
  ck('attachment_rule_resolution',expected_res==([a['resolution_ref']] if a['resolution_ref'] else []))
  ck('attachment_claim_scope_target',all(cl[x]['scope_ref']==a['scope_ref'] and (cl[x]['subject_ref'] is None or cl[x]['subject_ref']==a['target_ref']) for x in a['claim_refs']))
  for w in a['witness']:
   mapping=mp.get(w['mapping_ref']);edge=rr.get(w['edge_ref'])
   ck('witness_mapping_source_target',mapping is not None and w['source_ref'] in mapping['source_refs'] and a['target_ref'] in mapping['selected_refs']+[c['target_ref'] for c in mapping['candidates']])
   ck('witness_edge_component', (w['edge_ref'] is None and w['component_ref'] is None) or (edge is not None and any(member['mapping_ref']==w['mapping_ref'] and member['source_ref']==w['component_ref']==w['source_ref'] for member in edge['members'])))
 for case in p['cases']:
  ck('case_attachment_consistency',all(set(idx['attachments'][a]['claim_refs'])<=set(case['claim_refs']) for a in case['attachment_refs']),case=case['id'])
 ck('positive_exact_identity8',sum(m['state']=='exact' and m['purpose']=='identity' and bool(m['selected_refs']) for m in p['mappings'])==8)
 ck('positive_candidate_selected0',not any(m['selected_refs'] for m in p['mappings'] if m['state'] in ['ambiguous','compatible_candidate','unresolved']))
 return out
