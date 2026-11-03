"""Declarative strict pilot schema and a dependency-free JSON Schema subset validator."""
from common import *
def typ(t,**k):return {'type':t,**k}
S=typ('string');N=typ('null');J={};I=typ('integer',minimum=1);BOOL=typ('boolean')
def nullable(s):return {'anyOf':[s,N]}
def enum(*v):return {'enum':list(v)}
def arr(s,min=0):return typ('array',items=s,minItems=min)
def obj(**props):return typ('object',properties=props,required=list(props),additionalProperties=False)
def dictionary(s):return typ('object',additionalProperties=s)
REF=typ('string',minLength=1)
RULE=obj(id=REF,version=S,code_sha256=typ('string',pattern='^[0-9a-f]{64}$'))
FILE=obj(file=REF,sha256=typ('string',pattern='^[0-9a-f]{64}$'),bytes=typ('integer',minimum=0))
AXIS=obj(knowledge=enum('unknown','explicit','not_applicable','not_declared'),included=arr(S),excluded=arr(S),raw_refs=arr(REF))
QUA=obj(axis=S,raw=J,operator=enum('verbatim'),value=J,source_ref=REF)
CONFLICT=obj(axis=S,container=S,statement=S,source_ref=REF)
CAND=obj(target_ref=REF,role=enum('candidate'),basis=S,exclusion=nullable(S),scope_ref=REF)
EXIST=obj(id=REF,source_record_ref=REF)
BRANCH=obj(scope_ref=REF,value=enum('a','b','explicit_no_required_order','not_declared','unknown'),raw_ref=REF)
COND=obj(scope_ref=REF,value={'anyOf':[BOOL,N,enum('a','b','explicit_no_required_order','not_declared','unknown')]},options=nullable(arr(BRANCH,1)),raw_ref=REF)
INTERVAL=obj(raw=nullable(S),min=nullable(typ('number')),max=nullable(typ('number')),unit=nullable(S),open_high=nullable(BOOL),repeat=J)
T={}
T['snapshots']=obj(id=REF,source_version=nullable(S),files=arr(FILE,1),captured_at=nullable(S),source_kind=enum('raw_snapshot','generated','decision','research'))
T['source_records']=obj(id=REF,snapshot_ref=REF,file=REF,pointer=S,native_id=nullable(S),raw_value=J,parent_ref=nullable(REF),continuity_ref=nullable(REF))
T['entities']=obj(id=REF,type=enum('product','family','site','unit_procedure','concern','evidence_statement'),native_id=REF,source_refs=arr(REF,1))
T['scopes']=obj(id=REF,axes=dictionary(AXIS),container_scope_ref=nullable(REF),statement_qualifiers=arr(QUA),conflicts=arr(CONFLICT),application_state=enum('unknown','conditional','explicit','not_applicable'))
OVERRIDE=obj(claim_refs=arr(REF),predicate=REF,scope_ref=REF,priority=typ('integer'),decision_ref=nullable(REF),override_of=REF,level=S,source_record_ref=REF)
T['claims']=obj(id=REF,kind=enum('explanation','safety','risk','check','preparation','counseling','license','definition','recommendation','operational','price','evidence'),subject_ref=nullable(REF),predicate=REF,raw_field=REF,raw_value=J,normalized_value=J,source_refs=arr(REF,1),scope_ref=REF,mapping_refs=arr(REF),language=nullable(S),variant=obj(of=nullable(REF),equivalence=enum('unreviewed','equivalent','different')),override=nullable(OVERRIDE),review_state=enum('unreviewed','staff_check','confirmed','source_conflict'))
T['relation_claims']=obj(id=REF,claim_ref=REF,members=arr(obj(role=enum('a','b','component'),mapping_ref=REF,source_ref=REF),1),arity=I,relation_kind=enum('single_procedure_attribute','source_combo','timing'),direction=enum('directed','symmetric','not_applicable','unknown'),field_conditions=typ('object',properties={k:COND for k in ['first','same_day','days']},additionalProperties=False),interval=INTERVAL,parent_claim_ref=nullable(REF),derivation=nullable(obj(rule_ref=REF,input_refs=arr(REF,1),projection=S)),existing_expansions=arr(obj(id=REF,source_record_ref=REF,origin_state=enum('exact','ambiguous'),source_occurrence_refs=arr(REF,1),rule_text=S,lowering_text=nullable(S),source_index=S,endpoints_raw=obj(a=J,b=J),source_arity=I)),source_record_ref=REF,expansion_policy=REF)
T['mappings']=obj(id=REF,source_refs=arr(REF,1),purpose=enum('identity','membership','unit_compatibility','normalization','attachment','classification'),state=enum('exact','rule_mapped','ambiguous','unresolved','excluded','compatible_candidate','selected'),candidates=arr(CAND),selected_refs=arr(REF),rule=nullable(RULE),scope_ref=REF,decision_refs=arr(REF),reason=REF)
T['decisions']=obj(id=REF,target_refs=arr(REF,1),status=enum('proposed','approved','rejected','needs_source','needs_staff','superseded'),authority=obj(kind=enum('human','approved_rule'),reviewer=nullable(S)),reason=REF,source_refs=arr(REF,1),decided_at=nullable(S),supersedes=arr(REF))
T['resolutions']=obj(id=REF,input_claim_refs=arr(REF,1),scope_ref=REF,policy=obj(id=REF,version=S,code_sha256=typ('string',pattern='^[0-9a-f]{64}$'),decision_ref=REF),output=obj(selected_claim_ref=REF,value=J,existing_slot_ref=REF),alternatives=arr(REF),state=enum('single_source','same','conservative','conditional','staff_check','unresolved'),clinical_consensus=BOOL,unknown_branch=J)
T['attachments']=obj(id=REF,claim_refs=arr(REF,1),target_ref=REF,rule=obj(id=REF,version=S),witness=arr(obj(mapping_ref=nullable(REF),edge_ref=nullable(REF),component_ref=nullable(REF),source_ref=REF)),scope_ref=REF,application_state=enum('unknown','candidate','explicit','conditional','excluded'),resolution_ref=nullable(REF),unknown_reasons=arr(S))
T['legacy_aliases']=obj(namespace=enum('problem-packages.cc'),snapshot_ref=REF,alias=REF,state=enum('ambiguous'),selected_refs=arr(REF),targets=arr(obj(source_record_ref=REF,target_ref=REF,scope_ref=REF),2))
T['notes']=obj(id=REF,source_record_ref=REF,source_refs=arr(REF,1),claim_refs=arr(REF,1),existing_claim_refs=arr(EXIST,1),relation_ref=REF,application_state=enum('unknown'))
T['cases']=obj(id=REF,group=REF,evidence_refs=arr(REF,1),source_refs=arr(REF,1),silver_refs=arr(REF,1),claim_refs=arr(REF),relation_refs=arr(REF),mapping_refs=arr(REF),scope_refs=arr(REF),attachment_refs=arr(REF),note_refs=arr(REF),status=enum('represented_unreviewed'))
SCHEMA=obj(schema_version=enum('silver-design-pilot/1'),basis=obj(file=REF,sha256=typ('string',pattern='^[0-9a-f]{64}$'),status=enum('proposal_only')),**{k:arr(v) for k,v in T.items()},coverage=obj(raw_files_inventory=I,case_evidence_rows=I,safety_collision_rows=I,safety_original_fields=I,safety_leaves=I,previously_lost_leaves=I,duplicate_cc_occurrences=I,duplicate_cc_keys=I,cc_combos=I,cc_combos_arity=dictionary(I),note_links=I,comparison_members=I,language_variants=I,duration_source_claims=I,unstarted=REF))
SCHEMA['$schema']='https://json-schema.org/draft/2020-12/schema'
SCHEMA['$comment']='Strict pilot structural contract; validate.py supplies source, type-specific refs, and conditional invariants. null means unknown/absent computation as field documented; [] is explicit empty list, never universal permission. No entity clinical approval implied.'
def structural(value,schema=SCHEMA,path='$'):
 errors=[]
 if 'anyOf' in schema:
  if not any(not structural(value,s,path) for s in schema['anyOf']):errors.append(path+': no anyOf match')
  return errors
 if 'enum' in schema and not any(type(value)==type(x) and value==x for x in schema['enum']):errors.append(path+': enum')
 if 'type' in schema:
  t=schema['type'];ok={'string':isinstance(value,str),'null':value is None,'object':isinstance(value,dict),'array':isinstance(value,list),'integer':type(value)==int,'number':type(value) in (int,float),'boolean':type(value)==bool}[t]
  if not ok:return errors+[path+': type '+t]
 if isinstance(value,dict):
  props=schema.get('properties',{});additional=schema.get('additionalProperties',True)
  for k in schema.get('required',[]):
   if k not in value:errors.append(path+': missing '+k)
  for k,v in value.items():
   if k in props:errors.extend(structural(v,props[k],path+'.'+k))
   elif additional is False:errors.append(path+': unknown '+k)
   elif isinstance(additional,dict):errors.extend(structural(v,additional,path+'.'+k))
 if isinstance(value,list):
  if len(value)<schema.get('minItems',0):errors.append(path+': minItems')
  for i,v in enumerate(value):errors.extend(structural(v,schema.get('items',{}),path+f'[{i}]'))
 if type(value) in (int,float) and value<schema.get('minimum',float('-inf')):errors.append(path+': minimum')
 if isinstance(value,str):
  if len(value)<schema.get('minLength',0):errors.append(path+': minLength')
  if 'pattern' in schema and not re.search(schema['pattern'],value):errors.append(path+': pattern')
 return errors
if __name__=='__main__':write('schema.json',SCHEMA)
