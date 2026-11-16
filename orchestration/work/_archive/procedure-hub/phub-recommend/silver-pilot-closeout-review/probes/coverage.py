"""Explicit semantic correspondence, with concrete current pointers and typed evidence.
No name-match discovery; raw payload presence never supplies a typed path.
"""
import json,sys,collections
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];B=R.parent;V=B/'silver-design-pilot-v2'
d=json.loads((B/'silver-entity-graph-design/design.json').read_text());p=json.loads((V/'pilot.json').read_text());schema=json.loads((V/'schema.json').read_text())
sr=p['source_records'];cache={}
def read(f):
 if f not in cache:cache[f]=json.loads(Path(f).read_text())
 return cache[f]
def expand(obj,parts,ptr=''):
 if not parts:yield ptr,obj;return
 h,*rest=parts
 if h=='*':
  for k,v in (enumerate(obj) if isinstance(obj,list) else obj.items() if isinstance(obj,dict) else []):yield from expand(v,rest,ptr+'/'+str(k).replace('~','~0').replace('/','~1'))
 elif isinstance(obj,dict) and h in obj:yield from expand(obj[h],rest,ptr+'/'+h.replace('~','~0').replace('/','~1'))
# Current roots and fields are chosen by source meaning, not by proposed name.
roots={'product':('step1-products.json','items/*'),'family':('step2-families.json','families/*'),'subfamily':('step2-families.json','families/*/sub_families/*'),'site':('step3-sites.json','nodes/*'),'technique':('step4-techniques.json','nodes/*'),'unit_procedure':('step5-units.json','units/*'),'package':('step6-packages.json','packages/*'),'concern':('step7-concerns.json','concerns/*/*'),'purpose':('step7-concerns.json','purposes/*'),'combo':('step7-concerns.json','combos/*'),'check_condition':('step8-relations.json','conditions/nodes/*'),'complication':('step8-relations.json','safety/complications/*'),'evidence_statement':('step8-relations.json','evidence/statements/*'),'evidence_source':('step8-relations.json','evidence/literature/*'),'component':('step7-concerns.json','combos/*')}
# An entry (file, pointer pattern) is an observed current source, not a claim
# that its entire proposed target transformation has been implemented.
custom={
'product':{'id':['ledger_id'],'label':['2_names/display_name'],'aliases':['2_names/search_names'],'identity_kind':['1_identity/kind'],'license_claim_refs':['4_license'],'spec_claim_refs':['5_spec'],'company_roles':['6_companies'],'continuity':['active','merged_into','moved_to_procedure'],'family_mapping_refs':[('step2-families.json','product_family/*')],'line_memberships':[('step1-products.json','lines/*'),'line_row']},
'family':{'label':['name'],'aliases':['synonyms'],'definition_claim_refs':['definition','literature_name','name_status','name_basis'],'subfamilies':['sub_families'],'technique_defaults':[('step4-techniques.json','family_defaults/*')],'deferred_refs':['deferred','sub_family_handling']},
'subfamily':{'key':[],'family_ref':[('step2-families.json','families/*/id')],'label':[('step2-families.json','families/*/sub_families/*')],'axis':[]},
'site':{'parent_ref':['parent'],'anatomical_name':['anatomical_name'],'danger_claim_refs':['danger_zone',('step3-sites.json','danger_zone_mapping/*')],'compound_strings':['compound_strings']},
 'technique':{'parent_ref':['parent'],'level':['level'],'medical_name':['medical_name'],'source_expression_refs':['source_expressions',('step4-techniques.json','expressions/*')],'modes':['modes']},
'unit_procedure':{'key':['key'],'site_basis':['site_basis'],'attribute_claim_refs':['attrs','route_status','ops','step4_attrs','dose_range_text','market','side_effect_override'],'product_mapping_refs':['uses_product',('step5-units.json','product_links/*')],'purpose_refs':['purposes'],'candidate_of_refs':['candidate_of']},
'package':{'kind':['kind'],'components':['components',('step6-packages.json','contains/*'),('step6-packages.json','slots/*')],'attribute_claim_refs':['shape','menu_group','same_day_raw','price','description','detail_raw','recommendable']},
'concern':{'label':['name','source_label'],'parent_ref':['parent','subcategory','category'],'related_refs':['related'],'site_refs':['sites'],'source_kind':['node','kind'],'recommendation_claim_refs':[('step7-concerns.json','edges/*'),('step7-concerns.json','correspondence/*')]},
'purpose':{'id':[],'label':['name'],'same_as_concern_ref':['same_as_concern'],'source_expression_refs':['from','aliases']},
'combo':{'kind':['kind'],'anchor_scope_ref':['anchor','site_names','concern_regions'],'components':['components','members','upgrade','schedule'],'copy_claim_refs':['sales_copy','consult_copy','effect','price','products_text','tier'],'relation_claim_refs':[('step8-relations.json','claims/*')]},
'check_condition':{'match_pattern':['match_pattern'],'definition_claim_refs':['sources']},
'complication':{'family_ref':['family'],'severity_claim_refs':['severity','severity_site'],'detail_claim_refs':['incidence','onset','duration','mechanism','management','prevention','risk_factors','evidence']},
'evidence_statement':{'family_ref':['family'],'field_original':['field'],'class_mapping_ref':[('step9-explanations.json','section_map/*')],'variant_claim_refs':['statement','patient'],'evidence_refs':['evidence'],'accuracy_claim_refs':['accuracy_score','accuracy_note','added_at']},
'evidence_source':{'kind':['kind'],'identifiers':['key','pmid','doi','pmc','oa_url'],'bibliography':['title','journal','year','authors'],'verified_at':[]},
'component':{'id':[],'parent_ref':['id'],'role':['components','members','upgrade','schedule'],'ordinal':[],'raw_text':['components','members'],'mapping_ref':[('step6-packages.json','contains/*/unit'),('step6-packages.json','slots/*/candidates')],'quantity':[('step6-packages.json','contains/*/quantity_raw')],'sessions':[('step6-packages.json','contains/*/sessions')],'phase':['schedule'],'scope_ref':['anchor','site_names'],'source_refs':[]},
'value_dictionary':{'key':[('step4-techniques.json','dictionaries/*'),('step9-explanations.json','value_dictionary/*/key')],'label':[('step9-explanations.json','value_dictionary/*/text')],'meaning':[('step9-explanations.json','value_dictionary/*/decision')],'source_refs':[('step9-explanations.json','value_dictionary/*/source')],'constraints':[('step4-techniques.json','unit_procedure_attrs/safe_layers')]}}
# Explicit pilot field correspondence audited against schema and actual records.
records={
'snapshot':('snapshots','id source_version files captured_at source_kind'),
'source_record':('source_records','id snapshot_ref file pointer native_id raw_value parent_ref continuity_ref'),
'scope':('scopes','id axes container_scope_ref statement_qualifiers conflicts application_state'),
'claim':('claims','id kind subject_ref predicate raw_field raw_value normalized_value source_refs scope_ref mapping_refs language variant override review_state'),
'relation_claim':('relation_claims','id claim_ref members arity relation_kind direction field_conditions interval parent_claim_ref derivation'),
'mapping':('mappings','id source_refs purpose state candidates selected_refs rule scope_ref decision_refs'),
'decision':('decisions','id target_refs status authority reason source_refs decided_at supersedes'),
'resolution':('resolutions','id input_claim_refs scope_ref policy output alternatives state clinical_consensus unknown_branch'),
'attachment':('attachments','id claim_refs target_ref rule witness scope_ref application_state resolution_ref unknown_reasons')}
null_contract={('snapshot','source_version'),('snapshot','captured_at'),('source_record','parent_ref'),('source_record','continuity_ref'),('claim','normalized_value'),('relation_claim','parent_claim_ref'),('relation_claim','derivation'),('mapping','decision_refs'),('decision','supersedes'),('attachment','witness')}
uncertain={('purpose','id'),('subfamily','key'),('subfamily','axis')}
limited={'scope.axes':'Pilot axes/knowledge vocabulary differs from design: no subfamily/technique/ingredient/purpose/patient/language/route/time axes; explicit/unknown differ from declared/unresolved. Adoption requires a versioned compatibility decision.', 'source_record.file':'Proposed relative source key maps to logical_file_key; file remains physical locator. These are distinct contracts.', 'claim.subject_ref':'Pilot supports entity or null, not source occurrence as subject.', 'claim.source_refs':'Pilot forces exactly one source although schema declares min1; multi-source not implemented.', 'relation_claim.interval':'Raw timing text preserved; all numeric duration/range normalization remains absent.', 'relation_claim.members':'Inline role/mapping/source members; no standalone component entity.', 'decision.authority':'Only actual approved_rule source is exercised; human approval is unsupported.', 'attachment.witness':'Schema and negative checks only; all real witnesses empty.', 'resolution.output':'One existing duration conservative slot, not all policy/output forms.', 'claim.variant':'Five language leaves from one M2 statement; equivalence stays unreviewed.'}
def origin(t,f):
 if t not in roots and t not in custom:return []
 choices=custom.get(t,{}).get(f)
 if choices is None:
  choices={'id':['id'],'label':['name'],'aliases':['synonyms','aliases'],'status':['status'],'source_refs':[],'decision_refs':[],'revision':[]}.get(f,[])
 rows=[]
 for spec in choices:
  if isinstance(spec,tuple):file,pat=spec
  elif t in roots:file,base=roots[t];pat=base+'/'+spec
  else:continue
  file=str(B/file)
  for ptr,val in expand(read(file),pat.split('/')):
   # Concern logical entities require current node/kind filter; preserve this caveat.
   preserved=[s for s in sr if s['file']==file and (ptr==s['pointer'] or ptr.startswith(s['pointer']+'/'))]
   rows.append({'file':file,'pointer':ptr,'source_kind':'current_silver','value_type':type(val).__name__,'pilot_raw_source_refs':[s['id'] for s in preserved]})
 return rows
