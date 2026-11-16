"""The same 24 review mutations plus the 31 v1 mutations, applied to v2."""
import copy,json
from common import *
import validate as v
import project
p=read(O/'pilot.json')
def dump(name,obj):write(name,obj)
out=[]
def test(name,fn):
 q=copy.deepcopy(p);fn(q);c=v.safe_validate(q,project.project(q));fails=[x for x in c if not x['pass']]
 out.append({'probe':name,'accepted':not fails,'failed_checks':fails[:8]})
def case(q,cid):return next(x for x in q['cases'] if x['id']==cid)
def item(q,group,rid):return next(x for x in q[group] if x['id']==rid)
def claim(q,cid):return item(q,'claims',case(q,cid)['claim_refs'][0])
def scope(q,cid):return item(q,'scopes',case(q,cid)['scope_refs'][0])
def replace_id(q,old,new):
 def walk(x):
  if isinstance(x,dict):
   for k,vv in x.items():x[k]=new if vv==old else walk(vv)
  elif isinstance(x,list):
   for i,vv in enumerate(x):x[i]=new if vv==old else walk(vv)
  return x
 walk(q)
test('positive_control',lambda q:None)
test('decision_dangling_target',lambda q:q['decisions'][0].update(target_refs=['clm:'+'0'*64]))
test('decision_authority_changed_to_human',lambda q:q['decisions'][0]['authority'].update(kind='human'))
test('decision_dangling_supersedes',lambda q:q['decisions'][0].update(supersedes=['dec:'+'0'*64]))
test('override_dangling_claim',lambda q:claim(q,'PRODUCT-SCOPE-01')['override'].update(claim_refs=['clm:'+'0'*64]))
test('override_wrong_scope_type',lambda q:claim(q,'PRODUCT-SCOPE-01')['override'].update(scope_ref=q['entities'][0]['id']))
test('attachment_witness_wrong_ref_types',lambda q:q['attachments'][0].update(witness=[{'mapping_ref':q['claims'][0]['id'],'edge_ref':'missing','component_ref':'missing','source_ref':q['claims'][0]['id']}]))
test('axis_dangling_entity',lambda q:scope(q,'LOSS-01')['axes']['product'].update(included=['product:missing']))
test('scope_family_qualifier_erased_language',lambda q:scope(q,'PATIENT-LANG-01').update(axes={}))
test('claim_wrong_raw_field',lambda q:claim(q,'LOSS-01').update(raw_field='safety.common_completely_wrong'))
test('claim_predicate_changed_language',lambda q:claim(q,'PATIENT-LANG-01').update(predicate='safety.common'))
test('claim_variant_links_wrong_existing_claim',lambda q:next(x for x in q['claims'] if x['language']=='ko')['variant'].update(of=q['claims'][0]['id']))
test('claim_id_arbitrarily_changed_with_refs',lambda q:replace_id(q,q['claims'][0]['id'],'clm:'+'0'*64))
test('mapping_rule_wrong_version',lambda q:next(x for x in q['mappings'] if x['rule'])['rule'].update(version='incorrect-version'))
test('mapping_drop_exact_selection',lambda q:next(x for x in q['mappings'] if x['purpose']=='identity' and x['rule'] and x['rule']['id']=='step7-apply.py').update(selected_refs=[]))
test('snapshot_source_kind_wrong',lambda q:q['snapshots'][0].update(source_kind='research'))
test('source_native_id_wrong',lambda q:next(x for x in q['source_records'] if x['native_id']).update(native_id='wrong-native-id'))
test('combo_scope_container_erased',lambda q:q['scopes'][7].update(axes={}))
test('timing_days_false_instead_of_null',lambda q:next(x for x in q['relation_claims'] if x['relation_kind']=='timing')['field_conditions']['days'].update(value=False))
test('timing_interval_changed',lambda q:next(x for x in q['relation_claims'] if x['relation_kind']=='timing')['interval'].update(min=0,max=0,unit='day'))
test('relation_direction_unfounded',lambda q:next(x for x in q['relation_claims'] if x['arity']==3).update(direction='directed'))
test('case_wrong_claim_ref_existing',lambda q:case(q,'PATIENT-LANG-01').update(attachment_refs=[q['attachments'][0]['id']]))
test('scope_unknown_to_explicit_language',lambda q:scope(q,'PATIENT-LANG-01').update(application_state='explicit'))
test('schema_bool_in_integer_arity',lambda q:q['relation_claims'][0].update(arity=True))
test('schema_number_in_raw_value',lambda q:q['source_records'][0].update(raw_value=0))
dump('additional-probes.json',out)
old=v.mutation_tests(p)
write('existing-mutations.json',old)
write('probe-summary.json',{'review_positive_passed':out[0]['accepted'],'existing_mutations_total':len(old),'existing_rejected':sum(x['rejected'] for x in old),'review_mutations_total':len(out)-1,'review_rejected':sum(not x['accepted'] for x in out[1:]),'denominator':'31 historical mutations + 24 review mutations = 55 executions; overlapping semantic mechanisms are not claimed as 55 independent fault classes'})
print(json.dumps(read(O/'probe-summary.json')))
assert out[0]['accepted'] and all(not x['accepted'] for x in out[1:]) and all(x['rejected'] for x in old)
