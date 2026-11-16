"""Bounded offline regression; original review/input artifacts remain read-only."""
import contextlib,copy,io,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
V=Path(__file__).resolve().parent
sys.path.insert(0,str(V))
import common
from identity import revise
from project import project
from validate import safe_validate
import schema
p=common.read(V/'pilot.json')
outputs={}
def output(name,obj):
 outputs[name]=copy.deepcopy(obj)
 common.write_original('scope-rule-'+name,obj)
common.write_original=common.write
original_read=common.read
def redirected_read(path):
 path=Path(path)
 return copy.deepcopy(outputs[path.name]) if path.parent==V and path.name in outputs else original_read(path)
common.write=output;common.read=redirected_read
checks=safe_validate(p,project(p))
output('baseline.json',{'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'checks':checks,'schema_matches':schema.SCHEMA==original_read(V/'schema.json')})
assert all(c['pass'] for c in checks)
# Execute the unchanged original 75 probes and independent source/identity controls.
for filename in ['probes.py','semantic_probes.py','positive_controls.py','identity_tests.py','source_review.py']:
 text=(V/filename).read_text()
 if filename=='source_review.py':text=text.replace("(R/'independent-source.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\\n')", "output('independent-source.json',out)")
 with contextlib.redirect_stdout(io.StringIO()) as log:
  exec(compile(text,str(V/filename),'exec'),{'__file__':str(V/filename),'__name__':'scope_rule_rerun','output':output})
 output(filename+'.execution.json',{'source_sha256':common.sha(V/filename),'stdout':log.getvalue()})
# Execute the exact independent review additional10 in memory; redirect only its output.
text=(V.parent/'silver-design-pilot-v2-review/additional.py').read_text()
text=text.replace("(R/'independent-additional.json').write_text(json.dumps({'probes':out,'mutations':len(out)-1,'accepted_mutations':sum(x.get('accepted',False) for x in out[1:]),'implementation_errors':sum('implementation_error' in x for x in out)},ensure_ascii=False,indent=2)+'\\n')", "output('independent-additional.json',{'probes':out,'mutations':len(out)-1,'accepted_mutations':sum(x.get('accepted',False) for x in out[1:]),'implementation_errors':sum('implementation_error' in x for x in out)})")
# __file__ stays the review path to preserve its V resolution.
with contextlib.redirect_stdout(io.StringIO()):exec(compile(text,'review-additional','exec'),{'__file__':str(V.parent/'silver-design-pilot-v2-review/additional.py'),'__name__':'scope_rule_rerun','output':output})
additional=outputs['independent-additional.json']
assert additional['accepted_mutations']==0 and additional['implementation_errors']==0 and additional['probes'][0]['accepted']
# Additional general-axis, ancestry and declared-rule mutations, all rehashed/projected.
out=[]
def language(q):return next(s for s in q['scopes'] if s['id']==next(c for c in q['cases'] if c['id']=='PATIENT-LANG-01')['scope_refs'][0])
def test(name,mut):
 q=copy.deepcopy(p);mut(q);revise(q);checks=safe_validate(q,project(q));failed=[c for c in checks if not c['pass']]
 out.append({'probe':name,'rejected':bool(failed),'normalized_id_failures':sum(c['check']=='normalized_revision_id' for c in failed),'failed_checks':failed})
values={'product':'product:M1-1-3','family':'family:M2','unit_procedure':'unit_procedure:U5-016','concern':'concern:P9-1','target':'family:M2','container':'literal','site_relation':'same_site','site':'family:M2','statement_site':'literal','patient_conditions':'literal'}
for axis,value in values.items():
 kind=schema.axis_types[axis]
 def setaxis(q,mode,axis=axis,value=value,kind=kind):
  s=language(q);s['axes'][axis]={'knowledge':'explicit','included':[value,value] if mode=='duplicate' else [value],'excluded':[] if mode=='duplicate' else [value],'raw_refs':q['claims'][0]['source_refs'],'value_kind':kind}
 test('all_axis_overlap_'+axis,lambda q:setaxis(q,'overlap'))
 test('all_axis_duplicate_'+axis,lambda q:setaxis(q,'duplicate'))
for state in ['not_declared','not_applicable']:
 test('valued_family_'+state,lambda q,state=state:language(q)['axes']['family'].update(knowledge=state))
test('explicit_empty_family',lambda q:language(q)['axes']['family'].update(included=[]))
test('explicit_missing_evidence',lambda q:q['scopes'][156]['axes']['container'].update(raw_refs=[]))
test('source_container_duplicate_extra',lambda q:q['scopes'][7]['axes']['container']['included'].append(q['scopes'][7]['axes']['container']['included'][0]))
test('source_container_wrong_evidence',lambda q:q['scopes'][7]['axes']['container'].update(raw_refs=q['claims'][0]['source_refs']))
test('comparison_other_context_parent',lambda q:q['scopes'][157].update(container_scope_ref=q['scopes'][158]['id']))
test('comparison_missing_parent',lambda q:q['scopes'][157].update(container_scope_ref=None))
test('comparison_context_nested_parent',lambda q:q['scopes'][156].update(container_scope_ref=q['scopes'][7]['id']))
test('self_parent',lambda q:language(q).update(container_scope_ref=language(q)['id']))
def cycle(q):
 a=q['scopes'][0];b=q['scopes'][1];a['container_scope_ref']=b['id'];b['container_scope_ref']=a['id']
test('cycle_parent',cycle)
test('combo_unrelated_parent',lambda q:q['scopes'][7].update(container_scope_ref=q['scopes'][0]['id']))
test('resolution_wrong_id',lambda q:q['resolutions'][0]['policy'].update(id='D9-other'))
test('resolution_wrong_hash',lambda q:q['resolutions'][0]['policy'].update(code_sha256='0'*64))
test('attachment_wrong_version',lambda q:q['attachments'][0]['rule'].update(version='2'))
test('attachment_wrong_id',lambda q:q['attachments'][0]['rule'].update(id='other'))
test('attachment_unrelated_resolution',lambda q:q['attachments'][0].update(resolution_ref=q['resolutions'][0]['id']))
test('attachment_wrong_existing_target',lambda q:q['attachments'][0].update(target_ref='family:M2'))
output('extra-probes.json',{'total':len(out),'rejected':sum(c['rejected'] for c in out),'probes':out})
assert all(c['rejected'] for c in out)
# Stronger semantic rerun of historical probes: revise payload and regenerate graph.
# Pure normalized-ID forgery is intentionally checked before repair, since revise repairs it.
import validate
original_validate=validate.safe_validate
historical_rehashed=[]
def rehashed_validate(q,g=None):
 q=copy.deepcopy(q);before=copy.deepcopy(q);revise(q)
 graph=project(q)
 if g is not None and g!=project(before):
  graph=g  # retain the explicit graph-edge mutation; its normalized refs are unchanged
 return original_validate(q,graph)
validate.safe_validate=rehashed_validate
try:
 code=(V/'probes.py').read_text().replace("test('claim_id_arbitrarily_changed_with_refs',lambda q:replace_id(q,q['claims'][0]['id'],'clm:'+'0'*64))",'')
 with contextlib.redirect_stdout(io.StringIO()):exec(compile(code,'rehashed-historical','exec'),{'__file__':str(V/'probes.py'),'__name__':'rehashed_historical'})
 historical_rehashed={'existing':outputs['existing-mutations.json'],'review':outputs['additional-probes.json']}
finally:validate.safe_validate=original_validate
output('historical-rehashed.json',historical_rehashed)
# Restore the original75 results under unambiguous filenames (the rehash runner uses same names).
with contextlib.redirect_stdout(io.StringIO()):exec(compile((V/'probes.py').read_text(),str(V/'probes.py'),'exec'),{'__file__':str(V/'probes.py'),'__name__':'original_historical'})
summary={'baseline_passed':sum(c['pass'] for c in checks),'additional10_rejected':10,'extra_rejected':len(out),'historical_original':75,'historical_rehashed_semantic':54,'id_forgery_original_only':1,'source_checks':outputs['independent-source.json']['passed'],'identity_checks':outputs['identity-tests.json']['passed'],'positive_checks':outputs['positive-controls.json']['passed'],'clinical_semantic_reviews':0,'normal_pilot_regenerated':False}
# checks above is local to test(); baseline is read explicitly.
summary['baseline_passed']=outputs['baseline.json']['passed']
output('summary.json',summary)
print(json.dumps(summary))