entries=[]
for t in d['types']:
 for f in t['fields']:
  tid=t['id'];name=f['name'];key=tid+'.'+name;orig=origin(tid,name);path=None;status='미구현';evidence=[];notes=[]
  if tid in records and name in records[tid][1].split():
   group=records[tid][0];field='logical_file_key' if (tid,name)==('source_record','file') else name
   path=f'{group}[].{field}'
   assert field in schema['properties'][group]['items']['properties']
   vals=[x[field] for x in p[group]];status='계약만' if (tid,name) in null_contract else 'pilot검증'
   evidence=[{'file':str(V/'pilot.json'),'pointer':f'/{group}/{i}/{field}'} for i,x in enumerate(p[group]) if x[field] not in (None,[])][:3]
   if not evidence:evidence=[{'file':str(V/'pilot.json'),'pointer':f'/{group}/0/{field}','null_or_empty_only':True}]
   # Derived records have provenance through their linked source refs, not a
   # claimed pre-existing field. Include concrete source locators as context.
   refs=[]
   for x in p[group]:
    refs.extend(x.get('source_refs',[]));refs.extend([x['source_record_ref']] if x.get('source_record_ref') else [])
   if tid=='snapshot':refs=[x['id'] for x in sr]
   if tid=='source_record':refs=[x['id'] for x in sr]
   origins=[s for s in sr if s['id'] in set(refs)]
   orig=[{'file':x['file'],'pointer':x['pointer'],'source_kind':'record_provenance_context','pilot_raw_source_refs':[x['id']]} for x in origins]
   notes.append('Record field is a pilot contract/derivation; provenance context is not an asserted field-level transformation from every listed source.')
  elif tid in ['product','family','site','unit_procedure','concern','evidence_statement'] and name in ['id','source_refs']:
   path=f'entities[type={tid}].{name}';matches=[(i,x) for i,x in enumerate(p['entities']) if x['type']==tid]
   status='pilot검증' if matches else '계약만'
   evidence=[{'file':str(V/'pilot.json'),'pointer':f'/entities/{i}/{name}'} for i,x in matches][:3]
   if name=='source_refs':
    orig=[{'file':s['file'],'pointer':s['pointer'],'source_kind':'current_silver','pilot_raw_source_refs':[s['id']]} for _,e in matches for ref in e['source_refs'] for s in sr if s['id']==ref]
   notes.append('Only identity/source references; entity properties and full source population are not migrated.')
  elif any(o['pilot_raw_source_refs'] for o in orig):status='원문raw보존만'
  elif not orig:status='계약만'
  if (tid,name) in uncertain:status='의미미확정';notes.append('Requires a source/authority decision, not automatic data inference.')
  if tid=='subfamily' and name=='label':
   notes.append('sub_families elements require value-shape review; no stable subfamily key/label normalization claimed.')
  if tid=='concern':notes.append('Current roots contain non-node entries too; node=true/kind=고민 filtering remains part of the future migration.')
  if key in limited:notes.append(limited[key])
  if key=='evidence_source.verified_at':notes.append('Actual verification time has no confirmed source; do not fabricate a timestamp. This is absence of verification evidence, not uncertain timestamp semantics.')
  entries.append({'proposed':key,'logical_type':tid,'category':t['category'],'is_gold_node':t.get('gold_node',False),'proposed_contract':f,'origin_current_paths':orig[:8],'origin_current_matches':len(orig),'origin_paths_truncated':len(orig)>8,'pilot_raw_preserved_matches':sum(bool(x['pilot_raw_source_refs']) for x in orig),'pilot_typed_path':path,'status':status,'evidence':evidence,'design_evidence_ids':f['evidence'],'limitations':notes,'origin_status':'confirmed_current_or_provenance_context' if orig else 'no_confirmed_current_field_analogue','unconfirmed_origin':not bool(orig)})
