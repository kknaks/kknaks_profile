"""Produce migration, typed-path cardinality and immutable-input evidence in v2 only."""
from common import *
from ref_contract import REFS
from schema import SCHEMA,T
p=read(O/'pilot.json');v1=read(B/'silver-design-pilot/pilot.json')
rows=[]
for group in ['source_records','entities','scopes','claims','relation_claims','mappings','decisions','resolutions','attachments','notes','cases']:
 assert len(v1[group])==len(p[group])
 for old,new in zip(v1[group],p[group]):
  if group=='source_records':assert (old['file'],old['pointer'])==(new['file'],new['pointer'])
  rows.append({'group':group,'v1_id':old['id'],'v2_id':new['id'],'same_identity':old['id']==new['id']})
snaprows=[]
for old in v1['snapshots']:
 files={f['file'] for f in old['files']}
 new=next(s for s in p['snapshots'] if files<={f['file'] for f in s['files']})
 snaprows.append({'v1_id':old['id'],'v2_id':new['id'],'domain':new['domain'],'logical_file_keys':[f['logical_file_key'] for f in new['files'] if f['file'] in files]})
write('migration-map.json',{'record_correspondence':rows,'snapshot_correspondence':snaprows,'field_changes':{'snapshots':'13 file-content snapshots -> 3 domain/collection full manifests, logical_file_key plus physical locator','source_records':'logical_file_key added; snapshot+key+pointer ID replaces physical path identity','normalized_records':'record_schema_version and mapping_rule_revision added; canonical payload revision ID','scope_axes':'value_kind added; per-axis typed schema; no mixed entity/literal/condition axis','projection':'source_fact_lookup and identity_lookup with application unknown separated'},'refinements':['LOSS02 remains unit_procedure:U5-016, not product','nullable rule only with explicit reason; existing evidenced rules cannot be deleted','first options and explicit_no_required_order preserved separately from same_day','override priority/level/override_of and source record preserved','existing R8 pair expansions remain evidence; no new pair lowering'],'canonical_design_changed':False})
paths=[]
for group,fields in REFS.items():
 for field,target in fields.items():
  schema=T[group];cardinality=[]
  for part in field.split('.'):
   if 'anyOf' in schema:
    cardinality.append({'nullable':True});schema=next(x for x in schema['anyOf'] if x.get('type')!='null')
   if part=='*':
    if schema.get('type')=='array':
     cardinality.append({'minItems':schema.get('minItems',0),'maxItems':schema.get('maxItems'),'uniqueItems':False});schema=schema['items']
    else:
     named=list(schema.get('properties',{}).values())
     schema=named[0] if named else schema.get('additionalProperties',{})
     if not isinstance(schema,dict):schema={}
   else:
    cardinality.append({'field':part,'required':part in schema.get('required',[])})
    schema=schema.get('properties',{}).get(part,{})
  if 'anyOf' in schema:cardinality.append({'nullable':True})
  paths.append({'path':group+'.'+field,'target_type':target,'reachability':'required for every non-null value','cardinality':cardinality})
for name in ['product','family','site','unit_procedure','concern','target']:
 for field in ['included','excluded']:paths.append({'path':f'scopes.axes.{name}.{field}.*','target_type':'entities','reachability':'all entries','cardinality':[{'minItems':0}]})
write('ref-contract.json',{'record_refs':paths,'native_ids_not_record_refs':['existing_expansions.id','notes.existing_claim_refs.id'],'rule_identifiers_not_record_refs':['mappings.rule.id','resolutions.policy.id','attachments.rule.id','relation_claims.derivation.rule_ref (derivation forbidden in this pilot)'],'literals_not_record_refs':['cases.evidence_refs','basis.file','source_records.file','snapshots.files.file','container included/excluded','site_relation included/excluded'],'schema':SCHEMA,'note':'schema.json is authoritative cardinality. scope axes use axis-specific schemas; wildcard axes raw_refs have minItems 0.'})
start=read(O/'protected-start.json')
def end(rows):return [{'file':r['file'],'sha256':sha(r['file']),'bytes':Path(r['file']).stat().st_size} for r in rows]
endmanifest={k:end(rows) for k,rows in start.items()};write('protected-end.json',endmanifest)
v1baseline=read(B/'silver-design-pilot/inputs-start.json')
write('immutability.json',{'immutable_files':len(start['immutable']),'immutable_unchanged':start['immutable']==endmanifest['immutable'],'mutable_progress_files':len(start['mutable_progress']),'mutable_progress_changed_during_v2':start['mutable_progress']!=endmanifest['mutable_progress'],'v1_known_progress_mismatches':[{'file':r['file'],'v1_sha256':r['sha256'],'current_sha256':sha(r['file']),'classification':'known coordinator progress update; not retroactively repaired'} for r in v1baseline if Path(r['file']).name=='WORK.md' and sha(r['file'])!=r['sha256']]})
assert start['immutable']==endmanifest['immutable']
