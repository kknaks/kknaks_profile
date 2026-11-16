"""Rehash modified records before validation: integrity IDs cannot mask semantic holes."""
import copy,json
from common import *
from identity import revise
from validate import safe_validate
from project import project
p=read(O/'pilot.json');out=[]
def case(q,cid):return next(c for c in q['cases'] if c['id']==cid)
def record(q,g,rid):return next(c for c in q[g] if c['id']==rid)
def claim(q,cid):return record(q,'claims',case(q,cid)['claim_refs'][0])
def scope(q,cid):return record(q,'scopes',case(q,cid)['scope_refs'][0])
def timing(q):return next(r for r in q['relation_claims'] if r['relation_kind']=='timing')
def test(name,mut):
 q=copy.deepcopy(p);mut(q);revise(q);checks=safe_validate(q,project(q));failed=[c for c in checks if not c['pass']]
 out.append({'probe':name,'rejected':bool(failed),'failed_checks':failed,'id_integrity_only_rejection':bool(failed) and all(c['check']=='normalized_revision_id' for c in failed)})
test('language_family_erased',lambda q:scope(q,'PATIENT-LANG-01').update(axes={}))
test('language_application_promoted',lambda q:scope(q,'PATIENT-LANG-01').update(application_state='explicit'))
test('language_predicate_changed',lambda q:claim(q,'PATIENT-LANG-01').update(predicate='safety.common'))
test('language_variant_wrong_parent',lambda q:next(c for c in q['claims'] if c['language']=='ko')['variant'].update(of=q['claims'][0]['id']))
test('combo_container_erased',lambda q:q['scopes'][7].update(axes={}))
test('timing_zero_days_invented',lambda q:timing(q)['interval'].update(min=0,max=0,unit='day'))
test('nary_direction_invented',lambda q:next(r for r in q['relation_claims'] if r['arity']==3).update(direction='directed'))
test('exact_selection_erased',lambda q:next(m for m in q['mappings'] if m['state']=='exact' and m['rule']) .update(selected_refs=[]))
test('exact_all_held',lambda q:[m.update(state='unresolved',selected_refs=[]) for m in q['mappings'] if m['state']=='exact'])
test('rule_version_changed',lambda q:next(m for m in q['mappings'] if m['rule'])['rule'].update(version='wrong'))
test('rule_id_changed',lambda q:next(m for m in q['mappings'] if m['rule'])['rule'].update(id='step5-apply.py'))
test('rule_hash_changed',lambda q:next(m for m in q['mappings'] if m['rule'])['rule'].update(code_sha256='0'*64))
test('native_id_changed',lambda q:next(r for r in q['source_records'] if r['native_id']).update(native_id='wrong'))
test('raw_snapshot_as_generated',lambda q:q['snapshots'][0].update(source_kind='generated'))
test('human_without_reviewer',lambda q:q['decisions'][0]['authority'].update(kind='human'))
test('human_with_invented_reviewer',lambda q:q['decisions'][0]['authority'].update(kind='human',reviewer='invented'))
test('decision_existing_wrong_target',lambda q:q['decisions'][0].update(target_refs=[q['claims'][0]['id']]))
test('override_existing_wrong_scope',lambda q:claim(q,'PRODUCT-SCOPE-01')['override'].update(scope_ref=q['scopes'][0]['id']))
test('case_existing_wrong_attachment',lambda q:case(q,'PATIENT-LANG-01').update(attachment_refs=[q['attachments'][0]['id']]))
def forged_witness(q):
 a=q['attachments'][0];m=next(m for m in q['mappings'] if m['state']=='exact');a['witness']=[{'mapping_ref':m['id'],'source_ref':m['source_refs'][0],'edge_ref':None,'component_ref':None}]
test('witness_real_refs_wrong_target',forged_witness)
write('rehashed-semantic-probes.json',{'total':len(out),'rejected':sum(t['rejected'] for t in out),'probes':out,'scope':'20 additional executions, deliberately overlapping historical semantic probes; all normalized revision IDs recalculated before validation.'})
print(json.dumps({'total':len(out),'rejected':sum(t['rejected'] for t in out),'id_only':sum(t['id_integrity_only_rejection'] for t in out)}))
assert all(t['rejected'] and not t['id_integrity_only_rejection'] for t in out)