assert len(d['types'])==25 and len(entries)==247 and len({e['proposed'] for e in entries})==247
out={'scope':'Current versus unimplemented coverage; neither full migration nor semantic/clinical approval. 42 cases and 146 combos only.','denominator':{'logical_types':25,'proposed_fields':247,'gold_node_types':len(d['nodes'])},'status_definitions':{'pilot검증':'Typed field is exercised in the stated pilot subset; limitations apply.','원문raw보존만':'Mapped current value preserved within source_record.raw_value; no entity typed transformation.','계약만':'Declared only, null/empty only, or no confirmed origin/pilot population; not implemented coverage.','미구현':'Current field confirmed but no pilot typed field or preservation for this correspondence.','의미미확정':'Source/identity/authority decision remains open.'},'summary':{'by_status':dict(collections.Counter(e['status'] for e in entries)),'unconfirmed_origin_fields':sum(e['unconfirmed_origin'] for e in entries),'typed_paths':sum(e['pilot_typed_path'] is not None for e in entries)},'types':[{'id':t['id'],'category':t['category'],'gold_node':t.get('gold_node',False),'fields':sum(e['logical_type']==t['id'] for e in entries),'by_status':dict(collections.Counter(e['status'] for e in entries if e['logical_type']==t['id']))} for t in d['types']],'fields':entries,'source_evidence':d['evidence'],'source_questions_separate_from_implementation':d['questions'],'limitations':['No fieldname-match inference and no raw payload as typed completion.','Concrete locators are checked against local JSON; up to 8 samples per field with full match count.','Current stage files are not automatically original raw: untraced originals remain unconfirmed.','25 logical storage types and 13 proposed Gold node types are separate denominators.','No full safety580 / semantic-pending1277 / duration196slots343alternatives approval.']}
(R/'coverage.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out['summary'],ensure_ascii=False))
